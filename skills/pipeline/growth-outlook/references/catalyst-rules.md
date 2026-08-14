# Catalyst rules

## No date, no row

The repo's decision-journal template already says it: *"catalyst + deadline — no
deadline = wishful thinking."*

A catalyst without a window cannot be waited for and cannot falsify anything. If
the best available is a quarter or a half, use that — a window is a date. If not
even that, it is a hope, and hopes do not go in the table.

## The verification column

Every row needs **how you would know it happened**. This is the column people
skip and the one that does the work.

A catalyst you cannot verify has occurred is indistinguishable from one that
never occurs — you will still be waiting a year later, unable to say whether the
thesis failed or is merely early. It is also what makes the claim attackable in
`stock-grill` R5: *"you said this would happen by Q3 — has it, and what are you
reading to tell?"*

Good verification columns are specific and cheap to check:

| Weak | Strong |
|---|---|
| "margin improves" | "COGS/revenue below 80% in the Q3 release" |
| "tariffs resolved" | "USTR publishes the revised schedule" |
| "capacity comes online" | "management confirms commercial operation date on the call" |
| "sentiment turns" | — not verifiable; drop the row |

## Certain-to-occur versus might-occur

Separate them. An earnings date is **certain**; what it reveals is the catalyst.
Writing "Q3 earnings" as a catalyst says nothing — write what you expect the
print to settle.

| Kind | Example | Confidence field |
|---|---|---|
| Scheduled | results, AGM, index review, lock-up expiry | occurrence certain; outcome unknown |
| Conditional | tariff review, contract renewal, approval decision | both uncertain — state each |
| Driver-mechanical | inventory buffer runs out, hedge rolls off | occurrence near-certain, timing knowable from `business-drivers` |

That third kind is the most useful and the most often missed. It is not news; it
is arithmetic already in motion. Thai Union's two-to-four-month tuna buffer means
a March cost move **will** reach margin around Q3 — no announcement required.

## Sizing

"Positive" is not usable. Take the magnitude from `business-drivers`'
sensitivity output where one exists:

> tuna +10% → −2.3pp operating margin at 60% pass-through → roughly −3.1bn THB
> of operating income, landing Q3

Where no number exists, say the magnitude is unquantified rather than reaching
for an adjective.

## Ordering

Rank by **expected impact**, not by date. A large event nine months out matters
more than a small one next week, and a table sorted by calendar buries it.

## Handing to R5

`stock-grill`'s final round pre-commits kill criteria and a review date. The
catalyst table is what it draws on: the earliest dated catalyst that would
materially change the thesis **is** the natural review date. Set it there rather
than picking a round number of months.
