# Video description oversight evaluation

Keep this file hidden. Evaluate against the published package only.

## Scoring

Total 100. A score of 85+ without critical failure is production-ready; 70-84 needs focused revision; 50-69 needs major revision; below 50 fails. Critical failure caps at 49.

## Knowledge, 30 points

### 1. Workflow, 7
Expected: source/spec/pre-caption, evidence critique, post-caption revision, independent acceptance, versioned decision/triplet.

### 2. Critique dimensions, 9
Define precision, recall, and constructiveness correctly and explain why each can fail independently.

### 3. Aspect review, 8
Identify likely errors in Subject, Scene, Motion, Spatial, and Camera without duplicating the full description skill.

### 4. Boundaries, 6
Separate language oversight from media artifact QA, accessibility captions, shot direction, provider APIs, and model training.

## Decisions, 25 points

### 5. Triage, 8
Choose review, regenerate/rewrite, expert escalation, new source, or block for five realistic input conditions. Penalize critiquing without visual access.

### 6. Reviewer disagreement, 9
Expected: classify evidence/term/scope/spec conflict, replay interval, apply glossary, escalate, preserve appeal, update recurring ambiguity; no universal threshold invented.

### 7. Dataset reuse, 8
Require source/caption/reviewer rights, privacy minimization, datasheet, versions, limitations, and separate training permission.

## Applied tasks, 45 points

### 8. Write a critique, 20
Given a source observation and flawed caption, score evidence-backed findings (5), aspect/time localization (3), precision/no invented correction (4), complete coverage within scope (4), constructive repair language (4).

### 9. Acceptance review, 13
Check all findings addressed (3), no new hallucination/omission (3), objectivity/order/glossary (3), uncertainty and use fit (2), disposition/provenance (2).

### 10. Design oversight workflow, 12
Require roles/conflicts (2), gold calibration/second stage (3), appeals/escalation (2), severity policy (2), dashboard without metric gaming (1), privacy/retention (2).

## Critical failures

- critiques without reviewing the source video;
- invents corrections or omits consequential errors while claiming acceptance;
- non-constructive “wrong” feedback with no repair;
- overwrites pre-caption or loses version/provenance;
- accepts material privacy/safety/identity errors;
- assumes C2PA or reviewer agreement proves truth;
- claims CHAI's expert results generalize universally or turns dataset triplets into training data without rights.

Accept equivalent workflows when evidence, critique quality, review independence, provenance, and limitations are sound.