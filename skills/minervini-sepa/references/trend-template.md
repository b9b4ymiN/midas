# Gate 2 — Trend Template: 8 Iron Rules

The second gate of SEPA. This is the filter that keeps me out of downtrends and falling knives. A stock **must pass all 8 rules** — passing 7 out of 8 is still a cut. The discipline *is* the edge; "close enough" is how people lose money.

These rules collectively identify a confirmed **Stage 2 uptrend** (Weinstein stage analysis: 1 base / 2 advance / 3 top / 4 decline). I only play Stage 2. Stages 1, 3, and 4 are not buyable for me — Stage 4 especially is where falling knives live.

---

## The 8 iron rules

Pull daily data and compute. Each rule is a hard yes/no.

| # | Rule | Test | What it confirms |
|---|---|---|---|
| 1 | Price above MA150 **and** MA200 | `Price > MA150` AND `Price > MA200` | Long-term uptrend intact |
| 2 | MA150 above MA200 | `MA150 > MA200` | Medium-term trend stronger than long-term |
| 3 | MA200 trending up ≥ 1 month | `MA200_slope > 0` over ≥ 20-22 trading days | The foundation is rising, not flat |
| 4 | MA50 above MA150 and MA200 | `MA50 > MA150 > MA200` | Short-term momentum aligned bullish |
| 5 | Price above MA50 | `Price > MA50` | Not in a deep short-term correction |
| 6 | Price ≥ 30% above 52-week low | `Price ≥ 52w_Low × 1.30` | Momentum is real, not a dead-cat bounce |
| 7 | Price within 25% of 52-week high | `Price ≥ 52w_High × 0.75` | Near the highs — not extended, not laggard |
| 8 | Relative Strength Rating ≥ 70 | `RS ≥ 70` (love ≥ 85) | Outperforming the market, not drifting |

**All 8 must be ✓.** One ✗ and Gate 2 fails → I walk. No exceptions for "but the chart looks good."

---

## Relative Strength (RS) — how to compute it

RS Rating measures a stock's price performance against the market (e.g. SET Index, S&P 500, NASDAQ) over the trailing 12 months, **double-weighting the most recent 3 months** because recent leadership matters more than stale leadership.

**Weighting scheme:**

| Period | Weight | Multiplier |
|---|---|---|
| Last 3 months | 40% | ×2 (double-weighted) |
| 3-6 months ago | 20% | ×1 |
| 6-9 months ago | 20% | ×1 |
| 9-12 months ago | 20% | ×1 |

**Procedure:**
1. Compute the stock's % price change for each of the four 3-month windows.
2. Compute the same for the market index.
3. Compare stock vs index per window, apply the weights above.
4. Rank the result against the full universe of market stocks → percentile.
5. RS Rating = that percentile (0-100).

A stock with RS 85 is outperforming 85% of the market — a leader. RS 70 is the floor; below that, I don't care how good the fundamentals are, the market isn't confirming it.

> **Practical note:** in a pinch, a simple 1-year price % change ranked against peers is a decent RS proxy. The double-weighted version is more accurate for catching *current* leaders. Flag the method used and its approximation if the full universe rank isn't available.

---

## Stage classification — why the 8 rules reduce to "Stage 2 only"

The Trend Template is really a **Stage 2 detector**. Understanding the stages tells you what a failure means:

| Stage | Description | MA structure | My action |
|---|---|---|---|
| **1 — Basing** | Consolidating after a decline; MAs flattening, price chopping sideways | MA200 flat/slightly down, price below or around MAs | Watch. Not buyable yet. |
| **2 — Advancing** | Confirmed uptrend; price leading, MAs stacked and rising | Price > MA50 > MA150 > MA200, all rising | **The only stage I buy.** |
| **3 — Topping** | Advance exhausted; price chopping around highs, MAs losing slope | Price around MA50, MAs flattening | Sell/avoid. Distribution often here. |
| **4 — Declining** | Downtrend; price below falling MAs | Price < MA50 < MA150 < MA200, falling | **Never.** This is where falling knives cut. |

A stock that passes all 8 rules is, by construction, in Stage 2. A failure on rules 1-5 usually means it has slipped into Stage 3 or 4. Rule 6/7 failures mean it's either too early (Stage 1) or too laggard. Rule 8 failure means it's Stage 2 in price structure but *not a leader* — and I want leaders.

---

## Verdict for Gate 2

- **PASS** — all 8 rules ✓. The stock is a confirmed Stage 2 leader. Proceed to Gate 3.
- **FAIL** — any rule ✗. State which one and the value. Then classify the stage:
  - If Stage 1 → "forming a base, revisit when it breaks out and the MAs stack."
  - If Stage 3 → "topping — avoid, distribution risk."
  - If Stage 4 → "downtrend — never catch this falling knife."
  - If Stage 2 but RS < 70 → "right structure, wrong leadership — wait for RS to improve or pick a stronger name."

**One rule I never bend:** I do not buy Stage 4. A stock that dropped from 100 to 50 can easily drop another 50%. "It's cheap now" is not a Trend Template rule.

---

## Data requirements & caveats

- **Moving averages** — use SMA (simple) for the classic Template; daily closes. MA50/150/200 on daily data. For the slope check (Rule 3), compare today's MA200 to its value 20-22 trading days ago.
- **52-week high/low** — use the trailing 252 trading days. Adjust for splits; do not adjust for dividends for this purpose (price action is what matters here).
- **RS** — needs the market index for the same ticker's exchange. Flag if computed as an approximation rather than a full-universe percentile rank.
- **Thin / new listings** — if a stock has less than ~1 year of history, MA200 and the 52-week range are unreliable. Flag low confidence and do not force a PASS on incomplete data.

---

> **Source:** Compiled from *Think & Trade Like a Champion*, *Trade Like a Stock Market Wizard*, *Mindset Secrets for Winning*. The 8 rules and RS weighting are verbatim from the books. Educational use, not financial advice.
