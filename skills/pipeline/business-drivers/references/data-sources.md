# Where to find each driver

Only after Step 1 and Step 2. Searching before the drivers are named produces a
generic list dressed in citations.

## By driver type

| Driver | Prefer | Notes |
|---|---|---|
| Exchange-traded commodity | **futures / forward curve** | Damodaran prefers market prices over analyst forecasts — no career risk attached. The curve also gives the time path free. |
| Non-exchange commodity (e.g. tuna) | trade press, industry association, the company's own disclosure | Often no public index; the company's commentary may be the best available source. Say so. |
| FX | forward curve for the specific pair | The pair that matters is buy-vs-sell currency, not the reporting currency. |
| Interest rates | forward curve / policy path | For the currency the debt is actually in. |
| Freight | published route indices | Route-specific, not global averages. |
| Tariffs and policy | primary announcements, then trade press | Dates matter as much as levels — they become catalysts. |
| Wages | national statistics, sector agreements | Slow-moving; usually a headwind, rarely a catalyst. |
| Demand proxies | the customer industry's own volumes | Better than macro GDP for a supplier. |

## Preference order

1. **Market prices** — futures, forwards, published indices. No forecaster bias.
2. **The company's own disclosure** — sensitivity tables in the filing beat any
   estimate you construct. Check for them before computing your own.
3. **Industry sources** — associations, trade press.
4. **Computed from cost structure** — what `sensitivity.py` does. Label it as
   computed.
5. **Analyst estimates** — last, and note the bias.

## The rule that carries over

Every driver figure carries the same obligation as every other number in this
pipeline: **source, as-of date, and reproducibility**. A tuna price with no date
is unusable three weeks later, and a driver analysis nobody can re-run is a
snapshot, not a tool.

Where the data layer can supply it, take it through `har-to-api`'s `fetch.py` so
the provenance comes attached. Where it cannot — and for most non-exchange
commodities it cannot — record the source and date by hand, and mark the figure
as manually sourced so downstream steps know its standing.
