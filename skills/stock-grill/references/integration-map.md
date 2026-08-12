# Integration Map — which round consumes which skill's output

stock-grill is an adversarial adapter — it **does not recompute**. It consumes the output of the construction skills (all in this repo) and attacks it. Read this when building the input contract before starting a grill.

## Round × input table

| Round | Consumes output from | Used for |
|---|---|---|
| **R1 Pre-mortem** | thesis-breakers (synthesis) · the most sensitive input (sensitivity grid) | seed failure causes + add what the user missed |
| **R2 Sensitivity attack** | sensitivity grid · blended fair value · metric history (find yourself) | challenge the assumption that moves the price most |
| **R3 Variant perception** | consensus/estimates · analyst targets (find yourself) · earnings positioning read | identify "what the market thinks" to find the divergence |
| **R4 Gate audit** | SEPA 4-gate verdict · VCP/setup · entry/stop/target (if a trade) — or fair value + setup archetype (if a valuation entry) | audit whether rules were truly enforced or bent |
| **R5 Sell pre-commit** | thesis-breakers · catalysts · upper bound of the range · stop (if any) | pre-commit kill-criteria + compare to the stop |

## Source skill → fields pulled

**investment-synthesis** (`skills/pipeline/investment-synthesis/`)
- thesis paragraph → R1 context
- bull/base/bear table + probabilities + E[return] → R2 (does base sit ≥ 50%?)
- thesis-breakers → R1 + R5
- conviction-builders → R5 (the opposite — what would raise confidence)
- setup archetype → R4

**company-valuation** (`skills/pipeline/company-valuation/`)
- blended fair value → R2 anchor
- sensitivity grid (the inputs that move fair value the most) → R2 core
- ROIC−WACC spread → R4 (margin of safety scales with quality)
- leverage read → R4 (margin of safety scales with balance-sheet risk)

**minervini-sepa** (`skills/minervini-sepa/`) — *if it is a trade setup*
- 4-gate verdict → R4 audit
- VCP/setup quality (contractions, tightness) → R4
- entry/stop/target + R-multiple → R4 + R5 (compare stop to kill-criteria)

**earnings-preview / earnings-recap** (`skills/pipeline/earnings-*/`)
- "priced for perfection or pessimism" → R3 (what the market prices in) + R4 (does the entry allow for that positioning?)

## If an input is missing

| Missing | Impact | Fallback |
|---|---|---|
| synthesis (not analyzed yet) | no thesis to grill | tell the user to run `both-stock-analysis` / `investment-synthesis` first |
| sensitivity grid | R2 cannot run | ask the user for the key assumption + history, then grill manually |
| SEPA verdict (not a trade) | skip the SEPA part of R4 | use only the valuation audit |
| consensus data | R3 weakens | state the variant perception qualitatively + flag that confidence is low |

stock-grill never fills gaps by inventing numbers — if something is missing, tell the user directly.
