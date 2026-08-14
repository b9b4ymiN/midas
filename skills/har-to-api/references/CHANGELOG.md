# CHANGELOG

## v2 — finance/research hardening

Driven by using v1 against stockanalysis.com, finviz, valueinvesting.io and
gurufocus for repeated equity work. Everything below is a bug found in
practice, not a speculative improvement.

### Fixed

**1. A capture taken after the session expired produced a "working" spec.**
`parse_har.py` kept 401/403 responses as ordinary endpoints. You would generate
a client, ship it, and every call would fail — with nothing in the spec hinting
why. Error responses are now quarantined into a separate `quarantined` list
with an actionable reason, and the run prints a warning.

*Reproduce on v1:* a HAR containing two 401 gurufocus requests yields
`www.gurufocus.com/api/stock/{symbol}/summary` as a normal endpoint.

**2. Two ID-ish segments in one path collided.**
`/compare/AAPL/MSFT/summary` normalised to `/compare/{symbol}/{symbol}/summary`
— a template that cannot be filled unambiguously. Params are now uniquely
named (`symbol`, `symbol2`, `id`, `id2`, …).

**3. Always-sent query params were indistinguishable from incidental ones.**
Every query param was recorded as a "sample", so a param the browser sends on
every request — SvelteKit's `x-sveltekit-trailing-slash=1`, a screener's
`p=quarterly` — was dropped from the generated client as noise. Params present
on *every* occurrence of an endpoint are now flagged and carried into the
profile under `always_present_query`.

The field name matters and the first one was wrong. See *"Correction: a
requirement I never tested"* below — frequency in a capture is evidence about
the **browser**, not about what the server will reject.

**4. Framework data routes were fragile to the noise filter.**
`/__data.json` (SvelteKit) and `/_next/data/<build>/*.json` (Next.js) are the
real API on many modern sites while looking like static assets. They are now
recognised explicitly and never filtered.

### Added

**`scripts/discover.py`** — walks a response, prints finance-looking leaves
with their values, and emits a ready-to-paste `facts` block. Handles
SvelteKit's **deduplicated** `__data.json` wire format, where a node's `data`
is a flat array and objects hold integer indices into it. Read naively,
`revenueTotal` comes back as `3` — an array index that looks like a plausible
small number. That is the worst class of bug: wrong, quiet, and typed
correctly.

**`scripts/fetch.py`** — the runtime layer:
- every fact carries `source`, `tier`, `as_of`, `url`
- dated snapshots + `--use-snapshot` for byte-identical replay
- yfinance fallback that is always tagged `FALLBACK` with a reason
- cross-provider disagreement > 2% reported, never silently resolved
- `auth` / `notfound` / `network` failures distinguished, since each needs a
  different response from the operator
- segment facts tagged with `segment_source` + a cross-check flag
- `json_path` supports `[key=value]` selection, not just `[i]`

**`profiles/`** — per-site route definitions. `stockanalysis.json` ships with
six endpoints verified working (2026-08-13), no capture and no auth required,
covering US and non-US listings including Thai SET. The other three are stubs
with capture recipes.

**`parse_har.py --profile`** — emits a profile skeleton alongside
`endpoints.json`, with `facts` left empty on purpose.

### Deliberately not done

- **Auto-mapping response fields to fact names.** The tool could guess that
  `revenueTotal` means `revenue_ttm`. It does not, because a wrong guess is
  indistinguishable from a right one downstream. `discover.py` proposes and a
  human confirms.
- **Auto-resolving provider disagreements.** Picking the "better" source hides
  the more useful signal: that two providers define the metric differently.
- **Segment inference.** See rule 4 in SKILL.md.

### Correction made during development

An earlier draft of this layer **refused segment facts outright**, on the
belief that stockanalysis exposed segments for some issuers and not others —
inferred from a rendered page that showed segments for one Thai large cap and
not for Thai Union.

That was wrong, and wrong in an instructive way. The rendered-page reading was
a summary; the `__data.json` route carries a full `revenue-segments` section
for Thai Union, sourced from S&P Global, whose ambient-seafood share (47.2% of
gross) matches the company's own results release exactly. The refusal rule was
built on a secondhand observation instead of the primary payload — the same
mistake the rest of this design exists to prevent.

What survived the correction is the *structural* concern, which is real: the
section genuinely is absent for some issuers, and positional addressing
(`sections[1]`) would then bind "segments" to whatever section slid into that
slot and return a plausible wrong number. Hence `[key=value]` selection, and
tagging rather than refusing.

### Correction: a requirement I never tested

**Claimed, in four places:** that `__data.json` routes on stockanalysis need
`?x-sveltekit-trailing-slash=1`, and that without it the server serves the HTML
page with a 200.

**Actually true:** the same route without the param returns identical JSON.
Verified live on 2026-08-14 against `TU` on `bkk` — both requests produced the
same field count off the same payload.

The mechanism was plausible. Some SvelteKit configurations really do behave
this way, and the param really is on every browser request. What was missing is
that I never dropped it and looked. Worse, the fixture server written to test
the behaviour *implemented my assumption* — it served HTML when the param was
absent — so the test suite reported a pass. A fixture that encodes the belief
it is meant to check will confirm anything.

Changed:

- `required_query` → **`always_present_query`** in `parse_har.py`, `fetch.py`
  and the profiles. The old key is still read, so existing profiles work. The
  name now describes what was measured — presence in the capture — rather than
  asserting a server rule.
- `fetch.py` no longer names a cause when a data route returns HTML. It reports
  what came back and lists the plausible explanations.
- `tests/fixture_server.py` keeps the param-gated route, relabelled as the
  synthetic scenario it is. It tests `fetch.py`'s error path against a server
  that *does* gate — it is not a model of stockanalysis.
- `tests/smoke_live.sh` step 2 now **observes** what the live route does
  without the param and prints the finding, instead of asserting an outcome.

**The generalisable part:** every claim in this layer that came from reading a
payload has held up. Both claims that came from reasoning about how a system
*ought* to behave — this one, and the segment refusal above — were wrong. The
data layer exists to stop invented numbers; it has to hold its own
documentation to that standard.

### Fixed: `discover.py` hid two-thirds of the payload

`walk()` capped list traversal at three elements. For year-series — lists of
scalars, newest first — three is the right call. But stockanalysis puts its
**seven named sections** in one array, so the cap stopped at
`sections[0..2]` and everything from `cash-flow-capex` onward was invisible:
operating margin, gross margin, FCF, capex, dividends per share, and the whole
valuation block. The tool reported *"52 candidate fields out of 302 leaves"*
and sounded thorough while doing it.

Lists are now split by content: scalars keep the cap of 3, lists of objects get
24. Same TU payload, after: **147 candidate fields out of 629 leaves**, all
seven sections reached.

`profiles/stockanalysis.json` was unaffected — its 28 fact paths were read off
the raw payload directly rather than through `discover.py`. The cost would have
landed on the next profile built with the tool, which is to say on
finviz, valueinvesting and gurufocus.
