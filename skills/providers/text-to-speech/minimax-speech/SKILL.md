---
name: minimax-speech
description: Use this skill when producing speech, narration, dubbing, localization, advertising voice, voice-clone previews, or interactive voice with MiniMax speech/audio APIs. It covers MiniMax T2A HTTP, WebSocket streaming, async long-form TTS, Speech 2.8/2.6/02 model selection, system and custom voices, rapid voice cloning, voice design, pronunciation/language/emotion controls, pricing and limits, artifact custody, consent and rights checks, and production QA.
---

# MiniMax speech production

Use MiniMax when the production goal is generated speech: narration, localized VO, ad reads, audiobook-style segments, synthetic dialogue, product walkthroughs, voice-agent responses, or approved voice cloning. Do not use this skill for MiniMax video, music generation, image generation, or general LLM calls except where they affect speech production.

The facts below were verified against official MiniMax API documentation, release notes, pricing, and policy pages on 2026-07-10. Treat model IDs, prices, rate limits, retention windows, voice lists, and policy language as volatile; re-check before a paid or regulated production run.

## Capability boundary

Documented MiniMax speech capabilities:

- Synchronous text-to-audio over HTTP: `POST https://api.minimax.io/v1/t2a_v2`.
- Synchronous text-to-audio over WebSocket: `wss://api.minimax.io/ws/v1/t2a_v2`.
- Asynchronous long-form text-to-audio: create a task with `POST /v1/t2a_async_v2`, query it, then retrieve the generated file.
- System voices, cloned voices, and text-designed voices, queryable through Voice Management.
- Rapid voice cloning through file upload plus `POST /v1/voice_clone`.
- Voice design through `POST /v1/voice_design`, where a text description produces a generated `voice_id` and preview audio.
- Subtitle timestamp generation from TTS (`sentence`, `word`, or `word_streaming` depending on streaming mode).
- An ASR-based validation check inside voice cloning when `text_validation` is provided.

Not documented as standalone production APIs in the official docs index as of 2026-07-10:

- Standalone speech recognition / transcription.
- Speech-to-speech dubbing.
- Voice conversion from arbitrary source speech to a target voice while preserving timing.
- A separate low-latency conversational turn-taking API beyond T2A WebSocket streaming.

If a user asks for transcription, voice conversion, or full dubbing, combine MiniMax TTS with another documented ASR/alignment/dubbing provider, or explain that MiniMax’s official speech surface does not currently expose that workflow directly.

## Model selection

Use the newest supported model unless a constraint points elsewhere.

- `speech-2.8-hd`: choose for final narration, ads, audiobooks, brand films, expressive dialogue, and sound-tag support where quality matters more than turnaround.
- `speech-2.8-turbo`: choose for interactive voice, review drafts, batch localization, cost-sensitive social variants, and latency-sensitive WebSocket work.
- `speech-2.6-hd`: use only when a legacy production has already approved its sound, or when testing shows it handles a specific cloned voice better.
- `speech-2.6-turbo`: use for legacy or high-volume cases that were tuned around 2.6 behavior.
- `speech-02-hd` and `speech-02-turbo`: legacy; keep for continuity with old approved voices or third-party wrappers that have not upgraded.
- `speech-01-*`: legacy compatibility only.

Documented model facts as of 2026-07-10:

- The API accepts `speech-2.8-hd`, `speech-2.8-turbo`, `speech-2.6-hd`, `speech-2.6-turbo`, `speech-02-hd`, `speech-02-turbo`, `speech-01-hd`, and `speech-01-turbo`.
- MiniMax’s model overview lists Speech 2.8 and 2.6 as supporting 40 languages and 7 emotions; Speech-02 is listed with 24 languages and 7 emotions.
- Interjection / natural sound tags are documented only for `speech-2.8-hd` and `speech-2.8-turbo`.

Production heuristic:

- HD is the “approve the master” path; Turbo is the “iterate and serve” path. For a serious piece, cast and proof in Turbo if needed, then render finals in HD and do a fresh QA pass because timing and prosody may shift.

## Endpoint choice

Use HTTP when the full audio can be generated before playback and the text is under the sync limit. Use WebSocket when the user hears speech as it is generated, or when the script is over 3,000 characters but still within the synchronous 10,000-character ceiling. Use async for long-form narration, audiobook chapters, many-file jobs, or anything approaching the 50,000-character async text limit.

Documented limits and lifecycle:

- HTTP T2A text must be less than 10,000 characters; MiniMax recommends streaming for text over 3,000 characters.
- Async T2A text accepts up to 50,000 characters directly and is mutually exclusive with `text_file_id`; official async guide material also describes long-form file workflows.
- WebSocket starts with `task_start`, accepts one or more `task_continue` text events after `task_started`, and ends with `task_finish`.
- A WebSocket connection can close automatically if no new event is sent within 120 seconds after receiving the last result.
- HTTP non-streaming can return `hex` audio or a URL; returned URLs are documented as valid for 24 hours.
- Async task creation returns `task_id`, `task_token`, `file_id`, and `usage_characters`; after completion, retrieve the file through File Retrieve. The async docs warn that the download URL is valid for 9 hours from generation and generated data is lost after expiration.

Production heuristic:

- For video narration, split scripts by editorial unit, not by maximum API length: intro, chapter, scene, disclaimer, CTA. Smaller units make timing repair, substitutions, and human approval much easier.

## Core T2A controls

Use a minimal request first, then add controls only for the production problem you need to solve.

Common controls:

- `voice_setting.voice_id`: system, cloned, or voice-designed ID.
- `voice_setting.speed`: `0.5` to `2`; use small changes such as `0.92`, `1.0`, `1.08`.
- `voice_setting.vol`: `(0, 10]`; keep near `1` and normalize in post unless a voice is consistently underpowered.
- `voice_setting.pitch`: `-12` to `12`; prefer `-2` to `2` for natural production.
- `voice_setting.emotion`: documented values include `happy`, `sad`, `angry`, `fearful`, `disgusted`, `surprised`, `calm`, `fluent`, and `whisper`, with `fluent`/`whisper` documented only for 2.6 models and `whisper` not supported by 2.8.
- Text normalization: useful for digit-heavy scripts; expect slightly higher latency. Current official specs are inconsistent about the field name (`text_normalization` in the HTTP OpenAPI, `english_normalization` in async/WebSocket-related specs), so verify the exact parameter name for the endpoint before implementation.
- `language_boost`: set a specific language or dialect when the script is known; use `auto` when uncertain. Do not assume Speech-01/02 support Persian, Filipino, or Tamil even though those values appear in the enum.
- `pronunciation_dict.tone`: define specific pronunciation substitutions such as acronym expansions.
- Inline pronunciation: wrap IPA, Mandarin Pinyin with tone number, or Cantonese Jyutping with tone number in parentheses near the target word.
- Pause markers: insert `<#x#>` between speakable text segments, where `x` is `0.01` to `99.99` seconds. Do not place pause markers consecutively.
- `audio_setting.sample_rate`: documented values include `8000`, `16000`, `22050`, `24000`, `32000`, and `44100`; use `32000` for API default, `44100` if the rest of the audio post chain requires it, and `8000` only for telephony-style tests.
- `audio_setting.bitrate`: documented values include `32000`, `64000`, `128000`, and `256000`; relevant to MP3.
- `audio_setting.format`: rendered HTTP docs list `mp3`, `wav`, and `flac` for non-streaming and `mp3` for streaming, while current embedded OpenAPI specs also expose `pcm`, `pcmu_raw`, `pcmu_wav`, and `opus` with endpoint-specific caveats. Verify the exact format set before telephony, raw PCM, or Opus workflows.
- `audio_setting.channel`: `1` mono or `2` stereo; mono is usually best for VO stems.
- `subtitle_enable` and `subtitle_type`: enable sentence or word timestamps for video caption alignment; `word_streaming` is only valid with `stream=true`.
- `voice_modify`: deeper/brighter pitch, stronger/softer intensity, fuller/crisper timbre, and one optional effect such as `spacious_echo`, `auditorium_echo`, `lofi_telephone`, or `robotic`.

Production heuristic:

- Avoid stacking too many controls. If a line needs emotion, pace, pronunciation, pause, and voice modification all at once, rewrite the line first. Most “bad TTS” is script shape, not parameter failure.

## Writing scripts for MiniMax voices

Write for a performer, not for a page.

- Keep sentences short enough to speak in one breath.
- Put one intent per sentence.
- Use line breaks at performance beats.
- Write numbers the way they should be spoken when precision matters.
- For acronyms, decide between spelled letters, a word, or an expansion before generation.
- Use punctuation for syntax, not as a timing interface; use pause markers for precise pauses.
- For multilingual content, avoid switching languages inside a sentence unless code-switching is the intended performance.
- For localization, localize idioms and legal/regulatory lines before TTS. Do not rely on `language_boost` to fix a literal translation.

Sound tags on 2.8:

- Use tags such as `(laughs)`, `(sighs)`, `(breath)`, `(inhale)`, `(exhale)`, `(gasps)`, `(coughs)`, `(humming)`, or similar documented tags only where a human would actually make that sound.
- Sound tags are performance directions inside the text stream, not guaranteed sound-effect assets. If the sound is editorially important, render it as its own take and review it separately.

## Voice casting and voice IDs

Always treat the voice as a production decision.

1. Query available voices with Voice Management instead of hardcoding from memory.
2. Generate short auditions from the same 60–120 words of the actual script.
3. Compare on intelligibility, brand fit, fatigue, emotional range, pronunciation, and editability.
4. Lock the voice ID, model, speed, pitch, and language settings in the production notes.
5. Render a full script only after a human or QA pass approves the audition.

Documented voice management:

- `POST /v1/get_voice` can list `system`, `voice_cloning`, `voice_generation`, or `all`.
- Returned categories include system voices, quick cloned voices, and voices generated from text prompts.
- Quick-cloned voices and text-designed voices may not appear in queries until they have been successfully used for speech synthesis.
- `POST /v1/delete_voice` deletes only cloned or voice-designed `voice_id` values. Deleted IDs cannot be reused.

Production heuristic:

- Store the chosen `voice_id` with the project artifact ledger, not just in the generation script. Voice IDs are creative assets and audit objects.

## Rapid voice cloning

Use cloning only with explicit permission, rights clearance, and a documented purpose. Voice is a biometric identifier and a performance asset.

Documented workflow:

1. Upload the source audio to `POST /v1/files/upload` with `purpose=voice_clone`.
2. The cloning source must be `mp3`, `m4a`, or `wav`, at least 10 seconds and no more than 5 minutes, and no larger than 20 MB.
3. Call `POST /v1/voice_clone` with the returned `file_id`, a custom `voice_id`, and optional preview text.
4. Custom `voice_id` must be 8–256 characters, start with an English letter, contain only letters, digits, `-`, and `_`, not end in `-` or `_`, and not duplicate an existing ID.
5. If a cloned voice is not used within 7 days, MiniMax documents that the system deletes it.
6. Use `text_validation` to compare the sample transcript with ASR output; if similarity is below `accuracy`, the request is rejected with error `1043`.
7. Optional `need_noise_reduction` and `need_volume_normalization` can clean a clone source, but use better source audio first.
8. Optional `aigc_watermark` appends an AI-generated-content watermark tone to preview audio.

Prompt audio for stability:

- MiniMax also supports uploading a short prompt audio file with `purpose=prompt_audio`.
- Prompt audio must be `mp3`, `m4a`, or `wav`, less than 8 seconds, and up to 20 MB.
- Use it with `clone_prompt.prompt_audio` and `clone_prompt.prompt_text` to improve similarity and stability.

Consent gate:

- Do not clone a celebrity, politician, private individual, employee, customer, or performer unless the project has written consent for this specific use, territory, duration, and distribution channel.
- Do not infer consent from “audio is public.”
- For ads, political content, finance, health, or impersonation-sensitive contexts, require legal review and on-screen/audio disclosure.
- Keep the source clip, consent record, generated `voice_id`, deletion plan, and usage log together.

## Voice design

Use voice design when the user needs a custom voice persona but does not have a legally cleared speaker sample.

Documented workflow:

- `POST /v1/voice_design` accepts a required `prompt` voice description and required `preview_text`.
- `preview_text` has a documented maximum of 500 characters.
- If `voice_id` is omitted, MiniMax returns a generated one.
- The response includes `voice_id` and `trial_audio` as hex-encoded preview audio.
- Pricing docs list Voice Design at `$3 per voice`; the Voice Design API page also notes preview audio character fees. Verify the current bill before bulk casting.

Production heuristic:

- Write voice design prompts like casting notes: age range, accent/language, energy, social role, pacing, vocal texture, emotional baseline, and use case. Avoid protected-class stereotypes and celebrity references.

## Artifact custody

Treat generated audio and voice IDs as production assets.

- Save the request JSON minus secrets, response metadata, `trace_id`, model ID, voice ID, language settings, cost estimate, source script hash, and output file hash.
- Decode hex audio to a local WAV/FLAC/MP3 immediately; do not rely on temporary URLs.
- For async outputs, retrieve files before the documented 9-hour URL expiry.
- For HTTP URL outputs, retrieve within the documented 24-hour URL window.
- Keep each generated take immutable. If you regenerate, create a new take ID rather than overwriting.
- Store final approved stems separately from auditions, rejected takes, and raw clone samples.
- For cloned voices, record whether and when the voice was deleted or intentionally retained.

## Pricing, quota, and throughput

Documented pay-as-you-go prices on 2026-07-10:

- `speech-2.8-turbo`: `$60 / 1M characters`.
- `speech-2.8-hd`: `$100 / 1M characters`.
- Legacy `speech-2.6-turbo` / `speech-02-turbo`: `$60 / 1M characters`.
- Legacy `speech-2.6-hd` / `speech-02-hd`: `$100 / 1M characters`.
- Rapid Voice Cloning: `$1.5 per voice`.
- Voice Design: `$3 per voice`.

Documented rate limits on 2026-07-10:

- T2A for `speech-2.8`, `speech-2.6`, and `speech-02`: `60 RPM` on the general rate-limit page.
- Voice Cloning: `60 RPM`.
- Voice Design: `20 RPM`.
- Audio subscription tiers publish different RPM and voice slot limits; use the account’s actual plan for production scheduling.

Production heuristic:

- Estimate cost from characters before generating. Add a 10–20% retake budget for final narration and a larger audition budget for casting. Character billing rewards script discipline: remove stage directions that are not meant to be spoken.

## Production QA

Review with headphones and a transcript, then in the final video mix.

Minimum QA checklist:

- Text fidelity: no missing words, insertions, malformed acronym reads, or hallucinated punctuation.
- Pronunciation: names, product terms, medical/legal terms, units, currencies, URLs, and code words.
- Language and accent: correct language, dialect, and code-switching behavior.
- Timing: line duration fits edit; pauses feel intentional; no rushed disclaimers.
- Performance: emotion matches scene, not just a label.
- Audio quality: no clipping, pumping, metallic buzz, low-bitrate artifacts, harsh sibilance, or room/effect mismatch.
- Consistency: voice, model, sample rate, loudness, and tone match across scene boundaries.
- Accessibility: captions/subtitles align with the actual spoken output.
- Rights and disclosure: cloned/designed voices have consent, allowed use, and required disclosure.
- Custody: output file, metadata, trace IDs, cost, and approvals are archived.

Recommended measurable checks:

- Loudness: normalize narration stems in post to the target platform spec rather than relying on `vol`.
- Captions: use MiniMax subtitle timestamps as a starting point, then verify against the rendered video.
- Localization: have a fluent reviewer check intelligibility, idiom, cultural tone, and required legal phrasing.
- Interactive voice: measure time-to-first-audio and interruption behavior in the actual application, not only with a single WebSocket sample.

## Example: polished product narration

Production intent: a 30-second SaaS launch voiceover for a web video.

Approach: cast system voices, approve one, render final with `speech-2.8-hd`, keep mono MP3/WAV stem for editing.

Example request:

```json
{
  "model": "speech-2.8-hd",
  "text": "Your support queue should not feel like a guessing game.<#0.35#>\nMeet Northstar Assist: it reads every ticket, finds the real blocker, and drafts the next best reply before your team opens the thread.<#0.5#>\nLess triage. Faster answers. Happier customers.",
  "stream": false,
  "language_boost": "English",
  "voice_setting": {
    "voice_id": "English_Insightful_Speaker",
    "speed": 0.96,
    "vol": 1,
    "pitch": 0,
    "emotion": "calm"
  },
  "pronunciation_dict": {
    "tone": ["Northstar/North star"]
  },
  "audio_setting": {
    "sample_rate": 44100,
    "bitrate": 256000,
    "format": "mp3",
    "channel": 1
  },
  "subtitle_enable": true,
  "subtitle_type": "word",
  "output_format": "hex"
}
```

Expected result: a controlled, premium read with clean word-level subtitle data.

Failure modes:

- “Northstar” reads awkwardly unless the pronunciation rule or script spelling is adjusted.
- `calm` may underplay a launch; test one take with no manual emotion and one with `happy`.
- The pause after the first line may feel too slow once music is added; retime with `<#0.2#>` or edit silence in post.

Variation: use `speech-2.8-turbo` for auditions, then regenerate the approved take in HD.

## Example: approved cloned-voice localization

Production intent: localize an internal training video using an employee’s approved voice.

Approach: collect written consent, upload a clean source sample, clone, activate the voice with a short synthesis, then generate localized scene stems.

Workflow:

1. Confirm consent covers synthetic voice, internal training, target languages, retention period, and deletion policy.
2. Prepare a 60–90 second WAV with one speaker, low noise, no music, and natural pacing.
3. Upload it with `purpose=voice_clone`.
4. Call `voice_clone` with a project-scoped `voice_id`, `text_validation`, `accuracy`, and normalization only if needed.
5. Generate a 10-second audition in the target language with `language_boost` set explicitly.
6. Ask the speaker or project owner to approve the audition before generating all scenes.

Example clone request body:

```json
{
  "file_id": 123456789012345680,
  "voice_id": "AcmeTraining_JRivera_2026Q3",
  "text": "Welcome to the safety briefing. Today we will cover the three checks every operator must complete before starting a shift.",
  "model": "speech-2.8-hd",
  "language_boost": "English",
  "text_validation": "Welcome to the safety briefing. Today we will cover the three checks every operator must complete before starting a shift.",
  "accuracy": 0.75,
  "need_noise_reduction": false,
  "need_volume_normalization": true,
  "aigc_watermark": true
}
```

Expected result: a cloned voice ID and a preview URL if preview text/model are supplied.

Failure modes:

- Clone rejected because ASR validation does not match the sample transcript.
- Voice sounds unstable because the source has music, multiple speakers, or room echo.
- The cloned voice does not appear in `get_voice` until it has been used successfully for synthesis.
- The clone is deleted after 7 days if never used.

Variation: use `clone_prompt` with a sub-8-second prompt audio and transcript when the clone needs more stable similarity.

## Example: low-latency agent response

Production intent: a voice assistant that speaks an answer while generating.

Approach: use WebSocket T2A with `speech-2.8-turbo`, short chunks, and a playback buffer.

Workflow:

1. Open `wss://api.minimax.io/ws/v1/t2a_v2` with Bearer auth.
2. Send `task_start` with model, voice, language, and MP3 audio settings.
3. Wait for `task_started`.
4. Send one concise `task_continue` message per response segment.
5. Play received hex audio chunks in order and append them to the saved take.
6. Send `task_finish` when the response is complete.

Example `task_start`:

```json
{
  "event": "task_start",
  "model": "speech-2.8-turbo",
  "language_boost": "English",
  "voice_setting": {
    "voice_id": "English_radiant_girl",
    "speed": 1.08,
    "vol": 1,
    "pitch": 0,
    "english_normalization": true
  },
  "audio_setting": {
    "sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3",
    "channel": 1
  }
}
```

Example `task_continue`:

```json
{
  "event": "task_continue",
  "text": "I found three matching invoices. The newest one is from June tenth for four hundred eighty dollars."
}
```

Expected result: audio chunks arrive during synthesis, then an `is_final` event marks completion for the segment.

Failure modes:

- Sending text before `task_started`.
- Letting the connection sit idle long enough to close.
- Choosing HD when Turbo would meet the quality bar with lower perceived latency.
- Long, clause-heavy assistant text that sounds unnatural even if latency is acceptable.

Variation: for a non-interactive IVR prompt library, render the same copy over HTTP or async and QA the files offline.

## Sources to verify before production

- MiniMax API documentation index: https://platform.minimax.io/docs/llms.txt
- T2A HTTP API: https://platform.minimax.io/docs/api-reference/speech-t2a-http
- T2A WebSocket API: https://platform.minimax.io/docs/api-reference/speech-t2a-websocket
- Async T2A create/query and guide: https://platform.minimax.io/docs/api-reference/speech-t2a-async-create and https://platform.minimax.io/docs/guides/speech-t2a-async
- Voice cloning upload/clone APIs: https://platform.minimax.io/docs/api-reference/voice-cloning-uploadcloneaudio and https://platform.minimax.io/docs/api-reference/voice-cloning-clone
- Voice design and management APIs: https://platform.minimax.io/docs/api-reference/voice-design-design, https://platform.minimax.io/docs/api-reference/voice-management-get, and https://platform.minimax.io/docs/api-reference/voice-management-delete
- Model overview and release notes: https://platform.minimax.io/docs/guides/models-intro and https://platform.minimax.io/docs/release-notes/models
- Pricing and rate limits: https://platform.minimax.io/docs/guides/pricing-paygo, https://platform.minimax.io/docs/guides/pricing-speech, and https://platform.minimax.io/docs/guides/rate-limits
- Privacy Policy and Terms of Service: https://platform.minimax.io/protocol/privacy-policy and https://platform.minimax.io/protocol/terms-of-service
- Technical background, not an API contract: MiniMax-Speech paper, https://arxiv.org/abs/2505.07916
- Voice rights risk background, not provider policy: PRAC3 paper on synthetic voice risks, https://arxiv.org/abs/2507.16247
