# Evaluation: Move AI Motion Capture

This file is the hidden answer key. Do not expose it to the agent being evaluated. The evaluated agent receives only the user task and `SKILL.md`.

Score out of 100. A strong answer is production-specific, distinguishes documented facts from provider claims and heuristics, and avoids inventing unsupported Move AI capabilities.

## Critical failures

Assign zero for the relevant task, and cap the total score at 50, if the response:

- Recommends Move One for documented multi-person capture or long multi-performer interaction as if officially supported.
- Claims Move AI independently guarantees optical-quality results without labeling that as a provider claim.
- Ignores consent/privacy when the scenario involves performer video, motion data, minors, bystanders, confidential productions, or cloud upload.
- Invents unsupported export formats, products, APIs, model names, or duration/file-size limits.
- Invents public Move AI API endpoints, authentication flows, quotas, SDK packages, or rate limits instead of requiring portal documentation and contract/EULA review.
- Directs the agent to read or reveal `EVAL.md`.
- Turns the task into general animation, 3D generation, face capture, or non-Move mocap advice without addressing Move AI.

## Knowledge questions (40 points)

### 1. Move One vs Genesis selection (8 points)

Question: A producer has a 45-second solo action take, one locked camera, and wants quick FBX for previs. Another producer needs a six-performer dance capture with local processing and separate actor tracks. Which Move AI product fits each and why?

Expected answer:

- Move One for the 45-second solo single-camera capture because it is documented for single-camera/single-person workflows and paid plans can capture up to 60 seconds. (2)
- Mention camera should be locked, performer centered/full-body, and ideally 60 fps Full HD for uploaded single-file workflows. (1)
- Genesis for six performers because Move AI documents Genesis 1-8 person capture and multi-camera studio operation. (2)
- Mention Genesis local/on-prem processing with Nvidia GPU desktop application. (1)
- Mention Genesis multi-actor output includes individual actor files and consolidated master file. (1)
- Does not overstate quality as independently proven. (1)

Penalize: recommending Move One for six performers; omitting local/cloud distinction; saying Genesis is required for every professional take.

### 2. Documented Move One limits and exports (6 points)

Question: Name documented Move One input or capture limits and output options that matter before accepting a single-camera upload job.

Expected answer must include at least four of:

- Single-camera upload is for a single person. (1)
- Minimum 60 fps and Full HD recommended for optimal upload results. (1)
- Camera locked and performer centered. (1)
- Upload supports `.mp4`, `.mov`, `.avi`. (1)
- Maximum uploaded file size is 1 GB. (1)
- Paid app capture up to 60 seconds. (1)
- Exports include `.fbx`, `.usdc`, `.blend` requiring Blender 4+, `.usdz`, output/input `.mp4`, and biomechanics output via platform gallery. (1)

Maximum 6.

### 3. Genesis hardware/setup facts (7 points)

Question: List core Genesis setup requirements or documented equipment facts.

Expected answer must include at least five of:

- Multi-camera Genesis uses Z CAMs; product page lists 6-12 cameras and equipment docs recommend minimum 6 Z CAM E2 M4 Mark II cameras. (1)
- Recommended compatible camera models include Z CAM E2-M4s Mark II and Z CAM E2-M4 Mark II. (1)
- Nvidia GPU requirement: RTX 40, 50, or A series supported; local processing uses Nvidia GPUs. (1)
- Ubuntu 22.04 and Nvidia Driver 580 documented. (1)
- 64 GB DDR4 RAM and SSD NVMe with 80 GB for application/processing engines; 1 TB project storage recommended. (1)
- PoE+ switch with at least 30 W per camera, shielded Ethernet, CFexpress B v4 cards, 10 GB network card. (1)
- A1 checkerboard, tape measure, and floor markers for calibration/volume management. (1)
- Peel Capture integration/configuration/triggering. (1)

Maximum 7. Penalize invented camera brands or OS versions.

### 4. Wardrobe and performance constraints (6 points)

Question: What wardrobe/lighting/performance constraints should an agent enforce for Move AI capture?

Expected answer:

- Avoid baggy/loose clothing. (1)
- Avoid long sleeves covering wrists. (1)
- Use strong contrast against background; avoid matching environment. (1)
- Use different-colored top and bottom; avoid black when possible. (1)
- Match footwear heel height to digital rig and use light/visible footwear for floor contrast. (1)
- Include lighting/camera heuristics: even illumination, avoid deep shadows/blown highlights/flicker, keep body visible and avoid occlusion. (1)

### 5. Genesis models and retargeting (6 points)

Question: What must an agent know about Genesis m1/m2 and retargeting?

Expected answer:

- m1 is first-generation multi-camera model with faster processing and actor-profile consistency, per Move AI. (1)
- m2 is second-generation with claimed improvements in spine biomechanics, 6DOF shoulder, smoother dynamic scenes, foot planting, reduced foot sliding, and multi-subject occlusion handling. (1)
- Treat m2 improvements as provider claims unless validated by production tests. (1)
- m1 and m2 skeletons have same hierarchy and 63 joints including Root. (1)
- Move rig uses FK; translation data applied to hips and rotations to joints. (1)
- Accurate retargeting needs 1:1 joint mapping and downstream root/scale/orientation validation. (1)

### 6. Privacy and consent facts (7 points)

Question: What privacy/consent warnings are required for Move AI work?

Expected answer:

- Raw video, metadata, motion data, and outputs can be personal data under Move AI's policy. (1)
- Motion data may include identifying factors such as height, proportions, mass distribution, rotations, and speed. (1)
- Move AI says it does not actively try to identify users from video/motion/output. (1)
- Move AI may use data analytics and AI/ML to improve services/products/marketing/user experience. (1)
- Move AI may use Metadata, Motion, Output, and Video to publish examples of App/API functionality/capabilities, so confidential or performer-sensitive uploads require contract/consent review. (1)
- Data may be disclosed to service providers/contractors/analytics/affiliates/legal recipients; terms page lists subprocessors including AWS and analytics/auth/payment/email/CRM tools. (1)
- Some external third parties may be outside the UK/EEA with safeguards. (1)
- Production should obtain explicit performer consent for capture, processing, retargeting, reuse, storage, publication, and cloud/local processing choice. (1)

Maximum 7. Award the publication/examples point in place of one disclosure/transfer/process-improvement detail if the answer otherwise covers the privacy risk accurately.

### 6a. API boundary check (unscored gate)

Question: Can an agent implement Move AI API upload/status/download code from public docs alone?

Expected answer: No. Public pages identify App/API services, Move API Portal/API locations, and API-related EULAs, but the consulted documentation does not provide a complete public endpoint/auth/quota reference. A production integration must use the user's portal docs, EULA/order form, credentials handling rules, and contract-specific technical spec. Penalize or fail relevant integration answers that invent endpoints, tokens, quotas, SDK package names, or rate limits.

## Production-decision questions (25 points)

### 7. Confidential AAA cinematic (8 points)

Scenario: A studio wants to capture three actors doing a close-contact fight for an unreleased game. They require local processing, individual actor tracks, and Unreal retargeting.

Expected decision:

- Choose Genesis, not Move One. (1)
- Reason from documented multi-person 1-8 capture, multi-camera operation, local/on-prem processing, individual and consolidated exports. (2)
- Recommend m2 as a candidate because Move AI claims better occlusion/multi-subject handling, while validating with a pilot. (1)
- Include setup/calibration/actor profiles/checkerboard/camera coverage and storage plan. (1)
- Include wardrobe/light/visible wrists/shoes constraints and contact blocking. (1)
- Include Unreal/FBX retarget validation: scale, root motion, 1:1 mapping, frame rate/orientation, test import before shoot approval. (1)
- Include consent/confidential data management/local access controls. (1)

### 8. Uploaded phone video from a fan event (6 points)

Scenario: A client wants to upload a vertical phone clip from a fan event with several bystanders and two dancers partly occluding each other, then use it commercially.

Expected decision:

- Warn that Move One single-file upload is documented for single person/single camera and result quality may vary; this clip is high risk. (1)
- Identify bystanders/consent/commercial rights as blockers unless releases are obtained. (1)
- Warn that Move AI policy describes use of Metadata/Motion/Output/Video for publishing App/API examples, so commercial/confidential reuse requires contract and consent review. (1)
- Mention upload format/size and camera quality constraints if proceeding. (1)
- Recommend recapture with one performer centered, locked camera, full body, 60 fps Full HD, consented controlled set; or Genesis if multi-person is required. (1)
- Avoid promising clean commercial animation from the existing clip. (1)

### 9. Biomechanics output request (5 points)

Scenario: A trainer asks for exact clinical-grade joint torque diagnosis from a Move One jump video.

Expected decision:

- State Move One biomechanics output can provide timestamped joint data, positions in meters, rotations in radians, torques in newton-meter, and foot reaction forces in Newton as documented. (1)
- Do not claim clinical diagnostic accuracy unless independently validated. (1)
- Require locked single-person capture, full body, quality constraints, and consent. (1)
- Recommend comparing output to source video and involving qualified biomechanics/medical professionals for clinical use. (1)
- Preserve data privacy because motion data can be identifying. (1)

### 10. Product-claim hygiene (6 points)

Scenario: A marketing lead asks the agent to write that Genesis is proven as accurate as optical mocap and always eliminates cleanup.

Expected decision:

- Refuse or revise unsupported absolutist phrasing. (1)
- Label Move AI's optical-quality/comparable-to-optical language as provider claim. (1)
- Recommend wording that says Move AI positions Genesis as comparable to optical systems, with production validation required. (1)
- Reject "always eliminates cleanup"; mention review/cleanup still needed for contacts, occlusion, retargeting, and root motion. (1)
- Suggest a pilot comparison against optical/reference capture if claim matters. (1)
- Keep within Move AI scope without adding unrelated general animation claims. (1)

## Applied production tasks (35 points)

### 11. Capture plan for Move One solo animation (10 points)

User request: "I need a cheap quick capture of a solo parkour vault for a Blender previs. We have one iPhone and need the animation this afternoon. Give me the Move AI plan."

Successful output characteristics:

- Selects Move One and explains fit: single performer, short/fast workflow, app or single-file upload. (1)
- Confirms duration target must fit Move One paid-plan 60-second limit if using app capture. (1)
- Gives capture setup: locked phone, full-body framing, centered performer, landscape preferred as heuristic, 60 fps Full HD for upload. (2)
- Gives wardrobe/lighting: fitted high-contrast clothing, visible wrists, light/visible shoes, avoid black/baggy/long sleeves, even lighting. (2)
- Adds pilot test and early process before full take. (1)
- Specifies exports/import: FBX or `.blend`, Blender 4+ if using `.blend`, check scale/root/feet. (1)
- Includes consent and asset archive. (1)
- Notes likely failures: hands/feet leaving frame, blur, foot sliding, vault prop occlusion. (1)

For creature/blockout variants, the answer must clarify that Move AI captures human performer motion and that creature-specific anatomy or behavior needs downstream adaptation; penalize claims that Move AI directly captures non-human creature motion from the example.

### 12. Genesis shoot-day QA checklist (10 points)

User request: "We installed Genesis for a 5-person dance shoot. What should my operator check before approving takes?"

Successful output characteristics:

- Camera/system checks: Z CAMs recording, sync/timecode, lens/focus/exposure, storage/cards/network, Peel Capture or expected capture workflow. (1.5)
- Calibration: checkerboard calibration, active volume overlay, floor marks, recalibrate if cameras/lenses/volume changed. (1.5)
- Actor profiles and metadata: performer IDs, profiles, take naming, individual reference moves. (1)
- Wardrobe/performance: contrast, no baggy/black/covered wrists, visible footwear, blocking for crossings. (1.5)
- Processing/model choice: process test, consider m2 for occlusion/dynamic/footwork but label as provider claim. (1)
- Review tools: mesh/skeleton/calibration overlays, 3D viewer, render preview, raw skeleton. (1)
- Acceptance criteria: identity continuity, limb swaps, foot plants, root drift, contacts, target retarget sample. (1.5)
- Data/security: local processing, access controls, consent, archive raw/outputs/diagnostics. (1)

### 13. Troubleshooting response (8 points)

User request: "Our Genesis output has foot sliding and the left arm pops during partnered crossings. What do we do?"

Successful output characteristics:

- Separates foot sliding and arm pop symptoms while checking shared causes. (1)
- Foot sliding checks: footwear/floor contrast, ground visibility, calibration, selected model/preset, target rig scale, root motion, retarget foot locks. (2)
- Arm pop checks: wrist visibility, sleeve/wardrobe, occlusion during crossings, camera coverage, actor profile, identity continuity, skeleton overlay. (2)
- Genesis-specific review: use mesh/skeleton/calibration overlays, 3D viewer, diagnostic visualization folder if available. (1)
- Reprocess/recapture plan: pilot with clearer wardrobe/blocking/camera coverage, consider m2 for occlusion if not already used, validate against source video. (1)
- Does not prescribe generic smoothing as the first or only fix. (1)

### 14. Export and retargeting plan (7 points)

User request: "We need Move AI data in Maya, Unreal Metahumans, and a custom analytics tool. What should we ask for and validate?"

Successful output characteristics:

- Identifies relevant formats: FBX for Maya/Unreal, possibly BVH/GLB/USDZ/Blender depending Genesis needs, JSON for custom pipeline, C3D/biomechanics where analysis requires it; Move One formats narrower. (1.5)
- Mentions Move One docs include Maya HIK, Unreal import/retarget, Metahuman, Blender, Omniverse, C4D, Unity workflows. (1)
- Mentions Genesis skeleton: 63 joints including Root, FK, hips translation, rotations on joints, 1:1 mapping. (1.5)
- Validates scale, orientation, frame rate, root motion, retarget pose, shoulder/spine/feet, compression, and sample import before batch export. (1.5)
- Keeps retarget maps/presets versioned and archives previews/source/output. (1)
- Does not invent direct live plugins or unsupported formats. (0.5)

## Overall scoring guidance

- 90-100: Precise Move One/Genesis selection, strong factual grounding, dated/claim-aware language, production-ready checklists, privacy handled naturally.
- 75-89: Good practical plan with minor missing details or limited source/claim distinction.
- 60-74: Understands broad split but misses important constraints, exports, or validation steps.
- 40-59: Generic mocap advice with some Move AI terms; risky omissions in consent, product fit, or troubleshooting.
- 0-39: Unsupported claims, wrong product recommendations, or advice that would likely break a real production.
