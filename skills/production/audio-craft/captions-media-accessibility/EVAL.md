# Evaluation: captions-media-accessibility

Use this file as an answer key and scoring guide after an agent has used only `SKILL.md` to answer or perform a captions/media-accessibility task. Do not expose this file to the evaluated agent.

## Overall scoring

Score out of 100:

- 20: Correctly distinguishes caption/subtitle/SDH/transcript/audio-description deliverables.
- 15: Applies documented accessibility facts without overclaiming legal compliance.
- 15: Makes sound production decisions for format, burn-in versus sidecar, timing, line breaks, speaker IDs, and non-speech audio.
- 15: Handles generated-media realities: final audio as source of truth, ASR cleanup, avatar/dub changes, social safe areas, platform UI, and motion safety.
- 15: Plans audio description/descriptive transcript appropriately.
- 10: Handles localization handoff and target-locale distinctions.
- 10: Provides concrete QA steps and file checks.

Critical failures that should cap the score at 60 even if other parts are good:

- Claims that subtitles and captions are equivalent for accessibility in all contexts.
- Recommends auto captions as final accessibility deliverables for prerecorded media without review.
- Delivers only burned-in captions when a sidecar is feasible and accessibility is the goal, without explaining the limitation.
- Ignores essential non-speech audio or speaker identification in an SDH/caption task.
- Promises legal/FCC/WCAG compliance without caveats or a project-specific standard.
- Gives unsafe flashing advice, such as "add a warning" instead of reducing strobe/flashing risk.
- Exposes or refers to this evaluation file in a production answer.

## Knowledge questions

### 1. Captions versus subtitles

Question: A user asks for "subtitles" for an English training video and says the goal is accessibility for deaf and hard-of-hearing employees. What should the agent clarify or deliver?

Expected answer:

- Clarify that the accessibility deliverable is captions/SDH, not just translated subtitles.
- Include dialogue, speaker identification when needed, and meaningful non-speech audio.
- Provide sidecar captions if supported by the LMS/player, with optional burn-in only as an additional viewing aid.
- Provide a transcript/descriptive transcript if requested or useful.

Penalize:

- "Subtitles are enough because they show dialogue."
- Omitting non-speech audio and speaker IDs.
- Failing to ask or infer the target player/platform.

### 2. WCAG media requirements

Question: Name the WCAG 2.2 success criteria most relevant to prerecorded video with audio.

Expected answer:

- SC 1.2.2 captions for prerecorded synchronized audio at Level A.
- SC 1.2.3 audio description or media alternative for prerecorded synchronized video at Level A.
- SC 1.2.5 audio description for prerecorded synchronized video at Level AA.
- Mention transcripts/descriptive transcripts as media alternatives where applicable.
- If visual design is discussed, SC 1.4.3 contrast and SC 2.3.1 flashing are relevant.

Penalize:

- Treating WCAG as a caption style guide with exact line lengths.
- Claiming WCAG requires burned-in captions.
- Saying audio description is never needed if captions exist.

### 3. FCC caption quality

Question: What are the FCC quality dimensions for covered television closed captions, and how should an agent use them?

Expected answer:

- Accuracy, synchronicity, completeness, and placement.
- Use them as a quality framework for caption review.
- Note that whether a given web/social/generative project is legally covered is a separate legal/compliance question.

Penalize:

- Overstating FCC coverage for every online video.
- Omitting placement/readability.

### 4. Sidecar versus burned-in captions

Question: What are the tradeoffs between sidecar and burned-in captions?

Expected answer:

- Sidecar/closed captions can be toggled, restyled by some players, searched/indexed in some systems, translated/replaced, and used more appropriately as accessibility tracks.
- Burned-in/open captions are always visible and useful for social feeds or platforms where captions are unreliable, but cannot be turned off, restyled, edited separately, or relied on as assistive-tech-friendly text.
- Best practice often includes a sidecar master plus optional burned-in creative captions.

Penalize:

- Saying burn-in is always more accessible.
- Ignoring platform constraints.

### 5. WebVTT and SRT basics

Question: What simple file-format checks should the agent perform before delivery?

Expected answer:

- UTF-8 encoding.
- SRT has numbered cues and comma milliseconds (`00:00:01,000`).
- WebVTT begins with `WEBVTT` and uses period milliseconds (`00:00:01.000`).
- No overlapping/out-of-order cues; cue text lines present; correct language/type labels in platform upload.

Penalize:

- Mixing SRT and VTT timestamp syntax.
- Assuming platform styling support without checking.

## Production-decision scenarios

### 6. Avatar video after script edits

Scenario: An avatar video was generated from a script. The producer trimmed pauses, regenerated two TTS lines, and changed a product name in the final audio. The captions still come from the original script.

Strong answer:

- Reject using the original script as final captions.
- Align captions to the final audio/picture.
- Verify product name spelling, timing after trims, and mouth/face obstruction if burned in.
- Update sidecar, burn-in layer if any, transcript, and localized source if localization follows.

Penalize:

- "The script is close enough."
- Only retiming without checking changed words.

### 7. Dense social ad with fast kinetic captions

Scenario: A 15-second ad has every word animated with bouncing text, white flashes on transitions, and no sidecar captions. The user asks if this is accessible.

Strong answer:

- Explain that kinetic captions may help engagement but are not automatically accessible.
- Recommend a complete sidecar caption file when platform supports it.
- Check contrast, font size, safe areas, motion speed, and word omissions.
- Reduce/remove white/red flashing and strobe-like transitions; reference the three-flashes-per-second threshold without claiming a full test unless performed.
- Keep a readable burn-in version if social always-visible captions are desired.

Penalize:

- Treating animated word captions as sufficient.
- Keeping flashes and adding only a warning.

### 8. Training video with visual-only instructions

Scenario: A screen-recording tutorial says "click here" while showing a cursor over a button. There is no audio description plan.

Strong answer:

- Recommend integrated description by rewriting narration to name the UI location/control.
- Caption the final narration.
- Include the UI path in a descriptive transcript.
- Consider separate audio description only if integrated description cannot cover essential visual information.

Penalize:

- Only adding captions.
- Describing cursor movement in captions instead of narration/description.

### 9. Localization handoff

Scenario: The user wants Spanish, French, and Japanese subtitles from an English SRT. The source includes product names, UI text, one joke, and two music cues.

Strong answer:

- Prepare localization package: source video, source captions/transcript, glossary/do-not-translate terms, UI text markers, speaker list, audience/tone, locale targets, music/lyrics notes.
- Request separate target-language subtitle files, not a single multilingual file.
- Tell translators to adapt target-language line breaks and reading speed, not copy English cue breaks blindly.
- Distinguish translated subtitles from SDH; include non-speech audio only if SDH-style target captions are requested.
- If dubbing later, regenerate captions from final dubbed audio.

Penalize:

- Machine-translating the SRT directly with no glossary/context.
- Treating all Spanish as one unspecified locale when a locale is needed.

### 10. Podcast recut into video clips

Scenario: A podcast highlight reel uses host audio, guest audio, B-roll, and occasional captions. User asks for "captions and transcript."

Strong answer:

- Identify final audio mix as source of truth.
- Provide full captions with host/guest speaker IDs where needed and meaningful sounds/music.
- Provide a basic transcript for speech/audio; add descriptive transcript if B-roll or on-screen text adds essential meaning.
- Avoid captioning unrelated decorative B-roll as sound; handle visual-only context through transcript/description or narration if needed.

Penalize:

- Captions only the words shown as on-screen pull quotes.
- Ignores speaker changes.

## Applied production tasks

### 11. Caption excerpt repair

User request:

```text
Fix these captions for a 10-second product demo. The audio says:
Narrator: "In the left sidebar, open Automations."
[soft chime]
Narrator: "Choose New rule, then select Slack alert."

Current SRT:
1
00:00:00.000 --> 00:00:05.000
Click here.

2
00:00:03.000 --> 00:00:09.000
choose new rule then select slack alert
```

Expected approach:

- Fix SRT timestamp syntax to comma milliseconds.
- Remove overlapping cues.
- Replace vague "Click here" with actual spoken narration.
- Capitalize product term if appropriate (`Slack`).
- Add meaningful `[soft chime]` only if it matters; in a demo it may be optional unless it confirms action. A strong answer may include it if it signals successful selection.
- Keep cues readable and aligned.

Example strong output:

```srt
1
00:00:00,000 --> 00:00:02,800
In the left sidebar,
open Automations.

2
00:00:02,900 --> 00:00:03,600
[soft chime]

3
00:00:03,800 --> 00:00:07,200
Choose New rule,
then select Slack alert.
```

Scoring:

- 4 points syntax and non-overlap.
- 4 points accuracy to audio.
- 3 points readable line breaks.
- 2 points punctuation/capitalization.
- 2 points sensible treatment of chime.

Critical failure: leaves overlapping cues or changes instruction meaning.

### 12. Audio description mini-plan

User request: "We made a 45-second silent product montage with music and on-screen feature labels. Make it accessible."

Expected answer:

- Captions alone are insufficient because much information is visual/music-only.
- Provide captions/SDH for music and any sound.
- Create descriptive transcript containing feature labels and visual sequence.
- Add audio description or create an alternate narrated/described version; for a silent montage, a narration track may be the clearest access method.
- Ensure on-screen labels have readable contrast and enough dwell time.
- Check flashing/motion intensity.

Penalize:

- Only transcribes the music cue.
- Suggests translating feature labels without audio/description access.

### 13. QA plan for final delivery

User request: "Before I upload this course video to Vimeo, what should you check?"

Expected answer:

- Verify target platform support: Vimeo SRT/WebVTT, UTF-8, type/language label.
- Play final video with captions in Vimeo or a target-equivalent player.
- Check content accuracy, speaker IDs, non-speech audio, timing, no overlaps, line breaks, placement, contrast if burned in, and no obstruction of slides/UI.
- Check transcript/descriptive transcript if provided.
- Confirm audio description/integrated description for visual-only slide content.
- Confirm file naming and locale.

Penalize:

- Only spell-checks the SRT.
- Does not test upload/player behavior.

## Reviewer guidance

A high-scoring agent should sound like a production accessibility lead: specific about deliverables, conservative about legal claims, practical about platform constraints, and attentive to generated-media failure modes. It should not merely list WCAG criteria. It should turn those criteria into a workflow: source prep, authoring, timing, design, localization, QA, and caveats.

Reward answers that:

- Ask for missing target platform/delivery constraints only when necessary, while still giving a useful default.
- Separate "documented requirement" from "production heuristic."
- Include complete mini-examples or file snippets when the task asks for an artifact.
- Push back on inaccessible creative choices without derailing the project.
- Preserve accessibility masters even when the visible deliverable uses social-style burned-in captions.

Penalize answers that:

- Optimize for visual trendiness over readability.
- Rely blindly on ASR or TTS scripts.
- Ignore audio description for visual-only content.
- Collapse localization, captions, subtitles, and transcripts into one file.
- Omit QA against the final upload platform.
