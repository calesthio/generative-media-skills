#!/usr/bin/env python3
"""Bounded glTF/GLB preflight inspector.

This helper intentionally performs structural and packaging checks only. It is
not a replacement for Khronos glTF Validator, target DCC or engine import, or
visual/material/animation QA.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
from pathlib import Path
import struct
import sys
from typing import Any
from urllib.parse import unquote, urlparse


EXIT_OK = 0
EXIT_VALIDATION = 2
EXIT_OPERATIONAL = 3

GLB_MAGIC = 0x46546C67
GLB_VERSION = 2
CHUNK_JSON = 0x4E4F534A
CHUNK_BIN = 0x004E4942
DEFAULT_DATA_URI_LIMIT = 32 * 1024 * 1024
DEFAULT_MAX_FILE_BYTES = 256 * 1024 * 1024

TOP_LEVEL_ARRAYS = (
    "scenes",
    "nodes",
    "meshes",
    "materials",
    "textures",
    "images",
    "animations",
    "skins",
    "cameras",
    "accessors",
    "buffers",
    "bufferViews",
    "samplers",
)


class PreflightError(Exception):
    """Operational failure that prevents validation from completing."""


def issue(code: str, message: str, path: str, severity: str = "error") -> dict[str, str]:
    return {"code": code, "message": message, "path": path, "severity": severity}


def base64_decoded_size_estimate(payload: str) -> int | None:
    compact = "".join(payload.split())
    if not compact:
        return 0
    if len(compact) % 4 == 1:
        return None
    padding = len(compact) - len(compact.rstrip("="))
    if padding > 2:
        return None
    return (len(compact) // 4) * 3 + ((len(compact) % 4) * 3 // 4) - padding


def byte_count_from_data_uri(uri: str) -> int | None:
    comma = uri.find(",")
    if comma < 0:
        return None
    header = uri[:comma].lower()
    payload = uri[comma + 1 :]
    if ";base64" in header:
        compact = "".join(payload.split())
        try:
            return len(base64.b64decode(compact, validate=True))
        except binascii.Error:
            return None
    return len(unquote(payload).encode("utf-8"))


def read_gltf_json(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise PreflightError(f"Could not read input: {exc}") from exc
    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise PreflightError(f"Could not parse glTF JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}") from exc
    if not isinstance(document, dict):
        raise PreflightError("glTF JSON root must be an object")
    return document, {"kind": "gltf", "chunks": []}


def read_glb_json(path: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise PreflightError(f"Could not read input: {exc}") from exc

    issues: list[dict[str, str]] = []
    if len(data) < 12:
        raise PreflightError("GLB is shorter than its 12-byte header")
    magic, version, declared_length = struct.unpack_from("<III", data, 0)
    if magic != GLB_MAGIC:
        raise PreflightError("GLB magic is not 'glTF'")
    if version != GLB_VERSION:
        issues.append(issue("GLB_VERSION", f"GLB container version is {version}, expected 2", "$"))
    if declared_length != len(data):
        issues.append(issue("GLB_LENGTH", f"GLB declared length {declared_length} does not match file length {len(data)}", "$"))

    chunks: list[dict[str, Any]] = []
    offset = 12
    while offset < len(data):
        if offset + 8 > len(data):
            raise PreflightError("GLB chunk header is truncated")
        chunk_length, chunk_type = struct.unpack_from("<II", data, offset)
        payload_start = offset + 8
        payload_end = payload_start + chunk_length
        if payload_end > len(data):
            raise PreflightError("GLB chunk payload is truncated")
        if chunk_length % 4 != 0:
            issues.append(issue("GLB_CHUNK_ALIGNMENT", f"Chunk at byte {offset} has non-4-byte length {chunk_length}", "$.chunks"))
        chunks.append({"type": chunk_type, "length": chunk_length, "offset": offset, "data": data[payload_start:payload_end]})
        offset = payload_end
    if offset != len(data):
        raise PreflightError("GLB chunk parsing did not end at file length")
    if not chunks:
        raise PreflightError("GLB contains no chunks")
    if chunks[0]["type"] != CHUNK_JSON:
        raise PreflightError("GLB first chunk must be JSON")
    if len(chunks) > 1 and chunks[1]["type"] != CHUNK_BIN:
        issues.append(issue("GLB_CHUNK_ORDER", "GLB second chunk is not BIN", "$.chunks[1]"))
    for index, chunk in enumerate(chunks[2:], start=2):
        if chunk["type"] in (CHUNK_JSON, CHUNK_BIN):
            issues.append(issue("GLB_CHUNK_ORDER", f"Known GLB chunk type appears after allowed position at index {index}", f"$.chunks[{index}]"))

    json_bytes = chunks[0]["data"].rstrip(b" ")
    try:
        document = json.loads(json_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PreflightError(f"Could not parse GLB JSON chunk: {exc}") from exc
    if not isinstance(document, dict):
        raise PreflightError("GLB JSON root must be an object")

    chunk_summary = []
    for chunk in chunks:
        chunk_type = chunk["type"]
        if chunk_type == CHUNK_JSON:
            type_name = "JSON"
        elif chunk_type == CHUNK_BIN:
            type_name = "BIN"
        else:
            type_name = f"0x{chunk_type:08X}"
        chunk_summary.append({"type": type_name, "length": chunk["length"], "offset": chunk["offset"]})

    metadata = {"kind": "glb", "chunks": chunk_summary, "declaredLength": declared_length, "fileLength": len(data)}
    return document, metadata, issues


def top_array(document: dict[str, Any], name: str, issues: list[dict[str, str]]) -> list[Any]:
    value = document.get(name, [])
    if value is None:
        return []
    if not isinstance(value, list):
        issues.append(issue("TYPE", f"Top-level {name} must be an array when present", f"$.{name}"))
        return []
    return value


def check_index(value: Any, array: list[Any], array_name: str, path: str, issues: list[dict[str, str]]) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        issues.append(issue("INDEX_TYPE", f"Reference to {array_name} must be a non-negative integer", path))
    elif value < 0 or value >= len(array):
        issues.append(issue("INDEX_RANGE", f"Reference {value} is outside {array_name}[0..{len(array) - 1}]", path))


def check_index_list(values: Any, array: list[Any], array_name: str, path: str, issues: list[dict[str, str]]) -> None:
    if not isinstance(values, list):
        issues.append(issue("TYPE", f"{path} must be an array of indices", path))
        return
    seen: set[int] = set()
    for index, value in enumerate(values):
        item_path = f"{path}[{index}]"
        check_index(value, array, array_name, item_path, issues)
        if isinstance(value, int) and not isinstance(value, bool):
            if value in seen:
                issues.append(issue("DUPLICATE_INDEX", f"Duplicate index {value}", item_path))
            seen.add(value)


def safe_external_path(uri: str, asset_dir: Path, root: Path) -> tuple[Path | None, str | None]:
    parsed = urlparse(uri)
    if parsed.scheme or parsed.netloc or parsed.params or parsed.query or parsed.fragment:
        return None, "URI must be a plain relative path without scheme, authority, query, or fragment"
    decoded = unquote(uri.replace("\\", "/"))
    if not decoded or decoded.startswith("/") or decoded.startswith("//"):
        return None, "URI must be a relative local path"
    candidate = Path(decoded)
    if candidate.is_absolute():
        return None, "URI must not be absolute"
    resolved = (asset_dir / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return resolved, "URI escapes the allowed root"
    return resolved, None


def check_uri(
    uri: Any,
    kind: str,
    path: str,
    asset_dir: Path,
    root: Path,
    data_uri_limit: int,
    issues: list[dict[str, str]],
    dependencies: list[dict[str, Any]],
) -> None:
    if not isinstance(uri, str):
        issues.append(issue("URI_TYPE", "URI must be a string", path))
        return
    if uri.startswith("data:"):
        comma = uri.find(",")
        estimate = None
        if comma >= 0 and ";base64" in uri[:comma].lower():
            estimate = base64_decoded_size_estimate(uri[comma + 1 :])
            if estimate is not None and estimate > data_uri_limit:
                entry = {"kind": kind, "path": path, "type": "data", "bytes": None, "estimatedBytes": estimate}
                dependencies.append(entry)
                issues.append(issue("DATA_URI_LIMIT", f"Data URI has estimated {estimate} bytes, over limit {data_uri_limit}", path))
                return
        byte_count = byte_count_from_data_uri(uri)
        entry: dict[str, Any] = {"kind": kind, "path": path, "type": "data", "bytes": byte_count}
        if estimate is not None:
            entry["estimatedBytes"] = estimate
        dependencies.append(entry)
        if byte_count is None:
            issues.append(issue("DATA_URI", "Data URI could not be decoded", path))
        elif byte_count > data_uri_limit:
            issues.append(issue("DATA_URI_LIMIT", f"Data URI has {byte_count} bytes, over limit {data_uri_limit}", path))
        return

    resolved, error = safe_external_path(uri, asset_dir, root)
    entry = {"kind": kind, "path": path, "type": "external", "uri": uri, "resolved": str(resolved) if resolved else None}
    if error:
        issues.append(issue("URI_PATH", error, path))
        entry["exists"] = False
        dependencies.append(entry)
        return
    exists = bool(resolved and resolved.is_file())
    entry["exists"] = exists
    dependencies.append(entry)
    if not exists:
        issues.append(issue("MISSING_URI", f"Referenced local dependency does not exist: {uri}", path))


def primitive_count(meshes: list[Any]) -> int:
    count = 0
    for mesh in meshes:
        if isinstance(mesh, dict) and isinstance(mesh.get("primitives"), list):
            count += len(mesh["primitives"])
    return count


def check_texture_info(value: Any, textures: list[Any], path: str, issues: list[dict[str, str]]) -> None:
    if not isinstance(value, dict):
        issues.append(issue("TYPE", "Texture info must be an object", path))
        return
    if "index" in value:
        check_index(value["index"], textures, "textures", f"{path}.index", issues)
    else:
        issues.append(issue("TEXTURE_INFO", "Texture info must define index", f"{path}.index"))


def inspect_document(document: dict[str, Any], asset_path: Path, root: Path, data_uri_limit: int, container: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]], list[dict[str, Any]]]:
    issues: list[dict[str, str]] = []
    dependencies: list[dict[str, Any]] = []
    arrays = {name: top_array(document, name, issues) for name in TOP_LEVEL_ARRAYS}

    asset = document.get("asset")
    if not isinstance(asset, dict):
        issues.append(issue("ASSET", "glTF asset object is required", "$.asset"))
    elif asset.get("version") != "2.0":
        issues.append(issue("ASSET_VERSION", "asset.version should be '2.0' for this glTF 2.0 preflight", "$.asset.version"))

    if "scene" in document:
        check_index(document["scene"], arrays["scenes"], "scenes", "$.scene", issues)
    elif "scenes" not in document:
        pass

    for scene_index, scene in enumerate(arrays["scenes"]):
        if isinstance(scene, dict) and "nodes" in scene:
            check_index_list(scene["nodes"], arrays["nodes"], "nodes", f"$.scenes[{scene_index}].nodes", issues)

    for node_index, node in enumerate(arrays["nodes"]):
        if not isinstance(node, dict):
            issues.append(issue("TYPE", "Node must be an object", f"$.nodes[{node_index}]"))
            continue
        if "children" in node:
            check_index_list(node["children"], arrays["nodes"], "nodes", f"$.nodes[{node_index}].children", issues)
        if "mesh" in node:
            check_index(node["mesh"], arrays["meshes"], "meshes", f"$.nodes[{node_index}].mesh", issues)
        if "skin" in node:
            check_index(node["skin"], arrays["skins"], "skins", f"$.nodes[{node_index}].skin", issues)
            if "mesh" not in node:
                issues.append(issue("NODE_SKIN_MESH", "Node with skin must also define mesh", f"$.nodes[{node_index}]"))
        if "camera" in node:
            check_index(node["camera"], arrays["cameras"], "cameras", f"$.nodes[{node_index}].camera", issues)
        if "matrix" in node and any(key in node for key in ("translation", "rotation", "scale")):
            issues.append(issue("NODE_TRANSFORM", "Node must not mix matrix with TRS properties", f"$.nodes[{node_index}]"))

    for mesh_index, mesh in enumerate(arrays["meshes"]):
        if not isinstance(mesh, dict):
            issues.append(issue("TYPE", "Mesh must be an object", f"$.meshes[{mesh_index}]"))
            continue
        primitives = mesh.get("primitives")
        if not isinstance(primitives, list) or not primitives:
            issues.append(issue("MESH_PRIMITIVES", "Mesh must contain at least one primitive", f"$.meshes[{mesh_index}].primitives"))
            continue
        target_counts = []
        for primitive_index, primitive in enumerate(primitives):
            primitive_path = f"$.meshes[{mesh_index}].primitives[{primitive_index}]"
            if not isinstance(primitive, dict):
                issues.append(issue("TYPE", "Primitive must be an object", primitive_path))
                continue
            attributes = primitive.get("attributes")
            if not isinstance(attributes, dict) or not attributes:
                issues.append(issue("PRIMITIVE_ATTRIBUTES", "Primitive must contain attributes", f"{primitive_path}.attributes"))
            else:
                joints = {key.split("_", 1)[1] for key in attributes if key.startswith("JOINTS_")}
                weights = {key.split("_", 1)[1] for key in attributes if key.startswith("WEIGHTS_")}
                if joints != weights:
                    issues.append(issue("SKIN_ATTRIBUTES", "JOINTS_n and WEIGHTS_n attribute sets must match", f"{primitive_path}.attributes"))
                for name, value in sorted(attributes.items()):
                    check_index(value, arrays["accessors"], "accessors", f"{primitive_path}.attributes.{name}", issues)
            if "indices" in primitive:
                check_index(primitive["indices"], arrays["accessors"], "accessors", f"{primitive_path}.indices", issues)
            if "material" in primitive:
                check_index(primitive["material"], arrays["materials"], "materials", f"{primitive_path}.material", issues)
            if "targets" in primitive:
                targets = primitive["targets"]
                if not isinstance(targets, list):
                    issues.append(issue("TYPE", "Primitive targets must be an array", f"{primitive_path}.targets"))
                else:
                    target_counts.append(len(targets))
                    for target_index, target in enumerate(targets):
                        if isinstance(target, dict):
                            for name, value in sorted(target.items()):
                                check_index(value, arrays["accessors"], "accessors", f"{primitive_path}.targets[{target_index}].{name}", issues)
            elif target_counts:
                target_counts.append(0)
        if len(set(target_counts)) > 1:
            issues.append(issue("MORPH_TARGETS", "All primitives in a mesh must have the same number of morph targets", f"$.meshes[{mesh_index}].primitives"))

    for material_index, material in enumerate(arrays["materials"]):
        if not isinstance(material, dict):
            issues.append(issue("TYPE", "Material must be an object", f"$.materials[{material_index}]"))
            continue
        material_path = f"$.materials[{material_index}]"
        pbr = material.get("pbrMetallicRoughness")
        if isinstance(pbr, dict):
            for key in ("baseColorTexture", "metallicRoughnessTexture"):
                if key in pbr:
                    check_texture_info(pbr[key], arrays["textures"], f"{material_path}.pbrMetallicRoughness.{key}", issues)
        for key in ("normalTexture", "occlusionTexture", "emissiveTexture"):
            if key in material:
                check_texture_info(material[key], arrays["textures"], f"{material_path}.{key}", issues)

    for texture_index, texture in enumerate(arrays["textures"]):
        if isinstance(texture, dict):
            if "source" in texture:
                check_index(texture["source"], arrays["images"], "images", f"$.textures[{texture_index}].source", issues)
            if "sampler" in texture:
                check_index(texture["sampler"], arrays["samplers"], "samplers", f"$.textures[{texture_index}].sampler", issues)

    asset_dir = asset_path.parent.resolve()
    for buffer_index, buffer in enumerate(arrays["buffers"]):
        if not isinstance(buffer, dict):
            issues.append(issue("TYPE", "Buffer must be an object", f"$.buffers[{buffer_index}]"))
            continue
        if "uri" in buffer:
            check_uri(buffer["uri"], "buffer", f"$.buffers[{buffer_index}].uri", asset_dir, root, data_uri_limit, issues, dependencies)
        elif container.get("kind") == "glb" and buffer_index == 0:
            bin_chunks = [chunk for chunk in container.get("chunks", []) if chunk.get("type") == "BIN"]
            byte_length = buffer.get("byteLength")
            if not bin_chunks:
                issues.append(issue("GLB_BIN", "First GLB buffer without uri requires a BIN chunk", f"$.buffers[{buffer_index}]"))
            elif not isinstance(byte_length, int) or isinstance(byte_length, bool) or byte_length < 0:
                issues.append(issue("GLB_BIN_LENGTH", "First GLB buffer byteLength must be a non-negative integer", f"$.buffers[{buffer_index}].byteLength"))
            elif bin_chunks[0].get("length", 0) < byte_length:
                issues.append(issue("GLB_BIN_LENGTH", "BIN chunk must not be shorter than first buffer byteLength", f"$.buffers[{buffer_index}].byteLength"))
            elif bin_chunks[0].get("length", 0) > byte_length + 3:
                issues.append(issue("GLB_BIN_LENGTH", "BIN chunk may be at most 3 padding bytes longer than first buffer byteLength", f"$.buffers[{buffer_index}].byteLength"))
    for buffer_view_index, buffer_view in enumerate(arrays["bufferViews"]):
        if isinstance(buffer_view, dict):
            if "buffer" in buffer_view:
                check_index(buffer_view["buffer"], arrays["buffers"], "buffers", f"$.bufferViews[{buffer_view_index}].buffer", issues)
            else:
                issues.append(issue("BUFFER_VIEW", "BufferView must reference a buffer", f"$.bufferViews[{buffer_view_index}].buffer"))

    for accessor_index, accessor in enumerate(arrays["accessors"]):
        if isinstance(accessor, dict):
            if "bufferView" in accessor:
                check_index(accessor["bufferView"], arrays["bufferViews"], "bufferViews", f"$.accessors[{accessor_index}].bufferView", issues)
            sparse = accessor.get("sparse")
            if isinstance(sparse, dict):
                indices = sparse.get("indices")
                values = sparse.get("values")
                if isinstance(indices, dict) and "bufferView" in indices:
                    check_index(indices["bufferView"], arrays["bufferViews"], "bufferViews", f"$.accessors[{accessor_index}].sparse.indices.bufferView", issues)
                if isinstance(values, dict) and "bufferView" in values:
                    check_index(values["bufferView"], arrays["bufferViews"], "bufferViews", f"$.accessors[{accessor_index}].sparse.values.bufferView", issues)

    for image_index, image in enumerate(arrays["images"]):
        if not isinstance(image, dict):
            issues.append(issue("TYPE", "Image must be an object", f"$.images[{image_index}]"))
            continue
        has_uri = "uri" in image
        has_buffer_view = "bufferView" in image
        if has_uri and has_buffer_view:
            issues.append(issue("IMAGE_SOURCE", "Image must not define both uri and bufferView", f"$.images[{image_index}]"))
        if has_uri:
            check_uri(image["uri"], "image", f"$.images[{image_index}].uri", asset_dir, root, data_uri_limit, issues, dependencies)
        if has_buffer_view:
            check_index(image["bufferView"], arrays["bufferViews"], "bufferViews", f"$.images[{image_index}].bufferView", issues)
            if "mimeType" not in image:
                issues.append(issue("IMAGE_MIME", "Image with bufferView must define mimeType", f"$.images[{image_index}].mimeType"))

    for skin_index, skin in enumerate(arrays["skins"]):
        if isinstance(skin, dict):
            if "joints" in skin:
                check_index_list(skin["joints"], arrays["nodes"], "nodes", f"$.skins[{skin_index}].joints", issues)
            else:
                issues.append(issue("SKIN_JOINTS", "Skin must define joints", f"$.skins[{skin_index}].joints"))
            if "inverseBindMatrices" in skin:
                check_index(skin["inverseBindMatrices"], arrays["accessors"], "accessors", f"$.skins[{skin_index}].inverseBindMatrices", issues)
            if "skeleton" in skin:
                check_index(skin["skeleton"], arrays["nodes"], "nodes", f"$.skins[{skin_index}].skeleton", issues)

    for animation_index, animation in enumerate(arrays["animations"]):
        if not isinstance(animation, dict):
            issues.append(issue("TYPE", "Animation must be an object", f"$.animations[{animation_index}]"))
            continue
        samplers = animation.get("samplers", [])
        channels = animation.get("channels", [])
        if not isinstance(samplers, list):
            issues.append(issue("TYPE", "Animation samplers must be an array", f"$.animations[{animation_index}].samplers"))
            samplers = []
        if not isinstance(channels, list):
            issues.append(issue("TYPE", "Animation channels must be an array", f"$.animations[{animation_index}].channels"))
            channels = []
        for sampler_index, sampler in enumerate(samplers):
            if isinstance(sampler, dict):
                if "input" in sampler:
                    check_index(sampler["input"], arrays["accessors"], "accessors", f"$.animations[{animation_index}].samplers[{sampler_index}].input", issues)
                if "output" in sampler:
                    check_index(sampler["output"], arrays["accessors"], "accessors", f"$.animations[{animation_index}].samplers[{sampler_index}].output", issues)
        seen_targets: set[tuple[int | None, str | None]] = set()
        for channel_index, channel in enumerate(channels):
            channel_path = f"$.animations[{animation_index}].channels[{channel_index}]"
            if not isinstance(channel, dict):
                continue
            if "sampler" in channel:
                check_index(channel["sampler"], samplers, "animation.samplers", f"{channel_path}.sampler", issues)
            target = channel.get("target")
            if isinstance(target, dict):
                if "node" in target:
                    check_index(target["node"], arrays["nodes"], "nodes", f"{channel_path}.target.node", issues)
                key = (target.get("node") if isinstance(target.get("node"), int) else None, target.get("path") if isinstance(target.get("path"), str) else None)
                if key in seen_targets:
                    issues.append(issue("ANIMATION_TARGET", "Animation channels must not target the same node/path more than once", f"{channel_path}.target"))
                seen_targets.add(key)

    inventory = {name: len(arrays[name]) for name in TOP_LEVEL_ARRAYS}
    inventory["meshPrimitives"] = primitive_count(arrays["meshes"])
    return inventory, issues, dependencies


def inspect(path: Path, root: Path, data_uri_limit: int, max_file_bytes: int) -> tuple[dict[str, Any], int]:
    if not path.is_file():
        raise PreflightError(f"Input is not a file: {path}")
    try:
        file_size = path.stat().st_size
    except OSError as exc:
        raise PreflightError(f"Could not stat input: {exc}") from exc
    if file_size > max_file_bytes:
        raise PreflightError(f"Input has {file_size} bytes, over max file limit {max_file_bytes}")
    suffix = path.suffix.lower()
    parse_issues: list[dict[str, str]] = []
    if suffix == ".glb":
        document, container, parse_issues = read_glb_json(path)
    elif suffix == ".gltf":
        document, container = read_gltf_json(path)
    else:
        raise PreflightError("Input extension must be .gltf or .glb")

    inventory, validation_issues, dependencies = inspect_document(document, path.resolve(), root.resolve(), data_uri_limit, container)
    all_issues = parse_issues + validation_issues
    result = {
        "tool": "inspect_gltf.py",
        "scope": "bounded glTF/GLB structural and dependency preflight; not a substitute for Khronos glTF Validator, DCC/engine import, or visual QA",
        "input": {"path": str(path), "format": container["kind"]},
        "container": container,
        "asset": document.get("asset", {}) if isinstance(document.get("asset"), dict) else {},
        "inventory": inventory,
        "dependencies": dependencies,
        "issues": all_issues,
        "ok": not any(item.get("severity") == "error" for item in all_issues),
    }
    return result, EXIT_VALIDATION if not result["ok"] else EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect .gltf JSON or .glb v2 JSON chunks for bounded preflight issues.")
    parser.add_argument("input", help="Path to a .gltf or .glb file")
    parser.add_argument("--root", help="Allowed dependency root. Defaults to the input file directory.")
    parser.add_argument("--data-uri-limit", type=int, default=DEFAULT_DATA_URI_LIMIT, help="Maximum decoded bytes allowed for one data URI")
    parser.add_argument("--max-file-bytes", type=int, default=DEFAULT_MAX_FILE_BYTES, help="Maximum input file size in bytes")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    input_path = Path(args.input).resolve()
    root = Path(args.root).resolve() if args.root else input_path.parent.resolve()
    try:
        if args.data_uri_limit < 0:
            raise PreflightError("--data-uri-limit must be nonnegative")
        if args.max_file_bytes < 0:
            raise PreflightError("--max-file-bytes must be nonnegative")
        result, exit_code = inspect(input_path, root, args.data_uri_limit, args.max_file_bytes)
    except PreflightError as exc:
        result = {"tool": "inspect_gltf.py", "input": {"path": str(input_path)}, "ok": False, "issues": [issue("OPERATIONAL", str(exc), "$", "fatal")]}
        exit_code = EXIT_OPERATIONAL
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())