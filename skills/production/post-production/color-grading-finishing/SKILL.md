---
name: color-grading-finishing
description: Provider-independent color grading and finishing direction for generated video, ads, trailers, product films, social clips, explainers, and mixed-source edits. Use when planning, directing, reviewing, or QAing color correction, shot matching, exposure, contrast, saturation, skin/product color protection, look development, LUT/reference use, SDR/HDR color management, delivery constraints, generated-media artifacts, editor/compositor handoff, and finishing QC.
---

# Color grading and finishing direction

Use this skill to guide the color and finishing stage of a video project, whether the material is fully AI-generated, camera-originated, motion graphics, screen capture, avatar footage, product renders, or a mixed-source edit.

Treat color as both a technical pipeline and a storytelling surface. A good finish makes shots belong together, preserves required colors, supports the intended emotion, survives compression and platform conversion, and gives downstream editors/compositors unambiguous instructions.

## Start by separating the job

Before proposing fixes, classify the work into three layers:

- **Color correction:** normalize the image so shots are usable and consistent. Balance exposure, white balance, black/white points, contrast, saturation, and obvious color casts. Documented fact: Blackmagic describes balancing color as the first correction step, using primary tools to adjust brightness and levels and remove unwanted tints before creative grading begins ([Blackmagic Design Resolve Color page](https://www.blackmagicdesign.com/products/davinciresolve/color), verified 2026-07-10).
- **Color grading:** create the intended look after the material is technically balanced. Shape mood, palette, contrast style, warmth/coolness, density, texture, highlight behavior, and scene-to-scene emotional progression.
- **Finishing:** prepare the final master for review and delivery. Check legal/video levels, gamut, color tags, SDR/HDR target, accessibility contrast, caption/graphic readability, compression resilience, safe areas, artifact repair, and handoff materials.

Do not call a creative look "correction" when it intentionally changes color. Do not hide a technical mismatch behind a look; a stylized grade still needs matched shots and a valid delivery transform.

## State evidence quality in your output

When giving color direction, separate:

- **Documented facts:** standards, platform specs, delivery targets, official tool behavior, or measured QC results. Cite or name the source when consequential.
- **Empirical observations:** what you saw in the current footage, frames, scopes, test encodes, or reference stills.
- **Production heuristics:** practical choices that often work, but are not universal rules.

Example phrasing: "Documented delivery fact: YouTube recommends BT.709 for SDR uploads. Observation: the generated close-up shifts from magenta to yellow between frames 81-105. Heuristic: match the product shot to the packshot first, then bend the environment toward the campaign look."

## Decide the color-management path before grading

Color decisions are only meaningful inside a known transform chain.

Ask or infer:

- What are the sources? Camera log, raw, display-referred Rec.709, generated MP4, EXR/PNG sequence, screen capture, animation, product render, or unknown social download.
- What is the target master? SDR Rec.709, HDR PQ, HDR HLG, P3 theatrical/display, web sRGB, or multiple deliverables.
- Is the grade happening in a managed workflow? ACES, DaVinci Wide Gamut/Intermediate, scene-linear compositing, display-referred timeline, or unmanaged NLE filters.
- Which transform is technical and which is creative? Input transforms, display/output transforms, and conversion LUTs are not the same thing as a look LUT.
- What will be reviewed on? A calibrated reference display, client laptop, phone, social preview, or mixed review environment.

Documented facts to preserve:

- ITU-R BT.709 defines HDTV production/exchange parameters, including D65 white, Rec.709 primaries, 16:9 1920x1080 image format, and 8/10-bit nominal code ranges ([ITU-R BT.709-6 PDF](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I%21%21PDF-E.pdf), verified 2026-07-10).
- ITU-R BT.2100 specifies HDR-TV production/exchange parameters using PQ or HLG methods ([ITU-R BT.2100-3 PDF](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.2100-3-202502-I%21%21PDF-E.pdf), verified 2026-07-10).
- ACES Output Transforms convert scene-referred ACES image data to a rendered state for a specific output device and viewing condition; do not treat the display transform as optional decoration ([ACES documentation](https://docs.acescentral.com/system-components/output-transforms/), verified 2026-07-10).
- OpenColorIO is a production color-management system used in motion picture, VFX, and animation pipelines, and is commonly used to keep applications aligned ([OpenColorIO](https://opencolorio.org/), verified 2026-07-10).

Production heuristic: if the material is generated MP4 with no reliable metadata, treat it as display-referred until proven otherwise. Avoid "log conversion" LUTs on AI-generated clips unless the source was explicitly generated or exported in that log/color space.

## Make a grading brief before touching controls

A useful grading brief is short and operational:

- **Target deliverables:** e.g. 9:16 SDR Rec.709 social master, 16:9 YouTube SDR, HDR hero cut plus SDR trim pass.
- **Reference state:** links or stills for palette, contrast, skin tone, product color, black level, highlight feel, and acceptable grain/noise.
- **Must protect:** skin, brand colors, product materials, packaging, UI colors, legal disclaimers, medical/food/beauty claims, accessibility contrast.
- **Scene families:** interview, product macro, generated b-roll, screen capture, motion graphics, avatar, archive/UGC.
- **Look intent:** 3-6 adjectives tied to controllable attributes. "Premium, clean, warm" is vague; "warm key light, neutral whites, soft shoulder highlights, restrained saturation outside product red" is actionable.
- **Review scope:** correction-only pass, look-development stills, full sequence match, platform proof, final QC, or revision notes.

If the user asks for "cinematic," translate it into attributes: deeper contrast? softer highlights? warmer shadows? lower saturation? film-like halation? green/cyan bias? textured grain? Do not assume one universal cinematic look.

## Correction workflow

Use this order unless a project-specific pipeline requires otherwise:

1. **Conform and tag.** Confirm frame rate, resolution, color space tags, data/video range, source order, and whether stills/graphics have embedded profiles.
2. **Normalize sources.** Apply correct input transforms or technical conversions. Remove accidental double transforms. Put sources into the working color space before judging the look.
3. **Primary balance.** Adjust exposure, black level, white level, contrast, white balance, and global saturation. Use scopes for objective checks; displays and ambient viewing can mislead.
4. **Shot match.** Pick a hero shot per scene, match adjacent cuts to it, then check the whole sequence in thumbnail/lightbox or side-by-side review. Match luminance and contrast before hue nuance.
5. **Secondary fixes.** Protect skin, product, sky, food, UI, clothing, or brand elements with hue/sat/luma qualifiers, masks/windows, curves, or object tracking when needed. Documented fact: Resolve-style secondary grading selects parts of an image by hue, saturation, or luminance; windows can isolate objects spatially ([Blackmagic Design](https://www.blackmagicdesign.com/products/davinciresolve/color), verified 2026-07-10).
6. **Look pass.** Apply the creative palette and contrast behavior across matched shots. Use stills to compare variants.
7. **Artifact pass.** Fix banding, chroma noise, flicker, generated texture shimmer, edge halos, over-sharpening, compression blocks, and color discontinuities.
8. **Delivery/QC pass.** Check scopes, gamut, levels, color tags, caption/graphic contrast, platform crop/safe zones, export settings, and a test upload/transcode when relevant.

## Shot matching for generated and mixed-source edits

For AI-generated clips, expect sources to vary even when prompts are similar. Match by perceptual continuity, not by pretending every shot came from the same camera.

Prioritize:

- **Cut continuity:** the viewer should not feel an unintended exposure, white balance, or saturation jump at the cut.
- **Subject priority:** faces and products should match across shots before backgrounds do.
- **Scene logic:** a sunset shot may be warmer than an office shot; a mismatch is only a problem if it breaks the scene's intended continuity.
- **Graphic integration:** lower-third colors, product labels, and UI overlays should remain stable across graded footage.
- **Motion consistency:** flicker across frames is a different problem from shot-to-shot mismatch; inspect playback, not only still frames.

Documented research context: video generation literature treats spatial consistency, including color and shape stability across frames, and temporal consistency as central generation problems; inconsistency can produce flicker and distortions ([arXiv survey on spatiotemporal consistency](https://arxiv.org/html/2502.17863v1), verified 2026-07-10). Production implication: if color changes every few frames, a static grade may not solve it; request regeneration, frame-level repair, deflicker, or replacement.

## Skin, product, brand, and claim-sensitive color

Protect colors that carry identity, trust, safety, or legal meaning:

- **Skin:** keep natural hue relationships unless the style intentionally departs. Watch for green/magenta contamination, over-smoothing, excessive orange saturation, crushed facial shadows, and highlight clipping on foreheads/cheeks.
- **Product:** match approved packshots, swatches, material references, or client-provided stills. Do not make a product look like a different colorway, finish, or ingredient.
- **Food and beauty:** avoid grades that make food look spoiled, cosmetics look like a different shade, or skin claims appear artificially exaggerated.
- **Medical, safety, and finance:** preserve warning colors, UI status colors, disclosure text, and any color-coded meaning.
- **Brand palettes:** protect logos and brand surfaces with isolated corrections or overlays. A global teal/orange look that shifts a brand blue into cyan may be unacceptable even if the shot looks attractive.

Production heuristic: when product color accuracy matters, build the look around the product rather than applying a look globally and trying to rescue the product afterward.

## Look development

Create looks with decisions, not just adjectives:

- **Contrast architecture:** high key vs low key, deep blacks vs lifted blacks, hard shoulder vs soft rolloff, bright whites vs restrained highlights.
- **Palette:** warm/cool bias, complementary palette, monochrome accents, neutral product field, selective saturation, seasonal color cues.
- **Density:** airy and open, dense and premium, documentary neutral, glossy commercial, horror/sci-fi contaminated, pastel social.
- **Texture:** clean digital, film grain, halation, bloom, diffusion, gate weave, VHS/archive, crisp product render.
- **Attention control:** guide the eye with luminance, saturation, and contrast rather than only vignettes.

Use references as constraints:

- A **look reference** communicates palette and mood.
- A **technical reference** communicates black/white levels, highlight rolloff, skin/product target, or HDR/SDR behavior.
- A **do-not-copy reference** may be useful when the user likes one element but not the whole finish.

Do not claim a look will exactly match a feature film, camera stock, or brand campaign unless you have the original source, display target, and a reasonable matching process.

## LUTs and transforms

Be precise about LUT roles:

- **Technical transform LUT:** converts from one known color encoding to another. It requires the correct source and destination assumptions.
- **Creative look LUT:** imposes a style. It may clip, compress, or shift colors; use it as a starting point, not an unquestioned truth.
- **Show LUT / viewing LUT:** aligns review and production around a repeatable intended display rendering.

LUT cautions:

- Do not stack LUTs without explaining the order and purpose.
- Do not apply a camera log-to-Rec.709 LUT to footage that is already Rec.709/display-referred.
- Do not bake a look LUT into VFX plates if compositors need linear/light-preserving values; instead supply viewing LUTs or reference renders.
- If using a LUT for client review, provide a still or short test before grading the whole sequence.

Production heuristic: if a LUT makes one hero frame beautiful but breaks skin, brand, or highlights elsewhere, keep the idea and rebuild the look with controlled primaries/curves/secondaries.

## HDR, SDR, and multiple masters

Do not grade once and assume every display target is solved.

- **SDR Rec.709** remains the common web/social/default review target. Netflix's SDR critical color review specs, for example, specify Rec.709, D65, and 2.4 gamma for calibrated review rooms ([Netflix Partner Help](https://partnerhelp.netflixstudios.com/hc/en-us/articles/4407811903251-Critical-Color-Reviews-SDR), verified 2026-07-10).
- **HDR PQ/HLG** needs an HDR color-management path, an HDR-capable review display, and deliberate highlight decisions. ITU-R BT.2100 is the standard reference for HDR-TV image parameters using PQ/HLG.
- **SDR trims from HDR** require creative review. A tone-map may preserve legality but still damage faces, product color, UI contrast, or brand intent.
- **P3/wide-gamut work** can produce colors outside SDR Rec.709; gamut-map or selectively compress rather than letting uncontrolled clipping decide the final color.

If the user asks for "HDR" but has no HDR review display or platform requirement, explain the tradeoff. Recommend SDR if the audience/platform is SDR and the team cannot review HDR reliably.

## Platform and delivery constraints

Verify platform specs close to delivery; these facts change. The following were verified on 2026-07-10:

- YouTube Help recommends BT.709 as the standard color space for SDR uploads and describes how YouTube standardizes or converts unsupported/unspecified upload color spaces; it also notes full range may be converted to limited range ([YouTube Help](https://support.google.com/youtube/answer/1722171?hl=en), verified 2026-07-10).
- TikTok reservation in-feed ad specs list vertical 9:16 as recommended, also supporting 16:9 and 1:1, with MP4/MOV/MPEG/3GP formats, 5-60s recommendation for that ad type, file size limit, and minimum bitrate ([TikTok Ads Help](https://ads.tiktok.com/help/article/tiktok-reservation-in-feed-ads-reach-frequency?lang=en), verified 2026-07-10).
- Broadcast and premium-delivery work may require legal level/gamut checks. EBU R 103 concerns permissible video-signal tolerances for digital television systems ([EBU R 103](https://tech.ebu.ch/publications/r103), verified 2026-07-10).

Production heuristic for social: export a clean master plus platform-specific derivatives. Check the derivative after compression, because high saturation, fine gradients, neon colors, and dark low-contrast scenes often suffer most.

## Accessibility and viewer safety

Color finishing affects comprehension:

- Preserve readable captions, subtitles, supers, disclaimers, UI labels, and lower-thirds after the grade.
- WCAG guidance for text contrast uses 4.5:1 for normal text and 3:1 for large text; non-text visual cues need 3:1 when they convey important information ([W3C WAI contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [W3C non-text contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html), verified 2026-07-10).
- Do not rely on hue alone for meaning; color-vision differences can make red/green or blue/purple distinctions unreliable.
- Watch flicker, strobing, rapid luminance changes, and high-contrast flashing in generated glitch looks, trailers, and music edits. If a platform or jurisdiction has flashing-content requirements, request or run the appropriate photosensitivity check rather than relying on taste.

Production heuristic: add caption/graphic contrast checks after the final grade, not before; the grade can change the background underneath text.

## Generated-media artifact checklist

Inspect AI-generated and AI-enhanced video for:

- Frame-to-frame hue shifts in faces, skies, walls, or product surfaces.
- Flickering saturation or brightness in hair, fabric, foliage, fine texture, water, screens, neon, and particles.
- Color crawling around edges, hands, teeth, logos, text, jewelry, and transparent objects.
- Banding in gradients, skies, bokeh, shadows, and synthetic backgrounds.
- Over-sharpened, plastic, or denoised skin that grades poorly.
- Mismatched embedded lighting: subject warm, background cold; object reflection inconsistent with environment.
- Prompt-driven palette drift: a "blue product" becoming teal in one shot and navy in another.
- Text and logo hallucinations that become more distracting after contrast/saturation changes.

Repair choices:

- **Regenerate** when the artifact is semantic or unstable across the whole clip.
- **Replace** with a still, crop, graphic cover, or alternate angle when only a section fails.
- **Deflicker/denoise/deband** when the issue is technical and the image content is otherwise acceptable.
- **Isolate secondaries** for product/skin fixes when the rest of the frame can keep the look.
- **Reduce look intensity** when the creative grade amplifies artifacts.

Do not over-grade a broken AI shot into acceptability if the defect will damage trust in a product, face, claim, or brand.

## Review scopes and feedback language

Ask what kind of note is needed:

- **Look development note:** describes desired mood and palette before final matching.
- **Correction note:** points out exposure, white balance, cast, contrast, saturation, or shot-match problems.
- **Finishing note:** identifies delivery, scopes, legal levels, color tags, accessibility, compression, or artifact issues.
- **Revision note to editor/colorist:** specific, timecoded, actionable, and priority-ranked.
- **Client note:** concise, outcome-oriented, avoids unnecessary tool jargon.

Strong review notes include:

- timecode or shot identifier;
- what is wrong;
- what should change;
- what must be protected;
- whether it is creative preference, technical QC, or platform risk.

Weak note: "Make it pop."  
Better note: "00:12-00:17 product macro: lift product-side exposure about half a stop, keep background moody, reduce cyan cast on chrome edge, and protect the approved red label from shifting orange."

## Handoff to editors, colorists, and compositors

For a serious finish, hand off:

- timeline/EDL/XML/AAF or frame sequence references;
- source file list with known color spaces, camera/log settings, generated-source notes, and any unreliable metadata;
- target deliverables and color tags;
- reference stills, look stills, and approved product/brand swatches;
- LUTs/CDLs with names, purpose, order, and whether they are viewing-only or baked;
- handles needed for VFX/compositing;
- alpha/graphics requirements and whether overlays should be graded, ungraded, or applied after grade;
- caption/subtitle files and contrast requirements;
- timecoded color notes and known exceptions;
- QC requirements: legal levels, gamut, HDR metadata, bitrate/container/codec, platform specs, review environment.

For AI-generated footage, add prompt/model/source provenance if available, because regeneration may be the cleanest color fix.

## Finishing QA checklist

Use this before calling a color pass final:

- Target color space, transfer, gamut, range, and tags are known and match the export.
- No accidental log, double LUT, missing transform, or full/limited range mismatch.
- Shots match within each scene unless a motivated change is intended.
- Skin, product, brand, UI, and claim-sensitive colors are protected.
- Captions, lower-thirds, disclaimers, and UI overlays are readable after grading.
- Gamut and levels are legal for the delivery requirement.
- Banding, flicker, chroma noise, aliasing, edge halos, and compression artifacts are checked in motion.
- HDR and SDR versions are reviewed separately if both are delivered.
- Platform crops/safe zones do not hide color-critical text or product details.
- Test export is checked on the intended review/display class, not only inside the grading app.
- Handoff package names LUTs/transforms clearly and distinguishes creative look from technical conversion.

## Example: AI product-film color direction

Production intent: 30-second premium skincare product film assembled from AI-generated macro clips, product renders, and motion-graphic end card. Target is SDR Rec.709 for YouTube and 9:16 paid social derivatives.

Direction:

1. Treat AI clips as display-referred unless metadata proves otherwise; do not apply camera-log conversion LUTs.
2. Build the hero look from the approved product render: neutral pearl bottle, soft warm highlights, clean white label, pale champagne background.
3. Correct each shot first: remove green cast from cream texture, match black/white points, keep highlights below clipping on glossy bottle shoulder.
4. Protect label and cap with isolated keys/windows. The bottle must remain pearl, not yellow; logo must remain neutral charcoal.
5. Grade background warmer and lower contrast than the product so the product stays clean and premium.
6. Inspect in motion for shimmer in cream swirls and label edges. If label text crawls or changes, replace with composited label art rather than grading it.
7. Export a Rec.709 SDR master and a separate vertical derivative; check YouTube/TikTok specs at delivery.

Expected result: consistent cream/pearl palette, product color accuracy, soft commercial contrast, no obvious AI shimmer, readable end card.

Likely failure modes: applying a heavy warm LUT shifts the bottle yellow; increasing contrast clips product highlights; matching backgrounds before the product causes packaging drift.

## Example: timecoded review notes for a mixed-source explainer

User request: "Review this draft for color before final export."

Response style:

- 00:00-00:05 intro graphic: finishing issue. White title is readable, but the blue subtitle loses contrast against the dark gradient after compression. Raise subtitle luminance or add a translucent backing plate.
- 00:06-00:14 talking head: correction issue. Face is about one stop darker than the surrounding b-roll and leans green in midtones. Warm/tint toward neutral skin before applying the global look.
- 00:15-00:22 AI b-roll: generated-media issue. The orange server lights flicker between frames and draw attention away from narration. Try deflicker; if it persists, replace with a less textured shot.
- 00:23-00:28 product UI capture: protection issue. Do not apply the teal look to the UI layer; it changes status colors. Composite UI after the grade or isolate it from the look.
- Final export: delivery issue. Confirm SDR Rec.709 tags and run a short platform test encode before approval.

Why this works: each note says where, what kind of issue, what to change, and what downstream risk it addresses.

## Example: HDR request with SDR social delivery

Scenario: user asks for a "glossy HDR trailer" but the campaign will run on TikTok, Instagram, and YouTube Shorts, and the team has only laptop/phone review.

Recommended answer:

Proceed with an SDR Rec.709 master styled with HDR-like highlight design rather than a true HDR master, unless the user can review HDR on a suitable display and needs HDR distribution. Use soft highlight rolloff, bright practicals, and controlled contrast to suggest gloss. Preserve a clean SDR master, then create platform-specific 9:16 derivatives. If a true HDR version is still required, make a separate HDR grade and an SDR trim pass; do not rely on automatic tone mapping for final brand/product approval.

Why this works: it distinguishes aesthetic intent from technical HDR delivery and avoids creating an unreviewable master.
