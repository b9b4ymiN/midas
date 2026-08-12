# Business Narrative

Research and structure the qualitative business story of a public company the way Aswath Damodaran does in *Narrative and Numbers*, then translate that story into the valuation inputs a model consumes.

## What it does

- Researches current filings / IR material (never stale memory) into a fact base
- Builds four story pillars: income structure, business model & moat, industry & TAM, growth & reinvestment quality
- Classifies the company's corporate life-cycle stage and the dominant value driver
- Runs Damodaran's possible / plausible / probable test plus a "this time is different" red-flag check
- Outputs a Narrative Brief ending in a **story-to-numbers map** — suggested ranges for growth, margins, reinvestment, risk, and terminal posture, plus method/SOTP signals — that hands off to `company-valuation`

## Triggers

`what's the story on X`, `understand the business`, `business model of X`, `how does this company make money`, `investment narrative`, `bull case / bear case`, `is the growth story credible`, `what's the moat`, `revenue mix and segments`, `TAM for X`, `what has to be true for this to work`. Also runs as Step 2 of `both-stock-analysis`.

## Prerequisites

- Web access for current filings, IR material, and industry/TAM research
- No special libraries; this is a research-and-reasoning skill

## Output

A Narrative Brief: one-line description, four pillars, life-cycle stage, the 3 P's verdict, and the story-to-numbers map (driver → input → default → story-implied range → justifying pillar) with path signal, SOTP signal, and a confidence level.

## Reference Files

- `references/narrative_framework.md` — Life-cycle → driver → story-type mapping, the value-driver bridge in depth, the 3 P's ladder, and the "this time is different" checklist
- `references/research_checklist.md` — What to gather per pillar, the US/Thai primary-source map, the segment-data note, and pre-handoff quality checks

## Disclaimer

For research and educational purposes only. Not financial advice.
