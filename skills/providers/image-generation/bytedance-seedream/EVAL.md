# Evaluation rubric: bytedance-seedream

Evaluate the answer or implementation without revealing this rubric to the task solver. Award only demonstrated behavior. When a criterion has multiple parts, award partial credit proportionally unless the criterion says all-or-nothing.

## Critical scoring caps

Apply the lowest applicable cap after calculating the raw score.

- **20-point cap:** exposes an API key; forwards Ark authorization to an artifact/reference host; accepts arbitrary API bases without a strict allowlist; buffers an untrusted artifact without a streaming byte cap; follows artifact redirects to unapproved/private-network destinations; allows an EU host/current-model pairing outside the live EU catalog; or provides runnable code that sends a paid call by default without explicit opt-in.
- **35-point cap:** uses a third-party gateway as the first-party production path; conflates Seedream image generation with Seedance video tasks; invents an async image job/poll/webhook/idempotency contract; or presents `seed`/`guidance_scale` as supported current-family controls.
- **50-point cap:** mixes China and global hosts/model namespaces; invents a global 5.0 Pro ID; sends grouped output, SSE, or web search to China 5.0 Pro; or otherwise relies on a materially false compatibility claim.
- **60-point cap:** has no meaningful safety, privacy, consent, or rights gate for user/reference images and generated outputs.
- **70-point cap:** can generate but has no durable artifact acquisition, partial-failure handling, provenance record, or pre-release QA plan.

## A. Interface and model correctness — 24 points

1. **Surface separation (6):** identifies the first-party China route and at least one first-party BytePlus route, uses `/api/v3/images/generations`, and keeps `doubao-...` IDs on China versus `seedream-...` IDs globally.
2. **Current model selection (5):** distinguishes China 5.0 Pro from 5.0 Lite/4.5/4.0 and does not invent global Pro; pins a dated ID or endpoint and includes lifecycle rechecking.
3. **Capability matrix (7):** correctly limits grouped output and SSE to 5.0 Lite/4.5/4.0, web search to 5.0 Lite, Pro references to 10, 5.0 Lite/4.5 references to 14, and format/resolution controls by model. For 4.0, accepts either the conservative model-card limit of 10 or 11–14 only with an explicit live-endpoint validation because the generic API and model card conflict.
4. **Region boundary (3):** notes EU availability restrictions and that BytePlus endpoint choice is not a guaranteed data-residency boundary.
5. **Scope discipline (3):** stays on Seedream first-party image generation/editing and clearly excludes Seedance/task APIs and undocumented features.

## B. Request, prompting, and output semantics — 20 points

6. **Request validation (5):** validates required model/prompt, input URL or lowercase data URL, documented image type/size/dimensions/aspect ratio, reference count, and model-specific size constraints.
7. **Current controls (4):** handles `size`, `response_format`, `output_format`, `watermark`, and prompt optimization accurately; does not carry legacy seed/guidance controls into current models.
8. **Editing/reference prompting (4):** assigns ordinal roles to references, names the edit operation and invariants, and explains annotation-based local control without inventing a mask endpoint.
9. **Grouped output (3):** uses `auto` plus `max_images` 1–15, respects the 15-image input-plus-output ceiling, requests an explicit set in the prompt, and validates actual count.
10. **Response semantics (4):** checks top-level and per-item errors, handles partial success, validates decoded bytes, and treats 24-hour URLs as ephemeral.

## C. Runnable integration and artifact security — 25 points

11. **Authentication and request example (5):** provides a complete runnable example using runtime secret injection, Bearer auth, JSON content type, a correct first-party host/model pair, timeouts, and non-secret error reporting.
12. **Base64 or URL handling (5):** strictly decodes base64 or safely streams URLs with a pre-buffer byte cap; checks content type and magic bytes and rejects malformed output.
13. **Credential isolation (4, all-or-nothing):** never forwards the Ark bearer token to returned artifact URLs or reference hosts and explicitly enforces or explains that boundary.
14. **Durability (4):** downloads before expiry, uses safe temporary/atomic persistence or equivalent, hashes artifacts, and writes a manifest/metadata record.
15. **Stream/group example (4):** shows a correct grouped or SSE request on a supporting model and explains final completion plus partial success/failure behavior.
16. **Code integrity (3):** examples are syntactically coherent, placeholders/environment variables are clear, request JSON matches prose, and the code would run after installing any explicitly named dependency and setting credentials/inputs.

## D. Production resilience and operations — 17 points

17. **Retry classification (5):** retries only network/transient 429/500 classes with capped exponential backoff, jitter, concurrency control, and `Retry-After`; avoids blind retries for auth, invalid input, moderation, or ambiguous duplicate-risk timeouts.
18. **Job ledger and idempotency honesty (3):** creates a client job/request hash/state record and explicitly says provider idempotency is undocumented, so timeout reconciliation is required.
19. **Quota and cost controls (4):** distinguishes documented global IPM from account/endpoint limits, bounds group/resolution cost before submission, counts successful outputs, and rechecks dated official pricing.
20. **Observability (2):** records model/region, latency, attempts/errors/throttles, successes/failures, bytes/resolution, usage/tool use, cost, and review outcome without secrets.
21. **Regression and migration (3):** maintains a golden suite covering generation, edits, multi-reference, typography, safety, grouped/partial failures, throttling, timeouts, and corrupt artifacts; compares model upgrades before switching.

## E. Privacy, safety, rights, and evidence quality — 14 points

22. **Data handling (4):** distinguishes 24-hour output URL retention from documented safety-filter retention, identifies processing/residency caveats, minimizes metadata/logging, and directs the implementer to the applicable DPA/contract.
23. **Rights and consent (4):** requires rights/consent for inputs, faces/likenesses, trademarks, and copyrighted/private material; notes output non-uniqueness, no provider non-infringement guarantee, and human review.
24. **Safety and disclosure (3):** blocks representative prohibited/deceptive/abusive uses, preserves required provenance/disclosures, and does not treat `watermark: false` as a legal waiver.
25. **Evidence hygiene (3):** separates documented facts, provider claims, operational recommendations, and unknowns; dates volatile facts and relies on first-party ByteDance/Volcengine/BytePlus sources.

## Point check

`24 + 20 + 25 + 17 + 14 = 100`

## Minimum evidence expected from a strong submission

- Exact deployment surface and model ID, with host/model namespace validation.
- A realistic request and response path, including item-level failures.
- Secure artifact acquisition with no credential leakage and a hard byte cap.
- A retry/timeout/quota/cost plan grounded in the documented contract.
- A durable manifest connecting sources, prompt/request hash, model, usage, artifact hash, and review state.
- A privacy/safety/rights review appropriate to the proposed inputs and release context.
