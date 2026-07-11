# Evaluation — audiobook-production

This is the scoring key. The evaluated agent receives only the user task and
`SKILL.md`, never this file. Score the captured response against the expected
answers, rubrics, and critical failures below.

Volatile platform facts are dated to **2026-07-10**; if evaluating later,
re-verify against the cited primary sources before penalizing an answer that
reflects a newer policy.

---

## Part A — Knowledge questions

### A1. State the ACX audio submission technical specs.

**Expected answer (all required):**
- RMS loudness between **−23 and −18 dB**.
- Peak below **−3 dB**.
- Noise floor below **−60 dB RMS**.
- Room tone **1–5 seconds** head and tail (max 5s).
- **192 kbps CBR MP3 or higher**, **44.1 kHz**.
- All files same channel format (all mono or all stereo).
- Each file **≤ 120 minutes**, **one section/chapter per file**.
- Opening + closing credits; retail sample ≤ 5 minutes.

**Scoring:** 1 point per correct spec, 8 total. Full credit needs the three
loudness/noise numbers plus at least three of the structural specs.

**Critical failures:** inventing numbers (e.g., "−16 dB RMS", "−1 dB peak",
"−50 dB noise floor"); stating LUFS targets as the ACX spec without noting ACX
specifies RMS; claiming there is no automated gate.

### A2. Why is book-length synthesis different from a short TTS clip? Name at least three problems unique to hour scale.

**Expected:** voice drift/timbre inconsistency across chapters; the need for a
book-wide pronunciation dictionary (one wrong name repeats dozens of times);
chunking strategy and per-chapter architecture; consistent global pacing;
homograph resolution across many contexts; QC requiring a full real-time listen
of many hours. A 100k-word book ≈ 8–12 hours of audio.

**Scoring:** 1 point each, cap 4. Must be problems that genuinely don't arise in
a single clip.

**Critical failure:** treating an audiobook as "just a longer generation" with
no drift, pronunciation-consistency, or chapterization concerns.

### A3. What is a homograph error and why can't a global pronunciation dictionary fix it?

**Expected:** a homograph is one spelling with two valid pronunciations chosen by
context ("read", "lead", "tear", "live", "bass", "wind", "minute", "content").
A global lexicon entry can't fix it because **both** pronunciations are correct
somewhere in the book; the fix must be **context-specific** at each occurrence
(e.g., an SSML/phoneme override at that spot). This is why homographs get their
own QC pass.

**Scoring:** full credit requires the "both valid → needs per-occurrence fix"
reasoning, not just a definition.

**Critical failure:** claiming one dictionary entry solves homographs.

### A4. Distinguish text rights from narration rights, and state the consent requirement for cloning a voice.

**Expected:** the author holds copyright in the words; the narrator holds a
separate performance right in the recording — owning the book does not grant
rights to a performance, and you must hold the audio rights for the title.
Cloning a specific/recognizable voice requires the voice owner's **explicit
written consent** (right of publicity; SAG-AFTRA-style consent + compensation);
watch license fine print claiming derivative uses / model training.

**Scoring:** 2 points for the rights distinction, 2 for the consent requirement.

**Critical failure:** saying that owning the book (text rights) lets you clone
any narrator's voice, or that a public-domain text makes voice cloning of a real
person's voice permissible.

### A5. Which platforms allow AI narration and how, as of 2026-07-10?

**Expected (accept minor wording, penalize wrong direction):**
- **Audible/ACX:** human narration only for standard submissions; AI path only
  via the **Narrator Voice Replica** beta (narrator's own voice, consent,
  labeled). You cannot upload a generic AI file.
- **Amazon KDP Virtual Voice:** Amazon-generated AI audiobook from an eligible
  Kindle ebook (separate from ACX).
- **Spotify (for Authors):** AI allowed, must **disclose** ("digital voice
  narration"); does not push to referral partners.
- **Voices by INaudio** (successor to Findaway Voices, which ceased 2025-08-01):
  wide distribution, AI allowed with disclosure.
- **Google Play Books:** platform generates AI narration from your EPUB.
- **Apple Books:** platform-generated digital narration via approved partners,
  English, reflowable, supported genres.

**Scoring:** 1 point per platform correctly characterized, cap 6.

**Critical failures:** claiming you can upload a self-made generic AI audiobook
directly to Audible/ACX; claiming Spotify/INaudio require *no* disclosure;
stating Findaway Voices is still operating unchanged.

---

## Part B — Production-decision questions

### B1. A client wants an AI-narrated audiobook "on Audible." How do you route it?

**Expected decision:** Explain that ACX does not accept a generic self-made AI
file. The realistic Audible/Amazon AI paths are (a) **Amazon KDP Virtual Voice**
(Amazon generates it from the ebook) or (b) an **ACX Narrator Voice Replica**
(a consenting narrator's own AI voice). If the client insists on self-producing
their own AI audio, they can go wide via an aggregator (INaudio) + Spotify with
disclosure, but that route does not put a self-made AI file on Audible/ACX.
Should date the policy and offer to re-verify.

**Reward:** naming the ACX prohibition, offering the two legitimate Audible AI
routes, and separating "AI on Audible" from "self-made AI file."

**Penalize:** promising to upload a self-generated AI file to ACX; ignoring the
consent/labeling structure of the replica program.

### B2. First-person memoir vs. a large ensemble fantasy — how do you cast each, and how do you keep character voices consistent in the generative case?

**Expected:** memoir/first-person/nonfiction → **single narrator** (intimate,
lecture-like, cost-effective). Ensemble third-person fantasy → candidate for
**multicast/full cast** for character differentiation, at higher assembly/QC
cost. In the generative case, differentiation should come first from pitch/pace/
energy (accent last, avoid caricature), and each character's voice/seed/style
settings must be **logged and reused** so Chapter 12 matches Chapter 2; each
voice needs its own drift check.

**Reward:** POV/genre reasoning + the "log and reuse per-character settings"
consistency mechanism + caricature caution.

**Penalize:** defaulting every book to full cast; recommending accent-based
stereotyping; ignoring that multiple synthetic voices multiply the drift problem.

### B3. A nonfiction book has 60 footnotes, three data tables, and several charts. How do you prepare it for narration?

**Expected:** make a per-element include/omit decision. Footnotes: drop
bare-citation notes, fold substantive ones into sentences, or read interesting
ones with an audible "in a footnote…" cue; scholarly/accessibility editions bias
toward including notes and bibliographies. Tables/charts: cannot be read — rewrite
the essential finding as one or two spoken sentences, or cut. Normalize numbers,
symbols, abbreviations, URLs in a pre-pass. Add opening/closing credits.

**Reward:** the include/omit-per-element framing and the "rewrite the finding"
move for visuals; noting the accessibility-vs-commercial difference.

**Penalize:** "read the footnote markers/superscripts aloud" or "read the table
row by row"; leaving visual-dependent content unflagged.

---

## Part C — Applied production tasks

### C1. Build the pre-production plan for a 110k-word first-person thriller to be self-produced with a generative voice and distributed wide.

**Essential characteristics of a strong output:**
- States route (self-produced generative) and its distribution reality (wide via
  aggregator + Spotify with AI disclosure; not a generic file on Audible/ACX).
- Single narrator (first person).
- Manuscript prep: footnote/table handling, number/abbreviation normalization,
  credits, dialogue attributable by ear.
- A **book-wide pronunciation dictionary** step (proper nouns, invented terms)
  plus a homograph flag list for QC.
- Voice consistency mechanics: fixed voice + seed, global pacing, **one file per
  chapter**, logged settings.
- Full 1× QC listen with an error taxonomy and local (per-chunk/chapter) fixes.
- Mastering per file to ACX specs (RMS window, −3 dB peak, room tone, 192k CBR
  44.1 kHz, uniform channels) with per-file loudness verification.
- Chapterized numbered files + ID3 metadata.
- Rights/consent + disclosure flags.

**Rubric (10 pts):** route+distribution reality (1), casting (1), manuscript
prep (2), pronunciation dictionary + homographs (2), voice-consistency mechanics
(1), QC listen + taxonomy (1), mastering to spec (1), chapterization/metadata
(0.5), rights/disclosure (0.5).

**Critical failures:** no full QC listen; no pronunciation dictionary; ignoring
loudness specs; promising the self-made AI file will go on Audible; no AI
disclosure.

### C2. QC triage: given a list of six issues from a proofing listen, classify each and give the correct fix.
*(Evaluator supplies the six; expected classification/fix per the taxonomy.)*

Expected mapping (name the type, then the fix):
- "The name 'Saoirse' is said 'sao-irse' everywhere" → **mispronunciation** →
  lexicon entry, regenerate affected chunks.
- "'He will lead the team' said with the metal sound" → **homograph error** →
  per-occurrence phoneme override, regenerate that spot.
- "A sentence at the end of Ch. 4 is missing" → **skipped/dropped text** →
  re-chunk and regenerate; check for a silent parse/SSML failure.
- "Chapter 9 sounds brighter/faster than Chapter 1" → **voice drift** →
  re-anchor voice/seed (and rate), regenerate the chapter.
- "'1980s' read as 'one thousand nine hundred eighties'" → **number misread** →
  fix in the text-normalization pre-pass, regenerate.
- "A click/pop between two words" → **audio defect** → fix in mastering/editing,
  not generation.

**Rubric:** 1 point per correctly classified issue with a fix that matches the
type. **Critical failure:** prescribing a full-book regeneration for a local
error, or "fix in mastering" for a mispronunciation (or vice versa).

### C3. Master and package deliverables: describe how you take generated chapter audio to a spec-compliant, retail-ready set of files.

**Essential characteristics:**
- Per-file loudness normalization into the **−23 to −18 dB RMS** window.
- Peak-limit to **below −3 dB**.
- Add **1–5 s room tone** head/tail (real low-level tone, not dead digital
  silence).
- Export **192 kbps CBR MP3 @ 44.1 kHz**, **uniform channel format**.
- One chapter per file, **≤120 min**, numbered filenames in playback order.
- **ID3 tags**: Title=chapter, Album=book, Artist=author/narrator, Track=order.
- Opening/closing credits present; retail sample ≤5 min.
- **Verify every file with a loudness meter** before upload (one bad file rejects
  the batch).

**Rubric (8 pts):** RMS (1), peak (1), room tone (1), format/sample rate/channels
(1), chapterization + naming (1), ID3 metadata (1), credits/sample (1), per-file
verification (1).

**Critical failures:** mixing mono and stereo across files; exporting VBR or the
wrong sample rate; skipping per-file verification; omitting room tone; putting
multiple chapters in one file.

---

## Scoring summary

- **Part A (knowledge):** ~28 points. Below ~60% → the agent lacks the factual
  base (specs, policies, rights) to produce compliant work.
- **Part B (decisions):** pass requires correct routing, casting logic, and
  manuscript-prep judgment without any critical failure.
- **Part C (applied):** the core of the evaluation. C1 and C3 must be
  spec-accurate; C2 must classify errors and map each to the correct **local**
  fix.

**Automatic fail (any one):** claims a self-made generic AI file can be uploaded
to Audible/ACX; omits the full QC listen; invents ACX loudness numbers; asserts
text/ebook ownership authorizes cloning a narrator's voice; recommends
regenerating the whole book for a single local error.
</content>
