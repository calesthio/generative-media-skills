import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import package_skill


class PackageSkillTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def make_skill(self, name="sample-skill"):
        root = self.workspace / name
        root.mkdir()
        (root / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Demo skill for tests.\n---\n\nUse this skill.\n",
            encoding="utf-8",
        )
        (root / "EVAL.md").write_text("# Evaluation only\n", encoding="utf-8")
        return root

    def package_dir(self, skill, output=None, overwrite=False, dry_run=False):
        return package_skill.package_skill(
            skill,
            output or (self.workspace / "published"),
            "dir",
            overwrite=overwrite,
            dry_run=dry_run,
        )

    def test_directory_package_includes_only_skill_and_publishable_dirs(self):
        skill = self.make_skill()
        (skill / "scripts").mkdir()
        (skill / "scripts" / "helper.py").write_text("print('ok')\n", encoding="utf-8")
        (skill / "tests").mkdir()
        (skill / "tests" / "test_helper.py").write_text("raise AssertionError\n", encoding="utf-8")
        (skill / ".hidden").write_text("hidden\n", encoding="utf-8")

        plan = self.package_dir(skill)

        self.assertEqual([file.archive_path for file in plan.files], ["SKILL.md", "scripts/helper.py"])
        self.assertTrue((self.workspace / "published" / "SKILL.md").is_file())
        self.assertTrue((self.workspace / "published" / "scripts" / "helper.py").is_file())
        self.assertFalse((self.workspace / "published" / "EVAL.md").exists())
        self.assertFalse((self.workspace / "published" / "tests").exists())
        self.assertFalse((self.workspace / "published" / ".hidden").exists())

    def test_validation_requires_skill_and_eval(self):
        skill = self.make_skill()
        (skill / "EVAL.md").unlink()

        with self.assertRaisesRegex(package_skill.ValidationError, "EVAL.md"):
            self.package_dir(skill)

    def test_validation_requires_name_to_match_directory(self):
        skill = self.make_skill("actual-name")
        (skill / "SKILL.md").write_text(
            "---\nname: other-name\ndescription: Demo.\n---\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(package_skill.ValidationError, "must match"):
            self.package_dir(skill)

    def test_validation_requires_kebab_case_name_and_description(self):
        skill = self.make_skill("actual-name")
        (skill / "SKILL.md").write_text(
            "---\nname: Actual Name\ndescription: Demo.\n---\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(package_skill.ValidationError, "kebab-case"):
            self.package_dir(skill)

        (skill / "SKILL.md").write_text(
            "---\nname: actual-name\n---\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(package_skill.ValidationError, "description"):
            self.package_dir(skill)

    def test_unknown_top_level_items_fail_closed(self):
        skill = self.make_skill()
        (skill / "notes.md").write_text("not publishable\n", encoding="utf-8")

        with self.assertRaisesRegex(package_skill.ValidationError, "unknown top-level"):
            self.package_dir(skill)

    def test_caches_are_excluded_inside_publishable_dirs(self):
        skill = self.make_skill()
        scripts = skill / "scripts"
        scripts.mkdir()
        (scripts / "ok.py").write_text("print('ok')\n", encoding="utf-8")
        (scripts / "__pycache__").mkdir()
        (scripts / "__pycache__" / "ok.pyc").write_bytes(b"cache")

        plan = self.package_dir(skill)

        self.assertEqual([file.archive_path for file in plan.files], ["SKILL.md", "scripts/ok.py"])

    def test_secret_like_files_inside_publishable_dirs_fail_closed(self):
        skill = self.make_skill()
        scripts = skill / "scripts"
        scripts.mkdir()
        (scripts / "token.txt").write_text("secret\n", encoding="utf-8")

        with self.assertRaisesRegex(package_skill.ValidationError, "secret-like"):
            self.package_dir(skill)

    @unittest.skipIf(not hasattr(Path, "symlink_to"), "symlinks are unavailable")
    def test_symlink_inside_publishable_dir_is_rejected(self):
        skill = self.make_skill()
        (skill / "scripts").mkdir()
        target = self.workspace / "outside.txt"
        target.write_text("outside\n", encoding="utf-8")
        link = skill / "scripts" / "outside.txt"
        try:
            link.symlink_to(target)
        except OSError as exc:
            self.skipTest(f"symlink creation failed: {exc}")

        with self.assertRaisesRegex(package_skill.ValidationError, "symlink"):
            self.package_dir(skill)

    def test_no_overwrite_by_default(self):
        skill = self.make_skill()
        output = self.workspace / "published"
        output.mkdir()

        with self.assertRaises(package_skill.OutputExistsError):
            self.package_dir(skill, output=output)

    def test_overwrite_replaces_existing_directory(self):
        skill = self.make_skill()
        output = self.workspace / "published"
        output.mkdir()
        (output / "old.txt").write_text("old\n", encoding="utf-8")

        self.package_dir(skill, output=output, overwrite=True)

        self.assertTrue((output / "SKILL.md").is_file())
        self.assertFalse((output / "old.txt").exists())

    def test_output_must_not_overlap_source_or_ancestor(self):
        skill = self.make_skill()

        with self.assertRaisesRegex(package_skill.ValidationError, "source skill"):
            self.package_dir(skill, output=skill, overwrite=True)

        with self.assertRaisesRegex(package_skill.ValidationError, "inside the source"):
            self.package_dir(skill, output=skill / "published", overwrite=True)

        with self.assertRaisesRegex(package_skill.ValidationError, "ancestor"):
            self.package_dir(skill, output=self.workspace, overwrite=True)

    def test_zip_output_is_deterministic_and_excludes_authoring_files(self):
        skill = self.make_skill()
        (skill / "scripts").mkdir()
        (skill / "scripts" / "helper.py").write_text("print('ok')\n", encoding="utf-8")
        first = self.workspace / "first.zip"
        second = self.workspace / "second.zip"

        package_skill.package_skill(skill, first, "zip")
        package_skill.package_skill(skill, second, "zip")

        self.assertEqual(hashlib.sha256(first.read_bytes()).hexdigest(), hashlib.sha256(second.read_bytes()).hexdigest())
        with zipfile.ZipFile(first) as archive:
            self.assertEqual(archive.namelist(), ["SKILL.md", "scripts/helper.py"])
            self.assertEqual(archive.getinfo("SKILL.md").date_time, package_skill.ZIP_TIMESTAMP)
            self.assertEqual((archive.getinfo("SKILL.md").external_attr >> 16) & 0o777, 0o644)

    def test_dry_run_does_not_write_output(self):
        skill = self.make_skill()
        output = self.workspace / "published"

        plan = self.package_dir(skill, output=output, dry_run=True)

        self.assertTrue(plan.dry_run)
        self.assertFalse(output.exists())

    def test_cli_list_outputs_stable_json(self):
        skill = self.make_skill()
        output = self.workspace / "published.zip"

        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "package_skill.py"), str(skill), str(output), "--list"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, package_skill.EXIT_OK, result.stderr)
        self.assertFalse(output.exists())
        summary = json.loads(result.stdout)
        self.assertEqual(summary["files"], ["SKILL.md"])
        self.assertEqual(summary["output_kind"], "zip")

    def test_cli_validation_error_exit_code(self):
        skill = self.make_skill()
        (skill / "SKILL.md").write_text("no frontmatter\n", encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "package_skill.py"), str(skill), str(self.workspace / "out")],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, package_skill.EXIT_VALIDATION_ERROR)
        self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()