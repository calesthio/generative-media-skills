---
name: google-cloud-vision
description: Use this skill when an agent needs Google Cloud Vision API for still-image understanding: labels, object localization, OCR, document text, SafeSearch, image properties, crop hints, web detection, batch annotation, Cloud Storage based pipelines, confidence evaluation, privacy, quotas, cost, and QA. Do not use it for Gemini multimodal reasoning, video analysis, image generation, custom model training, product catalog search design, or human reference/authenticity review.
---

# Google Cloud Vision API for still-image understanding

Use Google Cloud Vision when the production task needs structured annotations from still images: general labels, object boxes, text/OCR, dense document text, explicit-content likelihoods, dominant colors, crop suggestions, or web-reference signals. Treat it as a computer-vision annotation service, not as a conversational image reasoner.

Verified on 2026-07-11 against first-party Google Cloud documentation whose Cloud Vision pages were last updated 2026-07-07 unless otherwise noted. Pricing, quotas, endpoints, product lifecycle, supported features, and model behavior are volatile; recheck the linked Google pages before promising a production SLA, budget, data-region commitment, or migration path.

## Use and non-use boundaries

Documented fact: Cloud Vision API feature types include `TEXT_DETECTION`, `DOCUMENT_TEXT_DETECTION`, `LABEL_DETECTION`, `OBJECT_LOCALIZATION`, `SAFE_SEARCH_DETECTION`, `IMAGE_PROPERTIES`, `CROP_HINTS`, and `WEB_DETECTION`, among other features such as landmarks, logos, and faces. Source: Google Cloud Vision [features list](https://docs.cloud.google.com/vision/docs/features-list), verified 2026-07-11.

Use Cloud Vision for:

- Still images that need stable JSON fields rather than prose: labels with scores, object bounding polygons, OCR structure, SafeSearch likelihoods, dominant color values, crop vertices, web matches, or batch outputs.
- Backend media pipelines where images live in Cloud Storage and annotations must be stored, audited, thresholded, or joined with internal records.
- High-throughput OCR triage, moderation prefilters, asset tagging, crop automation, or web-reference discovery where deterministic fields and quotas matter more than open-ended reasoning.

Do not use Cloud Vision as the primary tool for:

- Gemini multimodal reasoning: use Gemini/Vertex AI image understanding when the user asks for reasoning, visual question answering, comparison across many images, narrative descriptions, explanation, or flexible prompt-following. Documented distinction: Gemini image understanding accepts image-plus-text prompts and has limitations around precise spatial localization and possible hallucination; Cloud Vision returns feature-specific annotations. Source: Google Cloud Gemini image understanding docs, last updated 2026-07-09, verified 2026-07-11.
- Video analysis: use Video Intelligence API or another video-understanding provider for per-shot, per-frame, segment-level, object tracking, text in video, explicit content in videos, audio transcription, or live-stream analysis. Source: Google Cloud Video Intelligence overview, verified 2026-07-11.
- Image generation or editing: Cloud Vision analyzes images; it does not generate, retouch, upscale, remove backgrounds, or alter pixels.
- Custom category training: use AutoML Vision or current Vertex AI/AutoML routes when the business needs a custom labeler/object detector. Cloud Vision's standard features are fixed provider models. The Product Search docs also state that AutoML Vision enables custom image labeling; verify current AutoML/Vertex recommendations before starting a new custom-model project.
- Human reference analysis, provenance, or legal authenticity: `WEB_DETECTION` can return matching pages/images and inferred web entities, but it does not prove authorship, license, consent, manipulation history, source-of-truth identity, or rights clearance. Use it as evidence collection for a human reviewer, not as the reviewer.

## Feature selection map

Documented facts below are from the Google Cloud Vision feature docs, verified 2026-07-11.

| Need | Request feature | Output to expect | Production notes |
| --- | --- | --- | --- |
| Sparse text in a photo, sign, label, package, screenshot region | `TEXT_DETECTION` | `textAnnotations` plus `fullTextAnnotation`; extracted UTF-8 text, words, bounding boxes | Use for text embedded in broader imagery. Do not force language hints unless the language is known; Google says empty hints usually yield best automatic detection, and wrong hints can hinder results. |
| Dense page, scanned form, document image, handwriting, PDF/TIFF OCR | `DOCUMENT_TEXT_DETECTION` | `fullTextAnnotation` hierarchy: Page -> Block -> Paragraph -> Word -> Symbol; dense document structure | Takes precedence if both OCR features are requested. Use Document AI instead when you need structured form parsing, entity extraction, document workflows, or specialized processors. |
| General image tags | `LABEL_DETECTION` | `labelAnnotations` with description, score, topicality, and MID | Good for search tags and coarse categorization. Do not treat labels as exhaustive or mutually exclusive taxonomy. |
| Objects with locations | `OBJECT_LOCALIZATION` | `localizedObjectAnnotations` with English object names, scores, MIDs, and normalized vertices in `[0,1]` | Use for bounding-box workflows. Labels are returned in English; translate downstream if needed. |
| Explicit-content prefilter | `SAFE_SEARCH_DETECTION` | Likelihoods for `adult`, `spoof`, `medical`, `violence`, and `racy`: `UNKNOWN`, `VERY_UNLIKELY`, `UNLIKELY`, `POSSIBLE`, `LIKELY`, `VERY_LIKELY` | Design policy thresholds per category. Do not collapse the five categories into one opaque score without documenting why. |
| Dominant colors | `IMAGE_PROPERTIES` | Dominant RGBA colors, score, pixel fraction | Google says `ColorInfo` does not carry absolute color-space info; assume sRGB unless your pipeline controls color management. |
| Automated crop suggestions | `CROP_HINTS` | Crop polygons, confidence, importance fraction; optional aspect ratios | You can supply up to 16 width:height aspect ratios. Crop hints are saliency suggestions, not art direction; check brand, faces, product edges, and text manually or with additional rules. |
| Web context and reverse-image-like signals | `WEB_DETECTION` | Web entities, full matching images, partial matches, pages with matching images, visually similar images, best-guess labels | Useful for asset triage and context discovery. It is not a license search, provenance guarantee, or fact-checking authority. |

### OCR distinctions that matter

Documented fact: `TEXT_DETECTION` is optimized for sparse areas of text within a larger image. `DOCUMENT_TEXT_DETECTION` is optimized for dense text, document images, handwriting, and PDF/TIFF file OCR, and it takes precedence when both OCR features are requested. Source: [OCR docs](https://docs.cloud.google.com/vision/docs/ocr) and [features list](https://docs.cloud.google.com/vision/docs/features-list), verified 2026-07-11.

Production heuristic: choose OCR by the visual shape of the image, not by the file extension alone. A product photo with a nutrition label may need `TEXT_DETECTION` for quick copy extraction, while a phone photo of a printed invoice should usually use `DOCUMENT_TEXT_DETECTION` because block/paragraph/word structure is valuable.

Documented fact: Cloud Vision's `fullTextAnnotation` organizes extracted UTF-8 text as Page -> Block -> Paragraph -> Word -> Symbol, with bounding boxes and per-component properties. The older `textAnnotations` output continues to be supported. Source: [dense document text tutorial](https://docs.cloud.google.com/vision/docs/fulltext-annotations), verified 2026-07-11.

Production heuristic: evaluate OCR output at the unit your downstream workflow consumes. For search indexing, document-level text recall may be enough. For captions, forms, or layout-sensitive design review, measure word-level accuracy, bounding-box placement, reading order, line breaks, and confidence behavior separately.

## Request modes, storage, and IAM

Documented fact: synchronous `images:annotate` returns inline annotations and accepts up to 16 images per request. Offline asynchronous `images:asyncBatchAnnotate` starts a long-running operation and writes JSON output to a Cloud Storage bucket; it accepts up to 2000 image files per request. Source: [batch image annotation](https://docs.cloud.google.com/vision/docs/batch) and [quotas](https://docs.cloud.google.com/vision/quotas), verified 2026-07-11.

Documented fact: file annotation has separate limits. Synchronous `files:annotate` can annotate one file and up to 5 pages. Asynchronous `files:asyncBatchAnnotate` can annotate up to 2000 pages per PDF/TIFF file and writes JSON to Cloud Storage. Source: [batch](https://docs.cloud.google.com/vision/docs/batch), [PDF/TIFF OCR](https://docs.cloud.google.com/vision/docs/pdf), and [quotas](https://docs.cloud.google.com/vision/quotas), verified 2026-07-11.

Documented fact: for PDF/TIFF offline large batch annotation, Google currently supports only `DOCUMENT_TEXT_DETECTION` and `TEXT_DETECTION`; the file must be in Cloud Storage, output is written to Cloud Storage, and API keys are not supported for `files:asyncBatchAnnotate`. The authenticating account must have access to the input and write permission to the output bucket; Google names `roles/editor` or `roles/storage.objectCreator` or above for output creation in its PDF/TIFF docs. Source: [PDF/TIFF OCR](https://docs.cloud.google.com/vision/docs/pdf), verified 2026-07-11.

Documented fact: Cloud Vision can fetch remote HTTP/HTTPS image URLs, but Google warns that completion is not guaranteed because hosts can deny, throttle, or be throttled for abuse-prevention reasons; Google recommends not depending on externally hosted images for production. Source: multiple Cloud Vision feature docs, verified 2026-07-11.

Production heuristic: in production, copy user-supplied or third-party images into a controlled Cloud Storage bucket before annotation. This gives stable access, uniform IAM, retryability, lifecycle rules, audit logs, and cleaner deletion.

Production checklist for Cloud Storage pipelines:

- Put input images and async outputs in separate prefixes or buckets.
- Grant the calling service account read access to input objects and create/write access to the output prefix; avoid broad project roles unless the deployment already requires them.
- Use object lifecycle policies to delete raw images and annotation outputs according to privacy and audit requirements.
- Record the feature list, image URI, operation name, request time, and output URI so failed items can be retried without reprocessing successful items.
- For external image URLs, first download, hash, validate type/size, scan for policy issues if needed, and upload to Cloud Storage.

## Region and data handling

Documented fact: for OCR features (`TEXT_DETECTION` and `DOCUMENT_TEXT_DETECTION`), Cloud Vision supports the global endpoint plus region-based endpoints for United States and European Union processing/storage: `us-vision.googleapis.com` and `eu-vision.googleapis.com`. Google says this regional functionality currently only applies to OCR. Source: [OCR docs](https://docs.cloud.google.com/vision/docs/ocr) and [PDF/TIFF OCR](https://docs.cloud.google.com/vision/docs/pdf), verified 2026-07-11.

Documented fact: Google says it does not use content sent to Vision API for purposes other than providing the service, does not make submitted content public, does not use submitted content to train/improve Cloud Vision features, and does not claim ownership of submitted content. For online operations, image data is processed in memory and not persisted to disk. For asynchronous offline batch operations, Google stores the image briefly to perform analysis and return results, typically deleting it after processing with a failsafe TTL of a few hours. Google also temporarily logs metadata such as request time and request size. Source: Cloud Vision [Data Usage FAQ](https://docs.cloud.google.com/vision/docs/data-usage), verified 2026-07-11.

Production heuristic: privacy obligations do not end at the API boundary. Check whether the image contains faces, IDs, minors, medical content, location data, documents, or confidential products. Minimize retention in your own buckets, avoid public URLs, redact before annotation when the task permits, and keep the annotation JSON under the same access controls as the source image.

## Quotas, limits, and cost model

Documented facts from Google Cloud Vision quotas and pricing, verified 2026-07-11:

- Quotas are project-level and shared across applications/IP addresses in the project. Quotas have defaults and can typically be adjusted; system limits are fixed.
- Current default quotas include 1800 requests per minute except listed request types, 1800 label-detection requests per minute, 1800 text-detection requests per minute, 8000 asynchronous image-annotation images in processing, 10000 asynchronous document-text pages in processing, and 300 batch requests per day.
- System limits include 20 MB image file size, 10 MB JSON request object size, 1 GB PDF file size, 16 images per `images:annotate`, 2000 images per `images:asyncBatchAnnotate`, 5 pages per `files:annotate`, and 2000 pages per `files:asyncBatchAnnotate`.
- Base64 encoded images may exceed the JSON size limit even when the original image is within the file-size limit; Google notes base64 can be about 37 percent larger. Larger images should be hosted on Cloud Storage or a publicly accessible URL.
- Billing is per image or per file page, and each feature applied to an image is a billable unit. For example, Label Detection plus Face Detection on one image bills one unit for each feature. For PDF files, each page is treated as an individual image.
- As of the pricing page fetched on 2026-07-11, first 1000 units/month are free. Units 1001 to 5,000,000/month were listed at: Label/Text/Document Text/Image Properties $1.50 per 1000 units, Object Localization $2.25 per 1000, Web Detection $3.50 per 1000, SafeSearch free with Label Detection or $1.50 standalone, Crop Hints free with Image Properties or $1.50 standalone. Higher volume tiers differ by feature. Always recheck [Cloud Vision pricing](https://cloud.google.com/vision/pricing).

Production heuristic: estimate cost as:

```text
billable_units = number_of_images_or_pages * number_of_paid_features_per_image
```

Then adjust for bundle behavior such as SafeSearch with Label Detection and Crop Hints with Image Properties, free monthly tier, downstream Cloud Storage charges, retries, failed-item handling, and non-USD SKU pricing.

## Confidence and QA practice

Documented fact: Cloud Vision returns feature-specific scores, likelihood enums, bounding polygons, normalized vertices, confidence values, topicality values, crop importance fractions, and web entity/match fields depending on feature. Source: Cloud Vision feature docs and response examples, verified 2026-07-11.

Production heuristics for evaluation:

- Do not use one universal threshold across all features. Calibrate per feature, category, language, asset source, and downstream risk.
- Keep a labeled holdout set from the actual production image distribution: low light, motion blur, compressed social images, screenshots, rotated phone photos, packaging variants, dense documents, handwriting, multilingual text, stylized typography, occlusions, and edge cases that trigger policy review.
- For labels and objects, measure precision/recall at candidate thresholds and inspect false positives that would create bad user-facing tags.
- For object localization, evaluate both class correctness and box quality. Normalized vertices need conversion to pixel coordinates before visual QA.
- For OCR, measure exact text accuracy, normalized text accuracy, reading order, word-level bounding boxes, language coverage, and line-break/layout fidelity.
- For SafeSearch, tune category-specific routing: for example, `adult` and `racy` may drive age gates, while `medical` should not automatically suppress legitimate health or educational material.
- For crop hints, evaluate visible subject retention, product/logo completeness, text preservation, and whether the suggested aspect ratio works with actual platform safe areas.
- For web detection, audit stale URLs, unrelated visually similar images, search-index bias, and whether page titles/entities are being mistaken for verified facts.
- Log raw responses for an internal sample under access controls, but expose only task-specific fields to non-technical reviewers.

## Product search, custom models, and lifecycle boundaries

Documented fact: Vision API Product Search lets retailers create products with reference images, group products into product sets, and query with user images to return visually and semantically similar products. It supports product categories including homegoods, apparel, toys, packaged goods, and general. Source: [Vision API Product Search docs](https://docs.cloud.google.com/vision/product-search/docs), verified 2026-07-11.

Documented fact: the Product Search documentation currently displays a maintenance-mode notice: "The Product Search feature is in maintenance mode. For better scalability and the same functionality as Product Search, use the Vision Warehouse." Source: [Vision API Product Search docs](https://docs.cloud.google.com/vision/product-search/docs), verified 2026-07-11.

Production heuristic: do not design new catalog search systems around legacy Product Search without validating the lifecycle and Vision Warehouse migration path with current Google docs and account support. For simple one-off tagging or object detection, standard Cloud Vision may be enough. For custom business taxonomies, train/evaluate a custom model path. For ecommerce visual similarity at scale, evaluate Vision Warehouse/current Google retail search offerings rather than assuming Cloud Vision label/object APIs are catalog search.

## Operational workflow

1. Define the annotation contract: exact features, desired fields, thresholds, output schema, and human-review route.
2. Validate input handling: accepted file type, size, resolution, orientation, EXIF, color profile assumptions, Cloud Storage URI, IAM, and retention policy.
3. Run a small labeled pilot with representative images and at least one negative-control set.
4. Tune thresholds and post-processing per feature. Keep raw confidence values for analysis, but output decisions as explicit labels such as `pass`, `review`, or `block` with reasons.
5. Choose sync for small user-facing interactions; choose async batch for large backfills, PDF/TIFF OCR, and offline jobs.
6. Estimate cost and quota. Include every feature per image/page, retries, Cloud Storage, and monthly free tier. Request quota changes before launch.
7. Add QA dashboards: failure rates by feature, empty responses, low-confidence rates, OCR character error, moderation review overturn rate, and batch-operation queue lag.
8. Revalidate after major source-distribution changes: new camera app, new region/language, new packaging, new document template, new moderation policy, or Google API behavior/pricing changes.

## Example: multi-feature asset intake annotation

Example, not a mandatory formula.

Production intent: tag incoming still images for a media library, identify major objects, prefilter explicit content, extract sparse text, and store enough raw data for QA.

Provider and feature choice: Cloud Vision `LABEL_DETECTION`, `OBJECT_LOCALIZATION`, `SAFE_SEARCH_DETECTION`, and `TEXT_DETECTION` on controlled Cloud Storage inputs. This is better than Gemini because the pipeline needs structured fields and repeatable thresholds, not a prose description.

Inputs and constraints:

- Images are uploaded to `gs://media-intake-prod/raw/YYYY/MM/DD/...`.
- User-facing tags must have high precision.
- Any SafeSearch `adult` or `violence` value of `LIKELY` or `VERY_LIKELY` routes to review before publication.
- OCR is for search indexing only; layout is not required.

Complete REST request body:

```json
{
  "requests": [
    {
      "image": {
        "source": {
          "imageUri": "gs://media-intake-prod/raw/2026/07/11/example.jpg"
        }
      },
      "features": [
        { "type": "LABEL_DETECTION", "maxResults": 20 },
        { "type": "OBJECT_LOCALIZATION", "maxResults": 20 },
        { "type": "SAFE_SEARCH_DETECTION" },
        { "type": "TEXT_DETECTION" }
      ]
    }
  ]
}
```

Interpretation plan:

- Keep labels with `score >= 0.80` as publishable candidate tags only if they are on the approved vocabulary list.
- Keep labels with `0.55 <= score < 0.80` as internal search-only tags.
- Convert object `normalizedVertices` to pixel coordinates for reviewer overlays.
- Route SafeSearch `LIKELY`/`VERY_LIKELY` in `adult` or `violence` to human review; do not auto-delete.
- Store extracted OCR text in the search index but hide it from public captions until a reviewer approves it.

Why structured this way: Cloud Vision bills each selected feature, so the request includes only features used by downstream decisions. The thresholds are production policy, not provider truth; they must be calibrated with a labeled sample.

Likely failure modes:

- Overbroad labels such as "product" or "font" clutter search unless filtered.
- Object boxes may miss small or occluded objects.
- SafeSearch can route news, medical, or documentary images to review.
- OCR may misread stylized logos or low-resolution text.

Meaningful variations:

- Add `IMAGE_PROPERTIES` and `CROP_HINTS` when the asset pipeline also produces color palettes and social crops.
- Remove `TEXT_DETECTION` when images never contain useful text.
- Use async batch for nightly backfills or migration imports.

## Example: dense document OCR from PDF/TIFF

Example, not a mandatory formula.

Production intent: extract text from scanned PDF statements for internal search and document routing.

Provider and feature choice: Cloud Vision `files:asyncBatchAnnotate` with `DOCUMENT_TEXT_DETECTION`, because the input is a multi-page dense document in Cloud Storage. Consider Document AI instead if the goal is to parse fields, tables, entities, forms, or invoices into structured business records.

Inputs and constraints:

- Input file: `gs://doc-intake-prod/incoming/acct-1931.pdf`.
- Output prefix: `gs://doc-intake-prod/vision-output/acct-1931/`.
- Service account has read permission on the input object and create/write permission on the output prefix.
- The PDF must be within current Cloud Vision file/page limits.

Complete REST request body:

```json
{
  "requests": [
    {
      "inputConfig": {
        "gcsSource": {
          "uri": "gs://doc-intake-prod/incoming/acct-1931.pdf"
        },
        "mimeType": "application/pdf"
      },
      "features": [
        {
          "type": "DOCUMENT_TEXT_DETECTION"
        }
      ],
      "outputConfig": {
        "gcsDestination": {
          "uri": "gs://doc-intake-prod/vision-output/acct-1931/"
        },
        "batchSize": 10
      }
    }
  ]
}
```

HTTP endpoint:

```text
POST https://vision.googleapis.com/v1/files:asyncBatchAnnotate
```

Expected result: the initial response returns a long-running operation name. When the operation state is `DONE`, JSON output files appear under the destination prefix. Each output resembles image OCR output and includes context about the source file and page range.

QA plan:

- Sample at least 50 pages across templates and scan qualities.
- Check page count, empty-page handling, text extraction recall, reading order, and whether headers/footers create duplicate search hits.
- Flag pages with unusually low extracted character count for manual review.
- Compare Cloud Vision to Document AI on a subset if field extraction is later requested.

Likely failure modes:

- Wrong IAM on the output bucket causes async failure.
- A large base64 or inline request is attempted even though PDF/TIFF batch OCR requires Cloud Storage.
- The team expects key-value form parsing, which belongs in Document AI, not raw Vision OCR.

Meaningful variations:

- Use `eu-vision.googleapis.com` or `us-vision.googleapis.com` regional endpoints for OCR when regional processing/storage requirements apply and current docs still support the needed method.
- Use `TEXT_DETECTION` instead if the file contains sparse text and dense structure is unnecessary.

## Example: social crop QA with crop hints and color properties

Example, not a mandatory formula.

Production intent: prepare editorial images for 1:1, 4:5, and 9:16 social placements while preserving subjects, text, product edges, and brand colors.

Provider and feature choice: Cloud Vision `CROP_HINTS` plus `IMAGE_PROPERTIES`. Crop hints give candidate polygons for requested aspect ratios; image properties provide dominant colors for layout theming or contrast checks.

Inputs and constraints:

- Input image: `gs://campaign-prod/selects/hero-014.jpg`.
- Required crops: 1:1, 4:5, 9:16.
- Text overlays will be added later, so crops must leave safe area.

Complete REST request body:

```json
{
  "requests": [
    {
      "image": {
        "source": {
          "imageUri": "gs://campaign-prod/selects/hero-014.jpg"
        }
      },
      "features": [
        { "type": "CROP_HINTS" },
        { "type": "IMAGE_PROPERTIES", "maxResults": 10 }
      ],
      "imageContext": {
        "cropHintsParams": {
          "aspectRatios": [1.0, 0.8, 0.5625]
        }
      }
    }
  ]
}
```

Interpretation plan:

- Convert each crop hint to pixel coordinates, filling omitted zero `x` or `y` values as zero because Google omits zero coordinate fields in JSON bounding polygons.
- Reject hints that cut through faces, products, logos, readable text, or required legal marks.
- Use dominant colors as candidate palette inputs only after checking actual rendered contrast in the final design.

Why structured this way: crop hints automate first-pass saliency, but final crops are production design decisions. The response's `confidence` and `importanceFraction` help rank candidates, not approve them automatically.

Likely failure modes:

- Saliency favors a face but loses the product.
- Tall crops remove contextual brand elements.
- Dominant colors are not perceptually suitable for text contrast.

Meaningful variations:

- Add `OBJECT_LOCALIZATION` if products must remain fully inside the crop.
- Add OCR if visible text must not be cut.
- Use manual art direction for hero images with legal or brand-review stakes.

## Source notes

Primary first-party sources consulted and verified 2026-07-11:

- Google Cloud Vision [features list](https://docs.cloud.google.com/vision/docs/features-list), last updated 2026-07-07.
- Google Cloud Vision [OCR](https://docs.cloud.google.com/vision/docs/ocr), [full text annotations](https://docs.cloud.google.com/vision/docs/fulltext-annotations), and [PDF/TIFF OCR](https://docs.cloud.google.com/vision/docs/pdf), last updated 2026-07-07.
- Google Cloud Vision feature guides for [object localization](https://docs.cloud.google.com/vision/docs/object-localizer), [SafeSearch](https://docs.cloud.google.com/vision/docs/detecting-safe-search), [image properties](https://docs.cloud.google.com/vision/docs/detecting-properties), [crop hints](https://docs.cloud.google.com/vision/docs/detecting-crop-hints), and [web detection](https://docs.cloud.google.com/vision/docs/detecting-web), last updated 2026-07-07.
- Google Cloud Vision [batch annotation](https://docs.cloud.google.com/vision/docs/batch), [quotas and limits](https://docs.cloud.google.com/vision/quotas), [pricing](https://cloud.google.com/vision/pricing), and [Data Usage FAQ](https://docs.cloud.google.com/vision/docs/data-usage), verified 2026-07-11.
- Google Cloud [Vision API Product Search docs](https://docs.cloud.google.com/vision/product-search/docs), verified 2026-07-11, including current maintenance-mode notice.
- Google Cloud Gemini [image understanding](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/image-understanding), last updated 2026-07-09, verified 2026-07-11.
- Google Cloud [Video Intelligence API docs](https://docs.cloud.google.com/video-intelligence/docs), verified 2026-07-11.