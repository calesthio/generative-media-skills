# Adobe Firefly Image — hidden evaluation key

## Evaluator protocol

Give the evaluated agent the task and `SKILL.md` only. Do not reveal, quote, summarize, or link this file before capturing the response. Score evidence present in the captured response; do not award points for unstated intent. Accept equivalent correct wording and equally robust implementations.

The maximum is **100 points**:

- Knowledge and boundary checks: 30
- Production decisions: 25
- Applied production and executable implementation: 45

Use current first-party Adobe behavior as of 2026-07-09. When Adobe prose conflicts with the operation schema, reward an explicit reconciliation that gives the API reference and later changelog priority without pretending the conflict does not exist.

## Critical failures and score caps

Apply the single lowest applicable cap after item scoring:

- **Cap at 20:** exposes or requests embedding a client secret/access token in browser/public code; instructs evasion of safety filters or a 451 restriction; asserts that all Firefly output is automatically legally safe or indemnified; or uses supplied people/assets without a rights/consent check in a high-risk scenario.
- **Cap at 35:** builds a new integration on a removed synchronous Generate v3, Generate v2, Expand v1, or Fill v1 route; treats `/v4/images/generate-async` as a completed synchronous response and never polls/downloads; or sends an incompatible hybrid of v3 and v4 schemas as working code.
- **Cap at 50:** claims Image 5 supports four variations per request, v3 style/structure controls, or an arbitrary negative-prompt field; uses `creative_upsampler_v1` or `/v1/images/upsample-async` as the current upscale contract; or promises exact product preservation with Adaptive Composite without review.
- **Cap at 60:** fabricates a public per-image dollar price or universal indemnity; states a wrong default rate limit as fact; omits all provenance, privacy, and output-download handling from a production plan.
- **Cap at 70:** an architecture, model-selection, migration, or governance answer asserts consequential volatile facts without first-party support or any freshness date. Do not apply this cap to a correct pure implementation response merely because the user did not ask for a research memo; deduct only when its extra factual claims are unsupported.

Also deduct within items for smaller errors. Do not double-penalize the same defect unless it creates distinct risks.

## Knowledge and boundary checks — 30 points

### K1. Current model and route map — 8 points

**Question:** Describe the current Firefly still-image generation routes, model identifiers, and lifecycle boundaries.

**Expected answer:**

- Image 5 uses `POST /v4/images/generate-async`, header `x-model-version: image5`, and body `modelId: firefly_image`.
- Image 3/4 generation uses `POST /v3/images/generate-async` with header values `image3`, `image4_standard`, `image4_ultra`, `image3_custom`, or `image4_custom`; custom values require `customModelId`.
- Current still-image generation is asynchronous. V3 returns 202 with `jobId/statusUrl/cancelUrl`; v4 returns 200 with result/cancel links and progress but still requires polling.
- Deprecated synchronous v3 references were removed in October 2025; Generate v2, Expand v1, and Fill v1 were removed in September 2025.

**Scoring:**

- 2 points: correct v4 route and both model selectors.
- 2 points: correct v3 route and all five documented header values, including custom-ID requirement.
- 2 points: correct v3 versus v4 acceptance response and polling distinction.
- 2 points: correct lifecycle/deprecation boundary and refusal to build on removed routes.

**Incorrect/disqualifying:** calling `image5` a v3 model header; claiming v3 models are removed; treating HTTP 200 from v4 as completed image bytes.

### K2. Schema constraints — 7 points

**Question:** Contrast the important Image 5 and v3 request constraints.

**Expected answer:**

- V4 prompt 1–1500; aspect enum `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `auto`; resolution `1MP`, `2.4MP`, `4MP`; maximum one variation, one seed, and one reference.
- A non-empty v4 `referenceBlobs` changes the operation to instruct edit; aspect must be omitted or `auto`.
- V4 locale is in `modelSpecificPayload.localeCode`; reasoner is `speed` or `quality`; quality populates alt text.
- V3 prompt max 1024; 1–4 variations; seed count equals variation count; locale is `promptBiasingLocaleCode`; style/structure strength 1–100; `visualIntensity` 2–10.
- V3 negative prompt is unsupported for custom Image 3/4; v4 operation schema does not document a negative-prompt field.

**Scoring:**

- 2 points: v4 prompt/aspect/resolution limits.
- 2 points: v4 variation/reference/instruct-edit/aspect interaction.
- 1 point: locale/reasoner distinction and alt-text behavior.
- 1 point: v3 prompt/variation/seed/control limits.
- 1 point: negative-prompt boundary.

### K3. Editing, compositing, upload, and upscale — 7 points

**Question:** Choose and characterize the non-generation still-image operations.

**Expected answer:**

- Fill is masked localized replacement; Expand is canvas growth/outpainting; Generate Similar uses a source image; v4 instruct edit uses one general reference and natural-language edit.
- Generate Object Composite creates a background from a prompt; Precise Composite preserves the supplied object and uses an existing background/fill-area mask; Adaptive Composite may regenerate/adapt the object to fit an existing background.
- Upload uses `POST /v2/storage/image`, returns `images[0].id`, accepts up to 15 MB per current reference, and the upload ID is valid seven days.
- Current upscale is `POST /v3/images/upscale`, `precise_upsampler_v1`, factor 2/3/4/6, async; `creative_upsampler_v1` is rejected.

**Scoring:**

- 2 points: differentiates fill, expand, similar, and instruct edit.
- 2 points: differentiates all three composites by background availability and fidelity.
- 1 point: upload route/shape/validity.
- 2 points: current upscale route/model/factors/async lifecycle and stale-model rejection.

### K4. Access, governance, and provenance — 8 points

**Question:** State the current authentication, capacity, billing, privacy, indemnity, and provenance rules without overclaiming.

**Expected answer:**

- Server-side OAuth Server-to-Server; bearer token plus Client ID in `x-api-key`; tokens documented as 24 hours.
- Default limits are 4 RPM and 9,000 RPD per organization; use `Retry-After`/backoff and contact account manager for increases.
- Billing is in Operations under contract/Admin Console rate card; an action may cost multiple Operations; no universal public per-image dollar figure should be invented.
- Security sheet defaults: prompt/settings/pseudonymous ID 90 days, API reference inputs cached 24 hours, generated API images stored 24 hours, provenance hash/manifest may persist.
- Indemnity applies only if specifically contracted and only to eligible features/surfaces/export events, subject to terms and caps.
- Current 2026v2 terms restrict using Developer Tools or derived content/data/output to create/train/test/improve AI systems; external-facing Customer Software requires express Sales Order permission. Modification or combination of Firefly Output can exclude an indemnity claim.
- Content Credentials are automatically attached to fully Firefly-generated assets; they establish provenance context, not factual truth, ownership, consent, or non-infringement.

**Scoring:**

- 1 point: auth headers and server-side handling.
- 1 point: token lifetime.
- 1 point: both rate limits and organization scope.
- 1 point: Operations/rate-card pricing boundary.
- 2 points: accurate retention distinctions and immediate download recommendation.
- 1 point: current Sales Order/external-use and AI-training restrictions plus indemnity qualifiers, including downstream modification/combination risk.
- 1 point: Content Credentials scope and limitations.

## Production decisions — 25 points

### D1. Global campaign concepting — 9 points

**Scenario:** A team needs 30 concept images for a multilingual campaign, then one selected 4 MP hero. It wants fast iteration, controlled aspect ratios, regional relevance, and an audit trail. No reference image or custom model is required.

**Expected decision:**

- Use Image 5 v4, one request per variation. Use 1 MP or 2.4 MP for concepting only if the organization's cost/quality tests support that choice; rerun the selected seed/prompt at 4 MP rather than claiming a deterministic upscale.
- Use the required aspect enum and `modelSpecificPayload.localeCode`; have native/cultural review because locale bias is not translation.
- Consider `prompt_reasoner: speed` for concepts and `quality` for finals, while independently reviewing alt text.
- Build organization-wide rate control for 4 RPM, budget Operations from the actual rate card, store seeds/payload/model/job/source/output hashes, and download promptly.
- State that each payload is an example configuration, not a universal formula.

**Scoring:**

- 2 points: correct Image 5 route/model and one-request-per-variation plan.
- 2 points: sensible staged resolution/reasoner decision, explicitly conditioned on tests/cost.
- 1 point: correct aspect and locale handling plus native review.
- 2 points: rate/cost-aware queue and asynchronous lifecycle.
- 2 points: audit, output download, and QA plan.

**Penalize:** batch of 30 in one `numVariations`; invented negative prompt; assuming alt text is automatically publishable.

### D2. Regulated product composite — 8 points

**Scenario:** Place a medical-device package into a supplied clinic background. Every label pixel and regulatory mark must remain unchanged. Shadows may adapt. The background has a supplied placement mask.

**Expected decision:**

- Select Precise Composite, not Adaptive Composite or generic generation, because exact subject fidelity is the governing constraint.
- Use existing background + fill-area mask + object image. Tune `blend` through small samples; do not promise fidelity from the endpoint name.
- Require rights, regulated-claim review, pixel diff/label OCR or equivalent, seam/shadow inspection, exact-dimension check, and human approval.
- Preserve originals, payload/seeds/job IDs/hashes/provenance and reject any label change.

**Scoring:**

- 3 points: correct endpoint and reasoning against Adaptive Composite.
- 1 point: correct required inputs and `blend` role.
- 2 points: pixel/label/mask/lighting QA.
- 1 point: regulated-use and rights/human gate.
- 1 point: audit/provenance preservation.

**Critical failure:** choosing Adaptive Composite without acknowledging its subject alteration risk.

### D3. Lifestyle edit with a style reference — 8 points

**Scenario:** A brand wants four square variations that preserve the layout of a reference scene, borrow a second reference's color/lighting style, and exclude text. It later wants a single natural-language tweak to the selected image.

**Expected decision:**

- Use v3 Generate for the four-way structured/style-controlled exploration, with exact square size, four seeds, `structure.imageReference`, `style.imageReference`, strengths, and a documented preset only if useful.
- Upload references or use allowed pre-signed domains. Sweep strengths rather than maxing both blindly.
- Use a negative prompt for text on non-custom v3.
- After selection, use Image 5 v4 instruct edit for the natural-language tweak if one reference suffices; remove/set aspect to auto and use one variation. Alternatively use Fill if the tweak is localized and maskable, with rationale.

**Scoring:**

- 3 points: correct v3 exploration design and exact seed/variation match.
- 1 point: correct source upload/domain handling.
- 1 point: controlled strength experiment.
- 1 point: valid negative-prompt boundary.
- 2 points: correct v4 instruct-edit or mask-fill follow-up with schema transition.

## Applied production and executable implementation — 45 points

### A1. Implement a robust Image 5 client — 18 points

**User request:** “Write a complete Python script that authenticates, generates one 16:9 Image 5 image at 4 MP, waits for completion, downloads it safely, and handles production errors.”

**Essential characteristics:** executable code using environment variables, token exchange, both auth headers, correct route/header/body, v4 result-link polling under the organization-wide 4-RPM default, bounded timeout, 429/5xx backoff, terminal failure handling, content-type-aware download, and secret-free audit metadata.

**Rubric:**

- 3 points: reads Client ID/secret from environment and exchanges them at IMS with client-credentials form data; no secret logging.
- 3 points: `POST https://firefly-api.adobe.io/v4/images/generate-async`, `x-model-version: image5`, `modelId: firefly_image`, `aspectRatio: 16:9`, `resolutionLevel: 4MP`, one variation.
- 2 points: valid prompt and optional valid v4 fields only.
- 3 points: extracts and follows returned result link with the same bearer/API-key headers; handles completion and failure.
- 2 points: bounded polling/cancellation/timeout awareness and an organization-wide limiter that averages at least 15 seconds per Firefly request at the default entitlement.
- 2 points: honors `Retry-After` or jittered backoff for 429 and transient 5xx; does not retry 4xx unchanged.
- 2 points: downloads the actual asset, checks HTTP/content type, and does not treat URL as durable storage.
- 1 point: stores secret-free endpoint/model/payload/seed/job/result metadata or explicitly describes it.

**Critical failures:** hard-coded real-looking secret; v3 route with Image 5; `numVariations: 4`; no polling; writes the acceptance JSON as the image.

### A2. Build a mask-fill request and diagnosis — 12 points

**User request:** “Provide an executable cURL or Python workflow that uploads `source.png` and `mask.png`, replaces only the masked object with four seeded variants, and explain how to diagnose changes outside the mask.”

**Essential characteristics:** two binary uploads, extraction of IDs, v3 fill route, correct source/mask nesting, four unique seeds matching four variations, supported exact output size, quota-aware polling/retries, and isolation QA.

**Rubric:**

- 2 points: uploads both files to `/v2/storage/image` with correct auth and binary content type, then extracts `images[0].id`.
- 3 points: correct `/v3/images/fill-async` payload with separate image source and mask source.
- 2 points: `numVariations: 4` and exactly four unique seeds; valid prompt/negative prompt and size.
- 2 points: routes uploads/submission/polls through the default 4-RPM organization limiter, honors `Retry-After` for 429/transient errors, handles failed state, and saves/downloads all outputs.
- 2 points: compares unchanged regions against source, checks mask inversion/alignment/seams/halos at zoom, and rejects collateral edits.
- 1 point: preserves source/mask/output hashes and notes upload/output lifetime.

**Critical failures:** uploads a mask but never references it; seed count mismatch; retries a 422 unchanged; assumes white/black semantics without inspection.

### A3. Production rollout, governance, and QA plan — 15 points

**User request:** “Plan a 2,000-asset enterprise launch using Firefly generation, fill, and product composites. Include model migration, cost/capacity, safety, privacy, provenance, failure handling, and acceptance QA.”

**Expected approach:**

- Inventory each use case and select v4, v3 Fill, Generate Object Composite, Precise, or Adaptive by required preservation and background availability.
- Pin endpoint/model headers and schema validators. Explicitly identify the current Image 5 migration/upscale documentation conflicts and rely on operation reference/changelog plus contract tests.
- Create sample gates before batch: rights/consent, locale, prompt, mask/source, product fidelity, exact dimensions, and human approval.
- Queue every upload, submission, and poll under one organization limiter; at the default entitlement average at least 15 seconds across all workers, negotiate a rate increase where needed, price from the Operations rate card, and track actual consumption.
- Implement idempotency/reconciliation around timeouts, bounded retries for 429/5xx, token refresh for 401, no unchanged retry for validation/policy errors, cancellation, and dead-letter review.
- Minimize data, use short-lived URLs, download outputs promptly to governed storage, follow 90-day/24-hour documented defaults, and do not invent `storeInputs`.
- Preserve Content Credentials/originals and an audit ledger; verify Sales Order permission for external-facing Customer Software and avoid prohibited AI-system training/testing uses; explain indemnity's contract/feature/surface/export and modification/combination exclusions.
- Define measurable batch QA and rollback/stop thresholds.

**Rubric:**

- 3 points: operation/model routing and preservation rationale across all three classes.
- 2 points: schema pinning, migration contract tests, and documentation-conflict handling.
- 2 points: representative sample and rights/safety/human gates.
- 2 points: correct 4 RPM/9,000 RPD capacity plan and Operations-based cost governance.
- 2 points: robust asynchronous error, retry, reconciliation, cancellation, and dead-letter design.
- 2 points: accurate privacy/retention and durable-download plan.
- 1 point: Content Credentials/audit preservation and qualified indemnity statement.
- 1 point: measurable QA/stop criteria including product pixel fidelity, mask isolation, text, dimensions, provenance, and reject rate.

**Critical failures:** proceeds to 2,000 assets without a sample gate; prices from an invented public dollar rate; strips provenance by default; describes indemnity as automatic; stores output only at Adobe's temporary URL.

## Score interpretation

- **90–100:** production-ready; accurate version boundaries, executable integration, strong creative/technical QA, and careful legal/privacy/provenance reasoning.
- **75–89:** capable with limited omissions; safe for supervised implementation after targeted fixes.
- **60–74:** partial competence; significant schema, operations, or governance gaps require review.
- **40–59:** unreliable for production; likely to waste Operations or mishandle assets.
- **0–39:** unsafe or fundamentally incompatible with current Firefly image APIs.

Record the raw item total, any deductions, the applied cap, and the final score. Cite the exact response evidence for every critical failure.
