# Evaluation: motion-graphics-direction

Use this answer key to score an agent that has access to `SKILL.md` and is asked to perform motion graphics direction. Do not expose this file to the evaluated agent.

Total suggested score: 100 points. Passing: 80+. Strong: 90+. A response with any critical failure should not pass even if the numeric score is high.

## Critical failures

Fail the evaluation if the response:

- treats motion as decoration without explaining viewer purpose;
- invents data, sources, legal substantiation, product facts, or claim evidence;
- ignores accessibility when flashes, reduced motion, small text, color-only meaning, or captions are relevant;
- recommends misleading data animation such as proportional bars without scale/baseline context;
- gives implementation-only code without motion direction, hierarchy, timing, or review criteria;
- covers or disregards important footage, faces, captions, UI actions, or required disclaimers;
- exposes or references this evaluation file in a production answer.

## Knowledge questions

### 1. What is a motion purpose?

Expected answer: A motion purpose states what the movement should make the viewer understand, notice, remember, or feel. It is more specific than "make it dynamic." It should tie motion to orientation, identification, emphasis, explanation, proof, rhythm, or brand affect.

Required points:

- Mentions viewer effect or story function.
- Rejects generic decorative motion.
- Connects purpose to design choices such as timing, hierarchy, hold, or reveal.

Penalize: "Motion purpose is the animation style" or "use motion to make things pop."

### 2. Explain why hierarchy in motion graphics is temporal.

Expected answer: Viewers read graphics over time: establish focus, reveal the main idea, add context, hold for comprehension, then exit/settle. Hierarchy is created by order, timing, stillness, size, placement, contrast, and relationship to narration/edit.

Required points:

- Includes reveal order.
- Includes hold/readability.
- Notes that simultaneous changes can compete.

### 3. What accessibility issues must be checked in motion graphics?

Expected answer: Flash/flicker risk, reduced-motion needs, text contrast against actual moving backgrounds, non-text contrast, color-only meaning, captions/subtitles collision, reading time, fast movement/zoom/spin/parallax, and pause/stop behavior for ongoing interactive motion.

Required points:

- References flashes or flicker.
- References reduced motion.
- References text readability/contrast.
- References captions or reading time when video includes speech/text.

Critical miss: Saying accessibility is only font size or only alt text.

### 4. How should an agent handle a data callout in a motion graphic?

Expected answer: Require source, timeframe, units, denominator/baseline, and uncertainty/sample/projection notes when relevant; animate proportional marks honestly; keep axes/labels/source visible during the hold; avoid 3D/perspective/overshoot that distorts comparison; distinguish qualitative claims from measured data.

Required points:

- Mentions source and timeframe.
- Mentions denominator/unit/baseline as applicable.
- Mentions honest proportional animation.
- Mentions not overstating evidence.

### 5. What is the difference between screen-space and scene-attached overlays?

Expected answer: Screen-space overlays are stable editorial graphics above the frame, such as cards, captions, and lower thirds. Scene-attached overlays are tracked or pinned to objects/UI in the shot. Scene-attached overlays require sufficient tracking stability and should fall back to editorial inserts or redraws when footage/generated video drifts.

Required points:

- Defines both.
- Mentions tracking quality.
- Mentions fallback when unstable.

## Production-decision scenarios

### 6. Lower third over emotional interview

Scenario: A customer story has an interview subject on the left, open captions at the bottom, and a restrained enterprise brand. The user asks for "a stylish lower third."

Strong expected decision:

- Place the lower third away from face and caption-safe area.
- Use hierarchy for name, role, organization.
- Use quiet entry, stable hold, quiet exit.
- Specify readable contrast over footage, possible panel/scrim, and crop variants.
- Avoid playful bounce or excessive logo animation.

Scoring: 10 points.

- 2 purpose and restraint.
- 2 layout respecting face/captions.
- 2 hierarchy/copy roles.
- 2 timing/easing/hold.
- 2 accessibility/crop QA.

Penalize: Bottom placement colliding with captions, decorative kinetic type, no duration, no contrast check.

### 7. UI demo with callouts

Scenario: A SaaS demo shows cursor clicks in a product. The user wants labels that explain each step.

Strong expected decision:

- Sync callouts to cursor/action timing.
- Define callout grammar for action, result, warning, or context.
- Keep labels legible and anchored to stable UI regions.
- Avoid delayed labels and excessive zooms.
- Use split-screen redraw or editorial panel if tracking/capture resolution is poor.
- Distinguish actual UI from mock/simulated data.

Scoring: 10 points.

- 2 sync to UI action.
- 2 visual grammar/hierarchy.
- 2 tracking/resolution fallback.
- 2 accessibility/readability.
- 2 product/data truthfulness.

### 8. Social ad data claim

Scenario: Approved copy says "31% fewer manual escalations in pilot teams," with source "Internal pilot, 8 teams, Apr-Jun 2026." The user wants a punchy animated number.

Strong expected decision:

- Use the exact claim and source.
- Avoid unsupported embellishment such as "proven," "guaranteed," or public benchmark language.
- Keep "fewer," denominator/sample/timeframe, and source visible long enough to read.
- Avoid misleading count-up from zero if it implies an absolute quantity; use a restrained scale/reveal.
- If using bars, preserve proportional baseline and labels.
- Use high contrast and avoid color-only meaning.

Scoring: 12 points.

- 2 exact claim preservation.
- 2 source/timeframe/sample visibility.
- 2 honest number animation.
- 2 proportional chart treatment.
- 2 accessibility/readability.
- 2 legal/claim restraint.

Critical fail: inventing a stronger claim or omitting the internal-pilot source.

### 9. Title sequence for brand film

Scenario: A premium brand film needs a 12-second opening title over slow product footage.

Strong expected decision:

- Defines brand behavior: restraint, precision, negative space, fewer moves.
- Integrates with footage and avoids covering product hero moments.
- Uses a small motion palette: title reveal, subtle transition, final hold.
- Specifies timing/easing and what remains still.
- Includes crop/contrast/compression checks.

Scoring: 8 points.

- 2 brand behavior.
- 2 footage integration.
- 2 timing/easing/hold.
- 2 QA/accessibility/export concerns.

Penalize: adding particles, fast kinetic text, or many transitions without story purpose.

### 10. Explainer diagram

Scenario: A narrator explains how data moves through three systems. The user asks for a diagram animation.

Strong expected decision:

- Reveals one relationship at a time in narration order.
- Uses consistent symbols, connectors, labels, and directionality.
- Holds completed state for comprehension.
- Avoids simultaneous motion overload.
- Specifies source/claim handling if metrics appear.
- Provides reduced-motion fallback using cuts/fades/progressive states.

Scoring: 10 points.

- 2 progressive disclosure.
- 2 visual/system consistency.
- 2 timing/narration sync.
- 2 readability/accessibility.
- 2 evidence handling/fallback.

## Applied production task

### 11. Full motion direction brief

User request: "Create motion graphics direction for a 30-second product launch video. It has generated hero footage, one UI screen recording, two metric claims, a founder quote, captions, and versions for 16:9 and 9:16. The brand is modern but credible, not hypey."

Expected approach:

- Start by classifying graphic jobs across the piece: title, lower third/quote, UI callouts, data claims, transitions, captions.
- Provide a motion palette consistent with "modern but credible": restrained easing, clear holds, limited accent motion, no gratuitous bounce/particles.
- Specify timeline beats with time ranges, purpose, focus, text roles, motion behavior, and holds.
- Address generated footage limitations: avoid precise tracking unless verified; use editorial cards or clean overlays when footage drifts.
- Address UI capture: action-synced callouts, capture resolution, fallback redraw.
- Address metric claims: source, denominator, timeframe, units, proportional chart treatment, visible source holds.
- Address quote/lower third: readable hierarchy and caption-safe layout.
- Address accessibility: contrast over footage, flashes, reduced motion, captions, color-only meaning.
- Address multi-aspect delivery: safe areas and alternate layout for 9:16.
- Include implementation handoff and QA checklist.

Scoring rubric: 25 points.

- 3 clear graphic-job classification and purpose.
- 3 strong temporal hierarchy/timeline.
- 3 timing/easing specificity.
- 3 composition/footage/caption integration.
- 3 brand-motion coherence.
- 3 data and claim integrity.
- 3 accessibility and reduced-motion handling.
- 2 runtime/implementation handoff.
- 2 QA and iteration notes.

Critical failures:

- Omits claims/data integrity.
- Omits captions or accessibility.
- Treats generated footage as reliably trackable without verification.
- Provides only generic style adjectives and no production-ready timing/spec.

## Scoring guidance by dimension

### Purpose and hierarchy, 15 points

Strong answers identify the job of each graphic and describe the reading path over time. Weak answers list graphic types without explaining why they move.

### Motion craft, 15 points

Strong answers specify entries, holds, exits, easing character, relation to narration/edit/music, and what remains still. Weak answers say "smooth," "dynamic," "cinematic," or "fast-paced" without operational detail.

### Composition and integration, 15 points

Strong answers account for footage, faces, UI actions, captions, crop variants, safe areas, and contrast zones. Weak answers design on an empty frame.

### Typography and brand, 10 points

Strong answers preserve hierarchy, type roles, legibility, brand posture, and localization/crop concerns. Weak answers choose fonts or colors without motion behavior.

### Accessibility, 15 points

Strong answers explicitly handle flashing, reduced motion, contrast, reading time, captions, and color-only meaning. Weak answers mention accessibility generically.

### Data/claim integrity, 15 points

Strong answers require source, timeframe, denominator, units, baseline, and visual proportionality. Weak answers animate numbers as persuasion without substantiation.

### Handoff and QA, 15 points

Strong answers provide enough detail for implementation and review: layers/roles, tokens, timecodes, fallback paths, crop/export checks, and iteration notes. Weak answers stop at concept direction.

## Calibration examples

Excellent response characteristics:

- "The metric reveal should not count from 0 to 31 because the approved claim is a percentage reduction from an internal pilot; reveal 31% with a restrained scale and hold the source line for 1.5 seconds."
- "The UI callout should enter within 6 frames of the click and disappear before the cursor moves to the next target."
- "For reduced motion, replace the zooming parallax title with a cut to final layout plus opacity fade; preserve the same reading order."

Poor response characteristics:

- "Use flashy kinetic typography and animated charts to grab attention."
- "Make the lower third pop with bouncing text and particles."
- "Animate the bar chart dramatically so the improvement looks bigger."
- "Track labels to the generated footage objects" without checking whether the objects are stable.
