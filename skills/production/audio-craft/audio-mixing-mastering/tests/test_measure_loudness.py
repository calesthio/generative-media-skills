import json
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

import sys

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
SCRIPT = SCRIPT_DIR / "measure_loudness.py"
sys.path.insert(0, str(SCRIPT_DIR))

import measure_loudness


LOUDNORM_JSON = {
    "input_i": "-15.04",
    "input_tp": "-1.23",
    "input_lra": "3.50",
    "input_thresh": "-25.10",
    "target_offset": "0.04",
    "normalization_type": "dynamic",
}


class MeasureLoudnessTests(unittest.TestCase):
    def test_extract_loudnorm_json_from_ffmpeg_log(self):
        output = "before\n" + json.dumps(LOUDNORM_JSON, indent=2) + "\nafter"

        parsed = measure_loudness.extract_loudnorm_json(output)

        self.assertEqual(parsed["input_i"], "-15.04")
        self.assertEqual(parsed["input_tp"], "-1.23")

    def test_normalize_loudnorm_emits_stable_schema(self):
        report = measure_loudness.normalize_loudnorm(LOUDNORM_JSON, Path("sample.wav"), "ffmpeg")

        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["measurements"]["integrated_lufs"], -15.04)
        self.assertEqual(report["measurements"]["true_peak_dbtp"], -1.23)
        self.assertNotIn("target_offset_lu", report["measurements"])
        self.assertIn("algorithm", report["tool"])
        self.assertEqual(report["tool"]["analysis_mode"], "single_pass_measurement")
        self.assertFalse(report["tool"]["dual_mono"])
        self.assertEqual(report["tool"]["ffmpeg_reported_offset_lu"], 0.04)
        self.assertIn("never normalizes or mutates", report["tool"]["mode_note"])

    def test_run_loudnorm_uses_argv_and_no_shell(self):
        completed = subprocess_completed(stdout="", stderr=json.dumps(LOUDNORM_JSON), returncode=0)
        with mock.patch("measure_loudness.shutil.which", return_value="/usr/bin/ffmpeg"), mock.patch(
            "measure_loudness.subprocess.run", return_value=completed
        ) as run_mock:
            report = measure_loudness.run_loudnorm(Path("input.mp4"), "ffmpeg", 5, dual_mono=True)

        self.assertEqual(report["measurements"]["integrated_lufs"], -15.04)
        self.assertTrue(report["tool"]["dual_mono"])
        kwargs = run_mock.call_args.kwargs
        self.assertNotIn("shell", kwargs)
        argv = run_mock.call_args.args[0]
        self.assertEqual(argv[0], "/usr/bin/ffmpeg")
        self.assertIn("loudnorm=dual_mono=true:print_format=json", argv)
        self.assertIn("-map", argv)
        self.assertIn("0:a:0", argv)

    def test_run_loudnorm_reports_missing_ffmpeg(self):
        with mock.patch("measure_loudness.shutil.which", return_value=None):
            with self.assertRaises(measure_loudness.ToolUnavailableError):
                measure_loudness.run_loudnorm(Path("input.wav"), "missing", 5)

    def test_run_loudnorm_reports_timeout(self):
        with mock.patch("measure_loudness.shutil.which", return_value="/usr/bin/ffmpeg"), mock.patch(
            "measure_loudness.subprocess.run",
            side_effect=measure_loudness.subprocess.TimeoutExpired(["ffmpeg"], 5),
        ):
            with self.assertRaises(measure_loudness.LoudnessTimeoutError):
                measure_loudness.run_loudnorm(Path("input.wav"), "ffmpeg", 5)

    def test_run_loudnorm_reports_malformed_output(self):
        completed = subprocess_completed(stdout="not json", stderr="also not json", returncode=0)
        with mock.patch("measure_loudness.shutil.which", return_value="/usr/bin/ffmpeg"), mock.patch(
            "measure_loudness.subprocess.run", return_value=completed
        ):
            with self.assertRaises(measure_loudness.MalformedLoudnormOutputError):
                measure_loudness.run_loudnorm(Path("input.wav"), "ffmpeg", 5)

    def test_run_loudnorm_reports_absent_audio(self):
        completed = subprocess_completed(stdout="", stderr="Stream map '0:a:0' matches no streams.", returncode=1)
        with mock.patch("measure_loudness.shutil.which", return_value="/usr/bin/ffmpeg"), mock.patch(
            "measure_loudness.subprocess.run", return_value=completed
        ):
            with self.assertRaises(measure_loudness.NoAudioMeasuredError):
                measure_loudness.run_loudnorm(Path("input.mp4"), "ffmpeg", 5)

    def test_compare_targets_pass_and_fail(self):
        report = measure_loudness.normalize_loudnorm(LOUDNORM_JSON, Path("sample.wav"), "ffmpeg")

        passing = measure_loudness.compare_targets(report, -15.0, 0.1, -1.0, 0.0)
        failing = measure_loudness.compare_targets(report, -18.0, 0.25, -2.0, 0.1)

        self.assertEqual(passing["status"], "pass")
        self.assertTrue(all(check["passed"] for check in passing["checks"]))
        self.assertEqual(failing["status"], "fail")
        self.assertFalse(all(check["passed"] for check in failing["checks"]))

    def test_main_returns_target_mismatch_exit_code(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            media = Path(temp_dir) / "sample.wav"
            media.write_bytes(b"placeholder")
            with mock.patch(
                "measure_loudness.run_loudnorm",
                return_value=measure_loudness.normalize_loudnorm(LOUDNORM_JSON, media, "ffmpeg"),
            ):
                with redirect_stdout(StringIO()):
                    code = measure_loudness.main([str(media), "--target-lufs", "-18", "--lufs-tolerance", "0.1"])

        self.assertEqual(code, measure_loudness.EXIT_TARGET_MISMATCH)

    def test_main_returns_operational_failure_for_bad_args(self):
        with redirect_stdout(StringIO()):
            code = measure_loudness.main(["missing.wav", "--timeout", "0"])

        self.assertEqual(code, measure_loudness.EXIT_OPERATIONAL_FAILURE)

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not available")
    def test_real_ffmpeg_loudness_measurement_on_generated_tone(self):
        ffmpeg = shutil.which("ffmpeg")
        with tempfile.TemporaryDirectory() as temp_dir:
            media = Path(temp_dir) / "tone.wav"
            generate = subprocess.run(
                [
                    ffmpeg,
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-f",
                    "lavfi",
                    "-i",
                    "sine=frequency=1000:duration=1.0",
                    "-c:a",
                    "pcm_s16le",
                    str(media),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(generate.returncode, 0, generate.stderr)

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(media), "--dual-mono"],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "pass")
        self.assertTrue(payload["tool"]["dual_mono"])
        self.assertIsInstance(payload["measurements"]["integrated_lufs"], float)


def subprocess_completed(stdout, stderr, returncode):
    return type("Completed", (), {"stdout": stdout, "stderr": stderr, "returncode": returncode})()


if __name__ == "__main__":
    unittest.main()