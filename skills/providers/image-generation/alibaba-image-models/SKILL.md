---
name: alibaba-image-models
description: Plan, prompt, call, edit, iterate, and productionize Alibaba Cloud Model Studio image generation with current Wan 2.7 Image, Qwen-Image 2.0, and Z-Image Turbo models. Use for Alibaba/DashScope text-to-image, multi-reference generation, instruction editing, character-consistent image sets, typography and layout work, regional authentication, model selection, API integration, cost/rate-limit planning, troubleshooting, safety, rights, privacy, and output QA.
---

# Alibaba image models

Treat this skill as the production guide for Alibaba Cloud Model Studio image inference, not for local Wan checkpoints, image-to-video, model training, or legacy one-purpose Wan editing endpoints. Check the live model list before every production integration because model IDs, aliases, regions, pricing, and quotas change.

## Establish the production contract

Before generating, record:

- deliverable and channel: hero, poster, product image, character sheet, storyboard, social crop, or edit;
- required pixel dimensions, aspect ratio, count, and file format;
- exact text, brand colors, protected areas, and layout hierarchy;
- reference-image roles and permission to use each reference;
- acceptable identity/product drift and whether exact typography must be composited later;
- target region, workspace, model ID or pinned snapshot, budget ceiling, and retention needs;
- approval gates: low-cost sample, selected direction, edit pass, final QA.

Announce the provider, model, region, number of requested images, and estimated charge before a paid call. Generate one or two low-cost candidates first. Do not silently change a chosen model, region, or prompt-rewrite policy.

## Route deliberately

The following facts were verified against Alibaba Cloud documentation on **2026-07-09**.

| Need | Prefer | Why and boundary |
|---|---|---|
| Broad generation, text rendering, brand palette, editing, up to nine references, bounding-box edits, or coherent sets | `wan2.7-image-pro` | Most complete current Wan route. Pure text-to-image can reach the 4K specification; edits and image sets are limited to 2K. Standard mode returns 1–4 images; sequential mode can return up to 12. |
| Similar Wan workflows with faster/lower-cost output | `wan2.7-image` | Same workflow family, but up to 2K. Validate quality on the actual brief. |
| Negative prompt or up to six variants in one synchronous request | `qwen-image-2.0-pro` | Combined generation/editing route with 1–6 PNG outputs and a documented negative prompt. Editing accepts one to three images. |
| Faster Qwen generation/editing | `qwen-image-2.0` | Accelerated 2.0 route; retain the same sync protocol and test quality against Pro. |
| Fast, inexpensive generation-only portraits or product photos | `z-image-turbo` | One PNG output, no editing, 512×512 through 2048×2048 range. Prompt rewriting doubles its documented per-image price. |

Do not call older `wanx2.1-*`, Qwen Plus/Max, or separate Qwen edit IDs merely from habit. Use them only for an explicit compatibility or migration requirement after checking their current region and protocol. The current 2.0 models are synchronous-only; asynchronous Qwen image calls apply to `qwen-image-plus` and `qwen-image`, not Qwen-Image 2.0.

Do not equate provider descriptions with independent quality proof. “Faster,” “Pro,” and “recommended” are documented product positions; run a brief-specific sample when the choice matters.

## Bind region, key, workspace, and endpoint

Use a Model Studio API key from the same region as the model and endpoint. Store it in `DASHSCOPE_API_KEY`; never place it in source, prompts, logs, patches, or artifacts. Prefer a least-privilege workspace and separate development and production keys.

For current synchronous Wan 2.7, Qwen-Image 2.0, and Z-Image native calls, use:

| Region | Endpoint |
|---|---|
| Singapore | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` |
| China (Beijing) | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` |

Send `Authorization: Bearer $DASHSCOPE_API_KEY` and `Content-Type: application/json`. Workspace-dedicated domains are Alibaba's production recommendation; shared DashScope and trial domains have different tradeoffs. Never use the OpenAI-compatible `/compatible-mode/v1` path for the native image payload shown here.

Treat the model, key, region, deployment scope, and endpoint as one configuration unit. A 401 or service error often means they do not match. Confirm availability in the console/model list rather than assuming that every model exists in every region.

### Choose synchronous versus asynchronous deliberately

Current Wan 2.7 supports both native protocols; Qwen-Image 2.0 and Z-Image Turbo are synchronous-only.

| Workload | Create route | Required header | Completion |
|---|---|---|---|
| Wan 2.7 short interactive call | `POST .../api/v1/services/aigc/multimodal-generation/generation` | normal JSON/Bearer headers | Result in the response |
| Wan 2.7 long generation, edit, bounding-box edit, or sequential set | `POST .../api/v1/services/aigc/image-generation/generation` | add `X-DashScope-Async: enable` | Save `output.task_id`, then poll |
| Qwen-Image 2.0 or Z-Image Turbo | synchronous multimodal route only | do **not** add the async header | Result in the response |

For an asynchronous Wan call, persist the creation `request_id`, `output.task_id`, and initial `task_status` before doing other work. Poll `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` with Bearer authentication, capped backoff, jitter, and a deadline. Continue through `PENDING` and `RUNNING`; accept output only at `SUCCEEDED`; stop and record `code`/`message` for `FAILED`, `CANCELED`, or `UNKNOWN`. Do not create a replacement task merely because polling was interrupted. Task IDs, task data, and result URLs are documented for 24 hours, so reconcile and download inside that window.

### Preserve known documentation ambiguities

- The current Qwen text-to-image page labels a Beijing endpoint but prints the Singapore host in that line and in some SDK comments. Other current Alibaba pages show `cn-beijing.maas.aliyuncs.com` for Beijing. Treat this as an apparent documentation copy error; verify the endpoint in the console before deployment.
- Alibaba marks `qwen-image-2.0-pro-2026-06-22` as recommended while also stating that the floating `qwen-image-2.0-pro` alias is currently equivalent to `...-2026-04-22`. Do not assume the floating alias points to the newest snapshot. Pin a dated ID when reproducibility matters, after confirming regional availability.
- Qwen describes the custom-size range in total-pixel terms using “512×512 to 2048×2048,” while recommended presets include a side longer than 2048. Use documented presets or validate the requested dimensions; do not reinterpret the statement as a per-side cap.
- The Z-Image page currently shows a shared Beijing DashScope endpoint while newer platform guidance recommends workspace-dedicated domains. Confirm the exact supported Z-Image endpoint for the selected region before shipping.

## Build requests correctly

Use a single `user` message. Put each reference in an `image` object and one instruction in a `text` object. Use `"width*height"` with an asterisk, never `"widthxheight"`.

### Wan 2.7

- Accept 0–9 JPEG/JPG/PNG-without-alpha/BMP/WEBP inputs; each must be at most 20 MB, 240–8000 pixels per side, and within a 1:8–8:1 aspect ratio.
- Write prompts in Chinese or English, up to 5,000 characters; excess text is truncated.
- Use `size: "1K"`, `"2K"`, or `"4K"`, or a custom `"width*height"`. `wan2.7-image-pro` allows 4K only for pure text-to-image outside sequential mode. `wan2.7-image` tops out at 2K.
- Treat a requested Wan size as a target rather than proof of exact delivered pixels; inspect the decoded output and usage because provider-selected dimensions can differ slightly.
- Use `n: 1..4` in standard mode. With `enable_sequential: true`, use `n: 1..12`; the model may return fewer than `n`.
- Use `bbox_list` for interactive edits. Keep one outer list per input image, use absolute source-image coordinates `[x1,y1,x2,y2]`, use `[]` when an image has no target, and specify at most two boxes per image.
- Leave `thinking_mode: true` for difficult pure text-to-image work when latency is acceptable. It only applies in non-sequential mode with no image input.
- Use `color_palette` only outside sequential mode: 3–10 HEX colors, each ratio written to two decimal places, summing exactly to `100.00%`.
- Do not send `prompt_extend`; current Wan 2.7 uses `thinking_mode` instead.

### Qwen-Image 2.0

- Generate from one text object; 2.0 prompts accept up to 1,300 tokens and excess input is truncated.
- Edit with one to three JPG/JPEG/PNG/BMP/TIFF/WEBP/GIF inputs of at most 10 MB each. Only the first GIF frame is used. For best results, keep each side between 384 and 3072 pixels.
- Refer to inputs by order: “Image 1,” “Image 2,” and “Image 3.” State the role of each image and what must remain unchanged.
- Set `n: 1..6`, `negative_prompt` up to 500 characters, `seed: 0..2147483647`, and `size: "width*height"`. Output is PNG.
- Leave `prompt_extend: true` for short exploratory prompts. Set it to `false` for exact copy, brand constraints, reproducible prompt audits, or carefully specified layouts. Rewriting does not change the negative prompt.
- Treat equal seeds as a stability aid, not deterministic reproduction.
- For Qwen edits, the service adjusts requested dimensions to nearby multiples of 16; the official example maps `1033*1032` to `1040*1024`. Decode and record the actual size. When delivery pixels are exact, crop/resize deterministically after generation rather than asserting the model returned the request verbatim.

### Z-Image Turbo

- Use one Chinese or English text object, up to 800 characters, and receive exactly one PNG.
- Use `size: "width*height"`; the documented range is 512×512 through 2048×2048 and the default is `1024*1536`.
- Keep `prompt_extend: false` for fastest/lower-cost direct generation. Set it to `true` only when LLM rewriting/reasoning is worth the extra latency and documented 2× price.
- Do not supply edit images or request multiple outputs.

## Prompt for controllable production

Label the following as **production heuristics**, not provider guarantees.

Write prompts in descending importance:

1. Name the deliverable and subject.
2. Lock composition: viewpoint, framing, subject placement, negative space, depth planes.
3. Describe identity/product invariants and reference roles.
4. Specify materials, lighting, color, medium, and finish.
5. Quote every required string exactly and describe its hierarchy, location, alignment, case, and contrast.
6. State exclusions or preservation constraints.

Prefer concrete spatial language over adjective piles. For editing, write a change list and a preservation list: “Replace X with Y; preserve face, pose, camera, shadows, packaging geometry, logo placement, and background.” For multi-reference work, map each input to one responsibility and avoid asking two images to define the same property.

For character continuity, first approve a neutral identity sheet. Reuse it as the first reference, repeat identity invariants, change one scene variable at a time, keep a stable seed where supported, and compare face, hair, body proportions, costume anchors, and distinctive marks across the set. Use Wan sequential mode when narrative coherence matters, but expect to curate rather than accept every frame.

For brand color, use Wan `color_palette` when palette proportions matter, then measure the returned asset rather than trusting visual impression. Reserve final logo geometry, legal copy, small labels, and exact color values for deterministic composition when deviation is unacceptable.

For typography and layout:

- Quote literal copy and keep it short per generation pass.
- Describe one hierarchy at a time: headline, subtitle, label, footer.
- Define a clear grid, margins, safe zones, alignment, and contrast.
- Generate the background/illustration separately from long or regulated copy.
- Composite exact copy in a design tool when spelling, font licensing, kerning, accessibility, or legal accuracy is mandatory.

## Use a gated iteration loop

1. **Validate locally:** check required variables, region/endpoint match, model ID, input formats, image counts, sizes, and estimated maximum output charge. Do not call the API yet.
2. **Explore cheaply:** request one or two samples at a suitable lower resolution. Keep model, prompt, parameters, seed, request ID, and source hashes in a manifest.
3. **Select structurally:** judge composition, identity, text placement, edit fidelity, and brand fit before surface polish.
4. **Repair one axis:** change only prompt, reference, crop, seed, palette, or model per pass. Preserve the accepted variables.
5. **Finish deterministically:** composite exact typography/logos, crop variants, color-manage, and export with the needed profile and metadata.
6. **Run final QA:** inspect at 100%, thumbnail size, and every delivery crop; verify literal text, anatomy, reflections, product geometry, reference leakage, edge artifacts, watermark policy, and provenance records.
7. **Persist immediately:** download returned URLs before their 24-hour expiry and verify status, MIME type, magic bytes, byte count, image decode, and actual dimensions before marking the job complete. Apply a deterministic crop/resize only after preserving the original.

Use automated checks for dimensions, file type, alpha, blank/corrupt files, and duplicate hashes. Use human review for meaning, likeness, IP/trademark issues, deceptive context, cultural sensitivity, and aesthetic quality.

## Example: dry-run-first Wan generation

This complete example logs only a request hash and redacted summary by default, and sends only when `SEND_DASHSCOPE_REQUEST=1`. Sending creates a billable call. Install `requests` and Pillow first.

```python
import hashlib
import ipaddress
import json
import os
import socket
import tempfile
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests
from PIL import Image, UnidentifiedImageError

MAX_JSON_BYTES = 8 * 1024 * 1024
MAX_IMAGE_BYTES = 25 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000
Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS


def require_safe_https(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise RuntimeError("Artifact URL must use HTTPS")
    if parsed.username or parsed.password or parsed.fragment:
        raise RuntimeError("Artifact URL contains credentials or a fragment")
    addresses = {
        info[4][0] for info in socket.getaddrinfo(parsed.hostname, parsed.port or 443)
    }
    if not addresses or any(not ipaddress.ip_address(value).is_global for value in addresses):
        raise RuntimeError("Artifact host did not resolve exclusively to public addresses")


def download_verified_image(url, destination):
    current = url
    response = None
    for _ in range(6):
        require_safe_https(current)
        response = requests.get(
            current,
            headers={"Accept": "image/png"},  # Never forward the Ark bearer token.
            timeout=(10, 120),
            stream=True,
            allow_redirects=False,
        )
        if response.status_code in {301, 302, 303, 307, 308}:
            location = response.headers.get("Location")
            response.close()
            if not location:
                raise RuntimeError("Artifact redirect omitted Location")
            current = urljoin(current, location)
            continue
        response.raise_for_status()
        break
    else:
        raise RuntimeError("Too many artifact redirects")

    content_type = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
    if content_type != "image/png":
        response.close()
        raise RuntimeError(f"Unexpected artifact Content-Type: {content_type}")
    declared = response.headers.get("Content-Length")
    if declared and int(declared) > MAX_IMAGE_BYTES:
        response.close()
        raise RuntimeError("Artifact exceeds declared byte cap")

    destination.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=destination.parent, prefix=".wan-")
    total = 0
    digest = hashlib.sha256()
    try:
        with os.fdopen(handle, "wb") as output:
            for chunk in response.iter_content(64 * 1024):
                if not chunk:
                    continue
                total += len(chunk)
                if total > MAX_IMAGE_BYTES:
                    raise RuntimeError("Artifact exceeded byte cap while streaming")
                digest.update(chunk)
                output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
        response.close()
        with open(temporary, "rb") as source:
            prefix = source.read(8)
            if prefix != b"\x89PNG\r\n\x1a\n":
                raise RuntimeError("Artifact signature is not PNG")
            source.seek(0)
            try:
                with Image.open(source) as image:
                    actual_format = image.format
                    actual_size = image.size
                    if actual_size[0] * actual_size[1] > MAX_IMAGE_PIXELS:
                        raise RuntimeError(f"Artifact exceeds pixel cap: {actual_size}")
                    image.verify()
                with Image.open(temporary) as image:
                    image.load()
            except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
                raise RuntimeError("Artifact failed bounded image decode") from exc
        if actual_format != "PNG" or actual_size[0] * actual_size[1] > MAX_IMAGE_PIXELS:
            raise RuntimeError(f"Unexpected decoded image: {actual_format} {actual_size}")
        os.replace(temporary, destination)
    except Exception:
        response.close()
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    return {"bytes": total, "sha256": digest.hexdigest(), "dimensions": actual_size}

key = os.environ.get("DASHSCOPE_API_KEY")
workspace = os.environ.get("DASHSCOPE_WORKSPACE_ID")
region = os.environ.get("DASHSCOPE_REGION", "ap-southeast-1")
hosts = {
    "ap-southeast-1": f"https://{workspace}.ap-southeast-1.maas.aliyuncs.com",
    "cn-beijing": f"https://{workspace}.cn-beijing.maas.aliyuncs.com",
}
if region not in hosts:
    raise SystemExit("DASHSCOPE_REGION must be ap-southeast-1 or cn-beijing")

payload = {
    "model": "wan2.7-image-pro",
    "input": {"messages": [{"role": "user", "content": [{
        "text": "Editorial product hero for a matte navy travel bottle, three-quarter view on a pale stone plinth, bottle centered left with clean negative space on the right, soft window light, restrained shadows, premium realistic photography, no text, no logo invention"
    }]}]},
    "parameters": {"size": "2K", "n": 1, "thinking_mode": True,
                   "watermark": False, "seed": 18427},
}
payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
print({"model": payload["model"], "request_sha256": hashlib.sha256(payload_bytes).hexdigest(),
       "n": payload["parameters"]["n"], "size": payload["parameters"]["size"]})
if os.environ.get("SEND_DASHSCOPE_REQUEST") != "1":
    raise SystemExit("Dry run only; set SEND_DASHSCOPE_REQUEST=1 to send a paid call")
if not key or not workspace:
    raise SystemExit("Set DASHSCOPE_API_KEY and DASHSCOPE_WORKSPACE_ID")

url = hosts[region] + "/api/v1/services/aigc/multimodal-generation/generation"
r = requests.post(url, headers={"Authorization": f"Bearer {key}",
                  "Content-Type": "application/json"}, data=payload_bytes,
                  timeout=(10, 180), stream=True)
raw_response = r.raw.read(MAX_JSON_BYTES + 1, decode_content=True)
r.close()
if len(raw_response) > MAX_JSON_BYTES:
    raise RuntimeError("API response exceeded JSON byte cap")
try:
    data = json.loads(raw_response)
except (UnicodeDecodeError, ValueError):
    raise RuntimeError(f"Non-JSON response: HTTP {r.status_code}")
if not r.ok or data.get("code"):
    raise RuntimeError({"http": r.status_code, "request_id": data.get("request_id"),
                        "code": data.get("code"), "message": data.get("message")})

items = data["output"]["choices"][0]["message"]["content"]
urls = [item["image"] for item in items if item.get("type") == "image" or "image" in item]
if not urls:
    raise RuntimeError("Successful response contained no image URL")
out = Path("wan-output.png")
artifact = download_verified_image(urls[0], out)
print({"saved": str(out), **artifact,
       "request_id": data.get("request_id"), "usage": data.get("usage")})
```

For a Qwen multi-image edit, retain the same transport but replace the model and message content:

```python
payload = {
    "model": "qwen-image-2.0-pro",
    "input": {"messages": [{"role": "user", "content": [
        {"image": os.environ["PRODUCT_IMAGE_URL"]},
        {"image": os.environ["MATERIAL_IMAGE_URL"]},
        {"text": "Use Image 1 as the product geometry and camera reference. Apply only the brushed copper material from Image 2 to the product shell. Preserve silhouette, controls, label position, perspective, lighting direction, shadows, and background. Do not add objects or text."}
    ]}]},
    "parameters": {"n": 2, "size": "1536*1024", "prompt_extend": False,
                   "negative_prompt": "warped geometry, altered controls, extra text, extra objects",
                   "watermark": False, "seed": 18427},
}
```

Use public HTTPS URLs only for non-sensitive references, or use documented Base64 data URLs when policy permits. Avoid embedding secrets in URLs.

## Handle failures without duplicate spend

- **401/authentication:** verify key, region, workspace ID, endpoint, and model deployment scope as a unit. Do not print the key.
- **InvalidParameter:** validate the asterisk size syntax, counts, model-specific fields, input ordering, and unsupported combinations such as Wan `color_palette` with sequential mode.
- **`DataInspectionFailed`:** treat this as moderation rejection. Review prompt and references for non-compliant content; do not disguise or obfuscate the request to bypass controls.
- **Rate limiting or bursts:** queue calls, cap concurrency, add randomized exponential backoff, and honor any retry guidance. Do not retry validation or moderation failures blindly.
- **Timeout or uncertain outcome:** preserve `request_id`; determine whether a result exists before resubmitting. For current asynchronous Wan 2.7 or older asynchronous Qwen routes, poll the existing `task_id` instead of creating duplicates. Qwen-Image 2.0 and Z-Image Turbo do not gain an async recovery route.
- **Missing/corrupt URL:** require at least one returned image item, download immediately, verify MIME/decode, and retry only the failed unit.

As verified 2026-07-09, limits are account-level across RAM users, workspaces, and keys. The rate-limit page lists Wan 2.7 at 5 task submissions/second and concurrency 5 in Singapore and Beijing; Z-Image Turbo at 2 submissions/second; and Qwen-Image 2.0 submission limits that differ by Pro versus accelerated IDs. Treat the console and current rate-limit page as authoritative rather than hard-coding these values. A rate limit controls throughput, not total spend.

## Govern cost, data, rights, and safety

As verified 2026-07-09, Alibaba bills successful output images, not inputs; failed processing is not billed. Current Singapore list prices are `wan2.7-image-pro` $0.075/image, `wan2.7-image` $0.03/image, `qwen-image-2.0-pro` $0.075/image, `qwen-image-2.0` $0.035/image, and Z-Image Turbo $0.015/image without prompt rewriting or $0.03/image with it. Beijing prices and free quotas differ. Free quotas in the cited image tables apply only to international deployment and expire 90 days after activation. Recheck price and quota immediately before quoting or calling.

Compute worst-case charge from requested outputs, including Wan sequential `n`, not from the number of requests. Set account budgets/alerts and application-side count and spend caps.

Returned image URLs and Wan task data are documented as available for 24 hours; that is not a complete statement of service-wide input/output retention. Download to approved storage, then apply the organization's deletion, access, encryption, and backup rules. Model monitoring can collect account/workspace call data, and inference logging—when enabled—records inputs and outputs to Log Service. Basic and advanced monitoring data is documented as retained for 30 days by default, but the cited page does not establish the inference-log retention period; confirm the Log Service configuration.

For an account governed by the current Alibaba Cloud International Model Studio terms, Alibaba states that it will not use Member Content to develop or improve Model Studio models without separate consent; current Model Studio privacy materials likewise state customer data is not used for model training. Record the applicable contract, account, and verification date rather than generalizing this commitment to every Alibaba affiliate or future term. This no-training commitment does **not** mean zero retention.

Endpoint region alone is not a strict residency guarantee: the international terms permit transfer, storage, and processing where Alibaba, affiliates, or subcontractors maintain facilities. Confirm console settings, deployment scope, cross-border transfer terms, subprocessors, regional requirements, contracts, and DPA/security review before sending confidential, biometric, health, customer, or unreleased product data. If public documentation does not answer a retention or residency question, state the uncertainty and escalate it; do not promise zero retention.

Use only references and copy the user has the right and consent to process. Obtain explicit consent for identifiable people and heightened approval for minors or sensitive contexts. Do not imply endorsement, fabricate documentary evidence, remove provenance to deceive, or use generation to evade moderation. Check trademarks, celebrity likenesses, copyrighted characters, packaging, fonts, and licensed assets before publication. Alibaba's own text-to-image guide makes the customer responsible for evaluating trademark, celebrity-likeness, and copyright risk.

Treat `watermark: true` as a visible provider mark (`AI Generated` for Wan 2.7; `Qwen-Image` for Qwen), not as a complete provenance or rights solution. Preserve an internal manifest containing source permissions, model/snapshot, region, prompt, parameters, seed, request ID, creation time, edits, and human approvals even when a visible watermark is off. Independently review every output: the service terms warn that outputs may be unintended, non-unique, or similar across customers.

## Primary sources

All volatile facts above were checked **2026-07-09** against first-party sources:

- [Alibaba Cloud image model selection](https://www.alibabacloud.com/help/en/model-studio/image-model)
- [Wan 2.7 image generation and editing API](https://www.alibabacloud.com/help/en/model-studio/wan-image-generation-and-editing-api-reference)
- [Qwen-Image text-to-image API](https://www.alibabacloud.com/help/en/model-studio/qwen-image-api)
- [Qwen-Image Edit API](https://www.alibabacloud.com/help/en/model-studio/qwen-image-edit-api)
- [Qwen image editing guide](https://www.alibabacloud.com/help/en/model-studio/qwen-image-edit-guide)
- [Z-Image API](https://www.alibabacloud.com/help/en/model-studio/z-image-api-reference)
- [Text-to-image guide and safety notes](https://www.alibabacloud.com/help/en/model-studio/text-to-image)
- [Base URL overview](https://www.alibabacloud.com/help/en/model-studio/base-url)
- [Model pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing)
- [Rate limiting](https://www.alibabacloud.com/help/en/model-studio/rate-limit)
- [Model monitoring and log retention](https://www.alibabacloud.com/help/en/model-studio/model-telemetry)
- [Alibaba Cloud International Product Terms, Model Studio section](https://www.alibabacloud.com/help/en/legal/latest/alibaba-cloud-international-website-product-terms-of-service-v-3-8-0)
- [Model Studio privacy notice](https://www.alibabacloud.com/help/en/model-studio/privacy-notice)
- [Model Studio FAQ, training and output-storage domains](https://www.alibabacloud.com/help/en/model-studio/faq-about-alibaba-cloud-model-studio)
