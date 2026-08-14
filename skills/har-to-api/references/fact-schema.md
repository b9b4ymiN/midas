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
| `as_of` | yes | The data's own date when the response carries one (`as_of_path`), else the fetch date. **These are not the same thing** — a fetch date on a stale figure is misleading. |
| `url` | yes | The exact URL, query string included. Reproducible by hand. |
| `reason` | fallback only | Why the primary source failed. |

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
