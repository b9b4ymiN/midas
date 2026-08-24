---
"midas-skills": patch
---

Two defects the ANTA Sports run found in the accumulation layer

Running the pipeline end to end on a company it was not built against surfaced both of these. Neither was visible from reading the code.

- **The gate told the pack it had no binding constraint.** The `proven-compounder` branch carried "with no binding constraint" as fixed wording, which contradicted the `binding_leg` field sitting beside it in the same pack. It now names the leg and says that it constrains the rate rather than blocking the plan.
- **The bands stopped discriminating and said nothing about it.** ANTA trades below what a no-growth business would be worth at a 10% required return, so inverting the expectations arithmetic put the accumulate ceiling at 3.28 times the traded price — every price a buyer could pay landed in one band. The arithmetic was right and the output was useless. `plan_math.py` now reports `band_discrimination`, flagging `BANDS_DO_NOT_DISCRIMINATE` when the ceiling is more than twice the price, and `accumulation-plan.md` requires the report to say so in words instead of quoting a ceiling nobody will ever see. The plan's shape then has to come from the staging and the kill conditions.
