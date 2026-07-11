---
name: podcast-production
description: >-
  Produce audio-first podcast episodes with generative tools — design the show and episode
  format (interview, narrative, news brief, two-host conversational), write scripts for the
  ear, decide between fully-synthetic and hybrid (recorded human + synthetic) production and
  meet the disclosure duty each triggers, cast and direct multi-voice TTS for consistency and
  chemistry, build episode structure (cold open, intro/outro, segments, ad slots), assemble
  and edit, clear music and SFX rights, hit podcast loudness and delivery standards, ship
  metadata/chapters/transcripts through RSS, and pass platform AI-content policy and QA before
  publishing. Use this skill whenever the deliverable is a podcast episode or a podcast show
  bible, or when an agent must make production, rights, disclosure, or delivery decisions for
  spoken-word audio. Not for music tracks, single-voice notification prompts, or video where
  picture leads (route audio-for-video to a video skill).
---

# Podcast production with generative tools

This skill covers producing a finished, publishable podcast episode when some or all of the
audio is machine-generated. It is provider-neutral: it names TTS engines, music libraries, and
hosts only as illustrative options, never as the method. The craft — format design, writing for
the ear, voice direction, structure, rights, loudness, delivery, disclosure, and QA — is the
same regardless of which tool renders the audio.

An episode is *done* when it (1) serves a defined show and audience, (2) sounds intentional and
consistent, (3) uses only audio you have the right to distribute, (4) meets the loudness and
file specs of its target platforms, (5) ships correct RSS metadata plus a transcript, (6)
carries any legally or platform-required AI disclosure, and (7) has passed a listen-through QA.
Skipping any of these is a defect, not a shortcut.

---

## 1. Scope and activation

Use this skill when the task is a spoken-word audio program: a topic explainer show, an
interview series, a daily/weekly news brief, a narrative/documentary episode, a two-host
conversational show, an internal briefing feed, or a show bible/format design for any of those.

Do **not** use it for:

- **Music production** — songs, beds, or stings as the deliverable (that is a music/audio-generation
  concern). This skill *consumes* music and treats it as a rights and loudness problem.
- **A single TTS line** — an IVR prompt, a notification, one voiceover clip with no show context.
- **Video where the picture leads** — if the deliverable is a video and audio is a track under it,
  the video workflow owns pacing and delivery. This skill applies when audio is the product.

If a request is ambiguous ("make an audio version of this article"), confirm whether the output
is a one-off narration or an episode of a show. The two need different structure and metadata.

---

## 2. Format design (do this before writing a word)

The single most consequential early decision is **format**, because format dictates script
style, voice count, structure, and length. Common podcast formats and what each demands
(production heuristic, drawn from standard podcast-production practice — see Sources):

| Format | Typical length | Voices | Script style | Best for |
|---|---|---|---|---|
| **Two-host conversational** | 20–60 min | 2 (chemistry critical) | Outlined, not fully written | Ongoing relationship with audience; opinion/commentary |
| **Interview** | 25–75 min | Host + guest(s) | Host questions scripted; answers live | Expertise, guests, evergreen back-catalog |
| **Solo / monologue** | 5–30 min | 1 | Fully or mostly scripted | Teaching, essays, focused explainers |
| **Narrative / documentary** | 20–45 min | Narrator + tape/characters | Fully scripted, structured in acts | Storytelling, high production value |
| **News brief / daily** | 3–10 min | 1–2 | Tightly scripted, dense | Recurring, time-sensitive, habit-forming |

For a **fully-synthetic** show (every voice is TTS), the interview and two-host formats are the
hardest to make convincing because they depend on turn-taking realism and chemistry; solo,
narrative-narrator, and news-brief formats are the most forgiving. Weigh this when advising a
format for a synthetic show.

Design the **show** once, in a short show bible, before designing episodes:

- **Premise and audience** — one sentence: who it is for and the promise each episode keeps.
- **Cadence and length** — a length band the format supports and a realistic release schedule.
- **Voice identity** — which voice(s), their names/personas, and a locked voice configuration so
  episode N sounds like episode 1 (see §4).
- **Signature elements** — the intro line, the outro/call-to-action, the music theme, and any
  recurring segments. These are the show's "sonic branding" and must be reused verbatim.
- **Disclosure stance** — decided up front (see §6), because it affects the script and metadata.

---

## 3. Writing for the ear

Scripts for audio are not text documents read aloud. The ear has no scrollbar, cannot re-read,
and loses complex clauses. Rewrite prose into speech (production heuristics, widely taught in
podcast scriptwriting — see Sources):

- **Short sentences, one idea each.** Break compound sentences. The listener holds only the last
  clause in memory.
- **Contractions and spoken register.** "It's / you'll / here's," not "it is / you will / here
  is." Write how a competent host actually talks.
- **Front-load the point.** Say the conclusion, then support it. Never bury the payoff behind a
  long subordinate clause.
- **Signpost transitions aloud.** "Three things. First… / But here's the catch… / So what does
  that mean?" These are the audio equivalent of headings.
- **Kill the unpronounceable.** Spell out or rephrase acronyms, symbols, URLs, and numbers.
  "twenty-sixteen L-U-F-S," not "-16 LUFS." "dot com slash join," not "/join."
- **Read it out loud.** Anything that trips a human reader will trip a synthetic voice too and
  will bore a listener. For a synthetic show, read-aloud testing is doubly important because you
  cannot ad-lib a save in post.

**How much to script depends on format.** Fully script the high-risk moments regardless of
format: the hook/cold open, segment transitions, sponsor reads, and the close. For conversational
and interview shows, outline the middle so the talk stays natural. For solo, narrative, and
synthetic shows, script fully — a synthetic voice reads exactly what you give it, so the script
*is* the performance.

When the script is the performance (fully-synthetic), also write **performance direction** into
the script: mark intended pauses, emphasis, and emotional tone per paragraph, because those become
your TTS instructions in §4.

---

## 4. Multi-voice casting and TTS direction

This is the craft that separates a convincing synthetic episode from an obviously robotic one.
The goal is voices that are *distinct from each other*, *consistent across episodes*, correctly
*pronounced*, and — for dialogue — plausibly *reactive to each other*.

### 4.1 Casting and consistency

- **Lock voice configuration per persona.** Save the exact voice identifier plus every generation
  parameter (stability/consistency, similarity, style/expressiveness, speed) as the persona's
  "voice lock." Reuse it for every episode. Voice **drift** — the same nominal voice sounding
  different across episodes or even across a long file — is the top continuity failure in
  synthetic shows (practitioner observation, corroborated across TTS vendor guidance — see Sources).
- **Cast for contrast.** In a two-voice show, pick voices that differ in pitch, pace, and timbre
  so listeners can tell who is speaking without name tags. Two similar voices are worse than one.
- **Segment long scripts by speaker/role** and generate each speaker's lines in that speaker's
  locked config, then assemble. This preserves consistency better than switching voices mid-request
  on engines that support only one primary voice per call.
- **Higher stability/consistency settings reduce drift and expressiveness together.** For a
  narrator that must sound identical for 30 minutes, bias toward stability. For a character that
  needs range, accept more variation and regenerate takes until consistent (heuristic).

### 4.2 Pronunciation control

- **Fix names, jargon, and foreign words explicitly.** Do not hope the model guesses. Use the
  engine's pronunciation mechanism: phoneme markup (IPA or CMU Arpabet via SSML `<phoneme>`), a
  custom pronunciation/lexicon dictionary, or, as a last resort, phonetic respelling in the text
  ("KAI-roh" for "Cairo"). Documented fact: SSML `<phoneme>` supports IPA and CMU Arpabet on major
  engines; some newer expressive models honor a lexicon or respelling but not full SSML — verify
  per engine (verified 2026-07-10 against ElevenLabs, Google Cloud TTS, and Azure Speech docs).
- **Build a per-show pronunciation glossary** in the show bible (recurring names, the show title,
  sponsor names) and apply it every episode so "the host's name" never changes pronunciation.
- **Numbers, dates, units, and symbols** are read inconsistently. Normalize them in the script
  ("July tenth, twenty-twenty-six"), which also helps human clarity.

### 4.3 Emotional pacing and performance

- **Punctuation is your primary pacing tool.** Periods = full stop; commas = short breath;
  ellipses = a hanging pause; question marks lift the final pitch. Sentence length sets rhythm —
  short sentences accelerate, long ones slow down. Around **140–160 words per minute** reads as
  natural, engaged speech (production heuristic — see Sources).
- **Apply emotion at the paragraph/section level, not word-by-word.** Set a tone for a passage;
  use per-word emphasis sparingly. Stacking many emotion directions or switching every sentence
  produces unnatural tonal lurches (practitioner heuristic corroborated across TTS best-practice
  docs — see Sources).
- **Use the engine's expressive controls deliberately:** SSML `<prosody>` (rate/pitch/volume),
  `<break time="…">` for engineered pauses, `<emphasis>`, or an engine's audio/emotion tags. Where
  the engine is prompt-driven rather than SSML-driven, put the direction in a delivery note the
  engine reads. Verify which markup your chosen engine actually honors before authoring — support
  is uneven (verified 2026-07-10).
- **Generate multiple takes and choose.** Synthetic delivery is stochastic; the first take is
  rarely the best. Budget for regeneration.

### 4.4 Host chemistry in generated dialogue

Chemistry between synthetic hosts must be *engineered*, because the voices are generated
independently and do not actually react. Techniques (heuristics):

- **Write the reactions in.** Interruptions ("—wait, say that again"), back-channels ("mm-hm,"
  "right,"), and callbacks to earlier lines. If it is not in the script, it is not in the audio.
- **Vary turn length.** Real conversation is uneven — a long point, a two-word reply. Scripting
  even, equal turns is a tell.
- **Control the seams in assembly.** Turn-taking realism lives in the *gaps*. Tighten or overlap
  the joins between speaker clips so the reply does not sound like it was recorded in a different
  room a week later. Consistent room tone under both voices sells co-presence.
- **Do not fake a live remote.** If you add fake "over the phone" filtering to sell realness, that
  edges toward deception; keep it clearly a produced show.

---

## 5. Episode structure and assembly

### 5.1 Structure

A conventional episode spine (production heuristic; adapt to format):

1. **Cold open (optional, 10–30 s)** — the single strongest moment or hook, before any branding.
   Earns the listen. Strong for narrative and social-clip-driven shows.
2. **Intro / theme (5–20 s)** — show name, host, one-line promise, over the theme music. Keep it
   short and *identical* every episode (sonic branding).
3. **Episode tease** — what this episode delivers, in one or two sentences.
4. **Body / segments** — the content, broken into clearly transitioned segments. Signpost each
   segment change with a spoken transition and, optionally, a short music sting.
5. **Ad slots** — see §5.3. Mark them structurally so they can be inserted/removed or
   dynamically served.
6. **Outro (15–30 s)** — recap, call to action (subscribe/share/link), sign-off, theme out.

Narrative shows use an act structure inside the body (setup → complication/turn → resolution or
open question) rather than flat segments.

### 5.2 Assembly and editing

- **Level the dialogue first**, then place music and SFX under it. Speech intelligibility wins over
  music every time.
- **Duck music under speech** (sidechain or manual automation) so beds sit roughly 12–18 dB below
  the voice during talk and come up in the gaps (heuristic; tune by ear).
- **Trim synthetic artifacts** — clipped word-onsets, unnatural breaths, and swallowed
  syllables are common in TTS. Cut or regenerate the offending line.
- **Consistent room tone / silence** between clips. Dead-digital silence between assembled TTS
  clips sounds unnatural; a low consistent floor reads as one continuous recording.
- **Match levels across segments** so the intro, body, and ads are not wildly different volumes
  before you do the final loudness pass (§7).

### 5.3 Ad slots

- **Baked-in vs. dynamic.** Baked-in ads are part of the file forever; dynamically inserted ads are
  stitched at request time by the host and can be updated or removed. If the show will run ads long
  term, structure the timeline with clean, silent insertion points so ads can be dynamic.
- **Disclosure carries into ads.** A synthetic-voice ad read, or an AI-generated endorsement, may
  trigger the same disclosure and consent duties as the show (see §6), plus advertising-law rules
  about endorsements. Never synthesize a real person appearing to endorse something without rights.

---

## 6. Fully-synthetic vs. hybrid, and the disclosure duty

### 6.1 The production decision

- **Fully-synthetic** — every voice is TTS. Cheapest and fastest to iterate; best for solo,
  narrative-narrator, and news-brief formats; weakest for spontaneity and true interview dynamics.
- **Hybrid** — recorded human voice(s) plus synthetic segments (e.g., a real host with a synthetic
  co-host, synthetic narration around recorded interview tape, or synthetic reconstruction of
  unavailable audio). Best of both, but multiplies the rights and disclosure surface: every
  recorded human needs a release, and every synthetic voice needs a licensed/consented source.

Choose hybrid when the show needs a real human's authority, spontaneity, or an actual guest, and
fully-synthetic when scale, consistency, or cost dominate and the format tolerates it.

### 6.2 Disclosure and consent obligations

Treat these as **requirements**, not style choices. They are the highest-risk part of a synthetic
podcast.

- **Voice cloning requires documented consent from the voice owner.** Cloning or replicating a
  real person's voice without permission exposes you to right-of-publicity and voice-rights
  liability. As of 2026 multiple U.S. states protect voice as a distinct likeness right — Tennessee's
  **ELVIS Act** (effective 2024) is the first to name AI voice replicas explicitly, and California,
  Illinois, New York and others have related statutes; the federal **TAKE IT DOWN Act** (signed May
  2025) targets nonconsensual synthetic depictions (documented fact, verified 2026-07-10 — see
  Sources; not legal advice — confirm current law for your jurisdiction and use). **Consent must be
  specific, written, and documented; a verbal "yes" does not meet the bar.** Never clone a public
  figure, a guest, or a co-host's voice without a signed release scoped to the use.
- **Platform AI-disclosure policies apply to synthetic voices** (documented facts, verified
  2026-07-10):
  - **YouTube** requires creators to disclose *realistic* altered or synthetic content at upload,
    explicitly including synthetic/cloned voices and AI voiceovers that could mislead a viewer into
    thinking a real person spoke. A "How this content was made" label may be shown. Mass-produced,
    low-effort AI content risks demonetization under 2025 monetization updates.
  - **Spotify** does not down-rank AI-assisted content per se but bans unauthorized voice clones,
    aggressively removes spam/low-quality mass-produced audio, and is adopting a DDEX-based AI
    disclosure standard surfaced in-app. Its "Verified" program excludes profiles that primarily
    represent AI personas.
  - **Apple Podcasts** does not currently mandate a generic "this is AI" label for synthetic voices
    in the base RSS spec, but its content policies still prohibit impersonation and require rights
    to all audio. (Verify current policy at publish time — platform policy is volatile.)
- **When in doubt, disclose.** A brief, honest note ("voices in this episode are AI-generated" in
  the show notes and/or a spoken line) is cheap insurance and increasingly expected. Regulatory
  momentum (e.g., transparency laws emerging in 2025–2026) is toward *more* mandatory disclosure,
  not less.
- **Hybrid shows: label which parts are synthetic** if a listener could otherwise be deceived about
  a real person's words — for example, a synthetically reconstructed quote must be marked as a
  recreation, never presented as authentic tape.

---

## 7. Loudness and delivery standards

This is a hard-numbers area. Get it wrong and platforms turn your show up or down, or reject it.

### 7.1 The target

**Documented facts (verified 2026-07-10):**

- **Apple Podcasts** recommends preconditioning so overall loudness is **around -16 dB LKFS
  (= LUFS) with ±1 dB tolerance**, and **true peak ≤ -1 dB FS**, measured per ITU-R BS.1770.
  (LKFS and LUFS are the same unit.)
- **The commonly cited creator targets are -16 LUFS for a stereo file and -19 LUFS for a mono
  file.** The mono figure is lower on purpose: a mono file played through a stereo player is
  perceived roughly 3 LU quieter, so mastering a mono file to ~-19 LUFS makes it *sound* like a
  -16 LUFS stereo file. (Production heuristic reconciling the two numbers; the ~2–3 LU
  perceptual offset is documented in AES TD1008 — see Sources.)
- **Spotify** normalizes podcasts to **-14 LUFS** at playback with a -1 dBTP ceiling; **YouTube**
  normalizes toward roughly -14 LUFS as well. These platforms apply gain at playback rather than
  re-encoding your file.
- **AES TD1008 (2021, supersedes TD1004)** — the streaming-loudness recommendation — sets a
  **distribution** target of **-18 LUFS for speech/"assorted" content** and advises keeping
  integrated loudness **above -20 LUFS**; it notes speech is perceived ~2–3 LU louder than music at
  the same measured loudness. Note this is guidance for the *distributor's normalization*, not the
  creator's master file.

**Practical resolution (heuristic):** Master **one stereo file to -16 LUFS integrated, true peak
≤ -1.0 dBTP** as the portable default that sits inside Apple's window and is only gently adjusted
by Spotify/YouTube. If delivering **mono**, target **-19 LUFS** for equivalent perceived loudness.
Never chase Spotify's -14 by squashing dynamics — platforms turn quiet content *up*; loud, over-
limited content cannot be turned back down cleanly and sounds fatiguing. Preserve dialogue dynamic
range; a spoken-word show does not need to be as loud as a mastered song.

### 7.2 File and encoding specs

**Documented facts — Apple Podcasts (verified 2026-07-10):**

- **RSS-delivered episode audio:** MP3 or AAC. Mono **64–128 kbps**, stereo **128–256 kbps**, at
  44.1/48 kHz.
- Spoken-word content is often fine in **mono** — smaller files, and most listening is on a single
  speaker or earbud. Reserve stereo for shows with meaningful music/SFX staging.
- Loudness is set *before* encoding: lossy compression does not change measured loudness, so
  precondition first, then encode.
- (Apple's high-resolution WAV/FLAC specs apply to subscriber audio uploaded to Podcasts Connect,
  not to the public RSS enclosure.)

Deliver a single file per episode via the `<enclosure>` in the RSS item (URL + byte length + MIME
type, all three required).

---

## 8. Metadata, chapters, transcripts, and RSS

A podcast *is* an RSS feed; the audio is just the enclosure. Getting the feed right is as much of
the deliverable as the audio (documented facts about the spec, verified 2026-07-10 — see Sources).

- **Feed-level required elements:** title, description, language, at least one `<itunes:category>`,
  `<itunes:explicit>`, artwork (Apple requires cover art typically 1400×1400 to 3000×3000 px, RGB
  JPEG/PNG), and an owner/contact. Missing `<itunes:explicit>` or `<itunes:category>` gets a feed
  rejected by Apple.
- **Episode-level required elements:** title, a `<enclosure>` (URL, length in bytes, MIME type), a
  **globally unique `<guid>` that never changes**, and a publish date. Changing a GUID duplicates
  the episode for subscribers.
- **Chapters** — two mechanisms: (a) embedded in the file (ID3v2 `CHAP` frames in MP3, MP4 `chpl`
  atoms in M4A), or (b) linked from the feed via the Podcasting 2.0 `<podcast:chapters>` tag
  pointing to an external JSON chapters file. Chapters improve navigation and are surfaced by
  several clients.
- **Transcripts** — the Podcasting 2.0 `<podcast:transcript>` element links a transcript file from
  the RSS item. **WebVTT (`.vtt`) is the preferred format** because it supports speaker labels
  (via cue identifiers), timing, and light styling, and has the widest client support; SRT is
  accepted but simpler. Major clients (Apple, and Spotify as of late 2025) render feed-linked
  transcripts. For a **synthetic** show you effectively have the transcript already — it is your
  script — so shipping one is nearly free and removes any excuse not to.
- **Namespaces:** declare the `itunes` and `podcast` (Podcasting 2.0) namespaces in the feed to use
  those tags; validate the feed before publishing.

---

## 9. Accessibility

- **Ship a transcript for every episode.** It is the core accessibility feature of podcasting — it
  serves Deaf and hard-of-hearing listeners, improves discoverability/SEO, and is trivially cheap
  for a synthetic show (your script). Link it via `<podcast:transcript>` (§8).
- **Speaker-labeled transcripts** (WebVTT cue identifiers) matter for multi-voice shows so a reader
  can follow who said what.
- **Clear show notes** with a summary, key timestamps/chapters, and link text that makes sense out
  of context.
- **Avoid audio-only information that a transcript cannot carry** — if a laugh, tone, or sound is
  load-bearing for meaning, note it in the transcript ("[laughs]", "[phone rings]").

---

## 10. Rights and safety checklist

Every audio element must be one of: original, licensed for this use, or public-domain/appropriately
Creative-Commons-licensed with attribution honored.

- **Music.** You need rights to *both* the composition and the specific recording (master). Buying a
  song, or a personal streaming subscription, does **not** grant podcast/sync rights. Use a
  royalty-free / production-music library license that explicitly covers podcasts, a direct sync
  license from the rights holders, or genuinely license-clear music. "Royalty-free" means one fee,
  not free-of-charge, and not free-of-license-terms — read the license scope (episodes covered,
  ad-supported use, term) (documented fact — see Sources).
- **Sound effects** — same principle; use SFX libraries whose license covers commercial podcast
  distribution.
- **Voices** — every recorded human needs a release; every cloned/synthetic voice needs a licensed
  or consented source and must respect the TTS provider's commercial-use terms (some voices/tiers
  are non-commercial). Re-confirm the provider grants you rights to *distribute* generated audio
  commercially.
- **Third-party audio / clips** — quoting tape, songs, or another show requires permission or a
  valid fair-use/fair-dealing basis; do not assume short clips are automatically fine.
- **Disclosure/consent** for synthetic and cloned voices — see §6. This is the one that creates
  legal exposure, not just a takedown.

---

## 11. Pre-publish QA (do not skip)

Run this before every release. A synthetic show especially needs a human (or careful agent)
listen-through, because generation errors are silent until you hear them.

1. **Full listen-through** end to end, at listening volume, on earbuds. Catch mispronunciations,
   voice drift, clipped words, robotic seams, awkward pacing, and level jumps.
2. **Pronunciation check** against the show glossary — every name, the show title, the sponsor.
3. **Structure check** — intro/outro present and identical to prior episodes; segments transition;
   ad slots correct; cold open lands.
4. **Loudness/peak verification** with a meter — integrated LUFS at target (~-16 LUFS stereo /
   ~-19 LUFS mono), true peak ≤ -1 dBTP, no clipping (§7).
5. **Encoding/format** — correct codec, bitrate, channels, sample rate; file plays on a phone.
6. **Metadata** — title, unique unchanged GUID, description, chapters, correct enclosure length in
   bytes, artwork, categories, explicit flag (§8).
7. **Transcript** attached, accurate, speaker-labeled (§9).
8. **Rights** — every music/SFX/voice element cleared (§10).
9. **Disclosure** — AI/synthetic disclosure present where required by law or platform, and consent
   on file for any cloned voice (§6).
10. **Feed validation** — run the feed through a validator; confirm it parses before it goes live.

---

## 12. Worked examples

The following are **illustrative examples**, not mandatory templates. They show how the decisions
above compose on a real brief. Adapt the specifics.

### Example A — Fully-synthetic daily 5-minute news brief

**Intent:** A recurring weekday "3-minute-ish" brief summarizing one industry's news, single
synthetic host, published to Apple/Spotify/YouTube.

**Format & bible:** News-brief format (forgiving for synthetic). One host persona "Ava," a
mid-pitch, steady voice locked at high stability (news must sound identical daily). Glossary of
recurring company and person names with phoneme entries. Fixed 8-second music intro, 6-second
outro with a "subscribe" CTA. Disclosure stance: state "This is an AI-generated briefing" in the
show description and once in the outro.

**Script (writing for the ear), abridged:**

```
[COLD OPEN — no music]
Three things moved the market today, and the third one nobody saw coming.

[THEME 8s, duck under]
This is The Daily Brief for Tuesday, July eighth. I'm Ava. Here's what matters.

[BODY]
First. [company], read "ACK-mee", reported earnings after the bell...
(short sentences. One idea each. A pause... before the turn.)

[OUTRO, theme up]
That's your brief. Follow the show so tomorrow's finds you automatically.
This is an AI-generated briefing from [publisher]. See you tomorrow.
```

**TTS direction:** Generate the whole body in Ava's lock. Emotion at paragraph level: neutral-
authoritative for the body, a lift on the outro CTA. Numbers/dates spelled out in the script. Two
takes per day; pick the cleaner. **Loudness:** master mono to -19 LUFS, TP ≤ -1 dBTP; encode MP3
mono 96 kbps 44.1 kHz. **Delivery:** unique GUID per day; `<podcast:transcript>` VTT built from the
script; chapters unnecessary at this length. **Disclosure:** in description + spoken outro (covers
YouTube's synthetic-voice disclosure and general transparency).

**Likely failure modes:** drift if the voice lock is not reused; "ACK-mee" reverting to a spelling
pronunciation without the phoneme entry; over-limiting to chase Spotify's -14 and sounding harsh.

### Example B — Hybrid two-host conversational tech show

**Intent:** Weekly 35-minute show. One **real** human host (recorded) plus one **synthetic** co-host
persona. This is the hard case: chemistry and disclosure both matter.

**Decision:** Hybrid, because the human brings spontaneity/authority and the synthetic co-host adds
a consistent "explainer" foil cheaply. **Consent/rights:** the synthetic co-host uses a voice the
producers **licensed for commercial use** (documented, provider terms confirmed); if it were modeled
on any real person, a signed release would be mandatory — it is not, it is a wholly synthetic
persona. **Disclosure:** the synthetic co-host is introduced honestly as an AI co-host in episode 1
and in every show description; a "How this content was made" disclosure is toggled on at YouTube
upload because a synthetic voice is present.

**Chemistry engineering:** The human's side is recorded live around a scripted skeleton. The
synthetic co-host's lines are written to *react* — interruptions, back-channels ("right, right"),
callbacks to what the human just said — then generated in the co-host's voice lock and edited into
the gaps with matched room tone so the exchange sounds co-present. Turn lengths are deliberately
uneven.

**Assembly & loudness:** Level both voices to match, duck the bed 12–15 dB under talk, master
**stereo to -16 LUFS**, TP ≤ -1 dBTP; encode AAC stereo 128 kbps. **Delivery:** chapters (JSON via
`<podcast:chapters>`) for the segment structure; speaker-labeled WebVTT transcript distinguishing
the human host and the AI co-host; clean silent ad-insertion points for dynamic ads.

**Likely failure modes:** the synthetic replies sounding recorded "elsewhere" (fix room tone and
tighten seams); even, equal turn lengths reading as fake; forgetting the platform AI-disclosure
toggle; the synthetic co-host reading a sponsor endorsement without the extra care ad reads require.

### Example C — Narrative documentary episode with reconstructed audio

**Intent:** A 30-minute story where an unavailable historical quote is voiced synthetically.

**The critical rule:** A synthetically reconstructed voice or quote **must be disclosed as a
recreation** — never presented as authentic archival tape. Mark it in the narration ("what follows
is an AI re-creation of the words in the letter, not a recording") and in the transcript. Cloning a
specific real person's voice would additionally require rights/consent from their estate; a neutral
"reader" voice avoids that and is the safer choice unless rights are secured. Everything else
follows the narrative act structure (§5.1), full scripting (§3), and the standard rights, loudness
(-16 LUFS stereo), transcript, and QA passes.

---

## Sources

Volatile facts (platform specs, policies, laws) verified **2026-07-10**. Standards and craft
heuristics are labeled inline. Do not treat legal notes as legal advice; confirm current law and
policy at publish time.

**Standards & loudness**
- Apple Podcasts — Audio requirements (formats, bitrates, -16 dB LKFS ±1, -1 dB FS true peak):
  https://podcasters.apple.com/support/893-audio-requirements
- AES TD1008 (2021), *Recommendations for Loudness of Internet Audio Streaming and On-Demand
  Distribution* (supersedes TD1004; -18 LUFS speech, keep above -20 LUFS, speech ~2–3 LU louder
  than music): https://aes2.org/wp-content/uploads/2024/01/20210924_TD1008_v3.13.pdf and
  https://aes.org/technical-council/technical-document-aestd1008/
- Production Advice, summary of AES TD1008: https://productionadvice.co.uk/td1008/
- Spotify — Loudness normalization (-14 LUFS, -1 dBTP):
  https://support.spotify.com/us/artists/article/loudness-normalization/

**RSS / metadata / transcripts / chapters**
- Apple Podcasts — Podcast RSS feed requirements:
  https://podcasters.apple.com/support/823-podcast-requirements
- Podcasting 2.0 / Podcast Namespace spec (transcript, chapters, etc.):
  https://podcasting2.org/docs/podcast-namespace/1.0 and
  https://github.com/Podcast-Standards-Project/PSP-1-Podcast-RSS-Specification

**Platform AI-content policies**
- YouTube — Disclosing altered or synthetic content (blog):
  https://blog.youtube/news-and-events/disclosing-ai-generated-content/ ; "How this content was
  made" help: https://support.google.com/youtube/answer/15447836
- Spotify — verification/AI-persona and spam enforcement (secondary, practitioner reporting):
  https://www.musicbusinessworldwide.com/spotify-extends-verified-by-spotify-badges-to-podcasts-further-cracking-down-on-ai-impersonators/

**Voice rights & disclosure law (not legal advice)**
- Tennessee ELVIS Act overview (Art and Media Law): https://artandmedialaw.com/elvis-act/
- Right-of-publicity / voice-cloning risk map (Holon Law):
  https://holonlaw.com/entertainment-law/synthetic-media-voice-cloning-and-the-new-right-of-publicity-risk-map-for-2026/
- Deepfake & AI voice-cloning laws by state (Recording Law):
  https://www.recordinglaw.com/us-laws/deepfake-laws/

**TTS direction (best-practice docs, provider-neutral synthesis)**
- ElevenLabs — Text-to-speech best practices:
  https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
- Microsoft Azure — SSML voice/prosody/phoneme reference:
  https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-voice
- Google Cloud Text-to-Speech — SSML reference:
  https://docs.cloud.google.com/text-to-speech/docs/ssml

**Music/SFX rights (practitioner references)**
- The Podcast Haven — How to license music for a podcast:
  https://thepodcasthaven.com/how-to-license-music-for-a-podcast/
- Art and Media Law — Podcast music licensing: https://artandmedialaw.com/podcast-music-licensing/

**Format, structure & scriptwriting (practitioner references)**
- Buzzsprout — How to write a podcast script: https://www.buzzsprout.com/blog/write-podcast-script-examples
- Riverside — Podcast structure: https://riverside.com/blog/podcast-structure
- Podnews — LUFS/LKFS for podcasters: https://podnews.net/article/lufs-lkfs-for-podcasters
