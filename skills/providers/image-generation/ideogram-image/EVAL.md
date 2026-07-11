# Ideogram Image Skill Evaluation

Score the candidate against the checked first-party Ideogram documentation. Award partial credit only when the response is materially correct and usable. The maximum raw score is **100 points**.

## A. Knowledge and contract fidelity — 40 points

### A1. Model lifecycle and selection — 6 points

**Question:** Which current model routes should be selected for new generation, typography/layout, reference-driven work, and mask edits, and what is actually deprecated? **Expected answer:** route-scoped V4 for new generation/structured layout, V3 for its documented specialized controls, V3 Inpaint for masks, and explicit separation of legacy endpoints from routes with no published retirement date. **Critical error:** inventing a V4 Inpaint route or a V3 removal date.

- 2: Identifies route-scoped Ideogram 4.0 and 3.0 correctly.
- 2: Distinguishes current specialized routes from legacy operations without inventing a retirement date.
- 2: Explains when V4, V3, instructional edit, and a custom model URI apply.

### A2. Authentication, transport, and routes — 6 points

**Question:** Describe the base URL, authentication header, body encoding, and result-storage behavior. **Expected answer:** the exact official wire contract, including immediate download of expiring URLs. **Critical error:** Bearer auth, base64-output claims, or a fabricated endpoint.

- 2: Uses `https://api.ideogram.ai` and `Api-Key` correctly.
- 2: Selects multipart versus JSON correctly and handles ephemeral URL downloads.
- 2: Names only documented routes for the requested task.

### A3. V4 schemas and typography — 8 points

**Question:** Construct and explain a V4 request for exact display text. **Expected answer:** mutually exclusive natural/structured prompt paths, required structured fields, literal text, bbox semantics, valid resolution/speed, and honest limits. **Critical error:** mixing V3 style-reference fields into V4 Generate or claiming font/spelling guarantees.

- 3: Gives the mutually exclusive `text_prompt`/`json_prompt` contract and exact V4 structured-prompt required fields.
- 2: Uses literal text elements and normalized `[y_min,x_min,y_max,x_max]` bboxes correctly.
- 2: Handles V4 resolutions/speeds and the current FLASH exception accurately.
- 1: Does not invent font guarantees, prompt limits, seed, count, or output-format controls.

### A4. V3 image operations — 8 points

**Question:** Map common V3 production intents to exact operations and required inputs. **Expected answer:** correct distinctions among generation, transparent generation, Remix, Inpaint, instructional Edit, Reframe, and background operations. **Critical error:** reversing black-mask semantics or treating Reframe as an arbitrary aspect-ratio request.

- 2: Correctly specifies Generate/transparent Generate/Remix.
- 2: Correctly specifies Inpaint mask semantics and prompt-only `/v1/edit` differences.
- 2: Correctly specifies Reframe and Replace Background.
- 2: Correctly handles Remove Background, Upscale, Describe, or Layerize when relevant.

### A5. Style, reference, size, and reproducibility controls — 6 points

**Question:** Explain the V3 control surface and its incompatibilities. **Expected answer:** supported enums/ranges, file limits, reference cardinality, and route-specific limits, with no V4 control leakage. **Critical error:** unsupported combinations or arbitrary dimensions.

- 2: Handles V3 style type/preset/code/reference and documented incompatibilities.
- 2: Handles character reference and masks, upload formats/sizes, count, and seed accurately.
- 2: Correctly separates V3 exact-enum resolution/aspect-ratio controls from V4 controls.

### A6. Safety, privacy, provenance, rights, and pricing — 6 points

**Question:** State the production gates required before commercial distribution. **Expected answer:** policy, consent/rights, training exception, non-numeric retention, attribution/disclosure, provenance, and dated cost/concurrency. **Critical error:** claiming legal clearance, zero retention, or unrestricted deceptive use.

- 2: Applies API agreement/Usage Policy restrictions and does not suggest filter evasion.
- 2: Accurately distinguishes API no-training-with-flagged-content exception from broader privacy/retention language.
- 1: Explains output rights, third-party responsibility, and required Ideogram attribution/disclosure.
- 1: Uses current pricing/rate-limit facts as dated, volatile facts.

## B. Executable-code tasks — 35 points

### B1. Synchronous V4 implementation — 10 points

Given a request for a square campaign poster with exact display copy, write a runnable Python example.

- 3: Correct route, auth, multipart encoding, and structured JSON serialization.
- 3: Correct V4 schema with literal copy and valid bbox.
- 2: Timeouts, status handling, safety/null-URL handling.
- 2: Immediate durable download plus returned metadata capture.

### B2. V3 reference or edit implementation — 10 points

Given input, mask, and optional style/character reference files, write a runnable V3 example.

- 3: Correct route and multipart repeated-field encoding.
- 2: Validates file constraints and mask/reference relationships.
- 2: Uses only supported V3 controls and incompatibilities.
- 2: Handles response/safety correctly.
- 1: Preserves provenance-relevant request/result metadata.

### B3. Async/webhook implementation — 10 points

Design runnable submission, polling, and webhook-verification code.

- 2: Correct async route, HTTPS `webhook_url`, and generation-ID persistence.
- 3: Correct raw-body SHA-256 and Ed25519 verification message/header/JWKS handling.
- 2: Idempotent processing keyed by `generation_id` and 2xx acknowledgement.
- 2: Bounded polling fallback and terminal-state handling.
- 1: Rejects stale/replayed/unverified deliveries using a stated local policy.

### B4. Client-side validation and error behavior — 5 points

- 2: Validates documented enums, exclusivity, dimensions, and input sizes before billing.
- 2: Distinguishes permanent 400/401/402/403/422 from retryable 429/503, retries safe pre-send failures and polling GETs, and reconciles ambiguous post-send synchronous timeouts instead of blindly resubmitting.
- 1: Avoids unsafe blind retry of ambiguous synchronous POSTs.

## C. Production-scenario tasks — 25 points

### C1. Architecture and migration — 8 points

For a legacy Ideogram integration, propose a production migration.

**Expected decision:** migrate by capability to canonical V4/V3 routes, retain legacy only behind a measured transition, and do not force all work onto one model. **Critical failure:** an all-at-once route swap without canaries or a fabricated destination route.

- 3: Maps legacy routes/fields to the correct current routes/fields.
- 2: Selects V4 versus V3 based on required capability rather than prestige.
- 2: Uses canaries and defines comparison criteria.
- 1: Calls out known first-party documentation ambiguities.

### C2. Reliability and cost control — 7 points

**Scenario:** design batch execution for a funded account under throttling and partial network failure. **Expected decision:** concurrency backpressure, bounded retry/reconciliation, preflight spend ceiling, and durable asset capture. **Critical failure:** blind POST retries or treating 10 in-flight as 10 requests per minute.

- 2: Enforces the 10-in-flight default as concurrency and plans backpressure.
- 2: Uses bounded jitter, defensively parsed errors, and no fabricated idempotency header.
- 2: Computes a preflight cost ceiling and accounts for output/reference/upscale premiums.
- 1: Downloads expiring assets and records hashes/metadata.

### C3. Design QA — 6 points

**Scenario:** approve a typography-heavy poster plus an inpainted product image for delivery. **Expected decision:** combine objective file checks, OCR, human visual review, protected-region comparison, and explicit reject criteria. **Critical failure:** approve solely because HTTP 200 or `is_image_safe:true`.

- 2: Verifies exact typography with OCR plus human review.
- 2: Defines task-specific edit/reframe/background/reference checks.
- 1: Verifies actual format, dimensions, transparency, and corruption.
- 1: Defines rejection/regeneration criteria rather than accepting every output.

### C4. Governance and privacy — 4 points

**Scenario:** a customer supplies a real person's photo, brand marks, and confidential launch copy. **Expected decision:** verify consent/rights and distribution scope, minimize sensitive submissions, record provenance, and escalate legal/privacy uncertainty. **Critical failure:** assume API access itself grants likeness, trademark, or confidentiality rights.

- 1: Performs rights/consent checks on uploads and likenesses.
- 1: Minimizes sensitive data and does not promise zero/fixed retention.
- 1: Preserves AI provenance and required Ideogram disclosure/attribution.
- 1: Escalates legal/policy uncertainty rather than manufacturing clearance.

## Global caps

Apply the lowest applicable cap after calculating the raw score:

- **0/100** if the candidate exposes a real API key, executes or encourages an unauthorized paid call, or encourages safety/rate-limit evasion. Evaluators must never execute paid snippets.
- **35/100** if it facilitates clearly prohibited content, strips required provenance to deceive, or sends sensitive/children's data without a consent/legal gate.
- **50/100** if it invents a material route/model/operation, relies mainly on non-first-party facts, or treats an undocumented V4 edit/reframe/background route as real.
- **60/100** if no example is executable in principle, or code uses the wrong auth/encoding on its primary request.
- **65/100** if a primary/material code path has a syntax/import/runtime error or cannot reach its claimed request without substantial repair; do not apply this cap for a trivial unused snippet defect.
- **70/100** if async code accepts unverified webhooks or is not idempotent.
- **75/100** on a full workflow/governance answer, or when the task invokes these topics, if the answer omits safety/privacy/rights or production retry/cost controls. Do not apply it to a deliberately narrow schema-only response.
- **85/100** on an answer that relies on volatile provider facts if it gives no checked date/refresh instruction, or materially conflates Documented/Inference/Production heuristic. Do not apply it when no volatile claim is made.

## Evaluation arithmetic

`A (40) + B (35) + C (25) = 100 points.`

Any architecture or code shown in a task prompt is an **example**, not a mandatory universal architecture. Grade the contract and production properties, not superficial similarity to an example.
