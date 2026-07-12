#!/usr/bin/env python3
"""Verify GNU-style SHA-256 manifests for delivery packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath


EXIT_VALID = 0
EXIT_VERIFICATION_FAILURE = 2
EXIT_OPERATIONAL_FAILURE = 3

LINE_PATTERN = re.compile(r"^([0-9A-Fa-f]{64})  (.+)$")
BUFFER_SIZE = 1024 * 1024
O_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)


class ManifestError(Exception):
    """Raised for parse, operational, or package-shape failures."""


@dataclass(frozen=True)
class ManifestEntry:
    line: int
    checksum: str
    manifest_path: str
    file_path: Path


def _json_result(status: str, root: Path | None, manifest: Path | None, **fields: object) -> dict[str, object]:
    result: dict[str, object] = {
        "status": status,
        "root": str(root) if root is not None else None,
        "manifest": str(manifest) if manifest is not None else None,
    }
    result.update(fields)
    return result


def _write_json(result: dict[str, object]) -> None:
    print(json.dumps(result, indent=2, sort_keys=True))


def _is_relative_posix_path(value: str) -> bool:
    if not value or value.strip() != value:
        return False
    if "\x00" in value or "\\" in value:
        return False
    posix_path = PurePosixPath(value)
    windows_path = PureWindowsPath(value)
    if posix_path.is_absolute() or windows_path.is_absolute() or windows_path.drive or windows_path.root:
        return False
    if any(part in {"", ".", ".."} for part in posix_path.parts):
        return False
    return True


def _resolve_under_root(root: Path, manifest_path: str, line_number: int) -> Path:
    if not _is_relative_posix_path(manifest_path):
        raise ManifestError(f"line {line_number}: unsafe relative path {manifest_path!r}")

    candidate = root.joinpath(*PurePosixPath(manifest_path).parts)
    try:
        lexical_candidate = candidate.absolute()
    except OSError as exc:
        raise ManifestError(f"line {line_number}: cannot resolve {manifest_path!r}: {exc}") from exc

    if not _is_under_root(root, lexical_candidate):
        raise ManifestError(f"line {line_number}: path escapes root {manifest_path!r}")
    return candidate


def _is_under_root(root: Path, path: Path) -> bool:
    try:
        os.path.commonpath([str(root), str(path)])
    except ValueError:
        return False
    return os.path.commonpath([str(root), str(path)]) == str(root)


def _parse_manifest(root: Path, manifest: Path) -> list[ManifestEntry]:
    entries: list[ManifestEntry] = []
    seen_paths: set[str] = set()

    try:
        with _open_regular_no_follow(manifest, "r", encoding="utf-8", newline=None) as manifest_file:
            for line_number, raw_line in enumerate(manifest_file, start=1):
                line = raw_line.rstrip("\r\n")
                if not line:
                    raise ManifestError(f"line {line_number}: empty lines are not valid manifest entries")
                match = LINE_PATTERN.fullmatch(line)
                if match is None:
                    raise ManifestError(
                        f"line {line_number}: expected '<64hex><two spaces><relative path>'"
                    )
                checksum, manifest_path = match.groups()
                if manifest_path in seen_paths:
                    raise ManifestError(f"line {line_number}: duplicate manifest entry {manifest_path!r}")
                seen_paths.add(manifest_path)

                file_path = _resolve_under_root(root, manifest_path, line_number)
                if file_path.resolve(strict=False) == manifest:
                    raise ManifestError(f"line {line_number}: manifest must not include itself")
                entries.append(
                    ManifestEntry(
                        line=line_number,
                        checksum=checksum.lower(),
                        manifest_path=manifest_path,
                        file_path=file_path,
                    )
                )
    except UnicodeDecodeError as exc:
        raise ManifestError(f"manifest is not valid UTF-8: {exc}") from exc
    except OSError as exc:
        raise ManifestError(f"cannot read manifest: {exc}") from exc

    if not entries:
        raise ManifestError("manifest contains no entries")
    return entries


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with _open_regular_no_follow(path, "rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(BUFFER_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _open_regular_no_follow(path: Path, mode: str, **kwargs: object):
    if "r" not in mode or any(flag in mode for flag in "+wax"):
        raise ValueError("_open_regular_no_follow only supports read modes")
    if os.name == "nt" or O_NOFOLLOW == 0:
        if path.is_symlink() or not path.is_file():
            raise OSError(f"not a regular file: {path}")
        return path.open(mode, **kwargs)

    flags = os.O_RDONLY | O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    fd = os.open(path, flags)
    try:
        stat_result = os.fstat(fd)
        if not stat.S_ISREG(stat_result.st_mode):
            raise OSError(f"not a regular file: {path}")
        return os.fdopen(fd, mode, **kwargs)
    except Exception:
        os.close(fd)
        raise


def _verify_entries(root: Path, entries: list[ManifestEntry]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    verified: list[dict[str, object]] = []
    failures: list[dict[str, object]] = []

    for entry in entries:
        resolved_path = entry.file_path.resolve(strict=False)
        if not _is_under_root(root, resolved_path):
            failures.append(_failure(entry, "symlink_escape", "path resolves outside root"))
            continue
        if not entry.file_path.exists():
            failures.append(_failure(entry, "missing", "file is listed but does not exist"))
            continue
        if entry.file_path.is_symlink():
            failures.append(_failure(entry, "symlink", "manifest entries must resolve to regular files, not symlinks"))
            continue
        if not entry.file_path.is_file():
            failures.append(_failure(entry, "not_regular_file", "manifest entry is not a regular file"))
            continue

        try:
            actual = _hash_file(entry.file_path)
        except OSError as exc:
            failures.append(_failure(entry, "read_error", f"could not safely read file: {exc}"))
            continue
        if actual != entry.checksum:
            failure = _failure(entry, "mismatch", "SHA-256 digest does not match manifest")
            failure["expected_sha256"] = entry.checksum
            failure["actual_sha256"] = actual
            failures.append(failure)
            continue

        verified.append({"path": entry.manifest_path, "sha256": actual})

    return verified, failures


def _failure(entry: ManifestEntry, code: str, message: str) -> dict[str, object]:
    return {"code": code, "line": entry.line, "message": message, "path": entry.manifest_path}


def _relative_payload_files(root: Path, manifest: Path) -> list[str]:
    root = root.resolve(strict=True)
    manifest = manifest.resolve(strict=True)
    payload_files: list[str] = []

    for directory, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        dirnames[:] = sorted(dirname for dirname in dirnames if dirname not in {".git", "__pycache__"})
        for filename in sorted(filenames):
            candidate = Path(directory) / filename
            if candidate.is_symlink() or not candidate.is_file():
                continue
            if candidate.resolve(strict=True) == manifest:
                continue
            relative = candidate.relative_to(root).as_posix()
            if _is_excluded_payload_file(relative):
                continue
            payload_files.append(relative)
    return payload_files


def _is_excluded_payload_file(relative_path: str) -> bool:
    name = PurePosixPath(relative_path).name
    return name.startswith("manifest-") and name.endswith(".txt")


def verify_manifest(root_arg: str, manifest_arg: str, require_all_files: bool) -> tuple[int, dict[str, object]]:
    root = Path(root_arg).resolve(strict=True)
    if not root.is_dir():
        raise ManifestError("root must be an existing directory")

    manifest_input = Path(manifest_arg)
    manifest = manifest_input if manifest_input.is_absolute() else root / manifest_input
    manifest = manifest.resolve(strict=True)
    if not _is_under_root(root, manifest):
        raise ManifestError("manifest must be inside root")
    if not manifest.is_file() or manifest.is_symlink():
        raise ManifestError("manifest must be a regular file inside root")

    entries = _parse_manifest(root, manifest)
    verified, failures = _verify_entries(root, entries)

    listed_paths = {entry.manifest_path for entry in entries}
    unlisted: list[str] = []
    if require_all_files:
        unlisted = [path for path in _relative_payload_files(root, manifest) if path not in listed_paths]
        for path in unlisted:
            failures.append(
                {
                    "code": "unlisted",
                    "line": None,
                    "message": "regular payload file is not listed in manifest",
                    "path": path,
                }
            )

    status = "valid" if not failures else "verification_failed"
    exit_code = EXIT_VALID if not failures else EXIT_VERIFICATION_FAILURE
    return exit_code, _json_result(
        status,
        root,
        manifest,
        counts={
            "entries": len(entries),
            "failures": len(failures),
            "unlisted": len(unlisted),
            "verified": len(verified),
        },
        failures=failures,
        unlisted=unlisted,
        verified=verified,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify a GNU-style SHA-256 manifest against files under a package root."
    )
    parser.add_argument("root", help="Package root directory")
    parser.add_argument("manifest", help="Manifest path, absolute or relative to root")
    parser.add_argument(
        "--require-all-files",
        action="store_true",
        help="Report unlisted regular payload files under root, excluding manifests and common tool directories.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    root_for_error: Path | None = None
    manifest_for_error: Path | None = None
    try:
        root_for_error = Path(args.root).resolve(strict=False)
        manifest_input = Path(args.manifest)
        manifest_for_error = manifest_input if manifest_input.is_absolute() else root_for_error / manifest_input
        exit_code, result = verify_manifest(args.root, args.manifest, args.require_all_files)
    except (ManifestError, OSError) as exc:
        _write_json(
            _json_result(
                "error",
                root_for_error,
                manifest_for_error,
                error={"code": "operational_or_parse_error", "message": str(exc)},
            )
        )
        return EXIT_OPERATIONAL_FAILURE

    _write_json(result)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())