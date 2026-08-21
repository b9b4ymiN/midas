#!/usr/bin/env python3
"""Segment reconciliation: which rows are parts, and which is the total.

Two regressions guarded here, both found live:

1. Summing the provider's own total row in with the parts doubles the figure.
   TU.BK and AAPL both read as exactly +100% off — two unrelated issuers
   landing on the same round number, which is the shape of a bug in the
   checker rather than a finding about the data.

2. Matching the total row too loosely eats a real segment. Ping An
   (SHA:601318) has a segment literally named "Total Asset Management"; a
   pattern of `(^|_)total(_|$)` treated `total_asset_management_revenue` as
   the summary row, dropped CNY 71.9bn of real revenue from the sum, then
   divided by it — reporting a +1481% gap where the true gap is +22.6%.

Run: python tests/test_segment_reconciliation.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

from fetch import _is_segment_total, reconcile_segments  # noqa: E402

FAILURES: list[str] = []


def check(name: str, got: object, want: object) -> None:
    ok = got == want
    print(f"{'PASS' if ok else 'FAIL'}  {name}  -> {got!r}")
    if not ok:
        FAILURES.append(f"{name}: got {got!r}, want {want!r}")


def test_total_row_naming() -> None:
    for key in ("total", "revenue_total", "total_revenue", "segment_total"):
        check(f"'{key}' is a total row", _is_segment_total(key), True)
    for key in ("total_asset_management_revenue", "banking_revenue",
                "life_and_health_insurance_revenue", "total_return_segment"):
        check(f"'{key}' is NOT a total row", _is_segment_total(key), False)


def test_pingan_segment_named_total() -> None:
    """SHA:601318, TTM to 2026-06-30. Six parts, no declared total."""
    rec = {"value": {
        "datekey": "2026-06-30",
        "life_and_health_insurance_revenue": 546_643_000_000,
        "property_and_casualty_insurance_revenue": 360_401_000_000,
        "banking_revenue": 209_288_000_000,
        "total_asset_management_revenue": 71_928_000_000,
        "finance_enablement_revenue": 52_916_000_000,
        "other_business_revenue_and_eliminations": -31_970_000_000,
    }}
    out = reconcile_segments(rec, 985_974_000_000)
    check("all six parts summed", out["segment_sum"], 1_209_206_000_000.0)
    check("no total row claimed", out["segment_declared_total"], None)
    check("gap vs revenue", out["segment_vs_revenue_delta_pct"], 22.64)


def test_declared_total_is_excluded_from_parts() -> None:
    """TU.BK shape: four segments, eliminations, and a real total row."""
    rec = {"value": {
        "datekey": "2026-06-30",
        "ambient_seafood": 80_171_273_000,
        "frozen_and_chilled_seafood_and_related_business": 47_272_830_000,
        "pet_food": 24_982_371_000,
        "value_added_others": 17_476_890_000,
        "eliminations": -34_463_446_000,
        "total": 135_439_918_000,
    }}
    out = reconcile_segments(rec, 135_439_918_000)
    check("total excluded from parts", out["segment_sum"], 135_439_918_000.0)
    check("total recognised", out["segment_declared_total"], 135_439_918_000.0)
    check("reconciles exactly", out["segment_vs_revenue_delta_pct"], 0.0)


def test_implausible_total_is_demoted() -> None:
    """Belt and braces: a 'total' smaller than the largest part is not one."""
    rec = {"value": {"big_segment": 900, "small_segment": 100, "odd_total": 50}}
    out = reconcile_segments(rec, 1050)
    check("implausible total folded back into parts", out["segment_sum"], 1050.0)
    check("no total claimed", out["segment_declared_total"], None)


def test_no_numeric_parts_returns_empty() -> None:
    check("empty record", reconcile_segments({"value": {"datekey": "2026-06-30"}}, 100), {})
    check("non-dict value", reconcile_segments({"value": 42}, 100), {})


def main() -> int:
    for fn in (
        test_total_row_naming,
        test_pingan_segment_named_total,
        test_declared_total_is_excluded_from_parts,
        test_implausible_total_is_demoted,
        test_no_numeric_parts_returns_empty,
    ):
        print(f"\n--- {fn.__name__} ---")
        fn()
    print()
    if FAILURES:
        print(f"RESULT: {len(FAILURES)} FAILED")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("RESULT: all pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
