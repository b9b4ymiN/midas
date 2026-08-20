# Market Scope Classification

Classify every economic arena independently. Market size does not affect evidence class.

## PROVEN
Required evidence:
- real customer adoption/usage;
- meaningful revenue or economically equivalent monetization;
- evidence of unit/corporate economics or profit capture;
- operating presence sufficient to analyze competitors/position.

## EMERGING
Required evidence:
- real management commitment (capital, team, capacity, partnerships, or acquisitions);
- customer/operating traction (deployments, recurring users, contracts, repeat demand);
- economics may still be immature or not separately disclosed.

## OPTION
Required evidence:
- credible transferable capability;
- intentional action such as R&D, pilot, partnership, dedicated team, IP, or limited capex;
- commercial/economic evidence is not yet sufficient for EMERGING.

## NARRATIVE
Typical evidence only:
- strategic language;
- consultant TAM;
- thematic association;
- technical possibility without committed action/customer proof.

## Upgrade rule

Every arena must state:
- current classification;
- evidence supporting it;
- why it is not promoted further;
- specific evidence that would upgrade/downgrade it.

**Never combine OPTION or NARRATIVE market size with core/proven TAM downstream.**

## Arena relationship to the core

Evidence maturity (PROVEN/EMERGING/OPTION/NARRATIVE) answers **how proven** an arena is. Separately classify **how it relates economically to the core**:

- **CORE_EXTENSION** — same core economic engine extended to a new product/geography/customer.
- **CORE_COMPLEMENT** — increases adoption, retention, conversion, utilization, or economics of the core but is not yet an independent profit pool.
- **ADJACENT_STANDALONE** — has a distinct customer/job and can support independent economics.
- **ENABLING_INFRASTRUCTURE** — capability/infrastructure used across arenas; do not count its activity again as a separate TAM unless external monetization exists.
- **UNRESOLVED** — relationship cannot yet be established.

Every arena should carry both `evidence_class` and `arena_relationship`. This prevents double counting one economic mechanism as multiple independent growth markets.
