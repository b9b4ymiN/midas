# Report-ready content pack v1.0 — contract

Deliver three companion files in a `report-storytelling/` folder next to the ticker's research work:

- **`report-ready.md`**: complete reader-edited sections, tables, original caveats and sources. This is narrative content for BF-Report, **not HTML**.
- **`report-manifest.json`**: audit and mapping described below. A JSON file allows simple deterministic validation and traceability without parsing finance numbers from prose.
- **`evidence-review.md`**: verification summary, evidence reviewed, material issues, unresolved ambiguities, and suggested upstream fixes. It is **not** a substitute for original filings.

## `report-manifest.json`

Top-level keys:

- `schema_version`: `"1.0"`.
- `report_id`, `ticker`, `as_of`, `language`, `audience`, `upstream_snapshot` (path or stable identifier, not a fabricated URL).
- `source_sections`: ordered array of original section identifiers including executive summary and appendix.
- `sections`: each `{ "id", "source_ids": [...], "content_heading", "completeness": "COMPLETE" }`; sections can be reordered/merged but every `source_sections` ID must remain covered.
- `claims`: each `{ "id", "source_step", "source_ref", "period", "unit", "basis", "classification", "verification", "value" }`. `value` is numeric when applicable. May include description/source URL if available; don't make one up.
- `issues`: each `{ "id", "severity": "BLOCKER|MAJOR|MINOR", "status": "OPEN|RESOLVED|ACCEPTED_WITH_DISCLOSURE", "owner", "claim_ids": [...], "explanation", "suggested_action", "evidence_refs": [...] }`.
- `checks`: each `{ "id", "kind", "inputs", "expected", "tolerance" }` with supported kinds `pct_change`, `difference`, `spread_pp`, `weighted_sum`, `sum`; see script documentation.
- `visuals`: each `{ "id", "question", "takeaway_title", "chart_type", "classification", "unit", "period", "basis", "source_claim_ids": [...], "data": [{"label","value", "claim_id"}], "source_note", "text_fallback" }`.
- `disclaimer`: contains "Not financial advice".

**Warning:** Do not generate manifest claims *from invented final prose*. The manifest is created from the *upstream facts* before the rewrite. Every important number in the polished document should be traceable to a claim ID, but the included validator cannot prove that a writer did this exhaustively. Manual/AI QA remains necessary.

## Check semantics

- `pct_change`: inputs `{ "previous": 2768, "current": 2350 }`; expected percentage, e.g. `-15.101156`.
- `difference`: inputs `{ "a": 1.10, "b": 0.86 }`; expected `a-b` in the **same input unit** (e.g. 0.24 times).
- `spread_pp`: inputs `{ "a": 9.96, "b": 9.5 }`; expected `a-b` in **percentage points**; do not apply this name to leverage ratios.
- `weighted_sum`: inputs `{ "values": [...], "weights": [...] }`; expected sum of weight*value, weights must total 1 (tolerance 0.00001).
- `sum`: inputs `{ "values": [...] }`; expected arithmetic sum.

All check values and weights must be finite numbers. JSON booleans are not valid numbers.

## Handoff and refusal

- Run the validator and record exit status. A `BLOCKER` in any non-`RESOLVED` state refuses final handoff; a check mismatch also refuses handoff.
- A completed editorial `content pack` is not itself a verified equity analysis. The reader-ready manuscript must still undergo primary-source review and subsequent HTML R0/R1–R5 checks.
- If user requests only a standalone reader edition of historical content, the pack may be produced with disclosed blockers as **DRAFT** for educational use; do not declare it validated or publish it as final.
- BF-Report should keep independent original upstream data available when rendering and must not overwrite its financial figures from editorial guesses.

## Export example

See `examples/minimal-report-manifest.json` for structural behavior. It is a fictional fixture, **not current MINT market data**.