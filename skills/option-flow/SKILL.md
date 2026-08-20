---
name: option-flow
description: >
  Read the mechanical hedging pressure sitting in a stock's option chain — dealer gamma
  exposure (GEX), call/put walls, the gamma-flip level, and the implied 1-sigma move — to
  judge whether the market around this name is currently *sticky* (moves get absorbed) or
  *slippery* (moves extend), and to size the stop against the stock's own option-implied
  noise band. Use this whenever the user asks: "option flow on NVDA", "gamma exposure",
  "GEX", "call wall / put wall", "is there a gamma squeeze", "dealer positioning", "where
  will it pin at expiry", "how wide should my stop be", or "will this breakout stick" — on
  its own, or as a follow-up check on an entry zone and stop that came from a technical
  read (e.g. `bf-tech-analysis`). It is deliberately narrow: it answers *sticky or slippery*, never *up or down*.
  It runs a liquidity gate first and REFUSES to emit numbers on a thin chain rather than
  producing plausible noise, declares its sign convention as an explicit written contract
  (the sign is an inventory assumption, not a Greek property), and caps its own weight at
  10/100 in any downstream decision. Free EOD data only — no paid feed required.
  Not financial advice.
---

# Option Flow — Dealer Positioning Read

Reads the **mechanical** layer of price: the buying and selling that option dealers are *obliged* to do as spot moves, regardless of any view on the business. That obligation leaves a measurable footprint on the option chain, and the footprint says whether hedging flows will currently **dampen** moves or **amplify** them.

This is the smallest useful claim, and the skill refuses to make a bigger one:

> **Option flow tells you whether the market is sticky or slippery — never whether it goes up or down.**

It pairs well with any technical read (e.g. `bf-tech-analysis`): technicals produce the entry zone, stop and target; option flow says whether this is a week when a breakout is likely to be absorbed, and whether the proposed stop sits inside the stock's own noise band. It also runs standalone with just a ticker.

**Disclaimer:** Research and educational output only. Not financial advice. Dealer positioning is *estimated from an assumption*, never observed.

---

## Vocabulary (defined inline — this skill is self-contained at runtime)

**Dealer**: the market maker on the other side of retail and institutional option trades. Does not want directional exposure; hedges with the underlying stock continuously.
_Avoid_: whale, smart money, institution

**Sticky / slippery regime**: whether aggregate dealer hedging currently works *against* price moves (sticky — sells rallies, buys dips) or *with* them (slippery — buys rallies, sells dips). The single most defensible output of this skill.
_Avoid_: bullish/bearish regime, long/short gamma (jargon; use only with the plain term attached)

**Wall**: a strike where hedging obligation is concentrated enough to act as a mechanical brake. Requires **both** near-money gamma **and** large open interest — either alone is not a wall.
_Avoid_: resistance, support (walls expire; chart levels do not)

**Sign contract**: the explicitly declared assumption about who holds which side of the inventory. Must be printed in every output. Flipping it negates net GEX exactly while leaving vanna, charm and the flip level unchanged — so a mislabelled sign inverts the regime read while every magnitude still looks correct.
_Avoid_: convention, methodology note

**Noise band**: the option-implied 1-sigma move to the next expiry. A stop placed inside it will be hit by ordinary oscillation rather than by thesis damage.
_Avoid_: expected move, volatility range

**Expiry cliff**: walls belong to one expiry and vanish at its close. Behaviour on the first session *after* expiry is the free experiment that separates mechanical pinning from real supply.
_Avoid_: level break

---

## Inputs

- **Ticker** with correct exchange suffix. US-listed names only — non-US options chains are generally too thin for this to mean anything, and the gate below will say so.
- **Pivot / entry zone and proposed stop**, if you have them from a prior technical read. Without them the skill still produces the regime read but cannot compute wall headroom or run the stop-vs-noise check, and must flag both as unavailable.
- **Option chain** — full chain with strike, expiry, right, open interest, implied volatility, and last/bid/ask, for every expiry ≤45 DTE. `scripts/gex_scan.py` fetches this live via `yfinance` by default.

> **Pin the spot price if you have a more authoritative one.** Option chains
> move intraday; if this ticker's price was already pulled elsewhere in the
> same session (a snapshot, a chart read), pass it through with `--spot` so
> the regime math and any downstream report agree on one number instead of
> disagreeing by whatever moved between two pulls minutes apart:
>
> ```bash
> python scripts/gex_scan.py TICKER --spot 123.45 --pivot 120 --stop 118
> ```
>
> The option chain itself still comes from the live fetch (or `--snapshot` for
> a known-answer chain file, schema in `tests/fixture_*.json`) — only the spot
> quote is overridable. Anything sourced from a different snapshot than the
> rest of an analysis must be flagged as such.

---

## Step 1: Run the liquidity gate — BEFORE computing anything

**This step is blocking. It is the most important step in the skill.** GEX computed on a thin chain is noise wearing the costume of a signal, and once a number reaches the page it will be used regardless of any caveat attached to it.

```
near_band  = strikes within ±10% of spot
near_oi    = total open interest in that band
n_strikes  = priced strikes in that band

PASS   near_oi ≥ 2,000  AND  n_strikes ≥ 8
FAIL   → emit UNRELIABLE. Do not compute walls. Do not compute a regime.
         Say which of the two thresholds failed and by how much.
```

On FAIL the skill's entire output is one line stating the chain is too thin to read, plus the two counts. **Do not soften this into a number with a warning label.** Full tiering and the rationale in `references/liquidity-gates.md`.

---

## Step 2: Declare the sign contract, then compute

The sign attached to calls and puts is **not** a property of the Greek. Black-Scholes gamma is identical and positive for a call and a put at the same strike — a direct consequence of put-call parity. The sign is therefore an *inventory assumption*, and it must be written down.

**Contract used (Model A — the SqueezeMetrics open-interest proxy):** dealers are assumed long calls and short puts. Calls carry a positive sign, puts negative.

```
strike_gex = gamma × open_interest × 100 × spot² × 0.01
             calls positive · puts negative
net_gex    = Σ strike_gex over all strikes, all expiries ≤45 DTE
```

Implied volatility is inverted from the **OTM side only** — puts for strikes below spot, calls for strikes above — because deep-ITM options carry almost no vega and invert to unstable values. Method and code in `references/gex-method.md`.

Then derive:

| Output | Definition |
|---|---|
| `regime` | sign of `net_gex` → STICKY (positive) or SLIPPERY (negative) |
| `call_wall` | strike with maximum positive net GEX |
| `put_wall` | strike with most negative net GEX |
| `gamma_flip` | spot level where net GEX changes sign (sweep spot ±25%) |
| `noise_band_1sd` | spot × ATM IV × √T to nearest expiry |
| `wall_headroom` | (call_wall − pivot) / pivot, if a pivot was supplied |
| `data_quality` | HIGH / MED, plus `near_oi` and `n_strikes` |

---

## Step 3: Run the masking test — the built-in negative control

A sign inversion is the one bug in this class of computation that **survives inspection**: every magnitude stays correct while the regime read flips. Inspection therefore cannot catch it; only a test can.

```bash
python skills/option-flow/scripts/verify_sign.py [TICKER]
```

The test asserts that flipping the contract **negates net GEX exactly** while leaving the flip level and per-strike gamma magnitudes unchanged. If flipping the sign changes anything else, the implementation is wrong — stop and fix it before reading any output.

---

## Step 4: Read the map — four questions, in this order

1. **Sticky or slippery?** The sign of net GEX. This is the headline and the only claim with index-level published support behind it.
2. **How much headroom to the first wall?** Distance from the pivot to `call_wall` as a percentage. Small headroom means a breakout is entering the densest mechanical selling immediately.
3. **Is the downside hollow?** Compare the magnitude of the put wall to the call wall. Heavy above with nothing below is a real asymmetry and must be stated — it does not predict a fall, it says a fall would arrive without mechanical cushioning.
4. **Does the stop clear the noise band?** If the proposed stop distance is inside `noise_band_1sd`, it will be hit by ordinary oscillation. This is the most concretely actionable output the skill produces.

Then note **days to the nearest expiry**. Walls are strongest just before expiry and gone the session after. Say so explicitly whenever DTE ≤ 5.

---

## Step 5: Say what it cannot say — mandatory section

Every output carries these, not as boilerplate but because each has bitten a real analysis:

- **The sign is an assumption.** Public data never identifies who holds which side.
- **Open interest is T−1.** True of every provider, including expensive ones. Same-day expiry volume does not appear in OI until the day closes, so this is an end-of-day picture.
- **Walls expire.** They are not chart resistance and do not persist.
- **No directional claim.** Sticky is not bearish. A real catalyst moves price straight through a wall; the wall only raises the force required.

If any input was degraded (stale option prices against live spot, IV inverted from minimum-tick quotes, fallback data source), name the specific field and mark it LOW CONF rather than lowering the whole output's confidence generically.

---

## Step 6: Hand off with a capped weight

If this output feeds into a broader conviction score or investment decision elsewhere, contribute **at most 10 of 100**, and only into a *timing* component — never into stock selection, never into valuation. Above that weight, mechanical noise starts vetoing good setups. State the weight in the output so anything downstream can see the cap.

The regime modifies **size and patience**, not the decision to own the business.

---

### Output format

```
# Option Flow — [Company] ([Ticker])
Sign contract: Model A (dealers long calls / short puts) · Data: [source] · OI as of [date]

## Gate
[PASS · near-money OI n across k strikes] or [UNRELIABLE — chain too thin: n OI / k strikes]

## Regime
[STICKY / SLIPPERY] · net GEX [value] per 1% move
[one plain sentence on what that means for a breakout this week]

## Map
call wall [strike] ([value], [±%] from spot) · put wall [strike] ([value])
gamma flip [level or "none within ±25%"] · nearest expiry [date, n DTE]
[the ladder of walls above/below, if there is one]

## Risk geometry check
noise band 1sd: ±[value] ([%]) → [low]–[high]
proposed stop [level]: [clears / sits inside] the noise band
wall headroom from pivot [pivot]: [%]

## Asymmetry
[heavy above / hollow below, or symmetric, with the two magnitudes]

## What this cannot say
[sign assumption · OI is T-1 · walls expire · no directional claim · any LOW CONF fields]

## Timing verdict
[one line: how this modifies entry timing and stop, if a technical read supplied them — weight ≤10/100]

## Disclaimer
Research and educational output only. Not financial advice.
```

---

## Caveats

- The published evidence for regime effects is strongest at **index level** (SPY/QQQ). Applying it to a single name to predict whether *that* breakout holds is a reasonable hypothesis, **not** an established result — label it as such.
- Three widely-sold signals are dead and this skill must never use them: max pain as a magnet, IV skew as a directional signal, and "following the flow." Evidence and citations in `references/false-edges.md`.
- A chain that passes the gate can still mislead if its open interest is overwhelmingly deep-ITM legacy positions carrying near-zero gamma. Check the near-money share, not just the total.
- Free EOD data is sufficient for everything in this skill. Paid feeds buy intraday refresh and trade-level classification, neither of which changes any output above.

---

## Reference Files

- `references/gex-method.md` — The formulas, the sign contract in full, OTM-only IV inversion, gamma-flip solving (portfolio root vs per-strike approximation), and the wall/ladder derivation, with code.
- `references/liquidity-gates.md` — Gate thresholds and why these numbers, the HIGH/MED/UNRELIABLE tiering, the near-money-share check for deep-ITM legacy OI, and the refusal rules.
- `references/false-edges.md` — What is dead, why, and the citation for each: max pain, IV skew/spread, following visible flow. Read before adding any new metric to this skill.
- `references/evidence-base.md` — Every claim this skill makes, tagged FACT / ASSUME / HYPOTHESIS with its source, and the sample-size and negative-control requirements for testing whether the single-name hypothesis holds.
