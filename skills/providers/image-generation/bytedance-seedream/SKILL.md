---
name: bytedance-seedream
description: Build and operate production image generation and natural-language image editing with ByteDance Seedream through first-party Volcengine Ark (China) or BytePlus ModelArk (global), including model and region selection, multi-reference and grouped outputs, streaming, secure artifact handling, retries, cost controls, prompting, safety, and rights review.
---

# ByteDance Seedream

Use this skill when an application calls Seedream directly through the first-party Ark image-generation API. It covers text-to-image, reference-guided generation, natural-language editing, multi-image fusion, grouped outputs, and streamed grouped outputs. It does not cover Seedance video generation, third-party gateways, consumer apps, model training, or UI automation.

All volatile facts below were checked against first-party documentation on **2026-07-09**. Recheck the linked model catalog, availability, pricing, and retirement pages before a production launch.

## Evidence labels

- **Documented** means a current ByteDance Seed, Volcengine, or BytePlus page states the behavior.
- **Provider claim** means a first-party product or research page makes a qualitative performance claim; treat it as marketing until tested on the application's corpus.
- **Operational recommendation** means a production practice inferred from the documented contract, not a provider guarantee.
- **Unknown** means the first-party pages reviewed do not establish the behavior. Feature-detect or ask support instead of inventing a contract.

## Choose the commercial surface first

Model IDs and hosts are not interchangeable.

| Deployment | API base | Current image model IDs documented on 2026-07-09 | Important boundary |
|---|---|---|---|
| Volcengine Ark, China | `https://ark.cn-beijing.volces.com/api/v3` | `doubao-seedream-5-0-pro-260628`, `doubao-seedream-5-0-260128` (also documented as alias `doubao-seedream-5-0-lite-260128`), `doubao-seedream-4-5-251128`, `doubao-seedream-4-0-250828` | China host and `doubao-...` IDs only |
| BytePlus ModelArk, Asia Pacific | `https://ark.ap-southeast.bytepluses.com/api/v3` | `seedream-5-0-260128` (also documented as alias `seedream-5-0-lite-260128`), `seedream-4-5-251128`, `seedream-4-0-250828` | Global host and non-`doubao` IDs only |
| BytePlus ModelArk, Europe | `https://ark.eu-west.bytepluses.com/api/v3` | Seedream 5.0 Lite is documented for EU; confirm the live catalog before deploying any other version | The availability page prohibits restricted models, including Seedream 4.0, in the EU/EU market |

All three use:

```text
POST {API_BASE}/images/generations
Authorization: Bearer {ARK_API_KEY}
Content-Type: application/json
```

Do not send a China token to a BytePlus host or a BytePlus token to the China host. Use an exact host allowlist, never log the key, and inject it at runtime from a secret manager.

**Documented region caveat:** BytePlus says an AP request normally prefers AP but may be served from EU, and an EU request may be served from AP when needed. Endpoint selection is therefore not a data-residency guarantee. Obtain a contractual answer if residency is a requirement.

## Select a model by contract, not name alone

| Capability | China 5.0 Pro | 5.0 Lite | 4.5 | 4.0 |
|---|---:|---:|---:|---:|
| Text generation and reference/edit input | Yes | Yes | Yes | Yes |
| Max reference images | 10 | 14 | 14 | 10 conservative; generic API says 14 |
| Grouped output (`sequential_image_generation`) | No | Yes | Yes | Yes |
| SSE streaming (`stream`) | No | Yes | Yes | Yes |
| `web_search` tool | No | Yes | No | No |
| Output format control | PNG/JPEG | PNG/JPEG | JPEG only | JPEG only |
| Resolution labels | 1K/2K | 2K/3K/4K | 2K/4K | 1K/2K/4K |
| Prompt optimization | `standard`; not `fast` | `standard`; not `fast` | `standard`; not `fast` | `standard` or `fast` |

The 5.0 Pro row applies to the China model documented above; BytePlus's current global image API does not document a global 5.0 Pro ID. Do not synthesize one.

**First-party 4.0 conflict:** the current generic image API describes 2–14 reference inputs, while the Seedream 4.0 model-specific card describes 2–10 for multi-image-to-single and multi-image-to-set workflows. Default 4.0 production validation to 10. Use 11–14 only after an authorized live canary confirms the exact endpoint contract; record the response and retrieval date.

Use 5.0 Lite when grouped output, SSE, or optional real-time web search is required. Use China 5.0 Pro when its documented higher-end single-image contract is required and grouped/streamed output is not. Keep 4.5 or 4.0 only for a measured compatibility, quality, or cost reason and maintain a migration test.

Seedream 5.0 Lite's first-party release page describes multimodal reasoning, world knowledge, and optional real-time search. These are **provider claims**; evaluate factuality and visual quality with representative prompts.

## Request contract

### Core fields

- `model` is required and may be a documented model ID or a configured endpoint ID.
- `prompt` is required. The guide recommends no more than about 300 Chinese characters or 600 English words; this is a recommendation, not a documented hard server limit.
- `image` is optional and accepts one URL/data URL or an array. A data URL must be `data:image/<lowercase-format>;base64,<payload>`.
- Input formats: JPEG, PNG, WebP, BMP, TIFF, GIF, HEIC, or HEIF. Each dimension must be greater than 14 px, aspect ratio must be within `[1/16, 16]`, file size at most 30 MB, and total image area at most 36 MP.
- `size` accepts a model-supported resolution label or explicit `WIDTHxHEIGHT` string. Validate against the selected model before sending.
- `response_format` is `url` or `b64_json`; default is `url`. Returned URLs expire after 24 hours.
- `watermark` defaults to `true` and adds a visible Chinese “AI generated” mark. `false` removes that visible mark; it does not waive disclosure, provenance, or legal obligations.
- `output_format` is `png` or `jpeg` only on current 5.0 models; it defaults to JPEG. Do not send it to 4.5/4.0 expecting conversion.

The current canonical 4.0–5.0 API pages do not document `seed` or `guidance_scale` for these models. BytePlus documents those controls only for legacy 3.0 models and explicitly marks guidance unsupported on the current family. Do not send them unless the exact endpoint contract you control explicitly documents them. Similar output is not deterministic output.

### Size constraints

| Model | Default | Explicit-pixel area | Aspect ratio |
|---|---:|---:|---:|
| China 5.0 Pro | `1024x1024` | 921,600 through 4,624,220 pixels | `[1/16, 16]` |
| 5.0 Lite | `2048x2048` | 3,686,400 through 16,777,216 pixels | `[1/16, 16]` |
| 4.5 | `2048x2048` | 3,686,400 through 16,777,216 pixels | `[1/16, 16]` |
| 4.0 | `2048x2048` | 921,600 through 16,777,216 pixels | `[1/16, 16]` |

Prefer a documented label plus an aspect/use description in the prompt, or choose a documented recommended size. Common documented examples include 5.0 Lite `2K` square `2048x2048`, landscape `2848x1600`, portrait `1600x2848`; 5.0 Lite `4K` square `4096x4096`; and Pro `1K` square `1024x1024` or `2K` square `2048x2048`. Do not assume the same label maps to the same pixel dimensions on every model.

### Natural-language edits and references

There is no separate mask/inpaint route in the current unified API. Supply one or more `image` references and describe the edit in `prompt`:

1. Identify references by ordinal: “In image 1… use the lighting from image 2.”
2. State the target operation: add, remove, replace, recolor, relight, restyle, or compose.
3. State invariants explicitly: “Keep pose, face proportions, camera, background, and all text unchanged.”
4. For a hard-to-identify local region, annotate the source image with an arrow, box, or doodle and refer to that mark. This technique is documented in the prompt guide.
5. For fusion, assign a single role to each reference rather than asking the model to infer roles.

Reference URLs must be fetchable by the service. Prefer short-lived, least-privilege presigned URLs. Data URLs avoid public hosting but still transmit the image to the provider and can make request bodies large.

### Grouped output

On 5.0 Lite, 4.5, or 4.0:

```json
{
  "sequential_image_generation": "auto",
  "sequential_image_generation_options": {"max_images": 4}
}
```

`max_images` is 1–15 and defaults to 15. The input-reference count plus generated-image count must not exceed 15. `auto` lets the model decide whether and how many images to create; it does not promise the requested maximum. Name the exact set in the prompt—such as “Create exactly four storyboard frames; frame 1…, frame 2…”—then validate the actual count. Do not send these fields to China 5.0 Pro.

### Optional web search

Only 5.0 Lite currently documents:

```json
{"tools": [{"type": "web_search"}]}
```

The model decides whether to use it; `usage.tool_usage.web_search` reports use. Search adds latency and external-content risk. Treat searched facts and visual details as untrusted, review attribution and rights, and do not promise that search will occur.

## Interpret responses defensively

For non-streaming requests, expect top-level `model`, `created`, `data`, `usage`, and possibly `error`. Each `data` member may be either a successful image (`url` or `b64_json`, `size`, and where supported `output_format`) or an item-level `error`. A 200 response can therefore still contain partial failure.

Validate:

1. Top-level status and error.
2. Every `data` item independently.
3. The actual successful count versus the requested deliverable.
4. Declared size/format versus decoded bytes.
5. `usage.generated_images`, output tokens, and tool usage for cost and observability.

The documentation says only successful generated images are billed. Do not infer zero cost from a client timeout: without a documented idempotency key, a timed-out request may have completed server-side.

When `stream: true`, parse server-sent events until the final completion event:

- `image_generation.partial_succeeded`: contains `image_index` (zero-based) plus `url` or `b64_json` and `size`.
- `image_generation.partial_failed`: contains `image_index` and an error.
- `image_generation.completed`: final usage/tools summary.
- top-level `error`: request failure.

The stream guide says a content-filter failure can be followed by later images, while an internal 500 stops subsequent generation. Do not treat the first partial event as completion.

## Production workflow

### 1. Establish a policy envelope

Before calling the API, record:

- deployment surface, account, endpoint region, exact model/endpoint ID, and launch date;
- allowed input classifications and whether personal data, faces, trademarks, or confidential material are permitted;
- maximum references, output count, dimensions, bytes, latency, retries, and spend per job;
- visible watermark/disclosure policy and a durable provenance policy;
- reviewer and approval criteria for public, commercial, or high-impact use.

### 2. Normalize and validate input

- Decode local inputs and inspect their real type; do not trust filenames or client MIME alone.
- Reject malformed, oversized, decompression-bomb, extreme-ratio, and unsupported inputs before upload.
- Strip unnecessary EXIF/location metadata unless it is intentionally preserved.
- Hash each source, store its license/consent record, and assign a stable reference number.
- Keep reference order stable from prompt through audit record.

### 3. Build a testable prompt

Use natural sentences rather than a keyword pile:

```text
[deliverable/use]. [subject and action]. [environment].
[camera/composition]. [lighting/color/style].
[exact text in double quotes]. [reference roles]. [edit invariants].
[numbered outputs if a set].
```

For typography, put required copy in double quotes, specify placement and hierarchy, then run OCR and human proofing. Generation is not a typesetting guarantee.

### 4. Submit with a job ledger

Create a client job ID and persist the request hash, redacted parameters, model, host, start time, attempt number, and state. The image API is synchronous or request-scoped SSE; the current docs do **not** document an async image job, polling API, webhook, or idempotency key. Do not import Seedance video task semantics.

### 5. Retry narrowly

Retry network failures, 429 throttles, and transient 500 errors with capped exponential backoff, jitter, and `Retry-After` when present. Bound total attempts and concurrency. Do not retry:

- authentication, account, balance, service-not-open, or model-access failures;
- invalid/missing parameters or bad images;
- content safety, copyright, or privacy rejections;
- an ambiguous timeout automatically if duplicate billing/output is unacceptable.

Ark documents account/model/endpoint-specific IPM, RPM, TPM, burst, quota, and overload errors. BytePlus's current Seedream tutorial lists 500 images/minute per current global model, but account and endpoint controls may be lower. Measure real headers/errors and configure admission control below the proven limit.

### 6. Acquire artifacts safely

For `url` responses, download immediately because links last 24 hours. The artifact URL is a separate untrusted fetch:

- require HTTPS and reject credentials/fragments and unexpected redirects;
- never attach the Ark `Authorization` header to the artifact request;
- enforce a streaming byte cap before buffering;
- allowlist image content types, verify magic bytes, decode dimensions, and rescan;
- write to a temporary file, fsync where required, then atomically promote;
- hash the final bytes and store dimensions, MIME, model, prompt hash, source hashes, review state, and provider usage.

For `b64_json`, use strict base64 decoding and apply the same decoded-byte, magic, dimension, and scanning checks.

### 7. Evaluate before release

Use a fixed regression set with text-to-image, single edit, multi-reference identity consistency, typography, prohibited content, extreme aspect ratio, group count, partial failure, throttling, timeout, and corrupt download cases. Score prompt adherence, edit locality, reference consistency, visual defects, OCR accuracy, safety, latency, and cost. Compare candidate and incumbent models blindly where possible.

## Example: strict non-streaming generation

This complete Python standard-library example is **not executed by this skill**. It uses BytePlus AP and 5.0 Lite, requests base64 to avoid an expiring asset URL, validates the API base, caps decoded size, checks PNG/JPEG magic, and writes durable metadata. Set `ARK_API_KEY`; optionally set `ARK_API_BASE` and `SEEDREAM_MODEL` to a compatible documented pair.

```python
import base64
import binascii
import hashlib
import json
import os
import pathlib
import tempfile
import time
import urllib.error
import urllib.request

ALLOWED = {
    "https://ark.cn-beijing.volces.com/api/v3": {
        "doubao-seedream-5-0-pro-260628", "doubao-seedream-5-0-260128",
        "doubao-seedream-5-0-lite-260128", "doubao-seedream-4-5-251128",
        "doubao-seedream-4-0-250828",
    },
    "https://ark.ap-southeast.bytepluses.com/api/v3": {
        "seedream-5-0-260128", "seedream-5-0-lite-260128",
        "seedream-4-5-251128", "seedream-4-0-250828",
    },
    "https://ark.eu-west.bytepluses.com/api/v3": {
        "seedream-5-0-260128", "seedream-5-0-lite-260128",
    },
}
MAX_IMAGE_BYTES = 25 * 1024 * 1024
MAX_JSON_BYTES = ((MAX_IMAGE_BYTES + 2) // 3) * 4 + 1024 * 1024


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=".seedream-")
    try:
        with os.fdopen(handle, "wb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise

api_base = os.getenv(
    "ARK_API_BASE", "https://ark.ap-southeast.bytepluses.com/api/v3"
).rstrip("/")
api_key = os.environ.get("ARK_API_KEY", "")
model = os.getenv("SEEDREAM_MODEL", "seedream-5-0-260128")
configured_endpoint = os.getenv("SEEDREAM_ALLOWED_ENDPOINT_ID")
configured_endpoint_base = os.getenv("SEEDREAM_ALLOWED_ENDPOINT_API_BASE")
configured_endpoint_model = os.getenv("SEEDREAM_ALLOWED_ENDPOINT_MODEL")
allowed_models = ALLOWED.get(api_base, set())
bound_endpoint = (
    model == configured_endpoint
    and api_base == configured_endpoint_base
    and configured_endpoint_model in allowed_models
)
if api_base not in ALLOWED or (model not in allowed_models and not bound_endpoint):
    raise SystemExit("Refusing an undocumented host/model namespace pairing")

payload = {
    "model": model,
    "prompt": (
        "Square editorial product photograph for a coffee brand. A matte black "
        "ceramic cup on pale limestone, soft window light from camera left, subtle "
        "steam, generous negative space, realistic materials. No logos or text."
    ),
    "size": "2K",
    "response_format": "b64_json",
    "output_format": "png",
    "watermark": True,
}
body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
request = urllib.request.Request(
    api_base + "/images/generations",
    data=body,
    method="POST",
    headers={
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
)
print({
    "model": payload["model"], "size": payload["size"],
    "request_sha256": hashlib.sha256(body).hexdigest(),
    "watermark": payload["watermark"],
})
if os.environ.get("SEND_SEEDREAM_REQUEST") != "1":
    raise SystemExit("Dry run only; set SEND_SEEDREAM_REQUEST=1 after approving the paid call")
if not api_key:
    raise SystemExit("Set ARK_API_KEY before the paid call")
try:
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = response.read(MAX_JSON_BYTES + 1)
except urllib.error.HTTPError as exc:
    # Do not print request headers or secrets.
    detail = exc.read(64 * 1024).decode("utf-8", "replace")
    raise SystemExit(f"Ark HTTP {exc.code}: {detail}") from exc

if len(raw) > MAX_JSON_BYTES:
    raise SystemExit("JSON response exceeded configured base64 envelope cap")
try:
    document = json.loads(raw)
except (UnicodeDecodeError, json.JSONDecodeError) as exc:
    raise SystemExit("Response was not valid bounded JSON") from exc
if document.get("error"):
    raise SystemExit(f"Ark error: {document['error']}")
successful = [item for item in document.get("data", []) if item.get("b64_json")]
failed = [item.get("error") for item in document.get("data", []) if item.get("error")]
if len(successful) != 1 or failed:
    raise SystemExit(f"Expected one image; successes={len(successful)} failures={failed}")

encoded = successful[0]["b64_json"]
if len(encoded) > ((MAX_IMAGE_BYTES + 2) // 3) * 4 + 8:
    raise SystemExit("Encoded image exceeds the configured cap")
try:
    image = base64.b64decode(encoded, validate=True)
except (binascii.Error, ValueError) as exc:
    raise SystemExit("Image was not strict base64") from exc
if len(image) > MAX_IMAGE_BYTES:
    raise SystemExit("Decoded image exceeds the configured cap")
if image.startswith(b"\x89PNG\r\n\x1a\n"):
    suffix = ".png"
elif image.startswith(b"\xff\xd8\xff"):
    suffix = ".jpg"
else:
    raise SystemExit("Unexpected image signature")

out = pathlib.Path("seedream-output" + suffix)
atomic_write(out, image)
metadata = {
    "created_unix": int(time.time()),
    "model": document.get("model", model),
    "request_sha256": hashlib.sha256(body).hexdigest(),
    "artifact_sha256": hashlib.sha256(image).hexdigest(),
    "declared_size": successful[0].get("size"),
    "usage": document.get("usage"),
    "watermark_requested": payload["watermark"],
}
atomic_write(
    out.with_suffix(out.suffix + ".json"),
    json.dumps(metadata, indent=2, ensure_ascii=False).encode("utf-8"),
)
print(out.resolve())
```

Production code should additionally decode pixels with a maintained image library, enforce width/height/area, scan content, use atomic writes, redact logs, and integrate the retry policy above.

## Example: multiple references, grouped output, and safe URL acquisition

This complete example is **not executed by this skill**. It requires two HTTPS reference URLs fetchable by BytePlus and an administratively maintained comma-separated `SEEDREAM_ASSET_HOSTS` allowlist derived from the provider's current artifact domains. The model may return fewer than three images because grouped mode is `auto`; the program records item-level failures and safely downloads successful URLs without forwarding the API token.

```python
import hashlib
import ipaddress
import json
import os
import pathlib
import socket
import tempfile
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"
API_KEY = os.environ.get("ARK_API_KEY", "")
REF_1 = os.environ.get("SEEDREAM_REFERENCE_1", "https://example.invalid/reference-1")
REF_2 = os.environ.get("SEEDREAM_REFERENCE_2", "https://example.invalid/reference-2")
MAX_DOWNLOAD = 25 * 1024 * 1024
MAX_API_JSON = 8 * 1024 * 1024
ASSET_HOSTS = {
    host.strip().lower()
    for host in os.environ.get("SEEDREAM_ASSET_HOSTS", "").split(",")
    if host.strip()
}
if not ASSET_HOSTS:
    raise SystemExit("Set SEEDREAM_ASSET_HOSTS to approved provider artifact hostnames")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate_artifact_url(url):
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https" or parsed.hostname not in ASSET_HOSTS
        or parsed.username or parsed.password or parsed.fragment
    ):
        raise ValueError("Artifact URL is outside the approved HTTPS allowlist")
    addresses = {
        info[4][0] for info in socket.getaddrinfo(parsed.hostname, parsed.port or 443)
    }
    if not addresses or any(not ipaddress.ip_address(value).is_global for value in addresses):
        raise ValueError("Artifact host did not resolve exclusively to public addresses")


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=".seedream-meta-")
    try:
        with os.fdopen(handle, "wb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise

for ref in (REF_1, REF_2):
    parsed = urllib.parse.urlsplit(ref)
    if parsed.scheme != "https" or parsed.username or parsed.password:
        raise SystemExit("References must be credential-free HTTPS URLs")

payload = {
    "model": "seedream-5-0-260128",
    "prompt": (
        "Create exactly three coordinated campaign images. Preserve the product "
        "shape and label from image 1. Use only the blue-and-amber palette and soft "
        "paper texture from image 2. Frame 1: square hero. Frame 2: vertical detail. "
        "Frame 3: wide environmental scene. Keep all label spelling unchanged."
    ),
    "image": [REF_1, REF_2],
    "size": "2K",
    "sequential_image_generation": "auto",
    "sequential_image_generation_options": {"max_images": 3},
    "response_format": "url",
    "output_format": "jpeg",
    "watermark": True,
}
request = urllib.request.Request(
    API_BASE + "/images/generations",
    data=json.dumps(payload).encode("utf-8"),
    method="POST",
    headers={
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
)
print({
    "model": payload["model"], "references": len(payload["image"]),
    "max_images": payload["sequential_image_generation_options"]["max_images"],
    "request_sha256": hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest(),
})
if os.environ.get("SEND_SEEDREAM_REQUEST") != "1":
    raise SystemExit("Dry run only; set SEND_SEEDREAM_REQUEST=1 after approving the paid call")
if not API_KEY or "example.invalid" in {urllib.parse.urlsplit(REF_1).hostname, urllib.parse.urlsplit(REF_2).hostname}:
    raise SystemExit("Set ARK_API_KEY and both SEEDREAM_REFERENCE environment variables")
try:
    with urllib.request.urlopen(request, timeout=240) as response:
        response_bytes = response.read(MAX_API_JSON + 1)
except urllib.error.HTTPError as exc:
    raise SystemExit(f"Ark HTTP {exc.code}") from exc
if len(response_bytes) > MAX_API_JSON:
    raise SystemExit("Grouped API response exceeded configured JSON cap")
try:
    document = json.loads(response_bytes)
except (UnicodeDecodeError, json.JSONDecodeError) as exc:
    raise SystemExit("Grouped API response was not valid bounded JSON") from exc

def safe_download(url: str, destination: pathlib.Path) -> dict:
    opener = urllib.request.build_opener(NoRedirect())
    current = url
    response = None
    for _ in range(6):
        validate_artifact_url(current)
        # Deliberately no Authorization header here or on any redirect hop.
        req = urllib.request.Request(current, headers={"Accept": "image/png,image/jpeg"})
        try:
            response = opener.open(req, timeout=90)
            break
        except urllib.error.HTTPError as exc:
            if exc.code not in {301, 302, 303, 307, 308}:
                raise
            location = exc.headers.get("Location")
            exc.close()
            if not location:
                raise ValueError("Artifact redirect omitted Location")
            current = urllib.parse.urljoin(current, location)
    else:
        raise ValueError("Too many artifact redirects")

    hasher = hashlib.sha256()
    total = 0
    prefix = b""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with response:
        content_type = response.headers.get_content_type()
        if content_type not in {"image/png", "image/jpeg"}:
            raise ValueError(f"Unexpected Content-Type: {content_type}")
        declared = response.headers.get("Content-Length")
        if declared and int(declared) > MAX_DOWNLOAD:
            raise ValueError("Artifact exceeds byte cap")
        fd, temporary = tempfile.mkstemp(dir=destination.parent, prefix=".seedream-")
        try:
            with os.fdopen(fd, "wb") as output:
                while True:
                    chunk = response.read(64 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_DOWNLOAD:
                        raise ValueError("Artifact exceeded byte cap while streaming")
                    if len(prefix) < 12:
                        prefix += chunk[: 12 - len(prefix)]
                    hasher.update(chunk)
                    output.write(chunk)
                output.flush()
                os.fsync(output.fileno())
            is_png = prefix.startswith(b"\x89PNG\r\n\x1a\n")
            is_jpeg = prefix.startswith(b"\xff\xd8\xff")
            if not (is_png or is_jpeg):
                raise ValueError("Unexpected artifact signature")
            os.replace(temporary, destination)
        except Exception:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise
    return {"bytes": total, "sha256": hasher.hexdigest(), "content_type": content_type}

if document.get("error"):
    raise SystemExit(f"Ark error: {document['error']}")
manifest = {"model": document.get("model"), "usage": document.get("usage"), "items": []}
success_index = 0
for index, item in enumerate(document.get("data", [])):
    if item.get("error"):
        manifest["items"].append({"index": index, "error": item["error"]})
        continue
    if not item.get("url"):
        manifest["items"].append({"index": index, "error": "missing url"})
        continue
    success_index += 1
    path = pathlib.Path("seedream-set") / f"image-{success_index:02d}.jpg"
    audit = safe_download(item["url"], path)
    manifest["items"].append({"index": index, "path": str(path), **audit})

atomic_write(
    pathlib.Path("seedream-set/manifest.json"),
    json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8"),
)
if success_index == 0:
    raise SystemExit("No successful images")
print(f"Saved {success_index} image(s); review count, labels, and visual consistency")
```

## Example: request-scoped SSE

This curl example is **not executed by this skill**. It demonstrates the wire shape, not production parsing. Use a real SSE parser in production, preserve event order, handle partial failures, and wait for `image_generation.completed`.

```bash
: "${ARK_API_KEY:?set ARK_API_KEY}"
: "${SEND_SEEDREAM_REQUEST:?set SEND_SEEDREAM_REQUEST=1 after approving the paid call}"
[ "${SEND_SEEDREAM_REQUEST}" = "1" ] || { echo 'Refusing paid call without SEND_SEEDREAM_REQUEST=1' >&2; exit 2; }
curl --fail-with-body --no-buffer \
  --connect-timeout 10 --max-time 300 \
  'https://ark.ap-southeast.bytepluses.com/api/v3/images/generations' \
  -H "Authorization: Bearer ${ARK_API_KEY}" \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  --data-binary @- <<'JSON'
{
  "model": "seedream-5-0-260128",
  "prompt": "Create a three-frame horizontal storyboard of a paper airplane crossing a quiet library: establishing shot, close tracking shot, final landing. Consistent airplane and lighting in every frame.",
  "size": "2K",
  "sequential_image_generation": "auto",
  "sequential_image_generation_options": {"max_images": 3},
  "response_format": "url",
  "stream": true,
  "watermark": true
}
JSON
```

## Error map and observability

| Class | Typical documented errors | Action |
|---|---|---|
| 400 request | invalid/missing parameter, invalid image/base64/URL, input/output safety/copyright/privacy | Do not blind-retry; correct input or stop |
| 401/403 | authentication, access denied, account overdue, service not open, terms/access | Rotate/fix credentials or account state; do not retry as transient |
| 404 | model/endpoint not found, model access disabled | Check surface, region, model ID, endpoint, lifecycle, and entitlement |
| 429 | model/account IPM, RPM, TPM, endpoint limit, burst, quota, overload | Queue, reduce concurrency, honor retry timing, jittered backoff |
| 500 | internal service error | Capped retry if duplicate risk is acceptable; otherwise reconcile manually |

Emit metrics for attempts, status/error code, throttle class, queue wait, provider latency, download latency, successful/failed image count, bytes, resolution, model, region endpoint, web-search use, estimated and invoiced cost, moderation outcome, and reviewer decision. Never record raw secrets; minimize raw prompts and source URLs in telemetry.

## Cost and lifecycle controls

Pricing is volatile. The China pricing page displayed on 2026-07-09: 4.0 at ¥0.20/successful image, 4.5 at ¥0.25, 5.0 Lite at ¥0.22, and 5.0 Pro at ¥0.30 up to 2.36 MP or ¥0.60 above 2.36 MP. BytePlus first-party pages reviewed showed 4.0 at US$0.03/image and 4.5 at US$0.04/image; a current public 5.0 Lite global price was not established. Recheck the account console and official price page because region, contract, tax, packs, and promotions can differ.

Estimate the upper bound before submission using maximum successful group count and applicable resolution tier. Reconcile the provider `usage` and invoice rather than relying solely on estimates. Failed moderation outputs are documented as unbilled, while successful members of a partially failed group are billed.

Pin dated model IDs, subscribe to model retirement notices, and maintain a golden migration suite. The current catalog and API page are the authority for availability; do not infer lifecycle from a product name. Alias behavior can change. Treat any legacy 3.0 `seed` workflow as a migration project rather than carrying legacy parameters into 4.0/5.0.

## Privacy, rights, and safety gate

BytePlus's current Model Service terms say Input and Output are not used to train base models without separate consent, and BytePlus does not claim ownership of Output. They also say outputs may not be unique, rights held by BytePlus/affiliates/third parties remain theirs, and the customer remains responsible for inputs, outputs, applicable law, and rights clearance. This is not a guarantee that an output is copyrightable, exclusive, non-infringing, accurate, or safe.

The BytePlus data-processing page states processing may occur in Malaysia, Indonesia, and/or the EU/EEA and says content that triggers a safety filter may be retained for 180 days in Malaysia. That retention is distinct from the 24-hour generated-image URL. Confirm the current DPA, subprocessor locations, encryption options, deletion, and support commitments for the actual contract.

Before generation and publication:

- obtain licenses/consent for source images, trademarks, copyrighted characters, private data, faces, likenesses, and biometric-sensitive use;
- prohibit sexual exploitation, minors abuse, non-consensual intimate imagery, deceptive impersonation, fraud, illegal surveillance/identification, hate/extremism, self-harm encouragement, and other disallowed content;
- do not bypass safety systems or remove/obscure required credentials, watermarks, metadata, or disclosures;
- label AI-generated material where law, platform policy, or context requires it, even if `watermark: false` is technically used;
- require human review for factual claims, typography, likeness, medical/legal/financial implications, elections/public affairs, and consequential use;
- preserve a provenance record; no universal C2PA guarantee was found in the reviewed image API contract.

Do not use the model or its output to train or improve another model where the applicable Model Service terms prohibit that use. Ask counsel for jurisdiction- and contract-specific advice.

## First-party sources

Checked 2026-07-09:

- Volcengine Ark image generation API: https://www.volcengine.com/docs/82379/1541523
- Volcengine Ark current model catalog: https://www.volcengine.com/docs/82379/1330310
- Volcengine Ark Seedream 4.0–5.0 prompt guide: https://www.volcengine.com/docs/82379/1829186
- Volcengine Ark streaming response contract: https://www.volcengine.com/docs/82379/1824137
- Volcengine Ark error codes: https://docs.volcengine.com/docs/82379/1299023?lang=zh
- Volcengine Ark pricing: https://docs.volcengine.com/docs/82379/1544106?lang=zh
- Volcengine Ark model retirement notices: https://docs.volcengine.com/docs/82379/1350667?lang=zh
- BytePlus ModelArk image generation API: https://docs.byteplus.com/en/docs/ModelArk/1541523
- BytePlus Seedream image tutorial/capability matrix: https://docs.byteplus.com/en/docs/ModelArk/1824121
- BytePlus ModelArk regional availability: https://docs.byteplus.com/api/docs/modelark/2191806
- BytePlus international availability restrictions: https://docs.byteplus.com/en/docs/ModelArk/availability?TimeBefore=1757476852
- BytePlus ModelArk data processing: https://docs.byteplus.com/api/docs/ModelArk/BytePlus_ModelArk_Data_Processing
- BytePlus service-specific terms (including Model Services): https://docs.byteplus.com/en/docs/legal/docs-service-specific-terms
- BytePlus GenAI acceptable use policy: https://docs.byteplus.com/en/docs/legal/acceptable_use_policy_byteplus_genai
- ByteDance Seed Seedream 5.0 Lite product page: https://seed.bytedance.com/en/seedream5_0_lite
- ByteDance Seed Seedream 5.0 Lite release article: https://seed.bytedance.com/en/blog/deeper-thinking-more-accurate-generation-introducing-seedream-5-0-lite
- ByteDance Seed Seedream 4.0 product page: https://seed.bytedance.com/en/seedream4_0

## Known gaps

The reviewed first-party image API pages do not establish an idempotency key, async image job/polling/webhook contract, deterministic current-family seed, universal residency guarantee, universal C2PA output, or a public current BytePlus price for 5.0 Lite. Do not claim these capabilities. Recheck documentation or obtain a written provider answer when one is required.
