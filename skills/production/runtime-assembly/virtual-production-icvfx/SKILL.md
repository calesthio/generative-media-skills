---
name: virtual-production-icvfx
description: Plan, troubleshoot, and hand off provider-independent in-camera VFX and LED volume virtual-production work, with Unreal Engine/nDisplay/Live Link awareness. Use for ICVFX suitability, LED stage geometry, frustums, tracking, lens calibration, sync, render nodes, color, lighting/reflections, artifact mitigation, rehearsal, live-composite fallback, monitoring, records, QA, and handoff. Do not use for ordinary offline post compositing, generic storyboards, or full game production.
---

# Virtual Production ICVFX

Use this skill when an agent must help make an in-camera VFX plan, diagnose an LED-volume shoot, prepare a stage/rehearsal/QA checklist, or translate production requirements into a practical virtual-production package. It is provider-independent: it does not assume a particular LED vendor, tracking vendor, media server, camera, or render-node brand. It is Unreal-aware because many ICVFX stages use Unreal Engine, nDisplay, Live Link, Camera Calibration, OCIO, Switchboard, Stage Monitor, Timed Data Monitor, Multi-User Editing, Remote Control, and Composure.

Do not use this skill for ordinary offline green-screen post compositing, generic storyboard advice, previs with no stage or camera-tracked final-pixel intent, full game mechanics, or general Unreal gameplay engineering.

## Source Posture

Label claims as one of these:

- **Documented fact**: backed by official documentation, standards, or vendor-neutral technical references.
- **Dated engine detail**: behavior documented for Unreal Engine documentation pages verified on 2026-07-11. Recheck before making purchase, version-lock, or stage-build decisions.
- **Production heuristic**: stage practice that is useful but must be tested with the actual camera, lens, LED, processor, tracking, sync, content, and color pipeline.
- **Observation to verify**: plausible diagnosis that needs a stage test, measurement, or vendor/stage confirmation.

Authoritative sources used for this skill, verified 2026-07-11:

- Epic Games, In-Camera VFX Overview: https://dev.epicgames.com/documentation/en-us/unreal-engine/in-camera-vfx-overview-in-unreal-engine
- Epic Games, nDisplay Overview: https://dev.epicgames.com/documentation/en-us/unreal-engine/ndisplay-overview-for-unreal-engine
- Epic Games, nDisplay Configuration File Reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/ndisplay-configuration-file-reference-for-unreal-engine
- Epic Games, Live Link: https://dev.epicgames.com/documentation/en-us/unreal-engine/live-link-in-unreal-engine
- Epic Games, Timecode and Genlock: https://dev.epicgames.com/documentation/en-us/unreal-engine/timecode-and-genlock-in-unreal-engine
- Epic Games, Synchronization in nDisplay: https://dev.epicgames.com/documentation/en-us/unreal-engine/synchronization-in-ndisplay-in-unreal-engine
- Epic Games, Camera Lens Calibration: https://dev.epicgames.com/documentation/en-us/unreal-engine/camera-lens-calibration-in-unreal-engine
- Epic Games, Color Management with OpenColorIO: https://dev.epicgames.com/documentation/en-us/unreal-engine/color-management-with-opencolorio-in-unreal-engine
- OpenColorIO documentation: https://opencolorio.readthedocs.io/en/latest/
- ACES documentation: https://docs.acescentral.com/
- OSHA Electrical safety topic: https://www.osha.gov/electrical
- OSHA Heat safety topic: https://www.osha.gov/heat-exposure
- OSHA Evacuation Plans and Procedures eTool: https://www.osha.gov/etools/evacuation-plans-procedures
- UK Health and Safety Executive, Event safety: https://www.hse.gov.uk/event-safety/
- W3C WCAG 2.2, Three Flashes or Below Threshold: https://www.w3.org/TR/WCAG22/#three-flashes-or-below-threshold
- FDA Laser Products and Instruments: https://www.fda.gov/radiation-emitting-products/home-business-and-entertainment-products/laser-products-and-instruments

## What ICVFX Is Actually Solving

**Documented fact:** Unreal's ICVFX overview defines in-camera VFX as a live-action method using LED lighting, camera tracking, and real-time rendering with off-axis projection to create final-pixel or near-final images in camera. The camera-visible region is the **inner frustum**: it updates with the tracked camera's position, orientation, and lens field of view. The camera-outside region is the **outer frustum**: it remains stable enough to provide lighting and reflections from the virtual world.

The point is not simply to put a pretty plate on a wall. A valid ICVFX plan must answer:

1. Can the shot tolerate the LED volume's spatial, color, refresh, brightness, and resolution limits?
2. Can the real camera, virtual camera, lens data, tracking data, and rendered frame be aligned in time and space?
3. Can the content run at the required frame rate with consistent quality across all render nodes?
4. Can the LED surface light the real set and reflective objects without unacceptable artifacts?
5. Is there a rehearsed fallback if final-pixel capture fails?

## Safety, Rights, and Data

ICVFX plans are not safety authorizations. A production agent can identify risks and required records, but qualified stage authority, production safety, rigging, electrical, laser/radiation, stunt, child/welfare, legal, privacy, and data-protection leads must approve the actual work.

**Documented fact:** OSHA describes electricity as a serious workplace hazard with risks including electric shock, electrocution, fires, and explosions; its electrical topic also names frequent construction electrical injury causes such as missing ground-fault protection, discontinuous paths to ground, improper equipment use, and extension/flexible cord misuse. OSHA's heat topic states that occupational heat illness can occur indoors or outdoors, is preventable, and is associated with heavy physical activity, hot environments, lack of acclimatization, and clothing that holds in body heat. OSHA's evacuation material covers emergency action planning, and HSE event-safety guidance frames safe events as work to plan, manage, and review. W3C WCAG 2.2 says content must not flash more than three times in any one-second period unless below general and red flash thresholds. FDA describes laser hazard classes I-IV, with higher classes posing greater injury potential; class IIIb and IV products can create immediate eye or skin hazards, and class IV may also present fire hazards.

Operational checklist:

- Authority: name the person with stop-work authority for LED wall operation, electrical distribution, rigging, moving platforms, tracking hardware, emergency action, and performer welfare. Do not let a creative or software operator override a safety call.
- LED exposure: record operating brightness, refresh/scan settings, intended shutter/frame-rate range, content with flashes/strobes/rapid high-contrast cuts, and any photosensitivity review. Production heuristic: keep flashing content below WCAG-style three-flash thresholds unless the qualified safety/medical/accessibility review explicitly clears the exposure context; warn crew and performers before tests.
- Physical hazards: confirm electrical load/distribution, grounding/GFCI or local equivalent, cable runs, trip protection, rigging certification, overhead loads, egress paths, heat buildup around LED/processors/render nodes, ventilation, moving rigs, vehicle platforms, turntables, cranes, lifts, and emergency stop procedures.
- Tracking hazards: document IR, laser, radio, optical-marker, LiDAR, or other tracking emissions and line-of-sight needs; obtain laser/radiation safety review for any class or wavelength that could expose eyes, skin, camera sensors, or reflective props.
- Vulnerable performers: treat children, older performers, pregnant performers, disabled performers, performers with epilepsy/photosensitivity, heat sensitivity, sensory sensitivity, or restricted mobility as requiring explicit welfare planning, breaks, consent handling, guardians or advocates where applicable, and egress/blocking rehearsal.
- Rights clearance: confirm asset, scan, plate, artwork, logo, product, trademark, map, location, vehicle, wardrobe, and signage rights before content is loaded to the wall or captured in final-pixel plates. LED playback can make an uncleared asset part of principal photography, not just a temporary reference.
- Likeness and scan consent: obtain explicit consent and usage limits for body, face, voice, motion, photogrammetry, LiDAR, witness-camera footage, mocap/tracking data, and any digital double or crowd replication use.
- Data minimization: define who can access tracking, lens, timecode, camera, take, witness-camera, scan, and rehearsal data; retain only what production, VFX, insurance, legal, and archive needs require; redact private locations, minors' information, health accommodations, and unneeded biometric detail from routine handoff.
- Final-pixel versus fallback records: every take should be labeled final-pixel, live comp, green fallback, clean plate, rehearsal, or test. Keep fallback records good enough for post: camera originals, timecode, tracking, lens data, calibration, wall state, color state, clean plates, and incident notes.

Production heuristic: safety, rights, and privacy checks belong in tech scout, rehearsal, call sheet, data-wrangling, and handoff workflows. If they are left until camera roll, the practical answer is usually to reduce brightness/motion, simplify blocking, switch to fallback, remove uncleared content, or stop until authority clears the risk.

## Suitability Triage

Start with shot suitability before prescribing hardware or Unreal settings.

Strong ICVFX candidates:

- Camera can stay within a known tracking volume and a tested range of lens/focus/iris settings.
- Background can be rendered in real time at the required frame rate without volatile screen-space seams or node divergence.
- Foreground set and props benefit from LED lighting/reflections.
- Composition does not require viewing the LED plane in sharp focus at a distance/angle that reveals moire, scan, panel seams, or pixel structure.
- Art direction accepts real-time lighting tradeoffs, baked assets, level-of-detail management, and prebuilt shot states.

Weak or risky candidates:

- Macro, long-lens, or shallow-stage setups where the LED plane must be sharp or near focus.
- Highly reflective foregrounds that reveal the LED wall as a panel array rather than a plausible environment.
- Very fast pans, rolling-shutter stress, strobing practicals, or high-speed capture without a tested sync path.
- Scenes requiring complex destructive simulation, path-traced-quality lighting, heavy translucency, or screen-space effects across node boundaries.
- Camera moves that leave the calibrated tracking volume or see beyond LED coverage.
- Shots whose success depends on last-minute content changes that cannot be rebuilt, optimized, and rehearsed.

Production heuristic: when the shot has high ICVFX value but high final-pixel risk, plan it as an LED-lit live-composite/green fallback from the beginning instead of discovering that fallback on the shoot day.

## LED Stage Planning

Map the stage to the camera, not just to the room.

Required stage facts:

- Wall shape: flat, curved, corner, horseshoe, 270-degree volume, ceiling, floor, set-window insert, car-process wall, or hybrid.
- Physical dimensions in meters; cabinet dimensions; cabinet resolution; pixel pitch in millimeters; processor canvas layout; scan/refresh behavior; panel brightness and operating brightness.
- Camera positions, lens list, subject distances, minimum distance from camera/subject to LED, expected focus distances, and maximum camera angle to panel surface.
- Whether the LED should be final background, lighting/reflection source, live comp background, or all three.

**Documented fact:** Epic states that LED stage design drives the rest of the setup; a 270-degree enclosed volume may be required for fully virtual environments, while a one-sided or curved wall can work when physical set pieces carry much of the scene. LED ceilings are useful for ambient lighting and reflections. Pixel pitch is the distance between LED lights in millimeters, with lower pitch generally increasing pixel density and cost; lower pitch alone does not guarantee suitability because viewing angle, color shift, consistency, heat, and other factors also matter.

Production heuristic for pixel pitch and viewing distance:

- Treat manufacturer pitch charts as a starting point, not an answer. Test with the actual camera sensor, OLPF, lens, focus distance, shutter angle, frame rate, compression path, and show LUT.
- The focus plane should usually sit in front of or behind the LED surface so the panel is slightly out of focus. Epic explicitly recommends avoiding focus on the LED surface to reduce moire risk.
- Severe camera angles to the LED surface increase moire risk. Prefer perpendicular or modest angles when final-pixel background is critical.
- Content with fine repeated lines, high-contrast grills, tiny specular points, scrolling text, or high-frequency texture is more likely to alias on LED.

Stage planning output should include a camera-facing diagram or table:

- Screen segment name and real dimensions.
- Distance from principal camera positions to LED.
- Minimum actor/set distance to LED.
- Pixel pitch and processor resolution per segment.
- Expected inner-frustum coverage and overscan.
- Non-camera LED used for lighting/reflection only.
- Risk notes for moire, seams, angles, and reflections.

## Unreal-Aware System Topology

**Dated engine detail:** Epic's nDisplay documentation describes a cluster with one primary node and any number of secondary nodes. Each Unreal instance renders one or more viewports for one or more displays. A shared nDisplay configuration asset records cluster PCs, windows, viewports, display geometry, projection policy, output mapping, cameras, and transforms. Switchboard launches the cluster.

Typical ICVFX topology:

- House sync/master clock feeding cameras, video devices, GPU sync, and other timing-critical systems.
- Production camera with camera tracking and lens encoder data.
- Tracking server or tracking vendor system sending camera transform and possibly lens data.
- Unreal primary/operator workstation for setup, Switchboard, Remote Control, and cluster control.
- nDisplay render nodes driving wall processors or GPU outputs.
- Optional Unreal editor/tech-art workstation in Multi-User Editing.
- Optional record workstation using Take Recorder or equivalent capture for camera, lens, light, prop, and shot-state data.
- Optional compositing workstation for live Composure/green fallback.
- Video village, waveform/vectorscope/color tools, and recording/playback systems.
- Protected high-throughput LAN for Unreal, tracking, Live Link, Switchboard, source control, and monitoring traffic.

## nDisplay Geometry, Projection, and Frustums

**Dated engine detail:** nDisplay config values for physical/virtual measurements are in meters and degrees unless otherwise specified; window and viewport values are in pixels. Screen configurations define rectangles in 3D space, usually matching the physical display surfaces. Viewports render into rectangular areas of an application window. Projection policies define how the view is rendered, including simple planar screens and calibrated projection methods such as MPCDI, VIOSO, EasyBlend, DomeProjection, mesh, and manual/camera policies. Epic's config reference says nDisplay currently supports MPCDI 1.0, 2D and A3D profile types.

For an ICVFX agent, the critical reasoning is:

- The physical LED geometry, nDisplay screen/mesh geometry, and stage coordinate system must agree.
- The tracked camera must resolve to the same origin and axes as the nDisplay root and virtual environment.
- Inner-frustum view should be rendered from the camera perspective and sized with enough overscan for latency, tracking jitter, lens breathing, camera motion, and operator safety.
- Outer frustum should prioritize stable lighting and reflections. It should not slide with the camera in a way that makes reflections feel attached to the lens.
- Calibrated curved or irregular displays usually require a proper projection/calibration policy rather than pretending the wall is a flat screen.

Ask for or produce these nDisplay artifacts:

- nDisplay Config Asset or exported `.ndisplay`/`.cfg` where applicable.
- Cluster node list: hostnames/IPs, GPU IDs, application windows, viewports, processor mapping, and failover expectations.
- Display geometry: real measurements, coordinate origin, screen normals, arc radius, ceiling/floor relationship, and mesh/calibration files if used.
- ICVFX camera settings: inner/outer frustum settings, overscan, soft-edge/feather if available, hidden markers, green fallback state, GPU assignment if multi-GPU is used.

## Content and Performance

ICVFX content is stage software. It must be authored for deterministic real-time playback, not just visual approval in an editor viewport.

Production heuristics:

- Build shot-specific levels or shot states instead of one massive all-purpose scene when reliability matters.
- Prefer baked lighting, optimized reflection strategies, stable LODs, Nanite/Lumen/Virtual Shadow Maps only when tested on the actual cluster and engine version.
- Avoid last-minute high-frequency textures, dense foliage shimmer, tiny emissive details, screen-space-dependent effects, heavy translucency, particle storms, and expensive dynamic GI unless tested under cluster load.
- Lock exposure, color transforms, level variants, time-of-day, and interactive controls per shot or per rehearsal state.
- Budget for the worst inner-frustum camera move, not the average editor preview.

**Documented fact:** Epic warns that screen-space effects such as SSGI, SSAO, SSR, vignetting, eye adaptation, and bloom should be avoided in nDisplay ICVFX contexts because screen-space effects can cause issues at borders between clustered nodes. Treat this as a serious review point, not a style preference.

Performance checks should include:

- Cluster frame time on every node.
- Inner-frustum cost versus outer-frustum cost.
- GPU, CPU, network, storage, and video I/O headroom.
- Node boundary tests with high-motion objects.
- Rehearsal with production camera, real tracking, real LED brightness, and final color path.

## Tracking and Lens Calibration

**Documented fact:** Unreal Live Link is an extensible framework for streaming live data into Unreal, with roles such as cameras, lights, transforms, characters, and basic data. Live Link sources manage incoming data; subjects are the streams. Live Link can evaluate using engine time, latest frame, or timecode. Epic warns not to use Timecode evaluation mode when the engine has no Timecode provider. UDP Messaging may need explicit network-adapter configuration, and packaged game use may require `-messaging` for message bus workflows.

**Documented fact:** Epic's Camera Calibration plugin creates Lens File assets containing calibration data for camera/lens alignment and lens distortion. It supports workflows to model lens distortion and nodal point offset and can apply distortion to Cine Camera actors or Composure CG layers.

Practical calibration package:

- Tracking system coordinate-frame alignment to Unreal axes and stage origin.
- Camera body tracking offset from tracker rigid body to optical center/nodal point.
- Lens File or equivalent calibration per camera/lens/encoder range.
- Distortion, focal length, focus, iris, entrance-pupil/nodal offset, and lens breathing behavior where relevant.
- Time alignment between video, tracking, lens metadata, and Unreal frame evaluation.
- Test chart captures and solved residual/error notes.

Production heuristics:

- Recalibrate after lens changes, camera-body changes, tracker remount, focus motor changes, large temperature shifts, or stage origin adjustments.
- A camera can be visually close but temporally wrong. If parallax swims during moves, test latency/timecode before blaming spatial calibration.
- Track and record lens metadata even if the shot seems locked; editorial, VFX, and troubleshooting benefit from proof.
- Use hidden tracking markers for green fallback only if they are outside final crop or are planned for removal.

## Timecode, Genlock, and Sync

**Documented fact:** Epic distinguishes timecode from genlock. Timecode makes Unreal adopt timecode values from a specified source; genlock locks engine frame production to a video/reference input so Unreal generates one output frame for each input frame. Unreal can visualize timecode through the Timecode Provider panel or `stat timecode`.

**Documented fact:** Epic's nDisplay sync documentation separates software synchronization from hardware/OS display synchronization. Software barriers coordinate simulation/render timing across nodes. Hardware synchronization uses professional GPUs/sync cards and a shared clock to present frames without tearing. Epic describes genlock plus framelock as the most desirable approach for virtual production and lists nDisplay render sync policies: None, Ethernet, NVIDIA, and Custom. NVIDIA policy uses hardware framelock through NVIDIA SwapLock API. Epic recommends testing sync with a fast-moving object crossing display boundaries.

Stage sync plan should answer:

- What is the house frame rate and reference format?
- Which device is the master clock? How is sync distributed?
- Are camera, tracking, video I/O, Unreal, render nodes, LED processors, recorders, and monitors all locked or explicitly free-running?
- What is the Live Link evaluation mode and buffer/offset strategy?
- What is the nDisplay render sync policy?
- How is sync verified before camera rolls?

Incident pattern examples:

- Tearing or one-node edge discontinuity: verify nDisplay render sync policy, GPU sync cabling, Mosaic/Eyefinity, driver/control-panel sync state, and node frame time.
- Correct still alignment but moving parallax swim: verify timecode provider, Live Link evaluation, tracking latency, lens data latency, and camera/video path latency.
- Intermittent dropped node: inspect network timeouts, node health, failover policy, thermal/power state, and Stage Monitor events.

## Color Pipeline, OCIO, and LED Reality

**Documented fact:** OpenColorIO is a color-management solution geared toward motion-picture production, VFX, and computer animation. OCIO is compatible with ACES and supports sophisticated production configurations. ACES is an industry standard for managing color and digital files through a production lifecycle, including capture, editing, VFX, mastering, presentation, archive, and remastering.

**Dated engine detail:** Unreal Engine 5 supports OCIO v2. Unreal can apply OCIO to media sources, viewport/PIE, Composure, Movie Render Queue, and nDisplay renders, including entire clusters, inner frustums, or individual nodes. Unreal uses an OpenColorIO Configuration Asset referencing an `.ocio` config file.

**Documented fact:** Epic's ICVFX overview says to verify the final image through the live-action camera, test live-action assets on stage with the LED volume as a light source, avoid changing cameras across shots when consistency matters, and disable the Unreal tonemapper so engine output to LED panels is in linear sRGB as input, using `ShowFlag.Tonemapper 0`.

Production heuristic: adopting OCIO or ACES vocabulary does not make the wall calibrated. Measured LED calibration, processor and camera tests, monitoring transforms, camera-view verification, and controlled viewing conditions remain necessary.

Color plan contents:

- Show color pipeline: camera log/color space, on-set LUTs, OCIO config, LED processor calibration/LUTs, monitor transforms, live comp transforms, dailies transforms, and delivery color expectations.
- Who owns transforms: color scientist/DIT, virtual art department, Unreal operator, LED tech, compositing supervisor.
- Reference captures: grey card, color chart, skin tone, key props, practical lights, reflective/chrome reference, and stills through the taking camera.
- LED measurement: brightness setting, white point, primaries/gamut behavior, panel uniformity, black floor, scan/refresh constraints, viewing-angle color shift, and processor settings.
- Records: exact OCIO config hash/version, LED processor project, Unreal project commit/build, media profile, show LUTs, camera LUTs, monitor LUTs, and take-specific adjustments.

Production heuristics:

- Do not assume the LED wall is a reference monitor. It is a light source, background, and reflective environment with camera-dependent behavior.
- Validate through the camera pipeline, not only by eye on the wall.
- If the LED content is used mainly for reflection/illumination, color decisions may prioritize plausible light response over wall-only beauty.
- Avoid unrecorded per-node or processor-side tweaks. They are expensive to reconstruct later.

## Lighting, Reflections, and Physical Integration

ICVFX succeeds when physical foregrounds, LED light, practicals, and virtual environment agree.

Checklist:

- Determine whether LED is key, fill, ambient, reflection, background, or all of those.
- Match virtual sun/sky/practicals to physical set lighting direction, softness, intensity, and color.
- Use LED ceiling/side returns when reflective props, vehicles, helmets, glasses, water, or polished floors need plausible environment coverage.
- Test exposure and black floor with wardrobe, skin, hair, glass, chrome, and dark props.
- Put highly reflective objects through rehearsal; they reveal wall gaps, ceiling absence, processor seams, and outer-frustum errors.
- Plan negative fill and physical flags. LED volumes can overfill and flatten faces.
- If physical lighting must dominate, make sure the wall content still reads correctly under the taking camera exposure.

Production heuristic: reflections often show ICVFX mistakes earlier than the direct background. A chrome ball, grey ball, color chart, and representative hero prop should be part of stage tests.

## Moire, Scan, Rolling Bands, and Other LED Artifacts

Artifact triage:

- Moire: panel pixel grid interacts with camera sensor/photosite pattern or focus plane. Mitigate by changing camera distance, focus, aperture/depth of field, lens, focal length, angle, wall content frequency, pixel pitch, or panel choice.
- Scan/rolling bands: camera shutter/scan conflicts with LED refresh/scan/processor settings. Mitigate by testing shutter angle, frame rate, phase, LED refresh settings, camera sync, and processor configuration.
- Panel seams/cabinet mismatch: calibration, brightness/color mismatch, physical alignment, thermal drift, or content crossing cabinet boundaries.
- Node seams: nDisplay sync, color transform mismatch, projection mismatch, exposure/eye adaptation, screen-space effects, or divergent scene state.
- Reflected LED structure: wall is too sharp/close/bright in reflective prop; add diffusion, alter angle, change content, use physical reflection cards, or plan comp cleanup.

Always diagnose artifacts through the taking camera and record the test conditions. Wall-only inspection can miss camera-sensor interactions.

## Rehearsal, Roles, and On-Set Control

Minimum roles for serious ICVFX:

- Director/DP: shot intent, lensing, exposure, blocking, lighting taste.
- Virtual production supervisor: technical/creative authority across stage, camera, Unreal, tracking, color, and workflow.
- Unreal/nDisplay operator: cluster, levels, ICVFX camera, Switchboard, scene states.
- Tracking/lens technician: camera tracking health, lens data, calibration, latency checks.
- LED engineer/processor operator: processor mapping, brightness, scan, panel health, calibration.
- DIT/color scientist: color pipeline, monitoring, charts, LUT/OCIO records.
- VAD/tech artist: optimized content, set dressing, lighting states, fixes.
- Gaffer/key grip: physical light and rig integration with LED output.
- Script supervisor/data wrangler: take records, state changes, incidents, metadata.

Rehearsal should include:

- Full camera move at speed, with final lens/focus/iris and production shutter.
- Node-boundary and frustum-boundary stress tests.
- Moire tests with chart-like content and hero wardrobe/props.
- Tracking loss/occlusion test and recovery path.
- Green fallback state and live comp check.
- Restore-from-snapshot or source-control rollback test.
- Data-recording test: camera, lens, timecode, tracking, Unreal state, color, LED settings, and take naming.

## Live Composite and Green Fallback

**Documented fact:** Epic documents a fallback where the inner frustum can become green screen with adjustable tracking markers while the outer frustum continues to display the Unreal environment for lighting and reflections. This reduces required green-screen area, can reduce green spill, and preserves LED lighting/reflection benefits. Composure is Unreal's real-time compositing framework and can include live video feeds, AR compositing, keying, garbage mattes, color correction, and lens distortion.

Fallback planning:

- Decide before shoot which shots are final-pixel candidates, live-comp candidates, and green fallback candidates.
- Prepare a green inner-frustum state with markers, spill expectations, garbage matte strategy, and matching color pipeline.
- Keep outer frustum environment active for lighting/reflections if it benefits the foreground.
- Record clean plates, tracking, lens data, timecode, Unreal scene state, wall state, and live comp preview.
- Do not promise that live comp preview equals final post quality unless the comp pipeline and deliverable are defined.

## Monitoring, Incidents, and Records

**Documented fact:** Epic describes Stage Monitor as a tool for receiving event reports from multiple Unreal instances in a live setup, and Timed Data Monitor as a way to configure and visualize how incoming timed data such as SDI frames and Live Link tracking relate to engine time. Level Snapshots can save and restore actor configurations and help reset virtual environments between takes.

Use monitoring to answer what changed, not only what broke.

Minimum records per setup/take:

- Unreal project version/commit, packaged build, map/level, Level Snapshot or shot state.
- nDisplay config, Switchboard config, render-node list, GPU/driver versions if available.
- Live Link sources/subjects/evaluation modes, timecode provider, custom timestep/genlock state.
- Camera body, sensor mode, frame rate, shutter, ISO/EI, lens, focal length, focus, iris, filters.
- Lens File/calibration version and tracker rigid-body offset.
- LED processor project, brightness, refresh/scan settings, wall calibration, active content version.
- OCIO config, show LUTs, monitor LUTs, camera LUTs, per-node transforms.
- Safety/rights/data status: stage authority approvals, flash/brightness notes, moving-rig/laser/tracking restrictions, asset/plate/trademark clearance, likeness/scan consent limits, and retention/access rules for tracking, lens, take, witness-camera, and scan data.
- Incident log: timecode, take, symptom, suspected cause, fix, retest result, and whether editorial/VFX must know.

## QA and Handoff

Do not hand off only a pretty take. Hand off evidence.

Pre-shoot QA:

- Stage geometry matches nDisplay geometry.
- Qualified stage authority has cleared electrical distribution, rigging, egress, heat, moving rigs, tracking emissions, LED brightness/flicker/photosensitivity risks, performer welfare accommodations, rights clearance, consent, and data-retention rules.
- Camera/lens/tracking calibration has been tested at shot distances and lens settings.
- House sync, timecode, Live Link timing, and nDisplay sync pass boundary tests.
- Content hits frame-rate target on every render node with headroom.
- Screen-space effects and auto-exposure/eye-adaptation risks are reviewed.
- Color path is documented and verified through taking camera.
- Moire/scan tests are shot and reviewed.
- Green fallback state is rehearsed.

Shoot-day QA:

- Confirm timecode/genlock/cluster health before each setup.
- Roll a chart/reference at the beginning of major lighting or content changes.
- Log every content, color, processor, camera, lens, tracking, and sync change.
- Recheck calibration after physical changes.
- Capture incident evidence, not just verbal notes.

Handoff package:

- Shot/take list with final-pixel/live-comp/fallback status.
- Camera originals, audio/timecode references, and video village references as available.
- Tracking and lens metadata.
- Unreal project/build references, nDisplay config, Level Snapshots/shot states, take recordings, and content versions.
- Color/OCIO/LUT/LED processor records.
- Calibration assets and calibration reports.
- Incident log and known limitations.
- Notes for editorial/VFX: where wall artifacts, live comp, green fallback, or cleanup are expected.

## Complete Example: Car Process Final-Pixel Candidate

Example, not a mandatory formula.

Production intent: dialogue in a stationary car at dusk, seen through windshield and side windows, with moving city reflections on glass and paint. The director wants final-pixel backgrounds if possible, but editorial can accept live-comp fallback for two risky angles.

Inputs and constraints:

- Curved LED wall behind and around car, plus ceiling strip for reflections.
- Camera A: 24 fps, 180-degree shutter, 35 mm and 50 mm lenses, mostly locked-off and small slider moves.
- Strong reflective windshield, black paint, glasses on actor.
- Unreal/nDisplay cluster driving wall segments; tracking available for slider camera.

Recommended approach:

1. Classify wide and medium shots as final-pixel candidates; classify tight windshield reflections and extreme side angle as fallback candidates.
2. Build shot-specific Unreal states: dusk street, traffic light passes, storefront parallax, and reflection-only side/ceiling content.
3. Test pixel pitch and moire at actual camera distance with windshield focus, actor focus, and background focus. Prefer actor focus with LED sufficiently soft.
4. Calibrate tracked camera and lens for the 35 mm and 50 mm ranges used in shot. Record lens encoder data even for locked-off takes.
5. Use inner frustum for camera-visible background with overscan; keep outer/ceiling frustum stable for light and reflection.
6. Disable or replace screen-space effects that cause node seams. Test traffic-light motion crossing processor and node boundaries.
7. Build green inner-frustum fallback with outer frustum still displaying city lighting/reflections.
8. Record charts through windshield and clean plates with LED states.

Expected result: final-pixel capture for stable angles; fallback captures retain useful windshield and paint reflections because outer/ceiling LED remains active.

Likely failure modes:

- Moire in distant high-rise windows or street grids.
- Reflections reveal wall seams or ceiling absence.
- Moving city lights create scan bands with shutter/refresh settings.
- Parallax swim if tracking latency is not aligned.

Meaningful variations:

- If the car has no reflective hero surfaces, ceiling LED may be less important.
- If camera is fully locked, tracking may be minimized but lens, color, and sync still need records.
- If background must be sharp, test lower pixel pitch or change blocking before assuming final-pixel feasibility.

## Complete Example: Incident Diagnosis Response

Example, not a mandatory formula.

User request: "During a handheld move, the LED background looks aligned at the start mark, but it swims behind the actor during the move. Static charts look fine. What should we check?"

Good response:

1. Label this as an observation to verify: static spatial calibration may be acceptable, but timing or dynamic lens/tracking data may be off.
2. Check timecode/genlock: confirm Unreal has the intended Timecode Provider and Custom TimeStep, and confirm frame rate through the Timecode Provider panel or `stat timecode`.
3. Check Live Link evaluation mode and offsets: if Timecode mode is used, confirm the engine has a Timecode provider; otherwise test engine-time/latest modes with controlled offsets.
4. Check tracking latency and smoothing: disable excess smoothing for a test, compare fast pan/translation against a known marker, and inspect Timed Data Monitor.
5. Check lens metadata latency: focal length/focus/iris updates can lag transform data, especially during focus pulls or zooms.
6. Check camera-to-tracker rigid-body offset and nodal calibration under motion, not just on a static chart.
7. Run a repeatable move with timecode slate/reference and record tracking, lens, and camera video for later analysis.

Why this structure works: the symptom changes during motion, so the response prioritizes temporal alignment and dynamic metadata before rebuilding spatial calibration from scratch.

## Complete Example: Handoff Checklist for a Green Fallback Shot

Example, not a mandatory formula.

Production intent: hero actor in front of LED-lit alien landscape. Final-pixel failed because panel structure appears in shallow-focus reflections on helmet. Inner frustum is switched to green; outer frustum remains the alien landscape for lighting and reflections.

Handoff package:

- Takes labeled as green fallback, not final-pixel.
- Camera originals, timecode, and live comp preview.
- Tracking data and lens metadata for every take.
- Lens File/calibration version and tracker offset.
- Unreal project/build, map, Level Snapshot, nDisplay config, and green inner-frustum state.
- Outer-frustum content version and LED processor settings used for reflections.
- OCIO config, camera LUT, monitor LUT, and any live comp transforms.
- Clean plate with green inner frustum, outer-frustum lighting active, and no actor.
- Grey/chrome/color chart through taking camera under the same LED state.
- Incident note: final-pixel rejected due to helmet reflection resolving panel structure; cleanup expected in helmet edge reflections; outer-frustum reflection retained intentionally.

Expected result: editorial and VFX can reconstruct the intended background, use the recorded tracking/lens data for comp, and understand why LED reflections should remain part of the plate.
