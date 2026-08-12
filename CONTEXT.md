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
