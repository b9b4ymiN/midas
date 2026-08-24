# Stage classification at long-term settings

The stage taxonomy is Stan Weinstein's, from *Secrets for Profiting in Bull and Bear Markets* (1988): a stock is always in one of four phases, and the phase is read from where price sits relative to a long moving average and which way that average is pointing. Weinstein's own instrument is the **30-week moving average on weekly bars** — that is used here unchanged.

The monthly read has no Weinstein setting, because he did not publish one. It uses the **10-month simple moving average**, the instrument in Meb Faber's *A Quantitative Approach to Tactical Asset Allocation* (2007), which is roughly the 200-day average expressed in months and is the most widely tested long-horizon trend filter in print. Both choices are recorded in the pack so a reader can see what the stage was judged against.

Nothing here is a trading system. The stages are a description of what has already happened, used to sit beside the business life-cycle stage in `stage-business-alignment.md`.

---

## The two instruments

| Read | Bars | Moving average | What it answers |
|---|---|---|---|
| Monthly | Monthly OHLCV, 10 years where available | 10-month SMA | Which decade-scale phase the stock is in |
| Weekly | Weekly OHLCV, 5 years where available | 30-week SMA | The phase now, and what is changing |

The monthly is read before the weekly. The monthly is the context; the weekly is the movement inside it. Reading the weekly on its own produces a stage change every few months, which is exactly the noise a long-term reading exists to filter out.

---

## The unclosed bar

**The newest bar is excluded from every judgement until its period closes.** A monthly bar four days into the month is not a monthly bar, and a weekly bar on a Tuesday is not a weekly bar. Both are partial samples that move, and reading them produces stage changes that unwind by the end of the period.

The excluded bar is still shown on the chart — it is real price — and `data_quality.unclosed_bar_excluded` records the date that was dropped and from which timeframe. The last close is reported separately in `price_context` so the reader has today's price without it having contaminated the stage.

---

## Measuring the two inputs

**Price position** — the close of the most recent *closed* bar against the moving average value at that bar. Above or below; no tolerance band, because the slope carries the ambiguity.

**Slope class** — the percentage change in the moving average across a lookback window, classified into rising, flat, or falling:

| Read | Lookback | Rising | Flat | Falling |
|---|---|---|---|---|
| Monthly | 6 months | > +2% | −2% to +2% | < −2% |
| Weekly | 13 weeks | > +1.5% | −1.5% to +1.5% | < −1.5% |

The flat band exists because a base and a top are both defined by an average that has stopped going anywhere; without a band, every base reads as a shallow advance or a shallow decline depending on the last bar.

**Volume context** — the ratio of the last 3 bars' average volume to the trailing 12-bar average, reported alongside each read. Weinstein's breakout condition is volume expansion, so a stage 1 → 2 transition without it is recorded as unconfirmed rather than being denied.

---

## The four stages

### Stage 1 — Base

Price oscillating around a **flat** moving average, after a decline. Neither side has control. The characteristic mistake is calling it stage 2 on the first move above the average while the average is still flat.

Reads as stage 1 when: slope class is flat, the highest close of the last 12 bars is not in the last 3, and the last close sits in the **lower** half of the 12-bar high-low range.

### Stage 2 — Advance

Price **above** a **rising** average, making higher highs and higher lows. This is the phase in which almost all lasting gains occur, which is why Minervini's trend template — implemented in this repo under `minervini-sepa` — screens for it as a precondition rather than as a signal.

Reads as stage 2 when: price is above the average and slope class is rising.

### Stage 3 — Top

Price still near or above the average, but the average has **stopped rising**. Volatility usually widens and new highs stop being made. Stage 3 is the hardest read and the most valuable, because it is where an advance ends without any single dramatic bar.

Reads as stage 3 when: slope class is flat, the highest close of the last 12 bars is not in the last 3, and the last close sits in the **upper** half of the 12-bar high-low range. The range position is what separates a top from a base: both are flat averages, and the difference is whether the stock is sitting near the top of its recent range or near the bottom of it.

### Stage 4 — Decline

Price **below** a **falling** average, making lower highs and lower lows.

Reads as stage 4 when: price is below the average and slope class is falling.

### When none of them fits

Where the combination does not match any of the four, the read is `TRANSITIONAL`, with the two inputs stated. Three cases produce it, and all three are common:

- **Price above a falling average** — a rally inside a decline, or the beginning of the end of one.
- **Price below a rising average** — a pullback inside an advance, or the beginning of the end of one.
- **A flat average with the stock making its highest close right now** — an advance the average has not confirmed yet.

`TRANSITIONAL` is an honest answer and usually a temporary one. Forcing it into the nearest stage is not honest, and it is how a decline gets reported as a base.

---

## `stage_since`

The date the current stage began: the close of the earliest bar from which the stage classification has held continuously to now, requiring **two consecutive confirming bars** before a change is recognised. The confirmation rule exists because a single bar crossing an average and crossing back is not a stage change, and dating a stage from that bar makes the stage look older than it is.

A stage whose start date cannot be established from the available bars is `UNRESOLVED`. It is not backdated to the beginning of the data, and it is not given today's date.

### The pending change

The confirmation rule creates a gap: the newest closed bar can already read as something else while the confirmed stage has not moved yet. Reporting only the confirmed stage produces a read that contradicts its own stated price position — "stage 4" beside "price above the average" — and a reader is right to distrust it.

So both are reported. `pending_change` carries what the newest closed bar reads, how many bars it has held, and how many more it needs, or `NONE`. The confirmed stage stays the pack's answer; the pending change is what the reader watches. On a weekly chart it is often the most decision-relevant line in the pack, because it is the earliest visible sign that a multi-year phase is ending.

---

## Invalidation

Every read carries what would falsify it, in terms of observations rather than opinion — the level the price would have to close beyond, or the slope change that would reclassify the average, and on which bar interval it would be observed. A stage read without an invalidation condition cannot be checked later, and a reading nobody can check is not evidence.

---

## What this file is not

It is not an entry method. There are no pivots, stops, position sizes, or R-multiples here, and none belong in `stage_pack`. Weinstein's own buy rules and Minervini's trend template both live on the timing line of this repo, where entry is the actual question being asked.
