---
name: kling-advanced-lip-sync
description: Production guidance for Kling AI Open Platform Advanced Lip-Sync. Use for identifying/selecting one face in an existing video, assigning URL/Base64 or Kling TTS audio, cropping and inserting audio in milliseconds, mixing original sound, creating and monitoring tasks, downloading expiring results, consent/privacy review, sync QA, and repair. Do not use for still-image avatar generation or ordinary Kling video generation.
---

# Kling Advanced Lip-Sync

Use this skill for Kling AI Open Platform's documented Advanced Lip-Sync workflow on an existing video. It is distinct from Avatar, which generates a new talking performance from a still image and audio.

## Verification and evidence

- **Documented fact:** behavior stated in first-party Kling Open Platform pages.
- **Production heuristic:** a practical sync/repair recommendation not guaranteed by Kling.
- **Empirical observation:** a result measured from an actual task/output.

Facts were verified **2026-07-12**. Endpoint visibility, entitlement, pricing, callback behavior, retention, limits, and policy can change. Re-check official documentation, authenticated console, account package, and applicable agreement before paid use.

## Official workflow

Base URL in current examples:

```text
https://api-singapore.klingai.com
```

Operations:

1. `POST /v1/videos/identify-face`
2. `POST /v1/videos/advanced-lip-sync`
3. `GET /v1/videos/advanced-lip-sync/{id}`
4. `GET /v1/videos/advanced-lip-sync`

Although the navigation may call a tab Face Recognition, the operation is Identify Face. Describe it as face identification/detection for selecting a visible face; do not claim general identity matching.

## Authentication

Official docs use JWT Bearer authentication derived from Kling Open Platform access/secret credentials:

```http
Authorization: Bearer ${KLING_JWT}
Content-Type: application/json
```

Follow the current authentication page for token construction and lifetime. Generate server-side, use least privilege, and never place keys/secrets/JWTs in browser code, logs, callbacks, or fixtures.

## Validate the video source

Identify Face accepts exactly one:

- `video_id`: Kling-generated video from the documented recent window;
- `video_url`: accessible external video.

They are mutually exclusive.

Current external-video constraints include `.mp4` or `.mov`, 2-60 seconds, at most 100 MB, 720p or 1080p, and width/height each 512-2160 pixels. Current docs also limit Kling `video_id` recency to 30 days. Kling performs content validation.

Preflight codec/container, duration, dimensions, file size, URL reachability, audio presence, face visibility, cuts, occlusion, and consent. Do not upload a private URL that Kling cannot access or a mutable URL that can change between operations.

## Identify and select a face

Example:

```http
POST /v1/videos/identify-face

{"video_url":"https://example.com/source.mp4"}
```

The response includes `session_id` and `face_data[]`; each face can include `face_id`, `face_image`, `start_time`, and `end_time` in milliseconds.

Present detected face crops/intervals to the user or authorized operator. If several faces exist, require an explicit `face_id` unless a documented, approved selection rule exists. Record selected face, reason, and interval.

`face_choose` is an array, but current docs explicitly say only one-person lip-sync is supported. Do not claim simultaneous multi-speaker replacement. Re-identify after any source-video edit; do not reuse a stale session against changed media.

Kling does not publicly establish session expiry/reuse semantics in the verified docs. Keep identify/create close together and handle invalid sessions as a new identification job.

## Prepare audio and timing

For the selected face, provide exactly one:

- `audio_id`: recent Kling TTS audio;
- `sound_file`: accessible URL or Base64 audio.

They are mutually exclusive.

Current external-audio constraints include `.mp3`, `.wav`, `.m4a`, or `.aac`, 2-60 seconds, and at most 5 MB. Current docs limit `audio_id` recency to 30 days.

Timing fields are milliseconds:

- `sound_start_time`: crop start in source audio;
- `sound_end_time`: crop end;
- `sound_insert_time`: insertion point in source video.

Validate:

$$
cropDuration = soundEnd - soundStart \ge 2000\text{ ms}
$$

The crop must fit inside the source audio, the inserted range must fit inside the video, and the inserted range must overlap the selected face's detected appearance interval by at least two seconds.

Use explicit millisecond arithmetic. Never pass seconds by accident.

Mix controls:

- `sound_volume`: current documented range 0-2, default 1;
- `original_audio_volume`: range 0-2, default 1; no effect for silent source.

Preserve ambience when it matters, but ensure source dialogue does not create double speech. Review the final mix separately from lip motion.

## Create the task

Illustrative request:

```json
{
  "session_id": "<identify-face-session>",
  "face_choose": [
    {
      "face_id": "<approved-face-id>",
      "sound_file": "https://example.com/dialogue.wav",
      "sound_start_time": 0,
      "sound_end_time": 3000,
      "sound_insert_time": 1000,
      "sound_volume": 1,
      "original_audio_volume": 0.25
    }
  ],
  "external_task_id": "scene-014-take-03",
  "callback_url": "https://example.com/hooks/kling",
  "watermark_info": {"enabled": false}
}
```

This assumes a three-second crop, sufficient video duration, and at least two seconds of overlap with the selected face interval.

`external_task_id` uniqueness is caller-owned. Store it with the system `task_id`, source/audio hashes, session/face IDs, timings, volumes, attempt, consent record, and cost preflight.

## Monitor and reconcile

Task statuses:

- `submitted`
- `processing`
- `succeed`
- `failed`

Use the single-task endpoint as source of truth. Callbacks can reduce polling latency, but production handling should be idempotent and accept duplicates/out-of-order events. Unless the current callback page documents a signature mechanism, do not invent one. Retrieve the task before trusting or publishing callback data.

List queries use current pagination ranges; do not scan the list when a task ID is known.

Retry transient rate/concurrency/server errors with bounded jitter. Do not retry auth, permission, parameter, policy, or invalid-media failures unchanged. Preserve provider code/message/request ID.

## Cost, access, and result custody

The public pricing page did not clearly establish a dedicated Advanced Lip-Sync list price during verification. Do not assume Avatar pricing applies. Check authenticated console/package entitlement and create a dated budget approval.

Successful task responses expose final deduction fields; reconcile actual units/balance against the estimate.

Generated media is documented as deleted after 30 days. Download promptly into controlled storage, checksum, probe, and preserve provenance. Do not use provider URLs as permanent delivery storage.

Endpoint entitlement and concurrency are account/package dependent. Errors such as rate, concurrency, package exhaustion, or permission denial should be surfaced precisely.

## Consent, privacy, and rights

This workflow processes recognizable face video and voice/audio. Require:

- explicit recorded authority for likeness and audio/voice;
- intended use, audience, territory, term, modification scope, revocation, and retention;
- additional review for minors, employees, public figures, political use, deceased persons, and sensitive contexts;
- no deceptive impersonation or undisclosed material alteration;
- access controls and deletion procedure for source video, face crops, audio, sessions, and output;
- platform/legal disclosure and provenance where required.

Kling's technical `face_id` does not prove identity or consent. Review current API privacy/terms for hosting, storage, transfer, processing, model improvement, and enterprise exceptions. Do not make unqualified training, residency, or deletion claims.

## Sync QA and repair

Kling does not publish a formal sync-quality metric or repair API. The following are production heuristics:

1. Review normal speed and frame-by-frame around plosives, labials, word starts, and phrase ends.
2. Check mouth motion begins/ends with speech rather than room tone.
3. Verify the selected face stays visible across the insertion.
4. Inspect profiles, cuts, occlusion, hand-over-mouth, facial hair, and motion blur.
5. Check jaw, teeth/tongue, frozen expression, identity drift, and surrounding pixels.
6. Check ambience continuity and double speech after mix changes.
7. Repair timing first by recropping or changing insertion time.
8. Shorten difficult segments rather than repeatedly processing a full clip.
9. Preserve an untouched master and compare outside the altered range.

Do not claim a rerun will necessarily improve output. Change one variable, record it, and compare.

## Example 1: single-speaker localization insert

This is a complete example, not a mandatory formula.

**Intent:** replace a three-second line in an authorized interview while keeping room ambience.

Preflight a 12-second 1080p MP4 under 100 MB, confirm one visible consented speaker, and provide a 3.2-second WAV under 5 MB. Identify faces, select the approved face whose interval covers seconds 2-10, then crop audio 100-3100 ms and insert at 3500 ms. This yields a 3000 ms insertion within video and at least two seconds inside the face interval. Set source dialogue low enough to avoid doubling while retaining ambience.

Monitor by task ID, download/checksum immediately, then review consonants, start/end motion, identity, occlusion, and ambience. If sync starts late, adjust insertion/crop before changing volume or regenerating audio.

## Example 2: multiple detected faces

This is a complete example, not a mandatory formula.

**Intent:** replace one host line in a two-person panel clip.

Identify Face returns two faces with distinct crops and intervals. Present both; the authorized editor selects the host. Because only one-person lip-sync is documented, create one task for that face and do not promise simultaneous guest replacement. Choose a segment where the host remains visible and the guest does not occlude the mouth. Keep original audio if only ambience remains; otherwise use a prepared mix.

If the requirement becomes replacing both speakers, stop and choose another supported workflow rather than chaining undocumented multi-face tasks.

## Sources

Official sources verified 2026-07-12:

- Advanced Lip-Sync and Identify Face: https://kling.ai/document-api/api/video/lip-sync and https://kling.ai/document-api/api/video/lip-sync/face-detection
- Avatar boundary: https://kling.ai/document-api/api/video/avatar
- Authentication, callbacks, concurrency, and errors: https://kling.ai/document-api/api/get-started/authentication , https://kling.ai/document-api/api/get-started/callbacks , https://kling.ai/document-api/api/get-started/concurrency-rules , and https://kling.ai/document-api/api/get-started/error-codes
- Open Platform overview and pricing: https://kling.ai/document-api/guides/get-started/overview and https://klingai.com/dev/pricing
- API privacy and global policies: https://kling.ai/document-api/guides/protocols/privacy-policy , https://kling.ai/docs/user-policy , and https://kling.ai/docs/privacy-policy