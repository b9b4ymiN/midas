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

## Demand-evidence basis
When channel inventory or intermediary stocking is material, state whether the observable KPI is `SELL_IN`, `SELL_THROUGH`, `USAGE`, `BOOKINGS`, `GMV`, or `OTHER/UNRESOLVED`. Do not translate sell-in growth into end-demand growth without inventory/returns or other corroborating evidence.

## Failure modes
- Treating a member-definition change as organic customer growth.
- Comparing franchise revenue under different monetization models as if economics were unchanged.
- Using post-acquisition revenue growth as organic share gain.

## Handoff
Layer 1 owns trend comparability. Layer 2 owns the economic interpretation once comparable growth drivers are identified.
