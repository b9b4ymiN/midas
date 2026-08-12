# Technical Playbook — Diagnose, Then Prescribe

The reasoning core of `bf-tech-analysis`. The discipline: **read top-down (weekly → daily), classify the chart's condition, then run the toolkit that fits that condition** — never force one trading style. Every chart receives a classification; nothing is rejected for "failing a setup." Read alongside Steps 2–4 of `SKILL.md`.

Two rules govern everything below:
1. **Two-sided.** Every read states what *confirms* it and what *invalidates* it (or warrants caution). A trigger with no invalidation is incomplete.
2. **Confluence sets conviction.** A call is stronger when independent tools agree (fitted MA + Fib + structure + volume + no adverse divergence). One tool alone is a hint, not a signal.

And one prerequisite: the moving averages, Fib anchors, volatility, and volume thresholds must be **calibrated to this stock first** (`indicators.md`). The levels below are only as good as that calibration.

---

## The top-down spine

- **Weekly = context (what game are we playing?).** Primary trend, Weinstein stage (1 base / 2 advance / 3 top / 4 decline), Minervini Trend Template, major horizontal S/R, governing trendlines/channels, big-picture Fib. A daily "buy" inside a weekly stage-4 downtrend is a different (worse) trade than the same daily pattern in a weekly stage-2.
- **Daily = the entry (where and when?).** Refine the actual zone, the trigger, and the stop, *consistent with* the weekly.
- **Lower/intraday = optional** precision on the entry once the daily says go.

---

## Condition decision tree

Classify the daily within the weekly context into one condition, then go to its toolkit.

```
Weekly trend?
├─ Up (stage 2)
│   ├─ consolidating under resistance / tightening → WAITING TO BREAK (incl. VCP)
│   └─ pulling back toward a respected MA/Fib  → PULLBACK IN AN UPTREND
├─ Down (stage 4) but a descending trendline just broke → BROKEN DOWNTREND — AWAIT PULLBACK
├─ Down decelerating into structural support, volume drying → AT SUPPORT / POSSIBLE BOTTOM
├─ Down, intact, no break yet → DOWNTREND INTACT (no entry; project downside)
└─ Range / extended / choppy → NO CLEAN CONDITION (wait)
```

---

## Per-condition toolkits

Each toolkit lists what to measure, what **confirms**, what **warns/invalidates**, and the **targets**. Express entries and targets as **zones**, not single prices.

### 1. Waiting to break (base / coil under resistance, incl. VCP)
- **Measure:** the resistance/**pivot**; base depth and length; volume trend into the pivot; for **VCP**, the contraction sequence (per Minervini: successive tighter pullbacks, each shallower, volume drying — e.g. 3 contractions like ~25% → ~12% → ~6%; the pivot is the final tight area).
- **Confirm:** breakout through the pivot on **volume expansion** vs the stock's baseline; ideally a market in an uptrend; tight price near the pivot.
- **Warn / invalidate:** bearish **RSI/momentum divergence** into the highs; prior **failed breakouts** from the same level; heavy **overhead supply** (large prior volume above); a breakout on weak volume (suspect). Stop goes below the pivot / last contraction.
- **Targets:** measured move (base height projected), prior highs, Fib extensions; fundamental fair value as the longer-term cap/magnet.

### 2. Pullback in an uptrend
- **Measure:** the prior up-swing for **Fib retracement** (38.2 / 50 / 61.8); the **MA this stock respects** (from calibration — *not* an assumed 20/50); pullback volume; structure of lows.
- **Confirm:** price reaches the **confluence zone** (Fib ∩ respected MA ∩ prior support) on **light** volume, then a **higher-low / reclaim** candle.
- **Warn / invalidate:** abnormally deep pullback *for this name*; heavy down-volume; loss of the 61.8 retr or the respected MA (trend may be changing → re-classify).
- **Targets:** retest/break of the prior high, then Fib extensions; FV magnet.

### 3. At support / possible bottom
- **Measure:** structural support from prior bases; **Fib retracement/extension of the entire down-leg** to locate where the decline is statistically likely to end; volume (looking for **dry-up**); momentum for **bullish divergence**.
- **Confirm:** support holding *with* volume dry-up, a bullish divergence, and an early **higher-low** or reclaim of a near MA; the **valuation floor** (large fair-value upside) adds conviction to the left-side entry.
- **Warn / invalidate:** "bottom" called with **no** volume change and **no** divergence (likely premature); a break of the support / next Fib level just opens the next leg down — do not average blindly.
- **Targets:** first the down-leg's Fib retracement (38.2/50) as the bounce objective; longer term the fair-value magnet.

### 4. Broken downtrend line — await pullback
- **Measure:** the descending trendline that broke; the break candle's volume; the level that should now act as support on a pullback.
- **Confirm:** a **pullback that holds above the break** and reclaims — *then* enter. Early stage-2 character (reclaiming key MAs) strengthens it.
- **Warn / invalidate:** entering on the **first break** (often retests/fails); a pullback that slices back below the broken line (failed break → back to downtrend).
- **Targets:** the prior consolidation / first major resistance, then Fib extensions; FV magnet.

### 5. Downtrend intact (stage 4) / extended / choppy — no entry
- **Measure (so you know where to watch, not to buy):** **downside targets** from **Fib extensions** of the decline and the **descending channel** (upper and lower lines); the level/structure whose break would change the trend.
- **Action:** **no entry.** Wait for a base to form or a trendline break + pullback confirm (→ condition 4). If fundamentally cheap, the fair-value upside is the reason to *watch*, not yet to *act*.

---

## No clean condition

If nothing classifies cleanly (whipsaw, news-driven gaps, extreme extension), say so plainly: "no actionable technical setup — wait for a base / let the fundamental margin of safety govern sizing." A non-call is a valid, professional output.

---

## Confluence scoring (how to express conviction)

Rate the setup by how many *independent* factors align, e.g.:
- Trend/stage supportive (weekly) · price at a fitted-MA + Fib + structural confluence · volume behaving as the condition requires · momentum **not** diverging adversely · the fundamental fair value pointing the same way.

More aligned factors → higher conviction and a larger (still staged) position; fewer → smaller size, tighter trigger, or wait. Always pair conviction with the **R-multiple** and the explicit **invalidation** from the toolkit.
