# Scenario Math — Timeline, Expected Value, Margin of Safety

How to turn a static fair value into a forward timeline and a sized plan. Read alongside Steps 2–3 of `SKILL.md`. Keep the arithmetic transparent — the point is disciplined reasoning, not false precision.

## Contents
- Value-to-price: where return comes from
- Building the 12/24/36-month targets
- Expected value and probability discipline
- Margin of safety, sized
- Position sizing

---

## Value-to-price: where return comes from

A stock's forward price return over a holding period comes from two sources:

1. **Intrinsic value growth** — fair value itself compounds as the business grows earnings/cash flow (roughly the company's sustainable growth + shareholder yield).
2. **Gap closing** — if price sits below (or above) fair value, the gap can converge, but only if a catalyst forces the market to re-rate. No catalyst, no reliable convergence — a cheap stock can stay cheap.

A useful decomposition:
```
expected price ≈ today's fair value × (1 + value growth)^years  ... adjusted toward,
                 not necessarily fully to, fair value as the gap closes over the
                 convergence period IF a catalyst exists.
```
Be explicit about the convergence assumption (often 2–3 years) and name the catalyst. If you cannot name one, assume the gap closes slowly or not at all, and lean on value growth alone.

---

## Building the 12/24/36-month targets

Reuse the valuation's Bull/Base/Bear driver shifts (revenue growth ±, margin ±, WACC ∓, terminal g) rather than inventing prices:

- **Base** — fair value compounding at its value-growth rate, with the price↔value gap closing over the convergence period given the expected catalysts.
- **Bull** — the valuation's bull-case drivers (higher growth/margin, lower WACC) → a higher fair value, plus faster/fuller gap closing if sentiment turns.
- **Bear** — the thesis-breaker drivers → a lower fair value, and a gap that may widen if sentiment sours.

Spread each scenario's endpoint across 12/24/36 months along a sensible path (re-ratings rarely happen in a straight line; cyclicals and catalysts cluster). Keep targets inside what the drivers support — a target the DCF cannot produce is a guess wearing a number.

---

## Expected value and probability discipline

```
E[return] = p_bull · R_bull + p_base · R_base + p_bear · R_bear,   with  p_bull + p_base + p_bear = 1
```

Discipline:
- **Base usually ≥ 50%.** If you genuinely think bull and base are equally likely, your "base" is mislabelled.
- **Avoid 33/33/33.** Equal weights signal no view — if that is honestly the case, confidence is low and the margin of safety must be large.
- **Tie probabilities to the 3 P's and the sentiment read.** A "probable" base with washed-out sentiment skews the distribution favourably; a story that only reaches "plausible" caps the bull probability.
- **Report asymmetry, not just the mean.** A positive expected value with limited, asset-protected downside and large upside is the setup worth taking. A positive mean built on a fat-tailed bull case with an unprotected downside is fragile.

---

## Margin of safety, sized

Margin of safety = the discount to fair value you demand before committing. It scales with uncertainty. Rough guide (judgement, not a rule):

| Condition | Required discount to fair value |
|---|---|
| High confidence, wide ROIC−WACC spread, low leverage, narrow scenario range | ~10–15% |
| Moderate confidence, average quality | ~20–30% |
| Low confidence, thin/negative spread, high leverage, wide scenario range, "plausible-only" story | ~35–50%+ |

The worse the business quality and the wider the range of outcomes, the more you insist on price protection. A great business needs less discount than a fragile one — but "great" still does not mean "any price."

---

## Position sizing

Size from two factors, kept qualitative:
- **Conviction** — how firmly the four pillars agree and the 3 P's hold (the narrative confidence level carries through).
- **Asymmetry** — how skewed the expected-value distribution is (protected downside, large upside → larger size justified).

Practical posture:
- **Stage entries.** Commit in tranches against price and evidence rather than all at once; this respects the uncertainty in both value and timing.
- **Use the sentiment read for timing.** Priced-for-perfection (per the earnings setup) argues for patience and a deeper entry discount; a sentiment washout may mean the margin of safety is already on offer.
- **Let thesis-breakers cap size.** If a single sensitive input (from the valuation grid) can break the thesis, size smaller and watch that input.

Sizing is conviction × asymmetry, disciplined by what could go wrong — never a fixed percentage applied regardless of the setup.
