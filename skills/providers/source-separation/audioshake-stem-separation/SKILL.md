---
name: audioshake-stem-separation
description: >-
  Operate AudioShake's cloud source-separation service (developer.audioshake.ai)
  to split a recording into stems. Use when a task involves isolating vocals,
  drums, bass, guitar, piano, keys, strings, or winds from music; separating
  dialogue / music / effects (DME) for film-TV post-production, localization, and
  dubbing; splitting a mixed recording into one stem per speaker; lyric
  transcription or word-level alignment; music detection/identification; or
  speech denoise/dereverb. Covers the Tasks API job lifecycle (assets, targets,
  formats, polling vs webhooks, credits, limits), choosing which stem targets a
  production actually needs, reviewing separated stems for bleed / artifacts /
  transient smearing / phase problems and repairing them, the rights and consent
  questions raised by separating copyrighted or third-party recordings, and the
  decision boundary for when a local open model such as Demucs is the better
  route than the API. Not for generating or synthesizing new audio, mixing, or
  mastering.
---

# AudioShake stem separation

AudioShake is a hosted audio **source-separation** service: it takes one mixed recording and returns isolated component tracks ("stems"). It does not generate, synthesize, mix, or master audio — it decomposes an existing mix. This skill covers driving its developer API, choosing the right separation targets for a production job, judging and repairing the resulting stems, the rights questions that separation raises, and when to reach for a local open model instead.

All API facts below were verified against `developer.audioshake.ai` on **2026-07-10**. Endpoints, model names, credit rates, and limits are volatile — re-check the live `models` / `billing` / `rate-limits` reference pages and the OpenAPI spec (`https://developer.audioshake.ai/api-reference/openapi.json`) before relying on a specific number in production.

## When this skill applies

Use it when the job is to *pull apart* a recording:

- **Music stems** — isolate vocals, drums, bass, guitar, piano, keys, strings, or winds for remixing, karaoke, sampling, sync, immersive/Atmos re-authoring, or practice/minus-one tracks.
- **Dialogue / Music / Effects (DME)** — split a film, TV, or podcast mix into clean dialogue, a music+effects bed, or an effects-only bed for localization, foreign-language dubbing, M&E (music-and-effects) deliverables, or archival restoration where the original stems are lost.
- **Multi-speaker** — separate an interview, panel, meeting, or overlapping-dialogue recording into one stem per speaker.
- **Lyric transcription / alignment** — line-level lyric transcripts or word-level karaoke timing.
- **Content analysis / cleanup** — detect or identify music inside long-form content (rights clearance), or denoise/dereverb speech.

Do **not** use it to write, generate, or synthesize audio, to compose music, to mix or master, or to add effects. Those are generative or engineering tasks, not separation. If the user already has clean stems and wants them combined or processed, that is out of scope.

## API model: the Tasks API

**Base URL:** `https://api.audioshake.ai` (verified 2026-07-10).
**Auth:** every request carries the header `x-api-key: <key>`. Keys are created in the dashboard (`dashboard.audioshake.ai`). New accounts receive 10 free credits on signup (first-party claim, verified 2026-07-10).

> Note: AudioShake replaced its older **Jobs** API (`/job`, `/upload`, per-request `callbackUrl`) with the **Tasks** API. The Tasks API is the current interface: `POST /assets` instead of `/upload`, `POST /tasks` instead of `/job`, `GET /tasks/{id}` instead of `/job/{id}`, and webhooks registered once via `POST /webhooks` instead of a per-job callback. If you find code using `/job`, it is on the legacy path.

### Job lifecycle

1. **Provide the source audio.** Either pass a public **`url`** (HTTPS) directly, or upload a local file with `POST /assets` and pass the returned **`assetId`**. `url` and `assetId` are mutually exclusive per task.
2. **Create a task** with `POST /tasks`, listing one or more **targets**. Each target is `{ "model": "<name>", "formats": ["<fmt>", ...] }`. A single task takes **1–20 unique targets** and runs them together — this is both cheaper in round-trips and the recommended way to avoid rate limits.
3. **Wait for completion** by either **polling** `GET /tasks/{id}` or registering a **webhook**. Each target moves through `processing` → `completed` | `error`.
4. **Download outputs** from the `output` array. Download URLs are presigned and **expire ~1 hour** after the task completes — fetch and store them promptly, or write directly to your own bucket (see `writeDestination`).

### Request body reference (verified 2026-07-10)

| Field | Type | Notes |
|---|---|---|
| `url` **or** `assetId` | string | Source media. Exactly one. |
| `targets` | array (1–20, unique) | Each item: `model` (2–255 chars) + `formats` array. |
| `formats` | array | Per target. `wav` / `mp3` / `flac` / `aiff` for audio, `mp4` for video, `json` / `srt` / `txt` for transcription & detection. Availability varies by model. |
| `residual` | boolean | Return *everything except* the target stem (the complement). Useful for "remove X" jobs and for catching energy a target misses. |
| `language` | string (ISO 639-1) | For transcription/alignment; auto-detected if omitted. |
| `transcriptAssetId` **or** `transcriptUrl` | string | Required only by the `alignment` model — the known transcript to align. |
| `writeDestination` | string | S3 URI prefix to write outputs to your own bucket instead of the expiring presigned URLs. |
| `metadata` | string (≤4096 chars) | Opaque client metadata echoed back. |

### Response fields

`id`, `createdAt`, `completedAt` (or null), `cost` (credits actually charged), `targets[]` (each with `status`, `output` files, and `error`), a top-level `output[]` of downloadable files, and `error` (code + message, null on success).

### Limits and formats (verified 2026-07-10)

- **Rate limit:** ~60 requests/second. On `429`, back off exponentially, and prefer batching many targets into one task and using webhooks over tight polling.
- **Input audio:** WAV, AIFF, FLAC, MP3, AAC (up to 192 kHz; 16/24-bit WAV recommended).
- **Input video:** MP4, MOV (AAC or PCM audio; the video track is ignored — audio is extracted).
- **Output:** WAV, MP3, FLAC, AIFF; MP4 (separated audio in the original container); JSON/SRT/TXT for text.
- **Not supported:** DRM/encrypted content, and multi-channel/surround formats (e.g. 5.1) — downmix to stereo first if needed.
- **Duration caps by model:** `multi_voice` ≤ 1.5 hours; `transcription` and `alignment` ≤ 45 minutes. Other separation models have no documented cap but cost scales with length.

## The model catalog

Credits are charged **per minute of source audio, per target model, rounded up to the next whole minute** (verified 2026-07-10). So a 3:10 song billed for two targets is charged as 4 min × 2 targets. Rates below are the documented per-minute costs.

### Music / instrument stems — 1.0 credit/min each
`vocals` (all sung voice, lead + backing) · `vocals_lead` (lead only) · `vocals_backing` (harmonies, ad-libs, choir) · `instrumental` (full mix minus vocals) · `drums` · `bass` · `guitar` (all guitar) · `guitar_electric` · `guitar_acoustic` · `piano` (acoustic piano) · `keys` (keyboard family, incl. electric/digital pianos) · `strings` · `wind` (woodwind + brass) · `other` (everything except vocals/drums/bass) · `other-x-guitar` (everything except vocals/drums/bass/guitar).

### Post-production DME — 1.5 credits/min each
`dialogue` (clean speech stem) · `effects` (ambience + SFX bed, dialogue and music removed) · `music_fx` (music + effects, dialogue removed).

### Speech models
`multi_voice` (**10.0 credits/min**, ≤ 1.5 h) — one stem per detected speaker, keeping each speaker isolated even through overlap. `speech_denoise` (1.5/min) — remove background noise, hum, interference. `speech_dereverb` (2.0/min) — remove room reverb/echo for a drier, closer sound.

### Copyright-compliance / analysis
`music_detection` (0.5/min) — return time ranges where music is present. `music_identification` — identify music and return track metadata. `music_removal` — keep speech + effects, remove background music.

### Lyric transcription — 1.0 credit/min each (≤ 45 min)
`transcription` — line-level timestamped lyric transcript (JSON; convertible to SRT/VTT). `alignment` — precise word-level *and* line-level timestamps; **requires** a supplied transcript (`transcriptUrl`/`transcriptAssetId`).

## Choosing targets for a production job

The single most common mistake is requesting the wrong granularity — either paying for stems nobody will use, or requesting a coarse stem when the job needs a fine one. Match targets to the deliverable:

- **Karaoke / instrumental backing:** `vocals` + `instrumental` covers it. If you also need on-screen timed lyrics, add `transcription` (or `alignment` if you already have accurate lyrics and only need timing). Requesting `drums`/`bass`/etc. as well wastes credits unless the product actually plays them separately.
- **Remix / production stems:** request the specific instruments the remixer will touch (`vocals_lead`, `drums`, `bass`, `guitar`, `keys`…). Use `other` / `other-x-guitar` to sweep up the remaining energy so the sum reconstructs the mix — otherwise instruments you didn't request vanish.
- **"Remove one instrument" (minus-one / practice track):** request that instrument with `residual: true` to get the complement in one target, rather than requesting all the other stems and re-summing.
- **Localization / dubbing (M&E):** request `dialogue` (translation reference) + `music_fx` (the bed to layer the new voiceover onto). Add `effects` separately only if the workflow needs music and effects independently (e.g. remixing the music but keeping SFX).
- **Interview / podcast cleanup:** if speakers overlap and you need them apart, `multi_voice`. If speech is buried in noise or a boomy room, chain `speech_denoise` and/or `speech_dereverb` first, then separate.
- **Rights clearance on long-form content:** `music_detection` to find where music appears, then `music_identification` on those ranges; `music_removal` if you must deliver a music-free version.

Prefer the finest stem the deliverable justifies, and always include a residual/`other` target when the stems must re-sum to the original.

## Reviewing separated stems

Separation is never perfect. The following are production heuristics for judging output, not documented guarantees.

Listen to each stem **soloed**, and also **summed back together**, checking for:

- **Bleed / crosstalk** — traces of another source leaking into a stem (a snare ghost in the "vocals" track, vocal breath in "drums"). Most audible on soloed stems and in quiet passages.
- **Musical-noise / "watery" artifacts** — the burbling, underwater texture from spectral holes, worst on `vocals` and busy `other` stems, and on heavily-compressed source (MP3 at low bitrate).
- **Transient smearing / pre-echo** — softened or ghosted drum hits and pluck attacks; check `drums`, `bass`, and plucked `guitar`.
- **Phase / nulling problems** — sum the stems and null-test against the original: a good multi-target set reconstructs the mix closely. Large residual energy means a source went missing (you didn't request an `other`/residual target) or a stem is phase-rotated.
- **Missing energy** — sustained pads, reverb tails, and room tone often collapse into `other`; if you didn't request it they are simply gone.

### Repair strategies

1. **Feed a cleaner source.** Separation quality tracks input quality directly — a 24-bit WAV master separates far better than a 128 kbps MP3. Never up-transcode a lossy file and expect it to help.
2. **Cover the residual.** If summed stems don't reconstruct the mix, add an `other`/`other-x-guitar` target or use `residual: true` so no energy is silently dropped.
3. **Split then clean, in the right order.** For speech, run `speech_denoise`/`speech_dereverb` *before* `multi_voice` when the recording is degraded; for music stems, separate first, then repair the isolated stem with a dedicated tool (e.g. iZotope RX spectral repair) rather than the source.
4. **Use finer targets to reduce bleed.** `vocals_lead` + `vocals_backing` often leaves less bleed than a single `vocals` when only the lead is needed.
5. **Re-derive DME by subtraction.** If `dialogue` is clean but `effects` has bleed, deriving effects as `residual` of dialogue+music can beat the direct `effects` model on some material — A/B them.
6. **Escalate to manual finishing.** Persistent artifacts are a mix/restoration problem: hand the stem to a spectral editor rather than re-running the API repeatedly.

## Rights, consent, and privacy

Separating a recording does not create rights in it. These are legal/policy facts (verified against AudioShake's Terms and public statements on 2026-07-10) plus production caution, not legal advice — advise the user to confirm with counsel for consequential use.

- **You must have rights to the audio you upload.** AudioShake's Terms require the user to represent and warrant they hold all rights needed to upload and process the content and that it infringes no third party; the user indemnifies AudioShake against claims from breaching that warranty.
- **The user keeps ownership of their content**; uploading grants AudioShake only a limited license to process it. Separating a track does not transfer or launder ownership of the underlying recording or composition.
- **Stems of a copyrighted recording are still derivatives of that recording.** Extracting an a cappella or instrumental from a commercial track you don't control does not make it clearable — sync, sampling, remix, and distribution rights still belong to the master and publishing owners. Flag this whenever a user wants to separate a released commercial song for anything beyond private study.
- **Repeat-infringer / takedown policy.** AudioShake states it will block or remove content it believes in good faith to be infringing and discontinue service to repeat offenders.
- **Voices are sensitive.** Multi-speaker separation and dialogue isolation produce identifiable-voice data; treat it under the same consent and privacy obligations as any voice recording (GDPR/CCPA and, in some jurisdictions, biometric-voice laws). Get consent before separating and reusing someone's isolated voice.
- **Data handling for confidential material.** AudioShake's public privacy policy does **not** clearly state whether uploaded audio is used to improve models (verified 2026-07-10). For unreleased masters or confidential film audio, get a written data-processing/retention commitment from AudioShake (enterprise/DPA), or keep the audio off the cloud entirely (see the SDK / local-model options below).

## On-device SDK vs. the cloud API

AudioShake also ships a **local inference SDK** (verified 2026-07-10) that runs separation on-device — Linux, Windows, macOS, Android, iOS (x86_64 / ARM64), CPU or GPU (CUDA, DirectX 12, Apple Metal/Neural Engine, OpenGL ES), with a real-time streaming path (`AudioShakeSeparator`) and a file path (`SourceSeparationTask`). Access needs a Client ID/Secret from AudioShake (contact `info@audioshake.ai`). Choose the SDK over the cloud API when the workflow is **real-time / low-latency** (live music removal, in-app karaoke, game audio), **offline**, or **privacy-constrained** so audio must never leave the device. Choose the cloud Tasks API for batch/back-catalog processing, the full model catalog, transcription/alignment, and when you don't want to ship and update models.

## When a local open model (e.g. Demucs) is the better route

This is a decision boundary only — not a guide to running Demucs. **Demucs / HTDemucs** (`htdemucs`, `htdemucs_ft`) from Meta, usable via UVR or StemRoller, is the strongest open-weight separator and runs free and locally, typically producing a 4-stem split (vocals / drums / bass / other).

Independent and first-party benchmarks agree AudioShake measures higher (AudioShake's first-party claim: vocals SDR ~2 dB above Demucs and ~1 dB better averaged across sources; it won the Sony Sound Demixing Challenge 2023 across both the music (MDX) and cinematic (CDX) tracks — treat the specific dB figures as first-party/secondary evidence, verified 2026-07-10). But the *right* choice depends on constraints, not just SDR:

**Prefer a local model (Demucs) when:** the budget for per-minute credits is effectively zero and volume is high; audio must never be uploaded (privacy/NDA); you need unlimited/bulk offline runs; or a plain 4-stem split at good-not-best quality is sufficient.

**Prefer AudioShake when:** you need top measured quality on hard material (dense mixes, backing vocals, low-level detail); you need capabilities Demucs doesn't offer at all — **DME/dialogue separation, per-speaker `multi_voice`, lyric transcription/alignment, music detection/identification, and fine instrument stems** like `guitar_acoustic`, `keys`, `strings`, `wind`; or you need a managed service with an SLA rather than maintaining models yourself.

A common production pattern: prototype and bulk-triage locally with Demucs, then send the shots that must be broadcast-clean, or that need DME/transcription, through AudioShake.

## Example A — karaoke package for a licensed catalog track (API)

*This is a worked example, not a required template.*

**Intent:** produce an instrumental backing plus timed on-screen lyrics from a 3:20 master the user has licensed for karaoke.

**Request** (`POST https://api.audioshake.ai/tasks`, header `x-api-key: …`):

```json
{
  "assetId": "asset_9f3c...",
  "targets": [
    { "model": "instrumental",  "formats": ["wav"] },
    { "model": "vocals",        "formats": ["wav"] },
    { "model": "transcription", "formats": ["json"] }
  ],
  "metadata": "catalog:track-8842"
}
```

**Why:** `instrumental` is the deliverable; `vocals` is kept as a guide/quality check and is nearly free to add on the same task; `transcription` gives line-level timing for the lyric display. Billing ≈ ceil(3:20)=4 min × 3 targets, at 1.0/min each → ~12 credits.
**Then:** poll `GET /tasks/{id}` (or use a webhook) until each target is `completed`; download from `output` within the hour or set `writeDestination` to your bucket.
**Likely failure modes:** thin/watery `instrumental` if the source was a lossy MP3 (feed the WAV master); lyric timing drift on heavily reverbed vocals (switch to `alignment` with a hand-checked transcript for tighter sync).
**Variation:** for a *practice* app that mutes one instrument on demand, request that instrument with `residual: true` instead of `instrumental`.

## Example B — localization M&E from an episode mixdown (API)

*Worked example.*

**Intent:** prepare a 22-minute TV episode stereo mixdown for Spanish dubbing — a clean dialogue reference plus a music-and-effects bed to lay the new dub over.

**Request:**

```json
{
  "url": "https://assets.studio.example/ep204_stereo_mix.wav",
  "targets": [
    { "model": "dialogue", "formats": ["wav"] },
    { "model": "music_fx", "formats": ["wav"] }
  ],
  "language": "en"
}
```

**Why:** `dialogue` feeds translation/ADR; `music_fx` is the fill under the new voiceover, so no music/SFX is lost when English dialogue is removed. Billing ≈ 22 min × 2 targets × 1.5/min → ~66 credits.
**Review:** solo `music_fx` and listen under where dialogue used to sit — residual dialogue "mumble" bleed is the usual defect. If present, A/B against deriving the bed as the `residual` of `dialogue`, or request `effects` separately and rebuild the bed. Confirm the summed dialogue+bed nulls close to the original.
**Rights note:** confirm the studio holds M&E-creation rights and, if the mix is unreleased, secure a data/retention commitment or use the on-device SDK.

## Example C — reviewing and repairing a noisy multi-speaker interview

*Worked example of the review/repair loop, not a template.*

**Situation:** a 40-minute two-person interview recorded in a reverberant room; the user wants each speaker isolated for editing.

**Approach:** because the room is boomy, clean *before* separating —
1. `POST /tasks` with `speech_dereverb` (and `speech_denoise` if hiss is present) on the source;
2. take the cleaned output as a new asset and `POST /tasks` with `multi_voice` to get one stem per speaker.

**Why this order:** `multi_voice` isolates voices but doesn't fix a bad room; feeding it a dereverbed input yields cleaner per-speaker stems than reverb-in-reverb-out. Billing note: `multi_voice` is the expensive model (10.0/min) — clean first so you only run it once. Watch the 1.5-hour cap (40 min is fine).
**Review:** solo each speaker stem for cross-talk (the other speaker leaking through during overlaps) and for dereverb over-processing (thin, phasey speech). If over-dry, back off to `speech_denoise` alone.
**Consent:** isolated identifiable voices — confirm both speakers consented to processing and reuse before distributing the stems.

## Sources

All verified **2026-07-10**:

- AudioShake Developers — Introduction, Quickstart, Tasks/Assets/Webhooks API reference, Models, Billing & Credits, Formats, Rate Limits, Multi-Speaker, Dialogue/DME, Speech Recovery, Transcription, SDK Overview: `https://developer.audioshake.ai/` and the `*.md` reference pages under it (site map at `https://developer.audioshake.ai/llms.txt`; schema at `https://developer.audioshake.ai/api-reference/openapi.json`).
- AudioShake Terms of Service and Privacy Policy: `https://www.audioshake.ai/terms`, `https://www.audioshake.ai/privacy-policy`; Copyright policy: `https://www.audioshake.ai/copyright`.
- Benchmarks (first-party / secondary, labeled as such): AudioShake posts on the Sony Sound Demixing Challenge 2023 and vocal-model SDR (`https://www.audioshake.ai/post/audioshake-sony-demixing-2023`, `https://www.audioshake.ai/post/audioshake-voice-model-achieves-highest-quality-state-of-the-art-benchmark`); Sound Demixing Challenge 2023 write-up (`https://arxiv.org/html/2308.06979v4`).
- Demucs (open model) capability reference: `https://github.com/facebookresearch/demucs`.
