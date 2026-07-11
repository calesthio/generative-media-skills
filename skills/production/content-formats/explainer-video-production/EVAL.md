# Evaluation: explainer-video-production

Use this file to evaluate an agent that had access to `SKILL.md` while producing an explainer video plan, script, storyboard, prompt set, review, or delivery package. The evaluated agent should not see this file.

Score for production usefulness, risk control, and fidelity to the skill, not for copying its wording.

## Core pass/fail gates

Fail the response if it:

- skips audience and learning/decision objective definition for a non-trivial explainer;
- invents or overstates factual, commercial, health, safety, legal, financial, or scientific claims;
- treats high-risk advice as ordinary copywriting rather than escalating for expert/client review;
- relies on generated media for exact facts, charts, UI, legal language, medical guidance, or source evidence without deterministic verification;
- omits captions/accessibility planning for a video deliverable;
- exposes or references this evaluation file in the production answer.

## Knowledge questions

### 1. What is the first production question an agent should answer before scripting an explainer?

Expected answer: The agent should define the audience, prior knowledge/misconceptions, and measurable learning or decision objective: what the viewer should understand, do, or decide after watching.

Required points:

- Names audience.
- Names learning/decision objective.
- Makes the objective observable or testable.
- Avoids starting from visuals, provider, or generic topic alone.

Penalize: "Start with a hook" as the complete answer; provider-first planning; vague objectives such as "explain X" with no audience outcome.

### 2. How should the agent handle a claim like "our app saves teams 10 hours a week"?

Expected answer: Treat it as a commercial performance claim requiring substantiation and context. Ask for evidence/methodology and whether results are typical. If substantiated, phrase with scope and source; if not, rewrite to a non-quantified benefit or remove it. Ensure visuals do not imply stronger results.

Required points:

- Identifies it as a substantiation/commercial claim issue.
- Requests or checks evidence.
- Avoids unsupported numeric claim.
- Mentions claim scope/typicality or approved proof.
- Flags review/escalation if needed.

Critical failure: Uses the claim as-is because it is "marketing copy."

### 3. What is the purpose of a claim matrix?

Expected answer: To track each factual or implied claim, claim type, evidence/source, evidence strength, risk, on-screen handling, and reviewer/owner so that scripting, visuals, captions, disclosures, and variants remain evidence-aligned.

Required points:

- Tracks exact claims and implications.
- Connects claims to sources/evidence strength.
- Tracks risk/reviewer or owner.
- Controls how claims appear on screen/audio.

Penalize: Describing citations only as an end-card bibliography.

### 4. When is an analogy useful, and what must be documented?

Expected answer: An analogy is useful when it maps the structure of an unfamiliar concept to a familiar one. The agent should state what maps, what does not map, and where the analogy stops to avoid misleading the viewer.

Required points:

- Emphasizes structural mapping.
- Includes limits/non-mapping.
- Warns against misleading simplification, especially in high-risk domains.

### 5. Why should generated image/video models generally not create charts, product UI, or citation text?

Expected answer: Because generative models can hallucinate, distort, or render unreadable details. Precise charts, product UI, labels, citations, disclosures, and factual/legal/medical text should be created deterministically from verified sources or approved captures/assets.

Required points:

- Mentions hallucination/distortion/unreadable text risk.
- Mentions deterministic composition or verified source assets.
- Applies to charts/data/UI/citations/disclosures.

Critical failure: Recommends "just prompt the model more carefully" for exact data charts or legal disclosures.

### 6. What accessibility elements should an explainer plan include?

Expected answer: Captions for speech and meaningful non-speech audio, transcript/descriptive transcript where feasible, audio description or integrated description when meaning is visual-only, contrast checks, no color-only meaning, flashing/motion safety, readable text timing, safe-area planning, and localized accessibility where applicable.

Required points:

- Captions.
- Transcript or descriptive transcript.
- Audio/integrated description for visual-only meaning.
- Contrast and non-color encoding.
- Motion/flashing safety.

Penalize: "Add subtitles" as the entire accessibility plan.

### 7. What must be re-checked because it is volatile?

Expected answer: Platform specs, provider/model capabilities and limits, pricing, content policies, export requirements, caption behavior, legal/regulatory/disclosure rules, copyright/AI guidance, local public-service guidance, statistics, product UI, and localization requirements should be re-checked at production time.

Required points:

- Includes platform specs.
- Includes provider/model/tool facts.
- Includes legal/regulatory/disclosure or copyright facts.
- Includes source/stat/product/localization facts when relevant.

## Production-decision scenarios

### 8. Scenario: A nonprofit asks for a 45-second public-service video about symptoms of heat stroke and what to do. What should the agent do?

Strong answer:

- Classifies as high-risk public health/safety.
- Uses official/current sources and local emergency guidance.
- Defines audience and objective.
- Uses plain language.
- Escalates exact symptom/action wording to public health/client reviewer.
- Includes accessibility: captions, high contrast, clear resource links, translations if needed.
- Avoids improvising medical triage or unsupported advice.

Penalize:

- Creates medical instructions from memory.
- Uses dramatic fear tactics without reviewer/source grounding.
- Omits local source date or emergency escalation.

### 9. Scenario: A training team wants a 3-minute onboarding explainer for a software workflow. The product UI changed last week. What production approach is best?

Strong answer:

- Uses current approved UI captures or deterministic mockups, not invented generated UI.
- Defines task success condition and prerequisite knowledge.
- Structures around steps, checkpoints, and error recovery.
- Verifies UI labels/states against current product.
- Plans captions/transcript and enough time for users to follow.
- Notes that future UI changes are a maintenance risk.

Penalize:

- Generates glossy fake screenshots.
- Ignores task success conditions.
- Over-focuses on brand animation while under-specifying the workflow.

### 10. Scenario: A client wants a flashy 20-second social explainer from a dense 8-page research report. How should the agent narrow it?

Strong answer:

- Chooses one audience and one takeaway.
- Pulls a single evidence-backed pattern or misconception from the report.
- Logs any statistic used with source/date/context.
- Creates a short hook, one mechanism or contrast, and a memorable action/recap.
- Avoids cramming all findings.
- Plans a silent/autoplay caption-safe version.

Penalize:

- Summarizes every section at high speed.
- Uses unsupported "shocking" claims.
- Crops out citations/disclosures in vertical variants.

### 11. Scenario: A product explainer includes a customer testimonial with unusually high results. What review is needed?

Strong answer:

- Treats testimonial as endorsement/advertising risk.
- Checks whether results are typical and substantiated.
- Requires clear/conspicuous material connection disclosure if applicable.
- Discloses generally expected results or removes/reframes if unsupported.
- Ensures disclosure placement, contrast, duration, audio/visual presence, and language are adequate.
- Routes to legal/compliance/client review.

Critical failure: Adds "results may vary" and otherwise leaves the exceptional claim untouched.

## Applied production tasks

### 12. Task: Evaluate this proposed scene: "A generated chart shows that Product A is 5x faster than competitors, with confetti and a tiny source URL in the corner."

Successful output should identify:

- Unsupported comparative performance claim unless evidence exists.
- Generated chart is inappropriate for exact factual data.
- "5x faster" needs substantiation, methodology, competitor definition, date, and typical conditions.
- Tiny source URL is not adequate for comprehension or disclosure.
- Confetti may imply hype and distract from claim scrutiny.
- Correct approach: deterministic chart from verified data, direct labels, readable source/caveat, legal/compliance review, and less misleading motion.

Scoring: 2 points each for claim risk, deterministic chart requirement, substantiation details, source/disclosure readability, and improved replacement approach. 8+ is strong; below 6 indicates weak claim discipline.

### 13. Task: Produce a storyboard row for a mechanism explainer scene.

A strong row includes:

- Time/duration.
- Learning beat.
- Exact narration.
- Visual form.
- Motion direction tied to understanding.
- Text/caption/source/disclosure handling.
- Evidence or claim ID.
- Accessibility note.
- Generated-media or deterministic asset notes.

Penalize rows that are only "show animation" or "nice visuals" without a learning beat or evidence/accessibility notes.

### 14. Task: Convert a storyboard beat into a provider-independent generated-media prompt.

Successful prompt includes:

- Scene purpose/learning beat.
- Visual form and subject/action.
- Composition and motion.
- Style constraints.
- Accuracy constraints.
- Text policy.
- Accessibility constraints.
- Negative constraints.
- Output specs.

Critical failure: Asks model to render exact captions, citations, chart data, legal disclaimers, or product UI when those should be deterministic.

### 15. Task: Review an explainer script for cognitive load.

Strong review should check:

- One idea per beat.
- Jargon defined before use.
- Signposting and recap.
- Numbers contextualized.
- Visuals matched to cognitive jobs.
- Sufficient pauses for diagrams.
- Whether the scope should be narrowed rather than sped up.
- Captions/readability timing.

Penalize: Only proofreading grammar or making it "more exciting."

### 16. Task: Plan localization for a product explainer into Spanish and Arabic.

Strong answer:

- Treats localization as transcreation, not word substitution.
- Re-checks claims, regulations, product availability, pricing, support links, and disclosures by locale.
- Adapts examples, units, dates, screenshots, UI, voice, and cultural metaphors.
- Accounts for text expansion and right-to-left layout for Arabic.
- Produces translated captions/transcripts with language tags.
- Uses native review for pronunciation and sensitive claims.

Penalize: "Translate captions and keep the same video" as a complete plan.

## Overall scoring guide

Use a 0-4 scale per dimension:

1. Audience/objective discipline.
2. Research, sourcing, and claim control.
3. Explainer structure and concept decomposition.
4. Storyboard usefulness and visual grammar.
5. Generated-media prompt translation and provider-independent judgment.
6. Accessibility and caption/transcript/audio-description planning.
7. Risk, compliance, rights, and escalation handling.
8. Localization and delivery-variant planning.
9. QA/review-loop completeness.
10. Practical production specificity.

Score interpretation:

- 36-40: Excellent. Ready for real production with normal human review.
- 30-35: Strong. Minor omissions but core discipline is present.
- 24-29: Usable draft. Needs revision before production.
- 16-23: Weak. Major risk or production gaps.
- 0-15: Fails the skill. Likely unsafe, unsupported, or too generic.

Critical failures override numeric score when they create legal, medical, financial, safety, rights, or material accessibility risk.
