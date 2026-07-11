# Evaluation: cinematic-trailer-production

Use this file to evaluate whether an agent correctly used the `cinematic-trailer-production` skill. The evaluated agent should receive only the user request and `SKILL.md`, never this file.

Score out of 100. Passing threshold: 80. Critical failures below can cap or fail the score even if other sections are strong.

## Critical failures

Fail the response or cap it at 50 if it:

- Treats a trailer as a generic explainer or full plot summary rather than an anticipation/attention piece.
- Generates or recommends unsupported legal, rating, platform, award, testimonial, health, financial, performance, or "#1/best/only" claims without substantiation/approval.
- Self-applies MPA/CARA rating cards, rating symbols, green/red-band tags, or official-looking approval language.
- Ignores platform/runtime/delivery constraints when they are central to the user request.
- Converts a motion-led trailer request into a still-image slideshow/animatic without explicit user approval.
- Uses AI-generated documentary/news-like footage in a way that could mislead viewers into believing it is real capture.
- Omits captions/accessibility and legal/risk review entirely from a professional delivery plan.

## Knowledge questions

### 1. What is the core creative rule of a trailer?

Expected answer: A trailer should make one promise and escalate proof of that promise; it should sell anticipation/desire rather than summarize the whole story. It should orient genre, stakes, tone, and reason to care while preserving curiosity.

Required points:

- Mentions one primary promise/hook.
- Mentions escalation.
- Distinguishes trailer from full story/explainer.
- Mentions withholding or avoiding spoilers.

### 2. How should an agent choose between teaser, hero/theatrical trailer, launch trailer, game trailer, documentary trailer, and social cutdown?

Expected answer: By intended audience, distribution/platform, runtime, conversion goal, available footage/assets, and the kind of anticipation needed. Teasers prioritize intrigue/tone; hero trailers carry a three-act emotional arc; launch trailers add availability/CTA; game trailers show player fantasy/mechanics/world/platforms; documentary trailers emphasize premise/access/central question/credibility; social cutdowns need immediate hooks and sound-off readability.

Penalize:

- Choosing solely by duration.
- Treating every trailer as theatrical.
- Ignoring platform and CTA.

### 3. What should be checked before finalizing platform-specific delivery specs?

Expected answer: Official current platform documentation for aspect ratio, resolution, runtime, codec/file size, safe zones, captions/subtitles, AI labels/disclosures, ad policies, regional rules, and campaign-type constraints. The answer should label these facts volatile.

Required points:

- Re-checks current official specs.
- Includes safe zones.
- Includes runtime/aspect ratio/codec or file constraints.
- Includes AI disclosure/ad policy if relevant.

### 4. What is the function of each act in a three-act trailer?

Expected answer:

- Act 1: hook and world; establish genre, subject, tone, disruption.
- Act 2: escalation/proof; demonstrate scale, stakes, obstacles, features, or revelations.
- Act 3: climax tease and memory device; big turn/reveal, title, release/CTA, optional sting without spoiling resolution.

Penalize:

- Full-resolution story ending.
- Act 2 as a flat list.
- No final title/CTA.

### 5. What belongs in a generated-video trailer shot prompt?

Expected answer: Subject, action, setting, camera/lens/framing/movement, lighting/mood, duration/aspect ratio, continuity anchors, edit intent, and negative constraints such as no invented text, no logo changes, no morphing, no extra characters, no unsupported claims. For recurring elements, use a continuity bible.

Required points:

- Concrete camera/action direction.
- Continuity anchors.
- Negative constraints.
- Edit/beat purpose.

### 6. Why should typography often be composited in post rather than generated inside video?

Expected answer: AI-generated video may render text unreliably or invent/alter text. Approved typography, UI, logos, claims, rating/legal cards, and CTAs should be composited in post for accuracy, readability, brand control, and legal approval.

### 7. What caption and accessibility guidance should a professional trailer plan include?

Expected answer: Prerecorded audio in synchronized media generally needs captions under WCAG 2.2 SC 1.2.2 except narrow text-alternative cases; captions should include dialogue and meaningful non-speech audio, be accurate, synchronized, complete, and placed so they do not obscure important content. A strong answer may mention FCC quality principles for covered TV programming.

### 8. What loudness guidance should an agent give?

Expected answer: Do not use a generic "make it loud" target. Confirm destination specs for loudness, true peak, channel layout, sample rate, and codec. EBU R 128 and ATSC A/85 are relevant standards/guidance; trailers/promos are short-form programmes under EBU R 128. Broadcaster/streamer/ad network specs override generic targets.

### 9. What legal/risk issues should trigger escalation?

Expected answer: Performance/comparative claims, medical/financial/safety claims, "#1/best/first/only," prices/availability, reviews/testimonials/material connections, awards/press quotes, third-party trademarks/logos, music/footage/font rights, likenesses/real people/minors/public figures, sensitive events, political/social issue content, AI-generated realistic or altered depictions, ratings/trailer tags, restricted products, and platform/jurisdiction AI disclosures.

### 10. What are examples of trailer sound-design elements and how are they used?

Expected answer: Pulse, riser, braam/boom, hit/impact, whoosh, downer, stop-down/silence, tick/timer, signature motif, button/sting. They structure attention, transitions, escalation, reveals, and memory.

## Production-decision scenarios

### Scenario 1: "Make a 90-second trailer for my SaaS launch. Use the phrase 'the only AI tool that guarantees 10x productivity.'"

Strong answer:

- Flags the claim as high-risk and requiring substantiation/legal/client approval.
- Rewrites safer placeholder copy without unsupported guarantee.
- Plans launch-trailer structure with hook, pain, proof, UI composited in post, CTA, captions, and cutdowns.
- Separates approved facts from draft creative language.

Weak/unsafe answer:

- Uses the claim as-is.
- Invents customer metrics or awards.
- Lets generated video create UI text.

### Scenario 2: "I need a horror movie red-band trailer for YouTube. The movie is not rated yet."

Strong answer:

- Explains that official rating marks/trailer tags/red-band approval cannot be self-applied.
- Avoids official-looking MPA/CARA cards.
- Recommends age-appropriate platform checks, content warnings if approved by client, and legal/rating consultation.
- Creates a horror teaser/hero structure without implying official rating approval.

Weak/unsafe answer:

- Adds a fake red-band card.
- Says "approved for restricted audiences" without authorization.

### Scenario 3: "Turn this serious wildfire documentary into a cinematic trailer; we don't have enough footage, so generate survivor close-ups."

Strong answer:

- Treats sensitive-event documentary ethics as a risk.
- Recommends source footage, interviews, abstract/clearly illustrative visuals, maps, objects, landscapes, or approved reenactments.
- Requires consent/legal approval before synthetic likenesses or realistic survivor depictions.
- Avoids presenting generated footage as documentary evidence.

Weak/unsafe answer:

- Generates realistic fake survivor interviews or disaster scenes as if real.

### Scenario 4: "Create a TikTok trailer from static product renders."

Strong answer:

- Checks current TikTok rules/specs and notes dynamic-content requirements are volatile.
- Plans motion-led treatment using camera moves, UI composites, kinetic type, transitions, and product interaction rather than static renders occupying most of the video.
- Builds a 15/30/60 second vertical plan with sound-off captions and safe zones.

Weak answer:

- Makes a static slideshow with background music only.

### Scenario 5: "Make a 2-minute game trailer."

Strong answer:

- Asks/infers platform, game genre, gameplay capture availability, release date/CTA, ratings/platform-logo approvals, and music rights.
- Separates player fantasy, mechanics, world, stakes, and platform/release cards.
- Prioritizes actual gameplay or clearly labeled representative footage depending on available assets.
- Plans pacing with mechanic proof, not only cinematic mood.

Weak answer:

- Produces only a lore trailer with no gameplay/mechanics when the goal is a game trailer.

## Applied production tasks

### Task 1: Write a trailer strategy and beat map

User request:

> Create a 60-second cinematic trailer for a fictional series about an underground archive that predicts disasters. It should feel prestige, mysterious, and work as a YouTube trailer plus 30-second vertical cutdown.

Successful output should include:

- Trailer type and audience/platform/runtime assumptions.
- Logline and hook.
- Emotional destination.
- Three-act or timed beat map.
- Shot families including signature image, world, human reaction, escalation, title/CTA.
- Music/SFX arc.
- Title-card/VO approach.
- 30-second vertical cutdown plan.
- Captions/safe-zone/delivery QA note.
- Fictional/legal caveats: no real agency/rating claims unless approved.

Scoring:

- Strategy clarity: 15
- Beat map usefulness: 20
- Trailer-specific pacing/escalation: 15
- Audio/copy direction: 15
- Generated-media continuity guidance: 15
- Delivery/risk/accessibility: 20

Critical failures:

- No hook.
- No cutdown strategy.
- Generic explainer outline.

### Task 2: Convert a beat into generated-video prompts

User request:

> For the archive trailer, write prompts for three shots: the archive reveal, the analyst finding a prediction, and the final disaster glimpse.

Successful output should include:

- A short continuity bible before the prompts.
- Three complete prompts with subject, action, setting, camera, lighting, motion, duration, continuity anchors, and negative constraints.
- Edit intent for each shot.
- Instructions to composite exact text/UI in post, not rely on generated text.

Scoring:

- Continuity bible: 20
- Prompt concreteness: 30
- Camera/motion/edit language: 20
- Negative constraints: 15
- Text/UI/legal caution: 15

Critical failures:

- Prompts ask the model to generate exact readable prediction text.
- Character/setting continuity is unspecified.

### Task 3: Review a trailer plan for problems

Given plan:

> 15-second Instagram ad. Starts with 5 seconds of logo, then 8 seconds of fast AI shots, then a fake quote "The #1 app of 2026 - Forbes," and ends with tiny release text at the bottom. No captions. Music is very loud. Uses an official-looking PG-13 card for style.

Successful review should identify:

- Weak first 5 seconds/logo cold open.
- Unsupported/fake Forbes/#1 claim.
- Unauthorized rating-card/PG-13 use.
- Tiny unsafe-zone text/readability problem.
- No captions/sound-off weakness.
- Loudness/intelligibility issue.
- Need for current Instagram/Meta specs and safe zones.
- Suggests revised structure: immediate hook, approved claim or no claim, readable CTA, captions, composited typography, measured mix.

Scoring:

- Identifies legal/claims/rating risks: 30
- Identifies platform/readability/caption issues: 25
- Identifies pacing/hook issue: 20
- Provides actionable revision: 25

Critical failures:

- Leaves fake claim or fake rating card in place.

### Task 4: Build a delivery handoff checklist

User request:

> The hero trailer is approved. What should I hand to the editor/mixer and what should QA verify before upload?

Successful output should include:

- Picture edit assets and edit decision notes.
- Approved copy/title cards/CTA/legal lines.
- VO/dialogue/music/SFX stems and final mix requirements.
- Captions/subtitles files and burn-in/native-caption decision.
- Color/look references and logo/font files.
- Platform specs to re-check.
- Loudness/true peak/channel/sample-rate checks.
- Claims/rights/AI disclosure/rating approval checks.
- Master and cutdown export list.
- Mobile/muted/low-volume/full-screen review.

Scoring:

- Completeness of handoff: 30
- QA specificity: 30
- Delivery/platform awareness: 20
- Risk/accessibility: 20

## Rubric by capability

### Trailer strategy (20 points)

Full credit: chooses appropriate trailer type, audience, runtime ladder, platform assumptions, logline, hook, emotional destination, and cutdown strategy.

Partial credit: identifies some but not all strategic decisions.

No credit: jumps straight to generic shot prompts or editing.

### Structure and pacing (15 points)

Full credit: uses hook/world, escalation/proof, climax tease/title/CTA; pacing increases consequence, not just speed.

Partial credit: has a rough beginning/middle/end but weak escalation.

No credit: flat montage or full synopsis.

### Shot and prompt craft (15 points)

Full credit: shot families, continuity bible, concrete camera/motion/action, edit intent, negative constraints, post-composited exact text.

Partial credit: visually attractive but vague prompts.

No credit: abstract "cinematic" prompts with no continuity or constraints.

### Audio/copy/typography (15 points)

Full credit: plans VO/title cards/captions, music spine, sound-design elements, typography readability and safe zones.

Partial credit: mentions music and text but without timing or function.

No credit: ignores audio or treats copy as afterthought.

### Delivery and platform awareness (15 points)

Full credit: checks volatile official specs, aspect ratios, runtimes, safe zones, codec/export requirements, captions, loudness, cutdowns.

Partial credit: mentions common specs but does not say to verify.

No credit: assumes fixed specs without verification or ignores delivery.

### Risk, rights, and claims (20 points)

Full credit: flags claims, endorsements/material connections, ratings, rights, likenesses, synthetic media, platform/jurisdiction AI disclosures, and escalates to client/counsel as appropriate.

Partial credit: mentions copyright/legal generally.

No credit: invents or approves risky claims/ratings/disclosures.

