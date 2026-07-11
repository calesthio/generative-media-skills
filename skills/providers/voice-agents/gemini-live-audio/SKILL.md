---
name: gemini-live-audio
description: Build and evaluate low-latency spoken, multimodal, and translation experiences with Google Gemini Live API and Gemini Enterprise Agent Platform Live API. Use when a media-production or voice-agent workflow needs real-time audio input/output, barge-in, voice configuration, live transcription, live translation, tool/function calling during a spoken session, WebSocket session design, latency QA, quotas/cost review, or Google/Vertex data-governance tradeoffs.
---

# Gemini Live audio

Use this skill when the job is a live spoken interaction, not a batch narration render. Gemini Live is for bidirectional sessions: microphone or streamed media in, spoken model output back, with turn-taking, interruptions, tools, and session lifecycle concerns. If the deliverable is a finished voiceover, audiobook, podcast narration, or offline transcript, prefer a TTS or speech-to-text skill unless the user explicitly needs live turn-taking.

All volatile facts below were verified against official Google AI and Google Cloud documentation on 2026-07-10. Model names, preview/GA status, pricing, rate limits, supported regions, and governance controls change often; re-check official docs before production launch, procurement commitments, or regulated deployment.

## Documented facts

### Current shape of the product

- Gemini Live API is a stateful WebSocket API for low-latency voice and vision interactions. It can process continuous streams of audio, images, text, and, in API references, video; it returns spoken/audio output and can also return text/function-call events depending on configuration and model.
- Google AI Live API pages currently note that the Interactions API is generally available and recommended for access to the latest features and models. Treat this skill as Live-API-specific guidance; for a greenfield production agent, verify whether Live API or Interactions API is the intended Google surface before committing architecture.
- Google AI Developer API docs mark Live API as Preview. Google Cloud / Gemini Enterprise Agent Platform docs separately document Vertex/enterprise availability and a GA Gemini 2.5 Flash Native Audio model. Treat Developer API and Gemini Enterprise Agent Platform as distinct deployment surfaces with different auth, terms, locations, governance, quotas, and support.
- The principal Live agent model family documented on 2026-07-10 includes `gemini-3.1-flash-live-preview` in the Developer API docs and `gemini-live-2.5-flash-native-audio` / Gemini 2.5 Flash Live API Native Audio in Gemini Enterprise Agent Platform docs. Live Translation is documented separately with `gemini-3.5-live-translate-preview`.
- Use Live Agent mode when the model is an assistant that reasons, asks questions, calls tools, and handles turns. Use Live Translation mode when the model is an interpreter pipeline: audio in one language, translated audio out another. Live Translation is documented as audio-restricted, translation-only, and not a tool/instruction-driven agent surface.

### Media and transport boundaries

- Transport: persistent WSS session. With SDKs, use the Live connect/session abstractions; with raw WebSockets, connect to the documented `BidiGenerateContent` endpoint and manage JSON messages, setup, realtime input, server content, tool calls, and closure yourself.
- Session setup is front-loaded. The initial setup message/config includes model, response modalities, generation parameters, system instructions, and tools. Do not assume you can freely mutate the model mid-connection; design reconnect/resume paths for material changes.
- Audio input: raw little-endian 16-bit PCM. Native input rate is 16 kHz; docs say Live API can resample, but production clients should send `audio/pcm;rate=16000` unless there is a measured reason not to.
- Audio output: raw little-endian 16-bit PCM at 24 kHz.
- Chunk microphone audio in small frames. Google best practices recommend 20-40 ms chunks for latency, and warn against large input buffering. A practical upper bound for client buffering is 100 ms unless you are deliberately trading latency for stability.
- Images are documented as JPEG at up to 1 FPS on the Developer API overview. Video/image input support and pricing differ by model and surface; verify the exact model page before promising live screen share, camera, or frame ingestion.
- Native-audio Live models support audio response modality. If the product needs text of the model's spoken answer, enable output audio transcription rather than assuming text output from the native audio response.

### Transcription, language, voice, and turn-taking

- Live API supports audio transcriptions of user input and model output when enabled in session config. Use these transcripts for UI captions, logs, QA, and handoff summaries; do not sell them as court-grade transcripts without separate validation.
- Developer docs list broad multilingual support for Live; the overview highlights 70 supported languages for voice-agent use cases and the capabilities page currently lists 97 supported languages. Native audio models can switch languages naturally; for constrained language behavior, put the output language restriction in system instructions. Non-native/cascaded models may use `speech_config.language_code`.
- Voice selection is configured through `speechConfig.voiceConfig.prebuiltVoiceConfig.voiceName`. Official docs show 30 voice options for Gemini Live API / Native Audio on Vertex and note native audio models can use the TTS voice set available in AI Studio. Always verify the current voice list before offering named voices.
- Barge-in is supported. When the user speaks over the model, the server can send an interruption signal. The client must stop/discard queued playback immediately; otherwise the user hears stale audio and the system feels like it ignored them.
- Automatic VAD can be configured, or disabled so the client sends `activityStart` and `activityEnd`. With automatic VAD, `prefixPaddingMs` protects word onsets and `silenceDurationMs` controls turn-end latency. Google documents 500-800 ms silence as a good balance and warns that very low thresholds fragment utterances; manual VAD should include pre-speech context and avoid aggressive end-of-speech cutoffs.
- Proactive Audio and Affective Dialog are Native Audio capabilities documented for Gemini 2.5 Flash Live API Native Audio. Use them for ambient or device-directed experiences only after explicit user consent and a QA plan; they change when and why the system responds.

### Tools and agent behavior

- Live API supports function calling and Google Search grounding. It does not support all non-live tools; official tool tables list Google Maps, code execution, and URL context as unsupported for the compared Live models on the Live tools page dated 2026-06-01.
- Unlike some non-live SDK flows, Live API does not automatically handle tool responses. The client must receive tool-call events, execute/dispatch the allowed function, and send `FunctionResponse` objects back.
- Tool behavior differs by model. Docs list Gemini 3.1 Flash Live Preview as synchronous-only for function calling, while Gemini 2.5 Flash Live Preview supports synchronous and asynchronous function calling. Do not promise non-blocking tools unless the selected model officially supports them.
- For non-blocking tools where supported, design the function declaration and response scheduling deliberately: interrupt, wait until idle, or silently store/use later. Tool responses that arrive at the wrong time can make the agent interrupt sensitive speech or ignore important events.
- Grounding with Google Search can improve factual freshness, but it has pricing and data-retention implications. In privacy-sensitive or zero-retention scopes, confirm whether Search grounding is allowed.

### Sessions, auth, cost, quotas, and governance

- Without context window compression, documented session limits are 15 minutes for audio-only and 2 minutes for audio+video. Google also documents a connection lifetime around 10 minutes. Use context window compression and session resumption for production-length sessions.
- Session resumption requires receiving/storing resumption handles/tokens and reconnecting with the latest handle. Developer API docs mention resumption token validity of 2 hours; Gemini Enterprise zero-data-retention docs say Live session resumption stores cached data including text/video/audio prompt data and model outputs for up to 24 hours. Treat these as surface-specific and verify before designing retention promises.
- Context windows differ by model class: Google docs list 128k tokens for native audio output models and 32k for other Live models. Audio accumulates quickly; Google docs price/count audio at roughly 25 tokens per second.
- Rate limits are per project and vary by model and usage tier. Experimental/preview models usually have stricter rate limits. Check active limits in AI Studio or Google Cloud before load tests.
- Developer API pricing on 2026-07-10 lists `gemini-3.1-flash-live-preview` paid pricing at $0.75/M text input tokens, $3.00/M audio input tokens (about $0.005/min), $1.00/M image/video input tokens (about $0.002/min), $4.50/M text output tokens, and $12.00/M audio output tokens (about $0.018/min). It lists Live Translate audio as about $0.0368/min combined input/output based on 25 audio tokens/sec. Re-check pricing before quoting.
- Developer API free tier content may be used to improve Google products; paid tier content is documented as not used to improve products. Developer API logs can be retained for project logging if enabled, and abuse monitoring/grounding have separate retention rules. For regulated users, evaluate Gemini Enterprise Agent Platform instead of defaulting to API keys.
- Gemini Enterprise Agent Platform uses Google Cloud auth/IAM, regional/global endpoints, enterprise support/SLA options, provisioned throughput, and data residency controls. Endpoint choice alone does not guarantee data residency; Cloud docs distinguish endpoint routing from data-at-rest and ML processing commitments. Global endpoints maximize availability/latency but do not provide regional isolation.
- For zero data retention on Gemini Enterprise Agent Platform, do not enable request-response logging, do not enable Live session resumption, understand abuse-monitoring exceptions, and account for in-memory caching settings. For Developer API ZDR, paid services have a training restriction, but Search/Maps grounding and abuse monitoring have separate retention constraints.

## Empirical / operational observations

No first-party benchmark is bundled with this skill. Do not invent latency or quality numbers. If the user cares about latency, run a project-specific measurement on the target network, browser/device, model, and deployment surface.

Operational observations from production voice systems that must be verified in the target app:

- Perceived latency is often dominated by microphone capture, VAD end-of-speech delay, client buffering, playback scheduling, and reconnect handling, not only model inference.
- The best-sounding demo can fail in production if barge-in handling leaves stale audio in the output buffer.
- Live function calling needs stricter schema and flow design than text chat, because a spoken user cannot easily inspect or edit arguments before actions execute.
- Real-time translation and voice-agent behavior should be tested separately; a strong assistant setup may be wrong for translation because translation needs low-latency continuous streaming, not deliberative turns.

## Production heuristics

### Choose the right Gemini Live mode

Use Gemini Live Agent when the user needs:

- a voice assistant, coach, tutor, concierge, interviewer, receptionist, NPC, operator, or visual-support agent;
- barge-in and natural turn-taking;
- live tool use/function calling;
- screen/camera/image context during conversation;
- transcripts alongside spoken interaction.

Use Live Translation when the user needs:

- low-latency speech-to-speech interpretation;
- source language to target language audio;
- no tools, no agent actions, no multimodal reasoning, and no persona-heavy conversation beyond interpreter behavior.

Do not use Gemini Live as the primary tool when the user needs:

- a polished prerecorded narration file;
- deterministic subtitle generation for an existing video;
- offline batch transcription with word-level timestamps;
- long-form audio mastering, music, or sound effects;
- a regulated call-center deployment without legal review of consent, recording, retention, and escalation requirements.

### Architecture choices

For prototypes and trusted server environments, a backend-to-Gemini WebSocket is simplest:

1. Browser/mobile captures mic and optional camera/screen frames.
2. Client streams to your backend over WebRTC/WebSocket.
3. Backend authenticates to Gemini, applies policy/tool gating, and forwards allowed media.
4. Backend returns audio chunks, transcript events, tool confirmations, and state updates.

For lowest-latency client-to-Gemini connections, use ephemeral tokens:

1. Client authenticates with your backend.
2. Backend requests an ephemeral token, ideally constrained to model/config/tool policy.
3. Client opens the Live API WebSocket with the token.
4. Backend still controls tool execution, user identity, logging policy, and escalation.

Prefer client-to-Gemini only when you can still protect secrets, enforce allowed tools, record consent, and monitor abuse. Never ship a long-lived API key in a browser or mobile app.

### System instruction design for spoken agents

Write the Live agent instruction as operational policy, not a long essay:

1. Persona and role: who the agent is, voice/tone, domain, language.
2. Conversation loop: what to ask once, what can repeat, when to summarize.
3. Tool policy: exact conditions for each function, required confirmation before consequential actions, what to say while waiting.
4. Safety/consent boundaries: recording notice, emergency limitations, privacy, escalation.
5. Response style: short spoken turns, one question at a time, no markdown, no hidden chain-of-thought.

For spoken UX, keep responses short by default. Ask one question per turn. Confirm high-risk facts verbally before tool calls that spend money, alter accounts, make bookings, send messages, or disclose sensitive data.

### Audio and latency setup

Use this starting point unless measurement says otherwise:

- input format: mono PCM16 little-endian at 16 kHz;
- output playback: PCM16 at 24 kHz;
- input chunk size: 20-40 ms;
- automatic VAD silence: 500-800 ms;
- prefix padding: nonzero; tune with clipped-first-syllable tests;
- client input buffer: as small as stable networking allows, usually below 100 ms;
- playback buffer: enough to avoid clicks/dropouts, but discard immediately on interruption;
- session lifecycle: enable context compression for long calls; implement GoAway and reconnect/resume logic.

### Tool-calling safety for voice

Classify tools before exposing them:

- Read-only tools: weather, order status, product lookup. Can usually run without confirmation if the user asks.
- Low-impact write tools: create draft, add note, set reminder. Confirm if content matters.
- High-impact write tools: purchase, submit form, cancel service, send message, unlock door, update financial/health/legal data. Require explicit confirmation with a spoken summary of arguments.
- Background tools: long searches, CRM lookup, RAG, ticket creation. Use non-blocking only if the model supports it and the user experience remains understandable.

Make function schemas narrow. Include enums, units, locale, timezone, irreversible/action flags, and user-visible confirmation text in tool responses. Do not rely on the model to infer policy from function names.

### Governance and consent

Before productionizing a Live audio experience, document:

- whether audio is recorded or only streamed;
- whether transcripts are stored, how long, and who can access them;
- whether the app uses Developer API free tier, paid tier, or Gemini Enterprise Agent Platform;
- whether grounding, logging, session resumption, or caching changes retention;
- whether users are informed that they are speaking with AI;
- whether local law requires two-party call recording consent;
- escalation paths for emergencies, minors, medical/legal/financial advice, or abuse.

For voice likeness and media rights, do not imply that a Gemini voice is a cloned human voice unless Google explicitly supports that workflow and the user has documented rights/consent. Avoid prompts that impersonate a real person, celebrity, employee, or customer without authorization.

## Complete examples

### Example 1: retail support voice agent with order lookup

Production intent: A low-latency spoken assistant answers product and order questions, can look up order status, and creates return labels only after confirmation.

Applicable mode: Gemini Live Agent, not Live Translation.

Model/surface to verify: `gemini-3.1-flash-live-preview` on Developer API for prototype; consider Gemini Enterprise Agent Platform for production support, IAM, data residency, and support/SLA.

Inputs and constraints:

- Browser microphone, English and Spanish users, no camera.
- Need transcripts for support QA.
- Read-only `get_order_status(order_id, postal_code)`.
- Write tool `create_return_label(order_id, reason)` requires confirmation.
- No payment changes, no medical/legal advice.

Session config sketch:

```json
{
  "model": "gemini-3.1-flash-live-preview",
  "response_modalities": ["AUDIO"],
  "output_audio_transcription": {},
  "input_audio_transcription": {},
  "speech_config": {
    "voice_config": {
      "prebuilt_voice_config": { "voice_name": "Kore" }
    }
  },
  "realtime_input_config": {
    "automatic_activity_detection": {
      "prefix_padding_ms": 300,
      "silence_duration_ms": 700
    }
  },
  "tools": [
    {
      "function_declarations": [
        {
          "name": "get_order_status",
          "description": "Look up status for an authenticated order when the user provides order ID and postal code.",
          "parameters": {
            "type": "object",
            "properties": {
              "order_id": { "type": "string" },
              "postal_code": { "type": "string" }
            },
            "required": ["order_id", "postal_code"]
          }
        },
        {
          "name": "create_return_label",
          "description": "Create a return shipping label only after the user explicitly confirms the order ID and return reason.",
          "parameters": {
            "type": "object",
            "properties": {
              "order_id": { "type": "string" },
              "reason": { "type": "string" },
              "confirmed_by_user": { "type": "boolean" }
            },
            "required": ["order_id", "reason", "confirmed_by_user"]
          }
        }
      ]
    }
  ]
}
```

System instruction excerpt:

```text
You are Mira, a concise retail support voice assistant.
Speak in the user's language when you can do so clearly.
Ask one question at a time. Keep spoken answers under 20 seconds unless the user asks for detail.
For order lookup, collect order ID and postal code, then call get_order_status.
Before creating a return label, summarize the order ID and reason, ask "Should I create the return label now?", and call create_return_label only if the user explicitly says yes.
Never ask for full payment card numbers. If the user asks for a refund decision, explain you can create a return request but a human reviews refunds.
If the user interrupts, stop your current explanation and answer the new question.
```

Expected result:

- Natural spoken turns, quick interruption handling, order status returned verbally and in UI transcript.
- Return label creation occurs only after explicit confirmation.

Failure modes:

- Agent calls `create_return_label` before confirmation.
- Audio continues playing after interruption.
- VAD clips order IDs or postal codes.
- Language auto-switching surprises QA; constrain language in instructions if required.
- Search grounding is enabled unnecessarily and creates retention/cost exposure.

Variations:

- Move to backend-proxied architecture for stricter tool control.
- Use ephemeral tokens only for WebSocket media path while backend owns tools.
- Add camera/screen only after verifying model support, session duration, cost, and consent.

### Example 2: live speech-to-speech event translation

Production intent: Translate a presenter from Japanese to English in near real time for a remote audience.

Applicable mode: Live Translation with `gemini-3.5-live-translate-preview`, not a general Live Agent.

Inputs and constraints:

- One speaker feed, no tools, no assistant persona.
- Target language English.
- Audio must remain continuous; transcript is nice-to-have but not the primary deliverable.
- Human interpreter fallback for critical segments.

Workflow:

1. Verify the source/target languages are supported on the current Live Translation doc.
2. Configure Live API translation settings for source and target language.
3. Capture presenter audio as PCM16, chunk 20-40 ms, and stream continuously.
4. Play translated output with a jitter buffer tuned for intelligibility, not interruption-heavy dialogue.
5. Record input/output timing, dropout, mistranslations, and audience feedback.

Expected result:

- The system behaves like a translator pipeline and does not ask clarifying questions, call tools, or take actions.

Failure modes:

- An agent prompt is used, causing summaries or responses instead of direct translation.
- The app waits for complete turns, adding unacceptable delay.
- Mixed-language code-switching or names are mistranslated; provide glossary/context if the API surface supports it and test beforehand.
- Sensitive event audio retention is not reviewed.

Variations:

- For bilingual meetings where users ask the AI to take notes or call tools, use Live Agent plus a translation policy, not Live Translation.
- For broadcast-quality captions, run separate post-event transcription/subtitle QA.

### Example 3: field technician visual support agent

Production intent: A technician points a mobile camera at equipment and asks spoken questions. The agent can identify likely components, ask for another view, and open a support ticket.

Applicable mode: Gemini Live Agent with audio plus low-rate image/video input, if the selected model/surface supports it.

Inputs and constraints:

- Mobile microphone plus camera frames.
- No claims of definitive safety diagnosis.
- Tool `create_support_ticket(summary, severity, asset_id, photo_refs)` requires user confirmation.
- Session may exceed 2 minutes, so compression/resumption or session handoff is required.

System instruction excerpt:

```text
You are an equipment support assistant for trained technicians.
Use visual context only to guide inspection; do not certify equipment as safe.
Ask for a closer view, better lighting, or label photo when needed.
If a potential hazard is visible or described, tell the technician to follow their site safety procedure and stop remote troubleshooting.
Before creating a support ticket, summarize the observed issue, asset ID, severity, and photos to attach, then ask for confirmation.
```

Expected result:

- Short spoken guidance, requests for better frames when visual input is insufficient, conservative safety language, and confirmed ticket creation.

Failure modes:

- Session terminates after the documented audio+video limit because no compression/resumption/handoff was implemented.
- Visual frames are too infrequent/blurred for reliable guidance.
- The agent overstates diagnosis or safety.
- Tool call includes images/audio not approved by the user or not allowed by data policy.

Variations:

- If camera streaming is too costly or unavailable, capture still images on user request and send at <=1 FPS.
- Use Gemini Enterprise regional endpoints for data governance after verifying model/location support.

## Production QA checklist

Before shipping, test with real devices and noisy environments:

- Audio format: verify PCM16 mono input, 16 kHz input rate, 24 kHz output playback, no endian or WAV-header mistakes in raw chunks.
- Latency: measure mic-to-first-audio, end-of-speech-to-first-audio, interruption-to-silence, reconnect time, and tool-call round trip.
- Barge-in: while model is speaking, interrupt with short, long, and noisy utterances; confirm stale output is discarded.
- VAD: test clipped first syllables, mid-sentence pauses, long thinking pauses, short confirmations, serial numbers, and accented speech.
- Transcripts: compare input/output transcriptions against recordings for the product's required accuracy; mark them as assistive if not formally validated.
- Tools: simulate missing arguments, ambiguous requests, duplicate function calls, delayed responses, tool errors, and high-impact confirmations.
- Session lifecycle: test 2-minute, 10-minute, 15-minute, reconnect, GoAway, context compression, and resumption behavior.
- Cost: estimate per-minute input and output audio tokens, plus Search/tool costs; enforce spend/rate-limit alerts.
- Privacy: verify consent prompts, recording indicators, logs retention, transcript storage, grounding retention, and ZDR constraints.
- Safety: test harassment, self-harm, medical/legal/financial, emergency, minors, and disallowed impersonation scenarios with the configured safety settings.

## Source ledger

Official sources used and verified on 2026-07-10:

- Gemini Live API overview: https://ai.google.dev/gemini-api/docs/live-api
- Interactions API overview: https://ai.google.dev/gemini-api/docs/interactions-overview
- Live API capabilities guide: https://ai.google.dev/gemini-api/docs/live-api/capabilities
- Raw WebSockets API reference: https://ai.google.dev/api/live
- Get started with raw WebSockets: https://ai.google.dev/gemini-api/docs/live-api/get-started-websocket
- Tool use with Live API: https://ai.google.dev/gemini-api/docs/live-api/tools
- Session management: https://ai.google.dev/gemini-api/docs/live-api/session-management
- Ephemeral tokens: https://ai.google.dev/gemini-api/docs/live-api/ephemeral-tokens
- Live API best practices: https://ai.google.dev/gemini-api/docs/live-api/best-practices
- Live Translation: https://ai.google.dev/gemini-api/docs/live-api/live-translate
- Gemini model list: https://ai.google.dev/gemini-api/docs/models
- Developer API pricing: https://ai.google.dev/gemini-api/docs/pricing
- Developer API rate limits: https://ai.google.dev/gemini-api/docs/rate-limits
- Developer API regions: https://ai.google.dev/gemini-api/docs/available-regions
- Developer API data logging/sharing: https://ai.google.dev/gemini-api/docs/logs-policy
- Developer API zero data retention: https://ai.google.dev/gemini-api/docs/zdr
- Safety settings: https://ai.google.dev/gemini-api/docs/safety-settings
- Gemini Enterprise Agent Platform Live API and Gemini 2.5 Flash Native Audio: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-live-api
- Gemini Enterprise Agent Platform voice/language configuration: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/live-api/configure-language-voice
- Gemini Enterprise Agent Platform session management: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/live-api/start-manage-session
- Gemini Enterprise pricing: https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing
- Gemini Enterprise endpoints/locations: https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations
- Gemini Enterprise data residency: https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/data-residency
- Gemini Enterprise zero data retention: https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/zero-data-retention
