---
name: runway-image
description: Generate, edit, and iterate still images with Runway's official API, especially native Gen-4 Image and Gen-4 Image Turbo reference workflows. Use when implementing Runway text-to-image, reference-driven image generation or natural-language image edits, task polling, secure artifact handling, production retries, cost controls, or Runway image API QA. Do not use for Runway video generation or third-party gateway APIs.
---

# Runway Image

Use the official Runway API to create still images. Prefer Runway-native `gen4_image` and `gen4_image_turbo`; keep partner image models explicitly labeled. This skill does not cover Runway video endpoints, the web-app UI, unofficial wrappers, or third-party gateways.

## First response

Before writing code or starting a billable task, establish:

- Desired output: subject, environment, composition, style, aspect/resolution, count, and acceptance criteria.
- Mode: text-only generation, reference-guided generation, or a natural-language edit using the source image as a reference.
- References: paths/URLs, rights and consent, each image's role, and whether identity must remain stable.
- Delivery: destination, naming, metadata/manifest, and maximum budget.
- Runtime: direct REST, Python SDK, or Node SDK. Prefer an official SDK for normal application code.

If required creative details are missing, propose a concrete default and ask only the questions that materially change cost, rights, or output. Never make a paid call without explicit approval.

## Current contract snapshot

Verified against first-party documentation and the official Python SDK on **2026-07-09**. Recheck the API reference, model catalog, pricing, limits, changelog, terms, and usage policy before production deployment; these are volatile.

### Routes and authentication

| Purpose | Method and route | Result |
|---|---|---|
| Create an image task | `POST https://api.dev.runwayml.com/v1/text_to_image` | `{ "id": "..." }` |
| Read task | `GET https://api.dev.runwayml.com/v1/tasks/{id}` | Discriminated task object |
| Cancel or delete task | `DELETE https://api.dev.runwayml.com/v1/tasks/{id}` | Cancels active task or deletes terminal task |
| Start ephemeral upload | `POST https://api.dev.runwayml.com/v1/uploads` | Multipart upload instructions plus `runwayUri` |

Send these headers on API calls:

```http
Authorization: Bearer $RUNWAYML_API_SECRET
Content-Type: application/json
X-Runway-Version: 2024-11-06
```

`/v1` is a URL namespace, not the API version. Runway versions behavior with the date-valued header and says an old version is supported for four months after a replacement version is introduced. Pin and test the header; do not omit it.

Keep the organization-scoped key server-side in a secret manager. Runway reveals it once. Removing an organization member does not revoke their key, so disable/rotate keys separately. Never send the bearer token to reference hosts or output CDN URLs.

### Runway-native model selection

| Model | Inputs | Use it for | Cost snapshot |
|---|---|---|---|
| `gen4_image` | Text; optionally 1–3 references | Text-only work, best-quality native generation, edits, style/identity/composition control | 5 credits per 720p image; 8 per 1080p image |
| `gen4_image_turbo` | Text **and 1–3 required references** | Faster, inexpensive reference-driven iteration | 2 credits per image at any supported resolution |

One credit is $0.01 before applicable tax. Moderated generations cost the same as successful generations. Do not infer a specific ratio's 720p/1080p billing tier from dimensions alone; confirm in the current pricing page or developer portal.

Provider-reported launch claims for Turbo (speed, relative quality, or benchmark scores) are marketing claims, not guarantees. Benchmark on representative prompts and references.

### Exact native request schema

Both native models accept:

- `model`: exactly `gen4_image` or `gen4_image_turbo`.
- `promptText`: required, non-empty, at most 1,000 UTF-16 code units.
- `ratio`: required and exactly one of:

```text
1024:1024  1080:1080  1168:880   1360:768
1440:1080  1080:1440  1808:768   1920:1080
1080:1920  2112:912   1280:720   720:1280
720:720    960:720    720:960    1680:720
```

- `referenceImages`: objects with required `uri` and optional `tag`. `gen4_image` accepts 0–3; Turbo requires 1–3.
- `seed`: optional integer `0..4294967295`. An identical request and seed should be similar, not necessarily bit-identical.
- `contentModeration.publicFigureThreshold`: optional `auto` or `low`. `low` is less strict for recognizable public figures; it is not a safety bypass, consent grant, or rights clearance.

The current API schema constrains reference tags to 3–16 lowercase characters matching `^[a-z][a-z0-9_]+$`; mention one in `promptText` as `@product_ref`. Normalize tags to this conservative form because an official getting-started example still shows uppercase tags, a documentation inconsistency as of the verification date.

There is no documented separate Gen-4 still-image mask/inpaint/edit route. For an edit, submit the source as a reference and describe the changed result while restating invariants. Do not invent masks, denoise strength, negative prompts, ControlNet, weights, or image-strength fields.

### Partner models exposed by Runway

The public model catalog currently lists `gemini_image3_pro`, `gpt_image_2`, and `gemini_2.5_flash` on the same route. These are partner models, not Runway-native Gen-4. Their schemas and provider behavior differ:

| Model | Notable contract | Current price |
|---|---|---|
| `gemini_image3_pro` | Up to 5,500 UTF-16 code units; up to 14 references (at most 5 `human`, 9 `object`); `outputCount` 1 or 4; 1K/2K/4K ratios | 20 credits at 1K/2K; 40 at 4K |
| `gpt_image_2` | Up to 32,000 characters; up to 16 references; `outputCount` 1–10; `quality` low/medium/high/auto; opaque/auto background, no transparent | 1–41 credits per output by quality and resolution; `auto` resolution bills as 4K |
| `gemini_2.5_flash` | Up to 5,500 UTF-16 code units in the current API schema; up to 3 references; ten documented ratios | 5 credits per image |

The official Python SDK schema exposed `gemini_image3.1_flash` on 2026-07-09 while the public model catalog and pricing page omitted it. The current API schema and model catalog list `seedream5_pro`, while the pricing page and current Python SDK omit it. Treat either as unavailable for a cost-governed production call until the request schema, catalog, pricing, SDK/access for the account agree or Runway support confirms the missing contract. Never copy one model's fields into another.

## Input media

Reference `uri` accepts:

1. HTTPS URL.
2. `data:image/...;base64,...` data URI.
3. `runway://...` URI returned by an ephemeral upload.

Supported still formats are JPEG (`image/jpeg` or `image/jpg`), PNG, and WebP; GIF is unsupported. Current limits:

| Transport | Image limit | Operational notes |
|---|---:|---|
| HTTPS URL | 16 MB | URL ≤2,048 chars; host must be a domain, not IP; no redirects; `HEAD` and `Content-Length` required; exact media `Content-Type`; 200 response |
| Data URI | 5 MB encoded | Binary should be about 3.3 MB or less after accounting for base64 expansion |
| Ephemeral upload | 200 MB | Minimum 512 bytes; needs purchased API credits; rate-limited; `runway://` URI valid 24h |

Runway's input guide recommends references roughly from 640px through 4K; it does not publish a Gen-4 reference-image 8,000-pixel dimension rule. Prefer sharp, minimally compressed sources with one clear subject, even neutral lighting, and no watermark or overlaid text. Runway may resize inputs. Do not transplant the separate upscaler endpoint's 8,000-pixel limit into this route.

For a customer-hosted reference URL, implement a dedicated signed asset endpoint that answers `HEAD` and `GET` without redirects, returns exact `Content-Type` and `Content-Length`, and permits Runway's `User-Agent` prefix `RunwayML API/`. Do not expose private-network assets.

## Prompt and reference design

### Text-only generation

Describe what should appear, positively and visually:

```text
[medium/style] of [subject and defining details] in [scene].
[composition and angle]. [lighting]. [palette]. [focus/lens/material/mood].
```

Example:

```text
Editorial product photograph of a matte cobalt travel mug on pale limestone.
Three-quarter view, centered with generous negative space on the right. Soft north-window
light, crisp rim highlight, restrained blue and warm gray palette, 85mm lens, shallow depth.
```

Use full sentences and concrete visual language. Gen-4 does not support a separate negative-prompt field; rewrite negatives positively (`bald person`, not `person with no hair`). Avoid conversational filler such as “please generate.” State exact text to render in quotes, then inspect spelling manually.

### References and edits

Assign each reference one role and a stable lower-snake tag:

```json
{
  "referenceImages": [
    {"uri": "https://assets.example.com/mug.jpg", "tag": "product_ref"},
    {"uri": "https://assets.example.com/light.jpg", "tag": "style_ref"}
  ],
  "promptText": "@product_ref unchanged in shape, logo placement, and cobalt color, photographed with the soft window lighting and pale stone setting of @style_ref. Three-quarter product view with clear negative space on the right."
}
```

An untagged reference can influence overall style. Tagged references provide clearer roles. For character consistency, use a clean neutral view with even lighting and unobscured features. A sketch or annotated composition can be another reference, but the API receives it as an ordinary image; there is no separate sketch-control field.

For edits, describe the target image, the change, and invariants:

```text
@source_ref in the same camera position and crop. Replace the background with a warm,
minimal studio wall and add soft late-afternoon side light. Preserve the person's identity,
facial expression, hairstyle, clothing silhouette, and hand position.
```

Do one complex change at a time. Feed the approved result back as the next reference. This is a heuristic workflow, not a guaranteed identity lock.

### Iteration and QA

Use a branch ledger containing prompt, model, ratio, seed, reference hashes/URIs, task ID, cost estimate, output hashes, and reviewer decision. Change one factor per branch:

1. Lock composition and subject.
2. Tune lighting and palette.
3. Tune style/material/lens.
4. Correct one local semantic issue through a new reference-based edit.
5. Freeze approved source hashes and render the delivery ratio.

Review every output at full size for prompt adherence, anatomy/geometry, identity/product fidelity, text/logo accuracy, edge artifacts, unintended people/marks, privacy/rights concerns, and delivery dimensions. Similar seeds are an exploration aid, not reproducibility proof.

## Async lifecycle

Creation returns only a task ID. Poll `GET /v1/tasks/{id}`; do not expect meaningful updates more often than once every five seconds.

| Status | Action |
|---|---|
| `PENDING` | Wait at least 5s, then poll |
| `THROTTLED` | Valid queued task; wait and poll, do not resubmit |
| `RUNNING` | Record `progress`; wait and poll |
| `SUCCEEDED` | Download every output immediately and persist manifest |
| `FAILED` | Inspect `failureCode` and human-readable `failure`; apply failure policy |
| `CANCELLED` | Stop; do not treat as success |

Use jittered polling and exponential backoff for transient non-200 responses. Official SDK wait helpers default to a ten-minute timeout; timeout/abort stops local polling but **does not cancel the remote task**. Call `DELETE /v1/tasks/{id}` only when cancellation is actually intended. Deleting a terminal task makes its task data and outputs unavailable through the API.

Output URLs expire within 24–48 hours. Re-fetching a retained successful task can issue fresh URLs, but that is not durable storage. Download promptly, store in your own controlled bucket, and never expose provider-signed URLs directly to end users.

## Complete direct REST example

This Python example creates one text-only `gen4_image` task, records its ID before polling, handles every task status, and downloads outputs without forwarding API credentials. Install Pillow first. It defaults to a redacted dry run and becomes billable only after `SEND_RUNWAY_REQUEST=1`; review the model, ratio, prompt, allowlist, and budget first.

```python
#!/usr/bin/env python3
import hashlib, ipaddress, json, os, random, socket, tempfile, time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from PIL import Image, UnidentifiedImageError

BASE = "https://api.dev.runwayml.com"
VERSION = "2024-11-06"
KEY = os.environ.get("RUNWAYML_API_SECRET", "")
OUT = Path(os.environ.get("RUNWAY_OUTPUT_DIR", "runway-output")).resolve()
MAX_BYTES = 25 * 1024 * 1024
MAX_API_BYTES = 4 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000
Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS
ALLOWED_HOSTS = frozenset(
    x.strip().lower().rstrip(".")
    for x in os.environ.get("RUNWAY_OUTPUT_HOSTS", "").split(",") if x.strip()
)

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = build_opener(NoRedirect)

def api(method, path, body=None, timeout=60):
    data = None if body is None else json.dumps(body).encode()
    req = Request(BASE + path, data=data, method=method, headers={
        "Authorization": f"Bearer {KEY}",
        "X-Runway-Version": VERSION,
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    with opener.open(req, timeout=timeout) as response:
        raw = response.read(MAX_API_BYTES + 1)
    if len(raw) > MAX_API_BYTES:
        raise ValueError("Runway API response exceeded configured JSON cap")
    return json.loads(raw)

def atomic_json(path, value):
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            fd = None
            json.dump(value, f, indent=2, sort_keys=True)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if fd is not None: os.close(fd)
        if os.path.exists(tmp): os.unlink(tmp)

def task_snapshot(task):
    # Signed output URLs are bearer credentials. Never log or persist them.
    return {
        key: task[key] for key in (
            "id", "status", "createdAt", "progress", "failureCode", "failure"
        ) if key in task
    } | {"outputCount": len(task.get("output") or [])}

def wait_for_task(task_id, timeout_s=900):
    deadline, delay = time.monotonic() + timeout_s, 5.0
    while time.monotonic() < deadline:
        try:
            task = api("GET", f"/v1/tasks/{task_id}")
            delay = 5.0
        except HTTPError as e:
            if e.code not in (429, 502, 503, 504): raise
            delay = min(30.0, max(5.0, delay * 2))
            time.sleep(delay + random.uniform(0, delay * 0.5)); continue
        except URLError:
            delay = min(30.0, max(5.0, delay * 2))
            time.sleep(delay + random.uniform(0, delay * 0.5)); continue
        atomic_json(OUT / "task.json", task_snapshot(task))
        status = task["status"]
        if status == "SUCCEEDED": return task
        if status == "FAILED":
            raise RuntimeError(f"task failed: {task.get('failureCode')}: {task.get('failure')}")
        if status == "CANCELLED": raise RuntimeError("task cancelled")
        if status not in ("PENDING", "THROTTLED", "RUNNING"):
            raise RuntimeError(f"unknown task status: {status}")
        time.sleep(5.0 + random.uniform(0, 1.0))
    raise TimeoutError("local wait expired; remote task was NOT cancelled")

def checked_output_url(url):
    p = urlparse(url)
    host = (p.hostname or "").lower()
    if (p.scheme != "https" or p.username or p.password or p.fragment or not host
            or p.port not in (None, 443)):
        raise ValueError("unsafe output URL")
    if host.rstrip(".") not in ALLOWED_HOSTS:
        raise ValueError(f"output host not allowlisted: {host}")
    for info in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global: raise ValueError(f"non-public output address: {ip}")
    return url

def download(url, index):
    # Deliberately no Authorization header and no redirects.
    req = Request(checked_output_url(url), headers={"Accept": "image/*"})
    with opener.open(req, timeout=60) as response:
        ctype = response.headers.get_content_type()
        ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(ctype)
        if not ext: raise ValueError(f"unexpected media type: {ctype}")
        declared = int(response.headers.get("Content-Length", "0") or 0)
        if declared and declared > MAX_BYTES: raise ValueError("output too large")
        fd, tmp = tempfile.mkstemp(dir=OUT, suffix=".part")
        digest, total = hashlib.sha256(), 0
        try:
            with os.fdopen(fd, "wb") as f:
                fd = None
                while chunk := response.read(1024 * 1024):
                    total += len(chunk)
                    if total > MAX_BYTES: raise ValueError("output exceeded byte cap")
                    digest.update(chunk); f.write(chunk)
                f.flush(); os.fsync(f.fileno())
            head = Path(tmp).read_bytes()[:12]
            valid = (head.startswith(b"\xff\xd8\xff") if ext == ".jpg" else
                     head.startswith(b"\x89PNG\r\n\x1a\n") if ext == ".png" else
                     head[:4] == b"RIFF" and head[8:12] == b"WEBP")
            if not valid: raise ValueError("media signature mismatch")
            try:
                with Image.open(tmp) as probe:
                    dimensions = probe.size
                    if dimensions[0] * dimensions[1] > MAX_IMAGE_PIXELS:
                        raise ValueError(f"output exceeds pixel cap: {dimensions}")
                    decoded_format = probe.format
                    probe.verify()
                with Image.open(tmp) as probe:
                    probe.load()
            except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
                raise ValueError("output failed bounded pixel decode") from exc
            expected_format = {".jpg": "JPEG", ".png": "PNG", ".webp": "WEBP"}[ext]
            if decoded_format != expected_format:
                raise ValueError("decoder and MIME/signature disagree")
            final = OUT / f"image-{index:02d}{ext}"
            os.replace(tmp, final)
            tmp = None
            return {"path": str(final), "bytes": total, "sha256": digest.hexdigest(),
                    "mediaType": ctype, "dimensions": list(dimensions)}
        finally:
            if fd is not None: os.close(fd)
            if tmp is not None and os.path.exists(tmp): os.unlink(tmp)

request_body = {
    "model": "gen4_image",
    "ratio": "1920:1080",
    "promptText": "Editorial product photograph of a matte cobalt travel mug on pale limestone. Three-quarter view, soft north-window light, crisp rim highlight, restrained blue and warm gray palette, 85mm lens.",
}

request_bytes = json.dumps(request_body, separators=(",", ":")).encode()
print({"model": request_body["model"], "ratio": request_body["ratio"],
       "request_sha256": hashlib.sha256(request_bytes).hexdigest(),
       "estimated_credits_snapshot_2026_07_10": 8})
if os.environ.get("SEND_RUNWAY_REQUEST") != "1":
    raise SystemExit("Dry run only; set SEND_RUNWAY_REQUEST=1 after approving the paid call")
if not KEY or not ALLOWED_HOSTS:
    raise SystemExit("Set RUNWAYML_API_SECRET and exact RUNWAY_OUTPUT_HOSTS")
OUT.mkdir(parents=True, exist_ok=True)

# Do not blindly retry this POST after a timeout: its outcome may be ambiguous and a retry may duplicate cost.
try:
    created = api("POST", "/v1/text_to_image", request_body)
except HTTPError as e:
    raise SystemExit(f"create rejected with definite HTTP {e.code}; fix or classify before retry")
except (URLError, TimeoutError) as e:
    raise SystemExit(f"create outcome unknown; reconcile before retrying: {e}")
task_id = created["id"]
atomic_json(OUT / "job.json", {"taskId": task_id, "request": request_body, "createdAt": time.time()})
task = wait_for_task(task_id)
artifacts = [download(url, i) for i, url in enumerate(task["output"], 1)]
atomic_json(OUT / "manifest.json", {"taskId": task_id, "artifacts": artifacts})
print(json.dumps({"taskId": task_id, "artifacts": artifacts}, indent=2))
```

Set `RUNWAY_OUTPUT_HOSTS` to exact output hostnames observed and security-reviewed for your account. Do not allow a shared tenancy suffix such as `.cloudfront.net`. The standard-library example checks public DNS before connecting, but DNS can change between resolution and connection; for hostile multi-tenant inputs, route downloads through an egress proxy that pins the validated address while preserving TLS SNI/certificate validation.

## Complete official-SDK reference example

Install `runwayml`, set the API key and two approved HTTPS/`runway://` references, then use this Turbo example. It defaults to a redacted dry run and is billable only after `SEND_RUNWAY_REQUEST=1`. `max_retries=0` is deliberate for task creation because Runway does not document a public create-idempotency contract.

```python
import os
import hashlib
import json
import random
import time
from pathlib import Path
from runwayml import RunwayML

product_uri = os.environ.get("RUNWAY_PRODUCT_URI", "<required-product-uri>")
style_uri = os.environ.get("RUNWAY_STYLE_URI", "<required-style-uri>")
request_summary = {
    "model": "gen4_image_turbo", "ratio": "1920:1080",
    "reference_hashes": [hashlib.sha256(value.encode()).hexdigest()
                         for value in (product_uri, style_uri)],
    "estimated_credits_snapshot_2026_07_10": 2,
}
print(json.dumps(request_summary, indent=2))
if os.environ.get("SEND_RUNWAY_REQUEST") != "1":
    raise SystemExit("Dry run only; set SEND_RUNWAY_REQUEST=1 after approving the paid call")
if not os.environ.get("RUNWAYML_API_SECRET") or product_uri.startswith("<required-") or style_uri.startswith("<required-"):
    raise SystemExit("Set RUNWAYML_API_SECRET and both approved reference URIs")

create_client = RunwayML(api_key=os.environ["RUNWAYML_API_SECRET"], max_retries=0)
created = create_client.text_to_image.create(
    model="gen4_image_turbo",
    ratio="1920:1080",
    prompt_text=(
        "@product_ref unchanged in shape, cobalt color, and logo placement, photographed "
        "with the soft window light and pale stone setting of @style_ref. Three-quarter "
        "product view with clear negative space on the right."
    ),
    reference_images=[
        {"uri": product_uri, "tag": "product_ref"},
        {"uri": style_uri, "tag": "style_ref"},
    ],
)
Path("runway-task-id.txt").write_text(created.id + "\n", encoding="utf-8")
print("persisted task id:", created.id)

# Use a separate retrying client only for idempotent reads. Poll manually because
# the synchronous SDK wait helper in the reviewed version did not terminate on CANCELLED.
read_client = RunwayML(api_key=os.environ["RUNWAYML_API_SECRET"], max_retries=2)
deadline = time.monotonic() + 600
while time.monotonic() < deadline:
    task = read_client.tasks.retrieve(created.id)
    status = task.status
    print(created.id, status)
    if status == "SUCCEEDED":
        print("outputs ready; pass in-memory URLs to the secure downloader above")
        break
    if status == "FAILED":
        raise RuntimeError(f"generation failed: {getattr(task, 'failure_code', None)}")
    if status == "CANCELLED":
        raise RuntimeError("generation cancelled")
    if status not in ("PENDING", "THROTTLED", "RUNNING"):
        raise RuntimeError(f"unknown task status: {status}")
    time.sleep(5 + random.uniform(0, 1))
else:
    raise TimeoutError("local polling timed out; the provider task was NOT cancelled")
```

Before production use, persist `created.id` durably before waiting and use the secure downloader/manifest pattern above rather than printing or returning signed URLs.

## Errors, retries, and duplicate-cost control

### HTTP layer

| Response | Retry? | Action |
|---|---|---|
| 400, 401, 404, 405 | No | Fix request, credentials, ID, or method |
| 429 | Yes, bounded | Honor quota/budget; exponential backoff with up to 50% jitter |
| 502, 503, 504 | Yes, bounded | Back off with jitter |

Official SDKs retry connection errors, 408, 409, 429, and 5xx twice by default. That is useful for reads, but a create request that reaches the server and loses its response can be duplicated by a retry. No endpoint-specific idempotency key or reconciliation API was found in first-party public documentation as of 2026-07-09. Therefore:

- Prefer `max_retries=0` for creation when duplicate billing matters.
- Persist the task ID immediately after a successful response.
- Use an application job key and ledger to prevent local duplicate submissions.
- Retry `GET` safely; do not resubmit a `THROTTLED` task.
- If the create outcome is ambiguous, stop and reconcile credits/support rather than guessing.

### Task failure layer

| Failure family | Policy |
|---|---|
| `SAFETY.INPUT.*`, `INPUT_PREPROCESSING.SAFETY.TEXT` | Do not retry unchanged; revise/clear input. Input safety failures are not refunded. |
| `SAFETY.OUTPUT.*` | Do not loop; review prompt/references and policy. Moderated generations are billed. |
| `ASSET.INVALID` | Fix URL, MIME, dimensions, size, or encoding. |
| `INPUT_PREPROCESSING.INTERNAL` | Retry later with bounded backoff. |
| `THIRD_PARTY.UNAVAILABLE` | Wait before retry; applies to partner-model dependencies. |
| `INTERNAL.BAD_OUTPUT.*` | Remove watermarks/overlaid text, avoid asking the model to write a prompt, simplify explicit text requests, then try a changed request. |
| `INTERNAL` or missing code | Bounded delayed retry; preserve evidence and task ID. |

Never show raw `failure` text directly to end users without context; it is a diagnostic string and can change.

## Limits and scheduling

Limits are per organization and tier. All image-generation models share the image concurrency bucket. Excess accepted tasks become `THROTTLED` and are queued approximately in creation order. Daily generation limits use a rolling 24-hour window; exceeding them yields HTTP 429. Runway currently documents no requests-per-minute ceiling while within daily limits, but this is not permission to create unbounded bursts.

The published tier table is volatile and can be account-specific. Read the developer portal as authoritative, enforce an internal concurrency ceiling and daily/monthly credit budget below provider limits, and request custom/guaranteed capacity through Runway for production SLAs.

## Rights, privacy, safety, and provenance

This is operational guidance, not legal advice.

- Inputs and outputs are your responsibility. Obtain copyright, trademark, privacy, publicity, and biometric/likeness permissions; obtain informed consent for identifiable people. A public figure threshold does not create rights.
- Standard Terms (last updated 2026-05-11) say Runway does not claim ownership of inputs/outputs and does not restrict commercial output use when compliant, but outputs may not be unique and rights are not guaranteed. They also require API applications to display **Powered by Runway** linking to `runwayml.com`, and require protective end-user terms.
- A current API marketing page says both “No training on your data” and “Zero-data retention ... as default,” while the standard Terms say inputs and outputs may be used to train/improve systems under a broad license. The marketing page does not define the API-specific deletion boundary or SLA. These statements conflict in public materials. Treat the signed order form, enterprise terms/DPA, and written Runway confirmation as controlling; do not promise no training or zero retention from marketing copy alone.
- Public materials do not provide a generally applicable API retention period, deletion SLA, regional processing list, or customer-selectable data residency for this endpoint. Output links lasting 24–48h and `runway://` URIs lasting 24h are access lifetimes, not full backend-retention statements. Resolve these unknowns contractually before regulated/sensitive workloads.
- Partner models add subprocessors. Runway's enterprise FAQ says enterprise terms/DPA cover selected third-party models and providers contractually cannot train on customer content. Verify the specific API model, provider, processing region, subprocessor list, and contract for your account.
- Runway moderates text, media inputs, and outputs using automated systems and possible human review. Pre-moderate end-user content. Repeated moderated requests can lead to suspension.
- Follow the current Usage Policy, including prohibitions concerning child sexual abuse/sexualization, non-consensual intimate content, severe violence, fraud/deception, illegal activity, privacy violations, hateful/harassing abuse, and attempts to bypass safeguards. Consult the full policy; a summary is not exhaustive.
- Runway states that generated outputs include C2PA provenance metadata. Preserve original bytes and metadata, hash at ingestion, and record task/model/prompt provenance. Verify actual delivered files because transformations, re-encoding, screenshots, or downstream tools can strip metadata. Do not claim C2PA proves truth or consent.
- Do not put secrets, confidential personal data, or regulated data in prompts/references unless the governing contract and security review permit it. Use least-privilege asset URLs, short expiry, encryption, audit logs, and deletion workflows.

## Preflight and handoff checklist

Before submission:

- [ ] User approved billable generation, model, ratio, output count, and maximum spend.
- [ ] Prompt fits 1,000 UTF-16 units for native Gen-4; positive visual language used.
- [ ] Turbo has 1–3 references; standard Gen-4 has no more than 3.
- [ ] Tags are unique, lowercase, 3–16 chars, and mentioned correctly.
- [ ] Reference transport, MIME, size, dimensions, rights, consent, and retention are cleared.
- [ ] Version header pinned; key is server-side; task ID and job key will be persisted.
- [ ] Concurrency, timeout, cancel behavior, and retry budget are explicit.
- [ ] Output host allowlist, byte cap, MIME/magic validation, hashing, atomic storage, and manifest are ready.
- [ ] Usage policy, attribution, end-user terms, training/retention, region, and subprocessors are reviewed for this account.

At handoff, provide model and exact request parameters, task ID, cost estimate/actual credits, artifact paths and SHA-256 hashes, QA results, rejected branches, known rights/consent basis, and any unresolved provider-policy assumptions. Do not expose the API key or signed output URLs.

## First-party sources

Accessed 2026-07-09:

- API reference: https://docs.dev.runwayml.com/api/
- Model catalog: https://docs.dev.runwayml.com/guides/models/
- Getting started and image examples: https://docs.dev.runwayml.com/guides/using-the-api/
- Versioning: https://docs.dev.runwayml.com/api-details/versioning/
- SDK behavior: https://docs.dev.runwayml.com/api-details/sdks/
- Official Python SDK/OpenAPI types: https://github.com/runwayml/sdk-python
- Inputs and outputs: https://docs.dev.runwayml.com/assets/inputs/ and https://docs.dev.runwayml.com/assets/outputs/
- Ephemeral uploads: https://docs.dev.runwayml.com/assets/uploads/
- Pricing and limits: https://docs.dev.runwayml.com/guides/pricing/ and https://docs.dev.runwayml.com/usage/tiers/
- HTTP and task failures: https://docs.dev.runwayml.com/errors/errors/ and https://docs.dev.runwayml.com/errors/task-failures/
- Moderation and attribution: https://docs.dev.runwayml.com/api-details/moderation/ and https://docs.dev.runwayml.com/usage/attribution/
- Changelog: https://docs.dev.runwayml.com/api-details/api_changelog/
- Prompting and references: https://help.runwayml.com/hc/en-us/articles/35694045317139-Gen-4-Image-Prompting-Guide and https://help.runwayml.com/hc/en-us/articles/40042718905875-Creating-with-Gen-4-Image-References
- Reference-media preparation: https://docs.dev.runwayml.com/recipes/reference-media/
- Terms, privacy, and policy: https://runwayml.com/terms-of-use, https://runwayml.com/privacy-policy, and https://runwayml.com/safety/usage-policy
- API and enterprise claims: https://runwayml.com/api and https://help.runwayml.com/hc/en-us/articles/51248305153683-Enterprise-FAQ-Third-party-Models-in-Runway


