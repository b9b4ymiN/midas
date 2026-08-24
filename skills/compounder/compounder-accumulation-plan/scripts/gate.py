#!/usr/bin/env python3
"""Decide whether a compounding verdict has earned an accumulation plan.

The gate is mechanical on purpose. A judgement call here would drift, and it would
drift in the permissive direction — every company looks worth a plan once you have
spent a day reading about it. Same pack in, same decision out.

It reads only `compounder_thesis_pack`. It never looks at price: a company that did
not clear the compounding work does not get a price opinion, and one that did gets
the plan its own weakest leg allows.

    python gate.py run/CPRT-2026-08-24/compounder_thesis_pack.json

Rules and their reasoning: ../references/gate.md
Contract: ../../future-compounder/references/pipeline-contract.md

Research and educational output only. Not financial advice.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date

PASSING_POTENTIAL = {"Exceptional", "Strong", "Moderate"}
ABOVE_MODERATE = {"Exceptional", "Strong"}
BLOCKING_CLASS = "Not a Compounder"
SHALLOW_EVIDENCE = {"Early", "Developing"}
EMERGING_CLASS = "Emerging Candidate"
NARROW_RUNWAY_CLASS = "Great Business, Narrow Runway"

REQUIRED_FIELDS = (
    "compounding_potential",
    "compounder_class",
    "evidence_maturity",
    "leg_ratings",
    "review_schedule",
)


def _unwrap(pack):
    if isinstance(pack, dict) and len(pack) == 1:
        only = next(iter(pack))
        if only == "compounder_thesis_pack" and isinstance(pack[only], dict):
            return pack[only]
    return pack


def _as_date(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def evaluate_gate(thesis_pack: dict, run_date: str) -> dict:
    """Return the gate decision for one thesis pack.

    `gate` is PASSED or BLOCKED. A pass carries `plan_archetype`; a block carries
    `unblock_conditions` naming what would have to change, so the report can tell a
    reader what it is waiting for rather than just closing.
    """
    pack = _unwrap(thesis_pack) or {}
    reasons: list[str] = []
    unblock: list[str] = []

    missing = [f for f in REQUIRED_FIELDS if not pack.get(f)]
    if missing:
        reasons.append(
            f"the thesis pack is missing {', '.join(missing)} — a gate cannot be "
            f"evaluated on a partial verdict"
        )
        unblock.append(f"complete the thesis pack: {', '.join(missing)}")
        return _result("BLOCKED", reasons, None, unblock, run_date, pack)

    potential = str(pack.get("compounding_potential", "")).strip()
    klass = str(pack.get("compounder_class", "")).strip()
    maturity = str(pack.get("evidence_maturity", "")).strip()
    legs = pack.get("leg_ratings") or {}

    if potential not in PASSING_POTENTIAL:
        reasons.append(
            f"compounding potential is {potential or 'UNRESOLVED'} — below the "
            f"Moderate floor a plan would be written against a business the work "
            f"did not clear"
        )
        unblock.append("compounding potential reaching Moderate on new evidence")

    if klass == BLOCKING_CLASS:
        reasons.append(
            f"the categorical reading is {BLOCKING_CLASS} — whatever the label says, "
            f"this is not a business to accumulate"
        )
        unblock.append(
            f"the categorical reading moving off {BLOCKING_CLASS}, which takes "
            f"evidence about the engine, not a better price"
        )

    broken = sorted(k for k, v in legs.items() if str(v).strip() == "Broken")
    if broken:
        reasons.append(
            f"{', '.join(broken)} rated Broken — one broken leg is enough, because a "
            f"plan cannot compound through it"
        )
        unblock.extend(f"{leg} rated above Broken" for leg in broken)

    if potential in ABOVE_MODERATE:
        unresolved = sorted(k for k, v in legs.items() if str(v).strip() == "UNRESOLVED")
        if unresolved:
            reasons.append(
                f"potential is {potential} while {', '.join(unresolved)} is still "
                f"UNRESOLVED — a verdict above Moderate may not rest on an unread leg"
            )
            unblock.extend(f"{leg} resolved to a rating" for leg in unresolved)

    expires = _as_date((pack.get("review_schedule") or {}).get("expires_on"))
    today = _as_date(run_date)
    if expires and today and expires < today:
        reasons.append(
            f"the verdict expired on {expires.isoformat()} — past its expiry it may be "
            f"read as history, but it may not carry a decision"
        )
        unblock.append("the compounding analysis re-run so the verdict is current")

    if reasons:
        return _result("BLOCKED", reasons, None, unblock, run_date, pack)

    if klass == NARROW_RUNWAY_CLASS:
        archetype = "narrow-runway"
        why = (f"{NARROW_RUNWAY_CLASS}: the economics are excellent and the business "
               f"cannot absorb capital at those returns, so the entry price carries "
               f"the return rather than the compounding")
    elif maturity in SHALLOW_EVIDENCE or klass == EMERGING_CLASS:
        archetype = "emerging-starter"
        why = (f"evidence maturity is {maturity} and the reading is {klass}: the "
               f"business may be excellent, but not enough is known yet to size a "
               f"position on it")
    else:
        archetype = "proven-compounder"
        binding = pack.get("binding_leg") or "UNRESOLVED"
        why = (f"{klass} with {maturity} evidence; the binding leg is {binding}, and "
               f"it constrains the rate rather than blocking the plan: the return "
               f"comes from the business, so time held matters more than the entry "
               f"price")

    return _result("PASSED", [why], archetype, [], run_date, pack)


def _result(gate, reasons, archetype, unblock, run_date, pack):
    return {
        "gate": gate,
        "gate_reason": reasons,
        "plan_archetype": archetype,
        "unblock_conditions": unblock,
        "evaluated_on": run_date,
        "thesis_as_of": (pack.get("review_schedule") or {}).get("as_of", "UNRESOLVED"),
        "binding_leg": pack.get("binding_leg", "UNRESOLVED"),
        "verdict_read": {
            "compounding_potential": pack.get("compounding_potential", "UNRESOLVED"),
            "potential_qualifier": pack.get("potential_qualifier", ""),
            "compounder_class": pack.get("compounder_class", "UNRESOLVED"),
            "evidence_maturity": pack.get("evidence_maturity", "UNRESOLVED"),
            "confidence": pack.get("confidence", "UNRESOLVED"),
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("thesis_pack", help="path to compounder_thesis_pack.json")
    ap.add_argument("--run-date", default=date.today().isoformat())
    args = ap.parse_args(argv)

    with open(args.thesis_pack, encoding="utf-8") as fh:
        pack = json.load(fh)

    result = evaluate_gate(pack, args.run_date)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["gate"] == "PASSED" else 2


if __name__ == "__main__":
    sys.exit(main())
