---
name: documentary-montage-production
description: Provider-independent workflow for AI agents producing documentary-style montages, archive-driven timelines, interview-supported sequences, nonprofit or advocacy shorts, historical explainers, and hybrid generated/archive edits. Use for editorial thesis development, research/source logs, fact-checking, archive rights, synthetic reenactment disclosure, chronology, interview selects, lower thirds, generated b-roll direction, music restraint, captions, sensitive subjects, review escalation, delivery variants, and documentary QA.
---

# Documentary Montage Production

Use this skill when the deliverable asks the viewer to believe, understand, or feel the significance of real people, real events, real institutions, or real-world claims. The central rule is: do not let the audience become more certain than the evidence allows.

This is not legal advice. Treat rights, defamation, privacy, platform-policy, election, medical, financial, public-safety, and vulnerable-subject issues as escalation triggers for the appropriate human editor, client approver, platform owner, or counsel.

## Non-negotiable documentary posture

Separate five things in every decision:

1. **Documented fact**: directly supported by a logged source.
2. **Corroborated interpretation**: a reasonable conclusion from multiple logged sources.
3. **Participant testimony**: attributed lived experience or opinion, not universal proof.
4. **Illustration or reenactment**: visual support that is not evidence.
5. **Editorial thesis**: the argument the piece makes from the above.

If a shot, sound cue, texture, caption, edit, or generated image makes category 3, 4, or 5 look like category 1, revise it.

## Start with an evidence-first brief

Before writing a script or making prompts, create a working brief with:

- **Thesis**: one sentence the piece can fairly support.
- **Audience and release context**: platform, geography, client, advocacy/commercial/newsroom/nonprofit context, and expected scrutiny.
- **Core claims**: the 3-7 factual claims the piece depends on.
- **Human stakes**: whose life, community, work, property, reputation, or safety is affected.
- **Evidence map**: source status for each claim: verified, needs corroboration, contested, or must cut.
- **Rights/disclosure map**: what footage, photos, voices, logos, documents, maps, music, and generated media will require permission, attribution, label, or review.
- **Sensitivity level**: routine, sensitive, high-risk, or legal/editorial review required.

Useful thesis test: "Because [documented change/conflict], [specific people/place/system] now faces [specific consequence]." If the thesis only says "this is shocking" or "you won't believe," it is not yet documentary-grade.

## Maintain a source and research log

Keep a source log even for short social documentaries. A reliable log lets another agent or human reconstruct why each line and shot exists.

Minimum fields:

- `source_id`
- title or description
- creator/publisher/archive
- URL, catalog ID, collection, box/folder/item, or file path
- date created, date published, and date accessed
- source type: primary record, official data, peer-reviewed research, news report, interview, participant-provided material, archive still/video, generated illustration, etc.
- rights status: owned, commissioned, licensed, Creative Commons license, public domain claim, government work claim, fair-use review needed, unknown, or prohibited
- provenance notes: original capture, digitized copy, upload mirror, C2PA/Content Credentials present, metadata stripped, chain of custody unknown
- relevant claims or scene IDs
- confidence and unresolved questions

Minimum claim log:

| Field | What to record |
|---|---|
| `claim_id` | Stable ID used in script, cards, and QA |
| exact wording | The narration, lower third, card, or caption text |
| evidence | `source_id` values and exact page, timestamp, table, quote, or frame |
| support level | single-source, corroborated, disputed, inference, opinion |
| on-screen treatment | spoken, card, lower third, graphic, caption, or omitted |
| fact-check status | unchecked, checked, needs editor, needs counsel, cut |

Do not cite a search result, social repost, or AI summary as the source for a consequential claim. Use the underlying original source when available.

## Fact-checking discipline

Use an evidence hierarchy:

1. Original records, official data, court filings, archival catalog records, direct footage, and complete interview recordings.
2. Subject-matter experts, peer-reviewed research, institutional reports with disclosed methods.
3. Reputable journalism with named sources and corrections practices.
4. Participant testimony, clearly attributed.
5. Social media, unsourced compilations, AI summaries, and viral claims only as leads to verify elsewhere.

For each claim:

- Confirm that the source actually says the scripted claim, not merely something adjacent.
- Check dates, units, denominators, names, locations, and causal language.
- Prefer "after," "during," or "alongside" unless evidence supports "because."
- Preserve uncertainty: use "about," "at least," "reported," "according to," or "records show" when appropriate.
- Keep allegations attributed and give fair opportunity for response when making serious claims about identifiable people or organizations.
- Remove or reframe claims that are true individually but misleading in sequence.

For historical timelines, distinguish:

- **event date**: when the event happened
- **source date**: when the image/document/interview was created
- **publication date**: when a source was published
- **edit date**: when the montage was produced

Cards such as "Chicago, 1968" must mean the image/clip actually depicts Chicago in 1968. If not, write "Archive image, Chicago, 1960s" or "Illustrative archival image; not the meeting described."

## Build chronology and causality carefully

Documentary montages often compress time. Compression is allowed; false causality is not.

Use one of these structures:

- **Timeline spine**: chronological progression with dates or era cards.
- **Argument ladder**: each beat proves a step in the thesis.
- **Witness braid**: interview testimony alternates with records and archive to avoid one voice carrying all proof.
- **Then/now contrast**: historical source followed by present-day consequence.
- **Case-to-system zoom**: one person or place opens into broader data and policy context.
- **Mystery/reveal**: acceptable only if the withheld information is not necessary for informed consent or safety.

For every transition, ask: "Does this imply A caused B?" If yes, ensure the claim log supports causality. If not, add a card or narration bridge: "The records do not show why the decision changed, but they show what changed next."

## Handle interviews and audio selects

Work from complete transcripts and source audio/video, not isolated clips.

For each select, log:

- speaker name, role, and release/consent status
- source file and timecode in/out
- transcript text, including meaningful pauses or corrections
- context before/after the select
- why the select is used
- whether it is factual testimony, lived experience, opinion, or emotional color
- cleanup applied: noise reduction, pause removal, filler removal, translation, subtitle edit

Do not create "Frankenbites" that combine fragments into a meaning the speaker did not convey. If a sentence is assembled from non-adjacent moments, verify the combined meaning against the full interview and avoid hiding the join when the change is material. Use paraphrase in narration rather than manufacturing a cleaner quote.

For translated interviews:

- keep original-language audio audible where possible;
- identify translator/subtitler status when high-stakes;
- flag idioms, contested terms, and emotionally loaded phrasing for human review;
- avoid synthetic voiceover that could be mistaken for the original speaker unless explicitly disclosed and approved.

## Archive and reference rights

"Found online" is not a rights status. Treat every archive or reference item as requiring a rights decision before final delivery.

Common statuses:

- **Owned or commissioned**: confirm contract covers this use, territory, term, platform, paid ads, and derivatives.
- **Licensed stock/archive**: keep license, invoice, allowed uses, restrictions, attribution requirements, and expiration.
- **Creative Commons**: verify exact license version and restrictions. BY requires credit; NC may block commercial or fundraising use; ND may block edits/adaptations; SA may impose share-alike obligations.
- **Public domain**: record why it is public domain in the relevant jurisdiction. A scan, upload, or compilation can add separate rights even when the underlying work is public domain.
- **U.S. federal government work**: may be public domain under U.S. copyright law, but check third-party material, logos, privacy, personality rights, and agency-specific restrictions.
- **Fair use / fair dealing / quotation**: do not self-approve for final. Prepare a rationale and escalate.
- **Unknown or orphan**: do not use in final unless counsel/editor explicitly approves.

Prefer a rights log tied to the source log:

`asset_id`, `source_id`, owner/licensor, license terms, required credit, allowed platforms, edit restrictions, expiration, model/property/person releases, music/publishing/master rights, reviewer, decision date.

## Provenance and authenticity

When available, preserve original filenames, checksums, embedded metadata, camera metadata, archive catalog IDs, and C2PA/Content Credentials. C2PA provenance is useful but not a truth guarantee: it can show signed provenance information and tamper evidence when supported, but it does not prove that the underlying claim is true.

When metadata is missing or stripped, say so in the log; do not infer authenticity from visual appearance.

## Synthetic reenactment and generated media disclosure

Use generated imagery, generated video, synthesized voices, face swaps, recreated documents, and reenactments only when they clarify a story without pretending to be evidence.

Allowed uses, with labels:

- "AI-generated illustration" for abstract or generic b-roll.
- "Illustrative reenactment" for staged or generated depictions of reported events.
- "Recreated from court filing / transcript / interview" when visualizing a record; show the record source if possible.
- "Synthetic voice used for narration" when a generated voice is used.

Avoid or escalate:

- private person likeness without permission;
- minors' likenesses;
- public figures shown endorsing, confessing, acting in a crisis, or doing something not documented;
- generated disaster, war, crime, protest, medical, or police footage that viewers could mistake for real footage;
- fake authoritative sources, fake news footage, fake official documents, fake logos, fake camera timecodes, or fake archive stamps;
- synthetic trauma scenes where the informational value is not necessary and approved.

Disclose in three places when material is realistic or consequential:

1. **On-screen** near the generated or reenacted material.
2. **Credits/description** with a short generated-media note.
3. **Platform upload controls** where required.

Platform and regulatory rules change. Re-check distribution rules at production time. Verified on 2026-07-11: YouTube requires creators to disclose realistic AI-generated or meaningfully AI-altered content during upload; TikTok asks/requires labeling for realistic AIGC and prohibits harmful misleading impersonation categories including certain uses of public figures, private adults without permission, and minors; Meta has used AI labels based on self-disclosure and industry signals across Facebook, Instagram, and Threads. Treat these as volatile facts.

FTC and similar consumer-protection risk increases when synthetic media impersonates a business, government, official, endorser, expert, or ordinary person in a way that could mislead viewers in commerce. Escalate synthetic endorsements, fundraising appeals, political persuasion, product/medical/financial claims, and impersonation.

## Generated b-roll prompt translation

Generated b-roll should translate evidence into clearly illustrative visuals, not invent new facts.

Before prompting, write:

- factual anchors: what must be true in the image/video
- forbidden details: real faces, logos, badges, documents, locations, uniforms, timestamps, news chyrons, or readable text that are not licensed/verified
- disclosure label: how it will appear on screen
- visual role: mood, context, metaphor, process diagram, map, document texture, or reenactment

Prompt pattern:

```text
Create [illustrative / non-photoreal / stylized / clearly reenacted] b-roll for a documentary segment about [topic].
Show only: [verified or generic elements].
Avoid: real person likenesses, official logos, readable fake documents, news-watermark styling, camera timecodes, or details that imply this is authentic footage.
Tone: [observational, restrained, sober, hopeful].
Composition: [specific shot/framing/motion].
On-screen label to be added in edit: [AI-generated illustration / illustrative reenactment].
```

Example generated b-roll prompt:

```text
Create a restrained, clearly illustrative shot for a documentary about a city housing waitlist: an anonymous stack of generic paper forms on a public-office counter, shallow depth of field, no readable text, no logos, no real addresses, no identifiable people, natural window light, observational tone. This will be labeled "AI-generated illustration" in edit.
```

Do not ask a model to create "archival footage," "news footage," "CCTV," "bodycam," "court exhibit," or "realistic video of [actual event]" unless the output is explicitly framed and labeled as reenactment and approved.

## Lower thirds, date/location cards, and source cards

Lower thirds and cards are editorial claims. Fact-check them like narration.

Use:

- person lower third: `Name`, `role at time of event` or `current role`, and optional relationship to story.
- date/location card: exact date and location only when known; otherwise `circa`, `undated`, `location reported as`, or omit.
- archive/source card: `Source: [archive/publisher/collection]`, `Courtesy of [rights holder]`, or `Public domain: [basis]` when useful.
- generated-media card: `AI-generated illustration`, `Illustrative reenactment`, or `Recreated from [source]`.

Avoid:

- "exclusive," "never before seen," or "declassified" unless source log proves it;
- official-looking seals, typewriter textures, or broadcast chyrons that imply institutional provenance;
- role labels that prejudice the viewer, such as "fraudster" or "victim," before the evidence establishes that label.

## Archival texture ethics

Texture affects truth. Grain, scratches, projector flicker, VHS noise, monochrome, aspect ratio, and handheld shake can imply age or authenticity.

Use archival texture only when:

- it comes from the actual source;
- it is a clearly aesthetic treatment that does not alter meaning; or
- the piece's style makes the treatment obvious and not evidentiary.

Do not add fake archive wear, timestamps, watermarks, camera overlays, tape glitches, or "old film" processing to generated or modern footage in a way that implies it is historical evidence.

Restoration is also editorial. Do not over-clean footage so that important context disappears; record major stabilization, colorization, speed changes, or frame interpolation. Colorized, upscaled, slowed, or AI-restored archive should be labeled when the change is material.

## Music and sound restraint

Documentary music should support comprehension, not coerce belief.

Guidelines:

- Keep music below narration and testimony; preserve intelligibility first.
- Avoid villain cues under unproven allegations or identifiable people.
- Avoid swelling music exactly where a contested factual claim is made.
- Use silence, room tone, and natural sound to let difficult material breathe.
- Do not add screams, sirens, crowds, gunshots, crying, or disaster sounds unless sourced, licensed, and contextually accurate; synthetic sound effects that mimic real events require disclosure when consequential.
- For advocacy pieces, separate emotional appeal from evidentiary claims.

## Captions, transcript, and accessibility

Provide captions for prerecorded audio in synchronized media unless the video is clearly a media alternative for text. Captions should include dialogue, speaker identification when needed, and meaningful non-speech sound that affects understanding.

Deliver, when scope allows:

- burned-in captions for social feeds;
- sidecar SRT/VTT for platforms that support accessibility;
- transcript with speaker labels and source notes for web publication;
- audio description or a text alternative when key visual information is not available in the audio/narration;
- readable contrast, safe margins, and enough dwell time for lower thirds and cards.

For multilingual releases, do not translate captions from an already compressed social caption file if original transcripts are available. Use the source transcript and keep names, dates, and place names consistent with the claim log.

## Sensitive subjects and harm reduction

Use heightened review for:

- children and minors;
- death, grief, illness, disability, sexual violence, self-harm, addiction, domestic violence, hate crimes, war, disaster, displacement, incarceration, immigration, and poverty;
- private individuals who did not seek public attention;
- communities historically misrepresented by extractive media;
- active legal proceedings, active conflict, or ongoing safety risks.

Production practices:

- Ask whether the visual is necessary, not merely powerful.
- Prefer dignity-preserving details over repeated graphic imagery.
- Avoid identifying addresses, schools, workplaces, faces, license plates, medical details, or immigration status unless necessary and approved.
- Use content warnings where appropriate.
- Do not generate synthetic images of identifiable victims, minors, or traumatic events for emotional effect.
- Give participants clear context for how their interview, voice, image, and story will be used when you are responsible for production planning.

## Review and escalation triggers

Escalate before final delivery when any of the following are present:

- serious allegations about identifiable people or organizations;
- hidden-camera, leaked, hacked, scraped, or private material;
- unlicensed archive, music, logos, trademarks, maps, photographs, or social posts;
- fair-use/fair-dealing reliance;
- minors or vulnerable subjects;
- synthetic likeness, synthetic voice, face swap, or realistic reenactment;
- political/election content, public-health claims, financial/legal advice, product claims, or fundraising claims;
- graphic or traumatic material;
- contested chronology or causality;
- a client/advocacy sponsor with a direct interest in the outcome;
- platform disclosure uncertainty;
- any instruction to hide AI use, source limitations, sponsorship, or material edits.

Prepare the escalation packet with: brief, script, source log, claim log, rights log, generated-media log, rough cut or scene list, platform list, and specific questions needing approval.

## Production workflow

### 1. Research and thesis

- Define thesis, audience, platforms, sensitivity, and review owner.
- Build source, claim, rights, and generated-media logs.
- Identify what is verified, contested, missing, and out of scope.
- Decide whether the piece is journalism-style, advocacy, educational, branded, or artistic documentary; each has different disclosure and review expectations.

### 2. Script and edit map

- Write narration with claim IDs in comments or brackets.
- Map each interview select and archive asset to claims.
- Mark synthetic/illustrative material in the script, not just in the asset list.
- Use attribution in voiceover for contested or single-source claims.
- Leave room for natural sound and breathing space after emotional testimony.

### 3. Scene plan and assets

- For every scene, specify: purpose, evidence level, visuals, source IDs, rights status, lower thirds/cards, audio, captions, disclosure labels, and QA risks.
- Replace weak evidence scenes with diagrams, source documents, or explicitly illustrative visuals rather than overclaiming with fake realism.
- Confirm all generated prompts include forbidden details and disclosure intent.

### 4. Edit

- Check chronology and implied causality in sequence.
- Review all cards and captions as claims.
- Listen with music muted, then with music on; the story should still be fair both ways.
- Verify that interview edits preserve speaker meaning.
- Confirm no generated or recreated asset is visually indistinguishable from evidence without a label.

### 5. Delivery variants

Plan variants intentionally:

- **Festival/long-form**: fuller credits, source notes, archival acknowledgments, optional transcript.
- **Web article embed**: citations, transcript, image credits, correction/update note.
- **Social vertical**: burned captions, larger labels, fewer claims, stronger source cards, no tiny legal credits.
- **Paid ad/advocacy**: sponsor disclosure, platform ad rules, claim substantiation, rights for paid media.
- **Education/internal**: still requires rights and source logs; may allow more detailed source cards.

Do not remove AI, sponsor, or source-limit disclosures just because a shorter platform variant is crowded. Simplify the edit instead.

## Documentary QA checklist

Before final:

- Thesis is supported by logged evidence.
- Every factual narration line, lower third, date/location card, statistic, and caption has a claim ID or is clearly subjective.
- No edit implies unsupported causality.
- Interview selects preserve meaning and consent constraints.
- Archive rights are approved for the exact use, platform, term, and territory.
- Creative Commons and public-domain assumptions are documented.
- Generated media and reenactments are labeled in script, edit, credits/description, and platform controls as needed.
- No fake archive texture or official styling misleads viewers.
- Music and sound design do not prejudice contested claims.
- Captions include dialogue, speaker IDs when needed, and meaningful sound.
- Sensitive-subject treatment has been reviewed for dignity, safety, and necessity.
- Escalation triggers have either been cleared or the risky material has been cut.
- Delivery variants preserve source, rights, AI, sponsor, and accessibility obligations.

## Example: nonprofit advocacy short

**User request:** "Make a 90-second vertical documentary montage about families waiting years for affordable housing in our city. We have one interview, city data, and a few photos."

**Approach:**

- Classify as advocacy/nonprofit documentary with claim-substantiation risk.
- Thesis: "City records and one family's experience show that demand for affordable housing has outpaced available placements."
- Build claim log:
  - `C1`: current waitlist size from city housing department dataset, accessed date.
  - `C2`: interviewee's wait duration, supported by interview and optionally documents if provided.
  - `C3`: number of new units last year, from city annual report.
- Rights log:
  - interview release needed;
  - family photos: participant permission and any photographer credit;
  - city data: cite source;
  - generated office-paper b-roll: label as AI-generated illustration.
- Structure:
  1. Hook: interview select, not a statistic.
  2. Source card: "City housing data, accessed [date]."
  3. Timeline: application date, wait milestones, present day.
  4. System context: data card with denominator and source.
  5. Call to action: sponsor/nonprofit disclosure and claim review.
- Generated prompt:

```text
Create a restrained, non-photoreal illustrative shot for a vertical documentary: anonymous hands holding a generic envelope at a kitchen table, no readable text, no logos, no real addresses, no identifiable faces, soft natural light, sober observational tone. This will be labeled "AI-generated illustration."
```

**Likely failure modes:** turning one family's story into a universal claim; using "the city failed families" without documented causality; adding sad music under a contested policy claim; cropping family photos without consent; omitting sponsor disclosure in the social caption.

## Example: historical archive explainer

**User request:** "Create a 3-minute historical explainer about why a 1930s bridge project changed a neighborhood."

**Approach:**

- Thesis: "Planning records, maps, and newspaper accounts show the bridge redirected traffic and accelerated demolition along [corridor]."
- Source plan:
  - planning commission minutes and maps as primary records;
  - archive photos with catalog IDs;
  - newspaper reports as contemporary secondary sources;
  - present-day footage or maps for then/now contrast.
- Chronology:
  - 1931 proposal;
  - 1933 approval;
  - 1935 construction;
  - 1936 traffic rerouting;
  - later demolition, only if supported.
- Cards:
  - "Planning Commission Map, 1933 - Source: [Archive]"
  - "Archive photo, circa 1935; exact date not listed"
  - "Illustrative map animation based on [source IDs]"
- Generated media:
  - use diagrammatic maps and abstract construction silhouettes, not fake "1930s newsreel footage."
- Review:
  - verify public-domain or license status for each photo;
  - do not colorize archive unless labeled;
  - avoid saying the bridge "destroyed the neighborhood" unless sources establish causality and scope.

**Likely failure modes:** mixing photos from different years under one date card; adding fake film scratches to generated clips; using modern neighborhood boundaries for historical claims; presenting newspaper rhetoric as settled fact.

## Sources and verification notes

Verified 2026-07-11 unless noted. Re-check volatile platform, regulatory, and copyright guidance at production time.

- YouTube Help, "Disclosing use of GenAI content": https://support.google.com/youtube/answer/14328491
- TikTok Support, "About AI-generated content": https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content
- Meta, "Our Approach to Labeling AI-Generated Content and Manipulated Media": https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/
- FTC, "Trade Regulation Rule on Impersonation of Government and Businesses" final rule PDF: https://www.ftc.gov/system/files/ftc_gov/pdf/r207000_govt_biz_impersonation_rule.pdf
- U.S. Copyright Office, "Copyright and Artificial Intelligence" and registration guidance index: https://www.copyright.gov/ai/
- C2PA, "Verifying Media Content Sources": https://c2pa.org/ and C2PA Explainer: https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html
- Reuters, "Journalistic Standards": https://reutersagency.com/about/standards-values/
- Society of Professional Journalists, "SPJ Code of Ethics": https://www.spj.org/spj-code-of-ethics/
- W3C WCAG 2.2, time-based media criteria: https://www.w3.org/TR/WCAG22/ and WAI Understanding SC 1.2.2 Captions: https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
- Dublin Core Metadata Initiative, "Metadata Basics": https://www.dublincore.org/resources/metadata-basics/
- Creative Commons Chooser and license guidance: https://creativecommons.org/chooser/
