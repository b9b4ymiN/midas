#!/usr/bin/env python3
"""
peer_impact.py — rank competitors by whether their actions can actually move
your earnings, not by how similar their business looks.

The distinction this enforces
-----------------------------
A peer set for VALUATION wants companies the market prices with the same logic —
that is what the multiples table needs, and `company-valuation`'s Peer Validation
Gate already handles it correctly.

A peer set for IMPACT wants something different: companies whose decisions change
your margin. The two overlap and are not the same set. A domestic food company
selling unrelated products is a fine valuation comp and irrelevant to your
earnings; a Korean tuna processor competing for the same fish is the reverse.

Three channels, and a candidate must score on at least one:

  supply   buys the same constrained input — their capacity decisions move the
           price you pay. The strongest channel, because it works even when you
           never meet in a market.
  demand   sells to the same buyer or sits on the same shelf — their pricing
           forces yours.
  price    large enough to set the market price you then follow.

Scoring is overlap-weighted: a channel that touches 47% of your revenue is worth
more than the same channel touching 7%. The script ranks and shows its
arithmetic; it does not decide who is a competitor.

Where a supply-channel peer exists and you supply an estimated input price move,
it chains into the same margin arithmetic as business-drivers/sensitivity.py, so
"they add capacity" becomes "we lose N points of margin".

stdlib only.

Usage
-----
  peer_impact.py --candidates peers.json
  peer_impact.py --candidates peers.json --margin 0.0487 --cost-share 0.55 \\
                 --pass-through 0.6 --input-move 0.10

Input format (peers.json)
-------------------------
{
  "company": "TU.BK",
  "segments": {"ambient": 0.472, "frozen": 0.278, "petfood": 0.147},
  "candidates": [
    {"name": "...", "country": "...", "overlaps": ["ambient"],
     "channels": ["supply", "demand"], "evidence": "buys skipjack from WCPO",
     "note": "..."},
    {"name": "...", "country": "...", "overlaps": [],
     "channels": [], "evidence": "sells unrelated categories",
     "rejected_because": "no shared input, no shared shelf, not a price setter"}
  ]
}

Exit codes: 0 ok, 1 no candidate scored, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

# The supply channel scores highest because it does not require the two
# companies to meet in any market — a competitor bidding for the same scarce
# input raises your cost whether or not you compete for a single customer.
CHANNEL_WEIGHT = {"supply": 1.0, "demand": 0.8, "price": 0.6}
CHANNEL_LABEL = {
    "supply": "buys the same constrained input",
    "demand": "sells to the same buyer / same shelf",
    "price": "large enough to set the price you follow",
}


def new_margin(m: float, c: float, x: float, p: float) -> float:
    """Same model as business-drivers/sensitivity.py, kept identical on purpose."""
    denom = 1.0 + c * x * p
    if denom <= 0:
        return float("nan")
    return (m - c * x * (1.0 - p)) / denom


def score(cand: Dict[str, Any], segments: Dict[str, float]) -> Dict[str, Any]:
    overlaps = cand.get("overlaps") or []
    channels = [c for c in (cand.get("channels") or []) if c in CHANNEL_WEIGHT]

    exposure = sum(segments.get(s, 0.0) for s in overlaps)
    unknown = [s for s in overlaps if s not in segments]
    channel_score = max((CHANNEL_WEIGHT[c] for c in channels), default=0.0)
    # Channels beyond the strongest add, but with diminishing effect — two ways
    # of being hurt by the same competitor is worse than one, not twice as bad.
    extra = sum(sorted((CHANNEL_WEIGHT[c] for c in channels), reverse=True)[1:]) * 0.4
    impact = exposure * (channel_score + extra)

    return {
        "name": cand.get("name", "(unnamed)"),
        "country": cand.get("country", ""),
        "overlaps": overlaps,
        "revenue_exposure": exposure,
        "channels": channels,
        "channel_labels": [CHANNEL_LABEL[c] for c in channels],
        "impact_score": impact,
        "evidence": cand.get("evidence", ""),
        "note": cand.get("note", ""),
        "rejected_because": cand.get("rejected_because"),
        "unknown_segments": unknown,
    }


def analyse(doc: Dict[str, Any], margin: Optional[float], cost_share: Optional[float],
            pass_through: Optional[float], input_move: Optional[float]) -> Dict[str, Any]:
    segments: Dict[str, float] = doc.get("segments") or {}
    cands = doc.get("candidates") or []
    warnings: List[str] = []

    if not segments:
        warnings.append(
            "no segment mix supplied — exposure cannot be weighted, so every "
            "candidate scores the same. Take the mix from the filing first; "
            "it is what makes this ranking mean anything."
        )
    else:
        total = sum(segments.values())
        if not 0.8 <= total <= 1.2:
            warnings.append(
                f"segment shares sum to {total:.2f}, not ~1.0 — check whether these "
                f"are shares of gross revenue before eliminations"
            )

    scored = [score(c, segments) for c in cands]
    kept = [s for s in scored if s["channels"] and not s["rejected_because"]]
    rejected = [s for s in scored if not s["channels"] or s["rejected_because"]]
    kept.sort(key=lambda s: s["impact_score"], reverse=True)

    for s in scored:
        if s["unknown_segments"]:
            warnings.append(
                f"{s['name']}: overlaps name segment(s) {s['unknown_segments']} that are "
                f"not in the segment mix — exposure for those counted as zero"
            )
    for s in kept:
        if not s["evidence"]:
            warnings.append(
                f"{s['name']}: kept on a channel claim with no evidence recorded — "
                f"a channel asserted without evidence cannot be argued with"
            )
    for s in rejected:
        if not (s["rejected_because"] or s["evidence"]):
            warnings.append(
                f"{s['name']}: dropped with no reason recorded — write why, so the "
                f"exclusion can be challenged rather than assumed to be an oversight"
            )

    # Chain the supply channel into margin arithmetic when the inputs allow.
    margin_impact = None
    if (margin is not None and cost_share is not None and input_move is not None):
        p = pass_through if pass_through is not None else 0.0
        nm = new_margin(margin, cost_share, input_move, p)
        supply_peers = [s["name"] for s in kept if "supply" in s["channels"]]
        margin_impact = {
            "input_move": input_move,
            "pass_through": p,
            "margin_before": margin,
            "margin_after": nm,
            "delta_pp": (nm - margin) * 100.0,
            "attributable_to": supply_peers,
            "note": "the move is your estimate of what their action does to the "
                    "shared input price; the script does not model that step",
        }
        if not supply_peers:
            warnings.append(
                "margin impact computed but no candidate scored on the supply "
                "channel — check the attribution before using this number"
            )

    return {
        "company": doc.get("company", ""),
        "segments": segments,
        "kept": kept,
        "rejected": rejected,
        "margin_impact": margin_impact,
        "warnings": warnings,
    }


def render(r: Dict[str, Any]) -> str:
    L = [f"# Peers that can move earnings — {r['company'] or '(unnamed)'}", ""]
    if r["segments"]:
        L.append("segment mix: " + " · ".join(f"{k} {v:.1%}" for k, v in r["segments"].items()))
        L.append("")

    if r["kept"]:
        # Width the name column to the longest name rather than truncating to a
        # fixed size — a competitor listed under a clipped name is harder to
        # look up than a slightly wider table is to read.
        w = max(12, min(46, max(len(s["name"]) for s in r["kept"]) + 2))
        L.append(f"{'#':<3}{'competitor':<{w}}{'country':<9}{'exposure':>9}{'score':>7}  channels")
        for i, s in enumerate(r["kept"], 1):
            nm = s["name"] if len(s["name"]) <= w - 2 else s["name"][: w - 3] + "…"
            L.append(f"{i:<3}{nm:<{w}}{s['country'][:8]:<9}"
                     f"{s['revenue_exposure']:>8.1%}{s['impact_score']:>7.2f}  "
                     f"{', '.join(s['channels'])}")
        L.append("")
        for s in r["kept"]:
            L.append(f"  {s['name']}")
            for c in s["channels"]:
                L.append(f"    · {c}: {CHANNEL_LABEL[c]}")
            if s["evidence"]:
                L.append(f"    evidence: {s['evidence']}")
            if s["note"]:
                L.append(f"    note: {s['note']}")
            L.append("")
    else:
        L.append("No candidate scored on any impact channel.")
        L.append("Either the search was too narrow, or this company genuinely has no")
        L.append("competitor whose actions reach its margin. Say which.")
        L.append("")

    L.append("CONSIDERED AND DROPPED — write these down, or the reader cannot tell")
    L.append("a thorough search from a short one")
    if r["rejected"]:
        wr = max(12, min(46, max(len(s["name"]) for s in r["rejected"]) + 2))
        for s in r["rejected"]:
            why = s["rejected_because"] or "no impact channel identified"
            L.append(f"  {s['name']:<{wr}} {why}")
    else:
        L.append("  (none recorded — if nothing was considered and dropped, the")
        L.append("   candidate list was probably drawn too narrowly)")
    L.append("")

    mi = r["margin_impact"]
    if mi:
        L.append("IF THE SHARED INPUT MOVES")
        L.append(f"  input {mi['input_move']:+.0%} at {mi['pass_through']:.0%} pass-through")
        L.append(f"  margin {mi['margin_before']:.2%} -> {mi['margin_after']:.2%} "
                 f"({mi['delta_pp']:+.2f}pp)")
        if mi["attributable_to"]:
            L.append(f"  supply-channel peers: {', '.join(mi['attributable_to'])}")
        L.append(f"  {mi['note']}")
        L.append("")

    if r["warnings"]:
        L.append("WARNINGS")
        for w in r["warnings"]:
            L.append(f"  ! {w}")
        L.append("")

    L.append("NOT A VALUATION PEER SET — the multiples table needs companies the")
    L.append("market prices with the same logic, which is a different question and")
    L.append("already handled by company-valuation's Peer Validation Gate.")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(description="Rank peers by earnings impact, not similarity")
    p.add_argument("--candidates", required=True, help="JSON file (see module docstring)")
    p.add_argument("--margin", type=float, default=None, help="Your operating margin")
    p.add_argument("--cost-share", type=float, default=None,
                   help="Shared input's share of your revenue")
    p.add_argument("--pass-through", type=float, default=None)
    p.add_argument("--input-move", type=float, default=None,
                   help="Your estimate of the input price move their action causes")
    p.add_argument("--json", action="store_true")
    p.add_argument("--out", default=None)
    args = p.parse_args()

    try:
        with open(args.candidates, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if not isinstance(doc, dict):
        print("ERROR: candidates file must be a JSON object", file=sys.stderr)
        return 2

    r = analyse(doc, args.margin, args.cost_share, args.pass_through, args.input_move)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)
    print(json.dumps(r, indent=2, ensure_ascii=False) if args.json else render(r))
    return 0 if r["kept"] else 1


if __name__ == "__main__":
    sys.exit(main())
