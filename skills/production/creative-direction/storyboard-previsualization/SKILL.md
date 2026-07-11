---
name: storyboard-previsualization
description: Provider-independent storyboard and previsualization direction for AI agents turning briefs, scripts, treatments, ads, films, social videos, and generated-media concepts into shot-by-shot boards, animatics, previs plans, camera/blocking/movement direction, reference packs, AI image/video prompt plans, review workflows, continuity checks, and production handoffs.
---

# Storyboard and previsualization direction

Use this skill when a user needs to plan what a video, film, ad, animation, social cut, product piece, or generated-media sequence should look like before expensive production or generation begins. The deliverable may be text-only shot boards, illustrated boards, an animatic, 3D previs, techvis, or a generation-ready prompt plan.

Do not start by making polished images. Start by proving the sequence works: story beat, geography, framing, action, cut, duration, audio, and continuity.

## Evidence classes to keep separate

- Documented facts: cite or name the source when relying on platform specs, professional tool behavior, review-tool features, or production terminology.
- Empirical observations: label anything learned from inspecting a reference, prototype, generated output, or test render.
- Production heuristics: use as judgment aids, not universal laws. Explain why the heuristic fits the current brief.

Volatile facts such as platform aspect ratios, upload lengths, ad specs, model duration limits, generation features, or pricing must be rechecked for the current project. Source examples in this skill were verified on 2026-07-10.

## Decide the right previs fidelity

Match the planning artifact to the risk:

- Beat board: 6-12 key panels to test the story arc, useful for pitches and loose briefs.
- Shot board: one row per intended shot, useful before image/video generation, live action, animation, or edit assembly.
- Animatic: timed panels with scratch narration, temp music/SFX, captions, and placeholder motion to test pacing and comprehension.
- 3D previs: rough spatial scene with camera, blocking, lens/framing, and timing when depth, action choreography, or camera movement matters.
- Techvis: production-facing diagrams and measurements for camera placement, lens, crane/drone path, VFX plates, LED volume, stunt beats, or set constraints.

Documented fact: Autodesk describes previs as a way to lay out creative vision before production, using storyboards, animatics, shot lists, photos, or 3D previs scenes; it also notes that previs helps plan actor movement, camera placement, set design, lighting, and VFX integration. Toon Boom positions professional storyboarding around thumbnailing, visual storytelling, pitching boards, and timing camera moves in an animatic.

Production heuristic: Use the lowest fidelity that can answer the current question. If the open question is "does the emotional sequence work?", a beat board is enough. If the open question is "will the orbiting move reveal the product label without crossing screen direction?", use animatic or 3D previs.

## Intake checklist

Before designing shots, extract or ask for:

- Intent: story outcome, audience feeling, conversion goal, or information the viewer must retain.
- Delivery: platform, aspect ratio, duration, audio/no-audio assumption, captions, language, thumbnail/poster needs, and versions.
- Inputs: script, brief, brand rules, product claims, legal disclaimers, locations, characters, assets, references, must-show moments, must-avoid moments.
- Production path: AI image generation, AI video generation, live action, animation, edit of existing footage, or hybrid.
- Review path: who approves story, style, timing, legal/brand, and final generation.
- Constraints: budget, deadline, number of generation attempts, likeness/rights limits, sensitive content, and accessibility needs.

If platform is unknown, propose a master plan plus variants. Example: a 16:9 master can be useful for YouTube/web, while a 9:16 board needs different composition, typography, and safe-zone planning for vertical social.

## Build the board from story beats, not from pretty frames

Use this sequence:

1. State the delivery promise in one sentence.
2. Split the brief/script into beats: hook, setup, complication, proof/demo, turning point, payoff, CTA or emotional landing.
3. Assign each beat a viewer question: "Where are we?", "What changed?", "Why believe this?", "What should I do?"
4. Choose the minimum shot count that answers those questions with visual clarity.
5. Create a continuity bible before generating individual shots.
6. Only then write panel prompts, camera instructions, and review criteria.

Recommended shot-board fields:

| Field | Purpose |
|---|---|
| Shot ID | Stable reference for review and handoff, e.g. `S03A` |
| Beat | Narrative purpose, not just image subject |
| Duration | Initial timing estimate in seconds or frames |
| Frame | Shot size, angle, subject placement, foreground/background |
| Action | What changes during the shot |
| Camera | Static/pan/tilt/dolly/truck/orbit/handheld/zoom plus motivation |
| Blocking | Character/object positions, movement path, eyeline, screen direction |
| Audio | Dialogue, VO, SFX, music cue, silence, caption need |
| Continuity anchors | Character look, prop state, lighting, wardrobe, location, product orientation |
| AI prompt notes | Reference inputs, shot-specific prompt, negative constraints, seed/model notes if applicable |
| Handoff notes | Crew, animator, editor, VFX, or compliance instructions |

## Camera, blocking, and continuity

Treat every board as a map of space and attention.

- Establish geography early when orientation matters. Use an establishing shot, insert, map-like diagram, or repeated background anchor.
- Track the line of action. Adobe and Filmmakers Academy both describe the 180-degree rule as a way to preserve spatial orientation and eyeline/screen direction; crossing it can disorient viewers unless done intentionally.
- Mark screen direction with arrows. If the subject moves left-to-right in one shot and right-to-left in the next, say whether that change is a motivated turn, a reverse angle, or a continuity problem.
- Give camera movement a job. A move can reveal information, follow action, shift power, add instability, or create scale. Avoid moving the camera merely because motion is available.
- Use shot-size changes to control emphasis: wide for geography, medium for relationship/action, close-up for decision/emotion/detail, insert for evidence.
- Reserve complex moves for moments that benefit from spatial change. If the board relies on an impossible or expensive move, flag it early and propose a simpler coverage option.
- Keep product, logo, prop, and wardrobe continuity explicit. Note which hand holds an object, whether a package is open, where a label faces, and what state a UI screen is in.
- In generated-media work, include continuity anchors in every shot prompt that needs them; do not assume the model will remember prior shots.

Production heuristic: If a viewer cannot answer "where is everyone, what changed, and what am I supposed to look at?" from the board, the shot design is not ready for production.

## Reference strategy

References must serve specific decisions. Do not provide a pile of inspiration without routing each reference to its use.

Use these reference types:

- Story reference: pacing, structure, tone, or beat order.
- Composition reference: framing, negative space, foreground/background layering, lens feel.
- Motion reference: camera move, gesture, physical action, transition, or edit rhythm.
- Design reference: palette, typography, lighting, texture, set design, wardrobe, product art direction.
- Continuity reference: character sheet, product turntable, location map, prop board, UI state, wardrobe board.
- Negative reference: "avoid this kind of polish/camera/lighting/tone."

For rights and ethics, identify whether references are owned by the user, licensed, public-domain, created for the project, or used only for private analysis. Do not direct an AI system to clone a living artist, brand, copyrighted character, performer likeness, or exact frame from an unlicensed source. Translate references into observable traits such as lighting ratio, composition, camera height, color contrast, blocking, and editing rhythm.

## Aspect ratio, platform, and safe-zone planning

Documented facts verified on 2026-07-10:

- TikTok Auction In-Feed Non-Spark ads list vertical 9:16 at at least 540x960 as the recommended dimension, with 16:9 and 1:1 also accepted.
- YouTube Help says Shorts uploads from desktop can be up to 3 minutes with a square or vertical aspect ratio.
- Meta/Facebook Help Center's Instagram Reels size page, visible in indexed/search snippets on 2026-07-10, reported Reels can be uploaded between 1.91:1 and 9:16, with minimum 30 FPS and minimum resolution requirements; the page may require login, so recheck from an authenticated official source for production.

Production heuristics:

- Board in the final aspect ratio whenever possible. Reframing later changes staging, text layout, and eye trace.
- For vertical social, keep the action center-biased unless the platform placement has known side UI. Leave room for captions, handles, CTAs, progress bars, and engagement buttons.
- For multi-aspect campaigns, design a "protected action box" shared across crops, then create aspect-specific boards for text, lower thirds, and product close-ups.
- Avoid making one frame carry both tiny legal text and essential action. If disclaimer text is required, allocate a calm shot or end card.

## AI-generation prompt planning

Plan prompts as a production system, not as isolated magic sentences.

Create three layers:

1. Continuity bible: recurring characters, wardrobe, product state, location, lighting logic, style boundaries, color palette, aspect ratio, lens language, and forbidden changes.
2. Shot prompt: shot ID, narrative purpose, frame composition, subject/action, camera movement, timing, audio/silence assumption, and continuity anchors.
3. Review criteria: what must be true for the output to pass, what can vary, and what requires regeneration.

Write visual prompts in concrete screen language:

- Prefer "low camera at waist height, product box in sharp foreground left, founder blurred in background right" over "cinematic product shot."
- Prefer "slow push-in over 4 seconds as the latch clicks open" over "dramatic movement."
- Prefer "same red jacket, silver zipper, coffee stain on left cuff from shot S02" over "same character."
- Use "not final text; placeholder label area only" when a model is likely to hallucinate typography.

Generation order for continuity-heavy boards:

1. Create or collect approved reference assets: character sheets, product packshots, location plates, palette, typography, logo files.
2. Generate key establishing frames and continuity-critical inserts.
3. Generate action panels or video clips shot-by-shot.
4. Assemble an animatic before polishing.
5. Regenerate only the shots that fail the board criteria; do not redesign the sequence during asset cleanup unless review explicitly changes the story.

Empirical observation from current generative workflows: image/video models can produce compelling individual shots while drifting across identities, props, backgrounds, logos, text, and spatial relationships. Recent storyboard-generation research explicitly treats multi-shot continuity as a core challenge. Therefore, require a continuity bible, shot IDs, reference frames, and per-shot pass/fail criteria.

Limitations to plan around:

- Identity drift across shots, especially with secondary characters.
- Prop and wardrobe state changes after cuts.
- Unreliable exact text, UI, product labeling, hands, and small logos.
- Camera movement described in film terms may be interpreted loosely unless translated into visible motion.
- Long action chains may collapse; split them into shorter shots or key beats.
- Exact duration, frame-accurate choreography, and physical continuity may require animation, compositing, or 3D previs rather than direct text-to-video.

## Animatic and timing direction

An animatic should answer timing and comprehension questions before final rendering.

Include:

- Board panels cut to estimated duration.
- Scratch VO or dialogue, even if synthetic/temp.
- Temp music and SFX only when timing depends on them.
- Captions or subtitle placeholders when the final platform will be watched silently.
- Camera moves as simple pans, zooms, parallax, or 3D camera paths only where needed.
- Slugs for shots not yet generated, marked with their shot IDs.

Review the animatic in real time. Do not evaluate only as a table. Watch for dead air, confusing geography, too many ideas in one shot, action that finishes after the cut, captions that fight the image, and missing emotional landing.

Documented fact: Toon Boom's Storyboard Pro product materials explicitly connect preproduction storyboarding with timing camera moves in an animatic. Frame.io documents single-frame, range-based, anchored, and annotated comments; Autodesk Flow Production Tracking described version comparison, frame-accurate annotations, notes, attachments, and live review in its 2026 review update.

## Iteration and review workflow

Use separate review passes. Mixing every concern into one pass creates vague notes.

1. Story pass: Does the viewer understand the sequence without extra explanation?
2. Geography/blocking pass: Is space, eyeline, movement direction, and object state clear?
3. Timing pass: Does the animatic breathe correctly? Are cuts motivated?
4. Brand/legal pass: Are claims, logos, disclaimers, likenesses, and references allowed?
5. Generation feasibility pass: Can the planned shots be made with available tools and budget?
6. Handoff pass: Can an artist, editor, cinematographer, animator, or generation agent execute from the board without guessing?

Write notes with shot IDs and timecodes. A good note is "S04, 00:11-00:13: keep the courier moving screen-left; the reverse direction makes it look like he is returning to the store." A weak note is "this feels off."

For AI iterations, classify failures:

- Story failure: wrong beat or emotional intent. Revise board/script.
- Direction failure: prompt omitted framing, action, continuity, or duration. Revise prompt.
- Model limitation: prompt is clear but output cannot hold identity, motion, text, or physics. Change method, use references, split the shot, composite, or move to 3D/animation.
- Review ambiguity: stakeholders disagree or notes conflict. Resolve the decision before generating again.

## Production handoff

A production-ready handoff should include:

- Shot board with stable shot IDs.
- Continuity bible and reference pack with provenance.
- Animatic or timing table if duration matters.
- Camera/blocking notes or overhead diagrams for spatial scenes.
- AI prompt plan with global bible, per-shot prompts, pass/fail criteria, and regeneration priority.
- Aspect-ratio and safe-zone notes.
- Audio/caption plan.
- Open questions and known risks.
- Version history: what changed and why.

For live-action or virtual production, add lens/framing intent, camera height, approximate subject distance, movement path, set/prop requirements, VFX plates, and techvis needs. For animation, add key poses, arcs, holds, transitions, expression changes, and frame-count or timing notes. For ads, add product claims, required supers, compliance timing, CTA, and platform variants.

## Example: vertical product ad board and generation plan

This is an example, not a formula.

Brief: 20-second 9:16 ad for a spill-proof travel mug. Tone: practical, premium, slightly humorous. Must show leak-proof lid, one-handed opening, and CTA. Assume no live action; use AI image/video generation plus edit/composite.

Delivery promise: "Show commuters that the mug survives real chaos without making the product feel gimmicky."

Continuity bible:

- Product: matte graphite travel mug, short cylindrical body, black flip lid, small blank logo plate on front; do not invent readable brand text.
- Location: morning subway platform, cool gray tiles, yellow platform line, soft practical lights.
- Character: 30s commuter, navy coat, tan messenger bag, white earbuds.
- Style: clean premium commercial, naturalistic lighting, shallow depth of field for product inserts.
- Aspect/safe zone: 9:16, keep product and face in central 70%; lower 20% reserved for captions/CTA.

Shot board excerpt:

| ID | Dur | Frame/action | Camera/blocking | Audio/text | Prompt notes |
|---|---:|---|---|---|---|
| S01 | 2.0 | Close insert: mug tips sideways inside open bag; coffee does not leak. | Static macro, product diagonal from lower-left to upper-right. | SFX: train rumble, soft clink. Caption: "Commute-proof." | Generate as product insert. Emphasize closed black flip lid and dry notebook nearby. |
| S02 | 3.0 | Medium: commuter grabs bag as train arrives; bag swings. | Handheld follow, commuter moves screen-right, mug visible in side pocket. | VO: "For mornings that move faster than you do." | Use continuity anchors for coat, bag, platform. |
| S03 | 3.0 | Close-up: one thumb flips lid open. | Locked close-up, hand enters from right, lid opens toward camera. | SFX: satisfying click. | If model fails hand mechanics, create still insert and animate lid in compositing. |
| S04 | 4.0 | Wide vertical: crowd jostle, bag bumps, commuter stays calm. | Slow push-in; keep movement screen-right. | Music lift. | Avoid chaotic faces; product remains readable. |
| S05 | 4.0 | Hero product on bench, steam, subway blur behind. | Low camera, product center, slight parallax push. | Super: "Locks tight. Opens easy." | Composite actual logo/text later; leave blank plate. |
| S06 | 4.0 | End card with product and CTA. | Static. | CTA: "Meet your no-spill morning." | Use designed typography, not generated text. |

Why structured this way:

- The first shot proves the claim before the ad explains it.
- The continuity bible prevents the mug, commuter, and platform from changing across shots.
- The board flags the hand/lid mechanic as a likely model limitation and provides a compositing fallback.
- The vertical safe-zone note keeps the CTA and product from colliding with platform UI.

Pass/fail criteria:

- Pass if the mug remains the same shape/color, the lid is visibly closed before the leak-proof proof point, the notebook stays dry, and no fake readable brand text appears.
- Regenerate or composite if the lid changes design, hands deform during the open, or the product is hidden by captions.

## Example: cinematic scene previs plan

This is an example, not a formula.

Script moment: A daughter returns to an abandoned family diner at night, finds the "OPEN" sign still glowing, and realizes someone has been there.

Previs choice: Shot board plus rough 3D layout. The diner geography and reveal timing matter more than polished art.

Overhead map:

- Entrance south wall.
- Counter runs east-west on north side.
- Neon sign in front window west of door.
- Back hallway behind counter at northeast.
- Daughter enters from south, crosses to window, then turns toward hallway sound.
- Camera stays mostly south/west of the daughter-counter axis until the reveal; crossing the line at S06 is intentional to create unease.

Shot plan:

| ID | Dur | Frame/action | Camera/blocking | Continuity |
|---|---:|---|---|---|
| S01 | 5 | Exterior wide: diner in rain, one neon sign flickering. | Slow dolly toward window; daughter silhouette enters frame left. | Rain direction left-to-right; neon red. |
| S02 | 4 | Interior wide from behind booths: door opens, daughter enters. | Static; foreground booths create depth. | Door remains open; wet footprints begin at threshold. |
| S03 | 3 | Insert: her hand touches dusty counter, but one clean ring mark is visible. | Locked macro. | Dust continuity; ring mark implies recent cup. |
| S04 | 5 | Medium: she looks to neon sign; its reflection trembles in her eyes. | Slow push-in. | Eyeline screen-left toward window. |
| S05 | 4 | Over-shoulder: hallway light clicks off in background. | Hold; no camera move. | Daughter foreground right, hallway background left. |
| S06 | 3 | Reverse angle across the axis: she whips toward sound. | Intentional line cross, handheld jolt. | Mark as motivated disorientation. |
| S07 | 6 | Long lens down hallway: wet footprints continue into darkness. | Static, compression makes hallway feel longer. | Footprints match threshold pattern. |

Why structured this way:

- The map prevents accidental geography changes.
- The board reserves the line cross for the story turn rather than using it casually.
- Inserts carry clues, so prop continuity is central to the suspense.
- A rough 3D layout can test whether the hallway reveal is visible from the intended camera positions.

## QA checklist

Before handing off, verify:

- The board can be understood without the creator verbally explaining missing action.
- Each shot has one primary viewer focus.
- Shot IDs are stable and referenced in notes, prompts, and animatic slugs.
- The aspect ratio matches the intended platform or each variant has its own crop plan.
- Camera moves are motivated and physically/generatively feasible.
- Screen direction, eyelines, object state, wardrobe, and product continuity are tracked.
- References are labeled by use and rights/provenance.
- AI prompt plans separate continuity bible, shot prompt, and pass/fail criteria.
- Known model/tool limitations are flagged with fallbacks.
- The animatic has been watched in real time if timing matters.
- Review notes are timecoded or shot-specific, not vague global reactions.

## Source ledger

Sources used for documented facts and professional grounding, checked 2026-07-10:

- Autodesk, "What Is Previs? Previsualization Software": https://www.autodesk.com/solutions/previsualization-software
- Unreal Engine, "Virtual Production Field Guide" PDF: https://cdn2.unrealengine.com/vp-field-guide-v1-3-01-f0bce45b6319.pdf
- Toon Boom, "Storyboard Pro": https://www.toonboom.com/products/storyboard-pro
- Adobe, "What is the 180-degree rule in filmmaking": https://www.adobe.com/creativecloud/video/discover/what-is-the-180-degree-rule.html
- Filmmakers Academy, "Camera Composition: 180-Degree Rule": https://www.filmmakersacademy.com/blog-camera-180-degree-rule/
- Frame.io Knowledge Center, "Commenting on your media": https://help.frame.io/en/articles/9105251-commenting-on-your-media
- Autodesk Media & Entertainment Blog, "Introducing Your New Home for Post-Production Review in Flow Production Tracking," 2026-06-29: https://blogs.autodesk.com/media-and-entertainment/2026/06/29/new-review-and-collaboration-tools-in-flow-production-tracking/
- TikTok Ads Manager, "TikTok Auction In-Feed Ads," last updated June 2026: https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads
- YouTube Help, "Upload YouTube Shorts" and "Understand three-minute YouTube Shorts": https://support.google.com/youtube/answer/12779649 and https://support.google.com/youtube/answer/15424877
- Meta/Facebook Help Center, "Reel size & aspect ratios on Instagram": https://www.facebook.com/help/1038071743007909
- Mondal et al., "CANVAS: Continuity-Aware Narratives via Visual Agentic Storyboarding," arXiv, 2026: https://arxiv.org/abs/2604.13452
- Li et al., "StoryBlender: Inter-Shot Consistent and Editable 3D Storyboard with Spatial-temporal Dynamics," arXiv, 2026: https://arxiv.org/abs/2604.03315
- Mayer, multimedia learning research as represented by Cambridge Handbook chapter listing for coherence/signaling/contiguity principles: https://www.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/CD5B7AE1279A9AB81F8EEBB53DBEC86E
