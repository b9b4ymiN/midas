# Research Foundations and Methodology Provenance

Every rule in this skill that could have been invented was taken from a published method instead. This file records which one, and what each source does *not* support — because the failure mode of a price layer bolted onto a durability pipeline is quietly reinventing a valuation and calling it something else.

For live work, consult the current original document and record the exact source used in the Evidence Ledger.

## Provenance fields

Each foundation below records:
- **Publication date** — date of the cited source/version when known.
- **Concept used** — the analytical idea inherited by this skill.
- **Source role** — method / measurement / empirical prior / governance prior.
- **Limitation** — what the source does *not* prove and how the skill must avoid overreach.

---

## Alfred Rappaport and Michael J. Mauboussin

### *Expectations Investing: Reading Stock Prices for Better Returns*
- **Authors:** Alfred Rappaport, Michael J. Mauboussin
- **Publication date:** 2001; revised and updated edition 2021 (Columbia Business School Publishing)
- **URL:** https://cup.columbia.edu/book/expectations-investing/9780231203043
- **Concept used:** The central inversion this skill is built on — take the market price as given and solve for the performance it implies, rather than building a value and comparing. The output of the analysis is an expectation, not a price.
- **Source role:** **Method**. It supplies the direction of the arithmetic and the discipline of treating the price as the input.
- **Limitation:** The book's full method reads expectations through explicit value drivers — sales growth, operating margin, and incremental investment — and locates the market-implied forecast period rather than fixing one. This skill uses a simplified single-growth form over a stated ten-year horizon, which is coarser. It must therefore be reported with its sensitivity and never quoted as a precise expectation, and it must not be described as the book's full method.

---

## Christopher W. Mayer

### *100 Baggers: Stocks That Return 100-to-One and How to Find Them*
- **Author:** Christopher W. Mayer
- **Publication date:** 2015
- **URL:** https://www.harriman-house.com/100baggers
- **Concept used:** The twin engine — long-run returns come from earnings compounding *and* the change in the multiple, so the two are decomposed rather than reported as one number. Also the patience argument that shapes the `proven-compounder` archetype: where the business does the work, entry price matters least.
- **Source role:** **Method** for the return decomposition; **empirical prior** for the archetype's staging.
- **Limitation:** A retrospective study of winners. It supports the decomposition and the disposition; it does not supply expected values, probabilities, or any basis for a price target. Its patience argument is drawn from survivors and says nothing about how to hold a business that turns out not to be one — which is why the kill conditions come from the thesis pack rather than from here.

---

## Stan Weinstein

### *Secrets for Profiting in Bull and Bear Markets*
- **Author:** Stan Weinstein
- **Publication date:** 1988
- **URL:** https://www.mheducation.com/highered/product/secrets-profiting-bull-bear-markets-weinstein/9781556238055.html
- **Concept used:** The four-stage taxonomy the staging rules read from `stage_pack`, at the long-horizon settings documented in `compounder-stage-chart`.
- **Source role:** **Method**, used only for describing the market's current phase.
- **Limitation:** Weinstein's own work is a trading method with entries, stops, and position rules. None of that is inherited here: this skill takes the stage vocabulary and nothing else, and it never converts a stage into an entry or an exit.

---

## Meb Faber

### *A Quantitative Approach to Tactical Asset Allocation*
- **Author:** Meb Faber
- **Publication date:** 2007 (Journal of Wealth Management); updated versions subsequently
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461
- **Concept used:** The 10-month simple moving average as a long-horizon trend filter, which is the instrument behind the monthly stage read this skill consumes.
- **Source role:** **Measurement**.
- **Limitation:** Published as a timing rule for asset-class allocation, tested on indices rather than single stocks, and evaluated on returns and drawdowns — none of which is claimed here. It is used only to justify the choice of averaging window.

---

## U.S. Securities and Exchange Commission

### *A Plain English Handbook: How to Create Clear SEC Disclosure Documents*
- **Issuer:** SEC Office of Investor Education and Assistance
- **Publication date:** August 1998
- **URL:** https://www.sec.gov/pdf/handbook.pdf
- **Concept used:** The sentence-level rules the plan is written under — active voice, everyday words, tables for complex information, no multiple negatives — and the standard of writing for one non-specialist reader.
- **Source role:** **Governance prior** for how the plan is written.
- **Limitation:** A disclosure-drafting guide. It governs how something is said, never whether it is true, and it supplies no analytical content.

---

## What no source here supports

Stated plainly, because these are the overreaches this layer is most exposed to:

- **No source here produces a fair value or a target price.** Rappaport and Mauboussin explicitly argue against the habit; Mayer's work is retrospective; Weinstein and Faber are about trend, not worth.
- **No source here supports converting a chart stage into a buy or a sell** in this pipeline's context, and the two trend sources are used for description only.
- **No source here supports position sizing** for any individual, and none is attempted.
