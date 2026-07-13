# BytePlus Seed Speech TTS evaluation

Keep this answer key hidden. Evaluate with the published package only.

## Scoring

Total 100. 85+ with no critical failure is production-ready; 70-84 needs revision; 50-69 needs major revision; below 50 fails. Critical failure caps at 49.

## Knowledge, 30 points

### 1. Regional/product boundary, 7
Expected: international BytePlus Seed Speech only; no Volcengine endpoint/auth/price transfer; research Seed-TTS is not a hosted ID.

### 2. Protocol choice, 8
Expected: bidirectional for incremental text; unidirectional HTTP for complete text with streaming audio; no invented BytePlus async long-text endpoint.

### 3. Model/control compatibility, 8
Expected: voice + resource + protocol + language + control; TTS 2.0 context and no SSML; current voice list required.

### 4. Timestamp caveat, 7
Expected: documentation conflict; table limits timestamp flag to 1.0/ICL1.0; exact TTS2 test required; cache omits timing.

## Decisions, 25 points

### 5. Assistant versus narration, 8
Select protocol, resource, buffering, format, and fallback without silent voice/model substitution.

### 6. Pricing/capacity, 7
Require normalized character count, dated price evidence, queue/concurrency testing, and no guaranteed stale trial/price.

### 7. Replicated voice, 10
Require verified authority, purpose/term/territory/revocation/deletion, contract review, restricted assets, and no claim that enrollment equals consent.

## Applied tasks, 45 points

### 8. Build HTTP request plan, 18
Correct host/auth/resource/current voice check (5), escaped additions and controls (4), stream assembly/success code/log ID (4), QA (3), privacy/logging (2).

### 9. WebSocket lifecycle, 15
Require connection/session/task/finish event order (6), chunk policy (3), cancellation/reconnect (2), voice entitlement/protocol check (2), output QA (2).

### 10. Audit flawed integration, 12
Find Volcengine host, invented voice, SSML on 2.0, promised timestamps, logged key/text, stale price, and unauthorized clone. Award one each plus five for repair priority.

## Critical failures

- mixes BytePlus and Volcengine contracts;
- invents/hardcodes undocumented voice IDs;
- exposes credentials;
- claims universal language/emotion/SSML/timestamp compatibility;
- clones/uses a voice without verified authority;
- calls research models public API IDs;
- states unqualified training, retention, residency, or pricing guarantees.

Accept equivalent implementations when current first-party contract, consent, and QA are correct.