import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "normalize_qa_report.py"
SPEC = importlib.util.spec_from_file_location("normalize_qa_report", SCRIPT_PATH)
normalize_qa_report = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(normalize_qa_report)


def base_report():
    return {
        "asset_id": "asset-001",
        "review": {
            "reviewer": "QA Agent",
            "date": "2026-07-11T12:00:00Z",
            "target_platform": "Instagram Reels",
            "intended_use": "draft review",
            "source_package": "package-v1",
        },
        "policy": {
            "dispositions": {
                "critical": "reject",
                "major": "hold",
                "minor": "ready",
                "observation": "ready",
            },
            "waivable_severities": ["major"],
            "non_waivable_areas": ["rights", "accessibility", "safety", "policy"],
        },
        "checks": [
            {
                "id": "dimensions",
                "status": "pass",
                "evidence_type": "empirical_observation",
                "evidence_detail": "Measured 1080x1920 in delivery metadata.",
            }
        ],
        "findings": [],
    }


class NormalizeQaReportTests(unittest.TestCase):
    def test_ready_report_exits_zero(self):
        output, exit_code = normalize_qa_report.normalize_report(base_report())

        self.assertEqual(exit_code, 0)
        self.assertEqual(output["summary"]["disposition"], "ready")
        self.assertFalse(output["summary"]["final_approval"])
        self.assertEqual(output["schema_validation_findings"], [])

    def test_major_finding_holds_and_preserves_evidence_type(self):
        report = base_report()
        report["findings"] = [
            {
                "id": "caption-late",
                "severity": "major",
                "area": "captions",
                "issue": "Caption appears late over the CTA.",
                "evidence_type": "empirical_observation",
                "evidence_detail": "Manual playback shows the final caption starts after speech ends.",
                "timecode": "00:13.200",
            }
        ]

        output, exit_code = normalize_qa_report.normalize_report(report)

        self.assertEqual(exit_code, 2)
        self.assertEqual(output["summary"]["disposition"], "hold")
        self.assertEqual(output["summary"]["severity_counts"]["major"], 1)
        self.assertEqual(output["findings"][0]["evidence_type"], "empirical_observation")

    def test_critical_finding_rejects(self):
        report = base_report()
        report["findings"] = [
            {
                "severity": "critical",
                "area": "policy",
                "issue": "Platform-required synthetic disclosure is missing.",
                "evidence_type": "documented_fact",
                "evidence_detail": "Client policy requires disclosure for realistic synthetic people.",
                "region": "end card",
            }
        ]

        output, exit_code = normalize_qa_report.normalize_report(report)

        self.assertEqual(exit_code, 2)
        self.assertEqual(output["summary"]["disposition"], "reject")

    def test_allowed_major_waiver_can_ready_non_protected_area(self):
        report = base_report()
        report["findings"] = [
            {
                "severity": "major",
                "area": "visual",
                "issue": "Background matte edge is visible on pause.",
                "evidence_type": "empirical_observation",
                "evidence_detail": "Visible around background plant only when paused at target resolution.",
                "timecode": "00:04.000",
                "waiver": {
                    "owner": "Creative Director",
                    "reference": "QA-1234",
                    "reason": "Accepted for internal-only review cut.",
                },
            }
        ]

        output, exit_code = normalize_qa_report.normalize_report(report)

        self.assertEqual(exit_code, 0)
        self.assertEqual(output["summary"]["disposition"], "ready")

    def test_safety_waiver_is_validation_finding_and_hold(self):
        report = base_report()
        report["findings"] = [
            {
                "severity": "major",
                "area": "safety",
                "issue": "Fast red flashes need review.",
                "evidence_type": "empirical_observation",
                "evidence_detail": "Three high-contrast flashes observed in the end transition.",
                "timecode": "00:10.000",
                "waiver": {
                    "owner": "Producer",
                    "reference": "QA-5678",
                },
            }
        ]

        output, exit_code = normalize_qa_report.normalize_report(report)

        self.assertEqual(exit_code, 2)
        self.assertEqual(output["summary"]["disposition"], "hold")
        messages = [finding["message"] for finding in output["schema_validation_findings"]]
        self.assertIn("rights, accessibility, safety, and policy findings cannot be waived", messages)

    def test_schema_findings_hold_even_without_qa_findings(self):
        report = base_report()
        del report["policy"]
        report["checks"][0]["status"] = "maybe"
        del report["checks"][0]["evidence_type"]

        output, exit_code = normalize_qa_report.normalize_report(report)

        self.assertEqual(exit_code, 2)
        self.assertEqual(output["summary"]["disposition"], "hold")
        paths = [finding["path"] for finding in output["schema_validation_findings"]]
        self.assertIn("policy", paths)
        self.assertIn("checks[0].status", paths)
        self.assertIn("checks[0].evidence_type", paths)

    def test_cli_policy_override_accepts_nested_policy_object(self):
        report = base_report()
        del report["policy"]
        policy_override = {
            "dispositions": {
                "critical": "reject",
                "major": "hold",
                "minor": "ready",
                "observation": "ready",
            },
            "waivable_severities": ["major"],
            "non_waivable_areas": ["rights", "accessibility", "safety", "policy"],
        }

        output, exit_code = normalize_qa_report.normalize_report(report, policy_override)

        self.assertEqual(exit_code, 0)
        self.assertEqual(output["summary"]["disposition"], "ready")
        self.assertEqual(output["schema_validation_findings"], [])


if __name__ == "__main__":
    unittest.main()