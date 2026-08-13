# Finance provider profiles

Per-site capture recipes and the precedence rules between them.

## Precedence

One fact, one primary source, one cross-check. Two steps pulling the same
number from different providers without knowing it is how a report ends up
disagreeing with itself.

| Fact family | Primary | Cross-check | Fallback |
|---|---|---|---|
| Income statement, balance sheet, cash flow (5y + TTM) | **stockanalysis** | the filing | yfinance |
| Ratios / multiples | **stockanalysis** `/ratios` | gurufocus | compute from statements |
| WACC / cost of capital | **valueinvesting** | compute CAPM | default table |
| Technicals (RSI, ATR, SMA, RelVol, Beta, 52w) | **finviz** | compute from OHLCV | — |
| Price history OHLCV | **stockanalysis** `/history` | yfinance | — |
| ROIC / F-Score / Z-Score | **gurufocus** | compute from statements | — |
| **Segment / revenue mix** | **stockanalysis** (tagged) | **the filing — always** | — |

## Capture order

Do them in this order. Each step is more fragile than the last, so you bank
working coverage before taking on maintenance burden.

1. **stockanalysis** — already verified in `profiles/stockanalysis.json`. No
   capture, no auth. Fill the `facts` maps with `discover.py` and you have a
   working data layer today.
2. **finviz** — no login. Capture a quote page.
3. **valueinvesting** — may be pure SSR. If `parse_har` reports `kept: 0`,
   that *is* the answer: compute WACC from CAPM and label it computed.
4. **gurufocus** — login required, cookie expires. Highest ongoing cost, so
   last. When it starts failing, `fetch.py` will say `AUTH FAILED` rather than
   quietly returning less data.

## stockanalysis — route shapes

| Purpose | Route |
|---|---|
| Resolve a name to venue+symbol | `/api/search?q=` |
| Income statement | `/quote/{market}/{symbol}/financials/__data.json` |
| Balance sheet | `…/financials/balance-sheet/__data.json` |
| Cash flow | `…/financials/cash-flow-statement/__data.json` |
| Ratios | `…/financials/ratios/__data.json` |
| Price history | `/api/symbol/s/{symbol}/history?type=annual\|quarterly\|chart` |
| Screener | `/stocks/screener/__data.json` |

All `__data.json` routes need `?x-sveltekit-trailing-slash=1`. Without it the
server returns the HTML page with a 200 — which is why `parse_har.py` now
tracks required query params, and why `fetch.py` reports a `parse` failure
naming the likely cause instead of a bare JSON error.

- Thai SET: `market` = `bkk`, e.g. `/quote/bkk/TU/financials/`
- US: use `/stocks/{symbol}/financials/` (no `{market}` segment)
- Add `&p=quarterly` for quarterly periods.

**Verified 2026-08-13:** Thai names return five fiscal years plus TTM in THB.

## Segment coverage — what is actually true

stockanalysis **does** return segments, via `__data.json`, under a
`revenue-segments` section. Verified on Thai Union (2026-08-13): five segments
plus eliminations plus a total, five fiscal years and a TTM column, tagged
`source: "spg"` (S&P Global). Ambient Seafood at 47.2% of gross revenue matches
the company's own Q1/2026 release.

Three caveats, all of which the profile encodes rather than assumes away:

1. **The section is absent for issuers the provider has no segment data on.**
   Address it as `sections[id=revenue-segments]`, never `sections[1]` — with
   positional addressing a missing section silently binds the next one and
   hands you Cash & Debt figures labelled as segments.
2. **The labels are the provider's rendering**, e.g.
   `frozen_and_chilled_seafood_and_related_business`. They track the company's
   reporting but are not verbatim, and they change when the company
   re-segments.
3. **History is partial.** Thai Union's segment `ttmPrior` is `null` across
   every segment, so year-over-year segment growth is not available from this
   route alone.

So: use the API mix as the fast path, and confirm it against the filing before
peer selection or driver analysis depends on it. `fetch.py` attaches
`segment_source` and `cross_check_required` to every segment fact so the
obligation travels with the number.


## Rate limiting

These are courtesy limits, not enforced ones — which is exactly why they matter.

- One fetch per ticker per day is plenty; that's what snapshots are for.
- Re-analysis should use `--use-snapshot`, not a fresh pull.
- Never loop a screener over hundreds of symbols without a delay.
- Personal research use. Don't redistribute the raw data.
