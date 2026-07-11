---
name: google-gemini-image
description: Plan, generate, edit, and quality-check still images with Google's Gemini native image models (Nano Banana), including Gemini 3.1 Flash Image, Gemini 3.1 Flash-Lite Image, Gemini 3 Pro Image, and legacy Gemini 2.5 Flash Image. Use for model and API-route selection, conversational editing, multi-reference composition, thinking and Google Search grounding, resolution/aspect-ratio control, exact-text and brand workflows, SynthID/provenance, safety, privacy, rights, and migration from legacy Gemini or Imagen image endpoints. Do not use for Veo/video generation or Gemini Live/audio work.
---

# Produce still images with Gemini

Treat this as a production discipline, not a bag of adjectives. Establish rights and delivery constraints, choose a route and model, assign references explicit roles, generate a reviewable draft, and repair one defect class at a time.

## Evidence labels and freshness

Interpret labels consistently:

- **Documented fact**: stated in a cited Google first-party source.
- **Inference**: a conclusion drawn from documented capabilities; validate it on the actual workload.
- **Production heuristic**: operational advice, not a provider guarantee.

All volatile facts in this skill were verified **2026-07-09**. Recheck model IDs, launch stages, locations, pricing, quotas, API schemas, retention, and deprecation dates before a consequential run. Provider words such as “best” or “professional” are positioning, not independent benchmark results.

## Bound the job before calling a model

Collect or infer these fields. Stop for user input when an assumption would alter rights, identity, factual meaning, or required deliverables.

```text
deliverable: file count, channel, crop/aspect ratio, minimum pixels, file type
intent: what the image must communicate and to whom
must_preserve: identities, product geometry, approved logo, exact copy, legal marks
may_change: background, lighting, styling, pose, crop, color treatment
references: file -> role -> rights/consent -> priority
factuality: timeless invention | supplied facts | current facts requiring grounding
privacy: public | internal | confidential | personal/biometric
acceptance_tests: exact strings, subject match, layout, factual checks, brand checks
route_constraints: Gemini Developer API or Google Cloud; latency/cost/batch needs
```

Do not cover Veo, motion generation, or Gemini Live/audio. Gemini 3.1 Flash Image and Gemini 3.1 Flash-Lite Image can accept video as context for a still-image result through `generateContent`, but that is an image workflow; do not let it expand this skill into video production.

## Choose the route first

Do not mix payload dialects. Record the route, API interface, SDK version, model ID, location, storage setting, and response schema in the run manifest.

### Gemini Developer API: Interactions API

**Documented facts:** As of June 2026, the Interactions API is GA and Google recommends it for new Gemini API projects. It uses `interactions.create`; the REST endpoint is `https://generativelanguage.googleapis.com/v1beta/interactions` with an API key. `previous_interaction_id` retrieves stored conversation history. Tools, system instructions, and generation configuration are interaction-scoped, so repeat them on later turns. Requests default to `store=true`; paid-tier interactions are retained for 55 days and free-tier interactions for one day unless storage is disabled. `store=false` prevents later use of `previous_interaction_id` and background execution. Custom safety settings are not yet available in Interactions. [Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview)

Use Interactions when server-side continuation, observable steps, current image features, or concise multi-turn editing matters. For sensitive content, evaluate whether paid service terms and storage controls are sufficient; use `store=false` only with an explicit stateless history plan.

Minimal single-turn image request:

```python
from google import genai
import base64

client = genai.Client()  # GEMINI_API_KEY
interaction = client.interactions.create(
    model="gemini-3.1-flash-image",
    input="Create one editorial still image of a wind farm at dawn, viewed from a low hill.",
    response_format={
        "type": "image",
        "mime_type": "image/png",
        "aspect_ratio": "16:9",
        "image_size": "2K",
    },
)
with open("wind-farm.png", "wb") as f:
    f.write(base64.b64decode(interaction.output_image.data))
```

### Gemini Developer API: `generateContent`

**Documented fact:** `generateContent` is considered legacy but remains fully supported. Its payload uses `contents`/`parts`, `generationConfig`, response modalities, and image configuration rather than the Interactions resource schema. [Generate Content image guide](https://ai.google.dev/gemini-api/docs/generate-content/image-generation)

Keep it for an existing integration or a feature not yet exposed by Interactions, such as custom safety settings or Batch API use. Preserve full response parts and thought signatures in stateless multi-turn histories. Do not translate field names by guesswork; consult the current guide for the chosen interface.

Complete Developer API `generateContent` example:

```python
import os
from pathlib import Path

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-3.1-flash-image",
    contents="Create one 16:9 editorial illustration of a coastal wetland at sunrise; no text.",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K"),
    ),
)
images = [part for part in response.candidates[0].content.parts if part.inline_data]
if len(images) != 1:
    raise RuntimeError(f"Expected one image part, received {len(images)}")
images[0].as_image().save(Path("wetland-developer.png"))
```

### Google Cloud / Gemini Enterprise Agent Platform route

**Documented facts:** The Google Gen AI SDK can route through Google Cloud with project credentials and `location="global"`; current model cards list global availability for the three Gemini 3 image models and Cloud security controls such as data residency, CMEK, VPC-SC, and AXT. Cloud REST uses OAuth/ADC and project-scoped `aiplatform.googleapis.com` resources rather than the Gemini Developer API key endpoint. Cloud model availability, launch stage, API version, and security controls are separate contracts and must be checked on the current model card. [Cloud quickstart](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart), [Gemini 3.1 Flash Image model card](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-flash-image), [Cloud Interactions reference](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/interactions-api)

Use the Cloud route when IAM, billing/project governance, enterprise security controls, auditability, Cloud Storage inputs, or Cloud consumption options are requirements. Current documentation may call this surface Gemini Enterprise Agent Platform while older code and environment variables say Vertex AI. Treat product naming as documentation context, not as permission to interchange endpoints.

Complete GA Cloud `generateContent` v1 example using Application Default Credentials:

```python
import os
from pathlib import Path

from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True,
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location="global",
    http_options=types.HttpOptions(api_version="v1"),
)
response = client.models.generate_content(
    model="gemini-3.1-flash-image",
    contents="Create one 4:5 premium studio product backdrop in charcoal and amber; no text or logo.",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="4:5", image_size="2K"),
    ),
)
images = [part for part in response.candidates[0].content.parts if part.inline_data]
if len(images) != 1:
    raise RuntimeError(f"Expected one image part, received {len(images)}")
images[0].as_image().save(Path("product-backdrop-cloud.png"))
```

Before execution, verify whether the chosen workflow uses `client.models.generate_content(...)` or Cloud `client.interactions.create(...)`, which API version it requires, and whether the stable model ID is enabled in that project. The documented Cloud Interactions REST surface is experimental and uses `v1beta1`; when GA API stability is required, prefer Cloud `generateContent` v1 or explicitly accept the experimental Interactions contract. Never silently fall back from Cloud to the Developer API; the auth, retention, controls, quotas, and agreement may differ.

## Select the image model

### Dated capability matrix

| Model | Documented capability at 2026-07-09 | Best-fit inference | Avoid or escalate when |
|---|---|---|---|
| `gemini-3.1-flash-lite-image` (Nano Banana 2 Lite) | Fastest/lowest-cost family member; 1K output only; up to 14 object references; controllable minimal/high thinking; `generateContent` video context for still output; no Search grounding; not optimized for multiple-reference or long sequential editing in the Gemini API guide | High-volume thumbnails, exploration, simple edits, inexpensive first-pass layout tests | Exact brand work, difficult identity continuity, current-fact visuals, or final delivery above 1K |
| `gemini-3.1-flash-image` (Nano Banana 2) | Generalist image model; 0.5K/1K/2K/4K; up to 10 high-fidelity object references and 4 character references; Search grounding plus Image Search grounding; video context for still output; controllable minimal/high thinking | Default candidate for mixed generation/editing, multi-reference products/characters, grounded infographics, and balanced iteration | Use Pro evaluation when the brief has dense copy, complex localization, hard brand constraints, or repeated high-stakes edits |
| `gemini-3-pro-image` (Nano Banana Pro) | Complex professional asset positioning; 1K/2K/4K; up to 6 high-fidelity object references, 5 character references, 3 style references, 14 total; Search grounding; interleaved text/image output | Premium candidate for complex instructions, brand systems, dense layouts, localization, and multi-turn precision | Latency/cost-sensitive bulk work; it still requires exact-text and brand QA and does not guarantee fidelity |
| `gemini-2.5-flash-image` (Nano Banana) | Stable legacy model; 1024-class output; best results with up to 3 input images; no Search grounding or thinking; earliest possible shutdown listed as 2026-10-02 | Compatibility-only path while migrating an existing integration | New work, 2K/4K delivery, many references, grounding, or Gemini 3 thinking workflows |

Sources: [Gemini image generation guide](https://ai.google.dev/gemini-api/docs/image-generation), [2.5 model card](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image), [Gemini deprecations](https://ai.google.dev/gemini-api/docs/deprecations).

**Production heuristic:** begin with 3.1 Flash Image unless an explicit constraint points to Lite or Pro. Run a small representative bake-off before committing a high-volume or high-stakes workload; do not treat provider positioning as measured superiority.

## Control references deliberately

**Documented facts:** Gemini 3 image models accept up to 14 reference images, but fidelity categories differ by model. Gemini 3.1 Flash Image supports up to 10 object references plus up to 4 character references; Pro supports up to 6 object, 5 character, and 3 style references; Lite supports up to 14 object references but is not optimized for multiple-reference or sequential editing. [Gemini image generation guide](https://ai.google.dev/gemini-api/docs/image-generation)

Do not upload 14 images just because the limit exists. More references increase role ambiguity and rights exposure.

For every input, write a reference ledger:

```text
R1: hero product packshot — preserve silhouette, cap, label hierarchy, material color
R2: approved logo master — reproduce geometry and clear space; never invent glyphs
R3: palette/mood — borrow lighting and palette only; do not copy composition
R4: person — identity reference; consent recorded; preserve facial proportions
R5: pose — borrow body pose only; do not inherit identity or wardrobe
priority: R1 > R2 > R4 > R5 > R3
```

Then name those roles in the prompt. Separate identity, object, pose, style, layout, and environment references. If two references conflict, resolve the conflict explicitly rather than asking the model to “blend” them.

**Production heuristic:** for a critical identity or SKU, use one clean canonical view plus only the minimum supplemental angles needed. Crop or remove irrelevant background content from references when authorized. Keep originals, hashes, rights notes, and the exact ordered input list.

## Build prompts as an acceptance contract

Write in positive, concrete language. A robust prompt usually needs:

1. Deliverable and purpose.
2. Primary subject and action.
3. Reference-role mapping and preservation hierarchy.
4. Composition, camera, crop-safe regions, and spatial relationships.
5. Materials, environment, lighting, palette, and style.
6. Exact copy in quotation marks, with capitalization and line breaks.
7. Invariants: what must remain unchanged.
8. Factual source instruction, when grounding is enabled.
9. Output request: one image, aspect, size, format.

Do not use vague quality piles such as “masterpiece, 8K, award-winning” as a substitute for production direction. Describe observable properties. Prefer “an empty pedestrian street at blue hour” to a long negative list.

For edits, lead with the delta:

```text
Edit the supplied image. Change only the background from gray paper to warm limestone.
Keep the bottle silhouette, cap geometry, label placement, logo, all printed copy,
camera position, crop, scale, highlights, and shadow direction unchanged.
Return one image; do not add objects or text.
```

## Use conversation without accumulating drift

**Documented facts:** Interactions can continue with `previous_interaction_id`. That ID preserves conversation inputs and outputs, but does not carry tools, system instructions, or generation configuration; repeat those parameters. With stateless `generateContent`, return thought signatures exactly or use the official SDK chat/history utilities. [Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview), [Thought signatures](https://ai.google.dev/gemini-api/docs/thought-signatures)

Apply this edit loop:

1. Save every accepted image as a versioned artifact.
2. Diagnose one defect class: text, identity, geometry, layout, lighting, or factual content.
3. Request one bounded delta and restate invariants.
4. Reapply response format and any required tool configuration.
5. Compare the result against both the previous accepted image and canonical references.
6. If drift expands, restart from the last accepted image rather than repairing a damaged descendant.

**Production heuristic:** after two failed repairs of the same defect, change strategy: simplify the copy, isolate an element, use Pro, regenerate a clean base, or composite a deterministic asset in post. Do not keep spending turns on an unstable branch.

## Thinking and grounding

### Thinking

**Documented facts:** Gemini 3 image models use an enabled-by-default reasoning process and can create up to two interim thought images. Thinking cannot be fully disabled. Both Gemini 3.1 Flash Image and Gemini 3.1 Flash-Lite Image expose `minimal` (default) and `high` thinking levels. Thought tokens are billed whether or not a summary is viewed; interim thought images are not separately charged. [Gemini image generation guide](https://ai.google.dev/gemini-api/docs/image-generation), [Generate Content thinking controls](https://ai.google.dev/gemini-api/docs/generate-content/image-generation#controlling-thinking-levels), [Flash-Lite Image model card](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-image)

Use high thinking for spatial logic, multi-reference reconciliation, dense infographics, or several interacting constraints. Keep minimal for simple crops, palette changes, and high-volume exploration. Do not expose raw hidden reasoning as production rationale; report decisions and observable evidence.

```python
interaction = client.interactions.create(
    model="gemini-3.1-flash-image",
    input="Create one cutaway diagram of a heat pump with a physically coherent flow path.",
    generation_config={"thinking_level": "high"},
    response_format={"type": "image", "aspect_ratio": "16:9", "image_size": "2K"},
)
```

### Google Search grounding

**Documented facts:** 3.1 Flash Image and 3 Pro Image support Google Search grounding; Lite does not. Only 3.1 Flash Image supports Google Image Search grounding. Image Search grounding cannot search for people. Google stores prompts, contextual information, and generated output for 30 days when Google Search grounding is used, with no opt-out; `store=false` alone therefore does not make a grounded request ZDR. The response can include grounding metadata and required search suggestions/display material. [Gemini image generation guide](https://ai.google.dev/gemini-api/docs/image-generation), [Zero data retention guidance](https://ai.google.dev/gemini-api/docs/zdr)

Use grounding only for genuinely current or externally verifiable facts. Record returned sources, retrieval time, and the claim-to-source mapping. Grounding helps retrieval; it does not make rendered numbers, labels, maps, or claims automatically correct.

```python
interaction = client.interactions.create(
    model="gemini-3.1-flash-image",
    input=(
        "Using current official public sources, create one clean weather infographic for "
        "San Francisco for the next five days. Include date, high/low, and precipitation chance."
    ),
    tools=[{"type": "google_search"}],
    response_format={"type": "image", "aspect_ratio": "16:9", "image_size": "2K"},
)
```

If Image Search is enabled, treat retrieved images as context, not a blanket license to reproduce them. Display a recognizable link to each containing webpage; when showing a source image, provide direct single-click navigation from that image to its containing webpage. Preserve the returned attribution material. Do not use grounded imagery to bypass consent, publicity, copyright, or brand restrictions.

## Set aspect ratio and resolution explicitly

**Documented facts:** Without an input image, the default is 1:1; with an input, the output tends to match the input. Use uppercase `K` values. 3.1 Flash Image supports 0.5K, 1K, 2K, and 4K. Pro supports 1K, 2K, and 4K. Lite supports only 1K. 4K output remains a preview feature on Cloud model cards; 3.1 Flash video input is also preview there. [Gemini image generation guide](https://ai.google.dev/gemini-api/docs/image-generation), [3.1 Flash Cloud model card](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-flash-image)

Supported ratios documented for 3.1 Flash Image include `1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, and `21:9`. Pro and legacy 2.5 use the more conventional set from `1:1` through `21:9`; Lite is 1K-only and its current model card lists conventional and panoramic ratios. Check the current route-specific table before using an extreme ratio.

**Production heuristic:** draft at 1K or 0.5K, approve composition and copy, then regenerate at final resolution from the accepted state. Verify actual pixel dimensions after decoding. “4K” is a model size class, not a promise of a particular broadcast raster or added semantic detail.

## Exact text, trademarks, and brand QA

**Documented fact:** Google recommends generating the required text first, then asking for an image containing that text. Gemini 3 improves text rendering, but Google documents no guarantee of exact spelling, count, kerning, or logo fidelity. [Gemini image generation guide](https://ai.google.dev/gemini-api/docs/image-generation)

For exact copy:

1. Freeze approved source text outside the image model.
2. Keep rendered copy short; quote it exactly and specify line breaks.
3. Generate a composition with a clean, high-contrast text zone.
4. Transcribe the result independently with OCR plus human review.
5. Compare Unicode-normalized strings, punctuation, case, dates, units, and line order.
6. Reject any mismatch. Do not “close enough” regulated, price, dosage, legal, or brand copy.
7. Prefer deterministic typography in a design tool for final critical copy.

For brands and products:

- Require an approved logo master and proof of permission.
- Compare logo geometry, colors, clear space, label hierarchy, pack dimensions, and mandatory marks.
- Never infer that model access grants trademark, trade-dress, publicity, or merchandising rights.
- Do not ask Gemini to recreate a logo from memory when a canonical asset exists.
- For a product hero, consider generating the environment and compositing the exact pack/logo in post.

**Production heuristic:** use Gemini as a concept/composition engine and deterministic compositing for pixel-exact identity assets. Pro’s “brand consistency” positioning is a model-selection signal, not an accuracy warranty.

## Review every output

Run review at decoded full resolution, not from a chat thumbnail.

### Technical

- File opens; expected MIME and alpha behavior; actual dimensions and aspect.
- No unintended crop, padding, compression damage, or color-space surprise.
- Required image count present; do not assume the model obeyed a requested count.

### Visual and instruction adherence

- Primary intent reads at target display size.
- Subject count, anatomy, reflections, shadows, perspective, and occlusion are plausible.
- Reference roles are honored; no identity, SKU, pose, or style leakage.
- Invariants remain unchanged after edits.

### Text, facts, and brand

- Exact OCR comparison and human proofreading.
- Every number, unit, date, map, chart, and current claim checked against recorded sources.
- Logo/pack overlay comparison against canonical assets.
- No invented certifications, endorsements, legal marks, citations, or UI.

### Safety, rights, and provenance

- Consent and lawful basis documented for real-person/biometric references.
- Input and output rights checked for the intended territory and use.
- No deceptive impersonation, non-consensual intimate imagery, exploitation, privacy breach, or prohibited use.
- AI provenance disclosure and asset ledger completed.

## Safety, rights, privacy, and provenance

Google’s prohibited-use policy bars rights violations, including privacy and intellectual-property violations, and forbids non-consensual intimate imagery, deceptive impersonation, harmful misinformation, and other listed harms. Do not evade refusals or filters. [Generative AI Prohibited Use Policy](https://policies.google.com/terms/generative-ai/use-policy)

For a real person, obtain consent appropriate to the edit and distribution; verify identity/publicity rights, special rules for minors, and whether the image implies endorsement or a sensitive trait. Decline deceptive identity substitution, sexualized or intimate edits without consent, surveillance, or misleading political/current-event imagery. A public photo is not automatically reusable.

**Documented facts about Gemini API data use:** Google states that unpaid-service prompts and responses may be used to improve products and may be reviewed by humans; do not submit sensitive, confidential, or personal information to unpaid services. For paid services, Google says prompts and responses are not used to improve products and are processed under the applicable data-processing terms, while limited logging and feature-specific retention may still apply. Interactions storage and Search grounding add their own retention behavior. [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms), [Zero data retention guidance](https://ai.google.dev/gemini-api/docs/zdr)

Do not promise zero retention without checking the exact route, tier, `store` setting, abuse-monitoring arrangement, grounding/tools, logging, and contract. Prefer Cloud governance for enterprise controls when required, but verify project configuration rather than assuming it.

**Documented provenance facts:** all Gemini-generated images include SynthID. On current Cloud models, Content Credentials (C2PA) are automatically added and signed by Google LLC. C2PA authenticates provenance assertions and tamper state; it does not decide whether an image is true or “real.” Non-C2PA-aware editing may break verification. SynthID is an imperceptible pixel watermark designed to survive common edits, but Google says it is not foolproof against extreme manipulation. [Gemini image generation guide](https://ai.google.dev/gemini-api/docs/image-generation), [Cloud Content Credentials](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/content-credentials), [SynthID](https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/)

Preserve original generated files, interaction IDs where permitted, prompts, input hashes, model/route/version, timestamps, grounding sources, and edit history. Do not strip provenance to misrepresent AI media as solely human-created.

## Complete examples

These are examples, not mandatory formulas.

### Example 1 — Multi-reference product hero with exact brand constraints

**Intent:** Create a 4:5 e-commerce campaign image while protecting product geometry and an approved logo.

**Model/route:** Gemini Developer API Interactions; `gemini-3-pro-image` because the brief has brand, layout, and copy constraints. Test 3.1 Flash Image against it if cost or latency matters.

**Inputs:** R1 front packshot, R2 side packshot, R3 approved SVG/PNG logo, R4 lighting mood only. Rights to all four recorded. Exact source copy: `NORTHLINE` and `FIELD NOTES / No. 04`.

**Complete prompt:**

```text
Create one premium 4:5 campaign still for an outdoor notebook.

Reference roles:
- R1 and R2 define the exact notebook: preserve its dimensions, rounded corners,
  olive fabric texture, black elastic position, spine construction, and paper color.
- R3 is the approved NORTHLINE logo. Reproduce only this supplied logo; do not
  redesign, stylize, add, or infer any brand mark.
- R4 supplies warm late-afternoon lighting and color mood only. Do not copy its
  objects, composition, landscape, or text.

Composition: notebook at a three-quarter angle on pale sandstone, occupying 58%
of frame height, with open negative space in the upper-left. Camera at 20 degrees
above the surface, natural 70mm perspective. One soft key from camera-right and a
short grounded shadow. No hands or extra products.

Printed cover copy, exactly two elements:
"NORTHLINE"
"FIELD NOTES / No. 04"
Preserve capitalization, slash, spacing, and zero in 04. No other text.

The exact notebook geometry, logo, and printed copy are higher priority than the
lighting reference. Return one image only.
```

**Parameters:** `aspect_ratio="4:5"`, draft `image_size="1K"`, final `"4K"` only after approval; PNG; `store=false` if stateless processing is required and all images are resent.

**Why structured this way:** It gives each reference one job, resolves priority, limits text, and reserves copy-safe space.

**Expected result:** A strong campaign composition with recognizable pack geometry. Do not assume the logo or copy is exact.

**Likely failures and repair:** OCR mismatch -> regenerate without printed copy and composite exact typography; logo deformation -> composite R3; spine/cap drift -> restart from R1/R2 and remove R4; extra props -> bounded edit that restates the inventory.

**QA:** Pixel overlay R1/R2 geometry, logo overlay against R3, OCR exact match, 4:5/dimensions, shadow coherence, rights ledger, provenance retained.

**Meaningful variation:** Use 3.1 Flash Image at 2K for a four-SKU family after a bake-off; keep each SKU in a separately labeled reference slot.

### Example 2 — Conversational localization without layout drift

**Intent:** Generate an English museum poster, then localize only the headline to Spanish.

**Model/route:** Gemini Developer API Interactions; `gemini-3.1-flash-image`; stateful continuation.

**Turn 1 complete prompt:**

```text
Create one 2:3 exhibition poster for a fictional astronomy museum.
Headline exactly: "NIGHT SIGNALS"
Subhead exactly: "A FIELD GUIDE TO THE LISTENING SKY"
Date exactly: "12–28 OCTOBER 2026"
Use an abstract radio telescope silhouette, cobalt-to-black sky, restrained grain,
and a strict Swiss grid. Headline at top, silhouette centered, date at bottom.
No logos, sponsor names, prices, QR codes, or other text.
```

**Parameters:** 2:3, 2K, PNG, high thinking. Save `interaction.id`, output, OCR, and layout reference.

**Turn 2 complete prompt:**

```text
Edit the preceding poster. Change only the headline from "NIGHT SIGNALS" to
"SEÑALES NOCTURNAS". Keep the subhead and date in English. Preserve every other
pixel-level design decision as closely as possible: canvas, grid, telescope,
palette, grain, spacing, type scale, and all element positions. Add no text.
```

Repeat `response_format` and `generation_config`; they are not inherited from `previous_interaction_id`.

**Expected result:** A localized variation with the same visual system.

**Likely failures and repair:** Accent loss or copy mutation -> deterministic text overlay; layout shift -> edit from the saved English image rather than another descendant; inherited tool/config omission -> explicitly resend fields.

**QA:** Exact Spanish Unicode string including `Ñ`; unchanged English strings/date; perceptual diff outside headline region; 2:3 raster; retained interaction/provenance record.

**Meaningful variation:** For five locales, generate a text-free locked background once and compose approved localized typography deterministically instead of five generative edits.

### Example 3 — Grounded current-fact infographic

**Intent:** Produce a same-day public-transit service card using current official information.

**Model/route:** `gemini-3.1-flash-image` with Google Search grounding. Lite is disqualified because it has no grounding; Pro is an alternative for a denser layout.

**Complete prompt:**

```text
Using current official transit-agency sources, create one 16:9 rider information
card for the Red Line for 9 July 2026. State only verified service changes,
affected stations, and effective times. If a required fact is unavailable or
conflicts across sources, omit it and leave a clearly labeled blank review box;
do not infer. Visual style: accessible high-contrast public information design,
large type, simple route line, no decorative illustration. Do not use agency
logos unless retrieved material and our rights permit it. Return the image and
grounding metadata.
```

**Parameters:** tools `[{"type":"google_search"}]`; 16:9; 2K; PNG; high thinking.

**Expected result:** A source-informed draft, not a publish-ready authority.

**Likely failures and repair:** Stale/incorrect time, invented station, malformed route map, missing search-display attribution, or factual copy corruption. Correct source data outside the model; regenerate or typeset deterministically.

**QA:** Human opens each grounding source, records retrieval time, verifies agency authority and every claim, OCRs all rendered text, checks accessibility contrast and map geometry, and gets operational sign-off before publication.

**Meaningful variation:** If the facts are supplied and already approved, disable grounding and treat them as immutable source copy.

### Example 4 — High-volume draft set on Lite

**Intent:** Explore 30 square, text-free botanical icon concepts inexpensively before selecting six.

**Model/route:** `gemini-3.1-flash-lite-image`; 1K only; batch when the current route supports it.

**Complete prompt for each item:**

```text
Create one 1:1 text-free icon of a maidenhair fern for a calm habit-tracking app.
Single centered leaf cluster, readable at 64 px, flat vector-like shapes, two
greens (#1F6B4F and #9CCFAE) on transparent-looking neutral white, consistent
2 px-equivalent rounded outline, no pot, no border, no letters, no symbols,
no gradients. Return one image only.
```

**Parameters:** 1:1, 1K, image-only response. Record request/item IDs because the model may not follow requested image counts.

**Expected result:** Broad concept coverage suitable for selection, not a final icon system.

**Likely failures and repair:** Extra symbols, inconsistent stroke, poor 64 px readability, or no true alpha. Select, redraw/vectorize, and normalize geometry/color deterministically.

**QA:** Downsample to 64 px, silhouette test, palette sampling, duplicate detection, file count, alpha inspection, and human selection.

**Meaningful variation:** Escalate the six selected concepts to 3.1 Flash Image for controlled family refinement; do not continue a long Lite edit chain.

## Dated migration appendix

### From Gemini 2.5 Flash Image

**Documented facts at 2026-07-09:** `gemini-2.5-flash-image` is stable but its deprecation table lists 2026-10-02 as the earliest possible shutdown date; Google says exact shutdown dates are communicated later. Its deprecated preview ID is already retired. The current replacement guidance points to the Gemini 3.1 Flash Image line. 2.5 is 1024-class, works best with at most three input images, and lacks Gemini 3 thinking and Search grounding. [Gemini deprecations](https://ai.google.dev/gemini-api/docs/deprecations), [2.5 model card](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image)

Migration checklist:

1. Inventory stable and preview model strings; reject removed preview IDs in CI.
2. Choose Developer API Interactions, legacy `generateContent`, or Cloud deliberately.
3. Translate response configuration to the chosen schema; do not mechanically rename fields.
4. Add explicit aspect/size and decode validation.
5. Preserve or correctly circulate state/thought signatures.
6. Re-baseline reference fidelity, copy accuracy, safety behavior, latency, and cost on representative prompts.
7. Cut over behind a version flag and monitor blocked/empty/text-only responses.

### From Imagen — migration only

**Documented fact at 2026-07-09:** Gemini API Imagen 4 generation endpoints `imagen-4.0-generate-001`, `imagen-4.0-ultra-generate-001`, and `imagen-4.0-fast-generate-001` are deprecated. Their table lists **2026-08-17 as the earliest possible shutdown date**, not a guaranteed exact date; Google recommends `gemini-3.1-flash-image` and says exact shutdown dates are communicated later. [Gemini deprecations](https://ai.google.dev/gemini-api/docs/deprecations), [Gemini image generation guide](https://ai.google.dev/gemini-api/docs/image-generation)

Do not build new Imagen expertise here. Map each Imagen workload by actual requirement—single-shot generation, deterministic seed, negative prompt, mask/edit, output count, safety fields, watermark controls—not by model name. Gemini is conversational and multimodal; its request/response, editing, count behavior, safety controls, provenance, and determinism are not drop-in equivalents. Treat 2026-08-17 as the migration deadline because service may end on or after that earliest date; do not wait for a later exact-date notice.

## Official sources

Verified 2026-07-09:

- [Gemini native image generation guide](https://ai.google.dev/gemini-api/docs/image-generation)
- [Legacy `generateContent` image guide](https://ai.google.dev/gemini-api/docs/generate-content/image-generation)
- [Interactions API overview](https://ai.google.dev/gemini-api/docs/interactions-overview)
- [Gemini 3.1 Flash Image model card](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image)
- [Gemini 2.5 Flash Image model card](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image)
- [Gemini API deprecations](https://ai.google.dev/gemini-api/docs/deprecations)
- [Cloud 3.1 Flash Image model card](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-flash-image)
- [Cloud 3.1 Flash-Lite Image model card](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-flash-lite-image)
- [Cloud Gemini 3 Pro Image model card](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-pro-image)
- [Cloud image best practices](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/gemini-image-generation-best-practices)
- [Cloud image limitations](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/gemini-image-generation-limitations)
- [Cloud responsible image generation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/gemini-image-responsible-ai)
- [Gemini API terms](https://ai.google.dev/gemini-api/terms)
- [Gemini API zero-data-retention guidance](https://ai.google.dev/gemini-api/docs/zdr)
- [Generative AI Prohibited Use Policy](https://policies.google.com/terms/generative-ai/use-policy)
- [Cloud Content Credentials](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/content-credentials)
- [Google DeepMind SynthID explanation](https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/)
