---
name: nvidia-speech-nim
description: Use NVIDIA Speech NIM microservices for speech production and voice workflows, including self-hosted ASR/STT, TTS, text translation, speech-to-speech pipeline design, Riva Python client integration, deployment planning, GPU/runtime sizing, licensing/privacy review, and production QA for transcription, captioning, voice agents, localization, and synthetic voice output.
---

# NVIDIA Speech NIM

Use this skill when an agent must plan or implement a speech workflow with NVIDIA Speech NIM microservices rather than a generic speech API. Treat NVIDIA Speech NIM as a deployable containerized speech stack: the application talks to independent ASR, TTS, and NMT NIM containers over HTTP, gRPC, or WebSocket APIs, and the agent remains responsible for model/profile choice, orchestration, rights checks, audio custody, and QA.

Facts in this skill were verified from official NVIDIA sources on 2026-07-10 unless noted otherwise.

## First classify the job

Separate the user's request into one or more speech capabilities:

- ASR/STT: audio to text for transcription, captions, subtitles, call analytics, meeting notes, voice-agent input, or speech-to-text translation where an ASR model supports translation.
- TTS: text to speech for narration, localized voice-over, conversational output, accessibility, kiosk/agent responses, or approved voice cloning.
- NMT: text translation between languages. NVIDIA's documented Speech NIM translation route is a separate NMT container, not hidden inside every ASR or TTS call.
- Speech-to-speech translation: a pipeline that chains ASR -> NMT -> TTS. Do not present it as a single monolithic Speech NIM unless the selected model/card explicitly exposes an end-to-end speech-to-speech endpoint.
- Full-duplex voice chat: a distinct Nemotron VoiceChat-style model if explicitly selected; do not assume ordinary ASR + TTS NIM provides duplex conversational behavior by itself.

If the user asks only for "speech NIM," keep ASR, TTS, and NMT together as a speech-and-voice provider decision. If the user asks for a narrow transcription or narration integration, scope to the needed container but keep the route boundaries visible.

## Documented capability map

Use these as documented facts, not preferences.

- NVIDIA Speech NIM microservices deploy ASR, TTS, and NMT models as standalone containers. The application calls the NIM APIs; it does not call the raw model directly. Source: [How NVIDIA Speech NIM Microservices Work](https://docs.nvidia.com/nim/speech/latest/about/how-it-works.html).
- ASR NIM converts speech to text and supports streaming and offline modes. Streaming returns partial transcripts as audio arrives; offline processes a complete file and returns a complete transcript. Source: [About NVIDIA ASR NIM](https://docs.nvidia.com/nim/speech/latest/asr/index.html).
- TTS NIM converts text to speech and supports offline synthesis and streaming synthesis. Offline returns a complete audio response and the gRPC path is subject to a 4 MB message-size limit; streaming returns audio chunks and is the route for lower time-to-first-audio or long text. Source: [About NVIDIA TTS NIM](https://docs.nvidia.com/nim/speech/latest/tts/index.html).
- NMT NIM translates text between languages. NVIDIA documents real-time translation as a chain of ASR NIM, NMT NIM, and TTS NIM that the application orchestrates. Source: [NVIDIA Speech NIM overview](https://docs.nvidia.com/nim/speech/latest/about/index.html) and [About NVIDIA NMT NIM](https://docs.nvidia.com/nim/speech/latest/nmt/index.html).
- ASR APIs: HTTP REST for simple offline transcription/translation, gRPC for batch and streaming recognition, and WebSocket for low-latency realtime sessions. Source: [ASR API references](https://docs.nvidia.com/nim/speech/latest/reference/api-references/asr/index.html).
- TTS APIs: HTTP REST for voice listing and offline/streaming synthesis, gRPC for batch and streaming synthesis, and WebSocket for realtime interactive synthesis. Source: [TTS API references](https://docs.nvidia.com/nim/speech/latest/reference/api-references/tts/index.html).
- ASR HTTP accepts WAV, OPUS, and FLAC for `/v1/audio/transcriptions`; either `language` or `model` is required. `/v1/audio/translations` is supported only by models with translation capability, such as Canary or Whisper in NVIDIA's REST documentation. Source: [ASR HTTP REST API](https://docs.nvidia.com/nim/speech/latest/reference/api-references/asr/http-asr.html).
- TTS HTTP `/v1/audio/synthesize` returns a WAV file; `/v1/audio/synthesize_online` streams raw 16-bit signed LPCM chunks without a WAV header. Text is limited to 2,000 normalized characters per request on the documented HTTP endpoints. Source: [TTS HTTP REST API](https://docs.nvidia.com/nim/speech/latest/reference/api-references/tts/http-tts.html).
- TTS voice names come from `/v1/audio/list_voices` and follow `Model.LOCALE.Speaker` or `Model.LOCALE.Speaker.Emotion`; emotion suffix availability varies by speaker. Source: [TTS HTTP REST API](https://docs.nvidia.com/nim/speech/latest/reference/api-references/tts/http-tts.html).
- Zero-shot voice cloning is documented for Magpie TTS Zeroshot and Magpie TTS Flow. Both require access approval; the reference prompt should be a clear 16-bit mono WAV at 22.05 kHz or higher, about 3-10 seconds. Flow requires a transcript and is offline-only; Zeroshot supports streaming and offline. Source: [Cloning a Voice with Zero-Shot TTS](https://docs.nvidia.com/nim/speech/latest/tts/voice-cloning.html).
- NIM containers expose health, version, metadata, model, and Prometheus-style metrics endpoints. Use readiness checks before sending production audio. Sources: [ASR HTTP REST API](https://docs.nvidia.com/nim/speech/latest/reference/api-references/asr/http-asr.html), [TTS HTTP REST API](https://docs.nvidia.com/nim/speech/latest/reference/api-references/tts/http-tts.html), and [Observability](https://docs.nvidia.com/nim/speech/latest/reference/observability.html).

## Model and profile selection

Select at deployment time, not after the service is already running. NVIDIA documents `CONTAINER_ID` and `NIM_TAGS_SELECTOR` as the route for choosing a container and deployment profile. Use the support matrix for the current profile names, memory requirements, inference mode, language support, WSL2 status, and model-specific notes.

### ASR selection

Prefer:

- English real-time captions, voice-agent input, and single-language call center transcription: start with a streaming English Parakeet/Nemotron ASR profile, then validate word error rate and endpointing on representative audio.
- Long prerecorded audio, media libraries, compliance review, or subtitle backfills: choose an offline or true-offline profile. NVIDIA documents true-offline Parakeet profiles that use VAD to segment long files into up-to-30-second chunks for parallel offline processing.
- Multilingual streaming input: use a multilingual streaming model/profile such as Parakeet RNNT Multilingual or Nemotron ASR Streaming `type=multi` when the documented language list covers the target language. Some profiles support automatic language detection; some require a language code for better accuracy.
- Speech-to-text translation from audio: use models documented with audio translation capability, such as Canary or Whisper via `/v1/audio/translations`; otherwise run ASR first and then NMT.
- Multiple speakers: choose a documented profile with VAD and Sortformer diarization when available. Do not promise diarization for every ASR model or profile.

Documented ASR hardware/software boundary verified 2026-07-10: ASR NIM requires NVIDIA GPU compute capability 8.0 or higher and at least 16 GB VRAM; Linux Ubuntu 22.04 or later is recommended; NVIDIA Driver >= 535 and NVIDIA Docker >= 23.0.1 are listed. WSL2 support is model-dependent and the ASR matrix lists Windows 11 Build 23H2+, driver >= 570, Ubuntu 24.04, and Podman as recommended for WSL2. Source: [ASR support matrix](https://docs.nvidia.com/nim/speech/latest/reference/support-matrix/asr.html).

### TTS selection

Prefer:

- Fixed multilingual voices for production narration: Magpie TTS Multilingual when its nine documented locales cover the job: en-US, es-US, fr-FR, de-DE, zh-CN, vi-VN, it-IT, hi-IN, ja-JP.
- Broader multilingual TTS with a community-published model: Chatterbox TTS Multilingual if its documented language list and licensing fit the job; clearly label its publisher as Resemble AI community, not NVIDIA-authored.
- Approved voice matching: Magpie TTS Zeroshot or Magpie TTS Flow only after explicit rights/consent are confirmed and access approval is available.
- Low latency conversational output: streaming TTS or WebSocket, not offline WAV synthesis.
- Batch narration or file-based localization: offline synthesis, chunking text at natural sentence/paragraph boundaries under endpoint limits and preserving stable voice/sample-rate settings.

Documented TTS hardware/software boundary verified 2026-07-10: TTS NIM requires NVIDIA GPU compute capability 8.0 or higher and at least 16 GB VRAM; Linux Ubuntu 22.04 or later is recommended; NVIDIA Driver >= 535 and NVIDIA Docker >= 23.0.1 are listed. TTS support matrix lists all TTS models as FP16. Source: [TTS support matrix](https://docs.nvidia.com/nim/speech/latest/reference/support-matrix/tts.html).

### NMT selection

Use NMT when the task needs text translation, speech-to-speech translation, localization review, or terminology control after ASR. Riva Translate 1.6b is documented as the NMT model; the container name is `riva-translate-1_6b`, while the served model may appear as `megatronnmt_any_any_1b`. It supports any-to-any translation across 36 languages as documented by NVIDIA. Source: [About NVIDIA NMT NIM](https://docs.nvidia.com/nim/speech/latest/nmt/index.html).

Use `<dnt>...</dnt>` tags or custom dictionaries for brand, product, and technical terms that must not be translated or must translate in a specific way. Increase `--max-len-variation` for morphologically complex target languages if output truncation appears. Source: [About NVIDIA NMT NIM](https://docs.nvidia.com/nim/speech/latest/nmt/index.html).

Documented NMT hardware/software boundary verified 2026-07-10: NMT NIM requires GPU compute capability 8.0 or higher and at least 16 GB VRAM; Linux Ubuntu 22.04 or later is recommended; NVIDIA Driver >= 535 and NVIDIA Docker >= 23.0.1 are listed. Source: [NMT support matrix](https://docs.nvidia.com/nim/speech/latest/reference/support-matrix/nmt.html).

## API route selection

Choose the client route by interaction pattern:

- HTTP REST: simplest offline tests, curl-based CI checks, language-agnostic integration, single complete files, and file-based TTS. Use `/v1/health/ready` before inference.
- gRPC: higher-feature production clients, streaming ASR/TTS, richer Riva protocol features, and use of NVIDIA's Riva Python client or provided scripts.
- WebSocket realtime: browser-friendly or event-based low-latency interactive sessions. ASR connects to `ws://<address>:9000/v1/realtime?intent=transcription`; TTS connects to `ws://<address>:9000/v1/realtime?intent=synthesize`.

For Python clients, NVIDIA documents `pip install -U nvidia-riva-client` and the `nvidia-riva/python-clients` repository for ready-to-use scripts that call Speech NIM services. Source: [Install the NVIDIA Riva Python Client](https://docs.nvidia.com/nim/speech/latest/get-started/riva-client.html).

## Production heuristics

These are heuristics to improve production quality; validate them on representative audio before treating them as guarantees.

- Preprocess ASR audio to a stable sample rate/channel layout before upload. Keep the original untouched and store derived WAV/FLAC intermediates with provenance.
- For ASR, measure WER/CER on a domain-specific sample set, not just generic clips. Include accents, noise, crosstalk, telephony bandwidth, music beds, and the real microphones/codecs used by the product.
- For realtime ASR, tune chunk duration, endpointing, interim results, punctuation, and diarization separately. Lowest latency and best final transcript are different objectives.
- For diarization, verify "who spoke when" independently from transcript quality. A clean transcript with swapped speaker tags is still a production failure.
- For TTS, generate by semantic chunks rather than arbitrary character windows. Review cross-chunk prosody, breath/noise floors, pronunciation drift, and loudness consistency.
- For voice cloning, create an approval packet before generation: speaker identity, consent evidence, allowed script/use, reference-audio origin, expiration/revocation terms, and storage/deletion plan.
- For localization, run terminology before fluency. Lock product names, acronyms, UI labels, legal phrases, and medical/financial terms with dictionaries or do-not-translate tags before creative polish.
- For speech-to-speech translation, budget latency per stage: ASR endpointing + NMT + TTS first-chunk latency + network jitter. Do not promise "live interpretation" without measuring the whole chain.
- Cache model assets and pre-warm services before first user traffic. First startup can include model download or profile optimization, especially where RMIR generates an optimized engine on the target GPU.
- Record the deployed container image, `NIM_TAGS_SELECTOR`, `/v1/version`, `/v1/metadata`, driver version, GPU model, and API route with each production run.

## Rights, consent, privacy, and licensing

Do this before sending or generating user speech.

1. Confirm rights to input audio. Transcription of calls, meetings, or medical/legal content may require consent, retention controls, and jurisdiction-specific notice.
2. Confirm rights to output voice. Never clone or imitate a person's voice from reference audio unless the user has explicit authorization for that speaker, script, distribution channel, geography, and time period.
3. Separate self-hosted custody from hosted/trial endpoints. Self-hosting can keep speech data inside the user's chosen infrastructure, but logs, metrics, model downloads, license checks, and operational telemetry still need review under the deployed NVIDIA terms and the organization's privacy/security controls.
4. Treat NVIDIA API Catalog hosted endpoints as a trial/prototyping surface unless the user has a production-grade hosted partner route. NVIDIA's FAQ states Developer Program access is for prototyping/research/development/testing, and production use requires NVIDIA AI Enterprise or production-ready partner endpoints. Source: [NVIDIA NIM FAQ](https://forums.developer.nvidia.com/t/nvidia-nim-faq/300317).
5. For production self-hosted NIM, confirm NVIDIA AI Enterprise entitlement or another valid production license path. NVIDIA's developer materials state production deployment is tied to NVIDIA AI Enterprise assurance, support, and API stability. Sources: [NIM for Developers](https://developer.nvidia.com/nim) and [NVIDIA NIM FAQ](https://forums.developer.nvidia.com/t/nvidia-nim-faq/300317).
6. For custom TTS applications, NVIDIA's AI Product Terms state that the customer must have sufficient rights and licenses for content used to generate new content, and restrict custom TTS application distribution/service use. Source: [Product Specific Terms for AI Products](https://www.nvidia.com/en-us/agreements/enterprise-software/product-specific-terms-for-ai-products/).
7. For API Trial Service usage, NVIDIA's API Trial Terms state that user and generated content may be used during the session solely to provide the API service, and are not stored or used at the end of each session except as stated for specific services or security/fraud monitoring. Source: [NVIDIA API Trial Terms of Service PDF](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf).
8. Review data collection in enterprise software terms. NVIDIA's Software License Agreement describes collection for configuration/optimization, service delivery, compliance/fraud detection, product improvement, and related telemetry categories. Source: [NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/).

If the user cannot confirm voice rights or regulated-data handling, refuse voice cloning and propose safer alternatives: stock voice, user-recorded voice with signed consent, transcript-only output, or local-only redaction before inference.

## Complete example: offline ASR for subtitle generation

Production intent: turn a recorded training video into editable captions with timestamps and quality review.

Decision:

- Use ASR NIM offline or true-offline profile if the audio is prerecorded and latency is not interactive.
- Use gRPC/Riva client if word time offsets and richer transcript fields are required; use HTTP only for simple text extraction.
- Enable punctuation if supported and desired, but audit punctuation manually for captions.

Example HTTP smoke test:

```bash
curl -sS http://localhost:9000/v1/health/ready

curl -sS http://localhost:9000/v1/audio/transcriptions \
  -F language=en-US \
  -F response_format=json \
  -F file="@training_clip.wav" \
  --output transcript.json
```

QA checklist:

- Compare a 5-10 minute stratified sample against a human reference.
- Check specialized nouns, product names, numbers, currencies, and acronyms.
- Verify speaker labels separately if a diarization profile was used.
- Store original audio, normalized audio, transcript, model profile, and review notes together.
- Do not burn captions into video until transcript review is complete.

Likely failure modes:

- Wrong language/profile chosen for code-switching.
- Great transcript but missing usable word timings.
- Diarization labels drift through overlapping speech.
- HTTP route used when a gRPC route was needed for richer output.

## Complete example: low-latency voice-agent loop

Production intent: a kiosk or agent hears short user utterances and speaks responses.

Decision:

- ASR: streaming profile over gRPC or WebSocket, with interim results only if the dialogue manager can tolerate corrections.
- NMT: include only if cross-language support is required; otherwise avoid the extra latency stage.
- TTS: streaming TTS or WebSocket route so playback can begin before the full response is synthesized.
- Deployment: run ASR and TTS as independent containers so each can scale separately.

Operational plan:

1. Pre-warm ASR and TTS containers and poll readiness.
2. Send microphone audio in chunks; keep final transcript confidence/endpointing separate from interim text.
3. Send final or stable partial text to the dialogue system.
4. Chunk response text at phrase boundaries and start TTS streaming.
5. Measure total turn latency from end of user speech to first audible output, not just model latency.
6. Log dropped chunks, reconnects, health failures, and request duration metrics.

QA checklist:

- Test barge-in, silence, short acknowledgements, noisy background, and accents.
- Validate that captions/transcripts do not leak to analytics stores without consent.
- Confirm all generated voice output is labeled or disclosed if the deployment context requires it.

## Complete example: approved voice-cloned localization

Production intent: localize internal training modules using an approved employee voice reference.

Decision:

- Use NMT with do-not-translate tags or custom dictionaries for product terminology.
- Use a zero-shot TTS model only if access approval is available and the speaker consent packet is complete.
- Use Flow when a clean prompt transcript exists and offline higher-fidelity matching matters; use Zeroshot when streaming or no prompt transcript is needed.

Required custody packet:

- Speaker name or pseudonymous ID.
- Written consent scope: languages, scripts, distribution, duration, revocation process.
- Reference WAV source and transcript.
- Storage location for reference audio and generated outputs.
- Reviewer sign-off for likeness and misuse risk.

Example HTTP synthesis shape:

```bash
curl -sS http://localhost:9000/v1/audio/synthesize --fail-with-body \
  -F language=en-US \
  -F text="This internal module explains how to configure <dnt>NVIDIA NIM</dnt> safely." \
  -F audio_prompt=@approved_reference.wav \
  --output localized_voice.wav
```

QA checklist:

- Confirm pronunciation of protected terminology.
- Loudness-normalize and compare against house delivery standards.
- Have the consenting speaker or authorized reviewer approve likeness if policy requires it.
- Retain the run manifest; delete prompt audio and generated variants according to the consent plan.

## Failure triage

- `503` readiness errors: poll `/v1/health/ready`; do not retry large audio blindly while models are still loading.
- `400` on ASR HTTP: verify `file`, `language` or `model`, supported audio format, and model availability.
- `400` on TTS HTTP: verify non-empty text/language, text under 2,000 normalized characters, valid voice name from `/v1/audio/list_voices`, and `LINEAR_PCM` encoding.
- Slow first request: check whether the container is downloading models or building an RMIR profile for the target GPU.
- GPU out of memory: choose a smaller batch/profile, remove unneeded `mode=all`, disable diarization if not required, or deploy separate containers on separate GPUs.
- Bad ASR punctuation: confirm punctuation is enabled for the model/profile; post-process cautiously and never alter legal/medical transcripts without review.
- TTS raw output sounds like noise: if using `/v1/audio/synthesize_online`, add a WAV header or convert raw LPCM with the correct sample rate, channels, and signed 16-bit format.
- Hosted endpoint throttling or variable latency: treat build.nvidia.com/API Catalog as a trial/prototyping route; self-host or use a production partner endpoint for predictable service.

## Source notes

Use current NVIDIA docs before deploying because model names, profile selectors, supported languages, WSL2 status, licensing, and hosted endpoint availability are volatile. Core sources verified 2026-07-10:

- [NVIDIA Speech NIM Microservices overview](https://docs.nvidia.com/nim/speech/latest/about/index.html)
- [How NVIDIA Speech NIM Microservices Work](https://docs.nvidia.com/nim/speech/latest/about/how-it-works.html)
- [ASR NIM docs](https://docs.nvidia.com/nim/speech/latest/asr/index.html), [ASR support matrix](https://docs.nvidia.com/nim/speech/latest/reference/support-matrix/asr.html), and [ASR API references](https://docs.nvidia.com/nim/speech/latest/reference/api-references/asr/index.html)
- [TTS NIM docs](https://docs.nvidia.com/nim/speech/latest/tts/index.html), [TTS support matrix](https://docs.nvidia.com/nim/speech/latest/reference/support-matrix/tts.html), and [TTS API references](https://docs.nvidia.com/nim/speech/latest/reference/api-references/tts/index.html)
- [NMT NIM docs](https://docs.nvidia.com/nim/speech/latest/nmt/index.html) and [NMT support matrix](https://docs.nvidia.com/nim/speech/latest/reference/support-matrix/nmt.html)
- [NIM for Developers](https://developer.nvidia.com/nim), [NVIDIA NIM FAQ](https://forums.developer.nvidia.com/t/nvidia-nim-faq/300317), [NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/), [Product Specific Terms for AI Products](https://www.nvidia.com/en-us/agreements/enterprise-software/product-specific-terms-for-ai-products/), and [NVIDIA API Trial Terms of Service](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)
