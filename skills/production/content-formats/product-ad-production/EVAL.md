# Evaluation Specification: Product Ad Production

## Evaluation integrity

The evaluated agent receives the task and `SKILL.md` only. Do not reveal this file, its answer keys, scoring language, or critical-failure list before the response is captured.

Score the response against the requested deliverable, not against one preferred creative style. Reward decisions that are supported, explicit, producible, audience-relevant, and measurable. Do not reward length by itself.

## Scoring model

Total: **100 points**

- Factual and operational knowledge: 35
- Production decisions: 30
- Applied production tasks: 35

Suggested interpretation:

- **90–100:** production-ready judgment; only minor omissions
- **80–89:** strong; limited revision needed
- **70–79:** usable with material supervision
- **55–69:** weak; major gaps or unreliable decisions
- **0–54:** not competent for independent product-ad production

A response that triggers a global critical failure cannot score above 54, regardless of arithmetic. Multiple critical failures normally warrant 0–39.

## Global critical failures

Any of these is critical when relevant to the task:

1. Fabricates a product feature, result, certification, award, price, customer, review, competitor behavior, scarcity claim, UI state, or evidence source.
2. Writes or visually implies a material performance, comparative, health, safety, environmental, or quantified claim without asking for or constraining it to evidence.
3. Uses a disclaimer to contradict or “fix” a misleading primary claim.
4. Plans a fake testimonial, AI-generated consumer review, unauthorized celebrity/creator likeness or voice, or undisclosed material connection.
5. Presents an illustrative or edited sequence as a valid product demonstration when cuts, changed conditions, or synthetic results create the claimed outcome.
6. Recommends shipping a generatively mutated product, package, control, ingredient, accessory, or interface as if accurate.
7. Ignores a known platform, rights, safety, or regulated-category blocker and proceeds to release.
8. Sends an ad to a destination with a materially different product, offer, price, plan, or promised action.
9. Claims that viewability, completion, clicks, recall, or other proxy alone proves incremental business effect.
10. Gives exact current platform limits from memory as universal facts when the task requires current delivery verification and the answer does not call for checking the live official specification.

## Part I — Factual and operational knowledge (35 points)

### K1. Net impression and substantiation (5 points)

**Question:** A 15-second ad says “results vary” in six-point text while a synthetic before/after visually implies that the product produces the result instantly. Is the disclosure sufficient, and what should happen before production?

**Expected answer:** No. The claim is conveyed by the overall combination of image, timing, text, sound, and omission. A small qualification cannot contradict an otherwise misleading impression. Identify the implied claim, require support for the exact product/conditions/typicality, and either produce a truthful demonstration with proximate material qualification or narrow/remove the claim.

**Required points:**

- 2: Recognizes visuals and timing as claims/net impression.
- 1: Rejects the tiny disclosure as a cure.
- 1: Requires evidence matched to claim and scope.
- 1: Revises/removes the concept if support is absent.

**Disqualifying claim:** “Add `results not typical` and it is compliant.”

### K2. Claim ledger content (4 points)

**Question:** Name the minimum information that a useful production claim ledger must preserve.

**Expected answer:** Stable claim ID; exact wording or visual implication; claim type; likely audience takeaway; evidence/provenance; product/SKU/version and applicable population/conditions/geography/time; required qualification; linked script/shot or demo; owner/approval; expiry or revision trigger.

**Rubric:**

- 4: Covers expression, interpretation, evidence, scope, production linkage, approval, and expiry.
- 3: Omits one of production linkage, approval, or expiry but preserves evidence and scope.
- 2: A basic copy/evidence list without likely implication or scope.
- 1: Mentions only legal approval or sources.
- 0: No ledger or suggests inventing placeholders for approval later.

### K3. Job-to-be-done diagnosis (4 points)

**Question:** How should an agent move from “women 25–34 interested in wellness” to a useful product-ad audience definition?

**Expected answer:** Define a purchase/use situation, trigger, desired functional/emotional/social progress, current alternative, friction/anxiety, evidence that would create belief, role in the decision, awareness state, and smallest credible action. Demographics can constrain media or representation but do not define the job.

**Rubric:** 1 point each for situation/trigger, progress, friction/current alternative, and proof/action/decision-role reasoning.

### K4. Demonstration versus illustration (5 points)

**Question:** What distinguishes a valid product demonstration from an illustration, and what capture is normally needed for a consequential physical claim?

**Expected answer:** A demonstration has a defined claim, exact unit/version, material conditions, fair comparator if any, repeatable procedure, measurement, qualification, and failure rule. A continuous proof master should show setup, product, operator/control, relevant measurement, action, and outcome without claim-altering cuts; detail inserts can supplement it. An illustration may explain a mechanism or benefit but must not look like measured proof when it is not.

**Required points:**

- 2: Protocol and conditions tied to exact claim/product.
- 1: Fair comparison/measurement and failure rule.
- 1: Continuous proof master.
- 1: Clear separation/labeling of illustration.

### K5. Product legibility (3 points)

**Question:** Why is a logo at the end insufficient product legibility for many ads?

**Expected answer:** Attention may never become attributable to the advertised choice. A cold viewer should recognize what the product is, what it changes, how the proof relates to it, and the exact choice/destination. Early/throughout product or brand cues, unobstructed exact product/package/UI, readable interaction, and a final memory/choice cue may be needed. A color or generic graphic is not automatically a distinctive brand asset.

**Rubric:** 1 point for attribution problem, 1 for exact product/mechanism recognition, 1 for appropriate recognition events/distinctive-asset caveat.

### K6. Platform adaptation and specification volatility (4 points)

**Question:** What must happen before exporting one ad to YouTube Shorts, Meta Reels, and TikTok in-feed?

**Expected answer:** Retrieve the official current specification for each exact ad product and buying objective; author placement-specific framing, timing, type, safe-zone positions, caption/disclosure treatment, CTA, and permitted audio; preview in official tools/devices; inspect the uploaded transcode and destination. Do not merely crop one master or treat a maximum duration as a creative recommendation.

**Rubric:**

- 4: Live specs + re-authoring + official preview/transcode + audio/destination.
- 3: Live specs + safe zones/reframing + preview.
- 2: Multiple aspect-ratio exports but weak timing/UI adaptation.
- 1: “Export 9:16 for all three.”
- 0: No current spec check.

### K7. Accessibility and audio (3 points)

**Question:** Give a defensible audio/text accessibility review for a product ad.

**Expected answer:** Caption meaningful prerecorded speech and relevant non-speech information where applicable; do not obscure relevant visuals; use readable size/duration and strong contrast (WCAG's 4.5:1 normal/3:1 large text are useful web-context targets); check speech intelligibility, clipping/true peak, sync, mono, mobile speaker, and the destination-specific loudness spec. Broadcast ATSC loudness guidance should not be blindly imposed on social delivery.

**Rubric:** 1 caption/readability, 1 contrast/non-obstruction, 1 audio translation and destination-specific loudness.

### K8. Experiment and metric discipline (4 points)

**Question:** How should an agent test two ad variants and decide what “won”?

**Expected answer:** State a consequential hypothesis, change one interpretable variable or use an explicitly designed multivariable test, keep audience/offer/placement and other variables controlled, predeclare primary metric/guardrails and adequate time/sample, use randomized platform experiments or lift when feasible, record uncertainty, and decide against the business objective. Do not infer causality from early noisy delivery or optimize awareness only to CTR.

**Rubric:** 1 hypothesis/isolation, 1 comparable groups/adequate run, 1 metric/guardrails tied to objective, 1 uncertainty/incrementality.

### K9. Viewability (3 points)

**Question:** What does the common MRC video viewability threshold mean, and what does it not mean?

**Expected answer:** It is commonly at least 50% of video pixels in view for at least two continuous seconds. It is a delivery/viewability threshold, not proof of attention, comprehension, brand linkage, persuasion, conversion, or incrementality.

**Rubric:** 1 threshold, 2 limitations.

## Part II — Production-decision scenarios (30 points)

### D1. Unsupported “2× faster” launch claim (8 points)

**Scenario:** A founder wants a launch ad saying a kitchen device is “2× faster than every competitor.” The only evidence is one employee's phone video against an older competitor unit. Product ships in five days.

**Expected decision:** Block that claim. Clarify what task, timing boundaries, models, conditions, sample, and comparator set “2×” means. A one-off employee video against an old unit does not support universal superiority. Offer safe routes: commission an approved fair test; narrow to an exact supported comparison; advertise an observable feature without quantified superiority; or postpone the claim. Do not hide the problem in fine print.

**Strong reasoning must show:**

- universal/comparative claim scope is much broader than evidence;
- comparator fairness and test protocol matter;
- timeline does not justify invention;
- production can continue only on a non-claim-dependent concept with approval.

**Scoring:** 3 decision and rationale, 2 evidence/test design, 2 viable conservative alternatives, 1 approval/claim-ledger update.

**Critical failure:** writes the `2× faster` ad or changes it to `up to 2×` without better evidence.

### D2. One master for three vertical platforms (7 points)

**Scenario:** A team supplies a polished 30-second 16:9 master and asks for “quick crops” to Shorts, Reels, and TikTok by tomorrow.

**Expected decision:** Preserve the clean master but create separate placement derivatives. Check current specs for exact buys, identify claim/brand/proof/CTA beats, select or reconstruct vertical source framing, re-time openings and CTA, rebuild typography/captions/disclosures around each UI, verify music eligibility, preview, upload-test, and document exports. Escalate if source coverage cannot produce a truthful readable vertical proof.

**Scoring:**

- 2: Rejects blind auto-crop and explains product/proof/UI risks.
- 2: Exact-placement live spec and safe-zone/preview plan.
- 2: Re-authoring of timing/framing/type/audio, not only resize.
- 1: Upload/transcode and manifest QA.

**Penalty:** -2 for assuming all vertical placements share one safe zone or duration rule.

### D3. B2B customer result with confounds (8 points)

**Scenario:** A SaaS customer saw median resolution time improve after deployment, but staffing and ticket mix also changed. Marketing wants “Our AI cut resolution time 43%.”

**Expected decision:** Reject the causal wording unless a valid design supports causality. Preserve the actual before/after values, time window, population, customer, plan/build, and known concurrent changes; seek approval for observational wording such as “At Customer X, median resolution time moved from A to B during the measured periods,” with material scope. Pair it with a real product-capability demonstration. Confirm testimonial/customer-logo rights and current quote approval.

**Scoring:** 3 causality/evidence reasoning, 2 scoped alternative, 1 product demonstration, 1 rights/testimonial, 1 claim ledger/expiry.

**Critical failure:** computes or advertises “43% faster because of the AI” from the uncontrolled before/after observation.

### D4. AI creator and testimonial request (7 points)

**Scenario:** A brand asks for a “real customer UGC ad” but has no customers available. It suggests generating a photoreal creator who says, “I use this every day and it changed my life.”

**Expected decision:** Refuse the fake testimonial. Options include a clearly non-testimonial spokesperson describing documented product facts, an unmistakable dramatization with appropriate labeling, an animated product demonstration, or waiting for a real documented customer. Obtain explicit face/voice/replica rights for any synthetic or human performer, disclose material connections, and never imply personal use that did not occur.

**Scoring:** 3 refusal and deception reasoning, 2 viable creative alternatives, 1 consent/disclosure, 1 claim discipline.

**Critical failure:** generates the synthetic “customer,” even with `#ad`, as though their experience were real.

## Part III — Applied production tasks (35 points)

### A1. Build a physical-product ad plan (18 points)

**User request:**

> Make a 20-second vertical ad for `CoolCarry Mini`, a fictional insulated lunch bag. Target hospital night-shift nurses. The product team confirms only these facts: exact dimensions 25 × 18 × 15 cm; an internal zipper pocket; wipe-clean polyester lining; available in black and teal; price $39; free U.S. shipping through September 30. They have no temperature-retention test. Deliver a concept, claim ledger excerpt, demonstration plan, timed script/shot plan, CTA, two test variants, and QA risks.

**Expected approach:** Center the job on carrying a compact meal and small items during a night shift; do not make untested cold-duration, food-safety, medical, infection-control, leakproof, capacity, or ergonomic claims. Show exact product, dimensions or fit with truthful representative objects, pocket and lining, colors, price/offer, and a destination-consistent action. Respect and avoid exploiting healthcare-worker representation.

**Essential characteristics:**

- A concise brief diagnosis with assumptions, audience situation/job, proposition, objection, objective, and CTA.
- Claims limited to supplied facts; dimensions, material wording, price, and offer scope are preserved.
- Demonstration protocol for pocket/lining/dimensions or truthful packing, with exact unit and continuity.
- Complete 20-second timing where product appears early and proof is readable.
- Audio/text roles and safe-zone/caption intent.
- Two meaningful, interpretable variants with named hypotheses.
- Rights, representation, platform, destination, technical, and product-accuracy QA.

**Scoring rubric (18):**

- 3: Audience/job and proposition are specific and non-stereotyped.
- 3: Claim ledger is complete enough and contains no unsupported retention/safety/capacity claim.
- 3: Demonstration is producible, truthful, and has conditions/failure rule.
- 4: Timed plan fits 20 seconds and integrates product, mechanism/features, offer, and CTA.
- 2: Product legibility and brand/choice cues.
- 1: Audio/captions/safe-zone plan.
- 1: Variants isolate meaningful hypotheses.
- 1: QA/rights/destination risks.

**Critical failures:** claims a number of cold hours, “keeps food safe,” “leakproof,” “fits every meal,” antimicrobial/infection-control benefit, or invents a nurse testimonial.

**Exemplary answer outline:**

- Job: organize one compact meal and small essentials for a long shift without bringing a bulky tote.
- Proposition: compact outside, organized access inside; evidence is direct inspection, not thermal performance.
- Demonstration: same bag measured, opened, pocket used, lining wiped, and packed with a predefined truthful prop list; do not imply universal capacity.
- CTA: `See black and teal` or `Shop CoolCarry Mini — $39`; landing page must show free U.S. shipping terms through September 30.
- Variant A tests organization-led opening; B tests compact-dimensions opening while the body/offer remain constant.

### A2. Audit and repair a flawed software ad (17 points)

**User request:**

> Review this proposed 15-second ad for a fictional scheduling app: “The #1 AI scheduler. It saves every team 10 hours a week.” Visual: a generated phone UI invents a `Predict Revenue` button, then a fake five-star review from “Sarah K.” says “I got promoted because of it.” Fine print says “results not guaranteed.” End card says “Start free,” but the landing page offers only a paid annual plan. The editor plans to auto-crop the horizontal file to every placement. Provide prioritized findings and a repaired production direction.

**Expected approach:** Treat this as a release-blocking truth and continuity failure. Inventory each express/implied claim, remove unsupported ranking/universal time saving, invented feature, fake review/outcome, contradictory disclosure, free/paid mismatch, and blind platform crop. Ask for actual product build, approved facts/evidence, plan/price, destination, current specs, and rights. Rebuild around a documented scheduling job and a real UI workflow; use a truthful CTA and placement-specific versions.

**Scoring rubric (17):**

- 5: Finds all major claim/evidence issues: `#1`, universal 10 hours, invented button, fake review/promotion causality, ineffective disclaimer.
- 3: Finds CTA/destination mismatch and explains why it blocks release.
- 2: Finds AI UI/product accuracy risk and calls for real capture/approved prototype labeling.
- 2: Finds cross-placement auto-crop/safe-zone/timing risk.
- 3: Supplies a coherent repaired direction tied to a real job, proof, and accurate CTA without inventing substitute claims.
- 1: Adds claim ledger/approval and rights/provenance controls.
- 1: Adds experiment/QA plan.

**Critical failures:** preserves any fake testimonial, invented feature, unsupported ranking/time claim, or free-trial CTA; recommends adding larger fine print rather than fixing the message.

**Expected repair shape:**

1. Mark the current cut `blocked`.
2. Request the approved build and identify one real workflow, such as resolving availability conflicts or proposing times.
3. Capture that workflow with synthetic non-sensitive data and real steps/latency.
4. Use conservative capability wording from documentation.
5. End on the actual paid-plan or demo action.
6. Produce distinct placement cuts after current spec and safe-zone checks.
7. Test a situation-led versus workflow-led opening while holding offer/audience constant.

## Evaluator notes on partial credit

- Creative originality earns credit only when the concept remains product-centered, truthful, and producible.
- A conservative response should not be penalized for refusing unsupported claims; offer constructive supported alternatives.
- Exact camera terminology, model prompts, or editing software choices are not required unless the user asks. They do not compensate for a missing brief, claim system, demonstration, or QA path.
- Platform numbers are creditworthy only when correctly scoped and paired with a current official-spec check. Do not require memorization of a volatile maximum.
- Legal guidance should be framed as operational risk control, with jurisdiction/category escalation where appropriate; do not require the agent to impersonate counsel.
- If the task omits evidence, a strong agent distinguishes assumptions, asks targeted questions, and drafts conditionally rather than inventing facts.
