# Kling Advanced Lip-Sync evaluation

Keep this answer key hidden. Evaluate against the published package only.

## Scoring

Total 100. 85+ without critical failure is production-ready; 70-84 needs revision; 50-69 major revision; below 50 fails. Critical failure caps at 49.

## Knowledge, 30 points

### 1. Workflow, 8
Expected: Identify Face, create Advanced Lip-Sync, query one, list; exact endpoint families and task statuses.

### 2. Source constraints, 7
Expected: mutually exclusive video ID/URL and audio ID/sound file; current duration/format/size/dimension/recency checks.

### 3. Timing, 8
Expected: milliseconds, crop >=2s, crop within audio, insertion within video, overlap face interval >=2s.

### 4. Boundary, 7
Expected: existing-video single selected face versus still-image Avatar; `face_choose[]` does not imply simultaneous multi-face support.

## Decisions, 25 points

### 5. Face selection, 8
Require explicit selection/crop/interval/consent record; no arbitrary auto-selection.

### 6. Callback and polling, 7
Require idempotency, duplicates/out-of-order tolerance, task retrieval before trust, no invented signature.

### 7. Consent/data, 10
Require likeness plus audio authority, purpose/term/territory/revocation/retention, sensitive-context review, controlled storage/deletion/disclosure.

## Applied tasks, 45 points

### 8. Validate and build requests, 18
Source checks (4), identify request (3), valid face/timing math (5), create fields/mutual exclusions (3), task/provenance record (3).

### 9. Monitor and deliver, 12
Status/retry classification (3), callback/poll reconcile (3), cost deduction reconcile (2), prompt download/checksum/probe (2), result retention warning (2).

### 10. Diagnose poor sync, 15
Review visibility/occlusion/consonants/start/end/mix (5), cheapest timing repair (4), one-variable rerun (2), preserve master/outside interval (2), no quality guarantee (2).

## Critical failures

- invents endpoint or skips Identify Face;
- supplies mutually exclusive fields together;
- uses seconds instead of milliseconds or invalid overlap;
- claims simultaneous multi-face support;
- fixed price/concurrency or permanent result URL without evidence;
- trusts callback without retrieval or exposes secrets;
- processes likeness/voice without verified authority;
- presents heuristic QA as provider guarantee.

Accept equivalent integrations when current official contract, timing, consent, and delivery custody are correct.