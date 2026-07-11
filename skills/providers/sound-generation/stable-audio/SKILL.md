---
name: stable-audio
description: "Use for Stability AI Stable Audio production work: selecting Stable Audio hosted API or open-weight models, generating or editing music, loops, sound effects, foley, beds, stingers, and sonic-branding audio from text or source audio, planning rights-safe uploads, setting model parameters, polling asynchronous jobs, and reviewing generated audio for media projects."
---

# Stable Audio production guide

Stable Audio is Stability AI's generative-audio family for music and sound-design outputs, not speech, voice cloning, dialogue, or final mix/mastering. Use it when a project needs instrumental music, loops, stems/ideas, sound effects, foley-like assets, ambience, stingers, transitions, or style/continuation edits from rights-cleared audio. Route speech, dubbing, voiceover, transcript alignment, and loudness mastering to the appropriate speech/audio-post tools instead.

All volatile facts in this guide were verified on 2026-07-10 from Stability AI official pages, the Stability API OpenAPI specification, official model cards/repositories, and Stability policy pages.

## Capability map

Documented facts:

- Hosted Stability API exposes two Stable Audio route families:
  - Stable Audio 2 endpoints under `/v2beta/audio/stable-audio-2/...`, with `model` choices `stable-audio-2` and `stable-audio-2.5`.
  - Stable Audio 3 endpoints under `/v2beta/audio/stable-audio/...`, with `model=stable-audio-3`.
- Supported hosted workflows are text-to-audio, audio-to-audio, and inpainting/continuation.
- Hosted outputs are 44.1 kHz stereo, with `mp3` or `wav` output format.
- Stable Audio 2/2.5 hosted endpoints return audio synchronously on success. Stable Audio 3 hosted endpoints return HTTP 202 with a generation id; poll `GET /v2beta/audio/results/{id}` until HTTP 200 returns the audio.
- Stable Audio 2/2.5 hosted duration limits are 1-190 seconds. Audio uploads for audio-to-audio and inpaint must be 6-190 seconds, `mp3` or `wav`, and requests are capped at 50 MB.
- Stable Audio 3 hosted duration limits are 1-380 seconds. Audio uploads for audio-to-audio and inpaint must be 6-380 seconds, `mp3` or `wav`, and requests are capped at 100 MB.
- Prompt length is capped at 10,000 characters.
- `seed` accepts `0` or omitted for random generation; explicit seeds may be recorded for reproducibility.
- `steps` differs by model: Stable Audio 2 accepts 30-100 steps and defaults to 50; Stable Audio 2.5 and Stable Audio 3 accept 4-8 steps and default to 8.
- `cfg_scale` ranges 1-25. API docs describe it as prompt-adherence strength; defaults are 7 for Stable Audio 2, 1 for Stable Audio 2.5, and 1 for Stable Audio 3. Treat it as a secondary control after prompt, duration, model, steps, and source-audio strategy.
- `strength` in audio-to-audio ranges 0-1 and controls source-audio influence. Stability describes `0` as identical to the input and `1` as equivalent to no audio influence.
- Inpaint uses `mask_start` and `mask_end` in seconds to choose the replacement/continuation segment.
- Hosted pricing, verified 2026-07-10: Stable Audio 2.0 is `credits = 17 + 0.06 * steps` per successful generation, usually 20 credits at the default 50 steps and 23 credits at 100 steps; Stable Audio 2.5 is 20 credits per successful result; Stable Audio 3.0 is 26 credits per successful result. Stability states failed generations are not charged. Stability pricing uses 1 credit = $0.01 and is subject to change.
- Stable Audio Open 1.0 is an open-weight text-to-audio model that generates variable-length stereo audio up to 47 seconds at 44.1 kHz.
- Stable Audio 3 open-weight releases include `small-music`, `small-sfx`, and `medium`; the official repository lists Small music/SFX as CPU-capable 433M-parameter models with 120s max length and Medium as a 1.4B CUDA model with 380s max length. Stable Audio 3 Large is API-only in the official repo.

Sources: [Stability API reference / OpenAPI spec](https://api.stability.ai/v2alpha/openapi), [Stable Audio 3 page](https://stability.ai/stable-audio), [Stable Audio 2.0 announcement](https://stability.ai/news-updates/stable-audio-2-0), [Stable Audio 2.5 announcement](https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale), [Stable Audio 3 repository](https://github.com/Stability-AI/stable-audio-3), [Stable Audio Open 1.0 model card](https://huggingface.co/stabilityai/stable-audio-open-1.0), [Stable Audio Open paper](https://arxiv.org/abs/2407.14358), [Stable Audio 3 paper](https://arxiv.org/abs/2605.17991), [Stability pricing page](https://platform.stability.ai/pricing).

## Choose the route before prompting

Use hosted Stable Audio 3 when the project needs current highest-capability hosted Stable Audio, up to ~6 minute beds, async generation is acceptable, or inpainting/continuation is part of the plan. It is the cleanest choice for longer music beds, adaptive game/music cues, sonic-branding variations, and complex ambience where 190 seconds is not enough.

Use hosted Stable Audio 2.5 when you need synchronous API behavior, 190 seconds is enough, and the brief is commercial music/sound production where Stable Audio 2.5's documented improvements in speed, musical structure, mood/genre prompt adherence, and inpainting matter.

Use hosted Stable Audio 2 only when a pipeline already depends on its behavior or when you intentionally need its 30-100 step range and `cfg_scale` behavior. Do not default to it just because the endpoint default is `stable-audio-2`; explicitly set the model.

Use Stable Audio 3 open weights when local or self-hosted generation, fine-tuning/LoRA experimentation, data-control review, or offline iteration matters. Choose:

- `small-music` for quick CPU music drafts up to 120s;
- `small-sfx` for quick CPU sound-effect drafts up to 120s;
- `medium` for higher-quality local generation up to 380s when CUDA and dependency constraints are acceptable.

Use Stable Audio Open 1.0 only when the 47s limit is acceptable and the workflow needs the older open model, diffusers/stable-audio-tools compatibility, or research comparison.

Do not use Stable Audio for:

- lyrics or sung vocal performance unless the current product/tool explicitly supports the needed vocal workflow;
- voiceover, narration, voice cloning, or lip-sync;
- exact recreation of a known artist, track, label sound, or copyrighted recording;
- uploads that the user has not rights-cleared;
- final legal/music-supervision clearance.

## Rights, consent, privacy, and upload gate

Before any audio-to-audio or inpaint request, require the user or project brief to establish that every uploaded sound is rights-cleared for transformation. Stability's API docs and Stable Audio announcements state that copyrighted content is not allowed to be uploaded and describe content recognition/compliance scanning for uploads. Treat "I found this song online" as blocked until replaced with licensed, public-domain, commissioned, self-recorded, or otherwise authorized material.

For commercial media, record:

- provider/model/version or repository id;
- endpoint/workflow;
- prompt;
- duration, seed, steps, `cfg_scale` if used, `strength`, mask times, and output format;
- source-audio filename, owner, license/permission, and whether it contains third-party music, vocals, identifiable voices, brands, or location ambience;
- generation timestamp, request id/generation id if available, and credit cost;
- post-processing chain and final exported path.

Stability's Terms of Service state that users are responsible for inputs and must have rights, licenses, and permissions for inputs; as between the user and Stability, Stability assigns any right it has in outputs subject to compliance and applicable law. The same terms also say outputs may be similar across users, users must verify legality/appropriateness before use, and Stability may use inputs/outputs to improve services unless the user opts out where available. Privacy/security policy claims should not be overstated: Stability states it uses organizational and technical safeguards, but no internet transmission/storage is guaranteed to be fully secure.

For confidential brand libraries, unreleased music, celebrity voices, minors, medical/legal content, or contractual IP, prefer enterprise-approved settings or local/open-weight routes only after the project's data-handling requirements are known. Do not upload sensitive stems just because the API is convenient.

Sources: [Stability Terms of Service](https://stability.ai/terms-of-service), [Stability Acceptable Use Policy](https://stability.ai/use-policy), [Stability Privacy Policy](https://stability.ai/privacy-policy), [Stable Audio 2.0 announcement](https://stability.ai/news-updates/stable-audio-2-0), [Stable Audio 2.5 announcement](https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale), [Stability SOC 2/SOC 3 announcement](https://stability.ai/news-updates/stability-ai-achieves-soc-2-type-ii-and-soc-3-compliance).

## Prompting for production

Stable Audio responds best when the prompt describes what the audio should sound like, not what the video should show. Translate visual intent into sonic parameters.

Documented prompt elements from Stability guidance include genre/subgenre, style, tempo/BPM, mood, and instrument type. Production heuristics below are not documented guarantees; use them because they make review and iteration easier:

- State the deliverable role first: "15-second UI success stinger", "90-second product-launch bed", "6-second cloth-rustle foley", "loopable 120 BPM tech-house drum loop".
- Include tempo/BPM when synchronization matters; include "loopable" only when you will QA the loop seam.
- Include key only when the composition must sit under other music; verify by ear or audio analysis because key adherence is not guaranteed.
- Use concrete instrumentation and mix language: "muted palm-picked electric guitar", "dry close-mic footsteps on wet concrete", "subtle analog tape hiss", "wide stereo pad, no lead melody".
- Use section language for music beds: intro, lift, breakdown, outro, button ending, no hard drop before 20s.
- Use avoidance language sparingly inside the positive prompt when no negative prompt parameter exists in the hosted API: "no vocals, no recognizable melody, no heavy drums".
- For sound effects, describe object, material, gesture, space, distance, intensity, and tail: "ceramic mug placed gently on a wooden desk, close perspective, small room reflection, short natural tail."
- For cinematic ambience, separate bed and events: "continuous low city night ambience with occasional distant siren and soft tire hiss; no foreground speech."

Keep prompts internally consistent. A single prompt that asks for "minimal ambient corporate piano" and "aggressive drum & bass festival drop" will produce less controllable review targets.

## Parameter strategy

Duration:

- Generate close to the needed edit length plus handles. For a 30s bed, request 35-45s if the edit may need a fade-in/out or alternate downbeat. For SFX, request only the needed length plus a small tail; long SFX generations invite unrelated events.
- For looping assets, generate longer than one loop cycle, then cut the best stable section and crossfade/beat-match in post.

Model:

- Always set `model` explicitly. Do not rely on endpoint defaults.
- Prefer `stable-audio-3` for 191-380s hosted work or async pipelines.
- Prefer `stable-audio-2.5` for synchronous 1-190s hosted work unless project history requires 2.0.

Steps:

- For 2.5/3, default 8 is the quality-first setting within the documented 4-8 range; use lower steps only for draft batches.
- For 2.0, default 50 is the cost/quality baseline; increase toward 100 only when a near-final render needs another quality pass and the extra credits are acceptable.

Seed:

- Use random seed for ideation batches.
- Record returned seed for any keeper.
- Reuse a seed only to test prompt or parameter changes; do not promise exact repeatability after model/provider updates.

Output format:

- Use `wav` for assets that will be edited, looped, layered, mixed, or mastered.
- Use `mp3` for quick previews, low-risk temp tracks, or delivery systems that require it.

Audio-to-audio strength:

- 0.15-0.35: preserve source gesture/timing; subtle restyling.
- 0.35-0.65: keep rough rhythm or contour while changing sound identity.
- 0.65-0.9: strong transformation with source used mostly as inspiration.
- 1.0: effectively no source influence per API docs; use text-to-audio instead unless the implementation requires the upload route.

Inpaint masks:

- Place `mask_start` slightly before the flawed region and `mask_end` slightly after it so the model has room to blend.
- For continuation, mask from the continuation point to the desired end.
- After inpainting, check transition clicks, phase shifts, tempo drift, key drift, and room-tone discontinuity.

## Workflow patterns

Text-to-audio music bed:

1. Convert the video/edit need into musical function: energy curve, target duration, tempo range, no-go elements, and edit points.
2. Generate 3-6 short or medium candidates before committing to a full-length final.
3. Pick for structure and editability, not just first-listen excitement.
4. Generate the final in `wav` with documented seed/parameters.
5. Edit, fade, duck under dialogue, normalize loudness, and test under picture.

Text-to-audio SFX/foley:

1. Generate isolated, dry-enough assets unless ambience is intentional.
2. Ask for close perspective and short tail for UI/foley; ask for environment and distance for ambience.
3. Generate multiple variants at short duration.
4. Layer and time-align in post; do not expect one generation to solve every hit.
5. QA for hidden speech, music, clipping, excessive reverb, and mismatched perspective.

Audio-to-audio transformation:

1. Confirm upload rights and remove private or unneeded material.
2. Trim the source to only the useful segment; keep it within documented duration/size limits.
3. Choose strength based on how much timing/motif must survive.
4. Prompt the target sound, not the source description alone.
5. Compare against source for unwanted copying, leakage, or recognizable third-party material.

Inpainting/continuation:

1. Use it when most of an audio asset works but one section needs replacement or extension.
2. Preserve tempo/key/texture cues in the prompt.
3. Mask generously but avoid replacing stable sections unnecessarily.
4. Validate the repaired seam under headphones and on speakers.

## Complete examples

### Example: 30-second product-launch bed

Intent: an optimistic bed under narration for a SaaS launch reel, no vocals, easy to duck.

Route: hosted Stable Audio 2.5 text-to-audio, synchronous, `wav`.

Parameters:

```text
endpoint: POST /v2beta/audio/stable-audio-2/text-to-audio
model: stable-audio-2.5
duration: 40
steps: 8
output_format: wav
seed: 0
```

Prompt:

```text
40-second modern product-launch instrumental bed at 104 BPM, optimistic and confident, clean electronic pop with warm analog synth pulses, soft piano accents, light brushed percussion, subtle bass, wide polished stereo mix. Structure: 4-second gentle intro, steady lift through 25 seconds, restrained final button ending. Designed to sit under spoken narration. No vocals, no lead guitar solo, no aggressive drums, no recognizable melody.
```

Why structured this way: The prompt names function, duration, BPM, mood, arrangement, section behavior, mix priority, and exclusions relevant to narration.

Expected review: Check the first 4 seconds for usable intro space, verify the 25-30s region can support the hero claim, and cut/fade the 40s render to the final 30s edit.

Likely failures: too much lead melody, drums masking speech, unresolved ending, or tempo not matching the edit. Iterate by reducing instrumentation or asking for "more sparse, more sidechain space for narration."

### Example: rights-cleared audio-to-audio sonic-brand variation

Intent: transform a client-owned two-note chime into a family of softer onboarding sounds.

Precondition: project log confirms the client owns the chime and permits transformation.

Route: hosted Stable Audio 3 audio-to-audio, async, `wav`.

Parameters:

```text
endpoint: POST /v2beta/audio/stable-audio/audio-to-audio
model: stable-audio-3
duration: 8
steps: 8
strength: 0.42
output_format: wav
seed: 0
```

Prompt:

```text
8-second soft premium onboarding chime derived from the source gesture, calm and reassuring, two-note identity preserved as a subtle motif, warm glass mallet tone layered with quiet felt piano resonance, gentle airy tail, close clean studio sound, no melody beyond the two-note motif, no voice, no percussion, no harsh digital sparkle.
```

Workflow: Submit the job, store the returned generation id, poll `/v2beta/audio/results/{id}`, save the returned seed and request id, then create a short candidate sheet with waveform, loudness, and subjective notes.

Likely failures: source motif disappears at high strength; source is too literal at low strength; tail is too long for UI. Adjust `strength` first, not prompt complexity.

### Example: inpaint a flawed game ambience

Intent: replace a 12-second section with accidental foreground chatter in an otherwise useful 90-second sci-fi hallway ambience.

Route: hosted Stable Audio 2.5 inpaint, synchronous, `wav`.

Parameters:

```text
endpoint: POST /v2beta/audio/stable-audio-2/inpaint
model: stable-audio-2.5
duration: 90
steps: 8
mask_start: 31.5
mask_end: 45.0
output_format: wav
seed: keep original asset seed if known; otherwise 0
```

Prompt:

```text
90-second seamless sci-fi hallway ambience, low ventilation rumble, distant electrical hum, subtle metallic room tone, occasional very soft servo movement far away, tense but not musical. The replacement section should match the surrounding ambience and contain no speech, no footsteps, no alarms, no rhythmic music.
```

Review: Listen across 28-48s on headphones for seam clicks, room-tone jump, new foreground events, and stereo image shifts. If the new section draws attention, reduce event density in the prompt and widen the mask slightly.

## Production QA

Before accepting a Stable Audio asset:

- Rights: inputs are cleared; prompt does not request a living artist, copyrighted song, or protected recording imitation; output is approved for the project's license context.
- Fit: duration, tempo, energy curve, section changes, and button ending serve the edit.
- Audio quality: no clipping, pumping, brittle highs, excessive low end, unwanted noise, hidden speech, or sudden artifacts.
- Editability: usable intro/outro handles, loop seam if needed, clean transient timing for SFX, and enough separation from narration/dialogue.
- Consistency: key, BPM, ambience perspective, reverb space, and stereo width match surrounding assets.
- Provenance: model, endpoint, parameters, seed/request/generation id, prompt, source rights, and file checksums are logged.
- Delivery: export an archival `wav` for production; derive compressed preview/delivery formats from the approved master.
