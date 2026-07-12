import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import sys

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import inspect_workflow


VALID_WORKFLOW = {
    "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "model.safetensors"}},
    "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 512, "height": 512, "batch_size": 1}},
    "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": "quiet studio product photo"}},
    "7": {"class_type": "KSampler", "inputs": {"model": ["4", 0], "positive": ["6", 0], "latent_image": ["5", 0], "seed": 42}},
    "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": "demo"}, "_meta": {"title": "Save"}},
}


class InspectWorkflowTests(unittest.TestCase):
    def test_valid_workflow_inventory_has_no_findings(self):
        report = inspect_workflow.inspect_workflow(VALID_WORKFLOW)
        self.assertEqual(report["summary"]["error_count"], 0)
        self.assertEqual(report["summary"]["warning_count"], 0)
        self.assertEqual(report["summary"]["node_count"], 5)
        self.assertEqual(report["summary"]["edge_count"], 5)
        self.assertEqual(report["classes"]["KSampler"], 1)

    def test_invalid_links_and_cycles_are_errors(self):
        workflow = {
            "1": {"class_type": "A", "inputs": {"from_two": ["2", 0], "missing": ["9", 0], "bad": ["2", -1]}},
            "2": {"class_type": "B", "inputs": {"from_one": ["1", 0]}},
        }
        report = inspect_workflow.inspect_workflow(workflow)
        codes = {finding["code"] for finding in report["findings"]}
        self.assertIn("dangling_link", codes)
        self.assertIn("invalid_link_output_index", codes)
        self.assertIn("cycle", codes)
        self.assertGreater(report["summary"]["error_count"], 0)

    def test_sensitive_findings_redact_values(self):
        workflow = {
            "1": {
                "class_type": "APINode",
                "inputs": {
                    "api_key": "comfyui-87d01e28d0000000000000000000000000000000000000000",
                    "image": "C:/Users/Alice/Documents/private.png",
                },
            }
        }
        report = inspect_workflow.inspect_workflow(workflow)
        messages = json.dumps(report["findings"], sort_keys=True)
        self.assertIn("suspicious_key", messages)
        self.assertIn("suspicious_value", messages)
        self.assertNotIn("87d01e28", messages)
        self.assertNotIn("Alice", messages)

    def test_unknown_class_policy_can_error(self):
        report = inspect_workflow.inspect_workflow(VALID_WORKFLOW, {"SaveImage"}, "error")
        codes = [finding["code"] for finding in report["findings"]]
        self.assertIn("unknown_class_type", codes)
        self.assertEqual(report["summary"]["error_count"], 4)

    def test_main_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            valid_path = Path(directory) / "valid.json"
            invalid_path = Path(directory) / "invalid.json"
            valid_path.write_text(json.dumps(VALID_WORKFLOW), encoding="utf-8")
            invalid_path.write_text("{not json", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                valid_code = inspect_workflow.main([str(valid_path)])
            with redirect_stdout(io.StringIO()):
                parse_code = inspect_workflow.main([str(invalid_path)])

        self.assertEqual(valid_code, 0)
        self.assertEqual(parse_code, 3)


if __name__ == "__main__":
    unittest.main()