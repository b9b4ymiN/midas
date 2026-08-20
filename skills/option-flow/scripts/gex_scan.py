#!/usr/bin/env python3
"""
gex_scan.py -- dealer gamma exposure per strike, from a free option chain.

Sign contract: Model A (SqueezeMetrics open-interest proxy) --
dealers assumed LONG calls / SHORT puts. The sign is an INVENTORY ASSUMPTION,
not a property of the Greek: BS gamma is identical and positive for a call and
a put at the same strike. Flipping the contract negates net GEX exactly while
leaving the flip level and gamma magnitudes unchanged, so a mislabelled sign
inverts the regime read with no visible symptom. See verify_sign.py.

Liquidity gate runs FIRST and is blocking. A thin chain returns UNRELIABLE
rather than a number, because a number that reaches the page gets used
regardless of the caveat attached to it.

Usage
-----
  gex_scan.py VLO
  gex_scan.py VLO NVDA SCHW --json
  gex_scan.py VLO --pivot 320 --stop 337.50
  gex_scan.py --snapshot .data/VLO/2026-08-18.json

Exit codes: 0 ok, 1 no chain, 2 all tickers failed the gate, 3 IO error.
Research and educational output only. Not financial advice.
"""
from __future__ import annotations

import argparse
import json
import sys
import warnings

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

warnings.filterwarnings("ignore")

RISK_FREE = 0.04
MAX_DTE = 45
GATE_NEAR_OI = 2_000
GATE_N_STRIKES = 8
HIGH_NEAR_OI = 10_000
HIGH_N_STRIKES = 15
HIGH_NEAR_SHARE = 0.25
STALE_NEAR_SHARE = 0.15
SIGN_CONTRACT = {"call": 1.0, "put": -1.0}   # Model A
CONTRACT_LABEL = "Model A (dealers long calls / short puts)"


# ----------------------------------------------------------------- pricing --
def bs_price(S, K, T, r, q, sig, cp):
    d1 = (np.log(S / K) + (r - q + sig * sig / 2) * T) / (sig * np.sqrt(T))
    d2 = d1 - sig * np.sqrt(T)
    if cp == "c":
        return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)


def implied_vol(price, S, K, T, r, q, cp):
    """Invert IV. Returns (iv, low_conf) or (None, False) if unusable."""
    intrinsic = max(S - K, 0) if cp == "c" else max(K - S, 0)
    if price is None or price <= intrinsic + 0.01:
        return None, False
    try:
        iv = brentq(lambda s: bs_price(S, K, T, r, q, s, cp) - price, 1e-4, 6.0)
    except (ValueError, RuntimeError):
        return None, False
    if not (0.05 <= iv <= 3.0):
        return None, False
    return iv, price <= 0.05          # min-tick quotes bias IV upward


def bs_gamma(S, K, T, r, q, sig):
    if T <= 0 or sig <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r - q + sig * sig / 2) * T) / (sig * np.sqrt(T))
    return np.exp(-q * T) * norm.pdf(d1) / (S * sig * np.sqrt(T))


# -------------------------------------------------------------- chain load --
def load_yfinance(ticker):
    """Return (spot, rows) where rows = [(K, T_years, right, oi, iv, low_conf)]."""
    import pandas as pd
    import yfinance as yf

    t = yf.Ticker(ticker)
    spot = float(t.fast_info["last_price"])
    today = pd.Timestamp.utcnow().tz_localize(None).normalize()
    rows = []
    for exp in t.options:
        dte = (pd.Timestamp(exp) - today).days
        if not 0 < dte <= MAX_DTE:
            continue
        T = dte / 365.0
        ch = t.option_chain(exp)
        for right, df in (("call", ch.calls), ("put", ch.puts)):
            for _, r in df.iterrows():
                oi = 0 if pd.isna(r.openInterest) else int(r.openInterest)
                iv = None if pd.isna(r.impliedVolatility) else float(r.impliedVolatility)
                if iv is not None and not (0.05 <= iv <= 3.0):
                    iv = None
                rows.append((float(r.strike), T, right, oi, iv, False))
    return spot, rows


def load_snapshot(path):
    with open(path) as f:
        d = json.load(f)
    spot = float(d["spot"])
    rows = [(float(r["strike"]), float(r["T"]), r["right"],
             int(r.get("open_interest", 0)),
             r.get("implied_volatility"), bool(r.get("low_conf", False)))
            for r in d["chain"]]
    return spot, rows


# ------------------------------------------------------------------- gate ---
def run_gate(spot, rows):
    band = [r for r in rows if spot * 0.9 < r[0] < spot * 1.1]
    near_oi = sum(r[3] for r in band)
    n_strikes = len({r[0] for r in band if r[4] is not None})
    total_oi = sum(r[3] for r in rows) or 1
    near_share = near_oi / total_oi
    ok = near_oi >= GATE_NEAR_OI and n_strikes >= GATE_N_STRIKES
    if not ok:
        tier = "UNRELIABLE"
    elif (near_oi >= HIGH_NEAR_OI and n_strikes >= HIGH_N_STRIKES
          and near_share >= HIGH_NEAR_SHARE):
        tier = "HIGH"
    else:
        tier = "MED"
    if ok and near_share < STALE_NEAR_SHARE:
        tier = "MED"
    return ok, tier, int(near_oi), int(n_strikes), round(near_share, 3)


# ---------------------------------------------------------------- analysis --
def analyse(spot, rows, sign=None, pivot=None, stop=None, q=0.0):
    sign = sign or SIGN_CONTRACT
    ok, tier, near_oi, n_strikes, near_share = run_gate(spot, rows)
    if not ok:
        return {"gate": "FAIL", "tier": tier, "spot": spot,
                "near_oi": near_oi, "n_strikes": n_strikes,
                "need_oi": GATE_NEAR_OI, "need_strikes": GATE_N_STRIKES}

    live = [(K, T, right, oi, iv, lc) for (K, T, right, oi, iv, lc) in rows if iv]
    if not live:
        return {"gate": "FAIL", "tier": "UNRELIABLE", "spot": spot,
                "near_oi": near_oi, "n_strikes": 0,
                "need_oi": GATE_NEAR_OI, "need_strikes": GATE_N_STRIKES}

    per, low_conf_strikes = {}, set()
    for K, T, right, oi, iv, lc in live:
        g = bs_gamma(spot, K, T, RISK_FREE, q, iv)
        per[K] = per.get(K, 0.0) + sign[right] * g * oi * 100 * spot * spot * 0.01
        if lc:
            low_conf_strikes.add(K)

    net = sum(per.values())
    call_wall = max(per, key=per.get)
    put_wall = min(per, key=per.get)

    # ladder: strikes above spot >= 25% of the wall magnitude
    peak = per[call_wall]
    ladder = sorted(K for K, v in per.items() if K > spot and peak > 0 and v >= 0.25 * peak)

    # gamma flip: portfolio root, not the per-strike approximation
    grid = np.linspace(spot * 0.75, spot * 1.25, 260)
    tot = np.array([
        sum(sign[r] * bs_gamma(s, K, T, RISK_FREE, q, iv) * oi * 100 * s * s * 0.01
            for K, T, r, oi, iv, _ in live)
        for s in grid])
    cross = np.where(np.diff(np.sign(tot)))[0]
    flip = float(grid[cross[np.argmin(abs(grid[cross] - spot))]]) if len(cross) else None

    atm = sorted(live, key=lambda r: abs(r[0] - spot))[:4]
    atm_iv = float(np.mean([r[4] for r in atm]))
    T_near = min(r[1] for r in live)
    band = spot * atm_iv * np.sqrt(T_near)

    out = {
        "gate": "PASS", "tier": tier, "spot": spot, "sign_contract": CONTRACT_LABEL,
        "near_oi": near_oi, "n_strikes": n_strikes, "near_money_share": near_share,
        "net_gex": net, "regime": "STICKY" if net > 0 else "SLIPPERY",
        "call_wall": call_wall, "call_wall_value": per[call_wall],
        "put_wall": put_wall, "put_wall_value": per[put_wall],
        "ladder": ladder, "gamma_flip": flip,
        "atm_iv": atm_iv, "dte_nearest": round(T_near * 365),
        "noise_band_1sd": band, "noise_low": spot - band, "noise_high": spot + band,
        "low_conf_strikes": sorted(low_conf_strikes),
        "per_strike": {str(k): v for k, v in sorted(per.items())},
    }
    if pivot:
        out["wall_headroom_pct"] = (call_wall - pivot) / pivot * 100
    if stop:
        out["stop_distance_pct"] = (spot - stop) / spot * 100
        out["stop_clears_noise"] = (spot - stop) > band
    return out


# ----------------------------------------------------------------- report ---
def report(tk, r):
    print(f"=== {tk} ===")
    if r["gate"] == "FAIL":
        print(f"  UNRELIABLE - chain too thin to read.")
        print(f"  near-money OI {r['near_oi']:,} (need {r['need_oi']:,}) "
              f"across {r['n_strikes']} strikes (need {r['need_strikes']}).")
        print("  No regime, no walls, no levels computed.\n")
        return
    s = r["spot"]
    print(f"  spot ${s:,.2f} | {r['tier']} | {r['sign_contract']}")
    print(f"  regime      {r['regime']}   net GEX ${r['net_gex']:,.0f} per 1% move")
    print(f"  call wall   ${r['call_wall']:,.2f} (${r['call_wall_value']:,.0f}) "
          f"{(r['call_wall']/s-1)*100:+.1f}%")
    print(f"  put wall    ${r['put_wall']:,.2f} (${r['put_wall_value']:,.0f}) "
          f"{(r['put_wall']/s-1)*100:+.1f}%")
    if r["ladder"]:
        print(f"  ladder      {' -> '.join(f'${k:g}' for k in r['ladder'])}")
    print(f"  gamma flip  " + (f"${r['gamma_flip']:,.2f} "
          f"{(r['gamma_flip']/s-1)*100:+.1f}%" if r["gamma_flip"] else "none within +/-25%"))
    print(f"  noise band  ATM IV {r['atm_iv']:.1%} -> +/-${r['noise_band_1sd']:,.2f} "
          f"({r['noise_band_1sd']/s:.2%})  ${r['noise_low']:,.2f}-${r['noise_high']:,.2f}")
    print(f"  nearest exp {r['dte_nearest']} DTE"
          + ("   << walls strongest now, gone after expiry" if r["dte_nearest"] <= 5 else ""))
    if "wall_headroom_pct" in r:
        print(f"  headroom    {r['wall_headroom_pct']:+.1f}% from pivot to call wall")
    if "stop_clears_noise" in r:
        verdict = "CLEARS" if r["stop_clears_noise"] else "SITS INSIDE - will be hit by noise"
        print(f"  stop check  {r['stop_distance_pct']:.1f}% vs 1sd "
              f"{r['noise_band_1sd']/s:.1%} -> {verdict}")
    if r["low_conf_strikes"]:
        print(f"  LOW CONF    IV inverted from min-tick quotes at: "
              f"{', '.join(f'${k:g}' for k in r['low_conf_strikes'][:8])}")
    print("  cannot say  sign is an assumption | OI is T-1 | walls expire | no direction\n")


def main():
    ap = argparse.ArgumentParser(description="Dealer gamma exposure from a free option chain.")
    ap.add_argument("tickers", nargs="*", default=[])
    ap.add_argument("--snapshot", help="known-answer chain JSON ({spot, chain:[...]}) "
                    "instead of fetching -- see tests/fixture_*.json for the schema")
    ap.add_argument("--pivot", type=float, help="VCP pivot, for wall headroom")
    ap.add_argument("--stop", type=float, help="proposed stop, for the noise-band check")
    ap.add_argument("--spot", type=float, help="pin spot to this price (e.g. from another "
                    "step's snapshot) instead of the chain's own quote; the option chain "
                    "itself still comes from --snapshot or a live fetch. Only valid with "
                    "--snapshot or a single ticker.")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.spot and not a.snapshot and len(a.tickers) != 1:
        ap.error("--spot needs --snapshot or exactly one ticker (which price would it pin?)")

    results, any_pass = {}, False
    try:
        if a.snapshot:
            spot, rows = load_snapshot(a.snapshot)
            if a.spot:
                spot = a.spot
            name = a.snapshot
            results[name] = analyse(spot, rows, pivot=a.pivot, stop=a.stop)
        else:
            if not a.tickers:
                ap.error("give at least one ticker, or --snapshot")
            for tk in a.tickers:
                tk = tk.upper()
                try:
                    spot, rows = load_yfinance(tk)
                except Exception as e:
                    print(f"=== {tk} === fetch failed: {e}\n", file=sys.stderr)
                    continue
                if not rows:
                    print(f"=== {tk} === no chain within {MAX_DTE} DTE\n", file=sys.stderr)
                    continue
                if a.spot:
                    spot = a.spot
                results[tk] = analyse(spot, rows, pivot=a.pivot, stop=a.stop)
    except OSError as e:
        print(f"IO error: {e}", file=sys.stderr)
        return 3

    if not results:
        return 1
    for k, v in results.items():
        any_pass |= v["gate"] == "PASS"
    if a.json:
        print(json.dumps(results, indent=2, default=float))
    else:
        for k, v in results.items():
            report(k, v)
        print("Research and educational output only. Not financial advice.")
    return 0 if any_pass else 2


if __name__ == "__main__":
    sys.exit(main())
