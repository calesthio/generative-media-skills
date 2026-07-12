import base64
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_gltf.py"


def write_json(path, document):
    path.write_text(json.dumps(document, separators=(",", ":")), encoding="utf-8")


def tiny_document(buffer_uri="data:application/octet-stream;base64,AAAA", image_uri="texture.png"):
    return {
        "asset": {"version": "2.0", "generator": "unit-test"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "material": 0}]}],
        "materials": [{"pbrMetallicRoughness": {"baseColorTexture": {"index": 0}}}],
        "textures": [{"source": 0}],
        "images": [{"uri": image_uri}],
        "buffers": [{"byteLength": 3, "uri": buffer_uri}],
        "bufferViews": [{"buffer": 0, "byteLength": 3}],
        "accessors": [{"bufferView": 0, "componentType": 5126, "count": 1, "type": "VEC3", "min": [0, 0, 0], "max": [0, 0, 0]}],
    }


def make_glb(document, bin_payload=b"\x00\x00\x00\x00"):
    json_payload = json.dumps(document, separators=(",", ":")).encode("utf-8")
    json_payload += b" " * ((4 - len(json_payload) % 4) % 4)
    bin_payload += b"\x00" * ((4 - len(bin_payload) % 4) % 4)
    chunks = [struct.pack("<II", len(json_payload), 0x4E4F534A) + json_payload]
    if bin_payload:
        chunks.append(struct.pack("<II", len(bin_payload), 0x004E4942) + bin_payload)
    length = 12 + sum(len(chunk) for chunk in chunks)
    return struct.pack("<III", 0x46546C67, 2, length) + b"".join(chunks)


class InspectGltfTests(unittest.TestCase):
    def run_tool(self, path, *extra):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(path), *extra],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(completed.stderr, "")
        return completed.returncode, json.loads(completed.stdout)

    def test_valid_gltf_inventory_and_dependencies(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "texture.png").write_bytes(b"not a real png")
            path = root / "asset.gltf"
            write_json(path, tiny_document())

            code, report = self.run_tool(path)

        self.assertEqual(code, 0)
        self.assertTrue(report["ok"])
        self.assertEqual(report["inventory"]["meshes"], 1)
        self.assertEqual(report["inventory"]["meshPrimitives"], 1)
        self.assertEqual(len(report["dependencies"]), 2)

    def test_valid_glb_reads_json_chunk_and_bin_buffer(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "texture.png").write_bytes(b"not a real png")
            document = tiny_document(buffer_uri=None)
            del document["buffers"][0]["uri"]
            path = root / "asset.glb"
            path.write_bytes(make_glb(document))

            code, report = self.run_tool(path)

        self.assertEqual(code, 0)
        self.assertTrue(report["ok"])
        self.assertEqual(report["container"]["chunks"][0]["type"], "JSON")
        self.assertEqual(report["container"]["chunks"][1]["type"], "BIN")

    def test_glb_bin_length_accepts_exact_and_padded_relationships(self):
        for byte_length, payload in ((4, b"1234"), (3, b"123"), (1, b"1")):
            with self.subTest(byte_length=byte_length, payload_length=len(payload)):
                with tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    (root / "texture.png").write_bytes(b"not a real png")
                    document = tiny_document(buffer_uri=None)
                    document["buffers"][0] = {"byteLength": byte_length}
                    path = root / "asset.glb"
                    path.write_bytes(make_glb(document, payload))

                    code, report = self.run_tool(path)

                self.assertEqual(code, 0, report)

    def test_glb_bin_length_rejects_invalid_short_and_overpadded_relationships(self):
        cases = [
            ({"byteLength": -1}, b"1234"),
            ({"byteLength": True}, b"1234"),
            ({"byteLength": 5}, b"1234"),
            ({"byteLength": 0}, b"1234"),
        ]
        for buffer, payload in cases:
            with self.subTest(buffer=buffer, payload_length=len(payload)):
                with tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    (root / "texture.png").write_bytes(b"not a real png")
                    document = tiny_document(buffer_uri=None)
                    document["buffers"][0] = buffer
                    path = root / "asset.glb"
                    path.write_bytes(make_glb(document, payload))

                    code, report = self.run_tool(path)

                self.assertEqual(code, 2)
                self.assertIn("GLB_BIN_LENGTH", {item["code"] for item in report["issues"]})

    def test_rejects_missing_and_unsafe_external_uris(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "asset.gltf"
            write_json(path, tiny_document(buffer_uri="../secret.bin", image_uri="missing.png"))

            code, report = self.run_tool(path)

        codes = {item["code"] for item in report["issues"]}
        self.assertEqual(code, 2)
        self.assertIn("URI_PATH", codes)
        self.assertIn("MISSING_URI", codes)

    def test_detects_bad_common_index_references(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "texture.png").write_bytes(b"not a real png")
            document = tiny_document()
            document["nodes"][0]["mesh"] = 7
            document["textures"][0]["source"] = 4
            document["materials"][0]["pbrMetallicRoughness"]["baseColorTexture"]["index"] = 3
            path = root / "asset.gltf"
            write_json(path, document)

            code, report = self.run_tool(path)

        self.assertEqual(code, 2)
        self.assertGreaterEqual(sum(1 for item in report["issues"] if item["code"] == "INDEX_RANGE"), 3)

    def test_glb_missing_required_bin_chunk_is_validation_error(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "texture.png").write_bytes(b"not a real png")
            document = tiny_document(buffer_uri=None)
            del document["buffers"][0]["uri"]
            path = root / "asset.glb"
            path.write_bytes(make_glb(document, bin_payload=b""))

            code, report = self.run_tool(path)

        self.assertEqual(code, 2)
        self.assertIn("GLB_BIN", {item["code"] for item in report["issues"]})

    def test_data_uri_limit_is_validation_error(self):
        payload = base64.b64encode(b"123456").decode("ascii")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "texture.png").write_bytes(b"not a real png")
            path = root / "asset.gltf"
            write_json(path, tiny_document(buffer_uri=f"data:application/octet-stream;base64,{payload}"))

            code, report = self.run_tool(path, "--data-uri-limit", "2")

        self.assertEqual(code, 2)
        self.assertIn("DATA_URI_LIMIT", {item["code"] for item in report["issues"]})

    def test_base64_data_uri_limit_uses_estimate_before_decode(self):
        payload = base64.b64encode(b"x" * 128).decode("ascii")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "texture.png").write_bytes(b"not a real png")
            path = root / "asset.gltf"
            write_json(path, tiny_document(buffer_uri=f"data:application/octet-stream;base64,{payload}"))

            code, report = self.run_tool(path, "--data-uri-limit", "64")

        self.assertEqual(code, 2)
        dependency = next(item for item in report["dependencies"] if item["kind"] == "buffer")
        self.assertEqual(dependency["estimatedBytes"], 128)
        self.assertIsNone(dependency["bytes"])

    def test_negative_limits_are_operational_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "texture.png").write_bytes(b"not a real png")
            path = root / "asset.gltf"
            write_json(path, tiny_document())

            code, report = self.run_tool(path, "--data-uri-limit", "-1")

        self.assertEqual(code, 3)
        self.assertIn("nonnegative", report["issues"][0]["message"])

    def test_max_file_byte_guard_is_operational_error(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "asset.gltf"
            write_json(path, tiny_document())

            code, report = self.run_tool(path, "--max-file-bytes", "8")

        self.assertEqual(code, 3)
        self.assertIn("max file limit", report["issues"][0]["message"])

    def test_corrupt_json_is_operational_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "asset.gltf"
            path.write_text("{not json", encoding="utf-8")

            code, report = self.run_tool(path)

        self.assertEqual(code, 3)
        self.assertFalse(report["ok"])
        self.assertEqual(report["issues"][0]["code"], "OPERATIONAL")

    def test_truncated_glb_is_operational_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "asset.glb"
            path.write_bytes(b"glTF")

            code, report = self.run_tool(path)

        self.assertEqual(code, 3)
        self.assertEqual(report["issues"][0]["severity"], "fatal")


if __name__ == "__main__":
    unittest.main()