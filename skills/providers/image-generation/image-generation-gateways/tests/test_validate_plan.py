from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_plan.py"
NOW = "2026-07-11"


def digest(char: str) -> str:
    return char * 64


def valid_plan() -> dict[str, object]:
    return {
        "gateway": "fal.ai",
        "model": {
            "id": "fal-ai/flux/schnell",
            "endpoint": "fal-ai/flux/schnell",
            "version_policy": "pinned-endpoint",
        },
        "schema": {
            "url": "https://fal.ai/models/fal-ai/flux/schnell/api",
            "sha256": digest("a"),
            "checked_at": "2026-07-11",
        },
        "canonical_payload": {
            "prompt": "A labeled packaging concept on a plain tabletop.",
            "image_size": "landscape_4_3",
            "num_images": 2,
            "enable_safety_checker": True,
        },
        "output": {"count": 2, "policy": "store-approved-artifacts-only"},
        "price": {
            "source": "https://api.fal.ai/v1/models/pricing?endpoint_id=fal-ai/flux/schnell",
            "checked_at": "2026-07-11",
            "currency": "USD",
            "unit": "megapixel",
            "unit_price": "0.003",
            "billable_units": "2.5",
            "estimate": "0.0075",
            "ceiling": "0.01",
        },
        "governance": {
            "rights_digest": digest("b"),
            "moderation_digest": digest("c"),
            "governance_digest": digest("d"),
        },
        "attempt": {"uuid": "4f0b6d27-84b9-4d7b-a9e6-41fb2d8f4b8d"},
    }


class ValidatePlanTests(unittest.TestCase):
    def run_cli(self, plan: dict[str, object] | str, *args: str) -> tuple[int, dict[str, object], str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "plan.json"
            if isinstance(plan, str):
                path.write_text(plan, encoding="utf-8")
            else:
                path.write_text(json.dumps(plan, sort_keys=True, indent=2), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(path), "--max-age-days", "1", "--now", NOW, *args],
                check=False,
                capture_output=True,
                text=True,
            )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            self.fail(f"CLI did not emit JSON. stdout={completed.stdout!r} stderr={completed.stderr!r}: {exc}")
        return completed.returncode, payload, completed.stderr

    def test_valid_plan_returns_stable_redacted_digest(self) -> None:
        code, payload, stderr = self.run_cli(valid_plan())

        self.assertEqual(stderr, "")
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["computed_estimate"], "0.0075")
        self.assertNotIn("A labeled packaging concept", json.dumps(payload))
        self.assertNotIn("image_size", json.dumps(payload))
        self.assertRegex(str(payload["approval_sha256"]), r"^[0-9a-f]{64}$")

    def test_expected_digest_must_match(self) -> None:
        code, payload, _ = self.run_cli(valid_plan(), "--expected-approval-sha256", digest("0"))

        self.assertEqual(code, 2)
        self.assertEqual(payload["error"]["code"], "approval_digest_mismatch")

    def test_over_budget_plan_fails(self) -> None:
        plan = valid_plan()
        plan["price"]["ceiling"] = "0.001"

        code, payload, _ = self.run_cli(plan)

        self.assertEqual(code, 2)
        self.assertIn("ceiling", payload["error"]["message"])

    def test_stale_schema_or_price_fails(self) -> None:
        plan = valid_plan()
        plan["schema"]["checked_at"] = "2026-07-09"

        code, payload, _ = self.run_cli(plan)

        self.assertEqual(code, 2)
        self.assertIn("stale", payload["error"]["message"])

    def test_secret_like_payload_key_fails(self) -> None:
        plan = valid_plan()
        plan["canonical_payload"]["api_key"] = "not allowed"

        code, payload, _ = self.run_cli(plan)

        self.assertEqual(code, 2)
        self.assertIn("secret-bearing", payload["error"]["message"])

    def test_secret_like_key_anywhere_in_plan_fails(self) -> None:
        plan = valid_plan()
        plan["model"]["token"] = "not allowed"

        code, payload, _ = self.run_cli(plan)

        self.assertEqual(code, 2)
        self.assertIn("secret-bearing", payload["error"]["message"])

    def test_secret_like_value_anywhere_in_plan_fails(self) -> None:
        plan = valid_plan()
        plan["canonical_payload"]["prompt"] = "Authorization: Bearer abc123"

        code, payload, _ = self.run_cli(plan)

        self.assertEqual(code, 2)
        self.assertIn("secret value", payload["error"]["message"])

    def test_unknown_keys_fail_at_defined_object_levels(self) -> None:
        cases = [
            ((), "extra"),
            (("model",), "extra"),
            (("schema",), "extra"),
            (("output",), "extra"),
            (("price",), "extra"),
            (("governance",), "extra"),
            (("attempt",), "extra"),
        ]
        for path, key in cases:
            with self.subTest(path=path or ("plan",)):
                plan = valid_plan()
                target = plan
                for part in path:
                    target = target[part]
                target[key] = "not accepted"

                code, payload, _ = self.run_cli(plan)

                self.assertEqual(code, 2)
                self.assertIn("unknown key", payload["error"]["message"])

    def test_strict_json_rejects_nan_and_infinity(self) -> None:
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                text = json.dumps(valid_plan(), sort_keys=True).replace('"num_images": 2', f'"num_images": {constant}')

                code, payload, _ = self.run_cli(text)

                self.assertEqual(code, 3)
                self.assertIn("strict JSON", payload["error"]["message"])

    def test_secret_query_params_fail_but_endpoint_id_is_allowed_for_price_source(self) -> None:
        plan = valid_plan()
        plan["schema"]["url"] = "https://example.com/schema?token=abc"

        code, payload, _ = self.run_cli(plan)

        self.assertEqual(code, 2)
        self.assertIn("secret-bearing query", payload["error"]["message"])

        safe_plan = valid_plan()
        code, payload, _ = self.run_cli(safe_plan)

        self.assertEqual(code, 0)

    def test_estimate_must_equal_decimal_product(self) -> None:
        plan = valid_plan()
        plan["price"]["estimate"] = "0.0074"

        code, payload, _ = self.run_cli(plan)

        self.assertEqual(code, 2)
        self.assertIn("unit_price * billable_units", payload["error"]["message"])

    def test_digest_changes_when_any_accepted_semantic_changes(self) -> None:
        base_code, base_payload, _ = self.run_cli(valid_plan())
        self.assertEqual(base_code, 0)

        semantic_changes = [
            (("model", "endpoint"), "fal-ai/flux/dev"),
            (("schema", "sha256"), digest("e")),
            (("output", "policy"), "store-approved-artifacts-and-ledger"),
            (("price", "ceiling"), "0.02"),
            (("governance", "rights_digest"), digest("f")),
            (("attempt", "uuid"), "9ac6ed2c-0d0c-4b35-b244-2d52f3f10563"),
        ]
        for path, value in semantic_changes:
            with self.subTest(path=path):
                plan = valid_plan()
                target = plan
                for part in path[:-1]:
                    target = target[part]
                target[path[-1]] = value

                code, payload, _ = self.run_cli(plan)

                self.assertEqual(code, 0)
                self.assertNotEqual(payload["approval_sha256"], base_payload["approval_sha256"])

    def test_bad_json_is_operational_exit_three(self) -> None:
        code, payload, _ = self.run_cli("{")

        self.assertEqual(code, 3)
        self.assertEqual(payload["status"], "error")


if __name__ == "__main__":
    unittest.main()