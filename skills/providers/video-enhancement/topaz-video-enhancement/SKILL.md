---
name: topaz-video-enhancement
description: >-
  Use when enhancing, upscaling, restoring, denoising, sharpening, deinterlacing,
  stabilizing, motion-deblurring, colorizing, SDR-to-HDR converting, or
  frame-rate/slow-motion converting video (and secondarily images) with Topaz Labs
  — whether cleaning up AI-generated video, compressed UGC, or old archival footage,
  or building a generate-low-res-then-upscale delivery pipeline. Covers choosing the
  right named Topaz model for a specific footage problem, setting parameters, driving
  the Topaz Platform (Video/Image) REST API's async job lifecycle, judging when
  enhancement helps versus when it introduces artifacts (over-smoothing, temporal
  shimmer, face hallucination), and QA of enhanced output. Do not use for
  originating new video content, non-Topaz upscalers, or purely editorial cuts.
---

# Topaz Labs video (and image) enhancement

Topaz Labs makes AI enhancement/restoration models delivered three ways: the
**desktop apps** (Topaz Video AI, Gigapixel, Photo AI), and the **Topaz Platform
REST API** (`api.topazlabs.com`) which exposes the same model families for
programmatic, batch, and pipeline use. This skill is about applying the *models* to
solve concrete footage problems and about driving the *API* inside an automated
pipeline. When a task is a one-off manual cleanup, the desktop app is usually faster;
when enhancement is a repeatable stage in a generate → enhance → deliver pipeline,
use the API.

Enhancement is a **repair and finishing** operation, not a creation operation. It
cannot add information that was never plausibly there; it can only reconstruct,
interpolate, or invent detail. Every model on this page trades some fidelity for some
apparent quality, and the whole discipline is choosing the trade that matches the
footage and the deliverable.

> Verification note: model names, model **codes/slugs**, parameters, limits, and
> pricing below were verified against Topaz's developer documentation on
> **2026-07-10**. These are volatile — Topaz ships new model versions frequently
> (the `-N` suffix in a code is a version). Before hard-coding a code in a pipeline,
> confirm it against the live `Available Models` reference / OpenAPI schema
> (`developer.topazlabs.com/reference`). Codes are used in API `filters[].model`;
> the desktop app shows friendly names.

## When this skill applies (and when it does not)

Applies:
- Upscaling video to a higher resolution (SD→HD, HD→4K/8K).
- Cleaning AI-generated video that came out soft, low-res, flickery, or plastic.
- Restoring old/archival footage: film grain, compression, interlacing, low res.
- Denoising, sharpening, deblurring, deinterlacing, stabilizing.
- Frame-rate conversion and slow-motion (frame interpolation).
- SDR→HDR conversion, black-and-white colorization, foreground object removal.
- Enhancing stills (Gigapixel/Photo models via the Image API) as a secondary need.
- Designing the *enhancement stage* of a "generate low-res, then upscale" pipeline.

Does not apply:
- Generating original video or images (that is a generation model's job — Topaz
  enhances an existing frame sequence; even its "creative" models start from footage).
- Non-Topaz upscalers/tools (Real-ESRGAN, Video2X, cloud VSR from other vendors).
- Editorial decisions (what to cut, pacing, story) — enhancement is orthogonal.
- Any task where the source is already at or above delivery quality; enhancement
  there only adds cost, processing time, and artifact risk.

## Where enhancement fits an AI-generated-video pipeline

*(Production heuristic, corroborated by practitioner reports cited in Sources.)*

Most current text/image-to-video generators are cheaper and more controllable at low
resolution and short duration. A common delivery pattern:

1. **Generate low-res** (e.g. 480–720p) for iteration speed and cost. Lock the edit,
   motion, and composition here.
2. **Enhance/upscale as a finishing pass** to the delivery resolution (1080p/4K),
   choosing a model by *what the footage needs*, not by "biggest number."
3. **QA the motion**, not just a frame. Generated video's failure mode is temporal:
   shimmer, warping, identity drift. A still frame can look perfect while the clip
   is unusable.

Why enhance last, not during generation: enhancement models are deterministic given
inputs and let you separate concerns (denoise, then upscale, then interpolate) so
each model solves one problem. Upscaling noisy or warpy footage *amplifies* the noise
and warping — fix those first.

Key mindset difference from camera footage: AI-generated frames contain **synthetic
texture** the generator invented. A restoration model tuned for real footage may read
that texture as detail to preserve, or a creative model may *replace* it. Match the
model's assumptions to the source (see model selection below).

## Model families and how to choose

Topaz groups video models into families. Pick the **family** by the dominant problem,
then the **variant** by quality/speed and source condition. Codes verified 2026-07-10.

### Proteus family — upscale + enhance (the workhorse)
Deterministic (non-diffusion) upscaling and detail/noise/sharpen control. Best when
you want the output to stay faithful to the source and be reproducible.

| Model | Code(s) | Solves | Notes |
|---|---|---|---|
| Proteus | `prob-4` | General upscale/enhance of low-to-mid quality real footage | Most versatile default; exposes manual detail/noise/sharpen params |
| Iris | `iris-3` (LQ), `iris-2` (MQ) | Face/detail recovery from degraded sources | Choose LQ vs MQ by source quality; strongest on faces |
| Artemis | `ahq-12`, `amq-13`, `alq-13`, `amqs-2`, `alqs-2`, `aaa-9` | Combined denoise + sharpen, compression/halo cleanup | Variant suffixes target high/medium/low quality (HQ/MQ/LQ) sources |
| Dione | `ddv-3`, `dtv-4`, `dtd-4`, `dtvs-2`, `dtds-2` | **Deinterlacing** 480i/576i/1080i broadcast (TV) and camcorder (DV) | Purpose-built for interlaced → progressive; TV vs DV variants |
| Gaia | `gcg-5` (CG), `ghq-5` (HQ) | Clean CGI / animation / rendered content | Final polish for already-clean synthetic sources |
| Rhea | `rhea-1` | 4× upscale prioritizing fine/organic texture and fidelity | Use when a large jump must preserve delicate detail |
| Theia | `thd-3` (Detail), `thf-4` (Fidelity) | Clarity/detail sharpening with noise control | Detail vs Fidelity trade sharpening aggressiveness |

Note: any Proteus-family model can be told the source is interlaced via `video_type`,
but **Dione** is the model actually designed to deinterlace well.

### Starlight family — diffusion-based restoration
Generative (diffusion) restoration. Recovers detail, stability, and texture that a
deterministic model cannot, at higher cost and with more risk of invented detail.
Reported (2026) as a temporal-stability leader.

| Model | Code | Primary use | Max frames* |
|---|---|---|---|
| Starlight Precise 1 | `sl-1` | Archival / heavily degraded real footage, max source fidelity | 9,000 |
| Starlight Precise 2 | `slp-2` | GenAI faces/skin + stable motion; has `creativity` (low/middle/high) | 450 |
| Starlight Precise 2.5 | `slp-2.5` | AI-generated video plus some archival; improved realism | 9,000 |
| Starlight HQ | `slhq-1` | Progressive video up to 4K | — |
| Starlight Mini | `slm-1` | Degraded archival (8mm/16mm/MiniDV); auto-deinterlaces | — |
| Starlight Sharp | `wonder-1` | Restoration + detail sharpening | — |
| Starlight Fast 1 / Fast 2 | `slf-1`, `slf-2` | Speed-priority; Fast 2 balances speed + realism | 9,000 |

*Max frames per request — verified 2026-07-10; enforce by segmenting long clips.

### Astra — creative diffusion upscaling
`ast-2` (Astra 2). A **creative** model for GenAI video that *adds new dynamic detail
and texture*, best on stylized/wide/large-scale AI shots. Parameters include
`creativity` (0.0–1.0, required), optional `prompt`, `sharp` (default 0.5),
`realism`, and `input_frame_count` (max 9000 without prompt, 450 with). **Warning
(documented):** creative models can change objects, identity, and stylization. Do not
use Astra when the output must match the source exactly — use Proteus (preserve) or
Starlight (restore with intent preserved).

### Nyx — dedicated denoise
| Model | Code | Use |
|---|---|---|
| Nyx | `nyx-3` | Balanced high-quality denoise; camera/low-light/compression noise while keeping detail |
| Nyx XL | `nxl-1` | Aggressive denoise when noise removal dominates |
| Nyx Fast | `nxf-1` | Faster, cheaper — previews, batch, time-sensitive |
| Nyx High Fidelity | `nxhf-1` | Denoise-only, preserves source exactly; can export a noise pass |

### Frame interpolation — frame-rate and slow-motion (does NOT upscale)
| Model | Code | Use |
|---|---|---|
| Apollo | `apo-8` | Best all-around slow-motion + frame-rate conversion; precise 2×/4×/8× |
| Apollo Fast | `apf-2` | Simpler motion, faster |
| Chronos | `chr-2` | Hard frame-rate conversions, linear/layered motion |
| Chronos Fast | `chf-3` | Speed over precision |
| Aion | `aion-1` | Extreme slow motion with heavy parallax / fast camera; minimizes duplication/instability |

Shared params: `slowmo` (1–16), `fps` (15–240), `duplicate` (bool),
`duplicateThreshold`/`duplicate_threshold` (0.001–0.1). **These models do not
upscale** — run interpolation and upscaling as separate stages.

### Video utilities
| Task | Model | Code | Notes |
|---|---|---|---|
| Motion deblur | Themis 2 | `thm-2` | Fast camera shake / fast subjects; recovers clarity without harsh edges |
| Colorization | Video Colorization | `color-1` | B&W → color, temporally consistent (no per-frame flicker); no params |
| SDR→HDR | Hyperion / Hyperion 2 | `hyp-1`, `hyp-2` | `transfer_function` "pq"/"hlg"; exposure/saturation/highlight controls; Hyperion 2 supports ProRes PQ / EXR ACES |
| Foreground removal | Foreground Object Removal | `remove-1` | Needs source video + tracked matte/mask video; reconstructs background |
| Stabilization | (desktop feature) | — | Available in Topaz Video AI desktop; confirm current API exposure before scripting |

### Selection quick-reference by footage problem
- **Low-res AI-generated video** → Starlight Precise 2.5 (`slp-2.5`) for faithful
  realism; Astra 2 (`ast-2`) when you *want* new stylized detail on wide shots. Fix
  temporal warping first; upscaling amplifies it.
- **Compressed UGC (phone/social)** → Proteus (`prob-4`) default; Artemis for
  denoise+sharpen on visible compression/halos; Iris if faces are the priority.
- **Old archival / film** → Starlight Precise 1 (`sl-1`) or Mini (`slm-1`, auto-
  deinterlaces small formats); Iris LQ/MQ for a lighter deterministic pass.
- **Interlaced broadcast/camcorder** → Dione (TV `dtv-4` / DV `ddv-3` variants), or
  Starlight Mini for degraded interlaced.
- **Slow motion / frame-rate change** → Apollo (`apo-8`) default; Aion (`aion-1`)
  for extreme slow-mo with big parallax; Chronos for tough fps conversions.
- **Just noisy** → Nyx (`nyx-3`); Nyx XL for severe noise; Nyx HF to preserve source.
- **Motion blur** → Themis 2 (`thm-2`). **B&W** → `color-1`. **SDR→HDR** → Hyperion.

## Parameters

Deterministic enhancement models (Proteus, Artemis, Dione, Theia, Nyx, Themis) share
a common tuning surface (verified 2026-07-10; ranges are decimals):

- `video_type`: `"Progressive"` | `"Interlaced"` | `"ProgressiveInterlaced"`
- `field_order`: `"TopFirst"` | `"BottomFirst"` | `"Auto"` (interlaced sources)
- `auto`: `"Auto"` | `"Manual"` | `"Relative"` (whether the model self-tunes)
- `focus_fix_level`: `"None"` | `"Normal"` | `"Strong"`
- `compression`, `details`, `noise`, `halo`, `blur`, `preblur`: `-1 … 1`
- `prenoise`, `grain`: `0 … 0.1`
- `grain_sigma`: `0 … 1`; `grain_size`: `0 … 5`
- `grain_type`: `"silver_rich"` | `"gaussian"` | `"grey"`
- `recover_original_detail_value`: `0 … 1` (Nyx)

Heuristics: start with `auto` and only go manual to fix a specific defect. Raise
`details`/`sharpen` cautiously — over-sharpening is the fast road to waxy faces and
shimmer. Add a little **grain** back after heavy denoise to avoid a plastic look.
Diffusion models (Starlight/Astra) expose `creativity`/`realism` instead: higher
creativity = more invented detail = more identity/artifact risk.

## Driving the API

The Video API is an **async, multi-step job**, not a single call. Auth on every
request: header `X-API-Key: <key>`. HTTPS only. Per-request source limit **500 MB**
(verified 2026-07-10) — segment longer/larger sources. Expect HTTP 429 under load;
use exponential backoff.

Lifecycle (base `https://api.topazlabs.com/video/`):
1. **Create** — `POST /video/` with `source`, `output`, and `filters` objects.
   Returns a `requestID`. *Free — creating a request costs no credits* (credits are
   charged when the job actually processes).
2. **Accept** — `PATCH /video/{requestID}/accept` → returns S3 upload URL(s).
3. **Upload** — `PUT` the file to each S3 URL with `Content-Type: video/mp4`; keep
   each returned `eTag`.
4. **Complete upload** — `PATCH /video/{requestID}/complete-upload` with the
   `uploadResults` array of `{partNum, eTag}` to start processing.
5. **Poll** — `GET /video/{requestID}/status` until completed; response carries the
   download link. Also available: `create-express-request`, `cancel-request`,
   `delete-files`, `get-request-metrics`, `get-request-history`; account credits at
   `/account/credits`.

Formats: MP4 container in the documented examples; audio commonly `AAC` with
`audioTransfer: "Copy"` to pass audio through unchanged. `output.frameRate` and
`output.resolution` define the target; frame-interpolation `fps`/`slowmo` live in the
filter. Confirm current container/codec support in the reference before committing a
pipeline to a non-MP4 source.

### Image API (secondary scope)
Separate, simpler async flow for stills: `POST /enhance/async` (plus
`sharpen`/`denoise`/`restore`/`lighting`/`matting`/`tool`), `GET /status/{id}`,
`GET /download/{id}`. Params include `model` (e.g. Gigapixel `Standard`/`High
Fidelity`/`Low Resolution`/`Art & CGI`/`Recover Faces`, plus Wonder/Bloom/Redefine),
`output_format`, and the `image` upload. Image credit rule (verified 2026-07-10):
**~1 credit per 24 MP of output**, scaling up for larger outputs. Use the Image API
to upscale key frames, posters, or thumbnails from a video pipeline.

## Pricing (volatile — verified 2026-07-10)

Billing is credit-based. Per-credit USD from the API product page:
**$0.12** (Starter/pay-as-you-go), **$0.10** (Developer), **$0.08** (Scale). The
product page listed plans (Developer $50/500 credits/mo, Scale $240/3,000
credits/mo, Enterprise custom) while the developer docs emphasize pay-as-you-go with
no expiration — treat the plan structure as changeable and re-verify before quoting.

Approximate video credit cost for a **10 s 1080p** clip (scales with duration and
resolution; 4K is roughly 3× the 1080p figure):
- Proteus / Denoise: ~2 credits (1080p), ~6 (4K)
- Frame interpolation: Fast ~1, Quality ~2
- Starlight: Fast ~5–6, Quality ~11–12 (1080p); ~12–25 (4K)
- Astra: ~39 (1080p), ~70 (4K) — the most expensive family

Cost implication: **enhance last and only what you ship.** Diffusion/creative models
(Starlight, Astra) cost 3–20× a Proteus pass, so reserve them for footage that
deterministic upscaling genuinely cannot fix, and prototype settings on a short clip.

## When enhancement helps vs. hurts (artifacts)

Enhancement helps when the source has recoverable structure the model was trained for:
real footage that is soft/noisy/compressed/low-res/interlaced, or AI footage that is
merely low-res but temporally stable. It hurts — or is wasted — when:

- **Over-smoothing / plastic / waxy faces:** aggressive denoise or sharpen strips
  micro-texture. Faces go uncanny. Mitigate: lighter settings, add grain back, prefer
  a face-aware model (Iris / Starlight) over brute sharpening.
- **Temporal shimmer / flicker:** per-frame enhancement invents high-frequency detail
  that shifts frame to frame. Fine textures (hair, foliage, fabric) crawl. Mitigate:
  prefer temporally-aware models (Starlight, Nyx v3); never judge from a single frame.
- **Face hallucination / identity drift:** diffusion/creative models can *invent* a
  face or change identity, especially at high `creativity`. Mitigate: lower
  creativity, use Precise/Proteus for preservation, and check identity across the
  whole clip, not one frame.
- **Amplified warping:** upscaling AI footage that already warps makes warping worse.
  Fix motion first (or regenerate); do not "upscale away" a bad generation.
- **Over-interpolation:** interpolating duplicate/near-static frames or across cuts
  produces morphing. Set `duplicate`/`duplicateThreshold` and split on scene cuts.

## QA criteria for enhanced output

*(Production heuristic + practitioner reports.)*
1. **Prototype before committing.** Render 5–10 s of the *most demanding* scene
   (fast motion, faces, fine texture) before processing the full job — the cheapest
   way to avoid a "face disaster" and wasted credits/hours.
2. **Judge in motion at full speed**, not by screenshots. Watch fine textures for
   shimmer/crawl and moving subjects for warping.
3. **Check faces and identity** across the clip. Reject waxy skin, morphing features,
   or drift.
4. **Prefer modest jumps.** 2× per pass upscales more cleanly than a single 4×; chain
   passes if you need more.
5. **Separate concerns.** Denoise → upscale → interpolate as distinct stages so each
   model solves one problem; this reduces warping vs. one aggressive combined pass.
6. **Confirm no new detail was invented** when fidelity matters (evidence, archival,
   brand assets). Creative models are disqualifying there.
7. **Verify deliverable specs:** resolution, frame rate, audio passthrough, container,
   HDR transfer function if applicable.

## Rights, consent, and provenance

Enhancement can make a person look like they were filmed at higher fidelity than they
were, and creative/diffusion models can *invent* facial detail — so enhanced footage
of real people can misrepresent them. Only enhance footage you have the right to
process. For archival/third-party footage, confirm licensing before upload (frames
leave your machine to Topaz's cloud in the API path). For anything evidentiary,
journalistic, or identity-sensitive, avoid models that add invented detail and
disclose that AI enhancement was applied. Follow Topaz's terms and your jurisdiction's
rules on synthetic-media disclosure.

## Complete examples (illustrative — verify codes/params against the live reference)

### Example A — Upscale a low-res AI clip to 1080p, faithfully
- **Intent:** A 720p, temporally-stable text-to-video clip needs to ship at 1080p
  without inventing new content.
- **Model:** Starlight Precise 2.5 (`slp-2.5`) for AI-source realism; or Proteus
  (`prob-4`) if budget-sensitive and the source is clean.
- **Why:** Precise 2.5 targets AI-generated video and preserves creative intent; a
  deterministic Proteus pass is far cheaper if artifacts are mild.
- **Flow:** create → accept → PUT to S3 → complete-upload → poll status → download.
- **Create body (Proteus variant):**
  ```json
  {
    "source":  { "resolution": {"width":1280,"height":720}, "container":"mp4",
                 "size": 18450000, "duration": 8, "frameRate": 24, "frameCount": 192 },
    "output":  { "resolution": {"width":1920,"height":1080}, "container":"mp4",
                 "audioCodec":"AAC", "audioTransfer":"Copy", "frameRate": 24,
                 "dynamicCompressionLevel":"High" },
    "filters": [ { "model":"prob-4", "details":0.2, "noise":0.0, "sharpen":0.1 } ]
  }
  ```
- **Expected:** clean 1080p, source-faithful. **Failure modes:** shimmer on foliage/
  hair (switch to Starlight); waxy faces (lower details/sharpen, use Iris/Starlight).
- **Variation:** if the clip *warps*, regenerate or stabilize first — do not upscale.

### Example B — 24→60 fps slow motion, no upscale
- **Intent:** Turn 24 fps action into smooth 2.5× slow motion at 60 fps.
- **Model:** Apollo (`apo-8`); switch to Aion (`aion-1`) if heavy parallax/fast pan.
- **Filter:** `{ "model":"apo-8", "fps":60, "slowmo":1, "duplicate":true,
  "duplicateThreshold":0.1 }` (raise `slowmo` toward 2–2.5 for time-stretch).
- **Why:** Apollo is the all-around interpolation default; `duplicate` handling avoids
  morphing across repeated frames. **Do not** expect any resolution change here.
- **Failure modes:** morphing across scene cuts (split clip on cuts first);
  ghosting on transparent/reflective motion (try Aion).

### Example C — Restore interlaced archival broadcast
- **Intent:** 1080i broadcast capture → clean 1080p progressive.
- **Model:** Dione TV (`dtv-4`) to deinterlace + enhance; or Starlight Mini (`slm-1`)
  if the source is degraded small-format film that also needs restoration.
- **Params:** `video_type:"Interlaced"`, `field_order:"Auto"` (set explicitly if you
  know top/bottom-first).
- **QA:** check for combing artifacts on horizontal motion; verify no residual
  interlace lines after processing.

### Example D — Denoise a noisy low-light phone clip, keep grain character
- **Intent:** Compressed low-light UGC, heavy luma noise, must not look plastic.
- **Model:** Nyx (`nyx-3`); Nyx XL (`nxl-1`) only if noise dominates.
- **Params:** start `auto:"Auto"`; if plastic, set `grain:0.03`,
  `grain_type:"gaussian"` to re-add texture; keep `details` low.
- **Then:** a separate Proteus (`prob-4`) upscale pass if resolution must increase —
  never denoise and 4×-upscale in one aggressive step.

## Sources (verified 2026-07-10)

Primary (official Topaz Labs):
- Developer docs — Introduction / Video API quickstart / API walkthrough /
  Available Models / model-selection: https://developer.topazlabs.com/
- Video model family pages (codes, params): Proteus, Starlight, Astra, Denoise,
  Frame Interpolation, Video Utilities under
  https://developer.topazlabs.com/video-models/
- API reference / OpenAPI schema: https://developer.topazlabs.com/reference
- Pricing pages: https://developer.topazlabs.com/getting-started/tier-pricing and
  /individual-model-pricing
- API product page (USD per-credit rates, plans): https://www.topazlabs.com/api
- Product pages: https://www.topazlabs.com/topaz-video and /video-creators
- Desktop docs: https://docs.topazlabs.com/

Secondary (independent practitioner reports, disclosed-method, for artifact/QA
heuristics only — not sole basis for technical claims):
- inference.sh blog on Topaz upscaling; morphed.app "AI Video Upscaler 2026 guide";
  vegavid.com troubleshooting AI video artifacts; mindstudio.ai Astra scene-detection.
  (These corroborate temporal-shimmer, over-smoothing, and multi-pass heuristics.)
