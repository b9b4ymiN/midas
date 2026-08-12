# Logo Resolution Chain

How to fetch and embed the company logo in the report header for **any** market.
All fetches must end with the logo embedded as `data:image/png;base64,...` (or
`data:image/svg+xml;base64,...`) so the report stays a single self-contained file
that works offline. Never link to a remote URL.

> **Why this file exists.** The previous skill only specified a logo source for
> Thai SET stocks and a vague "company IR / favicon" fallback for everything
> else. That left US tickers, preferred-stock tickers (STRC/STRK/STRF), and
> non-Thai international listings with no logo at all. This file gives a
> deterministic **3-step chain** plus a ticker→domain lookup table so ~95% of
> tickers resolve without guessing.

---

## The 3-step resolution chain

Run these in order. **Stop at the first one that returns a valid image** (HTTP 200,
content-type `image/*`, byte size > 500 bytes — anything smaller is almost
certainly a placeholder/error GIF). Embed the winner as base64.

### Step 1 — Exchange media library (primary, market-specific)

| Market | URL pattern | Notes |
|---|---|---|
| **Thai SET** | `https://media.set.or.th/common/logo/company/{SYMBOL}.png` | Drop the `.BK` suffix. e.g. `PTT`, `CPALL`, `AOT`, `KBANK`, `DELTA`. Returns 140×140 PNG. Verified working 2026-06. |

For Thai tickers this is the only step you need — SET's library is complete and
brand-accurate.

### Step 2 — IEX Cloud public logo CDN (primary for US tickers)

```
https://storage.googleapis.com/iex/api/logos/{TICKER}.png
```

- Uses the **raw ticker** (no exchange suffix): `AAPL`, `MSFT`, `MSTR`, `NVDA`, `TSLA`.
- Returns 128×128 PNG for most large/mid-cap US names. Verified 2026-06.
- **Coverage gaps:** newer/smaller tickers, most preferred-stock tickers
  (`STRC`, `STRK`, `STRF`, `STRD` return 403), and any non-US listing return
  403 or a placeholder. If you get 403 or a tiny response → go to Step 3.
- **For preferred-stock / subsidiary tickers** (e.g. `STRC`): fall back to the
  **parent issuer's** common-stock ticker (`MSTR` for STRC) and use that logo.
  The header already names the issuer; the logo represents the company, not the
  instrument.

### Step 3 — Google S2 Favicon (universal fallback, needs domain)

```
https://www.google.com/s2/favicons?domain={DOMAIN}&sz=128
```

- Works for essentially any company with a website. Always returns a valid PNG
  (64–128px) for real domains.
- **Requires the company's primary domain**, not the ticker. Use the
  **ticker→domain lookup table** below. For any ticker not in the table,
  look up the company's IR site or main domain at analysis time and add it.
- Quality is lower than Steps 1–2 (it's a favicon, sometimes letter-mark only),
  but it always renders and is better than no logo.
- Use `curl -sL` (follow redirects) — Google returns a 301 to the actual image.

### Step 4 — Monogram fallback (last resort, never fails)

If all three steps fail (extremely rare), do **not** leave the header empty.
Render a deterministic **monogram** — the first 1–2 letters of the company name
or ticker on a tinted square — as an inline SVG:

```html
<!-- 2-letter monogram, no network needed -->
<svg class="logo" viewBox="0 0 64 64" role="img" aria-label="Strategy logo">
  <rect width="64" height="64" rx="10" fill="#E3DACC"/>
  <text x="32" y="42" text-anchor="middle" font-family="ui-serif,Georgia,serif"
        font-size="30" font-weight="600" fill="#3D3D3A">St</text>
</svg>
```

Derive the fill color deterministically from the ticker hash if you want
variety, or just use the oat accent (`#E3DACC`) to stay in the house palette.

---

## Ticker → domain lookup table (for Step 3)

Maintain this as you encounter new tickers. Domain = the company's primary
corporate website (the one Google would associate with the brand). When in
doubt, use the IR-site domain. Sorted by how often they appear in research.

### US mega-cap / large-cap

| Ticker | Domain |
|---|---|
| AAPL | apple.com |
| MSFT | microsoft.com |
| NVDA | nvidia.com |
| GOOGL, GOOG | google.com |
| AMZN | amazon.com |
| META | meta.com |
| TSLA | tesla.com |
| BRK.B | berkshirehathaway.com |
| JPM | jpmorgan.com |
| V | visa.com |
| JNJ | jnj.com |
| WMT | walmart.com |
| XOM | exxonmobil.com |
| PG | pge.com (proctergamble.com also works) |
| MA | mastercard.com |
| HD | homedepot.com |
| CVX | chevron.com |
| ORCL | oracle.com |
| ABBV | abbvie.com |
| KO | coca-cola.com |
| PEP | pepsico.com |
| COST | costco.com |
| BAC | bankofamerica.com |
| MDT | medtronic.com |
| NFLX | netflix.com |
| AMD | amd.com |
| INTC | intel.com |
| CRM | salesforce.com |
| ADBE | adobe.com |
| DIS | thewaltdisneycompany.com |
| NKE | nike.com |
| PYPL | paypal.com |
| UBER | uber.com |
| ABNB | airbnb.com |
| SHOP | shopify.com |
| SQ | squareup.com (Block, Inc.) |

### US mid-cap / thematic (crypto, fintech, etc.)

| Ticker | Domain | Note |
|---|---|---|
| MSTR | strategy.com | Strategy Inc. (renamed from MicroStrategy). `microstrategy.com` also resolves. **Use this logo for STRC/STRK/STRF/STRD** — all preferred series of Strategy. |
| COIN | coinbase.com | |
| HOOD | robinhood.com | |
| GLXY | galaxy.com | Galaxy Digital |
| MARA | marathondh.com | Marathon Digital |
| RIOT | riotplatforms.com | |
| CLSK | cleanspark.com | |
| PLTR | palantir.com | |
| SNOW | snowflake.com | |
| CRWD | crowdstrike.com | |
| NET | cloudflare.com | |
| DASH | doordash.com | |
| ABNB | airbnb.com | |
| RIVN | rivian.com | |
| LCID | lucidmotors.com | |

### International (also resolvable via Step 1/Step 3)

| Ticker | Domain |
|---|---|
| TSM (ADR) | tsmc.com |
| BABA (ADR) | alibabagroup.com |
| TCEHY (ADR) | tencent.com |
| NTES (ADR) | netease.com |
| SHEL | shell.com |
| SAP (ADR) | sap.com |
| ASML (ADR) | asml.com |
| NVO (ADR) | novonordisk.com |
| TM (ADR) | toyota-global.com |

---

## Helper one-liners

### Fetch + base64-embed in one shot (bash)

```bash
# Pick the right source per market, then base64-encode.
# Example: US ticker MSTR via IEX (Step 2)
curl -sL "https://storage.googleapis.com/iex/api/logos/MSTR.png" \
  | base64 -w0 \
  | awk '{print "data:image/png;base64," $0}'
```

### Validate the result (reject placeholders)

Before embedding, sanity-check: a real logo PNG from any of these sources is
**>500 bytes** and parses as a valid PNG (magic bytes `89 50 4E 47`). Anything
smaller or starting with `<html`/`{` is an error page — move to the next step.

```bash
# Returns "OK" only for a real PNG > 500 bytes
check_logo() {
  local f="$1"
  local sz; sz=$(wc -c < "$f")
  if [ "$sz" -lt 500 ]; then echo "FAIL: too small ($sz bytes)"; return 1; fi
  if head -c4 "$f" | od -An -tx1 | grep -q "89 50 4e 47"; then echo "OK ($sz bytes)"; return 0
  else echo "FAIL: not a PNG"; return 1; fi
}
```

---

## What NOT to use (tested 2026-06, don't waste time retrying)

| Source | Status | Why avoid |
|---|---|---|
| Clearbit Logo API (`logo.clearbit.com`) | Dead | Deprecated after HubSpot acquisition (2024). Returns HTTP 000. |
| logo.dev (`img.logo.dev`) | Broken on free tier | Requires API token; `token=free` returns identical-size HTML placeholder for every ticker. |
| `www.logo.dev/logo/{TICKER}` | Returns HTML, not image | 67KB HTML page for every ticker — not a real logo. |
| TradingView logo CDN (`s3-symbol-logo.tradingview.com`) | 403 blocked | Blocks unauthenticated curl. Only accessible in TradingView's own UI. |
| Stock Analysis (`stockanalysis.com/img/logo/...`) | 404 | That path does not exist. |
| Brandfetch API | 401 | Requires paid API key. |
| Yahoo Finance logo path | 429 | Rate-limited; unofficial and unreliable. |
| DuckDuckGo icons (`icons.duckduckgo.com/ip3/`) | Works but 32px only | Too small for a 64px header slot; use only if Google S2 also fails. |

---

## Workflow summary (paste this into the report-building step)

1. Resolve the **market** (from Step 1 of `both-stock-analysis`).
2. If Thai SET → Step 1 of this chain. Done.
3. If US (or US-listed preferred/ADR) → Step 2 (IEX CDN with raw ticker).
   - For a **preferred-stock ticker** with no logo, retry Step 2 with the
     **parent issuer's common ticker** (e.g. STRC → MSTR).
4. If Step 2 returns 403 / placeholder / missing → Step 3 (Google S2 with the
   domain from the lookup table, or looked up at analysis time).
5. If all fail → Step 4 monogram (never leave the slot empty).
6. **Always** base64-embed the result; never link remotely.
