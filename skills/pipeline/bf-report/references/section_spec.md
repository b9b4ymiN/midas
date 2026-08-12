# BF-Report Section Spec

The exact section-by-section content of a BF-Report, and which upstream step each part is drawn from. The document is numbered and anchored like a 10-K / 56-1: a reader can jump to any part from the TOC and knows where each topic lives. Fill `references/report_template.html` against this spec. Keep every figure dated and currency-labelled; lead with judgement, not raw numbers.

Section map (TOC order):

```
Cover / header
Executive Summary            ← investment-synthesis + company-valuation
1  Business & Narrative      ← business-narrative
   1.1 Business model & income structure
   1.2 Moat & competitive position
   1.3 Industry & TAM
   1.4 Growth & reinvestment quality
   1.5 Life-cycle stage & the 3-P verdict
2  Financial Dashboard       ← company-valuation (financial-health snapshot)
3  Valuation                 ← company-valuation
4  Earnings & Sentiment      ← earnings-recap + earnings-preview
5  Technical Timing          ← bf-tech-analysis
6  Scenarios & Investment Plan ← investment-synthesis
7  Key Risks                 ← investment-synthesis
Appendix                     ← all steps (assumptions, sources, methodology, disclaimer)
```

---

## Cover / header
Company name (serif h1) **preceded by the company logo** (embedded as `data:image/png;base64,...`, 64×64, white-padded, in a flex `.head-title` row), a "Equity Research · Not financial advice" pill, and a mono metadata line: ticker **with exchange suffix**, market, currency, and as-of date. Optionally a one-line business descriptor under the title.

**Logo source:** Thai SET → `https://media.set.or.th/common/logo/company/{SYMBOL}.png`; fetch, then embed base64 (never link remotely — the file must stay self-contained). US/other → company IR or favicon, embedded the same way.

## Executive Summary
The decision, up top, so a busy reader gets it in 15 seconds.
- **Key Investment Insight** (callout, before the KPI band): the one primary hook from `investment-synthesis`, written in plain language. It must explain why the stock is interesting now, with a number or mechanism translated into a comparison investors understand immediately (per share vs current price, % market cap, yield, payout, or fair-value gap). If no hook is clear, state "No clear investment hook identified."
- **Verdict band** (KPI band, 4–5 stat cards): choose cards that reinforce the key insight first, then blended fair value · current price · % upside/downside (color the delta) · conviction/stance lean · margin-of-safety required. Mark the most decision-relevant card `.warn`.
- **Thesis** (callout): the one-paragraph thesis from `investment-synthesis` — what you pay, what you get, what must be true, the asymmetry.
- One line pointing to where the supporting detail lives (e.g., "Valuation build in §3; scenarios in §5").

## 1 Business & Narrative  (from `business-narrative`)
This section renders the Narrative Brief in full — it is the story spine, so give it room. Five subsections, each its own anchor:

**1.1 Business model & income structure.** How the company makes money. A revenue-mix table (segment · % of revenue · margin) and a one-line read on where profit really concentrates. Optional: a simple inline-SVG donut or stacked bar for the mix.

**1.2 Moat & competitive position.** The signature subsection. Include:
- Moat type chips (network effects / switching costs / scale / brand / cost advantage / regulatory licence).
- The **moat meter** visual (design-system component): strength (none→narrow→wide) + durability arrow (widening↑ / stable→ / eroding↓).
- **ROIC−WACC spread as the quantitative proof** — the headline number plus a 5-yr sparkline; a wide, stable/widening positive spread *is* the evidence the moat is real and compounding.
- Evidence prose (pricing power, retention/churn, share stability) and the single biggest threat to the moat.

**1.3 Industry & TAM.** Structural tailwinds/headwinds, competitive structure (consolidating vs fragmenting), the TAM, and the company's share and its trajectory. Note any regulatory backdrop.

**1.4 Growth & reinvestment quality.** Where future growth comes from; whether reinvestment earns **above** WACC (the only growth that creates value); capex-vs-FCF read; whether growth is self-funded or relies on outside capital. Tie directly to §2 and §3.

**1.5 Life-cycle stage & the 3-P verdict.** A stage badge (young / growth / mature / decline / cyclical) and what it implies for which driver dominates. Then the **possible / plausible / probable** verdict (callout) and any "this time is different" flags, each with what the company would concretely have to do to earn the optimistic case.

## 2 Financial Dashboard  (from `company-valuation` snapshot)
The ~20-metric fact base in one dense, scannable block, organised by family: profitability · returns & capital efficiency · cash flow · leverage · valuation multiples · dividend/shareholder return. For **each** metric: latest value · a 5-yr **sparkline** · a one-line read · a judgement chip (good/watch/bad by direction & meaning, not sign). **Lead** the section with the diagnostics that carry the thesis in this specific case. If the Key Investment Insight is a look-through asset, net cash, capital return, or segment-value anomaly, show that diagnostic first in plain language and table form. If there is no special hook, default to ROIC−WACC spread, CapEx-vs-FCF, and the leverage trend. Include Piotroski / Altman as a gut-check row if available.

## 3 Valuation  (from `company-valuation`)
- **Headline:** blended fair value vs current, % up/downside (band or callout).
- **Three-method table:** method · implied price · weight · one-line rationale.
- **DCF build:** assumptions table (growth path, margins, WACC components, terminal method) + 5-yr FCFF projection + EV→equity bridge.
- **Sensitivity:** the 5×5 WACC × terminal-g **heatmap**, base case highlighted.
- **Relative:** peer table (P/E fwd, EV/Rev, EV/EBITDA, margin, growth; median row; flag the target's premium/discount).
- **SOTP:** only if 2+ distinct segments — segment table + per-segment multiple + corporate adjustments + implied equity; note any conglomerate discount.

## 4 Earnings & Sentiment  (from `earnings-recap` + `earnings-preview`)
- **Recap:** most recent quarter — actual vs estimate, surprise magnitude, and the stock's price reaction.
- **Preview:** next report — consensus EPS/revenue, the beat/miss track record (last 4 quarters table), analyst price targets, recommendation distribution.
- **Sentiment read:** is the stock priced for perfection or for pessimism, and does recent execution support or contradict the §3 valuation story?

## 5 Technical Timing  (from `bf-tech-analysis`)
- **TradingView chart image:** embed the chart image from `tradingview_chart_image` as a self-contained `data:image/png;base64,...` image. Do not link to an external image file. Caption it with symbol, exchange, interval, and capture date/time if available.
- **Top-down read:** weekly context first, then daily condition classification (waiting to break / pullback in uptrend / at support or possible bottom / broken downtrend awaiting pullback / downtrend intact or no clean setup).
- **Calibrated parameters:** respected MA(s), Fib anchors, ATR, typical pullback depth, and volume baseline.
- **Risk geometry:** entry zone, stop/invalidation, target(s), fair-value magnet, R-multiple, and whether the setup is high/mixed/low confluence.
- **Timing verdict:** enter now / stage on trigger / wait for specific event / avoid, tied explicitly to §3 valuation upside and §6 investment plan.

## 6 Scenarios & Investment Plan  (from `investment-synthesis`)
- **Scenario timeline table:** Bull / Base / Bear × (~12 / 24 / 36 mo) with the levers, implied return, and probability; show **expected value** below. Anchor every target to the §3 fair value and its drivers.
- **Investment plan** (conditional, never a buy/sell command): entry vs fair value & margin of safety · technical entry/stop from §5 · sizing & staging · conviction-builders (watch each quarter) · thesis-breakers (exit triggers, from the sensitivity grid and technical invalidation) · horizon. Name the **setup archetype** (quality compounder / deep-value / cyclical / GARP) and how it shapes the plan.

## 7 Key Risks  (from `investment-synthesis`)
The 3–5 assumptions that move the answer most, ranked by impact, each with direction and roughly how much of fair value is at stake. Map them to the §6 thesis-breakers, the most sensitive inputs in §3, and any key technical invalidation from §5.

## Appendix
- Full assumptions table (every valuation input + its source/rationale).
- **Data sources & dates** (filings, IR, market data; note yfinance is unofficial — cross-check primary filings).
- Methodology notes / glossary (optional).
- **Disclaimer:** research and educational output only; not financial advice. (Also keep a short disclaimer in the footer.)

---

## Thai Investor & Mobile Requirements

- For reports intended for Thai investors, write the report in **Thai** unless the user explicitly asks for English.
- Explain the Key Investment Insight in Thai plain language before using technical terms.
- Keep English finance terms only where they are common and useful (e.g., DCF, SOTP, WACC), and define them briefly when needed.
- The HTML must be responsive on mobile: KPI cards wrap, tables do not force page-level horizontal scrolling, Thai text does not clip, and the first viewport remains readable.
- For wide tables, wrap them in a scroll container or simplify columns on mobile.
- The TOC is **collapsible on mobile** (≤900px) and the toggle bar is **`position:fixed` at the very top**, so it stays reachable no matter how far the reader scrolls. It starts collapsed behind a hamburger toggle, drops down as an overlay (capped ~70vh, own internal scroll) when opened, and auto-collapses after the reader follows a link. `padding-top:64px` on the shell and `scroll-margin-top:64px` on sections keep content and jump-targets clear of the bar. On desktop it stays the always-open sticky rail. **Keep the template's `<script>` block verbatim** — it gates on `DOMContentLoaded`, wraps scrollspy and TOC-toggle in *separate* `try/catch` blocks (so one error can't break the other), uses event delegation for auto-collapse, and has been regression-tested. Do not refactor it back into paired IIFEs: an uncaught throw in the first IIFE silently prevents the second from binding, which leaves the mobile TOC permanently open and un-closable.

---

## Cross-referencing
Wherever the prose refers to another part, link it (e.g., `see <a href="#s3">§3 Valuation</a>`). This is what makes the document navigable like a filing. Confirm every TOC link and inline §-link resolves before presenting.
