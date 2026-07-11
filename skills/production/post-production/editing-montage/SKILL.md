---
name: editing-montage
description: "Provider-independent editing and montage direction for AI agents producing generated videos, ads, trailers, social clips, explainers, product videos, documentary-style pieces, and music- or beat-driven cuts. Use when planning, revising, QAing, or handing off an edit: story structure, shot selection, continuity, montage theory, rhythm and pacing, J/L cuts, match cuts, cutaways, transitions, beat sync, platform timing, source/generated asset management, revision workflow, and composition handoff."
---

# Editing and montage direction

Use this skill when the edit itself determines whether a video works. Your job is to make decisions about sequence, duration, shot function, rhythm, continuity, audio/visual relationship, platform fit, and revision logic. Do not treat editing as "put the clips in order." Treat it as the craft of controlling what the viewer notices, understands, feels, and remembers.

Work provider-independently. The source clips may be human-shot footage, generated clips, stills animated in a composition engine, screen recordings, avatar footage, stock, captions, product UI, diagrams, or music. The same edit principles apply, but generated media needs stricter provenance, continuity, and QA because shots may not share stable identity, lighting, geometry, text, or physics.

## Evidence classes to keep separate

Documented facts:

- Film-analysis sources commonly describe editing as the relationship between shots and the construction of graphic, rhythmic, spatial, and temporal relationships. Source: Yale Film Analysis, "Part 4: Editing" (<https://filmanalysis.yale.edu/editing/>).
- J-cuts introduce the next shot or scene's audio before the visual cut; L-cuts let prior audio continue after the visual cut. Source: DINFOS Pavilion, "How to Edit Video with the J-Cut and L-Cut," last verified 2025-01-16 (<https://pavilion.dinfos.edu/How-To/Article/2286253/how-to-edit-video-with-the-j-cut-and-l-cut/>).
- Prerecorded synchronized media with audio needs captions under WCAG 2.2 Success Criterion 1.2.2 unless the media is an explicitly labeled media alternative for text. Source: W3C WAI (<https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html>).
- Practical caption placement guidance includes safe-zone placement and no more than two lines per caption. Source: DCMP Captioning Tip Sheet (<https://dcmp.org/learn/225-captioning-tip-sheet>).
- Netflix timed-text general requirements specify a 5/6-second minimum and 7-second maximum subtitle event duration for Netflix deliveries; do not generalize these as universal requirements for all platforms. Source: Netflix Partner Help (<https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements>).
- YouTube Shorts facts verified on 2026-07-10: square or vertical videos up to 3 minutes are categorized as Shorts for standard channels when uploaded on or after 2024-10-15; YouTube also states Shorts views count starts/replays from 2025-03-31. Sources: YouTube Help (<https://support.google.com/youtube/answer/15424877?hl=en>, <https://support.google.com/youtube/answer/10059070?hl=en>).
- TikTok ads facts verified on 2026-07-10: TikTok's ad policy states ad video duration must be 5-60 seconds and use standard video sizes including vertical 9:16, square 1:1, or horizontal 16:9; TikTok's June 2026 in-feed auction specs list Non-Spark vertical recommended 9:16 at at least 540x960, up to 10 minutes, 500 MB max, and safe-zone files. Treat the policy/spec distinction carefully for the placement you are delivering. Sources: TikTok Ads Help (<https://ads.tiktok.com/help/article/tiktok-ads-policy-ad-format-and-functionality>, <https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads?redirected=2>).
- Adobe documents Premiere Team Projects and Productions as collaboration/media-management choices; Productions break long projects into smaller projects and rely on shared media access. Source verified 2026-07-10: Adobe Help (<https://helpx.adobe.com/premiere/desktop/collaborate-with-others/collaborate-using-team-projects/when-to-use-team-projects-and-when-to-use-productions.html>).

Empirical observations from generated-media production:

- AI-generated adjacent shots often drift in faces, logos, product geometry, UI copy, hands, scale, reflections, and object permanence even when each clip looks plausible alone.
- Generated clips frequently have strong local motion but weak editorial endpoints: the first and last 6-12 frames may wobble, smear, or change identity. Trimming heads/tails often improves continuity more than re-generating immediately.
- Beat-synced edits feel late if the visual impact happens after the audio transient. In most composition contexts, place the cut or visual hit on the transient or a frame or two before it, then review by eye and ear.
- Platform retention patterns are audience-, category-, and distribution-dependent. Treat "hook in the first seconds" as a testing heuristic, not as proof that every good edit must cut rapidly.

Production heuristics:

- Prefer emotional clarity and story comprehension over clever transitions. A beautiful match cut that obscures causality is a bad cut.
- Every shot should earn its screen time by doing at least one job: orient, reveal, prove, compare, intensify, relieve, bridge, humanize, or close.
- A cut should usually happen when the viewer has received the necessary information, not when the source clip ends.
- A montage should have an argument. "Many cool shots" is not yet a montage.
- Faster pacing is not automatically better. Pace is the controlled contrast between density, rests, anticipations, and payoffs.

## Start by defining the edit promise

Before choosing cuts, state the edit promise in one sentence:

> This edit will make the viewer feel/understand/believe/do ___ by arranging ___ into ___ over ___ seconds for ___ platform/context.

Then lock these working decisions:

- Delivery context: ad, trailer, social post, explainer, documentary segment, product demo, music video, internal recap, teaser, or cutdown.
- Primary viewer action: keep watching, understand a concept, feel stakes, trust a claim, click, buy, remember, share, approve, or learn.
- Emotional curve: curiosity to clarity, anxiety to relief, awe to proof, problem to solution, calm authority, escalating hype, playful reveal, investigative discovery.
- Time budget and aspect ratio: target duration, safe-zone needs, caption strategy, platform constraints, audio-on/audio-off assumption.
- Source regime: source footage-led, generated clip-led, stills-to-motion, screen/UI-led, avatar-led, mixed media, or music-led.
- Revision authority: what may change freely, what is locked by client/brand/legal/music/platform, and what requires approval.

If the user only asks "make it snappier," translate that into observable edit changes: shorter shot durations, earlier hook, removed redundancy, stronger audio hits, simpler captions, tighter action matching, or changed story order.

## The edit decision ladder

When judging any cut, use this priority order. It is inspired by professional editing traditions that rank emotion, story, rhythm, viewer attention, and spatial clarity, but it is a heuristic, not a law.

1. Viewer effect: What should the viewer feel, infer, or ask at this instant?
2. Story function: Does the cut advance the promise, reveal, proof, escalation, or payoff?
3. Attention path: Does the viewer's eye land where the next shot needs it?
4. Rhythm: Does the cut align with breath, speech, movement, beat, or intentional rupture?
5. Continuity: Is time, space, identity, screen direction, and causality clear enough for this style?
6. Technical cleanliness: Are frames, audio joins, captions, and transitions free of avoidable defects?

If two priorities conflict, explain the tradeoff. Example: "This jump cut violates spatial smoothness, but it improves urgency and removes a dead clause; acceptable for TikTok UGC, not for a calm documentary sequence."

## Build the story spine before the timeline

Choose a structure that matches the deliverable.

For explainers:

- Cold open: state the surprising problem, visual metaphor, or before/after.
- Orientation: give the viewer the minimum context needed to follow.
- Steps: one idea per beat; each visual must prove or clarify the narration.
- Synthesis: show how the parts connect.
- Close: memorable sentence, implication, or action.

For product videos:

- Pain or desired outcome.
- Product in use, not just product beauty.
- One feature per beat, tied to a user benefit.
- Proof: UI, result, comparison, testimonial, metric, or demonstration.
- CTA or next step.

For ads:

- Hook: recognizable problem, contradiction, spectacle, person-to-camera line, product-in-action, or fast before/after.
- Relevance: "this is for me" signal.
- Value proposition: one main claim, not a pile of features.
- Proof or demo.
- Offer, urgency, or CTA.

For trailers/teasers:

- World or premise.
- Disruption.
- Escalation through increasingly consequential images.
- Signature moments.
- Final button: joke, shock, title, date, product/logo, or unresolved question.

For documentary-style pieces:

- Claim/question.
- Human anchor or observed reality.
- Evidence beats.
- Counterpoint or complication.
- Synthesis without over-explaining.

For music/beat-driven edits:

- Map sections first: intro, groove, lift, drop, bridge, finale.
- Assign visual energy to musical energy.
- Use repetition with variation: recurring subject, movement, color, framing, or motif.
- Reserve the strongest visual change for the strongest musical change.

## Shot selection: assign function, then choose

Log or infer each candidate shot with:

- ID/path/source/provider/seed/version/license/rights status.
- Duration, usable in/out range, frame rate, resolution, aspect ratio, audio status.
- Shot type: establishing, wide, medium, close-up, insert, cutaway, reaction, POV, screen capture, graphic, title, transition, product macro, proof shot, texture.
- Content: subject, action, text visible, brand marks, faces, hands, UI state, object state.
- Motion: camera, subject, dominant direction, speed, start/end pose.
- Continuity risks: identity drift, lighting mismatch, impossible geography, bad hands, text artifacts, logo distortion, physics issues.
- Editorial value: orient, reveal, prove, compare, intensify, bridge, breathe, or close.

Select shots by function, not prettiness. Keep a beautiful generated shot only if it carries story value or emotional force. Reject shots that introduce unpayable questions unless confusion is intentional.

Common shot functions:

- Establishing: where/what scale are we in?
- Insert: what exact detail matters?
- Reaction: how should the viewer feel about what just happened?
- Cutaway: what covers a time jump, compresses action, or adds context?
- Proof: what makes the claim credible?
- Bridge: what lets two discontinuous moments connect?
- Reset: where can the viewer breathe before density rises again?
- Button: what last image or sound seals the beat?

## Continuity editing for generated and mixed media

Use continuity when the viewer must believe events are connected in time and space.

Check:

- Screen direction: a subject moving left-to-right should usually keep that direction across adjacent shots unless you establish a turn, neutral shot, or deliberate disorientation.
- Eyeline: if a person looks screen right, the object/person they look at should be positioned to satisfy the implied look.
- Match on action: cut during a movement and continue the same action in the next shot when preserving flow.
- Object permanence: product color, logo, shape, UI state, outfit, props, hand count, and environment should not mutate accidentally.
- Temporal logic: if a cup is full, then empty, then full, the timeline needs a reason.
- Light and color: generated clips with different time-of-day or color temperature need a motivated transition, grade, or separation.
- Spatial scale: avoid cutting from macro to wide if the viewer cannot identify the object being magnified.
- Audio space: room tone, ambience, music bed, and reverb should not jump unless the location changes.

When continuity fails, choose one:

- Hide it: cut away, crop, cover with graphics, use a reaction, or trim unstable frames.
- Motivate it: turn mismatch into a time jump, dream logic, glitch, memory, or montage association.
- Separate it: insert a title card, wipe, sound bridge, flash, map, caption, or chapter beat.
- Regenerate/replace it: if the continuity problem corrupts identity, factual claims, product trust, or safety.

## Montage theory for production use

Montage creates meaning from juxtaposition. Use it when sequence matters more than continuous action.

Choose the montage relationship:

- Graphic: shots connect by shape, color, composition, line, texture, or visual mass.
- Rhythmic: shots connect by movement, beat, action speed, or cut length.
- Spatial: shots build or disrupt a sense of place.
- Temporal: shots compress time, compare past/present/future, or imply process.
- Associative: shots create an idea by collision, analogy, contrast, or metaphor.
- Emotional: shots intensify, release, or redirect feeling.
- Evidentiary: shots accumulate proof or examples.

Do not call every fast sequence a montage. A montage needs a transformation, contrast, accumulation, or idea that emerges across shots.

Useful montage patterns:

- Accumulation: one example, then another, then another, until the claim feels proven.
- Compression: remove procedural steps but preserve cause and result.
- Contrast: before/after, promise/reality, old/new, manual/automated, expensive/simple.
- Parallel escalation: two threads become more intense until they meet.
- Motif return: repeat an image or sound with changed meaning.
- Conceptual collision: place two images together so the viewer infers the relationship.

Avoid weak montage patterns:

- Random B-roll over narration.
- Visual synonyms that repeat the script literally without adding information.
- Unmotivated speed ramps and whip transitions.
- Cutting on every beat with no phrase-level shape.
- Visual escalation that arrives before the story stakes are established.

## Rhythm and pacing

Pacing is the viewer's perceived information flow, not just average shot length.

Shape rhythm with:

- Shot duration.
- Motion speed inside the frame.
- Narration density and pause length.
- Music tempo, bars, fills, drops, and transients.
- Caption length and reading speed.
- Visual complexity.
- Sound design attacks, risers, impacts, whooshes, silence.
- Repetition, variation, and rest.

Use faster cuts when:

- The viewer already understands the subject and needs energy.
- The beat is emotional rather than explanatory.
- The platform rewards immediate clarity and novelty.
- The source footage has redundant action.
- The music is the structural driver.

Use slower cuts when:

- The viewer must read UI, captions, labels, charts, or product details.
- A reaction, reveal, or emotion needs time to land.
- The shot contains complex spatial information.
- The voiceover is dense.
- The brand tone is premium, calm, technical, or documentary.

Review rhythm in passes:

1. Silent picture pass: does the visual story read without narration?
2. Audio-only pass: does the argument, emotion, and timing work without picture?
3. Caption-only pass: can a sound-off viewer understand the video?
4. Full pass: do picture, audio, captions, and graphics compete or cooperate?

## J-cuts, L-cuts, and sound bridges

Use split edits to make edits feel intentional and to bridge discontinuous visuals.

J-cut:

- Best for entering a new scene, thought, location, speaker, or energy before the viewer sees it.
- Use when the next beat should pull the viewer forward.
- Example use: hearing crowd noise before cutting from a quiet product close-up to a launch event.

L-cut:

- Best for preserving emotion, explanation, or ambience while the picture moves on.
- Use when a speaker's words should carry over proof shots, reactions, product inserts, or memory images.
- Example use: founder says "we almost missed payroll" while the image cuts to empty desks and a late-night spreadsheet.

Sound bridge:

- Use ambience, music, breath, effects, or a repeated sound motif to connect shots whose images do not match.
- Keep room tone and music continuity clean; abrupt audio holes are often more distracting than visual discontinuity.

## Match cuts, cutaways, transitions

Match cut:

- Connect shots through matched action, composition, shape, motion, color, sound, or concept.
- Use for elegance, compression, metaphor, or continuity.
- Do not use if the viewer needs a clear factual boundary and the match implies a false equivalence.

Cutaway:

- Use to compress time, hide a jump, show context, redirect attention, cover a bad generated frame, or add proof.
- Prefer cutaways that add meaning, not generic filler.
- In interviews or documentary edits, cutaways should relate to the statement being made or reveal a truthful context.

Transition:

- A straight cut is usually the default.
- Use dissolves for time passage, memory, softness, or comparison when motivated.
- Use wipes, whip pans, flashes, glitch, morphs, or animated transitions only when they match the visual language and do not hide weak structure.
- For generated media, transitions can mask discontinuity, but overuse makes the edit feel evasive.

## Beat sync and music-led editing

Create a beat map before cutting:

- BPM and time signature if known.
- Section boundaries: intro, verse, pre-chorus, chorus/drop, bridge, outro.
- Strong transients: kick, snare, clap, impact, vocal entry, fill, downbeat.
- Emotional lifts: risers, chord changes, silence, breakdowns.
- Required lyric boundaries if lyrics matter.

Then decide the sync strategy:

- Hard sync: cuts or visual impacts land on transients. Use for ads, hype, trailers, drops.
- Phrase sync: major story beats land on musical phrases, not every beat. Use for explainers, premium product films, documentaries.
- Counter-rhythm: visuals move against the beat for tension, irony, or unease.
- Motivated silence: remove or duck music for a line, reveal, impact, or joke.

Beat-sync checklist:

- Avoid cutting on every beat for the whole video; it becomes predictable.
- Let anticipation start before the beat and payoff land on or just before the beat.
- Keep dialogue intelligible; music-led editing must not bury the message.
- Check captions against musical hits; captions popping on every beat may harm readability.
- If using generated clips, trim unstable first/last frames before aligning to beats.

## Platform and format timing

Treat platform facts as volatile and verify them for the actual delivery date. The following facts were verified on 2026-07-10 from official sources listed above.

YouTube Shorts:

- Standard-channel square or vertical videos up to 3 minutes uploaded on or after 2024-10-15 are categorized as Shorts.
- Shorts views count starts/replays from 2025-03-31; "engaged views" remains a separate analytics metric.
- Heuristic: even though 3 minutes is allowed, design the first 3-5 seconds to establish why the viewer should continue.
- Heuristic: for explainers or product content, use a visible title/promise early because replay-count metrics do not prove comprehension.

TikTok ads:

- TikTok ad policy lists 5-60 seconds and standard sizes including 9:16, 1:1, and 16:9; in-feed auction specs have placement-specific details that may differ, including Non-Spark up to 10 minutes.
- Vertical 9:16 is the recommended in-feed direction in TikTok's June 2026 specs.
- Heuristic: keep the first shot visually active, legible, and native to the platform; do not rely on a static title card as the primary hook.
- Heuristic: if the video is an ad, show the product/use case earlier than you would in a cinematic teaser.

Meta Reels/Stories:

- Official Meta pages may require login or vary by region. Verify current requirements before final export.
- Heuristic: plan 9:16 safe-zone composition with captions, UI overlays, profile elements, and CTAs away from edges.

General social cutdowns:

- Make a platform-specific edit, not only a crop. Re-order the story if the audience context changes.
- Create a "sound-off intelligibility" pass for captions and visible context.
- Use safe-zone guides before final composition, especially for lower captions and right-side UI controls.

## Source and generated asset management

Every edit decision must be reproducible enough for another agent to revise it.

Maintain an edit inventory:

- Source ID and filename/path.
- Origin: user-supplied, generated, stock, screen-recorded, captured, rendered graphic, archival, licensed.
- Rights status and usage constraints.
- Provider/model/tool/version/seed/prompt for generated material when available.
- Creation date and any verification date for volatile platform/tool facts.
- Technical specs: frame rate, resolution, color space if known, audio channels, duration.
- Content notes: people, products, logos, UI states, readable text, sensitive info.
- Usable ranges with reason: good action, bad frames, stable product, caption-safe, logo clean.
- Rejected ranges with reason: drift, blur, artifacts, continuity failure, legal risk, factual error.

Use versioned edit artifacts:

- `v01_rough`: structure and coverage.
- `v02_story`: clarity, order, hook, payoff.
- `v03_rhythm`: timing, music, transitions.
- `v04_finish`: captions, graphics, mix, color, safe zones.
- `v05_delivery`: platform exports and QC notes.

For AI-generated media, preserve rejected shots if they explain a decision. A later agent may need to know why a visually attractive clip was not used.

## Revision workflow

Separate revision notes by type:

- Story: confusing order, missing stakes, weak CTA, unsupported claim.
- Timing: too slow, too fast, redundant, rushed reading, late payoff.
- Continuity: identity drift, screen direction, object state, audio space, UI mismatch.
- Style: too corporate, too chaotic, not native, too templated, not premium enough.
- Compliance/rights: captions, claims, copyrighted music, brand/logo misuse, platform policy.
- Technical: frame glitches, bad crops, dead audio, clipping, export specs.

Translate vague feedback into an edit action:

- "Make it punchier" can mean remove setup, shorten shots, bring proof earlier, use stronger music hits, reduce caption length, or cut pauses.
- "More cinematic" can mean fewer explanatory graphics, longer suspense, wider shots, motivated sound design, stronger contrast, or a trailer-like rise.
- "More premium" can mean slower pacing, cleaner typography, fewer transitions, richer sound bed, restrained motion, and more product confidence.
- "More social" can mean immediate human/action hook, shorter setup, bigger captions, native framing, lower polish, more direct claim.

Always produce revision notes as specific timeline-level decisions:

- Keep / cut / replace / move / trim / extend / cover / reframe / caption / duck audio / add bridge / change transition.
- Include the reason and expected viewer effect.

## Handoff to composition

When handing off an edit to a composition or render agent, provide a concrete edit decision list. Include:

- Global settings: duration, aspect ratio, frame rate, safe-zone assumptions, platform, audio mix target if known.
- Timeline beats: start/end time, source asset IDs, in/out ranges, visual action, narration/audio, captions/on-screen text, transition, SFX/music cue, notes.
- Layering: background, primary video/still, overlays, captions, logos, callouts, UI highlights, subtitles, lower thirds.
- Motion instructions: push-in, pan, hold, snap zoom, speed ramp, freeze, blur, parallax, text reveal, beat hit.
- Audio instructions: music start, ducking, J/L cuts, room tone, SFX, silence, impact, voiceover placement.
- QA flags: shots needing visual inspection, generated artifacts to mask, text to verify, legal/brand approvals pending.

Use this compact EDL shape when helpful:

| Time | Picture | Audio | Text/graphics | Edit note |
|---|---|---|---|---|
| 00:00-00:02 | Product macro, stable logo | Music hit + riser | "Stop losing edits" | Hook; cut on snare |
| 00:02-00:06 | UI screen capture, crop to timeline | VO starts before picture change | Cursor callout | J-cut from VO into proof |

## Edit QA

Run QA in focused passes:

Story pass:

- Can the viewer state the promise after the first few seconds?
- Does each beat change what the viewer knows, feels, or wants?
- Is there a clear payoff or CTA?
- Are claims supported by visuals or evidence?

Continuity pass:

- Do characters, products, UI, logos, colors, object states, and screen direction stay coherent enough?
- Are time and place shifts motivated?
- Are generated artifacts visible at cuts, hands, text, reflections, faces, or edges?

Rhythm pass:

- Do cuts land on meaningful movement, speech, breath, beat, or contrast?
- Is there enough variation in shot size, density, and rest?
- Are captions readable at the chosen pace?

Audio pass:

- Are dialogue/VO intelligible?
- Are J/L cuts and bridges clean?
- Does music support rather than fight the story?
- Are there pops, abrupt ambience changes, clipping, or dead air?

Platform pass:

- Does the edit fit duration, aspect ratio, safe zones, and caption needs?
- Does the first frame communicate value or intrigue?
- Is important text away from UI overlays?
- Does the video work sound-off if needed?

Rights and truth pass:

- Are licensed/stock/user/generated assets documented?
- Are product claims, testimonials, statistics, and UI states truthful?
- Are deepfake/avatar/synthetic people used with appropriate consent and disclosure when required by context?
- Is copyrighted music or third-party content cleared for the intended platform?

## Example: 30-second product ad edit plan

Intent: Make a B2B viewer understand that a project-management product prevents missed handoffs.

Inputs:

- Generated office stress clips.
- Screen recordings of dashboard and assignment flow.
- Product logo animation.
- Voiceover and music bed.
- Delivery: 9:16 social ad, 30 seconds.

Approach:

- 00:00-00:03: Start with a human problem, not the logo. Quick close-up of three overlapping message notifications. Overlay: "The handoff failed again?"
- 00:03-00:07: J-cut VO starts before dashboard appears: "Most teams don't need another meeting..." Picture cuts to messy calendar, then blank task owner field.
- 00:07-00:14: Product proof. Screen capture shows auto-owner assignment, status change, due date. Use L-cut from VO over UI inserts. Hold long enough for UI text to read.
- 00:14-00:20: Contrast montage. Before: scattered Slack/email/calendar. After: one dashboard with owner and next action. Use graphic match between red overdue badge and green completed badge.
- 00:20-00:26: Outcome. Team member closes laptop calmly. Use slower shot and music lift to create relief.
- 00:26-00:30: CTA/logo. One line only: "Make every handoff visible." Button/URL in safe zone.

Why this works:

- Story order moves from pain to proof to relief.
- Screen recordings are held longer than emotional B-roll.
- The edit uses a match cut for conceptual contrast, not decoration.
- Captions and UI are protected from platform overlays.

Likely failure modes:

- Cutting UI proof too quickly.
- Letting generated office clips drift in character identity.
- Using too many notification graphics until the ad feels generic.

## Example: 60-second documentary-style montage

Intent: Explain how a community garden changed a neighborhood without pretending all problems are solved.

Inputs:

- Interview clips from two residents.
- B-roll of empty lot, planting, kids watering, harvest table.
- Archival still of the lot before cleanup.
- Ambient audio and light music.

Approach:

- Start with a quiet visual: empty lot archival still, then present-day wide shot. Let ambience lead before music.
- Use an L-cut from resident line "Nobody crossed this block after sunset" over the archival still and boarded fence.
- Cut to hands planting, not a generic smiling montage, when the story turns to action.
- Use cutaways to tools, soil, signs, and neighbors to cover interview trims.
- Let one interview reaction breathe after a difficult line; do not cover every silence.
- Build montage by season/process: clearing, planting, watering, gathering.
- End with an honest unresolved note if present: "It's not fixed everything, but now people stop here."

Why this works:

- The montage accumulates evidence over time.
- L-cuts preserve human voice while showing context.
- The edit avoids false triumphalism by allowing complication.

Likely failure modes:

- Overusing upbeat music and erasing the story's tension.
- Using B-roll unrelated to the speaker's claim.
- Cutting interviews so tightly that people sound unnatural.

## Example: beat-driven trailer beat sheet

Intent: Create a 45-second AI-generated sci-fi teaser from generated clips.

Inputs:

- 12 generated clips: city, lab, protagonist, signal, chase, sky anomaly.
- Music track with 8-second intro, 16-second pulse section, 8-second breakdown, 13-second final rise.
- Minimal dialogue fragments.

Approach:

- 00:00-00:08 intro: slow city shots, one mysterious sound bridge, title fragment. Cut on phrase boundaries, not every beat.
- 00:08-00:24 pulse: shorten shot durations progressively. Alternate protagonist, signal, consequences. Trim generated clip heads/tails where identity wobbles.
- 00:24-00:32 breakdown: remove music density, use one line of dialogue and a held close-up. Let tension breathe.
- 00:32-00:43 final rise: hard sync impacts to strongest transients. Use increasingly large-scale images: lab failure, chase, sky anomaly.
- 00:43-00:45 button: silence half-beat, then title/date impact.

Why this works:

- The music structure drives escalation.
- The breakdown creates contrast before the final rise.
- Generated-media weaknesses are handled through trimming and scale alternation.

Likely failure modes:

- Showing the largest anomaly too early.
- Cutting every beat from the start, leaving no escalation.
- Letting inconsistent protagonist shots imply multiple characters.

## Source notes

Primary sources consulted include Yale Film Analysis on editing relationships; W3C WCAG 2.2 and DCMP/Netflix timed-text guidance for captions; YouTube Help and TikTok Ads Help for volatile platform facts verified on 2026-07-10; DINFOS Pavilion for J/L cuts; and Adobe Help for collaboration/media-management concepts. Treat platform specs, ad policies, and tool workflows as volatile and re-check them at delivery time.
