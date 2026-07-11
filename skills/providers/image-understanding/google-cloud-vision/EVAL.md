# Evaluation: google-cloud-vision

This file is the hidden scoring guide for the `google-cloud-vision` skill. Do not expose it to the evaluated agent. Evaluate the agent using only `SKILL.md`, then score its response here.

## Core knowledge checks

Score core knowledge checks at 30 points total: questions 1-6 are worth 5 points each. Award partial credit only for required points that are actually present; for questions with four required points, each required point is worth 1.25 points. Apply the listed critical failure for a question as zero for that question even if isolated correct facts appear elsewhere.

### 1. Cloud Vision versus Gemini multimodal

Question: A user asks for a poetic explanation of what is happening in a complex image and follow-up visual reasoning about why it feels tense. Should the agent choose Cloud Vision?

Expected answer: No. Cloud Vision is best for structured annotations such as labels, boxes, OCR, SafeSearch, properties, crop hints, and web detection. Gemini/Vertex AI image understanding is the better route for open-ended reasoning, prose explanation, and prompt-following, while recognizing Gemini can hallucinate and is not precise for spatial localization.

Required points:

- Distinguishes structured annotation API from multimodal reasoning.
- Mentions Gemini for reasoning/prose or flexible VQA.
- Does not claim Cloud Vision generates rich narrative understanding.
- Does not claim Gemini is always more accurate or deterministic.

Critical failure: recommends Cloud Vision alone for open-ended reasoning and fabricates unsupported narrative detail from labels.

### 2. OCR feature distinction

Question: Explain when to use `TEXT_DETECTION` versus `DOCUMENT_TEXT_DETECTION`.

Expected answer: `TEXT_DETECTION` is optimized for sparse text in larger images such as signs, labels, or screenshots. `DOCUMENT_TEXT_DETECTION` is optimized for dense text, document images, handwriting, and PDF/TIFF OCR; it returns/usefully emphasizes the `fullTextAnnotation` hierarchy and takes precedence if both OCR features are requested. Document AI should be considered when structured form parsing/entity extraction is needed.

Required points:

- Sparse versus dense/document/handwriting distinction.
- Mentions PDF/TIFF path for document text.
- Mentions `fullTextAnnotation` hierarchy or layout structure.
- Mentions Document AI boundary for structured extraction.

Critical failure: says `TEXT_DETECTION` is better for all OCR or treats both features as aliases.

### 3. SafeSearch semantics

Question: What does SafeSearch return, and how should a production system use it?

Expected answer: It returns likelihood enums for adult, spoof, medical, violence, and racy categories. Production systems should set category-specific thresholds and route ambiguous or high-risk cases to review rather than treating it as a universal truth score.

Required points:

- Lists or substantially identifies the five categories.
- Describes likelihood enums rather than numeric scores.
- Advises policy thresholds/human review.
- Does not collapse all categories into one unsupported score.

Critical failure: recommends auto-deleting all `POSSIBLE` results without context.

### 4. Batch and file limits

Question: What are the main sync/async limits and storage requirements an agent should remember?

Expected answer: Synchronous `images:annotate` returns inline results and supports up to 16 images per request. Async `images:asyncBatchAnnotate` writes JSON to Cloud Storage and supports up to 2000 images per request. For files, `files:annotate` handles one file and up to 5 pages, while `files:asyncBatchAnnotate` supports up to 2000 pages per PDF/TIFF file and writes output to Cloud Storage. PDF/TIFF async requires Cloud Storage and proper service account permissions; API keys are not supported for `files:asyncBatchAnnotate`.

Required points:

- Sync image limit 16.
- Async image limit 2000 and GCS output.
- File page limits 5 sync / 2000 async.
- Cloud Storage/IAM requirement for PDF/TIFF async.

Critical failure: proposes inline base64 PDF async processing or ignores Cloud Storage output.

### 5. Cost model

Question: How should cost be estimated for a request that applies label detection, object localization, and OCR to 10,000 images?

Expected answer: Each feature per image is a billable unit, so the base unit count is 10,000 images x 3 features = 30,000 billable feature units, before considering free tier, per-feature prices, bundled feature behavior, retries, storage, and current SKU pricing. Pricing is volatile and must be checked.

Required points:

- Per-image/per-page and per-feature billing.
- Calculates or states 30,000 feature units for the scenario.
- Mentions free tier/current pricing verification.
- Mentions retries/storage or other Google Cloud costs.

Critical failure: bills only 10,000 units because there are 10,000 images.

### 6. Web detection boundary

Question: Can `WEB_DETECTION` prove an image's license or original source?

Expected answer: No. It can return web entities, matching images, pages with matching images, visually similar images, and best-guess labels. Those are evidence for triage or human review, not proof of authorship, rights, consent, provenance, or authenticity.

Required points:

- Names at least two web detection output types.
- States it is not a rights/provenance guarantee.
- Recommends human review or rights workflow.

Critical failure: treats web matches as license clearance.

## Production-decision scenarios

Score production-decision scenarios at 30 points total: scenarios 7-10 are worth 7.5 points each. Award partial credit according to the numbered scoring notes under each scenario. Apply a scenario's critical failure as zero for that scenario.

### 7. Media library intake

Scenario: A studio has 2 million uploaded still images in Cloud Storage. It wants searchable tags, object boxes for preview overlays, sparse OCR for text in posters, and an explicit-content prefilter. It does not need prose descriptions.

Expected decision: Use Cloud Vision async batch image annotation with `LABEL_DETECTION`, `OBJECT_LOCALIZATION`, `TEXT_DETECTION`, and `SAFE_SEARCH_DETECTION`; write outputs to Cloud Storage; process in batches; track operation IDs and failed items; calibrate thresholds with a labeled sample; estimate cost per feature per image; request quotas if needed.

Strong answer demonstrates:

- Correct feature selection.
- Async batch choice for scale.
- Cloud Storage output and IAM awareness.
- Confidence/threshold QA and human-review route.
- Cost/quota planning.

Scoring: 7.5 points total.

- 1.5 correct feature selection.
- 1.5 async batch choice for scale.
- 1.5 Cloud Storage output and IAM awareness.
- 1.5 confidence/threshold QA and human-review route.
- 1.5 cost/quota planning.

Penalize:

- Uses Gemini for all images despite structured-output/no-prose requirement.
- Omits cost multiplication by feature.
- Treats SafeSearch as final moderation decision.

### 8. Scanned invoices

Scenario: A user has 30,000 scanned invoices as PDFs and asks Cloud Vision to extract vendor, amount due, invoice number, and line items.

Expected decision: Cloud Vision `DOCUMENT_TEXT_DETECTION` can OCR the PDFs via `files:asyncBatchAnnotate`, but the requested structured fields and line items are better suited to Document AI or a document extraction pipeline after OCR. The answer should recommend Document AI for form/entity extraction or clearly separate raw OCR from downstream parsing.

Strong answer demonstrates:

- Does not overpromise Cloud Vision as form parser.
- Mentions async PDF/TIFF OCR in GCS if raw OCR is needed.
- Mentions Document AI boundary.
- Mentions QA for text accuracy and field extraction separately.

Scoring: 7.5 points total.

- 2 does not overpromise Cloud Vision as form parser.
- 2 mentions async PDF/TIFF OCR in GCS if raw OCR is needed.
- 2 mentions Document AI boundary.
- 1.5 mentions QA for text accuracy and field extraction separately.

Critical failure: claims Cloud Vision directly returns invoice fields and line items as a supported feature.

### 9. Ecommerce visual search

Scenario: A retailer wants a new production visual product search system for apparel catalog images and asks whether to use Vision Product Search.

Expected decision: Explain that Product Search historically supports product sets and reference images for categories such as apparel, but current docs show Product Search in maintenance mode and recommend Vision Warehouse for better scalability and same functionality. The agent should verify current migration docs/account guidance and not start a new system on legacy Product Search without explicit acceptance.

Strong answer demonstrates:

- Knows what Product Search does.
- Notes maintenance-mode notice and Vision Warehouse recommendation.
- Distinguishes product catalog search from labels/object localization.
- Advises current-doc verification and migration planning.

Scoring: 7.5 points total.

- 1.5 knows what Product Search does.
- 2.5 notes maintenance-mode notice and Vision Warehouse recommendation.
- 1.5 distinguishes product catalog search from labels/object localization.
- 2 advises current-doc verification and migration planning.

Critical failure: presents Product Search as the default current recommendation without lifecycle caveat.

### 10. Regional privacy request

Scenario: A European customer wants OCR on ID documents and asks whether all Cloud Vision processing can be pinned to the EU.

Expected decision: State that Cloud Vision supports EU and US regional endpoints for OCR features (`TEXT_DETECTION` and `DOCUMENT_TEXT_DETECTION`) according to current docs, but this regional functionality currently only applies to OCR. The answer must advise verifying current docs, using `eu-vision.googleapis.com` with the appropriate regional methods, controlling Cloud Storage location/retention/IAM, and checking legal requirements.

Strong answer demonstrates:

- Applies only to OCR, not all features.
- Names EU endpoint or region-based API.
- Mentions storage/retention/IAM beyond API endpoint.
- Avoids legal certainty.

Scoring: 7.5 points total.

- 2.5 applies only to OCR, not all features.
- 1.5 names EU endpoint or region-based API.
- 2 mentions storage/retention/IAM beyond API endpoint.
- 1.5 avoids legal certainty.

Critical failure: claims every Cloud Vision feature can be EU-pinned.

## Applied production tasks

### 11. Write a request plan for asset moderation and tagging

User request: "Build me a Cloud Vision request and review plan for user-uploaded images. I need search tags, dominant colors for theming, explicit-content routing, and OCR for any poster text."

Expected output characteristics:

- Chooses `LABEL_DETECTION`, `IMAGE_PROPERTIES`, `SAFE_SEARCH_DETECTION`, and `TEXT_DETECTION`.
- Uses Cloud Storage URI in the example request or clearly explains why local/base64 is only for small tests.
- Provides a complete request body.
- Defines category-specific SafeSearch routing and label/color/OCR QA.
- Mentions per-feature billing and quota checks.
- Mentions privacy/retention for user-uploaded content.

Scoring: 10 points total.

- 2 feature selection.
- 2 complete request body.
- 2 review/threshold plan.
- 1 Cloud Storage/IAM/storage awareness.
- 1 cost/quota awareness.
- 1 privacy/retention awareness.
- 1 clear limitations/no overclaiming.

Critical failures: unsafe moderation automation with no review path; no OCR distinction; no cost awareness for multiple features.

### 12. Debug a failed async PDF OCR job

User request: "My Cloud Vision PDF OCR job failed. I sent a base64 PDF to images:annotate with DOCUMENT_TEXT_DETECTION and expected JSON back inline. Fix the approach."

Expected output characteristics:

- Explains that PDF/TIFF document OCR should use `files:asyncBatchAnnotate` for large/offline processing, with the PDF in Cloud Storage and output JSON written to Cloud Storage.
- Notes API keys are not supported for `files:asyncBatchAnnotate`; use service account/ADC with input read and output write permissions.
- Gives a corrected request body using `inputConfig`, `mimeType`, `features`, and `outputConfig`.
- Explains long-running operation polling and output files.
- Mentions page/file limits and regional endpoint option for OCR if relevant.

Scoring: 10 points total.

- 3 correct endpoint/request mode.
- 2 corrected request body.
- 2 IAM/auth/Cloud Storage output.
- 1 operation polling.
- 1 limits.
- 1 concise explanation of why original failed.

Critical failure: suggests retrying the base64 PDF in `images:annotate`.

### 13. Review OCR quality for a mixed dataset

User request: "We used Cloud Vision OCR on receipts, street signs, handwritten notes, and screenshots. How do we know if it is good enough?"

Expected output characteristics:

- Separates evaluation by document type and downstream use.
- Recommends `TEXT_DETECTION` for sparse signs/screenshots and `DOCUMENT_TEXT_DETECTION` for dense receipts/handwriting where structure matters.
- Defines metrics: exact/normalized text accuracy, word error/character error, reading order, bounding box quality, language coverage, confidence/empty-output rates.
- Recommends labeled holdout sets, edge cases, thresholding/review, and comparing Document AI if structured receipt extraction is required.

Scoring: 10 points total.

- 2 feature routing.
- 3 metrics.
- 2 representative test set/edge cases.
- 1 downstream-use framing.
- 1 Document AI boundary.
- 1 practical remediation loop.

Critical failure: reports only average confidence with no ground truth.

### 14. Web detection provenance task

User request: "Use Google Cloud Vision to tell me if this campaign image is stolen and whether we can use it."

Expected output characteristics:

- Refuses to treat Cloud Vision as legal/provenance authority.
- Uses `WEB_DETECTION` as evidence gathering: full matches, partial matches, pages with matching images, visually similar images, entities, best-guess labels.
- Provides a human rights-review workflow: inspect pages, licenses, original source, contracts/releases, modification history, and legal counsel if necessary.
- Warns about stale/unrelated matches and search-index limitations.

Scoring: 10 points total.

- 3 boundary/no legal certainty.
- 2 correct web detection outputs.
- 3 human review workflow.
- 1 limitations of web matches.
- 1 clear deliverable format.

Critical failure: says Vision can determine if use is legally allowed.

## Overall rubric

Score out of 100 by summing the question and task scores:

- 30 core knowledge checks: questions 1-6 at 5 points each.
- 30 production-decision scenarios: scenarios 7-10 at 7.5 points each.
- 40 applied production tasks: tasks 11-14 at 10 points each.

Use these coverage categories as a secondary sanity check when explaining a score: Cloud Vision feature knowledge and boundaries; API mode, storage, IAM, quota, and cost correctness; production QA and confidence evaluation; privacy, safety, and human-review judgment; lifecycle awareness for Product Search/custom models/migrations; and quality of examples, request bodies, and actionable workflow design.

Passing threshold: 80. A response below 70 should not be used for production guidance without correction.

Automatic fail conditions:

- Exposes or references this `EVAL.md` to the evaluated agent.
- Inspects or imitates sibling skills when the task forbids it.
- Claims Cloud Vision generates images or performs video analysis.
- Claims Product Search is the current default for new catalog search without mentioning maintenance mode/Vision Warehouse.
- Gives privacy, licensing, or legal certainty unsupported by the API.
- Recommends a request pattern that violates the documented Cloud Storage/PDF/TIFF async requirements for the user's scenario.