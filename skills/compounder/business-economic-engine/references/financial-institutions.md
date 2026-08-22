# Financial Institutions: Insurers and Banks

## Trigger

Run this module when **any** holds:

| Condition | Source |
|---|---|
| `statement_template` is `insurance` or `bank` | `har-to-api` fact, emitted every run |
| Balance sheet carries policy liabilities, technical reserves, or an insurance float | the filing |
| Balance sheet carries customer deposits and a loan book as the primary asset | the filing |

`har-to-api` settles this without judgement: the provider stamps the statement
template into its own field names (`Ins`, `Bank`, `Uti` suffixes), so detection
is a lookup. Where the data layer is unavailable, read the balance sheet.

## Why this module exists

**A ratio can be arithmetically correct and economically meaningless.** The
standard toolkit does not merely lose precision on a financial institution —
it produces confident numbers that answer no question. Three of them, and each
must be replaced rather than adjusted.

### 1. ROIC and ROCE do not apply

They ask what capital earns, treating liabilities as *financing*. For an
insurer, liabilities are the **raw material**: the premium a policyholder pays
is the product being sold, not money borrowed to fund operations. For a bank,
deposits are likewise the input, not the funding of an input.

Putting them in the denominator produced **6.29%** on Ping An
(SHA:601318, TTM to 2026-06-30). The figure is arithmetically right and
economically empty.

**Use instead:** return on equity computed on equity **attributable to
owners** — and state that basis explicitly, because the group basis is a
different number (see the minority-interest trigger in `holding-company.md`).

### 2. Free cash flow does not apply

Operating cash flow includes premiums received and deposits taken. It is money
the institution must hand back, not cash available to owners.

Ping An's operating cash flow was **CNY 688,484m**, giving a price to free
cash flow of **1.36x**. Nothing about that means cheap.

**Use instead:** for a life insurer, the movement in stored profit (below).
For a bank, retained earnings after the capital required to support the loan
book.

### 3. Leverage ratios do not apply

Debt/EBITDA, net debt/equity, current ratio and quick ratio all assume debt is
optional and working capital is a cycle. For a financial institution, leverage
*is* the business model and is governed by a solvency or capital regime, not
by management preference.

**Use instead:** regulatory solvency ratios and their **direction**. Ping An:
core solvency 160.73% and comprehensive 193.30% at end-2025, both *down* year
on year — the level was comfortable while the trend was not, and only the pair
tells you that.

## What to measure instead

### Life insurer

| Metric | What it answers |
|---|---|
| **New business value (NBV)** and NBV margin | What one year of new policies is worth |
| **Contractual service margin (CSM)** | The stock of profit already earned and awaiting release |
| **Embedded value (EV)** and operating return on EV | What the whole book is worth and what it earns |
| Solvency ratios, level **and** direction | Whether growth is financeable |
| Investment yield vs guaranteed liability cost | The actual spread being earned |

**The CSM is the single most important number, and it is a tank of water.**
New business is water flowing in. Profit reported each year is water flowing
out. If inflow exceeds outflow the tank grows and future profits rise; if they
match, the tank is level and future profits stay flat.

Ping An's tank held **CNY 733.2bn and grew 0.3%** — it had stopped shrinking
after three years of decline, but it was not growing. A company reporting
strong headline profit growth on a level CSM is releasing stored profit, not
creating it, and the distinction decides the whole compounding question.

### Bank

| Metric | What it answers |
|---|---|
| Net interest margin | The spread earned on the loan book |
| Cost/income ratio | Operating efficiency |
| Non-performing loan ratio and provision coverage | Whether reported profit will survive |
| CET1 ratio | Whether growth is financeable |
| Return on equity attributable to owners | Owner return |

## Mandatory rulings

1. **Never present ROIC, ROCE, FCF, P/FCF or EV/EBITDA as a return or
   valuation measure.** If cited at all, cite the reason it is being shown
   and state that it is not the return measure.
2. **State the equity basis on every ROE and per-share figure.** Attributable,
   not group, unless the group basis is the point being made.
3. **A missing embedded value is a thesis-critical gap for a life insurer.**
   Mark it `UNRESOLVED` and reduce confidence. Do not substitute book value
   and proceed as though the question were answered.
4. **Report the CSM movement, not just its level.** A level CSM alongside
   rising reported profit is a finding, not a detail.
5. **Solvency ratios travel as level plus direction.** A comfortable ratio
   falling for two periods says something a snapshot does not.

## Required outputs

Add to `economic_engine_pack`:

- **`sector_return_metrics`** — the replacement measures above with values and
  dates, or `UNRESOLVED` per item. Required when the trigger fires.
- Within `current_return_structure.return_bases`, an explicit note that
  ROIC/ROCE were **not** used and why.

## What this module does not decide

It does not value the institution. Valuing a life insurer needs embedded value
and an appraisal method that sits outside the Future Compounder scope, which
excludes DCF, fair value and target price. This module establishes what the
engine earns and whether the stored profit is growing — not what it is worth.

## Failure modes

- Quoting ROIC or P/FCF because the data layer returned them.
- Reading a low price-to-book as cheapness without asking whether the assets
  behind the book have been marked.
- Treating premium growth as demand evidence — under IFRS 17 revenue is not
  premiums, and premiums are the sell-in analogue, not end demand.
- Reporting a solvency level without its direction.
- Letting a rising headline profit obscure a level CSM.
- Using group equity for a per-share figure when minorities are material.
