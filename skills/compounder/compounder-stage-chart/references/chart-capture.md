# Getting the two charts into the report

Two images are needed — one monthly, one weekly — and both must end up **inside** the HTML file. The report is a single self-contained document that has to work with no network, so a remote `src` is a defect, not a shortcut. Every asset is either a `data:image/png;base64,...` payload or inline SVG markup.

There are two ways to produce them. Which one ran is recorded in `chart_assets[].source`, because a reader deserves to know whether they are looking at a captured chart or a drawing.

---

## Path A — `TRADINGVIEW_MCP`

Where a TradingView capture tool is connected (`tradingview_chart_image` or equivalent), use it. It produces the chart a reader recognises, with the exchange's own data.

Capture twice, changing only the interval:

| Capture | Interval | Range | Overlay |
|---|---|---|---|
| Monthly | `1M` | 10 years where available | 10-period SMA |
| Weekly | `1W` | 5 years where available | 30-period SMA |

Then:

1. **Validate the bytes before embedding.** A real PNG is over 500 bytes and starts with the magic bytes `89 50 4E 47`. Anything smaller, or anything that is HTML, is an error page — treat it as a failed capture and move to Path B rather than embedding a broken image.
2. **Base64-encode and inline it** into `src="data:image/png;base64,..."`. Never keep the remote URL.
3. **Caption it** with symbol, exchange, interval, and the capture timestamp. A chart without a capture date becomes wrong silently.
4. Record `source: TRADINGVIEW_MCP` and the capture date in `chart_assets`.

A capture that succeeds for one interval and fails for the other is fine: record each asset's source independently and let one be `TRADINGVIEW_MCP` and the other the fallback.

---

## Path B — `RENDERED_SVG` (the fallback)

Where no capture tool is connected, `scripts/stage_read.py` renders both timeframes as inline SVG from the bars it already pulled. This is a genuine fallback, not a placeholder — and it can do one thing Path A cannot, which is draw the **business life-cycle bands underneath the price**, so the cross-reading in `stage-business-alignment.md` becomes visible rather than described.

Each rendered chart carries:

- **Price** as a line of closes (not candles — at 120 monthly bars, candles are noise at report width).
- **The moving average** the stage was judged against, drawn as a second line and labelled with its length.
- **Chart-stage bands** as background shading across the x-axis, one band per stage run, labelled with the stage number and its start date.
- **A marker at `stage_since`** for the current stage, so the date in the prose has a place on the picture.
- **The unclosed bar** drawn, and visually distinguished — it is real price, and it was excluded from the stage judgement.
- **Volume** as a low-opacity bar strip along the bottom, with the 12-bar average line, because Weinstein's stage transitions lean on volume expansion.
- **Axis labels** carrying the currency, and a caption with ticker, interval, bar count, and the as-of date.

### Rendering rules

- **No external anything.** No web fonts, no chart library, no image references. Plain SVG elements and the report's own font stack.
- **Both themes.** Colours come from the report's CSS custom properties (`var(--ink)`, `var(--accent)`, `var(--line)`, and the judgement tokens) rather than being hard-coded, so the chart follows the reader's light or dark setting like the rest of the page. A hard-coded `#000` stroke disappears in dark mode.
- **Responsive.** A `viewBox` with `width:100%` and `height:auto`, so it scales on a phone rather than forcing the page to scroll sideways.
- **Legible small.** At 360px wide the moving-average label, the stage numbers and the axis dates must still be readable; drop intermediate x-axis ticks rather than shrinking type below 11px.
- **Stage bands are shading, not decoration.** Use the design system's judgement tokens at low opacity, keyed to the stage meaning, and never a rainbow.

Record `source: RENDERED_SVG`, the number of bars drawn, and the as-of date.

---

## What goes into `chart_assets`

For each of the two timeframes:

```json
{
  "timeframe": "monthly",
  "source": "TRADINGVIEW_MCP",
  "captured_on": "2026-08-24",
  "interval": "1M",
  "bars": 120,
  "moving_average": "10-month SMA",
  "asset": "data:image/png;base64,...",
  "caption": "CPRT · NASDAQ · monthly · captured 2026-08-24"
}
```

For a rendered chart the `asset` holds the SVG markup instead, and `bars` is what was actually drawn rather than what was requested.

---

## Failure handling

- **No bars at all** for a timeframe: record the timeframe with `source: UNAVAILABLE` and the reason, and let the report say so in words. Do not substitute a different interval and label it as the missing one.
- **Short history** — a company listed two years ago has no ten-year monthly chart. Draw what exists, record the true bar count in `data_quality`, and let the stage read say that a base cannot be distinguished from a first advance on this much history.
- **A capture tool that returns an error page** is a failed capture, not an asset. Fall back and record it.
- **Never fabricate a chart.** No drawn-from-memory prices, no illustrative shapes, no "representative" charts from another ticker. An absent chart with a stated reason is acceptable; an invented one is not.
