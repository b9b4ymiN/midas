# From the gap to a plan

The plan is the last thing written and the first thing read. It has one job: to turn everything above it into something a reader can act on **using their own judgement**, without being told what to do.

That distinction is the whole discipline. A conditional plan says what follows from a state of the world; an instruction says what to do. "Below the accumulate band, with the weekly stage no longer falling, build in three parts over two quarters" is a plan. "Buy at 27" is an instruction, and this pipeline does not give instructions.

---

## The bands

Three, always, each a range with the condition that defines it.

| Band | Defined by | What it says |
|---|---|---|
| **Accumulate** | at or below the price at which the market's implied growth equals the engine's durable growth **less the archetype's cushion** | The price is asking for less than the business has shown, with room to spare |
| **Hold, do not chase** | between that price and the price at which implied growth exceeds durable growth by the archetype's stretch | The price asks for roughly what the business does. Hold what you own; do not build |
| **Too demanding** | above that | The price assumes growth the work did not find evidence for |

An **Accumulation Band** boundary is produced by inverting the expectations arithmetic — the same calculation as the implied-growth solve, run in the other direction. Three rules keep it from becoming a target price:

1. **It is stated as a condition, not a value.** Every band carries the sentence that defines it: what growth the market is asking for at that price, against what the engine has shown. The number is the consequence of the condition, not the point of it.
2. **It moves with the required-return assumption, and it is shown moving.** The band is reported across the same sensitivity range as the implied growth. A band quoted as a single price has thrown away the honest part.
3. **It is never called a target, a fair value, or an objective**, and no upside percentage is computed from it. There is nothing to be "up to".

Where the expectations reading is `UNRESOLVED`, there are no bands. The plan then rests on the return paths and the staging, and says so.

### When the bands stop discriminating

The band construction assumes the price sits somewhere near what the engine could justify. Where the gap is very large it does not, and the arithmetic produces an accumulate ceiling far above anything the stock trades at — every price a buyer could pay lands in the same band, and the three bands answer nothing.

`band_discrimination` reports this: where the accumulate ceiling is more than twice the current price, the pack is marked `BANDS_DO_NOT_DISCRIMINATE`. The report must then say so in words rather than quoting a ceiling nobody will ever see. The finding is still real — the price is nowhere near what the engine could justify — but the plan's shape has to come from the staging and the kill conditions instead of from the bands.

This was found by running the pipeline on a company trading below a no-growth perpetuity. It is not a rare case: it is what any cheap stock with a strong measured engine produces.

---

## Staging

How a position gets built, and this is where `stage_pack` earns its place. The chart does not decide whether to own the business — the compounding work did that — but it does say whether the market is currently disagreeing, and building into a monthly stage 4 means buying from someone who has been right so far.

| Stage alignment | What the staging does |
|---|---|
| `MARKET_HAS_NOT_PRICED_IT` | The most favourable case for building: the price has not moved with the economics. Build on the band alone. |
| `MOVING_TOGETHER` | Ordinary. Build on the band, in parts rather than at once. |
| `LATE_AND_EXTENDED` | The price has run ahead of a business that stopped growing into capital. Require the band, and expect it to be a long wait. |
| `MARKET_SEES_DAMAGE_FIRST` | Something may be wrong that the filings have not shown. Hold building until either the pending stage change confirms an end to the decline, or the open question that would explain it is answered. Say which. |

Staging is expressed in **parts and conditions**, never in a schedule of dates and amounts. "Three parts, the second only after the next annual report confirms capital spending came down" is a plan a reader can follow and check.

---

## The rules, wired to work that already exists

The plan invents no new triggers. Everything it watches is already named upstream, which is what makes it checkable later.

- **`add_rules`** — from `upgrade_conditions` in the thesis pack. Each names a metric, a direction, and a threshold a future filing can settle.
- **`pause_rules`** — from the stage reading and the data gaps: what would make building stop without meaning the thesis is wrong.
- **`exit_rules`** — from `kill_conditions`. These are the thesis breaking, not the price falling. A price move is not a kill condition, and writing one in as though it were is how a plan quietly becomes a stop-loss.
- **`plan_review`** — from `review_schedule`, plus anything the plan itself must check sooner. The verdict's `expires_on` is the plan's expiry too: past it, the plan may not carry a decision until the analysis is re-run.

**`position_bounds`** states the size range the plan's arithmetic was written against, with the reasoning — a starter position for `emerging-starter`, a full one for `proven-compounder`. It is a bound on the plan, not advice about anyone's portfolio, and it never appears as a single number or a percentage of someone's money.

---

## The self-check

Before the plan goes into the report:

1. Is every line conditional? Search for the imperative — buy, sell, take, exit now — and rewrite each one as a condition.
2. Does every threshold name something a future filing or a stated stage event can settle?
3. Is there a band quoted without the condition that defines it, or without its sensitivity?
4. Is there a price anywhere that is doing the work of a target?
5. Do the exit rules come from the thesis breaking rather than from the price falling?
6. Does the plan say when it expires, and what would force an earlier look?
7. Would a reader who disagrees with the required-return assumption be able to see exactly which conclusions move, and by how much?
