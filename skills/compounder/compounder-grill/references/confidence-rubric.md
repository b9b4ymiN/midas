# Confidence Rubric

Confidence answers: **how likely is this verdict to survive better information?** It is independent of both other axes. Deep evidence of mediocre economics can be held with High confidence; an Exceptional reading on a young company can be held with Low.

Never derive Confidence from Evidence Maturity or from Potential. A company can be well documented and still sit on one contested number that decides everything.

## Three inputs, all countable

### 1. Evidence composition

The share of the Evidence Ledger classed `FACT` or `DERIVED`, versus `MANAGEMENT_CLAIM`, `ESTIMATE`, `INFERENCE`, and `UNVERIFIED`.

What matters is not the overall mix but **the class of the entries the verdict actually rests on.** A ledger that is three-quarters FACT still supports only a Low-confidence verdict if the binding leg is carried by a single management claim.

### 2. Thesis-critical gaps

Count the entries in `critical_unknowns` that would change the label if resolved against the current reading. Gaps that would refine a number without moving a band do not count.

### 3. Sensitivity

Move the one or two assumptions the verdict leans on by **20%** in the adverse direction. Does the label move?

For most runs the assumption to test is the incremental return, since it drives the durable-growth figure and the hurdle comparison at once.

## Mapping

| Confidence | Evidence under the verdict | Thesis-critical gaps | Survives ±20% |
|---|---|---|---|
| **High** | Binding legs carried by FACT or DERIVED from primary statements | None open, or open ones cannot move the label | Yes |
| **Medium** | Binding legs mostly measurable, with one material claim or estimate | One or two open, direction known | Label moves at most one band |
| **Low** | A binding leg rests on management claim, single-period data, or inference | Any open gap that could move the label two bands, or an unresolved contradiction between sources | Label moves two or more bands |

The mapping is judgemental. Where the three inputs disagree, **the lowest governs** and the reason is recorded — a verdict that fails the sensitivity test is fragile regardless of how well sourced its inputs are.

## Cases that force Low

- A cross-provider conflict on a figure the verdict depends on, unresolved.
- A binding leg whose only support is a management statement not yet visible in reported results.
- An incremental return computed on a window shorter than three years where a longer one was available, or on a denominator that failed Guard B in `potential-rubric.md`. A genuinely short history is not a Confidence penalty by itself — it is carried by Evidence Maturity, and Confidence turns on how well the emerging-compounder bridge is evidenced.
- A promoted non-GAAP profit measure that could not be reconciled to the statutory figure, where that measure feeds the growth base.

## What Confidence is not

It is not a hedge. Lowering Confidence does not license a Potential label the evidence does not support — the caps in `potential-rubric.md` apply first and independently. Writing `Strong / Low` where Rule 3 requires a Moderate cap is the same error twice: guessing the axis, then discounting the guess instead of accepting the cap.
