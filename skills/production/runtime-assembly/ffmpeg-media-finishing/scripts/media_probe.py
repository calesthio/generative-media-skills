#!/usr/bin/env python3
"""Deterministic ffprobe audit and expectation validator."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


EXIT_OK = 0
EXIT_EXPECTATION_FAILED = 1
EXIT_USAGE_OR_INPUT = 2
EXIT_TOOL_UNAVAILABLE = 3
EXIT_PROBE_FAILED = 4
EXIT_TIMEOUT = 5
EXIT_MALFORMED_PROBE = 6
EXIT_MALFORMED_EXPECTATION = 7


class MediaProbeError(Exception):
    exit_code = EXIT_PROBE_FAILED


class ToolUnavailableError(MediaProbeError):
    exit_code = EXIT_TOOL_UNAVAILABLE


class ProbeTimeoutError(MediaProbeError):
    exit_code = EXIT_TIMEOUT


class ProbeFailedError(MediaProbeError):
    exit_code = EXIT_PROBE_FAILED


class MalformedProbeError(MediaProbeError):
    exit_code = EXIT_MALFORMED_PROBE


class MalformedExpectationError(MediaProbeError):
    exit_code = EXIT_MALFORMED_EXPECTATION


def _load_json_file(path: Path, error_type: type[MediaProbeError]) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except OSError as exc:
        raise error_type(f"Could not read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise error_type(f"Could not parse JSON in {path}: {exc}") from exc


def _parse_decimal(value: Any) -> float | None:
    if value in (None, "", "N/A"):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _expectation_number(value: Any, label: str, *, allow_negative: bool = True) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise MalformedExpectationError(f"{label} must be numeric") from exc
    if not math.isfinite(number):
        raise MalformedExpectationError(f"{label} must be finite")
    if not allow_negative and number < 0:
        raise MalformedExpectationError(f"{label} must be greater than or equal to 0")
    return number


def _parse_int(value: Any) -> int | None:
    if value in (None, "", "N/A"):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_fraction(value: Any) -> dict[str, Any]:
    text = str(value) if value not in (None, "") else "0/0"
    if text in ("N/A", "0/0"):
        return {"raw": text, "value": None}
    try:
        fraction = Fraction(text)
    except (ValueError, ZeroDivisionError):
        return {"raw": text, "value": None}
    return {"raw": text, "value": float(fraction)}


def _first_stream(streams: list[dict[str, Any]], codec_type: str) -> dict[str, Any] | None:
    for stream in streams:
        if stream.get("codec_type") == codec_type:
            return stream
    return None


def _duration(format_section: dict[str, Any], video: dict[str, Any] | None, audio: dict[str, Any] | None) -> float | None:
    for container in (format_section, video or {}, audio or {}):
        parsed = _parse_decimal(container.get("duration"))
        if parsed is not None:
            return parsed
    return None


def normalize_probe(raw_probe: dict[str, Any], media_path: Path, ffprobe_path: str) -> dict[str, Any]:
    if not isinstance(raw_probe, dict):
        raise MalformedProbeError("ffprobe output was not a JSON object")
    streams = raw_probe.get("streams", [])
    format_section = raw_probe.get("format", {})
    if not isinstance(streams, list) or not isinstance(format_section, dict):
        raise MalformedProbeError("ffprobe JSON is missing object format or list streams")

    video = _first_stream(streams, "video")
    audio = _first_stream(streams, "audio")
    normalized: dict[str, Any] = {
        "schema_version": "1.0",
        "status": "pass",
        "tool": "media_probe.py",
        "ffprobe": {
            "executable": ffprobe_path,
            "argv": [
                ffprobe_path,
                "-v",
                "error",
                "-show_format",
                "-show_streams",
                "-print_format",
                "json",
                str(media_path),
            ],
        },
        "media": {
            "path": str(media_path),
            "format_name": format_section.get("format_name"),
            "format_long_name": format_section.get("format_long_name"),
            "duration_seconds": _duration(format_section, video, audio),
            "size_bytes": _parse_int(format_section.get("size")),
            "bit_rate": _parse_int(format_section.get("bit_rate")),
        },
        "streams": {
            "counts": {
                "video": sum(1 for stream in streams if stream.get("codec_type") == "video"),
                "audio": sum(1 for stream in streams if stream.get("codec_type") == "audio"),
                "subtitle": sum(1 for stream in streams if stream.get("codec_type") == "subtitle"),
                "other": sum(1 for stream in streams if stream.get("codec_type") not in {"video", "audio", "subtitle"}),
            },
            "video": None,
            "audio": None,
        },
        "expectations": None,
    }

    if video is not None:
        normalized["streams"]["video"] = {
            "index": video.get("index"),
            "codec_name": video.get("codec_name"),
            "profile": video.get("profile"),
            "width": _parse_int(video.get("width")),
            "height": _parse_int(video.get("height")),
            "pix_fmt": video.get("pix_fmt"),
            "r_frame_rate": _parse_fraction(video.get("r_frame_rate")),
            "avg_frame_rate": _parse_fraction(video.get("avg_frame_rate")),
            "duration_seconds": _parse_decimal(video.get("duration")),
        }

    if audio is not None:
        normalized["streams"]["audio"] = {
            "index": audio.get("index"),
            "codec_name": audio.get("codec_name"),
            "sample_rate": _parse_int(audio.get("sample_rate")),
            "channels": _parse_int(audio.get("channels")),
            "channel_layout": audio.get("channel_layout"),
            "sample_fmt": audio.get("sample_fmt"),
            "duration_seconds": _parse_decimal(audio.get("duration")),
        }

    return normalized


def run_ffprobe(media_path: Path, ffprobe_path: str, timeout_seconds: float) -> dict[str, Any]:
    executable = shutil.which(ffprobe_path) if Path(ffprobe_path).name == ffprobe_path else ffprobe_path
    if not executable:
        raise ToolUnavailableError(f"ffprobe executable not found: {ffprobe_path}")

    argv = [
        executable,
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-print_format",
        "json",
        str(media_path),
    ]
    try:
        completed = subprocess.run(
            argv,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise ProbeTimeoutError(f"ffprobe timed out after {timeout_seconds:g} seconds") from exc
    except OSError as exc:
        raise ToolUnavailableError(f"Could not execute ffprobe: {exc}") from exc

    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "ffprobe returned a non-zero exit code"
        raise ProbeFailedError(f"ffprobe failed with exit code {completed.returncode}: {detail}")

    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise MalformedProbeError(f"ffprobe did not emit valid JSON: {exc}") from exc


def _get_path(document: dict[str, Any], dotted_path: str) -> tuple[bool, Any]:
    value: Any = document
    for part in dotted_path.split("."):
        if not isinstance(value, dict) or part not in value:
            return False, None
        value = value[part]
    return True, value


def _compare_equal(actual: Any, expected: Any) -> bool:
    return actual == expected


def _compare_in(actual: Any, expected: Any) -> bool:
    return isinstance(expected, list) and actual in expected


def _compare_range(actual: Any, expected: Any) -> bool:
    if not isinstance(expected, dict):
        return False
    actual_number = _parse_decimal(actual)
    if actual_number is None:
        return False
    minimum = expected.get("min")
    maximum = expected.get("max")
    if minimum is not None and actual_number < minimum:
        return False
    if maximum is not None and actual_number > maximum:
        return False
    return True


def _compare_tolerance(actual: Any, expected: Any) -> bool:
    if not isinstance(expected, dict) or "value" not in expected:
        return False
    actual_number = _parse_decimal(actual)
    if actual_number is None:
        return False
    tolerance = expected.get("tolerance", 0.0)
    return abs(actual_number - expected["value"]) <= tolerance


COMPARATORS = {
    "equals": _compare_equal,
    "in": _compare_in,
    "range": _compare_range,
    "tolerance": _compare_tolerance,
}


def _validated_expected_value(comparator: str, expected: Any, position: int) -> Any:
    if comparator == "range":
        if not isinstance(expected, dict):
            raise MalformedExpectationError(f"Check {position} range value must be an object")
        if "min" not in expected and "max" not in expected:
            raise MalformedExpectationError(f"Check {position} range value must include min or max")
        normalized: dict[str, float] = {}
        if expected.get("min") is not None:
            normalized["min"] = _expectation_number(expected.get("min"), f"Check {position} range min")
        if expected.get("max") is not None:
            normalized["max"] = _expectation_number(expected.get("max"), f"Check {position} range max")
        if "min" in normalized and "max" in normalized and normalized["min"] > normalized["max"]:
            raise MalformedExpectationError(f"Check {position} range min must be less than or equal to max")
        return normalized
    if comparator == "tolerance":
        if not isinstance(expected, dict) or "value" not in expected:
            raise MalformedExpectationError(f"Check {position} tolerance value must include value")
        return {
            "value": _expectation_number(expected.get("value"), f"Check {position} tolerance value"),
            "tolerance": _expectation_number(expected.get("tolerance", 0), f"Check {position} tolerance", allow_negative=False),
        }
    return expected


def validate_expectations(report: dict[str, Any], expectation: dict[str, Any]) -> dict[str, Any]:
    checks = expectation.get("checks")
    if not isinstance(checks, list):
        raise MalformedExpectationError("Expectation JSON must contain a checks array")

    results = []
    for position, check in enumerate(checks):
        if not isinstance(check, dict):
            raise MalformedExpectationError(f"Check {position} must be an object")
        field = check.get("field")
        comparator = check.get("op", "equals")
        expected = check.get("value")
        if not isinstance(field, str):
            raise MalformedExpectationError(f"Check {position} is missing string field")
        if comparator not in COMPARATORS:
            raise MalformedExpectationError(f"Check {position} has unsupported op: {comparator}")
        expected = _validated_expected_value(comparator, expected, position)

        present, actual = _get_path(report, field)
        passed = present and COMPARATORS[comparator](actual, expected)
        results.append(
            {
                "field": field,
                "op": comparator,
                "expected": expected,
                "actual": actual if present else None,
                "passed": passed,
                "message": "ok" if passed else ("field missing" if not present else "expectation not met"),
            }
        )

    passed_all = all(result["passed"] for result in results)
    return {"status": "pass" if passed_all else "fail", "checks": results}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe media with ffprobe and emit a stable normalized JSON audit.",
    )
    parser.add_argument("media", type=Path, help="Media file to inspect. The file is never modified.")
    parser.add_argument("--expect", type=Path, help="Optional JSON expectation spec to validate against the audit.")
    parser.add_argument("--ffprobe", default="ffprobe", help="ffprobe executable path or name. Default: ffprobe")
    parser.add_argument("--timeout", type=float, default=30.0, help="ffprobe timeout in seconds. Default: 30")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output with two-space indentation.")
    return parser.parse_args(argv)


def build_error_report(error: MediaProbeError) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "status": "error",
        "error": {"type": error.__class__.__name__, "message": str(error), "exit_code": error.exit_code},
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    media_path = args.media
    if not media_path.exists() or not media_path.is_file():
        error = MediaProbeError(f"Media path is not a readable file: {media_path}")
        error.exit_code = EXIT_USAGE_OR_INPUT  # type: ignore[attr-defined]
        print(json.dumps(build_error_report(error), indent=2 if args.pretty else None), file=sys.stderr)
        return EXIT_USAGE_OR_INPUT
    if args.timeout <= 0:
        error = MediaProbeError("Timeout must be greater than zero")
        error.exit_code = EXIT_USAGE_OR_INPUT  # type: ignore[attr-defined]
        print(json.dumps(build_error_report(error), indent=2 if args.pretty else None), file=sys.stderr)
        return EXIT_USAGE_OR_INPUT

    try:
        raw_probe = run_ffprobe(media_path, args.ffprobe, args.timeout)
        report = normalize_probe(raw_probe, media_path, args.ffprobe)
        if args.expect:
            expectation = _load_json_file(args.expect, MalformedExpectationError)
            report["expectations"] = validate_expectations(report, expectation)
            report["status"] = report["expectations"]["status"]
        print(json.dumps(report, indent=2 if args.pretty else None, sort_keys=True))
        return EXIT_OK if report["status"] == "pass" else EXIT_EXPECTATION_FAILED
    except MediaProbeError as exc:
        print(json.dumps(build_error_report(exc), indent=2 if args.pretty else None, sort_keys=True), file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())