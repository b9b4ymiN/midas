---
name: report-storytelling
description: >
  Prepare a source-faithful, beginner-investor-friendly, fully explained research report
  BEFORE bf-report renders the HTML. Use automatically in both-stock-analysis AFTER
  investment-synthesis and BEFORE bf-report; also use standalone when the user provides
  an existing research report or article and asks for a clearer, complete reader edition.
  Audit material numbers and provenance, rewrite dense explanations, plan evidence-led charts,
  and produce a report-ready content pack. Do not recalculate valuation, invent a thesis,
  change investment decisions, or render HTML. For Thai investing reports, assume the reader
  knows P/E, EPS, D/E and dividends but needs WACC, ROIC, FCFF and DCF explained.
---

# Report Storytelling — Editorial Gate Before BF-Report

**Role:** faithful research editor, fact-consistency checker, financial educator, and evidence-led visual storyteller. **Not** an equity analyst, independent valuation engine, investment-synthesis replacement, or HTML renderer.

## Boundary

1. `investment-synthesis` **owns the thesis and conditional investment plan**.
2. `company-valuation` **owns valuation methods, inputs, formulas and prices**.
3. `report-storytelling` **owns the reading experience**, first-use explanations, claim traceability, chart *specifications*, and the editorial integrity gate.
4. `bf-report` **owns HTML/CSS/SVG rendering and mobile/print behavior**.
5. `stock-grill` **owns adversarial verification of the rendered report**; R0 runs on the HTML, not on remembered prose.

**Never silently change:** numbers, calculation bases, periods, sources, probabilities, prices, implied returns, thesis direction, recommendations, uncertainty or disclaimers. Reordering, unpacking abbreviations and adding faithful worked examples are allowed. On material conflict, route to the owning upstream skill and block final publication until resolved; do not improvise a repair.

**Disclosure:** Research and educational output only. Not financial advice. Preserve the original disclaimer in the report and appendix.

## When and how to invoke

**Pipeline, default:** `both-stock-analysis` invokes after Step 5 (`investment-synthesis`) and before Step 6 (`bf-report`). The skill reads the research outputs from Steps 2–5, including the underlying quantitative outputs, not merely the 1-paragraph synthesis. Preserve the shared `har-to-api` as-of snapshot. No duplicate data fetch by default.

**Standalone:** for an existing HTML/Markdown/PDF/article, read the complete source and its original citations. The output is an edited content pack and audit, **not** an independently re-valued company. If primary source access is unavailable, label key claims `SOURCE_ONLY` or `UNVERIFIED` instead of pretending they were independently checked. Keep any original analysis clearly attributed. Use the general audience rules when the topic is not investing.

## Input contract

Required for full Midas invocation:
- `source_id`, ticker/exchange, source as-of date/time, currency, language, and shared snapshot location.
- The complete business narrative and industry/reinvestment/moat findings.
- Financial-health time series and valuation **with source definitions**, WACC, DCF/relative/SOTP tables, scenarios and sensitivity matrix.
- Earnings actual/consensus, source dates, technical timing and chart metadata.
- The completed Investment Synthesis: key insight, thesis, scenario probabilities, risks and conditional plan.
- Source citations/references and available unresolved data-quality flags.

If an input is missing, **record the gap**; do not fill it by guesswork. Preserve the known sections and block finalization only when the absence prevents a consequential claim from being supported.

## Procedure

### 1. Ingest and preserve

Read **all** upstream sections. Build section-to-source crosswalk and a claim ledger with for each material number: `claim_id`, owning step, source, as-of date, period, unit, reporting basis, fact/derivation/assumption category, and verification state. Distinguish company statement, market quote, consensus estimate and analyst model. Maintain complete scope, including risks, dissenting evidence, technical timing, appendices and methodology.

### 2. Editorial integrity gate (before rewriting)

Read `references/evidence-and-integrity.md`. Recompute mechanical arithmetic where feasible: YoY, QoQ, percentage-point changes, scenario probability sums, weighted fair values/returns, formula bridges. Compare definitions before comparing magnitudes: reported vs core; IFRS vs non-IFRS; quarterly vs half-year; gross vs net debt; lease included/excluded; FCFF vs FCF/equity; source quote vs forecast. Do not characterize independent source verification unless an actual primary document was inspected.

For each mismatch: create an Issue with severity, exact conflicting claims, the computation/source, owning upstream skill, and suggested rework. **BLOCKER** issues (material numeric, source, or methodology conflicts) stop handoff to BF-Report; rerun only the relevant upstream step and repeat integrity checks. Noncritical discrepancies remain disclosed.

### 3. Reader-first rewrite, full coverage

Read `references/audience-and-prose.md`. Default `beginner-investor` audience: understands P/E, EPS, D/E, dividends and ordinary financial statements, but **does not** assume working knowledge of WACC, ROIC, ROIC-vs-WACC, FCFF, reverse DCF, terminal value, lease accounting and SOTP. Expand the first occurrence of complex terms with (1) the business question, (2) a tiny accurate worked example, (3) the actual report numbers and bases, (4) what this metric cannot establish. Respect the reader; do not use childlike analogies.

Write a **complete** chapter-ready `report-ready.md` in the source language (Thai for Thai-market reports unless the user requests otherwise). Use clear, evidence-supported action headings; natural explanatory paragraphs; chart/table context; and explicit transitions. **Do not replace reasoning with arrows or acronym chains** in prose. Keep tables, forecasts, assumptions, sources, material uncertainties and caveats, even when reorganizing sections. Maintain the upstream source crosswalk. Preserve original thesis content verbatim in meaning, even if readability improves.

### 4. Visual evidence plan

Read `references/visual-storytelling.md`. For each proposed figure create an exhibit spec: question, takeaway-title, series/claims, date/unit/basis, visual form, annotation, source and a textual/tabular fallback. Use **only** actual sourced or clearly marked hypothetical data. For missing/incomparable data, use explanation rather than manufactured charts. Use no images/diagrams merely to decorate. `bf-report` renders approved specs in its own house style.

### 5. Export and validate pack

Read `references/content-pack-contract.md`. Output all three files alongside the stock's other research artifacts:

- `report-storytelling/report-ready.md`: complete rewritten body, ready to map into BF-Report sections.
- `report-storytelling/report-manifest.json`: source and section crosswalk, claim IDs, issues, reproducible arithmetic checks, chart specs and data provenance.
- `report-storytelling/evidence-review.md`: explicit verification, blocked corrections, trade-offs and what remains uncertain.

Run `python scripts/validate_pack.py <path-to-report-manifest.json>` (path relative to this installed skill's folder for the script). A nonzero exit blocks the BF-Report handoff; do not override it by claiming a pass. The validator checks **document structure and declared arithmetic**, not independent financial correctness or factual truth; primary-source and editorial review are still required.

### 6. Handoff to BF-Report, then Stock Grill

Send the **validated content pack plus original immutable upstream outputs** to BF-Report. BF-Report is forbidden to silently override the pack, invent numbers, or omit source/caveat maps. Its numbered section map, design tokens and navigation remain the same. Render only approved charts and maintain visible disclosures for model outputs. Mark the HTML as **DRAFT** until Stock Grill R0 has passed; then run R1–R5 per `stock-grill` (the user may decline the interactive rounds). Do not call a report fully stress-tested before those rounds actually complete.

## Definition of Done

- All material original sections and claims have an explicit source crosswalk; no important risk disappears.
- No unresolved material BLOCKER, unknown source of a consequential figure, or unverified arithmetic presented as settled.
- Finance definitions, units, time periods and reporting bases are comparable or plainly distinguished.
- The reader can explain *what, why it matters, and what cannot be concluded* for each difficult concept.
- Arrow chains have been rewritten into comprehensible prose; no claim of causal certainty from mere correlation.
- Each evidence exhibit has traceable numbers, takeaway, caveat and text/table fallback.
- Full body text exists; no compressed executive summary substituted for a complete report.
- BF-Report remains the single HTML renderer; Stock Grill remains the independent challenger.

## References (read on demand)

- `references/evidence-and-integrity.md` — proof hierarchy, issue severity, numerical reconciliation and escalation.
- `references/audience-and-prose.md` — beginner investor profile and complete-document editorial rules.
- `references/visual-storytelling.md` — chart selection, exhibit contract and responsive accessibility.
- `references/content-pack-contract.md` — manifest schema, handoff and validator boundaries.
- `examples/mint-mismatch.md` — historical MINT teaching fixture; **do not** treat as live market data.

**Prior art:** [DreambigOu/ELI5](https://github.com/DreambigOu/ELI5) for audience calibration; [consulting-problem-solving](https://github.com/wudpeker/consulting-problem-solving) vertical reports for evidence-led prose; publicly available McKinsey charts for communication *inspiration*, not an official McKinsey-branded method.