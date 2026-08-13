#!/usr/bin/env python3
"""
gen_openapi.py — Convert parsed endpoints JSON (from parse_har.py) into an
OpenAPI 3.0.3 spec.

Design:
- Pure stdlib (yaml is not required; we emit JSON-formatted OpenAPI which is
  valid and accepted by every OpenAPI tool).
- Each endpoint becomes one operation. Parameters are inferred from the parser
  (path + query). Bodies are inferred from request_body_sample when present.
- Response schemas are inferred shallowly: we try to JSON-parse the response
  sample and walk one level deep. Anything we can't infer is typed as
  object/string fallback so the spec stays valid. A human (or the AI driving
  this skill) can refine later — the goal is a correct starting point, not a
  perfect model.

Usage:
    python gen_openapi.py <endpoints.json> [--out openapi.json] [--title "X API"]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional


# --- Schema inference helpers ---------------------------------------------

def _infer_type(value: Any) -> str:
    if value is None:
        return "string"  # nullable; OpenAPI 3.0 prefers explicit null
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "string"


def _infer_schema(value: Any, depth: int = 0) -> Dict[str, Any]:
    t = _infer_type(value)
    schema: Dict[str, Any] = {"type": t}

    if t == "array":
        if value:
            schema["items"] = _infer_schema(value[0], depth + 1)
        else:
            schema["items"] = {"type": "string"}
        return schema

    if t == "object" and depth < 2:
        props = {}
        for k, v in list(value.items())[:50]:  # cap to avoid huge specs
            props[k] = _infer_schema(v, depth + 1)
        if props:
            schema["properties"] = props
        return schema

    return schema


def _try_parse_json(text: Optional[str]) -> Optional[Any]:
    if not text:
        return None
    text = text.strip()
    if not text or text[0] not in "[{":
        return None
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None


# --- OpenAPI builder -------------------------------------------------------

def build_spec(parsed: Dict[str, Any], title: str) -> Dict[str, Any]:
    endpoints: List[Dict[str, Any]] = parsed.get("endpoints", [])
    if not endpoints:
        print("ERROR: no endpoints in input. Run parse_har.py first.",
              file=sys.stderr)
        sys.exit(2)

    # Group operations by host → tag. Keeps the spec readable when a HAR
    # contains traffic to multiple domains (CDNs, third-party APIs).
    paths: Dict[str, Dict[str, Any]] = {}
    servers_seen: Dict[str, Dict[str, str]] = {}

    for ep in endpoints:
        host = ep["host"]
        if host not in servers_seen:
            servers_seen[host] = {
                "url": f"{ep['scheme']}://{host}",
                "description": f"{host} API",
            }

        tag = host.split(":")[0]  # strip port
        path_key = ep["template_path"] or "/"
        if path_key not in paths:
            paths[path_key] = {}

        op: Dict[str, Any] = {
            "operationId": ep["id"],
            "summary": f"{ep['method']} {ep['template_path']}",
            "tags": [tag],
        }

        # Parameters
        params: List[Dict[str, Any]] = []
        for prm in ep.get("parameters", []):
            params.append({
                "name": prm["name"],
                "in": prm.get("in", "query"),
                "required": prm.get("in") == "path",
                "schema": _infer_schema(prm.get("value_sample")),
                "example": prm.get("value_sample"),
            })
        if params:
            op["parameters"] = params

        # Request body (only for methods that have one)
        if ep["method"] in ("POST", "PUT", "PATCH") and ep.get("request_body_sample"):
            body = _try_parse_json(ep["request_body_sample"])
            schema = _infer_schema(body) if body is not None else {"type": "string"}
            op["requestBody"] = {
                "required": False,
                "content": {
                    "application/json": {
                        "schema": schema,
                        **({"example": body} if body is not None else {}),
                    }
                },
            }

        # Security note (auth headers seen, never their values)
        if ep.get("auth_headers"):
            op["security"] = [{"bearerAuth": []}]
            op["description"] = (
                f"Captured auth headers: {', '.join(ep['auth_headers'])}. "
                "Values are NOT stored — see SKILL.md for how to supply them at "
                "runtime via environment variables."
            )

        # Response
        status = str(ep.get("status") or 200)
        resp_sample = _try_parse_json(ep.get("response_body_sample"))
        resp_schema = (
            _infer_schema(resp_sample) if resp_sample is not None
            else {"type": "string"}
        )
        content_type = ep.get("content_type", "application/json")
        media = "application/json"
        if "xml" in content_type:
            media = "application/xml"

        op["responses"] = {
            status: {
                "description": "Captured response",
                "content": {
                    media: {
                        "schema": resp_schema,
                        **({"example": resp_sample}
                           if resp_sample is not None else {}),
                    }
                },
            }
        }

        # HTTP method key must be lowercase.
        paths[path_key][ep["method"].lower()] = op

    spec: Dict[str, Any] = {
        "openapi": "3.0.3",
        "info": {
            "title": title,
            "version": "0.1.0",
            "description": (
                "Auto-generated by har-to-api skill. Schemas are inferred "
                "shallowly from captured samples and may need refinement. "
                "Auth header values are never stored — set them at runtime."
            ),
        },
        "servers": list(servers_seen.values()),
        "paths": paths,
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "description": (
                        "Placeholder. The real scheme depends on what was "
                        "captured — see operation descriptions."
                    ),
                }
            }
        },
    }
    return spec


def main() -> int:
    p = argparse.ArgumentParser(description="Parsed endpoints → OpenAPI 3.0")
    p.add_argument("endpoints", help="Path to endpoints.json from parse_har.py")
    p.add_argument("--out", default="openapi.json", help="Output spec path")
    p.add_argument("--title", default="Reverse-engineered API",
                   help="Spec title")
    args = p.parse_args()

    try:
        with open(args.endpoints, "r", encoding="utf-8") as f:
            parsed = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read endpoints file: {e}", file=sys.stderr)
        return 3

    spec = build_spec(parsed, args.title)

    try:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"ERROR: cannot write output: {e}", file=sys.stderr)
        return 4

    print(f"OpenAPI 3.0.3 spec → {args.out}")
    print(f"  paths:    {len(spec['paths'])}")
    print(f"  servers:  {len(spec['servers'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
