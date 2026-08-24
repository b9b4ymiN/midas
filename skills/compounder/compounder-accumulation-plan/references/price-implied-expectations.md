# Reading what the price already assumes

The ordinary way to bring price into an analysis is to build a value and compare. That is `company-valuation`'s job on the valuation line of this repo, and it is a good job done properly there. It is the wrong instrument here, for two reasons: it would import a whole model's worth of new assumptions into a layer that is supposed to be a comparison, and it would end in a number — a fair value — that the compounding line has spent five layers deliberately not producing.

The instrument used instead is Rappaport and Mauboussin's, from *Expectations Investing* (2001, revised 2021): **take the price as given and solve for what it assumes.** The price is the input, the expectation is the output, and no valuation is produced at any point.

---

## The arithmetic

Owner cash flow per share grows at `g` for ten years, then at a terminal rate forever, discounted at a stated required return. Solve for the `g` that makes the total equal today's price.

```
price = Σ  F₀(1+g)ᵗ / (1+r)ᵗ   for t = 1..10
      +   [F₀(1+g)¹⁰(1+gₜ) / (r − gₜ)] / (1+r)¹⁰
```

`scripts/plan_math.py` solves it by bisection. Five inputs, and every one of them is stated in the pack:

| Input | Where it comes from |
|---|---|
| `price` | Last close, with its date. Not an average, not a round number. |
| `F₀` — owner cash flow per share | The data layer, with the definition used stated: free cash flow after maintenance investment, per share on the current count. |
| `r` — required return | **An assumption.** See below. |
| `gₜ` — terminal growth | Long-run inflation by default, 2.5%, moved in the sensitivity. |
| Horizon | Ten years by default, stated. |

---

## The required return is an assumption, and it is declared as one

This is the input that would normally be a WACC. It is not one here, deliberately.

A cost of capital derived from a beta, an equity risk premium, and a cost of debt looks like a measurement and is not one — small changes in inputs nobody can observe move it by more than a point, and the number arrives at three decimals carrying a precision the inputs never had. Worse, deriving it would drag the whole apparatus of `company-valuation` into a layer that exists to make one comparison.

So: **state it, do not derive it.** A long-run equity return assumption, declared with its basis, and then moved:

- Reported at the stated rate, and at that rate **plus and minus two points**.
- The terminal rate moved **plus and minus one point** at the same time.
- The full grid goes in the pack as `price_implied_expectations.sensitivity`, and into the report's appendix.

A single implied-growth figure without its band is a false precision, and the pack validator rejects it.

---

## The Expectation Gap

Compare the solved growth against `durable_growth` from the thesis pack — the growth the compounding work concluded the engine can actually deliver, derived from what new capital earns and how much of it can be put to work.

| Reading | When | What it means in words |
|---|---|---|
| `PRICE_ASKS_LESS` | implied is more than 1.5 points below durable | The price assumes less than the business has shown. The gap is the reader's margin. |
| `PRICE_ASKS_ABOUT_THE_SAME` | within 1.5 points either way | The price assumes roughly what the work found. Nothing is being given away, and nothing outrageous is being demanded. |
| `PRICE_ASKS_MORE` | implied is more than 1.5 points above durable | The price assumes growth the work did not find evidence for. Something has to arrive that the analysis did not see. |
| `UNRESOLVED` | the arithmetic could not run | Say so, and say why. |

The 1.5-point tolerance exists because neither side is precise to a point. Reporting a 0.4-point gap as a finding would be reading noise.

### Both sides on the same basis

`durable_growth` carries a nominal figure and a real one. Implied growth solved from nominal cash flows is **nominal**, so it is compared against `durable_growth.nominal`. Comparing a nominal implied growth against a real durable growth manufactures a gap of roughly the inflation rate out of nothing. The pack records which basis was used, on the same line.

---

## When it cannot run

Three cases, all common, all handled by saying so rather than by forcing a number:

- **Owner cash flow is zero or negative.** There is no stream to run backwards. Record `UNRESOLVED` with that reason.
- **A bank or an insurer.** Free cash flow does not carry its usual meaning where capital is the raw material; the sector routing already sends these names elsewhere in this pipeline, and the same applies here.
- **The price sits outside the range the arithmetic can express** at the stated required return — which usually means the required return assumption is doing more work than the growth rate is. Record `UNRESOLVED` and say which input is binding.

In every case the plan continues on the expected-return paths alone, and says in the body that the expectations reading was not available. A missing reading, labelled, is worth more than a fabricated one.

---

## What this is not

- **Not a valuation.** No fair value is computed, and the output is a growth rate, not a price.
- **Not the Reverse Reality Check.** That starts from a 10x business outcome and asks whether the required world is plausible. This starts from today's price and asks what it is already paying for. Different question, different direction, different layer.
- **Not a signal.** A gap is a comparison. What to do about it is the plan's business, and the plan is conditional.
