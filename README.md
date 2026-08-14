<p align="center">
  <a href="https://github.com/b9b4ymiN/midas">
    <img alt="A stern panda investment master snapping a gold-gloved hand in a vintage comic poster" src="assets/midas-panda-banner.png" width="560">
  </a>
</p>

# midas

[![skills.sh](https://skills.sh/b/b9b4ymiN/midas)](https://skills.sh/b9b4ymiN/midas)

Investment skills that **build a thesis — then try to break it before you commit capital.** A self-contained pipeline from ticker to decision: a construction layer assembles the case (narrative → valuation → earnings → synthesis → report), and an adversarial layer stress-tests it before you act.

Most investing tools help you *build* a case. Very few help you *demolish* it. midas is intentionally split along that line — every output is a conditional plan, and the decision always stays with you.

> ⚠️ **Not financial advice.** Research and educational output only. Nothing here is a recommendation to buy, sell, or hold any security.

## Installation

```bash
npx skills add b9b4ymiN/midas -g --all --copy
```

`--copy` is recommended on Windows (avoids symlink permission issues). After install, **restart your agent session** — skills appear in the picker as `/<name>` (e.g. `/midas`, `/stock-grill`).

<details>
<summary><strong>Install only specific skills</strong></summary>

```bash
npx skills add b9b4ymiN/midas -g -s stock-grill -s minervini-sepa --copy
```

List what's available first with `npx skills add b9b4ymiN/midas -l`.

</details>

<details>
<summary><strong>Project-level (editable files in your repo) instead of global</strong></summary>

Drop `-g` to write the skills into your current project as plain, editable files:

```bash
npx skills add b9b4ymiN/midas --all
```

Nothing updates behind the scenes — pull the latest with `npx skills update` when you want.

</details>

## Why midas exists

### #1: You fell for your own thesis

> "The investor's chief problem — and even his worst enemy — is likely to be himself."
>
> Benjamin Graham, *The Intelligent Investor*

**The problem.** Once you've built a case for a stock, confirmation bias makes every new data point feel like proof. Confirming evidence is cheap; the mind manufactures it for free.

**The fix** is [`/stock-grill`](./skills/stock-grill/SKILL.md) — an **adversary by role**. It consumes your finished thesis and tries to demolish it across five rounds: pre-mortem, sensitivity attack, variant-perception check, discipline audit, and sell pre-commit. It never tells you to buy or sell; it just refuses to let an assumption survive untested. Structured adversarial questioning is the one debiasing move that reliably survives replication.

### #2: You forgot why you bought

> "Know what you own, and know why you own it."
>
> Peter Lynch, *One Up On Wall Street*

**The problem.** Months in, a position is down and the original reasoning has blurred into a vague feeling. You start judging the decision by the outcome — *resulting* — instead of by the thinking that produced it.

**The fix.** Every stock-grill run ends by writing a **pre-registered decision journal**: the thesis, your confidence as a number, the variant perception, the pre-mortem, and the sell triggers — captured *before* the outcome is known. It locks the belief ex-ante so hindsight can't quietly rewrite it. ([template](./skills/stock-grill/references/decision-journal-template.md))

### #3: Your sell discipline evaporated

> "Close enough loses money."
>
> Mark Minervini

**The problem.** The plan was disciplined at entry. Then the stock falls and "hold and hope" feels easier than re-checking the thesis. The biggest leak in most portfolios is a rationalized hold.

**The fix.** stock-grill's final round forces you to **pre-commit sell triggers** — catalyst-fail, thesis-broken, valuation-stretched — with a review date, *before* you own the position. Drawdown ≠ a broken thesis, but you only know the difference if you wrote it down while you were still objective.

## How it's organized

Three layers, all sharing one canonical vocabulary ([`CONTEXT.md`](./CONTEXT.md) — 24 terms):

- **Router** — `/midas` points you to the right skill when you don't remember which to reach for.
- **Construction pipeline** (`skills/pipeline/`) — `both-stock-analysis` orchestrates eleven sub-skills into a full research report from a single ticker.
- **Data layer** (`skills/har-to-api/`) — **Step 0 of the pipeline.** Pulls every fact once with provenance, dated snapshots and flagged fallbacks, so the whole run reads one set of numbers and `--use-snapshot` replays it exactly.
- **Adversarial + technical** — `/stock-grill` attacks a finished thesis; `minervini-sepa` is the standalone SEPA trading-timing system.

## Reference

Grouped by role. **User-invoked** skills are typed by hand (`/midas`). **Model-invoked** skills are reached by the agent automatically when the task fits. Each line is a summary — open the `SKILL.md` for the full discipline.

### Router

**User-invoked**

- **[midas](./skills/midas/SKILL.md)** — Which investment skill fits your situation. A router over the skills in this repo.

### Construction pipeline

Builds the thesis and report from a ticker. Usually entered via `both-stock-analysis`, which chains the rest automatically.

- **[both-stock-analysis](./skills/pipeline/both-stock-analysis/SKILL.md)** — Full equity research in the spirit of Damodaran; orchestrates the seven sub-skills into a filing-grade HTML report.
- **[business-narrative](./skills/pipeline/business-narrative/SKILL.md)** — The story behind the numbers → story-to-numbers map.
- **[business-drivers](./skills/pipeline/business-drivers/SKILL.md)** — Read the business first, then derive what moves its earnings → named drivers with a sensitivity number and a timing lag.
- **[earnings-quality](./skills/pipeline/earnings-quality/SKILL.md)** — Normalise the earnings base Damodaran's way (average the margin over a cycle, not the earnings) → defensible base + growth-eligibility ruling.
- **[company-valuation](./skills/pipeline/company-valuation/SKILL.md)** — DCF + relative + SOTP → blended fair value, sensitivity grid, candidate investment hooks.
- **[earnings-preview](./skills/pipeline/earnings-preview/SKILL.md)** — Pre-earnings: consensus, beat/miss track record, positioning.
- **[earnings-recap](./skills/pipeline/earnings-recap/SKILL.md)** — Post-earnings: actual vs estimate, reaction, what changed.
- **[peer-impact](./skills/pipeline/peer-impact/SKILL.md)** — Competitors ranked by whether their actions move your earnings, not by how similar they look → worldwide search, three impact channels, and the names you dropped.
- **[growth-outlook](./skills/pipeline/growth-outlook/SKILL.md)** — Growth split by source and graded for repeatability, plus a catalyst table where every row has a date and a way to verify it.
- **[bf-tech-analysis](./skills/pipeline/bf-tech-analysis/SKILL.md)** — TradingView chart + top-down technical timing, entry zone, stop, target.
- **[investment-synthesis](./skills/pipeline/investment-synthesis/SKILL.md)** — Turn narrative + valuation + earnings into a thesis, scenarios, and a conditional plan.
- **[bf-report](./skills/pipeline/bf-report/SKILL.md)** — The filing-grade HTML research-document renderer.

### Adversarial

**Model-invoked**

- **[stock-grill](./skills/stock-grill/SKILL.md)** — Adversarial stress-test of a thesis: pre-mortem → sensitivity attack → variant-perception check → gate audit → sell pre-commit. Outputs a pre-registered decision journal.

### Technical timing

**Model-invoked**

- **[minervini-sepa](./skills/minervini-sepa/SKILL.md)** — Specific Entry Point Analysis (SEPA): the 4-gate screen (Q33 fundamentals → Trend Template → VCP → risk geometry) with entry/stop/target/size.

## Docs layout

- [`CONTEXT.md`](./CONTEXT.md) — shared glossary; the canonical vocabulary and authoring single-source-of-truth (each skill inlines the terms it needs at runtime).
- `docs/adr/` — methodology rationale, created lazily when a choice is hard to reverse.
- Per-decision **decision journals** live in each stock's own analysis output, *not* in this repo.

## Disclaimer

Research and educational output only. **Not financial advice.** Nothing in this repo is a recommendation to buy, sell, or hold any security. Data from third-party sources (e.g. yfinance) is unofficial — cross-check against primary filings before any decision.
