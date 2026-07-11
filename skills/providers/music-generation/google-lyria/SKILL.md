---
name: google-lyria
description: Use Google Lyria music generation models through Google Cloud / Vertex AI / Gemini Enterprise Agent Platform for production music beds, songs, vocal tracks, image-conditioned music, short-form social audio, ad music, and video scoring. Covers Lyria 2, Lyria 3 Clip, and Lyria 3 Pro model selection, prompt construction, rights/privacy checks, SynthID/C2PA provenance, artifact custody, and QA.
---

# Google Lyria music generation

Use this skill when a production plan calls for Google Lyria as the music-generation provider. It is for selecting the right Lyria model, writing usable music prompts, deciding when Lyria is inappropriate, and packaging generated music safely for videos, ads, social clips, apps, or internal content.

Facts in this skill were verified against official Google Cloud and Google DeepMind sources on 2026-07-10. Treat model IDs, limits, launch stages, pricing, regions, and policy behavior as volatile; re-check official docs before committing spend, compliance claims, or product launches.

## Provider boundary

Documented facts:

- Lyria is Google's music-generation model family. Lyria 3 is documented as synthesizing music from text prompts and outputting audio music plus text lyrics.
- Google Cloud documentation currently appears under Gemini Enterprise Agent Platform and may be reached from Vertex AI / Generative AI on Vertex AI links. Do not assume an older Vertex AI URL means the API contract is unchanged.
- The production-relevant Google Cloud models are:
  - `lyria-3-pro-preview`: preview model for full-song music generation.
  - `lyria-3-clip-preview`: preview model for 30-second clips.
  - `lyria-002`: Lyria 2, documented as generally available and instrumental-only in the API reference.
- Lyria is not a general audio editor, stem separator, music transcription tool, MIDI renderer, or licensed-catalog search engine. Use another tool if the user needs exact beat matching to an existing song, remixing of copyrighted source music, stem extraction, or guaranteed legal clearance.

Production implication:

Use Lyria for new music creation, not for reproducing existing songs, mimicking named artists, cloning voices, or manufacturing "soundalikes." If the brief references a commercial track, convert it into neutral musical attributes: tempo, instrumentation, energy curve, era, arrangement density, and emotional function.

## Model choice

Use `lyria-3-pro-preview` when the deliverable needs a coherent song or long-form music bed: intros, verses, choruses, bridges, vocal sections, timed lyrics, or scene-by-scene scoring up to roughly three minutes. Official docs list maximum clip length as 184 seconds, one clip per prompt, 44.1 kHz, 192 kbps, MP3 output, global region, preview launch stage, and 2026-03-25 release date for this model.

Use `lyria-3-clip-preview` when the deliverable needs fast exploration, variations, social stings, short ads, UI loops, or a 30-second scene bed. Official docs list maximum clip length as 30 seconds, one clip per prompt, 44.1 kHz, 192 kbps, MP3 output, global region, preview launch stage, and 2026-03-25 release date.

Use `lyria-002` only when the job specifically benefits from the GA Lyria 2 API or from deterministic seeding / `sample_count` behavior. The Lyria 2 API reference documents a `predict` request with `prompt`, optional `negative_prompt`, optional `seed`, optional `sample_count`, base64 WAV responses, and 48 kHz WAV instrumental clips. Google's "generate music" guide says each Lyria 2 clip is 32.8 seconds long; the Lyria API reference says 30-second clips. Record this discrepancy in production notes if duration matters.

Do not choose Lyria 3 when the job requires generally available status, negative prompting, or multiple clips per prompt. The Lyria 3 model page documents negative prompting as not supported, maximum clips per prompt as one, and preview launch stage for both Lyria 3 models.

## API routes and request shape

Documented Lyria 3 route, verified 2026-07-10:

```http
POST https://aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/global/interactions
```

Minimal Lyria 3 request pattern:

```json
{
  "model": "lyria-3-pro-preview",
  "input": [
    {
      "type": "text",
      "text": "Create a 90-second instrumental product-launch bed..."
    }
  ]
}
```

Lyria 3 can include optional image input by Cloud Storage URI or base64 data in the interaction input array. Use image conditioning when an approved moodboard, key visual, brand frame, or storyboard genuinely contains visual information that should shape the music. Do not include confidential images unless the project's Google Cloud data-retention and access controls permit it.

Documented Lyria 2 route pattern, verified 2026-07-10:

```http
POST https://LOCATION-aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/publishers/google/models/lyria-002:predict
```

Lyria 2 request pattern:

```json
{
  "instances": [
    {
      "prompt": "A calm acoustic folk instrumental with gentle guitar and soft strings.",
      "negative_prompt": "drums, electric guitar",
      "seed": 98765
    }
  ],
  "parameters": {}
}
```

For Lyria 2, do not combine `seed` and `sample_count` in the same request. Use `seed` for approximate reproducibility and `sample_count` for exploration. Decode `predictions[].audioContent` from base64 and write it as a WAV file.

## Prompt construction

Documented controls:

- Lyria prompting guidance asks for descriptive, specific prompts with genre, mood, stylistic characteristics, instruments, tempo/rhythm, and iteration.
- Lyria 3 supports vocals, instrumental mode, lyrics generation, user-provided lyrics, image-to-music, prompt rewriting, audio watermarking, C2PA Content Credentials, input filtering, output recitation checks, and output vocal-likeness filtering.
- Lyria 3 Pro supports duration, BPM, and intensity controls; Lyria 3 Clip supports BPM and intensity controls.
- Lyria 3 vocal generation supports English, German, Spanish, French, Hindi, Japanese, Korean, and Portuguese. The same languages are listed in the Lyria 3 model technical specs.
- To provide lyrics in Lyria 3, Google's prompt guide says to type `Lyrics:` before lines the model should sing.
- For detailed structure, Google's prompt guide shows timestamps in `[mm:ss - mm:ss]` format, song key, BPM, and intensity values.

Production heuristic:

Write prompts as a music brief, not as keyword soup. Include the deliverable role, total duration, edit requirements, genre/era, instrumentation, rhythm, arrangement arc, emotional function, vocal/lyric boundary, mix constraints, and hard exclusions in plain language. Use named artists only if the user has explicit authorization and the platform policy allows it; otherwise describe traits without names.

Useful prompt slots:

```text
Purpose: where the track will be used and what it must do for the edit.
Duration: target length and whether it must resolve cleanly.
Mode: instrumental, vocal, generated lyrics, or user-provided lyrics.
Style: genre, era, geography, arrangement density, production finish.
Tempo/rhythm: BPM or tempo feel; straight/swing/syncopated; beat drop timing.
Instrumentation: lead instruments, supporting textures, drums/percussion, bass.
Emotion: audience feeling at each section.
Structure: timestamped sections, intensity, key, transitions, ending.
Mix notes: leave space for narration/dialogue, avoid harsh highs, keep low-end controlled.
Rights/safety: avoid named-artist imitation, recognizable melodies, quoted lyrics, or vocal likeness.
```

For video scoring, prompt against the edit timeline. Give timecoded emotional actions rather than vague style labels:

```text
Create a 60-second instrumental bed for a SaaS launch video, 96 BPM, modern electronic-pop with warm analog synths, muted guitar pulses, soft sub bass, and clean handclaps. Leave room for spoken narration: no lead vocal, no busy top-line melody, no harsh risers.

[00:00 - 00:08] Curious intro: filtered synth pulse, low intensity 2/10, a sense of possibility.
[00:08 - 00:22] Product reveal: add tight percussion and brighter chord stabs, intensity 4/10.
[00:22 - 00:42] Momentum: fuller drums, confident bass movement, optimistic but not cheesy, intensity 6/10.
[00:42 - 00:55] Proof and trust: pull back the lead melody, keep groove steady for VO clarity, intensity 4/10.
[00:55 - 01:00] Logo resolve: clean final cadence with a short reverb tail that can be cut at exactly 60 seconds.
```

For Lyria 3 Pro vocal songs, make the vocal brief explicit:

```text
Create a 2-minute, 30-second upbeat pop-soul song for a brand anthem. Warm, confident, human, not theatrical. 112 BPM, A major, live bass, tight drums, bright piano, subtle brass swells. Female alto lead vocal in English, expressive but natural, with a small backing group only in choruses. Avoid any named-artist resemblance.

Lyrics:
Verse 1:
We built a light for the long way home
...

[00:00 - 00:12] Intro: piano hook, no vocal, intensity 2/10.
[00:12 - 00:40] Verse 1: intimate lead vocal, sparse groove, intensity 3/10.
[00:40 - 01:05] Chorus: backing vocals answer the last line of each phrase, intensity 7/10.
```

For Lyria 2 instrumental clips, use `negative_prompt` instead of unsupported Lyria 3-style negative instructions:

```json
{
  "instances": [
    {
      "prompt": "A 30-second cinematic ambient instrumental bed for a healthcare explainer: gentle felt piano, warm pads, slow pulse, calm trust, minimal melody, soft ending.",
      "negative_prompt": "vocals, choir, drums, suspense, dissonance, celebrity artist style",
      "seed": 412991
    }
  ],
  "parameters": {}
}
```

## Rights, consent, and commercial use gate

Before generation, check:

- Does the user need commercial use, broadcast, paid ads, platform monetization, or client delivery? If yes, verify the governing Google Cloud agreement, product launch stage, and client legal policy. Lyria 3 is preview; Google Cloud docs state customers may elect to use this preview offering for production or commercial purposes, subject to the agreement under which they access Google Cloud.
- Does the prompt request a named artist, celebrity, living person, estate-controlled voice, specific song, quoted lyrics, label catalog, copyrighted melody, or "sound exactly like" direction? If yes, stop and ask for proof of rights or rewrite as neutral musical attributes.
- Are user-provided lyrics original, licensed, public-domain, or otherwise cleared? If not, do not use them.
- Does the brief involve deception, undisclosed impersonation, misleading provenance, sensitive political persuasion, hate, sexual content, self-harm, illegal activity, or privacy/IP violations? Google's Generative AI Prohibited Use Policy applies.
- Does the output need provenance disclosure? For public/client content, preserve SynthID and C2PA where possible and disclose AI-generated music according to platform, client, and jurisdiction requirements.

Production heuristic:

Treat Lyria output as a generated asset that still needs normal rights review. Watermarking, filters, and indemnity language do not guarantee that a specific track is usable in every ad, territory, or license context.

## Privacy, security, and retention

Documented Google Cloud behavior, verified 2026-07-10:

- Google Cloud says it will not use customer data to train or fine-tune AI/ML models without prior permission or instruction for managed models on Gemini Enterprise Agent Platform, including GA and pre-GA models.
- Request-response logging is disabled by default, but can be enabled per model and project. Leave it disabled for zero-data-retention goals.
- Google may log prompts for abuse monitoring for Google models under some Google Cloud Platform Terms of Service contexts; customers seeking zero data retention may need to request an exception.
- In-memory caching for Google published Gemini models is described as project-isolated, not stored at rest, with a 24-hour TTL, and can be disabled at project level. Confirm whether this applies to the specific Lyria endpoint before claiming zero retention.

Production implications:

- Do not place unreleased lyrics, confidential scripts, private user data, unreleased product names, or licensed reference images into prompts unless the project's data governance permits it.
- Store generated audio, prompts, model IDs, timestamps, and source images in the project asset ledger. Restrict access as you would for unreleased campaign audio.
- If the job is regulated or under NDA, document the exact endpoint, region (`global` for Lyria 3 as documented), logging settings, retention assumptions, and who approved them.

## Provenance and artifact custody

Documented facts:

- Google states Lyria audio is watermarked with SynthID. DeepMind describes SynthID audio watermarks as inaudible and designed to survive common modifications such as noise addition, MP3 compression, and speed changes.
- Lyria 3 model specs list Content Credentials (C2PA) as supported.
- Google's Content Credentials documentation says verification can fail if a C2PA-compliant media file is modified using a non-C2PA-aware tool.

Custody workflow:

1. Save the raw provider output exactly as returned.
2. Save a sidecar production record outside the media file: provider, model ID, endpoint, prompt, image references, request time, response ID if available, output filename, duration, sample rate/bitrate, safety/rejection notes, and reviewer.
3. Preserve a raw copy before trimming, loudness normalization, looping, or muxing into video.
4. When exporting edits, note that C2PA metadata may be stripped by ordinary audio/video tools. Keep the raw artifact for provenance even if the final MP4 loses embedded credentials.
5. Do not claim SynthID or C2PA makes the track tamper-proof. Present it as provenance support, not legal or forensic proof.

## Music QA for production

Review generated tracks before using them:

- Prompt adherence: duration, structure, instruments, BPM/tempo feel, vocal/lyric choices, language, and scene timing.
- Edit utility: clean intro, no awkward pickup if starting under VO, usable ending, loop potential, enough stems/versions if the edit needs them.
- Mix safety: headroom, low-end control, no piercing highs, no lead melody fighting narration, no vocal where an instrumental was requested.
- Rights risk: no recognizable existing melody, lyric fragment, named-artist likeness, celebrity voice, or style imitation that is too specific.
- Brand fit: emotional tone matches the product and audience; no unintentional comedy, menace, sensuality, or cultural mismatch.
- Platform fit: short-form hook in the first seconds, clean logo resolve, safe loudness target after mastering, no unlicensed samples.
- Provenance: raw output stored, request metadata recorded, AI-generation disclosure and watermark/C2PA notes preserved.

Iteration tactics:

- If the track is too busy, reduce lead instruments, ask for "underscore," specify "leave room for narration," and lower intensity.
- If the track misses the emotional arc, add timestamped scene functions and intensity numbers.
- If vocals appear when not wanted, use Lyria 3 instrumental mode language; for Lyria 2, add `negative_prompt: "vocals, choir, spoken words"`.
- If the ending is unusable, request a resolved final cadence and a short reverb tail.
- If the result sounds like a known artist, remove era/genre combinations that overconstrain toward that artist and add "avoid named-artist resemblance."

## Example: choosing between Lyria models

User request: "Make background music for a 45-second paid social ad. No lyrics; it needs to sit under narration and hit a logo at the end."

Recommended decision:

Use `lyria-3-pro-preview` if the ad needs exact 45-second structure and scene-timed music. Use `lyria-3-clip-preview` only if a 30-second cue can be looped or extended in edit. Use `lyria-002` if the project requires GA status and instrumental-only output is acceptable, but plan around a roughly 30-second WAV and possible editing.

Prompt:

```text
Create a 45-second instrumental bed for a paid social ad under spoken narration. Modern optimistic electronic-pop, 104 BPM, warm analog synth chords, muted guitar pulse, tight light percussion, controlled sub bass. No vocals, no choir, no spoken words, no lead melody that competes with narration. Confident, premium, friendly, not childish.

[00:00 - 00:05] Hook: immediate soft pulse and warm chord, intensity 3/10.
[00:05 - 00:20] Problem/setup: restrained groove, lots of space for VO, intensity 4/10.
[00:20 - 00:36] Product benefits: fuller drums and brighter synth layers, intensity 6/10.
[00:36 - 00:45] Logo resolve: pull back slightly, clean uplifting cadence, final hit at 00:43 with a short tail ending by 00:45.
```

QA focus:

Check that any generated vocal-like texture is absent, the logo cadence lands close enough for edit, and the music does not mask narration after compression for mobile platforms.

## Key official sources

- Google Cloud, "Lyria 3" model page: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/lyria/lyria-3
- Google Cloud, "Generate music with Lyria": https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/music/generate-music
- Google Cloud, "Lyria API" (`lyria-002`): https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/lyria-music-generation
- Google Cloud, "Lyria music generation prompt guide": https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/music/music-gen-prompt-guide
- Google Cloud Blog, "Lyria 3 and Lyria 3 Pro on Vertex AI": https://cloud.google.com/blog/products/ai-machine-learning/lyria-3-and-lyria-3-pro-on-vertex-ai
- Google Cloud Blog, "Ultimate prompting guide for Lyria 3 Pro": https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-lyria-3-pro
- Google DeepMind, "Lyria 3" model card: https://deepmind.google/models/model-cards/lyria-3/
- Google DeepMind, "Lyria 3": https://deepmind.google/models/lyria/
- Google DeepMind, "SynthID": https://deepmind.google/models/synthid/
- Google Cloud, "Gemini Enterprise Agent Platform and zero data retention": https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/zero-data-retention
- Google, "Generative AI Prohibited Use Policy": https://policies.google.com/terms/generative-ai/use-policy
- Google Cloud, "Content Credentials": https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/content-credentials
