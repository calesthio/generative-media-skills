---
name: remotion-video-composition
description: Provider-independent production workflow for assembling generated or sourced media into React/Remotion videos. Use when an agent must plan, build, render, review, variant-render, or hand off Remotion compositions with media custody, captions, audio, animation, accessibility, provenance, QA, and delivery requirements.
---

# Remotion video composition production

Use this skill when Remotion is the composition layer for a real video deliverable: generated-media explainers, product videos, social variants, data-driven videos, screen-demo composites, captioned talking-head recuts, or any render where React code, assets, captions, audio, and delivery metadata must become a reproducible video package.

This is a production skill, not just a coding recipe. Treat Remotion as the deterministic assembly and finishing engine around media that may have been generated elsewhere.

## Source status and volatility

Facts below are based on primary sources verified on 2026-07-11 unless noted otherwise:

- Remotion documentation for composition properties, assets, static files, media components, renderer APIs, schemas, dynamic metadata, randomness, performance, captions, and licensing: https://www.remotion.dev/docs/
- FFmpeg official documentation for stream mapping, codecs, filters, and filtergraphs: https://ffmpeg.org/ffmpeg.html and https://ffmpeg.org/ffmpeg-filters.html
- W3C/WAI WCAG guidance for captions and flashing: https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html and https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- W3C WebVTT specification for timed-text cues: https://www.w3.org/TR/webvtt1/
- C2PA specifications and Content Credentials guidance for provenance manifests: https://spec.c2pa.org/ and https://c2pa.org/

Volatile facts: Remotion package versions, API availability, licensing and pricing, cloud render limits, browser renderer status, package deprecations, social-platform delivery specs, caption file requirements, and AI/provider usage rights. Re-check those at production time and record the verification date in the project handoff.

## Production stance

Remotion is strongest when the video can be expressed as deterministic React over a timeline:

- branded motion graphics;
- generated-image or generated-clip assembly;
- chart/stat/data videos;
- captioned narration;
- batch variants;
- programmatic product or screen-demo layouts;
- precise frame-based review exports.

Do not use Remotion as a substitute for missing creative decisions. Before writing code, lock the brief, visual system, asset list, caption approach, audio plan, target aspect ratio, duration, and delivery requirements.

Escalate instead of guessing when:

- the target platform or legal usage rights determine encoding, captions, or licensing;
- the client requires C2PA signing, EIDR/ISAN/broadcast metadata, union talent constraints, music clearance, or regulated claims;
- source media may include third-party IP, likenesses, trademarks, private data, or model outputs with unclear license terms;
- automated captions or translations affect safety, legal, medical, financial, or public-facing claims;
- flashing, photosensitive risk, minors, political persuasion, synthetic likeness, or accessibility obligations are high-stakes.

## Intake contract

Collect or derive these before composition work:

1. Deliverables: final runtime, aspect ratios, resolution, frame rate, audio channels, container/codec, platform(s), language(s), and whether burned-in captions are required.
2. Audience and purpose: viewing context, brand tone, call to action, accessibility needs, review process.
3. Timeline: exact scenes or beats with start/end times in seconds and frames.
4. Media inventory: every image, video, audio stem, font, logo, subtitle file, data file, and source transcript.
5. Rights and provenance: origin, owner, license/permission, restrictions, model/provider, prompt, seed, generation date, modification chain, and whether Content Credentials are expected.
6. Quality bar: reference look, motion intensity, type density, safe areas, color/contrast constraints, loudness target if supplied, and variant rules.
7. Approval gates: what the user/client must approve before final render.

If the user provides only a vague "make a video" brief, first produce a short proposal and ask for missing decisions that materially affect the result. Do not begin asset-heavy implementation until the composition contract is coherent.

## Project architecture

Create a composition project whose code mirrors the production contract.

Recommended structure:

```text
project/
+- package.json
+- remotion.config.ts
+- public/
|  +- assets/
|  |  +- image/
|  |  +- video/
|  |  +- audio/
|  |  +- fonts/
|  |  +- captions/
|  +- provenance/
+- src/
|  +- Root.tsx
|  +- compositions/
|  +- scenes/
|  +- components/
|  +- data/
|  +- styles/
|  +- utils/
+- review/
+- renders/
+- handoff/
```

Keep creative data separate from rendering mechanics:

- `src/Root.tsx` registers compositions.
- `src/data/*.json` or typed modules define scenes, variants, captions, and asset references.
- `src/scenes/*` render individual scenes from data.
- `src/components/*` hold reusable layout primitives, not one-off scene decisions.
- `public/assets/*` contains frozen media used by `staticFile()`.
- `handoff/` contains final outputs, caption sidecars, stems, provenance ledger, and render notes.

Use stable identifiers for every asset, scene, caption track, and variant. These IDs should survive code refactors and appear in filenames, review notes, and provenance records.

## Composition registration and timing model

In Remotion, a composition is the renderable video and is registered with properties such as `durationInFrames`, `fps`, `width`, and `height`. Keep these values explicit and derived from the production contract, not scattered through components.

Use:

- `<Composition>` to register renderable videos.
- `<Sequence>` or `<Series>` to place scenes on the timeline.
- `useCurrentFrame()` for frame-relative animation.
- `useVideoConfig()` for `fps`, `durationInFrames`, `width`, and `height`.
- `calculateMetadata()` when duration, dimensions, fps, codec, or props must be computed from input data.

Frame math:

```ts
export const secondsToFrames = (seconds: number, fps: number) =>
  Math.round(seconds * fps);
```

Use the same helper everywhere. For exact broadcast rates such as 23.976 or 29.97, decide whether the project will represent timing as integer frame counts from an edit decision list rather than repeatedly converting decimal seconds.

When scenes are sequential, compute `from` values from accumulated frame durations rather than hardcoding them. Hardcoded frame offsets are acceptable only for tiny one-off compositions after review.

Example:

```tsx
import {Composition, Series} from 'remotion';
import {z} from 'zod';
import {MainVideo} from './compositions/MainVideo';
import {projectSchema, defaultProject} from './data/project';

export const RemotionRoot = () => (
  <Composition
    id="MainVideo"
    component={MainVideo}
    fps={30}
    width={1920}
    height={1080}
    durationInFrames={defaultProject.totalFrames}
    defaultProps={defaultProject}
    schema={projectSchema}
    calculateMetadata={({props}) => ({
      durationInFrames: props.scenes.reduce((sum, s) => sum + s.frames, 0),
      props,
    })}
  />
);
```

Remotion input props must be JSON-serializable when used for rendering. Use a Zod schema for variant data so a bad render fails before frames are produced.

## Aspect ratio, resolution, and safe areas

Select a canonical composition target before layout:

- landscape: commonly 16:9, for web players and presentations;
- vertical: commonly 9:16, for phone-first feeds;
- square or portrait variants only when explicitly requested.

Do not assume one master crop will work everywhere. Compose either:

- separate compositions per aspect ratio, sharing scene data; or
- a layout system that derives canvas regions from `width` and `height`.

Use safe-area constants and design to them:

```ts
export const makeSafeArea = (width: number, height: number) => ({
  x: Math.round(width * 0.07),
  y: Math.round(height * 0.07),
  w: Math.round(width * 0.86),
  h: Math.round(height * 0.86),
});
```

Keep critical text, logos, captions, and calls to action inside the safe area unless the platform-specific spec says otherwise. Platform UI overlays change; re-check current platform templates or client delivery specs at export time.

## Asset custody

Freeze inputs before coding against them.

For each asset, record:

- stable asset ID;
- local path under `public/assets`;
- source path or URL;
- SHA-256 or other checksum;
- creator/owner;
- license or permission;
- generation provider/model/version when applicable;
- prompt, seed, parameters, and generation date when applicable;
- transformations performed before import;
- usage restrictions and required attribution;
- whether the asset carries C2PA/Content Credentials and whether they survived transformations.

Use Remotion `staticFile()` for files in the project `public/` directory. This avoids fragile absolute paths and works across Studio and render environments. For embedded video, check the installed Remotion version and choose the current recommended media component for that version: current docs recommend `<Video>` from `@remotion/media` for new code, while `<OffthreadVideo>` remains useful when you specifically need its FFmpeg-backed frame extraction behavior.

Do not leave final composition dependencies in temp folders, downloads, cloud URLs, or external drives. Remote URLs are acceptable for quick exploration only; production renders should use frozen local copies unless the pipeline explicitly requires remote fetches and records their immutable version.

Preflight every media file:

- inspect dimensions, duration, frame rate, codec, alpha, color profile/HDR, and audio channels;
- check whether clips contain audio that should be muted or mixed;
- transcode or proxy problematic assets with FFmpeg when the browser or renderer struggles;
- normalize naming to IDs, not user-facing descriptions;
- verify that fonts are licensed and bundled.

## Captions and subtitles

Caption strategy is a production decision:

- sidecar captions: SRT or WebVTT delivered alongside the video;
- burned-in captions: rendered into pixels for platforms or styles where native captions are unavailable or undesired;
- both: common for social and accessibility handoff.

For prerecorded synchronized media with meaningful audio, WCAG 1.2.2 expects captions that represent spoken content and meaningful non-speech information. Do not provide dialogue-only subtitles when sound effects, speaker identity, or music cues are needed to understand the video.

Recommended workflow:

1. Create or import a transcript.
2. Time-align at cue or word level.
3. Human-review names, terminology, numbers, claims, and translations.
4. Convert to a normalized caption shape used by the composition.
5. Render burned-in captions only after checking safe area, contrast, reading speed, and overlap with lower-thirds.
6. Export sidecar SRT/VTT if the platform or client can use native captions.

Remotion provides caption utilities through `@remotion/captions`; re-check the installed package and API version before relying on helpers such as SRT parsing or TikTok-style segmentation.

Caption design rules:

- keep captions inside title-safe/action-safe areas unless platform overlays require a different placement;
- avoid covering mouths, products, UI controls, or critical chart labels;
- use high contrast and enough background separation for varied footage;
- avoid rapid word-by-word karaoke unless it is intentional and readable;
- include non-speech cues when meaningful, for example `[door closes]` or `[music swells]`;
- for multilingual output, treat line breaks and text expansion as design problems, not an afterthought.

## Audio mixing and stems

Plan audio as stems:

- narration/dialogue;
- music;
- sound effects;
- source clip audio;
- optional accessibility or audio-description track.

In Remotion, align audio using the same frame timeline as visuals. Use `<Sequence>` to delay stems and use the media component `volume` prop for static or frame-varying levels. Multiple audio tags can be mixed, but still review the final render with audio tools; visual preview is not enough.

Production heuristics:

- narration must remain intelligible over music and effects;
- fade music under speech and restore it in gaps;
- avoid clipping on the summed mix;
- keep ambience continuous across scene cuts unless a hard audio cut is intentional;
- preserve separate stems in handoff when the client may need localization, revisions, or compliance review.

If using FFmpeg for post-mix or loudness checks, use official filter documentation for `loudnorm`, `amix`, `atrim`, `afade`, and related filters. Do not hardcode a universal LUFS target; platform, broadcast, podcast, and client specs differ. If the spec is unknown, flag the chosen target as a production assumption.

## Animation and transitions

Keep animation deterministic and frame-based:

- use `useCurrentFrame()` and `useVideoConfig()`;
- use `spring()` for physically plausible reveals;
- use `interpolate()` and `interpolateColors()` for value mapping;
- use Remotion `random(seed)` for deterministic variation;
- avoid `Math.random()`, `Date.now()`, unstable network fetches during render, and layout that depends on browser timing.

Design motion from the message:

- reveal information in the order the viewer needs it;
- use transitions to clarify structure, not to decorate every cut;
- reserve heavy motion for moments of emphasis;
- match motion intensity to the brand and audience;
- avoid motion that makes small text unreadable.

For scene transitions, first decide whether the cut is conceptual, spatial, rhythmic, or purely editorial. Then choose a transition family:

- straight cut: fastest and often best for dense information;
- fade/dissolve: soft topic shift or time passage;
- slide/wipe: spatial or UI-like movement;
- scale/zoom: hierarchy shift or reveal;
- match cut: preserves shape/color/motion across scenes;
- audio-led transition: music or SFX motivates the visual cut.

If using `@remotion/transitions` or any transition package, verify the current API and version at production time.

## Text, layout, and visual system

Treat text as designed media:

- use a type scale, not arbitrary font sizes;
- constrain line length;
- define styles for title, section label, caption, annotation, stat, source note, and CTA;
- keep key text in safe areas;
- localize with expansion in mind;
- include source notes for factual claims where required.

Use layout primitives that respond to composition dimensions:

- `Frame`: establishes background and safe area;
- `Grid` or `Stack`: controls spacing;
- `CaptionLayer`: reserves caption position;
- `BrandBug`: controls logo placement;
- `SceneChrome`: optional scene label, source note, or progress indicator;
- `MediaSlot`: covers fit/crop decisions for images or video.

Do not rely on CSS responsive behavior alone. Render review stills at multiple frames and aspect ratios to catch clipped text, invisible overlays, and captions competing with UI.

## Data-driven variants

Remotion is well-suited to batch variants if the creative system is explicit.

Use variants when changing:

- copy, language, voice, captions;
- product screenshots or generated images;
- stats, names, offers, dates;
- aspect ratio;
- logo/brand theme;
- CTA or localization.

Variant rules:

- keep all render inputs in JSON-serializable props;
- validate props with schema before rendering;
- derive duration from data when scene counts or caption lengths vary;
- use stable asset IDs and variant IDs;
- produce a render manifest mapping each output to props, assets, captions, and provenance ledger entries;
- render deterministic stills before batch video renders.

Do not batch-render many variants until one representative variant has passed visual, caption, audio, and accessibility review.

## Rendering and export

Use the render path that matches the environment:

- CLI render for local operator workflows;
- `@remotion/renderer` `renderMedia()` for programmatic Node/Bun rendering;
- cloud/server rendering only after checking Remotion's current SSR/cloud docs, licensing, and infrastructure limits.

Choose output settings from the delivery spec:

- container and codec;
- resolution and frame rate;
- audio codec/sample rate/channels;
- CRF or bitrate constraints;
- alpha requirements;
- thumbnail/still requirements;
- subtitle sidecar format;
- filename convention and version.

Remotion `renderMedia()` and CLI render expose codec and output-location choices. Remotion's quality guidance identifies CRF as a main quality control for supported codecs, while FFmpeg documentation governs underlying codec and filter behavior. Lower compression usually increases quality and file size; always verify visually after export.

Use deterministic review exports before final:

- contact sheet of key frames: first frame, every scene start, every caption style, every CTA, every transition midpoint;
- low-resolution watermarked preview for review when file size matters;
- full-resolution short segment around the highest-motion section;
- final full render only after critical issues are cleared.

If a render fails, classify the failure:

- code/build error;
- missing asset or wrong path;
- media decode/transcode issue;
- memory/concurrency issue;
- font/rendering mismatch;
- audio mix issue;
- platform/codec incompatibility.

Then fix the class of problem rather than blindly retrying.

## Performance and reliability

Before a serious render:

- pin package versions or record the installed versions;
- run typecheck/lint/build if available;
- confirm all assets exist under `public/`;
- confirm no render-time fetch depends on a mutable external service;
- reduce huge input props; store large data or media as files;
- use still-frame renders to debug layout before full video;
- choose concurrency based on hardware and memory;
- test one representative segment before long renders.

Avoid:

- per-frame network calls;
- decoding oversized images when a smaller production asset would do;
- unnecessary DOM depth and heavy CSS effects;
- animated blur/shadow/filter effects on many elements unless tested;
- unbounded image/video elements;
- large base64 blobs in props;
- nondeterministic timers or random values.

If using `calculateMetadata()` for data fetching, follow current Remotion guidance and avoid repeated rate-limited calls in highly concurrent renders. Cache or freeze fetched data into project files when practical.

## Accessibility and safety checks

Run these checks before delivery:

- Captions: prerecorded meaningful audio has captions; captions include meaningful non-speech audio and speaker context when needed.
- Reading: caption and title text can be read at playback speed on the target device.
- Contrast: text and UI overlays remain legible over every background.
- Flashing: avoid content that flashes more than three times in any one-second period unless it is below WCAG general/red flash thresholds. When uncertain, reduce flashes, lower contrast, slow the sequence, or remove the effect.
- Motion sensitivity: avoid unnecessary shake, rapid zooms, or strobing backgrounds; provide a calmer version if requested.
- Audio: no clipping, painful peaks, or sudden loud transitions.
- Audio description or alternative: if important visual information is not conveyed by the main audio, escalate for an audio-description or text-alternative decision, especially for accessibility-regulated deliverables.

Automated checks do not replace human review for captions, flashing risk, or comprehension.

## Provenance, licensing, and Content Credentials

Maintain a provenance ledger even if the final file is not C2PA-signed.

Minimum ledger fields:

```json
{
  "project_id": "example-video",
  "verified_on": "2026-07-11",
  "outputs": [
    {
      "id": "main-16x9-v03",
      "path": "handoff/main-16x9-v03.mp4",
      "sha256": "..."
    }
  ],
  "assets": [
    {
      "id": "hero-image-01",
      "local_path": "public/assets/image/hero-image-01.png",
      "source": "generated",
      "provider": "example-provider",
      "model": "example-model",
      "prompt_or_brief": "stored in secure project notes",
      "seed": "12345",
      "license_or_permission": "client approved for this campaign",
      "restrictions": "no standalone resale",
      "sha256": "..."
    }
  ],
  "software": {
    "remotion": "record installed version",
    "ffmpeg": "record installed version"
  },
  "human_approvals": [
    {
      "scope": "final render",
      "approver": "client/contact",
      "date": "YYYY-MM-DD"
    }
  ]
}
```

C2PA Content Credentials are a technical provenance standard built around manifests, assertions, claims, signatures, and ingredients. If the client requires C2PA, use a current C2PA-compatible toolchain and verify that credentials survive the export and platform upload path. If platforms strip metadata, preserve the signed source/output plus a separate ledger in handoff. Do not imply that C2PA proves truthfulness; it records provenance claims whose trust depends on the signer and chain.

Escalate to client, counsel, or platform owner when:

- license terms are unclear or conflict with intended use;
- generated likeness, voice, logo, music, or trademark rights are involved;
- attribution is required but the platform layout cannot support it;
- an AI provider's output terms or safety policies affect publication;
- synthetic or edited media must be labeled;
- regulated claims appear in captions, narration, visuals, or metadata.

## QA checklist

Run this before final handoff:

1. Composition contract: duration, fps, dimensions, aspect ratio, and variant list match the brief.
2. Timeline: scene boundaries, transitions, caption timing, and audio cues are frame-accurate.
3. Media custody: every referenced file exists locally, is checksummed, and has provenance.
4. Visual review: key-frame contact sheet passes for layout, safe area, crop, brand, text, and CTA.
5. Motion review: transitions support meaning; no accidental jitter, stutter, or over-animation.
6. Caption review: transcript accuracy, punctuation, speaker cues, non-speech cues, line breaks, and translations pass.
7. Audio review: intelligibility, mix, fades, sync, clipping, and loudness assumption pass.
8. Accessibility review: captions, contrast, flashing, motion sensitivity, and audio-description decision pass or are escalated.
9. Determinism: rerendered review stills match expectation; no random/network/time dependency is present.
10. Encoding review: final file opens in target players; codec/container/audio settings match delivery requirements.
11. Provenance review: ledger, licenses, approvals, versions, prompts/seeds, and source notes are complete.
12. Handoff review: final files, sidecars, stems, source package, render notes, and residual risks are included.

## Delivery handoff

Deliver:

- final video file(s);
- caption sidecars, if any;
- burned-in caption status;
- thumbnail/still exports;
- audio stems or final mix, as agreed;
- source Remotion project or archived source bundle;
- exact render command or script entry point;
- package lockfile and software version notes;
- provenance/licensing ledger;
- QA report with known limitations and volatile facts rechecked;
- client approval record or list of decisions still pending.

The handoff should let another agent or engineer reproduce the render without guessing which assets, props, or settings were used.

## Example: generated-media explainer assembled in Remotion

User request: "Make a 60-second vertical explainer from generated images, narration, music, captions, and a CTA."

Strong approach:

1. Confirm `1080x1920`, `30 fps`, `60 seconds`, language, caption style, brand colors, and music source.
2. Freeze generated images under `public/assets/image/` and narration/music under `public/assets/audio/`.
3. Create a `project.json` with five scenes, each with duration, image asset ID, narration segment, headline, caption cue range, and transition style.
4. Register `VerticalExplainer` with `width={1080}`, `height={1920}`, `fps={30}`, and `durationInFrames` derived from scenes.
5. Use `<Series>` for scene order and `<Sequence>` for overlays, audio cues, and caption layers.
6. Use the current recommended Remotion video component for generated clips, falling back to `OffthreadVideo` when its FFmpeg-backed extraction is the better fit; otherwise use `Img` for stills with deterministic camera moves.
7. Render a contact sheet: scene starts, headline reveals, caption-heavy frames, transition midpoints, final CTA.
8. Review captions and flashing before the full render.
9. Export MP4 plus SRT/VTT, provenance ledger, and source bundle.

Example scene data:

```json
{
  "id": "scene-03-proof",
  "frames": 360,
  "image": "workflow-diagram-01",
  "narration": "vo-03-proof",
  "headline": "The hidden cost is handoff friction",
  "captionCueIds": ["c011", "c012", "c013"],
  "motion": {"type": "slow-push", "intensity": 0.18},
  "transitionOut": "match-cut-line"
}
```

Example implementation sketch:

```tsx
const Scene = ({scene}: {scene: SceneData}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const safe = makeSafeArea(width, height);
  const reveal = spring({frame, fps, config: {damping: 18}});

  return (
    <AbsoluteFill style={{backgroundColor: '#080A12'}}>
      <KenBurnsImage assetId={scene.image} motion={scene.motion} />
      <Headline text={scene.headline} progress={reveal} safe={safe} />
      <CaptionLayer cueIds={scene.captionCueIds} safe={safe} />
    </AbsoluteFill>
  );
};
```

Why this works: Remotion controls the deterministic timeline, while generated media remains frozen and traceable. The agent can revise copy, captions, timing, or layouts without regenerating all assets.

Likely failures to watch: captions too low for platform UI, images too low-resolution for vertical crop, music masking narration, text expansion in translated variants, and unrecorded AI generation settings.

## Example: data-driven variant campaign

User request: "Create 40 short product-update videos, one per customer segment, using the same structure but different metrics, screenshots, and CTA."

Strong approach:

1. Build one representative variant first.
2. Define `VariantProps` with schema validation.
3. Store variant data in JSON and all assets under stable IDs.
4. Use `calculateMetadata()` to extend duration for variants with longer localized copy.
5. Render still frames for each variant's first frame, metric reveal, and CTA before batch video.
6. Produce a render manifest mapping each output to input props and ledger entries.

Example variant prop shape:

```ts
const variantSchema = z.object({
  variantId: z.string(),
  locale: z.string(),
  segmentName: z.string(),
  metrics: z.array(z.object({
    label: z.string(),
    value: z.string(),
    sourceNote: z.string().optional(),
  })),
  screenshotAssetId: z.string(),
  cta: z.string(),
  captionTrack: z.string(),
});
```

Batch rule: if any variant fails schema, asset existence, caption timing, or safe-area still review, stop the batch and fix the data or layout. Do not render 40 flawed videos faster.
