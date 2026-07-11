# Evaluation spec for `gemini-live-audio`

This file is withheld from evaluated agents. Give the agent only `SKILL.md` and the user task, then use this key to score the response.

## Core scoring dimensions

Score out of 100:

- Capability boundaries and mode selection: 20
- Architecture, transport, media format, and session lifecycle: 20
- Voice, turn-taking, transcription, language, and latency QA: 15
- Tool/function calling and safety gating: 15
- Cost, quotas, regions, data governance, and retention: 15
- Production usefulness, examples, and troubleshooting quality: 15

Critical failure cap: If an answer exposes a long-lived Gemini API key in a client app, ignores consent/retention for recorded live audio, or claims unsupported high-impact actions can be performed without confirmation, cap at 55 even if other details are strong. If it confuses Live Translation with a general tool-using Live Agent in a way that would break the product, cap at 70. If it invents exact latency/accuracy guarantees without measurement or source, cap at 80.

## Knowledge questions

### 1. When should Gemini Live audio be used instead of ordinary TTS?

Expected answer:

- Use Gemini Live for real-time bidirectional spoken sessions with low-latency streaming, interruptions/barge-in, live turn-taking, optional multimodal input, tool calls, and transcripts.
- Use ordinary TTS for batch/prerecorded narration, podcast/audiobook rendering, or deterministic voiceover production.
- Use STT/transcription tools for offline transcript/subtitle workflows.

Required points:

- Distinguishes live spoken interaction from batch audio generation.
- Mentions barge-in/turn-taking or WebSocket session nature.
- Names at least one non-use case.

Penalize:

- Treats Live as simply a higher-quality TTS model.
- Suggests it is the best default for all voice work.

### 2. What are the documented audio format requirements?

Expected answer:

- Input audio is raw little-endian 16-bit PCM, natively 16 kHz, usually sent with MIME type like `audio/pcm;rate=16000`.
- Output audio is raw little-endian 16-bit PCM at 24 kHz.
- Production clients should chunk microphone input in small frames, ideally 20-40 ms, and avoid large buffering.

Required points:

- PCM16/little-endian.
- 16 kHz input and 24 kHz output.
- MIME/rate or chunking detail.

Penalize:

- Sends MP3/WAV files directly as realtime chunks without conversion.
- Reverses input/output sample rates.

### 3. What is the difference between Live Agent and Live Translation?

Expected answer:

- Live Agent is an assistant-like mode for turns, reasoning, multimodal context, tools/function calling, search grounding, and actions.
- Live Translation is a low-latency speech-to-speech interpreter pipeline, documented as audio-restricted and translation-only, without tools/instructions as a general agent surface.

Required points:

- Correctly identifies Live Translation as separate from conversational agent workflow.
- States that tools/function calling belong to Live Agent, not Live Translation.

Penalize:

- Uses a persona/tool prompt for pure live translation.
- Claims Live Translation can call tools without source verification.

### 4. How should a browser app authenticate directly to the Live API?

Expected answer:

- Do not ship a long-lived API key in client code.
- Use a backend to authenticate the user and mint short-lived ephemeral tokens for client-to-Gemini WebSocket connections, ideally constrained by model/config.
- Backend remains responsible for policy, tool execution, consent/logging, and user identity.

Required points:

- Mentions ephemeral tokens.
- Explains backend minting/auth flow.
- Warns against long-lived API keys in browsers/mobile apps.

Penalize:

- Suggests embedding an API key in JavaScript.

### 5. What must the client do when the user interrupts model speech?

Expected answer:

- Detect the server interruption/barge-in signal and immediately stop/discard queued playback audio.
- Otherwise the agent continues speaking stale audio over the user.
- Test interruption-to-silence latency.

Required points:

- Immediate discard/stop playback.
- Mentions stale buffer or talking over user.

Penalize:

- Only pauses future requests but lets queued audio finish.

### 6. What are the Live API session duration issues and mitigations?

Expected answer:

- Without compression, documented limits include 15 minutes audio-only and 2 minutes audio+video; connection lifetime is around 10 minutes.
- Use context window compression for long sessions.
- Use session resumption/reconnect handling with latest resumption handle/token and GoAway handling.
- Retention implications differ by surface and must be reviewed.

Required points:

- Gives the 15 min / 2 min limits.
- Mentions context compression.
- Mentions resumption/reconnect.

Penalize:

- Promises unlimited calls without compression/resumption.
- Ignores retention implications of resumption in ZDR contexts.

### 7. What tool-use limitations matter for Live API?

Expected answer:

- Live supports function calling and Google Search grounding, but not every Gemini tool.
- The client must manually handle tool-call events and send `FunctionResponse`; automatic tool response handling should not be assumed.
- Model differences matter: Gemini 3.1 Flash Live Preview is documented synchronous-only for function calling, while Gemini 2.5 Flash Live Preview supports synchronous and asynchronous.
- High-impact tools need confirmation.

Required points:

- Manual tool responses.
- Function calling/Search supported.
- Mentions unsupported/differing tools or model differences.

Penalize:

- Claims code execution, Maps, or URL context are generally supported in Live based only on non-live Gemini docs.
- Omits confirmation for write actions.

### 8. What should an answer say about pricing and quotas?

Expected answer:

- Treat pricing/rate limits as volatile and re-check official docs.
- Audio is counted/priced at approximately 25 tokens/sec in docs.
- Rate limits are per project, tier/model dependent, and preview models often have stricter limits.
- Estimate per-minute cost from both input and output audio plus search/tool costs.

Required points:

- Volatility/re-check.
- 25 tokens/sec audio.
- Project/tier/model quota variability.

Penalize:

- Quotes stale or unqualified exact prices as permanent.
- Ignores output audio cost.

### 9. What governance distinction exists between Developer API and Gemini Enterprise Agent Platform?

Expected answer:

- Developer API commonly uses API keys and has free/paid data-use differences; paid tier is documented as not used to improve products, while free tier may be.
- Gemini Enterprise Agent Platform uses Google Cloud/IAM, regional/global endpoints, enterprise terms/support/SLA options, provisioned throughput, and data residency controls.
- Endpoint choice alone is not a data residency guarantee; ML processing commitments depend on endpoint/model/location.
- Grounding, logging, session resumption, and caching have separate retention implications.

Required points:

- Distinguishes API key Developer API from Cloud/IAM enterprise surface.
- Mentions data-use/training or logging.
- Mentions regions/data residency caveat.

Penalize:

- Says all Gemini calls are zero-data-retention by default.
- Says global endpoint guarantees regional residency.

## Production-decision scenarios

### Scenario A: The user asks for “a Gemini voicebot for a bank that can transfer money by voice.”

Strong expected decision:

- Gemini Live Agent could be a candidate for spoken interaction, but banking transfers are high-impact financial actions.
- Recommend enterprise/Gemini Enterprise Agent Platform review rather than casual Developer API prototype for production.
- Require strong user authentication, explicit spoken confirmation with amount/payee/source account, fraud/risk controls, audit logs, consent/recording disclosure, human/escalation path, and compliance/legal review.
- Expose transfer function only after confirmation and policy checks; tool schema must include confirmation and idempotency.
- Do not claim the model itself should decide transfer eligibility.

Score:

- 9-10: Covers all risk controls and Live-specific details.
- 6-8: Good direction but misses either governance or tool confirmation/idempotency.
- 3-5: Mentions caution but offers a thin prompt-only solution.
- 0-2: Allows direct transfers based on one utterance or ignores compliance.

Critical failures:

- No explicit confirmation for transfers.
- No authentication or compliance review.

### Scenario B: The user asks for “real-time translation from Spanish to English for a conference, plus the AI should answer audience questions and search the web.”

Strong expected decision:

- Separate the use cases: pure continuous speech-to-speech translation maps to Live Translation; answering audience questions/searching web is a Live Agent feature.
- Recommend either two modes/products or a controlled handoff: translation channel for presenter audio; separate moderated Q&A agent for audience questions with Search grounding.
- Warn that Live Translation is not the right place for tools/instructions.
- Include consent/recording notices, latency and glossary QA, human interpreter fallback for critical content.

Score:

- 9-10: Cleanly separates channels and gives deployable architecture.
- 6-8: Correct distinction but limited QA/governance.
- 3-5: Suggests one agent with a mixed prompt but notes tradeoffs.
- 0-2: Treats Live Translation as a tool-using assistant.

### Scenario C: The user wants a browser-only demo with direct Gemini WebSocket connection.

Strong expected decision:

- Browser direct connection can reduce latency, but must use ephemeral tokens minted by a backend; never a long-lived API key.
- Backend authenticates user and creates constrained tokens. Tools should still be routed through backend or a trusted service.
- Include token expiry, reconnect/session resumption, consent, CORS/deployment details, and local audio conversion to PCM16.

Score:

- 9-10: Complete secure architecture and Live session concerns.
- 6-8: Mentions ephemeral tokens but misses tools/session details.
- 3-5: Secure warning only, little implementation guidance.
- 0-2: Embeds API key in browser.

### Scenario D: The user wants a 45-minute visual troubleshooting call with a technician’s camera.

Strong expected decision:

- Live Agent with visual input may fit, but verify model/surface support, cost, regions, and media limits.
- Documented audio+video session limit without compression is 2 minutes; implement context window compression, session resumption/handoff, or periodic summaries/reconnects.
- Use low-rate images/video, safety disclaimers, no definitive safety certification, and confirmed ticket/tool actions.
- QA camera quality, frame rate, battery/network, VAD in noisy field settings, and retention of video/audio.

Score:

- 9-10: Complete plan and limitations.
- 6-8: Correct but misses duration/session mitigation or safety language.
- 3-5: Generic multimodal plan without Live limits.
- 0-2: Promises uninterrupted 45-minute camera session without mitigation.

## Applied production tasks

### Task 1: Draft a system instruction for a healthcare appointment scheduling voice agent.

Expected approach:

- Keep it concise and spoken-interaction oriented.
- Agent can schedule or reschedule appointments but not provide diagnosis or emergency advice.
- Ask one question at a time.
- Collect minimum necessary info.
- Confirm date/time/provider/location before booking.
- Tool-call conditions are explicit.
- Include privacy/consent and emergency escalation.

Rubric out of 20:

- 4 persona and spoken style suitable for Live.
- 4 clear scheduling flow and one-question turns.
- 4 tool-call gating and explicit confirmation.
- 4 healthcare safety boundaries and emergency escalation.
- 2 privacy/minimum necessary data.
- 2 handles interruptions/short responses.

Critical failures:

- Provides medical diagnosis.
- Books without confirmation.
- Requests unnecessary sensitive data.

### Task 2: Design a latency QA plan for Gemini Live audio.

Expected approach:

- Measure mic-to-first-audio, end-of-speech-to-first-audio, interruption-to-silence, chunk upload timing, VAD turn segmentation, playback buffer underflow, reconnect time, tool-call round trip, and transcript lag.
- Test quiet/noisy/accented speech, short confirmations, long pauses, serial numbers, network jitter, mobile devices, and long sessions.
- Include audio format validation and barge-in buffer discard.
- Include cost/rate monitoring.

Rubric out of 20:

- 5 latency metrics.
- 4 VAD and barge-in tests.
- 3 device/network/environment coverage.
- 3 session/reconnect/tool-call coverage.
- 3 audio/transcript correctness checks.
- 2 cost/quota monitoring.

Critical failures:

- Uses only subjective “feels fast” testing.
- Does not test interruption.

### Task 3: Produce a safe tool schema strategy for a hotel concierge voice agent.

Expected approach:

- Separate read-only lookup tools from booking/payment/write tools.
- Read-only can execute after clear request; bookings/payments require explicit confirmation.
- Narrow schemas with dates, timezone, locale, guest counts, room/table IDs, idempotency keys, and confirmation booleans.
- Spoken summaries before actions.
- Backend validates policy, availability, identity, payment authorization.
- Handle delayed tool responses gracefully; use async/non-blocking only if selected model supports it.

Rubric out of 20:

- 4 tool risk classification.
- 4 narrow schema design.
- 4 confirmation and spoken summary.
- 3 backend validation/idempotency.
- 3 Live model async/sync caveat.
- 2 error/retry behavior.

Critical failures:

- Lets model directly charge or book without confirmation.
- Omits backend validation.

### Task 4: Review this flawed plan: “Use `gemini-3.5-live-translate-preview` as our customer support agent. Put our tool definitions in the prompt and let it search order status. We’ll run it for 30-minute calls from a browser with our API key. No need to log consent because we don’t record audio.”

Expected answer:

- Reject or substantially revise.
- `gemini-3.5-live-translate-preview` is for translation, not a tool-using support agent.
- Need Live Agent model for support/tools, and real function declarations, not only prompt text.
- Browser must not use a long-lived API key; use backend-provisioned ephemeral tokens or backend proxy.
- 30-minute sessions require context compression/resumption/reconnect design.
- Consent is still needed for live AI audio/transcripts/processing depending on jurisdiction/product policy, even if not recording raw audio.
- Search/order status has data governance implications; order status should be backend function with auth.

Rubric out of 20:

- 4 catches wrong model/mode.
- 4 catches insecure API key.
- 3 catches tool implementation flaw.
- 3 catches session duration issue.
- 3 catches consent/privacy flaw.
- 3 proposes corrected architecture.

Critical failures:

- Accepts the plan unchanged.
- Misses API key exposure.

## Overall evaluator notes

High-quality answers should keep documented facts, operational observations, and heuristics separate. They should date volatile claims or explicitly say to re-check docs. They should be useful to an agent building real media/voice production systems, not merely list API features.

Common weak-answer patterns:

- Over-indexing on model marketing and ignoring transport/audio details.
- Omitting playback buffer discard on barge-in.
- Treating transcripts as guaranteed perfect.
- Forgetting output audio cost.
- Assuming all Gemini tools work in Live.
- Assuming Developer API and Gemini Enterprise Agent Platform have identical data governance.
- Ignoring consent because audio is streamed instead of stored.
