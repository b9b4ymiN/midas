---
name: bf-tech-analysis
description: >
  Read a stock's chart the way a seasoned discretionary trader does — top-down (weekly then
  daily), with parameters calibrated to the specific stock rather than fixed defaults — to
  judge timing, entry zones, stops, and risk (R), and connect it to the fundamental fair
  value. Use this whenever the user wants a technical read or entry timing: "technical
  analysis of NVDA", "is this a good entry", "trend and Fibonacci", "VCP / pivot / breakout",
  "where's the stop", or "is the bottom in" — and as Step 4.5 of both-stock-analysis. It is
  not fixed to one style: it classifies the chart's condition (waiting to break, pullback in
  an uptrend, at support or a possible bottom, a broken downtrend awaiting a pullback, or an
  intact downtrend), then runs the fitting toolkit — fitted MAs, Fibonacci, trendlines/
  channels, relative volume, ATR, RSI divergence, VCP — with confirmations, warnings, and
  targets as zones. Output: entry zone, stop, target, R-multiple, and a timing verdict for
  investment-synthesis. Not financial advice.
---

# BF Technical Analysis

Reads a chart the way a professional discretionary trader does: **top-down**, with the parameters **fitted to this specific stock**, to decide *when and how to act and where the risk is* — not whether the company is worth owning (that is the fundamental work). It is deliberately **multi-style**: it diagnoses the chart's condition first, then applies the toolkit that fits, with confirmations *and* warnings, and **targets/entries as zones, not single points**. Conviction scales with **confluence** (independent tools agreeing). When there is no clean setup, it says so.

The technical read pairs with the intrinsic **fair value as the long-term magnet**: a cheap stock (large fair-value upside) in a constructive technical condition is a high-conviction, defined-risk entry; the same cheap stock in an intact downtrend is a "wait for the trigger."

**Disclaimer:** Research and educational output only. Not financial advice. Technicals inform timing and risk, not whether to own the business.

---

## Inputs

- **Ticker** with the correct exchange suffix and currency (from the pipeline's Step 1, e.g. `.BK`).
- **Fundamental fair value & upside** if available (from `company-valuation`) — needed to set the long-term magnet/target and to judge the "bottom + volume drying + valuation upside" case. If running standalone without it, still do the technical read but flag that the magnet is unknown.
- **Price/volume history** — pull weekly *and* daily OHLCV (see Step 1).

---

## Step 1: Pull multi-timeframe data, then CALIBRATE to this stock

Do **not** apply default parameters (the classic "buy the 20/50-day" is often wrong for a given name). First fit the parameters to the stock's own behaviour. Pull **weekly and daily** OHLCV (≥3–5 years weekly, ≥1–2 years daily), then calibrate — full routines and code in `references/indicators.md`:

- **Which moving average the stock actually respects** — test SMA/EMA across lengths (10/20/30/50/100/150/200); count touches and clean bounces; pick the MA(s) this stock honours, not an assumed one.
- **Fibonacci anchors** — auto-detect the significant swing(s) to anchor retracements/extensions on; check which Fib levels have historically acted as support/resistance for this name.
- **Volatility & typical pullback** — ATR (for stop distance) and the stock's usual pullback depth (so "a normal dip" is measured against its own history, not a generic %).
- **Volume baseline** — the average and what counts as a genuine expansion/dry-up *for this stock*.

These fitted parameters feed every later step. State them, because they justify the levels you use.

---

## Step 2: Top-down read — the weekly first

Establish context on the **weekly** before touching the daily entry. Cover: the **primary trend** and **Weinstein stage** (1 base / 2 advance / 3 top / 4 decline), the **Minervini Trend Template** check, the **major** horizontal support/resistance, the governing **trendlines and channels**, and the **big-picture Fib** levels. The weekly tells you *what game you are playing*; the daily only refines *the entry*. (Methods in `references/indicators.md` and `references/levels_and_risk.md`.)

---

## Step 3: Classify the chart's condition (diagnose before prescribing)

On the daily, within the weekly context, classify the chart into its current condition. **Every chart gets a classification — nothing is rejected for failing a setup filter.** The condition then selects which toolkit to run (Step 4). The conditions (full decision tree in `references/playbook.md`):

| Condition | What it looks like |
|---|---|
| **Waiting to break** (base / coil under resistance, incl. VCP) | Constructive consolidation, contracting range, volume drying into a pivot |
| **Pullback in an uptrend** | Stage-2 uptrend pulling back toward a respected MA / Fib zone |
| **At support / possible bottom** | A decline decelerating into structural support, volume drying up |
| **Broken downtrend line — awaiting pullback** | A descending trendline just broken; needs a pullback to confirm |
| **Downtrend intact (stage 4) / extended / choppy** | No actionable condition yet |

---

## Step 4: Run the context toolkit (confirmations, warnings, targets — as zones)

For the diagnosed condition, run the fitting toolkit. Each read is **two-sided** (what confirms it *and* what would invalidate or warrant caution) and conviction rises with **confluence**. Full per-condition toolkits in `references/playbook.md`; the essentials:

- **Waiting to break / VCP** — locate the **pivot**; require **volume expansion** on the break; for VCP verify the contraction sequence per Minervini (successive tighter pullbacks, volume dry-up). **Warn** on bearish **RSI/momentum divergence** into the highs, prior failed breakouts, or heavy overhead supply.
- **Pullback in an uptrend** — find the buy **zone** from **Fibonacci** (38.2 / 50 / 61.8 of the prior swing) **confluent with the MA this stock respects** (from Step 1, not assumed 20/50); pullback volume should be light; confirm on a higher-low / reclaim. **Warn** if the dip is abnormally deep for this name, volume is heavy, or it loses the 61.8 / the fitted MA.
- **At support / possible bottom** — confirm *where the decline is likely to end* using **Fib retracement/extension of the down-leg** + prior structural support + **volume dry-up** + **bullish divergence**; do not assume the bottom is in — state the levels that would confirm it, and let the **valuation floor** add conviction.
- **Broken downtrend line** — wait for the **pullback** that holds above the break and reclaims; enter on confirmation, not on the first break.
- **Downtrend intact / extended** — project **downside targets via Fib extensions** and the **descending channel lines** (upper/lower) so you know how far it could go and where to *start* watching; otherwise **no entry** — wait for a base or a trend change.

---

## Step 5: Risk geometry & timing verdict

Translate the read into tradeable geometry (see `references/levels_and_risk.md`):

- **Entry zone** (a band, from the toolkit) — not a single price.
- **Stop** — below the structure that invalidates the setup, sized with ATR so it is neither too tight for this stock's noise nor too loose.
- **Target(s)** — Fib extensions, prior highs, measured move, and the **fundamental fair value as the longer-term magnet**.
- **R-multiple** — (target − entry) / (entry − stop); state the reward-to-risk.

Then give a **timing verdict**, conditional and explicit: **enter now** / **stage in on a trigger** (name it) / **wait for** a specific technical event / **avoid**. This is what flows into `investment-synthesis`'s entry, staging, and stop.

---

## Step 6: Connect to valuation, then respond

Reconcile the technical timing with the fundamental fair value, and say which case this is — e.g. *cheap (large upside) + waiting-to-break/at-support with volume drying ⇒ stage in with defined risk*; *cheap but stage-4 downtrend ⇒ wait for the trendline break + pullback confirm*; *fairly valued but a clean VCP pivot ⇒ a faster, tighter-risk trade with the FV as the cap*.

### Output format

```
# Technical Read — [Company] ([Ticker])

## Calibrated parameters
[respected MA(s); Fib anchors + levels that held; ATR; typical pullback; volume baseline]

## Top-down context (weekly)
[primary trend, stage, Trend Template, major S/R, trendlines/channels, big Fib]

## Condition (daily)
[the classified condition + why]

## Read & confluence
[the context toolkit: confirmations · warnings (incl. divergence) · Fib/channel targets — as zones]

## Risk geometry
[entry zone · stop · target(s) incl. fair-value magnet · R-multiple]

## Timing verdict
[enter now / stage on trigger / wait for [event] / avoid] — and how it pairs with the valuation upside

## Disclaimer
Research and educational output only. Not financial advice.
```

---

## Caveats
- Technical analysis is probabilistic, not predictive — it sets odds and a stop, not a certainty.
- Always calibrate to the stock; assumed parameters (a generic MA or Fib) are the most common error.
- Read two-sidedly — every setup has an invalidation; a trigger without an invalidation is incomplete.
- The lower/intraday timeframe is optional for entry precision; weekly→daily is the required spine.
- yfinance data is unofficial; cross-check unusual prints. Not financial advice.

---

## Reference Files
- `references/playbook.md` — The top-down method, the chart-condition decision tree, and the per-condition toolkit (confirmations, warnings, targets) with confluence scoring and invalidation.
- `references/indicators.md` — Weekly+daily data pull and the calibration routines (which MA the stock respects, Fib auto-anchoring, ATR, pullback depth, volume baseline), plus MA stack, RSI + divergence, Weinstein stage, Minervini Trend Template, swing/pivot, and VCP-contraction detection — with code.
- `references/levels_and_risk.md` — Support/resistance, trendline and channel construction, Fibonacci (retracement entries, extension and downside targets), and risk geometry (entry zone / stop / target → R) with confluence and position-sizing linkage.
