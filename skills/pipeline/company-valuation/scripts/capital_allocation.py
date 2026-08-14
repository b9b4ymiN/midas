#!/usr/bin/env python3
"""
capital_allocation.py — the three things about management that the income
statement cannot show you.

Most of what a bad steward of capital does eventually reaches reported profit.
Three things do not, or do not in time to help:

  1. Dilution. Issue shares and revenue is unchanged, operating income is
     unchanged, net income is unchanged — and your claim on all three shrinks.
     No line on the income statement moves. Only the denominator does.

  2. Overpaying for acquisitions. This is the worst of the three, because the
     acquired company's profit CONSOLIDATES: operating income goes UP and the
     year looks like growth. The damage sits in goodwill and in the ROIC
     denominator. The income statement does not merely fail to show it — it
     points the other way.

  3. Related-party leakage. Buying from an affiliate above market price arrives
     as ordinary cost of goods sold, indistinguishable from real input cost.
     Material for family-controlled companies, which is most of the Thai market.

And a fourth reason the three belong together: even when the damage eventually
does reach earnings, it arrives two or three years late. By then you own it.

This is deliberately NOT a new narrative pillar. Return on capital, the
ROIC-WACC spread and buyback yield already live in the financial dashboard and
already cover most of the ground. These are the three gaps, added as one more
metric family — not a new step in the pipeline.

stdlib only.

Usage
-----
  capital_allocation.py --shares 4128,4110,4098,3980,3720 --years 2025,2024,2023,2022,2021
  capital_allocation.py --shares ... --goodwill 12400,12500,4100,4050,4000 \\
                        --total-assets 210000,205000,190000,188000,180000 \\
                        --roic 0.081,0.079,0.112,0.118,0.121 \\
                        --related-party-purchases 8200 --cogs 109000

Exit codes: 0 ok, 1 nothing to compute, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

# Annual dilution above this is worth naming. Modest issuance funds options and
# is normal; sustained issuance is the shareholder paying for the growth.
DILUTION_WARN_PCT = 2.0
DILUTION_BAD_PCT = 5.0

# Goodwill this large a share of assets means the balance sheet is mostly a
# record of prices paid for other companies.
GOODWILL_WARN = 0.20
GOODWILL_BAD = 0.35

# Related-party purchases above this share of COGS deserve the notes read.
RPT_WARN = 0.05
RPT_BAD = 0.15


def parse_list(s: Optional[str]) -> Optional[List[float]]:
    if not s:
        return None
    try:
        return [float(x) for x in s.replace(" ", "").split(",") if x]
    except ValueError:
        return None


def analyse(
    shares: Optional[List[float]],
    years: List[str],
    goodwill: Optional[List[float]],
    assets: Optional[List[float]],
    roic: Optional[List[float]],
    rpt: Optional[float],
    cogs: Optional[float],
) -> Dict[str, Any]:
    out: Dict[str, Any] = {"metrics": {}, "findings": [], "not_available": []}

    # --- 1. dilution ------------------------------------------------------
    if shares and len(shares) >= 2:
        latest, oldest = shares[0], shares[-1]
        n = len(shares) - 1
        total = (latest / oldest - 1.0) * 100.0 if oldest else 0.0
        cagr = ((latest / oldest) ** (1.0 / n) - 1.0) * 100.0 if oldest > 0 and n else 0.0
        yoy = []
        for i in range(len(shares) - 1):
            if shares[i + 1]:
                yoy.append({
                    "period": years[i] if i < len(years) else f"t-{i}",
                    "change_pct": (shares[i] / shares[i + 1] - 1.0) * 100.0,
                })
        out["metrics"]["share_count"] = {
            "latest": latest, "oldest": oldest, "years": n,
            "total_change_pct": total, "annual_pct": cagr, "by_year": yoy,
        }
        if cagr > DILUTION_BAD_PCT:
            out["findings"].append({
                "severity": "high", "metric": "dilution",
                "message": f"share count grew {cagr:.1f}% a year ({total:+.1f}% over {n} years). "
                           f"Per-share results are being diluted faster than most businesses "
                           f"grow. Check what the issuance funded and whether it earned its cost.",
            })
        elif cagr > DILUTION_WARN_PCT:
            out["findings"].append({
                "severity": "medium", "metric": "dilution",
                "message": f"share count grew {cagr:.1f}% a year ({total:+.1f}% over {n} years) "
                           f"— above routine option issuance. Worth knowing what it bought.",
            })
        elif cagr < -1.0:
            out["findings"].append({
                "severity": "info", "metric": "dilution",
                "message": f"share count shrank {abs(cagr):.1f}% a year — buybacks are "
                           f"returning capital. Whether that was the best use of it depends "
                           f"on the price paid.",
            })
    else:
        out["not_available"].append("share count series — dilution cannot be assessed")

    # --- 2. goodwill and acquisition returns ------------------------------
    if goodwill and assets and len(goodwill) == len(assets) and goodwill:
        ratios = [g / a for g, a in zip(goodwill, assets) if a]
        if ratios:
            latest_r = ratios[0]
            out["metrics"]["goodwill_to_assets"] = {
                "latest": latest_r,
                "series": ratios,
                "years": years[:len(ratios)],
            }
            if latest_r > GOODWILL_BAD:
                out["findings"].append({
                    "severity": "high", "metric": "goodwill",
                    "message": f"goodwill is {latest_r:.0%} of total assets — most of the "
                               f"balance sheet records prices paid for other companies rather "
                               f"than productive assets. An impairment here is a restatement "
                               f"of past judgement, not an operating event.",
                })
            elif latest_r > GOODWILL_WARN:
                out["findings"].append({
                    "severity": "medium", "metric": "goodwill",
                    "message": f"goodwill is {latest_r:.0%} of total assets — acquisition-led. "
                               f"Judge management on the returns those deals earn, not on "
                               f"consolidated revenue growth.",
                })
            # a step change in goodwill marks the deal year
            for i in range(len(goodwill) - 1):
                prev = goodwill[i + 1]
                if prev and goodwill[i] / prev > 1.5:
                    yr = years[i] if i < len(years) else f"t-{i}"
                    out["findings"].append({
                        "severity": "info", "metric": "goodwill",
                        "message": f"goodwill jumped {goodwill[i]/prev - 1:.0%} in {yr} — a major "
                                   f"acquisition landed. Compare ROIC before and after.",
                    })
    else:
        out["not_available"].append("goodwill / total assets — acquisition quality cannot be assessed")

    # --- ROIC before vs after ---------------------------------------------
    if roic and len(roic) >= 4:
        half = len(roic) // 2
        recent = sum(roic[:half]) / half
        older = sum(roic[half:]) / (len(roic) - half)
        out["metrics"]["roic_shift"] = {
            "recent_avg": recent, "earlier_avg": older,
            "change_pp": (recent - older) * 100.0,
        }
        if older - recent > 0.02:
            out["findings"].append({
                "severity": "high", "metric": "roic",
                "message": f"ROIC averaged {older:.1%} in the earlier half of the window and "
                           f"{recent:.1%} in the recent half — a fall of "
                           f"{(older-recent)*100:.1f} points. If goodwill rose over the same "
                           f"period, capital was deployed at returns below what the business "
                           f"already earned. Consolidated profit can rise while this happens.",
            })
    elif not roic:
        out["not_available"].append("ROIC series — the returns on deployed capital cannot be compared")

    # --- 3. related-party transactions -------------------------------------
    if rpt is not None and cogs:
        share = rpt / cogs if cogs else 0.0
        out["metrics"]["related_party_share_of_cogs"] = share
        if share > RPT_BAD:
            out["findings"].append({
                "severity": "high", "metric": "related_party",
                "message": f"related-party purchases are {share:.0%} of cost of goods sold. "
                           f"At this size, pricing on those transactions materially sets "
                           f"reported margin. Read the notes for how the prices were set and "
                           f"whether an independent party reviewed them.",
            })
        elif share > RPT_WARN:
            out["findings"].append({
                "severity": "medium", "metric": "related_party",
                "message": f"related-party purchases are {share:.0%} of cost of goods sold — "
                           f"large enough to check the pricing basis in the notes.",
            })
    else:
        out["not_available"].append(
            "related-party purchases / COGS — read the notes to the financial statements; "
            "no data provider exposes this"
        )

    return out


def render(r: Dict[str, Any]) -> str:
    L = ["# Capital allocation — what the income statement cannot show", ""]
    m = r["metrics"]

    if "share_count" in m:
        s = m["share_count"]
        L.append(f"SHARE COUNT   {s['oldest']:,.0f} -> {s['latest']:,.0f} over {s['years']} years")
        L.append(f"              {s['total_change_pct']:+.1f}% total · {s['annual_pct']:+.2f}% a year")
        for y in s["by_year"]:
            L.append(f"                {y['period']:<8} {y['change_pct']:+.2f}%")
        L.append("")
    if "goodwill_to_assets" in m:
        g = m["goodwill_to_assets"]
        L.append(f"GOODWILL / ASSETS   latest {g['latest']:.1%}")
        pairs = list(zip(g["years"], g["series"])) if g["years"] else list(enumerate(g["series"]))
        L.append("              " + "  ".join(f"{y}:{v:.1%}" for y, v in pairs))
        L.append("")
    if "roic_shift" in m:
        rs = m["roic_shift"]
        L.append(f"ROIC          recent half {rs['recent_avg']:.2%} · earlier half "
                 f"{rs['earlier_avg']:.2%}  ({rs['change_pp']:+.1f}pp)")
        L.append("")
    if "related_party_share_of_cogs" in m:
        L.append(f"RELATED PARTY   {m['related_party_share_of_cogs']:.1%} of COGS")
        L.append("")

    if r["findings"]:
        L.append("FINDINGS")
        order = {"high": 0, "medium": 1, "info": 2}
        for f in sorted(r["findings"], key=lambda x: order.get(x["severity"], 3)):
            L.append(f"  [{f['severity'].upper():6}] {f['metric']}")
            L.append(f"           {f['message']}")
        L.append("")
    elif m:
        L.append("No capital-allocation flags on the metrics supplied.")
        L.append("")

    if r["not_available"]:
        L.append("NOT ASSESSED — say so in the report rather than implying it was checked")
        for n in r["not_available"]:
            L.append(f"  - {n}")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(description="Capital-allocation metrics the P&L cannot show")
    p.add_argument("--shares", help="Diluted share count, most recent first")
    p.add_argument("--years", default="", help="Labels, most recent first")
    p.add_argument("--goodwill", help="Goodwill series, most recent first")
    p.add_argument("--total-assets", help="Total assets series, most recent first")
    p.add_argument("--roic", help="ROIC series (0.12 = 12%%), most recent first")
    p.add_argument("--related-party-purchases", type=float, default=None)
    p.add_argument("--cogs", type=float, default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--out", default=None)
    args = p.parse_args()

    shares = parse_list(args.shares)
    goodwill = parse_list(args.goodwill)
    assets = parse_list(args.total_assets)
    roic = parse_list(args.roic)
    if args.shares and shares is None:
        print("ERROR: could not parse --shares", file=sys.stderr)
        return 2
    if goodwill and assets and len(goodwill) != len(assets):
        print("ERROR: --goodwill and --total-assets must be the same length", file=sys.stderr)
        return 2
    years = [y for y in args.years.split(",") if y] if args.years else []

    r = analyse(shares, years, goodwill, assets, roic,
                args.related_party_purchases, args.cogs)
    if not r["metrics"]:
        print("ERROR: nothing to compute — supply at least --shares, or "
              "--goodwill with --total-assets", file=sys.stderr)
        return 1
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)
    print(json.dumps(r, indent=2, ensure_ascii=False) if args.json else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
