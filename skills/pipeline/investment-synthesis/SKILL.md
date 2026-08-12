---
name: investment-synthesis
description: >
  Synthesize a completed business narrative, an intrinsic valuation, and an earnings/
  sentiment read into a decision package — turning story, numbers, and price into a plan
  the way a Damodaran-style analyst would. Use this skill after valuation and earnings work
  is done, or whenever the user asks: "build the investment thesis", "synthesize this into a
  recommendation", "should I buy at this price", "what's my plan for NVDA", "bull/base/bear
  scenarios", "expected return", "margin of safety and sizing", or "what would break the
  thesis". It outputs a one-paragraph thesis, a probability-weighted bull/base/bear scenario
  timeline (12/24/36 months) with expected value, a conditional investment plan (entry,
  margin of safety, sizing, conviction-builders, thesis-breakers), and key risks. Step 5 of the both-stock-analysis
  pipeline; a synthesis step that requires the upstream narrative, valuation, and earnings
  outputs as inputs. It frames a conditional plan, never a buy/sell command — research,
  not advice.
---

# Investment Synthesis

This is where story, numbers, and sentiment become a decision. You have (from earlier steps) a business narrative, an intrinsic value, and a read on how the market is positioned. Your job is to answer: at today's price, what are you paying, what are you getting, what has to be true, and what would you do about it. Work in Damodaran's spirit — value versus price, with honest probabilities and an explicit margin of safety.

You produce a **conditional plan**, not advice. "Below $X with a catalyst, scale in" is analysis; "buy now" is a command you do not give.

**Disclaimer:** Research and educational output only. Not financial advice. Restate this in the output.

---

## Inputs required (input contract)

This step synthesizes; it does not generate the raw material. Confirm you have the following before proceeding — if any is missing, say so and run the relevant upstream step (or ask the user) rather than inventing it:

- **From the business narrative** — the four-pillar story, the 3 P's verdict, the life-cycle stage, and the confidence level.
- **From the valuation** — blended fair value, per-method implied prices, current price, the WACC components, the sensitivity grid, and the Bull/Base/Bear table (with the driver shifts behind each). Also the ROIC−WACC spread and leverage read from the financial-health snapshot, plus the `candidate_hooks` anomaly scan.
- **From earnings** — the recent-quarter execution read (beat/miss + reaction) and the upcoming-quarter setup (consensus, track record, sentiment). The key question: is the stock priced for perfection or for pessimism?

If you are running standalone and these are not on hand, request them — the synthesis is only as good as its inputs.

---

## Step 1: Select the Key Investment Insight

Before writing the thesis, choose the **Key Investment Insight**: the single most important reason this stock may be interesting at today's price. Read `references/hook_patterns.md` when you need examples.

Selection rules:
- Pick one primary hook from the valuation's candidate hooks, or say "No clear investment hook identified."
- The hook must change the risk/reward, not merely be an unusual number.
- Translate it into a comparison the investor can grasp immediately: per share vs current price, % of market cap, % of enterprise value, yield, payout, or fair-value gap.
- Explain it in plain language in 3-5 lines.
- Keep secondary hooks subordinate; do not let a checklist dilute the central idea.

**Suzuki example (pattern, not a rule):** The primary hook is not "Suzuki has a Maruti stake." It is: "Suzuki's ~58.5% Maruti stake is worth about ¥2,080 per Suzuki share, above Suzuki's current share price around ¥1,866; therefore the rest of Suzuki is being valued at little or negative residual value."

---

## Step 2: The thesis paragraph

Write one tight paragraph in Damodaran's voice and open from the Key Investment Insight when one exists. It must contain: **what you pay** (current price vs blended fair value, the gap), **what you get** (the business and where its value comes from — which driver), **what has to be true** (the one or two narrative claims the value hinges on), and **the asymmetry** (is the downside protected by asset value / a low multiple, or is this priced for flawless execution?). No hedging filler — a reader should finish it knowing the bet.

---

## Step 3: Scenario timeline + expected value

Map the valuation's Bull/Base/Bear onto a timeline, fold in catalysts and the sentiment read, then weight by probability. Anchor every target to the Step-3 fair value and its drivers — do not invent prices the valuation does not support. The construction method (how targets grow over time, the expected-value math, probability discipline) is in `references/scenario_math.md` — read it.

| Scenario | What has to happen (levers) | ~12 mo | ~24 mo | ~36 mo | Implied return | Prob. |
|---|---|---|---|---|---|---|
| Bull | growth/margin/catalyst levers from the valuation's bull case | target | target | target | % | p_bull |
| Base | the most-likely path | target | target | target | % | p_base |
| Bear | the thesis-breakers | target | target | target | % | p_bear |

Then compute and state **expected value**: `E[return] = p_bull·R_bull + p_base·R_base + p_bear·R_bear`. Probabilities must reflect genuine conviction (base usually ≥ 50%; avoid the 33/33/33 cop-out, which says you have no view). Note whether the expected value is positive *and* whether the distribution is asymmetric (big upside, protected downside — the setups worth taking).

---

## Step 4: The investment plan (conditional, not a command)

Translate the above into what a disciplined investor would actually do. Keep it conditional and tied to price and evidence:

- **Entry & margin of safety** — at what discount to fair value the risk/reward turns attractive, and *why that much*. The required margin of safety scales with valuation uncertainty (width of the scenario range), business quality (ROIC−WACC spread), and balance-sheet risk (leverage). `references/scenario_math.md` gives a rough sizing guide.
- **Sizing & staging** — conviction × asymmetry sets size; stage entries across tranches or wait for a catalyst/sentiment washout rather than committing at once. If earnings showed the stock is priced for perfection, favour patience; if it washed out, the entry may already be here.
- **Conviction-builders** — the specific data points to watch each quarter that would *raise* conviction (segment growth, margin trend, the ROIC−WACC spread, capex-vs-FCF).
- **Thesis-breakers** — the assumptions that, if wrong, break the thesis. Pull these from the sensitivity grid: the inputs the fair value is most sensitive to are the ones to monitor. Define what observation would make you exit.
- **Horizon** — the time frame each scenario needs to play out.

### Tailor to the setup archetype
The plan differs by what kind of investment this is. Identify the archetype and adjust — full patterns (quality compounder, deep-value/turnaround, cyclical mid-cycle, growth-at-reasonable-price) in `references/thesis_patterns.md`. A quality compounder can be bought near fair value and held; a turnaround demands a large margin of safety, a catalyst, and a smaller position. Match the plan to the archetype, not a one-size template.

---

## Step 5: Key risks

The 3–5 assumptions that move the answer most, plainly stated and ranked by impact. These should map to the thesis-breakers and the most sensitive inputs in the valuation grid — not a generic risk-factor list. For each, note the direction and roughly how much of the fair value is at stake.

---

## Output format

```
# Investment Synthesis — [Company] ([Ticker])

## Key Investment Insight
[one primary hook in 3-5 plain-language lines; or "No clear investment hook identified."]

## Thesis
[one paragraph: what you pay · what you get · what must be true · the asymmetry]

## Scenarios & expected value
[the bull/base/bear timeline table + probabilities + E[return] + asymmetry note]

## Investment plan
- Entry & margin of safety: ...
- Sizing & staging: ...
- Conviction-builders (watch each quarter): ...
- Thesis-breakers (exit triggers): ...
- Horizon: ...
[+ one line naming the setup archetype and how it shapes the plan]

## Key risks
[3-5, ranked by impact on fair value]

## Disclaimer
Research and educational output only. Not financial advice.
```

---

## Caveats
- The synthesis inherits the uncertainty of its inputs; low upstream confidence → wider scenarios and a larger required margin of safety.
- Probabilities are judgement, not fact — state them anyway, because a thesis without them hides its own conviction.
- A conditional plan respects the reader's autonomy and the not-advice line; never collapse it into "buy" or "sell."
- Not financial advice.

---

## Reference Files
- `references/scenario_math.md` — Turning fair value into a 12/24/36-month timeline, the value-to-price convergence model, expected-value math, probability discipline, and the margin-of-safety / position-sizing guide.
- `references/thesis_patterns.md` — Setup archetypes (quality compounder, deep-value/turnaround, cyclical mid-cycle, GARP) and how the plan, sizing, and what-to-watch differ for each.
- `references/hook_patterns.md` — Investment-hook patterns and the Suzuki case example; use as prompts for judgement, not as mechanical rules.
