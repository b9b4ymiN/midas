# False Edges — what is dead, and why

Read before adding any metric to this skill. Each item below was widely believed, is widely sold, and has been tested and found wanting. The skill must not use any of them.

---

## 1. Max pain as a price magnet — DEAD

**The claim:** price gravitates toward the strike that maximises aggregate option-holder loss.

**Why it fails:** max pain is computed from open interest that accumulated at past prices. When a stock has trended, OI sits where the stock *used to be*, and max pain becomes a fossil rather than a magnet.

**Worked example (VLO, 18 Aug 2026, spot $347.95).** Max pain sat below spot at *every single expiry*:

| Expiry | Max pain | Distance from spot |
|---|---|---|
| 21 Aug 2026 | $307.50 | -11.6% |
| 18 Sep 2026 | $270.00 | -22.4% |
| 18 Dec 2026 | $320.00 | -8.0% |
| 15 Jan 2027 | $195.00 | -44.0% |

A "magnet" pointing 44% down on a stock at all-time highs is not a signal. It is a record of where option buyers positioned before the move.

**Residual validity:** pinning near very large OI strikes in the final hours before expiry is a real, separately documented effect — but that is *near-money gamma pinning*, which this skill already captures through the wall computation. It is not max pain.

---

## 2. IV skew / IV spread as a directional signal — DEAD

**The claim:** the gap between put and call implied volatility, or between implied and historical volatility, predicts stock returns.

**Why it fails:** the effect was real in the data and had a mundane cause. Published 2025 work in the *Journal of Financial Economics* (Muravyev, Pearson & Pollet) showed the predictability is largely an artefact of **stock borrow fees** that standard IV calculations omit. Excluding hard-to-borrow names removes at least two-thirds of it. The authors describe the remaining public-data predictability as not exploitable in practice.

**Consequence for this skill:** IV is used here **only** to compute gamma and the noise band. It is never used as a directional input.

**Consequence for testing:** because skew is known-dead, it makes an excellent **negative control**. Any backtest of this skill's hypotheses should include a skew-based directional signal. If that signal shows edge, the pipeline has a bug — look-ahead, survivorship, or point-in-time contamination. See `evidence-base.md`.

---

## 3. "Following the flow" / unusual options activity — DEAD

**The claim:** large or unusual option trades reveal informed positioning worth copying.

**Why it fails on two counts:**

*Identification.* Free and retail-priced data show volume, not who initiated or whether the trade opened or closed a position. A large print is equally consistent with an opening bullish bet, a closing sale, a hedge leg, or a spread. The classification that made the original academic result work (buy-to-open volume) requires exchange Open-Close reports priced at roughly $600/month per exchange for end-of-day, considerably more for intraday.

*Population.* Even correctly identified, most visible option flow is not informed. Published work finds retail option traders lose on average — of the order of 5-9% per position, worse around anticipated high-volatility events — while paying average bid-ask spreads around 12.6% on the short-dated contracts they favour. "Following the flow" is frequently following the losing side.

**Consequence:** this skill reads *positioning* (open interest, which is a fact) and never *flow* (trade-level inference, which is not available).

---

## 4. Things to be suspicious of, not yet dead

Not banned, but require evidence before being added:

- **Vanna / charm levels.** Mechanically real and computable from the same chain. But they add parameters without adding an independent testable claim, and the sign-contract problem applies to them identically. If added, they need their own negative control.
- **DIX / dark-pool prints.** Different data lineage, different assumptions, not free at useful granularity.
- **Single-name regime as a return predictor.** The regime effect has published support at index level. Applying it to predict whether *this* breakout holds is this skill's central hypothesis and is explicitly untested — see `evidence-base.md`.

---

## The general rule

Before adding a metric to this skill, answer three questions in writing:

1. What specific, falsifiable claim does it make?
2. What data would show it false, and do we have that data?
3. Has someone already tested it? (If yes and it failed, stop. Do not re-derive a dead result.)

A metric that cannot answer (1) is decoration.
