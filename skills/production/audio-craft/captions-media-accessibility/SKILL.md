---
name: captions-media-accessibility
description: Provider-independent captions and media accessibility direction for AI agents producing or finishing generated videos, ads, social clips, explainers, avatar videos, documentaries, podcasts/video recuts, training media, and localized content. Use when planning, authoring, reviewing, localizing, burning in, exporting, or QAing captions, subtitles, SDH, transcripts, audio description, flashing/motion safety, caption readability, or accessible media handoff files.
---

# Captions and media accessibility direction

Treat captions and accessibility tracks as production assets, not polish. Build them from the script, audio mix, edit, localization plan, and platform delivery target. If the user asks for legal compliance, say what standards you are using and recommend review by qualified accessibility/legal counsel; do not promise legal compliance from a generated file alone.

## Start by classifying the media

Before writing or exporting captions, identify:

- Content type: prerecorded video with audio, live/near-live video, audio-only, video-only, or silent social cut.
- Audience need: captions for deaf/hard-of-hearing viewers, translated subtitles for hearing viewers, SDH, transcript, descriptive transcript, audio description, sign language, or platform-default auto captions.
- Delivery target: social burn-in, web player sidecar, broadcast/OTT, LMS/training portal, internal review, localized package, or archival master.
- Accessibility risk: essential visual text, charts, screen recordings, multiple speakers, overlapping dialogue, music/lyrics, sound-driven story beats, flashing/strobe, fast kinetic typography, low contrast, small mobile screens, or platform UI overlays.
- Final-source truth: the locked audio mix and final picture. Generated scripts, TTS drafts, and ASR transcripts are starting points, not the authority after edits.

## Documented facts to preserve

Use these as factual constraints when relevant, citing the source in your output or handoff notes when the claim matters.

- WCAG 2.2 requires captions for prerecorded audio in synchronized media at Level A (SC 1.2.2), captions for live synchronized audio at Level AA (SC 1.2.4), and audio description for prerecorded video at Level AA (SC 1.2.5). WCAG Level A allows either audio description or a media alternative for prerecorded synchronized video under SC 1.2.3. Source: W3C WCAG 2.2, verified 2026-07-10.
- WCAG 2.2 flashing guidance says content must not flash more than three times in any one-second period unless below the general/red flash thresholds. Source: W3C Understanding SC 2.3.1, verified 2026-07-10.
- WCAG contrast minimum for text is 4.5:1, with 3:1 for large-scale text. This is a web-text criterion; burned-in captions are video pixels, but use it as the minimum design target for caption readability unless a stricter platform/spec applies. Source: W3C WCAG 2.2 SC 1.4.3, verified 2026-07-10.
- Section508.gov distinguishes closed captions, open captions, subtitles, and transcripts: closed captions can be turned on/off; open captions are permanent in the video; subtitles usually translate dialogue for hearing audiences and do not normally include speaker IDs or non-speech audio; transcripts are not time-coded. Source: Section508.gov synchronized media guidance, verified 2026-07-10.
- U.S. FCC caption quality rules for covered television programming define quality around accuracy, synchronicity, completeness, and placement; captions should include relevant nonverbal information, be legible, and avoid blocking essential visual content. Source: 47 CFR Sec. 79.1 via Legal Information Institute/eCFR text, verified 2026-07-10. This skill does not determine whether a specific project is covered by FCC rules.
- YouTube Help listed SRT and SBV/SubViewer as basic formats and WebVTT/TTML/SAMI/RealText as advanced formats; basic SRT/SBV files must be plain UTF-8 and YouTube notes that styling support is limited. Source: YouTube Help, verified 2026-07-10.
- Vimeo Help stated that Vimeo supports SRT and WebVTT for captions/subtitles, recommends WebVTT, and requires UTF-8 encoding for special characters. Source: Vimeo Help, verified 2026-07-10.
- WebVTT is a UTF-8 timed-text format used with media tracks; it begins with `WEBVTT`, contains timed cues, and can be used for captions, subtitles, descriptions, chapters, or metadata depending on player support. Sources: W3C/MDN and Library of Congress WebVTT documentation, verified 2026-07-10.
- W3C WebVTT syntax requires UTF-8, a `WEBVTT` file signature, cue timings with period milliseconds, ordered cue start times, and end times greater than start times. Cue overlap is allowed by the format for captions/subtitles, but many caption delivery workflows still reject or flag overlaps. Source: W3C WebVTT Candidate Recommendation Draft, verified 2026-07-11.
- SRT is a widely used but lightly standardized plain-text sidecar convention made of repeated blocks: numeric counter, start/end timing line, caption text, and a blank-line separator. Common delivery practice uses `HH:MM:SS,mmm --> HH:MM:SS,mmm` timing and UTF-8 for modern platform upload, even though legacy SRT files may use other encodings. Source: Library of Congress SRT format description plus platform guidance already cited here, verified 2026-07-11.
- Netflix timed-text guidance is platform-specific, not universal law. Its public partner help guidance includes 2-line maximums, language-specific style guides, minimum/maximum event durations in general requirements, and U.S. English SDH conventions for bracketed speaker IDs/sound effects. Source: Netflix Partner Help Center, verified 2026-07-10.

## Production heuristics to apply

These are craft defaults. Override them for a formal client style guide, broadcaster spec, language-specific subtitle convention, or platform validation error.

- Prefer a sidecar caption file for accessibility whenever the platform supports it. Add burned-in/open captions only when the platform, ad buy, or user experience requires always-visible text.
- If burning in captions for social, still keep an editable sidecar/transcript master. Burned-in captions cannot be toggled, restyled, searched, translated, or reliably used by assistive tech.
- Use edited captions for prerecorded media. Auto captions are useful for draft alignment, but final work needs human/agent review against audio, speaker identity, punctuation, sound effects, proper nouns, and timing.
- Keep cues readable: usually 1-2 lines, balanced line lengths, natural phrase breaks, and enough on-screen time to read without racing. If text is too dense, edit only nonessential redundancy while preserving meaning and key vocabulary.
- Time cues to the audio they represent: appear near speech/sound onset, disappear near its end, avoid overlapping cues, and avoid making captions lead jokes, reveals, or safety-critical instructions before they are heard.
- Reposition captions when they cover faces, lower-thirds, product UI, charts, subtitles already in picture, legal supers, or platform controls.
- In generated video, reduce caption work by designing the script and edit for accessibility: fewer competing voices, readable on-screen text, visual information described in narration when possible, and pauses for audio description where needed.

## Caption and SDH authoring

Create a caption master from these inputs:

- locked video and audio;
- final narration/dialogue script or transcript;
- speaker list with names, titles, roles, pronunciations, and when names are first revealed;
- glossary for product names, proper nouns, acronyms, technical terms, legal phrases, and invented/generated names;
- music cue sheet and lyrics status;
- on-screen text list, charts/data callouts, and any visual-only story beats;
- target format(s), frame rate/timecode policy, language/locale tag, and style guide.

For each caption cue:

- Include spoken words in order. Do not paraphrase unless readability/time constraints require compression and the chosen standard permits it.
- Preserve meaning, tone, and essential vocabulary. Keep intentional slang, grammatical errors, repetitions, or hesitations when they matter to characterization, humor, safety, or instruction.
- Use punctuation to clarify meaning, not to decorate.
- Identify speakers when the viewer cannot reliably infer who is speaking from placement or picture. Use known names only after the content reveals them; otherwise use neutral descriptors such as `[narrator]`, `[offscreen voice]`, `[woman 1]`, or client-approved labels.
- Include non-speech audio when it affects meaning, mood, safety, story, or instruction: `[alarm blares]`, `[soft piano music]`, `[audience laughs]`, `[door unlocks]`. Do not caption every incidental sound.
- Caption lyrics when lyrics are audible and important, subject to rights/client instructions. If lyrics are not being captioned, identify the music when it affects the experience.
- Avoid exposing information not available to hearing viewers at that moment. Do not name a mystery speaker, reveal a twist, or explain a hidden cause early.
- Avoid visual descriptions inside captions unless they are representing sound or speaker identification. Visual access belongs in narration, integrated description, audio description, or descriptive transcript.

Line breaks:

- Break at sentence, clause, or phrase boundaries.
- Avoid separating articles from nouns, adjectives/modifiers from nouns, first and last names, auxiliary verbs from main verbs, prepositions from their objects, or a subject pronoun from its verb.
- Do not place the end of one sentence and the beginning of another on the same line when a cleaner split is available.
- Keep two-speaker cues rare; when unavoidable, make the speakers visually distinct with a consistent convention supported by the target format/platform.

Timing:

- Align captions to final audio, not script timing.
- Do not let captions persist far beyond speech unless needed for readability and not misleading.
- Use gaps when they improve readability, but avoid unnecessary flicker from very short gaps.
- If a speaker is interrupted, use punctuation that makes the interruption understandable.
- For fast disclaimers, safety instructions, or legal text, push back on unreadable delivery instead of hiding the problem in tiny captions.

## Burned-in/open caption design

Burn-in is typography over moving imagery. Design it like a legible UI:

- Use high contrast against all representative frames. Add a semi-opaque box, shadow, stroke, or gradient when backgrounds vary.
- Keep text large enough for the smallest expected screen and compression path. Preview at phone size, not just on a desktop monitor.
- Leave margins for platform UI: captions, handles, reaction buttons, progress bars, lower-thirds, and safe areas differ by platform and orientation.
- Avoid placing captions over faces, mouths in lip-sync/avatar work, products being demonstrated, charts, subtitles already present, and sign-language interpreters.
- Keep animations restrained. Kinetic word-by-word captions can help social retention, but they are not a substitute for accessible captions if they omit words, move too quickly, lack contrast, or cannot be turned off.
- Do not use color alone to distinguish speakers or meaning. Pair color with labels, placement, or other non-color cues.

## Transcripts and descriptive transcripts

Provide a transcript when the user asks for one, when the media is audio-only, when training/search/review workflows benefit from it, or when accessibility requirements call for a time-based media alternative.

Basic transcript:

- Include speech, speaker names, meaningful non-speech audio, and music/lyrics notes.
- Clean obvious ASR errors, punctuation, and proper nouns.
- Add headings or timestamps when useful for navigation.

Descriptive transcript:

- Include the basic transcript plus essential visual information: on-screen text, charts, actions, scene changes, demonstrations, gestures, and visual-only jokes or instructions.
- Use the same source of truth as captions and audio description.
- Prefer concise descriptions that let a reader understand the content without seeing or hearing the video.

## Audio description planning

Plan audio description before picture lock when possible. The cheapest and cleanest solution for many explainers, demos, and training videos is integrated description: write the main narration so it naturally says essential visual information.

Choose the method:

- Integrated description: best for new explainers, training videos, screen demos, product walkthroughs, and educational media where narration can mention what matters visually.
- Separate audio-description track: best when the original mix should remain unchanged and the player/platform supports an alternate described audio track.
- Described-video alternate export: best when the platform does not support user-selectable audio description but can host a second version.
- Timed text description file: possible where the player supports descriptions from text; verify playback support.
- Descriptive transcript: useful for broad access and required in some WCAG contexts, but not always a replacement for synchronized audio description at the requested conformance level.

What to describe:

- Essential actions, identities, scene changes, settings, charts, diagrams, screen operations, on-screen text, product states, gestures, and visual-only cause/effect.
- Describe from general to specific when orienting a viewer.
- Prioritize what is needed to follow, understand, and appreciate the content. Do not fill every pause.
- Use present tense, active voice, objective wording, and vocabulary suited to the audience.
- Avoid interpreting emotion or intent when a visible fact is enough. Prefer "Maya clenches her fists" over "Maya is furious" unless the emotion is otherwise stated or unmistakable and relevant.
- Place description before or during the relevant visual moment when possible, not after the viewer needs it.
- Avoid talking over dialogue or audio that is essential to comprehension unless necessary.

## Flashing, motion, and sensory safety

Run a sensory-safety pass for generated motion graphics, glitch edits, lightning, alarms, camera flashes, strobes, rapid cuts, high-contrast pattern flicker, red flashes, and aggressive kinetic typography.

- Avoid flashes above the WCAG three-flashes-per-second threshold unless a qualified tester confirms the flash is below the general/red flash thresholds.
- Reduce or remove full-screen white/red flashes, alternating high-contrast frames, rapid inversion effects, and repeated strobe transitions.
- Avoid making captions themselves flash, shake, spin, blur, or rapidly change position.
- For motion-heavy deliverables, consider a reduced-motion variant or less intense edit when the audience or platform warrants it.
- A warning is not a substitute for avoiding unsafe flashing when you can design it out.

## Localization handoff

Do not treat localization as "translate the SRT." Prepare a package:

- final video reference with burnt-in review timecode if helpful;
- source transcript and captions;
- speaker list, character names, pronouns if provided, titles/roles, and pronunciation notes;
- glossary for product names, brand terms, acronyms, UI strings, legal phrasing, jokes, and do-not-translate terms;
- explanation of audience, register/formality, locale, reading level, and platform;
- notes for songs, lyrics, quoted material, censored/bleeped words, and foreign-language dialogue;
- separate instructions for subtitles versus SDH in the target language;
- screenshots or markers for on-screen text that needs translation, dubbing, replacement, or description;
- required output formats, locale tags, and file naming.

Localization decisions:

- Produce separate files per language/locale and per purpose: translated subtitles, same-language captions/SDH, forced narrative subtitles, audio-description scripts, and transcripts are distinct deliverables.
- Let target-language reading speed and subtitle conventions govern line breaks, punctuation, and compression.
- Preserve speaker identification and meaningful non-speech audio in SDH. Standard translated subtitles for hearing audiences may omit non-speech audio unless the client asks for SDH-style subtitles.
- Do not translate source-language dialogue inside same-language captions unless the deliverable is explicitly interlingual subtitles.
- For dubbed/avatar-localized video, captions must match the final dubbed audio, not the source script.

## QA checklist

Review with the final video, final audio, and exported files.

Content:

- Captions match final audio, including added/removed lines, retakes, bleeps, and AI voice changes.
- Proper nouns, numbers, URLs, product terms, units, and acronyms are correct.
- Speaker IDs are accurate and do not reveal information early.
- Essential non-speech audio is included; incidental clutter is removed.
- Captions do not duplicate on-screen text unless needed for accessibility or timing.

Timing and readability:

- No cue overlaps, negative durations, missing end times, or out-of-order cues.
- Cues appear and disappear near the corresponding audio.
- Dense sections are readable at target screen size.
- Line breaks preserve phrase meaning.
- Captions do not obscure essential visuals.

Accessibility and design:

- Sidecar captions are available when the platform supports them.
- Burned-in captions meet contrast and safe-area needs across representative frames.
- Audio description or integrated description covers essential visual-only information.
- Descriptive transcript exists when requested or needed.
- Flashing/motion risks are reduced and documented.

Delivery:

- Files are UTF-8.
- SRT uses comma milliseconds and numbered cues; WebVTT starts with `WEBVTT` and uses period milliseconds.
- Language/locale and type labels are correct on platform upload.
- Sidecars were tested in the target platform or player, not only in a local editor.
- Localized files use target-language style, not source-language line breaks copied blindly.

## Bundled caption validator

This skill includes a standard-library Python 3.11+ validator at `scripts/validate_captions.py`. Use it when an agent needs a local, deterministic check of SRT or WebVTT sidecar structure before handoff, platform upload, or regression review.

What it validates:

- UTF-8 decoding.
- SRT and WebVTT structural parsing by cue blocks, not whole-file substitutions.
- WebVTT `WEBVTT` signature/header separation before cue blocks.
- Focused WebVTT validation for `STYLE`, `REGION`, and cue timing settings; unsupported, duplicate, malformed, or out-of-range settings fail clearly rather than being silently ignored.
- Auto-detected or explicit `srt`/`vtt` format.
- Timestamp syntax: SRT comma milliseconds; WebVTT period milliseconds with `MM:SS.mmm` or `HH:MM:SS.mmm`.
- Cue start time before cue end time.
- Cue ordering and overlap warnings/errors according to this tool's delivery-oriented policy.
- Cue text presence.
- Configurable maximum text lines and visible characters per line.
- Configurable visible characters-per-second warning.

Boundaries:

- The tool does not certify WCAG, FCC, ADA, Section 508, broadcaster, streamer, or platform compliance.
- The tool validates a focused subset of WebVTT settings used in production sidecars; it does not fully parse CSS inside `STYLE` blocks or prove player-specific rendering behavior.
- The tool does not judge transcript accuracy against audio, speaker identity, translation quality, semantic completeness, contrast, placement, flashing safety, or whether captions are sufficient for a given legal duty.
- The tool does not rewrite, compress, translate, normalize Unicode, or semantically edit captions.
- Treat warnings as production review signals. Some WebVTT overlaps are syntactically allowed, but this validator flags overlaps because many caption delivery workflows require non-overlapping readable sidecars.

Example CLI calls:

```bash
python skills/production/audio-craft/captions-media-accessibility/scripts/validate_captions.py captions_en.srt
python skills/production/audio-craft/captions-media-accessibility/scripts/validate_captions.py --format vtt captions_en.txt
python skills/production/audio-craft/captions-media-accessibility/scripts/validate_captions.py --max-lines 2 --max-chars-per-line 42 --cps-warning 20 captions_en.vtt
python skills/production/audio-craft/captions-media-accessibility/scripts/validate_captions.py --warnings-as-errors captions_en.srt
```

Exit codes:

- `0`: no validation errors; warnings may be present unless `--warnings-as-errors` is set.
- `2`: validation errors, or warnings with `--warnings-as-errors`.
- `3`: operational or parse failure, such as unreadable file, invalid UTF-8, unknown format, missing WebVTT header, or malformed cue block.

JSON output schema:

```json
{
	"tool": "validate_captions",
	"version": "1.0.0",
	"status": "passed",
	"summary": {
		"files": 1,
		"cues": 2,
		"errors": 0,
		"warnings": 0
	},
	"files": [
		{
			"path": "captions_en.srt",
			"format": "srt",
			"cues": 2,
			"errors": 0,
			"warnings": 0
		}
	],
	"findings": [
		{
			"severity": "warning",
			"code": "characters_per_second",
			"cue": 2,
			"location": {
				"file": "captions_en.srt",
				"line": 6
			},
			"message": "Cue reads at 22.50 characters per second; warning threshold is 20"
		}
	]
}
```

Stable finding fields are `severity`, `code`, `cue`, `location`, and `message`. `location` always contains `file` and may contain `line` and `column`. Known finding codes include `invalid_utf8`, `file_read_failed`, `format_unknown`, `webvtt_header_missing`, `webvtt_header_invalid`, `webvtt_late_header_block`, `webvtt_timing_missing`, `srt_block_too_short`, `srt_index_invalid`, `timestamp_syntax`, `time_order`, `cue_order`, `cue_overlap`, `cue_text_missing`, `srt_index_sequence`, `max_lines`, `max_chars_per_line`, `characters_per_second`, and `no_cues`.

## Examples

### Example: social ad caption plan

Production intent: 20-second vertical ad for a running app, English source, uploaded to TikTok/Reels/YouTube Shorts, with always-visible creative captions plus an SRT master.

Approach:

- Create a verbatim SDH-capable SRT from the final mix.
- Burn in a shorter visual caption layer for retention only if it does not omit safety-critical claims.
- Keep captions above bottom UI and away from the app screen recording.
- Use a semi-opaque dark backing because footage alternates between outdoor daylight and phone UI.
- Run a flash check on impact transitions and remove white-frame strobes.

Example SRT excerpt:

```srt
1
00:00:00,200 --> 00:00:02,000
[upbeat electronic music]

2
00:00:02,100 --> 00:00:04,300
MAYA: I stopped guessing
what my training needed.

3
00:00:04,500 --> 00:00:07,000
Now RunPilot adjusts my plan
after every workout.

4
00:00:07,200 --> 00:00:09,100
[watch chimes]
Today's run just got easier.
```

Why it is structured this way: the SRT keeps speaker and sound context for accessibility, while the separate burned-in creative layer can use fewer words only because the sidecar remains complete.

Likely failure modes: platform UI covers the bottom line; ASR hears "RunPilot" as "run pilot"; the burned-in layer becomes the only delivered caption and omits `[watch chimes]`.

### Example: integrated audio description for a training explainer

Production intent: 90-second onboarding video showing how to reset a dashboard filter. The user wants accessible training media, not a cinematic story.

Accessible narration rewrite:

```text
Original narration:
"Click here, then choose last quarter."

Integrated description rewrite:
"In the left sidebar, open Filters, then choose Last quarter from the Date range menu."
```

Additional handoff notes:

- Ensure the cursor target is also visible and highlighted for sighted users.
- Add captions matching the final narration.
- Add a descriptive transcript with the exact menu path and any on-screen confirmation text.
- If the edit later removes the sidebar shot, update both captions and transcript so the instruction still makes sense.

Why it is structured this way: essential visual information is moved into the main audio, reducing the need for a separate audio-description track while improving the training script for everyone.

### Example: localization package summary

Production intent: English product-launch video localized into Spanish (Latin America), French (France), and Japanese; captions and subtitles are required, dub may be added later.

Handoff:

```text
Files:
- launch_final_ref_23976.mp4
- launch_en-US_captions_SDH.vtt
- launch_en-US_transcript_descriptive.md
- launch_source_dialogue_glossary.csv
- launch_on_screen_text_markers.csv

Deliverables requested:
- es-419 translated subtitles, not SDH, WebVTT
- fr-FR translated subtitles, not SDH, WebVTT
- ja-JP translated subtitles, not SDH, WebVTT
- separate translator notes for UI text that should remain in English

Style:
- Product name "Northstar Studio" is never translated.
- Tone is confident but not slang-heavy.
- Preserve the joke in scene 4 by adapting the idiom, not literal word order.
- If later dubbed, regenerate captions from the final dubbed audio.
```

Why it is structured this way: it separates same-language accessibility assets from translated subtitles, gives locale targets, and avoids freezing English line breaks into other languages.

## Source notes

Verified on 2026-07-10:

- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- W3C Understanding SC 1.2.5 Audio Description: https://www.w3.org/WAI/WCAG22/Understanding/audio-description-prerecorded
- W3C Understanding SC 2.3.1 Three Flashes or Below Threshold: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- W3C Making Audio and Video Media Accessible: https://www.w3.org/WAI/media/av/
- W3C Transcripts: https://www.w3.org/WAI/media/av/transcripts/
- W3C Description of Visual Information: https://www.w3.org/WAI/media/av/description/
- Section508.gov synchronized media guidance: https://www.section508.gov/create/synchronized-media/
- 47 CFR Sec. 79.1 captioning quality standards: https://www.law.cornell.edu/cfr/text/47/79.1
- DCMP Captioning Tip Sheet: https://dcmp.org/learn/225-captioning-tip-sheet
- DCMP Audio Description Tip Sheet: https://dcmp.org/learn/227-audio-description-tip-sheet
- YouTube Help supported subtitle and closed caption files: https://support.google.com/youtube/answer/2734698
- Vimeo Help captions/subtitles upload guidance: https://help.vimeo.com/hc/en-us/articles/21956884955537-How-to-add-captions-or-subtitles-to-my-video
- Vimeo Help caption file types: https://help.vimeo.com/hc/en-us/articles/21957353918609-Troubleshooting-Caption-file-types
- MDN WebVTT format: https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API/Web_Video_Text_Tracks_Format
- Library of Congress WebVTT format description: https://www.loc.gov/preservation/digital/formats/fdd/fdd000567.shtml
- W3C WebVTT Candidate Recommendation Draft: https://www.w3.org/TR/webvtt1/
- Library of Congress SRT format description: https://www.loc.gov/preservation/digital/formats/fdd/fdd000569.shtml
- Netflix Timed Text Style Guide general requirements: https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements
- Netflix English (USA) Timed Text Style Guide: https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide
