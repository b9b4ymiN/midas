---
name: har-to-api
description: Reverse-engineer a website's hidden JSON API from network traffic, then fetch from it reproducibly with full provenance. Use this whenever the user wants to call a website's data programmatically without a browser, automate data extraction from a site (especially financial dashboards like stockanalysis.com, valueinvesting.io, gurufocus.com, finviz.com), build a client/scraper from a HAR file, or convert recorded network traffic into an API. Also use when the user says "I want to fetch X from website Y directly", "this site has no API, how do I call it", "why do my numbers change between runs", "where did this figure come from", or shows a screenshot/tweet about deriving API clients from HAR capture.
---

# HAR → API

Turn a website's hidden XHR/fetch traffic into a callable API — then keep the
numbers it returns **traceable and reproducible**.

Two halves:

| Half | Scripts | What it does |
|---|---|---|
| **Capture** (one-time per site) | `parse_har` → `gen_openapi` → `gen_client` | Record traffic once, derive an OpenAPI spec + a Python client |
| **Fetch** (every run) | `discover` → `fetch` | Map the response to named facts, pull them with provenance, snapshot them |

The second half is what makes this usable for research rather than one-off
scraping. Any number that reaches a document should be able to answer three
questions — *where did you come from, when, and can I get you again* — and
`fetch.py` makes those answers structural rather than remembered.

## When to use

- User wants to pull data from a website **programmatically** (no browser).
- Site has **no documented API** but clearly loads JSON in the browser.
- User has a HAR file already and wants a client from it.
- User needs the **same numbers twice** — analysis, reports, anything audited.

## When NOT to use

- Site is pure server-rendered HTML with no XHR → no hidden API to find.
  (The skill detects this and says so — see troubleshooting.)
- Site requires solving CAPTCHAs or bypassing anti-bot (Datadome, etc.).
  Out of scope; don't try to defeat these.
- Traffic is WebSocket / raw TCP, not HTTP. Not supported.

Respect each site's terms of service and rate limits. This is built for
personal research use: cache aggressively, re-fetch rarely, redistribute
nothing.

---

## Prerequisites — Dev Proxy (one-time setup)

Uses **Microsoft Dev Proxy** as the capture tool because it lets the user
browse in their **own** browser with existing logins, is a standalone ~50 MB
binary, and has a built-in `HarGeneratorPlugin` with URL filtering.

```bash
winget install DevProxy.DevProxy --silent          # Windows
brew tap dotnet/dev-proxy && brew install dev-proxy # macOS
bash -c "$(curl -sL https://aka.ms/devproxy/setup.sh)"  # Linux
devproxy --version                                  # verify (restart terminal first)
```

First run installs a local CA cert so HTTPS can be decrypted **locally** —
nothing leaves the machine.

**Skip capture entirely when the site already exposes an open route.** Check
`profiles/` first: `stockanalysis.json` ships with six verified endpoints that
need no capture and no auth.

---

## Workflow A — capture a new site

### Step 1 — Capture traffic

Tell the user:
> I'm going to start a local proxy. Keep your browser open and do what you
> normally do on the site — log in if needed, navigate to the page with the
> data you want. Tell me "done" when you've seen the data load.

`devproxyrc.json`:
```json
{
  "plugins": [{
    "name": "HarGeneratorPlugin", "enabled": true,
    "pluginPath": "~appFolder/plugins/DevProxy.Plugins.dll",
    "configSection": "harGeneratorPlugin"
  }],
  "harGeneratorPlugin": { "includeUnsupportedRequests": false },
  "urlsToWatch": ["https://*.stockanalysis.com/*", "https://stockanalysis.com/*"],
  "logLevel": "info"
}
```
```bash
devproxy --configFile devproxyrc.json     # Ctrl+C when done → devproxy.har
```

> Already have a HAR (browser DevTools, Charles, mitmproxy)? Skip to Step 2.

### Step 2 — Parse + filter

```bash
python scripts/parse_har.py devproxy.har \
  --out output/endpoints.json \
  --profile profiles/<site>.json --provider-name <site> \
  --host-filter <site>.com
```

Drops static assets, ads and analytics; normalises IDs in paths
(`/PTT/` → `/{symbol}/`); redacts auth header **values**; marks query params
required vs optional; and **quarantines any request that came back 4xx/5xx**.

**Read the quarantine warning.** A capture taken after a session expired used
to yield a spec whose every call 401s — silently. Now it says so, and refuses
to emit those routes. If you see `!! N request(s) came back 401/403`, log in
and capture again before going further.

If `kept: 0` → `references/troubleshooting.md`.

### Step 3 — Generate spec + client (optional)

Only needed if you want a general-purpose client. For research use, skip
straight to Workflow B — `fetch.py` reads the profile directly.

```bash
python scripts/gen_openapi.py output/endpoints.json --out output/openapi.json --title "<site> API"
python scripts/validate_spec.py output/openapi.json
python scripts/gen_client.py output/openapi.json --out output/client.py --title "<site> API"
```

---

## Workflow B — fetch facts reproducibly

### Step 1 — Discover the fact paths

`parse_har` finds the *endpoints*; it deliberately leaves each route's `facts`
map empty, because deciding that "revenue_ttm lives at
`nodes[2].data.revenueTotal[0]`" is a judgement call. Guessing it would be
exactly the silent invention this layer exists to prevent.

`discover.py` does the tedious part:

```bash
python scripts/discover.py \
  --url "https://stockanalysis.com/quote/bkk/TU/financials/__data.json?x-sveltekit-trailing-slash=1" \
  --save /tmp/tu.json
```

It walks every leaf, prints the finance-looking ones with their values, and
emits a ready-to-paste `facts` block. **Check the printed numbers against the
page before pasting.** The tool proposes; you decide.

> **SvelteKit `__data.json`** (what stockanalysis.com serves) uses a
> *deduplicated* wire format: each node's `data` is a flat array and objects
> hold integer **indices** into it. Read it naively and `revenueTotal` comes
> back as `3` — an array index that looks like a plausible number.
> `discover.py` detects the format and rebuilds it automatically.

### Step 2 — Fetch

```bash
python scripts/fetch.py TU.BK --market bkk --profiles ./profiles
python scripts/fetch.py TU.BK --need revenue_ttm,net_income_ttm
python scripts/fetch.py TU.BK --providers stockanalysis,finviz   # precedence order
python scripts/fetch.py TU.BK --use-snapshot 2026-08-13          # replay, no network
python scripts/fetch.py TU.BK --no-fallback                      # fail loudly, don't degrade
```

Every fact comes back wearing its provenance:

```json
"revenue_ttm": {
  "value": 134984000000, "unit": "THB",
  "source": "stockanalysis", "tier": "primary",
  "as_of": "2026-03-31",
  "url": "https://stockanalysis.com/quote/bkk/TU/financials/__data.json?..."
}
```

---

## The four rules `fetch.py` enforces

**1. Missing stays missing.** A path that resolves to nothing produces a
warning and no fact. Nothing is inferred, interpolated, or carried over from a
previous run.

**2. Fallback is flagged, never silent.** When a primary source fails,
`fetch.py` may degrade to yfinance — but the fact is tagged
`"tier": "FALLBACK"` with the reason, the run prints a count to stderr, and the
flag is meant to travel all the way into whatever document consumes it. Use
`--no-fallback` when you would rather fail than quietly degrade.

**3. Disagreements are reported, not resolved.** Two providers giving the same
fact values more than **2%** apart produces a warning naming both. The first
provider in precedence order is used, but the conflict is on the record —
usually it means the two sources define the metric differently, which is worth
knowing before you build on either.

**4. Segment facts are allowed but never anonymous.** These providers *do*
expose segments — stockanalysis returns a full `revenue-segments` section for
Thai Union, sourced from S&P Global, and the split cross-checks against the
company's own results release. What they do not do is expose them *uniformly*:
the section is absent for issuers the provider has no segment data on, the
labels are the provider's rendering rather than verbatim reporting, and history
can be partial. So every segment fact is tagged with its `segment_source` and
carries a `cross_check_required` note, and the run warns out loud. Confirm the
mix against the filing before peer selection or driver work leans on it.

The matching structural rule: address list elements **by id, not position**.
`sections[id=revenue-segments]` returns `None` for an issuer with no segments;
`sections[1]` returns whatever section happens to sit there — a plausible
number bound to the wrong label.

---

## Auth handling

`parse_har.py` detects sensitive headers by name (Authorization, Cookie,
X-API-Key, …) and **redacts their values** before writing them anywhere. The
generated client and `fetch.py` read the value from `$HAR2API_AUTH` at runtime.

HAR files are effectively credentials. Treating them as secrets means the spec,
the profile and the client are all safe to commit or share.

**Rotation:** session cookies expire. `fetch.py` distinguishes an expired
session (`kind: "auth"`, with instructions) from a genuinely absent field
(`kind: "notfound"`) from a flaky network (`kind: "network"`, retried twice) —
because the three need different responses from you. When you see the auth
failure, re-capture and update the env var; the profile usually survives.

---

## Files

```
har-to-api/
├── SKILL.md
├── scripts/
│   ├── parse_har.py      HAR → filtered endpoints (+ --profile)
│   ├── discover.py       response → suggested fact paths
│   ├── fetch.py          profiles → facts with provenance + snapshots
│   ├── gen_openapi.py    endpoints → OpenAPI 3.0.3
│   ├── gen_client.py     OpenAPI → runnable client
│   └── validate_spec.py  spec sanity check
├── profiles/
│   ├── stockanalysis.json   6 endpoints VERIFIED, no capture needed
│   ├── finviz.json          stub — capture required
│   ├── valueinvesting.json  stub — may be pure SSR
│   └── gurufocus.json       stub — login required, do last
├── references/
│   ├── finance-profiles.md  per-site capture recipes + precedence table
│   ├── fact-schema.md       the fact record contract
│   ├── examples.md          3 worked sites
│   ├── troubleshooting.md   kept:0, 401s, GraphQL, pagination
│   └── CHANGELOG.md         what changed in v2 and why
└── templates/client.py.tmpl
```

Read `references/finance-profiles.md` before capturing a finance site, and
`references/troubleshooting.md` when `kept: 0` or the client 401s.

---

## Design notes

- **Local proxy over browser automation** — the user keeps their own session
  (cookies, logins, 2FA). Spawning a fresh headless browser loses all of that.
- **OpenAPI as the intermediate format** — the same spec can later feed
  MCP-server generation, TypeScript clients or Postman without re-capturing.
- **stdlib-only** — no pip install, no venv, runs anywhere Python 3.8+ exists.
  yfinance is imported lazily and only as a flagged fallback.
- **Empty `facts` by default** — the machine finds endpoints; a human confirms
  what the numbers mean. That seam is where correctness lives.
- **Snapshots over caching** — a cache optimises speed; a snapshot preserves
  *what you actually saw*. `--use-snapshot` is how you tell "the data moved"
  apart from "my code moved".

## Limitations

- **No WebSocket support.**
- **Schema inference is shallow** (1–2 levels); ambiguous fields type as string.
- **GraphQL partially supported** — operations collapse into one POST.
- **No anti-bot bypass.** Datadome, Cloudflare challenge, reCAPTCHA: out of scope.
- **`discover.py` proposes, it does not verify.** Always check a couple of the
  suggested numbers against the rendered page before trusting the mapping.
- Non-US coverage varies by provider. Gaps are reported as gaps.
