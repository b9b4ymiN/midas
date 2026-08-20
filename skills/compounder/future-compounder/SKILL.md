---
name: future-compounder
description: Use when the question is whether a company can keep compounding business value per share for many years, rather than what it is worth today — "is NVDA a compounder", "can CPALL still grow for another decade", "is this a 100-bagger candidate", "quality compounder or just a hot stock", "will they keep earning good returns on the cash they reinvest", "run the Future Compounder analysis on TSLA", or any request framed around long-term compounding, reinvestment runway, or Christopher Mayer's 100 Baggers. It orchestrates six specialist skills and keeps potential, evidence maturity, and confidence as three separate verdicts. It is deliberately not a valuation — it produces no DCF, no fair value, no target price, and no entry timing.
---

# Future Compounder

## Overview

Orchestrate a Mayer-centered investigation. Core question: **can this company deploy incremental capital at attractive returns, at meaningful scale, for long enough to create exceptional per-share compounding?**

## Required sub-skills

Use, in order:
0. `business-identity-scope` — mandatory Layer 0 framing gate
1. `market-growth-intelligence` — mandatory Layer 1 external-growth gate
2. `business-economic-engine`
3. `reinvestment-runway`
4. `compounder-grill`
5. `compounder-bf-report`

Read `references/pipeline-contract.md` before handoffs. Layer 0 precedes Layer 1; Layer 1 precedes internal economics.

## Operating rules

- Preserve one Evidence Ledger across the run.
- Validate each upstream DoD before downstream work.
- Pass `UNRESOLVED` and thesis-critical **Data Gaps** forward; never silently fill them.
- Short histories do not reject young companies. Keep Potential, Evidence Maturity, and Confidence separate.
- Keep DCF, target price, technical signals, portfolio sizing, and holding dashboards outside this core pipeline.
- Do not let downstream writing upgrade a management claim or inference into a fact.

## Data sources

Pull quantitative facts through the `har-to-api` data layer when it is available: it records
source, as-of date, and URL per figure, which carries straight into the Evidence Ledger unchanged.
Qualitative evidence - segment mix, management promises, channel and cohort disclosure - must come
from primary filings, investor material, and calls, never from a scraped summary.

## Layer 0 framing gate

Require `business_identity_pack` before Layer 1. Inherit its candidate frame, arena classes/relationships, alternative frame, and scope risks. If downstream evidence materially changes them, emit `SCOPE_CHALLENGE` and rerun Layer 0.

## Layer 1 external-growth gate

Require `market_growth_pack` before the Business Economic Engine. Separate category/demand momentum, profit capture, share change, M&A, operating vectors, channel/expansion incrementality, international replication, and metric comparability. Layer 1 explains **where growth comes from**; downstream skills explain what it earns.

## Loop gate before final report

Verify explicitly:
0. Is the Business Identity & Market Scope framed without product myopia, TAM inflation, or optionality double counting?
1. Is the external growth system understood: category regime, profit capture, share mechanism, growth decomposition, channel/geographic incrementality, and KPI comparability?
2. Is the business/Economic Unit and repeatability understood?
3. Does Growth Architecture connect to corporate and **per-share** economics?
4. What does incremental capital appear to earn?
5. How much reinvestment is attractive and **financial resilience** sufficient to finance it?
6. Does capital allocation support or destroy the core engine?
7. What supports Duration and what can cause decay?
8. What does the outside-view **base rate** imply, and what company evidence updates that prior?
9. Where is the evidence on the Evidence Ladder?
10. Was counter-evidence actively sought and are Kill Conditions explicit?
11. Does the **reverse** 10x business-reality check avoid impossible share, margin, capital, funding, or dilution assumptions?

If a thesis-critical answer remains unknown, preserve `UNRESOLVED`, reduce certainty, and surface the next evidence needed.

## Final DoD

A full run requires Layer 0 scope, Layer 1 external growth, Return × Reinvestment × Duration, per-share translation, financeability, outside view, evidence maturity, counter-thesis, reverse reality, and traceable gaps.

**STOP:** The master orchestrates and validates. It does not redo specialist research, valuation, or holding analysis.

---

Research and educational output only. Not financial advice.
