<p align="center">
  <a href="https://github.com/b9b4ymiN/midas">
    <img alt="A stern panda investment master snapping a gold-gloved hand in a vintage comic poster" src="assets/midas-panda-banner.png" width="560">
  </a>
</p>

<p align="center">
  <strong>English</strong> · <a href="README.th.md">ไทย</a>
</p>

# midas

[![skills.sh](https://skills.sh/b/b9b4ymiN/midas)](https://skills.sh/b9b4ymiN/midas)

Midas is a collection of investment-research skills for AI agents. It helps you move from a ticker to a sourced thesis, a valuation, a conditional plan, and a self-contained HTML report. It can then challenge that work before you commit capital.

Midas contains **two research lines that answer two different questions**, and you choose one by what you are actually asking:

- **“What is this worth today?”** → the **valuation line** (`both-stock-analysis`), which bridges the business story to a fair value, a scenario range, and an entry plan.
- **“Can this keep compounding for years?”** → the **compounding line** (`future-compounder`), which asks whether the next dollar the company reinvests still earns a good return, and for how long. It produces no fair value, target price, or entry timing by design.

Both lines share the same data layer, so their facts agree. Their conclusions stay separate on purpose: a company can be a fine compounder at a bad price, or cheap and unable to compound.

You do not need to remember all the skill names. Start with `/midas`, describe what you want in normal language, and it will point you to the right workflow.

> **Research and educational output only. Not financial advice.** Midas does not make the final investment decision for you and does not promise returns.

## What Midas does

Midas separates investment work into clear jobs:

- **Choose:** find the right method for the question you are asking.
- **Collect:** fetch dated financial facts with their sources and save a replayable snapshot.
- **Build:** connect the business story to earnings, valuation, catalysts, and technical timing.
- **Explain:** turn the work into a readable, self-contained BF-Report in HTML.
- **Challenge:** look for contradictions, fragile assumptions, and reasons the thesis could fail.

Every plan is conditional. It should say what evidence would strengthen the thesis, what would weaken it, and when the situation should be reviewed. The human keeps decision authority.

## Why Midas exists

Investment mistakes often begin after the first good idea. Once we like a thesis, confirming evidence feels stronger than disconfirming evidence. Months later, we may also forget why we entered or quietly move the rules when the price moves against us.

Midas is designed around three protections:

1. **Trace the evidence.** Important figures carry a source and an as-of date.
2. **Write the logic down.** The report connects the story, numbers, scenarios, and review conditions.
3. **Attack the finished thesis.** `stock-grill` checks the report against itself and then stress-tests the reasoning.

The goal is not to guarantee a good outcome. It is to make the decision process more explicit, reproducible, and difficult to rationalize after the fact.

## Installation

You need Node.js with `npm`/`npx`, Python 3.8 or newer, and an AI agent environment that supports installable Agent Skills. Node.js installs the skills; Python runs the data and analytical helpers used by a full workflow. On Windows, check both with `npx --version` and `python --version`. Run the following command in your terminal, not in the agent chat:

Install every skill globally:

```bash
npx skills add b9b4ymiN/midas -g --all --copy
```

`--copy` is recommended on Windows because it avoids common symbolic-link permission problems. After installation, **restart your agent session** so the new skills appear. The `-g` option makes them available globally. If `npx` is not recognized, install a current Node.js release and open a new terminal before trying again.

<details>
<summary><strong>Install only selected skills</strong></summary>

```bash
npx skills add b9b4ymiN/midas -g -s stock-grill -s minervini-sepa --copy
```

Use this when you only want the adversarial review and the standalone SEPA workflow. You can list the available skills first with `npx skills add b9b4ymiN/midas -l`.

</details>

<details>
<summary><strong>Install editable copies inside the current project</strong></summary>

Omit `-g` to install project-local files that you can inspect and edit:

```bash
npx skills add b9b4ymiN/midas --all
```

Installed copies do not change automatically. Run `npx skills update` when you choose to update them.

</details>

## Quick Start

If you are unsure where to begin, type this in your AI agent's chat or prompt after restarting the session:

```text
/midas
I want to analyze CPALL.BK but I do not know which workflow to use.
```

`/midas` explains which skill fits the request. It does not run every method automatically. Once the route is clear, ask the agent to continue with the recommended skill.

For a complete company analysis, you can also ask directly:

```text
Run a full analysis of CPALL.BK and produce the final BF-Report.
```

This reaches `both-stock-analysis`, which confirms the market, gathers one consistent data snapshot, runs the research pipeline, renders the report, and finishes with an adversarial review.

## Common workflows

You can write requests in normal language. Slash commands are useful for user-invoked skills such as `/midas`, but model-invoked skills can be selected automatically when your request is clear.

| What you want | Example prompt | Skill and result |
|---|---|---|
| A complete investment report | `Run a full analysis of CPALL.BK and produce the final BF-Report.` | `both-stock-analysis` → full research pipeline and HTML BF-Report |
| A long-horizon compounding verdict | `Can CPALL.BK keep compounding for the next ten years?` | `future-compounder` → evidence on returns, reinvestment, and duration, with potential and confidence reported separately |
| A focused valuation | `Estimate the fair value of NVDA using DCF, relative valuation, and SOTP where applicable.` | `company-valuation` → blended fair value and sensitivity grid |
| A Minervini-style setup review | `Run the Minervini SEPA process on AAPL.` | `minervini-sepa` → four-gate SEPA assessment and conditional setup |
| A dealer-positioning / gamma read | `What does option flow say about NVDA right now?` | `option-flow` → sticky/slippery regime, call/put walls, and a stop-vs-noise-band check |
| Traceable source data | `Fetch reproducible financial facts for TU.BK and save a dated snapshot.` | `har-to-api` → sourced JSON snapshot that can be replayed |
| A challenge to an existing report | `Stress-test this BF-Report before I make a decision.` | `stock-grill` → consistency check, five adversarial rounds, and decision journal |

## What you get

A full run builds an audit trail rather than one large, unexplained answer:

1. **Sourced data snapshot** — a dated set of facts reused by the whole analysis.
2. **Business narrative** — what the company does, why it may grow, and how the story should appear in the numbers.
3. **Business drivers** — the variables that can move earnings, with sensitivity and timing.
4. **Normalized earnings** — an earnings base adjusted for cycles and one-off effects.
5. **Valuation** — DCF, relative valuation, SOTP where useful, blended fair value, and a sensitivity grid.
6. **Context** — competitors with real earnings impact, earnings setup or recap, repeatable growth, dated catalysts, and technical timing.
7. **Investment synthesis** — the key insight, bull/base/bear scenarios, thesis-builders, thesis-breakers, and a conditional plan.
8. **BF-Report** — a self-contained, mobile-responsive HTML research document.
9. **Adversarial review** — internal consistency checks and a deliberate attack on the thesis.
10. **Decision journal** — beliefs, confidence, failure conditions, and review triggers recorded before the outcome is known.

## How a full analysis works

<p align="center">
  <img alt="The Midas panda selects a Minervini methodology figure from categorized shelves of investor thinking modules" src="assets/midas-investor-module-lab.png" width="760">
</p>

The full workflow selects different “thinking tools” for different jobs. `both-stock-analysis` coordinates them in this order:

```text
Step 0: data snapshot
→ resolve market, exchange suffix, currency, and country risk
→ business narrative
→ business drivers
→ earnings quality
→ company valuation
→ impact peers
→ earnings setup/recap and growth catalysts
→ technical timing
→ investment synthesis
→ BF-Report
→ stock-grill
```

The construction stage contains **eleven sub-skills**. The data layer runs before them, the orchestrator controls the sequence, and `stock-grill` attacks the completed result afterward. If you only need one part—such as valuation or earnings quality—you can run that skill without the full pipeline.

## How a compounding analysis works

The compounding line asks a different question, so it uses a different order. `future-compounder` coordinates it:

```text
Step 0: data snapshot (optional, shared with the valuation line)
→ business identity and market scope   what business is this, really?
→ market and growth intelligence       where does growth come from, and who captures it?
→ business economic engine             how does one unit of this business make money?
→ reinvestment and runway              what does the next dollar earn, and for how long?
→ compounder grill                     what would have to be true, and what would break it?
→ compounder BF-Report
```

Each stage is a gate rather than a chapter. The market frame must hold before market research is trusted; market evidence must hold before internal economics are read; and if later evidence contradicts the original framing, the analysis is sent back rather than quietly redefined.

The result separates three things a single rating would blur together: how large the compounding could be, how far the evidence actually reaches, and how confident the conclusion can be. A young company can legitimately score high on the first and low on the second.

This line deliberately excludes DCF, fair value, target price, entry timing, and position sizing. Use the valuation line for those.

## Choose the right skill

| Your question | Use |
|---|---|
| “I do not know where to start.” | `/midas` |
| “Give me the full picture and a finished report.” | `both-stock-analysis` |
| “Can this company keep compounding for a decade?” | `future-compounder` |
| “What business is this company really in?” | `business-identity-scope` |
| “Is that growth the market, or share, or acquisitions?” | `market-growth-intelligence` |
| “How does one store or one customer actually make money?” | `business-economic-engine` |
| “What does the next dollar they reinvest earn?” | `reinvestment-runway` |
| “Try to break this compounding thesis.” | `compounder-grill` |
| “Write the compounding research up as a document.” | `compounder-bf-report` |
| “Fetch the facts once and show where they came from.” | `har-to-api` |
| “Explain the business story behind the numbers.” | `business-narrative` |
| “What actually moves this company’s earnings?” | `business-drivers` |
| “Are reported earnings a reliable valuation base?” | `earnings-quality` |
| “What is the company worth?” | `company-valuation` |
| “Which competitors can materially affect earnings?” | `peer-impact` |
| “What should I know before the next results?” | `earnings-preview` |
| “What changed in the latest results?” | `earnings-recap` |
| “Is growth repeatable, and what catalysts have dates?” | `growth-outlook` |
| “What does the weekly and daily chart say about timing?” | `bf-tech-analysis` |
| “Turn the research into one thesis and conditional plan.” | `investment-synthesis` |
| “Render the research as a professional HTML document.” | `bf-report` |
| “Try to break this finished thesis.” | `stock-grill` |
| “Run the Minervini SEPA process.” | `minervini-sepa` |
| “Is there a gamma squeeze?” / “where will it pin at expiry?” | `option-flow` |

New to the terminology? **DCF** values expected cash flows; **SOTP** values business parts separately; a **sensitivity grid** shows how valuation changes when assumptions change; a **provenance tier** labels the quality or role of a data source; **Trend Template** and **VCP** are Minervini chart filters; **risk geometry** compares the planned entry, stop, target, and potential loss; and **GEX** (gamma exposure) is the mechanical hedging pressure sitting in a stock's option chain.

## Skill reference

The repository currently contains **24 skills**. Start with the router when you are uncertain; enter one of the two orchestrators for end-to-end work; reach a construction skill directly for one focused question.

### Start here

- **[midas](./skills/midas/SKILL.md)** — user-invoked router that selects the right investment workflow from a plain-language request.

### Data layer

- **[har-to-api](./skills/har-to-api/SKILL.md)** — fetches financial facts with provenance, saves dated snapshots, and can derive a client from captured website traffic when a new source is needed.

### Full workflows

- **[both-stock-analysis](./skills/pipeline/both-stock-analysis/SKILL.md)** — coordinates the complete ticker-to-report workflow, including the eleven construction sub-skills and the final adversarial review.
- **[future-compounder](./skills/compounder/future-compounder/SKILL.md)** — coordinates the compounding investigation across its six sub-skills, and reports how large the compounding could be, how mature the evidence is, and how confident the conclusion can be as three separate verdicts.

### Construction: eleven focused skills

- **[business-narrative](./skills/pipeline/business-narrative/SKILL.md)** — turns company research into a story-to-numbers map.
- **[business-drivers](./skills/pipeline/business-drivers/SKILL.md)** — identifies and quantifies the factors that move earnings.
- **[earnings-quality](./skills/pipeline/earnings-quality/SKILL.md)** — normalizes the earnings base and tests whether reported growth is dependable.
- **[company-valuation](./skills/pipeline/company-valuation/SKILL.md)** — combines DCF, relative valuation, and SOTP where appropriate, then shows sensitivity.
- **[peer-impact](./skills/pipeline/peer-impact/SKILL.md)** — finds competitors whose actions can affect the company’s earnings through shared inputs, customers, or pricing.
- **[earnings-recap](./skills/pipeline/earnings-recap/SKILL.md)** — compares reported results with expectations and explains what changed.
- **[earnings-preview](./skills/pipeline/earnings-preview/SKILL.md)** — prepares for upcoming earnings using consensus, history, and positioning.
- **[growth-outlook](./skills/pipeline/growth-outlook/SKILL.md)** — separates sources of growth, judges repeatability, and records dated catalysts.
- **[bf-tech-analysis](./skills/pipeline/bf-tech-analysis/SKILL.md)** — reads weekly and daily charts for conditional timing, risk, and invalidation levels.
- **[investment-synthesis](./skills/pipeline/investment-synthesis/SKILL.md)** — joins narrative, valuation, earnings, and timing into scenarios and a conditional plan.
- **[bf-report](./skills/pipeline/bf-report/SKILL.md)** — renders the completed research as a filing-style, self-contained HTML document.

### Compounding: six focused skills

- **[business-identity-scope](./skills/compounder/business-identity-scope/SKILL.md)** — settles what business the company actually operates before any market size, competitor, or runway claim is trusted, labelling each arena as proven, emerging, an option, or narrative.
- **[market-growth-intelligence](./skills/compounder/market-growth-intelligence/SKILL.md)** — explains growth from outside the company: category demand, who captures the profit, share gains and their cause, and whether new channels, stores, and countries add demand or move it around.
- **[business-economic-engine](./skills/compounder/business-economic-engine/SKILL.md)** — rebuilds how one repeatable unit of the business makes money, and traces that through to cash flow and owner economics per share.
- **[reinvestment-runway](./skills/compounder/reinvestment-runway/SKILL.md)** — measures what incremental capital earns rather than what past capital averaged, sizes how much more can be deployed, and tests whether the balance sheet can fund it.
- **[compounder-grill](./skills/compounder/compounder-grill/SKILL.md)** — challenges the compounding thesis with the outside-view base rate, falsification tests, and a reverse check that starts from the outcome and backs out what the world would have to look like.
- **[compounder-bf-report](./skills/compounder/compounder-bf-report/SKILL.md)** — writes the research up with every claim labelled by evidence type and traceable to an original source, and with the gaps left visible.

### Adversarial review

- **[stock-grill](./skills/stock-grill/SKILL.md)** — checks a finished report for contradictions, attacks its assumptions across five rounds, and produces a pre-registered decision journal.

### Standalone technical systems

- **[minervini-sepa](./skills/minervini-sepa/SKILL.md)** — applies the four-gate SEPA process: fundamentals, Trend Template, VCP setup, and risk geometry.
- **[option-flow](./skills/option-flow/SKILL.md)** — reads dealer gamma exposure (GEX) from a US-listed option chain to judge whether the market is sticky or slippery, and whether a proposed stop clears the option-implied noise band. Refuses to output on a chain too thin to trust.

## Data you can trace and replay

The `har-to-api` data layer is Step 0 of a full analysis. It pulls data once so later stages do not silently use different prices or reporting periods.

Its main rules are:

- Each fetched fact records its **source, as-of date, URL, and provenance tier**.
- Missing data stays missing. The system should not invent a number to complete a table.
- A reserve source such as yfinance is marked `FALLBACK` with a reason.
- If two providers disagree by more than **2%** on the same fact, the disagreement is reported instead of silently resolved.
- Dated snapshots can be replayed, helping distinguish “the data changed” from “the analysis changed.”
- Segment data should always be checked against the company’s primary filing.

The included `stockanalysis` mapping has local-fixture coverage and six mapped routes for US and Thai listings. However, a real network path can change, and the live HTTP path plus provider profiles other than `stockanalysis` have documented verification limits. This repository-level smoke check is for users who want to validate the provider directly; it is not required just to open the installed skills. Obtain a checkout and run it in Bash (Git Bash or WSL on Windows):

```bash
git clone https://github.com/b9b4ymiN/midas.git
cd midas
bash skills/har-to-api/tests/smoke_live.sh TU bkk
```

Respect provider terms and rate limits, and cross-check decision-critical figures against primary filings. Replaying a saved snapshot reproduces the input data for an earlier analysis; fetching again from a live provider is a new capture and may return changed data.

## Limits and responsible use

- Midas improves research structure; it cannot remove uncertainty or guarantee an outcome.
- Source availability, website formats, market data, and analyst estimates can change.
- Valuation depends on assumptions. Read the sensitivity grid, not only the headline fair value.
- The compounding line judges business durability, not price. A company can pass it and still be a poor investment at today's quote, so a compounding verdict is never an entry signal on its own.
- Technical levels are conditional risk markers, not promises that a price will behave in a certain way.
- Personas and named methodologies are tools for structured thinking, not exact simulations or endorsements by those investors.
- The final report may contain errors or stale third-party data. Verify material facts against filings and official announcements.
- Outputs are conditional plans and research questions, never instructions to buy, sell, or hold.

<details>
<summary><strong>Under the hood</strong></summary>

### Repository layout

```text
skills/
├── midas/                  router
├── har-to-api/             traceable and replayable data layer
├── pipeline/               valuation orchestrator plus 11 construction skills
├── compounder/             compounding orchestrator plus 6 construction skills
├── stock-grill/            adversarial review
├── minervini-sepa/         standalone SEPA system
└── option-flow/            standalone dealer-positioning (GEX) read
```

Each skill is a folder with a required `SKILL.md` and optional `references/`, `scripts/`, `assets/`, `agents/`, or `tests/` directories. Skills are self-contained at runtime.

The helper scripts use the Python 3.8+ standard library, with one exception: `option-flow`'s Black-Scholes math needs `numpy` and `scipy` (`yfinance` too, but only lazily, for its live-fetch path, same pattern as `har-to-api`'s fallback). Every other skill's scripts are stdlib-only. Shell regression tests cover the data layer and several analytical helpers; live provider behavior still needs the documented smoke checks. The compounding line carries no runtime scripts — it is reasoning, not computation — but `python skills/compounder/tests/validate_skills.py` checks that its seven skills still hold their structure, their evidence contracts, and the mandatory disclaimer.

[`CONTEXT.md`](./CONTEXT.md) is the maintainer’s canonical authoring vocabulary. Installed skills do not depend on that root file; each skill carries the definitions it needs. Hard-to-reverse methodology decisions belong in `docs/adr/`. A per-stock decision journal belongs with that stock’s analysis output, not in this repository.

The main deliverable is named `[TICKER]_BF-Report.html`: one self-contained file that the agent presents for download and that opens in a normal web browser. The dated data snapshot and decision journal stay with the stock's analysis output. `stock-grill` reads the rendered report; high-severity consistency errors should be repaired before the five reasoning rounds, while the grill findings and journal remain separate analysis artifacts unless the user asks for a revised report.

</details>

## License

Midas is available under the [MIT License](LICENSE).

## Disclaimer

**Research and educational output only. Not financial advice.** Nothing in this repository or its generated artifacts is a recommendation to buy, sell, or hold any security. Check important figures against primary filings and make decisions based on your own circumstances and risk limits.
