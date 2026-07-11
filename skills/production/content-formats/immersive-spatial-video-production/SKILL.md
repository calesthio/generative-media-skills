---
name: immersive-spatial-video-production
description: Use this skill to plan, direct, finish, and QA provider-independent mono or stereo 180-degree, 360-degree, spherical, spatial, wide-FOV, and immersive video. It covers format choice, capture rigs, stitching, nadir and seam management, stereoscopic comfort, attention direction, stabilization, ambisonic and spatial audio, titles, captions, accessibility, edit, color, VFX, projection metadata, Vision Pro, YouTube, headset delivery, device QA, and privacy, location, and likeness rights. Do not use it for interactive XR apps, volumetric/world-model generation, game-engine experiences, or provider-specific video generation prompts.
---

# Immersive Spatial Video Production

This skill is for passive video deliverables that surround or partially surround the viewer: monoscopic 360, stereoscopic 360, VR180, spatial video, dome/wide-FOV video, and headset-first immersive films. It helps an agent make production decisions, write capture and finishing plans, review outputs, and troubleshoot delivery failures without depending on one camera vendor, headset, or generator.

Do not activate this skill for interactive XR applications, OpenXR/WebXR app design, volumetric scene generation, Gaussian-splat/world-model navigation, realtime game-engine builds, or ordinary flat 16:9/9:16 edits unless the requested output explicitly needs spherical, stereo, spatial, wide-FOV, or headset delivery.

## Evidence Map

Documented facts below use these sources, verified 2026-07-11 unless a source date is named inline:

- Apple Human Interface Guidelines, "Immersive experiences," https://developer.apple.com/design/human-interface-guidelines/immersive-experiences. Access path: Apple Developer > Design > Human Interface Guidelines > Immersive experiences. Supports the visionOS passthrough, immersion-style, 1.5-meter boundary, movement, permission, attention-cue, and transition-comfort claims in this skill.
- Apple Human Interface Guidelines, "Playing video," https://developer.apple.com/design/human-interface-guidelines/playing-video. Access path: Apple Developer > Design > Human Interface Guidelines > Playing video. Supports the system video player, original aspect ratio, subtitles/transport controls, visionOS comfort, automatic full-immersion warning, thumbnail-track, and RealityKit closed-caption claims in this skill.
- Apple Developer Documentation, "Reading stereoscopic 3D video files," https://developer.apple.com/documentation/avfoundation/media_reading_and_writing/reading_stereoscopic_3d_video_files. Access path: Apple Developer > Documentation > AVFoundation > Media reading and writing > Reading stereoscopic 3D video files. Used only for the narrow claim that Apple documents AVFoundation workflows for reading stereoscopic video files.
- Apple Developer Documentation, "Writing spatial video," https://developer.apple.com/documentation/avfoundation/media_reading_and_writing/writing_spatial_video. Access path: Apple Developer > Documentation > AVFoundation > Media reading and writing > Writing spatial video. Used only for the narrow claim that Apple documents AVFoundation workflows for writing spatial video.
- YouTube Help: Upload 180- or 360-degree videos; Use spatial audio in 360-degree and VR videos.
- Google Spatial Media Spherical Video V2 RFC and Spatial Audio RFC, plus Spatial Media Metadata Injector v2.1 release notes.
- Khronos OpenXR and W3C WebXR specifications for boundary definition only: they describe interactive XR runtimes, not passive video production deliverables.
- Professional production heuristics are labeled as heuristics, because comfort thresholds vary by headset optics, viewer sensitivity, screen scale, and playback app.

## What The Agent Must Decide First

Start by asking what kind of presence the viewer needs, then choose the smallest immersive format that achieves it.

| Format | Use when | Avoid when | Production implications |
| --- | --- | --- | --- |
| Monoscopic 360 | Place, event, journalism, architecture, documentary context, or location survey where looking around matters more than depth | Close human performance, intimacy, objects within arm's reach, heavy motion | Simpler rig and stitch; weaker scale/depth; hides crew poorly because everything is visible |
| Stereoscopic 360 | Viewer should perceive depth throughout a full sphere | Fast action near the rig, many seam crossings, low budget, heavy VFX, viewers may watch on flat screens | Hardest stitch; depth mismatches around seams and poles can be uncomfortable; needs headset QA |
| VR180 stereo | Performance, education, travel, sports, product demo, or story content with a natural front stage | Viewer must inspect behind them or understand a full environment | Stronger stereo quality and easier directing; crew can work behind camera; attention stays forward |
| Apple-style spatial video | Personal memories, intimate documentary, object-scale moments, headset/photo-library viewing | Need full 180/360 environment or platform-neutral spherical playback | Treat as stereoscopic video with constrained FOV; preserve native metadata and test in target Apple playback path |
| Dome or wide-FOV immersive | Planetarium, installation, simulator, or venue projection | Headset distribution is primary | Requires venue mapping, safe horizon, and playback-system tests rather than generic YouTube metadata |
| Flat companion cut | Marketing, accessibility, social trailer, editorial review, stakeholders without headsets | It is the only deliverable for an immersive-first commission | Reframe from the spherical master; do not simply crop random viewports without attention design |

Documented fact: YouTube supports upload and playback of 180-degree and 360-degree spherical videos on desktop browsers and YouTube/YouTube VR apps on many VR headsets; YouTube spatial audio supports First Order Ambisonics and First Order Ambisonics with head-locked stereo. Verified 2026-07-11 from YouTube Help.

Production heuristic: prefer VR180 stereo over 360 stereo when the story has a clear front, because it gives the viewer stronger depth and the crew a safe working zone behind camera. Use full 360 only when the viewer genuinely benefits from turning around.

## Capture Planning

A useful immersive video brief includes:

- viewer posture: seated, standing, walking only in the real world, or venue-seated;
- intended viewer agency: look-around ambience, front-stage performance, guided attention, or inspection;
- platform priority: Vision Pro, YouTube VR, Quest browser/player, dome, museum player, native app, archival master;
- stereo requirement: mono, stereo 180, stereo 360, spatial video, or both stereo and monoscopic fallbacks;
- audio requirement: mono/stereo, head-locked stereo, FOA ambisonics, FOA plus head-locked narration/music, or platform-specific spatial mix;
- accessibility requirement: captions/subtitles, transcript, audio description, motion-comfort version, and flat fallback;
- rights boundary: people, private property, sensitive location geometry, bystanders, signage, music, and platform terms.

Capture rig decisions:

- Use fewer lenses when possible. Every lens boundary is a seam, and seams are where parallax, exposure, flare, and timing mismatches become visible.
- For 360 mono, prioritize dynamic range, synchronized exposure, and clean lens overlap.
- For stereo 360, prioritize synchronized shutters, stable interaxial geometry, calibration, and subjects kept away from seam zones.
- For VR180 stereo, prioritize lens cleanliness, level horizon, viewer eye-height placement, and a front-stage blocking plan.
- For spatial video, preserve the camera's native stereo relationship and metadata through ingest and export; avoid transcoding steps that flatten stereo to 2D unless intentionally making a companion cut.
- For action, prefer moving the subject within a stable world over moving the rig. When the rig must move, choose smooth pathing, low acceleration, and a visible stable horizon.

Documented fact: Apple HIG says people should be able to choose when to start video and should not be automatically launched into fully immersive video; it also recommends keeping people able to see surroundings during playback and avoiding virtual content that obscures playback controls in fully immersive contexts. Verified 2026-07-11.

Production heuristic: set the camera at or near the viewer's expected eye height. Unmotivated high, low, or tilted placement can make viewers feel like a floating observer rather than present in the scene.

## Stitch, Nadir, Poles, And Seams

Treat stitch quality as a story and comfort problem, not only a technical cleanup pass.

Pre-shoot seam strategy:

- Draw seam maps for the chosen rig before blocking actors or action.
- Keep faces, hands, text, product labels, and close foreground objects out of known seam corridors.
- Put seam lines through low-detail, distant, or static areas when possible.
- Control lighting so neighboring lenses do not disagree on exposure or white balance.
- Slate and sync all cameras and recorders; even small temporal offsets can break stitch and stereo comfort.

Post stitch review:

- Check the horizon level before creative stabilization.
- Inspect seams while scrubbing, not only on still frames.
- Review high-contrast lines, moving limbs, reflective objects, smoke, water, and crowds.
- Patch nadir only when the patch is less distracting than the rig footprint. A blurred disk under the viewer may be more honest and comfortable than a warped fake floor.
- Keep pole regions clean, because equirectangular distortion can hide defects in edit view that become obvious in headset playback.

Production heuristic: if a subject must cross a seam, stage the crossing far from the rig and in a low-attention moment. A distant seam crossing is often acceptable; a near-face seam crossing is usually a reshoot or reframing problem.

## Stereo Depth And Comfort

Stereo comfort failures are among the fastest ways to make immersive video unusable. Review stereo as early as possible, ideally on the target headset.

Comfort principles:

- Keep the viewer's expected forward direction stable unless a motivated reveal requires otherwise.
- Avoid rapid rotational motion, handheld shake, and acceleration that the viewer's body does not feel.
- Avoid forcing viewers to converge on very near objects for long periods.
- Avoid objects passing extremely close to the camera unless the whole piece is designed around that effect and tested.
- Avoid vertical disparity, left/right exposure mismatches, left/right color mismatches, sync offsets, and stereo window violations.
- For 360 stereo, be extra cautious near seams, zenith, and nadir because stereo correspondence can degrade there.
- For titles and captions, place text at a comfortable apparent distance and keep it stable relative to the viewing context.

Apple documented fact: visionOS immersive experiences use passthrough to keep people connected to physical surroundings; in progressive and full immersion, the system defines an approximately 1.5-meter boundary and increases passthrough/fades the experience as the wearer approaches or passes it. Apple also advises avoiding encouraging movement in progressive or full immersion. Verified 2026-07-11.

Production heuristics:

- Prefer seated or stationary viewing unless the deliverable is intentionally designed for a supervised venue.
- Keep critical action inside the viewer's natural forward field most of the time. Let viewers explore between beats, not during beats that carry plot, safety, or instructions.
- When judging stereo, use a conservative viewer, not the most VR-tolerant person on the team.
- If the camera moves, make the path visually predictable and give viewers stable references such as floor, horizon, architecture, or vehicle frame.

## Blocking And Attention Direction

Immersive video cannot assume the editor controls the frame, so direction must be built into staging, audio, lighting, and motion.

Attention cues that usually work:

- actor eyeline and body orientation;
- sound arriving from the area of interest;
- brightness, color contrast, or motion contrast in the intended region;
- foreground-to-background movement that leads the gaze;
- objects entering from peripheral vision slowly enough to be noticed;
- temporary quiet or stillness elsewhere in the sphere;
- repeated spatial geography, so viewers learn where important things happen.

Avoid relying on:

- hard cuts that move the viewer's facing direction without preparation;
- tiny details hidden outside the likely forward field;
- subtitles as the only clue to look somewhere;
- constant action in every direction;
- sudden loud sounds behind the viewer without narrative reason.

Production heuristic: in immersive story cuts, treat every shot as a stage picture plus an invitation. The viewer should know where to look, but should not feel punished for looking elsewhere.

## Stabilization And Motion

Stabilization must preserve orientation truth while reducing discomfort.

- Level the horizon unless a stylized or physical reason justifies roll.
- Correct jitter before creative reframing.
- Avoid excessive yaw smoothing that lags behind a moving platform and makes the world feel detached.
- If walking footage is unavoidable, test whether a shorter cut, locked forward view, or flat companion cut is more humane.
- In 360, stabilization can reveal blank or patched areas at poles and nadir; inspect after stabilization, not before only.
- For headset playback, verify that metadata and pose are still correct after stabilization and export.

Apple documented fact: Apple HIG recommends smooth, predictable transitions between immersive styles and warns that sudden transitions can be disorienting or uncomfortable. Verified 2026-07-11.

## Spatial And Ambisonic Audio

Audio often does more attention work than the picture.

Use these layers deliberately:

- Ambisonic bed: environment, crowd, room tone, ambience, diegetic space.
- Directional objects or panned elements: attention cues and visible sound sources.
- Head-locked stereo: narration, music, accessibility narration, or UI-like content that should not rotate with the viewer.
- Standard stereo fallback: non-headset delivery and flat companion cuts.

Documented fact: YouTube accepts First Order Ambisonics and First Order Ambisonics with Head-Locked Stereo for 360-degree and VR videos. Its upload guidance says to create the 360/VR video with spatial audio, run the latest Spatial Media metadata tool, and upload the result. Verified 2026-07-11.

Documented fact: Google's Spatial Audio RFC defines an MP4 `SA3D` box for spatial audio metadata. For first-order periphonic ambisonics, four ambisonic components are required, and the RFC describes ACN channel ordering and SN3D normalization. Verified 2026-07-11.

Production heuristics:

- Record a clean ambisonic bed at camera position, plus isolated lavs/booms for dialogue. The ambisonic recording alone is rarely enough for intelligible speech.
- Keep narration head-locked unless there is a strong story reason for the narrator to occupy a world position.
- Do not over-pan every sound. Stable ambience plus a few meaningful spatial cues is usually more comfortable than a busy sphere.
- Always check audio rotation in headset: front should sound front, left should sound left, and head-locked elements should remain attached to the viewer.

## Titles, Captions, Subtitles, And Accessibility

Immersive text must be readable, comfortable, and discoverable without becoming a visual trap.

Documented facts:

- Apple HIG Playing video says the system video player provides transport controls that include subtitle options, and RealityKit video playback supports closed captions. Verified 2026-07-11.
- Apple advises restricting extra metadata/overlays so they do not obscure media playback, and in fully immersive contexts warns against virtual content obscuring playback or transport controls. Verified 2026-07-11.

Caption and title guidance:

- Prefer captions that follow the viewer's current forward view or sit in a consistent comfortable lower region, depending on platform capability.
- For speaker identification, combine caption labels with spatial audio and blocking; do not make viewers spin to find every speaker.
- Avoid placing captions at the equirectangular poles or across stitch seams.
- Keep caption depth consistent and comfortable in stereo deliverables.
- Use high contrast without pure bright panels that burn into OLED displays or dominate the scene.
- Provide transcript and flat captioned fallback when platform caption support for immersive playback is uncertain.
- For accessibility, include motion warnings, seated-viewing guidance, audio description when visual-only information matters, and a non-immersive fallback for viewers who cannot or do not want to use a headset.

Production heuristic: if a viewer misses the story when looking 30 degrees away from center, the issue is not just captions; it is staging and attention design.

## Edit, Color, And VFX

Editing immersive video means preserving spatial continuity while still shaping time.

Edit rules:

- Cut on motivated attention shifts, audio cues, or moments of low movement.
- Avoid cutting from one forward direction to a radically different forward direction without a cue.
- Keep shot durations long enough for orientation, especially after entering a new environment.
- Build a flat review cut only as a proxy; final decisions need headset review.
- Use dissolves sparingly. Crossfading spherical scenes can produce confusing double environments.

Color rules:

- Match exposure and white balance across lenses before look creation.
- Avoid heavy vignettes or edge treatments that become obvious when the viewer turns.
- Check banding in sky, walls, gradients, and low-light ambisonic concert/event scenes.
- For stereo, match left/right grade precisely.

VFX rules:

- Work in the correct projection or convert to a VFX-friendly representation, then return with validated projection metadata.
- Paint-outs must survive head movement and stereo disparity; a patch that works in one viewport may fail from another viewing direction.
- Track graphics in spherical coordinates or as world-locked elements, not as arbitrary flat overlays.
- Never hide legal/privacy issues with cosmetic blur alone if the release plan requires consent or location clearance.

## Projection, Container, And Metadata

Delivery failure often comes from metadata, not pixels.

Documented facts from Google Spatial Media Spherical Video V2 RFC, verified 2026-07-11:

- MP4 spherical video metadata is stored in an `sv3d` box in the visual sample entry, with projection information in a `proj` box.
- MP4 stereoscopic layout can be signaled with an optional `st3d` box. Defined stereo modes include monoscopic, top-bottom, left-right, stereo-custom, and right-left.
- Equirectangular projection is signaled with an `equi` projection box; cubemap with `cbmp`; mesh projection with `mshp`.
- WebM/Matroska uses a `Projection` master element inside the video track's `Video` element, with projection type values including rectangular, equirectangular, cubemap, and mesh.
- Pose metadata includes yaw, pitch, and roll values so the intended default view can be set.
- The Spatial Media Metadata Injector v2.1 release notes state support for VR180 and an additional non-diegetic head-locked stereo track in the spatial audio stream; release date August 27, 2018.

Metadata checklist:

- Correct projection: equirectangular, cubemap, mesh, VR180, or platform-native spatial video.
- Correct stereo layout: mono, top-bottom, left-right, right-left, or custom as required by player.
- Correct default view: yaw, pitch, roll; horizon level; forward direction aimed at the intended first beat.
- Correct audio metadata: ambisonic order, channel ordering, normalization, and head-locked stereo if used.
- Correct captions/subtitles track and language labels.
- Correct aspect ratio without embedded letterbox or pillarbox padding unless the target explicitly requires it.
- Correct color space, transfer, HDR/SDR signaling, and bitrate ladder for the platform.

Apple documented fact: Apple HIG Playing video says video should be displayed at original aspect ratio and warns that embedded letterbox or pillarbox padding can prevent correct scaling in playback modes. Verified 2026-07-11.

## Platform Delivery Notes

### Vision Pro and Apple playback

Use Apple playback guidance when the target is visionOS, Photos, AVKit, RealityKit, or a native app.

Documented facts, verified 2026-07-11:

- Apple recommends the system video player for familiar playback behavior unless a custom player is truly needed.
- Apple says viewers should choose when video starts and should not be unexpectedly launched into full immersion.
- Apple recommends a small resizable playback window when helping people stay comfortable, and making sure people can see surroundings during playback.
- In fully immersive video, Apple notes the system places the video player predictably and warns against occluding playback or transport controls.
- Apple recommends thumbnail tracks for scrubbing; its HIG notes 160 px width thumbnails for visionOS trick play.
- Apple publishes AVFoundation documentation titled "Reading stereoscopic 3D video files" and "Writing spatial video"; preserve stereo/spatial metadata when targeting Apple spatial playback and verify the export path in the intended Apple player.

Practical delivery approach:

- Keep a platform-native mezzanine with original stereo/spatial metadata.
- Export an Apple-targeted file only through tools known to preserve MV-HEVC/stereo metadata when spatial video is required.
- Test in the actual target path: Photos, TV app, Quick Look, AVPlayerViewController, RealityKit video player, or custom app.
- Verify captions, audio language, scrub thumbnails, resume behavior, and whether system controls remain usable.

### YouTube and YouTube VR

Documented facts, verified 2026-07-11:

- YouTube supports 180-degree and 360-degree spherical videos on current major desktop browsers and in YouTube/YouTube VR apps on many VR headsets.
- YouTube tells creators to prepare the file with its metadata tool before upload for spatial/VR metadata workflows.
- YouTube spatial audio support is First Order Ambisonics and First Order Ambisonics with Head-Locked Stereo.

Practical delivery approach:

- Upload a short private/unlisted test before final delivery.
- Confirm YouTube recognizes the file as 180/360 and preserves intended stereo mode.
- Confirm the default opening view.
- Check spatial audio on a headset, not just desktop browser playback.
- Check captions/subtitles after YouTube processing, including language labels and timing.

### Meta Quest, other headsets, and local playback

When official player requirements differ, treat each target player as a separate delivery.

- Confirm supported container, codec, maximum resolution, maximum bitrate, frame rate, stereo layout, projection, subtitles, and audio layout.
- Test sideloaded/local playback as well as streaming playback if both are part of delivery.
- Check whether the player interprets equirectangular, cubemap, mesh, VR180, top-bottom, or side-by-side layouts correctly.
- Check whether the app honors spatial audio metadata or only plays a stereo downmix.
- Confirm recenter behavior, transport controls, subtitles, and comfort settings.

Boundary note: Khronos OpenXR and W3C WebXR are relevant when building interactive runtimes or browser XR sessions, but this skill excludes interactive XR apps. Use those standards only to understand playback/runtime boundaries, not to turn this deliverable into an app-design task.

## Device QA Protocol

Run QA in three layers.

File inspection:

- container opens;
- duration, frame rate, resolution, codec, bitrate, color, and audio tracks match spec;
- projection and stereo metadata are present;
- captions/subtitles are present and language-tagged;
- audio channel order and head-locked/stage-locked behavior are documented;
- no accidental flat transcode or letterbox padding.

Viewport review on desktop:

- default view is correct;
- horizon is level;
- seams, nadir, zenith, and titles survive scrubbing;
- no visible rig shadow/reflection/crew unless intentional;
- text is readable in the intended viewport;
- color and exposure are consistent around the sphere.

Headset review:

- open in each target app/device;
- test first minute, densest action, every transition, captions, audio, and end state;
- check viewer comfort while seated and, if relevant, standing;
- rotate head through full range during seams, titles, and sound cues;
- verify stereo depth, scale, and vertical alignment;
- verify controller/hand/system UI does not block essential content;
- have at least one reviewer unfamiliar with the piece watch without coaching, then ask where they looked and what they missed.

Production heuristic: never accept a spherical video based only on an equirectangular timeline preview. Many failures are invisible until the viewer can turn their head.

## Privacy, Location, Likeness, And Rights

Immersive capture records more than conventional video. It may capture bystanders, private interiors, security layouts, precise geography, license plates, screens, reflections, conversations, and biometric-like likeness from many angles.

Required rights checks:

- location releases for private property and controlled venues;
- participant releases for recognizable people, performers, hosts, and crew who appear in reflections or nadir/pole patches;
- bystander strategy for public spaces;
- music, performance, artwork, signage, trademarks, and projected media clearances;
- sensitive-location review for schools, hospitals, homes, workplaces, religious spaces, shelters, security checkpoints, and restricted sites;
- platform policy review for the target distribution platform;
- privacy review for spatial maps, room layouts, or headset sensor data if the deliverable becomes part of an app pipeline.

Apple documented fact: Apple HIG says apps that need sensitive data such as nearby physical objects, room layout, or hand positions must request permission. Verified 2026-07-11. For this passive-video skill, avoid collecting such runtime data unless a separate app workflow explicitly requires it.

Production heuristic: in 360 capture, assume every crew member, lighting stand, monitor, brand mark, and bystander will be seen unless a documented hiding, release, or paint-out plan exists.

## Failure Modes And Repairs

| Symptom | Likely cause | Repair |
| --- | --- | --- |
| Player opens as flat video | Missing/stripped projection metadata | Re-inject or export with correct spherical/spatial metadata; retest target player |
| Left/right depth feels inverted | Stereo layout wrong, eyes swapped, right-left vs left-right mismatch | Correct stereo layout metadata or eye order; verify on headset |
| Viewer feels pulled or sick during motion | Camera acceleration, roll, unstable horizon, excessive rotational motion | Shorten shot, stabilize horizon, choose static angle, add flat fallback |
| Dialogue location does not match picture | Ambisonic orientation wrong, channel order wrong, bad pan automation | Correct orientation/channel map; run headset audio rotation check |
| Caption is hard to find | Caption locked to world behind viewer or placed at seam/pole | Use head-following or comfortable forward placement; provide transcript/fallback |
| Seams visible on faces/hands | Blocking crossed seam too close, poor calibration, sync mismatch | Re-stitch if possible; cut around; reshoot with seam map |
| Nadir patch distracts | Rig removal too sharp, warped floor, moving shadows | Use subtler patch, crop/mask if format allows, or embrace visible tripod if acceptable |
| YouTube ignores spatial audio | Unsupported layout or missing SA3D/spatial metadata | Use FOA or FOA plus head-locked stereo; run metadata tool; private upload test |
| Vision Pro playback loses spatial effect | Transcode flattened stereo/spatial metadata | Return to native capture master; export through metadata-preserving workflow |

## Complete Example: VR180 Museum Performance

Example, not a required formula.

Production intent: create a 6-minute headset-first performance video of a chamber musician in a museum gallery, with a flat trailer for social promotion.

Chosen format: stereoscopic VR180, because the performer and artwork are front-stage and the crew can safely operate behind camera. Full 360 would add privacy and lighting problems without adding story value.

Capture plan:

- Seat camera at audience eye height, centered 2.5 to 3.5 meters from performer.
- Keep performer, instrument, and featured artwork inside the central forward field.
- Record native stereo VR180 video, ambisonic room tone at camera, lav/spot mic for instrument, and room impulse/clean ambience.
- Hide crew, monitor, and lighting behind the 180 field; clear reflective surfaces in the visible half.
- Capture 30 seconds of empty room tone and a calibration slate.

Direction:

- Performer enters from front-left and settles center.
- Gallery light subtly favors the artwork the performer references.
- No action behind the viewer; attention is guided by music, gaze, and lighting.

Post:

- Stitch/align stereo and inspect eye comfort on target headset.
- Mix instrument primarily world-anchored, room tone ambisonic, intro narration head-locked.
- Add captions in a comfortable lower-forward region, speaker/music labels included.
- Export headset master with stereo metadata preserved and flat 16:9 trailer reframed from the master.

QA:

- Headset review for stereo comfort, caption legibility, audio direction, and whether the viewer notices the artwork cue.
- Flat trailer review separately; do not judge headset comfort from the trailer.

Likely failure modes:

- Reflections reveal crew.
- Captions sit too close or too low.
- Instrument spot mic feels disconnected from the visual source.
- The viewer misses the artwork cue if lighting and gaze are too subtle.

Meaningful variations:

- If the museum requires full room context, shoot a short monoscopic 360 establishing scene separately and cut into VR180 performance only after an audio cue.
- If headset delivery is uncertain, make stereo VR180 primary but generate a monoscopic 180 and flat fallback.

## Complete Example: 360 Construction-Site Safety Walkthrough

Example, not a required formula.

Production intent: train contractors by placing them in real site conditions while keeping the experience passive and headset-safe.

Chosen format: monoscopic 360 with spatial/ambisonic audio, because environmental awareness matters more than stereo depth and the site has many near objects that would create stereo seam problems.

Capture plan:

- Shoot from locked-off tripod positions at decision points: entry gate, scaffold base, electrical room, and roof edge.
- Do not walk the camera through the site; cut between stable positions.
- Place important hazards in the forward 120 degrees at the start of each scene, then let viewers explore.
- Record ambisonic bed plus safety narrator separately.
- Clear or blur sensitive signage, access codes, license plates, and unrelated workers without releases.

Direction:

- Begin each scene with a head-locked prompt, then use a directional sound cue from the hazard area.
- Keep each shot long enough for the viewer to inspect.
- Use simple world-locked callouts only after the viewer has had a moment to orient.

Post:

- Level horizon and set default yaw to the main hazard.
- Patch tripod/nadir with a simple floor mark, not a fake texture that could imply safe footing.
- Use captions and a transcript; include a non-headset flat training version.
- Export YouTube-compatible 360 test with FOA plus head-locked narration if platform allows.

QA:

- Confirm no one needs to physically walk while wearing the headset.
- Check that recentering does not hide essential text.
- Confirm all sensitive details are removed throughout the sphere, including reflections.

Likely failure modes:

- Viewers miss hazards behind them.
- Metadata opens the file as flat video.
- Ambisonic bed orientation is rotated 90 degrees from picture.
- Blurred access codes remain readable in headset.

Meaningful variations:

- For a supervised installation, add a facilitator script and shorter loops.
- For public release, replace site footage with a staged mock environment to reduce privacy and security risk.

## Complete Example: Spatial Family Archive To Vision Pro

Example, not a required formula.

Production intent: preserve a family celebration as an intimate spatial video for Apple Vision Pro viewing, plus a standard 2D copy for relatives.

Chosen format: platform-native spatial video, because emotional scale and depth in a forward-facing memory matter more than full spherical exploration.

Capture plan:

- Use native spatial capture on a supported camera/phone path.
- Keep people at comfortable conversational distance and avoid fast pans across the room.
- Ask consent from attendees; mark private rooms and children-only areas as no-shoot zones.
- Record a clean stereo/mono backup audio source if the environment is noisy.

Post:

- Preserve original spatial metadata through import, edit, and export.
- Avoid aggressive reframing or stabilization that breaks stereo geometry.
- Add a separate captioned 2D edit if caption support in the target spatial playback path is uncertain.
- Export archival original, edited spatial master, and standard flat share copy.

QA:

- Test in the exact Apple playback path intended for the family.
- Confirm the video still presents as spatial, not flat.
- Check that no private addresses, documents, or bystanders are visible.

Likely failure modes:

- Editing software exports a flat 2D file.
- Stereo is uncomfortable because of fast camera movement.
- Captions or overlays become distracting in spatial playback.
- Relatives without compatible devices cannot view the primary version, so the flat fallback matters.

Meaningful variations:

- If long-term preservation is more important than edit polish, keep the original capture untouched and make derivative edits only from copies.
- If public sharing is requested, treat it as a separate rights-cleared edit, not the family archive master.
