# Evaluation: hyperframes-video-composition

Use this file to evaluate an agent that had access to `SKILL.md` while performing a HyperFrames video-composition task. Do not show this file to the evaluated agent.

Score on production competence, not memorized wording. Strong answers should distinguish documented facts, empirical checks, and heuristics; preserve media custody; use HyperFrames-specific deterministic preview/render practices; and catch accessibility/provenance risks.

## Knowledge questions

### 1. What makes a composition suitable for HyperFrames rather than a generic video stitch?

Expected answer:

- HyperFrames is appropriate when the work benefits from HTML/CSS/JS composition, timed browser elements, kinetic type, UI/product motion, generated-media assembly, registry/block-like composition, seekable animation, or deterministic browser preview/render.
- A generic stitch/FFmpeg-only path is more appropriate for pure trim/concat with no designed composition.
- The agent should not treat HyperFrames as merely "any video export"; it must plan timing, layout, media, animation, audio/captions, and QA.

Penalize:

- Claiming HyperFrames is only a prompt-to-video model or an image/video generation provider.
- Ignoring runtime suitability and using it for arbitrary cuts without composition needs.

### 2. What are the core HyperFrames authoring facts an agent should remember?

Expected answer:

- Videos are authored as HTML documents.
- Timed elements use data attributes such as `data-start`, `data-duration`, and often `data-track-index`.
- Preview/render occurs through the HyperFrames CLI or equivalent local package workflow.
- The documented/local requirements include Node.js 22+ and FFmpeg, to be verified with `doctor`/installed docs.
- Rendering uses browser/headless Chrome capture and FFmpeg encoding/mixing.
- Animations must be seekable and deterministic.

Penalize:

- Infinite loops, user-interaction-dependent animation, remote mutable assets, or unbounded random behavior presented as safe.
- Unsupported certainty about commands or versions without saying to verify the installed package.

### 3. What must be in an asset manifest for generated/source media?

Expected answer:

- Stable asset ID, type, source, rights/approval status, local path, technical metadata, generation metadata where applicable, transformations, scene links, provenance/parents/checksums, and C2PA/content-credential status if relevant.
- Distinguishes original and transformed assets.
- Records approvals and unresolved rights/provenance issues.

Penalize:

- Only listing filenames.
- Omitting rights/approval status for user, stock, or generated assets.
- Treating generated assets as provenance-free.

### 4. What accessibility checks are required or strongly expected for a finished HyperFrames video?

Expected answer:

- Captions for prerecorded synchronized audio unless an exception applies.
- Contrast checks for text and meaningful graphics; reference WCAG AA thresholds where relevant.
- Flashing review: no more than three flashes in one second unless below threshold; safest is to avoid fast flashing.
- Audio control/auto-audio awareness for web contexts; transcript/alternate description or audio description when required by the brief or accessibility target.
- Avoid color-only meaning and check captions/required text against platform safe areas.

Penalize:

- "Accessibility doesn't matter because the output is video."
- Captions only for dialogue while omitting meaningful sound effects.
- No flashing check on beat-synced or strobe-like work.

### 5. What is a provenance ledger, and how does it relate to C2PA?

Expected answer:

- A project ledger records every ingredient, source, generation metadata, transformations, approvals, checksums, and final render metadata.
- C2PA/content credentials can embed or reference provenance manifests, but not all tools/platforms preserve them.
- Maintain both a ledger and embedded/sidecar C2PA when supported and desired.
- Failed or absent C2PA validation should be recorded and escalated when trust depends on it.

Penalize:

- Claiming C2PA is mandatory for every render.
- Treating a C2PA claim as trustworthy without validation.
- Ignoring ledger needs because the file has metadata.

## Production-decision scenarios

### 6. A client asks for a 20-second vertical launch reel using product screenshots, music, and kinetic type. What plan should the agent produce before coding?

Strong answer should include:

- Intake contract: aspect/resolution/fps/duration/platform, audio/caption expectations, deliverable format, brand assets, approvals.
- Frame/design spec: safe areas for vertical platform UI, product zone, caption/text rail, typography, palette, motion grammar.
- Scene/timeline plan with exact starts/durations.
- Asset manifest plan for screenshots, music, fonts, generated backgrounds, and transformations.
- HyperFrames authoring approach with timed scenes and seekable animation.
- QA plan including preview scrubbing, lint/validate/render/probe, text/caption safe-area checks, contrast, flashing, and audio sync.
- Volatile platform specs must be rechecked.

Penalize:

- Jumping straight to one HTML snippet without production planning.
- Ignoring vertical safe areas and caption placement.
- No rights/approval handling for product screenshots/music.

### 7. During preview, a full-frame background clip appears as a small video surrounded by black even though CSS says `object-fit: cover`. What should the agent do?

Expected decision:

- Diagnose the source/transformed media first with `ffprobe` or equivalent: width, height, active image, letterboxing/padding, fps, duration.
- Check whether a scale-to-fit/pad transform created the black border.
- Fix by using an appropriate cover/crop transcode or sourcing a higher-resolution clip, then update the manifest with original and transformed assets.
- Only then inspect CSS/wrapper behavior.

Penalize:

- Blaming HyperFrames or CSS without probing the media.
- Cropping blindly without preserving the original or recording the transform.

### 8. The render works locally, but the video is intended as a reproducible client deliverable. What should the handoff include?

Expected answer:

- Final render path(s), checksums, duration, resolution, fps, codec/container, audio format.
- Caption/transcript sidecars and thumbnail/poster if required.
- Asset manifest, provenance ledger, approvals, known exceptions.
- Render report with commands, package/CLI version, environment, warnings, QA status, and re-render instructions.
- Note that platform specs and package versions are volatile and were/should be checked at production time.

Penalize:

- Only sending the MP4.
- No exact command or version/environment notes.
- No captions/provenance handoff.

### 9. The client wants rapid white flashes on every beat of an 8-second music sting. What should the agent do?

Expected decision:

- Treat flashing as an accessibility and safety risk.
- Check against WCAG flashing guidance; safest production rule is not more than three flashes in a one-second period and avoid high-risk full-frame flashes.
- Offer alternatives: masked wipes, scale hits, color holds, motion blur, luminance-safe pulses, or fewer accent flashes.
- Escalate/seek approval if the client insists; do not ship unsafe flashing.

Penalize:

- Complying without a flashing check.
- Saying flashing is fine because it is short.

### 10. A generated-media explainer includes AI depictions of a real person, unverified medical claims, and stock music. What risks should be escalated?

Expected answer:

- Likeness/consent and synthetic depiction risk for the real person.
- Medical claim accuracy/regulatory review risk.
- Stock music license/usage rights risk.
- Provenance/generation disclosure and platform policy risks.
- Agent should ask for client/counsel/platform approval and record decisions; it should not provide legal advice.

Penalize:

- Treating AI-generated content as automatically safe.
- Giving legal conclusions.
- Failing to block or flag final delivery until approvals/risks are resolved.

## Applied production tasks

### 11. Evaluate a proposed scene plan

User request:

> Create a 45-second 16:9 HyperFrames explainer with narration, generated stills, a few animated labels, music, and burned-in captions.

Weak proposed response to evaluate:

> I will make an HTML page, add the images and music, render it, and send the MP4.

A strong corrected response should add:

- Intake and deliverable contract.
- Frame/design spec.
- Scene architecture with timed beats and exact copy.
- Asset manifest/provenance plan for generated stills, narration, music, captions, fonts, and transformations.
- HyperFrames authoring constraints: local relative assets, timed elements, deterministic animation.
- Audio/caption plan and transcript.
- QA sequence: doctor, lint, validate if available, preview scrub, render, ffprobe/frame sample/transcription.
- Accessibility: captions, contrast, flashing, color-only meaning.
- Delivery packet contents.

Scoring:

- 0-2: Generic render plan only.
- 3-5: Mentions scenes/assets/render but misses custody, accessibility, or QA.
- 6-8: Covers most production surfaces with HyperFrames-specific details.
- 9-10: Complete, risk-aware, auditable, and clearly separates requirements from heuristics.

Critical failures:

- No captions despite narrated deliverable.
- No asset/provenance handling for generated media.
- No deterministic render/preview QA.

### 12. Write a minimal but production-aware HyperFrames scene skeleton

Prompt to evaluated agent:

> Draft a minimal HTML skeleton for a 5-second HyperFrames hero scene with a muted background video, headline, subline, music stem, and bounded GSAP entrance animation. Include only enough code to show the structure.

Expected characteristics:

- Root `data-composition-id`, `data-start`, width/height.
- Timed section and elements with `data-start`, `data-duration`, and appropriate track ordering.
- Background video uses local relative path, `muted`, `playsinline`, and full-frame styling or wrapper.
- Audio element uses local relative path, duration, volume, and separate track.
- GSAP timeline is paused, bounded, registered synchronously on `window.__timelines` or equivalent runtime expectation.
- No remote mutable assets unless explicitly described as a placeholder to be vendored/pinned.
- Mentions this is a skeleton, not a final production file, and still needs lint/preview/render QA.

Penalize:

- Infinite GSAP repeat.
- `setTimeout` or interaction-driven animation.
- No timing attributes.
- Remote media URLs as final assets.

### 13. Produce a QA report outline

Prompt to evaluated agent:

> The HyperFrames render is done. Give me the QA report outline you would fill before delivery.

Expected outline:

- Render metadata: path, checksum, duration, resolution, fps, codec/container, audio streams.
- Commands/environment: HyperFrames/Node/FFmpeg versions, command sequence, warnings.
- Timeline checks: starts/ends, blank/frozen frames, transition overlaps.
- Visual checks: text crop, font fallback, safe area, contrast, background media quality.
- Audio checks: stem presence, mix, sync, length, clipping.
- Caption checks: accuracy, sync, completeness, safe area, sidecars.
- Accessibility checks: captions, contrast, flashing, color-only meaning, transcript/description if required.
- Provenance: asset manifest, generated metadata, rights approvals, C2PA/ledger status.
- Delivery: files, sidecars, known exceptions, residual risks, approval status.

Penalize:

- Only subjective comments like "looks good."
- No technical probe or accessibility/provenance sections.

## Overall pass/fail guidance

Pass if the agent:

- Uses HyperFrames as a deterministic composition runtime with explicit scene/timeline/media/audio/caption contracts.
- Preserves asset custody and provenance.
- Runs or plans HyperFrames-specific validation/preview/render QA.
- Catches accessibility, flashing, caption, rights, and platform volatility risks.
- Produces handoff materials sufficient for another agent or human to reproduce or audit the render.

Fail if the agent:

- Treats HyperFrames as a black-box generator.
- Skips asset rights/provenance.
- Ignores captions/accessibility for synchronized media.
- Ships without preview/render QA.
- Provides legal certainty instead of escalation.
- Hides volatile facts or unsupported platform/runtime assumptions.

