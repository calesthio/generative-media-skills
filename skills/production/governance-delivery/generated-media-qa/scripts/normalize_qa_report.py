#!/usr/bin/env python3
"""Normalize generated-media QA handoff reports.

Python 3.11+ stdlib only. This script validates a documented JSON report,
sorts findings deterministically, summarizes severities, and computes a
mechanical disposition from explicit policy. It never inspects media or grants
final approval.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


SEVERITIES = ("critical", "major", "minor", "observation")
EVIDENCE_TYPES = ("documented_fact", "empirical_observation", "heuristic")
DISPOSITIONS = ("ready", "hold", "reject")
DEFAULT_POLICY = {
    "critical": "reject",
    "major": "hold",
    "minor": "ready",
    "observation": "ready",
}
DEFAULT_NON_WAIVABLE_AREAS = {"rights", "accessibility", "safety", "policy"}
BLOCKING_DISPOSITIONS = {"hold", "reject"}
WAIVER_REQUIRED_FIELDS = ("owner", "reference")


class ValidationFinding(dict):
    """Schema or handoff validation finding."""

    def __init__(self, path: str, message: str) -> None:
        super().__init__(
            severity="major",
            code="schema_validation",
            path=path,
            message=message,
        )


class OperationalErrorForCli(Exception):
    """Operational failure that should exit 3."""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and normalize a generated-media QA JSON report.",
    )
    parser.add_argument("report", type=Path, help="Path to input QA report JSON.")
    parser.add_argument(
        "--policy",
        help=(
            "JSON object mapping severities to dispositions, for example "
            "'{\"critical\":\"reject\",\"major\":\"hold\"}'. Overrides input policy."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path for normalized JSON. Defaults to stdout.",
    )
    return parser.parse_args(argv)


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except OSError as exc:
        raise OperationalErrorForCli(f"could not read report: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise OperationalErrorForCli(f"could not parse report JSON: {exc}") from exc


def parse_policy_override(raw_policy: str | None) -> dict[str, Any] | None:
    if raw_policy is None:
        return None
    try:
        parsed = json.loads(raw_policy)
    except json.JSONDecodeError as exc:
        raise OperationalErrorForCli(f"could not parse --policy JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise OperationalErrorForCli("--policy must be a JSON object")
    return parsed


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_mapping(value: Any, path: str, findings: list[ValidationFinding]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    findings.append(ValidationFinding(path, "must be an object"))
    return {}


def require_list(value: Any, path: str, findings: list[ValidationFinding]) -> list[Any]:
    if isinstance(value, list):
        return value
    findings.append(ValidationFinding(path, "must be an array"))
    return []


def validate_policy(raw_policy: Any, findings: list[ValidationFinding], source: str) -> dict[str, Any]:
    policy = DEFAULT_POLICY.copy()
    waivable_severities: set[str] = set()
    non_waivable_areas = set(DEFAULT_NON_WAIVABLE_AREAS)
    if raw_policy is None:
        findings.append(ValidationFinding(source, "explicit policy object is required in input or CLI"))
        return {
            "dispositions": policy,
            "waivable_severities": sorted(waivable_severities),
            "non_waivable_areas": sorted(non_waivable_areas),
        }
    mapping = require_mapping(raw_policy, source, findings)
    disposition_mapping = mapping.get("dispositions", mapping)
    disposition_mapping = require_mapping(disposition_mapping, f"{source}.dispositions", findings)
    raw_waivable = mapping.get("waivable_severities", [])
    if raw_waivable is not None:
        for index, severity in enumerate(require_list(raw_waivable, f"{source}.waivable_severities", findings)):
            severity_key = str(severity).strip().lower()
            if severity_key not in SEVERITIES:
                findings.append(ValidationFinding(f"{source}.waivable_severities[{index}]", "unknown severity"))
            else:
                waivable_severities.add(severity_key)
    raw_non_waivable = mapping.get("non_waivable_areas", sorted(non_waivable_areas))
    non_waivable_areas = set()
    for index, area in enumerate(require_list(raw_non_waivable, f"{source}.non_waivable_areas", findings)):
        area_value = str(area).strip().lower()
        if not area_value:
            findings.append(ValidationFinding(f"{source}.non_waivable_areas[{index}]", "must be a non-empty string"))
        else:
            non_waivable_areas.add(area_value)
    non_waivable_areas.update(DEFAULT_NON_WAIVABLE_AREAS)
    for severity, disposition in disposition_mapping.items():
        severity_key = str(severity).strip().lower()
        disposition_value = str(disposition).strip().lower()
        if severity_key not in SEVERITIES:
            findings.append(ValidationFinding(f"{source}.{severity}", "unknown severity in policy"))
            continue
        if disposition_value not in DISPOSITIONS:
            findings.append(ValidationFinding(f"{source}.{severity}", "disposition must be ready, hold, or reject"))
            continue
        policy[severity_key] = disposition_value
    return {
        "dispositions": policy,
        "waivable_severities": sorted(waivable_severities),
        "non_waivable_areas": sorted(non_waivable_areas),
    }


def normalize_checks(raw_checks: Any, findings: list[ValidationFinding]) -> list[dict[str, Any]]:
    checks = []
    for index, item in enumerate(require_list(raw_checks, "checks", findings)):
        check = require_mapping(item, f"checks[{index}]", findings)
        check_id = check.get("id") or check.get("name")
        if not is_non_empty_string(check_id):
            findings.append(ValidationFinding(f"checks[{index}].id", "must be a non-empty string"))
        status = str(check.get("status", "")).strip().lower()
        if status not in {"pass", "fail", "not_applicable", "not_checked"}:
            findings.append(
                ValidationFinding(
                    f"checks[{index}].status",
                    "must be pass, fail, not_applicable, or not_checked",
                )
            )
        evidence_type = str(check.get("evidence_type", "")).strip().lower()
        if evidence_type not in EVIDENCE_TYPES:
            findings.append(ValidationFinding(f"checks[{index}].evidence_type", "unknown evidence type"))
        evidence_detail = check.get("evidence_detail")
        if not is_non_empty_string(evidence_detail):
            findings.append(ValidationFinding(f"checks[{index}].evidence_detail", "must be a non-empty string"))
        checks.append(
            {
                "id": str(check_id).strip() if check_id is not None else "",
                "status": status,
                "evidence_type": evidence_type,
                "evidence_detail": evidence_detail.strip() if isinstance(evidence_detail, str) else "",
            }
        )
    return sorted(checks, key=lambda item: item["id"])


def normalize_waiver(raw_waiver: Any, path: str, findings: list[ValidationFinding]) -> dict[str, str] | None:
    if raw_waiver in (None, False):
        return None
    waiver = require_mapping(raw_waiver, path, findings)
    normalized: dict[str, str] = {}
    for field in WAIVER_REQUIRED_FIELDS:
        value = waiver.get(field)
        if not is_non_empty_string(value):
            findings.append(ValidationFinding(f"{path}.{field}", "waiver requires non-empty owner and reference"))
        else:
            normalized[field] = value.strip()
    if is_non_empty_string(waiver.get("reason")):
        normalized["reason"] = waiver["reason"].strip()
    return normalized


def evidence_needs_locator(evidence_type: str, issue_area: str) -> bool:
    return evidence_type == "empirical_observation" or issue_area in {
        "visual",
        "audio",
        "captions",
        "accessibility",
        "safety",
    }


def normalize_findings(raw_findings: Any, findings: list[ValidationFinding]) -> list[dict[str, Any]]:
    normalized = []
    for index, item in enumerate(require_list(raw_findings, "findings", findings)):
        finding = require_mapping(item, f"findings[{index}]", findings)
        severity = str(finding.get("severity", "")).strip().lower()
        if severity not in SEVERITIES:
            findings.append(ValidationFinding(f"findings[{index}].severity", "unknown severity"))
        evidence_type = str(finding.get("evidence_type", "")).strip().lower()
        if evidence_type not in EVIDENCE_TYPES:
            findings.append(ValidationFinding(f"findings[{index}].evidence_type", "unknown evidence type"))
        issue = finding.get("issue")
        if not is_non_empty_string(issue):
            findings.append(ValidationFinding(f"findings[{index}].issue", "must be a non-empty string"))
        issue_area = str(finding.get("area", "general")).strip().lower() or "general"
        evidence_detail = finding.get("evidence_detail")
        if not is_non_empty_string(evidence_detail):
            findings.append(ValidationFinding(f"findings[{index}].evidence_detail", "must be a non-empty string"))
        locator = finding.get("timecode") or finding.get("frame") or finding.get("region")
        if evidence_needs_locator(evidence_type, issue_area) and not is_non_empty_string(locator):
            findings.append(
                ValidationFinding(
                    f"findings[{index}].timecode",
                    "timecode, frame, or region is required for this evidence",
                )
            )
        normalized.append(
            {
                "id": str(finding.get("id") or f"finding-{index + 1:03d}"),
                "severity": severity,
                "area": issue_area,
                "issue": issue.strip() if isinstance(issue, str) else "",
                "evidence_type": evidence_type,
                "evidence_detail": evidence_detail.strip() if isinstance(evidence_detail, str) else "",
                "timecode": str(finding.get("timecode", "")).strip() or None,
                "frame": str(finding.get("frame", "")).strip() or None,
                "region": str(finding.get("region", "")).strip() or None,
                "recommended_fix": str(finding.get("recommended_fix", "")).strip() or None,
                "owner": str(finding.get("owner", "")).strip() or None,
                "retest_required": bool(finding.get("retest_required", severity in {"critical", "major"})),
                "waiver": normalize_waiver(finding.get("waiver"), f"findings[{index}].waiver", findings),
            }
        )
    severity_rank = {severity: rank for rank, severity in enumerate(SEVERITIES)}
    return sorted(
        normalized,
        key=lambda item: (
            severity_rank.get(item["severity"], len(SEVERITIES)),
            item["area"],
            item["timecode"] or "",
            item["id"],
        ),
    )


def validate_review(raw_review: Any, findings: list[ValidationFinding]) -> dict[str, Any]:
    review = require_mapping(raw_review, "review", findings)
    required = ("reviewer", "date")
    for field in required:
        if not is_non_empty_string(review.get(field)):
            findings.append(ValidationFinding(f"review.{field}", "must be a non-empty string"))
    if is_non_empty_string(review.get("date")):
        try:
            datetime.fromisoformat(review["date"].replace("Z", "+00:00"))
        except ValueError:
            findings.append(ValidationFinding("review.date", "must be ISO-8601 compatible"))
    return {
        "reviewer": str(review.get("reviewer", "")).strip(),
        "date": str(review.get("date", "")).strip(),
        "target_platform": str(review.get("target_platform", "")).strip() or None,
        "intended_use": str(review.get("intended_use", "")).strip() or None,
        "source_package": str(review.get("source_package", "")).strip() or None,
    }


def disposition_for_findings(
    normalized_findings: list[dict[str, Any]],
    policy: dict[str, Any],
    validation_findings: list[ValidationFinding],
) -> str:
    disposition_rank = {"ready": 0, "hold": 1, "reject": 2}
    dispositions = policy["dispositions"]
    waivable_severities = set(policy["waivable_severities"])
    non_waivable_areas = set(policy["non_waivable_areas"])
    worst = "ready"
    for finding in normalized_findings:
        severity = finding["severity"]
        disposition = dispositions.get(severity, DEFAULT_POLICY[severity])
        if finding.get("waiver") and disposition in BLOCKING_DISPOSITIONS:
            if severity not in waivable_severities:
                validation_findings.append(
                    ValidationFinding(f"findings.{finding['id']}.waiver", "policy does not allow waivers for this severity")
                )
            elif finding["area"] in non_waivable_areas:
                validation_findings.append(
                    ValidationFinding(f"findings.{finding['id']}.waiver", "rights, accessibility, safety, and policy findings cannot be waived")
                )
            else:
                disposition = "ready"
        if disposition_rank[disposition] > disposition_rank[worst]:
            worst = disposition
    return worst


def normalize_report(raw_report: Any, policy_override: dict[str, Any] | None = None) -> tuple[dict[str, Any], int]:
    schema_findings: list[ValidationFinding] = []
    report = require_mapping(raw_report, "$", schema_findings)
    asset_id = report.get("asset_id")
    if not is_non_empty_string(asset_id):
        schema_findings.append(ValidationFinding("asset_id", "must be a non-empty string"))
    review = validate_review(report.get("review"), schema_findings)
    policy_source = "cli_policy" if policy_override is not None else "policy"
    policy = validate_policy(policy_override if policy_override is not None else report.get("policy"), schema_findings, policy_source)
    checks = normalize_checks(report.get("checks"), schema_findings)
    qa_findings = normalize_findings(report.get("findings"), schema_findings)
    severity_counts = {severity: 0 for severity in SEVERITIES}
    severity_counts.update(Counter(finding["severity"] for finding in qa_findings if finding["severity"] in SEVERITIES))
    disposition = disposition_for_findings(qa_findings, policy, schema_findings)
    if schema_findings:
        disposition = "hold"
    normalized = {
        "schema_version": "generated-media-qa-report-v1",
        "asset_id": str(asset_id).strip() if isinstance(asset_id, str) else "",
        "review": review,
        "policy": policy,
        "summary": {
            "severity_counts": severity_counts,
            "disposition": disposition,
            "mechanical_only": True,
            "final_approval": False,
        },
        "checks": checks,
        "findings": qa_findings,
        "schema_validation_findings": list(schema_findings),
        "boundaries": [
            "No media inspection performed.",
            "No subjective quality decision made by this script.",
            "No rights, accessibility, safety, or policy waiver granted by this script.",
            "Mechanical disposition is not final approval.",
        ],
    }
    exit_code = 0 if disposition == "ready" and not schema_findings else 2
    return normalized, exit_code


def emit_json(output: dict[str, Any], output_path: Path | None) -> None:
    rendered = json.dumps(output, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    if output_path is None:
        sys.stdout.write(rendered)
        return
    try:
        output_path.write_text(rendered, encoding="utf-8")
    except OSError as exc:
        raise OperationalErrorForCli(f"could not write output: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        raw_report = load_json(args.report)
        policy_override = parse_policy_override(args.policy)
        normalized, exit_code = normalize_report(raw_report, policy_override)
        emit_json(normalized, args.output)
        return exit_code
    except OperationalErrorForCli as exc:
        error = {
            "schema_version": "generated-media-qa-report-v1",
            "error": str(exc),
            "summary": {
                "disposition": "hold",
                "mechanical_only": True,
                "final_approval": False,
            },
        }
        sys.stderr.write(json.dumps(error, sort_keys=True, ensure_ascii=True) + "\n")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())