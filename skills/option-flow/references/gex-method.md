# GEX Method — formulas, sign contract, and code

Read when implementing or auditing the computation. Everything here is deterministic; nothing in this file involves judgement.

---

## 1. The sign contract (read this first)

Black-Scholes gamma is **identical and positive for a call and a put at the same strike and expiry**. This follows directly from put-call parity: the two options differ by a forward and a bond, neither of which has gamma.

Therefore the call-positive / put-negative sign used in every GEX aggregate is **not a property of the Greek**. It is an assumption about who holds the inventory, and published treatments disagree about it silently.

**Consequence, demonstrated on real chains:** flipping the convention negates net GEX *exactly*, while vanna, charm and the gamma-flip level stay invariant. Every magnitude continues to look correct. A single mislabelled term therefore inverts the regime read — sticky and slippery swap places — with no visible symptom.

**Contract adopted here — Model A (SqueezeMetrics open-interest proxy):**

```
dealers are LONG calls   -> call gamma carries a POSITIVE sign
dealers are SHORT puts   -> put  gamma carries a NEGATIVE sign
```

Rationale: investors typically write covered calls against holdings and buy protective puts, putting dealers on the opposite side of both. This is a behavioural generalisation, not a measurement. **Print the contract in every output.**

Two alternatives exist and are *not* used here: Model B (dealers short both, appropriate when customer flow is known to be net long options) and Model C (net-directional-open-interest estimation, which needs open/close classification unavailable in free data). If a future version switches models, that is a version bump and the output label must change with it.

---

## 2. Per-strike aggregation

```
strike_gex(K) = gamma(K) * open_interest(K) * 100 * spot^2 * 0.01
                calls positive, puts negative per the contract above

net_gex = sum of strike_gex over all strikes, all expiries with 0 < DTE <= 45
```

Unit: **dollars of stock the dealer complex must trade per 1% move in spot.** The `* 100` is the contract multiplier; `spot^2 * 0.01` converts per-share gamma into a dollar figure per 1% move.

The 45-DTE ceiling is a practical cut: beyond it, gamma per contract is small enough that the contribution is dominated by OI noise, while the strike count roughly doubles.

---

## 3. Implied volatility — invert from the OTM side only

Deep-ITM options carry almost no vega. Inverting IV from their prices produces unstable or non-convergent values that then propagate into gamma.

```
for each strike K:
    if K <  spot:  invert IV from the PUT  price
    if K >= spot:  invert IV from the CALL price
    apply that single IV to both call and put gamma at K
```

Reject or flag any strike where:
- price <= intrinsic + 0.01 (no time value, IV undefined) -> skip
- solved IV < 0.05 or > 3.0 (non-convergent or absurd) -> skip
- the quote sits at the minimum tick (typically $0.01-$0.05) -> **keep but mark LOW CONF**; these invert to upward-biased IV, and dropping them silently shifts the aggregate

```python
from scipy.optimize import brentq
from scipy.stats import norm
import numpy as np

def bs_price(S, K, T, r, q, sig, cp):
    d1 = (np.log(S/K) + (r - q + sig*sig/2)*T) / (sig*np.sqrt(T))
    d2 = d1 - sig*np.sqrt(T)
    if cp == 'c':
        return S*np.exp(-q*T)*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    return K*np.exp(-r*T)*norm.cdf(-d2) - S*np.exp(-q*T)*norm.cdf(-d1)

def implied_vol(price, S, K, T, r, q, cp):
    intrinsic = max(S-K, 0) if cp == 'c' else max(K-S, 0)
    if price <= intrinsic + 0.01:
        return None
    try:
        return brentq(lambda s: bs_price(S,K,T,r,q,s,cp) - price, 1e-4, 6.0)
    except ValueError:
        return None

def bs_gamma(S, K, T, r, q, sig):
    d1 = (np.log(S/K) + (r - q + sig*sig/2)*T) / (sig*np.sqrt(T))
    return np.exp(-q*T) * norm.pdf(d1) / (S * sig * np.sqrt(T))
```

---

## 4. Walls and the ladder

```
call_wall = argmax over K of net_gex(K)
put_wall  = argmin over K of net_gex(K)
```

A single wall is rarely the whole story. Report the **ladder**: every strike above spot holding >= 25% of the call wall's magnitude, in order. Four consecutive strikes at 60-100% of the maximum is a materially different structure from one isolated spike, and only the ladder makes that visible.

**A wall requires both factors.** A strike near spot with negligible OI is not a wall; a strike with enormous OI 40% away carries gamma near zero and is not a wall either. Report OI alongside the GEX value so the reader can see which factor is doing the work.

---

## 5. Gamma flip

The flip is the spot level at which net GEX changes sign. Two ways to compute it, and they are not equivalent.

**Portfolio root (correct).** Sweep hypothetical spot levels, recomputing *every* option's gamma at each level, and find where the total crosses zero:

```python
grid = np.linspace(S*0.75, S*1.25, 260)
totals = []
for s in grid:
    g = np.array([bs_gamma(s, K, T, r, q, sig) for K, T, sig in chain])
    totals.append((sign * g * oi * 100 * s * s * 0.01).sum())
totals = np.array(totals)
cross = np.where(np.diff(np.sign(totals)))[0]
flip = float(grid[cross[np.argmin(abs(grid[cross] - S))]]) if len(cross) else None
```

**Per-strike approximation (wrong, but common).** Taking the strike where cumulative GEX crosses zero. This produces a class of false flips because it holds each option's gamma fixed at today's spot instead of recomputing it. Do not use it.

If no crossing exists within +/-25%, report `none within +/-25%` rather than extrapolating.

---

## 6. Noise band

```
noise_band_1sd = spot * ATM_IV * sqrt(T_nearest_expiry_in_years)
```

ATM IV is the mean of the four strikes nearest spot. Report as a dollar figure, a percentage, and the resulting range.

Interpretation to use in output: about two-thirds of comparable periods end inside this band; roughly one in three end outside it, split evenly between directions. **One-in-three outside is normal, not anomalous.**

---

## 7. Near-money share

Total OI can be dominated by deep-ITM legacy positions with gamma near zero.

```
near_money_share = OI within +/-10% of spot / total OI
```

Below ~15% the chain is technically liquid but structurally stale: the aggregate is driven by positions that generate no hedging flow. Report it and mark the regime read MED confidence.
