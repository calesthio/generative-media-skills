# Evaluation: storyboard-previsualization

Use this answer key to score an agent that had access to `SKILL.md` only. Do not expose this file to the evaluated agent.

Total suggested score: 100 points. Passing: 80+. Strong: 90+. A response with any critical failure should not score above 70 even if it is polished.

## Critical failures

Cap the score at 70 if the response:

- Starts producing polished final imagery or video without first planning beat, shot, continuity, and review criteria.
- Treats platform specs, model limits, or tool features as stable without verification when they affect delivery.
- Produces a generic prompt list with no shot IDs, continuity anchors, camera/blocking direction, or pass/fail criteria.
- Ignores aspect ratio/platform constraints in a platform-specific brief.
- Uses references to clone copyrighted/living-artist/brand/performer likeness material without rights qualification.
- Claims AI video/image systems can reliably preserve exact identity, text, logos, action, or spatial continuity across shots without caveats.
- Links or reveals the evaluation file or instructs the production agent to read it.

Cap the score at 60 if the response:

- Confuses storyboards, animatics, previs, and techvis so badly that the proposed artifact does not solve the production risk.
- Recommends breaking the 180-degree line or reversing screen direction with no intentional story reason.
- Provides no review or iteration workflow.

## Knowledge questions

### 1. What is the difference between a beat board, shot board, animatic, 3D previs, and techvis?

Expected answer:

- Beat board: key panels testing story arc or pitch.
- Shot board: shot-by-shot plan with framing, action, camera, duration, continuity, audio, and handoff notes.
- Animatic: timed board panels with scratch audio/SFX/music/captions and simple motion/cuts to test pacing.
- 3D previs: rough spatial/camera/blocking sequence for depth, action, lens/framing, and movement planning.
- Techvis: technical production diagram/specification for how to execute shots, equipment, VFX, stunt, virtual production, or set constraints.

Required points: identifies all five and connects each to the risk it answers. Penalize treating 3D previs as merely "higher quality storyboard."

### 2. Why should an AI agent create a continuity bible before writing per-shot generation prompts?

Expected answer:

- Multi-shot AI generation often drifts in identity, wardrobe, props, backgrounds, logos/text, and spatial relationships.
- A continuity bible centralizes recurring character, product, location, lighting, style, aspect, and forbidden-change constraints.
- Per-shot prompts then reuse only the relevant anchors while preserving stable references and pass/fail criteria.
- It enables targeted regeneration rather than redesigning the sequence after each failed output.

Required points: continuity risk, contents of bible, reuse across shots, review/regeneration value.

### 3. What does the 180-degree rule protect, and when may it be broken?

Expected answer:

- It protects viewer orientation, eyelines, screen direction, and spatial relationship across cuts.
- It is not an absolute law; breaking it may be valid when the intent is disorientation, power shift, altered perspective, chaos, or a clearly motivated geography reset.
- The board should mark the line of action, screen direction, and reason for any cross.

Penalize answers that call it mandatory in all cases or ignore intentional line-crossing.

### 4. What should be included in a generation-ready shot-board row?

Expected answer should include most of:

- Stable shot ID.
- Narrative beat/purpose.
- Duration/timing.
- Frame/shot size/angle/composition.
- Action/change during shot.
- Camera movement and motivation.
- Blocking, eyeline, screen direction, object path.
- Audio/dialogue/SFX/music/caption cue.
- Continuity anchors.
- Reference/provenance or AI prompt notes.
- Pass/fail or handoff notes.

Score full credit for equivalent fields. Penalize visual-only rows that omit story purpose, continuity, and review criteria.

### 5. Why must platform and aspect-ratio decisions be made before boarding?

Expected answer:

- Aspect ratio changes composition, typography, safe zones, subject placement, action path, caption/CTA design, and crop strategy.
- Platform UI, upload specs, duration limits, and viewer behavior can change, so volatile specs must be verified.
- Multi-aspect campaigns need protected action areas and variant-specific boards for text and crops.

Penalize claiming a 16:9 board can always be cropped to 9:16 without redesign.

## Production-decision scenarios

### Scenario 1: User asks, "Make me a storyboard for a 15-second TikTok ad from this product brief."

Strong decision:

- Confirm/derive vertical delivery and verify current TikTok specs if final specs matter.
- Build a 9:16 board with central action and safe-zone awareness.
- Start from hook/proof/payoff/CTA beats.
- Use stable shot IDs, short durations, product continuity anchors, caption/CTA plan, and AI generation pass/fail criteria.
- Avoid relying on generated text/logos; plan to composite final typography.

Weak decision:

- Produces landscape cinematic boards only.
- Makes generic "Shot 1: product appears" prompts.
- Omits product claim proof and CTA.
- Uses platform specs without dated verification.

### Scenario 2: Scripted dialogue scene has two actors facing each other in a kitchen, and the client wants it to feel calm and intimate.

Strong decision:

- Establish kitchen geography.
- Track the line of action between actors and keep cameras on one side for stable eyelines unless a motivated shift occurs.
- Use restrained shot/reverse shot, inserts, and close-ups for emotional beats.
- Mark props and actor positions.
- Avoid arbitrary orbiting or line-crossing movement that would disorient the audience.

Weak decision:

- Suggests constant camera moves or 360 coverage because it is more "dynamic."
- Does not plan eyelines or screen direction.

### Scenario 3: A sci-fi chase sequence involves a drone flying through a narrow industrial corridor with VFX and stunt beats.

Strong decision:

- Recommend 3D previs and possibly techvis rather than only a text board.
- Map corridor dimensions, obstacles, camera/drone path, subject paths, action beats, VFX elements, safety/stunt constraints, and cut points.
- Use animatic timing to test speed and comprehension.
- Provide shot-board rows plus overhead diagrams or spatial notes.

Weak decision:

- Generates polished concept frames without testing camera path or blocking.
- Treats impossible camera moves as production-ready without flagging feasibility.

### Scenario 4: A brand supplies five inspiration clips and asks the agent to "make it exactly like these."

Strong decision:

- Classify references by use: story, composition, motion, design, continuity, negative.
- Check provenance/rights and avoid cloning protected frames, living artists, brand identities, or performer likenesses.
- Translate references into observable traits: lighting, lens feel, pacing, blocking, palette, typography rhythm, etc.
- Provide a distinct board that serves the new brief.

Weak decision:

- Directs a model to copy a named director/artist or exact shot from unlicensed material.
- Uses references as a vague mood pile with no routing.

## Applied production task rubric

### Task A: Create a board plan from a brief

User request:

"Create a storyboard/previs plan for a 30-second vertical launch video for an AI calendar assistant. It should show a busy founder being saved from scheduling chaos. It will be generated with AI images/video and composited in edit. Need it to work with captions off and on."

Excellent response characteristics:

- States delivery promise and assumes/verifies 9:16 vertical.
- Splits story into coherent beats: chaos hook, assistant intervention, conflict resolved, proof/demo, emotional payoff, CTA.
- Provides a shot table with stable IDs, durations totaling about 30 seconds, camera/framing/action/audio/caption notes, continuity anchors, and prompt notes.
- Includes continuity bible: founder look, device/UI state, office setting, assistant visual metaphor, brand palette, forbidden generated text/logo issues.
- Plans silent-viewing captions and composite UI/text rather than trusting AI-generated readable UI.
- Flags AI limitations: UI text, identity drift, hand/device interactions, screen continuity.
- Provides pass/fail criteria and regeneration/compositing fallbacks.
- Includes review passes: story, timing, platform safe zone, brand/legal, generation feasibility.

Scoring, 40 points:

- Story/beat structure and timing: 8
- Shot-board specificity and stable IDs: 8
- Camera/blocking/continuity: 7
- AI prompt planning and limitation handling: 7
- Platform/caption/safe-zone planning: 5
- Review/handoff workflow: 5

Critical failures for this task:

- No shot IDs or timings.
- No continuity bible.
- Trusts AI to generate final UI text/logos.
- Ignores captions/silent viewing.

### Task B: Diagnose a flawed storyboard

User request:

"Here is my board: Shot 1 wide office, Shot 2 founder at desk, Shot 3 product UI, Shot 4 happy customer, Shot 5 logo. It feels boring. Fix it."

Excellent response characteristics:

- Diagnoses that the board lists subjects, not beats or changes.
- Adds a viewer question for each shot and creates a stronger cause-effect sequence.
- Introduces a hook/problem, visual escalation, product action proof, before/after contrast, and CTA.
- Specifies what changes within each shot.
- Adds camera movement only when motivated.
- Adds continuity anchors and UI/text compositing notes.
- Offers a revised shot table rather than only abstract advice.

Scoring, 25 points:

- Diagnosis of missing narrative/action: 5
- Revised beat structure: 6
- Concrete shot revisions: 6
- Continuity and platform/generation considerations: 5
- Clear review criteria: 3

### Task C: Write an animatic review note set

User request:

"I watched the animatic and it is confusing around the middle. What kind of notes should I give?"

Excellent response characteristics:

- Instructs the user/agent to give timecoded or shot-ID-specific notes.
- Separates story, geography, timing, brand/legal, generation feasibility, and audio/caption passes.
- Gives examples of precise notes such as screen direction reversal, action beginning after the cut, caption covering product, missing establishing shot, or ambiguous prop state.
- Recommends watching in real time and not only reading the shot table.
- Advises resolving conflicting stakeholder notes before regenerating assets.

Scoring, 20 points:

- Timecoded/shot-specific note guidance: 5
- Separate review passes: 5
- Concrete note examples: 5
- Real-time timing/comprehension emphasis: 3
- Conflict/iteration management: 2

## Source and evidence scoring

Award up to 15 points across any task for evidence discipline:

- 5: Clearly separates documented facts, empirical observations, and production heuristics.
- 4: Dates or rechecks volatile platform/tool/model facts when relevant.
- 3: Avoids unsupported universal claims such as "always use 9:16" or "AI preserves continuity."
- 3: Uses professional/official/academic grounding where consequential claims are made.

Deduct up to 10 points for:

- Citing only community or marketing sources for technical/platform claims.
- Using exact platform specs in final production without checking current official sources.
- Presenting current AI limitations as permanent facts without context, or current AI capabilities as guaranteed.

## Overall scoring guide

90-100: Production-ready. The agent plans story, spatial continuity, timing, platform constraints, AI generation, review, and handoff with evidence-aware judgment.

80-89: Usable with minor omissions. The agent covers most planning needs but may under-specify review, fallbacks, or reference provenance.

70-79: Partial. The response has useful board content but lacks important continuity, camera/blocking, prompt-planning, or platform details.

Below 70: Not production-safe. The response is generic, prompt-only, visually decorative, unsupported, or likely to cause expensive generation/production failures.
