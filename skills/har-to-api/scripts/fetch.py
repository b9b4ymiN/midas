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
                # Very common failure: a framework data route without its
                # required query param quietly serves HTML instead of JSON.
                head = raw[:80].decode("utf-8", "replace").strip()
                raise FetchError(
                    "parse",
                    f"response was not JSON ({e}); starts with {head!r} — check "
                    f"the route's required query params",
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
        "as_of": as_of or _today(),
        "url": url,
    }
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
    url = route["url_template"]
    symbol = ticker.split(".")[0]
    subs = {
        "symbol": symbol,
        "ticker": ticker,
        "market": (market or "").lower(),
    }
    for k, v in subs.items():
        url = url.replace("{" + k + "}", v)
    if "{" in url:
        missing = re.findall(r"\{([^}]+)\}", url)
        raise FetchError("parse", f"route {route.get('id')} has unfilled params: {missing}")
    q = route.get("required_query") or {}
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
                )
                break
    return out


# --- Conflict check ---------------------------------------------------------

def check_conflicts(per_provider: Dict[str, Dict[str, Dict[str, Any]]]) -> List[str]:
    """Compare the same fact across providers. Report, never resolve."""
    warnings: List[str] = []
    names: Dict[str, List[Tuple[str, Any]]] = {}
    for provider, facts in per_provider.items():
        for fact, rec in facts.items():
            names.setdefault(fact, []).append((provider, rec.get("value")))
    for fact, pairs in names.items():
        nums = [(p, v) for p, v in pairs if isinstance(v, (int, float)) and v not in (0, None)]
        if len(nums) < 2:
            continue
        base_p, base_v = nums[0]
        for other_p, other_v in nums[1:]:
            delta = abs(other_v - base_v) / abs(base_v) * 100.0
            if delta > CONFLICT_PCT:
                warnings.append(
                    f"{fact}: {base_p}={base_v} vs {other_p}={other_v} "
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

    order = args.providers.split(",") if args.providers else list(profiles.keys())

    for pname in order:
        prof = profiles.get(pname.strip())
        if prof is None:
            warnings.append(f"profile '{pname}' not found — skipped")
            continue
        tier = prof.get("tier", "primary")
        got: Dict[str, Dict[str, Any]] = {}

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

            for fact, path in fact_map.items():
                if wanted is not None and fact not in wanted:
                    continue
                val = json_path(doc, path)
                if val is None:
                    warnings.append(f"{pname}: '{fact}' not present at path '{path}' — left absent")
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
                warnings.append(f"{k}: using FALLBACK (yfinance) — {reason}")

    warnings.extend(check_conflicts(per_provider))

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
