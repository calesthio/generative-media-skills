---
name: title-kinetic-typography
description: Provider-independent title design and kinetic typography direction for video, animation, ads, explainers, social hooks, brand films, lyric/text videos, title cards, main titles, lower thirds, captions-as-design, and other motion-led text. Use when an agent must plan, prompt, implement, hand off, iterate, or QA typography hierarchy, readability, timing, reveal/hold/exit, motion semantics, line breaks, safe areas, localization, brand constraints, accessibility, flashing/motion safety, or production specs for animated text.
---

# Title and kinetic typography direction

Use this skill to make text behave like a designed scene, not a decorative overlay. Treat every text element as a timed editorial decision with a job: identify, explain, sell, signal emotion, guide attention, or make speech readable.

This is provider-independent. It applies whether the final asset is built in After Effects, HTML/CSS/GSAP, Remotion, Lottie, a game engine, subtitles, an AI video prompt, or a still-image/video generator. When exact text must remain correct, prefer editable/rendered typography layers over asking an image or video generator to invent letterforms.

## Separate facts, observations, and heuristics

Documented facts:

- WCAG 2.2 requires web content to avoid more than three flashes in any one-second period unless flashes are below threshold; apply this as a conservative safety rule for video text even when the deliverable is not a web page.
- WCAG guidance on moving, blinking, scrolling, or auto-updating content lasting more than five seconds supports giving viewers control where the medium allows it; when control is impossible, reduce or simplify nonessential motion.
- Unicode and W3C internationalization resources define line breaking as script-specific; do not assume English word-wrap behavior works for CJK, Thai, Arabic, Indic scripts, or mixed-script titles.
- TikTok ad safe-zone documentation says key elements such as text and logos must be inside the relevant safe zone, and that safe-zone size changes with ad dimension, caption length, and add-ons. Verified 2026-07-10.
- Google Ads video spec guidance says important elements such as logos, products, and supers should be within the provided safe area to reduce the risk of being covered in certain inventory. Verified 2026-07-10.
- Meta Reels/Stories safe-zone guidance can be accessed in Ads Manager, but public access may require login; verify current placement overlays in the account before final ad delivery. Verified 2026-07-10.

Empirical observations:

- AI image/video generators can produce attractive letter-like textures while corrupting exact spelling, kerning, punctuation, brand glyphs, and multilingual text. Use them for backgrounds, typographic mood frames, or abstract letter motion only after checking exact glyph fidelity.
- Motion text that looks clear on a desktop preview often fails on phones because platform chrome, compression, glare, thumbs, captions, and reduced viewing time change readability.
- Fast kinetic typography can feel impressive in isolation but becomes tiring when every word is animated with the same intensity.

Production heuristics:

- Make the message readable first, expressive second, and novel third.
- Animate the smallest unit that serves meaning: block, line, word, syllable, glyph, stroke, or texture. Smaller units increase energy and risk.
- Use motion to clarify a relationship or change state. If motion does not clarify, emphasize, pace, or delight, remove it.
- Build a text system before building shots: type roles, safe zones, timing rules, motion vocabulary, brand constraints, accessibility limits, and QA checks.

## Start with the text job

Classify each text element before designing it.

- Main title: announces the piece and carries the strongest tone. It can be expressive, but it still needs a clean readable hold.
- Title card/intertitle: resets chapters, compresses story beats, or creates anticipation. It must work without voiceover.
- Lower third: identifies a person, place, product, source, or metric while other content remains primary. It should enter politely, hold long enough to read, then leave without stealing the cut.
- Caption-as-design: reinforces speech or music while becoming part of the visual language. It must still serve deaf/hard-of-hearing viewers if it replaces accessible captions.
- Lyric/text video: makes text the main performance. Pacing, line breaks, and emotional motion are the edit.
- Social hook: creates immediate recognition in the first seconds. It must survive platform overlays and fast scrolling.
- CTA/super/legal: conveys a required message. Clarity, compliance, and safe placement outrank flourish.

For each element, write a one-line job:

- "Hook the first two seconds with one provocative phrase."
- "Identify the speaker without covering hands or face."
- "Make the chorus feel like a collective chant while keeping every lyric readable."
- "Reveal the product claim and proof in the same gaze path."

If the job is vague, the design will drift into generic motion.

## Build typographic hierarchy

Define roles before choosing animation.

- Primary: the one thing the viewer must read now.
- Secondary: context that can be read after the primary message.
- Tertiary: source, date, label, handle, disclosure, or metadata.
- Ambient: decorative letterforms, oversized cropped words, typographic texture, or repeated phrases that are not required reading.

Use contrast deliberately:

- Size: the fastest hierarchy cue, but it consumes safe area.
- Weight: useful for emphasis; avoid too many weights in one frame.
- Case: all caps can work for short labels and impact words, but use tracking and avoid long all-caps passages.
- Width: condensed faces save space but can reduce legibility; expanded faces feel premium or cinematic but need room.
- Color and value: type must separate from the background throughout motion, not only on a still frame.
- Position: top, center, lower third, side rail, or full-frame title changes perceived importance.
- Motion: faster, earlier, larger, or more elastic motion reads as more important.

Do not use every contrast axis at once. A strong title often uses one dominant contrast and one supporting contrast.

## Readability rules for motion text

Design for the delivery context, not the artboard.

Check these conditions:

- Smallest target device and expected viewing distance.
- Aspect ratio and crop variants.
- Background movement, contrast changes, and compression.
- Platform UI overlays, captions, profile handles, buttons, and ad CTAs.
- Whether the viewer has audio, watches muted, or depends on captions.
- Whether the text is exact brand/legal copy or flexible editorial language.

Practical guardrails:

- Keep important reading text in the safe area for the target platform or create platform-specific versions.
- Give every critical phrase a readable hold after the reveal and before the exit.
- Avoid putting critical type over faces, hands, eyes, small product details, subtitles, or high-motion background regions.
- Add a backing plate, gradient, shadow, blur, stroke, or dimming pass when the background changes behind the text.
- Review at 100% output size and on a phone, not only in the editor.
- Use sentence case for longer phrases unless the brand requires otherwise.
- Avoid more than two active text ideas in a single frame.

For captions and subtitles, borrowed broadcast/education norms are useful but not absolute for designed social content. DCMP guidance supports short caption durations long enough to read, no more than two lines, and safe-zone placement. Use tighter or looser settings only when the content, audience, and platform justify it.

## Line breaks are editorial

Line breaks change meaning, rhythm, and visual balance. Never accept auto-wrap for hero text without review.

For English and similar space-separated scripts:

- Break at semantic chunks: noun phrase, verb phrase, contrast pair, setup/payoff.
- Keep modifiers attached to the words they modify.
- Avoid orphaned small words when they make the line feel accidental.
- Avoid splitting names, numbers with units, product names, URLs, handles, hashtags, and legal phrases.
- Use line length to create rhythm: short line for punch, wider line for calm explanation.

For multilingual and mixed-script work:

- Ask for the target language, locale, script, reading direction, and approved translation.
- Do not force English capitalization, word spacing, or line-break habits onto other scripts.
- Use proper shaping for Arabic and Indic scripts; do not animate isolated glyphs if shaping changes meaning or readability.
- For right-to-left text, design the reveal direction and reading order intentionally; do not just mirror an English layout.
- For CJK, consult locale-appropriate line-breaking rules and avoid illegal punctuation starts/ends.
- For Thai, Lao, Khmer, and other scripts without visible word spaces, use a text engine or line-breaker appropriate to the language.
- Leave expansion room. Translated text may grow, shrink, or change line count; design variants rather than squeezing one layout.

When text is localized, define a "meaning lock" and a "layout lock":

- Meaning lock: words, names, numbers, disclosures, and claims that cannot change.
- Layout lock: maximum lines, safe-area box, approximate emphasis points, and timing budget.

If the translation cannot satisfy both, escalate instead of silently shrinking type until it is unreadable.

## Timing: reveal, hold, exit

Every text beat needs three timed states.

Reveal:

- Establish where to look.
- Signal tone and importance.
- Avoid over-animating before the viewer can recognize the phrase.

Hold:

- Let the viewer actually read.
- Keep the text stable enough for comprehension.
- Use micro-motion only when it supports the mood and does not damage readability.

Exit:

- Prepare the cut, transition, or next idea.
- Avoid exiting before the last word can be read.
- Use exits as punctuation: snap, dissolve, wipe, drift, collapse, cut, smear, or deconstruct.

Timing heuristics:

- Social hook title: reveal within the first second unless intentional suspense is the concept.
- Lower third: enter after the viewer sees the person or subject; hold through the first complete identification moment.
- Main title: allow a clean hero hold, even if the reveal is complex.
- Captions-as-design: synchronize to speech or music, but favor readable phrasing over word-by-word chaos.
- Lyric video: let musical meter drive entrances; let meaning drive holds.
- Legal/disclosure: do not animate so fast that it appears intentionally hidden.

Do not time only by seconds. Time by attention:

- What is the viewer looking at before the text appears?
- What visual event competes with the text?
- What audio beat justifies the motion?
- What must be understood before the next cut?

## Motion semantics

Motion should mean something. Create a small vocabulary and reuse it consistently.

Common mappings:

- Rise or lift: emergence, optimism, status, activation.
- Drop or fall: consequence, weight, failure, impact.
- Slide from source direction: arrival, attribution, entering a conversation.
- Scale up: importance, confidence, proximity; overuse can feel cheap.
- Scale down: precision, compression, realization.
- Blur to focus: discovery, clarification, memory.
- Wipe/reveal: proof, unveiling, editorial certainty.
- Type-on: process, evidence, live thought, computation.
- Scramble/glitch: uncertainty, error, cyber aesthetic; dangerous for readability and accessibility if too aggressive.
- Stretch/squash: playfulness, tactility, musicality.
- Tracking expansion: luxury, breath, distance, cinematic pause.
- Kinetic collision: conflict, humor, emphasis, impact.
- Masked behind objects: spatial integration, premium compositing, realism.

Use expressive motion for high-value moments and productive/subtle motion for supporting labels. IBM Carbon's motion guidance distinguishes subtle productive motion from more visible expressive motion; that distinction is useful for title systems even outside UI.

## Safe areas and platform variants

Safe areas are volatile. Verify them at export time for the exact placement, account, and ad product.

As of verification on 2026-07-10:

- TikTok ad documentation states that text/logos must stay within safe zones and that safe-zone size depends on format, caption length, and add-ons; preview the actual effect before delivery.
- Google Ads provides safe-area references/templates for video ads and warns that important elements can be covered in some inventory if placed outside the safe area.
- Meta has safe-zone guardrails for Reels and Stories ads in Ads Manager, but public help pages may require login; use the account preview/guardrail before final delivery.
- Third-party Shorts safe-zone tools commonly describe YouTube Shorts as 9:16 with top, bottom, and right-side UI risk. Treat these as useful overlays, not authoritative platform guarantees; verify in YouTube/Google ad tooling when buying media.

Production rule: if one asset must serve TikTok, Reels, Shorts, and paid ads, design the critical message in a conservative central band and make platform-specific exports for CTAs, captions, and lower thirds.

## Brand constraints

Before designing, ask for:

- Approved typefaces, fallback fonts, and font licensing for video embedding.
- Logo clear space and minimum size.
- Color palette, contrast requirements, and forbidden combinations.
- Brand voice: calm, witty, premium, aggressive, editorial, playful, institutional.
- Motion principles: snappy, cinematic, restrained, elastic, mechanical, organic.
- Required words, legal copy, trademark formatting, punctuation, capitalization, and pronunciation.
- Localization requirements and markets.

If no brand system exists, create a lightweight one:

- One display face or display treatment.
- One readable support face.
- Three text roles: hero, support, metadata.
- Two motion intensities: functional and expressive.
- One safe-area grid per aspect ratio.
- One contrast/backplate rule.

Do not invent trademark styling. Preserve capitalization, marks, accents, registered/trademark symbols, model numbers, URLs, and legal phrasing.

## Accessibility and safety

Treat accessibility as part of the design brief.

Checklist:

- Contrast: keep text distinguishable throughout motion; test worst frame, not best frame.
- Motion sensitivity: avoid unnecessary camera shake, intense zoom loops, rapid oscillation, and large repeated parallax when the viewer cannot opt out.
- Flashing: avoid more than three flashes in any one-second period unless verified below WCAG thresholds; be stricter for full-screen high-contrast flashes.
- Reading time: hold critical text long enough for the target audience and complexity.
- Captions: if designed captions replace standard captions, include all essential speech and meaningful non-speech audio.
- Non-audio comprehension: title cards and hooks should still communicate when muted.
- Dyslexia/cognitive load: avoid cramped spacing, excessive all-caps passages, rapidly changing fonts, or word-by-word animation for dense explanations.
- Color dependence: do not use color alone to communicate speaker, status, error, or emphasis.

When safety is uncertain, reduce contrast of flashes, slow the transition, remove alternation, or replace flashing with a wipe, dim, blur, or single impact cut.

## Prompting and specification

For generative tools, state the typography as an art direction and a fidelity constraint.

Include:

- Exact text and allowed variations.
- Language/script and reading direction.
- Type personality, not just font name: geometric sans, editorial serif, condensed grotesk, monospaced terminal, hand-lettered brush, etc.
- Hierarchy: primary/secondary/tertiary roles.
- Layout: aspect ratio, safe area, position, number of lines.
- Timing: reveal, hold, exit durations or beats.
- Motion semantics: why it moves that way.
- Background relationship: backing plate, mask, depth, interaction, or separation.
- Accessibility limits: contrast, flash, reduced-motion, readable hold.
- Deliverable: editable layers, alpha, vector, baked video, subtitles, or prompt-only concept.

Avoid vague requests like "cool kinetic typography." Replace them with a text system:

- "The phrase `STOP SCROLLING` appears as two stacked lines, heavy condensed sans, white on black, central safe area. It slams in on the first drum hit, overshoots 6%, settles by 0.35s, holds stable for 1.0s, then cuts out. No flicker or glitch."

For AI video/image prompts, add a recovery plan:

- "If exact lettering is unreliable, generate the background plate without text and render typography separately."

## Implementation handoff

Hand off a kinetic typography spec that another agent or designer can build without guessing.

Minimum spec:

- Canvas: resolution, aspect ratio, frame rate, duration.
- Text inventory: exact text, role, language, pronunciation if relevant.
- Layout: bounding boxes, alignment, safe-area constraints, responsive/crop variants.
- Typography: font family or category, weight, size range, tracking, leading, case, color, effects.
- Timing: in/out frame or timecode, reveal/hold/exit, sync points with audio/cuts.
- Motion: transform properties, easing, intensity, stagger, masks, blur, deformation, physics notes.
- Background interaction: plates, mattes, occlusion, shadows, dimming, collision, depth order.
- Accessibility: contrast target, flashing check, reduced-motion alternate if needed, caption completeness.
- Localization: expansion budget, line-break rules, RTL/CJK considerations, review owner.
- QA: device/platform checks, exact text proofing, brand/legal approval.

Use frame numbers for implementation when possible. Use seconds only when the tool does not expose frames.

## Iteration workflow

Review in this order:

1. Text accuracy: spelling, punctuation, capitalization, names, numbers, legal copy, and language.
2. Readability: can the target viewer read it on the target device while the video plays?
3. Hierarchy: does the eye go to the right phrase first?
4. Timing: does the reveal/hold/exit fit the edit and audio?
5. Motion meaning: does motion reinforce the message?
6. Safe areas: does any platform UI cover important text?
7. Brand: does the treatment match the brand's type, tone, and motion rules?
8. Accessibility/safety: contrast, flashing, motion intensity, caption completeness.
9. Craft: kerning, line breaks, easing, masks, alignment, optical balance, compression artifacts.

Do not iterate only from still frames. Scrub, play at speed, watch on a phone, and check the worst frame.

## Common failure modes

- Text is misspelled or AI-hallucinated.
- Reveal is beautiful but the hold is too short.
- Every word animates, so no word matters.
- Lower thirds cover captions, faces, hands, or product action.
- Safe-zone assumptions from one platform are reused for another.
- Legal or CTA text is squeezed into unreadable microtype.
- Brand fonts are unavailable, substituted silently, or unlicensed.
- Localization expands beyond the box and is fixed by shrinking below legible size.
- Glitch/flicker effects create flash risk or make letters unreadable.
- Motion direction conflicts with reading direction or story meaning.
- Text contrast is checked on one frame but fails over moving footage.

## Example: social hook

Intent: vertical social ad hook for a meal-planning app, 9:16, muted-first viewing.

Spec:

- Text: `Dinner decisions are stealing your week.`
- Role: primary hook.
- Layout: two lines in the central safe band; avoid right-side UI and lower caption/CTA areas.
- Type: bold humanist sans, sentence case, tight but readable leading.
- Motion: `Dinner decisions` slides up as one block over 8 frames; `stealing your week` wipes on from left to right with a slight drag, then holds.
- Timing at 30 fps: reveal 0:00-0:14, hold 0:14-1:18, exit on cut at 1:18.
- Background: dim food-prep footage behind text by 35%; add soft shadow only if compression test needs it.
- Safety: no flash, no glitch, stable hold.
- QA: phone preview with platform UI overlay; exact punctuation proof.

Why structured this way: the text job is to stop scrolling, so the line is short, the hierarchy has one idea, motion reinforces loss of time without sacrificing a readable hold.

## Example: main title

Intent: premium brand film title over slow macro product footage.

Spec:

- Text: `Built for the long run`
- Role: main title.
- Layout: centered, one line on 16:9; two-line optical break for 9:16: `Built for / the long run`.
- Type: elegant high-contrast serif or brand display face; avoid thin hairlines if compression or small screens are expected.
- Motion: letters begin with slightly expanded tracking, then settle inward over 32 frames as the camera push-in slows. No per-letter bounce.
- Timing: reveal begins after the product silhouette is recognizable; hold at least one full breath before the next cut.
- Background: dark-to-mid gradient plate behind type; keep product logo unobstructed.
- Accessibility: no flashing; contrast checked against the brightest product highlight.

Why structured this way: premium tone comes from restraint, space, and a clean hold, not from many animated effects.

## Example: captions-as-design

Intent: explainer video uses designed captions as the main visual rhythm.

Spec:

- Spoken line: "The trick is not doing more. It is removing the decision."
- Caption text: `Not doing more.` then `Removing the decision.`
- Role: accessible caption and emphasis graphic.
- Layout: lower-middle safe area, not bottom edge; two-line maximum.
- Type: readable sans, white text on translucent charcoal rounded plate.
- Motion: first clause appears on speech start, holds, then the word `more` gently fades down. Second clause replaces it with a clean upward wipe, emphasizing `decision` in brand accent color.
- Timing: synchronize to speech phrase boundaries, not every word.
- Accessibility: include the full meaning of the spoken line; do not rely on accent color alone; avoid covering diagrams.

Why structured this way: the caption is edited for comprehension while preserving the speaker's meaning. Motion marks the conceptual reversal.

## Source notes

Use these as grounding, not as a substitute for current project specs:

- W3C WCAG 2.2, including 2.3.1 Three Flashes or Below Threshold and 2.2.2 Pause, Stop, Hide: https://www.w3.org/TR/WCAG22/ and https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- W3C Internationalization line-breaking overview and Unicode UAX #14: https://w3c.github.io/i18n-drafts/articles/typography/linebreak.en and https://www.unicode.org/reports/tr14/
- W3C Japanese Layout Requirements and language enablement resources: https://www.w3.org/2007/02/japanese-layout/docs/aligned/japanese-layout-requirements-en.html and https://www.w3.org/TR/typography/
- IBM Carbon motion guidance, including productive versus expressive motion and evaluation checklist; checked 2026-07-10: https://carbondesignsystem.com/elements/motion/overview/ and https://carbondesignsystem.com/elements/motion/resources/
- Material Design typography and motion references for hierarchy and purposeful motion: https://m3.material.io/styles/typography/overview and https://m2.material.io/design/motion/understanding-motion.html
- Apple Human Interface Guidelines typography, motion, and accessibility references: https://developer.apple.com/design/human-interface-guidelines/typography and https://developer.apple.com/design/human-interface-guidelines/motion
- TikTok Ads safe-zone documentation for interactive add-ons; checked 2026-07-10: https://ads.tiktok.com/help/article/tiktok-interactive-add-on-download-card-ad-specifications
- Google Ads video ad specs and safe-area templates; checked 2026-07-10: https://support.google.com/google-ads/answer/13547298
- Meta Business Help safe-zone page may require login; verify in Ads Manager safe-zone guardrails for active placements. Public URL checked 2026-07-10: https://www.facebook.com/business/help/980593475366490
- DCMP Captioning Key and presentation-rate guidance: https://dcmp.org/learn/captioningkey and https://dcmp.org/learn/601-captioning-key---presentation-rate
- Netflix English timed-text style guide for professional timed-text requirements: https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide
- Butterick's Practical Typography for practical hierarchy, all-caps spacing, headings, and line-length craft: https://practicaltypography.com/
- Recent research on AI/dynamic typography highlights the dual need for aesthetic motion and readable glyphs, e.g. "Dynamic Typography" (2024) and "Kinetic Typography Diffusion Model" (2024): https://arxiv.org/abs/2404.11614 and https://arxiv.org/abs/2407.10476
