# Procedural Canvas animation evaluation

Keep this file hidden. Evaluate against the published package only.

## Scoring

Total 100. 85+ with no critical failure is production-ready; 70-84 needs focused revision; 50-69 needs major revision; below 50 fails. Any critical failure caps at 49.

## Knowledge, 30 points

### 1. Canvas sizing and reset, 8
Expected: backing bitmap differs from CSS size; dimensions clear pixels/reset context; explicit density; resize rebuild.

### 2. Time, 7
Expected: rAF/frameRate do not define media time; use frame/fps; reject wall-clock state.

### 3. Randomness, 7
Expected: Math.random unseeded/implementation-defined; p5 seeds are scoped and not universal cross-version pixel guarantees; record generator/seed.

### 4. Alpha and CORS, 8
Expected: alpha context, premultiplication, compatible output, background tests, origin-clean requirement, SecurityError risk.

## Decisions, 25 points

### 5. Determinism strategy, 10
Choose stateless, fixed replay, or checkpoints for analytic ribbons, snow, flocking, and persistent trails. Penalize arbitrary access claims without history.

### 6. Performance, 7
Expected: profile/reduce complexity before workers; OffscreenCanvas not automatically faster; measure representative frames.

### 7. Variants and reduced motion, 8
Expected: normalized state, intentional projection/density changes, same event, reduced displacement/density or static output; lower FPS alone is insufficient.

## Applied tasks, 45 points

### 8. Transparent particle overlay, 22
Require contract (3), seeded absolute-frame design (5), bounded trail/compositing (4), alpha/output custody (4), aspect/reduced-motion variants (3), QA/provenance (3).

### 9. Repair a p5 sketch, 15
Find and fix `millis`, `deltaTime`, `frameCount`, window dimensions, resize mutation, unseeded randomness, and opaque/JPEG output. Award two each plus one for coherent frame-zero semantics.

### 10. Safety/accessibility review, 8
Require flash-loop test, meaningful alternative, pause/control for qualifying interactive autoplay, non-color meaning, and host semantics.

## Critical failures

- promises determinism with wall-clock/unseeded state;
- claims persistent trails support random access without replay/checkpoints;
- destroys required transparency or ignores CORS readback;
- claims workers or seeds guarantee universal pixel identity;
- omits flash/reduced-motion/alternative requirements for public autoplay;
- treats Canvas visuals as semantic controls without host accessibility.

Accept equivalent libraries when the bitmap, timing, determinism, safety, and delivery contracts are correct.