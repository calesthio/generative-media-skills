---
name: openai-audio
description: Produce and understand audio with OpenAI request-based audio APIs and audio-capable chat models, including text-to-speech, transcription, translation, multimodal audio input/output, model routing, prompt and performance direction, artifact custody, approval gates, and safety/rights review. Use for non-realtime OpenAI audio production; route continuous live voice agents to the separate realtime voice skill.
---

# OpenAI audio

Use this skill when a user wants OpenAI audio production or understanding in a bounded request: generated narration, spoken product demos, podcast or interview transcription, subtitle timing, translation to English, audio QA, or adding audio input/output to an existing chat workflow.

Do not use this as the primary guide for continuous low-latency speech-to-speech agents, live interpreting, SIP/WebRTC sessions, or voice activity detection. Those belong to the separate realtime voice skill. This skill may still explain the boundary: request-based audio APIs fit files, scripts, and bounded requests; realtime sessions fit open connections with live audio events. Documented source: OpenAI’s audio guide distinguishes request-based APIs, realtime sessions, and multimodal chat completions; verified 2026-07-10: https://developers.openai.com/api/docs/guides/audio

## Source status and evidence labels

Treat the following as documented facts verified on 2026-07-10 from OpenAI public docs:

- The request-based speech endpoint is `POST /v1/audio/speech`; it accepts `gpt-4o-mini-tts`, the current pinned snapshot `gpt-4o-mini-tts-2025-12-15`, `tts-1`, and `tts-1-hd`, and supports built-in voices plus custom voice IDs where available. Speech input is limited to 4,096 characters. The older pinned snapshot `gpt-4o-mini-tts-2025-03-20` is scheduled to shut down on 2026-07-23 with `gpt-4o-mini-tts-2025-12-15` as its documented substitute; do not confuse that snapshot retirement with retirement of the unpinned alias. Sources: https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create and https://developers.openai.com/api/docs/deprecations
- `gpt-4o-mini-tts` supports instruction-style voice control; the older `tts-1` and `tts-1-hd` models do not support the `instructions` parameter. Source: https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create
- Speech output formats for `/v1/audio/speech` are documented as `mp3`, `opus`, `aac`, `flac`, `wav`, and `pcm`; `speed` ranges from `0.25` to `4.0`; streaming format can be `sse` or `audio`, with SSE not supported for `tts-1`/`tts-1-hd`. Source: https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create
- The speech-to-text endpoint is `POST /v1/audio/transcriptions`; documented models include `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `gpt-4o-transcribe-diarize`, and `whisper-1`, with response-format and streaming differences by model. File uploads are limited to 25 MB; split or compress larger inputs without cutting mid-sentence. Source: https://developers.openai.com/api/docs/guides/speech-to-text
- `gpt-4o-transcribe-diarize` does not support `prompt`, logprobs, or `timestamp_granularities[]`; input longer than 30 seconds requires `chunking_strategy`, with `"auto"` recommended. Source: https://developers.openai.com/api/docs/guides/speech-to-text
- Transcription streaming is supported for current GPT transcription models, but not for `whisper-1`; streamed transcription emits transcript delta/done events. Source: https://developers.openai.com/api/docs/guides/speech-to-text
- The translation endpoint is `POST /v1/audio/translations`; the API reference states that only `whisper-1` is currently available for translation to English, even though shared model type enums may list additional audio model IDs. Source: https://developers.openai.com/api/reference/resources/audio/subresources/translations/methods/create
- Audio-capable chat completions can use `gpt-audio-1.5` with `modalities: ["text", "audio"]`, an `audio` object for voice/format, and `input_audio` content blocks for audio input. Source: https://developers.openai.com/api/docs/guides/audio
- Realtime routing is separate: the realtime overview points low-latency voice agents to `gpt-realtime-2.1`, live translation to `gpt-realtime-translate`, and live transcription to `gpt-realtime-whisper`. Source: https://developers.openai.com/api/docs/guides/realtime
- Pricing is volatile. As of 2026-07-10, OpenAI’s pricing page lists realtime/audio-generation prices by token or minute and transcription prices for `gpt-4o-transcribe` and `gpt-4o-mini-transcribe` by token with estimated per-minute costs. Always re-check before quoting costs in production. Source: https://developers.openai.com/api/docs/pricing
- OpenAI’s platform data-controls page says API endpoint data is not used for training, lists abuse-monitoring and application-state retention by endpoint, and says `/v1/audio/transcriptions` and `/v1/audio/translations` have no abuse-monitoring retention while `/v1/audio/speech` has 30-day abuse-monitoring retention by default; verified 2026-07-10. Source: https://developers.openai.com/api/docs/guides/your-data
- OpenAI’s usage policies prohibit use of someone’s likeness, including voice, without consent in ways that could confuse authenticity. The TTS guide also requires clear disclosure to end users that the voice is AI-generated, and custom-voice creation is limited to eligible customers and requires separate matching consent and sample recordings. Sources: https://openai.com/policies/usage-policies/ and https://developers.openai.com/api/docs/guides/text-to-speech

Treat the following as production heuristics, not OpenAI guarantees:

- Use `gpt-4o-mini-tts` first when the creative brief needs performance direction, expressive control, or iteration through natural-language voice notes.
- Use `tts-1` only when low latency matters more than quality or detailed direction; use `tts-1-hd` only when an older integration already depends on it or when tests prove it wins for the specific voice/script.
- Use `gpt-4o-transcribe` when accuracy, proper nouns, or speaker-ready output is more important than cost; use `gpt-4o-mini-transcribe` for volume, rough cuts, drafts, and cost-sensitive batch transcription; use `gpt-4o-transcribe-diarize` when speaker labels matter.
- Use `whisper-1` when you need translation-to-English or word/segment timestamp formats that are documented for `whisper-1`; otherwise prefer the newer transcription models after testing on representative audio.
- For finished media, generate high-quality WAV or FLAC intermediates, archive them, and encode MP3/AAC only for delivery copies.

## Route the job before making an API call

Ask or infer these variables before choosing an endpoint:

1. Input: text script, audio file, live microphone stream, or a mixed chat turn with audio.
2. Output: audio file, transcript, translated English transcript, captions, diarized transcript, chat response with audio, or live audio events.
3. Time shape: bounded request versus continuous session.
4. Approval risk: celebrity/employee/customer voice, regulated transcript, public-facing ad, legal/medical/financial content, minors, or sensitive personal data.
5. Artifact custody: where raw inputs, generated audio, transcripts, sidecars, and approvals must be stored.

Decision table:

| User intent | Primary route | Model/API choice | Notes |
|---|---|---|---|
| Generate narration or a spoken line from text | `/v1/audio/speech` | Usually `gpt-4o-mini-tts` | Best fit for file output, batch narration, style-directed voice performance. |
| Generate low-latency speech in an older simple TTS integration | `/v1/audio/speech` | `tts-1` | Accept lower quality; do not send `instructions`. |
| Generate speech when an older high-quality TTS path is required | `/v1/audio/speech` | `tts-1-hd` | Test against `gpt-4o-mini-tts`; do not assume “HD” beats a newer model for every brief. |
| Transcribe a file or bounded upload | `/v1/audio/transcriptions` | `gpt-4o-transcribe` or `gpt-4o-mini-transcribe` | Use model selection by accuracy/cost; request only supported response formats. |
| Transcribe with speaker labels | `/v1/audio/transcriptions` | `gpt-4o-transcribe-diarize` | Use `diarized_json` when speaker annotations are required. |
| Create word/segment timestamps for captions | `/v1/audio/transcriptions` | Often `whisper-1` with `verbose_json` and timestamp granularities | Docs say timestamp granularities require `verbose_json`; word timestamps add latency. |
| Translate non-English audio to English | `/v1/audio/translations` | `whisper-1` | The translation endpoint is not general localization dubbing; it produces English text. |
| Add audio input/output to an existing chat app | Chat Completions | `gpt-audio-1.5` with `modalities` and `audio` | Use when the model must reason over audio and respond in text/audio in one chat turn. |
| Build live speech-to-speech, live translation, live transcription, SIP, WebRTC, or VAD | Realtime API | Route out of this skill | Use the separate realtime voice skill. |

Never silently substitute a route. If the approved path is blocked, say what failed, whether it is model access, parameter incompatibility, policy, privacy, cost, or product mismatch, and ask before switching endpoint or model.

## Text-to-speech production

### Script preparation

Write for spoken performance before prompting. A TTS model can render pacing and tone, but it cannot rescue a script that is visually written, over-punctuated, or full of unexpanded abbreviations.

Production heuristics:

- Convert dense prose into breath-length lines. One idea per sentence is usually safer than nested clauses.
- Spell out pronunciation landmines in the script or instructions: product names, acronyms, people, non-English terms, numerals, units, URLs, and legal disclaimers.
- Use plain punctuation for prosody. Avoid theatrical markup unless the endpoint or downstream tool explicitly supports it.
- Keep pronunciation notes separate from creative performance notes when possible.
- For long narration, chunk at paragraph or scene boundaries and keep voice/instruction settings consistent across chunks.
- Leave a short room-tone or silence handle in post rather than trying to force exact silence inside the script.

Example performance brief shape:

```text
Voice: coral
Model: gpt-4o-mini-tts
Format: wav for editing; mp3 only for review copies
Performance instructions:
Warm, confident startup launch voice. Conversational, not announcer-like.
Medium pace, lightly excited on the first sentence, then grounded.
Pronounce "Aster Lane" as "ASS-ter lane"; pronounce "SOC 2" as "sock two".
Do not impersonate any real person or named celebrity.
```

Documented controls:

- Built-in voices listed in the speech API reference include `alloy`, `ash`, `ballad`, `coral`, `echo`, `fable`, `onyx`, `nova`, `sage`, `shimmer`, `verse`, `marin`, and `cedar`; the TTS guide notes that voice availability depends on model, and older `tts-1`/`tts-1-hd` support a smaller set. Sources: https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create and https://developers.openai.com/api/docs/guides/text-to-speech
- The TTS guide says voices are currently optimized for English and recommends `marin` or `cedar` for best quality; verified 2026-07-10. Source: https://developers.openai.com/api/docs/guides/text-to-speech
- The `instructions` field has a documented maximum length of 4096 characters and does not work with `tts-1` or `tts-1-hd`. Source: https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create

### Voice selection

Do not describe voices only by demographic labels. Describe the performance role the production needs:

- “credible founder reading a release note”
- “gentle tutorial host”
- “premium documentary narrator”
- “fast but legible support IVR”
- “calm safety instruction”

Select 2 or 3 candidate voices, generate short auditions from the same representative line, and get approval before full-run generation. Use the exact final script or a dense excerpt, not a generic demo sentence, because pronunciation and pacing failures often appear only in the real copy.

Approval gate for public-facing voice:

1. Confirm the user has rights to the script and any referenced brand/character.
2. Confirm the selected built-in or custom voice is permitted for the intended use.
3. Confirm no request asks for confusing impersonation of a real person without consent.
4. Generate an audition no longer than needed to judge tone.
5. Store the selected voice, model, instructions, script version hash or filename, approver, date, and approved audition path.
6. Only then generate the full batch.

For a custom voice, also confirm organization eligibility, retain the provider consent-recording ID, verify that the actor in the consent and sample recordings is the same person, and follow the Text-to-Speech Supplemental Agreement. A general email approval is not a substitute for OpenAI's required consent-recording workflow.

### Output formats and custody

Use format by lifecycle:

- `wav` or `flac`: editing masters, archival custody, downstream mixing.
- `mp3` or `aac`: web preview, social draft, compact delivery.
- `opus`: speech-heavy streaming or low-bitrate distribution when supported by the target.
- `pcm`: low-level audio pipelines that require raw PCM.

Record every generated audio artifact with:

- source script path or exact script text;
- model;
- voice;
- instructions;
- response format;
- speed;
- generation date;
- OpenAI request ID if available in SDK logs;
- approval status;
- checksum for the output file;
- any post-processing steps.

Do not overwrite approved masters. If you regenerate a line, create a new versioned file and update the manifest.

### Complete example: narrated product launch line

User intent: create one public-facing launch voiceover line, with approval before batch generation.

Model and endpoint: `/v1/audio/speech`, `gpt-4o-mini-tts`, voice `marin`, WAV master.

This call is the audition/sample, not authorization for a full batch. Run it only after the rights, disclosure, storage, and sample-cost preflight above; require recorded approval of this take before expanding the run.

Python example:

```python
from pathlib import Path
from openai import OpenAI

client = OpenAI()

script = (
    "Aster Lane turns every customer call into a searchable product signal, "
    "so your team can fix what matters first."
)

instructions = (
    "Speak as a warm, credible product-launch narrator. "
    "Confident but not hypey. Medium pace. "
    "Pronounce Aster as ASS-ter. "
    "Do not imitate any real person."
)

out = Path("artifacts/audio/aster-lane-launch-v001.wav")
out.parent.mkdir(parents=True, exist_ok=True)

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="marin",
    input=script,
    instructions=instructions,
    response_format="wav",
    speed=1.0,
) as response:
    response.stream_to_file(out)
```

Why it is structured this way:

- WAV is used because this is a production master.
- Pronunciation is specified explicitly.
- The performance direction is concise and avoids celebrity imitation.
- The file path encodes versioning rather than overwriting a prior take.

Review criteria:

- Correct pronunciation of “Aster”.
- Natural emphasis on “searchable product signal”.
- No ad-read exaggeration.
- No clipped start/end.
- Delivery has a clear AI-generated-voice disclosure plan.
- Loudness and silence handled in post, not assumed from raw model output.

## Speech-to-text production

### Choose the transcription model by downstream use

Documented facts:

- `/v1/audio/transcriptions` accepts audio file objects in formats listed by the API reference, including common compressed and uncompressed audio formats. Source: https://developers.openai.com/api/reference/resources/audio/subresources/transcriptions/methods/create
- The typed API reference says `gpt-4o-transcribe` and `gpt-4o-mini-transcribe` support only `json`, while the current speech-to-text guide says `json` or plain `text` and includes `text` examples. Treat this first-party mismatch as volatile: use `json` for portable production code unless a current account test confirms `text`. `gpt-4o-transcribe-diarize` supports `json`, `text`, and `diarized_json`, with `diarized_json` required for speaker annotations. Sources: https://developers.openai.com/api/reference/resources/audio/subresources/transcriptions/methods/create and https://developers.openai.com/api/docs/guides/speech-to-text
- `whisper-1` supports timestamp granularities with `response_format="verbose_json"`; OpenAI’s guide says `timestamp_granularities[]` is only supported for `whisper-1`. Sources: https://developers.openai.com/api/docs/guides/speech-to-text and https://developers.openai.com/api/reference/resources/audio/subresources/transcriptions/methods/create

Production heuristics:

- For edit logs, legal-ish review, or named-entity-heavy interviews, prefer the higher-accuracy model and add a vocabulary prompt.
- For rough-cut triage across many hours, use the cheaper model, then re-transcribe selected segments with the more accurate model if needed.
- For captions, decide first whether you need word timing, segment timing, speaker labels, or only plain text. The required output shape may determine the model.
- For low-confidence or noisy segments, extract a clean WAV segment and retry with a vocabulary prompt rather than repeatedly sending the entire long file. Because the diarization model does not accept `prompt`, use a prompt-capable transcription model for the isolated repair and reconcile its text with the diarized timeline manually.

### Transcription prompts

Use `prompt` to guide style, spelling, jargon, or continuation from previous segments. The prompt should match the audio language for transcription. Do not use the prompt to invent content or “fix” unclear audio; mark inaudible spans in post-review when necessary.

Good prompt contents:

- names and product terms;
- speaker names if known;
- domain vocabulary;
- expected acronyms;
- casing preferences;
- prior segment tail for continuity;
- language variety when relevant.

Example:

```text
This is an English product interview about Aster Lane, SOC 2, Snowflake, Zendesk, and call summarization. Preserve product names. Use "Aster Lane" not "Asterlane". Use "SOC 2" not "sock two" in the transcript.
```

### Complete example: diarized meeting transcript

User intent: transcribe a 35-minute customer interview and preserve speaker turns for a researcher.

Model and endpoint: `/v1/audio/transcriptions`, `gpt-4o-transcribe-diarize`, `diarized_json`.

Python example:

```python
from pathlib import Path
from openai import OpenAI

client = OpenAI()

audio_path = Path("raw/customer-interview-2026-07-10.m4a")  # Prevalidated at <25 MB.

with audio_path.open("rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-transcribe-diarize",
        file=audio_file,
        response_format="diarized_json",
        chunking_strategy="auto",
    )

Path("artifacts/transcripts/customer-interview-diarized-v001.json").write_text(
    transcript.model_dump_json(indent=2),
    encoding="utf-8",
)
```

Expected result:

- diarized JSON with speaker-labeled segments;
- enough structure for qualitative coding;
- no word-level caption timing unless separately produced.

Likely failure modes:

- overlapping speakers may be mislabeled;
- a recurring product name may still be misspelled;
- diarization should not be treated as legal identity verification.

Repair:

- manually map speaker labels to real names after review;
- transcribe unclear spans separately with a prompt-capable model and a corrected vocabulary list, then reconcile them with the diarized timeline;
- keep the raw transcript and reviewed transcript as separate artifacts.

### Complete example: caption timing with word timestamps

User intent: create caption timing for a short tutorial clip where word-level karaoke highlighting is required.

Model and endpoint: `/v1/audio/transcriptions`, `whisper-1`, `verbose_json`, `timestamp_granularities=["word"]`.

Python example:

```python
from pathlib import Path
from openai import OpenAI

client = OpenAI()

with open("exports/tutorial-voice.wav", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["word"],
        prompt=(
            "Tutorial narration about Aster Lane, SOC 2, and Zendesk. "
            "Use product capitalization exactly."
        ),
    )

Path("artifacts/captions/tutorial-word-timestamps-v001.json").write_text(
    transcription.model_dump_json(indent=2),
    encoding="utf-8",
)
```

Why this route:

- The documented timestamp granularities route is tied to `whisper-1`.
- Word timestamps add latency, so request them only when the edit actually needs word-level timing.
- The transcript still needs a human or automated caption QA pass for line breaks, reading speed, and accessibility.

## Translation to English

The audio translations endpoint translates audio into English text. Do not present it as multilingual dubbing, voice conversion, or localized audio production.

Use it when:

- the user has non-English speech and wants an English transcript;
- the downstream edit, research, or subtitle workflow is English-first;
- the user accepts loss of original-language phrasing and speaker performance nuance.

Do not use it when:

- the deliverable needs subtitles in the original language;
- the target language is not English;
- the user wants synthetic dubbed speech in another language;
- speaker identity or exact legal wording matters without human review.

Complete example:

```python
from pathlib import Path
from openai import OpenAI

client = OpenAI()

with open("raw/founder-clip-es.m4a", "rb") as audio_file:
    translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",
        prompt=(
            "The speaker discusses Aster Lane, customer support analytics, "
            "and SOC 2. Translate to clear English while preserving product names."
        ),
    )

Path("artifacts/transcripts/founder-clip-english-v001.txt").write_text(
    translation,
    encoding="utf-8",
)
```

Approval rule: if the translation will be published, require bilingual review or explicit user acceptance that the machine translation may miss nuance.

## Audio-capable chat completions

Use Chat Completions with an audio-capable model when audio is part of a conversational model turn, not merely a file conversion job. Documented pattern: use `gpt-audio-1.5`, set `modalities` to include `audio`, provide `audio` output parameters, and include audio inputs as base64 `input_audio` content blocks. Source: https://developers.openai.com/api/docs/guides/audio

Use this route for:

- “listen to this short recording and answer out loud”;
- voice-enabled chat in an existing Chat Completions app;
- an agent that reasons about spoken content and returns both text and audio in one bounded turn.

Do not use this route for:

- bulk transcription, where `/v1/audio/transcriptions` is simpler;
- pure narration from a finished script, where `/v1/audio/speech` is simpler;
- continuous microphone interaction, where realtime sessions fit better.

Complete example:

```python
import base64
from pathlib import Path
from openai import OpenAI

client = OpenAI()

audio_bytes = Path("raw/user-question.wav").read_bytes()
encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

completion = client.chat.completions.create(
    model="gpt-audio-1.5",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {
            "role": "system",
            "content": (
                "Answer as a concise support coach. If the recording is unclear, "
                "say what you could not determine rather than guessing."
            ),
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is the customer asking for?"},
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": encoded_audio,
                        "format": "wav",
                    },
                },
            ],
        },
    ],
)

message = completion.choices[0].message
Path("artifacts/chat-audio/answer-transcript-v001.txt").write_text(
    message.audio.transcript,
    encoding="utf-8",
)
Path("artifacts/chat-audio/answer-v001.wav").write_bytes(
    base64.b64decode(message.audio.data)
)
```

Custody note: chat audio responses include base64 audio bytes and a transcript. Store both if the output is an approved production artifact. If privacy policy requires no server-side persistence, verify `store` behavior and the organization’s data controls before use.

## Latency, cost, and batching

Documented cost facts are volatile; always re-check pricing on the day of production. On 2026-07-10, OpenAI’s pricing page lists:

- realtime/audio-generation model prices by audio/text/image token or minute depending on model;
- transcription model prices for `gpt-4o-transcribe` and `gpt-4o-mini-transcribe`, including estimated per-minute rates;
- no separate platform fee for Responses, Chat Completions, Realtime, Batch, or Assistants APIs beyond model/tool billing. Source: https://developers.openai.com/api/docs/pricing

Production heuristics:

- Estimate TTS cost from generated text and audio-token billing when using audio-generation models; estimate transcription cost from audio duration and the current pricing page.
- For transcription, run low-cost first-pass transcription only when errors will be caught later; do not use rough transcripts as final legal, medical, compliance, or public quote artifacts.
- For long TTS scripts, generate auditions first, then batch full narration only after voice approval.
- For long transcription files, split only on natural pauses or scene boundaries if you need parallelism or retry isolation. Keep overlap small and reconcile duplicates in post.
- Streaming is useful for UX latency; it does not remove the need to store final artifacts and review output before publication.

## Rights, consent, privacy, and safety

Hard requirements:

- Do not generate, transform, or imitate a person’s voice in a way that could confuse authenticity unless the user has consent and rights. OpenAI policy specifically flags use of someone’s likeness, including voice, without consent in confusing contexts. Source: https://openai.com/policies/usage-policies/
- Do not present a synthetic voice as a real person’s live or recorded speech.
- Do not process private calls, interviews, meetings, or voicemails unless the user has lawful authority and any required participant consent.
- Clearly disclose to end users that OpenAI TTS audio is AI-generated and not a human voice; also satisfy any additional legal, platform, or client disclosure requirements.
- For minors, healthcare, legal, workplace surveillance, biometric, or sensitive personal data, pause for a privacy and policy review before processing.
- Treat diarization as a production convenience, not identity proof.
- Treat transcripts as potentially sensitive records. Store raw audio and transcripts only in approved locations.

Data-control facts verified 2026-07-10:

- OpenAI’s platform data-controls table says API data is not used for training across listed endpoints.
- The table lists `/v1/audio/transcriptions` and `/v1/audio/translations` with no abuse-monitoring retention and no application-state retention.
- The table lists `/v1/audio/speech` with 30-day abuse-monitoring retention and no application-state retention.
- Audio outputs in Chat Completions and Responses may have application state stored for 1 hour to enable multi-turn conversations.
- Zero Data Retention and Modified Abuse Monitoring require approval and have endpoint-specific limitations. Source: https://developers.openai.com/api/docs/guides/your-data

## Approval and artifact custody protocol

Use this protocol for any production asset, public-facing content, customer content, regulated transcript, or paid batch job.

Before generation or transcription:

1. Name the endpoint, model, output format, and reason for the route.
2. Confirm rights/consent for voices, recordings, scripts, brands, and music beds.
3. Confirm privacy classification and storage location.
4. Confirm cost estimate source and date if cost is material.
5. Confirm whether the first call is an audition/sample or full batch.

After a sample:

1. Store raw output under a versioned path.
2. Produce a short review note: model, voice, prompt/instructions, input file/script, format, reviewer, date, pass/fail.
3. Ask for approval or revision before generating the full batch.

After a full batch:

1. Store raw inputs, generated outputs, transcripts, sidecars, manifests, and approvals separately.
2. Preserve original model outputs before post-processing.
3. Write a manifest that records model, endpoint, parameters, source files, output files, checksums, and approval status.
4. Mark derivative files clearly: edited, normalized, mixed, captioned, translated, or reviewed.
5. Do not delete raw source or approved masters unless the user’s retention policy requires deletion and the deletion is logged.

Minimal artifact manifest shape:

```json
{
  "artifact_id": "narration_sc01_v003",
  "created_at": "2026-07-10T18:30:00Z",
  "provider": "openai",
  "endpoint": "/v1/audio/speech",
  "model": "gpt-4o-mini-tts",
  "voice": "marin",
  "input_script": "scripts/narration/sc01_v004.txt",
  "instructions": "Warm, credible, medium pace; pronounce Aster as ASS-ter.",
  "parameters": {
    "response_format": "wav",
    "speed": 1.0
  },
  "outputs": [
    {
      "path": "artifacts/audio/sc01_v003.wav",
      "role": "raw_model_master",
      "sha256": "..."
    }
  ],
  "approval": {
    "status": "approved",
    "approver": "user",
    "approved_at": "2026-07-10T18:45:00Z"
  },
  "source_verification": {
    "docs_checked_at": "2026-07-10",
    "pricing_checked_at": "2026-07-10"
  }
}
```

## Quality review

For generated speech, review:

- pronunciation of names, acronyms, numbers, currencies, and URLs;
- pacing, pauses, and breath realism;
- emotion relative to the brief;
- consistency across chunks;
- clipping, dropouts, artifacts, noise, or abrupt endings;
- compliance with consent/disclosure requirements;
- loudness and peak headroom after post-processing.

For transcripts, review:

- speaker labels and turn boundaries;
- named entities and technical terms;
- timestamps against the actual waveform;
- omissions during crosstalk, music, applause, or noise;
- hallucinated text in inaudible sections;
- punctuation and casing;
- privacy redaction requirements.

For translated transcripts, review:

- whether the output is English-only as expected;
- product names preserved;
- idioms and jokes not over-literalized;
- quotes not published without bilingual review;
- culturally sensitive or legal wording escalated for human review.

## Common failure modes and repairs

| Failure | Likely cause | Repair |
|---|---|---|
| TTS mispronounces a product name | Name not phonetically constrained | Add pronunciation in `instructions` and/or script; regenerate only affected lines. |
| TTS sounds like an ad read | Direction too broad: “excited”, “professional” | Specify audience, emotional arc, pace, and what to avoid. |
| TTS chunks do not match | Direction changed between chunks or script boundaries were unnatural | Lock one instruction block and chunk at scene/paragraph boundaries. |
| Output format wrong for edit | Delivery format chosen too early | Generate WAV/FLAC master; transcode copies downstream. |
| Transcript misses proper nouns | No vocabulary prompt or poor audio | Add vocabulary prompt; retry clean segments; manually QA final. |
| Timestamps unavailable | Wrong model/response format | Use documented timestamp route: `whisper-1`, `verbose_json`, requested granularities. |
| Streaming request ignored | `whisper-1` used | Use a GPT transcription model for streaming, or accept non-streaming Whisper behavior. |
| Translation requested to non-English target | Endpoint mismatch | Use translation endpoint only for English text, or route to a localization/dubbing workflow outside this skill. |
| Speaker labels treated as identity | Misuse of diarization | Human-review speaker mapping; never use diarization as biometric ID. |
| Privacy blocker | Sensitive source audio or unclear consent | Pause, confirm lawful basis, storage, retention, and disclosure requirements. |

## Final response pattern for production work

When handing off results, include:

- endpoint and model used;
- input source and output artifact paths;
- parameters that materially affected output;
- approval status;
- QA findings and unresolved risks;
- any required human review before publication;
- source dates for volatile pricing/model/retention claims.
