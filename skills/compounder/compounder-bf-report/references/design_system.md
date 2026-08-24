# Compounder Report Design System

The house style for the Future Compounder write-up. It is a **reading document** — an article with an appendix behind it — not a slide deck and not an analyst note. Everything below exists to serve one reader working through an argument on a phone or a laptop, in either theme, and printing it if they want to.

Reuse it verbatim so every compounder report looks like the same publication. The palette is green because this line of work is its own thing; do not swap it for a company's brand colours.

`references/report_template.html` implements all of it. Copy that file and fill it — do not rebuild the CSS from this document.

---

## Design tokens (`:root`)

Green, with a warm paper ground in light and a near-black green-grey in dark. The judgement scale is separate from the accent: the accent is identity, the judgement colours carry a read and are never used for decoration.

```css
:root{
  /* surfaces & ink — light */
  --ground:#FAFAF8; --surface:#F0EFEA; --surface-2:#E5E3DB;
  --line:#D5D2C6; --line-soft:#E4E1D7;
  --ink:#16181A; --ink-2:#454A4D; --ink-3:#767C80;
  /* identity */
  --accent:#1D4F3F; --accent-soft:#DCE9E3;
  /* judgement scale — encodes a read, never decoration */
  --good:#1D4F3F; --good-soft:#DCE9E3;
  --warn:#8C5E10; --warn-soft:#F3E9D3;
  --risk:#8A2E24; --risk-soft:#F3DFDB;
  /* type */
  --display:"Bai Jamjuree","IBM Plex Sans Thai",ui-sans-serif,system-ui,sans-serif;
  --sans:"IBM Plex Sans Thai","IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  /* shape */
  --radius-panel:12px; --radius-row:8px;
  --border:1.5px solid var(--line); --rule:1px solid var(--line);
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --ground:#101211; --surface:#191C1B; --surface-2:#232726;
  --line:#363B39; --line-soft:#272B2A;
  --ink:#EAEDEB; --ink-2:#B2B8B5; --ink-3:#848A87;
  --accent:#6FBFA0; --accent-soft:#15302A;
  --good:#6FBFA0; --good-soft:#15302A;
  --warn:#D0A046; --warn-soft:#2C2415;
  --risk:#D4837A; --risk-soft:#301C19;
}}
:root[data-theme="dark"]{ /* same overrides again, so an explicit toggle wins */ }
```

**Rules that matter more than the values.** Define the complete light palette on bare `:root`; redefine only what changes in the dark blocks; give `body` an explicit `background:var(--ground)`. Never give a colour its only definition inside a media query — a page that does that renders unstyled for half its readers.

The colour that changes meaning between themes is the accent: `#1D4F3F` is dark green on paper, `#6FBFA0` is light green on near-black. Both must pass contrast against their own ground, and both are used for the same thing.

---

## Typography

| Role | Face | Size | Notes |
|---|---|---|---|
| Body | `--sans` | 16.5px / 1.8 | Thai and Latin in one stack; long-form line height |
| Masthead h1 | `--display` 700 | `clamp(29px,4.7vw,47px)` | `text-wrap:balance`, tight tracking |
| Movement heading h2 | `--display` 600 | `clamp(21px,2.6vw,28px)` | Every one is a question |
| Sub-heading h3 | `--sans` 600 | 17.5px | |
| Eyebrow / metadata | `--mono` | 11–12.5px | uppercase, `letter-spacing:.16em` |
| Figures in tables | `--mono` | inherit | `font-variant-numeric:tabular-nums` everywhere digits are compared |

Body copy sits in a ~68ch column. The dek under the masthead is lighter weight and capped at 62ch.

Web fonts are optional: the stack degrades to system Thai/Latin faces. Where fonts are linked, only Google Fonts is permitted, and the fallback stack must be real.

---

## Layout & the sticky TOC

A left rail on wide screens, a fixed hamburger bar on narrow ones. The rail lists the movements — the reader should see the whole argument as a short list and jump into it.

```css
.shell{max-width:1160px;margin:0 auto;padding:48px 28px 120px;
       display:grid;grid-template-columns:228px minmax(0,1fr);gap:54px;align-items:start;}
.toc{position:sticky;top:32px;align-self:start;font-size:13.5px;}
.toc a{display:block;padding:5px 0 5px 12px;color:var(--ink-2);text-decoration:none;
       border-left:2px solid transparent;}
.toc a.active{color:var(--ink);border-left-color:var(--accent);font-weight:600;}
.doc{max-width:820px;min-width:0;}
@media(max-width:900px){
  .shell{grid-template-columns:1fr;gap:0;padding:64px 16px 80px;}
  section,h3[id]{scroll-margin-top:64px;}
  .toc{position:fixed;top:0;left:0;right:0;z-index:100;background:var(--ground);
       border-bottom:var(--rule);box-shadow:0 1px 6px rgba(0,0,0,.08);}
  .toc-toggle{display:flex;}
  .toc ol{max-height:70vh;overflow-y:auto;transition:max-height .3s ease;}
  .toc.collapsed ol{max-height:0;overflow:hidden;}
}
```

**The TOC script is the most fragile part of the template.** It is one `<script>` at the end of `<body>`, a single `initReportInteractivity()` gated on `DOMContentLoaded` with a `readyState` fallback, containing **two independent `try/catch` blocks** — scrollspy and TOC toggle. Keep that shape:

- **Do** keep each block in its own `try/catch`, so an error in one cannot stop the other binding.
- **Do** bind the toggle as one listener on `.toc-toggle` calling `e.preventDefault()` then `classList.toggle('collapsed')`.
- **Do** use event delegation on `.toc` for auto-collapse after a link is followed.
- **Don't** split it back into paired IIFEs sharing a script tag. A throw in the first halts the second, which leaves the mobile menu permanently open and un-closable. That was a real bug in the sibling report skill; it is not being reintroduced here.
- **Do** collapse the menu when the viewport **crosses** into mobile, tracked with a `wasMobile` flag — not on every resize event. The sibling skill only sets the collapsed state once, at load, so a desktop window narrowed to phone width ends up with a fixed overlay covering the top of the page until it is tapped. Collapsing on *every* resize would be worse: phones fire resize when the URL bar hides during a scroll, which would shut the menu while the reader is using it. Watching the crossing fixes the first without causing the second, and it holds no per-click state.

---

## Components

### Masthead

Logo (64×64, base64, white-padded) beside the title, an eyebrow line, the h1 title, a one-line dek, then a mono `.tickline` carrying ticker with exchange suffix, market, currency, as-of date, and the review date. The evidence-marker legend sits here too, so certainty is visible before the first claim.

```css
.masthead{border-bottom:2px solid var(--ink);margin-bottom:38px;}
.head-title{display:flex;gap:16px;align-items:center;}
.logo{width:64px;height:64px;object-fit:contain;background:#fff;border-radius:10px;
      padding:6px;border:var(--rule);flex:none;}
```

### Article summary

The opening block: continuous prose, 3,000–6,000 characters, no bullets and no question heading. It is the thing most readers will read instead of the report, so it is typeset slightly larger than body copy and given room.

```css
.summary{font-size:17.5px;line-height:1.85;border-left:3px solid var(--accent);
         padding:4px 0 4px 22px;margin:0 0 34px;}
.summary p{margin:0 0 16px;}
.summary p:first-child{font-size:19px;}      /* the lede carries the whole finding */
```

On mobile the left rule stays; the padding drops to 14px. Never let this block become a card with a background — it is the article, not a callout.

### Verdict panel

The three axes reported separately, a row per leg, the binding leg marked, and the dates. It is a **table**, not three words in a paragraph, and it sits *after* the article summary — the prose is what the reader reads, the panel is what they come back to.

```css
.verdicts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:26px 0;}
.vcell{border:var(--border);border-radius:var(--radius-panel);padding:14px 16px;
       background:var(--surface);}
.vlabel{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;
        color:var(--ink-3);}
.vval{font-family:var(--display);font-size:23px;font-weight:700;margin-top:4px;}
.vnote{font-size:13px;color:var(--ink-2);margin-top:6px;}
.leg-binding td{background:var(--warn-soft);font-weight:600;}
@media(max-width:640px){.verdicts{grid-template-columns:1fr;}}
```

The binding leg is the most decision-relevant row on the page and is the only one highlighted. A reader who sees only "Strong" cannot tell a business whose returns are excellent but whose runway is closing from one where every leg is strong.

### Evidence markers

Superscript class letters linked to Appendix A — **F** fact · **D** derived · **M** management claim · **E** estimate or assumption · **X** market expectation · **U** unverified. Never the bracketed inline form in the body.

```css
.tag{font-family:var(--mono);font-size:10px;vertical-align:super;padding:1px 4px;
     border-radius:4px;text-decoration:none;margin-left:2px;}
.t-fact{background:var(--good-soft);color:var(--good);}
.t-der{background:var(--accent-soft);color:var(--accent);}
.t-mgmt{background:var(--warn-soft);color:var(--warn);}
.t-est{background:var(--surface-2);color:var(--ink-2);}
.t-mkt{background:var(--surface-2);color:var(--ink-2);}
.t-unver{background:var(--risk-soft);color:var(--risk);}
```

Each class keeps its colour in both themes. The legend in the masthead is not optional — an unexplained marker is worse than no marker.

### Callout

```css
.callout{border:var(--border);border-left-width:3px;border-radius:var(--radius-panel);
         padding:16px 18px;margin:22px 0;background:var(--surface);}
.callout.good{border-left-color:var(--good);}
.callout.amber{border-left-color:var(--warn);}
.callout.risk{border-left-color:var(--risk);}
```

### Dense table

```css
.tablewrap{overflow-x:auto;margin:20px 0;}          /* the page never scrolls sideways */
table{width:100%;border-collapse:collapse;font-size:14.5px;}
th{text-align:left;font-family:var(--mono);font-size:11px;letter-spacing:.1em;
   text-transform:uppercase;color:var(--ink-3);border-bottom:var(--rule);padding:8px 10px;}
td{padding:9px 10px;border-bottom:1px solid var(--line-soft);vertical-align:top;}
td.num,th.num{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums;}
```

Wide tables scroll inside `.tablewrap`. A table that forces the page body to scroll sideways is a defect.

### Sparkline

Five values, inline SVG, no library. `x = 0,30,60,90,120`; `y = 30·(1 − (v−min)/(max−min))`. Stroke coloured by **judgement**, never by sign: a falling number can be good.

### Stage figure

The frame around each chart from `stage_pack`, whether it holds a captured PNG or rendered SVG.

```css
.figure{border:var(--border);border-radius:var(--radius-panel);padding:14px;margin:24px 0;
        background:var(--surface);}
.figure img,.figure svg{width:100%;height:auto;display:block;}
.figcap{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);margin-top:10px;
        display:flex;flex-wrap:wrap;gap:6px 18px;}
```

The caption carries symbol, interval, moving average, bar count, and capture date — and, where the image was drawn rather than captured, says so. Rendered SVG inherits the page's custom properties, so it follows the reader's theme.

### Expectation gap

One row, three positions, the current reading marked. It compares two growth rates; it is not a price scale and must never be drawn as one.

```css
.gapbar{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin:18px 0 8px;}
.gapseg{padding:10px 12px;font-size:13px;text-align:center;background:var(--surface);
        border:1px solid var(--line-soft);}
.gapseg.on{background:var(--accent-soft);border-color:var(--accent);font-weight:600;}
```

### Accumulation bands

A three-row table: band · price range · the condition that defines it. **The condition column is not optional** — a band without its condition has become a target price, which this report does not produce.

Where the gate blocked, none of this appears. Instead:

```css
.blocked{border:var(--border);border-left:3px solid var(--risk);border-radius:var(--radius-panel);
         padding:18px 20px;background:var(--risk-soft);}
```

carrying what was found, why the work stops, what would reopen it, and the review date.

---

## Print

```css
@media print{
  .toc,.toc-toggle{display:none;}
  .shell{display:block;padding:0;max-width:none;}
  body{background:#fff;color:#000;font-size:11pt;}
  .callout,.figure,.vcell,table,.blocked{page-break-inside:avoid;}
  a[href^="#"]{color:inherit;text-decoration:none;}
}
```

`page-break-inside:avoid` goes on **self-contained blocks only** — callouts, tables, figures, the verdict panel. Never on a whole movement: a 2,600-character block that refuses to break leaves most of a page empty.

---

## Do / don't

- **Do** colour by judgement. **Don't** colour for decoration, and never by the sign of a number.
- **Do** keep every figure with its unit and currency. **Don't** print a ratio without the two things being compared.
- **Do** let the article summary carry the finding. **Don't** replace it with a card grid — cards are what the reader skims, prose is what they understand.
- **Do** keep the accent green. **Don't** re-theme to the company's brand: a research document that looks like a company's marketing has told the reader something untrue about its independence.
- **Do** embed every asset. **Don't** reference a remote image, font file, or script — the file must work offline.
- **Do** test at 360px wide before publishing. **Don't** ship a first viewport that scrolls sideways.
