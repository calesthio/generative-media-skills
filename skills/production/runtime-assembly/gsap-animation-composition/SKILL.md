---
name: gsap-animation-composition
description: Production guidance for authoring, integrating, and reviewing GSAP animation in browser-rendered media. Use for deterministic kinetic typography, SVG drawing and morphing, motion paths, FLIP transitions, responsive motion systems, or frame-seekable GSAP timelines inside HTML video composition and React-based renderers; not for ordinary CSS transitions or generic frontend development.
---

# GSAP animation composition

Use GSAP when a media composition needs choreography that is awkward to express as isolated CSS transitions or simple frame interpolation: overlapping multi-beat sequences, per-character typography, SVG stroke drawing or shape morphing, curved paths, layout-state transitions, or a reusable motion language controlled from one playhead.

This skill covers GSAP as an animation engine inside media production. It does not replace the composition contract, edit decisions, audio timeline, asset ledger, accessibility review, or delivery workflow of the host renderer.

## Evidence and version stance

The following labels are used throughout:

- **Documented fact**: behavior stated in official GSAP, W3C, or browser documentation.
- **Production heuristic**: a practical default that should yield to the brief, brand system, renderer, or measured result.
- **Empirical observation**: a result measured in the actual composition, preview, render, or target device.

GSAP APIs, plugin packaging, licensing, and framework integrations are volatile. The API and license facts below were verified on **2026-07-12**. Re-check the installed GSAP version, official installation guidance, plugin documentation, and current license before production use.

## Decide whether GSAP is warranted

Choose GSAP when at least one of these is central to the deliverable:

- many dependent animation beats must share labels, overlaps, or nested timelines;
- text must split into words, lines, or characters for designed reveals;
- SVG paths must draw, morph, or carry moving objects;
- a layout change must preserve apparent continuity through a FLIP transition;
- a browser-native composition needs one seekable playhead for preview and frame capture;
- responsive variants need related but materially different motion choreography.

Prefer a simpler mechanism when:

- one element only fades, translates, scales, or rotates;
- the host video runtime already provides concise frame interpolation or spring primitives;
- conventional editing, compositing, or keyframes will be easier for the receiving team to revise;
- the deliverable is a static image, an interchange asset, or a native application animation that will not run in a browser context.

Do not add a plugin merely because it exists. Every plugin should eliminate meaningful implementation risk or improve the intended motion.

## Lock the motion contract

Before writing animation code, record:

- composition dimensions, aspect ratios, frame rate, and duration;
- scene and beat timecodes, including audio or narration anchors;
- exact on-screen text and final held states;
- layer names, selectors, SVG path IDs, and transform pivots;
- entry, emphasis, transition, and exit purpose for each animated element;
- motion tokens: duration families, easing families, stagger policy, travel limits, and overshoot policy;
- responsive and reduced-motion variants;
- renderer ownership of the playhead;
- plugin imports and current licensing review;
- review frames and failure thresholds.

If the renderer captures arbitrary frames, the composition must be correct when visited out of order. A beautiful real-time preview is not evidence of deterministic rendering.

## Build one controlled timeline

**Documented fact:** a GSAP `Timeline` contains tweens and nested timelines and can control them as a unit. Its position parameter can place children at absolute times, relative to the timeline end, relative to labels, or relative to the most recently added child with markers such as `<` and `>`. Timelines expose controls including `pause()`, `seek()`, `time()`, `progress()`, and `totalProgress()`.

Use semantic labels for editorial beats, not incidental implementation steps:

```js
const timeline = gsap.timeline({
  paused: true,
  defaults: {duration: 0.42, ease: "power3.out"},
});

timeline
  .addLabel("claim", 0.4)
  .from(".claim-line", {yPercent: 110, stagger: 0.07}, "claim")
  .addLabel("proof", "claim+=0.85")
  .from(".proof-mark", {scaleX: 0, transformOrigin: "left"}, "proof")
  .from(".proof-label", {opacity: 0, y: 16}, "<0.12")
  .to(".claim-group", {opacity: 0, duration: 0.24}, ">+1.1");
```

This is an example, not a required timeline shape.

Production rules:

- Use labels such as `claim`, `proof`, `turn`, and `cta` when they correspond to script, music, or edit events.
- Use timeline defaults for a coherent motion family, then override deliberately.
- Nest timelines by scene or semantic unit; return them to a master timeline.
- Prefer position parameters over chains of manually calculated delays.
- Keep the timeline finite for rendered media. An infinite repeat has no auditable final state.
- Use `fromTo()` when both endpoints must be explicit, especially after rerenders, responsive rebuilds, or repeated state changes. Otherwise prefer the simpler `to()` or `from()` form.
- Do not let CSS transitions compete with GSAP on the same properties.
- Set transform state consistently through GSAP when GSAP owns those transforms.

### Staggers

**Documented fact:** GSAP staggers can be numeric, objects, or functions. Object configuration can distribute start times with `each` or a total `amount`, choose a `from` origin, account for a grid, restrict an axis, and ease the distribution.

Use stagger to express hierarchy, direction, or rhythm. Do not use it to avoid designing individual beats. For text, keep the final phrase readable long enough after the last unit arrives. For grids, test the actual responsive layout rather than assuming DOM order matches visual order.

## Make frame capture deterministic

Normal GSAP playback is driven by the browser animation loop. **Documented fact:** `gsap.ticker` updates the global timeline from `requestAnimationFrame`; browser scheduling and hidden-tab throttling vary. A video renderer that requests exact frames should therefore own time explicitly rather than waiting for wall-clock playback.

Use this pattern when the host can seek a paused timeline:

```js
const timeline = buildTimeline();
timeline.pause(0);

export function renderAtFrame(frame, fps) {
  const time = frame / fps;
  timeline.time(Math.min(time, timeline.duration()), false);
}
```

If the host expects normalized progress:

```js
timeline.totalProgress(frame / Math.max(1, totalFrames - 1), false);
```

Renderer-specific integration may use another adapter, but preserve these invariants:

1. Build the timeline synchronously after required DOM, fonts, SVG, and local assets are ready.
2. Pause it before capture begins.
3. Derive time only from the requested frame and declared fps.
4. Use fixed inputs. Seed or precompute random values; do not call `Math.random()` during frame evaluation.
5. Avoid network fetches, time-of-day values, user input, scroll state, and asynchronous callbacks as animation state.
6. Ensure seeking backward restores a correct state.
7. Make callback side effects idempotent or suppress them during arbitrary seeks.

Do not confuse `gsap.ticker.fps(30)` with deterministic 30 fps rendering. It throttles ticker callbacks; it does not make browser scheduling a frame-render contract.

## Select plugins by production problem

Register only the plugins included in the actual build, using the official installation pattern for the current package version.

| Production problem | Appropriate capability | Main review risk |
|---|---|---|
| Word, line, or character choreography | SplitText | changed semantics, broken line wrapping, missing cleanup, text no longer accessible |
| Reveal an SVG stroke | DrawSVG | wrong path length, line too thin after compression, no meaningful final state |
| Transform one SVG shape into another | MorphSVG | poor point correspondence, self-intersections, unintended silhouette, incompatible source paths |
| Move or orient an object along a path | MotionPath | wrong coordinate space, unexpected rotation, path outside crop, motion sickness |
| Animate between measured layout states | Flip | stale measurements, reflow during capture, unclear end layout |
| Encode a project-specific motion curve | CustomEase | overfitted or extreme curve, inconsistent naming, inaccessible acceleration |
| Couple animation to page scroll | ScrollTrigger | unsuitable for fixed-time video unless scroll is converted into explicit timeline progress |

### Text splitting

Treat split wrappers as implementation layers, not authored copy. Preserve the exact text in source and verify assistive-technology behavior in the target delivery. Wait for production fonts before splitting because line breaks and glyph metrics can change. Rebuild and revert split text when responsive line wrapping changes.

For a fixed video render, save the approved line breaks when the design requires them. Do not let an incidental browser width determine the hero copy.

### SVG drawing, morphing, and paths

- Clean source paths and set an intentional `viewBox`.
- Record each pivot and coordinate system.
- Verify the start, midpoint, and final silhouette at delivery resolution.
- Keep source and target shapes semantically related; a morph should communicate transformation, not merely display technical novelty.
- Test thin strokes after final video compression.
- For character or object rigs, animate stable groups around authored pivots rather than deforming every path independently.

### FLIP transitions

Capture the first state, apply the final layout, then animate the measured difference. Freeze the data and layout inputs for deterministic rendering. If the final state depends on font loading, network data, or a responsive measurement, resolve those before recording state.

## Responsive and reduced-motion variants

**Documented fact:** `gsap.matchMedia()` can run setup for native media queries, collect animations in a context, and revert them when conditions stop matching. It can combine width queries with `(prefers-reduced-motion: reduce)`.

Use responsive variants to preserve hierarchy, not to squeeze desktop choreography into a smaller frame. Change line breaks, path geometry, travel distance, stagger direction, and label timing when the aspect ratio changes. Rebuild the timeline after the relevant layout is stable.

For interactive delivery, honor the user preference and provide a control when required. Reduced motion can use cuts, short fades, local emphasis, and stable final states rather than large-field translation, parallax, rapid zoom, or spinning.

For prerecorded video, `prefers-reduced-motion` cannot change the pixels after export. Decide whether the audience or destination needs a separately rendered reduced-motion version.

**Documented fact:** WCAG 2.2 SC 2.3.3 says non-essential interaction-triggered motion animation can be disabled, unless essential. SC 2.3.1 requires content not to flash more than three times in any one-second period unless it remains below the general and red flash thresholds. Test rendered video at its largest intended presentation and test loops while looping.

## Cleanup and framework lifecycle

**Documented fact:** `gsap.context()` can collect animations created within its function, scope selectors, and revert collected animations. `gsap.matchMedia()` uses a context internally. Reversion kills collected animation and restores recorded pre-animation state; custom event listeners still need explicit cleanup.

Create timelines once per mounted composition or responsive state. On teardown:

- revert the context or match-media object;
- remove custom event and ticker listeners;
- revert split text and temporary wrappers;
- dispose renderer-specific observers;
- clear references to detached DOM or SVG nodes.

In React-based renderers, use the current official GSAP React integration or an equivalent lifecycle-safe effect. Do not instantiate timelines during every render.

## Performance and render reliability

Production heuristics:

- Prefer transforms and opacity for high-frequency motion; measure before assuming other properties are unacceptable.
- Avoid animating large blur, filter, shadow, or mask regions across many layers without profiling.
- Keep SVG path complexity proportionate to output resolution.
- Pre-create stable timelines instead of constructing them inside repeated interaction callbacks.
- Scope selectors to the composition root.
- Use one owner per animated property.
- Freeze remote assets locally and wait for fonts before capture.
- Render a short stress segment before committing to a long or high-resolution export.

Record empirical results: browser and GSAP versions, renderer, GPU/software path, frame size, fps, concurrency, dropped or duplicated frames, memory behavior, and any differences between preview and render.

## Licensing and rights gate

The repository containing this skill is MIT-licensed. That does **not** change the license of GSAP.

**Documented fact, verified 2026-07-12:** the current official page identifies Webflow's Standard "No Charge" GSAP License as effective April 30, 2025 and last modified May 30, 2025. It grants use for permitted website, web application, and digital-interface implementations, including commercial projects. It prohibits use in tools that let users build visual animations without code when that use competes with Webflow's visual animation-building capabilities, absent consent. It also restricts reverse engineering for competitive products and removal of proprietary notices. The license page says it may be updated, so re-check it before production use.

The separate `greensock/gsap-skills` documentation repository may carry an MIT license; that does not relicense the GSAP runtime or plugins. Do not infer runtime rights from documentation-source licensing.

Before shipping:

- identify who distributes and operates the composition or tool;
- check the current GSAP license and package notices;
- escalate visual animation builders, editor products, templates-as-a-service, sublicensing, redistribution, or ambiguous competitive uses to the rights owner or counsel;
- retain third-party notices required by the package and deployment;
- verify rights for fonts, logos, illustrations, SVG artwork, music, source media, and likenesses separately.

This is production risk guidance, not legal advice.

## Review and QA

Review the composition in this order:

1. **Contract:** dimensions, fps, duration, exact copy, approved assets, plugins, and license status.
2. **Determinism:** capture the same frame twice in clean runs; compare scene boundaries and backward seeks.
3. **Timing:** confirm labels against narration, music, and edit events; ensure final holds are readable.
4. **Motion:** inspect arcs, pivots, morph silhouettes, path orientation, FLIP continuity, easing, and overshoot.
5. **Typography:** confirm font load, line wrapping, wrapper cleanup, glyph integrity, and readable final states.
6. **Accessibility:** review reduced-motion delivery, flashes, large-field motion, text contrast, and information conveyed only by motion.
7. **Performance:** profile the highest-motion section and final delivery resolution.
8. **Output:** inspect sampled frames plus full playback for clipping, missing assets, frozen layers, compression damage, and audio sync.

Critical failures include nondeterministic frame output, unsafe flashing, missing required reduced-motion handling for an interactive surface, unreadable required text, broken final SVG silhouette, unlicensed use, or a timeline that depends on wall-clock/scroll state during fixed-time rendering.

## Example 1: kinetic launch claim

This is a complete example, not a mandatory formula.

**Production intent:** create a six-second 9:16 product-launch insert with exact brand copy and no narration. The first claim must arrive quickly, the proof must remain readable, and a reduced-motion social variant is required.

**Inputs and constraints:** approved font files; copy `Review less. Decide sooner.`; 1080x1920 at 30 fps; final CTA lockup; no full-frame flashes; GSAP and SplitText available under reviewed terms.

**Plan:**

```text
00:00.00-00:00.35  Background and clipping masks already stable.
00:00.35-00:01.15  Split headline by words; reveal from lower mask with 0.07 s stagger.
00:01.15-00:02.20  Hold complete claim.
00:02.20-00:03.05  Draw proof underline; reveal source-safe proof label 0.12 s later.
00:03.05-00:04.45  Hold claim and proof without motion.
00:04.45-00:05.10  Exit claim as one group; do not scramble characters.
00:05.10-00:06.00  CTA lockup, static final state.
```

Implementation direction:

- Load the exact font before splitting.
- Use a paused six-second master timeline with labels `claim`, `proof`, and `cta`.
- Drive timeline time from `frame / 30`.
- Keep the source heading text intact and revert SplitText wrappers during teardown.
- Reduced-motion variant uses a 0.18-second group fade for the claim, a direct proof cut, and the same hold durations.

**Why this works:** the word stagger expresses the sentence rhythm while the long proof hold protects comprehension. The deterministic playhead keeps preview and render aligned.

**Expected result:** exact copy, no line-wrap change between captures, stable final CTA, and matching frames across repeated renders.

**Likely failures:** font loads after splitting; a character stagger makes reading too slow; wrappers remain after a responsive rebuild; timeline callbacks fire twice during seeking; the CTA appears before the exit finishes.

**Meaningful variation:** for 16:9, preserve the labels but replace the vertical word stack with two lines and shorten travel distance rather than center-cropping the vertical design.

## Example 2: SVG route-to-mark transition

This is a complete example, not a mandatory formula.

**Production intent:** create an eight-second explainer transition in which a delivery route becomes the product's approved symbol, connecting a process explanation to the brand end card.

**Inputs and constraints:** approved SVG route and logo paths; 1920x1080 at 30 fps; muted navy background; no random particles; stroke must survive H.264 compression; logo geometry cannot be altered beyond the approved morph.

**Workflow:**

1. Normalize both SVGs to one reviewed `viewBox`; simplify only redundant path points and archive originals.
2. Use DrawSVG to reveal the route from 00:00.40 to 00:01.80.
3. Move a small package marker along the route with MotionPath from 00:00.55 to 00:02.00, with auto-orientation disabled because the package label must remain upright.
4. Hold the completed route for 0.6 seconds.
5. Morph the approved route path into the approved symbol from 00:02.60 to 00:03.55.
6. Settle without elastic overshoot, reveal the wordmark, and hold the complete lockup through 00:08.00.
7. Seek and inspect frames 0, 12, 30, 54, 78, 92, 107, and 239, plus the morph midpoint.

**Why this works:** each plugin has one semantic job: route progress, package movement, then transformation into identity. The extended final hold makes the brand mark usable as an edit point.

**Expected result:** the package follows the path without rotation, the morph has no self-intersection, and the final symbol matches the approved source exactly.

**Likely failures:** coordinate systems disagree; path stroke becomes too thin after compression; morph correspondence creates a knot; the marker drifts outside the crop; the final shape is nearly but not exactly the approved mark.

**Meaningful variation:** if the paths cannot morph cleanly without changing brand geometry, use a match cut or masked crossfade at the shared silhouette instead of forcing MorphSVG.

## Sources

Official and authoritative sources checked 2026-07-12:

- GSAP Timeline documentation: https://gsap.com/docs/v3/GSAP/Timeline/
- GSAP stagger guidance: https://gsap.com/resources/getting-started/Staggers/
- GSAP context and matchMedia documentation: https://gsap.com/docs/v3/GSAP/gsap.context/ and https://gsap.com/docs/v3/GSAP/gsap.matchMedia/
- GSAP ticker documentation: https://gsap.com/docs/v3/GSAP/gsap.ticker/
- GSAP plugin documentation: https://gsap.com/docs/v3/Plugins/
- GSAP CustomEase documentation: https://gsap.com/docs/v3/Eases/CustomEase/
- GSAP common mistakes: https://gsap.com/resources/mistakes/
- Webflow, Standard "No Charge" GSAP License: https://gsap.com/community/standard-license/
- W3C WCAG 2.2, Animation from Interactions: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
- W3C WCAG 2.2, Three Flashes or Below Threshold: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- MDN, `prefers-reduced-motion`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion