---
name: precise-video-description
description: Provider-independent production guidance for converting observed video into precise, objective, temporally ordered language. Use for shot descriptions, searchable metadata, dataset captions, reference logs, generation-prompt handoffs, and analysis across subject, scene, motion, spatial, and camera aspects; not for deciding what to shoot, accessibility captions, creative interpretation, or provider-specific video analysis APIs.
---

# Precise video description

Use this skill when an existing video must be represented faithfully in production language. The output should let another agent or reviewer reconstruct what is visibly present, where it is, how it changes, and how the camera records it without inventing intent or atmosphere.

This skill describes observed media. It does not direct a future shot, infer a filmmaker's psychology, write accessibility captions, or execute a provider API.

## Evidence stance

- **Observed fact:** directly visible in reviewed frames or playback.
- **Measured fact:** derived from file metadata or a reproducible tool, with method and tolerance.
- **Inference:** plausible but not visually established; label it or omit it.
- **Production heuristic:** a practical description rule, not a claim about the source.

The five-aspect structure below is informed by Lin et al.'s CHAI video-language specification and professional cinematography practice. Sources were checked **2026-07-14**. CHAI's complete CameraBench-Pro primitive catalog was not fully available under a stable public package during authoring; do not reconstruct or copy an unavailable taxonomy from screenshots.

## Define the description contract

Before watching in detail, record:

- asset ID, path/URL, checksum, rights basis, source, and analysis date;
- duration, dimensions, aspect, frame rate/timebase, audio presence, and shot boundaries;
- intended use: log, search, reference analysis, dataset, prompt handoff, edit notes, VFX handoff, or review;
- required detail and temporal precision;
- approved terminology/glossary and domain-specific definitions;
- whether overlays, subtitles, graphics, edits, and audio are in scope;
- uncertainty policy and reviewer/approval requirements;
- privacy, likeness, confidential-data, and publication restrictions.

Description depth depends on use. A search index may need concise shot-level fields; a training dataset or VFX handoff may need time-bounded state changes. Length is never a substitute for accuracy.

## Describe five distinct aspects

CHAI organizes precise video language into five aspects. Use them as coverage lanes, not a mandatory paragraph order.

### Subject

Describe visible people, animals, objects, and graphics:

- type and stable distinguishing attributes;
- appearance, clothing, material, color, pose, and orientation;
- count and relationships among subjects;
- entry, exit, occlusion, reveal, and identity continuity;
- body/character side only when distinguishable from frame side.

Do not infer identity, age, gender, ethnicity, diagnosis, emotion, occupation, or relationship beyond visible evidence or supplied metadata. Prefer “the person in the yellow coat” over ambiguous numbering or pronouns.

### Scene

Describe environment and presentation context:

- setting, interior/exterior, visible geography, surfaces, weather, and time-of-day evidence;
- point-of-view structure when observable;
- overlays, borders, subtitles, interfaces, split screens, and transitions;
- changes in setting, light, weather, or visible context.

Separate composited overlays from physical scene objects. Avoid mood statements such as “inspiring” unless quoting approved creative direction rather than describing pixels.

### Motion

Describe observable subject/object activity in temporal order:

- action verb, actor, target, direction, start/end state, and contact;
- interactions and cause/consequence visible in the clip;
- simultaneous versus sequential actions;
- group activity and relative motion;
- uncertainty when low frame rate, blur, cuts, or occlusion prevent discrimination.

Choose the most specific supported verb. Do not upgrade walking to running, reaching to taking, or correlation to causation without visible evidence.

### Spatial

Describe composition and relationships in the image:

- shot size and how much of the subject is visible;
- frame-left/right/center, top/bottom, foreground/midground/background;
- overlap, occlusion, relative depth, scale, and movement through frame;
- start and end framing when it changes;
- subject-relative versus frame-relative direction.

Always name the reference frame when ambiguity matters: “moves toward frame-right,” “raises the subject's left hand,” or “passes behind the foreground post.” For camera-facing subjects, subject-left and frame-right may correspond; never collapse them.

### Camera

Describe observable capture behavior:

- height, angle, roll, and viewpoint;
- field-of-view/lens characteristics only to the confidence supported by evidence;
- focus plane, depth of field, and focus shifts;
- steadiness and camera movement geometry;
- playback-speed effects and shot transitions when included in the contract.

Distinguish translation from rotation and focal-length change:

- pan/tilt/roll rotate the camera;
- dolly/truck/pedestal/crane translate it;
- zoom changes focal length/angle of view without camera translation;
- rack focus changes the focus plane;
- an arc/orbit changes camera position around a subject.

Do not assert an exact focal length from appearance alone unless metadata or calibrated analysis supports it. Use “wide field of view with visible edge distortion” rather than fabricated millimeters.

## Observe before composing prose

Use a multi-pass review:

1. **Boundary pass:** identify cuts, transitions, speed changes, and major state changes.
2. **Subject/scene pass:** establish stable entities and environment.
3. **Motion/spatial pass:** track actions, reference frames, occlusions, and temporal order.
4. **Camera pass:** separate subject motion from camera motion, focus, framing, and playback effects.
5. **Contradiction pass:** compare start/middle/end and recheck ambiguous claims frame by frame.
6. **Prose pass:** assemble coherent language only after evidence notes exist.

For difficult clips, view at normal speed, slower playback, and isolated representative frames. Preserve the original playback interpretation; slow review is an inspection method, not evidence that source motion is slow.

## Represent time and change

Use intervals and state transitions rather than a bag of terms.

```yaml
shot_id: shot-014
start: 00:00:12.400
end: 00:00:17.800
subject:
  start: person in yellow coat, profile, frame-left
  change: turns toward camera and lifts a parcel
scene: rain-covered street; red sign in midground
motion: walks left-to-right, stops, then raises parcel
spatial:
  start: full shot, subject frame-left, sign frame-right
  end: medium shot, subject centered, sign partly occluded
camera: smooth lateral track, then short hold; no observable zoom
uncertainty: exact focal length not established
```

This is an example schema, not a required format.

Record both start and end states for properties that change: shot size, angle, focus plane, subject count, spatial depth, camera movement, or overlays. Keep edit transitions separate from continuous camera movement.

Use source timecode or exact frame numbers when required. State rounding and time-origin policy. Do not imply frame accuracy from rounded decimal seconds.

## Build and govern a project glossary

Create definitions only for terms the project needs. Each entry should have:

- preferred term and plain-language definition;
- inclusion/exclusion rules;
- confusing neighbors and decision rule;
- one rights-cleared positive example and, where useful, a counterexample;
- source and verification date;
- owner and version.

High-risk confusions include dolly versus zoom, pan versus lateral translation, high angle versus high camera height, full shot versus close-up, bird's-eye versus broadly elevated view, shallow focus versus blur from motion, and object motion versus camera tracking.

If reviewers cannot distinguish a term reliably, use more literal geometry until the glossary is improved.

## Objectivity, uncertainty, and omissions

Exclude:

- emotional interpretation, theme, symbolism, quality judgments, or presumed intent unless the task explicitly asks for a separate inference lane;
- invisible causes, offscreen events, and identity claims not supplied by authorized metadata;
- audio claims when audio was not reviewed;
- exact technical settings inferred only from style.

Use uncertainty that says what cannot be resolved and why:

```text
The framing tightens, but the shot does not provide enough parallax or metadata to distinguish a slow dolly-in from a zoom-in.
```

Do not use “possibly” to decorate every sentence. If uncertainty is immaterial to the use case, choose a literal observable description such as “the subject becomes larger in frame.”

## Convert labels into coherent language

Primitive labels are evidence, not a finished description. Compose prose that:

- identifies entities before pronouns;
- follows temporal order;
- connects simultaneous actions clearly;
- states reference frames;
- avoids redundant repetition across aspects;
- retains key omissions/uncertainties;
- does not add subjective connective language.

For downstream generation prompts, keep an explicit distinction between **observed source description** and **desired future direction**. A description says what happened; a prompt may request what should happen.

## Rights, privacy, and data custody

Detailed descriptions can expose faces, locations, screens, health/financial information, badges, license plates, private actions, or copyrighted story content even when video files are not redistributed.

- minimize personally identifying and confidential details to the use case;
- use stable pseudonymous subject labels where appropriate;
- preserve rights/consent restrictions with the description;
- do not publish detailed plot/action descriptions when licensing permits analysis only;
- record model/human author, source asset/version, glossary version, review status, and transformations;
- treat descriptions used for training as dataset assets requiring provenance, license, consent, and limitation documentation.

CHAI's public test artifacts and model have their own licenses/cards; the paper's arXiv distribution license does not grant unrestricted reuse of every underlying professional video or unreleased primitive example.

## Quality checklist

- All five required aspects were considered; intentionally omitted lanes are documented.
- Subjects are stable and unambiguous.
- Events appear in source order and simultaneity is preserved.
- Frame-relative and subject-relative directions are not confused.
- Camera translation, rotation, zoom, focus, and subject motion are distinguished.
- Start/end states are captured for changing properties.
- No hallucinated object, action, intent, technical setting, or emotion appears.
- Terminology follows the approved glossary.
- Uncertainty is specific and evidence-based.
- Description depth matches its use.
- Rights, privacy, provenance, and review metadata travel with the output.

## Example 1: single cinematic shot

This is a complete example, not a mandatory formula.

**Intent:** create a production-search description for a six-second dialogue shot.

**Observed video:** A woman in a dark jacket stands at a kitchen counter. A man remains soft in the doorway. She raises her eyes toward him while the frame gradually tightens.

**Structured result:**

- Subject: woman in dark jacket at counter; man in doorway, partly visible and out of focus.
- Scene: dim kitchen interior at blue hour; warm pendant visible in background.
- Motion: woman lifts her gaze toward the man and speaks; man remains still.
- Spatial: starts medium with woman left of center and man at frame-right edge; ends shoulders-and-head on woman while the man remains soft at edge.
- Camera: smooth forward translation on the woman with no visible pan or tilt; shallow focus remains on her near eye. Exact focal length is not established.

**Coherent description:** “In a dim kitchen, a woman in a dark jacket stands left of center at the counter while a man remains out of focus at the frame-right doorway. She raises her eyes toward him and speaks. During the eye movement, the camera moves smoothly forward from a medium view to a shoulders-and-head framing, keeping focus on her near eye; the man stays soft at the edge.”

**Likely failure:** calling the move a zoom because the subject grows in frame. Repair by checking parallax/background change and using literal tightening language if unresolved.

## Example 2: generated game clip with ambiguous motion

This is a complete example, not a mandatory formula.

**Intent:** produce dataset metadata for a five-second side-view game clip.

**Observed video:** A small armored character travels toward frame-right while platforms move frame-left. The framing stays side-on. A score overlay remains at top-left. The clip contains one hard cut near the end.

**Description:** “A small armored character runs toward frame-right across elevated platforms in a side-view game scene. The character remains near the left third while the platforms move toward frame-left, consistent with a camera that tracks the character laterally; exact world-versus-camera displacement cannot be recovered from the rendered view alone. A numeric score overlay stays fixed at the top-left. Near the end, a hard cut changes to a closer side-on view of the same character.”

**Why this works:** it distinguishes screen motion from uncertain world motion, identifies the overlay as graphics, and separates the edit from camera movement.

**Likely failure:** claiming the character's world speed or lens from rendered pixels. Keep those fields unknown unless game telemetry or metadata is supplied.

## Sources

Verified 2026-07-14:

- Lin et al., “Building a Precise Video Language with Human-AI Oversight,” CVPR 2026 / arXiv:2604.21718: https://arxiv.org/abs/2604.21718
- Official CHAI project and code: https://linzhiqiu.github.io/papers/chai/ and https://github.com/chancharikmitra/CHAI
- CameraBench, camera-motion taxonomy and expert annotation: https://linzhiqiu.github.io/papers/camerabench/
- ASC camera movement and shot craft: https://theasc.com/articles/shot-craft-camera-movement and https://theasc.com/articles/shot-craft-fresh-perspectives
- Columbia Film Language Glossary: https://filmglossary.ccnmtl.columbia.edu/
- W3C media accessibility requirements, used to distinguish production description from accessibility deliverables: https://www.w3.org/TR/media-accessibility-reqs/
- Gebru et al., Datasheets for Datasets: https://doi.org/10.1145/3458723