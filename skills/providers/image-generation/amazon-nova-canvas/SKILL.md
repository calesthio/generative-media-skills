---
name: amazon-nova-canvas
description: Produce and review production image-generation and image-editing workflows with Amazon Nova Canvas on Amazon Bedrock, including native InvokeModel payloads, safe authentication, validation, retries, cost controls, provenance, and lifecycle migration checks. Use when a task names Nova Canvas, amazon.nova-canvas-v1:0, Bedrock image generation, Canvas inpainting/outpainting/background removal, image conditioning, color guidance, image variation, virtual try-on, or Canvas fine-tuning.
---

# Amazon Nova Canvas

Build against the native Amazon Bedrock `InvokeModel` API. Treat every inference as a paid, synchronous image-generation operation and preserve the returned bytes unchanged.

## Start with the lifecycle gate

As verified on 2026-07-09, AWS lists `amazon.nova-canvas-v1:0` as **Legacy** in its supported Regions and gives it an end-of-life date of **2026-09-30**. Do not start a new production dependency on it. New customers cannot use Legacy models; existing customers may lose access after 15 days of inactivity. On or soon after EOL, requests fail unless the customer has a documented private arrangement with the provider. Stakeholder acceptance does not extend service availability.

AWS also forbids new fine-tuning jobs and new Provisioned Throughput endpoints after a foundation model enters Legacy. Public extended access, when offered, may carry higher provider-set pricing. Before any continued use by an eligible existing customer:

1. Query `GetFoundationModel` or `ListFoundationModels` in the intended Region.
2. Confirm the account is still eligible and active, verify the current billing rate, and make a separately authorized low-cost canary only before EOL or under a documented private arrangement when paid inference is allowed.
3. Recheck the [Nova Canvas model page](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-canvas.html) for lifecycle, endpoint, Region, and successor information.
4. Refuse to guess a replacement model ID. Record a named migration owner and cutover date.

Current production facts (verified 2026-07-09):

| Item | Value |
| --- | --- |
| Base model ID | `amazon.nova-canvas-v1:0` |
| Runtime | `bedrock-runtime` |
| API | Native synchronous `InvokeModel`; not Converse, Responses, Chat Completions, or Bedrock Mantle |
| Inference route | In-Region only; no geo or global inference profile |
| Base-model service tier | Standard only |
| Base-model provisioned throughput | Not supported |
| In-Region availability | `us-east-1`, `eu-west-1`, `ap-northeast-1` |
| Prompt language | English |
| Inputs / output | Text and image / image |
| Lifecycle | Legacy in all currently supported Regions; EOL 2026-09-30 |

Never silently move an image or prompt to a different Region. Region choice is a data-residency decision.

## Establish access without embedding secrets

Prefer the AWS SDK credential-provider chain and short-lived role credentials. On AWS compute, attach a least-privilege execution role. For local development, use IAM Identity Center, `aws login`, or an assume-role profile. Do not place access keys or Bedrock API keys in source, command history, manifests, prompts, or logs.

Bedrock also supports service-specific bearer API keys through `AWS_BEARER_TOKEN_BEDROCK`. Long-term Bedrock API keys are tied to IAM users; use them only when the organization's key policy permits them, store them in a secret manager, and rotate them. The environment variable is recognized by current AWS SDKs. See [Bedrock API-key authentication](https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys-use.html) and the [AWS credential provider chain](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html).

Grant only `bedrock:InvokeModel` for the model and Regions actually used. For example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "InvokeNovaCanvasOnly",
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-canvas-v1:0",
        "arn:aws:bedrock:eu-west-1::foundation-model/amazon.nova-canvas-v1:0",
        "arn:aws:bedrock:ap-northeast-1::foundation-model/amazon.nova-canvas-v1:0"
      ]
    }
  ]
}
```

Narrow this list to one Region when possible. Model discovery, customization, S3, KMS, logging, and watermark-detection operations require separate permissions; do not broaden the inference role preemptively.

## Choose an official task

Use only the task types in the current [request/response schema](https://docs.aws.amazon.com/nova/latest/userguide/image-gen-req-resp-structure.html):

| Goal | `taskType` | Parameter object | Key inputs |
| --- | --- | --- | --- |
| Text-to-image | `TEXT_IMAGE` | `textToImageParams` | `text`; optional `negativeText`, `style` |
| Layout/composition conditioning | `TEXT_IMAGE` | `textToImageParams` | Add `conditionImage`, optional `controlMode`, `controlStrength` |
| Palette guidance | `COLOR_GUIDED_GENERATION` | `colorGuidedGenerationParams` | `colors`, `text`; optional `referenceImage`, `negativeText` |
| Reference variation | `IMAGE_VARIATION` | `imageVariationParams` | `images`; optional/ambiguous `text`, `negativeText`, `similarityStrength` |
| Replace/remove a region | `INPAINTING` | `inPaintingParams` | `image`, exactly one of `maskPrompt`/`maskImage`; optional generation text |
| Extend/replace outside region | `OUTPAINTING` | `outPaintingParams` | `image`, exactly one mask, optional `outPaintingMode`, generation text |
| Cut out foreground | `BACKGROUND_REMOVAL` | `backgroundRemovalParams` | `image` only |
| Transfer a product/garment | `VIRTUAL_TRY_ON` | `virtualTryOnParams` | `sourceImage`, `referenceImage`, one mask mode |

Do not invent upscaling, image-to-video, asynchronous jobs, streaming, ControlNet names other than the two documented control modes, arbitrary style IDs, or an OpenAI-compatible route.

Subject consistency is not an inference-time task type. Although Canvas historically supported fine-tuning, AWS now forbids new fine-tuning jobs because the foundation model is Legacy. Only evaluate a custom Canvas model that was created before Legacy under the narrowly documented lifecycle rules; otherwise choose and validate an Active alternative without inventing a successor ID.

## Apply the common schema precisely

For every task except `BACKGROUND_REMOVAL`, `imageGenerationConfig` is optional:

```json
{
  "width": 1024,
  "height": 1024,
  "quality": "standard",
  "cfgScale": 6.5,
  "seed": 12,
  "numberOfImages": 1
}
```

- `quality`: `standard` (default) or `premium`.
- `cfgScale`: 1.1–10 inclusive; default 6.5. Start in the 4–7 range.
- `numberOfImages`: 1–5; default 1.
- `seed`: 0–2,147,483,646; default 12. Pin it in experiments and manifests. A seed aids comparison but is not a contractual guarantee of byte-identical output across service/model updates.
- `width` and `height`: default 1024. Omit both for `INPAINTING`, `OUTPAINTING`, and `VIRTUAL_TRY_ON`, whose output follows the edit input.
- Omit the entire configuration object for `BACKGROUND_REMOVAL`.

For generation dimensions, require each side to be 320–4096 inclusive, divisible by 16, aspect ratio from 1:4 through 4:1, and within the documented pixel cap. Use AWS's published supported-resolution examples or a canary for a boundary value; AWS pages conflict on whether exactly 4,194,304 pixels is accepted.

Input images must be base64-encoded PNG or JPEG, 8-bit RGB. PNG may have an alpha channel, but input pixels cannot be transparent or translucent. Input dimensions follow the side/aspect/pixel rules, except sides need not be divisible by 16. Validate locally before encoding.

### Task-specific payloads

Replace each `<BASE64_...>` placeholder with base64 image bytes, not a data URL.

Text-to-image with optional conditioning:

```json
{
  "taskType": "TEXT_IMAGE",
  "textToImageParams": {
    "text": "Editorial product photograph of a ceramic teapot on pale oak, soft window light, three-quarter view",
    "negativeText": "text, watermark, duplicate objects, distorted handle",
    "style": "PHOTOREALISM",
    "conditionImage": "<BASE64_PNG_OR_JPEG>",
    "controlMode": "CANNY_EDGE",
    "controlStrength": 0.7
  },
  "imageGenerationConfig": {
    "width": 1024,
    "height": 1024,
    "quality": "standard",
    "cfgScale": 6.5,
    "seed": 24816,
    "numberOfImages": 1
  }
}
```

Omit the three conditioning fields for pure text-to-image. `controlMode` is `CANNY_EDGE` (default) or `SEGMENTATION`; `controlStrength` is 0–1, default 0.7. The eight documented `style` values are:

`3D_ANIMATED_FAMILY_FILM`, `DESIGN_SKETCH`, `FLAT_VECTOR_ILLUSTRATION`, `GRAPHIC_NOVEL_ILLUSTRATION`, `MAXIMALISM`, `MIDCENTURY_RETRO`, `PHOTOREALISM`, `SOFT_DIGITAL_PAINTING`.

Color-guided generation:

```json
{
  "taskType": "COLOR_GUIDED_GENERATION",
  "colorGuidedGenerationParams": {
    "colors": ["#16324F", "#E8C547", "#F7F4EA"],
    "text": "Flat editorial illustration of a harbor market at sunrise",
    "negativeText": "gradients, text, logo"
  },
  "imageGenerationConfig": {
    "width": 1536,
    "height": 1024,
    "quality": "standard",
    "cfgScale": 6.5,
    "seed": 7301,
    "numberOfImages": 1
  }
}
```

Supply 1–10 `#RRGGBB` values. An optional `referenceImage` competes with and contributes its own colors.

Image variation:

```json
{
  "taskType": "IMAGE_VARIATION",
  "imageVariationParams": {
    "images": ["<BASE64_REFERENCE_1>", "<BASE64_REFERENCE_2>"],
    "similarityStrength": 0.7,
    "text": "Studio product photograph, centered composition",
    "negativeText": "text, extra products"
  },
  "imageGenerationConfig": {
    "width": 1024,
    "height": 1024,
    "quality": "standard",
    "cfgScale": 6.5,
    "seed": 901,
    "numberOfImages": 1
  }
}
```

Supply 1–5 images. `similarityStrength` is 0.2–1.0; lower values permit more variation. AWS's overview calls `text` optional, while the detailed schema labels it required and contains unrelated omission wording. Include a non-empty `text` in production until an authorized canary confirms omission behavior in the exact Region.

Inpainting:

```json
{
  "taskType": "INPAINTING",
  "inPaintingParams": {
    "image": "<BASE64_SOURCE>",
    "maskImage": "<BASE64_MASK>",
    "text": "A small matte-black table lamp",
    "negativeText": "cord, text"
  },
  "imageGenerationConfig": {
    "quality": "standard",
    "cfgScale": 6.5,
    "seed": 41,
    "numberOfImages": 1
  }
}
```

Use either `maskImage` or `maskPrompt`, never both. For inpainting masks, pure black pixels change and pure white pixels are protected. Although AWS labels `text` required, the same page says omission removes the masked object and fills the background; include `text` for replacement and use a tested omission only for removal.

Outpainting:

```json
{
  "taskType": "OUTPAINTING",
  "outPaintingParams": {
    "image": "<BASE64_SOURCE>",
    "maskPrompt": "ceramic teapot",
    "outPaintingMode": "PRECISE",
    "text": "A ceramic teapot on a breakfast table in a bright Scandinavian kitchen",
    "negativeText": "text, duplicate teapot"
  },
  "imageGenerationConfig": {
    "quality": "standard",
    "cfgScale": 6.5,
    "seed": 42,
    "numberOfImages": 1
  }
}
```

`DEFAULT` blends through the boundary but can halo under large background changes; `PRECISE` follows the boundary more strictly. With an explicit outpainting mask, the detailed input guide says **white pixels change**. AWS's schema prose elsewhere describes black/white inconsistently, so make a tiny visual fixture part of integration testing and reject masks whose polarity is not recorded.

Background removal:

```json
{
  "taskType": "BACKGROUND_REMOVAL",
  "backgroundRemovalParams": {"image": "<BASE64_SOURCE>"}
}
```

Expect one PNG with 8-bit transparency. Verify that the decoded image has an alpha channel; do not add `imageGenerationConfig`.

Virtual try-on:

```json
{
  "taskType": "VIRTUAL_TRY_ON",
  "virtualTryOnParams": {
    "sourceImage": "<BASE64_PERSON_OR_SCENE>",
    "referenceImage": "<BASE64_PRODUCT>",
    "maskType": "GARMENT",
    "garmentBasedMask": {
      "maskShape": "BOUNDING_BOX",
      "garmentClass": "UPPER_BODY",
      "garmentStyling": {"outerLayerStyle": "OPEN"}
    },
    "maskExclusions": {
      "preserveBodyPose": "ON",
      "preserveHands": "ON",
      "preserveFace": "ON"
    },
    "mergeStyle": "BALANCED",
    "returnMask": true
  },
  "imageGenerationConfig": {
    "quality": "standard",
    "cfgScale": 6.5,
    "seed": 43,
    "numberOfImages": 1
  }
}
```

Virtual try-on does not support `text` or `negativeText`. Choose exactly one mask branch:

- `IMAGE` + `imageBasedMask.maskImage`.
- `GARMENT` + `garmentBasedMask.garmentClass`; use only documented garment classes and applicable styling cues.
- `PROMPT` + `promptBasedMask.maskPrompt`; `BOUNDING_BOX` is recommended when replacement and source silhouettes differ.

Choose `BALANCED` to preserve non-mask pixels, `SEAMLESS` to reduce seams while allowing all pixels to shift slightly, or `DETAILED` for fine logos/text at the risk of a visible seam. Do not represent results as exact sizing or fit; AWS explicitly says fit accuracy is not guaranteed.

## Build prompts as image captions

Write a compact English caption describing subject, action, setting, composition, camera/viewpoint, lighting, palette, and medium. Put unwanted concepts as nouns or phrases in `negativeText`; avoid `no`, `not`, and `without` in either field. Do not pad with claims such as “award winning,” “4K,” or “best quality.”

Use double quotes around short scene text, then verify it manually. Nova Canvas is not reliable for coherent typography. Composite exact legal copy, prices, logos, and UI text downstream with a deterministic graphics tool.

Keep each positive and negative field within 1–1024 characters. The 2025 service card says the 1,024-character cap is combined across the two fields, while the current API page describes 1,024 for each. Use the conservative combined cap unless a Region-specific canary proves otherwise.

## Use a bounded, provenance-preserving Python invocation

Install `boto3` and `Pillow`, configure credentials outside the script, and run only after obtaining approval for paid inference. This example performs one text-to-image request, validates the response, writes the original PNG/JPEG bytes atomically, and creates a non-secret manifest.

```python
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import io
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from PIL import Image, UnidentifiedImageError

MODEL_ID = "amazon.nova-canvas-v1:0"
ALLOWED_REGIONS = {"us-east-1", "eu-west-1", "ap-northeast-1"}
MAX_RESPONSE_BYTES = 25_000_000
MAX_REQUEST_BYTES = 25_000_000
MAX_DECODED_IMAGE_BYTES = 20_000_000
Image.MAX_IMAGE_PIXELS = 20_000_000


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temp_name = handle.name
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def validate_dimensions(width: int, height: int) -> None:
    if not (320 <= width <= 4096 and 320 <= height <= 4096):
        raise ValueError("Each side must be between 320 and 4096 pixels")
    if width % 16 or height % 16:
        raise ValueError("Each generation dimension must be divisible by 16")
    if max(width / height, height / width) > 4:
        raise ValueError("Aspect ratio must be between 1:4 and 4:1")
    # Conservative because AWS pages disagree at the exact 4,194,304 boundary.
    if width * height > 4_194_304:
        raise ValueError("Pixel count exceeds the documented Canvas limit")


def decode_and_inspect(encoded: str) -> tuple[bytes, str, tuple[int, int]]:
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("Response image is not strict base64") from exc
    if not raw or len(raw) > MAX_DECODED_IMAGE_BYTES:
        raise ValueError("Decoded image is empty or exceeds the local safety cap")
    try:
        with Image.open(io.BytesIO(raw)) as probe:
            fmt = probe.format
            size = probe.size
            probe.verify()
        with Image.open(io.BytesIO(raw)) as probe:
            probe.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError("Decoded bytes are not a valid bounded image") from exc
    if fmt not in {"PNG", "JPEG"}:
        raise ValueError(f"Unexpected response image format: {fmt}")
    if size[0] * size[1] > 4_194_304:
        raise ValueError(f"Unexpected response dimensions: {size}")
    return raw, fmt.lower().replace("jpeg", "jpg"), size


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("--negative", default="text, watermark, distorted anatomy")
    parser.add_argument("--region", default=os.getenv("AWS_REGION", "us-east-1"))
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=12)
    parser.add_argument("--quality", choices=("standard", "premium"), default="standard")
    parser.add_argument("--output", type=Path, default=Path("nova-canvas-output"))
    parser.add_argument("--store-prompt", action="store_true")
    args = parser.parse_args()

    if args.region not in ALLOWED_REGIONS:
        raise ValueError("Nova Canvas is not documented for that In-Region endpoint")
    validate_dimensions(args.width, args.height)
    if not (0 <= args.seed <= 2_147_483_646):
        raise ValueError("Seed is outside the documented range")
    if not (1 <= len(args.prompt) <= 1024 and 1 <= len(args.negative) <= 1024):
        raise ValueError("Prompt fields must each contain 1-1024 characters")
    if len(args.prompt) + len(args.negative) > 1024:
        raise ValueError("Conservative combined prompt cap exceeded")

    payload = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": args.prompt,
            "negativeText": args.negative,
        },
        "imageGenerationConfig": {
            "width": args.width,
            "height": args.height,
            "quality": args.quality,
            "cfgScale": 6.5,
            "seed": args.seed,
            "numberOfImages": 1,
        },
    }
    request_body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    if len(request_body) > MAX_REQUEST_BYTES:
        raise ValueError("Serialized request exceeds the InvokeModel body limit")

    # Default to one paid attempt because InvokeModel has no client idempotency token.
    # Enable more attempts only behind an explicit duplicate-spend policy.
    client = boto3.client(
        "bedrock-runtime",
        region_name=args.region,
        config=Config(
            connect_timeout=10,
            read_timeout=300,
            retries={"mode": "standard", "total_max_attempts": 1},
        ),
    )

    try:
        response = client.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=request_body,
        )
        body = response["body"].read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise ValueError("Response exceeds the InvokeModel API body limit")
        document = json.loads(body)
    except ClientError as exc:
        meta = exc.response.get("ResponseMetadata", {})
        error = exc.response.get("Error", {})
        print(
            f"Bedrock error code={error.get('Code')} status={meta.get('HTTPStatusCode')} "
            f"request_id={meta.get('RequestId')}",
            file=sys.stderr,
        )
        return 2
    except (BotoCoreError, json.JSONDecodeError, ValueError) as exc:
        print(f"Invocation/response failure: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3

    images = document.get("images")
    moderation_error = document.get("error")
    if not isinstance(images, list) or not images:
        print(f"No releasable image returned; moderation={moderation_error!r}", file=sys.stderr)
        return 4
    if len(images) != 1:
        print(f"Unexpected returned image count: {len(images)}", file=sys.stderr)
        return 4

    raw, extension, size = decode_and_inspect(images[0])
    output_path = args.output.with_suffix(f".{extension}")
    atomic_write(output_path, raw)  # Keep C2PA/watermark-bearing bytes unchanged.

    response_meta = response.get("ResponseMetadata", {})
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model_id": MODEL_ID,
        "region": args.region,
        "task_type": payload["taskType"],
        "config": payload["imageGenerationConfig"],
        "prompt_sha256": hashlib.sha256(args.prompt.encode()).hexdigest(),
        "negative_sha256": hashlib.sha256(args.negative.encode()).hexdigest(),
        "prompt": args.prompt if args.store_prompt else None,
        "negative_text": args.negative if args.store_prompt else None,
        "aws_request_id": response_meta.get("RequestId"),
        "moderation_notice": moderation_error,
        "output_file": output_path.name,
        "output_format": extension,
        "output_dimensions": list(size),
        "output_sha256": hashlib.sha256(raw).hexdigest(),
    }
    atomic_write(
        output_path.with_suffix(output_path.suffix + ".manifest.json"),
        json.dumps(manifest, indent=2, sort_keys=True).encode(),
    )
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Do not reopen and resave the returned image merely to validate it; common image libraries can strip C2PA metadata. Hash and archive the original bytes first. If downstream transformation is necessary, retain the original, log the derivative relationship, and preserve provenance in accordance with applicable AWS terms.

## Handle moderation, service errors, and retries deliberately

Canvas has two error channels:

- Request validation or unsafe text/image input: HTTP 400 `ValidationException`. Do not retry unchanged. Distinguish ordinary schema errors from Canvas content-filter messages without attempting to evade the filter.
- Unsafe generated output: HTTP 200 can contain fewer `images` than requested plus an `error` string saying some or all images were blocked. Treat the count mismatch and `error` as a moderation outcome, not transport success.

The `InvokeModel` API also documents `AccessDeniedException` (403), `ResourceNotFoundException` (404), `ModelTimeoutException` (408), `ModelErrorException` (424), `ThrottlingException`/`ModelNotReadyException` (429), `InternalServerException` (500), and `ServiceUnavailableException` (503).

Use exponential backoff with jitter for 429 and 503, a small total-attempt budget, and a concurrency limiter below the account quota. Do not retry 400, 403, or 404 unchanged. A connection reset or timeout is ambiguous: the service may have completed and charged for the image, and `InvokeModel` has no client idempotency token. Escalate or retry under an explicit duplicate-cost policy. Keep the same seed/config for diagnosis, but do not assume this prevents a second charge.

Set `read_timeout` to at least 300 seconds as AWS recommends for Canvas, especially for premium quality, high resolutions, or multiple images. Keep connect timeout much shorter.

## Validate production output, not just HTTP status

For every returned image:

1. Require a bounded JSON body and strict base64.
2. Decode to bounded bytes and verify the real image format and dimensions.
3. Require the intended number of releasable images; inspect `error` even on HTTP 200.
4. For background removal, require PNG with meaningful alpha, inspect subject edges, and test compositing over light/dark/checkerboard backgrounds.
5. For edits, compare protected regions pixel-for-pixel where the selected mode promises preservation; inspect seams, halos, subject identity, hands/faces, product markings, and geometry.
6. Verify prompt adherence, object counts, camera/view, palette, anatomy, factual/product claims, scene text, protected traits, and prohibited content with a use-case-specific rubric.
7. Route public, commercial, likeness-sensitive, high-impact, or regulated content to a qualified human reviewer.
8. Preserve the original bytes, request ID, model ID, Region, task, config, seed, hashes, moderation outcome, review decision, and parent/derivative relationship.
9. Maintain a fixed regression set across seeds, task types, demographics, edge cases, and known failures; retest after model/service updates.

Do not claim that a successful watermark check proves authorship, truth, consent, or rights. Modified images can reduce watermark-detection accuracy.

## Control cost and quota before invoking

AWS prices Canvas per generated image, based on resolution band and quality. The [Bedrock pricing page](https://aws.amazon.com/bedrock/pricing/) is dynamic; recheck it and the account's actual Legacy-access billing immediately before estimating or running a job. AWS's lifecycle policy says public extended access can carry higher provider-set pricing, so the static table below is not authority for a Legacy account's current charge. Snapshot verified 2026-07-09:

| Output band | Standard | Premium |
| --- | ---: | ---: |
| Up to 1024×1024 | $0.04/image | $0.06/image |
| Up to 2048×2048 | $0.06/image | $0.08/image |

Estimate `requested_images × unit_price × attempts`, then add storage, transfer, logging, review, derivative processing, and any custom-model charges. Moderation, failures, and retries can affect billed totals; use AWS Cost Explorer/Budgets and actual billing data rather than assuming only saved images are charged. Require a hard maximum for images, attempts, concurrency, and spend before a batch.

The [Bedrock quota table](https://docs.aws.amazon.com/general/latest/gr/bedrock.html) currently lists **100 on-demand Nova Canvas requests per minute per supported Region**, marked non-adjustable. AWS notes that account quotas can vary. Query Service Quotas and observe actual throttling for the account/Region; rate-limit below the smaller value. Five images in one request consume one request but can cost five image generations and take longer.

Base Nova Canvas does not support provisioned throughput. Do not create a new fine-tuning job or new Provisioned Throughput endpoint for this Legacy model. A custom Canvas model created before Legacy may qualify for continued existing deployment or a new on-demand custom deployment under AWS's lifecycle rules; verify that exact resource and arrangement rather than generalizing from historical fine-tuning documentation.

## Preserve privacy, rights, safety, and provenance

- Obtain rights to every prompt, source, reference, mask, logo, garment/product image, and person's likeness. Obtain appropriate consent for real-person manipulation, biometric processing, and digital replicas. Virtual try-on is not permission to alter a person's image.
- Do not use outputs for prohibited practices under applicable law or the [AWS Responsible AI Policy](https://aws.amazon.com/ai/responsible-ai/policy/). Never attempt to bypass non-configurable Canvas safety filters.
- Treat outputs as probabilistic drafts. They can misrepresent products, hallucinate unseen sides, distort anatomy, introduce bias, and render incorrect text. Do not use them as evidence or as the sole basis for consequential decisions.
- Keep sensitive data out of prompts and references unless the approved data classification, Region, retention, access, encryption, and incident-response controls allow it. Disable or protect model invocation logging; if enabled, it can copy full requests/responses to customer-controlled logs or S3.
- The current [Canvas service card](https://docs.aws.amazon.com/ai/responsible-ai/nova-canvas/overview.html) says Bedrock does not use Canvas inputs or outputs to train Bedrock models and does not share them between customers or with third-party model providers. AWS's newer abuse-detection documentation describes default zero data retention while reserving model-specific exceptions. Recheck both before processing sensitive data and document the governing contract.
- Do not promise ownership or freedom from infringement. Check the current AWS agreement, service terms, applicable licenses, and local law with counsel. The service card describes IP indemnity for generally available Nova outputs, subject to the conditions in the AWS Service Terms; this is not a substitute for rights clearance.
- Canvas adds an invisible watermark to generated images and C2PA Content Credentials containing model/platform/task provenance. Preserve them. Current AWS Service Terms prohibit removing or altering generated provenance data.
- Content Credentials can be inspected with Content Credentials Verify unless metadata was removed. AWS watermark detection for Canvas is currently a **preview**, available in `us-east-1` and `us-west-2`, accepts JPEG/PNG up to 18 MB, and can become less accurate after edits. Do not build a hard compliance dependency on a preview API without version and fallback controls.

## Gate historical custom models

Do not start a new Canvas fine-tuning project: AWS's current lifecycle policy prohibits new customization jobs after the foundation model enters Legacy. If the organization created a Canvas custom model before the 2026-03-30 Legacy date, inventory its training authorization, IAM role, S3/KMS controls, evaluation record, current deployment, billing, deletion/retention duties, and EOL migration plan. AWS says such a pre-existing custom model may continue an existing on-demand deployment or pre-Legacy Provisioned Throughput endpoint, and may create a new **on-demand custom deployment**; it may not create a new fine-tuning job or new Provisioned Throughput endpoint.

For a new subject-consistency need, discover an Active model with current customization support, validate it independently, and obtain approval before changing provider/model. Do not guess a Nova Canvas successor or transplant historical Canvas hyperparameters into another model.

## Record known documentation conflicts

Do not silently resolve these current AWS discrepancies:

- Image variation: overview says `text` optional; detailed schema labels it required and contains inpainting language. Include text unless an authorized canary proves omission.
- Prompt length: schema gives 1–1024 characters for positive and negative fields individually; the 2025 service card says 1,024 combined. Enforce the stricter combined cap by default.
- Pixel boundary: overview names 2048×2048 as valid and editing allows 4.19 million pixels or smaller; detailed input guide says total pixels must be *less than* 4,194,304. Prefer published examples and canary boundary values.
- Outpainting masks: the dedicated input guide says white pixels change, while schema prose repeats black-change wording before calling inpainting/outpainting opposites. Lock polarity with a fixture test.
- Seed: current schema allows 0–2,147,483,646, while some official SDK examples still describe a smaller 0–858,993,459 range. Use the schema range, or the smaller range when maximum backward compatibility matters.
- Provisioned throughput: base-model page says unsupported and historical fine-tuning materials describe customized Canvas provisioned serving, but the current lifecycle policy forbids new Provisioned Throughput endpoints after Legacy. Treat only qualifying pre-Legacy custom resources as continuable.

When a boundary matters, save the source URL, retrieval date, Region, exact payload, response status/message, SDK version, and AWS request ID. Revalidate after any lifecycle or documentation change.

## Primary sources

All volatile facts above were checked on 2026-07-09 against primary AWS sources:

- [Nova Canvas model details, lifecycle, endpoints, tiers, and Regions](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-canvas.html)
- [Bedrock model lifecycle, Legacy access, EOL, pricing, and customization restrictions](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html)
- [Canvas features and top-level limits](https://docs.aws.amazon.com/nova/latest/userguide/image-generation.html)
- [Input images, masks, and resolution constraints](https://docs.aws.amazon.com/nova/latest/userguide/image-gen-access.html)
- [Native task request/response schema and generation config](https://docs.aws.amazon.com/nova/latest/userguide/image-gen-req-resp-structure.html)
- [Canvas-specific error handling](https://docs.aws.amazon.com/nova/latest/userguide/image-gen-errors.html)
- [Virtual try-on behavior and tradeoffs](https://docs.aws.amazon.com/nova/latest/userguide/image-gen-vto.html)
- [InvokeModel API and service errors](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
- [Bedrock endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html)
- [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
- [Canvas responsible-AI service card](https://docs.aws.amazon.com/ai/responsible-ai/nova-canvas/overview.html)
- [Bedrock data protection](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html)
- [Bedrock abuse detection and retention](https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html)
- [AWS Service Terms](https://aws.amazon.com/service-terms/)
- [AWS Responsible AI Policy](https://aws.amazon.com/ai/responsible-ai/policy/)
- [Watermark detection preview](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-image-models.html)
