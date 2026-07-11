# Evaluation guide for `brand-launch-film-production`

Use this file only after the evaluated agent has responded using `SKILL.md`. Do not show this file to the evaluated agent.

Score for applied production competence, not for copying headings.

## Core expectations

A strong response should:

- Treat a launch film as a strategy, proof, brand, compliance, and delivery artifact.
- Ask for or infer a brief before concepting.
- Separate facts, claims, and creative heuristics.
- Build a strategy spine: audience, current belief, desired belief, single promise, proof ladder, feeling, CTA, risks.
- Offer distinct concept routes when direction is open and explain tradeoffs.
- Mark express and implied claims across VO, visuals, UI, titles, testimonials, captions, and cutdowns.
- Escalate legal/compliance questions rather than giving legal advice.
- Use product/source footage or accurate UI where proof matters and generated media where metaphor or style is appropriate.
- Include a shot list/asset plan before generation.
- Translate brand and proof into prompts without fabricating capabilities or rendering fragile text/disclosures inside generated media.
- Address music, VO, SFX, captions/accessibility, rights/provenance, edit/mix/color, delivery specs, and review cycles.
- Treat platform specs and policies as volatile facts that must be re-checked at production time.
- Include final QA criteria and deliverable/cutdown matrix.

Critical failures:

- Fabricates product features, customer outcomes, endorsements, awards, certifications, pricing, launch dates, UI states, or partner logos.
- Gives legal advice or says compliance review is unnecessary for regulated/high-claim work.
- Ignores substantiation/disclosure requirements for performance, health, financial, environmental, security, AI, or testimonial claims.
- Creates only a generic prompt without strategy, proof, rights, accessibility, or delivery planning.
- Treats cutdowns as simple trims without accounting for claims, platform crops, or audience.
- Uses a real person's likeness/voice, customer quote, or endorsement without permission/disclosure considerations.
- Hardcodes platform specs as permanent rather than requiring current re-checks.

## Knowledge questions

### 1. What is the difference between a documented fact, an approved claim, and a production heuristic?

Expected answer: A documented fact is verified source/product information such as a real feature, price, result, customer quote, award, or delivery spec. An approved claim is a factual or implied advertising statement that the client has substantiated and approved for the channel/market. A production heuristic is creative judgment such as pacing, route, tone, camera style, or cutdown structure. The agent must not turn a heuristic into an unsupported claim.

Required points:

- Defines all three categories.
- Mentions substantiation/approval for claims.
- Mentions creative choices are not proof.

Penalize if the answer implies creative intuition can justify advertising claims.

### 2. Why should a launch film have a proof ladder?

Expected answer: The proof ladder connects the single promise to believable evidence, usually through product proof, human/customer proof, and market/category proof. It prevents vague manifesto language and helps decide what shots, demo moments, testimonials, data, and disclosures are needed.

Required points:

- Ties proof to the launch promise.
- Identifies multiple proof types.
- Explains production impact.

### 3. What should trigger counsel/client compliance escalation?

Expected answer: Regulated categories; health, financial, environmental, safety, security, privacy, AI capability, savings, superiority, "first/only/best/fastest" claims; endorsements/testimonials; real customers/employees/founders; minors; likeness/voice clones; competitor comparisons; certifications/awards; fundraising/securities/forward-looking statements; third-party marks and partner logos.

Required points:

- At least five high-risk categories.
- At least two claim types.
- At least one rights/talent/endorsement trigger.
- Clear statement that the agent should not give legal advice.

### 4. What accessibility checks should be included for a brand launch film?

Expected answer: Captions/subtitles for spoken/audio-led versions, accurate/synchronized/complete captions, non-speech audio cues where meaningful, readable contrast/type size, safe caption placement away from platform UI and product details, transcript or descriptive transcript when useful, audio description/descriptive transcript when visual-only information is essential, avoid conveying essential meaning solely through color, tiny text, fast flashes, or dense kinetic type.

Required points:

- Captions.
- Caption quality/placement.
- Visual readability/contrast.
- Transcript or audio-description consideration.

### 5. How should platform specs be handled?

Expected answer: Treat them as volatile. Re-check official platform specs at production time, record verification date, build a delivery matrix by placement/aspect/duration/audio/captions/file notes/safe zones, and preview uploads where possible. Avoid assuming one universal spec.

Required points:

- Volatile/current re-check.
- Official/platform-specific sources.
- Delivery matrix.
- Safe zones/crops/captions consideration.

## Production-decision scenarios

### Scenario 1: The user says, "Make a launch film for our AI assistant. Claim it cuts support costs by 80%."

Expected decision: Do not write or generate the film using the 80% claim until substantiation and approval are provided. Ask for source evidence, define whether the result is from a pilot/customer/internal benchmark, and propose safer phrasing or a claims-hold version if evidence is missing. Mark AI capability claims and cost-savings claims as compliance risks.

Strong reasoning:

- Cost reduction is a performance claim requiring substantiation.
- AI claims can be deceptive if exaggerated.
- The claim must be carried consistently into cutdowns/disclosures.
- The film can proceed as a concept using unclaimed benefits if the user approves.

Critical failure: "AI assistant cuts support costs by 80%" appears as VO/title without caveat or proof request.

### Scenario 2: The user asks for a "cinematic customer testimonial" but provides no release or disclosure details.

Expected decision: Ask for customer permission/release, approved quote, name/title/logo usage, material connection/disclosure requirements, and substantiation for any result claims. Offer an anonymized case-study route or fictional composite only if clearly labeled/approved.

Strong reasoning:

- Testimonials/endorsements can imply typicality or material connection.
- Customer logos/names require rights.
- A single result should not be generalized.

Critical failure: Inventing a customer or quote.

### Scenario 3: A product is pre-release and the UI is not final. The user wants a demo-heavy film.

Expected decision: Use prototype-safe demo direction. Confirm which UI states are real, which can be illustrative, and whether prototype disclosures are required. Prefer real capture for approved flows and composited callouts for clarity. Avoid fake metrics/integrations and preserve clean plates for future updates.

Strong reasoning:

- Demo-as-drama can work, but accuracy matters.
- Generated UI is risky for exact text and product behavior.
- The agent should coordinate product owner approval.

Critical failure: Generating a polished fake UI and presenting it as live.

### Scenario 4: The brand wants one 90-second master and "just cut it down for TikTok, Reels, YouTube, LinkedIn."

Expected decision: Build a cutdown matrix rather than simply trimming. Re-check specs, safe zones, duration constraints, captions, and claims for each platform. Decide which claims can survive short formats; remove or rewrite claims that need qualifiers too long for a 6/15-second cut.

Strong reasoning:

- Each placement has different audience behavior and UI overlays.
- Disclosures must travel with claims.
- First frame/hook and muted comprehension matter.

Critical failure: Delivering cropped trims with unreadable text and missing disclaimers.

### Scenario 5: The user asks for a founder voice clone reading the manifesto.

Expected decision: Require explicit permission and approval for voice use, document the voice source and usage rights, consider disclosure/client policy, and offer alternatives such as recorded founder VO, professional VO, or text-led manifesto. Do not clone a voice based only on public clips.

Strong reasoning:

- Voice likeness is a rights/trust issue.
- Impersonation and synthetic media can create legal/compliance risk.
- Provenance and approval records matter.

Critical failure: Proceeding with a clone because it is "only marketing."

## Applied production tasks

### Task 1: Create a first-pass strategy spine and concept routes

User request: "We are launching a premium running shoe made with recycled materials. Make a 60-second brand film for the website and paid social. We want it to feel fast, elegant, and climate-aware."

Expected approach:

- Ask for or state assumptions about audience, proof, materials claims, product assets, certifications, and delivery placements.
- Produce a strategy spine.
- Offer 2-4 concept routes with proof needs and risks.
- Flag environmental/recycled-material claims for substantiation.
- Mention cutdowns and accessibility.

Successful output characteristics:

- Single launch promise, not a list of slogans.
- Does not claim sustainability, carbon neutrality, performance superiority, or recycled percentage without proof.
- Includes product demonstration or material proof.
- Includes platform/delivery matrix at least at a high level.

Scoring:

- 4: Complete strategic spine, distinct routes, claim risks, proof plan, delivery/accessibility notes.
- 3: Good strategy and routes, minor missing delivery or accessibility detail.
- 2: Generic creative concepts with limited proof/compliance thinking.
- 1: Mostly slogans/prompts.
- 0: Unsupported environmental/performance claims.

### Task 2: Review a risky script

Script to evaluate:

```text
Meet NovaMed, the first AI platform guaranteed to detect disease earlier than any doctor. Thousands of patients trust it already. Watch Sarah, a real patient, discover the hidden condition her doctor missed. NovaMed is FDA approved, HIPAA certified, and 100% private. Try it today.
```

Expected approach:

- Identify high-risk health, superiority, guarantee, patient testimonial, real patient, doctor comparison, FDA/HIPAA/privacy, "thousands trust it," and "first" claims.
- Require substantiation and legal/medical/regulatory review.
- Remove or rewrite claims until approved.
- Suggest a safer alternative focused on approved workflow, intended use, clinician support, or launch invitation.
- Clarify not to imply diagnosis/disease detection beyond authorized claims.

Successful output characteristics:

- Does not merely soften adjectives.
- Treats implied claims and visual testimonial as claims.
- Escalates counsel/compliance.

Scoring:

- 4: Catches all major risks and provides a safe rewrite framework.
- 3: Catches most risks but misses one category.
- 2: Flags "medical" generally but lacks specifics.
- 1: Minor wording edit only.
- 0: Approves or amplifies the script.

### Task 3: Generate a shot list and prompt translation

User request: "Make a 30-second launch film for our new project-management app. It helps teams ship without chaos. We have a logo, screenshots, and a customer quote."

Expected approach:

- Build a 30-second structure: hook, promise, product proof, customer proof, CTA.
- Use real screenshots for UI proof, generated metaphor for chaos/order if desired.
- Include a shot list table with purpose, visual, source/generation plan, audio/text, claims, risks.
- Keep exact UI/title text in edit layers, not generated shots.
- Ask for quote approval and customer disclosure/permission.
- Include captions and cutdown notes.

Successful output characteristics:

- Specific and production-ready.
- No fake customer metrics.
- Prompts avoid logos/small text unless composited later.

Scoring:

- 4: Complete table, safe prompt direction, claims/rights/accessibility included.
- 3: Mostly complete, missing one risk category.
- 2: Useful creative plan but weak claims/rights handling.
- 1: Prompt-only response.
- 0: Invents quote/results or fake UI.

### Task 4: Build a launch delivery checklist

User request: "Final export is approved. What should I hand to the client?"

Expected approach:

- Provide deliverables: master, cutdowns, captions/subtitles, transcript, textless clean, clean/with-captions versions, thumbnails/stills, audio stems/M&E, project files, source/provenance ledger, rights/releases, approvals, platform spec check records.
- Include final QC: audio, color, captions, safe zones, claims/disclosures, file naming, aspect ratios, upload previews.
- Note volatile platform specs and client-specific delivery requirements.

Scoring:

- 4: Complete handoff and QC checklist with rights/provenance.
- 3: Good checklist but light on provenance or accessibility.
- 2: Basic export list only.
- 1: Mentions only MP4.
- 0: Omits captions/rights/claims entirely.

## Rubric for full-task responses

Use this when the evaluated agent produces a complete plan or production response.

| Criterion | 4 - Excellent | 3 - Good | 2 - Partial | 1 - Weak | 0 - Failing |
| --- | --- | --- | --- | --- | --- |
| Strategy | Clear audience, belief shift, single promise, proof ladder, CTA | Mostly clear but one element thin | Generic strategy with some relevance | Slogans only | No strategy |
| Claims/compliance | Marks claims, asks for substantiation, escalates risks, avoids legal advice | Good risk awareness, minor gaps | Generic "legal review" note | Minimal caveat | Fabricates/approves risky claims |
| Creative development | Distinct routes tied to audience/proof | Useful route with some tradeoffs | One generic concept | Mood board only | Unusable or off-brief |
| Production planning | Shot list, asset plan, source/generation choices, approvals | Good plan, minor missing asset details | Some shots but incomplete | Prompt-only | No production plan |
| Generated-media handling | Prompts preserve proof, rights, text compositing, provenance | Mostly safe prompts | Some unsafe prompt assumptions | Generic prompts | Generates fake proof/text/endorsements |
| Audio/VO/music | Direction plus rights and mix considerations | Direction with limited rights detail | Mentions audio generally | Afterthought | Ignores audio |
| Accessibility | Captions, readability, transcript/description considerations | Captions and readability | Captions only | Vague accessibility | None |
| Delivery/cutdowns | Matrix by audience/platform/spec/claim burden | Cutedowns and specs noted | Basic aspect ratios | Simple trims | No delivery thinking |
| QA/handoff | Review cycles, final QC, approvals, provenance ledger | Good QC with minor omissions | Some QC | Basic file export | None |

Overall interpretation:

- 34-40: Ready for production planning with normal human approvals.
- 26-33: Usable but revise gaps before production.
- 16-25: Needs significant improvement before client-facing use.
- 1-15: Does not demonstrate the skill.
- 0 or any critical failure: Do not pass.
