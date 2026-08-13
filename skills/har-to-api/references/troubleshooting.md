# Troubleshooting

## "No API endpoints found" after parsing

**Cause:** the page had no XHR/fetch calls — it was server-rendered (SSR)
or all traffic was filtered as noise.

**Diagnose:**
```bash
python parse_har.py capture.har --out endpoints.json
# look at the summary line: "kept: 0" means nothing survived filtering
```

**Fixes:**
- Try a different page on the same site. Dashboards, tables, and "load
  more" buttons almost always fire XHR; pure article pages often don't.
- Relax the filter: re-run with `--host-filter` set to the site's API host
  (look at `hosts seen` in the summary — one of them is usually the API).
- If the site is genuinely SSR, this skill is the wrong tool. Scrape HTML
  directly with `WebFetch` + a parser instead.

---

## Token / cookie expired (401 or 403)

**Symptom:** generated client worked yesterday, 401s today.

**Cause:** the captured auth token (cookie, bearer, etc.) has expired.

**Fix:**
1. Stop dev-proxy if still running.
2. Start it again: `devproxy --urls-to-watch "<site>/*" --record`
3. Re-browse the site in your own browser (login again if needed).
4. Stop dev-proxy, re-run `parse_har.py` → `gen_openapi.py` → `gen_client.py`.
5. Update `$env:HAR2API_AUTH` with the new value.

The spec rarely changes when only the token expired. You can skip
`gen_client.py` and just update the env var if the endpoints are the same.

---

## GraphQL sites

**Symptom:** HAR shows many POST requests to a single `/graphql` (or
`/api/graphql`) endpoint with different JSON bodies.

**Why it's special:** all operations share one URL. They're distinguished
by the `operationName` field inside the request body, not by the URL path.

**Approach (manual, not yet automated):**
1. `parse_har.py` will collapse them into one POST operation (correct —
   they're the same URL).
2. Open the generated OpenAPI spec and look at `requestBody.example` —
   it's one captured operation. To use a different operation, edit the
   body sent by the client.
3. For heavy GraphQL use, consider a dedicated GraphQL client instead of
   the generated REST-style client.

**Future enhancement:** a `--graphql` flag that splits operations by
`operationName` into separate OpenAPI operations. Tracked as a TODO.

---

## Pagination (next-token / cursor)

**Symptom:** the same endpoint appears many times with different query
params (`?page=1`, `?page=2`, ... or `?cursor=abc`).

**What `parse_har.py` does:** dedupes by URL template — concrete query
values are kept as samples, not as separate operations. So one operation
will appear, with `page` (or `cursor`) listed as a query parameter.

**In the client:**
```bash
python client.py op1 page=1
python client.py op1 page=2
```

---

## CORS / preflight (OPTIONS) requests

`parse_har.py` keeps OPTIONS requests only if they returned JSON, which is
rare. You can usually ignore them — the actual data call is the GET/POST
that follows.

---

## Huge response bodies slow down parsing

**Fix:** `parse_har.py` truncates bodies to 8 KB before storing. If you
need full bodies (e.g. for richer schema inference), raise `MAX_BODY_SAMPLE`
at the top of the script.

---

## dev-proxy didn't capture anything

**Checklist:**
- Did you start dev-proxy **before** browsing? Traffic before start isn't
  recorded.
- Did you trust the Dev Proxy CA certificate on first run? Without trust,
  HTTPS interception fails silently.
- Is `--urls-to-watch` matching the right host? Use a broad pattern like
  `*example.com/*` if unsure.
- On Windows, did you restart your terminal after `winget install`? The
  PATH entry needs a fresh shell.

---

## Generated client fails with "Network error"

**Cause:** the captured base URL is unreachable from your script context
(corporate proxy, VPN needed, host only resolves in-browser, etc.).

**Fix:**
- Confirm the URL works from `curl` first:
  ```bash
  curl -H "Authorization: Bearer $HAR2API_AUTH" "<url>"
  ```
- If a corporate proxy is required, set `HTTP_PROXY` / `HTTPS_PROXY` env
  vars — Python's `urllib` honors them.

---

## Schema inference looks wrong (e.g. everything is `string`)

**Expected behavior.** `gen_openapi.py` walks one level deep. For deeply
nested APIs the spec will be conservative — fields that look ambiguous
default to `string`.

**Fix:** open the generated `openapi.json` and refine the `properties`
blocks. The samples are kept under `example` so you can see the real shape.
