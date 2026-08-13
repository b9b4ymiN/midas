# Exclusion rules

What comes out of the earnings base, what stays in, and how to tell.

## The test

> **If nothing changes, will this happen again next year?**

Yes → it belongs in the base, however unusual it feels.
No → exclude it, and write down why.

That is the whole rule. Everything below is it applied to cases people get
wrong.

## Exclude

| Item | Why |
|---|---|
| Gain/loss on disposal of assets, land, a subsidiary | Happens once; the asset is gone |
| Asset revaluation | Accounting entry, no cash, no repeat |
| Impairment / goodwill write-down | Recognition of a past mistake, not this year's operations |
| FX translation gain/loss | Artefact of reporting currency, not operating performance |
| Litigation settlement, insurance recovery | Event-driven |
| One-time tax charge or refund | Not the going tax rate |
| Business-interruption compensation | Event-driven |

## Keep

| Item | Why |
|---|---|
| Import tariffs and duties | Permanent change to the cost of selling in that market |
| New regulation altering the cost structure | Recurs by definition |
| Raw-material price moves | **This is the cycle.** Normalisation averages across it; excluding it defeats the point |
| Restructuring charges taken every year | If it recurs annually it is a cost base, not an event |
| Competitive price pressure | Ordinary operating reality |
| Higher interest expense from higher rates | Real and recurring while rates hold |

## Three cases people get wrong

**FX loss versus import tariff.** Both feel like "not normal operations", both
are handled oppositely. FX translation is a function of where the books are
kept and reverses when the currency does — exclude. A tariff is a permanent
change to the economics of that market until policy changes — keep. Thai Union
reported both in the same quarter: an FX loss, and a US tariff that cost 0.5pp
of gross margin. The FX comes out; the tariff stays in.

**Commodity price spikes.** Tempting to strip out "the year raw materials
spiked". Do not — that year *is* the cycle, and averaging across the cycle is
the entire method. What you should do instead is capture the sensitivity (how
much margin moves per 10% move in the input) and carry it into the scenario
range.

**"Non-recurring" that recurs.** Check whether the same line appeared in the
prior three years. A company taking a restructuring charge annually is not
restructuring; that is how it operates. Keep it.

## Sector-specific items

| Sector | Watch for |
|---|---|
| Banks / insurers | Loan-loss provisioning swings — normalise through the credit cycle, do not exclude; reserve releases flatter a year and reverse |
| Property | Fair-value gains on investment property — exclude, they are revaluation |
| Energy / commodities | Hedging gains and losses — exclude the mark-to-market, keep the realised cost effect |
| Pharma | Milestone and upfront licensing payments — exclude unless the pipeline produces them steadily |
| Retail | Store-closure charges — exclude if a programme with an end, keep if closures are continuous |
| Tech / SaaS | Share-based compensation — **not** an exclusion; decide cash-vs-non-cash once, disclose it, and apply the same treatment to the share count |

## How to report it

Every exclusion needs three fields, so it can be argued with:

```
| Item | Amount | Year | Why excluded | Recurs? |
```

An exclusion with no stated reason is indistinguishable from a number someone
did not like. `stock-grill` should be able to attack this table directly.
