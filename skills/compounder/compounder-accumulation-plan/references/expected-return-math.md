# What a holding would earn, and where the return comes from

A reader who has been told the price asks for roughly what the business can deliver still wants the next thing: *so what would I make?* This is the arithmetic that answers it, and its value is less in the total than in the decomposition — because the three parts behave completely differently over ten years, and only one of them is the business.

Christopher Mayer's *100 Baggers* (2015) is the source of the framing: the enormous long-run outcomes come from earnings compounding **and** the multiple, and studying only the first half explains why so many good businesses produce ordinary results. Mayer's own phrase for it is the twin engine.

---

## The decomposition

```
annual return  ≈  business growth  +  shareholder yield  ±  annual change in the multiple
```

| Part | What it is | Where it comes from |
|---|---|---|
| **Business growth** | Growth in owner earnings **per share** — after dilution, not before it | `durable_growth.nominal` from the thesis pack |
| **Shareholder yield** | Dividends plus net buybacks, less issuance, as a share of market value | The data layer; the per-share view already in `per_share_view` |
| **Multiple change** | The annualised change from today's multiple to the scenario's ending multiple | Today's multiple and this stock's own median, both with their windows stated |

Two things this framing gets right that a single expected-return number does not.

**Per share, not in total.** A business growing owner earnings 12% a year while issuing 3% of its shares is a 9% business to its owners. The compounding work already carries this distinction in `per_share_view`; the return math must not quietly undo it by using a corporate growth figure.

**The multiple is the part that takes it back.** Over ten years, a multiple falling from 35× to its own median of 25× costs roughly 3.3 points a year — enough to turn an excellent business into a mediocre holding. Naming that separately is what stops a plan resting on a business being good while the price already says everyone agrees.

---

## The three scenarios

Not probabilities and not forecasts. Three stated assumption sets, so the reader can see which assumption is carrying the answer.

| Scenario | Business growth | Ending multiple | The question it answers |
|---|---|---|---|
| **growth-slows** | 60% of the durable figure | this stock's own median | What if the engine slows and the multiple lands on its own average? |
| **as-shown** | the durable figure | this stock's own median | What if the business does what it has been doing and the multiple lands on its own average? |
| **no-rerating** | the durable figure | today's multiple | What if the business delivers and the market keeps paying exactly what it pays now? |

**The names describe the assumption, not the outcome.** This matters more than it sounds, and it was learned by getting it wrong: the first version of this table called them weak / central / strong, which quietly assumed that a return to the median is a *headwind*. It is only a headwind when the stock trades above its own median. Copart in August 2026 traded at 23× its own free cash flow against a four-year median of 43×, which made the "strong" path — the multiple holding where it is — the **lowest**-returning of the three. A reader handed that table would have read the labels and drawn the opposite conclusion from the arithmetic.

So the pack carries `multiple_context` alongside the paths, saying explicitly whether a reversion adds to the return or subtracts from it, and the report states that in words before the table.

The 60% haircut in the growth-slows case is a stated convention, not an estimate — it is there to show sensitivity to the growth input, and the report says so rather than dressing it as a forecast.

**The median is a fact, not a judgement.** It is this stock's own median multiple over a stated window — five years at minimum, ten preferred — pulled from the data layer with its window recorded. A median taken over a window that contains a re-rating is not a median of anything; where the window is unrepresentative, say so and widen it.

**A multiple that cannot be sourced makes the path `UNRESOLVED`**, not zero. Assuming no multiple change is an assumption, and an invisible one is worse than a missing number.

---

## Reading the result

The decomposition is the output; the total is a by-product. Three readings worth writing out whenever they appear:

- **The multiple carrying the return.** Where most of the as-shown return comes from the multiple rather than the business, the plan is a bet on sentiment wearing a compounding costume. Say it in those words, and say which direction the bet runs.
- **A slower-growth case that still works.** Where even the growth-slows scenario clears a sensible return, the business is doing the work and the entry price matters less. This is what a `proven-compounder` looks like in the arithmetic.
- **The spread between the three.** A narrow spread means the answer does not depend much on the assumptions; a wide one means the reader is being asked to have a view, and the plan should say which view.

---

## What this is not

- **Not a price target.** No scenario's output is converted into a price, and no ending price is named.
- **Not a probability-weighted expected value.** No weights are assigned, because assigning them would put a judgement where the reader's own belongs.
- **Not a substitute for the expectations reading.** The two answer different questions — one is what the price assumes, the other is what a holding might earn — and a plan uses both.
