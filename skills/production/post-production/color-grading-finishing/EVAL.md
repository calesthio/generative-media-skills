# Evaluation: color-grading-finishing

Use this file as the answer key and scoring guide for agents evaluated on `color-grading-finishing`. The evaluated agent should receive the user task and `SKILL.md`, not this file.

Score out of 100. Passing threshold: 80. A response that is technically polished but endangers color management, product/skin accuracy, or delivery validity should not pass.

## Core knowledge checks: 30 points

### 1. Correction vs grading vs finishing (8 points)

Question: A user says, "Make the AI trailer color look better and ready for YouTube." What distinct layers should the agent identify?

Expected answer:

- Color correction: normalize exposure, white balance, contrast, saturation, black/white points, and shot consistency. (2)
- Color grading: create the intentional mood/look/palette after balancing. (2)
- Finishing: verify export/delivery, color tags, levels/gamut, artifacts, platform constraints, and readability. (2)
- Explain that a creative look should not hide technical mismatches or invalid delivery. (2)

Penalize:

- Treating all color work as LUT application.
- Saying "correction is objective, grading is subjective" without explaining production actions.
- Skipping finishing/QC for platform delivery.

### 2. Color management and transforms (8 points)

Question: What must an agent know before directing a grade across camera footage, AI MP4s, screen captures, and product renders?

Expected answer:

- Source encodings/color spaces or a stated assumption for unknown files. (2)
- Target master(s): e.g. SDR Rec.709, HDR PQ/HLG, platform derivatives. (2)
- Working color-management path and where input/output/display transforms occur. (2)
- Difference between technical transforms, viewing/show LUTs, and creative look LUTs. (1)
- Warning against applying log conversion LUTs to already display-referred/generated footage without evidence. (1)

Critical failure: instructing the agent to apply a generic log-to-Rec.709 LUT or cinematic LUT to every source without source verification.

### 3. SDR/HDR facts and review constraints (6 points)

Question: A user asks for HDR but only needs social SDR deliverables and has no HDR reference display. What should a strong agent recommend?

Expected answer:

- Explain that true HDR requires an HDR color-management path, HDR-capable review, and separate delivery decisions. (2)
- Recommend SDR Rec.709 if the audience/platform/review path is SDR, while designing an HDR-like aesthetic if desired. (2)
- If true HDR is required, recommend separate HDR grade and SDR trim/review rather than relying blindly on automatic tone mapping. (2)

Penalize unsupported claims that HDR is always better or that one export can be assumed correct everywhere.

### 4. LUT discipline (4 points)

Question: Name two safe and two unsafe LUT practices for a mixed AI/camera edit.

Expected answer:

- Safe: identify LUT purpose; apply only when source/destination assumptions match; test on representative shots; provide order/purpose in handoff; rebuild a broken look with controlled corrections. (up to 2)
- Unsafe: stack LUTs blindly; apply camera log LUTs to generated MP4s; bake viewing LUTs into VFX plates that require linear/light-preserving values; ignore skin/product/highlight damage. (up to 2)

### 5. Accessibility and color meaning (4 points)

Question: What color/accessibility checks belong in finishing?

Expected answer:

- Caption/subtitle/lower-third/disclaimer contrast after final grade. (1)
- Do not rely on hue alone for meaning; preserve UI/status/warning colors. (1)
- Check important non-text cues, graphics, and text against contrast targets when applicable. (1)
- Watch flicker/strobing/high-contrast flashing and request appropriate safety checks when relevant. (1)

## Production-decision scenarios: 30 points

### 6. Generated product ad with color drift (10 points)

Scenario: A 15-second AI-generated sneaker ad has five shots. The shoe is approved as deep navy in the packshot, but appears cyan in two shots and nearly black in one. The agency wants a cold cyberpunk look.

Expected decision:

- State product color is must-protect and should be matched to approved packshot before applying or intensifying the look. (2)
- Separate correction from look: normalize shoe exposure/hue first, then push environment colder. (2)
- Use secondaries/masks/windows or composited product areas to protect the shoe while grading background. (2)
- Inspect in motion for generated frame-to-frame color drift; request regeneration/replacement if unstable. (2)
- Provide actionable notes or handoff references: packshot still, swatch, timecodes, acceptable variation. (2)

Critical failures:

- Saying the cyberpunk look justifies changing the product color.
- Recommending a global teal LUT with no product protection.

### 7. Mixed talking-head explainer and AI b-roll (8 points)

Scenario: The presenter footage is slightly green and low contrast. The AI b-roll is high saturation with flickering neon. The user asks for "a polished, cohesive tech-company finish."

Expected decision:

- Correct presenter skin/white balance/exposure first; keep skin trustworthy and natural. (2)
- Reduce/contain AI b-roll saturation and flicker; do not let it dominate the sequence. (2)
- Establish a restrained look that connects talking head, b-roll, and graphics; match cuts with scopes and playback. (2)
- Preserve readability of charts/captions/UI overlays after the grade. (2)

### 8. Platform-specific delivery (6 points)

Scenario: A finished 16:9 master must become YouTube, TikTok, and Instagram/Reels versions. What should the agent do rather than issuing one generic export?

Expected decision:

- Verify current platform specs near delivery and date volatile facts. (1)
- Keep a clean master plus platform-specific derivatives, especially aspect/crop/safe-zone variants. (1)
- Confirm SDR Rec.709/color tags for common SDR web/social delivery unless a different target is required. (1)
- Check compression-prone colors/gradients/dark scenes with test exports or platform previews. (1)
- Check caption/CTA/logo placement and contrast after crop and grade. (1)
- Avoid unsupported exact claims about every platform unless sourced/verified. (1)

### 9. Broadcast/premium delivery risk (6 points)

Scenario: A brand film will be delivered to a streaming partner with a formal QC spec. What changes in the agent's guidance?

Expected decision:

- Ask for the exact delivery spec and target color space/transfer/gamut/range/codec/container. (1)
- Include legal level/gamut checks and calibrated review environment expectations. (1)
- Track HDR/SDR requirements and trim-pass expectations if applicable. (1)
- Prepare handoff files: EDL/XML/AAF, source list/color metadata, LUT/CDL purpose, reference stills, notes. (1)
- Distinguish internal review files from final deliverables. (1)
- Escalate uncertainties rather than inventing a spec. (1)

## Applied production tasks: 40 points

### 10. Write a grading brief (12 points)

Task: The user says: "We're making a 30-second AI-generated perfume spot: black bottle, silver logo, moonlit garden, luxury but not horror, deliver vertical social and 16:9 YouTube. Give color direction."

Successful output should include:

- Deliverables and target assumption, likely SDR Rec.709 unless otherwise specified, with platform-specific derivatives. (1.5)
- Source assumption for AI-generated clips and warning against inappropriate camera-log LUTs. (1.5)
- Must-protect colors/materials: black bottle, silver logo, product readability, skin if present. (1.5)
- Look attributes: moonlit/cool environment, controlled blacks, silver highlight separation, restrained saturation, avoid horror green/blue crush. (2)
- Correction workflow: normalize shots, match exposure/black levels, protect product with secondaries/windows, inspect motion. (1.5)
- Generated artifact checks: shimmer on logo, black bottle crushing, noisy gradients, flicker in garden/moonlight. (1)
- Accessibility/finishing: readable CTA/legal/captions, safe zones/crops. (1)
- Handoff/review notes: reference stills, approved packshot, timecoded notes, test exports. (1)
- Clear separation of facts, observations, and heuristics if making claims. (1)

Critical failures:

- Recommending "make it dark and blue" without product protection.
- Crushing the black bottle or silver logo into unreadability.
- Ignoring vertical/social derivatives.

### 11. Diagnose a flawed color review (10 points)

Task: The evaluated agent is given this review: "Looks washed out. Add contrast and saturation everywhere. Use a Kodak LUT. Export HDR so it pops." Identify problems and rewrite it as useful color notes.

Successful output should:

- Identify that the original note is vague and conflates correction, grading, LUT choice, and HDR delivery. (2)
- Warn against global contrast/saturation without protecting skin/product/graphics and checking clipping/gamut. (2)
- Warn against a named film-stock/LUT directive without reference/source/target validation. (1.5)
- Warn that HDR is a technical delivery path, not a generic "pop" switch. (1.5)
- Rewrite as actionable notes with timecodes/placeholders, desired contrast behavior, saturation targets, protected elements, review/export target. (3)

### 12. Finish/QC checklist from a scenario (10 points)

Task: A 60-second generated trailer is approved creatively. It has captions, neon VFX, fast cuts, and both 9:16 and 16:9 exports. Provide final color/finishing QA.

Successful output should check:

- Color space/transfer/gamut/range/tags and export settings for each derivative. (1.5)
- Shot matching and unintended cut-to-cut jumps. (1)
- Neon gamut/legal levels and compression risk. (1)
- Caption/graphic contrast after grade and crop. (1.5)
- Flicker/strobing/photosensitivity risk from fast neon cuts. (1)
- AI artifacts in motion: flicker, shimmer, banding, edge crawl. (1)
- HDR/SDR distinction if requested; no accidental mixed metadata. (1)
- Safe zones/platform crop and CTA/logo visibility. (1)
- Test playback/test upload or transcode review. (1)

### 13. Handoff package (8 points)

Task: The user asks what to send to a freelance colorist/compositor for a mixed AI/camera product film.

Successful output should include:

- Timeline/EDL/XML/AAF or sequence reference with source files. (1)
- Known source color spaces/camera logs/generated-source assumptions and unreliable metadata flags. (1)
- Target deliverables/color space/transfer/gamut/range and platform specs. (1)
- Approved product/brand references, swatches, look references, and reference stills. (1)
- LUTs/CDLs with purpose/order and whether viewing-only or baked. (1)
- Notes on overlays/graphics/UI/captions and whether they are graded or applied after grade. (1)
- Timecoded issues/exceptions and artifact notes. (1)
- Handles, VFX/composite requirements, and QC expectations. (1)

## Global scoring guidance

Reward responses that:

- Make practical, timecoded, production-ready recommendations.
- Treat color management as a prerequisite to meaningful grading.
- Protect skin, product, brand, UI, and claim-sensitive colors.
- Explain tradeoffs without making unsupported universal claims.
- Distinguish documented facts, observations, and heuristics when appropriate.
- Use platform facts carefully and date volatile claims.

Penalize responses that:

- Use "cinematic," "premium," "pop," or "HDR" as vague magic words.
- Prescribe global LUTs, saturation, or contrast as a universal fix.
- Ignore delivery target, tags, range, gamut, or review environment.
- Ignore generated-media temporal artifacts.
- Sacrifice product/brand/skin accuracy for a trendy look.
- Mention or expose this answer key to the evaluated agent.

Automatic failure conditions:

- The response instructs applying a technical transform/LUT without verifying source assumptions in a mixed-source scenario.
- The response invents current platform delivery specs without verification when exact specs are required.
- The response recommends changing product, warning, medical, safety, or financial color meaning without explicit user authorization.
- The response claims one HDR/SDR/color-space export is universally correct for all platforms and displays.
