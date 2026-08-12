---
name: bf-report
description: >
  Produce a single self-contained, professional HTML equity-research document — filing-grade
  like a 10-K or 56-1, with a sticky linked table of contents, numbered anchored sections,
  dense tables, judgement-coloured metrics, inline SVG charts, and print-ready CSS. Use this
  as the final step of both-stock-analysis instead of slides, or whenever the user asks for:
  "BF-Report", "a research report / write-up / memo (not slides)", "professional HTML report",
  "10-K or 56-1 style document", "turn this analysis into a document", or "equity research
  document". It is a continuous reading document, not a slide deck: no build step, no
  dependencies. Input contract: it renders completed work, so it needs the upstream business
  narrative, valuation, earnings, technical timing, and synthesis — if run standalone without them, ask for or
  produce them first. Output is a single .html file written via bash heredoc and presented for
  download. Research and educational output only — not financial advice.
---

# BF-Report

Turns a finished equity analysis into a **document you can read front-to-back or jump into by section** — structured like a 10-K / 56-1 so the reader always knows where each topic lives. This replaces slideware: the goal is detail and navigability, not a sparse keynote. The output is one self-contained `.html` file — no build, no dependencies, no web fonts — in a sober, editorial house style.

**Disclaimer:** Research and educational output only. Not financial advice. Carry this into the appendix and footer.

---

## Inputs required (input contract)

BF-Report **renders** completed analysis; it does not generate the underlying numbers. Confirm you have these before building — if a piece is missing and you are running standalone, ask the user or run the relevant skill first:

- **Business narrative** (`business-narrative`) — four pillars, moat read + durability, life-cycle stage, the 3-P verdict, confidence.
- **Valuation** (`company-valuation`) — the ~20-metric financial-health snapshot with 5-yr trends, blended fair value, per-method prices, WACC components, the 5×5 sensitivity grid, and Bull/Base/Bear.
- **Earnings** (`earnings-recap` + `earnings-preview`) — recent-quarter result + reaction, upcoming setup, track record, the priced-for-perfection-vs-pessimism read.
- **Technical timing** (`bf-tech-analysis`) — the TradingView chart image from `tradingview_chart_image`, weekly→daily condition, entry zone, stop/invalidation, target(s), R-multiple, and timing verdict.
- **Synthesis** (`investment-synthesis`) — the thesis paragraph, the scenario timeline + expected value, the conditional plan, and the ranked key risks.
- **Key Investment Insight** (`investment-synthesis`) — the one primary hook in plain language, or an explicit "No clear investment hook identified."

In the full `both-stock-analysis` pipeline these are already produced upstream — just collect them.

---

## Step 1: Load the design system and section spec

Read both before writing any HTML:
- **`references/design_system.md`** — the tokens, typography, layout, sticky-TOC, and every component (KPI band, dense tables, judgement chips, sparkline, sensitivity heatmap, the moat meter, print CSS). This is the house style; reuse it verbatim so all reports match.
- **`references/section_spec.md`** — the section-by-section content map and which upstream step feeds each part.

The design language is distilled from the `anthropics/html-effectiveness` report family. For a live pattern beyond the encoded spec, `web_fetch` the examples (`https://github.com/anthropics/html-effectiveness` → `11-status-report`, `12-incident-report`, `16-implementation-plan`, `14`/`15`) — but the references are sufficient to build the whole document.

---

## Step 2: Build from the template

Use **`references/report_template.html`** as the scaffold — it already implements the full design system, the sticky TOC, every numbered section, the moat meter, sparkline and heatmap patterns, the scrollspy, the collapsible mobile TOC, and print CSS, with `[placeholders]` and `<!-- FILL -->` markers.

1. Copy the template to your working file:
   `cp /mnt/skills/user/bf-report/references/report_template.html /home/claude/[TICKER]_BF-Report.html`
2. **Fetch the company logo and embed it base64 in the header** (left of the title in `.head-title`). Read **`references/logos.md`** first — it has the tested 3-step resolution chain, a ticker→domain lookup table, and the helper one-liners. Summary:

   - **Thai SET** → `https://media.set.or.th/common/logo/company/{SYMBOL}.png` (drop `.BK`; e.g. `PTT`, `CPALL`). Verified working, 140×140.
   - **US (common stock)** → `https://storage.googleapis.com/iex/api/logos/{TICKER}.png` (raw ticker, no suffix; e.g. `AAPL`, `MSTR`, `NVDA`). 128×128 for most names.
   - **US preferred / subsidiary ticker without its own logo** (e.g. `STRC`, `STRK`) → retry Step 2 with the **parent issuer's common ticker** (`MSTR` for STRC).
   - **Fallback** → Google S2 favicon `https://www.google.com/s2/favicons?domain={DOMAIN}&sz=128` using the domain from the lookup table in `references/logos.md` (or looked up at analysis time). Use `curl -sL` (it 301-redirects).
   - **Last resort** → render a 2-letter monogram as inline SVG (never leave the logo slot empty).

   Always **validate** the result (a real logo PNG is >500 bytes and starts with magic bytes `89 50 4E 47`); anything smaller or HTML is an error page → move to the next step. Then base64-encode and drop into `src="data:image/png;base64,..."` in the `<img class="logo">`. **Never link the remote URL** — the report must be a single self-contained file that works offline.
3. **Keep the entire `<style>` block, the TOC (including the `.toc-toggle` hamburger button and `.collapsed` class), the scrollspy, and the TOC-toggle `<script>` verbatim.** Do not swap the palette to the company's brand colours — the editorial house style is deliberate (a filing is sober). A single accent override is acceptable only if the user explicitly asks.
4. Replace every `[placeholder]` and `<!-- FILL -->` with real content from the inputs, section by section per `section_spec.md`. Add rows / family tables / SVG charts as the data warrants (e.g., the full six metric families in §2; a SOTP block in §3 only if 2+ distinct segments). The Executive Summary must lead with the **Key Investment Insight** before the KPI band.
5. Build sparklines by mapping 5 yearly values to the SVG `points` (x = 0,30,60,90,120; y = 30·(1 − (v−min)/(max−min))). Colour every chip and stroke by **judgement** (good / watch / bad), never by sign.
6. For the moat meter (§1.2): set the strength segments, the durability arrow, and the ROIC−WACC spread + its 5-yr sparkline as the quantitative proof.

**Write the finished file with a single quoted bash heredoc**, not `create_file` — a full report is long and `create_file` truncates:

```bash
cat > /home/claude/[TICKER]_BF-Report.html <<'HTML'
...the complete document...
HTML
```

(The quoted `'HTML'` delimiter disables shell expansion so `$`, backticks, etc. in the content are safe.)

Match the report's **language to the user's**. For reports intended for Thai investors, write in **Thai** unless the user explicitly asks for English. Keep currency consistent and labelled throughout.

---

## Step 3: Quality checklist (before presenting)

- The **company logo** is embedded as base64 in the header (left of the title), not linked to a remote URL.
- Every figure carries units / currency; numerics right-aligned with tabular figures.
- Colour encodes judgement, not decoration; nothing is coloured purely for flourish.
- Executive Summary starts with the Key Investment Insight in plain language, not with generic KPI cards.
- §2 leads with ROIC−WACC spread, CapEx-vs-FCF, and the leverage trend; each metric has a 5-yr trend + a read.
- If the Key Investment Insight is supported by a different diagnostic, §2 leads with that diagnostic first; ROIC−WACC / CapEx-vs-FCF / leverage are the default fallback, not a fixed order.
- §1.2 has the moat meter and the ROIC−WACC proof; §1.4 ties growth to whether it earns above WACC.
- §5 includes the TradingView chart image and the technical timing read when `bf-tech-analysis` was run.
- Every TOC link and every inline §-reference resolves to a section.
- The **collapsible mobile TOC works and stays reachable**: the hamburger toggle bar is `position:fixed` at the top of the viewport on screens ≤900px (so the reader never has to scroll back up to open it), the TOC starts collapsed, expands on tap as an overlay capped at ~70vh with its own internal scroll, and auto-collapses after a link is followed. `padding-top:64px` on the shell and `scroll-margin-top:64px` on sections keep content and jump-targets clear of the bar. On desktop (≥900px) the toggle is hidden and the sticky rail is always open.
- **The TOC toggle actually works on mobile (regression-tested):** after filling the template, render the file in a viewport ≤900px and confirm — (a) it starts collapsed, (b) the first tap opens it, (c) a second tap closes it again, (d) it can be re-opened indefinitely. If any of these fails, you have almost certainly refactored the `<script>` block: re-check that it still (1) gates on `DOMContentLoaded`, (2) wraps scrollspy and TOC-toggle in **separate** `try/catch` blocks, (3) uses event delegation (one listener on `.toc`) for auto-collapse, and (4) has not been split back into paired IIFEs that share a script tag. The original paired-IIFE form had a real bug where an error in the scrollspy block silently prevented the toggle handlers from binding, leaving the mobile TOC permanently open and un-closable — do not reintroduce it.
- Mobile check passes: no horizontal overflow in the first viewport; KPI cards wrap; wide tables are scroll-contained or responsive; Thai text does not clip in cards/buttons.
- It prints cleanly (test the print CSS mentally: TOC hidden, full width, sections don't split badly).
- The not-financial-advice disclaimer is in both the appendix and the footer.
- Scenario targets are anchored to the §3 fair value — no invented prices.

---

## Step 4: Present

Copy the final file to the outputs directory and present it:

```bash
cp /home/claude/[TICKER]_BF-Report.html /mnt/user-data/outputs/
```

Then call `present_files` on `/mnt/user-data/outputs/[TICKER]_BF-Report.html` with a one-line summary (headline verdict). Keep the post-amble short — the document speaks for itself.

---

## Caveats
- BF-Report is a renderer; its quality is bounded by the upstream analysis. Low upstream confidence → say so in the document and widen the scenario ranges.
- One continuous document, never slides — no fixed-aspect stages or per-screen pagination.
- Self-contained only — no chart libraries, frameworks, web fonts, or external assets; inline SVG, embedded base64 images (including the company logo), and the small scrollspy + TOC-toggle script are the only "code." Embed TradingView chart PNGs and the company logo as `data:image/png;base64,...`.
- Not financial advice.

---

## Reference Files
- `references/design_system.md` — Tokens, typography, layout + sticky TOC, components (KPI band, tables, chips, sparkline, heatmap, moat meter), print CSS, do/don't.
- `references/section_spec.md` — Section-by-section content and the upstream-step → section mapping.
- `references/report_template.html` — The fillable, self-contained scaffold (copy, then fill).
