---
name: vfx-compositing
description: Provider-independent VFX compositing direction for generated video, ads, trailers, product films, social clips, explainers, mixed-source edits, and image/video composites. Use when an agent must plan, brief, generate, integrate, repair, or quality-check visual effects composites involving plates, alpha/mattes, keying, roto, tracking, stabilization, matchmove, lighting/color integration, grain/noise/sharpness, shadows/reflections/contact, depth/atmosphere, AI-generated elements, clean plates, editor/colorist handoff, rights/safety, or compositing QA.
---

# VFX compositing direction

Use this skill to make composite shots feel photographed together, not stacked together. Treat compositing as shot integration across color, motion, geometry, light, lens, material contact, atmosphere, artifact repair, and delivery handoff.

Do not use this skill as a substitute for legal clearance, colorist judgement, an on-set VFX supervisor, or a compositor operating a specific node graph. Use it to brief, plan, supervise, and review provider-independent compositing work.

## Evidence posture

Documented facts below come from professional documentation and standards sources listed at the end. Tool-specific documentation facts were verified on 2026-07-10 and may change.

Empirical observations are repeatable checks an agent can perform by reviewing frames, scopes, mattes, tracks, and before/after renders.

Production heuristics are practical rules of thumb. They are not universal laws; override them when shot evidence, client direction, or a facility spec requires a different approach.

## The compositing target

A good composite satisfies four contracts:

1. The audience contract: the shot does not pull attention away from the story, product, or message.
2. The camera contract: inserted elements share the plate’s perspective, lens behavior, exposure logic, motion, and defocus.
3. The image contract: elements share color pipeline, black/white points, grain/noise, sharpness, compression, and atmospheric depth.
4. The production contract: inputs, versions, rights, AI provenance, handles, mattes, and final outputs are traceable enough for editor/colorist handoff.

When time is short, prioritize the most audience-visible mismatches: perspective, scale, contact/shadow, edge quality, color temperature, motion jitter, and grain/sharpness.

## Start with plate and reference prep

Before requesting generation, roto, cleanup, or integration, inventory the plate:

- Delivery target: aspect ratio, frame rate, resolution, color space, HDR/SDR, codec, duration, handles, captions/safe areas.
- Plate quality: camera motion, rolling shutter, motion blur, focus, lens distortion, chromatic aberration, grain/noise, compression, exposure, white balance, clipped highlights, crushed shadows.
- Spatial facts: horizon, vanishing points, camera height, focal-length feel, ground plane, object scale references, parallax, occluders.
- Lighting facts: key direction, softness, color temperature, bounce fill, practical lights, contact shadows, reflective surfaces, atmospheric haze.
- Matte needs: what must be foreground, background, holdout, garbage matte, key, roto, object selection, depth mask, or clean plate.
- Rights and safety: whether people, products, logos, artwork, locations, copyrighted plates, synthetic endorsements, or likenesses require permission or disclosure.

Production heuristic: write a one-paragraph "shot physics note" before creating any element. Include camera, light, scale, and artifact targets. It prevents generic AI elements from drifting away from the plate.

Example shot physics note:

> 6-second handheld product insert, 24 fps, shallow depth of field. Add a translucent blue holographic UI emerging from the phone screen. Match the plate’s warm practical key from camera left, mild green office spill, visible rolling-shutter wobble, 35mm-ish perspective, screen reflections, contact glow on fingers, plate grain, and slight compression softness. Keep UI behind thumb occlusion and avoid over-bright clipped cyan.

## Choose the composite strategy

Use the least destructive strategy that can pass the shot’s QA bar:

- 2D overlay: for screen replacements, glows, lower-complexity HUDs, product labels, sky swaps, text/callouts, and stylized explainers where perspective is simple.
- 2.5D card/projection: for stills, generated backgrounds, matte paintings, parallax layers, product hero plates, or social clips needing camera drift without full 3D.
- 3D matchmove: for objects that must sit in a moving camera, cast/contact with surfaces, pass behind occluders, or share lens/parallax.
- Deep/depth-aware integration: for fog, smoke, translucent layers, dense occlusion, or CG renders with depth where depth samples or Z passes are available. Documented fact: deep images store multiple samples at varying depths with color, opacity, and camera-relative depth; Foundry documents this for Nuke deep compositing.
- Full replacement/regeneration: for shots with unusable plate quality, impossible rights issues, severe motion/occlusion mismatch, or when a generated shot can satisfy the creative intent more safely than repairing the plate.

Empirical observation: if an element only "sticks" when viewed as a still but swims during playback, the chosen strategy probably under-solves motion, perspective, occlusion, or rolling-shutter behavior.

## Alpha, mattes, keying, and roto

Documented facts:

- Alpha channels carry transparency information; premultiplied color must be handled correctly during over operations. OpenEXR documentation notes alpha/opacity conventions and premultiplied color for correct over compositing.
- Keying tools extract mattes procedurally. Foundry documents keyer nodes for luma, chroma, and difference keying, and documents Keylight as a color-difference keyer.
- Foundry’s Keylight documentation distinguishes screen matte, inside/holdout masks, outside/garbage masks, despill, and screen matte adjustments.
- Adobe’s After Effects Object Matte documentation, last updated May 25, 2026 and verified here on 2026-07-10, describes AI-assisted subject selection, propagation across time, manual refinement, Refine Edge, and freezing the matte for compositing.

Direct the agent or compositor to separate matte decisions:

- Core matte: the object’s opaque body. It should be stable and not breathe.
- Edge matte: hair, motion blur, glass, mesh, smoke, translucent fabric, and defocused boundaries. It should preserve softness and partial transparency.
- Garbage matte: excludes rigs, tracking marks, unwanted screen edges, or areas that should never be considered foreground.
- Holdout/inside matte: protects foreground regions that a keyer or AI matte wrongly hollows out.
- Occlusion matte: puts plate objects in front of inserted elements.

Production heuristics:

- Do not judge a matte only over black, white, or checkerboard. Review over the intended background plus high-contrast test colors.
- Do not crush a matte into hard black/white unless the source edge is genuinely hard. Motion blur and defocus need gray alpha.
- Use multipass keying when different regions have different contamination: hair, body, transparent props, and spill often need different treatment.
- Despill should remove screen contamination without turning skin, fabric, or product colors gray.
- Roto should follow anatomy, mechanics, and perspective; avoid single giant shapes when a limb/object has independently moving parts.

Common failures:

- Chattering/boiling edges from unstable AI masks or noisy keys.
- Edge halos from mismatched premultiplication, bad despill, over-eroded mattes, or background contamination.
- Cutout look from hard roto on motion-blurred footage.
- Matte lag where propagated selection trails behind fast motion.
- Transparent holes in foreground details such as logos, hair, fingers, or product edges.

## Tracking, stabilization, and matchmove

Documented facts:

- Foundry’s CameraTracker is designed to create a virtual camera whose movement matches the original camera, allowing 3D objects to be added to 2D footage.
- Foundry documents masks for excluding areas likely to cause CameraTracker problems, such as moving actors or burn-ins.
- Adobe documents 3D Camera Tracker workflows in After Effects, and Adobe tracking/stabilization docs were updated in 2026; verify exact UI behavior for the installed version before instructing users.

Direct tracking by intent:

- Stabilize only when the final shot needs a stable design surface or when cleanup requires it; reapply original motion afterward if the plate should remain handheld.
- Use 2D point/planar tracking for screens, signs, labels, wall graphics, patches, and flat surfaces.
- Use camera solve/matchmove for 3D inserts, volumetric effects, parallax-heavy shots, or objects touching the ground plane.
- Use object tracking or manual animation when the camera is stable but the target object moves.
- Use masks to exclude independently moving actors, vehicles, reflections, subtitles, burn-ins, and generated artifacts from the solve.

Empirical track checks:

- Place a temporary grid, axis marker, or card on the tracked plane and play the whole shot.
- Check start, middle, end, and hardest motion frames.
- Watch for sliding at contact points, perspective shear, scale drift, and "rubber sheet" warping.
- Verify that stabilization did not crop important edges or alter intended motion.
- If solving a camera, compare estimated horizon and ground plane against plate cues.

Production heuristic: never approve a track from a single representative frame. Most track failures appear during acceleration, occlusion, motion blur, or near frame edges.

## Perspective, camera, and lens integration

A generated element must inherit the plate’s camera logic:

- Match horizon height, vanishing points, and ground plane before color work.
- Match focal-length feel: wide lenses exaggerate scale and edge distortion; telephoto lenses compress depth.
- Match lens distortion: straight generated geometry can look pasted onto a distorted plate. Undistort/track/redistort when needed.
- Match focus and depth of field: a razor-sharp element in a soft plate is usually wrong.
- Match motion blur direction, shutter feel, and rolling-shutter wobble where visible.
- Respect occlusion ordering: foreground objects, fingers, hair, smoke, glass, and reflections must layer correctly.

AI generation note: request perspective and lens traits explicitly in the generation prompt, but verify them visually. AI models may create plausible-looking elements with inconsistent geometry, impossible reflections, or unstable detail across frames.

## Lighting, color, and exposure integration

Documented facts:

- ACES is a free, open, device-independent color management and image interchange system from the Academy. Adobe documents After Effects OCIO/ACES integration and recommends OCIO color management when working in ACES workflows; that Adobe page was last updated May 5, 2026 and verified here on 2026-07-10.
- OpenColorIO is used in motion-picture production color management; Nuke uses OCIO configuration files for color transforms.
- OpenEXR supports high dynamic range, 16-bit/32-bit floating point data, arbitrary channels, metadata, multi-part files, and deep data.

Direct color workflow:

1. Identify plate color space or require the producer to state it. Do not guess silently when professional delivery matters.
2. Convert elements into the working color space before grading them to match.
3. Match exposure and contrast before hue tweaks.
4. Match black point, white point, saturation rolloff, and highlight clipping behavior.
5. Apply creative grade/view transform consistently; do not bake a display transform into an element and then grade it again.
6. Deliver colorist-friendly outputs: ungraded/precomped passes when requested, final comp preview, LUT/OCIO notes, and any baked transforms called out.

Production heuristics:

- If an insert looks "too clean," reduce local contrast and saturation before adding noise.
- Match shadow hue separately from highlight hue; many plates have warm highlights and cool shadows, or mixed practical colors.
- Product work may require brand-color protection. Match the plate, but do not accidentally change regulated packaging, logo colors, or UI colors beyond approved tolerances.
- For SDR social delivery, test on a phone-size preview; subtle edge/color issues can vanish, while oversharpening and halos can become worse.

## Grain, noise, sharpness, compression, and lens artifacts

Generated elements often fail because they are too pristine.

Match the plate’s:

- Grain/noise size, color, intensity, and temporal behavior.
- Compression softness, banding, macroblocking, and chroma subsampling artifacts.
- Sharpness, edge enhancement, chromatic aberration, bloom, halation, flare, vignette, and sensor clipping.
- Motion blur, defocus blur, bokeh shape, and rolling-shutter skew.

Production heuristics:

- Add grain/noise late, after color matching and blur, but before final compression tests.
- Degrain-match-regrain can help with plate cleanup, but regrain must be consistent across repaired and untouched areas.
- Do not sharpen generated elements to "improve quality" if the plate is softer. Integrate first; enhance globally only if the final finish requires it.
- Watch temporal noise: static noise on a moving element or crawling noise on a locked plate will reveal the composite.

## Contact, shadows, reflections, and material response

Contact sells the composite. Add or verify:

- Contact shadows where objects meet ground, hands, shelves, screens, or faces.
- Occlusion darkening under feet, products, vehicles, furniture, labels, and floating UI anchors.
- Reflections on glass, metal, glossy plastic, wet surfaces, screens, and eyes.
- Bounce light or colored spill cast by bright inserted elements.
- Refraction or transparency when elements pass behind glass, liquid, smoke, or translucent material.
- Surface interaction: dust displacement, footprints, screen glow on fingers, condensation, ripples, or mild deformation if relevant.

Production heuristic: a weak contact shadow is usually better than no contact shadow, but a shadow in the wrong direction is worse than a subtle one. Direction must obey the plate’s key light.

## Depth, atmosphere, and volumetrics

Depth cues must agree:

- Add atmospheric perspective for distant inserts: lower contrast, lower saturation, haze color, and softened detail.
- Put fog/smoke behind and in front of objects using depth/holdout mattes, not one flat overlay when occlusion matters.
- Match particle scale and drift to the shot: sparks, dust, rain, snow, and smoke should move with the environment and camera.
- Keep depth of field consistent: foreground UI, midground product, and background skyline should not all be equally sharp if the plate is shallow-focus.

AI caution: generated fog, smoke, rain, fire, and particles can look spatially convincing in one frame but ignore depth ordering over time. Review in motion with occlusion guides.

## AI-generated element integration

When using AI to create inserts, extensions, repairs, or full replacement shots, brief the model with integration constraints, not just subject description.

Include:

- Plate context: camera angle, lens feel, motion, lighting, color, time of day, surface material, occluders.
- Element purpose: background extension, product insert, magic effect, cleanup patch, reflection, matte painting, set extension, screen replacement.
- Continuity constraints: exact product shape, logo placement, wardrobe, hand pose, actor identity only if authorized, scene geography, UI state, or story beat.
- Negative constraints: no extra fingers, no logo changes, no new text, no impossible reflections, no invented faces, no added background people, no camera angle change.
- Output request: alpha if supported, clean plate, separate shadow/reflection pass, foreground holdout, handles, consistent seed/version if available.

Empirical observations to check:

- Temporal consistency of textures, logos, hands, eyes, and product geometry.
- Element scale from frame to frame.
- Whether AI changed the underlying plate while "repairing" it.
- Whether artifact removal erased real details such as jewelry, labels, scars, vents, or product seams.
- Whether generated text/logos are accurate enough for the delivery context; regenerate or replace manually when necessary.

Production heuristic: for product films and ads, prefer controlled still/image generation plus compositing for exact product appearance unless a video model can preserve geometry, text, and brand details at the required fidelity.

## Clean plates and artifact repair

Use clean plates for removals, replacements, retiming gaps, and object occlusion. A clean plate can come from:

- The same shot before/after the object enters.
- Neighboring frames stabilized and patched.
- A separate on-set clean plate.
- A reconstructed still/image generated from the plate, if rights and disclosure requirements allow it.
- Manual paint/clone/projection work.

Repair process:

1. Stabilize or track the region if the camera moves.
2. Patch in a color-managed working space.
3. Preserve plate grain, blur, lighting variation, and perspective.
4. Reapply motion if stabilized.
5. Compare against adjacent frames and untouched areas.
6. Log AI-assisted repair if provenance or client policy requires it.

Common failures:

- Frozen patch in a moving/noisy shot.
- Repeated texture clones.
- Edge seams revealed by compression.
- Missing shadows/reflections after object removal.
- AI hallucinated objects in blank walls, skies, shelves, or skin texture.

## Versioning and handoff

Track enough metadata for another agent, compositor, editor, or colorist to continue without guessing:

- Shot ID, source plate path, frame range, handles, frame rate, resolution, color space, and delivery target.
- Tool/provider/model/version/date for AI-generated or AI-repaired elements when available.
- Prompt or direction used for generated elements; seed/reference IDs if available.
- Matte/roto/key/tracking status and known weak frames.
- Color pipeline notes: OCIO config, ACES version/config if used, LUTs, display transform, baked transforms, precomp/final comp distinction.
- Passes delivered: beauty, alpha, matte, clean plate, shadow, reflection, depth/Z, normal, motion vector, grain plate, final preview.
- Review notes and open risks.

Naming heuristic:

Use stable shot/version names such as `brandfilm_sh012_comp_v004_preview.mp4`, `brandfilm_sh012_cleanplate_v002.exr`, `brandfilm_sh012_ui_alpha_v003.exr`. Do not overwrite approved versions.

Editor handoff:

- Provide a lightweight review render in the edit codec/resolution requested.
- Include handles if the shot may be trimmed.
- State whether the render is final, temp, slap comp, color-unmanaged preview, or pending color.

Colorist handoff:

- Clarify whether the comp is pre-grade or post-grade.
- Avoid baking a look unless requested.
- Deliver EXR or high-bit-depth intermediates when the workflow requires latitude.
- Provide mattes for selective grade if the colorist will refine integration.

## Rights, safety, and disclosure

Documented facts:

- The U.S. Copyright Office’s AI reports include Part 1 on digital replicas, Part 2 on copyrightability of generative AI outputs, and a pre-publication Part 3 on generative AI training; this page was verified on 2026-07-10.
- The FTC states endorsements must be truthful and not misleading, and material connections that affect how people evaluate an endorsement should be disclosed.
- Content Credentials/C2PA provide provenance signals that can show how content was made and edited; Adobe describes Content Credentials as durable metadata that can include whether content was camera-captured, AI-generated, or edited.
- WCAG 2.2 Success Criterion 2.3.1 says web pages must not contain content that flashes more than three times in any one-second period unless below flash thresholds.

Apply these rules:

- Do not create or composite a recognizable person, performer, private individual, voice/face likeness, or digital replica without appropriate permission for the intended use.
- Do not fabricate endorsements, testimonials, review footage, product demos, medical/financial outcomes, or news-like evidence.
- Do not alter regulated claims, safety labels, price disclosures, UI states, or product performance in a way that misleads viewers.
- Keep provenance for source plates, stock assets, generated elements, and licensed VFX elements.
- Flag synthetic or materially altered media when required by platform, client policy, jurisdiction, or context.
- Check intense flashes, strobe effects, explosions, glitch cuts, and high-contrast rapid transitions against photosensitive safety guidance.

When rights are unclear, stop and ask for clearance direction instead of burying the risk inside a comp note.

## Compositing QA

Review in motion, at delivery size, and frame-by-frame around problem areas.

Minimum QA pass:

- Edges: halos, chatter, cutout look, matte holes, despill errors, premult issues.
- Motion: sliding, lagging, jitter, stabilization crop, rolling-shutter mismatch, motion blur mismatch.
- Geometry: wrong perspective, scale, horizon, lens distortion, parallax, occlusion order.
- Light/material: missing contact shadows, wrong shadow direction, no reflections, wrong bounce/spill, impossible highlights.
- Color: mismatched white balance, black/white point, saturation, contrast, gamut clipping, baked display transform.
- Texture: grain/noise mismatch, static grain, oversharpening, compression artifacts, banding.
- Continuity: product/logo/text accuracy, wardrobe/prop consistency, geography, time of day, temporal flicker.
- Safety/rights: likeness permission, licensed elements, provenance, synthetic disclosure, flash risk, misleading claims.
- Handoff: versions, handles, source paths, color notes, mattes, known limitations.

Diagnostic review sequence:

1. Watch full shot at speed without pausing. Note what draws the eye first.
2. Toggle comp over plate if possible.
3. Inspect alpha/matte over black, white, gray, and final background.
4. Check scopes for black/white point and saturation mismatch.
5. Scrub problem frames and adjacent handles.
6. View at phone/social size and full resolution.
7. Encode a test at final compression; compression can reveal seams and banding.

## Example: screen replacement in handheld product footage

Production intent: replace a blank phone screen with a live app UI in a 7-second handheld social ad while preserving fingers crossing the screen.

Inputs and constraints:

- 24 fps handheld plate, shallow focus, warm practical light.
- Final 1080x1920 social vertical.
- UI must be brand-accurate; no AI-generated text in the UI.
- Thumb crosses the screen from frames 61-83.

Direction:

1. Track the phone screen as a planar surface. Verify with a temporary checkerboard across the full shot.
2. Create a thumb occlusion matte for frames 61-83; preserve motion-blurred thumb edges.
3. Corner-pin or project the rendered UI into the tracked screen.
4. Add screen reflection and slight glass softness; do not make the UI perfectly crisp if the phone is out of focus.
5. Add faint blue/cyan spill on the thumb only if visible and believable.
6. Match plate grain and final compression.
7. QA for track sliding at screen corners and matte chatter around the thumb.

Why structured this way:

The UI is controlled artwork, not generated text. The track and occlusion sell the physical screen. Reflection, blur, and grain prevent a pasted-on look.

Likely failure modes:

- UI corners drift during hand motion.
- Thumb appears behind the screen due to missing occlusion.
- UI is too bright and clips differently from the plate.
- UI remains sharp while the phone falls out of focus.

Meaningful variations:

- If the phone rotates in 3D, use a stronger planar solve or camera/object matchmove.
- If the UI is a stylized hologram rather than screen content, add light wrap, glow, and contact/reflection on glass/fingers, but still preserve occlusion.

## Example: AI creature in a trailer plate

Production intent: add a shadowy creature crossing a foggy alley for a 3-second teaser shot.

Inputs and constraints:

- Moving camera with foreground trash bags and drifting fog.
- Creature is mostly silhouette; no recognizable animal IP.
- Final must cut quickly but withstand 4K review.

Generation direction for the creature element:

> Generate a dark, original quadruped creature silhouette crossing left to right in a foggy night alley, low camera angle, wet asphalt reflections, backlit by a cold streetlamp, motion-blurred legs, partial occlusion by foreground trash bags, no gore, no recognizable franchise creature, no readable text or logos. Keep the body mostly in shadow, with faint rim light and wet specular highlights. Provide alpha or clean background separation if supported; otherwise provide a high-contrast pass suitable for roto.

Compositing direction:

1. Solve or approximate the camera motion; place the creature on the ground plane.
2. Add contact shadows under feet and soft reflection on wet asphalt.
3. Put foreground trash bags in front using roto/holdout matte.
4. Place some fog in front of the creature and some behind it; avoid one flat fog layer.
5. Match plate grain, low-light chroma noise, lens softness, and cold/warm light mix.
6. Review only after final teaser compression, because dark fog gradients band easily.

Why structured this way:

The creature can remain impressionistic, but ground contact, occlusion, wet reflection, and depth-layered fog must be precise or the shot will fail.

Likely failure modes:

- Creature floats because contact shadow/reflection is missing.
- Fog overlays creature uniformly and flattens depth.
- AI limb motion warps between frames.
- Creature design resembles protected IP or adds unintended gore.

## Example: product beauty comp from generated stills and live-action plate

Production intent: combine a generated premium kitchen background with a real photographed bottle for a product film hero shot.

Inputs and constraints:

- Real bottle plate with alpha, 4K, product color must remain accurate.
- Generated background must feel like a photographed kitchen at sunrise.
- Final colorist will grade the whole film.

Direction:

1. Keep bottle as the color authority. Do not AI-regenerate the label or cap.
2. Generate or select a background with matching camera height and focal-length feel; avoid impossible countertop reflections.
3. Composite in a color-managed workflow; preserve high-bit-depth intermediate if available.
4. Add contact shadow and subtle reflection from bottle onto countertop.
5. Match background depth of field to the bottle focus plane.
6. Add warm sunrise bounce on bottle edges only if consistent with existing plate highlights.
7. Deliver final preview plus a pre-grade/high-bit-depth comp and separate bottle matte for colorist isolation.

Why structured this way:

Product accuracy and colorist latitude matter more than fully generative novelty. The bottle stays real; the environment is adjusted to support it.

Likely failure modes:

- Background perspective makes bottle scale ambiguous.
- Generated countertop reflection contradicts bottle placement.
- Product label changes due to AI repair.
- Final preview has a baked look that limits color grading.

## Source notes

- Foundry Nuke documentation: Keylight (`https://learn.foundry.com/nuke/content/reference_guide/keyer_nodes/keylight.html`), CameraTracker (`https://learn.foundry.com/nuke/14.0/content/comp_environment/cameratracker/camera_tracking.html`), masking for camera tracking (`https://learn.foundry.com/nuke/content/comp_environment/cameratracker/masking.html`), deep compositing (`https://learn.foundry.com/nuke/content/comp_environment/deep/deep_compositing.html`), and OCIO color management (`https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/using_ocio_config_files.html`). Verified 2026-07-10.
- Adobe After Effects documentation: Object Matte (`https://helpx.adobe.com/after-effects/desktop/roto-brush-and-refine-matte/roto-brush/object-matte.html`), tracking/stabilization (`https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/track-motion/tracking-stabilizing-motion-cs5.html`), 3D Camera Tracker (`https://helpx.adobe.com/after-effects/desktop/work-with-3d-composition/3d-camera-tracker-effect/tracking-3d-camera-movement.html`), and OCIO/ACES color management (`https://helpx.adobe.com/after-effects/desktop/adjust-colors/opencolorio-and-aces-color-management/opencolorio-aces-color-management.html`). Verified 2026-07-10.
- Academy ACES (`https://www.oscars.org/science-technology/sci-tech-projects/aces`) and OpenColorIO (`https://opencolorio.org/`) documentation for color-management concepts. Verified 2026-07-10.
- OpenEXR technical documentation (`https://openexr.com/en/latest/TechnicalIntroduction.html` and `https://openexr.com/en/latest/InterpretingDeepPixels.html`) for high dynamic range, arbitrary channels, alpha conventions, metadata, multi-part files, and deep data. Verified 2026-07-10.
- U.S. Copyright Office AI initiative page (`https://www.copyright.gov/ai/`) for digital-replica, generative-output copyrightability, and generative-AI-training report status. Verified 2026-07-10.
- FTC endorsement guidance (`https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking` and `https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255`) for truthful, non-misleading endorsements and disclosure of material connections. Verified 2026-07-10.
- C2PA (`https://c2pa.org/`), Content Credentials (`https://contentcredentials.org/`), Content Authenticity Initiative (`https://contentauthenticity.org/how-it-works`), and Adobe Content Credentials overview (`https://helpx.adobe.com/creative-cloud/apps/adobe-content-authenticity/content-credentials/overview.html`) documentation for provenance metadata. Verified 2026-07-10.
- W3C WCAG 2.2 guidance (`https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html`) for three-flashes safety threshold and video accessibility planning. Verified 2026-07-10.
