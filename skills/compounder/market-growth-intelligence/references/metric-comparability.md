# Metric Comparability Gate

## Trigger
Always before interpreting a KPI trend across periods.

## Method
For each thesis-critical series, compare:
- metric definition and denominator;
- consolidation/segment scope;
- owned/franchise or principal/agent recognition mix;
- acquisitions/divestitures;
- accounting/revenue-recognition changes;
- FX/currency basis;
- channel/customer-definition changes;
- fiscal-period/calendar changes;
- demand-evidence basis: sell-in shipments, sell-through/end demand, usage/consumption, bookings/orders, GMV, installed capacity, or another basis.

## Status
- `COMPARABLE` — same economic definition/basis.
- `ADJUSTED_COMPARABLE` — a documented adjustment makes the periods usable.
- `NOT_DIRECTLY_COMPARABLE` — trend may still be discussed, but not as a clean like-for-like series.
- `UNRESOLVED` — available disclosure is insufficient.

## Adjusted-to-Statutory Reconciliation (mandatory)

The checks above ask whether *this period* compares to *last period*. This one
asks whether the headline profit compares to the audited one. Run it on any
company reporting a profit measure of its own devising — "core profit",
"underlying earnings", "adjusted EBITDA", "normalised net income".

**Method.** Take the promoted figure, walk it back to statutory profit
attributable to owners, and account for every unit of the difference:

```
reported adjusted profit
  ± each disclosed reconciling item
  = statutory net profit attributable to owners
```

Anything that will not reconcile is a gap, not a rounding difference.

**When the reconciliation is not disclosed, arithmetic still bounds it.** If
the company names non-operating items in the same release, test whether they
sit inside or outside the adjusted figure by asking whether
`adjusted + items ≤ statutory` is possible at all.

*Worked case — GULF Q2/2026.* Reported core profit THB 12,332m, described in
the same release alongside KBANK dividend income of THB 2,842m and a THB
1,928m gain on divesting the Pak Lay hydro stake. Statutory net profit was THB
12,446m. Were those two items *outside* core profit, statutory would have to
be at least 12,332 + 2,842 + 1,928 = 17,102m. It is not — so both sit
**inside** the headline, and 39% of "core profit" is a dividend receipt plus a
disposal gain. The reported +74% YoY becomes roughly +6% to +30% once the base
period is put on the same footing.

**Status and consequence.**
- `RECONCILED` — every item accounted for; the adjusted figure may be used.
- `PARTIALLY_RECONCILED` — a residual remains; state its size and direction.
- `UNRECONCILED` — mark `UNRESOLVED`. The adjusted figure **may not** be used
  as a growth base or as the denominator of a ratio downstream. Use statutory
  profit and say why.

Record the outcome in `metric_comparability.adjusted_profit_reconciliation`.

**The failure mode this exists to stop:** repeating a company's own growth rate
for a measure the company itself defines, where the definition quietly absorbs
non-operating income. It costs one subtraction and it is the cheapest check in
Layer 1.

## Demand-evidence basis
When channel inventory or intermediary stocking is material, state whether the observable KPI is `SELL_IN`, `SELL_THROUGH`, `USAGE`, `BOOKINGS`, `GMV`, or `OTHER/UNRESOLVED`. Do not translate sell-in growth into end-demand growth without inventory/returns or other corroborating evidence.

## Failure modes
- Treating a member-definition change as organic customer growth.
- Comparing franchise revenue under different monetization models as if economics were unchanged.
- Using post-acquisition revenue growth as organic share gain.

## Handoff
Layer 1 owns trend comparability. Layer 2 owns the economic interpretation once comparable growth drivers are identified.
