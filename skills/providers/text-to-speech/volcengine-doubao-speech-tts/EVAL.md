# Volcengine Doubao Speech TTS evaluation

Keep this answer key hidden. Evaluate against the published package only.

## Scoring

Total 100. 85+ without critical failure is production-ready; 70-84 needs revision; 50-69 needs major revision; below 50 fails. Critical failure caps at 49.

## Knowledge, 30 points

### 1. Regional boundary, 6
Expected: mainland Volcengine only; no BytePlus hosts/keys/prices/legal assumptions.

### 2. Protocols, 9
Expected: V3 bidirectional for incremental text, unidirectional for known text, async submit/query up to current long-text limit; V1 legacy TTS1 only.

### 3. Async lifecycle, 8
Expected: submit/task_id/query statuses 1/2/3, seven-day server retention, one-hour URL, concurrency shared, download promptly.

### 4. Compatibility, 7
Expected: speaker + resource + protocol + language + control + entitlement; no invented voice; TTS2 no SSML.

## Decisions, 25 points

### 5. Long form, 8
Require normalized source/hash, cost/concurrency approval, stable unique ID, polling/idempotency, prompt download, QA.

### 6. Timestamp subtitles, 7
Require exact voice/protocol test, normalization awareness, monotonic/duration validation, semantic grouping, fallback alignment.

### 7. Cloned voice, 10
Require explicit authority, use scope, retention/deletion resolution, protected assets, no deceptive/public-figure use, no technical-consent inference.

## Applied tasks, 45 points

### 8. Async request plan, 18
Correct endpoint/headers/resource/current speaker (5), unique ID/task lifecycle (5), expiry/download (3), timestamps/QA (3), logging/privacy (2).

### 9. Streaming assistant, 15
Correct protocol/voice preflight (4), event lifecycle/chunking (5), cancel/reconnect (2), concurrency/errors (2), QA (2).

### 10. Audit flawed integration, 12
Find BytePlus host, V1 with TTS2 voice, invented speaker, SSML on 2.0, blind async resubmit, permanent result URL, hardcoded price, unauthorized clone. Award one each plus four for repair sequence.

## Critical failures

- mixes regional contracts;
- sends TTS 2.0 voice through unsupported V1/resource;
- invents voice IDs or prices;
- exposes credentials;
- blindly duplicates async jobs;
- treats expiring URL as storage;
- claims universal timestamp/SSML/language/protocol support;
- uses cloned voice without verified authority or makes unverified privacy/residency claims.

Accept equivalent implementations when current first-party contract, idempotency, consent, and QA are correct.