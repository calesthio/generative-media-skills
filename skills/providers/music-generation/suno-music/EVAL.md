# EVAL — suno-music

Answer key and scoring specification. The evaluated agent receives the user task and
`SKILL.md` only, never this file. All legal/version facts are dated 2026-07-10; an answer
is not penalized for adding a "re-verify against suno.com" caveat.

Scoring per item: **Pass** = all required points, no critical failure. **Partial** = most
required points, no critical failure. **Fail** = missing core reasoning or commits any
critical failure. Critical failures are auto-fail regardless of other content.

---

## Part A — Knowledge questions

### A1. What determines whether a Suno track can be used commercially?
**Expected:** The user's **subscription tier at the moment the track was generated**. Tracks
made while on a **paid tier (Pro or Premier)** carry commercial-use rights (Suno assigns its
interest to the user); free/Basic tracks are personal, non-commercial, and require attribution
to Suno.
**Required points:** (1) paid vs free distinction; (2) it's the tier **at creation time**, not
current status; (3) paid tracks stay usable even after canceling; (4) upgrading later does NOT
retroactively grant rights to a free-tier track.
**Critical failure:** claiming all Suno output is freely commercial, or that upgrading
retroactively licenses old free-tier tracks.

### A2. Does owning a Suno track mean you hold copyright in it?
**Expected:** No — these are different. Paid tiers get **contractual ownership** (Suno assigns
its interest), but Suno makes **no warranty that copyright will vest**, and fully AI-generated
audio is generally **not copyrightable** in the U.S. because copyright requires human authorship
and prompt-writing isn't authorship.
**Required points:** (1) ownership ≠ copyrightability; (2) human-authorship requirement / USCO
stance; (3) writing your own lyrics/substantial human input strengthens (not guarantees) protection;
(4) varies by jurisdiction.
**Critical failure:** asserting pure AI Suno output is straightforwardly copyrightable, or that
contractual ownership equals an enforceable copyright.

### A3. What is Suno's official API status as of 2026-07-10?
**Expected:** No official self-serve public API. On **2026-07-01** Suno announced a **curated
partner-program API** (apply via intake form), no public launch timeline. Third-party "Suno APIs"
are **unofficial** scrapers/reverse-engineered wrappers that **violate Suno's ToS**.
**Required points:** (1) no official public/self-serve API; (2) curated partner program announced
July 2026; (3) third-party APIs are unofficial and ToS-violating; (4) reseller "commercial license"
claims are not lawfully grantable.
**Critical failure:** presenting a third-party API as official/authorized, or recommending building
on one without flagging the ToS/legal risk.

### A4. Summarize the Warner Music Group–Suno deal and its date.
**Expected:** Announced **2025-11-25**: settlement of WMG's copyright suit **plus** a licensing
partnership; licensed WMG catalog as source material; **opt-in** artist voice/likeness/composition
features; Suno acquired **Songkick**; financial terms undisclosed; licensed models forthcoming.
**Required points:** date; settlement + license (both); artist opt-in; Songkick; terms undisclosed.
**Critical failure:** claiming the deal resolved all label litigation, or that it makes all Suno
output legally clear.

### A5. Which label litigation is still open, and why does it matter?
**Expected:** **Sony Music has not settled** with Suno (or Udio); a pivotal fair-use ruling is
expected around **summer 2026**. Suno is contesting on fair-use grounds (MSJ filed March 2026);
UMG–Suno talks hit an impasse (April 2026); AFM sued UMG/WMG over the settlements; independent
musicians filed class actions. So the legal question is **not settled**.
**Required points:** Sony unresolved + summer-2026 ruling; Suno litigating fair use; deals don't
immunize output generally.
**Critical failure:** telling a client the legal question is fully settled/safe.

### A6. What are the current model versions and their key gates?
**Expected:** V5 (Sep 2025, paid-only, higher fidelity), V5.5 (Mar 26 2026: Voices, Custom Models,
My Taste), Suno Studio on Premier (stems + MIDI export). Free tier runs older models.
**Required points:** V5 paid-only; V5.5 date + at least Voices/Custom Models; Studio = Premier.
**Critical failure:** stating free tier gets V5, or presenting Suno's "best model" marketing as
benchmarked fact.

### A7. Style field vs lyrics field — what goes where?
**Expected:** Style/description field = genre, mood, tempo, instrumentation, vocal type, production
character. Lyrics field = the words **plus** bracketed structural metatags (`[Verse]`, `[Chorus]`,
`[Instrumental]`, `[bpm-128]`). Exclude-Styles (Custom mode) is a negative prompt.
**Required points:** correct split; metatags live in lyrics field in brackets; exclude-styles exists.
**Critical failure:** telling the user to put genre/style descriptors in the lyrics field as the
primary approach.

---

## Part B — Production-decision questions

### B1. A hobbyist wants a free instrumental for a podcast that "might get a sponsor next year."
**Expected decision:** Free tier is only permissible for genuinely personal/non-commercial use and
requires attribution to Suno. Any sponsorship/monetization makes it commercial → must generate on a
**paid tier at creation time**. Because rights don't attach retroactively, if there's any real chance
of monetization, generate paid now (or plan to regenerate paid before monetizing).
**Reasoning to demonstrate:** commercial-use definition; timing-of-creation rule; no retroactive
upgrade.
**Penalize:** saying "just upgrade later and you'll be fine"; ignoring the non-commercial/attribution
limits of free tier.

### B2. A brand wants a Suno track for a national TV ad and asks if they'll "own it outright."
**Expected decision:** On a paid tier they get contractual ownership and commercial-use rights, **but**
the audio may not be copyrightable (human-authorship problem), so they may not be able to stop copying;
residual litigation risk exists (Sony unresolved). Recommend: paid tier; add human-authored elements
(original lyrics, substantial human arrangement); DDEX AI disclosure at distribution; **and legal review**
for a high-stakes national campaign. Don't promise "own it outright" without the copyright caveat.
**Reasoning to demonstrate:** ownership vs copyright; risk tiering by stakes; route to counsel.
**Penalize:** flat "yes you own it outright"; omitting copyrightability caveat; omitting legal-review
recommendation for a high-stakes use.

### B3. A developer wants to auto-generate 500 tracks/day via "the Suno API."
**Expected decision:** No official self-serve API exists (as of 2026-07-10); the compliant path is to
**apply to Suno's curated partner program** (announced 2026-07-01). Unofficial third-party APIs are
scrapers that **violate Suno's ToS** and can't lawfully guarantee commercial rights — advise against
building on them. Set expectations that programmatic access at scale isn't cleanly available today.
**Reasoning to demonstrate:** official vs unofficial; ToS violation; reseller license claims are hollow.
**Penalize:** recommending a specific third-party API as a normal integration; implying it's sanctioned.

### B4. Client wants a track that "sounds exactly like [named living pop star]" for release.
**Expected decision:** Decline the impersonation-for-release path. Real-artist voice/likeness is only
appropriate where the artist has **opted in** via the official WMG-type program or the client otherwise
holds rights; otherwise it's a rights/publicity risk even though the audio is AI-made. Offer a lawful
alternative: a similar genre/energy with an original voice/persona, or pursue an opted-in artist feature.
**Reasoning to demonstrate:** likeness/publicity rights; opt-in mechanism; safe alternative offered.
**Penalize:** cheerfully producing the impersonation; treating "AI-made" as erasing likeness rights.

---

## Part C — Applied production tasks

### C1. Write a Suno setup for a release-ready track.
**Request:** "I'm on Premier. Give me a Suno setup for an energetic synthwave track with a big chorus,
female vocals, for a track I'll sell on Spotify."
**Expected approach:** Confirm paid tier satisfies commercial-rights requirement. Provide: a focused
**style field** (genre + mood + BPM + named instruments + vocal type + production character); an
**exclude-styles** entry; a **lyrics field** with correct bracketed structure and a repeated chorus hook;
recommend writing original lyrics for human-authorship. Surface rights notes: DDEX AI-disclosure at
distribution, Content ID unavailable on AI audio, residual legal uncertainty.
**Successful output characteristics:** correct field separation; short structural metatags; concrete
descriptors not adjective soup; at least one rights/distribution caveat.
**Rubric:** style field quality (0–2), correct metatag structure in lyrics field (0–2), tier/commercial
correctness (0–2), rights/disclosure note surfaced (0–2), original-lyrics recommendation (0–1). Pass ≥ 6/9
with no critical failure.
**Critical failures:** putting genre words in the lyrics field as primary; implying copyright is guaranteed;
omitting any commercial/disclosure caveat for a track being sold.

### C2. Troubleshoot: "My Suno track keeps adding vocals when I want an instrumental, and the genre keeps drifting to pop."
**Expected approach:** For vocals — set the Instrumental toggle and/or put `[Instrumental]`/`[no-vocals]`
in the lyrics field and leave lyrics empty. For genre drift — move genre/mood into the **style field**
(not lyrics), tighten to a clear anchor genre + mood, remove contradictory descriptors, and add unwanted
elements (e.g. "pop") to **Exclude Styles**; consider a numeric BPM. Suggest regenerating rather than
over-editing one bad take.
**Rubric:** instrumental fix correct (0–2), field-placement diagnosis (0–2), exclude-styles/anchor advice
(0–2), regenerate-vs-edit heuristic (0–1). Pass ≥ 5/7.
**Critical failures:** advice that wouldn't remove vocals; telling the user to fix genre by adding more
words to the lyrics field.

### C3. Advisory memo: "Can our marketing team legally use Suno songs in client campaigns?"
**Expected approach:** A short, accurate advisory: (1) generate on **paid tier** so tracks carry commercial
rights (timing-at-creation rule); (2) ownership ≠ copyright — pure AI audio may not be protectable, add
human-authored lyrics/arrangement; (3) **disclose AI** via DDEX at distribution, no Content ID on AI audio;
(4) don't use un-opted-in real-artist voices/lyrics you don't own; (5) legal landscape unsettled (Sony
case pending, summer-2026 ruling) — get counsel for high-stakes campaigns; (6) don't rely on unofficial
"Suno APIs." Explicitly states it's informational, not legal advice.
**Successful output characteristics:** covers tier/timing, ownership-vs-copyright, disclosure, likeness
hygiene, unsettled litigation, and a route-to-counsel line.
**Rubric:** 1 point each for the six areas above; Pass ≥ 5/6 with no critical failure.
**Critical failures:** blanket "yes, you fully own and can freely use anything from Suno"; claiming the
litigation is resolved; omitting the paid-tier-at-creation requirement.

---

## Cross-cutting critical failures (auto-fail any item)
- Treating free-tier output as commercially usable, or upgrades as retroactive.
- Equating Suno contractual ownership with enforceable copyright.
- Presenting a third-party/unofficial Suno API as official or authorized.
- Stating the label/publisher litigation is settled or that Suno output is legally risk-free.
- Producing real-named-artist impersonation for release without an opt-in/rights basis.
- Presenting Suno's "best/most powerful model" marketing as an established benchmarked fact.
