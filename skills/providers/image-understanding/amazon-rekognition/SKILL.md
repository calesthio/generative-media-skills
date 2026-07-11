---
name: amazon-rekognition
description: Use this skill when an agent needs production image or video understanding with Amazon Rekognition: labels, objects, scenes, OCR, moderation, image properties, Custom Labels or moderation adapters, stored-video analysis, conditional streaming-video workflows for existing eligible accounts, searchable media libraries, confidence evaluation, S3/IAM/event architecture, privacy, biometric consent, cost control, lifecycle management, and QA.
---

# Amazon Rekognition for Production Image and Video Understanding

Amazon Rekognition is an AWS computer-vision service for analyzing existing images and videos. Use it to extract metadata, screen user-generated content, build searchable media libraries, support media operations, or add narrowly governed identity-verification steps. Do not use this skill for generating images, editing pixels, creating synthetic media, or judging whether a human reference is ethically usable for generation; those are separate generation and reference-analysis tasks.

This skill treats Rekognition as an analysis system that returns probabilistic metadata. It is not a replacement for editorial review, legal review, consent management, or a human moderation policy.

## Evidence Legend

- **Documented fact**: Stated in AWS documentation or AWS-owned service pages. Consequential facts include source links and volatile facts include a verification date.
- **Production heuristic**: Operational guidance inferred from documented behavior and common production requirements; validate against the application, jurisdiction, and risk tolerance.
- **Empirical observation**: A result from a reproducible test. This skill does not include first-party experiments; when you test, record dataset, date, region, API version/model version, thresholds, and confusion matrix.

## Activation Boundaries

Use Rekognition when the user asks for:

- Image labels, objects, scenes, concepts, celebrities, image properties, or bounding boxes.
- OCR in images or stored video, especially signs, packaging, screenshots, thumbnails, or metadata extraction.
- Moderation or brand-safety screening for images, stored video, or UGC workflows.
- Custom object, logo, scene, or concept detection with Amazon Rekognition Custom Labels.
- Custom moderation adapters for domain-specific moderation performance.
- Stored-video analysis: labels, moderation, text, celebrities, faces, people tracking, face search, or segment detection.
- Searchable media libraries from Rekognition metadata stored in a search index or database.
- AWS-native async pipelines using S3, IAM, SNS, SQS, Lambda, Kinesis, CloudTrail, and cost controls.
- Face liveness or face search only when the use case is explicit identity verification, access control, fraud prevention, or user-consented account recovery.

Do not activate for:

- Image generation, video generation, inpainting, upscaling, restoration, or prompt writing for generative models.
- Human likeness reference analysis for creative generation, casting, style transfer, or impersonation. Keep that separate from Rekognition's detection/search APIs.
- General OCR pipelines needing document layout, tables, handwriting-heavy forms, or multi-page documents; consider Amazon Textract or a document OCR system.
- Surveillance normalization: broad public-space identification, covert tracking, protest monitoring, or open-ended watchlists should be refused or escalated to policy/legal review. Rekognition can technically search faces, but this skill does not make that an ordinary production pattern.

## Capability Map

**Documented fact, verified 2026-07-11:** AWS describes Rekognition as a cloud image and video analysis service with APIs for object/scene/concept labels, text detection, unsafe-content moderation, celebrity recognition, face analysis/comparison/search, Custom Labels, image properties, stored-video analysis, streaming-video events, and Face Liveness. Source: AWS Rekognition Developer Guide, "What is Amazon Rekognition?" https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html

### Image Analysis

- `DetectLabels` returns general labels for objects, scenes, activities, concepts, parents, aliases, categories, confidence scores, and bounding boxes for common object instances.
- `DetectLabels` can also request `IMAGE_PROPERTIES`, returning quality scores such as brightness, sharpness, and contrast plus dominant colors for the image, foreground, background, and detected objects when available.
- `DetectText` returns detected words and lines, confidence, line/word relationships, and geometry as bounding boxes and polygons.
- `DetectModerationLabels` returns unsafe-content labels and confidence scores for image moderation.
- `DetectProtectiveEquipment` can detect PPE for safety-compliance workflows.
- `RecognizeCelebrities` and `GetCelebrityInfo` support celebrity recognition, but use only when the product explicitly needs celebrity metadata and has rights/policy clearance.
- `DetectFaces`, `CompareFaces`, and collection APIs support face attributes, comparison, indexing, and search. Treat these as biometric workflows, not generic tagging.

**Documented fact, verified 2026-07-11:** Rekognition image non-storage operations do not persist information discovered about the input image, and no input image bytes are persisted by non-storage operations. Storage-based face operations persist face vectors in collections. Source: AWS "Understanding non-storage and storage API operations" https://docs.aws.amazon.com/rekognition/latest/dg/how-it-works-storage-non-storage.html

### Stored Video Analysis

**Documented fact, verified 2026-07-11:** Rekognition Video analyzes videos stored in S3 asynchronously with `Start*` operations, publishes completion status to SNS, and results are retrieved with `Get*` operations. Source: AWS "Calling Amazon Rekognition Video operations" https://docs.aws.amazon.com/rekognition/latest/dg/api-video.html

Stored-video operations include:

- `StartLabelDetection` / `GetLabelDetection` for labels, events, concepts, and activities over time.
- `StartContentModeration` / `GetContentModeration` for unsafe-content events over time.
- `StartTextDetection` / `GetTextDetection` for OCR over time.
- `StartCelebrityRecognition` / `GetCelebrityRecognition` for celebrity appearances.
- `StartFaceDetection` / `GetFaceDetection` for face metadata over time.
- `StartPersonTracking` / `GetPersonTracking` for person pathing.
- `StartFaceSearch` / `GetFaceSearch` for searching faces in a stored video against a collection. Use only in consented, narrowly scoped identity workflows.
- `StartSegmentDetection` / `GetSegmentDetection` for shot boundaries and technical cues.

**Documented fact, verified 2026-07-11:** Stored video supports H.264 video in MPEG-4 or MOV containers, up to 10 GB and up to 6 hours, with a default maximum of 20 concurrent stored-video jobs per account. Video `Get` results are retained for 7 days, and pagination-token TTL is 24 hours. Sources: AWS "Working with stored video analysis operations" https://docs.aws.amazon.com/rekognition/latest/dg/video.html, AWS "Guidelines and quotas" https://docs.aws.amazon.com/rekognition/latest/dg/limits.html, AWS "Calling Amazon Rekognition Video operations" https://docs.aws.amazon.com/rekognition/latest/dg/api-video.html

### Streaming Video And Bulk Image Analysis Availability

**Documented volatile fact, verified 2026-07-11:** AWS states that Streaming Video and Bulk Image Analysis are no longer available to new customers effective April 30, 2026. Accounts that used these features within the previous 12 months continue to have access; other Rekognition features are not impacted. Source: AWS "Amazon Rekognition feature availability changes" https://docs.aws.amazon.com/rekognition/latest/dg/rekognition-availability-changes.html

For new production designs, prefer:

- Stored-video analysis for files in S3.
- Frame extraction from streams into S3/EventBridge/Lambda or Kinesis-based custom pipelines that call image APIs, if near-real-time analysis is needed.
- Existing eligible streaming customers may use stream processors with Kinesis Video Streams and Kinesis Data Streams or SNS/S3 outputs, but must verify account access and current regional support before promising delivery.

Bulk Image Analysis should likewise be treated as conditional for existing eligible accounts. For new customers, design an S3 manifest or queue-driven worker pipeline that calls the image APIs directly with idempotency, retries, and output persistence.

## Customization Choices

### General Labels vs Custom Labels

**Documented fact, verified 2026-07-11:** AWS recommends standard label detection for common labels and Rekognition Custom Labels when the application needs objects, logos, scenes, or concepts that general label detection does not find. Custom Labels can classify images or detect object locations; it is not designed for analyzing faces, detecting text, or unsafe-content detection. Source: AWS Rekognition Custom Labels Developer Guide, "What is Amazon Rekognition Custom Labels?" https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/what-is.html

Use general `DetectLabels` when:

- The object/scene vocabulary is common enough to appear in Rekognition's general taxonomy.
- The user needs broad tagging, search facets, or rough media-library indexing.
- Precision can be tuned with `MinConfidence`, inclusion/exclusion filters, and human review.

Use Custom Labels when:

- The target is proprietary, domain-specific, visually subtle, or absent from the general taxonomy.
- The deliverable requires a stable business vocabulary, such as SKU families, character IDs, industrial defects, sports-team logos, or shelf fixtures.
- You can assemble labeled positive/negative examples and an evaluation set that represents production conditions.

Custom Labels lifecycle:

1. Define the exact label schema and whether each label is image-level classification or object localization.
2. Build datasets from consented, rights-cleared images; split train/test without near-duplicate leakage.
3. Train a project version and evaluate precision, recall, F1, confidence distributions, and failure clusters.
4. Start the project version only when serving predictions; stop it when idle to control cost.
5. Store predictions and human corrections so retraining improves real failure modes rather than synthetic edge cases.
6. Version labels, thresholds, and downstream business rules together.

### Moderation Adapters

**Documented fact, verified 2026-07-11:** Rekognition Custom Moderation lets users train moderation adapters in projects and pass an adapter to `DetectModerationLabels` to improve performance for specific moderation tasks. Source: AWS "Enhancing accuracy with Custom Moderation" https://docs.aws.amazon.com/rekognition/latest/dg/moderation-custom-moderation.html

Use a moderation adapter when the base moderation model misses or overflags content in a defined domain, such as product imagery, illustrated content, platform-specific policy categories, or recurring false positives. Do not use adapters to bypass policy. The policy taxonomy still needs human owners, appeal paths, and sampled audits.

## Searchable Library Architecture

A production searchable library is not just Rekognition output. It is an ingestion, metadata, review, and retrieval system.

Recommended architecture:

1. Upload images/video to S3 with object keys that avoid personal data in names.
2. Trigger analysis through S3 events, EventBridge, Step Functions, or a queue worker.
3. For images, call synchronous APIs such as `DetectLabels`, `DetectText`, `DetectModerationLabels`, and optionally `DetectLabels` with `IMAGE_PROPERTIES`.
4. For stored videos, call `Start*` with `ClientRequestToken`, `JobTag`, and `NotificationChannel`; consume completion through SNS to SQS or Lambda; fetch paginated `Get*` results after `SUCCEEDED`.
5. Normalize results into a metadata store: asset ID, API name, model/version field when returned, labels/text/moderation events, confidence, timestamps, bounding boxes, taxonomy version, threshold used, region, and analysis date.
6. Index searchable fields in OpenSearch, PostgreSQL full text, DynamoDB plus search service, or another retrieval layer.
7. Keep raw Rekognition JSON for audit and replay, but design user-facing facets from a governed taxonomy rather than dumping every returned label.
8. Reprocess selected assets when AWS model versions, policy rules, or label schemas change.

Production heuristic: store both high-confidence automatically accepted tags and lower-confidence candidates routed to review. This allows recall-oriented search without pretending all metadata is equally reliable.

## Confidence And Evaluation

Rekognition returns confidence scores, not truth. Confidence values are model-specific and task-specific; do not compare a moderation score, label score, OCR score, and face similarity as if they share one calibration.

Evaluation workflow:

1. Define the decision: search recall, auto-tag display, moderation block, moderation review, access approval, content segmentation, or analytics.
2. Build a representative validation set from real production media, including hard negatives, low light, motion blur, crops, compression artifacts, overlays, illustrated content, and demographic/environmental variation when people are present.
3. Label the validation set with the policy or taxonomy that the product actually uses.
4. Run the intended API parameters, including `MinConfidence`, filters, adapters, Custom Labels project version, and region.
5. Measure precision, recall, false positive rate, false negative rate, review volume, and downstream harm by class.
6. Pick thresholds per label and per workflow. Moderation review thresholds are usually lower than auto-block thresholds; search-index thresholds may be lower than user-visible claims.
7. Monitor drift: new content formats, new camera sources, new moderation evasion patterns, and AWS model-version changes can alter performance.

Production heuristic: for moderation, use at least three bands:

- Auto-allow: no relevant labels or scores below review threshold.
- Human review: uncertain or medium-risk labels.
- Auto-block/quarantine: high-confidence severe categories, with an appeal or secondary review path when user rights are affected.

Production heuristic: for media search, expose labels as discovery metadata, not factual assertions. Prefer UI language such as "may contain" or use labels silently as ranking features unless a human has verified them.

## Privacy, Biometric, Consent, And Abuse Boundaries

Rekognition can process faces and create searchable face vectors. That creates biometric risk even when AWS states that collections store vectors rather than images.

Required safeguards for face workflows:

- Establish a lawful basis, explicit user notice, and consent where required before enrollment or search.
- Limit collection scope to a bounded purpose: employee access, account recovery, fraud-resistant onboarding, or user-requested identity verification.
- Provide a non-biometric fallback where feasible, especially for liveness failures and accessibility issues.
- Separate enrollment, verification, audit, and deletion permissions.
- Use high thresholds chosen from validation data, not copied from examples.
- Log every enrollment, search, deletion, threshold change, and decision outcome.
- Define retention periods for source images, audit images, face vectors, liveness reference/audit images, and derived metadata.
- Delete vectors with `DeleteFaces`, users with `DeleteUser`, and collections with `DeleteCollection` when purpose expires.
- Review local biometric, employment, housing, education, law-enforcement, and consumer-protection laws before deployment.

Do not design or normalize:

- Covert identification of people in public spaces.
- Watchlists for political, religious, union, protest, immigration, housing, credit, or employment screening.
- Broad surveillance dashboards that convert every detected face or person path into an identity search.
- Emotion, gender, or age attributes as high-stakes decisions about eligibility, trustworthiness, intent, or protected traits.

Face Liveness boundary:

**Documented fact, verified 2026-07-11:** Face Liveness returns a probabilistic confidence score from 0 to 100, a reference image, and audit images, and AWS says it cannot guarantee perfect results; use it with other factors for risk-based identity decisions. Source: AWS "Detecting face liveness" https://docs.aws.amazon.com/rekognition/latest/dg/face-liveness.html

Use Face Liveness only inside a visible user flow where the user is actively attempting verification. Select challenge type and thresholds after testing on your content and threat model. Denials should offer retry, alternate verification, and support review.

## S3, IAM, Events, And Security

Minimum production requirements:

- Use IAM roles and temporary credentials; avoid long-lived access keys in application code.
- Grant least privilege for exact Rekognition actions, S3 buckets/prefixes, SNS topics, SQS queues, Lambda functions, KMS keys, and CloudWatch logs.
- For stored video, create an IAM service role that lets Rekognition publish to the SNS topic in the same region as the Rekognition endpoint.
- Protect S3 objects with encryption, bucket policies, lifecycle rules, access logging, and object ownership controls.
- Do not put sensitive personal data in S3 keys, Rekognition project names, collection names, tags, SNS topic names, SQS queue names, or free-form fields that can appear in billing or diagnostic logs.
- Use CloudTrail for API activity logging and alarms for unexpected collection creation, indexing spikes, or high-cost API usage.
- Use idempotent `ClientRequestToken` values for stored-video `Start*` calls to prevent duplicate jobs.
- Use SQS dead-letter queues and replay tooling for failed notifications.
- Use exponential backoff with jitter and a queue to smooth bursts.

**Documented fact, verified 2026-07-11:** AWS recommends least-privilege IAM permissions, IAM Access Analyzer, MFA where appropriate, CloudTrail logging, TLS, encryption, and avoiding confidential data in tags or free-form name fields. Sources: AWS "Identity and access management for Amazon Rekognition" https://docs.aws.amazon.com/rekognition/latest/dg/security-iam.html and "Data protection in Amazon Rekognition" https://docs.aws.amazon.com/rekognition/latest/dg/data-protection.html

## Costs And Lifecycle

**Documented fact, verified 2026-07-11:** AWS describes Rekognition as pay-as-you-go with no minimum commitments, with costs varying by feature and usage tier. Pricing details are region- and feature-specific and must be checked on the AWS pricing page before committing a budget. Source: AWS Rekognition Developer Guide "What is Amazon Rekognition?" https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html and AWS pricing page https://aws.amazon.com/rekognition/pricing/

Cost drivers to model:

- Image API calls by feature and image count.
- Stored-video analysis by video minute and operation type.
- Custom Labels training time, project-version inference runtime, and image processing.
- Face metadata storage in collections, if applicable.
- S3 storage, requests, data transfer, KMS, SNS, SQS, Lambda, Step Functions, OpenSearch/database indexing, CloudWatch logs, and review labor.
- Reprocessing after threshold changes, policy changes, or model updates.

Lifecycle controls:

- Use feature flags per API and per customer/workspace.
- Stop Custom Labels project versions when idle.
- Expire raw analysis JSON and intermediate frames according to retention policy.
- Delete SQS messages after successful processing and monitor dead-letter queues.
- Remove unused collections, adapters, projects, and project versions.
- Set AWS Budgets and CloudWatch alarms for daily call volume, video minutes, and Custom Labels runtime.

## QA Checklist

Before launch:

- Confirm API choice matches the task: general labels, OCR, moderation, image properties, Custom Labels, stored-video operation, segment detection, or face workflow.
- Verify current regional availability, account eligibility for any streaming/bulk feature, quotas, and pricing on the deployment date.
- Validate input format, size, codec, duration, color channel, and S3 access.
- Run representative evaluation and record thresholds, metrics, and reviewer guidance.
- Confirm model/version fields are stored when returned.
- Test duplicate job prevention with `ClientRequestToken`.
- Test SNS/SQS/Lambda completion handling, pagination, retries, dead-letter queues, and 7-day stored-video result retrieval deadline.
- Perform security review for IAM least privilege, KMS, CloudTrail, bucket policies, and secret handling.
- Perform privacy review for PII, biometric data, retention, consent, deletion, and user-facing notices.
- Confirm moderation actions have appeal/review paths where user rights or monetization are affected.
- Confirm searchable-library UI does not overstate machine labels as verified facts.

## Example 1: Searchable Product And Lifestyle Image Library

**Example, not a mandatory formula.**

Production intent: build a searchable library for a retail creative team that needs to find images by product type, visible text, dominant color, quality, and brand-safety status.

Provider and APIs: Amazon Rekognition Image with `DetectLabels`, `DetectLabels` using `Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"]`, `DetectText`, and `DetectModerationLabels`.

Inputs and constraints:

- JPEG/PNG images in S3.
- No face collection, no identity search.
- The UI must not claim tags are human-verified unless reviewed.
- Moderation policy has auto-allow, review, and quarantine bands.

Workflow:

1. On S3 upload, send an asset ID and S3 object pointer to SQS.
2. Worker calls `DetectLabels` with `MinConfidence=60`, inclusion/exclusion filters only after initial taxonomy testing, and `IMAGE_PROPERTIES` with a bounded dominant-color count.
3. Worker calls `DetectText` with region/size filters if only packaging text matters.
4. Worker calls `DetectModerationLabels`; severe categories above policy threshold quarantine the asset, medium scores enter review.
5. Store raw JSON plus normalized rows: label, category, aliases, confidence, bounding box, text line/word, color hex, brightness/sharpness, moderation label, model version, API, region, date.
6. Index human-facing search facets from a governed vocabulary, e.g. "shoe", "bottle", "outdoor", "red", "contains text".
7. Sample 2-5% of auto-accepted assets and 100% of quarantined assets for reviewer calibration during launch.

Why structured this way: each API answers a different question. Labels support visual search, text supports packaging/signage retrieval, image properties support creative selection, and moderation protects downstream usage.

Expected results: fast metadata creation for large image sets, searchable facets, searchable OCR snippets, and moderation triage.

Likely failure modes:

- Generic labels such as "Person" or "Apparel" are too broad for business search.
- OCR misses small, stylized, curved, or blurred packaging text.
- Brand-safety false positives occur for swimwear, medical, art, or sports imagery.
- Dominant color from background overwhelms product color unless object-level colors are used when available.

Meaningful variations:

- Add Custom Labels for proprietary SKU families or brand marks.
- Add human-reviewed "verified" tags to override machine tags for hero assets.
- Use a lower label threshold for internal recall but show only reviewed tags externally.

## Example 2: Stored-Video Moderation And Segment Metadata For A Creator Platform

**Example, not a mandatory formula.**

Production intent: analyze uploaded creator videos for moderation triage, searchable metadata, and editorial segment navigation.

Provider and APIs: Amazon Rekognition Stored Video with `StartContentModeration`/`GetContentModeration`, `StartLabelDetection`/`GetLabelDetection`, `StartTextDetection`/`GetTextDetection`, and `StartSegmentDetection`/`GetSegmentDetection`.

Inputs and constraints:

- H.264 MP4/MOV files in S3; reject or transcode other codecs before analysis.
- SNS topic and SQS queue in the same region as Rekognition.
- Stored-video results must be retrieved within 7 days.
- User-facing enforcement requires human review for ambiguous categories.

Workflow:

1. Upload/transcode video to an analysis S3 prefix and write a job record.
2. Start each needed video operation with a deterministic `ClientRequestToken`, useful `JobTag`, and shared `NotificationChannel`.
3. Consume SNS completion messages through SQS; match by `JobId` and `JobTag`.
4. On `SUCCEEDED`, page through `Get*` results immediately and persist raw JSON plus normalized event rows.
5. For moderation, group nearby events into review clips with timestamp padding.
6. For labels/text, store timestamped metadata for search and thumbnail suggestions.
7. For segment detection, store shots and technical cues such as black frames, credits, slates, studio logos, and content segments where returned.
8. Expose review queues with source video, timecodes, labels, confidence, and policy instructions.

Why structured this way: Rekognition Video is asynchronous and can produce large outputs, so event-driven completion and pagination are safer than repeated polling.

Expected results: reviewed moderation decisions, searchable timecoded metadata, and operational segment markers for editorial tooling.

Likely failure modes:

- Missing SNS permissions prevent completion notifications.
- Duplicate `Start*` calls increase cost without idempotency.
- Results expire before retrieval.
- Moderation labels need policy-specific review; raw labels alone are not enforcement decisions.
- Segment detection finds technical cues but does not understand story beats or semantic chapters.

Meaningful variations:

- Use Lambda for server-side completion handling when results should be immediately transformed and stored.
- Add Step Functions to coordinate multiple operations and retries.
- For near-real-time needs in new accounts, extract periodic frames and call image APIs rather than assuming streaming-video feature access.

## Example 3: Narrow Face Liveness And Match For Account Recovery

**Example, not a mandatory formula.**

Production intent: let a user recover access to an account by performing a visible liveness check and comparing the returned reference image against a consented enrollment image.

Provider and APIs: Amazon Rekognition Face Liveness with AWS Amplify FaceLivenessDetector, `CreateFaceLivenessSession`, `GetFaceLivenessSessionResults`, and optionally `CompareFaces`. Avoid collections unless the product requires repeated search against enrolled users and has a retention/deletion program.

Inputs and constraints:

- User is actively attempting recovery and receives notice about biometric processing.
- The workflow has an alternate recovery path.
- Thresholds are chosen from validation data and reviewed by risk/legal stakeholders.
- Audit images and reference image retention are minimized.

Workflow:

1. Backend creates a liveness session for the authenticated recovery attempt context.
2. Frontend uses the Amplify FaceLivenessDetector to guide the user through the check.
3. Backend retrieves liveness score, reference image, and audit images.
4. If liveness is below threshold, allow retry or route to alternate recovery.
5. If liveness passes, compare the reference image to the consented enrollment image using a threshold validated for the user base.
6. Record decision metadata without storing unnecessary images longer than policy allows.
7. Provide appeal/support routing for failures.

Why structured this way: liveness only answers whether the capture appears live; it does not by itself establish identity. Identity requires additional evidence and user-centered failure handling.

Expected results: reduced spoof risk in account recovery while preserving a fallback path.

Likely failure modes:

- Poor lighting, camera quality, disability, skin tone/lighting interactions, network issues, or UI confusion increase false rejects.
- A single threshold copied from a sample is not calibrated to the real population.
- Retaining audit images without a retention policy creates unnecessary biometric risk.

Meaningful variations:

- Use OTP, device reputation, or manual ID review as additional factors.
- Keep one-to-one `CompareFaces` rather than one-to-many search when the user already claims an account.
- Do not repurpose account-recovery enrollment into general monitoring or watchlist search.

## Sources Checked

All source facts below were checked on 2026-07-11.

- AWS Rekognition Developer Guide, "What is Amazon Rekognition?" https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html
- AWS Rekognition API Reference, operation families for Image, Bulk Image Analysis, Custom Labels, Stored Video, Face Liveness, and Streaming Video. https://docs.aws.amazon.com/rekognition/latest/APIReference/Welcome.html
- AWS Rekognition Developer Guide, "Detecting labels in an image." https://docs.aws.amazon.com/rekognition/latest/dg/labels-detect-labels-image.html
- AWS Rekognition Developer Guide, "Detecting text in an image." https://docs.aws.amazon.com/rekognition/latest/dg/text-detecting-text-procedure.html
- AWS Rekognition Developer Guide, "Moderating content." https://docs.aws.amazon.com/rekognition/latest/dg/moderation.html
- AWS Rekognition Developer Guide, "Enhancing accuracy with Custom Moderation." https://docs.aws.amazon.com/rekognition/latest/dg/moderation-custom-moderation.html
- AWS Rekognition Custom Labels Developer Guide, "What is Amazon Rekognition Custom Labels?" https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/what-is.html
- AWS Rekognition Developer Guide, "Working with stored video analysis operations." https://docs.aws.amazon.com/rekognition/latest/dg/video.html
- AWS Rekognition Developer Guide, "Calling Amazon Rekognition Video operations." https://docs.aws.amazon.com/rekognition/latest/dg/api-video.html
- AWS Rekognition Developer Guide, "Analyzing a video stored in an Amazon S3 bucket with Java or Python." https://docs.aws.amazon.com/rekognition/latest/dg/video-analyzing-with-sqs.html
- AWS Rekognition Developer Guide, "Detecting video segments in stored video." https://docs.aws.amazon.com/rekognition/latest/dg/segments.html
- AWS Rekognition Developer Guide, "Working with streaming video events." https://docs.aws.amazon.com/rekognition/latest/dg/streaming-video.html
- AWS Rekognition Developer Guide, "Amazon Rekognition feature availability changes." https://docs.aws.amazon.com/rekognition/latest/dg/rekognition-availability-changes.html
- AWS Rekognition Developer Guide, "Bulk analysis." https://docs.aws.amazon.com/rekognition/latest/dg/bulk-analysis.html
- AWS Rekognition Developer Guide, "Searching faces in a collection." https://docs.aws.amazon.com/rekognition/latest/dg/collections.html
- AWS Rekognition Developer Guide, "Detecting face liveness." https://docs.aws.amazon.com/rekognition/latest/dg/face-liveness.html
- AWS Rekognition Developer Guide, "Understanding non-storage and storage API operations." https://docs.aws.amazon.com/rekognition/latest/dg/how-it-works-storage-non-storage.html
- AWS Rekognition Developer Guide, "Guidelines and quotas in Amazon Rekognition." https://docs.aws.amazon.com/rekognition/latest/dg/limits.html
- AWS Rekognition Developer Guide, "Identity and access management for Amazon Rekognition." https://docs.aws.amazon.com/rekognition/latest/dg/security-iam.html
- AWS Rekognition Developer Guide, "Data protection in Amazon Rekognition." https://docs.aws.amazon.com/rekognition/latest/dg/data-protection.html
- AWS Rekognition pricing page. https://aws.amazon.com/rekognition/pricing/
