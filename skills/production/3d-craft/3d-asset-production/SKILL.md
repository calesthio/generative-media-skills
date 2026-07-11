---
name: 3d-asset-production
description: Use this skill to turn generated, captured, scanned, or modeled 3D output into production-ready standalone assets for DCC, real-time engine, web, or interchange delivery. It covers requirements, topology repair, scale and axes, UVs, PBR baking, LODs, static and skeletal readiness, rig handoff, optimization, glTF/USD/FBX delivery, validation, QA, and rights/provenance. Do not use it for provider-specific generation prompts, full scene/world building, mocap operation, or exact CAD/manufacturing work.
---

# 3D Asset Production

This skill is for finishing an asset so another artist, engine, viewer, marketplace, configurator, game, AR app, or renderer can actually use it. The input may be generated mesh output, photogrammetry, NeRF/GSplat-derived mesh, scan cleanup, sculpt, CAD-derived polygon export, hand-modeled geometry, or a kitbashed draft. The output is a documented, validated asset package with predictable geometry, scale, materials, texture maps, LODs when needed, and provenance.

Use it when the user asks for asset prep, retopology, cleanup, optimization, baking, UVs, PBR textures, LODs, rig handoff, static mesh delivery, skeletal mesh readiness, game-ready assets, web-ready assets, GLB/glTF/USD/FBX export, DCC-to-engine delivery, or QA of a 3D model.

Do not use it for:

- Choosing or prompting a specific 3D generation provider.
- Building a whole environment, shot, level, or composed scene.
- Running motion-capture sessions or solving mocap performances.
- Exact CAD, toleranced manufacturing, BIM compliance, or simulation-grade engineering geometry.
- Character performance direction, although this skill can prepare a mesh for rigging or animation handoff.

## Start With The Delivery Contract

Before touching topology, define the asset's consumer. A beautiful mesh is still a failed delivery if the receiving engine cannot load its textures, its unit scale is wrong, or the rigging team cannot bind it.

Ask for or infer these requirements:

- Asset role: hero prop, background prop, avatar body, modular garment, weapon, vehicle, scan archive, AR product, web configurator item, cinematic asset, marketplace asset, mobile asset.
- Target consumers: Blender, Maya, Houdini, Unreal, Unity, WebGL/three.js/Babylon, USD pipeline, DCC handoff, custom runtime, marketplace.
- Format set: source DCC file, `.glb`/`.gltf`, `.usd`/`.usda`/`.usdc`/`.usdz`, `.fbx`, texture archive, preview renders, validation report.
- Runtime budget: triangle count, vertex count, material count, draw-call/submesh target, texture resolution, compressed texture formats, LOD count, memory/download size, supported extensions.
- Spatial contract: real-world dimensions, unit system, axis/up convention, pivot, origin, bounds, snap points, socket points.
- Material contract: PBR workflow, color space, texture channel packing, transparency mode, normal tangent basis, renderer-specific shader expectations.
- Animation contract: static mesh, skeletal mesh, blend shapes/morph targets, cloth/hair handoff, deformation range, max bone influences, root bone, naming convention.
- Rights contract: input source, user rights, third-party references, scan consent, generated-output terms, trademarks/logos, attribution, license, distribution region.

Treat unknown target requirements as a risk, not as permission to guess. If the user cannot specify budgets, create a defensible baseline and label it as a proposed budget.

## Evidence Classes

This skill uses three kinds of claims:

- Documented facts are statements from official specifications, vendor manuals, standards, or project documentation. They are cited in the source notes.
- Empirical observations are repeatable production findings that should be verified on the user's actual asset and target runtime.
- Production heuristics are practical defaults. They are not universal rules; change them when the delivery contract says otherwise.

## Documented Facts To Anchor Decisions

- glTF 2.0 is an API-neutral runtime asset delivery format, not an authoring format. It represents scene descriptions with JSON plus binary buffers and image resources, or as GLB for a single binary container. Source: Khronos glTF 2.0 specification, verified 2026-07-11, https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html.
- glTF uses a right-handed coordinate system with +Y up, +Z forward, -X right, and meters for linear distances. Source: Khronos glTF 2.0 specification, verified 2026-07-11.
- glTF material core is metallic-roughness PBR. Base color textures are sRGB; metallic-roughness texture data is linear, with roughness in green and metalness in blue. Normal textures are tangent-space and linear. Source: Khronos glTF 2.0 specification, verified 2026-07-11.
- glTF skinning uses linear blend skinning with `JOINTS_n` and `WEIGHTS_n` attributes; one joint/weight set gives up to four influences per vertex, and `JOINTS_n` and `WEIGHTS_n` sets must match. Source: Khronos glTF 2.0 specification, verified 2026-07-11.
- glTF node transforms can use either a matrix or TRS. Animated nodes must not use `matrix`; animations target translation, rotation, scale, or morph target weights. Source: Khronos glTF 2.0 specification, verified 2026-07-11.
- glTF Validator validates JSON/GLB correctness, internal references, binary buffers, forbidden accessor values such as NaN, accessor bounds, sparse accessors, animation data, images, and several extensions. Source: KhronosGroup/glTF-Validator README, verified 2026-07-11, https://github.com/KhronosGroup/glTF-Validator.
- USD is designed for scalable interchange, composition, layering, overriding, and organization of 3D scene description across DCC pipelines. USD can represent models, geometry, shading, animation, primvars, payloads, references, variants, and asset metadata. It is not itself a high-performance rigging system. Source: OpenUSD Introduction, verified 2026-07-11, https://openusd.org/release/intro.html.
- Unreal Engine's FBX pipeline imports static meshes, skeletal meshes, animation, morph targets, materials, textures, and multiple LODs, and Unreal documents that its FBX import pipeline uses FBX 2020.2; exporting with a different FBX version may cause incompatibilities. Source: Unreal Engine FBX Content Pipeline, verified 2026-07-11, https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-content-pipeline.
- Unreal skeletal mesh assets contain visual mesh geometry and skeleton bone data; they are usually authored in external DCC software and imported as FBX. Source: Unreal Engine Skeletal Meshes documentation, verified 2026-07-11, https://dev.epicgames.com/documentation/en-us/unreal-engine/skeletal-mesh-assets-in-unreal-engine.
- Unity model files can contain meshes, animation rigs/clips, materials, and textures. Unity's primary model-file support is FBX; Unity recommends direct FBX export from the DCC into the project in most cases. Source: Unity Manual, Importing a model, verified 2026-07-11, https://docs.unity3d.com/Manual/ImportingModelFiles.html.
- Unity rig import settings distinguish None, Legacy, Generic, and Humanoid animation types. For generic rigs, Unity needs a root node; skin weights affect per-vertex bone influence count and performance. Source: Unity Manual, Rig tab Import Settings reference, verified 2026-07-11, https://docs.unity3d.com/Manual/FBXImporter-Rig.html.
- meshoptimizer provides mesh indexing, vertex cache optimization, overdraw optimization, vertex fetch optimization, quantization, simplification, compression, analyzers, and glTF-related tooling. Its recommended core pipeline orders indexing before cache optimization, optional overdraw optimization, fetch optimization, quantization, filtering, and optional shadow indexing. Source: meshoptimizer README, verified 2026-07-11, https://github.com/zeux/meshoptimizer.

## Production Heuristics That Usually Hold

- Finish the asset against the weakest target, not the strongest DCC. If a mobile WebGL viewer and Unreal are both targets, the web budget usually constrains geometry, material count, extensions, and texture sizes.
- Preserve an editable source file and export a runtime derivative. Do not make GLB/FBX/USDZ the only source of truth unless the user explicitly wants a flat interchange package.
- Separate semantic meshes only when downstream operations need it: material assignment, sockets, destructibility, animation, collision, occlusion, user customization, or culling. Splitting everything by generated fragments usually damages runtime performance and asset usability.
- Prefer indexed triangle meshes for real-time delivery unless the target specifically requires another topology. Keep curves, subdivision, hair, procedural modifiers, and high-poly sculpt data in the source package, not the runtime export, unless the consumer supports them.
- Bake detail from high-poly/generated/scanned source to a clean low/mid-poly render mesh. Runtime assets should usually carry high-frequency detail in normal, ambient occlusion, curvature/cavity, and material maps rather than in noisy dense topology.
- Protect silhouette, deformation zones, contact surfaces, sockets, and UV/material boundaries during simplification. Let interior flat regions and visually hidden backs reduce first.
- For deformation, regular edge flow and stable weights matter more than raw triangle count. A slightly heavier mesh with clean loops can animate better than an aggressively decimated mesh.
- For hero assets, verify by import into the actual target engine/viewer. Validator success is necessary but not enough for visual parity.

## Intake Triage

Classify the source before deciding the repair path.

### Generated Mesh Output

Common traits: uneven tessellation, fused parts, non-manifold pockets, noisy normals, arbitrary scale, missing UV intent, baked colors instead of material logic, plausible silhouette with weak mechanical construction.

Best path:

1. Freeze a source archive and record generation provider/model/settings if known.
2. Decide whether the mesh is a concept reference, a high-poly bake source, or a direct cleanup candidate.
3. If topology is chaotic but shape is valuable, retopologize rather than decimate-only.
4. Rebuild UVs and PBR maps from the approved surface appearance.
5. Validate by import, not by visual inspection in the generator's viewer.

### Captured Or Scanned Output

Common traits: high density, holes, scan shadows, texture-lighting baked into albedo, fragile thin surfaces, scale drift, scan table/floor debris.

Best path:

1. Preserve raw scan/photogrammetry source.
2. Establish real scale from a measured feature or calibration object.
3. Remove debris and reconstruct missing geometry only where physically justified.
4. Build clean retopology or optimized decimation depending on role.
5. De-light textures if the asset must respond to new lighting.

### Modeled Or Sculpted Output

Common traits: cleaner intent, possible unapplied transforms/modifiers, hidden high-poly details, overlapping UV shells, unsupported procedural materials.

Best path:

1. Apply/export only intentional transforms and modifiers.
2. Keep authoring file with non-destructive layers where useful.
3. Bake high-poly or procedural detail to maps for runtime targets.
4. Validate normals, tangents, UV sets, pivots, and unit scale after export.

### CAD-Derived Polygon Output

Common traits: exact design intent but unsuitable tessellation, many parts/material IDs, tiny bevels, n-gon/trim conversion artifacts, real-world units.

Best path:

1. Do not claim manufacturing exactness after polygon conversion.
2. Retain CAD as provenance/reference if licensed.
3. Tessellate with chord/angle tolerances appropriate to the viewing distance.
4. Merge or instance repeated parts where runtime permits.
5. Rebuild materials as renderable PBR approximations.

## Geometry And Topology Repair

The goal is not a theoretically perfect mesh; it is a mesh whose topology supports the intended rendering, deformation, collision, LOD, and editing tasks.

Minimum repair checklist:

- Remove duplicate vertices where they are not required for UV, material, hard-normal, tangent, color, or skinning boundaries.
- Delete hidden debris, isolated fragments, accidental internal shells, and zero-area or near-zero-area triangles.
- Resolve non-manifold edges, self-intersections, flipped normals, open holes, and inconsistent winding according to asset intent.
- Preserve hard-surface support loops or bevels that define silhouette and specular response.
- Avoid long skinny triangles in deformation areas and high-specular surfaces.
- Keep material boundaries and UV seams intentional, named, and documented.
- Use normals deliberately: flat for planar mechanical surfaces, smoothed for continuous curved surfaces, custom/weighted normals when they are part of the shading design.

Retopology decision:

- Retopologize when the asset must deform, receive clean bakes, support predictable LODs, use mirrored/symmetrical UVs, or survive close camera inspection.
- Decimate when the asset is static, scanned, mostly organic, non-deforming, and the source detail is more important than editability.
- Re-model when the source is visually plausible but physically incoherent, such as generated machinery with fused impossible parts.

Topology QA:

- Inspect wireframe over shaded view from close and far distances.
- Check silhouette at target FOV and distance.
- Test smoothing under high-contrast HDRI or studio lights.
- Confirm no surface tears after export/import round trip.
- For deforming assets, test extreme bend/twist poses before signoff.

## Scale, Axes, Origin, Pivots, And Naming

Scale errors are expensive because they propagate into physics, animation, camera framing, lighting, AR placement, and UI fit.

Set and document:

- Unit basis: meters, centimeters, or target-engine units.
- Real dimensions: bounding box and key measured dimensions.
- Orientation: up axis, forward axis, front-facing convention, and any format conversion.
- Pivot/origin: bottom center for props that sit on surfaces, center of mass for physics props, hinge point for doors/wheels, grip point for weapons/tools, root at floor between feet for characters unless target says otherwise.
- Transforms: freeze/apply scale and rotation before export unless the target pipeline needs authored transforms.
- Naming: stable ASCII names for objects, materials, bones, sockets, UV sets, textures, and LODs. Avoid autogenerated gibberish and duplicate material names.

For glTF delivery, remember the documented coordinate and unit contract: right-handed, +Y up, +Z forward, meters. If the authoring DCC or engine uses a different convention, explicitly test the exporter/importer conversion.

## UV Strategy

UVs are a delivery system for texture resolution, seams, baking, and material reuse.

Choose UV layout by asset role:

- Unique hero asset: non-overlapping UV0 for baked PBR maps, consistent texel density, shells aligned for paintability, seams hidden on backs/creases/material breaks.
- Tiled material asset: UV0 can use repeatable coordinates; create a second non-overlapping UV set for lightmaps or baked masks if required by the engine.
- Mirrored character or prop: mirroring is acceptable for symmetric albedo/roughness but risky for readable logos, asymmetrical damage, tangent-space normal maps, and baked AO. Split or offset mirrored areas as needed.
- Modular kit part: snap-friendly UVs, consistent texel density across modules, trim sheets when the project already uses them.
- Scan-derived asset: unwrap for stable reprojection; clean baked lighting or shadows from albedo if relighting is required.

UV QA:

- No unintended overlaps in a bake UV set.
- Adequate padding for the final mip chain and texture resolution.
- Consistent texel density for surfaces viewed together.
- Seams placed where geometry, material, or visibility already hides them.
- Checker texture shows no severe stretching, flipped islands, or mis-scaled shells.
- Target engine recognizes every UV set required by materials, lightmaps, decals, or runtime effects.

## PBR Materials, Baking, And Texture Packaging

Build material output from the target shading model, not from whatever the source happened to contain.

Common PBR map set:

- Base color/albedo: surface color only, no baked direct lighting unless the target intentionally wants a lit texture.
- Normal: tangent-space for real-time assets unless the target requests object/world-space normals.
- Roughness: micro-surface response; keep plausible variation, avoid using it as a generic dirt map.
- Metallic: usually binary by material region for real metals versus dielectrics; avoid gray metalness as a casual blend unless representing mixed texels or a target-specific material.
- Ambient occlusion: indirect-occlusion multiplier or mask; do not bake hard direct shadows into albedo.
- Emissive: authored glow color/intensity, not a lighting substitute unless target shader is unlit.
- Opacity/alpha: choose cutout/mask or blend intentionally because sorting and depth behavior differ.

Baking sequence:

1. Lock the low-poly mesh, smoothing groups/custom normals, UVs, and cage before final bakes.
2. Bake normal, AO, curvature, thickness, position, ID/material masks, and any height/displacement needed for texturing.
3. Check skewing, waviness, projection misses, cage intersections, and mirrored tangent seams.
4. Re-bake after topology, UV, or normal changes; do not patch a normal map to hide a changed mesh unless the change is purely local and verified.
5. Export maps with documented color space and channel packing.

glTF-specific material delivery:

- Use metallic-roughness as the base interchange material when delivering glTF/GLB.
- Pack roughness in G and metallic in B for the core `metallicRoughnessTexture`.
- Treat base color and emissive as sRGB inputs; normal, occlusion, metallic, and roughness data are linear according to glTF rules.
- Record any required glTF extensions. Do not mark extensions as required unless the asset cannot load/render acceptably without them.

Material QA:

- Test under at least one neutral HDRI and one direct/key light setup.
- Compare source and exported render side by side in the target renderer.
- Check tangent-space normal orientation, especially green-channel convention and mirrored UV seams.
- Verify that transparent materials sort acceptably in the intended target.
- Confirm that texture filenames and material slot names survive import.

## LODs And Optimization

LOD work is not only triangle reduction. It is controlled visual loss with stable material, tangent, skinning, and collision behavior.

LOD planning:

- Define the target platform and screen-size thresholds before generating LODs.
- Choose whether LODs share materials and textures, use atlas variants, or collapse material slots at distance.
- Preserve silhouette longer than interior surface detail.
- For skeletal assets, protect joints, face/hands, attachments, and cloth boundaries.
- For modular assets, avoid cracks between neighboring parts by locking shared boundaries or simplifying combined groups.

Optimization order for real-time meshes often follows this logic:

1. Clean/weld topology and index the mesh.
2. Finalize UVs, normals, tangents, vertex colors, material IDs, and skin weights.
3. Generate LODs or use asset-specific manual LODs for hero/deforming meshes.
4. Optimize index order for vertex cache and vertex fetch where the runtime benefits.
5. Quantize or compress only after visual validation at target distance.
6. Validate in the target engine or viewer after compression/extension use.

Heuristic budgets depend heavily on camera distance, platform, shader cost, and project style. If the user has no budget, propose ranges rather than universal counts:

- Web/mobile background prop: prioritize single material, small textures, aggressive LODs, and GLB size.
- Web/mobile hero product: preserve silhouette and material quality; reduce hidden/internal geometry and texture count first.
- PC/console hero prop: allow more geometry for silhouette and bake quality, but still constrain material slots and texture memory.
- Cinematic/offline asset: keep high-resolution source and USD/material handoff; runtime compression may be irrelevant.

Use analyzers and target profiling when available. meshoptimizer's analyzers can estimate vertex cache, vertex fetch, and overdraw behavior, but its own documentation notes that precise performance must be measured on target GPU.

## Static Mesh Readiness

A static mesh package should be ready to place, instance, collide, light, and render.

Static readiness checklist:

- Correct scale, orientation, pivot, and transforms.
- Clean mesh with no accidental non-manifold render artifacts.
- Intentional material slots and material names.
- UV0 for surface textures; additional UVs for lightmaps, masks, decals, or target-specific requirements.
- Collision mesh or collision notes if the engine should generate it.
- LODs with stable material slot mapping.
- Socket/attachment markers if needed.
- Bounds and origin suitable for culling and placement.
- Preview thumbnail/render and import notes.

## Skeletal Mesh And Rig Handoff Readiness

This skill prepares assets for rigging or import; it does not replace a rigger.

Skeletal readiness checklist:

- Mesh topology supports deformation loops around shoulders, elbows, knees, mouth, eyes, fingers, cloth folds, and mechanical hinges.
- Symmetry is intentional; asymmetrical geometry is clearly named and placed.
- Bone naming, hierarchy, root, scale, and orientation follow the receiving rig standard.
- Bind pose/rest pose is documented and exported.
- Skin weights are normalized, non-negative, and within target influence limits.
- No accidental weights on hidden debris or helper meshes.
- Blend shapes/morph targets have matching topology and names that survive export.
- Corrective shapes, wrinkle maps, cloth/hair cards, sockets, and attachment points are named and delivered.
- Deformation tests include maximum expected pose range, not just an A/T-pose.

For glTF skinning, check that `JOINTS_n` and `WEIGHTS_n` sets are paired, joint indices are valid, and weight sums are valid for the chosen component type. For Unity, decide None/Generic/Humanoid and root node behavior. For Unreal, validate FBX skeletal import, Skeleton asset creation, morph target import if needed, and animation compatibility.

Rig handoff package:

- Clean mesh source file with bind pose.
- Separate high-poly/sculpt source if used for bakes.
- Texture maps and material definitions.
- Bone/mesh naming guide.
- Deformation notes and known problem areas.
- Export settings and target engine import settings.
- Validation screenshots from DCC and engine.

## Format Selection And Interchange

Pick formats by what must survive, not by popularity.

### glTF / GLB

Use when the asset is meant for runtime delivery, web, AR preview, lightweight exchange, or broad viewer compatibility. Prefer `.glb` for single-file handoff and `.gltf` with external resources when texture/buffer separation helps asset management.

Strengths:

- Compact runtime asset delivery.
- Defined coordinate/unit/material behavior.
- PBR metallic-roughness baseline.
- Good web/viewer ecosystem.
- Validation tooling.

Risks:

- Not an authoring format; many DCC-specific modifiers, shaders, constraints, and procedural systems will not survive.
- Extension support varies by viewer.
- Rig and animation behavior may import differently across engines.

### USD / USDZ

Use when the asset belongs in a composed DCC/film/VFX pipeline, needs references, variants, layers, payloads, primvars, material networks, or AR platform packaging via USDZ.

Strengths:

- Strong composition and override model.
- Scales to large production pipelines.
- Can encode models, geometry, shading, animation, asset metadata, references, variants, and payloads.
- Useful as a high-fidelity production interchange layer.

Risks:

- USD is not a universal rigging system.
- Renderer and DCC support for material networks and schemas varies.
- Namespace changes can break downstream overrides; stable prim paths matter.

### FBX

Use when the target DCC/engine pipeline expects FBX for static meshes, skeletal meshes, animation clips, morph targets, or legacy interoperability, especially Unity and Unreal workflows.

Strengths:

- Common DCC/engine bridge.
- Carries meshes, skeletons, animation, blend shapes/morph targets, materials/textures to varying degrees.
- Unreal and Unity both document FBX-centered model import workflows.

Risks:

- Version and exporter differences matter. Unreal documents FBX 2020.2 for its pipeline.
- Material translation is often approximate; always test in the target engine.
- Axis, unit, pre/post rotation, and animation bake settings can cause subtle import errors.

### Source DCC Package

Use when the user needs future edits. Include `.blend`, `.ma`/`.mb`, `.max`, `.hip`, `.c4d`, `.spp`, `.ztl`, or project-native files only when licensing and recipient tooling permit.

Strengths:

- Preserves authoring layers, modifiers, high-poly sources, rigs, procedural materials, and editable context.

Risks:

- Less portable than interchange formats.
- May require commercial software or plugins.
- Can accidentally include unused references or licensed assets.

## Delivery Package Pattern

For a production-ready standalone asset, deliver a package like:

- `source/`: editable source file(s), high-poly source, bake cages, sculpt or scan reference if permitted.
- `export/`: final `.glb`, `.gltf`, `.usd`/`.usdz`, `.fbx`, or target-specific import files.
- `textures/`: final maps with clear names, resolution, color space, and channel packing.
- `previews/`: neutral renders, wireframe, UV checker, engine/viewer screenshots.
- `docs/`: readme, dimensions, budgets, coordinate conventions, export/import settings, rights/provenance, known limitations.

If the user explicitly requests only two files or a single final asset, still preserve the same information inside a readme section, asset metadata, or response summary as appropriate.

## Validation And QA

Validation has three layers: structural, visual, and production-use.

Structural validation:

- File opens in the intended DCC/engine/viewer without errors.
- glTF/GLB passes glTF Validator with no errors and only accepted warnings.
- USD opens in `usdview` or the target USD consumer; prim paths, variants, references, payloads, and material bindings resolve.
- FBX imports into the exact target engine version with correct scale, normals, UVs, material slots, skeleton, morph targets, and animation settings.
- Texture links are relative or packaged as required.
- No missing files, absolute local paths, hidden dependencies, or unsupported extensions.

Visual validation:

- Compare source, DCC export, and target import under matched camera and lighting.
- Inspect close-up bakes, silhouettes, hard edges, transparency, decals, emissive materials, and mirrored areas.
- Check UV checker and texture density.
- Verify LOD transitions at target distances.
- For scans, verify that albedo is not carrying unwanted shadows/highlights when relighting is expected.

Production-use validation:

- Place the asset in a clean target project.
- Test pivot placement, scale, snap behavior, sockets, and bounds.
- Test collision if required.
- Test memory/download/build size against budget.
- Test animation deformation, root behavior, retargeting, and morph targets if skeletal.
- Re-import from the delivered package on another machine or clean workspace.

Common disqualifying failures:

- Wrong real-world scale or axis orientation.
- Missing textures due to absolute paths.
- Non-manifold or self-intersecting render artifacts visible in target.
- Materials rely on unsupported procedural/shader features without baked fallback.
- Normal map tangent mismatch causing seams or inverted lighting.
- Texture color spaces are wrong.
- LODs reorder material slots or pop severely.
- Rig weights exceed target limits or are not normalized.
- No rights/provenance record for scanned/generated/third-party inputs.

## Rights, Consent, And Provenance

Every asset needs a production provenance record.

Record:

- Source type: generated, scanned/captured, modeled, purchased, client-provided, open asset, internal library, CAD-derived.
- Source owner and license or terms.
- Generation provider/model/settings and date, if generated.
- Capture location/date and consent/release status, if scanned from real property, person, artwork, branded product, or private space.
- Third-party references, trademarks, logos, labels, distinctive product shapes, and any clearance status.
- Human likeness, biometric, or personal-data issues if the asset depicts a person.
- Modifications performed: retopo, texture repaint, material rebuild, decimation, format conversion, optimization.
- Redistribution permissions and attribution requirements.

Do not remove copyright notices, creator metadata, or license files just to make the package cleaner. If provenance is incomplete, label the asset as not cleared for distribution.

## Example: Generated Chair To Web-Ready GLB

This is an example, not a required formula.

Production intent: Convert a generated modern lounge chair mesh into a web product configurator asset.

Inputs and constraints:

- Source: generated OBJ with 280k triangles, vertex colors, no usable UVs.
- Target: WebGL viewer using GLB, target download under 8 MB, two color variants, product height 0.82 m, static mesh.
- Required: one GLB per variant, neutral preview renders, provenance note.

Workflow:

1. Archive source OBJ and record generator, prompt, seed/settings, and date if available.
2. Measure target dimensions; scale model so chair height is 0.82 m and seat sits on floor plane.
3. Rebuild topology as static low-poly mesh with clean silhouette and separate cushions/frame only if material separation requires it.
4. Remove interior hidden surfaces and fused debris under cushions.
5. Create UV0 with non-overlapping shells, consistent texel density, seams hidden under cushion edges and frame backs.
6. Bake normals and AO from original high-poly source onto cleaned mesh.
7. Author PBR material: fabric base color, roughness variation, metal frame metallic=1, roughness adjusted by reference images.
8. Pack glTF metallic-roughness texture with roughness in G and metalness in B; export base color as sRGB and data maps as linear.
9. Generate LOD1/LOD2 or rely on runtime simplification only if viewer supports it; test transitions if included.
10. Export GLB and validate with glTF Validator.
11. Open GLB in the actual web viewer and inspect scale, material response, texture seams, and file size.

Expected result:

- A GLB that loads without errors, appears at correct scale, has clean PBR fabric/metal materials, and preserves the product silhouette within the download budget.

Likely failure modes:

- Generated mesh has physically impossible cushion intersections that require manual re-modeling.
- Vertex-color appearance cannot be converted directly to clean albedo, requiring texture repainting.
- Aggressive simplification damages chair legs or cushion seams.
- Viewer lacks a glTF extension used by the exporter.

Meaningful variations:

- For AR, add stricter real-scale verification and platform-specific USDZ if required.
- For desktop hero view, increase texture resolution and preserve bevel detail.
- For a large product catalog, standardize pivots, naming, texture packing, and material variants across all chairs.

## Example: Photogrammetry Statue To Engine Prop

This is an example, not a required formula.

Production intent: Convert a photogrammetry statue scan into a static Unreal and Unity prop.

Inputs and constraints:

- Source: 22M triangle scan with 16k diffuse texture, uneven lighting, holes under overhangs.
- Target: FBX plus textures for Unreal/Unity, 3 LODs, collision proxy, base height 1.4 m.
- Required: no exact museum-copy licensing claim; internal visualization only until rights are cleared.

Workflow:

1. Preserve raw scan, camera set, and reconstruction metadata.
2. Confirm capture permissions and label redistribution status as internal-only if clearance is missing.
3. Establish scale from measured plinth height; set pivot at bottom center of plinth.
4. Remove floor/table artifacts and fill holes where the statue should be continuous.
5. Build a clean render mesh by retopology or controlled decimation, protecting face, hands, silhouette, and carved edges.
6. Create UV0 for baked maps and UV1 for lightmaps if the target engine/project requires it.
7. De-light diffuse texture or repaint base color to remove capture shadows and highlights.
8. Bake normal, AO, and curvature from scan to render mesh.
9. Generate LODs with silhouette preservation and validate transitions in both engines.
10. Build simple convex or custom collision proxy that matches plinth/body enough for gameplay.
11. Export FBX using target engine settings; import into clean Unreal and Unity projects and capture screenshots.

Expected result:

- A static prop package with correct scale, stable materials, collision, LODs, and documented internal-use rights status.

Likely failure modes:

- Baked lighting remains in base color and looks wrong under engine lighting.
- Thin fingers or carved edges collapse in LODs.
- FBX import uses wrong unit conversion, making the statue 100x too large or small.
- Unity/Unreal material import approximates roughness/metalness differently, requiring engine-native material adjustment notes.

Meaningful variations:

- For museum archival, keep a high-resolution USD/source package and do less aggressive cleanup.
- For mobile, reduce material slots and use smaller texture sets.
- For a cinematic, preserve displacement or high-poly source for offline rendering.

## Example: Character Outfit Mesh For Rig Handoff

This is an example, not a required formula.

Production intent: Prepare a generated jacket mesh for rigging onto an existing humanoid character.

Inputs and constraints:

- Source: generated jacket mesh, 95k triangles, no rig, rough zipper/buttons, intended for an existing character skeleton.
- Target: rigging handoff in DCC plus FBX test import, max 4 bone influences per vertex for runtime.
- Required: clean deformation around shoulders, elbows, torso twist, and collar.

Workflow:

1. Align jacket to the approved character body in bind pose; freeze transforms only after alignment is verified.
2. Remove hidden inner geometry unless needed for open collar/cuffs.
3. Retopologize with loops around shoulders, elbows, cuffs, hem, and collar; keep zipper/buttons as separate meshes if they should be rigid or swapped.
4. Create UVs with seams along garment construction lines and hidden underside areas.
5. Bake fabric weave and seam detail from high-poly/generated source to normal/AO maps.
6. Name meshes/materials predictably: `jacket_body`, `zipper_teeth`, `button_L/R`, `mat_jacket_fabric`, etc.
7. Transfer/prototype skin weights from body or guide rig, then normalize and cap to target influence count.
8. Test arm raise, elbow bend, torso twist, crouch, and collar/head contact.
9. Deliver source DCC file, FBX test export, textures, bind-pose notes, weight problem areas, and rigging assumptions.

Expected result:

- A rig-ready garment asset that deforms predictably and gives the rigger clear mesh/material/weight structure.

Likely failure modes:

- Generated wrinkles are modeled as chaotic triangles that collapse under deformation.
- Buttons are fused into cloth and smear during skinning.
- UVs stretch across seams, making fabric weave swim.
- Bone influence limits are exceeded or weights are not normalized after transfer.

Meaningful variations:

- For cloth simulation, preserve separate cloth panels and solver-friendly topology rather than final skinned topology.
- For non-humanoid rigs, replace humanoid assumptions with the project's actual skeleton and root requirements.
- For cinematic close-ups, add displacement or higher-resolution fabric detail in the source handoff.

## Source Notes

Sources verified on 2026-07-11 unless otherwise noted.

- Khronos glTF 2.0 Specification: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html.
- KhronosGroup glTF Validator: https://github.com/KhronosGroup/glTF-Validator.
- OpenUSD Introduction: https://openusd.org/release/intro.html.
- Unreal Engine FBX Content Pipeline: https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-content-pipeline.
- Unreal Engine Skeletal Meshes: https://dev.epicgames.com/documentation/en-us/unreal-engine/skeletal-mesh-assets-in-unreal-engine.
- Unity Manual, Importing a model: https://docs.unity3d.com/Manual/ImportingModelFiles.html.
- Unity Manual, Rig tab Import Settings reference: https://docs.unity3d.com/Manual/FBXImporter-Rig.html.
- meshoptimizer README: https://github.com/zeux/meshoptimizer.
