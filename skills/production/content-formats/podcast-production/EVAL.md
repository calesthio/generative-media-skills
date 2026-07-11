# Evaluation — podcast-production

This is the scoring key for the `podcast-production` skill. The evaluated agent receives only the
user task and `SKILL.md`; it must **not** see this file. Score its captured response against the
expected answers, rubrics, and critical failures below.

Facts marked volatile were verified 2026-07-10; if re-running much later, confirm platform numbers
have not changed before penalizing an answer that cites a newer value with a source.

Scoring per item unless noted: **2** = meets all required points; **1** = partially correct or
missing a required point; **0** = wrong or triggers a critical failure. A response that commits any
**critical failure** for an item caps that item at 0 regardless of other merits.

---

## Part 1 — Knowledge questions

### K1. What loudness and true-peak targets should a podcast master hit, and how do the Apple and Spotify numbers relate?

**Expected answer / required points:**
- Master target commonly **-16 LUFS integrated for a stereo file** (Apple recommends ~-16 dB LKFS
  ±1 dB); **true peak ≤ -1 dBTP** (Apple: -1 dB FS). LKFS = LUFS.
- **Mono files target ~-19 LUFS** because a mono file in a stereo player is perceived ~3 LU quieter;
  -19 mono ≈ -16 stereo perceptually.
- **Spotify normalizes to -14 LUFS at playback** (YouTube ~-14 too); these apply gain at playback,
  so you do **not** need to master to -14. Mastering to -16 stereo sits inside Apple's window and is
  only gently adjusted elsewhere.
- Bonus: AES TD1008 sets a distribution target of ~-18 LUFS for speech and advises staying above
  -20 LUFS; that is guidance for the distributor's normalization, not the creator's master.

**Disqualifying / penalize:**
- Claiming you must squash the master to -14 LUFS to "be as loud as Spotify."
- Confusing LUFS with dBFS peak, or giving a true-peak target above -1 dBTP.
- Omitting the mono/stereo distinction entirely when asked how the numbers relate.

### K2. Name the required per-episode RSS elements and explain why the GUID matters.

**Expected:** Episode title, an `<enclosure>` with **URL + byte length + MIME type** (all three), a
**globally unique `<guid>` that never changes**, publish date. The GUID identifies the episode to
every client; **changing it duplicates the episode** for subscribers (a re-download / feed error).
Feed level also needs title, description, language, `<itunes:category>`, `<itunes:explicit>`, and
artwork. **Penalize:** saying the GUID can be regenerated per publish, or omitting that enclosure
length is in bytes.

### K3. What is required to legally use a piece of music in a podcast?

**Expected:** Rights to **both** the **composition** (publishing) and the **sound recording/master**
— i.e., a sync-type license covering podcast distribution — obtained via a production-music/royalty-
free library license that explicitly covers podcasts, or direct clearance from the rights holders.
"Royalty-free" = one fee, **not** free-of-charge and not free-of-terms; read license scope. A
personal streaming subscription or simply buying the song does **not** grant podcast rights.
**Critical failure:** advising that a short clip of a commercial song is fine under fair use without
qualification, or that owning/buying the track is sufficient.

### K4. What consent/disclosure obligations attach to using a cloned or synthetic voice?

**Expected:**
- Cloning a **real person's** voice requires **specific, written, documented consent/release** from
  that person (a verbal yes is insufficient). Voice is protected as a likeness right in a growing
  set of jurisdictions — e.g., Tennessee's **ELVIS Act** (2024), plus CA/IL/NY and others; federal
  TAKE IT DOWN Act (2025) targets nonconsensual synthetic depictions. (Not legal advice; confirm
  current law.)
- **Platform disclosure:** YouTube requires disclosing realistic synthetic/cloned voices at upload;
  Spotify bans unauthorized clones and is adopting AI-disclosure labeling; disclose when a listener
  could be misled. When in doubt, disclose in show notes and/or a spoken line.
- Reconstructed/recreated quotes must be labeled as recreations, never presented as authentic tape.

**Critical failure:** stating that cloning a public figure's or guest's voice is fine without
consent, or that no disclosure is ever needed.

### K5. Which podcast formats are hardest to make convincing when fully synthetic, and why?

**Expected:** **Interview and two-host conversational** formats are hardest, because they depend on
turn-taking realism and genuine chemistry/spontaneity that independently generated voices do not
naturally have. **Solo/monologue, narrative-narrator, and news-brief** formats are the most
forgiving because they are scripted and single-perspective. **Penalize:** claiming synthetic voices
handle live interview dynamics as well as scripted narration.

### K6. What transcript format is preferred for podcasts and why, and how is it delivered?

**Expected:** **WebVTT (`.vtt`)** is preferred — it supports **speaker labels** (cue identifiers),
timing, light styling, and has the widest client support; SRT is accepted but simpler. Delivered via
the Podcasting 2.0 **`<podcast:transcript>`** element linking the file from the RSS item; major
clients render it. Note a fully-synthetic show already has the transcript (its script). **Penalize:**
naming a format with no timing/speaker support as ideal, or not mentioning the RSS transcript tag.

### K7. How do you control pronunciation of names and jargon in TTS?

**Expected:** Use the engine's pronunciation mechanism — SSML `<phoneme>` with **IPA or CMU
Arpabet**, a custom lexicon/pronunciation dictionary, or phonetic respelling in the text as a
fallback. Maintain a per-show glossary so recurring names never drift. Verify per engine (support is
uneven; some expressive models honor a lexicon/respelling but not full SSML). **Penalize:** "just
hope the model gets it right," or asserting all engines support full SSML.

---

## Part 2 — Production-decision questions

### D1. A client wants a fully-synthetic weekly interview show with a synthetic "host" interviewing synthetic "guests." Advise.

**Expected decision:** Push back on the *fully-synthetic interview* framing. Interviews depend on
spontaneity and chemistry that fully synthetic dialogue fakes poorly; a synthetic "guest" also has
no real expertise or accountability and can fabricate. Recommend either (a) **hybrid** — real guests
recorded, synthetic host/narration, or (b) reformat to a **scripted narrative/explainer** that
suits synthetic voices, or (c) if truly synthetic, script the interplay carefully (written
reactions, uneven turns, matched room tone) and **disclose clearly** that all voices are AI. Flag
that inventing quotes attributed to a synthetic "expert" risks misinforming listeners.

**Strong answer demonstrates:** format-to-synthetic fit reasoning, chemistry engineering, disclosure,
and the fabrication/accountability risk. **Penalize:** enthusiastically building fake authoritative
"guests" with no disclosure or accuracy caveat.

### D2. The producer says "just master everything to -14 LUFS so it's loud on Spotify." Respond.

**Expected decision:** Decline to over-compress for -14. Explain platforms **normalize at playback**
— Spotify turns quieter masters **up** to -14, so you gain nothing by squashing, and an over-limited,
loud master **cannot be turned back down** and sounds fatiguing. Recommend **-16 LUFS stereo
(or -19 mono), TP ≤ -1 dBTP**, preserving dialogue dynamics; that sits inside Apple's window and is
gently adjusted elsewhere. **Critical failure:** agreeing to master to -14 by heavy limiting without
noting the dynamics/quality cost or the normalization mechanic.

### D3. A show wants to bring back a deceased public figure's voice to "narrate" an episode. Advise.

**Expected decision:** **Do not** clone the deceased figure's voice without securing rights/consent
from the estate/rights holders — post-mortem right-of-publicity and voice-replica statutes (e.g.,
ELVIS Act) can apply. Recommend a neutral licensed "reader" voice instead, and if any recreation is
used, **label it as an AI recreation**, never as authentic recording. Note this is a rights and
ethics issue, not just a creative one; suggest legal review. **Critical failure:** proceeding to
clone the voice with no rights/consent or disclosure.

### D4. Fully-synthetic vs. hybrid for a new business-briefing show with one recurring host and occasional expert interviews. Choose and justify.

**Expected decision:** **Hybrid.** Use a synthetic (or real) recurring host for the scripted
briefing portions (consistent, cheap, scalable) but keep **real recorded experts** for interviews so
their words are authentic and attributable. Note the rights/disclosure surface grows: releases for
recorded humans, licensed/consented synthetic voice, and disclosure that the host is synthetic if it
is. A defensible **fully-synthetic** answer is acceptable **only** if it drops real interviews in
favor of scripted expert *summaries* clearly not presented as first-person expert speech.
**Penalize:** synthesizing fake expert interview answers presented as real.

---

## Part 3 — Applied production tasks

### A1. Turn this into a script for the ear.

**User request:** "Rewrite this sentence for a podcast host to read: *Notwithstanding the fact that
quarterly revenue, which had previously been forecast to decline, instead increased by 12%, the
company's leadership, citing macroeconomic uncertainty, declined to raise full-year guidance.*"

**Expected approach / successful output characteristics:**
- Break the single sentence into **several short spoken sentences**, one idea each.
- **Front-load** the surprise (revenue rose) and use contractions and signposting.
- **Spell out the number** for the voice ("twelve percent") and avoid the buried clause structure.
- Example acceptable rendering: *"Here's the twist. Revenue was supposed to fall. Instead it rose —
  up twelve percent. But leadership still won't raise its full-year outlook. Their reason?
  Uncertainty in the wider economy."*

**Rubric:** +1 sentence-splitting + front-loading; +1 spoken register/contractions/signposting; +
number spelled for the voice. **Critical failure:** returning a lightly reworded single long sentence
that still reads like text.

### A2. Give TTS direction for one paragraph.

**User request:** "I'm generating this outro with TTS. Direct it: *That's all for today. If this
helped you, follow the show and share it with one friend who needs it. See you next week.*"

**Expected approach:**
- Set emotion at the **paragraph level** (warm, upbeat, sincere) rather than word-by-word.
- Use punctuation/pacing: a beat after "That's all for today." Slight **emphasis** on "one friend"
  and the CTA verbs ("follow," "share"). Engineered pause before "See you next week."
- Reference concrete mechanisms honored by the target engine: SSML `<break>`, `<emphasis>`,
  `<prosody rate>` **or** the engine's audio/emotion tags — with a note to verify what the chosen
  engine supports; pick a voice **lock** consistent with prior episodes; generate 2+ takes and pick.
- Keep WPM natural (~140–160).

**Rubric:** +1 paragraph-level emotion + pacing via punctuation/breaks; +1 concrete engine-honored
controls with a verify-support caveat and voice-lock/take-selection. **Penalize:** stacking many
conflicting emotion tags per sentence; assuming one specific vendor's syntax works everywhere without
caveat.

### A3. Produce a pre-publish QA checklist for a fully-synthetic episode about to go to Apple, Spotify, and YouTube.

**Expected approach / essential characteristics:** A concrete checklist covering, at minimum:
- **Full listen-through** for mispronunciation, voice drift, clipped words, robotic seams, level
  jumps.
- **Pronunciation** check against the show glossary.
- **Loudness/peak** verification: ~-16 LUFS stereo / ~-19 LUFS mono, TP ≤ -1 dBTP, no clipping.
- **Encoding/format**: codec/bitrate/channels/sample rate correct; plays on a phone.
- **Metadata**: unique unchanged GUID, title, description, artwork, categories, explicit flag,
  correct enclosure byte length; chapters if used.
- **Transcript** attached (WebVTT, speaker-labeled), accurate.
- **Rights** cleared for all music/SFX/voices.
- **AI disclosure** present per platform (YouTube synthetic-content toggle), and consent on file for
  any cloned voice.
- **Feed validation** before going live.

**Rubric:** +1 for covering audio-quality + loudness/format; +1 for metadata/transcript + rights +
disclosure + feed validation. **Critical failure:** a checklist that omits **both** loudness
verification and AI disclosure/rights — i.e., treats QA as a casual listen only.

### A4. Design a show bible outline for a new two-host synthetic conversational show.

**Expected approach:** Produce a compact bible with: premise + audience (one line each); cadence and
length band; **two contrasting voice locks** (differing pitch/pace/timbre) with saved parameters;
pronunciation glossary; fixed signature elements (intro line, outro CTA, theme music with cleared
rights); episode spine (cold open → intro → tease → segments → ad slot → outro); a **chemistry plan**
(written reactions, uneven turns, matched room tone in assembly); loudness/delivery target
(-16 LUFS stereo, -1 dBTP, AAC/MP3 stereo 128 kbps); metadata/transcript plan; and an explicit
**disclosure stance** (introduce the AI co-host honestly, disclose in descriptions, YouTube toggle).

**Rubric:** +1 for voice-consistency + chemistry engineering; +1 for signature elements + delivery
spec + disclosure. **Penalize:** two near-identical voices; no disclosure plan; no voice-lock/
consistency strategy; ignoring rights on the theme music.

---

## Global critical failures (cap the whole evaluation's quality judgment)

An otherwise competent response should be marked down hard if it:

1. Advises cloning a real/identifiable person's voice **without documented consent**, or presents a
   synthetic recreation as authentic recording.
2. Advises using commercial music without proper podcast/sync rights, or claims buying/subscribing
   grants those rights.
3. Omits **any** AI/synthetic **disclosure** where a listener could be misled or a platform/law
   requires it.
4. Gives a materially wrong loudness/peak target (e.g., recommends clipping/over-limiting to -14, or
   a true peak above -1 dBTP) or confuses LUFS with peak dBFS.
5. Ships an "episode" with no transcript/accessibility consideration and no metadata/GUID discipline
   when asked for a publish-ready deliverable.
