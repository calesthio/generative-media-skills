---
name: media-provenance-rights
description: Provider-independent provenance, rights, consent, disclosure, and release governance for AI-generated media. Use when producing or reviewing generated images, video, audio, ads, avatars, product content, social clips, documentaries, localization, music, sound, or campaign assets that need source-rights checks, model/provider term checks, likeness or voice consent, trademark/logo review, copyrighted-character/style risk triage, music licensing, C2PA/content credentials, provenance ledgers, release notes, platform disclosures, jurisdiction/client caveats, or rights QA.
---

# Media provenance and rights governance

Use this skill to make generated media releasable, auditable, and explainable. It is not legal advice. It is a production governance workflow that helps an agent identify rights evidence, missing permissions, disclosure duties, and escalation points before a client or platform receives the asset.

Default posture: do not claim an asset is "cleared," "copyright-safe," "commercially safe," or "owned" unless the production record shows the exact basis for that statement. Prefer "approved for this release under the documented assumptions" plus a dated caveat.

## Separate facts, observations, and heuristics

Treat these as different evidence classes in your work product:

- Documented facts: directly supported by contracts, licenses, provider terms, platform rules, consent forms, official guidance, or technical metadata. Cite the source and verification date for volatile facts.
- Empirical observations: things observed in the actual workflow, such as "metadata survived this export" or "the uploaded platform copy retained no visible credential." Record the test, file hash, date, tool, and result.
- Production heuristics: conservative operating rules used to reduce risk when legal certainty is unavailable. Label them as heuristics, not law.

## Documented facts to keep in mind

Facts below were verified on 2026-07-10 unless otherwise noted. Re-check them for high-value, regulated, political, public-company, celebrity, or international releases.

- C2PA/Content Credentials represent provenance through signed manifests, assertions, claims, signatures, and content bindings. A C2PA manifest can be embedded in an asset or stored externally, and authenticity depends on validation of the signed claim and bindings, not on a human-readable note alone. Source: [C2PA Technical Specification 2.4](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html).
- The U.S. Copyright Office's AI report series covers digital replicas, copyrightability, and generative AI training. Part 1 was published July 31, 2024; Part 2 on copyrightability was published January 29, 2025; Part 3 on training was released as a pre-publication version on May 9, 2025 with final publication expected later. Source: [U.S. Copyright Office AI initiative](https://www.copyright.gov/ai/).
- U.S. copyright registration guidance for works containing AI-generated material requires attention to human authorship and may annotate registrations to clarify the claimed human-authored scope. Source: [Federal Register, 88 FR 16190](https://www.federalregister.gov/documents/2023/03/16/2023-05321/copyright-registration-guidance-works-containing-material-generated-by-artificial-intelligence).
- FTC endorsement guidance focuses on preventing deceptive advertising and includes disclosure of material connections between advertisers and endorsers. Source: [FTC endorsements, influencers, and reviews guidance](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews).
- Trademark risk is mainly a consumer-confusion and brand-use issue, not just an image-generation issue. Review visible marks, lookalike marks, product packaging, slogans, and trade dress against the release context. Source: [USPTO trademark resources](https://www.uspto.gov/trademarks).
- SAG-AFTRA frames AI performance guardrails around consent, fair compensation, and control over performances; NAVA recommends performer contracts cover consent, limits on use, opt-outs or term limits, payment, exclusivity, and secure tracking of voice/likeness products. Sources: [SAG-AFTRA AI framework](https://www.sagaftra.org/contracts-industry-resources/member-resources/artificial-intelligence), [NAVA Synth & AI](https://navavoices.org/synth-ai-info/).
- Creative Commons licenses vary materially. Some permit commercial use, some restrict noncommercial use, some prohibit derivatives, and attribution is generally required unless the work is CC0/public-domain-dedicated. Source: [Creative Commons license overview](https://creativecommons.org/cc-licenses/).
- YouTube requires creators to disclose realistic AI-generated or meaningfully AI-altered content through the upload flow; non-realistic or minor edits are treated differently. Source: [YouTube Help: disclosing GenAI content](https://support.google.com/youtube/answer/14328491).
- TikTok lets creators label content that is completely generated or significantly edited by AI and requires creators to label AI-generated content that contains realistic images, audio, or video. Source: [TikTok Support: AI-generated content](https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content).
- Meta describes "AI info" labels for some AI-created or significantly edited ad images and says social issue, election, or political ads already require disclosure in relevant cases. Source: [Meta Help: AI-generated images in ads](https://www.meta.com/help/artificial-intelligence/355108217670024/).
- Provider output rights and restrictions differ. For example, OpenAI terms assign output rights as between user and OpenAI while requiring users to have rights for inputs and comply with law; Runway states users retain rights and commercial-use ability as between user and Runway; ElevenLabs prohibits unauthorized, deceptive, or harmful voice impersonation; Adobe's generative AI guidelines prohibit violating third-party copyright, trademark, privacy, publicity, or other rights and may attach Content Credentials. Sources: [OpenAI Terms of Use](https://openai.com/policies/row-terms-of-use/), [Runway usage rights](https://help.runwayml.com/hc/en-us/articles/18927776141715-Usage-rights), [ElevenLabs Prohibited Use Policy](https://elevenlabs.io/use-policy), [Adobe Generative AI User Guidelines](https://www.adobe.com/legal/licenses-terms/adobe-gen-ai-user-guidelines.html).

## Intake: define the release, not just the asset

Rights governance depends on where and how the asset will be used. Before generation or review, capture:

- Deliverable: image, video, audio, avatar, localization dub, ad variant, product page, documentary sequence, social clip, pitch material, internal rough cut.
- Release surface: organic social, paid ad, broadcast, theatrical, web, app store, marketplace listing, investor deck, classroom, internal-only.
- Territory and audience: country/region, age targeting, regulated sector, political/social issue content, public figure relevance.
- Commercial posture: internal draft, client-facing concept, paid media, monetized channel, resale/template, merchandise, product packaging.
- Subject matter: real people, synthetic people, public figures, minors, health/finance/legal claims, newsworthy events, documentary claims, product performance claims.
- Inputs and references: user-provided files, stock assets, archival footage, brand assets, product photos, music, voice samples, scripts, datasets, prompts, negative prompts, LoRAs/fine-tunes, style references.
- Required representation: what the client expects you to warrant, indemnify, disclose, attribute, or document.

If any answer is unknown, record it as unknown. Unknowns become release blockers only when the missing information affects the planned release.

## Rights map every asset

Create a rights map before final release. Use one row per input, generated asset, edited derivative, and final deliverable.

Minimum fields:

- `asset_id`: stable ID.
- `file_path` and `hash`: for each reviewed file version.
- `role`: input, reference, ingredient, generated output, edit, final master, thumbnail, caption file, audio stem.
- `source`: user upload, stock library, public-domain source, CC-licensed source, provider generation, camera capture, screen recording, agency asset, client asset.
- `source_url_or_contract`: URL, contract ID, purchase receipt, consent form, license file, or "none provided."
- `rights_holder_or_claimant`: known owner or claimant.
- `license_or_permission`: exact license, contract clause, provider plan/terms, consent scope, or "not established."
- `allowed_use`: release surfaces, territories, duration, exclusivity, edit rights, sublicensing, paid-media rights, model-training restrictions.
- `restrictions`: attribution, noncommercial, no derivatives, no political use, no sensitive verticals, union constraints, platform constraints.
- `AI_process`: provider, model/tool, version if known, date, prompt summary, seed/job ID if available, human edits, reference strength, fine-tune/LoRA/dataset details.
- `likeness_voice_identity`: people depicted or simulated, consent basis, release scope, expiry, revocation terms.
- `marks_logos_trade_dress`: visible marks, client-owned marks, third-party marks, altered marks, product packaging.
- `music_sound`: composition rights, master/sound-recording rights, sync rights, mechanical/public-performance assumptions, SFX license, attribution.
- `provenance_metadata`: C2PA present, watermark present, EXIF/XMP retained, sidecar ledger path, platform disclosure choice.
- `review_status`: clear-for-scope, needs attribution, needs client confirmation, needs legal review, blocked.
- `reviewer`, `review_date`, `notes`.

## Source and input rights

Do not feed an asset into a model merely because it is visible online. For each input/reference:

- Confirm who supplied it and whether they had rights to provide it for AI use.
- Check whether the source license permits derivatives, AI processing, commercial use, paid media, sublicensing, and territory/duration needed for the release.
- For CC materials, distinguish BY, SA, NC, ND, and CC0. Do not use NC material in commercial or monetized contexts without separate permission. Do not adapt or use as a generative reference if ND restrictions would be implicated by the intended output; escalate rather than assuming.
- For stock assets, read the plan/license tier. "Royalty-free" usually means no per-use royalty, not unlimited rights for every release or model-training/reference use.
- For brand assets, confirm they are client-owned or client-licensed for the specific campaign, territory, and media.
- For confidential inputs, check whether the chosen provider may use inputs/outputs for training or improvement and whether the client contract permits that processing.

Heuristic: when input rights are unclear, use a newly created clean reference, client-owned asset, commissioned asset, public-domain asset, or provider with documented training/enterprise controls rather than trying to transform the original enough to "make it safe."

## Provider and model terms check

Before release, record the provider terms that matter to the actual workflow:

- Input responsibility: who warrants rights to prompts, uploads, reference images, voice samples, training data, and fine-tunes.
- Output rights: whether the provider claims ownership, assigns rights, allows commercial use, limits exclusivity, or allows similar outputs for others.
- Usage restrictions: impersonation, sexual content, political content, deception, regulated industries, public figures, minors, hate/harassment, biometric or voice cloning restrictions.
- Training/data use: whether prompts, inputs, outputs, voice data, or fine-tune data may be used to train or improve services; opt-out or enterprise settings.
- Disclosure/provenance: watermark, Content Credentials, labeling, generated-content statements, removal restrictions.
- Indemnity/support: whether any IP indemnity exists, what tier it requires, exclusions, claim process, and whether it covers the planned release.
- Beta/preview caveats: preview tools may have weaker warranties, different commercial terms, or no indemnity.

Production heuristic: provider terms can grant permission as between the user and provider, but they do not clear third-party rights in inputs, trademarks, likenesses, music, or substantially similar outputs. Keep those layers separate in the release notes.

## Likeness, voice, and performance consent

Treat recognizable identity as a separate rights surface from copyright. This includes face, body, voice, name, signature phrases, performance style, biometric data, and combinations that make a person identifiable.

Require documented consent when:

- Cloning, synthesizing, dubbing, de-aging, face-swapping, or lip-syncing a real person.
- Making a real person appear to say, endorse, do, wear, attend, or believe something they did not.
- Using an employee, customer, influencer, performer, patient, student, minor, public figure, executive, or deceased person.
- Training or fine-tuning on someone's voice, likeness, motion, or performance.

Consent should specify:

- Person and identity attributes covered.
- Allowed media, campaign, brand/client, territory, duration, platform, paid/organic use, and derivative/localization rights.
- Whether AI generation, voice cloning, face replacement, lip-sync, editing, training, and future reuse are permitted.
- Review/approval rights, revocation/expiry, exclusivity, compensation, union or guild terms, storage/security requirements.
- Whether disclosure is required in the content, caption, contract, or platform upload settings.

For minors, sensitive contexts, health/finance/legal claims, sexualized content, political content, or posthumous likeness, escalate to legal/client approval even with apparent consent.

## Trademarks, logos, products, and trade dress

Generated media can create trademark risk by displaying marks, confusingly similar marks, product packaging, UI screens, uniforms, venues, slogans, or trade dress. Review:

- Is the mark owned or licensed by the client for this use?
- Is the use nominative, incidental, comparative, parody, editorial, or promotional? Do not decide legal status alone; flag it.
- Could the asset imply endorsement, sponsorship, affiliation, product compatibility, or official status?
- Does the generated mark mutate a real logo into a lookalike that increases confusion?
- Does product packaging or UI resemble a competitor's trade dress?
- Are fake logos accidentally readable enough to be mistaken for real marks?

Production heuristic: for paid ads and product pages, remove or replace third-party marks unless the client specifically approves the use and provides a basis. For documentary/editorial contexts, preserve truthful context but document why the mark appears and whether it was altered.

## Copyrighted characters, style references, and protected works

Separate broad inspiration from protected expression:

- Avoid prompts that request living artists' exact recent style, copyrighted characters, franchise worlds, proprietary mascots, distinctive costumes, identifiable scenes, album covers, posters, game assets, or "same as" references unless the client owns or licenses them.
- Do not rely on "make it like X but not X" as a clearance strategy. If a viewer would identify the source property, treat it as a rights risk.
- Style alone may not be copyrightable in some jurisdictions, but prompts that target a specific artist, series, character, or protected work can still create client, platform, publicity, trademark, unfair competition, or reputational risk.
- For documentary or commentary use, distinguish showing a factual reference from generating new derivative-looking material. Escalate if the generated material substitutes for licensed clips, stills, posters, or music.

Production heuristic: translate style references into neutral craft attributes: palette, lens, era, composition, lighting, texture, motion, edit rhythm, typography class, mood. Keep an internal note mapping the reference to these attributes without asking the model to imitate a protected source.

## Music and sound rights

Music requires special care because composition rights and sound-recording/master rights are separate.

For each music or sound asset:

- Identify whether it is generated, commissioned, library/stock, CC, public domain, user-provided, extracted from video, or platform-library-only.
- Confirm rights for synchronization to video, paid advertising, monetized social, broadcast, territory, duration, edits, stems, loops, and sublicensing to the client.
- Record attribution requirements and cue-sheet needs.
- Check whether "free," "royalty-free," or "platform audio library" is limited to a specific platform or noncommercial use.
- For AI music, check provider terms, training/input obligations, vocal likeness restrictions, lyric rights, and whether output can resemble existing songs or artists.
- For sound effects, confirm whether license permits commercial synchronization and derivative editing.

Heuristic: if a track is only licensed inside a social platform's native library, do not reuse it in rendered exports for ads, other platforms, client websites, or broadcast without a separate license.

## C2PA, metadata, and provenance ledger design

Use C2PA/Content Credentials where the toolchain supports it, but do not treat metadata as the only record. Many production steps can strip or alter metadata. Maintain a sidecar ledger for every release candidate.

Recommended provenance stack:

1. Embedded or sidecar C2PA manifest when available.
2. Human-readable release ledger in JSON/YAML/CSV or project database.
3. Hashes of release candidates and source ingredients.
4. Export/test notes showing whether C2PA, EXIF, XMP, watermarks, and captions survived editing, compression, and upload.
5. Client-facing release note summarizing AI use, rights basis, required attribution, and caveats.

Minimum release ledger example:

```yaml
release_id: spring-campaign-hero-video-v3
reviewed_on: 2026-07-10
review_scope:
  surfaces: [instagram_paid_ad, youtube_organic, client_landing_page]
  territory: US
  duration: 12 months
final_assets:
  - path: renders/spring-campaign-hero-v3.mp4
    sha256: "..."
    c2pa_status: "present in master; stripped by test upload to platform X"
ai_generation:
  - asset_id: bg_scene_04
    provider: "provider name"
    model_or_tool: "model/tool/version if known"
    job_id: "..."
    prompt_summary: "original abstract spring background, no artist/style/character references"
inputs:
  - asset_id: product_packshot
    source: client
    rights_basis: "client-owned product photography, email approval 2026-07-08"
    restrictions: "use only for Spring 2026 campaign"
identity:
  real_people: []
  synthetic_people: ["non-realistic illustrated shopper"]
music_sound:
  track: "commissioned instrumental loop"
  rights_basis: "work-for-hire agreement 2026-07-09"
trademarks:
  client_marks: ["ClientName logo"]
  third_party_marks: []
platform_disclosure:
  youtube_ai_use: "yes if uploaded as realistic AI-altered content; otherwise document rationale"
  tiktok_creator_label: "apply if significantly AI-generated/edited"
release_status: "approved for stated scope after client confirmation"
caveats:
  - "Not a legal opinion."
  - "Re-check provider/platform terms before reuse outside stated scope."
```

## Platform and audience disclosure

Plan disclosure before upload, not after rendering.

Disclose when:

- The platform requires it for realistic or meaningfully altered synthetic content.
- The content includes a synthetic real-person likeness, voice, endorsement, testimonial, news-like scene, public event, political/social issue content, or product demonstration that could mislead.
- The client, agency, union agreement, license, or provider terms require it.
- FTC endorsement or advertising principles require material connections, sponsorship, influencer, testimonial, or AI-generated testimonial context to be clear.

Disclosure can appear in platform toggles, labels, captions, supers, alt text, landing-page notes, ad library settings, release notes, contracts, or all of these. Keep the wording accurate: "AI-generated background," "synthetic voice with performer consent," "AI-assisted edit," and "dramatization" mean different things.

Do not remove or obscure generated-content credentials, watermarks, or required notices unless the terms permit removal and the release still satisfies disclosure obligations.

## Risk triage

Classify each asset by the highest applicable level.

| Level | Typical signals | Action |
|---|---|---|
| Low | Original abstract visuals, no real people, no third-party marks, provider allows commercial output, client-owned inputs, no platform disclosure trigger | Record ledger and release note. |
| Medium | Stock/CC inputs, visible client marks, synthetic people, AI product backgrounds, generated music, platform labeling likely, unclear attribution | Resolve license details, add disclosures/attributions, get client confirmation. |
| High | Real person likeness/voice, public figures, minors, testimonials, political/social issue ads, health/finance/legal claims, competitor marks, documentary/news realism, celebrity-like outputs | Require documented consent, client legal review, platform policy check, and human approval. |
| Blocked | Missing rights for key input, no consent for cloned likeness/voice, NC/ND license conflict, requested copyrighted character/franchise lookalike, deceptive endorsement, provider terms prohibit use | Do not release. Rework with cleared inputs or obtain permission. |

Escalate to legal/client counsel when the answer requires interpreting law, fair use, right of publicity, union contracts, privacy law, political advertising rules, international jurisdiction, indemnity, or litigation risk.

## Rights QA before delivery

Run this review on final masters, not only prompts:

- Compare final output against prompts and references. Flag unplanned logos, faces, signatures, characters, watermark artifacts, product claims, and style imitation.
- Search visually or manually for recognizable brands, copyrighted characters, celebrities, public figures, landmarks, uniforms, or trade dress if relevant.
- Listen for music/song similarity, recognizable voice likeness, artist imitation, uncleared samples, and lyrics that may require separate rights.
- Verify attribution text is present and correct for CC/stock/commissioned assets.
- Confirm platform toggles and captions are planned for each upload surface.
- Verify C2PA/metadata on the exact delivery file; record whether export/transcode/upload stripped it.
- Confirm file hashes and version numbers match the approved release.
- Record unresolved assumptions in the release note; do not hide them in internal chat.

## Example: product social ad using generated visuals

Intent: create a 15-second paid Instagram and YouTube ad for a client-owned water bottle. The team will use a client packshot, generated backgrounds, generated motion graphics, and stock SFX.

Workflow:

1. Intake records paid ad, US release, 6-month campaign, client landing page reuse, no people, no competitor comparisons.
2. Rights map records the packshot as client-supplied and restricted to the campaign. If the client cannot confirm rights, pause before using it as an image prompt/reference.
3. Prompt avoids "in the style of Brand X" and competitor bottle silhouettes. It describes neutral attributes: "minimal studio lighting, condensation, recycled-paper texture, soft morning color palette."
4. Provider terms are checked for commercial output and input treatment. If the client prohibits training use, choose a provider/tier/settings that match that requirement or avoid uploading confidential packshots.
5. SFX license is checked for paid ads and web use; attribution is included if required.
6. QA inspects frames for accidental third-party logos on generated gym bags, shoes, storefronts, or UI.
7. Release note says: "AI-generated abstract backgrounds and motion graphics; client-owned product photography; stock SFX under [license]; no real-person likeness; platform AI labels to be applied if upload flow treats the generated realistic background as requiring disclosure."

Likely failure modes: generated fake certification seals, unreadable pseudo-brands, competitor-like packaging, provider terms unsuitable for confidential product images, or stock SFX licensed only for organic social.

## Example: consent-governed avatar localization

Intent: localize a CEO announcement into Spanish and Japanese with a synthetic voice and lip-sync avatar.

Workflow:

1. Treat the CEO's face, voice, name, job title, and performance as identity rights, even though the company employs the CEO.
2. Obtain written consent for synthetic voice, lip-sync, languages, script, company channels, territories, duration, paid/organic use, storage of voice/face data, approvals, and revocation.
3. Check provider voice/lip-sync terms for consent, impersonation, data use, commercial use, and prohibited political/regulated contexts.
4. Put human translation review and the CEO or authorized representative approval into the release gate; mistranslation can create false endorsement or securities/compliance risk.
5. Add a disclosure such as "Localized using an AI-assisted synthetic voice with approval" if required by client policy, platform policy, provider terms, or audience context.
6. Ledger records original approved script, translations, voice sample consent, provider job IDs, final file hashes, and approval timestamps.

Likely failure modes: consent only covers English, provider stores voice data contrary to company policy, translated speech changes claims, or platform disclosure is missed because the video looks real.

## Example: documentary sequence with archival-looking generated material

Intent: produce a documentary explainer about a 1980s technology company where no archive footage is available.

Workflow:

1. Mark generated scenes as dramatizations, not archival evidence.
2. Avoid generating exact logos, real executives, real office interiors, newspaper mastheads, or product UIs unless rights or factual/editorial basis is reviewed.
3. Use neutral scene design: "period-inspired office, beige CRT monitors, generic circuit-board diagrams," not "shot from inside [specific company] headquarters."
4. If using real quotes, source and clear quote use separately; do not synthesize a real person saying them unless consent and disclosure are handled.
5. Use licensed or commissioned music. Do not use soundalikes of famous 1980s songs to imply era.
6. On-screen or description disclosure: "Some scenes are AI-generated dramatizations based on documented facts; not archival footage."

Likely failure modes: viewers mistake dramatizations for evidence, generated visuals include false logos or real people, or "period style" becomes an identifiable film/artist imitation.

## Delivery language

A good client-facing release note is concise and bounded:

- What was generated or AI-assisted.
- What inputs were used and their rights basis.
- What real identities, voices, marks, music, and third-party materials appear.
- What disclosures or attributions are required.
- What release scope was reviewed.
- What remains unverified or requires client/legal confirmation.

Example release note:

"Reviewed for US organic social and paid Instagram/YouTube use through 2026-12-31. Final video uses client-supplied product photography, AI-generated abstract backgrounds, commissioned original music, and no real-person likeness. C2PA metadata is present in the master file; platform transcodes may not retain it. Apply platform AI disclosure if prompted for generated realistic visuals. This is a production rights review, not a legal opinion; reuse outside the stated scope requires re-review."


