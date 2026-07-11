# Evaluation: production-design-direction

Use this file as the scoring key for agents evaluated with the production-design-direction skill. The evaluated agent should receive the production task and SKILL.md only.

Total suggested score: 100 points. Passing: 80+. Strong: 90+. A response with a critical safety/legal failure, severe reference-copying instruction, or no production-design reasoning should not pass even if it scores well on surface style.

## Core competency weights

1. Production-design framing and brief translation: 15 points
2. Set/location, prop, color/material, graphic/environmental design specificity: 25 points
3. Reference, era, worldbuilding, and rights-aware strategy: 15 points
4. Prompt/shot planning and handoff usefulness for generated media: 15 points
5. Iteration and QA reasoning: 15 points
6. Separation of documented facts, empirical observations, and heuristics: 5 points
7. Format/platform/brand/legal/accessibility constraints: 10 points

## Knowledge questions

### Q1. What is production design doing in a generated-media workflow?

Expected answer:

- It translates story, brand, product, audience, and format intent into the visible world: sets, locations, props, color/value/material systems, graphics, era/world rules, continuity anchors, prompt plans, handoff, and QA.
- It is not merely a moodboard or list of style adjectives.
- It should guide what appears, what must remain stable, what is composited later, and what must be avoided.

Required points:

- 2 points for visible-world translation.
- 2 points for including sets/locations/props/color/materials/graphics/continuity.
- 1 point for distinguishing production design from generic prompting.

Penalize:

- Treating the skill as only "make prompts cinematic."
- Ignoring brand/product/story intent.

### Q2. How should an agent handle exact logos, UI, package labels, claims, and readable text in generated images or video?

Expected answer:

- Exact or legally important text/logos/UI should usually be reserved for post-production compositing or controlled editing, because generated text and marks are unreliable.
- The production plan should include blank label/screen areas, safe zones, contrast/readability needs, and claim/legal verification.
- The agent should avoid fake endorsements, fake seals, competitor lookalikes, and unverified performance/health/sustainability claims.

Required points:

- 2 points for reserving exact text/logos/UI for post where appropriate.
- 2 points for safe zones/readability/contrast.
- 2 points for legal/brand risk awareness.

Critical failure:

- Instructs the model to generate exact trademarked competitor marks or fake certifications.

### Q3. Why separate hue, value, chroma/saturation, and material when writing color direction?

Expected answer:

- Hue alone is insufficient; value controls readability and frame hierarchy, chroma controls intensity/mood, and material controls how color behaves under light.
- This separation makes palette direction more renderable and testable.
- It helps prevent vague labels such as "luxury," "retro," or "warm" from collapsing into clichés.

Required points:

- 2 points for value/readability/hierarchy.
- 2 points for chroma/saturation/mood.
- 1 point for material/light behavior.
- 1 point for renderability/testability.

### Q4. What should a reference ledger capture?

Expected answer:

- Source, date/era/geography, what the reference informs, rights/usage status, what not to copy, and whether it is architecture, material, object, signage, camera mood, or palette evidence.
- For historical/culturally specific work, it should separate evidence by category and avoid mixing eras or regions without reason.

Required points:

- 2 points for source/date/geography.
- 2 points for what it informs.
- 2 points for rights/what not to copy.
- 1 point for category separation.

Critical failure:

- Tells the agent to copy a protected still, brand, artist, or production design wholesale.

### Q5. Name at least four continuity anchors useful for generated video production design.

Expected answer examples:

- Doorway shape, window grid, floor pattern, hero wall color, signature prop, hero product geometry, furniture layout, lighting fixture, material palette, signage shape, repeated accent color, background landmark.

Scoring:

- 1 point each for four valid anchors.
- Bonus within task scoring if the answer explains that anchors should be repeated in every shot prompt.

## Production-decision scenarios

### Scenario 1: Paid social privacy-app ad

User asks for a vertical paid social ad for a privacy-focused team app, "warm and trustworthy, not hacker-like."

Strong expected decision:

- Choose a human, tactile workspace world rather than cyber-security clichés.
- Define a set with warm daylight, partitions, controlled reveal, calm props, and blank compositing-safe UI areas.
- Use one or two brand-memory accents, low-glare materials, and phone-readable hierarchy.
- Reserve caption/disclosure/CTA space.
- Avoid hooded hackers, neon code, server rooms, fake security certifications, unreadable generated UI text, and competitor cues.

Scoring, 10 points:

- 2 brief translation into design thesis.
- 2 set/location specificity.
- 2 props and graphics plan.
- 2 platform/brand/legal constraints.
- 2 prompt/shot handoff practicality.

Penalize:

- Generic "modern office, cinematic lighting" with no privacy metaphor.
- Exact UI text/logos generated directly without noting risk.

### Scenario 2: Historical railway room

User asks for a 1930s railway waiting room, no people, bittersweet, ten-second image-to-video.

Strong expected decision:

- Build an era/location research plan using primary or authoritative visual references.
- Specify architecture, benches, lamps, tile, signage/posters, luggage, patina, and exact exclusions such as LED signs, plastic chairs, and modern safety graphics.
- Use continuity anchors such as a brass clock, bench paint, tile border, and doorway.
- Treat readable signage as blank or post-produced.
- Repeat "no people" and physical details in the video prompt.

Scoring, 10 points:

- 2 research plan and era discipline.
- 2 set/material specificity.
- 2 prop/evidence logic.
- 2 video continuity and prompt planning.
- 2 exclusions and text handling.

Critical failure:

- Produces vague "vintage train station" direction with no era safeguards, or introduces modern elements without intention.

### Scenario 3: Product sustainability hero image

User asks for e-commerce hero images for a refillable cleaner bottle, "minimal, sustainable, not greenwashed."

Strong expected decision:

- Show reuse through product system and ritual: refill pouch, measuring cap, cloth, durable materials.
- Avoid symbolic greenwashing: leaves, fake seals, certification badges, forest backgrounds, unverified claims.
- Define product silhouette/material fidelity and blank label area for exact packaging graphics.
- Use warm neutral palette, practical kitchen context, negative space for layout.
- QA for product geometry, claim safety, and e-commerce readability.

Scoring, 10 points:

- 2 product truth and hierarchy.
- 2 prop logic.
- 2 palette/material plan.
- 2 claims/label/legal safeguards.
- 2 e-commerce composition practicality.

## Applied production tasks

### Task A: Create a production design bible

User request:

"Design a visual world for a 45-second teaser for a fictional climate-tech battery startup. The product stores home solar energy. Audience is investors and early adopters. It should feel credible and optimistic, not sci-fi."

Expected approach:

- Produce a design thesis tied to credibility, optimism, home energy, and investor trust.
- Define domestic and light-industrial sets/locations, not generic laboratories or sci-fi cities.
- Specify product environment, hero props, evidence props, palette/material rules, graphic/UI handling, continuity anchors, and negative constraints.
- Include shot/asset prompt planning and QA.
- Include brand/legal/accessibility cautions: no unverified claims, readable chart/UI reserved for post, contrast for overlays, no confusing competitor marks.

Rubric, 20 points:

- 4 points design thesis and strategic translation.
- 4 points set/location specificity with functional logic.
- 3 points props and evidence of product use.
- 3 points color/value/material system.
- 2 points graphic/environmental design and post-compositing plan.
- 2 points shot/prompt planning with continuity anchors.
- 2 points QA and constraints.

Critical failures:

- Turns the concept into space-age neon sci-fi despite "credible and optimistic."
- Adds fake awards, certifications, or measurable claims.
- Omits the product's relationship to home solar use.

### Task B: Diagnose and repair a failed render

User says:

"The generated frame for our artisanal coffee subscription ad looks like a generic luxury hotel breakfast. It needs to feel like a real neighborhood roaster: warm, small-batch, approachable, but still premium."

Expected approach:

- Diagnose story/set/prop/palette/material misses: wrong location class, generic luxury cues, insufficient roaster evidence, props too hotel-like.
- Repair with specific set and prop changes: roaster counter, burlap or paper sacks if appropriate, labeled but non-readable roast cards, scale, hand tools, grinder, cupping spoons, paper order tickets, worn wood/steel surfaces, local morning light.
- Maintain premium through craft, restraint, material quality, and hierarchy rather than marble/gold/champagne.
- Include prompt rewrite and negative constraints.
- Note exact labels/logos/claims should be composited or verified.

Rubric, 15 points:

- 4 points accurate diagnosis by layer.
- 4 points concrete repair plan.
- 3 points premium-but-approachable palette/material/prop system.
- 2 points prompt rewrite quality.
- 2 points brand/legal/text safeguards.

Penalize:

- Merely says "make it more authentic."
- Adds clutter without hierarchy.

### Task C: Reference-use plan under rights constraints

User says:

"Use this famous film still's production design as the basis for our perfume launch images. We want it to feel exactly like that scene."

Expected approach:

- Refuse to copy the film still or recreate its protected production design "exactly."
- Offer a clean-room reference strategy: identify abstract attributes such as emotional temperature, spatial density, material contrast, lighting direction, palette relationship, and symbolic object function without duplicating the scene.
- Build a new design thesis for the perfume brand using original sets, props, palette, and materials.
- Include a reference ledger and "what not to copy" guardrails.

Rubric, 15 points:

- 4 points rights/copying risk recognition.
- 4 points clean-room abstraction method.
- 3 points original production design alternative.
- 2 points handoff/reference ledger.
- 2 points diplomatic user-facing phrasing.

Critical failure:

- Provides prompts to reproduce the famous still or name-specific look in a confusingly similar way.

## Required QA signals in strong answers

A strong answer should include most of these checks when relevant:

- Hero subject legibility in first seconds or first glance.
- Set logic and location plausibility.
- Props divided into hero/action/evidence/texture roles.
- Palette includes value/chroma/material, not only color names.
- Graphic design/text/logos handled by compositing when exactness matters.
- Reference use avoids copying and tracks rights.
- Historical/cultural details use dated/geographic evidence.
- Accessibility considered for text, UI, callouts, charts, and overlays.
- Advertising/product claims and endorsements are verified or excluded.
- Continuity anchors repeated for multi-shot generation.
- Negative constraints are specific and tied to likely failure modes.

## Disqualifying or severe-penalty patterns

- No production-design content beyond generic visual adjectives.
- No connection between set/props/palette and narrative, brand, product, or audience.
- Direct instruction to copy a living artist, film still, brand, or competitor trade dress.
- Fake legal, medical, financial, safety, sustainability, certification, or endorsement claims.
- Historical/cultural stereotypes or unsupported sacred/political/uniform symbols.
- Omits exact-text/logo/UI risk in a task where those elements matter.
- No continuity planning for multi-shot video.
- Treats accessibility contrast as irrelevant when readable text or information graphics are central.

## Suggested evaluator procedure

1. Give the evaluated agent SKILL.md and one or more tasks above, or a comparable unseen task.
2. Capture its full response.
3. Score against the relevant rubric and core competency weights.
4. Check for critical failures before assigning pass/fail.
5. Reward concise but operational handoff artifacts over long moodboard prose.
