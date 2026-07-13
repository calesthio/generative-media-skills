---
name: threejs-scene-composition
description: Production guidance for planning, building, animating, capturing, and reviewing complete Three.js scenes for rendered media. Use for browser-native 3D product shots, title sequences, procedural worlds, glTF scene assembly, camera and lighting animation, shaders, post-processing, deterministic frame export, and Three.js render QA; not for modeling standalone assets, WebXR interaction, or generic website decoration.
---

# Three.js scene composition

Use Three.js when depth, camera, lighting, material response, geometry, or spatial animation carries the media idea and a browser-rendered scene is an appropriate production surface. This skill begins after asset requirements and creative intent are known and ends with a reproducible rendered scene package.

It does not teach mesh modeling, retopology, rig authoring, physics simulation, WebXR product design, or game logic. It may consume approved glTF assets, animation clips, textures, environment maps, fonts, data, and audio cues produced elsewhere.

## Evidence stance

- **Documented fact** means behavior specified by official Three.js, Khronos, WebGL, or W3C sources.
- **Production heuristic** means a useful starting point that must be tested on the actual scene and delivery hardware.
- **Empirical observation** means a result measured from the scene, frame output, browser, GPU, or encoded deliverable.

Three.js releases frequently and examples/addons may change paths or APIs. Facts and links were checked **2026-07-12**. Pin and record the installed revision, check migration notes, and test the exact target browser and renderer before delivery. WebGPU support and renderer parity are especially volatile.

## Decide whether Three.js is the right renderer

Use Three.js when the deliverable needs:

- a real 3D camera, parallax, depth, occlusion, or spatial continuity;
- glTF scene or product assets rendered with browser PBR materials;
- skeletal, morph-target, keyframe, or procedural 3D animation;
- custom shaders, particles, instancing, or post-processing;
- deterministic frame capture from a browser-based composition system;
- one scene adapted across aspect ratios or camera framings.

Prefer another approach when:

- a 2D compositor can express the result more clearly and cheaply;
- the job is to prepare a mesh for downstream engines rather than compose a shot;
- exact offline path tracing, feature-film simulation, or DCC-native handoff is required;
- a static product render already exists and no 3D revision value remains;
- the target depends on browser interactions rather than a rendered media deliverable.

Do not add a 3D scene merely to make a composition feel expensive. The camera and dimensionality must serve the message.

## Lock the scene contract

Before implementation, define:

- output dimensions, aspect ratios, frame rate, duration, alpha need, and color/HDR expectations;
- shot list with camera, lens/FOV, subject, action, lighting change, and transition at each beat;
- approved assets and their scale, axes, pivot, animation clips, morph targets, materials, and rights;
- material references and color-critical requirements;
- environment, lights, shadows, reflections, background, fog, and post-processing;
- deterministic inputs: seeds, data, animation times, simulation caches, and asset versions;
- performance envelope: browser, GPU/software path, memory, frame size, render workers, and delivery deadline;
- accessibility constraints, especially flashing, rapid camera motion, and reduced-motion variants;
- review gates: graybox, look development, animation, stress frame, encoded proof, and final.

Create a scene manifest mapping stable IDs to files, checksums, transformations, licenses, and scene usage. Freeze remote assets locally before final rendering.

## Scene, camera, and renderer architecture

**Documented fact:** Three.js composes an `Object3D` hierarchy in a `Scene`, views it through a camera, and draws it through a renderer. Child transforms inherit parent transforms. Perspective and orthographic cameras serve different spatial readings.

Structure the scene by production role:

```text
scene
+- world
|  +- environment
|  +- set
|  `- practical-lights
+- subject-root
|  +- approved-model
|  `- subject-controls
+- fx-root
+- camera-rig
|  +- camera-target
|  `- camera
`- review-guides
```

Use stable names and keep camera rigs, subject transforms, imported animation, and procedural effects separate. Avoid modifying deeply nested imported nodes by array index; resolve named nodes once and validate that they exist.

### Camera direction

- Choose perspective for lens-like depth and orthographic for diagrammatic/isometric scenes.
- Define near/far planes tightly enough for useful depth precision without clipping approved motion.
- Animate a rig or target rather than mixing unrelated direct camera mutations.
- Test framing at the actual aspect ratios. A center crop is not a vertical composition plan.
- Keep camera velocity, acceleration, and horizon changes appropriate to the audience and reduced-motion requirement.

## Import and validate glTF ingredients

**Documented fact:** glTF 2.0 describes scenes, nodes, meshes, skins, animations, cameras, PBR materials, textures, and binary resources. Three.js `GLTFLoader` returns loaded scenes and animation clips and supports a documented set of glTF extensions. Core glTF materials use metallic-roughness PBR.

For every imported asset:

1. Validate the source with Khronos glTF Validator.
2. Record required/used extensions and verify loader support.
3. Inspect scene scale, orientation, bounds, pivots, cameras, lights, skins, morph targets, animations, and material count.
4. Check texture color-space annotations and UV/tangent behavior.
5. Compare the asset in a reference viewer and the production scene.
6. Preserve the source package; document any conversion, compression, or material override.

Use Draco or mesh compression and KTX2/Basis texture paths only after checking decoder deployment, target support, visual changes, and startup cost. Compression is a delivery decision, not an automatic quality improvement.

## Color, materials, and lighting

**Documented fact:** Three.js uses a color-management workflow with Linear-sRGB as its working color space. Color textures such as base color and emissive maps require an sRGB color-space annotation; non-color data textures such as normal, roughness, and metalness maps should not be treated as color. Output conversion and tone mapping are renderer concerns.

Color-critical workflow:

- identify each texture as color or data;
- set the renderer output color space intentionally;
- choose and record tone mapping and exposure;
- compare neutral reference values and approved product colors through the complete render and encode chain;
- avoid judging material color under one stylized light only;
- do not bake display conversion twice.

Use physically based materials when lighting response matters. Preserve the intended distinction between dielectrics and metals, and review roughness, normals, clearcoat, transmission, volume, sheen, iridescence, and other extensions only where the asset and target support them.

Lighting plan:

- establish environment/reflection contribution separately from direct lights;
- use a key/fill/rim or motivated practical system only when it supports the visual intent;
- set shadow-casting subjects and receivers explicitly;
- fit each shadow camera/frustum to the useful region;
- tune bias and normal bias against acne and peter-panning;
- test contact and silhouette at final resolution and compression.

Production heuristic: begin with the fewest lights and shadow maps that produce the intended form. Add complexity in response to a visible deficiency, not because more lights sound cinematic.

## Animation systems

Three.js can combine imported clips, scripted transforms, morph targets, cameras, and shader uniforms. Keep one declared owner per property.

### Imported clips and skeletal animation

**Documented fact:** `AnimationMixer` controls `AnimationAction` instances created from `AnimationClip` data. Clips contain keyframe tracks. Actions can loop, crossfade, change weight, and use normal or additive blending.

- Verify clip names, duration, loop intent, root motion, bind pose, and scale.
- Test extreme deformations and transitions, not only the middle of a clip.
- Normalize or preserve root motion deliberately.
- Use crossfades for performance continuity only when the poses and contact constraints permit them.
- Check feet, hands, props, facial morphs, and shadows frame by frame around blends.

### Morph targets

Use morphs for approved shape changes, facial poses, or corrective deformation. Validate that topology and target order match. Clamp or intentionally combine influence values; inspect midpoints for volume loss, self-intersection, and texture stretching.

### Procedural motion

Write procedural state as a pure function of composition time whenever possible:

```js
function applyFrameState(frame, fps) {
  const time = frame / fps;
  subject.rotation.y = baseRotation + time * radiansPerSecond;
  material.uniforms.uTime.value = time;
  cameraRig.position.copy(cameraPath.getPointAt(clamp01(time / shotDuration)));
}
```

This example assumes `clamp01(value)` returns `Math.max(0, Math.min(1, value))` and `cameraPath` is a configured Three.js curve such as a `Curve3` implementation. Validate the actual curve and camera target separately.

Seed particle distributions and noise inputs. Do not accumulate state with `position.x += ...` during frame export because seeking backward or rendering frames out of order will produce the wrong result.

## Deterministic frame rendering

Live preview commonly uses `requestAnimationFrame` and incremental deltas. Fixed media capture should instead derive the entire scene state from the requested frame.

For each frame:

1. Compute `time = frame / fps` from the composition contract.
2. Set imported animation to that absolute time using the mixer/action strategy supported by the installed version; do not rely on an unknown number of prior `update(delta)` calls.
3. Set camera rigs, procedural transforms, particles, shaders, morphs, and visibility from absolute time or cached deterministic state.
4. Update required world matrices, skeletons, and render targets.
5. Render the scene and post-processing chain once.
6. Read or capture the completed frame through the host renderer.

Example adapter shape:

```js
export function renderAtFrame(frame, fps) {
  const time = frame / fps;
  mixer.setTime(time);
  applyFrameState(frame, fps);
  scene.updateMatrixWorld(true);
  composer.render();
}
```

Check the current `AnimationMixer` semantics before using `setTime()` with non-unit mixer time scale. The principle is absolute-time evaluation, not allegiance to one API call.

Do not use wall-clock time, unseeded randomness, live network responses, hidden-tab timing, device orientation, or unconstrained physics during final capture. Bake simulations or define a reproducible fixed-step cache when simulation is essential.

Render the same stress frames in two clean runs and compare them. Exact GPU pixels may vary across backends or hardware; define tolerances and lock the render environment when exact reproducibility is required.

## Shaders and post-processing

Use built-in materials first when they meet the visual requirement. Custom `ShaderMaterial`, raw shaders, node-based shading, and post-processing increase both creative range and portability risk.

For custom shaders:

- record uniforms, coordinate spaces, precision assumptions, and required extensions;
- drive time from composition time;
- clamp unstable math and test edge values;
- compile/prewarm all production variants before frame one;
- capture shader errors and renderer information;
- provide a fallback if the target backend cannot run the effect.

For post-processing:

- specify pass order because effects are not generally commutative;
- budget render-target memory at full delivery resolution;
- inspect bloom, blur, depth of field, grain, and chromatic effects after compression;
- avoid effects that hide asset or material defects;
- check alpha and premultiplication through the final pipeline.

## Performance and resource custody

**Documented fact:** removing a mesh from a scene does not automatically release its geometry, material, texture, or render-target GPU resources. Disposable resources expose `dispose()` methods. Three.js provides renderer memory information for diagnostic use.

Production approach:

- reuse geometry and materials where identity permits;
- use instancing or batching for repeated objects;
- reduce draw calls, material variants, overdraw, transparent layers, and shadow casters before sacrificing the hero silhouette;
- use level of detail only when camera distance makes the substitution invisible;
- size textures for the maximum useful screen coverage;
- dispose replaced geometries, materials, textures, render targets, controls, and post-processing resources;
- remove event listeners and animation loops at teardown.

Measure a representative sequence, not an empty scene. Record load time, first-frame shader compilation, peak memory, render time per frame, readback/capture cost, and encoded output quality.

## Accessibility and viewer safety

**Documented fact:** WCAG 2.2 SC 2.3.1 limits content to no more than three flashes in any one-second period unless below general and red flash thresholds. Evaluate loops while looping and test at the largest intended presentation.

Also review:

- rapid full-field camera movement, rotation, zoom, parallax, and horizon roll;
- flickering shadows, z-fighting, emissive pulses, lightning, particles, and post effects;
- information available only through color, depth, or motion;
- captions and required text over changing 3D backgrounds;
- a reduced-motion render where audience or destination needs it.

For interactive publication, expose motion controls and honor user preferences where applicable. For prerecorded video, produce a separate calmer output because a media query cannot alter already rendered pixels.

## Rights and provenance

Three.js is MIT-licensed, but the scene's dependencies retain their own terms. Record licenses and permissions for models, textures, HDRIs, fonts, shaders, motion clips, mocap, plugins, logos, and reference media. Generated ingredients need provider/model/version/prompt/seed metadata when available.

Do not assume an asset downloaded from a public demo is cleared for commercial reuse. Preserve required notices. If a model depicts a real person, branded product, private location, artwork, or protected character, verify the applicable consent and rights before rendering.

## Render QA and handoff

Review these gates:

- **Structure:** all assets load locally; glTF validation and extension support are documented.
- **Framing:** camera, crop, safe areas, near/far clipping, and aspect variants pass.
- **Look:** color spaces, tone mapping, exposure, materials, reflections, lights, and shadows match approval.
- **Motion:** clips, blends, morphs, procedural state, camera paths, contacts, and loops pass at frame level and normal playback.
- **Determinism:** repeated stress frames and backward seeks match the declared tolerance.
- **Performance:** peak memory and render time fit the production envelope; teardown releases disposable resources.
- **Safety:** flashing and large-field motion review passes or a safer variant is delivered.
- **Output:** frame count, fps, dimensions, alpha, codec, audio sync, and compression pass.

Handoff should include source code, pinned dependencies/lockfile, local assets, scene manifest, render settings, exact command or host entrypoint, representative frame checks, performance notes, provenance ledger, license notices, QA report, and known backend limitations.

## Example 1: color-critical product orbit

This is a complete example, not a mandatory formula.

**Intent:** produce a 12-second 4K orbit of an approved running shoe for a product launch. Material and color fidelity matter more than dramatic effects.

**Inputs and constraints:** validated GLB; approved base-color swatches; two 4K texture sets; licensed studio HDRI; 3840x2160 at 30 fps; H.264 review plus high-quality master frames; no invented logos or geometry.

**Workflow:**

1. Load and inventory the GLB, confirm meter scale, bounds, named materials, UVs, and required extensions.
2. Annotate base-color textures as sRGB and leave normal/roughness/metalness as non-color data.
3. Build a neutral environment plus one broad key and restrained rim; fit a soft contact shadow to the turntable.
4. Lock tone mapping and exposure against approved swatches and a neutral reference card.
5. Keep the shoe static and animate a camera rig through one eased 210-degree orbit; hold the hero three-quarter view for the final two seconds.
6. Evaluate camera and turntable state from absolute frame time.
7. Render frames 0, 1, 90, 180, 299, 300, and 359 twice before the full export.
8. Compare the encoded review against master frames for fine mesh, logo, shadow, and color changes.

**Expected result:** stable geometry and logo, repeatable camera frames, neutral material response, readable contact, and approved color through the final encode.

**Likely failures:** double color conversion, roughness map tagged as sRGB, environment overpowering approved color, near-plane clipping, shader compilation hitch on frame one, and compression damaging knit texture.

**Variation:** for 9:16, author a closer camera path and different final hold rather than cropping the 16:9 orbit.

## Example 2: procedural title world

This is a complete example, not a mandatory formula.

**Intent:** make an eight-second title sequence in which 2,000 instanced columns rise into a city-like word silhouette while a camera passes through it.

**Inputs and constraints:** 1920x1080 at 30 fps; one approved title; no external 3D assets; deterministic seed; restrained glow; reduced-motion alternative; no flashing.

**Workflow:**

1. Convert the approved title mask into a frozen per-instance target-height table using a stored seed and versioned generation settings.
2. Render columns with one instanced geometry/material and per-instance transforms.
3. Drive each height from absolute time, target height, and a deterministic spatial delay; do not mutate cumulative height.
4. Use a camera spline with authored position and look target; cap horizon roll.
5. Apply a subtle bloom pass after the main render and verify pass order and render-target memory.
6. Hold the readable title silhouette for 1.5 seconds.
7. Reduced-motion version uses a stationary camera and shorter column travel.
8. Run full-screen flashing review and repeated stress-frame comparison.

**Expected result:** identical instance layout across renders, no one-frame jumps, readable title, stable camera, and bounded GPU memory.

**Likely failures:** unseeded instance placement, accumulated transforms breaking backward seek, moire in dense columns, excessive bloom, camera clipping, and no readable hold.

**Variation:** if GPU or render-worker limits are tight, pre-render the 3D layer with alpha and composite it in a 2D runtime, retaining the scene manifest and provenance.

## Sources

Official and authoritative sources checked 2026-07-12:

- Three.js documentation and manual: https://threejs.org/docs/ and https://threejs.org/manual/
- Three.js animation system: https://threejs.org/manual/en/animation-system.html
- Three.js color management: https://threejs.org/manual/en/color-management.html
- Three.js cleanup guidance: https://threejs.org/manual/en/cleanup.html
- Three.js `GLTFLoader`: https://threejs.org/docs/#examples/en/loaders/GLTFLoader
- Khronos glTF 2.0 specification: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
- Khronos glTF Validator: https://github.com/KhronosGroup/glTF-Validator
- WebGL 2.0 specification: https://registry.khronos.org/webgl/specs/latest/2.0/
- Three.js license: https://github.com/mrdoob/three.js/blob/dev/LICENSE
- W3C WCAG 2.2, Three Flashes or Below Threshold: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html