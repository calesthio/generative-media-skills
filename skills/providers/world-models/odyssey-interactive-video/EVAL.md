# EVAL — odyssey-interactive-video

Answer key and scoring specification. The evaluated agent receives the user task and `SKILL.md` only, never this file. Score the captured response against the criteria below.

Facts are dated to a **2026-07-10** verification point. If evaluating later, allow answers that correctly note a fact may have changed and that first-party re-verification is needed — that is a strength, not a miss.

Scoring per item: **2** = all required points, no critical failure; **1** = partial, minor omissions; **0** = misses required points or commits any critical failure. A critical failure caps the item at 0 regardless of other content.

---

## Part 1 — Knowledge questions

### K1. What distinguishes Odyssey's world models from offline video generators like Sora/Veo/Kling?
**Expected answer.** Odyssey models are **causal and autoregressive** — each frame is predicted only from past frames and past/incoming user input, then streamed immediately, so the user can change the video *mid-generation*. Offline generators are **bidirectional**, planning a whole fixed clip with knowledge of future frames, taking seconds-to-minutes per clip, and cannot be steered live. Odyssey generates *every frame* (diffusion-based, no game engine, no pre-authored assets) and streams it (~40–50 ms/frame).
**Required points:** (a) autoregressive/causal, per-frame, conditioned on user input; (b) real-time streaming vs. offline fixed clip; (c) user steers mid-stream vs. no mid-clip control.
**Critical failure:** describing Odyssey as producing downloadable fixed clips, or equating it to Sora/Veo.

### K2. Name the current Odyssey model lineup and what each is for.
**Expected answer.** **Odyssey-1** (2025-05-28) first playable world model, narrow/unstable, superseded. **Odyssey-2** / API tier **Odyssey-2 Pro** general-purpose, prompt-steered, the live default. **Starchild-1** (2026-05-17) first multimodal — synchronized audio+video from streaming text/speech/action. **Agora-1** multi-agent, up to 4 players in one shared environment. **PROWL-1** an RL research framework (not an interactive product).
**Required points:** at least Odyssey-2 (default), Starchild-1 (audio+video), and Agora-1 (multiplayer) correctly differentiated.
**Disqualifying claim:** inventing capabilities (e.g., "Starchild-1 exports 3D meshes") or confusing which model adds audio.

### K3. State the latency, frame-rate, and coherence characteristics.
**Expected answer.** Per-frame latency ~40 ms (Odyssey-1) to ~50 ms (Odyssey-2); frame rates ~20 fps (Odyssey-2), up to ~24 fps (Starchild-1), up to ~30 fps (Odyssey-1). Coherence is **bounded and drifts**: Odyssey claims 5+ minutes for Odyssey-1, but the CTO's more conservative later framing is ~1–2 minutes before degradation; plan around ~1–2 min. Latency is measured **per frame**, not per clip.
**Required points:** (a) tens-of-ms per-frame latency; (b) ~20–30 fps range; (c) bounded coherence with drift, realistic ~1–2 min planning figure.
**Critical failure:** claiming unlimited/indefinite coherence or persistent stable worlds.

### K4. What are the access routes as of 2026-07-10, and what is uncertain?
**Expected answer.** Reliably public: **web experiences** — experience.odyssey.ml (Odyssey-2) and agora.odyssey.ml (Agora-1), playable in-browser. An **API exists but is emerging** — developer.odyssey.ml / documentation.api.odyssey.ml describe an Odyssey-2 Pro API (interactive streams, viewable/broadcast streams, Simulate for offline batch; API-key auth; session/duration limits). The launch blog originally said "API coming soon" and the homepage didn't headline it, so API status/quotas/terms must be **verified directly** before promising an integration. Starchild-1/PROWL-1 are preview + technical report, not documented general APIs.
**Required points:** (a) web experiences are the safe public route; (b) API is real but nascent and must be verified; (c) does not fabricate stable/guaranteed API.
**Critical failure:** asserting a mature, stable, SLA-backed API without any verification caveat, or claiming there is no way to access the models at all.

### K5. How mature is this technology, in Odyssey's own words?
**Expected answer.** Research-stage. CTO Jeff Hawke calls it "the GPT-2 era of world models" and "a phase of mass exploration, not mass commercialization." No standardized quality benchmarks for the interactive style exist yet. Output is dreamlike/unstable.
**Required points:** explicitly research-grade / pre-commercialization, not production-reliable.
**Critical failure:** presenting Odyssey as a production-ready, reliable service.

---

## Part 2 — Production-decision questions

### D1. Client wants a 60-second finished, brand-controlled hero video for a product launch, downloadable for YouTube. They heard Odyssey is "the new AI video." Recommend.
**Expected decision.** **Do not use Odyssey.** This is a fixed, downloadable, pixel-controlled deliverable → route to an offline generator (Sora/Veo/Kling/Runway) or traditional production. Odyssey produces no clean downloadable clip by default, output is dreamlike/unstable, not brand-pixel-controllable, and isn't the right shape for one-to-many distribution.
**Reasoning a strong answer shows:** distinguishes interactive-stream vs. finished-file deliverable; cites fidelity/control limits; notes distribution/cost shape.
**Penalize:** recommending Odyssey for a downloadable brand clip; failing to name a better-fit alternative.

### D2. A museum wants a staffed installation where visitors type a mood and walk through an evolving dreamlike world for ~90 seconds each. Recommend.
**Expected decision.** **Strong fit for Odyssey-2.** Real-time, prompt-steered, short staffed sessions, novelty and surreal aesthetic are assets not liabilities. Use experience.odyssey.ml or the Odyssey-2 Pro API. Design for ~1–2 min coherence, budget per concurrent user-hour (GPU-per-viewer), verify API terms, handle drift with short guided sessions, clear rights/privacy for streamed input.
**Reasoning:** matches interactive/live/novelty criteria; correctly sets maturity, cost, and drift expectations.
**Penalize:** promising persistent worlds, ignoring per-viewer GPU cost, ignoring coherence limits, or over-promising fidelity.

### D3. A game studio asks whether Odyssey can replace their Unity level-building so they stop authoring assets. Recommend.
**Expected decision.** **No, not for a shippable game today.** No persistent/deterministic world (geometry drifts, no durable state), no exportable assets or exact collision, coherence bounded to minutes, live GPU session per player that doesn't scale like a client engine. Position as a research/prototype probe (Agora-1 for multiplayer feel), cite "GPT-2 era" framing, recommend a real engine for the product.
**Penalize:** validating engine-replacement; ignoring persistence, asset-export, scaling, or maturity.

### D4. A companion-app startup wants a character that talks with real voice and ambient sound, reacting to the user's speech in real time. Which model, and what caveats?
**Expected decision.** **Starchild-1** — it is the multimodal model with synchronized audio+video and streaming speech/text/action input, and a companionship/narrator interaction regime. Caveats: preview + technical-report stage (verify programmatic access — don't assume a stable API), acoustic/scene identity drifts over long horizons, no interactive-quality benchmarks yet, and consent/privacy handling required for streamed user speech.
**Penalize:** choosing Odyssey-2 (drops audio) with no correction; ignoring the preview/access caveat; ignoring speech-privacy.

---

## Part 3 — Applied production tasks

### A1. Write the honest scoping note for a mixed request.
**User request:** "Build us an interactive AI world for a trade-show booth where people type a scene and explore it, AND give us polished clips of the best sessions for our socials."
**Expected approach & essential characteristics of a good output:**
- **Splits the two deliverables.** Booth = interactive → Odyssey-2 (experience.odyssey.ml or Odyssey-2 Pro API). Social clips = finished file → either screen-record the live session (accepting dreamlike look) or produce separately with an offline generator.
- Sets expectations: ~1–2 min coherence, non-persistent geometry, ~20 fps, dreamlike fidelity, GPU cost per concurrent visitor, staffed sessions.
- Names verification of API status/quotas/terms at developer.odyssey.ml and rights/consent/privacy for public deployment.
**Scoring rubric:** 2 = separates deliverables, correct model, realistic limits, cost + access + rights covered. 1 = right model but glosses over the clip/file mismatch or omits cost/rights. 0 = promises clean downloadable social clips straight from Odyssey, or treats it as a mature turnkey service.
**Critical failures:** silently promising brand-clean downloadable clips; omitting the maturity/drift warning; inventing pricing tiers as fact.

### A2. Draft the "expectations & risks" section an agent would put in a project brief before a client signs off on an Odyssey prototype.
**Expected approach.** A short, plainly worded risk list covering, at minimum: research-stage maturity ("GPT-2 era," not commercialized); dreamlike/unstable visuals, unreliable text/detail; coherence bounded ~1–2 min with drift; no persistent world / no exportable asset / no default downloadable clip; per-concurrent-user GPU cost (order-of-magnitude $1–2/user-hour historical, verify current); access via web now, API emerging (verify terms/quotas); rights/ownership unsettled (read the API License Agreement, don't assume commercial rights/indemnity); consent + privacy for streamed input. Each item dated / flagged as verify-before-relying.
**Scoring rubric:** 2 = covers maturity, fidelity, coherence/persistence, no-asset, cost, access, rights, privacy, with volatile items flagged for re-verification. 1 = covers maturity + a few technical limits but misses rights/privacy or cost shape. 0 = reads as a marketing pitch, omits maturity/limits, or states volatile facts as permanent.
**Critical failures:** asserting commercial-use rights/ownership as settled; presenting as production-reliable; quoting a firm price as current fact without a verify caveat.

### A3. A user says only: "Set me up with the Odyssey interactive video API." Respond.
**Expected approach.** Don't blindly claim a turnkey SDK. Point to **experience.odyssey.ml** to evaluate first; explain the API is **Odyssey-2 Pro** at developer.odyssey.ml (get an API key on the dashboard; surfaces are interactive streams, viewable/broadcast streams, and Simulate for offline batch; key stays server-side, browsers use short-lived credentials; watch session/duration/"credit lease" limits and the API License Agreement). Flag that this is emerging and quotas/terms/pricing must be checked live, and that budget scales per concurrent user-hour. Ask what the actual deliverable is, since interactive video may be the wrong tool.
**Scoring rubric:** 2 = correct API surface + auth model + verify-terms caveat + budget shape + a clarifying question on the real goal. 1 = points to the right place but omits the nascent/verify caveat or the cost shape. 0 = invents endpoints/SDK details as fact, or claims a mature stable API with guarantees.
**Critical failures:** fabricating specific endpoint URLs/parameters/pricing as established fact; omitting that the API is early and must be verified.

---

## Cross-cutting critical failures (cap any item at 0)

- Presenting Odyssey as a production-ready, SLA-backed, reliable service.
- Claiming persistent, stable, downloadable, or exportable output (clips, meshes, saved worlds) as a default capability.
- Stating volatile facts (model names, latency, fps, access routes, pricing) as permanent without a verification date or re-verify caveat.
- Fabricating API endpoints, parameters, SDKs, or price tiers.
- Recommending Odyssey for a fixed, brand-controlled, downloadable deliverable without redirecting to an offline/engine alternative.
- Asserting commercial-use rights, output ownership, or indemnity as settled without pointing to Odyssey's own terms.
- Ignoring consent/privacy for streamed user input (speech, likeness) in a deployed context.
