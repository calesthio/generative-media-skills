# Evaluation: immersive-spatial-video-production

Use this file as the hidden answer key and scoring specification. The tested agent may receive the user request and `SKILL.md`; do not expose or link this file during the production test.

Score out of 100. A passing response should demonstrate practical production judgment, not just list terminology. Award partial credit for defensible tradeoffs when the agent explicitly labels assumptions and protects viewer comfort, metadata integrity, accessibility, and rights.

## Critical Failures

Any of these should fail the evaluation regardless of total score:

- Treats the task as an interactive XR app, game-engine build, OpenXR/WebXR runtime, or world-model/volumetric generation assignment instead of passive immersive video.
- Recommends automatic forced full-immersion playback without user choice for a headset deliverable.
- Ignores stereo comfort when planning or reviewing stereoscopic 180/360/spatial video.
- Delivers or recommends only a flat crop when the user requested an immersive/spherical/spatial master.
- Omits projection/stereo metadata from a YouTube, headset, or spatial-video delivery plan.
- Exposes private people/locations/sensitive geometry without any consent, clearance, or mitigation plan.
- Claims unsupported universal facts such as "all 360 video should be stereoscopic" or "YouTube supports any ambisonic order".

## Knowledge Questions

### 1. Format Selection

Question: A client wants a headset video of a chef teaching a recipe at a counter. Viewers only need to watch the chef, hands, ingredients, and stove in front of them. Which format should the agent recommend first, and why?

Expected answer: Recommend stereoscopic VR180 or a constrained spatial/wide-FOV front-facing format, not full 360, because the action has a natural front stage, depth and hand scale matter, and crew/lighting can remain behind camera. Mention a flat fallback or companion cut if needed.

Required points:

- Identifies front-stage nature of the scene.
- Explains why 180/spatial is better than 360 here.
- Mentions stereo depth/comfort for near hands/objects.
- Does not over-prescribe one vendor.

Penalize:

- Recommending stereo 360 merely because it sounds more immersive.
- Ignoring crew/lighting and viewer attention.

### 2. YouTube Spatial Audio

Question: What spatial audio formats does YouTube document for 360-degree and VR videos?

Expected answer: First Order Ambisonics and First Order Ambisonics with Head-Locked Stereo, verified from YouTube Help in the skill. Strong answers note that head-locked stereo can carry non-diegetic narration/music and that a metadata tool/test upload may be needed.

Required points:

- Names FOA.
- Names FOA plus head-locked stereo.
- Does not claim arbitrary HOA support as a YouTube requirement.

### 3. Projection Metadata

Question: What metadata concepts must be checked when an equirectangular stereo 360 MP4 opens as a flat 2D video?

Expected answer: Check spherical projection metadata such as `sv3d`/`proj`/`equi`, stereoscopic layout metadata such as `st3d` and eye layout, default pose/yaw/pitch/roll, and whether export/transcode stripped metadata. If YouTube-bound, re-inject/export with compatible spherical metadata and retest.

Required points:

- Mentions projection metadata.
- Mentions stereo layout metadata.
- Mentions export/transcode stripping or reinjection.
- Mentions retesting in target player.

### 4. Apple Vision Pro Playback Comfort

Question: Give three Apple HIG-aligned comfort considerations for immersive video playback on visionOS.

Expected answer should include at least three of: let people choose when to start video; avoid automatically launching fully immersive playback; use system video player where appropriate; let people see surroundings or use small resizable playback when comfort matters; avoid occluding playback/transport controls in full immersion; use smooth predictable transitions; avoid encouraging movement in full/progressive immersion; respect the approximate boundary behavior; provide captions/subtitles via supported playback paths.

Penalize:

- Suggesting surprise full-screen immersion.
- Hiding controls for aesthetics.

### 5. Stereo Comfort

Question: Name common causes of discomfort in stereoscopic immersive video.

Expected answer: vertical disparity, eye order/layout errors, left/right exposure or color mismatch, sync offsets, excessive near objects, seam depth errors, rapid rotational motion, handheld shake, unstable horizon, excessive acceleration, bad stereo around poles/nadir/seams, and captions/titles placed at uncomfortable apparent depth.

Required points:

- At least four technical/staging causes.
- At least one motion/camera cause.
- At least one metadata/eye-layout or left/right mismatch cause.

### 6. Scope Boundary

Question: How should an agent use Khronos OpenXR or W3C WebXR references in this skill?

Expected answer: Only as boundary/context for interactive XR runtimes or browser sessions. The skill is for passive immersive video production, so OpenXR/WebXR should not turn the task into app design unless the user separately requests an interactive app.

## Production-Decision Scenarios

### 7. Documentary Protest In 360

Scenario: A journalist asks for a 360 video from inside a public protest, to be released online. They want the audience to "feel surrounded" and request no blurring because it hurts immersion.

Strong answer should:

- Consider whether monoscopic 360 is more appropriate than stereo 360 due to crowds, movement, privacy, and seams.
- Address consent, bystanders, faces, license plates, location sensitivity, safety, platform policy, and potential harm.
- Recommend a privacy plan: filming zones, signage/notice where feasible, selective blur, avoid vulnerable individuals, legal/editorial review.
- Use stable capture positions and careful default view/attention cues.
- Plan ambisonic bed plus clear narration if needed.
- Include a flat/contextual version if public accessibility matters.

Scoring: 10 points.

- 2 format rationale.
- 2 comfort/camera stability.
- 3 privacy/rights/safety.
- 1 audio plan.
- 1 accessibility/fallback.
- 1 platform QA.

Critical failure: accepts "no blurring" without rights/safety mitigation.

### 8. Product Launch In VR180

Scenario: A product team wants a premium VR180 headset demo where a designer presents a new physical device on a table. They also need YouTube distribution.

Strong answer should:

- Choose stereo VR180 or spatial/front-facing format and justify it.
- Plan table distance, hand/object proximity, lighting, reflections, and crew behind camera.
- Protect stereo comfort for close product handling.
- Plan captions/titles at comfortable depth and avoid seam/pole placement.
- Export/test YouTube VR180 metadata and captions; provide flat trailer or fallback.
- Mention rights/trademarks/prototype confidentiality.

Scoring: 10 points.

### 9. Construction Training

Scenario: A safety department wants headset training from a construction site and asks camera operators to walk around while filming so trainees can "move through the space."

Expected decision: Push back. For passive immersive video, avoid walking-camera locomotion if comfort matters. Recommend locked-off 360 stations, guided cuts between positions, clear default yaw, ambisonic environment, head-locked narration, captions/transcript, privacy review, and a non-headset fallback. If walking is unavoidable, keep motion short, smooth, slow, and heavily tested.

Scoring: 10 points.

- 3 comfort pushback.
- 2 safer capture alternative.
- 2 training/attention structure.
- 1 audio/caption accessibility.
- 1 privacy/site-sensitive details.
- 1 device QA.

### 10. Family Spatial Archive

Scenario: A user captured spatial video on a phone and asks for an edited Vision Pro version plus a shareable 2D version.

Strong answer should:

- Preserve native spatial/stereo metadata for the Vision Pro master.
- Avoid transcodes/edits that flatten stereo unless making the 2D derivative.
- Keep original archival files untouched.
- Test in the intended Apple playback path.
- Make a separate captioned/shareable 2D edit for non-compatible devices.
- Consider consent, minors, addresses, documents, and private spaces.

Scoring: 8 points.

## Applied Production Tasks

### 11. Write A Capture Brief

User request: "Create a capture plan for a 4-minute immersive headset video of a singer performing one song in a small club. We want the viewer to feel like they are in the front row."

Expected approach:

- Recommend stereo VR180 unless there is a strong reason for 360.
- Place camera at seated front-row eye height, at a safe distance from performer.
- Keep performer and band in forward field; manage stage lighting, flare, reflections, and audience releases.
- Record ambisonic room/crowd plus board feed/isolated vocals; decide head-locked vs world-anchored elements.
- Keep camera static or nearly static; no surprise cuts/rapid rotations.
- Plan captions/lyrics if requested, comfortable placement, and flat fallback/trailer.
- Include headset QA for stereo comfort, audio localization, captions, and low-light banding.
- Include music/performance/location rights.

Scoring rubric: 14 points.

- 2 format choice.
- 2 capture geometry/blocking.
- 2 audio plan.
- 2 comfort/stabilization.
- 2 stitch/stereo/low-light concerns.
- 1 captions/accessibility.
- 2 rights/releases.
- 1 device/platform QA.

Critical failure: ignores music/performance rights or proposes handheld walking through crowd as primary plan.

### 12. Troubleshoot Delivery

User request: "My 360 video looks correct in my editor, but after upload the platform shows a flat rectangle and the audio rotates wrong. What should I check?"

Expected output:

- Explain that editor preview does not prove delivery metadata.
- Check projection metadata, stereo layout, default pose, export path, and whether metadata was stripped.
- Check ambisonic channel order, normalization, orientation, head-locked vs world-locked tracks, and platform-supported audio layout.
- Re-export/re-inject metadata using platform-compatible tools.
- Run a short private test upload and headset playback check.
- Confirm captions/subtitles and fallback after processing.

Scoring rubric: 12 points.

- 4 video metadata diagnosis.
- 3 audio metadata/orientation diagnosis.
- 2 platform support/tooling.
- 2 test protocol.
- 1 clear user-facing explanation.

### 13. Review An Immersive Cut

User request: "Review this plan: We will shoot stereo 360 in a hospital ward, hide crew with AI paint-out, put animated labels everywhere, and upload publicly to YouTube."

Expected response:

- Identify high privacy and consent risk: patients, staff, medical info, screens, room layouts, location sensitivity.
- Challenge stereo 360 in a tight ward due to seams, near objects, comfort, and crew hiding difficulty.
- Recommend controlled/staged environment or monoscopic/VR180/flat alternative depending intent.
- Require releases, legal/privacy review, signage, de-identification, and platform-policy review.
- Reduce labels; place essential captions/callouts comfortably and accessibly.
- Plan device QA and private upload testing if public release remains appropriate.

Scoring rubric: 12 points.

- 4 privacy/rights/sensitive location.
- 3 format/comfort critique.
- 2 graphics/captions/accessibility.
- 2 safer alternative production path.
- 1 platform QA.

Critical failure: treats AI paint-out as sufficient privacy clearance by itself.

## Source And Claim Quality

Across any generated answer, award up to 8 points for evidence handling:

- 3 separates documented facts from production heuristics or assumptions.
- 2 dates volatile platform facts or avoids pretending they are timeless.
- 2 cites or names authoritative source categories when making consequential claims.
- 1 avoids provider marketing language and unsupported rankings.

Penalize unsupported exact specs unless the user supplied them or the skill documents them. It is acceptable to say "verify the current target-player spec" for codec/bitrate/resolution details that vary by player.

## Overall Scoring Guide

- 90-100: Production-ready. Makes conservative, source-aware format decisions; protects comfort, metadata, audio, captions, QA, and rights; gives actionable steps.
- 75-89: Strong but missing one moderate area such as detailed audio QA, captions, or fallback planning.
- 60-74: Usable outline but too generic, weak on platform metadata, comfort, or rights.
- 40-59: Knows some immersive terms but would likely cause delivery or comfort failures.
- Below 40: Mis-scoped, unsafe, or mostly ordinary video advice.
