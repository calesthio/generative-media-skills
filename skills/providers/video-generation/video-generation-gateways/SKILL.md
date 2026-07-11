---
name: video-generation-gateways
description: >-
  Select, integrate, and operate multi-model video-generation gateways —
  hosted inference aggregators such as fal.ai, Replicate, and WaveSpeed that
  expose many third-party video (and video-adjacent audio) models behind one
  account, one API surface, and one bill. Use when deciding whether to route
  video generation through a gateway versus a direct model-provider API; when
  comparing gateways on catalog, async/queue job design, webhooks, pricing,
  schema discovery, and version pinning; and when operating gateway workloads
  in production — spend controls, retries, cross-gateway failover, content-
  safety differences, data retention, and commercial-rights passthrough of the
  underlying model. Not for direct model-provider APIs, local/self-hosted
  inference, model training/fine-tuning, or image-only gateway use.
---

# Video-generation gateways

A **video-generation gateway** is a hosted inference aggregator that resells
many third-party video models (Veo, Kling, Seedance, Hailuo/MiniMax, Luma,
Wan, LTX-Video, Pika, and others) behind a single account, a single API
convention, and a single bill. You send a prompt and parameters to a
gateway-owned endpoint; the gateway runs the underlying model on its own
infrastructure and returns a hosted result URL. This skill covers **fal.ai**,
**Replicate**, and **WaveSpeed** as the representative gateways, and the
production decisions common to the category.

This skill is about *routing and operating*, not about art direction. Prompt
craft, shot design, and motion direction for a specific model belong to
model- or craft-specific skills. Here the questions are: which gateway, going
through a gateway at all, how the async job contract works, how to discover a
model's schema, how to pin a version, how to cap spend, how to fail over, and
whose license governs the output.

## When a gateway is the right route (and when it is not)

**Use a gateway when** (production heuristics):

- You need **several video models behind one integration** — e.g. Veo for
  premium shots, a Kling/Seedance tier for volume, and an audio or upscale
  model in the same pipeline — without signing and maintaining a separate
  contract, key, billing relationship, and SDK per vendor.
- You want **one async job contract** (submit → poll/webhook → fetch) instead
  of learning each vendor's bespoke long-running-job protocol.
- You are **model-shopping or A/B testing** and want to swap model IDs without
  re-plumbing auth, storage, and result handling.
- You want the gateway to **host input uploads and output media** on a CDN so
  you are not building that yourself.
- Your volume does not yet justify a direct enterprise contract, or the model
  has **no first-party public API** and is only reachable through resellers.

**Go direct (or reconsider) when**:

- You need a **first-party capability the gateway does not expose** — a
  parameter, resolution, region, private-model hosting, or SLA the reseller
  has not surfaced. Gateways expose a curated subset of each model's surface.
- You need **contractual data-processing terms, HIPAA/regional residency, or a
  signed DPA** that the gateway cannot pass through from the underlying vendor.
- You are at **very high, steady volume** where a direct committed-use contract
  beats per-call reseller margin.
- You need **the provider's own moderation posture** rather than the gateway's
  added moderation layer (see Content safety below).
- Latency is dominated by **gateway queueing/cold-start** overhead you cannot
  tune, and the direct API offers provisioned throughput.

Out of scope for this skill: direct model-provider APIs (Google Vertex/Gemini
Veo, Kling's own API, Runway, etc.), local/self-hosted inference, training or
fine-tuning, and image-only gateway use.

## The three reference gateways at a glance

*Volatile facts below verified 2026-07-10; re-verify model IDs, prices, and
limits before shipping — the catalogs and rate cards move frequently.*

| Dimension | fal.ai | Replicate | WaveSpeed |
|---|---|---|---|
| Positioning | Generative-media-first (image/video/audio/3D), latency-focused | General model marketplace (community + "official" curated models), broadest catalog | Speed/latency-optimized inference for media |
| Catalog size (self-reported) | 1,000+ models | 100+ official models plus a large community catalog | 700–1,000+ models |
| Submit endpoint | `https://queue.fal.run/{model-id}` | `https://api.replicate.com/v1/predictions` (community) or `.../v1/models/{owner}/{name}/predictions` (official) | `https://api.wavespeed.ai/api/v3/{model-id}` |
| Async job states | `IN_QUEUE` → `IN_PROGRESS` → `COMPLETED` | `starting` → `processing` → `succeeded`/`failed`/`canceled` | `created` → `processing` → `completed`/`failed` |
| Sync option | Queue is the primary path; short models also have a run endpoint | `Prefer: wait` header (default 60s) for sync | Poll or webhook; result endpoint |
| Billing basis | Per-output (per-second or per-video for video); GPU-per-second fallback | Per-output for official models; per-second GPU time for community models | Per-model per-run, scales with resolution/duration/count |
| Balance model | Prepaid credits | Prepaid credit (hard cap at $0 for new accounts) | Prepaid credits (non-expiring) |
| Charged on failure? | No — pay only for successful output | Community models bill for GPU time even on model errors; official models bill per output | Pay per use; check per-model behavior |
| Schema discovery | Model-endpoints API with `expand=openapi-3.0` | `openapi_schema` on the model version object | Per-model playground / API examples |

Sources: fal queue and pricing docs; Replicate HTTP API and pricing docs;
WaveSpeed predictions and pricing docs (see Sources).

**Reading the table:** the three overlap heavily on *what* you can call — the
same headline models (Veo, Kling, Seedance) appear on all three — so
differentiation is mostly in the *operational contract*: billing granularity,
whether failures cost money, how you discover a schema, and how versions are
pinned. Treat the catalog as necessary but not sufficient; the operational
contract is where integrations succeed or fail.

## The async job contract (the core of every gateway)

Video generation is slow (seconds to minutes), so every gateway is
fundamentally an **asynchronous job queue**. Do not build on a synchronous
request that blocks until the video is done — you will hit timeouts and lose
work. The universal shape:

1. **Submit** a job → receive a job/request ID immediately.
2. **Await** completion by **webhook** (preferred) or **polling** (fallback).
3. **Fetch** the result (a hosted media URL) and **download/persist** it before
   it expires.

### fal.ai queue

- **Submit:** `POST https://queue.fal.run/{model-id}` with header
  `Authorization: Key $FAL_KEY`. Returns `request_id`, `response_url`,
  `status_url`, `cancel_url`, `queue_position`.
- **Status:** `GET https://queue.fal.run/{model-id}/requests/{request_id}/status`
  (append `?logs=1` for runner logs). States: `IN_QUEUE`, `IN_PROGRESS`,
  `COMPLETED`.
- **Result:** `GET https://queue.fal.run/{model-id}/requests/{request_id}`.
- **Cancel:** `PUT .../requests/{request_id}/cancel` — removes queued jobs
  immediately; in-progress jobs get a best-effort cancel signal.
- Documented guarantee: "requests in the queue are never dropped."
- *Verified 2026-07-10 from fal queue docs.*

### Replicate predictions

- **Submit (community):** `POST https://api.replicate.com/v1/predictions`
  with a `version` field. **Submit (official):**
  `POST https://api.replicate.com/v1/models/{owner}/{name}/predictions`
  (no version needed).
- **Sync shortcut:** add `Prefer: wait` (or `Prefer: wait=5`) to hold the HTTP
  connection up to 60s and return output inline for fast models — not suitable
  for multi-minute video.
- **Deadline:** `Cancel-After` header (5s–24h) auto-cancels the prediction
  itself (distinct from `Prefer: wait`, which only bounds the HTTP wait).
- **Status/result:** poll the URL in `urls.get` until `succeeded` or `failed`;
  `output` is null until done. Web debug view at `urls.web`.
- *Verified 2026-07-10 from Replicate HTTP/create-prediction docs.*

### WaveSpeed predictions

- **Submit:** `POST https://api.wavespeed.ai/api/v3/{model-id}` → returns a
  task/prediction ID.
- **Result:** `GET https://api.wavespeed.ai/api/v3/predictions/{id}/result`.
  States: `created`, `processing`, `completed`, `failed`. `outputs` holds
  result URLs; `timings.inference` gives duration in ms.
- Data retention: predictions available for **7 days** (verified 2026-07-10);
  persist outputs promptly.
- *Verified 2026-07-10 from WaveSpeed get-result docs.*

### Webhooks vs polling (production heuristic)

Prefer **webhooks** for video: a minutes-long poll loop wastes requests and
risks rate limits, and holding a connection open is fragile. Fall back to
polling only when you cannot expose a public HTTPS endpoint (local dev,
locked-down networks). If you poll, back off — image tasks ~2s, video tasks
~5s, then widen the interval (WaveSpeed's documented guidance, and a sound
default everywhere). Never poll a single job multiple times per second.

Design every webhook handler to be **idempotent**: gateways retry deliveries
and may deliver more than once for the same job ID.

## Webhook security and reliability

Webhook payloads arrive from the public internet — verify them.

**fal.ai** signs webhooks with **ED25519**. To verify (verified 2026-07-10):

1. Read headers `X-Fal-Webhook-Request-Id`, `X-Fal-Webhook-User-Id`,
   `X-Fal-Webhook-Timestamp`, `X-Fal-Webhook-Signature` (hex).
2. Fetch the JWKS from `https://rest.fal.ai/.well-known/jwks.json` and cache it
   up to 24h.
3. Reject if the timestamp is outside ±300s (5 min) of now.
4. Reconstruct the signed message (request ID + user ID + timestamp +
   SHA-256 of the raw body, newline-joined) and verify the signature against
   the JWKS ED25519 public keys.
5. Optionally IP-allowlist using `webhook_ip_ranges` from
   `https://api.fal.ai/v1/meta`.

fal delivery/retry (verified 2026-07-10): initial delivery timeout **15s**;
on failure it retries **10 times over 2 hours**. The success payload carries
`status: "OK"`, results, and a `seed`; a request error carries
`status: "ERROR"`; a serialization failure sets `payload: null` with a
`payload_error`. The `request_id` is stable across retries; `gateway_request_id`
reflects the latest attempt.

**Replicate** lets you filter which events fire via `webhook_events_filter`
(e.g. `["completed"]`); `start` and `completed` are always sent. Replicate
supports webhook signature verification via a signing secret — verify before
trusting a payload. (Verify current mechanism in Replicate's webhook docs
before shipping; verified conceptually 2026-07-10.)

**WaveSpeed** delivers a POST with `id`, `model`, `input`, `outputs` (on
`completed`), `urls.get`, `status`, and `error` (on failure). Confirm current
signing details in WaveSpeed's webhook docs before relying on them.

## Schema discovery per model

Each model exposes a different input surface (resolution enums, duration caps,
image/video reference slots, audio toggles, seed, negative prompt). Never
hardcode assumptions — **discover the schema** so your integration validates
inputs and adapts when a model updates.

- **fal.ai:** the model-endpoints API accepts `expand=openapi-3.0` and returns
  the full **OpenAPI 3.0** schema for an endpoint in the `openapi` field. Query
  by `endpoint_id` (e.g. `fal-ai/veo3`) to get JSON Schema for every input
  parameter. Use list/search modes to enumerate the catalog. (Verified
  2026-07-10.)
- **Replicate:** fetch the model version object at
  `/v1/models/{owner}/{name}/versions/{version_id}` and read
  `openapi_schema.components.schemas` for the `Input` and `Output` schemas.
  (Verified 2026-07-10.)
- **WaveSpeed:** each model's page/playground exposes the parameter set and
  auto-generates Python/JS/cURL examples; there is no single documented
  cross-catalog OpenAPI export as of 2026-07-10 — treat per-model docs as the
  source of truth.

**Heuristic:** cache the discovered schema per `(model-id, version)` and
re-fetch on a version change or on the first `422`/validation error. Building a
small schema-validation layer in front of the gateway catches
parameter-shape breakage before you spend money on a failed job.

## Version pinning and deprecation

Reproducibility is the reason to care about versions: the same prompt on a
silently-updated model can produce different motion, framing, or quality.

- **Replicate** has the most explicit model: community models are addressed as
  `{owner}/{model}:{64-char-version-hash}`. Pinning the hash guarantees
  identical behavior over time; omitting it (or using an **official** model
  addressed as `{owner}/{model}` with no hash) means Replicate keeps you on the
  latest maintained version. **Trade-off:** pin the hash for reproducibility
  and to avoid surprise behavior changes; use the unpinned official-model form
  when you want automatic upgrades and less maintenance. Replicate documents
  pinning as a reproducibility best practice. (Verified 2026-07-10.)
- **fal.ai** and **WaveSpeed** address models by a stable string ID (e.g.
  `fal-ai/veo3`, or versioned IDs like `fal-ai/kling-video/v2/...`). Version
  granularity is encoded in the ID the vendor publishes; watch changelogs for
  new IDs and deprecations of old ones.

**Deprecation is a real operational risk on gateways, not a hypothetical.**
Underlying models are retired or superseded (a new Kling/Veo/Seedance version
lands and the old endpoint is sunset). Mitigations (heuristics):

- Track each gateway's **changelog** and pin to explicit versioned IDs where
  offered.
- Keep a **config-driven model map** (env/config, not inline strings) so a
  deprecated ID is a one-line change, not a code hunt.
- Add a **catalog/health probe** in CI that resolves each model ID you depend on
  and alerts when one stops resolving or its schema changes.
- Maintain a **named fallback model per capability tier** so a sunset endpoint
  degrades to a substitute instead of failing the pipeline.

## Spend controls

Video is the most expensive generative modality per call, and gateway spend can
run away fast under retries or a bad loop. Controls differ sharply:

- **fal.ai:** **prepaid credits** are the primary cap — you cannot spend past
  your balance. You **pay only for successful outputs**; you are not charged for
  server errors (HTTP 500+) or time spent queued. fal's own docs do not
  advertise per-project budget alerts as of 2026-07-10 — build your own spend
  accounting from the billing/platform APIs.
- **Replicate:** **monthly spend limits were deprecated (July 1, 2025)**;
  **prepaid credit is now the hard cap** — work stops at a $0 balance (prepaid
  credit for new accounts since July 16, 2025). There are **no native budget
  alerts** post-deprecation; low-balance alerting is left to you or third-party
  tools. Note the failure-billing asymmetry: **community models bill for GPU
  seconds even when the model errors**, so a crash-looping community model
  still costs money; official models bill per output. (Verified 2026-07-10.)
- **WaveSpeed:** **prepaid, non-expiring credits**; usage-based per-model
  pricing where cost scales with resolution, duration, and output count. The
  cost estimate is shown before you run, and can be queried via the pricing
  API. Monthly credit lines exist for approved/enterprise accounts. (Verified
  2026-07-10.)

**Production heuristics for cost safety:**

- Keep the **working balance small** and top up deliberately — prepaid balance
  is your real circuit breaker on all three.
- **Estimate before you submit**: video cost scales with **duration ×
  resolution × output count (× audio, on some models)**. A 8s 1080p Veo clip
  with audio is dramatically pricier than a 5s 720p Kling clip — know the unit
  price. Example (fal, verified 2026-07-10): Veo 3.1 is billed ~$0.20/s at
  720p/1080p without audio and ~$0.40/s with audio; Kling 2.5 Turbo Pro
  ~$0.07/s. Prices change — re-verify.
- **Cap concurrency and retries** in your own code; an unbounded retry loop on
  a failing model is the classic runaway on any prepaid gateway.
- **Prefer gateways/models that do not charge for failures** for
  experimentation, and prefer per-output over per-GPU-second when your job
  latency is unpredictable.
- **Instrument cost per job** (job ID → model → parameters → charge) so you can
  attribute and alert; do not rely on the gateway to warn you.

## Retries and cross-gateway failover

**Retries.** Transient failures (429 rate limit, 5xx, capacity/cold-start
timeouts) are expected. Retry with **exponential backoff and jitter**, an
idempotency key you control, and a **cap** (both attempts and total spend).
Because a submitted-but-slow job is not the same as a failed job, distinguish
"submit failed" (safe to retry) from "job running slowly" (poll/await, do not
resubmit — resubmitting double-charges). Honor `Retry-After` when present.

**Cross-gateway failover.** Because the same headline models appear on multiple
gateways, a gateway is a **substitutable route**, which is the strongest
operational argument for the aggregator pattern. To fail over:

- Abstract behind a **capability interface** (`generateVideo(prompt, tier,
  constraints)`), not a gateway-specific call, so the router picks a
  provider+model.
- Maintain a **model map per capability tier** across ≥2 gateways (e.g.
  "premium cinematic" → Veo on fal *or* Veo on Replicate; "volume" → Seedance on
  WaveSpeed *or* Kling on fal).
- **Normalize** at the seams: each gateway has its own auth, submit shape,
  status vocabulary, parameter names, and result JSON. Failover only works if
  you translate inputs/outputs to a canonical form.
- **Watch for output drift:** the same model on two gateways can differ in
  exposed parameters, default resolution, moderation, or even minor pipeline
  details. Failover preserves *availability*, not necessarily *identical
  output* — treat a failover result as a near-substitute, not a bit-identical
  one, and re-verify quality-critical shots.
- Keep **separate prepaid balances and keys** funded on each gateway so failover
  is not blocked by a zero balance on the backup.

## Content-safety behavior differs by gateway

Two moderation layers stack: the **underlying model's** own safety behavior and
the **gateway's** added moderation. They are not identical across gateways, so
the *same prompt on the same model* can be accepted on one gateway and blocked
on another.

- **fal.ai** integrates **OpenAI's Omni moderation API** for real-time
  filtering, maintains an NSFW content policy, and partners with NCMEC/Thorn
  (CSAM) and StopNCII (NCII). Some image models expose an
  `enable_safety_checker` toggle (default on); video-model moderation posture
  is model-dependent. Users remain bound by fal's Acceptable Use Policy.
  (Verified 2026-07-10.)
- **Replicate** enforces its terms and the underlying model's restrictions;
  moderation strictness is largely inherited from the specific model.
- **WaveSpeed** applies its own acceptable-use terms atop each model.

**Heuristics:** (1) test moderation behavior **per gateway**, not once — a
prompt cleared on your primary may be refused on your failover route, breaking
availability assumptions. (2) Handle a **moderation rejection distinctly** from
a transient error — it is deterministic, so retrying or failing over the *same*
prompt often just fails or double-charges; instead surface it, adjust the
prompt, or route to a model with a different policy. (3) Do not assume a gateway
strips or adds a watermark, C2PA/provenance signal, or safety filter the same
way the direct API does — verify.

## Data governance and commercial-rights passthrough

**Two separate questions:** where does your data live, and who may use the
output commercially.

**Data retention / residency:**

- **fal.ai:** input uploads and output media go to fal's CDN
  (`v3.fal.media/...`). Retention is controllable via the
  `X-Fal-Object-Lifecycle-Preference` header (`expiration_duration_seconds`, or
  `null` for no expiry). Request/response JSON is stored **30 days** by default.
  Download outputs before they expire — expired files are unrecoverable.
  (Verified 2026-07-10.)
- **Replicate:** for API-created predictions, input params, outputs, and logs
  are **auto-removed after ~1 hour by default** — you must persist outputs
  yourself. (Verified 2026-07-10.)
- **WaveSpeed:** predictions retained **7 days**. (Verified 2026-07-10.)

Because outputs are transient, **always download and re-host** anything you
need; never link end users directly to a gateway CDN URL for durable content.
For regulated data, confirm whether the gateway can offer a DPA or regional
processing — most reseller flows send your inputs to third-party model infra.

**Commercial-rights passthrough (the critical governance point):** a gateway
granting you rights to *its service output* does **not** override the
**underlying model's license**. Rights flow through the model, not the gateway.

- **Replicate's terms** grant you "all right, title and interest" in the Output
  including commercial use — **but explicitly subject to Third-Party Terms
  determined by the model you used.** Some models (e.g. permissive ones like
  Stable Diffusion) impose no ownership claim; others restrict commercial use.
  (Verified 2026-07-10.)
- The same logic applies on fal and WaveSpeed: the **model card / underlying
  vendor license** governs whether you may use a clip commercially, whether
  attribution is required, and whether the vendor asserts training or usage
  rights over your inputs.

**Heuristic:** before using a gateway-generated video commercially, resolve the
**underlying model's license and the model provider's terms**, not just the
gateway's ToS. Premium models (Veo, Kling) frequently carry provider-specific
commercial terms and per-clip restrictions; a gateway reselling them does not
relax those terms. Record, per model you ship on, the license basis for
commercial use so a later dispute or model swap is auditable.

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| Submit returns fast but no video | Working as designed — it is async; you got a job ID, not a result | Poll `status`/`result` or await the webhook; do not treat the submit response as the output |
| Webhook never arrives | Endpoint not public HTTPS, handler slow (>15s on fal), or signature check rejecting valid payloads | Verify reachability, respond quickly then process async, confirm signature logic; fall back to polling |
| Duplicate results processed | Gateway retried delivery | Make the handler idempotent keyed on job/request ID |
| `422`/validation error | Wrong parameter shape for this model/version | Re-fetch the model schema (fal `openapi-3.0`, Replicate `openapi_schema`); validate inputs before submit |
| Charged but no usable output | Community-model GPU-time billing on error (Replicate), or output expired before download | Prefer pay-per-output models for flaky work; download outputs immediately; check retention window |
| Model ID stopped resolving | Version deprecated/sunset | Update the config-driven model map to the new versioned ID or fail over to the tier fallback |
| Prompt blocked on one gateway, fine on another | Different stacked moderation layers | Treat as deterministic; adjust prompt or route to a different-policy model — do not blind-retry |
| Runaway spend | Unbounded retries or a bad loop against a prepaid balance | Cap retries/concurrency, keep balance small, instrument per-job cost |
| Output looks different after a "no-op" change | Unpinned version silently updated | Pin explicit version hashes/IDs; add a schema/behavior probe in CI |
| Result URL 404s later | Gateway CDN retention elapsed | Re-host durable content; never serve end users a raw gateway URL |

## Complete examples (illustrative — verify IDs/prices before use)

### Example A — Choose a route for a batch of short social clips

**Intent:** generate 500 five-second 720p vertical clips/day, cost-sensitive,
some prompts near content-policy edges, must not exceed a fixed daily budget.

**Reasoning:** volume + cost sensitivity favors a per-second/per-run model on a
gateway that (a) does not charge for failures and (b) supports a hard prepaid
cap. Pick a mid-tier model (e.g. a Kling/Seedance turbo tier) rather than Veo.
Put a **second gateway** behind the same capability tier for failover, since
availability of a single model on a single gateway is not guaranteed at 500/day.

**Plan:** primary = fal `queue.fal.run` submit + ED25519-verified webhook,
prepaid balance sized to the daily budget as the circuit breaker; secondary =
same-tier model on WaveSpeed with its own funded balance. Router picks by
health + queue depth. Per-job cost is logged (job ID → model → params → charge).
Moderation rejections are surfaced to a review queue, **not** retried.

**Expected result:** clips delivered async, budget bounded by prepaid balances,
a sunset or outage on one route degrades to the other. **Failure modes:**
forgetting to fund the backup balance (failover silently fails); blind-retrying
moderation rejections (wasted spend); serving raw CDN URLs that later 404.

### Example B — Pin a reproducible cinematic model on Replicate

**Intent:** a hero shot must render identically across months for a marketing
pipeline; commercial use required.

**Plan:**

1. Resolve the exact version: `GET /v1/models/{owner}/{name}/versions` and pick
   the hash; store `{owner}/{name}:{version_hash}` in config.
2. Submit `POST /v1/predictions` with that pinned `version`, a `webhook`, and
   `webhook_events_filter: ["completed"]`; set a `Cancel-After` deadline as a
   spend guard.
3. Discover/validate inputs against
   `openapi_schema.components.schemas.Input` before submitting.
4. On completion, **download and re-host** the video within the ~1-hour
   retention window.
5. **Rights check:** confirm the underlying model's Third-Party Terms permit
   commercial use, and record that basis, before publishing.

**Why structured this way:** pinning the hash locks reproducibility; the
schema check prevents parameter drift from silently changing output; the
retention-aware download prevents a lost result; the rights check prevents
shipping a clip whose model license forbids commercial use. **Failure modes:**
using the unpinned official-model form (auto-upgrades break reproducibility);
assuming Replicate's ownership grant overrides the model's restrictive license.

### Example C — Discover a model's schema before integrating (fal)

**Intent:** integrate a video model you have not used; you do not know its
duration cap, resolution enum, or whether it takes an image reference.

**Plan:** call the fal model-endpoints API with `endpoint_id` set to the model
(e.g. `fal-ai/veo3`) and `expand=openapi-3.0`; read the returned `openapi`
field's JSON Schema for the input object. Generate your request typing and a
validation layer from it; cache it keyed on the model ID; re-fetch on the first
`422` or a changelog-announced version bump.

**Why:** this makes the integration self-describing and resilient to the model
adding/renaming a parameter, instead of hardcoding a guessed body that breaks
on the next model update. **Failure mode:** skipping discovery and hardcoding
parameters copied from a blog post that lags the current schema.

## Sources

All URLs verified 2026-07-10.

- fal.ai queue API — https://fal.ai/docs/model-apis/model-endpoints/queue
- fal.ai webhooks (ED25519, retries, JWKS) — https://fal.ai/docs/model-apis/model-endpoints/webhooks
- fal.ai pricing / prepaid credits / pay-per-success — https://fal.ai/docs/documentation/model-apis/pricing and https://fal.ai/pricing
- fal.ai model search / OpenAPI schema discovery — https://fal.ai/docs/platform-apis/v1/models and https://docs.fal.ai/model-apis/model-endpoints
- fal.ai data retention / media expiration header — https://fal.ai/docs/documentation/model-apis/media-expiration
- fal.ai Trust & Safety (OpenAI Omni moderation, NCMEC/Thorn/StopNCII) — https://fal.ai/legal/trust-and-safety
- fal.ai Acceptable Use Policy — https://fal.ai/legal/acceptable-use-policy
- Replicate create-a-prediction (sync/async, Prefer, Cancel-After, webhook_events_filter) — https://replicate.com/docs/topics/predictions/create-a-prediction
- Replicate HTTP API reference (version formats, openapi_schema, rate limits, ~1h retention) — https://replicate.com/docs/reference/http
- Replicate model versions (pinning, reproducibility) — https://replicate.com/docs/topics/models/versions
- Replicate official models — https://replicate.com/docs/topics/models/official-models
- Replicate pricing (per-second GPU hardware, per-output official) — https://replicate.com/pricing
- Replicate billing (spend-limit deprecation, prepaid credit) — https://replicate.com/docs/topics/billing
- Replicate rate limits — https://replicate.com/docs/topics/predictions/rate-limits
- Replicate Terms of Service (Output ownership, Third-Party Terms) — https://replicate.com/terms
- WaveSpeed predictions / get-result (endpoints, states, 7-day retention) — https://wavespeed.ai/docs/get-result and https://wavespeed.ai/docs/what-are-predictions
- WaveSpeed pricing (per-model, credits) — https://wavespeed.ai/docs/how-pricing-works and https://wavespeed.ai/pricing
- WaveSpeed webhooks — https://wavespeed.ai/docs/docs-api/webhooks (confirm current signing/retry details before shipping)

Model-specific prices (Veo 3.1 ~$0.20–0.60/s by resolution/audio; Kling 2.5
Turbo Pro ~$0.07/s) are from fal's pricing pages, verified 2026-07-10, and are
volatile — always re-verify against the live rate card.
