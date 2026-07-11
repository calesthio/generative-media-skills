---
name: luma-ray-video
description: Direct and operate Luma Ray video generation through the current Luma Agents API and distinguish it from the consumer Luma App and legacy Dream Machine API. Use for Ray 3.2 text/image/multi-keyframe video, edits, extends, reframes, HDR/EXR, pricing and approvals, async delivery, migration, rights, privacy, and production QA.
---

# Luma Ray video production

Route the job before writing a request. Luma currently exposes similarly named products with incompatible models, schemas, credentials, prices, and data terms. For new API integrations, use the **Luma Agents API** and `ray-3.2`; treat the older Dream Machine API as a legacy compatibility surface.

Volatile facts were verified from first-party Luma sources on **2026-07-10**. Recheck the model page, schema, price, account limits, and applicable agreement before any paid or sensitive run.

## Separate the three surfaces

### Current developer surface: Luma Agents API

- Base URL: `https://agents.lumalabs.ai/v1`
- Credential: `LUMA_AGENTS_API_KEY`, sent as a Bearer token; current keys begin `luma-api-`.
- Model: `ray-3.2`.
- Generation types: `video`, `video_edit`, `video_reframe` on `POST /v1/generations`; poll `GET /v1/generations/{id}`.
- Current response header: `X-API-Version: 2026-04-01`. It is informational; do not send it as a request version.
- Current official Python package: `luma-agents` (`from luma_agents import Luma`). TypeScript, Go, CLI, and raw HTTP are also documented.

Use this surface for all new code. Sources: [Agents quickstart](https://docs.agents.lumalabs.ai/), [models](https://docs.agents.lumalabs.ai/guides/model/), [API reference](https://docs.agents.lumalabs.ai/api/).

### Consumer surface: Luma App

The browser/iOS product has subscription plans and a separate credit system. Ray3.14 is documented as App-only, not an API model. App credits do not transfer to API billing. Luma’s May 2026 official-information page says “Dream Machine” is retired product terminology and calls the consumer product **Luma App**.

Do not translate App controls, credit counts, relaxed mode, watermarks, or Ray3.14 features into Agents API fields. Sources: [official product terminology](https://lumalabs.ai/llm-info), [Ray3.14 FAQ](https://lumalabs.ai/learning-hub/ray3-faq), [App plans](https://lumalabs.ai/pricing).

### Legacy developer surface: Dream Machine API

The older `https://api.lumalabs.ai/dream-machine/v1` API, `LUMAAI_API_KEY`, `lumaai` SDK, and `ray-2` / `ray-flash-2` models remain documented. Its routes and shapes include legacy `keyframes.frame0/frame1`, callbacks, camera concepts, Modify Video, Reframe, and a separate `POST /generations/{id}/audio` operation.

Luma publishes no shutdown date for that surface in the reviewed docs. Therefore label it **legacy by product/API generation, not discontinued**. Maintain existing integrations only after checking their dashboard and docs; do not send legacy fields to the Agents API. The legacy audio reference does not publish enough current price, duration, output, or lifecycle detail to make it a safe default. Sources: [legacy video guide](https://docs.lumalabs.ai/docs/video-generation), [legacy Modify Video](https://docs.lumalabs.ai/docs/modify-video), [legacy audio operation](https://docs.lumalabs.ai/reference/addaudiotogeneration).

## Use the Ray 3.2 capability contract

| Intent | Current request | Key constraints |
|---|---|---|
| Text-to-video | `type: "video"` | Prompt plus video settings |
| Image-to-video | `type: "video"` + anchors | `start_frame`/`end_frame`, or multi-keyframes |
| Forward/backward extend | `type: "video"` + exactly one prior `generation_id` in `start_frame` or `end_frame` | Prior generation must be completed; SDR only |
| Video-to-video edit | `type: "video_edit"` + `source` + `video.edit` | Preserves/reinterprets source motion; source ≤18 s on every input channel |
| Reframe/outpaint | `type: "video_reframe"` + `source` + target `aspect_ratio` | SDR only; source ≤30 s on every input channel |

All current Ray 3.2 prompts are 1–6,000 characters. Video generation accepts `9:16`, `3:4`, `1:1`, `4:3`, `16:9`, and `21:9`. Output is MP4. Generation offers `360p` draft, `540p`, `720p`, and `1080p`; default is 720p. Standard generation supports 5 or 10 seconds. The public API has no seed parameter and no negative-prompt parameter.

### Anchors and multi-keyframes

`video.start_frame` and `video.end_frame` each accept exactly one of a public HTTPS `url`, base64 `data` plus `media_type`, a ready `file_id`, or, for extend, a prior `generation_id`. The legacy two-anchor form does not work at 10 seconds.

For the current multi-keyframe path, provide both:

- `video.keyframes`: 1–64 `ImageRef` entries;
- `video.keyframe_indexes`: same-length, unique positions in the 24 fps output grid: 0–120 for 5 s and 0–240 for 10 s.

Multi-keyframes are mutually exclusive with `start_frame`, `end_frame`, and `loop`; unlike the legacy anchor pair, they support 10 s and HDR. Luma’s marketing API page says “up to 16 keyframes,” while the current Agents guide and API schema say 64. Treat the current schema as the wire contract, but revalidate before relying on more than 16.

Source: [Ray 3.2 video generation](https://docs.agents.lumalabs.ai/guides/videos/generation/).

### Loop, HDR, EXR, and extend

- `video.loop: true` is create-only. It conflicts with 10 s, HDR, `end_frame`, and multi-keyframes.
- `video.hdr: true` requires 720p or 1080p and 5 s for `type: "video"`.
- `video.exr_export: true` requires HDR and yields an EXR alongside the HDR MP4.
- Single-keyframe extend uses a prior completed generation ID as the only `start_frame` (forward) or `end_frame` (backward). It is SDR and billed as one five-second block; loop is allowed only on forward extend.
- Interpolating a prior video generation plus another keyframe is not supported on the current extend path.

### Video editing

Supply exactly one source: a completed same-client `generation_id`, a `file_id`, or URL/base64 video with `media_type: "video/*"`. Every source channel is limited to 18 seconds; URL/data sources are also limited to 200 MB. The general FAQ currently says 30 seconds for edit, while the typed `video_edit` schema says 18 seconds. Use the stricter typed-schema limit and reverify before production.

Start with `video.edit.auto_controls: true`. For intentional preservation tradeoffs, use one of nine `strength` values: `adhere_1..3`, `flex_1..3`, or `reimagine_1..3`. For advanced control, use per-signal `pose`, `depth`, `normals`, `trajectory`, and `face`; these controls cannot coexist with `auto_controls: true`. Editing supports up to 64 indexed guide frames on the source frame grid. `end_frame`, loop, and `image_ref` are invalid. The output aspect ratio derives from the source and silently ignores a supplied `aspect_ratio`.

Source: [Ray 3.2 video editing](https://docs.agents.lumalabs.ai/guides/videos/editing/).

### Reframing

`video_reframe` requires a source and target aspect ratio. Every source channel is limited to 30 seconds; URL/data sources are also limited to 200 MB. It is SDR only and rejects edit controls, loop, anchors, HDR, and EXR. Optional `video.source_position` supplies all four normalized fields: `x_norm`/`y_norm` from -2 to 2 and positive `w_norm`/`h_norm` up to 2. Vertical 9:16 or 3:4 output at 1080p is not yet available; use 720p or lower.

Source: [Ray 3.2 reframing](https://docs.agents.lumalabs.ai/guides/videos/reframing/).

## Direct the shot

Write prompts as compact shot direction:

1. Subject and invariant identity.
2. Visible action over the clip.
3. Environment and physical interaction.
4. Camera position, lens feel, and one primary move.
5. Lighting, palette, texture, and finish.
6. Continuity or prohibited-change language only when it clarifies a positive target.

**Production heuristic:** one clip should carry one dramatic beat. Use keyframes for exact beats and prompt text for the motion between them. Do not ask one five-second shot to introduce a location, transform a character, execute three camera moves, and resolve an edit.

**Production heuristic:** preserve identity by repeating stable nouns and attributes, not by adding more adjectives. For a product, lock silhouette, material, color, cap/closure, label placement, lighting direction, and screen direction. For a person, use only authorized likeness references and lock wardrobe, hair, age presentation, and entry/exit motion.

### Example: 5-second HDR image-to-video

Intent: a compositing-ready product reveal from an approved starting image.

```python
request_body = {
    "model": "ray-3.2",
    "type": "video",
    "prompt": (
        "Slow 40mm dolly in on the cobalt glass perfume bottle as a narrow white highlight "
        "travels across the glass. Dark slate studio, soft rim light from camera left, restrained "
        "mist, preserve the rectangular silhouette and silver cap."
    ),
    "aspect_ratio": "16:9",
    "video": {
        "resolution": "720p",
        "duration": "5s",
        "hdr": True,
        "start_frame": {"file_id": "11111111-2222-4333-8444-555555555555"},
    },
}
```

Expected result: a five-second HDR MP4 starting from the reference. It does not produce audio or EXR unless `exr_export` is also true. Reject label, silhouette, cap, or color drift rather than presenting it as an approved product.

### Example: three-beat multi-keyframe clip

```python
request_body = {
    "model": "ray-3.2",
    "type": "video",
    "prompt": "A red paper kite rises steadily above a foggy green valley as sunrise warms the clouds; smooth lateral tracking, natural wind and taut string.",
    "aspect_ratio": "16:9",
    "video": {
        "resolution": "720p",
        "duration": "5s",
        "keyframes": [
            {"file_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
            {"file_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"},
            {"file_id": "cccccccc-cccc-4ccc-8ccc-cccccccccccc"},
        ],
        "keyframe_indexes": [0, 60, 120],
    },
}
```

The frames pin opening, midpoint, and closing composition. QA the transitions for speed discontinuity, morphing, and camera jumps.

### Example: motion-preserving edit

```python
request_body = {
    "model": "ray-3.2",
    "type": "video_edit",
    "prompt": "Preserve the choreography and camera motion; transform the warehouse into a moonlit glass conservatory, realistic reflections, cool 35mm film texture.",
    "source": {"generation_id": "d290f1ee-6c54-4b01-90e6-d701748f0851"},
    "video": {
        "resolution": "720p",
        "edit": {"auto_controls": True},
    },
}
```

If motion or identity drifts, try `adhere_1` or explicit guide frames rather than layering contradictory controls.

## Price and approve the exact operation

The current Agents pricing guide is the execution source. Luma’s general API marketing page contains a conflicting summary table, so quote from the dated Agents guide and recheck before submission. Pay-as-you-go is shared capacity with no latency SLA; Provisioned Throughput pricing for video requires sales contact.

Selected **2026-07-10** pay-as-you-go totals:

| Operation | 540p | 720p | 1080p |
|---|---:|---:|---:|
| SDR generation, 5 s | $0.15 | $0.30 | $1.20 |
| SDR generation, 10 s | $0.45 | $0.90 | $3.60 |
| HDR generation, 5 s | — | $0.60 | $2.40 |
| HDR+EXR generation, 5 s | — | $0.90 | $3.60 |
| SDR edit, 5 s | $0.72 | $1.08 | $2.16 |
| SDR edit, 10 s | $1.44 | $2.16 | $4.32 |
| Reframe, per source second | $0.06 | $0.12 | $0.36 |

Draft 360p and higher edit HDR/EXR rates are also documented; do not extrapolate them. Single-keyframe extend costs the five-second SDR generation price for its resolution. The pricing page says rates may change ahead of general availability. Source: [Agents API pricing](https://docs.agents.lumalabs.ai/guides/pricing).

Before a paid POST, create an approval record containing the canonical request SHA-256, model/type, all reference hashes or immutable IDs, current quoted price and timestamp, maximum USD, account/client, rights/consent, retention class, approver, and expiry. Fail closed on mutation, an expired or insufficient/non-finite maximum, unknown price, unsupported combination, or unapproved media.

### Example: dry-run-first, single-attempt submission

The current API documents `X-Request-Id` for tracing but **does not document it as an idempotency key**. This example makes exactly one POST after an atomic claim. An ambiguous network outcome is recorded and must not be blindly retried.

```python
import hashlib
import json
import math
import os
import urllib.error
import urllib.request
from decimal import Decimal, InvalidOperation
from pathlib import Path

API = "https://agents.lumalabs.ai/v1/generations"
PRICE = Decimal("0.30")  # 720p SDR 5s, verified 2026-07-10; recheck before execute.
body = {
    "model": "ray-3.2",
    "type": "video",
    "prompt": "Static wide shot of silver grass moving in dawn wind, soft fog, natural documentary light.",
    "aspect_ratio": "16:9",
    "video": {"resolution": "720p", "duration": "5s"},
}
canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
digest = hashlib.sha256(canonical).hexdigest()
state_path = Path(os.environ.get("LUMA_STATE", f"luma-{digest}.json"))
print(json.dumps({"sha256": digest, "estimated_usd": str(PRICE), "request": body}, indent=2))

if os.environ.get("EXECUTE") != "1":
    raise SystemExit("DRY RUN: approve the digest, then set EXECUTE=1")
if os.environ.get("APPROVED_SHA256") != digest:
    raise SystemExit("approval digest mismatch")
try:
    maximum = Decimal(os.environ["APPROVED_MAX_USD"])
except (KeyError, InvalidOperation):
    raise SystemExit("missing or invalid approved maximum")
if not math.isfinite(float(maximum)) or maximum < PRICE:
    raise SystemExit("approved maximum is non-finite or insufficient")
token = os.environ.get("LUMA_AGENTS_API_KEY", "")
if not token.startswith("luma-api-"):
    raise SystemExit("missing current Agents API key")

claim = {"state": "SUBMITTING", "request_sha256": digest, "x_request_id": f"req-{digest[:32]}"}
fd = os.open(state_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
with os.fdopen(fd, "w", encoding="utf-8") as handle:
    json.dump(claim, handle, indent=2)
    handle.flush()
    os.fsync(handle.fileno())

def save(value):
    temp = state_path.with_name(state_path.name + ".tmp")
    temp_fd = os.open(temp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(temp_fd, "w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, state_path)

request = urllib.request.Request(
    API,
    data=canonical,
    method="POST",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Request-Id": claim["x_request_id"],
    },
)
try:
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 201:
            raise RuntimeError(f"unexpected HTTP {response.status}")
        result = json.loads(response.read(1_000_000))
        claim.update(state="SUBMITTED", generation_id=result["id"])
except urllib.error.HTTPError as exc:
    # A 4xx response rejects the request. A 5xx can arrive after the service
    # accepted it, so preserve uncertainty and reconcile before any retry.
    state = "REJECTED" if 400 <= exc.code < 500 else "UNKNOWN"
    claim.update(state=state, http_status=exc.code)
    save(claim)
    raise SystemExit(
        f"HTTP {exc.code}; claim is {state}; inspect and reconcile before any new attempt"
    )
except Exception as exc:
    claim.update(state="UNKNOWN", error_type=type(exc).__name__)
    save(claim)
    raise SystemExit("submission outcome unknown; do not repeat POST—escalate with X-Request-Id")
save(claim)
print(json.dumps(claim, indent=2))
```

Persist the returned generation ID before polling. A trace ID helps support locate an attempt; it does not prove deduplication. The current Agents API exposes create and get, not a list-generations recovery endpoint, so an ambiguous response without an ID requires fail-closed support reconciliation.

## Operate, retrieve, and govern artifacts

Poll every 2–5 seconds with a deadline and bounded jitter. States are `queued`, `processing`, `completed`, and `failed`. Respect the account-specific RPM and concurrent-job limits shown in the dashboard and `X-RateLimit-*` response headers. On 429, distinguish `Rate limit exceeded` from `Too many concurrent jobs` and honor `Retry-After`; never turn a retry loop into duplicate paid creates.

Output URLs are presigned for one hour. Re-polling mints a fresh URL; the generation ID is the durable lookup handle, but the reviewed public docs publish no ID-expiry guarantee. Download promptly from the URL returned by an authenticated GET, enforce a local byte cap, and never expose the presigned URL as a durable end-user link.

Files API uploads are reusable by `file_id`, account-scoped, and may set `expires_at`; presigned upload supports declared files up to 5 GiB. Delete is a soft delete that prevents future references. Current Agents docs expose file deletion but no generation-deletion endpoint or guaranteed generation-storage TTL. For deletion/export needs, use the documented support channel and contract rather than assuming URL expiry deletes the asset.

Before promotion:

- preserve request, digest, approval, trace ID, generation ID, source/file IDs and hashes, model/type, price snapshot, and raw terminal response;
- download each MP4/EXR with a cap, reject HTML/error bodies, verify file signatures, probe and fully decode;
- confirm requested duration, dimensions/aspect, expected SDR/HDR metadata, frame cadence, and whether audio is present before making any audio claim;
- inspect identity, anatomy, object permanence, camera continuity, flicker, text, brand/product accuracy, edits, and reframe seams;
- hash originals, store in controlled durable storage, publish atomically without overwrite, and record every transcode or grade as a derivative.

Sources: [Files API](https://docs.agents.lumalabs.ai/guides/files/), [rate limits](https://docs.agents.lumalabs.ai/guides/rate-limits/), [error handling](https://docs.agents.lumalabs.ai/guides/error-handling/).

## Rights, privacy, safety, and disclosure

Use only media, likenesses, performances, brands, and locations you are authorized to submit and transform. Obtain documented consent for identifiable people and digital replicas. Do not use the service for deceptive deepfakes, impersonation, political manipulation, sexual content, child exploitation, fraud, harassment, or misleading provenance. Luma’s API terms require downstream API users to receive at least equivalent restrictions, reasonable moderation/abuse controls, and notice that output is AI-generated.

The April 2026 API Terms state that Luma will not use API input or output to train or develop its models and say those API Terms control over conflicting general Terms for governed API access. However, the current Agents pricing comparison labels pay-as-you-go as lacking a no-training guarantee while Provisioned Throughput has one. Treat this first-party conflict as unresolved: do not promise pay-as-you-go no-training for sensitive workloads without written confirmation from Luma; use confirmed enterprise/provisioned terms where the guarantee matters. Do not extend either statement automatically to the consumer App or legacy/free workflows. Luma still processes data to provide the service, enforce policy, bill, support, and operate storage. Public URL inputs also expose media to the hosting path. Use Files API or controlled short-lived URLs for private assets, minimize PII in prompts/user IDs/logs, and obtain enterprise terms when region, residency, retention, confidentiality, or deletion guarantees are required.

The current Agents docs publish one global base URL and do not publish a selectable processing Region or a comprehensive data-residency map. Do not claim US/EU pinning. Ask Luma for a written enterprise answer before regulated or residency-bound use.

Sources: [API Terms](https://lumalabs.ai/legal/api-terms-of-use), [Terms of Service](https://lumalabs.ai/legal/terms-of-service), [Content Moderation Policy](https://lumalabs.ai/legal/content-moderation-policy), [Privacy Policy](https://lumalabs.ai/legal/privacy-policy).

## Final release gate

- Surface, model, schema, price, API version, and account limits reverified.
- Complete media rights, likeness consent, downstream terms, and intended-use review recorded.
- Exact digest and finite cost approval match the submitted bytes.
- Only one create attempt occurred; ID and trace are durable; unknown outcomes were not replayed.
- Inputs and Files objects have owners, hashes, TTL/deletion plans, and no unintended public exposure.
- Original MP4/EXR and terminal response are preserved and technically validated.
- Creative, identity, continuity, edit, reframe, safety, text, and brand QA passed.
- Audio is verified from the file or separately produced; no unsupported “native audio” claim is made.
- AI disclosure, provenance record, derivative lineage, retention, and deletion owner accompany delivery.
