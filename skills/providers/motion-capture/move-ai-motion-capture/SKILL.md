---
name: move-ai-motion-capture
description: Use this skill when planning, capturing, processing, validating, troubleshooting, or exporting markerless human motion capture with Move AI products, including Move One single-camera workflows and Genesis multi-camera studio systems. It covers provider selection, setup, calibration, wardrobe and lighting constraints, documented multi-person operation, processing, cleanup, skeleton and retargeting choices, DCC/game-engine export, data management, consent, and privacy. Do not use it for general keyframe animation, non-Move mocap systems, 3D asset generation, or generic animation cleanup unrelated to Move AI outputs.
---

# Move AI Motion Capture

Use this skill to turn a Move AI capture request into a production-safe motion-capture plan. Move AI is a markerless human motion-capture provider; treat quality, capacity, and workflow statements here as provider claims unless a source is explicitly independent.

Verification date for volatile product facts: 2026-07-11.

## Scope boundary

Use Move AI when the task is to extract human body motion from video and deliver animation data, preview media, biomechanics data, or retargetable skeleton animation. The relevant public product split is:

- Move One: single-camera capture and upload workflow for one performer, using the Move One iOS app or a supported uploaded video file.
- Genesis: enterprise multi-camera markerless mocap system using Z CAM cameras, local processing, calibration, actor profiles, and studio pipeline export.

Do not use this skill for general animation direction, hand-keyed animation, generative 3D character creation, face performance capture beyond what is documented by Move AI, cloth simulation, or non-Move mocap systems.

API boundary, verified 2026-07-11: Move AI's Privacy Policy defines App/API coverage that includes a Move API Portal at `dev.move.ai` and single/multi-camera API at `api.move.ai`, and the terms page links API-related EULAs such as Move One API EULA. Public pages establish that API-related services and contracts exist, but they do not provide a complete public endpoint/authentication/quota reference in the consulted documentation. Do not invent endpoints, auth flows, quotas, SDK packages, or rate limits. For integration work, require the user's portal documentation, EULA/order form, and contract-specific technical spec before writing production code. Sources: https://move.ai/privacy-policy and https://move.ai/terms-of-use.

## Evidence labels

- Documented fact: stated by Move AI official pages or knowledge-base articles, verified 2026-07-11 unless otherwise dated.
- Provider claim: Move AI marketing, quality, or comparative assertion that should not be repeated as independent proof.
- Production heuristic: practical capture or pipeline guidance inferred from mocap practice and Move AI constraints; verify on a pilot take before relying on it.

## Product selection

### Choose Move One when

Documented facts:

- The shoot is single-camera and single-performer. Move AI's single-file upload article says it is for capturing a single person using a single camera, and recommends a locked camera with a single person centered in frame.
- The team needs a light capture workflow: place a phone vertically or horizontally, record, upload, and let the system process.
- The capture can fit the current Move One duration limit. Move AI states that a paid plan can capture up to 60 seconds.
- The source is an existing video that meets upload limits: Move AI documents single-file upload support for `.mp4`, `.mov`, and `.avi`, maximum file size 1 GB.
- The desired outputs are Move One-supported gallery/export formats: `.fbx`, `.usdc`, `.blend` requiring Blender 4 or newer, `.usdz`, output `.mp4`, input `.mp4`, and biomechanics output through the platform gallery. Gallery view lists `usdz`, `blend`, `usdc`, motion-data biomechanics joint data, and `fbx`.

Production heuristics:

- Use Move One for previsualization, social/creator animation, solo game animation tests, quick stunt blocking, and cases where the cost or logistics of multicamera capture are unjustified.
- Avoid Move One for complex contact, frequent occlusion, performer interaction, crowded scenes, long takes, or deliverables where every limb trajectory must survive close technical scrutiny without reshoot time.

### Choose Genesis when

Documented facts:

- The project needs a multi-camera markerless studio setup. Move AI describes Genesis as an enterprise-grade markerless system.
- The project needs local processing. Move AI's product page states Genesis runs on premise using Nvidia GPUs through a desktop application.
- The capture volume, camera count, or performer count exceeds Move One's public single-camera/single-performer workflow. Move AI's product page lists 6-12 Z CAMs, a volume range from 4 x 4 m to 20 x 20 m, and 1-8 person capture.
- The production needs individual per-actor files and a consolidated multi-track master file. Genesis output documentation says multi-actor sessions provide individual files for each actor and a consolidated master file containing all tracks.
- The pipeline needs formats beyond Move One's public list, including Genesis-documented FBX, BVH, GLB, USDZ, Blender, C3D, JSON, camera/render preview MP4, and diagnostic visualization AVI.

Provider claims:

- Move AI describes Genesis as delivering data quality directly comparable to optical systems and optical-quality data. Treat this as a provider claim unless the production runs its own comparison against optical reference or independent tests.
- Move AI says Genesis uses checkerboard calibration and actor profiles for consistent pipeline-ready output. Validate consistency against your own rig and animation standards.

Production heuristics:

- Use Genesis for multi-person scenes, staged combat, dance ensembles, interactive blocking, high-value game/VFX animation, local-data requirements, and repeatable studio capture.
- Treat Genesis as a system deployment, not a casual upload tool. Budget for hardware, calibration, storage, operator checks, pilot captures, and pipeline validation.

## Capture setup

### Move One single-camera setup

Documented facts:

- The iOS app capture flow is simple: place the phone down vertically or horizontally, record after countdown, and upload the selected take.
- Single-file upload should be shot at minimum 60 fps and Full HD for optimal results; camera should be locked in position; one person should be centered in frame.
- Supported upload containers for single-file upload are `.mp4`, `.mov`, and `.avi`, with maximum file size 1 GB.

Production heuristics:

- Lock exposure, focus, and white balance if the capture device permits it. Avoid auto-exposure pumping during fast motion.
- Frame the performer full body for the entire action, including hands and feet at extension. Do not let jumps, floor work, weapons, or props leave the frame.
- Use landscape unless a Move AI-documented app workflow or target platform specifically requires portrait. Landscape normally preserves lateral motion and limb visibility better.
- Keep the camera static. Handheld footage creates extra apparent motion that a single-camera mocap solver must separate from body motion.
- Shoot a quick calibration-quality test: walk cycle, arm raises, squat or kneel if relevant, and the hardest action beat. Process before capturing the full shot list.

### Genesis system setup

Documented facts:

- Genesis hardware requirements documented by Move AI include Intel i7/i9 8th generation or newer or equivalent, NVIDIA RTX 40/50/A-series GPU, DDR4 64 GB RAM, SSD NVMe with 80 GB for the application and local processing engines, recommended at least 1 TB project storage, Ubuntu 22.04, and Nvidia Driver 580.
- Move AI recommends Z CAM E2-M4s Mark II as extensively tested and compatible, and also says Z CAM E2-M4 Mark II delivers good results.
- Required Z-Camera operations list includes a minimum of 6 Z CAM E2 M4 Mark II cameras, Laowa 6 mm and 10 mm f/2 Zero-D MFT lenses, FTP shielded Ethernet cables, a PoE+ switch with at least 30 W per camera, AV PRO SE CFexpress B v4 memory cards, a 10 GB network card for faster harvesting, an HDMI monitor, mounts, A1 checkerboard, tape measure, and floor markers.
- Move AI's product page says Genesis uses 6-12 Z CAMs and can be mounted in volumes up to 20 x 20 m.
- Genesis capture and integration uses Peel Capture according to Move AI's product page; Peel Capture can configure and trigger cameras and prepare expected video files.

Production heuristics:

- Before the shoot day, make a capture-volume map with camera IDs, lens choice, height, tilt, cable route, power budget, and blind spots.
- Reserve storage for raw camera media, processed projects, exports, previews, diagnostic visualizations, and backups. Multi-camera raw video grows quickly.
- Name takes with project, scene, performer IDs, action, version, and date before processing. Multi-person sessions become painful if actor identity is only remembered informally.
- Keep a camera-health checklist: timecode/sync, lens cleanliness, focus, exposure, memory card status, network link, camera recording, and frame-rate consistency.

## Calibration and actor profiling

Documented facts:

- Genesis uses checkerboard calibration; Move AI lists A1 checkerboard as required equipment and describes checkerboard calibration as part of the system's consistency story.
- Move AI's Genesis docs include recording and processing actor profiles, and processing action takes using those profiles.
- Genesis viewing tools include a calibration overlay that displays the calibrated active area, representing the capture volume created during calibration.

Production heuristics:

- Calibrate whenever cameras, lenses, mounts, volume boundaries, or lighting conditions materially change.
- Capture actor profiles for each performer in the same footwear, approximate wardrobe bulk, and body proportions expected in action takes.
- Validate calibration with a short full-volume traversal: front/back, diagonals, crouch, jump, arm extension, and close performer interaction if the scene includes contact.
- Reject a calibration before action capture if the overlay, preview skeleton, or volume bounds do not match the physical floor marks.

## Wardrobe, lighting, props, and performance constraints

Documented facts from Genesis performance considerations:

- Avoid baggy or loose clothes because they can deceive the system about body shape.
- Avoid long sleeves that cover wrists because the system needs to see wrists to track hands optimally.
- Choose clothing with strong contrast against the background.
- Avoid clothing that matches the environment, such as white clothing against white walls.
- Use different colored top and bottom garments to help distinguish body segments.
- Avoid black clothing whenever possible because it absorbs light and obscures surface texture.
- Match footwear heel height to the digital rig. If the rig uses high heels, the performer should wear identical heels.
- Use light-colored footwear for contrast against the floor so the system can detect ground contact and improve foot planting.

Production heuristics:

- Prefer matte, fitted, high-contrast garments. Avoid reflective, translucent, heavily patterned, flowing, or limb-obscuring costume pieces unless a pilot proves they solve cleanly.
- Light the whole capture volume evenly enough to preserve visible limb detail from all cameras. Avoid hard moving shadows, strobing LEDs, windows with changing daylight, deep black corners, and blown-out white surfaces.
- Keep key props slim enough to avoid hiding wrists, elbows, knees, and feet. If a prop causes occlusion, run a prop-in-hand test and decide whether to split the action into cleaner beats.
- For floor work, grappling, or overlapping performers, expect more cleanup and use Genesis m2 where documented strengths align with occlusion and complex motion.

## Multi-person capture

Documented facts:

- Move AI's product page lists Genesis as supporting 1-8 person capture.
- Genesis output documentation says multi-actor sessions provide individual files for each actor and a consolidated master file with all tracks.
- Genesis m2 documentation claims superior handling of high-occlusion scenarios with multiple interacting subjects.

Production heuristics:

- Assign visible performer IDs in slate notes and metadata, not on costumes if labels compromise tracking.
- Block multi-person action to preserve limb separation at key storytelling/contact moments. Markerless systems can tolerate interaction, but persistent body overlap still reduces evidence for the solver.
- Capture a clean individual reference move for each performer if the scene has dense contact, then capture the ensemble take.
- Validate identity continuity after processing by scrubbing crossings, hugs, lifts, falls, and close combat beats where track swaps are most likely.

## Processing and cleanup

### Move One

Documented facts:

- Move One app workflow: after a satisfactory take, upload and the system processes it.
- Move Platform gallery shows processed takes in chronological order, newest first, and lets users view input video, output video, and download formats.
- Single-file upload result quality may vary because capture is outside Move AI's control.

Production heuristics:

- Process test takes before recording a full batch. A bad camera angle or wardrobe choice should fail early.
- Keep original input video, processed output, and chosen export together. Do not rely only on the platform gallery as the project archive.
- Cleanup in DCC or engine should focus on foot contacts, hand trajectories, root translation, jitter, retarget offsets, and pose extremes. Do not erase intentional performer timing.

### Genesis

Documented facts:

- Genesis processing includes importing videos into a project, processing action takes, processing actor profiles, viewing/exporting outputs, and viewing mesh, skeleton, and calibration overlays.
- Genesis 3D viewer lets users inspect animation from any angle.
- Output files are accessed from the output button on each action take.
- Diagnostic visualization folders may be generated during processing and are intended for diagnosing tracking issues.

Production heuristics:

- Review each processed take against camera preview and skeleton overlay before export. Scrub at normal speed and frame-by-frame at contacts.
- Use render preview for fast acceptance, then inspect raw skeletal data for technical signoff.
- If a take fails, classify the root cause before recapture: calibration, camera coverage, clothing contrast, lighting, body occlusion, sync/timecode, wrong actor profile, export/retarget settings, or solver/model choice.

## Skeleton, models, retargeting, and exports

### Genesis skeleton and mocap models

Documented facts:

- Genesis m1 is described by Move AI as a first-generation multi-camera model for high-fidelity motion with faster multi-camera processing and actor-profile consistency.
- Genesis m2 is described by Move AI as a second-generation multi-camera model with enhanced spine biomechanics, a new 6 degrees of freedom shoulder model, smoother and more stable motion for complex dynamic scenes, enhanced foot planting, reduced foot sliding, and better handling of high-occlusion multi-subject scenarios.
- Move AI's Genesis retargeting article states m1 and m2 skeletons contain the same joint count and identical hierarchy, 63 joints including Root.
- Move AI says the Move rig uses Forward Kinematics as its primary skeletal animation control method.
- Move AI says translation data is applied to the hips joint and rotation data is applied to associated joints.
- Accurate retargeting requires 1:1 mapping of corresponding joints.

Provider claims:

- Quality improvements assigned to m2 are Move AI claims. Use a side-by-side pilot if the choice affects cost, schedule, or technical acceptance.

Production heuristics:

- Choose m1 when speed and established actor-profile consistency matter more than the documented m2 improvements.
- Choose m2 for extreme spine poses, shoulder-demanding action, complex dynamic scenes, foot-planting-sensitive animation, and multi-subject occlusion.
- Create a retarget map once per target rig and test it with walk, turn, crouch, arm reach, jump/land, and the project's hardest pose.
- Confirm whether the target rig expects root motion on hips, a separate root, or engine-specific root-motion extraction. Fix this before animators clean dozens of takes.

### DCC and engine integration

Documented facts:

- Move One documentation includes workflows for Blender export/plugin, Blender retargeting, NVIDIA Omniverse import, Unreal Engine import, Unreal retargeting, Unreal-to-Metahuman retargeting, Maya HIK retargeting, Cinema 4D retargeting, and Unity retargeting.
- Genesis output formats include FBX, BVH, GLB, USDZ, Blender `.blend`, C3D, JSON, camera/render preview MP4, and diagnostic visualization AVI.
- Move One export formats include FBX, USDC, Blender, USDZ, MP4, and biomechanics output through the gallery.

Production heuristics:

- Use FBX for broad DCC/game-engine interchange, BVH when the downstream tool expects classic mocap hierarchy, C3D for biomechanics/motion-analysis tooling, JSON for custom pipeline integration, and USD-family files where the pipeline is USD-centric.
- Export a short accepted calibration/action take through the full target pipeline before the capture day: Move output, DCC import, retarget, engine import, playback, root motion, scale, orientation, frame rate, and animation compression.
- Keep retarget presets under version control or pipeline asset management. A silent retarget-map edit can invalidate comparisons between takes.

## Validation checklist

Run this before accepting Move AI data as production-ready:

1. Source integrity: input videos exist, file names match shot logs, camera count matches expectation, and no performer lacks consent documentation.
2. Product fit: Move One was not used for multi-person or long/occluded actions; Genesis was justified for multicam, multiperson, local-processing, or high-fidelity needs.
3. Setup: camera locked for Move One; Genesis cameras synced, recording, correctly placed, and calibrated.
4. Wardrobe and lighting: fitted, high-contrast clothing; visible wrists; visible shoes/feet; no black-on-dark or white-on-white conflicts.
5. Solver review: skeleton aligns with body, no persistent limb swaps, no root drift, no impossible knee/elbow flips, no hand/foot snapping that breaks the shot.
6. Contact review: foot plants, landings, hand contacts, prop contacts, lifts, and floor work checked at frame level.
7. Retarget review: target character scale, limb lengths, hips/root behavior, shoulders, spine, and hand reach preserve the performance.
8. Export review: expected files present, frame rate/orientation/units confirmed, preview media archived, diagnostic files retained for failed takes.
9. Privacy and rights: source video, derived motion data, and outputs handled under the production's consent, retention, and access-control plan.

## Troubleshooting decision tree

- Skeleton jitters everywhere: check source frame rate, blur, exposure, lighting flicker, camera stability, calibration, and sync/timecode before blaming retargeting.
- One limb repeatedly fails: check clothing contrast, wrist/ankle visibility, prop occlusion, camera coverage, and whether the limb leaves frame.
- Foot sliding: check footwear contrast, floor visibility, target-rig scale, root-motion handling, retarget foot locks, and whether the selected Genesis model/preset is appropriate.
- Actor identity swaps in multi-person Genesis: inspect crossing/occlusion moments, actor profile usage, calibration, camera coverage, and whether the scene should be split or reblocked.
- Good Move output looks wrong in engine: inspect import scale, axis orientation, frame rate, root-motion extraction, skeleton mapping, animation compression, and retarget pose.
- Upload fails or is rejected: for Move One single-file upload, verify `.mp4`, `.mov`, or `.avi`, file size no larger than 1 GB, and account/platform access.
- Export is missing an expected format: confirm whether the format belongs to Move One or Genesis, whether it is available in platform gallery or local Genesis output, and whether required plugins such as Blender 4+ are installed.

## Data management, consent, and privacy

Documented facts:

- Move AI's privacy policy, last updated 2025-08-21, says the App/API may process Move One mobile application, Move Multi-Cam, Move Pro for Desktop cloud/local processing, Move Live, Move API Portal, and single/multi-camera API data.
- Move AI's privacy policy identifies metadata, motion data, output files, and, for independent users, uploaded video as personal data categories. Motion data may include identifying factors such as height, body proportions, mass distribution, rotations, and speed of movement.
- Move AI says it does not use video data, motion data, or output files to actively try to identify users.
- Move AI's privacy policy says it may use Metadata, Motion, Output, and Video to publish examples of the functionalities and capabilities of its App/API under its stated legitimate-interest basis. Treat public examples, demos, and case-study uses as contract/consent review items before uploading confidential, unreleased, or performer-sensitive material.
- Move AI says it may use data analytics and AI/machine-learning technologies to improve its App/API, services/products, marketing, user relationships, and experiences.
- Move AI says it may disclose personal information to service providers, contractors, consultants, analytics/search providers, marketing/survey tools, fraud/criminal-activity detection parties, group companies, affiliates, licensees, or where legally required.
- Move AI says some external third parties are outside the UK/EEA and transfers are protected with appropriate safeguards.
- Move AI says it retains personal data only as long as reasonably necessary for the collected purposes, including legal/regulatory/tax/accounting/reporting needs, and may retain longer for complaints or litigation prospects.
- Move AI's terms page lists subprocessors including AWS, Mixpanel, PostHog, Auth0, Stripe, Datadog, Mailgun, and HubSpot, with purposes such as cloud services, analytics, authentication/security, payment processing, error tracking, email, CRM, and marketing tools.
- Move AI's product page says Genesis processes locally within the customer's infrastructure and can be air-gapped from the outside world.

Production heuristics:

- Obtain explicit performer consent for capture, processing, retargeting, reuse, AI/ML service processing where applicable, storage, and downstream publication. Motion data can be identifying even without the original video.
- Treat raw video, derived motion, actor profiles, biomechanics outputs, and retargeted animation as sensitive production assets.
- Review the applicable Move AI EULA/order form before upload for any rights to use metadata, motion, output, or video in examples, demos, marketing, service improvement, or publication; do not rely on the public policy alone for confidential productions.
- Decide cloud versus local processing based on contract, project confidentiality, performer agreements, and client security requirements. Prefer Genesis local processing for strict data-residency or air-gap needs if Move AI's current contract supports it.
- Keep an asset ledger: capture date, performers, consent scope, product used, processing location, source files, derived files, exports, retention deadline, access list, and deletion status.
- Do not upload minors, bystanders, private locations, or unreleased IP to cloud workflows without appropriate rights, releases, and security approval.

## Complete examples

### Example: solo creature stunt previsualization with Move One

Production intent: capture a 35-second solo human-performed crouch, leap, roll, and recovery for previsualizing a creature animation blockout.

Applicable product: Move One, because this is a single human performer, short take, and previsualization-quality pass. Move AI captures human motion here; creature proportion, gait, appendage, tail, wing, quadruped, or non-human behavior requires downstream animation adaptation rather than provider-side creature mocap.

Inputs and constraints:

- One performer, fitted red top and blue trousers, light shoes.
- Locked phone camera in landscape, full body visible at all extremes.
- 60 fps Full HD or better if using uploaded video.
- No second performer, no heavy prop, no camera movement.

Workflow:

1. Shoot a 5-second test with crouch, arm extension, and leap landing.
2. Upload/process in Move One.
3. Inspect output video and FBX in Blender or Unreal.
4. If feet slide, reshoot with more visible footwear/floor contrast and more frame margin.
5. Export FBX for animation blockout and archive input MP4, output MP4, FBX, and consent note.

Expected result: usable timing and body mechanics for previz. Likely failure modes: hands leave frame during roll, feet blur during leap, root motion needs cleanup after retargeting.

### Example: eight-performer dance capture with Genesis

Production intent: capture a full-body ensemble routine for a game cinematic with close crossings and synchronized footwork.

Applicable product: Genesis, because Move AI documents Genesis 1-8 person capture, multi-camera operation, multi-actor exports, and m2 improvements for high-occlusion multi-subject scenes.

Inputs and constraints:

- 8 performers, each with fitted high-contrast wardrobe and light shoes.
- Studio volume sized and configured with 6-12 Z CAMs according to the planned space.
- Local processing required by client confidentiality policy.
- Target engine needs FBX and individual actor tracks plus a consolidated reference file.

Workflow:

1. Confirm hardware, Ubuntu/Nvidia driver requirements, storage, camera sync, and Peel Capture integration before shoot day.
2. Calibrate with checkerboard, mark active volume, and capture actor profiles.
3. Record one simple individual reference move per performer, then ensemble takes.
4. Process using m2 if the action includes occlusion-heavy crossings and footwork.
5. Review mesh, skeleton, and calibration overlays; use 3D viewer for identity continuity and foot contacts.
6. Export individual FBXs and the consolidated master; import a sample into the engine before approving the session.

Expected result: separate and consolidated animation tracks suitable for retargeting. Likely failure modes: identity swaps at crossings, shoes blending into floor, insufficient camera coverage at edges, retarget scale mismatch.

### Example: biomechanics review from a Move One upload

Production intent: analyze a short jump landing for approximate joint position/rotation and foot contact review, not medical diagnosis.

Applicable product: Move One if a single-performer single-camera video meets file and quality constraints and biomechanics output is available through gallery.

Inputs and constraints:

- `.mp4`, `.mov`, or `.avi`; no larger than 1 GB.
- Locked camera, single performer centered, full-body visible, minimum 60 fps Full HD recommended by Move AI.
- Consent explicitly covers motion-data analysis.

Workflow:

1. Upload the file through Move Platform single-file upload.
2. Download biomechanics output from gallery if available.
3. Review timestamped joint data; Move AI documents positions in meters, rotations in radians, torques in newton-meter, and foot reaction forces in Newton.
4. Compare with video and do not overstate clinical accuracy unless validated by a qualified biomechanics workflow.

Expected result: structured motion data for production/analysis review. Likely failure modes: single-camera ambiguity, feet occluded at landing, output interpreted beyond its validated purpose.

## Sources

Official Move AI sources consulted 2026-07-11:

- Move AI homepage: https://www.move.ai/
- Move AI products page: https://move.ai/products
- Move AI Knowledge Base: https://docs.move.ai/knowledge
- Genesis overview/index: https://docs.move.ai/knowledge/genesis
- Move One overview/index: https://docs.move.ai/knowledge/move-one
- Genesis equipment list and requirements: https://docs.move.ai/knowledge/genesis-equipment-list-requirements
- Genesis performance considerations: https://docs.move.ai/knowledge/genesis-performance-considerations
- Genesis output formats: https://docs.move.ai/knowledge/genesis-output-formats
- Genesis mocap models: https://docs.move.ai/knowledge/genesis-mocap-models
- Retargetting with Genesis: https://docs.move.ai/knowledge/retargetting-with-genesis
- Genesis viewing and exporting animation output: https://docs.move.ai/knowledge/genesis-viewing-and-exporting-the-animation-output
- Move One capture/process/duration pages: https://docs.move.ai/knowledge/how-to-capture-your-motion, https://docs.move.ai/knowledge/how-to-process-your-motion, https://docs.move.ai/knowledge/how-long-can-i-capture-for
- Move One single-file upload: https://docs.move.ai/knowledge/single-file-upload
- Move One export formats and gallery: https://docs.move.ai/knowledge/which-file-formats-are-available-for-exporting, https://docs.move.ai/knowledge/gallery-view
- Move One biomechanics output: https://docs.move.ai/knowledge/motion-data-biomechanics-output
- Move One animation-use overview: https://docs.move.ai/knowledge/using-your-animations-overview
- Move AI privacy policy, last updated 2025-08-21: https://move.ai/privacy-policy
- Move AI terms/subprocessors page: https://move.ai/terms-of-use
