---
name: 2d-character-rig-animation
description: Production guidance for reusable layered 2D character rigs in browser-rendered and video media. Use for SVG hierarchies, pivots and constraints, FK/IK planning, pose and facial libraries, acting, cycles, deterministic handoff, crop variants, and rig QA; not for character concept continuity, 3D armatures, or motion-capture solving.
---

# 2D character rig animation

Use this skill after the character design and approved model/reference sheets exist. Its job is to turn that design into a reusable performance system whose parts stay connected, poses remain on-model, facial states read clearly, and animation can be reproduced across shots and runtimes.

The rig may be SVG, layered vector art, raster cutouts, a bone-and-mesh puppet, or a hybrid. Runtime APIs differ; the production contract does not.

## Boundaries

This skill owns:

- part decomposition, draw order, hierarchy, pivots, controls, and constraints;
- bind/rest pose and coordinate conventions;
- rigid cutout versus deforming mesh decisions;
- reusable body poses, facial states, visemes, gestures, and cycles;
- acting and choreography using the approved character;
- deterministic animation handoff and rig-specific QA;
- rig asset rights, likeness limits, provenance, and delivery notes.

It does not own:

- the character's visual identity, costume continuity, or reference-generation strategy;
- 3D armatures, volumetric deformation, or DCC-specific rigging;
- capture, cleanup, or retargeting of motion-capture data;
- voice performance, lip-sync provider selection, or final compositing;
- redesigning an approved character to hide a rig defect.

## Evidence stance

- **Documented fact:** behavior from SVG/W3C, browser, accessibility, or other authoritative technical documentation.
- **Production heuristic:** an animation or rigging practice that must be adapted to the design and runtime.
- **Empirical observation:** measured behavior from the actual rig preview, frame samples, render, or delivery crop.

Technical references were checked **2026-07-12**. Runtime-specific transform, clipping, mesh-deformation, IK, and export behavior is volatile; verify the selected renderer and version before committing the rig architecture.

## Lock the rig contract

Collect or create:

- approved turnaround/model sheet and character bible;
- exact deliverables, aspect ratios, resolution, fps, duration, and runtime candidates;
- required views, actions, emotional range, dialogue languages, props, and interactions;
- whether the rig uses rigid pieces, deforming meshes, replacements, or a hybrid;
- maximum limb bends, reaches, squash/stretch, head turns, and perspective cheats;
- body and facial control list;
- naming, coordinate, unit, pivot, and transform-order rules;
- source-art, performer-likeness, font, prop, and brand rights;
- deterministic timeline format and renderer handoff;
- approval poses and test actions.

If the approved design cannot separate or deform without visible damage, return to design with a specific production constraint. Do not quietly alter anatomy, costume, logo placement, disability representation, or signature features.

## Decompose the artwork by motion responsibility

Split the character where independent motion, occlusion, deformation, replacement, or attachment requires it. Too few parts limit acting; too many parts produce seams, draw-order problems, and maintenance cost.

Typical roles:

```text
character-root
+- shadow
+- rear-accessories
+- pelvis
|  +- torso-chain
|  |  +- chest
|  |  |  +- neck
|  |  |  |  `- head
|  |  |  +- arm-left
|  |  |  `- arm-right
|  |  `- clothing-overlap
|  +- leg-left
|  `- leg-right
+- front-accessories
`- fx-and-contact-guides
```

The face can use nested controls for brows, lids, pupils, mouth replacements/deformation, cheeks, and optional head-turn features.

Production heuristics:

- Separate at natural joints, seams, hair clumps, garment layers, and rigid accessories.
- Add overlap beyond visible edges so rotation does not open gaps.
- Preserve a clean silhouette at intended playback size.
- Keep left/right names from the character's perspective and document that convention.
- Separate draw order from transform hierarchy when the runtime permits it.
- Use stable ASCII IDs that survive export; avoid names based only on layer numbers.

## Coordinate systems and SVG structure

**Documented fact:** SVG establishes viewports and user coordinate systems. `viewBox` maps a specified rectangle into the viewport, and transforms can be applied to elements and groups. Nested group transforms compose through the hierarchy.

For SVG rigs:

- set one intentional root `viewBox` and document character scale/origin;
- place each rotating group around an authored pivot;
- avoid mixing unexplained transforms from design tools with runtime transforms;
- flatten only transforms that do not destroy editable pivots or hierarchy;
- preserve clipping paths, masks, gradients, IDs, and references through optimization;
- scope IDs when multiple character instances may share a document;
- test the exported SVG rather than only the design-tool preview.

Use a neutral root pose with known local transforms. Store pivots numerically in the rig manifest even when the runtime can infer transform origins, because browser and export behavior can differ.

## Choose rigid, replacement, or deforming parts

### Rigid cutout parts

Best for graphic, mechanical, paper-puppet, or limited-animation styles. Rotate/translate/scale whole parts around joints. Protect seams with overlap art and occlusion layers.

### Replacement parts

Best for discrete hand shapes, mouth poses, eye shapes, perspective turns, and props. Define mutually exclusive groups and transition rules. A replacement is not a tween unless an actual in-between design exists.

### Deforming meshes or paths

Best where bending a rigid piece would create an obvious elbow, torso, cloth, tail, or facial defect. Define control influences and limits, then test extreme poses. Keep deformation local; excessive influence creates rubbery volume loss.

### Hybrid

Often appropriate: rigid forearm plus replacement hands, deforming torso, replacement mouths, and layered hair chains. Choose per visual requirement rather than forcing the whole character into one technique.

## Build the hierarchy and controls

Every control should have:

- stable ID and human-readable name;
- parent and optional visual-part binding;
- local pivot and rest transform;
- allowed translation, rotation, scale, or replacement values;
- hard/soft limits;
- preferred direction and neutral value;
- draw-order or visibility effects;
- test poses and known exceptions.

### FK and IK planning

Use forward kinematics when rotations should flow from parent to child and arcs are artist-directed: spine, head, tail, hair, loose gestures. Use inverse kinematics when an endpoint must stay attached: planted foot, hand on a desk, prop grip. A hybrid arm/leg rig may switch modes only with an explicit match procedure so the limb does not pop.

IK requirements:

- target and bend/pole direction;
- chain length and reach limits;
- soft behavior near full extension;
- stretch policy;
- fallback when the target is unreachable;
- FK/IK match pose and keyed switch frame.

Never let the solver choose an arbitrary elbow/knee direction at a singularity.

## Pose library as production vocabulary

Create poses that represent performance intent, not only technical extremes:

- neutral/default and breathing idle;
- attention/listening;
- positive, negative, uncertain, surprised, concentrated, and character-specific emotional states;
- open/closed hand, point, present, hold, reach, and contact poses;
- walk/run/contact/pass/up/down keys where locomotion is required;
- seated, crouched, turn, enter, exit, and prop-specific poses;
- safety/extreme tests for every joint and deformation region.

Each pose record should include body controls, face state, hand/prop state, view variant, hold suitability, and approved transitions. Pose libraries accelerate work only when they preserve character-specific acting; generic emoji poses are not a performance system.

## Facial rig and dialogue states

Separate controls for:

- eye direction and convergence;
- upper/lower lids and blink closure;
- brows and asymmetry;
- mouth open/close, corners, width, roundness, and jaw where relevant;
- optional cheek, nose, ear, or accessory motion;
- head-turn replacement features.

Viseme count should match the style, language, shot size, and schedule. Do not prescribe a universal inventory. Group phonemes that look similar at the target resolution, but preserve closures and distinctive shapes needed for intelligibility. Record which languages the set has actually been tested against.

Dialogue direction:

- mouth shapes follow timed speech, not arbitrary frame cycling;
- preserve complete closure where bilabial sounds require it;
- lead or lag only as an intentional style decision;
- add blinks, gaze, brows, head motion, and gestures as performance, not noise;
- avoid changing every control on every syllable;
- hold readable facial poses across fast cuts.

Do not infer emotion or personality solely from an automatic transcript. Use the approved performance direction.

## Animate performance, not controls

Plan each beat with:

- objective and emotional change;
- line/action timing;
- primary pose and silhouette;
- anticipation;
- main action and contact;
- settle, overlap, and hold;
- gaze and hand intention;
- camera/crop relationship.

Production heuristics from animation craft:

- Pose the line of action and silhouette before polishing limbs.
- Move the character's center/root consistently with weight and contact.
- Let secondary chains such as ears, hair, clothing, or tails follow the primary action with controlled delay.
- Favor arcs for organic joints unless the style is deliberately mechanical.
- Use stillness. A held, specific pose can read better than constant idle motion.
- Apply squash/stretch only where the construction and material permit it; preserve intended volume unless the style says otherwise.

## Cycles and contacts

For a cycle, define exact first/last compatibility, contact phases, root travel, and whether it is in-place or translating.

Walk-cycle QA:

- planted feet remain fixed relative to the ground during contact;
- root travel matches stride length;
- knees and elbows keep intended bend direction;
- limb lengths do not jump;
- torso/hip counter-motion supports weight;
- first/last frames do not create a duplicate-frame hitch;
- accessories loop without a snap.

For object contact, decide which system owns the attachment. A prop should not be independently animated while also parented to a hand unless the offset is intentional and documented.

## Deterministic timeline handoff

Deliver animation as explicit time-addressable state. A renderer may request frames backward or out of order.

Recommended shot record:

```json
{
  "shot_id": "explain-step-two",
  "fps": 30,
  "start_frame": 0,
  "end_frame": 179,
  "rig_version": "presenter-rig-03",
  "view": "three-quarter-right",
  "tracks": {
    "root.position": [[0, [0, 0]], [72, [8, -3]], [179, [0, 0]]],
    "arm_right.rotation": [[42, 4], [64, 28], [110, 28], [142, 6]],
    "mouth.pose": [[51, "M"], [55, "AH"], [60, "rest"]]
  }
}
```

This is an example schema, not a repository requirement.

Handoff rules:

- use frame numbers or exact rational timing consistently;
- state degrees versus radians and coordinate orientation;
- record interpolation/ease per segment;
- avoid unseeded random blink/idle timing in final renders;
- keep visibility and replacement changes explicit;
- ensure any solver produces the same state from the same frame;
- test forward, backward, first, last, and isolated frames.

## Aspect and crop variants

Do not blindly scale one performance into every canvas.

- Reframe the root and camera/crop while protecting hands, gaze targets, props, captions, and ground contacts.
- Create alternate gestures when a wide arm pose exits a vertical frame.
- Use approved view variants rather than flattening or mirroring a perspective turn.
- Preserve character-left/right continuity when mirroring is forbidden by costume, disability, text, scar, or prop design.
- Check silhouette and facial readability at final physical playback size.

## Rig QA

Test the rig before shot production with a standard suite:

1. bind/rest pose round trip;
2. joint extremes and full-chain stretch/compression;
3. mirrored/symmetric pose where appropriate;
4. hand and foot contacts;
5. FK/IK matching and switches;
6. full facial-state and viseme sheet;
7. blink/gaze extremes;
8. walk/idle/action loop boundaries;
9. front, side, and approved turn variants;
10. every delivery crop and repeated clean render.

Classify defects:

- **Seam/gap:** overlap or pivot exposes background.
- **Pop:** one-frame transform, replacement, draw-order, or solver discontinuity.
- **Slide:** contact point drifts while meant to be planted.
- **Collapse:** deformation loses intended volume or silhouette.
- **Flip:** elbow/knee or path changes side unexpectedly.
- **Drift:** proportions, facial construction, or prop placement leave approved tolerance.
- **Occlusion error:** wrong layer appears in front/behind.
- **Loop hitch:** duplicate/mismatched boundary frames.

Record frame, control values, cause, fix, and retest. Do not repair shot after shot when the root cause belongs in the rig.

## Accessibility and safety

**Documented fact:** WCAG 2.2 SC 2.3.1 limits flashes to no more than three in any one-second period unless below general/red flash thresholds. Blinks, eye closures, and ordinary pose changes are not automatically flashes, but high-contrast full-field eyelid, background, FX, or emissive changes can be.

Also review repetitive shaking, rapid zooming, spinning, and large-field movement. Interactive character surfaces should support reduced-motion preferences and controls where applicable. Prerecorded output may need a separately rendered calmer version.

SVG IDs and ARIA labels do not make every internal rig part meaningful to assistive technology. For interactive delivery, expose the semantic character/action at the appropriate container level and hide purely decorative implementation parts when appropriate. For video, provide captions, transcript, and description of essential visual-only action.

## Rights, consent, and provenance

Track separately:

- character/IP owner and permitted uses;
- source artist and rigging/animation authors;
- performer likeness, voice, or motion reference consent;
- derivative assets, brushes, fonts, logos, and props;
- runtime/library licenses;
- modification and approval history.

A rig license does not grant character rights, and character rights do not automatically grant performer likeness or voice rights. Preserve attribution and restrictions in the delivery ledger. Escalate branded mascots, licensed characters, real-person likenesses, minors, culturally sensitive designs, and synthetic replicas for appropriate approval.

## Delivery package

Deliver:

- editable source art and runtime-ready assets;
- rig manifest with hierarchy, pivots, limits, view variants, and control definitions;
- bind/rest pose and approved model/turnaround references;
- pose, gesture, cycle, facial, and viseme libraries;
- animation tracks or shot data with timing convention;
- runtime/version/export notes;
- rig test renders and QA report;
- rights/provenance ledger and required notices;
- known limits, forbidden poses, and repair guidance.

## Example 1: quadruped mascot loop set

This is a complete example, not a mandatory formula.

**Intent:** build a reusable flat-vector dog mascot for a browser campaign with idle, walk, sit, alert, and tail-wag loops.

**Constraints:** side and three-quarter approved views; 30 fps output; no mesh deformation in legs; tail may use a three-segment chain; collar logo must never mirror; loops must work in 1:1 and 9:16.

**Rig plan:** root at pelvis; torso/chest/head FK chain; separate near/far legs with two-bone controls and foot targets; three tail groups; ear chains; eye replacements; mouth closed/open/pant states; collar/logo separate in fixed draw order.

**Animation plan:** four-pose walk structure with planted foot targets and matching root travel; idle uses subtle chest breath and staggered ear/tail overlap; alert pose leads with head and ears, then chest; sit is a keyed action, not an IK collapse.

**QA:** overlay ground-contact frames; test tail/body collision; inspect near/far leg draw order; check first/last loop state; verify collar logo orientation in every view; render isolated frames backward.

**Expected result:** stable silhouette, no sliding feet, no gaps at hips/shoulders, readable states at mobile size, and reusable loops with documented speed ranges.

**Likely failures:** far leg crosses in front, tail opens a seam, root travel disagrees with stride, eye replacements pop, logo mirrors in the alternate view.

**Variation:** for a paper-cut style, expose joint pins deliberately and remove hidden overlap art only after the visual treatment is approved.

## Example 2: seated explainer presenter

This is a complete example, not a mandatory formula.

**Intent:** animate a seated presenter for a 45-second technical explainer with dialogue, two pointing gestures, a tablet contact, and 16:9/9:16 outputs.

**Constraints:** approved three-quarter view; upper-body priority; exact narration timestamps; six-language localization planned; hands must contact tablet and diagram; restrained enterprise tone.

**Rig plan:** pelvis/root and three torso controls; neck/head; eye aim; independent lids/brows; tested language-appropriate viseme set; FK/IK arms with match controls; replacement hands; tablet attachment target; limited lower-body controls; front/back forearm draw-order switch.

**Performance plan:** establish listening pose; anticipate first point with gaze, then hand; pin fingertip to diagram while torso settles; return through a clear intermediate pose; use asymmetric brow/gaze on the contrast line; hold the final open-hand summary pose. Localized dialogue reuses acting beats but retimes mouth and selected gestures rather than time-stretching the whole performance blindly.

**QA:** arm reach and IK bend, hand/tablet attachment, mouth closure and corners, eye convergence, brow clipping, draw-order switches, caption clearance, vertical gesture replacement, and frame-accurate repeated render.

**Expected result:** character appears to think and present rather than cycle through controls; contact is stable; localization can revise speech timing without rebuilding the rig.

**Likely failures:** elbow flips near extension, hand slides on tablet, every syllable triggers head motion, visemes are unsuitable for a target language, vertical crop removes the pointing hand.

**Variation:** if deterministic exactness outweighs reusable deformation, replace the two hero gestures with approved pose-to-pose hand/arm drawings while retaining the facial rig.

## Sources

Official and authoritative sources checked 2026-07-12:

- W3C SVG 2, coordinate systems, transforms, and viewBox: https://www.w3.org/TR/SVG2/coords.html
- MDN SVG tutorial and transform reference: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial and https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/transform
- MDN `viewBox`: https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/viewBox
- W3C WCAG 2.2, Three Flashes or Below Threshold: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- W3C WCAG 2.2, Animation from Interactions: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
- Adobe, animation principles overview: https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html
- ScreenSkills, animation production roles and skills: https://www.screenskills.com/job-profiles/browse/animation/