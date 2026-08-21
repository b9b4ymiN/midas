#!/usr/bin/env python3
"""
fetch.py — the runtime half of har-to-api: pull facts through generated
provider profiles, normalise them, and write a dated snapshot.

Why this exists
---------------
parse_har/gen_client get you *a* client. That is not enough for research work,
where the same number gets read by five different steps hours apart. This layer
adds the three things that make a number trustworthy:

  1. provenance — every fact carries source, tier, as_of and the URL it came
     from. A number with no provenance is treated as absent.
  2. reproducibility — every run writes a dated snapshot; --use-snapshot
     replays it byte-for-byte so you can tell "the data changed" apart from
     "my code changed".
  3. honest failure — a primary source that 401s or times out falls back, but
     the fallback is FLAGGED, never silent. Missing stays missing; nothing is
     inferred.

stdlib only. yfinance is imported lazily and only as a flagged fallback.

Usage
-----
  fetch.py TU.BK --profiles ./profiles --all
  fetch.py TU.BK --need financials,ratios
  fetch.py TU.BK --use-snapshot 2026-08-13     # replay, no network
  fetch.py TU.BK --all --no-fallback           # fail loudly instead of degrading

Exit codes: 0 ok, 1 nothing fetched, 2 profile error, 3 IO error.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

UA = "Mozilla/5.0 (compatible; har-to-api/2.0; research use)"
TIMEOUT = 30
RETRIES = 2
RETRY_SLEEP = 1.5

# Two sources disagreeing by more than this on the same fact is reported,
# never silently resolved. 2% is wide enough to absorb rounding and
# reporting-date drift, tight enough to catch a genuine definition mismatch
# (e.g. one source's ROIC includes goodwill, the other's does not).
CONFLICT_PCT = 2.0

# ---------------------------------------------------------------------------
# Segment / revenue-mix facts: allowed, but never anonymous.
#
# These providers DO expose segments — stockanalysis returns a full
# `revenue-segments` section for Thai Union, sourced from S&P Global, and the
# split cross-checks against the company's own results release. What they do
# NOT do is expose them uniformly: the section is absent for issuers the
# provider has no segment data on, the labels are the provider's rendering of
# the company's reporting (not necessarily verbatim), and history can be
# partial (Thai Union's segment `ttmPrior` is null across the board).
#
# So the rule is provenance, not prohibition. A segment fact must carry the
# segment source tag, and the run must say out loud that the mix should be
# cross-checked against the filing before anything downstream — peer selection,
# driver analysis — is built on it.
# ---------------------------------------------------------------------------
SEGMENT_FACT_RE = re.compile(
    r"(^|_)(segment|segments|revenue_mix|revenue_by|business_unit|division)(_|$)", re.I
)
SEGMENT_MSG = (
    "segment facts carry the provider's own labelling and coverage is uneven "
    "(absent entirely for some issuers) — cross-check the mix against the "
    "filing / IR release before using it for peer selection or driver work"
)
# A breakdown that declares its own total can be checked against it directly,
# so only a real mismatch matters. Without one the sole available check is
# against revenue, and any material gap means parts are missing (GULF's mix
# carries no eliminations line, so it overstates) — hence the tighter bound.
SEGMENT_RECON_PCT = 5.0
SEGMENT_RECON_PCT_NO_TOTAL = 2.0
# The summary row, not a segment. Matched narrowly on purpose: a pattern like
# `(^|_)total(_|$)` also swallows `total_asset_management_revenue`, which is
# the *name of one of Ping An's segments*. Doing so drops a real segment from
# the sum and then divides by it — on 601318 that produced a +1481% "gap".
SEGMENT_TOTAL_NAMES = {"total", "revenue_total", "total_revenue",
                       "segment_total", "revenues_total", "grand_total"}


def _is_segment_total(key: str) -> bool:
    k = key.strip().lower()
    return k in SEGMENT_TOTAL_NAMES or k.endswith("_total")


# ---------------------------------------------------------------------------
# Statement template
#
# A ratio can be arithmetically correct and economically meaningless. ROIC on
# an insurer divides by liabilities that are its raw material, not its
# financing; Ping An's 6.29% answers no question anyone has. P/FCF of 1.36x
# does not mean cheap when the cash flow is mostly policyholder money.
#
# The provider settles this for us: it renders each issuer on a statement
# template and stamps the template into its own field names. Detection is a
# lookup, not a guess. Verified live 2026-08-21 — Ping An `Ins` x9, Ping An
# Bank `Bank` x12, GULF `Uti` x18, TU and AAPL unsuffixed.
#
# Facts are labelled, never dropped: removing them silently would be making
# the reader's judgement for them, which is the habit this layer exists to
# break.
# ---------------------------------------------------------------------------
TEMPLATE_SUFFIX_RE = re.compile(r"(Ins|Bank|Uti)$")
TEMPLATE_BY_SUFFIX = {"Ins": "insurance", "Bank": "bank", "Uti": "utility"}
TEMPLATE_MARKERS = {
    "insurance": ("policyLoans", "reinsuranceRecoverable", "separateAccountAssets",
                  "totalInvestment"),
    "bank": ("grossLoans", "totalDeposits", "loansReceivableNet"),
}
# Ratio families whose economic meaning does not survive the template.
NOT_MEANINGFUL = {
    "insurance": ("roic", "roce", "pfcf", "fcf", "ev_ebitda", "ev_ebit",
                  "debt_ebitda", "net_debt", "current_ratio", "quick_ratio",
                  "asset_turnover", "working_capital", "total_debt", "net_cash"),
    "bank": ("roic", "roce", "pfcf", "fcf", "ev_ebitda", "ev_ebit",
             "debt_ebitda", "net_debt", "current_ratio", "quick_ratio",
             "asset_turnover", "working_capital", "total_debt", "net_cash"),
}
INSTEAD_USE = {
    "insurance": "new business value and its margin, contractual service margin (CSM), "
                 "embedded value, solvency ratios, and return on equity computed on "
                 "equity ATTRIBUTABLE to owners",
    "bank": "net interest margin, cost/income, non-performing loan ratio, CET1, and "
            "return on equity computed on equity ATTRIBUTABLE to owners",
}


def detect_statement_template(doc: Any) -> Optional[str]:
    """Which statement template did the provider render this issuer on?"""
    fd = json_path(doc, "nodes[2].data.financialData")
    if not isinstance(fd, dict):
        return None
    keys = list(fd.keys())
    counts: Dict[str, int] = {}
    for k in keys:
        m = TEMPLATE_SUFFIX_RE.search(k)
        if m:
            counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    if counts:
        suffix = max(counts, key=lambda s: counts[s])
        return TEMPLATE_BY_SUFFIX[suffix]
    for template, markers in TEMPLATE_MARKERS.items():
        if sum(1 for m in markers if m in keys) >= 2:
            return template
    return "standard"


def reconcile_segments(
    seg_rec: Dict[str, Any], revenue: Optional[float]
) -> Dict[str, Any]:
    """Sum a segment breakdown and check it against whatever total exists.

    The standing `cross_check_required` note tells the reader to go and check.
    It does not say how far off the numbers already are, so nobody finds out
    without doing the arithmetic by hand. On GULF.BK (2026-08-21) the TTM
    segments summed 4.8% above revenue — invisible in the output.

    Keys matching SEGMENT_TOTAL_RE are the provider's own summary row and are
    excluded from the parts sum; summing them in doubles the total, which is
    what made TU and AAPL both read as exactly +100% before this existed.
    """
    val = seg_rec.get("value")
    if not isinstance(val, dict):
        return {}

    def num(v: Any) -> bool:
        return isinstance(v, (int, float)) and not isinstance(v, bool)

    parts, declared, declared_key = [], None, None
    for k, v in val.items():
        if k == "datekey" or not num(v):
            continue
        if _is_segment_total(k):
            declared, declared_key = float(v), k
        else:
            parts.append(v)
    if not parts:
        return {}

    # Sanity check on the name match: a total cannot be smaller than the
    # largest single part. If it is, the key was a segment that merely reads
    # like a total — put it back rather than dividing by it.
    if declared is not None and declared < max(parts):
        parts.append(declared)
        declared, declared_key = None, None

    out: Dict[str, Any] = {"segment_sum": float(sum(parts))}
    target, basis, limit = declared, "declared total", SEGMENT_RECON_PCT
    if target is None:
        target, basis, limit = revenue, "revenue_ttm", SEGMENT_RECON_PCT_NO_TOTAL
        out["segment_declared_total"] = None
    else:
        out["segment_declared_total"] = declared

    if not num(target) or not target:
        return out
    out["segment_vs_revenue_delta_pct"] = round(
        (out["segment_sum"] - target) / abs(target) * 100.0, 2
    )
    out["_recon"] = (basis, float(target), limit)
    return out


def _utcnow() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _today() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")


# --- HTTP -------------------------------------------------------------------

class FetchError(Exception):
    def __init__(self, kind: str, detail: str):
        # kind is one of: auth | notfound | network | parse
        self.kind = kind
        self.detail = detail
        super().__init__(f"{kind}: {detail}")


def http_json(url: str, auth_header: Optional[str] = None) -> Any:
    """GET a URL and parse JSON.

    Distinguishes auth failure from "no data" from "network flaked", because
    the three need different human responses: recapture the session, accept the
    gap, or just retry.
    """
    headers = {"User-Agent": UA, "Accept": "application/json"}
    if auth_header:
        token = os.environ.get("HAR2API_AUTH", "")
        if not token:
            raise FetchError(
                "auth",
                f"route needs header {auth_header} but $HAR2API_AUTH is unset — "
                f"re-capture the session and export it",
            )
        headers[auth_header] = token

    last: Optional[Exception] = None
    for attempt in range(RETRIES + 1):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                raw = r.read()
            try:
                return json.loads(raw.decode("utf-8", "replace"))
            except json.JSONDecodeError as e:
                # Do not name a cause we have not established. HTML from a
                # data route has several plausible explanations and picking one
                # confidently is how a guess becomes documentation.
                head = raw[:80].decode("utf-8", "replace").strip()
                looks_html = head.lstrip()[:9].lower().startswith(("<!doctype", "<html"))
                hint = (
                    " — an HTML body from a data route usually means the route "
                    "moved, the query string is incomplete, or the response is "
                    "an interstitial (bot check / consent). Open the URL in a "
                    "browser to see which."
                ) if looks_html else ""
                raise FetchError(
                    "parse",
                    f"response was not JSON ({e}); starts with {head!r}{hint}",
                )
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise FetchError(
                    "auth",
                    f"HTTP {e.code} — session rejected. Log in in the browser, "
                    f"re-capture, and update $HAR2API_AUTH",
                )
            if e.code == 404:
                raise FetchError("notfound", f"HTTP 404 for {url}")
            last = e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = e
        if attempt < RETRIES:
            time.sleep(RETRY_SLEEP * (attempt + 1))
    raise FetchError("network", f"{type(last).__name__}: {last}")


# --- SvelteKit rehydration --------------------------------------------------
# Shared with discover.py so the paths you find there are the paths that work
# here. Imported lazily so fetch.py still runs if discover.py is absent.

def _resolve_framework(doc: Any) -> Any:
    if not (isinstance(doc, dict) and doc.get("type") == "data"):
        return doc
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from discover import resolve_sveltekit
        return resolve_sveltekit(doc)
    except Exception:
        return doc


# --- JSON path --------------------------------------------------------------

def json_path(doc: Any, path: str) -> Any:
    """Dotted path with [i] indexing and [key=value] selection.

    'nodes[2].data.revenueTotal[0]'            positional
    'sections[id=revenue-income].ttm.revenue'  by key — USE THIS for anything
                                               whose position can shift

    Positional indexing into a list of named things is a trap: stockanalysis
    omits the `revenue-segments` section entirely for issuers that have no
    segment data, so `sections[1]` means "segments" for one company and
    "cash & debt" for the next — silently, with plausible numbers. Selecting by
    id costs nothing and cannot mis-bind.

    Returns None if any hop is missing.
    """
    cur = doc
    for token in re.findall(r"[^.\[\]]+|\[[^\]]*\]", path):
        if cur is None:
            return None
        if token.startswith("["):
            inner = token[1:-1]
            if "=" in inner:
                key, _, want = inner.partition("=")
                if not isinstance(cur, list):
                    return None
                cur = next(
                    (el for el in cur
                     if isinstance(el, dict) and str(el.get(key)) == want),
                    None,
                )
            else:
                try:
                    idx = int(inner)
                except ValueError:
                    return None
                if not isinstance(cur, list) or idx >= len(cur):
                    return None
                cur = cur[idx]
        else:
            if isinstance(cur, dict):
                cur = cur.get(token)
            else:
                return None
    return cur


# Composing a period end from fiscal year + fiscal quarter looks tempting and
# is wrong: fiscal labels are not calendar quarters. On 2026-08-21,
# MSFT's balance sheet reported fiscalYear 2026 / Q4 — composing that gives
# 2026-12-31, a date in the future, when the real TTM end was 2026-06-30.
# AAPL's 52/53-week year lands on 2026-06-27, not any quarter end at all.
# So routes borrow the date from a sibling route that publishes a real one
# (see `as_of_from_route`) rather than deriving it.


# --- Fact record ------------------------------------------------------------

def make_fact(
    value: Any,
    source: str,
    tier: str,
    url: str,
    as_of: Optional[str] = None,
    unit: Optional[str] = None,
) -> Dict[str, Any]:
    f = {
        "value": value,
        "source": source,
        "tier": tier,           # "primary" | "FALLBACK"
        "as_of": as_of,
        "url": url,
    }
    # An unknown reporting date is not today's date. Defaulting to the run
    # date silently asserts the figure is current, which for a balance sheet
    # is exactly the claim a reader must not be handed for free.
    if as_of is None:
        f["as_of_status"] = "UNRESOLVED"
    if unit:
        f["unit"] = unit
    return f


# --- Profiles ---------------------------------------------------------------

def load_profiles(directory: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if not os.path.isdir(directory):
        raise FetchError("parse", f"profile directory not found: {directory}")
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json"):
            continue
        p = os.path.join(directory, name)
        try:
            with open(p, encoding="utf-8") as f:
                prof = json.load(f)
        except json.JSONDecodeError as e:
            raise FetchError("parse", f"{name}: {e}")
        pname = prof.get("provider") or os.path.splitext(name)[0]
        out[pname] = prof
    return out


def build_url(route: Dict[str, Any], ticker: str, market: Optional[str]) -> str:
    """Fill the route template. Unfilled placeholders are an error, not a
    silently broken URL."""
    venue = (market or "").lower()
    url = route["url_template"]
    # Some providers address a venue-less listing through a different path
    # shape entirely (stockanalysis: /quote/{market}/{symbol}/ vs US
    # /stocks/{symbol}/). Substituting "" into {market} builds a URL that
    # still returns 200 with a *different* page, so every fact path misses
    # and the run degrades to fallback without ever saying the URL was wrong.
    if not venue and "{market}" in url:
        # A suffixed ticker (GULF.BK, 7203.T) names a non-US venue. Falling
        # back to the venue-less template there would fetch a *different*
        # listing that happens to share the symbol, return 200, and miss
        # every fact path — degrading to fallback without ever saying why.
        if "." in ticker:
            raise FetchError(
                "parse",
                f"'{ticker}' names a non-US venue but --market was not given; "
                f"route {route.get('id')} needs it (e.g. --market bkk). Refusing "
                f"to fetch the US listing for '{ticker.split('.')[0]}' instead.",
            )
        if route.get("url_template_no_market"):
            url = route["url_template_no_market"]
        else:
            raise FetchError(
                "parse",
                f"route {route.get('id')} has a {{market}} segment and the profile "
                f"gives no venue-less template; pass --market",
            )
    symbol = ticker.split(".")[0]
    subs = {
        "symbol": symbol,
        "ticker": ticker,
        "market": venue,
    }
    for k, v in subs.items():
        url = url.replace("{" + k + "}", v)
    if "{" in url:
        missing = re.findall(r"\{([^}]+)\}", url)
        raise FetchError("parse", f"route {route.get('id')} has unfilled params: {missing}")
    # `required_query` is the pre-2026-08-14 spelling; accept it so profiles
    # generated by an older parse_har keep working.
    q = route.get("always_present_query") or route.get("required_query") or {}
    if q:
        sep = "&" if "?" in url else "?"
        url += sep + "&".join(f"{k}={v}" for k, v in q.items())
    return url


# --- Fallback ---------------------------------------------------------------

YF_MAP = {
    "price": ("currentPrice", "regularMarketPrice"),
    "market_cap": ("marketCap",),
    "shares_outstanding": ("sharesOutstanding",),
    "beta": ("beta",),
    "trailing_pe": ("trailingPE",),
    "forward_pe": ("forwardPE",),
    "total_debt": ("totalDebt",),
    "total_cash": ("totalCash",),
    "revenue_ttm": ("totalRevenue",),
}


def yfinance_fallback(ticker: str, wanted: List[str]) -> Dict[str, Dict[str, Any]]:
    """Last resort. Everything it returns is tagged FALLBACK and carries the
    reason, so a reader can see which lines of a report rest on it."""
    try:
        import yfinance as yf  # noqa
    except ImportError:
        return {}
    try:
        info = yf.Ticker(ticker).info or {}
    except Exception as e:  # provider libraries throw a zoo of exceptions
        print(f"  [fallback] yfinance failed: {type(e).__name__}: {e}", file=sys.stderr)
        return {}
    out: Dict[str, Dict[str, Any]] = {}
    for fact in wanted:
        for key in YF_MAP.get(fact, ()):
            if info.get(key) is not None:
                out[fact] = make_fact(
                    info[key], "yfinance", "FALLBACK",
                    f"yfinance:{ticker}.info[{key}]",
                    # yfinance .info is a live snapshot: the run date really
                    # is its as-of, unlike a statement route's period end.
                    as_of=_today(),
                )
                break
    return out


# --- Conflict check ---------------------------------------------------------

def build_alias_index(profiles: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    """fact name -> comparison group, merged across every profile.

    Providers name the same measurement differently — stockanalysis says
    `pe_ratio`, yfinance says `trailing_pe`. Grouping on the literal key means
    those two are never compared, so a 41% disagreement (GULF, 2026-08-21:
    25.27 vs 35.61) passes without a word. Aliases give the comparison
    something to key on.
    """
    index: Dict[str, str] = {}
    for prof in profiles.values():
        for group, members in (prof.get("fact_aliases") or {}).items():
            for name in members:
                index[name] = group
    return index


def check_conflicts(
    per_provider: Dict[str, Dict[str, Dict[str, Any]]],
    aliases: Optional[Dict[str, str]] = None,
) -> List[str]:
    """Compare the same fact across providers. Report, never resolve."""
    warnings: List[str] = []
    aliases = aliases or {}
    names: Dict[str, List[Tuple[str, Any]]] = {}
    labels: Dict[str, List[str]] = {}
    for provider, facts in per_provider.items():
        for fact, rec in facts.items():
            group = aliases.get(fact, fact)
            names.setdefault(group, []).append((provider, rec.get("value"), fact))
            labels.setdefault(group, []).append(fact)
    for group, triples in names.items():
        nums = [(p, v, n) for p, v, n in triples
                if isinstance(v, (int, float)) and not isinstance(v, bool) and v not in (0, None)]
        if len(nums) < 2:
            continue
        base_p, base_v, base_n = nums[0]
        for other_p, other_v, other_n in nums[1:]:
            # Cross-provider only. Two facts from the same provider in one
            # alias group are the same measurement at different dates
            # (total_debt vs total_debt_fy0), not a disagreement — flagging
            # those is noise that teaches the reader to skip these warnings.
            if other_p == base_p:
                continue
            delta = abs(other_v - base_v) / abs(base_v) * 100.0
            if delta > CONFLICT_PCT:
                # Name both original facts when an alias joined them — the
                # reader has to be able to find them in the output.
                lhs = f"{base_p}.{base_n}" if base_n != group else base_p
                rhs = f"{other_p}.{other_n}" if other_n != group else other_p
                warnings.append(
                    f"{group}: {lhs}={base_v} vs {rhs}={other_v} "
                    f"({delta:.1f}% apart, threshold {CONFLICT_PCT}%) — do not "
                    f"pick one silently; state both or find the definition gap"
                )
    return warnings


# --- Snapshot ---------------------------------------------------------------

def snapshot_path(root: str, ticker: str, date: str) -> str:
    return os.path.join(root, ticker, f"{date}.json")


def write_snapshot(root: str, ticker: str, payload: Dict[str, Any]) -> str:
    path = snapshot_path(root, ticker, _today())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return path


# --- Main -------------------------------------------------------------------

def run(args: argparse.Namespace) -> int:
    ticker = args.ticker

    if args.use_snapshot:
        path = snapshot_path(args.data_dir, ticker, args.use_snapshot)
        if not os.path.exists(path):
            print(f"ERROR: no snapshot at {path}", file=sys.stderr)
            return 3
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
        payload.setdefault("warnings", []).append(
            f"REPLAYED from snapshot {args.use_snapshot} — no network was used"
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    profiles = load_profiles(args.profiles)
    if not profiles:
        print(f"ERROR: no profiles in {args.profiles}", file=sys.stderr)
        return 2

    wanted: Optional[set] = None
    if args.need:
        wanted = {s.strip() for s in args.need.split(",") if s.strip()}
        seg_asked = [w for w in wanted if SEGMENT_FACT_RE.search(w)]

    facts: Dict[str, Dict[str, Any]] = {}
    per_provider: Dict[str, Dict[str, Dict[str, Any]]] = {}
    warnings: List[str] = []
    failures: List[Dict[str, str]] = []
    statement_template: Optional[str] = None
    template_url: Optional[str] = None
    template_as_of: Optional[str] = None

    order = args.providers.split(",") if args.providers else list(profiles.keys())

    for pname in order:
        prof = profiles.get(pname.strip())
        if prof is None:
            warnings.append(f"profile '{pname}' not found — skipped")
            continue
        tier = prof.get("tier", "primary")
        got: Dict[str, Dict[str, Any]] = {}
        # period end per route, so a route whose newest column is labelled
        # "TTM" can borrow the real date from a sibling that publishes one
        route_as_of: Dict[str, Optional[str]] = {}

        for route in prof.get("routes", []):
            fact_map = route.get("facts") or {}
            if not fact_map:
                continue
            seg_keys = [k for k in fact_map if SEGMENT_FACT_RE.search(k)]
            if seg_keys:
                warnings.append(f"{pname}/{route.get('id')}: {SEGMENT_MSG}")
            if wanted is not None and not (set(fact_map) & wanted):
                continue

            try:
                url = build_url(route, ticker, args.market)
                auth = (route.get("auth_headers") or [None])[0] if route.get("requires_auth") else None
                doc = http_json(url, auth)
                if route.get("framework_data_route"):
                    doc = _resolve_framework(doc)
            except FetchError as e:
                failures.append({"provider": pname, "route": route.get("id", "?"),
                                 "kind": e.kind, "detail": e.detail})
                if e.kind == "auth":
                    warnings.append(f"{pname}: AUTH FAILED — {e.detail}")
                continue

            as_of = None
            if route.get("as_of_path"):
                v = json_path(doc, route["as_of_path"])
                if isinstance(v, str):
                    as_of = v
            if as_of is None and route.get("as_of_from_route"):
                as_of = route_as_of.get(route["as_of_from_route"])
            if as_of is None and (route.get("as_of_path") or route.get("as_of_from_route")):
                warnings.append(
                    f"{pname}/{route.get('id')}: no reporting period end available — facts from "
                    f"this route are marked as_of UNRESOLVED rather than dated to the run"
                )
            route_as_of[route.get("id")] = as_of

            if statement_template is None:
                statement_template = detect_statement_template(doc)
                if statement_template:
                    template_url, template_as_of = url, as_of

            for fact, path in fact_map.items():
                if wanted is not None and fact not in wanted:
                    continue
                val = json_path(doc, path)
                if val is None:
                    warnings.append(f"{pname}: '{fact}' not present at path '{path}' — left absent")
                    continue
                # NaN/±Inf can only arrive from a devalue sentinel, i.e. the
                # provider said "no value here". Keep it out of fact records
                # and snapshots — a non-finite float is not valid strict JSON
                # and is not a measurement either.
                if isinstance(val, float) and not math.isfinite(val):
                    warnings.append(
                        f"{pname}: '{fact}' resolved to a non-finite value at path '{path}' — left absent"
                    )
                    continue
                rec = make_fact(val, pname, tier, url, as_of,
                                (prof.get("units") or {}).get(fact))
                if SEGMENT_FACT_RE.search(fact):
                    rec["segment_source"] = (
                        json_path(doc, route["segment_source_path"])
                        if route.get("segment_source_path") else "unknown"
                    )
                    rec["cross_check_required"] = SEGMENT_MSG
                got[fact] = rec

        if got:
            per_provider[pname] = got
            for k, v in got.items():
                facts.setdefault(k, v)  # first provider in order wins

    # ---- fallback ---------------------------------------------------------
    if not args.no_fallback:
        missing = sorted((wanted or set(YF_MAP)) - set(facts))
        if missing:
            fb = yfinance_fallback(ticker, missing)
            for k, v in fb.items():
                reason = next(
                    (f"{f['provider']} {f['kind']}: {f['detail'][:70]}" for f in failures),
                    "primary source did not supply this fact",
                )
                v["reason"] = reason
                facts[k] = v
                # Also register it as a provider result, otherwise the
                # fallback source is invisible to check_conflicts and a
                # disagreement between it and the primary is never compared.
                per_provider.setdefault("yfinance", {})[k] = v
                warnings.append(f"{k}: using FALLBACK (yfinance) — {reason}")

    # ---- statement template ------------------------------------------------
    if statement_template:
        facts["statement_template"] = make_fact(
            statement_template, "stockanalysis", "primary",
            template_url or "", template_as_of,
        )
        families = NOT_MEANINGFUL.get(statement_template)
        if families:
            flagged = sorted(
                f for f in facts
                if f != "statement_template" and any(fam in f for fam in families)
            )
            if flagged:
                warnings.append(
                    f"statement_template={statement_template}: the following facts are "
                    f"arithmetically correct but economically meaningless for this "
                    f"business model and must not be used as return or valuation "
                    f"measures — {', '.join(flagged)}. Use instead: "
                    f"{INSTEAD_USE[statement_template]}. They are returned, not dropped; "
                    f"deciding for you is not this layer's job."
                )

    # ---- segment reconciliation -------------------------------------------
    for seg_name in [k for k in facts if SEGMENT_FACT_RE.search(k)]:
        seg_rec = facts[seg_name]
        if not isinstance(seg_rec.get("value"), dict):
            continue
        rev_rec = facts.get("revenue_ttm") or {}
        recon = reconcile_segments(seg_rec, rev_rec.get("value"))
        if not recon:
            continue
        basis_info = recon.pop("_recon", None)
        seg_rec.update(recon)
        if basis_info is None:
            continue
        basis, target, limit = basis_info
        delta = recon["segment_vs_revenue_delta_pct"]
        if abs(delta) > limit:
            warnings.append(
                f"{seg_name}: parts sum to {recon['segment_sum']:,.0f} vs {basis} "
                f"{target:,.0f} — {delta:+.2f}% (threshold ±{limit}%). The "
                f"breakdown does not reconcile"
                + ("" if recon.get("segment_declared_total") is not None else
                   " and the payload declares no total of its own")
                + "; do not present it as a complete mix until the filing "
                  "explains the gap"
            )

    warnings.extend(check_conflicts(per_provider, build_alias_index(profiles)))

    payload = {
        "ticker": ticker,
        "market": args.market,
        "fetched_at": _utcnow(),
        "fact_count": len(facts),
        "fallback_count": sum(1 for f in facts.values() if f["tier"] == "FALLBACK"),
        "facts": facts,
        "failures": failures,
        "warnings": warnings,
        "contract": {
            "every_fact_has_provenance": True,
            "segments_require_cross_check": SEGMENT_MSG,
            "conflict_threshold_pct": CONFLICT_PCT,
        },
    }

    if not args.stdout_only:
        try:
            path = write_snapshot(args.data_dir, ticker, payload)
            payload["snapshot"] = path
        except OSError as e:
            print(f"ERROR: cannot write snapshot: {e}", file=sys.stderr)
            return 3

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if payload["fallback_count"]:
        print(
            f"\n!! {payload['fallback_count']} fact(s) came from the FALLBACK source.\n"
            f"   Carry that flag into the report — do not present them as primary.",
            file=sys.stderr,
        )
    return 0 if facts else 1


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch facts through har-to-api provider profiles")
    p.add_argument("ticker", help="e.g. TU.BK, AAPL")
    p.add_argument("--market", default=None, help="e.g. SET, US (fills {market} in templates)")
    p.add_argument("--profiles", default="./profiles", help="Directory of provider profiles")
    p.add_argument("--providers", default=None, help="Comma list, in precedence order")
    p.add_argument("--need", default=None, help="Comma list of facts (default: everything mapped)")
    p.add_argument("--all", action="store_true", help="Fetch every mapped fact (default)")
    p.add_argument("--data-dir", default="./.data", help="Snapshot root")
    p.add_argument("--use-snapshot", default=None, metavar="YYYY-MM-DD",
                   help="Replay a snapshot instead of hitting the network")
    p.add_argument("--no-fallback", action="store_true",
                   help="Fail loudly rather than degrade to yfinance")
    p.add_argument("--stdout-only", action="store_true", help="Do not write a snapshot")
    args = p.parse_args()

    try:
        return run(args)
    except FetchError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
