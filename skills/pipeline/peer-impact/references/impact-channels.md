# The three impact channels

Layer 2: keep only candidates whose actions can reach your margin. A candidate
must score on at least one channel. Similarity of business is not a channel.

## Supply — they buy what you buy

**Test:** do they compete for the same constrained input?

The strongest channel, because it does not require the two companies to meet in
any market. A rival on the other side of the world stocking up ahead of a
shortage raises the price you pay, and you may never sell to a single shared
customer.

**Evidence that establishes it:**

- Same raw material named in both companies' filings
- Same sourcing region, fishery, mine, or growing area
- Bidding against each other in the same auction or spot market
- Both disclose exposure to the same published input index

**Why it ranks first:** it is the channel that turns a competitor's *internal*
decision — a capacity expansion, an inventory build — into your cost line, with
no market interaction required and usually no announcement you would notice.

**Weight: 1.0**

## Demand — they sell to who you sell to

**Test:** same buyer, or same shelf?

They cut price and you follow or lose the placement. Concentrated buyers make
this channel sharper: three retailers controlling distribution means a rival's
discount is a direct threat to volume rather than a diffuse market effect.

**Evidence:**

- Named in the same retailer's supplier list
- Same product category in the same geography
- Both bidding for the same contract or tender
- Private-label supplier to a retailer that also carries your brand

**Watch:** "same category" at the global level is too loose. Two companies both
selling frozen seafood in different continents share a category and no customer.
Get to the buyer.

**Weight: 0.8**

## Price — they set what you follow

**Test:** are they large enough that the market price is theirs to set?

You are a follower whether or not you sell to their customers. Their price
becomes your ceiling.

**Evidence:**

- Share large enough to move the published price for the product
- Trade press treats their announcements as the market reference
- Your own filing describes following market prices they influence

**Watch:** rarest of the three and the most over-claimed. Real price setting
needs genuine concentration; in a fragmented market nobody sets the price and
this channel does not apply to anyone.

**Weight: 0.6**

---

## Scoring

```
exposure       = sum of revenue shares of the overlapping segments
channel_score  = weight of the strongest channel
extra          = sum of the remaining channel weights x 0.4
impact         = exposure x (channel_score + extra)
```

**Overlap-weighted**, because a channel touching 47% of revenue is not the same
finding as the same channel touching 7%.

**Diminishing on extra channels**, because being hurt two ways by one competitor
is worse than one way, not twice as bad. Straight addition would rank a
weak-on-three candidate above a strong-on-one, which is the wrong order.

The score ranks. It does not measure — treat it as an ordering device and read
the evidence.

## From a competitor's action to your margin

For a supply-channel peer, the chain is:

```
they add capacity / build inventory
  -> demand for the shared input rises
  -> the input price moves        <- YOUR ESTIMATE, not the script's
  -> your margin moves            <- exact arithmetic, same model as
                                     business-drivers/sensitivity.py
```

The script computes the last step only, and says so. The middle step needs
elasticity, spare capacity and substitution, none of which is knowable to a
useful precision from public data. Estimating it silently would put a made-up
number at the centre of a competitive analysis and give it the appearance of
having been calculated.

State the input move as an assumption, show it, and let the sweep expose how much
the conclusion depends on it.

## Recording the drops

Every candidate considered and rejected needs a written reason. Without it, a
short list of competitors and a thorough search that found few are
indistinguishable to the reader.

It is also what makes the exclusion attackable. *"You dropped this name — on what
basis?"* can be asked of a list that records its rejections; *"did you consider
anyone else?"* is all that can be asked of one that does not, and it is a much
weaker question.
