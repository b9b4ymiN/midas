# Question Bank — 5 Rounds

The full question set for each round. Read at the start of each round. Terms are defined inline where used below; the repo's root `CONTEXT.md` is the authoring reference for the maintainer.

## Core mechanic (recap)

- **Frontier:** in each round, ask only the questions whose prerequisites are settled. Ask as a numbered set, give a ➡️ recommended answer, then wait for the user to answer one round at a time. Do not dump everything.
- **Facts are your job:** anything you can look up (price, historical drawdown, consensus, sensitivity grid, peer comparison) — find it yourself, do not ask the user. Dispatch a sub-agent / yfinance / the source skill's output files.
- **Decisions are the user's job:** confidence %, sell trigger, hold/exit — put them to the user and wait.
- **Round order matters:** R1 must come first (pre-mortem is independence hygiene — the user must generate the bear case before seeing the aggregate).

---

## R1 — Pre-mortem (prospective hindsight)

**Why first:** prospective hindsight yields ~30% more failure causes (Mitchell/Russo/Pennington 1989) and lowers the social cost of dissent — because failure is "assumed to have happened," not debated.

**Procedure (strict):**

1. Set the frame: _"It is 12 months from now; this stock is down 40% embarrassingly. Tell me what caused it."_
2. **Do NOT reveal your analysis first** — have the user write their own failure causes first (independently). Enforce this.
3. Wait for the user to give 3-5 causes.
4. Only then supplement: cross-check against thesis-breakers and the most sensitive inputs in the grid; add failure modes the user may have missed (e.g. whole-sector drawdown, key-man risk, regulatory).
5. Rank jointly by likelihood × impact.

**Core questions:**
- ❓ Q1: _"Assume -40% in 12 months — list 3-5 causes (before I add mine)."_ ➡️ recommended: start from the thesis-breakers you already have.
- ❓ Q2: _"Ranking by likelihood × impact — which is the scariest?"_ ➡️ recommended: the one that flips a core assumption, not a quiet known one.

**Find yourself (do not ask the user):** the stock's historical max drawdown · the sector's beta during market stress · points where the stock has drawn down with the whole sector.

---

## R2 — Sensitivity attack

**Input required:** the sensitivity grid from `company-valuation` (the inputs that move fair value the most) + the blended fair value.

**Procedure:**

1. Identify the input that moves fair value the most (from the grid).
2. Challenge whether that assumption is defensible vs history + peers — find this yourself.
3. Ask the user whether that assumption is "calculated" or "hoped."
4. Stress: if the input is wrong by 20% — what does fair value become, and do you still hold?

**Core questions:**
- ❓ Q1: _"Your fair value is X% terminal value — is this terminal growth/margin realistic vs the 10-year history?"_ ➡️ recommended: compare to the historical average of that metric.
- ❓ Q2: _"If [the most sensitive input] is wrong by 20% — fair value = ? Do you still hold at this price?"_ ➡️ recommended: compute before deciding.
- ❓ Q3: _"Which assumption feels 'hoped' rather than 'calculated'?"_ ➡️ recommended: the one with no historical anchor.

**Find yourself:** the 10-year historical average of the sensitive input · peer median · how far above/below history the assumption sits.

---

## R3 — Variant perception stress (CFA 5 dimensions)

**Core idea:** alpha is not in a more accurate cash-flow estimate, it is in the divergence between you and the market. If you cannot answer "why am I right and the market wrong," there is no real variant perception — buying is then just going with the flow.

**The 5 dimensions to probe (one by one):**

| Dimension | Question |
|---|---|
| **Fundamental** | _"What do you believe about the fundamentals (growth/margin/returns) that the market does not?"_ |
| **History** | _"What historical pattern / mean-reversion are you relying on that the market is overlooking?"_ |
| **Policy** | _"Is there a policy/regulatory/macro bet the market is not pricing?"_ |
| **Agency costs** | _"How does management alignment / capital allocation differ from what the market assumes?"_ |
| **Behavioral** | _"What is the market over-reacting or under-reacting to that you see as an overcorrection?"_ |

**Closing questions (mandatory):**
- ❓ _"Across all five — what is the market pricing in? Where do you differ? Why are you right and the market wrong?"_ ➡️ if it cannot be answered in one sentence, there is no real variant perception → lower confidence.
- ❓ _"Give a confidence % for this variant view"_ (not high/med/low).

**Find yourself:** consensus estimates + analyst price targets (to identify "what the market thinks") · short interest / positioning · recent estimate revisions.

---

## R4 — Discipline/gate audit

**If it is a SEPA setup:**

Audit the 4 gates — were they truly enforced, or quietly loosened via an "Adapted lens"? Minervini is explicit: _"close enough loses money," "never average down," "Stage 4 = never."_ If the rules are bent, it is no longer SEPA.

- ❓ Q1: _"Each gate (Q33 fundamentals / Trend Template / VCP setup / risk geometry) — truly pass or 'close enough'? Answer ✓/✗, no hedging."_ ➡️ recommended: use the Strict lens; if Adapted, say why.
- ❓ Q2: _"Is R-multiple ≥ 3:1 real? Where is the stop — does it have a logical basis, or was it moved to make the size bigger?"_
- ❓ Q3: _"Pyramid tranches or all-in? Does risk % per trade exceed 1-2%?"_

**If it is a valuation-based entry:**

- ❓ Q1: _"Your margin of safety of X% — from calculation or feeling? Does it match the width of the scenario range + business quality (ROIC−WACC) + leverage?"_ ➡️ recommended: scale it by those three, it is not a fixed number.
- ❓ Q2: _"What is the setup archetype? Does the plan/size match that archetype (a turnaround needs a large margin + a catalyst + a small size — does it?)"_

---

## R5 — Falsification + sell pre-commit

**Falsification (ACH-style):** hunt for the observation that *proves the thesis wrong*, not the one that confirms it. Confirming evidence is manufactured for free.

- ❓ Q1: _"What observation — if it occurred — would make you accept the thesis is wrong? Write it so it is testable (a number / a date)."_ ➡️ recommended: pull from the most sensitive input + the thesis-breakers.
- ❓ Q2: _"Three sell triggers: (a) catalyst-fail (the catalyst does not occur by the deadline) (b) thesis-broken (a core assumption is no longer operative) (c) valuation-stretched (price hits the upper bound) — what is each, concretely?"_ ➡️ pre-commit all three before owning.
- ❓ Q3: _"Review date — when will you come back and check?"_ ➡️ recommended: align with the catalyst deadline or the next earnings.
- ❓ Q4: _"Does your stop (if any) match the kill-criteria? If the stop is wider than the thesis-breaker → flag it."_ ➡️ drawdown ≠ broken thesis — but you must know the difference.

**Close:** write the decision journal entry (template in `decision-journal-template.md`) into that stock's analysis output — not into this repo.

---

## When the frontier is empty = done

Done when all 5 rounds are complete and every high-confidence / weak-evidence claim has been probed. Do not rush — but do not re-ask questions the user has already answered (that is noise).
