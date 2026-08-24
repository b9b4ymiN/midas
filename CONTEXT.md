# Investment Skills — Context

The canonical vocabulary that every skill in this repo shares (ubiquitous language). A new skill **references terms from this file** rather than copying definitions, so a given term means the same thing across the whole pipeline.

Rule: include only methodology-specific terms where "different people mean different things" is a real risk. General finance terms (P/E, EPS, profit, share price, WACC, terminal value) do not belong here — only the coinages of this methodology that flow between skills.

## Thesis & decision

**Key Investment Insight**:
The single most important reason this stock is interesting at today's price — translated from the chosen hook into 3-5 plain-language lines, backed by a number.
_Avoid_: thesis, reason to buy, bull case

**Investment hook**:
A candidate anomaly from the valuation that changes the risk/reward — not yet an insight until it is chosen and translated into plain language.
_Avoid_: catalyst, anomaly

**Candidate hook**:
One item from the valuation's anomaly scan — a list of candidate hooks is produced, then one is chosen and promoted to the Key Investment Insight.
_Avoid_: anomaly, raw hook, hook candidate

**Variant perception**:
What you believe that the market does not — if you see what the market sees, there is no alpha. State precisely where you differ, why you are right, and what the market is pricing in.
_Avoid_: contrarian view, thesis, different perspective

**Thesis**:
One paragraph containing: what you pay (price vs fair value) · what you get (where the value comes from) · what must be true (the 1-2 narrative claims the value hinges on) · the asymmetry (is the downside protected, or is this priced for flawless execution?).
_Avoid_: recommendation, buy case, summary

**Thesis-breaker**:
A core assumption that, if wrong, invalidates the original reason to hold the stock and requires exit. Pulled from the sensitivity grid inputs that move fair value the most, with a defined observation that would trigger exit.
_Avoid_: risk factor, downside, concern

**Conviction-builder**:
Data points to watch each quarter that, if they materialize, would raise conviction (e.g. segment growth, margin trend, ROIC−WACC spread). The opposite of a thesis-breaker.
_Avoid_: positive signal, good news

**Setup archetype**:
The type of investment, which determines a different plan / position size — quality compounder · deep-value/turnaround · cyclical mid-cycle · GARP.
_Avoid_: stock type, category, style

**Priced for perfection**:
The market has already discounted the best case, leaving little room to beat — even good results may not lift the price, or may push it down.
_Avoid_: overvalued, expensive

## Narrative (Damodaran)

**Four story pillars**:
The four drivers every valuation ties back to — cash flows, growth, reinvestment efficiency, and risk (cost of capital). The story-to-numbers map connects the narrative to these four.
_Avoid_: value drivers, key drivers, fundamentals

**Life-cycle stage**:
Where the company sits on Damodaran's life-cycle (start-up → young growth → high growth → mature growth → mature → decline) — it shapes which narrative is plausible and which valuation inputs are defensible.
_Avoid_: company stage, maturity stage, growth phase

**Story-to-numbers map**:
The bridge from business narrative to valuation drivers (growth, margin, reinvestment) — turns the story into numbers that can be tested.
_Avoid_: assumptions, model inputs, drivers

**The 3 P's**:
Three narrative-confidence levels — possible · plausible · probable — used to filter the story before running the numbers.
_Avoid_: probability, confidence level

## Valuation

**Fair value (blended)**:
The price the stock should trade at, weighted across DCF + relative + SOTP — not a single-method number, and not a target price.
_Avoid_: intrinsic value, target price

**Sensitivity grid**:
The matrix showing how fair value changes as key inputs (e.g. WACC × terminal growth) vary — the inputs that move fair value the most are the ones to challenge first. Produced by company-valuation; consumed by stock-grill R2.
_Avoid_: sensitivity matrix, sensitivity table, sensitivity analysis

**Margin of safety**:
The discount to fair value required before entry — it scales WITH the width of the scenario range (uncertainty) + business quality (ROIC−WACC) + balance-sheet risk. Not a fixed number.
_Avoid_: safety margin, buffer

**ROIC−WACC spread**:
Return on invested capital minus cost of capital — positive and growing means value creation; negative means value destruction. The test of whether the business genuinely creates value.
_Avoid_: spread, return on capital, ROIC

## Compounding (Mayer)

Vocabulary of the compounding line (`skills/compounder/`). It answers durability, not price, so it deliberately shares no terms with Valuation above.

**Future Compounding Economics**:
The research decomposition the whole compounding line hangs on — Incremental Return × Reinvestment Capacity × Duration. A decomposition for structuring evidence, never a formula that outputs a value.
_Avoid_: compounding formula, compounding score

**Economic Unit**:
The smallest repeatable thing whose economics reveal what incremental capital earns — one store, one cohort, one facility, one customer. A hybrid business may need more than one. Not a reporting segment, and not the corporate average.
_Avoid_: unit economics, segment, business unit

**Growth Architecture**:
The internal chain from external driver → capital/input → unit output → volume/price/mix/capacity/geography/product/M&A → revenue → NOPAT → FCF. It is what the company does with growth; Growth Decomposition is where the growth came from.
_Avoid_: growth model, growth bridge

**Growth Decomposition (Layer 1)**:
Splitting reported growth into category/geography momentum + market-share change + M&A, reconciled to operating drivers. Distinct from `growth-outlook`'s decomposition on the valuation line, which grades volume/price/expansion/acquisition/currency by repeatability for a forecast.
_Avoid_: growth breakdown, revenue bridge

**Arena class**:
The evidence class of each business arena — PROVEN · EMERGING · OPTION · NARRATIVE. Market size can never upgrade an arena's class; only evidence can.
_Avoid_: segment, opportunity, optionality

**Metric Comparability Gate**:
The check run before any multi-period trend, marking a series COMPARABLE, ADJUSTED_COMPARABLE, NOT_DIRECTLY_COMPARABLE, or UNRESOLVED, and stating whether demand evidence is sell-in or sell-through. Stops a redefined KPI from being read as a trend.
_Avoid_: like-for-like, apples to apples

**Net incrementality**:
New demand a channel, store, or geography adds after subtracting what it took from existing ones, including halo and recapture. A new store that moves existing customers is not growth.
_Avoid_: cannibalization, same-store growth

**Evidence Ladder**:
The five rungs evidence is ranked on — Story → Operating indicators → Unit economics → Corporate/per-share translation → Persistence. Determines Evidence Maturity.
_Avoid_: evidence quality, confidence level

**Potential / Evidence Maturity / Confidence**:
Three verdicts reported separately and never collapsed into one score — how large the compounding could be · how far up the Evidence Ladder the proof reaches · how sure we are given counter-evidence and gaps. A young company can rate high Potential and low Evidence Maturity at the same time.
_Avoid_: rating, conviction score, grade

**Reverse Reality Check**:
Starting from a 10x business outcome and backing out the market share, capital, funding, and dilution it would require, to see whether the required world is plausible. Stress, not prediction; 100x is optional.
_Avoid_: reverse DCF, upside case, price target

**SCOPE_CHALLENGE**:
The signal a downstream skill raises when new evidence invalidates the Layer 0 business frame — it forces the frame to be redone rather than silently redefined mid-analysis.
_Avoid_: scope creep, pivot

## Accumulation (price & stage)

Vocabulary of the two skills that run after the compounding verdict is settled (`compounder-stage-chart`, `compounder-accumulation-plan`). The compounding line above answers durability and refuses to look at price; this line is the only place in that run where price is allowed in, and it enters as a *comparison*, never as a valuation.

**Price-Implied Expectations**:
The growth the current share price already assumes, solved for by running the cash-flow arithmetic backwards from the market price at a stated required return. Rappaport & Mauboussin's method: the price is the input and the expectation is the output, so no fair value is ever produced. The required return is declared as an assumption and shown with its sensitivity, never derived into a single WACC.
_Avoid_: reverse DCF, implied valuation, fair value

**Expectation Gap**:
The distance between Price-Implied Expectations and the `durable_growth` the compounding work concluded the engine can actually deliver — reported as a direction and a size (the price asks for less than / about / more than the engine can produce), never as an upside percentage. Distinct from the **Reverse Reality Check**, which starts from a 10x business outcome and asks whether the required world is plausible; the Expectation Gap starts from today's price and asks what it is already paying for.
_Avoid_: upside, undervalued, margin of safety

**Accumulation Band**:
The price range in which buying is consistent with the Expectation Gap and the plan archetype — three bands (accumulate · hold, do not chase · too demanding), each a range with the condition that defines it. A band is not a target price and carries no instruction to trade.
_Avoid_: buy price, entry point, target price

**Stage Alignment**:
The reading produced by crossing the business life-cycle stage (from `economic_engine_pack.life_cycle_stage`) with the chart's Weinstein stage on the monthly and weekly views — four readings covering agreement in both directions and the two divergences, where the divergence is the information. Uses Weinstein's stage vocabulary defined under Technical timing below, at long-term settings rather than SEPA's entry settings.
_Avoid_: trend confirmation, technical setup, timing signal

**Plan archetype**:
Which shape the accumulation plan takes, selected from the thesis pack rather than chosen by judgement — `proven-compounder` (returns come from the business, so time in it matters more than entry price), `emerging-starter` (evidence is still shallow, so size is small and additions are conditional on evidence arriving), `narrow-runway` (the business cannot absorb capital at those returns, so the entry price is what the return depends on).
_Avoid_: strategy, style, allocation model

## Technical timing (SEPA)

**SEPA**:
Specific Entry Point Analysis — Mark Minervini's system that screens stocks through 4 gates: fundamentals (Q33) → trend template → setup (VCP) → risk geometry.
_Avoid_: trading system, strategy

**Stage 2**:
Weinstein's stage 2 (uptrend where price is above all key moving averages) — SEPA buys only in stage 2.
_Avoid_: uptrend, bullish phase

**Trend Template**:
SEPA's 8-rule price/MA screen that defines whether a stock is in a stage-2 uptrend — the second gate of SEPA (after Q33 fundamentals).
_Avoid_: trend rules, moving-average screen, MA checklist

**VCP**:
Volatility Contraction Pattern — a pattern where per-contraction volatility decreases progressively (contractions C1/C2/C3) before breakout. The core of timing.
_Avoid_: contraction pattern, base

**Pivot**:
The price point where a breakout confirms → the entry trigger (entry zone = pivot +0 to +5%).
_Avoid_: breakout point, entry

**R-multiple**:
The reward-to-risk ratio of a trade (target ≥ 3:1), used to compute position size from the entry-to-stop distance.
_Avoid_: RR, risk-reward, reward-risk

**Q33**:
SEPA's fundamental checklist split into MUST/PLUS/WATCH across 4 categories — earnings · sales · story/new factor · supply/demand.
_Avoid_: fundamental checklist, screen
