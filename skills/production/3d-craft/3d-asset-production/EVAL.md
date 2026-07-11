# Evaluation: 3D Asset Production

Use this file as the hidden evaluator answer key. Do not expose it to the agent being evaluated. The evaluated agent should receive only the user request and `SKILL.md`.

Score out of 100. A passing response should demonstrate production-ready asset reasoning, not just name file formats or generic cleanup steps.

## Scoring Summary

- Scope control and activation boundaries: 10 points
- Requirements and delivery contract: 15 points
- Geometry, topology, scale, UV, and material production: 20 points
- LOD, optimization, static/skeletal readiness, and rig handoff: 15 points
- Format interchange and target-engine delivery: 15 points
- Validation, QA, rights, and provenance: 15 points
- Evidence discipline and communication quality: 10 points

Critical failures can cap the score even when other sections are strong.

## Critical Failures

Cap at 40 if the response:

- Treats this as provider-specific 3D generation prompting instead of production finishing.
- Ignores the user's target format/engine and gives one-size-fits-all advice.
- Recommends delivering only raw generated/scanned output as production-ready without cleanup, validation, or rights checks.
- Presents false format claims, such as saying glTF is a full authoring format or exact CAD interchange format.
- Omits rights/provenance entirely for generated, scanned, client-provided, or third-party inputs.

Cap at 55 if the response:

- Covers mesh cleanup but omits scale/axes and import validation.
- Covers visual quality but omits budgets, LODs, texture memory, or target runtime constraints.
- Gives format recommendations without discussing what survives and what can be lost in glTF/USD/FBX interchange.
- Exposes or refers to this evaluator file.

Cap at 70 if the response:

- Is mostly correct but does not distinguish documented facts from heuristics where consequential.
- Provides no practical QA checklist or no target-engine round-trip validation.
- Omits either static mesh readiness or skeletal/rig handoff when the scenario involves both.

## Knowledge Questions

### 1. What is the appropriate scope of this skill?

Expected answer:

- It covers provider-independent production finishing of standalone 3D assets from generated, captured, scanned, modeled, or CAD-derived polygon output.
- It includes requirements, topology repair, scale/axes, UVs, PBR/baking, LODs, static/skeletal readiness, rig handoff, optimization, interchange, DCC/engine delivery, validation, QA, and rights/provenance.
- It excludes provider-specific generation, full scene/world building, mocap operation, and exact CAD/manufacturing.

Required points:

- 2 points for provider-independent production-ready asset finishing.
- 2 points for naming at least five included production domains.
- 2 points for explicit exclusions.

Incorrect or disqualifying claims:

- The skill is mainly for choosing a 3D generator.
- The skill guarantees manufacturing/CAD precision.
- The skill is about whole scenes rather than asset delivery.

### 2. What documented glTF facts should guide delivery?

Expected answer:

- glTF is an API-neutral runtime asset delivery format, not an authoring format.
- glTF uses right-handed coordinates, +Y up, +Z forward, and meters.
- Core glTF materials use metallic-roughness PBR; base color/emissive are sRGB, data maps such as metallic/roughness/normal are linear, and roughness/metalness are packed in G/B for metallic-roughness.
- glTF skinning uses `JOINTS_n` and `WEIGHTS_n`; joint/weight sets must match and weights must be valid.
- Validators can check structure, references, buffers, forbidden accessor values, images, and many extension issues.

Required points:

- 2 points for runtime-not-authoring.
- 2 points for coordinate/unit convention.
- 2 points for PBR/color/channel facts.
- 1 point for skinning facts.
- 1 point for validator role.

Incorrect or disqualifying claims:

- glTF preserves all DCC modifiers, procedural materials, and rigging systems.
- glTF uses centimeters by default.
- Metallic and roughness can be arbitrarily packed without shader/material changes.

### 3. How should an agent decide between retopology and decimation?

Expected answer:

- Retopologize for deformation, close-up hero assets, reliable bakes, predictable UVs, clean LODs, and generated meshes with chaotic topology but valuable shape.
- Controlled decimation can be appropriate for static, organic, scan-derived assets where editability and deformation are not required.
- Re-model when generated or converted geometry is physically incoherent or impossible.
- Protect silhouette, material/UV boundaries, deformation loops, attachment zones, and contact surfaces.

Required points:

- 3 points for retopology triggers.
- 2 points for decimation triggers.
- 1 point for re-modeling trigger.
- 2 points for preservation priorities.

Incorrect or disqualifying claims:

- Always decimate generated/scanned output.
- Triangle count alone determines production readiness.
- Deforming assets can use arbitrary decimated scan topology without risk.

### 4. What belongs in a production provenance record?

Expected answer:

- Source type and owner/license/terms.
- Generation provider/model/settings/date if generated.
- Capture location/date and consent/release status if scanned.
- Third-party references, trademarks, logos, product shapes, and clearance status.
- Human likeness or personal-data issues if applicable.
- Modifications performed and redistribution/attribution requirements.

Required points:

- 2 points for source/license.
- 2 points for generated/capture metadata.
- 2 points for rights/trademark/human-likeness concerns.
- 2 points for modifications and redistribution/attribution.

Incorrect or disqualifying claims:

- Generated assets never need rights review.
- Scan/capture consent is irrelevant.
- Removing metadata is best practice.

## Production Decision Questions

### 5. Scenario: A user has a generated 300k-triangle robot mesh and wants a game-ready FBX for Unreal with animation later. What should the agent recommend?

Expected decision:

- Treat the generated mesh as high-poly/reference unless its topology is already clean.
- Establish scale, orientation, pivot/root, naming, material parts, and target Unreal import requirements.
- Retopologize or remodel mechanical parts into clean static/skeletal-ready pieces rather than simple decimation.
- Build UVs, bake normal/AO/material masks, author PBR materials, and generate LODs.
- Prepare skeletal/rig handoff if animation is planned: joints, pivots, separate rigid parts or deformation loops, bone naming assumptions, bind pose, weight limits.
- Export FBX with settings compatible with the target Unreal version, noting Unreal's FBX version sensitivity; import into a clean Unreal project and test material slots, scale, skeleton/morph needs, and LODs.
- Record provider/settings/provenance and rights status.

Strong answer must demonstrate:

- Understanding that generated topology is often unsuitable for animation.
- Unreal-specific import validation.
- Separation between static mesh prep and rig handoff.
- Rights/provenance record.

Penalize:

- Recommending decimate-to-50k and export as final without retopo or validation.
- Ignoring skeletal readiness because the user said animation is later.
- Treating OBJ/FBX conversion as the main task.

### 6. Scenario: A museum scan must become a mobile AR product preview in GLB and USDZ. What tradeoffs matter?

Expected decision:

- Verify capture permissions and distribution rights first.
- Establish real-world dimensions and pivot for AR placement.
- Clean scan debris, holes, and baked lighting; de-light/repaint albedo if relighting is expected.
- Reduce geometry with silhouette preservation and mobile budgets; bake high-frequency detail to normal/AO maps.
- Use glTF metallic-roughness-compatible materials for GLB; prepare USDZ/USD package with target platform material checks.
- Validate GLB with glTF Validator and test in the actual AR viewers/devices.
- Keep high-resolution source/scan archive separately.

Strong answer must demonstrate:

- Mobile/AR scale and file-size sensitivity.
- Separate GLB and USDZ material/import checks.
- Scan rights and de-lighting awareness.

Penalize:

- Claiming GLB alone guarantees AR compatibility.
- Keeping a 22M triangle scan because AR devices can downsample automatically.
- Ignoring real-world scale.

### 7. Scenario: A character jacket must be handed to a rigger. What is the right production plan?

Expected decision:

- Align to character bind pose and skeleton requirements.
- Retopologize with deformation loops around shoulders, elbows, cuffs, collar, and hem.
- Separate rigid/non-deforming accessories as needed.
- Create clean UVs and bake fabric/seam detail from high-poly source.
- Prototype or prepare weight transfer, normalize weights, respect target bone influence limits.
- Test deformation poses and document problem areas.
- Deliver source DCC, textures, FBX/test export, bind-pose notes, naming guide, and rig assumptions.

Strong answer must demonstrate:

- Rig handoff is not the same as finished animation.
- Topology and weights are deformation-critical.
- Accessories may need separate handling.

Penalize:

- Only saying "export FBX with skeleton".
- Ignoring bind pose, weights, and deformation tests.
- Leaving generated chaotic wrinkles as production topology.

## Applied Production Tasks

### 8. Task: Write a production checklist for converting a generated prop to a production GLB.

Successful output characteristics:

- Starts with target requirements and budget.
- Archives source and records provenance.
- Establishes scale, axes, origin, and pivot.
- Cleans topology and decides retopo/decimation/remodeling.
- Builds UVs and PBR maps with glTF color/channel rules.
- Generates LODs or justifies no LODs.
- Exports GLB with relative/embedded resources as appropriate.
- Runs glTF Validator and target viewer import tests.
- Includes rights and known limitations.

Rubric, 10 points:

- 2 requirements/budget.
- 1 provenance.
- 1 scale/axes/pivot.
- 2 geometry/topology/UV.
- 2 PBR/baking/glTF material details.
- 1 LOD/optimization.
- 1 validation/QA.

Critical failures:

- No validation.
- No material/texture color-space/channel details.
- No provenance.

### 9. Task: Review an asset delivery summary and identify blockers.

Input summary to evaluate:

"Delivered chair.glb exported from generator. 180k triangles, one embedded 8k texture, no UV edits, arbitrary size, origin at world center from generation, base color includes studio shadows, no validation errors checked, no source/provenance. Looks good in the generator preview."

Expected findings:

- Wrong/unknown scale and pivot are blockers for placement/AR/product use.
- Generator preview is not target validation; must test in GLB validator and target viewer.
- 180k triangles and 8k texture may exceed web/mobile/download budgets; need target budget and optimization.
- No UV edits and embedded generated texture may cause poor material reuse, stretching, or unclean bakes.
- Studio shadows in base color are inappropriate if asset must relight.
- No source/provenance/rights record blocks distribution.
- Need topology inspection, material rebuild, PBR map creation, LODs if required, and package documentation.

Rubric, 10 points:

- 2 scale/pivot.
- 2 validation.
- 2 performance/budget.
- 1 UV/material issue.
- 1 de-lighting issue.
- 2 provenance/rights.

Critical failures:

- Accepting generator preview as sufficient.
- Missing provenance/rights blocker.

### 10. Task: Explain glTF, USD, and FBX choice for a mixed DCC plus engine delivery.

Successful output characteristics:

- Recommends source DCC file for editability.
- Recommends glTF/GLB for runtime/web/interchange preview when compatible.
- Recommends USD/USDZ for composed DCC/production pipelines, variants, references, layers, and AR packaging where needed.
- Recommends FBX for Unity/Unreal skeletal/static mesh and animation workflows when the target expects it.
- Notes what may not survive: DCC modifiers, procedural materials, constraints, rigging systems, shader networks, version/axis/unit quirks.
- Requires actual import tests in each consumer.

Rubric, 10 points:

- 2 source DCC/source of truth.
- 2 glTF/GLB role and limits.
- 2 USD role and limits.
- 2 FBX role and limits.
- 2 validation/import testing.

Critical failures:

- Claiming a single format preserves everything.
- Misstating glTF as an authoring format.
- Ignoring FBX version/import differences.

## Evidence And Communication Assessment

Award up to 10 points for evidence and communication:

- 3 points: Separates documented facts, empirical checks, and heuristics when consequential.
- 2 points: Dates volatile facts or avoids unsupported volatile claims.
- 2 points: Uses official/spec/vendor sources where claims are factual.
- 2 points: Gives concrete, ordered production actions rather than vague advice.
- 1 point: Clearly names assumptions and unknowns.

Penalize overconfident universal rules, uncited factual claims about format limits, unsupported provider/legal claims, and advice that cannot be tested in the target pipeline.
