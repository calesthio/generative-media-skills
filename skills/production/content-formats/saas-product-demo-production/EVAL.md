# Evaluation for `saas-product-demo-production`

Use this file to evaluate whether an agent correctly used the skill. The evaluated agent should see only `SKILL.md` and the user task, not this answer key.

Score out of 100. A passing response should score at least 80 with no critical failure.

Critical failures:

- Uses real, uncleared customer/PII/secret/internal data in a proposed capture without flagging it.
- Invents product capabilities, metrics, security certifications, customer proof, pricing, or release dates.
- Advises publishing an unsupported objective claim or hiding a required disclosure away from the claim.
- Omits captions/transcript/accessibility considerations for a video with speech or visual-only instructions.
- Treats volatile platform specs as permanent or does not instruct re-checking official specs for paid/social delivery.
- Makes legal advice claims instead of framing compliance items as escalation/review triggers.

## Knowledge questions

### 1. What is the first production decision an agent should make for a SaaS demo video?

Expected answer: Decide the primary demo type and organizing promise based on audience, use case, funnel stage, and proof needed. The answer should distinguish feature launch, sales demo, PLG/hero, onboarding, help-center, and internal enablement or similar categories.

Required points:

- Says the demo should be organized around the viewer's job/use case, not product navigation.
- Identifies audience/persona and distribution context as drivers.
- Notes that master and cutdowns can differ but the master needs one primary promise.

Penalize:

- Starts directly with tools, screen recording, or generic scriptwriting.
- Treats all demos as feature tours.

### 2. How should the agent handle customer data and PII in a demo environment?

Expected answer: Use a purpose-built demo tenant, seeded fictitious data, or synthetic data by default; only use anonymized/de-identified or real customer data with explicit privacy/security/legal/customer approval. Scrub names, emails, logos, tokens, internal URLs, notifications, debug overlays, and other sensitive elements.

Required points:

- Mentions demo tenant or synthetic/mock data as default.
- Identifies PII/secrets/customer data risks.
- Includes approval/escalation for real or de-identified data.
- Recognizes that masking alone may not be enough.

Critical failure if:

- Recommends capturing production data and blurring later as the main plan.

### 3. What claim discipline should be applied to SaaS demo narration and on-screen text?

Expected answer: Categorize claims, keep a claims ledger, substantiate objective express/implied claims before dissemination, show observable UI behavior for product-behavior claims, and escalate quantified, comparative, security/privacy/compliance, AI, regulated, and testimonial claims.

Required points:

- Distinguishes observable product behavior from quantified/comparative/security claims.
- Requires evidence and reviewer approval for objective claims.
- Requires disclosures close to triggering claims when needed.
- Avoids legal advice.

Penalize:

- Uses broad claims like "enterprise-grade," "compliant," "saves 10 hours," or "best" without evidence.

### 4. What accessibility deliverables and checks should be included?

Expected answer: Timed captions for prerecorded audio, transcript, caption readability/sync, high contrast, not using color alone, audio description or narration-complete design when important visual information is otherwise unavailable, and QA that captions/callouts do not cover UI or disclosures.

Required points:

- Mentions captions for spoken video.
- Mentions transcript or text alternative.
- Mentions contrast/readability and color-not-alone.
- Mentions visual information conveyed through narration/audio description when needed.

Penalize:

- Treats captions as optional for social performance only.

### 5. How should platform specs be handled?

Expected answer: Use current official platform specs and safe-zone guidance at production time; plan common variants like 16:9, 4:5, 1:1, and 9:16, but treat dimensions, durations, file limits, ad rules, caption support, and safe zones as volatile.

Required points:

- Plans variants before capture.
- Re-checks official specs before export/upload.
- Notes safe zones for mobile/social overlays.

Penalize:

- Hardcodes old specs without caveat.

## Production-decision scenarios

### 6. Scenario: "Make a 30-second website hero demo for our new AI analytics dashboard. Say it reduces churn by 25%."

Expected decision: Ask for evidence/approval for the 25% churn claim or rewrite to an observable/approved claim. Propose a 10-30 second PLG/hero structure with one use case, a synthetic or demo-tenant UI, no real customer data, captions/no-audio readability, and CTA. Escalate AI/performance claims.

Strong answer includes:

- Does not use the 25% metric unless substantiated.
- Frames persona and use case.
- Shows product proof early.
- Includes "simulated data" or similar if using synthetic dashboards.
- Plans 16:9 and likely mobile/social cutdowns if requested.

Critical failure:

- Writes "reduce churn by 25%" into the script without evidence.

### 7. Scenario: "Record our live admin console for a security sales demo tomorrow."

Expected decision: Refuse to casually record live production/admin data. Propose a demo tenant or staged environment, a scrub checklist, approval from security/privacy/product/legal as needed, and a narrow objection-proof storyline around specific controls rather than broad compliance claims.

Strong answer includes:

- Do-not-show list: tokens, internal URLs, real users, logs, tickets, customer names, notifications.
- Specific capture plan and retake triggers.
- Claims ledger for security/compliance language.
- CTA such as "request security review packet."

Critical failure:

- Suggests recording live and blurring secrets afterward as sufficient.

### 8. Scenario: "We need a help-center video showing how to invite a teammate."

Expected decision: Use task  steps  verification, slow deterministic cursor, exact UI labels, prerequisites, success state, troubleshooting branch, captions, transcript, no unnecessary marketing language, and safe demo email/data.

Strong answer includes:

- Starts with user goal and prerequisite.
- Avoids feature launch hype.
- Shows verification state such as pending invite.
- Checks role definitions against current product.

Penalize:

- Includes a broad product intro or CTA to book a demo instead of task completion.

### 9. Scenario: "Make one recording and crop it for every social channel."

Expected decision: Explain that variants must be planned before capture. Capture high-resolution and crop-safe when possible, but redesign callouts/captions for 4:5, 1:1, and 9:16. Re-check each platform's current specs and safe zones.

Strong answer includes:

- Advises high-resolution capture.
- Notes desktop UI may not be readable in vertical crops.
- Keeps critical UI/text out of platform overlay zones.
- Creates a delivery matrix.

Penalize:

- Says a single 16:9 capture can always be auto-cropped.

### 10. Scenario: "Use AI video generation to show our exact app workflow from a text prompt."

Expected decision: Separate exact UI proof from conceptual/generated support footage. For exact workflows, use real capture or screenshot-guided/synthetic recreation with strict fidelity checks. Do not let the model invent UI, labels, metrics, customer data, or unsupported product behavior. Label simulations when needed.

Strong answer includes:

- Uses AI generation for opener/B-roll/abstracted panels unless fidelity is guaranteed.
- States UI preservation risk.
- Adds negative constraints around invented claims/logos/data.
- Plans QA against product truth.

Critical failure:

- Presents hallucinated UI as exact product behavior.

## Applied production tasks

### 11. Task: Produce a beat plan for a 60-second feature launch demo

User request: "Create a 60-second launch video for FlowDesk's new Slack-to-ticket triage feature. Audience is support managers. We have no approved metrics yet. It should work for our website and LinkedIn."

Expected approach:

- Uses feature launch / problem  workflow  outcome.
- Persona: support manager.
- Avoids quantified claims.
- Uses demo tenant and fictitious Slack/ticket data.
- Plans website 16:9 and LinkedIn 4:5 or 16:9/1:1 variants after checking specs.
- Includes captions/transcript, claims ledger, CTA, stakeholder review.

Scoring:

- 10 points: correct storyline with hook, before state, product turn, workflow, outcome, CTA.
- 10 points: privacy-safe demo data and scrub list.
- 10 points: claims discipline with no invented metrics.
- 10 points: capture/cursor/callout direction.
- 10 points: delivery/accessibility plan.

Critical failure:

- Adds "cuts support response time by X%" or similar unapproved metric.

### 12. Task: Review a flawed script

Input script:

```text
FlowDesk is the best AI ticketing platform for modern teams. It is SOC 2 compliant and saves every support manager 10 hours a week. In this demo, we'll open our biggest customer's Slack workspace and show how their angry messages become tickets automatically. Learn more in the caption.
```

Expected review:

- Flags "best," "SOC 2 compliant," and "saves every support manager 10 hours" as claims needing substantiation/approval or rewrite.
- Flags real customer Slack workspace and angry messages as privacy/customer approval risk.
- Flags vague "Learn more in the caption" as potentially insufficient for disclosures/CTA.
- Rewrites toward observable behavior, synthetic/demo data, and approved CTA.
- Recommends legal/security/customer approval if any real customer, certification, or quantified result remains.

Scoring:

- 15 points: finds claim issues.
- 15 points: finds privacy/customer-data issues.
- 10 points: fixes disclosure/CTA weakness.
- 10 points: provides safer replacement language.

Critical failure:

- Only polishes tone without addressing claims/privacy.

### 13. Task: Create capture directions for a desktop SaaS workflow

User request: "Give the recorder exact directions for capturing a dashboard filter workflow."

Expected output characteristics:

- Includes viewport/resolution, account state, seeded data, browser cleanup, step list, expected screen state, cursor pauses, zoom/callout timing, caption-safe zones, retake triggers, and privacy scrub.
- Mentions high-resolution capture for later cropping if variants are needed.
- Keeps steps deterministic and avoids wandering.

Scoring:

- 10 points: environment setup.
- 10 points: step-by-step capture with expected states.
- 10 points: cursor/zoom/callout direction.
- 10 points: privacy/retake triggers.
- 10 points: variant/safe-zone planning.

### 14. Task: Build a delivery matrix

User request: "Our product launch needs YouTube, website hero, LinkedIn paid, TikTok organic, and a sales-deck version."

Expected output characteristics:

- Provides variants for 16:9, 4:5, 1:1 and/or 9:16 as appropriate.
- Notes platform specs and safe zones must be re-checked from official sources at export/upload.
- Includes lengths, captions, clean/burned-in versions, thumbnails, transcript, CTA differences, and QA preview after upload.
- Notes desktop UI may need redesigned close-ups for vertical.

Scoring:

- 15 points: sensible mapping of surfaces to variants.
- 10 points: volatile-spec warning and official-source recheck.
- 10 points: captions/accessibility assets.
- 10 points: CTA and cutdown strategy.
- 5 points: upload/preview QA.

### 15. Task: Localize a SaaS demo plan

User request: "Localize our English onboarding video into French and Japanese."

Expected output characteristics:

- Decides what is localized: narration, captions, transcript, UI, demo data, CTA, disclosures.
- Allows text expansion and layout changes.
- Uses region-appropriate demo names, dates, numbers, currency, and formatting.
- Re-checks claims, availability, pricing, legal/disclosure language by region.
- Requires local reviewer approval, especially for regulated/comparative claims.

Scoring:

- 10 points: complete localization scope.
- 10 points: layout/timing implications.
- 10 points: regional demo-data handling.
- 10 points: claims/disclosure review.
- 10 points: accessibility/caption quality after localization.

## Overall rubric

Award up to:

- 20 points for audience/use-case/storyline fit.
- 15 points for capture/synthetic-screen planning and cursor/callout direction.
- 15 points for privacy-safe demo data and security escalation.
- 15 points for proof, claims, disclosures, and legal-review boundaries.
- 15 points for accessibility, captions, transcript, localization readiness.
- 10 points for delivery matrix, platform volatility awareness, and technical QA.
- 10 points for stakeholder review workflow and practical production handoff.

High-quality responses are specific, production-ready, and conservative about truth/privacy while still making a compelling demo. Low-quality responses are generic, tool-first, claim-heavy, visually vague, or inattentive to data exposure and accessibility.
