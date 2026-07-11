---
name: audiobook-production
description: >-
  Produce full-length audiobooks and long-form narration with generative voice
  tools. Use when the task is to turn a manuscript or long text into hours of
  spoken audio: preparing the manuscript for narration (front/back matter,
  footnotes, tables, dialogue), casting a single narrator or full cast,
  controlling pronunciation and voice consistency across a whole book, running a
  proofing/QC listen, meeting a retailer's technical delivery specs (RMS, peak,
  noise floor, room tone, chapterized files, metadata), and choosing a
  distribution route under each platform's current AI-narration policy. Not for
  short TTS clips, single-line voiceover, podcast production, or captioning
  existing video.
---

# Audiobook production

An audiobook is not a long TTS clip. It is a **structured deliverable of many
chapterized files**, each of which must pass an automated loudness/noise gate,
carry the right metadata, and sound like the same performer that opened Chapter
1. The problems that dominate this work — voice drift over ten hours, a proper
noun mispronounced 40 times, a footnote that makes no sense read aloud, a file
rejected for a -58 dB noise floor, a platform that silently bans AI narration —
do not exist in short-clip synthesis. This skill is about managing hour-scale
production, not about generating one good sentence.

This is a **craft skill, provider-neutral**. Generative voice tools are
referenced by capability (pronunciation lexicon, SSML support, seed/consistency
control, per-chapter regeneration), not by brand. Specific tools and retail
platforms are named only as illustrative examples or as dated policy facts.

Labels used below:

- **[Fact]** — documented in a primary/official source, cited.
- **[Standard]** — an established industry technical standard.
- **[Heuristic]** — a production judgment that experienced producers use; not a rule.
- **[Policy — dated]** — a volatile platform policy verified on the stated date.

---

## 1. Decide the production route first

Three routes exist, and they diverge on cost, rights, quality ceiling, and where
you can sell. Pick before touching the manuscript, because the route changes how
you prepare it.

1. **Human narration** — a person performs the book. Highest quality ceiling,
   required by some retailers, needs a performer and studio-grade audio.
2. **Author/producer-driven generative narration** — you supply the text to a
   TTS system, tune pronunciation and pacing, and master the output yourself.
   You control every file and can distribute the finished audio wide.
3. **Platform auto-narration** — a retailer generates the audiobook from your
   ebook inside their walled system (e.g., Amazon's Virtual Voice, Google Play
   Books auto-narration, Apple Books digital narration). Lowest effort, least
   control, and distribution is often tied to that platform.

The rest of this skill mostly serves route 2 (the one where an agent does real
production work) and gives route-3 platform facts in §10.

---

## 2. Prepare the manuscript for narration

Print text is written to be *seen*. Narration text must work when *heard*, with
no page to glance back at. Preparing the manuscript is where most audiobook
quality is won or lost, and it is entirely upstream of the voice tool.

### Front and back matter — decide, don't default

[Heuristic] Treat each front/back-matter element as a separate short segment and
make an explicit include/omit decision:

- **Title page / copyright** — usually spoken briefly. Accessibility-focused
  production (see §12) narrates copyright, title, and section labels in full;
  commercial retail production often compresses them. [Fact] Accessibility
  guidance is to begin each section by speaking its title ("Copyright", "Chapter
  One"). ([NNELS accessibility guidelines](https://nnels.ca/accessibility-guidelines-audiobook-narrators), verified 2026-07-10)
- **Dedication, epigraph, acknowledgements, also-by lists** — short standalone
  segments if kept; frequently omitted from commercial audio. Decide per title.
- **Opening/closing credits** — retail platforms expect them (see §9). Opening
  credits state title, author, narrator; closing credits signal finality
  ("You have been listening to…" then title/author/narrator, then "The End").

### Footnotes and endnotes — the hardest call in nonfiction

[Heuristic] A footnote read aloud mid-sentence derails the listener because there
is no visual marker for "this is an aside." For each note, choose one of:

- **Fold into the sentence** — rewrite so the note's essential fact becomes part
  of the spoken prose.
- **Read in place, clearly bracketed** — introduce it audibly ("In a footnote,
  the author adds…") so the listener knows it is an aside.
- **Batch at end of chapter/section** — collect notes and read them together.
- **Drop** — citation-only notes (page numbers, ibid., bare URLs) usually add
  nothing in audio and are cut.

For scholarly/accessibility editions the default flips toward *including* notes
and bibliographies so the audio carries all the print information. ([NNELS](https://nnels.ca/accessibility-guidelines-audiobook-narrators), verified 2026-07-10)

### Tables, figures, charts, images — rewrite or cut

[Heuristic] A narrator cannot read a chart. Flag everything that depends on the
reader *seeing* it — tables, graphs, figures, image captions, sidebars, complex
formatting. For each: extract the essential finding as one or two spoken
sentences ("Table 3 shows sales roughly doubling each year from 2020 to 2024"),
or cut it. This is why platform auto-narration explicitly warns against
image/table-heavy books and cookbooks/coloring books being unsuitable. ([Amazon
KDP Virtual Voice eligibility](https://kdp.amazon.com/en_US/help/topic/GJSXT4GZLP4PL62B),
verified 2026-07-10)

### Inline text that must be spoken out

Build a pre-pass that resolves anything ambiguous when voiced:

- **Numbers** — "$1,200" → "twelve hundred dollars" or "one thousand two hundred
  dollars" (pick per context); "1990s" → "nineteen nineties"; "III" → "the
  third". TTS number handling is inconsistent; normalize deliberately.
- **Abbreviations/acronyms** — decide spell-out vs. say-as-word ("NASA" as a
  word; "e.g." → "for example"; "St." → "Saint" or "Street" depending on use).
- **URLs and emails** — almost always rewritten ("visit the site linked in the
  book description") rather than read character by character.
- **Symbols** — %, &, #, ° must be expanded.

### Dialogue attribution

[Heuristic] In print, "she said angrily" tells the reader the tone. In audio the
*performance* should carry the tone, so heavy adverbial tags can feel
redundant — but for **generative narration you often cannot rely on the voice to
act**, so you may need to *keep* attribution the human ear would find obvious, or
add bracketed performance cues the tool can act on where the tool supports them.
Whichever way, make sure every line of dialogue can be attributed by ear: a long
unbroken back-and-forth with no tags leaves the listener unsure who is speaking.

---

## 3. Cast the narration

### Single narrator vs. multi-voice vs. full cast

[Fact/Heuristic] Two base classes: **solo** (one voice performs the whole book,
voicing all characters) and **multicast** (two or more voices). Full cast is the
cinematic extreme — a distinct actor per character, dialogue tags stripped,
sometimes sound design added. ([Swift Publishing](https://swiftbookpublishing.co.uk/audiobook-narration-styles/),
[Spines](https://spines.com/pros-and-cons-full-cast-audiobooks-vs-single-narrator/),
verified 2026-07-10)

Decision drivers:

- **Point of view.** First-person narration usually points to a single
  narrator (the listener bonds with one voice = the protagonist). Third-person
  ensemble stories tolerate or benefit from multicast. [Heuristic]
- **Genre.** Nonfiction, memoir, and self-development are overwhelmingly single
  narrator — it reads like a lecture or a personal address. SFF and heavily
  dialogued fiction gravitate to full/dual cast. [Heuristic, supported by
  practitioner consensus above]
- **Cost and assembly.** [Fact] Full-cast raises cost and, more importantly,
  editing burden — you cast, direct, and splice many performers' files together.
  ([Spines](https://spines.com/pros-and-cons-full-cast-audiobooks-vs-single-narrator/),
  verified 2026-07-10)
- **Listener preference.** [Fact] An Audio Publishers Association figure cited
  widely holds that a majority of listeners enjoy the experience more with
  distinct character voices — but this is about *differentiation*, not
  necessarily separate actors; a skilled solo narrator supplies it too.
  (Reported via [Spines](https://spines.com/pros-and-cons-full-cast-audiobooks-vs-single-narrator/),
  verified 2026-07-10 — treat the exact percentage as secondary.)

For **generative** production, "full cast" is cheap to attempt (assign different
synthetic voices to characters) but expensive to make *good*: you now have
multiple voices that each must stay consistent, plus the assembly problem. Many
platform auto-narration tools support adding character voices within one book.
([Google Play Books auto-narration](https://play.google.com/books/publish/autonarrated/),
verified 2026-07-10)

### Character differentiation without caricature

[Heuristic] The goal is that a listener can tell who is speaking, not that every
character is a cartoon. For a solo narrator (human or synthetic):

- Differentiate by *pitch, pace, and energy* first, accent last. Accents drift
  and offend more easily than a slightly lower, slower register does.
- Keep each character's voice *reproducible*: write down the parameter settings
  or the descriptive anchor for each character so Chapter 12's dialogue matches
  Chapter 2's. With generative voices this means locking a voice/seed/style per
  character and logging it.
- Avoid demographic caricature — do not signal a character's ethnicity, age, or
  gender through stereotype. Restraint reads as skill.

---

## 4. Hour-scale synthesis: the problems short clips never have

This is the technical core that distinguishes audiobook production from TTS. A
100k-word book is roughly **8–12 hours of audio**. ([Fish Audio](https://fish.audio/blog/best-text-to-speech-for-audiobooks-2026/),
verified 2026-07-10)

### Voice drift

[Observation, well-documented] Across many hours the timbre, energy, and even
pace of a synthetic voice can shift — the tone that worked in Chapter 1 is subtly
different by Chapter 15 — because chunks are generated independently and random
sampling nudges each one. ([Fish Audio](https://fish.audio/blog/best-text-to-speech-for-audiobooks-2026/),
verified 2026-07-10)

Mitigations:

- **Fix the seed / consistency control** where the tool exposes one, so sampling
  is deterministic across chunks. [Heuristic, tool-dependent]
- **Use larger chunks** rather than sentence-by-sentence generation; more context
  per generation reduces inter-chunk timbre jumps. ([tts-audiobook-tool](https://github.com/zeropointnine/tts-audiobook-tool),
  [Fish Audio](https://fish.audio/blog/best-text-to-speech-for-audiobooks-2026/),
  verified 2026-07-10)
- **Anchor voice settings once and reuse** them for every chapter — never let the
  tool re-pick a voice per session.
- **Spot-check across the book** — listen to the first minute of Chapter 1, a
  middle chapter, and the last chapter back-to-back specifically for drift, not
  content.

### Chunking strategy

[Heuristic] Chunk on **semantic boundaries** (sentence/paragraph), not fixed
character counts, so a chunk never cuts mid-clause. Keep chunks as large as the
model reliably handles (a common working figure is on the order of ~80 words per
segment for models that stay accurate at that length; smaller for models that
degrade on long input). ([Qwen3 long-form TTS](https://medium.com/data-science-collective/high-quality-long-form-tts-with-qwen3-open-weight-models-cdd6e3d00df0),
verified 2026-07-10) Match chunk size to the specific model's stability, not a
universal number.

### Per-chapter architecture

[Heuristic] Generate and store **one chapter per file/session**. This gives QC
checkpoints and — critically — means fixing Chapter 15 does not force
regenerating the whole book. ([tts-audiobook-tool](https://github.com/zeropointnine/tts-audiobook-tool),
[Fish Audio](https://fish.audio/blog/best-text-to-speech-for-audiobooks-2026/),
verified 2026-07-10) It also maps directly onto retail chapterization (§9).

### Consistent pacing

[Heuristic] Lock speaking rate globally. Do not speed up dense chapters to save
runtime — inconsistent pace is as jarring as inconsistent timbre. If a passage
needs a different feel (a tense scene, a list), change it deliberately and note
it, don't let it emerge from the chunker.

---

## 5. Pronunciation control across a whole book

The signature failure of book-length synthesis: a character named "Siobhan" or a
place named "Worcester" or a term like "Nginx" mispronounced *the same wrong way
every time it appears*. One error becomes forty.

### Build a book-wide pronunciation dictionary

[Heuristic, strongly supported] Before generating, scan the manuscript and build
a lexicon of every proper noun, invented term, foreign word, and technical term
with an agreed pronunciation. A tool's **pronunciation dictionary / lexicon**
applies a fixed pronunciation everywhere the word appears, so you define it once
instead of tagging every instance. ([AI Narration Pronunciation Guide](https://blog.humanizeaudio.com/ai-narration-pronunciation-guide/),
verified 2026-07-10) Maintain this dictionary as a living artifact for the whole
title (and reuse it across a series so Book 3 pronounces the hero's name like
Book 1).

### SSML and phonetic overrides

[Fact] SSML (Speech Synthesis Markup Language) controls pronunciation, pauses,
and emphasis: `<phoneme>` for a phonetic override, `<break>` for measured
pauses, `<emphasis>` for weight, `<say-as>` for numbers/dates. Phoneme
inventories and supported SSML vary by engine and language. ([Google Play Books
program policies](https://support.google.com/books/partner/answer/10013009),
[pronunciation guide](https://blog.humanizeaudio.com/ai-narration-pronunciation-guide/),
verified 2026-07-10) Use IPA or the engine's phoneme set for names it gets
wrong; prefer a lexicon entry over inline tags so the fix is global.

### Homographs

[Fact] Homographs — same spelling, different sound: "read" (present) vs. "read"
(past), "lead" (verb) vs. "lead" (metal), "tear", "bass", "wind", "live",
"minute", "content". TTS may pick the wrong one from context. ([pronunciation
guide](https://blog.humanizeaudio.com/ai-narration-pronunciation-guide/),
verified 2026-07-10) These cannot be fixed by a single global lexicon entry
(both pronunciations are valid) — they require **context-specific** overrides at
each occurrence, which is why homographs are a first-class item on the QC pass.

---

## 6. Proofing / QC: the listen you cannot skip

[Heuristic, universally emphasized] Generation is not production. You must
**listen to the entire audiobook at normal speed** — the step most people skip
and the one that catches the errors that produce one-star reviews. ([TTS/AI
narration QC guidance](https://blog.humanizeaudio.com/ai-narration-pronunciation-guide/),
verified 2026-07-10) A skim at 2× hides misreads, clipped words, and drift.

### Error taxonomy for the proofing pass

Log every issue by type; each has a different fix:

| Error type | What it sounds like | Typical fix |
|---|---|---|
| **Mispronunciation** | Name/term said wrong | Lexicon entry; regenerate affected chunk |
| **Homograph error** | Right word, wrong sound ("lead the team" as metal) | Context-specific phoneme override at that spot |
| **Skipped / dropped text** | A word, line, or paragraph missing | Re-chunk and regenerate; check for silent SSML/parse failures |
| **Inserted / repeated text** | A phrase said twice or hallucinated | Regenerate chunk; tighten chunk boundaries |
| **Wrong emphasis / stress** | Stress on the wrong word, question read flat | SSML emphasis / rephrase; regenerate |
| **Pacing fault** | Rushed, or unnatural pause mid-clause | Adjust rate / break tags |
| **Voice drift** | Chapter sounds like a different reader | Re-anchor voice/seed; regenerate chapter |
| **Number/date/abbrev misread** | "1990s" as "one thousand nine hundred nineties" | Fix in text normalization pre-pass; regenerate |
| **Audio defect** | Click, breath, clip, glitch, wrong loudness | Fix in mastering (§7), not generation |

Because you generated per chapter (§4), fixes are local: regenerate the affected
chunk or chapter, not the book.

---

## 7. Technical delivery specs

[Fact — verified 2026-07-10] Retail audio gates are strict and often
**automated**: files outside the numeric window are rejected before a human
listens. The widely used **ACX/Audible** spec is the de facto reference target
and a safe master to hit even for other stores:

- **Loudness (RMS):** between **−23 dB and −18 dB RMS**.
- **Peak:** below **−3 dB** (true peak), to avoid clipping/encoding distortion.
- **Noise floor:** below **−60 dB RMS**. (The hardest spec to meet for home
  recordings and the most common cause of rejection.)
- **Room tone:** **1–5 seconds** at the head and tail of every file (max 5s).
- **Format:** **192 kbps CBR MP3 or higher**; **44.1 kHz** sample rate.
- **Channels:** all files the same — all mono *or* all stereo, never mixed.
- **File length:** each file **≤ 120 minutes**.
- **One section per file:** each file contains exactly one chapter/section.
- **Opening credits** (title, author, narrator) and **closing credits**; plus a
  **retail sample ≤ 5 minutes**.

Source: [ACX audio submission requirements](https://help.acx.com/s/article/what-are-the-acx-audio-submission-requirements),
verified 2026-07-10.

[Heuristic] For generative audio, the noise-floor spec is usually *easy* (no mic
hiss) but you still must: normalize loudness to land inside the RMS window,
peak-limit to −3 dB, and add real room tone (a short synthetic near-silence or
low-level tone) so files are not dead-digital-silent at the edges, which some
encoders and QC tools flag. Master **per file**, then verify every file with a
loudness meter before delivery — one out-of-spec file rejects the whole upload.

---

## 8. Chapterization and metadata

[Standard] Deliver **one file per chapter/section**, named in playback order so
players sort correctly: a chronological number prefix then the section name
(e.g., `01 Opening Credits`, `02 Chapter One`, `03 Chapter Two`). ([APLN /
accessibility production](https://nnels.ca/accessibility-guidelines-audiobook-narrators),
verified 2026-07-10)

[Standard] Embed **ID3 tags** on each MP3 so the audiobook carries its own
structure: **Title** = chapter name, **Album** = book title, **Artist** =
author/narrator, **Track number** = playback order. Robust metadata also
improves accessibility and reduces metadata-based rejections. ([APLN ID3 intro](https://apln.ca/introduction-to-id3-tags-in-audiobooks/),
[APLN metadata intro](https://apln.ca/introduction-to-audiobook-metadata/),
verified 2026-07-10)

Cover art, title, author, narrator credit, series, and description are set at the
distributor level and must match the ebook/print metadata.

---

## 9. Retail platforms and AI-narration policy (verify before you build)

**Policies here are volatile and differ sharply by platform. All verified
2026-07-10 — re-verify at production time.** AI-narration handling ranges from
*banned* to *required-to-disclose* to *the platform generates it for you*.

### Audible / ACX — human narration only, with a narrator-consent AI exception

[Policy — verified 2026-07-10] ACX requires human narration; unauthorized
text-to-speech / AI narration is not permitted for standard submissions.
([ACX requirements](https://help.acx.com/s/article/what-are-the-acx-audio-submission-requirements))
The exception is the **Narrator Voice Replica beta** (launched **July 9, 2025**,
US-only): a *narrator* creates an AI replica **of their own voice**, auditions
and is selected like a human, and edits the output for pronunciation and pacing.
Audible will not use a narrator's replica for any title without approval; titles
using a replica are labeled; compensation can be per-finished-hour, royalty
share, or a hybrid. ([ACX blog: Narrator Voice Replicas](https://www.acx.com/mp/blog/now-in-beta-narrator-voice-replicas-on-acx))
Implication: you cannot upload a generic AI-narrated file to ACX; the AI path
runs through a consenting narrator.

### Amazon KDP "Virtual Voice" — Amazon generates it (separate from ACX)

[Policy — verified 2026-07-10] A separate Amazon program (beta, often
invite-based) that generates an AI audiobook from an eligible Kindle ebook.
Eligibility: ebook live ≥7 days, has a table of contents, English primary
language, no existing audiobook, roughly **< ~240k words / ~26 hours**, and
suitable for audio (cookbooks/coloring books excluded). Choose from a set of
voices; list price **$3.99–$14.99**; distributed where Audible audiobooks are
sold. ([KDP Virtual Voice eligibility](https://kdp.amazon.com/en_US/help/topic/GJSXT4GZLP4PL62B),
[getting started](https://kdp.amazon.com/en_US/help/topic/GFAQU3LUEHCRB8KD))

### Spotify (via Spotify for Authors) — AI allowed, must disclose

[Policy — verified 2026-07-10] Spotify accepts digital-voice (AI) narration; the
author checks "This audiobook uses digital voice narration," and Spotify appends
a disclosure sentence to the description. It accepts digital narration from
providers such as Google Play Books, ElevenLabs, and others. Note: it does not
share digital-voice titles to referral partners. ([Spotify digital voice
narration](https://support.spotify.com/us/authors/article/digital-voice-narration/))

### Findaway Voices → Voices by INaudio — wide distribution, AI allowed with disclosure

[Policy — verified 2026-07-10] **Findaway Voices by Spotify ceased August 1,
2025.** Third-party (non-Spotify) distribution and the self-publishing business
were reacquired by Findaway's co-founders and relaunched as the independent
**Voices by INaudio**; the old Findaway URL redirects there and logins carried
over. INaudio distributes finished audiobooks to 30+ retailers/libraries
(Audible, Apple Books, Spotify, Google Play, etc.) and takes ~20% of net after
retailers' cut; AI narration is allowed if disclosed. Spotify uploads now go
through Spotify for Authors directly. ([Jane Friedman: Findaway as INaudio](https://janefriedman.com/what-authors-need-to-know-about-the-return-of-findaway-as-inaudio/),
[Self-Publishing Advice](https://selfpublishingadvice.org/spotify-ends-findaway-voices/))

### Google Play Books — auto-narration (platform-generated AI)

[Policy — verified 2026-07-10] Google generates the audiobook from your **EPUB**.
You must own audiobook rights and have the ebook live on Google Play. Supported
input languages include English, Spanish, German, French, Hindi, and Brazilian
Portuguese; 50+ voices; you can add character voices, edit speed, and fix
pronunciation (suggested, phonetic, or by recording the word). Publisher revenue
share ~52%; you may download the files and sell wide, but if it is for sale
elsewhere it must also be on Google Play, and the Google price must not exceed
the price elsewhere. ([Google auto-narration](https://play.google.com/books/publish/autonarrated/),
[program policies](https://support.google.com/books/partner/answer/10013009))

### Apple Books — digital narration (platform-generated AI)

[Policy — verified 2026-07-10] Apple produces a digitally narrated audiobook from
a reflowable **English** ebook that is live on Apple Books, in supported
categories (fiction, romance, mystery & thriller, SFF, nonfiction,
self-development; erotica excluded). Apple's pipeline combines speech synthesis
with linguists, QC specialists, and audio engineers; access is via approved
partners (e.g., Draft2Digital for indie authors, Ingram CoreSource / PublishDrive
for publishers); free; production/QC takes roughly one to two months. You keep
audiobook rights and can produce other versions. ([Apple Books digital
narration](https://authors.apple.com/support/4519-digital-narration-audiobooks),
[get started](https://authors.apple.com/support/4973-get-started-digital-narration))

### Route implication

[Heuristic] If you want an **AI audiobook on Audible/Amazon**, your realistic
paths are Amazon's Virtual Voice or a consenting narrator's ACX voice replica —
not a self-made AI file. If you want to **self-produce AI audio and go wide**,
master to ACX specs, disclose AI narration, and distribute through a
wide-distribution aggregator (e.g., INaudio) plus Spotify for Authors — but note
Audible/ACX will not take a generic AI file. Platform-generated routes (Google,
Apple) are lowest effort but keep you inside their pipeline and pricing rules.

---

## 10. Rights and consent

[Fact] **Text rights and narration rights are separate.** The author holds
copyright in the words; the narrator holds a separate performance right in the
recorded performance. Owning the book does not grant rights to a performance of
it, and you must actually hold the **audio rights** for the title (platform
auto-narration programs require you to attest this and exclude public-domain-only
claims where they require you to own rights). ([AI voice cloning legal issues](https://editorialge.com/ai-voice-cloning-for-audiobook-narration-legal-issues/),
[Apple](https://authors.apple.com/support/4519-digital-narration-audiobooks),
[Google policies](https://support.google.com/books/partner/answer/10013009),
verified 2026-07-10)

[Fact] **Voice cloning requires the voice owner's explicit consent.**
Right-of-publicity law protects a person's voice identity from unauthorized
commercial use; cloning a specific narrator or a recognizable voice without
written permission is a legal exposure, and industry practice (e.g., SAG-AFTRA
terms) requires written consent and compensation. Watch licensing fine print
that quietly claims "derivative uses" including **model training**. ([AI voice
cloning legal issues](https://editorialge.com/ai-audiobook-narration-legality),
[Authors Guild on Findaway/Spotify terms](https://authorsguild.org/news/response-to-findaway-spotify-audiobook-terms-of-use/),
verified 2026-07-10)

[Heuristic] Apply the **"three C's": consent, control, compensation** — a voice
is only ethically and legally safe to synthesize when its owner agreed, retains
control over which projects use it, and is paid. For a generic library TTS
voice, your safety comes from the tool's license granting commercial audiobook
use; read that license for scope (commercial use, audiobook distribution,
whether output is yours). Never clone a real person's voice — including a
celebrity narrator's "style" — without documented permission.

---

## 11. Accessibility framing

[Heuristic/Fact] Audiobooks are a primary reading format for people with print
disabilities, and accessibility-oriented production has *stricter* completeness
norms than commercial retail: narrate section titles, include footnotes /
endnotes / bibliographies rather than cutting them, and give every section its
own numbered file with full metadata so a print-disabled listener can navigate
the book the way a sighted reader navigates pages. ([NNELS guidelines](https://nnels.ca/accessibility-guidelines-audiobook-narrators),
[AccessiblePublishing.ca](https://www.accessiblepublishing.ca/audiobook-recommendations-for-publishers/),
verified 2026-07-10) When a title's purpose is access (library, education,
public-interest), bias every "include vs. omit" call in §2 toward *include*, and
keep chapterization/metadata (§8) rigorous — it is the navigation layer.

---

## 12. End-to-end example (labeled example — not a required formula)

**Intent:** Self-produce an AI-narrated audiobook of a 95,000-word first-person
memoir with light footnotes and distribute wide.

1. **Route:** Route 2 (self-produced generative). Because Audible/ACX won't take
   a generic AI file, plan wide distribution via an aggregator + Spotify for
   Authors, with AI narration disclosed.
2. **Manuscript prep:** First-person memoir → single narrator. Convert the ~15
   citation footnotes: drop 9 bare-citation notes, fold 4 into sentences, read 2
   interesting ones in-line with an audible cue. Normalize numbers/dates,
   expand abbreviations, rewrite the one table into two spoken sentences. Write
   opening + closing credits.
3. **Pronunciation dictionary:** Scan for proper nouns — the author's hometown
   "Beaufort" (BYOO-furt, not BOH-fort), two family surnames, one foreign
   phrase. Add lexicon entries. Flag homographs ("read", "tear", "live") for
   the QC pass since context decides them.
4. **Voice + consistency:** Pick one library voice licensed for commercial
   audiobook use. Fix the seed, set a global speaking rate, generate **one file
   per chapter**, and log the exact voice settings.
5. **QC:** Full listen at 1×. Log by the §6 taxonomy: two homograph errors
   ("live" as adjective, "tear" as crying) fixed with per-spot overrides; one
   dropped sentence regenerated; one chapter drifting brighter re-anchored to
   the seed and regenerated.
6. **Master:** Per file — normalize to ~−20 dB RMS, peak-limit to −3 dB, add 1s
   room tone head/tail, export 192 kbps CBR MP3 @ 44.1 kHz, all mono. Verify
   every file with a loudness meter.
7. **Chapterize + metadata:** Files `01 Opening Credits` … `NN Closing
   Credits`; ID3 Title/Album/Artist/Track on each.
8. **Rights + disclosure:** Confirm audiobook rights held; confirm the voice
   license covers commercial audiobook distribution; set the "digital voice
   narration" disclosure flag at every distributor that requires it.

**Expected result:** A spec-compliant, chapterized, disclosed AI audiobook
accepted wide. **Likely failure modes:** a mispronounced name that slipped the
lexicon, one out-of-RMS file rejecting the upload, or forgetting the disclosure
flag. **Variation:** an ensemble third-person novel would push toward multicast
(one consistent voice per major character, each with its own logged settings and
its own drift check), and a scholarly nonfiction title would push toward
*including* footnotes and full section-title narration.

---

## Sources (verified 2026-07-10)

- ACX audio submission requirements — https://help.acx.com/s/article/what-are-the-acx-audio-submission-requirements
- ACX Narrator Voice Replicas beta (July 9, 2025) — https://www.acx.com/mp/blog/now-in-beta-narrator-voice-replicas-on-acx
- Amazon KDP Virtual Voice eligibility — https://kdp.amazon.com/en_US/help/topic/GJSXT4GZLP4PL62B
- Amazon KDP Virtual Voice getting started — https://kdp.amazon.com/en_US/help/topic/GFAQU3LUEHCRB8KD
- Spotify digital voice narration — https://support.spotify.com/us/authors/article/digital-voice-narration/
- Google Play Books auto-narration — https://play.google.com/books/publish/autonarrated/
- Google Play Books auto-narrated program policies — https://support.google.com/books/partner/answer/10013009
- Apple Books digital narration — https://authors.apple.com/support/4519-digital-narration-audiobooks
- Apple Books get started with digital narration — https://authors.apple.com/support/4973-get-started-digital-narration
- Findaway Voices → Voices by INaudio transition (Jane Friedman) — https://janefriedman.com/what-authors-need-to-know-about-the-return-of-findaway-as-inaudio/
- Spotify ends Findaway Voices (ALLi/SelfPublishingAdvice) — https://selfpublishingadvice.org/spotify-ends-findaway-voices/
- Long-form TTS voice consistency / drift & chunking (Fish Audio) — https://fish.audio/blog/best-text-to-speech-for-audiobooks-2026/
- Long-form TTS chunking / per-chapter architecture (tts-audiobook-tool) — https://github.com/zeropointnine/tts-audiobook-tool
- Qwen3 long-form TTS (chunk sizing) — https://medium.com/data-science-collective/high-quality-long-form-tts-with-qwen3-open-weight-models-cdd6e3d00df0
- AI narration pronunciation, SSML, homographs, QC — https://blog.humanizeaudio.com/ai-narration-pronunciation-guide/
- Single vs full cast narration (Swift Publishing) — https://swiftbookpublishing.co.uk/audiobook-narration-styles/
- Pros/cons full cast vs single narrator (Spines) — https://spines.com/pros-and-cons-full-cast-audiobooks-vs-single-narrator/
- Accessibility guidelines for narrators (NNELS) — https://nnels.ca/accessibility-guidelines-audiobook-narrators
- ID3 tags in audiobooks (APLN) — https://apln.ca/introduction-to-id3-tags-in-audiobooks/
- Audiobook metadata intro (APLN) — https://apln.ca/introduction-to-audiobook-metadata/
- AI voice cloning legal issues / narration vs text rights — https://editorialge.com/ai-voice-cloning-for-audiobook-narration-legal-issues/
- Authors Guild on Findaway/Spotify audiobook terms — https://authorsguild.org/news/response-to-findaway-spotify-audiobook-terms-of-use/
</content>
</invoke>
