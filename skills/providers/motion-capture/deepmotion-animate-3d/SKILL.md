---
name: deepmotion-animate-3d
description: Use DeepMotion Animate 3D for markerless video-to-3D human motion capture through the cloud portal, sales-gated API, or real-time SDK; covers capture planning, body/hand/face/multi-person limits, custom characters, retargeting, refinement, exports, DCC/game-engine handoff, QA, pricing, privacy, consent, and rights checks.
---

# DeepMotion Animate 3D

Use this skill when an agent needs to turn recorded human performance video into 3D character animation with DeepMotion Animate 3D, or when planning an Animate 3D Cloud/API/Real-Time SDK mocap workflow. This is a provider skill for markerless video-to-3D motion capture, not a general 3D generation, text-to-animation, acting direction, rigging theory, or animation-polish skill.

Do not use this skill for:

- generating a 3D model, character mesh, environment, or prop from text or images;
- provider-independent animation craft, keyframe animation, mocap cleanup in Maya/Blender, or final acting polish;
- text-to-3D animation through DeepMotion SayMotion except when an API page exposes shared lifecycle patterns that must be clearly labeled as SayMotion rather than Animate 3D;
- non-human, non-humanoid, creature-specific, vehicle, cloth, or object motion capture unless the task is explicitly about testing a humanoid approximation.

## What Animate 3D Is

Documented fact, verified 2026-07-11: DeepMotion describes Animate 3D as markerless AI motion capture that converts ordinary human video into 3D animation. The product page and documentation say it can track full-body movement, facial expressions, hand gestures, and multiple subjects, with output formats including FBX, BVH, GLB, and MP4. Sources: https://www.deepmotion.com/animate-3d and https://www.deepmotion.com/doc/animate-3d.

Documented fact, verified 2026-07-11: DeepMotion positions Animate 3D in three access modes: Animate 3D Cloud through the browser, Animate 3D API for application integration, and Animate 3D Real-Time SDK as a lightweight real-time version. Public pages route API and Real-Time SDK access through sales/contact rather than publishing a complete public Animate 3D API reference. Source: https://www.deepmotion.com/animate-3d.

Marketing claim, verified 2026-07-11: DeepMotion calls Animate 3D accessible mocap with no suits or required cameras and says users can create animations "in minutes." Treat this as provider positioning, not an accuracy guarantee or processing-time SLA.

Access-gated unknown, verified 2026-07-11: a complete public Animate 3D REST API reference, production base URL, quota model, latency SLOs, realtime SDK platform matrix, SDK package, and enterprise retention/security terms were not publicly retrievable without portal/sales access. Do not invent endpoint names or capabilities for Animate 3D API. Ask the user for their portal/API documentation or sales-provided spec before writing integration code beyond general async-job pseudocode.

## Current Capability Boundaries

Documented fact, verified 2026-07-11: Animate 3D is for human motion and can be applied to human or humanoid characters. DeepMotion's capture quick guide says cartoon or abstract figures are not suitable as capture subjects. Source: https://www.deepmotion.com/article/capture-guidelines-quick-guide.

Documented fact, verified 2026-07-11: DeepMotion's Animate 3D product page says a single video can track up to 8 people. The release updates describe Multi-Person Tracking as beta in Animate 3D V5.0 and say it tracks full body, hand, and face motion for up to 8 people. Sources: https://www.deepmotion.com/animate-3d and https://www.deepmotion.com/release-updates.

Boundary note: Some documentation pages still contain older single-person language, such as the single-person guide saying to avoid multiple individuals until multi-person tracking is available. Treat this as stale page-level wording unless the current project has a plan or portal setting that lacks multi-person access. Source checked 2026-07-11: https://www.deepmotion.com/article/single-person-capture-guidelines-for-animate-3d.

Documented fact, verified 2026-07-11: Hand Tracking is an advanced setting that costs an additional 0.5 animation credit per animation second or pose, and hand results are combined with body tracking in BVH, FBX, and GLB exports when enabled. Source: https://www.deepmotion.com/article/hand-tracking-video-capture-guidelines.

Documented fact, verified 2026-07-11: DeepMotion's getting-started FAQ says 1 credit equals 1 second of animation or 1 3D pose, with Face Tracking and Hand Tracking each costing an extra 0.5 credit per animation second or pose. Source: https://www.deepmotion.com/article/getting-started.

Documented fact, verified 2026-07-11: Facial tracking accepts full-body, half-body, or headshot video, but quality improves when the face is larger and clearer. The face guide says headshot and half-body inputs can support eye/iris tracking and higher fidelity facial expressions, while full-body inputs are farther away so eye tracking is turned off but general facial expression, mouth movement, and head position can still be captured. Source: https://www.deepmotion.com/article/facial-tracking-video-capture-guidelines.

Documented fact, verified 2026-07-11: DeepMotion supports MP4, MOV, and AVI input videos according to the Animate 3D pricing FAQ/getting-started FAQ. Outputs are described as FBX, BVH, MP4, and GLB, with GLB noted as available for custom characters on the pricing FAQ. Sources: https://www.deepmotion.com/pricing-animate3d and https://www.deepmotion.com/article/getting-started.

Documented fact, verified 2026-07-11: File Types & Compatibility also lists BVH, FBX, GLB/GLTF animation formats, plus MP4, JPG, PNG, GIF for poses, and DMPE for DeepMotion Pose Estimation; it states DMPE includes 3D skeletal joint positions for every frame and is available for Professional and higher subscription levels. Source: https://www.deepmotion.com/article/file-types-compatibility.

Volatile plan fact, verified 2026-07-11: the visible pricing page advertised annual paid tiers at Starter $9/month, Innovator $17/month, Professional $39/month, and Studio $83/month, plus Freemium. The same page says API and Real-Time SDK require contacting DeepMotion. Re-check before quoting costs in user-facing plans. Source: https://www.deepmotion.com/pricing-animate3d.

Volatile plan fact, verified 2026-07-11: DeepMotion's pricing FAQ says Freemium accounts are personal, non-commercial, no credit card, and can create up to 60 seconds of animations every month. It also says credits do not carry over monthly. Source: https://www.deepmotion.com/pricing-animate3d.

Volatile upload-limit fact, verified 2026-07-11: the visible Animate 3D pricing page listed a current maximum uploaded video length of 300 seconds. It also listed plan-dependent upload file-size limits of 50 MB, 100 MB, and 200 MB across self-serve tiers. These limits are plan and page-state dependent; re-check the pricing page or portal before promising that a specific account can upload a given clip. Source: https://www.deepmotion.com/pricing-animate3d.

## Capture Planning

Animate 3D quality is mostly decided before upload. The agent should optimize the input video rather than assuming portal settings can repair occlusion, motion blur, missing feet, or low-detail hands.

### Single-subject body capture

Documented capture requirements, verified 2026-07-11:

- Place the camera about 2-6 meters, or 6-20 feet, from the subject.
- Keep the camera stationary and perpendicular to the person being recorded.
- Keep the entire body visible head-to-toe for full-body tracking.
- Avoid occlusion and objects covering body parts.
- For ground motions, shoot from a 3/4 angle so body parts do not hide key joints.
- Use neutral lighting, avoid overly dark or blown-out lighting, and avoid blur.
- Create contrast between the subject and background.
- Avoid loose clothing and clothing that covers knees, elbows, or hands; patterns or texture are preferred over all-black solid clothing.
- Use at least 1080p resolution; DeepMotion recommends 30 FPS or higher and says 60 FPS gives best results where available on premium subscriptions.

Sources: https://www.deepmotion.com/article/capture-guidelines-quick-guide and https://www.deepmotion.com/article/single-person-capture-guidelines-for-animate-3d.

Production heuristic: if the motion includes jumps, kicks, crawling, floor work, or fast spins, capture a short test first and inspect feet, hips, and hand-ground contact before recording a full batch. Use the same wardrobe and camera angle as the final take.

### Multi-person capture

Documented multi-person guidance, verified 2026-07-11:

- Frame the full capture area, place the camera at chest height, keep it stationary, and maintain an unobstructed view of all subjects.
- Give performers enough space to move without colliding.
- Minimize close interactions such as hugging, wrestling, holding hands, or characters passing in front of/behind one another.
- Avoid occlusion and avoid frequent relative-position swaps, which can lead to identity/position swaps.
- Use a 3/4 angle for ground motions.
- Use even neutral lighting and avoid harsh shadows or overly bright spots.
- Make subjects visually distinct through different colors or patterned clothing.
- Use at least 1080p and 30 FPS or higher.

Source: https://www.deepmotion.com/article/multi-person-ai-motion-capture-guidelines.

Production heuristic: for choreographed multi-person scenes, block the shot like a stage capture rather than a film shot. Wide, stable, separated, contrasty coverage is more valuable than dramatic camera language.

### Face capture

Documented face guidance, verified 2026-07-11:

- Keep the full head in frame with forehead, eyes, nose, and mouth visible.
- Have the subject face the camera directly for best results.
- Closer framing improves facial detail.
- Use neutral, even face lighting and avoid harsh shadows.
- For best facial tracking, keep only one person in frame.
- Full-body face capture can capture general expressions, mouth movement, and head position, but eye tracking is turned off due to distance.

Source: https://www.deepmotion.com/article/facial-tracking-video-capture-guidelines.

Production heuristic: if a deliverable needs believable facial nuance, record a half-body or headshot face pass and do not expect full-body footage shot for footwork to carry close-up acting detail.

### Hand capture

Documented hand guidance, verified 2026-07-11:

- Use full-body or half-body video where hands are clear, large, visible, and unobstructed.
- Upload at least full HD 1920x1080 video for hand detail.
- Avoid gloves, sleeves, accessories, or clothing that covers the hands.
- Avoid hand motions that are not optimized, including hands touching the face or hands interacting with each other such as clapping.
- Use neutral lighting and contrast between hands and background.

Source: https://www.deepmotion.com/article/hand-tracking-video-capture-guidelines.

Production heuristic: for sign language, magic tricks, weapon grips, finger-counting, typing, or hand-to-face acting, treat Animate 3D hand tracking as a starting point that will need animator cleanup or a dedicated hand mocap method.

## Settings And Refinement

Use settings as controlled rerun variables. Change one major setting at a time, record the original job settings, and compare output against the source video before deciding that a take has failed.

### Foot Locking

Documented fact, verified 2026-07-11: DeepMotion offers Foot Locking modes Auto, Always, Never, and Grounding. Auto is recommended for general cases and is available for all subscription plans. Always forces foot locking and is recommended when Auto leaves too much foot gliding; it is available for Professional or higher plans. Never keeps feet unlocked for airborne or underwater motions and is available for Innovator or higher. Grounding disables locking while keeping the character on the ground and is recommended when sliding/gliding is intended or Auto locks feet too long; it is available for Professional or higher. Source: https://www.deepmotion.com/article/foot-locking.

Production choices:

- Use Auto first for ordinary walks, acting beats, and non-stylized motion.
- Try Always for rooted stances, weight shifts, martial arts forms, or idle acting where foot sliding is visibly wrong.
- Try Grounding for shuffle dances, moonwalks, sprints, quick pivots, and fast footwork where sliding is intentional.
- Try Never for swimming, aerial flips, trampoline, falling, suspended motion, or motions where ground contact is not meaningful.

### Motion Smoothing

Documented fact, verified 2026-07-11: Motion Smoothing is an advanced AI filter that removes jitter and improves visual smoothness but may reduce animation accuracy in some frames or sequences. DeepMotion recommends tuning the degree of smoothing and reviewing tradeoffs. Source: https://www.deepmotion.com/article/motion-smoothing.

Production choices:

- Use low smoothing when preserving sharp gesture timing matters.
- Increase smoothing when jitter is more objectionable than exact micro-timing.
- Avoid high smoothing on impacts, precise dance accents, sign language, combat strikes, sports analysis, or any motion where frame-accurate direction changes matter.

### Physics Filter

Documented fact, verified 2026-07-11: the Physics Filter reinforces joint limits and attempts to resolve self-collisions and clipping. DeepMotion suggests experimenting and combining it with Motion Smoothing. Source: https://www.deepmotion.com/article/physics-filter.

Production choices:

- Enable it when limbs pass through the body, joints bend beyond plausible limits, or mesh clipping is more damaging than exact source fidelity.
- Be cautious when the source pose is genuinely extreme, stylized, acrobatic, or contorted; the filter can make the result more plausible but less faithful.

### Speed Multiplier

Documented fact, verified 2026-07-11: Speed Multiplier can compensate for slow-motion or insufficient-frame-rate input by adjusting the speed multiplier, previewing, and rerunning to optimize smoothness. Source: https://www.deepmotion.com/article/speed-multiplier.

Production choices:

- Use when input was recorded slow-motion or low-FPS and the generated motion is choppy or mistimed.
- Prefer recording real-time 30-60 FPS source when possible; Speed Multiplier is a repair tool, not a substitute for usable capture.

### Rotoscope Pose Editor and reruns

Documented fact, verified 2026-07-11: DeepMotion says the Rotoscope Pose Editor lets users trace/correct character motion over the input video. Release notes describe features including auto-saving, multi-joint selection, hotkeys, interpolation, and bone color selection. Pricing/credit FAQ says Animation Correction Credits can be earned by correcting body joints and improving the pose score. Sources: https://www.deepmotion.com/animate-3d, https://www.deepmotion.com/release-updates, and https://www.deepmotion.com/article/free-animation-credit-program-faq.

Production workflow:

1. Inspect the initial output beside the source video.
2. Identify whether the error is input-related, setting-related, character-retargeting-related, or localized pose error.
3. Rerun with changed settings when the whole clip shows a systematic issue, such as excessive foot lock, jitter, or clipping.
4. Use Rotoscope Pose Editor when the problem is localized to specific frames or joints.
5. Export only after reviewing root, feet, hands, fingers, face, and contact frames.

## Custom Characters And Retargeting

Documented fact, verified 2026-07-11: Animate 3D can use default DeepMotion characters, built-in Ready Player Me and Avaturn creators, or uploaded custom FBX/GLB/VRM characters according to the product page. The Custom Characters article says custom upload supports FBX and GLB and requires a rigged humanoid character; the API-related GitHub docs for the SayMotion REST API character upload mention fbx, glb, gltf, or vrm model upload URLs, but that is SayMotion/public REST documentation, not a complete Animate 3D public API contract. Sources: https://www.deepmotion.com/animate-3d, https://www.deepmotion.com/article/custom-characters, and https://github.com/DeepMotion/SayMotion-REST-API.

Documented custom-character requirements, verified 2026-07-11:

- The model must be rigged, humanoid, and full-body.
- Use a clean file containing only needed character mesh and rigging information; remove extra animations and environment models.
- Include only one character in the upload file.
- Export the default pose as T-pose.
- Put feet on the origin plane.
- Orient T-pose arms along world X, with the left hand pointing positive X, and face the character in positive Z; incorrect orientation can fail import.
- Use unique joint names with no spaces.
- DeepMotion recommends XYZ joint rotation order; non-XYZ joints are converted.
- Avoid scaling joints; scale the skeleton at a root node if necessary.
- Use human proportions, around 1.7 m / 5 ft 6 in tall.
- Use one root joint and avoid non-joint nodes in the middle of the hierarchy.

Source: https://www.deepmotion.com/article/custom-characters.

Retargeting guidance:

- If the target engine has robust retargeting, such as Unity Humanoid or Unreal IK Retargeter, exporting a clean FBX/BVH from a DeepMotion default or UE-compatible character can be easier than forcing a fragile custom upload.
- If the target is Blender or a DCC scene where retargeting tools are limited, uploading the custom character before processing can save time because Animate 3D exports the motion already applied to that character.
- For facial animation, confirm the character has compatible facial rig/blendshape support before promising face output. Public pages refer to custom-character face compatibility checks, but exact blendshape requirements may be account/tool-version dependent.
- For hand/finger animation, confirm the character includes finger joints and inspect finger curls after export.

## Cloud, API, Real-Time SDK, And Async Lifecycle

Cloud workflow, documented from public pages and portal descriptions, verified 2026-07-11:

1. Sign in at portal.deepmotion.com.
2. Choose Animate 3D and create a new job.
3. Upload a supported video.
4. Select the character or custom model.
5. Choose tracking/settings: body, hand, face, multi-person where available, physics, foot locking, smoothing, speed multiplier, MP4 camera/render settings if needed.
6. Submit the job and wait for processing.
7. Preview the result.
8. Rerun/refine if needed.
9. Download FBX/BVH/GLB/MP4 or other eligible outputs.

API implementation warning: public first-party pages do not expose a full current Animate 3D API reference. If a user asks for production integration, request their DeepMotion API portal docs and credentials, then implement against the provided specification. Do not hard-code endpoints inferred from SayMotion unless the supplied Animate 3D documentation confirms them.

Official GitHub observation, verified 2026-07-11: DeepMotion's public `DeepMotion/SayMotion-REST-API` repository is for SayMotion text-to-3D animation, not Animate 3D video-to-3D capture. It uses Basic authentication with client ID/client secret to retrieve a session cookie, then supports credit balance, job process, status polling, download URLs, list jobs, cancel job, custom character upload/list/delete, prompt optimization, and an `import animate3d` job endpoint. The repo has no published GitHub Releases visible on 2026-07-11. Source: https://github.com/DeepMotion/SayMotion-REST-API.

General async pattern for any DeepMotion integration, to be adapted only after reading the user's actual API spec:

1. Authenticate server-side; never expose client secret in browser code.
2. Check balance/plan/feature limits before accepting a user upload.
3. Upload media/model using provider-approved signed upload URLs or portal upload flow.
4. Submit processing job with explicit settings and export requirements.
5. Store request ID, user ID, source asset ID, settings snapshot, and consent/rights metadata.
6. Poll status with backoff or subscribe to provider webhooks if documented by the user's API contract.
7. Handle queue/progress/success/failure/cancel states distinctly.
8. On success, download outputs immediately into controlled project storage if the provider's download URLs are temporary.
9. On failure, surface provider error code/message, original video spec, settings, and next recommended action.
10. Log retention/deletion requirements and delete source assets when required by client policy or contract.

Real-Time SDK planning, verified 2026-07-11: DeepMotion markets a Real-Time SDK but public pages route access through contact/sales and do not expose a public SDK matrix. Before committing to a realtime product, confirm platform support, camera/device requirements, latency, frame rate, tracking points, number of subjects, face/hand availability, offline behavior, data egress, and commercial terms with DeepMotion.

## Export And Handoff

Use export format based on the receiving tool, character strategy, and review need.

- FBX: default handoff for Unreal, Unity, Maya, Blender retargeting, character mesh + animation workflows, and MetaHuman tutorials. Prefer for game-engine animation import.
- BVH: skeletal motion data handoff, especially when the destination has a known BVH retargeting path or when the character mesh is handled separately.
- GLB/GLTF: compact custom-character scene/animation handoff where GLB is supported; public FAQ notes GLB is only available for custom characters.
- MP4: visual review, client approval, side-by-side/output preview, or social/display output; not a source animation interchange format.
- DMPE: analysis-oriented output for 3D skeletal joint positions per frame, available on Professional and higher according to DeepMotion's file-types page.

Blender handoff, documented fact verified 2026-07-11: DeepMotion's Blender companion page says users can download animation with BVH or FBX preset format and transfer the rig to a character in Blender. Source: https://www.deepmotion.com/companion-tools/blender.

Unity handoff, documented fact verified 2026-07-11: DeepMotion's Unity companion page says Animate 3D outputs can be imported into Unity scenes and that a tutorial walks through retargeting results to a custom 3D character. Source: https://www.deepmotion.com/companion-tools/unity.

Unreal/MetaHuman handoff, documented fact verified 2026-07-11: DeepMotion's Unreal/MetaHuman companion pages and March 2025 MetaHuman tutorial describe exporting FBX, importing into Unreal Engine, enabling morph targets/import animations/snap to closest frame boundary, then using Unreal retargeting to apply animation to a MetaHuman. The tutorial recommends selecting an Adult Female with Facial Rig (UE) character for MetaHuman retargeting and turning on hand and face tracking. Sources: https://www.deepmotion.com/companion-tools/unreal-engine, https://www.deepmotion.com/companion-tools/metahuman-creator, and https://www.deepmotion.com/post/animate-a-metahuman-with-just-a-video-no-mocap-needed.

Production heuristic: always export a visual MP4 proof together with animation files. It gives animators and clients a reference for what DeepMotion produced before downstream retargeting changes the motion.

## QA And Cleanup Checklist

Before calling an Animate 3D result production-ready, inspect:

- Source fit: full performer visible when required, enough resolution, no motion blur, no occlusion, clear clothing/background contrast.
- Identity continuity: no subject swaps in multi-person scenes, especially during crossings or close interaction.
- Root motion: no unexplained drifting, sliding, vertical pops, or scale mismatch.
- Feet: correct planted frames, acceptable glide for intended sliding, no ground penetration, correct foot locking mode.
- Hips/spine: no sudden flips, twisted torso, or hip height collapse.
- Hands: visible finger articulation, no hand-to-face/hand-to-hand failures hidden by camera angle, no wrist flips.
- Face: head orientation, mouth movement, expression intensity, eye behavior where expected.
- Contacts: hand-ground, foot-ground, props, partner proximity, and floor work.
- Custom character: mesh deformation, skinning, facial blendshape availability, finger joints, scale, root orientation, and import errors.
- Export integrity: FBX/BVH/GLB opens in the target tool, frame rate/timing is correct, animation range is trimmed, and downstream retargeting preserves contacts.
- Rights/privacy: consent and upload permissions are recorded before source video is sent to DeepMotion.

Common failure responses:

- Missing feet or cropped limbs: reshoot or crop less; settings cannot reconstruct reliable full-body contact.
- Occlusion between performers: reshoot with spacing; multi-person can track several people but does not remove the identity-swap risk from crossings.
- Shaky camera: reshoot locked-off; stabilization may help visually but can introduce motion artifacts.
- Foot glide: compare Auto, Always, and Grounding; then fix residual frames in DCC if needed.
- Over-smoothed impacts: reduce Motion Smoothing and preserve key accents.
- Hands fail on claps/face touches: reshoot with clearer hands or plan manual hand cleanup.
- Face lacks detail: use half-body/headshot capture or separate facial workflow.
- Custom character upload fails: check orientation, T-pose, one root joint, unique names/no spaces, human scale, and extra scene data.

## Privacy, Consent, Rights, And Retention

Documented privacy facts, verified 2026-07-11: DeepMotion's Privacy Policy says it applies to Animate 3D web service, SDKs, APIs, and other services. It says users routinely submit Content Data, including videos and 3D models, and that processing such Content Data is a core element of the services. It says User Content voluntarily disclosed for posting remains private to the user and DeepMotion and will not be shared publicly unless explicitly agreed by both. It lists Google, Inc. as a cloud service provider subprocessor and says storage/processing may occur in the United States or other countries where DeepMotion or service providers maintain facilities. Source: https://www.deepmotion.com/privacy-policy, last updated December 1, 2023.

Documented retention/security facts, verified 2026-07-11: the Privacy Policy says DeepMotion may retain private profile information after account termination for a commercially reasonable time for backup, archival, or audit purposes, but it does not give a precise retention period for uploaded videos, 3D models, job outputs, or API assets in the public page. The Terms say users are responsible for data they transmit and waive claims for loss/corruption of such data; the public SayMotion REST docs note failed jobs and old jobs may be removed after a predefined retention period without specifying the period. Sources: https://www.deepmotion.com/privacy-policy, https://www.deepmotion.com/terms-of-use, and https://github.com/DeepMotion/SayMotion-REST-API.

Documented terms facts, verified 2026-07-11: DeepMotion's Terms of Use were last updated March 30, 2025. They say users retain full ownership of uploaded Content, but grant DeepMotion non-exclusive, fully-paid, royalty-free worldwide rights to access, review, use, copy, modify, create derivative works of, reproduce, analyze, visualize, and process uploaded Content to deliver services and to improve the site/services. The terms require users not to upload content that violates copyright, privacy, publicity, trademark, or other third-party rights. Source: https://www.deepmotion.com/terms-of-use.

Documented regulated-data warning, verified 2026-07-11: DeepMotion's Terms say the Site is not tailored to comply with industry-specific regulations including HIPAA and FISMA, and that users may not use the Site if their interactions would be subject to such laws. The same section says users may not use the Site in a way that would violate GLBA. Do not route regulated healthcare, government-security, financial-institution, or similarly controlled production data through DeepMotion without a separate contract and legal/security approval; the public terms make the self-serve Site a poor fit for those workloads. Source: https://www.deepmotion.com/terms-of-use.

Documented output-license facts, verified 2026-07-11: the Terms say DeepMotion owns Products of the Site and licenses them to users. Freemium outputs receive a revocable non-commercial license. Paid plans receive a perpetual, non-exclusive, fully-paid, royalty-free worldwide commercial license for Products created while subscribed to paid plans. The terms prohibit using Products as stand-alone digital assets, sublicensing/resale, or retargeting animations contained in Products to a different character and selling the retargeted animations. Source: https://www.deepmotion.com/terms-of-use.

Documented consent fact, verified 2026-07-11: DeepMotion's contribution terms require written consent/release/permission from every identifiable person in user Contributions for use of name or likeness in the manner contemplated by the site and terms. Although the legal section distinguishes Contributions from uploaded Content, production agents should treat identifiable performer video as consent-sensitive Content Data and require documented permission before upload. Source: https://www.deepmotion.com/terms-of-use.

Production privacy checklist:

1. Confirm the performer owns or has permission to submit the recorded likeness/performance.
2. Confirm wardrobe, music, set art, logos, and third-party video sources are cleared or removed.
3. Avoid uploading minors unless the project has parent/guardian consent and a policy review.
4. For enterprise/confidential work, verify retention, deletion, subprocessor, training/improvement use, API data handling, regional processing, and DPA terms directly with DeepMotion before upload.
5. Do not use Freemium outputs for commercial deliverables.
6. Do not sell DeepMotion motion files as stand-alone animation assets or asset packs unless a separate contract explicitly permits it.
7. Do not upload HIPAA-, FISMA-, GLBA-, or similarly regulated data through the self-serve Site; route those projects through legal/security review and a separate enterprise agreement if DeepMotion is still being considered.

## Complete Examples

### Example: Indie game locomotion from phone video

Production intent: create a base walk, jog, idle turn, and jump landing for a humanoid Unity character without a suit.

Provider: DeepMotion Animate 3D Cloud.

Inputs and constraints:

- Four separate phone videos, each 5-12 seconds.
- Actor framed head-to-toe, camera locked on tripod 3 meters away, 60 FPS if available.
- Fitted clothing with visible knees/elbows and high contrast from background.
- Target character is a Unity humanoid rig; final cleanup in Unity/Blender is allowed.

Workflow:

1. Shoot each move as a separate clip with a neutral start/end pose.
2. Upload one test clip first and use a default DeepMotion/Unity-friendly character.
3. Use Foot Locking Auto for walk/jog/idle turn.
4. Use Foot Locking Auto first for jump landing; rerun with Always if landing feet slide or with Grounding if fast approach steps stick too long.
5. Keep Motion Smoothing low unless the result jitters.
6. Export FBX for Unity and MP4 proof for review.
7. In Unity, import FBX, map to humanoid avatar/retarget target, inspect root motion and foot contacts, then trim loops.

Why structured this way: short separate clips reduce wasted credits and isolate settings. A default/Unity-friendly character reduces custom-character upload risk until capture quality is proven.

Expected result: usable base mocap that needs light trimming, loop cleanup, and possible foot-contact fixes.

Likely failure modes: foot slide during jog, hand jitter, root drift at loop boundaries, and retarget scale mismatch.

Meaningful variations: upload the actual custom character after the first pass if Blender retargeting time is more expensive than rerunning DeepMotion; use BVH instead of FBX if the destination retargeting pipeline is BVH-based.

### Example: MetaHuman performance with body, hands, and face

Production intent: animate a MetaHuman presenter for a cinematic previs shot, with body gesture, finger motion, and broad facial expression.

Provider: DeepMotion Animate 3D Cloud, then Unreal Engine 5 handoff.

Inputs and constraints:

- Half-body take for facial/hand detail, and optional full-body take if feet must be visible.
- Performer faces camera; hands remain visible, not touching face or each other.
- Even lighting, 1080p minimum, 30 FPS or higher.
- Paid plan required for commercial output.

Workflow:

1. Capture a half-body take for the acting beat.
2. In Animate 3D, select a UE/MetaHuman-compatible character such as the Adult Female with Facial Rig (UE) mentioned in DeepMotion's MetaHuman tutorial if it fits the target workflow.
3. Enable Face Tracking and Hand Tracking; budget extra credits for both.
4. Use Foot Locking only if lower-body contact matters; for half-body presentation it is secondary.
5. Preview and check head rotation, mouth movement, fingers, and wrists.
6. Use Rotoscope Pose Editor for localized body/hand pose corrections if needed.
7. Export FBX and import into Unreal with morph targets and animation import enabled, following the current Unreal version's retargeting path.
8. Retarget to MetaHuman, attach in Sequencer, remove conflicting control rigs if needed, and compare against the MP4 proof.

Why structured this way: a full-body capture is usually too distant for expressive face/hand detail; the target deliverable needs upper-body believability more than foot contact.

Expected result: a retargeted MetaHuman animation suitable for previs or first-pass production, with animator review for face/fingers.

Likely failure modes: flat expression from distant face capture, finger popping, wrist flips, morph target import omissions, or incorrect target skeletal mesh selection.

Meaningful variations: record a separate close-up face pass if the shot cuts close; use a dedicated facial capture pipeline if lip-sync or eye performance must be final quality.

### Example: Multi-person dance reference with QA-first expectations

Production intent: convert a two-person dance rehearsal into separate character animations for a stylized short.

Provider: DeepMotion Animate 3D Cloud multi-person tracking.

Inputs and constraints:

- Two dancers, wide shot, no camera movement, 1080p/30 FPS minimum.
- Dancers wear clearly different clothing colors/patterns.
- Choreography avoids crossings, lifts, hugs, and hand-holding.
- Output will be cleaned in Blender before layout.

Workflow:

1. Reblock choreography to keep performers separated and visible.
2. Put camera at chest height with enough room for all movement.
3. Record a 10-second test section containing the most complex crossing/turn.
4. Upload and enable multi-person tracking; select distinct characters for each person.
5. Inspect identity continuity before paying/processing longer sections.
6. If identity swaps occur, reshoot with more spacing or split performers into separate takes.
7. Export per-character FBX/BVH plus MP4 proof.
8. In Blender, check timing alignment, contacts, and root offsets between characters.

Why structured this way: multi-person tracking can handle several subjects, but occlusion and relative-position swaps are still major risk factors.

Expected result: separate performer animations that preserve broad choreography and timing.

Likely failure modes: performer swaps during crossing, lost hands during close interaction, feet locking incorrectly in slides, and root offsets between dancers.

Meaningful variations: shoot each dancer separately against the same music click if interaction is minimal and accuracy matters more than live duet timing.

## Source Log

Official DeepMotion sources checked 2026-07-11:

- Animate 3D product page: https://www.deepmotion.com/animate-3d
- Animate 3D documentation entry: https://www.deepmotion.com/doc/animate-3d
- Documentation hub: https://www.deepmotion.com/documentation
- Capture quick guide: https://www.deepmotion.com/article/capture-guidelines-quick-guide
- Single-person capture guide: https://www.deepmotion.com/article/single-person-capture-guidelines-for-animate-3d
- Multi-person capture guide: https://www.deepmotion.com/article/multi-person-ai-motion-capture-guidelines
- Facial tracking capture guide: https://www.deepmotion.com/article/facial-tracking-video-capture-guidelines
- Hand tracking capture guide: https://www.deepmotion.com/article/hand-tracking-video-capture-guidelines
- Physics Filter: https://www.deepmotion.com/article/physics-filter
- Motion Smoothing: https://www.deepmotion.com/article/motion-smoothing
- Speed Multiplier: https://www.deepmotion.com/article/speed-multiplier
- Foot Locking: https://www.deepmotion.com/article/foot-locking
- Custom Characters: https://www.deepmotion.com/article/custom-characters
- File Types & Compatibility: https://www.deepmotion.com/article/file-types-compatibility
- Getting Started: https://www.deepmotion.com/article/getting-started
- Pricing: https://www.deepmotion.com/pricing-animate3d
- Release updates: https://www.deepmotion.com/release-updates
- Blender companion page: https://www.deepmotion.com/companion-tools/blender
- Unity companion page: https://www.deepmotion.com/companion-tools/unity
- Unreal Engine companion page: https://www.deepmotion.com/companion-tools/unreal-engine
- MetaHuman companion page: https://www.deepmotion.com/companion-tools/metahuman-creator
- MetaHuman tutorial: https://www.deepmotion.com/post/animate-a-metahuman-with-just-a-video-no-mocap-needed
- UE5 retargeting post: https://www.deepmotion.com/post/deepmotion-ue5-animation-retargeting-just-got-easier
- Terms of Use: https://www.deepmotion.com/terms-of-use
- Privacy Policy: https://www.deepmotion.com/privacy-policy
- Official GitHub SayMotion REST API repository: https://github.com/DeepMotion/SayMotion-REST-API
