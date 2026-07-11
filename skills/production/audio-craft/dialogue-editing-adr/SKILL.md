---
name: dialogue-editing-adr
description: "Provider-independent dialogue editing and ADR direction for AI agents producing generated videos, films, ads, avatar clips, explainers, localization/dubbing, podcasts, recuts, and social content. Use for dialogue prep, repair, room tone, take comping, sync, ADR cueing, dubbing direction, pronunciation, de-essing, plosives, mouth clicks, voice continuity, synthetic voice consent boundaries, captions/transcripts handoff, mix handoff, loudness, intelligibility, accessibility, and QA."
---

# Dialogue editing and ADR direction

Use this skill when spoken audio must carry story, brand, instruction, character, or accessibility. Treat dialogue as a performance and an editorial contract, not just a waveform. The job is to preserve intelligibility, intent, continuity, and rights while leaving the mixer, captioner, localization team, or downstream video agent with unambiguous material.

## Evidence posture

Documented facts below come from professional standards, official platform guidance, official tool documentation, or rights organizations. Volatile platform/tool/legal facts were checked on 2026-07-10. Empirical observations are limited to listening/QC behaviors an agent should perform on the actual project; no universal audio-processing result is assumed without auditioning. Production heuristics are practical defaults to test against picture and delivery specs, not laws of audio.

## First pass: decide what kind of dialogue problem this is

Classify each line or section before touching it:

- `production-edit`: usable source audio needs cleanup, smoothing, fill, conform, or comping.
- `performance-fix`: the words are technically usable but the read, emotion, pronunciation, emphasis, or timing fails the scene.
- `ADR-replace`: production sound is not intelligible, has unrecoverable noise/clipping, contains changed script, needs a legal/brand correction, or must match a new cut.
- `localization-dub`: new language or regional version must preserve meaning, performance, timing, and picture sync.
- `VO-style-dub`: original voice remains partly perceptible or intentionally dipped under a localized voice-over.
- `synthetic-rerender`: a licensed synthetic voice or generic TTS voice must be regenerated, edited, or directed.
- `caption/transcript-handoff`: text assets must represent the final heard audio accurately and accessibly.

Do not choose ADR or synthetic replacement merely because repair is inconvenient. First determine whether the original performance can be made intelligible without audible artifacts, whether the actor/voice rights permit replacement, and whether the replacement will match picture and continuity.

## Documented facts to respect

- ITU-R BS.1770-5 specifies algorithms for measuring audio programme loudness and true-peak level; it is a measurement method, not a creative mix recipe. Source: ITU-R BS.1770-5, verified 2026-07-10.
- EBU R 128 version 5.0 recommends programme loudness normalization at -23 LUFS and uses loudness range and true peak descriptors. Source: EBU R 128, verified 2026-07-10.
- FCC caption quality guidance for U.S. television uses four quality pillars: accuracy, synchronicity, completeness, and placement. The FCC guide says prerecorded programming is expected to have full compliance because offline review is possible. Source: FCC DA 21-469, verified 2026-07-10.
- W3C WCAG 2.2 SC 1.2.2 requires captions for prerecorded audio in synchronized media, with captions covering dialogue, speaker identification, and meaningful non-speech information. Source: W3C WAI Understanding SC 1.2.2, verified 2026-07-10.
- Netflix timed-text general requirements use 5/6 second minimum and 7 second maximum subtitle-event durations, a two-line maximum, and positioning that avoids overlap with relevant on-screen text. These are Netflix requirements, not universal specs. Source: Netflix Partner Help Center, verified 2026-07-10.
- Netflix dubbing guidance emphasizes that lip sync should be judged primarily against picture, not original-version waveforms; key moments should account for mouth flaps, labials, and start/end mouth shapes. Source: Netflix Dubbing Guiding Principles, verified 2026-07-10.
- Netflix dubbing/mixing guidance asks for dialogue to be embedded naturally in the music-and-effects bed, with realistic level, EQ, reverbs, perspective, futzes, and continuity across languages. Source: Netflix Mixing Style Guide for Dubbed Content, verified 2026-07-10.
- Netflix nonfiction English dubbing guidance recommends recording clean dialogue without dynamic processing except a low-cut no higher than 100 Hz, removing tongue clicks/saliva unless performance-driven, using fades on dialogue clips, editing against the audio reference, and ending dubbed dialogue at the same time as the original version where that workflow applies. Source: Netflix Partner Help Center, verified 2026-07-10.
- iZotope RX documentation describes Mouth De-click as detecting and reducing mouth noises such as clicks and lip smacks, while warning that high sensitivity can affect plosives or damage the original signal. RX De-plosive is documented as identifying and reducing plosives while preserving speech fundamentals and harmonics, but higher strength can harm useful speech. These are tool capabilities, not guarantees. Source: iZotope RX docs, verified 2026-07-10.
- The U.S. Copyright Office's AI report page states that Part 1, published July 31, 2024, addresses digital replicas, while SAG-AFTRA's AI framework states clear consent, fair compensation, and control over performances as guardrails. NAVA recommends performer contracts include consent, limits on AI/synthetic use and training, opt-out or term limits, payment, exclusivity clarity, and safe storage/tracking. These are not a complete legal opinion. Sources: U.S. Copyright Office, SAG-AFTRA, NAVA, verified 2026-07-10.

## Empirical checks to perform on the actual media

Listen, do not infer from meters alone. For each deliverable, perform at least these checks:

- Headphones pass for clicks, edits, breaths, plosives, clothing noise, sibilance, harsh de-noise artifacts, clipped syllables, and unnatural room-tone loops.
- Speaker pass at normal consumer level, with captions off, to judge whether a person unfamiliar with the script can follow the words.
- Small-speaker or mono pass when the content may be watched on phones, laptops, TVs, or social feeds.
- Picture-sync pass at final frame rate and codec path, because DAW, NLE, browser, or low-latency preview timing can mislead sync judgment.
- Context pass with music, effects, and captions/subtitles as they will ship; a line that is clear solo may fail in the full mix.

## Production heuristics

### Build a dialogue map

Create a line-level map before repair or ADR. Include:

- timecode in/out;
- speaker/character;
- on-screen or off-screen status;
- source file/take/track;
- exact heard text and intended text if different;
- problem label;
- proposed treatment;
- pronunciation notes;
- rights/consent status for any real-person voice or synthetic likeness;
- handoff notes for captions, transcript, mixer, or localization.

Prefer this shape:

```text
TC In-Out | Speaker | Screen | Heard/Intended | Issue | Treatment | Notes
00:00:12:04-00:00:15:10 | Maya | on | "we ship Friday" | fan + click on "Friday" | repair | keep laugh breath; room tone B
00:00:35:12-00:00:37:01 | CEO | off | "Series B" misread as "serious B" | pronunciation | ADR | say "SEER-eez bee"; legal name unchanged
```

### Preserve the best original performance

Use the least invasive route that solves the real problem:

1. Alternate mic or isolated production channel.
2. Alternate take or wild line.
3. Manual edit, clip gain, short crossfade, room-tone fill.
4. Targeted repair on the defect only.
5. ADR or synthetic regeneration when the line remains unintelligible, wrong, unsafe, or off-brief.

Avoid broad noise reduction first. Broad processing often reduces consonant detail, breath realism, and room continuity before it solves the edit.

### Cut dialogue as continuous air

When assembling or comping:

- Keep breaths that support performance, remove only distracting or technically bad breaths.
- Use room tone or matching ambience under every gap where dialogue has been cut.
- Crossfade every clip boundary unless the cut falls inside masked noise or a transient that truly needs no fade.
- Match room tone by scene, mic perspective, and emotional distance. Do not paste one "silence" bed across different rooms.
- Use clip gain to smooth syllables before compression. Treat compression as mix support, not a fix for erratic edits.
- Maintain consonant attacks. Do not trim the front of plosives, fricatives, or soft entries just because the waveform looks quiet.

### Clean artifacts in a repair order

Use targeted, auditioned passes:

1. Remove edit pops with boundaries, fades, and zero-crossing adjustments.
2. Reduce mouth clicks/lip smacks locally; keep performance-relevant mouth texture when realism matters.
3. Reduce plosives with a targeted low-frequency or de-plosive pass; if the useful low voice is damaged, undo and use manual clip gain/spectral repair.
4. Control sibilance with narrow, dynamic treatment; do not lisp the speaker.
5. Reduce hum/rumble with a high-pass or hum removal only as far as needed. For spoken content, low-cut choices must respect voice body and delivery specs.
6. Use de-noise/de-reverb/dialogue isolation conservatively, listening for watery, phasey, chirping, or dull consonants.
7. Rebalance clip gain and room tone after repair, because repairs can reveal new discontinuities.

If a repair creates a more noticeable artifact than the original problem, revert and choose an alternate take, ADR, or an honest "cannot cleanly repair" note.

## ADR and dubbing direction

### Prepare the cue

An ADR cue should be performable without guessing. Include:

- scene context in one sentence;
- picture reference timecode;
- exact line and approved alternates;
- reason for ADR;
- performance intent;
- sync anchors: start/end mouth, labials, visible pauses, gestures, breaths, reactions;
- pronunciation guide for names, acronyms, product terms, and sensitive words;
- mic/perspective target: close, chesty, whispered, shouted across room, phone, helmet, radio, archival, etc.;
- room/processing target and whether the mixer should match production dirt or improve fidelity;
- takes requested and what changes between takes.

For cueing, use whatever the talent and recording setup support: beeps, streamers, visual text, loop recording, or listen-and-repeat. Three-beep ADR is common in film workflows, but do not impose it if it hurts the actor. The cueing method is a performance aid, not the goal.

### Direct the performance before the waveform

Give actors playable verbs and context:

- Say what the speaker wants from the listener.
- Identify the emotional turn in the line.
- Give one timing note at a time.
- Preserve the scene's social status, fatigue, age, accent policy, and relationship.
- Ask for natural pronunciation unless the story requires extra clarity.
- For ads and explainers, direct emphasis around meaning, not every brand word. Over-emphasized product terms sound synthetic.

For localization, preserve intent rather than word order. Use colloquial target-language phrasing when appropriate to the character and brief. When picture sync matters, judge against the mouth and cut, not only the source waveform. Start and end mouth shapes, visible labials, and open-mouth vowels matter most in close-up and key moments.

### Capture enough takes to edit

Request:

- one faithful timing take;
- one performance-priority take;
- one cleaner diction take;
- one safety alternate with a shorter or longer phrase if sync may need it;
- room tone/efforts/breaths only when rights and performance needs justify them.

For nonfiction VO-style dubbing, avoid recording laughs, cries, and nonverbal reactions unless the style guide or client explicitly asks. When original nonverbal sounds remain in the mix, the editor should feature them rather than duplicate them.

### Maintain voice continuity

Create a continuity note for recurring voices:

- voice source or actor;
- consent/rights scope;
- language/locale;
- age, gender expression, accent policy, dialect notes;
- speaking rate range;
- pitch/energy range;
- mic distance and room;
- signature pronunciations;
- previous treatments: EQ, reverb, futz, noise floor, de-ess behavior;
- exceptions, such as archival, phone, stress, illness, flashback, or intentional mismatch.

Never "match" a real person's voice with synthetic cloning unless the project has explicit rights and informed consent for that exact use. If consent is unclear, offer a generic voice, a new casting direction, or a rights-clearance question.

## Synthetic voice boundaries

Before using TTS, voice conversion, voice cloning, or synthetic dubbing:

- Verify who owns or controls the source voice, whether the speaker consented to this use, whether model training or voice replication is permitted, whether use is limited by term/territory/media, and whether disclosure is required by client, platform, contract, or law.
- Do not train on, clone, imitate, or "sound like" a living or deceased identifiable person without documented permission.
- Do not use a synthetic voice to make someone appear to say something they did not authorize.
- Do not infer consent from public availability of recordings.
- Preserve audit notes: source, license/consent summary, voice ID, provider/model, date, prompt, parameters, editor, and final use.
- If a prompt asks for a protected or identifiable voice imitation without rights, redirect to permissible vocal qualities: age range, energy, pace, timbre, accent only when appropriate and non-caricatured.

Good synthetic direction is still performance direction:

```text
Voice: licensed internal brand narrator, calm but not sleepy.
Line: "Your backup finishes before your coffee does."
Intent: reassuring proof, not hype.
Pace: medium-fast; slight smile on "coffee"; no announcer boom.
Pronunciation: "backup" as BACK-up, not back-UP.
Delivery constraints: no imitation of any celebrity or employee; no added words.
Edit notes: leave 200 ms clean tail for crossfade; deliver dry WAV plus timing.
```

## Captions, transcripts, and accessibility handoff

The spoken-audio handoff must match what ships, not what the script used to say.

Provide:

- final transcript word-for-word for discernible dialogue;
- speaker labels where needed for comprehension;
- non-speech audio notes when they carry meaning: `[door slams]`, `[crowd chanting]`, `[phone voice]`;
- pronunciation and spelling list for names, brands, acronyms, and invented terms;
- forced narrative needs for plot-relevant foreign language or on-screen text;
- caption timing notes if line timing changed after ADR;
- warnings for intentionally inaudible, overlapped, censored, or partially masked lines.

Do not "clean up" captions so they contradict the audio. If SDH/caption reading speed requires condensing, preserve meaning and spoken order as much as the target spec permits; flag any unavoidable deviation.

## Mix handoff

Deliver clean, traceable material:

- dialogue edit session or rendered stems organized by scene/speaker;
- dry ADR/dub takes and selected comps;
- processed dialogue premix only if requested;
- room tone/ambience fills;
- M&E interaction notes;
- repair notes for any aggressive processing;
- loudness measurements and target spec used;
- sample rate, bit depth, frame rate, pull-up/down if any;
- plugin/process list when needed for reproducibility;
- unresolved issues and decision requests.

Do not bake destructive processing into the only copy unless the client requires it. Prefer dry dialogue plus an optional processed reference.

## Loudness and intelligibility

Use the delivery spec first. If no spec exists, name the provisional target and ask for confirmation before final mix.

Heuristics:

- Social/platform/web shortform often benefits from a controlled, foreground dialogue balance, but target loudness varies by platform and client.
- Broadcast/streaming deliverables may require integrated loudness, true peak, dialogue-gated or programme-gated measurements, channel layout, and deliverable-specific tolerances.
- Intelligibility is not the same as loudness. The audience must understand consonants and meaning against music/effects on likely playback devices.
- Meters cannot prove intelligibility; use native-speaker listening when language matters, and do at least one pass with captions off.
- Do not crush dynamics just to make every syllable visually large. Natural dynamics help performance and listener comfort.

## QA checklist

Pass only when the answer is yes or a known exception is documented:

- Is every intended word intelligible in the final mix at normal volume?
- Are all ADR/dub lines in sync with picture at the final frame rate?
- Do visible mouth starts, ends, labials, and pauses work in close-ups and key moments?
- Are clicks, plosives, sibilance, de-noise artifacts, clipped consonants, and edit pops absent or intentionally retained?
- Does room tone change naturally across cuts?
- Does each recurring voice remain continuous unless the story explains the change?
- Are synthetic voice rights, consent, model/source, and use limits documented?
- Are captions/transcripts updated to the final audio?
- Are loudness and true peak measured against the correct spec?
- Has someone listened with captions off?
- Has a small-speaker/mono or likely-device pass been done when relevant?
- Are unresolved fixes separated into `must fix`, `creative choice`, and `client decision needed`?

## Example: dialogue rescue plan for an explainer

Production intent: repair a 90-second product explainer recorded in a home office. The voice is the founder, fan noise is present, and the brand wants the real performance retained.

Approach:

1. Build a dialogue map with fan-noise severity, clicks, plosives, and any words masked by music.
2. Ask for any alternate mic, original WAV, or second take before processing.
3. Assemble best takes and smooth clip gain.
4. Remove isolated mouth clicks manually or with a targeted mouth de-click pass.
5. Reduce plosives only on affected syllables.
6. Use light broadband noise reduction only after making a short noise print and auditioning consonants.
7. Add matched room tone beneath cuts; do not mute gaps to digital black.
8. Rebalance music after dialogue repair rather than over-processing the voice.
9. QA on headphones and laptop speaker, captions off.

Expected result: the founder still sounds like the founder; fan noise is reduced enough not to distract; no watery consonants; transcript updated to final wording.

Likely failure modes: too much de-noise, clipped breaths, dead-silent gaps, plosive repair removing low voice body, music reintroduced too loud.

## Example: ADR cue packet for a launch ad

Production intent: replace one line in a 30-second launch ad because the product name changed after picture lock.

```text
Cue ADR-07
Timecode: 00:00:18:12-00:00:20:02
Speaker: Ava, on camera, medium close-up, walking toward lens
Original line: "Montage Studio ships your recap by morning."
New line: "OpenMontage ships your recap by morning."
Reason: approved product naming
Performance intent: confident relief; she is solving the viewer's Friday problem, not pitching loudly
Sync anchors: visible "m/b/p" closure on first word; smile begins on "recap"; line must end before she turns away
Pronunciation: OpenMontage = OH-pen mon-TAHZH
Mic/perspective: match production lav; close, dry office hallway; no announcer tone
Takes:
  1. exact timing
  2. warmer, slightly faster
  3. cleaner product pronunciation without overemphasis
Edit note: keep original footstep and jacket rustle from production track; do not replace with synthetic voice
```

## Example: localization dubbing direction

Production intent: localize a documentary interview segment for a new market using VO-style dubbing.

Direction:

- Preserve the interviewee's credibility and fatigue; do not make the localized voice more polished than the original.
- Keep original interview audio perceptible only as the approved style requires; do not create confusing overlaps.
- Use natural target-language phrasing and research subject-specific vocabulary before recording.
- Do not reproduce the interviewee's non-native accent if it risks caricature or insensitivity.
- Keep the original laugh and breath if they carry emotion; do not re-record reactions unless requested.
- Edit dubbed line timing against the original audio reference and final picture.
- Update as-recorded script/transcript from the final recorded audio, not the translation draft.

QA: a native speaker unfamiliar with the script should understand the segment with subtitles off and feel that the voice belongs to the same person and moment.

## Example: QA finding

```text
Finding: Must fix
TC: 00:01:04:18-00:01:07:05
Issue: ADR line starts in sync but ends six frames late; final "now" lands after the actor's mouth closes.
Evidence: picture-sync pass at final 23.976 export; captions off.
Recommended fix: choose take 3, trim internal pause before "now", avoid time-stretch unless the edit still fails.
Risk if ignored: visible dub/ADR mismatch in close-up key moment.
```

## Source notes

- ITU-R BS.1770-5, "Algorithms to measure audio programme loudness and true-peak audio level": https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-5-202311-I!!PDF-E.pdf
- EBU R 128, "Loudness normalisation and permitted maximum level of audio signals": https://tech.ebu.ch/publications/r128
- AES, "Improving Dialogue Intelligibility in Media": https://aes.org/wp-content/uploads/2025/12/5297fea6-25ba-4865-92f6-dc1d0ba52ce4.pdf
- FCC DA 21-469, closed captioning quality standards compliance guide: https://docs.fcc.gov/public/attachments/DA-21-469A1.pdf
- W3C WAI, Understanding WCAG 2.2 SC 1.2.2 Captions (Prerecorded): https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
- Netflix Partner Help Center, Dubbing Guiding Principles: https://partnerhelp.netflixstudios.com/hc/en-us/articles/10258052221459-Dubbing-Guiding-Principles
- Netflix Partner Help Center, Mixing Style Guide for Dubbed Content: https://partnerhelp.netflixstudios.com/hc/en-us/articles/360017944573-Netflix-Mixing-Style-Guide-For-Dubbed-Content
- Netflix Partner Help Center, Dubbing Creative Guidelines - Nonfiction/Unscripted English: https://partnerhelp.netflixstudios.com/hc/en-us/articles/11220999686163-Dubbing-Creative-Guidelines-Nonfiction-Unscripted-English
- Netflix Partner Help Center, As Recorded Dubbing Script Scope of Work: https://partnerhelp.netflixstudios.com/hc/en-us/articles/4407306862611-As-Recorded-Dubbing-Script-Scope-of-Work
- Netflix Partner Help Center, Timed Text Style Guide: General Requirements: https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements
- iZotope RX Mouth De-click documentation: https://downloads.izotope.com/docs/rx6/33-mouth-de-click/index.html
- iZotope RX De-plosive documentation: https://downloads.izotope.com/docs/rx6/26-de-plosive/index.html
- U.S. Copyright Office AI initiative and report page: https://www.copyright.gov/ai/
- SAG-AFTRA Artificial Intelligence member resources: https://www.sagaftra.org/contracts-industry-resources/member-resources/artificial-intelligence
- NAVA Synth & AI resources: https://navavoices.org/synth-ai-info/
