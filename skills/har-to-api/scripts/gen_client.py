#!/usr/bin/env python3
"""
gen_client.py — Render a runnable Python client from an OpenAPI JSON spec.

Reads:  openapi.json (from gen_openapi.py)
Writes: <out>.py — a standalone client using only Python stdlib (urllib).

Usage:
    python gen_client.py <openapi.json> [--out client.py] [--title "X API"]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "..", "templates", "client.py.tmpl")


def _env_name(host: str) -> str:
    """Derive a stable env var name from host: api.stockanalysis.com → HAR2API_AUTH."""
    # All clients share one canonical env var for the most common auth header.
    return "HAR2API_AUTH"


def _auth_headers_from_spec(spec: Dict[str, Any]) -> Dict[str, str]:
    """Walk operations, collect auth header names seen during capture."""
    seen: Dict[str, str] = {}
    for path, ops in spec.get("paths", {}).items():
        for method, op in ops.items():
            desc = op.get("description", "") or ""
            # parse_har/gen_openapi write: "Captured auth headers: X, Y."
            if "Captured auth headers:" in desc:
                after = desc.split("Captured auth headers:", 1)[1]
                names_part = after.split(".", 1)[0]
                for name in [n.strip() for n in names_part.split(",") if n.strip()]:
                    if name not in seen:
                        seen[name] = _env_name(spec.get("info", {}).get("title", ""))
    if not seen:
        # Default — harmless if unused.
        seen["Authorization"] = "HAR2API_AUTH"
    return seen


def _operations_from_spec(spec: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    servers = spec.get("servers", [])
    base_url = servers[0]["url"] if servers else ""

    ops: Dict[str, Dict[str, Any]] = {}
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if method.lower() not in ("get", "post", "put", "patch", "delete"):
                continue
            op_id = op.get("operationId", f"op{len(ops)+1}")
            params = op.get("parameters", []) or []
            query_params = [p["name"] for p in params if p.get("in") == "query"]
            ops[op_id] = {
                "method": method.upper(),
                "path": path,
                "queryParams": query_params,
                "summary": op.get("summary", ""),
            }
    return ops


def _base_url(spec: Dict[str, Any]) -> str:
    servers = spec.get("servers", [])
    if servers:
        return servers[0]["url"].rstrip("/")
    return ""


def render(spec: Dict[str, Any], out_path: str, title: str) -> None:
    try:
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            tmpl = f.read()
    except FileNotFoundError:
        print(f"ERROR: template not found at {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(4)

    auth_headers = _auth_headers_from_spec(spec)
    operations = _operations_from_spec(spec)
    base_url = _base_url(spec)

    rendered = (
        tmpl
        .replace("{{TITLE}}", title)
        .replace("{{BASE_URL}}", base_url)
        .replace("{{AUTH_ENV_NAME}}", "HAR2API_AUTH")
        .replace("{{CLIENT_FILENAME}}", os.path.basename(out_path))
        .replace("{{AUTH_HEADERS}}", json.dumps(auth_headers))
        .replace("{{OPERATIONS}}", json.dumps(operations, indent=4))
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)


def main() -> int:
    p = argparse.ArgumentParser(description="OpenAPI → Python client")
    p.add_argument("spec", help="Path to openapi.json")
    p.add_argument("--out", default="client.py", help="Output .py path")
    p.add_argument("--title", default="Reverse-engineered API", help="Client title")
    args = p.parse_args()

    try:
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read spec: {e}", file=sys.stderr)
        return 3

    render(spec, args.out, args.title)
    print(f"Client → {args.out}")
    print(f"  operations: {len(_operations_from_spec(spec))}")
    print(f"  base_url:   {_base_url(spec)}")
    print(f"\nNext: set $env:HAR2API_AUTH='<token>' then python {os.path.basename(args.out)} list")
    return 0


if __name__ == "__main__":
    sys.exit(main())
