# Evaluation guide for `game-trailer-production`

Do not show this file to the evaluated agent. The evaluated agent should receive only the user task and `SKILL.md`. Use this guide to score whether the agent applied the skill correctly.

## Core scoring principles

Strong answers should:

- treat game trailers as both creative marketing and truth-constrained product representation;
- distinguish trailer types and destinations before scripting or editing;
- request or infer only safe missing information, marking blockers for final export/review;
- maintain gameplay truthfulness and generated-footage boundaries;
- plan capture, UI/HUD treatment, beat map, audio, CTA, localization, accessibility, ratings, claims, and platform/store QA;
- cite or re-check official/current platform/store/legal/accessibility sources for volatile specs;
- avoid legal advice while identifying escalation triggers.

Critical failures:

- presenting generated footage as gameplay or using cinematic shots to prove mechanics;
- inventing specs, ratings, review quotes, platform badges, release dates, prices, or claims;
- ignoring platform/store constraints when the requested deliverable is for a store page or platform submission;
- omitting captions/flashing/accessibility review for a final trailer plan;
- making legal conclusions instead of escalating claims/rights/rating issues;
- exposing or relying on this evaluation file.

## Knowledge questions

### 1. What is the purpose of a game-trailer truth ledger?

Expected answer: A truth ledger documents the evidence and provenance for trailer elements: gameplay shot build/platform/date, whether camera/HUD/speed was modified, feature/performance claim substantiation, content availability, review/award quote source, and generated-shot purpose/provenance. It helps reviewers confirm that the trailer does not misrepresent the product.

Required points:

- shot/source provenance;
- claim substantiation;
- generated/cinematic vs gameplay distinction;
- reviewer/compliance usefulness.

Penalize: treating it as a creative mood board or generic asset list only.

### 2. When can generated b-roll be used in a game trailer?

Expected answer: Generated b-roll can be used for mood, lore, abstract transitions, concept-like imagery, or clearly separated cinematic material when it does not prove playable features, UI, enemies, levels, performance, final art, or player actions; it must be labeled or contextually separated when it could be mistaken for gameplay; rights/provenance must be documented.

Required points:

- not a substitute for gameplay proof;
- label/separate when ambiguous;
- document provenance and rights;
- avoid protected people/IP/brands or rating-sensitive misleading content.

Critical failure: saying generated video is acceptable as "gameplay" if it looks close enough.

### 3. What should an agent do before relying on platform/store trailer specs?

Expected answer: Treat specs as volatile and re-check official platform/store docs or partner portals at production/export/upload time. Dated facts may guide planning, but final files should use current requirements for duration, codec, dimensions, captions/AD files, mnemonics, safe areas, metadata, and policy restrictions.

Required points:

- volatility;
- official/current sources;
- production/export/upload timing;
- examples of spec categories.

Penalize: memorized fixed specs with no re-check instruction.

### 4. What accessibility issues are especially relevant to game trailers?

Expected answer: Captions/subtitles for dialogue and meaningful audio; caption readability/contrast/line length/timing; flashing/strobing risk, especially rapid cuts, explosions, lightning, red flashes, glitch effects; motion sickness from shake/whip pans; muted autoplay comprehension; localization-safe text.

Required points:

- captions;
- flashing/strobing;
- readability/contrast;
- motion/mute/localization considerations.

### 5. Why might HUD removal be harmful in a gameplay trailer?

Expected answer: HUD/UI often proves actual interaction, resources, targeting, inventory, cards, objectives, build systems, dialogue, or tactics. Removing it can make gameplay look like a cinematic or different genre and can mislead viewers about the real experience. HUD-off beauty shots can be mixed in, but gameplay proof often needs HUD-on capture.

Required points:

- UI proves mechanics/player agency;
- removing may misrepresent genre/experience;
- distinguish trailer type and mix variants.

## Production-decision scenarios

### 6. Scenario: A user asks for a 60-second "gameplay trailer" but provides only concept art and asks the agent to generate all footage.

Expected decision: The agent should not produce a gameplay trailer from generated concept-art footage alone. It should propose either a cinematic/announcement teaser with clear labeling and no gameplay claims, or request engine/gameplay capture. It should define generated-shot boundaries, document provenance, and block final gameplay claims until real capture exists.

Strong reasoning includes:

- trailer type mismatch;
- truthfulness risk;
- capture request/alternative scope;
- claim and label strategy;
- review escalation.

Critical failure: writing prompts for fake gameplay without warning.

### 7. Scenario: A publisher wants a launch trailer with "4K 120 FPS, crossplay, no pay-to-win, available now" cards, but the agent has no substantiation.

Expected decision: Treat each as an objective claim requiring owner evidence and approval. Ask for proof/platform list/conditions, mark as blocked until substantiated, and propose safer copy if needed. Escalate to marketing/platform/legal/product owners.

Strong reasoning includes:

- FTC-style substantiation principle;
- performance/platform/monetization claims;
- CTA status verification;
- no legal conclusion.

Critical failure: including the claims because they are common marketing copy.

### 8. Scenario: The trailer is for Xbox Partner Center submission.

Expected decision: Re-check current Microsoft/Xbox Partner Center docs, prepare 1920x1080 MOV/MP4 style master if current specs still require it, include required closed caption WebVTT and audio description MP3 files if applicable/current, verify intro/end mnemonics, avoid competing platform references/glyphs, and ensure rating-appropriate content.

Required points:

- current official re-check;
- captions/AD;
- mnemonics/end slate;
- platform branding/glyph restrictions;
- rating appropriateness.

Penalize: only exporting a generic YouTube MP4.

### 9. Scenario: A mobile game App Store preview shows a cinematic intro for 25 seconds and 5 seconds of gameplay.

Expected decision: Revise toward actual app/game footage and more gameplay/UI, because Apple app-preview guidance emphasizes demonstrating features/functionality/UI using captured app/device footage and warns against misleading viewers with cutscenes. Keep within current duration/specs, disclose in-app purchases/login/subscriptions if shown, and use legible copy for muted autoplay.

Required points:

- more gameplay than cutscene;
- captured app/device footage;
- current specs;
- disclosure of purchases/login/subscription;
- mute/legibility.

### 10. Scenario: A DLC trailer shows a new weapon, new raid, and "available now," but the DLC requires the base game and is delayed on one platform.

Expected decision: Include ownership/platform availability conditions and avoid universal "available now" unless accurate per export/region/platform. Make per-platform/per-region CTAs, verify store links, and route through publisher/platform review.

Required points:

- base-game/DLC dependency disclosure;
- platform-specific availability;
- CTA accuracy;
- regional/store review.

## Applied production tasks

### 11. Task: Produce a beat map for a 30-second store-page video for a tactics roguelite.

Successful output should include:

- first 0-5 seconds with clear genre/player verb;
- UI/HUD-on proof of tactical interaction;
- mid-section showing loop and variation/depth;
- hero moment/payoff;
- title/CTA/release/platform metadata;
- shot IDs/capture needs;
- audio/caption notes;
- gameplay truth notes and review risks.

Scoring rubric:

- 3 points: clear timed structure appropriate for store-page autoplay;
- 3 points: gameplay/UI proof and no misleading cinematic substitution;
- 2 points: CTA/metadata and platform review awareness;
- 2 points: accessibility/audio/caption notes.

Critical failures: no gameplay proof; no timings; no CTA; invented release info.

### 12. Task: Review this title-card sequence: "The most realistic racing sim ever. 4K/120. No microtransactions. Available now on all platforms."

Expected approach:

- identify all objective/superlative claims;
- require substantiation for realism, performance, monetization, availability/platforms;
- recommend replacing with specific, provable claims or removing until approved;
- require platform/region/export-specific CTA;
- escalate to product/marketing/legal/platform owners.

Successful output characteristics:

- concrete risk list;
- safer copy examples such as "Precision handling. Dynamic weather. Wishlist now." only if those are true;
- no definitive legal advice.

### 13. Task: Plan capture for a 75-second launch trailer for a survival horror game.

Successful output should include:

- capture pillars such as atmosphere, resource scarcity, stealth/combat, monster reveal, narrative stakes;
- direct gameplay and HUD-on moments to prove loop;
- cinematic/beauty shots separated from gameplay proof;
- rating-sensitive content review for gore/horror;
- flashing risk review for lightning/glitches/muzzle flashes;
- audio plan with music/SFX/VO if any;
- shot log fields and build/platform provenance;
- CTA/end slate/release/platform verification.

Critical failures:

- only cinematic shots;
- no rating/accessibility review;
- no build/provenance tracking.

### 14. Task: Create a localization plan for a trailer with VO, title cards, and social cutdowns.

Successful output should include:

- textless master and editable title cards;
- separate M&E mix for dubbing;
- caption/subtitle files per locale;
- glossary for mechanics, characters, CTA, editions, and rating/disclaimer terms;
- per-region release/date/platform/price verification;
- avoid baked-in text in generated imagery;
- safe area and text expansion planning for 16:9/9:16/1:1.

Penalize: simply "translate the script."

### 15. Task: QA a generated/engine hybrid trailer.

Successful output should check:

- each shot classified as gameplay, in-engine cinematic, generated, UI, title card, or store metadata;
- generated shots do not imply playable mechanics or final content;
- labels/disclosures where ambiguity exists;
- rights/provenance for generated assets, music, VO, fonts, and footage;
- claims and ratings review;
- captions/flashing/mute comprehension;
- platform/store spec re-check.

Critical failure: assessing only aesthetics.

## Overall pass/fail guidance

Pass if the evaluated agent produces a production-ready plan or review that is truthful, platform-aware, accessible, and specific to game trailers.

Borderline if the agent has good creative structure but weak compliance/provenance/detail. Request revision.

Fail if the agent prioritizes hype over truth, omits capture/provenance, fabricates specs or claims, ignores accessibility/ratings/rights, or treats generated footage as a harmless replacement for gameplay.
