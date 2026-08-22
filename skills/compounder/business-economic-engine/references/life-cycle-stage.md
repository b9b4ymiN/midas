# Life Cycle Stage

## Why this is a separate reading

A company's *identity* — what business it is in — is contested, judgemental, and settled upstream in Layer 0. Its *stage* is not. Stage is where the business sits in its own financial arc, it is read from the cash flow statement, and it changes while the identity stays put.

Keeping the two apart matters because the second is what decides which measures mean anything. A tea brand moving from a franchise model that others fund to company-owned stores it funds itself is the same business in a different stage, and the toolkit has to follow the stage. Sector labels cannot do this job: industries mature the way companies do, so an industry label produces systematic mislabelling, and age is no better — Dickinson found it cannot even separate introduction firms from declining ones.

## The classifier

Dickinson (2011) derives five stages from the signs of the three cash flow sections. Two outcomes across three sections gives eight combinations, grouped into five stages on economic reasoning:

| | Introduction | Growth | Mature | Shake-out | Decline |
|---|---|---|---|---|---|
| **Operating** | − | + | + | +/− | − |
| **Investing** | − | − | − | +/− | + |
| **Financing** | + | + | − | +/− | +/− |

Enumerated, so nothing is ambiguous:

| Operating | Investing | Financing | Stage |
|---|---|---|---|
| − | − | + | Introduction |
| + | − | + | Growth |
| + | − | − | **Mature** |
| + | + | + | Shake-out |
| + | + | − | Shake-out |
| − | − | − | Shake-out |
| − | + | + | Decline |
| − | + | − | Decline |

The reasoning behind the three clean cases: an introduction-stage firm has not learned its cost structure so operations consume cash, it invests anyway on the expectation of growth, and it must raise the money. A growth-stage firm covers operations but still needs outside capital to fund the investment. A mature firm funds its own investment and returns the surplus. The remaining combinations are transitional or contracting.

**Recompute it every year.** The classifier is a snapshot, and its value is that a company moving between stages shows up without anyone having to decide that it has.

*Source: Dickinson, "Cash Flow Patterns as a Proxy for Firm Life Cycle", The Accounting Review 86(6), 2011. The table above is as reproduced in the published literature applying her model; the primary article was not directly accessible.*

## Mandatory adjustment: exclude securities flows

Investing cash flow as reported mixes two different things — capital put into the business, and a treasury portfolio being bought or sold. Dickinson's reasoning is about the first: investing cash flow is meant to show the magnitude of investment made in pursuit of growth. A company rolling a large securities portfolio can therefore be misclassified on a flow that has nothing to do with its growth.

**Classify on investing cash flow excluding purchases and sales of marketable securities, and report the raw classification alongside.** The data layer already carries the securities line, so this costs nothing.

The adjustment is not cosmetic and does not favour a direction. Measured live on the cached set, it moved two of six companies, in opposite directions:

- A vehicle auction operator read **Shake-out** on raw investing cash flow because it sold USD 1.22bn of securities to fund a repurchase. Excluding that, it is still investing USD 313m in the business and reads **Mature** — the adjusted answer is the true one.
- A power producer read **Mature** on raw investing cash flow while buying THB 30.7bn of securities. Excluding those, its operating investing is a net THB 18.3bn *inflow* and it reads **Shake-out** — again the adjusted answer is the informative one.

**Where the two readings differ, that difference is a finding.** It says the company is doing something material with its treasury that the headline cash flow statement folds into the same line as its capital spending. Record both and say which is which.

## What the stage is used for

**1. It gates which measures mean anything.** In Introduction and Decline, operating cash flow is negative, so a reinvestment rate computed on NOPAT is being divided by a number that carries no information. Those stages force the unit-economics path rather than the corporate-ratio path.

**2. It is a prior for Duration, not a verdict.** Dickinson's finding is that returns do not fade uniformly: five years on, mature and declining firms were still about seven points apart on return on net operating assets. Stage therefore carries information about persistence that a single-period return does not. A high return in Mature is a different claim from the same return in Shake-out.

**3. It detects transitions the identity work will not.** A company changing who funds its expansion changes stage while its Layer 0 frame is unchanged. That movement is evidence in its own right and belongs in the evidence trajectory.

## What the stage is NOT used for

**It never selects the business archetype, and it never sets the Potential label.** It is one input to the Duration leg and a gate on measure validity. A company is not downgraded for being Mature — most large compounders are Mature, and the mature signature (funding its own investment and returning the surplus) is what a self-funding compounder looks like.

**It does not override Layer 0.** Where the stage reading and the business frame appear to conflict, that is a `SCOPE_CHALLENGE` to be raised, not a licence to redefine the company from its cash flow statement.

## Required output

Add to `economic_engine_pack`:

```
"life_cycle_stage": {
  "stage": "Introduction | Growth | Mature | Shake-out | Decline",
  "signs": {"operating": "+", "investing": "-", "financing": "-"},
  "basis": "investing cash flow excluding securities purchases and sales",
  "raw_stage": "the classification on unadjusted investing cash flow",
  "divergence_note": "required whenever stage and raw_stage differ",
  "as_of": "period end",
  "prior_periods": "the stage in earlier years where computable, so a transition is visible"
}
```

`UNRESOLVED` is the correct answer where any of the three sections is unavailable — it is not a stage that can be guessed from the industry.

## Failure modes

- Classifying on raw investing cash flow for a company with a large securities portfolio.
- Reporting a single period and missing that the company has just changed stage.
- Reading Mature as a negative. It is the signature of a business that funds itself.
- Treating the stage as a substitute for the business frame, or letting it silently pick the measurement toolkit.
- Using age or sector as a shortcut when the cash flow statement is available.
