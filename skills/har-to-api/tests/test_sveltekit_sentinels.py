#!/usr/bin/env python3
"""Devalue sentinel handling in resolve_sveltekit().

Regression guard for the bug found on the GULF.BK run (2026-08): an undefined
field (`sections` on the balance-sheet route) hydrated to the raw integer -1
and would have been recorded as the *value* -1 in a fact record. That breaks
rule 1 of the skill — missing must stay missing.

The counterpart risk is over-correcting: a genuinely negative datum must still
survive. Devalue only uses negative integers in *reference* position; real
values live in the flat array behind a positive index, so both properties can
hold at once. Both directions are tested here.

Run: python tests/test_sveltekit_sentinels.py
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

from discover import resolve_sveltekit  # noqa: E402
from fetch import json_path  # noqa: E402

FAILURES: list[str] = []


def check(name: str, got: object, want: object) -> None:
    ok = (got is None) if want is None else (got == want and type(got) is type(want))
    print(f"{'PASS' if ok else 'FAIL'}  {name}  -> {got!r}")
    if not ok:
        FAILURES.append(name)


def node0(flat: list) -> dict:
    doc = {"type": "data", "nodes": [{"type": "data", "data": flat}]}
    return resolve_sveltekit(doc)["nodes"][0]["data"]


def test_undefined_becomes_none() -> None:
    """The exact shape stockanalysis serves on /financials/balance-sheet/."""
    doc = {"type": "data", "nodes": [None, None, {"type": "data", "data": [
        {"sections": -1, "financialData": 1},   # 0: root — sections is undefined
        {"equity": 2},                          # 1
        347604239000,                           # 2: GULF equity, TTM Jun-2026
    ]}]}
    resolved = resolve_sveltekit(doc)
    data = resolved["nodes"][2]["data"]
    check("undefined `sections` -> None", data["sections"], None)
    check("sibling value still resolves", data["financialData"]["equity"], 347604239000)
    check(
        "json_path through an undefined hop -> None",
        json_path(resolved, "nodes[2].data.sections[id=revenue-income].ttm.revenue"),
        None,
    )


def test_real_negative_values_survive() -> None:
    """Over-correction guard: negative *data* must not be swallowed."""
    data = node0([
        {"fcf": 1, "ncfo": 2, "capex": 3},
        -3839181000,    # GULF free cash flow, TTM — genuinely negative
        21632903000,
        -25472084000,   # capex — genuinely negative
    ])
    check("negative free cash flow preserved", data["fcf"], -3839181000)
    check("positive operating cash flow preserved", data["ncfo"], 21632903000)
    check("negative capex preserved", data["capex"], -25472084000)


def test_remaining_sentinels() -> None:
    data = node0([{"hole": -2, "nan": -3, "inf": -4, "ninf": -5, "negzero": -6}])
    check("-2 (sparse hole) -> None", data["hole"], None)
    is_nan = isinstance(data["nan"], float) and math.isnan(data["nan"])
    print(f"{'PASS' if is_nan else 'FAIL'}  -3 -> NaN  -> {data['nan']!r}")
    if not is_nan:
        FAILURES.append("-3 -> NaN")
    check("-4 -> +inf", data["inf"], float("inf"))
    check("-5 -> -inf", data["ninf"], float("-inf"))
    check("-6 -> -0.0", data["negzero"], -0.0)


def test_booleans_are_not_indices() -> None:
    """bool is a subclass of int in Python — it must not be index-resolved."""
    data = node0([{"flag": True, "off": False}, "unreachable"])
    check("True untouched", data["flag"], True)
    check("False untouched", data["off"], False)


def test_out_of_range_index_unchanged() -> None:
    """A positive index past the end is a malformed doc, not a sentinel."""
    data = node0([{"weird": 99}])
    check("out-of-range index returned as-is", data["weird"], 99)


def main() -> int:
    for fn in (
        test_undefined_becomes_none,
        test_real_negative_values_survive,
        test_remaining_sentinels,
        test_booleans_are_not_indices,
        test_out_of_range_index_unchanged,
    ):
        print(f"\n--- {fn.__name__} ---")
        fn()
    print()
    if FAILURES:
        print(f"RESULT: {len(FAILURES)} FAILED -> {FAILURES}")
        return 1
    print("RESULT: all pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
