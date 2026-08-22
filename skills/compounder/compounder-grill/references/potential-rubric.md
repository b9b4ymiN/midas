# Compounding Potential Rubric

Compounding Potential answers one question: **what rate of per-share business-value compounding does the evidence support, and is it durable?** It is not a measure of business quality, not a valuation, and not a prediction.

Read `hurdle-rates.md` first — every band below is conditional on the return clearing the two lines defined there.

## What the label is bound to

**Durable growth per year**, built from the mandatory measures the reinvestment layer computes:

```
durable growth = growth from new investment
               + growth from rising returns, ONLY the portion evidenced as pricing power

               − growth from slack removal        (3–5 year life, excluded)
               − effect of share-count reduction  (reported separately, excluded)
```

Buybacks are excluded deliberately. They raise per-share figures, they have a ceiling, and they depend on the price paid. A company whose per-share growth arrives only once repurchases begin is a capital-return story, and the verdict should not disguise it as a compounding engine.

## The bands

| Label | Durable growth | Must also hold |
|---|---|---|
| **Exceptional** | above 10% | incremental return ≥ 15% · no decay signature in the return series · evidence at Ladder level 4 or above · **and growth ≥ 1.5× the company's own category growth** |
| **Strong** | 6–10% | incremental return ≥ 15% · reinvestment runway still open, though its edge is visible |
| **Moderate** | 3–6% | return between the two hurdle lines · **or** a thesis-critical axis still `UNRESOLVED` |
| **Weak** | below 3% | return below the value-destruction line · **or** capital can be neither reinvested nor returned |
| **Broken** | negative | incremental capital destroys value |

**The category comparison** distinguishes a company compounding because it is winning from one carried by its market. A utility growing 8% durably where its category grows 3% is a rarer machine than a technology company growing 10% where its category grows 25% — the second is losing ground. Read category growth from `market_growth_pack.demand_category_evolution` and `growth_decomposition.strategic.category_momentum`; both are produced by the Layer 1 gate and need no separate research.

> **Calibration note.** The 3% / 6% / 10% cut-offs are **inferred, not published.** They were set so that Exceptional stays rare against the observed base rate for extreme compounding — Mayer's 100-baggers required roughly 20–26% per year sustained for 17–25 years, so a 10% floor is already far below that bar and should not be loosened. Attempts to retrieve the empirical growth-rate distributions that would replace these numbers were unsuccessful. Treat them as the most challengeable part of this file and change them here, in one place, when better evidence arrives.

## Three guards

Each guard exists because the rubric was run against real companies and produced a wrong answer without it. Apply all three before reading the bands.

### Guard A — measurement window

Use cumulative figures over **at least three years** for both numerator and denominator, and report the annual series alongside. Three is the practitioner floor for filtering capex lumpiness, working-capital seasonality and one-off tax effects; three to five years is the normal range.

*Why:* a single year of unusually heavy investment produces a reinvestment rate near 100% that no company sustains. One year is a decision; three years is a policy.

**This guard targets a measurement failure, not a young company.** The two cases are different and must not be conflated:

| Situation | Ruling |
|---|---|
| Three or more years of history exist but a shorter window was used | Measurement error. Recompute on the full window. Nothing is capped — the number was simply wrong |
| Fewer than three years of history, or the company sits in the Introduction or Growth stage with immature returns | Route to the **Emerging Compounder** path. Cap **Evidence Maturity**, never Potential |
| That path cannot be built either — no unit or cohort economics at all | Incremental return is `UNRESOLVED`; rule 3 then caps Potential at Moderate |

**Never treat length of history as an admission ticket.** A short record lowers Evidence Maturity; it does not lower Compounding Potential. This is not a preference — it is the framework's stated principle, and requiring a long return history is listed among its explicit anti-patterns. The reason is empirical: the companies that produced 100-fold returns had median sales around USD 170m and median market capitalisation around USD 500m at the point of purchase. They were small and proven, not old. A rule that grades on age would reject most of the reference class.

The substitute for missing history is not a longer wait but a different measurement. For a young company the most recent trailing twelve months carries more information than an older annual report, and where returns cannot be observed directly they are built forward: target mature margin anchored to comparables, capital intensity from a sales-to-capital ratio or capital per economic unit, and the implied return derived from the two. Every input in that bridge is tagged by evidence class, so the uncertainty is visible rather than hidden inside a projected return — which is what separates valuing a young company from merely pricing it.

### Guard B — the denominator must mean something

If adjusted invested capital is **less than one year of NOPAT, or negative**, the accounting return is void and may not be multiplied by anything. Fall back to `Δ NOPAT / Δ invested capital`, or to unit-level economics. Where neither is available, the incremental return is `UNRESOLVED` and Potential is capped at Moderate.

*Why:* sustained repurchases shrink book capital. A mature company that has bought back stock for a decade can report a return of several hundred percent, which describes its repurchase history and not its business.

### Guard C — the spread gate

Growth counts as positive evidence only where the incremental return clears the value-destruction line. Below it, Potential is capped at **Weak** no matter how attractive the growth rate looks; where the return is negative, the label is **Broken**.

*Why:* a company reinvesting more than its entire operating profit at a return below its cost of capital generates a healthy-looking growth number while making its owners poorer every year.

## Four rules

**1. The numbers are anchors, not instructions.** Move a company across a band when the evidence warrants it — but write the reason into the pack. An unexplained override is indistinguishable from an error.

**2. The weakest leg governs, and the label must say so.** Future compounding is a product of incremental return, reinvestment capacity and duration; a weak leg drags the product down. Where the leg ratings differ by more than one band, the label carries a qualifier naming the binding constraint — `Strong (runway-capped)`, `Moderate (return-capped)`. A bare label that hides a divergence is a failure of the report, not a simplification.

**3. An unresolved thesis-critical axis caps Potential at Moderate.** Most often this is the incremental return. Awarding Strong while the axis the framework calls decisive is unknown means guessing the answer and then grading the guess. If it cannot be measured, say so and accept the cap.

**4. Reinvestment and Duration high together is a claim, not a reading.** The forces that let a business scale quickly tend to shorten how long it stays on top; capital-light and fast-scaling usually means fast-fading, while capital-heavy and slow usually means durable. Rating both legs high requires an explicit account of why this company escapes the trade-off. Absent one, lower whichever leg has the thinner evidence.

## Banks and insurers

The durable-growth formula above is built on NOPAT over invested capital, and both are barred for a financial institution: its liabilities are the raw material of the business, not the funding of it, so putting them in a denominator produces a number that is arithmetically correct and answers nothing. The bands still apply — the pair that feeds them is substituted.

| | Standard business | Bank | Life insurer |
|---|---|---|---|
| What incremental capital earns | Δ NOPAT / Δ invested capital | Return on equity **attributable to owners** | Operating return on embedded value |
| How much can go back in | (net capex + working capital) / NOPAT | Retention ratio — earnings kept rather than paid out | Movement in contractual service margin |
| What binds it | The opportunity set | Regulatory capital, CET1 | The solvency position |

Durable growth for a bank is therefore **return on owners' equity × retention ratio**, the standard sustainable-growth identity, and it is capped by what the capital position will support: a bank can post a high return and still be unable to grow its book, and the constraint belongs in the reinvestment leg rather than being ignored.

For a life insurer the reinvestment leg turns on whether stored profit is growing. A flat contractual service margin alongside rising reported profit means the company is releasing profit already earned rather than writing new business worth having — the tank is being drained, not filled. Read the CSM as a movement, never a level, and treat a level CSM as a reinvestment leg near zero regardless of the headline growth rate.

Three rulings hold for both:

1. **State the equity basis on every figure.** Return on equity attributable to owners, not group equity, wherever minorities are material — the two can differ by tens of percent.
2. **The hurdle comparison moves to cost of equity**, not cost of capital, because the return being measured is an equity return.
3. **A missing embedded value for a life insurer is a thesis-critical gap.** Mark it `UNRESOLVED` and accept the Moderate cap under rule 3 rather than substituting book value and proceeding.

Record the substitution in `mandatory_measures` with `path: "sector_specific"`, naming which pair was used. A verdict whose measurement basis is not on the record cannot be reconstructed.

## The life-cycle stage as a Duration prior

`economic_engine_pack.life_cycle_stage` carries the stage read from the signs of the three cash flow sections. Use it when rating Duration, and read it as a prior rather than a verdict.

Returns do not fade at a uniform rate across stages: five years out, mature and declining firms remained roughly seven points apart on return on net operating assets. A given return therefore means different things depending on where the company sits, and the stage is measured rather than argued.

| Stage | What it implies for Duration | What it does not imply |
|---|---|---|
| **Mature** | The signature of a business funding its own investment and returning the surplus — the normal home of a self-funding compounder | Not a downgrade. Most large compounders read Mature |
| **Growth** | Still drawing outside capital; duration untested through a full cycle | Not a discount — Evidence Maturity carries the shortness of history, not Potential |
| **Shake-out** | Transitional. Ask what changed and whether the reinvestment leg is closing | Not decline; it is also the reading of a company mid-transition |
| **Introduction / Decline** | Operating cash flow is negative, so the corporate ratios are void | Force the unit-economics path per Guard B rather than grading on a meaningless denominator |

**A stage transition is evidence.** A company that has just moved stages has changed how its expansion is funded, and that shows up here before it shows up in a narrative. Where the stage moved and the Layer 0 frame did not, the movement is a finding about the engine, not a reason to redefine the business.

**Never let the stage set the label.** It informs one leg and gates measure validity. Reading Potential off the stage would be exactly the sector-label error the framework exists to avoid.

## Worked examples

Both are drawn from completed runs and can be checked against the packs.

### A high-return business with a closing runway

- Incremental return ~30–32%, stable across five years — clears both hurdle lines
- Reinvestment rate 32.6% of NOPAT cumulatively, **but falling: 50.4% → 25.1% → 18.1%**
- Durable growth 9.9%, decaying toward 5.3% on the current trend
- Duration strong: permitted land, two-sided liquidity, returns held through cycles
- Per-share compounding 13.2%/yr, achieved while the share count *rose* — earned operationally

**Verdict: `Strong (runway-capped)`.** Rule 2 supplies the qualifier: the return leg would support Exceptional, the reinvestment leg would not. Rule 4 is satisfied — the business is capital-heavy and slow-scaling, which is the profile in which a long duration is expected rather than surprising.

### A company whose incremental capital destroys value

- Revenue rose while operating profit fell over the same period — incremental return **negative**
- Balance sheet strong, category still growing, brand intact

**Verdict: `Broken`.** Guard C decides it before any band is consulted, and no strength elsewhere lifts it. This is the case the rubric exists for: without Guard C and Rule 3 the same evidence has previously supported a Strong reading, on the argument that the ingredients of a large compounder were present. Ingredients are not returns.
