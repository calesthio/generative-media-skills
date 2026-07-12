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
SCRIPT = SCRIPT_DIR / "media_probe.py"
sys.path.insert(0, str(SCRIPT_DIR))

import media_probe


RAW_PROBE = {
    "streams": [
        {
            "index": 0,
            "codec_type": "video",
            "codec_name": "h264",
            "profile": "High",
            "width": 320,
            "height": 180,
            "pix_fmt": "yuv420p",
            "r_frame_rate": "30/1",
            "avg_frame_rate": "30/1",
            "duration": "1.000000",
        },
        {
            "index": 1,
            "codec_type": "audio",
            "codec_name": "aac",
            "sample_rate": "48000",
            "channels": 2,
            "channel_layout": "stereo",
            "sample_fmt": "fltp",
            "duration": "1.000000",
        },
    ],
    "format": {
        "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
        "format_long_name": "QuickTime / MOV",
        "duration": "1.000000",
        "size": "12345",
        "bit_rate": "98765",
    },
}


class MediaProbeTests(unittest.TestCase):
    def test_normalize_probe_extracts_stable_fields(self):
        report = media_probe.normalize_probe(RAW_PROBE, Path("sample.mp4"), "ffprobe")

        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["media"]["duration_seconds"], 1.0)
        self.assertEqual(report["streams"]["counts"]["video"], 1)
        self.assertEqual(report["streams"]["video"]["codec_name"], "h264")
        self.assertEqual(report["streams"]["video"]["width"], 320)
        self.assertEqual(report["streams"]["video"]["avg_frame_rate"]["value"], 30.0)
        self.assertEqual(report["streams"]["audio"]["sample_rate"], 48000)
        self.assertEqual(report["streams"]["audio"]["channels"], 2)

    def test_validate_expectations_passes_supported_fields(self):
        report = media_probe.normalize_probe(RAW_PROBE, Path("sample.mp4"), "ffprobe")
        expectation = {
            "checks": [
                {"field": "media.duration_seconds", "op": "tolerance", "value": {"value": 1.0, "tolerance": 0.05}},
                {"field": "streams.video.codec_name", "op": "equals", "value": "h264"},
                {"field": "streams.video.width", "op": "equals", "value": 320},
                {"field": "streams.video.height", "op": "equals", "value": 180},
                {"field": "streams.video.avg_frame_rate.value", "op": "tolerance", "value": {"value": 30.0, "tolerance": 0.01}},
                {"field": "streams.video.pix_fmt", "op": "equals", "value": "yuv420p"},
                {"field": "streams.audio.codec_name", "op": "equals", "value": "aac"},
                {"field": "streams.audio.sample_rate", "op": "equals", "value": 48000},
                {"field": "streams.audio.channels", "op": "equals", "value": 2},
            ]
        }

        result = media_probe.validate_expectations(report, expectation)

        self.assertEqual(result["status"], "pass")
        self.assertTrue(all(check["passed"] for check in result["checks"]))

    def test_validate_expectations_reports_failures(self):
        report = media_probe.normalize_probe(RAW_PROBE, Path("sample.mp4"), "ffprobe")
        result = media_probe.validate_expectations(
            report,
            {"checks": [{"field": "streams.video.width", "op": "equals", "value": 640}]},
        )

        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["checks"][0]["actual"], 320)
        self.assertEqual(result["checks"][0]["message"], "expectation not met")

    def test_validate_expectations_rejects_bad_schema(self):
        report = media_probe.normalize_probe(RAW_PROBE, Path("sample.mp4"), "ffprobe")

        with self.assertRaises(media_probe.MalformedExpectationError):
            media_probe.validate_expectations(report, {"checks": {}})

    def test_validate_expectations_rejects_malformed_numeric_values(self):
        report = media_probe.normalize_probe(RAW_PROBE, Path("sample.mp4"), "ffprobe")
        cases = [
            {"field": "media.duration_seconds", "op": "range", "value": {"min": "low"}},
            {"field": "media.duration_seconds", "op": "range", "value": {"max": float("inf")}},
            {"field": "media.duration_seconds", "op": "tolerance", "value": {"value": 1.0, "tolerance": -0.1}},
            {"field": "media.duration_seconds", "op": "tolerance", "value": {"value": float("nan"), "tolerance": 0.1}},
        ]
        for check in cases:
            with self.subTest(check=check):
                with self.assertRaises(media_probe.MalformedExpectationError):
                    media_probe.validate_expectations(report, {"checks": [check]})

    def test_run_ffprobe_uses_argv_and_no_shell(self):
        completed = subprocess_completed(stdout=json.dumps(RAW_PROBE), stderr="", returncode=0)
        with mock.patch("media_probe.shutil.which", return_value="/usr/bin/ffprobe"), mock.patch(
            "media_probe.subprocess.run", return_value=completed
        ) as run_mock:
            result = media_probe.run_ffprobe(Path("input.mp4"), "ffprobe", 3)

        self.assertEqual(result["format"]["duration"], "1.000000")
        kwargs = run_mock.call_args.kwargs
        self.assertNotIn("shell", kwargs)
        self.assertEqual(run_mock.call_args.args[0][0], "/usr/bin/ffprobe")
        self.assertIn("-print_format", run_mock.call_args.args[0])
        self.assertIn("json", run_mock.call_args.args[0])

    def test_run_ffprobe_reports_missing_executable(self):
        with mock.patch("media_probe.shutil.which", return_value=None):
            with self.assertRaises(media_probe.ToolUnavailableError):
                media_probe.run_ffprobe(Path("input.mp4"), "missing-ffprobe", 3)

    def test_run_ffprobe_reports_timeout(self):
        with mock.patch("media_probe.shutil.which", return_value="/usr/bin/ffprobe"), mock.patch(
            "media_probe.subprocess.run", side_effect=media_probe.subprocess.TimeoutExpired(["ffprobe"], 3)
        ):
            with self.assertRaises(media_probe.ProbeTimeoutError):
                media_probe.run_ffprobe(Path("input.mp4"), "ffprobe", 3)

    def test_run_ffprobe_reports_malformed_json(self):
        completed = subprocess_completed(stdout="not json", stderr="", returncode=0)
        with mock.patch("media_probe.shutil.which", return_value="/usr/bin/ffprobe"), mock.patch(
            "media_probe.subprocess.run", return_value=completed
        ):
            with self.assertRaises(media_probe.MalformedProbeError):
                media_probe.run_ffprobe(Path("input.mp4"), "ffprobe", 3)

    def test_main_returns_expectation_failure_exit_code(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            media = Path(temp_dir) / "sample.mp4"
            media.write_bytes(b"placeholder")
            expect = Path(temp_dir) / "expect.json"
            expect.write_text(json.dumps({"checks": [{"field": "streams.video.width", "op": "equals", "value": 640}]}), encoding="utf-8")
            with mock.patch("media_probe.run_ffprobe", return_value=RAW_PROBE):
                with redirect_stdout(StringIO()):
                    code = media_probe.main([str(media), "--expect", str(expect)])

        self.assertEqual(code, media_probe.EXIT_EXPECTATION_FAILED)

    def test_main_returns_malformed_expectation_exit_code_for_bad_numeric_value(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            media = Path(temp_dir) / "sample.mp4"
            media.write_bytes(b"placeholder")
            expect = Path(temp_dir) / "expect.json"
            expect.write_text(
                json.dumps({"checks": [{"field": "media.duration_seconds", "op": "tolerance", "value": {"value": 1.0, "tolerance": -0.1}}]}),
                encoding="utf-8",
            )
            with mock.patch("media_probe.run_ffprobe", return_value=RAW_PROBE):
                stderr = StringIO()
                with redirect_stdout(StringIO()), mock.patch("sys.stderr", stderr):
                    code = media_probe.main([str(media), "--expect", str(expect)])

        self.assertEqual(code, media_probe.EXIT_MALFORMED_EXPECTATION)
        payload = json.loads(stderr.getvalue())
        self.assertEqual(payload["error"]["type"], "MalformedExpectationError")

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg/ffprobe not available")
    def test_real_ffprobe_on_generated_tone_with_expectation(self):
        ffmpeg = shutil.which("ffmpeg")
        ffprobe = shutil.which("ffprobe")
        with tempfile.TemporaryDirectory() as temp_dir:
            media = Path(temp_dir) / "tone.wav"
            expect = Path(temp_dir) / "expect.json"
            generate = subprocess.run(
                [
                    ffmpeg,
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-f",
                    "lavfi",
                    "-i",
                    "sine=frequency=1000:duration=0.2",
                    "-c:a",
                    "pcm_s16le",
                    str(media),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(generate.returncode, 0, generate.stderr)
            expect.write_text(
                json.dumps(
                    {
                        "checks": [
                            {"field": "streams.audio.sample_rate", "op": "equals", "value": 44100},
                            {"field": "streams.audio.channels", "op": "equals", "value": 1},
                            {"field": "media.duration_seconds", "op": "tolerance", "value": {"value": 0.2, "tolerance": 0.05}},
                        ]
                    }
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(media), "--expect", str(expect), "--ffprobe", ffprobe],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["streams"]["audio"]["channels"], 1)


def subprocess_completed(stdout, stderr, returncode):
    return type("Completed", (), {"stdout": stdout, "stderr": stderr, "returncode": returncode})()


if __name__ == "__main__":
    unittest.main()