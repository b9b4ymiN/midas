#!/usr/bin/env python3
"""
verify_sign.py -- the masking test.

A sign inversion is the one bug in this class of computation that SURVIVES
INSPECTION: every magnitude stays correct while the regime read flips. Reading
the output cannot catch it. Only this test can.

Asserts, on a real or fixture chain, that flipping the sign contract:
  1. negates net GEX EXACTLY          (|net_A + net_B| < 1e-6 * |net_A|)
  2. leaves per-strike |GEX| unchanged (gamma magnitudes are sign-independent)
  3. leaves the gamma-flip level unchanged

If any assertion fails, the implementation is wrong -- stop and fix it before
reading any output from gex_scan.py.

Usage
-----
  verify_sign.py --fixture tests/fixture_vlo_20260818.json
  verify_sign.py VLO

Exit codes: 0 pass, 1 FAIL (implementation bug), 2 chain unusable.
"""
from __future__ import annotations

import argparse
import sys

import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gex_scan import analyse, load_snapshot, load_yfinance  # noqa: E402

MODEL_A = {"call": 1.0, "put": -1.0}
MODEL_B = {"call": -1.0, "put": 1.0}
TOL_REL = 1e-6


def check(spot, rows):
    a = analyse(spot, rows, sign=MODEL_A)
    b = analyse(spot, rows, sign=MODEL_B)
    if a["gate"] == "FAIL":
        print("chain failed the liquidity gate - cannot run masking test")
        return 2

    fails = []

    # 1 -- exact negation
    na, nb = a["net_gex"], b["net_gex"]
    if abs(na + nb) > TOL_REL * max(abs(na), 1.0):
        fails.append(f"net GEX does not negate exactly: A={na:,.2f} B={nb:,.2f} "
                     f"sum={na+nb:,.6f}")

    # 2 -- per-strike magnitudes invariant
    pa, pb = a["per_strike"], b["per_strike"]
    if set(pa) != set(pb):
        fails.append("strike sets differ between contracts")
    else:
        worst = max((abs(abs(pa[k]) - abs(pb[k])), k) for k in pa)
        if worst[0] > TOL_REL * max(abs(pa[worst[1]]), 1.0):
            fails.append(f"per-strike magnitude changed at {worst[1]}: "
                         f"delta={worst[0]:,.6f}")

    # 3 -- flip level invariant
    fa, fb = a["gamma_flip"], b["gamma_flip"]
    if (fa is None) != (fb is None):
        fails.append(f"flip presence differs: A={fa} B={fb}")
    elif fa is not None and abs(fa - fb) > 1e-6 * max(abs(fa), 1.0):
        fails.append(f"flip level moved: A={fa:,.4f} B={fb:,.4f}")

    print(f"spot ${spot:,.2f} | {a['tier']} | {a['n_strikes']} strikes priced")
    print(f"  Model A net GEX  {na:>18,.2f}   regime {a['regime']}")
    print(f"  Model B net GEX  {nb:>18,.2f}   regime {b['regime']}")
    print(f"  sum              {na+nb:>18,.6f}   (must be 0)")
    print(f"  flip level       A={fa} B={fb}")
    if fails:
        print("\nMASKING TEST FAILED - the sign is not isolated:")
        for f in fails:
            print(f"  - {f}")
        print("\nDo not use gex_scan output until this passes.")
        return 1
    print("\nMASKING TEST PASSED - sign is an isolated, auditable design choice.")
    print("Regime read is therefore only as good as the contract you declared.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Masking test for the GEX sign contract.")
    ap.add_argument("ticker", nargs="?")
    ap.add_argument("--fixture", help="known-answer chain, no network")
    a = ap.parse_args()
    if a.fixture:
        spot, rows = load_snapshot(a.fixture)
    elif a.ticker:
        spot, rows = load_yfinance(a.ticker.upper())
    else:
        ap.error("give a ticker or --fixture")
    return check(spot, rows)


if __name__ == "__main__":
    sys.exit(main())
