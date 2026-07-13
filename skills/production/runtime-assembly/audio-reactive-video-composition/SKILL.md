---
name: audio-reactive-video-composition
description: Provider-independent production guidance for translating measured audio features into deterministic video timing and motion. Use for beat-, onset-, phrase-, energy-, silence-, or spectrum-reactive visualizers, edits, typography, and generated compositions; not for music-video concept direction, audio generation, or a runtime-specific recipe.
---

# Audio-reactive video composition

Use this skill to turn an approved audio source into an auditable cue map and then into bounded visual behavior. The central contract is:

$$
\text{source audio} \rightarrow \text{measured features} \rightarrow
\text{confidence-bearing cues} \rightarrow \text{reviewed anchors} \rightarrow
\text{deterministic visual timeline}
$$

Do not equate a detector output with editorial meaning. An onset is not automatically a beat, cut, drop, or lyric accent; an acoustic cluster is not automatically a verse or chorus.

## Evidence stance

- **Documented fact:** behavior stated by official analysis libraries, standards, or cited research.
- **Production heuristic:** a practical mapping that must be tested on the track and audience.
- **Empirical observation:** a measured result from the supplied audio, analyzer run, render, or playback.

Analysis algorithms, defaults, and model behavior are volatile. Facts were verified **2026-07-12**. Pin the decoder, library, model, parameters, and random seeds used for each production.

## Scope

This skill owns source custody, analysis policy, confidence interpretation, rhythmic/non-rhythmic routing, cue promotion, feature-to-visual mappings, rational frame alignment, accessibility, and render QA.

It does not own music-video narrative or artist branding, music generation, mastering, source separation, transcription, lyric writing, or a HyperFrames/Remotion/FFmpeg-specific implementation.

## Freeze the audio contract

Record before analysis:

- source path/URI, SHA-256, acquisition source, rights basis, and restrictions;
- selected stream, codec, native sample rate, channels/layout, start timestamp, and duration;
- decoder/resampler and versions;
- canonical PCM format, channel/downmix policy, analysis sample rate, window/hop sizes, centering, and padding;
- analyzer/library/model versions, priors, thresholds, and seeds;
- trim offsets and source time origin;
- master output frame rate as a rational number;
- transcript/lyrics source, language, timing provenance, review status, and separate rights basis.

Use sample indices as the primary analysis clock where possible. Derived seconds should not replace exact source positions.

## Interpret features conservatively

**Documented facts:**

- `librosa.beat.beat_track` estimates tempo from onset strength and selects beat positions consistent with it; it does not return calibrated beat confidence.
- `librosa.onset.onset_detect` peak-picks an onset-strength envelope. Onsets estimate event attacks, not semantic accents.
- Predominant local pulse can model changing tempo, but remains an estimate.
- Essentia confidence values are algorithm-specific; they are not universal probabilities, and some routes return an unusable zero confidence.
- Beat evaluation commonly accounts for half/double-tempo metrical ambiguity and uses tolerances rather than exact equality.
- Structural boundaries and structural labels are separate tasks. Cluster labels such as A/B/C do not establish verse/chorus meaning.
- RMS is an energy measure. EBU R128 loudness uses defined weighting and windows. Neither is a direct emotion score.
- Spectral centroid, bandwidth, and contrast describe spectrum distribution; they do not mean happiness, tension, or quality.
- Silence detection is relative to a declared reference and threshold.
- pYIN voicing means pitch periodicity, not proof that a person is speaking or singing.

Keep raw candidates distinct from human-promoted anchors.

## Cue-map contract

Each cue should include:

```json
{
  "id": "accent-014",
  "type": "onset",
  "time_samples": 417312,
  "time_seconds": 9.46399,
  "value": 0.82,
  "units": "normalized-onset-strength",
  "analyzer": "record exact library and algorithm",
  "confidence": null,
  "confidence_semantics": "not supplied by analyzer",
  "profile_hash": "sha256:...",
  "status": "promoted-anchor",
  "editorial_role": "single visual accent",
  "reason": "reviewed strong transient before section change"
}
```

For interval features, include exact end samples/times. Record rejected candidates rather than deleting evidence. Keep acoustic section names neutral until lyrics, metadata, or human review supports functional labels.

## Choose a routing mode

### Rhythmic

Use when the selected tracker has useful evidence, local tempo is stable enough, and beat/onset results agree. Periodic motion may follow beats; selected strong accents or reviewed section changes may motivate cuts.

### Mixed confidence

Use reliable rhythmic windows locally. Elsewhere shift to onsets, transcript phrases, energy, silence, or manual anchors. Never extrapolate a grid through a failed interval.

### Non-rhythmic

Use reviewed speech/lyric phrases, silence, energy contour, spectral change, and manually confirmed macro anchors. This suits rubato, ambient work, spoken word, sparse recordings, and free improvisation.

## Map features to visual behavior

Production heuristics:

- Give each feature a limited visual responsibility.
- Normalize continuous values with robust per-track or per-section statistics, not one extreme maximum.
- Smooth noise and use hysteresis before switching visual states.
- Clamp every parameter and define neutral behavior for missing/invalid values.
- Use macro section anchors, medium phrase anchors, and sparse accents rather than cutting on every event.
- Reserve low-energy or silent spans for holds, reading, resets, and visual breathing room.
- Protect lyric lines and important vocal phrases from competing cuts and overlays.
- Preserve one cue map across aspect ratios; recompose layout, not timing.

Avoid quantitative-looking mappings that imply false measurement. If energy maps to scale, define the exact bounded range and do not call it emotion.

## Deterministic frame timing

Keep exact rates such as $30000/1001$ rational. For each cue, define a rounding policy. A conservative visual-response policy assigns the cue to the first output frame whose presentation time is at or after the audio event:

$$
f = \left\lceil t_{event} \cdot \frac{fps_{num}}{fps_{den}} \right\rceil
$$

Record both the original event time and mapped frame. Verify actual frame presentation timestamps after encoding because an encoder may duplicate or drop frames to satisfy constant-frame-rate output.

The visual state at frame $f$ must derive from cue data and frame time, not wall-clock playback. Seed procedural mappings and freeze analyzer output before distributed rendering.

## Lyrics, vocals, and captions

Treat transcript or lyric timing as a separate evidence stream. Do not use pitch voicing as vocal detection. Human-review names, lyrics, line boundaries, and timing before they control typography.

Prerecorded synchronized media with meaningful speech needs accurate captions. Captions should include meaningful non-speech sound where needed. A stylized lyric layer does not automatically replace accessible captions or transcript.

## Safety, rights, and provenance

WCAG 2.2 SC 2.3.1 limits flashing above three times in one second unless below general/red-flash thresholds. Test loops while looping and at the largest intended scale. Reduced motion does not make unsafe flashing safe.

Provide a lower-motion version when large displacement, zoom, shake, or dense event response may cause discomfort. Reduce event density and travel, not merely output FPS.

The musical work, lyrics, and sound recording can carry separate rights. Possession of a file does not grant synchronization, adaptation, or distribution rights. Record source and transformation provenance; do not claim metadata proves authenticity or permission.

## QA

1. Re-run identical input/configuration and compare canonical cue-map hashes.
2. Audition click-marked candidate and promoted anchors.
3. Inspect tempo-level ambiguity and failed-confidence windows.
4. Compare source timing against decoded/trimmed master and non-zero timestamps.
5. Inspect frames immediately before, on, and after every macro anchor.
6. Verify aspect variants share cue IDs and frame assignments.
7. Probe output frame PTS, duration, and audio sync.
8. Review captions/lyrics, reduced motion, and flash safety.
9. Preserve source hash, profile, cue map, mapping table, render versions, and approvals.

## Example 1: constant-tempo electronic visualizer

This is a complete example, not a mandatory formula.

**Intent:** 30-second 9:16 and 16:9 visualizer from an authorized 44.1 kHz stereo instrumental at 30 fps.

**Approach:** confirm stable tempo with a documented analyzer and inspect local pulse. Retain all beat/onset candidates. Promote every fourth beat for medium choreography, reviewed top-strength transients for sparse accents, and reviewed recurrence changes for macro transitions. Beat phase drives scale only from 1.000 to 1.035; low-band energy controls bounded depth; centroid controls a narrow texture-density range. A six-beat low-energy span holds title copy.

Map all anchors to the first frame at or after their sample time. Both aspect variants use identical cue IDs. QA click tracks, rerun hashes, PTS, duration, final-size text, and full-screen flashing.

**Likely failure:** half/double-tempo ambiguity. Repair by documenting the metrical level selected for visual periodicity without rewriting the raw detections.

## Example 2: rubato spoken word

This is a complete example, not a mandatory formula.

**Intent:** 75-second poem with ambient bed at 24 fps.

**Approach:** global beat trackers disagree, so use the non-rhythmic route. Reviewed transcript line starts/ends are primary anchors; pauses reset the field; sustained loudness rises control subtle expansion; acoustic-change candidates remain review prompts. Each stanza establishes a stable visual field, and punctuation settles motion. No beat cuts or word-by-word scaling.

The vertical variant reflows text but retains timing. QA muted-caption comprehension, audio-only clarity, every line boundary, breath-adjacent silence, reduced motion, flashing, and separate text/recording rights.

**Likely failure:** an acoustic boundary lands inside a sentence. Keep it as a low-confidence event and reject it as an editorial anchor.

## Sources

Verified 2026-07-12:

- librosa beat, onset, PLP, tempo, segmentation, RMS, spectral, split, and pYIN documentation: https://librosa.org/doc/latest/
- Essentia rhythm and loudness references: https://essentia.upf.edu/reference/
- `mir_eval` beat, onset, and segment metrics: https://mir-eval.readthedocs.io/
- Ellis, Dynamic Programming Beat Tracking: https://www.ee.columbia.edu/~dpwe/pubs/Ellis07-beattrack.pdf
- FFmpeg and ffprobe documentation: https://ffmpeg.org/documentation.html
- EBU R 128: https://tech.ebu.ch/publications/r128
- WCAG flashing and captions: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html and https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
- U.S. Copyright Office guidance for musicians: https://www.copyright.gov/engage/musicians/