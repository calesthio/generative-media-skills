---
name: motion-graphics-direction
description: Provider-independent motion graphics direction for AI agents producing title sequences, lower thirds, explainer graphics, product UI overlays, social ads, kinetic typography, diagrams, data callouts, brand films, and video post. Use when planning, prompting, storyboarding, specifying, implementing, reviewing, or QAing motion graphics across live footage, generated video, UI capture, data visualization, brand systems, typography, accessibility, claim integrity, runtime handoff, and iteration.
---

# Motion Graphics Direction

Use this skill to turn a video brief into motion graphics that explain, emphasize, brand, or pace the piece. Treat motion as editorial direction: every move should reveal meaning, guide attention, clarify structure, or create a deliberate feeling.

This is provider-independent. Use it before choosing a model, renderer, animation library, editing tool, or compositing environment.

## Evidence stance

Documented facts:

- WCAG 2.2 requires web content to avoid flashes above the three-flashes threshold and documents that interaction-triggered motion should be disableable unless essential. Verified 2026-07-10 from W3C WCAG Understanding pages.
- W3C Technique C39 documents `prefers-reduced-motion` as a way to let users prevent animations. Verified 2026-07-10.
- WCAG contrast guidance sets 4.5:1 for normal text and 3:1 for large text at Level AA, with higher AAA ratios. Verified 2026-07-10.
- Apple, Material Design, Microsoft Fluent, and IBM Carbon all treat motion as a design-system behavior with purpose, timing, easing, accessibility, and consistency constraints rather than decoration. Verified 2026-07-10.
- Netflix timed-text guidance uses two-line maximums and language-specific line-length limits such as 42 characters per line for many Latin-script subtitle templates. Verified 2026-07-10.
- Datawrapper explains why bar and column charts should normally start at zero, because bar length encodes magnitude. Verified 2026-07-10.

Empirical observations from production practice:

- Viewers read motion graphics in a small number of attention windows: entry, hold, emphasis, exit. Crowding too many simultaneous changes often lowers comprehension.
- AI-generated and template-driven videos often fail because overlays compete with the subject, data marks animate without scale context, and typography is chosen for style before legibility.
- Strong motion packages usually feel simple because many hidden choices are locked: type scale, grid, safe areas, easing family, timing ratios, transitions, caption policy, and data-label policy.

Production heuristics:

- If motion does not change what the viewer understands, remembers, or feels, remove it or make it quieter.
- Animate attention in layers: one primary idea, one supporting cue, and one background behavior at most.
- Prefer motion contrast over motion volume: a single precise reveal often feels more premium than many animated parts.
- For accessibility, design a reduced-motion path at the concept stage, not as a late patch.

## Start with the job of the graphic

Classify every motion graphic by its production job before designing it:

| Job | Use it for | Direction test |
|---|---|---|
| Orientation | title sequence, section card, chapter open, map/location tag | Can the viewer answer "where am I in the story?" |
| Identification | lower third, speaker label, product label, source tag | Is the label readable before attention returns to footage? |
| Emphasis | callout, highlight, zoom box, pointer, price/feature reveal | Does it point to one thing without covering the evidence? |
| Explanation | diagram, process flow, kinetic typography, UI walkthrough | Does motion reveal causality or order? |
| Proof | data callout, chart, claim card, citation, before/after | Are source, denominator, unit, and timeframe visible enough? |
| Rhythm | beat-synced type, transition, visual punctuation | Does it support pacing without obscuring content? |
| Brand affect | logo sting, launch film, social ad, hero title | Does it express the brand's posture, not just its colors? |

If one graphic tries to do more than two jobs, split it into beats.

## Decide motion purpose before style

For each graphic, write a one-sentence motion purpose:

- "Reveal the three-step sequence in the same order the narrator explains it."
- "Make the product metric feel credible by holding the source and baseline long enough to read."
- "Let the lower third enter quietly so it identifies the speaker without interrupting emotion."
- "Use a sharp type snap on the campaign promise, then a calm hold for recognition."

Reject purposes like "make it dynamic," "add energy," or "look cool" unless they are translated into a viewer effect.

## Build hierarchy across time

Motion graphics hierarchy is temporal as much as visual. Give the viewer a controlled reading path:

1. Establish the frame: where the eye should look first.
2. Reveal the main idea: one title, number, label, or visual change.
3. Add context: unit, label, source, speaker role, UI location, comparison.
4. Hold: leave enough stillness for reading and comprehension.
5. Exit or settle: clear the frame before the next idea competes.

For short-form social, this can happen in under two seconds; for dense explainers or data graphics, it may need five to eight seconds. Do not choose duration only from platform norms; choose it from reading load, narration pace, and visual complexity.

## Timing and easing direction

Describe timing in beats, not vague adjectives. A useful spec includes:

- entry duration;
- hold duration;
- emphasis moment;
- exit duration;
- easing character;
- relationship to narration, music, or edit point;
- what stays still.

Common timing heuristics:

- Labels and lower thirds: fast entrance, stable hold, quiet exit. The entrance should be noticeable but not theatrical unless the piece is brand-led.
- Kinetic typography: move only the words that carry meaning. Keep supporting words calmer.
- Diagrams: reveal one relationship at a time; finish each causal link before starting the next.
- Data callouts: animate the measure, then hold the final value with its unit and source.
- UI overlays: sync to the user action. If a pointer/callout arrives late, the viewer may look at the wrong UI state.
- Transitions: treat as punctuation. A hard cut, dissolve, wipe, morph, or type burst should reflect the logical relationship between scenes.

Easing vocabulary:

- Linear: mechanical, constant, usually best for progress, clocks, scanning, or intentionally robotic systems.
- Ease-out: quick arrival with gentle settling; useful for labels, cards, and callouts entering the viewer's attention.
- Ease-in: delayed acceleration; useful for exits, pulls, or "departing" elements.
- Ease-in-out: controlled movement between two states; useful for UI state changes and diagrams.
- Spring/overshoot: expressive, physical, playful, but can look cheap or distracting if used on serious claims, legal copy, or dense data.
- Step/hold: editorial, rhythmic, useful for title cards, terminal/UI demos, and kinetic typography.

Design-system sources differ in exact values. Use the project's brand tokens when available; otherwise describe the curve intent and ask implementation to choose matching tokens in the chosen runtime.

## Composition and layout

Direct motion graphics inside a real frame, not on an empty artboard.

Check:

- Subject clearance: do not cover faces, hands, product interactions, medical/legal disclaimers, subtitles, or the key object.
- Safe areas: reserve edges for platform UI, captions, and cropping variants. For social deliverables, specify 9:16, 1:1, 16:9, and cropped derivatives separately when required.
- Eye trace: place graphics where the viewer is already looking or where you need the eye to travel next.
- Depth relationship: decide whether graphics live on glass above footage, attach to objects in the scene, or exist as editorial cards between shots.
- Contrast zone: add scrims, panels, blur, or local shadows when footage is too busy for text.
- Negative space: leave a quiet region for reading. If footage lacks it, create one with a crop, reframing, blur, or card.
- Continuity: carry anchor positions across a sequence so recurring labels are easy to find.

Avoid "floating decoration" that does not align to the footage, grid, subject, or narrative.

## Typography for motion

Typography must survive movement, compression, small screens, and short holds.

Direction checklist:

- Choose a type role first: title, subtitle, label, caption, number, source, legal, UI annotation.
- Use a type scale with clear contrast between roles. Do not rely only on color.
- Keep line lengths short for motion. If a phrase cannot be read in one hold, split it into beats.
- Use weight changes sparingly; animated weight changes can shimmer after compression.
- Avoid thin strokes, tiny all-caps, and tight tracking over video.
- Preserve brand typefaces when supplied, but override with a more legible fallback for captions, legal text, or tiny UI labels if needed.
- For multilingual/localized versions, reserve expansion space and avoid layouts that depend on English word length.
- For lower thirds, separate name, role, organization, and optional context into an intentional hierarchy.
- For kinetic typography, make semantic stress visible: nouns, verbs, numbers, contrasts, and reversals get motion; filler words stay stable or group with their phrase.

Accessibility anchors:

- Use WCAG contrast as a floor for digital text: 4.5:1 normal text and 3:1 large text at AA; consider stronger contrast for mobile video, compression, and outdoor viewing.
- Do not communicate meaning by color alone. Pair color with labels, icons, shape, position, or text.
- Keep important text on screen long enough to read aloud at a natural pace, then add a margin.

## Brand systems and motion language

Translate brand into behavior, not only appearance:

- Premium/minimal: fewer moves, longer holds, precise easing, restrained transitions, generous negative space.
- Editorial/news: direct cuts, source-forward lower thirds, stable charts, restrained emphasis.
- SaaS/product: UI-anchored overlays, clear step sequencing, consistent callout grammar, responsive micro-motion.
- Youth/social: larger type, rhythmic cuts, beat accents, bolder color, but still protect readability.
- Technical/explainer: diagram logic, progressive disclosure, consistent symbols, less ornamental motion.
- Luxury/brand film: slow reveal, controlled parallax or depth, tactile material behavior, fewer claims.

Create a motion palette for the project:

- entry style;
- exit style;
- emphasis style;
- transition family;
- lower-third behavior;
- data reveal behavior;
- reduced-motion alternative;
- forbidden moves.

Keep this palette small. Consistency is what lets viewers learn the system.

## Accessibility and viewer safety

Apply these as hard constraints unless the deliverable is a private draft with an explicit waiver:

- Do not create flashes above the WCAG three-flashes threshold. Avoid rapid high-contrast flicker even when technically below threshold.
- Provide or specify a reduced-motion treatment for interactive/web/app surfaces and for versions likely to be embedded in UI.
- Avoid unnecessary parallax, spinning, vortex, rapid zoom, large-field depth changes, and multi-axis motion when they are not essential.
- Ensure text contrast and non-text contrast against changing footage, not just against a static design mock.
- Do not place essential information only in motion; the final held state should still communicate the key point.
- Avoid fast-moving captions or subtitles. Caption motion should not compete with reading.
- If a video contains continuous animation, auto-advancing graphics, or background loops, specify pause/stop behavior when published in an interactive environment.
- For platform videos, include captions or caption-safe layout when speech carries meaning.

Reduced-motion does not always mean no animation. Prefer opacity, simple cuts, shorter travel distance, stable final states, and lower velocity while preserving orientation and meaning.

## Data, claim, and source integrity

Motion can make claims feel more persuasive than the evidence supports. Treat data graphics as editorial evidence.

Require:

- source;
- date or timeframe;
- denominator or base population;
- units;
- comparison baseline;
- uncertainty, estimate status, or sample size when relevant;
- transformation notes such as indexed values, averages, smoothing, or projections.

Data motion rules:

- Animate proportional marks honestly. If bar length encodes magnitude, a zero baseline is normally required unless a clearly labeled alternative is justified.
- Do not use 3D, perspective, elastic overshoot, or decorative scaling when it distorts comparison.
- Avoid animating a number upward without the denominator or timeframe.
- Do not cherry-pick a start or end frame to exaggerate a trend.
- Keep chart axes, labels, and units present during the hold, not only before or after the animation.
- If a claim is qualitative ("faster onboarding"), do not make it look like measured data unless a measured source exists.
- For before/after footage, match crop, timepoint, lighting, and scale when comparison fairness matters.
- For product UI overlays, distinguish "conceptual UI," "prototype," "simulated data," and "actual product capture."

If legal, medical, financial, or safety claims appear, ask for approved copy and source material. Motion direction cannot invent substantiation.

## Working with footage or generated video

Before adding overlays, inspect the actual shot:

- Where is the subject's attention?
- What areas are visually quiet?
- Does camera motion fight the overlay?
- Does depth of field make attachment tracking plausible?
- Is there room for captions and platform UI?
- Are there moments where the graphic should disappear to let performance or evidence breathe?

Overlay strategies:

- Screen-space overlay: stable cards, subtitles, labels, title graphics.
- Scene-attached overlay: tracked labels, arrows, product pins, map points. Use only when tracking quality supports it.
- Editorial insert: full-screen diagram or card between footage beats.
- Split composition: footage plus chart/UI panel. Use when evidence needs more room than an overlay can safely provide.
- Match cut or morph: transition from object/footage to diagram/UI state. Use when it clarifies identity or causality.

With AI-generated footage, expect spatial drift, inconsistent objects, and text artifacts. Avoid precise tracking or tiny labels unless the shot has been verified. It is often safer to use editorial cards, clean UI redraws, or abstract diagrams than to pin detailed graphics to unstable generated video.

## Storyboard-to-motion handoff

Convert storyboard frames into motion instructions by adding:

- beat number and timecode range;
- narrative purpose;
- primary viewer focus;
- on-screen text exactly as approved;
- elements entering, holding, transforming, and exiting;
- easing/timing character;
- relationship to narration/music/edit;
- layout anchors and safe-area notes;
- accessibility notes;
- data/source requirements;
- implementation notes and fallback if tracking or runtime fails.

Example beat spec:

```text
Beat 04, 00:12.0-00:16.5
Purpose: Explain why the old workflow loses time.
Focus: Cursor selects "Export CSV" in product capture.
Graphic: Three small delay labels appear beside the UI path: "download", "clean", "re-upload".
Motion: Each label enters 4 frames after the relevant click with ease-out, then connects with a thin line. No bounce. Hold all three labels for 1.2s after narration says "three manual steps."
Layout: Right side only; keep bottom 18% clear for captions.
Access: Labels must pass contrast over footage; add 70% dark scrim behind label group if capture is busy.
Fallback: If tracking is unstable, use a split-screen redraw of the UI path instead of pinned labels.
```

## Prompt/spec writing for generation and implementation

Write prompts and implementation specs with concrete motion grammar. Include:

- deliverable format and duration;
- audience and platform;
- brand tone;
- exact text;
- hierarchy;
- layout and safe areas;
- timing;
- easing;
- scene relationship;
- accessibility constraints;
- data/source constraints;
- forbidden artifacts.

Weak direction:

```text
Add cool animated text and charts to make the video pop.
```

Stronger direction:

```text
Create a 7-second motion-graphics insert for a B2B product explainer. Premium minimal style, dark navy background, off-white type, one cyan accent. Reveal the headline "Manual review is the bottleneck" first, hold 0.8s, then reveal a three-step horizontal process: Intake -> Review -> Escalate. Animate each node left to right as the narrator names it. Use ease-out entries with no bounce; thin connector lines draw after each node appears. Keep all elements stable for the final 1.5s. Include a small source note area in the lower-right but use placeholder text "[source/date]" until approved. No flashing, no 3D, no spinning, no decorative particles.
```

For implementation handoff, specify expected layer names or object roles rather than only visuals:

```text
Layers: bg_scrim, title_primary, process_node_1..3, connector_1..2, source_note.
Expose tokens: bg, text_primary, accent, duration_enter, duration_hold, ease_enter.
Required QA: contrast check on all text; 9:16 crop check; source note visible in final hold; reduced-motion variant uses cuts/fades only.
```

## Runtime handoff

Choose the runtime from the production needs:

- Timeline compositor or video editor: best when working with footage, precise cuts, audio sync, subtitle burn-in, color, and conventional post.
- HTML/CSS/GSAP-style runtime: strong for kinetic typography, UI overlays, SVG diagrams, responsive variants, and web-native motion systems.
- React/Remotion-style runtime: strong for code-driven video, data-bound graphics, repeatable scene components, captions, and programmatic variants.
- 3D runtime: use when depth, camera, lighting, or product geometry matters; avoid it for simple charts or lower thirds.
- Lottie/vector export: use for lightweight UI animations and reusable app assets; verify text rendering, font handling, and feature support.
- Data-viz runtime: use for charts that must be generated from data, not hand-drawn.

Runtime handoff should include:

- frame rate;
- resolution/aspect ratios;
- color profile expectations when known;
- font files or approved fallbacks;
- brand tokens;
- exact copy;
- data files and transformations;
- source/citation text;
- animation timing;
- reduced-motion behavior;
- export requirements;
- compression-sensitive details such as thin lines or gradients;
- QA checks.

Never ask implementation to "make it match the reference" without specifying which motion properties matter.

## Review and iteration

Review in passes:

1. Purpose pass: Does each graphic have a job?
2. Readability pass: Can text, numbers, labels, and sources be read at final size and speed?
3. Attention pass: Does the motion lead the eye to the intended focus?
4. Integration pass: Does it respect footage, captions, cropping, edit rhythm, and audio?
5. Brand pass: Does behavior match brand posture and system rules?
6. Evidence pass: Are data and claims sourced, proportional, and not over-animated?
7. Accessibility pass: Check contrast, flashing, reduced-motion needs, captions, and color-only meaning.
8. Technical pass: Check tracking, dropped frames, text shimmer, compression, crop variants, and export specs.

Give notes in production language:

- Replace "make it smoother" with "change the title entry from linear to ease-out and extend the deceleration by 6 frames."
- Replace "too busy" with "remove the background particle loop during the chart reveal; keep only the axis draw and value count-up."
- Replace "more premium" with "halve the number of animated elements, remove overshoot, increase the final hold, and use a quieter transition."
- Replace "data feels sketchy" with "hold the source, timeframe, and denominator with the number; remove the animated upward arrow unless the data is a time trend."

## Motion QA checklist

Use this before final export:

- Every graphic has a stated job and timecode.
- The primary message is readable with audio muted.
- Captions and lower thirds do not collide.
- Important text passes contrast against the actual moving background.
- No flash pattern exceeds WCAG guidance; risky flicker is removed.
- Reduced-motion requirements are specified for interactive or web/app delivery.
- All data claims include source, unit, timeframe, and denominator where relevant.
- Charts preserve proportional meaning.
- Brand tokens and type hierarchy are consistent.
- Crop variants preserve the important action and text.
- Overlay tracking is stable or replaced by an editorial insert.
- Final compression does not destroy thin lines, small text, gradients, or shadows.
- Legal/source text is held long enough to read if it substantiates a claim.

## Example: lower third over interview footage

Production intent: Identify a speaker in a serious customer story without interrupting emotional performance.

Inputs and constraints:

- 16:9 master and 9:16 crop.
- Speaker face is left third; captions occupy bottom center.
- Brand is restrained enterprise SaaS.

Direction:

```text
00:03.2-00:08.8 lower third.
Place on right third, vertically centered below shoulder line; keep bottom caption-safe area clear.
Text: "Maya Chen" primary, "VP Operations, Northstar Health" secondary.
Motion: A 1px accent line draws left-to-right over 10 frames; name fades/slides 12px up with ease-out over 12 frames; role follows 4 frames later. Hold stable for 4.8s. Exit by opacity fade over 8 frames. No bounce, no blur, no logo animation.
Accessibility: Maintain 4.5:1 contrast over footage using a subtle dark translucent panel if needed. Ensure 9:16 crop keeps the full lower third or replace with stacked mobile variant.
QA: Check it does not overlap open captions; export still at 00:05.0 for approval.
```

Why it is structured this way: the motion acknowledges the speaker without stealing attention; stagger creates hierarchy; the right-side placement avoids the face and captions.

Likely failure modes: placing text too low, using brand animation that competes with speech, too-short hold, insufficient contrast over a changing background.

## Example: product UI overlay

Production intent: Explain an automation flow on top of screen capture.

Inputs and constraints:

- 20-second product demo.
- Cursor path matters.
- Needs version for sales deck and social ad.

Direction:

```text
Use UI-attached callouts only when the underlying element is static for at least 1.0s. Each callout appears within 6 frames of the cursor action it explains.

Callout grammar:
- Primary action callout: cyan outline, label above target, connector line with 90-degree elbow.
- System-result callout: green check icon plus short label, no connector if adjacent.
- Warning/exception callout: amber label, never use red unless the UI itself indicates an error.

Timing:
00:04.0 click "Create rule" -> callout "Define once" enters 00:04.1, holds to 00:06.0.
00:06.2 rule preview appears -> callout "Applies to every new request" enters with ease-out, connector draws after label.
00:10.0 dashboard updates -> split-screen zoom panel replaces tracking; show before/after count with source note "Sample workspace data".

Accessibility: Keep all labels at least caption-size in the final export; no fast cursor zooms in reduced-motion version.
Fallback: If screen capture is low resolution, redraw the relevant UI in a clean vector panel rather than magnifying pixels.
```

Why it is structured this way: the overlay follows the user action, distinguishes action from result, and avoids pretending sample UI is production evidence.

Likely failure modes: delayed labels, jittery tracking, labels covering the cursor, overusing zooms, failing to distinguish simulated data.

## Example: data callout in a social ad

Production intent: Present a performance claim without overstating it.

Inputs and constraints:

- Approved claim: "31% fewer manual escalations in pilot teams."
- Required source: "Internal pilot, 8 teams, Apr-Jun 2026."
- 9:16 social, 6 seconds.

Direction:

```text
00:00.0-00:01.0: Title "Fewer manual escalations" appears as static type after a hard cut. No animated count-up yet.
00:01.0-00:02.2: Number "31%" scales from 96% to 100% with ease-out over 10 frames, not from 0. Add "fewer" as adjacent text, same baseline.
00:02.2-00:04.5: Small comparison bar appears underneath: "Pilot teams" vs "Prior workflow". Bars use a zero baseline and direct labels. Do not use 3D, perspective, or overshoot.
00:04.5-00:06.0: Hold final state with source: "Internal pilot, 8 teams, Apr-Jun 2026." Keep source visible for full final hold.
Accessibility: High contrast; do not use color alone to show improvement. Include down-arrow only with text "fewer".
```

Why it is structured this way: the claim is framed with denominator and timeframe, the bar comparison preserves proportion, and the number does not use a misleading dramatic count from zero.

Likely failure modes: "31%" animating like a financial ticker, source disappearing too quickly, missing baseline, implying audited public data when it is internal pilot data.

## Sources verified 2026-07-10

- W3C, WCAG 2.2 Understanding SC 2.3.1 Three Flashes or Below Threshold: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- W3C, WCAG 2.2 Understanding SC 2.3.3 Animation from Interactions: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
- W3C, Technique C39 Using the CSS `prefers-reduced-motion` query: https://www.w3.org/WAI/WCAG22/Techniques/css/C39
- W3C, WCAG 2.2 Understanding SC 1.4.3 Contrast Minimum: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- Apple Human Interface Guidelines, Motion: https://developer.apple.com/design/human-interface-guidelines/motion
- Apple App Store Connect, Reduced Motion evaluation criteria: https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria/
- Material Design 3, Easing and duration: https://m3.material.io/styles/motion/easing-and-duration
- Material Design, Understanding motion: https://m2.material.io/design/motion/understanding-motion.html
- Microsoft Fluent 2 Design System, Motion: https://fluent2.microsoft.design/motion
- IBM Carbon Design System, Motion: https://carbondesignsystem.com/elements/motion/overview/
- Netflix Partner Help, Timed Text Style Guide general requirements: https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements
- Netflix Partner Help, Subtitle templates: https://partnerhelp.netflixstudios.com/hc/en-us/articles/219375728-Timed-Text-Style-Guide-Subtitle-Templates
- Royal Statistical Society, Best Practices for Data Visualisation: https://royal-statistical-society.github.io/datavisguide/
- Data.europa.eu, Honest charts: ethics and integrity in data visualisation: https://data.europa.eu/en/publications/datastories/honest-charts-ethics-and-integrity-data-visualisation
- Datawrapper Academy, Why our column and bar charts start at zero: https://www.datawrapper.de/academy/why-our-column-and-bar-charts-start-at-zero
- Adobe, Understanding the 12 principles of animation: https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html
