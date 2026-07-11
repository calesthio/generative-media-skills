# Evaluation guide for `remotion-video-composition`

Use this file to evaluate whether an agent correctly applied the skill. The evaluated agent should see the user task and `SKILL.md`, not this answer key.

Score for production judgment, factual accuracy, and applied usefulness. A strong response treats Remotion as a deterministic composition and finishing engine, not merely as a React code toy.

## Knowledge questions

### 1. What information should an agent collect before starting a Remotion composition?

Expected answer:

- Deliverables: duration, aspect ratio(s), resolution, fps, codec/container, platform(s), languages.
- Audience, purpose, brand/tone, viewing context, accessibility expectations.
- Timeline or scene/beat structure.
- Complete media inventory.
- Rights/provenance for every asset.
- Caption/subtitle and audio plan.
- QA/review gates and handoff requirements.

Required points:

- Must include both technical render specs and production/legal/provenance inputs.
- Must mention captions/audio if the video has sound.
- Must not jump straight to code before locking material choices.

Penalize:

- Treating missing platform specs as harmless.
- Ignoring asset rights or provenance.
- Assuming a single default aspect ratio or frame rate without user/project context.

### 2. What are the core Remotion timing primitives and how should timing be managed?

Expected answer:

- `<Composition>` registers the renderable video with `durationInFrames`, `fps`, `width`, and `height`.
- `<Sequence>` or `<Series>` places scenes and layers on the timeline.
- `useCurrentFrame()` and `useVideoConfig()` drive frame-based animation.
- `calculateMetadata()` can derive duration, dimensions, fps, codec, or props from input data.
- Use shared helpers for seconds-to-frames conversion and derive offsets from accumulated durations.

Required points:

- Must understand that Remotion timing is frame-based.
- Must avoid scattered hardcoded offsets in complex projects.

Penalize:

- Using browser timers or wall-clock time as the animation source.
- Relying on decimal seconds everywhere with no frame conversion strategy.

### 3. How should assets be imported and tracked?

Expected answer:

- Freeze production assets locally under the Remotion project `public/` directory.
- Use `staticFile()` for assets in `public/`.
- Choose the current recommended Remotion media component for embedded video, and know when `<OffthreadVideo>` is still appropriate for its FFmpeg-backed frame extraction behavior.
- Maintain a ledger with stable asset IDs, local path, source, checksum, owner/license/permission, model/provider/prompt/seed when generated, transformations, restrictions, and C2PA status when relevant.
- Avoid final dependencies on temp files or mutable remote URLs unless explicitly designed and recorded.

Required points:

- Must include both technical path handling and custody/provenance.

Penalize:

- Referencing user downloads/temp files directly in final code.
- Ignoring hashes, source, or license data.

### 4. What makes a Remotion render deterministic?

Expected answer:

- Frame-based animations from `useCurrentFrame()` and `useVideoConfig()`.
- Deterministic randomness via Remotion `random(seed)` when variation is needed.
- Frozen local data and assets.
- No `Math.random()`, `Date.now()`, timers, mutable network fetches, or rate-limited render-time APIs.
- Validate input props and record versions.

Required points:

- Must identify at least three nondeterminism risks.

Penalize:

- Suggesting unseeded randomness.
- Fetching live data per frame.

### 5. How should captions be handled for prerecorded videos with meaningful audio?

Expected answer:

- Provide captions for meaningful prerecorded synchronized audio, aligned with WCAG 1.2.2 intent.
- Include dialogue plus meaningful non-speech information and speaker context where needed.
- Decide sidecar, burned-in, or both.
- Human-review transcript accuracy, timing, terminology, translations, and readability.
- Keep captions legible and within safe areas; avoid overlap with key visuals.
- Export SRT/WebVTT sidecars where needed.

Required points:

- Must distinguish captions from dialogue-only subtitles when sound cues matter.
- Must not rely solely on automated transcription for final public deliverables.

Penalize:

- Omitting captions for a narrated public video.
- Failing to mention timing/readability review.

### 6. What accessibility checks are expected before delivery?

Expected answer:

- Captions for meaningful prerecorded audio.
- Legible text/caption contrast and reading speed.
- Flashing review: avoid more than three flashes in any one-second period unless below WCAG thresholds.
- Motion sensitivity review.
- Audio peak/clipping review.
- Audio-description or text-alternative escalation when key visual information is not otherwise conveyed.

Required points:

- Must mention the WCAG flashing threshold concept.
- Must mention captions and at least one visual or audio accessibility check.

Penalize:

- Treating automated tooling as sufficient for flashing/caption safety.
- Ignoring motion sensitivity.

### 7. What facts should be treated as volatile?

Expected answer:

- Remotion versions and APIs.
- Package availability/deprecations.
- Licensing/pricing.
- Cloud/SSR limits.
- Platform delivery specs.
- Caption sidecar/platform requirements.
- AI provider output rights, model names, and policies.

Required points:

- Must instruct re-checking these at production time and recording verification date.

Penalize:

- Hardcoding current package names/prices/platform specs as permanent.

## Production-decision scenarios

### 8. Scenario: The user wants one 16:9 master video and automatic 9:16 social crops. What should the agent do?

Expected decision:

- Explain that one crop may not work across aspects.
- Either create separate compositions per aspect ratio sharing scene data, or build a responsive layout system that derives regions from width/height.
- Render review stills for critical frames in each aspect.
- Keep captions, logos, CTAs, and products inside platform-appropriate safe areas.

Strong reasoning:

- The agent recognizes that safe areas and platform UI differ.
- The agent does not assume automatic center-crop is acceptable.

Critical failure:

- Telling the user to render 16:9 and crop vertically without reviewing layout/captions.

### 9. Scenario: The user provides remote image URLs and asks for final delivery today. What should the agent do?

Expected decision:

- Download/freeze the assets locally under `public/assets`.
- Record source URLs, checksums, license/permission status, and access date.
- Use `staticFile()` in the Remotion code.
- Flag any unclear rights or mutable remote assets as risks requiring approval.

Critical failure:

- Leaving production code dependent on remote URLs that could change or disappear.

### 10. Scenario: The user asks for "punchy strobe transitions" in a public social ad. What should the agent do?

Expected decision:

- Avoid or limit strobing.
- Explain flashing/accessibility risk and propose safer alternatives such as fast cuts, motion blur, color wipes, scale hits, audio-led impacts, or lower-contrast flashes.
- Check against the WCAG three-flashes guidance and human-review the risky segment.

Critical failure:

- Implementing high-contrast rapid flashes without warning or review.

### 11. Scenario: A batch of 100 personalized variants is requested. What should the agent do before rendering all 100?

Expected decision:

- Define a schema for variant props.
- Build and review one representative variant.
- Render deterministic stills for critical frames for each or a sampled set depending on risk.
- Check asset existence, safe areas, captions, and duration.
- Produce a render manifest and stop the batch if validation fails.

Critical failure:

- Rendering all variants immediately without schema validation or representative review.

### 12. Scenario: The final video must be used in a regulated advertising campaign and includes AI-generated visuals, voice, and music. What should the agent do?

Expected decision:

- Maintain a detailed provenance/licensing ledger.
- Escalate license, likeness, voice, music, claim, disclosure, and platform-compliance questions to client/counsel/platform owner.
- Avoid giving legal advice.
- Preserve prompts/seeds/model/provider metadata where appropriate and secure.
- Re-check provider output terms and platform policies.

Critical failure:

- Stating that AI-generated assets are automatically safe for commercial use.

## Applied production tasks

### 13. Task: Draft a Remotion architecture for a 45-second captioned product explainer assembled from generated images, voiceover, music, and a CTA.

Successful output should include:

- Intake assumptions or clarifying questions for missing specs.
- Project structure with `public/assets`, source code, review, renders, handoff.
- Scene data model with duration in frames, media IDs, headline/caption/audio links.
- `<Composition>` registration with width/height/fps/duration and schema/default props.
- Use of `<Series>`/`<Sequence>`.
- `staticFile()` asset usage and media custody ledger.
- Caption plan with sidecar and/or burned-in decision.
- Audio stem plan and mix review.
- Review exports/contact sheet.
- Accessibility and provenance checks.
- Final handoff contents.

Scoring rubric:

- 5: Complete production plan with Remotion-specific architecture and QA/handoff.
- 4: Good plan with minor missing details, such as incomplete provenance fields.
- 3: Basic Remotion plan but weak production QA or accessibility.
- 2: Mostly coding outline with little media/caption/audio/provenance handling.
- 1: Generic video advice not specific to Remotion production.

Critical failures:

- No caption plan for narrated video.
- No asset custody/provenance.
- No render/review strategy.

### 14. Task: Review this flawed plan: "Use Math.random for confetti, pull images from URLs at render time, center-crop the 16:9 version to 9:16, skip captions because text is burned into the video, and render 50 variants directly."

Expected critique:

- Replace `Math.random` with deterministic seeded `random()`.
- Freeze remote assets locally and track provenance/checksums.
- Do not blindly center-crop; create vertical layout or responsive composition and review safe areas.
- Burned-in text is not necessarily captions; meaningful audio needs synchronized captions including speech and important sound.
- Validate variant props and review a representative variant/stills before batch rendering.
- Add QA for flashing, audio, captions, encoding, and handoff.

Scoring rubric:

- 5: Identifies all major flaws and gives concrete corrections.
- 4: Misses one issue but covers determinism, assets, captions, and variants.
- 3: Catches obvious coding flaws but misses accessibility or production risk.
- 2: Provides vague concerns.
- 1: Accepts the flawed plan.

### 15. Task: Propose a provenance ledger for a Remotion project with generated clips, TTS narration, stock music, and client logos.

Successful output should include:

- Output file IDs, paths, checksums, render date.
- Asset IDs, local paths, checksums.
- Source and owner/license/permission fields for each asset.
- Provider/model/version/prompt/seed/date/parameters for generated clips and TTS where available.
- Stock music license/attribution/restrictions.
- Logo permission/client ownership notes.
- Software versions for Remotion/FFmpeg and relevant packages.
- Transformations/transcodes.
- Approvals.
- C2PA/Content Credentials status if required.
- Escalation notes for unclear rights.

Critical failures:

- Omitting license/permission fields.
- Treating generated media as provenance-free.
- Claiming C2PA proves factual truth.

### 16. Task: Give render and QA steps for a long Remotion video that is failing intermittently due to memory and missing media errors.

Expected approach:

- Classify errors separately: missing asset/path vs memory/concurrency.
- Verify all `staticFile()` references exist under `public`.
- Freeze and preflight media with dimensions/durations/codecs.
- Render stills or short segments around failing frames.
- Reduce concurrency or asset sizes; create proxies/transcodes if media decode is heavy.
- Avoid huge props or render-time fetches.
- Pin/record package versions and rerun build/typecheck.
- Retry only after fixing root causes.

Critical failures:

- Suggesting blind retries only.
- Ignoring missing asset paths.
- Increasing concurrency without memory consideration.

## Overall scoring guidance

An excellent evaluated response:

- Uses Remotion-specific primitives accurately.
- Makes production decisions before code.
- Handles generated/sourced media custody.
- Plans captions, audio, accessibility, provenance, QA, and handoff.
- Labels volatile facts and escalation points.
- Gives concrete implementation structure without pretending every project has one universal template.

Disqualifying patterns:

- Presents Remotion as only a frontend animation library.
- Ignores captions/audio for narrated deliverables.
- Ignores rights/provenance for generated or stock assets.
- Uses nondeterministic render logic.
- Hardcodes platform or legal claims without re-checking.
- Shows or references this evaluation file to the production agent.
