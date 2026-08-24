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
import datetime as _dt
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
    # Post-verdict layers. They are the only place in a run where price is read,
    # and they may never revise anything above them.
    "stage_pack",
    "accumulation_pack",
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
        "life_cycle_stage",
        "current_return_structure", "intangible_capital", "scale_economics",
        "per_share_economics", "economic_inflections", "evidence_ledger",
        "data_gaps", "unresolved_questions",
    ],
    "reinvestment_runway_pack": [
        "historical_reinvestment", "mandatory_measures",
        "incremental_return", "capital_allocation",
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
        "critical_unknowns", "kill_conditions", "upgrade_conditions",
        "review_schedule",
        "leg_ratings", "binding_leg", "hurdle_used", "durable_growth",
        "compounding_potential", "potential_qualifier", "compounder_class",
        "evidence_maturity", "confidence", "evidence_ledger",
    ],
    "stage_pack": [
        "as_of", "price_context", "monthly_read", "weekly_read", "stage_conflict",
        "business_stage", "stage_alignment", "chart_assets", "data_quality",
        "evidence_ledger",
    ],
    # A blocked gate is a valid outcome, so only the fields both outcomes share are
    # required here; the rest are demanded per-outcome in validate().
    "accumulation_pack": [
        "gate", "gate_reason", "plan_review", "not_a_recommendation",
        "evidence_ledger",
    ],
}

# Fields a passing accumulation pack must carry on top of the shared ones.
ACCUMULATION_PASSED_FIELDS: List[str] = [
    "plan_archetype", "required_return_assumption", "price_implied_expectations",
    "expectation_gap", "expected_return_paths", "accumulation_bands", "staging",
    "position_bounds", "add_rules", "pause_rules", "exit_rules",
]

CHART_STAGES = {"STAGE_1", "STAGE_2", "STAGE_3", "STAGE_4", "TRANSITIONAL", "UNRESOLVED"}
STAGE_ALIGNMENTS = {
    "MARKET_HAS_NOT_PRICED_IT", "MOVING_TOGETHER", "LATE_AND_EXTENDED",
    "MARKET_SEES_DAMAGE_FIRST", "UNRESOLVED",
}
PLAN_ARCHETYPES = {"proven-compounder", "emerging-starter", "narrow-runway"}
EXPECTATION_GAP_STATES = {
    "PRICE_ASKS_LESS", "PRICE_ASKS_ABOUT_THE_SAME", "PRICE_ASKS_MORE", "UNRESOLVED",
}
# Words that mean a valuation or an instruction has leaked into a layer that may
# produce neither. Checked against the serialized pack, not against prose files.
FORBIDDEN_IN_POST_VERDICT = ("fair_value", "target_price", "price_target")

# Fields required only when a trigger fires, checked against the pack itself.
# Field names may be dotted: the contract nests the reconciliation inside
# metric_comparability, so a top-level-only lookup reports it missing when it
# is present and correct.
CONDITIONAL: Dict[str, List[Tuple[str, List[str], str]]] = {
    "market_growth_pack": [(
        "adjusted profit reconciliation",
        ["metric_comparability.adjusted_profit_reconciliation"],
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

# Potential ranks low to high; used for the UNRESOLVED cap in rule 3 of the rubric.
POTENTIAL_RANK = {"Broken": 0, "Weak": 1, "Moderate": 2, "Strong": 3, "Exceptional": 4}

# Per-leg ratings. Five legs share the Potential vocabulary; capital allocation
# keeps the vocabulary capital-allocation.md already defines for it.
LEG_VALUES = set(VERDICTS["compounding_potential"]) | {"UNRESOLVED"}
LEG_RATINGS: Dict[str, set] = {
    "incremental_return": LEG_VALUES,
    "reinvestment_capacity": LEG_VALUES,
    "duration": LEG_VALUES,
    "per_share_translation": LEG_VALUES,
    "financial_resilience": LEG_VALUES,
    "capital_allocation": {
        "VALUE_CREATING", "MIXED", "VALUE_DESTRUCTIVE", "UNRESOLVED",
    },
}

MEASURE_PATHS = {"standard", "emerging_bridge", "sector_specific"}
REVERSE_STATES = {"PLAUSIBLE", "STRETCHED", "IMPLAUSIBLE", "UNRESOLVED"}
MIN_WINDOW_YEARS = 3

LIFE_CYCLE_STAGES = {
    "Introduction", "Growth", "Mature", "Shake-out", "Decline", "UNRESOLVED",
}

COMPOUNDER_CLASSES = {
    "Proven Compounder", "Emerging Candidate",
    "Great Business, Narrow Runway", "Not a Compounder",
}

# Review cadence, borrowed from credit-rating surveillance: a scheduled review at
# least annually whether or not there is news, an outlook horizon of at most two
# years, and event-driven watches resolved inside about 90 days.
MAX_REVIEW_DAYS = 366
MAX_EXPIRY_DAYS = 731
MAX_WATCH_DAYS = 90


def _dig(pack: Dict[str, Any], dotted: str) -> Any:
    """Resolve a possibly-dotted field path. Returns None when any hop misses."""
    cur: Any = pack
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _empty(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip() == ""
    if isinstance(v, (list, dict, tuple, set)):
        return len(v) == 0
    return False


def _date(value: Any) -> _dt.date | None:
    """Parse an ISO YYYY-MM-DD date. Returns None for anything else."""
    if not isinstance(value, str):
        return None
    try:
        return _dt.date.fromisoformat(value.strip())
    except ValueError:
        return None


def check_review_schedule(pack: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """A verdict with no review date claims to be true forever.

    Kill and upgrade conditions say what would change the verdict; without a
    date nothing says when to look, so nobody ever does. The cadence rules come
    from rating surveillance — see references/pipeline-contract.md.
    """
    errors: List[str] = []
    warns: List[str] = []

    rs = pack.get("review_schedule")
    if rs is None:
        return errors, warns  # absence is already reported by the required check
    if not isinstance(rs, dict):
        return ["review_schedule must be an object, not a bare date or sentence"], []

    as_of = _date(rs.get("as_of"))
    nxt = _date(rs.get("next_review"))
    exp = _date(rs.get("expires_on"))

    for field, parsed in (("as_of", as_of), ("next_review", nxt), ("expires_on", exp)):
        if parsed is None:
            errors.append(
                f"review_schedule.{field}={rs.get(field)!r} is not an ISO "
                f"YYYY-MM-DD date"
            )

    if as_of and nxt:
        delta = (nxt - as_of).days
        if delta <= 0:
            errors.append(
                f"review_schedule.next_review is not after as_of "
                f"({rs.get('next_review')} vs {rs.get('as_of')})"
            )
        elif delta > MAX_REVIEW_DAYS:
            errors.append(
                f"review_schedule.next_review is {delta} days after as_of — the "
                f"floor is a review at least annually ({MAX_REVIEW_DAYS} days), "
                f"whether or not there is news"
            )

    if as_of and exp:
        delta = (exp - as_of).days
        if delta > MAX_EXPIRY_DAYS:
            errors.append(
                f"review_schedule.expires_on is {delta} days after as_of — a "
                f"verdict may not outlive a two-year outlook horizon "
                f"({MAX_EXPIRY_DAYS} days)"
            )
    if nxt and exp and exp < nxt:
        errors.append(
            "review_schedule.expires_on falls before next_review — the verdict "
            "would be stale before it is next looked at"
        )

    for field, why in (
        ("next_review_event", "a calendar date with no filing behind it is a guess"),
        ("settles", "a scheduled review that settles no condition is a diary entry"),
        ("cadence_basis", "the interval must be justified by the fastest-moving "
                          "evidence in the binding leg"),
    ):
        if _empty(rs.get(field)):
            errors.append(f"review_schedule.{field} is missing — {why}")

    triggers = rs.get("watch_triggers")
    if _empty(triggers):
        errors.append(
            "review_schedule.watch_triggers is empty — the scheduled review is "
            "the backstop, not the whole obligation; name at least one event "
            "that would force an earlier look"
        )
    elif not isinstance(triggers, list):
        errors.append("review_schedule.watch_triggers must be a list of entries")
    else:
        for i, t in enumerate(triggers):
            if not isinstance(t, dict):
                errors.append(
                    f"review_schedule.watch_triggers[{i}] is free text — it needs "
                    f"what it watches, what is observable, and a closing window"
                )
                continue
            for field in ("watches", "observable"):
                if _empty(t.get(field)):
                    errors.append(
                        f"review_schedule.watch_triggers[{i}].{field} is missing"
                    )
            days = t.get("resolve_within_days")
            if not isinstance(days, (int, float)):
                errors.append(
                    f"review_schedule.watch_triggers[{i}].resolve_within_days is "
                    f"missing — an open question with no closing date is how a "
                    f"thesis drifts"
                )
            elif days > MAX_WATCH_DAYS:
                warns.append(
                    f"review_schedule.watch_triggers[{i}].resolve_within_days="
                    f"{days} exceeds the {MAX_WATCH_DAYS}-day watch convention"
                )

    return errors, warns


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

    if pack_name == "reinvestment_runway_pack":
        mm = pack.get("mandatory_measures")
        if mm is not None and not isinstance(mm, dict):
            errors.append("mandatory_measures must be an object")
        elif isinstance(mm, dict):
            path = mm.get("path")
            if not isinstance(path, str) or path.strip() not in MEASURE_PATHS:
                errors.append(
                    f"mandatory_measures.path='{path}' is not one of "
                    f"{sorted(MEASURE_PATHS)}"
                )
                path = None
            else:
                path = path.strip()

            basis = mm.get("basis")
            if _empty(basis):
                errors.append(
                    "mandatory_measures.basis is empty — the denominator must be "
                    "stated so the figure can be checked"
                )
            elif isinstance(basis, str) and "free cash flow" in basis.lower():
                errors.append(
                    "mandatory_measures.basis names free cash flow — it is already "
                    "net of the capital spend being measured and may never be the "
                    "denominator of the reinvestment rate"
                )

            if path == "standard":
                yrs = mm.get("window_years")
                if not isinstance(yrs, (int, float)):
                    errors.append(
                        "mandatory_measures.window_years is required on the "
                        "standard path"
                    )
                elif yrs < MIN_WINDOW_YEARS:
                    errors.append(
                        f"mandatory_measures.window_years={yrs} is below the "
                        f"{MIN_WINDOW_YEARS}-year floor. If the company has no "
                        f"longer history, use path 'emerging_bridge' — a short "
                        f"record lowers Evidence Maturity, never Potential"
                    )
                rr = mm.get("reinvestment_rate")
                if not isinstance(rr, dict):
                    errors.append(
                        "mandatory_measures.reinvestment_rate must carry both a "
                        "cumulative figure and an annual series"
                    )
                elif _empty(rr.get("annual")):
                    errors.append(
                        "mandatory_measures.reinvestment_rate.annual is empty — a "
                        "cumulative figure without its annual series conceals the "
                        "trend, which is usually the more decision-relevant number"
                    )

    if pack_name == "economic_engine_pack":
        lc = pack.get("life_cycle_stage")
        if isinstance(lc, dict):
            st = lc.get("stage")
            if isinstance(st, str) and st.strip() and st.strip() not in LIFE_CYCLE_STAGES:
                errors.append(
                    f"life_cycle_stage.stage='{st}' is not one of "
                    f"{sorted(LIFE_CYCLE_STAGES)}"
                )
            raw = lc.get("raw_stage")
            if (isinstance(raw, str) and isinstance(st, str)
                    and raw.strip() and st.strip() and raw.strip() != st.strip()
                    and _empty(lc.get("divergence_note"))):
                errors.append(
                    f"life_cycle_stage: adjusted '{st}' and raw '{raw}' differ but "
                    f"divergence_note is empty — the difference is a finding about "
                    f"treasury activity, not a rounding detail"
                )

    ver = pack.get("schema_version")
    if ver and ver != SCHEMA_VERSION:
        warns.append(f"schema_version is '{ver}', contract expects '{SCHEMA_VERSION}'")

    if pack_name == "stage_pack":
        for side in ("monthly_read", "weekly_read"):
            read = pack.get(side)
            if isinstance(read, dict) and read.get("status") == "READ":
                stage = read.get("stage")
                if stage not in CHART_STAGES:
                    errors.append(f"{side}.stage='{stage}' is not one of {sorted(CHART_STAGES)}")
                if _empty(read.get("stage_since")):
                    errors.append(
                        f"{side}.stage_since is empty — a stage without a start date "
                        f"is UNRESOLVED, not a stage"
                    )
                if _empty(read.get("invalidates_if")):
                    errors.append(
                        f"{side}.invalidates_if is empty — a read nobody can check "
                        f"later is not evidence"
                    )
        alignment = pack.get("stage_alignment")
        if isinstance(alignment, dict):
            reading = alignment.get("reading")
            if reading not in STAGE_ALIGNMENTS:
                errors.append(
                    f"stage_alignment.reading='{reading}' is not one of "
                    f"{sorted(STAGE_ALIGNMENTS)}"
                )
        business = pack.get("business_stage")
        if isinstance(business, dict):
            st = business.get("adjusted")
            if isinstance(st, str) and st.strip() and st.strip() not in LIFE_CYCLE_STAGES:
                errors.append(
                    f"business_stage.adjusted='{st}' is not one of "
                    f"{sorted(LIFE_CYCLE_STAGES)}"
                )
        assets = pack.get("chart_assets")
        if isinstance(assets, list):
            for asset in assets:
                if not isinstance(asset, dict):
                    continue
                blob = str(asset.get("asset") or "")
                if 'src="http' in blob or blob.startswith("http"):
                    errors.append(
                        f"chart_assets[{asset.get('timeframe')}]: remote asset — the "
                        f"report must be self-contained"
                    )

    if pack_name == "accumulation_pack":
        gate = pack.get("gate")
        if gate not in {"PASSED", "BLOCKED"}:
            errors.append(f"gate='{gate}' must be PASSED or BLOCKED")
        elif gate == "PASSED":
            absent = [f for f in ACCUMULATION_PASSED_FIELDS if _empty(pack.get(f))]
            if absent:
                errors.append(
                    f"gate is PASSED but missing: {', '.join(sorted(absent))}"
                )
            archetype = pack.get("plan_archetype")
            if archetype not in PLAN_ARCHETYPES:
                errors.append(
                    f"plan_archetype='{archetype}' is not one of {sorted(PLAN_ARCHETYPES)}"
                )
            gap = pack.get("expectation_gap")
            if isinstance(gap, dict) and gap.get("direction") not in EXPECTATION_GAP_STATES:
                errors.append(
                    f"expectation_gap.direction='{gap.get('direction')}' is not one of "
                    f"{sorted(EXPECTATION_GAP_STATES)}"
                )
            pie = pack.get("price_implied_expectations")
            if isinstance(pie, dict) and _empty(pie.get("sensitivity")):
                errors.append(
                    "price_implied_expectations.sensitivity is empty — an implied "
                    "growth figure without its sensitivity band is a false precision"
                )
        else:
            if _empty(pack.get("unblock_conditions")):
                errors.append(
                    "gate is BLOCKED but unblock_conditions is empty — a blocked gate "
                    "must name its way out"
                )
            for field in ACCUMULATION_PASSED_FIELDS:
                if field in ("plan_archetype",) or _empty(pack.get(field)):
                    continue
                errors.append(
                    f"gate is BLOCKED but '{field}' is populated — a plan may not be "
                    f"written for a company that did not clear the gate"
                )

    if pack_name in ("stage_pack", "accumulation_pack"):
        blob = json.dumps(pack, ensure_ascii=False).lower()
        for token in FORBIDDEN_IN_POST_VERDICT:
            if token in blob:
                errors.append(
                    f"'{token}' appears in {pack_name} — the post-verdict layers "
                    f"produce no valuation"
                )

    # Evidence ledger must grow, never be replaced.
    ledger = pack.get("evidence_ledger")
    if isinstance(ledger, list) and not ledger:
        errors.append("evidence_ledger is empty — it is appended across the run, not reset")

    # Conditional requirements.
    for label, fields, why in CONDITIONAL.get(pack_name, []):
        absent = [f for f in fields if _empty(_dig(pack, f))]
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

        dg = pack.get("durable_growth")
        if isinstance(dg, dict):
            if _empty(dg.get("real")) and not isinstance(dg.get("real"), (int, float)):
                errors.append(
                    "durable_growth.real is missing — the band table is built on "
                    "real rates, so a nominal figure compared against it flatters "
                    "the company by the rate of inflation"
                )
            ib = dg.get("inflation_basis")
            if not isinstance(ib, dict) or _empty(ib.get("source")):
                errors.append(
                    "durable_growth.inflation_basis must name the rate used and "
                    "where it came from — the countries the company operates in, "
                    "revenue-weighted"
                )

        rrc = pack.get("reverse_reality_check")
        if isinstance(rrc, dict):
            for f, why in (
                ("required_cagr", "the rate the path demands is the point of the check"),
                ("horizon_years", "a multiple without a horizon is two different claims"),
                ("comparisons", "the required rate means nothing uncompared"),
            ):
                if _empty(rrc.get(f)):
                    errors.append(
                        f"reverse_reality_check.{f} is missing — {why}"
                    )
            st = rrc.get("state")
            if isinstance(st, str) and st.strip() and st.strip() not in REVERSE_STATES:
                errors.append(
                    f"reverse_reality_check.state='{st}' is not one of "
                    f"{sorted(REVERSE_STATES)}"
                )
        elif isinstance(rrc, str):
            warns.append(
                "reverse_reality_check is free text — the contract expects the "
                "required rate, the horizon and the three comparisons as fields, "
                "so a bare verdict word cannot stand in for them"
            )

        rs_errors, rs_warns = check_review_schedule(pack)
        errors.extend(rs_errors)
        warns.extend(rs_warns)

        cls = pack.get("compounder_class")
        if isinstance(cls, str) and cls.strip() and cls.strip() not in COMPOUNDER_CLASSES:
            errors.append(
                f"compounder_class='{cls}' is not one of {sorted(COMPOUNDER_CLASSES)}"
            )

        legs = pack.get("leg_ratings")
        if legs is not None and not isinstance(legs, dict):
            errors.append("leg_ratings must be an object keyed by leg name")
        elif isinstance(legs, dict):
            for leg, allowed in LEG_RATINGS.items():
                if leg not in legs:
                    errors.append(f"leg_ratings.{leg} is missing — every leg is rated")
                    continue
                v = legs[leg]
                if not isinstance(v, str) or v.strip() not in allowed:
                    errors.append(
                        f"leg_ratings.{leg}='{v}' is not one of {sorted(allowed)}"
                    )

            # Rubric rule 3: an unresolved thesis-critical leg caps Potential.
            unresolved = sorted(
                leg for leg, v in legs.items()
                if isinstance(v, str) and v.strip() == "UNRESOLVED"
            )
            potential = pack.get("compounding_potential")
            if unresolved and isinstance(potential, str):
                rank = POTENTIAL_RANK.get(potential.strip())
                if rank is not None and rank > POTENTIAL_RANK["Moderate"]:
                    errors.append(
                        f"compounding_potential='{potential}' while "
                        f"{', '.join(unresolved)} is UNRESOLVED — an unmeasured "
                        f"thesis-critical leg caps Potential at Moderate"
                    )

            # Rubric rule 2: the weakest leg governs, so binding_leg must name a
            # leg that is actually rated lowest. Naming a stronger leg misreports
            # what constrains the verdict — the emptiness of these fields is
            # already caught by the required-field check above.
            ranked = {
                leg: POTENTIAL_RANK[v.strip()] for leg, v in legs.items()
                if leg != "capital_allocation"
                and isinstance(v, str) and v.strip() in POTENTIAL_RANK
            }
            binding = pack.get("binding_leg")
            if ranked and isinstance(binding, str) and binding.strip():
                weakest = min(ranked.values())
                lowest = sorted(leg for leg, r in ranked.items() if r == weakest)
                if binding.strip() not in ranked:
                    warns.append(
                        f"binding_leg='{binding}' is not a rated leg "
                        f"{sorted(ranked)}"
                    )
                elif ranked[binding.strip()] > weakest:
                    errors.append(
                        f"binding_leg='{binding}' is rated above the weakest leg "
                        f"({', '.join(lowest)}) — the weakest leg governs"
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
    rc |= check_ledger_growth(found, target)
    return rc


def check_ledger_growth(found: Dict[str, str], target: List[str]) -> int:
    """The evidence ledger accumulates across layers; it may never shrink.

    A ledger that never grows is the other failure: the same entries copied into
    every pack satisfy a naive size check while losing which layer found what.
    """
    sizes: List[Tuple[str, int]] = []
    for pack_name in target:
        if pack_name not in found:
            continue
        try:
            _, pack = load(found[pack_name])
        except (OSError, json.JSONDecodeError):
            continue  # already reported by report()
        ledger = pack.get("evidence_ledger")
        if isinstance(ledger, list):
            sizes.append((pack_name, len(ledger)))

    rc = 0
    for (prev_name, prev_n), (name, n) in zip(sizes, sizes[1:]):
        if n < prev_n:
            print(f"[FAIL]    evidence_ledger shrank: {prev_name} had {prev_n} "
                  f"entries, {name} has {n}")
            print("           the ledger is appended across the run, never replaced")
            rc = 1

    if len(sizes) >= 3 and len({n for _, n in sizes}) == 1:
        print(f"[WARN]    evidence_ledger is {sizes[0][1]} entries in all "
              f"{len(sizes)} packs")
        print("           identical ledgers suggest one ledger copied to every pack; "
              "each layer should add what it found, and every entry carries "
              "origin_layer")
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
