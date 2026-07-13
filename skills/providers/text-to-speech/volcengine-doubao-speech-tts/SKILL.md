---
name: volcengine-doubao-speech-tts
description: Production guidance for mainland-China Volcengine Doubao Speech text-to-speech. Use for TTS 1.0/2.0 selection, V3 bidirectional or unidirectional streaming, asynchronous long-text submit/query jobs, current voices and controls, timestamps and SSML caveats, expiring results, quota/error handling, authorized cloned voices, privacy, and audio QA. Do not use for international BytePlus endpoints.
---

# Volcengine Doubao Speech TTS

Use this skill for mainland-China Volcengine Doubao Speech. Do not transfer BytePlus API hosts, keys, pricing, legal terms, or assumptions into this workflow. The services share model-family language but are separate regional products.

## Verification and evidence

- **Documented fact:** behavior stated by official Volcengine pages.
- **Production heuristic:** a workflow recommendation requiring target-account testing.
- **Empirical observation:** a result from a dated request in the actual account/region.

Facts were verified **2026-07-12**. Voice lists, protocol compatibility, pricing, activation, quotas, retention, regional availability, and legal terms are volatile. Re-check the Chinese official docs and authenticated console.

## Product and API boundary

Current synthesis resource families include:

- `seed-tts-1.0`: TTS 1.0 on V3;
- `seed-tts-2.0`: TTS 2.0 on V3;
- `seed-icl-1.0`: authorized cloned-voice 1.0 synthesis;
- `seed-icl-2.0`: authorized cloned-voice 2.0 synthesis.

Legacy `volc.service_type.10029` and the V1 API belong to older TTS 1.0 contracts. Do not call a TTS 2.0 voice through V1 or substitute legacy model selectors for a V3 resource ID.

This leaf covers synthesis and long-text production. Voice enrollment is included only as a consent/authorization boundary; ASR, speech agents, interpretation, podcasts, speech-to-speech, and international BytePlus are out of scope.

## Choose a protocol

### V3 bidirectional WebSocket

Use when text arrives incrementally:

```text
wss://openspeech.bytedance.com/api/v3/tts/bidirection
```

Follow the documented connection/session/task lifecycle. Not every voice supports every protocol; verify the current voice list and account entitlement before locking bidirectional delivery.

### V3 unidirectional streaming

Use when the complete text is known but audio should stream. Official Volcengine documentation includes V3 WebSocket, HTTP chunked, and SSE surfaces. Select the exact documented endpoint and response parser at implementation time; do not assume transport schemas are interchangeable.

### Asynchronous long text

Use for batch narration/audiobooks and inputs within the current documented limit:

```text
POST https://openspeech.bytedance.com/api/v3/tts/submit
POST https://openspeech.bytedance.com/api/v3/tts/query
```

Current docs state a maximum of 100,000 characters. Submit returns a `task_id`; query statuses are `1` running, `2` success, and `3` failure. On success, download immediately. Server audio is documented as retained seven days; each returned URL is valid for one hour and can be refreshed by querying again.

Submit and query consume the purchased concurrency pool. Use bounded polling with jitter and persist the provider task ID.

## Authentication

Volcengine V3 streaming and async pages use different documented header combinations. Follow the exact selected page.

Current V3 new-console integrations use `X-Api-Key` on relevant streaming surfaces. The async long-text API documents:

```http
X-Api-App-Id: ${VOLC_APP_ID}
X-Api-Access-Key: ${VOLC_ACCESS_KEY}
X-Api-Resource-Id: seed-tts-2.0
X-Api-Request-Id: <uuid>
```

Legacy V1 uses the unusual `Authorization: Bearer;${token}` form. Do not copy that to V3 without current documentation.

Preserve request IDs and `X-Tt-Logid` where returned. Never log secrets, tokens, enrollment audio, or sensitive source text.

## Voice, language, and control compatibility

Treat support as:

```text
speaker + resource ID + protocol + language + control + account entitlement
```

Load the current official voice list. Do not freeze counts, infer support from a suffix, or invent an ID. Some multilingual/current voices may be limited to unidirectional operation.

Documented controls include voice-specific emotion, non-linear `emotion_scale` 1-5, `speech_rate` -50 to 100, `loudness_rate` -50 to 100, sample rate/format, end silence, language filtering, Markdown/emoji/formula handling, and optional AIGC watermark settings.

TTS 2.0 uses contextual/instruction controls and does not support SSML on the documented V3 paths. SSML support belongs to compatible TTS 1.0 paths only; verify exact tags and limits before use.

Mixing voices or carrying controls across versions is not universal. The current voice/protocol page is authoritative.

## Timestamps and text normalization

Timestamp documentation varies by version/protocol. Volcengine async results can return sentence/word timing structures, but TTS 2.0/ICL 2.0 support and normalization behavior must be tested with the exact voice.

- Normalize text before submission and billing.
- Record pre- and post-normalized forms.
- Validate timestamp monotonicity, duration bounds, numbers, punctuation, and rewritten text.
- Group Chinese captions by semantic phrase, not fixed character count.
- Keep an alignment fallback when timing is absent or inaccurate.
- Do not use cached/estimated character timing as caption truth.

## Async idempotency and result custody

Set a stable caller-side `unique_id` and save it with `task_id`, source hash, normalized text, resource/speaker, and attempt number.

After an ambiguous timeout, query known task state before resubmitting. Blind resubmission can duplicate work or charges. On success, download before URL expiry, compute a checksum, verify decoding/duration, and move the asset into controlled storage. Result URLs are not durable delivery locations.

## Pricing, activation, and quota

Public RMB price amounts could not be confirmed from the unauthenticated documentation available during verification; the authenticated console and order terms are authoritative. Async long text is documented as using the corresponding short-text TTS/voice-replication pricing rather than a separate premium.

Before paid use, record:

- account/region and activated resource;
- character or concurrency package;
- current unit price and validity;
- free/trial amount if actually granted;
- voice-specific fee/entitlement;
- expected normalized characters and attempts;
- purchased concurrency and queue policy.

Do not promise a public free tier, region set, or fixed rate without current account evidence.

## Privacy, consent, and cloned voices

Voice and associated identity can be sensitive personal data. Public product docs do not replace the applicable contract, privacy terms, and legal review.

For cloned voices:

- require explicit, recorded, purpose-specific authority;
- document source speaker, permitted use, term, territory, distribution, revocation, and deletion;
- restrict enrollment audio and model identifiers;
- verify current training-audio/model retention and deletion through account/contract/support;
- avoid deceptive impersonation, public figures, minors, and unauthorized cross-language use;
- record disclosure/watermark requirements.

No technical enrollment or similarity check proves legal authorization. Do not claim unverified residency, retention, training exclusion, or regulatory compliance.

## Errors and retries

Current APIs use success code `20000000`; preserve detailed provider code/message/log ID.

- Invalid parameter/text/resource/speaker or unsupported protocol: repair; no unchanged retry.
- Speaker permission/resource mismatch: verify activation and matching version.
- Quota/concurrency: queue/back off or purchase capacity.
- Duplicate request/ID: query existing job or generate the appropriate new ID.
- General backend/network errors: bounded retry with idempotency safeguards.
- Async status `3`: surface failure details; do not conceal or endlessly poll.

## Production QA

Create a pronunciation set for names, brands, acronyms, numbers, dates, currencies, formulas, dialect, and domain terms. Generate approval samples before long jobs.

Verify:

- codec, sample rate, channels, duration, checksum, and file integrity;
- missing/repeated/truncated text;
- voice identity, language/dialect, rate, emotion, and pronunciation;
- clipping, peaks, loudness consistency, noise, silence, clicks, and sibilance;
- back-transcription against normalized source;
- timestamp/caption alignment;
- task/request/resource/speaker/log IDs, price evidence, consent, source revision, and output provenance.

## Example 1: async audiobook chapter

This is a complete example, not a mandatory formula.

**Intent:** synthesize a mainland-China audiobook chapter with an authorized TTS 2.0 voice.

Preflight current voice compatibility, normalize the chapter, hash it, calculate current billed characters, and secure price/concurrency approval. Submit with async-required headers, stable `unique_id`, `namespace: "BidirectionalTTS"`, `seed-tts-2.0`, MP3 24 kHz, and the exact authorized current speaker ID.

```json
{
  "user": {"uid": "audiobook-pipeline"},
  "unique_id": "chapter-0047-v3-9b2f8c4a",
  "namespace": "BidirectionalTTS",
  "req_params": {
    "text": "<normalized-chapter-text>",
    "speaker": "<authorized-current-voice-id>",
    "audio_params": {
      "format": "mp3",
      "sample_rate": 24000,
      "speech_rate": 0,
      "loudness_rate": 0,
      "enable_timestamp": true
    },
    "additions": "{\"disable_markdown_filter\":true,\"explicit_language\":\"zh-cn\"}"
  }
}
```

Poll by `task_id`; on status 2, download immediately, store timing payload, checksum, decoded duration, and URL expiry. Human-review chapter and captions. If this exact TTS 2.0 voice does not return usable timing, align separately.

## Example 2: bidirectional assistant

This is a complete example, not a mandatory formula.

**Intent:** stream Mandarin assistant speech as text arrives.

Select a current voice explicitly documented for bidirectional V3 and the matching resource. Use PCM or a tested streaming codec, stable connection/session IDs, and a bounded semantic text-buffer policy. Follow StartConnection/StartSession/TaskRequest/FinishSession events and cancel cleanly when upstream text is abandoned.

QA first-audio behavior, chunk ordering, sentence boundaries, reconnect/cancel, missing/repeated text, entitlement, concurrency, and final transcript parity. If the desired voice is unidirectional-only, request user approval for a voice or protocol change.

## Sources

Official sources verified 2026-07-12:

- Volcengine Doubao Speech overview/model/voice list: https://docs.volcengine.com/docs/6561/163032?lang=zh , https://docs.volcengine.com/docs/6561/2499930?lang=zh , and https://docs.volcengine.com/docs/6561/1257544?lang=zh
- V3 bidirectional and unidirectional WebSocket: https://docs.volcengine.com/docs/6561/2532486?lang=zh and https://docs.volcengine.com/docs/6561/2534913?lang=zh
- Async long-text submit/query: https://docs.volcengine.com/docs/6561/1829010?lang=zh
- Legacy V1 TTS: https://docs.volcengine.com/docs/6561/1257584?lang=zh
- Voice training and replication practice: https://docs.volcengine.com/docs/6561/2534906?lang=zh and https://docs.volcengine.com/docs/6561/1204182?lang=zh
- Seed-TTS report (research context only): https://arxiv.org/abs/2406.02430