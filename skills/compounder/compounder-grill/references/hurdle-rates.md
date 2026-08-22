# Hurdle Rates

Two lines, not one. They answer different questions and collapsing them into a single number is how a mediocre business gets read as a compounder, or a genuinely good one gets read as a failure.

| Line | Question it answers | Consequence of failing it |
|---|---|---|
| **Value-destruction line** — cost of capital | Does growth make the owner richer or poorer? | Potential is capped at **Weak**; a negative incremental return is **Broken** |
| **Attractive line** — 15% | Is the return high enough to call this a compounding engine at all? | Potential is capped at **Moderate** |

A company between the two lines is not failing. It is earning its keep without being the kind of business this skill exists to find, and the verdict should say so plainly.

## The value-destruction line

Growth creates value only when the return on the capital exceeds the cost of that capital. When the two are equal, growth is worthless — the added earnings are exactly consumed by the capital needed to produce them. This is why a company can post a healthy-looking growth rate while making its owners poorer, and why the growth number alone can never carry a verdict.

**Source.** Damodaran publishes cost of capital by industry and region, and country risk premiums for every rated country, updated annually. Both are free.

- Industry cost of capital, by region: US, Europe, Japan, Emerging Markets, India, China, Global
- Country risk premiums: `ctryprem.xlsx`, refreshed each **July**

**Which country.** Use the country the company **operates in**, not the one it is incorporated in. Where operations span countries, weight by revenue — the geographic split is already in the Layer 1 segment evidence, so read it rather than assuming a single country.

**Defaults when the current table has not been consulted.** Damodaran reports that 80% of US companies sit between **5.26% and 9.88%**, and 80% of global companies between **6.28% and 11.66%**. The midpoints below are derived from those published bands and are adequate for the only job this line has — separating value-creating growth from value-destroying growth. They are not a valuation input.

| Setting | Default | Basis |
|---|---|---|
| Developed market | **7.5%** | midpoint of the published US 80% band |
| Global / mixed | **9.0%** | midpoint of the published global 80% band |
| Emerging market | **11.0%** | upper half of the global band, where country risk premiums place emerging markets |

Use the actual industry-and-country figure whenever the return sits within roughly two points of the default, or whenever the company is capital-intensive or regulated. Precision beyond that buys nothing: Damodaran himself notes that time spent refining a cost-of-capital estimate has sharply diminishing returns.

**Table currency.** Figures above reflect the datasets as at **August 2026**. Refresh after each July update.

## The attractive line

**15% on incremental capital.** This is the bar the 100-bagger literature uses — Mayer screens for businesses able to redeploy earnings internally at 15% or better, on the reasoning that anything less cannot compound owner value fast enough to matter over a holding period measured in decades.

It is deliberately a fixed number rather than a risk-adjusted one. This skill exists to find compounding engines, not to grade every business fairly against its own cost of capital. A regulated utility earning 8% against a 6% cost of capital is creating value and is not a compounder; both statements are true and the two-line structure lets the verdict say both.

## Applying the pair

```
incremental return < 0                    →  Broken
incremental return < value-destruction    →  Weak (cap)
value-destruction ≤ return < 15%          →  Moderate (cap)
return ≥ 15%                              →  Strong and Exceptional available,
                                             subject to the growth bands
```

Record in the thesis pack which figures were used, on what basis, and as of when. A verdict whose hurdle cannot be reconstructed is not reproducible.

## Financial institutions

ROIC and free cash flow do not apply where liabilities are the raw material rather than the funding. Compare the sector return measures against the **cost of equity** for the same country, and state that basis explicitly. The attractive line still applies, read against return on equity attributable to owners.
