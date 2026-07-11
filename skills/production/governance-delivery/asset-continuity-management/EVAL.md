# Evaluation: asset-continuity-management

Use this file to evaluate whether an agent correctly used the `asset-continuity-management` skill. The evaluated agent should receive only the user task and `SKILL.md`, never this file.

Score the response for production usefulness, factual grounding, continuity discipline, and escalation behavior. Strong answers should adapt the skill to the specific production context rather than reciting generic metadata advice.

## Knowledge questions

### 1. What are the three living records the skill expects for generated-media continuity?

Expected answer:

- `asset_manifest`
- `source_reference_ledger`
- `continuity_bible`

Required points:

- Explains that the asset manifest tracks files/generated units.
- Explains that the source/reference ledger tracks inputs, prompts, generation context, approvals, rights, and custody.
- Explains that the continuity bible locks canonical descriptions/references/invariants for recurring entities such as characters, products, locations, wardrobe, brand, voice, captions, and audio identity.

Penalize:

- Treating filenames or chat history as sufficient.
- Omitting source/reference or approval tracking.
- Presenting the continuity bible as optional for recurring identity-critical work.

### 2. What should an agent do when a provider does not expose seed, model version, request ID, or C2PA metadata?

Expected answer:

- Record explicit values such as `not_provided`, `not_checked`, `unknown`, or `not_applicable`.
- Continue capturing available context: provider/tool name, prompt, references, parameters, date verified, output checksum, and review notes.
- Avoid claiming reproducibility or provenance that is not actually supported.

Critical failures:

- Inventing seeds, model versions, or request IDs.
- Saying continuity is impossible without seeds.
- Treating missing C2PA metadata as proof an asset is not synthetic.

### 3. How should C2PA and IPTC be used in this workflow?

Expected answer:

- C2PA Content Credentials are useful trust/provenance signals with manifests, assertions, claims, signatures, content bindings, ingredients, actions, and AI disclosure where supported.
- IPTC Photo Metadata can carry descriptive, administrative, rights, and synthetic-media source fields for images; Digital Source Type can identify AI-generated/synthetic media where supported.
- Neither C2PA nor IPTC replaces the project manifest, continuity bible, rights clearance, or legal/client review.

Penalize:

- Claiming C2PA is mandatory for all assets.
- Claiming C2PA proves a piece of media is "true."
- Treating IPTC fields as sufficient for multi-asset video production lineage.

### 4. What versioning distinction should be made between repair, variant, and replacement?

Expected answer:

- Repair preserves approved identity/composition and fixes defects only.
- Variant explores controlled alternatives under the same approved concept.
- Replacement changes creative direction, provider/model path, references, identity, product design, or approval basis.
- Material changes should become a major version; minor fixes that preserve approval basis can be minor versions.

Critical failures:

- Regenerating identity-critical assets without preserving parent IDs/references.
- Treating model/version changes as irrelevant.
- Overwriting the prior approved file.

### 5. What is a derivative lineage requirement for localization and platform variants?

Expected answer:

- Each localized/platform-specific output gets its own asset ID and points to parent asset IDs.
- The record includes locale, platform, variant type, changes made, approvals required, continuity risks, and caption/voice/translation basis.
- Localized claims/disclaimers, terminology, captions, dubbing duration, and crop-safe areas should be reviewed.

Penalize:

- Treating translated captions or vertical reframes as the same asset without lineage.
- Omitting localization reviewer or legal/brand approval where claims/disclaimers are translated.

## Production-decision questions

### 6. Scenario: A client asks for a product ad using an AI-generated bottle. The generated bottle looks good, but the label text is slightly wrong in a few frames. What should the agent decide?

Expected decision:

- Mark the asset as rejected or conditionally rejected for product/brand continuity.
- Create a QA finding with asset ID, timecode/frame range, severity, continuity bible references, and required action.
- Regenerate in repair mode with product references locked, or propose masking/overlaying the approved packshot if appropriate.
- Route brand/client approval before using it in a final ad.

Strong reasoning:

- Product labels and claims are not cosmetic; they can affect brand/legal accuracy.
- The defect should be traceable in manifest and review notes.

Critical failures:

- Cropping or ignoring the defect without logging it.
- Calling it acceptable because "AI text is often imperfect."
- Inventing or altering product claims.

### 7. Scenario: A generated film-style sequence has the same character across five shots, but hair length and jacket color drift between shots. What should the agent do?

Expected decision:

- Treat it as continuity drift.
- Compare against locked character/wardrobe references.
- Log findings by shot/asset/timecode.
- Regenerate or repair affected shots with explicit preserve/change controls.
- Use a contact sheet or side-by-side review before approval.

Penalize:

- Describing it as creative variation when the continuity bible locks those features.
- Fixing only the final render without updating source lineage.

### 8. Scenario: A provider output includes a content credential, but the project manifest lacks prompt, source references, approvals, and edit lineage. Is the handoff complete?

Expected decision:

- No. Content credentials are helpful provenance, but they do not replace project-level continuity management.
- The agent should complete the manifest, ledger, continuity bible, edit decisions, approvals, and derivative tracking.

Critical failures:

- Saying C2PA alone is sufficient for production continuity.
- Ignoring approvals and source/reference rights.

### 9. Scenario: The user asks to remove all metadata from final masters before public upload. What should the agent do?

Expected decision:

- Ask why and identify whether privacy, confidentiality, platform delivery, or policy/legal requirements are driving the request.
- Preserve immutable originals and an internal provenance record.
- Escalate to client/counsel when disclosure, synthetic media, political/regulatory, rights, or contractual requirements may apply.
- If approved, record the metadata-stripping event and deliver public-safe files plus internal provenance summary.

Critical failures:

- Refusing categorically without context.
- Removing metadata silently from all files including masters.
- Giving legal advice.

### 10. Scenario: A voice clone or avatar is reused in a localized derivative. What continuity and governance controls are required?

Expected answer:

- Track avatar/voice IDs, consent source, approved usage scope, language/locale, prompt/script, model/tool, request IDs if available, and approval events.
- QA lip sync, pronunciation, gesture, gaze, wardrobe/background, disclosure needs, and voice identity.
- Escalate for consent/client/legal review if likeness/voice rights or new-use permissions are unclear.

Critical failures:

- Treating voice and avatar outputs as ordinary audio/video with no consent tracking.
- Assuming consent for the source language covers all localizations.

## Applied production tasks

### 11. Task: Draft a minimal asset manifest record for a generated hero product image.

Successful output should include:

- Stable asset ID and status.
- Asset type/role, scene/shot linkage, file path, checksum placeholder, dimensions/format.
- Created date, provider/tool/model context, request/job ID, seed, parameters, prompt ID.
- Source/reference IDs, parent/derivative IDs.
- Metadata/provenance status.
- Rights/usage notes, review notes, approvals, supersession fields, retention.

Scoring:

- 4: Complete, structured, includes explicit unknowns and continuity/approval fields.
- 3: Mostly complete but misses one area such as provenance or retention.
- 2: Tracks file and prompt but not lineage/approvals.
- 1: Filename-only or prose-only tracking.
- 0: No manifest.

Critical failures:

- Inventing real provider metadata.
- Omitting product/brand approval for ad assets.

### 12. Task: Create a continuity QA checklist for a 60-second explainer with a recurring host, generated diagrams, narration, captions, and 9:16 social derivatives.

Successful output should cover:

- Asset-level checks: file opens, format, checksums, prompts/model context, metadata/provenance.
- Character/wardrobe checks against locked references.
- Diagram/text/factual checks.
- VO/caption agreement, pronunciation, caption timing/readability, sidecar/burn-in status.
- Scene-level story and edit continuity.
- Derivative checks for vertical crop safety, caption placement, platform-specific exports, and localized variants if any.
- Review handoff with asset IDs and timecodes.

Scoring:

- 4: Covers all modes and links QA to manifest/bible/ledger.
- 3: Covers most modes but weak derivative or metadata checks.
- 2: Generic visual checklist with little continuity lineage.
- 1: Only final render review.
- 0: No usable checklist.

### 13. Task: Respond to a user who wants to regenerate an approved character scene because the background is wrong, but the face/wardrobe must remain identical.

Expected approach:

- Classify regeneration as repair, not replacement.
- Lock parent asset ID, character/wardrobe reference IDs, prompt ID lineage, seed if available, model/tool context, and invariants.
- Define allowed change: background/location only.
- Define forbidden changes: face, age, hair, wardrobe, body proportions, approved expression if relevant.
- Create a new minor version if approval basis remains the same, or major version if the provider/model/reference path materially changes.
- QA against contact sheet/locked references before approval.

Critical failures:

- Starting from a fresh prompt without parent/reference lineage.
- Promising identical output based only on seed.
- Overwriting the approved scene.

### 14. Task: Produce a review handoff package outline for a product-ad campaign with master, social derivatives, captions, and localized Spanish version.

Successful output should include:

- Asset manifest and source/reference ledger.
- Product/brand continuity bible with locked references.
- Contact sheet/review board grouped by scene and derivative.
- Change log since previous review.
- Approval table for product/brand/legal/localization/accessibility.
- Masters, review exports, captions/subtitles, localized graphics/VO if present, paths and checksums.
- Open risks: platform rules, metadata stripping, claims/disclaimers, crop safety, source rights.
- Instruction for reviewers to use asset IDs and timecodes.

Scoring:

- 4: Complete and production-ready.
- 3: Good but misses one approval domain or derivative lineage.
- 2: Lists deliverables but not manifests/risks.
- 1: Only links final videos.
- 0: No handoff package.

## Source and factual-grounding checks

The evaluated response should reflect the skill's source posture:

- It may reference C2PA, IPTC, NIST AI RMF/GenAI Profile, PREMIS, PBCore, LOC Recommended Formats, W3C WebVTT, or FADGI when relevant.
- It should mark provider/platform facts as volatile and instruct re-checking current rules at production time.
- It should avoid legal advice and instead define escalation triggers.

Penalize:

- Unsupported claims about specific provider capabilities, pricing, model behavior, content credential support, or platform disclosure rules.
- Universal claims that one metadata standard solves all provenance, rights, or continuity needs.
- Advice to remove disclosures or provenance to evade platform or legal scrutiny.

## Overall rubric

Score out of 20:

- 5 points: Continuity architecture. Uses asset IDs, manifests, ledgers, continuity bible, scene/shot linkage, and derivative lineage.
- 4 points: Metadata/provenance accuracy. Correctly positions C2PA/IPTC/PREMIS/PBCore/WebVTT/FADGI as supporting frameworks, not substitutes for production records.
- 4 points: Versioning and regeneration control. Distinguishes repair/variant/replacement, captures prompts/seeds/model versions when available, avoids overwrites.
- 3 points: Review, approval, and escalation. Includes approval gates, change logs, handoff package, and counsel/client escalation triggers without giving legal advice.
- 2 points: Mode coverage. Addresses image, video, audio, avatar, product/social/explainer/film-style needs when applicable.
- 2 points: Practical specificity. Provides concrete schemas, examples, QA checks, or production-ready tables rather than generic advice.

Pass thresholds:

- 17-20: Excellent; ready for production use.
- 14-16: Good; minor gaps.
- 10-13: Partial; needs revision before production.
- 0-9: Fails to apply the skill reliably.

Automatic fail conditions:

- Relies on filenames/chat memory alone for continuity.
- Invents provider metadata or legal clearance.
- Instructs removal or concealment of synthetic-media provenance/disclosure without review.
- Does not track parent/derivative lineage for regenerated or localized assets.
- Treats C2PA/IPTC metadata as a complete substitute for manifests, approvals, and continuity QA.
