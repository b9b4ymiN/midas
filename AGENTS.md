# AGENTS.md — thp-investment-skills

> For agents that **edit this repo** (create/modify skills) — not the skills themselves.
> Same rules as THP's global operating manual, except where this file overrides.

## Repo conventions

- **One skill = one folder** under `skills/` containing `SKILL.md` (required) + optional `references/`, `scripts/`, `assets/`, `agents/`
- **Minimum frontmatter:** `name` (lowercase-hyphen, unique in the repo) + `description`
- **`description` = the trigger** — write it "pushy", state explicitly when to use it; use a YAML folded block scalar `>` when it spans multiple sentences (see `both-stock-analysis` in `~/.agents/skills/` as an example)
- **Default = model-invoked.** If a skill is user-invoked only (slash command, should not auto-load into the ambient prompt) → add `disable-model-invocation: true`
- **Path is cosmetic** — the `name` in frontmatter is the key the CLI uses; nesting is allowed up to 3 levels deep
- **SKILL.md ≤ ~500 lines** — beyond that, split into `references/*.md` with "when-to-read" pointers; use the thin-SKILL / fat-reference split (see `investment-research-workflow`)
- **Reference files:** topic-named lowercase-hyphen `.md` in `references/`, each with a single purpose; reference them from SKILL.md via relative path + a condition for when to read

## Language

- **This repo is English-standard.** All skill source (SKILL.md, references) is written in English.
- Runtime output may still be produced in Thai for Thai-market stocks (a behavior of the producing skill, not a source-language rule).

## Vocabulary

- Canonical vocabulary lives in [`CONTEXT.md`](./CONTEXT.md) (root) — the **authoring single-source-of-truth** for the maintainer
- When writing a new skill → **use terms from CONTEXT.md, do not copy definitions**; if you need a new term → add it to CONTEXT.md first
- **Filter:** general finance terms (P/E, EPS, profit) do NOT go in CONTEXT.md — only methodology-specific terms where "different people mean different things" is a real risk
- **CONTEXT.md is authoring-only — never a runtime dependency.** The skills CLI installs only skill folders, never root files, so a `../../CONTEXT.md` link from an installed skill resolves to a non-existent file. Each skill MUST be self-contained at runtime: define the terms it needs **inline** in its SKILL.md or in a sibling `references/*.md` (which ships inside the skill folder and IS installed). This is the mattpocock convention (`codebase-design` inlines a `## Glossary`; `domain-modeling` ships `./CONTEXT-FORMAT.md` as a sibling).

## Docs layout

- **Methodology rationale** (why a method was chosen, why a default was set) → `docs/adr/NNNN-slug.md` — created lazily, only when all three hold: hard-to-reverse + surprising-without-context + real trade-off
- **Per-decision journal** (which stock, which day, what you believed) → **must NOT be committed to this repo**; it lives in each stock's analysis output (Layer 3)

## Disclaimer (mandatory)

Every skill touching investing → attach **"Research and educational output only. Not financial advice."** in both the SKILL.md and the output artifact (appendix + footer). Plans produced must be "conditional plans," never buy/sell commands.

## Commit

- Do not commit without explicit permission (per global rule)
- Conventional commits: `feat(skill): ...`, `docs: ...`, `chore: ...`
