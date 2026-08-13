# Test log

Run against a local fixture server (`tests/fixture_server.py`) because the
sandbox this was built in blocks direct outbound HTTP. **The live network path
has not been exercised end-to-end — run `tests/smoke_live.sh` on your own
machine before trusting the stockanalysis profile.**

| # | What | Result |
|---|---|---|
| 1 | SvelteKit `__data.json` route survives the noise filter | pass |
| 2 | Query param on every occurrence → `required: true`; param on one → `false` | pass |
| 3 | `/compare/AAPL/MSFT/` → `{symbol}` + `{symbol2}`, no collision | pass |
| 4 | 401 responses quarantined, not emitted as endpoints | pass |
| 5 | Cookie value never appears in `endpoints.json` or the profile | pass |
| 6 | Missing required query param → server serves HTML → `kind: parse` with cause named | pass |
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
**still unverified**: the live HTTP path from a machine with real network
access, and every profile other than stockanalysis. Run `tests/smoke_live.sh`
before relying on either.
