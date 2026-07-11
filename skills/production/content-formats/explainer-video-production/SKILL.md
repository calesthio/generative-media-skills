---
name: explainer-video-production
description: Provider-independent explainer video production for AI agents creating educational, product, concept, nonprofit/public-service, onboarding, training, animated, mixed-media, and short social explainers. Use when an agent must turn a topic, brief, research corpus, product, process, policy, dataset, or complex idea into a factual, accessible, narrated, captioned, storyboarded, generated-media-ready explainer video with claim review, localization, pacing, variants, and QA.
---

# Explainer video production

Produce an explainer only after defining what the audience should understand, believe, decide, or do differently after watching. Treat the video as a learning and decision artifact, not as a sequence of pretty scenes.

This skill is provider-independent. Use the available generation, editing, composition, captioning, and review tools in the host environment, but keep the explainer logic, factual discipline, accessibility, and QA standards intact across providers.

## Non-negotiables

- Start from audience, prior knowledge, and a measurable learning or decision objective.
- Separate documented facts, source-backed inferences, production heuristics, and creative inventions.
- Maintain a claim log for factual, commercial, comparative, health, safety, legal, financial, scientific, and public-service claims.
- Escalate high-risk claims to the client, subject-matter expert, legal/compliance reviewer, medical reviewer, financial reviewer, or policy owner. Do not provide legal, medical, or financial advice.
- Build accessibility into script, storyboard, captions, audio, data visuals, and delivery variants. Retrofitting is weaker and more expensive.
- Re-check volatile provider/platform facts at production time: social aspect ratios, maximum lengths, safe areas, caption behavior, model inputs, model limits, pricing, regional availability, disclosure rules, and rights/licensing terms.
- Never ask an image or video generation model to invent evidence, render precise charts, preserve exact legal/medical/scientific statements, or create readable fine text. Use deterministic layout/composition for facts, citations, captions, tables, UI text, labels, and charts.

## Intake: define the learning contract

Before writing or generating, answer:

- Audience: Who is this for, what do they already know, what do they misunderstand, what language/register do they use, and what accessibility/localization needs are known?
- Objective: What single sentence should the viewer be able to say, do, or decide after watching?
- Use case: education, product, onboarding, training, public-service, fundraising, policy, sales enablement, social awareness, internal change management, or technical concept.
- Success evidence: quiz answer, demo completion, reduced support question, sign-up, policy comprehension, behavior change, stakeholder approval, or share/save.
- Constraints: duration, platform, brand, required sources, must-include/must-avoid claims, restricted imagery, voice, captions, languages, review approvers, budget, and tool availability.
- Risk tier:
  - Low: general concept, internal orientation, non-sensitive creative explanation.
  - Medium: product benefits, nonprofit/public-service behavior guidance, data claims, employment/training requirements.
  - High: health, safety, legal, financial, regulated products, children, political persuasion, crisis guidance, comparative advertising, public statistics with policy implications.

Write the objective as an observable outcome, not a vague topic:

- Weak: "Explain carbon offsets."
- Strong: "After 90 seconds, a first-time buyer can tell the difference between reducing emissions and buying offsets, and knows to look for project verification before trusting a claim."

## Research and citation discipline

Create a claim matrix before scripting. The matrix prevents persuasive polish from outrunning the evidence.

| Field | Use |
|---|---|
| Claim | The exact statement or implication the video may make. |
| Claim type | Definition, statistic, causal, comparative, product performance, testimonial, safety, behavior recommendation, forecast, opinion, metaphor, or CTA. |
| Source | Primary source preferred; include title, URL, publication/update date, and access date. |
| Evidence strength | Official/primary, peer-reviewed, technical report, reproducible test, reputable secondary, client-provided, anecdotal, or creative. |
| On-screen handling | Citation, source line, voice-only, legal/disclosure copy, excluded from final, or expert-review required. |
| Risk | Low/medium/high and why. |
| Owner | Agent, client, SME, legal/compliance, medical, financial, accessibility, localization. |

Use primary sources where possible: official documentation, standards, regulator guidance, government statistics, peer-reviewed research, product docs, client-approved evidence, or directly inspected source materials. Use secondary sources only when primary sources are unavailable or for background, and label them as such.

For commercial or product explainers, objective performance claims need substantiation. FTC business guidance says companies must support advertising claims with solid proof, especially health-related claims; the FTC Endorsement Guides also require material connections in endorsements to be disclosed clearly and conspicuously. Treat these as compliance triggers, not as copywriting suggestions. Re-check current FTC guidance and applicable jurisdiction at production time.

For AI-generated media and stock/media assets, record provenance: model/provider, prompt, seed if available, source asset license, release/consent status, edit history, and whether material is AI-generated. U.S. Copyright Office guidance says copyright registration of works containing AI-generated material turns on human authorship and disclosure of more-than-de-minimis AI-generated content; rights rules are volatile and jurisdiction-dependent, so escalate registration, ownership, likeness, and training-data questions to legal counsel.

## Decompose the concept before writing

Break the idea into explainable atoms:

1. Terms: vocabulary the audience needs before the explanation works.
2. Parts: components, actors, inputs, outputs, constraints.
3. Mechanism: what changes, in what order, and why.
4. Contrast: what this is not; common misconception or false alternative.
5. Example: concrete case, scenario, or mini-demo.
6. Consequence: why it matters; what happens if ignored.
7. Action: what the viewer should do next.

Choose the minimum set needed for the objective. If the concept has too many atoms for the duration, narrow the promise instead of compressing everything.

Useful decomposition patterns:

- Definition explainer: term -> contrast -> example -> use.
- Mechanism explainer: input -> transformation -> output -> feedback loop.
- Product explainer: problem -> current workaround -> product mechanism -> proof -> next step.
- Public-service explainer: situation -> risk -> recommended action -> exception -> where to get help.
- Training explainer: task goal -> prerequisites -> steps -> check -> recovery path.
- Data explainer: question -> dataset/source -> pattern -> caveat -> implication.

## Script architecture

Use the structure that fits the objective; do not force every explainer into the same funnel.

Core structure for most 60-180 second explainers:

1. Hook: name the tension or practical question.
2. Promise: tell viewers what they will understand or be able to do.
3. Map: preview the two to four pieces of the explanation.
4. Build: explain one idea per beat, each beat resolving one question.
5. Example/demo: show the concept working in a concrete case.
6. Caveat or boundary: prevent overclaiming and address a common misconception.
7. Action: next step, summary, practice task, or decision prompt.

Short social variant, 15-45 seconds:

- 0-3s: pattern interrupt or specific problem.
- 3-8s: promise and stakes.
- Middle: one mechanism or one before/after, not a full curriculum.
- End: memorable line, CTA, or "save this" recap.

Training/onboarding variant:

- State the task and success condition.
- Demonstrate steps in order.
- Add checkpoints and error recovery.
- End with where to find help or how to verify completion.

Public-service/nonprofit variant:

- Use plain language and avoid shame.
- Make the recommended action concrete.
- Show who the recommendation applies to and who needs different guidance.
- Cite official sources and escalate health/safety/legal claims.

## Write narration for comprehension

Narration should sound like a capable guide, not a whitepaper read aloud.

- Use everyday words unless a technical term is necessary; define necessary terms before relying on them.
- Put one idea in each sentence.
- Keep clauses short enough for voiceover and captions.
- Use signposting: "First," "The key difference," "Here is the catch," "Now watch what changes."
- Repeat critical terms consistently; do not rotate synonyms for concepts the viewer is still learning.
- Put numbers in context: compare, convert, show scale, or say why the number matters.
- Read the script aloud. If the voice trips, the viewer will too.

For scripted voiceover, plan roughly 130-160 spoken English words per minute for calm explainers, slower for technical, translated, child-facing, or accessibility-sensitive videos. Treat this as a heuristic; actual pacing depends on language, speaker, audience, visuals, and pause needs.

## Use analogies without lying

Analogies help when they map structure, not just mood.

Before using an analogy, write:

- What maps: "A is like B because both..."
- What does not map: "Unlike B, A does not..."
- Where to stop: the exact point after which the analogy becomes misleading.

Example: "A heat pump is like moving water uphill with a pump: you spend energy moving heat rather than creating heat. But unlike water, heat naturally flows from warmer to cooler places, so the device uses a refrigerant cycle to move it the other way."

Avoid analogies in high-risk domains if the simplification could change behavior, dose, safety, eligibility, legal interpretation, or financial decision-making. Use plain causal explanation instead.

## Storyboard as information design

Storyboard every scene with these columns:

| Column | Required content |
|---|---|
| Time | Start/end, duration, and pacing intention. |
| Learning beat | What the viewer learns or can now do. |
| Narration | Exact voiceover or dialogue. |
| Visual | Diagram, character action, screen capture, product UI, data chart, live footage, icon system, or generated media shot. |
| Motion | What changes on screen and why that motion helps understanding. |
| Text/caption | On-screen labels, source line, disclosure, lower third, or no text. |
| Evidence | Claim IDs from the claim matrix. |
| Accessibility | Caption note, audio-description need, contrast risk, no-color-only encoding, flashing/motion risk, transcript note. |
| Asset/prompt notes | What must be deterministic vs. what may be generated. |

If a scene has no learning beat, cut it or convert it into a transition lasting only as long as needed.

## Visual grammar for explainer scenes

Match the visual form to the cognitive job:

- Definition: term card, labeled object, side-by-side "is/is not."
- Process: flow, timeline, numbered sequence, conveyor, state machine.
- Cause/effect: before/after, causal chain, feedback loop, split screen.
- System: map of actors, inputs, outputs, dependencies, boundaries.
- Scale: familiar comparison, proportional bars, nested containers, map inset.
- Data: chart with one takeaway, highlighted trend, source line, caveat.
- Product: real UI or product surface, problem context, feature in use, result state.
- Training: cursor path, highlighted control, checklist, success/error state.
- Social/emotional: human scenario, testimonial with disclosure, character metaphor.

Keep visual language consistent: one color for "problem," one for "solution," one for "warning," one for "proof." Do not switch meanings mid-video.

Avoid decorative literalism. A cloud icon behind every mention of "cloud" rarely explains anything. Use visuals to show relationships, sequence, magnitude, change, and exceptions.

## Diagrams, charts, and data callouts

Use charts and diagrams only when they answer a question better than narration.

Data and diagram rules:

- State the takeaway in words before or with the chart.
- Use the simplest chart that preserves the truth. Prefer bar charts for category comparisons, line charts for trends over time, timelines for sequence, and annotated diagrams for mechanisms.
- Do not use pie/donut charts for many categories, small differences, or precise comparisons.
- Label directly where possible; reduce legend hunting.
- Do not encode meaning by color alone. Add labels, position, shape, pattern, or text.
- For web or interactive delivery, provide accessible alternatives. W3C WAI treats graphs, charts, flow charts, diagrams, and maps as complex images when they contain substantial information, requiring short and long text alternatives. USWDS guidance notes that SVG chart content can be hard for screen readers and recommends screen-reader-accessible tables plus plain-text trend/statistical summaries, while warning that tables alone may not be sufficient for complex datasets.
- In video-only delivery, make the narration and captions carry the key chart takeaway, and provide a transcript or companion notes when the chart is essential.
- Generate charts deterministically from verified data. Do not ask a generative image model to create a factual chart.

## Motion direction

Motion should explain change.

Use motion to:

- reveal sequence;
- connect cause to effect;
- show state transitions;
- compare before/after;
- guide attention;
- pace cognitive load;
- create emotional emphasis after the viewer understands the point.

Avoid motion that competes with the explanation:

- constant background motion under dense text;
- rapid camera moves during new information;
- simultaneous changes in multiple regions;
- transitions that imply causality where none exists;
- fake UI behavior that differs from the product;
- flashing more than three times in one second or flashes near known thresholds; WCAG includes a "three flashes or below threshold" requirement for web content.

Use pauses. A half-second hold after a key reveal often teaches more than another flourish.

## Narration, voice, music, and sound

Choose voice by trust relationship:

- Teacher/mentor: calm, precise, warm.
- Product guide: confident, practical, not hype-heavy.
- Public-service: respectful, plain, non-shaming.
- Training: steady, directive, enough pauses for task execution.
- Youth/social: energetic but still intelligible and caption-friendly.

Prepare a pronunciation sheet for names, acronyms, medication/technical terms, non-English words, and brand terms. For TTS, test a short sample before batch generation.

Mix for speech intelligibility:

- Narration must remain dominant.
- Music should support pace and emotion, not fill every gap.
- Sound effects should mark state changes or actions; avoid cartoon clutter unless the style calls for it.
- If background audio runs longer than a few seconds under speech, keep it low and non-distracting. WCAG includes guidance on low/no background audio at AAA, and WAI media guidance emphasizes low background audio as part of accessible examples.

## Captions, transcripts, and accessibility

Design accessibility from the script stage.

Minimum production targets:

- Captions for all speech and meaningful non-speech audio. WCAG 2.2 includes prerecorded captions at Level A and live captions at Level AA for synchronized media.
- Descriptive transcript for meaningful video where feasible; W3C WAI recommends transcripts that include speech, meaningful non-speech audio, and ideally visual information.
- Audio description or integrated description when key meaning is visual-only. WAI recommends planning integrated description before filming/scripting because it is easier and often better for accessibility.
- Sufficient contrast for text and essential graphical objects. WCAG 2.2 includes text contrast and non-text contrast requirements; use them as a floor, not a ceiling.
- No information conveyed only by color, sound, motion, or spatial position.
- Avoid dense text. If text must be read, leave enough on-screen time for the intended audience and localized variants.
- Keep lower-thirds, source lines, disclosures, and captions out of crop-risk areas for all delivery variants.
- Provide language tags, translated captions, and localized transcripts when localizing.

Caption style:

- Break lines at phrase boundaries.
- Keep captions synchronized with speech.
- Identify speakers when unclear.
- Include meaningful non-speech audio: "[door chime]," "[alarm beeps]," "[music fades]."
- Do not paraphrase claims in captions in a way that changes legal or factual meaning.

## Generated-media prompt translation

Translate the storyboard into generation instructions only after the facts, visuals, and motion jobs are clear.

For each generated asset or clip, specify:

- scene ID and learning beat;
- exact content that must appear;
- content that must not appear;
- style, medium, aspect ratio, framing, lighting, camera/motion, duration, and mood;
- whether text must be absent, added later in composition, or generated deterministically;
- continuity constraints: recurring character, product, colors, icon shapes, UI state, diagram geometry;
- evidence/provenance constraints: source image, product screenshot, brand asset, release/consent, citation;
- review criteria and failure modes.

Provider-independent prompt pattern:

```text
Scene purpose: [what the viewer learns]
Visual form: [diagram/product demo/character metaphor/data callout/live-action shot]
Subject/action: [what happens]
Composition: [framing, layers, focal hierarchy]
Motion: [what changes and why]
Style constraints: [brand, palette, texture, realism level]
Accuracy constraints: [must match product/source; no invented UI/text/data]
Text policy: [no generated text; labels added in edit; or exact deterministic overlay]
Accessibility constraints: [contrast, no color-only meaning, no rapid flashing]
Negative constraints: [avoid stereotypes, unsafe behavior, extra objects, fake logos]
Output: [duration, aspect ratio, resolution, transparent background if needed]
```

If the provider cannot reliably preserve required details, change the production method: compose deterministic diagrams, use screenshots, use vector animation, record real UI, or simplify the scene. Do not accept a plausible but false generated visual.

## Claim, risk, and rights review

Run review before final render and again after variants are made.

Escalate when the video:

- tells viewers what to do about health, medication, diagnosis, safety, law, taxes, investing, insurance, immigration, employment rights, or regulated products;
- compares products, competitors, performance, prices, environmental impact, or "best" claims;
- uses testimonials, endorsements, influencer-style content, affiliate links, sponsored content, or before/after results;
- uses children, vulnerable groups, crisis contexts, public emergencies, political persuasion, or targeted demographic claims;
- uses AI-generated likenesses, voices, public figures, private people, copyrighted characters, trademarks, client confidential information, or third-party footage/music/images;
- includes statistics that could be outdated, cherry-picked, or missing base rates;
- will be localized into languages or jurisdictions with different legal/cultural requirements.

Commercial claims checklist:

- Is each objective claim substantiated by current evidence?
- Does any visual imply a stronger result than the narration says?
- Are typical results disclosed when testimonials show unusual results?
- Are material connections disclosed clearly in both audio and visual form when the endorsement claim is audio+visual?
- Is disclosure readable, audible, unavoidable, and in the same language as the claim?
- Is the CTA materially different from the educational objective? If so, make the persuasive turn explicit.

## Localization and cultural adaptation

Localize the explanation, not just the words.

- Re-check claims, regulations, measurements, prices, product availability, and support links for each locale.
- Replace idioms and analogies that do not travel.
- Adapt examples, names, units, currency, dates, screenshots, voice, music, gestures, reading direction, and caption length.
- Allow more time for languages that expand in translation.
- Rebuild text layouts for translated copy; do not shrink text until unreadable.
- Re-record or regenerate narration with native pronunciation review for important releases.
- Keep source citations and disclosures matched to the localized claim.

## Edit pacing and structure review

During edit, watch once for comprehension with no pausing:

- Can a first-time viewer state the core idea?
- Is there enough time to inspect each diagram?
- Do cuts happen after the learning beat lands?
- Does the eye know where to look?
- Are visual transitions carrying meaning or just energy?
- Are there unsupported claims hiding in b-roll, icons, UI mockups, or generated scenes?
- Does the final CTA follow from the explanation rather than hijack it?

Use an animatic for any explainer with more than six scenes, dense data, product UI, or high-risk claims. An animatic can be rough, but it must include timing, narration, placeholder visuals, captions, and claim/disclosure placement.

## Delivery variants

Create a master version first, then variants.

Variant plan:

- Master: highest-quality aspect ratio and full captions/transcript/source log.
- Social cutdowns: one idea per cutdown; do not crop away labels, captions, disclosures, or important gestures.
- Silent/autoplay version: captions and visual context must carry the story without audio.
- Training/LMS version: include chapters, transcript, quiz/checkpoints, and downloadable references if applicable.
- Public-service version: include source date, eligibility boundaries, and help/resource CTA.
- Sales/product version: include approved claims, proof points, disclosure handling, and current product UI.

Platform specs are volatile. Re-check official platform requirements at export time instead of relying on memorized values.

## Explainer QA checklist

Pass the video only when all relevant checks are true:

- Objective: one clear audience and one clear learning/decision objective.
- Structure: hook, promise, build, example, boundary, and action are appropriate for duration.
- Evidence: every factual/commercial/statistical claim is sourced or removed.
- Risk: high-risk claims have the right human reviewer.
- Clarity: jargon is defined or replaced.
- Cognitive load: one new idea per beat; visuals are not overstuffed.
- Visual grammar: diagrams, charts, UI, footage, and generated scenes each do a defined explanatory job.
- Motion: motion guides attention and explains change; no unsafe flashing.
- Accessibility: captions, transcript plan, contrast, audio-description/integrated-description needs, and non-color encodings are handled.
- Audio: narration is intelligible; music and SFX do not mask speech.
- Generated media: no invented facts, fake charts, fake UI, accidental trademarks, distorted people, or unreadable generated text.
- Rights/provenance: assets, voices, likenesses, AI generation, licenses, and releases are logged.
- Localization: translated variants preserve claims, disclosures, timing, and accessibility.
- Delivery: exports keep captions/disclosures/source lines in safe areas and match current platform specs.

## Example: educational concept explainer

User request: "Make a 90-second animated explainer about how heat pumps heat a home."

Production intent: teach homeowners the mechanism and correct the misconception that a heat pump "creates heat" like a furnace.

Learning objective: after watching, a homeowner can explain that a heat pump moves heat using a refrigerant cycle and can name the indoor coil, outdoor coil, compressor, and expansion step.

Decomposition:

- Terms: heat, refrigerant, compressor, coil.
- Misconception: "cold air has no heat."
- Mechanism: refrigerant absorbs heat outside, compressor raises temperature, indoor coil releases heat, expansion cools refrigerant, repeat.
- Boundary: performance and backup heat depend on climate/model; avoid universal efficiency claims unless sourced.

Scene excerpt:

| Time | Narration | Visual/motion | Evidence/accessibility |
|---|---|---|---|
| 0-7s | "A heat pump does not make heat the way a flame does. It moves heat, like a refrigerator running in reverse." | Split screen: furnace icon creates flame; heat pump moves glowing dots from outside to inside. | Label analogy boundary later. Captions; no color-only distinction. |
| 7-22s | "Even cold outdoor air contains heat energy. The refrigerant absorbs some of it as it passes through the outdoor coil." | Simple loop diagram. Outdoor coil highlights; dots move into refrigerant line. | Avoid exact temperature claims unless sourced. |
| 22-38s | "The compressor squeezes the refrigerant, raising its temperature." | Compressor icon compresses line; thermometer rises. | Deterministic labels, not generated text. |
| 38-55s | "Inside, that hotter refrigerant releases heat into the home." | Indoor coil warms airflow arrows; room warms. | Audio describes visual change. |
| 55-72s | "Then the refrigerant expands, cools down, and the cycle starts again." | Expansion valve opens; loop returns. | Motion explains sequence. |
| 72-90s | "So the simple idea is: spend electricity to move heat, not to create it from scratch." | Full loop recap with four numbered steps. | Recap supports memory. |

Generated-media prompt for a diagram scene:

```text
Scene purpose: show that a heat pump moves heat through a repeating loop.
Visual form: clean animated vector diagram, not photorealistic.
Subject/action: a closed refrigerant loop connects an outdoor coil, compressor, indoor coil, and expansion valve; small warm-energy dots move from outdoor air into the loop, then into the house.
Composition: left side outdoor unit, right side simple house interior, loop centered, four large icon-like components with empty space for labels added later.
Motion: dots move clockwise; compressor briefly squeezes the line; indoor airflow arrows glow gently.
Style constraints: flat educational animation, high contrast, limited blue/orange palette, no brand logos.
Accuracy constraints: no extra components, no numerical efficiency claims, no rendered text.
Text policy: all labels added later in composition.
Accessibility constraints: do not rely on color alone; use arrows and position; no flashing.
Output: 16:9, 8 seconds, seamless motion, transparent-safe background if possible.
```

Likely failure modes: generated model adds unreadable labels, depicts a flame, shows impossible pipe routing, or implies the outdoor air must be warm. Fix by using deterministic vector composition or tighter diagram prompts.

## Example: product explainer with claim controls

User request: "Create a 60-second explainer for our AI meeting assistant that saves teams 10 hours a week."

Risk: commercial performance claim. "Saves 10 hours a week" needs substantiation and context.

Safe production approach:

1. Ask for substantiation: study, customer data, methodology, sample size, time period, and whether the result is typical.
2. If substantiated, state the claim with scope: "In a customer survey of [n] [audience] over [period], teams reported saving an average of [x] hours..."
3. If not substantiated, rewrite as a non-quantified benefit: "helps teams spend less time turning meetings into follow-ups."
4. Show actual or approved UI, not invented screens.
5. Put any endorsement, testimonial, sponsored review, or atypical result through disclosure review.

Structure:

- Hook: "The meeting is over. The work is not."
- Problem: notes, owners, deadlines, follow-up drift.
- Mechanism: records/transcribes, identifies decisions, drafts action items, syncs to workflow.
- Proof: approved claim or demo result.
- Boundary: "Review AI-generated notes before sending."
- CTA: "Try it with your next recurring meeting."

Storyboard note: use real UI capture or deterministic mockups approved by the client. Do not generate fake product screens that imply unsupported features.

## Example: public-service explainer

User request: "Make a 45-second video telling people what to do during extreme heat."

Risk: public health/safety. Use official sources, current local guidance, and expert/client review.

Approach:

- Audience: local residents, including older adults, outdoor workers, parents, and people without reliable cooling.
- Objective: viewer can name three immediate protective actions and knows where to find local cooling-center information.
- Sources: official local emergency management/public health pages, weather service alerts, and client-approved resource links.
- Language: plain, direct, non-shaming.
- Accessibility: captions, high contrast, no tiny emergency URLs, voice and text in target languages.

Script shape:

- "When heat becomes dangerous, do three things early."
- "Drink water before you feel thirsty."
- "Spend time in air conditioning if you can; use the local cooling-center link on screen."
- "Check on neighbors, older adults, and people who live alone."
- "Call emergency services if someone has confusion, fainting, or other emergency symptoms." Escalate exact symptom/action wording to public health reviewer.

Do not improvise medical triage. Keep emergency guidance aligned with official local sources and reviewer approval.

## Source notes and verification

Sources consulted and verified on 2026-07-10:

- W3C, Web Content Accessibility Guidelines (WCAG) 2.2, W3C Recommendation, 2024-12-12: https://www.w3.org/TR/WCAG22/
- W3C WAI, Making Audio and Video Media Accessible, updated 2024-09-17: https://www.w3.org/WAI/media/av/
- W3C WAI, Complex Images tutorial: https://www.w3.org/WAI/tutorials/images/complex/
- U.S. Web Design System, Data visualizations component guidance: https://designsystem.digital.gov/components/data-visualizations/
- CDC, Clear Communication Index: https://www.cdc.gov/ccindex/index.html
- Digital.gov, Plain language guide series: https://digital.gov/guides/plain-language
- FTC, Advertising and Marketing business guidance: https://www.ftc.gov/business-guidance/advertising-marketing
- eCFR, 16 CFR Part 255, Guides Concerning Use of Endorsements and Testimonials in Advertising, displayed current as of 2026-07-09 when consulted: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255
- FTC, Endorsement Guides: What People Are Asking: https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- U.S. Copyright Office, Copyright and Artificial Intelligence portal and 2023 registration guidance: https://www.copyright.gov/ai/ and https://www.copyright.gov/ai/ai_policy_guidance.pdf

Volatile areas to re-check at production time: platform export specifications, provider/model capabilities and terms, pricing, content policies, social disclosure UX, advertising/endorsement rules, copyright/AI guidance, local public-service guidance, product UI, client claims, statistics, and localization/legal requirements.
