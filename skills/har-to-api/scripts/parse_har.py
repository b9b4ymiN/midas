#!/usr/bin/env python3
"""
parse_har.py — Stream-parse a HAR file, filter noise, extract API endpoints.

v2 changes (see references/CHANGELOG.md):
  - Error responses (4xx/5xx) are quarantined, not emitted as endpoints.
    A HAR captured after a session cookie expired used to produce a "working"
    spec whose every call 401s. Now it says so.
  - Path params get unique names (symbol, symbol2, ...) instead of colliding.
  - Query params are marked by how often they appeared, so params the browser
    always sends (SvelteKit's x-sveltekit-trailing-slash) survive into the
    generated client instead of being dropped as "samples". NOTE: frequency is
    evidence of what the browser sends, NOT proof the server requires it — the
    profile key is named always_present_query for that reason.
  - Known data-framework routes (SvelteKit __data.json, Next.js _next/data)
    are recognised rather than filtered as static assets.
  - --profile emits a fetch.py provider profile in addition to endpoints.json.

Design goals (unchanged):
- stdlib only, no dependencies.
- Noise filtering happens BEFORE we keep anything.
- Auth header VALUES are never written anywhere.

Usage:
    python parse_har.py <input.har> [--out endpoints.json] [--host-filter example.com]
                        [--profile provider.json] [--provider-name stockanalysis]
                        [--keep-errors]

Exit codes: 0 ok, 2 no endpoints found, 3 bad HAR, 4 IO error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import parse_qsl, urlparse

# --- Noise filters ---------------------------------------------------------

NOISE_CONTENT_TYPES = (
    "image/", "font/", "text/css", "text/html",
    "application/javascript", "application/x-javascript",
    "application/manifest+json", "application/vnd.ms-fontobject",
    "application/octet-stream",
)

NOISE_HOST_RE = re.compile(
    r"(google-analytics|googletagmanager|doubleclick|googlesyndication|"
    r"facebook\.com|facebook\.net|fbcdn|hotjar|clarity\.ms|segment\.io|"
    r"mixpanel|amplitude\.com|sentry\.io|datadome|cloudflareinsights|"
    r"newrelic|nr-data|scorecardresearch|quantserve|adnxs|criteo)",
    re.I,
)

NOISE_PATH_RE = re.compile(
    r"(\.(?:png|jpg|jpeg|gif|webp|svg|ico|css|js|mjs|map|woff2?|ttf|eot|mp4|webm)"
    r"$|/sentry/|/beacon|/track|/analytics|/_next/static/|/static/|/assets/)",
    re.I,
)

# v2: data-framework routes that LOOK static but are the real data API.
#   SvelteKit  → /path/__data.json          (stockanalysis.com uses this)
#   Next.js    → /_next/data/<build>/....json
# These must be checked BEFORE NOISE_PATH_RE, which would drop them on the
# ".json"-adjacent /_next/ prefix or a trailing static-ish segment.
FRAMEWORK_DATA_RE = re.compile(
    r"(/__data\.json|/_next/data/[^/]+/.*\.json)",
    re.I,
)

SENSITIVE_HEADER_RE = re.compile(
    r"(authorization|cookie|set-cookie|x-api-key|x-auth-token|x-csrf-token|"
    r"csrf-token|x-session|x-amz-security-token)",
    re.I,
)

MAX_BODY_SAMPLE = 8192

# v2: statuses that mean "this capture is not usable as an endpoint".
AUTH_STATUSES = {401, 403}


def _is_framework_data(url: str) -> bool:
    return bool(FRAMEWORK_DATA_RE.search(urlparse(url).path))


def _is_noise(url: str, content_type: str) -> bool:
    if _is_framework_data(url):
        return False  # v2: never filter the real data route
    if NOISE_HOST_RE.search(url):
        return True
    if NOISE_PATH_RE.search(url):
        return True
    ct = (content_type or "").lower()
    if any(ct.startswith(prefix) for prefix in NOISE_CONTENT_TYPES):
        return True
    return False


def _looks_like_api(url: str, content_type: str, status: int) -> bool:
    if _is_framework_data(url):
        return True  # v2
    ct = (content_type or "").lower()
    if "json" in ct or "xml" in ct or "graphql" in ct:
        return True
    path = urlparse(url).path.lower()
    if any(seg in path for seg in ("/api/", "/graphql", "/v1/", "/v2/", "/rpc/")):
        return True
    if 200 <= status < 400 and ("json" in ct or ct == ""):
        return True
    return False


# --- Path normalization ----------------------------------------------------

_INT_ID_RE = re.compile(r"^\d{2,}$")
_HEX_ID_RE = re.compile(r"^[0-9a-f]{8,}$", re.I)
# Ticker-ish: PTT, PTT.BK, BRK.B, BTC-USD. Must be all-caps to avoid eating
# lowercase route segments like "bkk", "stocks", "financials".
_TICKERISH_RE = re.compile(r"^[A-Z]{1,6}([.\-][A-Z]{1,4})?$")

# Segments that are all-caps but are route words, not symbols.
_CAPS_ROUTE_WORDS = {"API", "V1", "V2", "US", "ETF", "IPO", "TTM", "PDF", "CSV"}


def _normalize_path(path: str) -> Tuple[str, List[Dict[str, str]]]:
    """Return (template_path, [extracted_params]).

    v2: param names are made unique. Two ticker segments in one path used to
    both become {symbol}, producing an unbuildable URL template.
    """
    params: List[Dict[str, str]] = []
    seen: Dict[str, int] = {}

    def _uniq(base: str) -> str:
        seen[base] = seen.get(base, 0) + 1
        return base if seen[base] == 1 else f"{base}{seen[base]}"

    out: List[str] = []
    for seg in path.split("/"):
        if not seg:
            out.append(seg)
            continue
        if _INT_ID_RE.match(seg) or _HEX_ID_RE.match(seg):
            key = _uniq("id")
        elif (
            _TICKERISH_RE.match(seg)
            and len(seg) <= 12
            and seg.upper() not in _CAPS_ROUTE_WORDS
        ):
            key = _uniq("symbol")
        else:
            out.append(seg)
            continue
        out.append("{" + key + "}")
        params.append({"name": key, "in": "path", "value_sample": seg, "required": True})
    return "/".join(out), params


def _redact_headers(headers: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    out = []
    for h in headers:
        name = h.get("name", "")
        if SENSITIVE_HEADER_RE.search(name):
            out.append({"name": name, "value": "<redacted>", "_sensitive": True})
        else:
            out.append({"name": name, "value": h.get("value", "")})
    return out


def _sample_body(content: Optional[Dict[str, Any]]) -> Optional[str]:
    if not content:
        return None
    text = content.get("text") or ""
    if not text:
        return None
    if len(text) > MAX_BODY_SAMPLE:
        return text[:MAX_BODY_SAMPLE] + f"\n...<truncated {len(text) - MAX_BODY_SAMPLE} bytes>"
    return text


# --- Core parser -----------------------------------------------------------

def parse_har(
    har_path: str,
    host_filter: Optional[str] = None,
    keep_errors: bool = False,
) -> Dict[str, Any]:
    try:
        with open(har_path, "r", encoding="utf-8") as f:
            har = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: HAR file not found: {har_path}", file=sys.stderr)
        sys.exit(4)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid HAR JSON: {e}", file=sys.stderr)
        sys.exit(3)

    entries = har.get("log", {}).get("entries", [])
    if not entries:
        print("ERROR: HAR has no entries (log.entries empty)", file=sys.stderr)
        sys.exit(3)

    endpoints: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
    # v2: query-param frequency per endpoint key, to decide required vs optional
    qp_counts: Dict[str, Dict[str, int]] = {}
    quarantined: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()

    stats = {
        "total_entries": len(entries),
        "dropped_noise": 0,
        "dropped_non_api": 0,
        "quarantined_auth": 0,
        "quarantined_error": 0,
        "kept": 0,
        "duplicates_merged": 0,
        "hosts_seen": set(),
    }

    for entry in entries:
        req = entry.get("request", {})
        res = entry.get("response", {})
        url = req.get("url", "")
        if not url:
            continue

        parsed = urlparse(url)
        stats["hosts_seen"].add(parsed.netloc)

        if host_filter and host_filter.lower() not in parsed.netloc.lower():
            continue

        req_headers = req.get("headers", [])
        res_headers = res.get("headers", [])
        ct = ""
        for h in res_headers:
            if h.get("name", "").lower() == "content-type":
                ct = h.get("value", "")
                break

        status = res.get("status", 0)

        if _is_noise(url, ct):
            stats["dropped_noise"] += 1
            continue
        if not _looks_like_api(url, ct, status):
            stats["dropped_non_api"] += 1
            continue

        method = req.get("method", "GET").upper()
        template_path, path_params = _normalize_path(parsed.path)
        key = f"{method} {parsed.scheme}://{parsed.netloc}{template_path}"

        # ---- v2: quarantine error responses -------------------------------
        if not keep_errors and status >= 400:
            bucket = "quarantined_auth" if status in AUTH_STATUSES else "quarantined_error"
            stats[bucket] += 1
            if key not in quarantined:
                quarantined[key] = {
                    "method": method,
                    "url_template": f"{parsed.scheme}://{parsed.netloc}{template_path}",
                    "status": status,
                    "reason": (
                        "auth rejected — capture again after logging in, or the "
                        "session cookie expired mid-capture"
                        if status in AUTH_STATUSES
                        else f"server returned {status}"
                    ),
                    "occurrences": 1,
                }
            else:
                quarantined[key]["occurrences"] += 1
            continue

        query_pairs = parse_qsl(parsed.query, keep_blank_values=True)
        counts = qp_counts.setdefault(key, {})
        for name, _v in query_pairs:
            counts[name] = counts.get(name, 0) + 1

        if key in endpoints:
            endpoints[key]["occurrences"] += 1
            stats["duplicates_merged"] += 1
            # remember any query param we had not seen on the first occurrence
            known = {p["name"] for p in endpoints[key]["parameters"] if p.get("in") == "query"}
            for name, value in query_pairs:
                if name not in known:
                    endpoints[key]["parameters"].append(
                        {"name": name, "value_sample": value, "in": "query", "required": False}
                    )
                    known.add(name)
            continue

        query_params = [
            {"name": n, "value_sample": v, "in": "query", "required": False}
            for n, v in query_pairs
        ]

        auth_headers = [
            h["name"] for h in req_headers if SENSITIVE_HEADER_RE.search(h.get("name", ""))
        ]

        endpoints[key] = {
            "id": f"op{len(endpoints) + 1}",
            "method": method,
            "scheme": parsed.scheme,
            "host": parsed.netloc,
            "template_path": template_path,
            "original_url": url,
            "status": status,
            "content_type": ct,
            "framework_data_route": _is_framework_data(url),
            "parameters": path_params + query_params,
            "auth_headers": sorted(set(auth_headers)),
            "requires_auth": bool(auth_headers),
            "request_headers_sample": _redact_headers(req_headers)[:8],
            "request_body_sample": _sample_body(req.get("postData")),
            "response_body_sample": _sample_body(res.get("content")),
            "response_size": res.get("content", {}).get("size", 0),
            "occurrences": 1,
        }
        stats["kept"] += 1

    # ---- v2: flag query params present on EVERY occurrence -----------------
    # This measures the CAPTURE, not the server. A param the browser always
    # sends may still be optional; verify by dropping it and re-requesting.
    # Calling this field `required` once led to a documented claim that the
    # stockanalysis __data.json routes need x-sveltekit-trailing-slash=1. They
    # do not — see references/CHANGELOG.md, "Correction: a requirement I never
    # tested".
    for key, ep in endpoints.items():
        total = ep["occurrences"]
        counts = qp_counts.get(key, {})
        for p in ep["parameters"]:
            if p.get("in") == "query":
                p["required"] = counts.get(p["name"], 0) >= total

    stats["hosts_seen"] = sorted(stats["hosts_seen"])

    return {
        "summary": stats,
        "endpoints": list(endpoints.values()),
        "quarantined": list(quarantined.values()),
    }


# --- v2: provider profile emitter -----------------------------------------

def to_profile(result: Dict[str, Any], provider_name: str) -> Dict[str, Any]:
    """Emit a fetch.py provider profile.

    Deliberately leaves `facts` empty: mapping an endpoint's JSON to canonical
    fact names is a judgement call a human (or the agent) makes after looking
    at the response sample. Guessing it here would be exactly the kind of
    silent invention the data layer exists to prevent.
    """
    routes = []
    for ep in result["endpoints"]:
        req_q = {
            p["name"]: p.get("value_sample", "")
            for p in ep["parameters"]
            if p.get("in") == "query" and p.get("required")
        }
        routes.append(
            {
                "id": ep["id"],
                "method": ep["method"],
                "url_template": f"{ep['scheme']}://{ep['host']}{ep['template_path']}",
                # Present on every captured occurrence — send them, but do not
                # read this as "the server rejects the request without them".
                "always_present_query": req_q,
                "path_params": [
                    p["name"] for p in ep["parameters"] if p.get("in") == "path"
                ],
                "requires_auth": ep["requires_auth"],
                "auth_headers": ep["auth_headers"],
                "framework_data_route": ep.get("framework_data_route", False),
                "facts": {},  # fill in manually: {"revenue_ttm": "json.path.here"}
            }
        )
    return {
        "provider": provider_name,
        "tier": "primary",
        "generated_from": "har-to-api parse_har.py v2",
        "routes": routes,
        "notes": [
            "Fill each route's `facts` map before fetch.py can use it.",
            "NEVER map a segment/revenue-mix fact here — segment data is not "
            "reliably exposed by these APIs; it must come from the filing.",
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Parse HAR -> normalized endpoint list")
    p.add_argument("har", help="Path to .har file")
    p.add_argument("--out", default="endpoints.json", help="Output JSON path")
    p.add_argument("--host-filter", default=None, help="Only keep this host substring")
    p.add_argument("--profile", default=None, help="Also write a fetch.py provider profile here")
    p.add_argument("--provider-name", default="provider", help="Name for --profile output")
    p.add_argument(
        "--keep-errors",
        action="store_true",
        help="Keep 4xx/5xx responses as endpoints (default: quarantine them)",
    )
    p.add_argument("--quiet", action="store_true", help="Only emit warnings/errors")
    args = p.parse_args()

    result = parse_har(args.har, args.host_filter, args.keep_errors)

    if not result["endpoints"]:
        print(
            "WARNING: No API endpoints found. The site may be server-rendered "
            "(no XHR/fetch calls) or all traffic was filtered as noise.",
            file=sys.stderr,
        )

    try:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        if args.profile:
            with open(args.profile, "w", encoding="utf-8") as f:
                json.dump(to_profile(result, args.provider_name), f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"ERROR: cannot write output: {e}", file=sys.stderr)
        return 4

    if not args.quiet:
        s = result["summary"]
        print(f"Parsed {s['total_entries']} entries")
        print(f"  kept:              {s['kept']}")
        print(f"  dropped (noise):   {s['dropped_noise']}")
        print(f"  dropped (non-api): {s['dropped_non_api']}")
        print(f"  duplicates merged: {s['duplicates_merged']}")
        print(f"  unique endpoints:  {len(result['endpoints'])}")
        print(f"  hosts seen:        {', '.join(s['hosts_seen']) or '(none)'}")
        if s["quarantined_auth"]:
            print(
                f"\n  !! {s['quarantined_auth']} request(s) came back 401/403.\n"
                f"     Your session was not valid for those calls. Log in in the\n"
                f"     browser, then capture again — do NOT ship a spec built from\n"
                f"     rejected responses."
            )
        if s["quarantined_error"]:
            print(f"  !! {s['quarantined_error']} request(s) returned 4xx/5xx (see 'quarantined')")
        print(f"  -> {args.out}")
        if args.profile:
            print(f"  -> {args.profile}  (fill in each route's `facts` map before use)")
    return 0 if result["endpoints"] else 2


if __name__ == "__main__":
    sys.exit(main())
