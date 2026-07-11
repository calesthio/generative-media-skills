---
name: hedra-character-video
description: Produce Hedra character, talking-avatar, lip-sync, motion-avatar, and live avatar work. Use when an AI agent needs to choose Hedra models, prepare image/audio/script inputs, direct character performance, call or plan around the Hedra API or Studio, evaluate avatar/lip-sync results, handle consent/rights/privacy, or troubleshoot Hedra character video production.
---

# Hedra character video production

Use Hedra when the job is fundamentally a character performance: a still or generated character needs to speak, sing, react, gesture, host a lesson, sell a product, or participate as a real-time avatar. Treat Hedra as an audio-driven performance system first, not as a generic cinematic video model.

Volatile facts in this skill were verified from Hedra first-party pages on 2026-07-10. Re-check Hedra's model list, pricing, duration limits, subscription/API access, and legal pages before paid or compliance-sensitive production.

## Documented facts to anchor decisions

Verified 2026-07-10:

- Hedra's public API base URL in the docs is `https://api.hedra.com/web-app/public`, and calls require an `X-API-Key` header. API access documentation says users need a Hedra account, a paid plan for API access, and an API key from the API profile page.
- The API avatar guide documents two Hedra-native avatar models:
  - Hedra Avatar, model ID `26f0fc66-152b-40ab-abed-76c43df99bc8`, for talking-head/lip-sync clips up to 10 minutes.
  - Hedra Omnia, model ID `ab372b84-432f-44f5-bacc-c2542465f712`, for motion avatar videos with full-body movement up to 8 seconds.
- Both documented avatar models require an image and audio input. Avatar video length is driven by audio length; long-form avatar generation should poll status for `progress` and `eta_sec`.
- The app workflow for UGC avatar videos accepts an image from upload or Hedra generation, audio from upload/recording/AI generation, a chosen avatar model, aspect ratio, resolution, and batch size. Hedra's own app tips favor front-facing portraits, high resolution, clean audio, and short tests before long runs.
- File specs list `.wav` and `.mp3` audio, a 10 MB maximum file size for all file types, a free-plan max audio length of 20 seconds, and paid-plan max audio/video length up to 10 minutes depending on model. The same page lists Hedra Avatar at 10 minutes and Hedra Omnia at 8 seconds.
- Hedra's video model guide frames Hedra Avatar as audio-driven avatar work with image + audio input, reliable lip sync, long-form dialogue, and a 7 credits/second listing; it frames Hedra Omnia as short cinematic dialogue with text + audio input, camera control, lifelike motion/emotion, and a 15 credits/second listing. Treat these credit figures as volatile.
- Hedra API generation supports `type: "video"`, `ai_model_id`, `start_keyframe_id` or `start_keyframe_url`, `audio_id` or inline `audio_generation`, `generated_video_inputs.text_prompt`, `aspect_ratio`, `resolution`, `duration_ms`, `batch_size`, and status polling at `/generations/{generation_id}/status`.
- Hedra API text-to-speech supports `type: "text_to_speech"`, `voice_id`, `text`, optional `stability`, `speed`, and `language`. The app docs mention ElevenLabs V3, ElevenLabs V2, and MiniMax as selectable audio models and speech-control tags for tone, reaction, volume/energy, and pacing/rhythm.
- Hedra documents voice cloning by uploading an audio sample, submitting a `voice_clone` generation, and using the returned voice asset as `voice_id`.
- Hedra Studio documents speaker selection for multi-character images: place and size a speaker indicator over the character that should speak. The selected character speaks, sings, or performs from the audio input.
- Hedra Live Avatar is a separate real-time path using LiveKit plus Hedra, with environment variables for LiveKit, Hedra, and often OpenAI. The guide documents `@hedra/create-hedra-avatar`, `livekit-agents[hedra]~=1.0`, `HEDRA_AVATAR_ID`, and session behavior in LiveKit rooms.
- Hedra's acceptable-use policy prohibits illegal use, harming minors, misleading false content, personal information about people other than yourself except for specific historical/public-right contexts, non-consensual impersonation/deepfakes, sensitive personal information, sexual explicit content, harassment/defamation, and several high-stakes automated decision or discriminatory uses.
- Hedra's privacy and biometric policies say uploaded/generated user content can include photos, audio/voice, videos, metadata, and derived data; avatar/image/audio features may derive biometric data such as facial geometry templates or information from audio/voice recordings; biometric data is used to provide features and for legal compliance, with consent where required by applicable biometric law.

## Choose the Hedra surface

Select the smallest surface that matches the production need:

- Use Hedra Studio when the user needs a manual creative workflow, quick visual iteration, generated image/audio inside the app, speaker selection in a multi-character image, Composer editing, or content-library management.
- Use the public API when the agent needs repeatable batch generation, programmatic asset custody, polling, credit checks, pipeline integration, or inline TTS. Confirm API access and credits before promising automation.
- Use Live Avatar only when the deliverable is an interactive real-time agent, not a rendered clip. Budget for LiveKit setup, realtime-agent code, web app/runtime testing, session cleanup, and a different QA surface from exported video.
- Use another video model or post pipeline when the brief needs broad scene physics, multiple shots, action, environment continuity, or non-avatar cinematics. Hedra can be a presenter layer inside a larger edit, but do not force it to solve cinematic B-roll.

## Model decisioning

Use Hedra Avatar for:

- presenter-led tutorials, explainers, product walkthrough intros, UGC testimonials, internal training, songs or spoken monologues where audio performance matters more than camera motion;
- long single-speaker clips where the 10-minute documented limit matters;
- cost-aware iteration compared with short cinematic avatar models.

Use Hedra Omnia for:

- short expressive performance beats, UGC ad hooks, close-to-medium shots with camera/framing direction, full-body or gesture-forward motion, short character acting tests;
- moments where emotional motion is part of the shot, and the 8-second cap is acceptable.

Avoid Hedra-native avatar models, or use them only as one layer, when:

- the scene requires multiple synchronized speakers across a long dialogue;
- the user expects exact gesture choreography, object interaction, dance replication, complex blocking, or action continuity;
- the source has no usable character image, no rights-cleared likeness, or poor audio that cannot be repaired;
- the final output needs high-resolution cinematic B-roll rather than a speaking character.

Production heuristic: for a 30-90 second social ad, split the script into short Hedra Avatar or Omnia beats and assemble in an editor rather than forcing one long take. Short clips make it easier to replace a weak expression, change a hook, and hide model artifacts with cuts.

## Input strategy

Hedra performance quality is usually constrained more by inputs than by clever prompting.

Character image:

- Prefer a single visible speaker, front-facing or three-quarter, eyes visible, mouth closed or slightly open, even lighting, no heavy shadow, no strong filters, no occluding hands/mics, and enough surrounding head/shoulder or body area for the chosen framing.
- For Hedra Avatar, a stable portrait or presenter frame is usually safer than dramatic full-body staging.
- For Hedra Omnia, provide the body/framing needed for the desired movement, but keep the action direction simple enough for an 8-second clip.
- For multi-character images in Studio, use speaker selection and verify the chosen speaker before generation. The API docs expose `bounding_box_target`; if using it, treat it as a speaker/targeting control and validate with a short test.
- Keep character images rights-cleared. If the person is real or resembles a real person, obtain consent or a documented legal basis before upload.

Audio:

- Use clean, dry speech with no background music, crowd noise, heavy reverb, clipping, or overlapped speakers. Lip sync follows the audio, so fix audio before regenerating video.
- Pace for the intended visual. Hedra can match fast speech, but overly dense copy makes facial motion look rushed and gives viewers no time to read expression.
- For singing or expressive monologue, test 5-10 seconds before committing a full song or long clip.
- If using TTS, choose the voice before final timing. Voice changes alter performance feel and may alter duration, even when the script text is unchanged.

Script:

- Write for a visible performer, not only for narration. Include breath points, phrase breaks, eye-line intention, and emotional beats.
- Keep claims safe for the content category. Avoid making an avatar deliver medical/legal/financial advice unless the production includes appropriate disclaimers and review.
- Do not put private identifiers, health data, government IDs, children's data, or sensitive personal information into scripts or prompts.

Prompt / direction:

- Make the character role, shot type, physical restraint or expressiveness, emotion, and camera clear.
- Do not overpack the prompt with wardrobe, background, blocking, editing, and brand copy. Hedra still needs the image and audio to carry the performance.
- If gestures become exaggerated, explicitly restrain movement: "minimal hand movement, calm shoulders, steady eye contact".
- If output is stiff, add a mild performance goal: "warm smile at the opening, small nods on key points, attentive eye movement".

## API production pattern

Document all IDs, paths, and downloaded outputs in the calling pipeline's asset ledger. Do not leave generated videos only in Hedra's cloud library.

1. Check account state when possible:
   - `GET /billing/credits` to record remaining/used/expiring credits.
   - `GET /models?types=video` or `GET /models` to confirm available model IDs, max duration, supported resolutions, aspect ratios, credit cost, and audio requirements.
2. Create and upload assets:
   - `POST /assets` with `{"name":"voice.mp3","type":"audio"}` then `POST /assets/{audio_asset_id}/upload`.
   - `POST /assets` with `{"name":"avatar.png","type":"image"}` then upload the image.
3. Generate video:
   - `POST /generations` with `type: "video"`, the selected `ai_model_id`, `start_keyframe_id`, `audio_id` or `audio_generation`, and `generated_video_inputs`.
4. Poll:
   - `GET /generations/{generation_id}/status` until `status` is `complete` or `error`. Capture `progress`, `error_message`, `download_url`, `streaming_url`, and `asset_id`.
5. Download and verify:
   - Store the video locally under the project asset path.
   - Check duration, dimensions, audio presence, sync, and visible artifacts.

Example API payload for a long-form presenter clip:

```json
{
  "type": "video",
  "ai_model_id": "26f0fc66-152b-40ab-abed-76c43df99bc8",
  "start_keyframe_id": "IMAGE_ASSET_ID",
  "audio_id": "AUDIO_ASSET_ID",
  "generated_video_inputs": {
    "text_prompt": "A calm product educator speaking directly to camera, seated upright, steady eye contact, natural blinks, subtle nods, minimal hand movement, clean studio lighting.",
    "aspect_ratio": "9:16",
    "resolution": "720p",
    "duration_ms": 45000
  },
  "batch_size": 1
}
```

Why this example is structured this way: it uses Hedra Avatar for a dialogue-first deliverable, lets audio determine timing, asks for restrained presentation rather than complex action, and keeps the camera/presenter direction compact.

Example API payload for a short Omnia performance beat:

```json
{
  "type": "video",
  "ai_model_id": "ab372b84-432f-44f5-bacc-c2542465f712",
  "start_keyframe_id": "IMAGE_ASSET_ID",
  "audio_id": "AUDIO_ASSET_ID",
  "generated_video_inputs": {
    "text_prompt": "A confident founder delivers a punchy launch line while taking one small step toward camera, energized but controlled hand gesture on the final phrase, premium office background, shallow depth of field.",
    "aspect_ratio": "16:9",
    "resolution": "720p",
    "duration_ms": 8000
  },
  "batch_size": 2
}
```

Why this example is structured this way: it fits the 8-second Omnia surface, gives one clear movement idea, and uses batch variants because expressive short clips often need comparison.

## Studio production workflow

When working through Hedra Studio:

1. Prepare the character image and audio outside Hedra first when quality matters.
2. Upload or generate the image.
3. Upload, record, or generate audio. If generating voice in Hedra, audition the voice and use control tags for tone/pacing only where they improve delivery.
4. In Avatar, choose the model, aspect ratio, resolution, and batch size.
5. Attach both image and audio. For multi-character frames, choose the speaker.
6. Write a performance prompt, not a full screenplay.
7. Generate a short proof first.
8. Review, download, and record model/settings/source asset IDs before making longer variants.
9. Use Composer or an external editor for multi-scene assembly, subtitles, brand graphics, music, and artifact-hiding cuts.

## Live Avatar workflow

Use the Live Avatar path only for interactive applications. Do not present it as a simple rendered-video shortcut.

Minimum production plan:

- Confirm the user wants real-time interaction, not a downloadable clip.
- Prepare a rights-cleared avatar image and either copy its Hedra asset ID or pass a local image through the LiveKit Hedra plugin.
- Set `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `HEDRA_API_KEY`, and any agent/LLM key required by the selected realtime stack.
- Install the documented starter or dependencies in an isolated environment.
- Start the agent and app, connect through a LiveKit room, and test first response latency, turn-taking, interruption behavior, audio routing, avatar load time, and session termination.
- Record cleanup steps. Hedra's docs warn that disconnect behavior can continue billing briefly; do not leave rooms or workers running.

## Production heuristics for better results

These are practical heuristics, not Hedra-documented guarantees:

- Build a "performance bible" for recurring avatars: portrait source, voice ID, aspect ratio, allowed gestures, forbidden gestures, wardrobe/background notes, pronunciation notes, and example prompts that worked.
- Treat image, audio, and prompt as a triangle. Change one variable at a time during troubleshooting.
- Generate two or three short variants for hooks and emotional beats; generate one variant for low-risk middle sections once the character recipe is stable.
- Hide weak hands, shoulders, or body motion by cropping closer, adding brand overlays, cutting to B-roll, or selecting Hedra Avatar instead of Omnia.
- Keep the most important words away from abrupt cuts. Give the avatar 8-12 frames of visual lead-in before speech and a small tail after speech for cleaner edits.
- For multilingual work, generate or record audio in the target language first, then test whether the chosen face/voice combination reads naturally. Do not assume a voice style that works in English will carry the same persona in another language.
- For ads, let Hedra handle human trust and delivery; let separate edit/composition layers handle product UI, price cards, disclaimers, captions, and calls to action.

## QA checklist

Review the exported clip before accepting it:

- Rights and consent: image/voice/script are authorized; no prohibited personal or sensitive information is present.
- Technical: file downloaded locally, duration matches expectation, resolution/aspect ratio correct, audio not clipped, no missing audio channel.
- Lip sync: mouth closures align with plosives, vowels are not consistently early/late, there are no long frozen-mouth segments while speech continues.
- Performance: expression matches tone, gestures are not uncanny or distracting, eye-line is acceptable, head motion does not contradict the script.
- Character continuity: face identity, hair, glasses, clothing, skin tone, and background remain stable enough for the use case.
- Edit readiness: start/end handles are clean, captions will not cover mouth, there is room for logo/CTA/safe areas.
- Compliance: synthetic/AI disclosure and impersonation consent meet the user's jurisdiction/platform/brand requirements.
- Artifact response: mark each issue as accept, crop/edit around, regenerate with changed input, or switch model/surface.

## Troubleshooting

If lips do not match audio:

- First inspect audio for noise, distortion, clipping, reverb, multiple voices, or extreme speed.
- Regenerate a 5-10 second segment with cleaned audio.
- Keep the same image and prompt while testing so the audio change is isolated.
- If TTS timing changed after a voice swap, regenerate video from the final voice asset.

If the face looks unnatural:

- Replace heavy-filtered, side-profile, shadowed, low-resolution, or open-mouth images.
- Crop to a cleaner portrait for Hedra Avatar.
- Reduce prompt demands for large gestures or emotion.

If gestures are too dramatic:

- Use Hedra Avatar for locked-camera delivery or explicitly request minimal movement.
- Split expressive lines into shorter clips and choose the calmest variant.

If the wrong person speaks:

- In Studio, redo speaker selection and ensure the indicator covers the target character.
- In API workflows, test with a single-character crop or validate any target/bounding-box field with a short proof.

If generation fails:

- Confirm image and audio are attached/uploaded and under documented file limits.
- Confirm API key, paid API access, available credits, supported model settings, and duration cap.
- Poll status and capture `error_message`. Do not spend credits on repeated identical retries.

If video is queued:

- Treat queue time as provider state. Communicate delay, poll at reasonable intervals, and avoid submitting duplicate long jobs unless the user approves the extra cost.

## Safety, rights, and custody

Before using a face, voice, or performance:

- Get explicit consent for living people and for voice clones. Store the consent note or source license with the project.
- Avoid creating a real person's likeness or voice in a way that could mislead viewers about origin, endorsement, or speech.
- Do not upload children's data, government IDs, health/financial details, or other sensitive personal data.
- For enterprise work, check whether the customer's agreement overrides default privacy terms.
- Add disclosure or watermarking when the distribution context requires it.
- Keep local copies of inputs, outputs, prompts, model IDs, generation IDs, timestamps, and download URLs. Cloud library state is not enough for reproducible production.

## Sources verified on 2026-07-10

- Hedra API guide, Generate an Avatar Video: https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video
- Hedra API reference, Generate Asset: https://www.hedra.com/docs/api-reference/public/generate-asset
- Hedra API reference, List Models: https://www.hedra.com/docs/api-reference/public/list-models
- Hedra API reference, Get Status: https://www.hedra.com/docs/api-reference/public/get-status
- Hedra API reference, Get Credits: https://www.hedra.com/docs/api-reference/public/get-credits
- Hedra developer guide, Generate Audio: https://www.hedra.com/docs/pages/developer/guides/generate-audio
- Hedra app guide, Create UGC Avatar Videos: https://www.hedra.com/docs/pages/app/content-creation/create-avatar-video
- Hedra app guide, Create Voice: https://www.hedra.com/docs/pages/app/content-creation/create-audio
- Hedra app guide, Avatar Speaker Selection: https://www.hedra.com/docs/pages/app/content-creation/speaker-selection
- Hedra app troubleshooting, File Specifications: https://www.hedra.com/docs/pages/app/troubleshooting/file-specifications
- Hedra app guide, Which Video Model Should I Use?: https://www.hedra.com/docs/pages/app/getting-started/video-models
- Hedra Live Avatar docs: https://www.hedra.com/docs/pages/developer/realtime-avatar/about and related setup/expert pages
- Hedra Acceptable Use Policy: https://www.hedra.com/acceptable-use
- Hedra Privacy Policy: https://www.hedra.com/privacy
- Hedra Biometric Data Privacy Policy: https://www.hedra.com/biometric-data-policy
