---
name: saas-product-demo-production
description: Provider-independent workflow for producing SaaS and software product demo videos, including app walkthroughs, feature launches, sales demos, onboarding clips, help-center explainers, website hero demos, and PLG assets. Use when an agent must plan, script, capture, synthesize, edit, localize, review, or QA privacy-safe software demo videos with substantiated claims, accessible captions, screen/cursor direction, CTA variants, and stakeholder approval.
---

# SaaS product demo production

Use this skill to turn a software product brief into a production-ready demo video plan, script, capture direction, generated-media prompt set, edit plan, delivery matrix, and QA pass. It is provider-independent: adapt it to real screen recording, browser automation, synthetic screens, motion graphics, avatar narration, or AI video generation without assuming a specific tool.

The core job is not "show the UI." The job is to make the right viewer understand a valuable workflow, trust the evidence, and know what to do next without exposing private data or overstating the product.

## Non-negotiables

Treat these as production constraints, not suggestions:

1. Start from audience, use case, and proof. A demo organized by the product navigation usually feels like a tour; a demo organized by the buyer's job feels like a solution.
2. Use only approved demo tenants, seeded mock data, synthetic data, or explicitly cleared customer data. Never capture live production accounts, real customer names, internal tickets, API keys, session tokens, email addresses, payment details, unreleased roadmap, admin consoles, or analytics that security/legal/client stakeholders have not approved.
3. Substantiate every objective claim before writing it into narration, captions, on-screen text, thumbnails, or ad copy. The FTC states that advertising claims should be truthful, non-deceptive, and evidence-based, and its substantiation policy expects a reasonable basis for express and implied objective claims before dissemination. Do not treat this skill as legal advice; escalate regulated, comparative, performance, financial, health, security, privacy, AI, or pricing claims to the appropriate reviewer.
4. Put required disclosures close to the claim they qualify. FTC .com Disclosures guidance emphasizes clear and conspicuous disclosure placement, proximity, prominence, duration, cadence, understandable language, and the overall net impression of the ad. If a platform or short cutdown cannot carry the disclosure clearly, change the claim or do not use that placement.
5. Caption prerecorded audio. WCAG SC 1.2.2 calls for captions on prerecorded synchronized media with audio. Caption dialogue, speaker changes, meaningful sound effects, and important non-speech audio. Prefer sidecar captions for platforms that support them; burn in captions only when the distribution context needs always-on readability.
6. Make important visual information available beyond the pixels. If the demo depends on on-screen changes, describe them in narration, provide a text alternative, or add audio description for accessibility-sensitive deliveries. WCAG SC 1.2.5 requires audio description for prerecorded video at Level AA unless the main audio already conveys the important visual information.
7. Keep text, callouts, subtitles, UI, and disclosure overlays legible. Use WCAG contrast discipline for all production graphics: aim for at least 4.5:1 for normal text, 3:1 for large text and non-text UI indicators, and never rely on color alone to convey meaning.
8. Re-check delivery specs at production time. Platform ad specs, safe zones, duration limits, caption support, and file limits change. Treat any platform-specific numbers in this skill as volatile examples verified on 2026-07-10, not permanent truth.

## Decide the demo type before scripting

Choose one primary type. Secondary cutdowns can remix it, but the master needs one organizing promise.

| Demo type | Best for | Structure | Risk to avoid |
|---|---|---|---|
| Feature launch | Existing users, prospects, analysts | "Old painful way  new capability  proof  how to try it" | Listing features without a before/after |
| Sales demo | Buyers/evaluators | "Persona pain  workflow  differentiated proof  buying next step" | Too much UI detail before value is clear |
| Product-led growth / website hero | Top-of-funnel visitors | "One job, one win, one CTA" | Tiny UI, vague claims, no next action |
| Onboarding | New users | "Complete this task now  confidence for the next task" | Explaining every option instead of the first success path |
| Help-center explainer | Support deflection | "Symptom/problem  exact steps  verification  troubleshooting branch" | Marketing language where users need instructions |
| Internal enablement | Sales/support/customer success | "Talk track  proof points  objection handling  demo path" | Unapproved claims being taught to the field |

If the user's request says "make a demo" with no audience, ask for the persona and usage context unless you can infer them from the asset destination. A 15-second website hero, a 90-second launch post, a 4-minute help-center walkthrough, and a 12-minute sales demo need different pacing and evidence.

## Intake: the minimum brief

Collect or infer:

- Product and feature: exact name, status, release date, approved positioning, and whether UI is final.
- Audience: role, sophistication, buyer/user distinction, industry, region, language.
- Use case: the job-to-be-done, trigger event, current workaround, failure cost, desired outcome.
- Funnel stage: awareness, consideration, trial activation, onboarding, retention, support, expansion.
- Distribution: website hero, product page, sales deck, help center, email, paid social, organic social, app store, in-app modal, conference booth, or internal enablement.
- Required proof: approved metrics, customer quote, benchmark, certification, integration list, product behavior, or no claim beyond observable UI.
- Compliance level: whether legal, security, privacy, brand, accessibility, or customer approval is required.
- Capture method: real app capture, staged browser capture, synthetic UI recreation, animated mockup, generated app-like sequence, or hybrid.
- Demo environment: tenant URL, permissions, mock data source, reset procedure, and "do not show" list.
- Deliverables: master length/aspect, cutdowns, captions, thumbnail, transcript, social copy, localized variants, source project files.

When the brief is incomplete, make a conservative plan and label assumptions. Do not invent product capabilities, metrics, customer proof, certifications, integrations, or release dates.

## Persona and use-case framing

Write the demo around a specific viewer thought:

> "I have this problem, I recognize this screen, I see how the product gets me to a better state, and I trust the evidence."

Use this framing template:

- Persona: "RevOps manager at a 300-person SaaS company."
- Trigger: "Quarter-end forecast review is tomorrow."
- Pain: "Pipeline changes live across CRM notes, spreadsheets, and Slack."
- Desired outcome: "Know what changed, why, and which deals need action."
- Objection: "Will this break our workflow or expose sensitive data?"
- Proof needed: "Live sync shown in UI, supported integrations, permission model disclosure, approved time-saving metric if available."
- CTA: "Start a trial," "book a workflow audit," "read setup guide," or "enable the feature."

Do not start with company history, product category definitions, or a full dashboard overview unless the audience genuinely needs orientation.

## Storyline patterns

Use one of these patterns, then customize.

### Problem  workflow  outcome

Best for sales demos, launch videos, hero demos, and PLG pages.

1. Hook: name the painful job in the viewer's words.
2. Before state: show the old friction quickly.
3. Turn: introduce the product capability.
4. Guided workflow: 3-5 steps, each with visible progress.
5. Outcome: show the completed artifact, decision, saved step, or reduced risk.
6. Proof and limitation: support with approved evidence; qualify where needed.
7. CTA: one next action.

### Task  steps  verification

Best for onboarding and help-center clips.

1. State the user's goal.
2. Show prerequisites.
3. Perform the steps without flourish.
4. Show a success state.
5. Add a troubleshooting branch or "if you don't see this" note.
6. CTA: next task, docs link, or support path.

### Objection  proof  next step

Best for enterprise sales, security-sensitive products, and admin features.

1. Name the objection respectfully.
2. Show the control, audit trail, permission, or evidence.
3. Clarify scope and limits.
4. Give the buyer a review artifact or next meeting action.

## Feature prioritization

A short demo can usually carry one primary workflow and two supporting moments. Prioritize with this order:

1. The moment that proves the promise.
2. The screen state viewers will recognize from their own work.
3. The shortest path to the outcome.
4. Differentiators that are visible, not merely claimable.
5. Features that answer the top objection.

Cut:

- Settings screens unless setup is the point.
- Navigation detours.
- Empty-state explanations after the value has been shown.
- Secondary features that require separate context.
- Claims that need a long disclosure to be safe in a short asset.

For complex products, produce a "spine demo" master plus modular inserts: integration insert, security insert, admin insert, mobile insert, pricing/packaging insert, and industry-specific insert.

## Data and privacy-safe demo environments

Documented fact: NIST SP 800-122 says PII should be protected from inappropriate access, use, and disclosure. NIST SP 800-188 defines de-identification as removing association between identifying data and the data subject and warns that masking alone may not be sufficient for de-identification.

Production rule: avoid real personal or customer data in demos unless all approvals are explicit and documented.

Use this hierarchy:

1. Purpose-built demo tenant with fictitious accounts, organizations, dates, messages, payments, documents, and analytics.
2. Synthetic dataset generated to resemble plausible workflows without mapping to real people or customers.
3. Anonymized or de-identified data only after privacy/security approval and re-identification risk review.
4. Real customer data only with written customer permission, security/privacy/legal approval, and a capture checklist.

Scrub before capture:

- Names, faces, avatars, email addresses, phone numbers, home addresses.
- Customer logos, domains, file names, Slack channels, Jira tickets, support cases.
- API keys, tokens, secrets, OAuth consent screens, browser extensions, bookmarks.
- Internal hostnames, staging URLs, feature flags, admin IDs, debug overlays.
- Revenue, health, HR, legal, security, or financial records.
- Notification drawers, autofill suggestions, system clock if timing is sensitive.
- Browser history, OS menu bar, desktop wallpaper, local file paths.

Build demo data with narrative purpose: every visible row should support the storyline. Avoid lorem ipsum when a meaningful fictitious customer, task, or workflow label would help comprehension. Use obviously fictional entities where realism could create confusion, such as "Northstar Robotics Demo Co." or "Sample Customer."

Security and counsel escalation triggers:

- A real customer, logo, quote, benchmark, security certification, regulated workflow, or AI claim appears.
- The demo shows admin controls, permissions, audit logs, data export, deletion, privacy settings, encryption, auth, or compliance workflows.
- The claim touches legal compliance, money saved, revenue generated, risk reduction, medical/financial outcomes, employment decisions, public-sector use, children, or regulated industries.
- The recording requires production access or elevated privileges.

## Capture and synthetic-screen planning

Choose the lowest-risk capture method that still proves the product.

| Method | Use when | Strength | Watch-outs |
|---|---|---|---|
| Real screen recording | UI is final and behavior must be authentic | Highest product truth | Requires demo tenant, stable network, privacy scrub, retakes |
| Browser automation capture | Flow is deterministic and web-based | Repeatable, clean cursor, reusable variants | Needs selectors, app state reset, responsive viewport checks |
| Synthetic UI recreation | Real data is risky or UI is unfinished | Privacy-safe, art-directable, crisp for hero videos | Must not imply unavailable features; mark as simulated if needed |
| Motion graphic abstraction | The workflow is conceptual or cross-device | Communicates benefit without tiny UI | Can become vague if no real product proof appears |
| AI-generated app-like footage | Need mood or conceptual B-roll, not exact product truth | Fast atmospherics | Avoid hallucinated UI; do not pass it off as exact product behavior |

Before recording, create a capture sheet:

- Flow name and objective.
- Viewport: desktop 16:9, desktop 4:5 crop-safe, mobile 9:16, tablet, or responsive set.
- Browser/app state: logged-in role, seed data, flags enabled, zoom level, cookies reset.
- Step list with expected screen state after each click.
- Cursor path: where to pause, where to click, where not to hover.
- Callouts: text, timing, target UI element, and whether callout is spoken, graphic, or both.
- Safe zones: where captions, CTA, product nav, and platform UI overlays will sit.
- Privacy hazards and scrub actions.
- Retake triggers: spinner, notification, typo, wrong date, real data, cursor wobble, accidental hover, frame drop, network lag.

Use high-resolution capture and crop down for variants. For desktop UI, 1440p or 4K capture gives room for zooms; for final 1080p outputs, keep zoomed text crisp. For mobile-first demos, capture or compose directly at 9:16 rather than cropping a desktop screen after the fact.

## Cursor, zoom, and callout direction

Cursor and zoom are part of the script.

- Move slowly enough that viewers can predict the action. Avoid jittery mouse wandering.
- Pause before each click so the viewer sees the target.
- Use zoom for intent, not decoration: zoom into the field or result that proves the step, then return to context.
- Prefer one callout per beat. If you need three arrows at once, the scene is probably doing too much.
- Make callouts actionable: "Auto-filled from Salesforce" is better than "Integration."
- Put callouts near the UI element, but keep them out of captions, platform buttons, and disclosure zones.
- Maintain a consistent visual grammar: one style for feature labels, another for warnings/disclosures, another for CTA.
- For mobile variants, design callouts for thumbs and platform overlays. Do not place critical text at the top/bottom areas that common social UI may cover; TikTok notes safe-zone dimensions depend on format, caption length, and add-ons, so check current safe-zone templates before final export.

Use a three-layer clarity test:

1. Silent test: with audio off, can a viewer understand the flow from UI, captions, and callouts?
2. Tiny-screen test: at phone size, can they read the key UI state and CTA?
3. Audio-only test: without visuals, does narration convey the important outcome?

## Narration and script

Write narration as a guide beside the UI, not a transcript of every click.

Good demo narration:

- Names the viewer's job.
- Explains why a step matters.
- Lets obvious clicks stay silent.
- Uses concrete nouns from the UI.
- Leaves breathing room around visual proof.
- States limitations plainly when needed.
- Ends with a CTA that matches funnel stage.

Avoid:

- "As you can see here" without saying what matters.
- Repeating every button label.
- Superlatives without proof.
- Overexplaining setup in a short marketing demo.
- Mixing buyer benefit and user instructions in the same sentence.

Script beat format:

```text
00:00-00:04 Hook
Visual: Split before-state of spreadsheet + inbox + CRM card.
Narration: "Forecast changes should not take three tools to explain."
On-screen text: "Know what changed before forecast review."
Claim/proof: No quantified claim.

00:04-00:13 Product turn
Visual: Open Acme Pipeline Monitor demo tenant. Filter to "changed this week."
Cursor: Pause over filter, click once, no hover wandering.
Narration: "In Pipeline Monitor, RevOps sees every deal that changed this week in one review queue."
Callout: "One queue for changes"
Claim/proof: Observable UI only.
```

For text-to-speech, write punctuation for performance: short sentences, explicit pauses, and pronunciation notes for product names. For human voiceover, include emphasis and speed direction. For avatar demos, avoid long uninterrupted blocks; cut back to screen often.

## Proof and claims discipline

Categorize every claim:

| Claim type | Examples | Required handling |
|---|---|---|
| Observable product behavior | "Filter by owner," "Export CSV," "Invite teammates" | Show the UI doing it; QA against current product |
| Descriptive positioning | "A workspace for launch planning" | Confirm with approved messaging |
| Quantified performance | "Save 6 hours/week," "2x faster," "99.99% uptime" | Require substantiation source, date, scope, and approval |
| Comparative | "Better than spreadsheets," "faster than Vendor X" | Escalate; needs evidence and careful wording |
| Security/privacy/compliance | "SOC 2 ready," "HIPAA compliant," "private by default" | Escalate to security/legal; use approved exact language |
| AI capability | "Detects risk," "summarizes accurately," "automates decisions" | Verify product behavior; disclose human review/limitations if relevant |
| Testimonial/customer result | "Customer saved $1M" | Require permission, typicality/disclosure review, source approval |

Build a claims ledger:

```text
Claim: "Cuts weekly forecast prep from hours to minutes."
Where used: 60s launch video narration 00:42, end card, LinkedIn copy.
Type: Quantified/implied performance.
Evidence: Approved customer study? Internal benchmark? None yet.
Status: Not approved. Rewrite to "shortens the handoff from scattered updates to one review queue" unless evidence is supplied.
Reviewer: Marketing/legal.
```

If a claim needs a disclosure, put the disclosure in the video plan at the same beat as the claim. Do not leave it for a social caption or landing page unless the ad can still avoid a misleading net impression by itself.

## Translating demo plans into generated-media prompts

Generated media can support product demos, but should not hallucinate product truth. Separate "exact UI capture" from "conceptual support media."

Prompt structure for synthetic or generated scenes:

```text
Intent: Explain the benefit of [feature] for [persona] without pretending to show real product UI.
Scene: [screen/device/environment], [composition], [motion].
UI fidelity rule: Use abstracted panels and generic labels; do not invent real buttons, customer data, metrics, logos, or certifications.
Narrative beat: [problem / workflow / outcome].
Privacy rule: Use fictitious names and domains; no real brands unless approved.
Text overlays: [exact approved overlay text].
Camera/motion: [zoom, pan, cursor, callout, transition].
Accessibility: Leave lower caption band clear; high contrast; no color-only meaning.
Negative constraints: no real customer logos, no API keys, no unreadable microtext, no fake dashboards implying unsupported analytics.
```

For exact product walkthroughs, prompt the tool to use supplied screenshots or captured footage as references and to preserve UI truth. If the model cannot reliably preserve UI text, use it only for background motion, not for product proof.

Label simulations when ambiguity matters:

- "Simulated data shown"
- "Concept visualization"
- "Example workflow"
- "Screens shortened for clarity"

## Edit pacing

Pacing should fit the viewer's context:

- Website hero: 10-30 seconds, one workflow impression, mostly silent-readable, CTA visible early and late.
- Paid/organic social: 15-45 seconds, hook in first 1-3 seconds, product proof by 5-8 seconds, strong captions and safe zones.
- Feature launch: 45-90 seconds, before/after, 3-5 workflow beats, proof and CTA.
- Onboarding: 30-180 seconds per task, slower cursor, exact steps, success verification.
- Help center: as long as necessary but segmented; avoid marketing polish that slows task completion.
- Sales leave-behind: 2-5 minutes, persona-specific value, objection proof, chaptered sections.

Editing heuristics:

- Start with the outcome or pain, not the login page.
- Remove waiting states unless the speed itself is the proof; use a subtle jump cut and label "processing" if needed.
- Use zoom cuts to keep UI readable, but avoid disorienting camera motion.
- Let complex screens breathe for at least one beat after a callout appears.
- Use chapter cards only when they help comprehension.
- Put the CTA in voice, on-screen text, and end card when appropriate.
- Keep a "no-audio comprehension" path through captions and text.

## Mobile, desktop, and cutdown matrix

Plan aspect ratios before recording. A master timeline that cannot be cropped safely is expensive to repair.

Common SaaS demo deliverables:

| Variant | Use | Notes |
|---|---|---|
| 16:9 horizontal | YouTube, website, sales deck, help center, webinar follow-up | Best for dense desktop UI and longer walkthroughs |
| 4:5 vertical feed | LinkedIn/feed placements | Good balance of UI readability and mobile feed height |
| 1:1 square | Feed compatibility and thumbnails | Works for simplified UI, less ideal for full dashboards |
| 9:16 vertical | Shorts/Reels/TikTok/mobile app demos | Requires redesigned callouts and often mobile-specific UI |
| GIF/loop | Product page micro-demo, email | Use no-audio text and very short loops; watch file size |
| Still frames | Sales deck and docs | Capture key proof states from the video |

Verified examples as of 2026-07-10:

- LinkedIn video ad specs list 16:9 landscape, 1:1 square, 4:5 vertical, and 9:16 vertical options with stated min/max dimensions and 5% aspect-ratio tolerance.
- Google Ads API Performance Max asset requirements list YouTube video aspect ratios of 16:9, 1:1, or 9:16 and duration of at least 10 seconds.
- TikTok's in-feed ad guidance says safe-zone size varies by dimension, caption length, and add-ons and provides downloadable safe-zone files.

Do not hardcode these into final delivery without re-checking the platform's current official guidance and the exact ad/product surface.

## Captions, accessibility, and localization

Deliver:

- Timed captions: SRT or WebVTT depending on platform and player. WebVTT is a W3C text-track format for captions, subtitles, descriptions, chapters, and other time-aligned metadata.
- Transcript: clean text with links, steps, and relevant disclosures.
- Burned-in caption version if social distribution needs always-on text.
- No-caption clean master if the platform supports accessible sidecar captions and the client needs a clean archive.
- Audio-described or narration-complete version when important visual content is not conveyed by the main audio.

Caption quality checklist:

- Captions match spoken words except for intentional readability edits.
- Speaker changes are identified when relevant.
- Meaningful sound effects are included.
- Captions do not cover important UI, cursor targets, or disclosures.
- Line breaks support sense units.
- Reading speed is comfortable for the intended platform and audience.
- Product names, acronyms, and technical terms are spelled correctly.
- Captions remain legible over UI and motion.

Localization planning:

- Decide whether to localize narration, captions, UI, demo data, CTA, legal/disclosure text, or all of them.
- Check whether screenshots must show the localized UI or whether translated captions over source-language UI are acceptable.
- Replace idioms and culturally specific examples; do not merely translate word-for-word.
- Leave layout expansion room; translated strings may be longer.
- Re-check claims, pricing, availability, and compliance statements by region.
- Use region-appropriate date, number, currency, address, and name formats in demo data.
- Get local reviewer approval for regulated or comparative claims.

## CTA design

Match the CTA to the viewer's readiness:

- Awareness: "See the workflow," "Watch the full demo," "Explore templates."
- Consideration: "Book a demo," "Compare plans," "Read the security brief."
- Trial/onboarding: "Create your first project," "Connect your workspace," "Import sample data."
- Expansion: "Enable the integration," "Invite your team," "Try the advanced rule."
- Support: "Open the setup guide," "Contact support," "Check permissions."

Make the CTA visible and specific. A vague "Learn more" is acceptable only when the destination is obvious and the asset is broad awareness.

## Stakeholder review

Route reviews by risk:

- Product: UI accuracy, feature availability, roadmap/release timing.
- Product marketing: positioning, audience, CTA, competitive claims.
- Sales/customer success: objection handling, buyer relevance.
- Brand/design: visual system, voice, logo, motion style.
- Legal/compliance: claims, disclosures, testimonials, regulated content.
- Security/privacy: data exposure, demo tenant, admin/security screens.
- Accessibility/localization: captions, contrast, transcript, alt/audio description, region/language quality.
- Customer/partner: any logo, quote, integration, co-marketing mention.

Use a review packet:

```text
Video link:
Transcript:
Claims ledger:
Disclosure list:
Demo data source:
Do-not-show checklist:
Delivery matrix:
Open questions:
Approval requested from:
Deadline:
```

Force timestamped feedback. Untimestamped feedback like "make it punchier" should be translated into specific edit decisions before implementation.

## Demo QA

Run QA on the rendered file and the upload/preview surface.

Content and accuracy:

- The demo flow matches the current product.
- No unsupported feature, metric, integration, certification, price, or release timing appears.
- The UI language matches approved messaging.
- The product state is internally consistent across cuts.
- The CTA points to the correct destination.

Privacy and security:

- No real PII, customer data, secrets, internal URLs, debug logs, admin-only hazards, or notification leaks.
- Mock data is clearly fictitious where needed.
- Sensitive workflows have required approvals.
- Upload metadata, filenames, thumbnails, and captions are also scrubbed.

Claims and disclosures:

- Every objective claim is in the claims ledger.
- Evidence is linked or referenced with owner/date.
- Required disclosures appear close enough, large enough, long enough, and in understandable language.
- Short cutdowns still make a truthful net impression.

Accessibility:

- Captions are present, synced, readable, and complete.
- Text contrast is sufficient.
- Color is not the only meaning carrier.
- Important visual-only information is narrated, described, or available in transcript.
- Moving/blinking/auto-updating elements used on a webpage or interactive landing page can be paused/stopped/hidden when required; WCAG SC 2.2.2 warns that moving or blinking content can distract and interfere with use.

Technical:

- Correct aspect ratio, resolution, frame rate, codec, audio mix, loudness target, filename, and file size for each destination.
- No dropped frames, cursor stutters, compression artifacts, unreadable microtext, clipped captions, or unsafe-zone collisions.
- First frame, thumbnail, title, captions, transcript, and social copy align with the video.
- Platform upload preview matches the exported file.

## Example: PLG feature launch

Example intent: create a 60-second launch video for an AI meeting summary feature aimed at customer success managers.

Brief:

- Persona: CSM managing 40 accounts.
- Use case: turn call notes into follow-up tasks.
- Primary proof: observable UI creates summary and tasks; no quantified time-saving claim approved.
- Capture: browser automation in demo tenant.
- Deliverables: 16:9 website/product page master, 4:5 LinkedIn cutdown, 9:16 social teaser, captions, transcript.

Storyline:

```text
00:00-00:04 Hook
Visual: Calendar call ends, inbox and CRM tasks are empty.
Narration: "After the call, the real work is remembering every promise."
Text: "Turn calls into follow-up tasks"
Claim: Descriptive only.

00:04-00:12 Before state
Visual: Demo account "Northstar Robotics Demo Co." with recent call transcript.
Narration: "Instead of rewriting notes by hand, open the account timeline."
Cursor: Pause on "Latest customer call" then click.

00:12-00:28 Workflow
Visual: Click "Generate follow-up." Summary appears; tasks are suggested.
Narration: "The assistant drafts the summary, pulls out next steps, and keeps the account owner in control before anything is saved."
Callouts: "Draft summary", "Suggested tasks", "Review before saving"
Disclosure: If AI output can be inaccurate, include approved wording such as "Review AI-generated content before use."

00:28-00:42 Outcome
Visual: Save tasks; CRM timeline updates.
Narration: "Now the handoff is attached to the account, not buried in a private note."
Claim: Observable UI only.

00:42-00:53 Objection proof
Visual: Permission note or admin setting if approved.
Narration: "Admins can control who can use AI summaries for customer calls."
Claim: Security/admin; requires product/security approval.

00:53-00:60 CTA
Visual: End card with product UI behind it.
Narration: "Enable AI summaries for your team from workspace settings."
Text: "Try AI summaries in Workspace Settings"
```

Generated-media prompt for a conceptual opener:

```text
Create a clean SaaS motion-graphics opener for customer success managers after a video call.
Show abstract panels representing a calendar, CRM account, and task list converging into one organized workflow.
Use fictitious labels only: "Northstar Robotics Demo Co.", "Renewal follow-up", "Demo workspace."
Do not show real brand logos, real customer data, measurable time-saving claims, or exact product UI.
Leave the lower 20% clear for captions. Use high-contrast text and do not rely on color alone.
Motion: quick but readable 3-second transition from scattered notes to organized task cards.
```

Why this works: it shows the product behavior as proof, avoids unapproved "saves time" metrics, handles the AI-review limitation, and reserves security language for approval.

## Example: help-center walkthrough

Example intent: create a 2-minute support video showing admins how to invite users with the right role.

Plan:

- Use task  steps  verification.
- Capture exact UI in a demo tenant.
- No music if it interferes with instruction.
- Cursor path is slow and deterministic.
- Deliver sidecar captions, transcript, and an article embed.

Script outline:

```text
00:00-00:08 Goal and prerequisite
Narration: "This video shows workspace admins how to invite a teammate and assign a role. You need admin access before you begin."
Visual: Settings page already open; no login sequence.

00:08-00:35 Open member settings
Narration: "From Settings, choose Members, then Invite teammate."
Cursor: Pause on Members, click; pause on Invite teammate, click.
Callout: "Settings  Members"

00:35-01:05 Enter safe demo data
Narration: "Enter the teammate's work email. In this demo, we'll use a sample address."
Visual: alex.chen@example.invalid or other reserved/demo-safe domain approved by the team.
Privacy note: No real email addresses.

01:05-01:35 Choose role
Narration: "Choose the least-permissive role that fits the work. Viewer can read projects, Editor can make changes, and Admin can manage billing and members."
Visual: Role dropdown.
Callout: "Use least-permissive access"
Claim: Product behavior; verify role definitions.

01:35-01:55 Verify invite
Narration: "After sending, confirm the invite appears as Pending. If it does not, check your permission level or contact your workspace owner."
Visual: Pending invite row.

01:55-02:00 CTA
Narration: "For bulk invites, open the CSV import guide linked below."
```

QA focus: exact button names, role definitions, captions not blocking dropdowns, no real email, and transcript matches the support article.

## Example: enterprise sales demo insert

Example intent: create a 45-second insert for a security-conscious buyer evaluating audit logs.

Approach:

- Do not use broad "enterprise-grade security" language unless approved.
- Show the precise control and what the buyer can verify.
- Keep the claim narrow: "Admins can export audit events" instead of "fully compliant."

Beat plan:

```text
00:00-00:06 Objection
Narration: "Security teams need to know who changed access before a review."
Visual: Abstract lock-to-audit-log transition, not a real incident.

00:06-00:26 Product proof
Narration: "In the admin demo workspace, filter audit events by member, action, and date range."
Visual: Audit log filters in demo tenant.
Cursor: Click filter fields slowly.
Callout: "Member", "Action", "Date range"

00:26-00:37 Export
Narration: "Export the filtered events for your review process."
Visual: Export modal with synthetic data only.
Disclosure: "Example data shown" if needed.

00:37-00:45 CTA
Narration: "Ask your account team for the security review packet."
Text: "Request security review packet"
```

Escalate if the stakeholder wants to add "SOC 2 compliant," "meets GDPR," "HIPAA-ready," "zero-trust," or "prevents breaches." Those claims need exact approved language and substantiation.

## Sources and verification notes

Sources consulted for documented constraints; checked 2026-07-10:

- FTC Advertising and Marketing Basics: claims in advertisements must be truthful, non-deceptive/unfair, and evidence-based. https://www.ftc.gov/business-guidance/advertising-marketing
- FTC Policy Statement Regarding Advertising Substantiation: advertisers need a reasonable basis for objective express and implied claims before dissemination. https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation
- FTC .com Disclosures: clear and conspicuous online disclosures, proximity, prominence, duration, mobile/device context, net impression. https://www.ftc.gov/system/files/documents/plain-language/bus41-dot-com-disclosures-information-about-online-advertising.pdf
- W3C WCAG 2.2 Understanding SC 1.2.2 Captions (Prerecorded): captions for prerecorded synchronized media with audio. https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
- W3C WCAG 2.2 Understanding SC 1.2.5 Audio Description (Prerecorded): spoken description of visual content when needed. https://www.w3.org/WAI/WCAG22/Understanding/audio-description-prerecorded
- W3C WCAG 2.2 Understanding SC 1.4.3 Contrast (Minimum): contrast rationale and 4.5:1 normal text / 3:1 large text benchmarks. https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C WCAG 2.2 Understanding SC 1.4.11 Non-text Contrast: 3:1 contrast for meaningful UI components and graphical objects. https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- W3C WCAG Understanding SC 1.4.1 Use of Color: color cannot be the only visual means of conveying information. https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html
- W3C WCAG Understanding SC 2.2.2 Pause, Stop, Hide: moving/blinking/auto-updating content needs user controls in web contexts unless exceptions apply. https://www.w3.org/WAI/WCAG21/Understanding/pause-stop-hide.html
- W3C WebVTT specification: WebVTT provides timed text tracks for captions, subtitles, descriptions, chapters, and metadata. https://www.w3.org/TR/webvtt1/
- NIST SP 800-122: guidance for protecting confidentiality of PII. https://csrc.nist.gov/pubs/sp/800/122/final
- NIST SP 800-188: de-identification techniques and governance, including re-identification risk and synthetic-data models. https://csrc.nist.gov/pubs/sp/800/188/final
- LinkedIn Video Ads Specifications: example current aspect ratios and dimensions. https://business.linkedin.com/advertise/ads/sponsored-content/video-ads/specs
- Google Ads API Performance Max asset requirements: example current YouTube video ratios and minimum duration. https://developers.google.com/google-ads/api/performance-max/asset-requirements
- TikTok Auction In-Feed Ads safe-zone guidance: safe-zone varies by dimensions, caption length, and add-ons. https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads

Volatile facts: platform specs, upload limits, ad-placement rules, safe zones, caption-file support, and claim/disclosure enforcement guidance may change. Re-check official platform/legal/accessibility sources for the exact delivery surface before publishing.
