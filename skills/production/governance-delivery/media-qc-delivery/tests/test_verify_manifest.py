from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_manifest.py"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_lf(path: Path, value: str) -> None:
    path.write_bytes(value.encode("utf-8"))


class VerifyManifestTests(unittest.TestCase):
    def run_cli(self, root: Path, manifest: str = "manifest-sha256.txt", *args: str) -> tuple[int, dict[str, object]]:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(root), manifest, *args],
            check=False,
            capture_output=True,
            text=True,
        )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            self.fail(f"CLI did not emit JSON. stdout={completed.stdout!r} stderr={completed.stderr!r}: {exc}")
        return completed.returncode, payload

    def write_package(self, root: Path) -> None:
        (root / "platform").mkdir()
        (root / "captions").mkdir()
        write_lf(root / "platform" / "spot.txt", "approved spot\n")
        write_lf(root / "captions" / "spot.vtt", "WEBVTT\n")
        write_lf(
            root / "manifest-sha256.txt",
            f"{sha256_text('WEBVTT\n')}  captions/spot.vtt\n"
            f"{sha256_text('approved spot\n')}  platform/spot.txt\n",
        )

    def test_valid_manifest_returns_verified_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_package(root)

            code, payload = self.run_cli(root)

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["counts"]["verified"], 2)
        self.assertEqual(payload["failures"], [])
        self.assertEqual([item["path"] for item in payload["verified"]], ["captions/spot.vtt", "platform/spot.txt"])

    def test_mismatch_is_verification_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_package(root)
            write_lf(root / "platform" / "spot.txt", "corrupt\n")

            code, payload = self.run_cli(root)

        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "verification_failed")
        self.assertEqual(payload["failures"][0]["code"], "mismatch")

    def test_missing_is_verification_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_package(root)
            (root / "captions" / "spot.vtt").unlink()

            code, payload = self.run_cli(root)

        self.assertEqual(code, 2)
        self.assertEqual(payload["failures"][0]["code"], "missing")

    def test_require_all_files_reports_unlisted_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write_package(root)
            write_lf(root / "delivery-notes.md", "notes\n")

            code, payload = self.run_cli(root, "manifest-sha256.txt", "--require-all-files")

        self.assertEqual(code, 2)
        self.assertEqual(payload["unlisted"], ["delivery-notes.md"])
        self.assertEqual(payload["failures"][-1]["code"], "unlisted")

    def test_malformed_line_is_parse_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_lf(root / "manifest-sha256.txt", f"{sha256_text('x')} platform/spot.txt\n")

            code, payload = self.run_cli(root)

        self.assertEqual(code, 3)
        self.assertEqual(payload["status"], "error")
        self.assertIn("expected", payload["error"]["message"])

    def test_absolute_path_is_parse_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_lf(root / "manifest-sha256.txt", f"{sha256_text('x')}  /tmp/file.txt\n")

            code, payload = self.run_cli(root)

        self.assertEqual(code, 3)
        self.assertIn("unsafe relative path", payload["error"]["message"])

    def test_traversal_is_parse_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_lf(root / "manifest-sha256.txt", f"{sha256_text('x')}  data/../file.txt\n")

            code, payload = self.run_cli(root)

        self.assertEqual(code, 3)
        self.assertIn("unsafe relative path", payload["error"]["message"])

    def test_duplicate_entry_is_parse_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            checksum = sha256_text("x")
            write_lf(
                root / "manifest-sha256.txt",
                f"{checksum}  data/file.txt\n{checksum}  data/file.txt\n",
            )

            code, payload = self.run_cli(root)

        self.assertEqual(code, 3)
        self.assertIn("duplicate", payload["error"]["message"])

    def test_manifest_self_inclusion_is_parse_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_lf(
                root / "manifest-sha256.txt",
                f"{sha256_text('placeholder')}  manifest-sha256.txt\n",
            )

            code, payload = self.run_cli(root)

        self.assertEqual(code, 3)
        self.assertIn("must not include itself", payload["error"]["message"])

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are not supported on this platform")
    def test_symlink_escape_is_verification_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "root"
            outside = Path(temp_dir) / "outside.txt"
            root.mkdir()
            write_lf(outside, "outside\n")
            try:
                (root / "escape.txt").symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"cannot create symlink in this environment: {exc}")
            write_lf(
                root / "manifest-sha256.txt",
                f"{sha256_text('outside\n')}  escape.txt\n",
            )

            code, payload = self.run_cli(root)

        self.assertEqual(code, 2)
        self.assertEqual(payload["failures"][0]["code"], "symlink_escape")

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are not supported on this platform")
    def test_manifest_symlink_is_operational_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "root"
            root.mkdir()
            target = Path(temp_dir) / "manifest-sha256.txt"
            write_lf(target, f"{sha256_text('x')}  file.txt\n")
            try:
                (root / "manifest-sha256.txt").symlink_to(target)
            except OSError as exc:
                self.skipTest(f"cannot create symlink in this environment: {exc}")

            code, payload = self.run_cli(root)

        self.assertEqual(code, 3)
        self.assertIn("manifest must be a regular file", payload["error"]["message"])


if __name__ == "__main__":
    unittest.main()