# R0 — internal consistency

The round that runs before anyone argues about the thesis.

## Why it exists

R1-R5 attack the *reasoning*. R0 attacks something cheaper and more embarrassing:
whether the document agrees with itself.

This became possible only when stock-grill's input changed from "the output of
five skills" to "one HTML file with a fixed section structure". A remembered
analysis cannot be cross-checked against itself; a file can.

It runs first because its findings invalidate the rounds above it. If §5 and §3
disagree about the current price, every return figure in §6 is computed off one
of two different numbers, and debating the bull case is premature.

## The checks

`scripts/read_report.py` runs these mechanically. Nine of the ten are pure
arithmetic or structure — no judgement, no false modesty needed about them.

| Code | Severity | What it catches |
|---|---|---|
| `UNFILLED` | high | `<!-- FILL -->` markers left in the document |
| `PLACEHOLDER` | high | `[฿0,000]`-style template placeholders never replaced |
| `PRICE_DISAGREE` | high | "current price" differs between sections beyond tolerance — the sections were built from different data pulls |
| `PROB_SUM` | high | scenario probabilities do not sum to 100% |
| `NO_DISCLAIMER` | high | the not-financial-advice line is missing |
| `SECTION_MISSING` | medium | an expected numbered section is absent |
| `LINK_BROKEN` | medium | a cross-reference points at an anchor that does not exist |
| `TARGET_UNANCHORED` | medium | §6 carries a target >60% above the §3 fair value |
| `PROB_NO_VIEW` | medium | no scenario reaches 50% — `investment-synthesis`'s own rule calls that no view |
| `FV_NOT_FOUND` | medium | no fair-value stat card, so targets cannot be checked at all |
| `NO_SOURCES` | medium | no sources block near the end |
| `NO_ASOF` | medium | no as-of date, so staleness cannot be judged |
| `FALLBACK_PRESENT` | low | FALLBACK-tagged figures present — confirm the flag is explained, not just printed |
| `SECTION_THIN` | low | a section under 200 characters of prose — a stub |

## Two things the checks get right that are easy to get wrong

**Numbers live in tables, not only in prose.** A scenario target is always in a
table cell. An early version of the parser read only the narrative text, so
`TARGET_UNANCHORED` silently never fired on any real report — the check existed,
passed, and was worthless. Section numbers are now gathered from prose *and*
table cells.

**A return and a price can be the same number.** `+55%` and `฿55.00` both reduce
to `55` once symbols are stripped, and treating a bull-case return as a price
target produced a confident finding on a perfectly correct report. Target
detection now prefers **currency-marked** figures, falls back to
percent-excluded numbers only when a report carries no currency marks at all,
and downgrades its own severity when it has to.

That second one is the general lesson for this round: a check that fires wrongly
is worse than no check, because it trains the reader to skim past R0.

## Judgement checks R0 hands to the reader

Mechanically detectable is not the same as mechanically decidable. These are
surfaced with evidence, then handed over:

- **Does §7's ranked risk match the most sensitive input in §3's grid?** If the
  grid says terminal growth moves fair value most but §7 leads on competition,
  the report is watching the wrong thing.
- **Does §5's stop contradict §6's thesis-breaker?** A technical stop 8% below
  entry and a thesis-breaker 20% below leaves no rule for what to do in between.
- **Does every figure in the prose appear in the sources table?** A number with
  no provenance is a number someone typed.

## Running it

```bash
python scripts/read_report.py TU_BF-Report.html            # readable
python scripts/read_report.py report.html --json           # findings as JSON
python scripts/read_report.py report.html --extract        # structured extract for R1-R5
python scripts/read_report.py report.html --tolerance 2    # looser price agreement
```

Exit 0 clean, 1 findings, 2 unreadable.

## Feeding R1-R5

`--extract` emits sections, stat cards, tables, anchors and per-section numbers.
Use it so every later question can cite a section: not "what if margins fall"
but "§3 assumes 5.1% operating margin and §2 shows the last reported year at
4.6% — which one is the thesis relying on".
