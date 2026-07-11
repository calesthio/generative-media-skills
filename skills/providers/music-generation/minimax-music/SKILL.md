---
name: minimax-music
description: Produce music with MiniMax Music 2.6 and MiniMax cover/lyrics APIs for songs, instrumentals, AI-generated lyrics, reference-audio covers, video/social/ad soundtracks, artifact custody, rights checks, and production QA.
---

# MiniMax Music production

Use MiniMax Music when the job needs an original song, instrumental bed, theme, jingle, or cover-style rendition from a style prompt, lyrics, or authorized reference audio. Treat it as a music-production provider, not a generic sound-effects tool.

The current public API surface verified on 2026-07-10 is:

- `POST https://api.minimax.io/v1/music_generation` for text-to-music, instrumental music, and cover generation.
- `POST https://api.minimax.io/v1/lyrics_generation` for complete lyrics or lyrics editing/continuation.
- `POST https://api.minimax.io/v1/music_cover_preprocess` for extracting a reference track's feature ID, structured lyrics, and rough structure before an editable cover workflow.
- Global docs list `https://api.minimax.io`; some ecosystem tooling distinguishes a China endpoint such as `https://api.minimaxi.com`. If authentication fails with a valid key, verify the user's account region and configured base URL rather than repeatedly retrying.

Sources verified 2026-07-10: MiniMax music guide, API reference, lyrics API reference, cover preprocess reference, rate-limit guide, pay-as-you-go pricing guide, unified terms, Audio Music Creation Terms, and privacy overview:

- https://platform.minimax.io/docs/guides/music-generation
- https://platform.minimax.io/docs/api-reference/music-generation
- https://platform.minimax.io/docs/api-reference/lyrics-generation
- https://platform.minimax.io/docs/api-reference/music-cover-preprocess
- https://platform.minimax.io/docs/guides/rate-limits
- https://platform.minimax.io/docs/guides/pricing-paygo
- https://www.minimax.io/terms-of-service-v2.html
- https://www.minimax.io/audio/doc/terms-of-service-music.html
- https://www.minimax.io/privacy-policy-v2.html

## Route the job

Choose one of these routes before generating:

1. Original song with user-supplied lyrics: call `music_generation` with `model: "music-2.6"` or `music-2.6-free`, a production-style `prompt`, and the supplied `lyrics`.
2. Original song without lyrics: use `lyrics_generation` first, or set `lyrics_optimizer: true` with empty lyrics when using `music-2.6`/`music-2.6-free`. Prefer a separate lyrics pass when the words matter, because you can review structure, brand safety, and rhyme before paying for audio.
3. Instrumental: call `music_generation` with `is_instrumental: true`; omit `lyrics`. The prompt becomes mandatory and should specify genre, mood, instrumentation, energy arc, use case, and edit constraints.
4. Quick cover from authorized reference audio: call `music_generation` with `model: "music-cover"` or `music-cover-free`, `audio_url` or `audio_base64`, and a target style prompt. This extracts lyrics automatically if `lyrics` is omitted.
5. Editable cover from authorized reference audio: call `music_cover_preprocess` first, review/modify `formatted_lyrics`, then call `music_generation` with `cover_feature_id` and the edited lyrics.

Do not use cover mode unless the user owns or has licensed the reference audio, performance, voice, and lyrics rights needed for the intended use. MiniMax's Audio Music Creation terms require rights or authorization for input content, including audio, lyrics, music, voices, and works; if an input includes a person's voice, authorization is required.

## Current API facts to preserve

Facts below are documented by MiniMax and were verified on 2026-07-10.

Model choices:

- `music-2.6`: recommended text-to-music model; available to Token Plan and paid users, with higher RPM.
- `music-2.6-free`: free-tier text-to-music model; available through API key, with lower RPM.
- `music-cover`: reference-audio cover model; paid/Token Plan tier.
- `music-cover-free`: free-tier reference-audio cover model.

Core request fields:

- `model` is required.
- `prompt` describes style, mood, and scenario. For instrumental `music-2.6`, it is required and 1-2000 characters. For non-instrumental `music-2.6`, it is optional but should still be supplied for production control. For cover models, it is required and 10-300 characters.
- `lyrics` supports newline-separated lyrics and structure tags such as `[Intro]`, `[Verse]`, `[Pre Chorus]`, `[Chorus]`, `[Interlude]`, `[Bridge]`, `[Outro]`, `[Post Chorus]`, `[Transition]`, `[Break]`, `[Hook]`, `[Build Up]`, `[Inst]`, and `[Solo]`. For non-instrumental `music-2.6`, lyrics are required unless `lyrics_optimizer: true` is used with empty lyrics; documented length is 1-3500 characters. For cover models, lyrics are optional if the system extracts them from reference audio, or required at 10-1000 characters when using `cover_feature_id`.
- `lyrics_optimizer: true` is supported only on `music-2.6`/`music-2.6-free`; with empty lyrics it auto-generates lyrics from the prompt.
- `is_instrumental: true` is supported only on `music-2.6`/`music-2.6-free` and removes the lyrics requirement.
- `stream` defaults to `false`.
- `output_format` defaults to `hex`; `url` is also supported. If `stream: true`, only `hex` is supported. URL outputs expire after 24 hours, so download immediately into the project asset folder.
- `audio_setting` supports `sample_rate` values `16000`, `24000`, `32000`, `44100`; `bitrate` values `32000`, `64000`, `128000`, `256000`; and `format` values `mp3`, `wav`, `pcm`.
- `audio_url` and `audio_base64` are only for cover models. Exactly one is required for quick cover mode and both are mutually exclusive with `cover_feature_id`.
- Reference audio constraints for cover modes and preprocess: duration 6 seconds to 6 minutes, size max 50 MB, common formats such as mp3, wav, and flac.
- `cover_feature_id` comes from the preprocess endpoint, is valid for 24 hours, and requires lyrics in the second generation call. Same audio content returns the same ID.

Response and lifecycle:

- Successful music responses include `data.status`; `1` means in progress and `2` means completed.
- If `output_format: "hex"`, `data.audio` contains hex-encoded audio. Decode and write it to a durable local file; do not leave the audio only in logs.
- `extra_info` may include duration, sample rate, channel count, bitrate, and size.
- Preserve `trace_id`, model, prompt, lyrics or lyrics source, audio settings, output file path, cost estimate, and rights notes in the asset manifest.

Rates and costs:

- MiniMax's rate-limit guide lists Music Generation for Music-2.6, Music-Cover, and Music-2.0 at 120 RPM and 20 concurrent connections. Free-tier RPM may be lower; verify account-specific quotas before batch generation.
- MiniMax pay-as-you-go pricing lists Music-2.6 at `$0.15/up-to-5 minutes music` with limited free availability, and Lyrics Generation at `$0.01/per song` with limited free availability. Legacy Music-2.5+ and Music-2.5 are listed at the same 5-minute unit price; Music-2.0 is lower. Re-check pricing before committing a budget.

Error handling:

- `base_resp.status_code: 0` means success.
- Documented relevant error codes include `1002` rate limit, `1004` authentication failed, `1008` insufficient balance, `1026` content flagged for sensitive material, `2013` invalid parameters, and `2049` invalid API key.
- On `1002`, back off and retry within the user's approved batch scope.
- On `1004` or `2049`, check key validity, account tier, and regional endpoint.
- On `1008`, stop and ask the user whether to recharge, switch tier, or cancel.
- On `1026`, do not bypass moderation. Revise the creative brief or lyrics to remove unsafe or infringing material.
- On `2013`, validate required field combinations, length limits, mutually exclusive fields, and audio settings.

## Production prompting

Write the `prompt` like a short music brief. Include the sonic identity, emotional function, arrangement, vocal direction if applicable, structure or arc, and delivery context. Avoid vague strings such as "cinematic and inspiring" unless the use case is generic.

Useful prompt ingredients:

- Genre and subgenre: "indie folk", "future bass", "Motown-inspired soul", "90s boom bap", "minimal piano ambient".
- Function: "under a founder-narrated launch film", "loopable Shorts intro", "30-second product sting", "credits theme".
- Tempo and energy: "slow 72 BPM feel", "mid-tempo walking pace", "builds from sparse to triumphant".
- Arrangement: lead instruments, percussion density, bass presence, texture, silence/breathing room.
- Vocal direction: singer gender/timbre only when useful; do not request an identifiable living artist or cloned voice unless authorized and allowed.
- Mix needs: "leave room for narration", "no busy lead melody under dialogue", "strong downbeat at 0:08 for logo reveal", "clean ending for ad cutdown".
- Negative constraints: "no harsh cymbals", "avoid novelty/comedy tone", "no explicit lyrics", "do not imitate any named artist".

For lyrics, prefer explicit structure tags. Keep chorus words memorable but not repetitive enough to feel synthetic. Put brand/product names sparingly; many music models overemphasize repeated nouns if every line contains the product.

For video, design the music around the edit:

- 6-15 seconds: sting, hook, button, or loop. Use instrumental unless sung words are the point.
- 15-30 seconds: ad/social bed with a clear rise and logo/downbeat.
- 30-60 seconds: short song section or instrumental arc; provide section tags matching scene transitions.
- 60+ seconds: full song or stem-like main mix, then edit down externally.

MiniMax generates a finished mix, not separate stems. If the project needs ducking under narration, title-safe beats, stems, or alternate cutdowns, plan post-processing with the local audio editor/DAW/FFmpeg after generation.

## Artifact custody

Before a generation call, create an intended output path such as:

`projects/<project-id>/assets/music/minimax_<slug>_<model>_<timestamp>.mp3`

After receiving output:

1. If output is hex, decode the hex string to the chosen extension from `audio_setting.format`.
2. If output is a URL, download it immediately; MiniMax documents that URL links expire after 24 hours.
3. Run a basic media probe: duration, channels, sample rate, bitrate, file size, and decodability.
4. Audition the full track. Do not approve from waveform metadata alone.
5. Record provenance: endpoint, model, request JSON minus secrets, `trace_id`, `base_resp`, `extra_info`, source/reference audio path or URL, rights notes, reviewer decision, and any edit plan.

Recommended production defaults:

- For web/video/social: `audio_setting: { "sample_rate": 44100, "bitrate": 256000, "format": "mp3" }`.
- For post-production mastering or heavy editing: prefer `wav` if storage allows.
- For streaming response handling or minimal payload dependency: use `hex` and decode locally.
- For simple integration demos where the asset will be immediately downloaded: `output_format: "url"` is acceptable, but still store the file locally.

## QA checklist

Review every generated track for:

- Fit to brief: genre, mood, energy, instrumentation, vocal presence, and edit timing.
- Lyrics: pronunciation risk, grammar, awkward scansion, unwanted profanity, brand correctness, claims, and policy-sensitive content.
- Music quality: clipping, pumping, unnatural transitions, collapsed stereo image, overly busy melody under narration, abrupt endings, intro dead air, or genre mismatch.
- Duration and editability: whether it lands on the needed beat, has loopable sections, and can fade cleanly.
- Rights and disclosure: authorized inputs, no prompt requesting named-artist imitation or unauthorized voice/persona, AI disclosure where the destination requires or where MiniMax notices require labeling.
- Delivery specs: expected format, sample rate, loudness target after post, and storage in the canonical project asset folder.

Do at least one regeneration when a track fails the brief in a way that cannot be repaired by simple trimming, fading, EQ, or ducking. When regenerating, change only the variable that caused the failure so the comparison remains useful.

## Safety, rights, and policy posture

Documented terms and production heuristics:

- MiniMax unified terms make access dependent on account type, subscription plan, technical compatibility, geographic availability, and other eligibility requirements.
- MiniMax Audio Music Creation terms require rights or authorization for all input content, including lyrics, music, audio, video, voices, and works. They also require voice authorization when input includes an individual's voice.
- Terms prohibit unlawful or rights-infringing use, impersonation, reputational harm, misleading content, and other prohibited conduct.
- Terms state that identifiers or watermarks may be embedded in output and that users are responsible for clear AI-generated content labeling to avoid misleading others.
- MiniMax does not guarantee output accuracy, suitability, reliability, or completeness.

Practical rules for agents:

- Ask for confirmation of rights before using a reference song, commercial track, client jingle, performer recording, or voice-like source in cover mode.
- Do not use "in the style of [living artist]" as a production instruction. Convert artist references into musical attributes: era, instrumentation, tempo, timbre, arrangement, harmonic palette, mix texture.
- Do not claim exclusive copyright ownership or platform-safe commercial rights unless the user's legal terms/subscription and local law have been reviewed.
- Do not remove or hide provider-required identifiers/watermarks/notices.
- Keep generated music reviewable and traceable; avoid orphaned temporary URLs.

## Complete examples

### Example: 30-second SaaS launch film instrumental

Intent: create a background track for a founder voiceover and animated product reveal.

Route: original instrumental with `music-2.6`; post-edit if needed.

Request:

```json
{
  "model": "music-2.6",
  "prompt": "Premium minimalist electronic score for a 30-second SaaS launch film. 92 BPM feel, warm analog pad bed, soft plucked synth pulse, restrained sub bass, subtle brushed percussion. Start intimate and focused, lift at 0:12, confident logo downbeat around 0:24, clean final tail. Leave space for spoken narration; no lead vocal, no busy top-line melody, no harsh cymbals.",
  "is_instrumental": true,
  "output_format": "hex",
  "audio_setting": {
    "sample_rate": 44100,
    "bitrate": 256000,
    "format": "mp3"
  }
}
```

Why it is structured this way: the prompt specifies function, edit points, arrangement density, and narration space. It uses instrumental mode because sung content would compete with the voiceover.

Expected review: audition whether the lift and logo downbeat are close enough for the edit. If the generated piece is too melodic under narration, regenerate with stronger "rhythmic texture, no lead melody" language before trying EQ fixes.

### Example: social jingle with reviewed lyrics

Intent: generate a short brand-safe vocal hook for a hydration product short, avoiding medical claims.

Route: write/review lyrics first, then generate music.

Lyrics generation request:

```json
{
  "mode": "write_full_song",
  "prompt": "A clean 20-30 second pop jingle about grabbing a sparkling water after a workout. Bright, playful, no health or performance claims, no mention of curing or improving the body. Include a short chorus only and keep the brand placeholder as [BRAND].",
  "title": "Fresh Spark"
}
```

Curated lyrics for music call:

```text
[Intro]
Fresh from the fridge, a little fizz in the light

[Chorus]
Hey [BRAND], brighten up the break
Cold little bubbles, easy choice to make
Step outside, let the afternoon shine
One crisp sip and the moment feels fine
```

Music generation request:

```json
{
  "model": "music-2.6",
  "prompt": "Upbeat modern pop jingle, bright handclaps, clean electric piano, light funk bass, cheerful group backing vocals, 105 BPM feel, 20-30 second social ad hook, polished but not childish, clean brand-safe energy.",
  "lyrics": "[Intro]\nFresh from the fridge, a little fizz in the light\n\n[Chorus]\nHey [BRAND], brighten up the break\nCold little bubbles, easy choice to make\nStep outside, let the afternoon shine\nOne crisp sip and the moment feels fine",
  "output_format": "hex",
  "audio_setting": {
    "sample_rate": 44100,
    "bitrate": 256000,
    "format": "mp3"
  }
}
```

QA focus: confirm the placeholder is replaced correctly before publication, check no accidental health/performance claims were introduced, and make a cutdown if the generated track exceeds the ad length.

### Example: authorized reference-audio cover with modified lyrics

Intent: make a legally authorized alternate-language or campaign-specific cover of a client-owned jingle while preserving the melodic/structural feel.

Route: two-step cover workflow for lyric review.

Preprocess request:

```json
{
  "model": "music-cover",
  "audio_url": "https://example-client-cdn.com/authorized-jingle-master.mp3"
}
```

Then review the returned `formatted_lyrics` and `structure_result`. If rights are documented and the lyric changes are approved, generate:

```json
{
  "model": "music-cover",
  "prompt": "Friendly acoustic-pop cover for a family travel campaign, warm female vocal, ukulele, soft kick, handclaps, sunny but not childish, keep a compact ad-jingle feel.",
  "cover_feature_id": "returned_feature_id_here",
  "lyrics": "[Verse]\nPack the bags, the road is bright\nLittle maps and morning light\n\n[Chorus]\nGo with [BRAND], find your way\nSmall new wonders every day",
  "output_format": "hex",
  "audio_setting": {
    "sample_rate": 44100,
    "bitrate": 256000,
    "format": "mp3"
  }
}
```

Critical checks: the reference audio must be 6 seconds to 6 minutes and no larger than 50 MB; `cover_feature_id` expires after 24 hours; do not pass `audio_url` and `cover_feature_id` in the same generation request; keep proof of authorization in the project notes.

### Example: podcast bumper loop

Intent: a loopable instrumental bumper for a technology podcast.

Route: instrumental generation, then local loop edit.

Request:

```json
{
  "model": "music-2.6",
  "prompt": "Loopable 12-18 second technology podcast bumper, restrained future garage texture, muted kick, soft vinyl crackle, airy synth chord, two-note identity motif, editorial and intelligent, no vocals, no dramatic trailer drums, no abrupt ending. Make the first and last bars compatible for a crossfade loop.",
  "is_instrumental": true,
  "output_format": "hex",
  "audio_setting": {
    "sample_rate": 44100,
    "bitrate": 256000,
    "format": "mp3"
  }
}
```

Expected workflow: generate 2-3 candidates if budget allows, pick the least busy one, trim to a bar boundary, add a short equal-power crossfade, and export a final loop plus a one-shot ending.
