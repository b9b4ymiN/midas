# Financial Metrics & Health Snapshot

The purpose of this snapshot is **diagnostic, not just descriptive**. A table of numbers tells the reader *what* the company is; the interpretation tells them *what it means* and gives them a base to reason forward from. Every metric below ships with (a) how to compute it, (b) a 5-year history so the reader sees the *direction*, and (c) a one-line read that turns the number into a judgement.

The golden rule: **a single year is a data point; five years is a story.** Always pull the trend, not just the latest value. The direction of travel (improving / deteriorating / stable) is usually more decision-relevant than the absolute level.

---

## The Metric Families

Pull and present these six families. Aim for ~20 metrics total — enough to be a real fact base, not so many the reader drowns.

| Family | Metrics | What it answers |
|---|---|---|
| **Profitability** | Gross margin, Operating margin, Net profit margin (NPM), EBITDA margin | Can it turn revenue into profit, and is that improving? |
| **Returns / capital efficiency** | ROIC, ROE, ROA, ROCE, **WACC**, **ROIC−WACC spread** | Does it earn more than its cost of capital? (the value-creation test) |
| **Cash flow** | Operating CF, CapEx, Free cash flow (FCF), FCF margin, FCF/share | Does accounting profit convert to real cash after reinvestment? |
| **Balance sheet / leverage** | Debt/Equity (D/E), Net debt, Current ratio, Net debt/EBITDA, interest coverage | Is the balance sheet getting safer or riskier? |
| **Valuation multiples** | P/E, P/B, EV/EBITDA, P/S, P/FCF, EV/EBIT | Cheap or expensive vs. own history and peers? |
| **Dividend / shareholder return** | DPS, dividend yield, payout ratio, buyback yield, shareholder yield | How much cash comes back, and is it sustainable? |
| **Capital allocation quality** | Diluted share count trend, Goodwill/Total assets, ROIC before vs after major deals, Related-party purchases as % of COGS | Is management's use of capital reaching you, or leaking before it does? |

Plus a few **health scores** as a quick gut-check: Piotroski F-Score (0–9, fundamental momentum), Altman Z-Score (bankruptcy distance).

---

## How to Pull (yfinance, 5-year history)

yfinance exposes the statements as DataFrames with years as columns. Pull all three statements plus `info`, then compute the ratios yourself — the derived ratios (ROIC, FCF, spreads) are more reliable hand-computed than scraped.

```python
import yfinance as yf
import numpy as np
import pandas as pd

t = yf.Ticker(TICKER)
info   = t.info
inc    = t.income_stmt          # annual; columns = fiscal years (newest first)
bs     = t.balance_sheet
cf     = t.cashflow

def row(df, *names):
    """Return a row by the first label that exists, else NaN series."""
    for n in names:
        if n in df.index:
            return df.loc[n]
    return pd.Series([np.nan] * df.shape[1], index=df.columns)

rev   = row(inc, "Total Revenue")
ebit  = row(inc, "Operating Income", "EBIT")
ni    = row(inc, "Net Income", "Net Income Common Stockholders")
gp    = row(inc, "Gross Profit")
tax   = row(inc, "Tax Provision")
pretax= row(inc, "Pretax Income", "Income Before Tax")
da    = row(cf,  "Depreciation And Amortization", "Depreciation Amortization Depletion")
capex = row(cf,  "Capital Expenditure").abs()
ocf   = row(cf,  "Operating Cash Flow", "Cash Flow From Continuing Operating Activities")
equity= row(bs,  "Stockholders Equity", "Common Stock Equity")
debt  = row(bs,  "Total Debt")
cash  = row(bs,  "Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments")
assets= row(bs,  "Total Assets")
cur_a = row(bs,  "Current Assets")
cur_l = row(bs,  "Current Liabilities")

# Effective tax rate (for NOPAT), clamped to a sane band
eff_tax = (tax / pretax).clip(0.15, 0.35)

# ── Profitability (%) ──
gross_margin = gp   / rev
op_margin    = ebit / rev
npm          = ni   / rev
ebitda       = ebit + da
ebitda_margin= ebitda / rev

# ── Returns ──
nopat        = ebit * (1 - eff_tax)
invested_cap = debt + equity - cash          # common ROIC denominator
roic         = nopat / invested_cap
roe          = ni    / equity
roa          = ni    / assets
ce           = assets - cur_l                # capital employed
roce         = ebit  / ce

# ── Cash flow ──
fcf          = ocf - capex
fcf_margin   = fcf / rev
capex_pct    = capex / rev

# ── Leverage ──
de           = debt / equity
net_debt     = debt - cash
nd_ebitda    = net_debt / ebitda
current_ratio= cur_a / cur_l
```

For the **valuation multiples and WACC**, reuse the values already computed in the main valuation run (Step 1 risk-free, Step 4 WACC, current price, shares). For dividend data use `info` fields: `dividendRate`, `dividendYield`, `payoutRatio`, plus the cash-flow line `Common Stock Dividend Paid`. Health scores (`Piotroski`, `Altman Z`) are often easier to read off a data aggregator (StockAnalysis, GuruFocus) than to compute from scratch — pull via web if not derivable.

> If yfinance is blocked or returns sparse statements (common for non-US tickers and Japanese listings like `.T`), fall back to a web aggregator for the historical series. Cross-check the latest year against the primary filing, and label any web-sourced figure.

---

## The Interpretation Layer (the part that matters)

For each family, attach a **read** — a short, plain-language judgement keyed to the *trend*, not just the level. These are the rules. Apply them, then write the sentence.

### ROIC vs. WACC — the value-creation test (lead with this)

This is the single most important diagnostic. ROIC is what the business earns on the capital invested in it; WACC is what that capital costs. The gap between them is whether the company **creates or destroys value**.

| Condition | Read |
|---|---|
| `ROIC − WACC` strongly positive (>3–4pp) and stable/widening | **"Earns well above its cost of capital — this is durable, compounding value creation. Growth here is worth paying for."** |
| Spread positive but thin (0–3pp) | "Creates value, but with little margin for error — a rising cost of capital or margin slip could erase it." |
| Spread ≈ 0 | "Running to stand still — growth is not creating shareholder value." |
| Spread negative | **"Destroying value — every yen/dollar reinvested returns less than it costs. Growth here is a liability, not an asset."** |

Always state the spread explicitly (e.g., "ROIC 11.8% vs. WACC 4.7% → **+7.1pp**"). Show the ROIC *trend*: a spread that has widened over five years (e.g., from +0 to +7pp) is a quality-inflection story.

### D/E and leverage — direction of travel

| Pattern | Read |
|---|---|
| D/E falling steadily over 3–5y | **"Disciplined capital management — the balance sheet is getting safer year after year, which de-risks the equity and frees future cash for shareholders."** |
| D/E rising but funding high-ROIC growth | "Leverage rising, but in service of investment that out-earns its cost — acceptable *if* ROIC stays above WACC. Watch the spread." |
| D/E rising with flat/falling ROIC | **"Leverage rising without the returns to justify it — a deteriorating risk profile."** |
| Net cash position (net debt < 0) | "Net creditor — carries more cash than debt, a fortress balance sheet that can fund downturns and buybacks without external capital." |
| Net debt/EBITDA > ~3× | "Meaningfully leveraged — earnings volatility now translates into solvency risk." |

### CapEx vs. FCF — is the investment any good?

This pairing is the most under-used and most revealing. CapEx alone looks like a cost; the question is whether it *produces* cash.

| Pattern | Read |
|---|---|
| CapEx rising **and** FCF also rising | **"Investing heavily yet still growing free cash flow — the clearest sign the reinvestment is productive and genuinely returning cash, not just consuming it."** |
| CapEx rising, FCF flat/falling | "Investment is consuming the cash it should be generating — either the projects haven't matured yet (give it 1–2 years) or they're low-return. Watch whether FCF inflects." |
| CapEx flat/low, FCF high | "Harvesting — strong cash generation but under-investing; durable today, but question where future growth comes from." |
| FCF negative while CapEx high | "Growth phase — burning cash to build. Only justified if the end-market and unit economics support it; size the position for that uncertainty." |

Tie this back to ROIC: rising CapEx that *also* lifts ROIC is the gold standard — the company is finding more high-return places to put money.

### Margins — quality and trajectory

- Rising gross margin → pricing power or mix/cost improvement; the most durable kind of margin gain.
- Operating margin rising faster than gross → operating leverage (fixed costs spread over more revenue).
- NPM above the industry average → structural advantage; below → a cost or capital-structure drag worth explaining.
- A margin that *peaked and is now compressing* deserves a flag and a "why" (FX, input costs, tariffs, mix) — don't just report the level.

### Valuation multiples — cheap vs. own history, not just absolute

A P/E of 8× means nothing in isolation. Frame it three ways: vs. the company's **own 5-year history**, vs. **peers**, and vs. **what the growth/returns justify**. A high-ROIC, growing, de-leveraging company at a multiple *below* its own history and below peers is the setup worth surfacing.

- P/B < 1.0 with ROE comfortably above cost of equity → market is pricing the equity below book despite it earning good returns; a value signal worth interrogating.
- P/FCF well below its historical average → the cash-generation improvement hasn't been re-rated yet.

### Dividend — return and sustainability

- Payout ratio < ~40% with rising DPS → dividend is well-covered and has room to grow; **growth + safety**.
- Payout ratio > ~80% → little buffer; a profit dip could force a cut.
- Rising DPS *and* falling payout ratio simultaneously → earnings are growing faster than the dividend — the healthiest possible dividend trajectory.
- Add buyback yield to dividend yield for total **shareholder yield** — the real cash-return number.

### Health scores — the gut-check

- **Piotroski F-Score** 7–9 = strong fundamental momentum; 0–3 = weak. State it as "X / 9."
- **Altman Z-Score** > 3.0 = safe; 1.8–3.0 = grey zone (note it); < 1.8 = distress signal. For asset-heavy or finance-adjacent firms the Z-score runs low structurally — don't over-read a borderline score on a cash-rich industrial; mention the caveat.

---

## How to Present It

In a deck or report, the financial snapshot works best as **one dense dashboard slide/section** organised by the six families, where every metric shows:

1. the **headline number** (latest),
2. a **5-year mini-trend** (sparkline, small bar series, or just "FY22 X% → FY26 Y%"),
3. a **one-line read** drawn from the rules above, and
4. **colour coding** that encodes the judgement — green = strengthening / value-creating, amber = watch, red = deteriorating. (Never colour by sign alone; colour by *what it means*. Rising CapEx is red-the-cost but green-the-signal when FCF rises with it — code it green.)

Lead the section with the **two or three diagnostics that carry the thesis** — almost always (1) ROIC−WACC spread, (2) the FCF inflection / CapEx-productivity story, and (3) the leverage trend. Put the full grid behind them.

Round every displayed number. Keep currency consistent and labelled. Cross-check the latest year against the primary filing; aggregator data lags and can be revised.

> **Not financial advice.** These reads are analytical heuristics to help a reader reason, not recommendations. The same number supports different conclusions depending on price paid and horizon.


---

## Capital Allocation Quality — the three the income statement cannot show

Most of what a poor steward of capital does eventually reaches reported profit,
and ROIC, the ROIC−WACC spread and buyback yield above already cover most of the
ground. Three things they do not cover:

**1. Dilution.** Issue shares and revenue is unchanged, operating income is
unchanged, net income is unchanged — and your claim on all three shrinks. No line
on the income statement moves; only the denominator does. Track the **diluted**
share count over five to ten years, adjusted for splits.

| Annual change | Read |
|---|---|
| below +2% | routine option issuance |
| +2% to +5% | above routine — find out what it funded |
| above +5% | per-share results diluted faster than most businesses grow |
| negative | buybacks — whether that was the best use of the cash depends on the price paid |

**2. Overpaying for acquisitions.** The worst of the three, because the acquired
company's profit **consolidates**: operating income goes up and the year looks
like growth. The damage sits in goodwill and in the ROIC denominator. The income
statement does not merely fail to show it — it points the other way.

Track **goodwill / total assets** and watch for step changes marking the deal
year, then compare **ROIC before and after**. Above 20% of assets, judge
management on the returns those deals earn rather than on consolidated revenue.
Above 35%, most of the balance sheet is a record of prices paid for other
companies.

**3. Related-party leakage.** Buying from an affiliate above market price arrives
as ordinary cost of goods sold, indistinguishable from real input cost. This one
is not in any data feed — it is in the **notes to the financial statements**.
Material for family-controlled companies, which is most of the Thai market. Above
5% of COGS, read how the prices were set; above 15%, those transactions
materially set reported margin.

**And the timing reason they belong together.** Even where the damage does
eventually reach earnings, it arrives two or three years late. By then you own
the position. All three are visible in the year they happen.

### Running it

```bash
python scripts/capital_allocation.py \
  --shares 4128,4110,4098,3980,3720 --years 2025,2024,2023,2022,2021 \
  --goodwill 12400,12500,4100,4050,4000 \
  --total-assets 210000,205000,190000,188000,180000 \
  --roic 0.081,0.079,0.112,0.118,0.121 \
  --related-party-purchases 8200 --cogs 109000
```

It reports what it could not assess rather than staying silent about it — a
dashboard that omits a metric looks the same as one where the metric was fine.
