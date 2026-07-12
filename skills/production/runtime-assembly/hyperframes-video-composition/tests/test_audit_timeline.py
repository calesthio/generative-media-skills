import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SKILL = ROOT / "skills" / "production" / "runtime-assembly" / "hyperframes-video-composition"
SCRIPT = SKILL / "scripts" / "audit_timeline.py"
FIXTURES = SKILL / "tests" / "fixtures"


class AuditTimelineCliTests(unittest.TestCase):
    def run_audit(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_valid_fixture_exits_zero_with_stable_inventory(self):
        result = self.run_audit(str(FIXTURES / "valid_composition.html"), "--duration", "2", "--fps", "30")

        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["summary"]["error_count"], 0)
        self.assertEqual(report["summary"]["warning_count"], 0)
        self.assertEqual(report["summary"]["timed_element_count"], 5)
        self.assertEqual(report["findings"], [])
        self.assertEqual([item["element"] for item in report["inventory"]], ["main#stage", "section#scene-01", "h1#headline", "video#hero-video", "audio#music"])

    def test_invalid_fixture_reports_static_errors_and_frame_warnings(self):
        result = self.run_audit(str(FIXTURES / "invalid_composition.html"), "--duration", "4", "--fps", "30")

        self.assertEqual(result.returncode, 2)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "fail")
        codes = {finding["code"] for finding in report["findings"]}
        self.assertIn("duplicate-id", codes)
        self.assertIn("missing-clip-class", codes)
        self.assertIn("invalid-start", codes)
        self.assertIn("invalid-duration", codes)
        self.assertIn("invalid-track-index", codes)
        self.assertIn("missing-track-index", codes)
        self.assertIn("end-beyond-duration", codes)
        self.assertIn("frame-boundary-start", codes)
        self.assertGreaterEqual(report["summary"]["error_count"], 7)
        self.assertGreaterEqual(report["summary"]["warning_count"], 1)

    def test_warnings_as_errors_exits_two_for_alignment_only(self):
        result = self.run_audit(str(FIXTURES / "valid_composition.html"), "--duration", "2", "--fps", "25", "--warnings-as-errors")

        self.assertEqual(result.returncode, 2)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "fail")
        self.assertEqual(report["summary"]["error_count"], 0)
        self.assertGreater(report["summary"]["warning_count"], 0)

    def test_missing_input_is_operational_failure_on_stderr(self):
        result = self.run_audit(str(FIXTURES / "missing.html"))

        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, "")
        report = json.loads(result.stderr)
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["findings"][0]["code"], "operational-failure")

    def test_invalid_arguments_are_operational_failures_not_static_findings(self):
        result = self.run_audit(str(FIXTURES / "valid_composition.html"), "--fps", "0")

        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, "")
        report = json.loads(result.stderr)
        self.assertEqual(report["status"], "error")
        self.assertIn("--fps", report["findings"][0]["message"])


if __name__ == "__main__":
    unittest.main()
