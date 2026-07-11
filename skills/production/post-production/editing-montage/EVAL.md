# Evaluation: editing-montage

This is the private scoring guide for evaluating whether an agent can apply the editing-montage skill to real production work. The evaluated agent should receive only the user task and SKILL.md, never this file.

Score out of 100. Passing threshold: 80. A response below 70 is not production-ready even if it uses correct vocabulary.

## Core scoring dimensions

1. Edit reasoning and story structure (20 points)
2. Shot selection and continuity competence (15 points)
3. Montage/rhythm/audio craft (20 points)
4. Platform, captions, and delivery awareness (10 points)
5. Source/generated asset management and handoff clarity (15 points)
6. Revision workflow and QA behavior (10 points)
7. Evidence discipline and safety/rights awareness (10 points)

Critical failures that cap the score at 60:

- Treats editing as simple chronological assembly with no story, viewer-effect, or rhythm reasoning.
- Gives unsupported universal platform rules or outdated specs as fact.
- Ignores rights, captions, synthetic-media provenance, or factual-claim risks for a public deliverable.
- Produces vague advice without timeline-level decisions for a requested edit plan.
- Recommends decorative transitions or speed without clarifying the story function.

Critical failures that cap the score at 50:

- Advises hiding factual, product, legal, or identity errors with cuts when the correct action is replacement, disclosure, or approval.
- Invents source footage details or platform requirements not present in the prompt.
- Leaks or refers to this scoring file in a production answer.

## Knowledge questions

### 1. What is the difference between continuity editing and montage?

Expected answer:

- Continuity editing preserves enough time, space, identity, action, eyeline, and causality for the viewer to believe shots connect.
- Montage creates meaning from juxtaposition, accumulation, contrast, compression, rhythm, or association across shots.
- A strong answer notes that both can coexist: a sequence may use continuity inside beats and montage between beats.

Required points:

- Mentions spatial/temporal/identity coherence for continuity.
- Mentions meaning emerging from relationships between shots for montage.
- Avoids saying montage simply means "fast cuts."

Deduct:

- -4 for defining montage as any sequence of B-roll.
- -4 for implying continuity is always better or montage is always more creative.

### 2. Explain J-cuts and L-cuts and when to use each.

Expected answer:

- J-cut: next audio begins before the visual cut; useful for pulling the viewer into a new scene, thought, speaker, or energy.
- L-cut: previous audio continues after the visual cut; useful for carrying emotion, explanation, room tone, or a speaker over proof shots/cutaways.
- Should mention clean audio transitions, room tone/music continuity, and not obscuring dialogue.

Required points:

- Correct definitions.
- At least one production use case for each.
- Audio intelligibility/cleanliness consideration.

Deduct:

- -5 for reversing definitions.
- -3 for treating them only as software timeline shapes without editorial purpose.

### 3. What are common generated-media edit risks?

Expected answer:

- Identity drift in faces/characters/products.
- Logo/text/UI artifacts.
- Inconsistent lighting, scale, geography, physics, reflections, hands, object state.
- Bad first/last frames, local motion that lacks editorial endpoints.
- Need for provenance: provider/model/seed/prompt/version/rights where available.

Required points:

- At least four specific visual continuity risks.
- Mentions trimming, replacing, covering, or separating as possible remedies.
- Mentions documentation/provenance.

Deduct:

- -4 for saying AI clips can be treated like normal footage without extra QA.
- -4 for recommending cover-ups for distorted product/logo shots used as proof.

### 4. What caption/accessibility guidance should an editor consider?

Expected answer:

- Prerecorded synchronized media with meaningful audio generally needs captions for accessibility.
- Captions should be synchronized and include meaningful audio beyond dialogue when relevant.
- Practical layout should respect safe zones and avoid interfering with visuals/graphics.
- Two-line maximum is a common professional guideline; timed-text duration requirements vary by destination.
- Should not universalize Netflix delivery requirements for all platforms.

Required points:

- Accessibility requirement.
- Readability/timing/layout.
- Destination-specific caution.

Deduct:

- -3 for "captions are optional if the music is loud" when speech/meaningful audio exists.
- -3 for claiming one vendor's subtitle timing is universal.

### 5. What should an edit handoff include?

Expected answer:

- Global settings: platform, aspect ratio, duration, frame rate, safe zones.
- Timeline beats with start/end, source asset IDs, in/out ranges, picture, audio, captions/text, transitions, notes.
- Layering and motion instructions.
- Audio cues including music, SFX, J/L cuts, ducking, silence.
- QA flags and pending approvals/rights/factual checks.

Required points:

- Timeline-level specificity.
- Source IDs/in-out ranges.
- Audio/text/layering instructions.
- QA flags.

Deduct:

- -5 for only giving a prose summary with no executable handoff detail.

## Production-decision scenarios

### Scenario 1: "Make this 75-second product demo into a TikTok ad."

The source is a landscape screen recording, a logo animation, a 45-second voiceover, and three generated lifestyle clips. The product is B2B scheduling software. The user asks for a 20-second TikTok ad.

Expected decision:

- Rebuild as a platform-specific edit, not just crop the 75-second demo.
- Create a vertical-first structure: immediate pain/hook, quick relevance, one product proof, benefit/outcome, CTA.
- Protect UI readability and safe zones; crop/reframe or recreate UI moments rather than shrinking the whole landscape screen.
- Use generated lifestyle clips only if they support the story and pass continuity/brand QA.
- Add captions for voiceover and sound-off comprehension.
- Verify current TikTok placement specs before export; avoid unsupported claims about exact requirements unless verified.

Strong answer should include:

- A 20-second beat plan with timings.
- A source treatment plan for landscape UI.
- A risk note for generated clips and product claim truth.
- Audio/caption plan.

Penalize:

- Cropping the landscape demo center-cut with tiny UI text.
- Spending the first 3 seconds on logo animation only.
- Using all three lifestyle clips because they are "cinematic."
- Ignoring captions or safe zones.

### Scenario 2: A sci-fi teaser has beautiful AI clips but the protagonist changes face in every shot.

Expected decision:

- Identify identity drift as a serious continuity risk.
- Decide whether the edit is continuity-led or impressionistic/montage-led.
- If protagonist identity matters, replace/regenerate/restrict shots, use silhouettes, close-ups without face, POV, inserts, or separation devices; do not pretend inconsistent faces are the same person.
- If impressionistic teaser allows ambiguity, motivate it through memory/dream/glitch/multiple timelines and avoid factual continuity claims.
- Track which shots are usable and why.

Strong answer should include:

- A triage table or list: keep, trim, cover, replace.
- A revised story/edit strategy.
- QA notes for face consistency.

Penalize:

- Advising to cut faster so viewers won't notice.
- Using face morph transitions as a default fix without story motivation.
- Ignoring user trust and continuity.

### Scenario 3: The edit feels "flat" even though every shot is high quality.

Expected decision:

- Diagnose that high-quality shots may lack contrast, escalation, function, or rhythm.
- Rebuild around a story spine and emotional curve.
- Assign shot functions and remove redundant beauty shots.
- Add variation in shot size, duration, movement, audio dynamics, and rest.
- Use montage relationships deliberately: accumulation, contrast, motif return, proof, or transformation.

Strong answer should include:

- Specific likely causes.
- Concrete revision actions.
- A before/after rhythm or beat strategy.

Penalize:

- Adding more transitions, speed ramps, or color grade as the main fix.
- Saying the answer is simply shorter cuts.

### Scenario 4: A documentary interview cut has jump cuts and the client asks to "make it smoother."

Expected decision:

- Use cutaways, reaction shots, relevant B-roll, L-cuts, room tone, and pacing adjustments to smooth edits.
- Preserve meaning and avoid deceptive rearrangement.
- Keep pauses where they carry emotion or credibility.
- Use cutaways related to the statement, not generic filler.
- Maintain truthful context and speaker intent.

Strong answer should include:

- A sample timeline treatment.
- Ethical note about not changing meaning.
- Audio continuity plan.

Penalize:

- Covering cuts with unrelated stock footage.
- Removing all hesitations automatically.
- Rearranging statements into a claim the subject did not make.

### Scenario 5: A beat-driven launch reel is perfectly synced to every beat but feels monotonous.

Expected decision:

- Explain that beat sync alone is not rhythm; phrase-level structure, anticipation, rest, contrast, and payoff matter.
- Re-map the music into sections and reserve strongest visuals for musical changes.
- Use some hits on transients, some phrase sync, and occasional counter-rhythm or silence.
- Vary shot duration and visual density.
- Ensure dialogue/CTA/captions remain intelligible.

Strong answer should include:

- A revised beat map.
- Specific changes to cut density.
- Notes on visual escalation and audio dynamics.

Penalize:

- Adding more cuts or more impacts to every beat.
- Ignoring the CTA or message.

## Applied production tasks

### Task 1: Create an edit plan for a 30-second product ad

User request:

"We have 8 AI-generated office clips, a product screen recording, a voiceover, and a logo. Make a 30-second social ad for our task handoff app. It should feel urgent at first, then relieving."

Expected approach:

- Start with edit promise and platform assumptions.
- Use a problem-to-proof-to-relief structure.
- Use generated office clips for emotion/context, not as proof of the product.
- Hold screen recording long enough for UI readability.
- Include captions, safe-zone, audio, and CTA.
- Provide timeline-level plan.

Scoring rubric (15 points):

- 3: Clear story spine and emotional curve.
- 3: Timeline with plausible timings and shot functions.
- 2: Strong source treatment and generated-media risk handling.
- 2: Audio/J/L/music/caption plan.
- 2: Platform/safe-zone awareness.
- 2: CTA and product proof.
- 1: Notes likely failure modes.

Critical failures:

- Uses mostly generic office montage with no product proof.
- Opens with logo and slow brand intro despite urgent social-ad goal.
- No captions or UI readability concern.

### Task 2: QA a rough edit

User request:

"Here's the rough cut summary: 0-5 logo; 5-12 founder talking; 12-16 dashboard; 16-28 AI office montage; 28-30 CTA. It feels boring. Diagnose it."

Expected approach:

- Identify late hook and overlong logo.
- Founder context may be useful but needs earlier viewer relevance.
- Dashboard proof is too short if UI must read.
- Office montage is long and possibly generic.
- CTA may need clearer connection to proof/outcome.
- Recommend re-ordering: pain/hook, proof, founder as credibility or L-cut, outcome, CTA.

Scoring rubric (10 points):

- 2: Diagnoses structural issue, not just style.
- 2: Reorders with timings.
- 2: Explains viewer effect of changes.
- 1: Addresses UI readability.
- 1: Addresses generated montage risk/redundancy.
- 1: Addresses audio/captions.
- 1: Gives a concise QA pass or next cut objective.

Critical failures:

- Suggests only faster music/transitions.
- Keeps the 5-second logo opener.

### Task 3: Produce a composition handoff

User request:

"Turn this approved edit into handoff notes for a render/composition agent: 45s vertical trailer, music-led, 10 clips, title cards, captions, final logo."

Expected approach:

- Provide a structured EDL/table with timecodes, source IDs, picture, audio, text/graphics, transition, notes.
- Include global settings: 9:16, 45s, platform if known, frame rate if known or TBD, safe zones.
- Include music map and beat hit instructions.
- Include title/caption/logo layers.
- Include QA flags for generated clips, text, rights, and export.

Scoring rubric (15 points):

- 4: Complete timeline-level EDL.
- 3: Audio/music beat mapping.
- 2: Text/caption/title layer instructions.
- 2: Motion/transition instructions with purpose.
- 2: Asset IDs/provenance placeholders.
- 2: QA/export/safe-zone flags.

Critical failures:

- Handoff is only a narrative paragraph.
- Omits source IDs or timing.
- Omits audio and text layers.

## Evidence and source-use scoring

Award up to 10 points across the evaluation for evidence discipline:

- 3: Separates documented facts, empirical observations, and production heuristics when making consequential claims.
- 2: Dates volatile platform facts or says they must be verified at delivery.
- 2: Does not generalize platform/vendor-specific requirements as universal.
- 2: Uses professional terminology accurately without jargon padding.
- 1: Mentions source/rights/caption/accessibility responsibilities where relevant.

Deduct up to 10 points:

- -4 for citing platform rules without date or uncertainty.
- -3 for presenting retention/creative heuristics as guaranteed performance facts.
- -3 for unsupported claims that a specific pacing pattern always performs best.

## Ideal response characteristics

A strong editing-montage response:

- Starts from viewer effect and story promise.
- Makes timeline-level decisions with reasons.
- Uses shot function as the basis for selection.
- Treats generated media as useful but continuity-fragile.
- Uses J/L cuts, cutaways, transitions, and match cuts for editorial purpose.
- Shapes rhythm with contrast, phrase, breath, and audio, not only cut speed.
- Handles captions, safe zones, rights, and platform volatility.
- Produces handoff notes another agent could execute.
- Includes QA passes and likely failure modes.

A weak response:

- Lists generic editing tips.
- Adds transitions instead of solving structure.
- Uses all available footage without selection criteria.
- Ignores audio, captions, and delivery context.
- Treats platform specs as timeless.
- Cannot translate vague feedback into concrete edit actions.
