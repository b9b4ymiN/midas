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

Every browser request to a `__data.json` route carries
`?x-sveltekit-trailing-slash=1`, so the profiles send it too. It is **not
required**: verified live on 2026-08-14 that the same route without it returns
the same JSON. Send it anyway — matching the browser is the cheaper default —
but do not treat its absence as the explanation when a route stops working.

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

### The gap is now a number, not a reminder

A standing note to "cross-check against the filing" never said how far off the
figures already were, so nobody found out without doing the arithmetic by
hand. Every segment fact now also carries:

| Field | Meaning |
|---|---|
| `segment_sum` | The parts, summed. Rows matching `(^\|_)total(_\|$)` are excluded — they are the provider's own summary row, and summing one in doubles the figure. |
| `segment_declared_total` | The provider's total when the payload has one, else `null`. |
| `segment_vs_revenue_delta_pct` | Parts vs the declared total when there is one, otherwise vs `revenue_ttm`. |

Past threshold this raises a warning. Two thresholds, because the two cases
support different checks: **±5%** when the payload declares its own total (the
parts can be verified against it directly, so only a real mismatch matters),
**±2%** when it does not (the only check available is against revenue, and a
material gap there means parts are missing).

Verified live on 2026-08-21:

| Ticker | Parts | Declared total | Delta | Warns |
|---|---|---|---|---|
| TU.BK | 135,439,918,000 | 135,439,918,000 | 0.00% | no |
| AAPL | 466,823,000,000 | 466,823,000,000 | 0.00% | no |
| MSFT | 331,839,000,000 | 331,839,000,000 | 0.00% | no |
| GULF.BK | 149,340,000,000 | *none* | **+4.81%** | yes |

GULF is the case that motivated this. Its breakdown carries no eliminations
line and no declared total, so the parts overstate revenue by 4.81% with
nothing in the payload to reconcile against — the mix cannot be presented as
complete without the filing. Its FY2025 column is worse, summing roughly 24%
*below* reported revenue.

Before the total rows were excluded, TU and AAPL both read as exactly +100%
off. Two unrelated issuers landing on the same round number is the shape of a
bug in the checker, not a finding about the data.


## Rate limiting

These are courtesy limits, not enforced ones — which is exactly why they matter.

- One fetch per ticker per day is plenty; that's what snapshots are for.
- Re-analysis should use `--use-snapshot`, not a fresh pull.
- Never loop a screener over hundreds of symbols without a delay.
- Personal research use. Don't redistribute the raw data.
