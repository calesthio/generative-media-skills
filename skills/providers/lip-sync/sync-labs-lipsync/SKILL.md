---
name: sync-labs-lipsync
description: >-
  Generate AI lip sync and visual dubbing with Sync Labs (sync.so) — choose the
  right model (sync-3, lipsync-2, lipsync-2-pro, lipsync-1.9.0-beta, react-1),
  build the POST /v2/generate request, host inputs, handle async jobs via polling
  or webhooks, run batch dubbing/localization, and review output for sync accuracy
  and identity preservation. Use when an agent must re-voice, dub, translate,
  personalize, or re-time the mouth of a talking-head video (or animate a still
  face from audio), or must debug a failed/rejected Sync generation. Also covers
  consent, likeness, and rights obligations for editing a real person's face.
---

# Sync Labs lip sync and visual dubbing

Sync Labs (product domain `sync.so`, API host `api.sync.so`) is a hosted API and web
studio that regenerates a speaker's mouth (and, on newer models, jaw/expression/head)
to match a new audio track. It does not generate whole people or scenes: the input is
an existing talking-head video (or, on `sync-3`, a single still face), plus target
audio (a file, a hosted URL, or text synthesized through an integrated TTS provider).
Everything outside the driven face region — background, body, hair, clothing — is left
untouched and composited around the regenerated face. (Documented: sync.so/docs
introduction and "how AI lip sync works", verified 2026-07-10.)

Use this skill when the job is: dubbing/localizing a video into another language,
re-timing lips to corrected or re-recorded audio (ADR-style), personalizing a base
video with per-recipient names, cutting podcast/interview clips with clean lips, or
animating a portrait photo from a voiceover. Do **not** reach for it to generate a
face from scratch, to swap identities, or to produce a full avatar from text alone —
those are different product categories.

## What the models are and how to choose

All model facts below are from sync.so/docs (models pages and pricing), verified
2026-07-10. Prices are quoted per second of **output** at 25 fps and move with plan
tier, so treat them as dated reference, not a contract.

| Model ID | Face resolution | Obstruction handling | Speed (docs) | Price/sec @25fps | Built for |
|---|---|---|---|---|---|
| `lipsync-1.9.0-beta` | face crop | none | ~3x real-time (fastest) | $0.02–0.025 | cheap, simple, frontal clips; generic mouth motion |
| `lipsync-2` | 512×512 crop | optional (`occlusion_detection_enabled`) | ~1x real-time | $0.04–0.05 | general-purpose default; preserves each speaker's style |
| `lipsync-2-pro` | 512×512 + diffusion super-res | optional | ~0.5–0.7x (1.5–2x slower than lipsync-2) | $0.067–0.083 | premium detail on beards, teeth, fine facial features |
| `sync-3` | 4K native, full-shot | automatic, built-in | fast (processes whole shot at once) | $0.107–0.133 | close-ups, profiles/extreme angles, partial faces, still-image input |
| `react-1` | expression/head editing | — | short clips only | (see pricing page) | change emotion, expression, and head motion, not just lips |

Decision guidance (heuristic, grounded in the documented capability differences):

- **Start at `lipsync-2`** for a normal, well-lit, roughly frontal talking head. It is
  the documented "most natural" general model and the cheapest of the current-quality
  tier. Escalate only for a reason.
- **Go to `lipsync-2-pro`** when the mouth region shows fine texture that a viewer will
  scrutinize — facial hair crossing the lips, visible teeth in close-up, high-bitrate
  footage where 512-crop softness would read as a downgrade. It is slower and ~1.7x the
  cost; do not pay for it on a wide shot where the face is small.
- **Go to `sync-3`** when the shot breaks the frontal-face assumption: profile/over-the-
  shoulder angles, a hand or mic crossing the mouth, a cropped/partial face, or a
  genuine 4K deliverable where a 512 crop composited back would be soft. `sync-3` also
  handles obstructions with **no** configuration and is the **only** model that accepts
  a **still image** as the visual input (JPEG/PNG/WebP) to animate a portrait from audio.
- **Use `lipsync-1.9.0-beta`** only for throwaway/high-volume/tight-budget work where
  generic lip motion is acceptable; its mouth shapes are not speaker-specific.
- **Use `react-1`** when the deliverable requires *acting*, not just sync — you want the
  same person re-performed happier/angrier/sadder with matching head motion. Inputs are
  capped at 15 seconds (documented hard limit) and it exposes an emotion prompt of
  `happy | sad | angry | disgusted | surprised | neutral`.

Documented limitation to plan around: **`lipsync-2` and `lipsync-2-pro` require natural
speaking motion in the input video.** A near-static frame (a locked-off portrait, a
person holding still) may not sync well on those models — that is exactly the case for
`sync-3` (which can "open silent lips naturally") or a still-image `sync-3` job.

## API shape

Documented facts below verified 2026-07-10 against sync.so/docs API reference.

- **Endpoint:** `POST https://api.sync.so/v2/generate`
- **Auth header:** `x-api-key: YOUR_API_KEY` (not a Bearer token; the SDK reads
  `SYNC_API_KEY` from the environment).
- **SDKs:** Python `pip install syncsdk` (import `from sync import Sync`), and a
  TypeScript SDK (`SyncClient`). Both wrap `generations.create()` / `generations.get()`.
- **Rate limit:** 100 requests/minute per key (documented). Concurrency (in-flight
  generations) is separately capped by plan tier — exceeding it returns
  `concurrency_limit_reached` (429), which is *not* the same as `rate_limit_exceeded`.
- **Runtime error catalog:** unauthenticated `GET https://api.sync.so/v2/errors` returns
  `{code, message, suggestion}` objects. Resolve any `errorCode` against it at runtime
  rather than hard-coding message strings.

### Request body

```json
{
  "model": "lipsync-2",
  "input": [
    { "type": "video", "url": "https://cdn.example.com/source.mp4" },
    { "type": "audio", "url": "https://cdn.example.com/newvoice.mp3" }
  ],
  "options": {
    "sync_mode": "cut_off",
    "temperature": 0.5,
    "active_speaker_detection": { "auto_detect": true },
    "occlusion_detection_enabled": false
  },
  "outputFileName": "dub_v1",
  "webhookUrl": "https://your.app/hooks/sync"
}
```

Field notes (documented):

- **`input`** — exactly **one** visual item (`video` **or** `image`; `image` only on
  `sync-3`) plus one audio source (`audio`, or a `text` TTS item, or `dubParams` — pick
  one path). Supplying two visuals returns `generation_input_too_many_visual`. Each item
  takes either `url` (any publicly reachable URL) or `assetId` (from the Assets API),
  and an optional `refId` used to wire it to the `segments` array. Video items may carry
  `segments_secs` / `segments_frames` to lipsync only sub-ranges.
- **`options.sync_mode`** — how a video/audio duration mismatch is reconciled:
  `silence` (pad audio with silence to fill the video), `cut_off` (trim the video to the
  audio length), `remap` (change video playback speed to match audio), `loop` (repeat the
  video), `bounce` (ping-pong the video forward/back). Ignored for image inputs. `cut_off`
  is the safe default for dubbing when the new voice is shorter and you don't want frozen
  tails; `remap` risks unnatural motion speed, so use it deliberately.
- **`options.temperature`** — 0.0–1.0, expressiveness of the generated mouth motion.
  Higher is more animated but can over-articulate; lower is calmer/more conservative.
  (Documented range; effect is a first-party parameter description.)
- **`options.active_speaker_detection`** — for multi-face frames. `{auto_detect: true}`
  lets the model pick the talking face; otherwise pin the speaker with `coordinates`,
  `bounding_boxes`, `bounding_boxes_url`, and/or `frame_number`. Without this, a
  multi-face clip can drive the wrong face. Active Speaker Detection is a paid-tier
  feature (Creator plan and up).
- **`options.occlusion_detection_enabled`** — on `lipsync-2` / `lipsync-2-pro`, turn on
  when hands/mics/hair cross the mouth. On `sync-3` it is automatic and this flag is
  unnecessary.
- **`options.model_mode`** — `lips | face | head` (region the model is allowed to edit;
  broader modes drive expression/head, relevant to `react-1`-style editing).
- **`options.prompt`** — emotion for `react-1`: `happy | sad | angry | disgusted |
  surprised | neutral`.
- **`segments`** — array of `{startTime, endTime, audioInput:{refId,...}, optionsOverride}`
  to apply different audio and per-segment options to different time ranges of one video
  (multi-speaker / multi-line dubbing in a single job).
- **`dubParams`** — automatic translation dubbing: `{providerName:"elevenlabs",
  sourceLang, targetLang, numSpeakers}`. It extracts the audio from the input video,
  translates, and re-voices; do **not** also pass a separate `audio`/`text` input (that
  returns `generation_input_dub_audio_conflict`). Documented target languages include en,
  es, fr, de, it, pt, pl, hi, zh, ja, ar, ru, ko, id, nl, tr, sv, fil, ms, ro, uk, el,
  cs, da, fi, bg, hr, sk, ta; `numSpeakers` 0–50.
- **`outputFileName`** — alphanumerics/underscores/hyphens only, `.mp4` appended.

### Response and job lifecycle

`POST` returns `201` with an `id` and `status`. Statuses: **`PENDING`** (queued) →
**`PROCESSING`** → terminal **`COMPLETED`** (`outputUrl` populated), **`FAILED`** (check
`error` + `errorCode`), or **`REJECTED`** (validation/policy rejection before processing).

Two ways to learn the outcome:

1. **Poll** `GET /v2/generate/{id}` (SDK `generations.get(id)`) at ~10 s intervals.
   `GET ...?wait=true` long-polls but caps at a 10-second server timeout — it is not a
   substitute for polling a long job.
2. **Webhooks (preferred for anything long):** pass `webhookUrl` (public HTTPS, must
   return 2xx quickly). Each delivery carries a `Sync-Signature: t={timestamp},v1={hmac}`
   header; verify by computing HMAC-SHA256 over `timestamp + rawBody` with your signing
   secret (`whsec_...`) and comparing timing-safely. **There is no automatic retry** on a
   failed delivery, so keep a polling fallback for reconciliation.

## Complete examples

### Example 1 — Localize an ad into Spanish with cloned voice (production dubbing)

*This is a worked example, not a required template.*

- **Intent:** dub a 45 s English product ad into Spanish, keeping the presenter's own
  voice character, delivering a clean 1080p MP4.
- **Model:** `lipsync-2` (frontal, well-lit presenter; no occlusion) — escalate to
  `sync-3` only if QA shows profile shots.
- **Inputs/constraints:** source video hosted at a public URL (over the 20 MB direct-
  upload limit, so URL not upload). Spanish audio produced by an ElevenLabs voice cloned
  from the presenter's own consented English audio (30+ s clean single-speaker sample).

```python
from sync import Sync
from sync.common import Video, Audio, GenerationOptions

sync = Sync()  # reads SYNC_API_KEY
job = sync.generations.create(
    input=[
        Video(url="https://cdn.example.com/ad_en_1080p.mp4"),
        Audio(url="https://cdn.example.com/ad_es_clonedvoice.wav"),
    ],
    model="lipsync-2",
    options=GenerationOptions(
        sync_mode="cut_off",          # ES track is shorter; trim video tail
        occlusion_detection_enabled=False,
        active_speaker_detection={"auto_detect": True},
    ),
    output_file_name="ad_es_v1",
)
# then poll job.id, or receive a webhook
```

- **Why structured this way:** `cut_off` avoids a frozen final frame when the translated
  line runs short. Voice is cloned from the *presenter's own* consented sample — the
  consent-first path. 1080p input keeps face detection reliable while the 512 crop
  composites back cleanly at that scale.
- **Expected result:** lips track the Spanish audio, presenter's cadence preserved, rest
  of frame identical to source.
- **Likely failures:** if the ES track is much longer than the video, `cut_off` will
  truncate speech — switch to `remap` (accept mild speed change) or re-time the script.
  If QA shows soft teeth in the close-up hero shot, re-run that shot on `lipsync-2-pro`.

### Example 2 — Multi-speaker dialogue dub in one job (segments)

*Example.* Two on-camera speakers, one 15 s clip, each line re-voiced by a distinct
cloned voice via integrated TTS, no separate audio hosting:

```python
job = sync.generations.create(
    input=[
        Video(url="https://cdn.example.com/interview.mp4"),
        TTS(provider={"name":"elevenlabs","voiceId":"voice_A","script":"Bienvenidos al programa."}, ref_id="a"),
        TTS(provider={"name":"elevenlabs","voiceId":"voice_B","script":"Gracias por recibirme."}, ref_id="b"),
    ],
    segments=[
        {"startTime": 0, "endTime": 8,  "audioInput": {"refId": "a"}},
        {"startTime": 8, "endTime": 15, "audioInput": {"refId": "b"}},
    ],
    model="lipsync-2",
)
```

- **Why:** `segments` binds each TTS line to a time range and (via active-speaker
  detection per segment if needed) the right face. Keeps a two-person scene in one job.
- **Failure modes:** overlapping/mis-timed segments return
  `generation_input_segments_invalid`; if both faces are visible per segment, add
  `active_speaker_detection` in `optionsOverride` to pin each speaker.

### Example 3 — Animate a still portrait from a voiceover (sync-3 only)

*Example.* Bring a single headshot to life reading a 20 s script:

```json
{
  "model": "sync-3",
  "input": [
    { "type": "image", "url": "https://cdn.example.com/headshot.png" },
    { "type": "audio", "url": "https://cdn.example.com/vo.mp3" }
  ],
  "outputFileName": "portrait_talk"
}
```

- **Why sync-3:** image input and "opening silent lips naturally" are `sync-3`-only.
  `sync_mode` is ignored for images (no intrinsic duration).
- **Failure mode:** a low-res or heavily stylized face may not track; use a clear,
  well-lit, roughly frontal headshot.

### Example 4 — Batch localization (Scale/Enterprise)

*Example.* Batch API accepts a **JSONL** file, one record per line, each a `/v2/generate`
body plus a unique `request_id`. Documented constraints: **20–1000 records** per batch,
file **≤5 MB**, endpoint must be `/v2/generate`, `request_id`s unique, Scale plan or
higher (`batch_plan_required` / 403 otherwise). Use it to fan out one video into many
target languages, or many personalized variants, without 1000 individual calls.

## Input requirements and constraints (documented, 2026-07-10)

- **Video containers:** MP4, MOV, WebM, AVI. **Codec:** H.264 gives best quality;
  H.265/MPEG-2 lose up to ~15%, VP9 ~20%, AV1 >20% (everything is transcoded to H.264,
  output re-encoded `libx264 -crf 17 -preset slow`). Prefer **MP4/H.264 in, 1080p**.
- **Resolution:** ≥480p required for reliable face detection; 1080p recommended;
  max 4K (4096×2160). Non-`sync-3` models extract the face at **512×512**, process it,
  and composite back — so an enormous input resolution does not raise face detail on
  those models; `sync-3` works at 4K natively.
- **Aspect ratio:** any (9:16, 16:9, 1:1, custom).
- **Frame rate:** constant 24/25/30 fps recommended.
- **Audio:** WAV/MP3 recommended (also OGG/FLAC/ALAC/MP4-audio fully supported;
  WMA/M4A/AAC limited). 44.1 or 48 kHz recommended; up to 32-bit float, up to 7.1 ch.
  **One speaker per audio track**, isolated from music/crowd noise.
- **Direct upload limit:** 20 MB (`413`/`file_size_exceeds_plan_limit`); above that, host
  at a public URL (no size cap) or use the Assets API (`POST /v2/assets/upload`).
- **Duration:** per-generation cap is **plan-bound** — Free 20 s, Hobbyist 1 min,
  Creator 5 min, Growth 10 min, Scale/Enterprise 30 min. Additional hard caps: `react-1`
  input ≤15 s; audio ≤300 s (5 min) per generation; TTS text ≤5000 characters.

## Pricing and plans (verified 2026-07-10; volatile)

Usage is metered per second of output; a subscription unlocks higher limits, features,
and usage discounts. Per-second model prices are in the model table above.

| Plan | Price/mo | Per-sec | Max length | Concurrent | Voice clones | Notable |
|---|---|---|---|---|---|---|
| Free | $0 | — | 20 s | — | — | 3 generations/month |
| Hobbyist | $5 | $0.05 | 1 min | 1 | 3 | API, SDKs, Studio |
| Creator | $19 | $0.05 | 5 min | 3 | 5 | no watermark, own TTS key, Active Speaker Detection |
| Growth | $49 | $0.0475 (5% off) | 10 min | 6 | 15 | batch API, 3 team seats |
| Scale | $249 | $0.04 (20% off) | 30 min | 15 | 50 | batch API, 5 seats, delegated support |
| Enterprise | custom | custom | custom | custom | custom | contract |

Note: the free/low tiers **watermark** output and cap concurrency to 1 — remove the
watermark by upgrading to Creator+. Batch API is Growth+ (`batch_plan_required` cites
Scale for the batch endpoint specifically — confirm your tier against the live error
catalog before building a batch pipeline).

## Reviewing lip sync output (quality gate)

Before shipping, check each of these — the first two are the ones that make output look
"AI", and they fail independently:

1. **Sync accuracy / timing.** Do mouth shapes land on the right phonemes, not early or
   late? Scrub plosives (b/p/m — lips must fully close) and open vowels. Drift that grows
   over a long clip usually means duration mismatch — revisit `sync_mode` (try `cut_off`)
   or split into <2-minute segments.
2. **Identity preservation.** Does it still look like the same person? Watch for a
   "smeared" or averaged mouth, lost lip shape, or a jaw that moves unlike the subject.
   On `lipsync-1.9.0-beta` expect generic (non-speaker-specific) motion by design.
3. **Mouth-region artifacts.** Inspect teeth (blurred/merged teeth are the classic
   `lipsync-2` tell — fix with `lipsync-2-pro`), the lip/skin seam (blend/color/lighting
   mismatch at the composite boundary), and beard/mustache continuity across the mouth.
4. **Occlusion handling.** If a hand, mic, or hair crosses the mouth, does the model paint
   through it (wrong) or respect it? If wrong on `lipsync-2/pro`, set
   `occlusion_detection_enabled=true`; if still wrong, move to `sync-3` (automatic).
5. **Wrong-face / multi-speaker.** Confirm the intended speaker was driven; if not, pin
   with active-speaker detection.
6. **Silent/static frames.** On `lipsync-2/pro`, a near-still input can under-sync — this
   is the documented "requires natural speaking motion" limit; move to `sync-3`.

## Failure modes and repair (from the documented error catalog, 2026-07-10)

Branch on `errorCode`, not the human `error` string, and read `field` to see which input
was rejected. Key cases and fixes:

- **`generation_input_face_selection_invalid`** ("selected face unusable") — re-run face
  detection / enable auto-detect, or improve face size/lighting/angle.
- **`generation_input_too_many_visual`** — you sent two visuals; send exactly one.
- **`generation_input_segments_invalid`** — segments overlap or have invalid times; make
  them non-overlapping with valid ranges.
- **`generation_input_dub_audio_conflict`** — you passed both `dubParams` and an
  audio/text input; choose one.
- **`generation_audio_length_exceeded`** / **`generation_text_length_exceeded`** — trim
  audio ≤300 s / text ≤5000 chars, or split.
- **`generation_plan_duration_exceeded` (402)** — output exceeds your plan's per-gen cap;
  upgrade, trim input, or use a shortening `sync_mode`.
- **`concurrency_limit_reached` (429)** vs **`rate_limit_exceeded` (429)** — the first
  means too many *in-flight* jobs (wait/upgrade); the second means too many *requests/min*
  (exponential backoff). Do not confuse them.
- **`generation_media_metadata_missing`** — audio needs `duration`; video needs
  `duration` + `frame_rate`. Re-encode with FFmpeg to embed metadata.
- **`REJECTED`** status — validation or **policy** rejection before processing; do not
  blindly retry, inspect the reason.
- **Transient** (`500/503/504`, `controller_*`, `generation_timeout`,
  `generation_infra_*`) — retry with exponential backoff, honor `Retry-After`, try
  off-peak; escalate with `requestId` if persistent.
- **`402` payment / `401` auth** — retry never helps; fix billing or the key.

General repair ladder for a poor-but-successful result (heuristic): improve the input
(lighting, isolate voice, stabilize, raise resolution to 1080p, front the face) →
adjust parameters (`sync_mode`, `temperature`, `occlusion_detection_enabled`,
active-speaker pin) → escalate model (`lipsync-2` → `lipsync-2-pro` for detail, or →
`sync-3` for angle/occlusion/4K). Input quality dominates; try it before spending on a
pricier model.

## Consent, likeness, and rights (do this before generating)

Editing a real person's face to say new words is a likeness-and-voice action, not just a
render. Sync Labs' own published guidance frames the line clearly (sync.so blog, verified
2026-07-10): *dubbing is legitimate when the speaker/rights-holder agreed; the identical
output without that agreement is a deepfake.* Their design is "consent-first" — the
intended path is cloning **your own** voice, and using someone else's voice or face
requires their explicit permission.

Operating rules for an agent:

- **Verify rights before submitting.** Confirm the user owns or has licensed the source
  video, and has consent for any voice being cloned or any face being re-voiced. If those
  are unclear, ask — do not proceed on assumption.
- **Do not impersonate** real public figures or private individuals without consent, and
  do not produce deceptive content (fake statements, fabricated endorsements), non-
  consensual intimate content, or fraud/misinformation. These are the categories most
  likely to be `REJECTED` and are legally and ethically out of bounds regardless of the
  API accepting them.
- **Voice-clone samples** should be the consenting person's own clear single-speaker
  audio (30+ s). Cloning a third party's voice from scraped audio is the exact non-
  consensual case to refuse.
- **Data handling.** For sensitive footage, check the provider's retention/training/
  deletion posture (Sync Labs' own guidance advises verifying whether a provider retains,
  trains on, or deletes your content on request). Prefer not uploading sensitive material
  you cannot account for.
- **Disclosure.** For dubbed/altered public-facing content, follow applicable synthetic-
  media disclosure norms and platform rules; a paid tier is what removes the watermark,
  which means the burden of honest labeling shifts to you.

These obligations are independent of which model you pick and take precedence over
completing the generation.

## Sources (verified 2026-07-10)

First-party (Sync Labs / sync.so):
- Introduction — https://sync.so/docs/introduction
- Lipsync models — https://sync.so/docs/models/lipsync
- sync-3 model — https://sync.so/docs/models/sync-3 ; https://sync.so/sync-3
- react-1 model — https://sync.so/react-1
- Quickstart — https://sync.so/docs/quickstart
- Create Generation API reference — https://sync.so/docs/api-reference/api/generate-api/create.md
- Error handling — https://sync.so/docs/developer-guides/error-handling (catalog: `GET https://api.sync.so/v2/errors`)
- Webhooks — https://sync.so/docs/api-reference/guides/webhooks
- Media formats support — https://sync.so/docs/compatibility-and-tips/media-formats-support
- Improving lip sync quality — https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality
- How AI lip sync works — https://sync.so/docs/product/how-ai-lip-sync-works
- Text-to-speech lip sync tutorial — https://sync.so/docs/tutorials/text-to-speech-lipsync
- Pricing — https://sync.so/pricing
- "Is AI dubbing safe?" (consent/rights guidance) — https://sync.so/blog/is-ai-dubbing-safe/
- Privacy — https://sync.so/privacy

Secondary (third-party model listings, used only to cross-check model availability, not
as the basis for any consequential claim): fal.ai, wavespeed.ai, replicate.com,
segmind.com listings of the Sync lipsync models.
