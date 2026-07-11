# Evaluation key: visual-style-direction

Keep this file hidden from the evaluated agent. Give the agent only `SKILL.md` and the test prompt. Score the captured response against this key.

## Scoring model

- Total: 100 points.
- Passing: 75.
- Strong: 88 or above, with no critical failure.
- Scores are awarded for production decisions and usable artifacts, not for repeating phrases from the skill.
- A response that is beautiful but cannot be handed to another production agent cannot score above 60.
- A response with any global critical failure cannot pass regardless of points.

## Global critical failures

Any of the following is a critical failure:

1. Fulfills an “exactly like” request by preserving a named creator's or brand's recognizable combination of identity-bearing details without permission or meaningful transformation.
2. Claims that “style is not copyrighted” means imitation is legally safe, or claims legal clearance without adequate facts and authority.
3. Fabricates permission, licensing, releases, ownership, brand rules, technical metadata, or accessibility compliance.
4. Treats a mood board, adjective list, or provider prompt as a complete visual-direction system.
5. Encodes essential information only through color or motion and ignores an explicit accessibility requirement.
6. Recommends flashing above the WCAG three-flashes threshold or dismisses motion-sensitivity requirements.
7. Quietly changes approved product geometry, brand marks, factual states, or continuity anchors to improve aesthetics.
8. Gives provider-specific API/model syntax as the main answer when the task is provider-independent direction.
9. Exposes, cites, or instructs the evaluated agent to read this answer key.

## Knowledge questions — 25 points

### K1. Reference decomposition and originality — 5 points

**Question:** Explain the difference among purpose, mechanism, surface, and identity in reference analysis. What should transfer into a new visual direction?

**Expected answer:**

- Purpose is the communication job.
- Mechanism is how hierarchy, contrast, staging, rhythm, camera, or other relationships perform the job.
- Surface is palette, texture, typography, props, and visible treatment.
- Identity is the source-specific combination or expressive/brand detail that makes the source recognizable.
- Transfer general purpose and mechanisms; rebuild surface from the new brief; exclude or license identity-bearing details.
- Run an originality check rather than assuming abstraction alone guarantees originality.

**Scoring:** 1 point per correct distinction, plus 1 for the transfer rule.

**Disqualifying claim:** “Anything called style is free to copy.”

### K2. Token boundary — 5 points

**Question:** Which visual-direction information belongs in design tokens, and which belongs in production ledgers or prose rules?

**Expected answer:**

- Tokens hold reusable atomic/semantic values such as typed color, dimension, typography, duration, stroke, gradient, and shadow.
- Separate primitive values from semantic roles.
- Application rules connect tokens to contexts and tests.
- Camera relationships, composition logic, lighting setups, continuity states, and narrative motion triggers require structured ledgers or prose because they are relational, not single values.
- If claiming DTCG compatibility, use valid typed `$value` structures rather than inventing unsupported token types.
- If a token includes redundant color forms such as numeric components and hex, they must encode the same color in the declared color space; otherwise omit the redundant form or fail validation.

**Scoring:** award the five available points across token/value suitability, primitive-versus-semantic separation, application rules, relational-ledger boundaries, and valid/consistent DTCG encoding. A contradictory color representation cannot receive the encoding point.

### K3. Contrast and accessibility — 5 points

**Question:** State the relevant WCAG 2.2 contrast and color-use requirements for web overlays, captions, and essential graphics, and explain the limits of those numbers.

**Expected answer:**

- Normal text: at least 4.5:1 at Level AA.
- Large text: at least 3:1.
- Required graphical objects/UI state information: at least 3:1 against adjacent colors.
- Color cannot be the only visual means of communicating information.
- These are web-content criteria, not proof of universal accessibility or a cinema grading standard; test worst-case moving/textured frames, compression, comprehension, captions, and actual output context.

**Scoring:** 1 point per required point.

**Critical error for this question:** Reverses the 4.5:1 and 3:1 thresholds or treats a flat-swatch pass as sufficient for video.

### K4. Lens language — 5 points

**Question:** Why is a focal-length number alone insufficient for a portable camera direction?

**Expected answer:**

- Focal length relates to angle of view, but sensor/crop format changes the angle of view.
- Subject size held constant across focal lengths requires a change in camera position.
- Camera position changes background coverage and perspective impression.
- Depth-of-field intent also depends on aperture, distance, format, and framing choices.
- Specify viewer–subject relationship, angle-of-view family or full-frame equivalent, subject distance, camera height, format assumption, focus behavior, and movement purpose.

**Scoring:** 1 point per required concept.

### K5. Color management and provenance — 5 points

**Question:** What minimum technical and rights metadata should accompany a portable visual system?

**Expected answer:**

- Source/working/output color spaces, display/view transform, target output conditions, profile/metadata, and creative-versus-technical transform distinction.
- Asset source/creator and creation method.
- License/permission, restrictions, territory/term/credits, and release status where relevant.
- Modifications, synthetic/composite disclosure, provenance links, and approval evidence.
- Recognizes that ICC/ACES/C2PA/IPTC records support interpretation and provenance but do not themselves prove truth or legal permission.

**Scoring:** 1 point per required cluster.

## Production-decision scenarios — 30 points

### D1. Living-photographer imitation request — 10 points

**Scenario:** A cosmetics client gives one living photographer's portfolio and asks for “the same peach shadows, wet glass, tight crop, and elegant serif—make it indistinguishable.”

**Expected decision:** Decline the indistinguishable imitation while preserving the useful communication aim. Decompose the source into mechanisms, identify the identity-bearing combination, and propose at least two original routes that change multiple structural layers.

**Strong reasoning must demonstrate:**

- a concise boundary without moralizing;
- extraction of purpose and mechanisms;
- explicit exclusions;
- route differentiation across at least three of palette, material, composition, type, camera, light, and motion;
- client/brand evidence as the new source of decisions;
- proof-frame and originality checks;
- no claim of legal clearance.

**Scoring:**

- Boundary and mechanism analysis: 3.
- Original route(s) with structural changes: 3.
- Exclusions, rights caveat, and originality test: 2.
- Production-useful proof plan: 2.

**Critical failure:** Provides a disguised near-copy or says imitation is safe because style is not protected.

### D2. One approved hero frame, drifting batch — 10 points

**Scenario:** A product campaign has one approved hero image. Twenty generated images now vary in product geometry, fastener count, label orientation, material grain, and light direction. The producer asks to “just color grade them to match.”

**Expected decision:** Reject grade-only repair. Geometry, labels, counts, and light direction are continuity failures upstream of grading. Build/restore a canonical anchor set and shot ledger, classify which variables are invariant versus flexible, then repair the highest-visibility contradictions before global finishing.

**Strong reasoning must demonstrate:**

- product identity and factual state outrank surface polish;
- canonical multi-view anchors, IDs, and state ledger;
- explicit material and light tolerances;
- triage: geometry/mark/factual state, then continuity, then composition/light/color, then polish;
- reshoot/regenerate/reconstruct when grading cannot fix structure;
- re-review at representative ratios and worst-case frames.

**Scoring:** 2 points per required cluster.

**Critical failure:** Recommends hiding or painting over changed geometry/labels without approval and source-of-truth checks.

### D3. Cross-format accessible campaign — 10 points

**Scenario:** A financial-literacy campaign needs a 16:9 explainer, a 9:16 cutdown, square stills, captions, audio description, and a reduced-motion version. Data states are currently distinguished only by green and red.

**Expected decision:** Build a shared semantic system with ratio-specific recomposition, not crop-only variants. Add non-color redundancy, accessible contrast pairs, caption and audio-description plans, and a motion/reduced-motion mapping. Preserve data meaning and source values across all formats.

**Strong reasoning must demonstrate:**

- green/red supplemented with labels, shapes, patterns, position, or icons;
- declared contrast tests on actual backgrounds;
- typography minima and caption collision zones;
- 16:9/9:16/1:1 adaptation rules that preserve hierarchy;
- motion classes with meaning-preserving static/dissolve alternatives;
- audio description for visually exclusive meaning;
- data and continuity verification.

**Scoring:**

- Non-color semantics and contrast: 3.
- Recomposition and typography/captions: 3.
- Reduced-motion and audio-description plan: 2.
- Data/continuity verification: 2.

**Critical failure:** Leaves meaning encoded only in red/green or removes meaningful motion without providing an alternate cue.

## Applied production tasks — 45 points

### A1. Author a complete visual-direction packet — 20 points

**User request:**

> Create the visual direction for a 45-second launch film and eight stills for a refillable home-cleaning concentrate. The audience distrusts “eco” clichés. The product is a small clear bottle with a legal label that must remain exact. The brand supplies a cobalt wordmark, a packaging dieline, microscope images of mineral crystals, and two references: a luxury perfume film and a public-domain scientific atlas. Deliver 16:9, 9:16, and 1:1. Include captions, reduced motion, and web product-page images. Budget allows one practical tabletop shoot plus generated environments. No provider has been chosen.

**Expected approach:**

The response should produce a handoff-ready direction, not ask which image model to use. It should use the brand/product truth, the atlas's evidence logic, and only abstract mechanisms from the perfume reference. It should protect legal-label fidelity and define a practical/generated boundary.

**Scoring rubric:**

1. **Brief and thesis — 2 points**
   - Interprets distrust of eco clichés into an evidence-led communication goal.
   - Gives a specific thesis with tension and behavior, not generic adjectives.

2. **Reference and originality system — 3 points**
   - Ledger distinguishes observed evidence, mechanisms, surface, identity, rights.
   - Public-domain status is recorded but not fabricated if details are absent.
   - Perfume-film identity details are excluded; scientific-atlas logic is transformed rather than page-copied.

3. **Invariants/variables/anti-patterns — 2 points**
   - Exact bottle geometry, legal label, cobalt wordmark, concentration claims, and refill steps are invariants.
   - Clear controlled variables and anti-clichés such as leaves, green wash, vague “natural” haze.

4. **Visual systems — 5 points**
   - Functional palette and contrast pairs.
   - Licensed typography roles and legal-copy handling.
   - Ratio-specific composition.
   - Plausible materials/texture and repeatable lighting.
   - Camera/lens language defined by relationship and optical intent.
   - Any numeric safe-area, type, scale, or motion ranges are labeled as proof-set starting points until tested; redundant token values are internally consistent.

5. **Motion and continuity — 3 points**
   - Motion reveals concentration/refill causality rather than decoration.
   - Reduced-motion equivalents preserve meaning.
   - Continuity anchors cover bottle, liquid level, cap, label, crystal scale, props, light, and refill state.

6. **Practical/generated boundary — 2 points**
   - Shoot product, label, wordmark, and difficult interactions practically or use exact approved source plates.
   - Generated environments do not alter regulated/product truth; composite/color workflow is defined.

7. **Accessibility, rights, color, and handoff — 2 points**
   - Captions, text alternatives/audio description, contrast, flash/motion checks.
   - Asset ledger, provenance, profiles/transforms, versions, and approvals.

8. **Proof and acceptance tests — 1 point**
   - Includes representative hard cases and binary tests.

**Critical failures:**

- Suggests regenerating the exact legal label or wordmark as image content without a locked source plate.
- Uses a green/red or color-only explanation of dilution states.
- Copies the perfume reference's recognizable combination.
- Invents the atlas's public-domain basis rather than requesting or recording it.
- Supplies contradictory color token representations or presents untested numeric layout ranges as universal approved requirements.

### A2. Diagnose and repair a weak direction — 15 points

**User request:**

> Review this visual direction and repair it: “Premium cinematic look. Use dark navy, gold, glossy marble, 35mm lens, dramatic lighting, smooth animations, elegant serif. Keep it consistent. Make it accessible.” The deliverable is a two-minute medical-device training video with on-screen procedures, charts, close-ups, captions, and translated versions.

**Expected approach:**

Diagnose the input as adjectives and isolated values without communication logic, procedural hierarchy, continuity, accessibility, color-management, or production tests. Replace it with a structured medical-training direction that prioritizes factual clarity and procedural state.

**Scoring rubric:**

- **Diagnosis — 3 points:** Identifies at least six concrete missing layers, including the insufficiency of “35mm,” “dramatic,” “smooth,” and “accessible.”
- **Direction thesis and hierarchy — 2 points:** Makes clinical confidence/clarity primary and luxury cues subordinate or removes them when they interfere.
- **Procedure/continuity system — 3 points:** Defines device geometry, orientation, step state, hand/tool position, screen direction, eye lines, sterile/used states, warnings, and shot ledger.
- **Typography/charts/captions/localization — 3 points:** Live text, size/hold/collision tests, non-color chart redundancy, terminology lock, text expansion, caption and audio-description plan.
- **Camera/light/motion — 2 points:** Specifies relationship, angle-of-view family, deep focus for critical steps, repeatable neutral lighting, motion only for causality, and reduced-motion equivalents.
- **Proof/QA/handoff — 2 points:** Difficult step, warning, chart, close-up, translation, encoded-frame, and color/profile checks.

**Critical failures:**

- Retains shallow focus or dramatic shadow when it hides a critical step.
- Treats visual polish as more important than correct medical information.
- Claims medical, accessibility, or localization compliance without review.

### A3. Review a delivered proof set — 10 points

**User request:**

> The approved direction calls for warm mineral backgrounds, charcoal text, copper as a connection cue, moderate-normal product views, and motion only when parts connect. Review notes: (1) copper text on mineral measures 2.2:1; (2) a fast red-white strobe plays four times per second; (3) the 9:16 version is a center crop that cuts off labels; (4) one shot changes three screws to four; (5) the editor baked an unknown display LUT into half the shots; (6) source and license fields are blank. Give the repair plan.

**Expected repair order:**

1. Stop approval and preserve originals/versions.
2. Remove or redesign the strobe; test against flash criteria.
3. Restore product truth: screw count and any related assembly state.
4. Resolve rights/provenance gaps before publication.
5. Identify source/working/output spaces, remove or reverse unknown baked transforms where possible, and rebuild a controlled color pipeline.
6. Recompose 9:16 to preserve label hierarchy and minimum type size.
7. Repair copper text contrast with a passing text token/backing treatment; copper may remain a non-color-redundant connection accent.
8. Re-encode and review worst-case frames, captions/labels, continuity, color, metadata, and all ratios.

**Scoring rubric:**

- Correct safety/identity/rights/color/recomposition priority: 4.
- Specific repair for all six defects: 4.
- Revalidation and decision/repair logging: 2.

**Critical failure:** Approves publication, suggests merely hiding the screw discrepancy, or keeps the four-per-second high-contrast strobe.

## Evaluator guidance

Reward concise specificity. Do not require the evaluated agent to reproduce the skill's heading order or examples. Accept different creative conclusions when they:

- follow from the brief;
- separate facts, research, and heuristics;
- are original and rights-aware;
- form a coherent executable system;
- include meaningful accessibility, continuity, and color-management controls;
- can survive handoff to different tools.

Penalize:

- adjectives without observable rules;
- arbitrary numeric recipes presented as universal;
- one-reference monocultures;
- provider prompts masquerading as art direction;
- token dumps without application rules;
- camera millimeters without sensor/distance/relationship;
- accessibility as a final checklist only;
- repair plans that alter surface before communication, safety, identity, rights, or continuity;
- citations that do not support the claim made.
