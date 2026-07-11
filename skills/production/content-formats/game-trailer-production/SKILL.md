---
name: game-trailer-production
description: "Provider-independent production workflow for AI agents creating game trailers and promos, including announcement, gameplay, launch, DLC/update, store-page videos, social cutdowns, and generated/engine-capture hybrid trailers. Use when planning, scripting, capturing, generating, editing, localizing, reviewing, or QAing game marketing videos where gameplay truthfulness, platform/store constraints, ratings, accessibility, claims, CTA metadata, and rights provenance matter."
---

# Game trailer production

Use this skill to make trailers that sell the game without misrepresenting it. Treat a trailer as both creative work and regulated marketing: it must show the game clearly, preserve gameplay truth, respect platform/store rules, and survive publisher, ratings, localization, accessibility, and legal review.

This is not legal advice. Escalate to the publisher, platform representative, ratings body, or counsel when the trailer includes claims, third-party IP, paid endorsements, user data, minors, rating-sensitive content, AI-generated realism, region-specific offers, platform-exclusive language, or anything not yet implemented in the game.

## First classify the deliverable

Ask for the intended primary deliverable before structure or capture planning. If the user gives only "make a trailer," propose a primary and optional cutdowns.

- Announcement teaser: reveal existence, fantasy, tone, world, premise. Useful before gameplay is final. Do not imply final gameplay systems unless they are real or clearly labeled.
- Gameplay trailer: show actual play, verbs, UI readability, systems, player agency, combat/puzzle/exploration loop, progression, stakes.
- Launch trailer: combine fantasy, proof, availability, platforms, edition/CTA, review quotes only if approved and allowed by the storefront.
- DLC/update/season trailer: show what is new, who it is for, ownership requirements, base-game dependency, release window, and region/platform availability.
- Store-page video: optimize for mute autoplay, first 5-10 seconds, accurate in-game expectation, platform specs, subtitles/captions, and thumbnail/poster frame.
- Social cutdown: one idea, one hook, no slow ramp, safe title/action area, captions burned or provided per platform, CTA adapted to the surface.
- Generated/engine-capture hybrid promo: use generated shots only where they do not replace gameplay proof or misrepresent playable content.

## Intake that must exist before production

Collect these facts in a production brief. If missing, ask or mark as "TBD, blocked for final export/review."

- Game identity: title, subtitle, genre, short positioning line, developer/publisher, rating status, platforms, store links, region/language targets.
- Build facts: build version/date, branch, platform captured from, target FPS/resolution, known visual bugs, debug overlays to avoid, final vs pre-release art status.
- Game truth: core loop, playable verbs, player character(s), camera perspective, UI/HUD mode, multiplayer/online status, monetization, accessibility features, performance targets that are already substantiated.
- Trailer goal: awareness, wishlists, conversion, launch, update adoption, press beat, festival showcase, platform store submission, paid ad, organic social.
- Audience: new players, existing community, genre fans, press/creators, platform featuring team, ratings-safe broad audience, parents, competitive players, cozy/casual players, etc.
- Asset inputs: engine capture availability, previous trailers, key art, logo lockup, music rights, SFX library, VO script/voice, localization glossary, approved screenshots, rating badges/descriptors, legal disclaimers.
- Constraints: max duration, aspect ratios, store/platform specs, forbidden content, spoilers, publisher brand rules, embargo dates, price/discount/edition wording, required mnemonics or end slates.
- Reviewers: game director, capture lead, marketing lead, platform/store owner, community, localization, accessibility, ratings/compliance, legal/counsel.

## Truthfulness rules

The trailer must create excitement from the real product, not from a hypothetical better product.

Maintain a "truth ledger" while planning and editing:

| Element | Required proof |
|---|---|
| Gameplay shot | Build, level, mode, platform, capture date, whether HUD/camera/speed was modified |
| Feature claim | Evidence owner, implementation status, supported platforms/regions, conditions or limitations |
| Performance claim | Hardware/platform, mode, resolution/FPS test evidence, whether target is final |
| Multiplayer/online claim | Player count, online/local, crossplay/cross-save status, subscription/platform dependencies |
| Content claim | Whether content is base game, DLC, preorder bonus, season/event, unlockable, or paid add-on |
| Review/award quote | Source, exact approved quote, date, usage rights, storefront rules allowing it |
| Generated shot | Prompt/model/tool, intended role, what it represents, why it cannot be mistaken for playable footage |

Use these labels when needed:

- "Gameplay captured in-engine" only when the shot is recorded from the engine/game runtime.
- "Pre-alpha / alpha / beta footage" when visuals or systems are not final.
- "Cinematic trailer" when a shot is non-playable or pre-rendered.
- "Not actual gameplay" or a clearer equivalent when a generated or cinematic shot could be mistaken for play.
- "Feature shown requires [DLC/base game/login/subscription/online]" when omission would mislead.

Avoid these trailer sins:

- showing cinematics, generated b-roll, debug free-camera, or replay camera as if they are direct gameplay;
- hiding the UI for a gameplay trailer when UI readability is central to user expectation;
- cutting so fast that the player cannot understand the genre or interaction loop;
- using unimplemented features, target renders, old prototypes, or dev cheats without labeling and approval;
- making comparative or superlative claims ("fastest," "most realistic," "first ever," "4K/120," "no pay-to-win") without substantiation;
- using "available now," prices, discounts, platform logos, ratings, or edition names before the responsible owner confirms them for each region.

## Capture planning

Write a capture plan before generating or editing. A strong plan makes the eventual trailer easier to prove.

1. Select capture pillars: 3-5 things the trailer must prove, such as traversal, tactical combat, cozy building, boss scale, social play, customization, exploration, horror tension, procedural replayability, or platform-specific controls.
2. Map each pillar to shots: opener, readable loop proof, escalation, hero moment, CTA.
3. Assign capture type:
   - direct player gameplay: highest truth value; use for core loop and store-page proof;
   - in-engine cinematic/camera path: useful for world scale and mood; label when not representative of play;
   - UI/HUD capture: required for systems, inventory, card mechanics, tactics, building, accessibility features, and anything where interaction matters;
   - engine replay/photo mode/debug camera: acceptable for beauty shots if not passed off as gameplay;
   - generated b-roll: only for abstract mood, transitions, lore, non-product metaphor, or clearly separated cinematic framing.
4. Define technical settings: platform, resolution, frame rate, HDR/SDR, audio split, UI language, control glyphs, no debug overlays, safe-area guides, capture codec, naming convention.
5. Create a shot log: shot ID, build, level, action, start/end time, capture operator, notes, approval status, and any manipulation.

Capture for edit, not for archives. For each beat, capture:

- 3-5 clean attempts with handles before/after the action;
- one wide/context shot, one readable medium shot, one hero close/detail;
- HUD-on and HUD-off variants when allowed;
- clean ambience/SFX passes when audio matters;
- failures/outtakes only if the final brand voice intentionally uses them.

## UI and HUD treatment

Do not assume "cinematic" means "hide the HUD." Decide based on the trailer type:

- Gameplay trailer: preserve enough HUD/UI to prove interaction, resources, targeting, cards, inventory, party, choices, build tools, dialogue, or objective state.
- Announcement/launch trailer: mix HUD-off beauty with selected HUD-on proof. Avoid making the game look like a different genre.
- Store-page video: prioritize actual in-game experience early. A mute/autoplay viewer should understand what the player does.
- Mobile/App Store-style preview: stay inside the app/game, show captured device/app experience, and disclose in-app purchases, subscriptions, login requirements, or paid features when shown.
- Social cutdown: enlarge or crop only if it does not create false UI expectations. Use callout graphics to explain small UI instead of zooming into unreadable clutter.

When changing HUD, speed, camera, FOV, color, enemy behavior, damage, recoil, cooldown, or difficulty for capture, record it. If the change affects player expectation, disclose or avoid the shot.

## Trailer structure and beat maps

Use structure as a starting point, not a formula. The best structure depends on audience awareness, genre, and where the trailer will autoplay.

### 60-90 second gameplay/launch trailer

- 0-3s: instantly recognizable hook, no logo-only cold open unless the IP is already famous.
- 3-12s: genre and player verb clarity; answer "what do I do?"
- 12-30s: core loop proof through readable gameplay, not only montage.
- 30-50s: escalation: systems, enemies, stakes, customization, co-op, narrative complication, or world variety.
- 50-70s: hero moments: boss, reveal, transformation, build payoff, emotional beat, multiplayer chaos, spectacular mechanic.
- 70-85s: release/platform/CTA, rating/disclaimer/edition requirements, wishlist or buy action.
- Optional final sting: one joke, reveal, threat, or community-friendly moment after the CTA, only if it does not obscure required metadata.

### 30 second store-page video

- 0-5s: gameplay image that communicates genre even muted.
- 5-15s: primary loop, with UI/HUD if it clarifies play.
- 15-24s: variety and depth: second biome, enemy, build type, character, puzzle, system combo.
- 24-30s: title, platform/store CTA, release status. Keep copy evergreen if store review cycles are long.

### 15 second social cutdown

- 0-2s: thumb-stopping mechanic or spectacle.
- 2-8s: one clear setup-to-payoff action.
- 8-12s: second proof or reaction beat.
- 12-15s: title and CTA. Avoid tiny logos and dense disclaimers; use caption copy that can be read on mobile.

### 6-10 second bumper

- one mechanic, one emotion, one CTA. Do not try to explain the whole game.

## Beat map artifact

Before editing, create a beat map. Example fields:

```text
Beat ID:
Time range:
Purpose:
Viewer question answered:
Shot IDs / asset IDs:
Audio moment:
On-screen copy:
Gameplay truth note:
CTA or metadata:
Review owner:
Risk:
```

Every beat should answer one viewer question: "What is it?", "What do I do?", "Why is it exciting?", "What is new?", "Can I play it with friends?", "When and where can I get it?"

## Music, SFX, VO, and title cards

Audio is often the emotional spine of the trailer. Plan it early.

- Music: choose licensed or generated music with documented rights. Confirm territory, platform, paid-ad, store-page, broadcast/event, and perpetual/term limits. Avoid temp tracks surviving into final.
- SFX: use real game SFX where possible for truth and brand identity. Add sweeteners only when they do not imply absent mechanics or impacts.
- VO: use VO when it clarifies premise, character, or CTA. Do not let VO explain what the edit fails to show. Confirm voice rights, union/contract restrictions, synthetic voice consent, and localization plan.
- Title cards: make them short, readable, and backed by footage. One claim per card. Avoid stacked adjectives with no proof.
- Captions/subtitles: provide accurate captions for speech and meaningful non-speech audio; do not rely solely on auto-captions for final deliverables.
- Mix: prioritize intelligibility over loudness. Check trailer on phone speakers, headphones, TV, and muted autoplay.

On-screen copy should be evergreen unless the campaign requires urgency. "Wishlist now" and "Coming 2027" age better than "This spring" when store review or localization may slip.

## Generated b-roll boundaries

Generated video/images can help with mood, lore, abstract transitions, concept art-style cards, and social hooks, but it is risky in game trailers because viewers expect footage to represent the playable product.

Use generated b-roll only when all are true:

- the shot is not used as proof of a playable feature, level, character, UI, item, enemy, platform performance, or final art;
- the shot is visually separated, labeled, or contextually obvious as cinematic/conceptual when it could be confused with gameplay;
- the publisher owns or has rights to all inputs and outputs required for marketing use;
- the generation does not imitate a living actor, recognizable creator, competitor IP, platform UI, rating logo, real person, or protected brand without permission;
- the shot has provenance metadata in the truth ledger.

Prefer engine capture over generated substitutes when the brief promises gameplay, store-page conversion, platform featuring, or release-date credibility.

## Claims, ratings, and legal escalation

Documented facts:

- FTC business guidance says advertising claims must be truthful, not deceptive or unfair, and evidence-based; objective claims need a reasonable basis before use. See sources dated 2026-07-11.
- FTC endorsement guidance says endorsements must be honest, not misleading, and material connections should be clearly disclosed when they would affect credibility.
- IARC provides a streamlined age rating system for digitally delivered games/apps and may be usable across participating storefronts; for non-participating storefronts or legally required regions, use that store or country process.
- Storefront and platform rules are volatile. Re-check them at production/export time.

Escalate for approval before final if the trailer includes:

- rating-sensitive material: gore, sexual content, substances, gambling, loot boxes, strong language, horror, user interaction, in-game purchases, or online communication;
- claims: review quotes, awards, "exclusive," "best," "first," "most," "4K," "120 FPS," "crossplay," "offline," "free," "no ads," "no microtransactions," accessibility claims, anti-cheat claims, AI claims;
- legal/rights: licensed music, celebrities, influencers, streamers, UGC, fan art, mods, screenshots from another game, platform glyphs, trademarks, real brands, real locations, privacy-sensitive capture, synthetic people/voices;
- monetization: preorder bonuses, editions, subscriptions, in-app purchases, platform entitlements, regional pricing, discount windows, refund implications;
- rating badges/descriptors or platform mnemonics/end slates.

Do not invent rating badges or descriptors. Use official rating artwork and wording supplied by the rating/platform owner.

## Accessibility and safety QA

Use accessibility as a production requirement, not a late compliance pass.

- Captions: provide synchronized captions for dialogue and meaningful sound cues. W3C WCAG 2.2 SC 1.2.2 says prerecorded synchronized media with audio should have captions; captions include dialogue, speaker identification, and meaningful non-speech audio.
- Caption readability: follow game-caption practices such as no more than two lines where possible, avoid long lines, use mixed case, readable sans-serif options, sufficient contrast/background, and keep captions away from important UI.
- Flashing risk: check rapid cuts, explosions, lightning, muzzle flashes, glitch effects, white frames, red flashes, and strobing UI. WCAG 2.2 SC 2.3.1 uses a "no more than three flashes in any one-second period or below threshold" rule; when in doubt, reduce flashes, lower intensity, shorten area, or run a flash-analysis tool.
- Motion sickness: avoid unnecessary camera shake, whip pans, high-frequency zooms, rolling shutter simulation, and fast oscillation in social cutdowns.
- Mute comprehension: ensure the first 5-10 seconds work without audio through visuals, captions, or title cards.
- Color/contrast: check captions, UI callouts, and CTA text against bright gameplay backgrounds.
- Localization: leave expansion room for longer translated text; avoid baked-in English when localized deliverables are required unless producing per-locale renders.

## Localization and regionalization

Plan localization before locking the edit:

- decide which assets are textless masters, texted masters, caption files, dubbed VO, subtitled VO, platform-store exports, and social cutdowns;
- export clean M&E audio (music and effects without VO) when dubbing may happen;
- keep title cards editable and avoid text embedded in generated imagery;
- maintain glossary for character names, mechanics, abilities, CTA, edition names, and rating/disclaimer wording;
- verify release date/time, platforms, price, subscriptions, and rating badges per territory;
- check that screenshots/trailers do not show language-specific UI if the store listing is localized to another language;
- avoid idioms and jokes that require visual timing unless the localization team can adapt the edit.

## Platform and store constraints to re-check

Treat this table as a dated planning aid, not a permanent spec sheet. Re-check the official platform/store documentation immediately before final export and upload.

| Destination | Dated facts verified 2026-07-11 | Production implication |
|---|---|---|
| Apple App Store app previews | Up to 3 previews per language; up to 30s; must demonstrate features/functionality/UI using footage captured on device; Apple guidance says show more gameplay than cutscenes so users are not misled; specs list 15-30s, max 500 MB, H.264 or ProRes 422 HQ, max 30 fps, stereo audio. | For iOS/tvOS/macOS game previews, stay inside the app/game, use device-appropriate captures, disclose purchases/subscriptions/login when shown, keep copy legible with muted autoplay. |
| Google Play preview assets | Preview video appears before screenshots on the store listing and may autoplay muted up to 30s depending on device/settings/network; game screenshots should depict in-game experience and use captured footage/images of the game itself. | Put actual gameplay early; design feature graphic/poster with play button in mind; do not lead with misleading cinematics. |
| Xbox/Microsoft Store | Partner Center trailer requirements list 1920x1080 video, MOV/MP4, up to 15 trailers, duration under 30 minutes, 1920x1080 PNG thumbnail, trailer file under 10 GB, closed captions as WebVTT under 50 MB, audio description MP3 under 500 MB, intro/end mnemonic rules with short-trailer exceptions, and restrictions on platform branding/glyphs and rating-inappropriate elements. | Prepare caption and AD files; do not include competing platform references/glyphs; confirm mnemonics, any short-trailer exceptions, and rating treatment with the Xbox/store owner. |
| Steam | Steamworks docs define store graphical asset dimensions/rules and require accurate capsule dimensions; base capsule artwork is limited to game artwork, game name, official subtitle, with no review scores, awards, discount copy, other product promotion, or miscellaneous text; all capsules must be PG-13 appropriate. | Re-check Steamworks trailer upload/player rules in partner docs; avoid unapproved award/review/discount copy in capsules and store art. |
| Epic Games Store | Epic provides storefront media and content requirements for product review, but current requirements are store-policy controlled and may not render publicly in all contexts. | Use Epic's current developer docs/portal checklist at upload time; do not rely on memory for dimensions, codecs, ratings, or content restrictions. |
| YouTube | Recommended upload settings include MP4, H.264 video, progressive scan, AAC-LC/Opus/Eclipsa audio with 48 kHz sample rate; YouTube also requires disclosure for realistic AI-generated or altered content during upload. | Export high-quality progressive masters; complete synthetic-content disclosure when realistic AI-altered/generated material is present; provide captions manually where possible. |
| Social ads/platforms | Specs, safe zones, AI labels, and ad policies change frequently. | Build modular masters for 16:9, 9:16, 1:1, captions, safe zones, and platform-specific disclosures; re-check each ad account/platform before trafficking. |

## Review cycle

Use a staged review to avoid expensive rework.

1. Brief lock: objective, audience, destinations, trailer type, duration, truth boundaries, CTA, review owners.
2. Beat map review: structure, feature priority, claim list, capture needs, generated-shot boundaries.
3. Capture review: raw selects with shot log and truth ledger; reject shots that misrepresent or are visually broken.
4. Rough cut: pacing, comprehension, genre clarity, gameplay proof, audio direction. No final polish yet.
5. Fine cut: copy, CTA, music/SFX, VO, title cards, captions, platform safe areas.
6. Compliance review: claims, ratings, platform/store rules, rights/provenance, accessibility, localization, flashing risk.
7. Export QA: technical specs, file naming, duration, codec, loudness/intelligibility, captions/AD files, poster frames, per-locale/per-ratio versions.
8. Upload verification: check the actual store/social preview after upload; platform transcodes can change readability and audio sync.

Keep a decision log: what changed, who approved, when, and what was superseded.

## Game-trailer QA checklist

Before delivery, answer yes/no with evidence:

- Does the first 5 seconds communicate genre, tone, or a compelling hook?
- Can a viewer explain what the player does after one watch?
- Are gameplay, cinematic, generated, and UI/HUD shots distinguishable when needed?
- Does every feature/performance/availability claim have evidence and owner approval?
- Are any unimplemented, prototype, debug, manipulated, or target-render elements labeled or removed?
- Are rating-sensitive elements acceptable for the game's rating, audience targeting, and destination?
- Are platform logos, mnemonics, controller glyphs, end slates, and rating marks approved for the specific export?
- Are music, VO, SFX, fonts, footage, and generated assets cleared for all uses and territories?
- Are captions accurate, readable, synchronized, and delivered in the required format?
- Has flashing/strobing been checked and mitigated?
- Are localized versions text-safe, glossary-consistent, and regionally accurate?
- Are store specs re-checked and dated?
- Does the CTA match the actual page status: wishlist, demo, preorder, buy, play now, update available?
- Does the trailer still work muted and on a phone?
- Has the uploaded/transcoded version been reviewed, not just the local master?

## Complete example: gameplay store trailer

Example brief: "Make a 30-second Steam and YouTube gameplay trailer for a cozy automation game launching next quarter."

Approach:

```text
Primary promise:
Build a tiny forest factory where cute machines turn wild resources into whimsical inventions.

Truth boundary:
Only captured gameplay from build 0.9.14. No generated gameplay. Debug camera allowed only for one labeled beauty shot if direct gameplay cannot show factory scale.

Beat map:
0-3s: Hook - one machine chain transforms acorns into lanterns; HUD visible enough to show this is gameplay.
3-8s: Player verb - gather, place, connect conveyor, watch output.
8-14s: System depth - upgrade panel, recipe unlock, energy constraint.
14-21s: Variety - second biome and night lighting; show one character interaction.
21-26s: Hero payoff - full factory lights up the forest village.
26-30s: Title + Wishlist on Steam + Coming Q3 2027 + platform/store logo if approved.

Capture list:
G01 direct gameplay gather/place, HUD on, 1440p60, build 0.9.14.
G02 recipe UI, English and textless if possible.
G03 factory chain wide, HUD off and HUD on variants.
G04 village lights hero moment, direct gameplay camera.
G05 optional beauty flyover from debug camera, mark as "in-engine cinematic" if used.

Audio:
Use licensed cozy marimba bed; use in-game machine clicks; no VO. Captions for title cards and meaningful SFX if hosted with captions.

QA risks:
Release quarter must be confirmed before final. Steam capsule assets cannot include review/discount copy. Re-check Steam trailer export guidance at upload.
```

Why it works: the trailer opens with the game's loop, proves player interaction, saves the biggest factory payoff for the end, and avoids implying features beyond the captured build.

## Complete example: generated/engine hybrid announcement trailer

Example brief: "Create a 60-second announcement teaser for a dark sci-fi tactics game; gameplay is early but the world and faction art are approved."

Approach:

```text
Truth boundary:
Generated shots may establish mood, propaganda imagery, and abstract battlefield silhouettes.
Generated shots may not show UI, abilities, characters, enemies, maps, or tactical outcomes as if they are playable.
All actual mechanics must come from engine capture or title cards phrased as premise, not feature claims.

Structure:
0-5s: Engine-captured tactical grid silhouette, no UI claim yet.
5-16s: Generated propaganda montage: colony sirens, evacuation posters, orbital shadows. Label not needed if clearly non-gameplay stylized, but record provenance.
16-28s: Engine capture: unit movement, cover, overwatch arc, enemy reveal. HUD on.
28-40s: Title-card claims backed by capture: "Plan every move." "Exploit the dark." Avoid "revolutionary AI enemies" unless substantiated.
40-52s: Hero engine moment: chain reaction, squad extraction, loss/stakes.
52-60s: Title, "Wishlist now", platforms approved for announcement, rating pending if permitted by publisher/platform.

Review gates:
Game director approves generated lore imagery.
Marketing approves whether "rating pending" or no rating line is used.
Legal approves AI provenance and music license.
Platform owner approves store metadata.
```

Why it works: generated material supports mood without replacing gameplay proof. The edit is honest about early development while still giving viewers playable evidence.

## Sources consulted and evidence notes

Consequential factual claims above were checked on 2026-07-11. Re-check volatile store/platform specs at production time.

- Apple App Store App Previews and App Preview Specifications: https://developer.apple.com/app-store/app-previews/ and https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications/
- Google Play preview assets: https://support.google.com/googleplay/android-developer/answer/9866151
- Microsoft/Xbox Store listing trailer requirements and Xbox Accessibility Guidelines: https://learn.microsoft.com/en-us/gaming/game-publishing/concepts/store-listing and https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/104
- Steamworks graphical asset overview/rules: https://partner.steamgames.com/doc/store/assets and https://partner.steamgames.com/doc/store/assets/rules
- Epic Games Store storefront media/content documentation: https://dev.epicgames.com/docs/epic-games-store/sales-and-marketing/marketing/storefront-media-guide and https://dev.epicgames.com/docs/epic-games-store/requirements-guidelines/content-ratings/content-guidelines
- YouTube recommended upload encoding settings and GenAI disclosure: https://support.google.com/youtube/answer/1722171 and https://support.google.com/youtube/answer/14328491
- FTC advertising, substantiation, and endorsement guidance: https://www.ftc.gov/business-guidance/advertising-marketing, https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation, and https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- IARC FAQ and overview: https://www.globalratings.com/ and https://globalratings.com/faq/
- W3C WCAG 2.2 captions and flashing guidance: https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html and https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- U.S. Copyright Office copyright and AI materials: https://www.copyright.gov/what-is-copyright/ and https://www.copyright.gov/ai/
