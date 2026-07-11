---
name: elevenlabs-scribe
description: "Use ElevenLabs Scribe for speech-to-text production workflows: transcribing audio or video files, diarization and speaker/channel handling, word/character timestamps, captions/subtitles, keyterm prompting, entity detection/redaction, webhooks, realtime STT boundaries, pricing/limits, privacy/retention, consent, artifact custody, and QA for podcasts, interviews, edits, accessibility captions, and localization prep."
---

# ElevenLabs Scribe speech-to-text

Use this skill when a media-production task needs ElevenLabs Speech to Text (Scribe) for transcripts, caption timing, speaker-labeled interview logs, podcast edit prep, accessibility subtitles, localization handoff, call/interview analysis, or transcript cleanup. Do not use it as a text-to-speech, dubbing, voice cloning, or translation skill; Scribe produces text, timing, and metadata from existing audio/video. Use dubbing or TTS skills only after the transcript is verified and the user has rights to transform the source.

Volatile facts below were verified from official ElevenLabs documentation on 2026-07-10. If building against the live API, re-check model names, limits, pricing, residency endpoints, and retention options before irreversible production work.

## Source-grounded facts

### Current models and fit

- Use `scribe_v2` for batch/file transcription. ElevenLabs documents Scribe v2 as supporting 90+ languages, word-level timestamps, speaker diarization up to 32 speakers, dynamic audio tagging, keyterm prompting, entity detection, and smart language detection.
- Use `scribe_v2_realtime` only for live streaming use cases such as agents, live meetings, or interactive monitoring. It is a WebSocket STT service, not the normal path for post-production captions from a finished file.
- Treat `scribe_v1` as retired/unsafe for new work. The API schema still listed `scribe_v1` as an allowed value when checked, but the official changelog announced Scribe v1 removal on 2026-07-09. Prefer `scribe_v2` and flag any Scribe v1 dependency as a migration issue.

### Inputs, outputs, and request shape

Batch endpoint: `POST https://api.elevenlabs.io/v1/speech-to-text` with multipart form data.

Inputs:

- Provide exactly one file input path or URL source. The current API reference describes `file` upload and `source_url`; `cloud_storage_url` is deprecated in favor of `source_url`.
- Audio and video files are accepted. Official docs list common audio formats including AAC, AIFF, OGG, MP3, OPUS, WAV, FLAC, M4A, WebM, and common video formats including MP4, AVI, MKV, MOV, WMV, FLV, WebM, MPEG, and 3GPP.
- Documentation conflict on file size: the API reference states uploaded files must be less than 5.0 GB, while the overview/key-facts page states a 3 GB maximum. For production planning, use 3 GB as the conservative preflight limit unless a current API test or account documentation confirms a larger limit.
- Documentation conflict on duration/multichannel: the overview FAQ says standard mode supports up to 10 hours and combined multichannel duration must be under 10 hours, while key facts says multichannel maximum duration is 1 hour. Treat 1 hour as the conservative multichannel planning limit for unattended production and chunk longer files.

Core response fields:

- `language_code`, `language_probability`, `text`, and `words`.
- `words[]` entries can include `text`, `start`, `end`, `type`, `speaker_id`, `characters`, and `logprob` depending on requested options.
- Word types include `word`, `spacing`, and `audio_event`. `audio_event` represents non-speech sounds such as laughter or applause when event tagging is enabled.

Useful parameters:

- `model_id="scribe_v2"`.
- `language_code`: ISO-639-1 or ISO-639-3; provide it when the language is known and stable, otherwise allow automatic detection.
- `timestamps_granularity`: `word` by default; `character` returns character-level timing per word; `none` reduces timing detail and should not be used for captions, edit decision lists, or multichannel combined output.
- `tag_audio_events`: defaults to true; use it for podcasts, documentary, accessibility, and edit notes where laughter, applause, footsteps, or other events matter. Disable it only when the downstream deliverable must be pure spoken text.
- `diarize`: false by default; set true for mixed-mono multi-speaker recordings when speaker labels are useful.
- `num_speakers`: optional 1-32 maximum speaker hint. Use it when the speaker count is known; omit when uncertain and tune with QA.
- `diarization_threshold`: optional 0.1-0.4, only when `diarize=true` and `num_speakers` is not set. Higher threshold tends to merge speakers; lower threshold tends to split speakers. Default is model-chosen, usually around 0.22.
- `keyterms`: bias transcription toward product names, names, jargon, brands, URLs, acronyms, and proper nouns. Batch Scribe v2 allows up to 1000 keyterms, each under 50 characters and up to 5 words after normalization; realtime allows up to 50 keyterms, each under 20 characters. Keyterm prompting adds cost.
- `no_verbatim`: Scribe v2 option that removes filler words, false starts, disfluencies, and non-speech sounds for cleaner subtitles/summaries. Do not enable when legal, research, investigative, qualitative interview, or documentary integrity requires verbatim speech.
- `temperature`: usually omit or keep 0/near 0 for production; higher values can make results less deterministic and are rarely desirable for transcription.
- `seed`: best-effort deterministic sampling, not guaranteed.

### Speaker handling: diarization, channel separation, speaker library, roles

Choose speaker strategy before sending the file:

1. If every participant is isolated on a separate audio channel, use multichannel mode.
2. If all speakers are mixed into one mono/stereo bed, use diarization.
3. If only one narrator is present, do not request diarization; verify the output as a single-speaker transcript.

Multichannel mode:

- Set `use_multi_channel=true`, `diarize=false`, and `timestamps_granularity=word` or `character`.
- Supports up to 5 channels; each channel is processed independently and mapped deterministically to `speaker_0`, `speaker_1`, etc.
- Do not set `num_speakers`; channel count determines speaker count.
- `multichannel_output_style="separate"` returns one transcript per channel under `transcripts`.
- `multichannel_output_style="combined"` returns one top-level transcript with words merged and sorted by start time; each word carries `channel_index`. Combined output requires timestamps and does not support webhook delivery, entity detection, or redaction.
- Billing and concurrency scale linearly by channel duration. A 60-minute, 3-channel file can cost and count like 180 channel-minutes.

Diarization mode:

- Set `diarize=true` when speaker turns matter and channels are not isolated.
- Provide `num_speakers` when known (for example, host + guest = 2). If speaker count is unknown, leave `num_speakers` null and inspect clustering.
- Use `diarization_threshold` only after a first pass shows systematic over-splitting or merging; do not tune blindly.
- Diarization labels are not identity verification. `speaker_0` means "cluster 0," not a confirmed person. Human-map labels to names after listening.

Speaker library and roles:

- The API reference includes `use_speaker_library` to match known speakers in a workspace speaker library during diarization. Use only when the workspace has deliberately registered speakers and the user has rights/consent to identify them.
- The API reference includes `detect_speaker_roles` for `agent`/`customer` role labels. It requires `diarize=true`, cannot be used with multichannel mode, and adds cost. Use only for call-center style audio, not normal podcasts or documentaries.

### Captions, subtitles, and edit prep

Use `additional_formats` when the API client supports it, or generate captions from the JSON response if the SDK/tool layer does not expose it. The official API schema lists export option variants including `docx`, `html`, `pdf`, `segmented_json`, `srt`, and `txt`; the ElevenLabs product UI documents subtitle exports as SRT and VTT, and transcript exports as plain text, JSON, HTML, SRT, and VTT. Confirm the exact API variant supported by the client before promising VTT via API.

For caption workflows:

- Request `timestamps_granularity=word`.
- Use SRT/VTT as draft deliverables, not final accessibility captions, unless the user accepts machine captions.
- For readable captions, prefer `no_verbatim=true` only when the deliverable is subtitles/summaries and the raw transcript is separately preserved.
- Build captions from word timestamps into cues that meet platform constraints: roughly 1-2 lines, readable character count, no excessive cue duration, no overlap, and cuts placed at phrase boundaries.
- Keep the raw transcript JSON as the source of truth. Treat SRT/VTT as derived artifacts.
- ElevenLabs' product subtitle editor keeps transcript and subtitle edits separate; if a human edits captions, do not assume those edits changed the underlying transcript.

For edit prep:

- Preserve word-level timestamps for paper edits, soundbite selection, and jump-cut planning.
- Convert speaker-labeled words into turn-level segments with `speaker_id`, `start`, `end`, `text`, and confidence/QA notes.
- Keep audio events when they may influence story rhythm, reaction beats, applause, laughter, or accessibility.

### Async jobs and webhooks

For small/interactive jobs, use synchronous batch transcription and wait for the JSON response.

For long files, high volume, or unattended processing:

- Configure a Speech-to-Text webhook in the ElevenLabs dashboard.
- Send `webhook=true`; the request returns early with a request identifier and the transcript arrives later via webhook.
- Use `webhook_id` to target a specific configured webhook when multiple webhooks exist.
- Use `webhook_metadata` for project IDs, source asset IDs, expected duration, hash, editor job ID, and custody references. Keep it shallow: official docs specify max depth 2 and max size 16 KB.
- Verify webhook signatures. ElevenLabs docs recommend HMAC or OAuth auth methods and signature verification.
- Webhook URLs must be HTTPS.
- Return 2xx only after the payload is durably stored. Return 5xx for retryable server failures; 4xx indicates non-retryable client errors.
- Combined multichannel output is not supported with webhook delivery; use separate output and merge client-side.

### Entity detection, redaction, and sensitive content

Scribe v2 supports entity detection with exact positions/timestamps and categories such as `pii`, `phi`, `pci`, `other`, and `offensive_language`, plus many individual labels (names, DOBs, credit cards, SSNs, health conditions, medications, locations, emails, phone numbers, URLs, etc.). It adds cost.

Use entity detection when:

- Preparing public clips from customer calls or interviews.
- Creating localization or editing notes from recordings containing personal, medical, financial, or account data.
- Building redaction review queues.

Use entity redaction when the transcript itself must be safe to share. The API reference requires redaction targets to be a subset of `entity_detection`; redaction suppresses the `entities` field. Redaction can be formatted as `{REDACTED}`, `{ENTITY_TYPE}`, or enumerated entity markers.

Do not rely solely on automated redaction for regulated or public release. Use it as a first pass, then human-review the original audio and the transcript.

### Pricing, costs, and limits

Official API pricing verified 2026-07-10:

- Scribe v1/v2: listed at $0.22 per hour.
- Scribe v2 Realtime: listed at $0.39 per hour.
- Entity detection: listed as $0.070 per hour.
- Keyterm prompting: listed as $0.050 per hour in the pricing table, while the API reference describes keyterms as a 20% surcharge on base transcription cost. Treat pricing as volatile; quote both only if explaining the discrepancy and re-check before quoting a client.
- API reference describes entity detection and redaction as adding 30% surcharges, and role detection as adding a 10% surcharge.
- Multichannel bills each channel independently at full duration.

Preflight costs with:

`billable_audio_hours = duration_hours * max(1, channel_count_when_multichannel)`

Then add enabled-feature surcharges. If docs disagree, show the user the conservative estimate and cite the verification date.

### Privacy, retention, security, and custody

Do not upload source recordings until the user has confirmed rights, consent, and privacy posture appropriate to the material.

Official retention/security facts verified 2026-07-10:

- By default, ElevenLabs retains data in accordance with its Privacy Policy for service improvement, troubleshooting, and system security.
- Enterprise customers may have Zero Retention Mode for Speech to Text. For API products, it is enabled with `enable_logging=false`; when used on STT, request audio input and text output are not logged/stored long-term, but support/debugging is limited and transcript storage features are unavailable.
- Zero Retention Mode is available only to select enterprise customers; HIPAA-related integrations require contacting ElevenLabs Sales to sign a BAA before processing HIPAA workloads.
- ElevenLabs documentation recommends service accounts, environment separation, scoped API keys, least privilege, and resource-level permissions.
- Official docs list EU, India, and Singapore isolated data-residency API/WebSocket base URLs; the standard environment is U.S.-hosted by default, and `api.us.elevenlabs.io` can pin API traffic to U.S. servers for latency/routing needs. Use the workspace's configured environment endpoint when required by contract; do not assume the public global endpoint satisfies residency.
- Webhooks can carry transcript text and metadata. Treat webhook payloads as sensitive production artifacts.

Artifact custody rules:

- Store raw audio/video, submitted chunks, returned JSON, SRT/VTT/DOCX/PDF exports, redacted variants, and human-edited caption files as separate artifacts with provenance.
- Record request parameters, model ID, verification date, source media hash, chunk boundaries, channel mapping, speaker-label mapping, cost estimate, and retention mode.
- Never overwrite the raw transcript when producing a cleaned transcript; keep `raw`, `corrected`, `caption`, and `redacted` states distinct.
- Avoid sending presigned URLs that outlive the transcription job. Use least-privilege URLs and revoke or expire them after completion.
- Keep API keys server-side; use single-use tokens only for client-side realtime STT when the current docs support that flow.

### Consent, rights, safety, and disclosure

For transcription, the key rights issue is usually recording and processing human speech, not voice synthesis. Before transcribing:

- Confirm the user has the right to upload and process the recording.
- For private calls, interviews, minors, medical/financial data, or workplace recordings, require documented consent or a clear legal basis. Recording-consent laws vary by jurisdiction; do not infer permission from possession of a file.
- Warn the user before sending sensitive source media to a cloud API. Offer local/offline transcription if required by the project even when Scribe quality would be better.
- For public-facing captions, summaries, or clips, disclose material AI involvement when required by policy, platform rules, contract, or local law.
- Do not use Scribe output to impersonate, surveil, dox, harass, evade consent, or create misleading attribution.
- If a transcript will be used to generate a dub, clone a voice, or synthesize replacement speech, stop and apply the relevant voice consent/dubbing/TTS policy; transcription consent does not automatically authorize synthetic speech generation.

## Production workflow

1. Audit the source.
   - Identify duration, file size, format, channel count, language(s), speaker count, privacy sensitivity, and downstream deliverable.
   - For video, decide whether to upload video directly or extract audio first. Extracting clean WAV can reduce upload size and make custody clearer.

2. Choose mode.
   - Single speaker: `diarize=false`.
   - Mixed speakers in one track: `diarize=true`, optional `num_speakers`.
   - Isolated speaker channels: `use_multi_channel=true`, `diarize=false`.
   - Live/agent: `scribe_v2_realtime`, WebSocket workflow.

3. Prepare audio.
   - Prefer clean, lossless or high-quality audio. For multichannel, remove unused channels and ensure one speaker per channel.
   - For long or high-risk files, chunk at natural silences or known timecode intervals and preserve offset metadata.
   - For `pcm_s16le_16`, ensure 16-bit PCM, 16 kHz, mono, little-endian; use it only when low latency matters and the ingest tool can meet the format exactly.

4. Add vocabulary and privacy options.
   - Build `keyterms` from names, brands, product terms, acronyms, domain terms, episode titles, and non-English proper nouns.
   - Add `entity_detection`/`entity_redaction` only when needed; account for cost and output-shape effects.
   - Use `enable_logging=false` only when the account is enterprise-enabled for Zero Retention Mode and the loss of request history/transcript storage is acceptable.

5. Transcribe and preserve raw artifacts.
   - Save raw JSON before cleanup.
   - Save request metadata and source hash.
   - For webhooks, verify signatures and persist payloads idempotently by request ID.

6. QA before using output.
   - Listen-check a representative sample and all critical segments.
   - Verify speaker turns, names, numbers, timestamps near edits, and any legal/medical/financial terms.
   - Compare source duration to transcript coverage; investigate large gaps, repeated sections, or timestamp drift.
   - For captions, watch the video with captions enabled and check readability, line breaks, cue timing, and scene-cut clashes.

## Operational observations

- Mixed-mono diarization is useful but not identity-proof; overlapping speech, crosstalk, similar voices, room reverb, and telephone audio can split one speaker into several clusters or merge different speakers.
- Multichannel mode is usually cleaner than diarization when each speaker is truly isolated; it is worse when channels bleed heavily or contain multiple people.
- Keyterms help with spelling and jargon, but too many weak terms can increase cost and may bias output in surprising places. Prefer a curated list of high-value terms.
- `no_verbatim=true` can improve subtitle readability but can erase hesitation, emotion, and evidence that matters in documentary, research, legal, or editorial contexts.
- Audio-event tags are useful for accessibility and edit rhythm but may be noisy; treat them as annotations to review, not final stage directions.
- Webhook jobs need idempotent storage because retries or duplicate notifications can happen in production systems.

## Production heuristics

- For podcasts/interviews: request word timestamps, diarization or multichannel labels, audio events on, keyterms for guest names and show-specific vocabulary, then produce both raw and cleaned turn-level transcripts.
- For social captions: preserve raw JSON, create a cleaned subtitle draft with `no_verbatim=true` only if the user wants readable captions, then human-check cue timing against the final cut.
- For localization prep: use Scribe to produce the source transcript and timing, then hand off verified text to translation/dubbing. Do not treat Scribe as a translation system.
- For edit decisions: derive segments from word timestamps but snap final cuts to audio/video review, not just word boundaries.
- For sensitive calls: use entity detection/redaction as a triage layer, use enterprise zero retention if available, and keep redacted and unredacted transcripts in separate access-controlled stores.
- For long files: prefer webhooks or chunking. Chunk on silence when possible; otherwise carry exact time offsets and verify no words are lost at boundaries.

## Examples

### Example: two-person podcast edit prep from mixed stereo/mono

Production intent: create a searchable transcript, host/guest turn list, and candidate clips from a 72-minute podcast where speakers are mixed into one track.

Workflow:

1. Extract audio to a clean WAV if the source is a video file.
2. Submit to Scribe v2:

```json
{
  "model_id": "scribe_v2",
  "diarize": true,
  "num_speakers": 2,
  "timestamps_granularity": "word",
  "tag_audio_events": true,
  "keyterms": ["guest name", "company name", "product name", "technical acronym"],
  "no_verbatim": false
}
```

Expected result:

- Raw JSON with word timestamps and `speaker_id` clusters.
- Turn-level transcript after grouping consecutive words by speaker.
- Audio events retained for laugh/applause/reaction beats.

Failure modes:

- Speaker clusters swap after silence or crosstalk.
- Product names still misspelled if keyterms are incomplete.
- Timestamp drift around long music beds or ads.

Variations:

- If each participant is on a separate channel, use multichannel mode instead of diarization.
- For public show notes, create a cleaned transcript after preserving the verbatim raw transcript.

### Example: dual-channel customer call with redaction

Production intent: create a safe review transcript from a customer-support call where agent and customer are on separate channels and may mention account data.

Workflow:

```json
{
  "model_id": "scribe_v2",
  "use_multi_channel": true,
  "diarize": false,
  "multichannel_output_style": "separate",
  "timestamps_granularity": "word",
  "entity_detection": ["pii", "pci"],
  "entity_redaction": ["pii", "pci"],
  "entity_redaction_mode": "enumerated_entity_type",
  "tag_audio_events": false
}
```

Expected result:

- Separate channel transcripts mapped to `speaker_0` and `speaker_1`.
- Redacted transcript text suitable for broader internal review.
- No unredacted `entities` field when redaction is enabled.

Failure modes:

- Request fails if combined multichannel output is requested with entity detection/redaction.
- Channel bleed can put a customer word on the agent channel.
- Automated redaction may miss spoken variants of IDs; human review remains required before external release.

Variations:

- If roles are not channel-isolated but the audio is a call-center style mono mix, consider `detect_speaker_roles=true` with `diarize=true`, accounting for cost and QA.
- For asynchronous processing, use webhook delivery with separate output and merge client-side if needed.

### Example: caption draft for a product-launch video

Production intent: generate first-pass captions for a 90-second final MP4 and hand them to an editor.

Workflow:

```json
{
  "model_id": "scribe_v2",
  "timestamps_granularity": "word",
  "language_code": "en",
  "tag_audio_events": true,
  "no_verbatim": true,
  "additional_formats": [
    {
      "format": "srt",
      "max_segment_duration_s": 4,
      "max_characters_per_line": 42
    }
  ],
  "keyterms": ["brand name", "feature name", "speaker name"]
}
```

Expected result:

- Raw transcript JSON plus an SRT draft if the client/tool exposes `additional_formats`.
- Captions that are cleaner than verbatim but still require watch-through.

Failure modes:

- SDK wrapper may not expose returned `additional_formats`; generate SRT from JSON if needed.
- `no_verbatim=true` may remove intentional repetitions or brand-style speech.
- Captions can cross shot cuts or exceed platform readability constraints.

Variations:

- Disable `no_verbatim` if legal approval requires exact spoken words.
- If the final deliverable is VTT and API VTT support is not confirmed in the current client, generate VTT from the verified word-timed JSON or ElevenLabs UI export.

## Source links verified 2026-07-10

- ElevenLabs Speech to Text overview: https://elevenlabs.io/docs/overview/capabilities/speech-to-text
- ElevenLabs Speech to Text API reference: https://elevenlabs.io/docs/api-reference/speech-to-text/convert
- ElevenLabs Scribe model overview: https://elevenlabs.io/docs/overview/models
- ElevenLabs realtime STT API reference: https://elevenlabs.io/docs/api-reference/speech-to-text/v-1-speech-to-text-realtime
- ElevenLabs multichannel STT guide: https://elevenlabs.io/docs/eleven-api/guides/how-to/speech-to-text/batch/multichannel-transcription
- ElevenLabs asynchronous STT/webhooks guide: https://elevenlabs.io/docs/eleven-api/guides/how-to/speech-to-text/batch/webhooks
- ElevenLabs keyterm prompting guide: https://elevenlabs.io/docs/eleven-api/guides/how-to/speech-to-text/batch/keyterm-prompting
- ElevenLabs entity detection guide: https://elevenlabs.io/docs/eleven-api/guides/how-to/speech-to-text/batch/entity-detection
- ElevenLabs subtitles product guide: https://elevenlabs.io/docs/eleven-creative/products/subtitles
- ElevenLabs API pricing: https://elevenlabs.io/pricing/api
- ElevenLabs Zero Retention Mode: https://elevenlabs.io/docs/eleven-api/resources/zero-retention-mode
- ElevenLabs Data residency: https://elevenlabs.io/docs/overview/administration/data-residency
- ElevenLabs Latency optimization / U.S. API routing: https://elevenlabs.io/docs/eleven-api/guides/how-to/best-practices/latency-optimization
- ElevenLabs security best practices: https://elevenlabs.io/docs/eleven-api/guides/how-to/best-practices/security
- ElevenLabs changelog Scribe v1 removal notice: https://elevenlabs.io/docs/changelog
- ElevenLabs DPA and Privacy Policy: https://elevenlabs.io/dpa and https://elevenlabs.io/privacy-policy
- ElevenLabs Prohibited Use Policy and Safety page: https://elevenlabs.io/use-policy and https://elevenlabs.io/safety
