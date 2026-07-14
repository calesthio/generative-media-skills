---
name: generated-media-qa
description: Provider-independent quality assurance for AI-generated and AI-assisted media. Use when reviewing, accepting, revising, or reporting on images, video, audio, avatars, ads, product content, social clips, explainers, localization, mixed-source edits, captions, accessibility, provenance, model metadata, safety/policy, and delivery readiness.
---

# Generated Media QA

Treat QA as a release decision, not a vibe check. Judge the deliverable against the approved brief, platform specifications, legal/safety constraints, and the audience context. Record enough evidence that another agent or producer can reproduce the decision.

## Keep three evidence lanes separate

Documented facts are requirements from the brief, platform specs, legal/policy guidance, delivery standards, accessibility standards, or provider documentation. Cite them or name the source and verification date.

Empirical observations are what you directly measured or inspected in the asset: frame size, duration, loudness, sync offset, OCR output, transcript mismatch, visual artifact, metadata, or a timestamped defect.

Production heuristics are professional judgments used when no explicit spec exists: whether a hand artifact is audience-visible, whether a product packshot feels trustworthy, whether an accent is intelligible for the target market, whether a social caption is too fast for mobile. Label these as heuristics and avoid pretending they are universal standards.

## Intake before review

Do not start with random artifact hunting. Build the acceptance frame first.

Collect:

- Approved brief, prompt, storyboard, script, shot list, edit decision list, brand rules, product facts, target audience, target platform, duration, aspect ratio, language/locale, and known compromises.
- Delivery spec: file format, codec, resolution, frame rate, color space/HDR, audio channels, loudness target, captions format, thumbnail and metadata requirements.
- Source inventory: generated assets, human-shot assets, licensed stock, user-provided media, logos, fonts, music, SFX, voices, product claims, model releases, likeness/voice consent, and usage rights.
- Generation metadata when available: provider, model, model version/date, prompt, negative prompt, reference images, seed, dimensions, duration, fps, voice ID, language, post tools, upscalers, edit tools, and safety filters.
- Risk context: ads, health/finance/legal claims, political content, public figures, minors, regulated products, synthetic endorsements, realistic news-like scenes, localization, accessibility obligations, and platform disclosure requirements.

If the brief is missing, write a provisional QA basis such as: "Reviewing against supplied asset, target platform: Instagram Reels, inferred goal: 15 s product teaser. Product-claim and legal review cannot pass until facts and rights are supplied."

## First pass: acceptance matrix

Create a small matrix before deep inspection:

| Area | Pass evidence | Typical reject evidence |
|---|---|---|
| Brief conformance | Message, product, audience, tone, duration, format, and call to action match the approved brief | Wrong product, missing CTA, wrong locale, off-brand tone, materially changed promise |
| Technical delivery | File opens, spec matches, no corruption, correct duration/fps/aspect, audio/captions present as required | Wrong aspect, corrupt frames, missing audio, bad encode, unsupported caption file |
| Generated-media realism | No audience-visible anatomy, physics, identity, text, logo, continuity, or temporal defects | Warped hands/faces, unreadable text, drifting identity, morphing product, flicker, impossible motion |
| Audio and speech | Intelligible, synced, no clipping/noise/pops, correct language/voice, loudness meets target | Dialogue buried, lip sync off, clipping, wrong voice, mistranslation |
| Accessibility | Captions, transcript, alt text, audio description, safe flashing, and player affordances meet the delivery context | Missing captions where required, unreadable captions, unsafe flashes, visual-only information with no alternative |
| Rights and provenance | Source rights, consent, metadata, and AI disclosure are documented | Unlicensed source, unapproved likeness/voice, missing synthetic disclosure, unverifiable origin |
| Safety/policy | No disallowed deception, unsafe advice, discriminatory content, or platform-prohibited claims | Misleading synthetic person/event, unsupported health claim, unsafe instructions, regulated-product violation |

Then inspect. Do not let a single attractive frame override a failed acceptance criterion.

## Language-alignment QA lane

When the delivery includes generated shot descriptions, search metadata, prompt reconstructions, source captions, or dataset annotations, review language separately from pixel/audio quality.

- **Accuracy:** every described entity, action, spatial relation, camera behavior, overlay, and state change matches the source; no hallucination or unsupported intent.
- **Completeness:** coverage matches the declared use. Archive search, VFX handoff, prompt comparison, and training data require different levels of detail.
- **Terminology:** approved project vocabulary and reference frames are used consistently; distinguish subject-left from frame-left and dolly/translation from zoom/rotation.
- **Temporal order:** events, cuts, focus changes, entries/exits, and start/end states appear in source order.
- **Provenance:** description author/model/version, prompt, source asset/hash, specification/glossary version, reviewer, and acceptance status are recorded.
- **Risk:** false product, safety, legal, identity, medical, financial, or public-interest descriptions are Critical when they affect release or downstream decisions.

Accessibility captions, subtitles, and audio description have separate audience and standards requirements. Do not replace them with production descriptions. Use `precise-video-description` to define or repair the observation contract; use `video-description-oversight` for the complete pre-caption/critique/post-caption review workflow. This lane only ensures the final delivery's language assets align with the reviewed source and declared use.

## Technical file QA

Use automated checks for measurable properties and human review for perceptual defects. Automated file QC catches many delivery failures, but it cannot decide whether a generated product label is semantically wrong or whether a synthetic spokesperson feels deceptive.

Check:

- File integrity: opens in at least two players/viewers; no truncated tail, decode errors, missing streams, alpha surprises, or silent channels.
- Container and streams: expected format, codec, profile, resolution, pixel aspect ratio, frame rate, duration, color primaries/transfer/matrix, bit depth, bitrate, audio sample rate, channel layout, and captions/subtitle streams.
- Visual defects: black frames, freeze frames, dropped/duplicated frames, banding, macroblocking, moire, aliasing, unintended borders, watermark remnants, bad mattes, poor keying, crop errors, unsafe title area, unreadable small text, and compression damage.
- Audio defects: clipping, inter-sample peaks, noise floor, hum, clicks, pops, gating artifacts, reverb wash, harsh sibilance, phase cancellation, channel imbalance, missing stems, and abrupt edits.
- Versioning: filename, slate, burned-in timecode, metadata, export preset, and revision number match the delivery tracker.

For broadcast or premium delivery, use the client/platform spec as the authority. SMPTE describes IMF as a file-based media format for storing and delivering audiovisual masters across versions and territories. DPP/AS-11-style workflows use explicit technical and editorial metadata. These are not default requirements for a TikTok draft, but they are useful models for disciplined delivery tracking.

## Visual and motion QA for generated images/video

Generated media needs targeted inspection beyond normal color and compression checks.

Inspect still frames at 100% and at the intended viewing size. Scrub video slowly, then watch once without pausing on the target device class. Many AI defects are only obvious during motion, and many "defects" disappear at normal mobile viewing size.

High-priority checks:

- Anatomy and faces: hands, fingers, teeth, eyes, ears, joints, limb count, asymmetric pupils, skin texture, hairline shimmer, identity drift, age mismatch, and face-morphing between frames.
- Text and symbols: product labels, UI text, subtitles burned into imagery, signs, legal copy, prices, dates, numbers, QR codes, logos, trademark shapes, and brand color placement. Use OCR when possible, but manually verify brand-critical text.
- Product truth: package geometry, materials, scale, ports/buttons, SKU variant, colorway, dosage/amount, included accessories, ingredients, claims, safety warnings, and compatibility details.
- Temporal continuity: subject identity, wardrobe, prop positions, lighting direction, shadows, reflections, weather, time of day, screen contents, labels, and geography across shots.
- Motion plausibility: foot sliding, floating objects, rubber limbs, non-causal physics, warped vehicles, rolling-shutter hallucinations, facial/lip deformation, camera path discontinuity, interpolation smear, and background crawling.
- Compositing and mixed-source edits: matte edges, grain/noise mismatch, perspective, lens blur, color temperature, contact shadows, reflection consistency, scale, eye lines, room tone, and source footage/generative insert seams.
- Avatar and lip-sync: mouth closure on bilabials, jaw timing, head/neck motion, eye blinks, gaze, breathing, hand gestures, language/accent match, uncanny stillness, and whether the avatar is disclosed/approved.

Production heuristic: accept small artifacts only when they are not visible at intended size, do not affect the subject/product/message, and will not become a meme or trust-breaker. Reject or revise any defect on a face, hand, product, logo, legal copy, price, medical/financial statement, or safety instruction.

## Audio, loudness, and intelligibility

Use the delivery spec first. If none exists, choose a target appropriate to the platform and document it as a production heuristic.

Documented facts:

- ITU-R BS.1770 specifies algorithms for measuring programme loudness and true-peak audio level.
- EBU R 128 recommends an average programme loudness of -23 LUFS and the use of Loudness Range and Maximum True Peak descriptors for audio signals.
- ATSC A/85 provides methods for measuring and controlling loudness for digital television and is referenced by the FCC CALM Act context for TV commercials in the United States.
- Netflix partner guidance for its own deliveries tells reviewers to use meters implementing ITU-R BS.1770 variants and describes how/when to flag loudness issues. Treat Netflix requirements as Netflix-specific, not universal.

Review:

- Dialogue intelligibility: listen on headphones, laptop speakers, and a phone speaker when the target is social/mobile. Flag when music/SFX mask key words.
- Sync: check lip sync at start, middle, and end; check that translated dubs preserve turn-taking and emotional timing. For avatars, inspect consonant closure, pauses, breaths, and facial expression alignment.
- Loudness: measure integrated loudness, true peak, and loudness range. Record the tool and target. Do not "normalize by ear" for a final delivery.
- Mix balance: narration, dialogue, SFX, music, ambience, and captions should support the message. Lower music under legal disclaimers, product claims, and instructions.
- Localization: verify numbers, units, names, pronunciations, cultural references, idioms, and reading pace in the target language. Back-translation can catch gross errors but is not a substitute for native review on high-stakes content.

## Captions, accessibility, and viewer safety

Accessibility is part of QA, not a last-minute export option.

Documented facts:

- WCAG 2.2 requires captions for prerecorded audio content in synchronized media at Success Criterion 1.2.2 and audio description or a media alternative at 1.2.3; Level AA includes audio description at 1.2.5 for prerecorded synchronized media.
- WCAG 2.2 Success Criterion 2.3.1 says content must not flash more than three times in any one-second period unless below the general and red flash thresholds.
- Netflix timed-text guidance is a platform-specific professional reference for subtitle timing, duration, forced narratives, and style. Use the actual client/platform guide when delivering elsewhere.

Check:

- Captions are present when required; every spoken word, meaningful sound cue, speaker ID, and off-screen speech is represented as appropriate.
- Captions are timed to speech, not late; do not cover essential UI/product/legal information; remain readable over the background; stay within safe margins; and are not burned in if the platform/client requires sidecar captions.
- Subtitle translation preserves meaning, tone, names, numbers, legal claims, humor, and safety instructions. Do not accept a localization solely because it "sounds fluent."
- Audio description or text alternative exists when important visual-only information is necessary for comprehension.
- Alt text or extended descriptions exist for still images when the delivery context requires accessible images.
- Flashing/strobing sequences are tested or avoided. For public-facing video, treat fast flashes, saturated red flashes, and high-contrast repetitive patterns as a safety risk, not just a style choice.

## Rights, provenance, and disclosure

Generated media QA must include origin and usage review. Do not present metadata as proof of truth; use it as one trust signal.

Documented facts:

- C2PA defines technical specifications for content provenance; a C2PA manifest can contain assertions, claims, signatures, and content bindings for media provenance.
- IPTC Digital Source Type includes `trainedAlgorithmicMedia` for media created using generative AI and `compositeWithTrainedAlgorithmicMedia` for composites containing generative-AI elements.
- Google Merchant Center documentation says not to remove embedded metadata tags such as IPTC `DigitalSourceType` from AI-generated images; relevant NewsCodes include `TrainedAlgorithmicMedia`. Verified 2026-07-10; platform requirements are volatile.
- YouTube Help says creators must disclose AI-generated or meaningfully AI-altered content that appears realistic through the AI-use setting, and disclosed content can be labeled for viewers. Verified 2026-07-10; platform requirements are volatile.
- FTC advertising guidance does not create an "AI exemption" from truthful advertising rules; endorsements, testimonials, and product claims still need appropriate disclosure and substantiation.

Review:

- Source rights: stock license, music license, font license, logo permission, brand assets, user-provided media permission, and commercial usage terms.
- Likeness/voice: consent for synthetic or cloned voices, avatars, face swaps, public figures, employees, customers, and minors.
- Claims: product performance, before/after imagery, health/financial/legal benefits, prices, availability, endorsements, awards, comparative claims, and environmental claims.
- Provenance metadata: preserve C2PA/IPTC/XMP where required; record if metadata was stripped by editing or platform export; do not claim "verified real" just because a credential exists.
- Disclosures: add human-visible AI/synthetic disclosure when the platform, law, client policy, or audience deception risk requires it. For realistic people/events, political content, news-like scenes, ads, and endorsements, escalate rather than guessing.
- Model/provider metadata: capture provider, model, date, prompt lineage, reference sources, post tools, and revision history. If exact model version is unavailable, state that limitation.

## Safety and policy review

Apply the relevant model, platform, legal, and client policies. Platform facts change; verify at delivery time for regulated or high-risk content.

Flag or reject:

- Deceptive realistic synthetic people, events, endorsements, evidence, or news scenes.
- Non-consensual intimate imagery, sexualized minors, harassment, hate, extremist persuasion, self-harm encouragement, or instructions for wrongdoing.
- Medical, financial, legal, political, housing, employment, or credit claims without substantiation and required disclaimers.
- Misrepresentation of a product's capabilities, certification, price, availability, environmental impact, or safety.
- Privacy leaks: faces, license plates, addresses, screens, documents, account details, patient/customer data, location traces, or hidden metadata.
- Localization harms: culturally offensive imagery, mistranslated warnings, wrong units, taboo gestures, or regionally illegal claims.

## Revision triage

Use severity to decide whether to accept, revise, regenerate, or escalate.

Critical: must not ship. Examples: wrong product/claim, missing rights or consent, deceptive synthetic endorsement, disallowed safety/policy content, inaccessible required captions, unsafe flashing, corrupted final file, unintelligible core dialogue, wrong legal copy, or platform-required disclosure missing.

Major: revise before normal release unless stakeholder explicitly accepts risk. Examples: visible face/hand/logo defect, lip-sync drift, continuity break that harms comprehension, caption timing failures, audio clipping, noisy mix, bad localization, wrong brand color on key asset, or noticeable compositing seam.

Minor: fix if efficient; can ship with documented acceptance for low-stakes drafts. Examples: small background artifact, slight caption line break awkwardness, non-critical metadata typo, tiny compression artifact not visible at target size.

Observation: record without blocking. Examples: "AI-generated background texture visible on pause only", "music slightly more energetic than brief but message remains clear."

Do not use "minor" for defects on faces, bodies, product labels, logos, safety warnings, prices, legal copy, public figures, or accessibility requirements.

## QA report format

Write reports that make action obvious:

- Asset ID, version, reviewer, date, target platform, intended use, and source package reviewed.
- Verdict: Pass, Pass with notes, Revise, Reject, or Escalate.
- Acceptance basis: brief/spec/policy documents used, with dates for volatile platform/provider facts.
- Automated checks: tools used and measured results.
- Manual checks: devices/viewers used and review coverage.
- Findings table: severity, timestamp/frame/region, issue, evidence, likely cause, recommended fix, owner, and retest requirement.
- Rights/provenance: source inventory, consent status, metadata status, and disclosure status.
- Residual risks: what could not be verified and who must approve.

For revision loops, require a delta review plus spot checks around changed areas and one full playback/viewing pass. Fixing one generated defect often creates another nearby.

## Deterministic report normalization helper

Use `scripts/normalize_qa_report.py` when a QA report needs a stable JSON handoff for automation, ticket creation, release gates, or producer review. The helper is Python 3.11+ and uses only the standard library. It validates the report shape, normalizes and sorts findings, summarizes severity counts, and computes a mechanical disposition from an explicit policy supplied in the report or via CLI.

Run it from a copied skill package or this repository:

```bash
python scripts/normalize_qa_report.py report.json
python scripts/normalize_qa_report.py report.json --policy '{"dispositions":{"critical":"reject","major":"hold","minor":"ready","observation":"ready"},"waivable_severities":["major"],"non_waivable_areas":["rights","accessibility","safety","policy"]}'
```

Exit codes:

- `0`: valid report and mechanical disposition is `ready`.
- `2`: validly parsed report that results in `hold` or `reject`, or a report with schema validation findings.
- `3`: operational parse/read/write failure, such as invalid JSON or an unreadable file.

The input JSON must include:

- `asset_id`: stable asset or delivery ID.
- `review`: object with `reviewer` and ISO-compatible `date`; include target platform, intended use, and source package when available.
- `policy`: explicit disposition rules. Provide `dispositions` mapping each severity (`critical`, `major`, `minor`, `observation`) to `ready`, `hold`, or `reject`. Optional `waivable_severities` lists severities that a supplied waiver may mechanically unblock. Optional `non_waivable_areas` is extended by the script to always include `rights`, `accessibility`, `safety`, and `policy`.
- `checks`: array of automated or manual checks with `id`, `status` (`pass`, `fail`, `not_applicable`, or `not_checked`), required `evidence_type`, and evidence detail.
- `findings`: array with `severity`, `area`, `issue`, `evidence_type`, `evidence_detail`, and a locator (`timecode`, `frame`, or `region`) whenever the evidence is an empirical observation or the issue is visual, audio, captions, accessibility, or safety related.

Evidence type must remain one of `documented_fact`, `empirical_observation`, or `heuristic`. Do not collapse these lanes during normalization: a documented platform requirement, a measured artifact, and a professional judgment have different authority.

Waivers are intentionally narrow. A blocking finding can be mechanically unblocked only when the policy allows that severity and the finding includes a waiver with non-empty `owner` and `reference`. The helper never waives rights, accessibility, safety, or policy findings, even if a report supplies a waiver.

The helper does not inspect media, judge subjective quality, verify claims, grant rights/accessibility/safety exceptions, or issue final approval. Its output includes `mechanical_only: true` and `final_approval: false`; a producer, reviewer, legal owner, accessibility owner, or release owner still has to make the actual acceptance decision.

Example minimal input:

```json
{
	"asset_id": "skincare-ad-v004",
	"review": {
		"reviewer": "QA Agent",
		"date": "2026-07-11T12:20:00Z",
		"target_platform": "paid social",
		"intended_use": "public product ad",
		"source_package": "delivery-package-v004"
	},
	"policy": {
		"dispositions": {
			"critical": "reject",
			"major": "hold",
			"minor": "ready",
			"observation": "ready"
		},
		"waivable_severities": ["major"],
		"non_waivable_areas": ["rights", "accessibility", "safety", "policy"]
	},
	"checks": [
		{
			"id": "claim-substantiation",
			"status": "fail",
			"evidence_type": "documented_fact",
			"evidence_detail": "Product fact sheet does not approve disease-treatment claims."
		}
	],
	"findings": [
		{
			"severity": "critical",
			"area": "policy",
			"issue": "Overlay makes an unsupported eczema treatment claim.",
			"evidence_type": "documented_fact",
			"evidence_detail": "Approved product facts allow dry-skin support only; the video says 'repairs eczema overnight'.",
			"timecode": "00:06.000",
			"recommended_fix": "Replace with approved copy and send revised ad through legal and QA review.",
			"owner": "Legal review",
			"retest_required": true
		}
	]
}
```

## Test matrix by deliverable

| Deliverable | Minimum QA focus |
|---|---|
| Still image | Brief fit, dimensions, crop/safe area, product/logo/text accuracy, anatomy, rights, metadata/provenance, platform disclosure, alt text if needed |
| Social clip | Hook timing, platform aspect/duration, mobile readability, captions, music/dialogue balance, generated motion artifacts, flashes, thumbnail/frame hold, disclosure |
| Explainer | Factual accuracy, script-to-visual alignment, narration intelligibility, captions/transcript, diagrams/text, pacing, source citations if factual, accessibility |
| Product ad | Product truth, legal/claim substantiation, packshot fidelity, price/offer accuracy, brand rules, CTA, rights, synthetic endorsements, platform ad policy |
| Avatar/spokesperson | Consent, identity/voice approval, lip sync, gaze/gesture naturalness, disclosure, language/accent, uncanny artifacts, claims |
| Localization/dub | Translation accuracy, cultural fit, units/names, subtitle timing, dub sync, voice approval, local legal claims, on-screen text replacement |
| Mixed-source edit | Source rights, continuity, color/grain match, compositing seams, provenance per ingredient, edit rhythm, captions/audio mix |
| Broadcast/premium master | Client spec, automated QC, loudness, color/HDR, captions/subtitles, PSE/flashing, metadata, IMF/AS-11 or client package rules where applicable |

## Example: QA report for a 15-second generated product ad

Context: 15 s vertical skincare ad for Instagram Reels. Approved brief says "show the blue 50 ml bottle, no medical claims, CTA: Shop the summer set." Source package includes generated video, brand logo, music license, product facts, and prompt metadata.

Acceptance basis: 1080x1920 vertical, 15 s max, brand color guide, product fact sheet, FTC truthful-advertising posture, platform synthetic-media disclosure checked on delivery date.

Findings:

| Severity | Time/region | Issue | Evidence | Recommended fix |
|---|---|---|---|---|
| Critical | 00:06 text overlay | Unsupported claim "repairs eczema overnight" | Product facts only allow "supports dry skin barrier"; health claim not approved | Replace with approved claim; legal review revised copy |
| Major | 00:08 bottle label | AI label reads "HYDRATlON" with wrong letterform | Manual inspection and OCR mismatch | Regenerate packshot from locked product render or composite approved label |
| Major | Full mix | Music masks CTA | Phone speaker playback; last three words hard to understand | Duck music -6 dB under CTA and retest intelligibility |
| Minor | 00:03 background | Small warped leaf visible on pause | Not visible at normal playback | Accept if no other render is needed |

Verdict: Reject until claim and product label are fixed; retest final playback, captions, loudness, and disclosure after revision.

Why this example is structured this way: the critical issue is legal/claim risk, not visual polish. A visually beautiful ad with a false product claim fails QA.

## Example: QA plan for an avatar localization batch

Context: English training video localized into Spanish, French, and Japanese with synthetic avatar dubbing. Target is internal LMS, not public ads. The client provided consent for the avatar performer and requires captions.

Workflow:

1. Verify consent and allowed languages for the avatar/voice before watching outputs.
2. For each locale, compare translated script to approved source for meaning, warnings, numbers, product names, and URLs.
3. Watch the dub once without captions for naturalness and intelligibility; watch again with captions for timing and line breaks.
4. Spot-check lip sync at dense consonant passages and at the final 20 seconds, where drift often accumulates.
5. Confirm captions include speaker changes and meaningful non-speech audio if relevant.
6. Record locale-specific issues separately; do not let a pass in one language imply pass in another.

Expected failure modes: avatar mouth over-opens on Japanese vowels, Spanish text overruns caption safe area, French dub starts 300 ms late after a pause, translated safety warning changes "must" to "may."

Verdict rule: a locale with mistranslated safety instructions is Critical even if the video file is technically perfect.

## Example: QA checklist for a mixed-source explainer

Context: A 60 s explainer combines AI-generated diagrams, licensed stock footage, generated narration, and a human-edited timeline.

Review:

- Brief conformance: each beat in the approved script appears in order; no unsupported statistic was added by a generated diagram.
- Source ledger: stock clip license covers the distribution channel; AI diagrams are marked as generated; narration provider and voice are recorded.
- Visual continuity: diagram labels match narration; colors mean the same thing across scenes; no arrows point to impossible flows.
- Audio: narration is clean, music is under speech, no edits cut breaths unnaturally, integrated loudness target is documented.
- Captions/accessibility: captions match final narration, diagram-only information is described in narration or transcript, no flashing transitions exceed safe thresholds.
- Final package: export matches platform resolution/duration, filename/version is correct, and the QA report lists residual factual sources that were not independently verified.

Pass condition: all factual/statistical claims trace to approved source material, and no generated visual introduces a new unsupported claim.

## Source notes

- W3C, [WCAG 2.2](https://www.w3.org/TR/WCAG22/), especially synchronized media and flashing success criteria. Verified 2026-07-10.
- W3C, [Understanding SC 2.3.1 Three Flashes or Below Threshold](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html). Verified 2026-07-10.
- EBU, [R 128 Loudness normalisation and permitted maximum level of audio signals](https://tech.ebu.ch/publications/r128). Verified 2026-07-10.
- ITU, [Recommendation ITU-R BS.1770](https://www.itu.int/rec/R-REC-BS.1770). Verified 2026-07-10.
- ATSC, [A/85 Techniques for Establishing and Maintaining Audio Loudness for Digital Television](https://www.atsc.org/atsc-documents/a85-techniques-for-establishing-and-maintaining-audio-loudness-for-digital-television/), and FCC, [CALM Act overview](https://www.fcc.gov/enforcement/areas/sound-volume-commercials-calm-act). Verified 2026-07-10.
- C2PA, [Technical Specification](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html). Verified 2026-07-10.
- IPTC, [Digital Source Type NewsCodes](https://cv.iptc.org/newscodes/digitalsourcetype/) and [Photo Metadata Standard](https://iptc.org/standards/photo-metadata/iptc-standard/). Verified 2026-07-10.
- Google Merchant Center Help, [AI-generated content](https://support.google.com/merchants/answer/14743464). Platform fact verified 2026-07-10.
- YouTube Help, [Disclosing use of GenAI content](https://support.google.com/youtube/answer/14328491). Platform fact verified 2026-07-10.
- FTC, [Advertisement Endorsements](https://www.ftc.gov/news-events/topics/truth-advertising/advertisement-endorsements) and [Crackdown on deceptive AI claims and schemes](https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes). Verified 2026-07-10.
- SMPTE, [ST 2067 Interoperable Master Format](https://www.smpte.org/standards/st2067). Verified 2026-07-10.
- Netflix Partner Help Center, [Best Practices: Technical QC and Checks for Branded IMP Delivery](https://partnerhelp.netflixstudios.com/hc/en-us/articles/6284290824211-Best-Practices-Technical-QC-and-Checks-for-Branded-IMP-Delivery), [Timed Text Style Guide: General Requirements](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements), and [Subtitle Timing Guidelines](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines). Platform-specific references verified 2026-07-10.
- NIST, [AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) and [GenAI evaluation program](https://ai-challenges.nist.gov/genai). Verified 2026-07-10.
- Lin et al., [“Building a Precise Video Language with Human-AI Oversight”](https://arxiv.org/abs/2604.21718), structured video-language and critique quality findings, checked 2026-07-14.
