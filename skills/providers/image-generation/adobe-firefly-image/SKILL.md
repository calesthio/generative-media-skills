---
name: adobe-firefly-image
description: Use Adobe Firefly Services to generate, edit, expand, fill, match, composite, and upscale still images through the current REST APIs. Apply when selecting Firefly Image 5 versus Image 3/4 or custom models, implementing authenticated asynchronous image workflows, using style or structure references, building product composites, handling provenance and enterprise rights, or diagnosing Firefly image jobs in production. Exclude Firefly video, audio, and unrelated Creative Cloud APIs.
---

# Adobe Firefly Image

Treat this as a still-image production and integration skill. Keep video, audio, and unrelated Photoshop, Lightroom, Express, or Creative Production operations out of scope unless the user explicitly asks to combine systems.

## Evidence discipline

Use these labels consistently:

- **Documented** means the current Adobe API reference, changelog, product terms, or security material states the claim.
- **Inference** means the conclusion follows from documented fields or behavior but Adobe does not state it directly.
- **Production heuristic** means practical guidance to test in the target account and workflow.

Volatile API facts below were verified on **2026-07-09**. Re-check the [API reference](https://developer.adobe.com/firefly-services/docs/firefly-api/api/), [changelog](https://developer.adobe.com/firefly-services/docs/firefly-api/getting-started/changelog/), and [usage notes](https://developer.adobe.com/firefly-services/docs/firefly-api/getting-started/usage-notes/) immediately before shipping. Adobe has several prose pages whose examples conflict with the endpoint reference. When they disagree, prefer the operation schema in the API reference plus a later explicit changelog entry; do not merge fields from incompatible versions.

## Start with the production contract

Before generating anything:

1. Confirm that the organization is entitled to Firefly Services and that the project has OAuth Server-to-Server credentials.
2. Record the deliverable, aspect ratio or dimensions, acceptable alteration of supplied assets, rights/consent status, locale, accessibility needs, and review owner.
3. Choose the operation from the matrix below. Do not select a model only because it is newest.
4. Quote the endpoint, model header, variation count, and cost unit before a paid batch.
5. Run one representative sample, download it immediately, and perform visual and provenance QA before scaling.

## Current API and model map

**Documented, verified 2026-07-09:**

| Need | Endpoint | Model selection | Key boundary |
|---|---|---|---|
| New Image 5 generation | `POST /v4/images/generate-async` | Header `x-model-version: image5`; body `modelId: firefly_image` | One variation per request; up to one reference image |
| Image 5 natural-language edit | Same v4 endpoint | Same header/body | A non-empty `referenceBlobs` array switches the operation to instruct edit |
| Image 3/4 generation and explicit controls | `POST /v3/images/generate-async` | `image3`, `image4_standard`, or `image4_ultra` | Up to four variations; style/structure controls live here |
| Custom-model generation | Same v3 endpoint | `image3_custom` or `image4_custom` plus `customModelId` | Custom model must be provisioned and shared with the app |
| Similar image | `POST /v3/images/generate-similar-async` | `image3`, `image4_standard`, or `image4_ultra` | Source image required |
| Masked replacement | `POST /v3/images/fill-async` | Operation schema, not Image 5 instruct-edit schema | Source and mask required |
| Canvas expansion/outpainting | `POST /v3/images/expand-async` | Operation schema | Source required; mask and placement are mutually constrained |
| Prompt-generated background around an object | `POST /v3/images/generate-object-composite-async` | Operation schema | Use when no background exists |
| Preserve an object precisely in an existing background | `POST /v3/images/precise-composite` | Precise composite pipeline | Existing background and placement mask required |
| Adapt an object into an existing background | `POST /v3/images/adaptive-composite` | Adaptive composite pipeline | May regenerate/adapt the object for realism |
| Fidelity-oriented upscale | `POST /v3/images/upscale` | `x-model-version: precise_upsampler_v1` | Factors 2, 3, 4, or 6; asynchronous |
| Upload input image or mask | `POST /v2/storage/image` | None | Returns an upload ID valid for seven days |

Image 5 is the latest documented image model and exposes 1 MP, 2.4 MP, and 4 MP resolution levels. The v3 model values remain present in the current API schema; do not call them removed merely because Image 5 exists. Adobe removed the deprecated synchronous v3 references on 2025-10-03 and removed Generate Images v2, Expand v1, and Fill v1 on 2025-09-10. Build only against current asynchronous routes. See the [changelog](https://developer.adobe.com/firefly-services/docs/firefly-api/getting-started/changelog/).

### Resolve documentation conflicts deliberately

**Documented conflict, verified 2026-07-09:** the Image 5 API reference defines `aspectRatio`, `resolutionLevel`, `modelId`, `modelSpecificPayload`, and `referenceBlobs` for `/v4/images/generate-async`. The [Image 5 migration page](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/how-tos/cm-generate-image/breaking-changes) simultaneously describes some of those fields as removed and presents a payload resembling the v3 custom-model schema. Do not use that migration table as executable schema without reconciling it against the API reference.

Likewise, a prose upscale guide still names `/v1/images/upsample-async`, while the current API reference and 2026-04-24 changelog identify `POST /v3/images/upscale` and `precise_upsampler_v1`. Use the latter. `creative_upsampler_v1` is rejected with 422. This is a source-quality decision, not a claim that every Adobe prose page is obsolete.

## Authenticate from a server

**Documented:** Firefly requests require both an Adobe IMS bearer token and the Client ID as `x-api-key`. Use OAuth Server-to-Server. Never expose the client secret or access token in browser code, logs, prompts, or generated artifacts. Adobe documents 24-hour access-token validity; refresh proactively and retry once after a 401 only after obtaining a fresh token. See [Authentication](https://developer.adobe.com/firefly-services/docs/firefly-api/getting-started/) and [credentials setup](https://developer.adobe.com/firefly-services/docs/guides/get-started).

Token request:

```http
POST https://ims-na1.adobelogin.com/ims/token/v3
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=...&client_secret=...&scope=openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis
```

Every Firefly API call then includes:

```http
Authorization: Bearer <access-token>
x-api-key: <client-id>
Content-Type: application/json
Accept: application/json
```

Use the scopes and product profiles actually provisioned in the Developer Console; do not broaden scopes speculatively. A 403 after successful token exchange usually points to entitlement, product-profile, organization, custom-model sharing, policy, or regional access rather than malformed OAuth.

## Understand request and response contracts

### Image 5: v4 generate and instruct edit

**Documented v4 fields:**

- `prompt`: required, 1–1500 characters.
- `aspectRatio`: `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, or `auto`.
- `resolutionLevel`: `1MP`, `2.4MP` (default), or `4MP`.
- `modelId`: `firefly_image`.
- `numVariations`: maximum 1.
- `seeds`: maximum one integer; its count must match `numVariations` when both appear.
- `modelSpecificPayload.localeCode`: locale control used by Image 5.
- `modelSpecificPayload.prompt_reasoner`: `speed` (default) or `quality`; Adobe says `quality` populates `altText`, while `speed` returns it empty.
- `referenceBlobs`: maximum one. Empty means text-to-image; non-empty with `usage: general` means instruct edit. When present, omit `aspectRatio` or set it to `auto`.

Do not send v3-only `style`, `structure`, `contentClass`, `visualIntensity`, or `customModelId` fields to v4. The v4 operation schema does not document a negative-prompt field or arbitrary output-format selector. Validate the actual response asset `Content-Type` rather than assuming JPEG or PNG.

The v4 submission returns HTTP 200 with a `links.result.href`, `links.cancel.href`, and progress value. It is still asynchronous. Poll the returned result link with the same authorization headers until a terminal state, then download the image URL promptly.

### Image 3/4: v3 generate

**Documented v3 fields:**

- `prompt`: required, 1–1024 characters.
- `negativePrompt`: up to 1024 characters; not supported for Image 3 or Image 4 custom models.
- `contentClass`: `photo` or `art`.
- `numVariations`: 1–4. If seeds are supplied, seed count must equal variation count.
- `promptBiasingLocaleCode`: BCP-47-like language-region value such as `en-US`.
- `style.presets`: documented snake_case presets; combine deliberately.
- `style.strength`: 1–100, default 50; may accompany a style reference.
- `structure.strength`: 1–100, default 50; controls outline/depth resemblance to the structure reference.
- `visualIntensity`: 2–10; not supported by `image4_custom`.
- `upsamplerType`: only for `image4_custom`; `default` or `low_creativity`.

Supported generation sizes:

| Model | Exact documented sizes |
|---|---|
| Image 4 | `2048×2048`, `2304×1792`, `1792×2304`, `2688×1536`, `1440×2560` |
| Image 3 | `2048×2048`, `1024×1024`, `2304×1792`, `1792×2304`, `2688×1536`, `2688×1512`, `1344×768`, `1344×756`, `1152×896`, `896×1152` |

Do not round to a convenient aspect-equivalent size. The service validates exact pairs.

The v3 submission returns HTTP 202 with `jobId`, `statusUrl`, and `cancelUrl`. Poll `statusUrl`. A running response includes `status: running`; success includes `status: succeeded` and `result.outputs[]`, each with a seed and image URL. Treat `failed`, `cancelled`, HTTP terminal errors, and a local timeout as terminal outcomes; capture the response body and request ID for support.

### Uploads, masks, and source URLs

The upload API accepts binary image data. The current API reference lists PNG, JPEG, WebP, TIFF, and JXL with a 15 MB maximum, while an older upload guide lists only JPEG, PNG, and WebP. **Production heuristic:** use PNG for masks/transparency and JPEG or PNG for ordinary inputs unless the target account has been tested with the broader formats.

An upload response is shaped as `{"images":[{"id":"..."}]}`. The API contract says the ID is valid for seven days. Adobe's Firefly Services security sheet separately says uploaded reference content is cached for 24 hours; do not equate cache retention with ID validity.

For v3 source URLs, the operation reference commonly allow-lists `amazonaws.com`, `windows.net`, `dropboxusercontent.com`, and `storage.googleapis.com`. The Image 5 usage notes add `frontdoor.prod.azure.cxp.adobe.com`. Requirements vary by operation. Use short-lived HTTPS pre-signed URLs, restrict object permissions, and confirm the exact operation's allow-list. Never pass an arbitrary public URL and assume Firefly will fetch it.

Masks are production assets, not annotations. Inspect dimensions, alpha/gray semantics, inversion, feathering, and alignment before a paid call. `expand-async` forbids using `placement` for a source when a mask is also applied. Its output can be up to 3999×3999. Use Fill for a localized masked replacement; use Expand for a larger canvas; use Image 5 instruct edit for a natural-language whole-image refinement where one reference is sufficient.

## Choose references and composites by what must remain fixed

### Style and structure

Use v3 `style.imageReference` to transfer visual language such as palette, medium, lighting, or mood. Use `structure.imageReference` to guide outline and depth. Strength 1–100 changes adherence; default 50. These controls can coexist, but competing high strengths can reduce prompt compliance.

**Production heuristic:** sweep one control at a time—such as 30, 60, 90—using the same prompt and seed, then select by a written rubric. A seed is a reproducibility aid, not an archival guarantee across model, endpoint, or service updates. Adobe's seed guide says identical settings reproduce an image; still record the model header, endpoint, payload, and source hashes because lifecycle changes can invalidate cross-version assumptions.

Use only documented preset values from the [style preset catalog](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/concepts/style-presets/). Do not invent UI labels as API enum values. A few useful documented examples are `product_photo`, `studio_light`, `golden_hour`, `flat_design`, `watercolor`, `cinematic`, `bw`, and `shallow_depth_of_field`; this is not the complete catalog.

### Composite selection

- Use **Generate Object Composite** when the object exists but the background should be generated from a prompt. The request must provide an input that can be composited: a larger requested canvas, transparency, or a mask.
- Use **Precise Composite** when the supplied object's pixels or packaging details must remain exact. It uses background image + fill-area mask + object image. `blend` ranges 0–1; 0 is fully harmonized and 1 preserves the original object appearance. Up to three variations.
- Use **Adaptive Composite** when realism in an existing background is more important than pixel-exact object preservation. `harmonization` and `shadowIntensity` range 0–1; `preserveBackground` retains original background pixels while modifying the object region. Up to three variations.

All three are asynchronous. Do not promise that “precise” removes the need for a pixel-diff and label-legibility review. Do not use Adaptive Composite for regulated packaging or product claims unless alteration is acceptable and reviewed.

### Upscale

Use current `POST /v3/images/upscale` with `x-model-version: precise_upsampler_v1`, an input image source, one to four seeds, and `upscaleFactor` 2, 3, 4, or 6. Poll the returned `links.result.href`. The API reference describes output dimensions as input dimensions multiplied by the factor. Validate service limits and the actual result; a prose guide states a 6k maximum while the endpoint schema focuses on factors, so preflight large inputs instead of assuming every factor is accepted.

## Direct the image before writing prose

**Production heuristic:** express a prompt as a compact art-direction brief, not a pile of adjectives. Specify:

1. subject and action;
2. environment and era;
3. framing, viewpoint, lens language, or layout;
4. lighting and color relationships;
5. material and surface cues;
6. text that must be visible, quoted exactly, only when essential;
7. exclusions through the API's documented negative-prompt field when available.

Do not imitate a living artist or use third-party marks, faces, copyrighted characters, or reference assets without rights. For localization, set the API locale field and have a native reviewer check cultural details; locale bias is not translation or legal clearance.

For exact typography, logos, pack copy, QR codes, and compliance marks, generate a clean visual base and composite approved vector/raster artwork afterward. Treat model-rendered text as draft content. For a product, request negative space and camera geometry that accommodate the later overlay.

## Example 1 — complete Image 5 generation client

**Example, not a mandatory formula.** This Python 3.11+ standard-library program obtains a token, submits one Image 5 job, polls the returned result URL with bounded exponential backoff, downloads the first image, and records response metadata. Set `FIREFLY_SERVICES_CLIENT_ID` and `FIREFLY_SERVICES_CLIENT_SECRET` in a secure server environment.

```python
import json
import os
import random
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

CLIENT_ID = os.environ["FIREFLY_SERVICES_CLIENT_ID"]
CLIENT_SECRET = os.environ["FIREFLY_SERVICES_CLIENT_SECRET"]
TOKEN_URL = "https://ims-na1.adobelogin.com/ims/token/v3"
GENERATE_URL = "https://firefly-api.adobe.io/v4/images/generate-async"
SCOPES = "openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis"
MIN_API_INTERVAL = 15.0  # Default 4-RPM org entitlement; use a distributed limiter at scale.
_last_api_request = 0.0


def wait_for_org_quota():
    global _last_api_request
    delay = MIN_API_INTERVAL - (time.monotonic() - _last_api_request)
    if delay > 0:
        time.sleep(delay)
    _last_api_request = time.monotonic()


def retry_after_seconds(value, fallback):
    if not value:
        return fallback
    try:
        return max(0.0, float(value))
    except ValueError:
        when = parsedate_to_datetime(value)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return max(0.0, (when - datetime.now(timezone.utc)).total_seconds())


def request_json(url, *, method="GET", headers=None, body=None, attempts=5):
    data = None if body is None else json.dumps(body).encode("utf-8")
    for attempt in range(attempts):
        req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
        wait_for_org_quota()
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return response.status, dict(response.headers), json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            retryable = exc.code == 429 or 500 <= exc.code < 600
            if not retryable or attempt == attempts - 1:
                raise RuntimeError(f"HTTP {exc.code} from {url}: {detail}") from exc
            fallback = min(30, 2 ** attempt + random.random())
            time.sleep(max(MIN_API_INTERVAL, retry_after_seconds(exc.headers.get("Retry-After"), fallback)))
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == attempts - 1:
                raise RuntimeError(f"Network failure from {url}: {exc}") from exc
            time.sleep(max(MIN_API_INTERVAL, min(30, 2 ** attempt + random.random())))


def get_token():
    form = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPES,
    }).encode("utf-8")
    req = urllib.request.Request(
        TOKEN_URL,
        data=form,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)["access_token"]


def find_first_image_url(value):
    if isinstance(value, dict):
        image = value.get("image")
        if isinstance(image, dict) and isinstance(image.get("url"), str):
            return image["url"]
        for child in value.values():
            found = find_first_image_url(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_first_image_url(child)
            if found:
                return found
    return None


def main():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "x-api-key": CLIENT_ID,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-model-version": "image5",
    }
    payload = {
        "prompt": (
            "Editorial product photograph of a matte cobalt reusable bottle on pale limestone, "
            "three-quarter view, soft north-window light, restrained blue and warm-gray palette, "
            "clean negative space at upper left, realistic condensation, no logo or lettering"
        ),
        "aspectRatio": "4:3",
        "resolutionLevel": "4MP",
        "modelId": "firefly_image",
        "numVariations": 1,
        "seeds": [42345],
        "referenceBlobs": [],
        "modelSpecificPayload": {"localeCode": "en-US", "prompt_reasoner": "quality"},
    }
    status, response_headers, accepted = request_json(
        GENERATE_URL, method="POST", headers=headers, body=payload
    )
    result_url = accepted["links"]["result"]["href"]
    cancel_url = accepted["links"]["cancel"]["href"]
    deadline = time.monotonic() + 300
    final = accepted
    result_headers = {}
    while time.monotonic() < deadline:
        _, result_headers, final = request_json(result_url, headers=headers)
        state = str(final.get("status", "")).lower()
        if state in {"succeeded", "failed", "cancelled", "canceled"}:
            break
        if find_first_image_url(final):
            break
    else:
        cancel_result = None
        try:
            cancel_status, _, cancel_body = request_json(cancel_url, method="PUT", headers=headers)
            cancel_result = {"status": cancel_status, "body": cancel_body}
        except Exception as exc:
            cancel_result = {"error": str(exc)}
        Path("firefly-response.json").write_text(
            json.dumps({
                "request": payload,
                "accept_status": status,
                "accept_headers": response_headers,
                "accepted": accepted,
                "cancel_attempt": cancel_result,
            }, indent=2),
            encoding="utf-8",
        )
        raise TimeoutError("Firefly job did not finish within 300 seconds")

    if str(final.get("status", "")).lower() in {"failed", "cancelled", "canceled"}:
        raise RuntimeError(f"Firefly job ended unsuccessfully: {json.dumps(final)}")
    image_url = find_first_image_url(final)
    if not image_url:
        raise RuntimeError(f"No image URL in terminal response: {json.dumps(final)}")
    with urllib.request.urlopen(image_url, timeout=120) as image_response:
        content_type = image_response.headers.get_content_type()
        suffix = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}.get(
            content_type, ".bin"
        )
        Path("firefly-output" + suffix).write_bytes(image_response.read())
    Path("firefly-response.json").write_text(
        json.dumps({
            "request": payload,
            "accept_status": status,
            "accept_headers": response_headers,
            "accepted": accepted,
            "result_headers": result_headers,
            "result": final,
        }, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
```

Expected result: one 4:3 Image 5 asset, locally downloaded with its real media-type extension, plus an audit JSON. Likely failures: missing entitlement (403), a field from the v3 schema accidentally sent to v4 (422), organization throttling (429), expired token (401), or the output URL expiring before download.

Meaningful variations: switch `prompt_reasoner` to `speed` for latency testing; use `resolutionLevel: 1MP` for cheap preflight if the account rate card favors it; or supply one allowed `referenceBlobs` item, remove/auto the aspect ratio, and phrase the prompt as an edit instruction.

## Example 2 — upload and masked fill

**Example, not a mandatory formula.** This Python 3 program uploads a PNG source and mask, submits four seeded v3 fill variations, then polls the returned status URL. It assumes the source and mask share dimensions and the mask semantics have been verified visually.

```python
import json
import os
import random
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

CLIENT_ID = os.environ["FIREFLY_SERVICES_CLIENT_ID"]
TOKEN = os.environ["FIREFLY_SERVICES_ACCESS_TOKEN"]
BASE = "https://firefly-api.adobe.io"
AUTH = {"Authorization": f"Bearer {TOKEN}", "x-api-key": CLIENT_ID}
MIN_API_INTERVAL = 15.0  # Default 4-RPM org entitlement; replace with shared storage at scale.
_last_api_request = 0.0


def wait_for_org_quota():
    global _last_api_request
    delay = MIN_API_INTERVAL - (time.monotonic() - _last_api_request)
    if delay > 0:
        time.sleep(delay)
    _last_api_request = time.monotonic()


def retry_after_seconds(value, fallback):
    if not value:
        return fallback
    try:
        return max(0.0, float(value))
    except ValueError:
        when = parsedate_to_datetime(value)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return max(0.0, (when - datetime.now(timezone.utc)).total_seconds())


def open_bytes(req, *, attempts=5):
    for attempt in range(attempts):
        wait_for_org_quota()
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return response.status, dict(response.headers), response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            retryable = exc.code == 429 or 500 <= exc.code < 600
            if not retryable or attempt == attempts - 1:
                raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
            fallback = min(30, 2 ** attempt + random.random())
            time.sleep(max(MIN_API_INTERVAL, retry_after_seconds(exc.headers.get("Retry-After"), fallback)))
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == attempts - 1:
                raise RuntimeError(f"Network failure: {exc}") from exc
            time.sleep(max(MIN_API_INTERVAL, min(30, 2 ** attempt + random.random())))
    raise AssertionError("unreachable")


def upload_png(path):
    req = urllib.request.Request(
        f"{BASE}/v2/storage/image",
        data=Path(path).read_bytes(),
        method="POST",
        headers={**AUTH, "Content-Type": "image/png", "Accept": "application/json"},
    )
    _, _, raw = open_bytes(req)
    return json.loads(raw)["images"][0]["id"]


def json_request(url, *, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={**AUTH, "Content-Type": "application/json", "Accept": "application/json"},
    )
    _, _, raw = open_bytes(req)
    return json.loads(raw)


source_id = upload_png("source.png")
mask_id = upload_png("mask.png")
job = json_request(
    f"{BASE}/v3/images/fill-async",
    method="POST",
    payload={
        "image": {"source": {"uploadId": source_id}},
        "mask": {"source": {"uploadId": mask_id}, "invert": False},
        "prompt": (
            "replace only the masked vase with a handmade cobalt ceramic vase, "
            "preserve table and shadows"
        ),
        "negativePrompt": "lettering, logo, extra objects",
        "promptBiasingLocaleCode": "en-US",
        "numVariations": 4,
        "seeds": [101, 202, 303, 404],
        "size": {"width": 2048, "height": 2048},
    },
)
Path("fill-accepted.json").write_text(json.dumps(job, indent=2), encoding="utf-8")

deadline = time.monotonic() + 300
while time.monotonic() < deadline:
    result = json_request(job["statusUrl"])
    state = result.get("status", "")
    if state == "succeeded":
        Path("fill-result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        break
    if state in {"failed", "cancelled", "canceled"}:
        raise RuntimeError(json.dumps(result))
else:
    cancel_result = None
    try:
        cancel_result = json_request(job["cancelUrl"], method="PUT")
    except Exception as exc:
        cancel_result = {"error": str(exc)}
    Path("fill-accepted.json").write_text(
        json.dumps({"accepted": job, "cancel_attempt": cancel_result}, indent=2),
        encoding="utf-8",
    )
    raise TimeoutError("Fill job did not finish within 300 seconds")

outputs = result.get("result", {}).get("outputs", [])
if len(outputs) != 4:
    raise RuntimeError(f"Expected four outputs, received {len(outputs)}")
suffixes = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}
for index, output in enumerate(outputs, start=1):
    with urllib.request.urlopen(output["image"]["url"], timeout=120) as response:
        content_type = response.headers.get_content_type()
        suffix = suffixes.get(content_type)
        if suffix is None:
            raise RuntimeError(f"Unexpected output Content-Type: {content_type}")
        Path(f"fill-output-{index}{suffix}").write_bytes(response.read())
```

Expected result: four URLs and their seeds in `fill-result.json`, plus four locally downloaded image files. Likely failures: a source/mask dimension mismatch, inverted mask intent, unsupported size, seed-count mismatch, an unexpected delivery media type, or a prompt asking the fill endpoint to change unmasked pixels.

## Operate asynchronous jobs safely

1. Persist the submission response before polling.
2. Follow the returned `statusUrl` or `links.result.href`; do not reconstruct hostnames from a job ID.
3. Route uploads, submissions, and polls through one organization-wide limiter. At the default 4 RPM entitlement, average at least 15 seconds between all Firefly API requests across workers; use adaptive polling, honor `Retry-After`, and only poll faster when the organization's contracted limit supports it. Older one-second examples do not override the current usage notes.
4. Set a local deadline and expose cancellation. Current job cancellation is `PUT` to the returned cancel link.
5. Retry 429 and transient 5xx with jittered exponential backoff. Do not retry 400/403/413/415/422 unchanged.
6. Treat 401 as token refresh, then retry once. Repeated 401 is configuration failure.
7. Download outputs immediately to controlled storage; pre-signed URLs are delivery mechanisms, not durable asset management.
8. Store endpoint, model header, payload with secrets removed, seed, upload IDs, source hashes, job ID, Adobe request/correlation headers, output hash, media type, dimensions, and review status.

Common response meanings from the current reference:

| Status | Action |
|---|---|
| 400 | Fix malformed request; validate JSON and route |
| 401 | Refresh/verify bearer token |
| 403 | Check entitlement, product profile, organization, policy, custom-model access, and region |
| 404/410 | Treat job or temporary resource as unavailable/expired; do not loop |
| 408/499 | Request/client interruption; reconcile whether a job was accepted before resubmitting |
| 409 | Job state conflict, often cancel-after-terminal; fetch status |
| 413 | Reduce upload/request size |
| 415 | Correct `Content-Type` or image encoding |
| 422 | Fix field, enum, size, mask, seed count, model header, or incompatible schema |
| 429 | Honor `Retry-After`, back off, and apply organization-wide admission control |
| 451 | Stop and escalate legal/availability restriction; do not evade it |
| 500/503 | Retry with a cap; check Adobe status/support if persistent |

Never mutate a rejected prompt automatically to bypass safety filters. Present the failure category and ask for a compliant revision.

## Capacity, access, and cost

**Documented, verified 2026-07-09:** default Firefly API limits are **4 requests per minute and 9,000 requests per day per organization**. The daily limit becomes relevant when an account manager raises RPM without changing RPD. Higher limits require the account manager. Build a shared limiter across workers; polling also consumes requests unless the contract says otherwise. See [usage notes](https://developer.adobe.com/firefly-services/docs/firefly-api/getting-started/usage-notes/).

Firefly Services is an enterprise-provisioned offering. There is no universal public per-image price in the cited developer schema. Adobe meters API work in **Operations**; an API action or workflow may consume more than one Operation, and the applicable rate card is available in the Admin Console/contract. Do not fabricate dollar estimates. Query the organization's entitlement, rate card, included Operations, overage terms, model/feature availability, and regional restrictions before quoting a batch. See the [Shared Credit product description](https://helpx.adobe.com/legal/product-descriptions/shared-credits.html).

## Rights, safety, privacy, and provenance

### Inputs and outputs

Require rights to prompts, reference images, masks, people/likenesses, brands, custom-model training data, and intended distribution. Adobe's current 2026v2 enterprise API terms say inputs and outputs are Customer Content and warn that outputs may not be unique. They also restrict using Developer Tools or derived content/data/output to create, train, test, or improve AI systems, and restrict Customer Software to internal use unless the Sales Order expressly permits another use. This does not guarantee copyrightability, exclusivity, non-infringement, suitability, or permission for an external-facing integration. Review the current [Adobe Creative API product terms landing page](https://www.adobe.com/legal/terms/enterprise-licensing/cc-product-terms.html), [2026v2 PSLT](https://www.adobe.com/cc-shared/assets/pdf/legal/terms/enterprise/pdfs/pslt-adobecreativeapi-ww-2026v2.pdf), and the customer's Sales Order with counsel.

Adobe describes Firefly foundation-model training as using licensed content such as Adobe Stock and public-domain content, and says it does not train those models on customer/user content. The Firefly Services security sheet states that enterprise inputs/outputs are not included in foundation-model training, with limited exceptions for user-controlled feedback/improvement programs or features whose service is AI training. Present this as Adobe's documented policy, not an independently audited guarantee. See [Adobe's approach](https://www.adobe.com/ai/overview/firefly/gen-ai-approach.html) and the [Firefly Services security fact sheet](https://www.adobe.com/content/dam/cc/en/trust-center/ungated/whitepapers/creative-cloud/adobe-firefly-services-security-fact-sheet.pdf).

### Indemnification

Never say “Firefly outputs are indemnified” without qualifiers. Adobe's contractual Firefly Output IP indemnity applies only when specifically included in the Sales Order/qualifying offer, for listed Eligible Firefly Features and Surfaces, after the defined Export Event, and subject to exclusions, obligations, and liability caps in the controlling agreement. Current terms exclude, among other cases, claims arising from modification or combination of Firefly Output—directly relevant to compositing, re-encoding, or other post work. The product description lists Firefly APIs as a surface when a qualifying customer consumes Operations and downloads the output, but not every feature is necessarily eligible on every surface. Verify the current [Firefly product description](https://helpx.adobe.com/legal/product-descriptions/adobe-firefly.html), Sales Order, 2026v2 PSLT, eligible feature, export evidence, and downstream transformations. Escalate legal interpretation to counsel.

### Safety

Follow the current [Adobe Generative AI User Guidelines](https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html). They prohibit unlawful or harmful use, explicit sexual content, sexualized minors, hateful/dehumanizing content, glorified graphic violence, promotion of self-harm or violent extremism, harmful deception, privacy violations, noncompliant regulated activity, deceptive impersonation, and infringement of third-party rights. Adobe says prompts, inputs, and outputs may be reviewed automatically and manually for abuse prevention and filtering.

Add application-level consent, age, rights, privacy, impersonation, and regulated-use gates where relevant. Keep a human reviewer for public claims, news-like imagery, real-person depictions, children, health/finance/legal contexts, elections, and high-impact decisions. A successful API response is not a safety or rights clearance.

### Privacy and retention

**Documented enterprise service defaults in Adobe's security fact sheet:** Firefly generative API prompt text, configuration settings, and a pseudonymous user ID are retained for 90 days; reference content uploaded by API is cached for 24 hours; generated Firefly API images are stored for 24 hours and exposed through pre-signed URLs; a cryptographic hash and manifest information for Content Credentials may persist in the Content Credentials cloud. Confirm the current agreement and regional deployment because product surface and contract can alter handling.

Minimize personal/confidential data, use short-lived source URLs, avoid embedding secrets in prompts, download results to the customer's governed storage, and delete local staging copies according to policy. The public v4 request schema does not expose a client-controlled `storeInputs` switch; do not invent one.

### Content Credentials

Adobe says it automatically attaches Content Credentials to assets whose pixels are fully generated by Firefly, such as Text to Image. Credentials identify Adobe as issuer and add tamper-evident provenance about generative creation; they do not prove factual truth, ownership, consent, or safety. Preserve the original delivered file and its manifest. Do not strip provenance as a routine optimization. If a pipeline re-encodes, composites, or exports the asset, test whether credentials survive and create a new signed provenance record when the organization's tooling supports it. See Adobe's [Content Credentials overview](https://helpx.adobe.com/firefly/web/get-started/learn-the-basics/content-credentials-overview.html) and the primary [C2PA specification](https://c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html).

## Quality assurance gate

Reject or revise an asset when any applicable check fails:

- Prompt intent: subject, action, count, locale, and exclusions are satisfied.
- Composition: crop, safe areas, negative space, horizon, perspective, and target aspect are correct.
- Anatomy and geometry: hands, faces, reflections, shadows, repeated structures, and object contact are coherent.
- Product/brand: silhouette, proportions, color, material, labels, logos, and claims match approved reference; run pixel-diff where preservation is required.
- Edit isolation: compare unchanged regions; inspect mask seams, halos, texture repetition, and lighting transitions at 100% and 200%.
- Text: every character is legible and correct; otherwise replace in post.
- Technical: decode succeeds; media type, pixel dimensions, color profile, alpha, file size, and checksum meet the delivery contract.
- Accessibility: review generated `altText`; do not trust it merely because `prompt_reasoner: quality` populated it.
- Safety/rights: human review completed for relevant risks; references and likeness permissions are recorded.
- Provenance: original file and Content Credentials are retained or a documented transformation chain exists.
- Reproducibility: endpoint, model header, request, seeds, source hashes, job ID, and review decision are stored without secrets.

For a batch, define numeric acceptance thresholds before generation—for example zero label changes, no alteration outside a mask above a measured tolerance, exact dimensions, and a maximum manual-reject rate. Sample across prompts, locales, seeds, and reference types; do not approve a pipeline from one attractive hero image.

## Sources checked

All volatile facts were checked 2026-07-09 against first-party sources:

- [Firefly API reference](https://developer.adobe.com/firefly-services/docs/firefly-api/api/)
- [Firefly API changelog](https://developer.adobe.com/firefly-services/docs/firefly-api/getting-started/changelog/)
- [Technical usage notes and rate limits](https://developer.adobe.com/firefly-services/docs/firefly-api/getting-started/usage-notes/)
- [Authentication](https://developer.adobe.com/firefly-services/docs/firefly-api/getting-started/)
- [Using Image 5](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/how-tos/cm-generate-image/feature-guide)
- [Asynchronous API guide](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/how-tos/using-async-apis)
- [Image upload](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/concepts/image-upload/)
- [Style references](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/concepts/style-image-reference/), [structure references](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/concepts/structure-image-reference/), [style presets](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/concepts/style-presets/), and [seeds](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/concepts/seeds/)
- [Composite operations feature guide](https://developer.adobe.com/firefly-services/docs/firefly-api/guides/how-tos/object-composite/)
- [Firefly product description](https://helpx.adobe.com/legal/product-descriptions/adobe-firefly.html) and [Shared Credit product description](https://helpx.adobe.com/legal/product-descriptions/shared-credits.html)
- [Adobe Creative API product terms landing page](https://www.adobe.com/legal/terms/enterprise-licensing/cc-product-terms.html) and [2026v2 PSLT](https://www.adobe.com/cc-shared/assets/pdf/legal/terms/enterprise/pdfs/pslt-adobecreativeapi-ww-2026v2.pdf)
- [Firefly Services security fact sheet](https://www.adobe.com/content/dam/cc/en/trust-center/ungated/whitepapers/creative-cloud/adobe-firefly-services-security-fact-sheet.pdf)
- [Adobe Generative AI User Guidelines](https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html)
- [Content Credentials overview](https://helpx.adobe.com/firefly/web/get-started/learn-the-basics/content-credentials-overview.html) and [C2PA 2.2 specification](https://c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html)
