# Evidence Base — what is established, assumed, and merely hypothesised

Every claim this skill makes, tagged and sourced. When writing output, use these tags so a reader can tell measurement from inference.

---

## Tags

- **FACT** — published, replicated, or directly computed from data in hand
- **ASSUME** — required for the method to work, not verifiable from public data
- **HYPOTHESIS** — this skill's own untested claim; must be labelled as such in output

---

## FACT

| Claim | Source |
|---|---|
| Days with positive net gamma exposure show no intraday momentum; the effect appears across asset classes and is linked to market-maker hedging | Baltussen, Da, Lammers & Martens, *Journal of Financial Economics* (2021) |
| Effect size on the order of 18bp per 1% move, direction set by market-maker gamma, clearer in large-cap names | Beckmeyer & Moerke (2021) |
| Volatility is heavily suppressed at positive gamma extremes; largest intraday ranges occur when gamma is negative — tested on data back to 2004 | Independent backtest of SqueezeMetrics GEX series |
| Black-Scholes gamma is identical and positive for a call and a put at the same strike (put-call parity); the GEX sign is an inventory assumption, not a Greek property | Chilingarian, "The Sign of Dealer Gamma", SSRN (2026) |
| Flipping the sign convention negates net GEX exactly while leaving vanna, charm and the flip level invariant — verified on a 10,223-contract SPX snapshot | Chilingarian (2026) |
| IV spread and skew predictability falls by at least two-thirds once hard-to-borrow names are excluded — it reflects borrow fees, not private information | Muravyev, Pearson & Pollet, *JFE* (2025) |
| Retail option traders lose on average, roughly 5-9% per position and worse around anticipated volatility events; average spread paid on favoured short-dated contracts around 12.6% | de Silva, So & Smith, *Review of Finance* (2025); Bryzgalova et al. |
| Selling volatility is the most successful strategy for both retail and institutional participants in the sample studied | Hu, Kirilova, Park & Ryu, *Management Science* (2024) |
| 0DTE contracts represented roughly 59% of SPX option volume in 2025 | Cboe |
| Open interest updates once daily, post-close, for all providers | OCC / OPRA |

---

## ASSUME

| Assumption | Why it cannot be verified | What breaks if wrong |
|---|---|---|
| Dealers are long calls and short puts (Model A) | Public data never identifies who holds which side of open interest | The regime read inverts entirely; every magnitude still looks correct |
| Dealers hedge continuously and near-completely | Hedging cadence and completeness are not disclosed | Wall effects are weaker than computed; direction of the read is unaffected |
| Open interest is a usable proxy for current dealer inventory | OI is T-1 and does not capture same-day expiry activity | Intraday reads are stale; end-of-day reads remain usable |
| The single IV inverted per strike applies to both rights at that strike | Bid-ask and microstructure differ between the two | Gamma is slightly misestimated; typically second-order |

The originators of the GEX method acknowledged limits explicitly: in a March 2020 note, SqueezeMetrics observed that when dealers are short gamma their hedging acts as a multiplier on volume rather than a trigger, and that a degree of uncertainty has to be accepted.

---

## HYPOTHESIS — this skill's own untested claim

> **Dealer gamma regime at the single-name level improves the prediction of whether a VCP/SEPA breakout holds.**

The published evidence is **index-level**. Extending it to individual names to filter breakout entries is reasonable but unproven. Label it HYPOTHESIS in every output that leans on it.

### Testing requirements — before this becomes FACT

**Sample size, computed in advance.** To detect a 15-percentage-point difference in failed-breakout rate between regimes (50% baseline vs 35%) at alpha 0.05 and 80% power:

```
n per group = (1.96 + 0.8416)^2 * [0.5(0.5) + 0.35(0.65)] / 0.15^2
            = 7.849 * 0.4775 / 0.0225
            ~= 167
```

**Require >= 170 breakout events per regime bucket (>= 340 total).** Below that, do not run the test — an underpowered result is worse than no result because it will be believed.

**Negative control, mandatory.** Include a skew-based directional signal in the same test harness. Skew is known-dead (see `false-edges.md`). If it shows edge, the pipeline has a bug; stop and find it.

**Pre-committed pass criteria.** Write the accept/reject rule before running. All must hold:

```
[ ] negative control shows no significant edge
[ ] >= 1 hypothesis significant at p < 0.05 with n >= 170 per bucket
[ ] effect size >= 10pp in failed-breakout rate
[ ] direction matches the pre-stated expectation
[ ] result survives a first-half / second-half split
[ ] independently reproduced
```

Failing any one is a fail. Re-running with adjusted parameters until the result is favourable is the most common way this class of test lies.

**Point-in-time discipline.** Never reconstruct historical GEX from current open interest. That is look-ahead in its purest form and will manufacture a large false edge.

---

## Weight cap rationale

Even if the hypothesis passes, GEX contributes **at most 10 of 100** to conviction, into a timing component only.

The reason is asymmetric cost. A missed entry costs an opportunity. A good setup vetoed by a mechanical artefact costs an opportunity *and* corrupts the record used to evaluate the strategy — a rejection that never becomes a trade cannot be measured, so the error is invisible. Keeping the weight low bounds that invisible damage.
