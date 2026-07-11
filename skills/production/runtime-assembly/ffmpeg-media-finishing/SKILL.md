---
name: ffmpeg-media-finishing
description: Provider-independent FFmpeg finishing workflow for AI agents preparing generated or edited media deliverables. Use when finalizing images, image sequences, video, audio, captions, overlays, social/export variants, checksums, manifests, delivery specs, and QA with ffmpeg/ffprobe, including transcode versus stream-copy decisions, scaling, frame-rate handling, color metadata caution, loudness normalization, subtitle burn-in or sidecars, concat/trim, GIFs, batch variants, and reproducible command reporting.
---

# FFmpeg media finishing

Use this skill at the finishing stage: after creative generation or editing has produced source media and before the user receives deliverables. Your job is to turn fragile, inconsistent media outputs into reproducible, spec-aware files with an audit trail.

This skill is provider-independent. It assumes local `ffmpeg` and `ffprobe` are available, but not that every codec, filter, hardware encoder, or subtitle renderer is compiled into the installed build. FFmpeg build capabilities, encoder names, platform upload rules, and social specs are volatile; re-check them at production time with the commands below and with the current delivery spec.

## Operating rule

Do not guess the state of media. Probe first, decide, run deterministic commands, then probe outputs.

Every finishing handoff should include:

- input audit summary from `ffprobe`;
- chosen delivery spec and any unresolved assumptions;
- exact commands run, including FFmpeg version/build;
- output audit summary;
- checksums and, when useful, frame hashes;
- known risks such as re-encoded captions, color metadata ambiguity, clipping, lossy transcodes, or platform-specific uncertainty.

## 1. Preflight the toolchain and inputs

Record the FFmpeg build and encoder/filter availability because behavior depends on the installed binary, compile flags, and external libraries.

```bash
ffmpeg -hide_banner -version
ffmpeg -hide_banner -encoders
ffmpeg -hide_banner -muxers
ffmpeg -hide_banner -filters
ffmpeg -hide_banner -h encoder=libx264
ffmpeg -hide_banner -h filter=loudnorm
```

Run `ffprobe` on every source and save machine-readable JSON when the job has more than one input, a client spec, or a risk of mismatch:

```bash
ffprobe -v error \
  -show_format -show_streams -show_chapters \
  -print_format json input.mp4 > input.ffprobe.json
```

For a compact human audit:

```bash
ffprobe -v error \
  -select_streams v:0 \
  -show_entries stream=codec_name,profile,width,height,pix_fmt,r_frame_rate,avg_frame_rate,time_base,field_order,color_range,color_space,color_transfer,color_primaries,sample_aspect_ratio,display_aspect_ratio,duration,nb_frames \
  -of default=noprint_wrappers=1 input.mp4

ffprobe -v error \
  -select_streams a:0 \
  -show_entries stream=codec_name,sample_rate,channels,channel_layout,sample_fmt,bits_per_sample,duration,bit_rate \
  -of default=noprint_wrappers=1 input.mp4
```

Audit at least:

- container, duration, file size, timecode/chapter needs;
- video codec, resolution, display aspect ratio, sample aspect ratio, pixel format, bit depth, alpha, interlacing, nominal and average frame rate, time base, start time;
- color metadata: range, primaries, transfer, matrix/colorspace;
- audio codec, sample rate, channel count/layout, duration, bit depth/sample format, loudness target if required;
- subtitle streams and external captions;
- attachments such as fonts in MKV/ASS workflows;
- whether inputs have identical parameters before concat or stream copy.

If `ffprobe` reports missing or inconsistent metadata, treat it as a warning, not as permission to invent values. Ask the user or infer cautiously from the creative pipeline only when necessary, and document the inference.

## 2. Choose stream copy, transcode, or filter

Use stream copy when the encoded streams are already acceptable and only container-level operations are needed:

```bash
ffmpeg -y -i input.mov -map 0 -c copy -movflags +faststart output.mp4
```

Stream copy is appropriate for remuxing, trimming on keyframe boundaries, adding compatible metadata, or extracting tracks. It is not appropriate when changing resolution, codec, pixel format, frame rate by resampling, loudness, captions burn-in, overlays, color conversion, or any filtergraph output. FFmpeg documents `-codec copy` as copying streams without re-encoding; filters require decoded frames and therefore a re-encode.

Transcode when the deliverable requires a different codec/container, resolution, frame rate, pixel format, audio layout, loudness, burned captions, overlays, or compatibility profile.

When quality matters, prefer a constant-quality setting over arbitrary bitrates unless a platform or client spec requires a bitrate cap. For H.264 with `libx264`, a common mezzanine-to-delivery pattern is:

```bash
ffmpeg -y -i input.mov \
  -map 0:v:0 -map 0:a? \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart output.mp4
```

Production heuristic: use lower CRF for higher quality/larger files and higher CRF for smaller files. Verify visually; CRF values are not delivery guarantees. If a client gives a target bitrate, max bitrate, GOP length, profile, chroma, or level, follow the spec instead of this heuristic.

## 3. Containers, codecs, and compatibility

Distinguish container from codec:

- MP4/MOV/MKV/WebM are containers.
- H.264/H.265/AV1/ProRes/DNxHR/AAC/Opus/PCM are codecs.
- A stream can be compatible with one container and incompatible with another.

Common delivery choices:

- Broad web/social compatibility: MP4 with H.264 video and AAC audio, usually `yuv420p`.
- Transparent or alpha-preserving intermediate: ProRes 4444 in MOV, PNG sequence, WebM VP9/AV1 with alpha only if the target supports it and the installed build can encode it.
- Archival or review mezzanine: ProRes/DNxHR/PCM or another client-specified mezzanine; do not substitute H.264 unless approved.
- WebM: typically VP9/AV1/Opus or VP8/Vorbis depending on target compatibility.
- Audio-only: WAV/PCM for interchange; AAC/MP3/Opus for compact delivery according to platform spec.

Before using a codec, check the local build:

```bash
ffmpeg -hide_banner -encoders | findstr /i "264 265 av1 prores aac opus"
```

On non-Windows shells, use `grep -Ei` instead of `findstr`.

Hardware encoders such as `h264_nvenc`, `hevc_videotoolbox`, `h264_qsv`, or `h264_amf` are machine- and driver-dependent. They can be fast but may differ in rate-control behavior and quality. Do not assume availability; test a short sample.

## 4. Scaling, cropping, padding, and aspect ratio

Pick the geometry behavior intentionally:

- Scale to fit inside a canvas and pad when preserving the whole frame matters.
- Crop to fill when edge content may be sacrificed.
- Scale exactly only when distortion is acceptable or source already matches the target aspect ratio.
- Normalize sample aspect ratio to square pixels for most web/social deliverables.

Fit inside 1920x1080 with black padding:

```bash
ffmpeg -y -i input.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -c:a copy output_1080p_letterbox.mp4
```

Fill 1080x1920 vertical by cropping:

```bash
ffmpeg -y -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 192k output_9x16.mp4
```

For generated stills, use even dimensions for codecs that require chroma subsampling:

```bash
ffmpeg -y -loop 1 -framerate 30 -t 5 -i still.png \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow -an still_card.mp4
```

## 5. Frame rate, timestamps, time base, and sync

Frame rate changes are a common source of judder, drift, duplicate frames, and broken captions. Inspect both `r_frame_rate` and `avg_frame_rate`; variable-frame-rate sources often have a confusing nominal rate.

Rules:

- Preserve source frame rate unless a delivery spec requires conversion.
- Avoid converting 23.976/24/25/30/50/60 fps casually; conversions can introduce cadence artifacts.
- For social variants, choose a single constant frame rate only when the platform/client spec, editing timeline, or concat requirements demand it.
- When cutting with stream copy, expect keyframe-aligned trimming unless you re-encode.
- When using filters such as `fps`, `trim`, `setpts`, `atrim`, or `asetpts`, re-encode the filtered stream.

Force constant 30 fps for a platform-specific version:

```bash
ffmpeg -y -i input.mp4 \
  -vf "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 output_30fps_vertical.mp4
```

Trim accurately by re-encoding:

```bash
ffmpeg -y -ss 12.345 -to 27.890 -i input.mp4 \
  -map 0:v:0 -map 0:a? \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 192k clip_exact.mp4
```

Fast keyframe-aligned trim by stream copy:

```bash
ffmpeg -y -ss 12 -to 28 -i input.mp4 -map 0 -c copy clip_fast.mp4
```

If audio and video durations differ after finishing, inspect start times, PTS/DTS warnings, and whether a filtergraph dropped or duplicated frames. Do not hide sync defects with arbitrary audio padding unless the spec calls for it.

## 6. Color range and color space caution

FFmpeg can set or transform color metadata, but metadata is not the same as a correct color conversion. Generated assets often lack reliable color tags. Mismatched full/limited range, Rec.709/Rec.2020 primaries, transfer functions, or HDR/SDR assumptions can produce washed-out or crushed exports.

Minimum practice:

1. Probe source color tags.
2. If the source was generated or composited in a known working space, carry that information into finishing notes.
3. For normal SDR web delivery, commonly target Rec.709 metadata and yuv420p unless the client spec says otherwise.
4. If converting HDR, wide gamut, log, or client-critical brand colors, escalate to a color-managed workflow or human color approval.
5. After setting tags, re-probe the output and visually review on a known-good player.

Example of tagging an SDR H.264 delivery without claiming a color transform:

```bash
ffmpeg -y -i input.mp4 \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -c:a aac -b:a 192k output_sdr_tagged.mp4
```

If you must transform between matrices/ranges, use a color filter such as `zscale` or `colorspace` only after checking the installed filter options and validating with test frames. Do not use metadata flags alone as a conversion.

## 7. Audio loudness, sample rate, and channel layout

Finish audio to the delivery spec. If there is no spec:

- For web/social video, 48 kHz AAC stereo is broadly compatible.
- For broadcast, client, or advertising delivery, follow the exact loudness standard and tolerance.
- For archival/interchange, preserve PCM/WAV or deliver separate stems when requested.

Use standards language precisely:

- ITU-R BS.1770 defines loudness and true-peak measurement algorithms.
- EBU R 128 is a broadcast recommendation based on loudness normalization and true-peak limits.
- Platform loudness targets vary and are volatile; re-check platform documentation rather than relying on memory.

Measure first:

```bash
ffmpeg -hide_banner -i input.mp4 \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json \
  -f null -
```

For repeatable loudness normalization, use two-pass `loudnorm`: first measure, then feed measured values into the second pass. Example target shown is a common online-video heuristic, not a standard:

```bash
ffmpeg -hide_banner -i input.mp4 \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json \
  -f null -

ffmpeg -y -i input.mp4 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=-18.7:measured_TP=-3.2:measured_LRA=8.4:measured_thresh=-29.1:offset=0.2:linear=true:print_format=summary,aformat=sample_rates=48000:channel_layouts=stereo" \
  -c:v copy -c:a aac -b:a 192k output_loudnorm.mp4
```

Do not normalize blindly when preserving a theatrical mix, music dynamics, stems, spatial audio, or client-approved master. Ask before downmixing 5.1/7.1/Atmos/spatial audio to stereo.

Downmix example. Inspect the probed channel layout first and adapt channel names; some 5.1 sources expose side channels as `SL`/`SR` rather than back channels `BL`/`BR`.

```bash
ffmpeg -y -i input.mov \
  -map 0:v:0 -map 0:a:0 \
  -c:v copy \
  -af "pan=stereo|FL=0.707*FC+FL+0.707*BL+0.5*LFE|FR=0.707*FC+FR+0.707*BR+0.5*LFE,aformat=sample_rates=48000:channel_layouts=stereo" \
  -c:a aac -b:a 192k output_stereo.mp4
```

Review downmixes by ear. Formulaic downmix coefficients are a starting point, not a substitute for listening.

## 8. Captions and subtitles: burn-in versus sidecar

Make caption handling a delivery decision, not an afterthought.

Use sidecar captions when accessibility, searchability, user control, localization, or platform-native captions matter. Common sidecar formats include SRT and WebVTT; the target platform decides what is accepted.

Burn in captions when the platform does not support caption tracks, when the user requests open captions, or when short-form social readability is the priority. Burned captions are pixels: they cannot be turned off, searched, restyled by assistive technology, or corrected without re-rendering.

WCAG guidance treats captions as synchronized text for speech and needed non-speech audio. Do not treat auto-generated captions as final without review when accessibility or client compliance matters.

Add a compatible SRT sidecar as a subtitle stream when the container/player supports it:

```bash
ffmpeg -y -i input.mp4 -i captions.srt \
  -map 0:v -map 0:a? -map 1:0 \
  -c:v copy -c:a copy -c:s mov_text \
  -metadata:s:s:0 language=eng output_with_captions.mp4
```

Burn in SRT captions with libass-backed rendering:

```bash
ffmpeg -y -i input.mp4 \
  -vf "subtitles=captions.srt:force_style='Fontname=Arial,Fontsize=42,Outline=2,Shadow=1,MarginV=80'" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -c:a copy output_burned_captions.mp4
```

Before using `subtitles`, confirm the FFmpeg build has the filter and libass support:

```bash
ffmpeg -hide_banner -filters | findstr /i subtitles
```

Caption QA:

- confirm timing against final audio after all trims and speed changes;
- include meaningful speaker IDs and non-speech audio where needed;
- keep lines readable on the target aspect ratio;
- test safe areas for platform UI overlays;
- verify special characters and non-Latin scripts after encoding/burn-in;
- deliver sidecar and burned versions when the user needs both accessibility and social readability.

## 9. Image sequences, stills, and generated frames

Generated image sequences are common in AI pipelines. Stabilize numbering, frame rate, pixel format, and alpha policy before encoding.

Encode a numbered PNG sequence:

```bash
ffmpeg -y -framerate 24 -start_number 1 -i "frames/frame_%05d.png" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p output_from_sequence.mp4
```

Preserve alpha for compositing review:

```bash
ffmpeg -y -framerate 24 -i "frames/frame_%05d.png" \
  -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le output_alpha.mov
```

Extract frames for QA:

```bash
ffmpeg -y -i output.mp4 -vf "fps=1,scale=320:-1" "qa/thumb_%04d.jpg"
```

If a sequence has missing frames, duplicate numbers, mixed sizes, mixed color profiles, or inconsistent alpha, stop and repair the sequence before encoding.

## 10. GIF and social preview exports

GIF is often useful for previews but inefficient for photographic or long content. Prefer MP4/WebM for real delivery unless GIF is explicitly requested.

Use a palette for better GIF quality:

```bash
ffmpeg -y -ss 0 -t 4 -i input.mp4 \
  -vf "fps=12,scale=640:-1:flags=lanczos,palettegen" palette.png

ffmpeg -y -ss 0 -t 4 -i input.mp4 -i palette.png \
  -lavfi "fps=12,scale=640:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5" \
  preview.gif
```

Create quick social variants from a master, but re-check current platform rules before final delivery:

```bash
# 16:9 landscape
ffmpeg -y -i master.mov \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" \
  -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart deliverable_16x9.mp4

# 9:16 vertical
ffmpeg -y -i master.mov \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" \
  -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart deliverable_9x16.mp4

# 1:1 square
ffmpeg -y -i master.mov \
  -vf "scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080,setsar=1" \
  -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart deliverable_1x1.mp4
```

Social and ad specs change. Treat current platform docs, client media plans, and ad-manager requirements as binding; treat examples here as starting points.

## 11. Concat, trim, slates, overlays, and watermarks

Concat by stream copy only when inputs are compatible in codec, time base, resolution, pixel format, frame rate, sample rate, and channel layout. Otherwise normalize each clip first or use the concat filter and re-encode.

Concat demuxer with compatible clips:

```text
file 'clip01.mp4'
file 'clip02.mp4'
file 'clip03.mp4'
```

```bash
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy joined.mp4
```

Normalize first, then concat:

```bash
ffmpeg -y -i clip01.mov -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30,setsar=1,format=yuv420p" -af "aformat=sample_rates=48000:channel_layouts=stereo" -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k norm01.mp4
```

Overlay watermark:

```bash
ffmpeg -y -i input.mp4 -i logo.png \
  -filter_complex "[1:v]scale=180:-1[logo];[0:v][logo]overlay=W-w-40:H-h-40:format=auto" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -c:a copy output_watermarked.mp4
```

Add a slate from an image while keeping program audio in sync by concatenating explicit slate silence before the program audio:

```bash
ffmpeg -y -loop 1 -t 3 -i slate.png -i program.mp4 -f lavfi -t 3 -i anullsrc=r=48000:cl=stereo \
  -filter_complex "[0:v]scale=1920:1080,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale=1920:1080,setsar=1,fps=30,format=yuv420p[v1];[2:a]aformat=sample_rates=48000:channel_layouts=stereo[a0];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k output_with_slate.mp4
```

If the program has no audio, use a video-only concat (`concat=n=2:v=1:a=0`) and omit the audio maps. Do not map program audio directly under a prepended slate unless that offset is intentional.

## 12. Batch variants and reproducibility

Use a manifest-driven pattern for batch work. Record input path, output path, requested spec, exact command, FFmpeg version, source hash, output hash, and QA status. Avoid handwritten one-off commands for dozens of variants.

Example manifest fields:

```json
{
  "job_id": "campaign-final-2026-07-11",
  "ffmpeg_version": "record from ffmpeg -version",
  "source": "master.mov",
  "source_sha256": "computed before processing",
  "deliverables": [
    {
      "name": "youtube_16x9",
      "output": "deliverable_16x9.mp4",
      "spec": "MP4 H.264 AAC 1920x1080 SDR",
      "command": "exact command string",
      "output_sha256": "computed after processing",
      "qa": "pass with noted warnings"
    }
  ]
}
```

Use SHA-256 for file integrity manifests:

```bash
certutil -hashfile output.mp4 SHA256
```

On macOS/Linux:

```bash
shasum -a 256 output.mp4
```

Use FFmpeg frame hashes when verifying decoded frame equivalence or detecting accidental media changes:

```bash
ffmpeg -v error -i output.mp4 -f framehash output.framehash
ffmpeg -v error -i output.mp4 -f framemd5 output.framemd5
```

File checksums change if metadata changes. Frame hashes can remain stable across some container metadata changes but will change after lossy re-encode, scaling, audio normalization, or pixel/sample-format conversion.

## 13. Finishing QA checklist

Run automated checks:

```bash
ffmpeg -v error -i output.mp4 -f null -
ffprobe -v error -show_format -show_streams -print_format json output.mp4 > output.ffprobe.json
```

Inspect:

- output opens and plays in at least one target player;
- duration matches expectation within tolerance;
- audio/video sync holds at start, middle, and end;
- no unexpected dropped/duplicated-frame warnings;
- resolution, aspect ratio, frame rate, pixel format, codec, profile, level, bitrate/file size meet spec;
- audio sample rate, channel layout, loudness, and true peak meet spec;
- captions are synchronized, readable, accurate, and encoded or burned as requested;
- overlays and watermarks are placed correctly and safe from platform UI;
- color tags match the intended delivery and visual review is acceptable;
- metadata does not leak unwanted private paths, model prompts, or client information;
- checksums/manifests are produced;
- filenames are deterministic and platform-safe.

For important deliverables, sample frames rather than trusting command success:

```bash
ffmpeg -y -i output.mp4 -vf "select='eq(n,0)+eq(n,300)+eq(n,600)',scale=480:-1" -vsync vfr "qa_sample_%03d.jpg"
```

## Escalation triggers

Stop and ask for approval or specialist review when:

- the client spec conflicts with source media or platform limits;
- legal, rights, watermark, logo, music licensing, caption compliance, accessibility compliance, or ad-policy questions arise;
- HDR, wide-gamut, broadcast, theatrical, surround/spatial audio, or color-critical delivery is required;
- platform specs are unavailable, gated, or changed since the brief;
- generated content contains private data, unreleased product information, or unknown third-party marks;
- FFmpeg lacks required encoders/filters and alternatives would change quality, cost, or compatibility;
- a lossy transcode is unavoidable for a client-approved master;
- caption accuracy has not been human-reviewed for compliance-sensitive publication.

Avoid legal advice. State the production risk and recommend client, counsel, platform, or accessibility review as appropriate.

## Complete examples

### Example: Finalize a generated 9:16 social video with captions

Intent: prepare a vertical short from an AI video master and reviewed captions.

Inputs:

- `master.mov`: generated 16:9 or mixed-aspect video with audio;
- `captions.srt`: reviewed caption file;
- target: 1080x1920 MP4, H.264/AAC, burned captions for social feed.

Workflow:

```bash
ffmpeg -hide_banner -version > ffmpeg_version.txt
ffprobe -v error -show_format -show_streams -print_format json master.mov > master.ffprobe.json

ffmpeg -y -i master.mov \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,subtitles=captions.srt:force_style='Fontname=Arial,Fontsize=44,Outline=2,Shadow=1,MarginV=110',format=yuv420p" \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo" \
  -c:v libx264 -crf 20 -preset slow \
  -c:a aac -b:a 192k -movflags +faststart \
  final_9x16_burned.mp4

ffmpeg -v error -i final_9x16_burned.mp4 -f null -
ffprobe -v error -show_format -show_streams -print_format json final_9x16_burned.mp4 > final_9x16_burned.ffprobe.json
certutil -hashfile final_9x16_burned.mp4 SHA256
```

Why it is structured this way:

- scaling/cropping is explicit for vertical delivery;
- captions are burned because many social-view contexts default to sound-off quick viewing;
- audio is normalized to an online-video heuristic, not a broadcast standard;
- the output is re-probed and hashed.

Likely failure modes:

- crop cuts important visual content;
- `subtitles` filter unavailable due to missing libass;
- loudness target is inappropriate for a client/platform spec;
- color metadata from the source remains ambiguous.

### Example: Remux an approved master without changing encoded streams

Intent: convert an approved MOV master into an MP4 wrapper for review upload without re-encoding.

Workflow:

```bash
ffprobe -v error -show_format -show_streams -print_format json approved_master.mov > approved_master.ffprobe.json

ffmpeg -y -i approved_master.mov \
  -map 0 -c copy -movflags +faststart review_upload.mp4

ffprobe -v error -show_format -show_streams -print_format json review_upload.mp4 > review_upload.ffprobe.json
certutil -hashfile approved_master.mov SHA256
certutil -hashfile review_upload.mp4 SHA256
```

Decision notes:

- This preserves encoded streams; it is not a quality-changing render.
- It only works if the input streams are legal in MP4 and accepted by the target.
- File checksums differ because the container changed; decoded frame hashes can help verify media essence if needed.

### Example: Batch deliver landscape, square, and vertical variants

Intent: produce three deterministic variants from one master while preserving a manifest trail.

Workflow:

```bash
ffprobe -v error -show_format -show_streams -print_format json master.mov > master.ffprobe.json

ffmpeg -y -i master.mov \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p" \
  -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k -movflags +faststart deliverable_16x9.mp4

ffmpeg -y -i master.mov \
  -vf "scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080,setsar=1,format=yuv420p" \
  -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k -movflags +faststart deliverable_1x1.mp4

ffmpeg -y -i master.mov \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p" \
  -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k -movflags +faststart deliverable_9x16.mp4
```

Variation:

- A single multi-output filtergraph can be faster for large masters, but three separate commands are easier to audit and debug. Prefer clear, reliable outputs over clever one-liners.

## Sources and verification notes

Consequential facts in this skill are based on these sources, checked 2026-07-11:

- FFmpeg command and stream-copy documentation: https://ffmpeg.org/ffmpeg.html
- ffprobe documentation and JSON/show stream options: https://ffmpeg.org/ffprobe.html
- FFmpeg filter documentation including scale/crop/pad/fps/loudnorm/subtitles/overlay: https://ffmpeg.org/ffmpeg-filters.html
- FFmpeg format/muxer documentation including concat, image2, GIF, hash/framehash/framemd5: https://ffmpeg.org/ffmpeg-formats.html
- ITU-R BS.1770 recommendation page for loudness and true-peak algorithms: https://www.itu.int/rec/R-REC-BS.1770
- EBU R 128 loudness recommendation: https://tech.ebu.ch/publications/r128/
- W3C/WAI captions guidance and WCAG caption success criterion: https://www.w3.org/WAI/media/av/captions/ and https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
- YouTube recommended upload encoding settings, used only as an example of volatile platform guidance: https://support.google.com/youtube/answer/1722171
- TikTok Ads Manager specs, used only as an example of volatile platform/ad guidance: https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads
