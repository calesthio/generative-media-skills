---
name: openai-realtime-voice
description: Build production OpenAI Realtime voice agents and low-latency spoken interactions with live audio sessions, WebRTC or WebSocket transport, voice activity detection, tool/function calling, prompt design, logging, consent, privacy, safety, latency, and cost controls. Use for speech-to-speech agents and live voice UX; do not use for separate request-based transcription, text-to-speech, or offline audio generation work.
---

# OpenAI Realtime voice

Use this skill when the deliverable is a live spoken interaction: a browser voice assistant, phone-like agent, low-latency speech-to-speech support flow, guided interview, tutoring conversation, live kiosk, or realtime voice UI that listens, reasons, speaks, interrupts, and may call tools.

Do not use this skill for batch speech-to-text, offline TTS, voiceover generation, audio editing, dubbing, music, or file-based audio tasks. Those belong to the separate OpenAI audio/request APIs or other speech/audio skills. The boundary is simple: if a persistent realtime session and turn-taking behavior are part of the product, use this skill; if the job is "turn this file/text into text/audio," do not.

All OpenAI API facts below were verified against first-party OpenAI documentation on 2026-07-10. Re-check model identifiers, prices, session limits, voices, API object fields, data retention, and policy requirements before production release because Realtime surfaces change quickly.

## Source-grounded facts to carry into every design

Documented facts:

- OpenAI positions Realtime sessions as best for live audio that needs low latency; request-based audio APIs are best for files, bounded requests, or generated speech that does not need a live session. Source: [Realtime and audio overview](https://developers.openai.com/api/docs/guides/realtime).
- A voice-agent session is for applications where the model should respond to the user, call tools, and manage conversation state on `/v1/realtime`. Translation and transcription sessions are separate Realtime session types. Source: [Realtime and audio overview](https://developers.openai.com/api/docs/guides/realtime).
- OpenAI's voice-agent guide distinguishes speech-to-speech live audio sessions from chained STT -> text reasoning -> TTS pipelines. Live audio is the starting point for barge-in, low first-audio latency, natural turn taking, and realtime tool use. Source: [Voice agents](https://developers.openai.com/api/docs/guides/voice-agents).
- The documented browser path is WebRTC, preferably via Agents SDK helpers such as `RealtimeAgent` and `RealtimeSession`; server-to-server integrations use WebSocket. Source: [Voice agents](https://developers.openai.com/api/docs/guides/voice-agents), [WebRTC guide](https://developers.openai.com/api/docs/guides/realtime-webrtc), [WebSocket guide](https://developers.openai.com/api/docs/guides/realtime-websocket).
- A Realtime speech-to-speech session contains a Session object, a Conversation, and Responses. The Session controls model, voice, and configuration; the Conversation contains user and model Items; Responses are model-generated audio or text Items. Source: [Realtime conversations](https://developers.openai.com/api/docs/guides/realtime-conversations).
- After the server sends `session.created`, the client can use `session.update`. Most session properties can be updated at any time, but the voice cannot be changed after the model has responded with audio once in the session. The documented maximum Realtime session duration is 60 minutes. Source: [Realtime conversations](https://developers.openai.com/api/docs/guides/realtime-conversations).
- For WebSocket audio, the client manually sends base64-encoded audio through input-audio-buffer events; WebRTC handles much of the media transport. Source: [Realtime conversations](https://developers.openai.com/api/docs/guides/realtime-conversations).
- VAD is enabled by default in speech-to-speech Realtime sessions and can be configured at `session.audio.input.turn_detection`. Documented VAD modes are `server_vad` and `semantic_vad`; server VAD can tune threshold, prefix padding, and silence duration. Source: [Voice activity detection](https://developers.openai.com/api/docs/guides/realtime-vad).
- Realtime sessions can use function tools executed by the application, MCP tools exposed by a remote MCP server, and built-in connectors. Tools may be attached at the session level or for one response. Source: [Realtime with tools](https://developers.openai.com/api/docs/guides/realtime-mcp).
- Realtime voice-agent sessions accrue input and output tokens across text, audio, and image modalities; translation and transcription streaming sessions are duration-billed. Later conversational turns cost more because the whole server-side conversation is input to each Response. OpenAI documents audio-token accounting as 1 token per 100 ms for user-message audio and 1 token per 50 ms for assistant-message audio. Source: [Managing costs](https://developers.openai.com/api/docs/guides/realtime-costs).
- Input-audio transcription is a separate ASR process from the Realtime model's native audio understanding, and OpenAI warns the transcript may diverge from the model's interpretation. Treat transcripts as observability and accessibility artifacts, not as the exact reasoning input. Source: [Realtime API reference](https://developers.openai.com/api/reference/resources/realtime).
- OpenAI states that data sent to the API is not used to train or improve models unless the organization explicitly opts in. Source: [Data controls in the OpenAI platform](https://developers.openai.com/api/docs/guides/your-data).
- OpenAI's usage policies and safety best practices still apply to Realtime voice experiences, including harmful-content, impersonation, privacy, high-impact decision, and user-protection constraints. Sources: [Usage policies](https://openai.com/policies/usage-policies/), [Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices).

Production heuristics in this skill are not OpenAI promises. They are practical design guidance for agents building voice products from the documented API surface.

## Architecture choice

Choose the architecture before writing prompts or code.

Use a speech-to-speech Realtime voice-agent session when:

- latency and natural conversational flow are the product;
- users should be able to interrupt the assistant;
- the assistant needs tool calls while staying in a live audio exchange;
- the voice behavior, timing, and turn-taking are part of quality;
- the session can safely carry conversational state.

Use a chained STT -> text agent -> TTS pipeline instead when:

- every tool action must be explicitly sequenced by the application;
- deterministic transcripts are more important than natural speech-to-speech timing;
- the existing product already has a text agent and voice is an input/output layer;
- compliance requires storing, inspecting, or approving text before speech synthesis;
- batch processing, files, long recordings, narration, or voiceover is the real job.

Use Realtime transcription mode only when the product needs streaming transcript deltas and no model-generated voice response. Use Realtime translation only when the product is an interpreter. Do not smuggle those into a voice-agent architecture.

## Session and transport patterns

Design every implementation around three boundaries: client media, trusted server, and OpenAI Realtime session.

For browser or mobile:

1. Capture microphone audio locally after explicit user consent.
2. Ask your trusted server to start or authorize a Realtime session.
3. Use WebRTC for media and data channel events whenever possible.
4. Keep the standard OpenAI API key on the server. If using an ephemeral key flow, issue short-lived credentials only for the intended session.
5. Render assistant audio with visible speaking/listening state and an obvious stop/mute control.

For server-to-server:

1. Keep audio capture and playback on your controlled infrastructure, telephony bridge, or backend process.
2. Connect to `wss://api.openai.com/v1/realtime?model=...` with a standard API key only from the secure server.
3. Send session updates, input-audio-buffer events, and tool results explicitly.
4. Add a stable privacy-preserving safety identifier header when your application assigns one, as OpenAI documents for WebSocket connections.
5. Log event IDs, item IDs, response IDs, tool calls, and user-visible outcomes without logging raw secrets or unnecessary audio.

Do not put a standard API key in a browser, mobile app, desktop package, or downloadable client. Treat WebSocket-from-browser as a special-case prototype unless the authentication and media tradeoffs are deliberately accepted.

## Model, voice, and session configuration

Verified on 2026-07-10: OpenAI's current voice-agent examples use `gpt-realtime-2.1`. Older or alternate realtime model names may exist in docs and model pages; select the model from the current model reference at implementation time and record the exact model in logs and artifacts.

Minimum session decisions to log before launch:

- `model`: exact Realtime model identifier and verification date;
- `transport`: WebRTC, WebSocket, or SIP/telephony bridge if applicable;
- `session_type`: voice agent, transcription, or translation;
- `voice`: exact voice identifier; record that voice cannot be changed after the first audio response in a session;
- `modalities`: whether output is audio, text, or both;
- `input_audio_format` and `output_audio_format` when manually handling audio;
- `turn_detection`: `server_vad`, `semantic_vad`, or disabled/manual;
- `input_audio_transcription`: whether enabled, which ASR model, and whether transcripts are user-visible;
- `tools`: tool list, schemas, execution owner, approval policy, and side effects;
- `retention/logging`: whether raw audio, transcripts, events, and tool payloads are stored, for how long, and who can access them.

Heuristic: set the voice at session creation, not after connection. Treat a voice change request mid-call as "start a new session with the new voice" unless current docs explicitly change the documented immutability after first audio.

## Turn-taking and interruption design

Voice UX fails when the system does not make turn state visible. Implement the state machine explicitly:

- idle: microphone permission not active or call not started;
- listening: user audio is being streamed;
- user_speaking: VAD detected speech start;
- thinking: user turn committed and a Response is being generated;
- assistant_speaking: audio output is streaming;
- interrupted: user barge-in or UI stop has cancelled/trimmed the assistant output;
- tool_pending: model requested an external action;
- handoff_or_escalation: human or alternate workflow needed;
- ended: session closed, summary and artifacts sealed.

Use `server_vad` for a default conversational assistant in normal rooms. Tune:

- lower `silence_duration_ms` when users expect quick back-and-forth and interruptions are common;
- higher `silence_duration_ms` for users who pause mid-thought, accessibility contexts, language learners, or complex support cases;
- higher `threshold` in noisy rooms;
- enough `prefix_padding_ms` to avoid clipping first syllables.

Consider `semantic_vad` when silence-based chunking cuts off users who use long pauses or when phrase completeness matters more than speed. Test carefully with real accents, background noise, and domain vocabulary.

Disable automatic VAD and commit turns manually only when the UI has a deliberate push-to-talk or operator-controlled workflow. If VAD is off, the application owns turn boundaries and must avoid sending accidental background speech as user input.

Interruption rules:

- Provide a visible "stop speaking" or "mute assistant" control.
- Let user speech interrupt long assistant audio unless the product has a legal or safety reason not to.
- After interruption, summarize only what was actually said; do not assume the user heard the remainder.
- For tool calls, distinguish interrupting speech playback from cancelling a side-effecting tool action. Side effects require separate cancellation semantics.

## Prompt and instruction design for spoken agents

Realtime voice prompts need to constrain behavior that text prompts often leave implicit.

Include these instruction blocks when relevant:

1. Role and objective: what the agent helps with and what it must not handle.
2. Voice persona: warmth, formality, pace, concision, and filler policy.
3. Turn length: maximum sentence count or seconds per answer.
4. Conversation repair: how to ask for repeats, clarify uncertain audio, and recover from background noise.
5. Tool policy: when to call tools, when to ask permission, and how to describe waiting states.
6. Safety boundaries: regulated advice, emergencies, minors, identity verification, financial/legal/medical disclaimers.
7. Privacy behavior: never ask for sensitive information unless necessary; mask or avoid reading secrets aloud.
8. Language policy: supported languages, code-switching, pronunciation, and what to do when a user switches language.
9. Escalation and handoff: when to involve a human or end the session.
10. Output style: no markdown, no lists unless verbally natural, no "as an AI language model," and no pretending to have completed a tool action before the tool result arrives.

Spoken-agent heuristics:

- Prefer short answers: one direct answer plus one follow-up question.
- Avoid dense enumerations; if the answer has more than three steps, ask whether to continue.
- Use ear-friendly confirmations: "I found the order. It shipped yesterday." not "The tool returned status equal to shipped."
- Do not over-apologize; repeated apologies feel slow in voice.
- For uncertain ASR or ambiguous names, confirm the critical field: "Did you say order 3917?"
- For emotional conversations, acknowledge briefly, then move to the useful next action.
- For tool latency, narrate state once: "I'll check that now." Avoid filling silence with speculation.

## Tool and function calling

Attach tools only when the voice agent needs current data or side effects. Tools are not a substitute for prompt instructions.

Use application-executed function tools when:

- your app owns private business logic, credentials, or policy checks;
- a human approval gate may be needed;
- the action changes state, spends money, sends messages, books appointments, unlocks doors, or modifies records;
- the tool result needs redaction before being spoken.

Use MCP or connector tools only when the organization has approved the remote tool server/connector, the authorization boundary is understood, and logging includes what data may leave the application boundary.

Tool design rules:

- Keep schemas small and concrete. Voice users correct mistakes faster when the tool asks for one missing field.
- Mark required fields accurately; do not force the model to invent IDs.
- Validate arguments server-side even if the model emits JSON matching schema.
- Return concise, speech-ready results plus machine-readable fields for state.
- Never let the model perform irreversible actions without an application-side approval rule.
- For payments, contracts, medical scheduling, account changes, or legal/financial decisions, ask for explicit confirmation immediately before the side effect.
- If a tool fails, say what happened and offer one next step; do not expose stack traces.

Example tool approval policy:

```text
Read-only tools may run automatically after user intent is clear.
Drafting tools may create but not send.
Side-effecting tools require explicit user confirmation in the same turn as execution.
High-impact tools require human operator approval outside the model.
The assistant must never claim completion until function_call_output confirms success.
```

## Latency, cost, and context controls

Latency budget is an experience requirement, not just an engineering metric. Track at least:

- microphone permission to connection ready;
- speech start to VAD speech_started;
- speech stop to response creation;
- response creation to first assistant audio;
- first audio to final audio;
- tool call emitted to tool result returned;
- interruption command to audio stop.

Cost controls:

- Keep the system instructions compact but complete; long instructions recur in session context.
- Summarize or truncate stale conversation Items when a long session does not need verbatim history.
- Avoid creating Responses for non-speech or background noise; rely on VAD and UI mute.
- Use tool calls to fetch only necessary fields.
- End idle sessions promptly.
- Decide whether transcripts are necessary; input transcription is separately billed according to the ASR model pricing, not the Realtime model pricing.
- Estimate audio token pressure using OpenAI's documented rule of thumb: user audio is 1 token per 100 ms and assistant audio is 1 token per 50 ms, plus special-token variation.

Heuristic: in production dashboards, split cost by session, user turn, assistant audio duration, tool time, and abandoned/idle time. Voice teams often discover that long assistant monologues are both the most expensive and the least usable part of the UX.

## Consent, rights, privacy, and safety

Before capturing voice:

- Show clear consent for microphone use and, if applicable, recording or transcript storage.
- Say whether a human may review audio/transcripts.
- Provide mute, stop, delete/end-session, and human-support paths when appropriate.
- Avoid collecting children’s personal data unless legal/compliance controls are in place.
- Avoid biometric voice identification unless the product has explicit consent, legal basis, and provider support for the specific use.

For generated voice:

- Do not present the agent as a real human unless that is true and disclosed.
- Do not impersonate a person, celebrity, employee, clinician, or public official.
- Do not clone or imitate a voice unless rights and consent are documented under the applicable voice policy and local law.
- If the agent represents a brand, make the brand role clear.

For privacy:

- Minimize raw audio retention. Prefer event metadata and redacted transcripts when enough for QA.
- Never log API keys, ephemeral client secrets, Authorization headers, connector tokens, or unredacted secrets spoken by users.
- Treat transcripts as sensitive because they may contain PII even when audio is not stored.
- If using tools/connectors, document what user audio-derived data is sent to each external system.
- Provide retention and deletion behavior in the application, not just in internal docs.

For safety:

- Add domain-specific refusal and escalation behavior for medical, legal, financial, employment, housing, education, emergency, and self-harm contexts.
- Use stable privacy-preserving user identifiers where OpenAI recommends safety identifiers.
- Evaluate with adversarial audio: background voices, prompt injection spoken by a third party, children nearby, slurs, emotional distress, and tool-abuse attempts.

## Approval, logging, and artifact custody

For any production voice agent, create an auditable run record. At minimum, store:

- date of model/API verification;
- model, voice, transport, session type, and session configuration;
- prompt/instructions version;
- VAD configuration;
- tool schemas, tool approval policy, and connector inventory;
- user consent copy shown in UI;
- retention policy for raw audio, transcripts, events, tool payloads, and summaries;
- test matrix and results;
- known limitations and escalation routes.

Per session, log:

- session ID or application correlation ID;
- user safety identifier or internal user ID hash, not raw PII when avoidable;
- timestamps for connection, speech events, responses, interruptions, tool calls, and close;
- token/duration usage from API events;
- errors and recovery action;
- artifact custody: where audio/transcript/event logs are stored, retention deadline, and access class.

Never store evaluation or scoring artifacts in production agent context. Keep product prompts, test fixtures, and scoring materials separated.

## Complete example: browser customer-support voice agent

Example intent: a logged-in ecommerce user can ask about order status by voice, interrupt the assistant, and request a human handoff. The assistant may look up orders but cannot cancel or refund without explicit confirmation and server approval.

Documented API choices verified 2026-07-10:

- session type: voice-agent Realtime session;
- model: `gpt-realtime-2.1` if still current in model docs at build time;
- transport: browser WebRTC via Agents SDK helpers;
- VAD: `server_vad`, tuned after noisy-room tests;
- tools: application-executed `lookup_order`, `create_refund_draft`, `request_human_handoff`;
- logging: event metadata and redacted transcripts retained; raw audio off by default unless user opts into QA review.

Voice-agent instructions:

```text
# Role & objective
You are Acme Retail's voice support assistant. Help authenticated customers understand orders, shipping, returns, and simple account questions.

# Spoken style
Use a warm, calm retail-support voice. Keep answers to 1-2 short sentences, then ask one useful follow-up question. Do not use markdown or numbered lists unless the user asks for steps.

# Audio uncertainty
If a name, order number, address, or amount is uncertain, ask the user to confirm it before using a tool. If background noise may have changed intent, ask a clarifying question.

# Tools
Use lookup_order for order status. It is read-only and may run automatically after intent is clear.
Use create_refund_draft only after explaining the refund reason you heard. It creates a draft, not a refund.
Before any cancellation, refund, message send, or account change, ask for explicit confirmation. Never say an action is complete until the tool result says success.

# Privacy
Do not read full addresses, payment details, tokens, or secrets aloud. Mask sensitive fields. If the user starts sharing a card number or password, stop them and explain that you do not need it.

# Boundaries
For threats, self-harm, legal claims, medical issues, or harassment, move to the approved escalation route. If the user wants a human, call request_human_handoff.
```

Server-side ephemeral session creation pattern:

```ts
// Example only. Re-check current OpenAI SDK and REST shapes before production.
import express from "express";
import OpenAI from "openai";

const app = express();
app.use(express.json());
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.post("/voice/session", requireLoggedInUser, async (req, res) => {
  const realtimeSession = await openai.beta.realtime.sessions.create({
    model: "gpt-realtime-2.1",
    voice: "alloy",
    instructions: SUPPORT_VOICE_INSTRUCTIONS,
    audio: {
      input: {
        turn_detection: {
          type: "server_vad",
          threshold: 0.55,
          prefix_padding_ms: 300,
          silence_duration_ms: 650
        }
      }
    },
    tools: [
      {
        type: "function",
        name: "lookup_order",
        description: "Look up an authenticated customer's order status.",
        parameters: {
          type: "object",
          properties: {
            order_number: { type: "string" }
          },
          required: ["order_number"]
        }
      }
    ]
  });

  audit.log("realtime_session_created", {
    user_hash: hashUser(req.user.id),
    model: "gpt-realtime-2.1",
    voice: "alloy",
    raw_audio_retention: "off"
  });

  res.json({ client_secret: realtimeSession.client_secret });
});
```

Browser connection pattern:

```ts
// Example only. Prefer current Agents SDK docs at implementation time.
import { RealtimeAgent, RealtimeSession } from "@openai/agents/realtime";

const agent = new RealtimeAgent({
  name: "Acme Support",
  instructions: SUPPORT_VOICE_INSTRUCTIONS,
});

const session = new RealtimeSession(agent, {
  model: "gpt-realtime-2.1",
});

async function startVoice() {
  await showConsentAndGetMicPermission();
  const auth = await fetch("/voice/session", { method: "POST" }).then(r => r.json());
  await session.connect({ apiKey: auth.client_secret.value });
  ui.setState("listening");
}

session.on("transport_event", (event) => {
  auditClientEvent(event);
  updateVoiceUI(event);
});
```

Why this example is structured this way:

- The browser never sees the standard API key.
- The assistant has a narrow role and short spoken responses.
- Tool side effects are separated from read-only lookup.
- Consent and retention are explicit.
- VAD is configured but expected to be tested against real audio.

Likely failure modes:

- The assistant reads sensitive order details aloud.
- VAD clips a hesitant user's order number.
- A tool returns too much JSON and the assistant speaks it verbatim.
- The frontend logs ephemeral secrets.
- The model says a refund happened when only a draft was created.

## Complete example: server-side interview screener

Example intent: a research team runs a consented voice interview for product feedback. The agent asks prepared questions, follows up naturally, tags answers, and calls `save_answer` after each section. It must not make claims that the user will receive compensation unless the backend confirms eligibility.

Architecture:

- server-to-server WebSocket because the research platform records through controlled infrastructure;
- VAD: `semantic_vad` if current docs and model support it for the selected session, otherwise tuned `server_vad`;
- output: audio plus optional text summaries for moderator dashboard;
- raw audio retained 14 days only if the user consents; redacted transcript retained for study analysis.

Instructions:

```text
# Role & objective
You are a voice research moderator. Run a 12-minute interview about a beta productivity app. Ask one question at a time, listen actively, and save concise answer notes after each topic.

# Interview method
Use the approved topic order: onboarding, first useful moment, confusing moments, trust concerns, pricing reaction, final recommendation.
Ask one follow-up when an answer is vague. Do not argue, persuade, or defend the product.

# Spoken style
Sound curious and neutral. Keep your turns under 12 seconds. Leave space for the participant to think.

# Consent and privacy
If the participant asks about recording, say: "We record only if you opted in on the consent screen. You can stop at any time." Do not request passwords, payment details, or medical information.

# Tools
After each topic, call save_answer with topic, concise_summary, notable_quote_if_any, and sentiment. Do not invent quotes. If you are uncertain, omit the quote.
Call flag_for_human_review if the participant withdraws consent, reports a safety issue, or asks to delete data.
```

Server WebSocket pattern:

```ts
// Example only. Match event names and fields to the current Realtime API reference.
import WebSocket from "ws";

const ws = new WebSocket("wss://api.openai.com/v1/realtime?model=gpt-realtime-2.1", {
  headers: {
    Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
    "OpenAI-Safety-Identifier": hashParticipant(participantId),
  },
});

ws.on("open", () => {
  ws.send(JSON.stringify({
    type: "session.update",
    session: {
      type: "realtime",
      model: "gpt-realtime-2.1",
      voice: "alloy",
      instructions: INTERVIEW_INSTRUCTIONS,
      audio: {
        input: {
          turn_detection: {
            type: "server_vad",
            threshold: 0.5,
            prefix_padding_ms: 400,
            silence_duration_ms: 900
          }
        }
      },
      tools: [{
        type: "function",
        name: "save_answer",
        description: "Save a concise research note for the current interview topic.",
        parameters: {
          type: "object",
          properties: {
            topic: { type: "string" },
            concise_summary: { type: "string" },
            notable_quote_if_any: { type: "string" },
            sentiment: { type: "string", enum: ["positive", "neutral", "negative", "mixed"] }
          },
          required: ["topic", "concise_summary", "sentiment"]
        }
      }]
    }
  }));
});

ws.on("message", async (raw) => {
  const event = JSON.parse(raw.toString());
  logRealtimeEventMetadata(event);

  if (event.type === "response.function_call_arguments.done") {
    const result = await executeApprovedTool(event.name, event.arguments);
    ws.send(JSON.stringify({
      type: "conversation.item.create",
      item: {
        type: "function_call_output",
        call_id: event.call_id,
        output: JSON.stringify(result)
      }
    }));
    ws.send(JSON.stringify({ type: "response.create" }));
  }
});
```

Why this example is structured this way:

- The prompt enforces a research method, not a support persona.
- Longer `silence_duration_ms` gives participants thinking time.
- `save_answer` is additive and auditable, not a hidden decision engine.
- Consent withdrawal is a first-class tool path.

Likely failure modes:

- The assistant fills silence too quickly and biases the interview.
- It saves paraphrases as quotes.
- It misses consent withdrawal because that path was not tested.
- It produces a polished summary but not evidence-linked research notes.

## Review checklist before shipping

Block release until these are true:

- The model, API fields, price assumptions, session duration, voice list, transport path, and policy constraints have been re-verified against OpenAI docs with a date.
- The architecture choice is documented and separated from file-based OpenAI audio APIs.
- Standard API keys remain server-side; client credentials are ephemeral or otherwise scoped.
- The user sees microphone and recording/transcription consent before audio capture.
- The UI has mute/stop/end controls and visible listening/speaking states.
- VAD has been tested with real microphones, accents, noise, crosstalk, pauses, and interruptions.
- Tool schemas are minimal, validated server-side, and have approval gates for side effects.
- Logs capture enough for debugging, abuse review, and cost analysis without retaining unnecessary raw audio or secrets.
- Safety, escalation, and human handoff behavior has been tested by adversarial voice scenarios.
- Cost dashboards show per-session and per-turn usage, including audio tokens/duration and transcription costs.
- The team has a runbook for session failures, model unavailability, tool failure, stuck audio, user withdrawal, and data deletion requests.

## Quick troubleshooting

If the agent talks over users:

- Increase `silence_duration_ms`, consider semantic VAD, shorten assistant answers, and ensure barge-in cancels audio playback.

If first syllables are clipped:

- Increase `prefix_padding_ms`, inspect client microphone buffering, and test with quiet speakers.

If the agent is slow:

- Measure first-audio latency separately from total answer length, reduce prompt bloat, shorten spoken responses, reduce unnecessary tools, and use WebRTC for browser/mobile.

If transcripts disagree with what the model did:

- Remember input transcription is a separate ASR process; use transcript for observability, not as proof of the model's exact audio understanding.

If costs rise over the session:

- Check conversation growth, long assistant audio, unnecessary Responses, background noise, and transcript settings.

If a tool action is unsafe:

- Move approval outside the model, require explicit confirmation, narrow the schema, and return a speech-safe tool result.

If users distrust the voice:

- Disclose that it is an AI voice agent, state what is recorded or stored, avoid synthetic-human deception, and offer a human path.
