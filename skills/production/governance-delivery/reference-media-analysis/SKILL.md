---
name: reference-media-analysis
description: Provider-independent reference media analysis for generated-media production. Use when an agent must analyze reference images, videos, audio, style boards, product shots, brand assets, mood boards, storyboards, performances, prior cuts, or client examples and translate them into safe, non-copying direction, prompts, QA criteria, provenance records, and handoff notes for image, video, audio, avatar, or post-production agents.
---

# Reference Media Analysis

Use reference media to understand what works, not to reproduce protected expression, private identity, or misleading claims. Treat each reference as evidence for production decisions: extract transferable intent, structure, craft, constraints, and quality bars; avoid copying distinctive expression unless the client has explicit rights and approvals for that exact use.

This skill is not legal advice. It gives production triage, documentation, and escalation triggers. When rights, likeness, voice, trademark, privacy, endorsement, or jurisdictional questions materially affect release, pause and ask for client/legal approval.

## The governing rule: extract function, not identity

For every reference, separate:

- Documented facts: what the file visibly or audibly contains; metadata; rights and consent statements supplied by the client.
- Production inferences: why the reference works; what creative function each element serves.
- Heuristics: safe ways to adapt the function into a new work.
- Prohibited copying risks: distinctive expression, private identity, voice/likeness, trademarks, product claims, or platform-regulated synthetic media disclosures.

Convert "make it like this" into "make a new work with the same production function." Examples:

- Do extract "cold open in 0.8 seconds, problem stated before brand reveal, high-contrast captions."
- Do not copy the exact edit, catchphrase, character, layout, choreography, melody, camera sequence, voice, celebrity likeness, or trade dress.
- Do extract "warm, credible founder-read with relaxed pacing."
- Do not clone a real speaker's voice or imply their endorsement without documented consent.

## Start with a clearance and risk gate

Before detailed creative analysis, build a reference ledger. If inputs are incomplete, continue with visible/audio analysis but mark missing permissions as blockers for production use.

Minimum ledger fields:

```yaml
reference_id: ref_001
asset_type: image | video | audio | storyboard | mood_board | brand_asset | product_shot | prior_cut | performance
source_location: local path, URL, client upload, DAM ID, or physical source note
source_owner_or_provider: known owner, platform, agency, photographer, performer, unknown
provided_by: client | internal team | public web | user upload | stock provider | other
permission_basis: owned | licensed | client-approved | public-domain claim | fair-use claim | unknown
license_or_approval_evidence: contract ID, email, rights memo, release, invoice, stock license, none
allowed_uses: analysis only | prompt reference | direct incorporation | brand/product fidelity | internal review only
restricted_uses: no training, no public release, no likeness, no voice, no logo, no minors, no paid ads, etc.
people_present: none | private person | public figure | employee | actor | minor | unknown
likeness_or_voice_risk: none | low | medium | high | blocker
trademark_or_trade_dress_risk: none | low | medium | high | blocker
privacy_or_sensitive_data: none | faces | locations | medical | financial | credentials | minors | other
synthetic_or_manipulated_status: captured | edited | AI-generated | mixed | unknown
provenance_checked: C2PA/Content Credentials, IPTC, EXIF/XMP, file history, none
client_approval_status: approved | pending | rejected | not requested
analysis_date: YYYY-MM-DD
notes:
```

Triage:

- Green: client-owned or licensed reference, no private likeness/voice, no sensitive data, no direct reuse needed, output will be stylistically distinct.
- Yellow: public web reference, unclear license, recognizable people, visible brands, close style mimicry, testimonial/product claims, or uncertain platform disclosure. Use for analysis only; require abstraction and approval before production.
- Red/blocker: requested voice or likeness clone without consent; minor or private person in synthetic scenario; exact copy of distinctive ad/art/music/choreography; fake endorsement/testimonial; unsafe product/medical/financial claim; leaked/private asset; confidential client material without authorization; platform/political synthetic-media disclosure not resolved.

## Provenance and metadata checks

Check provenance when authenticity, rights, disclosure, or client trust matters. Do not treat metadata as conclusive proof: files can lose or alter metadata during export, upload, transcoding, or editing.

Use available tools to inspect:

- C2PA / Content Credentials: look for manifests, claims, assertion history, ingredients, signing status, and validation failures. C2PA manifests are provenance records, not legal clearance.
- IPTC Photo Metadata: inspect rights fields, creator, copyright notice, credit line, licensor, and Digital Source Type. For generated images, note whether the IPTC Digital Source Type indicates generative AI.
- EXIF/XMP/container metadata: capture camera/software, creation/modification dates, codec, dimensions, frame rate, color profile, sample rate, and embedded captions where available.
- File history: record URL, download date, uploader/client source, checksums if the workflow needs reproducibility.

If provenance is absent, stripped, conflicting, unverifiable, or inconsistent with the visible media, record "unknown/conflicting" and escalate if authenticity matters.

## What to extract versus what not to copy

| Reference dimension | Extract | Do not copy unless explicitly cleared |
|---|---|---|
| Concept | Audience, promise, emotional arc, information hierarchy | Exact joke, twist, slogan, storyline, fictional world, branded campaign idea |
| Visual style | Lighting logic, palette family, texture density, level of realism, lens language | Distinctive composition, character design, logo lockup, signature illustration style, trade dress |
| Shot design | Shot sizes, camera purpose, sequencing rhythm, transition function | Frame-for-frame storyboard, same camera path around same subject, recognizable staging |
| Editing | Pacing, beat structure, escalation, caption density, call-to-action timing | Exact cut timing, music-sync pattern, montage order, viral template with protected audio/graphics |
| Performance | Energy, intention, emotional beats, gesture categories | Likeness, face, voiceprint, accent caricature, exact gestures/choreography of a performer |
| Audio/music | Tempo range, instrumentation family, mix priorities, sonic mood | Melody, lyrics, sample, soundalike singer, recognizable voice, copyrighted recording |
| Product/brand | Accurate product geometry, approved colors, approved claims, mandatory disclaimers | Competitor marks, unauthorized co-branding, altered regulated claims, confusingly similar packaging |
| Accessibility | Caption placement, contrast, readable pacing, audio-description needs | Tiny inaccessible captions or color-only distinctions just because the reference used them |

## Decompose the reference

Analyze only at the depth needed for the production decision. A social cut may need frame-level timing; a style board may need only palette, materials, composition, and anti-patterns.

Universal decomposition:

- Intent: what the reference is trying to make the audience feel, understand, or do.
- Audience/platform: expected viewer context, aspect ratio, sound-on/off assumption, disclosure needs, accessibility needs.
- Structure: hook, setup, proof, emotional turn, reveal, CTA, end card.
- Craft: composition, light, color, motion, typography, edit rhythm, audio mix, performance, product fidelity.
- Distinctiveness: the elements that make this reference recognizably itself.
- Transferable principles: abstract rules that can guide a new work without copying.
- Risk register: rights, likeness, voice, trademark, safety, culture, privacy, platform disclosure.
- Production spec: prompts, shot list, negative constraints, QA criteria, handoff notes.

### Images, product shots, brand assets, mood boards

Capture:

- Subject and composition: hero object, support props, visual hierarchy, crop, negative space, perspective.
- Surface and material cues: gloss/matte, grain, fabric, metal, liquid, glass, screen reflections.
- Lighting: direction, hardness, falloff, catchlights, shadow density, color temperature.
- Palette: dominant/accent colors, contrast, saturation, brand color constraints.
- Lens/render language: macro, telephoto compression, wide-angle distortion, orthographic, CGI, editorial photography, flat illustration.
- Product fidelity: dimensions, labels, ports/buttons, packaging, SKU/colorway, "must be exact" details.
- Brand system: logo use, typography, spacing, approved lockups, prohibited distortions.
- Safe adaptation: keep authorized product truth; change set dressing, pose, camera angle, background, and art direction enough to avoid lookalike output.

### Video, prior cuts, reels, ads, trailers, storyboards

Build a beat map:

```text
00:00-00:02 Hook: visual/event, sound, text, viewer question
00:02-00:06 Setup: subject, setting, conflict, first proof
00:06-00:12 Development: cuts, motion direction, evidence, escalation
00:12-00:18 Turn/reveal: product, punchline, transformation, result
00:18-00:22 CTA/end: brand, disclosure, next action
```

Capture:

- Shot list: shot size, camera movement, subject action, transition in/out, duration.
- Pacing: average shot length, acceleration/deceleration, breath moments, jump cuts, match cuts.
- Motion grammar: push-in for importance, lateral move for discovery, handheld for urgency, locked-off for authority.
- Graphics: caption cadence, lower thirds, overlays, UI callouts, safe areas.
- Sound: music tempo, edit sync, SFX accents, voice/music balance, silence.
- Differences to require: new scene order, new visual metaphor, different set/props, distinct graphic system, distinct music/SFX, rewritten language.

### Audio, music, voice, and performance references

Capture:

- Voice/performance: pace, pitch range, energy, emotional intent, pauses, articulation, distance from mic.
- Music: tempo range, genre family, instrumentation, arrangement arc, density, dynamics, mix placement.
- Sound design: diegetic/non-diegetic sources, impacts, whooshes, room tone, transitions.
- Accessibility: transcript, captions, intelligibility, loudness consistency.

Translate to descriptors, not cloning:

- Use "confident, unhurried, friendly, dry humor, 145 WPM, conversational pauses."
- Avoid "sound like [real person]" unless the client provides a documented voice/likeness release and the provider permits it.
- Avoid mimicking distinctive singer timbre, melody, lyrics, or recognizable recordings.

### Avatar, face, likeness, and acting references

For human references, extract performance intent rather than identity:

- Allowed without special consent in many production workflows: "uses open palms when explaining," "smiles before CTA," "leans in at the objection," "speaks directly to camera."
- Needs documented permission and provider/platform review: face replacement, avatar made from a person, voice clone, celebrity/public-figure resemblance, employee testimonial, before/after medical or financial outcome, political synthetic media.
- Avoid demographic caricature. If a cultural marker matters, describe production-relevant context and ask for sensitivity review when the work targets or depicts a culture, religion, ethnicity, disability, gender identity, or protected class.

## Translate analysis into provider-independent prompts

Use a three-layer prompt handoff:

1. Production intent: the job the media must do.
2. Abstracted reference learnings: transferable style/structure/performance principles.
3. Safety and distinctness constraints: what must not be copied or implied.

Prompt skeleton:

```text
Intent:
[Audience, deliverable, platform, emotional and commercial goal.]

Reference-derived direction:
[Abstracted visual/audio/edit/performance principles. Do not name the reference as something to imitate unless the provider workflow requires reference attachment labels.]

Originality constraints:
Create a distinct new work. Do not reproduce the reference's exact composition, character design, layout, slogan, melody, voice, choreography, edit sequence, logo/trade dress, or any recognizable protected element. Preserve only the approved product/brand details listed below.

Approved exact elements:
[Client-owned product renders, logo, SKU geometry, claims, disclaimers, color values, if any.]

Creative spec:
[Shot list, style, camera, lighting, motion, audio, text, duration, aspect ratio.]

Negative constraints:
[No real-person likeness, no celebrity resemblance, no brand confusion, no fabricated endorsement, no inaccessible text, no unsafe stereotypes, no unapproved claims.]

Disclosure/provenance:
[AI/synthetic disclosure needed? C2PA/IPTC/ledger requirements? Client review checkpoint?]
```

When a provider accepts reference files, label each reference by function:

- `ref_style_palette`: color/material inspiration only.
- `ref_product_fidelity`: approved product geometry; preserve exactly.
- `ref_pacing`: timing/structure only; do not copy visuals.
- `ref_performance_energy`: acting energy only; do not copy identity or voice.
- `ref_brand_asset`: approved logo/typography use; follow brand rules.

Do not upload confidential, private, or unlicensed references to external providers unless the client has approved that provider/workflow and the provider terms permit the use.

## Similarity and plagiarism risk review

Rate similarity before handoff and again after generation.

- 0: no meaningful similarity beyond broad genre conventions.
- 1: shares generic production traits (e.g., warm studio lighting, fast captions).
- 2: shares several abstracted traits but composition, text, subjects, sequence, and audio are distinct.
- 3: recognizably close in layout, sequence, character, copy, sound, or campaign idea; revise before release.
- 4: likely copy/lookalike/soundalike/false association; stop and escalate.

Common escalation triggers:

- The user requests "same but with our logo," "in the exact style of this living artist," "clone this voice," "make the celebrity say," or "use this competitor ad as a template."
- Generated output would be mistaken for the reference creator's work, a real endorsement, a real news event, or an official product/brand asset.
- Product claims, testimonials, before/after results, prices, rankings, medical/financial outcomes, or sustainability claims are not substantiated.
- The output contains a person who did not consent, especially a minor, private person, employee, patient, student, customer, or deceased person.
- Political/election, public-interest, health, safety, or crisis content includes realistic synthetic people/events.

## Comparative QA against generated outputs

Review the generated output against two targets: the production brief and the risk register.

QA checklist:

- Intent match: does it solve the same production problem as the reference?
- Distinctness: would a reasonable viewer recognize the reference as the source? If yes, revise.
- Rights: are only approved assets directly reused? Are license restrictions preserved?
- Likeness/voice: no unauthorized identity, voiceprint, celebrity resemblance, or implied endorsement.
- Product fidelity: approved product details and claims are accurate; no hallucinated features, seals, partnerships, rankings, or UI.
- Trademark/trade dress: no confusingly similar competitor packaging, logos, app screens, or brand systems.
- Cultural safety: no stereotypes, sacred-symbol misuse, accent caricature, or decontextualized cultural markers.
- Accessibility: captions/transcripts where needed; readable text; sufficient contrast for overlays; no meaning conveyed by color alone.
- Disclosure: platform/client-required AI/synthetic labels, ad disclosures, and provenance metadata are planned.
- Technical fidelity: aspect ratio, frame rate, duration, codec, loudness, color profile, safe areas, and file naming match delivery specs.
- Ledger completeness: reference IDs, generated asset IDs, model/provider settings, dates, approvals, and review notes are captured.

## Safe handoff format

Give downstream production agents a compact packet, not a vague instruction to "match the reference."

```yaml
reference_analysis_packet:
  project:
    deliverable:
    platform:
    audience:
    release_context: organic | paid_ad | internal | broadcast | public_interest | political | regulated
  references:
    - reference_id:
      allowed_use:
      provenance_summary:
      rights_status:
      risk_status:
  extracted_principles:
    structure:
    visual_style:
    motion_editing:
    audio_voice:
    performance:
    product_brand:
  must_preserve:
    - approved product geometry
    - approved logo/color/claim/disclaimer
  must_change:
    - composition
    - copy
    - set/props
    - music/melody
    - performer identity
    - edit sequence
  prompt_blocks:
    image:
    video:
    audio:
    avatar:
  negative_constraints:
    - no unauthorized likeness or voice clone
    - no exact reference layout, slogan, melody, or sequence
    - no false endorsement or unsubstantiated claim
  disclosure_and_provenance:
    ai_label_needed:
    c2pa_or_iptc_needed:
    client_approval_needed:
  qa_plan:
    similarity_threshold: revise at 3, block at 4
    comparison_method:
    reviewer_questions:
```

## Example: adapting a product mood board into an image prompt

Production intent: create a hero image for a new insulated bottle. The client owns the product render and provided a mood board of premium outdoor ads from several brands.

Analysis:

- Extract: low sunrise angle, premium quiet mood, condensation detail, large negative space for headline, tactile rock/metal surfaces.
- Preserve exactly: approved bottle geometry, cap, color, logo placement, claim "keeps drinks cold up to 24 hours" only if substantiated by client.
- Do not copy: any competitor landscape, exact bottle placement, color-blocking, logo treatments, headline style, or recognizable campaign layout.
- Risk: medium trademark/trade-dress risk because references are competitor ads; use analysis only and make a distinct composition.

Prompt handoff:

```text
Create a distinct premium outdoor hero image for an insulated bottle campaign. Use the approved bottle render as the only exact reference for product geometry, cap shape, color, and logo placement. Build an original dawn setting with cool blue ambient light, a warm rim-light edge, realistic condensation, tactile stone texture, and generous negative space in the upper-left for future headline placement.

The image should feel quiet, durable, and high-end, with a low camera angle and shallow depth of field. Do not reproduce any reference ad layout, landscape, prop arrangement, slogan, color blocking, or competitor trade dress. Do not add unapproved certifications, awards, claims, or co-branding. Avoid visible people, competitor logos, and text.

Output: 4:5 vertical, product centered slightly right, clean space for typography, realistic commercial photography style.
```

QA:

- Compare against competitor references: if product placement, horizon, headline space, or palette feels recognizably lifted from one ad, revise.
- Confirm product render fidelity and no hallucinated features.
- Confirm client approves the claim and final layout before paid media.

## Example: adapting a prior cut into a new video direction

Production intent: make a 20-second launch reel using a client's previous SaaS launch video as pacing reference.

Reference-derived beat map:

```text
00:00-00:02 Pattern interrupt: fast UI close-up + short headline
00:02-00:06 Pain point: two rapid proof shots
00:06-00:12 Product flow: three-step transformation
00:12-00:17 Social proof: result metric + customer quote card
00:17-00:20 CTA: logo, URL, short offer
```

Safe adaptation:

- Keep the beat function and total duration.
- Change the visual metaphor, UI camera paths, type system, music, captions, and CTA phrasing.
- Use only current approved UI screens; do not reuse old customer quote unless cleared.

Video prompt/spec:

```text
Produce a new 20-second SaaS launch reel with a crisp editorial pace: immediate hook, two proof beats, a three-step product transformation, result card, and CTA. Use original kinetic typography based on the current brand system, new UI screen recordings, and a clean electronic pulse around 110-125 BPM.

Do not recreate the prior cut's exact shot order, camera moves, caption wording, music, transitions, or customer quote. Avoid implying new integrations, certifications, or metrics not listed in the approved claim sheet. Use AI/synthetic disclosure if the platform or ad policy requires it for generated UI, voice, or realistic synthetic scenes.
```

QA:

- Side-by-side review for timing, captions, and transitions: similarity score must remain 2 or below.
- Check all claims against the approved claim sheet.
- Check captions and end card readability on mobile.

## Example: translating a voice reference without cloning

Production intent: generate narration for an explainer. Client links a founder podcast as a "voice vibe" but has not provided a voice-clone release.

Allowed extraction:

- Calm founder energy, 135-150 words per minute.
- Mild enthusiasm on key product words.
- Short pauses after technical terms.
- Conversational, credible, not announcer-like.

Not allowed:

- "Clone this founder's voice."
- Matching vocal timbre, accent, speech quirks, or identity.
- Implied founder endorsement if the founder did not approve the script.

Prompt:

```text
Narration style: calm, credible founder-like delivery without imitating any real person. Conversational pace around 140 WPM, warm but restrained energy, clear articulation of technical terms, short pauses after each section heading, no announcer voice, no celebrity or founder soundalike.
```

Handoff note:

```yaml
voice_reference_use: performance energy only
voice_clone_authorized: false
approval_needed: client script approval; legal review if release context implies founder endorsement
```

## Cultural, safety, and privacy review

Reference media often encodes assumptions the client does not intend to copy. Watch for:

- Cultural markers used as decoration without context.
- Religious or sacred objects used for aesthetic impact.
- Accent, dialect, clothing, food, music, or gesture stereotypes.
- Disability, body, age, gender, race, ethnicity, nationality, caste, or class caricatures.
- Minors, patients, students, employees, customers, bystanders, addresses, badges, screens, license plates, documents, medical/financial data, or location metadata.
- Public-interest, election, health, legal, financial, disaster, or conflict scenarios where realistic synthetic media could mislead.

If the output depicts real-world events or people in a way viewers could mistake for authentic footage, require disclosure and review platform rules at production time.

## Volatile rules to re-check at production time

Platform and provider rules change often. Re-check current rules before upload, ad trafficking, or public release, especially for:

- YouTube altered/synthetic content disclosures.
- TikTok AI-generated content labels and synthetic media rules.
- Meta AI labels, ad policies, political/content standards, and manipulated media rules.
- Google Ads/Merchant Center requirements for AI-generated product imagery or synthetic political ads.
- EU AI Act Article 50 / Code of Practice obligations for machine-readable marking and deepfake labeling when the work targets or is distributed in the EU.
- Provider terms for uploading third-party references, faces, voices, product images, logos, and confidential assets.

## Sources and verification notes

Use these as factual anchors, but verify volatile platform/provider rules again on the production date.

- C2PA Technical Specification v2.4, Content Credentials manifests and provenance structure, verified 2026-07-10: https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html
- C2PA Implementation Guidance v2.4, including time-stamp manifest guidance, verified 2026-07-10: https://spec.c2pa.org/specifications/specifications/2.4/guidance/Guidance.html
- IPTC Photo Metadata Standard 2025.1 and IPTC Digital Source Type NewsCodes, verified 2026-07-10: https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata and https://cv.iptc.org/newscodes/digitalsourcetype/
- U.S. Copyright Office, Copyright and Artificial Intelligence hub; Part 1 Digital Replicas; Part 2 Copyrightability; and 2023 AI registration guidance, verified 2026-07-10: https://www.copyright.gov/ai/
- Federal Register, "Copyright Registration Guidance: Works Containing Material Generated by Artificial Intelligence," verified 2026-07-10: https://www.federalregister.gov/documents/2023/03/16/2023-05321/copyright-registration-guidance-works-containing-material-generated-by-artificial-intelligence
- FTC Dot Com Disclosures and revised online disclosure guidance; FTC Endorsement Guides FAQ; FTC final rule announcement on fake reviews/testimonials; FTC AI impersonation proposal, verified 2026-07-10: https://www.ftc.gov/business-guidance/resources/com-disclosures-how-make-effective-disclosures-digital-advertising, https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking, https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials, https://www.ftc.gov/news-events/news/press-releases/2024/02/ftc-proposes-new-protections-combat-ai-impersonation-individuals
- YouTube altered/synthetic content disclosure help and creator blog, verified 2026-07-10: https://support.google.com/youtube/answer/14328491 and https://blog.youtube/news-and-events/disclosing-ai-generated-content/
- TikTok AI-generated content label announcement, verified 2026-07-10: https://newsroom.tiktok.com/en-us/new-labels-for-disclosing-ai-generated-content
- Meta approach to labeling AI-generated content and manipulated media, verified 2026-07-10: https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/
- European Commission Code of Practice on Transparency of AI-Generated Content and EU AI Act Regulation (EU) 2024/1689, verified 2026-07-10: https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content and https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- NIST AI RMF Generative AI Profile, verified 2026-07-10: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- W3C WCAG 2.2 and WCAG 2.2 Understanding pages for contrast, captions, and audio description, verified 2026-07-10: https://www.w3.org/TR/WCAG22/
- USPTO likelihood of confusion and similar trademark search guidance, verified 2026-07-10: https://www.uspto.gov/trademarks/search/likelihood-confusion and https://www.uspto.gov/trademarks/basics/why-search-similar-trademarks
