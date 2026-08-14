---
name: growth-outlook
description: >
  Judge whether a company's growth is repeatable, and put dates on the events
  that could change it. Use when the user asks "is this growth real", "where
  does growth come from", "what are the catalysts", "what's the outlook",
  "tailwinds and headwinds", "what could move this stock", or "when should I
  check back". Decomposes reported revenue growth into volume, price, expansion,
  acquisition and currency — grading each by whether it can happen again —
  separates structural tail/headwinds from cycle noise, and produces a catalyst
  table in which every row carries a date and a way to tell whether it happened.
  Step 4 of the both-stock-analysis pipeline, alongside the earnings read.
  Research and educational output only — not financial advice.
---

# Growth Outlook

Whether the growth repeats, and what is coming that could change it.

**Disclaimer:** Research and educational output only. Not financial advice.

---

## 1. Where growth came from

"Revenue grew 12%" is not information. Twelve percent from selling more units is
a different company from twelve percent from a currency move, and they deserve
different terminal assumptions.

```bash
python scripts/growth_decomp.py \
  --revenue 112000,100000 --years 2025,2024 \
  --volume-growth -0.03 --price-growth 0.09 \
  --acquisition-revenue 3000 --fx-growth 0.02
```

| Source | Repeatable? | What it means |
|---|---|---|
| **Volume** | best | selling more of the same thing — the only source that compounds without needing anything new |
| **Price** | conditional | real pricing power **only if volume held**; if volume fell, it is cost pass-through wearing a growth label |
| **Expansion** | finite | works until the market is covered — check whether new units earn what the old ones do |
| **Acquisition** | bought | has to be bought again next year; check goodwill and the share count first |
| **Currency** | not earned | not an operating result; quote the organic figure |

The script compounds these in the order they actually stack rather than adding
them, and reports whatever the components fail to explain as **unexplained**
instead of spreading it across the parts. A residual is a signal that something
is missing, and hiding it inside the known components is how a decomposition
becomes decorative.

**The test worth running every time:** price up while volume down. The script
flags it. It is the most common way a company that is losing customers reports a
year of growth.

## 2. Tailwinds and headwinds — structural only

A tailwind must be a force that **does not reverse in the next cycle**. Consumer
behaviour that changed permanently, regulation that binds for years, demographics.

Not: this quarter's demand, a competitor's stumble, a favourable input price.
Those are cycle, and the cycle is already in the normalised base from
`earnings-quality`. Counting them again as a tailwind is the same
double-counting Damodaran warns about, wearing different clothes.

For each: name it, say who it helps and who it hurts, and say what would tell
you it has stopped.

## 3. Catalysts — no date, no entry

The repo's own decision-journal template says it: *"catalyst + deadline — no
deadline = wishful thinking."* Until now nothing produced the deadline. This does.

| catalyst | date/window | direction | if it happens | confidence | how you'd know |
|---|---|---|---|---|---|
| Q2 results | ~14 Aug 2026 | ? | does margin recover as guided | certain to occur | the release |
| tuna cost hits P&L | Q3 2026 | negative | 2–4 month buffer runs out → margin falls | high | COGS/revenue ratio |
| tariff review | Nov 2026 | either | 0.5pp of gross margin at stake | medium | policy announcement |

Four rules:

1. **No date, no row.** A catalyst without a window cannot be waited for, and a
   thesis that depends on one cannot be falsified.
2. **The last column is the important one.** A catalyst you cannot verify has
   occurred is indistinguishable from one that never does. This is also what
   makes the thesis attackable later: *"you said this would happen — has it, and
   what are you reading to tell?"*
3. **Separate certain-to-occur from might-occur.** An earnings date is not a
   catalyst, it is a checkpoint; what it reveals is the catalyst.
4. **Size it.** "Positive" is not usable. Take the magnitude from
   `business-drivers`' sensitivity numbers where one exists.

---

## Output contract

- **Growth decomposition** with the durable share stated as a number
- **Structural tailwinds and headwinds**, each with a stopping signal
- **Catalyst table**, every row dated and verifiable
- **What you could not decompose** — said plainly

Feeds forward:

| To | What |
|---|---|
| `company-valuation` | only the **durable share** belongs in a terminal growth assumption |
| `investment-synthesis` | catalysts and dates go into the scenario timeline |
| `stock-grill` R5 | dated catalysts become the review date and the kill criteria |
| `earnings-quality` | if its growth gates failed, none of this may be stacked on the normalised base |

---

## The interaction that is easy to get wrong

`earnings-quality` produces a normalised base that **already assumes recovery to
mid-cycle**. If its growth gates failed, applying a growth rate from this skill
on top counts the same recovery twice and inflates the valuation.

Check the gate verdict before handing any growth number forward. When they
failed, the only growth that may be stacked is **post-recovery** growth — growth
made of something other than the return to normal — and it must be labelled as
such in the model.

## Reference files

- `references/growth-sources.md` — decomposing each source, and the evidence each requires
- `references/catalyst-rules.md` — dating catalysts, sizing them, and the verification column

## Caveats

- Decomposition is only as good as the disclosure. Many companies do not split
  volume from price; when they do not, say so rather than inferring it.
- A structural tailwind is a judgement about the future dressed as an
  observation. State what would falsify it.
- Not financial advice.
