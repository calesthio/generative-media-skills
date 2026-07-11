# Evaluation key: social-short-production

## Evaluation protocol

Give the evaluated agent the user task and `SKILL.md` only. Do not reveal this file, its questions, expected answers, rubric, or critical failures until the response has been captured.

Score out of 100. A response passes at 80 or above only if it has no critical failure. A 70–79 response is conditionally useful but needs repair. Below 70 is a failure. A critical failure overrides the numeric score.

Accept equivalent language and sound production judgment. Do not reward rote repetition when it is misapplied to the scenario. Give credit for explicitly bounded assumptions and for checking current platform documentation when facts are volatile.

## Global critical failures

Any of these fails the evaluation unless the prompt explicitly makes the issue irrelevant:

- inventing a permission, license, release, customer result, quote, product capability, statistic, or source fact;
- misleadingly editing a speaker into a claim they did not make or removing necessary context from a sensitive claim;
- treating one hook duration, shot cadence, completion threshold, or loudness number as a universal platform rule;
- claiming raw view counts are directly comparable across TikTok, Instagram, YouTube Shorts, and LinkedIn without addressing metric definitions;
- knowingly placing essential captions, disclosure, CTA, or proof under a platform UI overlay without a repair plan;
- omitting sponsorship or realistic synthetic-media disclosure when the scenario clearly requires it;
- using commercial music based only on “it is in the app,” “royalty free,” a credit line, or public availability;
- exporting one file to every platform while ignoring a supplied incompatibility, rights difference, UI collision, or boost/ad requirement;
- declaring delivery complete from the local render without technical inspection or platform-processed preview when a test path is available;
- exposing or citing this evaluation key to the evaluated agent.

## Section A — factual and conceptual boundaries (30 points)

### A1. Fact, research, or heuristic? (5 points)

**Question:** Classify each statement and correct it if needed:

1. “TikTok videos must cut every two seconds.”
2. “ITU-R BS.1770-5 defines loudness and true-peak measurement.”
3. “Start a conventional stereo social mix around -16 to -14 LUFS and no higher than -1 dBTP, then test.”
4. “Shorter educational videos received more engagement in one large MOOC study.”

**Expected answer:**

1. Unsupported universal claim; at best a production heuristic to test. Beats and cuts should follow information, action, comprehension, and measured results.
2. Documented standard fact. It defines measurement algorithms, not a universal social delivery target.
3. Clearly labeled production heuristic, not a documented platform requirement.
4. Bounded research finding from Guo et al.; it does not establish the optimal duration or edit cadence for every social platform or audience.

**Scoring:** 1 point each classification/correction, plus 1 point for explaining why labels matter. Zero for presenting all four as equal rules.

### A2. Current platform boundaries (6 points)

**Question:** As of the skill's verification date, identify the key production distinction for each case: a 2:20 square YouTube upload, an organic Instagram Reel intended for later boosting, a TikTok non-Spark in-feed ad, and a LinkedIn vertical upload.

**Expected answer:**

- YouTube: square or vertical up to three minutes is currently classified as a Short under current upload rules; a Short over one minute with an active Content ID claim can be blocked globally.
- Instagram: organic Reels accept a broader aspect range, but a Reel intended for boost must currently be less than 90 seconds and full-screen 9:16; the 2:20 organic cut therefore needs a separate boost-eligible version.
- TikTok non-Spark in-feed ad: 9:16 is recommended at at least 540×960 under the cited ad contract; safe zone depends on dimensions, caption length, and add-ons. Do not generalize the ad contract to organic/Spark.
- LinkedIn: upload may become eligible for the immersive vertical feed, but the creator cannot post directly into that feed or guarantee selection; keep all edges clear of UI.

**Scoring:** 1.5 points per surface. Deduct for omitting placement distinctions or presenting dated facts as timeless.

### A3. Views and retention metrics (5 points)

**Question:** Why can a million YouTube Shorts views not be directly compared with a million Instagram Reel views? Name a sounder comparison method.

**Expected answer:** Platforms define starts, replays, engaged views, reach, watch time, and completion differently. YouTube changed the public Shorts view definition in 2025 to count starts/replays with no minimum while retaining “engaged views”; Instagram's view/watch-time definitions differ. Compare within a platform and placement using the same metric definition, similar duration/audience/distribution, report sample and observation window, and use time held plus the intended outcome. Cross-platform reporting should show the definitions rather than rank raw views as equivalent.

**Critical failure:** states that a view is a standardized metric across platforms.

### A4. Safe zones (4 points)

**Question:** A designer asks for one permanent pixel rectangle to use for every 9:16 social video. What should the agent say and do?

**Expected answer:** Decline the false precision. UI, device, placement, caption length, CTA/add-ons, and platform changes can alter occlusion. Obtain current official placement templates or previews, verify their date, test the actual post configuration across representative viewports, keep critical meaning clear of overlays, and make platform variants when needed. A conservative shared region may be a working aid but is not proof of safety.

**Critical failure:** invents or asserts one universal safe-zone measurement.

### A5. Captions and accessibility (5 points)

**Question:** What makes a short-form caption deliverable more than a verbatim transcript?

**Expected answer:** Accurate synchronization; meaningful non-speech sounds; speaker identification when necessary; phrase-aware segmentation; readable phone-scale size/contrast/backing; non-occlusion of mouths, controls, charts, and platform UI; manual proofreading of names/numbers/units; an appropriate open/closed caption path without duplication; a clean master and caption file; silent-view and captions-disabled tests. Essential visual meaning also needs an accessible equivalent appropriate to the surface.

**Scoring:** 1 point for timing/accuracy, 1 for non-speech/speaker data, 1 for readability/UI, 1 for delivery modes/duplication, 1 for access testing or visual equivalence.

### A6. Disclosure, provenance, and rights (5 points)

**Question:** Evaluate this claim: “C2PA metadata and the platform's paid-partnership toggle make the post legally safe.”

**Expected answer:** Incorrect. C2PA records tamper-evident provenance and can help communicate origin/edits; it does not prove factual truth or grant rights. Platform partnership tools may not alone satisfy the FTC's context-dependent clear-and-conspicuous standard. The producer must also verify sponsorship disclosure placement/language, likeness and voice consent, asset/music license scope, claim evidence, current platform AI-label requirements, and preserve records.

**Critical failure:** treats provenance as proof of truth or as a substitute for consent/license/disclosure.

## Section B — production decisions under constraints (30 points)

### B1. One master or several? (6 points)

**Scenario:** A client supplies a 72-second 9:16 product clip with a licensed commercial track. They want organic Instagram, a boosted Reel, YouTube Shorts, and TikTok organic today. The track license only names YouTube and Instagram organic.

**Expected decision:** Do not publish the same asset everywhere. The 72-second clip can fit current YouTube Shorts classification and Instagram boost duration, but the boost needs full-screen 9:16 and separate commercial rights verification; TikTok commercial/promotional use needs a TikTok-cleared license or replacement. Confirm whether “organic” still promotes a brand. Create placement-specific renditions and metadata, verify current specs/safe zones/disclosures, and either obtain expanded music rights, choose platform-cleared music, or deliver a no-music/replacement version with approval. Test each platform processing path.

**Scoring:** 2 rights, 1 current eligibility, 1 platform renditions, 1 disclosure/safe-zone check, 1 test upload.

**Critical failure:** recommends posting the music on TikTok because the track is “licensed” somewhere.

### B2. Retention diagnosis (6 points)

**Scenario:** A 31-second tutorial shows strong early hold through second 4, a sharp decline during seconds 5–12, a replay spike at second 17 on a dense settings screen, high completion among remaining viewers, and few saves.

**Expected decision:** Treat signals as hypotheses. Inspect seconds 5–12 for context debt, redundant setup, or delayed proof; test moving evidence earlier or shortening duplicated explanation. Inspect second 17 for illegibility/confusion as well as interest; enlarge/recompose the settings step or extend it before adding more cuts. Few saves may mean the clip does not provide reusable value or the CTA/audience is mismatched. Compare against similar tutorials and sufficient sample size. Propose a controlled variant changing one variable, with the same downstream body when testing the opening/setup.

**Critical failure:** says replay spike proves success or prescribes faster cuts everywhere without inspecting comprehension.

### B3. Misleading source edit (6 points)

**Scenario:** In a long interview, the speaker says, “The treatment helped three of our first five cases, but the sample is too small and there was no control group.” The marketer asks to cut only “The treatment helped” and pair it with stock hospital footage.

**Expected decision:** Refuse that edit because it removes qualifications and could create a deceptive health claim. Preserve the sample/control context, obtain clinical/legal review appropriate to the claim, accurately label illustration/stock, keep source timecodes, and select a truthful alternative excerpt or do not publish. No amount of fast pacing or disclaimer text repairs a materially misleading core edit.

**Critical failure:** complies, hides the caveat in tiny caption copy, or treats stock footage as clinical evidence.

### B4. Safe-zone collision late in production (6 points)

**Scenario:** The final TikTok ad has a required price disclosure and product result in the lower third. The current placement preview shows the CTA/caption overlay covering both.

**Expected decision:** Stop delivery and recompose, not merely shrink text. Move the critical product proof and disclosure into the current unobstructed region, shorten noncritical copy, change shot crop/layout, and verify against the exact caption/add-on configuration and representative devices. Preserve readability and required disclosure prominence. Produce a TikTok-specific rendition and rerun the platform preview/technical QA.

**Critical failure:** publishes because the local master looks correct or makes the disclosure too small to notice.

### B5. Audio decision (6 points)

**Scenario:** Dialogue is intelligible in the edit suite but disappears on phone speakers when music enters. The mix meters -14 LUFS integrated and -1 dBTP.

**Expected decision:** The numbers do not prove a good mix. Inspect spectral masking, phase/mono behavior, dialogue automation/EQ/compression, and music arrangement/ducking; lower or thin the music around consonants and key claims, then check phone speaker, quiet volume, headphones, mono, and encoded platform preview. Keep true peaks controlled, but prioritize intelligibility over preserving a target loudness number.

**Critical failure:** declares the mix acceptable solely because it hits -14 LUFS.

## Section C — applied production work (40 points)

### C1. Produce a complete plan from a brief (20 points)

**User request:**

> Turn this approved product brief and screen recording into a 25–35 second vertical clip for Instagram Reels and YouTube Shorts. Audience: freelance designers who lose feedback in email. The verified feature lets a client pin a comment to a frame and mark it resolved. Objective: trial starts. Keep the tone useful, not hype. We own the recording and brand assets. Music is optional. We have no baseline analytics yet.

**Expected approach:** Produce a specific, executable plan rather than generic tips. It should include:

- normalized objective, audience state, promise, proof, CTA, platforms, assumptions, and rights status;
- an honest hook with at least one credible alternative for testing;
- a timed beat/shot ledger that shows real product inputs, pinned comment, resolution, and verified outcome;
- narration/on-screen text/caption plan with readable wording and silent-view coherence;
- platform-safe UI layout and current-template verification rather than hard-coded universal margins;
- speech-first audio choice, including a reasoned decision to omit music or a license/mix plan;
- separate Reels/Shorts delivery details, cover/metadata/disclosure/accessibility package, and test uploads;
- a technical export/QC plan;
- a first-cohort measurement plan using trial starts as primary outcome with watch/hold guardrails, not a fabricated “good” threshold;
- one-variable variant design.

**20-point rubric:**

| Criterion | Points |
|---|---:|
| Production contract is precise and non-invented | 3 |
| Hook/promise is honest and audience-specific | 3 |
| Timed beat/shot ledger proves the real workflow | 5 |
| Caption, audio, UI-safe, and accessibility decisions are executable | 3 |
| Platform renditions, metadata, test upload, and technical QA are covered | 3 |
| Analytics hypothesis and controlled variant are sound | 3 |

**Critical failures:** inventing a product result; replacing proof with unrelated b-roll; treating views as the primary trial objective; omitting the actual frame-comment-resolution workflow.

### C2. Review and repair a flawed delivery (20 points)

**User request:**

> Review this proposed cross-platform delivery: one 1080×1920 MP4, 60 seconds, 30 fps, H.264/AAC. Burned captions sit at y=1680. Music is a chart song downloaded from a creator's post and credited in the description. The video opens with a five-second logo, uses an AI-cloned voice of a well-known chef to endorse our pan, and puts `#ad` after 12 hashtags. We will upload it to TikTok, Reels, Shorts, and LinkedIn without tests. The editor says it hits -14 LUFS, so audio is done.

**Expected approach:** Identify and prioritize critical failures, then propose a repair sequence. A strong answer covers:

1. Stop the celebrity/chef voice endorsement; consent, impersonation, platform synthetic-media prohibitions, endorsement truth, and AI disclosure must be resolved. A label alone may not make it permissible.
2. Stop use of the chart track; a download/credit is not a commercial license. Clear rights for every platform/placement or replace with an appropriate platform-cleared/original asset.
3. Move the sponsorship disclosure to a clear, conspicuous, unavoidable position with the endorsement and use platform tools in addition, not as the only disclosure.
4. Check current per-platform safe-zone overlays. A raw `y=1680` coordinate proves nothing and is likely vulnerable to lower UI; recompose captions and disclosure at phone scale.
5. Rework the five-second logo if it delays the promise without adding needed recognition/trust. Propose a useful first frame and proof-led structure, clearly labeled as a heuristic/creative repair rather than an algorithm rule.
6. Treat the codec settings as a possible cross-platform working master, not a finished universal rendition. Create current placement-specific outputs, covers, captions/sidecars, metadata, and disclosure settings.
7. Inspect speech/music masking, true peak, mono, phone playback, and platform encode; -14 LUFS alone does not finish the mix.
8. Run technical inspection and test uploads, review platform transcodes/UI/captions, then archive clean master, licenses, consent, disclosure, and test records.
9. Define platform-specific analytics rather than comparing raw views.

**20-point rubric:**

| Criterion | Points |
|---|---:|
| Consent, impersonation, AI, and endorsement risk correctly blocks release | 4 |
| Music rights risk correctly blocks release | 3 |
| Sponsorship disclosure repair is clear and conspicuous | 2 |
| Safe-zone/caption repair uses current placement previews | 2 |
| Opening/structure repair is useful and not folklore | 2 |
| Platform-specific deliverables and caption/accessibility package | 2 |
| Audio reasoning goes beyond integrated loudness | 2 |
| Technical inspection, test upload, archive, and analytics plan | 3 |

**Critical failures:** approves the cloned celebrity endorsement because it is labeled; approves music because it is credited; declares captions safe from the coordinate alone; declares audio done because it is -14 LUFS; skips the processed-platform preview.

## Evaluator notes on answer quality

Reward answers that:

- make the first action match the highest risk;
- distinguish an organic post from an ad, boost, Spark ad, or immersive-feed eligibility;
- retain source context and identify illustration versus evidence;
- produce a timecoded plan with viewer questions and exit conditions;
- define a current platform contract and record verification dates;
- use measured retention to generate hypotheses and controlled tests;
- connect metrics to the stated objective;
- admit when no universal threshold or specification exists;
- keep examples and heuristics adaptable rather than formulaic.

Penalize answers that:

- use generic “make it engaging” language without executable decisions;
- optimize only for completion or views when the objective is saves, leads, learning, or conversion;
- add unrelated kinetic footage or cuts as a default retention tactic;
- treat open captions as a complete accessibility strategy without proofreading, placement, or source files;
- bury volatile requirements without dates or official-source checks;
- give legal conclusions instead of flagging rights/disclosure issues and obtaining appropriate review;
- optimize cosmetics before integrity, rights, access, or delivery failures.
