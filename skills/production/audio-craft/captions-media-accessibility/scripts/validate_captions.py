#!/usr/bin/env python3
"""Validate SRT and WebVTT caption sidecar files.

This tool performs structural and readability-oriented checks only. It does not
certify legal or accessibility compliance, and it never rewrites cue text.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal


FormatName = Literal["srt", "vtt"]
Severity = Literal["error", "warning"]

VERSION = "1.0.0"

SRT_TIMESTAMP_RE = re.compile(
    r"^(?P<hours>\d{2,}):(?P<minutes>\d{2}):(?P<seconds>\d{2}),(?P<millis>\d{3})$"
)
VTT_TIMESTAMP_RE = re.compile(
    r"^(?:(?P<hours>\d{2,}):)?(?P<minutes>\d{2}):(?P<seconds>\d{2})\.(?P<millis>\d{3})$"
)
SRT_TIMING_RE = re.compile(r"^(?P<start>\S+)\s+-->\s+(?P<end>\S+)\s*$")
VTT_TIMING_RE = re.compile(r"^(?P<start>\S+)\s+-->\s+(?P<end>\S+)(?P<settings>(?:[ \t]+.*)?)$")
WEBVTT_SIGNATURE_RE = re.compile(r"^\ufeff?WEBVTT(?:[ \t].*)?$")
TAG_RE = re.compile(r"<[^>]*>")
PERCENT_RE = re.compile(r"^(?:100(?:\.0+)?|\d{1,2}(?:\.\d+)?)%$")


class CaptionParseError(Exception):
    def __init__(self, code: str, message: str, line: int | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.line = line


@dataclass(frozen=True)
class Location:
    file: str
    line: int | None = None
    column: int | None = None


@dataclass(frozen=True)
class Cue:
    index: int
    identifier: str | None
    start_ms: int
    end_ms: int
    text_lines: list[str]
    timing_line: int
    text_line: int | None


@dataclass(frozen=True)
class Finding:
    severity: Severity
    code: str
    cue: int | None
    location: Location
    message: str

    def to_json(self) -> dict[str, object]:
        location: dict[str, object] = {"file": self.location.file}
        if self.location.line is not None:
            location["line"] = self.location.line
        if self.location.column is not None:
            location["column"] = self.location.column
        return {
            "severity": self.severity,
            "code": self.code,
            "cue": self.cue,
            "location": location,
            "message": self.message,
        }


@dataclass(frozen=True)
class ParsedFile:
    format: FormatName
    cues: list[Cue]


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CaptionParseError("invalid_utf8", f"File is not valid UTF-8: {exc}") from exc
    except OSError as exc:
        raise CaptionParseError("file_read_failed", f"Could not read file: {exc}") from exc


def detect_format(path: Path, text: str, requested: str) -> FormatName:
    if requested in {"srt", "vtt"}:
        return requested  # type: ignore[return-value]

    stripped = text.lstrip("\ufeff")
    first_line = stripped.split("\n", 1)[0].strip()
    if first_line.startswith("WEBVTT"):
        return "vtt"
    if path.suffix.lower() == ".vtt":
        return "vtt"
    if path.suffix.lower() == ".srt":
        return "srt"
    raise CaptionParseError("format_unknown", "Could not auto-detect caption format; pass --format srt or --format vtt")


def parse_srt_timestamp(value: str) -> int:
    match = SRT_TIMESTAMP_RE.match(value)
    if not match:
        raise ValueError("expected HH:MM:SS,mmm")
    hours = int(match.group("hours"))
    minutes = int(match.group("minutes"))
    seconds = int(match.group("seconds"))
    millis = int(match.group("millis"))
    if minutes > 59 or seconds > 59:
        raise ValueError("minutes and seconds must be 00-59")
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def parse_vtt_timestamp(value: str) -> int:
    match = VTT_TIMESTAMP_RE.match(value)
    if not match:
        raise ValueError("expected MM:SS.mmm or HH:MM:SS.mmm")
    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes"))
    seconds = int(match.group("seconds"))
    millis = int(match.group("millis"))
    if minutes > 59 or seconds > 59:
        raise ValueError("minutes and seconds must be 00-59")
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def _is_percentage(value: str) -> bool:
    return bool(PERCENT_RE.match(value))


def _validate_vtt_percentage(value: str, field_name: str) -> None:
    if not _is_percentage(value):
        raise ValueError(f"{field_name} must be a percentage from 0% to 100%")


def _validate_vtt_anchor(value: str, field_name: str) -> None:
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"{field_name} must contain two comma-separated percentages")
    _validate_vtt_percentage(parts[0], field_name)
    _validate_vtt_percentage(parts[1], field_name)


def validate_vtt_style_block(block: list[str], block_start: int) -> None:
    if len(block) < 2:
        raise CaptionParseError("webvtt_style_invalid", "STYLE block must contain CSS lines", block_start)
    for offset, line in enumerate(block[1:], start=1):
        if "-->" in line:
            raise CaptionParseError("webvtt_style_invalid", "STYLE block must not contain cue timing arrows", block_start + offset)


def validate_vtt_region_block(block: list[str], block_start: int) -> None:
    if len(block) < 2:
        raise CaptionParseError("webvtt_region_invalid", "REGION block must contain settings", block_start)
    seen: set[str] = set()
    for offset, line in enumerate(block[1:], start=1):
        if "-->" in line or "=" not in line or re.search(r"\s", line.strip()):
            raise CaptionParseError("webvtt_region_invalid", "REGION settings must use name=value syntax without whitespace", block_start + offset)
        name, value = line.split("=", 1)
        if name in seen:
            raise CaptionParseError("webvtt_region_setting_duplicate", f"Duplicate REGION setting: {name}", block_start + offset)
        seen.add(name)
        try:
            if name == "id":
                if not value or "-->" in value:
                    raise ValueError("id must be non-empty and must not contain -->")
            elif name == "width":
                _validate_vtt_percentage(value, "width")
            elif name == "lines":
                if not value.isdecimal():
                    raise ValueError("lines must be a non-negative integer")
            elif name in {"regionanchor", "viewportanchor"}:
                _validate_vtt_anchor(value, name)
            elif name == "scroll":
                if value != "up":
                    raise ValueError("scroll must be up")
            else:
                raise ValueError(f"unsupported REGION setting: {name}")
        except ValueError as exc:
            raise CaptionParseError("webvtt_region_invalid", str(exc), block_start + offset) from exc


def validate_vtt_cue_settings(settings_text: str, line_number: int) -> None:
    if not settings_text:
        return
    seen: set[str] = set()
    for token in settings_text.split():
        if ":" not in token:
            raise CaptionParseError("webvtt_cue_setting_invalid", "Cue setting must use name:value syntax", line_number)
        name, value = token.split(":", 1)
        if name in seen:
            raise CaptionParseError("webvtt_cue_setting_duplicate", f"Duplicate cue setting: {name}", line_number)
        seen.add(name)
        try:
            if name == "vertical":
                if value not in {"rl", "lr"}:
                    raise ValueError("vertical must be rl or lr")
            elif name == "line":
                line_value = value.split(",", 1)[0]
                if line_value != "auto" and not re.fullmatch(r"-?\d+", line_value) and not _is_percentage(line_value):
                    raise ValueError("line must be auto, an integer, or a percentage from 0% to 100%")
                if "," in value and value.split(",", 1)[1] not in {"start", "center", "end"}:
                    raise ValueError("line alignment must be start, center, or end")
            elif name == "position":
                position_value = value.split(",", 1)[0]
                _validate_vtt_percentage(position_value, "position")
                if "," in value and value.split(",", 1)[1] not in {"line-left", "center", "line-right"}:
                    raise ValueError("position alignment must be line-left, center, or line-right")
            elif name == "size":
                _validate_vtt_percentage(value, "size")
            elif name == "align":
                if value not in {"start", "center", "end", "left", "right"}:
                    raise ValueError("align must be start, center, end, left, or right")
            elif name == "region":
                if not value or re.search(r"\s", value) or "-->" in value:
                    raise ValueError("region must be a non-empty identifier")
            else:
                raise ValueError(f"unsupported cue setting: {name}")
        except ValueError as exc:
            raise CaptionParseError("webvtt_cue_setting_invalid", str(exc), line_number) from exc


def split_blocks(lines: list[str], start_line: int = 1) -> Iterable[tuple[int, list[str]]]:
    block: list[str] = []
    block_start = start_line
    for offset, line in enumerate(lines, start=start_line):
        if line == "":
            if block:
                yield block_start, block
                block = []
            block_start = offset + 1
        else:
            if not block:
                block_start = offset
            block.append(line)
    if block:
        yield block_start, block


def parse_srt(text: str) -> ParsedFile:
    lines = normalize_newlines(text).split("\n")
    cues: list[Cue] = []

    for block_start, block in split_blocks(lines):
        if len(block) < 2:
            raise CaptionParseError("srt_block_too_short", "SRT cue block must include an index, timing line, and text", block_start)
        sequence = block[0].strip()
        if not sequence.isdecimal() or int(sequence) < 1:
            raise CaptionParseError("srt_index_invalid", "SRT cue index must be a positive integer", block_start)
        timing_line = block[1].strip()
        match = SRT_TIMING_RE.match(timing_line)
        if not match:
            raise CaptionParseError("timestamp_syntax", "SRT timing must use HH:MM:SS,mmm --> HH:MM:SS,mmm", block_start + 1)
        try:
            start_ms = parse_srt_timestamp(match.group("start"))
            end_ms = parse_srt_timestamp(match.group("end"))
        except ValueError as exc:
            raise CaptionParseError("timestamp_syntax", str(exc), block_start + 1) from exc
        cues.append(
            Cue(
                index=len(cues) + 1,
                identifier=sequence,
                start_ms=start_ms,
                end_ms=end_ms,
                text_lines=block[2:],
                timing_line=block_start + 1,
                text_line=block_start + 2 if len(block) > 2 else None,
            )
        )
    return ParsedFile(format="srt", cues=cues)


def parse_vtt(text: str) -> ParsedFile:
    lines = normalize_newlines(text).split("\n")
    if not lines or not WEBVTT_SIGNATURE_RE.match(lines[0]):
        raise CaptionParseError("webvtt_header_missing", "WebVTT files must start with WEBVTT", 1)
    if "-->" in lines[0]:
        raise CaptionParseError("webvtt_header_invalid", "WebVTT header must not contain -->", 1)

    header_end: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line == "":
            header_end = index
            break
        if "-->" in line:
            raise CaptionParseError("webvtt_header_separator_missing", "WebVTT signature/header must be separated from cues by a blank line", index + 1)
    if header_end is None:
        raise CaptionParseError("webvtt_header_separator_missing", "WebVTT signature/header must end with a blank line", len(lines))

    cues: list[Cue] = []
    seen_cue = False
    for block_start, block in split_blocks(lines[header_end + 1 :], start_line=header_end + 2):
        first = block[0].strip()
        if first == "NOTE" or first.startswith("NOTE ") or first.startswith("NOTE\t"):
            continue
        if first == "STYLE" or first == "REGION":
            if seen_cue:
                raise CaptionParseError("webvtt_late_header_block", f"{first} block must appear before cues", block_start)
            if first == "STYLE":
                validate_vtt_style_block(block, block_start)
            else:
                validate_vtt_region_block(block, block_start)
            continue

        identifier: str | None = None
        timing_offset = 0
        if "-->" not in block[0]:
            identifier = block[0]
            timing_offset = 1
        if timing_offset >= len(block):
            raise CaptionParseError("webvtt_timing_missing", "WebVTT cue is missing a timing line", block_start)
        timing_line = block[timing_offset].strip()
        match = VTT_TIMING_RE.match(timing_line)
        if not match:
            raise CaptionParseError("timestamp_syntax", "WebVTT timing must use MM:SS.mmm or HH:MM:SS.mmm with -->", block_start + timing_offset)
        validate_vtt_cue_settings(match.group("settings").strip(), block_start + timing_offset)
        try:
            start_ms = parse_vtt_timestamp(match.group("start"))
            end_ms = parse_vtt_timestamp(match.group("end"))
        except ValueError as exc:
            raise CaptionParseError("timestamp_syntax", str(exc), block_start + timing_offset) from exc
        seen_cue = True
        text_start = timing_offset + 1
        cues.append(
            Cue(
                index=len(cues) + 1,
                identifier=identifier,
                start_ms=start_ms,
                end_ms=end_ms,
                text_lines=block[text_start:],
                timing_line=block_start + timing_offset,
                text_line=block_start + text_start if text_start < len(block) else None,
            )
        )
    return ParsedFile(format="vtt", cues=cues)


def visible_text(line: str) -> str:
    return TAG_RE.sub("", line).strip()


def validate_cues(parsed: ParsedFile, file_label: str, max_lines: int, max_chars_per_line: int, cps_warning: float) -> list[Finding]:
    findings: list[Finding] = []
    previous_start: int | None = None
    previous_end: int | None = None

    if not parsed.cues:
        findings.append(Finding("warning", "no_cues", None, Location(file_label), "Caption file contains no cues"))

    for cue in parsed.cues:
        if cue.start_ms >= cue.end_ms:
            findings.append(Finding("error", "time_order", cue.index, Location(file_label, cue.timing_line), "Cue start time must be before end time"))

        if previous_start is not None and cue.start_ms < previous_start:
            findings.append(Finding("error", "cue_order", cue.index, Location(file_label, cue.timing_line), "Cue start time is earlier than the previous cue start time"))
        if previous_end is not None and cue.start_ms < previous_end:
            findings.append(Finding("error", "cue_overlap", cue.index, Location(file_label, cue.timing_line), "Cue overlaps the previous cue"))
        previous_start = cue.start_ms
        previous_end = cue.end_ms

        nonempty_lines = [line for line in cue.text_lines if visible_text(line)]
        if not nonempty_lines:
            findings.append(Finding("error", "cue_text_missing", cue.index, Location(file_label, cue.text_line or cue.timing_line), "Cue must contain caption text"))
        if parsed.format == "srt" and cue.identifier is not None and cue.identifier.isdecimal() and int(cue.identifier) != cue.index:
            findings.append(Finding("warning", "srt_index_sequence", cue.index, Location(file_label, cue.timing_line - 1), f"SRT cue index is {cue.identifier}; expected {cue.index}"))
        if len(cue.text_lines) > max_lines:
            findings.append(Finding("warning", "max_lines", cue.index, Location(file_label, cue.text_line or cue.timing_line), f"Cue has {len(cue.text_lines)} text lines; limit is {max_lines}"))
        for offset, line in enumerate(cue.text_lines):
            text_length = len(visible_text(line))
            if text_length > max_chars_per_line:
                line_number = (cue.text_line or cue.timing_line) + offset
                findings.append(Finding("warning", "max_chars_per_line", cue.index, Location(file_label, line_number), f"Cue line has {text_length} characters; limit is {max_chars_per_line}"))

        duration_seconds = max((cue.end_ms - cue.start_ms) / 1000.0, 0.001)
        char_count = sum(len(visible_text(line)) for line in cue.text_lines)
        cps = char_count / duration_seconds
        if char_count and cps > cps_warning:
            findings.append(Finding("warning", "characters_per_second", cue.index, Location(file_label, cue.timing_line), f"Cue reads at {cps:.2f} characters per second; warning threshold is {cps_warning:g}"))
    return findings


def validate_file(path: Path, requested_format: str, args: argparse.Namespace) -> tuple[dict[str, object], list[Finding]]:
    text = read_utf8(path)
    caption_format = detect_format(path, text, requested_format)
    parsed = parse_srt(text) if caption_format == "srt" else parse_vtt(text)
    findings = validate_cues(parsed, str(path), args.max_lines, args.max_chars_per_line, args.cps_warning)
    file_summary: dict[str, object] = {
        "path": str(path),
        "format": caption_format,
        "cues": len(parsed.cues),
        "errors": sum(1 for finding in findings if finding.severity == "error"),
        "warnings": sum(1 for finding in findings if finding.severity == "warning"),
    }
    return file_summary, findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate SRT and WebVTT caption files and emit stable JSON.")
    parser.add_argument("paths", nargs="+", help="Caption files to validate")
    parser.add_argument("--format", choices=["auto", "srt", "vtt"], default="auto", help="Caption format, or auto-detect from content/extension")
    parser.add_argument("--max-lines", type=int, default=2, help="Warn when a cue has more than this many text lines")
    parser.add_argument("--max-chars-per-line", type=int, default=42, help="Warn when a cue text line is longer than this many visible characters")
    parser.add_argument("--cps-warning", type=float, default=20.0, help="Warn above this visible characters-per-second rate")
    parser.add_argument("--warnings-as-errors", action="store_true", help="Exit with validation failure when warnings are present")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def make_output(files: list[dict[str, object]], findings: list[Finding], status: str) -> dict[str, object]:
    errors = sum(1 for finding in findings if finding.severity == "error")
    warnings = sum(1 for finding in findings if finding.severity == "warning")
    return {
        "tool": "validate_captions",
        "version": VERSION,
        "status": status,
        "summary": {
            "files": len(files),
            "cues": sum(int(file_summary["cues"]) for file_summary in files),
            "errors": errors,
            "warnings": warnings,
        },
        "files": files,
        "findings": [finding.to_json() for finding in findings],
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.max_lines < 1:
        parser.error("--max-lines must be at least 1")
    if args.max_chars_per_line < 1:
        parser.error("--max-chars-per-line must be at least 1")
    if args.cps_warning <= 0:
        parser.error("--cps-warning must be greater than 0")

    files: list[dict[str, object]] = []
    findings: list[Finding] = []
    operational_failure = False

    for raw_path in args.paths:
        path = Path(raw_path)
        try:
            file_summary, file_findings = validate_file(path, args.format, args)
            files.append(file_summary)
            findings.extend(file_findings)
        except CaptionParseError as exc:
            operational_failure = True
            files.append({"path": str(path), "format": args.format, "cues": 0, "errors": 1, "warnings": 0})
            findings.append(Finding("error", exc.code, None, Location(str(path), exc.line), exc.message))

    errors = sum(1 for finding in findings if finding.severity == "error")
    warnings = sum(1 for finding in findings if finding.severity == "warning")
    if operational_failure:
        status = "operational_failure"
        exit_code = 3
    elif errors or (args.warnings_as_errors and warnings):
        status = "failed"
        exit_code = 2
    else:
        status = "passed"
        exit_code = 0

    output = make_output(files, findings, status)
    print(json.dumps(output, indent=2 if args.pretty else None, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())