---
name: business-narrative
description: >
  Research and structure the qualitative business story of a public company the way Aswath
  Damodaran does in "Narrative and Numbers," then translate it into the valuation inputs a
  model consumes — growth path, margins, reinvestment, and risk. Use this skill before
  valuing a company, or whenever the user asks: "what's the story on NVDA", "understand the
  business", "business model of CPALL", "how does this company make money", "investment
  narrative", "bull case or bear case", "is the growth story credible", "what's the moat",
  or "revenue mix and segments". It builds four story pillars (income structure, model and
  moat, industry and TAM, growth and reinvestment quality), classifies the life cycle,
  applies the possible/plausible/probable test, and outputs a Narrative Brief plus a
  story-to-numbers map that hands assumption ranges to company-valuation. Step 2 of the
  both-stock-analysis pipeline. Always research current filings and IR material — never
  narrate revenue mix, strategy, or guidance from stale memory.
---

# Business Narrative

A number without a narrative is a guess; a narrative without numbers is a fairy tale. This skill builds the disciplined story side of a valuation and hands it, as concrete assumption ranges, to the numbers side. Work in the spirit of Damodaran: every claim about the business must eventually attach to one of four value drivers — **cash flows, growth, reinvestment efficiency, and risk (cost of capital)** — or it is decoration.

The deliverable is a **Narrative Brief** ending in a **story-to-numbers map**. That map is the whole point: it is what makes the downstream DCF assumption-driven rather than default-driven.

**Disclaimer:** Research and educational output only. Not financial advice.

---

## What you produce (output contract)

Hand the next step (valuation) a brief with these parts. The final table is mandatory — it is the handoff.

1. **One-line business description** — what the company sells and to whom, in plain language.
2. **Four pillars** — income structure, business model and moat, industry and TAM, growth and reinvestment quality (sections below).
3. **Life-cycle stage** — young/growth/mature/decline, and what that implies for which driver dominates.
4. **The 3 P's verdict** — is the implied story possible, plausible, probable? Plus any "this time is different" flags.
5. **Story-to-numbers map** — the table that converts the story into suggested inputs and ranges for the value drivers, each justified by a pillar.

Keep it tight (roughly one page of prose + the map). Depth lives in the reference files.

---

## Step 1: Research the company on current sources

Do not reconstruct revenue mix, strategy, or guidance from memory — these change every quarter. Pull current figures from primary sources first: the latest annual report / 10-K (Thai listings: the 56-1 One Report), recent quarterly filings and the MD&A, the investor-relations deck, and the most recent earnings call. Use web search to fill gaps and to read the competitive landscape and TAM.

`references/research_checklist.md` lists exactly what to gather, the Thai/US source map, and how to find segment-level numbers (which yfinance does not expose). Read it now.

The output of this step is a fact base — segment revenue and margins, unit economics, capex, balance-sheet posture, market shares, regulatory exposure. The next steps interpret it.

---

## Step 2: Build the four story pillars

### Pillar 1 — Income structure (where the money actually comes from)
Break revenue into segments / products / geographies, and attach a margin to each. Profit usually concentrates somewhere different from revenue — find it. State: the revenue mix, the gross/operating margin by segment, and which segment is the real profit (and growth) engine. A consolidated number hides the company; the mix reveals it.

### Pillar 2 — Business model and moat
How do unit economics work, and what protects them? Cover pricing power, the moat (network effects, switching costs, scale economies, brand, cost advantage, regulatory licence), capital intensity, and how revenue converts to cash. Be specific about *durability*: a moat that is widening justifies different numbers than one that is eroding. Name the single biggest threat to the moat.

### Pillar 3 — Industry and TAM
Structural tailwinds and headwinds, competitive dynamics (consolidating or fragmenting?), regulatory shifts, the total addressable market, and where the company sits in it (share, and whether share is rising). Distinguish a large TAM the company can actually capture from a large TAM that invites competition and compresses returns.

### Pillar 4 — Growth and reinvestment quality
Where does future revenue come from, and — the Damodaran test — does the company earn returns **above its cost of capital** on the capital it reinvests to get that growth? Growth that earns below WACC destroys value; only growth that out-earns its cost is worth paying for. Tie this to the ROIC−WACC spread the valuation step computes. State whether growth is reinvestment-funded (capex/acquisitions) or capital-light, and whether the reinvestment is productive (capex rising *with* FCF, not against it).

---

## Step 3: Classify the corporate life cycle

Place the company on its life cycle, because the stage tells you which driver carries the value and which numbers to scrutinise. Full mapping (stage → dominant driver → typical story type → valuation posture) is in `references/narrative_framework.md`.

| Stage | What carries value | Watch most |
|---|---|---|
| Young / pre-revenue | Total addressable market, narrative | Survival, funding, unit economics proof |
| Growth | Revenue growth + reinvestment quality | Whether ROIC clears WACC as it scales |
| Mature | Margins, cash return, capital discipline | Moat durability, reinvestment restraint |
| Decline | Asset value, cash extraction | Value traps, terminal assumptions |

---

## Step 4: Run the 3 P's test

State the implied story explicitly, then stress it (Damodaran's possible → plausible → probable ladder):

- **Possible** — could this happen at all? (Almost anything is.)
- **Plausible** — is there a credible mechanism and precedent?
- **Probable** — given competition, capacity, and base rates, how likely is it?

The discipline is forcing a story down this ladder before it becomes a number. Then run the **"this time is different" checklist** in `references/narrative_framework.md`: total-market sizes that imply impossible share, margins above the best operator in history, growth sustained far past any comparable, or a moat assumed permanent. Flag anything the numbers cannot support, and say what the company would have to *do* to earn the optimistic case.

---

## Step 5: Translate the story into numbers (the bridge)

This is the handoff. Convert the narrative into suggested inputs and ranges for the value drivers, and say how each differs from a naive default and why. The downstream `company-valuation` skill defaults to mechanical values (historical-CAGR growth, 3-year-median margins, market beta); your job is to replace those with narrative-driven ranges where the story warrants it.

Produce this table:

| Value driver | Valuation input it sets | Naive default | Story-implied range | Which pillar justifies it |
|---|---|---|---|---|
| Growth | Revenue growth path (5-yr) | Hist. CAGR / analyst +1y | e.g. 8–12% fading to GDP | TAM × share (Pillar 3, 4) |
| Profitability | Operating margin trajectory | 3-yr median | e.g. expand 200–400 bps on mix/scale | Model & moat (Pillar 1, 2) |
| Reinvestment | CapEx % of revenue, ΔNWC | 3-yr median | e.g. elevated while ROIC > WACC | Reinvestment quality (Pillar 4) |
| Risk | Beta / ERP / country premium | Market beta, base ERP | e.g. nudge up for cyclicality/leverage | Model risk, geography (Pillar 2, 3) |
| Terminal | Terminal growth & margin posture | ~GDP | Compounder vs fading vs cyclical | Life cycle (Step 3) |

Also emit two **method signals** for the valuation step:
- **Path signal** — stable cash flows → DCF-friendly; pre-revenue / hyper-growth → lean on EV/Revenue + relative; bank/insurer → P/B, P/TBV; REIT → P/FFO. (Mirrors `company-valuation`'s method-applicability table.)
- **SOTP signal** — if the company has 2+ segments with genuinely distinct economics (different growth, margin, capital intensity), flag SOTP, because a blended multiple will misprice it.

Close with confidence: **high** if the four pillars agree and the 3 P's hold comfortably; **low** if the story leans on a single fragile assumption or fails "probable" — and tell the valuation step to widen its scenario ranges accordingly.

---

## Output format

```
# Business Narrative — [Company] ([Ticker])

**In one line:** [what they sell, to whom]

## Income structure
[revenue mix + margin by segment; where profit really sits]

## Business model & moat
[unit economics, moat type + durability, biggest threat]

## Industry & TAM
[tailwinds/headwinds, competitive structure, TAM, share trajectory]

## Growth & reinvestment quality
[growth sources; does reinvestment earn > WACC?]

## Life-cycle stage
[stage → dominant driver]

## The 3 P's test
[possible / plausible / probable verdict + "this time is different" flags]

## Story → numbers map
[the bridge table + path signal + SOTP signal + confidence]
```

---

## Caveats
- The brief is only as current as the sources — date your figures and prefer primary filings.
- Narratives are accountable to numbers: if a pillar implies a number the company has never achieved, say so rather than smoothing it over.
- Confidence is part of the deliverable; an honest "low" with wide ranges beats false precision.
- Not financial advice.

---

## Reference Files
- `references/narrative_framework.md` — Damodaran's narrative-to-numbers method: life-cycle → story-type → driver mapping, the value-driver bridge in depth, and the "this time is different" red-flag checklist.
- `references/research_checklist.md` — What to gather, the US/Thai primary-source map, where to find segment data, and how to avoid stale-memory errors.
