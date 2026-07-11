# Evaluation spec for deepgram-speech

This file is an answer key and scoring guide. Do not expose it to evaluated agents. Evaluate agents using only SKILL.md plus the user task, then score with this file.

## Minimum competency expectations

A passing agent must:

- distinguish Nova-3, Flux, pre-recorded REST, live streaming WebSocket, TTS, and Voice Agent use cases;
- avoid inventing unsupported Deepgram translation or voice-cloning capabilities;
- handle diarization, multichannel, captions, language detection, and audio intelligence with correct caveats;
- include privacy/consent/artifact-custody practices for voice data;
- verify volatile pricing, model, rate-limit, and language facts instead of hardcoding them blindly;
- produce production-ready workflows with parameters, expected artifacts, QA, and failure modes.

## Knowledge questions

### 1. When should an agent choose Nova-3 versus Flux?

Expected answer: Nova-3 is the general-purpose ASR choice for pre-recorded transcription, captions, meetings, noisy/multilingual/far-field audio, and streaming transcripts where turn-taking is not the core product behavior. Flux is for interactive voice agents/turn-based conversational STT where end-of-turn and interruption behavior matter. Flux is not the normal offline batch transcription model.

Required points:

- States Nova-3 for batch/streaming transcription and captions.
- States Flux for conversational/agent turn detection.
- Mentions latency/turn-taking as the differentiator, not generic accuracy alone.
- Does not claim Flux replaces Nova-3 for all transcription.

Critical failures:

- Recommends Flux for a finished podcast transcript without rationale.
- Says Nova-3 has model-native turn detection like Flux.

### 2. Does Deepgram STT translate audio?

Expected answer: The skill should not promise translation from Deepgram STT. Deepgram supports language selection/detection and multilingual code-switching transcription in documented workflows, but those are transcription features, not translation. Use a separate translation step unless current official docs explicitly expose translation for the exact workflow.

Required points:

- Distinguishes transcription, language detection, code-switching, and translation.
- Advises separate translation for translated subtitles.
- Notes need to verify current docs for volatile feature support.

Critical failures:

- Produces a Deepgram-only translated subtitle workflow as if officially documented.

### 3. How should diarization and multichannel be chosen?

Expected answer: Use multichannel when speakers/sources are isolated on separate channels; use diarization when speakers are mixed in one channel. Diarization yields speaker clusters/numbers, not verified identities, and can fail with crosstalk/overlap/music/short turns. For streaming, prefer documented `diarize_model` rather than deprecated `diarize=true`, and do not request unsupported streaming diarization versions.

Required points:

- Correct channel-vs-speaker distinction.
- Notes numeric speaker clusters are not identities.
- Mentions streaming `diarize_model`/version caveat.
- Includes QA of speaker labels.

Critical failures:

- Treats diarization as biometric identification.
- Uses both multichannel and diarization casually without explaining the tradeoff.

### 4. What are the Audio Intelligence features and caveats?

Expected answer: Deepgram documents summarization, topic detection, intent recognition, sentiment analysis, and entity detection. Feature support varies by language and streaming/pre-recorded workflow; the skill notes current docs have per-feature limits and possible inconsistencies, so official pages must be checked immediately before promising support. Add-ons can lower concurrency and add cost/latency/warnings. Entity streaming has finalization tradeoffs.

Required points:

- Names the feature set.
- Mentions language/streaming limitations.
- Mentions rate/cost/latency/concurrency tradeoffs.
- Treats labels/summaries as analysis outputs requiring QA, not deterministic truth.

Critical failures:

- Claims every intelligence feature works in all languages and live streams.

### 5. What should a production TTS workflow do with Aura?

Expected answer: Choose a documented Aura model/voice such as `aura-2-...`, audition before batch, rewrite text for speech, chunk below the documented 2000-character limit at sentence/beat boundaries, use REST for media assets and WebSocket for streaming/interactive output, use controls/pronunciation when documented for the language, then loudness-normalize/mix outside Deepgram.

Required points:

- REST vs WebSocket distinction.
- 2000-character limit.
- Voice audition and frozen voice/parameters.
- Speech-friendly text and pronunciation handling.
- Postprocessing outside Deepgram.

Critical failures:

- Sends a whole long script as one unbounded request.
- Claims Deepgram Aura can clone a specific person's voice by default.

### 6. What privacy and retention claims are safe?

Expected answer: Deepgram publishes security/compliance and model-improvement/opt-out docs, but an agent must not promise zero data retention or regulated compliance unless the user's contract/account configuration confirms it. Obtain consent, minimize audio, use redaction when needed, store artifacts according to retention policy, and save transcripts because Deepgram docs warn responses are the retrieval opportunity.

Required points:

- Consent before processing voice.
- No unsupported ZDR/compliance promise.
- Mentions `mip_opt_out`/model improvement opt-out as documented but not equivalent to full ZDR.
- Artifact custody and retention plan.

Critical failures:

- Claims all Deepgram cloud API requests are zero-retention by default.
- Ignores consent for recorded calls.

### 7. How should the agent handle costs and limits?

Expected answer: Re-check current pricing/rate-limit docs on the day of the run. Plan around separate pricing for STT models/add-ons/TTS/Voice Agent, plan concurrency by product/model/region/plan, and if multiple services are used in one request, use the lower applicable limit. Implement queueing, retries/backoff, and usage tags.

Required points:

- Volatile verification.
- Concurrency varies by product/model/region/plan.
- Add-ons can lower limits/cost more.
- Queue/backoff/billing tags.

Critical failures:

- Quotes stale prices as guaranteed.
- Ignores rate limits in a batch/live production plan.

## Production-decision scenarios

### Scenario A: 90-minute legal deposition, two lav channels, sensitive PII, final transcript and captions

Strong decision:

- Use pre-recorded REST, not live streaming or Voice Agent.
- Use Nova-3 unless legal/domain requirements support another current model.
- Use `multichannel=true` because channels isolate speakers; avoid relying only on diarization.
- Use `smart_format`, `utterances`/`paragraphs`, word timings, and redaction if permitted by legal workflow.
- Save raw JSON, transcript, SRT/VTT, request metadata, warnings, and QA corrections.
- Verify consent/legal authority and retention; do not process under unconfirmed ZDR.
- Run manual QA for names, legal terms, numbers, and redaction.

Penalize:

- Voice Agent recommendation.
- No custody/consent discussion.
- Treating redaction as perfect.

### Scenario B: Bilingual English/Spanish live sales webinar wants live captions and translated Spanish subtitles after the event

Strong decision:

- Use live streaming Nova-3 with multilingual/code-switching settings only after verifying supported languages; or use the current documented multilingual model path.
- Explain live code-switching is transcription, not translation.
- Capture final transcript JSON and create post-event translated subtitles with a separate translation workflow.
- Tune interim/final display and endpointing.
- QA translations and terminology.

Penalize:

- Promising Deepgram-only live translation.
- Using language detection for streaming despite the current docs warning against it.

### Scenario C: Website chat support voice bot with barge-in and tool calls

Strong decision:

- Use Voice Agent or Flux + separate LLM/TTS; justify based on required orchestration control.
- Configure Settings immediately, including listen/think/speak providers, prompt, tools, audio format, and voice.
- Test interruption, silence, endpointing, function-call errors, warning/error messages, and privacy logging.
- Avoid using pre-recorded REST.

Penalize:

- Builds a batch transcription pipeline.
- Ignores turn detection and barge-in.

### Scenario D: 10-minute training video narration with product names and acronym-heavy copy

Strong decision:

- Use Aura TTS REST, audition voice(s), rewrite text for speech, chunk under 2000 characters at scene boundaries, apply speed/pronunciation controls if supported, generate per-scene audio assets, then normalize/mix externally.
- Store model/voice/parameters and script version.
- Warn that Aura is not custom voice cloning.

Penalize:

- Uses Voice Agent for non-interactive narration.
- Fails to handle acronyms/product pronunciations.

## Applied task rubrics

### Task 1: User asks, "Transcribe this podcast and give me clips, captions, topics, and speaker labels."

Score out of 10:

- 2: Chooses pre-recorded REST with Nova-3 and appropriate transcript features.
- 2: Handles diarization vs multichannel based on media inspection.
- 1: Generates/derives SRT/VTT with caption QA.
- 1: Uses topics/summaries with current support caveat and warnings handling.
- 1: Stores raw JSON and derived artifacts.
- 1: Includes clip-friendly timestamps/utterances.
- 1: Includes privacy/consent/rights.
- 1: Identifies failure modes and manual QA.

Critical failure cap: maximum 5 if the response omits raw JSON/artifact custody; maximum 4 if it uses Voice Agent.

### Task 2: User asks, "Make a live captioning plan for a noisy conference hall."

Score out of 10:

- 2: Uses streaming WebSocket with Nova-3 and accurate audio format parameters.
- 1: Explains interim vs final display behavior.
- 1: Tunes endpointing/utterance/speech events.
- 1: Addresses noise/crosstalk/mic routing.
- 1: Persistence/reconnect/gap handling.
- 1: Captions accessibility QA.
- 1: Rate-limit and latency monitoring.
- 1: Does not overpromise diarization/identity.
- 1: Privacy/notice signage or consent.

Critical failure cap: maximum 5 if audio encoding/sample rate/channel declaration is absent.

### Task 3: User asks, "Generate a Deepgram voiceover for my product launch."

Score out of 10:

- 2: Uses Aura TTS REST, not STT/Voice Agent.
- 1: Selects documented voice ID after current verification/audition.
- 1: Chunks under 2000 characters at beat boundaries.
- 1: Rewrites/directs text for speech.
- 1: Handles pronunciation and speed controls with support caveats.
- 1: Specifies output encoding/container/sample rate.
- 1: Plans QA/listening pass and retakes.
- 1: External loudness/mix.
- 1: Synthetic voice disclosure/rights when appropriate.

Critical failure cap: maximum 4 if it claims to clone a celebrity/founder voice without explicit rights and a documented provider path.

### Task 4: User asks, "Analyze call-center recordings for sentiment, intent, summaries, and compliance risk."

Score out of 10:

- 2: Chooses pre-recorded STT/audio intelligence and names supported features.
- 1: Checks language and feature support rather than assuming all languages.
- 1: Applies redaction/PII handling.
- 1: Uses tags/request metadata for usage and audit.
- 1: Notes add-on cost/concurrency impact.
- 1: Treats sentiment/intent as model outputs needing QA/escalation, not legal conclusions.
- 1: Stores artifacts and warnings.
- 1: Includes sampling/quality benchmark plan.
- 1: Consent/retention/compliance handling.

Critical failure cap: maximum 5 if it presents sentiment/intent as definitive compliance determinations.

## Overall scoring

- 9-10: Production-ready. Correct endpoint/model choices, strong caveats, privacy/custody, and QA.
- 7-8: Usable with minor omissions. Endpoint choices mostly right; some QA/cost/privacy detail missing.
- 5-6: Risky. Understands some capabilities but misses important limits or operational details.
- 3-4: Poor. Generic Deepgram advice, wrong model/endpoint choices, unsupported claims.
- 0-2: Failing. Invents capabilities, ignores consent/privacy, or cannot distinguish STT/TTS/Voice Agent.
