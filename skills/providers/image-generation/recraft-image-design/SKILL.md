---
name: recraft-image-design
description: Design and produce raster images, native SVG artwork, brand-controlled visuals, and documented image edits with Recraft's API. Use for Recraft model and route selection, exact request construction, image-to-image, inpainting, outpainting, background work, vectorization, remix/exploration, palette and typography control, API migration, safety and rights review, and production QA.
---

# Recraft image design

Use Recraft as a design-production system, not as a generic prompt box. Choose the model and operation from the required output contract, make only documented API calls, save returned assets immediately, and inspect the actual raster or SVG before delivery.

## Evidence labels and freshness

Interpret labels literally:

- **Documented** — stated in a first-party Recraft API reference, OpenAPI document, model page, legal page, or trust page.
- **Inference** — a conclusion derived from documented behavior but not promised by Recraft.
- **Production heuristic** — a practical workflow recommendation; test it on the current account and brief.

Volatile API facts in this skill were checked **2026-07-09**. Recheck model IDs, compatibility, pricing, limits, retention, and terms before a costly or regulated run. The human-readable API guide is the contract to prefer. The official Swagger specification sometimes exposes extra aliases or fields not explained in the guide; do not depend on those without a small validation request.

## Establish the production contract

Before calling the API, record:

1. deliverable: raster or editable SVG;
2. target aspect/size and final-use resolution;
3. exact copy that must appear, if any;
4. brand palette, forbidden colors, and style references;
5. what must remain unchanged in an edit;
6. rights/consent status for references, people, marks, and copy;
7. commercial use, provenance/disclosure, privacy, and retention requirements;
8. exploration budget and acceptance checks.

If a downstream tool requires true paths, request a vector model. A raster image that merely looks like vector art is not a substitute for SVG.

## Select a current model

**Documented, verified 2026-07-09:** `POST /v1/images/generations` defaults to `recraftv4_1`. The public guide accepts these proprietary model IDs:

| Family | Raster | Vector | Use |
|---|---|---|---|
| V4.1 expressive, standard | `recraftv4_1` | `recraftv4_1_vector` | Current default for concepting, polished art direction, typography, illustration, and general production |
| V4.1 expressive, Pro | `recraftv4_1_pro` | `recraftv4_1_pro_vector` | Same line at roughly 4 MP / higher output size for print and dense detail |
| V4.1 Utility, standard | `recraftv4_1_utility` | `recraftv4_1_utility_vector` | Cleaner, flatter, front-facing, predictable work such as product shots and mockup source imagery |
| V4.1 Utility, Pro | `recraftv4_1_utility_pro` | `recraftv4_1_utility_pro_vector` | Utility behavior with higher output size |
| V4 | `recraftv4` | `recraftv4_vector` | Previous design-forward generation family |
| V4 Pro | `recraftv4_pro` | `recraftv4_pro_vector` | Previous high-resolution family |
| V3 | `recraftv3` | `recraftv3_vector` | Keep for curated/custom styles, localized edit routes, text layout, negative prompts, and artistic-level controls |
| V2 | `recraftv2` | `recraftv2_vector` | Legacy styles/effects that exist only in V2 |

**Documented:** V4.1 was released in mid-May 2026; V4 in February 2026; V3 in October 2024; V2 in February 2024. Recraft says all 16 proprietary variants remain available through the API. No first-party deprecation dates or formal support windows were published at verification time.

**Production heuristic:** Start with V4.1 standard for inexpensive direction finding. Move only approved compositions to Pro. Choose Utility when the brief rewards predictability over drama. Retain V3 when its controls are requirements rather than trying to emulate them with undocumented V4.1 fields.

### Important compatibility boundaries

- **Documented:** V4 and V4.1 families do not support curated `style`, `style_id`, custom style creation, `negative_prompt`, V3 `text_layout`, or `artistic_level` in the human-readable compatibility tables. Put visual style into the prompt and use supported color controls.
- **Documented:** V2/V3 support named styles. API-created custom styles are for V3/V3 Vector; a style must be reused with its compatible model. `style` and `style_id` are mutually exclusive.
- **Documented conflict:** the current image-to-image endpoint prose says V3 and V4, while its parameter model list includes V4.1 raster/vector variants. Treat V4.1 image-to-image as documented-but-conflicting: verify it in the target account/contract or a budgeted validation request before production. Localized `inpaint`, `outpaint`, `replaceBackground`, and `generateBackground` are documented for V3/V3 Vector only.
- **Documented ambiguity:** an older V4 model page says prompt-based editing is not supported, reinforcing the current endpoint guide's own prose/parameter-list inconsistency. Do not extend any image-to-image support conclusion to localized edit routes.
- **Documented boundary:** third-party models shown in Recraft Studio are not part of the public Recraft API, even though internal Swagger enums may expose additional names.

## API contract

Use only the official production host:

```text
https://external.api.recraft.ai
```

Authenticate every protected request with:

```http
Authorization: Bearer $RECRAFT_API_TOKEN
```

Never send the token to an asset URL, user-provided URL, redirect target, logging service, or any host other than `external.api.recraft.ai`. Keep it in an environment variable. Do not print it.

### Core routes

**Documented, verified 2026-07-09:** all routes below are under `https://external.api.recraft.ai/v1`.

| Method and path | Purpose | Response shape |
|---|---|---|
| `POST /images/generations` | Raster or vector text-to-image | `{"created":...,"credits":...,"data":[Image...]}` |
| `POST /images/generations/raster` | Same body; enforce raster model/style | same |
| `POST /images/generations/vector` | Same body; enforce vector model/style | same |
| `POST /styles` | Create V3 custom style from images/source styles | style object plus `credits` |
| `POST /images/imageToImage` | Prompt-guided image variation/transformation | generation response |
| `POST /images/inpaint` | Fill white mask regions | generation response |
| `POST /images/outpaint` | Extend canvas | generation response |
| `POST /images/replaceBackground` | Detect and replace background | generation response |
| `POST /images/generateBackground` | Fill a supplied background mask | generation response |
| `POST /images/vectorize` | Raster to SVG | `{"created":...,"credits":...,"image":Image}` |
| `POST /images/removeBackground` | Remove raster/SVG background | process-image response |
| `POST /images/crispUpscale` | Structure-preserving raster upscale | process-image response |
| `POST /images/creativeUpscale` | Regenerative detail/face upscale | process-image response |
| `POST /images/eraseRegion` | Erase white mask regions | process-image response |
| `POST /images/variateImage` | Promptless remix to a target size | generation response |
| `POST /images/explore` | Produce a diverse exploration set | generation response |
| `POST /images/explore/similar` | Continue from an Explore `image_id` | generation response |
| `POST /prompts/enhance` | Expand a prompt, max 2,000 characters | `{"enhanced_prompt":...,"credits":...}` |
| `GET /users/me` | Account identity and unit balance | user object with `credits` |

The official Swagger also lists style/model discovery and style deletion routes. Because the human guide does not fully describe every schema, treat `GET /styles`, `GET /styles/basic`, `GET /styles/{style_id}`, `DELETE /styles/{style_id}`, and `GET /models` as **Swagger-documented** and feature-detect them before production use.

### Generation request

The JSON body for `/images/generations` uses:

| Field | Contract |
|---|---|
| `prompt` | required string; max 10,000 characters for V4/V4.1, 1,000 for V2/V3 |
| `model` | one public model ID above; default `recraftv4_1` |
| `n` | integer `1..6`; billed per image |
| `size` | supported `WxH` or aspect `w:h`; if omitted, selected from prompt |
| `random_seed` | optional unsigned integer; record it for repeat attempts |
| `response_format` | `url` (default) or `b64_json` |
| `style` / `style_id` | V2/V3 only; never both |
| `negative_prompt` | V2/V3 only |
| `text_layout` | V3/V3 Vector only |
| `controls` | palette/background on all documented families; `artistic_level` and `no_text` on V3 only |

**Swagger-documented, guide-light:** `image_format` is `png` or `webp` for raster responses. Vector models return SVG. Do not assume Studio export formats such as JPG, PDF, TIFF, or Lottie are valid API `image_format` values.

An `Image` can contain `image_id`, `url` or `b64_json`, `revised_prompt`, and optional feature data. Validate that the expected payload field exists before decoding or downloading.

### Sizes

**Documented:** accepted aspect ratios across families are `1:1`, `2:1`, `1:2`, `3:2`, `2:3`, `4:3`, `3:4`, `5:4`, `4:5`, `6:10`, `14:10`, `10:14`, `16:9`, and `9:16`.

Standard V4/V4.1 raster examples include `1024x1024`, `1536x768`, `768x1536`, `1280x832`, `832x1280`, `1216x896`, `896x1216`, `1152x896`, `896x1152`, `832x1344`, `1280x896`, `896x1280`, `1344x768`, and `768x1344`. Corresponding Pro dimensions are doubled per axis, including `2048x2048`, `3072x1536`, and `2688x1536`.

V2/V3 raster use a different explicit table: for example `1024x1024`, `2048x1024`, `1024x2048`, `1536x1024`, `1024x1536`, `1820x1024`, and `1024x1820`. Vector models accept the documented aspect tokens rather than a pixel-size guarantee. Recheck the Appendix instead of synthesizing arbitrary dimensions.

### Image inputs and masks

Image-taking endpoints accept either:

- `multipart/form-data` with `image`, `mask`, or `file`; or
- `application/json` with the corresponding `image_url` and `mask_url`, using a public URL or a `data:image/...;base64,...` data URL.

For current transform routes, input images are generally PNG/JPG/WEBP or SVG, no more than 10 MB, no more than 16 MP, maximum dimension 4096 px, and minimum dimension 256 px. Check the specific operation: erasing and utility endpoints have differing constraints.

For inpaint/generate-background masks:

- match the source dimensions exactly;
- use grayscale PNG/JPG/WEBP;
- use pure white (`255`) where content changes and pure black (`0`) where it remains;
- reject antialiasing and unintended gray pixels before upload.

### Transform requests

`/images/imageToImage` requires `image`/`image_url`, `prompt`, and `strength` in `[0,1]`; `0` means almost identical and `1` means minimal similarity. It also accepts `n` `1..6`, model, seed, response format, and model-compatible controls.

`/images/inpaint` requires image, mask, and prompt. `/images/generateBackground` uses the same input pattern. `/images/replaceBackground` requires image and prompt.

`/images/outpaint` requires image and prompt plus at least one of:

- `size`; or
- one or more of `expand_left`, `expand_right`, `expand_top`, `expand_bottom` in `0..4096`; or
- `zoom_out_percentage` in `[0,100)`.

Do not combine `size` with `expand_*`. `zoom_out_percentage` may accompany either. Final dimensions must not exceed 4096 px per side.

`/images/variateImage` requires image and `size`, accepts `n` `1..6`, model, seed, and response format, and does not accept a prompt.

### Vectorization and background removal

`/images/vectorize` accepts `file` or `image_url` and returns an SVG image. **Swagger-documented, guide-light** vectorization options include `svg_compression`, `limit_num_shapes`, `max_num_shapes`, color reduction, gradient return, shape stacking, small-shape filtering, and `strict_color_palette`. Because the guide does not publish all enums and interactions, omit them unless the current Swagger schema has been validated in a cheap test.

`/images/removeBackground` accepts raster or SVG. Raster input returns raster; SVG input returns SVG. Do not promise clean editable topology merely because background removal preserved SVG format.

### Sync, batch, and error behavior

- **Documented public contract:** endpoint calls return the finished response synchronously. `n=1..6` is the documented multi-image request mechanism.
- **Marketing-only statement:** Recraft's API landing page advertises asynchronous jobs, batch generation, and priority inference. At verification time, neither the public endpoint guide nor published Swagger exposed a job-submit, poll, cancel, webhook, signature, or priority schema. Do not invent one. Obtain the enterprise contract from Recraft before implementing these claims.
- **Documented rates:** 100 images per minute per user and 5 requests per second in the Appendix; API terms separately say 100 requests per minute. Enforce both image and request budgets, and expect account-specific adjustment.
- **Undocumented detail:** the public reference does not publish a stable error body or complete status-code table. Treat any non-2xx as failure; capture status, response body, response headers, and `X-Recraft-Requestid`; honor `Retry-After` if present. Retry 429 and a connect failure proven to occur before request transmission with bounded backoff/jitter. Treat read/post-submit timeouts, connection loss after transmission, and 5xx outcomes as potentially billable/ambiguous: park and reconcile them in the local ledger or with Recraft support/contract before resubmitting. Do not retry validation/auth/payment failures blindly.
- Use an idempotency ledger keyed by your job ID, prompt hash, model, seed, and intended count. Recraft does not document an idempotency-key header, so a timeout after submission can represent a billable ambiguous outcome.

## Direct design control

### Prompt as an art-direction spec

For V4/V4.1, write one coherent specification in this order:

1. deliverable and subject;
2. composition and hierarchy;
3. material, lighting, and rendering language;
4. exact text in quotation marks and its role;
5. palette and background relationship;
6. constraints stated positively;
7. intended use and crop-safe zones.

Avoid long synonym piles. Specify relationships: “single centered lockup,” “headline occupies upper third,” “three objects, evenly spaced,” “flat fills, no gradients,” “camera square to package.”

### Palette and brand consistency

**Documented:** `controls.colors` is an array of objects containing required `rgb: [r,g,b]` and optional `weight` in `0..1`; the sum of color weights must not exceed `1`. `controls.background_color` uses the same color object. These controls are preferences, not pixel-lock guarantees.

**Production heuristic:** Convert approved brand hex values to RGB in code, assign dominant weights only when necessary, and reserve unallocated weight for neutrals. Validate sampled output colors after generation. For exact logos or regulated colors, generate the surrounding design and composite the approved vector/logo/color in deterministic design software.

### Styles and substyles

**Documented:** V3 curated styles include raster categories such as `Photorealism`, `Illustration`, and `Recraft V3 Raw`, and vector categories such as `Vector art`, `Line art`, and `Engraving`. V2 has additional legacy effects. Use the live style list because names and access can change.

**Swagger-documented, guide-light:** requests may expose `substyle`, and the OpenAPI carries a large enum. The human API guide organizes these as named styles instead of promising every raw enum/model combination. Prefer a listed `style` or accessible `style_id`; use raw `substyle` only after discovery and a validation request.

To create a V3 custom style, `POST /styles` with one of the documented base types (`any`, `realistic_image`, `digital_illustration`, `vector_illustration`, `icon`, `logo_raster`) and up to five PNG/JPG/WEBP references. The human guide limits the reference set to 5 MB total and each upload to the current upload limit. It also documents optional model, image weights, source style IDs/weights, prompt, and `mix_policy` of `PaletteMatch` or `MaxWeight`.

Use only references you are allowed to upload and transform. A custom style is not a license to copy protected artwork or impersonate a living artist.

### Text and layout

For V4/V4.1, put short exact copy in quotation marks and describe hierarchy/placement. For long legal copy or pixel-exact typography, generate the visual substrate and typeset deterministically afterward.

V3 `text_layout` accepts one object per **single word**:

```json
{
  "text": "RECRAFT",
  "bbox": [[0.20, 0.40], [0.80, 0.40], [0.80, 0.56], [0.20, 0.56]]
}
```

The bounding box is exactly four `[x,y]` points in relative coordinates, with `(0,0)` top-left and `(1,1)` bottom-right; coordinates may extend beyond that range and be cropped. The API publishes a restricted character set. Validate every character before sending. Do not send spaces inside one `text` item; represent each word separately.

### Exploration and repeatability

Use `random_seed` to make a generation attempt reproducible, but do not treat seed/model labels as an archival guarantee across backend changes. Save output bytes, request JSON, model ID, seed, time, response IDs, credits, and a content hash.

Use `/images/explore` only with supported V4/V4.1 expressive and Pro models. It returns a set for visual discovery. `/images/explore/similar` requires an `image_id` from Explore and similarity `1..5`. Exploration can require temporary server-side artifacts; do not use it for sensitive material without confirming retention.

## Production workflow

1. **Preflight:** verify token, API-unit balance via `/users/me`, rights, output type, current model compatibility, rate budget, and official host.
2. **Probe:** generate `n=1` at standard resolution. Save request/response and asset immediately.
3. **Review direction:** check brief, composition, copy, palette, anatomy, brand risk, and unwanted content before multiplying spend.
4. **Iterate one variable:** change prompt, model, seed, palette, or operation—not all at once. Record the reason.
5. **Promote:** use Pro only after direction approval; keep the same aspect and art direction.
6. **Finish:** download URLs immediately, validate MIME/signature and dimensions or parse SVG safely, hash, scan, and store in controlled storage.
7. **QA:** review at intended display size and at 100%; test SVG editability, clipping, transparency, and small-size legibility.
8. **Deliver provenance:** retain prompt, model, seed, timestamp, Recraft request/image IDs, source permissions, edits, and disclosure decision.

### Raster QA

- correct subject count and geometry;
- coherent lighting/reflections/materials;
- exact required copy and no stray text;
- no clipped hero elements; crop-safe composition;
- intended palette, contrast, and transparent/background behavior;
- no face/hand/product defects at final size;
- actual dimensions, file signature, alpha, and color profile checked.

### Vector QA

- valid SVG parsed with scripts/external references disabled;
- no embedded raster unless explicitly accepted;
- sensible path count, grouping, fills, strokes, and viewBox;
- no accidental clipping, open seams, microscopic debris, or excessive nodes;
- text converted/handled according to downstream editing needs;
- flat-color and gradient requirements met;
- legible at favicon/icon size and clean at large scale.

## Complete examples

All examples are examples, not mandatory formulas. They assume `curl`, Python 3, `Pillow`, `defusedxml`, and an environment variable named `RECRAFT_API_TOKEN`.

### Example 1 — V4.1 brand-controlled raster, safe durable download

Intent: create one 16:9 campaign key visual with a restrained brand palette. V4.1 styles are expressed in the prompt; `controls` supplies color preferences.

```bash
set -euo pipefail
: "${RECRAFT_API_TOKEN:?Set RECRAFT_API_TOKEN}"

curl --fail-with-body --silent --show-error \
  --connect-timeout 15 --max-time 180 --max-filesize 5000000 --remove-on-error \
  --dump-header response.headers \
  'https://external.api.recraft.ai/v1/images/generations/raster' \
  -H "Authorization: Bearer ${RECRAFT_API_TOKEN}" \
  -H 'Content-Type: application/json' \
  -o response.json \
  --data-binary @- <<'JSON'
{
  "prompt": "Editorial launch key visual for a precision ceramic travel mug, one mug centered slightly right with open copy space in the left third, camera square to product, soft directional daylight, tactile matte ceramic and brushed steel, calm premium composition, deep navy background with a restrained coral accent, no logos, no embedded words, no extra products, 16:9 crop-safe layout",
  "model": "recraftv4_1",
  "n": 1,
  "size": "16:9",
  "random_seed": 284771,
  "response_format": "url",
  "image_format": "png",
  "controls": {
    "colors": [
      {"rgb": [10, 31, 68], "weight": 0.55},
      {"rgb": [242, 101, 91], "weight": 0.20}
    ],
    "background_color": {"rgb": [10, 31, 68]}
  }
}
JSON

python - <<'PY'
import hashlib, io, json, pathlib, urllib.error, urllib.parse, urllib.request, warnings
from datetime import datetime, timezone
from PIL import Image

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def open_https_without_auth(url, max_redirects=3):
    opener = urllib.request.build_opener(NoRedirect)
    current = url
    for _ in range(max_redirects + 1):
        parsed = urllib.parse.urlparse(current)
        if parsed.scheme != "https" or not parsed.hostname:
            raise SystemExit("Refusing non-HTTPS asset redirect")
        req = urllib.request.Request(current, headers={"User-Agent": "recraft-production-download/1"})
        try:
            return opener.open(req, timeout=120)
        except urllib.error.HTTPError as exc:
            if exc.code not in {301, 302, 303, 307, 308} or not exc.headers.get("Location"):
                raise
            current = urllib.parse.urljoin(current, exc.headers["Location"])
    raise SystemExit("Too many asset redirects")

r = json.loads(pathlib.Path("response.json").read_text(encoding="utf-8"))
item = r["data"][0]
url = item["url"]
u = urllib.parse.urlparse(url)
if u.scheme != "https" or not u.hostname:
    raise SystemExit("Refusing non-HTTPS asset URL")
with open_https_without_auth(url) as src:
    content_type = src.headers.get_content_type()
    body = src.read(50 * 1024 * 1024 + 1)
if len(body) > 50 * 1024 * 1024 or content_type != "image/png":
    raise SystemExit(f"Unexpected asset: {content_type}, {len(body)} bytes")
if not body.startswith(b"\x89PNG\r\n\x1a\n"):
    raise SystemExit("File signature does not match requested PNG")
warnings.simplefilter("error", Image.DecompressionBombWarning)
with Image.open(io.BytesIO(body)) as decoded:
    actual_size = decoded.size
    if actual_size != (1344, 768):
        raise SystemExit(f"Expected 1344x768 for standard 16:9, decoded {actual_size}")
    decoded.verify()
output = pathlib.Path("campaign-key-visual.png")
temporary = output.with_suffix(".png.tmp")
temporary.write_bytes(body)
temporary.replace(output)
pathlib.Path("campaign-key-visual.metadata.json").write_text(json.dumps({
    "submitted_request": {
        "prompt": "Editorial launch key visual for a precision ceramic travel mug, one mug centered slightly right with open copy space in the left third, camera square to product, soft directional daylight, tactile matte ceramic and brushed steel, calm premium composition, deep navy background with a restrained coral accent, no logos, no embedded words, no extra products, 16:9 crop-safe layout",
        "model": "recraftv4_1", "n": 1, "size": "16:9",
        "random_seed": 284771, "response_format": "url", "image_format": "png",
        "controls": {"colors": [{"rgb": [10, 31, 68], "weight": 0.55},
                                  {"rgb": [242, 101, 91], "weight": 0.20}],
                     "background_color": {"rgb": [10, 31, 68]}},
    },
    "response": r,
    "response_headers": pathlib.Path("response.headers").read_text(encoding="iso-8859-1"),
    "saved_utc": datetime.now(timezone.utc).isoformat(),
    "image_id": item.get("image_id"),
    "credits": r.get("credits"), "actual_size": actual_size,
    "sha256": hashlib.sha256(body).hexdigest(),
}, indent=2), encoding="utf-8")
PY
```

Expected result: one standard-resolution raster with navy-dominant art direction and left-side copy space. Likely failures: mug/logo hallucinations, insufficient empty space, or palette drift. Repair the prompt or seed before using Pro.

Variation: after approval, switch the model to `recraftv4_1_pro`, keep the aspect/prompt/controls stable, and update the local expected-size assertion from `(1344, 768)` to the documented Pro 16:9 size `(2688, 1536)`.

### Example 2 — native SVG logo exploration with base64 response

Intent: generate editable flat vector geometry without relying on an expiring URL.

```bash
set -euo pipefail
: "${RECRAFT_API_TOKEN:?Set RECRAFT_API_TOKEN}"

curl --fail-with-body --silent --show-error \
  --connect-timeout 15 --max-time 180 --max-filesize 30000000 --remove-on-error \
  --dump-header vector-response.headers \
  'https://external.api.recraft.ai/v1/images/generations/vector' \
  -H "Authorization: Bearer ${RECRAFT_API_TOKEN}" \
  -H 'Content-Type: application/json' \
  -o vector-response.json \
  -d '{
    "prompt": "Single centered symbol for a neighborhood seed library: an open seed pod forming a subtle letter S through negative space, flat vector geometry, two solid colors, bold silhouette, no gradients, no shadows, no mockup, no secondary symbols, no words, legible at 24 pixels",
    "model": "recraftv4_1_vector",
    "n": 1,
    "size": "1:1",
    "random_seed": 99214,
    "response_format": "b64_json",
    "controls": {"colors": [{"rgb": [20, 84, 63], "weight": 0.55}, {"rgb": [244, 184, 65], "weight": 0.30}]}
  }'

python - <<'PY'
import base64, hashlib, json, pathlib, re
from datetime import datetime, timezone
from defusedxml import ElementTree as ET

response_path = pathlib.Path("vector-response.json")
if response_path.stat().st_size > 30_000_000:
    raise SystemExit("Vector response exceeded transport cap")
r = json.loads(response_path.read_text(encoding="utf-8"))
raw = base64.b64decode(r["data"][0]["b64_json"], validate=True)
if len(raw) > 20 * 1024 * 1024 or b"<svg" not in raw[:4096].lower():
    raise SystemExit("Response is not a plausible SVG")
root = ET.fromstring(raw)
if root.tag.startswith("{"):
    namespace, local_root = root.tag[1:].split("}", 1)
else:
    namespace, local_root = "", root.tag
if local_root.lower() != "svg" or namespace not in {"", "http://www.w3.org/2000/svg"}:
    raise SystemExit("Root element is not SVG")
without_declaration = re.sub(br"^\s*<\?xml[^?]*\?>", b"", raw, count=1, flags=re.I)
if b"<?" in without_declaration:
    raise SystemExit("SVG contains a processing instruction")
allowed_tags = {
    "svg", "g", "defs", "title", "desc", "path", "rect", "circle", "ellipse",
    "line", "polyline", "polygon", "lineargradient", "radialgradient", "stop",
    "clippath", "mask",
}
allowed_attributes = {
    "id", "class", "viewbox", "width", "height", "x", "y", "x1", "y1", "x2", "y2",
    "cx", "cy", "r", "rx", "ry", "d", "points", "fill", "fill-opacity", "fill-rule",
    "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit",
    "stroke-dasharray", "stroke-dashoffset", "stroke-opacity", "opacity", "transform",
    "clip-path", "mask", "gradientunits", "gradienttransform", "spreadmethod", "offset",
    "stop-color", "stop-opacity", "preserveaspectratio", "href",
}
for element in root.iter():
    local_tag = element.tag.rsplit("}", 1)[-1].lower()
    if local_tag not in allowed_tags:
        raise SystemExit(f"SVG element is outside the passive allowlist: {local_tag}")
    for name, value in element.attrib.items():
        local_name = name.rsplit("}", 1)[-1].lower()
        lowered = value.strip().lower()
        if local_name.startswith("on") or local_name not in allowed_attributes:
            raise SystemExit(f"SVG attribute is outside the passive allowlist: {local_name}")
        if local_name == "href" and lowered and not lowered.startswith("#"):
            raise SystemExit("SVG contains an external/data reference")
        if "url(" in lowered and not re.search(r"url\(\s*['\"]?#", lowered):
            raise SystemExit("SVG contains a URL-based paint/reference")
        if "javascript:" in lowered or "data:" in lowered or "@import" in lowered:
            raise SystemExit("SVG contains active or embedded content")
output = pathlib.Path("seed-library-mark.svg")
temporary = output.with_suffix(".svg.tmp")
temporary.write_bytes(raw)
temporary.replace(output)
pathlib.Path("seed-library-mark.metadata.json").write_text(json.dumps({
    "submitted_request": {
        "prompt": "Single centered symbol for a neighborhood seed library: an open seed pod forming a subtle letter S through negative space, flat vector geometry, two solid colors, bold silhouette, no gradients, no shadows, no mockup, no secondary symbols, no words, legible at 24 pixels",
        "model": "recraftv4_1_vector", "n": 1, "size": "1:1",
        "random_seed": 99214, "response_format": "b64_json",
        "controls": {"colors": [{"rgb": [20, 84, 63], "weight": 0.55},
                                  {"rgb": [244, 184, 65], "weight": 0.30}]},
    },
    "response": r,
    "response_headers": pathlib.Path("vector-response.headers").read_text(encoding="iso-8859-1"),
    "saved_utc": datetime.now(timezone.utc).isoformat(),
    "image_id": r["data"][0].get("image_id"), "credits": r.get("credits"),
    "sha256": hashlib.sha256(raw).hexdigest(),
}, indent=2), encoding="utf-8")
PY
```

Expected result: SVG containing a compact two-color mark. Likely failures: embedded unwanted text, excessive nodes, or weak 24 px silhouette. Inspect and simplify in a vector editor; do not claim trademark clearance from generation.

### Example 3 — V3 masked inpaint with strict mask semantics

Intent: replace only a selected product-label region while preserving the rest of a raster photograph.

Inputs: `product.png` and an exactly matching binary `mask.png` where the label area is white and everything else black.

```bash
set -euo pipefail
: "${RECRAFT_API_TOKEN:?Set RECRAFT_API_TOKEN}"

python - <<'PY'
import pathlib
from PIL import Image
for name in ("product.png", "mask.png"):
    path = pathlib.Path(name)
    if path.stat().st_size > 10 * 1024 * 1024:
        raise SystemExit(f"{name} exceeds 10 MB")
    with Image.open(path) as check:
        width, height = check.size
        if min(width, height) < 256 or max(width, height) > 4096 or width * height > 16_000_000:
            raise SystemExit(f"{name} is outside the documented dimension/pixel bounds")
        check.verify()
        if check.format != "PNG":
            raise SystemExit(f"{name} must actually be PNG for the declared MIME type")
with Image.open("product.png") as im, Image.open("mask.png") as mask_source:
    if mask_source.mode not in {"1", "L"}:
        raise SystemExit("The uploaded mask bytes must already be binary/grayscale")
    mask = mask_source.convert("L")
    if im.size != mask.size:
        raise SystemExit("Mask dimensions must equal source dimensions")
    if set(mask.getdata()) - {0, 255}:
        raise SystemExit("Mask must contain only pure black and white pixels")
PY

curl --fail-with-body --silent --show-error \
  --connect-timeout 15 --max-time 180 --max-filesize 70000000 --remove-on-error \
  --dump-header inpaint-response.headers \
  'https://external.api.recraft.ai/v1/images/inpaint' \
  -H "Authorization: Bearer ${RECRAFT_API_TOKEN}" \
  -F 'image=@product.png;type=image/png' \
  -F 'mask=@mask.png;type=image/png' \
  -F 'prompt=Minimal cream paper label with a small centered green leaf emblem, matching the existing bottle curvature, lighting, grain, and perspective; no readable words' \
  -F 'model=recraftv3' \
  -F 'n=1' \
  -F 'random_seed=44102' \
  -F 'response_format=b64_json' \
  -o inpaint-response.json

python - <<'PY'
import base64, hashlib, io, json, pathlib, warnings
from datetime import datetime, timezone
from PIL import Image
response_path = pathlib.Path("inpaint-response.json")
if response_path.stat().st_size > 70_000_000:
    raise SystemExit("Inpaint response exceeded transport cap")
r = json.loads(response_path.read_text(encoding="utf-8"))
raw = base64.b64decode(r["data"][0]["b64_json"], validate=True)
if len(raw) > 50 * 1024 * 1024:
    raise SystemExit("Inpaint output exceeds local 50 MiB safety limit")
if raw.startswith(b"\x89PNG\r\n\x1a\n"):
    suffix = ".png"
elif raw.startswith(b"RIFF") and raw[8:12] == b"WEBP":
    suffix = ".webp"
else:
    raise SystemExit("Unexpected inpaint output signature")
warnings.simplefilter("error", Image.DecompressionBombWarning)
with Image.open("product.png") as source:
    expected_size = source.size
with Image.open(io.BytesIO(raw)) as decoded:
    actual_size = decoded.size
    if (max(actual_size) > 4096 or actual_size[0] * actual_size[1] > 16_000_000
            or actual_size != expected_size):
        raise SystemExit(f"Unexpected inpaint dimensions: {actual_size}; expected {expected_size}")
    decoded.verify()
output = pathlib.Path("product-inpaint" + suffix)
temporary = output.with_suffix(output.suffix + ".tmp")
temporary.write_bytes(raw)
temporary.replace(output)
pathlib.Path("product-inpaint.metadata.json").write_text(json.dumps({
    "submitted_request": {
        "prompt": "Minimal cream paper label with a small centered green leaf emblem, matching the existing bottle curvature, lighting, grain, and perspective; no readable words",
        "model": "recraftv3", "n": 1, "random_seed": 44102,
        "response_format": "b64_json",
    },
    "input_sha256": {name: hashlib.sha256(pathlib.Path(name).read_bytes()).hexdigest()
                     for name in ("product.png", "mask.png")},
    "response": r,
    "response_headers": pathlib.Path("inpaint-response.headers").read_text(encoding="iso-8859-1"),
    "saved_utc": datetime.now(timezone.utc).isoformat(),
    "image_id": r["data"][0].get("image_id"), "credits": r.get("credits"),
    "actual_size": actual_size, "sha256": hashlib.sha256(raw).hexdigest(),
}, indent=2), encoding="utf-8")
PY
```

This example uses Pillow only to validate the mask. Expected result: the selected label changes; unmasked regions remain substantially stable. Likely failures: mask seam, lighting mismatch, or unwanted text. Feathering is not represented by gray mask pixels because the API requires binary values; adjust the selection geometry and regenerate.

## Migration and fallback discipline

When moving an older integration to V4.1:

1. snapshot approved V2/V3 outputs and request metadata;
2. inventory every used field and route;
3. separate generation from V3-only style, negative prompt, text-layout, artistic-level, and localized-edit dependencies;
4. migrate plain text-to-image to `recraftv4_1` or Utility at standard resolution;
5. translate style intent into the prompt and retain palette controls;
6. run a fixed brief suite across old/new models and score composition, copy, palette, defects, and cost;
7. keep V3 calls for required V3-only operations instead of silently dropping controls;
8. promote to Pro only where resolution materially improves acceptance;
9. version the model and request schema in the asset manifest;
10. monitor the first-party changelog/docs and rerun the suite before changing defaults.

Do not silently substitute raster for vector, standard for Pro, expressive for Utility, image-to-image for inpaint, or Studio mockups for an API route. Surface the changed deliverable and obtain approval.

## Safety, privacy, rights, and provenance

**Documented legal terms, verified 2026-07-09:** API customers own Assets created through the API and Recraft assigns any copyright rights it may have for personal or commercial use, subject to compliance and a strict prohibition on using Assets to train AI models/systems/networks. Recraft's API-specific trust statement says API inputs and outputs are never used for model training; the API terms separately allow handling as needed for customer support, legal compliance, and policy enforcement. Keep that API override distinct from the general Studio training/opt-out regime. The general free-plan rule is also different: Free Tier Studio assets are Recraft-owned, public, personal-use only, and non-commercial. Do not apply Studio free-plan terms to paid API output or vice versa.

Ownership from Recraft is not third-party clearance. The customer remains responsible for rights in inputs and uses, including copyright, trademark, privacy, publicity, and consent. Do not generate deceptive impersonation, identifying personal data, abusive/illegal content, child exploitation, non-consensual intimate imagery, harmful disinformation, terrorist support, or protected-class violence. Apply human/legal review to people, trademarks, regulated claims, political persuasion, and high-stakes uses.

**Documented privacy/retention:** first-party pages are not perfectly aligned. API terms say Recraft does not store API images/metadata beyond delivery by default, while the API Appendix and trust documentation say generated results are stored/deleted within approximately 24 hours. Exploration/iterative features may retain artifacts temporarily and optional retention settings can extend storage. Operate to the conservative rule: assume processing and signed-link availability for up to about 24 hours, download immediately, never treat Recraft URLs as private storage, and ask Recraft for contractual clarification before sensitive workloads.

**Documented:** URL outputs are publicly accessible without authentication to anyone possessing the cryptographically signed URL. Never put secrets, confidential unreleased designs, biometric data, or unnecessary personal data into prompts/images. Prefer `b64_json` when link exposure is unacceptable, while recognizing the provider still processes the content.

**Documented provenance terms:** Recraft may embed machine-readable metadata, watermarks, or provenance information. Do not remove or alter Recraft-applied provenance unless expressly permitted by law. The user is responsible for legally required AI disclosures. Recraft does not publicly promise C2PA on every API output; inspect actual assets and maintain an independent provenance record.

## Cost and access snapshot

**Documented API pricing, verified 2026-07-09:** API units are prepaid at 1,000 units per USD $1 and do not expire; packages are non-cancellable/non-refundable. Current per-output charges include:

| Operation | USD / units |
|---|---:|
| V4.1 or V4.1 Utility raster | $0.035 / 35 |
| V4.1 Pro or Utility Pro raster | $0.21 / 210 |
| V4 raster / V4 Pro raster | $0.04 / 40; $0.25 / 250 |
| V3 raster / V2 raster | $0.04 / 40; $0.022 / 22 |
| V4.1/V4 standard vector | $0.08 / 80 |
| V4.1/V4 Pro vector | $0.30 / 300 |
| V3 vector / V2 vector | $0.08 / 80; $0.044 / 44 |
| V3 raster/vector image-to-image, inpaint, outpaint, background operations | $0.04 / 40; $0.08 / 80 per image |
| style creation | $0.04 / 40 per request |
| vectorize / remove background | $0.01 / 10 each |
| crisp upscale / creative upscale / erase / variate | $0.004 / 4; $0.25 / 250; $0.002 / 2; $0.04 / 40 |
| prompt enhancement | $0.01 / 10 |

The public API pricing page and general marketing pricing can briefly disagree during updates. Use the API pricing page and `/users/me` before a run. Compute expected units as operation cost times requested outputs, add a retry/ambiguity reserve, and stop when the budget is reached.

The current pricing table lists image-to-image pricing only for V3/V3 Vector and gives no Explore/Explore Similar charge, even though the endpoint guide exposes broader image-to-image model parameters and Explore routes. `/users/me` reports balance, not missing operation prices. Obtain written Recraft support/sales confirmation before budgeting V4/V4.1 image-to-image or Explore workloads.

## First-party sources

Verified 2026-07-09:

- API getting started and model IDs: https://www.recraft.ai/docs/api-reference/getting-started
- Endpoint guide and schemas: https://www.recraft.ai/docs/api-reference/endpoints
- Official examples: https://www.recraft.ai/docs/api-reference/examples
- Styles and compatibility: https://www.recraft.ai/docs/api-reference/styles
- Sizes, prompt limits, rates, and URL policy: https://www.recraft.ai/docs/api-reference/appendix
- API pricing: https://www.recraft.ai/docs/api-reference/pricing
- Official Swagger landing/specification: https://external.api.recraft.ai/doc/
- V4.1 family: https://www.recraft.ai/docs/recraft-models/recraft-v4-1
- Model selection: https://www.recraft.ai/docs/recraft-models/choosing-a-model
- Studio mockups (not an API route): https://www.recraft.ai/docs/recraft-studio/mockups/how-to-create-a-mockup
- Terms, API ownership, retention, provenance, and restrictions: https://www.recraft.ai/legal/terms
- Privacy policy: https://www.recraft.ai/legal/privacy
- API data use/training: https://www.recraft.ai/docs/trust-and-security/data-use-and-model-training
- Data protection and API deletion statement: https://www.recraft.ai/docs/trust-and-security/data-protection-and-privacy

## Explicitly unavailable or ambiguous facts

At verification time, first-party public materials did **not** provide:

- formal model deprecation dates or lifecycle guarantees;
- a public async/batch job, polling, cancellation, webhook, signature, or priority-inference schema despite marketing claims;
- a complete stable error-code/body contract;
- an idempotency-key guarantee;
- an SLA for generation latency or uptime in the public API guide;
- a public API endpoint for Studio mockup-layer warping/compositing;
- a universal provenance/C2PA guarantee for every API output;
- a single perfectly consistent default-retention statement across legal, Appendix, and trust pages.
- a reconciled V4.1 image-to-image compatibility statement between current endpoint prose and its model-parameter list;
- published V4/V4.1 image-to-image or Explore/Explore Similar operation pricing.

Do not fill these gaps with guessed fields or routes. Ask Recraft support/sales for a written contract where they are production requirements.
