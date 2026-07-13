---
name: lottie-animation-delivery
description: Production guidance for assessing, exporting, packaging, integrating, capturing, validating, and handing off Lottie vector animations. Use for Bodymovin/Lottie JSON, dotLottie archives, renderer and player compatibility, fonts and glyphs, image assets, markers and segments, deterministic video capture, responsive sizing, optimization, accessibility, and cross-platform QA; not for general After Effects animation craft or live-action/video delivery.
---

# Lottie animation delivery

Use this skill when a designed vector animation must move reliably from an authoring tool into web, mobile, application, or rendered-video players. The production problem is interchange: preserving intended motion, typography, assets, timing, accessibility, and control across implementations with different feature support.

Lottie is not a universal After Effects renderer. Treat the target-player matrix as an input before animation is finalized, not as a test performed only after export.

## Evidence and volatility

- **Documented fact:** behavior from the official Lottie specification, lottie-web, dotLottie specification, W3C, or browser documentation.
- **Production heuristic:** a practical default that must be tested against target players and the design.
- **Empirical observation:** a measured result from an exported file, player fixture, device, frame capture, or final delivery.

Facts were checked **2026-07-12**. The official Lottie specification describes itself as a work in progress. Player feature support, exporter options, dotLottie versions, state machines, themes, and package APIs can change. Record exact exporter/player versions and re-check their current documentation.

## Decide whether Lottie fits

Use Lottie when the deliverable benefits from:

- compact, scalable vector animation;
- authored keyframes, shapes, precompositions, images, text, masks, or mattes supported by the targets;
- runtime playback, seeking, markers, segments, or state changes;
- reuse across several supported players;
- responsive container scaling;
- deterministic frame capture into another video compositor.

Choose another format when:

- live action, video layers, photographic effects, or pixel processing dominate;
- audio is part of the animation asset contract;
- the required AE features do not survive the target players;
- exact offline rendering matters more than runtime control;
- 3D camera, lighting, particles, simulation, or shader behavior exceeds proven player support;
- a simple CSS/SVG transition is more maintainable.

**Documented fact:** the `AE Feature Support` section of the official lottie-web README says video, audio, and image sequences are not supported by its Bodymovin export/player path. Treat audio as a separately synchronized media asset in the host composition.

## Lock the delivery matrix first

Record:

- source composition, dimensions, frame rate, in/out range, and approved reference render;
- exact target players, versions, renderers, browsers/devices, and host frameworks;
- JSON versus `.lottie` deliverables and required dotLottie version;
- autoplay, loop, segment, marker, speed, direction, state, and interaction requirements;
- text strategy: glyph outlines, runtime text, localization, fonts, fallbacks, and licensing;
- external/embedded images and CORS/offline constraints;
- masks, mattes, blend modes, effects, expressions, time remap, and nested compositions used;
- responsive fit/crop behavior and reduced-motion/static fallback;
- deterministic video-capture requirements;
- file-size, startup-time, memory, and delivery limits;
- ownership, source-art rights, fonts, images, logos, and third-party notices.

Create one minimal feature fixture per risky capability and test it in every target before authoring many animations.

## Understand the interchange model

**Documented facts:** a Lottie document is JSON with an Animation object at the root. Animation data includes dimensions, frame rate, in/out points, layers, assets, and animated properties. Keyframes are ordered by frame and can use holds or cubic-bezier easing. Layers can be parented so child transforms compose with parent transforms.

This makes Lottie suitable for time-addressable vector motion, but a valid document does not prove identical rendering in every player. The specification covers an expanding subset of the ecosystem, and players may implement additional, missing, or different behavior.

Keep a compatibility ledger:

```text
feature | source usage | web-svg | web-canvas | ios | android | dotlottie-player | fallback
```

Populate it with tested results for the pinned versions. Do not copy a generic support table into production approval.

## Authoring and export contract

Bodymovin/lottie-web commonly exports supported After Effects compositions to JSON. Before export:

- set exact composition dimensions, fps, work area, and final duration;
- remove unused layers, effects, expressions, keyframes, and oversized hidden art;
- give layers and markers stable semantic names;
- convert or simplify unsupported effects only with design approval;
- keep a reference movie and representative source frames;
- collect or outline fonts and freeze approved copy;
- decide whether raster assets are external, embedded, or packaged;
- retain editable source and export settings.

**Documented facts from lottie-web:** Bodymovin supports common shapes, precompositions, solids, images, nulls, text, masks, and time remapping, with limitations. Its composition options include converting text to glyph shapes; including hidden/guided layers when referenced; exporting extra compositions; and preserving original raster-asset names. Hidden and guided layers increase output when included.

Use the exporter's report/preview plus target-player tests. A clean exporter preview is not cross-platform validation.

## Typography: glyphs or runtime text

### Glyph outlines

Choose glyph conversion when copy is fixed and exact visual shape matters. It removes runtime font loading as a rendering dependency, but increases vector data, loses normal text semantics/editability, and needs re-export for copy or localization changes.

### Runtime text and fonts

Choose runtime text when localization or dynamic copy is required and the target player supports the needed text behavior. Package or preload licensed fonts before animation initialization; test shaping, line breaks, fallback, glyph coverage, right-to-left scripts, combining marks, and locale expansion in every player.

Do not assume a Latin fixture validates Arabic, Devanagari, CJK, or another script. Do not outline copy that must remain accessible or dynamically translated without providing an equivalent semantic text layer in the host.

Text decision record:

- exact source string and locale;
- font family/file/weight/style/license/checksum;
- glyph versus text mode;
- expected wrap box and line breaks;
- runtime replacement API if used;
- accessibility text and localization owner;
- fallback if font or shaping fails.

## Images, masks, mattes, effects, and expressions

Inventory every non-shape feature. Test combinations, not only isolated features.

### Images

- Freeze local image files and preserve aspect behavior.
- Avoid mutable remote URLs in final packages.
- Test missing/error states and offline use.
- Deduplicate shared assets when packaging multiple animations.
- Record image rights and transformations.

### Masks and mattes

Mask and matte behavior can differ by renderer/player. Test edge quality, inverted/subtractive behavior, nesting, alpha, crop, and performance. If a target fails, simplify the construction, convert it to supported vector geometry, pre-render that element, or change the delivery format.

### Effects and blend modes

Do not assume AE effects or blend modes have portable equivalents. Use only the subset proven in the target matrix. Compare the result against reference frames over light, dark, transparent, and real host backgrounds.

### Expressions

Expressions add portability and determinism risk. lottie-web exposes a renderer setting that can disable expressions. Where expressions are required:

- test exact player support;
- avoid network, wall-clock, device, or unseeded random dependencies;
- profile runtime cost;
- document a baked-keyframe fallback;
- verify arbitrary seeking.

## Choose JSON or dotLottie deliberately

Raw Lottie JSON may reference image/font assets separately or embed some resources. It is simple and broadly understood but can produce multi-file custody problems.

**Documented fact:** dotLottie packages one or more Lottie JSON animations and resources into a Deflate-compressed ZIP archive with `.lottie` extension. In dotLottie v2, `manifest.json` and the `a/` animations directory are required; `i/`, `f/`, `t/`, and `s/` can contain images, fonts, themes, and state machines. The manifest requires a version and at least one animation entry.

Version choice matters. The official dotLottie documentation labels v2 as recommended for new projects and v1 as widely supported. Verify target-player support before choosing v2 features such as themes or state machines.

Package rules:

- validate manifest IDs against actual files;
- keep filenames portable and case-consistent;
- ensure paths do not escape the archive;
- include only required assets;
- deduplicate shared images/fonts;
- document initial animation/state and optional themes;
- test archive parsing, missing assets, and unsupported optional features;
- preserve the original JSON/source package for debugging and migration.

Do not hand-edit generated JSON or archives without recording the transformation and rerunning validation/reference comparisons.

## Playback, markers, and segments

**Documented facts from lottie-web:** animation instances support controls including `play`, `pause`, `stop`, speed, direction, `goToAndStop`, `goToAndPlay`, `playSegments`, `setSubframe`, `getDuration`, and `destroy`. Frame-based seeking is selected with the `isFrame` argument. `setSubframe(false)` respects the source composition fps; the default subframe mode updates with intermediate values.

Use markers as stable semantic edit/state names such as `idle`, `focus`, `success`, and `reset`. Verify exact names, start frames, durations, boundary semantics, and fallback behavior in each player. For dotLottie v2 state-machine segments, the specification says a missing marker falls back to the full animation range; treat that as a validation defect rather than a safe default.

Test:

- first and last frame of every segment;
- repeated triggering and interruption;
- reverse and speed changes if supported;
- transitions from every valid state;
- invalid/missing marker behavior;
- loop boundary without duplicate-frame hitch;
- teardown with `destroy()` or the target equivalent.

If the same `animationData` object containing repeaters is loaded into lottie-web more than once, the official README advises deep-cloning it per load because internal mutation can affect instances.

## Deterministic video capture

For frame-rendered video, disable autoplay and seek explicitly after data, DOM, fonts, and images are ready.

Example lottie-web capture shape:

```js
const animation = lottie.loadAnimation({
  container,
  renderer: "svg",
  loop: false,
  autoplay: false,
  animationData,
});

await readyForCapture(animation, fonts, assets);
animation.setSubframe(false);

export function renderFrame(frame) {
  animation.goToAndStop(frame, true);
}
```

The readiness helper is host-specific. Listen for and verify the relevant data/DOM/image readiness events and font promises; do not rely on a fixed delay.

Capture requirements:

- expected source frame count and frame rate recorded;
- explicit seek to frame zero before capture;
- fixed animation data and local assets;
- no autoplay, wall-clock callbacks, unseeded expressions, or interaction state;
- isolated, backward, and out-of-order seek tests;
- renderer and player pinned;
- repeated frame comparisons;
- separately synchronized audio based on the host timeline.

Decide subframe behavior from the contract. Source-frame capture commonly uses `setSubframe(false)`. If the host output fps differs and intermediate rendering is desired, test the chosen interpolation and frame mapping explicitly instead of assuming it preserves timing.

## Responsive sizing and variants

lottie-web renderer settings expose `preserveAspectRatio` behavior for SVG and Canvas. Decide whether each canvas should meet, slice, or use a separately authored composition.

- `meet` preserves the whole artboard but may letterbox.
- `slice` fills the box but can crop essential content.
- changing only container size does not redesign type, gesture, safe areas, or information density.

For materially different aspect ratios, produce separate layouts or source comps when crop rules cannot preserve the message. Test line weight, small type, masks, filter bounds, and raster assets at final dimensions.

## Optimization

Optimize after visual correctness and target compatibility are established:

- remove unused layers and keyframes;
- reduce path points while preserving silhouettes and easing;
- avoid huge masked shapes when a smaller construction works;
- reduce nested complexity and expression work;
- choose glyphs versus fonts based on the actual copy/locale matrix;
- centralize shared dotLottie assets;
- compress delivery transport without corrupting archive expectations;
- profile SVG, Canvas, or other target renderers rather than declaring one universally fastest.

Measure package size, parse/load time, first rendered frame, steady playback, memory, and teardown. Test low-end target devices and multiple simultaneous instances if that is the product use.

## Accessibility and safety

For interactive surfaces:

- expose semantic purpose at the host control/container level;
- ensure buttons and state changes remain operable without relying on the animation DOM;
- provide accessible name/description or adjacent text;
- honor `(prefers-reduced-motion: reduce)` by disabling autoplay, reducing movement, selecting a calm segment, or showing a static poster;
- provide user pause/stop controls where required;
- never encode essential status only in motion or color.

lottie-web supports SVG renderer settings for a title and description, but this does not replace accessible host semantics or a fallback for Canvas/other players.

For prerecorded exports, render a reduced-motion variant if needed; CSS cannot change pixels already encoded in a video.

**Documented fact:** WCAG 2.2 SC 2.3.1 restricts flashing above three times in one second unless below threshold. Test loops while looping and at the largest intended view. SC 2.3.3 says non-essential interaction-triggered motion can be disabled unless essential.

## Rights and provenance

lottie-web is MIT-licensed. That license does not clear source artwork, After Effects projects, fonts, logos, images, plugins, characters, or downloaded animation files. A file being technically editable or publicly viewable is not evidence of commercial rights.

Maintain:

- animation/source owner and license;
- exporter and player versions/licenses;
- font and image licenses;
- asset checksums;
- modifications and optimization steps;
- reference render and approvals;
- distribution targets and restrictions;
- generated-media provenance where applicable.

Preserve required notices and escalate unclear marketplace, template, branded, likeness, or derivative rights.

## Validation and QA

Validate in layers:

1. **Source:** approved reference, dimensions, fps, work area, exact copy, and asset inventory.
2. **Structure:** JSON/schema or dotLottie manifest/archive integrity, paths, IDs, assets, and versions.
3. **Feature parity:** source feature inventory against each target player/renderer.
4. **Frame parity:** compare representative first/mid/last, mask, text, effect, and segment-boundary frames.
5. **Behavior:** autoplay, loops, markers, segments, state transitions, invalid state, and destroy/reload.
6. **Typography:** font load, glyph coverage, shaping, line breaks, localization, and accessibility text.
7. **Performance:** load, playback, memory, simultaneous instances, and teardown.
8. **Accessibility:** semantics, reduced motion, flashing, controls, and static/structured alternatives.
9. **Capture:** frame count, arbitrary seeking, repeated frames, alpha/background, and audio sync in the host.

Critical failures include missing assets, wrong copy/font, unsupported feature changing meaning, nondeterministic frame capture, broken segment/state fallback, unsafe flashing, no reduced-motion handling where required, or unverified rights.

## Delivery handoff

Provide:

- editable source and approved reference render;
- exported JSON plus assets and/or `.lottie` package;
- target compatibility matrix with tested versions;
- exact player initialization and lifecycle notes;
- marker/segment/state/theme documentation;
- font/image packages and licenses;
- reduced-motion/static fallback;
- validation and performance report;
- deterministic capture notes where relevant;
- provenance ledger, notices, and known limitations.

## Example 1: localized onboarding sequence

This is a complete example, not a mandatory formula.

**Intent:** deliver a three-state onboarding illustration (`idle`, `scan`, `success`) for web, iOS, and Android in six locales.

**Constraints:** dynamic localized label; no audio; 320x320 logical artboard; host button provides interaction semantics; reduced-motion mode; one small raster texture; offline use.

**Workflow:**

1. Test shape, mask, text, and raster fixtures in pinned target players before final animation.
2. Keep the localized label as runtime text; package the licensed font and test shaping/glyph coverage for every locale before player initialization.
3. Author semantic markers and verify exact segment boundaries in all targets.
4. Package JSON/assets for broad compatibility first; add a dotLottie package only for targets that have passed the selected version/features.
5. Host controls state and accessibility; Lottie renders visual feedback only.
6. Record approved stable `idle-poster` and `success-poster` marker frames after export. Reduced-motion mode seeks directly to those frames and replaces the scan sweep with a short opacity change.
7. Test offline loading, wrong locale, missing font, marker typo, repeated success/reset, and destroy/reload.

**Expected result:** exact localized text, equivalent visual states, no inaccessible animation-only status, and no remote dependencies.

**Likely failures:** font initializes too late; one script shapes incorrectly; marker boundaries differ; mobile player drops a mask; the raster texture is missing offline; repeated loads share mutated data.

**Variation:** if cross-player runtime text cannot pass, export locale-specific glyph animations while keeping semantic label text in the host UI.

## Example 2: Lottie layer inside a rendered video

This is a complete example, not a mandatory formula.

**Intent:** use an approved eight-second vector route animation as a deterministic overlay in a 30 fps product video.

**Constraints:** transparent background; exact frame alignment to narration; SVG renderer in a pinned headless browser; no interaction; separate narration/music; final 1920x1080 and 1080x1920 versions.

**Workflow:**

1. Freeze JSON, images, font strategy, player version, and approved reference.
2. Disable autoplay and looping; wait for data, DOM, images, and fonts.
3. Set source-frame/subframe behavior explicitly and map host frames to animation frames.
4. Seek each requested frame with `goToAndStop(..., true)`; capture alpha through the host compositor.
5. Render frames 0, 1, every marker boundary, mask/effect stress frames, and final frame twice, including backward order.
6. Author a separate vertical layout if `slice` crops route labels.
7. Mux audio in the host timeline; do not expect Lottie to carry it.
8. Destroy the instance and verify no DOM/listener/resource accumulation across worker jobs.

**Expected result:** repeated frame identity within the locked browser environment, correct alpha, exact narration cues, and equivalent horizontal/vertical message.

**Likely failures:** fixed-delay readiness misses an image; source/output fps mapping is off by one; autoplay advances before capture; remote font changes wrapping; vertical crop cuts labels; final loop frame duplicates the first.

**Variation:** when a target renderer cannot reproduce a required matte, pre-render the approved Lottie layer to a lossless alpha sequence and document that the interactive asset and video derivative have different delivery paths.

## Sources

Official and authoritative sources checked 2026-07-12:

- Airbnb lottie-web repository, including `AE Feature Support`, usage, and license: https://github.com/airbnb/lottie-web#ae-feature-support
- lottie-web usage: https://github.com/airbnb/lottie-web/wiki/Usage
- lottie-web composition settings: https://github.com/airbnb/lottie-web/wiki/Composition-Settings
- lottie-web renderer settings: https://github.com/airbnb/lottie-web/wiki/Renderer-Settings
- Official Lottie specification: https://lottie.github.io/lottie-spec/latest/
- Lottie composition, layers, and properties: https://lottie.github.io/lottie-spec/latest/specs/composition/ , https://lottie.github.io/lottie-spec/latest/specs/layers/ , and https://lottie.github.io/lottie-spec/latest/specs/properties/
- dotLottie specification overview and v2: https://dotlottie.io/spec/ and https://dotlottie.io/spec/2.0/
- lottie-web MIT license: https://github.com/airbnb/lottie-web/blob/master/LICENSE.md
- MDN, `prefers-reduced-motion`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- W3C WCAG 2.2, Animation from Interactions: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
- W3C WCAG 2.2, Three Flashes or Below Threshold: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html