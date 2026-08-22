---
name: compounder-grill
description: Use when a compounding thesis exists and must survive attack before any capital is committed — "try to break this compounder thesis", "what would have to be true for this to work", "what does the base rate say", "am I just believing a good story", "what would make me sell", "stress-test this before I buy", or "what evidence am I actually standing on". It applies the outside view as a prior, ranks evidence on a Story-to-Persistence ladder, runs falsification tests, and reports Compounding Potential, Evidence Maturity, and Confidence as three separate verdicts rather than one score.
---

# Compounder Grill

## Overview

Turn all upstream evidence—including `market_growth_pack`—into a falsifiable compounder thesis. The job is not to reward attractive narratives; it is to determine what the evidence permits us to believe after both inside-view and **base rate** challenge.

Read `references/falsification-tests.md`, `references/base-rates.md`, `references/evidence-ladder.md`, `references/hurdle-rates.md`, `references/potential-rubric.md`, `references/confidence-rubric.md`, and `references/reverse-reality-check.md`.

## Required synthesis

Use **Future Compounding Economics ≈ Incremental Return × Reinvestment Capacity × Duration**. For each leg state supporting evidence, counter evidence, unknowns, and confidence.

Then:
1. Challenge the external-growth thesis: **category** regime, profit-pool direction, causal **share**-gain mechanism, Growth Decomposition, channel incrementality, international replication, and execution/evidence trajectory from `market_growth_pack`.
2. Apply the outside view / **base rate** as a **prior** and show the company-specific update.
3. Map evidence onto the **Evidence Ladder** (Story → Operating → Unit Economics → Corporate/Per-share Translation → Persistence).
4. Reconcile core economics with **per-share** economics, capital allocation, financial resilience, and **scale economics**.
5. Test repeatability, including **product-cycle** dependence where growth must be recreated through successive launches rather than retained cohorts/units.
6. Run all applicable falsification tests.
7. Perform the **reverse** **10x** business-reality check; 100x is optional stress and is **not a prediction or valuation**.

## Required classifications

Report separately:
- **Compounding Potential:** Exceptional / Strong / Moderate / Weak / Broken — assign with `references/potential-rubric.md`, whose three guards and four rules are mandatory, not advisory. Where the leg ratings diverge by more than one band the label carries a qualifier naming the binding leg.
- **Evidence Maturity:** Early / Developing / Established / Deep — assign with `references/evidence-ladder.md`
- **Confidence:** Low / Medium / High — assign with `references/confidence-rubric.md`

Also rate each leg separately — incremental return, reinvestment capacity, duration, per-share translation, financial resilience, capital allocation — and name the binding one. A single label that conceals a divergence between legs fails DoD.

Never combine these into one primary score. Never derive Confidence from Evidence Maturity or from Potential.

## Every verdict carries a review date

Kill and upgrade conditions say **what** would change the verdict. `review_schedule` says **when to look** — without it a verdict silently claims to be true forever, and the reader has no way to know whether the one in front of them is still live.

Set all of it, in `review_schedule`:

- `as_of` — the evidence cutoff this verdict rests on.
- `next_review` — at most twelve months later, with `next_review_event` naming the filing or result that makes that the right date, and `settles` naming which conditions that event can actually resolve.
- `cadence_basis` — one sentence, and the reason must be the fastest-moving evidence in the **binding leg**. A thesis bound by an annual capital budget is reviewed annually; one bound by monthly share data is not.
- `watch_triggers` — the events that would force an earlier look, each with what is observable and how long the question may stay open.
- `expires_on` — after this date the verdict may be read as history but may not carry a decision.

The design is borrowed from credit-rating surveillance, not invented here: a scheduled review at least annually whether or not there is news, plus event-driven watches with a bounded window. Do not set a cadence longer than the evidence that binds the verdict.

## Thesis pack

Produce the thesis pack exactly as defined in the pipeline contract, including supporting/counter evidence, critical unknowns, Kill Conditions, upgrade conditions, and the review schedule.

## DoD

The thesis must answer: whether the category/share/channel/geographic growth thesis survives adversarial review; what must be true for exceptional compounding; what outside view challenges it; how mature the evidence is; whether per-share/scale/funding/repeatability economics support the engine; whether the reverse reality check is plausible; what one or two developments would most seriously break the thesis; and when the verdict must be looked at again. A **bull-only** conclusion fails DoD, and so does a verdict with no review date.

**STOP:** Do not perform broad new research unless a critical contradiction cannot be adjudicated from existing packs. Do not perform valuation or write the BF report.

---

Research and educational output only. Not financial advice.
