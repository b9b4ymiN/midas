# Worked Examples

Three real-world sites the skill was designed against. Use these as mental
models when driving the skill on a new site.

---

## Example 1 — stockanalysis.com (Next.js, public-ish JSON API)

**Setup**
```
devproxy --urls-to-watch "(*.stockanalysis.com|api.stockanalysis.com)/*" \
         --record
```
Browse to `https://stockanalysis.com/quote/bkk/PTT/statistics/`.

**What we expect to find**
- Most data loads via `api.stockanalysis.com/api/symbol/s/PTT/statistics` (or
  a similar `_next/data/` route on the main domain).
- Response is JSON, big nested object with valuation / margins / dividends.

**Outcome**
- HAR typically contains ~5-15 real API calls plus ~200 noise requests
  (images, fonts, analytics). `parse_har.py` keeps the ~5-15, drops the rest.
- Generated client call:
  ```
  $env:HAR2API_AUTH='(none needed — public endpoint)'
  python client.py op1
  ```
  returns the full statistics JSON in one shot.

**Why it's a good first test**
- No login required → fastest smoke test.
- Multi-level nested JSON → exercises schema inference.
- Path parameter (`/PTT/`) → exercises ID normalization.

---

## Example 2 — valueinvesting.io (WACC page, light XHR)

**Setup**
```
devproxy --urls-to-watch "*valueinvesting.io/*" --record
```
Browse to `https://valueinvesting.io/PTT.BK/valuation/wacc`.

**What we expect to find**
- The page is mostly server-rendered; some metrics load via XHR.
- If HAR shows **zero** API endpoints after parsing → the page is pure SSR.
  In that case the skill's guidance is: this site is **not a good fit** for
  HAR→API. Fall back to scraping the HTML directly (out of scope for this
  skill) or pick a different page on the same site that does use XHR.

**Outcome (typical)**
- Either a couple of small JSON endpoints (good), or zero (skill reports
  "no API endpoints found — site may be server-rendered"). Both are valid
  outcomes — the skill is doing its job by telling you which.

---

## Example 3 — gurufocus.com (login-gated)

**Setup**
```
devproxy --urls-to-watch "*gurufocus.com/*" --record
```
1. Browse to gurufocus.com → **log in normally** in your own Chrome.
2. Navigate to `https://www.gurufocus.com/stock/PTXLF/summary`.

**What we expect to find**
- Summary data loads via XHR; auth is via session cookie set on login.
- Captured auth headers will include `Cookie` (and possibly `Authorization`).

**Outcome**
- `parse_har.py` redacts the cookie value but records the header name.
- Generated client reads the value from `$env:HAR2API_AUTH` at runtime.
- **Token lifetime:** session cookies expire. When the client starts
  returning 401/403, re-capture: stop dev-proxy, browse again, re-run the
  pipeline. The spec doesn't change — only the env var value does.

**Key lesson**
Cookies captured now may be invalid in an hour. The skill's design
(value in env, never in code) makes rotation painless.

---

## General pattern across all three

| Site type | Expect to find | If not found |
|-----------|----------------|--------------|
| SPA (React/Vue/Next) | 5-50 JSON XHRs per page | Site may be using SSR — try a different page |
| SSR (Rails/Django/PHP) | 0-2 XHRs | Skill will say "no API found"; consider HTML scraping |
| Login-gated | XHRs + auth headers | Re-capture when session expires |
| GraphQL SPA | One `/graphql` POST, many operations | See `troubleshooting.md` → GraphQL section |

---

## How to verify the generated client works

After `gen_client.py` runs:

```bash
# 1. List discovered operations
python client.py list

# 2. Call the first one (no auth needed for public sites)
python client.py op1

# 3. For path params, supply them as key=value
python client.py op1 symbol=PTT

# 4. Pipe through jq for a quick look
python client.py op1 --raw | jq .
```

If step 2 returns the same data you saw in the browser, the pipeline works
end-to-end. If it 401s, set `HAR2API_AUTH` (see SKILL.md "Auth" section).
