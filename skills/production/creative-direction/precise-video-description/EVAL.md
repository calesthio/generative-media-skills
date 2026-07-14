# Precise video description evaluation

Keep this file hidden. Evaluate with the published package only.

## Scoring

Total 100. A score of 85+ without critical failure is production-ready; 70-84 needs focused revision; 50-69 needs major revision; below 50 fails. Any critical failure caps the result at 49.

## Knowledge, 30 points

### 1. Five aspects, 10
Expected: Subject, Scene, Motion, Spatial, Camera with correct boundaries and examples. Penalize treating them as mandatory prose headings or mixing creative intent into observation.

### 2. Reference frames, 8
Expected: distinguish subject-left/right, frame-left/right, world/camera motion, foreground/depth, and camera-facing reversals.

### 3. Camera terminology, 7
Expected: distinguish rotation, translation, zoom, focus change, arc, tracking, and edit transition; avoid exact lens claims without evidence.

### 4. Description boundary, 5
Expected: separate source description from shot direction, creative interpretation, accessibility description/captions, and provider API execution.

## Decisions, 25 points

### 5. Granularity, 8
Choose appropriate detail/time precision for search metadata, VFX handoff, training data, and simple shot logs. Reject universal word-count targets.

### 6. Uncertainty, 8
Given ambiguous tightening and blurred motion, state literal observations, cause of uncertainty, and what evidence would resolve it.

### 7. Glossary governance, 9
Require definitions, decision rules, examples/counterexamples, source/version/owner, and fallback to literal geometry when agreement is poor.

## Applied tasks, 45 points

### 8. Describe a complex shot, 22
Score stable subject naming (3), scene/overlay distinction (3), temporal motion order (4), spatial/reference-frame accuracy (4), camera discrimination (4), uncertainty/objectivity (2), provenance/use metadata (2).

### 9. Repair a flawed description, 15
Find subjective mood, hallucinated identity, wrong left/right, pan-versus-truck confusion, zoom-versus-dolly certainty, omitted overlay, and events out of order. Award two each plus one for coherent rewrite.

### 10. Dataset handoff, 8
Require asset/license/checksum, glossary/schema version, author/model, timestamps, review status, privacy minimization, limitations, and train/use restrictions.

## Critical failures

- hallucinates subjects/actions/intent or exact technical settings;
- confuses subject and frame directions in a consequential way;
- reports camera/edit terminology contradicted by visible evidence;
- turns inference or emotion into observed fact;
- omits privacy/rights restrictions from a dataset handoff;
- claims CHAI's complete unreleased primitive catalog as reproduced in the skill.

Accept equivalent schemas when observation, temporal order, vocabulary, uncertainty, and provenance are sound.