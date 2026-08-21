# Fact record schema

The contract between `fetch.py` and everything downstream. A number without
these fields should be treated as absent, not as zero.

## Record

```json
{
  "value": 134984000000,
  "unit": "THB",
  "source": "stockanalysis",
  "tier": "primary",
  "as_of": "2026-03-31",
  "url": "https://stockanalysis.com/quote/bkk/TU/financials/__data.json?x-sveltekit-trailing-slash=1"
}
```

| Field | Required | Meaning |
|---|---|---|
| `value` | yes | The number or string as returned. Never rounded, never scaled. |
| `unit` | when known | From the profile's `units` map. Currency codes, `%`, `ratio`, `index`. |
| `source` | yes | Provider name — matches the profile's `provider`. |
| `tier` | yes | `primary` or `FALLBACK`. Anything `FALLBACK` must stay visibly flagged downstream. |
| `as_of` | yes | The data's own reporting date, from `as_of_path` or borrowed via `as_of_from_route`. `null` when the response carries none — **never** the fetch date, which would assert the figure is current. A live-quote fallback is the one case where the run date genuinely is the as-of. |
| `as_of_status` | when unknown | `UNRESOLVED`, present only when `as_of` is `null`. The figure's vintage is unknown, not today. |
| `url` | yes | The exact URL, query string included. Reproducible by hand. |
| `reason` | fallback only | Why the primary source failed. |

### Where `as_of` comes from

A route can name its own date with `as_of_path`. When the newest column is
labelled something other than a date — stockanalysis writes literally `"TTM"`
on balance-sheet, cash-flow and ratios — the route names a sibling instead:

```json
"as_of_from_route": "financials"
```

Do **not** compose a date from `fiscalYear` + `fiscalQuarter`. Fiscal labels
are not calendar quarter ends, and the failure is silent: on 2026-08-21 MSFT
reported FY2026 Q4, which composes to `2026-12-31` — a date in the future,
when the real TTM end was `2026-06-30`. AAPL's 52/53-week year ended
`2026-06-27`, not on any quarter boundary at all.

## Statement template

`fetch.py` emits a `statement_template` fact on every run: `insurance`,
`bank`, `utility`, or `standard`.

A ratio can be arithmetically correct and economically meaningless. ROIC on an
insurer divides by liabilities that are the company's *raw material*, not its
financing — Ping An's 6.29% answers no question anyone has. P/FCF of 1.36x
does not mean cheap when the operating cash flow is mostly policyholder money
the company must hand back.

Detection is a lookup rather than a guess, because the provider stamps the
template it rendered into its own field names. Verified live 2026-08-21:

| Issuer | Suffix | Marker fields | Template |
|---|---|---|---|
| Ping An (SHA:601318) | `Ins` ×9 | policyLoans, reinsuranceRecoverable, separateAccountAssets | insurance |
| Ping An Bank (SHE:000001) | `Bank` ×12 | grossLoans, totalDeposits | bank |
| GULF (BKK) | `Uti` ×18 | — | utility |
| TU (BKK), AAPL | none | — | standard |

For `insurance` and `bank` the run also warns, naming every fact whose meaning
does not survive the template — 29 of them on Ping An, 13 on Ping An Bank —
and naming what to use instead: new business value and margin, contractual
service margin, embedded value and solvency ratios for a life insurer; net
interest margin, cost/income, NPL and CET1 for a bank; and for both, return on
equity computed on equity **attributable to owners**.

The facts are labelled, never dropped. Removing them silently would be making
the reader's judgement for them, which is the habit this layer exists to break.

## Equity: whose equity?

Two facts, easily confused, and the confusion is expensive:

| Fact | Contains | Use for |
|---|---|---|
| `equity_ttm` | Total group equity, **including** minority interest | Group-level leverage |
| `common_equity_ttm` | Equity **attributable to owners** | ROE, book value per share, price/book |

On Ping An these read 1,454,080 and 1,028,084 CNY million — **41% apart**,
because minorities are 29.3% of group equity and rising from 24.6% in 2021.
`equity_ttm` reads like "the equity" and is the one a report reaches for, which
produces a per-share figure that belongs to somebody else.

The provider makes the same mistake: its own `pb_ratio` is computed on group
equity, giving 0.638x on Ping An where price to *owners'* book is 0.90x.

**Rule:** any per-share metric, any ROE, and any price-to-book uses
`common_equity_*`. Check the gap between the two before quoting either.

## Alias groups

Top level of a profile, optional:

```json
"fact_aliases": {
  "pe": ["pe_ratio", "trailing_pe"],
  "cash": ["cash_and_investments", "total_cash"]
}
```

`check_conflicts` compares the same measurement **across providers** and warns
past a 2% gap. It groups on the fact name, so two providers naming one
measurement differently were never compared at all. On GULF.BK (2026-08-21)
stockanalysis `pe_ratio` = 25.27 and yfinance `trailing_pe` = 35.61 — 41%
apart, and silent until these groups existed.

Two rules for membership:

1. **Same measurement at the same date.** Never group a TTM fact with its
   `_fy0` counterpart; that pair always differs and the warning is pure noise.
2. **Cross-provider only.** Facts from one provider inside a group are not
   compared against each other, which is what makes rule 1 enforceable.

Groups merge across every loaded profile, so an alias declared once applies to
the whole run.

## Envelope

```json
{
  "ticker": "TU.BK",
  "market": "bkk",
  "fetched_at": "2026-08-13T22:59:27+07:00",
  "fact_count": 3,
  "fallback_count": 0,
  "facts": { "...": {} },
  "failures": [ {"provider":"gurufocus","route":"op1","kind":"auth","detail":"..."} ],
  "warnings": [ "..." ],
  "contract": { "...": "..." }
}
```

`failures` and `warnings` are part of the payload, not console noise. A
consumer that renders the facts and drops the warnings has thrown away the
part that says how much to trust them.

## Failure kinds

| `kind` | Means | What to do |
|---|---|---|
| `auth` | 401/403, or `$HAR2API_AUTH` unset | Log in, re-capture, update the env var |
| `notfound` | 404 | The route moved, or this symbol isn't covered |
| `network` | timeout / DNS / connection (retried twice) | Retry later |
| `parse` | response wasn't JSON | Read the reported body. HTML means the route moved, the query string is incomplete, or it's an interstitial — open it in a browser rather than guessing |

## Naming

Snake case, period-suffixed where it matters: `revenue_ttm`, `revenue_fy2025`,
`operating_margin_ttm`, `roic`, `shares_diluted`, `goodwill`, `rsi_14`.

Names matching `segment`, `revenue_mix`, `revenue_by`, `business_unit` or
`division` get two extra fields:

| Field | Meaning |
|---|---|
| `segment_source` | The provider's own source tag for the segment block (`spg` = S&P Global on stockanalysis). `"unknown"` if the route does not declare one. |
| `cross_check_required` | Standing note that the mix must be confirmed against the filing before downstream use. |

See SKILL.md rule 4.
