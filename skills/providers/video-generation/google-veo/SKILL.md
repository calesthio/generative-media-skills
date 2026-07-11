---
name: google-veo
description: Direct production with Google DeepMind's Veo video-generation family across the Gemini Developer API and Google Cloud Gemini Enterprise Agent Platform (formerly Vertex AI). Use for Veo route and model selection, text/image/reference/first-last-frame/extension workflows, native-audio prompting, camera direction, async API operation, troubleshooting, QA, and responsible commercial content production.
---

# Produce with Google Veo

Treat a Veo request as a shot-production job, not as a generic text completion. Lock the access route, model, input mode, shot contract, and delivery constraints before generating.

## Read evidence labels correctly

- **Documented** means a current first-party Google API document, model card, policy, or technical report says it.
- **First-party evaluation** means Google measured or reported it; do not restate it as independent superiority.
- **Production heuristic** means a practical operating recommendation derived from the documented interface and common shot-production constraints. It is not a provider guarantee.
- **Documentation gap** means Google's current pages conflict or a generic schema exposes a field that the selected model card does not support. Run a low-cost preflight instead of guessing.

All volatile facts in this skill were verified **2026-07-09**. Recheck model lifecycle, quotas, pricing, regional availability, and terms before a paid production run.

## Confirm that Veo is the right Google video model

Use Veo for a shot-generation workflow that specifically benefits from Veo's first/last-frame control, asset references, extension, established publisher-model integration, or Veo-native audio contract. Do not use this skill for video understanding or transcription.

**Documented current product guidance:** Google's Gemini API video overview now recommends Gemini Omni Flash as the default for multimodal coherence, character consistency, factual accuracy, and conversational multi-turn video editing; it positions Veo 3.1 for capabilities such as scene extension, last-frame control, and legacy pipeline integration. Treat that as provider routing guidance, not independent quality proof. If the request is simply “make a video” and does not need a Veo-specific control, compare the current Google video models before committing. See [Video generation in the Gemini API](https://ai.google.dev/gemini-api/docs/video).

## Start with the route, because “Veo 3.1” is not one API contract

### Gemini Developer API

Use the Gemini Developer API when API-key access, one-output calls, and Veo 3.1's natively generated audio are the desired contract.

**Documented, verified 2026-07-09:**

- Current model IDs are `veo-3.1-generate-preview`, `veo-3.1-fast-generate-preview`, and `veo-3.1-lite-generate-preview`.
- These are preview models, accept text and image inputs, return one video, and generate audio with the video. Standard and Fast support 720p, 1080p, and 4K; Lite supports 720p and 1080p, but not 4K or extension.
- Clips are 4, 6, or 8 seconds, but 1080p, 4K, reference-image, and extension jobs require 8 seconds. Output is 24 fps. The prompt limit is 1,024 tokens.
- REST submits to `POST https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predictLongRunning` with `x-goog-api-key`. Poll the returned operation with `GET https://generativelanguage.googleapis.com/v1beta/{operationName}`. Download the returned URI with the API key within the retention window.
- Generated files remain on Google's server for two days. The Gemini API extension route accepts a Veo-generated 720p video from a prior operation, adds seven seconds, and can be repeated up to 20 times while the combined input remains within the documented limit.

See the current [Gemini Veo guide](https://ai.google.dev/gemini-api/docs/veo), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing), and [Gemini release notes](https://ai.google.dev/gemini-api/docs/changelog).

### Gemini Enterprise Agent Platform / Vertex publisher-model route

Use the Google Cloud route when stable model IDs, IAM, Cloud Storage, regional governance, up to four variants per prompt, Provisioned Throughput, or Cloud security controls matter. Current Google documentation calls this Gemini Enterprise Agent Platform; older integrations and environment flags may still say Vertex AI.

**Documented, verified 2026-07-09:**

- Stable IDs are `veo-3.1-generate-001` and `veo-3.1-fast-generate-001`. `veo-3.1-lite-generate-001` is Preview.
- The retired preview IDs `veo-3.1-generate-preview` and `veo-3.1-fast-generate-preview` had an April 2, 2026 retirement date on this route. Do not copy a Gemini Developer API preview ID into the Cloud publisher-model route.
- The stable Standard and Fast cards support text-to-video, image-to-video, first-and-last-frame generation, extension, and asset reference images. Lite supports text/image/extension and no reference images. Official documentation conflicts on Lite first-and-last-frame support: the Veo 3.1 model card lists it, while the dedicated first/last-frame guide lists only Standard and Fast. Treat Lite first/last as unconfirmed until a model-specific preflight succeeds.
- This route supports 1–4 outputs, 4/6/8-second clips, 9:16 or 16:9, 24 fps, MP4, and Cloud Storage output. Reference-image generation is 8 seconds. Official Cloud surfaces also conflict on 4K maturity: the model card and extension guide list 4K, while current mode-specific generation guides still call `"4k"` Preview-only. Use lowercase `"4k"` in REST and preflight the exact endpoint/mode before promising it. Current model cards list `us-central1`; verify location before deployment.
- Pay-as-you-go is not supported on the current Enterprise model card. Confirm fixed quota or Provisioned Throughput before choosing this route for production volume.
- REST submits to `POST https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/us-central1/publishers/google/models/{MODEL}:predictLongRunning` using OAuth. Poll with `POST .../publishers/google/models/{MODEL}:fetchPredictOperation` and body `{"operationName":"..."}`.

See the current [Veo 3.1 model card](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate), [model lifecycle](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions), and [video API guide](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-text).

### Do not flatten route-specific differences

| Contract | Gemini Developer API | Enterprise Agent Platform publisher model |
|---|---|---|
| Authentication | `x-goog-api-key` | OAuth / ADC |
| Current Standard ID | `veo-3.1-generate-preview` | `veo-3.1-generate-001` |
| Current Fast ID | `veo-3.1-fast-generate-preview` | `veo-3.1-fast-generate-001` |
| Current Lite ID | `veo-3.1-lite-generate-preview` | `veo-3.1-lite-generate-001` (Preview) |
| Outputs per call | 1 | 1–4 |
| Output delivery | temporary Gemini file URI | inline result or `storageUri` / GCS URI |
| Operation polling | `GET v1beta/{operationName}` | `POST ...:fetchPredictOperation` |
| Native audio | always on for current 3.1 variants | model-specific; see warning below |
| Stable 3.1 IDs | none documented | Standard and Fast `-001` |

**Documentation gap — audio:** the Gemini Developer API explicitly documents native audio as always on for all three 3.1 variants. The 2026-07-09 Cloud model card lists sound generation as **not supported** for Enterprise Standard and Fast, but **supported** for Enterprise Lite; a generic Cloud parameter schema still contains `generateAudio`. Follow the selected model card, not the generic field list. If Cloud audio is a delivery requirement, run one representative preflight and inspect the actual audio stream before committing budget. Never promise native dialogue from Enterprise Standard/Fast solely because `generateAudio` exists. The current [Cloud model card](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate) is the governing source.

**Documentation gap — generic fields:** `VideoGenerationModelInstance` exposes camera control, masks, style references, and video editing fields, while the Veo 3.1 card says object insertion/removal and style-reference images are unsupported. A schema describes the envelope, not every model's capability. Intersect the schema with the selected model card.

## Choose a Veo variant for the production objective

- Choose **Standard** when a final hero shot, difficult motion, facial performance, precise atmosphere, or best available route quality matters more than throughput. This is a production heuristic; Google does not publish a universal quality ranking for every brief.
- Choose **Fast** for storyboards, creative A/B tests, shot-list exploration, ads at scale, and latency-sensitive services. Google positions Fast for speed and business use cases.
- Choose **Lite** for low-cost/high-volume iteration. On the Gemini Developer API it cannot extend or output 4K and cannot accept reference images. On Enterprise it supports extension and audio according to the current model card but still does not support reference images.
- Use the stable Enterprise `-001` models for long-lived production integrations. Use Developer API preview models only when their contract—especially native audio—is worth preview lifecycle risk.
- Do not use Veo 2 or Veo 3 IDs for new Gemini Developer API integrations; current Gemini docs mark them deprecated. Cloud still lists stable Veo 2/3 IDs without an announced retirement, while its migration guidance recommends Veo 3.1 for new integrations. Do not describe the Cloud IDs as retired unless the current lifecycle page says so.

**Documented price snapshot, Gemini Developer API, 2026-07-09:** Standard with audio is USD $0.40/sec at 720p/1080p and $0.60/sec at 4K; Fast is $0.10/$0.12/$0.30 per second for 720p/1080p/4K; Lite is $0.05/$0.08 per second for 720p/1080p. There is no free tier for Veo. Treat this as a dated budget input, not a permanent price list; recheck the official pricing page.

## Select one generation mode per shot

### Text to video

Use when composition can vary and exploration is valuable. The prompt owns subject, action, setting, look, camera, lighting, timing, and—on an audio-capable contract—sound.

### First-frame image to video

Use when the opening composition, product design, character appearance, or brand color must be anchored. The input image becomes the first frame. Supply motion and sound in the prompt; do not redescribe the image so aggressively that the model must choose between the pixels and text.

**Production heuristic:** prepare the image at the target aspect ratio, with enough space in the direction of motion, no baked-in subtitles, no impossible occlusions, and a physically plausible pose from which the requested action can begin.

### First and last frames

Use when both endpoints matter: product closed-to-open, day-to-night, before/after, or a controlled transition. Pass the first image as `image` and the end image as `lastFrame` / `last_frame`. The two images must depict a plausible transition in the available 4–8 seconds.

**Production heuristic:** hold identity, lens family, camera height, scene geometry, and lighting direction consistent across endpoints. Ask for the motion between frames, not two separate scene descriptions. A large identity or viewpoint discontinuity invites morphing.

### Asset reference images / ingredients

Use up to three `asset` images to preserve one person, character, product, costume, or object across the shot. On Gemini Developer API this is supported by Standard and Fast only; current Gemini docs list `referenceImages` as unavailable for Lite. On Enterprise, Standard and Fast support asset references; Lite does not.

- `referenceImages` are guidance assets, not start frames.
- A start frame uses `image`; current contracts do not let it coexist with `referenceImages` on the same instance.
- Veo 3.1 does not support `style` reference images on the Enterprise route even though the generic schema names that reference type.
- Use a clean view set: distinct angles or components, consistent appearance, neutral backgrounds where possible, and no contradictory versions of the subject.

### Extension

Use when continuity from an existing Veo clip matters more than creating a separate shot.

- Gemini Developer API: input must be the `Video` object from a previous Veo generation; it must be 720p, 16:9 or 9:16, at most 141 seconds, and still available. Each extension adds seven seconds; the returned video includes the original and extension.
- Enterprise: current docs accept an MP4 of 1–30 seconds at 24 fps, 720p/1080p/4K and 9:16/16:9, and return a seven-second extension. Use the route's own guide rather than applying Gemini retention rules.
- The extension conditions on the last second / 24 frames. Dialogue or voice continuity is unreliable if the voice is absent from that final second.

**Production heuristic:** write only the next beat. Preserve subject, direction of travel, camera trajectory, lighting, and sound bed. Do not recap the whole prior clip; a recap can cause repetition or reset.

## Write a Veo shot contract

Google's documented prompt elements are subject, action, style, camera position/motion, composition, focus/lens effects, and ambiance. Audio-capable routes also accept dialogue, sound effects, and ambient sound cues. Build one coherent temporal event from those elements.

**Language boundary, verified 2026-07-09:** Gemini documents English as fully supported and other prompt languages as unevaluated; the Enterprise cards list English. Preflight non-English prompts and spoken dialogue on the exact route. For exact localization, legal wording, or pronunciation, plan ADR or post-production rather than promising native generation fidelity.

Use this order when it helps clarity; it is not a mandatory syntax:

1. State the shot and framing.
2. Name the stable subject and setting.
3. Describe one primary action with a start, development, and finish.
4. Direct one dominant camera behavior.
5. Add lens/focus, light, palette, texture, and medium.
6. Add a separate audio sentence when the route supports audio.
7. State what must remain stable only when necessary.

**Production heuristic:** an eight-second clip has little narrative bandwidth. Prefer one location, one dominant camera move, one focal action, and at most one short exchange. Generate a cut as multiple shots instead of forcing a miniature montage into one prompt.

### Camera language

Distinguish position, framing, and motion:

- Position: eye level, low angle, overhead, aerial.
- Framing: extreme close-up, close-up, medium, wide, two-shot.
- Motion: pan, tilt, dolly/push, pull out, truck, pedestal, arc, crane, handheld, whip pan, drone.
- Optics: macro, wide-angle, telephoto compression, shallow/deep focus, rack focus.

Use one dominant move unless the shot explicitly needs a compound path. “Slow push-in from medium to close-up” is more executable than a list of five camera verbs.

The Cloud generic instance schema also defines `cameraControl` for image-to-video only, with `fixed`, `pan_left`, `pan_right`, `tilt_up`, `tilt_down`, `truck_left`, `truck_right`, `pedestal_up`, `pedestal_down`, `push_in`, and `pull_out`. Treat this as a model-gated API field. Do not combine a conflicting prompt move and enum.

### Audio language

On the Gemini Developer API, audio is always on for Veo 3.1. Prompt three layers separately:

- Dialogue: identify the speaker, delivery, and exact short line.
- SFX: name discrete synced events such as a latch click, pour, footstep, or engine rise.
- Ambience: name the persistent bed such as room tone, surf, distant traffic, or insects.

Keep spoken language short enough for the clip. Separate sound direction into its own sentence. If exact wording, accessibility, localization, or legal copy is critical, plan to replace or mix audio in post even when native audio is requested.

Google's Developer API guide shows quoted dialogue, while the current Cloud best-practice page recommends a colon and no quotation marks to reduce accidental rendered text. Follow the route-specific examples; for robust cross-route prompting prefer `Speaker says: exact line` and inspect for unwanted on-screen text.

### Negative prompts

Use `negativePrompt` / `negative_prompt` for visual failure classes, not for core creative direction. Google recommends noun/attribute lists rather than instructions: `extra fingers, duplicate product, warped logo, subtitles, on-screen text, jump cuts` rather than `do not show text`.

Do not use negative prompts to bypass safety filters or request disallowed content indirectly.

### Prompt enhancement and seeds

- The Enterprise prompt rewriter adds detail and is mandatory for Veo 3 and 3.1; it cannot be disabled. A rewritten prompt is returned only when the original is under 30 words.
- The generic schema's deprecated `enablePromptRewriting` has no effect; `enhancePrompt` is the replacement, but the selected model may still force enhancement.
- A seed improves repeatability slightly; Google explicitly says it does not guarantee determinism. If `sampleCount > 1`, the service uses different random seeds for outputs even when a seed is supplied. Prompt enhancement further weakens reproducibility.

Log the submitted prompt, route, model ID, input hashes, configuration, operation name, returned URI, and chosen output. Do not promise bit-identical regeneration.

## Use the schemas exactly

### Gemini Developer API: Python SDK pattern

```python
import time
from google import genai
from google.genai import types

client = genai.Client()  # GEMINI_API_KEY
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=PROMPT,
    image=START_IMAGE,  # omit for text-to-video
    config=types.GenerateVideosConfig(
        last_frame=END_IMAGE,       # omit unless interpolating
        aspect_ratio="16:9",
        duration_seconds=8,
        resolution="1080p",
        number_of_videos=1,
        negative_prompt="subtitles, on-screen text, duplicate objects",
    ),
)

while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

if not operation.response or not operation.response.generated_videos:
    raise RuntimeError(f"No video returned: {operation}")

generated = operation.response.generated_videos[0]
client.files.download(file=generated.video)
generated.video.save("shot.mp4")
```

For reference assets, omit `image` and `last_frame`; place `VideoGenerationReferenceImage(..., reference_type="asset")` objects in `config.reference_images`. For extension, pass the prior returned `Video` as `video`, request 720p, and omit incompatible image fields.

### Gemini Developer API: REST shape

```json
{
  "instances": [{
    "prompt": "A single coherent shot...",
    "image": {"inlineData": {"mimeType": "image/png", "data": "BASE64"}},
    "lastFrame": {"inlineData": {"mimeType": "image/png", "data": "BASE64"}}
  }],
  "parameters": {
    "aspectRatio": "16:9",
    "durationSeconds": 8,
    "resolution": "1080p",
    "sampleCount": 1,
    "negativePrompt": "subtitles, on-screen text, duplicate objects"
  }
}
```

`image`, `lastFrame`, `referenceImages`, and `video` belong inside the instance. Generation controls belong in `parameters`. Do not move `referenceImages` into `parameters`.

### Enterprise publisher-model REST shape

```json
{
  "instances": [{
    "prompt": "A single coherent shot...",
    "image": {
      "gcsUri": "gs://bucket/input/start.png",
      "mimeType": "image/png"
    }
  }],
  "parameters": {
    "storageUri": "gs://bucket/output/shot-01/",
    "sampleCount": 4,
    "durationSeconds": 8,
    "aspectRatio": "16:9",
    "resolution": "1080p",
    "personGeneration": "allow_adult",
    "negativePrompt": "subtitles, on-screen text, duplicate objects",
    "seed": 17321
  }
}
```

The current Cloud reference accepts JPEG/PNG images as `bytesBase64Encoded` or `gcsUri`. The generic `VideoGenerationModelInstance` mutually excludes `image`, `video`, and `referenceImages`; `lastFrame` requires `image`; `referenceImages` require `prompt`. The instance schema is documented at [VideoGenerationModelInstance](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/Shared.Types/VideoGenerationModelInstance), and parameters at [VideoGenerationModelParams](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/Shared.Types/VideoGenerationModelParams).

## Operate long-running jobs safely

1. Validate route, model ID, input compatibility, billing/quota, region, and output destination before submission. On Enterprise, verify fixed quota or Provisioned Throughput; do not assume pay-as-you-go is available.
2. Persist the returned operation name immediately. Make jobs resumable after process restarts.
3. Poll at a moderate interval—Google examples use 10 seconds for Gemini and 15 seconds for Cloud. Add exponential backoff with jitter for transient 429/5xx responses; do not resubmit a generation merely because polling failed.
4. Apply a wall-clock timeout longer than normal generation latency, but retain the operation name and continue polling later rather than duplicating paid work. Gemini documents 11 seconds to six minutes during peak periods.
5. On completion, inspect operation-level errors before reading outputs. Treat an empty or short result set as a filtered/failed generation, not success.
6. Download or copy outputs promptly. Gemini files expire after two days; Cloud output should be written to a controlled bucket with retention and lifecycle rules.
7. Probe every returned file with a media tool: duration, frame rate, aspect, resolution, codecs, audio-stream presence, and decode errors.

For Cloud event-driven workflows, `pubsubTopic` is available in the generic parameter schema. Use it only after confirming permissions and the selected model path; keep polling as a recovery mechanism.

## Review the generated shot, not just the first frame

Run a full-speed review, a frame-by-frame spot check, and an audio review.

### Technical gate

- File decodes end to end.
- Duration, 24 fps, resolution, and aspect ratio match the request.
- Audio presence matches the route/model contract; dialogue is intelligible and synchronized.
- No unexpected black frames, frozen tail, corrupted frames, clipping, or severe compression artifacts.

### Continuity and craft gate

- Subject identity, product geometry, wardrobe, and scene layout remain stable.
- Primary action completes clearly inside the shot.
- Camera motion follows one intelligible path without unexplained cuts.
- Hands, contact, liquids, reflections, text, logos, and object counts survive temporal inspection.
- First/last-frame jobs reach both intended compositions without a late morph.
- Extension begins continuously from the source tail; motion direction, light, ambience, and voice do not reset.

### Editorial and audio gate

- The opening frame gives the editor a usable in-point and the final frames provide a usable out-point.
- Spoken words are exact enough for intended use; speakers do not swap voices.
- SFX occurs at the visible event; ambience does not pulse or disappear.
- No accidental captions, pseudo-text, watermarks beyond provider provenance, or unauthorized marks appear.
- The shot communicates the intended beat without relying on prompt knowledge.

## Repair by changing one layer

| Failure | Likely cause | First repair |
|---|---|---|
| Subject drifts or product mutates | too many changes; weak anchor | use a clean first frame or 1–3 asset references; reduce action complexity |
| Camera ignores direction | competing camera verbs or action overload | state one move and its start/end framing; remove secondary moves |
| First/last interpolation morphs | endpoints differ in identity, geometry, lens, or light | rebuild compatible endpoints; describe only the bridge action |
| Extension resets | prompt recaps prior scene or tail lacks stable motion | describe only the next beat; preserve tail direction and ambience |
| Dialogue garbles | too many words/speakers; short timing | shorten to one line or one exchange; render voice in post if exactness matters |
| Unwanted text appears | quoted dialogue, signs, or detailed typography | use colon-style dialogue; add `subtitles, on-screen text, letters` to negative prompt |
| Motion is frantic | too many beats for 4–8 seconds | choose one action arc; split into separate shots |
| Seed does not reproduce | nondeterministic sampling or prompt rewriting | accept approximate repeatability; keep the chosen output as the master |
| API rejects a field | route/model/schema mismatch | compare exact route model card and request shape; remove unsupported generic fields |
| Input image fails | unsupported MIME, corrupt base64/GCS permissions, size/aspect issue | verify decode, JPEG/PNG MIME, bytes/URI access, size, and target aspect |
| Safety block or fewer outputs | prompt/input/output filter | inspect support code; remove risky or unauthorized content; never evade the filter |
| Audio-required Cloud job is silent | route-specific audio support mismatch | use a supported audio contract or produce audio separately; do not toggle an unsupported field |

When visual quality fails, keep the route and model fixed during diagnosis. Change one of prompt, input anchor, duration, or camera at a time. When an API contract fails, fix the contract before creative iteration.

## Complete production examples

### Example 1 — Gemini Developer API vertical product spot with native audio

**Intent:** create an eight-second 9:16 social hero shot that keeps a real product consistent and includes synchronized sound.

**Route and model:** Gemini Developer API, `veo-3.1-generate-preview`.

**Inputs:** three authorized PNG asset references of the same espresso machine: front three-quarter, control panel, and cup platform. No start frame. All references show the identical product configuration.

**Complete prompt:**

```text
Vertical 9:16 premium product film, one continuous shot. A compact brushed-steel espresso machine matching the reference images stands centered on a dark walnut counter in a quiet dawn kitchen. Begin in a medium close-up at control-panel height. A warm amber button illuminates; the portafilter locks with a precise quarter turn; a thin caramel stream fills a small white cup as steam catches the window light. The camera makes one slow, smooth push-in and ends on the crema and the unchanged machine logo area. Shallow depth of field, realistic stainless-steel reflections, restrained warm palette, clean commercial lighting, no people.

Audio: quiet kitchen room tone, one crisp metal latch click, a soft pump hum, liquid pouring into ceramic, and a gentle steam hiss. No music and no speech.
```

**Configuration:**

```python
front_ref = types.VideoGenerationReferenceImage(
    image=front_image,
    reference_type="asset",
)
panel_ref = types.VideoGenerationReferenceImage(
    image=panel_image,
    reference_type="asset",
)
platform_ref = types.VideoGenerationReferenceImage(
    image=platform_image,
    reference_type="asset",
)

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    config=types.GenerateVideosConfig(
        reference_images=[front_ref, panel_ref, platform_ref],
        aspect_ratio="9:16",
        duration_seconds=8,
        resolution="1080p",
        number_of_videos=1,
        negative_prompt="people, hands, subtitles, on-screen text, duplicate cups, duplicate machine, warped product geometry",
    ),
)
```

**Why this structure:** references own product identity; the prompt owns a single action chain, one camera move, light, and four audible events. Reference jobs require eight seconds. Native audio is documented on this route.

**Expected result:** one 1080p portrait MP4 with audio. The machine remains recognizable and the latch/pour/steam sounds align with visible events.

**Likely failures and recovery:** if the machine mutates, remove the least consistent reference and simplify the portafilter action. If sounds overlap unnaturally, reduce to room tone, latch, and pour. If the product logo becomes pseudo-text, use a logo-free reference or composite the approved logo in post.

**Meaningful variation:** use Fast for internal A/B exploration, then rerun the approved prompt on Standard; do not claim identical output across variants.

### Example 2 — Enterprise Fast four-way silent storyboard batch

**Intent:** generate four candidate 16:9 establishing shots for editorial selection in a governed Cloud workflow; final sound will be designed separately.

**Route and model:** Gemini Enterprise Agent Platform publisher-model route, `veo-3.1-fast-generate-001`.

**Complete prompt:**

```text
One continuous cinematic establishing shot of a solar-powered research station on a basalt plateau just before sunrise. Three adult field researchers in orange weather shells cross from left to right toward the lit entrance while low fog streams around the buildings. Begin with a wide, low-angle view and perform one slow truck right parallel to the researchers. Deep focus, cool blue predawn light with a thin warm horizon, realistic wind movement, grounded documentary photography, restrained pacing. End with the entrance centered and the researchers still moving right.
```

**Request body:**

```json
{
  "instances": [{"prompt": "One continuous cinematic establishing shot of a solar-powered research station on a basalt plateau just before sunrise. Three adult field researchers in orange weather shells cross from left to right toward the lit entrance while low fog streams around the buildings. Begin with a wide, low-angle view and perform one slow truck right parallel to the researchers. Deep focus, cool blue predawn light with a thin warm horizon, realistic wind movement, grounded documentary photography, restrained pacing. End with the entrance centered and the researchers still moving right."}],
  "parameters": {
    "storageUri": "gs://production-bucket/veo/research-station/v01/",
    "sampleCount": 4,
    "durationSeconds": 8,
    "aspectRatio": "16:9",
    "resolution": "1080p",
    "personGeneration": "allow_adult",
    "negativePrompt": "subtitles, on-screen text, logos, jump cuts, duplicate people, deformed hands",
    "seed": 80421
  }
}
```

**Async sequence:** submit with OAuth to the `:predictLongRunning` publisher-model endpoint, persist `name`, then poll that exact model's `:fetchPredictOperation`. Read returned GCS URIs and probe all four files.

**Why this structure:** Fast and four outputs support selection efficiently. The prompt fixes geography, direction of travel, and one camera path so variants remain editorially comparable. The plan does not depend on native audio because the current Standard/Fast Enterprise card does not support sound generation.

**Expected result:** up to four eight-second candidates in the specified bucket. Fewer than four is a partial/filtered result and must be logged.

**Likely failures and recovery:** if people multiply, reduce the count to two or anchor with a first frame. If trucking becomes an arc, replace prose camera direction with an image-to-video preflight using a non-conflicting supported `cameraControl`, only after confirming endpoint support. If all variants fail similarly, fix the shot contract before changing models.

### Example 3 — First/last-frame controlled transformation

**Intent:** show an authorized package folding from flat carton to assembled display pack without changing camera or branding.

**Route and model:** Enterprise `veo-3.1-generate-001` for stable Cloud integration; use Gemini Developer API Standard instead if native generated audio is required.

**Inputs:** start PNG of the flat carton and end PNG of the assembled pack, both 16:9, same tabletop, lens, camera height, light direction, color treatment, and approved artwork.

**Complete prompt:**

```text
Static eye-level tabletop product shot. The flat die-cut carton in the first frame folds along its real crease lines in a physically plausible sequence: side walls rise, tabs tuck inward, the top closes, and the assembled display pack settles precisely into the final-frame position. Keep the camera fixed, preserve the printed artwork, proportions, tabletop, shadows, and soft north-window lighting. One continuous transformation with no cuts, no hands, and no extra objects.
```

**Complete Enterprise REST configuration:** put `prompt`, `image`, and `lastFrame` in the instance; put generation controls in `parameters`:

```json
{
  "instances": [{
    "prompt": "Static eye-level tabletop product shot. The flat die-cut carton in the first frame folds along its real crease lines in a physically plausible sequence: side walls rise, tabs tuck inward, the top closes, and the assembled display pack settles precisely into the final-frame position. Keep the camera fixed, preserve the printed artwork, proportions, tabletop, shadows, and soft north-window lighting. One continuous transformation with no cuts, no hands, and no extra objects.",
    "image": {"gcsUri": "gs://approved-inputs/carton-flat.png", "mimeType": "image/png"},
    "lastFrame": {"gcsUri": "gs://approved-inputs/carton-assembled.png", "mimeType": "image/png"}
  }],
  "parameters": {
    "durationSeconds": 8,
    "aspectRatio": "16:9",
    "resolution": "1080p",
    "sampleCount": 2,
    "storageUri": "gs://approved-output/veo/carton-fold/",
    "negativePrompt": "hands, extra panels, duplicate package, rewritten artwork, subtitles, camera movement"
  }
}
```

**Why this structure:** endpoints carry the exact compositions while the prompt describes only the bridge. Matching capture geometry reduces morph pressure.

**Expected result:** a continuous interpolation that begins and ends on the supplied frames.

**Likely failures and recovery:** if panels melt, simplify the fold sequence or create a more compatible intermediate end pose as a separate shot. If artwork crawls, use a logo-free generation plate and composite approved artwork in post; do not rely on generated typography for legal packaging.

### Example 4 — Developer API extension with continuity

**Intent:** continue a previously generated Veo shot of an origami bird without a visual or audio reset.

**Input condition:** the prior Gemini Veo `Video` object is still retained, 720p, and its final second shows the bird gliding right while paper-wing rustle and a quiet garden bed are audible.

**Complete extension prompt:**

```text
Continue the same shot without a cut. Track right at the existing speed as the origami bird glides beneath the arch, banks gently toward camera, and lands on the stone fountain rim. Preserve its blue paper pattern, afternoon light, garden layout, motion direction, shallow depth of field, paper-wing rustle, and quiet garden ambience. End after the bird becomes still on the rim.
```

**Configuration:** pass the prior returned `Video` as `video`, use `veo-3.1-generate-preview`, `resolution="720p"`, `duration_seconds=8`, and one output.

**Why this structure:** it describes only the next beat and repeats continuity constraints that matter at the seam. The source tail already contains the sound bed.

**Expected result:** the returned file combines the original video and a seven-second continuation.

**Likely failures and recovery:** if the bird resets position, trim or regenerate the source so its last second has a clean, stable trajectory. If sound changes abruptly, use the generated extension as a picture plate and build continuous audio in post.

## Rights, consent, provenance, and safety gate

Before submitting any prompt or reference:

1. Confirm rights to all input images, video, audio, trademarks, designs, characters, footage, and likenesses.
2. Obtain legally sufficient consent for identifiable people and biometric/likeness use. Do not create deceptive impersonation or non-consensual intimate content.
3. Do not use a public figure, private person, child, or copyrighted character as a covert way to bypass a safety block. Current Cloud safety codes explicitly include child, celebrity, third-party content, sexual, violence, hate, and other categories.
4. Avoid synthetic “evidence” of real news, elections, conflicts, crimes, or product performance. Label synthetic dramatization where a reasonable viewer could be misled.
5. Keep provenance. Gemini Veo output receives SynthID; Enterprise model cards also list C2PA support. Do not strip or misrepresent provenance metadata or claim an AI-generated clip was solely human-created.
6. Run legal/brand review for packaging text, endorsements, regulated claims, editorial news use, and sensitive historical depictions. Generated text and factual demonstrations are not evidence.
7. Test representation and stereotyping across the actual deployment prompt set. Google's Veo 3 technical report reports lighter-skin-tone skew in some underspecified profession prompts and semantic bias risks; specify demographics only when relevant and authorized, and review outputs rather than assuming neutrality.

Google's [Generative AI Prohibited Use Policy](https://policies.google.com/terms/generative-ai/use-policy) forbids dangerous/illegal activity, rights violations, non-consensual biometric use, deceptive impersonation, safety circumvention, harmful sexual/violent/hateful activity, and misleading provenance. The [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms) say Google does not claim ownership of generated content, but the user remains responsible for its use and similar output may be generated for others. Unpaid Services may use prompts and outputs to improve products and may involve human review; do not send confidential or personal material there. Paid Services do not use prompts or responses for product improvement under the stated paid-service terms. Verify which terms govern the chosen route.

The same Gemini API terms require users to be at least 18 and prohibit API clients directed toward or likely to be accessed by people under 18. They also require Paid Services for API clients made available in the EEA, Switzerland, or the UK. Treat these as route-specific deployment requirements and recheck the current terms before launch.

If a generation is blocked, inspect the error/support code, document the reason, and either revise to a legitimate safe concept or stop. Never “jailbreak,” euphemize, or decompose a prohibited request to evade filters.

## Source coverage and limitations of evidence

- **Official API and model contracts:** [Gemini Veo guide](https://ai.google.dev/gemini-api/docs/veo); [Enterprise Veo 3.1 card](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate); [Cloud instance schema](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/Shared.Types/VideoGenerationModelInstance); [Cloud parameter schema](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/Shared.Types/VideoGenerationModelParams); [Cloud result schema](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/Shared.Types/VideoGenerationModelResult).
- **Prompt and production guidance:** [Gemini Veo prompt guide](https://ai.google.dev/gemini-api/docs/veo#veo-prompt-guide); [Cloud Veo prompt guide](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide); [Cloud Veo best practices](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/best-practice); [prompt rewriter behavior](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/turn-the-prompt-rewriter-off).
- **Input-mode guides:** [Cloud image-to-video](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-an-image); [reference images](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/use-reference-images-to-guide-video-generation); [extension](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/extend-a-veo-video).
- **Safety and terms:** [Cloud Responsible AI for Veo](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/responsible-ai-and-usage-guidelines); [Google prohibited-use policy](https://policies.google.com/terms/generative-ai/use-policy); [Gemini API terms](https://ai.google.dev/gemini-api/terms).
- **First-party technical research:** Google's [Veo 3 technical report](https://storage.googleapis.com/deepmind-media/veo/Veo-3-Tech-Report.pdf) documents joint latent audio/video diffusion, data curation, evaluation design, safety mitigations, text weakness, small hallucinations, cinematic bias, deepfake risk, and measured fairness limitations. These findings concern Veo 3 and risk evaluation; do not assume every result transfers quantitatively to Veo 3.1.
- **First-party benchmark claims:** the [DeepMind Veo page](https://deepmind.google/models/veo/) reports internal human-preference comparisons. Treat these as provider-reported, not independent evidence.

No third-party benchmark is used to claim that Veo is universally superior. Model choice in this skill is based on verified interface capabilities and production fit.
