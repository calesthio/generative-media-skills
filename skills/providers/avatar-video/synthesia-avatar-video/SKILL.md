---
name: synthesia-avatar-video
description: Produce presenter-led AI avatar videos with Synthesia Studio and Synthesia API. Use for Synthesia-specific avatar video planning, avatar/voice/language selection, scripted scenes, template personalization, API job lifecycle, localization/dubbing, brand/training/product workflows, consent/rights/safety checks, artifact custody, troubleshooting, and final QA.
---

# Synthesia avatar video production

Use Synthesia when the job is a business, training, product, sales, onboarding, knowledge-base, or localized presenter video where a controlled avatar performance, brand consistency, and scalable variants matter more than cinematic freeform motion. Treat Synthesia as a synthetic presenter studio and templated video automation system, not as a general text-to-video model.

Facts in this skill were verified against official Synthesia documentation, API reference, pricing, and policy pages on 2026-07-10. Re-check volatile items before committing money or a production launch: plan access, quotas, supported languages, avatar IDs, voice IDs, endpoint schemas, template variables, processing times, pricing, and policy text.

## Route the work

Use this skill for:

- Synthesia Studio videos made manually from scenes, scripts, templates, avatars, brand kits, media, captions, and translations.
- Synthesia API videos from scratch through `POST /v2/videos`.
- Synthesia API videos from published templates through `POST /v2/videos/fromTemplate`.
- Personalized batches where variables drive names, roles, product details, CTAs, languages, or avatar choices.
- Custom avatar, Personal Avatar, Studio Avatar, stock avatar, and voice/likeness consent decisions.
- QA for lip sync, script pacing, pronunciation, avatar framing, identity disclosure, localization, download custody, and policy fit.

Do not use Synthesia as the primary tool when the user needs:

- multi-shot cinematic generative video, camera moves, physics, or photoreal B-roll generated from prompts;
- face-swap or lip-sync onto arbitrary footage outside Synthesia's supported avatar system;
- an avatar of a real person without documented consent;
- political/current-events persuasion, deceptive impersonation, sensitive identity claims, or paid social ads with stock avatars unless policy and written consent requirements are satisfied.

## Source-backed operating facts

Label facts separately from heuristics in your production notes.

Documented facts verified 2026-07-10:

- API access is documented as available for Creator plans or above. Test requests from docs are limited to 30 test videos per day. API keys belong to the user account that creates them, not the workspace.
- The create-video endpoint is `POST https://api.synthesia.io/v2/videos`; authentication uses an `Authorization` header.
- A create-video request requires `input`, an array of scene-like clips. Each input requires `avatar` and `background`.
- Supported aspect ratios on the create-video endpoint are `16:9`, `9:16`, `1:1`, `4:5`, and `5:4`.
- `test: true` creates a free, quota-exempt watermarked test video.
- Video visibility can be `private` or `public`. Private videos are downloaded through time-limited download links; public videos have a share page.
- API video status values include `complete`, `deleted`, `error`, `in_progress`, `rejected`, and `approved`. Retrieve status with `GET /v2/videos/{video_id}`.
- A quickstart-created video is documented as taking about 3 to 5 minutes to process, but production timing can vary.
- Direct API `scriptText` can use XML-like `<break time="1s"/>` pauses and `<sub alias="spoken text">caption text</sub>` pronunciation substitutions.
- If using `scriptAudio` instead of `scriptText`, provide `scriptLanguage`; Synthesia docs say uploaded scene audio is an Enterprise feature in Studio and cannot have its volume or playback speed changed there.
- The script box supports up to 5 minutes of script per scene. Studio voice speed controls are approximate, paragraph-level, and range from 0.8x to 1.2x.
- Studio supports multiple languages in a scene or video by applying different voices to script sections. The official translation language table contains many language/dialect codes; Synthesia marketing pages also describe 140+/160+ language coverage in different contexts, so verify the exact feature being used.
- The API provides stock avatar IDs and voice IDs in official reference pages. Custom avatar IDs are copied from the avatar page in the app.
- `avatarSettings.style` can be `rectangular`, `circular`, or `voiceOnly`; specifying `avatarSettings.voice` avoids default-voice drift.
- `green_screen` is a documented transparent-style background option for downstream replacement; other documented API backgrounds include solid colors and named image backgrounds.
- `seamless` avatar generation is documented with restrictions: only specific actors, static image backgrounds, and lower quality.
- The template endpoint is `POST /v2/videos/fromTemplate`; it requires `templateId` and `templateData` and can accept `brandKitId`.
- Script variables cannot begin with a number; variables are intended for template/API personalization.
- Personal Avatars require the subject to be at least 18. Personal Avatar from photo requires a live consent recording that cannot be uploaded and must show the same person as the photo.
- Personal Avatars from video require footage plus a consent recording and are documented as ready in 24 hours; they pair with a cloned voice and can communicate in 30+ languages. Re-verify availability and turnaround before scheduling.
- Synthesia's current avatar documentation describes Studio Avatars as using EXPRESS-1, while stock/avatar libraries may show multiple avatar versions and capabilities; verify the specific avatar's documented version before promising expressive behavior. The pricing page, verified 2026-07-10, listed Studio Express-1 avatar creation as a paid annual add-on that can take up to 10 days.
- Avatar and voice sharing are Enterprise-only in the official avatar docs, and sharing an avatar does not automatically share its voice.
- Deleting an avatar does not remove it from already-generated videos; regeneration later requires replacing the deleted avatar.
- Synthesia's Acceptable Use Policy prohibits or restricts impersonation, deception, rights violations, adult/minor exploitation, misinformation/disinformation campaigns, watermark removal, spam, and several stock-avatar uses in paid social, political/current-events, sensitive, or false-endorsement contexts.

Production heuristics:

- Prefer Synthesia when the viewer should feel guided by a presenter. Prefer a non-avatar motion-graphics or screen-demo pipeline when the avatar is only decorative.
- Keep one scene's spoken script under roughly 60-90 seconds when possible even though the documented maximum is 5 minutes; shorter scenes are easier to preview, localize, regenerate, and QA.
- Avoid full-frame avatar for dense explanations. Put the presenter in a circle/box or make them voice-only while the screen, diagram, or product footage carries the learning load.
- Choose templates for repeatability and compliance; choose from-scratch API requests for simple single-use presenter clips.
- Always specify voice IDs for production API runs so a default voice change does not alter future variants.
- Treat avatar likeness, voice, target demographic, and sensitive claims as rights/safety decisions, not styling choices.

## Production workflow

### 1. Confirm the delivery contract

Before writing a script or making API calls, capture:

- audience, language/dialect, reading level, and accessibility needs;
- platform and aspect ratio;
- intended use: internal training, customer onboarding, public marketing, paid ad, LMS/SCORM, website embed, sales personalization, or support;
- avatar type: stock, custom built from stock, Personal Avatar, Studio Avatar, or voice-only;
- whether any real person, employee, celebrity, public figure, patient, customer, or demographic identity is represented;
- brand kit/template ID, folder ID, assets, CTA URL, legal disclaimers, and retention requirements;
- whether the work is a test/watermarked preview or a quota-consuming final render.

Block or escalate before generation if consent, rights, policy, or data handling is unresolved.

### 2. Choose the Synthesia path

Use Studio manual editing when:

- the user needs layout control, scene preview, captions, animations, brand kit review, interactive elements, or translation review;
- you need to audition avatars/voices visually;
- an editor or legal reviewer must approve before generation.

Use API from scratch when:

- a simple scene or multi-scene presenter video can be expressed with `input[]`, `scriptText` or `scriptAudio`, avatar IDs, backgrounds, and basic settings;
- the job is programmatic but not template-heavy.

Use API from template when:

- brand, legal layout, scene structure, avatar placement, captions, animation triggers, or approval requirements are prebuilt in Studio;
- many variants differ only by variable values;
- avatar, text, media, language, or CTA variables must be controlled at scale.

Use translation/dubbing features when:

- the source video already exists in Synthesia and needs localized versions;
- locale-specific QA and glossary control matter.

### 3. Plan scenes like a presenter plus evidence

For each scene, define:

- presenter role: host, guide, instructor, sales rep, support agent, executive, narrator, or voice-only;
- viewer job: understand, remember, trust, take action, complete a task, or pass a compliance check;
- spoken script, target duration, on-screen visual, background/space, captions, CTA, and transition;
- avatar frame: fullscreen for human connection, rectangular side-presenter for teaching, circular for app demos or product UI, voice-only for dense visuals;
- B-roll/media: product screenshots, diagrams, screen recordings, forms, charts, icons, or safety callouts;
- QA check: pronunciation, lip sync, gaze, visual alignment, captions, policy disclosure, and localization notes.

Strong Synthesia videos do not ask the avatar to carry every second. Alternate presenter shots with visual proof: screen states, diagrams, checklists, before/after views, product footage, or quiz/CTA moments.

### 4. Write for synthetic delivery

Write in short paragraphs with one spoken idea per paragraph. Front-load context, avoid tongue-twisters, and place brand/product terms in a pronunciation plan.

Use:

- natural contractions and simple sentence structure;
- explicit pause cues for transitions, reveals, or emotional beats;
- pronunciation substitutions for acronyms, product names, names, and technical terms;
- separate paragraphs when the speed or voice should change;
- localized scripts written idiomatically, not word-for-word translations.

Avoid:

- overlong sentences;
- rapid lists without visual reinforcement;
- unexplained acronyms;
- claims that imply the avatar actor personally endorses, experienced, suffers from, or belongs to a sensitive identity unless consent and policy requirements are satisfied;
- jokes, sarcasm, or emotional nuance that depends on live acting.

For API script control, use supported tags:

```text
Welcome to <sub alias="Acme Insight">ACME Insight</sub>. <break time="0.7s"/>
In the next two minutes, you'll learn the three checks that prevent most onboarding delays.
```

### 5. Select avatars, voices, and languages deliberately

Selection checklist:

- Does this avatar match the role without falsely implying identity, endorsement, credentials, culture, medical status, employee status, or lived experience?
- Is stock avatar use allowed for this distribution channel and topic? Check paid social, politics/current events, sensitive attributes, and false association restrictions.
- Does the user have the right to use the selected custom/avatar voice in this workspace and for this use?
- Is the voice ID specified for API output?
- Is the dialect/localization correct for the audience?
- Does the avatar need to be visible at all, or would voice-only with better visuals serve the viewer?

Custom/person-specific avatar rule: do not proceed without documented consent from the person whose likeness or voice is used. For Personal Avatars, use Synthesia's consent flow; do not accept uploaded "consent" footage where Synthesia requires live recording.

### 6. Build API requests defensively

From-scratch API request shape:

```json
{
  "test": true,
  "visibility": "private",
  "title": "Example - Onboarding overview - TEST",
  "description": "Watermarked Synthesia API test render for internal review.",
  "callbackId": "crm-onboarding-2026-07-10-row-001",
  "aspectRatio": "16:9",
  "input": [
    {
      "avatar": "anna_costume1_cameraA",
      "avatarSettings": {
        "style": "rectangular",
        "horizontalAlign": "right",
        "scale": 0.92,
        "voice": "VOICE_UUID_FROM_OFFICIAL_VOICE_LIST"
      },
      "background": "off_white",
      "scriptText": "Welcome to <sub alias=\"Acme Insight\">ACME Insight</sub>. <break time=\"0.6s\"/> Today we'll set up your first workspace.",
      "soundSettings": {
        "soundtrackVolume": 0.12
      }
    }
  ]
}
```

Production notes:

- Start with `test: true` for layout, script, voice, and policy checks. Switch to `test: false` only after approval.
- Keep `visibility: private` unless the delivery explicitly requires a public share page.
- Use `callbackId` to map jobs back to a CRM row, LMS module, ticket, or render manifest. Avoid sensitive personal data if it is not needed.
- Use official avatar/voice IDs from the API docs or app. Do not assume marketing names are valid IDs.
- Store request JSON, response JSON, video ID, status history, source script, template ID/version, variable data, consent evidence pointer, and final MP4 path in the project manifest.

Template API request shape:

```json
{
  "test": true,
  "visibility": "private",
  "title": "Example - Renewal reminder - {{account_name}} - TEST",
  "templateId": "TEMPLATE_UUID_FROM_STUDIO",
  "brandKitId": "workspace_default",
  "callbackId": "renewal-campaign-2026-07-10-row-0042",
  "templateData": {
    "first_name": "Maya",
    "account_name": "Northwind Analytics",
    "renewal_date": "September 15",
    "cta_url": "https://example.com/renewal"
  }
}
```

Template notes:

- Publish and test the template in Studio before batch calls.
- Retrieve/list template details to confirm variable names and required values.
- Keep variable names alphabetic at the start.
- Validate every row for missing values, forbidden claims, unsupported languages, and broken URLs before generation.
- Use one approved template for many variants; do not let each row change the script structure unless reviewers approved that range.

### 7. Manage job lifecycle and custody

Lifecycle:

1. Create the video or template video.
2. Record the returned `id`.
3. Poll `GET /v2/videos/{video_id}` or use webhooks when the environment supports them.
4. Treat `complete` as ready for download, `in_progress`/`approved` as not yet final, and `error`/`rejected` as requiring triage.
5. Download promptly because private download links are time-limited.
6. Store the final MP4 and metadata in the project's artifact system, not only in a transient URL.
7. If publishing publicly, record the visibility change and share URL separately from the master MP4.

Custody manifest fields:

```json
{
  "provider": "synthesia",
  "verified_date": "2026-07-10",
  "mode": "api_from_template",
  "test": false,
  "video_id": "UUID",
  "template_id": "UUID",
  "brand_kit_id": "workspace_default",
  "avatar_ids": ["UUID_OR_STOCK_ID"],
  "voice_ids": ["UUID"],
  "languages": ["en-US"],
  "visibility": "private",
  "status_history": [
    {"status": "in_progress", "timestamp": "2026-07-10T18:00:00Z"},
    {"status": "complete", "timestamp": "2026-07-10T18:05:00Z"}
  ],
  "downloaded_to": "projects/acme-onboarding/assets/video/synthesia-final.mp4",
  "consent_evidence": "internal-rights-record-id-or-not-applicable",
  "policy_review": "passed with stock-avatar business-training use"
}
```

## Safety, consent, rights, and disclosures

Run this gate before every final render:

- Likeness/voice: Does every custom, personal, or studio avatar/voice have explicit consent and appropriate workspace sharing rights?
- Stock avatar identity: Could viewers think the real actor personally endorses the product, has a condition, is an employee, belongs to a represented group, or holds stated opinions?
- Distribution: Is the video public, paid social, TV/news, political/current-events, fundraising, or sensitive? If yes, re-check Synthesia's policy and obtain needed written consent.
- Content category: Does the script touch minors, adult content, regulated goods, medical/financial/legal advice, identity theft, fraud, misinformation, extremist content, harassment, or discrimination?
- Provenance: Are AI/avatar disclosures, watermarks, or required labels preserved? Do not remove provenance mechanisms.
- Data minimization: Are customer names, health data, student data, or account details necessary? Avoid putting sensitive data in `callbackId`, titles, public descriptions, or visible captions unless required and approved.
- Rights: Are background assets, images, music, logos, fonts, screenshots, and brand marks licensed for the intended distribution?
- Accessibility: Are captions, contrast, safe margins, and language choices appropriate?

If any answer is uncertain, stop and request consent/legal/product direction before generation.

## QA the finished video

Review the rendered MP4, not just the editor preview.

Minimum QA:

- script: exact approved message, correct variables, no stale placeholders, correct CTA;
- voice: correct voice ID, dialect, pronunciation, pacing, volume, and pauses;
- avatar: correct person/avatar, stable lip sync, acceptable gaze and expression, no false endorsement or sensitive identity implication;
- layout: avatar framing, safe margins, captions, logo placement, background, transitions, and mobile crop;
- localization: language code, idiom, names, numerals, dates, units, glossary, captions, and any translated onscreen text;
- accessibility: readable captions, no text hidden by avatar, adequate contrast, no audio-only critical information without captions;
- compliance: consent evidence, policy review, disclosure/provenance, rights record;
- technical: MP4 opens, duration matches expectation, audio not clipped, no watermark on final unless deliberately a test, final path stored, transient download link not the only copy.

Common failures and repairs:

- Wrong/default voice: specify `avatarSettings.voice`; regenerate only affected scenes if possible.
- Flat or unnatural delivery: split paragraphs, add `<break>`, regenerate speech in Studio, reduce dense phrasing, or choose a different voice.
- Mispronunciation: use `<sub>` in API or pronunciation/glossary controls in Studio.
- Avatar distracts from learning: switch to circular/rectangular side-presenter or voice-only; move dense information to visuals.
- Rejected generation: review policy-sensitive language, avatar choice, false association, restricted topic, asset rights, and account permissions.
- Missing variables in batch: retrieve template variables, validate row schema, use defaults only when the resulting statement remains true.
- Private link expired: re-retrieve the video or publish/update visibility if approved; always download and store the MP4.
- Localization sounds literal: rewrite the localized script by audience and dialect; do not rely only on machine translation for final public work.

## Complete examples

### Example 1: Internal compliance microlearning

Intent: produce a 90-second internal training clip explaining how employees should handle suspicious invoice emails.

Recommended path: Studio template or API from template. Use stock avatar only if the script clearly frames them as a training presenter, not a real employee or victim. Keep distribution internal. Use `16:9` for LMS unless mobile-first.

Scene plan:

1. Presenter hook: "Three checks before you approve an invoice."
2. Screen visual: sample invoice with highlighted sender, amount, and payment instructions.
3. Checklist: verify vendor, verify change request, escalate via finance channel.
4. Quiz/CTA: "Would you approve this?" with LMS or interactive follow-up.

Script excerpt:

```text
Before approving an invoice, pause for three checks. <break time="0.5s"/>
First, compare the sender domain to the vendor record.
Second, treat any bank-detail change as high risk.
Third, use the finance escalation channel before replying.
```

Why this structure works: the avatar establishes attention and authority, but the visual invoice carries the actual learning. The script avoids implying the stock avatar is a real finance employee.

QA focus: pronunciation of vendor/product names, captions for every instruction, no real customer data in screenshots, and clear internal-training disclosure.

### Example 2: Personalized customer onboarding via API template

Intent: create hundreds of welcome videos for new B2B customers with first name, company, plan, success-manager name, and CTA URL.

Recommended path: build one approved Studio template with variables; call `POST /v2/videos/fromTemplate` per row.

Template variables:

```json
{
  "first_name": "alphabetic start, display name",
  "company_name": "customer company",
  "plan_name": "approved product plan string",
  "success_manager": "assigned contact",
  "cta_url": "absolute HTTPS URL"
}
```

Preflight validation:

- no empty variable values;
- no sensitive data beyond agreed personalization;
- `cta_url` allowlisted;
- names reviewed for pronunciation when high-value accounts matter;
- template tested with shortest, longest, and non-ASCII names.

Expected result: consistent brand and scene structure, variable-personalized opening, no per-row layout drift, private outputs downloaded into a campaign folder.

Failure modes: variable overflow in onscreen text, mispronounced names, stale plan names, expired download links, or accidentally public share pages.

### Example 3: Product support article video

Intent: turn a "reset SSO mapping" help article into a 2-minute support video.

Recommended path: Synthesia Studio with avatar voice-only or circular side-presenter plus screen recordings. Use a calm support voice; avoid full-frame avatar during step-by-step UI.

Production outline:

- Scene 1: presenter states who the video is for and what will change.
- Scene 2: screen recording shows settings path; avatar hidden or circular.
- Scene 3: callout warns that changing mappings can affect login.
- Scene 4: recap and CTA to contact support if SAML/SSO errors continue.

Script excerpt:

```text
This walkthrough is for workspace admins who already have SSO enabled.
If you're not sure, stop here and check with your identity provider owner. <break time="0.8s"/>
From Workspace Settings, open Single Sign-On, then choose Attribute Mapping.
```

QA focus: UI version accuracy, no secret keys in screen footage, captions readable over UI, and voice pace slow enough for admins to follow.

### Example 4: Multilingual sales enablement variant

Intent: localize a product explainer for English, French, German, and Japanese sales teams.

Recommended path: create master Studio video, use translation/localization workflow, then human review each locale. Use locale-specific voices and date/number formats.

Localization guidance:

- rewrite idioms and jokes rather than translating literally;
- maintain brand terms through glossary/pronunciation controls;
- review Japanese politeness level and German compound product terms;
- regenerate audio where timing or intonation feels unnatural;
- verify on-screen text and captions are localized, not just narration.

Failure modes: text overflow, inconsistent CTA, overly literal slogans, wrong dialect code, missing captions, or voice mismatch with the sales audience.

## Official sources used

Re-check these before production if the decision depends on current facts:

- Synthesia API introduction: `https://docs.synthesia.io/reference/introduction`
- API quickstart: `https://docs.synthesia.io/reference/synthesia-api-quickstart`
- Create video endpoint: `https://docs.synthesia.io/reference/create-video`
- Create video from template endpoint: `https://docs.synthesia.io/reference/create-a-video-from-a-template`
- Retrieve video endpoint: `https://docs.synthesia.io/reference/retrieve-a-video`
- Stock avatar IDs: `https://docs.synthesia.io/reference/avatars`
- Voice IDs: `https://docs.synthesia.io/reference/voices`
- Script supported XML tags: `https://docs.synthesia.io/reference/script-supported-xml-tags`
- Script box: `https://docs.synthesia.io/docs/script`
- Avatar docs: `https://docs.synthesia.io/docs/avatar` and `https://docs.synthesia.io/docs/synthesia-avatars`
- Personal Avatar docs: `https://docs.synthesia.io/docs/personal-avatars`
- Supported translation languages: `https://docs.synthesia.io/docs/supported-languages`
- Pricing: `https://www.synthesia.io/pricing`
- Acceptable Use Policy: `https://www.synthesia.io/legal/acceptable-use-policy`
- AI Governance Practices: `https://www.synthesia.io/legal/ai-governance-practices`
- Responsible AI: `https://www.synthesia.io/responsible-ai`
- Platform Integrity help page: `https://help.synthesia.io/en/articles/8330564-platform-integrity`
