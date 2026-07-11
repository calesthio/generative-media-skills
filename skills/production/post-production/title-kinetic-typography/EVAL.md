# Evaluation: title-kinetic-typography

Use this file as the answer key and scoring specification. The evaluated agent receives the production task and `SKILL.md` only.

Score for applied competence, not memorized phrasing. A strong response should make typography more readable, more intentional, safer, and easier to implement.

## Core competencies

An agent competent with this skill should:

- Classify the job of each text element before styling it.
- Build hierarchy across role, size, weight, case, position, value, and motion.
- Specify reveal, hold, and exit timing rather than only describing a visual style.
- Treat line breaks as editorial and localization-sensitive.
- Protect exact text fidelity, brand/legal copy, names, numbers, punctuation, and trademarks.
- Verify safe areas for the exact platform/placement and date volatile platform facts.
- Address accessibility: contrast, motion sensitivity, flashing, reading time, caption completeness, and color independence.
- Separate documented facts, empirical observations, and production heuristics.
- Prefer editable/rendered text layers when exact glyphs matter.
- Produce implementation handoffs with enough detail to build and QA.

## Knowledge questions

### 1. Why is "make cool kinetic typography" an insufficient direction?

Expected answer:

- It does not state the text job, exact text, hierarchy, target platform, safe area, timing, motion meaning, readability constraints, or deliverable form.
- It invites generic motion and can lead to unreadable or misspelled text.
- A stronger direction specifies exact copy, roles, layout, reveal/hold/exit, motion semantics, background relationship, accessibility limits, and QA.

Required points: text job, exact copy/fidelity, timing, readability/safe area, motion semantics.

Penalize:

- Treating style adjectives as enough.
- Omitting exact text or readable hold.

### 2. What are reveal, hold, and exit, and why do they matter?

Expected answer:

- Reveal establishes attention and tone.
- Hold gives enough stable time for comprehension.
- Exit punctuates the beat, prepares the cut/next idea, and should not remove text before it is read.
- All three must be timed to edit/audio/attention, not only seconds.

Required points: purpose of each state; readable hold; relation to edit/audio.

### 3. How should an agent handle exact typography when using AI image or video generation?

Expected answer:

- Recognize that many generative image/video systems can corrupt exact lettering, punctuation, kerning, logos, and multilingual text.
- Use generated media for background/mood/plates when needed, then render exact text as editable layers or a controlled compositor when fidelity matters.
- Proof text after generation and escalate if exact legal/brand text cannot be guaranteed.

Required points: risk, layer/render workaround, proofing/escalation.

Critical failure: claiming AI generators can be trusted for all exact text without review.

### 4. What accessibility and safety checks apply to kinetic typography?

Expected answer:

- Contrast across worst frames.
- Reading time and stable holds.
- No more than three flashes per second unless below threshold; safer to avoid high-contrast flashing.
- Motion sensitivity: avoid unnecessary shake/zoom/oscillation and provide/recommend reduced-motion alternatives where possible.
- Do not rely on color alone.
- Captions-as-design must include essential speech and non-speech audio if replacing captions.

Required points: flash safety, contrast, reading time, motion sensitivity, caption completeness or color independence.

### 5. Why are line breaks localization-sensitive?

Expected answer:

- Scripts and locales use different line-breaking, shaping, spacing, punctuation, and reading-direction rules.
- English word-wrap assumptions do not apply universally.
- Arabic/Indic shaping, RTL reveal order, CJK punctuation rules, and languages without visible spaces require appropriate engines/review.
- Translation expansion can break boxes/timing; agents should define meaning locks and layout locks and escalate conflicts.

Required points: script-specific rules; at least two examples; expansion/escalation.

### 6. How should safe-zone facts be handled?

Expected answer:

- Treat platform UI/ad overlays as volatile.
- Verify against official/current tooling for the exact placement/account/export date.
- Keep critical text/logos inside safe areas; make platform-specific versions when needed.
- Do not assume TikTok, Reels, Shorts, and ads share identical safe zones.

Required points: volatility, verification, critical elements, platform variants.

Penalize:

- Presenting a single universal safe-zone rectangle as permanently correct.

## Production-decision scenarios

### Scenario A: AI-generated launch video with exact title

User asks: "Make a 12-second AI video with the words `NOVA-7™ is here` flying through smoke. It has to be spelled exactly."

Strong decision:

- Generate or source the smoke/background separately if needed.
- Render `NOVA-7™ is here` as controlled editable typography or composited layer.
- Specify type, safe area, reveal/hold/exit, contrast/backing, and exact text QA.
- Avoid relying on the video model to generate final glyphs.

Scoring:

- 4: Identifies text-fidelity risk and proposes layered implementation with timing/QA.
- 3: Mentions risk and proofing but lacks full timing or handoff detail.
- 2: Vague warning without a workable plan.
- 1: Uses AI prompt only and hopes spelling is correct.
- 0: Changes the text or omits the trademark symbol.

Critical failures:

- Dropping `™`, changing capitalization, or saying exact lettering is guaranteed without validation.

### Scenario B: Dense explainer captions

User asks: "Animate every word of this 90-second finance explainer in bouncing captions so it feels energetic."

Strong decision:

- Push back on animating every word if it harms comprehension.
- Propose phrase-level or keyword-level kinetic captions with readable holds and accessible caption completeness.
- Use hierarchy, two-line limit where feasible, backing plates/contrast, and timing to speech phrase boundaries.
- Maintain an accessibility caption track if designed captions become too selective.

Scoring:

- 4: Balances energy with readability and accessibility, offers concrete system.
- 3: Good readability guidance but weak caption/accessibility plan.
- 2: Generic "slow it down" advice.
- 1: Accepts every-word bouncing without concern.
- 0: Removes captions or ignores speech meaning.

### Scenario C: Multi-platform vertical ad

User asks: "One 9:16 text-heavy ad for TikTok, Reels, Shorts, and paid placements."

Strong decision:

- Explain that platform overlays differ and can change.
- Keep core headline/CTA in a conservative central safe band.
- Recommend platform-specific exports or at minimum separate CTA/lower-third positions.
- Verify safe zones in current official tools/preview for each placement.
- Date any volatile platform facts.

Scoring:

- 4: Clear platform-variant strategy with verification and safe central hierarchy.
- 3: Mentions safe areas but lacks variant/export plan.
- 2: Uses generic margins without verification.
- 1: Places key text near bottom/right because it "usually works."
- 0: Claims all 9:16 platforms share one safe zone.

### Scenario D: Localized title sequence

User asks: "Translate this English kinetic title into Arabic, Japanese, and Thai; keep the same animation exactly."

Strong decision:

- Reject "same animation exactly" as a risky constraint.
- Preserve meaning, timing intent, and brand feel while adapting shaping, reading direction, line breaking, and expansion.
- Use proper text engines and native/locale review.
- Define meaning locks and layout locks; escalate if conflicts occur.
- Avoid animating isolated glyphs where it breaks shaping or readability.

Scoring:

- 4: Addresses all three language/script issues and proposes adaptive variants.
- 3: Good RTL/CJK discussion but misses Thai/no-space or shaping risk.
- 2: General localization warning with little implementation detail.
- 1: Mirrors English layout and direction only.
- 0: Suggests manual glyph rearrangement that breaks scripts.

### Scenario E: Flashy music title

User asks: "Make the chorus title strobe white/red as fast as possible for intensity."

Strong decision:

- Identify seizure/flash risk.
- Avoid more than three flashes per second unless formally tested below threshold; recommend a safer alternative such as a single impact flash, wipe, pulse, blur, scale hit, or color accent.
- Preserve musical intensity through rhythm, cuts, scale, masks, or camera moves.
- Check contrast and device playback.

Scoring:

- 4: Clear safety refusal/adjustment plus creative alternative.
- 3: Mentions safety and slows strobe but weak alternative.
- 2: Vague "be careful" without threshold/plan.
- 1: Creates rapid strobe without safety check.
- 0: Encourages maximum flashing.

## Applied production task

### Task: Write a kinetic typography handoff

User request:

"Create the title/caption system for a 20-second vertical product teaser for a sleep app. Brand is calm, premium, and science-backed. Exact line: `Fall asleep 37% faster` and CTA: `Try tonight`. It will run on Reels, TikTok, and Shorts, mostly muted."

Expected approach:

- Define text jobs: hook/claim and CTA.
- Protect exact claim, number, and CTA.
- Use calm premium type choices and restrained motion.
- Put critical text in conservative central safe area and note platform-specific verification.
- Provide reveal/hold/exit timing and muted-first comprehension.
- Include contrast/backing over likely dark/night footage.
- Avoid flashy or overly energetic motion.
- Include accessibility checks, legal/claim review, and phone/platform QA.

Rubric, 20 points:

- Text role and hierarchy: 3 points.
- Exact copy fidelity and claim/legal review: 3 points.
- Layout/safe-area plan for multi-platform vertical delivery: 3 points.
- Timing with reveal/hold/exit: 4 points.
- Motion semantics matching calm/premium/science-backed brand: 3 points.
- Accessibility/readability checks: 3 points.
- Implementation clarity: 1 point.

Critical failures:

- Changes `37%`, removes the claim context, or invents unsupported medical certainty.
- Places CTA only in bottom platform UI risk zone.
- Uses rapid flashing/strobing for a sleep app.
- Provides only a vague visual mood without buildable timing/layout details.

## Scoring guidance

Overall:

- Excellent: Makes text decisions specific, buildable, readable, localized/safe where relevant, and grounded in constraints.
- Good: Covers most practical issues but misses one deeper risk such as localization, captions, or volatile safe-zone verification.
- Marginal: Gives general design advice without enough timing, text fidelity, or QA.
- Poor: Treats kinetic typography as decorative effects and ignores readability, accessibility, exact text, or platform constraints.

Disqualifying patterns:

- Exposes or references this evaluation file to the production agent.
- Fabricates official platform specs without verification.
- Claims universal rules where the skill asks for context-sensitive decisions.
- Ignores WCAG-style flash safety when asked for strobing/flashing.
- Silently changes required copy, legal text, names, numbers, or trademarks.
