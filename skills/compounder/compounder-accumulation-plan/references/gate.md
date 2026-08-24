# The gate, and the three plans it selects

Most of the value in this layer is in what it refuses to do. A plan written for a business the compounding work did not clear is worse than no plan, because it dresses a rejection up as an opportunity and gives the reader a price to act on. So the gate runs first, it runs on the thesis pack alone, and it never sees a price.

It is mechanical for one reason: a judgement call here would drift, and it would drift permissively. Every company looks worth a plan after a day spent reading about it.

`scripts/gate.py` is the executable copy of this file. Where the two disagree, the file is the specification and the script is the defect.

---

## Passing

All five must hold:

| Condition | Required | Why |
|---|---|---|
| `compounding_potential` | `Exceptional`, `Strong`, or `Moderate` | Below Moderate the work found a business that does not compound. A cheap price does not fix that. |
| `compounder_class` | not `Not a Compounder` | The categorical reading survives changes in the label, and this is the one value that means "whatever the grade says, do not accumulate this". |
| `leg_ratings` | no leg rated `Broken` | One broken leg is enough. A plan cannot compound through a broken balance sheet or a broken return. |
| `leg_ratings` | no leg `UNRESOLVED` while potential is above Moderate | A verdict of Strong or better resting on an unread leg is not a verdict yet. At Moderate an open leg is tolerated, because Moderate already says the case is incomplete. |
| `review_schedule.expires_on` | not in the past | Past its expiry a verdict may be read as history, but it may not carry a decision. |

**Moderate passes on purpose.** The instruction this gate was built to follow was "the ones with real potential, or a genuinely interesting business model" — and `Great Business, Narrow Runway` is exactly that: excellent economics with nowhere to put the money. It lands at Moderate almost by construction, and excluding it would throw away the most interesting case this pipeline finds.

## Blocking

A `BLOCKED` gate is a legitimate outcome, not a failed run. It writes an `accumulation_pack` carrying:

- `gate: "BLOCKED"` and `gate_reason` — every condition that failed, in plain words.
- `unblock_conditions` — what would have to change. Each one names evidence about the business, never a lower price. A blocked gate is not waiting for the stock to fall.
- The review date, so the reader knows when the question gets asked again.

And nothing else. No price, no band, no staging, no sizing. The pack validator enforces this: a blocked pack with populated plan fields fails.

The report then closes at the verdict, with a short section saying what was found, why it stops there, and what would reopen it.

---

## The three archetypes

A pass selects one, and it changes the plan's shape more than any other input.

| Selected when | Archetype | What the return depends on |
|---|---|---|
| `compounder_class` is `Great Business, Narrow Runway` | `narrow-runway` | The entry price. The business cannot absorb capital at its own returns, so there is no compounding to wait for — what you pay is most of what you get. |
| Evidence maturity is `Early` or `Developing`, or the class is `Emerging Candidate` | `emerging-starter` | Evidence arriving. The business may turn out to be excellent; not enough is known yet to size a position on it. |
| Anything else that passed | `proven-compounder` | Time held. The business does the work, so the entry price matters least of the three. |

Where both the narrow-runway and the emerging conditions hold, **narrow-runway wins**. An unabsorbable runway is a fact about the business that more evidence will not change; shallow evidence is a fact about what we know, which time fixes.

### What each archetype changes

| | `proven-compounder` | `emerging-starter` | `narrow-runway` |
|---|---|---|---|
| Cushion demanded below the engine's growth | none | 2 points | 3 points |
| Price above the engine's growth still tolerated | 1.5 points | 1 point | none |
| Staging | regular, over time, largely price-insensitive | small starter, additions conditional on named evidence | conditional on the band, patient, no regular schedule |
| Size the plan is written against | full | a fraction, with the rest held back for the evidence | full, but only inside the band |
| What ends it | a kill condition | evidence failing to arrive by a stated date | the price leaving the band, or a kill condition |

The asymmetry between the first and last row is the point. A proven compounder is damaged by waiting for a perfect price; a narrow-runway business is damaged by not waiting for one.

---

## What the gate must never do

- **Never be overridden by judgement.** If the gate is wrong, the thesis pack is wrong, and the fix belongs upstream where the evidence lives.
- **Never look at price.** Not to break a tie, not to soften a block, not at all.
- **Never revise the verdict.** It reads the pack; it does not edit it.
- **Never treat a block as a "wait for a better price".** The unblock conditions are about the business.
