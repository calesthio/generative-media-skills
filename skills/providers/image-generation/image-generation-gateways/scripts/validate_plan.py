#!/usr/bin/env python3
"""Validate an offline image-generation gateway approval plan.

This tool prepares a deterministic approval digest. It never imports provider
SDKs, reads credentials, makes network calls, generates media, authorizes a
paid request, or submits a provider job.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlsplit


VERSION = "1.0.0"
ENVELOPE_VERSION = "image-generation-gateway-approval-plan-v1"
ALLOWED_GATEWAYS = {"fal.ai", "replicate", "together-ai"}
ALLOWED_CURRENCIES = {"USD", "EUR", "GBP", "JPY", "CAD", "AUD"}
ALLOWED_VERSION_POLICIES = {"immutable-version", "pinned-endpoint", "maintained-latest", "documented-redirect-risk"}
MAX_JSON_BYTES = 1_000_000
SECRET_KEY_PARTS = (
    "api_key",
    "apikey",
    "auth",
    "authorization",
    "bearer",
    "client_secret",
    "credential",
    "fal_key",
    "password",
    "private_key",
    "replicate_api_token",
    "secret",
    "session",
    "together_api_key",
    "token",
)
SECRET_VALUE_MARKERS = (
    "authorization:",
    "bearer ",
    "api_key=",
    "apikey=",
    "password=",
    "secret=",
    "token=",
    "sk-",
    "whsec_",
)
URL_SECRET_QUERY_PARTS = SECRET_KEY_PARTS + ("access_key", "signature", "sig", "signed", "x_amz_signature")
ROOT_KEYS = {"attempt", "canonical_payload", "gateway", "governance", "model", "output", "price", "schema"}
MODEL_KEYS = {"endpoint", "id", "version_policy"}
SCHEMA_KEYS = {"checked_at", "sha256", "url"}
OUTPUT_KEYS = {"count", "policy"}
PRICE_KEYS = {"billable_units", "ceiling", "checked_at", "currency", "estimate", "source", "unit", "unit_price"}
GOVERNANCE_KEYS = {"governance_digest", "moderation_digest", "rights_digest"}
ATTEMPT_KEYS = {"uuid"}


class PlanError(ValueError):
    pass


class OperationalError(RuntimeError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise OperationalError(f"could not read plan: {exc}") from exc
    if len(raw) > MAX_JSON_BYTES:
        raise OperationalError(f"plan exceeds {MAX_JSON_BYTES} bytes")
    try:
        return json.loads(raw.decode("utf-8"), parse_constant=_reject_json_constant)
    except UnicodeDecodeError as exc:
        raise OperationalError("plan must be UTF-8 JSON") from exc
    except json.JSONDecodeError as exc:
        raise OperationalError(f"plan is not valid JSON: {exc.msg}") from exc
    except ValueError as exc:
        raise OperationalError(f"plan is not strict JSON: {exc}") from exc


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant {value} is not allowed")


def parse_now(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    text = value.strip()
    try:
        if len(text) == 10:
            parsed = datetime.fromisoformat(text).replace(tzinfo=timezone.utc)
        else:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise OperationalError("--now must be an ISO-8601 date or datetime") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def require_dict(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PlanError(f"{path} must be an object")
    return value


def reject_unknown_keys(container: dict[str, Any], allowed: set[str], path: str) -> None:
    unknown = sorted(key for key in container if key not in allowed)
    if unknown:
        raise PlanError(f"{path} contains unknown key(s): {', '.join(unknown)}")


def require_str(container: dict[str, Any], key: str, path: str, *, max_len: int = 512) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PlanError(f"{path}.{key} must be a non-empty string")
    value = value.strip()
    if len(value) > max_len:
        raise PlanError(f"{path}.{key} is too long")
    return value


def require_sha256(container: dict[str, Any], key: str, path: str) -> str:
    value = require_str(container, key, path, max_len=64).lower()
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise PlanError(f"{path}.{key} must be a lowercase SHA-256 hex digest")
    return value


def require_decimal(container: dict[str, Any], key: str, path: str) -> Decimal:
    value = container.get(key)
    if not isinstance(value, str):
        raise PlanError(f"{path}.{key} must be a decimal string")
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise PlanError(f"{path}.{key} must be a finite positive decimal") from exc
    if not parsed.is_finite() or parsed <= 0:
        raise PlanError(f"{path}.{key} must be a finite positive decimal")
    return parsed


def decimal_text(value: Decimal) -> str:
    normalized = value.normalize()
    if normalized == normalized.to_integral():
        return format(normalized, "f")
    return format(normalized, "f")


def validate_url(value: str, path: str) -> str:
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        raise PlanError(f"{path} must be credential-free HTTPS without fragments")
    if parsed.port not in (None, 443):
        raise PlanError(f"{path} must use the default HTTPS port")
    for key, query_value in parse_qsl(parsed.query, keep_blank_values=True):
        normalized_key = key.lower().replace("-", "_").replace(" ", "_")
        if any(part in normalized_key for part in URL_SECRET_QUERY_PARTS):
            if path == "price.source" and normalized_key == "endpoint_id":
                continue
            raise PlanError(f"{path} contains a secret-bearing query parameter")
        assert_no_likely_secret_values(query_value, f"{path}?{key}")
    return value


def validate_uuid4(value: str) -> str:
    try:
        parsed = uuid.UUID(value)
    except ValueError as exc:
        raise PlanError("attempt.uuid must be a canonical UUIDv4") from exc
    normalized = str(parsed)
    if parsed.version != 4 or value != normalized:
        raise PlanError("attempt.uuid must be a canonical UUIDv4")
    return normalized


def validate_fresh_date(value: str, path: str, now: datetime, max_age_days: int) -> str:
    try:
        checked = date.fromisoformat(value)
    except ValueError as exc:
        raise PlanError(f"{path} must be an ISO date") from exc
    today = now.date()
    if checked > today:
        raise PlanError(f"{path} must not be in the future")
    age_days = (today - checked).days
    if age_days > max_age_days:
        raise PlanError(f"{path} is stale: {age_days} days old exceeds {max_age_days}")
    return value


def validate_output_count(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise PlanError("output.count must be an integer")
    if value < 1 or value > 100:
        raise PlanError("output.count must be between 1 and 100")
    return value


def assert_no_likely_secret_keys(value: Any, path: str = "canonical_payload") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise PlanError(f"{path} contains a non-string key")
            normalized = key.lower().replace("-", "_").replace(" ", "_")
            if any(part in normalized for part in SECRET_KEY_PARTS):
                raise PlanError(f"{path}.{key} looks like a secret-bearing key")
            assert_no_likely_secret_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_no_likely_secret_keys(child, f"{path}[{index}]")


def assert_no_likely_secret_values(value: Any, path: str = "plan") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            assert_no_likely_secret_values(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_no_likely_secret_values(child, f"{path}[{index}]")
    elif isinstance(value, str):
        parsed = urlsplit(value)
        if parsed.scheme and parsed.query:
            for key, query_value in parse_qsl(parsed.query, keep_blank_values=True):
                normalized_key = key.lower().replace("-", "_").replace(" ", "_")
                if any(part in normalized_key for part in URL_SECRET_QUERY_PARTS):
                    if path == "plan.price.source" and normalized_key == "endpoint_id":
                        continue
                    raise PlanError(f"{path} contains a secret-bearing query parameter")
                assert_no_likely_secret_values(query_value, f"{path}?{key}")
            return
        lowered = value.strip().lower()
        if any(marker in lowered for marker in SECRET_VALUE_MARKERS):
            raise PlanError(f"{path} looks like it contains a secret value")


def normalize_gateway(value: str) -> str:
    aliases = {"fal": "fal.ai", "fal.ai": "fal.ai", "replicate": "replicate", "together": "together-ai", "together-ai": "together-ai"}
    normalized = value.strip().lower()
    if normalized not in aliases:
        raise PlanError(f"gateway must be one of {sorted(ALLOWED_GATEWAYS)}")
    return aliases[normalized]


def validate_plan(plan: Any, now: datetime, max_age_days: int) -> tuple[dict[str, Any], str]:
    root = require_dict(plan, "plan")
    reject_unknown_keys(root, ROOT_KEYS, "plan")
    assert_no_likely_secret_keys(root, "plan")
    assert_no_likely_secret_values(root, "plan")

    gateway = normalize_gateway(require_str(root, "gateway", "plan", max_len=64))
    model = require_dict(root.get("model"), "model")
    reject_unknown_keys(model, MODEL_KEYS, "model")
    model_id = require_str(model, "id", "model")
    endpoint = require_str(model, "endpoint", "model")
    version_policy = require_str(model, "version_policy", "model", max_len=64)
    if version_policy not in ALLOWED_VERSION_POLICIES:
        raise PlanError(f"model.version_policy must be one of {sorted(ALLOWED_VERSION_POLICIES)}")

    schema = require_dict(root.get("schema"), "schema")
    reject_unknown_keys(schema, SCHEMA_KEYS, "schema")
    schema_url = validate_url(require_str(schema, "url", "schema", max_len=2048), "schema.url")
    schema_sha256 = require_sha256(schema, "sha256", "schema")
    schema_checked_at = validate_fresh_date(require_str(schema, "checked_at", "schema", max_len=10), "schema.checked_at", now, max_age_days)

    payload = root.get("canonical_payload")
    if not isinstance(payload, dict):
        raise PlanError("canonical_payload must be an object")

    output = require_dict(root.get("output"), "output")
    reject_unknown_keys(output, OUTPUT_KEYS, "output")
    output_count = validate_output_count(output.get("count"))
    output_policy = require_str(output, "policy", "output")

    price = require_dict(root.get("price"), "price")
    reject_unknown_keys(price, PRICE_KEYS, "price")
    price_source = validate_url(require_str(price, "source", "price", max_len=2048), "price.source")
    price_checked_at = validate_fresh_date(require_str(price, "checked_at", "price", max_len=10), "price.checked_at", now, max_age_days)
    currency = require_str(price, "currency", "price", max_len=3).upper()
    if currency not in ALLOWED_CURRENCIES:
        raise PlanError(f"price.currency must be one of {sorted(ALLOWED_CURRENCIES)}")
    price_unit = require_str(price, "unit", "price", max_len=64)
    unit_price = require_decimal(price, "unit_price", "price")
    billable_units = require_decimal(price, "billable_units", "price")
    supplied_estimate = require_decimal(price, "estimate", "price")
    ceiling = require_decimal(price, "ceiling", "price")
    computed_estimate = unit_price * billable_units
    if supplied_estimate != computed_estimate:
        raise PlanError(
            f"price.estimate must equal unit_price * billable_units ({decimal_text(computed_estimate)})"
        )
    if ceiling < computed_estimate:
        raise PlanError("price.ceiling must be greater than or equal to the computed estimate")

    governance = require_dict(root.get("governance"), "governance")
    reject_unknown_keys(governance, GOVERNANCE_KEYS, "governance")
    rights_digest = require_sha256(governance, "rights_digest", "governance")
    moderation_digest = require_sha256(governance, "moderation_digest", "governance")
    governance_digest = require_sha256(governance, "governance_digest", "governance")

    attempt = require_dict(root.get("attempt"), "attempt")
    reject_unknown_keys(attempt, ATTEMPT_KEYS, "attempt")
    attempt_uuid = validate_uuid4(require_str(attempt, "uuid", "attempt", max_len=36))

    envelope = {
        "attempt_uuid": attempt_uuid,
        "canonical_payload_sha256": sha256_json(payload),
        "envelope_version": ENVELOPE_VERSION,
        "gateway": gateway,
        "governance": {
            "governance_digest": governance_digest,
            "moderation_digest": moderation_digest,
            "rights_digest": rights_digest,
        },
        "model": {
            "endpoint": endpoint,
            "id": model_id,
            "version_policy": version_policy,
        },
        "output": {
            "count": output_count,
            "policy": output_policy,
        },
        "price": {
            "billable_units": decimal_text(billable_units),
            "ceiling": decimal_text(ceiling),
            "checked_at": price_checked_at,
            "computed_estimate": decimal_text(computed_estimate),
            "currency": currency,
            "source": price_source,
            "unit": price_unit,
            "unit_price": decimal_text(unit_price),
        },
        "schema": {
            "checked_at": schema_checked_at,
            "sha256": schema_sha256,
            "url": schema_url,
        },
    }
    digest = sha256_json(envelope)
    redacted = {
        "approval_sha256": digest,
        "canonical_payload_sha256": envelope["canonical_payload_sha256"],
        "computed_estimate": decimal_text(computed_estimate),
        "currency": currency,
        "envelope": envelope,
        "freshness": {"max_age_days": max_age_days, "now": now.date().isoformat()},
        "script": {"name": "validate_plan.py", "version": VERSION},
        "status": "valid",
    }
    return redacted, digest


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True))


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        emit({"status": "error", "error": {"code": "operational", "message": message}})
        raise SystemExit(3)


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description="Validate an offline image-generation gateway approval plan.")
    parser.add_argument("plan", type=Path, help="Path to the JSON approval plan.")
    parser.add_argument(
        "--max-age-days",
        type=int,
        required=True,
        help="Explicit freshness window for schema and price checked_at dates.",
    )
    parser.add_argument("--now", help="ISO date/datetime for reproducible validation tests and demos.")
    parser.add_argument("--expected-approval-sha256", help="Exact approval digest expected by the caller.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.max_age_days < 0 or args.max_age_days > 366:
        emit({"status": "error", "error": {"code": "operational", "message": "--max-age-days must be between 0 and 366"}})
        return 3
    try:
        now = parse_now(args.now)
        plan = load_json(args.plan)
        payload, digest = validate_plan(plan, now, args.max_age_days)
        if args.expected_approval_sha256:
            expected = args.expected_approval_sha256.strip().lower()
            if len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
                raise PlanError("--expected-approval-sha256 must be a lowercase SHA-256 hex digest")
            if expected != digest:
                emit({
                    "status": "invalid",
                    "error": {"code": "approval_digest_mismatch", "message": "approval digest did not match expected value"},
                    "approval_sha256": digest,
                    "expected_approval_sha256": expected,
                })
                return 2
        emit(payload)
        return 0
    except PlanError as exc:
        emit({"status": "invalid", "error": {"code": "validation", "message": str(exc)}})
        return 2
    except OperationalError as exc:
        emit({"status": "error", "error": {"code": "operational", "message": str(exc)}})
        return 3


if __name__ == "__main__":
    raise SystemExit(main())