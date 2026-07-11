---
name: still-image-retouching-finishing
description: Provider-independent still-image post-production skill for RAW/rendered intake, nondestructive development, exposure, white balance, tone, color, ICC proofing, masking, repair, compositing, truthful retouching by genre, generative disclosure, sharpening, noise, resampling, variants, metadata, export, QA, rights, and ethical finishing. Use when an agent must plan, perform, direct, or review still photography retouching and finishing for print, web, social, archive, publication, or client delivery; do not use for image-generation APIs, video grading, or campaign-specific production strategy.
---

# Still Image Retouching and Finishing

This skill is for finishing existing still images. It assumes there is a captured, scanned, rendered, or composited source image and that the agent's job is to make production decisions about development, retouching, color, metadata, output, and review. It is tool-agnostic: Lightroom, Camera Raw, Capture One, Darktable, RawTherapee, Affinity Photo, Photoshop, GIMP, command-line processors, DAM systems, RIP software, and lab portals are possible instruments, but the skill's decisions are about craft and delivery rather than any one vendor.

Use it for:

- RAW intake, rendered-file intake, selects, versioning, sidecars, and handoff notes.
- Nondestructive development: exposure, white balance, tone mapping, lens corrections, local masks, snapshots, proof copies, layers, smart objects, adjustment stacks, and reversible repair.
- Color-managed finishing: working spaces, embedded profiles, monitor profiling, ICC soft proofing, rendering intents, output profiles, print proofing, and web/social conversions.
- Retouching: dust, sensor spots, blemishes, flyaways, fabric wrinkles, product cleanup, architecture perspective, food freshness, documentary limits, compositing cleanup, and client/legal review.
- Generative fill or AI repair decisions only as post-production interventions on existing stills, including disclosure, provenance, and rights notes.
- Sharpening, noise reduction, resampling, crop variants, batch consistency, metadata, accessibility metadata, export recipes, QA, and archive/delivery packages.

Do not use it for:

- Generating new images from prompts as the primary task.
- Choosing or integrating image-generation APIs.
- Video color grading, motion retouching, VFX shot work, or frame-by-frame video finishing.
- Campaign concepting, art direction, casting, styling, media buying, or platform growth strategy except where those affect still-image finishing constraints.

## Grounded Facts

These are documented facts, not taste preferences.

- ICC profiles describe device or color-encoding behavior so color management systems can transform color data between native device color spaces and device-independent spaces. ICC v4 uses a Profile Connection Space based on CIE colorimetry; ICC identifies input, display, and output device profile classes and defines rendering intents for gamut mapping. Source: International Color Consortium, "Introduction to the ICC profile format" and "ICC Specifications," verified 2026-07-11, https://www.color.org/iccprofile.xalter and https://www.color.org/icc_specs2.xalter.
- ICC.1:2022 profile version 4.4.0.0 is the current ICC v4 specification listed by ICC, and iccMAX is specified separately as ICC.2:2023 / ISO 20677 for extended needs such as spectral data or modified PCS behavior. Source: ICC Specifications, verified 2026-07-11, https://www.color.org/icc_specs2.xalter.
- CIE's electronic International Lighting Vocabulary provides public access to terms and definitions from CIE S 017:2020. Use CIE language for colorimetry, illuminants, observers, luminance, reflectance, and viewing-condition claims rather than inventing casual definitions. Source: CIE e-ILV, verified 2026-07-11, https://cie.co.at/e-ilv.
- Lightroom Classic official documentation states that Develop previews use ProPhoto RGB by default, other modules primarily use Adobe RGB, and export/print can choose output profiles such as sRGB or custom printer profiles. It also states that soft proofing previews destination appearance and gamut warnings, and that proof copies can preserve the original edit state. Source: Adobe Lightroom Classic color management and Develop module documentation, verified 2026-07-11, https://helpx.adobe.com/lightroom-classic/help/color-management.html and https://helpx.adobe.com/lightroom-classic/help/develop-module-options.html.
- Camera Raw and Lightroom process versions affect available controls and rendering. Adobe documents newer process versions for improved color mixer banding behavior, high-ISO rendering, dehaze, range mask behavior, tone controls, sharpening, and noise reduction. Source: Adobe Camera Raw and Lightroom process-version documentation, verified 2026-07-11, https://helpx.adobe.com/camera-raw/using/process-versions.html and https://helpx.adobe.com/lightroom-classic/help/develop-module-options.html.
- Exif is an embedded metadata family for digital still-camera files built on JPEG/TIFF/WAV-related specifications, primarily recording technical capture information. CIPA and JEITA jointly manage the Exif standard; the Library of Congress described Exif 3.0 as the most recent version in November 2023 and notes that GPS support was introduced in Exif 2.0 with improvements in 2.2. Source: Library of Congress format description, verified 2026-07-11, https://www.loc.gov/preservation/digital/formats/fdd/fdd000618.shtml.
- IPTC Photo Metadata defines professional photo metadata fields through IPTC Core and IPTC Extension, including rights, creators, people, locations, products, accessibility descriptions, and, in IPTC Photo Metadata 2025.1, AI-related properties. Those 2025.1 AI fields target metadata for AI-generated content; they do not by themselves satisfy every client, publisher, platform, legal, or ethical disclosure requirement for AI-assisted retouching, generative repair, or composite finishing. IPTC states that it uses XMP as one technical format and IIM as another. Source: IPTC Photo Metadata Standard, verified 2026-07-11, https://iptc.org/standards/photo-metadata/iptc-standard/.
- XMP is an extensible metadata framework for embedding metadata in files. Adobe's public XMP documentation describes Part 1 as the data model, serialization, and core properties; Part 1 is also ISO 16684-1:2012. Source: Adobe XMP documentation, verified 2026-07-11, https://www.adobe.com/devnet/xmp.html.
- C2PA develops technical standards for certifying source and history, or provenance, of media content. The C2PA specification site includes Content Credentials, implementation guidance, security considerations, and AI/ML guidance. Source: C2PA Specifications 2.2 index, verified 2026-07-11, https://spec.c2pa.org/specifications/specifications/2.2/index.html.
- Adobe documents Content Credentials in Photoshop as a way to attach attribution details and edit history on export. This is implementation-specific; do not treat it as a universal substitute for IPTC rights metadata, delivery notes, or client disclosure. Source: Adobe Photoshop Content Credentials documentation, verified 2026-07-11, https://helpx.adobe.com/photoshop/using/content-credentials.html.
- Adobe documents sharpening and noise reduction as operations that require 100% or 1:1 inspection for accurate judgment; Lightroom sharpening includes Amount, Radius, Detail, and Masking; Smart Sharpen includes Amount, Radius, Reduce Noise, and blur-type removal choices. Source: Adobe Lightroom retouch documentation and Photoshop Smart Sharpen documentation, verified 2026-07-11, https://helpx.adobe.com/lightroom-classic/help/retouch-photos.html and https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html.
- The NPPA Code of Ethics says visual journalists should be accurate and comprehensive, resist staged manipulation, not alter events, and maintain the integrity of image content and context; editing must not mislead viewers or misrepresent subjects. Source: National Press Photographers Association Code of Ethics, verified 2026-07-11, https://nppa.org/resources/code-ethics.

## Practical Observations

These are production observations that recur across tools and clients. They should be tested against the actual file, brief, and delivery path.

- RAW development is usually the least destructive place to set white balance, global exposure, highlight recovery, shadow placement, lens corrections, chromatic aberration removal, and broad color rendering. Pixel editing is better reserved for repairs, composites, local shape/texture work, and output-specific interventions.
- Rendered files such as JPEG, PNG, HEIC, TIFF, PSD/PSB, or web downloads have already had a demosaic/rendering/color transform applied. Treat them as smaller edit envelopes than camera RAW unless bit depth, profile, and edit history prove otherwise.
- A visually good file can still be production-bad if it lacks an embedded profile, clips important channel detail, contains hidden retouch artifacts, strips required rights metadata, changes documentary meaning, or fails the intended viewing medium.
- A retouch plan is more reliable when it names both the aesthetic target and the truth boundary: "remove temporary lint and sensor dust, keep garment shape and skin texture" is safer than "make it clean."
- Soft proofing is a prediction, not an oracle. It depends on monitor profile quality, ambient viewing conditions, the destination profile, rendering intent, paper/ink simulation, and the lab or press process actually used.
- Output sharpening is destination-dependent. A file prepared for matte fine-art print, glossy magazine reproduction, retina web display, and social recompression rarely wants the same sharpening or noise texture.
- Social platforms often recompress, resize, strip metadata, or convert color. Deliver a clean sRGB version for common social use unless the platform/client explicitly supports a different profile or HDR path, and keep the richer master separately.

## Production Heuristics

Heuristics are defaults to reason from, not rules to obey blindly.

1. Preserve originals and edits. Keep the untouched capture/render, sidecar/catalog state, layered master, flattened delivery exports, and notes on any destructive or generative intervention.
2. Decide the truth class before touching pixels. Editorial documentary, commercial beauty, product e-commerce, architecture, food, fine art, and restoration have different permissible edits.
3. Work broad to narrow. Correct profile interpretation, camera/lens issues, white balance, exposure, tone, and global color before local masks, cleanup, liquify/warp, dodge/burn, skin, product edges, and output sharpening.
4. Use reversible structures when available. Prefer sidecars, virtual copies, snapshots, adjustment layers, layer masks, smart objects, clone/heal on blank layers, named groups, and export presets over flattened edits.
5. Judge detail at the right zoom. Evaluate noise, sharpening, dust, skin texture, moire, halos, resampling, and clone artifacts at 100%; evaluate composition, color balance, and emotional read at fit-to-screen and expected display size.
6. Convert late, embed profiles, and proof before delivery. Keep a high-quality working/master state, then export destination-specific derivatives with explicit profile, dimensions, bit depth, compression, metadata, and sharpening choices.
7. Treat metadata as part of finishing. Technical Exif, IPTC rights/creator/caption, accessibility text, content warnings, model/property releases, AI/generative disclosures, and C2PA/Content Credentials may affect whether a file is usable.
8. Batch for consistency, not blindness. Sync exposure/color/lens settings across a set, then inspect edge cases: mixed light, different ISO, lens swaps, skin-tone variance, clipped product colors, and crops with different output ratios.

## Intake and Triage

Start by asking what the image must remain true to and where it will go.

Minimum intake checklist:

- Source type: camera RAW, DNG, scan, JPEG/HEIC, layered PSD/PSB, TIFF, PNG, screenshot, generated image, composite, or unknown.
- Bit depth, pixel dimensions, color profile, embedded metadata, sidecar/catalog state, and available original.
- Usage: editorial, documentary, e-commerce, beauty, fashion, food, architecture, real estate, fine art, archive, social, paid ad, print, packaging, internal review.
- Delivery: file formats, size/ratio variants, color profile, print process/profile, paper, web CMS, social platform, lab/press specs, naming convention, deadline.
- Permissions: copyright owner, photographer, model/property releases, location restrictions, artwork/product trademarks, client retouching rules, generative-AI policy.
- Truth boundary: what may be removed, improved, reshaped, reconstructed, synthesized, disclosed, or left untouched.

Classify the asset before editing:

- RAW original: build a nondestructive development recipe, keep the capture as source of truth, and export rendered deliverables only after proofing.
- Rendered original: verify profile and bit depth; avoid excessive tonal recovery; consider requesting RAW/TIFF/master if the requested change exceeds the file's latitude.
- Layered master: inspect layer names, masks, adjustment order, hidden layers, linked assets, embedded profiles, and existing retouch intent before changing it.
- Composite or AI-assisted still: identify ingredients, licenses, disclosure requirements, provenance data, and visible seams; do not present it as a documentary capture.
- Scan/restoration: preserve a raw scan, correct dust/fading/cast carefully, retain historical features unless explicitly restoring a display copy, and record interpretation.

## Development Order

A robust still-finishing pass usually follows this order:

1. Ingest and preserve. Duplicate or catalog the source; checksum or otherwise track critical originals when the work is archival or high value.
2. Interpret correctly. Confirm embedded profile, camera profile, RAW process version, demosaic settings, lens profile, orientation, crop, and metadata time/location sanity.
3. Normalize defects. Fix sensor spots, dead pixels, chromatic aberration, lens distortion, perspective issues, moire, and obvious scanning/capture defects before creative grading.
4. Establish neutrals and exposure. Set white balance, exposure, black/white points, highlight rolloff, shadow floor, and midtone contrast according to the subject and output medium.
5. Shape tone and color. Use curves, color mixer, color balance, selective color, calibration/profile choices, or equivalent controls to support the intended look without breaking memory colors or required product matches.
6. Localize with masks. Use subject, luminance, color, gradient, brush, path, frequency, or object masks as needed; feather and refine at natural transitions.
7. Retouch and repair. Heal/clone/patch/dodge/burn/liquify/warp/composite only within the truth boundary; keep repair layers separate when the tool permits.
8. Proof and variant. Soft proof or simulate target conditions, create print/web/social/crop variants, and apply destination-specific output sharpening and metadata rules.
9. QA and deliver. Inspect at multiple zoom levels, compare before/after, check metadata/profile/export specs, and package master plus derivatives according to the handoff.

## Color and ICC Decisions

Do not use color-management terms as decoration. Make explicit decisions.

Working state:

- For RAW development, stay in the tool's high-gamut internal pipeline and avoid premature conversion to sRGB.
- For layered retouching, choose a working RGB space compatible with the source, output, and collaborators. Common choices include ProPhoto RGB for high-gamut photo work, Adobe RGB for print-oriented interchange, and sRGB for web-only or low-risk rendered assets. A larger space is useful only if the pipeline preserves enough bit depth and every collaborator understands the profile.
- Preserve or embed the correct profile when exchanging files. An untagged RGB file is ambiguous.

Display/proofing:

- Calibrate/profile the monitor with a measuring device when color matters; keep ambient light stable and avoid strong colored surroundings.
- Soft proof against the actual destination profile when available: printer/paper/ink profile, CMYK press profile, lab profile, or constrained web/social profile.
- Use gamut warnings as diagnostic signals, not automatic commands. Decide whether hue, saturation, contrast, or perceptual relationship matters most.

Rendering intents:

- Perceptual: often useful for photographic images with many out-of-gamut colors where preserving visual relationships is more important than preserving exact in-gamut values.
- Relative colorimetric: often useful when much of the image is in gamut and preserving in-gamut colors matters; out-of-gamut colors are clipped or mapped to the nearest reproducible colors depending on the profile/CMM.
- Absolute colorimetric: use for proof simulation where the target medium's white point should be simulated, such as press proofing; it can look dull on screen if misunderstood.
- Saturation: generally for business graphics or diagrams rather than photographic fidelity.

Print finishing:

- Ask for paper, printer/press process, profile, required resolution, black generation/CMYK conversion responsibility, proofing expectations, bleed/crop, and maximum ink or file-prep constraints.
- For photo inkjet/fine-art work, keep RGB until the print driver/RIP/profiled workflow if that is the lab's requirement; convert only when the print provider asks for a specific space.
- For press/CMYK, do not casually convert to CMYK without the press profile and proofing context. RGB-to-CMYK is a production conversion, not a finishing afterthought.

Web/social finishing:

- Use sRGB for standard SDR web/social exports unless there is a documented HDR or wide-gamut path.
- Embed the color profile when the format supports it; keep a master with richer metadata because public platforms may strip fields.
- Resize deliberately rather than relying on platform scaling when quality matters.

## Retouching Boundaries by Subject

Define the allowed interventions before making them.

Documentary, news, and public-interest images:

- Allowed by default: exposure/white balance/tone corrections that preserve scene meaning; crop that does not misrepresent context; dust/sensor spot removal if policy permits; metadata correction.
- High risk: removing or adding people, objects, smoke, signage, wounds, weather, trash, shadows, reflections, police tape, protest signs, or anything that changes factual interpretation.
- Required stance: preserve content and context. If the client asks for misleading alteration, refuse or reclassify the image as illustration/composite with disclosure.

Portrait, beauty, and fashion:

- Preserve identity, expression, anatomy, skin texture, and plausible lighting unless the brief explicitly permits stylization.
- Prefer frequency-conscious cleanup, dodge/burn, color evenness, hair/fabric cleanup, and temporary blemish reduction over plastic smoothing.
- Do not change body shape, age, scars, disability markers, skin tone, or culturally significant features without explicit consent and use-case review.

Product and e-commerce:

- The product must remain materially accurate. Remove dust, scratches, fingerprints, capture reflections, stray fibers, and background issues, but do not change features, scale, included accessories, label text, regulatory marks, colorways, or finish unless the image is labeled as a mockup or corrected to match the real product.
- Use reference targets, client swatches, packaging proofs, or measured values when color-critical. Memory color is not enough for cosmetics, apparel, furniture, food packaging, or art reproduction.

Architecture and real estate:

- Correct perspective, verticals, lens distortion, chromatic aberration, mixed lighting, and window pulls while preserving layout and permanent conditions.
- Do not remove structural defects, neighboring buildings, power lines, safety hazards, water damage, or view obstructions when the image is a factual real-estate representation unless disclosure and jurisdiction/client rules permit it.

Food and beverage:

- Preserve edibility and honest serving appearance for editorial or menu use. Remove crumbs, plate smears, wilted edges, sensor dust, and color casts; be cautious about adding steam, gloss, grill marks, volume, garnish, or impossible freshness.
- Product packaging and menu/legal contexts may require closer truthfulness than mood editorial.

Fine art and creative composites:

- Broader manipulation is acceptable when the work is positioned as art, illustration, or fantasy. Still document sources, licenses, model/property releases, generative tools, and edition/export decisions.

## Generative Repair and Disclosure

Generative tools can be useful for extending backgrounds, removing distractions, repairing missing texture, or filling blank crop areas. They also create provenance, rights, and truth problems.

Before using generative repair:

- Confirm the use case permits synthetic pixels.
- Check client, publication, competition, platform, and legal rules.
- Decide whether the image remains a photograph, becomes a photo illustration, or must be labeled as composite/AI-assisted.
- Preserve the original and a non-generative edit path when possible.
- Record what was generated, where, with which system/version if known, and whether Content Credentials/C2PA or IPTC AI fields should be included.

Never use generative repair to fabricate factual content in documentary, news, legal, scientific, insurance, evidence, archival, medical, or real-estate contexts. For commercial images, do not generate product features, safety labels, trademarks, regulated claims, or model attributes that were not approved.

## Metadata and Provenance

Metadata is not merely archival housekeeping; it changes discoverability, accessibility, rights, and trust.

Retain or set:

- Exif: camera/lens/capture data where appropriate; remove GPS/location data when privacy or safety requires it.
- IPTC creator and credit: creator, contributor, copyright notice, credit line, source, contact, job identifier, usage terms, web statement of rights.
- IPTC caption/description: who, what, where, when, why, and relevant context for editorial/archive use.
- IPTC accessibility: alt text and extended description when the file is destined for web, publications, DAM, or accessibility-aware systems.
- IPTC region/product/person fields when they materially improve asset management and rights clarity.
- XMP edit/sidecar state when collaborators need to inspect or continue nondestructive work.
- C2PA/Content Credentials or equivalent provenance when the delivery ecosystem supports it and transparency is required or valuable.

Strip or reduce:

- GPS, serial numbers, private creator contact, client names, child/vulnerable-person locations, unreleased product names, internal prompts, or proprietary workflow notes when delivery privacy demands it.
- Metadata that contradicts the finished image, such as obsolete captions after a crop/composite or rights fields from a prior owner.

Do not rely on metadata alone for disclosure. Some systems strip it. Use visible labels, captions, delivery notes, contracts, or DAM fields when disclosure must survive redistribution.

## Export and Delivery

Match export to use. A good delivery set often includes a layered or high-bit master plus flattened derivatives.

Common master choices:

- Layered PSD/PSB/TIFF for retouch masters with masks and adjustment layers.
- 16-bit TIFF with embedded profile for print/lab/archival interchange when layers are not required.
- DNG or original RAW plus XMP/catalog instructions for nondestructive RAW handoff.

Common derivatives:

- Web/social SDR: JPEG or PNG as needed, sRGB, embedded profile, target pixel dimensions, appropriate compression, output sharpening for screen, metadata policy applied.
- Print photo/lab: TIFF or high-quality JPEG as specified, destination profile or requested RGB space, target dimensions/resolution, print sharpening for media type, crop/bleed checked.
- Press/publication: follow spec exactly; confirm RGB vs CMYK responsibility, profile, TAC/ink limits, resolution, file naming, and proof expectations.
- Archive: original plus high-quality rendered master, descriptive metadata, rights statement, checksum/package when required.
- HDR still: use only when the delivery ecosystem supports it; Adobe documents AVIF, JPEG XL, JPEG, TIFF, PSD/PSB, and PNG for HDR output in Lightroom Classic, with AVIF/JPEG XL support caveats. Verify target support before choosing this path.

Version naming should reveal intent without leaking private details. Example: `client_project_imageID_retouched_master_v03.tif`, `client_project_imageID_web-srgb_2400px_v03.jpg`, `client_project_imageID_print-paperprofile_16x20_v03.tif`.

## QA Checklist

Run QA on the final export, not only the master.

- Opens correctly in at least one independent viewer or target app.
- Correct file format, dimensions, aspect ratio, bit depth, compression, profile, and filename.
- Embedded profile present where needed; no accidental untagged RGB.
- No unwanted clipping in important highlights/shadows; specular clipping acceptable only when intended.
- Skin, neutrals, brand/product colors, foliage, sky, food, and memory colors look plausible for the brief.
- Retouch artifacts checked at 100%: repeating clone patterns, halos, crunchy sharpening, smeared texture, warped geometry, mask edges, banding, noise blotches, chromatic fringes, moire, stair-stepping, dust, and missed spots.
- Crop variants preserve important content, captions still match, and no text/logo is clipped.
- Print proof reviewed under appropriate light where feasible; web/social proof checked after export/resizing.
- Metadata included, updated, or stripped according to the delivery policy.
- Generative/composite disclosures included where required, and provenance credentials verified if used.
- Rights, releases, source assets, and client approval status documented.

## Example: Documentary News Crop and Tonal Finish

This is an example, not a mandatory formula.

Production intent: Finish a RAW news photograph of a city council protest for same-day publication. The editor wants a tighter crop, better readability of faces/signs, and a web JPEG.

Inputs and constraints:

- RAW file, caption notes, photographer credit, location, capture time.
- Editorial truth required; no object removal or generated pixels.
- Delivery: 2400 px long edge, sRGB JPEG, IPTC caption/credit/rights, no GPS in public file.

Workflow:

1. Preserve RAW and sidecar/catalog state.
2. Apply lens profile and chromatic aberration correction.
3. Set white balance from neutral architecture if available; avoid dramatic mood shift.
4. Adjust exposure, highlights, shadows, whites, blacks, and a modest curve so faces and signs are legible without changing night/rain context.
5. Crop tighter only if it does not remove context that changes meaning, such as counter-protesters or police line.
6. Remove sensor dust only if policy permits; do not remove signs, trash, facial expressions, or distracting hands.
7. Apply moderate luminance/color noise reduction at 100% if high ISO; preserve documentary texture.
8. Export sRGB JPEG at requested size with screen sharpening.
9. Add IPTC creator, credit, caption, location, copyright/rights URL; strip GPS if public safety/privacy requires it.
10. QA against original for factual integrity and caption consistency.

Why structured this way: It separates tonal readability from content manipulation. It treats crop and dust removal as editorial decisions, not just aesthetic choices.

Likely failure modes:

- Over-brightening makes night conditions appear safer or calmer than they were.
- Crop removes police presence and changes story context.
- Dehaze/clarity exaggerates conflict or facial features.
- Metadata still contains GPS for a sensitive subject.

Meaningful variations:

- If publication requires visible edit transparency, add C2PA/Content Credentials where supported.
- If the image is for legal evidence rather than publication, deliver the original with checksum and minimal or no rendered adjustment.

## Example: Color-Critical E-Commerce Product Finish

This is an example, not a mandatory formula.

Production intent: Finish studio images of a matte sage-green ceramic mug for e-commerce thumbnails and zoom views. The client reports returns when color is too blue.

Inputs and constraints:

- RAW captures with gray card and ColorChecker/reference frame.
- Physical product sample or approved brand color reference.
- Delivery: square 3000 px JPEGs, sRGB, white background, dust removed, product shape/color accurate.

Workflow:

1. Build or choose a camera/profile workflow from the reference frame; set white balance from the neutral target.
2. Normalize exposure across the set; enable lens corrections and correct perspective only enough to reflect real shape.
3. Use reference view or batch sync for consistent tone/color, then inspect each file for exposure and reflection differences.
4. Retouch dust, fingerprints, background seams, tiny temporary scratches, and capture reflections on separate layers or reversible masks.
5. Do not alter rim thickness, handle shape, glaze finish, logo, capacity cue, or included accessories.
6. Soft proof/export to sRGB and inspect on a profiled display. If the color falls outside sRGB or shifts materially, discuss expectation and provide a note or alternate output rather than forcing a misleading hue.
7. Export web JPEGs with embedded sRGB, consistent crop/scale, screen sharpening, and required product metadata.
8. QA by comparing final exports to the approved reference under controlled light and checking thumbnails and zoom crops.

Why structured this way: Product trust depends on material accuracy. Color decisions are anchored to references rather than subjective pleasing color.

Likely failure modes:

- Global saturation makes the mug more attractive but inaccurate.
- White-background cleanup erodes the product edge or changes silhouette.
- Batch sync ignores a frame with a different reflection and creates patchy glaze.
- Social/web compression shifts color because the export lacked an embedded profile.

Meaningful variations:

- For marketplace platforms that strip metadata, keep a separate rights-rich master and deliver platform files as expendable derivatives.
- For print packaging, request the press profile and proof; do not assume the sRGB web file is acceptable.

## Example: Beauty Portrait Retouch with Consent Boundary

This is an example, not a mandatory formula.

Production intent: Finish a high-resolution beauty portrait for a cosmetics brand. The campaign asks for polished skin while keeping the model recognizable and avoiding skin-tone lightening.

Inputs and constraints:

- 16-bit RAW-derived TIFF or RAW plus retouch brief.
- Model release and brand retouching policy.
- Delivery: layered master, print TIFF, web/social crops, disclosed generative policy if any AI tools are used.

Workflow:

1. Establish neutral color and exposure; keep skin tone aligned with reference and scene lighting.
2. Correct lens issues and chromatic aberration before skin work.
3. Clean temporary blemishes, stray makeup fallout, dust, lint, and flyaway hairs that distract from the product.
4. Use dodge/burn and frequency-aware cleanup sparingly to even tone while preserving pores, fine lines, facial asymmetry, and identity.
5. Avoid changing face shape, body shape, skin color, age markers, scars, or culturally significant features unless consent and policy explicitly allow it.
6. If generative fill is considered for background extension, keep it away from face/body/product claims and record the intervention.
7. Create crop variants after retouching but before final output sharpening; check that every crop respects anatomy and product placement.
8. Export print and web derivatives with appropriate profiles and sharpening; include rights/credit metadata as allowed.

Why structured this way: Beauty finishing has a high risk of unrealistic body/skin alteration and representational harm. The workflow makes consent and brand policy active constraints.

Likely failure modes:

- Texture smoothing creates plastic skin.
- Eye whitening, teeth whitening, or skin lightening changes identity and tone.
- Liquify creates impossible anatomy.
- Generative background fill introduces hair/edge artifacts or undisclosed synthetic pixels.

Meaningful variations:

- For editorial portraiture, reduce polish and avoid beauty-standard normalization.
- For medical/skincare before-and-after images, require stricter parity of lighting, expression, crop, exposure, and no misleading retouch.

## Example: Fine-Art Print Soft Proof and Delivery

This is an example, not a mandatory formula.

Production intent: Prepare a landscape photograph for a 24 x 36 inch matte cotton-rag print and a small online portfolio version.

Inputs and constraints:

- RAW file and photographer's preferred look.
- Printer/paper ICC profile supplied by lab.
- Delivery: 16-bit TIFF for print, web JPEG at 2200 px long edge.

Workflow:

1. Develop RAW in a wide-gamut pipeline; recover highlights and shape shadows while preserving intended atmosphere.
2. Remove sensor dust and chromatic aberration; inspect sky gradients for banding.
3. Create a proof copy for the matte paper profile. Enable paper/ink simulation if appropriate and compare against the non-proof master.
4. Adjust proof copy for reduced matte-paper contrast and gamut compression: targeted curve, saturation restraint, and local contrast where needed.
5. Choose rendering intent after comparing perceptual and relative colorimetric proof previews; document the selected intent.
6. Resize only if required by the lab; otherwise deliver at native pixels with lab instructions. Apply print sharpening appropriate to matte media.
7. Export embedded-profile print TIFF and sRGB web JPEG separately. Do not use the print-proof file as the web file unless it also looks correct in sRGB.
8. QA print TIFF for profile, dimensions, dust, halos along mountains/trees, clipped clouds, and banding; QA web JPEG for contrast and color after sRGB conversion.

Why structured this way: Matte paper reduces contrast and saturation compared with a backlit display. A proof copy avoids damaging the master while optimizing for a specific medium.

Likely failure modes:

- Editing only on a bright display leads to a dark print.
- Strong clarity creates halos along high-contrast ridgelines.
- Gamut compression dulls saturated foliage or sunset color without compensation.
- Web export accidentally uses the printer profile.

Meaningful variations:

- For glossy paper, use different proof/sharpening expectations.
- For press reproduction, request the publication's CMYK profile and proofing standard rather than using the fine-art lab profile.

## Source Notes

Key sources checked on 2026-07-11:

- International Color Consortium: ICC profile introduction and ICC specifications, https://www.color.org/iccprofile.xalter and https://www.color.org/icc_specs2.xalter.
- CIE: electronic International Lighting Vocabulary, https://cie.co.at/e-ilv.
- IPTC: Photo Metadata Standard, https://iptc.org/standards/photo-metadata/iptc-standard/.
- Adobe: XMP documentation, Lightroom Classic color management, Lightroom/Camera Raw process versions, Lightroom retouch/export documentation, Photoshop layers/repair/sharpening/Content Credentials documentation, https://www.adobe.com/devnet/xmp.html and Adobe Help pages cited above.
- C2PA: Specifications 2.2 index, https://spec.c2pa.org/specifications/specifications/2.2/index.html.
- Library of Congress: Exchangeable Image File Format family, https://www.loc.gov/preservation/digital/formats/fdd/fdd000618.shtml.
- National Press Photographers Association: Code of Ethics, https://nppa.org/resources/code-ethics.