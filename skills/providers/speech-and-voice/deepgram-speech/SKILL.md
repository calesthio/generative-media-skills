---
name: deepgram-speech
description: "Use for Deepgram speech and voice production workflows: speech-to-text transcription, live captions, diarization, audio intelligence, Aura text-to-speech, Flux and Voice Agent live audio, model selection, cost/limits/privacy checks, artifact custody, and production QA."
---

# Deepgram speech production

Use this skill when Deepgram is a candidate provider for transcription, captioning, speech analytics, voice-agent audio, or text-to-speech assets. Treat Deepgram as a production speech platform, not as a generic "make audio" button: choose the endpoint, model, features, and custody plan from the deliverable's latency, accuracy, language, privacy, and artifact requirements.

Facts in this skill were checked against official Deepgram documentation and pricing on 2026-07-10. Verify volatile items again before spend or launch: public model IDs, language support, add-on prices, concurrency, regional availability, and early-access controls.

Primary official evidence used:

- API overview: https://developers.deepgram.com/reference/deepgram-api-overview
- STT getting started: https://developers.deepgram.com/docs/stt/getting-started
- Pre-recorded STT API: https://developers.deepgram.com/reference/speech-to-text/listen-pre-recorded
- Streaming STT API: https://developers.deepgram.com/reference/speech-to-text/listen-streaming
- Models and languages: https://developers.deepgram.com/docs/models-languages-overview
- Flux docs: https://developers.deepgram.com/docs/flux/agent and https://developers.deepgram.com/reference/speech-to-text/listen-flux
- Diarization: https://developers.deepgram.com/docs/diarization
- Captions guide: https://developers.deepgram.com/docs/automatically-generating-webvtt-and-srt-captions
- Audio Intelligence overview: https://developers.deepgram.com/docs/audio-intelligence
- STT Intelligence feature matrix: https://developers.deepgram.com/docs/stt-intelligence-feature-overview
- Aura TTS models: https://developers.deepgram.com/docs/tts-models
- TTS REST and streaming: https://developers.deepgram.com/docs/text-to-speech and https://developers.deepgram.com/docs/streaming-text-to-speech
- TTS latency and controls: https://developers.deepgram.com/docs/text-to-speech-latency and https://developers.deepgram.com/docs/tts-voice-controls
- Voice Agent configuration/API: https://developers.deepgram.com/docs/configure-voice-agent and https://developers.deepgram.com/reference/voice-agent/voice-agent
- Rate limits: https://developers.deepgram.com/reference/api-rate-limits
- Pricing: https://deepgram.com/pricing
- Security/privacy/compliance: https://deepgram.com/data-security, https://developers.deepgram.com/trust-security/data-privacy-compliance, https://developers.deepgram.com/docs/the-deepgram-model-improvement-partnership-program

## Documented capability map

### Speech-to-text

Deepgram exposes three STT paths:

1. Pre-recorded audio through REST `POST /v1/listen`. Use for podcast/video transcription, post-production captions, batch media archives, call recordings, editorial analysis, and any job where complete-file turnaround matters more than sub-second partials. It accepts local binary audio or a hosted URL, supports callbacks, and returns the only transcript response Deepgram will provide unless you save it.
2. Live streaming through WebSocket `wss://api.deepgram.com/v1/listen`. Use for live captions, meeting/event transcription, live production logging, and agent-assist transcripts. It can emit interim and final results, speech events, endpointing, utterance events, and word timings.
3. Turn-based conversational STT through Flux (`/v2/listen` in current docs). Use for live voice agents and interruption-sensitive conversations where end-of-turn behavior matters. Flux is not the normal choice for offline transcription.

Current model guidance from Deepgram docs, verified 2026-07-10:

- `nova-3` / Nova-3: highest-performing general-purpose ASR without model-native turn detection. Use for pre-recorded media, live captions, meetings, multilingual/noisy/far-field content, and most transcription deliverables.
- `flux-*`: conversational speech recognition for agents. Use when detecting when a user is done speaking is part of the product behavior.
- `nova-2`: keep as fallback for languages/features not yet supported by Nova-3, and for filler-word needs where Deepgram documents that support.
- Whisper Cloud: pre-recorded only; Deepgram documents extra concurrency and long-audio processing limits. Do not choose it for live streams.

### Transcript formatting and enrichment

Deepgram can return word-level timestamps and confidence scores. Production-useful STT options include punctuation, smart formatting, paragraphs, utterances, numerals, profanity filtering, redaction, search/replace, keywords/keyterms, diarization, multichannel, language selection, language detection, and code-switching.

Important boundaries:

- `smart_format=true` is the usual readability switch; Deepgram documents that it includes punctuation and paragraph behavior at minimum for supported languages, with broader English formatting for dates, times, currencies, phone numbers, emails, and URLs.
- `diarize=true` is documented but the streaming API reference marks it deprecated in favor of `diarize_model`; use `diarize_model=latest` or a pinned documented version when available. Streaming does not support diarization `v2` in the current reference.
- Speaker labels are numeric diarization clusters, not verified human identities.
- Use multichannel when each speaker/source is isolated to a channel. Use diarization when speakers are mixed into one channel. If both are possible, prefer clean channel separation for production calls and panels.
- Language detection identifies/transcribes the dominant language and returns a language code/confidence for supported languages; current language-detection docs explicitly say it is not supported for streaming and recommend multilingual models for real-time multilingual audio.
- `language=multi` and Flux multilingual handle code-switching transcription, not translation. Do not promise translated subtitles from Deepgram STT unless current official docs explicitly expose translation for the requested workflow; otherwise use a separate translation step after transcription.

### Captions and subtitles

Deepgram is useful for producing timed subtitle files because the response includes word timings and Deepgram provides SRT/WebVTT examples. It does not replace video editorial QA:

- Generate SRT/VTT from words or utterances.
- Normalize line breaks, reading speed, and caption duration for the platform.
- Check proper names, numbers, speaker changes, profanity policy, and accessibility labels.
- Burn captions into video with a separate compositor or video tool if needed.

### Audio Intelligence

Official STT/audio intelligence features include summarization, topic detection, intent recognition, sentiment analysis, and entity detection. Current Deepgram docs contain per-feature language/streaming limits and at least one visible inconsistency between the feature matrix and an individual feature page, so verify the exact feature page immediately before promising language or streaming support.

Safe production interpretation, verified 2026-07-10:

- Sentiment, summarization, and topic detection are documented for pre-recorded audio and English in the feature matrix.
- Entity detection is documented for pre-recorded audio and some streaming use; streaming finalization may wait for an entity to complete unless low-latency `no_delay` behavior is chosen, which can miss entities.
- Intents/topics are generated from context and can accept custom hints in official docs; treat them as analysis labels, not deterministic taxonomy classification.
- Intelligence add-ons may lower effective concurrency. If multiple services are used in one request, Deepgram rate-limit docs say the lower service limit applies.

### Text-to-speech

Deepgram Aura provides TTS through REST `POST /v1/speak` and WebSocket `wss://api.deepgram.com/v1/speak`.

Documented TTS facts, verified 2026-07-10:

- Aura voices use model IDs like `aura-2-thalia-en`.
- Official Aura language support includes English, Spanish, German, French, Dutch, Italian, and Japanese, with accents/variants listed in the voice model docs.
- REST is a good fit for narration files, rendered voice lines, reviewable takes, and stable media assets.
- TTS WebSocket is a good fit for LLM-token streaming, IVR, voice agents, and immediate playback.
- Deepgram documents a 2000-character input limit for TTS requests and gives latency guidance: a baseline around 600 ms without streaming plus approximately 40 ms per 100 characters in their example model. For long narration, chunk near the limit for throughput, but split at sentence/beat boundaries for performance and editability.
- Aura-2 controls include speed and pronunciation controls for English and Spanish in REST and WebSocket; speed is documented as range `0.7`-`1.5`, with some early-access caveats in Voice Agent settings.
- Deepgram Aura TTS is stock voice generation. Do not imply custom voice cloning or likeness replication unless an official contract/product path is confirmed separately.

### Voice Agent API and live audio

Use Deepgram Voice Agent when the deliverable is an interactive agent, not just a transcript or narration file. Voice Agent combines audio input, STT, LLM routing, TTS, tool/function messages, conversation text, and audio output over a WebSocket. Send a Settings message immediately after connection to configure input/output audio, listen/think/speak providers, prompt, turn-taking, and tools.

Use separate STT + LLM + TTS components instead of Voice Agent when the production needs:

- deterministic offline assets;
- a post-produced soundtrack;
- independent provider evaluation;
- transcript-only or captions-only output;
- non-real-time editorial review before speech is played.

## Empirical and operational observations

These are operational patterns, not provider guarantees:

- Deepgram's live experience is usually best when audio is sent as small, steady, correctly declared chunks. The most common "bad transcript" cause in streaming integrations is wrong `encoding`, `sample_rate`, channel count, or container/raw mismatch.
- Low-latency settings can reduce editorial quality. Interim transcripts, aggressive endpointing, `no_delay`, and small TTS chunks are useful for responsiveness but increase revision, false finalization, entity misses, and unnatural speech cadence.
- Diarization quality is sensitive to overlap, crosstalk, music beds, room echo, and short speaker turns. Clean channel routing beats post-hoc diarization whenever production can control capture.
- For media production, raw Deepgram JSON is more valuable than just a plain transcript because it preserves word timings, confidence, speaker/channel labels, request ID, warnings, and add-on outputs.
- TTS narration often needs text written for speech, not prose copied from a script. Punctuation, sentence length, pronunciation hints, and spelling of acronyms materially affect Aura output.

## Production heuristics

Apply these unless user constraints require otherwise:

- Choose Nova-3 for finished transcription and captions; choose Flux for interactive agent turn-taking.
- Choose pre-recorded REST for file-based media; choose WebSocket only when the user needs live output.
- Keep a full JSON response artifact even if the deliverable is SRT, VTT, TXT, CSV, or EDL.
- Run a short representative sample before transcribing a long project when names, jargon, accents, music, or privacy-sensitive content matter.
- Treat every add-on as a tradeoff: it may improve usefulness but can add cost, lower concurrency, increase latency, or add failure/warning modes.
- For live captions, optimize for stability first: correct audio format, moderate endpointing, final results for display, and visible correction behavior if interim results are shown.
- For TTS, generate several short auditions before committing a long voice. Freeze voice ID, speed, text normalization rules, sample rate/container, and pronunciation overrides before batch synthesis.

## Workflow recipes

### Pre-recorded transcription and captions

1. Confirm consent and rights to process the audio.
2. Inspect media: duration, channels, sample rate, language(s), speakers, music/noise, target platform.
3. Choose model and features:
   - `model=nova-3` for most production audio.
   - `smart_format=true` for readable transcript.
   - `utterances=true` and/or `paragraphs=true` for reviewable chunks.
   - `diarize_model=latest` or current documented diarization parameter when speakers are mixed.
   - `multichannel=true` when channels isolate speakers.
   - `redact=...` for PII if needed.
4. Use callback for long jobs or server workflows; Deepgram documents asynchronous processing and retries for callback delivery.
5. Save raw response, plain transcript, SRT/VTT, warnings, request parameters, model, region, request ID, and checksums for source media.
6. QA against the audio. Correct names, numbers, timestamps, diarization, and caption line breaks.

### Live captions

1. Confirm live audio capture format before opening the socket. Pass `encoding`, `sample_rate`, and `channels` accurately for raw audio.
2. Use Nova-3 live streaming unless agent-style turn detection is required.
3. Enable `interim_results=true` only if the UI is designed to revise text; otherwise display final segments.
4. Tune `endpointing`, `utterance_end_ms`, and speech events for caption cadence.
5. Keep a rolling transcript buffer and persist final messages. Network interruptions are expected; implement reconnect behavior and mark gaps.
6. Do not rely on live diarization to identify people by name; map speakers after review or from channel/source metadata.

### Voice agent

1. Decide whether Voice Agent is warranted. If the task is "make a narrated video," use TTS. If the task is "build an interactive phone/web agent," Voice Agent may fit.
2. Configure Settings immediately after WebSocket connection.
3. Set listen/think/speak providers intentionally. Deepgram docs show Deepgram TTS as default and support managed/BYO LLM/TTS providers; record which provider produced each output.
4. Test interruption, barge-in, silence, endpointing, tool calls, errors/warnings, and fallback behavior before production.
5. Store conversation text and event logs according to consent and privacy rules; do not store sensitive raw audio unless required and authorized.

### TTS narration

1. Rewrite text for speech: short sentences, pronounceable acronyms, explicit pauses, and production-safe punctuation.
2. Pick an Aura voice ID from current docs, e.g. `aura-2-thalia-en`, and audition it.
3. Keep each request under the documented input limit. For long narration, chunk at sentence/paragraph boundaries and store each take as a separate artifact.
4. Use pronunciation controls for brand names, medical terms, or proper nouns when available for the language.
5. Export in the requested container/sample rate/encoding. Loudness-normalize and mix outside Deepgram.

## Cost, quotas, and rate-limit handling

Deepgram pricing and quotas are volatile. Verify the pricing page and rate-limit docs on the day of the run.

As of 2026-07-10, the public pricing page listed a $200 free credit and example pay-as-you-go STT rates such as Flux English, Flux Multilingual, Nova-3 Monolingual, and Nova-3 Multilingual with separate Growth rates. It also listed add-on pricing for features such as redaction and keyterm prompting. Do not hardcode these values in a client quote without rechecking.

As of 2026-07-10, official rate-limit docs listed different concurrency ceilings by plan, region, product, and feature. Examples included:

- STT REST pre-recorded commonly capped around 50 concurrent requests in public tables.
- STT streaming limits vary by model/plan/region and can be higher than REST.
- Diarization and Audio Intelligence have their own lower limits.
- TTS REST and TTS streaming have separate concurrent-request limits.
- Voice Agent has concurrent connection limits by plan/region.

If a request combines services, plan for the lowest applicable limit. In production, implement queueing, retries with backoff, circuit breakers, and per-project usage tags.

## Privacy, security, consent, and rights

Documented facts:

- Deepgram publishes security/privacy material and says it has SOC 2 Type 1 and Type 2 certification; compliance docs are available through account channels.
- Deepgram offers regional endpoints including North America, Europe, and Australia in rate-limit docs.
- Deepgram's Model Improvement Partnership Program documentation describes data handling and opt-out/retention choices; API references include `mip_opt_out`.
- Deepgram docs warn that it does not store transcripts for retrieval after the response, so your system must save required outputs.

Production rules:

- Obtain appropriate consent before recording, transcribing, analyzing, or synthesizing voice content. Voice can be biometric/personal data depending on jurisdiction.
- Do not promise zero data retention unless the user's Deepgram contract and account configuration explicitly provide it. For strict retention, regulated PHI, or air-gapped requirements, investigate Enterprise/self-hosted options and legal agreements before processing.
- Use redaction for transcripts that may contain SSNs, credit cards, phone numbers, addresses, health details, or other PII, but still QA redaction; it is not a compliance guarantee.
- Avoid sending unnecessary raw audio to any third party. Trim irrelevant sections, avoid background private conversations, and minimize stored artifacts.
- Generated voices must not impersonate real people. Label synthetic speech when the context requires disclosure, and keep proof of rights for scripts, source audio, and distribution.

## Artifact custody checklist

For every production job, write a small run record outside the final media asset:

- source media path/URL, hash, duration, channel count, language hypothesis;
- consent/rights notes and retention classification;
- Deepgram endpoint, region, model, feature parameters, SDK/API version if known;
- request ID, created timestamp, warnings, errors, and billing tags;
- raw JSON response;
- derived transcript formats: TXT, JSONL/CSV segments, SRT/VTT, speaker map, analysis outputs;
- QA notes and manual corrections;
- final delivery paths and whether source/raw artifacts should be deleted, retained, or escrowed.

## Complete examples

### Example: podcast episode transcript plus subtitles

Production intent: create an editable transcript, SRT, and topic summary for a 48-minute two-host podcast with occasional guest overlap.

Workflow and parameters:

```text
Endpoint: POST https://api.deepgram.com/v1/listen
Input: hosted WAV/MP3 URL or local audio upload
Query:
  model=nova-3
  smart_format=true
  utterances=true
  paragraphs=true
  diarize_model=latest
  summarize=v2
  topics=true
  tag=podcast-s01e04
```

Expected result: Deepgram returns a JSON transcript with words, timings, speaker labels, utterance/paragraph structure, summary/topics when supported, request metadata, and warnings if a feature/language combination is unsupported. Generate SRT from word or utterance timings, then manually correct names and speaker labels.

Why structured this way: Nova-3 fits finished transcript accuracy; smart formatting improves readability; utterances/paragraphs help editorial review; diarization is needed because speakers overlap in one mix; tags help usage tracking.

Failure modes:

- speaker labels swap during overlap;
- summary/topics omitted or warned because language/feature support changed;
- callback payload too large for the receiving server;
- transcript contains correct words but poor punctuation around crosstalk.

Variations:

- Use `multichannel=true` instead of diarization when host/guest tracks are isolated.
- Add redaction for sensitive listener calls.
- Remove intelligence features for non-English episodes and summarize after transcription with a separate approved model.

### Example: live conference captions

Production intent: display real-time captions on a conference stream and archive final transcript.

Workflow and parameters:

```text
Endpoint: wss://api.deepgram.com/v1/listen
Model: nova-3
Audio: linear16, 16000 Hz, mono, small steady chunks
Query:
  model=nova-3
  language=en-US
  encoding=linear16
  sample_rate=16000
  channels=1
  smart_format=true
  interim_results=true
  endpointing=300
  utterance_end_ms=1000
  vad_events=true
```

Expected result: interim hypotheses update during speech; final segments are persisted to the transcript and displayed with less churn. Caption UI visibly revises interim text and locks final text.

Why structured this way: live captions need responsiveness, but the archive needs final messages. Declaring raw audio format avoids decoding errors.

Failure modes:

- wrong sample rate or encoding causes unusable transcripts or WebSocket data errors;
- aggressive endpointing cuts sentences too early;
- music/applause lowers accuracy;
- network disruption creates gaps.

Variations:

- Disable interim display for broadcast overlays that should not visibly revise.
- Use `language=multi&model=nova-3` or Flux multilingual when code-switching is expected, after checking current supported languages.
- Use source channel metadata rather than diarization when each panelist has an isolated mic channel.

### Example: support voice agent prototype

Production intent: build a real-time customer support agent that handles interruptions and speaks back.

Workflow and parameters:

```text
Endpoint: Deepgram Voice Agent WebSocket
First message: Settings
Listen: Flux or current Deepgram conversational STT model
Think: configured LLM provider and system prompt
Speak: Deepgram Aura-2 voice, e.g. aura-2-thalia-en
Tools: order lookup, escalation, support article retrieval
Audio: telephony/browser format declared explicitly
```

Expected result: the agent emits conversation text, thinking/speaking state messages, function-call requests, warnings/errors, and binary audio output. It should detect end-of-turn and permit interruption according to configuration.

Why structured this way: Flux/Voice Agent is for turn-taking, not offline transcription. Settings-first configuration prevents ambiguous defaults.

Failure modes:

- agent talks over the caller because endpointing/eager end-of-turn is too aggressive;
- tool call schema fails and the agent loops;
- output voice has wrong pronunciation for product names;
- conversation logs store sensitive data longer than allowed.

Variations:

- Use Deepgram STT + your own LLM + Aura TTS instead of Voice Agent if you need full orchestration control.
- Use a managed/BYO LLM provider only after verifying current Voice Agent provider support and contract terms.

### Example: product-video narration with Aura

Production intent: generate clean English narration for a 90-second product video.

Workflow and parameters:

```text
Endpoint: POST https://api.deepgram.com/v1/speak
Model: aura-2-thalia-en
Container/encoding/sample rate: choose for the editor delivery spec
Request text: one paragraph or scene beat at a time, under 2000 characters
Optional controls: speed=0.95; pronunciation overrides for product names if supported
```

Expected result: separate audio files per scene/paragraph that can be reviewed, replaced, loudness-normalized, and mixed with music/SFX.

Why structured this way: scene-sized chunks are easier to retake and align. The 2000-character limit prevents request failure, while punctuation and beat-based text improve performance.

Failure modes:

- copied marketing copy sounds breathless or unnatural;
- product acronym is pronounced as a word;
- chunk boundary creates audible cadence mismatch;
- wrong container/sample rate creates editor import friction.

Variations:

- Use WebSocket TTS when streaming LLM output to a live user.
- Use a different Aura language/voice after auditioning against the brand tone.
- Postprocess loudness and noise floor outside Deepgram.
