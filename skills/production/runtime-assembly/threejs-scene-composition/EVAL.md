# Three.js scene composition evaluation

Keep this answer key hidden. Evaluate against the published package only.

## Scoring

Total: 100 points. A score of 85 or higher with no critical failure is production-ready; 70-84 needs focused revision; 50-69 needs major revision; below 50 fails. Any critical failure caps the result at 49.

## Knowledge

### 1. Scene versus asset production, 6 points

**Question:** Distinguish Three.js scene composition from preparing a web-ready 3D asset.

**Expected:** Asset production owns topology, UVs, baking, LOD construction, and interchange readiness. Scene composition consumes approved assets and owns camera, lighting, environment, animation, shaders/post, deterministic rendering, and shot QA.

**Critical failure:** proposes repairing a broken production mesh only with runtime shaders while hiding the source defect.

### 2. Texture color spaces, 10 points

**Question:** How should base-color, emissive, normal, roughness, and metalness textures be treated?

**Expected:** Base color and emissive are color data and should carry the appropriate sRGB annotation; normal, roughness, and metalness are non-color data. Three.js works in Linear-sRGB and output conversion/tone mapping must be intentional. Avoid double conversion.

**Scoring:** 2 points per correct map class and 2 for coherent working/output conversion, capped at 10.

**Critical failure:** marks a normal or roughness map as sRGB in a color-critical workflow.

### 3. Absolute-time capture, 10 points

**Question:** Why are `requestAnimationFrame`, `Clock.getDelta()`, and cumulative updates insufficient for arbitrary frame capture?

**Expected:** They depend on prior scheduling and frame history. The renderer may request frames out of order. Set animation mixer, camera, shader uniforms, morphs, and procedural state from `frame / fps` or a deterministic cache; seed randomness; verify backward seeks.

**Critical failure:** says setting the preview loop to the target fps guarantees deterministic export.

### 4. glTF intake, 8 points

**Question:** Name the minimum checks before using a GLB in a hero render.

**Expected points:** validator; extensions/loader support; dimensions/axes/pivots/bounds; materials/textures/color spaces; animations/skins/morphs; reference-viewer comparison; provenance/license. Award one point per item, maximum 8.

### 5. Resource disposal, 6 points

**Question:** Why is removing an object from the scene not enough?

**Expected:** GPU-backed geometry, materials, textures, and render targets are not automatically freed merely by scene removal. Dispose owned resources, remove loops/listeners, and avoid disposing shared resources prematurely.

## Production decisions

### 6. Product color mismatch, 10 points

**Scenario:** The shoe looks correct in the asset viewer but washed out in the final video.

**Expected:** Compare loader/material settings, texture color-space tags, renderer output color space, tone mapping/exposure, environment, and encode/display conversion. Use a neutral reference and inspect master frames before changing brand colors.

**Critical failure:** compensates by editing the approved base-color texture without diagnosing the pipeline.

### 7. Physics-driven title render, 8 points

**Scenario:** A title uses live physics and produces different positions in distributed render workers.

**Expected:** Bake/cache the simulation with fixed inputs and step, or replace it with an absolute-time authored motion function. Lock versions/environment and compare stress frames.

**Critical failure:** accepts visual similarity without disclosing nondeterminism when exact edit alignment is required.

### 8. Vertical variant, 7 points

**Scenario:** A 16:9 camera orbit crops the product in 9:16.

**Expected:** Author an aspect-specific camera/framing plan, preserving product and CTA safe areas. Recalculate camera path or subject blocking; do not blind center-crop.

## Applied tasks

### 9. Product-orbit plan, 16 points

**Request:** Plan a 10-second 4K product orbit from an approved GLB with color-critical materials.

**Required:** contract and provenance (2); glTF validation (2); color/PBR plan (3); lighting/shadow plan (2); absolute-time camera/animation (3); stress-frame and encode QA (3); cleanup/handoff (1).

**Critical failures:** no color-space plan, wall-clock capture, unvalidated rights, or no repeated-frame check.

### 10. Procedural scene diagnosis, 12 points

**Request:** Diagnose a scene with unseeded particles, `position += velocity`, `Date.now()` shader time, and a bloom target never disposed.

**Expected:** Seed/freeze particles; derive positions from initial state and absolute time or cache; replace wall-clock shader input with composition time; dispose render targets/passes and verify teardown. Test forward, backward, and clean-run frames.

Award 2 points for each correction and 4 for verification.

### 11. Safety review, 7 points

**Request:** Review a full-screen emissive pulse at 6 Hz plus rapid camera roll.

**Expected:** Treat flashing as blocking unless formally below thresholds; reduce/remove it and test rendered output at largest view. Flag vestibular risk, provide calmer camera/reduced-motion output, and do not rely on a warning alone.

**Critical failure:** approves the scene because it is under ten seconds.

## Evaluation integrity

Do not expose this rubric. Accept technically equivalent renderer-specific implementations when they preserve the production contract, deterministic state, safety, and verifiable output.