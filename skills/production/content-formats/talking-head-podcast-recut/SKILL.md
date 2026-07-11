---
name: talking-head-podcast-recut
description: Provider-independent production workflow for recutting long talking-head, podcast, interview, webinar, panel, lecture, livestream, founder call, or customer-call footage into short clips, highlight reels, trailers, audiograms, captioned vertical videos, and social cutdowns. Use when an agent must ingest source recordings, transcribe and diarize speakers, select quotes without misrepresentation, preserve context, handle consent/rights/disclosures, clean jump cuts and audio, add captions, graphics, lower thirds, b-roll, platform variants, synthetic-media boundaries, review packets, delivery specs, and recut QA.
---

# Talking-Head Podcast Recut

Use this skill to turn existing speech-led media into truthful, useful derivative edits. The central obligation is editorial integrity: every cut must remain faithful to what the speaker meant in the source recording, and every commercial, synthetic, legal, or rights risk must be surfaced before publishing.

This is provider-independent. Use whatever local or hosted tools are available for transcription, diarization, editing, captions, audio repair, motion graphics, and export, but keep the workflow, ledgers, and review standards below intact.

## Operating principle

Treat a recut as a quotation with pictures, not as raw material to rewrite.

- Do not create a clip whose apparent claim, emotional tone, chronology, or endorsement differs from the source.
- Do not use reaction shots, cutaways, captions, titles, or music to imply agreement, conflict, surprise, confidence, causality, or product endorsement that the original source does not support.
- Do not publish synthetic voice, face, avatar, or reconstructed dialogue without explicit approval from the rights holder and the depicted/simulated person.
- Do keep enough context for the clip to be understandable without requiring the audience to know the full episode.
- Do keep an audit trail from final frame back to source timecode.

## Intake: refuse to cut blind

Before editing, collect or infer a production brief. If any high-risk item is unknown, pause or mark it for approval.

Required brief fields:

- Source files or URLs, recording date, event name, speakers, host, guest, and known restrictions.
- Desired deliverables: single clip, clip batch, highlight reel, trailer, audiogram, captioned vertical video, LinkedIn cutdown, YouTube chapter clip, ad creative, internal sales enablement, or other use.
- Target platforms, aspect ratios, max duration, thumbnail/title/copy needs, caption style, language, brand guidelines, and review deadline.
- Intended use: organic editorial, paid ad, sales enablement, testimonial, investor update, course material, news, internal training, or archival.
- Rights status: who owns source footage, music, slides, screen shares, logos, transcript, and speaker likeness.
- Approval path: editor, producer, client, speaker/guest, legal/compliance, brand, accessibility, and final publisher.
- Risk notes: regulated topics, minors, medical/financial/legal claims, employment claims, politics/elections, customer testimonials, unreleased product information, confidential call participants, or sponsor/affiliate relationships.

Create a production ledger before cutting:

```text
source_id:
  path_or_url:
  owner:
  recording_date:
  speakers:
  permitted_uses:
  restrictions:
  transcript_path:
  diarization_path:
  generated_assets:
  approvals_required:
```

## Source ingest and transcript workflow

1. Preserve the original. Work from a duplicate or proxy. Record source file names, checksums if available, duration, frame rate, resolution, channels, and any embedded captions or metadata.
2. Extract high-quality audio for transcription. If the recording has separate mics/tracks, keep them separate for repair and diarization.
3. Generate a timestamped transcript with speaker diarization. If diarization is weak, use speaker names only after manual verification.
4. Create a speaker map: name, role, organization, pronunciation, lower-third wording, consent status, and allowed uses.
5. Mark unusable or restricted sections: private information, off-record sections, unapproved names, copyrighted clips, embargoed product material, sponsor reads that cannot be repurposed, audience Q&A with unconsented participants, or low-confidence transcript spans.
6. Normalize transcript text lightly for reading, but keep a verbatim layer for quote verification. Do not "clean up" meaning.
7. Build searchable markers for topic, emotion, claim, proof, story beat, objection, audience question, and repeated filler.

Useful transcript markers:

```text
[00:13:42.2 - 00:14:21.8] Speaker: Maya Chen
Topic: onboarding friction
Claim: "activation doubled after we removed the first five setup steps"
Context before: discussing enterprise admins, not all users
Context after: says result was a pilot, not general launch
Risk: metric requires client approval
Clip potential: strong, but title must say "pilot" or avoid universal claim
```

## Rights, consent, and disclosure gate

This skill does not provide legal advice. It provides escalation triggers for the agent. When in doubt, ask the client, rights owner, counsel, or participant before cutting or publishing.

Escalate before production or publication when:

- The source recording was private, semi-private, internal, customer-facing, webinar-gated, or captured in a jurisdiction or setting where consent expectations are unclear.
- A participant did not explicitly agree to public repurposing, paid promotion, advertising, testimonial use, voice cloning, face replacement, avatar generation, translation dubbing, or synthetic extension.
- The clip uses a customer, employee, expert, creator, or influencer in a way that could be an endorsement or testimonial.
- The output will be used as an ad, sales asset, fundraising asset, political communication, medical/financial/legal advice, employment/recruiting claim, or investor claim.
- The recut includes third-party music, TV/movie/game footage, slides, screenshots, artwork, conference footage, audience Q&A, user-generated content, or logos beyond the source owner's rights.
- The source is newsworthy or critical commentary and the edit relies on fair use rather than permission.
- The title, thumbnail, caption, or intro card makes a stronger claim than the speaker made.
- The speaker discusses another person, customer, employer, patient, student, or confidential situation.

Commercial and endorsement disclosure:

- Documented fact, verified 2026-07-11: FTC endorsement guidance treats material connections as needing clear disclosure when an endorsement can be attributed to an advertiser or marketer. Use clear, hard-to-miss disclosure for sponsorships, paid relationships, free products, affiliate relationships, or brand control. Source: FTC endorsement guidance and Disclosures 101.
- Documented platform examples, verified 2026-07-11: YouTube has paid-promotion declarations; TikTok requires commercial-content disclosure for content promoting a brand/product/service; Instagram branded content policies require use of branded-content tools for branded content; LinkedIn says value-exchange posts must be labeled as brand partnerships. These platform facts are volatile; re-check platform help pages at production time.

Synthetic and altered-media disclosure:

- Documented platform examples, verified 2026-07-11: YouTube requires creators to disclose realistic altered or synthetic content in defined cases, and TikTok requires labeling AI-generated content that contains realistic images, audio, or video. Re-check the current upload workflow and policy text before publishing.
- If a synthetic narrator, cloned speaker voice, avatar, lip-sync, face swap, translated dub, AI filler word reconstruction, or generated b-roll depicts a real person or realistic event, require explicit approval and a disclosure plan.

Copyright and fair use:

- Documented fact, verified 2026-07-11: U.S. Copyright Office fair-use guidance says there is no fixed number of words, notes, or percentage that is automatically safe; fair use depends on circumstances. Do not present clip length as permission. Escalate permission/fair-use decisions to counsel or the rights owner.

Provenance:

- When available, preserve or attach provenance metadata. C2PA Content Credentials are a standards-based way to describe media origin and edit history, but metadata can be stripped by platforms or workflows; keep an internal ledger even when credentials are present.

## Quote selection: the context test

For every candidate quote, answer these before it can become a clip:

1. What is the speaker's exact claim in plain language?
2. What did the speaker say immediately before and after?
3. Would the speaker reasonably agree this clip represents their point?
4. Does the clip omit a qualification such as "in our pilot," "for this customer," "we think," "we failed first," or "not always"?
5. Does the hook/title/caption introduce a claim not present in the source?
6. Does the clip use music, reaction shots, zooms, or graphics to intensify emotion beyond the source?
7. Does this quote need factual, legal, sponsor, customer, or speaker approval?

Prefer quotes that:

- Contain one clear idea, tension, lesson, story turn, or useful answer.
- Start quickly or can be introduced with a truthful setup card.
- Have a natural ending, punchline, decision, proof, or invitation.
- Work without relying on the full episode.
- Include enough specifics to feel credible, but not so much private or regulated detail that approval becomes fragile.

Reject or repair quotes that:

- Depend on pronouns or missing referents that require misleading titles.
- Sound stronger when isolated than in context.
- Are transcript artifacts, jokes without context, sarcasm, or cross-talk.
- Include private data, medical/financial/legal advice, unpublished performance data, or third-party allegations without approval.
- Require sentence splicing that makes the speaker say a sentence they did not say.

## Clip structures

Use these as production heuristics, not mandatory formulas.

### Single insight vertical clip

- 0-2s: truthful hook from the speaker or a setup title.
- 2-8s: context needed to understand the quote.
- 8-35s: core insight, story, or answer.
- 35-50s: implication, lesson, or memorable line.
- Last 1-3s: clean end beat, branded outro, or platform-native CTA if approved.

### Two-speaker exchange

- Start with the question if it is short and necessary.
- Preserve the answer's target. Do not cut a question about one topic into an answer about another.
- Use speaker labels and lower thirds, especially in vertical crop where faces may alternate.
- Avoid reaction shots from a different moment unless labeled or neutral enough not to imply a response.

### Highlight reel or trailer

- Organize around a promise: "three hard lessons from scaling support," not "random best moments."
- Use a spine: problem -> tension -> proof -> consequence -> invite.
- Maintain chronological clarity if chronology matters. If using non-linear montage, do not imply events happened in the order shown.
- Use on-screen topic cards to prevent decontextualized quote stacking.

### Audiogram

- Use when the visual source is weak, audio-only, remote-call quality, or a podcast platform needs shareable video.
- Include waveform only if it helps motion; do not let it compete with captions.
- Use host/guest photos, title, episode art, and topic cards with rights-confirmed assets.
- Ensure captions and speaker IDs carry the experience for muted viewing.

### Customer/founder/testimonial clip

- Require release/approval for testimonial use.
- Preserve the actual experience and scope. Do not generalize a pilot/customer quote into a universal result.
- Add disclosure if there is a material connection or incentive.
- Submit claims, logos, customer name, metrics, and title/thumbnails for client/legal approval.

## Edit craft

### A-roll assembly

- Cut for clarity before pace. Remove dead air, false starts, and repetitions only when doing so preserves meaning.
- Keep breaths and micro-pauses where they support authenticity or comprehension.
- Use jump cuts confidently for social clips, but hide distracting cuts with scale changes, B-roll, caption beats, or J/L cuts when the face movement is jarring.
- Never combine words from separate contexts to create a new sentence unless it is purely grammatical cleanup and the result is transcript-verifiable.
- Use room tone or ambience under repaired gaps. Avoid hard digital silence.
- If cutting between speakers, preserve conversational rhythm. Do not make an answer appear more immediate, hostile, or enthusiastic than it was.

### B-roll, screen, slides, and graphics

- B-roll should clarify, evidence, or pace the spoken point. Do not use generic filler that changes the topic.
- Use product footage, slides, charts, screenshots, or customer logos only when rights and freshness are confirmed.
- Use text callouts for names, terms, numbers, and transitions; avoid restating every spoken word outside captions.
- Lower thirds should include speaker name and role as approved; avoid inflated titles.
- If adding stock or generated visuals, record provenance and ensure they do not depict real people/events as if they were source footage.

### Cropping and reframing

- Reframe from the highest-resolution source available.
- For two-person remote calls, consider dynamic crop switching only when it improves comprehension and does not feel like fake reaction editing.
- Keep faces, hand gestures, slide text, and captions inside platform safe areas.
- Avoid excessive punch-ins on sensitive, emotional, or serious statements; they can editorialize the tone.

## Captions and accessibility

Documented facts, verified 2026-07-11:

- WCAG 2.2 Success Criterion 1.2.2 requires captions for prerecorded audio content in synchronized media, with exceptions for media alternatives.
- W3C understanding guidance says captions include dialogue, identify who is speaking, and include non-speech sound information needed to understand the content.
- WCAG includes transcript and audio-description/media-alternative requirements for some media contexts.

Caption workflow:

1. Generate captions from the verified transcript, not from a rough draft.
2. Correct names, jargon, product terms, numbers, and homophones manually.
3. Include speaker IDs when the speaker is not visually obvious or when the clip is audio-only/audiogram style.
4. Include meaningful non-speech audio when relevant, such as "[laughter]," "[applause]," or "[door closes]" if it affects meaning.
5. Keep caption lines readable. Use natural phrase breaks; do not split names, numbers, or dependent clauses awkwardly.
6. Use high contrast, sufficient size, and safe placement. Avoid hiding captions behind platform UI, lower thirds, progress bars, or auto-generated overlays.
7. Deliver both burned-in captions for social clips and sidecar captions (SRT/VTT) when the platform or client can use them.
8. For multilingual captions or translated cutdowns, verify translation against the source meaning and get approval for sensitive claims.

## Audio cleanup and loudness

Documented facts, verified 2026-07-11:

- ITU-R BS.1770 specifies algorithms for measuring programme loudness and true-peak level.
- EBU loudness guidance describes R 128 normalization around -23 LUFS for broadcast-style workflows.
- ATSC A/85 provides loudness guidance for television and streaming-media service providers.

Production heuristics for social and web cutdowns:

- Prioritize intelligibility of speech over loud music or heavy compression.
- Repair in this order: remove hum/clicks/plosives where possible, reduce broadband noise conservatively, de-reverb if needed, balance speakers, EQ for clarity, compress lightly, limit true peaks, then loudness-normalize.
- For web/social delivery where no client spec exists, a practical target is often around -14 to -16 LUFS integrated with true peak at or below -1 dBTP. Treat this as a platform-era heuristic, not a legal or universal standard.
- For broadcast, OTT, paid media, or client delivery, use the required spec exactly; do not substitute social loudness targets.
- Check the final export, not only the timeline mix. Captions, stingers, end cards, and music beds can change measured loudness.

Audio QA:

- No clipped syllables at edit points.
- No denoise warble or underwater artifacts on speech.
- Speakers balanced within the clip.
- Music ducks under dialogue and never hides required disclosure.
- Endings do not cut off breaths, laughs, or final consonants.

## Platform variants

Platform specs and policy workflows change. Re-check official documentation at production time, especially duration limits, monetization rules, ad/sponsorship labels, AI labels, music libraries, safe zones, and upload classifications.

Stable production planning:

- Vertical social: 9:16 master, face-safe crop, large captions, quick hook, no reliance on description text.
- Square feed/audiogram: 1:1 or 4:5 when useful, stronger title card, captions with speaker IDs.
- Horizontal/YouTube/webinar: 16:9, more room for slides and lower thirds, sidecar captions, chapters if needed.
- LinkedIn/business feed: often benefits from a context title card and a less frantic cut than TikTok/Reels.
- Podcast platforms: prioritize clean audio, waveform/episode art, and descriptive titles.

Documented platform examples, verified 2026-07-11:

- YouTube Help says the standard desktop aspect ratio is 16:9 and provides recommended resolutions; YouTube Shorts help describes square or vertical Shorts up to three minutes, with eligibility details and Content ID caveats.
- Instagram Help says Reels can be uploaded within a range of aspect ratios and gives minimum frame-rate/resolution guidance.

Do not assume these remain current. Confirm at upload time.

## Synthetic voice, avatar, and translation boundaries

Allowed only with explicit scope:

- Noise repair that does not alter words.
- Caption cleanup that corrects transcription errors.
- Translation subtitles with human or qualified review.
- Generated title cards, diagrams, or abstract B-roll that does not imply recorded reality.

Requires explicit speaker/rights-holder approval and disclosure plan:

- Voice cloning, voice replacement, speech synthesis in a real person's voice, translated dubbing that sounds like the speaker, lip-sync, face swap, avatar recreation, synthetic pickup lines, synthetic reaction shots, or generated footage of a real event/person.

Forbidden without a specific, approved ethical/legal basis:

- Creating new statements from a speaker.
- Making a guest endorse a product, candidate, company, or claim they did not endorse.
- Removing qualifications from medical, financial, legal, employment, or investment advice.
- Replacing a speaker's emotion, identity, or appearance in a way that could deceive viewers.

## Review workflow

Prepare a review packet for every externally published recut:

```text
deliverable_id:
  export_path:
  target_platform:
  duration:
  aspect_ratio:
  source_timecodes:
  transcript_excerpt:
  edit_summary:
  title:
  thumbnail_text:
  caption_file:
  disclosure_text_or_platform_toggle:
  music_and_asset_rights:
  approvals_needed:
  qa_status:
```

Minimum review passes:

1. Editorial review: Does the clip preserve meaning, context, speaker identity, and chronology?
2. Transcript review: Are captions and titles accurate?
3. Rights/disclosure review: Are releases, licenses, commercial disclosures, AI labels, and platform toggles handled?
4. Technical review: Audio, captions, safe zones, export settings, thumbnail, and playback.
5. Stakeholder approval: Speaker/client/legal/brand/compliance where required.

Use timecoded review comments. Never ask reviewers to approve a batch without source timecodes for each clip.

## Delivery package

Deliver:

- Final exports named by date, source, platform, aspect ratio, duration, and version.
- Sidecar captions where useful: `.srt` or `.vtt`.
- Thumbnail or cover frame, if requested.
- Text copy: title, description, hashtags, disclosure text, alt text if applicable.
- Source timecode ledger for every quote.
- Rights/provenance ledger for source media, music, B-roll, generated media, captions, and graphics.
- QA report and unresolved risk notes.

Example naming:

```text
2026-07-11_founder-podcast_clip01_activation-pilot_9x16_42s_v03.mp4
2026-07-11_founder-podcast_clip01_activation-pilot_captions_v03.srt
2026-07-11_founder-podcast_recut-ledger_v03.csv
```

## Recut QA checklist

Editorial integrity:

- The clip's apparent claim matches the source.
- No missing qualifier changes meaning.
- The title, hook, thumbnail, and captions do not overstate the quote.
- Reaction shots and B-roll are from the correct context or are clearly neutral.
- Speaker names, roles, and pronouns are correct.

Rights and compliance:

- Source use is authorized for the intended channel and purpose.
- Participant release/approval is present where required.
- Commercial, sponsorship, endorsement, or material-connection disclosures are handled.
- Synthetic/altered media labels are handled when required.
- Music, images, slides, screenshots, logos, and stock/generated assets have a rights/provenance entry.
- Legal/compliance review has happened for high-risk categories.

Accessibility and captions:

- Captions match the final audio.
- Captions include necessary speaker IDs and meaningful non-speech audio.
- Captions are readable in the target crop and not hidden by UI.
- Sidecar captions are included when needed.
- Descriptive transcript or audio-description needs were considered for the delivery context.

Technical:

- Correct aspect ratio, resolution, frame rate, codec, and duration for the target.
- Faces, graphics, and captions are in safe areas.
- Audio is intelligible, balanced, and not clipped.
- Loudness meets client/platform spec or stated heuristic.
- No flash frames, black frames, offline media, watermarks, dropped captions, or export glitches.

## Example: podcast interview to three vertical clips

Production intent: Turn a 72-minute founder podcast into three 30-60 second vertical clips for organic LinkedIn, YouTube Shorts, and Instagram Reels.

Inputs:

- 4K two-camera recording.
- Separate host and guest WAV files.
- Topic: reducing onboarding friction in enterprise SaaS.
- Constraint: no paid promotion; guest approval required before posting.

Workflow:

1. Ingest source and preserve originals.
2. Transcribe and diarize. Manually verify the guest's name and company.
3. Search transcript for "mistake," "pilot," "customer," "activation," and "what changed."
4. Select quotes only where "pilot" remains clear, because the source result was not a full-company metric.
5. Build three clip candidates:

```text
clip_01:
  hook: "We doubled activation by deleting setup steps."
  correction: Use "In one pilot, activation doubled after we deleted setup steps."
  source: 00:18:09.4-00:19:02.0
  context_needed: guest says enterprise admins only
  approvals: metric approval from guest/company

clip_02:
  hook: guest's own line "The hardest onboarding step was the one we loved most."
  source: 00:31:44.1-00:32:26.7
  context_needed: none beyond lower third
  approvals: guest review

clip_03:
  hook: host question "What did you remove first?"
  source: 00:33:12.0-00:34:05.5
  context_needed: include question, answer depends on it
  approvals: guest review
```

Edit decisions:

- Export 9:16 from the 4K guest camera with occasional split-screen question setup.
- Use burned-in captions, sidecar SRT, guest lower third on first appearance, and topic card before each clip.
- Use no B-roll for clip 02 because the facial performance carries the story.
- Use product UI B-roll for clip 01 only if the product owner approves the shown screen.
- Audio target: client has no spec; use social heuristic around -14 to -16 LUFS integrated, true peak no higher than -1 dBTP, then verify final exports.

Expected result:

- Three truthful clips that can stand alone.
- Review packet includes source timecodes, transcript excerpt, proposed titles, captions, and approval flags.

Likely failure modes:

- "Doubled activation" title omits "pilot" and becomes misleading.
- Dynamic crop cuts off captions under Instagram UI.
- Product B-roll shows unreleased UI.

## Example: customer call to testimonial cutdown

Production intent: Create a 45-second sales/social proof clip from a recorded customer call.

Inputs:

- Zoom recording with account executive, customer champion, and two silent attendees.
- Customer says: "We cut reporting time in half after switching."
- Intended use: paid LinkedIn ad and sales page.

Decision:

- Pause before edit until testimonial release, company name/logo approval, metric approval, and paid-ad disclosure plan are confirmed. This is not just an editorial clip; it is a commercial endorsement/testimonial.

Safe edit structure after approvals:

```text
0-3s: Title card: "How [Customer] reduced weekly reporting work"
3-8s: Customer context: role/team, approved lower third
8-28s: Verbatim quote with "for our weekly reporting workflow" preserved
28-38s: One concrete workflow detail
38-45s: Approved CTA or end card
```

Do not:

- Use silent attendee faces without permission.
- Turn "reporting time" into "all analytics work."
- Add synthetic voiceover in the customer's voice.
- Use the quote in paid media without disclosure and platform ad-policy review.

## Example: webinar to highlight reel plus audiogram

Production intent: Turn a 58-minute technical webinar into a 90-second horizontal highlight reel and a 40-second audiogram for social.

Inputs:

- Webinar recording with slides, host intro, three experts, audience Q&A.
- Some audience names appear in chat.

Workflow:

1. Ingest video and slide deck. Confirm slide/logo rights and whether audience Q&A can be public.
2. Transcribe, diarize, and separate expert sections from audience sections.
3. Pick a highlight spine: "why the old architecture broke," "what changed," "what teams should do next."
4. Remove housekeeping and chat names.
5. Use slide excerpts only where they match the spoken claim and remain legible at 16:9.
6. For audiogram, use approved episode art plus captions and speaker labels, not tiny webinar slides.
7. Include sidecar captions for the website upload.

QA emphasis:

- Captions include speaker IDs because three experts appear.
- Audio levels are matched across panelists.
- The title does not imply the experts made a stronger recommendation than they did.
- The review packet marks any audience question as "do not use" unless consent exists.

## Sources and verification notes

Sources below were consulted for consequential factual claims. Volatile platform rules were verified on 2026-07-11 and must be re-checked at production/upload time.

- FTC, "FTC's Endorsement Guides: What People Are Asking" (https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) and "Disclosures 101 for Social Media Influencers" (https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers): material-connection and endorsement disclosure guidance.
- W3C WCAG 2.2 (https://www.w3.org/TR/WCAG22/), WAI Understanding SC 1.2.2 (https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html), and WAI Understanding SC 1.2.5 (https://www.w3.org/WAI/WCAG22/Understanding/audio-description-prerecorded.html): captions, speaker identification, non-speech audio, transcripts, and audio description.
- ITU-R BS.1770 (https://www.itu.int/rec/R-REC-BS.1770), EBU R 128 loudness resources (https://tech.ebu.ch/groups/loudness), and ATSC A/85 (https://www.atsc.org/atsc-documents/a85-techniques-for-establishing-and-maintaining-audio-loudness-for-digital-television/): loudness measurement and broadcast/streaming loudness guidance.
- YouTube Help: paid promotion/altered-content upload settings (https://support.google.com/youtube/answer/57404), altered or synthetic content disclosure (https://support.google.com/youtube/answer/14328491), three-minute Shorts guidance (https://support.google.com/youtube/answer/15424877), and video aspect-ratio guidance (https://support.google.com/youtube/answer/6375112).
- TikTok Support and TikTok Ads Help: commercial content disclosure (https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/promoting-a-brand-product-or-service), AI-generated content labeling (https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content), and commercial music notes (https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/commercial-use-of-music-on-tiktok).
- Instagram Help Center: branded-content policies (https://help.instagram.com/1695974997209192), paid-partnership labels (https://help.instagram.com/1317960375957564/), and Reels size/aspect-ratio guidance (https://help.instagram.com/1038071743007909).
- LinkedIn Help: brand partnership label (https://www.linkedin.com/help/linkedin/answer/a1627083) and Advertising Policies (https://www.linkedin.com/legal/ads-policy).
- U.S. Copyright Office fair use guidance (https://www.copyright.gov/fair-use/ and https://www.copyright.gov/help/faq/faq-fairuse.html) and AI/copyright resources (https://www.copyright.gov/ai/): fair use and AI/copyright context.
- C2PA specification (https://spec.c2pa.org/) and Content Authenticity Initiative resources (https://contentauthenticity.org/): provenance metadata and content authenticity.
