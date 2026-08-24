---
"midas-skills": minor
---

Let the compounding line finish the thought: what the market thinks, and what to do about it

The Future Compounder run used to stop at the verdict. A reader who had just been told a business could compound for a decade was left with nowhere to go with it, and the write-up itself was typeset from scratch every time — no house style, no logo, no charts.

Three changes:

- **`compounder-stage-chart`** reads the share price on monthly and weekly bars at long-horizon settings, dates the phase it has been in, and crosses that with where the business is in its own life cycle. The disagreements are the point: a business compounding while its chart has been falling for two years is a question, not a coincidence. It runs for every company, including one that failed.
- **`compounder-accumulation-plan`** runs only for companies the compounding work cleared, behind a mechanical gate that reads the thesis pack and never sees a price. Where it passes, it answers what today's price already assumes rather than what the company is worth — the growth baked into the price against the growth the engine has shown — and turns that into three price bands and a conditional plan whose shape depends on which leg binds the thesis. Where it blocks, the report stops at the verdict and says what would reopen it.
- **The report becomes a document.** `compounder-bf-report` ships a green design system, a fillable HTML scaffold with a theme-aware palette, a working mobile table of contents and print rules, and a logo chain. Its opening is now an article of 3,000–6,000 characters rather than a capped summary block, because at 2,000 characters the only way to fit the finding was to write a specification.

The core layers are unchanged and still refuse to look at price: the exclusions now bind layers 0–5 explicitly, and the two new layers may never revise a verdict, a leg rating, or an evidence class. No fair value, no target price, and no entry geometry is produced anywhere in the run.
