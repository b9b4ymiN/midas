---
name: both-stock-analysis
description: >
  End-to-end equity research workflow that analyzes a stock the way Aswath Damodaran
  would — bridging the business narrative to the numbers — and ends with a filing-grade
  HTML research document. Use this skill WHENEVER the user gives a stock ticker or company name
  and wants the full picture: "analyze AAPL for me", "full stock analysis", "deep dive on
  NVDA", "build an investment thesis", "should I invest in PTT", "research CPALL and write
  me a report", or any request that combines valuation + earnings + an investment plan + a
  written report.
  This skill orchestrates seven sub-skills in sequence: business-narrative, company-valuation,
  earnings-preview, earnings-recap, bf-tech-analysis, investment-synthesis, and bf-report. ALWAYS confirm
  the market first (Thai / US / other)
  so the correct exchange suffix, currency, and country-risk parameters are used. Prefer
  this over running the individual finance skills separately whenever the user wants the
  complete analysis or a finished report as the deliverable.
---

# Both Stock Analysis

A full-stack equity research pipeline. You are the analyst, working **in the spirit of Aswath Damodaran**: every valuation is a bridge between a *story* about the business and the *numbers* that story implies. You are rigorous, intellectually honest about uncertainty, allergic to hype with no cash flows behind it, and you always tie value back to four drivers — **cash flows, growth, reinvestment efficiency, and risk (cost of capital).**

The pipeline runs in six steps plus a technical-timing step and finishes by producing a written report. It chains seven installed sub-skills:

| Step | Sub-skill used | Purpose |
|---|---|---|
| 1 | — | Confirm market, set country/currency parameters |
| 2 | `business-narrative` | Damodaran story research → story-to-numbers map |
| 3 | `company-valuation` | Financial health snapshot (~20 metrics, 5-yr trends + reads) → DCF + relative + SOTP → intrinsic value + candidate investment hooks |
| 4 | `earnings-preview` + `earnings-recap` | Setup, track record, sentiment |
| 4.5 | `bf-tech-analysis` | TradingView chart image + top-down technical timing, entry zone, stop, target, R |
| 5 | `investment-synthesis` | Select the key investment insight → thesis, 1–3 yr scenarios + investment plan |
| 6 | `bf-report` | Filing-grade HTML research document (10-K / 56-1 style), insight-first and mobile-responsive |

> **Dependencies:** This skill assumes `business-narrative`, `company-valuation`, `earnings-preview`, `earnings-recap`, `bf-tech-analysis`, `investment-synthesis`, and `bf-report` are installed. If one is missing, tell the user which `.skill` to install before continuing.

> **Disclaimer:** Research and educational output only. **Not financial advice.** Carry this disclaimer into the final document (appendix + footer). yfinance data is unofficial — cross-check decisions against primary filings.

---

## Investment Hook Discipline (applies to every run)

This pipeline must be **insight-first, not checklist-first**. A complete valuation that hides the reason the stock is interesting has failed the user.

Before writing the thesis or report, identify the **Key Investment Insight**: the single most important reason this stock may be interesting *at today's price*. It must satisfy these rules:

1. Explain it in plain language in 3–5 lines, so a non-specialist investor can understand it.
2. Back it with a concrete number or mechanism.
3. Translate the number into a unit investors can compare immediately with the current share price, market cap, enterprise value, yield, or payout.
4. Choose one primary hook. Keep secondary hooks subordinate.
5. If there is no clear edge, say so plainly: "No clear investment hook identified." Do not invent one.

Examples of possible hooks include: a look-through asset value exceeding the parent market price; net cash covering a large share of market cap; one segment worth more than the whole company; ROIC far above WACC while P/B is below 1; sustainable dividend/buyback yield that the market underprices; a trough-earnings valuation mistake; or a governance/capital-allocation catalyst.

**Suzuki example (pattern, not a rule):** Suzuki Motor (`7269.T`) holds roughly 58.5% of Maruti Suzuki India. In that case, the important hook was not merely "SOTP upside"; it was that Maruti's look-through value was about ¥2,080 per Suzuki share versus a Suzuki share price around ¥1,866. The report needed to show that plainly: the listed stake alone was worth more than the parent share price, before valuing the rest of Suzuki.

## Step 1: Confirm the Market (do this FIRST)

A ticker alone is ambiguous — the same symbol can trade on different exchanges, and the valuation math (risk-free rate, currency, country risk premium) depends on *where* the company lives. So before any analysis:

**Ask the user which market the stock is in.** If a structured-question UI is available, present buttons; otherwise ask plainly:

> "Which market is this stock in? **Thai (SET)** / **US** / **Other** (tell me which exchange)."

Skip the question only if the user already stated the market or the symbol is unambiguous (e.g., a `.BK` suffix → Thai, a clearly US mega-cap the user named with "NASDAQ"). When in doubt, ask — guessing the exchange corrupts every downstream number.

Once you know the market, fix these parameters and pass them into every later step. Full lookup table (exchange suffixes, currencies, risk-free proxies, country risk premiums) is in **`references/markets.md`** — read it now.

Quick anchors:

| Market | yfinance suffix | Currency | Risk-free proxy | Country risk premium add-on |
|---|---|---|---|---|
| Thai (SET) | `.BK` (e.g., `PTT.BK`, `CPALL.BK`, `AOT.BK`) | THB | Thai 10Y government bond | ~+0.9% over mature-market ERP |
| US | none (e.g., `AAPL`) | USD | 10Y UST (live) | 0 (base market) |
| Other | varies — see `references/markets.md` | local | local 10Y sovereign | per Damodaran country table |

Resolve the company name → correct suffixed ticker before proceeding (e.g., "Airports of Thailand" → `AOT.BK`). Confirm the resolved ticker and currency back to the user in one line.

**Output language:** Match the user's language. For Thai stocks, offer the report in Thai or English.

---

## Step 2: Build the Business Story — use `business-narrative`

Before touching valuation, understand what you are valuing. Read and follow the **`business-narrative`** skill end-to-end. It researches current filings/IR (not stale memory), builds the four story pillars (income structure, business model & moat, industry & TAM, growth & reinvestment quality), classifies the life-cycle stage, runs Damodaran's *possible / plausible / probable* test, and outputs a **Narrative Brief** ending in a **story-to-numbers map**.

Carry two things forward:
- **The story-to-numbers map → Step 3.** This is what makes the valuation assumption-driven rather than default-driven: it hands suggested ranges for growth, margins, reinvestment, risk, and terminal posture — plus a method-path signal and a SOTP signal — straight into `company-valuation`.
- **The narrative + 3 P's verdict + confidence → Step 5** (the story half of the thesis) and **→ the report (Step 6)** as the qualitative spine.

Use the correctly-resolved ticker and currency from Step 1.

---

## Step 3: Full Valuation — use `company-valuation`

Read and follow the **`company-valuation`** skill end-to-end. It now runs in two parts:

**3a — Financial health snapshot (do first).** Follow `company-valuation`'s Step 2.5 (`references/financial_metrics.md`) to build the ~20-metric fact base with **5-year history** and a plain-language read on each: profitability margins, returns vs. cost of capital (ROIC, ROE, ROA, ROCE, WACC, **ROIC−WACC spread**), cash flow (Operating CF, CapEx, FCF, FCF margin), leverage (D/E, net debt, current ratio), valuation multiples (P/E, P/B, EV/EBITDA, P/FCF), and dividend (DPS, yield, payout). This grounds the reader and *informs the DCF inputs* — a widening ROIC−WACC spread with rising FCF justifies more confident growth/margin assumptions.

**3b — Valuation.** Then run DCF + relative/peer multiples + SOTP (where segments warrant it), blended to an implied price with a sensitivity grid and Bull/Base/Bear scenarios.

**Feed it the Step 2 story** so the assumptions are narrative-driven, not defaults:
- Revenue growth path should reflect the growth opportunities you identified.
- Margins and reinvestment (capex, ΔNWC) should reflect the business model.
- If the company has 2+ distinct segments, push for the SOTP path.

**Country/currency overrides (critical for non-US stocks):** `company-valuation` defaults to US parameters (10Y UST, US GDP terminal growth, US ERP). Override them using Step 1 + `references/markets.md`:
- **Risk-free rate** → the local 10Y sovereign yield (in the stock's currency).
- **Equity risk premium** → mature-market ERP **plus the country risk premium** (Thailand and most "other" markets carry an add-on; the US does not).
- **Terminal growth** → cap at the long-run nominal GDP growth of the home economy, never above the risk-free rate.
- **Currency** → keep all figures in local currency; optionally show a USD-converted fair value for context.

Capture from this step: **the financial snapshot (metrics + 5-yr trends + reads)**, blended fair value, per-method implied prices, WACC and its components, the sensitivity matrix, the Bull/Base/Bear table, and **candidate investment hooks** from the valuation anomaly scan.

---

## Step 4: Earnings & Sentiment — use `earnings-recap` then `earnings-preview`

Two lenses on the same stock:

1. **`earnings-recap`** — Read and follow it to analyze the *most recent* reported quarter: actual vs. estimate, surprise magnitude, and the stock's price reaction. This tells you how the company is executing and how the market judged it.
2. **`earnings-preview`** — Read and follow it for the *upcoming* report: consensus estimates, the beat/miss track record, analyst sentiment, and what the market is positioned for.

Synthesize a **sentiment read**: Is the stock priced for perfection or for pessimism? Does recent execution support the valuation story from Step 3, or contradict it? A great business at a price that already bakes in flawless execution is a different investment than the same business after a sentiment washout — say which one this is.

Use the same correctly-suffixed ticker from Step 1 (e.g., `.BK` for Thai names) so the earnings skills pull the right listing.

---

## Step 4.5: Technical Timing — use `bf-tech-analysis`

Read and follow the **`bf-tech-analysis`** skill before final synthesis. It captures a TradingView chart image via the local `tradingview_chart_image` MCP tool, then performs a top-down weekly→daily technical read calibrated to the specific stock.

Pass it:
- **Resolved market symbols from Step 1** — yfinance ticker for OHLCV (e.g., `CPALL.BK`, `7269.T`, `600519.SS`) and TradingView symbol/exchange for the chart image (e.g., `SET:CPALL`, `TSE:7269`, `SSE:600519`).
- **Current price and currency** from the latest data pull.
- **Fair value and upside/downside** from Step 3 so the technical targets can reconcile with the long-term value magnet.
- **Earnings/sentiment context** from Step 4 when it affects timing.

Capture from this step: TradingView chart image(s), weekly context, daily condition classification, entry zone, stop, target(s), R-multiple, timing verdict, and technical invalidation. Feed these directly into Step 5's entry/staging/stop plan and Step 6's chart/technical timing section.

---

## Step 5: Synthesize — use `investment-synthesis`

Pull Steps 2–4.5 into a decision. Read and follow the **`investment-synthesis`** skill, feeding it its inputs:
- **From Step 2** — the narrative, the 3 P's verdict, the life-cycle stage, and the confidence level.
- **From Step 3** — blended fair value, per-method prices, WACC components, the sensitivity grid, the Bull/Base/Bear table, the ROIC−WACC spread / leverage read, and the candidate investment hooks.
- **From Step 4** — the recent-quarter execution read and the upcoming-quarter setup (is the stock priced for perfection or for pessimism?).
- **From Step 4.5** — the TradingView chart image, technical condition, entry zone, stop, target(s), R-multiple, timing verdict, and invalidation level.

It first selects the **Key Investment Insight**, then produces: a one-paragraph **thesis** in Damodaran's voice; a probability-weighted Bull/Base/Bear **scenario timeline** (~12 / 24 / 36 mo) with expected value; a **conditional investment plan** (entry vs fair value, margin of safety, sizing & staging, conviction-builders, thesis-breakers, horizon) tailored to the setup archetype; and the **key risks** ranked by impact.

Anchor every target to the Step-3 fair value and its drivers — do not invent prices the valuation doesn't support. The plan is conditional, never a buy/sell command. Restate the **not-financial-advice** disclaimer here.

---

## Step 6: Build the Report — use `bf-report`

Read and follow the **`bf-report`** skill to generate the deliverable: a single self-contained, **filing-grade HTML document** (10-K / 56-1 style) — a continuous, navigable report, not a slide deck. Collect the outputs of Steps 2–5 and hand them over as its inputs (it is a renderer):
- **Step 2** → §1 Business & Narrative (incl. the Moat subsection and the Growth subsection) and the 3-P verdict.
- **Step 3** → §2 Financial Dashboard (the ~20-metric snapshot with 5-yr trends) and §3 Valuation (methods, DCF build, sensitivity heatmap, peers, SOTP-if-any).
- **Step 4** → §4 Earnings & Sentiment.
- **Step 4.5** → §5 Technical Timing (TradingView chart image, top-down read, entry zone, stop, targets, R, timing verdict).
- **Step 5** → the Executive-Summary Key Investment Insight + thesis + verdict band, §6 Scenarios & Investment Plan, and §7 Key Risks.

`bf-report` owns the house style (sober editorial palette, sticky linked TOC, numbered/anchored sections, judgement-coloured metrics, inline SVG sparklines, the moat meter, print CSS) — **do not** brand-match the palette to the company. It writes one `.html` via bash heredoc, then presents it. For Thai investors, write the report in **Thai** unless the user explicitly asks otherwise. The final HTML must be responsive and usable on mobile, with no horizontal overflow in the first viewport or key tables.

Then present the finished HTML file to the user.

---

## Notes & Edge Cases

- **Market not given and symbol ambiguous** → ask before doing anything (Step 1). Never assume the exchange.
- **Thai / non-US tickers** → always carry the suffix through every sub-skill; mismatched suffixes silently return wrong data or fail.
- **Banks/insurers/REITs** → `company-valuation` handles these with P/B, P/TBV, or P/FFO instead of DCF; let it pick the right path, and reflect that in §3 of the report.
- **Thin data / pre-revenue / illiquid small caps** → flag confidence as low in both the analysis and in the report; widen scenario ranges.
- **User only wants part of this** (e.g., "just value it, no report") → run only the relevant steps; this skill is the full pipeline but the steps are modular.
- **Keep currency consistent** — never mix THB and USD figures in the same table or chart without labeling.
