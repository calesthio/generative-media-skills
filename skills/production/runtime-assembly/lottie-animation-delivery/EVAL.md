# Lottie animation delivery evaluation

Keep this answer key hidden from the evaluated agent. Test with the published package only.

## Scoring

Total: 100. A score of 85+ with no critical failure is production-ready; 70-84 requires focused revision; 50-69 requires major revision; below 50 fails. Any critical failure caps the score at 49.

## Knowledge questions

### 1. Fit assessment, 7 points

**Question:** When should a production avoid Lottie?

**Expected points:** live action/video/image sequence; embedded audio contract; unsupported AE effects/3D; exact offline rendering over runtime control; shader/simulation needs; simpler mechanism available. Award up to 7 for reasoned boundaries.

### 2. Glyphs versus runtime text, 10 points

**Question:** Compare the two text strategies.

**Expected:** glyphs preserve fixed visual outlines and avoid font loading but enlarge vector data, remove easy editing/localization, and need semantic host text; runtime text enables dynamic/localized copy but requires licensed fonts, preload, shaping/glyph/line-break tests, and player support.

**Critical failure:** says outlined glyphs remain normal accessible text automatically.

### 3. Player compatibility, 8 points

**Question:** Why is a generic renderer feature table insufficient for approval?

**Expected:** support differs by player, renderer, platform, and version; features interact. Build minimal fixtures, pin versions, compare reference frames, and record a compatibility matrix/fallbacks.

### 4. dotLottie, 8 points

**Question:** What does dotLottie v2 require, and what compatibility caveat applies?

**Expected:** Deflate ZIP `.lottie`; root manifest plus at least one animation in `a/`; optional images/fonts/themes/state machines. V2 is recommended for new work by its docs, while v1 is more widely supported, so test target players before using v2 features.

### 5. Deterministic capture, 10 points

**Question:** Describe frame-safe lottie-web capture.

**Expected:** freeze data/assets/player; disable autoplay/loop; await data/DOM/images/fonts; explicitly choose subframe behavior; seek with frame-based `goToAndStop`; test frame zero, boundaries, backward/out-of-order and repeated frames; sync audio in host.

**Critical failure:** records real-time autoplay and assumes frame accuracy.

## Production decisions

### 6. Matte failure, 8 points

**Scenario:** A matte works in exporter preview but fails in one mobile target.

**Expected:** treat target as authority; isolate fixture; verify version/renderer; simplify or convert construction, use a supported renderer, pre-render the element, or change format. Update matrix and compare frames.

### 7. Localization failure, 8 points

**Scenario:** Arabic copy renders with wrong shaping and clipping.

**Expected:** stop release; verify runtime-text/player shaping and font coverage/load order; test direction/wrap/line metrics with native review. Use locale-specific glyph export plus semantic host text if runtime support cannot pass.

**Critical failure:** fixes only by shrinking text until it fits.

### 8. Reduced motion, 7 points

**Scenario:** An autoplay loop is decorative and uses large scaling movement.

**Expected:** detect preference in host; disable autoplay or use a calm segment/static poster; preserve meaning; provide controls where required; test flashing while looping.

## Applied tasks

### 9. Multi-target handoff plan, 16 points

**Request:** Plan delivery of a branded onboarding animation to web, iOS, and Android with localized text and one image.

**Required:** target/version matrix and fixtures (3); text/font/localization strategy (3); image/offline custody (2); markers/state behavior (2); JSON/dotLottie version choice (2); accessibility/reduced motion (2); validation/provenance/handoff (2).

**Critical failures:** assumes identical players, omits font rights/load testing, or uses remote mutable assets for offline delivery.

### 10. Video-overlay capture plan, 14 points

**Request:** Render an eight-second transparent Lottie overlay into a 30 fps video with exact narration sync.

**Required:** frozen assets/player (2); readiness events/fonts (2); autoplay off and frame seeking (3); fps/subframe mapping (2); alpha/background test (1); repeated/backward boundary frames (2); host audio sync and teardown (2).

### 11. Broken package diagnosis, 12 points

**Request:** Diagnose a `.lottie` archive with a v2 manifest naming `hero`, file `a/Hero.json`, missing font, and a target that supports only v1.

**Expected:** catch ID/file case mismatch or mapping problem, missing font asset/reference, and unsupported package version/features. Choose compatible v1/raw JSON or update target; validate archive and preserve source. Award 3 per diagnosis/repair and 3 for retest plan.

### 12. Rights review, 7 points

**Request:** A marketplace Lottie file is downloadable and lottie-web is MIT. Can it be used in a paid campaign?

**Expected:** lottie-web's MIT license does not license the downloaded animation, fonts, images, logos, or characters. Verify marketplace/creator terms and asset provenance; do not publish until cleared.

**Critical failure:** equates runtime license with content rights.

## Critical-failure summary

- unsupported feature materially changes the approved animation;
- wrong copy/font/locale ships;
- wall-clock capture used where exact frame sync is required;
- required reduced-motion or flashing safeguards omitted;
- package/player version incompatibility ignored;
- content rights inferred from lottie-web's MIT license.

## Evaluation integrity

Do not expose this file. Accept alternate players and packaging tools when the response verifies their exact versions, feature support, lifecycle, accessibility, deterministic behavior, and rights.