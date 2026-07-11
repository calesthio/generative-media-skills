---
name: leonardo-image
description: Create, edit, guide, upscale, and quality-control still images with Leonardo.Ai's official Production API, including native Lucid and Phoenix models, uploaded or generated references, image-to-image, ControlNet guidance, realtime-canvas inpainting, Pro and Universal upscalers, and custom Elements or models. Use for Leonardo image API implementation, async polling or webhooks, dry-run and cost governance, secure artifact handling, prompt iteration, or production troubleshooting. Do not use for Leonardo video, 3D generation, unofficial wrappers, or third-party gateway APIs.
---

# Leonardo image production

Operate Leonardo.Ai's official Production API for still images. Keep native Leonardo models, partner models hosted by Leonardo, realtime-canvas endpoints, and legacy endpoints visibly separate: they have different routes and schemas.

## Start with a production brief

Collect or propose:

- Deliverable: subject, setting, style, composition, aspect/dimensions, output count, and acceptance criteria.
- Operation: text-to-image, image-to-image, reference guidance, masked edit, upscale, background removal, or custom training.
- Source media: local paths or Leonardo image IDs, whether each is uploaded or generated, and the intended role of each reference.
- Rights: ownership/licence, likeness consent, privacy classification, and whether public visibility is allowed.
- Runtime: direct REST, official Python SDK, or official TypeScript SDK.
- Spend: calculator estimate, hard budget, concurrency ceiling, and whether auto-top-up is disabled.

Default to a one-image private preview at a conservative dimension. Before any paid call, state the exact route, model/model ID, settings, sample count, calculator estimate, and why. Wait for explicit approval. Never silently change model, visibility, reference method, quality mode, or sample-to-batch scope.

## Evidence snapshot and boundaries

The contracts below were checked against first-party Leonardo documentation, the official SDK repositories, changelog, policies, and legal pages on **2026-07-10**. Recheck them before production: Leonardo is actively moving API pricing to PAYG, adds model-specific v2 contracts, and publishes occasional conflicting examples.

This skill covers:

- Native Leonardo still models on `POST /api/rest/v1/generations`.
- Still-image references, uploaded inputs, image-to-image, current `controlnets`, and LCM inpainting.
- Still-image upscalers and custom image Elements/models.

It excludes video endpoints, 3D generation, Blueprints as a general orchestration system, the Leonardo web editor itself, MCP proxies, and unofficial SDKs. Some partner image models are available *inside* Leonardo's API; label them as partner models and use their own v2 guide rather than treating them as Lucid/Phoenix variants.

## Choose the native model deliberately

These IDs were current on the verification date:

| Native model | `modelId` | Provider-described strengths | Practical choice |
|---|---|---|---|
| Lucid Origin | `7b592283-e8a7-4c5a-9ba6-d18c31f258b9` | Versatile, prompt-responsive, broad style range, graphic/text work | General ideation, stylized or designed imagery, precise briefs |
| Lucid Realism | `05ce0082-2d80-4a2d-8653-4d1c85e2418e` | Photorealism, natural light, cinematic mood | Portraits, products, editorial photography |
| Phoenix 1.0 | `de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3` | Prompt adherence and controlled layouts | Complex composition, stylized assets, multi-reference guidance |
| Phoenix 0.9 | `6b645e3a-d64f-4341-a6d8-7a3690fbf042` | Earlier Phoenix behavior | Reproduce an established 0.9 pipeline only |

The strengths are Leonardo claims and editorial guidance, not universal benchmark results. Run a representative one-image comparison when model choice matters. Call `GET /api/rest/v1/platformModels` or use **Get API Code** to confirm availability and IDs; a documentation list is not an entitlement for every account.

### Native v1 create contract

```http
POST https://cloud.leonardo.ai/api/rest/v1/generations
Authorization: Bearer $LEONARDO_API_KEY
Accept: application/json
Content-Type: application/json
```

The body is case-sensitive. `prompt` is the only universally required field in the generic reference, but production requests should pin a model and settings. A conservative native request is:

```json
{
  "modelId": "7b592283-e8a7-4c5a-9ba6-d18c31f258b9",
  "prompt": "Editorial product photograph of a cobalt travel mug on pale limestone, three-quarter view, soft north-window light, clear negative space on the right.",
  "negative_prompt": "warped logo, duplicate handle, illegible text, watermark",
  "width": 1024,
  "height": 1024,
  "num_images": 1,
  "contrast": 3.5,
  "alchemy": false,
  "ultra": false,
  "public": false,
  "seed": 18427
}
```

Current documented constraints and caveats:

- `prompt`: required; generic v1 generation rejects more than 1,500 characters.
- `negative_prompt`: optional generic v1 field. Use concrete visual exclusions; model adherence varies.
- `num_images`: documented common range 1–8, default 4, but the accepted maximum may shrink with dimensions and features. Start at 1.
- `contrast`: model guides use `3`, `3.5`, or `4` for low/medium/high; the generic reference exposes a wider 1–4.5 range. Use the model guide's three values unless Get API Code proves another value.
- `width`, `height`: must be model-compatible. A common-values page says 512–1536 and multiples of 8; Lucid's official sample uses 1920×1080; the error guide says Alchemy inputs should be 32–1024 and multiples of 8. These first-party statements conflict. Use the current model guide/Get API Code and calculator, and validate the exact combination with a one-image preview. Do not impose one universal range.
- `alchemy`: supported for Phoenix and some legacy SD models; Lucid guides say it is unsupported. Omit it for Lucid or set it false only when matching exported code.
- `ultra`: optional model-specific quality/upscale mode; it changes cost and may affect dimensions.
- `styleUUID`: optional current style UUID. Style IDs are volatile; obtain them from the model guide or exported code.
- `enhancePrompt`: boolean in the API reference, despite some model-guide tables calling it a string. `enhancePromptInstruction` refines the enhancement. Record both original and enhanced intent.
- `public`: explicitly set `false` for private API production. Do not rely on an undocumented default.
- `seed`: optional. Public v1 create docs do not publish one consistent cross-model maximum; model guides disagree by one around Flux limits. Use a modest non-negative integer and treat seed as a repeatability aid, not a byte-identical guarantee.
- `transparency`, scheduler, inference steps, `photoReal`, Elements, and legacy fields are model-specific. Only copy them from the selected current model guide or Get API Code.

Create returns a `generationId` (commonly under `sdGenerationJob.generationId`), not finished images.

## Do not mix v1 and v2 model shapes

Leonardo's v2 route is a model dispatcher:

```json
{
  "model": "model-specific-slug",
  "public": false,
  "parameters": {
    "prompt": "model-specific prompt",
    "quantity": 1,
    "width": 1024,
    "height": 1024
  }
}
```

Submit it to `POST /api/rest/v2/generations` only for a model whose current guide defines that shape. Current image guides include partner families such as FLUX, GPT Image, Ideogram, Nano Banana/Gemini, and Seedream. They differ in allowed sizes, reference counts, quality names, prompt enhancement, and seeds.

As of 2026-07-10, GPT Image-1.5 and Ideogram 3.0 no longer accept `mode`; their documented replacement is `quality` (`LOW|MEDIUM|HIGH` for GPT Image-1.5 and `TURBO|BALANCED|QUALITY` for Ideogram 3.0). One stale GPT guide still shows `mode`. Follow the deprecations page and the current `/me/docs/` guide, not cached snippets.

Do not send v1 `modelId`, `num_images`, `styleUUID`, or `controlnets` inside a v2 partner request unless that specific guide documents them.

## Bring images into Leonardo safely

Uploaded references use a two-step flow:

1. `POST /api/rest/v1/init-image` with `{ "extension": "png" }`. Allowed documented extensions are `png`, `jpg`, `jpeg`, and `webp`.
2. Parse `uploadInitImage.fields`, then multipart-POST those fields plus the raw binary file to the returned presigned `url` within two minutes.

The presigned upload normally returns 200 or 204. The init image ID was issued by step 1; the storage response does not issue another. Never send the Leonardo bearer token to the presigned storage host. Disable redirects, validate HTTPS and the host against an approved suffix list, and ensure the file's magic bytes and MIME match the declared extension.

Use `DELETE /api/rest/v1/init-image/{id}` when the uploaded input is no longer needed. A generated image ID and uploaded init image ID are not interchangeable:

- `init_image_id`: ID returned by Upload Init Image.
- `init_generation_image_id`: image ID returned inside a completed Leonardo generation.
- `controlnets[].initImageType`: `UPLOADED` or `GENERATED`, paired with the appropriate image ID.

## References and image guidance

Prefer current `controlnets` objects over deprecated `controlNet`, `controlNetType`, and `weighting` fields. A control object can contain:

```json
{
  "initImageId": "IMAGE_UUID",
  "initImageType": "UPLOADED",
  "preprocessorId": 430,
  "strengthType": "Mid"
}
```

Current native preprocessor IDs:

| Native model | Style reference | Character reference | Content reference |
|---|---:|---:|---:|
| Lucid Origin / Lucid Realism docs | 431 | not documented | 430 |
| Phoenix 1.0 / 0.9 | 166 | 397 | 364 |

The Lucid guide labels the same IDs for Origin while the general guidance table labels them under Lucid Realism; verify with the selected model's guide. Character Reference is not a face swap and does not guarantee a replica. For content and character references, documented strengths are `Low`, `Mid`, `High`; style references can extend through `Ultra` and `Max`. Multiple style references may use `influence` as a relative ratio; the values need not sum to 1.

For classic image-to-image, use exactly one of `init_image_id` or `init_generation_image_id` with `init_strength`. Higher strength generally permits more deviation. Keep source and requested output aspect compatible to reduce deformation.

Use one reference role at a time while tuning:

1. Lock content/composition.
2. Lock style.
3. Add character guidance only with consent and a clean, well-lit source.
4. Lower the strongest control if the output becomes stiff or copies irrelevant source details.

## Masked edits and upscaling

### Realtime-canvas inpainting

`POST /api/rest/v1/lcm-inpainting` is the clearest current masked-edit contract. It requires JPEG data URIs in `imageDataUrl` and `maskDataUrl`, plus `prompt`. The mask must match the image dimensions; white is regenerated and black is preserved. Documented parameters include:

- `width`, `height`: each 512, 640, or 1024.
- `guidance`: 0.5–20.
- `strength`: 0.1–1; higher deviates more.
- `steps`: 4–16.
- optional style and seed.

This is a realtime-canvas LCM edit, not Lucid/Phoenix inpainting. The generic v1 create schema also exposes `canvasRequest`, `canvasRequestType` (`INPAINT|OUTPAINT|SKETCH2IMG|IMG2IMG`), `canvasInitId`, and `canvasMaskId` after `POST /api/rest/v1/canvas-init-image`, but the current public guide does not fully specify a model-compatibility matrix. Use exported code or support confirmation before production.

### Upscale selection

For current Pro Upscalers, call `POST /api/rest/v2/generations` with one image reference:

- `model: "aurora-upscaler-precise"`: `upscale_factor` in `2|3|4|5|6|8`; `upscale_mode` is `clean` or `detailed`. Choose for fidelity/cleanup.
- `model: "aurora-upscaler-creative"`: same factor set; `creativity` is `low|mid|high`. Choose when reconstruction is acceptable.
- Reference type can be `GENERATED`, `UPLOADED`, or `VARIATION`; send the input's actual pixel width and height; set `public:false`.

The Creative guide's sample/title use `aurora-upscaler-creative`, but its parameter table mistakenly says `aurora-upscaler-precise`. Treat the sample/title as intended and verify with Get API Code.

The older Universal Upscaler is `POST /api/rest/v1/variations/universal-upscaler`. Its documented fields include one of `generatedImageId`, `initImageId`, or `variationId`, `upscaleMultiplier` (legacy guide: 1–2), `creativityStrength`, optional prompt, and style. The API reference—not a recipe that mistakenly shows GET—is authoritative for the HTTP method. Universal output is capped at 20 MP in its guide. Legacy variation endpoints may reject uploaded images; the Pro v2 upscalers explicitly support them.

## Custom Elements and models

Only train when a reusable identity/style/product benefit justifies cost and data risk.

Element (LoRA) flow:

1. `POST /api/rest/v1/datasets`.
2. For each image, `POST /api/rest/v1/datasets/{datasetId}/upload`, then complete the two-minute presigned multipart upload.
3. `POST /api/rest/v1/elements` with dataset, trigger (`instance_prompt`), SDXL configuration, and training parameters.
4. Poll `GET /api/rest/v1/elements/{id}`; training may take minutes to hours.
5. Generate on a compatible base model using `userElements: [{"userLoraId": ID, "weight": 1}]` and include the trigger phrase.

The current Element guide describes SDXL training at 1024×1024. The separate custom-model endpoint is `POST /api/rest/v1/models`, with required `name`, `datasetId`, and `instance_prompt`; documented options include `modelType`, `sd_version` (`v1_5|v2`), strength, and resolution. Do not conflate Elements with full custom models.

Curate rights-cleared, representative, sharp, consistently captioned images; avoid near-duplicates, watermarks, sensitive attributes, and unconsented faces. Hold out validation images. Record dataset file hashes, licences/consent, captions, training request, trigger, returned ID, base compatibility, cost, and deletion decision. Training concurrency defaults to 5 jobs.

## Prompting and iterative craft

Build the positive prompt from visual facts:

```text
[medium] of [subject and defining attributes] [action/pose] in [environment].
[framing, viewpoint, spatial arrangement]. [lighting]. [palette/materials].
[lens/focus/finish/mood]. Exact visible text: "...".
```

Be specific about subject and context before style keywords. Describe camera and lighting only when they affect the result. For exact typography, quote the text, describe placement and hierarchy, then inspect every character; no model makes trademark or spelling review unnecessary.

Use `negative_prompt` for a small set of observable defects, not a contradictory essay. If prompt enhancement is enabled, treat it as a creative transformation: retain the original prompt, enhancement instruction, exported request, and final resolved settings.

Iterate through a ledger:

1. One-image private draft at a safe size.
2. Change one variable: prompt, model, style, reference strength, or seed.
3. Promote an approved image ID into the next reference/edit step.
4. Upscale only after composition, text, identity, and rights review pass.
5. Record model ID/slug, full request, seed, reference IDs and hashes, generation ID, cost, output IDs/hashes, and decision.

Review full resolution for prompt adherence; composition; hand/anatomy and object geometry; character/product identity; text/logo accuracy; lighting/perspective consistency; reference leakage; seams/halos; NSFW flag; privacy/likeness/IP; and final pixels, color, alpha, and file format.

## Async lifecycle: webhook first, polling as reconciliation

`GET /api/rest/v1/generations/{generationId}` returns `generations_by_pk`. Documented statuses are `PENDING`, `COMPLETE`, and `FAILED`. A 200 with `generated_images: []` is not success while status is pending.

Leonardo recommends webhooks instead of frequent polling. Configure an HTTPS callback URL and callback API key while creating a Production API key. Leonardo sends:

- `authorization: Bearer <callback-secret>` (a separate secret from the Production API key).
- Event type such as `image_generation.complete`.
- Generation data including status and image URLs.

Use constant-time bearer comparison, TLS, a byte cap, strict JSON/content-type parsing, and an idempotency key such as event type plus generation ID. Queue work, return quickly, then fetch the generation by ID using your own API credentials. Redact before logging: the published sample payload contains an `apiKey` object and callback details. Leonardo publishes callback source IPs, but they are volatile and should supplement—not replace—secret validation.

Public docs do not specify an HMAC signature, delivery retry schedule, ordering guarantee, or replay window. Therefore keep periodic GET reconciliation for stuck jobs and make webhook processing idempotent. To rotate callback configuration, create a new Production API key with the new URL/secret, switch traffic, then delete the old key.

## Complete dry-run-first Python example

This example covers a private Lucid Origin preview, optional uploaded content reference, task ledger, conservative polling, NSFW rejection, and secure artifact persistence. It prints a dry run by default. It makes billable/upload calls only with `--execute`, a calculator estimate, and a budget that accepts that estimate.

```python
#!/usr/bin/env python3
import argparse, hashlib, ipaddress, json, math, os, random, socket, stat, subprocess, tempfile, time
from pathlib import Path
from urllib.parse import urlparse
import requests
from PIL import Image, UnidentifiedImageError

BASE = "https://cloud.leonardo.ai/api/rest"
ORIGIN = "7b592283-e8a7-4c5a-9ba6-d18c31f258b9"
MAX_DOWNLOAD = 30 * 1024 * 1024
MAX_UPLOAD = 30 * 1024 * 1024
MAX_API_JSON = 4 * 1024 * 1024
MAX_IMAGE_PIXELS = 24_000_000
Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS

def atomic_json(path, value):
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            fd = None
            json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if fd is not None: os.close(fd)
        if os.path.exists(tmp): os.unlink(tmp)

def allowed_https(url, suffixes):
    p = urlparse(url); host = (p.hostname or "").lower()
    if (p.scheme != "https" or p.username or p.password or p.fragment or not host
            or p.port not in (None, 443)):
        raise ValueError("unsafe URL")
    normalized = tuple(s.lower().lstrip(".").rstrip(".") for s in suffixes)
    if not any(host == s or host.endswith("." + s) for s in normalized):
        raise ValueError(f"host not allowlisted: {host}")
    for info in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        if not ipaddress.ip_address(info[4][0]).is_global:
            raise ValueError("URL resolves to a non-public address")
    return url

def api(session, key, method, path, body=None, timeout=(10, 60)):
    with session.request(method, BASE + path, json=body, timeout=timeout, stream=True,
            allow_redirects=False, headers={"Authorization": f"Bearer {key}",
            "Accept": "application/json", "Content-Type": "application/json"}) as response:
        response.raise_for_status()
        if response.status_code == 204 or response.headers.get("Content-Length") == "0":
            return {}
        ctype = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
        if ctype != "application/json": raise ValueError(f"unexpected API media type: {ctype}")
        raw = response.raw.read(MAX_API_JSON + 1, decode_content=True)
        if len(raw) > MAX_API_JSON: raise ValueError("API JSON exceeded byte cap")
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict): raise ValueError("API response was not a JSON object")
    return value

def inspect_image_handle(handle, extension):
    opened = os.fstat(handle.fileno())
    if not stat.S_ISREG(opened.st_mode): raise ValueError("reference must be a regular file")
    size = opened.st_size
    if size <= 0 or size > MAX_UPLOAD: raise ValueError("reference file size is outside the local cap")
    handle.seek(0)
    head = handle.read(12)
    if head.startswith(b"\xff\xd8\xff"):
        expected_format, ext, mime = "JPEG", {"jpg", "jpeg"}, "image/jpeg"
    elif head.startswith(b"\x89PNG\r\n\x1a\n"):
        expected_format, ext, mime = "PNG", {"png"}, "image/png"
    elif head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        expected_format, ext, mime = "WEBP", {"webp"}, "image/webp"
    else:
        raise ValueError("reference magic is not JPEG, PNG, or WebP")
    if extension.lower().lstrip(".") not in ext: raise ValueError("reference extension/magic mismatch")
    try:
        handle.seek(0)
        with Image.open(handle) as probe:
            dimensions, decoded_format = probe.size, probe.format
            if dimensions[0] * dimensions[1] > MAX_IMAGE_PIXELS:
                raise ValueError(f"reference exceeds pixel cap: {dimensions}")
            probe.verify()
        handle.seek(0)
        with Image.open(handle) as probe: probe.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError("reference failed bounded full decode") from exc
    if decoded_format != expected_format: raise ValueError("reference decoder/magic mismatch")
    digest = hashlib.sha256()
    handle.seek(0)
    for chunk in iter(lambda: handle.read(1024 * 1024), b""): digest.update(chunk)
    handle.seek(0)
    return {"extension": extension.lower().lstrip("."), "mime": mime, "bytes": size,
            "dimensions": list(dimensions), "sha256": digest.hexdigest()}

def inspect_local_image(path):
    if path.is_symlink(): raise ValueError("reference symlinks are not accepted")
    path = path.resolve(strict=True)
    with path.open("rb") as source:
        evidence = inspect_image_handle(source, path.suffix)
    return path, evidence

def upload_init(session, key, path, upload_suffixes, expected_evidence):
    if path.is_symlink(): raise ValueError("reference symlinks are not accepted")
    source_path = path.resolve(strict=True)
    suffix = source_path.suffix.lower()
    if suffix.lstrip(".") not in {"png", "jpg", "jpeg", "webp"}:
        raise ValueError("unsupported image extension")
    with tempfile.TemporaryFile(prefix="leonardo-approved-", suffix=suffix) as snapshot:
        with source_path.open("rb") as source:
            opened = os.fstat(source.fileno())
            if not stat.S_ISREG(opened.st_mode): raise ValueError("reference must be a regular file")
            if opened.st_size <= 0 or opened.st_size > MAX_UPLOAD:
                raise ValueError("reference file size is outside the local cap")
            copied = 0
            while chunk := source.read(1024 * 1024):
                copied += len(chunk)
                if copied > MAX_UPLOAD: raise ValueError("reference changed beyond upload byte cap")
                snapshot.write(chunk)
            snapshot.flush(); os.fsync(snapshot.fileno())
        evidence = inspect_image_handle(snapshot, suffix)
        if evidence != expected_evidence:
            raise ValueError("reference changed after approval; obtain a new approval hash")
        ext = suffix.lstrip(".")
        issued = api(session, key, "POST", "/v1/init-image", {"extension": ext})["uploadInitImage"]
        fields = json.loads(issued["fields"]) if isinstance(issued["fields"], str) else issued["fields"]
        snapshot.seek(0)
        # Upload the exact validated, continuously held snapshot handle; never reopen a path.
        # Never forward the Leonardo Authorization header to storage.
        with requests.post(allowed_https(issued["url"], upload_suffixes), data=fields,
                files={"file": (source_path.name, snapshot, evidence["mime"])},
                timeout=(10, 120), allow_redirects=False) as response:
            if response.status_code not in (200, 204): response.raise_for_status()
        return issued["id"], evidence

def poll(session, key, generation_id, out, timeout_s=900):
    deadline, delay = time.monotonic() + timeout_s, 5.0
    while time.monotonic() < deadline:
        try:
            raw = api(session, key, "GET", f"/v1/generations/{generation_id}")
            generation = raw["generations_by_pk"]; delay = 5.0
        except requests.HTTPError as e:
            if e.response.status_code not in (429, 500, 502, 503, 504): raise
            time.sleep(delay + random.uniform(0, delay * 0.5)); delay = min(delay * 2, 30); continue
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(delay + random.uniform(0, delay * 0.5)); delay = min(delay * 2, 30); continue
        atomic_json(out / "status.json", {"id": generation_id, "status": generation.get("status")})
        status = generation.get("status")
        if status == "COMPLETE": return generation
        if status == "FAILED": raise RuntimeError("Leonardo generation failed")
        if status != "PENDING": raise RuntimeError(f"unknown status: {status}")
        time.sleep(5 + random.uniform(0, 1))
    raise TimeoutError("local wait expired; no cancellation was performed")

def download(session, url, image_id, out, output_suffixes, scanner_command):
    fd = None
    tmp = None
    digest = hashlib.sha256()
    total = 0
    try:
        with session.get(allowed_https(url, output_suffixes), stream=True, timeout=(10, 60),
                allow_redirects=False, headers={"Accept": "image/*"}) as response:  # no API Authorization
            response.raise_for_status()
            ctype = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
            ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(ctype)
            if not ext: raise ValueError(f"unexpected media type: {ctype}")
            declared = response.headers.get("Content-Length")
            if declared:
                try: declared_size = int(declared)
                except ValueError as exc: raise ValueError("invalid Content-Length") from exc
                if declared_size < 0 or declared_size > MAX_DOWNLOAD:
                    raise ValueError("artifact exceeds declared byte cap")
            fd, tmp = tempfile.mkstemp(dir=out, suffix=".part")
            with os.fdopen(fd, "wb") as f:
                fd = None
                for chunk in response.iter_content(1024 * 1024):
                    if not chunk: continue
                    total += len(chunk)
                    if total > MAX_DOWNLOAD: raise ValueError("artifact exceeded streaming byte cap")
                    digest.update(chunk); f.write(chunk)
                f.flush(); os.fsync(f.fileno())
        head = Path(tmp).read_bytes()[:12]
        ok = (head.startswith(b"\xff\xd8\xff") if ext == ".jpg" else
              head.startswith(b"\x89PNG\r\n\x1a\n") if ext == ".png" else
              head[:4] == b"RIFF" and head[8:12] == b"WEBP")
        if not ok: raise ValueError("image signature mismatch")
        expected_format = {".jpg": "JPEG", ".png": "PNG", ".webp": "WEBP"}[ext]
        try:
            with Image.open(tmp) as probe:
                dimensions, decoded_format = probe.size, probe.format
                if dimensions[0] * dimensions[1] > MAX_IMAGE_PIXELS:
                    raise ValueError(f"artifact exceeds pixel cap: {dimensions}")
                probe.verify()
            with Image.open(tmp) as probe: probe.load()
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
            raise ValueError("artifact failed bounded full decode") from exc
        if decoded_format != expected_format: raise ValueError("artifact MIME/magic/decoder mismatch")
        subprocess.run([*scanner_command, tmp], check=True, timeout=120,
                       stdin=subprocess.DEVNULL, capture_output=True)
        final = out / f"{image_id}{ext}"
        os.replace(tmp, final)
        tmp = None
        return {"id": image_id, "path": str(final), "bytes": total, "mime": ctype,
                "dimensions": list(dimensions), "sha256": digest.hexdigest(),
                "securityScan": "passed"}
    finally:
        if fd is not None: os.close(fd)
        if tmp is not None and os.path.exists(tmp): os.unlink(tmp)

parser = argparse.ArgumentParser()
parser.add_argument("--prompt", required=True)
parser.add_argument("--reference", type=Path)
parser.add_argument("--estimated-usd", type=float, required=True,
    help="copy the current estimate from Leonardo's API pricing calculator")
parser.add_argument("--execute", action="store_true")
args = parser.parse_args()
if len(args.prompt) > 1500: raise SystemExit("prompt exceeds 1500 characters")
if not math.isfinite(args.estimated_usd) or args.estimated_usd <= 0:
    raise SystemExit("estimated-usd must be finite and positive")
try: budget = float(os.environ.get("LEONARDO_MAX_USD", "0"))
except ValueError as exc: raise SystemExit("LEONARDO_MAX_USD must be numeric") from exc
if not math.isfinite(budget) or budget < 0: raise SystemExit("LEONARDO_MAX_USD must be finite and non-negative")
body = {"modelId": ORIGIN, "prompt": args.prompt, "width": 1024, "height": 1024,
        "num_images": 1, "contrast": 3.5, "public": False, "seed": 18427}
preview = dict(body)
reference_evidence = None
if args.reference:
    _, reference_evidence = inspect_local_image(args.reference)
    preview["controlnets"] = [{"initImageId": "<uploaded-at-execution>",
        "initImageType": "UPLOADED", "preprocessorId": 430, "strengthType": "Mid"}]
approval_record = {"request": preview, "reference": reference_evidence,
                   "estimatedUsd": args.estimated_usd, "maxUsd": budget}
approval_sha256 = hashlib.sha256(json.dumps(
    approval_record, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
print(json.dumps({"dryRun": not args.execute, "estimatedUsd": args.estimated_usd,
                  "maxUsd": budget, "request": preview,
                  "referenceEvidence": reference_evidence,
                  "approvalSha256": approval_sha256}, indent=2))
if not args.execute: raise SystemExit(0)
if budget <= 0 or args.estimated_usd > budget: raise SystemExit("estimate is not within approved budget")
if os.environ.get("LEONARDO_APPROVED_REQUEST_SHA256") != approval_sha256:
    raise SystemExit("approval hash does not match this exact request, source, estimate, and budget")
try: scanner_command = json.loads(os.environ["LEONARDO_IMAGE_SCAN_COMMAND_JSON"])
except (KeyError, json.JSONDecodeError) as exc:
    raise SystemExit("set LEONARDO_IMAGE_SCAN_COMMAND_JSON to an approved scanner argv array") from exc
if (not isinstance(scanner_command, list) or not scanner_command
        or not all(isinstance(value, str) and value for value in scanner_command)):
    raise SystemExit("LEONARDO_IMAGE_SCAN_COMMAND_JSON must be a non-empty string array")
key = os.environ["LEONARDO_API_KEY"]
upload_suffixes = tuple(x.strip().lower() for x in os.environ["LEONARDO_UPLOAD_HOST_SUFFIXES"].split(",") if x.strip())
output_suffixes = tuple(x.strip().lower() for x in os.environ.get(
    "LEONARDO_OUTPUT_HOST_SUFFIXES", "cdn.leonardo.ai").split(",") if x.strip())
out = Path(os.environ.get("LEONARDO_OUTPUT_DIR", "leonardo-output")).resolve(); out.mkdir(parents=True, exist_ok=True)
session = requests.Session()
client_job_key = f"leonardo-{approval_sha256[:20]}"
job_path = out / "job.json"
atomic_json(job_path, {"state": "pre_submit", "clientJobKey": client_job_key,
    "approvalSha256": approval_sha256, "requestSha256": approval_sha256,
    "modelId": ORIGIN, "estimatedUsd": args.estimated_usd,
    "reference": reference_evidence, "updatedUnix": time.time()})
if args.reference:
    init_id, uploaded_evidence = upload_init(
        session, key, args.reference.resolve(), upload_suffixes, reference_evidence
    )
    body["controlnets"] = [{"initImageId": init_id, "initImageType": "UPLOADED",
        "preprocessorId": 430, "strengthType": "Mid"}]
actual_request_sha256 = hashlib.sha256(json.dumps(
    body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
atomic_json(job_path, {"state": "ready_to_submit", "clientJobKey": client_job_key,
    "approvalSha256": approval_sha256, "requestSha256": actual_request_sha256,
    "modelId": ORIGIN, "estimatedUsd": args.estimated_usd,
    "reference": reference_evidence, "updatedUnix": time.time()})
try:
    created = api(session, key, "POST", "/v1/generations", body)
except (requests.ConnectionError, requests.Timeout) as e:
    atomic_json(job_path, {"state": "ambiguous_create", "clientJobKey": client_job_key,
        "approvalSha256": approval_sha256, "requestSha256": actual_request_sha256,
        "modelId": ORIGIN, "estimatedUsd": args.estimated_usd,
        "reference": reference_evidence, "updatedUnix": time.time(),
        "note": "Do not replay; reconcile generations and account cost"})
    raise SystemExit(f"create outcome unknown; reconcile before retrying: {e}")
job = created.get("sdGenerationJob", created); generation_id = job.get("generationId")
if not generation_id: raise RuntimeError("create response did not contain generationId")
atomic_json(job_path, {"state": "submitted", "clientJobKey": client_job_key,
    "generationId": generation_id, "approvalSha256": approval_sha256,
    "requestSha256": actual_request_sha256, "modelId": ORIGIN,
    "estimatedUsd": args.estimated_usd,
    "createdCost": job.get("cost") or job.get("apiCreditCost"),
    "reference": reference_evidence, "updatedUnix": time.time()})
generation = poll(session, key, generation_id, out)
artifacts = []
for image in generation.get("generated_images", []):
    if image.get("nsfw"): raise RuntimeError(f"output rejected by NSFW policy: {image.get('id')}")
    artifacts.append(download(session, image["url"], image["id"], out,
                              output_suffixes, scanner_command))
if not artifacts: raise RuntimeError("COMPLETE generation returned no accepted images")
atomic_json(out / "manifest.json", {"generationId": generation_id, "status": "COMPLETE",
    "clientJobKey": client_job_key, "modelId": ORIGIN,
    "approvalSha256": approval_sha256,
    "requestSha256": actual_request_sha256,
    "promptSha256": hashlib.sha256(args.prompt.encode()).hexdigest(),
    "reference": reference_evidence,
    "estimatedUsd": args.estimated_usd,
    "actualCost": generation.get("cost") or generation.get("apiDollarCost"),
    "nsfwAccepted": False, "creativeQa": "pending", "rightsReview": "required",
    "provenance": "original provider bytes preserved; no universal C2PA claim",
    "artifacts": artifacts, "completedUnix": time.time()})
print(json.dumps(artifacts, indent=2))
```

For a webhook handler, use `hmac.compare_digest` for its separate callback bearer secret. Set upload suffixes from a reviewed presigned response/environment policy rather than hard-coding a storage provider.

## Failure, retry, and duplicate-cost policy

Separate HTTP response failures, terminal generation status, and quality failures.

| Signal | Response |
|---|---|
| 400 validation, invalid dimensions, too many images, prompt >1500 | Fix payload/model combination; do not retry unchanged |
| 401/403 auth | Correct/rotate key; do not retry unchanged |
| 403 moderation | Do not bypass; revise or reject against Terms |
| 404 ID/model | Verify generation vs image vs init ID and current model availability |
| 429 | Respect account limits; bounded exponential backoff with jitter |
| 5xx/network on GET | Bounded backoff with jitter; GET is safe to repeat |
| `PENDING` + empty images | Continue waiting or reconcile webhook; not success |
| `FAILED` | Preserve ID and diagnostic response, then classify before a changed retry |
| `COMPLETE` + `nsfw:true` | Quarantine/reject; add a separate moderation layer when needed |

The official SDKs expose configurable retries, but public docs do not document a create-generation idempotency key. Do not blindly retry `POST /generations` after a timeout because the job may have been accepted and billed. Persist a local job key before submission, store `generationId` immediately, and retry only reads. For an ambiguous create, stop automatic submission and reconcile recent account generations/cost/support.

Presigned upload URLs last two minutes; request a new one rather than retrying an expired URL. Never reuse a generation ID where an image ID is required.

## Cost and capacity governance

Leonardo's current Production API is transitioning to PAYG with a dollar balance. Cost depends on model, dimensions, count, quality/features, guidance, upscale, or training. Leonardo does not publish a stable complete per-model dollar table in the public docs; do not invent one.

Before execution:

1. Use the API pricing calculator in API Access with the exact configuration.
2. Record the estimate and enforce a local hard limit.
3. Keep `num_images:1` until the prompt/reference branch passes.
4. Disable or tightly cap automatic top-up for unattended services.
5. Record the returned `cost` object; `apiCreditCost` remains during migration.

PAYG balance does not expire. Web-app subscription tokens and API billing are separate. Custom plans can change limits and discounts; the portal/order form is authoritative.

Default published limits on 2026-07-10:

- 10 concurrent image-generation jobs.
- 5 concurrent training jobs.
- 200 queued/pending image generations; 100 queued upscales.
- 2,000 requests/minute overall.
- 100 create-generation requests/minute and 100/minute for each documented variation/upscaler create route.

One concurrency unit is described as adding 10 generation requests and 20 pending image jobs. These limits may be customized. Enforce lower application-side limits, honor 429s, and protect per-user budgets even if the provider accepts more work.

## Artifact, key, and webhook security

- Use named Production API keys in a server-side secret manager; never embed them in browser/mobile code. Current FAQ says an account can hold 10 keys. Rotate and delete unused keys.
- Treat all API responses and webhook bodies as sensitive. Persist an allowlisted projection, not raw objects that may include account/key metadata.
- Keep `public:false`. A private generation is not permission to upload secrets, regulated data, or unconsented biometric/likeness material.
- API-generated image URLs are documented as non-expiring and accessible in the web app. That is not a storage SLA. Download promptly, validate HTTPS/host/DNS, do not forward API credentials, cap bytes, verify MIME plus magic bytes, save atomically, hash, and store in controlled durable storage.
- Do not proxy arbitrary task-provided URLs. Maintain separate allowlists for presigned upload hosts and Leonardo output CDN hosts; reject redirects and private/reserved addresses.
- Delete generations with `DELETE /api/rest/v1/generations/{id}` and uploaded inputs with `DELETE /api/rest/v1/init-image/{id}` when required. Verify deletion behavior in your account and retain evidence; public docs do not state a backup-deletion SLA.

## Rights, privacy, safety, and provenance

This is operational guidance, not legal advice.

- You retain input ownership and must have all rights, licences, privacy permissions, and likeness consent. Do not use Character Reference or training as a face-swap/impersonation shortcut.
- Current Terms (2026-01-19) say paid subscribers own compliant Content as between the parties, and Leonardo assigns any interest it has. Outputs may be non-unique; Leonardo disclaims title/non-infringement warranties. The API page separately says API customers retain inputs and receive output rights. The governing subscription/order form controls.
- Always set `public:false`. Terms say Private Content is used only to perform obligations/exercise rights and will not be used, retained, analysed, or processed for model training/new products without express written consent. Public Content receives a broad perpetual licence that includes training and commercial use. The API page says API inputs and generated images are not used for training; privacy materials align this protection with private paid content. Do not generalize it to public content.
- Generated API images are documented as non-expiring; the privacy policy instead gives purpose-based retention, and Terms allow inactive accounts (12+ months) to be deleted. These statements address different layers. There is no public endpoint-specific deletion/backup SLA; contract for one if needed.
- The privacy policy says information is stored in the United States and processed in Australia and any country where Leonardo, affiliates, providers, or partners operate. No public API region parameter or customer-selectable residency was found. Use the DPA/order form for regulated workloads.
- Terms prohibit unlawful/infringing use, misleading or defamatory impersonation, sexual abuse/violence, explicit pornography, child exploitation, non-consensual depictions, animal cruelty, extreme gore, hate/discrimination, and endangerment. Prompt moderation may reject with 400/403; outputs include an `nsfw` flag. Add application-specific input/output moderation and human review.
- Leonardo states it is SOC 2 Type I and II certified. Treat that as a provider claim; obtain the report and control mapping for assurance work.
- No first-party API documentation found on 2026-07-10 guarantees C2PA Content Credentials, an invisible watermark, or another provenance marker on every output. Do not claim one. Preserve original bytes/metadata, hash artifacts, retain generation manifests, and disclose synthetic origin according to policy/law.

## Release checklist

- [ ] Exact native model ID or v2 model slug confirmed in current guide/account.
- [ ] Request validated against that model; no cross-model fields or deprecated parameters.
- [ ] Private one-image preview, calculator estimate, and hard budget approved.
- [ ] Reference IDs/types, preprocessing IDs, strengths, rights, consent, and deletion plan verified.
- [ ] Job key and generation ID persistence precede polling/webhook processing.
- [ ] Webhook bearer validation, idempotency, redaction, and GET reconciliation implemented.
- [ ] Ambiguous create is not automatically retried.
- [ ] NSFW/policy checks and full-resolution creative QA pass.
- [ ] Artifacts downloaded without API auth, validated, hashed, and stored durably.
- [ ] Actual cost, output IDs, provenance manifest, privacy/training/region assumptions, and deletions recorded.

## First-party source register

Accessed 2026-07-10:

- Quick start and generic API reference: https://docs.leonardo.ai/docs/getting-started and https://docs.leonardo.ai/me/reference/creategeneration
- Native model guides: https://docs.leonardo.ai/docs/lucid-origin, https://docs.leonardo.ai/me/docs/lucid-realism, and https://docs.leonardo.ai/docs/phoenix
- Models and values: https://docs.leonardo.ai/reference/listplatformmodels and https://docs.leonardo.ai/docs/commonly-used-api-values
- Image guidance and prompting: https://docs.leonardo.ai/docs/generate-images-using-image-to-image-guidance and https://leonardo.ai/news/ai-image-prompts
- Uploads: https://docs.leonardo.ai/reference/uploadinitimage and https://docs.leonardo.ai/docs/how-to-upload-an-image-using-a-presigned-url
- Lifecycle/webhooks: https://docs.leonardo.ai/reference/getgenerationbyid and https://docs.leonardo.ai/docs/guide-to-the-webhook-callback-feature
- Errors/moderation: https://docs.leonardo.ai/docs/api-error-messages and https://docs.leonardo.ai/docs/guide-to-handling-not-safe-for-work-image-generation-nsfw
- Inpainting and upscaling: https://docs.leonardo.ai/reference/performinpaintinglcm, https://docs.leonardo.ai/me/docs/pro-upscaler-precise, https://docs.leonardo.ai/me/docs/pro-upscaler-creative, and https://docs.leonardo.ai/reference/createuniversalupscalerjob
- Training: https://docs.leonardo.ai/docs/train-custom-element-and-generate-images and https://docs.leonardo.ai/reference/createmodel
- Official SDKs: https://github.com/Leonardo-Interactive/leonardo-python-sdk and https://github.com/Leonardo-Interactive/leonardo-ts-sdk
- Limits, PAYG, and pricing: https://docs.leonardo.ai/reference/limits, https://docs.leonardo.ai/docs/payg-guide, and https://docs.leonardo.ai/me/docs/pricing-and-plans-faq
- Deprecations: https://docs.leonardo.ai/me/docs/deprecations-changes
- API product/data claims: https://leonardo.ai/api
- Terms, privacy, and enterprise agreement: https://leonardo.ai/terms-of-service, https://leonardo.ai/privacy-policy, and https://leonardo.ai/master-services-agreement


