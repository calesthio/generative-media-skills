---
name: cinematic-trailer-production
description: Provider-independent cinematic trailer production for AI agents creating movie-style trailers, teaser trailers, launch trailers, game trailers, documentary trailers, series promos, and high-impact generated-media previews. Use for trailer strategy, structure, shot planning, voiceover/title-card copy, music and sound-design direction, generated-video prompt translation, edit pacing, platform/runtime choices, delivery handoff, rights/claims caveats, and trailer QA.
---

# Cinematic Trailer Production

Use this skill when the user wants a trailer-like video: a movie-style trailer, teaser, launch trailer, game trailer, documentary trailer, series promo, event reveal, high-impact product preview, or social cutdown that sells anticipation rather than fully explaining everything.

This is a production discipline skill, not a provider manual. Pair it with the relevant local pipeline, generation-provider skill, editing/composition skill, and delivery tool instructions before calling tools or exporting files.

## Core rule

Make one promise, then escalate proof of that promise.

A trailer is not a miniature full story. It is an engineered desire machine: the audience should understand the genre, stakes, tone, and reason to care while still wanting the full release. Every beat, shot, caption, sound cue, and title card should earn attention or increase anticipation.

## Start with the trailer brief

Before writing prompts or generating clips, lock these decisions:

1. **Trailer type**
   - Teaser: intrigue, tone, one image or question, usually minimal plot.
   - Theatrical/hero trailer: complete emotional arc, stakes, characters/product promise, climax tease.
   - Launch trailer: availability and conversion; spectacle plus clear release/CTA.
   - Game trailer: player fantasy, mechanics, world, loop, platforms, release/CTA.
   - Documentary trailer: premise, access, central question, credibility, emotional stakes.
   - Series promo: world, ensemble, recurring engine, season hook.
   - Social cutdown: one hook, fast proof, native vertical composition, minimal dependence on sound.
2. **Audience and distribution**
   - Primary platform and aspect ratio.
   - Runtime target and whether shorter cutdowns are required.
   - Sound-on versus sound-optional environment.
   - Accessibility/captions requirement.
   - Ratings, claims, disclosure, and legal review constraints.
3. **One-sentence logline**
   - Format: "When [inciting pressure], [subject] must [action/choice] before [stakes/consequence]."
   - For products: "For [audience] facing [pain], [product] makes [transformation] possible by [proof/mechanism]."
4. **Hook**
   - The first 3-5 seconds must contain an image, line, question, contradiction, deadline, or sonic event strong enough to survive scrolling.
5. **Emotional destination**
   - Choose the final feeling: dread, awe, urgency, triumph, mystery, rebellion, tenderness, prestige, discovery, FOMO, or trust.

If the user supplies only a broad request ("make it cinematic"), ask for the missing release object, audience, platform, runtime, and must-include/must-avoid items. If production must proceed, assume a 60-90 second hero trailer plus 30/15/6 second cutdowns and state that assumption.

## Runtime and format strategy

Treat platform and ad-spec facts as volatile. Re-check official platform specifications at production time, especially duration limits, AI labels, safe zones, codec requirements, ad policies, and regional rules.

As of verification on 2026-07-10:

- YouTube video ads recommend 1080p assets in 16:9, 9:16, or 1:1, with safe zones for overlays and CTAs; Google states format-specific length varies and should be checked by campaign type. Skippable in-stream ads allow broad runtime flexibility but list best-practice durations such as 15-20 seconds for awareness/action and 2-3 minutes for consideration. Sources: Google Ads video ad specs and skippable in-stream specs.
- YouTube upload guidance says the player adapts to vertical and square aspect ratios, and lists recommended bitrates/audio bitrates by resolution. Source: YouTube recommended upload encoding settings.
- TikTok's ad format and functionality policy currently requires legible high-resolution video, 5-60 seconds duration, standard video sizes including 9:16, 1:1, and 16:9, audio that is not poor quality, and dynamic content rather than mostly static imagery. Product- and placement-specific TikTok spec pages can differ, so verify the selected campaign/ad product before delivery. Source: TikTok ad format and functionality policy.
- Meta ad specs and placement rules change often and may require login or locale-specific pages. Re-check the relevant Meta Ads Guide/Business Help placement immediately before delivery.

Practical runtime map:

| Deliverable | Best use | Common structure |
|---|---|---|
| 6 seconds | Bumper, recall, reveal sting | Logo/subject + one shock/benefit + date/CTA |
| 10-15 seconds | Social hook, paid awareness | Hook + proof montage + CTA |
| 20-30 seconds | Social trailer, launch cut | Hook + stakes + 3 proof shots + final card |
| 45-60 seconds | Teaser/short trailer | Cold open + premise + escalation + tease |
| 75-120 seconds | Hero trailer | Three-act emotional arc with escalation and climax tease |
| 2-3 minutes | Deep theatrical/consideration trailer | More setup, dialogue, scenes, and story texture |

Prefer planning one master trailer and derivative cutdowns together. A strong 90-second hero trailer usually does not automatically become a strong 15-second ad; the short version often needs a different opening, fewer plot beats, larger captions, and a clearer CTA.

## Trailer structure

Use a three-act trailer shape unless the user requests an experimental piece.

### Act 1: Hook and world

Goal: establish genre, subject, tonal contract, and the reason to watch.

Typical beats:

- Cold open: arresting image, line, sound, statistic, or question.
- World state: where/when/what kind of reality.
- Disruption: what changes.
- Character/product promise: who or what carries the trailer.

Generated-media note: act 1 is where continuity is most fragile. Build a visual bible before generation: character look, environment, palette, lens language, time of day, logo/product state, and forbidden variations.

### Act 2: Escalation and proof

Goal: demonstrate scale and stakes without resolving the story.

Typical beats:

- Montage of attempts, obstacles, capabilities, or revelations.
- Voiceover or title cards clarify the premise.
- Music adds percussion, pulse, or harmonic lift.
- Scenes grow in movement, contrast, stakes, and shot size.
- Insert one quiet beat to reset attention before the final escalation.

Do not make act 2 a flat list. Each shot should answer "and therefore?" or "but then?" rather than "and also."

### Act 3: Climax tease and memory device

Goal: make the audience remember the title, release moment, and feeling.

Typical beats:

- Big turn, impossible image, confrontation, feature reveal, or emotional line.
- Music stop, downbeat, riser, impact, or silence.
- Title reveal.
- Release/CTA card.
- Optional button joke, sting, or final mystery image.

Never spoil the final resolution unless the trailer's purpose is conversion for an already-known product where clarity beats mystery.

## Beat map template

Use this as a planning scaffold, not a fixed formula.

| Time | Function | Picture | Audio | Copy |
|---:|---|---|---|---|
| 0-3s | Pattern interrupt | Impossible image, face, motion, threat, or product transformation | Hit, breath, glitch, silence, or first VO line | Optional 3-6 word hook |
| 3-10s | Context | Establish world or pain | Pulse begins | "In a world..." only if intentionally genre-aware |
| 10-25s | Inciting pressure | The change, mission, launch, discovery | Bass, ticking, first rise | Premise card or line |
| 25-45s | Proof montage | 4-8 shots showing scale/benefits/obstacles | Percussion, impacts, whooshes | Reviews, claims, or feature cards only if substantiated |
| 45-60s | Human/emotional beat | Quiet close-up, witness, pause, product-in-use | Drop out or thin texture | One line that reframes stakes |
| 60-80s | Final escalation | Fast cuts, strongest visuals, collision of forces | Full trailerization, risers, braams, hits | Minimal copy |
| 80-90s | Title and CTA | Title treatment, release date, platform, logo | Tail, final hit | Exact release/CTA/legal card |

For a 30-second version, compress to: 0-2 hook, 2-8 context, 8-20 proof escalation, 20-26 climax tease, 26-30 title/CTA. For 15 seconds, skip exposition and let the first line or title card carry context.

## Shot list design

Plan shots by trailer function rather than by visual prettiness.

Required shot families for most cinematic trailers:

- **Signature image**: the image the audience remembers.
- **World/wide shot**: scale, geography, genre.
- **Character/product hero shot**: subject identity and desirability.
- **Threat/friction shot**: antagonist, obstacle, pain, countdown, or market pressure.
- **Action/proof shot**: movement, capability, mechanic, transformation, or consequence.
- **Human reaction shot**: face, hand, breath, witness, user, fan, player, customer.
- **Texture inserts**: objects, UI, evidence, maps, newspaper, controls, artifacts, particles.
- **Escalation shot**: bigger motion, danger, speed, crowd, reveal, or impossible event.
- **Title/CTA shot**: clean enough to carry typography.

For AI-generated video, give every shot a continuity role:

- `subject_id`: recurring person/object/product.
- `setting_id`: environment and time.
- `story_beat`: why this shot exists.
- `camera`: lens feel, movement, framing, depth.
- `action`: one clear action, not a paragraph of events.
- `continuity anchors`: wardrobe, logo placement, color palette, props, weather, UI state.
- `negative constraints`: no extra fingers, no changing logo, no unreadable text, no random characters, no morphing, no flicker, no invented claims.
- `handoff`: exact first/last frame intent if stitching shots.

## Translating a trailer plan into generated-video prompts

Most video models respond better to concrete shot direction than to abstract genre labels. Translate "cinematic trailer" into specific visual, temporal, and editorial instructions.

Use this prompt stack:

1. **Continuity bible**
   - Characters/products, wardrobe/materials, palette, environments, era, camera language, aspect ratio, and typography restrictions.
2. **Shot prompt**
   - Subject + action + setting + camera + lighting + mood + duration + composition + continuity anchors.
3. **Motion contract**
   - What moves, how fast, where the camera moves, what must stay stable.
4. **Edit intent**
   - What shot precedes/follows and what beat it serves.
5. **Avoid list**
   - Model-specific failure risks and legal/brand restrictions.

Example shot prompt:

> A lone astronaut in a scratched white EVA suit stands at the edge of a black-glass crater under a pale blue sunrise, visor reflecting a distant city buried under ice. Slow 35mm push-in from wide to medium, subtle handheld drift, cold rim light, volumetric haze, grounded sci-fi realism, tense silence before impact. The astronaut's suit markings, orange wrist tether, and cracked left shoulder plate must match all other shots. No readable invented text, no extra people, no logo changes, no morphing helmet.

For product trailers, replace vague cinematic effects with product truth:

> Macro close-up of the actual matte-black device on a walnut desk, thumb presses the side button, screen wakes to the approved dashboard UI mockup, shallow depth of field, controlled studio reflections, smooth slider move left to right, premium launch-film lighting. Keep device proportions, logo, and UI layout identical to reference. No invented UI text or unsupported feature claims.

If a model cannot preserve continuity across shots, switch to one of these strategies:

- Generate fewer, longer shots with in-shot reframing.
- Use reference images or locked character/product sheets if the provider supports them.
- Use still-image keyframes plus controlled motion for hero/product shots.
- Hide continuity seams with silhouettes, inserts, POV shots, typography, speed ramps, match cuts, whip pans, light leaks, or sound bridges.
- Use editorial repetition: the same color, prop, shape, or sound cue can maintain identity even when exact character continuity varies.

## Voiceover, dialogue, and title-card direction

Use fewer words than a normal explainer. Trailer copy should create pressure and rhythm.

Strong trailer copy is:

- specific enough to orient the audience;
- incomplete enough to preserve curiosity;
- short enough to read while the cut keeps moving;
- timed as punctuation, not wallpaper;
- legally safe and substantiated when making claims.

Avoid generic lines unless parodying the form:

- "Everything will change."
- "The future is here."
- "In a world..."
- "You've never seen anything like this."
- "The ultimate solution."

Better patterns:

- "The signal arrived 12 minutes after Earth went dark."
- "One city. Seven nights. No exits."
- "Every forecast was wrong."
- "Build faster than the market can move."
- "The launch window closes Friday."

Use title cards when:

- the trailer must work without sound;
- plot context would be awkward as VO;
- claims need exact approved wording;
- brand/product names must land visually;
- pacing needs hard punctuation.

Use VO/dialogue when:

- human emotion or authority matters;
- documentary credibility depends on a real participant;
- the trailer needs a whispered hook, confession, or command;
- social captions can carry text but audio adds intimacy.

For captions, plan them from the script stage. W3C WCAG 2.2 SC 1.2.2 requires captions for prerecorded audio in synchronized media, except narrow text-alternative cases. FCC caption quality guidance for covered television programming emphasizes accuracy, synchronicity, completeness, and placement. Even when not legally required, trailers should ship with accurate captions/subtitles and a text-safe layout.

## Music and sound-design language

Trailer audio often carries more structure than dialogue. Design the sound arc before editing.

Common trailer audio elements:

- **Pulse**: low rhythmic element that starts tension.
- **Riser**: increasing pitch/noise/energy into a transition.
- **Braam/boom**: large low impact, often for reveals.
- **Hit/impact**: percussive cut punctuation.
- **Whoosh/swish**: movement or transition accent.
- **Downer**: falling tone for dread or reversal.
- **Stop-down**: sudden silence or thin audio before a reveal.
- **Tick/timer**: urgency and countdown.
- **Signature motif**: a memorable two- or three-note identity.
- **Button/sting**: short final joke, scare, or memory cue after title.

Build music in phases:

1. Sparse hook: texture, breath, isolated sound, or silence.
2. Pulse: tempo and movement begin.
3. First lift: harmonic or percussion expansion.
4. Drop/reset: attention reset and emotional line.
5. Final build: denser rhythm, faster cuts, bigger impacts.
6. Tail: title hit, release card, optional sting.

Do not crush the mix just to feel "epic." Check loudness against the delivery target. EBU R 128 and its R 128 s1 short-form supplement address loudness normalization and true-peak controls for short-form items such as trailers/promos; ATSC A/85 provides loudness guidance for television and streaming-media audio workflows. If delivering to a broadcaster, streamer, ad network, or cinema, use the client/platform spec rather than a generic web target.

Practical mix handoff:

- Separate dialogue/VO, music, SFX, and final mix stems when possible.
- Confirm loudness target, true-peak ceiling, channel layout, sample rate, and codec with the destination.
- Keep dialogue intelligible in phone speakers and noisy environments.
- Use captions and on-screen cards for critical information that may be missed in sound-off playback.
- Watch the trailer once at low volume and once muted before approval.

## Pacing and escalation

Escalation is not only faster cutting. It is increasing consequence.

Use multiple escalation lanes:

- shot size: wide -> medium -> close -> macro/impact;
- motion: stillness -> drift -> travel -> collision;
- stakes: curiosity -> danger/opportunity -> deadline -> irreversible choice;
- sound: texture -> pulse -> rhythm -> full hits -> stop-down;
- copy: question -> premise -> warning/proof -> title;
- color/light: neutral -> contrast -> extremes or brand color takeover.

Cut faster only when the audience already understands what they are seeing. If every shot is a new concept, rapid cutting creates noise instead of momentum.

Use transitions with intent:

- **Hard cut**: confidence, impact, comedy, threat.
- **Match cut**: continuity across time/space or product transformation.
- **Smash cut to silence**: shock or tonal pivot.
- **Whip pan/light wipe**: speed, social energy, hiding AI seams.
- **Dip to black**: gravity, chapter break, prestige, horror.
- **Glitch/datamosh**: tech, instability, signal corruption; overuse cheapens prestige.
- **J-cut/L-cut**: audio leads or trails picture, essential for polished trailers.

If the trailer feels flat, diagnose the lane that is not escalating. Often the fix is a quieter midpoint, a more specific threat, or a stronger final image-not more effects.

## Typography and title treatment

Typography must survive motion, compression, mobile screens, and platform UI overlays.

Rules:

- Keep title cards short: usually 2-7 words.
- Use large type and generous contrast.
- Avoid thin strokes and low-contrast glows for mobile.
- Keep key text inside platform safe zones.
- Do not rely on AI-generated video to render exact text unless the provider is proven reliable; composite approved text in post.
- Treat title cards as rhythm: they should land on hits, silence, or visual turns.
- Build a title hierarchy: hook card, premise cards, quote/claim cards, title, CTA/legal card.

For social cutdowns, prefer burned-in open captions or platform-native captions plus safe-zone-aware title cards. For theatrical/OTT deliverables, confirm whether subtitles/captions are sidecar files, embedded tracks, or burned-in.

## Claims, ratings, disclosure, and legal caveats

This skill is not legal advice. The agent should identify risk and escalate to the client, counsel, platform policy owner, ratings contact, or rights holder.

Escalate for approval before final delivery when the trailer includes:

- performance claims, "#1," "best," "first," "only," medical/financial/safety claims, guaranteed outcomes, pricing, availability, or comparisons;
- reviews, testimonials, influencers, affiliate relationships, awards, festival laurels, press quotes, or star ratings;
- third-party trademarks, game/platform logos, publisher logos, music, celebrity likenesses, real people, minors, sensitive events, or political/social issue content;
- AI-generated or materially altered depictions of real people, public figures, news-like events, synthetic endorsements, or realistic scenes that could mislead;
- MPA/CARA rating marks, trailer tags, green/red-band style cards, or claims that a film is rated when not authorized;
- restricted products or regulated categories;
- paid ads in regions or platforms with AI-content disclosure rules.

Baseline truth-in-advertising rule: in the United States, FTC business guidance states advertising claims must be truthful, not deceptive or unfair, and evidence-based. FTC endorsement guides require disclosure of material connections when the audience would not reasonably understand or expect them. Use exact approved claim language; do not let a model invent statistics, awards, quotes, UI promises, or release details.

For U.S. theatrical-style film advertising, the MPA Advertising Administration rules are specialized and volatile. As of the 2025 handbook, MPA rating symbols, legends, and trailer tags are certification marks that may not be self-applied and require authorization. Restricted-audience advertising is subject to placement limits and approval. Do not imitate rating cards in a way that implies approval if the project has not received it.

For AI-generated or AI-edited advertising assets, check platform and jurisdiction disclosure requirements at production time. Google Ads documentation notes AI label settings and warns that using the setting does not guarantee compliance with local obligations. Treat AI labels as a compliance workflow item, not a creative afterthought.

## Production workflow

Use the local production system's pipeline/checkpoint rules when available. This discipline layer fits inside that workflow.

1. **Discovery**
   - Collect brief, references, brand/legal constraints, platform/duration targets, release details, and available source assets.
   - Identify whether the deliverable is motion-led. Do not downgrade to a still-image animatic without explicit approval.
2. **Strategy**
   - Choose trailer type, audience, runtime ladder, aspect ratios, emotional destination, and hook.
   - Define cutdown plan and required approvals.
3. **Script and copy**
   - Write logline, beat map, title cards, VO/dialogue selects, CTA, captions plan, legal/claim placeholders.
   - Separate approved facts from draft creative language.
4. **Scene and shot plan**
   - Create shot list with timecodes, continuity anchors, generation prompts, source footage notes, typography/audio needs.
   - Mark hero shots that require extra generation attempts or client approval.
5. **Asset generation or sourcing**
   - Generate or select shots by beat priority, not chronological convenience.
   - Preserve seeds/model versions/references where supported.
   - Reject shots that violate continuity, brand, rights, or claims requirements even if visually attractive.
6. **Edit**
   - Build radio edit or music/sound spine first if audio-led.
   - Assemble picture for escalation; add title cards and captions early enough to test readability.
   - Create hero cut, then derive cutdowns intentionally.
7. **Mix, color, and finish**
   - Balance VO/dialogue/music/SFX, measure loudness to destination spec, check true peak.
   - Apply consistent color/look; avoid per-shot AI color drift.
   - Composite typography, logos, ratings/claim/legal cards from approved assets.
8. **QA and review**
   - Watch full-screen, mobile, muted, low-volume, and with captions.
   - Verify every claim, date, platform logo, spelling, caption, audio sync, and export setting.
   - Deliver files, stems, captions, source notes, and residual risk list.

## Review loop

Use three review passes. Do not mix them into one vague "looks good" review.

### 1. Story pass

Questions:

- Do I know what this is?
- Do I know why it matters?
- Does the trailer create a question or desire?
- Is anything spoiled too early?
- Is there one clear emotional destination?

### 2. Craft pass

Questions:

- Does the first 3-5 seconds earn attention?
- Does each shot have a job?
- Does pacing escalate or merely speed up?
- Are the best visuals saved or repeated strategically?
- Are title cards readable and rhythmic?
- Does the audio spine create momentum?
- Does the final title/CTA land cleanly?

### 3. Delivery/risk pass

Questions:

- Are platform specs, aspect ratios, safe zones, captions, and loudness targets checked against current official rules?
- Are claims, quotes, awards, ratings, release dates, and CTAs approved?
- Are AI disclosure requirements checked?
- Are rights for footage, music, fonts, logos, likenesses, and trademarks cleared or escalated?
- Are all captions accurate, synchronized, complete, and placed away from critical visual information?

## Trailer QA checklist

Before final delivery, verify:

- The trailer has a specific logline and one primary promise.
- The first 3-5 seconds work without context.
- The trailer type and platform are clear.
- Runtime matches the planned deliverable and platform constraints.
- Every shot supports hook, world, stakes, proof, emotion, escalation, or CTA.
- No generated shot invents unsupported facts, readable fake text, brand marks, characters, or UI.
- Recurring characters/products/locations are acceptably continuous.
- Title cards and captions are readable on a phone.
- Important text is inside safe zones.
- VO/dialogue is intelligible under music and SFX.
- Loudness/true peak are measured to the destination spec.
- Color and grain are consistent enough that AI/source seams do not distract.
- CTA, release date, platform logos, ratings, legal lines, and disclaimers are approved.
- AI-content labels/disclosures have been checked if relevant.
- Captions/subtitles are accurate and synchronized.
- Deliverables include master, cutdowns, captions/subtitles, stems if requested, and a notes/risk list.

## Complete example: generated sci-fi teaser

Example, not a mandatory formula.

**User request:** "Make a 45-second teaser for a fictional sci-fi short about astronauts discovering a city under Europa's ice. It will go on YouTube and Instagram Reels."

**Strategy**

- Trailer type: teaser.
- Runtime ladder: 45s 16:9 master, 30s 9:16 cutdown, optional 15s hook.
- Promise: cosmic discovery turns into existential threat.
- Hook: "The signal came from under the ice."
- Emotional destination: awe curdling into dread.
- Risk: fictional, no claims; still avoid fake NASA/ESA logos unless licensed/approved.

**Beat map**

| Time | Beat |
|---:|---|
| 0-3 | Black screen, radio crackle, ice cracking macro. Title card: "EUROPA / 2042" |
| 3-9 | Astronaut wide shot crossing blue-white ice plain toward a pulsing glow. |
| 9-15 | VO whisper: "The signal came from under the ice." Sonar line reveals geometry below. |
| 15-24 | Montage: drill lights, gloved hand over alien glyph, helmet reflection of buried skyline. |
| 24-29 | Stop-down: a childlike voice through comms says, "You're late." |
| 29-39 | Fast escalation: ice fractures, city lights ignite, astronaut runs, black water rises. |
| 39-45 | Title reveal: "BELOW THE QUIET" / "A short film concept" / date or CTA. |

**Continuity bible**

- Astronaut: white EVA suit, orange wrist tether, cracked left shoulder plate, no national logos.
- Location: Europa ice, pale blue sunrise, buried black-glass alien city.
- Camera: grounded sci-fi realism, 35mm/50mm, slow push-ins, limited handheld.
- Palette: blue-white ice, black glass, amber suit lights.
- Avoid: NASA logo, readable invented text, extra crew, changing suit design, gore.

**Example generated-video prompt for shot 4**

> Medium close-up inside a dim ice cave on Europa: a lone astronaut in a scratched white EVA suit with an orange wrist tether and cracked left shoulder plate raises a gloved hand toward black-glass alien glyphs glowing faintly beneath clear ice. The helmet visor reflects the buried city lights. Slow 50mm push-in, cold blue rim light, amber suit LEDs, suspended frost particles, grounded sci-fi realism, 5 seconds. Keep suit details identical to the continuity bible. No readable human text, no NASA or ESA logos, no extra astronauts, no morphing glyphs, no horror gore.

**Edit note**

Cut on sound hits, use radio static as a bridge, and reserve the strongest city reveal until after the voice line. The 9:16 cutdown should crop/recompose shots around the astronaut and glyphs, not simply center-crop wides.

## Complete example: product launch trailer

Example, not a mandatory formula.

**User request:** "Create a 60-second launch trailer for a new AI project-management app for startup founders."

**Strategy**

- Trailer type: launch trailer.
- Audience: founders/operators who feel buried by meetings and tools.
- Promise: turns scattered work into a single launch command center.
- Emotional destination: pressure -> clarity -> momentum.
- Legal/claims: no "guaranteed productivity" or invented customer numbers; all claims must be approved.

**Copy spine**

- Hook card: "Your launch is moving faster than your tools."
- VO: "Plans split. Owners drift. Deadlines move quietly."
- Proof card: "One place for decisions, blockers, and next actions."
- CTA: "Join the beta" or approved launch URL.

**Shot families**

1. Founder at 1:13 a.m., multiple windows, tired but focused.
2. Abstract task threads tangling into a knot.
3. Product UI reference composited in post, not generated as unreadable fake UI.
4. Decision timeline snaps into a clean path.
5. Team reaction shots across remote locations.
6. Launch dashboard at calm morning light.
7. Logo/title and CTA.

**Example generation prompt for non-UI mood shot**

> Cinematic close-up of a startup founder's hands moving between laptop, notebook, and coffee on a desk at 1:13 a.m., soft monitor glow, shallow depth of field, subtle handheld fatigue, premium SaaS launch film style, 4 seconds. The screen content should be abstract blurred shapes only because final approved UI will be composited later. No readable invented text, no fake logos, no extra fingers, no distorted keyboard.

**Edit note**

Composite all UI and claims in post from approved designs. Use the trailer rhythm to sell emotional relief, not magical automation. Make social cutdowns sound-off friendly with burned-in captions and proof cards.

## Complete example: documentary trailer

Example, not a mandatory formula.

**User request:** "Build a 90-second trailer for a documentary about a community rebuilding after a wildfire."

**Strategy**

- Trailer type: documentary.
- Promise: human resilience without exploitation.
- Hook: a specific image or line from a real participant.
- Legal/ethics: releases, consent, sensitive-event treatment, music rights, no fabricated documentary evidence.

**Beat structure**

- 0-8: Cold open with participant line over quiet aftermath image.
- 8-20: Establish place and loss.
- 20-45: Introduce people rebuilding; practical details.
- 45-55: Quiet line about what cannot be replaced.
- 55-78: Escalation toward community action and stakes.
- 78-90: Title, festival/date/CTA, partner credits.

**Direction**

Use source footage and verified interviews where possible. If generated visuals are used for abstract transitions, label internally as reenactment/illustration and do not present them as documentary capture. Avoid synthetic faces of real survivors unless explicit informed consent and legal approval exist.

## Source notes verified 2026-07-10

- Google Ads Help, "About video ad specs" and "Skippable in-stream ads" for YouTube ad dimensions, safe zones, file size, format, and runtime guidance.
- YouTube Help, "Recommended upload encoding settings" for upload bitrate/audio and aspect-ratio behavior.
- TikTok Ads Policy, "Ad Format and Functionality" for duration, aspect ratios, audio quality, and dynamic-content requirements.
- W3C WAI WCAG 2.2 Understanding SC 1.2.2 for prerecorded captions.
- FCC consumer guidance on closed captioning quality for accuracy, synchronicity, completeness, and placement.
- EBU R 128-2023 and EBU R 128 s1 for loudness normalization, true peak, and short-form items such as trailers/promos.
- ATSC A/85 page for television/streaming loudness workflow guidance, including the current A/85:2026-07 listing approved July 8, 2026.
- FTC Advertising and Marketing Basics and 16 CFR Part 255 for truth-in-advertising and endorsement/material-connection principles.
- MPA Advertising Administration Rules handbook, effective August 4, 2025, for rating marks/trailer tags and restricted-audience advertising caveats.
