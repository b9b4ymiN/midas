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
  This skill orchestrates eleven construction sub-skills in sequence — business-narrative,
  business-drivers, earnings-quality, company-valuation, peer-impact, earnings-recap,
  earnings-preview, growth-outlook, bf-tech-analysis, investment-synthesis, and bf-report —
  over one shared har-to-api data snapshot, and ends by handing the finished report to
  stock-grill. ALWAYS confirm
  the market first (Thai / US / other)
  so the correct exchange suffix, currency, and country-risk parameters are used. Prefer
  this over running the individual finance skills separately whenever the user wants the
  complete analysis or a finished report as the deliverable.
---

# Both Stock Analysis

A full-stack equity research pipeline. You are the analyst, working **in the spirit of Aswath Damodaran**: every valuation is a bridge between a *story* about the business and the *numbers* that story implies. You are rigorous, intellectually honest about uncertainty, allergic to hype with no cash flows behind it, and you always tie value back to four drivers — **cash flows, growth, reinvestment efficiency, and risk (cost of capital).**

The pipeline runs from ticker to report and then, deliberately, does not stop there: the last step attacks what the previous six built. It chains twelve installed sub-skills, and opens by pulling the data once:

| Step | Sub-skill used | Purpose |
|---|---|---|
| 0 | `har-to-api` | Pull every fact once, with provenance — one snapshot the whole run reads from |
| 1 | — | Confirm market, set country/currency parameters |
| 2 | `business-narrative` | Damodaran story research → story-to-numbers map |
| 2.3 | `business-drivers` | Read the business, derive what actually moves its earnings, and quantify it — margin points per 10% move, and when it lands |
| 2.5 | `earnings-quality` | Normalise the earnings base (Damodaran: average the MARGIN over a cycle, not the earnings) + rule on whether growth may be stacked |
| 3 | `company-valuation` | Financial health snapshot (~20 metrics, 5-yr trends + reads) → DCF + relative + SOTP → intrinsic value + candidate investment hooks |
| 3.5 | `peer-impact` | Find the competitors whose actions can actually move earnings — worldwide by revenue mix, filtered by shared input / shared customer / price setting |
| 4 | `earnings-preview` + `earnings-recap` + `growth-outlook` | Setup, track record, sentiment · growth decomposed by source · dated catalysts |
| 4.5 | `bf-tech-analysis` | TradingView chart image + top-down technical timing, entry zone, stop, target, R |
| 5 | `investment-synthesis` | Select the key investment insight → thesis, 1–3 yr scenarios + investment plan |
| 6 | `bf-report` | Filing-grade HTML research document (10-K / 56-1 style), insight-first and mobile-responsive |
| 7 | `stock-grill` | Attack the finished report before any capital moves — R0 consistency, then the five adversarial rounds |

> **Dependencies:** This skill assumes `har-to-api`, `business-narrative`, `business-drivers`, `earnings-quality`, `company-valuation`, `peer-impact`, `growth-outlook`, `earnings-preview`, `earnings-recap`, `bf-tech-analysis`, `investment-synthesis`, `bf-report`, and `stock-grill` are installed. If one is missing, tell the user which `.skill` to install before continuing.

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

## Step 0: Pull the Data Once — use `har-to-api`

Run this **before Step 1**, as soon as the ticker is known.

```bash
python skills/har-to-api/scripts/fetch.py [TICKER] --market [venue] --profiles skills/har-to-api/profiles
# -> writes .data/[TICKER]/[YYYY-MM-DD].json
```

Every later step reads from that snapshot instead of fetching its own copy.
Two reasons, and the second is the one that bites:

**Consistency.** Steps run minutes or hours apart. If §3 pulls the price at
10:00 and §5 pulls it at 14:00, every return figure in §6 is computed off one of
two different numbers — and the report will disagree with itself in a way that
looks like sloppiness rather than the timing artefact it is. Step 7's R0 pass
exists to catch exactly this; pulling once means it has nothing to catch.

**Reproducibility.** `--use-snapshot [date]` replays a run byte-for-byte. When a
figure looks wrong, that is what separates *the data moved* from *the analysis
changed* — without it you cannot tell, and both look identical from the outside.

Carry forward:

- **The snapshot path**, handed to every subsequent step.
- **The fallback count.** Facts the primary source could not supply are tagged
  `"tier": "FALLBACK"` with a reason. That flag must reach §6 of the report —
  a reader deciding on a number is entitled to know it came from the reserve
  source.
- **Conflicts.** Two providers disagreeing by more than 2% on the same fact are
  reported, never silently resolved. Usually it means they define the metric
  differently, which is worth knowing before building on either.

**What the snapshot will not carry:** segment mix comes tagged with the
provider's own labels and uneven coverage, so cross-check it against the filing
before Steps 2.3 and 3.5 rest on it. Non-exchange commodity prices (Step 2.3's
drivers) are usually absent entirely — source those by hand and record where
they came from.

If no snapshot exists — a standalone sub-skill run, or a fact outside the
profiles — each skill falls back to its own data path. That is supported, and it
must be **said out loud** rather than passed off as primary.

---

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

## Step 2.3: What Actually Moves the Earnings — use `business-drivers`

Read and follow **`business-drivers`** before valuing anything. Its governing
rule: **understand the business first, only then go looking for data.** A step
that starts from a list of candidate drivers returns "oil, FX, rates" for every
company alive, which is true and useless.

It reads the segment mix, cost structure, selling and buying geography and
contract terms, derives the drivers those imply, and then quantifies each:

```bash
python skills/pipeline/business-drivers/scripts/sensitivity.py \
  --driver "tuna" --cost-share 0.55 --margin 0.0487 --move 0.10 \
  --pass-through 0.6 --revenue 135439918000 --lag-months 3
```

Carry forward:

- **Sensitivity per driver** -> Step 3's scenario range, as a third axis beyond
  WACC x terminal growth.
- **The commodity price path** -> Step 2.5, where Damodaran's method calls for
  **futures prices** rather than analyst forecasts.
- **Timing lags** (inventory buffers, hedges, contract repricing) -> Step 4's
  catalyst dates. A driver that moved today may not reach reported margin for
  two quarters, and a model that books it immediately is wrong about the quarter
  in a way that reads as simply wrong.
- **The most sensitive driver** -> Step 5's thesis-breakers.

**Check it worked:** run it on a food processor and it must produce the raw
material without being told. If the output is generic macro variables, the
reading was skipped.

---

## Step 2.5: Normalise the Earnings Base — use `earnings-quality`

Before valuing anything, decide what the company earns in a *normal* year. A
DCF built on a distorted base is a precise calculation of a wrong number.

Read and follow the **`earnings-quality`** skill. It applies Damodaran's method
— average the **operating margin** across a full cycle (5-10 years, chosen from
the industry) and apply it to current revenue, rather than averaging reported
earnings, which breaks whenever a company has changed scale or taken a hit
below the operating line.

Feed it the ~5-year series from the data layer and carry three things forward:

- **The normalised operating income and the margin behind it** -> the starting
  point for Step 3's projection, replacing the naive "last year's EBIT".
- **The exclusion table** (every item removed, its amount, and why) -> goes
  into the report appendix and gives `stock-grill` something concrete to attack.
- **The growth-eligibility verdict.** If the gates fail, the normalised base
  *already contains* the recovery, and Step 3 must NOT also apply a consensus
  growth rate built from that same recovery — that is Damodaran's
  double-counting trap and it silently inflates fair value.

If earnings cannot be normalised responsibly (too little history, an erratic
margin, a structurally impaired business), say so plainly and let Step 3 widen
its scenario range instead of feigning precision.

**Consistency rule:** if you normalise earnings, normalise capex, working
capital and the financing assumption over the same window. A mid-cycle profit
paired with trough-year capex describes a year that never happened.

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

## Step 3.5: Who Can Actually Hurt You — use `peer-impact`

Step 3's relative valuation already built a peer set, and it is the right one for
its job: companies the market prices with the same logic. **This is a different
question** — whose decisions change our margin — and it produces a different set.

Read and follow **`peer-impact`**. Two layers:

**Layer 1** searches worldwide from the segment mix, with **no country filter**.
Competition for a scarce input is global by construction. A search restricted to
the home market returns domestic companies selling different products and misses
every real competitor, because they are all abroad.

**Layer 2** keeps only candidates that reach the margin through one of three
channels — they buy the same constrained input, sell to the same buyer, or are
large enough to set the price you follow. Everything scoring on none is dropped
however similar it looks.

```bash
python skills/pipeline/peer-impact/scripts/peer_impact.py \
  --candidates peers.json --margin 0.0487 --cost-share 0.55 \
  --pass-through 0.6 --input-move 0.10
```

For shared-input peers it chains into the same margin arithmetic as Step 2.3, so
"they add capacity" becomes "we lose N points of margin". The capacity-to-price
step is your estimate and the output says so.

**Do not replace the Peer Validation Gate.** Step 3's multiples table keeps its
own peer set and its own rules.

Carry forward: the ranked impact table into Step 5's key risks; shared-input
peers back into Step 2.3's driver confidence; a competitor's dated capacity
decision into Step 4b's catalysts.

**Write down who was dropped and why.** Without it a reader cannot tell a
thorough search from a lazy one, and Step 7 cannot attack the exclusions.

---

## Step 4: Earnings & Sentiment — use `earnings-recap` then `earnings-preview`

Two lenses on the same stock:

1. **`earnings-recap`** — Read and follow it to analyze the *most recent* reported quarter: actual vs. estimate, surprise magnitude, and the stock's price reaction. This tells you how the company is executing and how the market judged it.
2. **`earnings-preview`** — Read and follow it for the *upcoming* report: consensus estimates, the beat/miss track record, analyst sentiment, and what the market is positioned for.

Synthesize a **sentiment read**: Is the stock priced for perfection or for pessimism? Does recent execution support the valuation story from Step 3, or contradict it? A great business at a price that already bakes in flawless execution is a different investment than the same business after a sentiment washout — say which one this is.

Use the same correctly-suffixed ticker from Step 1 (e.g., `.BK` for Thai names) so the earnings skills pull the right listing.

---


### Step 4b: Growth & Catalysts — use `growth-outlook`

Alongside the earnings read, run **`growth-outlook`**. It answers two questions
the earnings skills do not.

**Is the growth repeatable?** It decomposes reported revenue growth into volume,
price, expansion, acquisition and currency, grading each by whether it can happen
again, and reports whatever the components fail to explain as *unexplained*
rather than spreading it across them. The test that earns its keep: price up
while volume down is cost pass-through, not pricing power — the most common way
a company losing customers reports a year of growth.

**What is coming, and when?** A catalyst table where **every row carries a date
and a way to verify it happened**. No date, no row — the repo's own decision
journal already says a catalyst without a deadline is wishful thinking, and until
now nothing produced the deadline.

Carry forward: the **durable share** of growth (only that belongs in a terminal
assumption), and the catalyst table into Step 5's scenario timeline and Step 7's
review date.

**Interaction to get right:** if Step 2.5's growth gates failed, the normalised
base already contains the recovery. Do not stack a growth rate from this step on
top of it — that counts the recovery twice.

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
- **From Step 2.3** — the driver list, each driver's sensitivity, and the timing lags.
- **From Step 2.5** — the normalised earnings base, the exclusion table, and whether a growth rate may be stacked on it.
- **From Step 3.5** — the ranked impact-peer table and the margin arithmetic for shared-input rivals.
- **From Step 4b** — the growth decomposition (durable share) and the dated catalyst table.
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

## Step 7: Attack What You Just Built — use `stock-grill`

**Do not end at Step 6.** A finished report is the moment confirmation bias is
strongest: the reader has just watched a case assemble itself and it looks
convincing, because it was built to. That is precisely when it should be
attacked.

Hand `stock-grill` the HTML file Step 6 produced:

```bash
python skills/stock-grill/scripts/read_report.py [TICKER]_BF-Report.html
```

It runs **R0 first** — a mechanical pass over the document's self-agreement:
does the current price match across §3 and §5, do the scenario probabilities sum
to 100, is the §6 target anchored to the §3 fair value, does every figure have a
source. Those are arithmetic errors, not wrong opinions, and they invalidate any
argument built on top of them. Fix the high findings before going further.

Then R1-R5 as documented in `stock-grill`: pre-mortem, sensitivity attack,
variant-perception check, gate audit, and the sell pre-commit that ends in a
**pre-registered decision journal**.

Two rules carried from `stock-grill`:

- The journal is written **ex ante**, before the outcome is known, and stored
  with the stock's analysis output — **never committed back to this repo**.
- Every question cites a section. Not "what if margins fall" but "§3 assumes a
  5.1% operating margin while §2 shows the last reported year at 4.6% — which
  is the thesis relying on?"

If the user declines the grill, say plainly that the report has not been
stress-tested, and note it in the handover. An unattacked thesis is a draft.

---

## Notes & Edge Cases

- **Market not given and symbol ambiguous** → ask before doing anything (Step 1). Never assume the exchange.
- **Thai / non-US tickers** → always carry the suffix through every sub-skill; mismatched suffixes silently return wrong data or fail.
- **Banks/insurers/REITs** → `company-valuation` handles these with P/B, P/TBV, or P/FFO instead of DCF; let it pick the right path, and reflect that in §3 of the report.
- **Thin data / pre-revenue / illiquid small caps** → flag confidence as low in both the analysis and in the report; widen scenario ranges.
- **User only wants part of this** (e.g., "just value it, no report") → run only the relevant steps; this skill is the full pipeline but the steps are modular.
- **Keep currency consistent** — never mix THB and USD figures in the same table or chart without labeling.
