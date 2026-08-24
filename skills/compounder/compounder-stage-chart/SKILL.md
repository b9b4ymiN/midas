---
name: compounder-stage-chart
description: Use when a compounding verdict already exists and the question turns to what the share price has been doing over years rather than days — "is the market already pricing this in", "what stage is the chart in", "the business is compounding but the stock is going nowhere", "show me the monthly and weekly picture", or "does the chart agree with the business". It reads Weinstein stages on monthly and weekly bars, crosses that reading with the company's business life-cycle stage, and reports where the two agree and where they diverge. It produces no entry price, stop, target, or position size.
---

# Compounder Stage Chart

## Overview

A compounding verdict says what the business can do. It says nothing about what the market has already concluded. This skill supplies that second reading — the long-term stage of the chart — and, more usefully, **crosses it with the business life-cycle stage** so the reader can see agreement and disagreement between the two.

The disagreements are the point. A business earning high returns on new capital while its chart has sat in a two-year decline is telling you something; so is a mature business whose chart has run far ahead of it. Neither is a signal to act, and this skill never turns one into one.

It runs for **every** company, whatever the verdict — including one that failed. What the market thinks of a business you have just rejected is still worth a paragraph.

## Inputs

- **Ticker with exchange suffix** and the currency the bars are quoted in.
- **`economic_engine_pack.life_cycle_stage`** — both the adjusted stage and the raw stage. Without it there is no cross-reading, and `stage_alignment` is `UNRESOLVED`.
- **`compounder_thesis_pack`** for the as-of date and the verdict this reading sits beside.

## Step 1: Pull the bars

Weekly and monthly OHLCV, adjusted for splits and dividends. Ten years of monthly bars and five years of weekly bars where they exist; less is allowed and recorded in `data_quality`, never silently accepted.

```bash
python skills/compounder/compounder-stage-chart/scripts/stage_read.py <TICKER> --out run/<TICKER>-<DATE>/
```

**The newest bar is excluded from every stage judgement until it closes.** A month that is four days old is not a monthly bar, and half the false stage changes in practice come from reading one. The script drops it and records that it did.

## Step 2: Classify the monthly, and only afterwards the weekly

Read `references/stage-classification.md` before judging anything. The monthly read establishes which decade-scale phase the stock is in; the weekly refines it and is the one that changes.

Each read carries: the stage (1 base · 2 advance · 3 top · 4 decline), the moving average it was judged against, where price sits relative to it, the slope of that average, **`stage_since`** — the date the stage began — and what observation would invalidate the reading. A stage without a start date is `UNRESOLVED`, not a stage.

Where the monthly and weekly disagree, record the disagreement in `stage_conflict` rather than resolving it by preference. A weekly stage 4 inside a monthly stage 2 is an ordinary pullback in a long advance; the same weekly stage 4 inside a monthly stage 3 is not.

## Step 3: Cross the chart with the business

Read `references/stage-business-alignment.md`. Crossing the business life-cycle stage with the chart stage produces the **Stage Alignment** reading: one of `MARKET_HAS_NOT_PRICED_IT`, `MOVING_TOGETHER`, `LATE_AND_EXTENDED`, or `MARKET_SEES_DAMAGE_FIRST` — and `UNRESOLVED` where either side is missing.

Write the reading as a sentence a reader can act on their own judgement with, not as a label. "The business is still reinvesting at high returns while the chart has been in decline since early 2025, which means either the market has seen something the filings have not shown yet, or it is wrong" is a reading. "Divergence: bullish" is not.

## Step 4: Capture the charts

Read `references/chart-capture.md`. Two images — monthly and weekly — embedded as `data:image/png;base64,...` or as rendered inline SVG. Never a remote URL: the report is one self-contained file.

Where the TradingView capture tool is available, use it and record `source: TRADINGVIEW_MCP`. Where it is not, the script renders the same two timeframes as inline SVG from the bars already pulled, with the moving average and the stage bands drawn on, and records `source: RENDERED_SVG`. The fallback is not a degraded mode to apologise for — it is the path that also lets the business life-cycle bands be drawn under the price.

## Step 5: Write and validate the pack

Serialize `stage_pack.json` into the run directory, then:

```bash
python skills/compounder/future-compounder/scripts/validate_pack.py run/<TICKER>-<DATE>/ --stage stage_pack
```

Append to the Evidence Ledger — every price figure carries its source, the bar interval, and the as-of date, exactly as a filing figure would.

## What this skill does not produce

- **No entry, stop, target, or R-multiple.** Entry geometry belongs to the SEPA line (`minervini-sepa`, `bf-tech-analysis`), which is a different question asked on different timeframes.
- **No target price** and no valuation of any kind.
- **No revision of the verdict.** A chart reading may never change a leg rating or an evidence class. Where price evidence genuinely contradicts the thesis, raise `SCOPE_CHALLENGE` and let the core layers re-run.
- **No instruction.** `stage_alignment` describes a relationship. It does not say buy, sell, or wait.

## DoD

`stage_pack` carries a monthly read and a weekly read, each with a moving average, a price position, a slope, a `stage_since` date, and its invalidation condition; a `stage_conflict` entry or `NONE`; the business life-cycle stage as it was received; a `stage_alignment` reading written as a sentence; two chart assets with their source recorded; and a `data_quality` block stating bar coverage and the excluded unclosed bar.

**STOP:** Do not infer fair value, set a target price, issue an entry or exit level, or adjust any upstream verdict from a chart reading.

---

Research and educational output only. Not financial advice.
