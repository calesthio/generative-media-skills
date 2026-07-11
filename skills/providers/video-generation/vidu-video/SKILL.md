---
name: vidu-video
description: Plan and integrate ShengShu Vidu Open Platform video generation with current model/mode selection, reference consistency, pricing, exact approval, async task handling, and safe artifact custody. Use for Vidu API text-to-video, image-to-video, start/end-frame, multi-subject reference, media-reference, or Q2 multi-frame work; do not conflate the API with vidu.com consumer plans or Vidu-S1 streaming digital humans.
---

# Vidu video

Use this skill to design a production request or integration for the **Vidu Open Platform API**. Default to dry-run planning. Never submit a paid generation, upload private media, cancel a task, or download a result until the operator has approved the exact provider, endpoint, model, inputs, request digest, maximum charge, storage destination, and disclosure plan.

This document was verified against first-party public documentation on **2026-07-10**. Models, prices, accepted fields, policies, and availability are volatile; re-open the linked endpoint and pricing pages immediately before execution.

## Keep the surfaces separate

- **Open Platform API:** `https://api.vidu.com`, API keys, organization-level limits, asynchronous tasks, and API credits. This is the surface covered here.
- **Vidu consumer product:** `https://www.vidu.com` and its subscription/plan credits. Do not assume its credits, features, watermark behavior, or terms apply to the API.
- **Vidu-S1 (Beta):** a separate interactive digital-human product using HTTP session setup, AliRTC media, and WebSocket control. It is not a Q3/Q2 clip model. Its public page currently mixes “1 minute to 2 hours” marketing language with a 600-second session maximum. Its pricing section separately says 3 S1 credits per 2 seconds, lists a `0.03125` credit unit price, deducts every 6 seconds, rounds to 2-second intervals, and requires at least 45 credits to create a session. Do not revalue those statements using the clip API's `$0.005` credit price without written confirmation.
- **S1 documentation conflict:** Step 3 says browser WebSocket authentication belongs in the URL query because browsers cannot set custom headers, while the page's Important Notes says it must be in an authorization header. Treat this as unresolved. Confirm the current transport with Vidu before implementation, never place a bearer URL in logs/analytics/referrers, and do not infer a secure browser design from the sample alone.
- **China host:** the S1 page documents `api.vidu.cn` for China and `api.vidu.com` internationally. The ordinary clip endpoints documented here use `api.vidu.com`; do not infer compute residency from the hostname.

## Choose a mode first, then a model

The endpoint contract is more authoritative than a family name. A model may exist without supporting every mode.

| Need | Endpoint | Production-safe current choices | Important limits |
|---|---|---|---|
| Prompt only | `POST /ent/v2/text2video` | `viduq3-turbo`, `viduq3-pro`; Q2/Q1 only for a documented compatibility need | Q3: 1–16 s, 540p/720p/1080p; aspect `16:9`, `9:16`, `3:4`, `4:3`, `1:1` |
| Animate one start image | `POST /ent/v2/img2video` | Q3 pro-fast/turbo/pro; Q2 pro-fast/pro/turbo; Q1; Vidu 2.0 | Exactly one image; URL or data URL; PNG/JPEG/JPG/WebP; ratio strictly within 1:4–4:1; ≤50 MB; entire POST body ≤20 MB |
| Bridge exact start and end | `POST /ent/v2/start-end2video` | Q3 turbo/pro; Q2 pro-fast/pro/turbo; Q1/classic; Vidu 2.0 | Exactly two ordered images; their aspect-ratio ratio must be 0.8–1.25; Q3 1–16 s; Q2 endpoint documents 1–8 s |
| Named entities / dialogue | `POST /ent/v2/reference2video`, `subjects` form | The page's accepted list is Q3 turbo, Q3, Q2, Q1, Vidu 2.0 | ≤7 total image/text subject items; ≤3 images per subject; reference with `@name`; Q3 duration 3–16 s |
| Unnamed reference images | Same endpoint, `images` form | Q3 mix/turbo/Q3, Q2 pro/Q2, Q1, Vidu 2.0 | 1–7 images normally; Q2-pro allows 1–4 images when videos are also supplied |
| Reference video / edit | Same endpoint, `videos` form | `viduq2-pro` only | At most one 8 s video or two 5 s videos; MP4/AVI/MOV; ≤100 MB each; decoded base64 <20 MB |
| Multi-keyframe continuity | `POST /ent/v2/multiframe` | `viduq2-pro`, `viduq2-turbo` only | Ordered keyframes; each segment duration 2–7 s; 540p/720p/1080p; verify the current page because its frame/segment counting and pricing prose are ambiguous |

### Current family map

- **Q3 pro:** quality-oriented prompt/image/start-end generation, 24 fps, 1–16 s, 540p/720p/1080p, optional direct audiovisual output.
- **Q3 turbo:** cheaper/faster Q3 option across prompt/image/start-end and reference generation. Use it for first motion tests unless the brief justifies pro.
- **Q3 pro-fast:** documented for image-to-video only, 720p/1080p, 1–16 s. Its “fast” name does not mean it is cheaper than turbo at every setting.
- **Q3 mix:** direct `images` reference-to-video only; 720p/1080p. The pricing table says 3–16 s while the endpoint prose says 1–16 s. Use the safe intersection, **3–16 s**, until Vidu resolves the conflict. It does not currently support the named-entity `subjects` form or off-peak.
- **Q3 (unqualified):** reference-to-video model with synchronized audio support. Do not silently replace it with Q3 pro: they are different accepted identifiers on the reference endpoint.
- **Q2 pro:** use when actual reference videos, video editing/replacement, or Q2 multi-frame is required. Q2 turbo/pro-fast cover their documented image/start-end/multi-frame roles. Q2 and Q3 parameters are not interchangeable.
- **Q1/classic and Vidu 2.0:** older compatibility choices with fixed or narrower durations/resolutions. Public docs do not publish an end-of-life date; call them older, not deprecated.

The public [Model Map](https://platform.vidu.com/docs/model-map) lags some endpoint pages: for example, it does not enumerate all newer Q3 reference identifiers. Resolve conflicts in this order: the exact endpoint accepted-values list, the current [Pricing page](https://platform.vidu.com/docs/pricing), then the model map/update notice. If those still conflict, stop and confirm in the signed-in console or with Vidu support.

## Audio is endpoint- and model-specific

- On Q3 generation, `audio: true` asks for synchronized generated speech/effects; the reference `subjects` form also supports `audio_type` (`all`, `speech_only`, `sound-effect_only`) and per-subject `voice_id`.
- Q3 does not use `bgm`; do not set both and assume a mix. `voice_id` is documented ineffective on Q3 image-to-video.
- Defaults differ by page and form. Set `audio` explicitly. For a visual-motion test use `false`; for approved dialogue use named subjects, exact quoted lines, and `audio_type`.
- Q2 audio pricing and availability differ; the pricing page currently adds 15 credits to Q2 image/reference tasks that enable audio.
- Vidu's text-to-audio, TTS, voice cloning, lip sync, and digital-human APIs are separate capabilities. Do not send their fields to a video endpoint.

## Build references that the model can use

Facts from the endpoint contract:

- Subject images must be at least 128×128, within 1:4–4:1, and PNG/JPEG/JPG/WebP. Each named subject accepts up to three images.
- Q3 mix does not support named entities. Q2-pro is the only listed model accepting reference videos in the media-list form.
- `subjects[].name` is invoked as `@name` in the prompt. `auto_subjects` is a separate intelligent-entity-library option; do not enable it without knowing which library assets are selected.

Production heuristics, not provider guarantees:

1. Give each person/object a unique, stable name and 2–3 clean views with consistent wardrobe, age, materials, and lighting. Avoid group photos as identity references.
2. Put identity and must-not-change traits before action: `@Mara, red linen coat, short black bob; coat and face remain unchanged.`
3. Describe one shot's subject → action → environment → camera → light → audio. Too many cuts or simultaneous actions increase identity drift.
4. Use start/end for geometry or pose endpoints; use subject references for identity; use multi-frame for a deliberately staged sequence. Do not use prompt prose as a substitute for the appropriate control mode.
5. Test at 540p/720p and short duration with a fixed seed. Approve motion and identity before paying for 1080p or a longer clip. A seed helps comparison but does not guarantee bitwise reproducibility across model updates.

Stage inputs before request construction:

- Build a canonical input manifest with a logical asset ID, SHA-256 of the actual approved bytes, byte count, detected media type, dimensions/duration where relevant, rights/consent record, and authorized locator. A URL is only a locator; hashing the URL does not prove which bytes Vidu will fetch. Reject mutable or unhashable source content.
- If the integration dereferences a user URL while hashing or staging, allow HTTPS only; reject userinfo, fragments, loopback/private/link-local/metadata destinations, DNS rebinding, and unapproved ports; cap redirects and revalidate every hop; enforce time and byte limits. Send Vidu an approved read-only staged URL rather than relaying an arbitrary user URL.
- Scope signed source URLs to one object and the minimum useful lifetime. Keep query strings out of logs and approval displays. Do not expose a bucket prefix, listing permission, or reusable write credential.
- The separate Image Upload flow is a consequential three-step write (create link, `PUT`, finish) and currently documents an image limit below 10 MB, unlike the generation pages' 50 MB file limit and 20 MB request-body limit. Obtain separate approval, validate bytes before upload, record the returned ETag/URI, and do not infer a retention or deletion SLA from the example's storage headers.

### Complete example 1 — named dialogue subjects

**Intent and constraints:** Keep one actor and one designed object identifiable during a six-second rainy-market dialogue shot. Use the `subjects` form because the prompt names entities with `@name`; use Q3 Turbo, normal mode, 720p, and explicit audiovisual controls for a low-cost identity test. This is a schema illustration only; do not run it without exact approval.

```json
{
  "model": "viduq3-turbo",
  "auto_subjects": false,
  "subjects": [
    {
      "name": "Mara",
      "images": [
        "https://assets.example.test/mara-front.jpg",
        "https://assets.example.test/mara-three-quarter.jpg"
      ],
      "voice_id": "APPROVED_VOICE_ID"
    },
    {
      "name": "OrchidDrone",
      "images": ["https://assets.example.test/orchid-drone.png"]
    }
  ],
  "prompt": "@Mara walks beside @OrchidDrone through a rainy market. Their designs remain unchanged. One continuous medium tracking shot. @Mara says: 'We leave before sunrise.' Rain and footsteps only after the line.",
  "duration": 6,
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "audio": true,
  "audio_type": "all",
  "seed": 18427,
  "off_peak": false,
  "payload": "job-20260710-shot-014"
}
```

**Expected quote and result:** At the current normal Q3 Turbo reference rate, `6 × 10 = 60` API credits, or `$0.30` before tax. Expect one continuous tracking shot with the approved line and ambience, not guaranteed identity or verbatim speech.

**Review and repair:** Reject face/object drift, an unapproved voice, changed wording, extra music, or cuts. First simplify action/camera and retest the same short setting; use `speech_only` only when the brief does not require rain/footsteps, and obtain a new digest and approval for every changed request.

### Complete example 2 — fixed start and end

**Intent and constraints:** Transform one cleared paper-bird frame into a second cleared flight frame while locking the background and camera. Start/end mode is the correct control because both endpoint compositions matter. Q3 Pro, 5 seconds, 1080p, silent, normal mode is a quality-oriented approved variant.

```json
{
  "model": "viduq3-pro",
  "images": [
    "https://assets.example.test/shot-08-start.png",
    "https://assets.example.test/shot-08-end.png"
  ],
  "prompt": "The paper bird unfolds into flight while the locked camera remains still; preserve the cream background and cobalt ink texture.",
  "duration": 5,
  "resolution": "1080p",
  "audio": false,
  "seed": 9081,
  "off_peak": false,
  "payload": "job-20260710-shot-008"
}
```

**Expected quote and result:** `5 × 24 = 120` API credits, or `$0.60` before tax. Expect interpolation toward the supplied end, not an exact geometric morph.

**Review and repair:** Reject an end-frame snap, topology break, camera motion, or background redesign. Make the two source frames more compatible before lengthening; a cheaper Q3 Turbo 720p motion test is a meaningful variation but requires a new request and approval.

### Complete example 3 — unnamed product references

**Intent and constraints:** Use three cleared product views to preserve an unnamed lamp across a five-second rotation. Use the direct `images` form and Q3 Mix because named `subjects` are not supported. Five seconds is inside the documented 3–16-second pricing range and the endpoint's broader 1–16-second prose.

```json
{
  "model": "viduq3-mix",
  "images": [
    "https://assets.example.test/product-front.png",
    "https://assets.example.test/product-side.png",
    "https://assets.example.test/product-detail.png"
  ],
  "prompt": "The same brass desk lamp rotates slowly on a dark walnut table, one continuous product shot, no redesign, no text or logos added.",
  "duration": 5,
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "seed": 22109,
  "off_peak": false,
  "payload": "job-20260710-product-003"
}
```

**Expected quote and result:** `5 × 24 = 120` API credits, or `$0.60` before tax. Q3 Mix has no listed off-peak rate. The media-list request schema does not currently document an `audio` request field even though the model description mentions audiovisual output, so do not invent the field or promise silence; inspect the returned streams and confirm with Vidu if audio state is consequential.

**Review and repair:** Reject product redesign, added text/logo, missing details, multi-shot cuts, or unexpected audio. Improve reference consistency/crops before adding more images. Q3 Turbo reference at 720p is the lower-cost variation; changing models requires a new quote, digest, and approval.

## Price and approval

API credits currently cost **$0.005 each**, before applicable tax. On 2025-11-03 Vidu multiplied the numerical denomination by 10 without changing value; ignore pre-adjustment credit examples.

Selected current normal/off-peak rates per generated second:

| Model/mode | 540p | 720p | 1080p |
|---|---:|---:|---:|
| Q3 pro prompt/image/start-end | 9 / 5 credits | 20 / 10 | 24 / 12 |
| Q3 turbo prompt/image/start-end | 7 / 4 | 11 / 6 | 13 / 7 |
| Q3 pro-fast image | — | 20 / 10 | 25 / 13 |
| Q3 mix reference | — | 24 / no off-peak | 29 / no off-peak |
| Q3 turbo reference | 4 / 2 | 10 / 5 | 13 / 7 |
| Q3 reference | 7 / 4 | 12 / 6 | 15 / 7 |

Example: Q3 turbo text-to-video, 5 s, 720p, normal = `11 × 5 = 55 credits = $0.275` before tax. Q3 pro, 5 s, 1080p, normal = `24 × 5 = 120 credits = $0.60`.

`off_peak: true` is cheaper but may take up to 48 hours; unfinished tasks are automatically cancelled and refunded. Compatibility is conditional: the reference page says Q3 can use off-peak with audio, while Q2/Q1/Vidu 2.0 require audio false; Q3 mix has no off-peak price. Confirm the exact row before approval.

An approval record must include:

```text
provider=Vidu Open Platform API
endpoint=/ent/v2/text2video
model=viduq3-turbo
mode=normal (off_peak=false)
duration=5s resolution=720p aspect=16:9 audio=false
input_manifest_sha256=<hash of canonical prompt/source-byte hashes, byte counts, media facts, and logical IDs; URLs are locators only>
request_sha256=<hash of canonical final JSON body>
execution_manifest_sha256=<hash binding method, URL, non-secret key ID, input/request hashes, pricing date, expected/max charge, call count, retries, and destination>
pricing_verified_on=<UTC date rechecked against pricing page/console>
expected=55 API credits / USD 0.275 before tax
max_authorized_credits=55
max_authorized_usd=<operator ceiling>
allowed_calls=1; retries=0; destination=<approved path/bucket>
```

The input-manifest digest must cover source bytes and media facts, not merely locator strings. The execution-manifest digest is the approval token: changing an endpoint, API-key identity, body, source, price, ceiling, call count, retry policy, or destination invalidates approval.

If the pricing page or console quote exceeds either ceiling, stop before submission. If the one allowed create returns a different credit charge, persist the task ID and a billing-exception state, make no further generation/cancellation call, and reconcile the receipt with Vidu. Do not reinterpret a general budget as authorization for another model, retry, upscale, prompt recommendation (`is_rec` currently adds 10 credits), or Q2 audio surcharge.

## Dry-run-first, one-call example

This standard-library Python example is intentionally fixed to the 55-credit request above. Default mode prints the canonical request and approval envelope and makes **no network call and no state write**. Rerun dry-run with the real non-secret key ID, destination, ceiling, pricing-verification date, and fresh client request ID before approval. Execution requires the exact execution-manifest digest and claims the request-body digest before the one POST. Because Vidu documents no idempotency key, any exception after transmission becomes `UNKNOWN`; the script never retries. Use a transactional datastore rather than this local-file illustration when multiple hosts or processes can submit.

```python
import datetime, hashlib, json, os, pathlib, sys, urllib.error, urllib.request
from decimal import Decimal

MODE = os.getenv("VIDU_MODE", "dry-run")
client_id = os.getenv("VIDU_CLIENT_REQUEST_ID", "dryrun-example")
endpoint = "https://api.vidu.com/ent/v2/text2video"
key_id = os.getenv("VIDU_KEY_ID", "UNBOUND")
destination = os.getenv("VIDU_DESTINATION", "UNSET")
pricing_verified_on = os.getenv("VIDU_PRICING_VERIFIED_ON", "UNVERIFIED")
body = {
    "model": "viduq3-turbo",
    "prompt": "A cobalt paper bird unfolds and glides across a cream studio background, one locked medium shot, preserve its ink texture.",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "audio": False,
    "seed": 18427,
    "off_peak": False,
    "payload": client_id,
}
wire = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
digest = hashlib.sha256(wire).hexdigest()
input_manifest = {"kind": "text-only", "prompt_sha256": hashlib.sha256(body["prompt"].encode("utf-8")).hexdigest()}
input_digest = hashlib.sha256(json.dumps(input_manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
expected_credits = 55
expected_usd = Decimal("0.275")
max_authorized_credits = int(os.getenv("VIDU_MAX_CREDITS", str(expected_credits)))
max_authorized_usd = Decimal(os.getenv("VIDU_MAX_USD", str(expected_usd)))
approval_manifest = {
    "provider": "Vidu Open Platform API", "method": "POST", "url": endpoint,
    "key_id": key_id, "input_manifest_sha256": input_digest, "request_sha256": digest,
    "pricing_verified_on": pricing_verified_on, "expected_credits": expected_credits,
    "expected_usd_before_tax": str(expected_usd), "max_authorized_credits": max_authorized_credits,
    "max_authorized_usd": str(max_authorized_usd),
    "allowed_calls": 1, "retries": 0, "destination": destination,
}
approval_wire = json.dumps(approval_manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
approval_digest = hashlib.sha256(approval_wire).hexdigest()
print(json.dumps({"mode": MODE, "execution_manifest_sha256": approval_digest,
                  "approval_manifest": approval_manifest, "input_manifest": input_manifest,
                  "body": body}, indent=2, ensure_ascii=False))
if MODE == "dry-run":
    raise SystemExit(0)
if MODE != "execute":
    raise SystemExit("VIDU_MODE must be dry-run or execute")
if client_id == "dryrun-example":
    raise SystemExit("Set a fresh VIDU_CLIENT_REQUEST_ID")
if key_id == "UNBOUND" or destination == "UNSET":
    raise SystemExit("Bind the non-secret key ID and destination before approval")
try:
    verified_date = datetime.date.fromisoformat(pricing_verified_on)
except ValueError:
    raise SystemExit("Set VIDU_PRICING_VERIFIED_ON to an ISO date")
if verified_date != datetime.datetime.now(datetime.timezone.utc).date():
    raise SystemExit("Pricing must be revalidated on the UTC submission date")
if os.environ.get("VIDU_APPROVED_MANIFEST_SHA256") != approval_digest:
    raise SystemExit("Exact execution manifest was not approved")
if max_authorized_credits < expected_credits or max_authorized_usd < expected_usd:
    raise SystemExit("Approved ceiling is below expected cost")
api_key = os.environ.get("VIDU_API_KEY", "")
if not api_key:
    raise SystemExit("VIDU_API_KEY is required")

state_dir = pathlib.Path(os.getenv("VIDU_STATE_DIR", ".vidu-state")).resolve()
state_dir.mkdir(parents=True, exist_ok=True)
state_path = state_dir / f"{digest}.json"
def replace_state(value):
    temp = state_path.with_suffix(f".tmp-{os.getpid()}")
    with open(temp, "x", encoding="utf-8") as f:
        json.dump(value, f)
        f.flush(); os.fsync(f.fileno())
    os.replace(temp, state_path)
try:
    fd = os.open(state_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
except FileExistsError:
    raise SystemExit("Digest already claimed; refusing a duplicate POST")
with os.fdopen(fd, "w", encoding="utf-8") as f:
    json.dump({"state": "PREPARED", "request_sha256": digest,
               "execution_manifest_sha256": approval_digest, "client_request_id": client_id}, f)
    f.flush(); os.fsync(f.fileno())

req = urllib.request.Request(
    endpoint, data=wire, method="POST",
    headers={"Authorization": f"Token {api_key}", "Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=45) as resp:
        raw = resp.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise RuntimeError("response exceeds 1 MiB")
        if resp.status not in (200, 201):
            raise RuntimeError(f"unexpected HTTP {resp.status}")
        result = json.loads(raw)
        task_id = result.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            raise RuntimeError("successful response lacks task_id")
        charged_credits = result.get("credits")
        if not isinstance(charged_credits, int) or isinstance(charged_credits, bool):
            raise RuntimeError("successful response lacks an integer credits receipt")
except Exception as exc:
    replace_state({"state": "UNKNOWN", "request_sha256": digest,
        "execution_manifest_sha256": approval_digest,
        "client_request_id": client_id, "error_type": type(exc).__name__})
    raise SystemExit("POST outcome is UNKNOWN; do not retry. Reconcile in Vidu console/support.") from exc
final_state = "SUBMITTED" if charged_credits == expected_credits and charged_credits <= max_authorized_credits else "SUBMITTED_BILLING_EXCEPTION"
replace_state({"state": final_state, "request_sha256": digest,
    "execution_manifest_sha256": approval_digest,
    "client_request_id": client_id, "task_id": task_id, "charged_credits": charged_credits})
print(json.dumps({"task_id": task_id, "state": final_state,
                  "next": f"GET /ent/v2/tasks/{task_id}/creations"}))
if final_state != "SUBMITTED":
    raise SystemExit("Task was created with a credit variance; do not submit or cancel anything else")
```

The local `payload` is echoed on the task but is not documented as a searchable Task List filter. On an ambiguous create, compare console/task history around the precise submission time, model, prompt, duration, resolution, key, and local client ID; involve Vidu support if needed. Do not issue a replacement until the original outcome is proven non-created or the operator explicitly approves duplicate risk and cost.

## Operate the asynchronous task safely

1. Persist `task_id`, canonical request, digest, API key identifier (not the secret), expected ceiling, and create response.
2. Poll `GET /ent/v2/tasks/{id}/creations` with bounded exponential backoff and jitter. States are `created`, `queueing`, `processing`, `success`, `failed`. Do not treat a client timeout as task failure.
3. The public default is **five concurrent tasks per organization**, not per key. Extra tasks queue roughly in creation order; the service may run below the maximum under load. `429` also covers too-frequent requests/system throttling, so back off reads. Do not flood the queue merely because submissions are accepted.
4. A successful task returns charged `credits` and `creations[].{id,url,cover_url}`. A failed task returns `err_code`; store the trace ID from structured errors. Policy failures are not prompt bugs to evade.
5. Cancellation is a consequential POST to `/ent/v2/tasks/{id}/cancel`; it may fail once a task reaches a non-cancellable state. Obtain task-specific authorization and then confirm terminal state/refund rather than assuming `{}` proves billing reversal.

Callbacks are optional. Vidu retries failed callback delivery three times, so handlers must be idempotent. Verify `X-HMAC-ALGORITHM=hmac-sha256`, access key `vidu`, Date freshness, and the exact ordered signed-header list before accepting the body. Reconstruct:

```text
METHOD + "\n" + URI_PATH + "\n" + RAW_QUERY + "\n" + "vidu" + "\n" + DATE + "\n"
+ each "HeaderName:HeaderValue\n" in X-HMAC-SIGNED-HEADERS order
signature = base64(HMAC-SHA256(callback TokenSecret, signing_string))
```

Use constant-time comparison, retain a short-lived `(access_key, nonce)` replay cache, reject stale Dates, cap the raw body, parse only after signature verification, and require a known task ID plus a schema-valid state transition before accepting an event. Store the raw-event hash and resulting state durably before acknowledging. Keep polling as recovery because callback delivery is not exactly once. Use the callback credential identified by Vidu as the application's TokenSecret; do not guess that any bearer key is interchangeable.

## Take custody and validate

Creation and cover URLs are documented as valid for only **24 hours**. On success, immediately copy them to the approved destination using a downloader that enforces HTTPS, approved host/redirect policy, public-IP resolution on every hop, timeouts, byte ceilings, and streaming hashes. Write to a newly created quarantine file beneath a fixed destination root; reject traversal, symlink/reparse-point escapes, overwrite, and content-type/byte-signature mismatches. Never log signed query strings.

For each clip:

- preserve Vidu task/creation IDs, final request, charged credits, URLs redacted, receipt time, SHA-256, byte count, and provenance/disclosure metadata;
- require an expected video content type, then use `ffprobe` to verify container, codec, actual width/height, fps, duration, and audio-stream presence;
- perform a full decode, not just a metadata probe; reject HTML/error bodies, truncated media, duration/resolution surprises, and unexpected executable/archive content;
- review every frame range for identity drift, extra limbs/objects, unsafe text/logos, cuts, flicker, and start/end compliance; review audio for exact speech, unwanted voices, music, and intelligibility;
- quarantine failures. Do not overwrite a previously accepted artifact. Preserve the source generation separately from any edit/upscale.

## Rights, privacy, disclosure, and unknowns

- Obtain documented rights and consent for every face, voice, trademark, copyrighted work, confidential file, and personal-data field. Do not create deceptive impersonation, non-consensual intimate content, harassment, fraud, or prohibited material.
- The API Terms require operators to inform end users, obtain necessary consent, minimize personal data, perform human review, avoid solely relying on outputs, and not use person-related output for material/legal decisions. They also prohibit removing, falsifying, or covering signs that distinguish deep-synthesis output and prohibit presenting it as human-made. Preserve Vidu's provenance/deep-synthesis markings and add appropriate visible disclosure.
- Vidu says it may monitor or review input/output for operation and policy enforcement. Its privacy policy covers user content, allows service-provider processing, gives purpose-based rather than fixed retention, and says personal data may be stored/transferred on servers in Singapore. This is not proof that all generation compute occurs there.
- Public docs do **not** provide a general API no-training promise, a fixed deletion SLA for all inputs/outputs, a complete compute-region map, output ownership assignment, model EOL dates, or an idempotency key. They publish five concurrent tasks but no single universal requests-per-minute figure. Resolve regulated, confidential, residency, ownership, indemnity, DPA, deletion, or training requirements in signed terms before upload.
- Vidu's 2024 [technical report](https://arxiv.org/abs/2405.04233) describes the historical U-ViT/diffusion Vidu system and an original 1080p/16 s claim. It predates Q3; do not use it to assert Q3 architecture, safety, training data, or benchmark performance.

## Troubleshoot without spending blindly

| Symptom | Check | Safe action |
|---|---|---|
| `401`/`403` | Header is exactly `Authorization: Token …`; key/account permissions | Fix auth; never print the key |
| `400 FieldInvalid` | Endpoint-specific model, duration, resolution, aspect, body size | Revalidate against that endpoint; dry-run a new digest |
| `400 ModelUnavailable` | Stale identifier or temporary availability | Stop; do not silently swap models |
| `429 QuotaExceeded` | Five-task organization concurrency or custom quota | Let queued/running work finish; request a limit change if needed |
| `429 TooManyRequests/SystemThrottling` | Poll/submission rate | Back off with jitter; respect any server guidance |
| `AuditSubmitIllegal` / `CreationPolicyViolation` | Input/output moderation | Stop and review rights/safety; do not obfuscate to bypass review |
| Long `queueing` | Concurrency or off-peak mode | Report the mode and age; off-peak has a 48-hour window |
| Success but URL fails | 24-hour link expired or unsafe redirect | Check task history; contact support if the artifact was not taken into custody |
| Wrong/no audio | Q3 `audio`, reference `audio_type`, voice mapping; Q3 ignores `bgm` | Correct schema, reprice, obtain new approval before another generation |

## Primary sources

- [Introduction](https://platform.vidu.com/docs/introduction), [Update Notice](https://platform.vidu.com/docs/update), [Model Map](https://platform.vidu.com/docs/model-map), [Pricing](https://platform.vidu.com/docs/pricing), [Usage and Limits](https://platform.vidu.com/docs/usage-and-limits)
- [Text to Video](https://platform.vidu.com/docs/text-to-video), [Image to Video](https://platform.vidu.com/docs/image-to-video), [Start End to Video](https://platform.vidu.com/docs/start-end-to-video), [Reference to Video](https://platform.vidu.com/docs/reference-to-video), [Multi-Frame](https://platform.vidu.com/docs/multi-frame)
- [Get Creation](https://platform.vidu.com/docs/get-generation), [Get Task List](https://platform.vidu.com/docs/tasks-list), [Cancel Generation](https://platform.vidu.com/docs/cancel-generation), [Error Code](https://platform.vidu.com/docs/error-code), [Callback Signature](https://platform.vidu.com/docs/callback-signature), [Image Upload](https://platform.vidu.com/docs/image-upload)
- [Terms of Use](https://platform.vidu.com/docs/terms-of-use), [Privacy Policy](https://platform.vidu.com/docs/privacy-policy), [Content Moderation](https://platform.vidu.com/docs/content-moderation), [Subprocessors](https://platform.vidu.com/docs/sub-processor), [Vidu-S1 Beta](https://platform.vidu.com/docs/vidu-s1), [consumer pricing](https://www.vidu.com/pricing), [2024 Vidu technical report](https://arxiv.org/abs/2405.04233)
