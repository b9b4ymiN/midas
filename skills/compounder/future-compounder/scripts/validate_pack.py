#!/usr/bin/env python3
"""Validate a Future Compounder handoff pack against the pipeline contract.

`references/pipeline-contract.md` specifies required fields for six packs in
detail. Until this existed nothing checked any of them: packs were carried in
working memory between layers, so a field could go missing without anything
noticing. On a long run that is where drift starts.

Usage
-----
    python scripts/validate_pack.py run/GULF-2026-08-21/market_growth_pack.json
    python scripts/validate_pack.py run/GULF-2026-08-21/          # whole run
    python scripts/validate_pack.py run/GULF-2026-08-21/ --stage economic_engine_pack

Exit code 0 = the pack may be handed downstream; 1 = it may not.

stdlib only, no install.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Tuple

SCHEMA_VERSION = "future-compounder-v2.2"

# Order matters: a pack may only be validated once its predecessors exist.
PIPELINE: List[str] = [
    "business_identity_pack",
    "market_growth_pack",
    "economic_engine_pack",
    "reinvestment_runway_pack",
    "compounder_thesis_pack",
]

REQUIRED: Dict[str, List[str]] = {
    "business_identity_pack": [
        "product_definition", "current_economic_business", "customer_jobs",
        "core_capabilities", "strategic_direction", "market_scope_portfolio",
        "identity_transition", "scope_stress_test", "structural_analogues",
        "main_alternative_frame", "scope_confidence", "framing_risks",
        "critical_unknowns", "disconfirming_evidence", "evidence_ledger",
    ],
    "market_growth_pack": [
        "scope_frame_used", "scope_challenges", "metric_comparability",
        "demand_evidence_basis", "demand_category_evolution",
        "industry_profit_pool", "competitive_system", "growth_decomposition",
        "customer_channel_incrementality", "expansion_incrementality",
        "international_replication", "management_growth_execution",
        "evidence_trajectory", "external_growth_runway", "counter_evidence",
        "evidence_ledger", "data_gaps", "unresolved_questions",
    ],
    "economic_engine_pack": [
        "company_context", "business_model", "economic_units", "unit_economics",
        "micro_to_corporate_bridge", "economic_drivers", "growth_architecture",
        "current_return_structure", "intangible_capital", "scale_economics",
        "per_share_economics", "economic_inflections", "evidence_ledger",
        "data_gaps", "unresolved_questions",
    ],
    "reinvestment_runway_pack": [
        "historical_reinvestment", "incremental_return", "capital_allocation",
        "acquisition_economics", "reinvestment_capacity", "opportunity_set",
        "runway", "duration", "moat_outcomes", "capital_constraints",
        "financial_resilience", "emerging_indicators", "evidence_maturity",
        "evidence_ledger", "counter_evidence", "data_gaps",
    ],
    "compounder_thesis_pack": [
        "external_growth_view", "category_profit_pool_view",
        "competitive_share_view", "growth_decomposition_view",
        "channel_international_view", "growth_execution_view",
        "compounding_engine", "return_view", "reinvestment_view",
        "duration_view", "per_share_view", "scale_economics_view",
        "financial_resilience_view", "base_rate_context", "evidence_ladder",
        "reverse_reality_check", "supporting_evidence", "counter_evidence",
        "critical_unknowns", "kill_conditions", "compounding_potential",
        "evidence_maturity", "confidence", "evidence_ledger",
    ],
}

# Fields required only when a trigger fires, checked against the pack itself.
CONDITIONAL: Dict[str, List[Tuple[str, List[str], str]]] = {
    "market_growth_pack": [(
        "metric_comparability.adjusted_profit_reconciliation",
        ["adjusted_profit_reconciliation"],
        "the company promotes a profit measure of its own definition",
    )],
    "economic_engine_pack": [(
        "associate/holding trigger",
        ["look_through_earnings", "associate_cash_bridge", "return_bases"],
        "associate profit >25% of net profit or long-term investments >30% of assets",
    )],
}

VALID_STATUS = {"RESOLVED", "PARTIALLY_RESOLVED", "UNRESOLVED", "NOT_APPLICABLE"}

VERDICTS = {
    "compounding_potential": {"Exceptional", "Strong", "Moderate", "Weak", "Broken"},
    "evidence_maturity": {"Early", "Developing", "Established", "Deep"},
    "confidence": {"Low", "Medium", "High"},
}


def _empty(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip() == ""
    if isinstance(v, (list, dict, tuple, set)):
        return len(v) == 0
    return False


def validate(pack_name: str, pack: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Return (errors, warnings)."""
    errors: List[str] = []
    warns: List[str] = []

    required = REQUIRED.get(pack_name)
    if required is None:
        return [f"unknown pack '{pack_name}' — not in the contract"], []

    missing = [f for f in required if f not in pack]
    empty = [f for f in required if f in pack and _empty(pack[f])]
    if missing:
        errors.append(f"missing required field(s): {', '.join(sorted(missing))}")
    if empty:
        errors.append(
            f"present but empty: {', '.join(sorted(empty))} — an unanswered field is "
            f"'UNRESOLVED' with a reason, never blank"
        )

    ver = pack.get("schema_version")
    if ver and ver != SCHEMA_VERSION:
        warns.append(f"schema_version is '{ver}', contract expects '{SCHEMA_VERSION}'")

    # Evidence ledger must grow, never be replaced.
    ledger = pack.get("evidence_ledger")
    if isinstance(ledger, list) and not ledger:
        errors.append("evidence_ledger is empty — it is appended across the run, not reset")

    # Conditional requirements.
    for label, fields, why in CONDITIONAL.get(pack_name, []):
        absent = [f for f in fields if f not in pack or _empty(pack[f])]
        if absent and len(absent) == len(fields):
            warns.append(
                f"{label}: {', '.join(fields)} absent. Required when {why}; "
                f"if it does not apply, state NOT_APPLICABLE explicitly rather "
                f"than omitting the field"
            )

    # Free-text status tokens must be from the contract's vocabulary.
    for field, value in pack.items():
        if isinstance(value, str) and value.strip().isupper() and "_" in value.strip():
            token = value.strip()
            if token not in VALID_STATUS and token not in {"SCOPE_CHALLENGE"}:
                warns.append(f"{field}: '{token}' is not a contract status value {sorted(VALID_STATUS)}")

    # The three verdicts must stay separate and use the contract's labels.
    if pack_name == "compounder_thesis_pack":
        for field, allowed in VERDICTS.items():
            v = pack.get(field)
            if isinstance(v, str) and v.strip() and v.strip() not in allowed:
                errors.append(f"{field}='{v}' is not one of {sorted(allowed)}")
        if any(k in pack for k in ("overall_score", "total_score", "composite_score")):
            errors.append(
                "a combined score is present — potential, evidence maturity and "
                "confidence are reported separately and never collapsed"
            )

    return errors, warns


def load(path: str) -> Tuple[str, Dict[str, Any]]:
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    name = os.path.splitext(os.path.basename(path))[0]
    # Allow either a bare pack or {"<pack_name>": {...}}
    if name not in REQUIRED and len(doc) == 1:
        only = next(iter(doc))
        if only in REQUIRED:
            return only, doc[only]
    return name, doc


def run_dir(path: str, stage: str | None) -> int:
    found = {}
    for fn in sorted(os.listdir(path)):
        if fn.endswith(".json"):
            name = os.path.splitext(fn)[0]
            if name in REQUIRED:
                found[name] = os.path.join(path, fn)

    target = PIPELINE if stage is None else PIPELINE[: PIPELINE.index(stage) + 1]
    rc = 0
    for pack_name in target:
        if pack_name not in found:
            print(f"[MISSING] {pack_name}: no file in {path}")
            print(f"           downstream layers may not run without it")
            rc = 1
            continue
        rc |= report(found[pack_name])
    return rc


def report(path: str) -> int:
    try:
        name, pack = load(path)
    except (OSError, json.JSONDecodeError) as e:
        print(f"[ERROR]   {path}: {type(e).__name__}: {e}")
        return 1
    errors, warns = validate(name, pack)
    if errors:
        print(f"[FAIL]    {name}")
        for e in errors:
            print(f"           - {e}")
    else:
        print(f"[OK]      {name}  ({len(REQUIRED[name])} required fields present)")
    for w in warns:
        print(f"           ! {w}")
    return 1 if errors else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path", help="a pack .json, or a run directory")
    ap.add_argument("--stage", choices=PIPELINE,
                    help="validate the pipeline only up to this pack")
    args = ap.parse_args()

    if os.path.isdir(args.path):
        rc = run_dir(args.path, args.stage)
    else:
        rc = report(args.path)

    print()
    print("PASS — pack(s) may be handed downstream" if rc == 0
          else "FAIL — resolve the above before the next layer runs")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
