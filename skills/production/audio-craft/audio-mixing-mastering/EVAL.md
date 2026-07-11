# Evaluation: audio-mixing-mastering

Use this file as the answer key and scoring guide for evaluating an agent that had access to `SKILL.md` only. Do not expose this file to the evaluated agent.

Score out of 100. Passing requires at least 75 overall, no critical failure, and at least 60% in each section.

Critical failures:

- Invents a universal loudness target and presents it as mandatory for all platforms.
- Ignores a provided client/broadcaster/platform spec.
- Confuses peak/sample peak with true peak or treats normalization as a substitute for mixing.
- Recommends heavy limiting or clipping as the main fix for intelligibility or platform loudness.
- Fails to protect dialogue intelligibility in speech-first content.
- Advises destructive overwrite of original sources or cannot preserve stems/source reversibility.
- Claims YouTube has an official public loudness target based only on the cited upload-encoding help page.
- Leaks, references, or asks to read this answer key during evaluation.

## Section 1: documented facts and standards (20 points)

Question 1: What measurement standard underlies most loudness and true-peak guidance in the skill?

Expected answer: ITU-R BS.1770-5 provides loudness and true-peak measurement algorithms; EBU R128, ATSC A/85, Apple Podcasts, and other specs refer to BS.1770-style measurement in different ways.

Required points:

- Names ITU-R BS.1770 or BS.1770-5.
- Mentions loudness and true peak, not just "volume."
- Understands it is a measurement algorithm/foundation, not a creative mixing preset.

Question 2: Give correct targets for EBU R128, ATSC A/85, Apple Podcasts, Spotify music, and Netflix branded content.

Expected answer:

- EBU R128: -23 LUFS, max -1 dBTP; current R 128 v5.0 allows +/-1 LU where target cannot practically be achieved and +/-0.2 LU for QC measurement error.
- ATSC A/85 default without metadata: -24 LKFS, max -2 dBTP; streaming services may use -23 to -27 LKFS unless arranged otherwise.
- Apple Podcasts: about -16 dB LKFS +/-1, true peak not above -1 dB FS/true peak.
- Spotify: -14 dB integrated LUFS, below -1 dBTP; if louder than -14 LUFS, below -2 dBTP.
- Netflix branded: -27 LKFS +/-2 LU dialog-gated, true peak not exceeding -2 dBTP, with 48 kHz/24-bit for original language/M&E masters.

Award partial credit for small terminology variants such as LUFS/LKFS equivalence where appropriate. Penalize if the answer treats these as interchangeable deliverables.

Question 3: What does the skill say about YouTube loudness?

Expected answer: The official YouTube upload encoding page verified in the skill lists audio bitrate recommendations but does not state an official public loudness target. For YouTube/social work without a formal spec, the skill allows a labeled heuristic such as -16 to -14 LUFS with safe true peak, but it must not be presented as an official YouTube rule.

Question 4: What accessibility guidance applies to background audio under speech?

Expected answer: For prerecorded speech, WCAG guidance says background sounds should be at least 20 dB lower than foreground speech, except brief sounds; the agent should use this especially for instructional/speech-critical content or provide another way to lower/disable background sound.

## Section 2: production decision-making (25 points)

Scenario 1: A client asks for one master for YouTube, Instagram, podcast RSS, and possible US broadcast later. What should the agent do?

Strong answer:

- Asks for or prioritizes explicit specs and separates masters when specs conflict.
- For podcast RSS, considers Apple Podcasts around -16 LKFS +/-1 and <= -1 dB true peak.
- For social/video, uses a labeled heuristic such as -16 to -14 LUFS and -1 to -2 dBTP if no platform spec is supplied.
- Does not make the broadcast master until the buyer/spec is known; if ATSC no-metadata delivery is requested, uses -24 LKFS and -2 dBTP.
- Recommends retaining stems to make broadcast reversion possible.

Penalize:

- Uses the loudest target for all.
- Says YouTube/Instagram require -14 LUFS as an official universal spec.
- Normalizes one file and calls every destination done.

Scenario 2: In a 45-second explainer, generated music masks the AI narration. The master is already at target loudness. What should the agent recommend?

Strong answer:

- Fix balance before mastering: lower/duck music, carve masking frequencies, remove busy arrangement elements, automate under key phrases, reduce SFX.
- Clip-gain/process narration for clarity if needed.
- Avoid pushing master louder or adding more limiting.
- Check intelligibility on small speakers/earbuds and consider WCAG separation for instructional parts.

Scenario 3: A trailer mix feels smaller after mastering, even though loudness increased. What diagnosis is expected?

Strong answer:

- Over-limiting may be flattening transients and contrast.
- Impacts/music/SFX may be hitting the limiter too hard.
- Preserve short-term dynamics, reduce density, automate impacts, control low end before the limiter, and use a safer true-peak ceiling.
- Loudness normalization may remove any playback gain advantage, leaving distortion/fatigue.

Scenario 4: A localization team needs a dubbed version next week. What deliverables should the agent prepare now?

Strong answer:

- Full mix, dialogue/VO stem, music stem, effects stem, M&E, possibly clean VO/narration, and time-aligned high-quality archive masters.
- Stems must start at same timecode, share sample rate/channel layout/duration, and either sum to full mix or document bus-processing differences.
- Preserve room tone/ambience and avoid baking original language dialogue into M&E.

## Section 3: applied production tasks (35 points)

Task 1: Produce a mix plan for a 60-second vertical social ad with AI VO, generated music, UI clicks, and a logo sting. No formal spec supplied. (12 points)

Expected characteristics:

- States hierarchy: VO/CTA first, music support, SFX punctuation.
- Chooses a labeled social/web heuristic target around -16 to -14 LUFS and -1 to -2 dBTP, not as a platform rule.
- Includes session prep, source preservation, grouping, sync checks, and artifact marking.
- Describes VO cleanup, clip gain, mild EQ/compression/de-essing.
- Uses music ducking/automation and SFX level control.
- Includes phone/earbud/laptop checks, mono/fold-down check, final encode re-check, and QA notes.
- Mentions stems if client revision/reversioning is likely.

Task 2: Review this flawed recommendation: "Normalize everything to -14 LUFS, set the limiter to 0 dB, and if the voice is hard to hear, increase the master by 3 dB." (8 points)

Expected critique:

- -14 LUFS is not universal.
- 0 dB limiter/sample ceiling is unsafe for true peaks and lossy encoding.
- Raising master does not fix voice/music masking.
- Should lower/duck/carve music, improve VO clarity, set appropriate true-peak ceiling, and remeasure.
- Should use client/destination spec.

Task 3: Troubleshoot a podcast recut where one speaker is noisy and quiet, the other is bright and loud, and the intro music startles listeners. (8 points)

Expected approach:

- Level each speaker with clip gain before compression.
- Conservative denoise/repair, avoid watery artifacts.
- Tailored EQ/de-ess per speaker.
- Compression in stages for consistency.
- Reduce/automate intro music and check loudness transition.
- Target podcast spec if applicable, e.g. Apple Podcasts -16 LKFS +/-1 and <= -1 true peak.
- Listen on earbuds; check mouth clicks, fatigue, and speech consistency.

Task 4: Create final QA checklist for a mixed documentary short. (7 points)

Expected checklist:

- Integrated loudness, true peak, LRA/short-term if needed; measurement standard/tool/mode.
- Export format/sample rate/bit depth/codec/channel layout/bitrate/container.
- Sync at start/middle/end.
- Full listening pass and device checks.
- Intelligibility, noise/artifact, clicks/pops/plosives/clipping, room-tone gaps.
- Mono fold-down/stereo width or surround downmix checks.
- Stem validation and known limitations.

## Section 4: source/evidence hygiene (10 points)

Expected behavior:

- Separates documented facts, empirical observations, and heuristics.
- Dates volatile platform/spec claims when discussed.
- Uses authoritative sources for standards/platform claims.
- Avoids unsupported "best" claims and marketing language.
- Notes when a target is a working heuristic due to absent official platform spec.

Full credit requires all five. Deduct for mixing facts and heuristics without labels, relying on forum claims for consequential specs, or failing to date platform details.

## Section 5: craft nuance and judgment (10 points)

Strong answers demonstrate:

- Balance and source repair before bus processing.
- Speech intelligibility as a core deliverable and accessibility issue.
- Proper stem planning and bus-processing awareness.
- Sensible handling of AI-generated voice/music/SFX artifacts.
- Understanding of stereo/mono compatibility and immersive/downmix implications.
- Awareness that codec/transcode checks happen after export, not only in the DAW/session.

Award up to 10 points for practical, production-ready reasoning. Deduct for rigid recipes, over-processing, ignoring monitoring context, or treating loudness meters as the only quality control.
