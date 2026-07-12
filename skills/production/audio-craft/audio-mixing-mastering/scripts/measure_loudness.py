#!/usr/bin/env python3
"""Measure media loudness with FFmpeg loudnorm and emit stable JSON."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


EXIT_OK = 0
EXIT_TARGET_MISMATCH = 2
EXIT_OPERATIONAL_FAILURE = 3

MEASUREMENT_ALGORITHM = "ffmpeg loudnorm single-pass analysis"
MEASUREMENT_STANDARD = "EBU R128 / ITU-R BS.1770 family via FFmpeg loudnorm"
DEFAULT_TIMEOUT_SECONDS = 120.0


class LoudnessToolError(Exception):
    """Base class for operational loudness measurement failures."""


class ToolUnavailableError(LoudnessToolError):
    pass


class LoudnessTimeoutError(LoudnessToolError):
    pass


class LoudnessCommandError(LoudnessToolError):
    def __init__(self, message: str, stderr: str = "") -> None:
        super().__init__(message)
        self.stderr = stderr


class MalformedLoudnormOutputError(LoudnessToolError):
    pass


class NoAudioMeasuredError(LoudnessToolError):
    pass


def _finite_float(value: Any, field_name: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise MalformedLoudnormOutputError(f"{field_name} is not numeric") from exc
    if not math.isfinite(number):
        raise MalformedLoudnormOutputError(f"{field_name} is not finite")
    return number


def build_ffmpeg_command(input_path: Path, ffmpeg_path: str, dual_mono: bool = False) -> list[str]:
    loudnorm_options = ["print_format=json"]
    if dual_mono:
        loudnorm_options.insert(0, "dual_mono=true")
    return [
        ffmpeg_path,
        "-hide_banner",
        "-nostats",
        "-i",
        str(input_path),
        "-map",
        "0:a:0",
        "-vn",
        "-sn",
        "-dn",
        "-af",
        "loudnorm=" + ":".join(loudnorm_options),
        "-f",
        "null",
        "-",
    ]


def extract_loudnorm_json(output: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    search_from = 0
    candidates: list[dict[str, Any]] = []
    while True:
        start = output.find("{", search_from)
        if start == -1:
            break
        try:
            parsed, end = decoder.raw_decode(output[start:])
        except json.JSONDecodeError:
            search_from = start + 1
            continue
        if isinstance(parsed, dict):
            candidates.append(parsed)
        search_from = start + end

    for candidate in reversed(candidates):
        if {"input_i", "input_tp", "input_lra", "input_thresh"}.issubset(candidate):
            return candidate
    raise MalformedLoudnormOutputError("ffmpeg loudnorm JSON block was not found")


def normalize_loudnorm(raw: dict[str, Any], input_path: Path, ffmpeg_name: str, dual_mono: bool = False) -> dict[str, Any]:
    integrated = _finite_float(raw.get("input_i"), "input_i")
    true_peak = _finite_float(raw.get("input_tp"), "input_tp")
    loudness_range = _finite_float(raw.get("input_lra"), "input_lra")
    threshold = _finite_float(raw.get("input_thresh"), "input_thresh")
    ffmpeg_reported_offset = None
    if "target_offset" in raw:
        ffmpeg_reported_offset = _finite_float(raw.get("target_offset"), "target_offset")

    if integrated <= -99.0 and true_peak <= -99.0:
        raise NoAudioMeasuredError("no measurable audio was found in the selected stream")

    return {
        "status": "pass",
        "input": str(input_path),
        "tool": {
            "name": ffmpeg_name,
            "filter": "loudnorm",
            "measurement_standard": MEASUREMENT_STANDARD,
            "algorithm": MEASUREMENT_ALGORITHM,
            "analysis_mode": "single_pass_measurement",
            "dual_mono": dual_mono,
            "ffmpeg_reported_offset_lu": ffmpeg_reported_offset,
            "mode_note": "Measurements depend on the loudness algorithm, filter, FFmpeg build, and analysis mode; this script measures only and never normalizes or mutates media.",
        },
        "measurements": {
            "integrated_lufs": integrated,
            "true_peak_dbtp": true_peak,
            "loudness_range_lu": loudness_range,
            "threshold_lufs": threshold,
        },
        "raw": {
            ("ffmpeg_reported_target_offset" if key == "target_offset" else key): raw[key]
            for key in sorted(raw)
            if key in {"input_i", "input_tp", "input_lra", "input_thresh", "target_offset", "normalization_type"}
        },
    }


def run_loudnorm(input_path: Path, ffmpeg: str = "ffmpeg", timeout: float = DEFAULT_TIMEOUT_SECONDS, dual_mono: bool = False) -> dict[str, Any]:
    ffmpeg_path = shutil.which(ffmpeg)
    if not ffmpeg_path:
        raise ToolUnavailableError(f"ffmpeg executable not found: {ffmpeg}")

    command = build_ffmpeg_command(input_path, ffmpeg_path, dual_mono)
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise LoudnessTimeoutError(f"ffmpeg loudness measurement timed out after {timeout:g} seconds") from exc

    combined_output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    if completed.returncode != 0:
        stderr_lower = completed.stderr.lower()
        if "stream map '0:a:0' matches no streams" in stderr_lower or "matches no streams" in stderr_lower:
            raise NoAudioMeasuredError("input has no selectable audio stream")
        raise LoudnessCommandError(f"ffmpeg exited with code {completed.returncode}", completed.stderr)

    raw = extract_loudnorm_json(combined_output)
    return normalize_loudnorm(raw, input_path, ffmpeg, dual_mono)


def compare_targets(report: dict[str, Any], target_lufs: float | None, lufs_tolerance: float | None, target_true_peak: float | None, true_peak_tolerance: float | None) -> dict[str, Any] | None:
    checks: list[dict[str, Any]] = []
    measurements = report["measurements"]

    if target_lufs is not None:
        tolerance = 0.0 if lufs_tolerance is None else lufs_tolerance
        actual = measurements["integrated_lufs"]
        delta = actual - target_lufs
        checks.append(
            {
                "field": "measurements.integrated_lufs",
                "target": target_lufs,
                "tolerance": tolerance,
                "actual": actual,
                "delta": delta,
                "passed": abs(delta) <= tolerance,
                "comparison": "absolute difference within tolerance",
            }
        )

    if target_true_peak is not None:
        tolerance = 0.0 if true_peak_tolerance is None else true_peak_tolerance
        actual = measurements["true_peak_dbtp"]
        allowed_max = target_true_peak + tolerance
        checks.append(
            {
                "field": "measurements.true_peak_dbtp",
                "target_max": target_true_peak,
                "tolerance": tolerance,
                "allowed_max": allowed_max,
                "actual": actual,
                "delta_to_ceiling": actual - target_true_peak,
                "passed": actual <= allowed_max,
                "comparison": "actual true peak must not exceed target plus tolerance",
            }
        )

    if not checks:
        return None
    return {"status": "pass" if all(check["passed"] for check in checks) else "fail", "checks": checks}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Measure a local media file with FFmpeg loudnorm and emit stable JSON.")
    parser.add_argument("input", type=Path, help="Local media file to measure. The file is never modified.")
    parser.add_argument("--ffmpeg", default="ffmpeg", help="ffmpeg executable name or path. Default: ffmpeg")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS, help="ffmpeg timeout in seconds. Default: 120")
    parser.add_argument("--target-lufs", type=float, help="Explicit integrated loudness target in LUFS. No target is assumed if omitted.")
    parser.add_argument("--lufs-tolerance", type=float, help="Allowed absolute LU difference from --target-lufs. Default: 0 when target is supplied.")
    parser.add_argument("--target-true-peak", type=float, help="Explicit maximum true peak target in dBTP. No peak target is assumed if omitted.")
    parser.add_argument("--true-peak-tolerance", type=float, help="Allowed dB overshoot above --target-true-peak. Default: 0 when target is supplied.")
    parser.add_argument("--dual-mono", action="store_true", help="Ask FFmpeg loudnorm to compensate mono input as dual-mono playback.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    return parser


def _validate_args(args: argparse.Namespace) -> None:
    for field_name in ("timeout", "target_lufs", "lufs_tolerance", "target_true_peak", "true_peak_tolerance"):
        value = getattr(args, field_name)
        if value is not None and not math.isfinite(value):
            raise ValueError(f"--{field_name.replace('_', '-')} must be finite")
    if args.timeout <= 0:
        raise ValueError("--timeout must be greater than 0")
    if args.lufs_tolerance is not None and args.lufs_tolerance < 0:
        raise ValueError("--lufs-tolerance must be greater than or equal to 0")
    if args.true_peak_tolerance is not None and args.true_peak_tolerance < 0:
        raise ValueError("--true-peak-tolerance must be greater than or equal to 0")
    if args.lufs_tolerance is not None and args.target_lufs is None:
        raise ValueError("--lufs-tolerance requires --target-lufs")
    if args.true_peak_tolerance is not None and args.target_true_peak is None:
        raise ValueError("--true-peak-tolerance requires --target-true-peak")


def emit_json(payload: dict[str, Any], pretty: bool) -> None:
    indent = 2 if pretty else None
    print(json.dumps(payload, indent=indent, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        _validate_args(args)
        if not args.input.exists():
            raise FileNotFoundError(f"input file not found: {args.input}")
        report = run_loudnorm(args.input, args.ffmpeg, args.timeout, args.dual_mono)
        comparisons = compare_targets(
            report,
            args.target_lufs,
            args.lufs_tolerance,
            args.target_true_peak,
            args.true_peak_tolerance,
        )
        if comparisons is not None:
            report["targets"] = comparisons
            report["status"] = comparisons["status"]
        emit_json(report, args.pretty)
        return EXIT_OK if report["status"] == "pass" else EXIT_TARGET_MISMATCH
    except (FileNotFoundError, ValueError, LoudnessToolError) as exc:
        emit_json({"status": "error", "error": {"type": exc.__class__.__name__, "message": str(exc)}}, args.pretty)
        return EXIT_OPERATIONAL_FAILURE


if __name__ == "__main__":
    raise SystemExit(main())