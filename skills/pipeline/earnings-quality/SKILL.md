---
name: earnings-quality
description: >
  Establish whether reported earnings can be trusted as a valuation base, and
  normalise them the way Damodaran does — by averaging the MARGIN over a full
  cycle and applying it to current revenue, not by averaging the earnings
  themselves. Use this before any DCF or multiple: "normalise earnings",
  "are these earnings real", "strip out one-off items", "what's the mid-cycle
  earnings power", "should I use last year's EPS", "cyclical normalisation",
  "is this growth real", or whenever a company has had an impairment, a
  disposal gain, a large FX swing, or a loss year that does not match its
  operating performance. Step 2.5 of the both-stock-analysis pipeline: it sits
  between the business narrative and the valuation, and it hands the valuation
  a base plus an explicit ruling on whether a growth rate may be stacked on
  top. Research and educational output only — not financial advice.
---

# Earnings Quality

A DCF built on a manipulated or distorted earnings base is a precise
calculation of a wrong number. This step decides what the company actually
earns in a normal year, before anything downstream projects it forward.

**Disclaimer:** Research and educational output only. Not financial advice.

---

## The method (Damodaran's, not the popular one)

Most people normalise by averaging reported earnings over five years.
Damodaran gives that method a narrow licence and prefers a different one.

| | Method 1 — average absolute earnings | Method 2 — average margin × current revenue |
|---|---|---|
| How | Mean of the last N years' earnings | Mean operating margin over N years, applied to today's revenue |
| Valid when | **Only if the company has not changed scale.** Applied to a business that grew or shrank, it is simply wrong. | Any company — it reflects today's size |
| Extra virtue | — | Starts from **revenue**, the line least exposed to accounting discretion |
| Damodaran's view | permitted, narrowly | **preferred** |

The second method's real advantage is structural. Method 1 asks you to find and
strip every one-off item by hand, and you will miss some. Method 2 starts from
a clean line and multiplies by a margin that has already absorbed the good and
bad years — **the one-offs never enter the calculation** rather than being
hunted out of it.

### Window

Long enough to contain a whole cycle: Damodaran frames this as **5–10 years**
and stresses that cycle length varies by industry — some run 2–3 years, some
over 10. Pick from the industry, do not default to five for everything.

### Commodity inputs

For a business whose earnings ride a commodity, Damodaran prefers **forward and
futures prices** over analyst forecasts, because the market's price has no
career risk attached to it. Take the price path from `business-drivers` (which
identifies which commodity actually matters) rather than assuming one.

---

## The three traps

Damodaran names three ways normalisation goes wrong. The script checks all
three and refuses to be quiet about any of them.

**1. Normalising only half the model.** Adjusting earnings to mid-cycle while
leaving capex, working capital and financing at current-year levels produces a
year that never existed — mid-cycle profit sitting on trough-year investment.
If you normalise, normalise the whole set.

**2. Counting the recovery twice.** This is the one that quietly inflates
valuations. You replace a depressed year with a normalised figure — which
already assumes recovery to mid-cycle — and then apply a consensus growth rate
that is itself made mostly of that same recovery. The script runs explicit
growth-eligibility gates and tells you when growth may not be stacked.

**3. Assuming recovery is instant.** The formula values a company as if it
normalises today. If recovery realistically takes three years, discount the
value back three years or the answer is too high.

---

## What to exclude, and what only looks excludable

The test is one question: **if nothing changes, will this happen again next
year?** If yes, it belongs in the base, however unusual it feels.

| Exclude | Keep |
|---|---|
| Gain or loss on disposal of assets, land, a subsidiary | Import tariffs and duties |
| Asset revaluation, impairment, goodwill write-down | New regulation that changes the cost structure |
| FX translation gains and losses | Raw-material price moves (they are the cycle, not an exception) |
| Litigation settlements, insurance recoveries | Restructuring that recurs every year (a habit, not an event) |
| Tax refunds and one-time tax charges | Competitive price pressure |

Two items that trip people up:

- **A large FX loss and a new import tariff both look like "not normal
  operations".** They are not the same. FX translation is an accounting
  artefact of where the company keeps its books; a tariff is a permanent change
  to the cost of doing business in that market. Exclude the first, keep the
  second.
- **"Non-recurring" charges that recur.** A company that takes a restructuring
  charge every year is not restructuring — that is its cost base.

---

## Growth eligibility

A normalised base already contains the recovery. Growth may only be stacked on
top of it when the growth is made of something else. The gates:

```
PASS required on all of:
  latest operating margin >= cycle average        (recovery has happened)
  revenue rose in each of the last two years       (volume/price, not base effect)
  operating income rose in each of the last two    (it reached the bottom line)

NOT evidence of real growth:
  earnings up because the prior-year base was low
  earnings up because of a one-off gain
  revenue up while margin contracts   (buying growth)
```

Fail any gate and the model must use **post-recovery growth only**, stated
explicitly as such.

---

## Running it

Reads a `fetch.py` snapshot from the data layer, or explicit series:

```bash
# from the data layer (preferred — carries provenance and fallback flags)
python scripts/normalize.py --snapshot .data/TU.BK/2026-08-13.json

# or by hand
python scripts/normalize.py --ticker TU.BK --currency THB \
  --years 2025,2024,2023,2022,2021 \
  --revenue 132718579000,138433059000,136152713000,155586350000,141047695000 \
  --op-margin 0.04595,0.05177,0.05018,0.05098,0.05828 \
  --net-margin 0.03473,0.03384,-0.10454,0.04395,0.05468 \
  --current-revenue 135439918000

python scripts/normalize.py --snapshot ... --json --out normalised.json
```

The script derives margins from absolutes (or the reverse) when only one is
given, picks the readable unit from the smallest headline figure, and reports
rather than resolves: outlier years are **flagged, never dropped**, because a
cycle peak or trough is a real observation, not an error.

---

## Worked example — why the method choice is not academic

Thai Union (BKK:TU), five reported years:

| Year | Revenue (THB m) | Operating margin | Net margin |
|---|---|---|---|
| 2025 | 132,719 | 4.59% | 3.47% |
| 2024 | 138,433 | 5.18% | 3.38% |
| 2023 | 136,153 | **5.02%** | **−10.45%** |
| 2022 | 155,586 | 5.10% | 4.40% |
| 2021 | 141,048 | 5.83% | 5.47% |

FY2023's operating margin is unremarkable — mid-pack against the other four
years. Its net margin is −10.45%. **All the damage sat below the operating
line.** Now compare the two methods against a reported TTM operating income of
6,601m:

| Base | Result (THB m) |
|---|---|
| Average net income (method 1) | **1,922** |
| Average net margin × current revenue | **1,697** |
| Average operating margin × current revenue | **6,966** |
| Reported TTM operating income | 6,601 |

Normalising off net income lands at roughly a quarter of what the business
demonstrably earns. Nothing about that number is defensible, and a DCF built on
it would price the company as if a single year's write-down were its permanent
condition. The operating-margin path lands 5.5% above the current TTM figure —
a mid-cycle base, which is exactly what normalisation is for.

The script detects this automatically: it compares the volatility of the two
margin series and checks whether the worst net year is also the worst operating
year. For Thai Union net margin is **14.9× more volatile**, and 2023 is the
worst net year but not the worst operating year — so it warns that the damage
sat below the operating line and directs you to the operating path.

Growth gates for the same company: **0 of 3**. So the normalised base may be
used, but no consensus growth rate may be stacked on it without double-counting
the recovery.

---

## Output contract

Hand these forward to `company-valuation`:

- **Normalised operating income** and the margin it came from
- **Which method was used and why the other was rejected**
- **Every excluded item with its reason**, so the exclusions can be attacked
- **Growth eligibility verdict** — may a growth rate be stacked, yes or no
- **Any FALLBACK-sourced inputs**, flagged onward

If the answer is "these earnings cannot be normalised responsibly" — too little
history, too erratic a margin — say that, and let the valuation widen its
scenario range instead of pretending to a precision it does not have.

---

## Reference files

- `references/damodaran-method.md` — the two methods, window selection, commodity handling, and the three traps in full
- `references/exclusion-rules.md` — the recurrence test, the exclude/keep table with worked cases, and the sector-specific items

## Caveats

- Normalisation is a judgement dressed as arithmetic. The script makes the
  judgement explicit and checkable; it does not remove it.
- A cycle-average margin assumes the cycle repeats. For a structurally
  impaired business it will read as too generous — check the narrative first.
- Not financial advice.
