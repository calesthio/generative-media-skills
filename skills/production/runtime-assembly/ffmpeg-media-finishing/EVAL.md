# Evaluation guide for `ffmpeg-media-finishing`

Use this file only to evaluate an agent that had access to `SKILL.md`. Do not provide this file to the agent being evaluated.

Strong responses should behave like a finishing engineer: probe inputs, choose the least destructive valid operation, document assumptions, run reproducible FFmpeg commands, verify outputs, and escalate when media, legal, color, accessibility, or platform risks exceed the agent's authority.

## Knowledge questions

### 1. What is the first thing an agent should do before finishing arbitrary generated media?

Expected answer:

- Check local FFmpeg/ffprobe version and build capabilities.
- Run `ffprobe` on every input, ideally saving JSON for non-trivial jobs.
- Audit streams, codec/container, dimensions, frame rate/time base, pixel format, color tags, audio layout, captions, duration, and compatibility.

Required points:

- Must mention probing before deciding.
- Must mention local build variability.
- Must distinguish media facts from assumptions.

Penalize:

- Starting with a transcode command without inspecting inputs.
- Assuming codecs/filters/platform specs from memory.

### 2. When is `-c copy` appropriate, and when is it not?

Expected answer:

- Appropriate for stream copy/remux operations when encoded streams already meet the target and no filters or stream changes are needed.
- Appropriate for compatible container changes, compatible metadata operations, and keyframe-aligned trims.
- Not appropriate for scaling, cropping, padding, overlays, burned captions, loudness changes, frame-rate resampling, codec changes, pixel-format changes, color conversion, or accurate non-keyframe edits.

Required points:

- Must say stream copy avoids re-encoding.
- Must state that filtering requires decode/re-encode of affected streams.

Critical failure:

- Claims `-c copy` can burn subtitles, normalize loudness, or resize video.

### 3. Explain container versus codec and give a compatibility-sensitive example.

Expected answer:

- Container is the wrapper such as MP4/MOV/MKV/WebM; codec is encoded essence such as H.264, ProRes, AAC, Opus, AV1.
- A codec/stream may be legal in one container and not accepted in another.
- Example: MP4/H.264/AAC/yuv420p for broad web review; ProRes 4444 MOV or PNG sequence for alpha/intermediate; WebM usually with VP9/AV1/Opus depending on target.

Penalize:

- Treating MP4 as a codec.
- Recommending a delivery codec without checking target requirements.

### 4. What is the color metadata caution?

Expected answer:

- Color tags such as primaries, transfer, matrix/colorspace, and range describe interpretation but are not necessarily a color transform.
- Generated media may lack reliable tags.
- Setting `-color_primaries`, `-color_trc`, `-colorspace`, or `-color_range` can label output but does not fix wrongly transformed pixels.
- HDR, wide gamut, log, broadcast, and brand-critical work should be escalated or validated with a color-managed workflow.

Critical failure:

- Claims that setting Rec.709 flags alone converts HDR/wide-gamut or full-range media correctly.

### 5. What standards are relevant to loudness normalization?

Expected answer:

- ITU-R BS.1770 defines loudness and true-peak measurement algorithms.
- EBU R 128 is a broadcast recommendation using loudness normalization and true-peak constraints.
- Platform targets vary and are volatile; re-check current docs/client specs.
- Use two-pass `loudnorm` for repeatable normalization when needed, and do not blindly normalize approved mixes or surround/spatial audio.

Required points:

- Must mention measuring before changing.
- Must distinguish a standard/client spec from an online-video heuristic.

### 6. What are the tradeoffs between burned captions and sidecar captions?

Expected answer:

- Sidecar captions support accessibility, user control, search, localization, platform-native styling, and correction without rerendering.
- Burned captions are always visible and useful for social contexts but become pixels that cannot be turned off, searched, restyled, or fixed without re-rendering.
- Caption timing and text must be reviewed after final trims/speed changes.
- Accessibility/compliance-sensitive captions require review; auto-captions are not enough by default.

Critical failure:

- Says burned captions are equivalent to accessible closed captions.

### 7. What makes concat by stream copy safe or unsafe?

Expected answer:

- Safe when inputs are compatible in codec, time base, resolution, pixel format, frame rate, sample rate, channel layout, and container expectations.
- Unsafe when inputs differ; normalize first or use concat filter and re-encode.
- Should inspect `ffprobe` outputs before deciding.

Penalize:

- Concatenating arbitrary generated clips with `-c copy` without checking parameters.

### 8. How should an agent verify outputs?

Expected answer:

- Run `ffmpeg -v error -i output -f null -` to catch decode errors.
- Re-probe output with `ffprobe` JSON.
- Inspect frames and playback for duration, sync, captions, overlays, color, and safe areas.
- Compute checksums/manifests and optionally frame hashes for media essence verification.

Required points:

- Must include both automated and human/visual/listening QA.

## Production-decision scenarios

### 9. User asks: "Just make this MOV uploadable as MP4, but don't reduce quality."

Expected decision:

- Probe the MOV.
- If video/audio streams are compatible with MP4 and the target accepts them, remux with `-map 0 -c copy -movflags +faststart`.
- If streams are incompatible, explain that a transcode is required and get approval because it may be lossy.

Strong answer characteristics:

- Does not automatically transcode to H.264.
- Documents that file checksum will change even with stream copy.
- Verifies output.

Critical failures:

- Re-encodes without need or approval.
- Promises no quality loss while transcoding lossy media.

### 10. User supplies a 16:9 AI master and requests a 9:16 social version.

Expected decision:

- Probe input and clarify/choose whether to crop-to-fill or pad-to-fit.
- If no guidance and social full-screen is intended, recommend crop-to-fill but warn edge content may be lost.
- Use explicit scale/crop or scale/pad, `setsar=1`, compatible codec/pixel format/audio.
- QA the crop for subject framing and platform UI safe areas.
- Re-check current platform specs.

Penalize:

- Stretching 16:9 to 9:16.
- Ignoring safe areas and subject framing.

### 11. User asks for "broadcast loudness normalization" but provides no network spec.

Expected decision:

- Ask for the broadcaster/network delivery spec before finalizing.
- Explain that ITU-R BS.1770/EBU R 128 are relevant but exact targets/tolerances may be client-specific.
- Measure with `loudnorm`; do not apply an arbitrary online-video target as broadcast compliance.

Critical failure:

- Applies `I=-16` or `I=-14` and calls it broadcast-ready.

### 12. User asks to burn auto-generated captions into a compliance-sensitive training video.

Expected decision:

- Explain burn-in versus sidecar tradeoff.
- Recommend reviewed sidecar captions for accessibility plus optional burned social/open-caption version if requested.
- Escalate caption accuracy/accessibility compliance for human review.
- If burning, verify `subtitles` filter/libass availability and QA timing/readability.

Critical failures:

- Treats unreviewed auto-caption text as compliance-ready.
- Delivers only burned captions for an accessibility requirement without warning.

### 13. User wants to convert an HDR/wide-gamut generated master to SDR web MP4.

Expected decision:

- Probe color metadata and identify uncertainty.
- Explain that metadata tagging is not a conversion.
- Recommend a color-managed transform and visual approval, or escalate to a color specialist if important.
- Avoid claiming correctness from simple Rec.709 flags.

Critical failure:

- Uses only `-color_primaries bt709 -colorspace bt709` and says HDR was converted to SDR.

### 14. User gives three AI clips with different frame rates and asks for a single video.

Expected decision:

- Probe each clip.
- If stream parameters differ, normalize to a common delivery frame rate/resolution/pixel format/audio layout first or use a concat filter with re-encode.
- Warn about cadence/judder if changing frame rates.
- Verify sync and duration after concat.

Penalize:

- Blind concat demuxer with `-c copy`.
- No discussion of frame-rate/cadence tradeoffs.

## Applied production tasks

### 15. Write a finishing plan for a 60-second generated product-launch video.

User request:

> Finish my generated launch video for YouTube and vertical socials. I have `master.mov`, `captions.srt`, and `logo.png`. Make final files and a manifest.

Expected approach:

- Probe `master.mov`, check FFmpeg version/build, inspect captions and logo.
- Confirm or state assumptions for YouTube landscape and vertical social specs; re-check platform rules.
- Produce at least two variants: 16:9 and 9:16.
- Use scale/pad or crop strategy explicitly, with warning about vertical crop.
- Apply logo overlay if requested/appropriate with safe-area placement.
- Decide sidecar versus burned captions; likely sidecar for YouTube and burned or both for social.
- Normalize or measure audio according to a stated target or spec; avoid pretending a heuristic is universal.
- Generate checksums and manifest with exact commands and QA.

Scoring rubric:

- 4 points: input/tool audit and volatile spec handling.
- 4 points: correct stream-copy/transcode decisions and FFmpeg command structure.
- 3 points: geometry/aspect handling and safe-area awareness.
- 3 points: caption and accessibility tradeoffs.
- 3 points: audio loudness/channel handling.
- 3 points: output QA, checksums, manifest, reproducibility.

Critical failures:

- No probing.
- One-size-fits-all platform settings without caveats.
- Stretching video to vertical.
- Treating burned captions as the only accessibility deliverable.

### 16. Diagnose a failed command.

User request:

> I ran `ffmpeg -i input.mp4 -vf scale=1080:1920 -c copy out.mp4` and FFmpeg failed. Fix it.

Expected answer:

- Explain that `-vf scale` filters video, so video cannot be stream-copied.
- Use `-c:v libx264` or another suitable video encoder; audio may be copied if compatible and not filtered.
- Recommend preserving aspect ratio using scale+crop or scale+pad instead of raw `scale=1080:1920`.
- Example:

```bash
ffmpeg -y -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a copy out.mp4
```

Required points:

- Must identify stream-copy/filter conflict.
- Must avoid distortion.

### 17. Create a command and QA checklist for an image sequence.

User request:

> I have `frames/shot_%05d.png` from an AI animation. Make a 24 fps MP4 and tell me how to verify it.

Expected output:

- Command with `-framerate 24` before `-i`, H.264, `yuv420p`, CRF/preset.
- Warn to check missing/mixed-size frames.
- Re-probe output, decode-check, sample frames/playback, checksum.

Example strong command:

```bash
ffmpeg -y -framerate 24 -i "frames/shot_%05d.png" \
  -vf "setsar=1,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow -an shot_24fps.mp4
```

Penalize:

- Places `-r 24` after input without explaining implications.
- Omits pixel format for compatibility.

### 18. Make a GIF preview from a video.

Expected approach:

- Use short duration, lower fps, scaled dimensions.
- Generate a palette then apply it.
- Warn that GIF is inefficient and not a substitute for MP4/WebM delivery.

Required command characteristics:

- `palettegen` pass.
- `paletteuse` pass.
- Explicit fps and scale.

### 19. Produce a hidden-risk review of a proposed finishing command.

Command:

```bash
ffmpeg -i master.mp4 -vf subtitles=captions.srt -af loudnorm -r 30 -s 1080x1920 -c:v h264 output.mp4
```

Expected findings:

- No input probe or output spec.
- `-s 1080x1920` likely distorts if aspect ratio differs; use scale/crop/pad.
- `-r 30` may introduce frame cadence issues; inspect source and justify.
- `loudnorm` default/one-pass may not meet a specific target; measure/two-pass if needed.
- `subtitles` burns captions; sidecar may be needed for accessibility.
- `h264` encoder choice is ambiguous/build-dependent; prefer explicit encoder after checking build.
- Missing audio codec/bitrate/sample rate/channel layout decisions.
- Missing pixel format, `faststart`, color metadata caution, output QA, checksums.

Scoring:

- Full credit requires identifying at least eight issues and proposing safer alternatives.
- Critical failure if the answer approves the command as production-ready without caveats.

## Overall scoring guidance

Excellent:

- Always probes first and cites exact media facts needed.
- Chooses stream copy only when valid and least destructive.
- Uses explicit, reproducible FFmpeg commands with correct option placement.
- Separates standards, platform rules, and heuristics.
- Handles captions, loudness, color, frame rate, and aspect ratio with appropriate caution.
- Produces QA steps, checksums, and manifests.
- Escalates legal/compliance/color/platform uncertainty rather than inventing certainty.

Adequate:

- Provides workable commands and some QA.
- Mentions probing and verification, but may miss secondary risks such as color metadata or caption accessibility.
- Uses reasonable defaults while labeling them as assumptions.

Poor:

- Starts from generic transcoding recipes.
- Ignores input audit, output spec, or volatile platform rules.
- Confuses container/codec, stream copy/transcode, or captions/subtitles.
- Makes unsupported compliance, legal, color, or platform claims.
- Omits verification and reproducibility.

