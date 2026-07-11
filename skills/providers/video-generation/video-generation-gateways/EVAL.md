# EVAL — video-generation-gateways

Answer key and scoring specification. The evaluated agent receives only the
user task plus `SKILL.md`; it must never see this file. The evaluator scores
the captured response against the criteria below.

Facts referenced here were verified 2026-07-10. If a volatile fact (endpoint,
price, retention window, billing rule) has changed since, re-verify before
penalizing an answer that reflects newer reality; reward answers that
correctly flag a fact as volatile and requiring re-verification.

---

## Section 1 — Knowledge questions

### K1. What is a video-generation gateway, and how does it differ from a direct model-provider API?

**Expected answer:** A hosted inference aggregator that resells many
third-party video (and video-adjacent audio) models behind one account, one API
convention, and one bill (fal.ai, Replicate, WaveSpeed). You call a
gateway-owned endpoint; the gateway runs the underlying model on its infra and
returns a hosted result. A direct API is the model vendor's own first-party
endpoint (e.g. Google Veo via Vertex, Kling's own API).

**Required points:** aggregator of multiple models; single API/account/bill;
runs on gateway infra; returns hosted result URL; contrast with first-party
direct API.

**Disqualifying claims:** describing it as local/self-hosted inference; claiming
a gateway is the model's owner; conflating with a training platform.

### K2. Why is every video-generation gateway fundamentally asynchronous, and what is the universal job shape?

**Expected answer:** Video generation takes seconds to minutes, so a blocking
synchronous request would time out. Universal shape: **submit → receive job/
request ID → await via webhook (preferred) or polling → fetch hosted result →
download/persist before it expires.**

**Required points:** async because generation is slow; submit returns an ID not
a result; webhook or polling to await; fetch + persist result.

**Disqualifying claims:** treating the submit response as the finished video;
recommending a synchronous blocking call as the default for multi-minute video.

### K3. Give the submit endpoint and the async status states for each of fal.ai, Replicate, and WaveSpeed.

**Expected answer:**
- fal.ai: `POST https://queue.fal.run/{model-id}`; states `IN_QUEUE` →
  `IN_PROGRESS` → `COMPLETED`.
- Replicate: `POST https://api.replicate.com/v1/predictions` (community, with a
  `version`) or `.../v1/models/{owner}/{name}/predictions` (official); states
  `starting` → `processing` → `succeeded`/`failed`/`canceled`.
- WaveSpeed: `POST https://api.wavespeed.ai/api/v3/{model-id}`; states
  `created` → `processing` → `completed`/`failed`; result at
  `.../v3/predictions/{id}/result`.

**Required points:** correct endpoint host per gateway; correct terminal-state
vocabulary per gateway (do not require exact non-terminal names, but the
distinct vocabularies must be recognized).

**Partial credit:** correct endpoints but mixed-up state names → half.

### K4. How does fal.ai secure webhooks, and what are its delivery/retry parameters?

**Expected answer:** ED25519 signatures. Verify by reading the
`X-Fal-Webhook-*` headers (Request-Id, User-Id, Timestamp, Signature), fetching
JWKS from `https://rest.fal.ai/.well-known/jwks.json` (cacheable ≤24h),
rejecting timestamps outside ±300s, reconstructing the signed message
(request ID + user ID + timestamp + SHA-256 of body) and verifying against the
JWKS public keys. Optional IP allowlist via `webhook_ip_ranges`. Delivery:
15-second initial timeout; on failure retries 10 times over 2 hours. `request_id`
is stable across retries.

**Required points:** ED25519; JWKS fetch/verify; timestamp tolerance; 15s
timeout; 10 retries / 2 hours; handler must be idempotent.

**Disqualifying claims:** "webhooks are unauthenticated/trust the payload
as-is"; inventing HMAC-SHA256 as fal's mechanism without noting uncertainty.

### K5. How do you discover a model's input schema on fal.ai and on Replicate?

**Expected answer:** fal.ai — call the model-endpoints/model-search API with
`expand=openapi-3.0`; the OpenAPI 3.0 schema comes back in the `openapi` field
for the given `endpoint_id`. Replicate — fetch the model version object
(`/v1/models/{owner}/{name}/versions/{version_id}`) and read
`openapi_schema.components.schemas` for `Input`/`Output`.

**Required points:** fal `expand=openapi-3.0`; Replicate `openapi_schema` on the
version object; both are JSON-Schema-based; discover rather than hardcode.

### K6. Explain Replicate version pinning and its trade-off.

**Expected answer:** Community models are addressed
`{owner}/{model}:{64-char-version-hash}`. Pinning the hash guarantees identical
behavior over time (reproducibility). Omitting it, or using an official model
addressed `{owner}/{model}` with no hash, keeps you on the latest maintained
version. Trade-off: pin for reproducibility and to avoid surprise behavior
changes; leave unpinned for automatic upgrades and lower maintenance.

**Required points:** hash pin = reproducible; unpinned/official = auto-updated;
the explicit trade-off.

**Disqualifying claims:** claiming pinning is impossible; claiming official
models require a version hash.

### K7. State the data-retention default for outputs on each gateway.

**Expected answer:** Replicate — API prediction inputs/outputs/logs auto-removed
after ~1 hour by default. fal.ai — request/response JSON stored ~30 days;
media on the CDN controllable via `X-Fal-Object-Lifecycle-Preference`.
WaveSpeed — predictions available ~7 days. In all cases: download/persist
outputs promptly; do not serve raw gateway CDN URLs for durable content.

**Required points:** Replicate ~1h; fal ~30 days JSON + configurable media;
WaveSpeed ~7 days; must-download implication.

### K8. Who owns a gateway-generated video's commercial rights?

**Expected answer:** The gateway's ToS may grant you the output (Replicate
grants "all right, title and interest," including commercial use), **but always
subject to the underlying model's Third-Party Terms.** Rights flow through the
model, not the gateway. Premium models (Veo, Kling) often carry
provider-specific commercial restrictions the gateway does not relax.

**Required points:** gateway grant is subject to model license; must check the
underlying model/provider terms; gateway ToS does not override the model.

**Disqualifying claims:** "the gateway grants full unconditional commercial
rights"; ignoring the underlying model license entirely.

---

## Section 2 — Production-decision questions

### D1. A team wants Veo-quality hero shots plus high-volume cheap clips plus an upscale step, all in one pipeline, and doesn't want three vendor contracts. Gateway or direct? Which and why?

**Expected decision:** Use a gateway. Multiple models behind one integration,
one bill, one async contract, model-shopping without re-plumbing — this is the
canonical gateway case.

**Reasoning a strong answer shows:** names the multi-model-one-integration
benefit; notes the single async contract; notes CDN hosting of inputs/outputs;
correctly does **not** recommend direct APIs given the stated no-contract
constraint; may note a caveat that if a needed parameter/region/SLA is missing,
selectively go direct for that one capability.

**Penalize:** recommending three direct integrations despite the explicit
constraint; ignoring that the same models are resell-able across gateways.

### D2. When should the team go direct instead, even though a gateway would work?

**Expected decision:** Go direct when they need a first-party capability the
gateway doesn't expose (parameter/resolution/region/private hosting/SLA); need a
signed DPA / regional data residency / regulated-data terms the reseller can't
pass through; are at very high steady volume where a committed-use contract
beats reseller margin; need the provider's own moderation posture; or when
gateway queue/cold-start latency is untunable and the direct API offers
provisioned throughput.

**Reasoning:** at least three distinct, correct reasons; recognizes gateways
expose a curated subset; connects the choice to concrete constraints.

**Penalize:** "always use a gateway" with no direct-route awareness; citing cost
alone without the volume/margin nuance.

### D3. A prompt renders fine on the primary gateway but is blocked on the failover gateway for the same model. What is happening and how should the pipeline handle it?

**Expected decision:** Two stacked moderation layers (underlying model + gateway)
differ across gateways, so the same prompt/model can be accepted on one and
refused on another. Handle a moderation rejection as **deterministic**, distinct
from a transient error: do **not** blind-retry or blind-failover the same
prompt (it will just fail again and may double-charge); surface it, adjust the
prompt, or route to a model with a different policy. Recognize that failover
preserves availability but not identical moderation behavior.

**Reasoning:** identifies stacked/differing moderation; deterministic vs
transient distinction; correct handling (no blind retry); notes failover
availability ≠ identical policy/output.

**Penalize:** treating a moderation block as a retryable transient error;
assuming moderation is identical across gateways.

### D4. On a fixed monthly budget with flaky experimental prompts, how do you keep spend bounded across these gateways?

**Expected decision:** Prepaid balance is the real circuit breaker on all three
— keep the working balance small and top up deliberately. Prefer
pay-per-successful-output models/gateways for experimentation (fal doesn't
charge for failures; Replicate **community** models bill GPU seconds even on
model error, so a crash-looping community model still costs money — prefer
official/per-output there). Cap retries and concurrency in your own code.
Estimate cost before submit (duration × resolution × output count × audio).
Instrument per-job cost; don't expect native budget alerts (Replicate deprecated
spend limits July 2025; fal has no advertised per-project alerts).

**Reasoning:** prepaid-cap-as-breaker; the failure-billing asymmetry
(Replicate community models); retry/concurrency caps; pre-submit estimation;
own instrumentation because native alerts are limited/absent.

**Penalize:** relying on native budget alerts as the primary control; ignoring
that community-model errors on Replicate still bill; unbounded retries.

### D5. A hero shot must render identically for a year. What do you set up, and what governance step is easy to forget?

**Expected decision:** Pin an explicit version — on Replicate the 64-char
version hash (`owner/model:hash`), not the unpinned official form; on fal/
WaveSpeed the explicit versioned model ID. Validate inputs against the
discovered schema; add a CI probe that alerts on schema/version drift; download
and re-host each result within the retention window. Easy-to-forget governance
step: confirm the **underlying model's Third-Party Terms permit commercial use**
and record that basis — the gateway's ownership grant does not override it.

**Reasoning:** explicit pinning for reproducibility; schema-drift protection;
retention-aware persistence; the commercial-rights passthrough check.

**Penalize:** using an auto-updating unpinned model for a reproducibility
requirement; assuming the gateway ToS settles commercial rights.

---

## Section 3 — Applied production tasks

### T1. Design the integration for 500 five-second 720p vertical clips/day, cost-capped, with some edge-of-policy prompts.

**User request:** "Build the plan for generating ~500 short vertical clips a day
through gateways. We have a hard daily budget and some prompts flirt with the
content policy. It must not fall over if one provider has an outage."

**Expected approach:** Pick a mid-tier per-second/per-run model (Kling/Seedance
turbo class), not Veo, on a gateway that doesn't charge for failures; async
submit + webhook (verified signature); prepaid balance sized to the daily budget
as the hard cap; a **second gateway** funded and mapped to the same capability
tier for failover behind a capability interface; per-job cost logging;
moderation rejections routed to a review queue, not retried; outputs downloaded/
re-hosted promptly.

**Essential characteristics of a successful output:**
- Async submit + webhook (with idempotent, signature-verified handler) or a
  backed-off poll fallback.
- Prepaid balance(s) as the budget circuit breaker; both primary and backup
  funded.
- Capability-interface abstraction with a ≥2-gateway model map per tier.
- Cost estimation before submit and per-job cost instrumentation.
- Moderation rejections handled deterministically (surface/adjust, not retry).
- Retention-aware download/re-host.

**Scoring rubric (10 pts):** async+webhook design 2; prepaid-cap budgeting 2;
cross-gateway failover with funded backup + abstraction 2; cost estimation +
instrumentation 1; deterministic moderation handling 2; download/persist +
model choice appropriateness 1.

**Critical failures (cap at ≤3/10):** synchronous/blocking design;
blind-retrying moderation blocks; unbounded retries against a prepaid balance;
failover to an unfunded backup (silent failure); serving raw CDN URLs as durable
content.

### T2. Write the resilient submit-and-await logic (pseudocode) for one gateway, retry-safe.

**User request:** "Show the submit → await → fetch logic against fal or
Replicate that won't double-charge on retries and won't hang."

**Expected approach:** Submit once, capture the job/request ID. Distinguish
"submit failed" (safe to retry, with backoff + jitter + cap, honoring
`Retry-After`) from "job running slowly" (poll/await; never resubmit — that
double-charges). Prefer webhook; if polling, back off (~5s for video, widening).
Idempotent completion handler keyed on job ID. Set a spend-guard deadline
(Replicate `Cancel-After`; or app-side timeout). On completion, download/persist
the output URL before retention expiry.

**Essential characteristics:**
- Single submit; resubmission only on confirmed submit failure.
- Backoff + jitter + attempt cap; `Retry-After` honored.
- Webhook-preferred, poll-with-backoff fallback.
- Idempotency keyed on job/request ID.
- Deadline/timeout guard.
- Persist output before expiry.

**Scoring rubric (10 pts):** submit-vs-slow distinction (no double-charge) 3;
backoff/jitter/cap 2; idempotent await/handler 2; webhook-vs-poll choice 1;
deadline guard 1; persist-before-expiry 1.

**Critical failures (cap at ≤3/10):** resubmitting a still-running job (double
charge); tight poll loop with no backoff; treating submit response as the
result; no idempotency.

### T3. Troubleshoot: "We're getting charged but often see no usable video, and sometimes the same prompt produces different output after a change we didn't intend."

**User request:** "Diagnose these two symptoms on our gateway pipeline."

**Expected approach:**
- *Charged but no output:* likely (a) Replicate **community-model** GPU-time
  billing on model errors — switch flaky work to pay-per-output/official
  models; and/or (b) outputs expired before download (Replicate ~1h) — download
  immediately, widen retention where configurable (fal media-lifecycle header).
- *Unintended output drift:* an **unpinned version silently updated** — pin the
  explicit version hash/ID; add a schema/behavior probe in CI; re-fetch schema
  on version bump.

**Essential characteristics:**
- Correctly attributes failure-billing to community-model GPU-second billing.
- Correctly ties output drift to unpinned versions.
- Concrete fixes: per-output models, immediate download/retention config,
  version pinning, CI drift probe.

**Scoring rubric (10 pts):** failure-billing diagnosis + fix 3; retention/
download diagnosis + fix 2; version-drift diagnosis 3; CI probe / schema
re-fetch 2.

**Critical failures (cap at ≤3/10):** attributing charges purely to a gateway
bug with no billing-model insight; recommending endless retries; not mentioning
version pinning for the drift.

### T4. A stakeholder wants to publish gateway-generated Veo clips in a paid ad campaign. What must be checked?

**User request:** "Legal-adjacent: can we run these Veo clips we made through the
gateway in a paid campaign?"

**Expected approach:** The gateway's ToS may grant output ownership, but it is
subject to the underlying model's Third-Party Terms — so resolve **Veo/Google's
model-provider commercial terms**, not just the gateway ToS. Check for
commercial-use permission, attribution/watermark/provenance requirements, and
any content restrictions; record the license basis per model shipped. Also
confirm data-governance implications (were proprietary inputs sent to
third-party model infra; retention). Flag that this is a rights question the
gateway does not settle; recommend confirming with the specific model card /
provider terms (and legal counsel for a paid campaign).

**Essential characteristics:**
- Identifies rights flow through the model, not the gateway.
- Names checking the specific underlying-model/provider commercial terms.
- Mentions attribution/watermark/provenance and input-data governance.
- Recommends recording the license basis; appropriate caution for commercial
  publication.

**Scoring rubric (10 pts):** model-license-governs-not-gateway 4; check specific
Veo/provider terms 2; attribution/provenance + data governance 2; record basis /
recommend caution-verification 2.

**Critical failures (cap at ≤3/10):** asserting the gateway ToS alone grants
unconditional commercial rights; ignoring the underlying-model license entirely.

---

## Global scoring notes

- Reward answers that **label volatile facts** (prices, endpoints, retention
  windows) as needing re-verification and cite the verification date.
- Reward answers that distinguish **documented facts** (endpoints, retry
  numbers, billing rules) from **production heuristics** (keep balance small,
  abstract behind a capability interface).
- Penalize confident invention of unverified specifics (e.g. a made-up webhook
  signing scheme, a fabricated price) presented as fact.
- An answer may exceed the skill by citing newer verified facts; do not penalize
  correctness that post-dates 2026-07-10 if it is accurate.
