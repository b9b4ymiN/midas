#!/usr/bin/env python3
"""
normalize.py — turn a reported earnings series into a defensible base for
valuation, following Damodaran's normalisation method.

The method, in one line: **average the margin over a full cycle and apply it to
current revenue** — do not average the earnings themselves.

Why that ordering matters is easiest to see on a real company. Thai Union's
FY2023 operating margin was 5.02%, sitting mid-range against the other four
years (4.6–5.8%). Its net margin that year was **−10.45%**. All the damage sat
below the operating line. Average the net income and the base collapses to a
number the business has never earned in any year; average the operating margin
and the distortion never enters the calculation.

Revenue is also the line accountants can least easily bend, so starting from
revenue and applying a cycle-average margin removes one-off items structurally
rather than by hunting them down one at a time.

stdlib only.

Usage
-----
  normalize.py --snapshot .data/TU.BK/2026-08-13.json
  normalize.py --revenue 132718579000,138433059000,... \\
               --op-margin 0.04595,0.05177,... \\
               --current-revenue 135439918000
  normalize.py --snapshot ... --window 10 --json

Exit codes: 0 ok, 1 not enough data, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from typing import Any, Dict, List, Optional

# Damodaran: average "over a period long enough to cover an entire cycle",
# which he frames as 5-10 years while noting cycles vary by industry. We warn
# rather than silently accept a window that cannot contain a cycle.
MIN_CYCLE_YEARS = 5
MAX_USEFUL_YEARS = 10

# If revenue at the ends of the window differs by more than this, the company
# has changed scale and averaging absolute earnings is not defensible — the
# margin method is the only honest one.
SCALE_DRIFT_PCT = 20.0

# A year whose margin sits this far from the cycle median gets called out. Not
# excluded automatically: an outlier can be a genuine cycle peak or trough.
OUTLIER_SIGMA = 1.5


def _pct(x: Optional[float]) -> str:
    return "n/a" if x is None else f"{x*100:.2f}%"


# Scale is chosen once per run, from the SMALLEST headline figure (normalised
# operating income) rather than the largest, so the number that matters keeps
# its significant digits. Scaling off revenue instead would render Thai Union's
# 135,440m revenue as "135" and throw away three digits; hardcoding "millions"
# printed 0 for anyone reporting in thousands. Both are the same mistake —
# picking a unit without looking at what has to fit in it.
_SCALE = {"div": 1.0, "label": ""}


def _set_scale(smallest_headline: float) -> None:
    """Pick the largest unit that still leaves the smallest headline figure
    with at least three digits before the decimal point.

    Choosing purely by magnitude puts Thai Union's 6.97bn normalised operating
    income in billions, which then renders 135,440m of revenue as "135". Anchor
    on the smallest number that has to stay readable and both fit.
    """
    a = abs(smallest_headline)
    for div, label in ((1e12, "trillions"), (1e9, "billions"),
                       (1e6, "millions"), (1e3, "thousands")):
        if a / div >= 100:
            _SCALE.update(div=div, label=label)
            return
    _SCALE.update(div=1.0, label="units")


def _m(x: Optional[float]) -> str:
    if x is None:
        return "n/a"
    v = x / _SCALE["div"]
    # Keep two decimals once the scaled figure is small enough that rounding to
    # a whole number would hide the value.
    return f"{v:,.0f}" if abs(v) >= 100 else f"{v:,.2f}"


def load_series(args: argparse.Namespace) -> Dict[str, Any]:
    """Either from a fetch.py snapshot or from explicit --flags."""
    if args.snapshot:
        with open(args.snapshot, encoding="utf-8") as f:
            snap = json.load(f)
        facts = snap.get("facts", {})

        def fv(name: str) -> Any:
            rec = facts.get(name)
            return rec.get("value") if isinstance(rec, dict) else None

        series = {
            "revenue": fv("revenue_series") or fv("revenue_history"),
            "op_margin": fv("operating_margin_series"),
            "net_margin": fv("profit_margin_series"),
            "net_income": fv("net_income_series"),
            "op_income": fv("operating_income_series"),
            "years": fv("fiscal_years"),
            "current_revenue": fv("revenue_ttm"),
            "current_op_income": fv("operating_income_ttm"),
            "current_net_income": fv("net_income_ttm"),
            "currency": fv("currency"),
            "as_of": (facts.get("revenue_ttm") or {}).get("as_of"),
            "ticker": snap.get("ticker"),
            "fallback_count": snap.get("fallback_count", 0),
        }
        return series

    def parse(s: Optional[str]) -> Optional[List[float]]:
        if not s:
            return None
        return [float(x) for x in s.replace(" ", "").split(",") if x]

    return {
        "revenue": parse(args.revenue),
        "op_margin": parse(args.op_margin),
        "net_margin": parse(args.net_margin),
        "net_income": parse(args.net_income),
        "op_income": parse(args.op_income),
        "years": args.years.split(",") if args.years else None,
        "current_revenue": args.current_revenue,
        "current_op_income": args.current_op_income,
        "current_net_income": args.current_net_income,
        "currency": args.currency,
        "as_of": None,
        "ticker": args.ticker,
        "fallback_count": 0,
    }


def analyse(s: Dict[str, Any], window: int) -> Dict[str, Any]:
    rev: List[float] = (s.get("revenue") or [])[:window]
    opm: List[float] = (s.get("op_margin") or [])[:window]
    npm: List[float] = (s.get("net_margin") or [])[:window]
    ni: List[float] = (s.get("net_income") or [])[:window]
    oi: List[float] = (s.get("op_income") or [])[:window]
    years: List[str] = (s.get("years") or [])[:window]

    # Derive margins if only absolutes were supplied.
    if not opm and oi and rev:
        opm = [o / r for o, r in zip(oi, rev) if r]
    if not npm and ni and rev:
        npm = [n / r for n, r in zip(ni, rev) if r]
    if not oi and opm and rev:
        oi = [m * r for m, r in zip(opm, rev)]
    if not ni and npm and rev:
        ni = [m * r for m, r in zip(npm, rev)]

    out: Dict[str, Any] = {"warnings": [], "notes": []}
    if not rev or not opm:
        out["error"] = "need at least a revenue series and an operating-margin (or operating-income) series"
        return out

    n = min(len(rev), len(opm))
    rev, opm = rev[:n], opm[:n]
    if npm:
        npm = npm[:n]
    if ni:
        ni = ni[:n]
    if oi:
        oi = oi[:n]

    cur_rev = s.get("current_revenue") or rev[0]

    # --- cycle coverage ----------------------------------------------------
    if n < MIN_CYCLE_YEARS:
        out["warnings"].append(
            f"only {n} year(s) of history — Damodaran asks for a window long "
            f"enough to cover a full cycle ({MIN_CYCLE_YEARS}-{MAX_USEFUL_YEARS} "
            f"years). Treat the normalised base as provisional."
        )
    if n > MAX_USEFUL_YEARS:
        out["notes"].append(f"window trimmed to {MAX_USEFUL_YEARS} years")

    # --- scale drift: does the absolute-average method survive? -------------
    drift = abs(rev[0] - rev[-1]) / abs(rev[-1]) * 100.0 if rev[-1] else 0.0
    scale_changed = drift > SCALE_DRIFT_PCT

    # --- method 1: average absolute earnings -------------------------------
    m1_op = statistics.fmean(oi) if oi else None
    m1_net = statistics.fmean(ni) if ni else None

    # --- method 2: average margin x current revenue (Damodaran's preference)
    avg_opm = statistics.fmean(opm)
    med_opm = statistics.median(opm)
    m2_op = avg_opm * cur_rev
    avg_npm = statistics.fmean(npm) if npm else None
    m2_net = avg_npm * cur_rev if avg_npm is not None else None

    # --- the distortion test ------------------------------------------------
    # If the two margin series disagree about which years were bad, the damage
    # sat below the operating line and net-based normalisation is unreliable.
    distortion = None
    if npm:
        opm_sd = statistics.pstdev(opm) if len(opm) > 1 else 0.0
        npm_sd = statistics.pstdev(npm) if len(npm) > 1 else 0.0
        if opm_sd > 0:
            distortion = npm_sd / opm_sd
        worst_op = opm.index(min(opm))
        worst_np = npm.index(min(npm))
        if worst_op != worst_np and distortion and distortion > 2.0:
            y = years[worst_np] if worst_np < len(years) else f"index {worst_np}"
            out["warnings"].append(
                f"net margin is {distortion:.1f}x more volatile than operating "
                f"margin, and the worst net year ({y}) is not the worst "
                f"operating year — the damage sat BELOW the operating line. "
                f"Averaging net income here would embed a one-off into the base. "
                f"Use the operating-margin path."
            )

    # --- outlier years (flagged, never auto-dropped) ------------------------
    outliers = []
    if len(opm) > 2:
        sd = statistics.pstdev(opm)
        if sd > 0:
            for i, m in enumerate(opm):
                if abs(m - med_opm) > OUTLIER_SIGMA * sd:
                    outliers.append(
                        {"year": years[i] if i < len(years) else str(i),
                         "op_margin": m,
                         "vs_median_pp": (m - med_opm) * 100}
                    )

    # --- growth eligibility -------------------------------------------------
    # Damodaran's second trap: replacing depressed earnings with a normalised
    # figure AND then applying a consensus growth rate that already assumes the
    # recovery. Growth may only be stacked on top of a normalised base if the
    # recovery is not what the growth is made of.
    gates: List[Dict[str, Any]] = []
    latest_opm = opm[0]
    gates.append({
        "gate": "latest operating margin >= cycle average",
        "passed": latest_opm >= avg_opm,
        "detail": f"latest {_pct(latest_opm)} vs cycle avg {_pct(avg_opm)}",
    })
    if len(rev) >= 3:
        rising = rev[0] > rev[1] > rev[2]
        gates.append({
            "gate": "revenue rose in each of the last 2 years",
            "passed": rising,
            "detail": f"{_m(rev[2])} -> {_m(rev[1])} -> {_m(rev[0])}",
        })
    if oi and len(oi) >= 3:
        oi_rising = oi[0] > oi[1] > oi[2]
        gates.append({
            "gate": "operating income rose in each of the last 2 years",
            "passed": oi_rising,
            "detail": f"{_m(oi[2])} -> {_m(oi[1])} -> {_m(oi[0])}",
        })

    passed = sum(1 for g in gates if g["passed"])
    growth_ok = passed == len(gates)

    if not growth_ok:
        out["warnings"].append(
            f"growth gates {passed}/{len(gates)} — the normalised base already "
            f"assumes a recovery to mid-cycle. Stacking a consensus growth rate "
            f"on top would count that recovery twice. Use post-recovery growth "
            f"only, and say so in the model."
        )

    # --- trap 1 and 3 reminders --------------------------------------------
    out["notes"].append(
        "if you normalise earnings you must normalise capex, working capital "
        "and financing to the same footing — a mid-cycle profit paired with a "
        "trough-year capex is a year that never existed"
    )
    out["notes"].append(
        "the formula assumes normalisation happens today; if recovery takes N "
        "years, discount the value back N years or the result is too high"
    )

    return {
        "ticker": s.get("ticker"),
        "currency": s.get("currency"),
        "as_of": s.get("as_of"),
        "years_used": n,
        "years": years,
        "current_revenue": cur_rev,
        "scale_drift_pct": round(drift, 1),
        "scale_changed": scale_changed,
        "method_1_average_absolute": {
            "applicable": not scale_changed,
            "reason": (
                f"revenue moved {drift:.1f}% across the window (> {SCALE_DRIFT_PCT}%) "
                f"— the company changed scale, so averaging absolute earnings "
                f"understates or overstates the base"
                if scale_changed else
                f"revenue moved only {drift:.1f}% across the window — scale is stable"
            ),
            "normalised_operating_income": m1_op,
            "normalised_net_income": m1_net,
        },
        "method_2_average_margin": {
            "applicable": True,
            "reason": "reflects today's size; revenue is the line least exposed "
                      "to accounting discretion",
            "avg_operating_margin": avg_opm,
            "median_operating_margin": med_opm,
            "normalised_operating_income": m2_op,
            "avg_net_margin": avg_npm,
            "normalised_net_income": m2_net,
        },
        "recommended": "method_2_average_margin",
        "recommended_base_operating_income": m2_op,
        "reported_latest": {
            "operating_income_ttm": s.get("current_op_income"),
            "net_income_ttm": s.get("current_net_income"),
        },
        "net_vs_operating_volatility_ratio": distortion,
        "outlier_years": outliers,
        "growth_eligibility": {"gates": gates, "passed": passed,
                               "of": len(gates), "may_stack_growth": growth_ok},
        "warnings": out["warnings"],
        "notes": out["notes"],
        "data_fallback_facts": s.get("fallback_count", 0),
    }


def render(r: Dict[str, Any]) -> str:
    if "error" in r:
        return f"ERROR: {r['error']}"
    L: List[str] = []
    cur = r.get("currency") or ""
    _headline = min(
        (abs(v) for v in (r.get("recommended_base_operating_income"),
                          r.get("current_revenue")) if v),
        default=0,
    )
    _set_scale(_headline)
    unit = f"{cur} ({_SCALE['label']})".strip()
    L.append(f"# Normalised earnings — {r.get('ticker') or '(unnamed)'}")
    if r.get("as_of"):
        L.append(f"as of {r['as_of']} · {r['years_used']} year window · {unit}")
    else:
        L.append(f"{r['years_used']} year window · {unit}")
    L.append("")
    L.append(f"current revenue           {_m(r['current_revenue'])}")
    L.append(f"revenue drift over window {r['scale_drift_pct']}%"
             f"{'  -> SCALE CHANGED' if r['scale_changed'] else ''}")
    L.append("")

    m1, m2 = r["method_1_average_absolute"], r["method_2_average_margin"]
    L.append("METHOD 1 — average absolute earnings")
    L.append(f"  applicable: {'yes' if m1['applicable'] else 'NO'} — {m1['reason']}")
    L.append(f"  normalised operating income  {_m(m1['normalised_operating_income'])}")
    L.append(f"  normalised net income        {_m(m1['normalised_net_income'])}")
    L.append("")
    L.append("METHOD 2 — average margin x current revenue   <-- Damodaran's preference")
    L.append(f"  avg operating margin  {_pct(m2['avg_operating_margin'])}"
             f"   (median {_pct(m2['median_operating_margin'])})")
    L.append(f"  normalised operating income  {_m(m2['normalised_operating_income'])}")
    if m2.get("avg_net_margin") is not None:
        L.append(f"  avg net margin        {_pct(m2['avg_net_margin'])}")
        L.append(f"  normalised net income        {_m(m2['normalised_net_income'])}")
    L.append("")
    rep = r["reported_latest"]
    if rep.get("operating_income_ttm"):
        L.append(f"reported TTM operating income  {_m(rep['operating_income_ttm'])}"
                 f"   (base is {'above' if r['recommended_base_operating_income'] > rep['operating_income_ttm'] else 'below'} it)")
    if rep.get("net_income_ttm"):
        L.append(f"reported TTM net income        {_m(rep['net_income_ttm'])}")
    L.append("")

    if r.get("outlier_years"):
        L.append("OUTLIER YEARS (flagged, not dropped — a cycle peak or trough is real)")
        for o in r["outlier_years"]:
            L.append(f"  {o['year']}: operating margin {_pct(o['op_margin'])}"
                     f"  ({o['vs_median_pp']:+.2f} pp vs median)")
        L.append("")

    g = r["growth_eligibility"]
    L.append(f"GROWTH ELIGIBILITY — {g['passed']}/{g['of']} gates")
    for gate in g["gates"]:
        L.append(f"  [{'PASS' if gate['passed'] else 'FAIL'}] {gate['gate']}")
        L.append(f"         {gate['detail']}")
    L.append(f"  -> may stack a growth rate on this base: "
             f"{'YES' if g['may_stack_growth'] else 'NO — post-recovery growth only'}")
    L.append("")

    if r["warnings"]:
        L.append("WARNINGS")
        for w in r["warnings"]:
            L.append(f"  ! {w}")
        L.append("")
    L.append("REMINDERS")
    for nt in r["notes"]:
        L.append(f"  - {nt}")
    if r.get("data_fallback_facts"):
        L.append(f"  - {r['data_fallback_facts']} input fact(s) came from a FALLBACK "
                 f"source; carry that flag forward")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(description="Normalise earnings, Damodaran's way")
    p.add_argument("--snapshot", help="fetch.py snapshot JSON")
    p.add_argument("--revenue", help="Comma series, most recent first")
    p.add_argument("--op-margin", help="Comma series (0.05 = 5%%)")
    p.add_argument("--net-margin", help="Comma series")
    p.add_argument("--op-income", help="Comma series")
    p.add_argument("--net-income", help="Comma series")
    p.add_argument("--years", help="Comma labels, most recent first")
    p.add_argument("--current-revenue", type=float)
    p.add_argument("--current-op-income", type=float)
    p.add_argument("--current-net-income", type=float)
    p.add_argument("--currency", default=None)
    p.add_argument("--ticker", default=None)
    p.add_argument("--window", type=int, default=MAX_USEFUL_YEARS)
    p.add_argument("--json", action="store_true", help="Emit JSON instead of a table")
    p.add_argument("--out", default=None, help="Write JSON here as well")
    args = p.parse_args()

    if not args.snapshot and not args.revenue:
        p.error("give --snapshot or --revenue")

    try:
        series = load_series(args)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    result = analyse(series, args.window)
    if "error" in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        return 1

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
