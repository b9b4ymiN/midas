---
name: business-economic-engine
description: Use when the money-making machine inside a company is still unclear — "how does this business actually make money", "what are the unit economics", "is one store or one customer profitable", "why does revenue grow but profit does not", "does growth actually reach shareholders per share", "is reported ROIC distorted by R&D or marketing spend", or "do the economics improve as it scales". It rebuilds the Economic Unit, traces growth from external driver through capital, output, and mix into revenue, cash flow, and per-share owner economics, and flags businesses whose economics reset with every product generation.
---

# Business Economic Engine

## Overview

Discover how the business creates cash and owner value before judging runway. Consume `market_growth_pack` as the source of external demand/category, competitive-share, channel, and geographic growth evidence; then translate those drivers through the business model and **Economic Unit** into corporate and per-share economics.

Read `references/evidence-ledger.md`, `references/economic-unit-guide.md`, `references/growth-architecture.md`, `references/per-share-economics.md`, and `references/intangible-capital.md`.

## Required investigation

1. Reconstruct who pays, for what, why, how often, through which channel, and where profit appears.
2. Identify one or more Economic Units that reveal incremental economics. Hybrid businesses may require multiple engines.
3. Test **repeatability**. Distinguish a repeatable unit/cohort from a **product-cycle** or one-off launch whose economics reset each generation.
4. Measure unit/cohort economics with metrics appropriate to the unit and maturity lag.
5. Start from `market_growth_pack.growth_decomposition` and build the internal **Growth Architecture**: external driver → capital/input → unit/cohort output → **volume/price/mix/capacity/geography/product/M&A** → revenue → contribution/NOPAT → FCF. Do not independently reinvent Layer 1 category/share/channel claims.
6. Build the **Micro → Corporate → Per-share** bridge. Reconcile unit economics to consolidated cash/returns, diluted share count, SBC/issuance/buybacks, and FCF/NOPAT per share where material.
7. Diagnose **intangible capital** when R&D, software, customer acquisition, brand, or similar spending can distort reported ROIC/reinvestment.
8. Classify **scale economics** as strengthening, stable, weakening, or unresolved using later cohorts/locations/capacity/product generations where available.
9. Separate structural drivers from temporary drivers, identify economic inflections, and tag material claims in the Evidence Ledger.

## Output

Produce `economic_engine_pack` exactly as defined in the pipeline contract.

## DoD

Complete only if it explains how the evidenced growth drivers from `market_growth_pack` translate into economics when the company adds one meaningful unit of input/capital, what causes growth, whether that unit is repeatable, how economics reach corporate cash/returns, and whether aggregate growth becomes **per-share owner economics**. Material intangible investment, product-cycle dependency, and scale-direction evidence must be addressed or explicitly `UNRESOLVED`.

**STOP:** Do not forecast runway, judge management capital allocation, classify the stock as a compounder, perform falsification synthesis, or write the BF report.

---

Research and educational output only. Not financial advice.
