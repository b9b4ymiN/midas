# Pipeline Contract v2

## Canonical handoff order

`company_request` → `business_identity_pack` → `market_growth_pack` → `economic_engine_pack` → `reinvestment_runway_pack` → `compounder_thesis_pack` → `bf_report`

Each pack MUST carry **every entry from the preceding packs plus the entries its own layer produced**. The ledger only ever grows; an entry is never removed or rewritten, and the entry count may not fall between layers. Each entry carries `origin_layer` naming the pack that first recorded it, so the audit trail shows which layer produced which evidence. Copying an identical ledger into all five packs satisfies the letter of "same ledger" and destroys that trail — it is not compliant. Use `schema_version: future-compounder-v2.2` in serialized handoffs where a version field is available.

Packs are serialized to `run/<TICKER>-<YYYY-MM-DD>/<pack_name>.json` as each
layer completes, and checked with `future-compounder/scripts/validate_pack.py`
before the next layer starts. The field lists below are what that script
enforces — they are a gate, not a suggestion.

## Shared status semantics

Use explicit states instead of fabricated precision:
- `RESOLVED`
- `PARTIALLY_RESOLVED`
- `UNRESOLVED`
- `NOT_APPLICABLE`

A critical `UNRESOLVED` field is forwarded as a data gap and must reduce downstream certainty when it affects the thesis. It is never converted into a neutral score or silently filled with an assumption.

## Company request

Required when available:
- legal/company name
- ticker and exchange
- analysis date / point-in-time cutoff
- requested scope
- known source set

If identity is ambiguous, resolve before research.


## `business_identity_pack` — Layer 0 framing gate

Required fields:
- `product_definition`
- `current_economic_business`
- `customer_jobs`
- `core_capabilities`
- `strategic_direction`
- `market_scope_portfolio` with `proven`, `emerging`, `option`, `narrative` arenas
- every arena also carries `arena_relationship`: `CORE_EXTENSION`, `CORE_COMPLEMENT`, `ADJACENT_STANDALONE`, `ENABLING_INFRASTRUCTURE`, or `UNRESOLVED`
- `identity_transition`
- `scope_stress_test` with `too_narrow`, `candidate`, `too_broad`, and downstream impact
- `structural_analogues` with transfer limits
- `main_alternative_frame`
- `scope_confidence`
- `framing_risks`
- `critical_unknowns`
- `disconfirming_evidence`
- `evidence_ledger`

Gate: the pack must separate current economics from strategic aspiration, stage each arena by evidence maturity, avoid claiming profit pools not economically captured, and state both too-narrow and too-broad frames. Potential market size cannot upgrade evidence class.

Downstream research may emit `SCOPE_CHALLENGE` when new evidence changes the customer job, economic arena, capability transfer, arena relationship, or evidence class. The master reruns Layer 0; downstream skills must not silently overwrite the frame.

## `market_growth_pack` — Layer 1 external-growth gate

Required fields:
- `scope_frame_used`
- `scope_challenges`
- `metric_comparability`, including `adjusted_profit_reconciliation` whenever
  the company promotes a profit measure of its own definition. States
  `RECONCILED`, `PARTIALLY_RECONCILED`, or `UNRECONCILED`, the residual, and
  the items accounted for. An `UNRECONCILED` adjusted figure may not be used
  downstream as a growth base or as a ratio denominator.
- `demand_evidence_basis`
- `demand_category_evolution`
- `industry_profit_pool`
- `competitive_system`
- `growth_decomposition`
- `customer_channel_incrementality`
- `expansion_incrementality`
- `international_replication`
- `management_growth_execution`
- `evidence_trajectory`
- `external_growth_runway`
- `counter_evidence`
- `evidence_ledger`
- `data_gaps`
- `unresolved_questions`

Gate: the pack must explain category/demand regime, value capture when material, the causal mechanism behind share gain/loss, strategic and operating growth attribution without double counting, material channel/geographic/expansion incrementality, and the demand-evidence basis when sell-in can diverge from sell-through. Trend claims must pass the Metric Comparability Gate. A large TAM, low share, channel GMV increase, or foreign store/capacity count cannot substitute for evidence.

If external research contradicts Layer 0, emit `SCOPE_CHALLENGE`; do not silently overwrite `business_identity_pack`. Full unit returns, ROIIC, per-share economics, capital allocation, and final compounder quality remain downstream.

## `economic_engine_pack`

Required fields:
- `company_context`
- `business_model`
- `economic_units`
- `unit_economics`
- `micro_to_corporate_bridge`
- `economic_drivers`
- `growth_architecture`
- `life_cycle_stage` — the Dickinson cash-flow-pattern reading, classified on
  investing cash flow excluding securities flows, with the unadjusted
  classification beside it and a note wherever the two differ. `UNRESOLVED`
  where a cash flow section is unavailable; never inferred from sector or age.
- `current_return_structure`
- `intangible_capital`
- `scale_economics`
- `look_through_earnings`, `associate_cash_bridge`, and `return_bases` — required
  when share of associate profit exceeds 25% of net profit, long-term
  investments exceed 30% of total assets, or minority interest exceeds 20%
  of total equity; `NOT_APPLICABLE` otherwise
- `sector_return_metrics` — required when the company is an insurer or a bank
  (`statement_template` of `insurance`/`bank`, or policy liabilities / a
  deposit-funded loan book on the balance sheet). Carries the replacement
  measures — NBV, CSM movement, embedded value and solvency for a life
  insurer; NIM, cost/income, NPL and CET1 for a bank — each valued or
  `UNRESOLVED`. ROIC, ROCE, FCF, P/FCF and EV/EBITDA may not carry a return
  or valuation conclusion for these models. `NOT_APPLICABLE` otherwise
- `per_share_economics`
- `economic_inflections`
- `evidence_ledger`
- `data_gaps`
- `unresolved_questions`

Gate: the pack must explain the economic unit, causal growth bridge, corporate translation, and per-share owner effect, or mark the missing link `UNRESOLVED`.

## `reinvestment_runway_pack`

Required fields:
- `historical_reinvestment`
- `mandatory_measures`
- `incremental_return`
- `capital_allocation`
- `acquisition_economics`
- `reinvestment_capacity`
- `opportunity_set`
- `runway`
- `duration`
- `moat_outcomes`
- `capital_constraints`
- `financial_resilience`
- `emerging_indicators`
- `evidence_maturity`
- `evidence_ledger`
- `counter_evidence`
- `data_gaps`

`mandatory_measures` carries the four numbers as data rather than prose, so the
basis of a verdict can be checked rather than taken on trust:

```
"mandatory_measures": {
  "path": "standard | emerging_bridge | sector_specific",
  "window_years": 4,
  "basis": "(net capex + change in working capital) / NOPAT",
  "reinvestment_rate": {
    "cumulative": 0.326,
    "annual": {"FY2022": 0.312, "FY2023": 0.390, "FY2024": 0.362, "FY2025": 0.251}
  },
  "incremental_return": 0.32,
  "growth_from_new_investment": 0.099,
  "growth_from_rising_returns": 0.007,
  "pricing_power_tiers_passed": 2
}
```

On the `standard` path the window must be **at least three years** and the annual
series is required — a cumulative figure alone conceals the trend, which is
usually the more decision-relevant number. Free cash flow may never be named as
the denominator of the reinvestment rate; it is already net of the capital spend
being measured.

`emerging_bridge` is the path for a company with less than three years of history
or immature returns. It carries the bridge inputs instead of a measured series and
is not penalised for the short window — short history lowers Evidence Maturity,
never Potential.

`sector_specific` is the path where the standard measures do not apply at all.
For a bank or insurer the pair becomes return on equity attributable to owners
multiplied by the retention ratio, bounded by the regulatory capital or solvency
position; for a life insurer the movement in contractual service margin and the
operating return on embedded value stand in for the reinvestment leg. State which
substitution was made.

Gate: Return, reinvestment amount, allocator behavior, financeability, and Duration must each be resolved to the level evidence permits. A large market TAM cannot substitute for financeable runway.

## `compounder_thesis_pack`

Required fields:
- `external_growth_view`
- `category_profit_pool_view`
- `competitive_share_view`
- `growth_decomposition_view`
- `channel_international_view`
- `growth_execution_view`
- `compounding_engine`
- `return_view`
- `reinvestment_view`
- `duration_view`
- `per_share_view`
- `scale_economics_view`
- `financial_resilience_view`
- `base_rate_context`
- `evidence_ladder`
- `reverse_reality_check`
- `supporting_evidence`
- `counter_evidence`
- `critical_unknowns`
- `kill_conditions`
- `upgrade_conditions`
- `leg_ratings`
- `binding_leg`
- `hurdle_used`
- `durable_growth`
- `compounding_potential`
- `potential_qualifier`
- `compounder_class`
- `evidence_maturity`
- `confidence`
- `evidence_ledger`

`leg_ratings` rates each leg on its own, so a divergence cannot hide inside a single
label. Five legs take the Potential vocabulary (`Exceptional`/`Strong`/`Moderate`/
`Weak`/`Broken`/`UNRESOLVED`); capital allocation keeps the vocabulary already
defined for it:

```
"leg_ratings": {
  "incremental_return":     "Strong",
  "reinvestment_capacity":  "Moderate",
  "duration":               "Strong",
  "per_share_translation":  "Strong",
  "financial_resilience":   "Strong",
  "capital_allocation":     "VALUE_CREATING | MIXED | VALUE_DESTRUCTIVE | UNRESOLVED"
},
"binding_leg": "reinvestment_capacity",
"potential_qualifier": "runway-capped",
"compounder_class": "Proven Compounder | Emerging Candidate
                     | Great Business, Narrow Runway | Not a Compounder"
```

`hurdle_used` records the two lines the verdict was judged against and their basis,
so the grading can be reconstructed: `{"value_destruction": 0.075, "attractive":
0.15, "basis": "..."}`.

`durable_growth` carries the growth figure the label was read from, with its window
and its components — **and both a nominal and a real figure**:

```
"durable_growth": {
  "nominal": 0.099,
  "real": 0.074,
  "inflation_basis": {
    "rate": 0.025,
    "source": "revenue-weighted across countries of operation: 82% US, 18% international",
    "as_of": "2026"
  },
  "window": "...", "components": {...}
}
```

The band table is built on **real** growth rates, so the comparison must be made on
the real figure. Comparing a nominal growth rate against a real base rate flatters
every company by the rate of inflation — two to three points against a median near
4.5%, enough to move a verdict two bands. Deflate by the inflation of the countries
the company **operates in**, revenue-weighted, and record the rate used. Where the
rate cannot be established, say so and mark the comparison `PARTIALLY_RESOLVED`
rather than silently comparing nominal against real.

`upgrade_conditions` is the counterpart of `kill_conditions` and is equally required.
Each entry must be observable in a future filing or result — a metric, a direction,
and a threshold — not a hoped-for change of narrative. A thesis with only downside
triggers cannot be re-rated upward on evidence and will drift.

`reverse_reality_check` carries the comparison as data, not a bare label. A word
on its own says nothing about how far away the path is, which is the only thing
the check exists to establish:

```
"reverse_reality_check": {
  "anchor": "operational — revenue, units, customers, capacity or share",
  "anchor_basis": "what the multiple was applied to, and its current value",
  "horizon_years": 10,
  "horizon_justification": "tied to the Duration evidence, not adopted by habit",
  "required_cagr": 0.26,
  "comparisons": {
    "achieved": 0.132,
    "engine_can_fund": 0.099,
    "reference_class": "100x needed ~20-26%/yr for 17-25 years"
  },
  "what_is_supported": "3-4x over the same horizon follows from durable growth",
  "state": "PLAUSIBLE | STRETCHED | IMPLAUSIBLE | UNRESOLVED"
}
```

A market-capitalisation anchor is optional and secondary; where used it states its
multiple assumption on the same line and never appears without the operational
path beside it.

`compounder_class` is a categorical reading that survives changes in the label.
`Great Business, Narrow Runway` is the case of high returns on capital the business
cannot absorb — excellent economics, limited compounding — and must not be recorded
as `Proven Compounder`.

Gate: the thesis pack must include an inside view, outside-view/base-rate challenge, evidence maturity explanation, reverse business-reality check, and counter-thesis. A bull-only pack fails. A pack whose `compounding_potential` exceeds `Moderate` while any leg in `leg_ratings` is `UNRESOLVED` fails.

## `bf_report`

Consumes the relevant upstream packs (`business_identity_pack`, `market_growth_pack`, `economic_engine_pack`, `reinvestment_runway_pack`, and `compounder_thesis_pack`) rather than relying on the thesis pack alone.

Must preserve source lineage for every major claim and visibly separate FACT, DERIVED, MANAGEMENT_CLAIM, MARKET_EXPECTATION, ASSUMPTION, ESTIMATE, INFERENCE, and UNVERIFIED statements. It must surface unresolved gaps rather than smooth them away.

## Scope boundary

Core v2 explicitly excludes:
- DCF / fair value / target price
- technical analysis / entry-exit signals
- portfolio sizing
- holding / quarterly monitoring dashboard
- mechanical 100-point scoring
- mechanical probability of “100x”

The Reverse Reality Check may use current scale or market capitalization as a **scenario anchor** but does not infer fair value or a target price.
