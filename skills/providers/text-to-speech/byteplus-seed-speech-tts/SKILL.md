---
name: byteplus-seed-speech-tts
description: Production guidance for international BytePlus Seed Speech text-to-speech. Use for selecting TTS 1.0 versus 2.0, bidirectional or unidirectional streaming, current voices and languages, prompt/prosody controls, subtitle timing validation, billing and concurrency, authorized replicated voices, privacy, error handling, and output QA. Do not use for mainland-China Volcengine Doubao Speech endpoints.
---

# BytePlus Seed Speech TTS

Use this skill for the international BytePlus Seed Speech service. The current documented API host is in the `ap-southeast-1.bytepluses.com` domain. Do not transfer credentials, endpoints, prices, voice IDs, or commercial assumptions from mainland-China Volcengine Doubao Speech.

## Verification and evidence

- **Documented fact:** behavior stated in official BytePlus documentation or its applicable legal pages.
- **Production heuristic:** a practical workflow that must be tested with the selected account, voice, and protocol.
- **Empirical observation:** output measured from an actual dated request.

Provider facts were verified **2026-07-12**. Voice inventory, language compatibility, pricing, free quota, concurrency, endpoints, retention, and protocol behavior are volatile. Re-check the official voice list, API page, console, pricing, order form, and DPA immediately before production.

## Boundary and taxonomy

BytePlus calls the international product **Seed Speech**. Current synthesis resource families include:

- `seed-tts-1.0`: TTS 1.0;
- `seed-tts-2.0`: TTS 2.0;
- `seed-icl-1.0`: authorized Voice Replication 1.0 synthesis;
- `seed-icl-2.0`: authorized Voice Replication 2.0 synthesis.

Seed-TTS research papers describe model research and are not API contracts. Do not expose research variants as hosted model IDs.

This leaf covers prebuilt TTS and synthesis with a voice already enrolled and authorized. Voice enrollment itself requires a separate consent, data, and lifecycle review. It does not cover ASR, speech-to-speech agents, interpretation, podcasts, or mainland Volcengine APIs.

## Select model family and protocol

### TTS 1.0

Use when a chosen voice or required feature is documented for TTS 1.0, especially where the selected protocol documents timestamp or voice-specific emotion support. Do not assume TTS 1.0 and 2.0 voices share identifiers or controls.

### TTS 2.0

BytePlus documents broader multilingual and contextual/instruction control. `context_texts` can give natural-language performance direction; only the first list value is documented as effective. `section_id` can connect prior synthesis context, with current documentation describing up to 30 rounds or ten minutes.

TTS 2.0 does not support SSML in the documented V3 bidirectional or unidirectional paths. Never send SSML as though it were a supported control.

### Bidirectional WebSocket

Use when text arrives incrementally and audio must stream while preserving session context:

```text
wss://voice.ap-southeast-1.bytepluses.com/api/v3/tts/bidirection
```

Lifecycle: establish WebSocket, `StartConnection`, wait for `ConnectionStarted`, `StartSession`, wait for `SessionStarted`, send one or more `TaskRequest` events, consume sentence/audio events, `FinishSession`, wait for `SessionFinished`, then close. Event codes currently include sentence start `350`, sentence end `351`, and TTS response `352`.

### Unidirectional HTTP streaming

Use when the complete text is known and audio should stream back over HTTP:

```text
POST https://voice.ap-southeast-1.bytepluses.com/api/v3/tts/unidirectional
```

Read newline/streamed JSON responses, base64-decode each audio payload, and concatenate in arrival order. Finish on provider success code `20000000`.

No public BytePlus async long-text workflow was established during verification. Do not redirect international jobs to Volcengine async endpoints.

## Authentication and headers

New integrations use a console-generated `X-Api-Key`. The selected resource ID is mandatory. Current HTTP documentation also requires the fixed `X-Api-App-Key` shown by the provider; verify it from the current page rather than assuming it is a secret or reusing a stale value.

Example header shape:

```http
X-Api-Key: ${BYTEPLUS_API_KEY}
X-Api-Resource-Id: seed-tts-2.0
X-Api-App-Key: <current documented fixed value>
X-Api-Request-Id: <uuid>
Content-Type: application/json
```

The WebSocket path uses an `X-Api-Connect-Id` for troubleshooting. Preserve the returned `X-Tt-Logid` and client request/connection ID. Never log credentials or sensitive source text.

Legacy App ID/access-key headers remain documented for compatibility, with legacy resource IDs. Do not mix a new API key with guessed legacy fields or copy Volcengine auth.

## Voice and language selection

Treat support as a tuple:

```text
voice ID + resource family + protocol + language + control
```

Load the official voice list at execution time. Verify that the account is entitled to the voice and that the chosen voice supports the target language, protocol, emotion, timestamps, and other requested controls. Do not invent IDs or infer capability from an ID suffix.

The TTS 2.0 overview currently lists English, Chinese, Japanese, German, French, Mexican Spanish, Indonesian, Brazilian Portuguese, Italian, and Korean. Protocol/voice pages may expose additional voice-specific language codes. The selected voice page is authoritative for a production call.

## Request controls

Current V3 request fields include text, speaker, audio format/sample rate, speech rate, loudness, voice-specific emotion, and an escaped JSON `additions` string.

Documented ranges include:

- `speech_rate`: -50 to 100, where -50 represents 0.5x and 100 represents 2x;
- `loudness_rate`: -50 to 100;
- `emotion_scale`: 1 to 5 for voices supporting emotion, with non-linear perceived change;
- formats: `mp3`, `ogg_opus`, and `pcm`;
- sample-rate values listed by the current protocol page from 8 kHz through 48 kHz.

Streaming WAV can produce repeated headers; prefer PCM when an unframed stream is needed, or use MP3/Opus with verified concatenation/decoding.

`additions` controls include language policy, Markdown/emoji handling, end silence, formula normalization, TTS 2.0 context, and optional cache behavior. Cache hits are documented as not returning timestamps.

Normalize numbers, dates, currencies, abbreviations, URLs, formulas, Markdown, emoji, and punctuation before estimating cost and synthesis. Save the exact normalized source used for the request.

## Timestamps and subtitles

Current V3 parameter tables say `enable_timestamp` works only for TTS 1.0 and ICL 1.0. Cache responses omit timestamps. Treat any timing observed from another model/protocol combination as an empirical account-level result, not a documented capability.

Therefore:

- never promise TTS 2.0 timing without a dated integration test of the exact voice/protocol;
- verify timestamps are monotonic, bounded by decoded duration, and aligned after text normalization;
- human-review names, numbers, punctuation, and line grouping;
- retain a fallback transcription/alignment workflow;
- do not construct captions from estimated character duration.

## Billing and capacity

Official public pricing checked 2026-07-12 lists TTS 2.0 packages and pay-as-you-go character billing, a 20,000-character activation trial, and separately purchased concurrency. It defines spaces, punctuation, symbols, and carriage returns as billable characters.

Because prices, packages, and terminology can change, create a dated cost record from the current pricing page/console. Count normalized request text using the provider's current billing rule. Confirm whether the account limit is expressed as concurrency or QPS and test queue behavior before batch production.

Do not state that a plan or trial is guaranteed outside the applicable account and date.

## Privacy, consent, and replicated voices

The applicable BytePlus agreement and DPA govern processing. The customer is responsible for notices, lawful basis/consent, and authorized instructions. BytePlus's current enterprise AI FAQ qualifies training claims: do not simplify it to “data is never used for training” without the corporate-customer and express-authorization context.

For any replicated voice:

- obtain explicit, purpose-specific authority from the speaker/rights holder;
- record permitted use, audience, territory, term, revocation, and deletion procedure;
- verify account, voice ID, and language are authorized;
- avoid public-figure or deceptive impersonation;
- minimize enrollment/source audio and restrict access;
- resolve retention, residency, deletion, and model-improvement terms in the current contract/order form.

A successful enrollment or voiceprint check is not legal consent.

## Error handling

Handle provider/application codes and preserve `X-Tt-Logid`.

- Invalid text, parameters, unsupported controls, or unauthorized voice: repair; do not retry unchanged.
- Concurrency/quota: queue, back off with jitter, or adjust purchased capacity.
- General server/network failures: bounded retry when idempotency/charge behavior is understood.
- Ambiguous partial stream: reject incomplete audio unless the workflow explicitly supports resume/reassembly.

Do not print the API key, legacy token, sensitive text, or full response bodies containing customer data.

## Production QA

Before a full batch, generate short samples and approve voice, language, pronunciation, rate, emotion, and context behavior.

Check:

- decoded codec, sample rate, channel count, duration, and corruption;
- missing/repeated/truncated words and stream ordering;
- names, acronyms, numbers, currencies, formulas, and multilingual switching;
- clipping, true peak, loudness consistency, noise, clicks, sibilance, and silence;
- performance direction and voice identity;
- back-transcription against normalized text;
- timestamp/caption alignment where used;
- request/resource/voice/log IDs, source revision, consent record, price evidence, and output hash.

Provider output can vary across calls. Do not promise bit-identical speech from the same request unless measured and contractually supported.

## Example 1: TTS 2.0 HTTP narration

This is a complete example, not a mandatory formula.

**Intent:** low-latency Chinese product narration with calm performance direction.

Preflight the current voice list and choose an authorized TTS 2.0 Chinese voice. Use `seed-tts-2.0`, MP3 at 24 kHz, exact normalized script, and one `context_texts` instruction: “Speak naturally, calmly, and warmly; avoid exaggeration.” Submit to the unidirectional HTTP endpoint, consume every audio chunk in order, and stop on `20000000`.

The payload shape is:

```json
{
  "user": {"id": "production-job-2841"},
  "req_params": {
    "text": "欢迎回来。项目已经准备就绪，我们现在可以开始。",
    "speaker": "<authorized-current-voice-id>",
    "audio_params": {
      "format": "mp3",
      "sample_rate": 24000,
      "speech_rate": 0,
      "loudness_rate": 0
    },
    "additions": "{\"explicit_language\":\"zh-cn\",\"disable_markdown_filter\":true,\"context_texts\":[\"请用自然、沉稳、亲切的语气表达，不要夸张。\"]}"
  }
}
```

QA decoded audio, duration, script completeness, pronunciation, performance, and log ID. Do not request timestamps unless this exact voice/protocol has passed a dated test.

## Example 2: incremental assistant response

This is a complete example, not a mandatory formula.

**Intent:** stream an authorized English assistant voice while response text arrives incrementally.

Use the bidirectional WebSocket lifecycle. Start connection/session with an authorized voice/resource pair, send complete semantic chunks as `TaskRequest` events, consume sentence/audio events, and finish only after the final chunk. Keep one performance instruction and context policy across the session. Buffer enough text to avoid unnatural fragments without delaying the first useful audio excessively.

QA chunk boundaries, missing/repeated text, ordering, cancellation, reconnection, rate limits, and final transcript/audio parity. If the selected voice does not support bidirectional operation, switch protocol or voice after explicit approval; do not silently substitute.

## Sources

Official sources verified 2026-07-12:

- BytePlus Seed Speech and TTS 2.0/1.0: https://www.byteplus.com/en/product/voice , https://docs.byteplus.com/en/docs/byteplusvoice/texttospeechv2 , and https://docs.byteplus.com/en/docs/byteplusvoice/texttospeechv_1
- Bidirectional WebSocket and unidirectional HTTP: https://docs.byteplus.com/en/docs/byteplusvoice/streaming_tts and https://docs.byteplus.com/en/docs/byteplusvoice/unidirectional_tts_http
- Current voice list and console guide: https://docs.byteplus.com/en/docs/byteplusvoice/voicelist and https://docs.byteplus.com/en/docs/byteplusvoice/Speech_Console_Guide
- Billing: https://docs.byteplus.com/en/docs/byteplusvoice/TTS_Billing
- Voice replication documentation and billing: https://docs.byteplus.com/en/docs/byteplusvoice/voicereplication-v3-voice-training and https://docs.byteplus.com/en/docs/byteplusvoice/voicereplicationbilling
- DPA, Privacy Policy, Acceptable Use Policy, and AI Models FAQ: https://docs.byteplus.com/en/docs/legal/docs-data-processing-addendum , https://docs.byteplus.com/en/legal/docs/privacy-policy , https://docs.byteplus.com/en/docs/legal/docs-acceptable-use-policy , and https://docs.byteplus.com/en/docs/legal/AI_Models_FAQ
- Seed-TTS technical report (research context only): https://arxiv.org/abs/2406.02430