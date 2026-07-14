---
name: video-description-oversight
description: Provider-independent governance workflow for verifying and correcting human- or model-generated video descriptions. Use for pre-caption critique and post-caption revision, aspect-by-aspect factual review, critique precision/recall/constructiveness, second-stage peer review, calibration, appeals, versioned triplets, provenance, and acceptance reporting; not for pixel/audio QA, accessibility captioning, model training, or creative shot direction.
---

# Video description oversight

Use this skill when language about a video must be accepted as evidence-quality metadata rather than plausible prose. It governs a correction loop:

```text
source video + specification + pre-caption
  -> evidence-backed critique
  -> revised post-caption
  -> independent acceptance review
  -> versioned triplet and decision record
```

The reviewer verifies what language says about media. Technical file integrity, visual artifact QA, accessibility captions, creative intent, and model post-training belong elsewhere.

## Evidence stance

- **Documented fact:** a finding supported by the source video, approved specification, or cited standard/research.
- **Reviewer observation:** a timestamped comparison between video and description.
- **Production heuristic:** an operational quality-control choice that must fit the project's risk and workforce.

The workflow is informed by Lin et al.'s CHAI framework, which reports that critiques used to revise precise video captions are most useful when accurate, complete, and constructive. Sources were verified **2026-07-14**. CHAI's performance numbers are first-party research results on its data and annotator program, not universal service-level guarantees.

## Activation and boundaries

Use this skill for descriptions used in:

- search, archive, edit logging, or reference analysis;
- training/evaluation datasets;
- generation-prompt handoff;
- cinematography-aware video understanding;
- regulated or high-risk metadata where language errors matter.

Route elsewhere for:

- codec, color, audio, anatomy, artifact, or final-media release QA;
- SDH/subtitle timing and accessibility compliance;
- deciding the desired shot or creative treatment;
- training/fine-tuning reward or caption models;
- provider-specific video analysis API calls;
- payroll, labor classification, or workforce procurement.

The workflow requires a description specification. If none exists, establish one through `precise-video-description` before grading completeness or terminology.

## Inputs and evidence package

Collect:

- immutable source asset/version, checksum, duration/timebase, rights and privacy classification;
- pre-caption text, author/model/version, prompt/instruction, timestamp, and provenance;
- approved description scope and five-aspect requirement: Subject, Scene, Motion, Spatial, Camera;
- project glossary/version, reference examples, uncertainty policy, and domain limitations;
- target use and severity policy;
- reviewer identity/pseudonymous ID, expertise, language, calibration status, and conflicts;
- prior critiques, revisions, appeals, and accepted version if any.

Do not let a reviewer critique video they cannot access. A text-only “blind critique” cannot establish visual accuracy.

## Triage the pre-caption

Before detailed review, decide:

- **reviewable:** coherent enough for correction;
- **requires domain expert:** specialized medicine, science, culture, language, or cinematography exceeds reviewer competence;
- **requires new source:** video is corrupted, too low quality, incomplete, or mismatched;
- **reject and regenerate/rewrite:** caption is irrelevant or so defective that itemized correction is less reliable than a new draft;
- **blocked:** rights, privacy, or specification is missing.

Record the reason. Do not force a critique workflow onto an unusable source/caption pair.

## Review by aspect and time

Use the project's precise-description contract rather than intuition.

### Subject

Check entity count, stable identifiers, visible attributes, pose, relationships, entry/exit, and unverified identity/demographic inference.

### Scene

Check setting, time/weather evidence, overlays versus physical objects, transitions, and unsupported mood/theme claims.

### Motion

Check action verbs, actors/targets, temporal order, simultaneous activity, contact, direction, and causal overstatement.

### Spatial

Check shot size, frame position, depth, overlap/occlusion, start/end framing, and subject-relative versus frame-relative direction.

### Camera

Check translation versus rotation, zoom versus movement, angle/height/roll, focus changes, steadiness, playback effects, edit transitions, and fabricated technical settings.

Review at normal speed and frame-level around disputed events. Each finding must include a locator or bounded interval where possible.

## Write a correctional critique

Every critique must pass three independent gates:

### Precision

Every finding is real and supported by visible evidence/specification. Do not add a plausible correction that the video does not establish.

### Recall

All consequential errors and omissions within the agreed scope are covered. Recall is not maximal verbosity; trivial details outside the contract can remain omitted.

### Constructiveness

Each finding says how to repair the caption: replace, add, delete, reorder, qualify, or mark uncertain. “This is wrong” is not a usable correction.

Recommended finding shape:

```json
{
  "aspect": "camera",
  "time_range": ["00:02.100", "00:04.800"],
  "error_type": "incorrect-term",
  "caption_claim": "the camera zooms in",
  "evidence": "foreground/background parallax increases while field of view appears stable",
  "correction": "replace with 'the camera moves forward'",
  "severity": "major",
  "reviewer_id": "reviewer-17",
  "spec_version": "video-language-2.1"
}
```

This is an example schema. It must not contain invented confidence scores. Separate observed evidence from the proposed wording.

## Handle accurate captions

Do not invent feedback to prove that review occurred. If no corrections are required, record an explicit sentinel such as:

```text
The description matches the reviewed source and specification; no edits are required.
```

An “accurate” decision still needs review scope, asset/version, reviewer, date, glossary/specification version, and any unreviewed lanes.

## Produce and verify the post-caption

The author/model revises from the accepted critique. Preserve all versions; never overwrite the pre-caption.

Second-stage acceptance asks:

1. Were all valid critique findings addressed?
2. Did revision introduce new hallucinations, omissions, ambiguity, or writing problems?
3. Does it remain objective and temporally ordered?
4. Does terminology match the approved glossary?
5. Are uncertainty and intentionally omitted aspects preserved?
6. Does the post-caption suit its declared use and privacy/rights scope?

The accepting reviewer should be different from the first reviewer for high-risk or dataset use. Lower-risk internal work may use calibrated spot review according to a documented policy.

## Severity and disposition

Define severity from downstream consequence, not word count:

- **Critical:** false identity, safety/regulatory claim, privacy leak, materially deceptive event, unusable dataset target, or unsupported statement that could cause harm.
- **Major:** wrong subject/action/camera/spatial relation, consequential omission, temporal inversion, or terminology that changes meaning.
- **Minor:** localized wording or non-consequential omission within scope.
- **Observation:** non-blocking note or limitation.

Possible dispositions: `accepted`, `accepted_with_limitations`, `revise`, `reject`, `escalate`, `blocked`.

Do not mechanically waive privacy, consent, safety, or material factual errors.

## Peer review, appeals, and calibration

Use gold examples and periodic blind calibration. Track agreement by aspect because a team may agree on Subject/Scene while failing on Spatial/Camera.

When reviewers disagree:

1. identify whether the conflict is evidence, terminology, scope, or specification ambiguity;
2. replay the disputed interval and apply the glossary decision rule;
3. escalate to an appropriate senior/domain reviewer if unresolved;
4. record the decision and update training material/specification if the ambiguity will recur;
5. allow a documented appeal without erasing the original review.

Do not impose a universal kappa threshold, daily review quota, compensation scheme, or expertise ladder. CHAI used a highly trained professional pipeline; teams with different content or reviewers must establish their own validated calibration criteria.

## Versioned outputs and provenance

Preserve:

- source asset ID/hash/version;
- specification/glossary version;
- pre-caption, critique findings, post-caption;
- author/model/prompt/version and reviewer IDs;
- timestamps, iteration number, status, acceptance/appeal decisions;
- domain, language, intended use, rights/privacy restrictions;
- known unreviewed aspects and residual risks.

The `(pre-caption, critique, post-caption)` triplet can become a valuable dataset asset, but production permission does not automatically grant model-training permission. Create a datasheet and confirm source-video, caption, reviewer, and derivative-data rights before reuse.

C2PA or signed records can support provenance; they do not prove that a caption is true.

## Privacy, workforce, and domain limitations

Detailed video descriptions may expose identity, location, private behavior, screens, health/financial details, or copyrighted story content. Minimize access, use pseudonymous reviewer IDs, define retention/deletion, separate public output from private review metadata, and audit exports.

Match reviewers to domain/language complexity. Cinematography expertise does not imply medical or cultural expertise; language fluency does not guarantee camera-motion discrimination. CHAI's findings came from trained professional creators and predominantly professional video domains. Do not assume equivalent results from untrained crowdworkers, multilingual auto-translation, long-form footage, or specialized domains.

## Quality dashboard

Track trends rather than optimizing one number:

- corrections and severity by aspect;
- false-positive critique rate;
- omissions found at second-stage review;
- revision iterations and rejection reasons;
- appeal rate and root cause;
- agreement/calibration by aspect and domain;
- source model/author defect patterns;
- specification ambiguities and glossary changes;
- review time and fatigue indicators without intrusive surveillance.

High critique volume can indicate either poor sources or overcritical reviewers. Audit evidence before drawing conclusions.

## Example 1: camera-term correction

This is a complete example, not a mandatory formula.

**Source:** six-second kitchen shot. **Pre-caption claim:** “The camera zooms in on the woman as she glances to the right.”

**Evidence review:** background/foreground parallax changes, supporting forward camera translation; the woman looks toward frame-right, but whether that is her left/right is not needed. Focus remains on her eye.

**Critique:** “Camera, 00:02.0-00:05.0: replace ‘zooms in’ with ‘moves forward’ because the viewpoint translates and parallax changes rather than only the field of view. Spatial/Motion: keep ‘looks toward frame-right’; do not convert it to the subject's right without evidence. The remaining subject and scene description is accurate.”

**Post-caption:** “In a dim kitchen, the camera moves smoothly forward toward a woman as she raises her gaze toward frame-right; focus remains on her near eye.”

**Acceptance:** second reviewer confirms correction, no new claims, and records the exact source/spec versions.

**Failure to avoid:** “The caption is wrong about camera motion.” It lacks the supported replacement and is non-constructive.

## Example 2: incomplete generated game description

This is a complete example, not a mandatory formula.

**Pre-caption:** “A knight runs through a level while the camera follows.”

**Reviewed scope:** all five aspects for dataset metadata.

**Findings:**

- Subject: “knight” overstates identity; visible evidence supports “small armored character.”
- Scene: missing elevated platforms and score overlay.
- Motion: add frame-right travel and stop before the cut.
- Spatial: add side view, left-third hold, and platforms moving frame-left; world/camera displacement remains uncertain.
- Camera: “follows” is plausible from stable framing but should be qualified as “consistent with lateral tracking”; add final hard cut to a closer view.

**Constructive critique:** provides each replacement/addition and preserves uncertainty. **Post-caption:** incorporates all five without claiming world speed or exact lens. **Disposition:** accepted after second review.

**Failure to avoid:** adding speculative game title, character name, player intent, or “dynamic exciting atmosphere.”

## Sources

Verified 2026-07-14:

- Lin et al., “Building a Precise Video Language with Human-AI Oversight,” CVPR 2026 / arXiv:2604.21718: https://arxiv.org/abs/2604.21718
- Official CHAI project, code, test data, and model card: https://linzhiqiu.github.io/papers/chai/ , https://github.com/chancharikmitra/CHAI , https://huggingface.co/datasets/chancharikm/CHAI_testset , and https://huggingface.co/chancharikm/CHAI_SFT_model_8b
- Saunders et al., “Self-critiquing models for assisting human evaluators”: https://arxiv.org/abs/2206.05802
- Gebru et al., Datasheets for Datasets: https://doi.org/10.1145/3458723
- C2PA specification index: https://spec.c2pa.org/