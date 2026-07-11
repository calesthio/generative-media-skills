---
name: elevenlabs-dubbing-voice-conversion
description: Use for ElevenLabs provider-specific dubbing, localization, voice changer, speech-to-speech, and voice isolation/enhancement workflows. Applies when an agent must prepare source media, choose ElevenLabs dubbing versus voice conversion, manage language/speaker/timing decisions, handle voice identity and consent, call or plan against documented ElevenLabs APIs, export dubs/transcripts, estimate cost/limits, or quality-control localized speech while avoiding generic text-to-speech guidance.
---

# ElevenLabs dubbing and voice conversion

Use this skill when the task is about transforming existing speech: translating a source audio/video into another language, converting a performed voice into a selected voice, cleaning speech before conversion, or planning localization deliverables around ElevenLabs. Do not use it for ordinary text-to-speech generation unless the TTS output is only one supporting step in a dubbing or voice-conversion workflow.

This skill is evidence-aware. Treat dated vendor facts below as documented facts verified on 2026-07-10. Treat operational observations and production heuristics as guidance to test on the current project, not as provider guarantees.

## Choose the ElevenLabs path

Use the decision before touching files:

- Dubbing/localization: choose ElevenLabs Dubbing when the source is an audio or video asset that must be translated into another language while preserving speaker timing, delivery, and identity as much as the product supports. Plan for transcript review, language QA, and media export.
- Voice changer / speech-to-speech: choose the Voice Changer API when the language/content is already correct and the job is to transform an existing performance into another available or cloned voice while retaining emotion, rhythm, timing, and delivery.
- Voice isolation: choose Audio Isolation before dubbing or voice conversion when noise, music, ambience, reverb-like background, or production sound makes speech recognition/conversion unreliable. Do not use it blindly on clean audio; extra processing can remove wanted texture or introduce artifacts.
- External localization: if exact legal/medical/brand translation, rigorous subtitle timing, or lip-sync under broadcast constraints matters, plan a human translation/review layer around ElevenLabs rather than presenting an automatic dub as final.
- Generic TTS: use a different ElevenLabs TTS skill for scripted voiceover from text. This skill only covers TTS-adjacent decisions where existing speech, speakers, timing, localization, or conversion are central.

## Documented facts verified 2026-07-10

ElevenLabs publishes an existing Dubbing API at `POST /v1/dubbing` that accepts multipart source media or a `source_url`, `target_lang`, optional `source_lang`, optional `num_speakers`, time range, watermark and background-audio controls, and automatic/manual mode. The response includes `dubbing_id` and `expected_duration_sec`. `GET /v1/dubbing/{dubbing_id}` returns status, source language, target languages, created time, editability, media metadata, and failure error text. `GET /v1/dubbing/{dubbing_id}/audio/{language_code}` streams the dubbed MP3/MP4 result for the original automatic dub; if a dub was edited in Dubbing Studio, use the resource render workflow rather than the original automatic-audio endpoint. Transcript export is available at `/v1/dubbing/{dubbing_id}/transcripts/{language_code}/format/{format_type}` with `srt`, `webvtt`, or `json`, and `source` may be used for the original media language. Sources: https://elevenlabs.io/docs/api-reference/dubbing/create, https://elevenlabs.io/docs/api-reference/dubbing/get, https://elevenlabs.io/docs/api-reference/dubbing/audio/get, https://elevenlabs.io/docs/api-reference/dubbing/transcripts/get.

ElevenLabs’ Dubbing capability page says Dubbing v2 Alpha is the default in Automatic Dubbing, supports 90+ languages, preserves each speaker’s tone/pace/style, separates overlapping speakers into tracks, recommends up to 9 unique speakers per file for best quality, and allows up to 5 concurrent dubbing jobs on self-serve plans and 100 by default on Enterprise. The same page says realtime/live dubbing is not currently available and that the Dubbing v2 API is not yet live; therefore, do not promise v2 API behavior unless the current docs have changed. Source: https://elevenlabs.io/docs/overview/capabilities/dubbing.

The Voice Changer API is `POST /v1/speech-to-speech/{voice_id}`. It transforms an input audio file into the selected voice while preserving emotion, timing, and delivery. Documented controls include `output_format`, `model_id`, `voice_settings` as a JSON string, optional `seed` with best-effort non-guaranteed determinism, `remove_background_noise`, `file_format`, and `enable_logging=false` for eligible enterprise zero-retention requests. The model must support speech-to-speech; ElevenLabs’ model-choice guide identifies `eleven_multilingual_sts_v2` as the Voice Changer model. Sources: https://elevenlabs.io/docs/api-reference/speech-to-speech/convert and https://elevenlabs.io/docs/eleven-api/choosing-the-right-model.

Audio Isolation is `POST /v1/audio-isolation`, accepts multipart `audio`, and removes background noise from audio. For `file_format=pcm_s16le_16`, input must be 16-bit PCM, 16 kHz, mono, little-endian; this has lower latency than encoded waveform input. Source: https://elevenlabs.io/docs/api-reference/audio-isolation/convert.

Pricing is volatile. On 2026-07-10, the ElevenAPI pricing page listed Voice Changer and Voice Isolator at $0.12 per minute and Dubbing at $0.33/minute automatic with watermark, $0.50/minute automatic without watermark, or $0.50/minute Dubbing Studio, with dubbing metered per source audio minute and taxes excluded. Re-check immediately before quoting budgets. Source: https://elevenlabs.io/pricing/api.

Privacy and retention are product-specific. On 2026-07-10, ElevenLabs documented Zero Retention Mode as available to select Enterprise customers. API zero retention via `enable_logging=false` covered Voice Changer, Speech to Text, Text to Speech, and Text to Dialogue, but the same table marked Dubbing input/output and voice-cloning audio samples as not eligible for Zero Retention. Source: https://elevenlabs.io/docs/eleven-api/resources/zero-retention-mode.

Voice cloning has consent boundaries. ElevenLabs documents verification for Instant and Professional Voice Cloning as an ethical/legal safeguard, but also says verification cannot prove a recording truly belongs to the requester and places responsibility for authorized use on the creator. Speaker separation for cloning works best with clearly distinct voices and substantial continuous target-speaker speech, and becomes unreliable with frequent overlap, similar voices, or fragmented target turns. Source: https://elevenlabs.io/docs/eleven-api/concepts/voice-cloning.

## Operational observations to verify on each project

Automatic dubbing can preserve surprising performance detail, but it is still a localization system, not a final human dub stage. Expect the highest risk in names, product terms, idioms, numbers, jokes, cross-talk, singing, whispered dialogue, heavy room noise, and languages whose natural translated phrase length differs greatly from the source.

Speech-to-speech conversion is performance-led. The source audio drives pacing and emotion more than a text prompt would. A weak read, clipped plosives, noisy room, or bad microphone will often survive the conversion in some form.

Voice isolation is a rescue and preparation tool, not a mastering chain. It can help speech recognition and conversion, but it can also thin voices, dull consonants, or remove ambience that the client wanted to preserve.

Speaker counting is a production decision. Auto-detection is convenient; explicit `num_speakers` can reduce speaker swaps when the cast is known, but a wrong value can be worse than auto.

The fastest high-quality workflow is usually not “run dub and ship.” It is: prepare source, run a short pilot clip, inspect transcript and speaker mapping, adjust language/voice/timing choices, then run the full asset and export review materials.

## Source-media preparation

Create a source inventory before calling ElevenLabs:

- Rights: confirm you can transform the source media, clone/preserve voices, translate the script, and distribute the result in every target territory.
- Consent: identify any real person whose voice is cloned, preserved, or converted. Obtain written permission for the exact use, languages, duration, territory, and disclosure requirements.
- Format: keep a high-quality master. Export a clean working file with stable sample rate, no clipping, and a clear spoken track. For video, preserve a separate picture reference and a separate original mix when possible.
- Timing: note target platform constraints, maximum duration, required exact runtime, and whether the dub must fit existing cuts, subtitles, lip movements, ad slots, or broadcast clocks.
- Speakers: list speakers, names, roles, approximate timestamps, accent/dialect, and whether each speaker should preserve identity, use a similar library voice, or be replaced with an approved voice.
- Language: specify source language if known instead of relying on auto when the source includes code-switching, short clips, proper nouns, or multiple languages. Use ISO-639 language codes where the API requires them.
- Background audio: decide whether the final dub should keep the original music/ambience or drop it. Use `drop_background_audio=true` only when background content should not remain, such as clean speeches or monologues.
- Terminology: prepare product names, speaker names, brand terms, prohibited translations, required formality level, and local-market substitutions.
- Pilot span: for long or high-stakes material, choose a 30-120 second section with each major speaker, noise condition, and emotional mode.

Pre-clean only when needed. If the source has obvious background noise, run or request Audio Isolation on a copy, then compare the isolated result to the original before sending the full asset to Dubbing or Voice Changer. If the original has music/SFX that should remain in the final mix, preserve a separate music/effects stem or source master.

## Dubbing workflow

For a production dub, follow this sequence:

1. Define deliverables: target languages, file outputs, subtitle outputs, whether a video file or audio-only dub is needed, and whether Dubbing Studio editability is required.
2. Audit safety and rights: do not proceed with unauthorized impersonation, undisclosed real-person voice cloning, political deception, fraud, harassment, or rights-unclear content.
3. Prepare source: trim dead air only if it is not part of the edit; avoid lossy re-encodes; keep timecode notes.
4. Run a pilot when quality risk is non-trivial. Use `start_time` and `end_time` if supported by the chosen API/product path.
5. Create the job. For API jobs, preserve `dubbing_id`, request parameters, source checksum or media URL, expected duration, and target language.
6. Poll status with `GET /v1/dubbing/{dubbing_id}`. Handle `queued`, `preparing`, `dubbing`, `dubbed`, and `failed` style states; avoid starting more concurrent jobs than the plan allows.
7. Export review materials: dubbed audio/video plus source and target transcripts/subtitles. Use transcript exports for subtitle QA and terminology review.
8. Review language and timing. Check whether speakers are preserved correctly, whether translation fits the shot, whether emotional delivery survived, and whether background audio is acceptable.
9. Repair or rerun. For simple automatic API jobs, rerun with corrected parameters or prepared source. For edited Dubbing Studio/resource workflows, use the render path for edited results rather than the original automatic-audio endpoint.
10. Deliver with disclosure and metadata: include language code, source version, ElevenLabs job ID, model/product path if known, date, human review status, and any consent/rights notes required by the client.

### Parameter decisions for `POST /v1/dubbing`

- `file` vs `source_url`: upload when you need reproducibility, private media, or exact source control; `source_url` is convenient for public or signed URLs, but record access expiry.
- `source_lang`: use `auto` for well-spoken single-language content; specify the source code for short, noisy, accented, or code-switched content.
- `target_lang`: required; choose the intended locale/dialect deliberately. If a dialect matters and the product path supports `target_accent`, test it on a pilot because the parameter is documented as experimental.
- `num_speakers`: `0` auto-detects. Set a known count when speaker separation is unstable and the cast is clear.
- `watermark`: confirm client requirements and current plan behavior. The Dubbing v2 capability page says v2 does not expose a watermark toggle and that free-tier dubs are watermarked automatically.
- `highest_resolution`: use for video deliverables when picture quality matters; avoid unnecessary high-res processing for audio-only review.
- `disable_voice_cloning`: use when preserving/cloning the source voice is not allowed or desired. The API docs say this uses a similar Voice Library voice and can fail if workspace voice slots or permissions are insufficient.
- `mode=manual`: only use with an intentionally prepared CSV transcript workflow. The docs call manual mode experimental and discourage production use.

## Voice Changer / speech-to-speech workflow

Use Voice Changer for same-language or already-translated performances where the timing and emotional delivery are acceptable and the desired output is “this performance in that approved voice.”

1. Confirm the target `voice_id` is authorized for the requested use. For cloned voices, keep consent and verification records.
2. Prepare the input performance. Use the cleanest possible take, with stable levels and no clipping. Split very long performances into semantically complete segments if review or retry granularity matters.
3. Select a speech-to-speech capable model. As of 2026-07-10, ElevenLabs recommends `eleven_multilingual_sts_v2` for Voice Changer.
4. Decide output format from downstream use: MP3 for quick review/social drafts; WAV/PCM only if the plan supports it and post-production needs it.
5. Use `remove_background_noise=true` only when the input needs cleanup. If preservation of breath, room tone, or performance grit matters, compare both versions.
6. If Enterprise zero retention is required and available, set `enable_logging=false`; note that history and stitching features are unavailable in that mode.
7. Review against source for timing, intelligibility, emotional match, artifacts, and identity/consent compliance.

Voice settings are not a replacement for a good source performance. Start from the approved voice’s stored settings, then override only when the output is too flat, unstable, exaggerated, or unlike the target voice. Use a seed for reproducibility attempts, but do not promise exact deterministic repeats.

## Voice isolation workflow

Use Audio Isolation as a preprocessing or repair pass:

- Pre-dubbing: clean dialogue before transcription/speaker separation when noise or music is confusing the system.
- Pre-voice-conversion: remove background noise so the conversion model follows the voice performance rather than the room.
- Post-production rescue: isolate a speech stem for review or manual remixing.

Do not use it as a blanket step on every asset. For clean studio recordings, isolation may reduce quality. For music-under-dialogue, it may also remove production value that the final mix needs. Always archive the original, isolated stem, and comparison notes.

## Timing, lip-sync, and translation fit

ElevenLabs dubbing is timing-aware, but it is not a guarantee of perfect visual lip-sync or broadcast-grade ADR. For video:

- Keep the original edit locked before dubbing. Re-cutting after dubbing invalidates timing QA.
- For talking-head or close-up material, review mouth-open/close alignment, pauses, laugh timing, and interruptions.
- For voiceover, prioritize natural translation and pacing over strict syllable fit.
- For ads, trailers, and legal disclaimers, check total runtime and required wording exactly.
- For subtitles, export SRT/WebVTT and check line length, reading speed, segmentation, punctuation, speaker labels, and terminology.

Production heuristic: if the target language expands significantly, choose between natural speech with slightly altered pacing, condensed translation, edited picture timing, or human ADR. Do not silently choose one; make it a production decision.

## Speaker identity, cloning, and consent

Never frame “voice preservation” as permission. Before preserving, cloning, or converting a real voice:

- Confirm the speaker, rights holder, and client authorize the exact use.
- Confirm whether the authorization covers language translation, commercial distribution, synthetic voice creation, edits, and reuse in future projects.
- Avoid cloning public figures, employees, customers, minors, or private individuals without explicit authorization and legal review where appropriate.
- Prefer `disable_voice_cloning=true` or approved library/brand voices when consent is absent or ambiguous.
- Require disclosure when the audience, platform, law, or client policy expects synthetic or translated audio labeling.
- Keep a production record: who approved, for what asset, what languages, what voice IDs, what dates, and any restrictions.

If a user asks to imitate a real person without permission, refuse that part and offer safer alternatives: a consented voice, a library voice with a similar broad style, subtitles only, or human-recorded localization.

## Quality-control checklist

Run QC on every target language:

- Rights and disclosure: consent recorded; synthetic/dubbed labeling plan clear; target territory cleared.
- Source integrity: correct source version; no accidental rough cut; time range correct.
- Speaker mapping: each speaker remains distinct; no identity swaps; overlapping speech handled acceptably.
- Translation: meaning, tone, formality, idioms, names, numbers, units, URLs, product terms, and legal lines are correct.
- Performance: emotion, pace, pauses, laughs, whispers, urgency, and emphasis match the scene.
- Intelligibility: no muffling, sibilance, clipping, robotic artifacts, dropped words, or hallucinated speech.
- Timing: no obvious late/early lines; runtime fits; video mouth movement acceptable for the deliverable tier.
- Background: original music/SFX retained or dropped intentionally; no pumping, ghost voices, phasey isolation artifacts, or doubled speech.
- Subtitles/transcripts: exported format correct; source transcript available when needed; target captions match dubbed audio.
- Packaging: output format, sample rate/bitrate, filename, language code, and metadata match the delivery spec.

For high-stakes releases, require bilingual human review. Automatic transcript export is a QA aid, not proof of translation quality.

## Failure modes and repairs

- Wrong source language: rerun with explicit `source_lang`; trim lead-in music/silence; provide a cleaner source.
- Speaker swaps: rerun with explicit `num_speakers`; split scenes by speaker; reduce overlap if possible; use Dubbing Studio/resource edits if available.
- Translation is literal or off-brand: prepare glossary and approved translations; use human translation review; rerun or manually edit target segments where the product path supports it.
- Dub sounds unnatural in target language: lower voice-cloning/preservation intensity where the UI supports it; use similar library voices; accept less voice similarity for more natural localization.
- Background audio competes with speech: test `drop_background_audio`; create separate M&E/music stems; mix externally.
- Voice Changer keeps noise/artifacts: run Audio Isolation first, re-record source performance, or split and retry only damaged sections.
- Output endpoint returns original automatic dub after edits: use the resource render workflow for Dubbing Studio/resource edits; do not use the automatic-audio endpoint for edited deliverables.
- Too many jobs: respect concurrency limits, queue jobs, and retry after current jobs complete rather than hammering the API.
- Privacy requirement conflicts with product: if the project requires zero retention for Dubbing or voice cloning samples, escalate. As of 2026-07-10, ElevenLabs did not mark those as zero-retention eligible.

## Complete examples

### Example: Spanish localization pilot for a two-speaker product demo

Intent: localize a 6-minute English product demo to Spanish for web release while preserving two founders’ speaking styles.

Inputs and constraints:

- Source: `demo_master_v12.mp4`, English, two known speakers, light music bed, no subtitles.
- Target: Spanish (`es`), MP4 review file plus SRT.
- Consent: both founders approved Spanish synthetic dubbing for the campaign.
- Risk: product names and pricing must be exact.

Workflow:

1. Create a glossary with product names, plan names, prices, and phrases not to translate.
2. Run a 60-second pilot covering both speakers with `source_lang=en`, `target_lang=es`, `num_speakers=2`, `start_time` and `end_time` around the representative span, `drop_background_audio=false`.
3. Poll with `GET /v1/dubbing/{dubbing_id}` until status is `dubbed` or failed.
4. Export dubbed media and SRT/WebVTT transcript.
5. Ask a Spanish reviewer to check product terms, tone, and speaker mapping.
6. If pilot passes, run full file with the same language/speaker/background choices.

Expected result: a Spanish dub that follows the original edit, keeps distinct founder voices, retains the music bed, and produces review captions.

Likely failure modes: product names translated incorrectly, one founder assigned the other’s voice, Spanish line length rushing the close-up shots, or music masking speech.

Variations: set `disable_voice_cloning=true` if founder voice preservation is not permitted; set `drop_background_audio=true` if the original bed causes separation artifacts and an external music stem will be mixed later.

### Example: Authorized voice conversion for a finished character performance

Intent: convert an actor’s approved English monster performance into an approved creature voice while preserving growls, timing, and emotional delivery.

Inputs and constraints:

- Source: `monster_take_03.wav`, clean mono performance, no music.
- Target voice: approved internal voice ID.
- Language: no translation.
- Deliverable: WAV/PCM for post if plan permits; otherwise high-bitrate MP3 review plus later approved export.

Workflow:

1. Confirm actor and target voice usage rights.
2. Send the source to `POST /v1/speech-to-speech/{voice_id}` with `model_id=eleven_multilingual_sts_v2`.
3. Keep `remove_background_noise=false` because the source is clean and contains intentional breath/growl texture.
4. Use a seed only to help reproduce review attempts; record that determinism is not guaranteed.
5. Review against the original for timing, emotion, consonant clarity, and whether creature traits overpower intelligibility.

Expected result: the same performance rhythm and emotional arc in the target voice.

Likely failure modes: roars become distorted, whispers lose intelligibility, or the converted voice sounds too human/too synthetic.

Variations: split roars and spoken lines into separate files for different settings; run a cleanup pass only if the source contains room noise.

### Example: Noisy interview rescue before dubbing

Intent: prepare a noisy street interview for French dubbing.

Inputs and constraints:

- Source: `street_interview.mov`, two speakers plus traffic.
- Target: French (`fr`) for internal review.
- Risk: traffic confuses transcription and speaker separation.

Workflow:

1. Extract a short representative audio segment and run Audio Isolation on the copy.
2. Compare original and isolated speech for word clarity, artifacts, and loss of ambience.
3. If isolation improves clarity, use the isolated dialogue track for dubbing review while preserving the original master for final mix reference.
4. Run dubbing with `source_lang=en`, `target_lang=fr`, and `num_speakers=2` or auto if speaker count is uncertain.
5. Export transcript/captions and verify names, street references, and speaker mapping.

Expected result: clearer speech recognition and fewer speaker/transcription errors.

Likely failure modes: isolation makes voices watery, traffic remains under speech, or ambience loss makes the final feel disconnected from picture.

Variations: keep the original ambience under the final dub in external mixing; use subtitles only if the source is too chaotic for reliable dubbing.

## Source and evidence notes

Primary sources used for this skill were ElevenLabs API reference pages, capability pages, model-selection docs, pricing, zero-retention documentation, and voice-cloning concept documentation, all checked on 2026-07-10. Re-check official docs before relying on volatile facts: model IDs, pricing, Dubbing v2 API availability, concurrency, language support, export formats, retention eligibility, and plan-gated output formats.
