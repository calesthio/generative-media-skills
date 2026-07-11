# Evaluation: neural-reality-capture

Do not provide this file to the agent being evaluated. The evaluated agent should receive only the user task and `SKILL.md`. Score whether it can perform provider-independent reality-capture planning, troubleshooting, and handoff reasoning for photogrammetric meshes, NeRFs, and 3D Gaussian splats.

Total: 100 points. Passing: 80. Strong: 90+.

## Critical Failures

Assign a maximum score of 50 if the response does any of the following:

- treats text-to-3D generation as part of this skill's core scope;
- promises survey/metrology-grade accuracy without control, checkpoints, calibration, and error reporting;
- recommends publishing scans of people, private property, restricted cultural sites, or sensitive locations without consent/rights review;
- exposes or links this evaluation file;
- ignores the requested representation and gives only a generic photogrammetry checklist;
- confuses NeRF/3DGS with conventional editable meshes and fails to mention handoff/runtime limitations.

Assign a maximum score of 65 if the response omits rights/privacy/cultural considerations for a scenario involving people, property, aerial capture, or heritage subjects.

## Knowledge Questions

### 1. Representation choice

Question: When should an agent choose a photogrammetric mesh over a NeRF or 3D Gaussian splat?

Expected answer: Choose mesh when explicit editable geometry, UVs/textures, collision, retopology, LODs, 3D printing, conventional engine/DCC import, scale/georeferencing inspection, or GLB/USD mesh handoff are needed. NeRF/3DGS are better for view synthesis and captured appearance, not as primary solid editable geometry.

Required points: mesh editability; runtime/interchange compatibility; scale/geometric inspection; contrast with view-synthesis strengths.

Score: 8 points.

### 2. Original NeRF facts

Question: What are the key original NeRF paper facts relevant to production planning?

Expected answer: NeRF represents a scene as a continuous 5D function of spatial position and viewing direction that outputs density and view-dependent radiance; it optimizes from images with known camera poses; it renders by volume rendering along rays. It is a view-synthesis representation, not a conventional mesh pipeline.

Required points: 5D coordinate; density and radiance; known camera poses; volume rendering; view-synthesis limitation.

Score: 7 points.

### 3. Original 3DGS facts

Question: What facts from the original 3D Gaussian Splatting paper should guide a production agent?

Expected answer: 3DGS starts from sparse points from camera calibration/SfM, represents the scene as optimized 3D Gaussians, performs optimization/density control, and uses visibility-aware splatting for high-quality real-time rendering in the paper's tested settings. It is not a conventional mesh and requires good poses/coverage.

Required points: sparse point initialization; Gaussian representation; optimization/density control; real-time rendering claim constrained to paper context; not a solid mesh.

Score: 7 points.

### 4. Capture fundamentals

Question: Name capture practices that reduce reconstruction/training failure.

Expected answer: fixed exposure/white balance/focus where practical, sharp images, low ISO, adequate shutter, stable lighting, high resolution, sufficient overlap, camera translation/loops rather than a panorama, coarse-to-fine passes, avoid large viewpoint jumps, preserve originals/EXIF, avoid cropping/geometric transforms, mask dynamics, include scale/control when needed.

Required points: at least eight items including overlap, sharpness, exposure/focus stability, motion/loop capture, originals/EXIF, and scale/control.

Score: 10 points.

### 5. glTF facts

Question: What standard facts about glTF/GLB matter for reality-capture handoff?

Expected answer: glTF is a runtime asset delivery format; GLB is binary glTF; glTF 2.0 uses meters and right-handed +Y up, +Z forward orientation; it supports meshes/nodes/materials/textures/buffers/extensions; it uses metallic-roughness PBR with specific color-space expectations; it is not an authoring or streaming format.

Required points: runtime delivery; GLB; units/axis; mesh/material/texture support; not authoring/streaming; extension support caution.

Score: 8 points.

### 6. OpenUSD facts

Question: What makes OpenUSD appropriate for some reality-capture handoffs?

Expected answer: USD is useful for scalable/layered scene description, assets, prims, attributes, relationships, metadata, composition arcs such as subLayers/references/payloads/variants, proxy/render purposes, AssetInfo, validation, and DCC/VFX assembly. It is not a rigging system and does not solve identity with GUIDs.

Required points: layers/composition; assets/references/payloads; variants or purpose/proxy; validation or AssetInfo; limitation.

Score: 8 points.

### 7. Scale and accuracy caveats

Question: What should the agent say when a user asks for "accurate to 1 mm" from casual photos?

Expected answer: It should refuse to guarantee that from casual photos; explain that physical accuracy needs controlled capture, calibration, scale bars/GCPs/control, independent checkpoints, appropriate equipment, and error reporting. It can plan a scaled visual model or recommend a qualified survey/metrology workflow.

Required points: no unsupported guarantee; requirements for control/checkpoints/calibration; alternative plan; qualified caveat.

Score: 8 points.

## Production-Decision Scenarios

### 8. Reflective product showroom

Scenario: A user has 400 phone photos of a glossy motorcycle and wants a browser showroom where viewers can orbit it. They do not need collision or manufacturing geometry.

Expected decision: Recommend testing 3DGS or NeRF for visual free-view appearance, with a mesh baseline only if needed for rough bounds or fallback. Call out reflective-surface risks, masking, controlled recapture if possible, runtime/viewer support, mobile performance, and no solid geometry claim.

Strong answer characteristics: explains why mesh may fail on chrome/glass; asks for or plans held-out-view QA; preserves source archive; documents limitations.

Unsafe/low-quality decisions: promises clean mesh from phone photos; ignores reflections; says GLB is the native deliverable for NeRF/3DGS without conversion/runtime discussion.

Score: 8 points.

### 9. Historic site with public-release restrictions

Scenario: A museum asks for a captured courtyard and mentions restricted inscriptions and Indigenous cultural concerns.

Expected decision: Begin with permissions, cultural consultation, restricted areas, access controls, and redaction plan. Use mesh/USD for controlled archive/handoff and optional private splat/NeRF review if useful. Mask/redact restricted content, avoid public release until approved, archive consent and limitations.

Strong answer characteristics: distinguishes internal master from public derivative; mentions location/property rights; avoids exposing sensitive metadata; includes QA and archive records.

Unsafe/low-quality decisions: recommends immediate public viewer; treats cultural restrictions as only a texture cleanup issue; omits rights packet.

Score: 9 points.

### 10. Ecommerce GLB request

Scenario: A brand needs a 20 MB AR-ready GLB of a fabric chair with correct approximate scale.

Expected decision: Choose photogrammetric mesh, plan studio capture with scale bars, diffuse lighting, fixed settings, solve/clean/decimate/texture/LOD/compress, export GLB in meters with target-viewer QA and no metrology guarantee.

Strong answer characteristics: mentions texture compression, LOD, origin placement, glTF validation/viewer test, and archive of source/master.

Unsafe/low-quality decisions: chooses NeRF as final GLB without mesh conversion; ignores size/LOD; omits scale source.

Score: 8 points.

### 11. Aerial excavation record

Scenario: An archaeology team has drone access and wants a record of an excavation trench for internal analysis and a public education derivative.

Expected decision: Plan nadir plus oblique capture, high overlap, ground-level detail, GCPs/checkpoints/scale bars, coordinate and location-redaction policy, mesh reconstruction, QA with checkpoints, internal master plus redacted public derivative, cultural permissions and archive records.

Strong answer characteristics: separates GCPs from checkpoints; avoids survey-grade claims unless error report supports them; handles exact-location metadata risk.

Unsafe/low-quality decisions: relies only on drone EXIF; omits cultural/location rights; produces one public model with all metadata.

Score: 8 points.

## Applied Production Tasks

### 12. Capture plan task

User request: "I need to scan a 2-meter bronze statue outdoors for a VFX reference asset. I have one mirrorless camera, two hours, and no drone. Make me a capture and handoff plan."

Expected approach: Provide a practical plan with permissions, lighting/time-of-day, fixed camera settings, loops at multiple heights, coarse-to-fine detail, bronze/reflection caveats, scale bars/markers if allowed, masks for bystanders/background, mesh plus optional 3DGS/NeRF visual reference, cleanup bounds, USD/GLB or DCC handoff, QA, archive, and rights notes.

Scoring rubric: 5 capture logistics; 4 reflective bronze risk handling; 4 representation/handoff choice; 3 scale/calibration; 3 QA/archive; 3 rights/safety. Total 22 points.

Critical failures: promises perfect geometry from reflective bronze; ignores property/people permissions; omits scale if VFX placement is requested.

### 13. Troubleshooting task

User request: "My Gaussian splat of an interior has cloudy halos around chairs, holes behind table legs, and ghost people. What should I do?"

Expected approach: Diagnose likely causes: dynamics, under-coverage, thin geometry, exposure/focus/motion issues, weak poses/masks. Recommend reviewing source frames, removing blurry/dynamic frames, masking people, adding recapture passes around occluded/thin areas, improving pose solve, cropping/pruning floaters, retraining, and QA with held-out views. Explain that converting to mesh will not automatically fix the issue.

Scoring rubric: 4 diagnosis; 4 source/mask cleanup; 4 recapture guidance; 3 retraining/pruning; 3 QA and limitations. Total 18 points.

Critical failures: suggests only post-blur or cosmetic cleanup; treats ghost people as acceptable for public delivery without consent; recommends mesh conversion as a magic fix.

## Source and Evidence Discipline

Across all answers, award up to 10 points for evidence discipline:

- 3 points: separates paper/standard/documentation facts from heuristics.
- 2 points: dates volatile standard/tool/runtime facts when making specific claims.
- 2 points: avoids unsupported "best" or universal-default claims.
- 2 points: cites or names authoritative source classes when consequential.
- 1 point: states limitations in plain language.

Deduct these points for marketing-style claims, undated volatile runtime support claims, or treating official guidance percentages as universal guarantees.

## Expected Coverage Summary

A strong evaluated agent can:

- choose between mesh, NeRF, and 3DGS from deliverable constraints;
- plan object, environment/interior, aerial, and people captures;
- manage overlap, exposure, focus, motion, calibration, scale, masks, and dynamics;
- outline reconstruction/training and cleanup without overclaiming;
- select glTF/GLB, USD, or other handoff formats with coordinate/unit awareness;
- run visual, geometric, and delivery QA;
- preserve archival records;
- handle property, location, people, aerial, privacy, and cultural rights;
- exclude text-to-3D, metrology guarantees, and broad downstream finishing.
