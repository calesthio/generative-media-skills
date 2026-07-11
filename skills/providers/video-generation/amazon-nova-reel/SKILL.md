---
name: amazon-nova-reel
description: Produce and operate Amazon Nova Reel video-generation jobs through Amazon Bedrock. Use for Nova Reel text-to-video, image-conditioned animation, automated or manual multi-shot storyboards, async S3 delivery, cost and approval gates, production continuity, output custody, and AWS-specific safety, privacy, IAM, and provenance decisions.
---

# Amazon Nova Reel production

Treat Nova Reel as an asynchronous production service, not a synchronous clip function. Plan the shots, validate every input, obtain an exact approval, submit once with an idempotency token, persist the invocation ARN, and promote only validated S3 artifacts.

All volatile facts in this skill were verified against first-party AWS sources on **2026-07-10**. Recheck model access, Region, price, quota, and lifecycle immediately before a paid run.

## Establish the current contract

Do **not** select Nova Reel as a new default. AWS's Bedrock lifecycle table marks both published Reel versions **Legacy** as of 2026-03-30, with EOL **2026-09-30**:

| Model | Region(s) | Current use |
|---|---|---|
| `amazon.nova-reel-v1:1` | `us-east-1` | Only an already-authorized, still-active workload that needs Reel 1.1 capabilities and has a funded exit plan |
| `amazon.nova-reel-v1:0` | `us-east-1`, `eu-west-1`, `ap-northeast-1` | Existing six-second legacy workloads only; do not migrate new work onto it |

New customers cannot use Legacy models, existing customers may lose access after 15 days of inactivity, and new Provisioned Throughput cannot be created. On or soon after EOL, calls fail unless the customer has a private continued-access arrangement. Migration is not automatic. AWS's table does not identify an active Nova Reel successor, so do not invent one: for work that must operate past EOL, select another currently active provider unless AWS publishes a successor or the account team confirms a private arrangement.

Where the account has confirmed Reel 1.1 access and the delivery can finish before EOL, Reel 1.1 supports:

- `TEXT_VIDEO`: one six-second text-to-video or image-to-video shot.
- `MULTI_SHOT_AUTOMATED`: one long prompt expanded into 12–120 seconds in six-second increments; no input image.
- `MULTI_SHOT_MANUAL`: an ordered list of six-second shots, each with a prompt and optional starting image; duration follows shot count, up to 120 seconds.
- English prompts, 1280×720 output, 24 fps, silent video, asynchronous `StartAsyncInvoke`, and S3 delivery.

The Nova generation guide still teaches Reel 1.1, but the Bedrock lifecycle page explicitly says its dates govern Bedrock usage. Treat the lifecycle table as authoritative when the pages differ. Before any run, confirm the account can invoke the exact model in the exact Region, confirm the job will complete before EOL, and record the exit route.

Sources: [Bedrock model lifecycle](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html), [Nova Reel generation guide](https://docs.aws.amazon.com/nova/latest/userguide/video-generation.html), [Bedrock Nova Reel model page](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-reel.html), [regional compatibility](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html).

### Exact input limits

| Mode | Text | Images | Duration |
|---|---|---|---|
| `TEXT_VIDEO` | 1–512 characters | zero or one starting image | exactly 6 seconds |
| `MULTI_SHOT_AUTOMATED` | 1–4,000 characters | none | 12–120 seconds, multiple of 6 |
| `MULTI_SHOT_MANUAL` | 1–512 characters per shot | optional image per shot | six seconds per shot, up to 120 seconds (therefore at most 20 shots) |

Always send `fps: 24` and `dimension: "1280x720"`. Seed is optional, defaults to 42, and must be 0–2,147,483,646. Reference images must be PNG or JPEG, 1280×720, 8-bit RGB; PNG alpha is allowed only when every pixel is fully opaque. AWS documents a 25 MB limit for images supplied from S3. Use an image as the starting keyframe, not as a general style-reference bank.

AWS's current manual-mode prose does not publish a separate minimum shot count. Use `TEXT_VIDEO` for one six-second shot and manual mode for a genuinely multi-shot list; do not turn the production convention “at least two” into a claimed service-schema minimum. Reel 1.0 is the legacy six-second model; long and multi-shot requests require Reel 1.1.

Source: [video generation access and input schemas](https://docs.aws.amazon.com/nova/latest/userguide/video-gen-access.html).

## Choose the mode from the edit decision

- Choose `TEXT_VIDEO` for a self-contained six-second insert, a first-frame animation, or cheap concept exploration.
- Choose `MULTI_SHOT_AUTOMATED` when overall theme and stylistic flow matter more than exact shot boundaries. It is not an image-conditioned mode.
- Choose `MULTI_SHOT_MANUAL` when the edit has an approved shot list, specific starting frames, product angles, or controlled transitions.
- Generate separate six-second jobs when shots require independent selection, replacement, budgets, or delivery schedules. A failed multi-shot request does not yield a dependable partial master.

Nova Reel has no native audio. Budget and produce music, dialogue, ambience, and effects separately. Do not promise lip sync, precise typography, exact product geometry, physical accuracy, or deterministic reproduction from a seed. AWS specifically warns that coherent on-screen text and anatomically correct humans are not assured.

## Direct motion rather than converse

Write a visual description, not a chat command. Put the highest-value subject and action first, then environment, lighting, look, and camera motion. Use one primary camera move per six-second shot.

Useful camera phrases documented by AWS include `dolly in`, `dolly out`, `pan left`, `pan right`, `tilt up`, `tilt down`, `orbit`, `tracking shot`, `zoom in`, `zoom out`, and `static shot`. Describe visible change over time: “steam curls upward as the camera slowly dollies in,” not “make it cinematic.”

For image-to-video, describe only the desired motion and changes. Re-describing the reference inconsistently can encourage drift. Preserve identity through stable nouns and attributes: repeat the same product name, material, color, wardrobe, time of day, and lens language in every manual shot.

**Production heuristic:** lock a continuity bible before a multi-shot run:

1. Subject identity: exact stable descriptors and prohibited changes.
2. World rules: place, weather, time, palette, texture, aspect and lens feel.
3. Motion grammar: camera height, speed, direction, and transition intent.
4. Shot purpose: what new information each six-second unit contributes.
5. Continuity anchors: entry/exit direction, screen position, action state, and lighting direction.

Source: [Nova Reel prompting best practices](https://docs.aws.amazon.com/nova/latest/userguide/prompting-video-generation.html).

## Build valid requests

### Example: single-shot image-to-video request

Intent: animate an approved packshot without introducing a new product design.

```python
model_input = {
    "taskType": "TEXT_VIDEO",
    "textToVideoParams": {
        "text": (
            "Slow dolly in on the cobalt glass perfume bottle. "
            "A narrow highlight travels across the glass while faint mist drifts behind it. "
            "Dark slate studio, soft rim light, premium restrained motion."
        ),
        "images": [{
            "format": "png",
            "source": {"s3Location": {
                "uri": "s3://approved-inputs/campaign-42/bottle-1280x720.png",
                "bucketOwner": "123456789012"
            }}
        }]
    },
    "videoGenerationConfig": {
        "durationSeconds": 6,
        "fps": 24,
        "dimension": "1280x720",
        "seed": 1845
    }
}
```

Expected result: a silent six-second 720p clip beginning from the supplied frame. Likely failures include label deformation, changing reflections, excessive mist, or camera motion stronger than requested. Reject rather than repair a materially incorrect product depiction.

### Example: automated 18-second concept

```python
model_input = {
    "taskType": "MULTI_SHOT_AUTOMATED",
    "multiShotAutomatedParams": {
        "text": (
            "Cinematic dawn study of a coastal research station built from weathered steel. "
            "Begin with a wide aerial approach over dark water, transition to scientists crossing "
            "a glass walkway, and finish inside the warm laboratory looking back toward the sea. "
            "Maintain overcast blue exterior light, amber interiors, realistic architecture, slow "
            "controlled camera motion, and a quiet documentary tone throughout."
        )
    },
    "videoGenerationConfig": {
        "durationSeconds": 18,
        "fps": 24,
        "dimension": "1280x720",
        "seed": 9071
    }
}
```

Use this mode for ideation, not exact editorial timing. Review each delivered shot as well as `output.mp4`.

### Example: manual three-shot storyboard

```python
model_input = {
    "taskType": "MULTI_SHOT_MANUAL",
    "multiShotManualParams": {
        "shots": [
            {"text": "Wide static shot of a cobalt glass perfume bottle centered on dark slate, soft white rim light from camera left, faint haze, premium minimal studio."},
            {"text": "Macro tracking shot moving left to right across the same cobalt glass bottle, preserving its rectangular silhouette and silver cap; the camera-left rim light glides over the glass."},
            {"text": "Slow dolly out from the same cobalt glass bottle on dark slate as the haze clears, preserving the silver cap, camera-left rim light, and restrained premium studio palette."}
        ]
    },
    "videoGenerationConfig": {
        "fps": 24,
        "dimension": "1280x720",
        "seed": 1845
    }
}
```

The repeated anchors are deliberate. If exact product shape is mandatory, attach an approved starting image to each shot and still require human product QA.

## Gate every paid submission

AWS prices Nova Reel per generated second. The Bedrock pricing page's interactive Nova Reel row showed **USD 0.08 per generated second** when verified on 2026-07-10. Treat that as a dated planning snapshot, not an execution constant: Legacy/public-extended-access pricing can change, and the lifecycle table currently shows no public-extended-access start date for Reel. Re-read the official price row or obtain an account quote immediately before approval and execution. Quote `duration × verified rate`, then add S3, KMS, logging, retrieval, and transfer costs separately. At the dated snapshot, 6 s = $0.48, 18 s = $1.44, and 120 s = $9.60.

Source: [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/).

Require an approval record containing:

- canonical approval-envelope SHA-256, exact request, model ID, Region, S3 input and output URIs;
- generated seconds, verified unit rate, currency, maximum authorized amount, and price verification timestamp;
- lifecycle verification timestamp, confirmed Legacy access, EOL date, planned completion date, and exit route;
- rights/consent status for every reference and depicted person;
- retention classification, approver identity, and expiration;
- an explicit statement that the run is paid and asynchronous.

Fail closed on a missing or mismatched digest, expired approval, non-finite or insufficient maximum, stale price/lifecycle evidence, unconfirmed Legacy access, a job that can cross EOL, wrong Region, unapproved bucket/prefix, or changed input bytes. A human “looks good” message is not a reusable spending authorization.

### Example: dry-run-first submission

This complete example is dry-run-first. It submits only when `EXECUTE=1`, current price and lifecycle evidence are supplied, Legacy access is explicitly confirmed, the approval digest exactly matches that evidence and the AWS request, and the approved maximum covers the estimate. It does not prove access without a call; the operator must verify access in the account before authorizing execution.

```python
import hashlib
import json
import math
import os
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse

MODEL_ID = "amazon.nova-reel-v1:1"
REGION = "us-east-1"
OUTPUT_URI = os.environ.get("NOVA_OUTPUT_S3", "")
RATE = Decimal(os.environ.get("NOVA_RATE_USD_PER_SEC", "0.08"))  # Planning fallback only.
PRICE_VERIFIED_AT = os.environ.get("NOVA_PRICE_VERIFIED_AT", "")
LIFECYCLE_VERIFIED_AT = os.environ.get("NOVA_LIFECYCLE_VERIFIED_AT", "")
PRICE_EVIDENCE = os.environ.get("NOVA_PRICE_EVIDENCE", "")
LIFECYCLE_EVIDENCE = os.environ.get("NOVA_LIFECYCLE_EVIDENCE", "")
PLANNED_COMPLETION_DATE = os.environ.get("NOVA_PLANNED_COMPLETION_DATE", "")
EXIT_ROUTE = os.environ.get("NOVA_EXIT_ROUTE", "")
AWS_ACCOUNT_ID = os.environ.get("NOVA_AWS_ACCOUNT_ID", "")
PROJECT_ID = os.environ.get("NOVA_PROJECT_ID", "")
APPROVER_ID = os.environ.get("NOVA_APPROVER_ID", "")
APPROVAL_EXPIRES_AT = os.environ.get("NOVA_APPROVAL_EXPIRES_AT", "")
RETENTION_CLASS = os.environ.get("NOVA_RETENTION_CLASS", "")
EOL = date(2026, 9, 30)

model_input = {
    "taskType": "TEXT_VIDEO",
    "textToVideoParams": {"text": "Static wide shot of wind moving through silver grass at dawn, soft fog, natural documentary light."},
    "videoGenerationConfig": {"durationSeconds": 6, "fps": 24, "dimension": "1280x720", "seed": 42},
}
aws_request = {
    "modelId": MODEL_ID,
    "modelInput": model_input,
    "outputDataConfig": {"s3OutputDataConfig": {"s3Uri": OUTPUT_URI}},
}
approval_envelope = {
    "aws_request": aws_request,
    "unit_rate_usd_per_generated_second": str(RATE),
    "price_verified_at": PRICE_VERIFIED_AT,
    "price_evidence": PRICE_EVIDENCE,
    "lifecycle_verified_at": LIFECYCLE_VERIFIED_AT,
    "lifecycle_evidence": LIFECYCLE_EVIDENCE,
    "model_lifecycle": "Legacy",
    "eol_date": EOL.isoformat(),
    "legacy_access_confirmed": os.environ.get("NOVA_LEGACY_ACCESS_CONFIRMED") == "1",
    "planned_completion_date": PLANNED_COMPLETION_DATE,
    "exit_route": EXIT_ROUTE,
    "aws_account_id": AWS_ACCOUNT_ID,
    "project_id": PROJECT_ID,
    "approver_id": APPROVER_ID,
    "approval_expires_at": APPROVAL_EXPIRES_AT,
    "rights_and_consent_confirmed": os.environ.get("NOVA_RIGHTS_CONFIRMED") == "1",
    "retention_class": RETENTION_CLASS,
}
canonical = json.dumps(approval_envelope, sort_keys=True, separators=(",", ":")).encode()
digest = hashlib.sha256(canonical).hexdigest()
STATE = Path(os.environ.get("NOVA_STATE", f"nova-reel-{digest}.json"))
seconds = Decimal(model_input["videoGenerationConfig"]["durationSeconds"])
estimate = seconds * RATE
print(json.dumps({"approval_sha256": digest, "estimated_usd": str(estimate), "approval_envelope": approval_envelope}, indent=2))

if os.environ.get("EXECUTE") != "1":
    raise SystemExit("DRY RUN: set EXECUTE=1 only after approval")
if not RATE.is_finite() or RATE <= 0:
    raise SystemExit("verified unit rate must be finite and positive")
if REGION != "us-east-1" or MODEL_ID != "amazon.nova-reel-v1:1":
    raise SystemExit("unsupported production route")
if os.environ.get("NOVA_LEGACY_ACCESS_CONFIRMED") != "1":
    raise SystemExit("Legacy model access is not confirmed for this AWS account")
if datetime.now(timezone.utc).date() >= EOL:
    raise SystemExit("Nova Reel EOL reached; use a confirmed successor or private arrangement")
if not PRICE_VERIFIED_AT or not LIFECYCLE_VERIFIED_AT or not PRICE_EVIDENCE or not LIFECYCLE_EVIDENCE:
    raise SystemExit("current price and lifecycle verification timestamps and evidence are required")
try:
    price_checked = datetime.fromisoformat(PRICE_VERIFIED_AT.replace("Z", "+00:00"))
    lifecycle_checked = datetime.fromisoformat(LIFECYCLE_VERIFIED_AT.replace("Z", "+00:00"))
    approval_expires = datetime.fromisoformat(APPROVAL_EXPIRES_AT.replace("Z", "+00:00"))
    planned_completion = date.fromisoformat(PLANNED_COMPLETION_DATE)
except ValueError:
    raise SystemExit("invalid verification, approval-expiry, or completion timestamp")
now = datetime.now(timezone.utc)
for label, checked in (("price", price_checked), ("lifecycle", lifecycle_checked)):
    age_seconds = (now - checked).total_seconds() if checked.tzinfo is not None else -1
    if checked.tzinfo is None or age_seconds < 0 or age_seconds > 86400:
        raise SystemExit(f"{label} verification is future-dated or older than 24 hours")
if approval_expires.tzinfo is None or approval_expires <= now:
    raise SystemExit("approval is expired or lacks a timezone")
if planned_completion < now.date() or planned_completion >= EOL or not EXIT_ROUTE.strip():
    raise SystemExit("completion must be current, precede EOL, and include an exit route")
if len(AWS_ACCOUNT_ID) != 12 or not AWS_ACCOUNT_ID.isdigit() or not PROJECT_ID.strip():
    raise SystemExit("AWS account and project identity are required")
if not APPROVER_ID.strip() or not RETENTION_CLASS.strip():
    raise SystemExit("approver identity and retention class are required")
if os.environ.get("NOVA_RIGHTS_CONFIRMED") != "1":
    raise SystemExit("input, brand, and likeness rights/consent are not confirmed")
parsed = urlparse(OUTPUT_URI)
allowed = os.environ.get("NOVA_ALLOWED_OUTPUT_PREFIX", "")
if parsed.scheme != "s3" or not parsed.netloc or ".." in parsed.path.split("/"):
    raise SystemExit("invalid S3 output URI")
if not allowed or not OUTPUT_URI.startswith(allowed.rstrip("/") + "/"):
    raise SystemExit("S3 output is outside the approved bucket/prefix")
if os.environ.get("APPROVED_SHA256") != digest:
    raise SystemExit("approval digest mismatch")
try:
    maximum = Decimal(os.environ["APPROVED_MAX_USD"])
except (KeyError, InvalidOperation):
    raise SystemExit("missing or invalid approved maximum")
if not math.isfinite(float(maximum)) or maximum < estimate:
    raise SystemExit("approved maximum is non-finite or insufficient")

claim = {"state": "SUBMITTING", "approval_sha256": digest, "approval_envelope": approval_envelope, "clientRequestToken": digest}
fd = os.open(STATE, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
with os.fdopen(fd, "w", encoding="utf-8") as handle:
    json.dump(claim, handle, indent=2)
    handle.flush()
    os.fsync(handle.fileno())

def replace_state(value):
    temporary = STATE.with_name(STATE.name + ".tmp")
    temp_fd = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(temp_fd, "w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, STATE)

try:
    import boto3
    client = boto3.client("bedrock-runtime", region_name=REGION)
    response = client.start_async_invoke(
        **aws_request,
        clientRequestToken=digest,
    )
    claim.update(state="SUBMITTED", invocationArn=response["invocationArn"])
except Exception as exc:
    claim.update(state="UNKNOWN", error_type=type(exc).__name__)
    replace_state(claim)
    raise SystemExit("submission outcome unknown; reconcile by exact token before any retry")
replace_state(claim)
print(json.dumps(claim, indent=2))
```

The API accepts `clientRequestToken` (1–256 printable ASCII characters) specifically for idempotency and returns an `invocationArn`. Persist both. `ListAsyncInvokes` returns each summary's `clientRequestToken`, but it does not offer a token filter: paginate the original submission window and match the token exactly, then use `GetAsyncInvoke` on the recovered ARN. If listing cannot establish the outcome and the SDK operation had a retryable transport ambiguity, retry only the **byte-for-byte same logical request with the same token**; never vary the payload or mint a new token. Escalate if the service does not return a recoverable ARN. Do not claim idempotency cancels a job or prevents charges for distinct tokens.

Source: [StartAsyncInvoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_StartAsyncInvoke.html), [ListAsyncInvokes API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ListAsyncInvokes.html), [GetAsyncInvoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_GetAsyncInvoke.html).

## Operate the asynchronous job

1. Persist the request, digest, token, invocation ARN, output prefix, submit time, approval, and input hashes before downstream work.
2. Poll `GetAsyncInvoke` with bounded exponential backoff and jitter. Valid states are `InProgress`, `Completed`, and `Failed`. Respect throttling and stop at a declared deadline; a local timeout does not mean the paid job stopped.
3. After network ambiguity, query by ARN or list by time and exact returned token. A retry is permissible only with the identical request and identical idempotency token; a new token is a new paid creation risk.
4. Treat `Completed` as “ready to inspect,” not “approved for delivery.”
5. Preserve the provider-written evidence. AWS documents `manifest.json`, `output.mp4`, and successful multi-shot files named `shot_0001.mp4`, etc. The same guide currently calls the status object `generation-status.json` in one summary and `video-generation-status.json` in its detailed result section. Discover the actual object within the exact invocation prefix, preserve its name and bytes, and validate its documented `fullVideo`/`shots` schema instead of assuming one filename.

AWS documents typical times of about 90 seconds for six seconds and 14–17 minutes for two minutes. These are observations, not an SLA. The dated default quota table lists 10 concurrent requests for Reel 1.0 and 3 for Reel 1.1; actual account quotas can differ and AWS may update defaults. Check Service Quotas before scheduling a batch.

Sources: [video access and result schema](https://docs.aws.amazon.com/nova/latest/userguide/video-gen-access.html), [Bedrock quotas](https://docs.aws.amazon.com/general/latest/gr/bedrock.html).

## Secure S3 and preserve custody

Grant least privilege. AWS documents `bedrock:InvokeModel` and prefix-scoped `s3:PutObject` as the minimum to generate, plus `bedrock:GetAsyncInvoke` and `bedrock:ListAsyncInvokes` for tracking. Reading results needs prefix-scoped `s3:GetObject` and usually `s3:ListBucket` constrained with `s3:prefix`. For a cross-account bucket, set `bucketOwner` and the bucket policy; do not infer ownership from the bucket name. For SSE-KMS, pass the KMS key ARN as `kmsKeyId` when required and grant only the necessary key use: writes need `kms:GenerateDataKey`; reads may need `kms:Decrypt`; `kms:DescribeKey` is commonly required. The key policy must also permit the correct principal and constrain account/source where supported.

Use a dedicated bucket or immutable per-job prefix in the same approved data boundary. Enable Block Public Access, versioning where appropriate, encryption, lifecycle rules, CloudTrail data events if required, and explicit bucket-owner conditions. Do not put secrets, personal data, or unapproved asset names in object keys, prompts, tags, or logs.

Before promotion:

- require `Completed` and a successful `fullVideo` entry in the discovered provider status JSON (`video-generation-status.json` or `generation-status.json` per the current documentation inconsistency);
- constrain every S3 URI to the approved bucket and invocation prefix;
- download with a byte cap and authenticated SDK call, never an arbitrary returned URL;
- verify MP4 magic/container with `ffprobe`, decode the full file, and confirm 1280×720, 24 fps, expected six-second multiple, and no required audio track;
- inspect every constituent shot for continuity, safety, text, anatomy, brand/product accuracy, flicker, warping, and unintended people or marks;
- compute SHA-256, preserve the original plus manifest/status, record model/Region/request/approval/source hashes, and publish atomically without overwriting an existing deliverable.

Keep the original Nova output if provenance matters. Transcoding, remuxing, metadata stripping, or social-platform processing can remove Content Credentials even when the invisible watermark remains. Record derivative lineage rather than claiming a derivative retains credentials you have not verified.

## Rights, privacy, and responsible release

Use only input images, brands, locations, and likenesses the project is authorized to use. Obtain documented consent for identifiable people and digital replicas. Do not imply that model safeguards replace legal or editorial review.

AWS states that Bedrock does not use Nova Reel inputs or outputs to train Bedrock models. Bedrock's current abuse-detection page describes zero operator access and zero data retention by default, with stated model-specific retention exceptions that do not list Nova Reel; it separately says apparent CSAM inputs or outputs may be blocked, stored, reviewed, and reported. Your S3 output and any invocation logging intentionally retain data under your controls. Avoid absolute “never stored” or “zero retention” claims without accounting for abuse handling, S3, logs, backups, and account configuration.

Nova Reel applies an invisible watermark to generated videos, and Reel 1.1 adds C2PA-based Content Credentials. Verify credentials on the original and disclose AI generation where the audience or policy warrants it. AWS Service Terms say AI output is Your Content, may not be unique, and Provenance Data must not be removed, obscured, or altered. AWS also describes conditional IP indemnity for generally available Nova outputs; eligibility and exclusions are contractual questions, not a warranty of uniqueness, ownership under every jurisdiction, or permission to use infringing inputs.

Sources: [Nova Reel AI Service Card](https://docs.aws.amazon.com/ai/responsible-ai/nova-reel/overview.html), [Bedrock abuse detection](https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html), [S3 access](https://docs.aws.amazon.com/bedrock/latest/userguide/s3-bucket-access.html), [AWS Service Terms](https://aws.amazon.com/service-terms/), [AWS Responsible AI Policy](https://aws.amazon.com/ai/responsible-ai/policy/), [AWS Acceptable Use Policy](https://aws.amazon.com/aup/).

## Final release checklist

- Current model ID, lifecycle, Region, account access, price, quota, planned completion before EOL, and exit route reverified.
- Mode and schema match the creative brief; images pass format, size, alpha, rights, and hash checks.
- Prompt and storyboard preserve subject, world, lighting, motion, and screen-direction continuity.
- Exact digest/cost approval exists; one idempotent creation attempt is durably recorded.
- Async status and provider S3 manifest/status are preserved.
- Original and every shot pass technical, safety, continuity, brand, likeness, and editorial QA.
- Artifact hash, provenance, disclosure, derivative lineage, retention, and deletion owner are recorded.
- Audio and final finishing are handled as separate, approved production stages.
