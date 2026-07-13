# Screen demo production evaluation

Keep this answer key hidden. Evaluate with the published package only.

## Scoring

Total 100. 85+ with no critical failure is production-ready; 70-84 needs focused revision; 50-69 needs major revision; below 50 fails. Any critical failure caps at 49.

## Knowledge, 25 points

### 1. Truth classification, 8
Distinguish authentic, controlled authentic, illustrative synthetic, and hybrid, including disclosure and claim limits.

### 2. Automation readiness, 7
Expected: actionability is not business readiness; avoid fixed sleeps/networkidle; assert observable product state; context does not reset server data.

### 3. Artifact sensitivity, 5
Expected: video, traces, HAR, logs, auth state, screenshots, captions, metadata each need separate review.

### 4. Accessibility, 5
Expected: captions, visual description/audio-only understanding, contrast, final-size readability, flashing.

## Decisions, 25 points

### 5. Capture mode, 10
Choose and justify modes for confidential CLI tutorial, real IDE behavior, flaky authenticated web flow, and conceptual cross-app explanation.

### 6. Reset and nondeterminism, 8
Require disposable/seeded state, fixed environment, mocks/disclosure, retries/branches, repeated rehearsal.

### 7. Variants, 7
Reject blind center crop; preserve navigation, target, result, captions, and readable scale through alternate compositions/recapture.

## Applied tasks, 50 points

### 8. Mixed terminal/IDE plan, 20
Require contract/truth class (3), reset (3), beat ledger with readiness (4), narration/cursor/callout (4), privacy (3), variants/QA/provenance (3).

### 9. Repair brittle Playwright plan, 18
Find fixed sleeps, networkidle, live customer data, committed auth, implicit video scaling, undisclosed HAR/mock, no persisted-result assertion, and no context close. Award two each plus two for sequencing.

### 10. Final artifact audit, 12
Assess claim truth, state continuity, readability, secrets/PII across artifacts, captions, crop safety, mocks, provenance, and output specs.

## Critical failures

- exposes credentials or real PII;
- presents synthetic/mocked behavior as authentic;
- no reset/reproducibility strategy;
- relies primarily on sleeps or hides contradictory failure by editing;
- unreadable final-size UI or missing required captions;
- claims provenance proves factual truth.

Accept equivalent capture tools when truth, reset, privacy, direction, accessibility, and QA are sound.