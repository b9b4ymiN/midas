# Reinvestment Methods

## Core decomposition

Use as an analytical identity, not a precise forecast formula:

**Future Compounding Economics ≈ Incremental Return × Reinvestment Capacity × Duration**

Christopher W. Mayer supplies the North Star (high returns + growth + ability to reinvest). Chuck Akre emphasizes reinvestment opportunity. Damodaran distinguishes returns on future investment from legacy returns. Mauboussin/Callahan formalize value creation around return spreads, investment amount, and competitive advantage period.

**The three legs are not independent.** Damodaran's life-cycle work finds that the same forces that let a business scale quickly also shorten how long it stays on top: capital-light businesses with low switching costs scale fast and fade fast, while capital-heavy businesses with high switching costs scale slowly and persist. Scoring Reinvestment Capacity and Duration both high is therefore a claim that requires its own evidence rather than an accident of two independent readings.

## Mandatory measures

Compute all four on every run and report them together. These are not options.

```
Reinvestment Rate  = (net capex + increase in working capital) / NOPAT
                     where net capex = capital expenditure − depreciation & amortisation

Incremental Return = Δ NOPAT / Δ invested capital          (window ≥ 3 years; 3–5 normal)

Growth from new investment = Reinvestment Rate × Incremental Return

Growth from rising returns = (ROIC_end − ROIC_start) / ROIC_start,
                             annualised over the same window
```

Net capex, not gross: the portion equal to depreciation replaces what wore out and buys no growth.

**Never use free cash flow as the denominator of the reinvestment rate.** Free cash flow is already net of the capital spend being measured, so the ratio answers a different question and understates reinvestment severalfold. Cash accumulating beyond what the business reinvests is a **capital allocation** finding — record it there, not here.

**Never report a cumulative figure without its annual series.** A stable multi-year average routinely conceals a collapsing trend, and the trend is the more decision-relevant number. A reinvestment rate averaging a third of NOPAT across four years while falling from a half to under a fifth is a company whose engine is closing, and only the series shows it.

## Invested capital and excess cash

Returns must be computed on capital that is actually working. Exclude non-operating assets from invested capital:

- cash and marketable securities
- equity investments in other companies and non-consolidated subsidiaries
- finance subsidiaries
- overfunded pension assets
- tax loss carry-forwards

Report the return **both before and after** the adjustment, with the gap. The gap is itself a finding: a large one means reported ROE or ROIC is describing the balance sheet rather than the business.

**Count the drag once, never zero times.** Removing idle capital from the denominator raises the measured return, and that is correct — the operating business does earn it. But the capital still exists and still earns nothing. Having adjusted the denominator, the reinvestment leg MUST state that the excluded balance is capital the business has not found work for. Adjusting the ratio and then omitting the observation turns a real problem into a better-looking number.

**When adjusted invested capital falls below one year of NOPAT, or turns negative, the accounting return is void.** Sustained repurchases can shrink book capital until the ratio reports repurchase history rather than business quality. Fall back to `Δ NOPAT / Δ invested capital` or to unit-level economics; when neither is available the incremental return is `UNRESOLVED` and must travel forward as such.

## Where growth comes from

Separate the two sources. They have different lifespans, and treating them as one number is how a temporary gain gets extrapolated.

| Source | Formula | How long it lasts |
|---|---|---|
| New investment | Reinvestment Rate × Incremental Return | As long as the company can keep deploying capital at that return |
| Rising returns on existing assets | (ROIC_end − ROIC_start) / ROIC_start | Bounded — roughly 3–5 years once slack is exhausted, **unless** it is pricing power |

Damodaran's distinction: growth from new investment "can be continued for as long as the firm can maintain its policy on reinvestment", while growth from improving efficiency on existing assets runs out when the inefficiency does.

The exception matters. Durable pricing power raises returns on existing assets for as long as the moat holds — decades, in the classic cases — and looks identical in the arithmetic to a one-off cost cut. Separate them with evidence, not judgement:

**Pricing-power test — three tiers**

1. **Gross margin did not fall through a rising input-cost cycle**, across at least one full cycle. This is the strongest available proof: a company with real pricing power passes costs through and holds or expands margin, while one without it shows revenue growing on inflation as margin erodes.
2. **Volume or share survived the price increase.** Units, customers, or market share held after prices rose.
3. **The company discloses price separately from volume**, so the split can be checked rather than asserted.

| Tiers passed | Treatment |
|---|---|
| Three | Count the rising-returns growth in full; it is durable while the moat holds |
| Two | Count half, and mark `PARTIALLY_RESOLVED` |
| One or none | Do not count it; treat as slack removal with a 3–5 year life |

Tier 3 is usually already answered upstream: `market_growth_pack.growth_decomposition` separates price from volume as part of the Layer 1 gate. Read it rather than rebuilding it.

## 1. Reinvestment reconstruction

Track material use of internal and external capital across organic capex/capacity, R&D/product, working capital, customer acquisition/brand, M&A, debt, buybacks, dividends, cash accumulation, SBC and equity issuance. Distinguish maintenance from growth investment where possible.

Use `capital-allocation.md` for allocator behavior, acquisitions, buybacks, and dilution.

## 2. Average vs marginal return

Historical ROIC asks: “How productive is the accumulated capital base?”
Marginal/ROIIC asks: “What are recent incremental investments earning?”

The mandatory `Δ NOPAT / Δ invested capital` above is the default. The following remain available as corroboration or where the default is distorted, chosen only when economically sensible:
- cohort/store/facility return on build/acquisition cost
- incremental gross/contribution profit / incremental acquisition or capacity spend
- `ΔRevenue / sales-to-capital` to infer growth capital, combined with normalized margins
- post-acquisition incremental NOPAT/FCF relative to full deal/follow-on capital

Use rolling/multi-year windows to reduce noise and avoid single-period denominator artifacts; a single year of unusually heavy or light investment is not a reinvestment policy. Explain distortions from acquisitions, impairments, leases, working capital, intangibles, and ramp periods.

### When the history is genuinely too short

Fewer than three years of history, or a company in the Introduction or Growth stage whose returns have not matured, is **not** a case for reporting a weak number or withholding a verdict. It is a case for a different measurement, and `emerging-compounder.md` defines it. Run that bridge and treat it as the primary path rather than one option among several:

`ΔRevenue / sales-to-capital` becomes the route to the reinvestment figure, combined with a target mature margin anchored to observed cohorts or comparable firms, from which the implied return follows. Each input carries its evidence class, so the uncertainty stays visible instead of being buried inside a single projected return.

Two cautions specific to young companies, both from the same source as the bridge:

- **Recent beats long.** For a company changing quickly, an older annual report is stale in a way that no averaging repairs. Trailing twelve months is the better input, and a longer window is not automatically a better one.
- **Some operating expense is capital expense.** Customer acquisition, brand building and R&D at a scaling company buy future growth. Where these are material the company is reinvesting far more than the capex line shows, and the reinvestment rate computed from reported capex understates it. Use the upstream intangible-capital diagnosis before concluding that a young company does not reinvest.

The result feeds Evidence Maturity, never a Potential penalty. Short history lowers what has been demonstrated; it does not lower what the economics can support.

## 3. Scale direction

Consume `scale_economics` from the Business Engine and test whether later units/cohorts confirm or contradict it. Reinvestment return is not assumed constant across geography, capacity, or maturity.

## 4. Intangible investment

Accounting can expense economic investment such as R&D, software, customer acquisition, brand building, and organizational capability. Use the upstream intangible-capital diagnosis. When material, adjust if defensible or state the directional bias and uncertainty.

## 5. Capital allocation quality

Evaluate behavior, not labels. Core-engine returns and allocator returns remain separate conclusions until synthesis.
