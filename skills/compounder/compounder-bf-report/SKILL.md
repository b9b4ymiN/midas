---
name: compounder-bf-report
description: Use when compounder research is complete and must become a reader-facing document a decision can rest on — "write up the compounder analysis", "turn this into a research report", "document the compounding thesis", or "produce the Future Compounder write-up". It renders the evidence with every claim carrying its label - FACT, DERIVED, MANAGEMENT_CLAIM, ESTIMATE, or UNVERIFIED - traceable back to an original source, keeps data gaps and unresolved questions visible instead of smoothing them over, and never upgrades a management claim into a fact while writing.
---

# Compounder BF Report

## Overview

Render the completed analysis—including `business_identity_pack`, `market_growth_pack`, economic-engine, runway, and thesis packs—into an evidence-backed report. Optimize for causal understanding, traceability, and decision usefulness—not decorative completeness or ratio dumping.

Read `references/report-template.md` and `references/citation-standard.md`; methodology provenance lives in `references/research-foundations.md`. The visual house style is `references/design_system.md`, implemented as the fillable scaffold `references/report_template.html`, with the masthead logo resolved by `references/logos.md`.

## Who the document is for

One reader: an intelligent adult who runs their own money, is not an analyst, and has not read the filings. Write to that person, not to a committee. The document is an article a friend writes for a friend — not an analyst note.

Two consequences that override any habit of professional register:

- **Plain words first.** A technical term is explained in ordinary language at its first use, in the sentence itself. A term the reader cannot define is a term the report has not delivered.
- **Meaning before the number.** Every claim opens with what it means and lands the figure after. Precision is never reduced; the order is what changes.

## How the document is built

Do not typeset it from scratch. The house style exists so every compounder report looks like the same publication and so the fragile parts — theme handling, the mobile table of contents, the print rules — are not re-derived and re-broken each time.

**Step 1 — read the style, then copy the scaffold.** `references/design_system.md` for the tokens and every component; `references/report_template.html` is that design already implemented, with the movements, the appendices and the placeholders in place.

```bash
cp references/report_template.html [TICKER]-compounder.html
```

Keep the entire `<style>` block, the table of contents including its toggle button, and the `<script>` block **verbatim**. The script is one function gated on `DOMContentLoaded` with two independent `try/catch` blocks; splitting it back into paired IIFEs leaves the mobile menu permanently open, which is a bug this line has already paid for once.

**Step 2 — resolve and embed the logo.** Follow the chain in `references/logos.md`: exchange media library, then the public logo CDN, then a favicon by domain, then a monogram drawn inline. Validate the bytes, base64-encode, and embed. Never link a remote URL — the file must work offline.

**Step 3 — write the article summary first.** It is the part most readers will read instead of the report, and writing it first tells you whether the finding is actually sharp. 3,000–6,000 characters of continuous prose, no bullets, no question heading. The spec is in `references/report-template.md`.

**Step 4 — fill the movements, then §8 and §9.** §8 renders `stage_pack` for every company, whatever the verdict. §9 is **gated**: write the plan only when `accumulation_pack.gate` is `PASSED`; where it is `BLOCKED`, replace the whole movement with the stop — what failed, what would reopen it, and the review date — and no price, band, staging, or size anywhere.

**Step 5 — check it on a phone.** At 360px wide: no sideways scrolling in the first viewport, the table of contents starts collapsed, opens on the first tap, closes on the second, and reopens indefinitely. Then check it prints: the rail hidden, blocks not split across pages.

Write the finished file with a single quoted bash heredoc rather than an editor call — a full report is long, and a truncated one fails silently.

## Required evidence language

Preserve claim labels including **FACT**, **DERIVED**, **MANAGEMENT_CLAIM**, MARKET_EXPECTATION, ESTIMATE, ASSUMPTION, INFERENCE, and UNVERIFIED. Never upgrade claim certainty during writing.

Carry them as superscript class markers linked to the evidence appendix, not as bracketed tags inside sentences. The class stays visible at a glance; the sentence stays readable. Where the certainty class is itself the point, say so in words instead of marking it.

## Report requirements

- Structure the argument as the seven questions in `references/report-template.md`, in that order, with the proving work in the appendix and §8–§9 after the verdict. Every heading is a question the reader would ask, never a framework name.
- **Open with an article, not a summary block.** 3,000–6,000 characters of continuous prose carrying what the company sells, how the money machine works, the strongest evidence and the contradiction against it, the likeliest breakage, the verdict with its binding leg, the key unknown, and the review date. No bullets and no question heading in this block. Potential, Evidence Maturity and Confidence stay three separate readings here as everywhere else, and the verdict panel sits after the article as the thing a reader returns to, never as the thing they read.
- Before internal economics, explain the Layer 0 market frame and Layer 1 **category/demand** regime, **Profit Pool**, competitive **share** mechanism, **Growth Decomposition**, material **channel** incrementality, and **international** replication evidence.
- Explain Economic Unit, **Growth Architecture**, repeatability/product-cycle dependency where material, and Micro → Corporate → **per-share** economics before broad quality conclusions.
- Make Return × Reinvestment × Duration visible, including **Capital Allocation** and financial resilience where material.
- Show the outside-view **base rate** and company-specific update.
- Explain the **Evidence Ladder** supporting Evidence Maturity.
- Close the document with the standing disclaimer as both an appendix section and a footer.
- Include counter-thesis, Kill Conditions, upgrade conditions, Data Gaps, and the **Reverse Reality** business-plausibility check.
- **Carry the review schedule from the thesis pack**: as-of date, next review with the event that settles it, what would force an earlier look, and the date the verdict expires. A verdict printed without them claims to be true forever.
- Place references close to major claims and preserve original source locators.
- **Render `stage_pack` as §8 for every company**, including one the gate blocked: both charts with their captions, the chart stage crossed with the business life-cycle stage, and the pending change on the newest closed bar. No entry, stop, target, or instruction.
- **Render `accumulation_pack` as §9 only when its gate passed.** Where it blocked, the movement carries the stop — the condition that failed, what would reopen it, the review date — and nothing else.
- Keep valuation, target price, technical signals, and holding-dashboard work outside this report unless another skill explicitly supplies them. Where `stage_pack` and `accumulation_pack` do supply them, the standing limits still hold: no fair value, no target price, no upside percentage, no entry geometry, and no instruction to buy or sell.

## DoD

A reader must be able to move from a major conclusion → market/growth evidence → economic translation → interpretation → supporting/contradicting evidence → original source. Every material number is sourced, derived, estimated, or explicitly unverified. The report must reveal what is known, inferred, and unresolved without turning the framework into a mechanical score.

It must also pass the template's self-check: headings that are questions, no technical term used before it is explained, no bracketed evidence tag left in the body, and a stated date for the next review.

The artifact itself must pass four checks that have nothing to do with the argument and everything to do with whether it can be read: the file is **self-contained** (every asset a `data:` URI, no remote `src`), it renders in **both light and dark**, it works on a **mobile** screen at 360px with a table of contents that opens and closes, and it prints without splitting a table or a callout across pages.

**STOP:** Do not invent missing evidence, rerun broad research without a critical contradiction, add valuation conclusions outside the supplied packs, or write §9 for a company whose gate blocked.

---

Research and educational output only. Not financial advice.
