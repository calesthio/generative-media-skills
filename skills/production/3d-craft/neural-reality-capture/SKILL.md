---
name: neural-reality-capture
description: Use this skill for provider-independent reality capture that turns photographed or video-derived real places, objects, aerial sites, interiors, or people into photogrammetric meshes, NeRFs, or 3D Gaussian splats. It guides representation choice, capture planning, calibration and scale, reconstruction or training, cleanup, compression and LOD, coordinate and interchange handoff, visual/geometric QA, archival records, and property, location, people, and cultural rights checks. Do not use it for text-to-3D generation, synthetic asset invention, guaranteed metrology, or broad downstream finishing after handoff.
---

# Neural Reality Capture

Neural reality capture is the production craft of reconstructing or rendering a real subject from many overlapping observations. In this skill, the deliverable is one of three families:

- a photogrammetric mesh with textures, usually for game, VFX, GIS, cultural heritage, ecommerce, or DCC handoff;
- a NeRF or related neural radiance field, usually for high-quality novel-view rendering from known camera poses;
- a 3D Gaussian splat scene, usually for real-time free-viewpoint playback with radiance-field appearance.

Stay provider-independent. Choose tools by evidence, constraints, and handoff needs, not by brand habit. Do not promise metrology unless the request includes surveyed control, calibrated capture, uncertainty reporting, and a qualified measurement workflow. Do not expand into text-to-3D, generative resculpting, animation rigging, material lookdev beyond captured handoff, or broad finishing work that belongs downstream.

## Evidence Labels

Use these labels in plans, reviews, and troubleshooting:

- **Paper fact**: a claim from a peer-reviewed paper or original technical report, such as the original NeRF or 3D Gaussian Splatting papers.
- **Standard fact**: a claim from a specification or standard, such as Khronos glTF or OpenUSD documentation.
- **Official documentation fact**: a claim from tool, capture, or production documentation maintained by the relevant organization.
- **Empirical observation**: a result from a documented test or reconstruction run.
- **Production heuristic**: a practical rule that usually improves capture or handoff, but is not a guarantee.

When the user asks for a recommendation, combine fact and heuristic explicitly: "Standard fact: glTF 2.0 uses meters and a right-handed coordinate system. Production heuristic: deliver GLB for lightweight web review and USD for layered VFX or DCC assembly."

## Representation Choice

Choose the representation from the final use, not from capture novelty.

### Photogrammetric mesh

Use a mesh when the asset must be edited, decimated, baked, collision-tested, physically placed, measured with documented caveats, 3D printed, or delivered to engines and DCC tools as conventional geometry.

Strengths:

- explicit topology, UVs, textures, normals, and material channels;
- established interchange through OBJ, FBX, Alembic, glTF/GLB, and USD;
- compatible with cleanup, retopology, collision, LOD, baking, and engine import;
- can be scaled and georeferenced with markers, scale bars, GCPs, or surveyed control.

Risks:

- reflective, transparent, hair-like, thin, repetitive, or textureless surfaces reconstruct poorly;
- topology and UVs are often production-unfriendly until cleaned;
- baked textures can hide geometric defects;
- high accuracy requires controlled capture, calibration, control points, and QA, not only many photos.

### NeRF

Use a NeRF when photorealistic novel-view rendering matters more than mesh editability, especially for bounded inward-facing captures, view-dependent appearance, transparency-like effects, and difficult glossy appearance that a quick mesh bake would mishandle.

Paper fact: the original NeRF paper, *Representing Scenes as Neural Radiance Fields for View Synthesis* (ECCV 2020), represents a scene with a continuous 5D function of spatial location and viewing direction that outputs volume density and view-dependent radiance. It optimizes from input images with known camera poses and renders by differentiable volume rendering along camera rays. Verified 2026-07-11 from the authors' project page and paper.

Strengths:

- strong novel-view appearance for captured radiance;
- handles view-dependent effects better than many naive texture bakes;
- useful for virtual tours, hero renders, volumetric previews, and reference playback.

Risks:

- camera poses and image consistency still matter;
- dynamic objects, exposure shifts, rolling shutter, motion blur, and focus changes become learned artifacts;
- mesh extraction is possible in some workflows but is not the primary representation and may be noisy;
- delivery is less standardized than mesh delivery, and runtime support depends on the target.

### 3D Gaussian splat

Use a Gaussian splat when real-time free-viewpoint playback of a captured scene is the priority and the target viewer supports splats. It is often a strong choice for rooms, streets, cultural sites, products with complex appearance, and location previews where interactive viewing beats editable topology.

Paper fact: the 2023 SIGGRAPH paper *3D Gaussian Splatting for Real-Time Radiance Field Rendering* starts from sparse points produced during camera calibration, represents scenes with optimized 3D Gaussians, includes interleaved optimization and density control, and uses a visibility-aware splatting renderer to achieve high-quality real-time rendering in their evaluated conditions. Verified 2026-07-11 from the authors' Inria project page and paper.

Strengths:

- fast interactive viewing compared with many neural-field renderers;
- strong appearance preservation for complex captured scenes;
- works well when the final deliverable is an immersive viewer rather than editable geometry.

Risks:

- splats are not conventional solid meshes;
- collision, CAD, 3D printing, and DCC editing require conversion or a separate mesh;
- file formats, compression, and engine support are still volatile compared with glTF mesh delivery;
- floaters and semi-transparent halos can be severe around thin, shiny, moving, or under-observed content.

### Quick decision table

| Constraint | Preferred representation | Reason |
|---|---|---|
| Game prop needs collision, retopo, LODs | Mesh | Editable geometry and standard engine pipeline |
| Museum room needs browser-like free-view walkthrough | 3DGS or NeRF | View synthesis preserves captured appearance |
| Architectural survey with GCPs and dimensional checks | Mesh plus survey records | Conventional geometry and QA artifacts are inspectable |
| Reflective retail object for turntable preview | Try NeRF/3DGS, plus controlled mesh capture if needed | View-dependent appearance may beat a quick texture bake |
| Asset must ship as GLB to ecommerce | Mesh | glTF/GLB is runtime asset delivery, not a NeRF container |
| VFX layout wants layered scene assembly | Mesh or point/splat reference in USD package | USD is strong for composition, payloads, variants, and asset references |

## Capture Planning

The capture plan is the cheapest place to prevent reconstruction failure. Start with the target use, subject type, rights, schedule, weather or lighting, scale strategy, and the required deliverable.

### Universal capture requirements

Official documentation fact: COLMAP is a general-purpose Structure-from-Motion and Multi-View Stereo pipeline for ordered and unordered image collections. Verified 2026-07-11 from COLMAP documentation. This means the capture must support camera pose recovery and multi-view correspondence.

Production heuristics:

- Use fixed exposure, fixed white balance, fixed focus when practical.
- Avoid autofocus hunting, zoom changes, rolling-shutter whip pans, motion blur, and image stabilization jumps.
- Keep ISO low enough to preserve fine texture; add light or a tripod instead of accepting noisy, blurred images.
- Shoot RAW or high-quality stills where the pipeline supports them; keep originals unwarped.
- Maintain consistent scale and focal length groups. If a zoom lens changes focal length, split calibration groups by EXIF or capture segment.
- Use diffuse, stable lighting. Avoid moving shadows, specular glare, flash falloff, and screen flicker.
- Capture the subject in loops rather than from one panorama position. A panorama is usually weak for 3D reconstruction because the camera center barely translates.
- Keep each visible surface in at least two high-quality images; more views are better for hard geometry and occlusion.
- Capture coarse-to-fine: establish full-object or full-room loops, then add detail passes while preserving overlap to the broader set.
- Record a capture log while still on site: camera/lens, settings, route, scale references, permissions, weather, lighting, and known blind zones.

Official documentation facts from Agisoft and RealityScan capture guidance, verified 2026-07-11: high resolution is recommended; sharp images matter; low ISO reduces noise; f/8 to f/11 is a common depth-of-field recommendation in Agisoft guidance; slow shutter can create blur; aerial guidance commonly asks for about 80 percent forward and 60 percent side overlap; RealityScan guidance warns not to change viewpoint by more than about 30 degrees between photos and recommends moving around objects in complete loops. Treat these as official capture guidance, not universal physical law.

### Overlap, exposure, focus, and motion

Overlap is not just a percentage. The usable overlap is the part of the subject that is sharp, exposed, textured, and shared with adjacent views.

Production heuristics:

- For objects: shoot at least two or three rings around the subject, plus top and low-angle passes where accessible.
- For interiors: make loops around room boundaries and islands, then add transitions through doorways and occluded corners.
- For exteriors and facades: capture broad establishing passes, oblique passes, and close detail strips.
- For aerial mapping-like capture: start from mission-planning overlap, then increase overlap for vegetation, low texture, oblique facades, altitude variation, or weak GNSS.
- Bracket only if the pipeline can handle or merge brackets predictably. Otherwise choose stable exposure that preserves texture in the subject.
- If motion cannot be controlled, shoot multiple passes and mask or remove moving objects from training/reconstruction.

Reject or isolate photos with heavy blur, clipped highlights on important texture, focus breathing mismatches, rain drops, lens smears, rolling-shutter distortion, people crossing the subject, or heavy JPEG artifacts.

### Object capture

Use object capture for props, artifacts, furniture, food, products, costumes, sculptures, and specimens.

Production heuristics:

- Prefer a textured, matte, non-moving subject on a non-repetitive background unless masking is planned.
- If the object is reflective or textureless, use removable matte spray, cross-polarized light, projected texture, or a NeRF/3DGS-first deliverable when allowed by conservation and rights constraints.
- Capture scale with a ruler, scale bars, coded targets, or a measured turntable scene. Do not put the only scale marker on a surface that may be cropped away.
- If using a turntable, keep camera, lights, and background consistent and understand whether the solver expects the object or camera to move. Mask static backgrounds when the object rotates against them.
- Include underside and contact surfaces only if needed and if you can register them with sufficient overlap.

### Environment and interior capture

Use environment capture for rooms, streets, cultural sites, sets, landscapes, and construction contexts.

Production heuristics:

- Build connected loops. Every side room, hallway, stair, or courtyard needs overlap back to the main path.
- Capture both human-eye height and lower or higher passes for occluded surfaces.
- For NeRF/3DGS, avoid large exposure jumps between windows and interiors; consider separate passes or controlled lighting if the viewer will inspect both.
- Record coordinate intent early: local artistic coordinates, building coordinates, GIS/geospatial, or surveyed control.
- Photograph control points, markers, and scale references clearly from multiple angles.

### Aerial capture

Use aerial capture for roofs, terrain, quarries, facades, industrial sites, agriculture, and large cultural or architectural sites.

Production heuristics:

- Combine nadir and oblique imagery when vertical faces, facades, or overhangs matter.
- Maintain consistent altitude relative to the surface when possible; terrain variation may require adaptive flight planning.
- Place GCPs/checkpoints across the reconstruction area, including edges and elevation changes, when georeferencing or accuracy assessment matters.
- Respect aviation rules, site permissions, privacy, sensitive infrastructure restrictions, and wildlife or cultural-site restrictions before flying.
- Do not present drone EXIF GNSS alone as survey-grade accuracy.

### People and performance capture

Use people capture only with explicit consent, privacy planning, and a clear use. People are difficult because faces, hair, clothing folds, and tiny motion all matter.

Production heuristics:

- Prefer multi-camera synchronized rigs for full-body/head capture; single-camera walkarounds risk expression drift and body sway.
- Use soft, even lighting; avoid blinking highlights and moving shadows.
- Capture neutral pose and expression unless a specific expression is requested.
- Treat biometric data, facial scans, tattoos, distinctive clothing, and minors as high-risk rights and privacy data.

## Calibration, Scale, and Coordinates

A capture without scale is often visually useful but physically ambiguous.

Official documentation fact: Agisoft guidance states that reliable EXIF helps camera autocalibration, that missing EXIF can force assumptions, that fisheye/spherical/cylindrical cameras require appropriate camera type settings, and that cropping or geometrically transforming original images can affect autocalibration. Verified 2026-07-11.

Production workflow:

1. Preserve originals and EXIF. Never overwrite source images.
2. Group cameras by body, lens, focal length, focus setting, sensor mode, and preprocessing state.
3. Add measured scale bars, marker distances, surveyed targets, or GCPs before solving if scale matters.
4. Use checkpoints separate from control points when assessing geometric accuracy.
5. Decide coordinate frame before handoff: local origin, subject-centered origin, building coordinates, GIS CRS, or DCC/engine axis convention.
6. Document unit, up axis, forward axis, origin, scale source, georeferencing source, and any transform applied during export.

Do not say "accurate to X mm" unless the workflow includes independent check data and a measured error report. Say "scaled from two 500 mm bars; no independent accuracy guarantee" when that is the real state.

## Reconstruction or Training Workflow

### Mesh workflow

Typical mesh path:

1. Ingest originals and metadata.
2. Cull unusable images and split camera groups.
3. Detect features and match images.
4. Estimate camera poses and sparse points with SfM.
5. Add or refine calibration, scale, markers, and control.
6. Run dense reconstruction or depth-map estimation.
7. Build mesh or point cloud.
8. Clean, crop, fill only justified holes, decimate, unwrap, and texture.
9. Bake normals, ambient occlusion, displacement, or texture variants only when required by handoff.
10. Validate geometry, texture, scale, coordinates, and package.

Official documentation fact: COLMAP cites *Structure-from-Motion Revisited* (CVPR 2016) and *Pixelwise View Selection for Unstructured Multi-View Stereo* (ECCV 2016) for its SfM and MVS pipeline. Verified 2026-07-11 from COLMAP documentation.

### NeRF workflow

Typical NeRF path:

1. Ingest source images or frames.
2. Estimate or import camera poses.
3. Remove blurred, inconsistent, duplicate, and dynamic-contaminated frames.
4. Define bounds, masks, near/far ranges, and scale normalization.
5. Train with held-out views for QA.
6. Render validation paths and compare with source views.
7. Export the runtime package, rendered video, depth, point cloud, or mesh extraction only if the target supports it.

Paper fact: NeRF needs known camera poses for optimization in the original formulation. If a user only has unordered images, pose estimation is part of the pipeline, not optional magic.

### 3D Gaussian splat workflow

Typical 3DGS path:

1. Estimate camera poses and sparse points, often via an SfM tool.
2. Normalize scene scale and bounds.
3. Train/optimize Gaussians with density control.
4. Inspect for floaters, ghosting, over-transparent edges, background leaks, exposure artifacts, and under-covered holes.
5. Crop, prune, compress, or convert for the target viewer.
6. Package viewer/runtime and preserve source, poses, and training settings.

Paper fact: the original 3DGS work initializes from sparse points produced during camera calibration. Production implication: bad pose estimation or weak sparse reconstruction usually harms the splat.

## Masks, Dynamics, and Difficult Surfaces

Reality capture assumes enough consistent static evidence. Any mismatch becomes noise, ghosts, floaters, smeared texture, or warped geometry.

Use masks when:

- the background moves or contradicts a rotating subject;
- people, vehicles, screens, reflections, vegetation, water, or shadows move through the scene;
- a subject must be separated from a turntable, rig, support, or conservation mount;
- a NeRF or 3DGS should ignore transient occluders.

Production heuristics:

- Mask before reconstruction/training when the masked content would affect camera solve or density.
- Keep masks consistent and feathered only when the tool expects soft alpha. Hard masks are often safer for geometry solvers.
- Do not mask away all shared context needed for pose estimation.
- For reflections, either control them physically or accept that radiance fields may represent view-dependent appearance while meshes may fail.
- For transparent objects, plan special capture or choose a deliverable that does not claim solid geometry.

## Cleanup, Decimation, Compression, and LOD

Cleanup must protect the evidence. Distinguish corrective cleanup from creative alteration.

Allowed within this skill:

- crop to subject or agreed boundary;
- remove floaters, disconnected noise, background fragments, tripod remnants, and masked supports;
- fill small holes when the fill is obvious and labeled;
- decimate with error checks;
- retopologize only enough for handoff when requested;
- generate LODs, normals, texture atlases, and compressed delivery packages;
- preserve an unedited high-resolution master.

After capture-derived delivery, full retopology, UV/PBR rebuilds, skeletal readiness, game LOD authoring, engine import finishing, and production asset packaging belong to `3d-asset-production`.

Out of scope:

- stylized redesign;
- generative replacement of missing evidence as if it were captured fact;
- full game-ready material authoring beyond capture-derived maps;
- rigging and animation.

Production heuristics:

- Keep three tiers: source archive, reconstruction master, delivery derivative.
- For mesh LOD, compare silhouette, normal deviation, texture readability, and scale after every decimation pass.
- For splats, prune floaters and crop bounds before compression; then inspect edge transparency and near-camera behavior.
- For NeRF/3DGS, keep the trained representation and camera path exports separate from any rendered video.

## Coordinates, Interchange, and Delivery

### glTF/GLB

Standard facts from Khronos glTF 2.0, verified 2026-07-11:

- glTF is an API-neutral runtime asset delivery format for 3D content.
- glTF 2.0 uses a right-handed coordinate system, +Y up, +Z forward, and meters for linear distance.
- GLB is the binary container form of glTF.
- glTF defines meshes, nodes, cameras, materials, textures, animations, buffers, and extensions; it is not an authoring format and is not a streaming format.
- glTF 2.0 uses metallic-roughness PBR material parameters; base color textures are sRGB encoded, while metallic-roughness texture values are linear and pack roughness in G and metalness in B.

Use GLB/glTF for web, mobile, ecommerce, game preview, and lightweight review. Include only extensions supported by the target runtime. Record texture sizes, compression choices, coordinate transform, and whether the origin was moved.

### OpenUSD

Standard facts from OpenUSD documentation, verified 2026-07-11:

- USD is a high-performance extensible platform for collaboratively constructing animated 3D scenes and robustly interchanging/augmenting 3D scenes composed from assets.
- USD organizes data into hierarchical prims with attributes, relationships, and metadata stored in layers.
- USD composition includes subLayers, references, payloads, variantSets, inherits, and specializes.
- USD supports asset references, AssetInfo metadata, payload working sets, variants, purposes such as render/proxy/guide, validation, and native crate `.usdc` plus text `.usda` formats.
- USD is not a rigging system and does not use GUIDs as the core identity mechanism.

Use USD when the handoff needs layered assembly, VFX pipeline integration, variants, payloads, asset references, proxy/render separation, or richer scene packaging. Use `usdchecker` or USD validation where available.

### Other handoff formats

- OBJ is simple and widely readable, but weak for materials, units, hierarchy, and modern runtime delivery.
- FBX is common in DCC/game pipelines but has implementation variation; always test import in the target application.
- Alembic is useful for baked geometry or VFX interchange, especially time-sampled geometry, but is not a material-rich runtime package.
- PLY is useful for point clouds, splats in some workflows, and reconstruction diagnostics; do not assume final viewer support.
- E57, LAS/LAZ, GeoTIFF, and related geospatial formats belong in survey/GIS handoffs when requested, but this skill does not make survey-grade guarantees.

## QA: Visual, Geometric, and Delivery

Run QA at the representation level and at the handoff level.

### Visual QA

- Compare rendered views against held-out source images.
- Check seams, texture swimming, ghosting, baked shadows, color shifts, glare, and exposure transitions.
- Inspect under neutral lighting and target lighting.
- For NeRF/3DGS, fly through slowly and inspect disocclusion, floaters, transparent edge halos, and near/far clipping.
- For meshes, inspect shaded, wireframe, normal, UV, texture-only, and scale-reference views.

### Geometric QA

- Check alignment residuals and camera pose outliers.
- Compare control points and independent checkpoints when present.
- Measure known scale bars or object dimensions.
- Inspect topology density, non-manifold geometry, inverted normals, disconnected islands, degenerate triangles, and holes.
- Check coordinate transform, unit, up axis, and origin in the target application.

### Delivery QA

- Open the final package in at least one target viewer, not only the authoring tool.
- Verify textures are linked or embedded as intended.
- Verify required extensions are supported by the target runtime.
- Verify LOD switching, bounds, collision or proxy meshes if included, and package size.
- Verify licenses, permissions, and redactions before publishing.

## Archival Records

Every reality-capture handoff should include enough recordkeeping for future reuse and dispute resolution.

Minimum archive:

- source images/video frames and checksums;
- capture log with date, location, device, lens, settings, route, lighting, permissions, and crew;
- camera calibration groups and pose files;
- scale bars, GCPs, checkpoints, measured distances, CRS/georeferencing notes where applicable;
- masks and dynamic-object notes;
- reconstruction/training software, version, settings, and random seeds when available;
- master model or trained representation;
- delivery derivatives with export settings;
- QA report and known limitations;
- rights packet: property/location release, people consent, cultural permissions, drone/aviation permissions, license terms, and publication restrictions.

Do not bury limitations in vague language. Good archive notes say: "Window wall is visually plausible in 3DGS but not geometrically reliable; moving pedestrians masked; scale set from two bars; no independent checkpoints."

## Rights, Privacy, and Cultural Constraints

Reality capture records real-world facts and therefore carries rights and safety obligations.

Check before capture and before delivery:

- Property and location: ownership, access permission, filming/scanning release, site-specific restrictions, ticket terms, tenant privacy, sensitive infrastructure, security systems, artworks, signage, trademarks, and trade dress.
- People: consent, likeness, biometric implications, minors, workers, bystanders, tattoos, badges, license plates, addresses, and health/safety data.
- Cultural heritage: sacred sites, burial sites, Indigenous cultural property, museum restrictions, conservation limits, repatriation concerns, looting risk, and whether public 3D release could enable harm.
- Aerial capture: aviation rules, no-fly zones, local permits, privacy, geofencing, insurance, and site safety.
- Data handling: encryption, access control, retention period, takedown path, and whether raw captures can be shared with third-party processors.

If rights are unclear, do not publish or train a public viewer from the capture. Offer a restricted internal review package or request releases.

## Complete Examples

### Example: ecommerce chair as GLB mesh


Production intent: a furniture brand needs a web-viewable chair asset accurate enough for appearance and scale in AR, but not for manufacturing.

Inputs and constraints:

- DSLR stills allowed in a studio for four hours.
- Matte fabric, semi-gloss wood legs, no people.
- Web GLB under 25 MB, 3 LODs, 2K textures.
- Must include scale caveat, not a metrology claim.

Recommended workflow:

1. Capture full chair loops at standing, seated, low, and overhead angles with fixed exposure, white balance, and focus.
2. Add two measured scale bars on the floor plane and one visible ruler near leg height.
3. Use diffuse large softboxes and polarizing control if wood glare becomes dominant.
4. Solve SfM/MVS, create high-resolution mesh, clean floor/background, keep master.
5. Retopologize or decimate to LOD0/1/2; bake normal and ambient occlusion only from captured geometry.
6. Export GLB with +Y up, meters, origin centered at floor contact midpoint, compressed textures supported by target viewer.
7. QA in the ecommerce viewer and a neutral glTF validator/viewer.

Why this structure: the final deliverable needs conventional geometry and runtime delivery, so mesh plus glTF/GLB is a better match than NeRF or 3DGS.

Expected result: a visually faithful, scaled chair model for AR/web placement with documented limitations.

Likely failure modes: glossy legs smear, underside is incomplete, fabric weave aliases, LOD silhouette changes too much, GLB texture compression shifts color.

Meaningful variations: if the brand wants a cinematic turntable only, a NeRF/3DGS viewer or rendered path may be tested; if CAD-level dimensions are required, refer to a survey/metrology workflow.

### Example: historic courtyard as USD plus splat review

Production intent: a VFX team needs a historic courtyard for layout and set-extension reference. They want a lightweight interactive viewer for directors and a layered USD package for artists.

Inputs and constraints:

- One day on site, tourists present, no drone permission.
- Cultural site restricts public release and prohibits scanning certain inscriptions.
- VFX handoff prefers USD, but directors want free-view navigation.

Recommended workflow:

1. Confirm location agreement, cultural restrictions, and redaction list before capture.
2. Capture connected loops around courtyard edges, architectural details, doorways, and elevation changes with fixed exposure segments.
3. Place temporary scale references where allowed; record any areas that cannot be marked.
4. Mask tourists and restricted inscriptions before reconstruction/training.
5. Build a mesh for layout/proxy and train a 3DGS for visual free-view review.
6. Package USD with component structure, proxy/render purpose separation, assetInfo, scale notes, and restricted-use metadata in accompanying records.
7. Export a private splat viewer package with access controls and redacted regions.
8. QA both: USD opens in the target DCC and splat viewer shows no restricted details or obvious dynamic ghosts.

Why this structure: USD serves layered VFX assembly; the splat serves fast visual review. Neither replaces rights review.

Expected result: artists receive a scaled layout/reference package, directors get an immersive preview, and publication restrictions are preserved.

Likely failure modes: moving tourists create ghosts, glossy stone produces floaters, restricted inscriptions leak into texture/splat, USD references break after packaging.

Meaningful variations: if later drone permission is granted, add aerial/oblique pass for roofs and upper facades; if public release is required, create a heavily redacted derivative.

### Example: small excavation area with aerial and ground mesh

Production intent: an archaeology team needs a documented 3D record of an excavation trench for internal analysis and educational still renders.

Inputs and constraints:

- Drone permitted at low altitude.
- Ground control and scale bars available.
- Public release must avoid exact location metadata.
- No claim of survey-grade measurement unless checkpoints support it.

Recommended workflow:

1. Capture nadir aerial grid with high overlap, plus oblique passes for trench walls.
2. Capture ground-level close passes around important finds and stratigraphy.
3. Place GCPs/checkpoints around the trench and record coordinate system separately from public derivative metadata.
4. Preserve RAW/stills, EXIF, GCP files, and field notes.
5. Reconstruct mesh, texture, and orthographic renders. Produce a scaled master and a public decimated/redacted GLB if approved.
6. QA with independent checkpoints and known scale distances. Report residuals and limitations.
7. Archive restricted master, public derivative, rights notes, cultural permissions, and location redaction choices.

Why this structure: the deliverable is a record and conventional mesh is inspectable, archiveable, and easy to derive stills from.

Expected result: a scaled internal model with documented control and a lower-risk public derivative.

Likely failure modes: sun movement changes shadows, loose soil lacks texture, trench wall occlusions remain, coordinate metadata accidentally reveals location.

Meaningful variations: if only education visuals are needed, simplify to a visual mesh and skip georeferencing; if legal measurement is needed, bring qualified survey support.

### Example: glossy motorcycle for interactive showroom

Production intent: an agency wants a browser-based interactive capture of a motorcycle with convincing chrome and paint.

Inputs and constraints:

- Object cannot be coated.
- Chrome, black paint, glass, and thin spokes are prominent.
- Final use is visual exploration, not collision or manufacturing.

Recommended workflow:

1. Capture under controlled large-area lighting, avoiding visible crew reflections where possible.
2. Shoot dense loops at multiple heights, with extra passes around spokes, engine, mirrors, and transparent/glossy parts.
3. Record a mesh baseline, but test 3DGS and NeRF early because view-dependent appearance may preserve the subject better than texture baking.
4. Mask crew, rig, turntable, and reflections that break consistency when possible.
5. Deliver private 3DGS viewer if QA shows acceptable floaters and edge behavior; include a simplified mesh only for rough bounds if needed.
6. State that the viewer is visual and not a solid engineering model.

Why this structure: the subject has exactly the surface properties where conventional photogrammetry struggles, while radiance-field style representations may preserve appearance for viewing.

Expected result: convincing interactive visual review with caveats around geometry and reflective surfaces.

Likely failure modes: chrome creates ghost environments, spokes fragment into floaters, glass turns cloudy, viewer lacks mobile performance.

Meaningful variations: for game use, plan a separate modeled/retopologized asset with artist-authored materials.

## Source Notes Verified 2026-07-11

- Mildenhall et al., *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*, ECCV 2020, authors' project page and paper: https://www.matthewtancik.com/nerf.
- Kerbl et al., *3D Gaussian Splatting for Real-Time Radiance Field Rendering*, ACM Transactions on Graphics/SIGGRAPH 2023, authors' Inria project page and paper: https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/.
- COLMAP documentation, project overview and citations for SfM/MVS: https://colmap.github.io/.
- AliceVision/Meshroom official site for open-source photogrammetry software context.
- Agisoft Metashape official image capture tips for resolution, focal length, ISO, aperture, shutter blur, overlap, markers, scale bars, EXIF, camera type, and no geometric image transforms: https://agisoft.freshdesk.com/support/solutions/articles/31000149337.
- RealityScan/RealityCapture official "How to Take Photographs" guidance for loops, viewpoint change, image count, movement, and precision caveats: https://rshelp.capturingreality.com/en-US/tutorials/takingpictures.htm.
- Khronos glTF 2.0 specification, version 2.0.1, for runtime asset delivery, coordinate system, units, GLB, materials, textures, buffers, extensions, and versioning: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html.
- OpenUSD documentation for scene description, layers, prims, attributes, relationships, composition arcs, assets, payloads, variants, validation, and limitations: https://openusd.org/release/intro.html.
