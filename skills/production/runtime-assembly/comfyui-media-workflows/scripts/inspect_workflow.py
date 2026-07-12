#!/usr/bin/env python3
"""Inspect ComfyUI API-format workflow JSON without executing it.

This script validates the static shape of the API prompt graph exported from
ComfyUI with File -> Export Workflow (API). It does not contact a ComfyUI
server, install custom nodes, load models, or claim runtime compatibility.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from typing import Any


EXIT_OK = 0
EXIT_VALIDATION_ERRORS = 2
EXIT_OPERATIONAL_ERROR = 3

SECRET_KEY_RE = re.compile(
    r"(api[_-]?key|access[_-]?token|auth|authorization|bearer|client[_-]?secret|credential|password|private[_-]?key|secret|token)",
    re.IGNORECASE,
)
SECRET_VALUE_RE = re.compile(
    r"(sk-[A-Za-z0-9_-]{16,}|comfyui-[A-Za-z0-9_*.-]{16,}|[A-Za-z0-9_-]{32,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,})"
)
PRIVATE_PATH_PARTS = {"users", "home", "documents", "desktop", "downloads", "appdata", "onedrive"}


class WorkflowInspectionError(Exception):
    """Raised for parse or operational failures."""


def add_finding(findings: list[dict[str, str]], severity: str, code: str, path: str, message: str) -> None:
    findings.append(
        {
            "severity": severity,
            "code": code,
            "path": path,
            "message": message,
        }
    )


def load_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise WorkflowInspectionError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    except OSError as exc:
        raise WorkflowInspectionError(f"could not read workflow JSON: {exc}") from exc


def load_approved_classes(path: str | None) -> set[str] | None:
    if path is None:
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return {line.strip() for line in handle if line.strip() and not line.lstrip().startswith("#")}
    except OSError as exc:
        raise WorkflowInspectionError(f"could not read approved class list: {exc}") from exc


def is_node_id(value: Any) -> bool:
    if isinstance(value, str):
        return value != ""
    if isinstance(value, int) and not isinstance(value, bool):
        return True
    return False


def normalize_node_id(value: Any) -> str:
    return str(value)


def is_link_value(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 2
        and is_node_id(value[0])
        and isinstance(value[1], int)
        and not isinstance(value[1], bool)
    )


def looks_like_path(value: str) -> bool:
    if re.match(r"^[A-Za-z]:[\\/]", value) or value.startswith("\\\\"):
        return True
    if value.startswith("/"):
        return True
    lower = value.replace("\\", "/").lower()
    parts = [part for part in lower.split("/") if part]
    return bool(parts and parts[0] in PRIVATE_PATH_PARTS)


def redact_reason_for_value(value: str) -> str:
    reasons = []
    if SECRET_VALUE_RE.search(value):
        reasons.append("secret-like token")
    if looks_like_path(value):
        reasons.append("absolute or private-looking path")
    return " and ".join(reasons)


def scan_sensitive_values(value: Any, path: str, findings: list[dict[str, str]]) -> None:
    if isinstance(value, dict):
        for key in sorted(value.keys(), key=str):
            child_path = f"{path}.{key}"
            if isinstance(key, str) and SECRET_KEY_RE.search(key):
                add_finding(
                    findings,
                    "warning",
                    "suspicious_key",
                    child_path,
                    "key name looks secret-like; value redacted",
                )
            scan_sensitive_values(value[key], child_path, findings)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_sensitive_values(item, f"{path}[{index}]", findings)
    elif isinstance(value, str):
        reason = redact_reason_for_value(value)
        if reason:
            add_finding(
                findings,
                "warning",
                "suspicious_value",
                path,
                f"string value looks like {reason}; raw value redacted",
            )


def iter_links(inputs: dict[str, Any]) -> list[tuple[str, str, int]]:
    links: list[tuple[str, str, int]] = []
    for input_name in sorted(inputs.keys()):
        value = inputs[input_name]
        if is_link_value(value):
            links.append((input_name, normalize_node_id(value[0]), value[1]))
    return links


def find_cycles(adjacency: dict[str, list[str]]) -> list[list[str]]:
    state: dict[str, str] = {}
    stack: list[str] = []
    cycles: list[list[str]] = []
    seen_cycle_keys: set[tuple[str, ...]] = set()

    def canonical_cycle(cycle: list[str]) -> tuple[str, ...]:
        rotations = [tuple(cycle[index:] + cycle[:index]) for index in range(len(cycle))]
        return min(rotations)

    def visit(node_id: str) -> None:
        state[node_id] = "visiting"
        stack.append(node_id)
        for next_id in adjacency.get(node_id, []):
            if state.get(next_id) == "visiting":
                cycle = stack[stack.index(next_id) :]
                key = canonical_cycle(cycle)
                if key not in seen_cycle_keys:
                    seen_cycle_keys.add(key)
                    cycles.append(list(key))
            elif state.get(next_id) is None:
                visit(next_id)
        stack.pop()
        state[node_id] = "visited"

    for node_id in sorted(adjacency.keys(), key=str):
        if state.get(node_id) is None:
            visit(node_id)
    return cycles


def inspect_workflow(
    workflow: Any,
    approved_classes: set[str] | None = None,
    unknown_class_policy: str = "warning",
) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    nodes: dict[str, dict[str, Any]] = {}
    duplicate_ids: set[str] = set()

    if not isinstance(workflow, dict):
        add_finding(findings, "error", "invalid_root", "$", "workflow must be a JSON object keyed by node ID")
        workflow_items: list[tuple[Any, Any]] = []
    else:
        workflow_items = sorted(workflow.items(), key=lambda item: str(item[0]))

    for raw_node_id, node in workflow_items:
        node_path = f"$.{raw_node_id}"
        if not is_node_id(raw_node_id):
            add_finding(findings, "error", "invalid_node_id", node_path, "node ID must be a non-empty string or integer")
            continue
        node_id = normalize_node_id(raw_node_id)
        if node_id in nodes:
            duplicate_ids.add(node_id)
            add_finding(findings, "error", "duplicate_node_id", node_path, "node ID duplicates another ID after string normalization")
            continue
        if not isinstance(node, dict):
            add_finding(findings, "error", "invalid_node", node_path, "node entry must be an object")
            continue

        class_type = node.get("class_type")
        inputs = node.get("inputs")
        if not isinstance(class_type, str) or not class_type:
            add_finding(findings, "error", "invalid_class_type", f"{node_path}.class_type", "class_type must be a non-empty string")
        elif approved_classes is not None and class_type not in approved_classes:
            severity = "error" if unknown_class_policy == "error" else "warning"
            if unknown_class_policy != "ignore":
                add_finding(findings, severity, "unknown_class_type", f"{node_path}.class_type", "class_type is not in the approved class list")
        if not isinstance(inputs, dict):
            add_finding(findings, "error", "invalid_inputs", f"{node_path}.inputs", "inputs must be an object")
            inputs = {}
        if "_meta" in node and not isinstance(node["_meta"], dict):
            add_finding(findings, "error", "invalid_meta", f"{node_path}._meta", "_meta must be an object when present")

        nodes[node_id] = {
            "class_type": class_type if isinstance(class_type, str) else None,
            "inputs": inputs,
        }

    scan_sensitive_values(workflow, "$", findings)

    edge_records: list[dict[str, Any]] = []
    adjacency: dict[str, list[str]] = defaultdict(list)
    incoming_by_target: dict[str, list[str]] = defaultdict(list)
    for target_id in sorted(nodes.keys(), key=str):
        inputs = nodes[target_id]["inputs"]
        for input_name in sorted(inputs.keys()):
            value = inputs[input_name]
            input_path = f"$.{target_id}.inputs.{input_name}"
            if isinstance(value, list) and len(value) == 2 and is_node_id(value[0]):
                if not isinstance(value[1], int) or isinstance(value[1], bool):
                    add_finding(findings, "error", "invalid_link_output_index", input_path, "link output index must be an integer")
                    continue
                if value[1] < 0:
                    add_finding(findings, "error", "invalid_link_output_index", input_path, "link output index must be nonnegative")
                    continue
                source_id = normalize_node_id(value[0])
                if source_id not in nodes:
                    add_finding(findings, "error", "dangling_link", input_path, "link source node does not exist")
                    continue
                edge_records.append(
                    {
                        "from": source_id,
                        "input": input_name,
                        "output_index": value[1],
                        "to": target_id,
                    }
                )
                adjacency[source_id].append(target_id)
                incoming_by_target[target_id].append(source_id)
            elif isinstance(value, list) and len(value) == 2 and (is_node_id(value[0]) or isinstance(value[1], int)):
                add_finding(findings, "error", "invalid_link", input_path, "link-like input must be [node_id, nonnegative_output_index]")

    for node_id in nodes:
        adjacency.setdefault(node_id, [])
    for cycle in find_cycles(adjacency):
        add_finding(findings, "error", "cycle", "$", "cycle detected: " + " -> ".join(cycle + [cycle[0]]))

    class_counts = Counter(node["class_type"] for node in nodes.values() if node["class_type"])
    severity_counts = Counter(finding["severity"] for finding in findings)
    normalized_nodes = [
        {
            "id": node_id,
            "class_type": nodes[node_id]["class_type"],
            "input_count": len(nodes[node_id]["inputs"]),
            "incoming_edge_count": len(incoming_by_target.get(node_id, [])),
            "outgoing_edge_count": len(adjacency.get(node_id, [])),
        }
        for node_id in sorted(nodes.keys(), key=str)
    ]
    findings.sort(key=lambda finding: (finding["severity"], finding["code"], finding["path"], finding["message"]))
    edge_records.sort(key=lambda edge: (edge["from"], edge["to"], edge["input"], edge["output_index"]))

    return {
        "format": "comfyui-api-workflow-inspection-v1",
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edge_records),
            "class_count": len(class_counts),
            "finding_count": len(findings),
            "error_count": severity_counts.get("error", 0),
            "warning_count": severity_counts.get("warning", 0),
        },
        "classes": dict(sorted(class_counts.items())),
        "nodes": normalized_nodes,
        "edges": edge_records,
        "findings": findings,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect ComfyUI API-format workflow JSON without executing it.",
    )
    parser.add_argument("workflow", help="Path to ComfyUI API-format workflow JSON")
    parser.add_argument(
        "--approved-classes",
        help="Optional newline-delimited allowlist of approved class_type names",
    )
    parser.add_argument(
        "--unknown-class",
        choices=("warning", "error", "ignore"),
        default="warning",
        help="How to report class_type values absent from --approved-classes (default: warning)",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        workflow = load_json(args.workflow)
        approved_classes = load_approved_classes(args.approved_classes)
        report = inspect_workflow(workflow, approved_classes, args.unknown_class)
    except WorkflowInspectionError as exc:
        error_report = {
            "format": "comfyui-api-workflow-inspection-v1",
            "summary": {"node_count": 0, "edge_count": 0, "class_count": 0, "finding_count": 1, "error_count": 1, "warning_count": 0},
            "classes": {},
            "nodes": [],
            "edges": [],
            "findings": [
                {
                    "severity": "error",
                    "code": "operational_error",
                    "path": "$",
                    "message": str(exc),
                }
            ],
        }
        print(json.dumps(error_report, indent=2 if args.pretty else None, sort_keys=True))
        return EXIT_OPERATIONAL_ERROR

    print(json.dumps(report, indent=2 if args.pretty else None, sort_keys=True))
    return EXIT_VALIDATION_ERRORS if report["summary"]["error_count"] else EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())