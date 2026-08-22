# Associate-Heavy and Holding-Company Economics

## Trigger

Run this module when **either** condition holds on the latest reported period:

| Condition | Threshold |
|---|---|
| Share of profit from associates / JVs ÷ net profit attributable to owners | > 25% |
| Long-term investments (equity stakes) ÷ total assets | > 30% |
| **Minority interest ÷ total group equity** | **> 20%** |

Any one alone is enough. The first two say the company's economics sit partly
in businesses it does not consolidate; the third says the opposite — it
consolidates businesses whose economics are partly somebody else's. Both
directions break the same measures.

*Calibrating case for the first two — GULF (SET), TTM to 2026-06-30:* equity
income was 64.5% of net profit and long-term investments 53.2% of assets. Both
cleared by a wide margin, and all three distortions below were present at once.

*Calibrating case for the third — Ping An (SHA:601318), TTM to 2026-06-30:*
neither associate condition fired, because Ping An consolidates its major
subsidiaries rather than equity-accounting them. Minority interest was
**29.3% of group equity, up from 24.6% in 2021** — nearly a third of the
consolidated capital belongs to outside shareholders, mostly in the listed
bank. Return on equity reads 15.50% on the owners' base and 13.11% on the
group base, and the gap widens every year. Without the third trigger the case
would have passed through unflagged.

Threshold evidence, measured live 2026-08-21 — the 20% line separates cleanly
and is not a round number picked for looks:

| Company | Minority ÷ group equity | Trigger |
|---|---|---|
| CPALL (SET) | 57.8% | fires |
| Ping An (SHA) | 29.3% | fires |
| TU (SET) | 13.9% | quiet |
| GULF (SET) | 9.2% | quiet |
| AAPL | none reported | quiet |

CPALL is the sharpest case: it consolidates subsidiaries in which outside
shareholders hold most of the equity, so **more than half of group equity is
not the parent's**. Every unadjusted group-level per-share and return figure
for that company describes a business the owner mostly does not own.

## Why this module exists

Equity-method accounting puts a company's earnings and its assets on different
footings. Three standard measures break in the same direction — flattering or
damning the company for reasons that have nothing to do with its economics —
and each has to be corrected separately.

### 1. Return on capital is measured against the wrong denominator

The carrying value of the stakes sits in invested capital, but their earnings
arrive as a single below-the-line item that most return calculations exclude.
The company looks less profitable than it is.

**Do:** compute and report **both** bases, always side by side.

| Basis | Includes associates? | Answers |
|---|---|---|
| Operating-only ROIC/ROCE | no, in neither numerator nor denominator | What do the assets the company *runs* earn? |
| Total-capital return | yes, both | What does every unit of capital raised earn? |

Never publish one alone. The **gap between them is itself the finding** — it
sizes how much of the company's return depends on stakes rather than
operations. On GULF the two read 3.8% and ~7%; that spread *is* the thesis.

### 2. Free cash flow understates cash generation

Dividends received from associates are an investing-activity line under both
IFRS and US GAAP, so they never enter operating cash flow. A company drawing
large associate dividends can show negative free cash flow while being
comfortably cash-generative.

**Do:** build the **associate cash bridge** explicitly:

```
share of profit from associates        (accrual, income statement)
− undistributed earnings retained at the associate
= dividends actually received          (cash, investing activities)
```

Locate the cash figure in the cash-flow statement — often inside a generic
"other investing activities" line — and say where it was found. If the line is
aggregated and cannot be isolated, mark `UNRESOLVED` and estimate it from the
associate's own declared dividend per share × the stake, labelled as DERIVED.

*GULF:* AIS paid THB 17.38/share against a 40.44% holding of 2,974m shares,
implying roughly **THB 20.9bn a year of cash** that never appears in operating
cash flow. Headline FCF was −3.8bn. Reading only the headline inverts the
conclusion.

### 3. EBITDA means two different things

Companies commonly fold share of associate profit into their own EBITDA;
data providers commonly do not. Leverage ratios computed on the two bases can
differ by roughly a factor of two.

**Do:** state which basis each leverage figure uses, every time, and show both
where the difference is material. *GULF FY2025:* company EBITDA THB 53,866m vs
provider EBITDA ~THB 27,800m; net debt / EBITDA reads 5.9× or 11.6×.

## Required outputs

Add to `economic_engine_pack`:

- **`look_through_earnings`** — the company's share of each material
  associate's *underlying* earnings, not merely the equity-accounted line.
  Note where the associate's own leverage, tax, or minorities sit.
- **`associate_cash_bridge`** — accrual → cash, per section 2, with the
  statement line the cash figure came from, or `UNRESOLVED`.
- **`return_bases`** — both return measures, their definitions, and an
  explicit statement of what the gap between them means.

## Reading the equity-method line's sign

In the cash-flow statement, share of associate profit appears as a **negative
add-back** (it is non-cash income being removed from net profit). A data field
of −24,299,184,000 is +24.3bn of associate income, not a loss. Getting this
backwards flips the entire diagnosis, so state the sign convention wherever
the figure is used.

## What this module does not decide

Whether the stakes were *bought well* is capital allocation — that belongs to
`reinvestment-runway`, which should consume `look_through_earnings` and
`associate_cash_bridge` rather than recomputing them. This module establishes
what the stakes earn and what cash they deliver; it does not judge the
purchase, and it does not value the holdings.

## Failure modes

- Reporting one ROIC basis and calling it *the* return.
- Concluding "burns cash" from headline FCF without the associate bridge.
- Comparing a company-basis leverage ratio to a provider-basis peer figure.
- Treating a listed stake's market value as though it were operating capacity.
- Reading the negative equity-method add-back as a loss.
- Letting a holding-company structure inherit an operating-company frame from
  Layer 0 — if this module triggers, check whether `business_identity_pack`
  needs a `SCOPE_CHALLENGE`.
