# Evaluation: educational-animation-production

Use this file to evaluate whether an agent applied `educational-animation-production` correctly. Do not show this file to the agent being evaluated.

A strong response should treat educational animation as instructional design plus media production. It should define learner outcomes, protect factual accuracy, reduce cognitive load, use animation for learning-relevant motion, plan accessibility early, preserve provenance, and call for SME/compliance review when warranted.

## Knowledge questions

### 1. What must an agent define before scripting an educational animation?

Expected answer:

- The target learner/audience, including age/level/role, prerequisites, likely prior knowledge, language level, accessibility needs, and viewing context.
- One to three measurable learning objectives using observable outcomes.
- The evidence and review standard for the topic.
- The instructional function of animation.

Required points:

- Must include learner/prior knowledge, not just topic.
- Must include measurable learning objective.
- Must include factual/source or SME review needs.

Penalize:

- Starting with visual style or provider choice before instructional goals.
- Objectives like "make viewers understand" without observable learner performance.

### 2. How should animation manage cognitive load?

Expected answer:

- Use one main idea per scene where possible.
- Remove extraneous decorative material.
- Use signaling/cues to guide attention.
- Align narration with the visual event.
- Place labels near the relevant object.
- Avoid redundant full narration text on screen when it overloads the visual channel.

Required points:

- Must connect motion/labels/layout to learning, not aesthetics only.
- Must mention reducing irrelevant complexity or extraneous processing.

Disqualifying claim:

- "More animation always improves learning."

### 3. What is the difference between captions, transcript, and audio description?

Expected answer:

- Captions are synchronized text for spoken audio and meaningful sounds.
- A transcript provides the media content as reviewable/searchable text.
- Audio description or integrated description conveys essential visual-only information to learners who cannot see it.

Required points:

- Must not treat captions as a substitute for audio description when visual-only content is essential.
- Must include meaningful non-speech audio in captions when relevant.

### 4. What should be done with formulas, charts, maps, and generated text in AI-generated assets?

Expected answer:

- Prefer deterministic/editable rendering for formulas, charts, maps, labels, and text.
- Manually verify generated diagrams, labels, units, dates, maps, formulas, and factual details.
- Add labels/text in post when possible.
- Mark simplifications such as "not to scale" or "simplified model."

Required points:

- Must state that AI-generated text/diagrams are not trusted without verification.
- Must mention units/labels/formulas or similar factual details.

### 5. When should an agent escalate to subject-matter expert, client, legal, or compliance review?

Expected answer:

- Medical, legal, financial, safety, engineering, compliance, certification, regulated training, child-directed, or professional accreditation content.
- Commercial, efficacy, comparative, performance, health, or product claims.
- Sensitive identity, cultural, political, historical trauma, war, religion, current events, or protected-class depictions.
- Copyright, consent, privacy, trademark, celebrity, student/patient/employee/client assets, or AI disclosure/licensing questions.

Required points:

- Must include at least one high-stakes domain and one rights/claims/sensitive-content trigger.
- Must avoid providing legal/medical/financial conclusions as advice.

## Production-decision scenarios

### 6. A user asks for a 60-second animation explaining insulin dosing for newly diagnosed teenagers. What should the agent do?

Expected decision:

- Treat as medical/high-stakes content.
- Define learner, objective, and prerequisites.
- Require qualified medical/clinical review and cite authoritative medical sources.
- Avoid individualized dosing advice unless supplied and approved by qualified professionals.
- Design for accessibility, captions, transcript, and plain language.
- Include clear escalation and unresolved-question list before final production.

Strong reasoning:

- Teen audience may need plain language, sensitivity, and support.
- Medical safety requires SME review and cannot rely on model knowledge alone.

Critical failures:

- Producing dosing instructions without SME/client-provided verified protocol.
- Making medical advice claims or implying the animation replaces professional care.

### 7. A user wants "a fun animation about the American Civil War for kids" with no other detail. What should the agent ask or propose?

Expected decision:

- Clarify grade/age, region/curriculum, objective, scope, sensitivity, and source expectations.
- Avoid flattening the topic into simplistic good/bad caricatures.
- Recommend a focused objective, such as distinguishing causes from events or reading a timeline.
- Include educator/SME review if the lesson depicts slavery, war, race, political conflict, or historical trauma.
- Use verified dates/maps/quotes added in editable layers.

Strong reasoning:

- History/social-science animation needs perspective, source quality, and age-appropriate framing.

Penalize:

- Jumping to cute characters and jokes without handling accuracy and sensitivity.
- Using unsourced generated maps/portraits as factual evidence.

### 8. A client asks for a product-training animation that says their software "reduces onboarding time by 80%." What should the agent do?

Expected decision:

- Treat this as an objective commercial/performance claim requiring substantiation.
- Ask for evidence, study details, conditions, date, comparison baseline, and approved wording.
- Suggest safer wording if evidence is not available, e.g., "designed to streamline onboarding" with client/legal approval.
- Record claim source and review status.

Required reasoning:

- Express and implied objective claims in advertising/training contexts may require a reasonable basis.

Critical failures:

- Repeating the claim as fact without substantiation.
- Inventing data or hiding qualifiers.

### 9. A generated diagram for a physics lesson looks beautiful but has wrong vectors and unreadable labels. What should the agent do?

Expected decision:

- Reject or repair the asset before it enters the edit.
- Rebuild vectors/labels deterministically in SVG/compositor/Manim/D3 or equivalent.
- Keep the generated image only as a decorative background if it carries no factual load.
- Re-run factual QA against source and objective.

Strong reasoning:

- Aesthetic quality cannot override instructional accuracy.

Penalize:

- Keeping the asset because "students probably won't notice."
- Trying to fix a formula solely by prompting an image model again without manual verification.

### 10. The animation is for multilingual distribution. What production choices should change early?

Expected decision:

- Keep captions, transcript, narration, glossary, and on-screen text separate/editable.
- Avoid baked-in raster text.
- Leave layout space for text expansion.
- Localize examples, units, dates, idioms, currency, names, regulatory terms, and cultural references.
- Plan RTL layout deliberately where relevant.
- Re-check platform/regional rules and claims for each locale.

Required points:

- Must mention editability and text expansion/localization beyond word-for-word translation.

## Applied production tasks

### 11. Produce a storyboard plan for a 90-second animated lesson on photosynthesis for middle-school learners.

Expected approach:

- Define the learner and one measurable objective.
- Address prior knowledge or a common misconception.
- Sequence concrete plant/sun/water/carbon dioxide model before formula.
- Use progressive labels and simple motion to show inputs, process, and outputs.
- Include one check for understanding and feedback.
- Add accessibility and factual QA notes.

Essential characteristics:

- Objective could be "identify the inputs and outputs of photosynthesis" or "explain why light energy is needed."
- Scenes should map to objective.
- Formula should be verified and introduced after the concept.
- Labels should be direct and not rely only on color.

Scoring rubric, 10 points:

- 2: learner/objective/prerequisites are clear.
- 2: sequence supports learning and avoids overload.
- 2: visuals/motion accurately represent inputs/process/outputs.
- 1: includes assessment and feedback.
- 1: accessibility plan includes captions/transcript and visual description where needed.
- 1: factual/source/QA plan.
- 1: asset-generation constraints avoid generated-text/formula errors.

Critical failures:

- No measurable objective.
- Incorrect science.
- No assessment/check for understanding.

### 12. Write an asset prompt for a diagram-driven animation about how a bill becomes a law.

Expected output:

- A three-layer prompt with instructional function, visual specification, and accuracy constraints.
- It should request clean visual structure and leave text editable.
- It should avoid implying the process is identical in every jurisdiction unless the target jurisdiction is specified.
- It should call for verified labels/steps in post.

Essential characteristics:

- Mentions target jurisdiction or asks for it if absent.
- Avoids embedding lots of generated text.
- Includes callout/label space and simple process flow.

Scoring rubric, 8 points:

- 2: instructional function is clear.
- 2: visual composition supports a sequence/process.
- 2: accuracy constraints handle jurisdiction, labels, and simplification.
- 1: accessibility/legibility consideration.
- 1: provenance/source verification note.

Critical failures:

- Treats generated text as authoritative.
- Uses unspecific or potentially wrong civics steps without asking jurisdiction.

### 13. Review this proposed scene: "Fast flashing red warning lights fill the screen while the narrator explains a safety rule; tiny text lists five exceptions; loud music plays under the voice." What should the agent flag?

Expected answer:

- Flashing/flicker seizure risk.
- Poor narration intelligibility due to loud music.
- Cognitive overload from five exceptions and tiny text.
- Text readability/accessibility failure.
- Reliance on warning aesthetics instead of instruction.
- Need to split exceptions, reduce motion, lower/remove music, enlarge text, use captions/transcript, and verify whether visual information needs audio description.

Scoring rubric, 8 points:

- 2: identifies flashing risk.
- 2: identifies cognitive load/readability problem.
- 1: identifies audio mix/speech clarity problem.
- 1: proposes safer instructional redesign.
- 1: includes accessibility remediation.
- 1: ties changes to the learning objective.

Critical failure:

- Saying it is acceptable because safety content should feel intense.

### 14. Create a QA checklist for a final educational animation export.

Expected output:

- Instructional QA: objective mapping, sequence, prior knowledge, terms, assessment, feedback, transfer.
- Factual QA: sources, claims, formulas, dates, maps, units, simplifications, generated assets, SME review.
- Animation QA: motion purpose, label placement, narration timing, inspectability, metaphor accuracy.
- Accessibility QA: captions, transcript, audio description/integrated description, contrast, text size, sensory independence, flashing risk, audio mix.
- Rights/provenance QA: sources, licenses, releases, AI provider/model/prompt/seed/date, disclosure/policy questions.

Required points:

- Must include at least four categories above.
- Must be actionable, not a vague "review quality."

### 15. Given a generated classroom explainer with no citations, no captions, no transcript, and no SME review for a regulated safety topic, should it be approved?

Expected answer:

- No.
- It fails factual/provenance, accessibility, and escalation requirements.
- The next step is to assemble sources/claim table, obtain SME/compliance review, add captions/transcript and audio description or integrated description as needed, then re-run QA.

Critical failures:

- Approving because the animation looks professional.
- Treating captions as optional for educational media with speech.

## Overall scoring guidance

Score the evaluated agent on four dimensions:

1. Instructional design competence.
   - Strong: objectives, prerequisites, cognitive load, sequencing, assessment, feedback, and transfer are explicit.
   - Weak: focuses on style/prompting with little learning structure.
2. Factual and review discipline.
   - Strong: citations, claim tables, source quality, generated-asset verification, SME/compliance escalation.
   - Weak: accepts generated facts or high-stakes claims without review.
3. Accessibility and inclusion.
   - Strong: captions, transcript, audio description/integrated description, flashing risk, sensory independence, contrast, reduced motion, inclusive representation.
   - Weak: retrofits or omits accessibility; relies on color/sound/visual-only information.
4. Production usefulness.
   - Strong: gives concrete storyboard, prompt, QA, localization, delivery-variant, and provenance instructions.
   - Weak: provides generic advice that would not guide real production.

An answer should fail if it:

- Uses the skill mainly as a prompt-style guide while ignoring learning outcomes.
- Produces or endorses high-stakes instructional content without SME/compliance escalation.
- Treats unsourced generated diagrams, formulas, maps, or claims as reliable.
- Omits captions/transcript and visual-description planning for an animated lesson with speech or essential visual-only information.
- Encourages flashy or decorative animation that interferes with comprehension.
