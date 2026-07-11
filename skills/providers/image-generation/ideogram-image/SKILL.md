---
name: ideogram-image
description: Generate, remix, edit, inpaint, reframe, background-process, describe, layerize, and upscale images with the Ideogram Developer API. Use when Codex must integrate Ideogram 4.0 or 3.0, render reliable typography or structured layouts, use style or character references, build synchronous or webhook workflows, migrate legacy Ideogram endpoints, or reason about Ideogram API pricing, safety, privacy, and production QA.
---

# Ideogram Image

Use the official Developer API directly and treat the checked date below as part of the contract.

## Evidence labels and refresh rule

- **Documented**: stated by an Ideogram first-party page or the official OpenAPI document.
- **Inference**: a conclusion not guaranteed by the published contract.
- **Production heuristic**: operational advice, not an Ideogram promise.
- Treat model availability, endpoint lifecycle, prices, limits, policy, and ephemeral URL lifetime as volatile. Re-check the [documentation index](https://developer.ideogram.ai/llms.txt), [OpenAPI 3.1 JSON](https://developer.ideogram.ai/openapi.json), [pricing](https://ideogram.ai/api-pricing/), [API agreement](https://ideogram.ai/legal/api-tos), [usage policy](https://ideogram.ai/legal/usage-policy), and [privacy policy](https://ideogram.ai/legal/privacy) before a release or quote.

Unless a paragraph says otherwise, API facts below are **Documented — checked 2026-07-09**.

## Select a route, not an invented model string

| Need | Canonical route | Effective model/lifecycle |
|---|---|---|
| New text/layout generation | `POST /v1/ideogram-v4/generate` | Ideogram 4.0; current flagship API route |
| Asynchronous new generation | `POST /v1/ideogram-v4/async/generate` | Ideogram 4.0; webhook plus polling |
| V4 image-guided change | `POST /v1/ideogram-v4/remix` | Ideogram 4.0 |
| Style/character references, mask edit, reframe, replacement background | `/v1/ideogram-v3/*` routes below | Ideogram 3.0; current specialized routes |
| Prompt-only multi-image edit | `POST /v1/edit` | Current instructional-edit route; docs expose V3 resolution controls but no request model field |
| Older body-selected generation | `/generate`, `/edit`, `/remix`, `/reframe` | Explicitly labeled legacy in the reference; avoid for new work |

Do not send `model` to V4 or V3 route-scoped endpoints. Their model identifiers are the route segments `ideogram-v4` and `ideogram-v3`. The legacy `ModelEnum` accepts `V_1`, `V_1_TURBO`, `V_2`, `V_2_TURBO`, `V_2A`, `V_2A_TURBO`, or `AUTO`; it does not expose V3/V4. The generic Describe route accepts `V_2`, `V_3`, or `V_4`. A V3 custom model is addressed by `custom_model_uri` in the form `model/<model_name>/version/<version_name>`.

The official reference explicitly says `POST /v1/ideogram-v3/edit` is legacy and will be removed; migrate it to `/v1/ideogram-v3/inpaint`. No first-party API retirement date is published for V3 or the remaining legacy routes. The app model history says 0.1 and 0.2 are retired, but those are not current API request IDs. Do not infer an API retirement schedule from the app history.

## Authenticate and establish the wire contract

Use base URL `https://api.ideogram.ai`. Send the secret only as `Api-Key: <key>`. API billing/account setup is separate from Ideogram app subscriptions. The full key is shown only once when created.

**Production heuristic:** read the key from `IDEOGRAM_API_KEY`, redact it from logs, use a secret manager in deployed systems, and set connect/read timeouts. The environment-variable name is a client convention, not an Ideogram-defined name.

Most current operations use `multipart/form-data`; let the HTTP library set its boundary. V4 Magic Prompt uses JSON. All successful generation/edit responses return URLs, not embedded image bytes. Download every wanted result immediately: first-party docs say image links expire but do not publish a fixed lifetime. There is no documented output-format selector; do not promise PNG/JPEG from the URL suffix. Inspect response headers/bytes after download.

## Use only documented operations

### Current image and vision surface

| Method and path | Required request | Optional request | Success shape |
|---|---|---|---|
| `POST /v1/ideogram-v4/generate` | exactly one of form `text_prompt:string` or `json_prompt:V4JsonPrompt` | `resolution:ResolutionV4`, `rendering_speed`, `enable_copyright_detection:boolean|null` | `ImageGenerationResponseV4` |
| `POST /v1/ideogram-v4/async/generate?webhook_url=<https-url>` | same V4 form; HTTPS webhook query required | same V4 options | `{generation_id:string}` |
| `GET /v1/generations/{generation_id}` | URL-safe base64 generation ID | none | pending/failed status or completed data |
| `POST /v1/ideogram-v4/remix` | form `image:file`, `text_prompt:string` | `image_weight:1..100`, V4 resolution/speed/copyright detection | `ImageGenerationResponseV4` |
| `POST /v1/ideogram-v4/magic-prompt` | JSON `text_prompt:string` | `aspect_ratio:AspectRatioV4=AUTO` | `{json_prompt:V4JsonPrompt, aspect_ratio}` |
| `POST /v1/ideogram-v4/describe` | form `image_file:file` (JPEG/PNG/WebP, max 10 MB) | `include_bbox:boolean=true` | `{json_prompt:V4JsonPrompt}` |
| `POST /v1/ideogram-v3/generate` | form `prompt:string` | V3 generation/style/reference fields below | `ImageGenerationResponseV3` |
| `POST /v1/ideogram-v3/generate-transparent` | form `prompt:string` | `seed`, `upscale_factor:X1|X2|X4=X1`, `aspect_ratio`, speed except FLASH, Magic Prompt, negative prompt, count | V3 image response |
| `POST /v1/ideogram-v3/inpaint` | form `image:file`, same-sized black/white `mask:file`, `prompt:string` | Magic Prompt, count, seed, speed, V3 style/reference fields | V3 image response |
| `POST /v1/ideogram-v3/remix` | form `image:file`, `prompt:string` | `image_weight=50`, seed, size, speed, Magic Prompt, negative prompt, count, style/reference fields | V3 image response |
| `POST /v1/ideogram-v3/reframe` | form `image:file`, `resolution:ResolutionV3` | count, seed, speed, preset/palette/style code/reference | V3 image response |
| `POST /v1/ideogram-v3/replace-background` | form `image:file`, `prompt:string` | Magic Prompt, count, seed, speed, preset/palette/style code/reference | V3 image response |
| `POST /v1/remove-background` | form `image:file` | none | `{created, data:[{url:string|null,is_image_safe:boolean}]}`; one entry |
| `POST /v1/ideogram-v3/layerize-text` | form `image:file` | `prompt:string`, `seed` | see documentation ambiguity below |
| `POST /v1/edit` | form `prompt:string` plus `images:file[]` or `image_urls:string[]` when editing inputs | count, seed, Magic Prompt, V3 resolution or aspect ratio, `transparent_background=false` | `{created,data:V1EditImageObject[]}` |
| `POST /upscale` | form `image_file:file`, `image_request` JSON object | object fields `prompt`, `resemblance=50`, `detail=50`, `magic_prompt_option`, `num_images=1`, `seed` | legacy-shaped image response |
| `POST /describe` | form `image_file:file` | `describe_model_version:V_2|V_3|V_4=V_3` | `{descriptions:[{text:string}]}` |

All uploaded image fields above accept JPEG, PNG, or WebP and are limited to 10 MB unless `/v1/edit` is used: that route accepts up to 10 uploaded images, each up to 10 MB, or up to 10 Ideogram image URLs. V3 style-reference and character-reference groups have a 10 MB total per group. The V3 API currently supports one character reference image; corresponding optional grayscale masks must match reference count and dimensions.

The OpenAPI also documents custom-model administration: `GET/POST /datasets`, `GET /datasets/{dataset_id}`, `POST /datasets/{dataset_id}/upload_assets`, `POST /v1/ideogram-v3/train-model`, `GET /models`, and `GET /models/{model_id}`. The current train-route/OpenAPI contract requires 15–100 dataset images, while the first-party tutorial says training can start at 10. Use at least 15 unless Ideogram resolves the conflict, validate before the $40 run, and record the live schema used. `model_name` is 5–30 alphanumeric/space/hyphen characters. Use these operations only for an explicit custom-model task.

Legacy-only documented operations are `POST /generate`, `/v1/ideogram-v3/edit`, `/edit`, `/remix`, and `/reframe`. Preserve them only while migrating; do not invent undocumented `v4/edit`, `v4/inpaint`, `v4/reframe`, or `v4/replace-background` routes.

### Exact shared schemas

`V4JsonPrompt`:

```json
{
  "high_level_description": "required string",
  "style_description": {
    "aesthetics": "optional string",
    "art_style": "optional string",
    "lighting": "optional string",
    "medium": "optional string",
    "photo": "optional string"
  },
  "compositional_deconstruction": {
    "background": "required string",
    "elements": [
      {"type": "obj", "desc": "required string", "bbox": [0, 0, 1000, 1000]},
      {"type": "text", "text": "required literal string", "desc": "required string", "bbox": [0, 0, 1000, 1000]}
    ]
  }
}
```

Require `high_level_description`, `compositional_deconstruction.background`, and `elements`. Require `type` plus `desc` for objects; require `type`, literal `text`, and `desc` for text. `style_description` and each `bbox` are optional. Interpret a bbox as four normalized integers `[y_min,x_min,y_max,x_max]` on a 1000×1000 coordinate system. The prose defines four values in `[0,1000]`; the published JSON Schema does not encode `minItems`, `maxItems`, or numeric bounds, so validate them client-side.

V4 resolutions are exactly:

```text
2048x2048, 1440x2880, 2880x1440, 1664x2496, 2496x1664, 1792x2240,
2240x1792, 1440x2560, 2560x1440, 1600x2560, 2560x1600, 1728x2304,
2304x1728, 1296x3168, 3168x1296, 1152x2944, 2944x1152, 1248x3328,
3328x1248, 1280x3072, 3072x1280, 1024x3072, 3072x1024
```

V4 Magic Prompt aspect ratios are `AUTO`, `1x4`, `1x3`, `1x2`, `9x16`, `10x16`, `2x3`, `3x4`, `4x5`, `1x1`, `5x4`, `4x3`, `3x2`, `16x10`, `16x9`, `2x1`, `3x1`, `4x1`.

V3 aspect ratios are `1x3`, `3x1`, `1x2`, `2x1`, `9x16`, `16x9`, `10x16`, `16x10`, `2x3`, `3x2`, `3x4`, `4x3`, `4x5`, `5x4`, `1x1`. Do not send V3 `aspect_ratio` with `resolution`; the default ratio is `1x1`. `ResolutionV3` is the exact 69-value enum in the [OpenAPI schema](https://developer.ideogram.ai/openapi.json); validate against that live enum instead of approximating arbitrary dimensions.

V3 `num_images` is 1–8, default 1. V3 `seed` is 0–2147483647. V4 generate/remix expose neither count nor request seed; the response returns a seed. Do not infer a controllable count from example response arrays.

`rendering_speed` is `FLASH|TURBO|DEFAULT|QUALITY`, default `DEFAULT`. **Volatile documented exception:** V4 currently returns 400 for `FLASH`; transparent-background generation also rejects `FLASH`. V3 style type is `AUTO|GENERAL|REALISTIC|DESIGN|FICTION`, default `GENERAL`. V3 Magic Prompt is `AUTO|ON|OFF`.

V3 style presets are exactly:

```text
80S_ILLUSTRATION, 90S_NOSTALGIA, ABSTRACT_ORGANIC, ANALOG_NOSTALGIA, ART_BRUT,
ART_DECO, ART_POSTER, AURA, AVANT_GARDE, BAUHAUS, BLUEPRINT, BLURRY_MOTION,
BRIGHT_ART, C4D_CARTOON, CHILDRENS_BOOK, COLLAGE, COLORING_BOOK_I, COLORING_BOOK_II,
CUBISM, DARK_AURA, DOODLE, DOUBLE_EXPOSURE, DRAMATIC_CINEMA, EDITORIAL,
EMOTIONAL_MINIMAL, ETHEREAL_PARTY, EXPIRED_FILM, FLAT_ART, FLAT_VECTOR,
FOREST_REVERIE, GEO_MINIMALIST, GLASS_PRISM, GOLDEN_HOUR, GRAFFITI_I, GRAFFITI_II,
HALFTONE_PRINT, HIGH_CONTRAST, HIPPIE_ERA, ICONIC, JAPANDI_FUSION, JAZZY,
LONG_EXPOSURE, MAGAZINE_EDITORIAL, MINIMAL_ILLUSTRATION, MIXED_MEDIA, MONOCHROME,
NIGHTLIFE, OIL_PAINTING, OLD_CARTOONS, PAINT_GESTURE, POP_ART, RETRO_ETCHING,
RIVIERA_POP, SPOTLIGHT_80S, STYLIZED_RED, SURREAL_COLLAGE, TRAVEL_POSTER,
VINTAGE_GEO, VINTAGE_POSTER, WATERCOLOR, WEIRD, WOODBLOCK_PRINT
```

Use one color-palette variant: `{"name":"EMBER|FRESH|JUNGLE|MAGIC|MELON|MOSAIC|PASTEL|ULTRAMARINE"}` or `{"members":[{"color_hex":"#RRGGBB","color_weight":0.05..1.0}]}`. Use 8-character hexadecimal `style_codes`. Do not combine `style_codes` with `style_reference_images` or `style_type`.

Common V4 success:

```json
{"created":"date-time","data":[{"url":"uri or null","prompt":"string","resolution":"ResolutionV4","is_image_safe":true,"seed":12345}],"response_type":"url"}
```

Common V3 success adds optional `upscaled_resolution` and `style_type`; require `created`, `data`, and per item `prompt`, `resolution`, `is_image_safe`, `seed`. When `is_image_safe` is false, `url` is empty/null. Polling requires `generation_id`, `status:pending|completed|failed`, and `created`; only completed responses contain `response_type:"url"` and `data`.

Ancillary exact responses: `/upscale` returns `{created, request_id?, data?}` using legacy `ImageObject` entries; `/describe` returns `{descriptions:[{text?:string}]}`; `/v1/ideogram-v4/describe` returns `{json_prompt:V4JsonPrompt}`; `/v1/remove-background` returns `{created,data:[{url?:string|null,is_image_safe:boolean}]}` with exactly one item. The OpenAPI leaves `descriptions` and each `text` formally optional even though normal examples include them, so validate their presence before use.

## Control text, layout, style, and references

For V4 typography, prefer `json_prompt` and place exact copy in a `type:"text"` element's `text`; describe font class, weight, case, color, alignment, and role in `desc`; use bbox for layout. `text_prompt` automatically enables Magic Prompt, while `json_prompt` bypasses it and is consumed directly. Generate structured JSON first with `/v1/ideogram-v4/magic-prompt`, or recover it from an image with `/v1/ideogram-v4/describe`.

No first-party API schema publishes a maximum prompt length, maximum literal-text length, guaranteed font catalog, or exact-spelling SLA. Do not invent one. **Production heuristic:** keep critical copy short, isolate each copy region, avoid contradictory visual text elsewhere, render variants, and verify exact spelling with OCR plus human review.

For V3, put literal display copy clearly in the prompt and choose `DESIGN` when appropriate. Use `style_preset` for known aesthetics, style references for visual transfer, a character reference for identity consistency, and Remix `image_weight` for source preservation. Do not claim the V4 Generate route accepts V3 style/character reference fields; it does not in the current OpenAPI.

For inpainting, make the mask the same dimensions as the input and mark editable pixels black. For reframe, specify a V3 resolution, not an aspect-ratio field. For replacement background, describe only the desired new background while preserving the foreground subject.

## Execute complete examples

The following are **examples**, not a universal client architecture. They make paid calls only when deliberately run with a funded key.

### Example: synchronous V4 structured typography and durable download

**Production intent:** create a 1:1 campaign poster whose headline matters more than stylistic randomness. **Why this structure:** use `json_prompt` to bypass automatic Magic Prompt rewriting, isolate literal copy, and place it explicitly. **Expected result:** one or more safe response items with exact headline candidates and a 2048×2048 result. **Likely failures:** misspelled copy, bbox crowding, null URL after safety checks, or an expiring download. **Meaningful variations:** change only `desc` to test typography while holding `text` fixed, or use `/magic-prompt` first when composition is exploratory.

```python
import hashlib
import json
import os
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

API = "https://api.ideogram.ai"
KEY = os.environ["IDEOGRAM_API_KEY"]
prompt = {
    "high_level_description": "A premium square coffee poster with one centered headline.",
    "style_description": {"medium": "screen-printed poster", "aesthetics": "minimal, warm"},
    "compositional_deconstruction": {
        "background": "Flat cream paper with subtle grain.",
        "elements": [{
            "type": "text",
            "text": "MORNING, MADE BOLD",
            "desc": "Large centered uppercase condensed black headline",
            "bbox": [360, 100, 600, 900],
        }],
    },
}
with requests.Session() as session:
    response = session.post(
        f"{API}/v1/ideogram-v4/generate",
        headers={"Api-Key": KEY},
        files={
            "json_prompt": (None, json.dumps(prompt)),
            "resolution": (None, "2048x2048"),
            "rendering_speed": (None, "TURBO"),
        },
        timeout=(10, 180),
    )
    response.raise_for_status()
    manifest = {"request": {"json_prompt": prompt, "resolution": "2048x2048",
                            "rendering_speed": "TURBO"}, "results": []}
    signatures = {
        "image/png": (b"\x89PNG\r\n\x1a\n", ".png"),
        "image/jpeg": (b"\xff\xd8\xff", ".jpg"),
        "image/webp": (b"RIFF", ".webp"),
    }
    for index, item in enumerate(response.json()["data"], start=1):
        if not item["is_image_safe"] or not item.get("url"):
            raise RuntimeError(f"Ideogram candidate {index} is unusable")
        with session.get(item["url"], timeout=(10, 60), stream=True) as download:
            download.raise_for_status()
            limit = 50 * 1024 * 1024
            declared = int(download.headers.get("content-length", "0") or 0)
            if declared > limit:
                raise RuntimeError("Declared image exceeds local 50 MiB safety limit")
            body = bytearray()
            for chunk in download.iter_content(1024 * 1024):
                body.extend(chunk)
                if len(body) > limit:
                    raise RuntimeError("Streaming image exceeded local 50 MiB safety limit")
            raw = bytes(body)
            media_type = download.headers.get("content-type", "").split(";", 1)[0].lower()
        if media_type not in signatures or not raw.startswith(signatures[media_type][0]):
            raise RuntimeError(f"Unexpected image payload: {media_type}")
        if media_type == "image/webp" and raw[8:12] != b"WEBP":
            raise RuntimeError("RIFF payload is not WebP")
        with Image.open(BytesIO(raw)) as decoded:
            decoded.verify()
        with Image.open(BytesIO(raw)) as decoded:
            actual_size = decoded.size
        expected_size = tuple(map(int, item["resolution"].lower().split("x")))
        if actual_size != expected_size:
            raise RuntimeError(f"Expected {expected_size}, decoded {actual_size}")
        output = Path(f"poster-{index}{signatures[media_type][1]}")
        temporary = output.with_suffix(output.suffix + ".tmp")
        temporary.write_bytes(raw)
        temporary.replace(output)
        manifest["results"].append({**item, "path": str(output),
                                    "download_content_type": media_type,
                                    "sha256": hashlib.sha256(raw).hexdigest()})
    Path("poster.metadata.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
```

### Example: V3 inpaint with a style reference

**Production intent:** replace only a selected object while borrowing an approved visual style. **Why this structure:** V3 Inpaint is the documented mask route and accepts repeated style-reference parts. **Expected result:** two candidates that preserve pixels outside the black mask. **Likely failures:** inverted mask semantics, dimension mismatch, visible seams, or style drift. **Meaningful variations:** omit the style reference for a neutral edit, or add the single supported character reference plus a matching grayscale reference mask when identity is required.

```python
import hashlib
import json
import os
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

API = "https://api.ideogram.ai"
image_path, mask_path, style_path = map(Path, ("input.png", "mask.png", "style.png"))
mime_by_format = {"PNG": "image/png", "JPEG": "image/jpeg", "WEBP": "image/webp"}
formats = {}
for path in (image_path, mask_path, style_path):
    if path.stat().st_size > 10 * 1024 * 1024:
        raise ValueError(f"{path} exceeds 10 MB")
    with Image.open(path) as check:
        check.verify()
        if check.format not in mime_by_format:
            raise ValueError(f"Unsupported image format for {path}: {check.format}")
        formats[path] = check.format
with Image.open(image_path) as source_check, Image.open(mask_path) as mask_check:
    if source_check.size != mask_check.size:
        raise ValueError("mask must match input dimensions")
    if mask_check.mode not in {"1", "L"}:
        raise ValueError("mask must be binary/grayscale")
    if set(mask_check.convert("L").getdata()) - {0, 255}:
        raise ValueError("mask must contain only black and white pixels")
if style_path.stat().st_size > 10 * 1024 * 1024:
    raise ValueError("style-reference group exceeds 10 MB")
with image_path.open("rb") as image, mask_path.open("rb") as mask, style_path.open("rb") as style:
    response = requests.post(
        f"{API}/v1/ideogram-v3/inpaint",
        headers={"Api-Key": os.environ["IDEOGRAM_API_KEY"]},
        data={"prompt": "Replace only the black mask region with a red enamel teapot", "num_images": "2", "seed": "42"},
        files=[("image", (image_path.name, image, mime_by_format[formats[image_path]])),
               ("mask", (mask_path.name, mask, mime_by_format[formats[mask_path]])),
               ("style_reference_images", (style_path.name, style, mime_by_format[formats[style_path]]))],
        timeout=(10, 180),
    )
response.raise_for_status()
payload = response.json()
manifest = {
    "endpoint": "/v1/ideogram-v3/inpaint",
    "request": {"prompt": "Replace only the black mask region with a red enamel teapot", "num_images": 2, "seed": 42},
    "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (image_path, mask_path, style_path)},
    "results": [],
}
for index, item in enumerate(payload["data"], start=1):
    if not item["is_image_safe"] or not item.get("url"):
        raise RuntimeError(f"Candidate {index} is not usable")
    with requests.get(item["url"], timeout=(10, 60), stream=True) as download:
        download.raise_for_status()
        limit = 50 * 1024 * 1024
        declared = int(download.headers.get("content-length", "0") or 0)
        if declared > limit:
            raise RuntimeError("Declared image exceeds local 50 MiB safety limit")
        body = bytearray()
        for chunk in download.iter_content(1024 * 1024):
            body.extend(chunk)
            if len(body) > limit:
                raise RuntimeError("Streaming image exceeded local 50 MiB safety limit")
        raw = bytes(body)
        media_type = download.headers.get("content-type", "").split(";", 1)[0].lower()
    signatures = {"image/png": (b"\x89PNG\r\n\x1a\n", ".png"),
                  "image/jpeg": (b"\xff\xd8\xff", ".jpg"),
                  "image/webp": (b"RIFF", ".webp")}
    if media_type not in signatures or not raw.startswith(signatures[media_type][0]):
        raise RuntimeError(f"Unexpected output type: {media_type}")
    if media_type == "image/webp" and raw[8:12] != b"WEBP":
        raise RuntimeError("RIFF payload is not WebP")
    with Image.open(BytesIO(raw)) as decoded:
        decoded.verify()
    with Image.open(BytesIO(raw)) as decoded:
        actual_size = decoded.size
    expected_size = tuple(map(int, item["resolution"].lower().split("x")))
    if actual_size != expected_size:
        raise RuntimeError(f"Expected {expected_size}, decoded {actual_size}")
    output = Path(f"inpaint-{index}{signatures[media_type][1]}")
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_bytes(raw)
    temporary.replace(output)
    manifest["results"].append({**item, "path": str(output), "content_type": media_type,
                                "sha256": hashlib.sha256(raw).hexdigest()})
Path("inpaint.metadata.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
```

### Example: submit V4 async and poll safely

**Production intent:** submit work without holding an HTTP connection open and recover even if webhook delivery fails. **Why this structure:** persist the server-issued ID and make polling a bounded fallback. **Expected result:** `pending` transitions to `completed` with downloadable data, or to terminal `failed`. **Likely failures:** non-public webhook URL, throttling, dropped delivery, or an indefinitely pending job. **Meaningful variations:** let a verified webhook complete the record first and have polling become reconciliation rather than the primary completion path.

```python
import hashlib
import json
import os
import random
import time
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

API = "https://api.ideogram.ai"
headers = {"Api-Key": os.environ["IDEOGRAM_API_KEY"]}
webhook_url = os.environ["IDEOGRAM_WEBHOOK_URL"]
if not webhook_url.startswith("https://"):
    raise ValueError("IDEOGRAM_WEBHOOK_URL must be public HTTPS")
accepted = requests.post(
    f"{API}/v1/ideogram-v4/async/generate",
    params={"webhook_url": webhook_url},
    headers=headers,
    files={"text_prompt": (None, "A crisp editorial photograph of a red bicycle")},
    timeout=(10, 30),
)
accepted.raise_for_status()
generation_id = accepted.json()["generation_id"]
Path("async.accepted.json").write_text(json.dumps({
    "generation_id": generation_id,
    "submitted_unix": int(time.time()),
    "webhook_url_sha256": hashlib.sha256(webhook_url.encode("utf-8")).hexdigest(),
}, indent=2), encoding="utf-8")
deadline = time.monotonic() + 10 * 60
completed = False
for attempt in range(40):
    if time.monotonic() >= deadline:
        break
    try:
        result = requests.get(
            f"{API}/v1/generations/{generation_id}", headers=headers, timeout=(10, 30)
        )
    except (requests.Timeout, requests.ConnectionError):
        time.sleep(min(30, 2 ** min(attempt, 5)) + random.random())
        continue
    if result.status_code == 429:
        time.sleep(min(30, 2 ** min(attempt, 5)) + random.random())
        continue
    if result.status_code in {500, 502, 503, 504}:
        time.sleep(min(30, 2 ** min(attempt, 5)) + random.random())
        continue
    result.raise_for_status()
    payload = result.json()
    if payload["status"] == "completed":
        manifest = {"generation_id": generation_id, "results": []}
        for index, item in enumerate(payload["data"], start=1):
            if not item["is_image_safe"] or not item.get("url"):
                raise RuntimeError(f"Completed candidate {index} is unusable")
            with requests.get(item["url"], timeout=(10, 60), stream=True) as download:
                download.raise_for_status()
                limit = 50 * 1024 * 1024
                declared = int(download.headers.get("content-length", "0") or 0)
                if declared > limit:
                    raise RuntimeError("Declared image exceeds local 50 MiB safety limit")
                body = bytearray()
                for chunk in download.iter_content(1024 * 1024):
                    body.extend(chunk)
                    if len(body) > limit:
                        raise RuntimeError("Streaming image exceeded local 50 MiB safety limit")
                raw = bytes(body)
                media_type = download.headers.get("content-type", "").split(";", 1)[0].lower()
            signatures = {"image/png": (b"\x89PNG\r\n\x1a\n", ".png"),
                          "image/jpeg": (b"\xff\xd8\xff", ".jpg"),
                          "image/webp": (b"RIFF", ".webp")}
            if media_type not in signatures or not raw.startswith(signatures[media_type][0]):
                raise RuntimeError(f"Unexpected output type: {media_type}")
            if media_type == "image/webp" and raw[8:12] != b"WEBP":
                raise RuntimeError("RIFF payload is not WebP")
            with Image.open(BytesIO(raw)) as decoded:
                decoded.verify()
            with Image.open(BytesIO(raw)) as decoded:
                actual_size = decoded.size
            expected_size = tuple(map(int, item["resolution"].lower().split("x")))
            if actual_size != expected_size:
                raise RuntimeError(f"Expected {expected_size}, decoded {actual_size}")
            output = Path(f"async-{index}{signatures[media_type][1]}")
            temporary = output.with_suffix(output.suffix + ".tmp")
            temporary.write_bytes(raw)
            temporary.replace(output)
            manifest["results"].append({**item, "path": str(output), "content_type": media_type,
                                        "sha256": hashlib.sha256(raw).hexdigest()})
        Path("async.metadata.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        completed = True
        break
    if payload["status"] == "failed":
        raise RuntimeError(f"generation failed: {generation_id}")
    time.sleep(min(30, 2 ** min(attempt, 5)) + random.random())
if not completed:
    raise TimeoutError(f"generation still pending at deadline: {generation_id}")
```

### Example: verify and durably accept an Ideogram webhook

**Production intent:** authenticate the raw delivery before storing it, reject stale or mismatched requests, and acknowledge duplicates idempotently. **Why this structure:** Ideogram signs raw bytes and may redeliver; SQLite stands in for a transactional production datastore. **Expected result:** a valid first delivery is stored once and returns HTTP 204; a valid duplicate also returns 204 without duplicate processing. **Likely failures:** stale timestamp, bad hex, unknown/rotated key, body reserialization, mismatched generation ID, or invalid JSON. **Meaningful variation:** replace SQLite with a transactional unique constraint in the application's durable database and queue a worker after commit.

```python
import base64
import hashlib
import json
import sqlite3
import time

import requests
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

JWKS_URL = "https://api.ideogram.ai/v1/.well-known/jwks.json"
H_GENERATION = "X-Ideogram-Webhook-Generation-Id"
H_USER = "X-Ideogram-Webhook-User-Id"
H_TIMESTAMP = "X-Ideogram-Webhook-Timestamp"
H_KEY = "X-Ideogram-Webhook-Key-Id"
H_SIGNATURE = "X-Ideogram-Webhook-Signature"
_JWKS_CACHE = {"keys": None, "expires": 0.0}


def b64url_decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def fetch_jwks(*, force_refresh: bool = False, ttl_seconds: int = 300) -> list[dict]:
    now = time.monotonic()
    if not force_refresh and _JWKS_CACHE["keys"] is not None and now < _JWKS_CACHE["expires"]:
        return _JWKS_CACHE["keys"]
    response = requests.get(JWKS_URL, timeout=(5, 15))
    response.raise_for_status()
    keys = response.json()["keys"]
    _JWKS_CACHE.update({"keys": keys, "expires": now + ttl_seconds})
    return keys


def verify_with_keys(keys: list[dict], key_hint: str, signature: bytes, message: bytes) -> bool:
    ordered = sorted(keys, key=lambda key: 0 if key.get("kid") == key_hint else 1)
    for key in ordered:
        if key.get("kty") != "OKP" or key.get("crv") != "Ed25519" or not key.get("x"):
            continue
        try:
            Ed25519PublicKey.from_public_bytes(b64url_decode(key["x"])).verify(signature, message)
            return True
        except (InvalidSignature, ValueError):
            continue
    return False


def verify_delivery(headers, raw_body: bytes, *, max_age_seconds: int = 300) -> dict:
    required = [H_GENERATION, H_USER, H_TIMESTAMP, H_KEY, H_SIGNATURE]
    missing = [name for name in required if not headers.get(name)]
    if missing:
        raise ValueError(f"Missing webhook headers: {missing}")
    timestamp = int(headers[H_TIMESTAMP])
    if abs(int(time.time()) - timestamp) > max_age_seconds:
        raise ValueError("Stale webhook timestamp")
    signature_hex = headers[H_SIGNATURE]
    if signature_hex != signature_hex.lower():
        raise ValueError("Signature must be lowercase hexadecimal")
    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError as exc:
        raise ValueError("Invalid signature hexadecimal") from exc
    body_hash = hashlib.sha256(raw_body).hexdigest()
    message = "\n".join([
        headers[H_GENERATION], headers[H_USER], headers[H_TIMESTAMP], body_hash
    ]).encode("utf-8")
    keys = fetch_jwks()
    if not verify_with_keys(keys, headers[H_KEY], signature, message):
        # Refresh once so key rotation does not require a process restart.
        if not verify_with_keys(fetch_jwks(force_refresh=True), headers[H_KEY], signature, message):
            raise ValueError("Webhook signature verification failed")
    payload = json.loads(raw_body)
    if payload.get("generation_id") != headers[H_GENERATION]:
        raise ValueError("Header/body generation_id mismatch")
    return payload


def handle_webhook(headers, raw_body: bytes, database_path="ideogram-webhooks.sqlite") -> int:
    payload = verify_delivery(headers, raw_body)
    generation_id = payload["generation_id"]
    with sqlite3.connect(database_path) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS deliveries (
            generation_id TEXT PRIMARY KEY, payload_json TEXT NOT NULL,
            received_unix INTEGER NOT NULL, status TEXT NOT NULL
        )""")
        db.execute(
            "INSERT OR IGNORE INTO deliveries VALUES (?, ?, ?, 'received')",
            (generation_id, json.dumps(payload, separators=(",", ":")), int(time.time())),
        )
    # Framework adapter should return this after commit; a worker processes 'received' rows.
    return 204
```

Install `requests`, `Pillow`, and `cryptography` for the four Python examples. The web framework must pass the untouched request-body bytes and original headers into `handle_webhook`; do not parse and reserialize first.

Verify webhook signatures exactly as specified in the [official webhook guide](https://developer.ideogram.ai/ideogram-api/webhooks): hash the raw body bytes with SHA-256; join generation ID, user ID, Unix timestamp, and body hash with newlines; verify the lowercase-hex Ed25519 signature against keys from `GET /v1/.well-known/jwks.json`. Never reserialize JSON before hashing. **Production heuristic:** cache keys, refresh on failure/rotation, reject stale timestamps using a locally chosen tolerance, require header/body ID agreement, and deduplicate deliveries transactionally by `generation_id`.

## Handle lifecycle, errors, retries, and concurrency

The default limit is **10 in-flight requests**; contact Ideogram for higher-volume access. A limit is concurrency, not a documented requests-per-minute quota.

| Status | Documented meaning | Action |
|---|---|---|
| 400 | invalid input; also current unsupported speed combinations | fix request; do not retry unchanged |
| 401 | missing/invalid authorization | stop, repair secret/account |
| 402 | insufficient credits/quota on `/v1/edit` | fund or change approved plan; do not loop |
| 403 | forbidden or not authorized on documented routes such as V3 Remix/Upscale | stop; verify account entitlement and route access; do not retry unchanged |
| 404 | unknown async generation ID | verify stored ID/environment |
| 422 | prompt or image safety failure; documented body `{ "error": "string" }` | do not evade; revise or reject according to policy |
| 429 | too many requests | reduce in-flight work and retry with bounded exponential jitter |
| 503 | temporary service unavailable on selected routes such as `/v1/edit` | bounded retry after backoff |

The OpenAPI leaves most 400/401/429/503 bodies untyped. Parse defensively and log status, request metadata, and a redacted/truncated body. It does not document a `Retry-After` guarantee; honor it if actually present, otherwise use full jitter.

No request idempotency-key header is documented. **Production heuristic:** never blindly retry a timed-out synchronous POST because it may have completed and been billed. Prefer V4 async, persist `generation_id` before doing other work, and retry only polling GETs. Ideogram may retry a webhook a limited number of times and delivery is not guaranteed; acknowledge successful duplicate deliveries with 2xx and fall back to polling.

## Price and gate spend

**Volatile documented prices — page last says revised 2025-08-06; checked 2026-07-09:** V4 Turbo/Default/Quality cost $0.03/$0.06/$0.10 per output; V3 Flash/Turbo/Default/Quality cost $0.03/$0.03/$0.06/$0.09; V3 with character reference Turbo/Default/Quality costs $0.10/$0.15/$0.20. Transparent V3 X1 costs $0.04/$0.07/$0.10 for Turbo/Default/Quality; 2X costs $0.16/$0.19/$0.22; 4X costs $0.20/$0.23/$0.26. Instructional edit is $0.20/output, upscale $0.06/input, Describe $0.01/input, Layerize $0.09/input, and self-serve custom-model training $40/run. Confirm the live page before estimating.

The price page also lists pricing-only or incompletely routed capabilities: Gemini generation at $0.20 for 1K/2K and $0.36 for 4K; Topaz upscale at $0.12/$0.24/$0.48 for 2K/4K/8K; Generate + Layerize V3 at $0.12/$0.15/$0.18 for Turbo/Default/Quality; and custom inference at V4 $0.06/$0.12/$0.20 and V3 $0.06/$0.12/$0.18. Do not invent endpoints for these entries. The current public OpenAPI does not expose routes for every pricing-table capability and documents only V3 `custom_model_uri`; treat them as unresolved until a first-party request schema is available to the target account.

Compute the upper bound before submission: requested outputs × per-output price, plus reference/upscale/edit premiums. Keep API auto-top-up behavior visible to the operator; setup docs describe configurable threshold/top-up balances and separate API credits.

## Enforce safety, privacy, provenance, and rights

Follow the API agreement and usage policy, not merely `is_image_safe`. Do not submit unlawful, infringing, non-consensual, privacy-invasive, pornographic, excessively violent, hateful, deceptive, bullying, political-campaigning/lobbying, or harmful/criminal content. Do not bypass filters or rate limits.

Obtain rights and consent for every uploaded image, character reference, likeness, trademark, and font/brand asset. Ideogram's general Terms say it does not claim ownership in user input/output and does not restrict commercial use, but the user remains responsible for law and third-party rights; output may be non-unique and no non-infringement warranty is provided. Treat this as operational guidance, not legal advice.

The API agreement requires the Developer Application to identify Ideogram-generated output (for example, “Powered by Ideogram”), display approved Ideogram marks where access is enabled, and link users to the Usage Policy. It prohibits presenting AI output as entirely human-made or as a real photo of a real event. Preserve a provenance record containing provider, endpoint/model route, UTC time, request parameters, returned prompt/seed/resolution, source hashes/rights, output hash, safety result, and human approvals. No C2PA field or downloadable provenance manifest is documented in the current response schema; do not claim one.

API input/output is not used to train the Ideogram model except content flagged for Usage Policy violations may be used to train/improve abuse and safety detection. The broader Privacy Policy says prompts/uploads are collected and gives a purpose-based, non-numeric retention period (“as long as reasonably necessary”). It also permits service providers and international processing. Therefore do not send health data, children's data, secrets, or sensitive personal data without a reviewed lawful basis and required consent. Do not promise zero retention or a fixed deletion window absent an order-specific agreement.

`enable_copyright_detection=true` opts a V3/V4 request into additional Hive likeness/logo checks unless the organization setting already enables them; it adds latency, and flagged images return `is_image_safe:false`. Treat this as an extra signal, not legal clearance.

## Run QA and migrate safely

Before sending:

1. Re-fetch the OpenAPI enum for routes, sizes, and presets in release automation.
2. Validate file type/size, mask dimensions, count, seed, mutually exclusive fields, and V4 bbox ordering/ranges.
3. Require approval for cost, references/likenesses, public distribution, and policy-sensitive prompts.
4. Store a redacted canonical request and source hashes before submission.

After receiving:

1. Reject missing URLs and unsafe results; download ephemeral URLs immediately.
2. Verify MIME signature, pixel dimensions, alpha channel when requested, and cryptographic hash.
3. Compare literal typography by OCR and human review; compare reference identity/style without assuming perfect fidelity.
4. For edits, diff protected regions; for inpaint, inspect mask seams; for reframe, inspect subject preservation and new edges; for background work, inspect hair/transparency halos.
5. Record endpoint, returned prompt, seed, actual resolution, price basis, and review outcome.

Migration map:

- Move `/v1/ideogram-v3/edit` and `/edit` mask workflows to `/v1/ideogram-v3/inpaint`; rename `image_file` to `image` and use black editable regions.
- Move legacy `/generate` to V4 Generate for new text/layout work or V3 Generate when V3 references/presets/custom models are required.
- Move legacy `/remix` and `/reframe` to `/v1/ideogram-v4/remix` or their V3 canonical routes according to required controls.
- Replace legacy `model`/`magic_prompt_option`/prefixed aspect-ratio enums with route-scoped models and the exact current field names.
- Canary each migration with frozen prompts/assets, compare dimensions, literal text, style, subject preservation, safety behavior, latency, and cost; never assume seed equivalence across model generations.

## Known first-party ambiguities

- The custom-model tutorial says at least 10 dataset images, while the current train-route/OpenAPI contract says 15–100. Enforce the stricter 15-image minimum and recheck immediately before a paid training run.
- The OpenAPI `WebhookUrl` component says the webhook body mirrors the synchronous response with `request_id`, while the async endpoint schema and dedicated webhook guide use `generation_id`. Follow the dedicated guide/header contract and require matching `generation_id`; treat `request_id` wording as stale until resolved.
- The Layerize Text prose and example show `text_blocks` with font/position/style data, while the current OpenAPI `LayerizeTextResponse` schema declares only `base_image_url`, optional `original_image_url`, and `seed`. Code to the declared schema and feature-detect `text_blocks`; do not make it required until Ideogram resolves the mismatch.
- The API overview V3 quickstart shows a JSON body for a route whose reference/OpenAPI declares multipart form. Follow the route reference/OpenAPI, especially when sending files.
- V4 response examples show multiple data items but the request schema has no `num_images`; do not treat example cardinality as a guarantee.
- Pricing describes V4 pricing across several operation classes, while current OpenAPI exposes V4 Generate/Remix but retains V3-only paths for inpaint/reframe/replace-background. Choose by documented route availability, not pricing-table wording.

## First-party sources

- [Developer API overview](https://developer.ideogram.ai/ideogram-api/api-overview)
- [API setup](https://developer.ideogram.ai/ideogram-api/api-setup)
- [Official OpenAPI JSON](https://developer.ideogram.ai/openapi.json)
- [V4 Generate](https://developer.ideogram.ai/api-reference/api-reference/generate-v4)
- [V4 async Generate](https://developer.ideogram.ai/api-reference/api-reference/generate-v4-async)
- [Webhooks](https://developer.ideogram.ai/ideogram-api/webhooks)
- [V3 Inpaint](https://developer.ideogram.ai/api-reference/api-reference/inpaint-v3)
- [V3 Generate](https://developer.ideogram.ai/api-reference/api-reference/generate-v3)
- [API pricing](https://ideogram.ai/api-pricing/)
- [Developer API Agreement and Policy](https://ideogram.ai/legal/api-tos)
- [Usage Policy](https://ideogram.ai/legal/usage-policy)
- [Privacy Policy](https://ideogram.ai/legal/privacy)
- [Terms of Service](https://ideogram.ai/legal/tos)
