---
name: assemblyai-transcription
description: Use this skill when an agent needs AssemblyAI for speech-to-text or speech-understanding work in media production, including pre-recorded, synchronous short-file, and real-time streaming transcription; speaker diarization or speaker identification; captions and subtitles; timestamps; language detection, code-switching, or transcript translation; audio intelligence such as summaries, chapters, topics, entities, key phrases, sentiment, content moderation, profanity filtering, and PII redaction; webhooks, scaling, rate limits, retention, security, consent, and QA for podcasts, interviews, captions, call recordings, and edit workflows.
---

# AssemblyAI transcription for media-production agents

Use AssemblyAI when the production job needs reliable transcript artifacts from recorded or live speech, especially when the transcript must drive captions, clip selection, speaker turns, show notes, chaptering, translation, moderation, or compliance review.

Treat this as a provider skill, not a generic ASR primer. Check the live AssemblyAI docs before implementing code in production because model names, pricing, add-ons, rate limits, and data-retention settings are volatile. The facts below were verified against official AssemblyAI documentation on 2026-07-10.

## Pick the product surface first

AssemblyAI exposes several surfaces that look similar but serve different production needs.

Documented facts:

- Pre-recorded STT is the main batch/async API for media files. Submit `audio_url` or upload a local file first, then poll `GET /v2/transcript/{id}` or use webhooks until the transcript is `completed` or `error`. The returned transcript includes text, metadata, words with millisecond timestamps, and optional feature outputs. Source: https://www.assemblyai.com/docs/pre-recorded-audio/getting-started/transcribe-an-audio-file
- Sync STT is for short clips in a single HTTP request, with no polling or session management. Official docs describe it as accepting audio clips from 80 ms to 120 s. Use it for short voice-agent turns, quick QC snippets, or small app interactions, not long podcasts or interviews. Sources: https://www.assemblyai.com/docs/sync-stt/getting-started/transcribe-a-short-audio-file and https://www.assemblyai.com/docs/sync-stt/audio-requirements
- Real-time STT streams audio over WebSocket (`wss://streaming.assemblyai.com/v3/ws`) and emits `Begin`, repeated `Turn`, and `Termination` events. Use it for live captioning, voice agents, live meeting assistants, or real-time production monitors. Word timings are in milliseconds. Source: https://www.assemblyai.com/docs/streaming/getting-started/transcribe-streaming-audio
- Streaming is billed for the duration the WebSocket is open, not the amount of audio sent. Unclosed sessions auto-close after 3 hours and can bill for the full session duration. Source: https://www.assemblyai.com/docs/billing-and-pricing
- Use temporary streaming tokens for browser clients; never expose the account API key in client-side code. Source: https://www.assemblyai.com/docs/streaming/getting-started/transcribe-streaming-audio

Production heuristic:

- For a finished media asset, prefer pre-recorded STT even if the recording started as a live session. Async models can use the full file context, which is better for final captions, transcript cleanup, chaptering, and quote extraction.
- For live captions or voice agents, use real-time STT during the event and optionally re-transcribe the final recording asynchronously afterward for the publication-grade transcript.
- Use Sync STT only when the clip is deliberately short and you need immediate response without job lifecycle overhead.

## Model and feature selection

Documented facts verified 2026-07-10:

- Pre-recorded models include Universal-3.5 Pro and Universal-2. AssemblyAI documents Universal-3.5 Pro as the highest-accuracy/fastest pre-recorded model with 18 languages, native code switching, contextual prompting, and up to 1,000 keyterms; Universal-2 supports 99 languages and up to 200 keyterms. Source: https://www.assemblyai.com/docs/getting-started/models
- Streaming models include Universal-3.5 Pro Streaming, Universal-Streaming Multilingual, and Universal-Streaming English. Universal-3.5 Pro Streaming supports 18 languages and up to 100 keyterms; Universal-Streaming Multilingual supports English, Spanish, Portuguese, German, French, and Italian; Universal-Streaming English is English-only. Source: https://www.assemblyai.com/docs/getting-started/models
- Medical Mode is an add-on (`domain: "medical-v1"`) for medical terminology and is billed separately. AssemblyAI documents it for pre-recorded and streaming models in English, Spanish, German, and French. Source: https://www.assemblyai.com/docs/getting-started/models
- Current posted model prices in the docs on 2026-07-10 were: pre-recorded Universal-3.5 Pro at $0.21/hr, Universal-2 at $0.15/hr; streaming Universal-3.5 Pro Streaming at $0.45/hr, Universal-Streaming Multilingual at $0.15/hr, Universal-Streaming English at $0.15/hr. Always re-check pricing before estimating costs. Sources: https://www.assemblyai.com/docs/getting-started/models and https://www.assemblyai.com/pricing

Decision rules:

- Use Universal-3.5 Pro for final English or supported-language interviews, podcasts, social clips, and captions when accuracy and diarization quality matter.
- Use Universal-2 when broad language coverage or lower cost matters more than the newest model.
- Use streaming Universal-3.5 Pro for real-time agent assist, live captions with difficult vocabulary, multilingual code-switching, or speaker-diarized live meetings.
- Use the cheaper streaming models for cost-sensitive live captions where the language set is simple and latency matters more than post-production accuracy.
- Add keyterms or prompting for names, brand vocabulary, show titles, technical terms, product names, spellings, and recurring phrases. Keep keyterms specific; do not stuff generic vocabulary.

## Inputs and artifact custody

Documented facts:

- Local files are uploaded to `/v2/upload`, and the returned `upload_url` is submitted as `audio_url`. For cURL uploads, stream raw bytes with `--data-binary @file`; sending JSON or a path string can create downstream transcoding failures. Source: https://www.assemblyai.com/docs/pre-recorded-audio/getting-started/transcribe-an-audio-file
- `audio_start_from` and `audio_end_at` can constrain a transcript to part of a file in pre-recorded jobs. Source: https://www.assemblyai.com/docs/api-reference/transcripts/submit
- Pre-recorded transcript statuses include `queued`, `processing`, `completed`, and `error`. A queued status can indicate waiting for a processing slot. Source: https://www.assemblyai.com/docs/pre-recorded-audio/check-transcript-status
- Delete transcripts with the transcript delete endpoint; store the `transcript_id` with every production artifact so deletion, audit, support, and retries are possible. Source: https://www.assemblyai.com/docs/api-reference/transcripts/delete

Production heuristic:

- Before upload, normalize production media to an audio-only mezzanine for repeatability: WAV or FLAC for master archival, 16 kHz mono WAV for telephony-like speech, or a high-quality compressed copy when transfer size matters. Preserve the original media separately.
- Keep a job ledger with: source asset path/hash, speaker/channel notes, consent status, request JSON, region endpoint, model, feature flags, transcript ID, submission time, completion time, cost estimate, output file paths, and deletion deadline.
- Do not use ephemeral AssemblyAI URLs as your only source of truth. Download subtitles, redacted audio, transcript JSON, and any derived edit artifacts into your production storage.

## Speaker separation and identity

Documented facts:

- Pre-recorded speaker diarization is enabled with `speaker_labels: true`. Results appear as `utterances`, each with speaker label, text, start/end in milliseconds, confidence, and word-level details. Source: https://www.assemblyai.com/docs/pre-recorded-audio/label-speakers
- Diarization labels are generic sequential labels such as A, B, C. Speaker Identification can map labels to known names or roles through Speech Understanding when you provide known values. Source: https://www.assemblyai.com/docs/pre-recorded-audio/label-speakers
- AssemblyAI documents `speakers_expected`, `speaker_options.min_speakers_expected`, and `speaker_options.max_speakers_expected` as hard boundaries, not soft hints. Over-tight caps merge speakers; overly high caps can over-split. Source: https://www.assemblyai.com/docs/pre-recorded-audio/label-speakers
- AssemblyAI recommends at least 30 seconds of continuous speech per speaker for best diarization results and warns that crosstalk, noise, similar voices, and short backchannels reduce accuracy. Source: https://www.assemblyai.com/docs/pre-recorded-audio/label-speakers
- Streaming supports diarization and multichannel workflows, but these are live session features with real-time constraints, not replacements for final editorial speaker QA. Source: https://www.assemblyai.com/docs/streaming/label-speakers-and-separate-channels
- Multichannel pre-recorded transcription bills each channel separately. Source: https://www.assemblyai.com/docs/billing-and-pricing

Production heuristic:

- For podcast/interview post-production, prefer isolated channels when available. Use multichannel when each speaker is reliably on a separate channel; use diarization when the recording is mono or channels are mixed.
- If exact speaker count is known from production notes, set it; otherwise use a plausible min/max range with slight headroom.
- Always perform human speaker-label QA before publishing captions, pull quotes, clips, or legal/medical notes.

## Captions, subtitles, timestamps, and edit data

Documented facts:

- Pre-recorded transcript responses include word-level start/end timestamps by default in the `words` array; utterances also include start/end when diarization is enabled. Source: https://www.assemblyai.com/docs/pre-recorded-audio/getting-started/transcribe-an-audio-file
- Subtitles are exported from completed transcripts as SRT or VTT through `GET /v2/transcript/{transcript_id}/{subtitle_format}`. Source: https://www.assemblyai.com/docs/api-reference/transcripts/get-subtitles
- Sentence and paragraph endpoints are available for completed transcripts. Source: https://www.assemblyai.com/docs/api-reference/transcripts/get-sentences and https://www.assemblyai.com/docs/api-reference/transcripts/get-paragraphs
- AssemblyAI has guides for custom-length subtitles and speaker-labeled subtitles. Source index: https://www.assemblyai.com/docs/llms.txt
- Sync STT returns word-level details in the `words` array with millisecond `start`/`end` timestamps and per-word confidence in the response for short-file requests. Source: https://www.assemblyai.com/docs/sync-stt/getting-started/transcribe-a-short-audio-file

Production heuristic:

- For broadcast-style captions, treat AssemblyAI’s SRT/VTT as a first timed draft, then enforce platform style: reading speed, line length, sentence segmentation, speaker labels, profanity policy, and house capitalization.
- For social burned-in captions, use word timestamps for karaoke/highlight animation but smooth micro-timing in the compositor. Do not animate every disfluency unless the style intentionally preserves verbatim speech.
- For edit decisions, export a durable transcript JSON plus EDL-like spans: `speaker`, `start_ms`, `end_ms`, `text`, `confidence`, `source_transcript_id`, and reviewer notes.

## Languages, code-switching, and translation

Documented facts:

- Automatic Language Detection identifies the dominant language and routes the request based on detected language and selected `speech_models`; the response includes `language_code` and `speech_model_used`. AssemblyAI recommends at least 15–90 seconds of spoken audio for best results. Source: https://www.assemblyai.com/docs/pre-recorded-audio/language-detection
- Pre-recorded Universal-3.5 Pro supports 18 languages; Universal-2 supports 99 languages. AssemblyAI documents fallback from Universal-3.5 Pro to Universal-2 outside the Universal-3.5 Pro language set. Source: https://www.assemblyai.com/docs/getting-started/models
- Translation is a Speech Understanding feature. It can run as part of the transcription request or as a separate request against an existing transcript and returns `translated_texts` keyed by target language. Source: https://www.assemblyai.com/docs/speech-understanding/translation
- Official docs include real-time translation via LLM Gateway as a streaming workflow, not as a native streaming STT transcript output field. Source: https://www.assemblyai.com/docs/streaming/guides/real_time_translation

Production heuristic:

- For multilingual finished captions, first produce and QA source-language captions, then translate. Do not assume translated subtitles will preserve line breaks, reading speed, or idioms.
- For code-switched speech, request a model that supports the relevant languages and include context/keyterms for names and domain terms. If the file is short or language confidence is low, route to a known language or run a separate detection pass.
- For dubbing/localization, keep source transcript, source captions, translated text, and human localization notes as separate artifacts.

## Speech Understanding and guardrails

Use Speech Understanding and Guardrails when transcript-derived production artifacts need structure, review, or safety processing. Do not confuse these outputs with the base transcript.

Documented facts:

- Summarization generates chapter-like summaries with timestamps and is documented as open beta. It supports `summary_type` values such as `paragraph` and `bullets`, and an `effort` parameter. Source: https://www.assemblyai.com/docs/speech-understanding/summarization
- The old `auto_chapters` transcription parameter is deprecated; AssemblyAI now recommends building chapter summaries by fetching paragraphs and using LLM Gateway for flexible summaries. Source: https://www.assemblyai.com/docs/speech-understanding/auto-chapters
- Entity Detection extracts entities such as people, organizations, addresses, phone numbers, medical data, and social security numbers, with timestamps. Source: https://www.assemblyai.com/docs/speech-understanding/entity-detection
- Sentiment Analysis labels each spoken sentence as positive, neutral, or negative with confidence and timestamps; with speaker labels enabled, sentiment results can include speaker labels. Source: https://www.assemblyai.com/docs/speech-understanding/sentiment-analysis
- Topic Detection and Key Phrases are documented Speech Understanding features. Source: https://www.assemblyai.com/docs/speech-understanding/topic-detection and https://www.assemblyai.com/docs/speech-understanding/key-phrases
- Speaker Identification, Translation, Custom Formatting, and Action Items are documented Speech Understanding features. Source index: https://www.assemblyai.com/docs/llms.txt
- PII Redaction redacts PII in transcript text and can also generate redacted audio. Redacted audio URLs are available only for 24 hours, and redacted audio creation is limited to original files smaller than 1 GB. PII redaction only redacts words in the `text` property; outputs from other features may still contain PII. Source: https://www.assemblyai.com/docs/guardrails/redact-pii-from-transcripts
- Content Moderation and Profanity Filtering are documented Guardrails features. Source: https://www.assemblyai.com/docs/guardrails/detect-sensitive-content and https://www.assemblyai.com/docs/guardrails/filter-profanity-from-transcripts

Production heuristic:

- Use summaries, topics, key phrases, entities, and sentiment as assistive indexes for producers, not as publish-ready editorial truth.
- For clip discovery, combine Speech Understanding signals with transcript search and human review: high sentiment, named entities, and topic shifts can identify candidates, but the editor must check context.
- For PII workflows, redact at the earliest artifact boundary and re-run PII checks after summaries/translations because derived fields can reintroduce sensitive text.

## Webhooks, lifecycle, scale, and retries

Documented facts:

- Pre-recorded jobs accept `webhook_url`, optional webhook auth header name/value, and call back with transcript ID and final status (`completed` or `error`). Source: https://www.assemblyai.com/docs/api-reference/transcripts/submit and https://www.assemblyai.com/docs/pre-recorded-audio/webhooks
- Pre-recorded rate limits are parallel transcription jobs: free accounts start at 5; paid accounts at 200+. Extra jobs queue FIFO. HTTP API requests across endpoints are limited to 20,000 requests per 5 minutes; exceeding that returns HTTP 403. Rate limits are account-level, not project-level. Source: https://www.assemblyai.com/docs/pre-recorded-audio/rate-limits
- Real-time STT paid accounts are constrained by new streaming sessions per minute, not a hard cap on open sessions. Defaults documented on 2026-07-10 were 5 new sessions/min for free accounts and 100+ for paid accounts, with automatic scale-up when usage reaches 70% or more of the current limit. Exceeding the current streaming limit produces a WebSocket closure. Source: https://www.assemblyai.com/docs/streaming/rate-limits
- LLM Gateway and Speech Understanding rate limits are model/service-specific and return `429` when exceeded; response headers can include rate-limit details. Source: https://www.assemblyai.com/docs/llm-gateway/rate-limits
- Failed transcripts are not charged; pre-recorded billing is pro-rated to exact seconds, and add-ons are billed separately. Source: https://www.assemblyai.com/docs/billing-and-pricing

Production heuristic:

- Prefer webhooks over tight polling for batches. Keep a polling fallback with jitter and a widening interval.
- Pilot a representative sample before a large import. Validate transcript quality, feature flags, webhooks, storage, deletion policy, and cost before submitting the full archive.
- For bulk jobs, size submission rate from measured turnaround time and keep in-flight jobs below roughly 80% of the account limit.
- Treat `4xx` as configuration/auth/input errors to inspect, except documented throttling; treat `5xx` as retryable with exponential backoff and a dead-letter queue.

## Security, privacy, consent, and rights

Documented facts:

- AssemblyAI documents data at rest encryption with AES 128 or AES-256 and data in transit with TLS 1.2+. Source: https://www.assemblyai.com/docs/data-retention-and-model-training
- AssemblyAI states it has SOC 2 Type 1 and Type 2 certifications. Source: https://www.assemblyai.com/docs/data-retention-and-model-training
- Paid accounts can use Data Controls to opt out of the model improvement program, set a TTL for audio and transcripts, and review/sign a BAA. Free users cannot access those controls. Source: https://www.assemblyai.com/docs/data-controls
- Opt-out changes are forward-looking. When opted out, AssemblyAI states it will not use Customer Data or Deidentified Data for model improvement/benchmarking. Source: https://www.assemblyai.com/docs/data-controls
- BAA execution automatically opts the account out of model improvement, and AssemblyAI says it does not use files submitted under a BAA for model training. Source: https://www.assemblyai.com/docs/data-controls
- For async production, TTL can be set as low as 1 hour for final transcription artifacts. Without TTL or BAA, default deletion timelines differ by artifact type; final transcription artifacts begin deletion at 30 days, while uploaded audio defaults to deletion beginning at 72 hours. Metadata may be retained for logging and billing. Source: https://www.assemblyai.com/docs/data-retention-and-model-training
- For streaming, AssemblyAI documents zero data retention of audio/transcripts when the account has opted out of model training, with certain metadata stored for logging/billing. Source: https://www.assemblyai.com/docs/data-retention-and-model-training
- AssemblyAI has opted out of data training with all LLM Gateway providers, but this is separate from whether AssemblyAI may train its own models unless the account is opted out or covered by other documented conditions. Source: https://www.assemblyai.com/docs/data-retention-and-model-training

Production requirements:

- Confirm recording consent and rights before transcription. Transcription can create a new sensitive text artifact even if the audio was already authorized for limited use.
- For minors, health data, legal matters, internal meetings, unreleased products, or customer calls, require explicit data controls: paid account, model-improvement opt-out, appropriate TTL, BAA when PHI is involved, and a documented deletion path.
- Do not put API keys in shared media folders, client apps, subtitles, logs, or project files. Use environment variables or a secrets manager.
- If using EU endpoints/data residency, ensure every step uses the correct endpoint, including LLM Gateway or Sync/Streaming variants where applicable.

## Production QA checklist

Run this checklist before shipping captions, clips, edits, or derivative text:

1. Source custody: original media exists, hash/path recorded, consent/rights state recorded.
2. Audio prep: channel layout, sample rate, clipping/noise, crosstalk, and duration checked; problematic files transcoded and rechecked.
3. Request integrity: model, language, keyterms/prompt, diarization/channel mode, PII/redaction, and add-ons match the production intent.
4. Lifecycle: transcript ID stored; status completed; no missing webhook; no orphaned queued jobs; cost and duration recorded.
5. Transcript review: proper nouns, acronyms, product names, numbers, medical/legal terms, and unclear segments reviewed.
6. Speaker review: speaker labels mapped to names/roles only after human confirmation.
7. Caption review: SRT/VTT line breaks, reading speed, timing, profanity policy, and accessibility labels checked.
8. Derived artifact review: summaries, chapters, topics, translations, sentiment, and entities checked against transcript context.
9. Privacy review: PII redaction verified across text, words, utterances, summaries, translations, entities, filenames, logs, and redacted audio.
10. Retention: outputs downloaded into controlled storage; TTL/delete requirements scheduled; transcript deletion tested when required.

## Example: podcast transcript, captions, chapters, and clip index

Example production intent: produce a publication-ready transcript package from a 75-minute two-host podcast with one guest.

Workflow:

1. Extract audio from the edit master; preserve original media and export a speech-focused WAV.
2. Submit a pre-recorded job with Universal-3.5 Pro, language detection if language is uncertain, `speaker_labels: true`, a speaker range such as min 2/max 4 if exact turns are uncertain, and keyterms for show names, hosts, guest, sponsors, and technical vocabulary.
3. Use a webhook for completion and store the transcript ID in the project ledger.
4. Download full JSON, SRT, VTT, paragraphs, and utterances.
5. Generate chapters by grouping paragraphs and using LLM Gateway or the documented summarization feature, then review for editorial accuracy.
6. Build a clip index from high-confidence quote spans, sentiment/topic/key-phrase signals, and producer notes.
7. Human-QA speaker mapping, captions, names, timestamps, and any sponsor/legal language.

Expected result:

- Durable transcript JSON with word timestamps.
- SRT/VTT caption drafts.
- Speaker-labeled utterance list.
- Reviewed chapter list with start/end times.
- Clip candidates with source timecodes and confidence/review status.

Failure modes:

- Guest and host labels swap during crosstalk.
- Sponsor/product names need keyterms or manual correction.
- SRT line breaks are usable but not styled for the target platform.
- Summaries overstate or smooth over uncertainty.

Variations:

- If each speaker has a separate channel, use multichannel instead of diarization, while accounting for per-channel billing.
- If the episode includes sensitive listener calls, enable PII redaction and separately review derived summaries/entities.
- If the podcast is multilingual, explicitly test the model/language path on a sample before batch processing.

## Example: live event captions plus final accessible captions

Example production intent: caption a live webinar and publish corrected captions afterward.

Workflow:

1. During the event, stream microphone or mixer output to Real-time STT with Universal-3.5 Pro Streaming, appropriate `sample_rate`, keyterms for speaker names and product vocabulary, and a termination message on shutdown.
2. Display only finalized turns for public captions unless the UX is designed for interim text.
3. Log session begin/end, session duration, and any WebSocket closures.
4. After the event, transcribe the final recording with pre-recorded STT for publication captions.
5. Export SRT/VTT and run caption QA against the video: timing, reading speed, line length, names, acronyms, and accessibility labels.

Expected result:

- Low-latency live captions during the event.
- Higher-quality final captions from the completed recording.
- Cost record that distinguishes streaming session duration from async audio duration.

Failure modes:

- WebSocket left open after the event, increasing cost.
- Interim captions show unstable text.
- Live transcript misses terms that were not included as keyterms.
- Final async captions differ from live captions; use the final file as canonical.

Variations:

- For browser capture, generate a temporary streaming token server-side.
- For multilingual events, confirm model language support and test code-switching before going live.
- For medical/regulated events, use paid account data controls, BAA as needed, and clear retention settings.

## Example: redacted interview review package

Example production intent: transcribe customer interviews while minimizing exposed PII for editors.

Workflow:

1. Confirm consent and define allowed use of the interview.
2. Enable PII redaction with relevant policies such as person names, phone numbers, email addresses, addresses, or account identifiers.
3. If editors need to hear the audio, enable redacted audio and download it within the 24-hour availability window.
4. Avoid enabling `redact_pii_return_unredacted` unless a restricted reviewer truly needs the original text.
5. Run summaries/entities only after deciding whether downstream derived artifacts may contain PII; review derived fields separately.
6. Store redacted artifacts in the normal edit workspace and unredacted artifacts, if any, in restricted storage with TTL/deletion tracking.

Expected result:

- Redacted transcript text for broad editorial review.
- Optional redacted audio file for clip selection.
- Restricted audit trail with transcript ID, PII policies, and deletion deadline.

Failure modes:

- PII remains in entity/summarization/translation outputs even though the main `text` field is redacted.
- Redacted audio link expires before the team downloads it.
- Over-redaction makes quotes unusable; solve with restricted unredacted review, not by exposing everything.

Variations:

- For public testimonials, run a human legal/privacy pass after automated redaction.
- For internal analysis, keep only aggregate notes and delete source transcripts after the approved retention window.

## Source map

Official sources verified on 2026-07-10:

- Documentation index and API map: https://www.assemblyai.com/docs/llms.txt
- Models and pricing: https://www.assemblyai.com/docs/getting-started/models and https://www.assemblyai.com/pricing
- Billing: https://www.assemblyai.com/docs/billing-and-pricing
- Pre-recorded quickstart/API: https://www.assemblyai.com/docs/pre-recorded-audio/getting-started/transcribe-an-audio-file and https://www.assemblyai.com/docs/api-reference/transcripts/submit
- Streaming quickstart/rate limits: https://www.assemblyai.com/docs/streaming/getting-started/transcribe-streaming-audio and https://www.assemblyai.com/docs/streaming/rate-limits
- Sync STT: https://www.assemblyai.com/docs/sync-stt/getting-started/transcribe-a-short-audio-file
- Diarization: https://www.assemblyai.com/docs/pre-recorded-audio/label-speakers
- Subtitles: https://www.assemblyai.com/docs/api-reference/transcripts/get-subtitles
- Language detection/translation: https://www.assemblyai.com/docs/pre-recorded-audio/language-detection and https://www.assemblyai.com/docs/speech-understanding/translation
- Speech Understanding: https://www.assemblyai.com/docs/speech-understanding/summarization, https://www.assemblyai.com/docs/speech-understanding/auto-chapters, https://www.assemblyai.com/docs/speech-understanding/entity-detection, https://www.assemblyai.com/docs/speech-understanding/sentiment-analysis
- Guardrails: https://www.assemblyai.com/docs/guardrails/redact-pii-from-transcripts, https://www.assemblyai.com/docs/guardrails/detect-sensitive-content, https://www.assemblyai.com/docs/guardrails/filter-profanity-from-transcripts
- Rate limits and scale: https://www.assemblyai.com/docs/pre-recorded-audio/rate-limits and https://www.assemblyai.com/docs/llm-gateway/rate-limits
- Data controls/security/retention: https://www.assemblyai.com/docs/data-controls and https://www.assemblyai.com/docs/data-retention-and-model-training
