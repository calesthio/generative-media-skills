# Recraft image design evaluation

This file is the hidden answer key. Give the evaluated agent the user task and `SKILL.md`, never this file.

## Scoring

Score each item independently, then apply the global caps. Award partial credit only for correct, actionable content. Total before caps is exactly **100 points**:

- Knowledge: 30
- Code and API execution: 30
- Production decisions and outputs: 40

### Global caps

Apply the lowest applicable cap after adding item scores:

- **20-point cap:** exposes a real token, sends/recommends sending the Bearer token to a non-Recraft host or asset URL, or provides code that can write arbitrary server content without pre-buffer transport bounds plus scheme/type/signature/decoded-size validation in a security-sensitive task.
- **35-point cap:** invents and relies on an undocumented Recraft async/job/webhook/priority route, mockup API route, model ID, or localized-edit compatibility; or routes Recraft API calls through a non-official host without an explicit user-supplied gateway requirement.
- **50-point cap:** uses V4/V4.1-only generation while claiming V3-only style/text-layout/inpaint/outpaint/background controls are supported, or substitutes raster for a required editable SVG without disclosure.
- **60-point cap:** omits all privacy/retention/signed-URL handling and all rights/safety analysis from a production plan involving uploaded assets or people/brands.
- **70-point cap:** otherwise strong answer lacks durable asset download, request/model/seed provenance, or final-output QA.

Factual caution is not penalized when first-party public documentation is genuinely ambiguous and the answer identifies what must be verified.

## Knowledge — 30 points

### K1. Model family and lifecycle — 6 points

Question: As of 2026-07-09, choose among V4.1 expressive, V4.1 Utility, Pro, vector, V3, and V2 for concept art, predictable product imagery, print, native SVG, controlled edits, and legacy styles. State the lifecycle uncertainty.

Expected answer:

- V4.1 expressive is the current default/general design and exploration family (1).
- Utility favors simple, flat-lit, front-facing, predictable results such as product shots/mockup source imagery (1).
- Pro variants supply the higher roughly 4 MP size; standard is for iteration (1).
- `_vector` is required for native SVG (1).
- V3 remains for curated/custom styles, negative prompts, V3 text layout/artistic level, and localized edit routes; V2 for legacy-only styles/effects (1).
- All 16 public proprietary IDs remain listed, but no public deprecation dates/support windows exist (1).

Disqualifying claim for this item: V4.1 style IDs or V4.1 inpaint/outpaint are documented as generally supported.

### K2. Operations and boundaries — 6 points

Question: Distinguish image-to-image, inpaint, outpaint, replace/generate background, remix, vectorize, remove background, Explore, and mockups.

Expected answer:

- Correctly differentiates prompt-guided whole-image transform, masked edit, canvas extension, and background operations (2).
- Notes localized edit/background routes are documented for V3/V3 Vector; identifies the current image-to-image conflict (prose V3/V4 versus parameter list including V4.1) and requires account/contract validation before relying on V4.1 (1).
- Remix/`variateImage` is promptless and requires target size; Explore Similar requires an Explore image ID and similarity 1..5 (1).
- Vectorize is raster-to-SVG; remove-background preserves raster/vector class based on input (1).
- Mockup composition/warping is documented in Studio, not as a public API route (1).

### K3. Exact generation schema — 6 points

Question: Describe a valid `/v1/images/generations` request and response.

Expected answer:

- Official host, Bearer auth, required `prompt`, valid public `model`, `n` 1..6 (2).
- `size`, `random_seed`, `response_format` `url|b64_json`, and model-compatible controls (1).
- V4/V4.1 max prompt 10,000 versus V2/V3 1,000; only listed sizes/aspects (1).
- Response has `created`, `credits`, `data[]`; each image can expose `image_id` and `url` or `b64_json` (1).
- Correctly limits API raster `image_format` to Swagger-documented PNG/WEBP and vector output to SVG, without importing Studio export formats (1).

### K4. Brand, style, text, and mask controls — 6 points

Question: Explain exact palette, style, text-layout, and mask semantics.

Expected answer:

- `controls.colors` uses RGB triples and optional weights in 0..1 with sum no more than 1; `background_color` uses a color object (1.5).
- Colors are preferences, not exact guarantees; deterministic postproduction for exact brand marks/colors (1).
- `style` and `style_id` are mutually exclusive and V2/V3-compatible; API custom styles are V3-bound (1).
- V3 `text_layout` uses one supported-character word and exactly four relative-coordinate points per bbox (1.5).
- White 255 changes/fills/erases, black 0 protects; mask matches source dimensions and is binary (1).

### K5. Rates, pricing, privacy, and rights — 6 points

Question: Summarize the production risk envelope.

Expected answer:

- 100 images/minute and 5 requests/second from Appendix, with API terms also stating 100 requests/minute; enforce conservatively (1).
- Correctly distinguishes current standard/Pro raster and vector pricing or says to recheck the dated API pricing page (1).
- URLs are signed but publicly accessible to anyone with the link and should be downloaded promptly (1).
- Identifies the retention conflict: beyond-delivery default in terms versus approximately 24-hour deletion/storage in Appendix/trust pages; uses conservative handling (1).
- API assets are customer-owned/commercial subject to terms and cannot be used to train AI; API inputs/outputs are not used for training per API terms/trust docs (1).
- User remains responsible for input/output clearance, consent, disclosure, and Recraft policy compliance (1).

## Code and API execution — 30 points

### C1. Executable generation and durable download — 12 points

Task: Write an executable example that generates one V4.1 raster or vector asset and stores it durably.

Rubric:

- Uses `https://external.api.recraft.ai/v1/images/generations`, `/raster`, or `/vector`, Bearer token from environment, and valid JSON fields (3).
- Chooses a correct model/output pair and valid `n`/size/seed/response format (2).
- Fails on non-2xx and uses finite connect/read timeouts (1).
- Parses expected response shape and checks field existence (1).
- For URL: requires HTTPS, does not forward auth, enforces a streaming/transport bound before buffering, checks content type plus magic/signature and decoded size; for base64: bounds the HTTP/JSON response before parsing, strict-decodes, bounds decoded bytes, and checks expected signature/XML (3).
- Saves the exact submitted request/prompt, response body and headers/`X-Recraft-Requestid`, UTC timestamp, IDs, credits, final output hash, and output (1).
- Does not log the token or use an untrusted API host (1).

Critical failures: guessed route/model; downloading URL with Authorization header; trusting extension alone; raster model for a task explicitly requiring editable SVG.

### C2. Executable masked edit or outpaint — 10 points

Task: Produce a valid V3 inpaint or outpaint request with input validation.

Rubric:

- Uses correct route, `recraftv3` or `recraftv3_vector`, and multipart fields or JSON URL counterparts (2).
- Inpaint: validates each input at 256 px minimum, 4096 px maximum edge, no more than 16 MP/10 MB, equal dimensions, actual file type, and a binary mask with correct white/black semantics; outpaint: uses valid `size` versus `expand_*` exclusivity and valid zoom range (3).
- Includes prompt, valid response handling, timeouts, and non-2xx behavior (2).
- Preserves immutable-region intent and includes seam/lighting QA (1).
- Uses a pre-buffer transport bound plus durable validated download/base64 decode and decoded-size/signature checks (1).
- Records seed/model/request IDs where available (1).

### C3. Retry, budget, and ambiguous outcomes — 8 points

Task: Describe or implement a safe request wrapper for batch production.

Rubric:

- Enforces image/minute, request/minute, and requests/second budgets and multiplies per-image cost by `n` (2).
- Retries 429 and only connect failures proven pre-send with bounded exponential backoff, jitter, and `Retry-After`; treats read/post-submit timeouts, connection loss after transmission, and 5xx as potentially billable/ambiguous and reconciles before resubmission (2).
- Does not blindly retry auth, validation, safety, or insufficient-unit failures (1).
- Captures status/body/headers and `X-Recraft-Requestid` without assuming a stable error JSON schema (1).
- Uses a local job ledger and flags post-submit timeout as potentially billable because idempotency is undocumented (1).
- Refuses to invent async/webhook/priority behavior from marketing copy (1).

## Production decisions and outputs — 40 points

### P1. Brand vector system — 15 points

Scenario: Create a scalable two-color icon family for a fintech product. It must remain legible at 20 px, use approved colors, contain no raster, and avoid close imitation of a competitor.

Expected approach and rubric:

- Selects V4.1 Vector standard for probes and Pro Vector only if justified by final complexity/size (2).
- Writes a complete prompt specifying icon subject, shared geometry language, flat fills, silhouette, palette, no text/gradient/shadow/mockup, and small-size intent (3).
- Uses palette controls correctly while stating exact color enforcement requires postproduction/validation (2).
- Generates one or a small controlled set with recorded seeds before scaling the family (1).
- Treats SVG as untrusted: uses a maintained sanitizer or strict passive element/attribute allowlist; rejects event handlers, style/style blocks, animation, processing instructions, embedded raster/foreign content, and non-fragment external/data/URL references; then checks viewBox, paths, path count, fills, clipping, and 20 px legibility (3).
- Includes similarity/trademark review and rights provenance for references (2).
- Saves bytes plus prompt/model/seed/image/request IDs/hash and cost (1).
- Provides a meaningful failure/repair loop rather than only regenerating blindly (1).

### P2. Predictable product campaign raster — 13 points

Scenario: Produce a print-oriented product hero with quiet front-facing lighting, strict copy space, a real trademarked package supplied by the client, and no generated package text.

Expected approach and rubric:

- Chooses V4.1 Utility standard for direction, then Utility Pro after approval; explains why expressive is less predictable (2).
- Uses client-cleared package reference appropriately; does not assume generation grants trademark clearance (2).
- Specifies camera, product count, lighting, material, background, copy-safe geometry, palette, and “no generated words/logos” (2).
- Keeps official package artwork deterministic via compositing/masking rather than trusting generated text (2).
- Budgets probe/promotion and records the model transition (1).
- Reviews dimensions, crop, material/reflections, package integrity, palette, defects, and print suitability (2).
- Handles signed URL privacy/retention and provenance/disclosure (2).

### P3. V3-to-V4.1 migration and incident response — 12 points

Scenario: A pipeline uses V3 custom style, text-layout boxes, inpaint, seeds, and background replacement. Leadership asks to “upgrade everything to V4.1” and the first timed request returns an unknown non-2xx body.

Expected approach and rubric:

- Inventories dependencies and refuses a blanket model-string replacement (2).
- Moves compatible plain generation to V4.1/Utility but retains V3 for custom style, text layout, inpaint, and documented background routes (3).
- Re-expresses only appropriate style intent in prompt/palette and flags losses for approval (1).
- Builds fixed regression briefs and compares copy, layout, palette, edit preservation, quality, cost, and seeds (2).
- Captures status/body/headers/request ID; classifies retryability without assuming an error schema (1).
- Uses bounded retry only if transient and treats timeout after submit as ambiguous/billable (1).
- Notes marketing async claims lack a public implementation contract and does not fabricate one (1).
- Includes rollback/versioned manifests and re-verification of current docs/pricing/terms (1).

## Evaluator notes

- Treat prompts, curl bodies, snippets, and plans shown in answers as **examples**, not mandatory formulas.
- Do not penalize an agent for omitting Swagger-only fields that are not needed for the task.
- Penalize confidently claiming undocumented behavior more than explicitly identifying an ambiguity.
- Accept equivalent secure download implementations and equivalent model-appropriate creative choices when the required constraints and tradeoffs are preserved.
