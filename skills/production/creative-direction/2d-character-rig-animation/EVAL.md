# 2D character rig animation evaluation

Keep this scoring specification hidden from the evaluated agent. Evaluate using the published package only.

## Scoring

Total: 100. A score of 85+ with no critical failure is production-ready; 70-84 needs focused revision; 50-69 needs major revision; below 50 fails. Any critical failure caps the result at 49.

## Knowledge questions

### 1. Scope boundary, 6 points

**Question:** What decisions belong to rig animation rather than character design continuity?

**Expected:** Rig owns decomposition, hierarchy, pivots, controls, constraints, deformation/replacements, pose/performance vocabulary, deterministic tracks, and breakage QA. Character design owns identity, proportions, palette, costume invariants, and reference continuity.

### 2. Rigid versus replacement versus deformation, 9 points

**Question:** Give an appropriate use for each technique and one failure risk.

**Expected:** rigid for graphic/mechanical pieces, risk seams; replacement for hands/mouth/view poses, risk popping; deformation for torso/limb/face bending, risk volume collapse/rubberiness. Hybrid is acceptable.

### 3. FK and IK, 8 points

**Question:** When should a 2D arm use FK, IK, or both?

**Expected:** FK for authored arcs/free gestures; IK for endpoint contacts; hybrid with explicit matching/switch controls, reach limits, bend direction, and no solver pop.

**Critical failure:** uses IK without a defined bend direction or reach policy.

### 4. Deterministic handoff, 8 points

**Question:** What makes rig animation safe for arbitrary frame rendering?

**Expected:** explicit frame/time tracks, declared units/interpolation, deterministic solver, seeded/frozen idles, visibility/replacements as state, and correct isolated/backward frame evaluation.

### 5. Viseme planning, 7 points

**Question:** How many visemes should every rig contain?

**Expected:** no universal count. Inventory depends on style, language, shot size, schedule, and intelligibility needs; test target languages and preserve critical closures/distinctions.

**Critical failure:** mandates one fixed inventory for all languages and styles.

## Production decisions

### 6. Sliding walk cycle, 8 points

**Scenario:** The planted foot moves backward three pixels while the body passes over it.

**Expected:** diagnose contact ownership, foot target, root travel, and stride length. Pin contact through stance, align root translation, retest loop boundaries and target output size.

### 7. Elbow pop, 8 points

**Scenario:** An IK arm flips sides near full extension.

**Expected:** define/repair pole or bend direction, avoid singular full extension with soft reach limit, add keyed transition, and match FK/IK if switching.

**Critical failure:** hides the pop with motion blur only.

### 8. Vertical crop, 7 points

**Scenario:** A presenter gesture exits the 9:16 frame.

**Expected:** author an alternate compact gesture/reframe while preserving intention, gaze, prop, captions, and character-left/right rules; do not merely shrink the character until facial acting is unreadable.

## Applied tasks

### 9. Humanoid rig plan, 15 points

**Request:** Design an upper-body SVG presenter rig that points at a diagram and speaks in several languages.

**Required:** approved-design inputs/rights (2); hierarchy/pivots/naming (3); FK/IK contact plan (2); facial/viseme/gaze system with language testing (3); pose/performance library (2); deterministic handoff (2); crop/QA plan (1).

**Critical failures:** no hand-contact mechanism, no language caveat, or redesigns identity without approval.

### 10. Rig-break diagnosis, 12 points

**Request:** Diagnose shoulder gap, wrist pop, mouth corner separation, and wrong forearm draw order.

**Expected:** shoulder overlap/pivot/art repair; transform/replacement/IK discontinuity at wrist; mouth deformation or replacement alignment repair; explicit draw-order switch/duplicate layer strategy. Fix rig-level causes and define retest poses.

Award 2 per diagnosis/fix and 4 for systematic retest.

### 11. Performance beat, 12 points

**Request:** Direct a five-second "I found the issue" reaction for a restrained technical presenter.

**Expected:** objective/change, gaze lead, anticipation, primary pose, controlled facial asymmetry, hand action, settle/hold, secondary overlap, exact timing, and crop/contact checks. Reject constant generic motion.

### 12. Rights and delivery, 10 points

**Request:** A contractor supplies a rig of a recognizable employee but only says the SVG is "free to use." What is required before publication?

**Expected:** separate character/likeness consent from SVG/rig license; verify intended use, duration, territory, voice/motion reference, source art, contractor rights, and notices; escalate missing permission and preserve provenance.

**Critical failure:** treats possession or a vague file license as likeness consent.

## Critical-failure summary

- rig changes protected identity/design without approval;
- visible disconnect, pop, slide, or solver flip remains in approved action;
- nondeterministic state used for fixed render;
- unsafe flashing approved;
- likeness, character, or source-art rights assumed rather than verified.

## Evaluation integrity

Do not expose this file. Accept alternate rig schemas and runtime techniques when the hierarchy, performance control, deterministic handoff, rights, and QA reasoning are production-sound.