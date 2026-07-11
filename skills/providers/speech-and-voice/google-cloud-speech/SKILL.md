---
name: google-cloud-speech
description: Use this skill when a media-production agent needs Google Cloud speech and voice services for transcription, captions/subtitles, long-form audio analysis, live caption planning, Text-to-Speech narration, Chirp 3 / Gemini-TTS voice selection, consented custom voice workflows, dubbing/localization planning, pricing/quotas/region checks, or speech-related safety and data-governance decisions.
---

# Google Cloud Speech for media production

Use Google Cloud Speech as a provider option when the job is fundamentally about speech audio:

- Transcribe existing audio/video into scripts, searchable text, edits, subtitles, captions, or speaker notes.
- Generate SRT/WebVTT captions from long media.
- Plan live captions or real-time transcript features.
- Create synthetic narration, dialogue prototypes, educational voiceovers, IVR-style prompts, or localized voice tracks.
- Use Google voice families such as Chirp 3 HD, Gemini-TTS, Studio, Neural2, WaveNet, or Standard when the production brief values Google Cloud governance, scale, regional controls, or existing GCP infrastructure.
- Create a consented custom voice only when official access, voice-owner consent, and rights review are present.

Do not use this skill as a generic audio-editing, music, denoise, DAW, mixing, or video-localization skill. Google Cloud Speech can produce transcripts and voice assets, but production finishing still needs editing, loudness normalization, sync, QC, and often translation tools outside the Speech APIs.

Volatile facts below were verified against official Google Cloud documentation on 2026-07-10. Re-check model IDs, launch stages, regional endpoints, quotas, and prices before committing spend or compliance claims.

## API boundary

Google exposes related but separate services:

- Cloud Speech-to-Text (STT): recognition/transcription from audio to text. For new media workflows, prefer API V2 unless an existing integration requires V1. V2 adds recognizer resources, regionalized service patterns, customer-managed encryption key support for resources and batch transcription, and audio auto-detect.
- Cloud Text-to-Speech (TTS): speech synthesis from plain text, SSML, markup, or model-specific prompted text into playable audio.
- Gemini-TTS appears in current Cloud Text-to-Speech documentation as a newer TTS family with text-prompted style control; some routes may involve Vertex AI permissions or endpoints. Verify the exact API route in the current docs before implementation.
- Instant Custom Voice is a Cloud TTS feature for creating a voice cloning key from consent and reference audio, but access is restricted to allow-listed users.

If the production requires both transcription and synthetic voice, treat them as one provider package for planning but as separate API integrations for implementation, quota, pricing, IAM, and data-governance review.

## Documented facts to preserve

### Speech-to-Text

- Chirp 3 Transcription is a Speech-to-Text API V2 model with model identifier `chirp_3`. Google documents it for `StreamingRecognize`, `Recognize`, and `BatchRecognize`.
- Google describes `StreamingRecognize` as suitable for streaming/real-time audio, `Recognize` for audio shorter than one minute, and `BatchRecognize` for long audio. Google’s Chirp 3 page states BatchRecognize is generally for 1 minute to 1 hour, but up to 20 minutes when word-level timestamps are enabled.
- As of the 2026-07-10 verification, Google documents Chirp 3 regional availability in `us` and `eu` multi-regions, with latest support discoverable through the Locations API.
- Caption outputs are V2-only and use `BatchRecognize`; SRT and WebVTT outputs can be returned inline or written to Cloud Storage, and Cloud Storage output can request multiple formats at once.
- V2 streaming recognition is gRPC-only. Google’s guide notes a 25 KB limit on audio sent in each request message of a stream.
- Google’s troubleshooting page documents a five-minute streaming recognition limit; near the limit, close and open a new stream.
- STT V2 quota examples verified on 2026-07-10 include 100 resource requests/minute/region, 150 operation requests/minute/region, 300 synchronous recognition requests/minute/region, 150 batch recognition requests/minute/region, and 300 concurrent `StreamingRecognize` sessions/region. Streaming request quota details can change and must be checked before a large live event.
- STT pricing is based on successfully processed audio duration. The pricing page verified on 2026-07-10 lists V2 standard recognition tiering beginning at $0.016/minute for 0 to 500,000 minutes and dynamic batch recognition at $0.003/minute. Empty responses can still count as processed if the API processed the audio.
- By default, Google says Cloud STT does not log customer audio data or transcripts. Data logging is opt-in and discounted pricing may depend on it. Do not opt in for sensitive or unreleased production audio without explicit client approval.

### Text-to-Speech

- Cloud TTS synchronous `text:synthesize` returns audio only after all input text is processed. The request requires `input`, `voice`, and `audioConfig`; successful responses contain base64 audio content.
- Cloud TTS long-form audio synthesis is asynchronous, writes to a Cloud Storage URI, and Google’s docs state it can synthesize up to 1 million bytes of input. The long-audio page was marked Preview at verification time.
- Bidirectional streaming synthesis is documented as Preview and is intended to reduce latency by sending text and receiving audio simultaneously.
- Cloud TTS supports audio settings such as encoding, speaking rate, pitch, volume gain, sample rate, and effects profiles, but support varies by voice family. The REST AudioConfig reference gives speaking rate range [0.25, 2.0], pitch range [-20.0, 20.0] semitones, and volume gain range [-96.0, 16.0] dB.
- SSML can control pauses, acronyms, dates, numbers, substitutions, and other speech details for supported voices, but not every voice family supports every SSML tag.
- The supported voices page verified on 2026-07-10 says Chirp 3 HD voices are designed for intonation-rich speech across many languages and support advanced audio controls and low-latency text streaming. That same page notes Chirp 3 HD is available in `global`, `eu`, and `us` endpoints but is out of scope for regionalization and data residency. Re-check because release notes show endpoint and language expansion over time.
- Chirp 3 HD voice control docs describe pace control, pause tags, and custom pronunciation controls. Some controls are Preview or Experimental; do not present them as stable unless current docs say so.
- Chirp 3 Instant Custom Voice is allow-list restricted. Official docs require recording a consent statement and reference audio, each as single-channel audio up to 10 seconds, and creating a voice cloning key. The documented consent statement is: "I am the owner of this voice, and I consent to Google using this voice to create a synthetic voice model."
- TTS pricing verified on 2026-07-10 listed Chirp 3 HD at $30 per 1M characters after 1M free characters, Instant Custom Voice at $60 per 1M characters with no free usage, Studio at $160 per 1M after 1M free, Neural2/Polyglot at $16 per 1M after 1M free, and Standard/WaveNet at $4 per 1M after 4M free. Gemini-TTS pricing is token-based; the page listed audio tokens at 25 tokens/second. Always re-check pricing.

## Empirical/operational observations to label as such

These are production observations, not guaranteed provider facts:

- Caption quality is more often limited by source audio, overlapping speech, music beds, and terminology than by API choice. A clean mono dialogue stem usually beats a full mix for transcription.
- Speaker diarization helps editorial workflows, but it is not a cast list. Human review is still required before attributing quotes.
- Automatic captions often need manual line breaking, reading-speed control, profanity/brand handling, and timing nudges before publishing.
- Synthetic narration that sounds natural in a standalone preview can feel wrong against picture after music, cuts, and captions are added. Review in the final mix, not only as isolated WAV/MP3.
- For localized dubbing, script adaptation and timing are usually bigger constraints than raw TTS quality. Translate for mouth/time fit and cultural intent, not literal text alone.

When you use these observations in a plan, label them as operational observations or production heuristics.

## Provider-selection decisions

### Choose Google STT when

- The project already uses Google Cloud storage, IAM, billing, or compliance controls.
- You need V2 BatchRecognize with SRT/WebVTT outputs for long-form captions.
- You need a currently documented Chirp transcription model and can run in its supported regions.
- You need structured batch processing, region-aware recognizers, Cloud Storage outputs, or Google Cloud auditability.
- You are processing high volume and can benefit from batch pricing, quota planning, and pipeline automation.

### Consider another STT provider when

- You need an offline/local transcript path.
- Your desired region, language, diarization behavior, timestamp mode, or latency requirement is not supported by the selected Google model.
- The client will not permit uploading audio to Google Cloud.
- You need an end-to-end dubbing platform rather than raw transcripts/captions.

### Choose Google TTS when

- You need Google Cloud governance, billing, IAM, or integration with existing GCP pipelines.
- Chirp 3 HD, Gemini-TTS, Studio, Neural2, WaveNet, or Standard voices match the creative direction and language.
- You need long-form synthesis to Cloud Storage or low-latency streaming with a supported model.
- You need consented custom voice and the client has official allow-list access plus written voice-owner authorization.

### Consider another TTS provider when

- You need a non-Google voice style, a particular celebrity/brand likeness, advanced director controls not supported by current Google docs, or guaranteed stable non-preview controls.
- You need voice cloning without Google allow-list access.
- You need a fully managed dubbing package with translation, timing, lip-sync, mix, and human review bundled.

## STT production workflow

1. Inspect the media.
   - Extract or identify the best dialogue track.
   - Use lossless or lightly compressed source where possible.
   - Verify sample rate, channel count, encoding, and duration with a tool such as `ffprobe`.
   - If separate speaker channels exist, preserve them; otherwise accept mixed-channel limits.

2. Select method.
   - Use `Recognize` only for short clips under the documented synchronous boundary.
   - Use `BatchRecognize` for long files, Cloud Storage inputs/outputs, captions, and scalable media libraries.
   - Use `StreamingRecognize` only for live or interactive workflows, and design stream rollover before the documented maximum duration.

3. Select model and region.
   - Prefer `chirp_3` when its language, method, feature, and region support match the job.
   - Use the Locations API or current docs to verify locale/model/feature support at runtime.
   - Lock the region deliberately; do not mix regions casually if the client has data-residency constraints.

4. Configure recognition.
   - Set language codes accurately. For auto language detection, provide a constrained list rather than every possible language.
   - Enable word time offsets only when needed for captions, karaoke timing, transcript search, or quote-level edits; note that it can change supported duration for some models.
   - Enable diarization only when speaker separation matters, and warn that speaker labels need review.
   - Use phrase hints/custom classes for brand names, product names, people, technical terms, acronyms, and unusual spellings.

5. Request outputs.
   - For captions, request SRT or WebVTT via V2 BatchRecognize `output_format_config`.
   - For editorial, keep native JSON as well as captions so downstream tools can use confidence, timestamps, and alternatives.
   - Store raw transcript, reviewed transcript, captions, and QC notes as separate artifacts.

6. Review.
   - Listen-check low-confidence or high-value segments.
   - Validate names, numbers, calls to action, legal claims, quotes, and any on-screen captions.
   - Check subtitle reading speed, line length, scene-cut collisions, and speaker changes.
   - If the transcript is empty or poor, verify audio metadata and intelligibility before blaming the model.

## TTS production workflow

1. Decide the voice role.
   - Narrator, instructor, character, customer support, ad read, accessibility description, temporary scratch VO, or localized replacement track.
   - State whether the output is final voice, prototype, temp VO for edit timing, or accessibility aid.

2. Select voice family.
   - Chirp 3 HD: use for modern natural narration or low-latency voice where the language/style is supported. Verify controls and endpoint limitations.
   - Gemini-TTS: consider when the current docs support the needed style prompting, multi-speaker dialogue, and output constraints. Verify model ID, region, launch stage, token pricing, permissions, and API route.
   - Studio: consider for news/broadcast-style reads if the language/voice and cost fit.
   - Neural2/WaveNet/Standard: consider for cost-sensitive, established, or compatibility-oriented uses.
   - Instant Custom Voice: use only after allow-list, consent, rights, and safety review.

3. Prepare script for speech, not print.
   - Rewrite dense prose into spoken sentences.
   - Spell out ambiguous numbers, currencies, URLs, acronyms, product names, and pronunciation traps.
   - Put breaths and thought breaks into punctuation, SSML, or model-specific pause controls only where supported.
   - For dubbing/localization, adapt text to duration and culture before synthesis.

4. Generate in sections.
   - Split by scene, paragraph, or beat so the editor can replace and retime individual lines.
   - Name files with sequence numbers, language, voice, model, and revision.
   - Keep a manifest of text, voice, model, region, audio config, date, and output path.

5. Review before final mix.
   - Check pronunciation, pacing, emotional fit, breath/pauses, clipped starts/ends, artifacts, and consistency across sections.
   - Test against picture with captions and music.
   - Regenerate only the failed segments; do not change voice/model mid-project without a logged decision.

## Dubbing and localization planning

Google Cloud Speech can support pieces of a dubbing workflow, but it is not automatically a full dubbing pipeline.

Plan these stages explicitly:

1. Source transcription with timestamps and speaker notes.
2. Human or machine translation plus cultural adaptation.
3. Duration-constrained script rewrite.
4. Voice selection or consented custom voice.
5. TTS generation by scene/line.
6. Edit, sync, room tone, EQ, loudness, subtitles, and final QC.

For lip-sync or avatar work, check the avatar/lip-sync provider separately. A Google TTS file is only the voice asset; it does not guarantee mouth-match, performance acting, or mix readiness.

## Safety, consent, rights, and data governance

- Get explicit permission to upload production audio to Google Cloud, especially unreleased content, interviews, minors, medical/legal content, internal meetings, or celebrity/performer material.
- Treat transcripts as sensitive derived data. They can expose private speech even when the original audio is access controlled.
- Do not enable STT data logging for client media unless the client approves the discount/privacy tradeoff in writing.
- For custom voice, require written confirmation that the speaker owns or controls the voice rights and consents to synthetic voice creation. The official Instant Custom Voice workflow requires a recorded consent statement.
- Never clone a voice from scraped, archival, deceased-person, employee, actor, customer, or public-figure audio without a specific rights and policy review.
- Mark synthetic narration as synthetic when the distribution context, platform policy, law, or client policy requires it.
- For localization, confirm rights to create derivative translated/dubbed versions of the source content.
- For regulated content, verify region, retention, encryption, IAM, logging, and deletion requirements before processing.

## Example: long podcast transcript and captions

Production intent: turn a 48-minute interview into reviewed transcript, quote pulls, SRT captions, and WebVTT captions.

Provider/method: Cloud Speech-to-Text V2 `BatchRecognize`, model `chirp_3` if current locale/feature support allows it.

Inputs:

- `gs://show-assets/raw/interview_ep12_dialogue.wav`
- English audio, two speakers, mostly clean dialogue, light intro music.
- Need JSON transcript, SRT, and VTT.

Workflow:

1. Inspect the file: duration, encoding, channels, sample rate, audible speech quality.
2. If music intro/outro confuses captions, trim or provide a dialogue stem for recognition.
3. Use V2 BatchRecognize with output to a Cloud Storage bucket and request native JSON plus SRT and VTT.
4. Enable word time offsets if quote-level editing requires them, but verify duration/model boundaries first.
5. Add phrase hints for guest names, sponsor names, product names, and recurring acronyms.
6. Poll the async operation.
7. Review transcript and captions manually before publishing.

Expected result:

- Native JSON for editing/search.
- `.srt` and `.vtt` files with time-aligned caption text.
- A QC list of uncertain names, overlapping speech, music-covered lines, and jokes/idioms requiring human review.

Likely failure modes:

- Empty or poor transcript from wrong audio metadata, wrong language, bad source audio, or music-heavy sections.
- Speaker labels treated as identities instead of diarization placeholders.
- Caption lines too long or poorly broken for platform standards.
- Cost incurred even for empty responses if the API successfully processed the audio.

Variations:

- For a 3-minute social clip, use BatchRecognize if captions are needed as files; use synchronous Recognize only if the clip is under the documented short-audio limit and captions are not required.
- For multilingual audio, constrain possible language codes and verify automatic language detection support for the selected model.

## Example: live event captions

Production intent: provide real-time rough captions for a livestream, with edited captions produced afterward.

Provider/method: Cloud Speech-to-Text V2 `StreamingRecognize` for live display; V2 `BatchRecognize` afterward from the recorded master for final captions.

Workflow:

1. Use a clean speech feed, not the broadcast mix if possible.
2. Open a gRPC streaming recognition session.
3. Keep each stream message within documented request-size limits.
4. Roll over streams before the documented maximum stream duration.
5. Display interim captions as provisional.
6. After the event, run BatchRecognize on the recording and produce reviewed SRT/VTT.

Expected result:

- Live captions with low latency but occasional recognition errors.
- Higher-quality final captions after batch transcription and human review.

Failure modes:

- Stream aborts near the duration limit if rollover is not implemented.
- Quota exhaustion for concurrent sessions during multi-room events.
- Bad captions from noisy room mics, crosstalk, or music beds.

Variation:

- For compliance-grade captions, use live captions only as an accessibility aid and schedule a human correction pass before archival publication.

## Example: narration with Chirp 3 HD

Production intent: generate warm, polished English narration for a 90-second product explainer.

Provider/model: Cloud Text-to-Speech, Chirp 3 HD voice selected from the current supported voices list.

Script excerpt:

```text
Most teams don't need more dashboards. They need one clear next step.

[pause short]

Open the workspace, choose the customer journey, and Montage builds the first cut: scenes, voice, captions, and review notes in one place.
```

Parameters:

- Voice: verify current `en-US` Chirp 3 HD voices; choose based on audition, not gender labels alone.
- Audio encoding: `LINEAR16` for editing or `MP3` for quick preview.
- Speaking rate: start at 1.0; adjust only if the chosen voice supports the control and the read misses timing.
- Segmenting: one file per scene or paragraph.

Expected result:

- Natural narration assets suitable for edit assembly.
- A manifest tying each audio file to text, voice, model, settings, region/endpoint, and generation date.

Failure modes:

- Pause tags ignored or overused.
- Brand/product terms mispronounced.
- Voice sounds natural alone but too slow or too upbeat against picture.
- Selected endpoint does not satisfy a data-residency requirement.

Variations:

- Use SSML for supported voices when you need standards-based pronunciation/pause markup.
- Consider Gemini-TTS instead when the current docs support the desired natural-language style direction and the project accepts its pricing/launch-stage constraints.

## Example: consented custom voice for localization

Production intent: create a synthetic voice track for an executive's approved internal training series in Spanish and French.

Provider/feature: Chirp 3 Instant Custom Voice, only if the organization is allow-listed.

Preconditions:

- Written permission from the executive and legal/communications approval.
- Official consent statement recorded as required by Google.
- Reference audio recorded cleanly, single-channel, up to 10 seconds, in the same environment as consent audio.
- Confirmation that the target language transfer is supported by current docs.

Workflow:

1. Store consent and reference audio in the approved Cloud Storage location.
2. Generate the voice cloning key using the official API workflow.
3. Keep the key access-restricted and auditable.
4. Adapt translated scripts to duration and tone.
5. Synthesize line-by-line or scene-by-scene.
6. Have the voice owner or designated reviewer approve the final audio.

Expected result:

- A controlled synthetic voice asset for approved internal use, not a general-purpose impersonation permission.

Critical failures:

- Using archival or public audio without direct consent.
- Treating allow-list access as legal approval.
- Publishing the synthetic voice in external advertising when consent was internal-only.
- Failing to disclose or govern synthetic identity use where required.

## Quality review checklist

For STT:

- Correct language/model/region/method.
- Source audio intelligible and metadata valid.
- Important names, numbers, quotes, and claims human-reviewed.
- Timestamps usable for the intended edit/caption task.
- Captions meet platform line length, reading speed, punctuation, and speaker-change conventions.
- Data logging, region, retention, and IAM choices match client requirements.

For TTS:

- Voice family and exact voice match the creative role.
- Launch stage, region, endpoint, quota, and price verified.
- Script is written for speech.
- Pronunciation traps are handled.
- Audio is generated in editable sections.
- Final review is against picture and mix, not isolated audio only.
- Synthetic/custom voice rights and disclosure requirements are satisfied.

## Source anchors verified 2026-07-10

- Cloud Speech-to-Text Chirp 3 Transcription: https://docs.cloud.google.com/speech-to-text/docs/models/chirp-3
- Cloud Speech-to-Text V2 captions: https://docs.cloud.google.com/speech-to-text/docs/caption-support
- Cloud Speech-to-Text streaming guide: https://docs.cloud.google.com/speech-to-text/docs/streaming-recognize
- Cloud Speech-to-Text troubleshooting: https://docs.cloud.google.com/speech-to-text/docs/troubleshooting
- Cloud Speech-to-Text quotas: https://docs.cloud.google.com/speech-to-text/docs/quotas
- Cloud Speech-to-Text pricing: https://cloud.google.com/speech-to-text/pricing
- Cloud Speech-to-Text data logging: https://docs.cloud.google.com/speech-to-text/docs/v1/data-logging
- Cloud Speech-to-Text migration/V2: https://docs.cloud.google.com/speech-to-text/docs/migration
- Cloud Speech-to-Text best practices: https://docs.cloud.google.com/speech-to-text/docs/best-practices
- Cloud Text-to-Speech basics: https://docs.cloud.google.com/text-to-speech/docs/basics
- Cloud Text-to-Speech supported voices and languages: https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types
- Cloud Text-to-Speech Chirp 3 HD: https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd
- Cloud Text-to-Speech Gemini-TTS: https://docs.cloud.google.com/text-to-speech/docs/gemini-tts
- Cloud Text-to-Speech Instant Custom Voice: https://docs.cloud.google.com/text-to-speech/docs/chirp3-instant-custom-voice
- Cloud Text-to-Speech long-form synthesis: https://docs.cloud.google.com/text-to-speech/docs/create-audio-text-long-audio-synthesis
- Cloud Text-to-Speech streaming synthesis: https://docs.cloud.google.com/text-to-speech/docs/create-audio-text-streaming
- Cloud Text-to-Speech pricing: https://cloud.google.com/text-to-speech/pricing
- Cloud Text-to-Speech quotas: https://docs.cloud.google.com/text-to-speech/quotas
