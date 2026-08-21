---
name: market-growth-intelligence
description: Use when growth must be explained by the outside world rather than by a company slide — "where is this growth actually coming from", "is the market growing or is it taking share", "who captures the profit in this industry", "is store expansion cannibalising existing stores", "is overseas expansion actually working", "is that revenue real end-demand or channel stuffing", or "can they keep gaining share". It gates metric comparability, decomposes reported growth into category momentum, share change, and M&A, and tests whether new channels, new stores, and new countries add genuinely incremental demand.
---

# Market & Growth Intelligence

## Overview

Explain **how the external growth system works** after Layer 0 has framed the business. Determine whether demand/category structure is expanding, who captures the profit, why the company should gain or lose share, which reported growth vectors are real and incremental, and whether geographic/channel expansion is replicating rather than cannibalizing.

Read `references/methodology-router.md` and `references/research-foundations.md`. Load focused references only when their trigger applies.

## Required investigation

1. Run the **Metric Comparability Gate** before any multi-period trend. Mark material series `COMPARABLE`, `ADJUSTED_COMPARABLE`, `NOT_DIRECTLY_COMPARABLE`, or `UNRESOLVED`; state the demand-evidence basis (for example sell-in vs **sell-through**, usage, bookings, or GMV) when channel inventory can distort demand. Where the company reports a profit measure of its own definition ("core profit", "adjusted EBITDA"), also run the mandatory **Adjusted-to-Statutory Reconciliation** and record `adjusted_profit_reconciliation`; an unreconciled adjusted figure may not be used as a growth base.
2. Diagnose **Demand & Category Evolution** using the economic demand unit appropriate to the business. Classify the regime as structural/cyclical tailwind, stable, headwind, or unresolved. Do not substitute consultant TAM for demand evidence.
3. Build the **competitive system**: direct rivals, substitutes, entrants, relative growth/share, and the causal mechanism behind share gain/loss. A low share is not a runway thesis.
4. When value capture is non-obvious, map **Industry Structure / Profit Pool / Value Migration** and identify who receives incremental economics as the market grows.
5. Build **Growth Decomposition** in two levels: portfolio/category/geography momentum + market-share change + M&A/divestiture; then reconcile operating drivers such as volume, price, mix, existing-unit productivity, new units, product, channel, customer usage, and geography without double counting.
6. For material channel/product changes, test **net incrementality**: new buyers/customers and occasions less cannibalization, including halo/recapture effects. Also test **Expansion Incrementality** for new stores, facilities, capacity, or geographies: new-unit contribution net of cannibalization/density effects on existing units. Never label delivery/app/channel or footprint growth highly incremental without evidence.
7. For material cross-border expansion, test **International Replication** using local adoption/productivity plus CAGE/AAA logic only as relevant. Store/capacity count alone is not proof.
8. Track major growth initiatives as **Promise → Action → Result** and classify **Evidence Trajectory** as improving, stable, deteriorating, or unresolved.
9. If new evidence invalidates the Layer 0 frame, emit `SCOPE_CHALLENGE`; do not silently redefine the company.

## Adaptive routing

Always run comparability, demand/category, competitive position, and growth decomposition. Route consumer availability/CEP, profit-pool/Five-Forces, channel incrementality, value migration, and international modules only when material.

## Output

Produce `market_growth_pack` exactly as defined in `../future-compounder/references/pipeline-contract.md` and append to the shared Evidence Ledger.

## DoD

Complete only when the analysis explains category regime, value capture, share mechanism, the reconciliation of any company-defined profit measure to statutory profit, strategic and operating growth sources, material channel/geographic/**Expansion Incrementality**, demand evidence basis including sell-in vs sell-through where relevant, execution trajectory, counter-evidence, and unresolved gaps without double counting.

**STOP:** Do not perform full unit-return/ROIIC analysis, per-share economics, capital allocation, final compounder verdict, valuation, or BF-report synthesis. Pass economic consequences to downstream skills.

---

Research and educational output only. Not financial advice.
