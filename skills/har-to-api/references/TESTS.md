# Test log

Run against a local fixture server (`tests/fixture_server.py`) because the
sandbox this was built in blocks direct outbound HTTP. **The live network path
has not been exercised end-to-end — run `tests/smoke_live.sh` on your own
machine before trusting the stockanalysis profile.**

| # | What | Result |
|---|---|---|
| 1 | SvelteKit `__data.json` route survives the noise filter | pass |
| 2 | Query param on every occurrence → flagged; param on one → not | pass |
| 3 | `/compare/AAPL/MSFT/` → `{symbol}` + `{symbol2}`, no collision | pass |
| 4 | 401 responses quarantined, not emitted as endpoints | pass |
| 5 | Cookie value never appears in `endpoints.json` or the profile | pass |
| 6 | Synthetic param-gated route serves HTML → `kind: parse`, body reported | pass |
| 7 | `$HAR2API_AUTH` unset vs HTTP 401 both → `kind: auth`, different detail | pass |
| 8 | `--need segment_mix` refused with a message pointing at the filing | pass |
| 9 | `--use-snapshot` replays identical values with no network | pass |
| 10 | 2.6% cross-provider gap reported; 1.68% stays silent | pass |
| 11 | `--providers a,b` vs `b,a` changes which source wins | pass |
| 12 | `discover.py` emits parseable JSON with no duplicate keys | pass |
| 13 | Real TU `__data.json` payload: resolver rebuilds it, all 28 mapped facts pull correctly | pass |
| 14 | Issuer with the segments section removed: `[id=revenue-segments]` → `None`; positional `[1]` would have returned Cash & Debt | pass |
| — | Full pipeline: parse → discover → fill → fetch → replay → fail offline | pass |

## v1 regressions confirmed

Running the **old** `parse_har.py` on the same HAR:

- kept the 401 gurufocus route as a normal endpoint (`kept: 4` vs v2's `3`)
- produced `/compare/{symbol}/{symbol}/summary` — an unfillable template

## Verified against the real payload

Tests 13–14 run against the **actual** stockanalysis `__data.json` for
`BKK:TU`, captured 2026-08-13 and replayed from a local server (the build
sandbox blocks direct outbound HTTP). Spot checks that passed:

| Fact | Value | Cross-check |
|---|---|---|
| `revenue_ttm` | 135,439,918,000 THB as of 2026-06-30 | matches the site |
| `net_income_ttm` | 4,694,921,000 THB | matches the site |
| `operating_margin_ttm` | 0.04874 | matches the site |
| `segment_revenue.ambient_seafood` | 80,171,273,000 (47.2% of gross) | matches the company's own Q1/2026 release |
| `segment_source` | `spg` | S&P Global, per the payload's `trust.sources` |

So the wire-format handling and the 28 mapped paths are confirmed. What is
**still unverified**: every profile other than stockanalysis. Run
`tests/smoke_live.sh` before relying on those.

---

## v2.1 — live network, four venues (2026-08-21)

The live-HTTP gap noted above is now closed for stockanalysis: these ran
against the **live** site from a networked machine, not the fixture server.

| Ticker | Command | Facts | Fallback | Statement `as_of` |
|---|---|---|---|---|
| GULF.BK | `fetch.py GULF.BK --market bkk` | 137 | 6 | 2026-06-30 |
| TU.BK | `fetch.py TU.BK --market bkk` | 133 | 7 | 2026-06-30 |
| AAPL | `fetch.py AAPL` | 119 | 7 | 2026-06-27 |
| MSFT | `fetch.py MSFT` | 124 | 7 | 2026-06-30 |

Before v2.1 these returned 28 / 35 / **9** / — facts. AAPL's 9 were *all*
fallback: `build_url` substituted `""` into `{market}`, fetched
`stockanalysis.com/quote//AAPL/…`, got a 200 back with a different page shape,
and missed all 138 paths silently. US listings now use
`url_template_no_market`.

### GULF.BK value checks

Cross-checked against the same figures pulled by hand from the four
`__data.json` routes during the `future-compounder` run:

| Fact | Value | Route |
|---|---|---|
| `equity_ttm` | 347,604,239,000 THB | balance_sheet |
| `long_term_investments_ttm` | 433,802,248,000 THB | balance_sheet |
| `net_ppe_ttm` | 115,603,869,000 THB | balance_sheet |
| `operating_cash_flow_ttm` | 21,632,903,000 THB | financials |
| `equity_method_income_cf_ttm` | −24,299,184,000 THB | cash_flow |
| `other_investing_ttm` | 50,138,282,000 THB | cash_flow |
| `dividends_paid_ttm` | −48,553,670,000 THB | cash_flow |
| `cash_interest_paid_ttm` | 13,429,013,000 THB | cash_flow |
| `roce_ttm` | 0.038 | ratios |
| `buyback_yield_ttm` | −0.19189 | ratios |

`equity_method_income_cf_ttm` is the cash-flow **add-back**, so its sign is
inverted relative to the income contribution: −24.3bn here means +24.3bn of
share of profit from associates. Do not read it as a loss.

### New regression tests

| # | What | Result |
|---|---|---|
| 15 | devalue `-1` (undefined) → `None`, not the number −1 | pass |
| 16 | genuinely negative data survives: GULF fcf −3,839,181,000 and capex −25,472,084,000 | pass |
| 17 | `-2`→None, `-3`→NaN, `-4`/`-5`→±inf, `-6`→−0.0 | pass |
| 18 | `bool` not treated as an index (bool subclasses int) | pass |
| 19 | non-finite float never reaches a fact record or snapshot | pass |
| 20 | `GULF.BK` without `--market` refuses rather than fetching the US `GULF` | pass |
| 21 | statement `as_of` borrowed from the financials route, not composed | pass |
| 22 | facts with no known period end carry `as_of: null` + `as_of_status: UNRESOLVED`, never the run date | pass |

Tests 15–19 live in `tests/test_sveltekit_sentinels.py`
(`python tests/test_sveltekit_sentinels.py`).

### Why `as_of` is borrowed rather than derived

Test 21 exists because the obvious implementation is wrong. Balance-sheet and
cash-flow routes label their newest column `"TTM"` instead of a date, but do
expose `fiscalYear` and `fiscalQuarter` — composing a quarter end from those
passes on GULF and fails elsewhere, because fiscal labels are not calendar
quarters:

| | true TTM end | composed from fiscal labels |
|---|---|---|
| GULF | 2026-06-30 | 2026-06-30 ✓ (fiscal = calendar) |
| AAPL | 2026-06-27 | 2026-09-30 ✗ (52/53-week year) |
| MSFT | 2026-06-30 | 2026-12-31 ✗ (**a future date**) |

The four statement routes describe the same TTM window, so the routes without
a date borrow one from `financials` via `as_of_from_route`.
