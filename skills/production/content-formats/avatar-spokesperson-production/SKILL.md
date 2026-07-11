---
name: avatar-spokesperson-production
description: Provider-independent production workflow for AI avatar spokesperson videos, including presenter briefs, consent and likeness rights, disclosure and platform labeling, casting, localization, performance direction, brand fit, claims review, lip-sync/audio QA, accessibility, approvals, and delivery packages. Use when creating synthetic presenter videos, corporate explainers, training modules, sales/support avatars, localization spokespeople, product announcements, compliance videos, or social avatar clips.
---

# Avatar Spokesperson Production

Use this skill to plan, direct, review, and package synthetic presenter videos where a humanlike avatar or digital spokesperson speaks to the viewer. It is provider-independent: adapt the workflow to the avatar, TTS, dubbing, lip-sync, compositing, or platform tools available in the current environment.

Do not treat avatar production as only a prompt-writing task. The core production risks are identity rights, audience transparency, claims accuracy, performance credibility, brand trust, localization, and QA.

This skill is not legal advice. When rights, advertising claims, union/talent terms, regulated industries, minors, political/civic content, health/financial claims, public figures, or deceased personalities are involved, escalate to the client, counsel, brand owner, performer/voice owner, or compliance reviewer before generation or publication.

## Non-negotiable production boundaries

Separate documented facts, project requirements, and production heuristics:

- Documented fact: cite a source or project artifact.
- Project requirement: comes from the client brief, contract, brand guide, legal review, consent form, platform spec, or tool documentation.
- Production heuristic: a practical quality rule that improves outcomes but is not a legal or technical requirement.

Before generation, confirm:

1. The avatar and voice are licensed or consented for this use, audience, territory, duration, channels, languages, and editing scope.
2. The video will not imply a real person, employee, expert, customer, celebrity, government official, medical/legal/financial professional, or organization endorsed a claim unless that is true and approved.
3. Required AI/synthetic-media disclosures and platform labels are planned.
4. Objective claims have substantiation and high-risk claims have the right approval.
5. The script, pronunciation list, performance direction, wardrobe/background, captions, and delivery variants are production-ready.

## First pass: classify the avatar job

Capture these fields before selecting tools or writing prompts:

```yaml
project:
  goal: "What business or learning outcome must the avatar achieve?"
  audience: "Who is watching, where, and what do they already believe?"
  format: "corporate explainer | training | sales | support | localization | announcement | compliance | social"
  channels: ["landing page", "YouTube", "TikTok", "LinkedIn", "LMS", "internal portal"]
  duration_targets: ["primary 60s", "vertical 30s cutdown", "6s hook"]
  risk_level: "low | moderate | high"
persona:
  role: "host | instructor | support agent | product manager | executive proxy | narrator"
  identity_type: "licensed real person | synthetic non-identifiable avatar | employee likeness | public figure likeness"
  voice_type: "licensed human voice | synthetic voice | cloned voice | recorded actor | localized dub"
  consent_artifacts: ["contract", "release", "usage limits", "revocation/expiry terms"]
content:
  script_source: "new | client-provided | translated | regulated/compliance"
  claims_inventory: ["all objective claims, endorsements, statistics, comparisons"]
  forbidden_implications: ["what the avatar must not appear to say, endorse, or represent"]
localization:
  languages: ["en-US"]
  pronunciation_list: ["brand names", "people names", "acronyms", "technical terms"]
  cultural_notes: ["gestures", "formality", "dress", "examples to avoid"]
approvals:
  required_reviewers: ["brand", "legal", "compliance", "talent/performer", "regional reviewer"]
```

Set `risk_level` to high if any of the following apply: public figure or employee likeness; cloned voice; medical, legal, financial, political, employment, housing, education, or safety claims; children or vulnerable audiences; synthetic expert/customer testimonials; regulated training; crisis communications; international release; or a platform where synthetic-media policy is material to distribution.

## Rights, consent, and likeness review

Treat avatar identity and voice as separate rights surfaces. A realistic face, body, voice, name, title, uniform, accent, and mannerism can each create audience assumptions.

Minimum consent packet for a real or cloned person:

- Written permission for avatar/voice capture, model creation if applicable, generation, editing, storage, and distribution.
- Specific permitted uses: product, campaign, client, channels, territories, languages, duration, paid media, organic social, internal training, and derivatives.
- Explicit prohibited uses: political persuasion, adult content, medical/financial advice, competitive brands, crisis statements, new scripts after expiry, model training, face/voice transfer, or unsupervised self-service.
- Compensation, revocation, renewal, exclusivity, takedown, and audit terms.
- Approval workflow for scripts, likeness, voice, translated performances, and final cuts.
- Security requirements for source recordings, voiceprints, face scans, prompts, project files, and generated takes.

SAG-AFTRA summarizes its AI guardrails as consent, fair compensation, and control over performances. NAVA recommends performer contracts cover consent, use limits, opt-out or term limits, payment, exclusivity, and safe storage/tracking of voice, likeness, performance, and resulting products. Use these as production governance principles even when the project is non-union, then defer to the actual contract and counsel for binding terms.

For a synthetic non-identifiable avatar, still check whether the avatar resembles a real person, implies a protected role, or uses a voice trained on identifiable speakers. Do not describe a synthetic avatar as an actual employee, doctor, customer, founder, or public official unless the identity and approval are real.

## Disclosure and labeling plan

Plan disclosure as part of the creative, not as an afterthought. The disclosure should be clear enough that an ordinary viewer understands that the presenter is synthetic or AI-generated when that fact is material to trust, identity, or platform policy.

Good disclosure locations:

- Opening or lower-third text for high-risk or testimonial-like content: "AI-generated avatar spokesperson."
- End card or description for lower-risk internal explainers: "Presenter video created using an AI avatar and synthetic voice."
- Platform-specific upload toggles or AI labels.
- Campaign trafficking notes so paid-media, social, and web teams do not strip the disclosure.

Avoid disclosures that are tiny, fleeting, hidden behind a click, contradicted by the script, or placed only after a misleading impression has already formed.

For advertising and endorsements, the FTC endorsement guides address endorsements and material connections under Section 5, and FTC advertising substantiation policy requires a reasonable basis for objective claims. If an avatar states a product claim, expert opinion, customer experience, ranking, statistic, savings number, health/safety outcome, or comparative superiority claim, the client must provide support before publication. Do not let the realism of an avatar create a fake testimonial or expert endorsement.

Platform and legal rules change. Re-check platform synthetic-media requirements at production time, especially for YouTube, TikTok, Instagram/Facebook, paid ads, app stores, LMS platforms, and regional variants. As verified on 2026-07-11: YouTube requires disclosure for realistic altered/synthetic content viewers could mistake for a real person, place, scene, or event; TikTok requires labels for AI-generated content containing realistic images, audio, or video; Meta describes "AI info" labels based on industry-standard signals and self-disclosure for AI-generated or AI-modified video, audio, and image content. Treat these facts as volatile.

## Script and persona brief

Write for an avatar like a camera-facing presenter, not a generic narrator. The script should be easy to perform in one breath group at a time and should not require facial nuance the avatar cannot deliver.

Create a persona brief:

```yaml
persona_brief:
  speaker_role: "Calm onboarding coach for new enterprise users"
  audience_relationship: "helpful peer, not executive authority"
  credibility_basis: "company-approved training host; not a real customer or lawyer"
  warmth: "medium-high"
  formality: "plain professional"
  pace: "145 words per minute target; slower for compliance terms"
  energy: "confident but not salesy"
  eye_line: "direct-to-camera for explanations; glance down only for quoted checklist moments"
  gestures: "small open-hand emphasis on transitions; no pointing at viewer"
  wardrobe: "solid navy blazer, no lab coat or official uniform"
  background: "brand-neutral office gradient, no fake newsroom/clinic/courtroom"
  forbidden_read: "must not appear to be a real employee giving legal advice"
```

Script rules:

- Put the key promise in the first 3-5 seconds for social and product announcements.
- Keep sentences short. Prefer one idea per sentence.
- Use contractions only if appropriate to brand voice and localization.
- Avoid tongue-twisters, repeated sibilants, awkward alliteration, and dense clauses near visual transitions.
- Spell out numbers and units when TTS may misread them: "twenty-four seven," "SOC two," "A P I."
- Mark pronunciation: `OpenMontage (OH-pun mon-TAHZH)`, `GDPR (G D P R)`, `SaaS (sass)`.
- Mark pauses and emphasis sparingly: `[beat]`, `[slower]`, `[smile]`, `[firm]`.
- Avoid saying the avatar has personal experience unless the experience belongs to the actual licensed person and is approved.

For compliance or training modules, separate "must-say" approved copy from optional connective tissue. Do not paraphrase regulated language unless the compliance reviewer approves.

## Casting and representation

Casting should support comprehension and trust without tokenism, stereotype, deception, or false authority.

Check:

- Does the avatar's apparent age, role, attire, accent, and setting imply credentials or lived experience?
- Would the same script be appropriate if spoken by a real person with this identity presentation?
- Is the avatar being used to simulate a customer, patient, student, doctor, lawyer, public official, or worker? If yes, require review.
- Are race, gender, disability, accent, nationality, body type, or dress being used as shorthand for trust, expertise, service labor, or exoticism?
- Does localization adapt persona, formality, gestures, examples, and pronunciation rather than merely translating words?

Prefer role clarity over realism. "Synthetic product guide" is often safer and more honest than "AI customer testimonial."

## Performance direction

Avatar providers vary in how much control they expose. Even when controls are limited, write direction in production language so the prompt, script markup, and review are aligned.

Direct:

- Eye-line: direct, slightly off-camera interview, teleprompter, or screen-pointing.
- Gesture density: none, low, medium, high. Corporate explainers usually need low-to-medium gestures; compliance videos usually need low gestures.
- Facial expression: neutral, warm, reassuring, serious, celebratory. Avoid rapid emotional shifts.
- Head movement: stable for authority, mild nods for support, no bobbing.
- Pacing: words per minute, pauses after section headers, slower pronunciation for names, acronyms, and legal language.
- Shot type: bust, waist-up, full-body, seated, standing, picture-in-picture, screen-side presenter.
- Interaction with graphics: indicate whether the avatar should point, glance, or leave space for overlays. If the provider cannot reliably coordinate gaze/gesture with graphics, use post-production graphics instead of generated pointing.

Break long scripts into takes. Generate and review 10-20 second segments for high-risk work before committing to a full-length render. For localization, generate a short proof clip per language that includes the hardest names, numbers, and claims.

## Wardrobe, background, and brand fit

Make the avatar fit the brand without implying unauthorized affiliation or credentials.

Wardrobe:

- Use solid colors and simple patterns to reduce rendering artifacts.
- Avoid uniforms, badges, lab coats, judicial robes, military/police-like attire, or branded logos unless authorized and needed.
- Avoid jewelry or fine patterns that shimmer or deform during lip-sync.

Background:

- Choose a setting that matches the promise: product UI, support desk, training room, neutral studio, event announcement, or brand gradient.
- Avoid fake newsrooms, clinics, courtrooms, government offices, exchange trading floors, or classrooms when they imply authority the avatar does not have.
- Leave safe zones for captions, lower thirds, platform UI, and crop variants.

Brand:

- Apply brand colors to background, lower thirds, slides, and supers rather than forcing the avatar to wear logo-heavy clothing.
- Keep contrast high enough for captions and titles.
- Ensure product screenshots, UI states, prices, and legal footers are current and approved.

## Claims, endorsements, and sensitive-content review

Create a claims inventory before production:

```yaml
claims_inventory:
  - script_line: "Cut onboarding time by 40%."
    claim_type: "objective performance claim"
    substantiation: "client study Q2 2026, approved by marketing/legal"
    risk: "moderate"
    reviewer: "legal"
  - script_line: "I recommend this to every sales team."
    claim_type: "endorsement/testimonial"
    substantiation: "none"
    action: "rewrite; avatar cannot imply personal recommendation"
```

Escalate if the avatar:

- Says "I tried," "my patients," "my clients," "as your doctor/lawyer/advisor," "we guarantee," or "officially approved" without proof.
- Mentions prices, discounts, availability, earnings, savings, performance, safety, health outcomes, environmental benefits, or comparative superiority.
- Looks or sounds like a real person who did not approve the exact use.
- Speaks about political, civic, emergency, medical, legal, financial, employment, housing, education, or insurance decisions.
- Is used in paid advertising, influencer-style content, testimonials, or native ads.

Rewrite synthetic endorsements into transparent brand narration:

- Risky: "I use Acme every day, and it saved me four hours."
- Safer: "Acme's customer study found an average four-hour weekly time savings among surveyed teams."
- Risky: "As your financial advisor, I recommend this plan."
- Safer: "This explainer is not financial advice. Review the plan details with a qualified advisor."

## Localization and pronunciation

Localization quality is a trust issue. A visually polished avatar with wrong pronunciation or culturally odd gestures feels deceptive or careless.

For each language or market:

- Use an approved translation or transcreation, not raw machine translation for customer-facing or regulated work.
- Create a pronunciation table for brand names, product names, people, places, acronyms, numbers, and domain terms.
- Confirm locale-specific formality, honorifics, units, currency, date formats, privacy terms, and examples.
- Check gesture norms. A gesture that reads friendly in one market can read dismissive or confusing in another.
- Decide whether to use the same avatar across markets or localize presenter appearance/voice. Do not assume one avatar is culturally neutral.
- Generate a proof segment that contains the hardest words and a representative emotional passage.
- Have a native or market-qualified reviewer approve audio, captions, on-screen text, and any mouth-shape oddities.

Keep source text, translated script, back-translation notes, pronunciation dictionary, voice/avatar choice, and reviewer signoff in the delivery record.

## Lip-sync, audio, and visual QA

Review avatar video at normal speed, half speed, and with audio-only playback.

Lip-sync and face:

- Mouth closures match `p`, `b`, `m`; teeth/tongue do not flicker unnaturally.
- No frozen smile during serious statements.
- No eye drift, dead stare, excessive blinking, crossed gaze, or asynchronous head nods.
- No face warping, jaw sliding, hairline crawl, hand/finger deformation, or clothing shimmer.
- Emotion matches script section and brand tone.

Audio:

- Voice matches approved persona and rights.
- Pronunciation is correct for names, numbers, acronyms, product terms, and localized terms.
- Pace is intelligible. Dense compliance lines should be slower than hype lines.
- No clipping, room mismatch, hiss, abrupt breaths, tonal jumps, or segment seams.
- Loudness is consistent across segments and variants.

Edit/composite:

- Lower thirds do not cover the mouth, hands, or required disclosure.
- Captions avoid the face and platform UI safe zones.
- Product screenshots and claims match the latest approved source.
- Cuts do not create misleading statements by removing qualifiers.
- Watermarks, provenance metadata, or labels required by the provider/platform are preserved when required.

If a defect affects consent, disclosure, claims, or identity, do not "fix in post" without re-approval. Regenerate or escalate.

## Accessibility and captions

For prerecorded synchronized media, WCAG 2.2 Success Criterion 1.2.2 requires captions for audio content, with exceptions for media alternatives clearly labeled as such. Use this as a baseline for avatar videos even when the distribution channel is not a website.

Caption package:

- Accurate dialogue, not paraphrase for compliance or training.
- Speaker identification when more than one speaker or off-screen voice appears.
- Meaningful non-speech audio cues when relevant: `[music fades]`, `[alert tone]`.
- Timing synchronized to speech and readable at platform size.
- Placement that avoids mouth, lower-third disclosure, product UI, and platform overlays.
- Burned-in captions for social variants when silent autoplay is likely; sidecar SRT/VTT for platforms and LMSs that support it.

Also consider audio description or an equivalent text transcript if visual information not spoken by the avatar is necessary to understand the video.

## Approval workflow

Use gates. Do not wait until the final render to discover a rights or compliance problem.

Recommended gates:

1. Brief approval: goal, audience, channel, risk level, avatar identity, voice identity, disclosure plan, claims inventory, required reviewers.
2. Script approval: exact spoken copy, pronunciation list, claims substantiation, disclaimer/disclosure text, localization plan.
3. Look/performance approval: avatar, wardrobe, background, shot framing, voice, gesture level, proof clip.
4. Rough cut approval: timing, graphics, captions, claims context, lip-sync quality, platform variants.
5. Final compliance approval: final files, labels/toggles, metadata/provenance, captions/transcripts, usage restrictions, expiry/takedown notes.

Record approvals with dates and scope. If the script, avatar, voice, language, channel, claim, edit, or disclosure changes after approval, route back to the affected reviewer.

## Delivery package

Deliver more than one MP4 when the project will be distributed across channels.

Include:

- Master file: high-quality MP4 or MOV with approved audio mix.
- Platform variants: 16:9, 9:16, 1:1, short cutdowns, silent-autoplay captioned version, no-caption master if needed.
- Caption files: SRT/VTT per language plus burned-in variants when requested.
- Transcript: final spoken text with disclosure and disclaimer text.
- Claims record: claim inventory and substantiation references, or a note that claims were client-provided and approved.
- Rights record: avatar/voice source, consent scope, restrictions, expiry, territories, channels, derivative limits, and reviewer approvals.
- Localization record: scripts, pronunciation dictionaries, reviewer signoffs.
- Provenance record: tools/providers used, model or voice/avatar identifiers where available, generation dates, prompt/direction summaries, edits, and content credentials or other provenance metadata if supported.
- Publishing notes: platform AI labels/toggles to set, description disclosure text, thumbnail safe zones, paid-media restrictions, takedown/expiry reminders.

## Example: corporate onboarding avatar

Production intent: a 90-second internal onboarding video introducing a new expense workflow.

Approach:

- Use a synthetic non-identifiable avatar, not an employee likeness, to avoid implying a real HR representative said every line.
- Persona: calm onboarding coach, medium warmth, direct eye-line, low gestures.
- Disclosure: internal LMS description and end-card note: "This training presenter is an AI-generated avatar."
- Claims: avoid "this will reimburse you faster"; use "the new workflow is designed to reduce manual review steps."
- Accessibility: SRT/VTT for the LMS, burned captions for mobile viewing, transcript attached.
- Approval gates: HR owner approves script; brand approves wardrobe/background; compliance approves policy language.

Example direction:

```text
Create a waist-up AI avatar presenter in a neutral modern office setting with soft brand-blue accents. The presenter is a synthetic training host, not a real employee. Tone: clear, calm, reassuring, professional. Eye-line: direct to camera. Gesture density: low; small open-hand gestures only at section transitions. Wardrobe: solid navy blazer, no badges, no logo shirt. Pace: about 140 words per minute, with a short pause after each numbered step. Keep the lower third and bottom 20% of frame free for captions.

Script excerpt:
"Welcome to the new expense workflow. [beat] This training presenter is AI-generated, and the process details have been approved by the People Operations team. Starting August first, submit travel receipts through the Expenses tab. The system will ask three questions: the trip name, the business purpose, and whether a client attended. [slower] If a receipt is missing, add a note before you submit."
```

Expected QA focus: pronunciation of policy terms, no fake employee implication, captions clear on mobile, product UI screenshots current, no promise of faster reimbursement unless substantiated.

## Example: multilingual support avatar

Production intent: product support videos in English, Spanish, and Japanese.

Approach:

- Use a synthetic support guide with localized voice per language.
- Generate 12-second proof clips first: product name, hardest support term, a number, and a reassuring sentence.
- Maintain visual consistency across markets but adjust formality and examples.
- Use market reviewers for pronunciation, captions, cultural tone, and support terminology.

Example localization record:

```yaml
termbase:
  "OpenMontage": "OH-pun mon-TAHZH; do not translate"
  "workspace": "approved localized product term per market glossary"
  "render": "use product glossary term, not literal machine translation"
proof_clip_lines:
  en-US: "OpenMontage keeps your workspace renders organized, even when a project has multiple language versions."
  es-MX: "OpenMontage organiza los renders del espacio de trabajo, incluso cuando un proyecto tiene varias versiones de idioma."
  ja-JP: "OpenMontage wa, fukusu no gengo versions ga aru project demo, workspace renders o seiri shimasu. (Example romanized placeholder; use approved Japanese copy in production.)"
reviewers:
  required: ["regional support lead", "native-language reviewer", "brand"]
```

Expected QA focus: natural localized phrasing, mouth-shape acceptability, no mismatched captions, correct UI language, correct formality.

## Example: product announcement social avatar

Production intent: 30-second vertical launch clip for LinkedIn, Instagram Reels, TikTok, and YouTube Shorts.

Approach:

- Use a clearly synthetic product guide rather than a fake founder or customer.
- Put the hook and disclosure early because social viewers may not read descriptions.
- Re-check platform AI-label requirements immediately before posting.
- Maintain safe zones for captions and app UI.
- Build cutdowns from an approved master rather than rewriting claims per platform.

Example opening:

```text
[On-screen lower third for first three seconds: "AI-generated product guide"]

"Meet the new release in thirty seconds. [beat] OpenMontage now helps teams review avatar videos before they publish: script, captions, claims, and platform labels in one approval flow."
```

Claims review:

- If saying "first," "best," "only," "saves hours," or "enterprise-grade," require substantiation.
- If using a customer logo, quote, screenshot, or result, require customer permission and context.
- If the video is paid media, ensure the paid social team receives the disclosure and labeling notes.

## Source anchors

Verified on 2026-07-11 unless noted. Re-check volatile platform/provider rules at production time.

- FTC, "Guides Concerning the Use of Endorsements and Testimonials in Advertising," 16 CFR Part 255, effective 2023-07-26: https://www.federalregister.gov/documents/2023/07/26/2023-14795/guides-concerning-the-use-of-endorsements-and-testimonials-in-advertising
- FTC, "Policy Statement Regarding Advertising Substantiation": https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation
- FTC, "Native Advertising: A Guide for Businesses": https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses
- YouTube Help, "Disclosing use of GenAI content": https://support.google.com/youtube/answer/14328491
- YouTube Blog, "How we're helping creators disclose altered or synthetic content," 2024-03-18: https://blog.youtube/news-and-events/disclosing-ai-generated-content/
- TikTok Support, "About AI-generated content": https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content
- TikTok Newsroom, "New labels for disclosing AI-generated content," 2023-09-19: https://newsroom.tiktok.com/new-labels-for-disclosing-ai-generated-content
- Meta, "Our Approach to Labeling AI-Generated Content and Manipulated Media," 2024-04-05, updated 2024-09-12 on "AI info" label placement: https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/
- SAG-AFTRA, "Artificial Intelligence": https://www.sagaftra.org/contracts-industry-resources/member-resources/artificial-intelligence
- NAVA, "Synth & AI": https://navavoices.org/synth-ai/
- W3C, WCAG 2.2 Success Criterion 1.2.2 Captions (Prerecorded): https://www.w3.org/TR/WCAG22/#captions-prerecorded
- FCC consumer guide, "Closed Captioning on Television," for caption quality concepts: https://www.fcc.gov/consumers/guides/closed-captioning-television
- U.S. Copyright Office, "Copyright and Artificial Intelligence": https://www.copyright.gov/ai/
- C2PA Specifications, content provenance standard overview: https://spec.c2pa.org/specifications/specifications/2.4/index.html
