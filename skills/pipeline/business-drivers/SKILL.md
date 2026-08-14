---
name: business-drivers
description: >
  Work out what actually moves a company's earnings, by reading the business
  first and only then going to look for data. Use when the user asks "what
  drives this stock", "what affects TU", "why did margin fall", "what should I
  watch on this name", "what is this company exposed to", "commodity/FX/input
  cost exposure", or before any valuation of a business whose earnings ride an
  input price. Produces a named driver list derived from the company's own cost
  and revenue structure, the data source for each, and — the deliverable that
  matters — a sensitivity number: how many points of operating margin a given
  move in that driver costs, and when it lands. Step 2.3 of the
  both-stock-analysis pipeline, feeding the valuation's scenario range and the
  thesis-breakers. Research and educational output only — not financial advice.
---

# Business Drivers

What moves this company's earnings, and by how much.

**Disclaimer:** Research and educational output only. Not financial advice.

---

## The rule that defines this skill

**Understand the business first. Only then go looking for data.**

Not a style preference — a correctness requirement. A skill that starts from a
list of candidate drivers returns "oil, FX, interest rates" for every company on
earth, which is both true and useless. The drivers that matter are the ones
implied by *this* company's cost and revenue structure, and you cannot know them
before reading it.

There is also a practical reason, discovered the hard way. Thai Union's real
drivers — tuna raw-material cost, US tariff exposure, currency translation on a
multi-currency footprint — do not appear in any financial data feed. No API
returns them. They come out of the segment mix, the cost structure and the
management discussion, which means the reading is not optional preparation for
the research; it *is* the research.

---

## Step 1 — Read, before searching anything

Do not open a data source yet. From the filing, the results release and the MD&A,
establish:

| What | Why it matters |
|---|---|
| **Revenue by segment** | Different segments ride different drivers. A driver hitting 47% of revenue is not the same finding as one hitting 7%. |
| **Cost structure** | Which line dominates: raw material, labour, energy, freight, rent? That line's price *is* the primary driver. |
| **Where it sells** | Demand geography sets tariff, regulation and consumer exposure. |
| **Where it buys, in what currency** | The mismatch between buying and selling currency is the FX exposure — not the reporting currency. |
| **Contract structure** | Fixed-price contracts, hedges, inventory buffers all delay when a move lands. |

Segment mix comes from the filing. The data layer exposes it inconsistently and
tags it with the provider's own labels, so it carries a cross-check obligation —
see `har-to-api`'s segment rule.

## Step 2 — Derive the drivers from that structure

Now name them, each traced to something you read. Full patterns in
`references/driver-derivation.md`. The shape:

```
largest cost line          -> its input price is the primary driver
buy currency != sell currency -> that pair is a driver
regulated or tariffed market -> policy is a driver
one segment growing differently -> it runs on its own cycle
```

**Test each candidate before keeping it:** if this moved 10%, would anyone
notice in the operating margin? If not, drop it. Three real drivers beat twelve
plausible ones.

## Step 3 — Only now, find the data

For each named driver, and nothing else. Sources in
`references/data-sources.md`. For commodities Damodaran's preference applies:
**forward and futures prices over analyst forecasts**, because the market's
price carries no career risk. That path feeds straight into `earnings-quality`.

## Step 4 — Quantify: the deliverable

"Tuna prices are rising" is an observation. This is the output:

```bash
python scripts/sensitivity.py --driver "tuna" \
  --cost-share 0.55 --margin 0.0487 --move 0.10 \
  --pass-through 0.6 --revenue 135439918000 \
  --lag-months 3 --currency THB
```

The script sweeps pass-through rather than hiding one guess inside a single
number, and reports the breakeven move **twice** — at zero pass-through and at
your stated assumption. Those two differ enormously (at a 4.9% margin and 55%
cost share: +9% versus +22%), and the gap between them *is* the question. Pricing
power is not a parameter you set once; it decides whether the move is survivable.

It cannot be run without the cost share and the margin, both of which come from
Step 1. That is deliberate.

---

## Worked example — Thai Union, Q1 2026

Three things moved earnings that quarter. None is visible in a standard
financial dashboard.

| Driver | Where it came from | Effect |
|---|---|---|
| **Tuna raw-material cost** | largest cost line; ambient seafood is 47% of revenue | prices climbed sharply in March |
| **US tariffs** | sells into the US; policy changed | cost 0.5pp of gross margin, offset by pricing |
| **Currency** | buys in USD, sells across many currencies | FX loss in the quarter |

And the detail that changes the forecast rather than describing the past: the
company holds a **two-to-four-month cost buffer**, so March's tuna move lands in
reported margin *next* quarter. A model that books it immediately is wrong about
timing in a way that will look like a miss.

ROIC, margin, D/E and P/E cannot surface any of this. It had to be read.

---

## Output contract

- **Named drivers**, each traced to the structural fact that implies it
- **The data source for each**, with futures preferred for commodities
- **Sensitivity per driver**: margin points per 10% move, at a stated
  pass-through, with the pass-through sweep beside it
- **Timing**: buffers, hedges and contract lags that delay when it lands
- **What you could not quantify**, said plainly rather than estimated

Feeds forward:

| To | What |
|---|---|
| `company-valuation` | sensitivity as a third scenario axis beyond WACC × g |
| `investment-synthesis` | the most sensitive driver becomes a thesis-breaker |
| `growth-outlook` | driver moves with dates become catalysts |
| `peer` work | shared inputs are what make a competitor's actions matter |
| `earnings-quality` | the futures path for the commodity |

---

## The failure mode to check for

If this skill runs on a company and returns "oil price, exchange rate, interest
rates", it skipped Step 1 and reached for a generic list. Run it on Thai Union:
it must produce **tuna** without being told, from the cost structure. If it does
not, the reading did not happen.

## Reference files

- `references/driver-derivation.md` — deriving drivers from structure, by business type
- `references/data-sources.md` — where each driver type is found, and what to prefer

## Caveats

- Sensitivity assumes the cost share holds over the range tested. A large move
  changes behaviour — substitution, renegotiation, demand destruction.
- Pass-through is a judgement. The sweep exposes it rather than resolving it.
- Not financial advice.
