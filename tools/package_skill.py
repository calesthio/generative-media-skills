#!/usr/bin/env python3
"""Package an Agent Skill leaf directory for publication."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence


EXIT_OK = 0
EXIT_VALIDATION_ERROR = 2
EXIT_OUTPUT_EXISTS = 3
EXIT_IO_ERROR = 4

APPROVED_TOP_LEVEL_DIRS = {"assets", "references", "scripts"}
EXCLUDED_NAMES = {"EVAL.md", "tests", "test", "demos", "demo", "__pycache__"}
SECRET_NAME_RE = re.compile(r"(secret|token|credential|credentials|apikey|api-key|private[_-]?key)", re.IGNORECASE)
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PYC_SUFFIXES = {".pyc", ".pyo"}
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ZIP_FILE_MODE = 0o644
MAX_SKILL_NAME_LENGTH = 64
MAX_SKILL_DESCRIPTION_LENGTH = 1024


class PackageSkillError(Exception):
    """Base class for expected packaging failures."""

    exit_code = EXIT_VALIDATION_ERROR


class ValidationError(PackageSkillError):
    """Input skill directory is invalid."""


class OutputExistsError(PackageSkillError):
    """Output exists and overwrite was not requested."""

    exit_code = EXIT_OUTPUT_EXISTS


class PackageIOError(PackageSkillError):
    """A filesystem operation failed while writing output."""

    exit_code = EXIT_IO_ERROR



@dataclass(frozen=True)
class PlannedFile:
    source: Path
    archive_path: str
    size: int


@dataclass(frozen=True)
class PackagePlan:
    source: Path
    output: Path
    output_kind: str
    files: tuple[PlannedFile, ...]
    dry_run: bool = False

    def summary(self) -> dict[str, object]:
        return {
            "dry_run": self.dry_run,
            "file_count": len(self.files),
            "files": [file.archive_path for file in self.files],
            "output": str(self.output),
            "output_kind": self.output_kind,
            "source": str(self.source),
        }


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _read_frontmatter(skill_md: Path) -> dict[str, str]:
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValidationError(f"cannot read {skill_md}: {exc}") from exc

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValidationError("SKILL.md must start with YAML frontmatter delimited by ---")

    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"\'')

    raise ValidationError("SKILL.md frontmatter is missing closing --- delimiter")


def validate_skill_source(source: Path) -> Path:
    root = source.resolve(strict=True)
    if not root.is_dir():
        raise ValidationError(f"source is not a directory: {source}")

    skill_md = root / "SKILL.md"
    eval_md = root / "EVAL.md"
    if not skill_md.is_file():
        raise ValidationError("source leaf must contain SKILL.md")
    if not eval_md.is_file():
        raise ValidationError("authoring source leaf must contain EVAL.md")

    metadata = _read_frontmatter(skill_md)
    name = metadata.get("name")
    if not name:
        raise ValidationError("SKILL.md frontmatter must include name")
    if len(name) > MAX_SKILL_NAME_LENGTH:
        raise ValidationError(f"SKILL.md frontmatter name must be at most {MAX_SKILL_NAME_LENGTH} characters")
    if not SKILL_NAME_RE.fullmatch(name):
        raise ValidationError("SKILL.md frontmatter name must be lowercase kebab-case")
    if name != root.name:
        raise ValidationError(f"SKILL.md frontmatter name {name!r} must match directory {root.name!r}")
    description = metadata.get("description")
    if not description or not description.strip():
        raise ValidationError("SKILL.md frontmatter must include description")
    if len(description) > MAX_SKILL_DESCRIPTION_LENGTH:
        raise ValidationError(f"SKILL.md frontmatter description must be at most {MAX_SKILL_DESCRIPTION_LENGTH} characters")

    return root


def _validate_output(root: Path, output: Path, overwrite: bool) -> Path:
    resolved_parent = output.parent.resolve(strict=False)
    resolved = resolved_parent / output.name
    if resolved.exists() and not overwrite:
        raise OutputExistsError(f"output already exists: {resolved}")
    _validate_output_target_safety(root, resolved)
    return resolved


def _validate_output_target_safety(root: Path, output: Path) -> None:
    source_real = root.resolve(strict=True)
    if output == source_real:
        raise ValidationError("output must not replace the source skill directory")
    if _is_relative_to(output, source_real):
        raise ValidationError("output must not be inside the source skill directory")
    if _is_relative_to(source_real, output):
        raise ValidationError("output must not be an ancestor of the source skill directory")
    if output.exists():
        if output.is_symlink():
            raise ValidationError("output must not be a symlink")
        output_real = output.resolve(strict=True)
        if output_real == source_real or _is_relative_to(output_real, source_real) or _is_relative_to(source_real, output_real):
            raise ValidationError("output must not overlap the source skill directory")
    if output.parent.exists() and output.parent.is_symlink():
        raise ValidationError("output parent must not be a symlink")


def _is_excluded_name(name: str) -> bool:
    return (
        name.startswith(".")
        or name in EXCLUDED_NAMES
        or name.endswith("~")
        or SECRET_NAME_RE.search(name) is not None
        or Path(name).suffix in PYC_SUFFIXES
    )


def _is_ignored_name(name: str) -> bool:
    return name.startswith(".") or name in EXCLUDED_NAMES or name.endswith("~") or Path(name).suffix in PYC_SUFFIXES


def _is_secret_like_name(name: str) -> bool:
    return SECRET_NAME_RE.search(name) is not None


def _require_safe_source_path(path: Path, root: Path) -> None:
    if path.is_symlink():
        try:
            target = path.resolve(strict=True)
        except OSError as exc:
            raise ValidationError(f"broken symlink is not publishable: {path.relative_to(root)}") from exc
        if not _is_relative_to(target, root):
            raise ValidationError(f"symlink escapes source: {path.relative_to(root)}")
        raise ValidationError(f"symlinks are not publishable: {path.relative_to(root)}")


def _iter_publishable_files(root: Path) -> Iterable[PlannedFile]:
    skill_md = root / "SKILL.md"
    yield PlannedFile(skill_md, "SKILL.md", skill_md.stat().st_size)

    for dirname in sorted(APPROVED_TOP_LEVEL_DIRS):
        directory = root / dirname
        if not directory.exists():
            continue
        _require_safe_source_path(directory, root)
        if not directory.is_dir():
            raise ValidationError(f"approved item is not a directory: {dirname}")

        for current_root, dirnames, filenames in os.walk(directory, topdown=True, followlinks=False):
            current = Path(current_root)
            safe_dirnames = []
            for child_dirname in sorted(dirnames):
                child = current / child_dirname
                _require_safe_source_path(child, root)
                if _is_secret_like_name(child_dirname):
                    raise ValidationError(f"secret-like item in publishable directory is not allowed: {child.relative_to(root)}")
                if not _is_excluded_name(child_dirname):
                    safe_dirnames.append(child_dirname)
            dirnames[:] = safe_dirnames

            for filename in sorted(filenames):
                if _is_secret_like_name(filename):
                    raise ValidationError(f"secret-like file in publishable directory is not allowed: {(current / filename).relative_to(root)}")
                if _is_ignored_name(filename):
                    continue
                file_path = current / filename
                _require_safe_source_path(file_path, root)
                if not file_path.is_file():
                    continue
                archive_path = PurePosixPath(file_path.relative_to(root).as_posix()).as_posix()
                yield PlannedFile(file_path, archive_path, file_path.stat().st_size)


def _find_unknown_top_level_items(root: Path) -> list[str]:
    allowed = {"SKILL.md", "EVAL.md", *APPROVED_TOP_LEVEL_DIRS}
    unknown = []
    for item in root.iterdir():
        if item.name in allowed:
            continue
        if _is_secret_like_name(item.name):
            raise ValidationError(f"secret-like top-level item is not allowed: {item.name}")
        if _is_excluded_name(item.name):
            continue
        unknown.append(item.name)
    return sorted(unknown)


def build_plan(source: Path, output: Path, output_kind: str, overwrite: bool = False, dry_run: bool = False) -> PackagePlan:
    root = validate_skill_source(source)
    unknown = _find_unknown_top_level_items(root)
    if unknown:
        raise ValidationError(f"unknown top-level item(s) are not publishable: {', '.join(unknown)}")

    resolved_output = _validate_output(root, output, overwrite)

    files = tuple(_iter_publishable_files(root))
    return PackagePlan(root, resolved_output, output_kind, files, dry_run=dry_run)


def _prepare_output_path(path: Path, overwrite: bool) -> Path | None:
    if not path.exists():
        return None
    if not overwrite:
        raise OutputExistsError(f"output already exists: {path}")
    if path.is_symlink():
        raise ValidationError("output must not be a symlink")
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_parent = Path(tempfile.mkdtemp(prefix=f".{path.name}.old-", dir=path.parent))
    backup_target = backup_parent / path.name
    try:
        path.replace(backup_target)
    except OSError as exc:
        shutil.rmtree(backup_parent, ignore_errors=True)
        raise PackageIOError(f"failed to stage existing output for replacement: {exc}") from exc
    return backup_parent


def _cleanup_backup(path: Path | None) -> None:
    if path is not None:
        shutil.rmtree(path, ignore_errors=True)


def _safe_output_temp_path(output: Path, suffix: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{output.name}.", suffix=suffix, dir=output.parent)
    os.close(fd)
    temp_path = Path(temp_name)
    temp_path.unlink()
    return temp_path


def _read_regular_file_no_follow(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise OSError(f"not a regular file: {path}")
    return path.read_bytes()


def write_directory(plan: PackagePlan, overwrite: bool = False) -> None:
    backup = _prepare_output_path(plan.output, overwrite)
    temp_output = _safe_output_temp_path(plan.output, ".dir")
    try:
        temp_output.mkdir(parents=True, exist_ok=False)
        for file in plan.files:
            destination = temp_output / Path(file.archive_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(_read_regular_file_no_follow(file.source))
            shutil.copystat(file.source, destination, follow_symlinks=False)
        temp_output.replace(plan.output)
        _cleanup_backup(backup)
    except OSError as exc:
        if temp_output.exists():
            shutil.rmtree(temp_output, ignore_errors=True)
        raise PackageIOError(f"failed to write directory output: {exc}") from exc


def _zip_info(path: str, source: Path) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(path, ZIP_TIMESTAMP)
    info.external_attr = (stat.S_IFREG | ZIP_FILE_MODE) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def write_zip(plan: PackagePlan, overwrite: bool = False) -> None:
    backup = _prepare_output_path(plan.output, overwrite)
    temp_path: Path | None = None
    try:
        plan.output.parent.mkdir(parents=True, exist_ok=True)
        temp_path = _safe_output_temp_path(plan.output, ".tmp")
        with zipfile.ZipFile(temp_path, "w") as archive:
            for file in plan.files:
                info = _zip_info(file.archive_path, file.source)
                archive.writestr(info, _read_regular_file_no_follow(file.source))
        temp_path.replace(plan.output)
        _cleanup_backup(backup)
    except OSError as exc:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise PackageIOError(f"failed to write zip output: {exc}") from exc


def package_skill(source: Path, output: Path, output_kind: str, overwrite: bool = False, dry_run: bool = False) -> PackagePlan:
    plan = build_plan(source, output, output_kind, overwrite=overwrite, dry_run=dry_run)
    if dry_run:
        return plan
    if output_kind == "dir":
        write_directory(plan, overwrite=overwrite)
    elif output_kind == "zip":
        write_zip(plan, overwrite=overwrite)
    else:
        raise ValidationError(f"unsupported output kind: {output_kind}")
    return plan


def _json_dump(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, sort_keys=True)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Package an Agent Skill leaf directory for publication.")
    parser.add_argument("source", type=Path, help="Leaf skill source directory containing SKILL.md and EVAL.md.")
    parser.add_argument("output", type=Path, help="Output directory or zip path.")
    parser.add_argument("--format", choices=("dir", "zip"), default=None, help="Output format. Defaults to zip for .zip outputs, otherwise dir.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing output path.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the publishable file list without writing output.")
    parser.add_argument("--list", action="store_true", help="Alias for --dry-run focused on the file list.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    output_kind = args.format or ("zip" if args.output.suffix.lower() == ".zip" else "dir")
    dry_run = args.dry_run or args.list

    try:
        plan = package_skill(args.source, args.output, output_kind, overwrite=args.overwrite, dry_run=dry_run)
    except PackageSkillError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return exc.exit_code

    print(_json_dump(plan.summary()))
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())