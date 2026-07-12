#!/usr/bin/env python3
"""Static HyperFrames timing preflight for local composition HTML.

This tool intentionally uses Python's html.parser and does not execute browser
JavaScript, load assets, or replace HyperFrames lint/validate/preview/render.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

EXIT_OK = 0
EXIT_STATIC_FINDINGS = 2
EXIT_OPERATIONAL_FAILURE = 3

TIMING_ATTRS = ("data-start", "data-duration", "data-track-index")
VISUAL_TAGS = {
    "a",
    "article",
    "aside",
    "canvas",
    "div",
    "figure",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "img",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "picture",
    "section",
    "span",
    "svg",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "ul",
    "video",
}
NON_VISUAL_TIMED_TAGS = {"audio", "source", "track", "script", "style", "meta", "link"}

SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


class TimelineAuditError(Exception):
    """Operational or parse failure."""


class CliUsageError(Exception):
    """Invalid CLI usage."""


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CliUsageError(message)


@dataclass(frozen=True)
class Element:
    order: int
    tag: str
    attrs: dict[str, str]
    line: int
    column: int

    @property
    def element_name(self) -> str:
        element_id = self.attrs.get("id")
        if element_id:
            return f"{self.tag}#{element_id}"
        classes = [item for item in self.attrs.get("class", "").split() if item]
        if classes:
            return f"{self.tag}." + ".".join(classes)
        return self.tag

    @property
    def has_timing(self) -> bool:
        return any(attr in self.attrs for attr in TIMING_ATTRS)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    element: str | None
    location: dict[str, int] | None
    message: str

    def to_json(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "element": self.element,
            "location": self.location,
            "message": self.message,
        }


class CompositionParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.elements: list[Element] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._record(tag, attrs)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._record(tag, attrs)

    def _record(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line, column = self.getpos()
        attr_map: dict[str, str] = {}
        for name, value in attrs:
            attr_map[name.lower()] = "" if value is None else value
        self.elements.append(Element(len(self.elements), tag.lower(), attr_map, line, column + 1))


def parse_finite_float(value: str) -> float | None:
    try:
        number = float(value)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return number


def parse_nonnegative_integer(value: str) -> int | None:
    try:
        number = int(value, 10)
    except ValueError:
        return None
    if str(number) != value.strip():
        return None
    if number < 0:
        return None
    return number


def is_frame_aligned(seconds: float, fps: float, tolerance: float) -> bool:
    frame_position = seconds * fps
    return abs(frame_position - round(frame_position)) <= tolerance


def location_for(element: Element) -> dict[str, int]:
    return {"line": element.line, "column": element.column}


def add_finding(
    findings: list[Finding],
    severity: str,
    code: str,
    element: Element | None,
    message: str,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            code=code,
            element=element.element_name if element else None,
            location=location_for(element) if element else None,
            message=message,
        )
    )


def has_clip_class(element: Element) -> bool:
    return "clip" in element.attrs.get("class", "").split()


def requires_track_index(element: Element) -> bool:
    return element.has_timing and (has_clip_class(element) or element.tag in {"audio", "video"})


def is_composition_root(element: Element) -> bool:
    return "data-composition-id" in element.attrs


def requires_clip_class(element: Element) -> bool:
    return element.has_timing and not is_composition_root(element) and element.tag in VISUAL_TAGS and element.tag not in NON_VISUAL_TIMED_TAGS


def requires_duration(element: Element) -> bool:
    return element.has_timing and not is_composition_root(element)


def finding_sort_key(finding: Finding) -> tuple[int, int, int, str, str]:
    location = finding.location or {"line": 0, "column": 0}
    return (
        SEVERITY_ORDER[finding.severity],
        location["line"],
        location["column"],
        finding.code,
        finding.element or "",
    )


def inventory_sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
    return (item["location"]["line"], item["location"]["column"], item["element"])


def audit_elements(
    elements: list[Element],
    *,
    duration: float | None,
    fps: float | None,
    tolerance: float,
) -> tuple[list[dict[str, Any]], list[Finding]]:
    findings: list[Finding] = []
    inventory: list[dict[str, Any]] = []
    seen_ids: dict[str, Element] = {}

    for element in elements:
        element_id = element.attrs.get("id")
        if element_id:
            if element_id in seen_ids:
                add_finding(
                    findings,
                    "error",
                    "duplicate-id",
                    element,
                    f"Duplicate id '{element_id}' also appears at line {seen_ids[element_id].line}.",
                )
            else:
                seen_ids[element_id] = element

        if not element.has_timing:
            continue

        start_value = element.attrs.get("data-start")
        duration_value = element.attrs.get("data-duration")
        track_value = element.attrs.get("data-track-index")
        start = parse_finite_float(start_value) if start_value is not None else None
        clip_duration = parse_finite_float(duration_value) if duration_value is not None else None
        track_index = parse_nonnegative_integer(track_value) if track_value is not None else None

        inventory.append(
            {
                "element": element.element_name,
                "tag": element.tag,
                "id": element_id,
                "classes": element.attrs.get("class", ""),
                "location": location_for(element),
                "data_start": start_value,
                "data_duration": duration_value,
                "data_track_index": track_value,
            }
        )

        if start_value is None:
            add_finding(findings, "error", "missing-start", element, "Timed element is missing data-start.")
        elif start is None or start < 0:
            add_finding(findings, "error", "invalid-start", element, "data-start must be a finite nonnegative number.")

        if duration_value is None and requires_duration(element):
            add_finding(findings, "error", "missing-duration", element, "Timed element is missing data-duration.")
        elif duration_value is not None and (clip_duration is None or clip_duration <= 0):
            add_finding(findings, "error", "invalid-duration", element, "data-duration must be a finite positive number.")

        if requires_track_index(element):
            if track_value is None:
                add_finding(findings, "error", "missing-track-index", element, "Timed clip/media element is missing data-track-index.")
            elif track_index is None:
                add_finding(findings, "error", "invalid-track-index", element, "data-track-index must be an integer greater than or equal to 0.")

        if requires_clip_class(element) and not has_clip_class(element):
            add_finding(findings, "error", "missing-clip-class", element, "Timed visual element must include class=\"clip\".")

        if start is not None and clip_duration is not None and start >= 0 and clip_duration > 0:
            end = start + clip_duration
            if duration is not None and end > duration:
                add_finding(
                    findings,
                    "error",
                    "end-beyond-duration",
                    element,
                    f"Timed element ends at {end:g}s beyond composition duration {duration:g}s.",
                )
            if fps is not None:
                if not is_frame_aligned(start, fps, tolerance):
                    add_finding(
                        findings,
                        "warning",
                        "frame-boundary-start",
                        element,
                        f"data-start {start:g}s is not aligned to a frame boundary at {fps:g} fps.",
                    )
                if not is_frame_aligned(clip_duration, fps, tolerance):
                    add_finding(
                        findings,
                        "warning",
                        "frame-boundary-duration",
                        element,
                        f"data-duration {clip_duration:g}s is not aligned to a frame boundary at {fps:g} fps.",
                    )
                if not is_frame_aligned(end, fps, tolerance):
                    add_finding(
                        findings,
                        "warning",
                        "frame-boundary-end",
                        element,
                        f"Element end {end:g}s is not aligned to a frame boundary at {fps:g} fps.",
                    )

    findings.sort(key=finding_sort_key)
    inventory.sort(key=inventory_sort_key)
    return inventory, findings


def load_html(path: Path) -> str:
    if not path.is_file():
        raise TimelineAuditError(f"input file does not exist: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise TimelineAuditError(f"input file is not valid UTF-8: {path}") from exc
    except OSError as exc:
        raise TimelineAuditError(f"could not read input file: {exc}") from exc


def parse_html(source: str) -> list[Element]:
    parser = CompositionParser()
    try:
        parser.feed(source)
        parser.close()
    except Exception as exc:  # HTMLParser can surface malformed declarations as parser errors.
        raise TimelineAuditError(f"could not parse HTML: {exc}") from exc
    return parser.elements


def build_report(path: Path, inventory: list[dict[str, Any]], findings: list[Finding], warnings_as_errors: bool) -> dict[str, Any]:
    error_count = sum(1 for finding in findings if finding.severity == "error")
    warning_count = sum(1 for finding in findings if finding.severity == "warning")
    status = "fail" if error_count or (warnings_as_errors and warning_count) else "pass"
    return {
        "status": status,
        "input": str(path),
        "summary": {
            "timed_element_count": len(inventory),
            "error_count": error_count,
            "warning_count": warning_count,
            "warnings_as_errors": warnings_as_errors,
        },
        "inventory": inventory,
        "findings": [finding.to_json() for finding in findings],
    }


def build_failure_report(path: Path | None, message: str, warnings_as_errors: bool = False) -> dict[str, Any]:
    return {
        "status": "error",
        "input": str(path) if path else None,
        "summary": {"timed_element_count": 0, "error_count": 1, "warning_count": 0, "warnings_as_errors": warnings_as_errors},
        "inventory": [],
        "findings": [
            {
                "severity": "error",
                "code": "operational-failure",
                "element": None,
                "location": None,
                "message": message,
            }
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = JsonArgumentParser(
        description="Static HyperFrames timeline preflight for local composition HTML.",
    )
    parser.add_argument("html", type=Path, help="Local HyperFrames composition HTML file to audit.")
    parser.add_argument("--duration", type=float, help="Optional composition duration in seconds; elements may not end beyond it.")
    parser.add_argument("--fps", type=float, help="Optional fps for frame-boundary alignment checks.")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-6,
        help="Frame-position tolerance for --fps alignment checks (default: 1e-6 frames).",
    )
    parser.add_argument("--warnings-as-errors", action="store_true", help="Exit 2 when warnings are present.")
    args = parser.parse_args(argv)

    if args.duration is not None and (not math.isfinite(args.duration) or args.duration < 0):
        parser.error("--duration must be a finite nonnegative number")
    if args.fps is not None and (not math.isfinite(args.fps) or args.fps <= 0):
        parser.error("--fps must be a finite positive number")
    if not math.isfinite(args.tolerance) or args.tolerance < 0:
        parser.error("--tolerance must be a finite nonnegative number")
    return args


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(sys.argv[1:] if argv is None else argv)
    except CliUsageError as exc:
        print(json.dumps(build_failure_report(None, str(exc)), indent=2, sort_keys=True), file=sys.stderr)
        return EXIT_OPERATIONAL_FAILURE

    try:
        source = load_html(args.html)
        elements = parse_html(source)
        inventory, findings = audit_elements(elements, duration=args.duration, fps=args.fps, tolerance=args.tolerance)
        report = build_report(args.html, inventory, findings, args.warnings_as_errors)
    except TimelineAuditError as exc:
        report = build_failure_report(args.html, str(exc), args.warnings_as_errors)
        print(json.dumps(report, indent=2, sort_keys=True), file=sys.stderr)
        return EXIT_OPERATIONAL_FAILURE

    print(json.dumps(report, indent=2, sort_keys=True))
    if report["summary"]["error_count"] or (args.warnings_as_errors and report["summary"]["warning_count"]):
        return EXIT_STATIC_FINDINGS
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
