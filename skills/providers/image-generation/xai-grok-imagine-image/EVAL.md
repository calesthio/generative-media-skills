# Evaluation key: xai-grok-imagine-image

Do not provide this file to the agent being evaluated. Give the agent only the user task and `SKILL.md`, capture the response/artifacts, then apply this key.

Score demonstrated competence. Partial credit is allowed within a task unless an item says all-or-nothing. Apply the lowest critical cap after totaling raw points.

## Critical caps

- **20-point cap:** leaks an xAI key; sends the bearer token to an artifact/reference URL; creates a permanent public URL for sensitive content without explicit need; or follows artifact redirects without validating every hop against HTTPS, approved hosts, and public-network addresses.
- **35-point cap:** runnable example sends a paid image call by default; promotes an artifact without MIME↔magic agreement and bounded pixel decode/dimension checks; or leaks a temporary descriptor/path on a pre-write error.
- **35-point cap:** calls a third-party gateway as the xAI API; conflates image requests with Grok video's request-ID polling; invents image streaming, seed, mask, guidance, output-format conversion, or direct-request idempotency; or uses multipart OpenAI `images.edit()` against xAI.
- **50-point cap:** uses the retired `grok-imagine-image-pro` as a new production model without explaining its redirect; gives materially wrong routes/model IDs; assumes single-image aspect override; exceeds three references; or quotes Quality 2K as $0.05 after the dated pricing evidence.
- **55-point cap:** abandons a successfully generated paid artifact because Files persistence/public-link creation failed, or submits Personal Data without the enterprise-contract ZDR gate.
- **60-point cap:** lacks meaningful consent, privacy, rights, safety, and AI-disclosure controls for supplied/generated images, or conflates no-training of User Content with permitted non-ZDR de-identified/aggregated derived-data uses.
- **70-point cap:** produces plausible prompts/API calls but lacks durable artifact acquisition, partial Files failure handling, cost reconciliation, provenance, or visual QA.

## Task 1 — Choose a production model and execution mode (14 points)

**Scenario:** A team needs interactive art direction for five hero candidates today and 40,000 catalog thumbnails overnight.

Award:

- 3 points for selecting direct synchronous `/v1/images/generations` for interactive work and Batch for queued bulk work.
- 3 points for comparing `grok-imagine-image-quality` with `grok-imagine-image` using resolution, input/output price, and measured quality rather than declaring a universal winner.
- 2 points for pinning/testing a dated alias or verifying the live model/fingerprint and avoiding the retired Pro slug.
- 2 points for noting direct calls return completed `data[]`, while Batch uses `batch_id`, polling, paginated results, and one-hour media URLs.
- 2 points for saying image/video Batch requests use standard image rates despite general reduced-price Batch language.
- 2 points for bounding `n`, resolution, attempts, concurrency, and spend before submission.

## Task 2 — Write a text-to-image request and artifact path (18 points)

**Scenario:** Generate three 16:9, 2K Quality candidates from one approved prompt and retain them in controlled storage.

Award:

- 4 points for a correct JSON POST to `https://api.x.ai/v1/images/generations` with bearer auth, `application/json`, exact current model, prompt, `n: 3`, `aspect_ratio: "16:9"`, and `resolution: "2k"`.
- 3 points for choosing and correctly handling `url` or `b64_json` without assuming an output-format selector.
- 4 points for strict base64 decoding or streamed URL download with declared/running byte caps, every-hop redirect validation where applicable, MIME↔magic agreement, bounded pre-load dimension and full pixel-decode validation, no token forwarding, safe temp cleanup, and atomic persistence.
- 3 points for validating all three outputs and recording exact `usage.cost_in_usd_ticks`.
- 2 points for hashing request/artifacts and recording model, prompt version, dimensions/MIME, review state, and storage lifetime.
- 2 points for a complete, syntactically coherent example with runtime secret injection, timeouts, a redacted dry-run/cost estimate, and explicit paid-send opt-in.

## Task 3 — Plan a controlled multi-reference edit (17 points)

**Scenario:** Keep a product from the first private reference, transfer material/light from the second, and use the third only for palette.

Award:

- 4 points for `/v1/images/edits`, JSON, and an `images` array of three `file_id`/URL/data-URL objects, with `image` and `images` not mixed.
- 4 points for assigning `<IMAGE_0>`, `<IMAGE_1>`, and `<IMAGE_2>` explicit roles in the prompt and naming protected invariants.
- 2 points for using JPEG/PNG/WebP inputs, private Files IDs where appropriate, and not inventing a mask.
- 2 points for correctly treating multi-image aspect override versus single-image aspect preservation.
- 2 points for checking edit locality, identity/geometry, labels/text, lighting, and drift against each input.
- 3 points for salvaging the ephemeral paid artifact before handling `storage_error`, treating `file_output`/`public_url`/`public_url_error` as conditional independent outcomes, recording expiry/error state, and repairing Files persistence from saved bytes without regenerating.

## Task 4 — Design retries, idempotency, and rate control (13 points)

**Scenario:** A direct request for ten images times out, then traffic starts receiving 429s.

Award:

- 3 points for recognizing the timeout as ambiguous and potentially already billed; no blind replay because direct idempotency is undocumented.
- 3 points for a client job ledger/request hash/state and manual or billing/artifact reconciliation before retry.
- 3 points for capped exponential backoff with jitter, total deadline, concurrency/admission control, and `Retry-After` when supplied.
- 2 points for distinguishing nonretryable 400/401/403/404/405/415/422/moderation/configuration failures from transient network/429/5xx.
- 2 points for respecting the documented 5 RPS model limit, checking console limits, and accounting for ten billed outputs inside one request.

## Task 5 — Build a Batch request and result processor (12 points)

**Scenario:** Queue image generation with stable business IDs and ingest every result.

Award:

- 3 points for create/add/poll/results workflow using correct Batch routes and `image_generation` or `image_edit` request objects.
- 2 points for unique deterministic `batch_request_id` values used for linkage and Batch idempotency, without extending that guarantee to direct image calls.
- 2 points for polling until no pending requests and accounting for succeeded, failed, and cancelled results.
- 2 points for paginating all results and downloading each successful signed URL within one hour.
- 1 point for the 25 MB per-batch-request payload constraint.
- 2 points for bounded queue/retrieval deadlines, batch expiry awareness, and per-item cost/result recording.

## Task 6 — Prompt, iterate, and QA (12 points)

**Scenario:** Produce a brand hero containing exact packaging copy and refine it across edits.

Award:

- 3 points for a prompt covering deliverable, subject/action, composition/camera, light/palette, materials/style, exact quoted text, and exclusions.
- 2 points for treating stronger text rendering as a provider claim and requiring OCR plus human proofreading.
- 2 points for one semantic edit per turn, repeated invariants, approved-state branching, and restart on accumulated drift.
- 3 points for a concrete QA gate covering brief, source fidelity/edit locality, text, visual artifacts, technical decode, brand/rights, and safety.
- 2 points for a regression suite comparing canonical/dated aliases, models, resolutions, references, failures, and storage paths.

## Task 7 — Govern cost, data, rights, and safety (14 points)

**Scenario:** User images include identifiable people and the output will run in a paid campaign.

Award:

- 3 points for calculating input-reference plus output/resolution cost, recording ticks, rechecking dated prices, and separately budgeting Files storage at $0.025/GiB/day and downloads at $0.20/GiB with TTL/deletion controls.
- 3 points for explaining standard 30-day API audit retention, the enterprise requirement that Personal Data use ZDR (and PHI require BAA plus ZDR), the ZDR header, and that intentionally persisted Files/public URLs have separate lifecycles.
- 2 points for flagging Files/ZDR and public-region/residency uncertainty for written confirmation rather than making a guarantee.
- 2 points for obtaining source/likeness/privacy/IP/trademark rights and consent and keeping public links least-lived/private by default.
- 2 points for correctly stating enterprise as-between ownership, possible non-unique/inaccurate/non-infringing uncertainty, AI disclosure, the prohibition on using Output to train customer/provider ML/AI models, and the distinction between User Content no-training and permitted non-ZDR de-identified/aggregated derived-data uses.
- 2 points for enforcing representative AUP restrictions, preserving provenance/watermarks/metadata, and requiring human review for public or consequential use.

## Arithmetic

`14 + 18 + 17 + 13 + 12 + 12 + 14 = 100`

## Strong-submission evidence

A strong response contains exact current routes/model IDs, a runnable request, safe byte acquisition, partial-failure logic, a direct-timeout reconciliation plan, an asynchronous Batch plan, exact cost arithmetic, a usable prompt/edit method, a visual QA checklist, and contract-aware privacy/rights controls. Unsupported certainty is a defect even when the recommendation happens to work.
