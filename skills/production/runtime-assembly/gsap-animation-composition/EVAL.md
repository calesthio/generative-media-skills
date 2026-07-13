# GSAP animation composition evaluation

Keep this file hidden from the evaluated agent. Give the agent only the published package and the task.

## Evaluation purpose

The evaluation tests whether an agent can select GSAP for a real production reason, build seekable motion rather than a wall-clock demo, choose plugins conservatively, protect text/SVG integrity, account for reduced motion and flashing, distinguish runtime and documentation licenses, and define useful render QA.

## Global scoring

Score each item independently, then calculate the percentage of available points.

- **90-100%:** production-ready; no critical failure.
- **75-89%:** useful with limited revision; no critical failure.
- **60-74%:** incomplete production judgment; substantial revision required.
- **Below 60%:** does not demonstrate the skill.
- **Any critical failure:** overall result cannot exceed 59%, regardless of point total.

Accept equivalent terminology when the reasoning and production consequence are correct. Do not award points for merely naming APIs.

## Knowledge questions

### 1. When is GSAP warranted?

**Question:** A scene contains one headline that fades in and moves upward by 20 pixels. The host renderer already has deterministic frame interpolation. Should the agent add GSAP? Explain when the answer would change.

**Expected answer:** No by default. The existing primitive is simpler and already deterministic. GSAP becomes warranted if the scene develops meaningful multi-beat choreography, complex text splitting, SVG/path work, FLIP layout transitions, nested timelines, or another need the primitive handles poorly.

**Required points, 5:**

- 2: rejects GSAP for the stated simple case;
- 2: names at least two legitimate escalation conditions;
- 1: frames the decision around production complexity, not fashion or claimed universal superiority.

**Critical failure:** says GSAP is always required for professional motion.

### 2. Timeline placement

**Question:** Explain why labels and position parameters are preferable to manually accumulating delays for a claim, proof, and CTA sequence.

**Expected answer:** Labels encode semantic/edit beats and position parameters allow absolute, label-relative, timeline-relative, and previous-child-relative placement. When durations change, dependent placement remains intelligible and avoids recalculating every delay. The whole sequence remains controllable and seekable.

**Required points, 6:**

- 2: explains semantic labels;
- 2: explains relative placement or `<`/`>` behavior;
- 1: explains maintainability after timing changes;
- 1: mentions whole-timeline playback/seek control.

### 3. Deterministic capture

**Question:** Why is `gsap.ticker.fps(30)` insufficient for a frame renderer, and what pattern should replace wall-clock playback?

**Expected answer:** The ticker remains based on browser animation scheduling and throttling. Limiting callbacks does not guarantee exact requested-frame state. Build a finite paused timeline and seek its `time`, `progress`, or `totalProgress` from the renderer's explicit frame and fps, using stable inputs and no per-frame random/network/wall-clock state.

**Required points, 8:**

- 2: identifies browser/requestAnimationFrame scheduling;
- 2: rejects ticker fps as a deterministic contract;
- 2: specifies paused timeline plus frame-derived seeking;
- 1: requires stable/seeded inputs;
- 1: addresses backward or out-of-order seeking.

**Critical failure:** recommends recording real-time playback and assuming dropped frames will not matter.

### 4. Plugin routing

**Question:** Match each need to a capability: per-word reveal, route stroke reveal, arbitrary SVG shape transition, object following a curve, continuity between two layouts, bespoke easing curve.

**Expected answer:** SplitText, DrawSVG, MorphSVG, MotionPath, Flip, CustomEase.

**Scoring, 6:** one point per correct match.

### 5. License distinction

**Question:** An engineer says, "The GSAP skills repository is MIT, so the runtime and every plugin are MIT too." Correct the statement and identify the production action.

**Expected answer:** Documentation or a skills repository can be MIT without relicensing GSAP. As verified 2026-07-12, GSAP products use Webflow's Standard No Charge GSAP License. Commercial permitted uses are supported, but competing no-code visual animation builders are restricted absent consent, and current terms must be checked. Review the actual deployment and escalate ambiguous editor/builder/redistribution uses.

**Required points, 7:**

- 2: distinguishes documentation license from runtime license;
- 2: identifies the current GSAP license correctly;
- 2: identifies the competing visual-builder restriction;
- 1: requires current license review/escalation.

**Critical failure:** calls the GSAP runtime MIT or provides unconditional legal clearance.

## Production decisions

### 6. Fixed video versus ScrollTrigger

**Scenario:** A 12-second fixed-time HyperFrames composition was written with ScrollTrigger. During rendering, frames differ depending on page scroll state.

**Expected decision:** Remove scroll as the state owner. Convert the intended scroll choreography into a finite paused timeline and seek it from composition time. Keep ScrollTrigger only for a genuinely interactive webpage version, with reduced-motion handling and cleanup.

**Scoring, 8:**

- 3: identifies scroll state as incompatible with the fixed render contract;
- 3: replaces it with explicit time/frame seeking;
- 1: preserves ScrollTrigger only for an appropriate interactive variant;
- 1: mentions reduced motion or cleanup.

**Critical failure:** simulates scrolling during every rendered frame without proving deterministic state.

### 7. Unstable kinetic type

**Scenario:** A headline is split into lines before a webfont loads. Desktop preview looks correct, but render workers produce different line wrappers.

**Expected decision:** Block timeline construction until the approved font is ready, establish intentional line width/breaks, split afterward, and revert/rebuild wrappers for responsive variants. Freeze font assets locally and test clean render workers.

**Scoring, 8:**

- 2: identifies font metrics as the cause;
- 2: waits for fonts before splitting;
- 2: handles responsive rebuild/revert;
- 1: freezes the font locally;
- 1: adds repeated clean-render verification.

### 8. Forced morph

**Scenario:** A route path and a protected logo morph through a visibly tangled midpoint, but the final frame looks correct.

**Expected decision:** Do not accept the morph merely because the endpoint passes. Review path correspondence and geometry; simplify only with brand approval. If a clean morph cannot preserve the approved mark, use a match cut, mask, or crossfade.

**Scoring, 7:**

- 2: treats midpoint silhouette as a production defect;
- 2: protects approved geometry;
- 2: proposes a non-morph fallback;
- 1: includes midpoint frame QA.

## Applied tasks

### 9. Author a deterministic animation plan

**User request:** "Build a five-second 9:16 launch card. Reveal `One queue. Every signal.` word by word, draw a small proof line, then settle on a CTA. It will render at 30 fps in a browser-based video tool."

**Expected approach:** Produce an implementation-ready plan with exact timing, stable selectors/layers, a finite paused timeline, semantic labels, SplitText and DrawSVG only if available and reviewed, frame-derived seeking, font readiness, readable holds, reduced-motion treatment, cleanup, and representative review frames.

**Scoring, 18:**

- 3: exact five-second beat plan with readable holds;
- 2: appropriate plugin choices without unrelated plugins;
- 3: paused timeline driven by frame/fps;
- 2: semantic labels/relative placement;
- 2: font and split-wrapper lifecycle;
- 2: reduced-motion variant;
- 2: flashing and text-legibility constraints;
- 2: frame-sampling and repeated-render QA.

**Critical failures:** wrong copy; infinite timeline; wall-clock-only playback; unsafe flashing; no final readable CTA state.

### 10. Diagnose nondeterministic output

**User request:** "Frame 60 changes between renders. The scene uses a random stagger origin, an async API response, an `onComplete` callback that appends DOM, and a timeline that starts playing on load. Fix the design."

**Expected approach:** Freeze API data before composition, replace or seed/precompute randomness, build DOM before timeline capture, remove non-idempotent callback mutation, pause immediately, and seek from requested frame. Verify frame 60 across clean runs and backward/out-of-order seeks.

**Scoring, 12:**

- 2 each for correcting random, network, callback DOM mutation, and autoplay causes;
- 2: verifies repeat capture of frame 60;
- 2: verifies backward/out-of-order seeks.

**Critical failure:** fixes only one cause and declares determinism solved.

### 11. Review a licensed interactive animation product

**User request:** "We're building a no-code visual animation editor powered by GSAP and selling subscriptions. The docs repo is MIT. Can we ship?"

**Expected approach:** Refuse to give unconditional clearance. Distinguish documentation from runtime licensing, identify the current Standard No Charge license restriction relevant to competing visual animation builders, ask for deployment/business details, and route the use to Webflow/GSAP or qualified counsel before shipping. Continue offering architecture planning that does not assume permission.

**Scoring, 9:**

- 3: no unconditional clearance;
- 2: correct license distinction;
- 2: identifies the directly relevant restricted-use category;
- 2: gives a practical escalation path.

**Critical failure:** says MIT documentation automatically permits the product.

## Evaluation integrity checks

The evaluated response must stand on the published skill alone. Do not reward references to this file. Do not expose these expected answers or rubrics before capturing the response. Applied tasks should be scored for production reasoning and actionable specificity, not verbatim similarity.