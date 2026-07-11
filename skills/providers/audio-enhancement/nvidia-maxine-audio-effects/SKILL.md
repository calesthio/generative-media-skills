---
name: nvidia-maxine-audio-effects
description: Use NVIDIA Maxine / NVIDIA AI for Media audio effects for speech cleanup and enhancement in live or offline media pipelines, including Background Noise Removal, denoise+dereverb, room echo removal, acoustic echo cancellation, audio super-resolution, Studio Voice, Speaker Focus, and Voice Font. Use when selecting, integrating, prompting around, QAing, or privacy-reviewing NVIDIA AFX SDK or BNR NIM workflows for conferencing, broadcast, podcast, avatar, ad, social, and video post-production audio.
---

# NVIDIA Maxine audio effects

Use this skill to plan and operate NVIDIA Maxine Audio Effects, now under NVIDIA AI for Media, as an audio cleanup and enhancement stage. Treat it as a production and integration skill, not as a sound-generation prompt recipe: the core work is choosing the correct effect, preparing audio correctly, protecting speaker rights, running the SDK or NIM in the right runtime, and proving that the processed speech is clearer without damaging the performance.

Facts below were verified against official NVIDIA documentation on 2026-07-10. Re-check NVIDIA docs, NGC, and license terms before quoting exact model profiles, supported GPUs, SDK versions, file limits, or access requirements in a production proposal.

## Capability boundaries

NVIDIA documents these Audio Effects SDK capabilities:

- `denoiser` / Background Noise Removal (BNR): remove common background noises from speech while preserving natural speech as much as possible.
- `dereverb`: suppress room echo/reverberation from recordings made in reflective rooms.
- `dereverb_denoiser`: use the combined denoise + dereverb model when both noise and reverb are present; do not chain separate denoiser and dereverb effects when NVIDIA provides the combined effect for that case.
- `aec`: acoustic echo cancellation for live bidirectional communication. This is not the same as dereverb; it needs near-end microphone audio plus a far-end/reference signal.
- `superres`: audio super-resolution, typically 8 kHz -> 16 kHz or 16 kHz -> 48 kHz, to restore/predict missing high-frequency content.
- `studio_voice_high_quality`: offline enhancement for degraded speech from poor microphones, noise filters, beamforming, static, or non-ideal acoustics.
- `studio_voice_low_latency`: real-time Studio Voice variant; use for live conferences or broadcasts, not offline batch finishing.
- `speaker_focus`: Early Access speaker isolation for keeping the primary speaker while suppressing other speakers and some noises.
- `voice_font_high_quality` / `voice_font_low_latency`: Early Access any-to-any voice conversion using reference speech. Treat as voice identity transformation requiring explicit consent and review.

NVIDIA BNR NIM is narrower than the full AFX SDK. Use it for Background Noise Removal through a containerized gRPC service or hosted Try API; do not assume NIM exposes dereverb, AEC, super-resolution, Studio Voice, Speaker Focus, or Voice Font unless current NVIDIA docs say so.

Do not use Maxine audio effects when the user needs:

- music generation, Foley, or sound design;
- source separation of music stems;
- creative voice acting or TTS;
- legal-quality forensic restoration;
- restoring clipped, over-compressed, or missing speech content beyond what enhancement can plausibly recover.

## Choose the runtime first

Select the deployment path before designing the cleanup chain.

### Local AFX SDK

Use the AFX SDK when the application needs one or more SDK effects beyond BNR, local custody, low-latency client integration, or direct control of sample format, batching, and chained effects. NVIDIA positions Windows SDK packages for client-side applications and Linux SDK packages for server/datacenter/cloud deployments. The SDK requires NVIDIA GPUs with Tensor Cores; official docs list Turing, Ampere, Ada, Hopper, and Blackwell families for current Linux SDK support.

Operational implications:

- Install the base SDK and the feature packages/models for the exact effects, sample rates, SDK version, and GPU compute architecture.
- Use NGC/API-key access and respect NVIDIA AI Enterprise / product terms where required.
- Query supported sample rates, channel counts, and frame sizes from the SDK instead of hardcoding them.
- Keep input/output audio as 32-bit float for the SDK effects unless current docs for the chosen effect state otherwise.
- Prefer local SDK processing for sensitive, unreleased, health, legal, enterprise, or talent-protected recordings when hardware and licensing allow.

### BNR NIM

Use BNR NIM when the job is specifically Background Noise Removal and the team wants a containerized service with gRPC, cloud/datacenter deployment, health checks, observability, and scalable inference.

BNR NIM has two modes:

- Streaming mode: recommended for live applications; raw audio is processed in 10 ms chunks.
- Transactional mode: complete-file request/response for offline enhancement and post-production; official Try API docs list WAV-only input constraints and a 35 MB / 6 minute limit for preview-style hosted requests.

Operational implications:

- Launch with Docker, NVIDIA Container Toolkit, a supported Tensor Core GPU, `NGC_API_KEY`, and a compatible `NIM_MODEL_PROFILE` when selecting a profile explicitly.
- Use gRPC on the service port, run a health check before production, and collect Prometheus/Triton metrics for throughput and failures.
- Use TLS or mTLS for networked deployment; hosted preview requests require TLS.
- Cache model artifacts locally for repeat runs where allowed.
- Treat hosted Try API as a testing path unless the user has approved uploading audio to NVIDIA-hosted infrastructure and the terms fit the project.

## Effect selection map

Start from the artifact, not the tool name.

| Input problem | Recommended Maxine path | Avoid |
|---|---|---|
| Fan, keyboard, traffic, HVAC, household noise under speech | BNR / `denoiser`; consider BNR 2.0 for ASR-prep if current docs and access support it | Heavy intensity before checking consonants, breaths, and emotion |
| Roomy lavalier, echoey webinar, reflective office | `dereverb`; if noise is also present use `dereverb_denoiser` | Using AEC for room reverb; AEC solves far-end playback echo |
| Remote guest hears their own delayed voice in a live call | `aec` with near-end mic plus far-end reference signal | Offline dereverb-only cleanup |
| Narrowband phone/Zoom archive that must become 48 kHz delivery audio | `superres` after basic cleanup, or a supported chain such as superres -> denoise where documented | Claiming real high-frequency recovery; describe it as inferred enhancement |
| Cheap headset or laptop mic sounds thin/static/processed | Studio Voice High Quality for offline; Low Latency for live | Low-latency Studio Voice for batch post-production |
| Main presenter has other people talking in background | `speaker_focus` only if Early Access/access constraints are acceptable and the clip has a clear primary speaker | Promising perfect diarization or multi-speaker preservation |
| User asks to make one person sound like another | Voice Font only with explicit rights/consent, reference custody, and disclosure policy | Covert voice conversion, impersonation, or using unlicensed reference speech |

For podcast, ad, avatar, or social pipelines, make Maxine one stage in a broader audio finish:

1. Ingest and archive the untouched original.
2. Convert a working copy to the required mono/stereo, sample rate, and 32-bit float format.
3. Run the selected Maxine effect(s).
4. Compare against the original.
5. Apply conventional finishing after cleanup: trim, de-click if needed, loudness normalization, EQ, compression, limiter, captions/ASR, and final mux.

## Ordering heuristics

Documented effect constraints override these heuristics.

- Preserve an untouched master. Never process destructively over the only copy.
- For noisy + reverberant speech, prefer NVIDIA's combined `dereverb_denoiser` over separate denoise and dereverb.
- For narrowband speech, decide whether intelligibility or delivery bandwidth is the goal:
  - for ASR, test denoise at native 16 kHz before super-resolution;
  - for final media delivery, cleanup then super-resolution can sound more polished, but must be checked for metallic highs.
- For live conferencing:
  - AEC belongs in the bidirectional audio path with synchronized far-end reference;
  - BNR/Dereverb/Studio Voice Low Latency can sit on the near-end microphone path;
  - keep total audio latency budget visible because each stage adds buffering.
- For offline post:
  - use higher-quality/offline variants where NVIDIA provides them;
  - process scene-by-scene or speaker-by-speaker rather than one global setting across a mixed program;
  - keep handles, file hashes, model/effect versions, intensity, sample rate, and output paths in an audio ledger.

## Input preparation

Before running an effect:

- Identify source type: single-speaker voiceover, live call, panel podcast, remote guest, avatar narration, ad VO, phone archive, or noisy UGC.
- Confirm rights: speaker consent, client permission, union/talent restrictions, and whether cloud processing is allowed.
- Capture diagnostics:
  - sample rate, bit depth/format, channels;
  - duration and file size;
  - speech regions vs silence/music;
  - dominant defects: stationary noise, transient noise, reverb tail, far-end echo, competing speakers, codec artifacts, clipping.
- Convert only the working copy. Keep the original's timecode and file hash.
- For SDK effects, match the model's sample rate and GPU architecture; for NIM, match the client sample rate to the selected NIM model profile.
- For AEC, provide the far-end reference signal. If the reference is missing, say AEC is not properly specified and offer dereverb/denoise alternatives if those defects are present.

## Intensity and repair strategy

Use the least processing that solves the content problem. NVIDIA exposes an `intensity_ratio` for several workflows where `0` is effectively passthrough and `1` is maximum impact. In production, render a small A/B ladder before committing:

- `0.35-0.50`: light cleanup for premium voiceover, interview, or emotional performance.
- `0.60-0.80`: typical remote guest, webinar, or social clip cleanup.
- `0.85-1.00`: rescue audio where intelligibility matters more than naturalness.

Listen for over-processing:

- lisping, missing fricatives, dull consonants;
- warbling/phasiness on sustained vowels;
- room tone pumping between words;
- breaths or laughter removed when they are part of the performance;
- metallic or "AI glossy" high end after super-resolution;
- timing drift or mismatched duration after streamed/chained processing.

If artifacts appear, reduce intensity, split the clip into regions, bypass clean sections, try native sample-rate cleanup before super-resolution, or use conventional editing for clicks/clips instead of stronger AI cleanup.

## Production applications

### Video conferencing and livestreaming

Use low-latency paths only. For a two-way call, route microphone audio through BNR/dereverb/Studio Voice Low Latency as needed and route echo cancellation through AEC with the far-end signal. Measure round-trip latency; do not add high-quality offline Studio Voice or large-buffer batch steps to a live path.

### Podcast and interview cleanup

Process each participant independently where possible. Use BNR for background noise, `dereverb_denoiser` for remote rooms with both hiss and reverb, and Speaker Focus only when background speakers are disposable. Preserve laughter, sighs, and emotional tone unless the brief says to sanitize them. Normalize loudness only after AI cleanup.

### Avatar, spokesperson, and ad VO

For recorded human VO, prioritize naturalness over maximum suppression. Use light-to-medium BNR or Studio Voice High Quality, then EQ/compress. For synthetic/avatar voice tracks, avoid heavy denoise unless there is actual generated noise; many artifacts are vocoder issues better fixed upstream by regenerating the voice.

### Social and UGC rescue

Use stronger cleanup if the platform and content tolerate a processed sound. Create a 10-20 second proof segment first. Preserve viral context noises if they matter to the joke/story; do not remove everything that is not speech by default.

### Localization and ASR prep

When audio is being cleaned before transcription, prioritize word error reduction over studio tone. BNR 2.0 is documented as a newer experimental denoiser focused on ASR accuracy; use it only if the current SDK/NIM path supports it and label the choice experimental. Always run before/after ASR spot checks on names, numbers, and code-switching.

## Privacy, consent, and security

Audio often contains biometric voice data, private conversations, unreleased scripts, and background speech from bystanders. Before processing:

- Use local AFX SDK or self-hosted NIM when the project is sensitive or contractually restricted.
- Get explicit approval before sending audio to NVIDIA-hosted Try API or any third-party cloud.
- Store API keys in environment variables or a secrets manager; never log keys in command lines, notebooks, or artifacts.
- Use TLS/mTLS for networked NIM services when audio crosses hosts.
- Minimize retention: keep originals, processed outputs, logs, and reference samples only as long as the project requires.
- For Voice Font, require explicit permission from both the input speaker and the reference speaker; document intended use and disclosure. Reject covert impersonation, fraud, harassment, or non-consensual identity conversion.
- For Speaker Focus, remember that suppressing background speakers can remove context and consent evidence; keep the original.

## Artifact custody checklist

For every Maxine processing run, record:

- source file path, source hash, duration, sample rate, channels;
- effect selector and variant, SDK/NIM version, model/profile, GPU architecture, and verification date;
- runtime path: Windows SDK, Linux SDK, self-hosted NIM, or hosted Try API;
- exact parameters: intensity, sample rate, streaming/transactional, batch/concurrency, chain order;
- privacy path: local/cloud, TLS/mTLS, key handling, retention;
- output file path and hash;
- QA notes with representative A/B timestamps.

## QA rubric

Pass a processed file only when it satisfies all applicable checks:

- Speech intelligibility improves or stays strong in noisy regions.
- Speaker identity and emotional tone remain acceptable for the brief.
- Consonants, breaths, laugh/sigh cues, and room pauses are not unnaturally removed.
- Noise floor is stable; no gating or pumping distracts between phrases.
- Reverb tails are reduced without making the voice sound underwater.
- AEC output removes far-end echo without suppressing double-talk or near-end speech.
- Super-resolution improves perceived bandwidth without brittle, metallic highs.
- Studio Voice does not make the speaker sound like a different person unless explicitly intended.
- Speaker Focus does not remove the intended speaker or create jumpy handoffs.
- Output duration, sync, and sample rate match the downstream video/audio pipeline.
- Final loudness is handled after cleanup according to the distribution target.

Use both objective and subjective checks. Objective checks can include waveform duration, LUFS, peak/true peak, spectrogram inspection, ASR before/after on a representative segment, and dropped-frame/sync checks after video mux. Subjective checks require headphones and at least one loudspeaker pass because denoise artifacts often reveal themselves differently.

## Example: offline podcast guest rescue

Production intent: clean a 42-minute remote podcast guest recorded in a kitchen with fridge hum, laptop fan, and room reverb.

Approach:

1. Archive the untouched WAV.
2. Split the guest track from host/music beds.
3. Convert the guest working copy to the supported 48 kHz 32-bit float mono/stereo format required by the chosen SDK effect.
4. Render a 30-second proof using `dereverb_denoiser` at intensity `0.55`, `0.70`, and `0.85`.
5. Pick the lowest setting that makes words clear without dulling laughter or consonants.
6. Apply final EQ, compression, and LUFS normalization after Maxine cleanup.
7. Spot-check timestamps with high laugh density, fast speech, and silent gaps.

Why: the combined effect is designed for simultaneous noise and reverb; a proof ladder avoids over-processing a long performance.

Expected result: clearer speech and reduced room tone while retaining the guest's personality.

Failure modes: watery vowels at high intensity, clipped plosives that no denoiser can fix, background clatter that survives the first seconds, and ASR regressions on proper nouns.

## Example: live webinar audio path

Production intent: improve a live panel webinar without adding noticeable delay.

Approach:

1. Use real-time compatible effects only.
2. For each speaker stream, route near-end microphone through BNR if background noise is the main issue.
3. If participants hear their own voice back, configure AEC with both near-end microphone and far-end playback/reference signal.
4. If using Studio Voice, choose Low Latency and verify the GPU can meet the target without buffer underruns.
5. Monitor total latency, dropped chunks, GPU utilization, and double-talk quality.

Why: AEC solves far-end echo, while BNR/dereverb clean the microphone path. Offline/high-quality models are not appropriate for live latency budgets.

Expected result: intelligible panel audio with less feedback/noise and no major delay.

Failure modes: AEC without a correct far-end reference, over-suppression during double-talk, and latency spikes when concurrency exceeds GPU resources.

## Example: BNR NIM cloud-safe production plan

Production intent: batch-clean short social clips before captioning, using a self-hosted BNR NIM on an internal GPU server.

Plan:

1. Confirm the job only needs Background Noise Removal.
2. Launch self-hosted NIM with the supported GPU, `NGC_API_KEY`, selected compatible `NIM_MODEL_PROFILE`, published service port, and TLS/mTLS if clients are remote.
3. Run a health check and verify metrics endpoint visibility.
4. Use transactional mode for complete WAV files; if clips exceed current limits or are not WAV, segment/convert working copies before processing.
5. Run ASR before/after on representative clips and compare name/number accuracy.
6. Write an artifact ledger with source hash, model profile, mode, intensity, output hash, and retention policy.

Why: NIM gives service deployment and observability while keeping audio inside the organization's infrastructure.

Expected result: cleaner captions and fewer ASR errors without uploading unreleased social assets to a hosted preview endpoint.

Failure modes: wrong model profile for the GPU, WAV/sample-rate mismatch, unsecured internal service, or treating preview API limits as production guarantees.

## Official sources verified 2026-07-10

- NVIDIA Audio Effects SDK User Guide, effects overview and Windows/Linux positioning: https://docs.nvidia.com/maxine/afx/latest/index.html
- NVIDIA AFX SDK API type definitions and selectors: https://docs.nvidia.com/maxine/afx/latest/APIReference/AFXTypeDefinitions.html
- NVIDIA AFX SDK Linux getting started and Tensor Core GPU requirements: https://docs.nvidia.com/maxine/afx/latest/LinuxAFXSDK/GetStartedOnLinux.html
- NVIDIA AFX SDK Linux installation and feature package model layout: https://docs.nvidia.com/maxine/afx/latest/LinuxAFXSDK/InstallTheAFXSDK.html
- NVIDIA AFX SDK set/query parameter docs: https://docs.nvidia.com/maxine/afx/latest/UseAFXInApps/SetParametersOfAnEffect.html and https://docs.nvidia.com/maxine/afx/latest/UseAFXInApps/GetParametersOfAnEffect.html
- NVIDIA AFX effect pages for BNR, dereverb, dereverb+denoiser, AEC, super-resolution, Studio Voice, Speaker Focus, and Voice Font: https://docs.nvidia.com/maxine/afx/latest/AboutTheEffects/AboutNoiseRemovalBackgroundNoiseSuppression.html
- NVIDIA BNR NIM overview, getting started, inference, support matrix, observability, and governing terms: https://docs.nvidia.com/nim/maxine/bnr/latest/overview.html
- NVIDIA NGC Windows/Linux AFX SDK collection pages and BNR/BNR-REC catalog pages: https://catalog.ngc.nvidia.com/orgs/nvidia/maxine/resources/maxine_windows_audio_effects_sdk/- and https://catalog.ngc.nvidia.com/orgs/nvidia/maxine/resources/maxine_linux_audio_effects_sdk/-
- NVIDIA AI for Media product page noting Maxine rename and SDK/NIM scope: https://developer.nvidia.com/topics/ai/generative-ai/ai-for-media
