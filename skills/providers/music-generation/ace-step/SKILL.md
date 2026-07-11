---
name: ace-step
description: Use ACE-Step and ACE-Step 1.5 for local or hosted AI music generation, including text-to-music, lyrics-to-song, instrumental beds, covers, repainting, stem/track extraction, track completion, LoRA personalization, REST/Python/Gradio workflows, rights review, and music integration for video, ads, games, and social content.
---

# ACE-Step music production

Use this skill when a task calls for ACE-Step or ACE-Step 1.5 as the music engine, or when choosing an open-weight/local music-generation path for songs, background music, vocal tracks, covers, remixes, stems, or video soundtrack assets.

Treat ACE-Step as a fast generative music workstation, not a deterministic MIDI sequencer. It can follow style, lyric, structure, tempo, key, and reference-audio guidance, but outputs still need listening, selection, edits, mastering, rights checks, and delivery-format prep.

## Current facts to anchor on

Documented facts below were verified on 2026-07-10 from official ACE-Step GitHub, Hugging Face model cards, official docs, and arXiv reports.

- ACE-Step 1.5 is an open-source music foundation model co-led by ACE Studio and StepFun. It combines a planning language model with a diffusion transformer acoustic renderer.
- Main generation modes include text-to-music, lyrics-to-song, instrumental generation, cover/style transfer, repainting, LEGO/layered track generation, extraction, and completion. Some editing modes are documented as base-model-only.
- The official ACE-Step 1.5 Hugging Face card lists license `MIT`, model type `Text2Music`, 50+ languages, and consumer-hardware/local operation claims. The GitHub repository is MIT-licensed.
- The official API is asynchronous: submit with `POST /release_task`, poll `POST /query_result`, then download files via `/v1/audio?path=...`.
- Duration control exists through `audio_duration` / `duration` / `target_duration`; the official API docs list range 10-600 seconds. The technical report describes v1.5 as scaling from short loops to 10-minute compositions.
- Output format options documented in the API include `flac`, `mp3`, `opus`, `aac`, `wav`, and `wav32`.
- Official model-zoo guidance distinguishes DiT model families:
  - `acestep-v15-turbo`: fast, SFT, 8-step, high quality, medium diversity, medium fine-tunability; good first default for production iteration.
  - `acestep-v15-base`: 50-step, CFG-enabled, medium quality, high diversity, easy fine-tuning; use when you need base-only tasks, CFG, higher exploration, extraction/LEGO/complete support, or training/fine-tuning workflows.
  - `acestep-v15-sft`: 50-step, high quality, medium diversity, easy fine-tuning; use when you prefer SFT quality over turbo speed and do not need base-only capabilities.
  - XL models use a larger 4B DiT decoder; official docs say they target higher quality and require more VRAM, with >=12GB VRAM using offload/quantization or >=20GB without offload.
  - LM options include `acestep-5Hz-lm-0.6B`, `1.7B`, and `4B`; larger LMs are documented as stronger at composition and melody copying.
- Official docs state launch scripts exist for Windows CUDA, Windows ROCm, Linux CUDA, and macOS Apple Silicon MLX. Custom launch settings can be kept in `.env` using variables such as `ACESTEP_CONFIG_PATH`, `ACESTEP_LM_MODEL_PATH`, `PORT`, and `LANGUAGE`.
- ACE-Step DAW is a separate AGPL-3.0-or-later project and has different distribution obligations than the MIT model repository; do not assume MIT terms apply to a bundled DAW deployment.

Sources:

- Official repository: https://github.com/ace-step/ACE-Step-1.5
- Official model card: https://huggingface.co/ACE-Step/Ace-Step1.5
- Official API docs: https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/API.md
- Official inference docs: https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INFERENCE.md
- Official tutorial: https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md
- Official LoRA training tutorial: https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/LoRA_Training_Tutorial.md
- ACE-Step 1.5 technical report: https://arxiv.org/abs/2602.00744
- ACE-Step v1 technical report: https://arxiv.org/abs/2506.00045
- ACE-Step DAW repository: https://github.com/ace-step/ACE-Step-DAW

## Decide whether ACE-Step is the right tool

Prefer ACE-Step when the user wants:

- local/offline or self-hosted music generation;
- rapid iteration over many full-song candidates;
- vocals plus backing track from lyrics;
- instrumental beds for videos, ads, games, or podcasts;
- reference-audio workflows such as cover, repaint, extraction, completion, or style transfer;
- open-weight model custody and reproducible seeds/model metadata;
- low marginal cost after setup and less dependence on a hosted commercial music generator.

Do not present ACE-Step as a perfect fit when the user needs:

- guaranteed legally clear soundalikes of a living artist, protected song, or label catalog;
- exact note-level or word-level timing control;
- a final broadcast master with no human listening or mastering pass;
- a cloud API SLA unless a deployed ACE-Step server is actually available;
- a DAW distribution without reviewing AGPL obligations if using ACE-Step DAW.

If the user asks for "make it like [artist/song]," convert that into permitted, non-identifying musical attributes: era, instrumentation, tempo range, mix density, vocal energy, harmony language, production texture, mood, and structure. Avoid cloning protected voices or recreating recognizable melodies unless the user supplies rights/consent.

## Production workflow

1. Lock the deliverable: instrumental bed, full song with vocals, hook loop, cover, repaint/edit, stem extraction, track completion, or style exploration batch.
2. Choose runtime: local Gradio for interactive listening, REST API for pipelines/services, Python inference for scripted local generation, ACE-Step DAW only when layer-by-layer composition is desired and licensing is acceptable.
3. Choose model:
   - Start with `acestep-v15-turbo` for fast text-to-music/vocal ideation.
   - Switch to `base` or `xl-base` for base-only tasks, CFG, extraction, LEGO, completion, broader diversity, or fine-tuning.
   - Use XL only if hardware supports it and the quality gain matters more than latency/VRAM.
4. Write the caption and lyrics as separate controls.
5. Generate a batch of candidates. Use fixed seed only when reproducing or making small changes to a promising result.
6. Listen before judging from metadata. Score at minimum for structure, lyric intelligibility, vocal fit, mix balance, section transitions, artifacting, and rights risk.
7. Save custody metadata with every selected artifact: model, LM model, task type, prompt/caption, lyrics, duration, BPM/key/time signature if set, seed(s), inference steps, guidance/shift settings, source/reference audio provenance, output format, and verification date.
8. Prepare the asset for its destination: trim intro/outro, loop or fade, loudness-match, leave headroom for narration/dialogue, export stems if available/needed, and document AI involvement when required.

## Prompting: caption, lyrics, and metadata

The caption is the main sound-control input. It may be simple tags, comma-separated descriptors, or natural language. Make it specific enough to guide a producer, but not so overstuffed that the model receives contradictory targets.

Good caption ingredients:

- genre/subgenre and era;
- mood and energy;
- vocal identity in broad terms, not a real-person clone;
- lead instruments and rhythm section;
- production texture and mix style;
- intended use: trailer bed, TikTok hook, game loop, corporate explainer underscore, podcast theme;
- structure cues: intro, drop, chorus, bridge, outro;
- constraints: instrumental, no drums, sparse vocal, no heavy bass, loopable ending.

For songs with vocals, write lyrics with bracketed structure tags. Keep lines singable. Use one core metaphor or story thread. Avoid long prose paragraphs, inconsistent section labels, and section tags that fight the caption.

Common tags include `[Intro]`, `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`, and descriptive variants like `[Chorus - powerful]` or `[Bridge - whispered]`.

For instrumental-only work, put `[Instrumental]` in lyrics or use instrumental structure tags, for example:

```text
[Intro - sparse pads]
[Main Theme - warm piano and soft pulse]
[Lift - added strings, brighter harmony]
[Outro - clean loopable tail]
```

Metadata is optional guidance, not a hard transport grid. Use it when the brief requires a tempo family, key color, language, or target length:

- `bpm`: documented range 30-300; common tempos are more reliable than extremes.
- `key_scale`: examples include `C Major`, `Am`, `F# Minor`; common keys are more likely to hold.
- `time_signature`: documented API form includes 2, 3, 4, 6 for 2/4, 3/4, 4/4, 6/8.
- `audio_duration`: documented API range 10-600 seconds; short clips and 2-4 minute songs are usually safer than very long single generations.
- `vocal_language`: set when lyrics language matters; otherwise let the LM infer.

Use `thinking=true` when you want the LM planner to generate codes or fill missing metadata for text-to-music, LEGO, or completion. Official API docs state the LM is skipped for cover, repaint, and extract tasks.

Use `use_format=true` or `/format_input` when the user supplies rough lyrics/caption and wants the LM to clean up formatting and metadata. Review the reformatted lyrics before production if meaning or brand language matters.

## Runtime patterns

### REST API pattern

Use this for production systems and video pipelines. Submit, poll, then download.

```json
{
  "prompt": "cinematic synthwave product launch bed, 118 BPM, pulsing analog bass, glossy arpeggios, confident but not aggressive, clean mix with space for voiceover, 30-second social ad structure",
  "lyrics": "[Instrumental]\n[Intro - filtered pulse]\n[Main Theme - bright synth hook]\n[Lift - wider drums and strings]\n[Outro - clean button ending]",
  "model": "acestep-v15-turbo",
  "thinking": true,
  "audio_duration": 30,
  "bpm": 118,
  "time_signature": "4",
  "audio_format": "wav",
  "batch_size": 4,
  "use_random_seed": true,
  "inference_steps": 8
}
```

API facts to remember:

- `POST /release_task` returns a task id.
- `POST /query_result` accepts task id lists and returns status 0 running, 1 succeeded, or 2 failed.
- Result records may include file URL, prompt, lyrics, metadata, seed values, LM model, and DiT model.
- Local deployments may have optional API-key auth via body `ai_token` or `Authorization: Bearer ...`.
- For uploaded reference/source audio, use multipart fields such as `reference_audio` / `ref_audio` or `src_audio` / `ctx_audio`.

### Python/local inference pattern

Use Python inference when the agent needs local scripting, direct file custody, or non-HTTP integration. Keep the generated file, params, and logs together in the project asset directory. Use official docs for exact class/function names in the installed version; ACE-Step docs evolve quickly.

### Gradio/UI pattern

Use Gradio when human taste selection matters. Generate batches, listen, mark candidates, refine caption/lyrics/metadata, then export final audio and a parameter record. This is often better than one "perfect prompt" because music taste is subjective and small seed/model changes can dominate.

### ACE-Step DAW pattern

Use ACE-Step DAW when the user wants layered composition where new tracks are generated with awareness of earlier tracks. Review AGPL-3.0-or-later obligations before hosting or bundling. The DAW README states it proxies `/api` to an ACE-Step 1.5 backend at `localhost:8001`, and can be configured for the cloud ACE Music API.

## Task-specific guidance

### Instrumental background music for video

Prioritize editability over full-song impressiveness:

- ask for or infer platform, duration, voiceover/dialogue density, mood, and loop/fade needs;
- avoid busy lead vocals unless the user explicitly wants lyrics;
- request mix space: "wide but uncluttered," "no lead vocal," "low-mid controlled," "dialogue-safe";
- generate slightly longer than needed, then trim or loop;
- export WAV or FLAC for editing, MP3/AAC for lightweight preview;
- loudness-match after edit, not before.

### Full song with vocals

Separate creative writing from model prompting:

- make the lyric fit a singable structure;
- keep chorus short and repeatable;
- use tags for performance changes;
- set `vocal_language` if language is non-obvious or mixed;
- batch several candidates and score lyric alignment, not just vibe;
- repair weak sections with repainting only when source audio and base/edit-capable model are available.

### Covers and style transfer

Use only with rights/consent for the source audio and any voice/style reference. Avoid celebrity voice cloning or misleading attribution. The model can transform source material, but legal risk depends on the source, reference, prompt, and distribution context.

Operationally:

- supply source audio through `src_audio` / `src_audio_path`;
- set `task_type="cover"` where supported;
- tune `audio_cover_strength`: lower values are documented for style transfer behavior;
- do not use `thinking=true` as a quality lever here; official docs say LM planning is skipped for cover tasks.

### Repainting

Use repainting to replace or regenerate a time span while preserving surrounding context:

- provide `src_audio`;
- set `task_type="repaint"`;
- specify `repainting_start` and `repainting_end`;
- give a concise `instruction` and, if supported, a caption describing the desired replacement;
- audition transitions at both boundaries.

### Extraction, LEGO, and completion

Use base-capable models when the documented task requires them.

- `extract`: isolate a requested track from a mix; instruction must name the target stem.
- `lego`: build layer by layer so later parts "hear" earlier tracks; useful for drums -> bass -> harmony -> lead/vocal workflows.
- `complete`: add specified instruments to an incomplete track; requires source audio, instruction, and desired style caption.

Available track names and exact instructions are version-specific. Check the installed official inference/API docs before committing to a production contract.

### LoRA personalization

Use LoRA/LoKr only when the user has rights to the training songs and wants a recurring style/persona. Do not train on commercial songs, artist catalogs, or private voice recordings without clear permission. Record dataset provenance and adapter version.

Prefer LoRA for reusable brand sonic identity, game soundtrack palette, creator jingle style, or a licensed in-house artist's style. Do not use it as a shortcut for "make a track by famous artist X."

## Iteration strategy

Use batch exploration first, then controlled refinement:

- Round 1: broad caption + batch 4-8 candidates + random seed.
- Round 2: keep the best direction, remove contradictory terms, lock duration/BPM if needed.
- Round 3: fix seed only if the candidate is close and you are testing one or two changes.
- Round 4: use edit modes or post-production for local repairs rather than rewriting the whole song.

Common failure modes and repairs:

- muddy mix: simplify instrumentation, ask for sparse arrangement, lower density, leave space for voiceover;
- weak chorus/hook: shorten chorus text, tag it as `[Chorus - powerful]`, add one memorable instrument;
- lyric slurring: reduce syllables per line, use clearer structure tags, try another seed;
- generic output: add production context, unusual but coherent instrumentation, one distinctive rhythmic or harmonic cue;
- prompt conflict: remove competing genres, impossible instrumentation, or "soft aggressive epic minimal maximal" stacks;
- duration drift/repetition: generate shorter segments, trim, or assemble in post;
- style too close to a protected reference: rewrite into abstract attributes and regenerate.

## QA checklist before delivery

Listen all the way through on headphones and speakers if possible.

Check:

- beginning and ending usable for the edit;
- no obvious clicks, dropouts, warbles, harsh clipping, or sudden volume jumps;
- lyrics match the approved text closely enough for the use case;
- no accidental real-person name, trademark, slur, or unsafe lyric;
- melody/hook is not intentionally copying a protected work;
- music leaves space for narration, dialogue, SFX, or captions where needed;
- loop points, fades, and stems work in the final timeline;
- exported format matches downstream needs;
- metadata and source/reference provenance are saved;
- AI involvement and license/permission notes are documented for commercial releases.

## Example: 30-second SaaS launch underscore

Intent: background music for a product-launch video with voiceover.

Use `acestep-v15-turbo` for fast ideation unless the installed runtime defaults otherwise. Export WAV for editing.

Request:

```json
{
  "prompt": "premium minimalist SaaS launch underscore, confident and optimistic, 112 BPM, warm analog pulse, soft kick, muted claps, airy piano motif, restrained strings lift at the end, clean modern mix, no lead vocal, dialogue-safe, suitable for a 30-second product reveal",
  "lyrics": "[Instrumental]\n[Intro - soft pulse and piano]\n[Build - subtle percussion and wider pads]\n[Reveal - restrained strings lift]\n[Outro - clean button ending]",
  "model": "acestep-v15-turbo",
  "thinking": true,
  "audio_duration": 34,
  "bpm": 112,
  "time_signature": "4",
  "audio_format": "wav",
  "batch_size": 6,
  "inference_steps": 8,
  "use_random_seed": true
}
```

Why structured this way: generate a few seconds extra for trim handles, request no lead vocal, describe mix space, and make the ending editorially useful.

Likely failures: too much lead melody or drum density. Repair by adding "no solo lead synth, no busy hi-hats, keep midrange open for narration" and reducing instrumentation.

## Example: multilingual short song demo

Intent: a 45-second bilingual creator jingle, not imitating a real artist.

```json
{
  "prompt": "upbeat indie pop jingle, friendly mixed English and Spanish vocal, handclaps, nylon guitar, light bass, bright chorus, social media creator intro, warm and human, not overproduced",
  "lyrics": "[Intro - guitar]\n[Verse 1]\nMorning light, we start again\nPequeños sueños, paso a paso\n[Chorus - bright]\nHere we go, aquí estamos\nMake it real, lo intentamos\n[Outro - claps]\nHere we go, aquí estamos",
  "model": "acestep-v15-turbo",
  "thinking": true,
  "vocal_language": "es",
  "audio_duration": 45,
  "bpm": 124,
  "audio_format": "wav",
  "batch_size": 4
}
```

Why structured this way: the lyrics are short and singable, the caption explains bilingual intent, and the chorus is repeatable for branding.

QA focus: intelligibility, awkward language mixing, vocal artifacts, and whether the jingle can be trimmed to 10-15 seconds.

## Example: rights-safe style rewrite from a risky user prompt

User asks: "Make a track exactly like Taylor Swift's latest single, same vocal vibe."

Respond by reframing:

```text
I can't help clone a real artist's voice or recreate a specific protected song. I can make a rights-safer pop track using broad attributes: confessional lyrics, bright acoustic guitar, clean pop drums, intimate female vocal tone, polished modern mix, and a lift into a catchy chorus.
```

Then generate:

```json
{
  "prompt": "modern confessional pop, intimate female vocal tone, bright acoustic guitar, clean pop drums, polished radio mix, emotional but optimistic, catchy chorus, original melody, no artist imitation",
  "lyrics": "[Verse 1]\nI kept a note beside the door\nA little truth I hid before\n[Pre-Chorus]\nNow every streetlight points me home\n[Chorus - lifted]\nI am not the shadow anymore\nI open up the windows\nI am walking through the door",
  "model": "acestep-v15-turbo",
  "thinking": true,
  "audio_duration": 90,
  "audio_format": "wav",
  "batch_size": 4
}
```

## Example: repaint a weak bridge

Intent: keep a selected song but replace a dull bridge from 72-96 seconds.

Use an edit-capable/base path if the installed model/docs require base for repaint.

```json
{
  "task_type": "repaint",
  "src_audio_path": "/project/assets/music/song_candidate_03.wav",
  "repainting_start": 72.0,
  "repainting_end": 96.0,
  "instruction": "Replace this bridge with a quieter half-time section, whispered vocal feel, reduced drums, and a smooth rise into the final chorus.",
  "prompt": "same song identity, intimate half-time bridge, sparse drums, warm pad, whispered vocal feel, smooth transition back to bright chorus",
  "model": "acestep-v15-base",
  "audio_format": "wav",
  "batch_size": 3
}
```

Review the repair by listening from 65-105 seconds, not only the edited span.

