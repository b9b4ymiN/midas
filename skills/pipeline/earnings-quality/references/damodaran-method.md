# Damodaran's normalisation method — the full version

Sources: Damodaran, *More on normalizing earnings* (NYU Stern) and *Ups and
Downs: Valuing Cyclical and Commodity Companies*.

## The two methods

### 1. Average absolute earnings

Take the mean of the last N years' earnings and use it as the base.

Damodaran's licence for this is narrow and explicit: it works **"for firms that
have not changed in scale (or size) over the period."** Applied to a company
that grew or shrank across the window, it produces an incorrect estimate — a
company that tripled its revenue gets a base drawn mostly from the years when
it was a third of its current size.

`normalize.py` measures revenue drift across the window and marks this method
**not applicable** above 20%.

### 2. Average margin (or return on capital) × current revenue (or capital)

Take the mean operating margin over the window, apply it to **current**
revenue.

Two advantages Damodaran names:

- It **reflects the firm's current size**, so growth or contraction during the
  window does not corrupt the base.
- Revenues are **"less susceptible to manipulation by accountants"** than
  earnings. Starting from the cleanest line and multiplying by a cycle-average
  margin means one-off items are excluded *by construction* rather than by
  successful detection.

The same logic applies with return on capital in place of margin, applied to
current invested capital — use that variant when the business is capital-driven
rather than margin-driven.

## Choosing the window

Damodaran: averaging "should occur over a period long enough to cover an entire
cycle" — framed as **5 to 10 years**, with the caveat that cycles range from
2–3 years to over 10 in mature economies. There is no universal number.

Practical reading:

| Industry character | Window |
|---|---|
| Consumer staples, utilities, healthcare | 5 years is usually enough |
| Industrials, chemicals, shipping | 7–10 years |
| Commodities, semiconductors, property | 10 years, and check where in the cycle both ends sit |
| Anything restructured or re-segmented mid-window | Shorter window + a note that the base is provisional |

A window that starts and ends at the same point in the cycle is worth more than
a longer one that starts at a trough and ends at a peak.

## Commodity price assumptions

For commodity-exposed businesses, Damodaran offers two routes and states a
preference:

1. Long-term **inflation-adjusted average price**
2. **Forward and futures market prices**

He prefers the market-based route, on the grounds that it removes analyst bias
and carries a built-in hedging mechanism.

This connects directly to `business-drivers`: that step identifies *which*
commodity actually drives the company's earnings; this step takes the futures
curve for that commodity rather than assuming the obvious one.

## The three traps, in his words

### Trap 1 — incomplete normalisation

Adjusting earnings while leaving **capital expenditures, working capital and
financing costs** at current-year levels. The result mixes a mid-cycle profit
with trough-year investment — a combination the company has never actually
experienced.

If the base is normalised, capex/revenue, ΔNWC/revenue and the financing
assumption must be normalised over the same window.

### Trap 2 — double-counting growth

Replacing depressed earnings with a normalised figure **and simultaneously
applying analyst growth forecasts that assume the recovery**. The normalised
base already contains the recovery; the growth rate contains it again.

This is the trap the growth-eligibility gates exist to catch. It is easy to
fall into because both halves look individually reasonable.

### Trap 3 — assuming normalisation is instantaneous

The formula prices the company as if earnings normalise today. Damodaran's
correction: if normalisation takes N periods, **discount the value back by N
periods**. Skipping this systematically overvalues every depressed cyclical.

## What he warns against beyond the three

- **Applying only industry-average margins** without capturing what is specific
  to the firm. The sector average is a sanity check, not the answer.
- Treating a structurally impaired business as cyclical. Mean reversion assumes
  there is a mean to revert to; check the narrative before assuming one exists.
