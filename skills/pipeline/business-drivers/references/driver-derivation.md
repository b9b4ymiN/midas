# Deriving drivers from structure

How to get from "what this company is" to "what moves its earnings", without
reaching for a generic list.

## The four questions

Every driver falls out of one of these. Answer them from the filing before
opening any data source.

**1. What is the largest cost line?**
That line's input price is the primary driver, almost without exception. Food
processor → raw material. Airline → fuel and labour. Retailer → cost of goods
and rent. Software → people. If the largest line is 40%+ of revenue, its price
dominates everything else on this page.

**2. Where does it buy, and where does it sell?**
The FX exposure is the **mismatch**, not the reporting currency. A Thai company
reporting in THB that buys in USD and sells in EUR has two exposures and neither
is THB. Read the currency of the actual transactions.

**3. Which markets set the rules it sells under?**
Tariffs, import quotas, food-safety regimes, price caps. If a policy change can
alter unit economics in a market that matters, policy is a driver.

**4. Do the segments run on different cycles?**
A group where one segment is consumer staple and another is commodity-linked
does not have "a" cycle. Derive drivers per segment and weight by revenue share.

## By business type

| Type | Primary driver | Second | Frequently missed |
|---|---|---|---|
| Food processing | raw material price | FX on imported inputs | tariffs into destination markets |
| Retail | same-store sales | rent and labour | mix shift between formats |
| Airlines | fuel | load factor | fleet lease currency |
| Banks | interest-rate spread | credit costs | funding mix |
| Property | occupancy and rent | financing cost | development completion timing |
| Semis | unit volume and ASP | utilisation | customer inventory cycles |
| Utilities | tariff regime | fuel pass-through | regulatory reset dates |
| Healthcare | volume and payer mix | wage inflation | reimbursement policy |
| Telecom | ARPU and subs | spectrum and capex | regulated termination rates |

Use as prompts for the four questions, never as an answer. A retailer with a
large imported private label is a food processor for driver purposes.

## The materiality test

For each candidate: **if this moved 10%, would anyone notice in the operating
margin?**

Run it through `scripts/sensitivity.py`. If a 10% move costs less than ~0.2
points of margin, it is context, not a driver. Drop it. Three real drivers beat
twelve plausible ones, because the list is meant to be *monitored*, and a list
nobody can monitor gets monitored by nobody.

## Timing — the part that gets skipped

A driver that moves today may not reach reported margin for quarters. Read for:

- **Inventory buffer.** Thai Union held two to four months of tuna cost, so a
  March price move lands in the *next* quarter's margin, not this one.
- **Hedges.** Check the tenor. A hedge does not remove exposure, it delays it.
- **Contract repricing.** Annual contracts mean a mid-year input move shows up
  at renewal.
- **Regulated pass-through.** Utilities often recover input costs on a lag set
  by the regulator — the lag is knowable and belongs in the model.

Get the lag wrong and the model is right about direction and wrong about
quarter, which reads to everyone else as being simply wrong.

## Pass-through

The single assumption that carries the sensitivity result. Evidence for it:

- Did margin hold the last time this input spiked? That is the historical answer.
- Is the product branded or commodity? Branded passes more through.
- Is the customer a concentrated retailer or a fragmented base? Concentration
  cuts pass-through.
- Are contracts fixed-price or indexed? Indexed contracts pass through by design.

State the assumption and the evidence. `sensitivity.py` sweeps the range anyway,
so the reader can see how much the answer depends on it.
