# Evaluation spec for `assemblyai-transcription`

This file is an answer key and scoring guide for evaluating agents that used only `SKILL.md`. Do not expose this file to evaluated agents.

Score out of 100. A passing answer should demonstrate AssemblyAI-specific production judgment, not generic transcription advice. Give partial credit for equivalent terminology when technically correct.

## Critical failure conditions

Fail the response regardless of point total if it:

- Claims unsupported capabilities as native AssemblyAI features, such as fully publication-ready translated subtitles without a translation/subtitle QA step, automatic perfect speaker names without known-value identification or human review, or guaranteed legal/medical compliance from PII redaction alone.
- Recommends exposing the AssemblyAI API key in a browser or client-side app.
- Treats real-time streaming billing as based only on audio sent rather than WebSocket session duration.
- Ignores consent/privacy for sensitive or recorded-human speech workflows.
- Says PII redaction redacts every output field, despite the documented limitation that other feature outputs may still contain PII.
- Uses the deprecated `auto_chapters` transcription parameter as the recommended chapter workflow without noting deprecation.
- Advises a large polling-heavy batch without addressing the HTTP rate limit or webhooks.

## Knowledge questions

### 1. Which AssemblyAI surface should be used for a 90-minute podcast, a 20-second voice-agent turn, and live webinar captions?

Expected answer:

- 90-minute podcast: pre-recorded/async STT through `/v2/transcript`, with polling or webhooks.
- 20-second voice-agent turn: Sync STT can be appropriate if the clip is under the documented short-file limit, or streaming if it is part of an ongoing live conversation.
- Live webinar captions: real-time/streaming STT over WebSocket.

Required points:

- Distinguishes async, sync, and streaming boundaries.
- Notes that final media captions should often be re-run async after a live event.
- Does not route a long podcast through Sync STT.

### 2. What are the documented speaker diarization controls and risks?

Expected answer:

- Enable with `speaker_labels: true`.
- Results are returned in `utterances` with generic speaker labels and millisecond timestamps.
- `speakers_expected` is an exact/hard boundary; min/max speaker options are hard lower/upper boundaries.
- Incorrect exact counts can merge or split speakers.
- Diarization works better with sufficient continuous speech per speaker and worse with crosstalk, noise, similar voices, or short backchannels.
- Speaker names/roles require separate identification or human mapping.

Penalize:

- Treating `speakers_expected` as a harmless hint.
- Publishing speaker names without verification.

### 3. Explain AssemblyAI subtitle/caption output and what QA is still required.

Expected answer:

- SRT or VTT can be exported from completed transcripts with the subtitle endpoint.
- Word-level timestamps and utterance timestamps support edit and caption work.
- QA must check timing, line breaks, reading speed, names, speaker labels, profanity/house style, and accessibility labels.
- Translated subtitles require separate translation/localization and subtitle timing review.

### 4. What is the difference between language detection and translation?

Expected answer:

- Language detection identifies the dominant spoken language and routes to an appropriate model; it returns language metadata such as `language_code` and model-used fields.
- Translation is a Speech Understanding/LLM Gateway workflow that produces translated text outputs for target languages.
- Detection/transcription and translation are not the same as ready-to-publish localized subtitles.

### 5. What should an agent know about AssemblyAI data controls and retention?

Expected answer:

- Paid accounts can access Data Controls for model-improvement opt-out, TTL, and BAA.
- Free users cannot use those controls.
- BAA execution opts the account out of model improvement.
- Opt-out is forward-looking.
- Async artifact retention varies by artifact and account settings; TTL can be as low as 1 hour for final artifacts; metadata may remain for logging/billing.
- Streaming can have zero retention for audio/transcripts when opted out, with metadata retained.
- LLM Gateway provider training opt-out is separate from AssemblyAI’s own model-improvement program.

Penalize:

- Claiming all data is always zero-retention by default.
- Omitting model-training opt-out when handling sensitive speech.

## Production-decision questions

### 6. Scenario: A producer has a three-speaker panel recording on one mixed channel and needs captions, chapters, pull quotes, and a show-notes draft.

Strong answer should:

- Choose pre-recorded STT, likely Universal-3.5 Pro if supported language and accuracy matter.
- Enable speaker diarization and set exact or min/max speaker controls carefully.
- Add keyterms/prompting for panelist names, organizations, jargon, and show title.
- Use webhook or reasonable polling; store transcript ID.
- Export JSON, utterances, SRT/VTT, paragraphs/sentences.
- Use summaries/chaptering/key phrases/entities as assistive indexes and require human editorial review.
- QA speaker labels, proper nouns, captions, and quote context.
- Record consent/rights and retention requirements.

Scoring rubric (15 points):

- Correct API/model surface: 3
- Speaker strategy: 3
- Caption/edit artifacts: 3
- Speech Understanding used appropriately: 2
- Lifecycle/cost/rate/privacy awareness: 3
- Human QA: 1

Critical failures:

- No human speaker/caption QA.
- Claims chapters or summaries are publish-ready without review.

### 7. Scenario: A web app needs live browser captions for users joining from their laptops.

Expected decision:

- Use Real-time STT/WebSocket or SDK streaming.
- Do not put the API key in browser code; generate temporary tokens server-side.
- Use finalized turns for stable captions, optionally display interim text if the UX tolerates changes.
- Include keyterms/prompting for event vocabulary.
- Terminate sessions and log session duration because billing is session-based.
- Monitor WebSocket closures/rate limits; understand new-session rate limits.
- Re-transcribe final recording asynchronously for archive-quality captions if publishing afterward.

Penalize:

- Client-side API key.
- Leaving connections open.
- Confusing async job polling with streaming events.

### 8. Scenario: A healthcare customer wants transcribed visits with PHI and medical terms.

Expected decision:

- Escalate privacy requirements before transcription: paid account, BAA, model-improvement opt-out, TTL, restricted storage, consent.
- Consider Medical Mode for terminology if supported language/model fits.
- Consider PII redaction for downstream editorial/QA artifacts, but note it is not a complete compliance solution and derived fields need separate review.
- Store transcript IDs and deletion deadlines.
- Require human clinical/legal review before use in records.

Critical failures:

- Telling the user automated transcription is HIPAA-compliant by itself.
- Using a free account for PHI.

### 9. Scenario: A localization team wants Spanish and French captions from an English interview.

Expected decision:

- Produce source-language transcript and captions first.
- Use Translation/Speech Understanding or separate translation workflow for Spanish and French text.
- Re-segment translated text for subtitle constraints and QA by a fluent reviewer.
- Preserve source transcript, translated texts, SRT/VTT, and reviewer notes separately.
- Do not assume English timings/line breaks remain correct after translation.

## Applied production tasks

### 10. Task: Write a job plan for bulk-transcribing 20,000 historical interview files.

Essential successful output:

- Pilot run with representative sample.
- Preflight: account rate limits, pricing, model/language/support, add-ons, region, retention, storage.
- Upload or URL strategy with URL TTL long enough for queue/processing.
- Webhooks preferred; polling fallback with jitter/widening.
- Submission ramp and in-flight cap below account parallel limit.
- Retry policy distinguishing 4xx from 5xx and dead-letter handling.
- Ledger with source IDs, transcript IDs, request JSON, status, costs, and deletion deadlines.
- QA sampling and downstream artifact validation before full batch.
- Contact AssemblyAI support/sales for very large rollouts or higher limits.

Rubric (20 points):

- Scaling/rate-limit correctness: 5
- Lifecycle/webhook/retry correctness: 4
- Artifact custody/ledger: 3
- Cost/feature planning: 2
- Privacy/retention: 3
- QA/pilot methodology: 3

Critical failures:

- Polls every job every few seconds without accounting for the 20,000 requests/5 min HTTP cap.
- No pilot or no dead-letter path.

### 11. Task: Design a redacted customer-interview review workflow.

Essential successful output:

- Confirms consent and permitted use.
- Enables PII redaction with selected policies.
- Notes that PII redaction affects main transcript text/words/utterances but other outputs may contain PII.
- If audio review is needed, enables redacted audio, downloads it within the documented availability window, and handles file-size constraints.
- Avoids returning unredacted transcript unless restricted reviewers need it.
- Stores unredacted material separately with TTL/deletion tracking if retained.
- Re-checks summaries/translations/entities and filenames/logs for PII.

Rubric (10 points):

- Correct redaction setup and limitations: 4
- Audio redaction custody: 2
- Privacy/consent/retention: 2
- Derived-artifact review: 2

### 12. Task: Produce an AssemblyAI request sketch for a podcast transcript package.

Expected characteristics:

- Uses pre-recorded STT request with `audio_url`, `speech_model` or `speech_models` according to current docs/SDK conventions, speaker labels, language detection or explicit language, and keyterms/prompting where appropriate.
- Includes webhook URL/auth if using async lifecycle.
- Optionally includes entity/sentiment/summarization/translation/redaction only if justified by production intent.
- Explains expected outputs and failure modes.
- Uses environment variable for API key, not hardcoded secret.

Score up to 10:

- Correct request surface/lifecycle: 3
- Sensible parameters: 3
- Security/custody: 2
- Failure modes/QA: 2

## Overall scoring guide

- 90-100: Strong AssemblyAI-specific production planner. Handles capability boundaries, privacy, cost, lifecycle, QA, and examples accurately.
- 75-89: Usable with minor omissions. May miss one feature nuance but avoids unsafe claims.
- 60-74: Generic but partly correct. Needs reviewer intervention before production.
- Below 60: Insufficient provider knowledge or production safety.

Reviewer notes:

- Reward responses that date volatile facts or say to re-check current pricing/rate limits/model support.
- Reward clear separation between documented facts and production heuristics.
- Penalize marketing-style claims of “best” accuracy unless tied to AssemblyAI’s own dated documentation and framed as provider-documented.
- Penalize unnecessary use of Speech Understanding features when a plain transcript/caption workflow would be cheaper, safer, or easier to QA.
