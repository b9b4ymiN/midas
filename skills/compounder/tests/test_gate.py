"""The accumulation gate must decide the same way every time it sees the same pack.

The gate is what keeps price out of a run that has not earned it: a company the
compounding work did not clear never reaches a plan, and the report closes at the
verdict instead. That decision is mechanical on purpose — a judgement call here
would drift, and the drift would always be in the permissive direction.

Fixtures are inline because `.data/` is gitignored; the CPRT case mirrors the real
2026-08-21 run and is also checked against that run's pack when it is on disk.
"""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "compounder-accumulation-plan" / "scripts" / "gate.py"

spec = importlib.util.spec_from_file_location("compounder_gate", GATE_PATH)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

RUN_DATE = "2026-08-24"


def pack(**overrides):
    base = {
        "compounding_potential": "Strong",
        "potential_qualifier": "",
        "compounder_class": "Proven Compounder",
        "evidence_maturity": "Deep",
        "confidence": "High",
        "binding_leg": "duration",
        "leg_ratings": {
            "incremental_return": "Strong",
            "reinvestment_capacity": "Strong",
            "duration": "Strong",
            "per_share_translation": "Strong",
            "financial_resilience": "Strong",
            "capital_allocation": "VALUE_CREATING",
        },
        "review_schedule": {
            "as_of": "2026-08-21",
            "next_review": "2027-02-15",
            "expires_on": "2027-08-21",
        },
    }
    base.update(overrides)
    return base


# --- the pass paths -------------------------------------------------------

def test_cprt_passes_as_narrow_runway():
    """CPRT's real verdict: Moderate potential, exceptional returns, no runway.

    It passes — the business is genuinely interesting — but the plan it earns is
    the one where the entry price carries the return, not the one where time does.
    """
    result = gate.evaluate_gate(
        pack(
            compounding_potential="Moderate",
            potential_qualifier="runway-capped; return leg is Exceptional",
            compounder_class="Great Business, Narrow Runway",
            evidence_maturity="Deep",
            binding_leg="reinvestment_capacity",
            leg_ratings={
                "incremental_return": "Exceptional",
                "reinvestment_capacity": "Moderate",
                "duration": "Strong",
                "per_share_translation": "Strong",
                "financial_resilience": "Exceptional",
                "capital_allocation": "VALUE_CREATING",
            },
        ),
        run_date=RUN_DATE,
    )
    assert result["gate"] == "PASSED"
    assert result["plan_archetype"] == "narrow-runway"


def test_shallow_evidence_passes_as_emerging_starter():
    result = gate.evaluate_gate(
        pack(
            compounding_potential="Strong",
            compounder_class="Emerging Candidate",
            evidence_maturity="Developing",
        ),
        run_date=RUN_DATE,
    )
    assert result["gate"] == "PASSED"
    assert result["plan_archetype"] == "emerging-starter"


def test_clean_strong_pack_passes_as_proven_compounder():
    result = gate.evaluate_gate(pack(), run_date=RUN_DATE)
    assert result["gate"] == "PASSED"
    assert result["plan_archetype"] == "proven-compounder"


def test_narrow_runway_wins_over_shallow_evidence():
    """Both archetype conditions hold; the runway is the tighter constraint."""
    result = gate.evaluate_gate(
        pack(
            compounding_potential="Moderate",
            compounder_class="Great Business, Narrow Runway",
            evidence_maturity="Early",
        ),
        run_date=RUN_DATE,
    )
    assert result["plan_archetype"] == "narrow-runway"


# --- the blocked paths ----------------------------------------------------

def test_not_a_compounder_is_blocked():
    result = gate.evaluate_gate(
        pack(compounding_potential="Weak", compounder_class="Not a Compounder"),
        run_date=RUN_DATE,
    )
    assert result["gate"] == "BLOCKED"
    assert result["plan_archetype"] is None
    assert any("Not a Compounder" in r for r in result["gate_reason"])


def test_broken_leg_is_blocked_even_with_strong_potential():
    legs = pack()["leg_ratings"] | {"financial_resilience": "Broken"}
    result = gate.evaluate_gate(pack(leg_ratings=legs), run_date=RUN_DATE)
    assert result["gate"] == "BLOCKED"
    assert any("financial_resilience" in r for r in result["gate_reason"])


def test_unresolved_leg_blocks_above_moderate_only():
    legs = pack()["leg_ratings"] | {"duration": "UNRESOLVED"}
    above = gate.evaluate_gate(
        pack(compounding_potential="Strong", leg_ratings=legs), run_date=RUN_DATE
    )
    assert above["gate"] == "BLOCKED"

    at_moderate = gate.evaluate_gate(
        pack(compounding_potential="Moderate", leg_ratings=legs), run_date=RUN_DATE
    )
    assert at_moderate["gate"] == "PASSED"


def test_expired_verdict_is_blocked():
    result = gate.evaluate_gate(
        pack(review_schedule={"as_of": "2024-01-01", "next_review": "2025-01-01",
                              "expires_on": "2025-06-30"}),
        run_date=RUN_DATE,
    )
    assert result["gate"] == "BLOCKED"
    assert any("expire" in r.lower() for r in result["gate_reason"])


def test_blocked_result_says_what_would_unblock_it():
    result = gate.evaluate_gate(
        pack(compounding_potential="Weak", compounder_class="Not a Compounder"),
        run_date=RUN_DATE,
    )
    assert result["unblock_conditions"], "a blocked gate must name its way out"


# --- shape --------------------------------------------------------------

def test_result_carries_every_contract_field():
    result = gate.evaluate_gate(pack(), run_date=RUN_DATE)
    for field in ("gate", "gate_reason", "plan_archetype", "unblock_conditions",
                  "evaluated_on", "thesis_as_of"):
        assert field in result


def test_missing_fields_block_rather_than_guess():
    result = gate.evaluate_gate({"compounding_potential": "Strong"}, run_date=RUN_DATE)
    assert result["gate"] == "BLOCKED"


@pytest.mark.skipif(
    not (Path(__file__).resolve().parents[3] / ".data/runs/CPRT-2026-08-21"
         / "compounder_thesis_pack.json").exists(),
    reason="local CPRT run data not present",
)
def test_real_cprt_run_still_reads_as_narrow_runway():
    path = (Path(__file__).resolve().parents[3] / ".data/runs/CPRT-2026-08-21"
            / "compounder_thesis_pack.json")
    real = json.loads(path.read_text(encoding="utf-8"))
    result = gate.evaluate_gate(real, run_date=RUN_DATE)
    assert result["gate"] == "PASSED"
    assert result["plan_archetype"] == "narrow-runway"
