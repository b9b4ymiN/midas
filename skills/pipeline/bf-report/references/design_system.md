# BF-Report Design System

The visual language for BF-Report, distilled from the `anthropics/html-effectiveness` report-family examples (`11-status-report`, `12-incident-report`, `16-implementation-plan`, and the `14`/`15` explainers). The house style is **editorial and filing-grade** — sober, dense, readable front-to-back like a 10-K / 56-1, not a slide deck. Reuse these tokens and component patterns verbatim so every report looks consistent. All CSS is inline; no build step, no external dependencies, no web fonts.

> When you want a live pattern beyond what is encoded here, `web_fetch` the example files from the repo (`https://github.com/anthropics/html-effectiveness`) — but the blocks below are sufficient to build the whole report.

## Contents
- Design tokens (`:root`)
- Typography
- Layout & the sticky TOC
- Components (header, KPI band, section, table, judgement chips, callout, sparkline, heatmap, moat meter)
- Print CSS
- Do / don't

---

## Design tokens (`:root`)

Drop this in once. The palette is the Claude editorial palette; **color carries judgement, not decoration**.

```css
:root{
  /* surfaces & ink */
  --ivory:#FAF9F5; --white:#FFFFFF; --slate:#141413;
  --gray-100:#F0EEE6; --gray-300:#D1CFC5; --gray-500:#87867F; --gray-700:#3D3D3A;
  --oat:#E3DACC;                 /* callout / muted panel */
  /* judgement scale — use ONLY to encode a read, never for flourish */
  --good:#788C5D;                /* olive  → strengthening / value-creating / positive */
  --watch:#D97757;               /* clay   → caution / watch / neutral-attention (brand accent) */
  --bad:#B04A3F;                 /* rust   → deteriorating / risk / negative */
  /* type */
  --serif:ui-serif,Georgia,'Times New Roman',serif;
  --sans:system-ui,-apple-system,'Segoe UI',sans-serif;
  --mono:ui-monospace,'SF Mono',Menlo,Consolas,monospace;
  /* shape */
  --radius-panel:12px; --radius-row:8px;
  --border:1.5px solid var(--gray-300);
  --rule:1px solid var(--gray-300);
}
```

Semantics: `--good`/`--watch`/`--bad` are the green/amber/red of the report. A metric is green when it is *strengthening or value-creating*, amber when it bears watching, red when *deteriorating* — judged on direction and meaning, not on sign. The brand accent (`--watch`/clay) doubles as the single decorative accent (links, section ticks); use it sparingly.

---

## Typography

```css
body{font-family:var(--sans);font-size:15px;line-height:1.6;color:var(--slate);
     background:var(--ivory);-webkit-font-smoothing:antialiased;margin:0;}
h1{font-family:var(--serif);font-weight:500;font-size:38px;letter-spacing:-.01em;margin:0;}
h2{font-family:var(--serif);font-weight:500;font-size:25px;letter-spacing:-.01em;margin:0 0 6px;}
h3{font-family:var(--serif);font-weight:500;font-size:18px;margin:28px 0 8px;}
.eyebrow,.label{font-family:var(--sans);font-size:11px;font-weight:600;text-transform:uppercase;
     letter-spacing:.06em;color:var(--gray-500);}
.num{font-family:var(--serif);font-weight:500;}      /* big figures in serif read as "editorial" */
code,.mono{font-family:var(--mono);font-size:13px;}
```

Rule of thumb: **serif for headings and headline figures, sans for prose, mono for labels / tickers / code / table-header captions.** This three-voice split is what makes the document feel like a published filing rather than a web app.

---

## Layout & the sticky TOC

Filing-grade means the reader always knows where each part lives. Use a **left sticky TOC rail** on wide screens that collapses to a **tappable, hamburger-toggle panel** on narrow screens (≤900px) so the first viewport on mobile stays clean and the long TOC never pushes content down. Content sits in a single ~820px reading column.

```css
.shell{max-width:1140px;margin:0 auto;padding:48px 24px 120px;
       display:grid;grid-template-columns:232px 1fr;gap:56px;}
.toc{position:sticky;top:32px;align-self:start;font-size:13.5px;}
.toc .eyebrow{margin-bottom:12px;}
.toc ol{list-style:none;margin:0;padding:0;counter-reset:s;}
.toc a{display:block;padding:5px 0 5px 12px;color:var(--gray-700);text-decoration:none;
       border-left:2px solid transparent;}
.toc a:hover{color:var(--slate);}
.toc a.active{color:var(--slate);border-left-color:var(--watch);font-weight:600;}
.toc .sub{padding-left:26px;font-size:12.5px;color:var(--gray-500);}
.doc{max-width:820px;min-width:0;}
/* Toggle button — hidden on desktop, shown ≤900px */
.toc-toggle{display:none;align-items:center;gap:10px;width:100%;justify-content:space-between;
            background:var(--white);border:var(--border);border-radius:var(--radius-panel);
            padding:12px 16px;font-weight:600;cursor:pointer;}
.toc-toggle .hamb{width:20px;height:14px;position:relative;}            /* animated to X when open */
.toc-toggle .hamb span{position:absolute;left:0;width:100%;height:2px;background:var(--slate);
                       transition:transform .25s, opacity .25s, top .25s;}
/* When TOC is OPEN (not .collapsed), the hamburger animates into an X */
.toc:not(.collapsed) .hamb span:nth-child(1){top:6px;transform:rotate(45deg);}
.toc:not(.collapsed) .hamb span:nth-child(2){opacity:0;}
.toc:not(.collapsed) .hamb span:nth-child(3){top:6px;transform:rotate(-45deg);}
@media(max-width:900px){
  .shell{grid-template-columns:1fr;gap:0;}
  .toc{position:static;border:var(--rule);border-radius:var(--radius-panel);background:var(--ivory);}
  .toc-toggle{display:flex;}
  .toc .eyebrow{display:none;}                 /* desktop-only heading */
  .toc ol{max-height:1600px;overflow:hidden;transition:max-height .3s ease;}
  .toc.collapsed ol{max-height:0;}             /* collapsed = only the toggle visible */
}
```

Every numbered section is an anchor target (`<section id="s3" ...>`); the TOC links to them, and cross-references in the prose (e.g., "see §3 Valuation") link too. A small scrollspy (in the template) toggles `.active`. The template's JS also: starts the TOC **collapsed** on mobile, toggles it on the hamburger button, and **auto-collapses after the user follows a link** (so mobile readers jump to a section and the menu gets out of the way). On desktop (≥900px) the toggle is hidden and the rail is always open — the sticky behaviour is unchanged.

**The TOC JS is the single most fragile part of the template — keep its structure intact when filling the template.** The whole script is one `<script>` block at the end of `<body>`, structured as a single `initReportInteractivity()` function gated on `DOMContentLoaded` (or run immediately if the DOM is already parsed). Inside it are **two independent `try { … } catch { … }` blocks** — one for scrollspy, one for the collapsible TOC toggle — so a runtime error in one (e.g. `IntersectionObserver` missing, a malformed selector) can never disable the other. Do **not** collapse the two blocks back into separate IIFEs that share a script tag: an uncaught throw in the first IIFE will halt script execution and the second IIFE never runs, which leaves the mobile TOC permanently open and un-closable (this was a real production bug). Rules:

- **Do** keep both blocks wrapped in their own `try/catch`.
- **Do** gate on `DOMContentLoaded` (with the `readyState` fallback) so the script works whether the DOM is ready or not.
- **Do** bind the toggle as a single listener on `.toc-toggle` that calls `e.preventDefault()` then `classList.toggle('collapsed')`. Never bind the same handler twice.
- **Do** use **event delegation** for link-follow auto-collapse: one listener on the `.toc` nav that checks `e.target.tagName === 'A'`. Do **not** loop over every `.toc a` and bind a per-link handler — that pattern silently no-ops if any link is re-rendered, and it multiplies the number of things that can go wrong.
- **Don't** reintroduce the `btn.dataset.touched` flag and the "reset on resize unless touched" logic — the simpler resize handler (`if(!isMobile()) remove('collapsed')`) is correct and avoids state drift across breakpoint crossings.
- **Don't** move the script, change `<script>` to `<script defer>`, or split it across files — the template is one self-contained file by design.

**Mobile (≤900px): the toggle bar is `position:fixed` at the very top**, so it stays reachable no matter how far down the reader scrolls — they never have to scroll back up to open the menu. The page gets `padding-top:64px` so content starts below the bar; every anchor target gets `scroll-margin-top:64px` so a jumped-to section isn't hidden behind the bar. When opened, the list **drops down as an overlay** capped at ~70vh with its own internal scroll, leaving the page behind usable; closing collapses it to just the bar. On desktop the rail reverts to `position:sticky` at `top:32px` and the toggle is hidden.

```css
@media(max-width:900px){
  .shell{padding:64px 16px 80px;}                 /* 64px = sticky bar height + gap */
  section, h3[id]{scroll-margin-top:64px;}        /* jump target clears the fixed bar */
  .toc{position:fixed;top:0;left:0;right:0;z-index:100;background:var(--ivory);
       border-bottom:var(--rule);box-shadow:0 1px 6px rgba(0,0,0,.05);}
  .toc-toggle{display:flex;}                      /* the always-visible bar */
  .toc ol{max-height:70vh;overflow-y:auto;transition:max-height .3s ease;}  /* overlay on open */
  .toc.collapsed ol{max-height:0;overflow:hidden;}
}
```

---

## Components

### Document header
Title (serif), the **company logo**, a status pill ("Research — not financial advice"), and a metadata line (ticker · market · currency · as-of date) in mono. The logo sits **left of the title** in a flex `.head-title` row; embed it as a self-contained `data:image/png;base64,...` (never an external URL) so the report stays a single portable file.

```html
<header class="rep-head">
  <div class="head-top">
    <div class="head-title">
      <img class="logo" src="data:image/png;base64,..." alt="[Company] logo" width="64" height="64">
      <h1>Company Name</h1>
    </div>
    <span class="pill">Equity Research · Not financial advice</span>
  </div>
  <div class="meta mono">TICKER.BK · SET · THB · as of 6 Jun 2026</div>
</header>
```
```css
.rep-head{margin-bottom:40px;}
.head-top{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;}
.head-title{display:flex;align-items:center;gap:18px;min-width:0;}
.logo{width:64px;height:64px;flex-shrink:0;border-radius:10px;object-fit:contain;
      background:var(--white);border:var(--border);padding:4px;}   /* white pad so transparent/dark logos read on ivory */
@media(max-width:520px){.logo{width:52px;height:52px;}.head-title{gap:12px;}}
.pill{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.06em;
      color:var(--gray-500);background:var(--gray-100);border:var(--border);border-radius:999px;
      padding:5px 11px;white-space:nowrap;}
.meta{color:var(--gray-500);font-size:13px;margin-top:8px;}
```

**Logo source convention** (so reports are consistent and offline-portable): resolve via the **3-step chain** in `references/logos.md`, then embed it base64. Quick reference:

| Market | Primary source | Fallback |
|---|---|---|
| **Thai SET** | `https://media.set.or.th/common/logo/company/{SYMBOL}.png` (drop `.BK`; e.g. `PTT`, `CPALL`, `DELTA`) — 140×140, brand-accurate | Google S2 favicon |
| **US (common stock)** | `https://storage.googleapis.com/iex/api/logos/{TICKER}.png` (raw ticker; e.g. `AAPL`, `MSTR`, `NVDA`) — 128×128 | Google S2 favicon with domain from the lookup table |
| **US preferred / sub ticker** (e.g. `STRC`, `STRK`) | Use the **parent issuer's** common ticker (`MSTR` for STRC) | Google S2 favicon |
| **Other / all else fails** | Google S2 `https://www.google.com/s2/favicons?domain={DOMAIN}&sz=128` (needs domain, `curl -sL`) | 2-letter monogram SVG (never empty) |

Always embed as `data:image/png;base64,...` — do not link to the remote URL, which would break offline and on mobile/slow networks. See `references/logos.md` for the full chain, the ticker→domain lookup table, and the "what NOT to use" list (Clearbit is dead, logo.dev free tier is broken, TradingView CDN returns 403, etc.).

### KPI / verdict band
A grid of stat cards (used for the Executive-Summary verdict and any section's key numbers). `.warn` adds a left accent border for the figure that needs attention.

```css
.band{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;}
@media(max-width:520px){.band{grid-template-columns:1fr;}}
.stat{background:var(--white);border:var(--border);border-radius:var(--radius-panel);padding:20px 22px;}
.stat{min-width:0;}
.stat.warn{border-left:4px solid var(--watch);}
.stat .v{font-family:var(--serif);font-size:40px;font-weight:500;line-height:1;margin-bottom:8px;}
.stat .k{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--gray-500);}
.stat .d{font-family:var(--mono);font-size:11px;margin-top:6px;}
.stat .d.up{color:var(--good);} .stat .d.down{color:var(--bad);} .stat .d.flat{color:var(--gray-500);}
```

### Section + rule
```css
section{margin-bottom:56px;scroll-margin-top:24px;}
.sec-h{display:flex;align-items:baseline;gap:12px;}
.sec-no{font-family:var(--mono);font-size:13px;color:var(--watch);}   /* "3" tick before the title */
hr.div{border:none;border-top:var(--rule);margin:0 0 22px;}
```

### Dense table
Uppercase sans header on a gray band, hover rows, generous padding. The workhorse for shipped/peer/financial/assumption tables.
```css
table{width:100%;border-collapse:separate;border-spacing:0;background:var(--white);
      border:var(--border);border-radius:var(--radius-panel);overflow:hidden;font-size:14px;}
thead th{text-align:left;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;
         color:var(--gray-500);background:var(--gray-100);padding:12px 16px;border-bottom:var(--rule);}
tbody td{padding:13px 16px;border-bottom:1px solid var(--gray-100);vertical-align:middle;}
tbody tr:last-child td{border-bottom:none;}
tbody tr:hover{background:var(--ivory);}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;}
.table-wrap{width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:var(--radius-panel);}
.table-wrap table{min-width:640px;}
@media(max-width:720px){table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;}}
```

### Judgement chip / dot
Encodes the read on a metric or risk.
```css
.chip{display:inline-flex;align-items:center;gap:7px;font-size:12px;color:var(--gray-700);}
.dot{width:9px;height:9px;border-radius:50%;flex-shrink:0;}
.dot.good{background:var(--good);} .dot.watch{background:var(--watch);} .dot.bad{background:var(--bad);}
.tag{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.05em;
     padding:3px 8px;border-radius:4px;background:var(--gray-100);color:var(--gray-700);}
```

### Callout panel
For the thesis, the 3-P verdict, or a key caveat. Oat background sets it apart.
```css
.callout{background:var(--oat);border-radius:var(--radius-panel);padding:22px 24px;}
.callout.accent{background:var(--white);border-left:4px solid var(--watch);}
```

### Sparkline (5-yr mini-trend) — inline SVG, no library
Render one per dashboard metric. Color the stroke by judgement.
```html
<svg class="spark" viewBox="0 0 120 32" preserveAspectRatio="none" aria-hidden="true">
  <polyline fill="none" stroke="var(--good)" stroke-width="2"
            points="0,24 30,20 60,14 90,12 120,7"/>
</svg>
```
```css
.spark{width:120px;height:32px;display:block;}
```
Build the `points` by mapping 5 yearly values to x = 0,30,60,90,120 and y = 32·(1 − (v−min)/(max−min)).

### Sensitivity heatmap (WACC × g, 5×5)
A `<table>` where each cell's background interpolates from `--bad` (low value) through neutral to `--good` (high), with the base case ring-highlighted. Keep text dark; tint the cell background lightly (e.g., `background:color-mix(in srgb, var(--good) NN%, var(--white))`).

### Moat meter (§1.2)
The signature visual for the Moat subsection: a labelled strength bar + a durability arrow, anchored to the ROIC−WACC spread as the quantitative proof.
```html
<div class="moat">
  <div class="moat-scale" aria-label="Moat strength: Wide">
    <span class="seg on"></span><span class="seg on"></span><span class="seg on"></span>
    <span class="seg on"></span><span class="seg"></span>
  </div>
  <div class="moat-meta">
    <span class="tag">Wide</span>
    <span class="chip"><span class="dot good"></span>Durability: widening ↑</span>
    <span class="mono">ROIC−WACC: +6.4 pp</span>
  </div>
</div>
```
```css
.moat-scale{display:flex;gap:5px;}
.moat-scale .seg{height:12px;flex:1;border-radius:3px;background:var(--gray-300);}
.moat-scale .seg.on{background:var(--good);}     /* shade by strength: bad→watch→good */
.moat-meta{display:flex;align-items:center;gap:16px;margin-top:10px;flex-wrap:wrap;}
```
Pair with a small ROIC−WACC 5-yr sparkline so the moat claim is backed by the spread trend, not asserted.

### Footer
```css
footer{margin-top:64px;padding-top:20px;border-top:var(--rule);
       font-family:var(--mono);font-size:12px;color:var(--gray-500);}
```

---

## Print CSS

A filing must print cleanly. Hide the TOC rail, go full width, force black ink, and break between top-level sections.
```css
@media print{
  body{background:#fff;}
  .shell{display:block;max-width:none;padding:0;}
  .toc{display:none;}
  .doc{max-width:none;}
  section{break-inside:avoid;}
  h2{break-after:avoid;}
  a{color:var(--slate);text-decoration:none;}
  .stat,table,.callout{box-shadow:none;}
}
@page{margin:18mm;}
```

---

## Do / don't

- **Do** label every figure with units/currency; right-align numerics with `tabular-nums`.
- **Do** color by judgement (good/watch/bad), and keep everything else in ink + gray.
- **Do** keep one reading column; let tables and SVG be full column-width.
- **Do** embed the company logo as base64 in the header — it gives the report a recognizable, filing-grade cover at a glance.
- **Do** make the TOC collapsible on mobile (hamburger toggle, starts collapsed, auto-collapses after a link is followed) so the first viewport stays clean on phones.
- **Don't** brand-match the palette to the company by default — this is a sober house style like a filing. (A single accent override is allowed if explicitly requested.)
- **Don't** add chart libraries, web fonts, frameworks, or animation. Inline SVG and a few lines of vanilla JS for scrollspy + TOC toggle only.
- **Don't** turn it into slides — no fixed-aspect stages, no per-screen pagination. It is a continuous document.
- **Don't** let mobile users hit page-level horizontal scrolling. KPI cards must wrap, wide tables must scroll inside their own container, and Thai text must not clip.
- **Don't** link the logo or any image to a remote URL — embed as base64 so the file is self-contained and works offline.
