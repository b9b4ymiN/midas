#!/usr/bin/env python3
"""
discover.py — walk a route's JSON response and suggest fact paths.

The gap this closes: parse_har.py finds the endpoints, but somebody still has
to say "revenue_ttm lives at nodes[2].data.revenueTotal[0]". Doing that by
eyeballing a 400 KB payload is where people give up, or worse, guess.

So: fetch once, walk every leaf, and print the paths whose key names look like
finance fields — plus a ready-to-paste `facts` block. You still confirm the
numbers against the page. The tool proposes; it does not decide.

SvelteKit note: `__data.json` uses a deduplicated wire format where a node's
`data` is a flat array and objects hold integer *indices* into it. --resolve
rebuilds the real object first, so the paths printed are the ones you can
actually use.

Usage:
  discover.py --url "https://site/x/__data.json?x-sveltekit-trailing-slash=1"
  discover.py --file response.json --resolve
  discover.py --url ... --grep revenue,margin,eps --max-depth 6
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Iterator, List, Optional, Tuple

UA = "Mozilla/5.0 (compatible; har-to-api/2.0; research use)"

# Key-name fragments worth surfacing, grouped so the output is readable.
FIELD_GROUPS = {
    "revenue":      r"revenue|sales|turnover",
    "profit":       r"netincome|grossprofit|operatingincome|ebit|ebitda|profit",
    "pershare":     r"\beps\b|pershare|dps|dividendpershare",
    "margin":       r"margin",
    "cashflow":     r"operatingcashflow|freecashflow|\bfcf\b|capex|capitalexp",
    "balance":      r"totaldebt|netcash|netdebt|cashandequiv|totalassets|equity|goodwill",
    "shares":       r"sharesout|sharecount|dilutedshares|weightedshares",
    "valuation":    r"\bpe\b|peratio|pbratio|psratio|evebitda|marketcap|enterprisevalue",
    "returns":      r"\broic\b|\broe\b|\broa\b|\brocе?\b",
    "dates":        r"asof|as_of|fiscal|period|reportdate|updated|date",
    "currency":     r"currency|\bcur\b|reportingcurrency",
}
ALL_RE = re.compile("|".join(FIELD_GROUPS.values()), re.I)


def fetch(url: str, auth_header: Optional[str], token: Optional[str]) -> Any:
    headers = {"User-Agent": UA, "Accept": "application/json"}
    if auth_header and token:
        headers[auth_header] = token
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} — {e.reason}", file=sys.stderr)
        if e.code in (401, 403):
            print("  the session was rejected; log in and re-capture", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(raw.decode("utf-8", "replace"))
    except json.JSONDecodeError as e:
        head = raw[:100].decode("utf-8", "replace").strip()
        print(f"ERROR: not JSON ({e})\n  starts with: {head!r}", file=sys.stderr)
        print("  an HTML body usually means the route moved, the query string is\n"
              "  incomplete, or this is an interstitial (bot check / consent).\n"
              "  Open the URL in a browser to see which — do not assume.", file=sys.stderr)
        sys.exit(2)


def resolve_sveltekit(doc: Any) -> Any:
    """Rebuild SvelteKit's deduplicated __data.json into plain JSON.

    Wire format: each node is {"type":"data","data":[...]} where element 0 is
    the root and every object/array value is an integer index into that same
    flat list. Without this, every path you read is an integer.
    """
    if not isinstance(doc, dict) or doc.get("type") != "data":
        return doc
    nodes = doc.get("nodes")
    if not isinstance(nodes, list):
        return doc

    out_nodes = []
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("data"), list):
            out_nodes.append(node)
            continue
        flat = node["data"]

        def hydrate(idx: Any, seen: Tuple[int, ...] = ()) -> Any:
            if not isinstance(idx, int) or idx < 0 or idx >= len(flat):
                return idx
            if idx in seen:  # cycle guard
                return None
            val = flat[idx]
            seen2 = seen + (idx,)
            if isinstance(val, dict):
                return {k: hydrate(v, seen2) for k, v in val.items()}
            if isinstance(val, list):
                return [hydrate(v, seen2) for v in val]
            return val

        out_nodes.append({**node, "data": hydrate(0)})
    return {**doc, "nodes": out_nodes}


def walk(doc: Any, prefix: str = "", depth: int = 0, max_depth: int = 8) -> Iterator[Tuple[str, Any]]:
    if depth > max_depth:
        return
    if isinstance(doc, dict):
        for k, v in doc.items():
            path = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, (dict, list)):
                yield from walk(v, path, depth + 1, max_depth)
            else:
                yield path, v
    elif isinstance(doc, list):
        # Year-series are lists of scalars and element 0 is the latest period, so
        # three is plenty. Lists of OBJECTS are a different animal: stockanalysis
        # puts seven named sections in one array, and capping at three hid
        # margins, dividends and valuation entirely — the tool reported 57 fields
        # while sitting on top of far more.
        limit = 3 if all(not isinstance(v, (dict, list)) for v in doc) else 24
        for i, v in enumerate(doc[:limit]):
            path = f"{prefix}[{i}]"
            if isinstance(v, (dict, list)):
                yield from walk(v, path, depth + 1, max_depth)
            else:
                yield path, v


def main() -> int:
    p = argparse.ArgumentParser(description="Suggest fact paths from a JSON response")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="Fetch this URL")
    src.add_argument("--file", help="Read this saved JSON file")
    p.add_argument("--auth-header", default=None, help="e.g. Cookie")
    p.add_argument("--token", default=None, help="Value for --auth-header (or set HAR2API_AUTH)")
    p.add_argument("--resolve", action="store_true", help="Force SvelteKit rebuild")
    p.add_argument("--no-resolve", action="store_true", help="Skip the SvelteKit rebuild (debug)")
    p.add_argument("--grep", default=None, help="Comma list of extra key fragments to match")
    p.add_argument("--max-depth", type=int, default=8)
    p.add_argument("--all", action="store_true", help="Print every leaf, not just finance-looking ones")
    p.add_argument("--save", default=None, help="Save the raw response here for re-runs")
    args = p.parse_args()

    if args.url:
        import os
        token = args.token or os.environ.get("HAR2API_AUTH")
        doc = fetch(args.url, args.auth_header, token)
    else:
        with open(args.file, encoding="utf-8") as f:
            doc = json.load(f)

    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
        print(f"raw response saved -> {args.save}\n")

    auto = (not args.no_resolve) and (args.resolve or (isinstance(doc, dict) and doc.get("type") == "data"))
    if auto:
        doc = resolve_sveltekit(doc)
        print("(SvelteKit __data.json detected — rebuilt into plain JSON)\n")

    pattern = ALL_RE
    if args.grep:
        extra = "|".join(re.escape(s.strip()) for s in args.grep.split(",") if s.strip())
        pattern = re.compile(ALL_RE.pattern + ("|" + extra if extra else ""), re.I)

    hits: List[Tuple[str, Any]] = []
    total = 0
    for path, value in walk(doc, max_depth=args.max_depth):
        total += 1
        leaf = path.split(".")[-1]
        if args.all or pattern.search(leaf):
            hits.append((path, value))

    if not hits:
        print(f"No finance-looking fields among {total} leaves.")
        print("Try --all, or --grep with a term you saw on the page.")
        return 1

    print(f"{len(hits)} candidate field(s) out of {total} leaves\n")
    width = max(len(h[0]) for h in hits)
    for path, value in hits:
        shown = value
        if isinstance(value, str) and len(value) > 40:
            shown = value[:40] + "..."
        print(f"  {path.ljust(width)}  = {shown!r}")

    print("\n--- paste into the profile's `facts` map, after checking the numbers "
          "against the page ---")
    # A year-series shows up as foo[0], foo[1], foo[2]. Emitting one line per
    # element produces duplicate keys — invalid as a mapping. Keep the latest
    # period ([0], which every provider seen so far puts first) and name the
    # rest explicitly if you want history.
    seen_names: Dict[str, str] = {}
    series: List[str] = []
    for path, value in hits:
        if not isinstance(value, (int, float)):
            continue
        m = re.match(r"^(.*?)\[(\d+)\]$", path)
        if m and int(m.group(2)) > 0:
            series.append(path)
            continue
        leaf = path.split(".")[-1].split("[")[0]
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", leaf).lower()
        if name in seen_names:
            continue
        seen_names[name] = path
    print('  "facts": {')
    items = list(seen_names.items())
    for i, (name, path) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        print(f'    "{name}": "{path}"{comma}')
    print("  }")
    if series:
        print(f"\n  ({len(series)} further period(s) available on those series, e.g. "
              f"{series[0]} — add them under explicit names like "
              f'"revenue_fy_minus_1" if you need history)')
    print("\nReminder: do NOT add a segment / revenue-mix field here even if one "
          "appears above — that has to come from the filing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
