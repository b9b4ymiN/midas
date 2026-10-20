# Evidence, numeric integrity and upstream ownership

## Evidence precedence

1. Original issuer filings, official exchange releases, management statements when clearly attributed.
2. Regulators, authoritative market sources and audited historical datasets.
3. Third-party aggregators and broker estimates, including date and coverage.
4. Upstream analyst's derived calculations, with formula, bases and inputs.
5. Unverified/inferred claims (explicitly labeled, never treated as proven fact).

Keep original provenance alongside each claim. Official sources do not validate *someone else's extrapolation* unless the underlying model assumptions are also separately supported.

## Minimum claim ledger columns

`id | originating_skill | source_ref | observed_as_of | financial_period | value | unit | basis | classification | verification | note`

Classification: `COMPANY_FACT | MARKET_FACT | CONSENSUS | DERIVED | ANALYST_ASSUMPTION | ILLUSTRATION`.

Verification: `PRIMARY_VERIFIED | CROSS_CHECKED | ARITHMETIC_VERIFIED | SOURCE_ONLY | UNVERIFIED | CONTESTED`. `SOURCE_ONLY` means faithfully copied from the originating research, **not** independently validated.

## Severity and action

| Level | Example | Gate | Owner |
|---|---|---|---|
| BLOCKER | Major source number contradicted, YoY sign wrong, model bridge broken, periods falsely compared, material claim with no provenance | Stop final handoff; propose rework | Source analytic skill (earnings/valuation/etc.) |
| MAJOR | Important ambiguity not yet proven to alter verdict; chart with incompatible series; quote without clear time stamp | Withhold affected exhibit/claim; disclose issue; decide if it is a BLOCKER for actual narrative | Source owner or editorial skill |
| MINOR | Redundant sentence, typo, legible chart improvement | Proceed and record | Editorial skill |

A price as of an intraday timestamp versus a close is not automatically a conflict; **label the distinct timestamps**. A discrepancy can arise from different definitions; do not assume fraud or a factual error when the bases differ.

## Math checks to attempt

- Year-over-year = `(current - previous) / abs(previous) * 100`; take care when baseline negative or near zero, and state why percentages become misleading.
- Percentage-point difference between comparable percentages = `new - old`.
- Fair value blending = `sum(weight * method_price) / sum(weights)` with weights explicitly defined.
- Scenario probabilities must add to `1.0` within declared precision.
- Expected return calculation must state whether dividends are included, price-as-of date, horizon and currency.
- EV to equity value deductions: beware adding gross debt and net debt twice, equity-like perpetual treatment and lease treatment consistency.
- ROIC versus WACC: prove numerator/denominator/lease policy match; do not just subtract.
- Check market prices/targets with timestamp, exchange suffix, split adjustment and FX if applicable.

The included deterministic validator supports only a handful of declared arithmetic operations. It does **not** validate DCF valuation methodology, source truth, corporate events, terminal value math or actual historical returns. A separate analyst or independent checker must still review those issues.

## Issue contract

Each issue contains `id`, `severity`, `status`, `owner`, `claim_ids`, `explanation`, `suggested_action` and `evidence_refs`. `status` can be `OPEN`, `RESOLVED`, `ACCEPTED_WITH_DISCLOSURE` (for non-blocker only). A `BLOCKER` must be `RESOLVED` before final handoff. Do not hide defects in appendix-only fine print when they materially affect the lead takeaway.

## Provenance examples

- "Company MD&A, Q2 FY2026, published 7 Aug 2026" is primary if actually inspected.
- "Reported by Yahoo Finance at 12:35 ICT, 20 Oct 2026" is market/aggregator with timestamp, **not** a company filing.
- "Model assumes WACC 9.5%" is an assumption, not an observed market fact.
- "The market believes permanent FCFF of X" is at best a reverse-DCF *interpretation conditional on all other input assumptions*. Never describe as a survey or directly observed collective belief.