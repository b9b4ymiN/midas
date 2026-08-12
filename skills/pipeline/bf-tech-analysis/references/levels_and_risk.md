# Levels & Risk Geometry

How to build the levels (support/resistance, trendlines, channels, Fibonacci) and turn the read into tradeable **risk geometry** — entry zone, stop, targets, and the **R-multiple** — then link it to position sizing and the fundamental fair-value magnet. Read alongside Step 5 of `SKILL.md`.

---

## Support / resistance
- Build from **swing pivots** (`indicators.md` §2b) and prior reaction points; the more touches and the more recent, the more weight.
- **Volume shelves** (prices with heavy prior volume) are stronger S/R and represent overhead supply on the way up.
- Round numbers and prior breakout points (old resistance → new support) matter.
- Treat S/R as **zones**, not exact lines.

## Trendlines & channels
- An **uptrend line** connects rising swing lows; a **downtrend line** connects falling swing highs. Two touches define it, a third confirms.
- A **channel** is the trendline plus a parallel line on the opposite swings. For a **downtrend**, the channel's lower line projects how far a decline may run and the upper line is the level whose break signals a possible trend change.
- Fit objectively when needed via least-squares on the relevant swing points, then snap to the actual touches.

## Fibonacci
- **Retracement (entries):** 38.2 / 50 / 61.8 of the prior swing locate pullback **buy zones** in an uptrend. Prefer levels that are **confluent** with the respected MA and structural support (`indicators.md` §2a/§2b). A close below the 61.8 typically negates the pullback thesis.
- **Extension (up-targets):** 1.272 / 1.618 / 2.0 project objectives above the swing.
- **Downside targets:** apply extensions to the **down-leg** (and use the channel's lower line) to estimate where a decline could end — used both to *confirm a possible bottom* and to *project further downside* when the trend is intact.

---

## Risk geometry (the output that feeds the plan)

For the diagnosed setup, define four things — all as the toolkit produced them:

1. **Entry zone** — a band (e.g. the Fib ∩ MA ∩ support confluence), not a single tick.
2. **Stop** — just beyond the structure that **invalidates** the setup (below the pivot / last contraction / swing low / broken line), distance sanity-checked against **ATR** so it respects this stock's noise. Too tight = stopped by normal wiggle; too loose = poor R.
3. **Target(s)** — the nearest Fib extension / prior high / measured move, and the **fundamental fair value as the longer-term magnet/cap**.
4. **R-multiple** — `R = (target − entry) / (entry − stop)`. State reward-to-risk explicitly; a setup with < ~2R is usually not worth taking unless confluence is exceptional.

```
entry ≈ [zone low–high] · stop ≈ [level] (≈ k×ATR) · target₁ ≈ [Fib/structure] · magnet ≈ [fair value]
R(target₁) ≈ ( target₁ − entry ) / ( entry − stop )
```

---

## Confluence → conviction → size

Conviction rises with **confluence** (trend/stage + fitted MA + Fib + structure + volume behaving + no adverse divergence + the fundamental fair value pointing the same way). Translate to action **conditionally** (this skill recommends, it does not command):
- **High confluence + good R** → a fuller, still-**staged** entry; first tranche in the zone, add on confirmation/strength.
- **Mixed** → smaller starter, tighter trigger, or **wait** for the missing confirmation.
- **Volume/divergence warning present** → reduce size or stand aside until it clears.

## Linking to the fundamental work
- The technical read sets **when/where/how-much-risk**; the **fair value** sets **whether and the long-term target**.
- Pass to `investment-synthesis`: the **entry zone, stop, target(s), R, and the timing verdict** — which become the plan's entry, staging, and stop. The scenario timeline's price targets and the fair-value magnet should reconcile with the technical targets.
- The **margin of safety** (fundamental) and the **stop** (technical) are complementary risk controls — state both.

Everything here is research/education, not financial advice.
