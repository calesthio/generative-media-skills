---
name: asset-continuity-management
description: Provider-independent asset continuity and version management for generated-media production. Use when an agent must track generated or reference assets, prompts, seeds, model/tool versions, manifests, approvals, edit decisions, derivatives, localization variants, metadata/provenance, and continuity QA across image, video, audio, avatar, product-ad, social, explainer, or film-style pipelines.
---

# Asset continuity management

Use this skill to keep generated-media projects reproducible, reviewable, and visually/aurally consistent across many assets, revisions, tools, and deliverables. Treat continuity as a production control system: every asset gets an ID, every change becomes an event, every derivative points back to its sources, and every continuity-critical choice is captured before more generation compounds the mistake.

This skill is provider-independent. Do not assume any particular generator exposes seeds, request IDs, input hashes, content credentials, prompt logs, or model versions. Capture them when available; explicitly record `unknown`, `not_provided`, or `not_applicable` when they are not.

## Core rule

Never manage continuity by memory, filenames alone, or chat history alone. Maintain a project-local continuity package with three living records:

1. `asset_manifest`: one row/object per file or generated unit.
2. `source_reference_ledger`: one row/object per source, reference, prompt, seed, model/tool context, approval, and rights/usage constraint.
3. `continuity_bible`: canonical descriptions and locked references for characters, products, locations, wardrobe, brand, voice, music, captions, and recurring design motifs.

If the host pipeline already has artifact schemas, map these records into the native schemas rather than inventing parallel files. If no schema exists, use structured JSON, YAML, CSV, or tables that can be diffed and reviewed.

## What to record first

Before generating or editing media, create the minimum continuity control plane:

- Project ID, client/title, date, owner, delivery platforms, target languages/locales, and review contacts.
- Asset ID pattern and file naming pattern.
- Storage locations for working files, approved masters, review exports, source references, and rejected/archived variants.
- Approval policy: who can approve character likeness, product accuracy, brand/legal claims, accessibility, voice, localization, and final delivery.
- Escalation triggers for legal/client review. Do not give legal advice; pause for counsel or client approval when rights, likeness, trademark, claims substantiation, licensed references, synthetic voice/face consent, regulated products, political/medical/financial claims, or platform disclosure obligations are in scope.

Recommended ID pattern:

```text
<project>-<type>-<scene_or_unit>-<role>-v<major>.<minor>
```

Examples:

- `aurora-img-s03-heroProduct-v1.0`
- `aurora-vid-s05-brollCity-v2.1`
- `aurora-aud-narration-enUS-v1.3`
- `aurora-cap-final-esMX-v1.0`

Use IDs as stable production identifiers. Filenames may change for delivery, but the asset ID should remain traceable through manifests, review notes, embedded metadata when possible, and final handoff.

## Asset manifest fields

For every asset, capture as many of these fields as apply. A strong manifest favors explicit unknowns over blank cells.

```yaml
asset_id: aurora-img-s03-heroProduct-v1.0
status: draft|candidate|approved|rejected|superseded|delivered
asset_type: image|video|audio|music|sfx|voice|avatar|caption|project-file|prompt|reference|composite|delivery
role: hero_product|character_ref|location_plate|wardrobe_ref|voice_take|music_bed|caption_track|final_master
scene_ids: [s03]
shot_ids: [s03_sh02]
file_path: projects/aurora/assets/images/aurora-img-s03-heroProduct-v1.0.png
checksum_sha256: "<hash after write>"
byte_size: 4821138
duration_or_dimensions: "2048x1152"
format_codec_profile: "PNG; sRGB" # or "MP4 H.264 High, AAC 48kHz"
colorspace_loudness_or_fps: "sRGB" # or "23.976 fps", "-16 LUFS integrated"
created_at_utc: "2026-07-10T18:41:00Z"
created_by: agent|human|vendor|tool
tool_provider: "not_provided|provider name"
tool_name: "not_provided|tool name"
model_or_engine: "not_provided|model id/version"
model_version_verified_at: "2026-07-10" # volatile; re-check at production time
request_or_job_id: "not_provided"
seed: "not_provided"
parameters:
  aspect_ratio: "16:9"
  guidance: "not_provided"
prompt_id: prompt-s03-heroProduct-v1.0
source_ids: [src-product-packshot-v1, ref-brand-board-v2]
parent_asset_ids: []
derived_asset_ids: [aurora-img-s03-heroProduct-v1.1]
c2pa_or_content_credential: present|absent|external|not_checked
embedded_metadata_checked: true
rights_usage_notes: "Client-owned packshot reference; no third-party logo beyond approved brand."
review_notes: "Approved for product shape, color, logo placement."
approval_record_ids: [approval-brand-2026-07-10-01]
supersedes: null
superseded_by: aurora-img-s03-heroProduct-v1.1
retention: keep_master|keep_review|archive|delete_after_delivery
```

Do not rely on generated filenames from providers. Rename or copy outputs into the project storage convention, then compute a checksum and record the original provider path or URL separately if it matters.

## Source and reference ledger

The source/reference ledger is the evidence trail. It should answer: "What did this asset depend on, what did we ask for, what did the tool return, and what constraints apply?"

Capture:

- `source_id`: stable ID for each reference, source clip, brand file, script, storyboard, prompt, negative prompt, seed bundle, voice sample, music reference, font, LUT, product spec, character sheet, or location reference.
- Origin: user-provided, generated in-project, licensed stock, public-domain, client-owned, commissioned, captured, synthetic, unknown.
- Custody: who supplied it, when, where it is stored, checksum, and whether the original is preserved.
- Rights and consent notes: usage scope, territory, duration, likeness/voice permissions, trademark/brand restrictions, and "needs counsel/client confirmation" flags.
- Generation context: provider/tool/model/version, seed, request ID, endpoint or UI, prompt text, system/style constraints, reference images/audio/video, parameters, safety or policy changes, and date verified.
- Continuity tags: character, product, location, wardrobe, brand, language, shot, sequence, campaign, platform.
- Approval events and rejection reasons.

Provider/platform rules are volatile. Re-check production-time rules for disclosure, content credentials, watermarking, model availability, pricing, supported inputs, retention, commercial-use terms, and safety policies when a project will ship publicly or commercially.

## Continuity bible

Create canonical entries for anything that must remain consistent. Each entry should contain the locked description, approved reference assets, banned variations, and QA checklist.

Use entries like these:

```yaml
character:
  id: char-maya-v1
  canonical_description: "Late-30s field engineer, warm brown skin, shoulder-length black curls, amber safety glasses, navy utility jacket with orange stitching."
  locked_reference_assets: [maya-turnaround-v1, maya-face-close-v2, maya-wardrobe-v1]
  invariants:
    - face shape and hair volume
    - amber safety glasses
    - navy/orange jacket
    - calm, competent posture
  allowed_variations:
    - jacket may be zipped or open
    - helmet on/off depending on scene safety
  forbidden_variations:
    - different hair color
    - logo on jacket unless brand-approved
    - age shift younger/older than brief
  approval_required_for:
    - face regeneration
    - wardrobe redesign
    - synthetic voice or avatar use
```

```yaml
product:
  id: product-orbit-bottle-v1
  canonical_description: "Matte white insulated bottle, rounded square body, teal cap, vertical ORBIT wordmark centered on front."
  locked_reference_assets: [orbit-packshot-front-v1, orbit-packshot-side-v1]
  invariants:
    - silhouette and cap color
    - exact approved wordmark placement
    - no invented claims, certifications, or UI labels
  forbidden_variations:
    - misspelled logo
    - unapproved ingredient/feature claims
    - altered capacity or materials
```

Also create entries for:

- Locations and sets: geography, era, weather, signage, layout, props, time of day.
- Wardrobe and styling: garments, colors, accessories, makeup, hair, continuity by scene.
- Brand system: logo usage, colors, typography, UI, tone, claims, disclaimers, lower thirds.
- Audio identity: narrator voice, pronunciation dictionary, music motifs, sound design palette, loudness target.
- Avatar identity: avatar ID, consent source, voice ID, language constraints, gesture style, lip-sync notes.
- Caption/localization style: reading speed, speaker labels, subtitle format, terminology glossary, do-not-translate terms.

## Scene and shot linkage

Every production unit should link scene/shot intent to assets and edit decisions:

```yaml
scene_id: s03
shot_id: s03_sh02
story_function: "Reveal product solving the setup problem."
continuity_requirements:
  character_ids: [char-maya-v1]
  product_ids: [product-orbit-bottle-v1]
  location_ids: [loc-lab-v1]
  brand_ids: [brand-orbit-v1]
required_assets:
  image: [aurora-img-s03-heroProduct-v1.0]
  video: [aurora-vid-s03-productPushIn-v1.0]
  audio: [aurora-aud-s03-vo-enUS-v1.0]
edit_decisions:
  - cut_in: "00:00:18.500"
  - cut_out: "00:00:23.000"
  - transition: "match cut from blueprint line to bottle edge"
  - caption_asset_id: aurora-cap-master-enUS-v1.0
qa:
  - product wordmark readable and correct
  - character glasses remain amber
  - no extra invented text in background
```

For film-style or multi-shot video generation, link generated clips to the beat they cover. If a generated clip contains multiple internal shots, describe the internal shots with approximate time ranges and note any continuity breaks inside the clip.

## Versioning and regeneration controls

Use semantic production versions:

- `v0.x`: exploration, not approved.
- `v1.0`: first approved candidate for the unit.
- `v1.x`: minor fixes that preserve the approved concept, composition, and identity.
- `v2.0`: material change to prompt, model, seed, reference, edit intent, identity, product design, or approval basis.

Before regenerating, decide whether the goal is:

1. **Repair**: preserve identity/composition; adjust defects only.
2. **Variant**: same approved concept; explore controlled alternatives.
3. **Replacement**: new creative direction or provider/model path.

Regeneration checklist:

- Lock the parent asset ID, prompt ID, seed, references, model/tool version, and continuity bible entries.
- State which fields may change and which must not change.
- Use the same seed only if the provider supports it and seed behavior is documented or observed for that provider. Seeds are not a guarantee across model versions, providers, or changed reference inputs.
- If model/tool version changed, record it as a material change even when the prompt is identical.
- Keep rejected outputs when they explain a decision, contain a useful partial element, or document a client/legal rejection. Otherwise archive according to the retention policy.

## Prompt and decision logs

Keep prompt records as first-class assets, not throwaway chat snippets.

```yaml
prompt_id: prompt-s03-productPushIn-v2.0
target_asset_role: video product push-in
scene_ids: [s03]
prompt_text: |
  A controlled studio push-in toward the matte white Orbit bottle...
negative_prompt: |
  misspelled logo, extra labels, altered cap color, warped bottle shape...
continuity_constraints:
  character_ids: []
  product_ids: [product-orbit-bottle-v1]
  location_ids: [loc-studio-v1]
references:
  - source_id: orbit-packshot-front-v1
    purpose: "shape/logo lock"
  - source_id: brand-board-v2
    purpose: "color and lighting"
parameters:
  aspect_ratio: "16:9"
  duration: "5s"
  seed: "123456789"
model_context:
  provider: "provider name or not_provided"
  model: "model name/version or not_provided"
  version_verified_at: "2026-07-10"
change_reason: "v2 uses approved packshot reference after v1 distorted cap."
```

For user-visible decisions, keep an append-only decision log. Do not silently mutate old decisions after a provider/model/reference/music/voice/runtime/approval choice changes. Append a revised decision with the same subject so review surfaces the current choice and the superseded choice.

## Edit decision tracking

Edit decisions are continuity events. Track:

- Source asset IDs, in/out timecodes, retimes, crops, reframes, stabilization, interpolation, color changes, upscales, denoise, audio processing, and caption burn-ins.
- Transform chain: original -> normalized mezzanine -> edit proxy -> review export -> approved master -> platform derivative.
- Rationale for cuts that hide continuity defects, such as cropping out malformed hands, trimming before a logo warps, or covering lip-sync drift with B-roll.
- Audio changes: voice take selection, pronunciation fixes, music edit points, ducking, loudness normalization, stems, and SFX placement.
- Caption changes: language, timing, speaker labels, translation basis, reading-speed edits, and whether captions are sidecar, embedded, or burned in.

If an edit changes meaning, claims, identity, or legal context, mark it as a new version and route it through the relevant approval gate.

## File naming and storage

Use boring, sortable names:

```text
<project>_<asset-id>_<locale-or-platform>_<status>_<yyyymmdd>.<ext>
```

Example:

```text
aurora_aurora-vid-s03-productPushIn-v2.0_master_approved_20260710.mp4
```

Rules:

- Prefer lowercase letters, digits, hyphens, underscores, and ISO-like dates.
- Avoid spaces, ambiguous words like `final_final`, provider download names, and destructive overwrites.
- Keep originals immutable. Write derivatives as new files.
- Store project files, exports, prompts, references, captions, and manifests in predictable directories.
- Compute checksums for sources, masters, and approved candidates.
- Keep a custody note when files move between local disk, cloud storage, client DAM/MAM, review tools, or delivery portals.

For preservation-minded handoff, use open or widely supported formats when practical, and keep masters separate from platform transcodes. The Library of Congress Recommended Formats Statement is a useful reference for format sustainability, but delivery specs and client requirements remain binding.

## Metadata and provenance

Preserve metadata unless there is a privacy, safety, legal, or platform reason to remove it. When metadata is stripped by a tool or platform, record that event in the manifest.

Use these standards as guidance:

- C2PA Content Credentials: Use when the workflow supports cryptographically verifiable provenance. C2PA manifests combine assertions, a claim, and a claim signature, and can describe actions, ingredients, content bindings, and AI disclosure. C2PA is a trust signal, not a creative continuity bible and not a legal clearance substitute.
- IPTC Photo Metadata: Use for embedded descriptive, administrative, and rights metadata in images where supported. For synthetic media, IPTC Digital Source Type values such as `trainedAlgorithmicMedia` identify media created using generative AI.
- PREMIS: Use its preservation concepts-Objects, Events, Rights, Agents-as a mental model for custody and change logs.
- PBCore: Use as an audiovisual metadata model when sharing or archiving complex audio/video collections across systems.
- WebVTT/FADGI: Treat caption/subtitle files as derivative assets. Use WebVTT for timed-text structure. When delivery uses sidecar WebVTT, FADGI draft guidance can inform embedded administrative/provenance fields such as type, language, responsible party, media identifier, originating file, file creator, and file creation date; keep version history, QC notes, approval status, and lineage in the project manifest/ledger.

Practical metadata checklist:

- Check whether C2PA/content credentials are present, absent, external, invalid, or stripped.
- Preserve source embedded metadata in the immutable original when allowed.
- Record AI/synthetic disclosure fields when supported by file type/tool/client policy.
- Do not embed private prompt text, personal data, exact location, internal client notes, or confidential source details into public files without approval.
- For final handoff, include a human-readable provenance summary even when embedded metadata exists.

## Localization and derivative tracking

Treat each localized or platform-specific version as a derivative with explicit lineage:

```yaml
asset_id: aurora-delivery-tiktok-esMX-v1.0
parent_asset_ids: [aurora-master-16x9-enUS-v1.0]
variant_type: localization+platform_reframe
locale: es-MX
platform: TikTok
changes:
  - translated captions from approved en-US captions
  - reframed 16:9 master to 9:16
  - replaced end card legal line with approved Spanish version
approvals_required:
  - localization reviewer
  - brand/legal for claims and disclaimer
continuity_risks:
  - cropped product wordmark in vertical frame
  - subtitle covers required on-pack text
```

For localization, maintain:

- Locale code, translator/reviewer, translation basis, terminology glossary, pronunciation dictionary, do-not-translate terms, and approved legal/claim wording.
- Separate asset IDs for dubbed voice, translated captions, localized graphics, platform reframes, and regional masters.
- Timecode mapping when translated speech changes duration.
- Accessibility checks for captions/subtitles, including timing, completeness, readability, speaker labels, and placement.

## Continuity QA

Run continuity QA before approval gates and again before final delivery. Do not wait until the final render to find identity drift.

Check at four levels:

1. **Asset-level**: file opens, expected format, checksum recorded, metadata/provenance checked, prompt/model/seed captured, no obvious generation defects.
2. **Continuity-level**: character/product/location/wardrobe/brand/voice/caption invariants match the continuity bible.
3. **Scene-level**: shot order, screen direction, time of day, props, wardrobe, audio perspective, lighting, and story logic remain consistent.
4. **Derivative-level**: localization, platform reframe, compression, captions, overlays, and metadata preserve required meaning and approvals.

Mode-specific QA:

- Image: identity consistency, hands/faces/logos/text, aspect ratio, color profile, embedded metadata, forbidden visual claims.
- Video: temporal identity drift, object permanence, motion continuity, flicker, warped text/logos, frame rate, audio sync, shot-to-shot geography.
- Audio/music/SFX: voice identity, pronunciation, clipping, loudness, rights/usage notes, stem lineage, music edit continuity.
- Avatar/lip-sync: consent/approval, voice/avatar ID, lip sync, gestures, gaze, wardrobe, background, disclosure requirements.
- Product ads: exact product shape, pack copy, claims, disclaimers, logo usage, regulatory/client review.
- Social derivatives: platform crop safety, caption safe areas, cover frame, burned-in text, disclosure labels, music licensing, metadata stripping.
- Explainers: factual claims, diagrams, labels, VO/caption agreement, source citations, localization of technical terms.
- Film-style pipelines: screen direction, eyelines, continuity of time/weather/wardrobe/props, editorial geography, color grade consistency.

Use visual contact sheets and side-by-side comparisons for recurring entities. When reviewing video, sample key frames and scene boundaries; for generated clips, also inspect frames near the middle because drift often appears after the opening image.

## Review handoff

A useful review package contains:

- Current asset manifest and source/reference ledger.
- Continuity bible with locked references.
- Contact sheet or review board grouped by character/product/location/scene.
- Change log since last review.
- Open questions and escalation flags.
- Low-resolution review exports plus paths/checksums for masters.
- Approval form or table with asset IDs, reviewer, decision, date, notes, and conditions.
- Known limitations: unavailable seeds, provider-hidden model version, stripped metadata, unresolved rights questions, platform rules to re-check.

Ask reviewers to comment using asset IDs and timecodes, not screenshots alone. Convert review comments into manifest or decision-log events.

## Example: product ad with image, video, audio, and social variants

Example production intent: Create a 20-second product ad for a client-owned bottle with 16:9 master, 9:16 social cutdown, English VO, Spanish captions, and generated product B-roll.

Example approach:

1. Create continuity bible entries for `product-orbit-bottle-v1`, `brand-orbit-v1`, and `voice-calm-enUS-v1`.
2. Ingest client packshots as `src-orbit-packshot-front-v1` and `src-orbit-packshot-side-v1`; compute checksums and mark origin as client-provided.
3. Generate a hero image and product-motion clip. Capture prompt ID, source IDs, model/tool version when available, request ID, seed if provided, and date verified.
4. QA for product silhouette, teal cap, exact wordmark, no invented claims, no deformed text.
5. Approve `aurora-vid-s03-productPushIn-v1.0` only after product/brand review.
6. Create `aurora-master-16x9-enUS-v1.0`, then derive `aurora-delivery-tiktok-enUS-v1.0` and `aurora-delivery-tiktok-esMX-v1.0`; each derivative points to the master and records crop/caption/localization changes.
7. Handoff includes the manifest, continuity bible, source ledger, final masters, caption files, platform derivatives, and unresolved risk notes.

Example QA finding:

```yaml
finding_id: qa-s03-002
asset_id: aurora-vid-s03-productPushIn-v1.0
severity: critical
finding: "The ORBIT wordmark changes to OR8IT for frames 74-96."
action: "Reject clip; regenerate or mask with approved packshot overlay."
continuity_bible_refs: [product-orbit-bottle-v1, brand-orbit-v1]
approval_needed: brand
```

## Example: character continuity across an explainer

Example production intent: Generate a 90-second explainer with one recurring host character across eight scenes.

Example controls:

- Generate and approve a character turnaround before scene assets.
- Store the approved front, side, expression, and wardrobe references as locked assets.
- Use the same `character_id` in every scene/shot record.
- Require a QA pass that compares each scene frame against the locked references.
- Treat any face, age, hair, skin tone, wardrobe, or body-proportion drift as a continuity defect, not merely a style preference.

Example manifest note:

```yaml
asset_id: nebula-img-s06-hostWhiteboard-v1.0
parent_asset_ids: [nebula-img-character-turnaround-v1.0]
prompt_id: prompt-s06-hostWhiteboard-v1.0
continuity_tags: [char-host-v1, wardrobe-host-jacket-v1, loc-whiteboard-v1]
qa_status: rejected
qa_notes:
  - "Hair length shortened materially from locked reference."
  - "Jacket changed from forest green to black."
regeneration_control:
  mode: repair
  preserve:
    - face shape
    - forest green jacket
    - shoulder-length hair
  may_change:
    - whiteboard diagram content
```

## Safety, rights, and governance boundaries

Escalate instead of improvising when:

- A reference asset may be copyrighted, trademarked, confidential, personal data, or outside the agreed license.
- A person's likeness, voice, or avatar is synthesized, face-swapped, cloned, localized, or used in a new context.
- A product ad contains performance, health, financial, legal, environmental, safety, or comparative claims.
- Synthetic-media disclosure, watermarking, platform labeling, or political-ad rules may apply.
- Metadata contains private prompts, geolocation, unreleased product details, client secrets, or personal data.
- The client asks to remove provenance/disclosure in a context where policy, contract, or law may require it.

NIST's AI RMF and Generative AI Profile are voluntary risk-management references, not production law. Use their governance posture-map risks, measure/monitor controls, manage residual risk, and document decisions-to structure escalation and review.

## Sources and verification notes

Factual grounding consulted and verified on 2026-07-10:

- C2PA Technical Specification 2.4 and Implementation Guidance: provenance manifests, assertions, claims, signatures, ingredients, actions, content binding, AI disclosure, and digital source type guidance. https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html and https://spec.c2pa.org/specifications/specifications/2.4/guidance/Guidance.html
- IPTC Photo Metadata Standard 2025.1 and IPTC Digital Source Type NewsCodes: administrative/descriptive/rights metadata and synthetic-media source type values. https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata and https://cv.iptc.org/newscodes/digitalsourcetype/
- NIST AI RMF Generative AI Profile, NIST AI 600-1, July 2024: voluntary GenAI risk-management companion to AI RMF 1.0. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- PREMIS Data Dictionary v3.0, Library of Congress: preservation metadata model of Objects, Events, Rights, and Agents. https://www.loc.gov/standards/premis/v3/
- PBCore: audiovisual metadata standard for organizing and exchanging information about audiovisual assets. https://pbcore.org/what-is-pbcore
- Library of Congress Recommended Formats Statement 2025-2026: format sustainability and accessibility considerations. https://www.loc.gov/preservation/resources/rfs/
- W3C WebVTT latest published version and FADGI draft WebVTT metadata embedding guidance: timed text tracks and sidecar WebVTT metadata fields. https://www.w3.org/TR/webvtt1/ and https://www.digitizationguidelines.gov/guidelines/FADGI_WebVTT_embed_guidelines_v0.1_2024-04-18.pdf

Volatile facts to re-check at production time: provider model IDs/versions, seed behavior, supported metadata/content-credential formats, platform synthetic-media disclosure rules, watermarking behavior, retention policies, pricing, regional availability, upload/download file transformations, and commercial-use terms.
