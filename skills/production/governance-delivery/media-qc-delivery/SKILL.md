---
name: media-qc-delivery
description: Provider-independent media quality control and delivery direction for generated images, video, audio, ads, product content, social clips, broadcast and streaming assets, localization packages, and mixed-source edits. Use when an agent must define final export specs, inspect technical and perceptual quality, check captions/audio/color/accessibility/provenance/rights, create delivery sheets, version filenames, checksums, manifests, package deliverables, set acceptance or rejection criteria, and perform final delivery QA before handoff to a platform, broadcaster, streamer, client, or ad trafficker.
---

# Media QC and delivery

Use this skill at the finish line of media production: after creative approval or near-final assembly, before the files are sent to a client, platform, publisher, broadcaster, streamer, localization vendor, or ad operations team.

Do not invent universal export specs. Delivery is governed in this order:

1. The signed client/platform/broadcaster delivery specification.
2. The campaign media plan, insertion order, distribution platform, or localization brief.
3. Official public platform specs verified for the current date.
4. A conservative house mezzanine plus platform-ready derivatives, clearly labeled as a production heuristic.

If the destination is unknown, ask for it. If the user needs a fast default, deliver a high-quality mezzanine plus common web/social derivatives and state that the package is provisional until the destination spec is confirmed.

## Evidence labels to use in every QC decision

Separate the basis for each QC call:

- **Documented fact**: Comes from a client spec, official platform doc, standards body, or file probe. Cite or name the source and verification date for volatile platform requirements.
- **Empirical observation**: Comes from watching/listening to the asset, reading scopes/meters, test-upload behavior, automated QC output, or a comparison render. Say how it was observed.
- **Production heuristic**: A practical default used when no binding spec exists. Label it as a heuristic, not a rule.

Example evidence language:

> Documented fact: YouTube upload guidance, verified 2026-07-10, recommends uploading at the same frame rate as recorded and lists H.264 High Profile, progressive scan, CABAC, closed GOP, variable bitrate, 4:2:0 chroma subsampling, and audio codec options including AAC-LC, Opus, or Eclipsa for upload encodes.  
> Empirical observation: ffprobe reports the delivered file is 29.97 fps CFR; visual review shows no cadence judder in the 00:00:07-00:00:12 pan.  
> Production heuristic: For an unspecified 1080p web review file, H.264 MP4 with AAC-LC stereo at 48 kHz is a low-friction review encode, but it is not a broadcast master.

## Delivery triage

Before exporting or judging a file, write a delivery intent in plain language:

- **Destination**: platform, broadcaster, streamer, ad network, client DAM, ecommerce PDP, app store, cinema/event screen, archive, localization vendor, or internal review.
- **Deliverable role**: master, mezzanine, platform upload, proxy, thumbnail, caption file, audio stem, open-caption burn-in, localization text package, ad variant, legal archive, or source package.
- **Audience and playback environment**: phone feed, connected TV, desktop web, cinema/event projection, broadcast, in-app ad unit, assistive technology, noisy retail floor, or internal review.
- **Mandated specs**: codec/container, raster, aspect ratio, frame rate, color space/HDR, loudness, channels, captions/subtitles, file-size limits, slate/handles/bars/tone, naming, metadata, manifest, checksum, and due date.
- **Authority**: exact spec document or platform help page; if none, say "house heuristic."
- **Risk level**: low-risk review asset, paid ad trafficking, regulated/broadcast, streamer delivery, legal/rights-sensitive, or public crisis-sensitive.

High-risk deliveries require a second human or independent automated QC pass. Generated-media deliveries require an explicit provenance and rights pass even when the technical file is clean.

## Source-of-truth facts to keep in mind

Use these as anchors, not as a replacement for the current destination spec.

### Documented facts

- **YouTube uploads**: Official YouTube upload guidance, verified 2026-07-10, recommends progressive scan, H.264 High Profile, CABAC, 2 consecutive B-frames, closed GOP, variable bitrate, 4:2:0 chroma subsampling, audio codecs including AAC-LC, Opus, or Eclipsa, and uploading at the same frame rate as the source recording. It lists common frame rates including 24, 25, 30, 48, 50, and 60 fps, while noting that other frame rates are acceptable.
- **TikTok Auction In-Feed Ads**: TikTok Ads Manager guidance, verified 2026-07-10, lists vertical 9:16 as recommended, with at least 540 x 960 px; horizontal 16:9 at least 960 x 540 px; square 1:1 at least 640 x 640 px; video formats including MP4 and MOV; duration up to 10 minutes; and maximum file size of 500 MB for the referenced in-feed unit.
- **Meta ads**: Meta Ads Guide and Help pages are placement-specific and volatile; verify in Ads Manager, the current Ads Guide, or the client media plan at delivery time. Public Meta pages checked on 2026-07-10 showed placement-specific requirements in search/help snippets (for example, MP4/MOV/GIF on some video placements, 16:9 recommendations for in-stream video, and 9:16 recommendations for some Audience Network placements), but some pages were login-gated or temporarily blocked during review. Do not use one Meta placement's spec for all Meta placements.
- **Google Ads**: Google Ads specs pages, verified 2026-07-10, vary by campaign type and asset. Common image sizes include 1200 x 628 and 1200 x 1200, but video ad delivery must be checked against the specific campaign and YouTube ad format.
- **IAB digital video/CTV ads**: IAB Tech Lab guidance defines cross-screen ad file specifications such as resolution, bitrate, frame rate, aspect ratio, color space, and multi-file delivery for intelligent selection and CTV/ad-serving workflows.
- **IMF**: SMPTE describes Interoperable Master Format, ST 2067, as a file-based media format for delivery and storage of audiovisual masters across multiple territories and platforms. It is suited to componentized, multi-version professional delivery, not casual social upload.
- **AS-11 / DPP**: AMWA AS-11 UK DPP HD defines an MXF file format for finished HD program delivery to UK DPP broadcasters. Use AS-11 only when the broadcaster/client asks for it or the receiving workflow is known to support it.
- **HLS**: Apple HLS authoring guidance includes constraints for variant streams; for VOD, peak bitrate should be no more than 200% of average bitrate, and variants may use different frame rates. HLS delivery requires playlist/package validation, not just a playable MP4.
- **Loudness measurement**: ITU-R BS.1770-5 specifies algorithms for program loudness and true-peak measurement. EBU R 128 recommends loudness normalization and true-peak measurement for broadcast workflows. Client/platform targets differ; measure to the target the receiver specifies.
- **Accessibility**: WCAG and Section 508 guidance treat captions, audio description, and synchronized media access as accessibility requirements in many contexts. Captions are not the same as subtitles: captions should include speech plus meaningful non-speech audio and speaker identification when needed.
- **WebVTT**: W3C WebVTT is a timed-text format for captions/subtitles and related time-aligned text tracks with HTML media.
- **Fixity**: IETF RFC 8493 BagIt defines a packaging convention with payload manifests and checksums. NIST lists SHA-2/SHA-3 families as approved hash algorithms; SHA-256 is a sensible default for delivery integrity when no client algorithm is mandated.
- **Provenance**: C2PA Content Credentials store provenance information in a manifest that can include origin, modification assertions, and hashes. Provenance metadata supports transparency but does not by itself clear rights, releases, music licenses, or platform policy.

### Empirical observations worth recording

Record empirical evidence when it affects acceptance:

- Playback on target devices or players.
- Automated QC results and tool versions.
- ffprobe/MediaInfo metadata.
- Loudness meter output and algorithm/version.
- Visual scopes for luma/chroma/HDR, if used.
- Caption spot-check notes.
- Test-upload warnings, transcode results, or platform rejection messages.
- Human review timecodes for artifacts, hallucinated details, lip-sync drift, UI-safe-zone collisions, or rights-sensitive content.

### Production heuristics when no spec exists

Use these only after labeling them as defaults:

- Keep a mezzanine master separate from compressed delivery files. A mezzanine can be ProRes, DNxHR, high-bitrate intra-frame, or image sequence plus WAV depending on the workflow.
- For web review and many platform uploads, MP4/H.264 plus AAC-LC at 48 kHz is broadly compatible, but it is not a substitute for broadcast/streamer specs.
- Preserve source frame rate unless a destination explicitly requires conversion. Avoid mixing 23.976, 24, 25, 29.97, 30, 50, and 59.94/60 fps without an intentional cadence plan.
- Keep text, logos, captions, and product UI inside platform-safe zones; test vertical, square, and landscape variants separately.
- Export derivatives from the approved master or timeline, not from an already compressed social file.
- Leave at least 1 dB true-peak headroom for generic web/social delivery when no loudness target is specified; use the mandated loudness target for broadcast/streaming.
- Prefer SHA-256 checksums for manifests; include MD5 only when the receiver requires legacy MD5.

## QC workflow

### 1. Intake and spec lock

Create a short delivery sheet before export:

| Field | Required entry |
|---|---|
| Project / campaign | Human-readable title |
| Delivery ID | Unique package or work order ID |
| Destination | Platform, client, vendor, broadcaster, streamer, ad network |
| Deliverable role | Master, upload, proxy, captions, stems, localization, source package |
| Spec authority | URL, PDF, contract section, or "house heuristic" |
| Verified date | Required for public platform specs |
| Technical specs | Container, codec, raster, aspect, fps, color, audio, captions |
| Versions | Language, market, cutdown, aspect ratio, revision |
| Rights/provenance requirements | Licenses, releases, AI disclosure, C2PA/metadata, asset ledger |
| Acceptance owner | Person or team that can approve/reject |

Block delivery if the sheet lacks destination, deliverable role, or authority for a paid/public/high-risk delivery.

### 2. Pre-export timeline checks

Check the timeline before rendering:

- Sequence raster, pixel aspect, frame rate, and color management match the intended output.
- Source clips are not scaled beyond acceptable quality unless intentionally stylized.
- Generated images/video do not contain visible watermarks, prompt artifacts, malformed text, distorted hands/faces/product geometry, unsafe brand claims, or unintended copyrighted characters/logos.
- Text overlays are legible at target device size.
- Legal supers, disclaimers, prices, dates, and offer terms match the approved copy.
- Captions/subtitles use approved language, line breaks, reading speed, timing, speaker IDs, and non-speech audio cues.
- Audio stems, music, VO, SFX, and M&E are routed correctly.
- No orphaned mute/solo tracks, disabled effects, offline media, wrong proxy, hidden guide layers, or temporary slates remain unless required.
- If exporting multiple aspect ratios, each crop is composed independently; do not assume center-crop is safe.

### 3. Export

For each file, state why the export settings match the destination. A useful export note includes:

- Filename and version.
- Source sequence or approved master.
- Container and codecs.
- Resolution/aspect/pixel aspect.
- Frame rate and whether CFR/VFR.
- Color space, transfer function, HDR metadata, and bit depth if relevant.
- Audio sample rate, channel layout, codec, bitrate, loudness target, measured loudness, and true peak.
- Caption/subtitle sidecars or burn-ins.
- Timecode start, slate, bars/tone, handles, and act breaks if required.
- Export tool/version and date.

Never rename an old file to simulate a new export. Re-export or copy with a new checksum and manifest entry.

### 4. Automated technical inspection

Use available tools proportionate to risk. Common local checks:

```bash
ffprobe -hide_banner -show_format -show_streams -print_format json "deliverable.mp4"
ffmpeg -hide_banner -i "deliverable.mp4" -filter_complex ebur128=peak=true -f null -
ffmpeg -hide_banner -i "deliverable.mp4" -vf blackdetect=d=0.5:pic_th=0.98 -an -f null -
ffmpeg -hide_banner -i "deliverable.mp4" -af astats=metadata=1:reset=1 -f null -
```

Use the output to verify, not merely to decorate notes. Flag mismatches between target specs and actual stream properties: wrong raster, wrong frame rate, interlacing, unexpected variable frame rate, wrong channel count, missing audio, wrong sample rate, wrong color tags, missing timecode, extreme bitrate, or unexpected duration.

For high-risk broadcast/streamer/ad trafficking, use the client's required automated QC tool or vendor portal when available. If the required tool is unavailable, note that the pass is preliminary.

### 5. Perceptual review

Watch the final exported file, not only the timeline. For short assets, review the whole file. For long assets, review the whole program when risk is high; otherwise do structured spot checks plus all transitions, all generated shots, all title/legal cards, first/last 30 seconds, and all known trouble timecodes.

Check:

- **Video**: dropped/frozen frames, judder, banding, macroblocking, aliasing, flicker, flash risk, bad cadence, visible masks, broken alpha, color shifts, wrong levels, crushed blacks, clipped highlights, bad deinterlace, unsafe crop, illegible text, UI overlap, dead pixels, repeated frames, incorrect slate.
- **Generated imagery**: anatomy, product geometry, brand marks, UI text, medical/legal/financial claims, culturally sensitive symbols, likeness issues, watermarks, obvious model artifacts, prompt leakage, unsafe photorealism claims.
- **Audio**: clipping, distortion, noise, plosives, sibilance, phase cancellation, bad downmix, channel swap, lip-sync, music ducking, M&E completeness, abrupt edits, loudness outliers, true-peak overs, silence where audio is expected.
- **Captions/subtitles**: timing, sync, reading speed, line length, spelling, names, numbers, units, speaker IDs, non-speech sounds, translation fit, text safe area, contrast, overlap with lower thirds.
- **Localization**: language/locale code, translated graphics, VO/subtitle consistency, date/currency formats, cultural or regulatory changes, text expansion, no burned-in source-language captions unless intended.
- **Accessibility**: captions available for speech-bearing media, audio description considered for visual-only meaning, sufficient contrast for text, no critical information conveyed by color alone, flash-sensitive content flagged.
- **Rights/provenance**: asset ledger complete; sources, model/tool versions, music licenses, releases, font licenses, stock IDs, and AI-use disclosures are present where required.

### 6. Acceptance, rejection, and waiver rules

Reject or hold delivery for:

- Wrong file, wrong version, wrong language, wrong market, wrong duration, or missing required deliverable.
- Codec/container/raster/fps/audio/caption/package mismatch against a binding spec.
- Missing or failed checksum for final delivery package.
- Corrupt file, playback failure, decode errors, bad duration, missing audio/video, or missing required sidecar.
- Legal, brand, medical, financial, political, or rights issue not approved by the accountable owner.
- Generated content that misrepresents a real person/product/place, includes unauthorized IP, or contains visible artifacts that harm the promised quality.
- Captions/subtitles materially out of sync, incomplete, mistranslated, unreadable, or missing when required.
- Loudness/true peak outside the required target/tolerance.
- HDR/SDR mismatch, missing color metadata where required, or obvious color transform error.
- Platform upload/ad portal rejection.

Allow with written waiver only when:

- The issue is visible/audible but accepted by the client or accountable owner.
- The file intentionally deviates from the spec for a documented reason.
- The destination portal accepts the file and the residual issue is not legally/accessibility/rights critical.

Never waive missing rights, missing required accessibility deliverables, or an unplayable/corrupt master without explicit written authority.

## Delivery sheets

Maintain a delivery sheet that a different agent or human can use to reconstruct the package. Minimum columns:

```text
package_id
asset_id
filename
version
status
destination
deliverable_role
language_locale
market
duration
aspect_ratio
resolution
frame_rate
container
video_codec
audio_codec
audio_channels
loudness_target
measured_loudness
true_peak
caption_files
color_space
source_master
export_tool
checksum_sha256
rights_status
provenance_status
qc_result
qc_notes
approved_by
delivery_date
```

Use `status` values such as `ready`, `hold`, `rejected`, `waived`, `delivered`, and `superseded`. Avoid ambiguous values like `final_final`.

## Filenames and versions

Use filenames that survive handoff without the folder context:

```text
<project>_<deliverable>_<market-or-locale>_<aspect>_<duration>_<spec-or-platform>_<version>_<date>.<ext>
```

Example:

```text
orchid-launch_paid-social_en-US_9x16_15s_tiktok-infeed_v03_20260710.mp4
orchid-launch_captions_en-US_9x16_15s_tiktok-infeed_v03_20260710.vtt
orchid-launch_mezzanine_en-US_16x9_30s_prores422hq_v03_20260710.mov
```

Versioning rules:

- Increment the version when pixels, audio, captions, metadata, or package composition changes.
- Keep rejected and superseded versions out of the delivery folder or mark them clearly.
- Do not reuse a filename for a changed file; it breaks checksum-based verification.
- Use ISO dates (`YYYYMMDD`) and standard locale tags (`en-US`, `fr-CA`) when useful.
- Keep filenames ASCII-safe unless the receiver explicitly supports other characters.

## Checksums, manifests, and package structure

For any non-trivial handoff, create a package manifest. For high-risk or archival transfer, use a BagIt-like structure or the client's package format.

Example package:

```text
orchid-launch_delivery_v03_20260710/
  manifest-sha256.txt
  delivery-sheet.csv
  delivery-notes.md
  masters/
    orchid-launch_mezzanine_en-US_16x9_30s_prores422hq_v03_20260710.mov
  platform/
    orchid-launch_paid-social_en-US_9x16_15s_tiktok-infeed_v03_20260710.mp4
    orchid-launch_paid-social_en-US_1x1_15s_meta-feed_v03_20260710.mp4
  captions/
    orchid-launch_captions_en-US_9x16_15s_tiktok-infeed_v03_20260710.vtt
  rights/
    asset-ledger.csv
    music-license.pdf
```

Generate SHA-256 checksums after final files are in their delivery locations. Use GNU-style manifest lines with exactly two spaces between the checksum and a package-relative POSIX path:

```bash
sha256sum platform/*.mp4 captions/*.vtt masters/*.mov > manifest-sha256.txt
```

On Windows PowerShell:

```powershell
Get-ChildItem -Recurse -File | Where-Object { $_.Name -ne "manifest-sha256.txt" } |
  ForEach-Object {
    $relative = Resolve-Path -LiteralPath $_.FullName -Relative
    "$((Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLower())  $($relative.TrimStart('.\').Replace('\', '/'))"
  } |
  Set-Content manifest-sha256.txt
```

When this skill package includes `scripts/verify_manifest.py`, use it as a deterministic fixity and completeness check before delivery:

```bash
python scripts/verify_manifest.py orchid-launch_delivery_v03_20260710 manifest-sha256.txt --require-all-files
```

The verifier accepts a package root and a SHA-256 manifest path, absolute or relative to that root. It rejects malformed lines, duplicate entries, absolute paths, traversal, paths outside the root, symlink escapes, non-regular manifest entries, and manifest self-inclusion. It hashes files as byte streams and emits stable JSON with `verified`, `failures`, and `unlisted` arrays. The script refuses symlink manifest paths and uses no-follow regular-file opens where the platform supports them; on platforms without no-follow open support, a malicious same-host actor with write access to the package directory could still race a file between validation and read, so run it on a stable package tree. Exit code `0` means all listed files verified; `2` means verification failed because files are missing, mismatched, unlisted under `--require-all-files`, or otherwise not acceptable payload files; `3` means the manifest or invocation could not be parsed or operated safely.

Do not treat checksum verification as creative, legal, accessibility, policy, or QC approval. The tool proves only that the files under the package root match the manifest and, with `--require-all-files`, that regular payload files were not silently omitted from the manifest. Rights, provenance, captions, loudness, playback, perceptual defects, and destination-spec conformance still require the QC workflow above.

After upload or copy, re-download or re-read the receiver-side file when possible and compare checksums. If the platform transcodes on ingest, verify ingest status and inspect the platform's playback/transcode output instead of expecting the same checksum.

## Delivery notes

Every final package should include concise delivery notes, either in the email/portal message or as a file:

```text
Project:
Package ID:
Delivered on:
Spec authority and verification date:
Files included:
Checksums:
QC summary:
Known waivers or limitations:
Rights/provenance summary:
Accessibility deliverables:
Contact / next action:
```

Good notes make hidden assumptions visible. Bad notes say only "attached final."

## Common deliverable profiles

### Social and paid ads

Check the specific placement, not only the platform brand. A Reels/Stories-style vertical asset, Facebook Feed asset, TikTok In-Feed ad, YouTube in-stream ad, YouTube Shorts upload, Google Performance Max asset, and CTV VAST asset can all have different safe zones, durations, aspect ratios, file-size limits, captions, and policy constraints.

QC emphasis:

- First-frame and first-3-second hook.
- Safe zones for platform UI and captions.
- Correct aspect ratio derivatives: 9:16, 1:1, 4:5, 16:9 as needed.
- Audio works with and without sound; critical message is not audio-only.
- Burned-in captions or sidecar captions match the media plan.
- File size/duration under placement limits.
- Legal claims, prices, promotional dates, and end cards match approved copy.
- Ad policy-sensitive content is reviewed by a human.

### Product/ecommerce content

QC emphasis:

- Product shape, color, label text, ports/buttons, packaging, and UI are accurate.
- No hallucinated claims, badges, certifications, ingredients, dimensions, or compatibility.
- Background, shadows, and reflections do not obscure the product.
- Transparent PNG/WebP assets preserve alpha correctly.
- Image dimensions, color profile, and file size match the ecommerce CMS.
- Variant naming maps to SKU, locale, and platform.

### Broadcast and streamer delivery

Do not infer these specs. Broadcast/streamer delivery often involves MXF, IMF, AS-11, ProRes, WAV stems, timed text, slate, timecode, bars/tone, act breaks, audio channel order, language metadata, and formal automated QC.

QC emphasis:

- Exact container/application/profile requested by the receiver.
- Audio channel layout and labels.
- Loudness target and measurement method.
- Timecode start, slate, bars/tone, black, handles, program start, and end hold.
- Color space, HDR metadata, legal levels, and caption/subtitle format.
- IMF/AS-11/package validation and manifest correctness.
- No undocumented fix in a derived file only; the master and derivatives must be traceable.

### Localization packages

QC emphasis:

- Source master version locked before translation starts.
- Locale-specific filenames and metadata.
- Subtitle/caption timing stays synced after conform.
- Text expansion does not collide with graphics.
- VO, dub, M&E, stems, and subtitles map to the same edit version.
- On-screen text, legal disclaimers, prices, measurements, dates, and cultural references are localized.
- Each locale has separate QC notes; do not approve all languages based on one review.

### Mixed-source edits

QC emphasis:

- Source resolution/frame-rate/color mismatches are intentionally conformed.
- Stock, UGC, generated, screen capture, and client footage rights are separately tracked.
- Audio noise floors and room tones are normalized across sources.
- Upres, denoise, retime, stabilization, and AI enhancement artifacts are checked at 100%.
- Any synthetic replacement or face/voice alteration has explicit consent and disclosure handling.

## Complete examples

### Example: paid social launch pack

**Intent**: Deliver three approved variants of a 15-second AI-assisted product launch ad for TikTok In-Feed, Meta Feed, and YouTube Shorts.

**Authority**: TikTok Ads Manager in-feed specs verified 2026-07-10; Meta placement specs verified 2026-07-10; YouTube upload guidance verified 2026-07-10; client media plan for exact durations and copy.

**Delivery plan**:

```text
Master:
  orchard-watch_mezzanine_en-US_16x9_15s_prores422hq_v04_20260710.mov
Platform:
  orchard-watch_paid-social_en-US_9x16_15s_tiktok-infeed_v04_20260710.mp4
  orchard-watch_paid-social_en-US_4x5_15s_meta-feed_v04_20260710.mp4
  orchard-watch_paid-social_en-US_9x16_15s_youtube-shorts_v04_20260710.mp4
Captions:
  orchard-watch_captions_en-US_9x16_15s_tiktok-infeed_v04_20260710.srt
  orchard-watch_captions_en-US_4x5_15s_meta-feed_v04_20260710.srt
Manifest:
  manifest-sha256.txt
  delivery-sheet.csv
  delivery-notes.md
```

**QC decisions**:

- Reject if any variant shows product geometry that differs from the approved packshot.
- Reject if legal offer text falls under app UI overlays in vertical format.
- Hold if the TikTok file exceeds the placement file-size limit or duration limit.
- Accept if ffprobe properties match the sheet, captions are in sync, audio has no clipping, all claims match approved copy, and checksums verify after package upload.

**Delivery note excerpt**:

```text
QC summary: Passed technical and perceptual QC on 2026-07-10. TikTok public specs checked the same day; Meta and YouTube specs are placement-dependent and were checked against the media plan. Known limitation: generated lifestyle background is synthetic; product packshot and claims are client-approved. Rights ledger included.
```

### Example: streamer localization handoff

**Intent**: Prepare a final locked episode package for a localization vendor creating subtitles and dubbed audio in three languages.

**Authority**: Client localization brief and streamer delivery guide; public SMPTE IMF information used only as background.

**Delivery plan**:

- Locked textless master or required mezzanine.
- Reference picture with burned-in timecode.
- Final script/dialogue list.
- M&E WAV stems if required.
- Existing captions/subtitles in source language.
- Shot/scene list and pronunciation guide.
- Asset ledger noting generated establishing shots and licensed music.
- Manifest with SHA-256 checksums.

**QC decisions**:

- Reject if the reference picture and textless master are not the same edit version.
- Reject if M&E contains source-language dialogue that should be absent.
- Hold if any generated shot lacks provenance/approval notes.
- Accept only after checksum validation, duration match, timecode alignment, caption sync, stem routing, and delivery sheet completion.

### Example: client archive package for generated campaign assets

**Intent**: Handoff final campaign files and provenance records for client DAM/archive.

**Authority**: Client DAM naming convention; BagIt/RFC 8493 used as a packaging model; SHA-256 selected as a house heuristic because the client did not mandate a hash algorithm.

**Delivery plan**:

```text
data/
  final-images/
  final-video/
  captions/
  audio/
  source-prompts-approved/
  rights/
manifest-sha256.txt
delivery-sheet.csv
bag-info.txt
delivery-notes.md
```

**QC decisions**:

- Reject if any file in `delivery-sheet.csv` is missing from the package.
- Reject if any checksum mismatch occurs after transfer.
- Hold if model/tool provenance is missing for AI-generated assets.
- Accept when the payload, manifest, rights ledger, and delivery notes agree exactly.

## Source notes

These sources informed the guidance above. Volatile public platform facts were checked on 2026-07-10:

- YouTube Help, "Recommended upload encoding settings": https://support.google.com/youtube/answer/1722171
- TikTok Ads Manager, "TikTok Auction In-Feed Ads": https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads
- Meta Ads Guide and Help Center placement guidance: https://www.facebook.com/business/ads-guide/update/video and https://www.facebook.com/business/help/103816146375741 (may require account access; public snippets/pages were checked where accessible)
- Google Ads Help, "Ad formats, sizes, and best practices": https://support.google.com/google-ads/answer/13676244
- IAB Tech Lab, "Digital Video and CTV Ad Format Guidelines": https://iabtechlab.com/dv-ctv-ad-format-guidelines/
- SMPTE ST 2067 Interoperable Master Format overview: https://www.smpte.org/standards/st2067
- AMWA AS-11 UK DPP HD: https://www.amwa.tv/as-11-uk-dpp-hd
- Apple HLS Authoring Specification for Apple Devices: https://developer.apple.com/documentation/http-live-streaming/hls-authoring-specification-for-apple-devices
- ITU-R BS.1770: https://www.itu.int/rec/R-REC-BS.1770
- EBU R 128: https://tech.ebu.ch/publications/r128/
- W3C WCAG: https://www.w3.org/TR/WCAG21/ and W3C WebVTT: https://www.w3.org/TR/webvtt1/
- Section508.gov synchronized media guidance: https://www.section508.gov/create/synchronized-media/
- IETF RFC 8493 BagIt: https://datatracker.ietf.org/doc/rfc8493/
- Python standard library documentation for `hashlib`, `pathlib`, and `os.path`, checked 2026-07-11: https://docs.python.org/3/library/hashlib.html, https://docs.python.org/3/library/pathlib.html, https://docs.python.org/3/library/os.path.html
- NIST hash functions project: https://csrc.nist.gov/projects/hash-functions
- C2PA specification and explainer: https://spec.c2pa.org/
- IPTC Photo Metadata Standard: https://iptc.org/standards/photo-metadata/iptc-standard/
