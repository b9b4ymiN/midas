# thp-investment-skills

A self-contained set of agent skills for **investment research and decision-making** — Thai + global equities. Installable via the [`skills`](https://github.com/vercel-labs/skills) CLI.

The repo covers the full path from ticker to decision: a **construction pipeline** builds a thesis (narrative → valuation → earnings → synthesis → report), and an **adversarial layer** stress-tests that thesis before you commit capital.

## Install

```bash
# list available skills
npx skills add b9b4ymiN/midas -l

# install all skills globally (user-level)
npx skills add b9b4ymiN/midas -g --all --copy
```

> `--copy` is recommended on Windows (avoids symlink permission issues). After install, **restart your agent session** — skills appear in the picker as `/<name>`.

## Skills

**Entry points** (the skills you usually invoke directly):

| Skill | What it does |
|---|---|
| `midas` | Router — which investment skill fits your situation |
| `both-stock-analysis` | Full analysis + HTML report — orchestrates the 7-skill construction pipeline |
| `stock-grill` | Adversarial stress-test of a thesis (pre-mortem → sensitivity → variant perception → gate audit → sell pre-commit) |
| `minervini-sepa` | SEPA trade timing — the 4-gate screen with entry/stop/target/size |

**Construction sub-skills** (usually reached via `both-stock-analysis`, usable standalone for a single slice):

| Skill | Slice |
|---|---|
| `business-narrative` | Damodaran story research → story-to-numbers map |
| `company-valuation` | Financial-health snapshot + DCF/relative/SOTP → blended fair value + candidate hooks |
| `earnings-preview` | Pre-earnings: consensus, beat/miss track record, positioning |
| `earnings-recap` | Post-earnings: actual vs estimate, reaction, what changed |
| `bf-tech-analysis` | TradingView chart + top-down technical timing, entry zone, stop, target |
| `investment-synthesis` | Synthesize narrative + valuation + earnings → thesis + scenarios + investment plan |
| `bf-report` | Filing-grade HTML research document (10-K / 56-1 style) |

## Vocabulary

All skills speak the canonical investment vocabulary defined in [`CONTEXT.md`](./CONTEXT.md) (24 terms). Skills reference terms there rather than redefining them — so a term means the same thing across the whole pipeline.

## Docs layout

- `CONTEXT.md` — shared glossary (Layer 1: canonical vocabulary)
- `docs/adr/` — methodology rationale, created lazily (Layer 2: why a method was chosen)
- Per-decision **decision journals** are written into each stock's analysis output, *not* committed here (Layer 3: ex-ante, per-position)

## Disclaimer

Research and educational output only. **Not financial advice.** Nothing in this repo is a recommendation to buy, sell, or hold any security.
