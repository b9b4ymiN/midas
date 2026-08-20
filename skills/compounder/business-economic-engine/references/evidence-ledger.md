# Evidence Ledger Standard

## Claim types

| Type | Meaning | Example |
|---|---|---|
| FACT | Directly supported by primary/credible source | Revenue reported in filing |
| DERIVED | Calculation from cited facts | Store payback = capex / EBITDA |
| MANAGEMENT_CLAIM | Statement by management not independently proven | “Payback below 2 years” |
| MARKET_EXPECTATION | Consensus / market-implied expectation | Street revenue forecast |
| ASSUMPTION | Deliberate input for analysis | Mature margin assumption |
| ESTIMATE | Analyst estimate from incomplete data | Estimated capex/store |
| INFERENCE | Reasoned conclusion from evidence | Density likely improves delivery cost |
| UNVERIFIED | Material claim lacking adequate verification | Unconfirmed market share |

## Required ledger fields

- `claim_id`
- `claim`
- `claim_type`
- `source_title`
- `source_date`
- `source_locator` (page, section, table, transcript timestamp, or URL where allowed)
- `source_tier`
- `freshness`
- `interpretation_role`
- `confidence`
- `limitations`
- `used_in`

## Source hierarchy

1. Audited/regulatory filings
2. Company results, investor materials, transcripts
3. Government, academic, industry datasets
4. Professional analyst/specialist research
5. Reputable press/interviews
6. Community/social/anecdotal sources

Lower tiers may be useful for discovery or contradiction; they must not silently override stronger primary evidence.

## Evidence discipline

- One source may support multiple claims, but each claim gets its own interpretation role.
- A management claim remains `MANAGEMENT_CLAIM` even when repeated by press.
- A calculation is `DERIVED`, not `FACT`, even if all inputs are facts.
- `UNVERIFIED` is a valid result. Do not manufacture a number to close a gap.
