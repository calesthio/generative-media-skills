---
name: elevenlabs-agents
description: Build, configure, and ship production voice agents on the ElevenLabs Agents platform (branded "ElevenAgents," formerly "Conversational AI"). Use when an agent must design a spoken-conversation system prompt, pick an LLM and TTS voice/model for a real-time voice bot, wire client/server/system tools and knowledge-base RAG, connect a channel (WebRTC/WebSocket SDK, embeddable widget, or telephony via Twilio/SIP), tune turn-taking and latency, set up simulation testing and evaluation, or reason about pricing, concurrency, and the consent/disclosure obligations of a synthetic voice talking to real people. Not for plain non-conversational text-to-speech, dubbing, or music generation.
---

# ElevenLabs Agents (ElevenAgents)

Production guidance for building voice (and text) agents on the ElevenLabs Agents platform. The product was renamed from "Conversational AI" to "ElevenLabs Agents" / "ElevenAgents" during 2026; documentation URLs use both `/docs/eleven-agents/...` and legacy `/docs/agents-platform/...` paths, and the two mostly mirror each other. All model IDs, prices, limits, and endpoints below are **volatile** and were verified on **2026-07-10** against elevenlabs.io/docs — re-verify before quoting them to a user, because ElevenLabs adds LLMs and revises plans frequently.

## When this skill applies

Use this skill when the work is a **two-way spoken (or typed) conversation** driven by the ElevenLabs Agents runtime: phone bots, website voice widgets, in-app voice assistants, WhatsApp/chat agents, outbound call campaigns, or a custom SDK integration. It also applies to configuring the agent's brain (prompt, LLM, tools, knowledge), its voice, its channel, and its evaluation.

Do **not** use it for one-shot text-to-speech, audiobook narration, dubbing, sound effects, or music — those are separate ElevenLabs products with their own APIs. If the user only wants a `.mp3` from text, they want the TTS API, not an agent.

## The pipeline you are configuring

**[Documented]** An ElevenAgents conversation is an orchestrated loop over four components (elevenlabs.io/docs/eleven-agents/overview, verified 2026-07-10):

1. **Speech-to-Text (ASR)** — a fine-tuned recognition model that turns caller audio into text. ElevenLabs' custom ASR is quoted at sub-100ms versus ~300ms+ for a generic Whisper deployment.
2. **Turn-taking / interruption model** — a proprietary model, layered on a Voice Activity Detector (VAD), that decides when the user has actually finished a turn (vs. a mid-sentence pause) and when a barge-in should stop the agent.
3. **LLM** — the reasoning brain. You pick from hosted models (Google/OpenAI/Anthropic/ElevenLabs-hosted open weights) or bring a custom endpoint.
4. **Text-to-Speech (TTS)** — a low-latency voice model rendering the reply, drawn from 5,000+ voices across 70+ languages (agent voice picker exposes ~31 languages; Flash/Turbo TTS models cover ~32).

Your job is to choose and tune each stage so the whole loop feels like a person. **[Heuristic]** Latency and quality trade against each other at every stage; optimize the loop as a whole, not one component in isolation.

## Latency: the budget that decides the feel

**[Documented]** ElevenLabs advertises first-turn latency under ~500ms for the ElevenAgents 2.0 stack (elevenlabs.io blog, 2026). Approximate per-stage contributions from ElevenLabs' own latency write-up (elevenlabs.io/blog/how-do-you-optimize-latency-for-conversational-ai, verified 2026-07-10):

| Stage | Typical contribution |
|---|---|
| ASR (ElevenLabs custom) | <100 ms |
| Turn-taking / VAD silence detection | tunable; adds the "end-of-turn" wait |
| LLM first-token | Gemini Flash <350 ms; GPT-4-class / Claude Sonnet 700–1000 ms |
| TTS (Flash v2.5) | ~75 ms model time, ~135 ms end-to-end |
| Network (same-region) | ~200 ms+ |
| Telephony (global) | ~500 ms+ |

**[Independent benchmark, disclosed method]** Third-party monitoring (Cekura, Deepgram, 2026) reports ElevenLabs among the fastest orchestrators — median turn ~1.7s — but with a long tail (P95 ~3.2s), driven mostly by LLM variance and telephony. Treat the sub-500ms figure as a best-case for the ElevenLabs-controlled stages, not the end-to-end phone experience.

**[Heuristic]** Practical latency levers, highest-impact first:
- Pick a fast LLM. The single biggest, most variable slice is LLM first-token. A Flash-tier or Haiku-tier model can save 400–700ms over a frontier model.
- Use `eleven_flash_v2_5` for the voice unless you have a specific quality reason not to.
- Keep the system prompt and per-turn context tight — long prompts inflate first-token time.
- Co-locate: choose the region closest to your callers; telephony hops dominate global calls.
- Mask unavoidable waits (tool calls, DB lookups) with a spoken filler ("Let me pull that up…") so dead air never exceeds ~1s.

## Agent configuration

### System prompt for a *spoken* conversation

**[Heuristic]** A voice-agent prompt is not a chatbot prompt. Spoken output is heard once, in sequence, with no scrollback, so:
- **Force brevity.** Instruct one idea per turn, ~1–3 sentences. Long paragraphs are unlistenable and inflate TTS latency and cost.
- **Ban screen-only formatting.** No markdown, bullet lists, tables, emojis, or URLs read aloud — they get spoken literally ("asterisk asterisk"). Ask for spelled-out numbers where clarity matters ("one-eight-hundred").
- **Give a persona and a scope.** Role, tone, what it can and cannot do, and an explicit "if you don't know / it's out of scope, say so and offer transfer" clause.
- **Script the edges.** First message, how to handle interruptions, silence, off-topic asks, and hostile callers.
- **Name the tools' triggers in prose.** State *when* to call each tool, because the LLM decides tool use from the prompt plus tool descriptions.

**[Documented]** The dashboard splits this into a **First message** (the opening line, supports dynamic variables) and a **System prompt**. A recent platform field, `trust_context`, marks an agent as `low` (serving untrusted external callers — restrict tool access) or `high` (serving the owner — full tool access appropriate) (changelog, 2026, verified 2026-07-10).

### LLM selection

**[Documented, volatile — verified 2026-07-10]** ElevenAgents supports a large, frequently-updated roster including:
- **OpenAI**: GPT-5.5, GPT-5.4 (+ Mini/Nano), GPT-5.2, GPT-5.1, GPT-5 (+ Mini/Nano), GPT-4.1 (+ Mini/Nano), GPT-4o, GPT-4o Mini.
- **Google**: Gemini 3.5 Flash, 3.1 Pro/Flash-Lite (preview), 3 Pro/Flash (preview), 2.5 Flash, 2.5 Flash-Lite.
- **Anthropic**: Claude Opus 4.7, Sonnet 4.6 / 4.5 / 4, Haiku 4.5.
- **ElevenLabs-hosted open weights**: Qwen3.6-35B-A3B, Qwen3.5-397B-A17B.
- **Custom LLM**: bring your own OpenAI-compatible endpoint with stored credentials.

The exact list changes almost monthly; always read the live Models page rather than trusting a memorized roster.

**[Heuristic]** Choose by the job:
- **Latency-first, simple flows** (FAQ, routing, quick info): a Flash / Flash-Lite / Haiku / Mini-tier model. Lowest first-token time.
- **Tool-heavy or reasoning-heavy flows** (multi-step, disambiguation, function calling that must not misfire): a higher-intelligence model — ElevenLabs' own tool-use guidance recommends the stronger Gemini Flash, GPT-5-class, or Claude Sonnet 4.x tiers and specifically warns against the weakest Flash models for reliable tool calls.
- **Data-residency-constrained (EU)**: some older Gemini/Claude variants are unavailable under EU residency; OpenAI and custom endpoints remain available. Verify per-model.

**[Documented]** **LLM cascading / fallback**: ElevenAgents can fall back through a backup sequence when the primary model errors or times out, protecting the conversation from a single provider outage. A documented default cascade (verified via docs search 2026-07-10) runs Gemini 2.5 Flash → Gemini 2.0 Flash → Claude 3.7 Sonnet → Claude 3.5 Sonnet v2. **[Heuristic]** For production, keep cascading on and make sure every model in the chain is fast enough that a fallback doesn't wreck the call.

### Voice and TTS model

**[Documented, verified 2026-07-10]** TTS model tradeoffs for agents:

| Model ID | Latency | Languages | Best for |
|---|---|---|---|
| `eleven_flash_v2_5` | ~75 ms | ~32 | **Default for real-time agents.** Best speed/quality balance, ~50% lower cost. |
| `eleven_flash_v2` | ~75 ms | English only | English-only, cost-sensitive. |
| `eleven_multilingual_v2` | Higher | 29 | Highest lifelike quality/emotion; long-form; when quality > latency. |
| `eleven_v3` | Higher | 70+ | Most expressive/dramatic; character work; generally **not** the low-latency real-time pick. |
| `eleven_turbo_v2_5` | Mid | ~32 | Deprecated for agents; superseded by Flash v2.5. |

**[Heuristic]** Default to `eleven_flash_v2_5`. Escalate to `eleven_multilingual_v2` only when a brand demands maximum warmth/expressiveness and can absorb the added latency. Higher-quality voice + model + LLM combined can visibly slow the turn — the dashboard itself warns of this.

**[Documented]** Voice settings that matter for agents: **stability** (lower = more emotional range and variation, higher = flatter/consistent), **similarity boost** (adherence to the source voice), and **speaker boost** (similarity at a slight latency cost). TTS output can be `mp3`, `pcm`, or `ulaw` — telephony typically needs `ulaw` 8kHz; SIP media runs G711 8kHz or G722 16kHz.

**[Heuristic]** Pick a voice whose native accent/language matches the caller base, keep stability moderate (very low stability can produce jarring swings across turns), and test the voice on your *actual* script — sample text flatters voices that stumble on domain jargon, phone numbers, and proper nouns.

### Language and multilingual

**[Documented]** Agents can run in a fixed language or detect/switch languages; TTS covers 70+ languages overall, with Flash v2.5 at ~32 and Multilingual v2 at 29. **[Heuristic]** For a multilingual agent, confirm all three stages support the target language: ASR recognition quality, the LLM's fluency, and the chosen TTS model's coverage. A voice cloned from one language may carry an accent when speaking another — audition it.

## Turn-taking and interruption

**[Documented]** ElevenAgents 2.0 uses a hybrid turn-taking model: a VAD plus deep-learning signals (filler words, prosody, rhythm, micro-pauses) to judge end-of-turn and handle barge-in. Configurable controls include **turn eagerness** (Eager / Normal / Patient) and a **turn timeout** from 1–30s (verified 2026-07-10).

**[Heuristic]**
- **Eager** cuts response delay but risks interrupting slow or thoughtful speakers; good for brisk transactional flows.
- **Patient** avoids cutting people off; good for support, elderly callers, or noisy lines, at the cost of a longer perceived pause.
- Background noise (HVAC, cross-talk, call-center ambiance) can trip the VAD and cut the agent off mid-sentence — **[Community/independent, disclosed]** ElevenLabs publishes no false-interruption precision/recall metrics, so validate barge-in behavior on real telephony audio, not a quiet office mic.
- A `background_sound` (ambient audio) option exists and an `agent_response_complete` client event now fires once when a turn is fully delivered — useful for reliable end-of-turn UI, wake-word gating, or message batching (changelog 2026).

## Knowledge base and RAG

**[Documented, verified 2026-07-10]** Attach documents to an agent as grounded knowledge:
- **Sources**: file upload (PDF, TXT, DOCX, HTML, EPUB; **max 21MB/file**), URL import (single page — it does **not** crawl linked pages), or pasted text.
- **Account limit**: non-enterprise caps at **20MB / 300k characters** total; enterprise expands via sales.
- **Config**: documents live under `conversation_config.agent.prompt.knowledge_base`, each with `type`, `name`, `id`, and an optional `usage_mode`. RAG can be enabled so the agent retrieves relevant chunks rather than stuffing everything into context.
- ElevenLabs does not publish the embedding model, chunk size, or retrieval internals.

**[Heuristic]** Split large manuals into focused documents, keep them current, and mine transcripts for questions the KB failed to answer. Put *stable* reference material in the KB; put *per-user* facts (account balance, order status) in dynamic variables or a server tool — never bake a customer's data into the KB.

## Tools and function calling

**[Documented]** Three tool types:
- **Server / webhook tools** — the agent makes an HTTP call to your backend for real-time data (DB lookups, order status) or authenticated actions (booking, refund). All secrets stay server-side.
- **Client tools** — invoke JavaScript in the caller's app/browser: open a modal, navigate, update UI, read local state. Configure with `type: "client"`, a `name`, `description`, `parameters`, and **`expects_response` / "Wait for response"** — when enabled, the agent pauses and appends the returned data to the conversation before continuing.
- **System tools** — built-in actions: end call, transfer to another agent, transfer to a human/number, skip turn, detect language. (System tools cannot update dynamic variables.)

**[Heuristic]** Tool reliability depends heavily on the LLM. Give each tool a crisp description and each parameter a clear `description` and `value_type` so the model extracts arguments correctly. For flows where a mis-fired tool is costly (payments, cancellations), use a higher-intelligence LLM and add tool-call tests (below). Design tools to be **idempotent** where possible and mask their latency with a spoken filler.

### Personalization: dynamic variables vs. overrides

**[Documented, verified 2026-07-10]**
- **Dynamic variables** inject runtime values (`{{user_name}}`, `{{account_tier}}`) into the prompt, first message, and tools — the **recommended** way to personalize per conversation. Passed via `conversation_initiation_client_data.dynamic_variables`. System variables like `system__caller_id`, `system__called_number`, `system__call_duration_secs`, `system__agent_id` are auto-available but **cannot** be set/overridden by the client payload.
- **Overrides** wholesale-replace the system prompt, first message, or other config at conversation start. Still supported but discouraged versus dynamic variables for maintainability.
- **Twilio personalization**: on an inbound call ElevenLabs webhooks your endpoint with call info; you return conversation-initiation data (dynamic variables + overrides) to tailor that specific call.

## Multi-agent workflows and transfers

**[Documented]** **Agent Workflows** are a visual editor for branching conversation graphs that route to specialized **subagents**, each with its own prompt, tools, and scoped knowledge base, and can hand off to a human. Two handoff mechanisms:
- **Agent-to-agent transfer** (system tool): the parent hands the live conversation to a child agent when a described condition is met ("user asks about billing"). Full transcript is preserved; the `transfer_to_agent` call is stripped from the child's visible history so it continues seamlessly. Supports an optional delay and an optional spoken transfer message (silent if blank).
- **Transfer to human / number**: routes to a person via the phone system, including warm-transfer into a conference with the caller.

**[Heuristic]** Prefer several small, single-purpose subagents over one giant prompt: each stays short (lower latency, fewer instructions to violate) and easier to test. Reserve human transfer for genuine escalation and always give the agent an explicit fallback path so a stuck caller is never trapped.

## Channels and SDKs

**[Documented, verified 2026-07-10]**
- **SDKs**: React (`@elevenlabs/react`), JavaScript/Web (`@elevenlabs/client`), Swift (iOS), Kotlin (Android), React Native, plus Python/TypeScript server SDKs. A CLI (`@elevenlabs/cli`) manages agents as code.
- **Transport**: **voice conversations default to WebRTC; text-only defaults to WebSocket.** The React `startSession` takes `signedUrl`, `conversationToken`, or `agentId` and infers transport from mode.
- **Widget**: an embeddable HTML snippet keyed by agent ID for zero-code website deployment.
- **Telephony**: native **Twilio** integration (inbound + outbound, no infra change) and **SIP trunking** compatible with most providers (Twilio, Vonage, Telnyx, Plivo, Bandwidth, Sinch, Infobip, RingCentral, Exotel, and other standards-compliant trunks). SIP supports digest or ACL/IP auth, TLS signaling, and SRTP media; codecs G711 8kHz or G722 16kHz. **Batch outbound calling** is available for campaigns.

### Authentication (do not leak your key)

**[Documented]** Never put the ElevenLabs API key in client code. For authenticated agents:
- **WebSocket** → your server calls the REST API to mint a **signed URL** (expires ~15 min); the client connects with it.
- **WebRTC** → your server mints a **conversation token**; the client connects with it.

**[Heuristic]** Always run authenticated agents in production so anyone can't rack up minutes on your agent ID, and gate the token/signed-URL endpoint behind your own auth. Public/unauthenticated agents are fine only for open demos.

## Testing, simulation, and evaluation

**[Documented, verified 2026-07-10]** ElevenAgents has a built-in test framework, runnable from the dashboard **Tests** tab, the CLI (`elevenlabs agents test <agent_id>`), or the SDK (`run_tests` / `runTests`, with `repeat_count` for probabilistic runs):
- **Scenario / LLM-eval tests** — a simulated user drives a conversation; an LLM scores the agent against success criteria you write (include tone expectations plus success *and* failure examples).
- **Tool-call tests** — assert the agent calls the right tool with the right args, validated by **exact match**, **regex** (e.g. `^ORD-[0-9]{8}$`), or **LLM semantic** check.
- **Simulation tests** — full or partial multi-turn simulations (a partial one starts mid-conversation to unit-test a sub-flow), with **tool mocking** and custom evaluation, scored against an outcome statement you define.
- **Probabilistic testing** — run a test N times; badges show green (100%), amber (≥80%), red (<80%) pass rates, grouping failures by reason. Because LLM output is stochastic, single-run "it worked once" is not a pass.
- **Create test from conversation** — turn a real failed call into a regression test in one click.

**[Documented]** Post-conversation **evaluation criteria** (success rubrics) and **data collection** (structured extraction) run automatically on live conversations using the same criteria as simulation, feeding analytics.

**[Heuristic]** Build a suite covering the happy path, each tool, each transfer condition, and the hostile/off-topic/silent edges; run it before every prompt or model change. Prompt and model swaps routinely regress behavior that "obviously" worked.

## Analytics

**[Documented]** The platform provides conversation search, transcripts, success-evaluation results, extracted data-collection fields, A/B testing, and performance metrics for monitoring at scale. **[Heuristic]** Watch median *and* tail latency, interruption/barge-in rates, tool error rates, transfer-to-human rate, and success-criteria pass rate — the tail and the transfer rate reveal production pain the averages hide.

## Pricing, concurrency, and burst

**[Documented, volatile — verified 2026-07-10]** ElevenAgents bills by **call minutes**, separate from the shared TTS credit pool; the **LLM and telephony are billed on top** by usage. Representative self-serve tiers (included minutes / concurrent calls):

| Plan | Included minutes | Concurrent calls |
|---|---|---|
| Free | 15 | 4 |
| Starter | 75 | 6 |
| Creator | 275 | 10 |
| Pro | 1,238 | 20 |
| Scale | 3,738 | 30 |
| Business | 12,375 | 40 |

Overage ≈ **$0.08/min** standard, **$0.16/min** burst; text messages ≈ **$0.003 each**. **Burst pricing**, when enabled, lets you exceed your concurrency cap up to ~3× at the doubled rate. There is no cap on how many agents you can create; the binding constraint is **concurrent calls**.

**[Heuristic]** Concurrency, not minutes, is what breaks at scale — a spike of simultaneous inbound calls hits the ceiling instantly and extra callers get rejected or burst-billed. For real call-center volume (hundreds of simultaneous calls) you need an enterprise concurrency arrangement; do not assume a self-serve plan absorbs a marketing blast. Model *both* levers: total minutes for the monthly bill, concurrent calls for the busy-hour peak.

## Safety, consent, and disclosure — a synthetic voice talking to real people

This is a legal and ethical surface, not a nicety. **[Documented / regulatory]**

- **AI disclosure**: Disclose that the caller is talking to an AI. Under the EU AI Act (Article 52 transparency for synthetic/deepfake audio), and analogous emerging rules, artificially generated voice interacting with a person must be disclosed. **[Heuristic]** Put the disclosure in the **first message** ("Hi, I'm an AI assistant from …"), not buried later.
- **TCPA (US)**: ElevenLabs' synthetic voices count as an "artificial or prerecorded voice." **Marketing** calls need **Prior Express Written Consent**; **informational** calls need prior express consent. Call only **8am–9pm** in the recipient's local time zone; scrub against the National DNC Registry and your internal DNC list; honor opt-outs promptly (within 10 business days) and offer an automated opt-out. Consent cannot be a condition of purchase. Many US states impose stricter rules — get legal counsel.
- **GDPR / biometrics**: Voice is generally biometric data under GDPR. Processing it typically needs an Article 9 lawful basis (usually explicit consent) plus a DPIA (Article 35). For EU/biometric processing use the enterprise tier and a signed DPA.
- **Voice cloning consent**: If the agent uses a **cloned** voice, you need documented, explicit written consent from the voice owner covering AI/synthetic voice-model creation and generated speech — cloning carries its own compliance posture beyond stock TTS.
- **Prohibited uses**: impersonation, fraud, evading voice verification, unauthorized robocalling, harassment, voter suppression, and similar. Don't build them.

**[Heuristic]** Bake compliance into config: disclosure in the first message, an easy "talk to a human" transfer, a recording/consent notice where required, timezone-aware scheduling for outbound, and DNC checks before dialing. Treat "is the user OK talking to a bot, and did they consent to the call?" as a design requirement, not an afterthought.

## Common failure modes

**[Heuristic, from documented behavior]**
- **Reads formatting aloud** — markdown/emojis/URLs in output. Fix: forbid them in the prompt; request plain speech and spelled-out numbers.
- **Rambling turns** — no brevity constraint. Fix: cap turns at 1–3 sentences in the prompt.
- **Gets cut off in noise** — VAD false-triggers. Fix: Patient turn-taking, test on real telephony audio, tune the timeout.
- **Sluggish replies** — frontier LLM + high-quality voice. Fix: Flash-tier LLM + `eleven_flash_v2_5`, tighten the prompt, add spoken fillers for tool waits.
- **Tools misfire or don't fire** — weak LLM or vague tool descriptions. Fix: stronger LLM for tool-heavy flows, sharpen descriptions/params, add tool-call tests.
- **Leaked API key / unauthenticated agent** — key in client code. Fix: signed URLs / conversation tokens minted server-side; authenticated agents in production.
- **Concurrency wall at launch** — self-serve concurrency too low for peak. Fix: size the plan to busy-hour simultaneous calls, enable burst, or go enterprise.
- **No AI disclosure / no consent** — regulatory exposure. Fix: disclose in the first message; secure TCPA/GDPR consent before deploying.

## Complete example (labeled example, not a required formula)

**Intent**: an authenticated, low-latency support agent for a mid-size e-commerce brand, deployed as a website voice widget with a phone fallback, that can look up order status and escalate to a human.

- **Trust context**: `low` (external callers).
- **LLM**: a fast Flash/Sonnet-tier model with high enough tool reliability for order lookups; LLM cascading left on.
- **TTS**: `eleven_flash_v2_5`, moderate stability, brand voice matched to the customer base's accent.
- **First message** (also the AI disclosure): *"Hi, you're speaking with an AI assistant from Northwind Support. I can check an order or connect you to a person — how can I help?"*
- **System prompt** (essentials): role = order-status support; keep replies to 1–2 spoken sentences; never read URLs, markdown, or emojis; spell out order numbers and tracking codes; if the order can't be found or the request is out of scope (refunds, complaints), apologize briefly and transfer to a human; call `get_order_status` whenever the user references an order.
- **Tools**: server tool `get_order_status(order_id)` → your backend; system tool `transfer_to_number` for escalation. `order_id` parameter has a clear description and a regex-checkable format.
- **Personalization**: `{{customer_first_name}}` and `{{account_tier}}` injected as dynamic variables at session start; `system__caller_id` used to pre-lookup the account on phone calls.
- **Knowledge base**: shipping-policy and returns-policy documents (as focused files, RAG on) for general questions — *not* per-customer data.
- **Turn-taking**: Normal eagerness, ~7s timeout; test barge-in on recorded phone audio.
- **Channel**: React SDK widget over WebRTC using a server-minted conversation token; Twilio number for inbound phone with a personalization webhook.
- **Testing**: scenario test (empathetic handling of a "where's my order" with success + failure examples), tool-call test asserting `get_order_status` fires with a regex-valid `order_id`, and a partial simulation for the escalation branch — each run with `repeat_count` ≥ 5.
- **Expected result**: sub-second-feel replies for cached info, a spoken filler while `get_order_status` runs, clean handoff to a human on out-of-scope asks.
- **Likely failure modes**: order-lookup tool misfires on ambiguous input (mitigate with a stronger LLM + clear param description); noisy callers cut off the agent (mitigate with turn-taking tuning); launch-day concurrency spike (size the plan / enable burst).
- **Variations**: swap the widget for pure telephony via SIP trunk; add a billing subagent and route via Agent Workflows; run outbound reminders as a batch campaign — which then triggers full TCPA consent + calling-window obligations.

## Primary sources (verified 2026-07-10)

- ElevenAgents overview — https://elevenlabs.io/docs/eleven-agents/overview
- Quickstart — https://elevenlabs.io/docs/eleven-agents/quickstart
- LLM / Models — https://elevenlabs.io/docs/eleven-agents/customization/llm ; LLM cascading — https://elevenlabs.io/docs/agents-platform/customization/llm/llm-cascading
- TTS models — https://elevenlabs.io/docs/overview/models
- Tools (client / server / system) — https://elevenlabs.io/docs/eleven-agents/customization/tools and .../tools/client-tools
- Knowledge base — https://elevenlabs.io/docs/eleven-agents/customization/knowledge-base
- Personalization / dynamic variables / overrides — https://elevenlabs.io/docs/eleven-agents/customization/personalization
- Conversation flow & workflows — https://elevenlabs.io/docs/eleven-agents/customization/agent-workflows ; agent transfer — .../tools/system-tools/agent-transfer
- SDKs (React / WebSocket / JS) & authentication — https://elevenlabs.io/docs/eleven-agents/libraries/react ; https://elevenlabs.io/docs/agents-platform/customization/authentication
- Telephony: Twilio native — https://elevenlabs.io/docs/eleven-agents/phone-numbers/twilio-integration/native-integration ; SIP trunking — https://elevenlabs.io/docs/eleven-agents/phone-numbers/sip-trunking
- Testing / simulation — https://elevenlabs.io/docs/eleven-agents/customization/agent-testing ; https://elevenlabs.io/docs/agents-platform/guides/simulate-conversations
- Latency optimization — https://elevenlabs.io/blog/how-do-you-optimize-latency-for-conversational-ai
- Pricing — https://elevenlabs.io/pricing/agents ; concurrency FAQ — help.elevenlabs.io (Agents requests/concurrency)
- Legal: TCPA — https://elevenlabs.io/docs/eleven-agents/legal/tcpa ; privacy policy — https://elevenlabs.io/privacy-policy
- Secondary/independent (disclosed method, labeled): Deepgram and Cekura production-latency/turn-taking write-ups (2026).
