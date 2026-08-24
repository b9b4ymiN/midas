# Logo Resolution Chain

The masthead carries the company's logo beside the title. It must end up embedded as `data:image/png;base64,...` (or `data:image/svg+xml;base64,...`) so the report stays one self-contained file that works with no network. **Never link a remote URL** — a report whose masthead breaks offline is not a document, it is a web page.

This file ships inside the skill on purpose. Each skill is installed as its own directory, so a reference to a sibling skill's file resolves to nothing at runtime.

---

## The chain

Run in order and **stop at the first valid image**. Valid means: HTTP 200, an `image/*` content type, and more than 500 bytes — a PNG starts with the magic bytes `89 50 4E 47`. Anything smaller, or anything that is HTML, is an error page, not a logo.

### Step 1 — Exchange media library

| Market | URL pattern | Notes |
|---|---|---|
| **Thai SET** | `https://media.set.or.th/common/logo/company/{SYMBOL}.png` | Drop the `.BK` suffix — `PTT`, `CPALL`, `AOT`, `KBANK`. Returns 140×140 PNG. |

For Thai tickers this is usually the only step needed; SET's library is complete and brand-accurate.

### Step 2 — Public logo CDN (US tickers)

```
https://storage.googleapis.com/iex/api/logos/{TICKER}.png
```

Raw ticker, no exchange suffix. Returns 128×128 for most large and mid-cap US names. Newer or smaller tickers, preferred-stock tickers, and non-US listings return 403 or a placeholder — go to Step 3.

For a **preferred or subsidiary ticker without its own logo**, retry with the parent issuer's common ticker. The masthead already names the issuer; the logo stands for the company, not the instrument.

### Step 3 — Favicon service (universal, needs a domain)

```
https://www.google.com/s2/favicons?domain={DOMAIN}&sz=128
```

Works for essentially any company with a website, and always returns a real PNG for a real domain. It needs the company's primary domain rather than the ticker — use the table below, or look the domain up at analysis time and add it. Fetch with `curl -sL`; the service redirects.

Quality is lower than Steps 1–2 — often a letter-mark — but it renders, and it is better than an empty slot.

### Step 4 — Monogram (the fallback that cannot fail)

If all three fail, do not leave the masthead empty. Render a deterministic **monogram** inline, in the report's own palette:

```html
<svg class="logo" viewBox="0 0 64 64" role="img" aria-label="Copart logo">
  <rect width="64" height="64" rx="10" fill="var(--accent-soft,#DCE9E3)"/>
  <text x="32" y="42" text-anchor="middle" font-family="var(--display)"
        font-size="28" font-weight="700" fill="var(--accent,#1D4F3F)">CP</text>
</svg>
```

One or two letters from the company name, the house green behind it. Because it uses the theme's custom properties it follows the reader's light or dark setting like everything else.

---

## Embedding

```bash
curl -sL "<url>" -o /tmp/logo.png
file /tmp/logo.png            # confirm it is a PNG, not HTML
base64 -w0 /tmp/logo.png      # paste into src="data:image/png;base64,..."
```

The `<img class="logo">` is 64×64 with white padding and a rounded border, so a logo with a transparent background stays visible in dark mode. That white plate is deliberate: most corporate logos are drawn for white paper and disappear on a dark ground.

---

## Ticker → domain lookup (for Step 3)

Extend it as new tickers appear. The domain is the company's primary corporate site — when in doubt, the investor-relations domain.

| Ticker | Domain |
|---|---|
| CPRT | copart.com |
| AAPL | apple.com |
| MSFT | microsoft.com |
| NVDA | nvidia.com |
| GOOGL, GOOG | google.com |
| AMZN | amazon.com |
| META | meta.com |
| BRK.B | berkshirehathaway.com |
| V | visa.com |
| MA | mastercard.com |
| COST | costco.com |
| KO | coca-cola.com |
| ADBE | adobe.com |
| ASML (ADR) | asml.com |
| TSM (ADR) | tsmc.com |
| 601318.SS | pingan.cn |

For a ticker that is not listed and whose domain is not obvious, look it up from the company's own filing cover page rather than guessing — a wrong domain returns a real favicon belonging to somebody else, which is worse than no logo.

---

## Checks before publishing

- The masthead `<img>` or inline `<svg>` is present, and its `src` starts with `data:` — not `http`.
- The logo renders in both themes; a dark-on-transparent mark still reads against the white plate.
- The image is under ~40KB after base64. A 2MB logo makes the file slow to open for no gain — resize before encoding.
- The `alt` text names the company.
