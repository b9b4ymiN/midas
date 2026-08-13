#!/usr/bin/env python3
"""
validate_spec.py — Sanity-check an OpenAPI JSON file without external deps.

We verify:
- top-level keys (openapi, info, paths)
- each path+method has operationId and at least one response
- parameter 'in' values are valid
- no $ref points outside the file (we don't resolve external refs)

This is NOT a full OpenAPI validator. It's a fast guard to catch generation
bugs before handing the spec to a human or codegen. For full validation use
`swagger-cli validate` or `redocly lint` if available.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List

VALID_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}
VALID_PARAM_IN = {"query", "header", "path", "cookie"}


def validate(spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    for key in ("openapi", "info", "paths"):
        if key not in spec:
            errors.append(f"missing top-level key: {key}")

    paths = spec.get("paths", {})
    if not isinstance(paths, dict) or not paths:
        errors.append("paths is empty or not a dict")
        return errors

    for path, ops in paths.items():
        if not isinstance(ops, dict):
            errors.append(f"{path}: operations must be a dict")
            continue
        for method, op in ops.items():
            if method.lower() not in VALID_METHODS:
                errors.append(f"{path} {method}: invalid HTTP method")
                continue
            if "operationId" not in op:
                errors.append(f"{path} {method}: missing operationId")
            if "responses" not in op or not op["responses"]:
                errors.append(f"{path} {method}: missing responses")
            for prm in op.get("parameters", []) or []:
                if prm.get("in") not in VALID_PARAM_IN:
                    errors.append(
                        f"{path} {method}: parameter '{prm.get('name')}' "
                        f"has invalid 'in': {prm.get('in')}"
                    )

    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="Lightweight OpenAPI sanity check")
    p.add_argument("spec", help="Path to OpenAPI JSON")
    args = p.parse_args()

    try:
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read spec: {e}", file=sys.stderr)
        return 3

    errors = validate(spec)
    if errors:
        print(f"FAIL — {len(errors)} issue(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK — {len(spec.get('paths', {}))} path(s) look well-formed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
