#!/usr/bin/env python3
"""
sensitivity.py — how far does operating margin move when an input price moves?

The number this produces is the one a driver analysis exists to deliver. "Tuna
prices are rising" is an observation; "a 10% move in tuna costs 1.4 points of
operating margin, landing two quarters out because the company holds a buffer"
is something a valuation can use and a thesis can be broken on.

The arithmetic is exact, not a heuristic. What it needs from you is the input's
share of revenue and how much of a cost increase the company can pass on — both
of which come from reading the filing, which is the point: the script cannot be
run without having done the work.

Model
-----
With revenue normalised to 1:

    input cost share      c    (input spend / revenue)
    operating margin      m
    input price move      x    (+0.10 = a 10% rise)
    pass-through          p    (0 = absorbs it all, 1 = passes it all on)

    revenue      -> 1 + c*x*p
    total cost   -> (1 - m) + c*x
    op income    -> m - c*x*(1 - p)
    new margin    = (m - c*x*(1-p)) / (1 + c*x*p)

Pass-through is the assumption that carries the answer, so the script sweeps it
rather than letting one guess hide inside a single number.

stdlib only.

Usage
-----
  sensitivity.py --driver "tuna" --cost-share 0.55 --margin 0.0487 --move 0.10
  sensitivity.py --driver "tuna" --cost-share 0.55 --margin 0.0487 \
                 --move 0.10 --pass-through 0.6 --revenue 135439918000 \
                 --lag-months 3 --currency THB
  sensitivity.py --driver fx --cost-share 0.30 --margin 0.05 --sweep

Exit codes: 0 ok, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

PASS_THROUGH_SWEEP = [0.0, 0.25, 0.5, 0.75, 1.0]
MOVE_SWEEP = [-0.20, -0.10, -0.05, 0.05, 0.10, 0.20]


def new_margin(m: float, c: float, x: float, p: float) -> float:
    denom = 1.0 + c * x * p
    if denom <= 0:
        return float("nan")
    return (m - c * x * (1.0 - p)) / denom


def analyse(
    driver: str,
    cost_share: float,
    margin: float,
    move: float,
    pass_through: Optional[float],
    revenue: Optional[float],
    lag_months: Optional[int],
    currency: str,
) -> Dict[str, Any]:
    warnings: List[str] = []
    if not 0 < cost_share <= 1:
        warnings.append(
            f"cost share of {cost_share:.0%} is outside (0, 1] — check it is the "
            f"input's share of REVENUE, not of total cost"
        )
    if cost_share > 0.9:
        warnings.append(
            "cost share above 90% of revenue leaves almost no room for anything "
            "else — verify against the filing before using this"
        )
    if abs(margin) > 0.6:
        warnings.append(f"operating margin of {margin:.0%} is unusual — confirm the input")

    grid = []
    for p in PASS_THROUGH_SWEEP:
        nm = new_margin(margin, cost_share, move, p)
        grid.append({
            "pass_through": p,
            "new_margin": nm,
            "delta_pp": (nm - margin) * 100.0,
            "op_income_delta": (nm - margin) * revenue if revenue else None,
        })

    chosen = None
    if pass_through is not None:
        nm = new_margin(margin, cost_share, move, pass_through)
        chosen = {
            "pass_through": pass_through,
            "new_margin": nm,
            "delta_pp": (nm - margin) * 100.0,
            "op_income_delta": (nm - margin) * revenue if revenue else None,
        }

    # The move that wipes out the margin entirely. Reported at BOTH the
    # no-pass-through worst case and the stated assumption, because the two
    # differ by a lot and a single number labelled loosely is worse than none:
    # at 55% cost share and a 4.87% margin, "breakeven" is +9% if the company
    # can pass on nothing and +22% if it can pass on 60%. Same formula, same
    # inputs, and the wrong caption turns a warning into a reassurance.
    breakeven_zero = margin / cost_share if cost_share > 0 else None
    breakeven_at_p = None
    if cost_share > 0 and pass_through is not None and pass_through < 1.0:
        breakeven_at_p = margin / (cost_share * (1.0 - pass_through))

    move_grid = []
    for x in MOVE_SWEEP:
        p = pass_through if pass_through is not None else 0.0
        nm = new_margin(margin, cost_share, x, p)
        move_grid.append({"move": x, "new_margin": nm, "delta_pp": (nm - margin) * 100.0})

    return {
        "driver": driver,
        "inputs": {
            "cost_share_of_revenue": cost_share,
            "operating_margin": margin,
            "price_move": move,
            "pass_through": pass_through,
            "revenue": revenue,
            "currency": currency,
            "lag_months": lag_months,
        },
        "chosen": chosen,
        "pass_through_grid": grid,
        "move_grid": move_grid,
        "breakeven_move_no_passthrough": breakeven_zero,
        "breakeven_move_at_stated_passthrough": breakeven_at_p,
        "lag_note": (
            f"the company holds roughly {lag_months} month(s) of buffer, so a move "
            f"today lands in reported margin about {lag_months} month(s) out — do "
            f"not expect it in the current quarter"
            if lag_months else None
        ),
        "warnings": warnings,
    }


def render(r: Dict[str, Any]) -> str:
    i = r["inputs"]
    cur = i["currency"] or ""
    L = [f"# Driver sensitivity — {r['driver']}", ""]
    L.append(f"input is {i['cost_share_of_revenue']:.1%} of revenue · "
             f"operating margin {i['operating_margin']:.2%}")
    if i["revenue"]:
        L.append(f"revenue base {i['revenue']/1e6:,.0f} {cur} (millions)")
    L.append("")

    L.append(f"A {i['price_move']:+.0%} move in {r['driver']}, by how much the company "
             f"can pass on:")
    L.append("")
    L.append(f"  {'pass-through':>14}  {'new margin':>11}  {'change':>9}"
             + (f"  {'op income':>16}" if i["revenue"] else ""))
    for g in r["pass_through_grid"]:
        line = f"  {g['pass_through']:>13.0%}  {g['new_margin']:>10.2%}  {g['delta_pp']:>+8.2f}pp"
        if g["op_income_delta"] is not None:
            line += f"  {g['op_income_delta']/1e6:>+15,.0f}"
        L.append(line)
    L.append("")

    if r["chosen"]:
        c = r["chosen"]
        L.append(f"At the stated pass-through of {c['pass_through']:.0%}: "
                 f"margin {i['operating_margin']:.2%} -> {c['new_margin']:.2%} "
                 f"({c['delta_pp']:+.2f}pp)")
        if c["op_income_delta"] is not None:
            L.append(f"  operating income {c['op_income_delta']/1e6:+,.0f} {cur} (millions)")
        L.append("")

    L.append(f"Across move sizes (at pass-through "
             f"{(i['pass_through'] if i['pass_through'] is not None else 0):.0%}):")
    for g in r["move_grid"]:
        L.append(f"  {g['move']:>+6.0%} -> margin {g['new_margin']:>7.2%}  ({g['delta_pp']:+.2f}pp)")
    L.append("")

    bz = r["breakeven_move_no_passthrough"]
    bp = r["breakeven_move_at_stated_passthrough"]
    if bz is not None:
        L.append("BREAKEVEN — the move that erases the operating margin entirely")
        L.append(f"  passing on nothing:      {bz:+.0%}")
        if bp is not None:
            L.append(f"  at the stated {i['pass_through']:.0%} pass-through: {bp:+.0%}")
            L.append(f"  The gap between those two is the whole question. Pricing power is")
            L.append(f"  not an assumption to set once — it is what decides whether a "
                     f"{bz:+.0%} move is survivable.")
        else:
            L.append("  (state a --pass-through to see how much room pricing power buys)")
        L.append("")

    if r["lag_note"]:
        L.append(f"TIMING: {r['lag_note']}")
        L.append("")

    L.append("CARRY FORWARD")
    L.append("  - into the valuation's scenario range, as a third axis beyond WACC x g")
    L.append("  - into the thesis-breakers, if this is the input that moves value most")
    L.append("  - into the catalyst table, with the date the move actually lands")
    if r["warnings"]:
        L.append("")
        L.append("WARNINGS")
        for w in r["warnings"]:
            L.append(f"  ! {w}")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(description="Input-price sensitivity of operating margin")
    p.add_argument("--driver", required=True, help="What is moving, e.g. tuna, FX, freight")
    p.add_argument("--cost-share", type=float, required=True,
                   help="The input's spend as a fraction of REVENUE (0.55 = 55%%)")
    p.add_argument("--margin", type=float, required=True, help="Operating margin (0.05 = 5%%)")
    p.add_argument("--move", type=float, default=0.10, help="Price move (0.10 = +10%%)")
    p.add_argument("--pass-through", type=float, default=None,
                   help="Share passed to customers (0-1). Omitted = sweep only")
    p.add_argument("--revenue", type=float, default=None, help="Revenue base, for currency impact")
    p.add_argument("--lag-months", type=int, default=None, help="Inventory/hedge buffer in months")
    p.add_argument("--currency", default="", help="Label only")
    p.add_argument("--sweep", action="store_true", help="(default behaviour; kept for clarity)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--out", default=None)
    args = p.parse_args()

    if args.pass_through is not None and not 0 <= args.pass_through <= 1:
        print("ERROR: --pass-through must be between 0 and 1", file=sys.stderr)
        return 2

    r = analyse(args.driver, args.cost_share, args.margin, args.move,
                args.pass_through, args.revenue, args.lag_months, args.currency)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)
    print(json.dumps(r, indent=2, ensure_ascii=False) if args.json else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
