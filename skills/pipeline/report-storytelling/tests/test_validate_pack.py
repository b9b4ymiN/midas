"""Unit tests: structural gates and important MINT-inspired arithmetic failures."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pack.py"
spec = importlib.util.spec_from_file_location("validate_pack", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
FIXTURE = json.loads((ROOT / "examples" / "minimal-report-manifest.json").read_text(encoding="utf8"))


class ValidatePackTests(unittest.TestCase):
    def test_valid_manifest(self):
        self.assertEqual(module.validate(FIXTURE), [])

    def test_uncovered_original_section_is_error(self):
        pack = copy.deepcopy(FIXTURE)
        pack["sections"].pop()
        self.assertTrue(any("no coverage" in x for x in module.validate(pack)))

    def test_open_blocker_cannot_publish(self):
        pack = copy.deepcopy(FIXTURE)
        pack["issues"] = [{
            "id": "q3-conflict", "severity": "BLOCKER", "status": "OPEN",
            "owner": "earnings-preview", "claim_ids": [], "explanation": "YoY sign is wrong",
            "suggested_action": "Correct upstream baseline", "evidence_refs": ["Q3-2025"]
        }]
        self.assertTrue(any("handoff forbidden" in x for x in module.validate(pack)))
        pack["issues"][0]["status"] = "RESOLVED"
        self.assertEqual(module.validate(pack), [])

    def test_mint_q3_growth_mismatch(self):
        pack = copy.deepcopy(FIXTURE)
        pack["checks"].append({
            "id": "mint-yoy", "kind": "pct_change",
            "inputs": {"previous": 2768, "current": 2350},
            "expected": 10.0, "tolerance": 0.1
        })
        self.assertTrue(any("mint-yoy: arithmetic mismatch" in x for x in module.validate(pack)))
        pack["checks"][-1]["expected"] = -15.101156
        self.assertEqual(module.validate(pack), [])

    def test_wacc_roic_subtraction_error(self):
        pack = copy.deepcopy(FIXTURE)
        pack["checks"].append({"id": "roic-wacc", "kind": "spread_pp",
                               "inputs": {"a": 9.96, "b": 9.50},
                               "expected": 1.6, "tolerance": 0.01})
        self.assertTrue(any("roic-wacc: arithmetic mismatch" in x for x in module.validate(pack)))

    def test_probability_not_one(self):
        pack = copy.deepcopy(FIXTURE)
        pack["checks"][1]["inputs"]["values"] = [0.4, 0.4, 0.1]
        self.assertTrue(any("probability-sum: arithmetic mismatch" in x for x in module.validate(pack)))

    def test_chart_cannot_invent_untracked_value(self):
        pack = copy.deepcopy(FIXTURE)
        pack["visuals"][0]["data"][0]["value"] = 9.2
        self.assertTrue(any("plotted value differs" in x for x in module.validate(pack)))

    def test_unverified_chart_must_cite_claim(self):
        pack = copy.deepcopy(FIXTURE)
        pack["visuals"][0]["source_claim_ids"] = []
        self.assertTrue(any("requires source claim IDs" in x for x in module.validate(pack)))

    def test_contested_claim_rejected_from_chart(self):
        pack = copy.deepcopy(FIXTURE)
        pack["claims"][0]["verification"] = "CONTESTED"
        self.assertTrue(any("contested claim" in x for x in module.validate(pack)))

    def test_manuscript_heading_missing(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "report-ready.md").write_text("# A document with no mapped sections", encoding="utf8")
            (root / "evidence-review.md").write_text("Evidence note", encoding="utf8")
            self.assertTrue(any("not found as Markdown heading" in x for x in module.validate(FIXTURE, root)))

    def test_denominator_zero_is_error(self):
        pack = copy.deepcopy(FIXTURE)
        pack["checks"].append({"id": "division", "kind": "pct_change",
                               "inputs": {"previous": 0, "current": 1},
                               "expected": 100, "tolerance": 0.1})
        self.assertTrue(any("cannot be zero" in x for x in module.validate(pack)))

    def test_weighted_sum(self):
        pack = copy.deepcopy(FIXTURE)
        pack["checks"].append({"id": "fv", "kind": "weighted_sum",
                               "inputs": {"values": [31.77, 25.90, 29.64],
                                          "weights": [0.4, 0.3, 0.3]},
                               "expected": 29.37, "tolerance": 0.001})
        self.assertEqual(module.validate(pack), [])


if __name__ == "__main__":
    unittest.main()