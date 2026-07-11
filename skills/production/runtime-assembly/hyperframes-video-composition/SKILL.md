---
name: hyperframes-video-composition
description: Provider-independent production workflow for AI agents assembling generated or source media into HyperFrames HTML/CSS/JS videos. Use for HyperFrames composition planning, scene architecture, media custody, animation/timing, captions/audio, deterministic preview/render QA, accessibility/flashing checks, provenance ledgers, and delivery handoff.
---

# HyperFrames video composition

Use this skill when the job is to assemble images, clips, narration, music, captions, UI captures, generated assets, or brand material into a finished HyperFrames video. Treat HyperFrames as a production composition runtime, not just a code target: the agent owns intake, the frame/design spec, media custody, timing, QA, provenance, and handoff.

This skill is provider-independent. It does not choose the image, video, TTS, or music model for you. It tells you how to turn approved assets and creative decisions into a deterministic HTML/CSS/JS/HyperFrames composition.

## Source status

Documented facts below are grounded in these sources, verified 2026-07-11 unless noted:

- HyperFrames official docs and repo: [Introduction](https://hyperframes.heygen.com/introduction), [Quickstart](https://hyperframes.heygen.com/quickstart), [Prompting guide](https://hyperframes.heygen.com/guides/prompting), [GitHub repository](https://github.com/heygen-com/hyperframes), plus local HyperFrames package READMEs for CLI, core, engine, and producer.
- Local OpenMontage HyperFrames bridge: `C:\Users\ishan\Documents\OpenMontage\skills\core\hyperframes.md`, `tools\video\hyperframes_compose.py`, and `lib\hyperframes_style_bridge.py`.
- WCAG 2.2 Quick Reference: captions, audio description, contrast, audio control, flashing, and non-text contrast: [W3C WCAG 2.2 Quickref](https://www.w3.org/WAI/WCAG22/quickref/).
- Browser media behavior: [MDN Autoplay guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay), [MDN `<video>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video), and [MDN `<audio>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/audio).
- Provenance terminology: [C2PA Technical Specification](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html) and [C2PA overview](https://c2pa.org/).

Volatile facts: HyperFrames CLI commands, package names, Node/FFmpeg requirements, registry block names, cloud render support, browser capture behavior, platform delivery specs, and social platform safe areas can change. Re-check the installed package docs, `npx hyperframes --help`, `npx hyperframes doctor`, and target-platform delivery docs at production time.

## Production stance

Separate three kinds of information in your own notes and client updates:

- Documented fact: behavior or requirement found in official/local docs or a standard.
- Empirical observation: something verified in this project by preview, render, ffprobe, frame sampling, transcription, or manual review.
- Production heuristic: a practical rule that improves output but is not a formal requirement.

Escalate rather than guess when the issue is rights, licensing, privacy, likeness, client brand approval, platform policy, medical/legal/financial claims, political persuasion, regulated ads, or unverified provenance. Do not provide legal advice; identify the risk and ask for client, counsel, platform, or rights-holder approval.

## 1. Intake: lock the composition contract

Before authoring HTML, produce a short composition brief with these fields:

- Intent: what the video must make the viewer understand, feel, or do.
- Audience and context: where and how it will be watched.
- Deliverables: aspect ratio, resolution, duration, fps, audio/no-audio, caption requirement, transparent overlay requirement, and required file formats.
- Runtime: HyperFrames, with a note that it is appropriate because the piece benefits from HTML/CSS/JS composition, seekable browser animation, kinetic type, UI motion, generated media assembly, or registry/block-style composition.
- Inputs: approved assets, generated assets to create, brand materials, script, source footage, captions, audio stems, fonts, data, references, and rights constraints.
- Review gates: script/beat plan, design frame, rough preview, audio/caption pass, final render.
- Non-negotiables: brand rules, disclaimers, accessibility targets, platform rules, client approvals, and forbidden treatments.

If the request is still ambiguous, ask only for choices that materially change the result: target duration, aspect ratio/platform, narration vs. text-led, brand/style references, and whether source assets are approved for use.

## 2. Design the frame before the timeline

HyperFrames compositions are browser frames captured into video. Design for a camera, not a scrolling page.

Create a frame/design spec before coding:

- Canvas: width, height, fps, aspect ratio, safe regions, and bleed policy.
- Visual system: background, foreground, accent palette, typefaces, type scale, corner radii, stroke weights, shadows, texture/grain, and motion intensity.
- Layout grammar: grid, margins, title zones, lower-thirds, caption rail, logo zone, product/device zone, and chart/data zone.
- Scene density: maximum words on screen, maximum simultaneous claims, minimum hold time for reading, and hierarchy rules.
- Motion grammar: entrance, emphasis, transition, exit, camera/parallax, and reduced-motion alternative when relevant.
- Audio grammar: narration role, music role, sound-effect restraint, silence beats, stem names, and target loudness policy if one is specified by the client.
- Accessibility targets: captions for spoken audio, contrast targets, no unsafe flashing, no critical information conveyed by color alone, and transcript or alternate description when required.

For platform deliverables, reserve safe areas for UI overlays and captions. Treat platform safe-area dimensions as volatile; re-check the target platform's current creator/ad specs before final crop and delivery.

## 3. Scene architecture

Plan the piece as timed scenes and layers. A useful scene plan includes:

- `scene_id`: stable kebab-case identifier.
- `start`, `duration`, `end`: seconds, with frame-derived values checked against fps.
- `purpose`: hook, setup, proof, demo, transition, CTA, disclaimer, etc.
- `visual`: what appears and why.
- `text`: exact on-screen copy, not placeholders.
- `media`: asset IDs and how they are used.
- `audio`: narration segment, music cue, SFX, silence, or stem ducking.
- `animation`: entrance, emphasis, transition, exit, and key beats.
- `accessibility`: caption text, contrast risk, flashing risk, and description need.
- `qa`: what to check in preview/render for this scene.

Prefer a small number of strong scenes over many thin cuts. For social or launch work, build the first 1-2 seconds as a true hook; do not spend the opening on a logo unless the brief requires it.

## 4. HyperFrames authoring contract

Documented HyperFrames facts:

- HyperFrames defines video as HTML. Elements use timing attributes such as `data-start` and `data-duration`; layout/timeline ordering can use `data-track-index`.
- The current quickstart states that timed elements need `class="clip"` along with `data-start`, `data-duration`, and `data-track-index`; keep the class on timed visual elements unless the installed CLI/project docs say otherwise.
- HyperFrames supports preview in the browser with `npx hyperframes preview` and rendering to MP4 with `npx hyperframes render`.
- The local/official docs describe Node.js 22+ and FFmpeg as requirements; verify with `npx hyperframes doctor`.
- The core package includes parsers, generators, timing compilation, linting, runtime support, and frame adapters for seekable animation runtimes.
- The engine/producer render path uses headless Chrome plus FFmpeg to capture frames, encode video, and mix audio.

Authoring rules:

- Keep a single root composition with a clear `data-composition-id`, explicit canvas size, and deterministic initial state.
- Use absolute positioning or a strict grid inside the fixed video canvas; avoid page-flow surprises that depend on viewport defaults.
- Give every timed visual element a stable ID or class, a start, a duration, and a track index when layering matters.
- Stage media with relative paths inside the project workspace; never reference temp files, external URLs that may change, or another runtime's public folder.
- Register animation timelines synchronously after page load. Do not depend on unbounded timers, network races, or user interaction.
- Bound all loops. Infinite GSAP repeats, wall-clock-only animations, random values without stored seeds, and async timeline construction break deterministic capture.
- Pin external script versions or vendor local copies when the final render must be reproducible.

Example root shape:

```html
<main id="stage" data-composition-id="launch-hero" data-start="0" data-width="1920" data-height="1080">
  <section class="scene scene-01 clip" data-start="0" data-duration="5" data-track-index="0">
    <video class="bg clip" data-start="0" data-duration="5" data-track-index="0" src="./assets/hero-loop.mp4" muted playsinline></video>
    <h1 id="headline" class="clip" data-start="0.4" data-duration="3.8" data-track-index="2">Ship the impossible demo</h1>
    <p id="subline" class="clip" data-start="1.2" data-duration="3" data-track-index="2">A launch reel assembled from approved product captures.</p>
  </section>

  <audio data-start="0" data-duration="5" data-track-index="10" data-volume="0.45" src="./assets/music-bed.wav"></audio>

  <script src="./vendor/gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from("#headline", { opacity: 0, y: 48, duration: 0.55, ease: "power3.out" }, 0.4);
    tl.from("#subline", { opacity: 0, y: 24, duration: 0.45, ease: "power2.out" }, 1.2);
    window.__timelines = window.__timelines || {};
    window.__timelines["launch-hero"] = tl;
  </script>
</main>
```

Use this as an example of structure, not a mandatory template.

## 5. Media import and custody

Every asset that enters the composition needs an asset record before it is referenced by HTML.

Minimum asset manifest fields:

- `asset_id`: stable ID used by scene plan and HTML comments or metadata.
- `type`: image, video, audio, music, narration, SFX, font, data, logo, caption, LUT, transcript, etc.
- `source`: user-provided, generated, licensed stock, public-domain, first-party capture, synthetic, or derived.
- `path`: workspace-relative and absolute local path.
- `rights_status`: approved, pending approval, restricted, unknown, or generated-under-policy.
- `generation_metadata`: provider/model/version/prompt/seed/settings when generated.
- `transformations`: trims, crops, resizes, color conversions, denoise, upscales, transcodes, normalization, background removal.
- `technical`: width, height, fps, duration, codec, sample rate, channel count, alpha, color space if known.
- `scene_links`: scene IDs where used.
- `provenance`: parent assets, checksums, C2PA/content-credential status if available, and ledger row.

Empirical production checks:

- Run `ffprobe` or equivalent on every video/audio asset before staging.
- For full-frame background video, check active source resolution before blaming CSS. Upscaling a letterboxed low-res source into a 1920x1080 container can still leave visible black padding inside the picture.
- Re-encode heavy stock/source clips to render-friendly H.264, constant fps, short keyframe interval, and `faststart` when browser capture stalls or freezes. Keep the original and transformed paths in the manifest.
- Avoid remote media URLs in final HTML. Download or freeze files locally so render and audit do not depend on an external server.
- Use relative paths from the HyperFrames project root.

## 6. Timeline, duration, aspect, and fps

Treat time as an audited contract:

- Decide the master fps before animation. Use 24/30/60 only when the toolchain and delivery need support them; verify current producer/CLI support at production time.
- Convert all scene starts and durations to frame boundaries: `frame = round(seconds * fps)`. Watch for cumulative drift when using decimals.
- Keep a timeline table with scene start, end, audio segment, caption segment, and transition overlap.
- Do not let CSS transition durations silently exceed the scene duration.
- If using transitions that overlap scenes, represent overlap explicitly in the plan and HTML rather than hiding it in animation code.
- For multiple aspect ratios, create separate layout specs. Do not rely on a blind center-crop from 16:9 to 9:16 unless the brief explicitly allows it.

Safe production heuristic: leave at least 5-10% of frame width/height as action-safe margin for important text and logos unless target-platform specs require a larger safe area. For vertical social, reserve extra space for captions and platform UI overlays after checking current platform specs.

## 7. Animation and transitions

HyperFrames rewards seekable, frame-deterministic animation.

Use animation to clarify hierarchy:

- Entrance: establish what matters now.
- Emphasis: point at the active idea, number, product feature, or evidence.
- Transition: carry the viewer from one beat to the next.
- Exit: clear the canvas; do not leave visual debris.

Good motion patterns:

- Kinetic type: word/line reveals, masked wipes, scale/perspective hits, and timed emphasis.
- Product/UI motion: cursor paths, focus rings, device pans, progressive disclosure, and callout lines.
- Data motion: axis first, mark reveal second, annotation third, takeaway last.
- Atmospheric motion: grain, light sweep, parallax, or particles at low intensity, bounded and not distracting.

Avoid:

- Random motion without a stored seed.
- Flash cuts, strobes, or high-contrast inversion without a flashing review.
- Motion that causes text to be unreadable while it is supposed to be read.
- Infinite loops or wall-clock-only timelines.
- Decorative animation that competes with narration or captions.

For transitions, choose the semantic type:

- Hard cut: urgency, comedy, list pacing.
- Match cut: same object, shape, UI element, or phrase bridges scenes.
- Wipe/mask: product reveal, data reveal, page-to-page movement.
- Crossfade: memory, softness, recap.
- White/black flash: only when flash-safe and narratively justified.

## 8. Typography, layout, and captions

Text is often the main visual asset in HyperFrames.

Typography rules:

- Prefer live text over rasterized text except for logos or required brand artwork.
- Set max line length and intentional line breaks; do not let browser wrapping decide the hero line.
- Use real hierarchy: title, claim, evidence, caption, label, disclaimer.
- Keep captions visually distinct from marketing copy.
- Avoid putting critical text at the extreme edges.
- Test every text state on actual background frames, not just a clean design frame.

Accessibility and legibility facts from WCAG 2.2:

- Prerecorded synchronized media with audio needs captions unless it is clearly a media alternative for text.
- WCAG AA minimum contrast for normal text is 4.5:1; large text has a 3:1 threshold.
- Non-text visual information and UI component boundaries require sufficient contrast; use at least 3:1 as the WCAG AA reference point where applicable.
- Content should not flash more than three times in any one-second period unless it is below the general/red flash thresholds. The safest production rule is no flashing beyond three flashes per second.

Caption production:

- Decide open captions, closed caption sidecar, or both based on delivery. Burned/open captions are safer for social feeds; sidecars are better for accessible players and localization.
- Captions must include dialogue and important non-speech audio when that audio conveys meaning.
- Keep captions synchronized to speech, readable, and clear of platform overlays.
- If using word-level captions, verify timing after render by watching, not just by trusting transcript timestamps.
- Keep a canonical transcript/subtitle file in the asset ledger even when captions are burned into video.

## 9. Audio, stems, and synchronization

Build audio as stems, not as one mystery file:

- Narration/dialogue stem.
- Music stem.
- SFX stem.
- Ambience stem if used.
- Final mix.

For each stem, record source, rights, duration, loudness/normalization if measured, sample rate, and scene links. If narration is generated, store script text, voice/provider/model/version/settings, and approval status.

Browser/media facts:

- HTML `<audio>` embeds sound content; HTML `<video>` embeds a media player for video playback.
- Browser autoplay rules restrict audible autoplay. Muted video or video with no audio track is treated differently from audible autoplay. HyperFrames render tooling drives media for capture, but the composition should still use sane browser media attributes such as `muted` and `playsinline` for background videos.

Production heuristics:

- Mix speech first; music supports, never masks, narration unless the piece is intentionally music-led.
- Duck music under narration and restore during visual-only beats.
- Use SFX sparingly for semantic events: click, reveal, transition, impact, notification.
- Verify final audio length matches video duration and no stem starts before/after its intended scene.
- After render, transcribe or spot-check narration against the approved script and caption file.

## 10. Deterministic preview, validation, and render

Run the HyperFrames loop as a gate sequence:

1. `npx hyperframes doctor` to verify environment when starting or when render behavior changes.
2. `npx hyperframes lint` for static composition findings.
3. `npx hyperframes validate` when available in the installed CLI or project workflow; do not rely on render alone for browser-state issues.
4. `npx hyperframes preview` and scrub representative frames: first frame, scene boundaries, dense text, data/chart moment, caption-heavy moment, background-video scenes, CTA/disclaimer, and final frame.
5. Render only after lint/validation and preview checks pass or documented exceptions are approved.
6. Post-render probe: duration, resolution, fps, codec/container, audio streams, frame samples, black/frozen frames, clipped text, caption sync, and audible mix.

If the installed CLI differs from these command names, re-check `npx hyperframes --help` and use the equivalent commands. Record the exact command, package version, and environment in the render report.

For video-heavy compositions, reduce parallelism/workers if headless Chrome or media decode stalls. Treat this as an empirical fix: record what failed, what changed, and the before/after result.

## 11. Browser/render QA checklist

Before final delivery, review:

- Timeline: total duration, scene boundaries, transition overlaps, no unexpected blank frames.
- Canvas: correct aspect, resolution, fps, pixel-safe text, no crop surprises.
- Media: every asset appears at intended quality, no missing files, no remote dependency, no unintended letterboxing, no frozen frames.
- Typography: readable on real backgrounds, correct font fallback, no orphaned words, no clipped descenders, disclaimers legible.
- Captions: accurate, synchronized, complete, safe-area compliant, no conflict with other text.
- Audio: no clipped speech, no missing stem, music ducked, SFX not distracting, final length matches picture.
- Accessibility: contrast pass or documented exception, flashing pass, no color-only meaning, transcript/captions included as required.
- Provenance: manifest complete, generated assets labeled, user-provided assets approved, source/transform chain preserved.
- Delivery: correct filename, format, codec, aspect, thumbnail/poster frame, sidecars, and handoff notes.

Classify findings:

- Critical: rights/consent unknown; unsafe flashing; missing captions when required; runtime swap without approval; render mismatch with approved spec; broken/missing media; unreadable required text; false or unapproved claims.
- Major: caption timing drift; weak contrast; audio mix masks speech; visible layout/crop issue; unsupported platform format; incomplete provenance fields.
- Minor: slight easing polish, minor texture, non-essential frame aesthetics.

Do not ship with critical findings. Ship with major findings only if the client explicitly accepts the tradeoff.

## 12. Provenance ledger and content credentials

C2PA defines Content Credentials/C2PA manifests as provenance data that can bind assertions, claims, signatures, and ingredients to an asset. Not every workflow or platform preserves embedded credentials, so maintain both:

- A machine/human-readable project provenance ledger.
- Embedded or sidecar C2PA/content-credential data when the toolchain supports it and the client wants it.

Minimum ledger rows:

- final render ID and checksum.
- ingredient asset ID, source, rights status, and checksum.
- generation metadata for AI-created assets.
- transformation steps and tools.
- approvals and dates.
- C2PA/content-credential status: present, validated, absent, stripped by transform, unsupported, or not checked.

If a source asset claims provenance but validation fails, do not silently treat it as authenticated. Mark the validation failure and escalate if the claim affects trust, newsworthiness, compliance, or client approval.

## 13. Delivery handoff

Provide a delivery packet, not just an MP4:

- Final render path(s), checksums, duration, resolution, fps, codec/container, audio format.
- Captions/subtitles/transcript sidecars if required.
- Thumbnail/poster frame if requested.
- Asset manifest and provenance ledger.
- Render report with commands, HyperFrames/package version, environment, warnings, and QA status.
- Known limitations, approved exceptions, and residual risks.
- Re-render instructions: exact source workspace, command sequence, package/version notes, and required local assets.

For platform uploads, re-check current target specs just before export: aspect, max duration, file size, codec, audio requirements, caption sidecars, safe areas, disclosure labels, and ad policy. Treat these as volatile facts.

## 14. Example: narrated product launch reel

Example intent: create a 30-second 16:9 launch reel from approved product captures, generated abstract backgrounds, narration, music, and open captions.

Approach:

1. Intake locks 1920x1080, 30 fps, 30 seconds, MP4, open captions, approved product screenshots, brand colors, no unapproved customer logos.
2. Frame spec defines a product/device zone on the right, kinetic headline zone on the left, caption rail at the bottom, and a CTA safe from platform overlays.
3. Scene plan:
   - 0-3s: hook/title with abstract motion background.
   - 3-10s: product problem with one UI capture and callout.
   - 10-18s: feature proof with three fast UI beats.
   - 18-25s: outcome/customer-safe metric, if approved.
   - 25-30s: CTA and logo.
4. Asset manifest stores screenshots, generated background loops, narration stem, music stem, caption file, font files, checksums, and approvals.
5. HTML uses timed sections, relative asset paths, bounded GSAP timelines, muted `playsinline` background video, and separate caption elements.
6. QA gates run doctor/lint/validate/preview/render/probe and specifically check UI legibility, caption rail, no customer-logo leaks, and safe flashing.

Expected failure modes:

- Captions fight with headline copy: lower headline density or move captions to a fixed rail.
- Background video makes text fail contrast: add a local scrim behind text instead of globally dimming everything.
- Product screenshots are too small: reduce simultaneous UI panels and use animated zooms/callouts.
- Narration drifts: retime scene starts to the approved narration stem instead of stretching speech.

## 15. Example: music-led kinetic typography sting

Example intent: create an 8-second square or vertical social sting with no narration, synced to an approved music hit.

Approach:

1. Analyze the music stem for beat accents or manually mark beat times.
2. Build a sparse frame spec: large type, one accent color, strong negative space, and no small text.
3. Use the timeline as the script: each text reveal lands on a beat; transitions are short and bounded.
4. Use captions only if there are vocals or meaningful spoken words; otherwise include a short title/description sidecar for accessibility where required by the destination.
5. Run a flashing check because beat-synced cuts can accidentally exceed safe flash thresholds.

Expected failure modes:

- Too many words for 8 seconds: cut copy until each beat is readable.
- Flashy inversions are unsafe: use motion, scale, masks, or color holds instead of rapid full-frame flashes.
- Export crop breaks type: design separately for square and vertical instead of cropping.

## 16. Example: generated-media explainer assembly

Example intent: assemble AI-generated stills/video clips, narration, captions, diagrams, and music into a 60-second explainer.

Approach:

1. Treat generated assets as ingredients with full prompts, model/version/settings, seeds when available, and approvals.
2. Build scenes around claims, not assets. Each scene needs a takeaway and one dominant visual idea.
3. Use HyperFrames for the editorial layer: animated titles, diagram labels, callouts, captions, transitions, audio mix, and final QA.
4. Keep a transcript and caption file even if captions are burned into the video.
5. Flag factual claims, synthetic depictions of real people/events, medical/legal/financial claims, and copyrighted/reference-derived visuals for approval.

Expected failure modes:

- Asset style drift: normalize with CSS treatments, color overlays, consistent crops, and restrained transitions; regenerate only when the source is unusable.
- Generated clips have inconsistent fps/resolution: transcode to a common render profile before staging.
- Provenance is incomplete: block final delivery until missing model/source/rights fields are resolved or explicitly accepted.
