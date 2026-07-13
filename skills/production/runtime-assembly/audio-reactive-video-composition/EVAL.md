# Audio-reactive video composition evaluation

Keep this answer key hidden. Evaluate with the published package only.

## Scoring

Total 100. A score of 85+ with no critical failure is production-ready; 70-84 needs focused revision; 50-69 needs major revision; below 50 fails. Any critical failure caps the score at 49.

## Knowledge, 30 points

### 1. Feature meanings, 10
Explain beat, onset, tempo, local pulse, structural boundary, RMS, loudness, spectral centroid, silence, and pYIN voicing. Full credit requires rejecting semantic overclaims.

### 2. Confidence, 7
Expected: analyzer-specific semantics; librosa beat tracking has no calibrated confidence; unavailable/zero values cannot be invented; confidence is not universal probability.

### 3. Timing, 7
Expected: source samples/time origin, rational FPS, declared rounding, original cue time plus mapped frame, and PTS verification.

### 4. Rights, 6
Expected: distinguish recording, composition, lyric, synchronization, adaptation, and distribution rights; no clearance by possession.

## Decisions, 30 points

### 5. Routing, 10
Route a stable dance track, tempo-changing performance, ambient track, and spoken word. Penalize extending unreliable beats.

### 6. Mapping, 10
Require bounded, normalized, smoothed mappings with one role per feature and neutral fallback. Disqualify “centroid = happiness” or elastic quantitative overstatement.

### 7. Variants and safety, 10
Preserve cue timing across aspects, protect lyrics/captions, provide lower-motion behavior, and independently test flashing.

## Applied tasks, 40 points

### 8. Build a production plan, 24
Given an analysis report, produce source contract (4), candidates versus anchors (4), routing rationale (4), mapping table (4), rational timing policy (4), and QA/provenance (4).

### 9. Audit a flawed plan, 16
Find and repair: every onset becomes a cut; beat confidence is fabricated; clusters are called choruses; 29.97 is a float with no policy; aspect variants drift; captions/flashing omitted; one music license is assumed to clear all rights. Award two points per issue plus two for coherent prioritization.

## Critical failures

- fabricating confidence or semantic labels;
- applying a beat grid after reliability fails;
- treating all onsets as cuts;
- nondeterministic or undeclared timing;
- aspect variants use different cue times;
- unsafe flashing or missing required captions;
- assuming one audio file/license clears all underlying rights.

Accept equivalent tools and schemas when evidence, timing, safety, and reproducibility are sound.