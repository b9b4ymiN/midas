---
name: peer-impact
description: >
  Find the competitors whose actions can actually move this company's earnings —
  searching worldwide by revenue mix, then filtering by whether they compete for
  the same input, the same customer, or set the price. Use when the user asks
  "who are the real competitors", "who competes with TU", "what if a competitor
  adds capacity", "who else buys this input", or before any competitive-risk
  section. NOT the peer set for a multiples table: that wants companies the
  market prices with the same logic, which is a different question and already
  handled by company-valuation's Peer Validation Gate. Outputs a ranked table
  with the impact channel, the revenue exposed, and — for shared-input peers —
  the margin arithmetic. Step 3.5 of the both-stock-analysis pipeline.
  Research and educational output only — not financial advice.
---

# Peer Impact

Which competitors can move your earnings, and through what.

**Disclaimer:** Research and educational output only. Not financial advice.

---

## Two peer sets, one of which already exists

| | Valuation peers | Impact peers |
|---|---|---|
| **Question** | who does the market price with the same logic? | whose decisions change our margin? |
| **Used in** | the multiples table, §3 | competitive risk, drivers, thesis-breakers |
| **Owned by** | `company-valuation`'s Peer Validation Gate | this skill |
| **Constraint** | same sector, same region — cross-sector is a hard reject | **no country constraint at all** |

They overlap and are not the same set. A domestic food company selling unrelated
products is a reasonable valuation comp and completely irrelevant to earnings; a
Korean tuna processor competing for the same fish is the reverse.

**This skill does not touch the Peer Validation Gate.** That gate is correct for
its purpose and stays as it is.

---

## Layer 1 — search worldwide, by revenue mix

Start from the segment mix — from the **filing**, not a data provider, and
cross-checked if it came through the data layer (see `har-to-api`'s segment
rule). Then look for companies with a similar mix, **without a country filter**.

For Thai Union, the mix that drives the search:

| Segment | Share of gross revenue | Who to look for |
|---|---|---|
| Ambient seafood (canned tuna) | 47.2% | global tuna processors — Korea, US, Europe |
| Frozen and chilled | 27.8% | frozen seafood and shrimp exporters — Asia, Latin America |
| Pet food | 16.0%* | wet pet-food manufacturers — a different sport entirely |
| Value-added | 7.5%* | too small to define a competitor set |

<small>*shares of the TTM total; the mix shifts between reporting bases, so state which you used</small>

Restricting the search to the home market by GICS sector returns domestic food
companies selling different products, and **misses every real competitor**,
because they are all abroad. That failure is the reason this skill exists.

Full method in `references/finding-peers.md`.

## Layer 2 — keep only what can reach your margin

Three channels. A candidate must score on at least one.

| Channel | Test | Why it counts |
|---|---|---|
| **Supply** | do they buy the same constrained input? | The strongest, because it works even if you never meet in a market. A rival stocking up raises the price you pay. |
| **Demand** | same buyer, or same shelf? | They cut price, you follow or lose placement. |
| **Price** | large enough to set the market price? | You are a follower whether or not you sell to their customers. |

**Everything that scores on none is dropped — however similar the business
looks.** The criterion is impact, not resemblance.

Scoring is **overlap-weighted**: a channel touching 47% of revenue outranks the
same channel touching 7%. Multiple channels compound, with the second and third
counting less than the first — two ways of being hurt by one competitor is worse
than one, not twice as bad.

```bash
python scripts/peer_impact.py --candidates peers.json \
  --margin 0.0487 --cost-share 0.55 --pass-through 0.6 --input-move 0.10
```

Where a supply-channel peer exists and you supply the input price move their
action would cause, the script chains into the **same margin arithmetic as
`business-drivers/sensitivity.py`** — so "they add capacity" becomes "we lose N
points of margin". The script does not model the capacity-to-price step; that is
your estimate, and it says so.

Full scoring rules in `references/impact-channels.md`.

---

## Write down who you dropped

The output has a **considered and dropped** section, and it is not optional.

Without it a reader cannot tell a thorough search from a lazy one — an empty
competitor list looks identical whether you searched the world and found nothing
or searched one country and gave up. It also gives `stock-grill` something to
attack: *"you dropped this name — on what basis?"* is a better question than
*"did you consider anyone else?"*, and only the first can be asked of a list that
records its exclusions.

The script warns when a candidate is dropped with no reason recorded, and when
one is **kept** on a channel claim with no evidence — an asserted channel cannot
be argued with either.

---

## Output contract

- **Ranked table**: competitor · country · channels · revenue exposed · score
- **Evidence per channel** — what you read that establishes it
- **Considered and dropped**, with reasons
- **Margin arithmetic** for shared-input peers
- **What you could not establish**, said plainly

Feeds forward:

| To | What |
|---|---|
| `investment-synthesis` | competitive risk in the ranked key risks |
| `business-drivers` | shared-input peers confirm the driver matters and who else pulls on it |
| `growth-outlook` | a competitor's capacity decision with a date is a catalyst |
| `stock-grill` | both the kept and the dropped list are attackable |

---

## Reference files

- `references/finding-peers.md` — the worldwide search by revenue mix, and why the country filter has to come off
- `references/impact-channels.md` — the three channels, evidence each requires, and the scoring

## Caveats

- Impact scoring ranks; it does not measure. The margin arithmetic is exact, but
  the input move it consumes is a judgement.
- Segment mix from a data provider carries the provider's labels and uneven
  coverage — cross-check against the filing before the search rests on it.
- Not financial advice.
