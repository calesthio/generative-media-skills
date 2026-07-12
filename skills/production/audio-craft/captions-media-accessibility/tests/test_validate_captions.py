import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
SCRIPT = ROOT / "skills" / "production" / "audio-craft" / "captions-media-accessibility" / "scripts" / "validate_captions.py"


class ValidateCaptionsCliTests(unittest.TestCase):
    def run_validator(self, content, suffix, *args, binary=False):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / f"sample{suffix}"
            if binary:
                path.write_bytes(content)
            else:
                path.write_text(content, encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(path), *args],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)
            return completed.returncode, payload, completed.stderr

    def test_valid_srt_passes_with_stable_summary(self):
        code, payload, stderr = self.run_validator(
            "1\n00:00:00,000 --> 00:00:02,000\nHello there.\n\n"
            "2\n00:00:02,500 --> 00:00:04,000\nNext cue.\n",
            ".srt",
        )

        self.assertEqual(stderr, "")
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["summary"], {"cues": 2, "errors": 0, "files": 1, "warnings": 0})
        self.assertEqual(payload["findings"], [])

    def test_valid_webvtt_with_note_style_and_identifier_passes(self):
        code, payload, _ = self.run_validator(
            "WEBVTT\n\n"
            "NOTE Draft note\n\n"
            "STYLE\n::cue { color: white; }\n\n"
            "intro\n00:00.000 --> 00:02.000 align:start\n<v Narrator>Hello.</v>\n",
            ".vtt",
        )

        self.assertEqual(code, 0)
        self.assertEqual(payload["files"][0]["format"], "vtt")
        self.assertEqual(payload["summary"]["cues"], 1)

    def test_validation_errors_exit_two(self):
        code, payload, _ = self.run_validator(
            "1\n00:00:02,000 --> 00:00:01,000\nBackwards.\n\n"
            "2\n00:00:00,500 --> 00:00:03,000\nOverlap and out of order.\n\n"
            "3\n00:00:03,500 --> 00:00:04,000\n\n",
            ".srt",
        )

        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "failed")
        codes = [finding["code"] for finding in payload["findings"]]
        self.assertIn("time_order", codes)
        self.assertIn("cue_order", codes)
        self.assertIn("cue_overlap", codes)
        self.assertIn("cue_text_missing", codes)

    def test_readability_warnings_do_not_fail_by_default(self):
        code, payload, _ = self.run_validator(
            "1\n00:00:00,000 --> 00:00:10,000\n"
            "This caption line is deliberately longer than the configured limit.\n"
            "And this is a third line.\nThird line again.\n",
            ".srt",
            "--max-chars-per-line",
            "20",
            "--max-lines",
            "2",
        )

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "passed")
        self.assertGreaterEqual(payload["summary"]["warnings"], 2)

    def test_warnings_as_errors_exit_two(self):
        code, payload, _ = self.run_validator(
            "1\n00:00:00,000 --> 00:00:01,000\nThis cue is far too dense for one second.\n",
            ".srt",
            "--cps-warning",
            "5",
            "--warnings-as-errors",
        )

        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "failed")
        self.assertEqual(payload["findings"][0]["severity"], "warning")

    def test_parse_failure_exit_three(self):
        code, payload, _ = self.run_validator(
            "1\n00:00:00.000 --> 00:00:01.000\nWrong decimal separator for SRT.\n",
            ".srt",
        )

        self.assertEqual(code, 3)
        self.assertEqual(payload["status"], "operational_failure")
        self.assertEqual(payload["findings"][0]["code"], "timestamp_syntax")

    def test_invalid_utf8_exit_three(self):
        code, payload, _ = self.run_validator(b"1\n\xff\n", ".srt", binary=True)

        self.assertEqual(code, 3)
        self.assertEqual(payload["findings"][0]["code"], "invalid_utf8")

    def test_explicit_format_overrides_extension(self):
        code, payload, _ = self.run_validator(
            "WEBVTT\n\n00:00.000 --> 00:01.000\nHello.\n",
            ".txt",
            "--format",
            "vtt",
        )

        self.assertEqual(code, 0)
        self.assertEqual(payload["files"][0]["format"], "vtt")

    def test_webvtt_requires_blank_line_after_signature_before_cues(self):
        code, payload, _ = self.run_validator(
            "WEBVTT\n00:00.000 --> 00:01.000\nHello.\n",
            ".vtt",
        )

        self.assertEqual(code, 3)
        self.assertEqual(payload["findings"][0]["code"], "webvtt_header_separator_missing")

    def test_notebook_is_valid_webvtt_cue_identifier_not_note(self):
        code, payload, _ = self.run_validator(
            "WEBVTT\n\nNOTEBOOK\n00:00.000 --> 00:01.000\nHello.\n",
            ".vtt",
        )

        self.assertEqual(code, 0)
        self.assertEqual(payload["summary"]["cues"], 1)

    def test_webvtt_rejects_invalid_style_block(self):
        code, payload, _ = self.run_validator(
            "WEBVTT\n\nSTYLE\n00:00.000 --> 00:01.000\n\n00:00.000 --> 00:01.000\nHello.\n",
            ".vtt",
        )

        self.assertEqual(code, 3)
        self.assertEqual(payload["findings"][0]["code"], "webvtt_style_invalid")

    def test_webvtt_rejects_invalid_region_block(self):
        code, payload, _ = self.run_validator(
            "WEBVTT\n\nREGION\nwidth=120%\n\n00:00.000 --> 00:01.000\nHello.\n",
            ".vtt",
        )

        self.assertEqual(code, 3)
        self.assertEqual(payload["findings"][0]["code"], "webvtt_region_invalid")

    def test_webvtt_rejects_duplicate_bad_and_out_of_range_cue_settings(self):
        cases = [
            ("00:00.000 --> 00:01.000 align:start align:end\nHello.\n", "webvtt_cue_setting_duplicate"),
            ("00:00.000 --> 00:01.000 banana:start\nHello.\n", "webvtt_cue_setting_invalid"),
            ("00:00.000 --> 00:01.000 size:101%\nHello.\n", "webvtt_cue_setting_invalid"),
        ]
        for timing_and_text, expected_code in cases:
            with self.subTest(timing_and_text=timing_and_text):
                code, payload, _ = self.run_validator("WEBVTT\n\n" + timing_and_text, ".vtt")

                self.assertEqual(code, 3)
                self.assertEqual(payload["findings"][0]["code"], expected_code)


if __name__ == "__main__":
    unittest.main()