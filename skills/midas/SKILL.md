---
name: midas
description: Ask which investment skill in this repo fits your situation. A router over the skills — read this when you don't remember which skill to reach for, or when the user asks "which skill should I use".
disable-model-invocation: true
---

# Midas

_From ticker to decision — build the thesis, then try to break it._

The router over the **midas** investment skills — a self-contained pipeline from construction to stress-test. You don't remember every skill, so ask here first.

The repo has three layers:
- **Construction pipeline** (`skills/pipeline/`) — `both-stock-analysis` orchestrates 8 sub-skills (`business-narrative` → `earnings-quality` → `company-valuation` → `earnings-preview`/`earnings-recap` → `bf-tech-analysis` → `investment-synthesis` → `bf-report`) to build a full thesis + report from a ticker.
- **Adversarial** (`skills/stock-grill`) — attacks a finished thesis before you commit capital.
- **Standalone technical** (`skills/minervini-sepa`) — the SEPA trading system, usable standalone or referenced by the technical-timing step.

## Skills (entry points)

### `both-stock-analysis` — full analysis + report (the orchestrator)
**Use when:** the user gives a ticker/company and wants the full picture — narrative + valuation + earnings + investment plan + a written HTML report. It chains the 7 sub-skills automatically.
**Not for:** attacking a thesis you already have (use `stock-grill`), or a single slice like pure valuation (use `company-valuation` directly).

### `stock-grill` — adversarial thesis stress-test
**Use when:** you have a **BF-Report** (or a thesis / Investment Synthesis / SEPA verdict) and want to **attack it before committing capital**. Point it at the report file — R0 checks the document against itself, then R1-R5 attack the reasoning — pre-mortem, sensitivity attack, variant-perception check, gate audit, sell pre-commit.
**Not for:** building a valuation or trade plan — build first (`both-stock-analysis`), then grill.

### `minervini-sepa` — SEPA trade timing
**Use when:** you want a Specific Entry Point Analysis on a stock — the 4-gate screen (Q33 fundamentals → Trend Template → VCP → risk geometry) with entry/stop/target/size.
**Not for:** fundamental valuation (use `company-valuation`) or a full report (use `both-stock-analysis`).

### Sub-skills (usually reached via `both-stock-analysis`, not directly)
`business-narrative` · `business-drivers` · `earnings-quality` · `company-valuation` · `earnings-preview` · `earnings-recap` · `growth-outlook` · `bf-tech-analysis` · `investment-synthesis` · `bf-report` — reach directly only when the user wants a single slice (e.g. just the valuation, just the narrative).

## How to choose (when to use what)

| Situation | Use |
|---|---|
| New stock, want full analysis + report | `both-stock-analysis` |
| Have a thesis/Synthesis, want to check before committing | `stock-grill` |
| Already in a position, want a pre-mortem ("why would this drop 40%?") | `stock-grill` |
| Want pure SEPA / trade timing on a stock | `minervini-sepa` |
| Want just one slice (valuation, narrative, earnings, report) | the specific sub-skill |
| "Are these earnings real?" / strip out one-off items | `earnings-quality` |
| "What actually moves this stock?" / input-cost or FX exposure | `business-drivers` |
| "Is this growth real?" / "what catalysts are coming?" | `growth-outlook` |
| Need the same numbers twice, or "where did this figure come from" | `har-to-api` (data layer) |

## Vocabulary

Canonical terms (thesis-breaker, variant perception, sensitivity grid, VCP, etc.) are defined inline where used across the pipeline. The repo's root `CONTEXT.md` is the authoring single-source-of-truth for the maintainer (not a runtime dependency).

## Principles inherited by every skill

- **Decision quality ≠ outcome quality** — these skills judge the *reasoning process*, not predict whether the stock goes up or down.
- **The adversarial skill is an adversary by role** — challenging is the job, not nuisance. It is what makes dissent legitimate rather than overstepping.
- **Output is a conditional plan**, never a buy/sell command — decision authority stays with the human.
- **Not financial advice** — research and educational output only.
