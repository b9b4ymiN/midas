#!/usr/bin/env python3
"""The arithmetic behind an accumulation plan: what the price asks, what it would earn.

Two calculations, both deliberately small:

1. **Price-implied expectations** — run the cash-flow arithmetic backwards from
   today's price at a stated required return, and read out the growth rate the price
   already assumes. The price is the input; the expectation is the output. No fair
   value is produced and none is implied.
2. **Expected return paths** — decompose a holding-period return into business
   growth, shareholder yield, and the change in the multiple, under three stated
   assumption sets.

The bands come from inverting (1): the range of prices over which what the market
asks stays at or below what the business has shown it can deliver, less the cushion
the plan archetype requires. That boundary is a break-even for a stated set of
assumptions, not a valuation, and it is never reported without its sensitivity.

    python plan_math.py --price 33.80 --fcf-per-share 1.42 --required-return 0.09 \\
        --durable-growth 0.099 --archetype narrow-runway

Method and provenance: ../references/price-implied-expectations.md and
../references/expected-return-math.md

Research and educational output only. Not financial advice.
"""
from __future__ import annotations

import argparse
import json
import sys

HORIZON = 10
TERMINAL_GROWTH = 0.025
REQUIRED_RETURN_SENSITIVITY = (-0.02, 0.0, 0.02)
TERMINAL_SENSITIVITY = (-0.01, 0.0, 0.01)
GAP_TOLERANCE = 0.015  # within 1.5 points, the price and the engine agree

# How far below the engine's demonstrated growth the market's demand has to sit
# before the plan will accumulate. A business that cannot reinvest has no runway to
# grow into a mistake, so it needs the widest cushion; a proven compounder earns its
# return from duration, so it needs none.
ARCHETYPE_CUSHION = {
    "proven-compounder": 0.00,
    "emerging-starter": 0.02,
    "narrow-runway": 0.03,
}
# Above the engine's growth by this much, the price is asking for something the work
# did not find. Tighter where there is no runway.
ARCHETYPE_STRETCH = {
    "proven-compounder": 0.015,
    "emerging-starter": 0.010,
    "narrow-runway": 0.000,
}


def value_per_share(cash_flow, growth, required_return, horizon=HORIZON,
                    terminal_growth=TERMINAL_GROWTH):
    """Present value of a cash flow growing at `growth`, then at `terminal_growth`."""
    if required_return <= terminal_growth:
        return None
    total = 0.0
    flow = cash_flow
    for t in range(1, horizon + 1):
        flow = flow * (1 + growth)
        total += flow / (1 + required_return) ** t
    terminal = flow * (1 + terminal_growth) / (required_return - terminal_growth)
    return total + terminal / (1 + required_return) ** horizon


def implied_growth(price, cash_flow, required_return, horizon=HORIZON,
                   terminal_growth=TERMINAL_GROWTH):
    """Solve for the growth rate that makes the arithmetic equal today's price."""
    if cash_flow is None or cash_flow <= 0 or price is None or price <= 0:
        return None
    lo, hi = -0.50, 0.60
    v_lo = value_per_share(cash_flow, lo, required_return, horizon, terminal_growth)
    v_hi = value_per_share(cash_flow, hi, required_return, horizon, terminal_growth)
    if v_lo is None or v_hi is None:
        return None
    if not (v_lo <= price <= v_hi):
        return None  # the price sits outside what this model can express
    for _ in range(200):
        mid = (lo + hi) / 2
        v = value_per_share(cash_flow, mid, required_return, horizon, terminal_growth)
        if v is None:
            return None
        if v < price:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 5)


def sensitivity_table(price, cash_flow, required_return, horizon=HORIZON,
                      terminal_growth=TERMINAL_GROWTH):
    """Implied growth across required return and terminal growth, both moved."""
    rows = []
    for dr in REQUIRED_RETURN_SENSITIVITY:
        row = {"required_return": round(required_return + dr, 4), "implied_growth": {}}
        for dg in TERMINAL_SENSITIVITY:
            g = implied_growth(price, cash_flow, required_return + dr, horizon,
                               terminal_growth + dg)
            row["implied_growth"][f"terminal_{round(terminal_growth + dg, 4)}"] = g
        rows.append(row)
    return rows


def gap(implied, durable):
    if implied is None or durable is None:
        return {"direction": "UNRESOLVED", "size": None,
                "note": "the implied growth could not be solved from the inputs given"}
    difference = implied - durable
    if abs(difference) <= GAP_TOLERANCE:
        direction = "PRICE_ASKS_ABOUT_THE_SAME"
    elif difference < 0:
        direction = "PRICE_ASKS_LESS"
    else:
        direction = "PRICE_ASKS_MORE"
    return {
        "direction": direction,
        "size": round(difference, 5),
        "implied_growth": implied,
        "durable_growth": durable,
        "basis": "nominal, both sides",
        "tolerance": GAP_TOLERANCE,
    }


def price_for_growth(cash_flow, growth, required_return, horizon=HORIZON,
                     terminal_growth=TERMINAL_GROWTH):
    return value_per_share(cash_flow, growth, required_return, horizon, terminal_growth)


def bands(cash_flow, durable, required_return, archetype, horizon=HORIZON,
          terminal_growth=TERMINAL_GROWTH):
    """Invert the expectations arithmetic into three price ranges."""
    cushion = ARCHETYPE_CUSHION.get(archetype)
    stretch = ARCHETYPE_STRETCH.get(archetype)
    if cash_flow is None or durable is None or cushion is None:
        return None
    accumulate_to = price_for_growth(cash_flow, durable - cushion, required_return,
                                     horizon, terminal_growth)
    stretch_from = price_for_growth(cash_flow, durable + stretch, required_return,
                                    horizon, terminal_growth)
    if accumulate_to is None or stretch_from is None:
        return None
    return [
        {
            "band": "accumulate",
            "upper": round(accumulate_to, 4),
            "lower": None,
            "condition": (f"at or below this price the market is asking for no more "
                          f"than {round((durable - cushion) * 100, 1)}% growth a year, "
                          f"against the {round(durable * 100, 1)}% the engine has "
                          f"shown — a cushion of {round(cushion * 100, 1)} points for "
                          f"a {archetype} plan"),
        },
        {
            "band": "hold, do not chase",
            "lower": round(accumulate_to, 4),
            "upper": round(stretch_from, 4),
            "condition": ("in this range the price asks for roughly what the business "
                          "has shown it can do; there is no cushion left, so an "
                          "existing position is held and a new one is not built"),
        },
        {
            "band": "too demanding",
            "lower": round(stretch_from, 4),
            "upper": None,
            "condition": (f"above this price the market is asking for more than "
                          f"{round((durable + stretch) * 100, 1)}% a year, which the "
                          f"compounding work did not find evidence for"),
        },
    ]


def multiple_context(current_multiple, median_multiple):
    """Which way a return to the median would push the return."""
    if not current_multiple or not median_multiple:
        return {"direction": "UNRESOLVED",
                "note": "one of the two multiples could not be sourced"}
    if median_multiple > current_multiple:
        return {
            "direction": "REVERSION_IS_A_TAILWIND",
            "current": current_multiple, "median": median_multiple,
            "note": ("the stock trades below its own median, so a return to that "
                     "median adds to the return — say so plainly rather than letting "
                     "a scenario name imply otherwise"),
        }
    if median_multiple < current_multiple:
        return {
            "direction": "REVERSION_IS_A_HEADWIND",
            "current": current_multiple, "median": median_multiple,
            "note": ("the stock trades above its own median, so a return to that "
                     "median subtracts from the return"),
        }
    return {"direction": "NO_CHANGE", "current": current_multiple,
            "median": median_multiple, "note": "the stock trades at its own median"}


def return_paths(durable, shareholder_yield, current_multiple, median_multiple,
                 horizon=HORIZON):
    """Business growth + shareholder yield ± the change in the multiple."""
    if durable is None:
        return [{"scenario": "UNRESOLVED",
                 "note": "no durable growth figure was supplied"}]
    y = shareholder_yield or 0.0
    paths = []
    # Named after the assumption, never after a judgement of the outcome. Where the
    # stock trades below its own median, a reversion is a tailwind and "strong" would
    # have labelled the worst path as the best one.
    scenarios = [
        ("growth-slows", durable * 0.6, median_multiple,
         "growth at 60% of what the engine has shown, and the multiple moving back "
         "to this stock's own median"),
        ("as-shown", durable, median_multiple,
         "growth at what the engine has shown, and the multiple moving back to this "
         "stock's own median"),
        ("no-rerating", durable, current_multiple,
         "growth at what the engine has shown, and the multiple staying where it is "
         "today"),
    ]
    for name, growth, target_multiple, note in scenarios:
        if target_multiple and current_multiple:
            multiple_change = (target_multiple / current_multiple) ** (1 / horizon) - 1
        else:
            multiple_change = None
        total = None if multiple_change is None else growth + y + multiple_change
        paths.append({
            "scenario": name,
            "note": ("these are three assumption sets, not a ranking: where the "
                     "multiple sits below its own median, a reversion adds to the "
                     "return rather than subtracting from it"),
            "business_growth": round(growth, 5),
            "shareholder_yield": round(y, 5),
            "multiple_change_annual": (None if multiple_change is None
                                       else round(multiple_change, 5)),
            "annual_return": None if total is None else round(total, 5),
            "horizon_years": horizon,
            "assumption": note,
            "status": "UNRESOLVED" if total is None else "COMPUTED",
        })
    return paths


def build(args):
    cash_flow = args.fcf_per_share
    implied = implied_growth(args.price, cash_flow, args.required_return,
                             args.horizon, args.terminal_growth)
    unresolved_reason = None
    if implied is None:
        if cash_flow is None or cash_flow <= 0:
            unresolved_reason = ("free cash flow per share is zero or negative, so "
                                 "there is no cash-flow stream to run backwards")
        else:
            unresolved_reason = ("the price sits outside the growth range this "
                                 "arithmetic can express at the stated required return")

    return {
        "required_return_assumption": {
            "value": args.required_return,
            "basis": args.required_return_basis,
            "sensitivity_tested": [round(args.required_return + d, 4)
                                   for d in REQUIRED_RETURN_SENSITIVITY],
            "note": ("stated as an assumption and moved, never derived into a single "
                     "cost of capital"),
        },
        "price_implied_expectations": {
            "implied_growth": implied,
            "status": "COMPUTED" if implied is not None else "UNRESOLVED",
            "unresolved_reason": unresolved_reason,
            "window": f"{args.horizon} years, then {args.terminal_growth:.1%} in perpetuity",
            "inputs": {
                "price": args.price,
                "fcf_per_share": cash_flow,
                "required_return": args.required_return,
                "terminal_growth": args.terminal_growth,
            },
            "sensitivity": sensitivity_table(args.price, cash_flow,
                                             args.required_return, args.horizon,
                                             args.terminal_growth),
        },
        "expectation_gap": gap(implied, args.durable_growth),
        "multiple_context": multiple_context(args.current_multiple,
                                            args.median_multiple),
        "expected_return_paths": return_paths(args.durable_growth,
                                              args.shareholder_yield,
                                              args.current_multiple,
                                              args.median_multiple,
                                              args.horizon),
        "accumulation_bands": bands(cash_flow, args.durable_growth,
                                    args.required_return, args.archetype,
                                    args.horizon, args.terminal_growth)
        or "UNRESOLVED — the bands need a positive cash flow and a durable growth figure",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--price", type=float, required=True)
    ap.add_argument("--fcf-per-share", type=float, default=None,
                    help="owner cash flow per share the expectations are solved from")
    ap.add_argument("--required-return", type=float, default=0.09,
                    help="stated as an assumption, not derived")
    ap.add_argument("--required-return-basis", default=(
        "a stated long-run equity return assumption; moved plus and minus 2 points "
        "in the sensitivity rather than derived into one cost of capital"))
    ap.add_argument("--durable-growth", type=float, default=None,
                    help="durable_growth.nominal from the thesis pack")
    ap.add_argument("--terminal-growth", type=float, default=TERMINAL_GROWTH)
    ap.add_argument("--horizon", type=int, default=HORIZON)
    ap.add_argument("--shareholder-yield", type=float, default=None)
    ap.add_argument("--current-multiple", type=float, default=None)
    ap.add_argument("--median-multiple", type=float, default=None)
    ap.add_argument("--archetype", choices=sorted(ARCHETYPE_CUSHION),
                    default="proven-compounder")
    ap.add_argument("--out", default=None, help="write the fragment to this JSON file")
    args = ap.parse_args(argv)

    fragment = build(args)
    text = json.dumps(fragment, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
