# Investment Synthesis

Synthesize a completed business narrative, an intrinsic valuation, and an earnings/sentiment read into a decision package — thesis, scenario timeline, and a conditional investment plan — in the spirit of Aswath Damodaran.

## What it does

- Confirms it has the upstream inputs (narrative, valuation, earnings) — an explicit input contract
- Writes a one-paragraph thesis: what you pay, what you get, what must be true, the asymmetry
- Maps Bull/Base/Bear onto a 12/24/36-month timeline, weights by probability, and computes expected value
- Produces a conditional investment plan: entry & margin of safety, sizing & staging, conviction-builders, thesis-breakers, horizon
- Tailors the plan to the setup archetype (quality compounder / deep-value / cyclical / GARP)
- Lists the 3–5 key risks ranked by impact on fair value

## Triggers

`build the investment thesis`, `synthesize this into a recommendation`, `should I buy at this price`, `what's my plan for X`, `scenario analysis bull base bear`, `expected return`, `price targets over 1-3 years`, `margin of safety and position sizing`, `what would break the thesis`. Also runs as Step 5 of `both-stock-analysis`.

## Prerequisites

This is a synthesis step. It requires, as inputs: a business narrative (e.g. from `business-narrative`), an intrinsic valuation with sensitivity + Bull/Base/Bear (e.g. from `company-valuation`), and an earnings/sentiment read (e.g. from `earnings-recap` + `earnings-preview`). If run standalone without these, it will ask for them rather than invent them.

## Output

A decision package: thesis paragraph, scenario-timeline table with probabilities and expected value, a conditional investment plan, the setup archetype, key risks, and the not-financial-advice disclaimer.

## Reference Files

- `references/scenario_math.md` — Value-to-price convergence, building 12/24/36-month targets, expected-value math, probability discipline, and the margin-of-safety / position-sizing guide
- `references/thesis_patterns.md` — Setup archetypes and how entry, sizing, horizon, and what-to-watch differ for each

## Disclaimer

For research and educational purposes only. Not financial advice. It frames a conditional plan, never a buy/sell command.
