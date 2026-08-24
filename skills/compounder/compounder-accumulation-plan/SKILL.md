---
name: compounder-accumulation-plan
description: Use when a company has already cleared the compounding work and the remaining question is what to do about it at today's price — "the business passed, now what", "how would I build a position in this", "is it already priced for perfection", "what growth is the market assuming", "where would I add and where would I stop", or "write the accumulation plan". It reads what the share price already assumes, compares that against the growth the business has shown it can deliver, and turns the difference into price bands and a conditional plan. It produces no fair value and no target price.
---

# Compounder Accumulation Plan

## Overview

The compounding work answers whether a business can keep compounding. It says nothing about whether today's price leaves anything for the buyer. This skill closes that gap without turning into a valuation.

The method is expectations-first, from Rappaport and Mauboussin's *Expectations Investing*: instead of building a value and comparing it to the price, **run the arithmetic backwards from the price** and read out the growth it already assumes. Then set that against `durable_growth` — the growth the compounding work concluded the engine can actually deliver. The distance between the two is the **Expectation Gap**, and it is the only price judgement this skill makes.

That framing matters. "The stock is worth $X" invites an argument about the model. "At this price the market is asking for 14% a year, and the work found 9%" is a comparison a reader can check, argue with, and act on their own judgement about.

## The gate comes before anything else

Run the gate before reading a single price:

```bash
python skills/compounder/compounder-accumulation-plan/scripts/gate.py \
    run/<TICKER>-<DATE>/compounder_thesis_pack.json --run-date <YYYY-MM-DD>
```

Read `references/gate.md` for what it decides and why. Two outcomes:

- **`BLOCKED`** — write `accumulation_pack` with the block, the reasons, the conditions that would unblock it, and the review date. **Stop there.** No price is read, no band is computed, no plan is written. A company the compounding work did not clear does not get a price opinion, and the report closes at the verdict.
- **`PASSED`** — the gate also names the `plan_archetype`, which changes the shape of everything below it.

The gate is mechanical so it cannot drift. Do not override it by judgement; if it is wrong, the thesis pack is wrong, and that is where the fix belongs.

## Step 1: What is the price asking for?

Read `references/price-implied-expectations.md`, then:

```bash
python skills/compounder/compounder-accumulation-plan/scripts/plan_math.py \
    --price <last close> --fcf-per-share <owner cash flow per share> \
    --required-return 0.09 --durable-growth <durable_growth.nominal> \
    --archetype <from the gate> --out run/<TICKER>-<DATE>/plan_math.json
```

Three things this step must get right:

- **The required return is an assumption, and it is declared as one.** It is not derived into a single cost of capital, because a number derived to three decimals invites a precision the input does not have. State it, move it plus and minus two points, and show what that does.
- **Both sides of the comparison sit on the same basis.** Implied growth solved from nominal cash flows is compared against `durable_growth.nominal`, never against the real figure. Mixing them manufactures a gap that is not there.
- **Where it cannot run, it says so.** Negative owner cash flow, a financial company whose cash flow statement does not carry the meaning, or a price outside what the arithmetic can express — all produce `UNRESOLVED` with the reason, and the plan proceeds on the return paths alone.

## Step 2: What would it earn from here?

Read `references/expected-return-math.md`. Decompose a ten-year holding-period return into business growth, shareholder yield, and the change in the multiple, across three stated assumption sets. This is the twin-engine arithmetic behind Mayer's *100 Baggers* — most long-run return comes from the business, and the multiple is the part that can quietly take it back.

Every input needs a source. The median multiple in particular is a historical fact about this stock, not a judgement, and it comes from the data layer with its window stated.

## Step 3: Turn the gap into bands

Read `references/accumulation-plan.md`. The bands come from inverting Step 1: the range of prices over which what the market asks stays at or below what the business has shown it can deliver, less the cushion the archetype requires.

A band boundary is a break-even for a stated set of assumptions. It is **not a fair value and not a target price**, it is always a range, and it never appears without the sensitivity that produced it.

## Step 4: Write the plan

Conditional, always. "Below the accumulate band with the weekly stage no longer falling, build in three parts" is a plan. "Buy now" is an instruction, and this skill does not give instructions.

The plan wires into work that already exists rather than inventing new triggers: `kill_conditions` and `upgrade_conditions` from the thesis pack become the exit and add rules; `stage_alignment` and the pending stage change from `stage_pack` set the staging; `review_schedule` sets when the plan is looked at again.

## Step 5: Write and validate the pack

```bash
python skills/compounder/future-compounder/scripts/validate_pack.py run/<TICKER>-<DATE>/ --stage accumulation_pack
```

## What this skill does not produce

- **No fair value, no blended value, no target price, and no target price by another name.** The bands are conditions, not valuations.
- **No entry trigger, stop, or R-multiple.** Those are the timing line's work.
- **No portfolio sizing.** `position_bounds` states the size range the plan's arithmetic was written against; it does not size anyone's portfolio.
- **No revision upstream.** A price reading may never change a verdict, a leg rating, or an evidence class.

## DoD

`accumulation_pack` carries the gate outcome with its reasons; where it passed, the `plan_archetype`, the required-return assumption with its sensitivity, the price-implied expectations with their sensitivity table, the Expectation Gap on a stated basis, three decomposed return paths, three bands each with the condition that defines it, staging tied to the stage reading, add / pause / exit rules wired to the thesis pack's conditions, position bounds with their reasoning, and the review schedule. Every figure that moves with the required-return assumption is shown with the range it moves across.

**STOP:** Do not compute a fair value, name a target price, issue a buy or sell instruction, size a portfolio, or write any plan at all when the gate is BLOCKED.

---

Research and educational output only. Not financial advice.
