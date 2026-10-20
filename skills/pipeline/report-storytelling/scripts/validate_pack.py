#!/usr/bin/env python3
"""Validate declared Report Storytelling pack structure and arithmetic.

Does NOT establish factual truth, correctness of upstream financial models,
completeness of the claims extracted from source, or quality of editorial prose.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

REQUIRED_TOP = (
    "schema_version", "report_id", "ticker", "as_of", "language", "audience",
    "upstream_snapshot", "source_sections", "sections", "claims", "issues",
    "checks", "visuals", "disclaimer",
)
CLASSIFICATIONS = {"COMPANY_FACT", "MARKET_FACT", "CONSENSUS", "DERIVED", "ANALYST_ASSUMPTION", "ILLUSTRATION"}
VERIFICATIONS = {"PRIMARY_VERIFIED", "CROSS_CHECKED", "ARITHMETIC_VERIFIED", "SOURCE_ONLY", "UNVERIFIED", "CONTESTED"}
ISSUE_LEVELS = {"BLOCKER", "MAJOR", "MINOR"}
ISSUE_STATUS = {"OPEN", "RESOLVED", "ACCEPTED_WITH_DISCLOSURE"}
CHART_CLASSES = {"OBSERVED", "DERIVED", "MODEL", "ILLUSTRATION"}


def is_number(x: object) -> bool:
    return type(x) in (float, int) and math.isfinite(x)


def as_number(x: object, path: str, errors: list[str]) -> float | None:
    if not is_number(x):
        errors.append(f"{path}: expected finite number")
        return None
    return float(x)


def unique_id_list(items: object, key: str, path: str, errors: list[str]) -> dict[str, dict]:
    out = {}
    if not isinstance(items, list):
        errors.append(f"{path}: expected array")
        return out
    for i, item in enumerate(items):
        at = f"{path}[{i}]"
        if not isinstance(item, dict) or not isinstance(item.get(key), str) or not item[key].strip():
            errors.append(f"{at}: missing {key}")
            continue
        if item[key] in out:
            errors.append(f"{at}: duplicate {key} {item[key]}")
        out[item[key]] = item
    return out


def calculate(check: dict, at: str, errors: list[str]) -> float | None:
    kind = check.get("kind")
    x = check.get("inputs")
    if not isinstance(x, dict):
        errors.append(f"{at}: inputs must be object")
        return None
    if kind in ("pct_change", "spread_pp", "difference"):
        akey, bkey = ("previous", "current") if kind == "pct_change" else ("a", "b")
        a, b = as_number(x.get(akey), f"{at}.inputs.{akey}", errors), as_number(x.get(bkey), f"{at}.inputs.{bkey}", errors)
        if a is None or b is None:
            return None
        if kind == "pct_change":
            if a == 0:
                errors.append(f"{at}: previous value cannot be zero in pct_change")
                return None
            return (b - a) / abs(a) * 100
        return a - b
    if kind in ("sum", "weighted_sum"):
        values = x.get("values")
        if not isinstance(values, list) or not values:
            errors.append(f"{at}.inputs.values: nonempty list required")
            return None
        if not all(is_number(v) for v in values):
            errors.append(f"{at}.inputs.values: all elements must be finite numbers")
            return None
        if kind == "sum":
            return float(sum(values))
        weights = x.get("weights")
        if not isinstance(weights, list) or len(weights) != len(values) or not all(is_number(w) for w in weights):
            errors.append(f"{at}.inputs.weights: finite weights must match values length")
            return None
        if abs(sum(weights) - 1) > 0.00001:
            errors.append(f"{at}.inputs.weights: weights must sum to 1.0")
        return float(sum(v * w for v, w in zip(values, weights)))
    errors.append(f"{at}.kind: unsupported kind {kind!r}")
    return None


def validate(data: dict, base: Path | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root: expected JSON object"]
    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"root: missing {key}")
    if data.get("schema_version") != "1.0":
        errors.append("schema_version: expected '1.0'")
    for key in ("report_id", "ticker", "as_of", "language", "audience", "upstream_snapshot"):
        if not isinstance(data.get(key), str) or not data.get(key, "").strip():
            errors.append(f"{key}: nonempty string required")
    if not isinstance(data.get("disclaimer"), str) or "not financial advice" not in data.get("disclaimer", "").lower():
        errors.append("disclaimer: must contain 'Not financial advice'")
    manuscript = None
    if base is not None:
        for name in ("report-ready.md", "evidence-review.md"):
            if not (base / name).is_file() or not (base / name).read_text(encoding="utf-8").strip():
                errors.append(f"file: missing or empty {name} in manifest directory")
        if (base / "report-ready.md").is_file():
            manuscript = (base / "report-ready.md").read_text(encoding="utf-8")

    sources = data.get("source_sections")
    if not isinstance(sources, list) or not sources or not all(isinstance(s, str) and s.strip() for s in sources):
        errors.append("source_sections: expected nonempty string array")
        sources = []
    if len(sources) != len(set(sources)):
        errors.append("source_sections: duplicate source ID")
    sections = unique_id_list(data.get("sections"), "id", "sections", errors)
    covered = set()
    for sid, section in sections.items():
        ids = section.get("source_ids")
        if not isinstance(ids, list) or not ids or not all(isinstance(x, str) for x in ids):
            errors.append(f"sections.{sid}.source_ids: nonempty string array required")
            continue
        if section.get("completeness") != "COMPLETE":
            errors.append(f"sections.{sid}.completeness: expected COMPLETE")
        heading = section.get("content_heading")
        if not isinstance(heading, str) or not heading.strip():
            errors.append(f"sections.{sid}.content_heading: required")
        elif manuscript is not None:
            headings = [line.strip().lstrip("#").strip() for line in manuscript.splitlines()
                        if line.lstrip().startswith("#")]
            if heading.strip() not in headings:
                errors.append(f"sections.{sid}: content_heading not found as Markdown heading in report-ready.md")
        covered.update(ids)
    for sid in sources:
        if sid not in covered:
            errors.append(f"sections: no coverage for source section {sid}")
    for sid in sorted(covered - set(sources)):
        errors.append(f"sections: unknown source section {sid}")

    claims = unique_id_list(data.get("claims"), "id", "claims", errors)
    for cid, claim in claims.items():
        for name in ("source_step", "source_ref", "period", "unit", "basis"):
            if not isinstance(claim.get(name), str) or not claim[name].strip():
                errors.append(f"claims.{cid}.{name}: required")
        if claim.get("classification") not in CLASSIFICATIONS:
            errors.append(f"claims.{cid}.classification: invalid classification")
        if claim.get("verification") not in VERIFICATIONS:
            errors.append(f"claims.{cid}.verification: invalid verification")
        if "value" in claim and not is_number(claim["value"]):
            errors.append(f"claims.{cid}.value: expected finite number")

    issues = unique_id_list(data.get("issues"), "id", "issues", errors)
    for iid, issue in issues.items():
        severity, status = issue.get("severity"), issue.get("status")
        if severity not in ISSUE_LEVELS or status not in ISSUE_STATUS:
            errors.append(f"issues.{iid}: invalid severity/status")
        if severity == "BLOCKER" and status != "RESOLVED":
            errors.append(f"issues.{iid}: unresolved BLOCKER; handoff forbidden")
        for name in ("owner", "explanation", "suggested_action"):
            if not isinstance(issue.get(name), str) or not issue[name].strip():
                errors.append(f"issues.{iid}.{name}: required")
        ids = issue.get("claim_ids", [])
        if not isinstance(ids, list):
            errors.append(f"issues.{iid}.claim_ids: expected array")
        else:
            for cid in ids:
                if cid not in claims:
                    errors.append(f"issues.{iid}: unknown claim {cid}")

    checks = unique_id_list(data.get("checks"), "id", "checks", errors)
    for cid, check in checks.items():
        actual = calculate(check, f"checks.{cid}", errors)
        expected = as_number(check.get("expected"), f"checks.{cid}.expected", errors)
        tolerance = as_number(check.get("tolerance", 0.0001), f"checks.{cid}.tolerance", errors)
        if tolerance is not None and tolerance < 0:
            errors.append(f"checks.{cid}.tolerance: must be nonnegative")
        if None not in (actual, expected, tolerance) and abs(actual - expected) > tolerance:
            errors.append(f"checks.{cid}: arithmetic mismatch (expected {expected:g}, computed {actual:g}, tol {tolerance:g})")

    visuals = unique_id_list(data.get("visuals"), "id", "visuals", errors)
    for vid, visual in visuals.items():
        for name in ("question", "takeaway_title", "chart_type", "unit", "period", "basis", "source_note", "text_fallback"):
            if not isinstance(visual.get(name), str) or not visual[name].strip():
                errors.append(f"visuals.{vid}.{name}: required")
        classification = visual.get("classification")
        if classification not in CHART_CLASSES:
            errors.append(f"visuals.{vid}.classification: invalid")
        ids = visual.get("source_claim_ids")
        if not isinstance(ids, list):
            errors.append(f"visuals.{vid}.source_claim_ids: expected array")
            ids = []
        if classification != "ILLUSTRATION" and not ids:
            errors.append(f"visuals.{vid}: non-illustration requires source claim IDs")
        for cid in ids:
            if cid not in claims:
                errors.append(f"visuals.{vid}: unknown claim {cid}")
            elif claims[cid].get("verification") == "CONTESTED":
                errors.append(f"visuals.{vid}: contested claim {cid} cannot be graphed as reliable evidence")
        points = visual.get("data")
        if not isinstance(points, list) or not points:
            errors.append(f"visuals.{vid}.data: nonempty array required")
            continue
        for idx, point in enumerate(points):
            if not isinstance(point, dict) or not isinstance(point.get("label"), str) or not is_number(point.get("value")):
                errors.append(f"visuals.{vid}.data[{idx}]: must contain label and finite numeric value")
                continue
            cid = point.get("claim_id")
            if classification != "ILLUSTRATION" and cid not in ids:
                errors.append(f"visuals.{vid}.data[{idx}]: claim_id must be in source_claim_ids")
            if cid in claims and "value" in claims[cid] and abs(point["value"] - claims[cid]["value"]) > 0.000001:
                errors.append(f"visuals.{vid}.data[{idx}]: plotted value differs from source claim {cid}")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifest", type=Path)
    p.add_argument("--json", action="store_true", help="print JSON result")
    args = p.parse_args()
    try:
        obj = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors = [f"unable to read manifest: {exc}"]
    else:
        errors = validate(obj, args.manifest.parent)
    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    else:
        print("Report Storytelling pack: PASS (structural/arithmetic checks only)" if not errors else "Report Storytelling pack: FAIL")
        for error in errors:
            print("  -", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())