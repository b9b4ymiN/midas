# Pipeline Contract v2

## Canonical handoff order

`company_request` → `business_identity_pack` → `market_growth_pack` → `economic_engine_pack` → `reinvestment_runway_pack` → `compounder_thesis_pack` → `bf_report`

Every pack MUST carry the same `evidence_ledger`, appended rather than replaced. Use `schema_version: future-compounder-v2.2` in serialized handoffs where a version field is available.

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
- `current_return_structure`
- `intangible_capital`
- `scale_economics`
- `look_through_earnings`, `associate_cash_bridge`, and `return_bases` — required
  when share of associate profit exceeds 25% of net profit or long-term
  investments exceed 30% of total assets; `NOT_APPLICABLE` otherwise
- `per_share_economics`
- `economic_inflections`
- `evidence_ledger`
- `data_gaps`
- `unresolved_questions`

Gate: the pack must explain the economic unit, causal growth bridge, corporate translation, and per-share owner effect, or mark the missing link `UNRESOLVED`.

## `reinvestment_runway_pack`

Required fields:
- `historical_reinvestment`
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
- `compounding_potential`
- `evidence_maturity`
- `confidence`
- `evidence_ledger`

Gate: the thesis pack must include an inside view, outside-view/base-rate challenge, evidence maturity explanation, reverse business-reality check, and counter-thesis. A bull-only pack fails.

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
