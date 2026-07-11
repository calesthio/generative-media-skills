---
name: hume-evi
description: "Build production realtime voice agents with Hume's Empathic Voice Interface (EVI): speech-to-speech sessions, empathic/prosodic response design, EVI 3 versus EVI 4-mini selection, WebSocket and SDK integration, tools/function calling, interruption/barge-in, turn-taking, transcripts/audio artifacts, pricing/limits, privacy, safety, consent, and QA."
---

# Hume EVI production guide

Use this skill when the task is to design, implement, troubleshoot, or review a Hume Empathic Voice Interface (EVI) realtime voice agent. Do not use it for offline-only Hume Text-to-Speech/Octave work unless the user is explicitly configuring EVI voices or comparing EVI to TTS.

Hume's EVI is a realtime speech-to-speech agent interface. It streams user audio, measures expressive vocal modulation, generates a language response, and produces expressive assistant speech. Treat it as a live conversation system, not as a batch transcription or batch TTS API. Documented facts below were verified on 2026-07-10 unless a source date is explicitly noted.

Primary official sources:

- Hume EVI overview: https://dev.hume.ai/docs/speech-to-speech-evi/overview
- EVI version guide: https://dev.hume.ai/docs/speech-to-speech-evi/configuration/evi-version
- Configuration guide: https://dev.hume.ai/docs/speech-to-speech-evi/configuration/build-a-configuration
- Chat WebSocket API reference: https://dev.hume.ai/reference/speech-to-speech-evi/chat
- Audio guide: https://dev.hume.ai/docs/speech-to-speech-evi/guides/audio
- Tool use guide: https://dev.hume.ai/docs/speech-to-speech-evi/features/tool-use
- Prompting guide: https://dev.hume.ai/docs/speech-to-speech-evi/guides/prompting
- Privacy controls: https://dev.hume.ai/docs/resources/privacy
- Pricing page: https://www.hume.ai/pricing
- Acceptable Use Policy: https://www.hume.ai/acceptable-use-policy

## Capability boundaries

Documented facts:

- EVI is for realtime voice interaction. The Chat WebSocket accepts streamed `audio_input`, `session_settings`, `user_input`, `assistant_input`, and tool response messages; audio input must be streamed continuously in small chunks, not sent as a whole prerecorded file. Hume recommends roughly 20 ms audio buffers generally or 100 ms for web apps. Source: https://dev.hume.ai/reference/speech-to-speech-evi/chat
- Direct browser or app integration is typically WebSocket-based. Hume's React SDK abstracts microphone capture, playback, and WebSocket connection management; the TypeScript and Python SDKs expose lower-level integration paths. Source: https://dev.hume.ai/docs/speech-to-speech-evi/quickstart/nextjs and https://dev.hume.ai/docs/speech-to-speech-evi/quickstart/typescript
- Use the Python SDK primarily for CLIs and desktop apps where the Python process can access the user's audio device. For hosted web apps, put audio capture in the browser; server-side Python cannot directly access the user's microphone and routing audio through a backend adds latency. Source: https://dev.hume.ai/docs/speech-to-speech-evi/quickstart/python
- EVI can use Hume Voice Library voices and account-private Custom Voices. The EVI voice can be specified in a persistent config or overridden for a session with a voice ID. Custom voice cloning requires rights/consent to the voice sample. Sources: https://dev.hume.ai/docs/speech-to-speech-evi/configuration/voice and https://dev.hume.ai/docs/voice/voice-cloning
- EVI supports tools/function calling through supported supplemental LLMs, not through every native EVI-only configuration. Hume documents tool use with Claude, GPT, Gemini, Moonshot AI, and custom language models that follow OpenAI function-calling conventions. Source: https://dev.hume.ai/docs/speech-to-speech-evi/features/tool-use
- Expression measurements are available from audio user messages, not text-only `user_input`, because the prosody model relies on audio input. Source: https://dev.hume.ai/reference/speech-to-speech-evi/chat
- Chat history and reconstructed audio are retrievable only when data retention is enabled. If data retention is disabled, resume chats, chat history retrieval, and audio reconstruction are not supported. Sources: https://dev.hume.ai/docs/speech-to-speech-evi/features/resume-chats and https://dev.hume.ai/docs/speech-to-speech-evi/features/audio-reconstruction

Do not claim:

- That EVI diagnoses a user's inner emotional state. Hume's own use-case guidance says expression labels should be treated as measurements of complex expressive behavior, not direct inferences of how someone feels. Source: https://dev.hume.ai/docs/resources/use-case-guidelines
- That EVI supports uploading whole audio files as a realtime conversation input. The realtime Chat endpoint expects streamed chunks; Hume error `E0723` flags whole audio files as an invalid incoming-audio pattern. Source: https://dev.hume.ai/docs/resources/errors
- That tool calling works without a supplemental or custom LLM configured for tool use.
- That an EVI agent is HIPAA-ready just because Hume has HIPAA-related features. Hume's terms require an express written agreement/BAA before covered entities or business associates provide PHI. Sources: https://www.hume.ai/terms-of-use and https://dev.hume.ai/docs/resources/privacy

## Choosing EVI version and model path

As of 2026-07-10, Hume documents EVI 3 and EVI 4-mini as the supported EVI versions; EVI 1 and EVI 2 reached end of support on 2025-08-30. If `config_id` is omitted, Chat uses EVI 3 by default. Source: https://dev.hume.ai/docs/speech-to-speech-evi/configuration/evi-version

Use EVI 3 when:

- The agent should run in English with Hume's native speech-language model and can benefit from quick responses.
- You want native EVI response generation without requiring an external LLM.
- You need the broadest documented support for quick, emotionally responsive English voice-agent behavior.
- The application is sensitive to external-LLM cost or third-party LLM data flow.

Use EVI 4-mini when:

- The agent must support one of Hume's documented EVI 4-mini languages: English, Japanese, Korean, Spanish, French, Portuguese, Italian, German, Russian, Hindi, or Arabic.
- You accept that EVI 4-mini requires a supplemental LLM and does not support quick responses, per Hume's EVI version comparison.
- You want the latency improvement Hume documents for EVI 4-mini: approximately 100 ms lower model latency on each response.

Use a supplemental LLM when:

- Tool use/function calling is needed.
- The domain requires complex reasoning, long system prompts, strict policy logic, or domain knowledge that should live in the LLM layer.
- You need provider-specific capabilities such as web search, structured function calling, or model behavior already validated elsewhere.

Use a custom language model (CLM) when:

- The application needs direct control over the assistant text before EVI speaks it.
- Regulatory or brand requirements require post-processing, deterministic routing, or proprietary model use.
- You need to keep the language generation account, logging, or policy enforcement outside Hume-managed external LLM usage.

Production heuristic: for a customer-support agent with tools, start with EVI 3 plus a fast supplemental LLM if English-only; start with EVI 4-mini plus a fast supplemental LLM if multilingual support is a hard requirement. Measure actual time-to-first-token and barge-in behavior with the user's target devices before deciding.

## Configuration surface

Persistent EVI Configs are versioned and can include:

- EVI version
- voice
- system prompt
- language model
- user-defined tools and built-in tools
- quick responses, only for EVI 3
- turn detection
- interruption sensitivity
- event messages
- timeouts
- webhooks

Source: https://dev.hume.ai/docs/speech-to-speech-evi/configuration/build-a-configuration

Session Settings are temporary and apply only to the current Chat. They can be supplied at Chat initialization or sent during a Chat with a `session_settings` message. They can override or provide session-specific voice, prompt, context, audio format, tools, built-in tools, dynamic variables, third-party LLM API key, and custom session ID. Source: https://dev.hume.ai/docs/speech-to-speech-evi/configuration/session-settings

Use persistent Configs for release-controlled agent behavior:

- stable voice and persona
- audited system prompt
- allowed tools
- language model selection
- turn-taking and interruption policy
- timeout policy
- webhook subscriptions

Use Session Settings for per-call context:

- user name, locale, plan tier, current account state
- temporary "the user just clicked X" context
- session-specific tool enable/disable
- voice override for a selected persona
- custom session correlation ID
- customer-owned supplemental LLM API key

Avoid burying critical safety or compliance requirements only in ephemeral session context. Put non-negotiable rules in the config prompt and enforce them in tools/backend policy as well.

## Audio and realtime UX requirements

Documented facts:

- EVI is live and streamed; send small audio chunks continuously, not whole files. Source: https://dev.hume.ai/docs/speech-to-speech-evi/guides/audio
- For web integrations, open the EVI WebSocket before starting microphone recording, because formats such as WAV or WebM include headers that EVI needs to interpret the stream. Source: https://dev.hume.ai/docs/speech-to-speech-evi/guides/audio
- Enable echo cancellation, noise suppression, and automatic gain control for capture. Hume's TypeScript helpers do this for web integrations. Source: https://dev.hume.ai/docs/speech-to-speech-evi/guides/audio
- For mute, Hume recommends sending silence frames rather than sending nothing, so the service can distinguish a muted active stream from a disconnected stream. Source: https://dev.hume.ai/docs/speech-to-speech-evi/guides/audio
- Audio output arrives as streamed `audio_output` messages containing base64-encoded WAV. Queue assistant audio segments rather than playing everything immediately, because generated audio can arrive faster than it should be spoken. Source: https://dev.hume.ai/docs/speech-to-speech-evi/guides/audio
- If using raw PCM, specify `linear16`, sample rate, and channels through audio session settings. Hume documents `linear16` as the supported raw encoding. Source: https://dev.hume.ai/docs/speech-to-speech-evi/guides/audio
- Mu-law (`mulaw` / `μ-law`), common in telephony streams, is not presently supported directly by EVI; convert telephony audio before sending it to EVI. Source: https://dev.hume.ai/docs/speech-to-speech-evi/guides/audio

Production heuristics:

- Prefer the React SDK for web prototypes and production web apps unless you have a reason to own the audio queue.
- Keep the WebSocket, microphone capture, and playback path client-side when possible. Backend proxying can be necessary for security or telephony, but it adds latency and failure modes.
- Collect QA traces with device/browser/OS, microphone, headset/speaker mode, packet loss, buffer size, time-to-first-audio, interruption delay, and final transcript.
- Treat poor acoustic echo cancellation as a product bug, not a model bug. It causes false user interruptions and can degrade prosody measurements.

## Turn taking, interruption, and pausing

EVI supports interruption/barge-in. When a user speaks while the assistant is responding, EVI detects the interruption, stops generating and streaming the current response, and sends `user_interruption` to the client. The client must also stop local playback and clear queued assistant audio, or the user will still hear the old response. Source: https://dev.hume.ai/docs/speech-to-speech-evi/features/interruptibility

Turn detection parameters documented by Hume:

- `end_of_turn_silence_ms`: default 800 ms, range 500-3000 ms. Lower values make responses faster but increase mid-thought cut-ins; higher values give users more pause room.
- `speech_detection_threshold`: default 0.5, range 0.0-1.0. Lower values detect softer speech but can trigger on noise; higher values reduce false activation but may miss quiet speech.
- `prefix_padding_ms`: default 300 ms, range 0-1000 ms. Higher values preserve more lead-in audio.

Source: https://dev.hume.ai/docs/speech-to-speech-evi/configuration/turn-detection

Interruption parameter documented by Hume:

- `min_interruption_ms`: default 800 ms, range 50-2000 ms. Lower values make EVI yield quickly; higher values reduce false interruptions from brief backchannels or noise.

Source: https://dev.hume.ai/docs/speech-to-speech-evi/configuration/interruption

Use `verbose_transcription=true` on the WebSocket when browser playback interruption feels delayed after EVI has finished generating a response but queued audio is still playing. Hume documents that interim `user_message` events can be used to stop playback sooner, but transcript logic must ignore or specially handle `interim: true`. Source: https://dev.hume.ai/docs/speech-to-speech-evi/guides/audio

Use `pause_assistant_message` / `resume_assistant_message` when the product needs to keep listening while holding assistant responses. While paused, EVI continues to listen and transcribe; when resumed, it responds considering user input received during the pause. Source: https://dev.hume.ai/docs/speech-to-speech-evi/features/pause-responses

Production heuristics:

- For interviews, coaching, counseling-like reflection, and language learning, start with patient turn-taking (`end_of_turn_silence_ms` around 1500-2000 ms) and more resilient interruption (`min_interruption_ms` around 1000-1500 ms).
- For scheduling, short Q&A, and command interfaces, start with responsive turn-taking (`end_of_turn_silence_ms` around 500-800 ms) and sensitive interruption (`min_interruption_ms` around 100-300 ms).
- For noisy public environments, raise `speech_detection_threshold` and test with actual background noise recordings.
- Tune with recorded sessions and user-perceived measures, not only logs: "felt cut off," "hard to interrupt," "talked over me," and "waited too long" are separate failure modes.

## Prompting an empathic voice agent

EVI prompts should shape role, tone, pacing, boundaries, escalation, and speech behavior. Hume's prompting guide notes that native SLMs can generate both language and speech for realtime conversation, while supplemental LLMs often do better for complex reasoning, long prompts, and tool use. Source: https://dev.hume.ai/docs/speech-to-speech-evi/guides/prompting

Write prompts for spoken interaction:

- Use short sentences.
- Ask one question at a time.
- Prefer explicit conversation states over long paragraphs.
- Include how to respond to uncertainty, user distress, interruption, silence, and tool failure.
- Specify when to stop talking and let the user respond.
- Avoid visual UI assumptions unless the integration has a screen.

Include emotional-expression policy:

- "Use vocal expression as a conversational signal, not as a diagnosis."
- "If the user sounds frustrated, respond supportively and verify the issue verbally; do not claim to know how they feel."
- "Do not infer protected traits or mental-health conditions from voice."

Example prompt fragment:

```text
You are an AI voice assistant for Acme Support. Speak naturally, warmly, and briefly.

Conversation style:
- Keep most replies under two spoken sentences unless the user asks for detail.
- Acknowledge frustration or uncertainty without claiming to know the user's emotions.
- Ask one clarifying question at a time.
- If interrupted, stop and adapt to the user's newest request.

Safety:
- Disclose that you are an AI assistant at the start of the call.
- Do not provide legal, medical, or financial advice. Offer to connect the user to a qualified professional where appropriate.
- Before taking an account action, summarize the action and ask for confirmation.

Tools:
- Use get_order_status only after collecting an order ID.
- If a tool fails, apologize briefly, say what can still be done, and offer human handoff.
```

## Tools and backend actions

Documented facts:

- Tools are resources EVI can use to call external APIs; Configs equip EVI with those tools and other settings. Source: https://dev.hume.ai/docs/speech-to-speech-evi/features/tool-use
- Hume supports user-defined tools and built-in tools. Documented built-in tools include web search and hang-up in the tools API reference. Source: https://dev.hume.ai/reference/speech-to-speech-evi/tools/create-tool
- Tools can include fallback content, which the LLM uses when a tool errors so the conversation can continue. Source: https://dev.hume.ai/reference/speech-to-speech-evi/tools/create-tool
- Function calls can be observed through Chat history events and webhooks. Chat history includes `FUNCTION_CALL` and `FUNCTION_CALL_RESPONSE` events. Sources: https://dev.hume.ai/docs/speech-to-speech-evi/features/chat-history and https://dev.hume.ai/docs/speech-to-speech-evi/configuration/webhooks

Production tool design:

- Make tool names and descriptions literal and narrow. A voice agent has less room to recover from an accidental action than a chat UI.
- For side-effecting tools, add confirmation in both the prompt and backend. Example: `cancel_order_pending_confirmation` should not cancel until the backend receives explicit confirmation.
- Return concise, speakable tool results. A realtime voice agent should not read raw JSON or long policy text.
- Use structured error classes: unavailable, unauthorized, not_found, validation_needed, unsafe_request, provider_timeout.
- Attach a `custom_session_id` and internal user/session IDs for audit correlation when appropriate.
- For regulated workflows, perform policy enforcement outside the LLM and use a custom language model or backend post-processing if text must be constrained before speech.

## Transcript, artifacts, and observability

Use Hume artifacts deliberately:

- `chat_metadata` provides `chat_id` and `chat_group_id`. Store them only if retention, privacy policy, and product requirements allow it.
- `chat_group_id` can resume context across WebSocket sessions through `resumed_chat_group_id`; this is not available when data retention is disabled.
- Chat Events can reconstruct transcripts, actions, settings changes, user interruptions, and expression predictions when retained.
- Audio reconstruction can stitch user and assistant snippets into a single past-conversation audio file when retention is enabled.
- Webhooks can notify systems of chat started, chat ended, and tool call events; verify HMAC signatures and timestamps to prevent tampering and replay.

Sources: https://dev.hume.ai/docs/speech-to-speech-evi/features/resume-chats, https://dev.hume.ai/docs/speech-to-speech-evi/features/chat-history, https://dev.hume.ai/docs/speech-to-speech-evi/features/audio-reconstruction, https://dev.hume.ai/docs/speech-to-speech-evi/configuration/webhooks

Production logging checklist:

- Hume `chat_id`, `chat_group_id`, `config_id`, config version, EVI version
- client platform, SDK version, browser/OS, audio format, buffer cadence
- selected voice ID/provider, language/locale
- turn-detection and interruption settings
- external/supplemental LLM provider and model, if used
- tool-call start/end/error timestamps, not just final outcome
- user disclosure and consent state
- retention mode and whether audio/transcripts are stored

Do not store raw audio, transcripts, expression predictions, or reconstructed calls by default. These are sensitive artifacts. Store the minimum required for QA/compliance, redact where possible, and align with the user-facing privacy policy.

## Pricing, limits, and deployment planning

Volatile facts verified on 2026-07-10:

- Hume's pricing page lists EVI 3 and EVI 4 mini under Speech-to-speech plan access.
- Free plan: 5 included monthly EVI minutes and 1 concurrent connection.
- Starter: 40 included monthly EVI minutes, additional EVI 3 listed at $0.07/min, 5 concurrent connections.
- Creator: 200 included monthly EVI minutes, additional EVI 3 listed at $0.07/min, 5 concurrent connections.
- Pro: 1,200 included monthly EVI minutes, additional EVI 3 listed at $0.06/min, 10 concurrent connections.
- Scale: 5,000 included monthly EVI minutes, additional EVI 3 listed at $0.05/min, 20 concurrent connections.
- Business: 12,500 included monthly EVI minutes, additional EVI 3 listed at $0.04/min, 30 concurrent connections.
- Enterprise: custom included usage, custom overage, and "as much as you need" concurrent connections.

Source: https://www.hume.ai/pricing

Billing facts:

- Hume subscriptions include TTS, EVI, and Voice features together rather than separate product subscriptions.
- Overage billing applies after included usage.
- Hume-managed external LLM usage with EVI adds supplemental usage to the Hume bill.
- If the developer uses their own LLM API key or a custom language model, Hume does not charge for that LLM usage.

Source: https://dev.hume.ai/docs/resources/billing

Production heuristics:

- Estimate cost from connected conversation minutes, not just assistant speaking time.
- Budget separate external LLM cost where the plan uses Hume-managed external LLMs or a developer-owned LLM key.
- Load-test concurrent sessions before launch. Concurrent-connection limits are product limits, not just billing labels.
- Design graceful admission control: queue, fallback to human, scheduled callback, or text chat when concurrency is exhausted.

## Privacy, consent, safety, and rights

Documented facts:

- Hume documents zero data retention for the EVI API as an option that turns off storage of chat histories/transcripts or voice recordings; API usage metadata remains stored. Source: https://dev.hume.ai/docs/resources/privacy
- Hume documents a training-data opt-out for anonymized EVI API interaction data. Source: https://dev.hume.ai/docs/resources/privacy
- Hume states HIPAA compliance features exist and says BAA/DPA requests should go through Hume; the Terms require express written agreement for HIPAA covered entities or business associates. Sources: https://dev.hume.ai/docs/resources/privacy and https://www.hume.ai/terms-of-use
- Hume's Acceptable Use Policy prohibits impersonation without permission and voice outputs that replicate others without clear affirmative consent. It also requires disclosure when AI agents are being used in interactions and qualified professional review for critical legal, financial, or medical advice. Source: https://www.hume.ai/acceptable-use-policy
- Free and Starter plan use is non-commercial under Hume's Terms; Creator plan and above can be used commercially subject to policy compliance. Source: https://www.hume.ai/terms-of-use
- Hume's Voice Cloning docs instruct users to upload only voice samples for which they have necessary rights or consent and to confirm legal agreements when creating a clone. Source: https://dev.hume.ai/docs/voice/voice-cloning

Production requirements:

- Disclose the AI agent at call/chat start.
- Obtain consent before recording, storing, analyzing, reconstructing, or reusing voice data where required by law or product policy.
- For voice clones, require affirmative authorization and keep evidence of consent and permitted use.
- Provide a human handoff path for sensitive, high-stakes, or user-distress scenarios.
- Avoid manipulating users based on inferred emotion. Use expression signals to improve clarity and support, not to exploit vulnerability.
- Do not infer protected attributes, health status, or mental state from voice.
- Review regional call-recording, biometric, privacy, telemarketing, and accessibility rules before launch.

## Production QA

A strong EVI QA plan tests more than "does it answer." Include:

- Conversation flow: first greeting, disclosure, expected task completion, clarification, refusal, handoff, ending.
- Turn-taking: mid-thought pauses, fast speakers, long pauses, overlapping speech, backchannels ("uh huh"), and user interruption during assistant audio.
- Audio: laptop mic, phone mic, earbuds, speakers with echo, noisy room, low volume, browser permission denial, microphone unplug/revocation.
- Latency: time from user stop to first assistant audio, assistant speech start after tool result, interruption-to-silence delay.
- Tool use: success, timeout, invalid arguments, unsafe action, unauthorized user, side-effect confirmation.
- Privacy modes: retention on/off, training opt-out, resume unavailable under zero retention, chat-history and audio-reconstruction behavior.
- Safety: AI disclosure, no emotion diagnosis, no high-stakes advice without professional review, no unconsented voice impersonation.
- Cost and scale: included minutes, overage, external LLM costs, concurrency limits, call admission behavior.
- Localization: if using EVI 4-mini, test every target language with native speakers and culturally specific conversation norms.

Review failures as system issues:

- If EVI interrupts too early, tune turn detection and client playback; do not only rewrite prompts.
- If users cannot interrupt, handle `user_interruption` and `user_message` locally and clear audio queues.
- If tools produce long spoken responses, shorten tool results and prompt the LLM to summarize.
- If latency spikes with external LLMs, compare TTFT by provider/model and reduce prompt/tool overhead.
- If expression signals seem wrong for a population, collect deployment-specific validation data and avoid emotion-label conclusions.

## Example: English support agent with account tools

This example is for a web support agent where users ask order-status and return-policy questions. It uses EVI 3 because the deployment is English-only and wants quick, natural support responses; it uses a supplemental LLM because tool calling is required.

Config choices:

```json
{
  "evi_version": "3",
  "name": "acme-support-agent",
  "voice": {
    "id": "VOICE_LIBRARY_OR_CUSTOM_VOICE_ID",
    "provider": "HUME_AI"
  },
  "turn_detection": {
    "end_of_turn_silence_ms": 800,
    "speech_detection_threshold": 0.5,
    "prefix_padding_ms": 300
  },
  "interruption": {
    "min_interruption_ms": 250
  },
  "timeouts": {
    "inactivity_timeout": 120,
    "max_duration_timeout": 1800
  }
}
```

System prompt:

```text
You are Acme's AI voice support assistant. At the start, say you are an AI assistant.
Speak warmly and briefly. Use one or two short sentences unless the user asks for detail.

Use vocal tone to show attentiveness, but never claim to know the user's feelings.
If the user sounds upset or frustrated, say: "I'm sorry this has been frustrating. Let's work through it."

Before using order_status, ask for the order ID if missing.
Before taking any account-changing action, summarize it and ask for confirmation.
If a tool fails, explain the problem in plain language and offer human handoff.
Do not provide legal, medical, or financial advice.
```

Client requirements:

- Use the React SDK or TypeScript SDK in the browser.
- Open the WebSocket before recording.
- Start `MediaRecorder` with 100 ms web chunks.
- Queue `audio_output` playback.
- On `user_interruption` or final/interim `user_message`, stop current playback and clear queued assistant audio.
- Use `verbose_transcription=true` if interruption feels delayed while queued audio is playing.

Expected result:

- The assistant speaks quickly, can be interrupted, uses order tools only when needed, and does not make unsupported claims about emotions.

Likely failures:

- False barge-ins in noisy rooms: raise `speech_detection_threshold` or `min_interruption_ms`.
- Slow response after tool calls: shorten tool result payloads and choose a lower-TTFT supplemental LLM.
- User hears old audio after interrupting: fix client queue clearing; the server has already stopped generating.

## Example: multilingual travel concierge

This example is for a web/mobile travel concierge that must support Spanish, French, German, and Japanese. It uses EVI 4-mini because those target languages are in Hume's documented EVI 4-mini language list; it requires a supplemental LLM because EVI 4-mini requires one.

Config choices:

```json
{
  "evi_version": "4-mini",
  "name": "multilingual-travel-concierge",
  "voice": {
    "id": "CUSTOM_OR_LIBRARY_VOICE_ID",
    "provider": "CUSTOM_VOICE"
  },
  "turn_detection": {
    "end_of_turn_silence_ms": 1000,
    "speech_detection_threshold": 0.5
  },
  "interruption": {
    "min_interruption_ms": 400
  }
}
```

Prompt fragment:

```text
You are an AI travel concierge. Begin by disclosing that you are an AI assistant.
Reply in the user's language unless they ask to switch languages.
Ask one question at a time and keep replies concise enough for speech.
Never invent booking confirmations. Use tools for availability and booking-state checks.
If the user sounds stressed, slow down and confirm the next step without claiming to know their emotion.
```

Session settings example:

```json
{
  "type": "session_settings",
  "variables": {
    "traveler_name": "Mina",
    "preferred_currency": "EUR"
  },
  "context": {
    "type": "persistent",
    "text": "The traveler is comparing flight options for September and wants refundable fares only."
  },
  "custom_session_id": "user-742-session-2026-07-10"
}
```

Expected result:

- The assistant maintains the selected language, uses concise spoken turns, and relies on booking tools for factual inventory.

Likely failures:

- Long external-LLM responses: add stricter spoken-length instructions and summarize tool results.
- Voice mismatch by language: create or select voices prompted/tested in each target language.
- Cultural mismatch: test with native speakers in every launch market.

## Example: phone calling through a telephony provider

This example is for phone support where the caller uses the public telephone network. Hume documents a Twilio integration for EVI, and its audio guide warns that telephony `mulaw` audio is not directly supported by EVI and must be converted.

Architecture:

```text
Phone caller
  -> telephony media stream
  -> server bridge: auth, disclosure state, audio conversion, logging policy
  -> Hume EVI WebSocket
  -> server bridge converts/routes assistant audio
  -> caller
```

Design choices:

- Use EVI event messages for a first-turn AI disclosure and an inactivity check-in.
- Convert telephony audio to a supported format before sending to EVI.
- Keep `max_duration_timeout` within product and plan expectations.
- Use Hume webhooks for chat started/ended/tool-call monitoring, and verify webhook HMAC signature and timestamp.
- If recording or retaining calls, explicitly align with consent law and the product privacy notice.

Expected result:

- The caller hears an AI disclosure, the agent can be interrupted, and support logs can correlate call events with internal case IDs.

Likely failures:

- Distorted or sped-up audio: sample-rate or encoding mismatch.
- Frequent interruptions from line noise: raise interruption duration and speech detection threshold.
- Missing audit records under zero retention: expected; choose retention mode deliberately and disclose it.


