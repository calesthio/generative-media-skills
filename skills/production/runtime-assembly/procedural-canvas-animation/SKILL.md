---
name: procedural-canvas-animation
description: Provider-independent production guidance for deterministic Canvas 2D and p5.js animation. Use for particles, fields, trails, weather, procedural textures, generative geometry, and lightweight 2D simulations that need fixed media dimensions, seeded repeatability, transparent compositing, aspect variants, performance QA, or frame-addressable rendering.
---

# Procedural Canvas animation

Use this skill when a 2D bitmap canvas is the appropriate drawing surface for procedural motion. It covers authored particles, vector/noise fields, trails, weather, textures, generative geometry, and lightweight simulations for rendered media.

It does not cover Three.js scene graphs, WebGL/WebGPU shaders, D3 data semantics, game-engine architecture, or a generic frontend Canvas tutorial.

## Evidence stance

- **Documented fact:** behavior from WHATWG, ECMAScript, p5.js, W3C, or cited API documentation.
- **Production heuristic:** a practical design or optimization choice to test in the target runtime.
- **Empirical observation:** a measured result from the actual animation, browser, frame output, or encoded delivery.

Facts were verified **2026-07-12**. Canvas, browser, p5.js, OffscreenCanvas, and encoding behavior can change; pin versions and record the render environment.

## Lock the canvas contract

Define:

- backing width/height, CSS/display size, aspect variants, fps, frame range, and alpha requirement;
- coordinate system and projection from normalized simulation space;
- seed, algorithm, initialization, parameters, and state-update order;
- stateless, replay, or checkpoint strategy;
- color space, compositing modes, background, and premultiplication assumptions;
- source images/fonts and CORS/offline policy;
- target runtime/browser, pixel density, output format, and encoder;
- reduced-motion/static variant and flash policy;
- performance budget and representative stress frames;
- provenance and rights for all source ingredients.

## Understand the bitmap

**Documented facts:** Canvas has an intrinsic resolution separate from CSS sizing. Its default bitmap is 300 by 150. Setting its `width` or `height` clears the bitmap and resets context state. Canvas 2D begins with `source-over` and `globalAlpha = 1` and uses premultiplied alpha. A context requested with `{alpha:false}` is opaque and unsuitable for transparent delivery.

Set backing dimensions explicitly. Do not stretch a low-resolution backing bitmap with CSS and call it high resolution. For fixed video output, choose exact pixel dimensions and an explicit density; p5.js `pixelDensity(1)` is often appropriate for predictable output.

Changing size is a reconstruction event: rebuild transforms, state, buffers, and layout rather than assuming pixels or context settings survive.

## Use an absolute-frame interface

Design around:

```js
renderFrame(frameIndex, variant, accessibilityMode)
```

with composition time:

$$
t = \frac{frameIndex}{fps}
$$

Keep `requestAnimationFrame()` outside production state. **Documented fact:** rAF is one-shot, follows browser display scheduling, may pause in hidden contexts, and does not guarantee 60 fps. p5.js `frameRate()` requests a target but does not define offline media time.

Do not use `Date.now()`, `performance.now()`, `millis()`, `deltaTime`, or mutable `frameCount` as final-render truth.

## Choose a determinism strategy

### Stateless

Calculate every object directly from `(seed, objectId, frameIndex, channel)`. Best for periodic fields, analytic particles, procedural lines, and arbitrary-frame access.

### Fixed-step replay

Reset to deterministic initial state and advance exactly $\Delta t = 1/fps$ in a documented order until the requested frame. Suitable for stateful snow, flocking, or cellular systems when duration is manageable.

### Checkpoints

Persist deterministic state at fixed frames and replay from the nearest earlier checkpoint. Useful for long stateful simulations. Version checkpoint schema and reject it when parameters/runtime change.

History-dependent persistent-buffer trails are not random-access. Replay history, store checkpoints, or draw the previous $K$ analytic positions into each frame.

## Seed randomness explicitly

**Documented fact:** ECMAScript `Math.random()` has an implementation-defined algorithm and no seed control. p5.js `randomSeed()` and `noiseSeed()` can repeat their respective sequences, but that does not guarantee pixel identity across p5/browser versions.

Record seed and generator implementation. Prefer keyed random values where arbitrary access matters, so rendering frame 200 does not depend on how many random values earlier frames consumed.

Never reseed every frame unless the intended algorithm is explicitly frame-keyed; that often freezes or correlates motion.

## Particles, fields, weather, and trails

For each system define:

- spawn domain and lifetime;
- initial position/velocity/shape/color distributions;
- force/field equations and units;
- boundary behavior: wrap, reflect, kill, respawn, or clamp;
- update ordering and collision policy;
- mapping from normalized simulation to each canvas;
- trail/history policy;
- outlier and NaN handling.

Keep simulation state independent of pixels. Aspect variants should share the event while changing framing, count, density, line width, or field bias intentionally.

For weather, distinguish visual plausibility from physical simulation. Do not claim meteorological accuracy unless the model and inputs support it.

## Compositing and alpha

Set `globalCompositeOperation` deliberately and restore context state. Test `source-over`, additive/lighten effects, masks, and erasure over black, white, and checkerboard backgrounds.

Transparent delivery requirements:

- context alpha enabled;
- no accidental background fill;
- output format/codec preserves alpha;
- corner and edge pixels inspected;
- premultiplied/straight-alpha conversion and halos checked in the receiving compositor.

JPEG cannot preserve alpha. WebCodecs encoder alpha behavior is configuration- and codec-dependent; verify capability and output instead of assuming support.

## External assets and origin cleanliness

**Documented fact:** drawing cross-origin media without valid CORS can make a canvas non-origin-clean, causing pixel reads and serialization to throw `SecurityError`.

Freeze production assets locally where possible. Record URLs, licenses, hashes, CORS policy, and failure behavior. Do not discover a tainted canvas after a long render.

## p5.js production pattern

For deterministic offline work:

```js
function setup() {
  pixelDensity(1);
  createCanvas(outputWidth, outputHeight, P2D);
  noLoop();
  initialize(seed);
}

function renderFrame(frame) {
  resetOrRestore(frame);
  advanceTo(frame, 1 / fps);
  drawCurrentState();
}
```

This is an architectural example. `advanceTo()` must not advance once too many; define whether frame zero represents initial state before any step.

Avoid allowing window size, input events, or live device density to alter final state. `resizeCanvas()` clears output and typically triggers redraw, so rebuild the declared variant explicitly.

## Performance

Profile before moving work to a worker. First reduce:

- algorithmic complexity and pairwise interactions;
- repeated path construction and context state changes;
- large shadows/filters and overdraw;
- pixel readbacks and per-pixel loops;
- allocation inside frame loops;
- excessive object count or trail history;
- redundant redraws of static layers.

**Documented fact:** OffscreenCanvas is transferable and can run in workers, but worker use does not guarantee lower total render time. It can improve main-thread responsiveness and pipeline separation. Verify APIs available in the worker and account for transfer/serialization cost.

Measure warm and cold frame time, p50/p95, peak memory, output readback, and teardown. Promise repeatability only for a pinned environment; fonts, antialiasing, filtering, floating point, and color conversion can differ.

## Accessibility and safety

Meaningful non-text content needs an equivalent alternative. Color cannot be the sole carrier of meaning, and meaningful graphics/control indicators need appropriate contrast.

WCAG 2.2 limits flashing above three times in one second unless below thresholds. Test rendered loops while looping. Qualifying automatic motion on interactive surfaces needs pause/stop/hide behavior.

Reduced motion should alter motion language: static representative frame, slower drift, smaller displacement, fewer particles, or user-controlled playback. Lowering FPS alone may increase jerk without reducing motion extent.

For decorative canvas, hide implementation details from assistive technology and expose meaning in the host. Canvas text or a description is not a substitute for keyboard-operable semantic controls.

## Provenance and QA

Record seed, generator, algorithm/library versions, parameters, dimensions, fps, frame range, color space, density, source assets/licenses/hashes, runtime/browser, and output hashes.

QA:

1. Render selected frames directly and sequentially; compare within the declared environment/tolerance.
2. Test first, last, loop boundary, respawn, collision, and aspect-variant frames.
3. Detect NaN, Infinity, runaway positions, and unbounded allocations.
4. Inspect transparent output over multiple backgrounds.
5. Test CORS/readback before full render.
6. Measure p50/p95 frame time after warm-up.
7. Review final-size detail, flashing, reduced motion, and alternatives.
8. Verify output frame count, dimensions, alpha, color, and encoding.

## Example 1: transparent wind-ribbon overlay

This is a complete example, not a mandatory formula.

**Intent:** eight-second, 30 fps, 1920x1080 transparent overlay of 600 luminous wind traces.

**Approach:** use seed `42719`, normalized coordinates, and 36-frame analytic trails. Immutable particle parameters come from a keyed generator. Each position is a pure periodic function of absolute time. Frame $f$ clears transparent and draws segments from $f-36$ through $f$ with bounded age-controlled alpha/width. Use `source-over` for base ribbons and a separately tested additive highlight.

**QA:** direct versus sequential hashes for frames 0, 1, 137, and 239; alpha histogram/corners; black/white/checkerboard composites; p50/p95; flash test.

**Likely failures:** mutable PRNG consumption, `{alpha:false}`, background fill, clipped additive values, or wrapped-trail jumps.

**Variation:** 9:16 lowers count and biases vertical flow; reduced-motion output is an approved static frame.

## Example 2: replayable p5.js snowfall

This is a complete example, not a mandatory formula.

**Intent:** 12-second snowfall at 30 fps in 9:16 and 16:9, plus static reduced-motion output.

**Approach:** `pixelDensity(1)`, `noLoop()`, seed random/noise with `8301`, use normalized state and fixed $1/30$ steps. `renderFrame(n)` resets, steps `0..n-1`, then draws. Dimensions affect projection and composition margins, not simulation state. Respawns consume values only in deterministic replay order.

**QA:** replay frame 240 twice; compare normalized state before projection; reject NaN/out-of-bounds growth; test crops, performance, pause behavior, alternatives, and flashing.

**Likely failures:** `deltaTime`, `millis()`, `frameCount`, or window dimensions leak into state; resizing without reconstruction; assuming seed output is version-stable.

## Sources

Verified 2026-07-12:

- WHATWG Canvas and animation frames: https://html.spec.whatwg.org/multipage/canvas.html and https://html.spec.whatwg.org/multipage/imagebitmap-and-animations.html#animation-frames
- ECMAScript `Math.random`: https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-math.random
- p5.js references for draw, frameRate, randomSeed, noiseSeed, pixelDensity, resizeCanvas, and noLoop: https://p5js.org/reference/
- MDN requestAnimationFrame, OffscreenCanvas, and Canvas optimization: https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame , https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas , and https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas
- WebCodecs: https://www.w3.org/TR/webcodecs/
- WCAG 2.2 non-text content, flashing, use of color, non-text contrast, and pause/stop/hide: https://www.w3.org/WAI/WCAG22/Understanding/