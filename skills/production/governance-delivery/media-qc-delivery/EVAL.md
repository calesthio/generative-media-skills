# Evaluation: media-qc-delivery

Use this file as the answer key and scoring guide for agents evaluated on `media-qc-delivery`. The evaluated agent should receive the user task and `SKILL.md` only, never this file.

Score out of 100. A passing response should be usable in real media production, separate documented facts from observations and heuristics, and prevent incorrect or incomplete delivery.

## Core scoring dimensions

| Dimension | Points |
|---|---:|
| Delivery triage and spec authority | 15 |
| Technical QC competence | 20 |
| Perceptual, generated-media, and accessibility QC | 15 |
| Platform/client delivery planning | 15 |
| Packaging, filenames, versions, checksums, manifests | 15 |
| Rights, provenance, localization, and acceptance governance | 10 |
| Communication clarity and evidence labeling | 10 |

Critical failures can cap the score regardless of points:

- Caps at 60 if the response gives one universal export spec without asking or identifying destination/spec authority.
- Caps at 60 if it ignores captions/accessibility for speech-bearing public media.
- Caps at 55 if it omits rights/provenance for AI-generated or mixed-source assets.
- Caps at 50 if it recommends delivery without any checksum/manifest/version control for a client/broadcast/streamer/high-risk package.
- Caps at 50 if it treats a social platform brand as one single spec rather than placement-specific.
- Caps at 45 if it tells the user to waive legal/rights/accessibility or corrupt-playback problems casually.
- Caps at 40 if it invents unsupported platform requirements and presents them as current documented facts.

## Knowledge questions

### 1. Why is "export as MP4 H.264 1080p" not a sufficient delivery instruction?

Expected answer:

- Destination, placement, role, and authority determine specs.
- Broadcast/streamer, ad trafficking, social upload, ecommerce, localization, archive, and review files can require different containers, codecs, durations, captions, audio, metadata, color, package structure, and QC.
- H.264 MP4 may be acceptable for some web/social review or upload cases but is not a universal master or professional delivery format.
- A strong answer asks for or identifies the delivery spec and labels any default as a heuristic.

Penalize:

- Claims MP4/H.264 is always safe.
- Ignores audio/captions/color/versioning.
- Does not distinguish master from derivative.

### 2. What are documented facts, empirical observations, and production heuristics in QC reporting?

Expected answer:

- Documented facts come from client/platform specs, standards, or file-probe data; volatile platform facts need verification dates.
- Empirical observations come from playback review, test uploads, meters, scopes, or automated QC results.
- Production heuristics are practical defaults used when no binding spec exists and must not be presented as rules.

Required points:

- Must include all three categories.
- Must include at least one example of each.

### 3. What should trigger a rejection or hold before delivery?

Expected answer should include several of:

- Wrong version/file/language/market/duration.
- Codec/container/raster/fps/audio/caption mismatch against binding spec.
- Corrupt/unplayable file or decode errors.
- Missing required captions, subtitles, stems, metadata, or sidecars.
- Loudness/true peak outside mandated tolerance.
- Missing checksum or checksum mismatch.
- Legal/brand/rights/provenance issue.
- Generated-media artifacts that damage truth, product accuracy, likeness, or brand trust.
- Platform/ad portal rejection.

Penalize:

- Treating visible artifacts or rights issues as minor if the file technically plays.
- Recommending delivery first and fixing later for public/paid/high-risk assets.

### 4. Why should checksums be generated after final files are placed in the delivery package?

Expected answer:

- The checksum should represent the exact bytes being handed off.
- Re-encoding, copying, metadata changes, or replacing sidecars changes the hash.
- Manifest verification after transfer confirms fixity/integrity.
- For platforms that transcode after ingest, verify the uploaded source before ingest or validate the platform's ingest/playback result instead of expecting source and transcode checksums to match.

### 5. What is the difference between captions and subtitles for QC purposes?

Expected answer:

- Subtitles often focus on spoken dialogue/translation.
- Captions, especially accessibility captions/SDH, include dialogue plus relevant non-speech sound, speaker IDs, and timing needed by deaf/hard-of-hearing viewers.
- QC must check sync, completeness, readability, line breaks, spelling, speaker identification, non-speech cues, safe area, and language/locale.

Penalize:

- Saying captions are just subtitles in another file format.

## Production-decision scenarios

### 6. User says: "Send the final ad to TikTok, Meta, and YouTube. Just make one file."

Strong answer:

- Refuses to assume one file fits all placements.
- Asks for or infers from media plan the placements: TikTok In-Feed, Meta Feed/Reels/Stories, YouTube Shorts/in-stream, etc.
- Recommends separate derivatives by aspect ratio, duration, safe zone, captions, and file-size constraints.
- Uses public platform specs only as dated facts and says they were verified or must be verified at delivery time.
- Provides a delivery sheet and naming/version scheme.
- Includes QC for first seconds, safe zones, captions, audio-on/off comprehension, legal copy, and checksums.

Weak answer:

- Produces a single 16:9 1080p MP4 for every platform.
- Ignores placement-specific safe zones and durations.

### 7. User says: "The streamer wants the episode package tomorrow. Can we deliver the MP4 we used for review?"

Strong answer:

- Treats streamer delivery as high risk and asks for the streamer delivery spec.
- Explains that review MP4 is not a substitute for required master/package.
- Checks whether IMF, ProRes, MXF/AS-11, WAV stems, captions/timed text, slate/timecode, audio layout, loudness, HDR/color, manifests, and automated QC are required.
- Recommends holding delivery until required package components pass QC or obtaining written waiver from the acceptance owner.

Weak answer:

- Says yes because the MP4 looks fine.
- Does not mention package validation, audio/captions, or loudness.

### 8. User has a speech-bearing product video for a public website and says captions are optional.

Strong answer:

- Flags captions/accessibility as a requirement/risk for many public synchronized media contexts.
- Recommends providing captions and checking WCAG/Section 508 obligations for the user's organization.
- Differentiates captions from subtitles.
- Includes caption QC and delivery of WebVTT/SRT or platform-required format.

Weak answer:

- Accepts "optional" without noting accessibility risk.

### 9. User wants to archive final AI-generated images and videos for a client DAM.

Strong answer:

- Creates a package with final assets, delivery sheet, rights/provenance ledger, prompts/model/tool metadata where approved, licenses/releases, captions/audio if relevant, checksums, and delivery notes.
- Recommends SHA-256 if no hash algorithm is mandated.
- Explains that C2PA/provenance metadata is useful but not a substitute for rights clearance.
- Uses stable filenames with project, role, locale/market, aspect, version, and date.

Weak answer:

- Uploads loose files with no ledger or manifest.
- Treats AI generation as automatically cleared.

## Applied tasks

### 10. Create a QC plan for a mixed-source 30-second paid social ad

User request:

> We have a 30-second ad made from client product footage, stock clips, AI-generated lifestyle shots, generated VO, licensed music, and burned-in captions. It needs 9:16 and 1:1 versions for paid social tomorrow. Give me a final QC and delivery plan.

Expected approach:

- Triage destination/placements and spec authority.
- Build delivery sheet fields.
- Export separate 9:16 and 1:1 variants from approved timeline/master.
- Check source conformance, generated shot artifacts, product accuracy, stock/music/VO rights, captions, safe zones, audio, legal copy, and platform duration/file-size constraints.
- Run technical inspection with ffprobe/MediaInfo and loudness/true peak check.
- Watch final exports, not just timeline.
- Create filenames, versioning, checksums, manifest, delivery notes.
- State acceptance/rejection criteria and what needs human approval.

Rubric (20 points):

- 4 spec/destination triage.
- 4 technical inspection details.
- 4 perceptual/generated-media/social-safe-zone checks.
- 3 rights/provenance/licensing checks.
- 3 packaging/naming/checksum plan.
- 2 clear acceptance/hold/reject criteria.

Critical failures:

- No separate aspect-ratio QC.
- No rights/provenance checks.
- No caption checks.

### 11. Review a flawed delivery note

Input:

```text
Final attached. MP4 is good for all platforms. Captions are burned in. Didn't include the source files because they're huge. I renamed it final_v2.mp4 after fixing the logo.
```

Expected critique:

- "Good for all platforms" is unsupported; specs/placements not identified.
- "Final" filename lacks project/destination/version/date and was reused/renamed after changes.
- Renaming after fixing logo does not establish a new export or checksum.
- No manifest/checksum.
- No delivery sheet.
- No authority/verification date.
- No technical metadata: duration, fps, raster, codec, audio, loudness, color, captions.
- No rights/provenance or source package/ledger explanation.
- Burned-in captions may be insufficient if sidecars are required.
- Large source files may be acceptable to omit only if deliverable role does not require source package and omission is documented.

Strong output should rewrite the delivery note with missing fields and hold conditions.

### 12. Decide whether to waive a mismatch

Scenario:

> A client asked for 25 fps, but the delivered file is 29.97 fps. The platform accepts upload and it looks okay. The campaign launches in two hours.

Expected answer:

- This is a documented spec mismatch and should be held or escalated.
- Platform acceptance does not override the client spec unless the client/acceptance owner approves a waiver.
- Explain risks: cadence, downstream transcode, regional broadcast/ad ops mismatch, inconsistent package records.
- Recommend either re-export to 25 fps from the correct timeline/conform if feasible or obtain explicit written waiver with the mismatch recorded in delivery notes.
- Do not silently deliver.

Critical failure:

- Advises delivery just because the platform accepts it.

## Source and fact-check expectations

A high-scoring answer should not need to recite source URLs, but it should behave as if facts are sourced:

- It dates volatile platform specs when invoking them.
- It uses "client spec prevails" reasoning.
- It does not make unsupported universal claims about YouTube, TikTok, Meta, Google Ads, Netflix/streamers, broadcast, or CTV.
- It knows standards are not interchangeable: IMF, AS-11, HLS, WebVTT, EBU R 128, ITU-R BS.1770, WCAG/Section 508, BagIt, SHA-256, C2PA, and IPTC solve different problems.

## Excellent-response characteristics

Excellent responses:

- Start with the delivery context and spec authority.
- Convert abstract QC into a concrete delivery sheet, package structure, filenames, and acceptance criteria.
- Include both automated and human/perceptual QC.
- Mention exact checks that catch common AI media failures.
- Separate technical readiness from legal/accessibility/provenance readiness.
- Treat localization and variant packages as separate deliverables, not afterthoughts.
- Are clear about what is blocked, what can be waived, who must approve, and what evidence supports the decision.
