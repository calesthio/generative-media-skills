# Evaluation — audioshake-stem-separation

Answer key and scoring specification. The evaluated agent sees only `SKILL.md` and the task; the scorer uses this file. Facts reflect AudioShake documentation verified 2026-07-10; if the agent cites newer live figures that contradict these, verify against the source before penalizing.

Scoring per item: **2** = all required points, no critical failure; **1** = mostly correct, minor omissions; **0** = missing core points or any critical failure.

---

## Part 1 — Knowledge questions

### K1. What does AudioShake do, and what is it *not* for?
**Expected:** It is a source-separation service — it decomposes one existing mixed recording into isolated stems (vocals, drums, DME, per-speaker, etc.). It does **not** generate/synthesize, compose, mix, or master audio.
**Required points:** separation ≠ generation; operates on an existing mix; lists at least music-stem and DME/speech capabilities.
**Critical failure:** describing it as an audio *generator* or claiming it creates new music.

### K2. Base URL, auth, and the current API surface.
**Expected:** Base `https://api.audioshake.ai`; auth via `x-api-key` header. Current interface is the **Tasks API**: `POST /assets` (upload), `POST /tasks` (create), `GET /tasks/{id}` (poll), plus `POST /webhooks`. The older **Jobs** API (`/job`, `/upload`, per-job `callbackUrl`) is legacy.
**Required points:** `x-api-key` header; `POST /tasks`; assets-or-url input; Tasks supersedes Jobs.
**Disqualifying:** claiming OAuth/bearer-token auth, or that keys go in a query string.

### K3. How is a task structured, and what are the target/format limits?
**Expected:** One source (`url` **or** `assetId`, mutually exclusive) plus a `targets` array of **1–20 unique** targets, each `{ model, formats }`. Formats: wav/mp3/flac/aiff (audio), mp4 (video), json/srt/txt (text), availability varying by model.
**Required points:** exactly one source field; 1–20 targets; per-target model+formats.
**Minor:** exact upper bound (20) — award full if agent says "up to ~20/multiple."

### K4. How does billing work?
**Expected:** Credit-based, charged **per minute of source audio, per target model, rounded up to the next whole minute**. Rates vary by model (e.g. instrument stems 1.0/min, DME 1.5/min, `multi_voice` 10.0/min, `music_detection` 0.5/min). 10 free credits on signup.
**Worked check:** a 3:10 track with `vocals`+`instrumental` = ceil(3:10)=4 min × 2 targets × 1.0 = **8 credits**.
**Required points:** per-minute × per-target; rounding up; rates differ by model.
**Critical failure:** claiming per-song flat pricing, or that adding targets is free.

### K5. How does an agent retrieve results, and what is the catch?
**Expected:** Poll `GET /tasks/{id}` or register a webhook; targets go `processing`→`completed`|`error`. Output download URLs are **presigned and expire ~1 hour** — download promptly or use `writeDestination` to write to your own S3.
**Required points:** poll or webhook; 1-hour expiry; download or write-destination.
**Critical failure:** assuming results are stored indefinitely.

### K6. Input/output formats and unsupported inputs.
**Expected:** Input audio WAV/AIFF/FLAC/MP3/AAC (to 192 kHz); video MP4/MOV (audio extracted, video ignored). Output WAV/MP3/FLAC/AIFF, MP4, JSON/SRT/TXT. **Not supported:** DRM/encrypted content and multi-channel/surround (5.1) — must downmix.
**Required points:** at least the common audio ins/outs; DRM and surround unsupported.

### K7. Name the DME targets and the multi-speaker model with its constraints.
**Expected:** DME (1.5/min each): `dialogue`, `effects`, `music_fx` (music+effects, dialogue removed). Multi-speaker: `multi_voice` — one stem per speaker, isolates each even through overlap; **10.0/min**, ≤ **1.5 hours**.
**Required points:** the three DME model names; `multi_voice` = one stem per speaker; its high cost or duration cap.

### K8. Transcription vs. alignment.
**Expected:** `transcription` = automatic line-level timestamped lyrics; `alignment` = precise word-level (and line-level) timing but **requires a supplied transcript** (`transcriptUrl`/`transcriptAssetId`). Both ≤ 45 min, 1.0/min.
**Critical failure:** claiming `alignment` transcribes from scratch, or that `transcription` gives word-level timing.

---

## Part 2 — Production-decision questions

### P1. Karaoke deliverable: which targets?
**Scenario:** instrumental backing + on-screen lyrics for a licensed 3-minute song.
**Expected decision:** `instrumental` (+ optionally `vocals` as a near-free guide) and `transcription` for timed lyrics. Do **not** request drums/bass/etc. unless the product plays them.
**Reasoning to demonstrate:** match targets to deliverable; extra stems waste credits; add `alignment` only if accurate lyrics already exist and tight sync matters.
**Penalize:** requesting a full multi-stem split "to be safe"; ignoring lyric timing entirely.

### P2. "Remove one instrument" for a practice track.
**Expected decision:** request the target instrument with **`residual: true`** to get the complement in a single target, rather than requesting every other stem and re-summing.
**Reasoning:** cheaper, avoids reconstruction error and missing-energy gaps.
**Penalize:** requesting all-but-one stems and manually summing without noting cost/quality downside.

### P3. Localization M&E.
**Scenario:** episode stereo mixdown to be dubbed into another language.
**Expected decision:** `dialogue` (translation/ADR reference) + `music_fx` (bed under the new voiceover). `effects` separately only if music and effects must be independent.
**Reasoning:** the bed must retain music+SFX when dialogue is removed; verify dialogue+bed nulls to the original; watch for residual-dialogue bleed in the bed.
**Penalize:** requesting only `dialogue` and discarding the bed; forgetting the M&E deliverable.

### P4. Noisy, reverberant multi-speaker interview — order of operations.
**Expected decision:** clean **first** (`speech_dereverb`, and `speech_denoise` if noisy), then run `multi_voice` on the cleaned audio.
**Reasoning:** `multi_voice` isolates but doesn't fix a bad room; cleaning first yields better per-speaker stems and avoids re-running the expensive (10.0/min) model. Note the 1.5-h cap.
**Critical failure:** running `multi_voice` on the raw boomy source and calling it done; ignoring the cost of `multi_voice`.

### P5. When to choose a local open model (Demucs) instead of AudioShake.
**Expected decision:** Demucs/HTDemucs (local, free, ~4-stem) when budget is ~zero at high volume, audio can't be uploaded (privacy/NDA), unlimited offline runs are needed, or a good-not-best 4-stem split suffices. AudioShake when top measured quality is needed, or for capabilities Demucs lacks — DME, `multi_voice`, transcription/alignment, music detection/identification, and fine stems (`guitar_acoustic`, `keys`, `strings`, `wind`).
**Reasoning:** decision driven by constraints (cost, privacy, capability, SLA), not SDR alone; may prototype locally then send broadcast-critical/DME/transcription jobs to AudioShake.
**Penalize:** "AudioShake is always best" with no constraint analysis; claiming Demucs offers DME/multi-speaker/transcription (it does not).
**Note:** the specific ~2 dB / ~1 dB SDR advantage is a first-party claim — an agent that hedges it appropriately should not be penalized; an agent that states it as independent fact should be marked down slightly.

### P6. Confidential unreleased master — data handling.
**Expected decision:** because AudioShake's public privacy policy does not clearly state whether uploads are used to improve models, obtain a written data/retention (DPA/enterprise) commitment, or keep the audio off the cloud using the on-device SDK / a local model.
**Reasoning:** privacy risk for confidential audio; don't assume deletion/non-use.
**Critical failure:** uploading confidential audio with no caveat about retention/training.

### P7. Real-time in-app karaoke (music removal on device).
**Expected decision:** the on-device **SDK** (real-time `AudioShakeSeparator`), not the cloud Tasks API, because the workflow is low-latency/real-time and possibly offline.
**Reasoning:** cloud round-trips can't meet real-time latency; SDK runs on-device across iOS/Android/desktop.

---

## Part 3 — Applied production tasks

### A1. Write the Task request for a remix stem set.
**Request:** "Give me the API request to pull lead vocals, drums, bass, and guitar out of a song I've uploaded as `asset_123`, as WAVs, and make sure the stems still add back up to the full mix."
**Expected approach:** `POST /tasks` with `assetId`, targets for `vocals_lead`, `drums`, `bass`, `guitar`, **plus** `other-x-guitar` (or `other` + no guitar) so residual energy is captured, all `formats: ["wav"]`.
**Successful output characteristics:** correct endpoint/auth mention; `assetId` (not `url`); the four requested stems; a residual/`other` target with justification that omitting it drops energy; note on per-target billing.
**Rubric:** 2 = valid request incl. residual target + reconstruction rationale; 1 = valid request but no residual/other (stems won't re-sum); 0 = wrong endpoint/auth, or requests generation, or uses both url+assetId.
**Critical failures:** claiming stems auto-reconstruct without a residual target; inventing model names not in the catalog.

### A2. Diagnose a bad stem.
**Request:** "The `vocals` stem from my track sounds watery/underwater and there's a snare ghost in it. What's wrong and how do I fix it?"
**Expected approach:** identify **musical-noise/spectral-hole artifacts** ("watery") and **drum bleed** (snare ghost). Fixes: (1) feed a higher-quality source (WAV master, not a low-bitrate MP3) — quality tracks input; (2) try `vocals_lead`/`vocals_backing` to cut bleed; (3) finish the isolated stem in a spectral editor (e.g. RX) rather than re-running the source; note that up-transcoding a lossy file won't help.
**Rubric:** 2 = names both defects + at least two concrete, correct fixes incl. source-quality point; 1 = identifies defects with one generic fix; 0 = misattributes cause (e.g. "the API is broken") or suggests only re-submitting unchanged.
**Critical failure:** advising to up-convert an MP3 to WAV to improve separation.

### A3. Review checklist for a delivered DME set.
**Request:** "I got `dialogue` and `music_fx` stems back for an episode. How do I check they're broadcast-ready?"
**Expected approach:** solo each stem; check `music_fx` for residual-dialogue bleed under former dialogue positions; check `dialogue` for music/SFX leakage; **null-test** dialogue+music_fx against the original mix to confirm nothing was lost or phase-rotated; if the bed has dialogue bleed, A/B a `residual`-derived bed or add `effects` and rebuild.
**Rubric:** 2 = solo + sum/null-test + at least one named defect (bleed) + a repair path; 1 = solo listening only; 0 = "just listen once, it's fine" with no reconstruction/null check.
**Critical failure:** no verification that the stems reconstruct the original (missing-energy risk unflagged).

### A4. Rights advisory.
**Request:** "I want to extract the a cappella from a chart hit and release a remix."
**Expected approach:** flag that separating the recording creates a **derivative** — it does not grant rights; releasing/remixing a commercial master needs master + publishing (sync/sample/remix) clearance from the rights holders, independent of AudioShake. AudioShake's Terms require the user to warrant they hold the necessary rights and to indemnify; infringing uploads can be removed and repeat offenders cut off. Advise confirming clearance with the rights holders/counsel; do not present as legal advice.
**Rubric:** 2 = clearly states separation ≠ clearance, names the rights holders/clearances needed, cites the warranty/indemnity obligation; 1 = general "you need permission" without the derivative/clearance reasoning; 0 = says separation makes it usable, or that owning the file / a subscription grants remix rights.
**Critical failure:** telling the user the extracted a cappella is theirs to release.

### A5. Cost estimate.
**Request:** "Roughly how many credits to run `dialogue` + `music_fx` + `effects` on a 47-minute podcast?"
**Expected approach:** ceil(47) = 47 min × 3 DME targets × 1.5 credits/min = **≈ 211.5 credits** (each target billed independently per minute). Should show the per-minute-per-target method and rounding.
**Rubric:** 2 = correct method and figure (accept ~210–212); 1 = right method, arithmetic slip; 0 = flat/per-file pricing or forgets per-target multiplication.
**Critical failure:** treating multiple targets as one charge.

---

## Cross-cutting critical failures (any → cap item at 0)

- Describing AudioShake as generating/synthesizing audio.
- Inventing endpoints, model names, or credit rates not supported by the catalog (or presenting them without hedging as live-verifiable).
- Advising upload of confidential/unreleased audio with no data-handling caveat.
- Asserting that separating a copyrighted recording grants any right to use, release, or monetize it.
- Presenting AudioShake's first-party benchmark numbers as independently established fact without qualification.
