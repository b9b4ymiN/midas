# BF-Report

Turn a finished equity analysis into a single self-contained, **filing-grade** HTML document — structured like a 10-K / 56-1, with a sticky linked table of contents and numbered, anchored sections — instead of a slide deck.

## What it does

- Renders completed analysis into one continuous, navigable document (no build, no dependencies)
- Sticky linked Table of Contents + numbered, anchored, cross-referenced sections
- Sober editorial house style: serif headings, sans body, mono labels; colour encodes judgement (good/watch/bad), not decoration
- Dense tables, KPI/verdict band, 5-yr sparklines, a WACC×g sensitivity heatmap, and a signature **moat meter** backed by the ROIC−WACC spread
- Print-ready (A4/Letter) and responsive (TOC collapses on mobile)

## Document structure

Cover → Executive Summary → 1 Business & Narrative (1.1 model & income structure · 1.2 moat & competitive position · 1.3 industry & TAM · 1.4 growth & reinvestment · 1.5 life cycle & 3-P verdict) → 2 Financial Dashboard → 3 Valuation → 4 Earnings & Sentiment → 5 Scenarios & Investment Plan → 6 Key Risks → Appendix.

## Triggers

`BF-Report`, `a research report / write-up / memo (not slides)`, `professional HTML report`, `10-K or 56-1 style document`, `turn this analysis into a document`, `equity research document`. Also runs as the final step of `both-stock-analysis` (in place of slides).

## Prerequisites

This is a renderer. It needs the upstream outputs: a business narrative (`business-narrative`), a valuation with snapshot + sensitivity + Bull/Base/Bear (`company-valuation`), an earnings/sentiment read (`earnings-recap` + `earnings-preview`), and a synthesis (`investment-synthesis`). If run standalone without these, it asks for or produces them first.

## Output

A single self-contained `.html` file written via bash heredoc and presented for download.

## Reference Files

- `references/design_system.md` — Tokens, typography, layout + sticky TOC, components, print CSS
- `references/section_spec.md` — Section-by-section content and the upstream-step → section mapping
- `references/report_template.html` — Fillable, self-contained scaffold (copy, then fill)

## Disclaimer

For research and educational purposes only. Not financial advice.
