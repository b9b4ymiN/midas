# Liquidity Gates — thresholds, tiers, and refusal rules

Read before computing anything. The gate runs first and can stop the skill entirely.

---

## Why a gate exists

GEX on a thin chain is not a weak signal — it is **noise with the appearance of precision**. A handful of contracts at one strike produces a "wall" indistinguishable in format from a genuine one.

The failure mode is observed, not hypothetical: a published dealer-positioning dashboard emitted a full calendar-spread trade plan, with confidence score and levels, on a chain holding 1,332 total contracts — while its own IV engine displayed `UNKNOWN` and its VRP field displayed `NA`. Every number on that screen was formatted identically to a reliable one.

**Operating principle:** a number that reaches the page will be used regardless of the caveat attached to it. The only effective control is to withhold the number.

---

## The gate

```
near_band  = strikes within +/-10% of spot
near_oi    = total open interest in that band, all expiries <= 45 DTE
n_strikes  = strikes in that band carrying a usable price

PASS  near_oi >= 2,000  AND  n_strikes >= 8
FAIL  otherwise
```

**On FAIL the entire output is:**

```
UNRELIABLE - chain too thin to read.
near-money OI [n] (need 2,000) across [k] strikes (need 8).
No regime, no walls, no levels computed.
```

Nothing else. No "but directionally it suggests", no greyed-out estimate.

---

## Why these two numbers

- **2,000 contracts** near the money is roughly 200,000 shares of hedging obligation concentrated where gamma is live. Below this, the aggregate is dominated by individual positions rather than a dealer complex, and one large trade rewrites the map.
- **8 strikes** is the minimum to distinguish a genuine concentration from a spike. With fewer, every strike looks like a wall relative to its neighbours.

Both are deliberately conservative. Tightening them is defensible; loosening them requires evidence, and the burden sits with whoever loosens.

---

## Quality tiers after PASS

| Tier | Condition | Effect on output |
|---|---|---|
| **HIGH** | near_oi >= 10,000 and n_strikes >= 15 and near_money_share >= 25% | Full read, all fields |
| **MED** | passes gate but not HIGH | Full read; regime marked MED; wall levels reported as zones (+/-1 strike), not points |
| **UNRELIABLE** | fails gate | Refusal line only |

Additional degradations that force MED regardless of counts:

- **Stale option prices against live spot.** Prior-close last-trade prices inverted against a live spot produce biased IV. Name the mismatch and both timestamps.
- **near_money_share < 15%.** Liquid but structurally stale.
- **Fallback data source.** Any field not from the live chain (e.g. a `--spot` pinned from elsewhere, or a `--snapshot` chain file).

---

## Non-US listings

Options chains outside US listings are, with rare exceptions, far below the gate. Expect UNRELIABLE and say so plainly rather than reaching for a proxy — there is no valid substitute, and a proxy here would be fabrication.

For Thai (SET) names specifically: single-stock options liquidity does not support this analysis. Return the refusal line.

---

## What "refuse" means downstream

If this skill's output feeds a larger analysis, a FAIL is a **normal expected outcome**, not an error. The rest of that analysis continues with "option flow unavailable — chain too thin" and proceeds on the technical and fundamental work alone.

A gate failure must not block the run, and must not degrade into a guess.
