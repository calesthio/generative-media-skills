---
name: audio-mixing-mastering
description: Provider-independent audio mixing and mastering direction for AI agents finishing generated videos, ads, trailers, explainers, podcasts, recuts, avatar clips, music videos, documentaries, and social content. Use when planning, mixing, repairing, mastering, QCing, or delivering dialogue, music, ambience, and sound effects, including loudness/true-peak targets, intelligibility, accessibility, stems, stereo/immersive decisions, platform/client specs, and final audio QA.
---

# Audio Mixing and Mastering Direction

Use this skill when audio must survive real playback: phone speakers, earbuds, laptops, TV soundbars, cinema-style trailers, podcasts, client review links, broadcast deliveries, and social feeds. Treat the mix as a production decision, not as a last-minute normalization step.

The job is to make the audience understand the foreground, feel the intended energy, avoid fatigue or distortion, and pass the declared delivery spec.

## Start with the audio contract

Before touching levels, write a short audio contract for the project:

- Delivery context: social post, YouTube upload, podcast RSS, streaming ad, broadcast, OTT, internal review, theatrical-style trailer, music video, documentary, localization, accessibility version.
- Foreground hierarchy: dialogue/VO first, performance/music first, sound-design impact first, or a changing hierarchy by scene.
- Required deliverables: full mix, dialogue stem, music stem, effects stem, M&E, narration-only, clean captions, audio-described version, alternate language mix, stereo fold-down, 5.1/Atmos printmaster, client preview.
- Target spec: use the client/platform/broadcaster spec if supplied. If no spec is supplied, choose a conservative target and label it as a heuristic.
- Monitoring assumption: headphones-only, nearfield speakers, phone/laptop check, calibrated room, or unavailable.
- Source risk: AI voice artifacts, room noise, inconsistent clips, clipping, music licensing, generated SFX harshness, missing room tone, mono/stereo mismatch, translated VO timing, or stem bleed.

Do not master blindly to the loudest reference. Streaming and broadcast systems may normalize loudness, and over-limiting can reduce clarity while gaining little or nothing at playback.

## Evidence categories

Documented facts:

- ITU-R BS.1770-5 specifies algorithms for programme loudness and true-peak signal level measurement, including K-weighting, channel weighting, gating, and true-peak guidance. Verified 2026-07-10: https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-5-202311-I!!PDF-E.pdf
- EBU R 128 version 5.0 recommends normalising programme loudness to -23.0 LUFS; where attaining target level is not practically achievable, a tolerance of +/-1.0 LU is permitted, and QC workflows may allow +/-0.2 LU for measurement error. The maximum true peak level during production linear audio should not exceed -1 dBTP. Verified 2026-07-10: https://tech.ebu.ch/files/live/sites/tech/files/shared/r/r128.pdf
- ATSC A/85:2026-07 quick reference lists -24 LKFS as the target for delivery/exchange without metadata where no prior arrangement exists, -2 dBTP maximum true peak, and a -23 to -27 LKFS range for streaming delivery services unless parties arrange otherwise. Verified 2026-07-10: https://www.atsc.org/wp-content/uploads/2026/07/A85-2026-07-Annex-M.pdf
- AES TD1008 recommends, for internet audio streaming/on-demand distribution, maximum true peak not exceeding -1 dBTP at the lossy codec input, with examples such as speech/assorted content around -18 LUFS, track-normalized music at -16 LUFS, album loudest track at -14 LUFS, interstitials at -18 LUFS, and format examples from -16 to -18 LUFS. Verified 2026-07-10: https://aes.org/wp-content/uploads/2024/01/20210924_TD1008_v3.13.pdf
- Spotify for Artists recommends targeting -14 dB integrated LUFS and keeping true peak below -1 dBTP; if a master is louder than -14 LUFS, Spotify recommends keeping true peak below -2 dBTP. Verified 2026-07-10: https://support.spotify.com/us/artists/article/loudness-normalization/
- Apple Podcasts recommends overall loudness around -16 dB LKFS with +/-1 dB tolerance and true peak not exceeding -1 dB FS, calculated according to ITU-R BS.1770-5. Verified 2026-07-10: https://podcasters.apple.com/support/893-audio-requirements
- YouTube's official upload encoding help lists recommended upload audio bitrates: mono 128 kbps, stereo 384 kbps, 5.1 512 kbps, and immersive audio at 128 kbps per channel. The same official page does not state a public loudness target. Verified 2026-07-10: https://support.google.com/youtube/answer/1722171
- Netflix branded sound mix specifications require -27 LKFS +/-2 LU dialog-gated loudness, true peaks not exceeding -2 dB True Peak, and 48 kHz/24-bit for original language mix or M&E mix masters. Verified 2026-07-10: https://partnerhelp.netflixstudios.com/hc/en-us/articles/360001794307-Netflix-Sound-Mix-Specifications-Best-Practices-v1-6
- WCAG 2.2 understanding guidance for low/no background audio says background sounds should be at least 20 dB lower than foreground speech, except brief sounds, to support users who are hard of hearing. Verified 2026-07-10: https://www.w3.org/WAI/WCAG22/Understanding/low-or-no-background-audio.html
- FFmpeg's `loudnorm` filter implements EBU R128 loudness normalization, supports single- and double-pass operation, can target integrated loudness, loudness range, and true peak, and upsamples to 192 kHz in dynamic mode for true-peak detection. Verified 2026-07-10: https://ffmpeg.org/ffmpeg-filters.html#loudnorm

## Bundled loudness measurement tool

Use `scripts/measure_loudness.py` when an agent needs a repeatable local measurement before making mix or delivery decisions. It requires Python 3.11+ and an `ffmpeg` executable with the `loudnorm` filter. The script invokes FFmpeg with an argument array rather than a shell, selects the first audio stream, and emits stable JSON. It never normalizes, rewrites, or replaces the input.

Measure without assuming a target:

```bash
python scripts/measure_loudness.py final_mix.wav --pretty
```

Compare against an explicitly selected project target:

```bash
python scripts/measure_loudness.py final_mix.wav \
	--target-lufs -16 --lufs-tolerance 1 \
	--target-true-peak -1 --pretty
```

For mono files intended to play from both speakers as dual mono, request FFmpeg's dual-mono compensation explicitly:

```bash
python scripts/measure_loudness.py narration_mono.wav --dual-mono --pretty
```

The JSON report includes:

- integrated loudness in LUFS;
- true peak in dBTP;
- loudness range in LU;
- measurement threshold;
- analysis mode, whether dual-mono compensation was requested, and FFmpeg's reported loudnorm offset under tool metadata;
- optional target checks with actual values, deltas, tolerances, and pass/fail results;
- an explicit note that results depend on the FFmpeg build, filter, algorithm, and analysis mode.

Exit codes are:

- `0`: measurement completed and every requested target check passed;
- `2`: measurement completed but one or more requested target checks failed;
- `3`: operational failure such as a missing input, missing FFmpeg, timeout, absent audio stream, or malformed loudnorm output.

This tool is deterministic assistance, not final mix approval. Listen to the complete deliverable, confirm the selected target is authoritative, inspect channel layout and codec behavior, and remeasure encoded outputs when delivery risk warrants it. Use a proper calibrated meter or the receiver's mandated QC system when the specification requires one.

Empirical observations:

- Small speakers often hide sub-bass and exaggerate upper-mid harshness; a mix that feels full only because of sub energy may feel thin on phones.
- Generated voices often contain transient clicks, metallic consonants, breaths in odd places, and inconsistent proximity; these problems become more obvious after compression and limiting.
- Generated music and SFX may arrive pre-limited; additional bus limiting can make them flat, gritty, or fatiguing before loudness meters show a problem.
- AI-generated ambience often loops too obviously under narration; crossfade or vary beds before mastering.

Production heuristics:

- For web/social video with speech and no formal spec, start around -16 to -14 LUFS integrated with a true-peak ceiling between -1 and -2 dBTP, then adjust for genre, platform, and client expectations. Label this as a working target, not a documented platform rule.
- For speech-first explainers, intelligibility is more important than loudness. Duck music and effects under speech before raising the whole master.
- For ads and trailers, impact comes from contrast and transient clarity, not constant maximum density. Preserve short-term dynamics around hits.
- For podcasts, listeners forgive moderate noise sooner than they forgive inconsistent dialogue level, distortion, harsh sibilance, or music masking speech.

## Session prep

Make a reproducible session before processing:

1. Confirm sample rate, frame rate, timecode, duration, and target container.
2. Keep an untouched copy of every source. Never destructively overwrite original VO, music, SFX, or stems.
3. Group tracks by role: dialogue/VO, production dialogue, ADR, translated VO, music, score, stingers, SFX, ambience/room tone, UI sounds, captions/audio description references.
4. Align all audio to picture and check sync at the start, middle, and end.
5. Remove dead air only where it does not break natural timing. Preserve room tone or ambience under edits.
6. Mark problem regions: clipped words, plosives, sibilance, room noise, hum, AI artifacts, music masks, SFX spikes, silence gaps, and scene transitions.
7. Decide whether to mix from stems, flattened source, or a hybrid. If sources are flattened, note what cannot be fixed cleanly.

If receiving only a final exported video, demux audio for analysis, but keep picture reference locked. If receiving multitrack/stems, avoid mastering the stereo mix until stem balance is correct.

## Balance and hierarchy

Build the mix from the foreground outward:

- Dialogue/VO: establish stable perceived loudness first. Level clip-by-clip before compression.
- Music: choose whether it supports, drives, or replaces speech. During narration, create space with level, EQ, sidechain ducking, arrangement edits, or automation.
- SFX: keep story-important effects present; trim decorative effects that compete with words.
- Ambience/room tone: fill holes and transitions, but avoid low-frequency buildup and hiss accumulation.
- Silence: use intentional silence for pacing; do not let accidental digital black expose edits.

Do not solve a balance problem only with a limiter. If the voice disappears under music, reduce or carve the music. If SFX feel too sharp, shape the SFX. If the master misses target loudness after the mix feels right, then use bus gain/limiting carefully.

## Dialogue and voice treatment

For spoken-word content:

- Clip-gain first. Bring phrases into a reasonable range before inserting compressors.
- High-pass gently to remove rumble, usually below the useful fundamental of the voice. Avoid thinning baritone or warm narration.
- Cut mud/boxiness only where present; common problem areas often live around low mids, but sweep and listen rather than applying a fixed curve.
- Improve presence with small broad moves; aggressive presence boosts can make AI speech synthetic or harsh.
- Use de-essing for sibilance before final limiting. Do not let a full-band compressor overreact to esses.
- Compress in stages when needed: mild levelling, then faster peak control. Heavy single-stage compression can raise breaths/noise and flatten performance.
- Add room/reverb only when it helps the voice sit in a scene. For explainer VO, keep reverbs short and subtle.
- For avatar/lip-sync, protect consonants and timing; do not process so heavily that lip closure cues feel late or blurred.
- For multilingual dubbing, match the original scene perspective and loudness, not just the transcript timing.

If AI voice artifacts remain audible, prefer localized repairs: replace the line, regenerate the phrase, use spectral repair, trim clicks, redraw fades, or edit breaths. Broadband noise reduction on the full VO can make artifacts worse.

## Music treatment

Music must be licensed, appropriate, and technically controlled:

- Verify rights before final delivery; do not assume generated or stock music is automatically cleared for every use.
- Edit to the picture structure before mastering. Avoid ending on arbitrary fade-outs when a musical button or resolved cadence is available.
- For narration beds, use arrangement edits: remove lead instruments, vocals, or busy fills under important speech when possible.
- Use sidechain ducking as a transparent aid, not as the only mix decision. Slow release can hide pumping; too-slow release can make music feel absent.
- Keep low end centered and controlled for most stereo/social deliveries. Excess wide bass can collapse unpredictably on mono playback.
- For music videos, music is the anchor. Voice tags, SFX, or narrative overlays should not damage the musical master unless that is the creative intent.

## Sound effects and ambience

SFX should clarify action, scale, or emotion:

- Choose fewer, better effects. Layering many generated effects often creates masking and harshness.
- Shape transient intensity. A hit can be exciting without clipping or startling the listener out of the story.
- Match perspective: close UI ticks should not sound like theatrical explosions; distant ambience should not cover dialogue.
- Use room tone/ambience across edits to avoid holes.
- Check repeated generated SFX for identical attacks; vary timing, pitch, or source if repetition calls attention to itself.
- For accessibility, do not bury speech under constant decorative audio. When speech is instructional or essential, use the WCAG 20 dB separation rule as a strict target when feasible, or provide a way to lower/disable background sound.

## EQ, compression, reverb, and limiting

Use processing to solve named problems:

- EQ: remove rumble, mud, resonance, harshness, or masking. Prefer small moves and bypass checks. If a track needs extreme EQ, consider source repair or replacement.
- Compression: stabilize performance, control peaks, glue related elements, or create style. Match attack/release to material; avoid pumping unless it is intentional.
- Expansion/gating: reduce gaps/noise only when it does not chop words, breaths, tails, or room tone. Generated speech often needs manual cleanup more than gates.
- Reverb/delay: place elements in a believable space or create style. Keep speech intelligible; automate returns when scenes change.
- Saturation/excitement: add density cautiously. It can improve small-speaker translation but can also exaggerate AI artifacts and codec distortion.
- Limiting: reserve headroom for codec conversion and true peaks. Use a true-peak limiter near the end, and avoid more than necessary gain reduction.

Limiter safety:

- Set the ceiling to the delivery spec. If no spec exists, -1 dBTP is a common conservative ceiling for web/social; -2 dBTP is safer for aggressive/lossy or broadcast-style deliverables.
- Re-measure after encoding/transcoding when possible. Codec overs can appear after the master.
- If integrated loudness is too low but the limiter is already working hard, fix the mix dynamics before pushing more gain.
- Do not chase short-term loudness by crushing the master; platform normalization may turn it down and leave only distortion.

## Loudness target selection

Prefer this order:

1. Client/broadcaster/platform delivery spec.
2. The strictest spec among intended destinations, if one master must serve all.
3. Separate masters per destination when quality matters and specs conflict.
4. A documented project heuristic when no official target exists.

Useful target map, verified 2026-07-10:

| Destination | Documented or working target | True peak | Notes |
|---|---:|---:|---|
| EBU R 128 broadcast/program exchange | -23 LUFS | -1 dBTP | Use compliant meter; measure full programme. Practical target tolerance may be +/-1 LU; QC measurement tolerance may be +/-0.2 LU. |
| ATSC A/85 TV delivery/exchange without metadata | -24 LKFS | -2 dBTP | Long-form dialogue loudness; short-form full-program mix loudness per A/85 quick reference. |
| ATSC A/85 streaming services | -23 to -27 LKFS | -2 dBTP | Unless prior arrangement says otherwise. |
| Netflix branded content | -27 LKFS +/-2 LU dialog-gated | -2 dBTP | Requires full spec compliance and stems/format rules. |
| Apple Podcasts | about -16 dB LKFS, +/-1 dB | -1 dB FS true peak | Precondition before encoding. |
| Spotify music | -14 dB integrated LUFS | below -1 dBTP, or below -2 dBTP if louder than -14 LUFS | Platform-specific music guidance. |
| AES internet audio examples | speech/assorted around -18 LUFS; music -16 LUFS track-normalized; album loudest track -14 LUFS | -1 dBTP at lossy codec input | For distributors; useful context for producers. |
| YouTube upload | no official loudness target found on upload help page | use project heuristic | Official page lists audio bitrates, not a loudness target. |
| General speech-first social/web video | -16 to -14 LUFS heuristic | -1 to -2 dBTP heuristic | Check speech clarity on phone/laptop/earbuds. |

Never convert these targets into universal rules. If the client asks for a spec, obey the client. If the destination will normalize loudness, prioritize clean transients, dialogue clarity, and codec-safe peaks.

## Stereo, mono, surround, and immersive

For stereo/social:

- Keep essential speech, bass, and call-to-action elements robust in mono.
- Check phase correlation and mono fold-down. Wide pads and stereo enhancers can make speech/music disappear on phones.
- Avoid putting critical UI sounds only in one side unless the picture clearly motivates it.
- Use stereo width for emotion and space, not for essential information.

For 5.1/7.1/Atmos/immersive:

- Confirm the exact deliverable: channel order, bed/object format, ADM/IAB/IMF/WAV requirements, fold-down requirements, and M&E/stem expectations.
- Do not derive immersive deliverables from a stereo master unless the client accepts an upmix.
- Check downmixes: center dialogue, LFE management, surround effects, object levels, and stereo compatibility.
- Keep spoken-word intelligibility as the anchor. Immersion should not make captions or dialogue necessary to understand basic content unless that is the intended accessible mode.

## Accessibility and intelligibility

Treat clear speech as an accessibility requirement:

- If the content teaches, instructs, sells, or explains, speech must remain understandable without perfect listening conditions.
- Keep background audio substantially below speech. For strict WCAG-style prerecorded speech content, target background sounds at least 20 dB lower than foreground speech, except brief effects.
- Avoid constant music with lyrics under narration unless the lyric is intentionally part of the story and does not mask speech.
- Reduce harsh sibilance and piercing effects; they can be painful in earbuds and hearing aids.
- Provide or request captions/transcripts, especially when speech is fast, accented, synthetic, stylized, noisy, or translated.
- For audio description versions, leave clean gaps or produce an alternate mix with ducked programme audio under descriptions.
- Check on at least one small speaker or phone, one pair of earbuds/headphones, and the main monitoring setup when available.

## Stems and deliverables

Plan deliverables before final mix export:

- Full mix: complete intended programme.
- Dialogue/VO stem: all spoken foreground, clean and time-aligned.
- Music stem: score/songs/stingers without dialogue/SFX.
- Effects stem: hard effects, ambience, foley, UI sounds.
- M&E: music and effects without original dialogue; required for dubbing/localization.
- Narration-only or clean VO: useful for accessibility, reversioning, and client edits.
- Printmaster: final approved mix at delivery spec.
- Archive master: high-quality WAV/BWAV, usually 48 kHz/24-bit for video unless spec says otherwise.
- Preview export: compressed review file that should still pass intelligibility and peak checks.

Stems must sum cleanly to the full mix unless the client explicitly requests differently. Check that stem exports start at the same timecode, same sample rate, same length, same channel layout, and no hidden master-bus processing is missing. If master-bus compression or limiting changes the balance, either print processed stems through the bus in solo-safe groups or document that stems are pre-master elements.

## Repair and iteration workflow

When a mix fails, diagnose by symptom:

- Dialogue buried: lower/duck music, carve masking frequencies, reduce ambience/SFX, clip-gain words, or regenerate unclear lines.
- Harsh/metallic voice: reduce presence resonance, de-ess, replace AI line, soften saturation/limiter, avoid over-noise-reduction.
- Muddy mix: remove low-mid buildup from music/ambience, high-pass non-bass elements, reduce reverb tails.
- Thin mix: restore body before adding limiter gain; check if high-pass filters are too aggressive.
- Pumping: slow or reduce compressor/ducking release, automate levels manually, split compression stages.
- Loudness target missed: adjust overall gain only if true peak allows; otherwise revise dynamics and balance.
- True peak failure: lower limiter ceiling, reduce transient elements before limiter, re-render, then re-measure.
- Codec distortion: lower true peak, reduce high-frequency harshness, reduce limiter drive, export higher bitrate if allowed.
- Stems do not sum: check bus routing, sends, sidechains, master effects, pan law, sample offsets, and export selection.
- Sync drift: confirm sample rate, video frame rate, pull-up/pull-down, and whether audio was stretched during editing.

Iterate in this order: source repair, edit cleanup, balance automation, track processing, bus processing, loudness normalization, encode check, final QC. Late mastering should not hide known source or edit defects.

## Final audio QA

Before delivery, create a concise QA note:

- Integrated loudness, short-term/momentary observations if relevant, LRA if required, and maximum true peak.
- Measurement standard/tool/mode, including whether it is ITU/EBU/ATSC/dialog-gated/two-pass.
- Export format, sample rate, bit depth, codec, channel layout, bitrate, and container.
- Sync check status at beginning/middle/end.
- Listening checks: full pass plus phone/laptop/earbuds/nearfield as available.
- Intelligibility pass: sections where speech competes with music/SFX, and what was done.
- Noise/artifact pass: clicks, pops, plosives, clipping, room-tone gaps, AI artifacts, codec distortion.
- Mono/fold-down check for stereo masters; downmix check for surround/immersive.
- Stem validation: same start, duration, sample rate, channel layout, and summing behavior.
- Known limitations: unavailable stems, clipped source, client-provided low-bitrate audio, unavoidable noise, platform uncertainty, unverified target.

If the project has multiple outputs, QA each exported file, not just the first master.

## Complete examples

Example: speech-first social explainer

Production intent: 60-second vertical explainer with AI narration, light music bed, UI clicks, and subtitles for Instagram/TikTok/YouTube Shorts. No formal platform loudness spec supplied.

Direction:

- Contract: speech is foreground; music supports pace; SFX are punctuation only.
- Working target: -15 LUFS integrated, -1.5 dBTP ceiling as a social/web heuristic, with a note that no official YouTube loudness target was used.
- Prep: align VO to picture; clean clicks and unnatural breaths; organize VO/music/SFX/ambience.
- Mix: clip-gain VO phrase-by-phrase, high-pass rumble, mild compression, de-ess. Duck music 6-10 dB under narration and more under dense captions or technical terms. Keep UI clicks short and below speech.
- Accessibility: phone check; if words vanish, lower music rather than raising master. Keep background substantially below speech; for instructional moments, aim for WCAG-style 20 dB separation where feasible.
- Master: true-peak limiter ceiling -1.5 dBTP, minimal gain reduction. Encode preview, re-check true peak and speech.
- Deliver: MP4 plus optional WAV master and VO/music/SFX stems if requested.

Expected result: narration is intelligible on phone speakers, music feels present but not competitive, no clipping after encode, and client can revise music without rebuilding VO.

Likely failure modes: too much high-mid EQ on AI voice, pumping music duck, clicks from VO edits, SFX peaks causing limiter gain reduction.

Example: podcast/video recut from noisy remote interview

Production intent: 18-minute podcast highlight video assembled from two remote speakers, intro music, outro ad tag, and occasional lower-thirds.

Direction:

- Contract: dialogue intelligibility and level consistency are the product. Music exists only at intro/outro and under transitions.
- Target: Apple Podcasts-compatible audio around -16 dB LKFS +/-1 with true peak not exceeding -1 dB FS if the audio is also released as podcast RSS; otherwise choose the video destination spec.
- Prep: separate speakers, mark clipped syllables and crosstalk, gather room tone, remove long silences without destroying conversational rhythm.
- Repair: reduce steady noise conservatively. Use manual edits for bumps/clicks. Replace or mask only severely damaged words; avoid watery noise-reduction artifacts.
- Mix: level each speaker to a similar perceived loudness before compression. Use different EQ only to solve each voice's problem. Keep intro/outro music at a tasteful level and never let ad tag distort.
- Master: measure the full episode, not isolated clips. Check earbuds for mouth clicks and fatigue.
- Deliver: full video mix, WAV audio master, dialogue-only stem, music/ad stem, captions/transcript.

Expected result: speakers feel matched, background noise is reduced but natural, intro/outro are not startling, and listeners do not ride the volume.

Likely failure modes: over-denoising, clipping preserved from source, one speaker much brighter/louder, music intro hitting the limiter and lowering subsequent speech.

Example: trailer/ad with VO, music, hits, and broadcast-style client review

Production intent: 30-second product trailer with cinematic music, VO, whooshes, impacts, and final logo sting. Client may place it on paid social and possibly broadcast later.

Direction:

- Contract: VO and brand message remain intelligible; music/SFX provide scale. Prepare a web/social master now and a broadcast-safe alternate if the media buy confirms it.
- Targets: web/social master at a conservative -16 to -14 LUFS heuristic with -2 dBTP if heavily encoded; broadcast alternate only after receiving buyer spec. If using EBU, aim -23 LUFS and -1 dBTP; if using ATSC without metadata, use -24 LKFS and -2 dBTP.
- Prep: cut music to hit picture beats; remove effects that duplicate music transients; keep logo sting from exceeding the limiter.
- Mix: automate VO above music, carve music during tagline, keep low-end hits powerful but short, and use contrast before each impact.
- Master: limit lightly. If the mix reaches target only by crushing impacts, lower music/SFX density or create more space.
- Stems: print full mix, dialogue, music, effects, and M&E; verify stems start at 00:00 and sum as intended.
- QC: check loudness, true peak, mono fold-down, laptop speaker, earbuds, and final encode.

Expected result: the trailer feels big without masking the message, has safe peaks for lossy platforms, and can be re-versioned for broadcast with stems.

Likely failure modes: SFX hits forcing limiter pumping, music masking final CTA, mono fold-down losing wide risers, broadcast version made by only lowering the social master instead of remixing to spec.
