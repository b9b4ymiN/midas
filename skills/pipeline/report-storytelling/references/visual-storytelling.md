# Evidence-led visualization and long-form storytelling

Use McKinsey-like communication principles as a *publicly known inspiration*: message-driven headlines, one reading question per graphic, unobtrusive labels, proof near the assertion. Do **not** represent any result as produced by or endorsed by McKinsey, and do not reproduce proprietary graphics.

## Selection matrix

| Question the reader asks | Preferred graphic | Critical guardrail |
|---|---|---|
| How do two directly comparable magnitudes differ? | Bar / dot plot | Same units/time basis; bars usually start at zero |
| What direction did a metric take over time? | Line | Ordered dates and real observations; avoid connecting missing periods as fact |
| What explains the change between two numbers? | Waterfall | Components must sum exactly to the reported bridge |
| Where does revenue/profit come from? | Stacked bar | Same consolidation perimeter and denominator; totals sum |
| How is the business or financial mechanic arranged? | Labeled relationship diagram | Arrow must reflect real causal/contractual flow, not insinuation |
| How sensitive is value to WACC and perpetual growth? | Sensitivity heatmap | Clearly mark estimates and conditional assumptions, not price observations |
| What are the conditional future scenarios? | Comparison chart plus table | Bull/Base/Bear are model scenarios, never probabilities established by observation |
| Are two definitions actually comparable? | Explanation/table, not chart | Refuse to compare incompatible accounting bases visually |

## Exhibit contract

Before any graphics are made, record:

- `id`, `question`, `takeaway_title`: complete, supported proposition, not "Financials".
- `chart_type`, `classification` (`OBSERVED`, `DERIVED`, `MODEL`, `ILLUSTRATION`).
- `unit`, `period`, source claim IDs, values with category/date labels (no invented points).
- `basis` and any relevant adjustments, e.g. "net debt excluding lease liabilities".
- `annotation`, `source_note`, `text_fallback` and `table_fallback` where complex.

All charts are authored in the BF-Report design system and must be accessible to Thai-language readers on small screens. A visually striking chart with invalid comparisons fails the editorial gate.

## Visual acceptance

1. Takeaway title and caption state the same careful claim; no misleading causal implications.
2. No invented missing values, time series, data-source URLs or confidence intervals.
3. No mixed positive/negative/fiscal-basis axes without explanation.
4. Every substantive chart has data provenance and can be understood in text-only form.
5. Chart is responsive; headings/labels do not clip or push the entire page horizontally.
6. Figure label distinguishes official numbers from model estimates and illustrative examples.

Prefer a small, legible table to an elaborate diagram if the diagram needs unproven links. Never force a chart quota.