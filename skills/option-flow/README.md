# option-flow

Reads the **mechanical** layer of price — the hedging that option dealers are obliged to do as spot moves — and answers one narrow question:

> Is the market around this name currently **sticky** (moves get absorbed) or **slippery** (moves extend)?

It never answers *up or down*.

## Where it sits

Standalone. Run it on its own for a regime read on any US-listed ticker, or as a follow-up check on an entry zone and stop produced by a technical read (e.g. `bf-tech-analysis`) — this skill says whether hedging flows will fight a breakout this week, and whether the proposed stop sits inside the stock's own option-implied noise band.

A gate failure is a **normal outcome**, not an error.

## Quick start

```bash
# standalone, free yfinance chain
python scripts/gex_scan.py VLO NVDA SCHW

# with a pivot/stop from elsewhere, and a spot price pinned to match another source
python scripts/gex_scan.py VLO --spot 347.95 --pivot 320 --stop 337.50

# known-answer chain file instead of a live fetch (schema: tests/fixture_*.json)
python scripts/gex_scan.py --snapshot tests/fixture_vlo_20260818.json --pivot 320 --stop 337.50

# the masking test -- run this before trusting any output
python scripts/verify_sign.py --fixture tests/fixture_vlo_20260818.json

# full suite, no network
bash tests/test_gex_scan.sh
```

Requires `numpy`, `scipy` (this skill's one dependency beyond the stdlib scripts used elsewhere in this repo); `yfinance` only for the live-fetch path.

## Three design decisions worth knowing

**1. The gate refuses rather than caveats.** A chain below 2,000 near-money contracts or 8 priced strikes returns a refusal line and nothing else — no greyed-out estimate. A number that reaches the page gets used regardless of the warning attached to it, so the only effective control is to withhold it.

**2. The sign is a declared contract, not a fact.** Black-Scholes gamma is identical and positive for a call and a put at the same strike, so the call-positive/put-negative sign is an *inventory assumption*. Flipping it negates net GEX exactly while leaving every magnitude and the flip level unchanged — meaning a mislabelled sign inverts the regime read with no visible symptom. `verify_sign.py` is the only thing that can catch this; inspection cannot.

**3. Weight is capped at 10/100.** This is a timing filter, not a stock picker. Above that weight, mechanical noise starts vetoing good setups — and a vetoed setup never becomes a trade, so the error is invisible in the track record.

## What it deliberately does not do

Max pain, IV skew as a directional signal, and "following the flow" are all excluded. Each was tested and found to be an artefact or a losing population — see `references/false-edges.md` for the evidence and citations. Do not re-derive a dead result.

## Status of the central claim

The regime effect has published support at **index level**. Using it on a **single name** to filter breakout entries is this skill's own hypothesis and is **untested** — it must be labelled HYPOTHESIS in output. `references/evidence-base.md` carries the sample-size calculation (>= 170 events per regime bucket), the mandatory negative control, and the pre-committed pass criteria for promoting it to FACT.

## Files

| Path | Purpose |
|---|---|
| `SKILL.md` | The skill: gate, sign contract, four-question read, output format |
| `references/gex-method.md` | Formulas, OTM-only IV inversion, flip solving, walls and ladder, with code |
| `references/liquidity-gates.md` | Thresholds and why, HIGH/MED/UNRELIABLE tiering, refusal rules |
| `references/false-edges.md` | What is dead, why, and the citation for each |
| `references/evidence-base.md` | Every claim tagged FACT/ASSUME/HYPOTHESIS + testing requirements |
| `scripts/gex_scan.py` | The computation |
| `scripts/verify_sign.py` | The masking test |
| `tests/fixture_vlo_20260818.json` | Real VLO chain, 21 Aug 2026 expiry — known-answer fixture |
| `tests/test_gex_scan.sh` | 13 assertions, no network |

The fixture is deliberately a **degraded** chain (prior-close option prices against live spot), so the tests exercise the MED tier rather than only the happy path.

---

Research and educational output only. Not financial advice.
