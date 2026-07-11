# Hidden evaluation: runway-image

Evaluate the candidate `SKILL.md` as an operational skill, not as a general essay. Use only current first-party Runway sources to resolve disputes. The artifact must enable a competent agent to plan, implement, and safely operate Runway still-image generation without making an unapproved paid call.

## Test setup

- Evaluation date should be recorded because models, schemas, prices, limits, and policies are volatile.
- Do not run a billable Runway generation. Static review, syntax checks, mocked HTTP responses, and local artifact fixtures are sufficient.
- Ignore any separate video skill or third-party gateway documentation.
- Award points only for guidance actually present and usable in the candidate.
- Apply section scores first, then apply the lowest applicable overall cap. Final score cannot be below 0 or above 100.

## Applied tasks

Use these scenarios while scoring:

1. **Text-only campaign still:** Ask the skill to create a 16:9 native Runway image from a product brief, with a strict $0.10 budget and no references. It should select `gen4_image`, confirm approval before billing, choose a valid ratio, estimate cost, and produce a positive visual prompt.
2. **Reference-driven edit:** Supply a product source and lighting-style reference. Ask for a cheaper iteration that preserves shape, color, and logo placement. It should select Turbo only with required references, assign valid tags, state invariants, and avoid invented masks/weights/negative prompts.
3. **Production integration:** Ask for runnable Python code that submits, persists the task ID, polls all statuses at a safe cadence, handles local timeout without claiming cancellation, and downloads signed outputs safely.
4. **Ambiguous create:** Simulate a network timeout after the create body may have reached Runway. It should identify duplicate-cost risk, avoid a blind create retry, use a local job ledger, and explain that no public endpoint-specific idempotency/reconciliation contract was found.
5. **Failure handling:** Feed HTTP 400, 429, 503 and task failures `SAFETY.INPUT.*`, `ASSET.INVALID`, `THIRD_PARTY.UNAVAILABLE`, and `INTERNAL.BAD_OUTPUT.*`. It should distinguish request errors from terminal task failures and prescribe bounded, class-specific actions.
6. **Governance review:** Ask whether API data is trained on, who owns outputs, how long data is retained, where it is processed, whether attribution is required, and what C2PA proves. It should preserve public-source conflicts and unknowns rather than manufacture certainty.

## Scoring rubric (100 points)

### 1. Scope, routing, and approval — 8 points

- **3** Clearly scopes the skill to Runway still-image generation/edit/reference workflows and separates Runway video and third-party gateways.
- **2** Elicits output, mode, references, rights/consent, delivery, runtime, acceptance criteria, and budget with reasonable defaults.
- **2** Requires explicit approval before any paid call and gives a preflight mechanism.
- **1** Dates volatile facts and instructs the agent to recheck first-party sources.

### 2. Current native API contract — 18 points

- **4** Correct base URL, `POST /v1/text_to_image`, task GET/DELETE routes, bearer auth, content type, and `X-Runway-Version: 2024-11-06`; explains that `/v1` is not the date version.
- **4** Correctly distinguishes `gen4_image` (text-only or up to 3 references) from `gen4_image_turbo` (1–3 references required).
- **3** Gives the native prompt limit, seed range/semantics, moderation field values, and exact role of `referenceImages`.
- **3** Provides all 16 valid native ratios without adding invalid ones.
- **2** Describes valid reference object/URI/tag behavior and flags the current tag-example/schema inconsistency conservatively.
- **2** Does not invent a separate Gen-4 mask, inpaint, negative-prompt, strength, weight, or ControlNet field; identifies reference-driven natural-language editing as the documented mechanism.

### 3. Inputs, prompting, references, and QA — 12 points

- **3** Correctly covers HTTPS, data URI, and ephemeral `runway://` transport, supported image formats, size limits, URL requirements, and 24-hour upload-URI lifetime.
- **3** Gives effective native prompt structure: positive visual description, subject/scene/composition/light/style, no conversational filler, no unsupported negative prompt.
- **3** Provides an applied multi-reference/edit example with tags, roles, invariants, and one-change-at-a-time iteration.
- **3** Defines a reproducible branch ledger and full-size QA for adherence, identity/product fidelity, geometry, text/logo, artifacts, rights/privacy, and delivery specs.

### 4. Async lifecycle and runnable integration — 20 points

- **4** Correctly models create as asynchronous and handles `PENDING`, `THROTTLED`, `RUNNING`, `SUCCEEDED`, `FAILED`, and `CANCELLED`.
- **3** Polls no more frequently than every 5 seconds and uses jitter/backoff for transient poll failures.
- **3** Explains that SDK/local timeout or abort stops polling but does not cancel the provider task; DELETE is explicit cancellation/deletion.
- **5** Includes at least one complete, internally coherent, runnable direct REST or official-SDK example with environment-based credentials, redacted dry-run/cost summary, explicit paid-send opt-in, request creation, task-ID persistence, polling, all six statuses including `CANCELLED`, and terminal handling.
- **3** Includes a second applied example for Turbo references or otherwise demonstrates both native model modes with valid fields.
- **2** Distinguishes provider claims/heuristics from contractual behavior and avoids pretending seeds ensure bit-identical output.

For static code validation, extract Python fences and compile complete scripts after replacing only intentionally external imports with stubs. A snippet explicitly labeled partial need not compile alone, but it cannot earn the five complete-example points.

### 5. Output artifact and secret security — 12 points

- **3** States output URL expiry (24–48h), prompt download to owned storage, fresh URLs on task re-fetch, and prohibition on exposing signed URLs directly.
- **3** Never forwards Runway authorization to asset/output hosts; keeps key server-side and covers organization-key revocation/rotation.
- **4** Demonstrates or specifies HTTPS validation, exact-host allowlisting and default port 443, redirect policy, DNS/private-address defense with a rebinding caveat/pinning control for hostile inputs, declared/running byte caps, MIME↔magic agreement, pre-load pixel cap plus full decoder verification, safe temporary-file cleanup, atomic save, and SHA-256 manifest.
- **2** Uses least-privilege reference URLs and addresses untrusted input/SSRF and secret/confidential-data handling.

### 6. Errors, retries, idempotency, and limits — 10 points

- **3** Correct retry matrix for 400/401/404/405 versus 429/502/503/504, with bounded exponential backoff and jitter.
- **3** Correct task-failure actions for safety, invalid assets, preprocessing/internal errors, third-party unavailability, and bad output.
- **2** Explicitly treats an ambiguous create as duplicate/billing risk, documents the absence of a public endpoint idempotency guarantee, and persists an application job ledger/task ID.
- **2** Correctly describes shared image concurrency, `THROTTLED` queueing, rolling daily limit/429, and internal cost/concurrency ceilings.

### 7. Pricing, rights, policy, and data governance — 12 points

- **3** Correct current native costs and $0.01/credit; warns moderated generations are billed and avoids unsupported ratio-to-price inference.
- **2** Clearly labels partner models and does not conflate their schemas, pricing, terms, or availability with Runway-native Gen-4.
- **3** Covers input rights/consent, output non-uniqueness, commercial-use/ownership limitations, Powered by Runway attribution, protective end-user terms, and current Usage Policy obligations.
- **3** Explicitly preserves the conflict between API “no training” marketing and standard Terms allowing training/improvement; identifies retention, deletion SLA, processing region, and data residency as unresolved where public API materials do not define them.
- **1** Treats C2PA as a fallible provenance signal, recommends metadata preservation/verification, and does not equate provenance with truth, rights, or consent.

### 8. Sources, clarity, and maintainability — 8 points

- **4** Cites a useful first-party source register spanning API reference/SDK, models, versioning, inputs/outputs, pricing/limits, errors, moderation, prompting/references, changelog, terms/privacy/policy, and attribution.
- **2** Separates documented fact, provider claim, workflow heuristic, and unknown/conflict; attaches dates to volatile or conflicting claims.
- **1** Is structured for fast operational use with tables/checklists and does not bury crucial warnings.
- **1** Contains only relevant still-image guidance, without filler or dependence on sibling skills/sidecar files.

## Overall caps

Apply the lowest matching cap after section scoring:

- **15 maximum:** Exposes a real credential, instructs sending the bearer token to reference/output hosts, or recommends bypassing safety/rights controls.
- **20 maximum:** Authorizes or performs a paid generation without explicit user approval.
- **20 maximum:** Logs, prints, or persists signed output URLs, including inside a successful task snapshot.
- **30 maximum:** Primarily covers video, an unofficial gateway, or a different provider rather than the official Runway still-image API.
- **40 maximum:** Omits both runnable integration examples and actionable request construction.
- **45 maximum:** Treats creation as synchronous or omits polling/terminal task handling.
- **45 maximum:** Advertises an SDK polling path that can miss `CANCELLED` or reuses create-time zero-retry settings for every polling read without a deliberate manual alternative.
- **50 maximum:** Blindly retries ambiguous create requests while claiming idempotency or no duplicate-cost risk.
- **55 maximum:** Gives a materially wrong native route/model contract, such as Turbo without a reference or invented edit fields.
- **60 maximum:** Omits secure output persistence and encourages serving expiring provider URLs directly.
- **70 maximum:** Omits rights/consent and safety policy for identifiable people or customer-submitted references.
- **75 maximum:** States categorical “no training,” fixed retention/deletion, or regional residency without reconciling the public conflict or citing a governing contract.
- **80 maximum:** Lacks dates and first-party sources for volatile models, prices, limits, or policy.

## Automatic packaging checks

The package fails packaging review, independent of the content score, if:

- The directory contains anything other than `SKILL.md` and `EVAL.md`.
- `SKILL.md` frontmatter has fields other than `name` and `description`, or `name` is not `runway-image`.
- `SKILL.md` references `EVAL.md` or requires hidden evaluation content at runtime.
- Markdown fences are unbalanced.
- A complete example contains a syntax error after environment values are mocked.

## Arithmetic check

Section totals: `8 + 18 + 12 + 20 + 12 + 10 + 12 + 8 = 100`.


