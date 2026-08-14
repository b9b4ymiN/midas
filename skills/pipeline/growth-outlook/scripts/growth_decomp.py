#!/usr/bin/env python3
"""
growth_decomp.py — break reported revenue growth into its sources, and judge
how much of it is repeatable.

"Revenue grew 12%" is not information. Twelve percent from selling more units
is a different company from twelve percent from a currency move, and they
deserve different terminal assumptions. This splits the number and grades each
part by whether it can happen again next year.

Ordering matters. Volume is compounded first, then price on top of the larger
base, then expansion, acquisition and currency — because that is the order in
which they actually stack, and treating them as additive quietly misstates the
residual. Anything the components do not explain is reported as **unexplained**
rather than distributed among them.

Repeatability grades:

  volume       best        selling more of the same thing
  price        conditional real only if volume held; otherwise cost pass-through
  expansion    finite      works until the market is covered — watch new-unit ROIC
  acquisition  bought      must be bought again; check goodwill and the share count
  fx           not earned  excluded from any growth claim about the business

stdlib only.

Usage
-----
  growth_decomp.py --revenue 132718,138433,136153,155586,141048 \\
                   --years 2025,2024,2023,2022,2021
  growth_decomp.py --revenue 132718,138433 --years 2025,2024 \\
                   --volume-growth 0.03 --price-growth 0.02 --fx-growth -0.01
  growth_decomp.py --revenue ... --acquisition-revenue 4200 --json

Exit codes: 0 ok, 1 not enough data, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

GRADE = {
    "volume": ("best", "selling more of the same thing — the only source that "
                       "compounds without needing anything new"),
    "price": ("conditional", "real pricing power only if volume held; if volume "
                             "fell, this is cost pass-through wearing a growth label"),
    "expansion": ("finite", "works until the addressable market is covered — check "
                            "whether new units earn the returns the old ones do"),
    "acquisition": ("bought", "has to be bought again next year; check goodwill and "
                              "the share count before calling it growth"),
    "fx": ("not earned", "a currency move is not an operating result — exclude it "
                         "from any growth claim about the business"),
}


def parse_list(s: Optional[str]) -> Optional[List[float]]:
    if not s:
        return None
    try:
        return [float(x) for x in s.replace(" ", "").split(",") if x]
    except ValueError:
        return None


def decompose(
    revenue: List[float],
    years: List[str],
    vol: Optional[float],
    price: Optional[float],
    expansion: Optional[float],
    acq_revenue: Optional[float],
    fx: Optional[float],
) -> Dict[str, Any]:
    warnings: List[str] = []
    if len(revenue) < 2:
        return {"error": "need at least two revenue periods"}

    latest, prior = revenue[0], revenue[1]
    if prior == 0:
        return {"error": "prior-period revenue is zero"}
    total_growth = latest / prior - 1.0

    acq = (acq_revenue / prior) if acq_revenue else None

    parts: Dict[str, Optional[float]] = {
        "volume": vol, "price": price, "expansion": expansion,
        "acquisition": acq, "fx": fx,
    }
    given = {k: v for k, v in parts.items() if v is not None}

    # Compound in the order the effects actually stack.
    explained = 1.0
    for key in ("volume", "price", "expansion", "acquisition", "fx"):
        if parts.get(key) is not None:
            explained *= (1.0 + parts[key])
    explained -= 1.0
    unexplained = total_growth - explained if given else None

    if given and unexplained is not None and abs(unexplained) > 0.02:
        warnings.append(
            f"components explain {explained:+.1%} of the {total_growth:+.1%} reported "
            f"— {unexplained:+.1%} is unaccounted for. Find it before treating the "
            f"split as complete; do not spread it across the parts."
        )

    # The price-without-volume test.
    if price is not None and price > 0.005:
        if vol is None:
            warnings.append(
                "price growth is claimed but volume is not given — without it there "
                "is no way to tell pricing power from cost pass-through"
            )
        elif vol < 0:
            warnings.append(
                f"price rose {price:+.1%} while volume fell {vol:+.1%} — this is cost "
                f"pass-through, not pricing power. Treating it as durable growth "
                f"assumes customers keep absorbing increases while already leaving."
            )

    if acq is not None and acq > 0.3 * abs(total_growth) and total_growth > 0:
        warnings.append(
            f"acquisitions supplied {acq/total_growth:.0%} of the growth — check the "
            f"goodwill line and the share count before this counts as performance"
        )
    if fx is not None and abs(fx) > 0.02:
        warnings.append(
            f"currency contributed {fx:+.1%}; organic growth is {total_growth - fx:+.1%}. "
            f"Quote the organic figure."
        )

    # Multi-year context
    history = []
    for i in range(len(revenue) - 1):
        if revenue[i + 1]:
            history.append({
                "period": years[i] if i < len(years) else f"t-{i}",
                "growth": revenue[i] / revenue[i + 1] - 1.0,
            })
    cagr = None
    if len(revenue) >= 3 and revenue[-1] > 0 and latest > 0:
        n = len(revenue) - 1
        cagr = (latest / revenue[-1]) ** (1.0 / n) - 1.0

    if history:
        pos = sum(1 for h in history if h["growth"] > 0)
        if pos and pos < len(history):
            warnings.append(
                f"revenue rose in {pos} of the last {len(history)} periods — growth is "
                f"not established; treat any single-year rate as noise"
            )

    breakdown = []
    for key in ("volume", "price", "expansion", "acquisition", "fx"):
        v = parts.get(key)
        if v is None:
            continue
        grade, why = GRADE[key]
        breakdown.append({
            "source": key, "growth": v,
            "share_of_total": (v / total_growth) if total_growth else None,
            "repeatable": grade, "note": why,
        })

    quality = None
    if given:
        durable = sum(v for k, v in given.items() if k in ("volume", "expansion"))
        quality = durable / total_growth if total_growth else None

    return {
        "years": years[:2],
        "revenue_latest": latest,
        "revenue_prior": prior,
        "total_growth": total_growth,
        "breakdown": breakdown,
        "explained": explained if given else None,
        "unexplained": unexplained,
        "durable_share": quality,
        "history": history,
        "cagr": cagr,
        "warnings": warnings,
    }


def render(r: Dict[str, Any]) -> str:
    if "error" in r:
        return f"ERROR: {r['error']}"
    L = ["# Growth decomposition", ""]
    yl = " vs ".join(r["years"]) if r["years"] else ""
    L.append(f"reported revenue growth {r['total_growth']:+.2%}  {yl}")
    if r.get("cagr") is not None:
        L.append(f"CAGR across the window   {r['cagr']:+.2%}")
    L.append("")

    if r["breakdown"]:
        L.append(f"  {'source':<13}{'growth':>9}{'share':>9}  {'repeatable':<12} why")
        for b in r["breakdown"]:
            share = f"{b['share_of_total']:.0%}" if b["share_of_total"] is not None else "n/a"
            L.append(f"  {b['source']:<13}{b['growth']:>+9.2%}{share:>9}  "
                     f"{b['repeatable']:<12} {b['note'][:52]}")
        L.append("")
        if r["unexplained"] is not None:
            L.append(f"  explained {r['explained']:+.2%} · unexplained {r['unexplained']:+.2%}")
        if r["durable_share"] is not None:
            L.append(f"  durable share (volume + expansion): {r['durable_share']:.0%} of growth")
        L.append("")
    else:
        L.append("No components supplied — only the headline rate is known.")
        L.append("A single growth number cannot be projected forward responsibly:")
        L.append("split it into volume, price, expansion, acquisition and currency first.")
        L.append("")

    if r["history"]:
        L.append("HISTORY")
        for h in r["history"]:
            L.append(f"  {h['period']:<8} {h['growth']:+.2%}")
        L.append("")

    if r["warnings"]:
        L.append("WARNINGS")
        for w in r["warnings"]:
            L.append(f"  ! {w}")
        L.append("")

    L.append("CARRY FORWARD")
    L.append("  - only the durable share belongs in a terminal growth assumption")
    L.append("  - if earnings-quality's growth gates failed, do not stack any of this")
    L.append("    on a normalised base — that counts the recovery twice")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(description="Decompose revenue growth by source")
    p.add_argument("--revenue", required=True, help="Comma series, most recent first")
    p.add_argument("--years", default="", help="Comma labels, most recent first")
    p.add_argument("--volume-growth", type=float, default=None)
    p.add_argument("--price-growth", type=float, default=None)
    p.add_argument("--expansion-growth", type=float, default=None,
                   help="New stores / capacity contribution")
    p.add_argument("--acquisition-revenue", type=float, default=None,
                   help="Revenue added by acquisitions, in the same units as --revenue")
    p.add_argument("--fx-growth", type=float, default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--out", default=None)
    args = p.parse_args()

    rev = parse_list(args.revenue)
    if not rev:
        print("ERROR: could not parse --revenue", file=sys.stderr)
        return 2
    years = [y for y in args.years.split(",") if y] if args.years else []

    r = decompose(rev, years, args.volume_growth, args.price_growth,
                  args.expansion_growth, args.acquisition_revenue, args.fx_growth)
    if "error" in r:
        print(f"ERROR: {r['error']}", file=sys.stderr)
        return 1
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)
    print(json.dumps(r, indent=2, ensure_ascii=False) if args.json else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
