# Evaluation: virtual-production-icvfx

Do not expose this file to the evaluated agent. The evaluated agent receives the user request and `SKILL.md` only. Score for applied production judgment, factual accuracy, and the ability to separate documented facts from heuristics.

Total: 100 points.

## Core Knowledge: 28 Points

1. What is the difference between inner frustum and outer frustum in ICVFX? (5 pts)
   - Expected: inner frustum is the camera-visible, tracked, camera-perspective render based on camera pose/lens/FOV; outer frustum is outside the camera FOV and supplies stable environmental light/reflections. (5 pts)
   - Notes that outer frustum should not simply move with the camera like the inner frustum. (bonus within above, not extra)
   - Penalize: describes both as generic wall regions, or says outer frustum is irrelevant to final image.

2. Why is pixel pitch alone insufficient for LED suitability? (5 pts)
   - Expected: pixel pitch affects pixel density/resolution, but suitability also depends on camera distance, sensor, lens/focus, viewing angle, moire risk, color shift, uniformity, heat, brightness, refresh/scan, content, and budget. (5 pts)
   - Penalize: treats lowest pitch as automatically best.

3. Explain timecode versus genlock in an Unreal/ICVFX context. (6 pts)
   - Expected: timecode makes devices/Unreal reference matching frame labels/time values; genlock locks frame generation/presentation cadence to a shared reference so frames occur at the right time. (4 pts)
   - Mentions Unreal Timecode Provider and Custom TimeStep or equivalent verification. (1 pt)
   - Mentions cluster display sync/framelock/render sync as a separate but related issue. (1 pt)
   - Penalize: says timecode alone prevents tearing or makes all frames present simultaneously.

4. What role does Live Link play, and what are common timing pitfalls? (5 pts)
   - Expected: streams external data such as camera, transform, lights, or lens-related subjects into Unreal; data is organized as sources/subjects/roles. (2 pts)
   - Mentions evaluation modes/buffering/timecode and the need for a Timecode provider if using Timecode evaluation. (2 pts)
   - Mentions network adapter/UDP/message bus or packaged `-messaging` caveat as relevant. (1 pt)

5. Why should some screen-space effects be avoided in nDisplay ICVFX? (4 pts)
   - Expected: screen-space effects can differ across viewports/nodes and cause seams or border artifacts in clustered rendering; examples include SSR, SSAO, SSGI, vignette, eye adaptation, bloom. (4 pts)

6. What does camera/lens calibration need to capture beyond camera transform? (3 pts)
   - Expected: lens distortion, focal length, focus/iris behavior, nodal/entrance-pupil offset, tracker-to-camera offset, lens files/calibration data, and timing alignment. (3 pts)

7. Name safety and rights/data issues that must be cleared before treating an LED-volume take as production-ready. (4 pts)
   - Expected: qualified stage/production safety authority; LED brightness, flicker, flashing/photosensitivity; electrical, rigging, egress, heat, moving-rig, and IR/laser/tracking hazards; vulnerable performer accommodations; asset/plate/trademark clearance; likeness/scan consent; retention/access rules for tracking/lens/take/witness/scan data; and final-pixel versus fallback labeling. (4 pts)
   - Penalize: treats safety or consent as optional paperwork, or says the virtual-production supervisor alone can approve all safety/legal/privacy matters.

## Production Decision Scenarios: 30 Points

1. Scenario: A director wants a macro product shot with a sharp LED background six feet behind a reflective chrome object. Decide whether ICVFX final-pixel is suitable. (8 pts)
   - Strong answer: flags high risk due to moire/pixel visibility, focus on LED, reflective surface revealing panel/seams, and macro/shallow-stage constraints. (4 pts)
   - Proposes tests with actual camera/lens/panel and alternatives such as LED for reflections only, physical backdrop, larger distance, different blocking, lower pitch, or post comp. (3 pts)
   - Avoids blanket rejection; frames as testable suitability. (1 pt)

2. Scenario: A curved LED wall uses an exported calibration mesh; an agent proposes a simple flat nDisplay screen config because it is faster. Evaluate the proposal. (7 pts)
   - Expected: rejects or challenges it for final-pixel curved-wall work; geometry/projection must match the real display and calibrated projection policy/mesh/MPCDI/VIOSO/etc. may be needed. (4 pts)
   - Notes that physical measurements, coordinate origin, screen normals, and projection policy must be verified. (2 pts)
   - Allows a simple config only for rough previs or explicitly non-camera-critical use. (1 pt)

3. Scenario: During a camera move, alignment is correct on a static chart but swims dynamically. What is the troubleshooting priority? (8 pts)
   - Expected: prioritize timing/latency checks: timecode/genlock, Live Link evaluation mode/offset, tracking latency/smoothing, lens metadata latency, Timed Data Monitor, and repeatable recorded test. (5 pts)
   - Then verify dynamic spatial calibration/nodal offset under motion. (2 pts)
   - Does not immediately rebuild all assets or blame only wall geometry. (1 pt)

4. Scenario: A final-pixel take fails because helmet reflections resolve panel structure, but the LED lighting looks good. What fallback should be recommended? (7 pts)
   - Expected: switch inner frustum to green/live comp fallback while keeping outer frustum environment for lighting/reflections if useful. (3 pts)
   - Record tracking, lens data, clean plates, color charts, Unreal/nDisplay state, OCIO/LUTs, and incident notes. (3 pts)
   - Warns not to represent live comp preview as final unless pipeline/deliverable are defined. (1 pt)

## Applied Production Tasks: 32 Points

1. Create a pre-shoot QA checklist for a one-day ICVFX car-process shoot. (12 pts)
   - Must include LED geometry/pixel pitch/viewing distance and moire/scan tests. (2 pts)
   - Must include tracking/lens calibration and timing checks. (2 pts)
   - Must include nDisplay cluster/render-node/sync/performance checks. (2 pts)
   - Must include color/OCIO/LUT/through-camera verification. (2 pts)
   - Must include qualified safety authority, LED brightness/flicker/photosensitivity, electrical/rigging/egress/heat/moving-rig/tracking-emission checks, vulnerable performer accommodations, rights/clearance/consent review, data-retention/access rules, fallback, records, roles, and handoff items. (4 pts)

2. Draft a response to a DP asking whether a 270-degree LED volume is required. (8 pts)
   - Strong answer: ties volume shape to shot needs, not prestige; 270 degrees may be needed for fully virtual environments and wraparound reflections/lighting, while one-sided/curved/set-window walls can work with physical set builds or limited camera angles. (4 pts)
   - Discusses ceiling/side returns for reflections and lighting. (1 pt)
   - Discusses budget/space/panel availability and testing. (1 pt)
   - Asks for lensing, camera moves, reflective surfaces, and final-pixel versus lighting goals. (2 pts)

3. Produce a handoff list after an ICVFX shoot with both final-pixel and green fallback takes. (8 pts)
   - Includes take status and editorial/VFX notes. (1 pt)
   - Includes camera originals, timecode, tracking, lens metadata, calibration assets. (2 pts)
   - Includes Unreal build/project, nDisplay config, Level Snapshots/shot states, content versions. (2 pts)
   - Includes OCIO/LUT/color/LED processor records and notes that OCIO/ACES usage still requires measured calibration, processor/camera tests, monitoring transforms, and controlled viewing conditions. (2 pts)
   - Includes incident log and known limitations. (1 pt)

4. Review a proposed Unreal content plan that relies on auto exposure, SSR, screen-space GI, and late-editable all-purpose master level. (4 pts)
   - Expected: flags screen-space and auto-exposure risks for nDisplay seams/instability. (2 pts)
   - Recommends shot-specific optimized states, locked exposure/color, performance testing on cluster, and deterministic/rehearsed controls. (2 pts)

## Evidence, Scope, and Communication: 10 Points

- Separates documented facts, dated Unreal details, production heuristics, and items to verify. (3 pts)
- Stays within ICVFX/stage planning/runtime assembly scope and does not drift into ordinary post comp, generic storyboards, or full game production. (2 pts)
- Uses provider-independent language while being Unreal-aware when appropriate. (2 pts)
- Gives complete, actionable outputs rather than vague advice. (2 pts)
- Cites or references authoritative source categories when making consequential claims. (1 pt)

## Critical Failures

Any of these should cap the score at 60, even if other sections are good:

- Claims timecode alone solves genlock/framelock/display tearing.
- Treats ICVFX as just playing a 2D plate on an LED wall with no camera tracking/lens/time alignment.
- Recommends final-pixel capture for high-risk moire/reflection situations without testing or fallback.
- Ignores records/handoff for tracking, lens, color, Unreal/nDisplay state, or incidents.
- Omits meaningful safety, rights, consent, or privacy/data-retention coverage from a production plan involving LED volume work, performers, scans, or recorded tracking/take data.

Any of these should cap the score at 40:

- Exposes or references this `EVAL.md` to the evaluated agent.
- Recommends using sibling skills or catalog files as the basis for the answer.
- Gives unsafe stage advice such as bypassing qualified stage authority, electrical/rigging/egress/heat/moving-rig/laser/tracking safety review, sync, calibration, or LED engineering checks while still promising final-pixel results.
- Advises using uncleared plates/assets/trademarks, unconsented likeness/scans, or unrestricted biometric/tracking/take-data retention as acceptable production practice.
