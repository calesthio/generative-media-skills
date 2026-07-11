---
name: stability-ai-image
description: Operate Stability AI image generation, image-to-image, edit, control, background, and upscale APIs safely and reproducibly. Use when selecting or calling Stable Image Ultra, Core, Stable Diffusion 3.5, v2beta image edit/control services, or Stability open-weight image models; when debugging schemas, moderation, rate limits, cost, lifecycle, licenses, privacy, provenance, or migrations; and when planning production QA for Stability-generated images.
---

# Stability AI Image Production

Use this skill to choose the correct Stability AI image surface, make schema-correct calls, preserve production evidence, and avoid confusing the hosted API with self-hosted weights.

## Evidence legend and freshness

- **Documented** means stated by a linked first-party Stability AI source or the live first-party OpenAPI document.
- **Inference** means a conclusion drawn from documented behavior; verify it when the consequence matters.
- **Production heuristic** means operational advice, not a provider guarantee.
- Volatile API facts in this skill were verified **2026-07-09**. Re-check the [API reference](https://platform.stability.ai/docs/api-reference), [pricing](https://platform.stability.ai/pricing), and [release notes](https://platform.stability.ai/docs/release-notes) before committing spend or shipping a long-lived integration.

## Route the job before writing a prompt

1. Decide between hosted and self-hosted execution.
   - Use the hosted Platform API for managed Stable Image services, edits, controls, upscalers, moderation, and provider-signed provenance.
   - Use open weights only when local data control, custom inference, fine-tuning, or deployment control justifies operating the model and its license obligations.
   - Do not imply that Stable Image Core or all Stable Image microservices are downloadable weights. The downloadable SD3.5 checkpoints and the hosted service catalog overlap only partly.
2. Match the intent to one operation rather than forcing every job through generation.
3. Confirm output size, input constraints, cost, and synchronous/asynchronous behavior.
4. Confirm rights, consent, privacy, and the current Acceptable Use Policy before uploading source images.
5. Generate a small approved sample before a batch. Record endpoint, parameters, seed returned by the API, request ID, input hashes, output hash, cost estimate, and policy/QA disposition.

## Current hosted surface

**Documented, verified 2026-07-09:** REST `v2beta` is the primary feature surface. Stability says REST v1, gRPC, and v2alpha remain maintained but receive no new features or parameters; it recommends changing equivalent v2alpha URLs to v2beta. Treat legacy APIs as maintenance/migration surfaces, not sources for new designs. [API reference](https://platform.stability.ai/docs/api-reference)

### Generate

| Service | Endpoint | Choose it for | Output | Current price |
|---|---|---|---|---|
| Stable Image Ultra | `POST /v2beta/stable-image/generate/ultra` | Highest-tier managed generation; also accepts an optional init image | 1 MP; 1024x1024 at 1:1 | 8 credits |
| Stable Image Core | `POST /v2beta/stable-image/generate/core` | Low-cost, fast managed text-to-image iteration | 1.5 MP | 3 credits |
| SD3.5 suite | `POST /v2beta/stable-image/generate/sd3` | Explicit base-model choice and `cfg_scale`; text-to-image or image-to-image | 1 MP; 1024x1024 at 1:1 | Large 6.5, Large Turbo 4, Medium 3.5, Flash 2.5 credits |

The documented SD3.5 identifiers are `sd3.5-large`, `sd3.5-large-turbo`, `sd3.5-medium`, and `sd3.5-flash`. Large is the default. The provider describes Turbo and Flash as four-step distilled variants. **Documentation inconsistency:** the API prose and pricing list Flash, while the downloadable OpenAPI `model` enum omitted `sd3.5-flash` when checked. If Flash matters, validate it with one low-cost call in the target account before batching and handle `400` without silently changing models. [API reference](https://platform.stability.ai/docs/api-reference), [pricing](https://platform.stability.ai/pricing)

### Edit

| Operation | Endpoint | Required fields | Important optional fields | Output / price |
|---|---|---|---|---|
| Erase | `/v2beta/stable-image/edit/erase` | `image`; mask file or image alpha determines the region | `mask`, `grow_mask` 0-20 default 5, `seed`, `output_format` | 4 MP / 5 credits |
| Inpaint | `/v2beta/stable-image/edit/inpaint` | `image`, `prompt`; mask file or alpha determines the region | `mask`, `negative_prompt`, `grow_mask` 0-100 default 5, `style_preset`, `seed`, `output_format` | 4 MP / 5 credits |
| Outpaint | `/v2beta/stable-image/edit/outpaint` | `image` and at least one nonzero direction | `left`, `right`, `up`, `down` each 0-2000; `prompt`; `creativity` 0-1 default .5; `style_preset`, `seed`, `output_format` | 4 credits |
| Search and Replace | `/v2beta/stable-image/edit/search-and-replace` | `image`, replacement `prompt`, `search_prompt` | `negative_prompt`, `grow_mask` 0-20 default 3, `style_preset`, `seed`, `output_format` | 4 MP / 5 credits |
| Search and Recolor | `/v2beta/stable-image/edit/search-and-recolor` | `image`, recolor `prompt`, `select_prompt` | `negative_prompt`, `grow_mask` 0-20 default 3, `style_preset`, `seed`, `output_format` | input resolution / 5 credits |
| Remove Background | `/v2beta/stable-image/edit/remove-background` | `image` | `output_format` is only `png` or `webp` | transparent-capable output / 5 credits |
| Replace Background and Relight | `/v2beta/stable-image/edit/replace-background-and-relight` | `subject_image` plus `background_prompt` and/or `background_reference` | `foreground_prompt`, `negative_prompt`, `preserve_original_subject` 0-1 default .6, `original_background_depth` 0-1 default .5, `keep_original_background`, `light_source_direction`, `light_reference`, `light_source_strength` 0-1 default .3, `seed`, `output_format` | asynchronous / 8 credits |

For masks, **documented:** black preserves, white edits at maximum strength, and gray supplies partial strength. An explicit `mask` overrides the image alpha channel. If no explicit mask is supplied, transparent pixels are edited and opaque pixels are preserved. A differently sized mask is resized automatically. Prefer a same-size mask anyway so QA can reason about exact boundaries. [API reference](https://platform.stability.ai/docs/api-reference)

**Specification defect, verified 2026-07-09:** the downloadable OpenAPI marks an undeclared `prompt` as required for Erase, while the endpoint prose and official sample require only `image` and optionally `mask`. Follow the prose/sample. If the service returns a schema error, log the response `id` and re-check the live reference instead of inventing a prompt.

### Control

| Operation | Endpoint | Request | Control semantics | Output / price |
|---|---|---|---|---|
| Sketch | `/v2beta/stable-image/control/sketch` | required `image`, `prompt`; optional `control_strength`, negative prompt, seed, style, format | contours/edges guide the result; strength 0-1 default .7 | input resolution / 5 credits |
| Structure | `/v2beta/stable-image/control/structure` | same schema as Sketch | input composition/structure guides the result; strength 0-1 default .7 | input resolution / 5 credits |
| Style Guide | `/v2beta/stable-image/control/style` | required style `image`, `prompt`; optional `aspect_ratio`, `fidelity`, negative prompt, seed, preset, format | reference style guides a newly generated composition; fidelity 0-1 default .5 | 1 MP / 5 credits |
| Style Transfer | `/v2beta/stable-image/control/style-transfer` | required `init_image`, `style_image`; optional prompt, negative prompt, seed, format | transforms existing content while preserving composition; `style_strength` default 1, `composition_fidelity` default .9, `change_strength` default .9 | 1 MP at init aspect / 8 credits |

Use Sketch for line/edge intent, Structure for layout/geometry, Style Guide to create new content in a reference aesthetic, and Style Transfer to restyle existing content. Do not promise identity, exact pixel layout, logo fidelity, or deterministic style copying; verify each requirement visually.

### Upscale

| Operation | Endpoint | Request and limits | Behavior | Output / price |
|---|---|---|---|---|
| Fast | `/v2beta/stable-image/upscale/fast` | `image`; width and height 32-1536, total 1,024-1,048,576 pixels | 4x dimensions, lightweight enhancement | API reference says maximum 16 MP / 2 credits |
| Conservative | `/v2beta/stable-image/upscale/conservative` | `image`, `prompt`; image at least 64 per side, 4,096-9,437,184 pixels, aspect 1:2.5-2.5:1 | aims to preserve rather than reinterpret; `creativity` documented base range .2-.5, default .35 | 4 MP / 40 credits |
| Creative | `/v2beta/stable-image/upscale/creative` | `image`, `prompt`; input at least 64 per side and no more than 1,048,576 pixels | heavy reimagining for degraded sub-1-MP inputs; creativity .1-.5 default .3 | asynchronous / 60 credits |

Do not use Creative when exact product geometry, faces, text, evidence, or faithful restoration matters. **Production heuristic:** compare Fast first, Conservative second, and Creative only when reinterpretation is acceptable. The current pricing page and live OpenAPI agree on 60 credits for Creative; older indexed prose may still show 40, so quote the pricing page at approval time.

**Current documentation conflict:** the Fast Upscaler API reference describes a maximum 16 MP output, while the current pricing page says maximum 4 MP. Treat 4 MP as the conservative budget/delivery promise until a target-account probe and current support guidance establish otherwise; record the input dimensions and reject an unexpected result size.

**Documentation inconsistency:** the Fast endpoint reference says 4x dimensions up to 16 MP, while the current pricing description says up to 4 MP. Do not contract a maximum from marketing copy; preflight representative dimensions against the live endpoint and verify the returned file before batching. Creative is described as reaching “4K,” but the schema does not promise one exact width-by-height pair. Outpaint and Relight likewise do not publish a fixed output-resolution guarantee in their operation summaries.

## Exact transport and response contract

### Authentication and headers

Use base URL `https://api.stability.ai`. Send:

```text
Authorization: Bearer <STABILITY_API_KEY>
Accept: image/*
```

All image POST bodies are `multipart/form-data`. Let the HTTP library set `Content-Type` and its boundary; do not hard-code `multipart/form-data`. Optional diagnostic headers are `stability-client-id`, `stability-client-user-id`, and `stability-client-version`, each at most 256 characters. Obfuscate the end-user ID. Store keys in a secret manager or environment variable and never ship one in browser code. [API key guidance](https://kb.stability.ai/knowledge-base/where-can-i-find-my-api-key)

**Documented access and price basis, verified 2026-07-09:** create a Platform account and key; new accounts are advertised with 25 trial credits, an account may hold up to 10 active keys, and 1 credit is currently $0.01. Pricing can change. Use separate keys for environments, but use the same key that started an async generation to fetch its result. Check the account balance and current pricing immediately before approval. [API key guidance](https://kb.stability.ai/knowledge-base/where-can-i-find-my-api-key), [pricing](https://platform.stability.ai/pricing)

Use `Accept: image/*` for binary bytes or `Accept: application/json` for base64 JSON. For a synchronous success:

- Binary response: image bytes; read `content-type`, `x-request-id`, `finish-reason`, and `seed` headers.
- JSON response: `{ "image": "<base64>", "seed": 343940597, "finish_reason": "SUCCESS" }`.
- `finish-reason` / `finish_reason` is `SUCCESS` or `CONTENT_FILTERED`. Treat filtered output as failed QA even if HTTP is 200.

For common errors, expect JSON shaped as `{ "id": "...", "name": "...", "errors": ["..."] }`. Persist the response `id` for support without persisting secrets or sensitive source content.

### Common fields and constraints

- `prompt`: 1-10,000 characters where required. Some edit/control prompts document `(word:weight)` with weights from 0 to 1.
- `negative_prompt`: at most 10,000 characters.
- `seed`: 0-4,294,967,294. Omit it or send `0` for a random seed. Persist the **returned** seed, not only the requested value.
- `output_format`: `png`, `jpeg`, or `webp`, except Remove Background supports only `png` or `webp`.
- Generated aspect ratios: `21:9`, `16:9`, `3:2`, `5:4`, `1:1`, `4:5`, `2:3`, `9:16`, `9:21`; default `1:1`.
- Style presets: `enhance`, `anime`, `photographic`, `digital-art`, `comic-book`, `fantasy-art`, `line-art`, `analog-film`, `neon-punk`, `isometric`, `low-poly`, `origami`, `modeling-compound`, `cinematic`, `3d-model`, `pixel-art`, `tile-texture`. The provider says this list may change.
- Uploaded images are JPEG, PNG, or WebP. Most edit/control inputs require at least 64 pixels per side and 4,096-9,437,184 total pixels; many also require aspect ratio 1:2.5-2.5:1. Remove Background caps total pixels at 4,194,304. Apply each endpoint's schema, not a single universal rule.
- Request payloads are capped at 10 MiB for these v2beta image calls.

For SD3.5 text-to-image, `aspect_ratio` is valid; for image-to-image, instead send `mode=image-to-image`, `image`, and `strength` 0-1. Strength 0 preserves the input and 1 approaches no-image conditioning. `cfg_scale` is 1-10; documented defaults are 4 for Large/Medium and 1 for Turbo/Flash. Stability recommends .94-.97 strength for Flash image-to-image. Ultra accepts optional `image` plus `strength` without the SD3.5 `mode` field. Core is text-to-image only in the documented schema.

### Synchronous versus asynchronous

All listed calls are synchronous HTTP 200 image responses **except** Creative Upscale and Replace Background and Relight:

1. POST the multipart request.
2. Parse `{ "id": "<64-character generation id>" }`.
3. Poll `GET /v2beta/results/{id}` with the **same API key**.
4. Wait at least 10 seconds between polls. `202` means in progress; `200` returns the result; `404` means the ID is wrong, belongs to another key, or expired.
5. Download immediately. Results are retained for 24 hours, then deleted.

The docs label the asynchronous start response as HTTP 200, despite some older client habits expecting 202. Accept the documented status for the image endpoints and require an `id` body. Do not treat general Platform input/output retention as 24 hours: that documented period applies to async result retrieval only.

## Complete executable example: one production-shaped Python client

This is an example, not a mandatory architecture. It covers a synchronous Core generation, masked Inpaint, and asynchronous Creative Upscale. It intentionally does not auto-retry ambiguous paid POST failures because the API documents no idempotency key.

```python
import base64
import hashlib
import json
import os
import sys
import time
from contextlib import ExitStack
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests
from PIL import Image

BASE = "https://api.stability.ai"
KEY = os.environ["STABILITY_API_KEY"]
SESSION = requests.Session()
SESSION.headers.update({
    "authorization": f"Bearer {KEY}",
    "stability-client-id": "image-pipeline",
    "stability-client-version": "1.0.0",
})


class StabilityError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def retry_after_seconds(value: str | None) -> float:
    if not value:
        return 60.0
    try:
        return max(60.0, float(value))
    except ValueError:
        try:
            when = parsedate_to_datetime(value)
            if when.tzinfo is None:
                when = when.replace(tzinfo=timezone.utc)
            return max(60.0, (when - datetime.now(timezone.utc)).total_seconds())
        except (TypeError, ValueError, OverflowError):
            return 60.0


def error_payload(response: requests.Response) -> dict:
    try:
        body = response.json()
        return body if isinstance(body, dict) else {"body": body}
    except ValueError:
        return {"body": response.text[:1000]}


def fail(response: requests.Response, context: str) -> None:
    payload = error_payload(response)
    request_id = payload.get("id") or response.headers.get("x-request-id")
    raise StabilityError(
        f"{context}: HTTP {response.status_code}; request_id={request_id}; "
        f"error={json.dumps(payload, ensure_ascii=False)}"
    )


def detect_image_type(raw: bytes) -> str:
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if raw.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if len(raw) >= 12 and raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return "image/webp"
    raise StabilityError("Output does not have a recognized PNG, JPEG, or WebP signature")


def write_image(response: requests.Response, output: Path) -> dict:
    transport_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
    if transport_type == "application/json":
        payload = response.json()
        encoded = payload.get("image")
        if not isinstance(encoded, str) or not encoded:
            raise StabilityError("JSON success response is missing image base64")
        try:
            raw = base64.b64decode(encoded, validate=True)
        except Exception as exc:
            raise StabilityError("JSON image field is not valid base64") from exc
        seed = payload.get("seed")
        finish_reason = payload.get("finish_reason")
    elif transport_type.startswith("image/"):
        raw = response.content
        seed = response.headers.get("seed")
        finish_reason = response.headers.get("finish-reason")
    else:
        raise StabilityError(f"Unexpected success content-type: {transport_type}")
    if finish_reason != "SUCCESS":
        raise StabilityError(f"Generation finished as {finish_reason}; do not publish")
    if len(raw) < 100:
        raise StabilityError("Image payload is implausibly small")
    image_type = detect_image_type(raw)
    if transport_type.startswith("image/") and transport_type != image_type:
        raise StabilityError(f"Header says {transport_type}, bytes are {image_type}")
    allowed_suffixes = {
        "image/png": {".png"},
        "image/jpeg": {".jpg", ".jpeg"},
        "image/webp": {".webp"},
    }
    if output.suffix.lower() not in allowed_suffixes[image_type]:
        raise StabilityError(f"Output extension {output.suffix} does not match {image_type}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(raw)
    return {
        "path": str(output),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "seed": seed,
        "request_id": response.headers.get("x-request-id"),
        "transport_content_type": transport_type,
        "image_content_type": image_type,
    }


def request_manifest(endpoint: str, data: dict, file_paths: dict, context: dict) -> dict:
    return {
        "endpoint": endpoint,
        "service": context["service"],
        "model": context["model"],
        "credit_estimate": context["credits"],
        "request_fields": dict(data),
        "requested_seed": data.get("seed"),
        "input_sha256": {name: sha256_file(path) for name, path in file_paths.items()},
        "policy_qa_disposition": "pending human review",
    }


def multipart_files(stack: ExitStack, file_paths: dict) -> dict:
    if not file_paths:
        return {"none": ("", b"")}  # Force a requests-generated multipart boundary.
    return {
        name: stack.enter_context(path.open("rb"))
        for name, path in file_paths.items()
    }


def sync_post(
    endpoint: str, *, data: dict, file_paths: dict, output: Path, context: dict
) -> dict:
    # A 429 is a documented rate-limit rejection; reopen every stream before retrying.
    manifest = request_manifest(endpoint, data, file_paths, context)
    for attempt in range(2):
        with ExitStack() as stack:
            response = SESSION.post(
                BASE + endpoint,
                data=data,
                files=multipart_files(stack, file_paths),
                headers={"accept": "image/*"},
                timeout=(15, 180),
            )
        if response.status_code == 429 and attempt == 0:
            time.sleep(retry_after_seconds(response.headers.get("retry-after")))
            continue
        if response.status_code != 200:
            fail(response, endpoint)
        metadata = write_image(response, output)
        metadata.update(manifest)
        return metadata
    raise AssertionError("unreachable")


def async_post(
    endpoint: str, *, data: dict, file_paths: dict, output: Path, context: dict
) -> dict:
    manifest = request_manifest(endpoint, data, file_paths, context)
    with ExitStack() as stack:
        start = SESSION.post(
            BASE + endpoint,
            data=data,
            files=multipart_files(stack, file_paths),
            headers={"accept": "application/json"},
            timeout=(15, 180),
        )
    if start.status_code != 200:
        fail(start, endpoint)
    generation_id = start.json().get("id")
    if not isinstance(generation_id, str) or len(generation_id) != 64:
        raise StabilityError(f"Missing/invalid async id: {start.text[:500]}")
    deadline = time.monotonic() + 15 * 60
    while time.monotonic() < deadline:
        time.sleep(10)
        result = SESSION.get(
            f"{BASE}/v2beta/results/{generation_id}",
            headers={"accept": "image/*"},
            timeout=(15, 180),
        )
        if result.status_code == 202:
            continue
        if result.status_code != 200:
            fail(result, f"poll {generation_id}")
        metadata = write_image(result, output)
        metadata["generation_id"] = generation_id
        metadata.update(manifest)
        return metadata
    raise TimeoutError(f"Generation {generation_id} did not finish before local deadline")


def run_core() -> dict:
    return sync_post(
        "/v2beta/stable-image/generate/core",
        file_paths={},
        data={
            "prompt": (
                "Editorial product photograph of a matte cobalt travel mug on pale gray stone, "
                "three-quarter view, soft north-window light, restrained shadow, no text"
            ),
            "negative_prompt": "logo, watermark, extra handles, warped rim",
            "aspect_ratio": "4:5",
            "seed": "18472931",
            "output_format": "webp",
        },
        output=Path("outputs/mug-core.webp"),
        context={"service": "Stable Image Core", "model": "managed-core", "credits": 3},
    )


def run_inpaint() -> dict:
    return sync_post(
        "/v2beta/stable-image/edit/inpaint",
        file_paths={"image": Path("inputs/room.png"), "mask": Path("inputs/mask.png")},
        data={
            "prompt": "a low walnut side table matching the room perspective and warm light",
            "negative_prompt": "people, text, floating furniture",
            "grow_mask": "6",
            "seed": "482019",
            "output_format": "png",
        },
        output=Path("outputs/room-inpaint.png"),
        context={"service": "Stable Image Inpaint", "model": "managed-edit", "credits": 5},
    )


def run_creative_upscale() -> dict:
    source = Path("inputs/degraded-portrait.jpg")
    if source.stat().st_size > 9 * 1024 * 1024:
        raise StabilityError("Creative Upscale input exceeds the conservative 9 MiB file gate")
    with Image.open(source) as image:
        width, height = image.size
        if image.format not in {"JPEG", "PNG", "WEBP"}:
            raise StabilityError(f"Unsupported input format: {image.format}")
    pixels = width * height
    if width < 64 or height < 64 or not 4_096 <= pixels <= 1_048_576:
        raise StabilityError(f"Creative Upscale input is outside documented bounds: {width}x{height}")
    return async_post(
        "/v2beta/stable-image/upscale/creative",
        file_paths={"image": source},
        data={
            "prompt": "natural editorial portrait, realistic skin texture, soft daylight",
            "negative_prompt": "plastic skin, altered identity, text, watermark",
            "creativity": "0.2",
            "seed": "92173",
            "output_format": "png",
        },
        output=Path("outputs/portrait-upscaled.png"),
        context={"service": "Creative Upscale", "model": "managed-upscaler", "credits": 60},
    )


if __name__ == "__main__":
    modes = {"core": run_core, "inpaint": run_inpaint, "creative-upscale": run_creative_upscale}
    if len(sys.argv) != 2 or sys.argv[1] not in modes:
        raise SystemExit(f"usage: {sys.argv[0]} {'|'.join(modes)}")
    print(json.dumps(modes[sys.argv[1]](), indent=2))
```

Before running: install `requests` and `Pillow`, set `STABILITY_API_KEY`, create only the input files required by the chosen mode, review current credits, and get approval for paid generation. The Creative example uses a low creativity setting but can still alter identity; do not use it for identity-critical restoration.

## Prompt and control practice

**Production heuristic:** write prompts as an ordered production brief: subject and action; composition/camera; material and lighting; environment; style/finish; exact visible text only when needed. Prefer concrete relationships over adjective piles. Keep negative prompts short and defect-specific; do not copy the whole positive prompt into the negative field.

Use a seed to compare one controlled change, not as a promise of permanent reproducibility. Hosted model/service updates, safety systems, and undocumented backend changes may alter output for the same request. Preserve the input, request fields, returned seed, date, and actual output.

For text in images, quote the exact desired string, specify placement and typography, and budget for manual typesetting if spelling is contractual. For brands and products, use edit/control references only when rights permit, then inspect logos, geometry, labels, and legal marks at 100% zoom. Do not rely on a negative prompt to enforce legal or safety policy.

For outpaint, expand in stages no larger than the source dimensions when practical; the provider explicitly recommends direction values no larger than source dimensions for quality. Inspect the original boundary, perspective continuation, repeating texture, subject duplication, and lighting drift after every stage.

## Failure handling

| Status / condition | Meaning | Action |
|---|---|---|
| 200 + `SUCCESS` | usable transport success | Still run content and technical QA |
| 200 + `CONTENT_FILTERED` | output violated moderation and was blurred | Reject; do not publish or attempt safeguard evasion |
| 400 | invalid parameters/schema | Do not retry unchanged; compare endpoint-specific fields and official reference |
| 401 | missing/invalid key or malformed auth | Stop; validate secret source and `Bearer` formatting; never log the key |
| 403 | moderation/policy flag or permission failure | Stop; review policy and rights; do not automatically paraphrase to evade filtering |
| 413 | request above 10 MiB | Resize/re-encode while respecting endpoint pixel/aspect limits |
| 422 | well-formed but rejected, including documented language/public-figure cases | Read `errors`; change the plan only when lawful and policy-compliant |
| 429 | over 150 requests/10 seconds; documented 60-second timeout | Pause at least 60 seconds, honor `Retry-After`, reduce concurrency, add jitter |
| 500 | internal error | Preserve response ID; retry only within an approved cost/idempotency policy |
| timeout/connection loss after POST | outcome may be ambiguous | Do not blindly repeat a paid POST; check account telemetry/support or obtain approval for possible duplicate spend |
| async 202 | still processing | poll again no sooner than 10 seconds |
| async 404 | wrong key/ID or result expired | verify same key and age; regenerate only with approval |

The public rate limit is 150 requests per 10 seconds; exceeding it returns 429 and a 60-second timeout. Rate limit and cost are different controls: use a token bucket for throughput and a separate per-job credit budget. Stability says failed generations are not charged, but ambiguous network outcomes still warrant conservative retry behavior. [rate-limit guidance](https://kb.stability.ai/knowledge-base/api-key-rate-limit-information)

## Production QA and acceptance

Define acceptance criteria before generation, then score every candidate:

1. **Intent:** subject count, action, framing, required/forbidden elements, exact text.
2. **Anatomy and geometry:** hands, faces, joints, reflections, shadows, perspective, repeated structures, product silhouette.
3. **Edit locality:** intended region changed; protected region did not; no halo, seam, color spill, or texture discontinuity.
4. **Reference fidelity:** composition, style, or subject preservation according to the selected control; do not conflate those goals.
5. **Technical:** dimensions, aspect, alpha, format, color appearance, corruption, and file hash.
6. **Safety and rights:** consent, publicity/privacy, trademark/copyright, minors, sensitive attributes, deceptive context, disclosure.
7. **Provenance:** retain original provider output before metadata-stripping transforms; verify credentials with a C2PA-capable validator when provenance is a delivery requirement.

**Production heuristic:** blind-review a seeded A/B set when choosing model, strength, or control settings. Change one variable at a time. Record reject reasons rather than keeping only winners; failure distributions are useful for batch planning.

## Hosted versus open-weight rights

Do not collapse these regimes:

- **Hosted Platform API:** governed by Stability's current Terms of Service, Acceptable Use Policy, Privacy Policy, and service pricing. As between the user and Stability, the user retains input rights and Stability assigns its rights, if any, in outputs subject to law and compliance. Similar outputs may be generated for others, and the user remains responsible for legality and appropriateness. The Terms prohibit representing AI output as human-generated. [Terms](https://stability.ai/terms-of-service)
- **Self-hosted Core Models:** each model repository's actual license controls. The SD3.5 suite is listed under the Stability AI Community License. It permits research, non-commercial, and limited commercial use; commercial users must register, and the free commercial license terminates when the user and affiliates exceed USD $1M annual revenue, requiring an Enterprise license. Distribution/attribution and AUP duties remain. Do not apply this threshold as the pricing rule for hosted API calls. [license overview](https://stability.ai/license), [SD3.5 Large model card/license](https://huggingface.co/stabilityai/stable-diffusion-3.5-large)
- **Other checkpoints:** do not assume SDXL, older SD releases, fine-tunes, third-party adapters, or community checkpoints use the same license. Inspect the exact model and every bundled component.

This is operational guidance, not legal advice. Escalate high-value, regulated, likeness, training, redistribution, or model-hosting uses to counsel.

## Privacy, safety, and provenance

**Documented:** Stability may use Platform inputs and outputs to improve and develop services and train models, but Platform API users can opt out in the account overview by setting “Training: Improve the Model for Everyone” to “No.” The general Privacy Policy does not promise a universal short retention period for synchronous image inputs/outputs. Do not send secrets, unnecessary personal data, biometric material, or client-confidential imagery based on an assumed 24-hour deletion window. [Privacy Center](https://stability.ai/privacy-center), [Privacy Policy](https://stability.ai/privacypolicy)

**Documented:** hosted APIs apply prompt/output safety filters; release notes describe input filtering, NSFW filtering, known-CSAM filtering through Thorn, C2PA signing, and watermarking. Preserve originals because later conversion, recompression, screenshots, or editing can remove or invalidate provenance signals. Do not claim that a visible watermark or intact C2PA manifest is guaranteed in every derivative. [release notes](https://platform.stability.ai/docs/release-notes), [safety](https://stability.ai/safety)

Require adult users and follow the current AUP. It prohibits rights/privacy violations, child exploitation, sexually explicit content, non-consensual intimate imagery, safeguard circumvention, harmful/deceptive uses, misinformation, and impersonation without consent or legal right. Obtain consent and lawful rights for identifiable people and uploaded references. A successful API response is not legal clearance. [Acceptable Use Policy](https://stability.ai/use-policy)

## Migration and change control

- Stable Diffusion 3.0 identifiers `sd3-large`, `sd3-large-turbo`, and `sd3-medium` have been automatically routed to their SD3.5 counterparts since 2025-04-17. Replace aliases with explicit SD3.5 identifiers so logs reflect the actual intent.
- Stable Diffusion 1.6 API and Stable Video Diffusion API ceased support on 2025-07-24. For old image generation, the provider named SDXL as a migration option, but new work should evaluate Core, Ultra, or SD3.5 against explicit requirements rather than inherit an SDXL assumption.
- Models deprecated 2024-10-11 include `stable-diffusion-512-v2-1`, `stable-diffusion-xl-beta-v2-2-2`, `stable-diffusion-xl-1024-v0-9`, and `esrgan-v1-x2plus`. Do not use those IDs in new examples.
- Before migration, capture a representative golden set; compare prompt adherence, text, identity, geometry, safety outcomes, latency, returned resolution, and credits. Do not silently switch provider, endpoint, model, or fidelity settings in a production batch.
- Pin what is actually pinnable: endpoint path, explicit model, request fields, and client version. Expect managed services such as Core/Ultra to evolve behind stable names.

## Official sources

Verified 2026-07-09:

- [Stability AI v2beta API reference and downloadable OpenAPI](https://platform.stability.ai/docs/api-reference)
- [Platform pricing](https://platform.stability.ai/pricing)
- [API release notes and deprecations](https://platform.stability.ai/docs/release-notes)
- [Stable Image getting started](https://platform.stability.ai/docs/getting-started/stable-image)
- [API key rate limits](https://kb.stability.ai/knowledge-base/api-key-rate-limit-information)
- [API key security and account access](https://kb.stability.ai/knowledge-base/where-can-i-find-my-api-key)
- [Terms of Service](https://stability.ai/terms-of-service)
- [Acceptable Use Policy](https://stability.ai/use-policy)
- [Privacy Policy](https://stability.ai/privacypolicy) and [Privacy Center opt-out instructions](https://stability.ai/privacy-center)
- [Safety and provenance overview](https://stability.ai/safety)
- [Stability AI license overview](https://stability.ai/license)
- [Official SD3.5 Large model card and Community License](https://huggingface.co/stabilityai/stable-diffusion-3.5-large)
- [Official SD3.5 Medium model card](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium)
