---
name: suno-music
description: >-
  Generate music with Suno (v5 / v5.5 era, 2026) and advise a production team on
  what they may legally do with the output. Use this skill when a user wants to
  create, extend, remaster, or stem-separate a track in Suno; craft Suno prompts
  (style field, lyrics/metatags, exclude-styles, personas, custom voices); choose
  a subscription tier for a given use; or get accurate answers about ownership,
  commercial rights, distribution/monetization on DSPs, the Warner Music Group
  settlement, the ongoing label/publisher litigation, and Suno's API situation.
  Do not use it for other music generators (Udio, ElevenLabs Music, Google Lyria)
  except by explicit contrast, and do not use it as a substitute for a lawyer on a
  specific commercial deal.
---

# Suno music generation and rights advisory

Suno is a text-to-music service that generates full songs (vocals + instrumental) from a
style description and optional lyrics, plus editing tools (extend, cover, remaster, stem
separation, a DAW-style Studio). This skill covers two things a production agent must get
right at the same time: **making good music with the current models** and **advising
accurately on the rights, licensing, and legal reality of using that music commercially**.

The rights half is not an appendix. As of mid-2026 the single most common way to give a
production team bad advice is to treat Suno output as freely ownable, copyrightable, and
API-accessible. Read the "Rights, licensing, and legal reality" section before advising on
any commercial or distribution use.

**Evidence labels used below**
- **[Documented]** — stated in Suno's own docs, terms, help center, or blog, or in a
  primary legal/press source, with a URL in Sources.
- **[First-party claim]** — Suno's own marketing/announcement language, reported as a
  claim rather than an independently verified fact.
- **[Heuristic]** — production practice inferred from how the tools behave; useful defaults,
  not guarantees.

**Volatility warning.** Models, tiers, prices, terms, litigation status, and API access
change fast. Every volatile fact below carries a verification date of **2026-07-10** unless
noted. Re-verify anything legal or version-specific against suno.com before relying on it.

---

## 1. Current models and what they do

**[Documented] Model timeline** (Suno help center "Model Timeline", verified 2026-07-10):

| Model | Released | What it added |
|-------|----------|---------------|
| V3.5 | Summer 2024 | Better structure; up to ~4 min first gen |
| V4 | Nov 2024 | Improved vocal quality; introduced Extend, Cover, Persona |
| V4.5 | May 2025 | Up to 8-min first generation; better prompt adherence; style mashups |
| V4.5+ | Jul 2025 | Add Vocals / Add Instrumental production tools |
| V5 | Sep 2025 | Higher audio fidelity, more authentic vocals; **Pro/Premier only** |
| V5.5 | Mar 26 2026 | Voices (record/upload your own voice), Custom Models, My Taste |

- **[Documented]** V5 launched ~September 23–25, 2025 and is available only to paid (Pro/Premier)
  subscribers; free-tier users generate on older models. Suno also shipped **Suno Studio**
  (a generative audio workstation with a multitrack editor and MIDI/stem export) on the
  Premier plan around Sep 25, 2025.
- **[Documented]** V5.5 (Mar 26 2026) added three features: **Voices** (capture or upload your
  own voice, sing on your creations; includes voice verification, recordings kept private),
  **Custom Models** (Pro/Premier can train up to three personal model versions on their own
  catalog), and **My Taste** (preference personalization, available to all tiers).
- **[First-party claim]** Suno marketed V5 as its "most powerful" / "world's best music model"
  and V5.5 as "more expressive." Treat superlatives as marketing, not benchmarks — there is no
  neutral, published head-to-head that establishes Suno as a universal "best." When a user asks
  "is Suno the best," answer on fitness for their use, not on the marketing claim.
- **[Documented — anticipated]** Under the Warner deal (see §5), Suno has said higher-quality
  models **trained on licensed WMG recordings** are forthcoming. As of 2026-07-10 no such
  licensed model is confirmed shipped under a public name; treat "WMG-licensed model" as
  announced-but-unshipped and re-verify.

**Version selection heuristic.** For any track intended for release, generate on V5/V5.5 (paid).
Free-tier output is both lower quality *and* non-commercial (§4), so it is only appropriate for
scratch ideas, learning, and personal listening.

---

## 2. The generation surface: fields and controls

Suno's create screen (Custom mode) has two text inputs that do different jobs — mixing them up
is the most common cause of bad output.

- **Style / description field** — genre, subgenre, mood, tempo feel, instrumentation, production
  character, vocal type, era, reference *adjectives*. This is where the sonic identity lives.
- **Lyrics field** — the actual words **plus structural metatags in square brackets**. If you put
  genre words here they may be sung. If you leave it empty (or use "Instrumental"), you get an
  instrumental.
- **[Documented] Exclude Styles** (negative prompt) — in Custom mode under Advanced Options; list
  what you do *not* want (e.g. a genre, an instrument, "male vocals") and Suno deprioritizes it.
- **Simple vs Custom mode** — Simple mode takes one free-text prompt and writes lyrics/structure
  for you; Custom mode exposes the style field, lyrics field, exclude-styles, model picker, and
  weirdness/style-influence sliders. Use Custom for anything you want control over.

**[Heuristic] Style field craft**
- Lead with the anchor: one clear genre + one clear mood, then layer detail. `melodic
  drum-and-bass, euphoric, driving` beats a 40-word soup of adjectives.
- Name instruments and vocal type explicitly when they matter (`female alto, breathy`,
  `analog synth bass`, `brushed jazz drums`).
- Tempo: you can state BPM in the style field, or use a `[bpm-128]` metatag in lyrics; giving a
  numeric BPM is more reliable than "fast."
- Don't over-stuff. Beyond ~6–10 strong descriptors, added words dilute rather than sharpen.
- Contradictions (e.g. "minimal, wall-of-sound maximalist") produce mush; pick a lane.

---

## 3. Lyrics, structure, and metatags

**[Documented]** Structural **metatags** go in the *lyrics* field inside square brackets and steer
arrangement, dynamics, and vocal behavior. Without them Suno infers structure from line breaks;
with them you remove the guesswork.

Common, reliably-understood tags (**[Documented]** for the core structure tags; **[Heuristic]** for
exact behavior, which varies by model):

```
[Intro]
[Verse]        [Verse 1] [Verse 2]
[Pre-Chorus]
[Chorus]
[Post-Chorus]
[Bridge]
[Instrumental]  [Guitar Solo]  [Drop]
[Outro]         [Fade Out]
[no-vocals]     [bpm-128]  [key-C-minor]  [time-signature-3/4]
```

**[Heuristic] Lyric and structure practice**
- `[Chorus]` triggers chorus behavior — bigger arrangement, hook, repetition on later
  occurrences. Reusing the exact same chorus text each time yields a consistent, memorable hook;
  varying it slightly yields evolution.
- Keep tags short (1–3 words). Long descriptive tags are less reliable than a short structural
  tag plus a style-field descriptor.
- To force an instrumental, put `[Instrumental]` / `[no-vocals]` and leave lyrics empty, or select
  the Instrumental toggle.
- Inline performance cues (whispered, ad-lib, spoken) work inconsistently across models — test,
  don't assume.
- Suno can auto-write lyrics; for a controlled brief, write your own lyrics so you also own that
  copyright layer (§4).

---

## 4. Editing, iteration, and stems

- **Extend** — continue a track past its current end; useful for building full arrangements from a
  strong 1–2 min section.
- **Cover** — re-perform existing lyrics/melody in a new style.
- **Remaster** — **[Documented]** re-render an older track on a newer model (e.g. lift a V4 track to
  V5 quality), with control over how much it varies from the original.
- **Add Vocals / Add Instrumental** — layer onto an existing track (V4.5+ onward).
- **Personas / Voices** — **[Documented]** Persona captures the vocal/stylistic identity of a prior
  generation to carry it across new songs; V5.5 **Voices** lets you record or upload your *own*
  voice to sing on creations (with verification; recordings private by default). Do not use a
  Voice/Persona to imitate a real artist you have no rights to (§5, §6).
- **Stems** — **[Documented / First-party claim]** Suno can split a generation into individual
  stems (vocals, drums, bass, and more — marketed as up to ~12 stems) and Suno Studio (Premier)
  exports multitrack stems and MIDI for finishing in a DAW (Ableton, Logic, FL, etc.).

**[Heuristic] Iteration workflow.** Generate several candidates on a tight style prompt → pick the
best structural take → Extend to full length → Remaster/clean if needed → export stems for mix and
master in a DAW. Regenerating from a slightly varied prompt is usually faster than fighting one
bad take with edits.

---

## 5. Rights, licensing, and legal reality (read before advising on commercial use)

This section is the core of the skill. Get the tier logic and the copyright caveat right every time.

### 5.1 Ownership and commercial use by tier

**[Documented]** (Suno Terms of Service, last revised **2026-03-26**; Suno help center "Rights &
Ownership"; verified 2026-07-10):

- **Free / Basic tier:** Suno **retains ownership**. You get a limited license to use output for
  **lawful, internal, personal, non-commercial** purposes **only**, and you must **give attribution
  to Suno**. No distribution, no monetization, no commercial use.
- **Pro / Premier (paid) tiers:** Suno **assigns to you** all of its right, title, and interest in
  the output generated from your submissions **while you were subscribed**. You may distribute,
  monetize, and use it commercially. Premier gets the same commercial *rights* as Pro — the extra
  cost buys volume (credits) and tooling (Studio), **not** broader legal rights.
- **Timing is what matters, not current status:** ownership/commercial rights attach based on your
  subscription **at the moment the track was generated**. **[Documented]** Songs made while paid stay
  commercial-usable **even after you cancel**. Conversely, upgrading later does **not**
  retroactively grant rights to a track you made on the free tier — you must regenerate it while paid.

**Approximate 2026 pricing (verify — volatile):** Pro ≈ $10/mo (~$8 annual), ~2,500 credits;
Premier ≈ $30/mo (~$24 annual), ~10,000 credits + Suno Studio. Prices/credits change; confirm on
suno.com before quoting.

### 5.2 The copyright caveat that ownership does not cure

**[Documented]** Two separate things, and agents routinely conflate them:

1. **Contractual ownership from Suno** — paid tiers get this (Suno assigns its interest to you).
2. **Copyright protection under law** — a *different* question. Suno's terms state it makes **no
   representation or warranty that any copyright will vest in any Output**. Suno's own help center
   warns output "may not be eligible for copyright protection."

**Why:** U.S. copyright requires human authorship; the U.S. Copyright Office has repeatedly held
that material generated by AI from a prompt is **not** protectable, because writing a prompt is not
authorship of the resulting expression. **[Documented]** Practical consequence: a fully
Suno-generated track can be **owned** (contractually, on a paid tier) and **legally used
commercially**, yet **not copyrightable**, meaning you may have limited ability to stop others from
copying it. **[Heuristic]** The strongest human-authorship hook is **writing your own lyrics**
(you own that literary copyright independently) and doing substantial human arrangement/editing;
this improves — but does not guarantee — registrability. This varies by country; direct
consequential decisions to a qualified attorney or the relevant copyright office.

### 5.3 Distribution, monetization, and disclosure

- **[Documented]** Suno officially says paid-tier songs can be distributed to Spotify, Apple Music,
  etc.; free-tier songs cannot be monetized.
- **[Documented]** Distributors (e.g. DistroKid) allow AI music in 2026 but require proof of
  commercial rights — you must have been on a **paid tier when the audio was generated** — and you
  must be the exclusive holder of 100% of the material (don't use someone else's lyrics/melody).
- **[Documented] AI disclosure:** From late 2025, DSPs began enforcing the **DDEX** industry
  standard for AI-disclosure metadata; a track using Suno-generated audio should be flagged as
  AI-generated during distributor upload. This is a contractual/labeling requirement, not optional.
- **[Documented] Content ID:** As of mid-2025, fully AI-generated audio is **not eligible** for
  YouTube Content ID. You can monetize your *own* videos using the track, but you cannot claim
  Content ID to monetize third-party uses. Do not promise a client Content ID revenue on pure Suno
  audio.

### 5.4 The Warner Music Group settlement and the licensing landscape

- **[Documented]** On **2025-11-25**, Warner Music Group and Suno announced a **settlement of WMG's
  copyright suit plus a licensing partnership**. Suno gets licensed access to WMG catalog as source
  material for "next-generation licensed AI music"; artists/songwriters can **opt in** to features
  that let users create content using their name, image, likeness, voice, and compositions. Suno
  also **acquired Songkick** (concert discovery) from WMG. **Financial terms were not disclosed.**
- **[Documented — anticipated]** Suno signaled 2026 changes under the deal: models trained on
  licensed WMG recordings are forthcoming, "you'll still be able to create original songs the way
  you do today," and download access remains monthly-limited for paid users while **Suno Studio
  users keep unlimited downloads**. Treat specifics as forward-looking; re-verify.
- **[Documented]** Udio settled with **Universal Music Group** on **2025-10-29** (payment + license
  for a joint AI platform). So by mid-2026, of the three majors: **UMG ↔ Udio** and **WMG ↔ Suno**
  have deals.

### 5.5 Litigation that is still open (as of 2026-07-10)

- **[Documented]** **Sony Music has NOT settled** with Suno (or Udio). Sony's fair-use cases are
  expected to produce a pivotal ruling around **summer 2026** that could set precedent for the whole
  sector. **Do not tell a client the legal question is settled.**
- **[Documented]** **Suno is contesting** on fair-use grounds — it filed a motion for summary
  judgment in **March 2026** arguing that training on copyrighted music is transformative use under
  17 U.S.C. §107. Reported **UMG–Suno settlement talks hit an impasse** (April 2026).
- **[Documented]** Additional suits: the **American Federation of Musicians (AFM)** sued UMG and WMG
  over how the Suno/Udio settlements were structured, and **independent musicians filed class
  actions** arguing the major-label deals don't protect smaller rights holders.
- **Advisory takeaway [Heuristic]:** the settlements reduce risk for *major-label* catalog exposure
  but do not immunize Suno output generally; training-data litigation and the human-authorship
  problem remain live. Advise clients that Suno output carries residual legal uncertainty and that
  high-stakes commercial uses (national ad, sync, brand campaign) warrant legal review and, where
  possible, human-authored components.

---

## 6. The API situation (verify before recommending any integration)

**[Documented, verified 2026-07-10]:**

- Suno has historically had **no official public API** — no developer console, no self-serve key
  page, no public SDK, no published docs.
- On **2026-07-01**, Suno CPO Jack Brody announced Suno is **opening an API partner program**,
  starting with a **curated group of partners** (application via an intake form), framed as a
  precursor to a "partner-powered model." **No public launch timeline** was given, and it is **not**
  self-serve as of 2026-07-10.
- **Third-party "Suno APIs" (e.g. sunoapi.org, PiAPI, gcui-art/suno-api and similar) are
  unofficial.** They work by reverse-engineering Suno's private web endpoints or by automating a
  logged-in browser (often with CAPTCHA-solving). They are **not authorized by Suno** and their use
  generally **violates Suno's Terms of Service** (which prohibits unauthorized automated access).
- **[Heuristic / advisory]** "Commercial license" guarantees advertised by unofficial API resellers
  are **not something they can lawfully grant**, because they themselves operate outside Suno's
  sanctioned ecosystem, and the underlying copyright caveat (§5.2) still applies. If a production
  team needs programmatic Suno access today, the compliant path is to **apply to the official
  partner program** and wait, not to wire up a scraper. Flag any request to build on an unofficial
  Suno API as a ToS-violation and legal risk before proceeding.

---

## 7. Safety, consent, and rights hygiene

- **Real-artist voices/likeness:** Only use an artist's voice, name, or likeness where they have
  **opted in** through the official WMG (or comparable) program, or where you otherwise hold rights.
  Generating "make it sound like [named living artist]" for release is a rights and publicity-rights
  risk even when the audio is AI-made.
- **Lyrics you don't own:** Don't feed copyrighted lyrics (or melodies via Cover) you have no license
  to. Distributors will pull tracks and blacklist accounts for it.
- **Disclosure:** Comply with DSP AI-disclosure (DDEX) at upload; don't pass AI tracks off as
  human-recorded where disclosure is required.
- **Don't overstate ownership:** When advising, separate "you can use it commercially" (true on paid
  tier) from "you own an enforceable copyright" (often false for pure AI output).
- **Not legal advice:** For a specific commercial deal, sync placement, or campaign, route the client
  to a qualified music/IP attorney. This skill informs; it does not replace counsel.

---

## 8. Worked examples (illustrative, not required formulas)

### Example A — Release-ready pop track for a paid client
**Intent:** upbeat indie-pop single a small brand will use in a monetized YouTube ad.
**Tier decision:** must generate on **Pro/Premier** (commercial rights require paid-at-creation).
Write original lyrics in-house to add a human-authored copyright layer.
**Style field:** `indie pop, bright and hopeful, 112 bpm, jangly electric guitar, warm female
vocal, punchy live drums, radio-ready mix`
**Exclude styles:** `lo-fi, trap, autotune-heavy`
**Lyrics field (human-written):**
```
[Verse 1]
<your original lyrics>
[Pre-Chorus]
<your original lyrics>
[Chorus]
<your original, repeated hook>
[Verse 2]
...
[Bridge]
...
[Chorus]
<same hook>
[Outro]
```
**Why:** paid tier secures commercial use; original lyrics improve the human-authorship position;
short structural tags give a clean radio arrangement.
**Expected:** a clean, distributable track. **Failure modes:** genre words leaking into lyrics if
placed in the wrong field; pure-AI melody may still be **non-copyrightable** (§5.2).
**Rights note the agent must surface:** flag DDEX AI-disclosure at DistroKid upload; note Content ID
is unavailable on the AI audio; note residual litigation uncertainty.

### Example B — Instrumental bed for a podcast (budget-conscious)
**Intent:** 60–90s calm instrumental loop for a personal, non-monetized hobby podcast.
**Tier decision:** if truly non-commercial and personal, free tier is *permissible* but requires
**attribution to Suno** and forbids monetization; if the podcast has any sponsorship, it's
commercial → **must be paid tier**. Clarify monetization before choosing.
**Style field:** `ambient lo-fi, calm and reflective, 80 bpm, soft Rhodes piano, mellow tape hiss,
gentle vinyl crackle, no drums`
**Lyrics field:** `[Instrumental]` (or use the Instrumental toggle)
**Why:** naming instruments and "no drums" plus `[Instrumental]` reliably yields a vocal-free bed.
**Failure modes:** stray vocals if the instrumental flag isn't set; free-tier output can't be used
the moment the show takes a sponsor.

### Example C — Client asks "wire Suno into our app via an API"
**Correct response:** Explain there is **no official self-serve API** as of 2026-07-10; Suno opened a
**curated partner program (announced 2026-07-01)** you can **apply** to. Warn that third-party "Suno
APIs" are **unofficial scrapers that violate Suno's ToS** and cannot lawfully guarantee commercial
licenses. Recommend applying to the official program and, meanwhile, not building on a scraper.
**Critical failure:** recommending a third-party Suno API as if it were official/authorized, or
promising it confers commercial rights.

---

## Sources (verified 2026-07-10)

Official / first-party:
- Suno Model Timeline — https://help.suno.com/en/articles/5782721
- Suno Terms of Service (revised 2026-03-26) — https://suno.com/terms-of-service
- "Does Suno own the music I make?" — https://help.suno.com/en/articles/2416769
- "Do I have the copyrights to songs I made?" — https://help.suno.com/en/articles/2746945
- "Can I distribute my songs to Spotify, etc?" — https://help.suno.com/en/articles/2410177
- Suno v5.5 blog — https://suno.com/blog/v5-5
- Suno release notes — https://suno.com/release-notes

Industry press (secondary, labeled):
- Suno–WMG settlement/partnership — https://www.rollingstone.com/music/music-features/suno-warner-music-group-ai-music-settlement-lawsuit-1235472868/
- 2026 changes under Warner deal — https://www.digitalmusicnews.com/2025/12/22/suno-warner-music-deal-changes/
- Suno API partner program — https://www.musicbusinessworldwide.com/suno-explores-developer-api-seeking-apps-that-unlock-experiences-generative-music-makes-possible-for-the-first-time/ and https://www.digitalmusicnews.com/2026/07/03/suno-is-opening-an-api-partner-program/
- UMG–Udio settlement — https://www.rollingstone.com/music/music-features/ai-music-universal-music-group-settlement-udio-1235457945/
- UMG–Suno settlement impasse (Apr 2026) — https://www.digitalmusicnews.com/2026/04/09/suno-universal-music-lawsuit-settlement-impasse/
- AFM suit over settlements — https://www.hollywoodreporter.com/music/music-industry-news/musicians-union-lawsuit-ai-song-generator-settlement-1236614835/
- V5 launch coverage — https://musically.com/2025/09/25/suno-launches-v5-claiming-its-the-worlds-best-music-model/
