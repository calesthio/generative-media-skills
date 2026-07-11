# Evaluation: openai-realtime-voice

Do not show this file to evaluated agents. Give evaluated agents only the user task and `SKILL.md`. Score the captured response with this answer key. Total: 100 points.

## 1. Scope and architecture boundary — 12 points

Question: A user asks for "an OpenAI voice feature where website visitors can talk to a support agent, interrupt it, and have it check order status." What architecture should the agent propose, and what should it explicitly not confuse this with?

Expected answer:

- Proposes a speech-to-speech OpenAI Realtime voice-agent session for low-latency conversation, barge-in, turn-taking, and tool use. 4 pts
- Recommends browser/mobile WebRTC or Agents SDK helper path with a trusted server for session authorization. 2 pts
- Distinguishes this from request-based transcription, text-to-speech, voiceover, file audio, or a generic OpenAI audio batch API. 3 pts
- Notes that chained STT -> text agent -> TTS is an alternative only when deterministic text control or existing text-agent integration is more important than natural realtime flow. 2 pts
- Mentions re-verifying current model/API facts before launch. 1 pt

Critical failures: treating this as only TTS; suggesting a standard API key in the browser; omitting the Realtime session concept.

## 2. Session facts and lifecycle — 12 points

Question: List the essential Realtime session facts a production design must account for.

Expected answer:

- Session object controls model, voice, and configuration; Conversation contains Items; Responses produce model audio/text Items. 3 pts
- `session.created` and `session.update` are part of lifecycle/configuration. 2 pts
- Most session properties can update during a session but voice cannot change after the first model audio response, per documented behavior. 2 pts
- Maximum documented session duration is 60 minutes, with a dated/reverify caveat. 2 pts
- WebSocket audio requires explicit base64/input-audio-buffer handling; WebRTC handles much of media transport. 2 pts
- Input transcription is separate ASR and may diverge from the model's native audio interpretation. 1 pt

Critical failures: claiming transcripts are the exact model input; claiming voice can freely change mid-call after audio output; omitting session duration entirely.

## 3. Transport and authentication — 10 points

Scenario: A developer proposes connecting a React app directly to Realtime over WebSocket using `OPENAI_API_KEY`.

Expected response:

- Rejects exposing a standard API key in browser/mobile/downloadable clients. 3 pts
- Recommends WebRTC for browser/mobile for more robust client media performance. 2 pts
- Places standard API key on a trusted server that creates/authorizes sessions or issues scoped ephemeral credentials. 2 pts
- Allows WebSocket as the normal server-to-server transport. 1 pt
- Mentions safety identifiers or privacy-preserving user correlation when applicable. 1 pt
- Advises logging connection/session decisions without logging secrets. 1 pt

Critical failures: approving standard API key exposure; presenting WebSocket browser direct as the default production choice.

## 4. Turn-taking and VAD — 12 points

Scenario: Users complain the agent cuts them off in a noisy warehouse and often misses the first word.

Expected answer:

- Identifies VAD/turn-detection tuning as a primary area: `server_vad`, `semantic_vad`, or manual/push-to-talk depending on UX. 2 pts
- Explains documented VAD modes: `server_vad` uses silence; `semantic_vad` uses model judgment of utterance completion. 2 pts
- Raises threshold for noisy environments. 2 pts
- Increases prefix padding to avoid clipped first syllables. 2 pts
- Adjusts silence duration: shorter for speed, longer for hesitant/pausing users; here likely longer and tested. 2 pts
- Adds UI state and interruption/stop controls rather than relying on invisible behavior. 1 pt
- Calls for real audio tests with accents, noise, crosstalk, and microphones. 1 pt

Critical failures: only changing the prompt; disabling VAD without taking ownership of manual commits; ignoring UI state.

## 5. Prompt design for spoken agents — 10 points

Task: Draft the major instruction categories for a Realtime voice support assistant.

Expected answer:

- Includes role/objective and domain boundaries. 1.5 pts
- Specifies spoken style: short turns, pace/tone, no markdown-like output. 1.5 pts
- Includes audio uncertainty and clarification behavior. 1.5 pts
- Includes tool-use policy and "do not claim completion before tool result." 1.5 pts
- Includes privacy behavior for secrets, addresses, payment details, and PII. 1.5 pts
- Includes safety/escalation/handoff behavior. 1.5 pts
- Includes language policy where relevant. 1 pt

Critical failures: writing a long text-chat prompt with no spoken constraints; no tool policy; no privacy or escalation behavior.

## 6. Tool/function calling and approvals — 12 points

Scenario: A Realtime agent can look up orders, cancel subscriptions, and send refund confirmations. What tool policy is required?

Expected answer:

- Separates read-only tools from drafting and side-effecting tools. 2 pts
- Allows read-only lookup after intent is clear; requires explicit user confirmation for side effects. 2 pts
- Requires server-side validation of all tool arguments. 2 pts
- Requires application-side approval or human review for high-impact or irreversible actions. 2 pts
- Returns concise speech-ready tool results; redacts sensitive fields before speaking. 1.5 pts
- Logs tool calls, results, approval path, and correlation IDs. 1 pts
- States the assistant must not say an action succeeded until `function_call_output` or equivalent result confirms success. 1.5 pts

Critical failures: letting the model directly execute refunds/cancellations without confirmation; trusting model-emitted JSON without validation.

## 7. Cost and latency — 10 points

Question: How should an agent manage cost and latency in an OpenAI Realtime voice product?

Expected answer:

- Measures latency stages: connect, speech start/stop, response creation, first audio, final audio, tools, interruption. 2 pts
- Notes voice-agent sessions accrue text/audio/image input-output token costs, while streaming transcription/translation are duration-billed. 2 pts
- Includes documented audio-token accounting: user audio 1 token/100 ms and assistant audio 1 token/50 ms, with caveat to re-check. 2 pts
- Explains later turns can become more expensive because conversation context grows. 1.5 pts
- Reduces long assistant monologues, prompt bloat, unnecessary tool calls, idle sessions, and background-noise Responses. 1.5 pts
- Treats transcription as an optional separately billed choice. 1 pt

Critical failures: claiming connections/bandwidth are the main cost; no per-turn monitoring; ignoring conversation growth.

## 8. Consent, privacy, rights, and safety — 12 points

Scenario: A startup wants a friendly AI receptionist voice that records all calls, stores transcripts forever, and sounds like the founder.

Expected response:

- Requires clear microphone, recording, transcript, human-review, retention, and deletion disclosures before capture. 2 pts
- Challenges indefinite retention and recommends data minimization with explicit retention period and access controls. 2 pts
- Flags transcripts and audio as sensitive, potentially containing PII. 1.5 pts
- Rejects impersonating or cloning/sounding like a specific person without documented consent/rights and legal/policy review. 2 pts
- Requires disclosure that the receptionist is an AI voice agent, not a real human. 1.5 pts
- Includes safety boundaries for emergencies, regulated domains, minors, harassment, and escalation. 1.5 pts
- Mentions OpenAI API data is not used to train by default unless opted in, but that application-side logging/retention remains the builder's responsibility. 1.5 pts

Critical failures: approving founder voice imitation casually; no consent; no retention/access controls.

## 9. Complete applied design — 10 points

Task: Produce a concise production plan for a voice agent that schedules dental appointments.

Expected output characteristics:

- Chooses Realtime voice-agent session only if live conversation is needed; otherwise notes chained alternative for deterministic scheduling workflows. 1 pt
- Uses WebRTC for browser/mobile or WebSocket for server/telephony, with server-side API key custody. 1.5 pts
- Logs model, voice, transport, VAD, tools, prompt version, consent copy, and retention. 1.5 pts
- Defines tools with read-only availability lookup and side-effecting appointment booking requiring confirmation. 1.5 pts
- Includes prompt constraints for short spoken turns, uncertainty confirmation, privacy, and no medical advice beyond scheduling. 1.5 pts
- Includes consent and safety plan for health-related data, minors, emergencies, and human handoff. 1.5 pts
- Includes VAD/audio testing and cost/latency dashboard. 1.5 pts

Critical failures: model directly books appointments without confirmation; no HIPAA/health-data caution; client-side standard API key.
