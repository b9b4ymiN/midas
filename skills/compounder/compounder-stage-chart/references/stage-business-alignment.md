# Crossing the chart stage with the business life cycle

The chart stage says what the market has concluded. The business life-cycle stage — `economic_engine_pack.life_cycle_stage`, read from the direction of the three cash-flow statements rather than from a story — says where the business actually is. Neither is worth much alone. Crossed, they answer a question a reader always has and rarely gets answered: **is the market ahead of this business, behind it, or with it?**

The divergences carry the information. Agreement mostly confirms that nothing surprising is happening.

---

## The two inputs

**Business stage** comes in as received, both figures: the adjusted stage and the raw stage. Where the two differ, the adjustment is stated when the alignment is written, because a business that only reads as Mature after securities flows are excluded is a different reading from one that reads Mature outright. Valid values are `Introduction`, `Growth`, `Mature`, `Shake-out`, `Decline`, and `UNRESOLVED`.

**Chart stage** is the monthly read from `stage-classification.md`, with the weekly used to say whether the monthly reading is currently strengthening or weakening. The monthly is the one crossed; the weekly is the qualifier.

Where either input is `UNRESOLVED` or `TRANSITIONAL`, the alignment is `UNRESOLVED` with the missing side named. It is never guessed from the other side.

---

## The four readings

| Business stage | Chart stage 1 or 2 | Chart stage 3 or 4 |
|---|---|---|
| **Introduction / Growth** | `MOVING_TOGETHER` | `MARKET_SEES_DAMAGE_FIRST` |
| **Mature / Shake-out / Decline** | `MARKET_HAS_NOT_PRICED_IT` (stage 1) · `LATE_AND_EXTENDED` (stage 2) | `MOVING_TOGETHER` |

### `MARKET_HAS_NOT_PRICED_IT`

A business whose economics are working while the chart has gone nowhere for a long time — most often a Mature business earning well on new capital with a chart in a flat base. Two explanations fit, and the reading names both: the market has not yet noticed, or the market has noticed something the reported economics have not shown yet.

The reading does not choose between them. What it does is send the reader to the counter-thesis and the data gaps with a specific question — *is there anything in the open questions that a patient seller would already know?*

### `MOVING_TOGETHER`

The chart and the business are telling the same story, in either direction: a Growth business in a monthly advance, or a Declining business in a monthly decline. The least interesting reading and the most common. Say so plainly and keep it short — a paragraph, not a section.

The one thing worth adding is *how long* they have agreed. A stage 2 that began eight years ago inside a business still in Growth is a different fact from one that began five months ago.

### `LATE_AND_EXTENDED`

A Mature or Shake-out business in a long chart advance. The business has stopped growing into new capital, and the price has been rising anyway — so the rise is being paid for by the multiple rather than by the engine. This is the reading that most often precedes disappointment, and it is the one where the accumulation layer's Expectation Gap matters most: if the price already assumes more growth than the engine can deliver, this reading is the visible half of that arithmetic.

### `MARKET_SEES_DAMAGE_FIRST`

A business still reading as Introduction or Growth, with a chart in a top or a decline. Markets are frequently early to damage that has not reached the filings, and cash-flow-based life-cycle reads are, by construction, backwards-looking.

This is the reading that most deserves a `SCOPE_CHALLENGE` check. It does not by itself change a verdict — a chart may never do that — but a sustained monthly stage 4 against a Growth business is a prompt to ask whether the Layer 0 frame or the Layer 1 growth decomposition is still describing the business the market is looking at.

---

## Writing the reading

Write it as a sentence with the dates in it. The label is for the pack; the reader gets prose.

- **Usable:** "The business is still reinvesting at high returns, but the chart has been in a monthly decline since March 2025 and the weekly has not recovered — either the market has seen something the filings have not shown yet, or it is wrong, and the open question about contract renewals is the place that would settle it."
- **Not usable:** "Divergence detected: business Growth vs chart Stage 4. Bearish."

Three things belong in the sentence: what each side says, since when, and where in the report a reader can go to settle the disagreement.

---

## The standing limits

- The alignment reading **never issues an instruction.** No buy, sell, wait, accumulate, or avoid. It describes a relationship between two readings and stops.
- It **never revises a verdict, a leg rating, or an evidence class.** A chart is not evidence about a business's economics. Where the divergence is severe enough to matter, the response is `SCOPE_CHALLENGE` and a re-run of the core layers.
- It **carries no price levels** — no support, no resistance, no entry, no stop. Those are the timing line's business.
- Where the business stage is `UNRESOLVED`, the chart read is still reported on its own. Half a reading, labelled as half, is more useful than a fabricated cross.
