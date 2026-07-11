---
name: heygen-avatar-video
description: Produce HeyGen avatar videos with Direct Video, Video Agent, Digital Twin, Avatar Realtime, and related avatar/voice/asset APIs. Use for provider routing, avatar and voice selection, script-to-video workflows, lip-sync from audio, backgrounds/scenes, callbacks and polling, consent and rights checks, localization handoffs, artifact custody, QA, and troubleshooting HeyGen avatar-video productions.
---

# HeyGen avatar video production

Use this skill when the production path is HeyGen and the deliverable involves an AI presenter, digital twin, photo avatar, studio avatar, prompt-composed avatar clip, or real-time streaming avatar. Treat HeyGen as both a creative video tool and a likeness-handling system: lock consent, identity rights, script intent, voice rights, and output custody before generation.

Facts below were verified from official HeyGen documentation and policy pages on 2026-07-10. Recheck the linked docs for volatile fields such as prices, engine support, endpoint shapes, limits, status values, moderation policy, and plan entitlements before a paid run.

## Choose the right HeyGen route

Prefer the most controllable API that still fits the brief.

- Use Video Agent (`POST /v3/video-agents`) when the user wants a complete avatar video from a natural-language brief and accepts HeyGen choosing or composing the script, avatar, voice, and visual style. It is the fastest exploration path and supports one-shot generation or interactive chat-style iteration, but it gives less deterministic scene control.
- Use Direct Video (`POST /v3/videos`, `type: "avatar"`) when the script, avatar look, voice, aspect ratio, background, captions, watermark, output format, or motion prompt must be explicit and repeatable. This is the default for production pipelines, personalized campaigns, compliance-reviewed scripts, and brand-controlled spokesperson videos.
- Use Cinematic Avatar (`POST /v3/videos`, `type: "cinematic_avatar"`) only when the output is a short prompt-composed cinematic shot with 1-3 avatar looks and no spoken script. Do not choose it for normal talking-head narration.
- Use Avatar Realtime (`POST /v3/avatar-realtime`) when the user needs a live HLS stream of an avatar speaking in real time. It is for kiosks, live agents, assistants, and broadcasts where the application owns STT/LLM orchestration. It is not a rendered MP4 workflow.
- Use Video Translation or Lipsync APIs for post-hoc localization or replacing audio on existing footage rather than regenerating the whole video when the visual source must be preserved.

Official routing basis: HeyGen's "Choosing the Right Video API" docs distinguish Video Agent as prompt-driven/low-control, Direct Video as structured/high-control, and Cinematic Avatar as prompt + avatar looks with no spoken voice. Official Avatar Realtime docs describe the real-time HLS path as separate from rendered video.

## Preflight checklist

Before generating:

1. Confirm authentication path and billing pool.
   - Direct API and skills use `X-Api-Key` / `x-api-key` and bill against the API wallet.
   - OAuth-based MCP/agent usage can bill against the web-plan balance instead.
2. Decide the API route above and record why.
3. Inventory available avatar looks with `GET /v3/avatars/looks`; pass the look ID as `avatar_id`, not the avatar group ID.
4. Inventory voices with `GET /v3/voices`; filter by language, gender, type, and engine when needed. If using the TTS endpoint, HeyGen docs call out `engine=starfish` voices.
5. Verify consent state for any digital twin. Do not generate with a real person's likeness unless the subject's permission and HeyGen consent requirements are satisfied.
6. Estimate cost using output duration and selected feature. Pricing is volatile; verify current API or enterprise pricing immediately before batch or paid production.
7. Confirm resource limits and file accessibility:
   - URLs passed to the API must be publicly reachable and direct to the file.
   - Official docs list supported upload formats and size limits; for larger files, use the direct-upload flow.
8. Set lifecycle strategy: callback URL, polling cadence, failure handling, local artifact storage, and presigned URL download before expiry.
9. Define QA acceptance criteria before render: pronunciation, lip-sync, identity/likeness, gesture appropriateness, brand/background, captions, aspect ratio, and safety/moderation status.

## Avatar, look, and consent handling

HeyGen separates avatar groups from avatar looks. A group is a character identity; a look is the renderable outfit/pose/style. In video creation, `avatar_id` should be the look ID.

Digital twins depict real identifiable people and require explicit consent handling. HeyGen's consent docs state that digital twins require proof that the depicted person agreed to be cloned, while photo avatars and prompt avatars do not require the same digital-twin consent flow. Available consent levels, verified 2026-07-10:

- Level 1: hosted webcam consent page; available in v3.
- Level 2: uploaded pre-recorded consent video through the API; enterprise/whitelisted.
- Level 3: skipped consent flow for accounts with special enterprise arrangements; whitelisted.

Production rules:

- Stop if the user asks to impersonate, clone, or use a private person, employee, celebrity, public figure, or customer without explicit rights and consent.
- Ask for proof of rights when the avatar subject is identifiable and not the requester.
- Do not present a stock/avatar-library look as a real employee or real customer unless that is true and authorized.
- Keep an audit note containing avatar group/look ID, ownership (`private` or stock/library when known), consent status or consent URL/result where available, and approval source.
- If a digital twin was created but not yet consented, route through `POST /v3/avatars/{group_id}/consent` and wait for completion/approval before generation.

## Engine selection for Direct Video

For `POST /v3/videos` avatar renders, HeyGen v3 supports Avatar III, Avatar IV, and Avatar V engines. Verified 2026-07-10:

- Avatar IV (`avatar_iv`) is the default when the `engine` field is omitted. It is the safest default for ordinary Direct Video because it is broadly supported.
- Avatar V (`avatar_v`) is higher-fidelity and cross-reference-driven in HeyGen's docs/research, but official docs say to check the avatar look's `supported_api_engines` via `GET /v3/avatars/looks/{look_id}` before requesting it. Avatar V support is narrower and documented as Digital Twin-only in pricing/model docs.
- Avatar III (`avatar_iii`) is a dedicated photo-to-video pipeline in the current v3 docs. Do not confuse it with older legacy v1/v2 Avatar III endpoints.
- `motion_prompt` support depends on both avatar source and engine: official v3 docs list it for photo avatars on either supported engine and for video avatars only when `engine.type` is `avatar_v`; it is rejected for video avatars on the default Avatar IV engine. `expressiveness` is photo-avatar-only, Avatar IV-only, and rejected with Avatar V.

Heuristic: for a compliance-reviewed corporate or training presenter, use Avatar IV unless Avatar V is explicitly supported and the user values maximum likeness/motion fidelity or video-avatar gesture prompting enough to pay for it. For photo-avatar experimentation, check whether Avatar III or IV better matches the available look and cost constraints.

## Script and performance direction

Write for a human presenter, not for a voiceover pasted onto a face.

- Keep sentences short and breathable. Put one idea per sentence.
- Avoid dense acronyms and numbers unless the target audience needs them; write pronunciations into the script when needed.
- Add stage direction through fields HeyGen supports, not by stuffing bracketed acting notes into spoken text unless the field is specifically interpreted as direction.
- Use `motion_prompt` for visible behavior only when the selected avatar/engine combination supports it: posture, hand restraint, warmth, pointing/gesture level, eye-contact style, and energy. Keep it natural and non-choreographic.
- Use `voice_settings` for speed, pitch, volume, locale, and engine settings when the selected voice supports them.
- For localization, do not simply translate word-for-word. Re-time the script by target language, then choose a voice/locale and check lip-sync/caption fit.

Script shape for avatar video:

- Hook: first 3-5 seconds, direct and spoken to camera.
- Context: one sentence naming the viewer's problem.
- Value: 2-4 short beats; put lists in parallel grammar.
- Proof/demo: one concrete example or visual reference.
- CTA: a single action, no pile-up.

Avoid:

- Long clauses that make lips move continuously without a natural pause.
- Timestamps or editing notes in the spoken script.
- Claims the avatar subject would not be authorized to make.
- Unlicensed brand comparisons, medical/legal/financial certainty, or deceptive endorsement language.

## Direct Video request pattern

Use this pattern for controlled rendered videos:

```json
{
  "type": "avatar",
  "avatar_id": "LOOK_ID",
  "voice_id": "VOICE_ID",
  "script": "Hi, I'm Maya. In the next thirty seconds, I'll show you how Acme reduces invoice review from days to minutes.",
  "title": "Acme invoice review intro",
  "resolution": "1080p",
  "aspect_ratio": "16:9",
  "background": {
    "asset_id": "BACKGROUND_ASSET_ID"
  },
  "caption": {
    "file_format": "srt",
    "style": "default"
  },
  "engine": {
    "type": "avatar_iv"
  },
  "callback_url": "https://example.com/webhooks/heygen",
  "callback_id": "project-scene-001"
}
```

Production notes:

- Use `audio_url` or `audio_asset_id` instead of `script` + `voice_id` when the user supplies approved narration and wants lip-sync to that audio.
- Add `motion_prompt` only when the selected avatar look and engine support it; do not include it for video-avatar or digital-twin renders on default Avatar IV.
- Use `remove_background` or a transparent/background workflow only when the downstream compositor needs the avatar isolated; verify whether the selected endpoint/plan supports the desired output format.
- Keep `callback_id` meaningful and unique for custody; mirror it in your local manifest.
- If no callback is available, poll `GET /v3/videos/{video_id}` until terminal status.

## Video Agent prompt pattern

Use Video Agent when speed and creative automation beat exact control. The prompt should still specify business constraints; do not leave brand, audience, duration, or compliance-sensitive claims implicit.

Example prompt:

```text
Create a 45-second avatar-led onboarding video for a B2B SaaS feature launch.
Audience: finance operations managers.
Goal: explain that Acme Review flags duplicate invoices before payment.
Tone: calm, credible, lightly upbeat; no hype.
Structure: 5-second hook, one pain point, three product benefits, one concrete example, CTA to book a demo.
Visual style: clean enterprise software, soft blue/white palette, no exaggerated gestures.
Must say: "duplicate invoice checks run before the payment batch is approved."
Avoid: guarantees of fraud prevention, competitor claims, fake customer quotes, legal advice.
Output: 16:9, captions on.
```

If the user needs exact wording, do not rely on Video Agent's script writing for final output. Use it to explore concepts, then rebuild as Direct Video with the approved script and explicit assets.

## Avatar Realtime production pattern

Use Avatar Realtime for live spoken avatars, not MP4 delivery. Official docs describe three speech drivers: `tts`, `audio`, and `text_stream`; sessions are played from HLS.

For `text_stream`, plan the upstream system:

- STT if speech input exists.
- LLM or rules engine that produces short response chunks.
- Profanity/safety filter before appending text.
- Backpressure handling so the avatar does not receive long stale responses.
- Idle timeout handling; official docs list a 30-second default idle timeout for `text_stream`.
- Session cap and concurrency handling; official docs list a one-hour max session length and three concurrent sessions per space by default, with adjustable limits.

QA for realtime includes startup latency, interruption behavior, stream stability, HLS player compatibility, end_reason/error messages, and whether the avatar's spoken response remains aligned with the user's actual question.

## Backgrounds, scenes, captions, and brand

HeyGen Direct Video gives structured control over a single avatar render; do not assume it is a full editor unless the selected route supports scenes/templates. For multi-scene brand videos:

- Use Video Agent when it can compose scenes and style automatically.
- Use multiple Direct Video renders when each scene needs a different script segment, background, or framing, then assemble downstream.
- Upload custom backgrounds or visual assets with the Assets API and reference returned `asset_id`s.
- Use captions when the destination platform defaults to muted playback. Always review SRT timing and line breaks.
- Add watermarks only when required by brand/compliance; avoid crowding the avatar's face or lower-third captions.

Artifact custody:

- Save the request payload minus secrets.
- Save response IDs: `video_id`, `callback_id`, avatar look ID, voice ID, asset IDs, engine type, and title.
- Download completed `video_url` artifacts into the project storage immediately; presigned links are not durable custody.
- Store thumbnails, captions, generated audio, and final MP4 separately when available.
- Record moderation/rejection/failure messages verbatim in the production log.

## Polling, callbacks, failures

Rendered video generation is asynchronous. Official docs list video statuses including `pending`, `processing`, `completed`, and `failed`; completed responses include a `video_url`, and failed responses include failure details. Use callbacks for scale and polling for simple runs.

Failure triage:

- `401 Unauthorized`: API key missing, wrong header, inactive key, or wrong billing/auth path.
- `429 Too Many Requests`: rate/concurrency limit. Respect `Retry-After`; do not tight-loop.
- Download/resource failures: public URL not reachable, file extension does not match content, unsupported format, oversized asset, corrupted file, or authenticated URL.
- Validation error: wrong engine for avatar look, unsupported `motion_prompt` for the selected avatar/engine, unsupported `expressiveness` with Avatar V or a non-photo avatar, missing script/audio/voice field, invalid aspect ratio/resolution, or prompt/script too long.
- Moderation/pending/rejection: content or likeness review. Do not repeatedly resubmit evasive variants; revise to comply with policy or escalate for human review.
- Late render failure near completion: retrieve `failure_code`/`failure_message`, preserve the request, and test with a minimal script + same avatar/voice to isolate whether the issue is content, asset, engine, or account limit.

Retry policy:

- Safe retry: transient 429/5xx after backoff, callback delivery failure, or network timeout where no job ID was returned.
- Cautious retry: failed render with same payload after verifying it was not moderation or validation.
- Do not retry unchanged: rights/consent failure, moderation rejection, unsupported engine, or inaccessible asset URL.

## Safety, policy, and truthful disclosure

HeyGen's current official pages require users to comply with its Terms and Acceptable Use/Moderation Policy and emphasize consent for custom avatars/digital twins. Build your own production gate:

- Require explicit permission for identifiable likeness and voice use.
- Avoid deceptive impersonation, fake endorsements, fake news/interviews, or undisclosed synthetic representation where disclosure is required or contextually expected.
- Keep content within HeyGen moderation boundaries and applicable law.
- Add a disclosure such as "AI-generated presenter" when the audience could reasonably believe the person is a real employee/customer/official and that would matter to their decision.
- Do not use cloned voices or avatars for sensitive persuasion, fraud, harassment, sexual content, child-safety violations, political deception, or medical/legal/financial advice presented as a real professional's statement.
- Preserve consent evidence and takedown/removal requests as production-critical records.

## QA review rubric

Review the downloaded video before delivery:

- Identity and rights: correct authorized avatar; no accidental misrepresentation.
- Script accuracy: exact approved claims; no hallucinated claims from Video Agent.
- Voice: correct language/locale, pronunciation, pacing, emotional fit, no clipped words.
- Lip-sync: syllable timing, mouth closure, plosives, no drift on long sentences.
- Motion: gestures fit the script; no uncanny hand/face artifacts; eye contact feels natural.
- Visuals: aspect ratio, framing, safe margins, background, brand colors, watermark, and captions.
- Accessibility: captions readable, not obscured; audio levels stable; no critical meaning only in visuals.
- Platform fit: duration, format, and first-frame/hook match destination.
- Custody: final MP4, captions, thumbnail, request/response manifest, and source asset IDs are saved.
- Compliance: consent, disclosure, moderation status, and approval notes are recorded.

## Complete example: controlled product-launch spokesperson

Intent: produce a deterministic 30-second product-launch video with an approved company presenter look.

Approach:

1. Confirm presenter consent and ownership for the private digital-twin look.
2. List avatar looks and voices; choose the approved look and brand voice.
3. Check `GET /v3/avatars/looks/{look_id}` for supported engines; use Avatar IV if Avatar V is not listed.
4. Upload the approved office background to Assets API if it is not already public and stable.
5. Generate via Direct Video with callback and captions.
6. Download and QA the final MP4.

Example payload:

```json
{
  "type": "avatar",
  "avatar_id": "maya_launch_look_01",
  "voice_id": "en_us_brand_voice_02",
  "script": "Today we're launching Acme Review. It checks every invoice before the payment batch is approved, flags likely duplicates, and gives your team a clear review queue. If you already use Acme Pay, you can turn it on from settings today.",
  "title": "Acme Review launch - approved spokesperson",
  "resolution": "1080p",
  "aspect_ratio": "16:9",
  "background": { "asset_id": "asset_office_soft_blue" },
  "caption": { "file_format": "srt", "style": "default" },
  "engine": { "type": "avatar_iv" },
  "callback_url": "https://video.example.com/hooks/heygen",
  "callback_id": "acme-review-launch-v1"
}
```

Why this works: the approved script avoids unverifiable guarantees, Avatar IV is a broad default for a controlled spokesperson render, the callback ID supports custody, and Direct Video preserves exact wording. If the approved digital-twin look supports Avatar V and gesture prompting is important, switch the engine after verifying support and then add a restrained `motion_prompt`.

Likely failure modes: unsupported private look, pending digital-twin consent, pronunciation of product names, captions colliding with lower thirds, or moderation review if claims imply fraud detection guarantees.

## Complete example: localized training module

Intent: convert an English HR training presenter into Spanish and French variants while preserving the approved visual identity.

Approach:

1. Treat each language as a new script adaptation, not a literal translation.
2. Keep the same avatar look only if rights cover localized use.
3. Select voices by target locale and review pronunciation for names, policy terms, and acronyms.
4. Generate one Direct Video per language using locale-appropriate script and voice settings.
5. QA native-language timing, lip-sync, captions, and policy wording.

Example Spanish script segment:

```text
Hola. En este modulo repasaremos como reportar un conflicto de intereses antes de aprobar una compra. Si tienes dudas, pausa el video y consulta la politica interna en el portal de cumplimiento.
```

Example payload differences:

```json
{
  "voice_id": "es_es_training_voice_01",
  "voice_settings": {
    "speed": 0.95,
    "pitch": 0,
    "volume": 1,
    "locale": "es-ES"
  },
  "caption": {
    "file_format": "srt",
    "style": "default"
  }
}
```

Why this works: the slightly slower speed gives captions and lip-sync more room, while separate scripts preserve compliance language in each market.

Likely failure modes: too-long translated sentences, formal/informal pronoun mismatch, cloned voice not licensed for all regions, and text overflow in captions.

## Complete example: live concierge avatar

Intent: place an avatar face on a live support assistant in a kiosk.

Approach:

1. Use Avatar Realtime, not rendered Direct Video.
2. Select a stock or authorized avatar look and an appropriate voice.
3. Open a `text_stream` session.
4. Poll until the HLS URL is live.
5. Stream short answer chunks after the application's own STT, LLM, retrieval, and safety checks.
6. Cancel/close sessions on idle or kiosk reset.

Example initial request:

```json
{
  "type": "text_stream",
  "avatar_id": "concierge_stock_look_07",
  "voice_id": "en_us_warm_support_03",
  "text": "Hi, I'm here to help. What can I find for you today?"
}
```

Example text append:

```json
{
  "text": "The returns desk is on level two, near the west elevators."
}
```

Why this works: Avatar Realtime only handles the talking face and voice stream; the application remains responsible for retrieval accuracy, safety filtering, and conversation state.

Likely failure modes: idle timeout, too many concurrent sessions, HLS playback issues on the kiosk browser, long LLM responses queued after the user changes topics, or the avatar appearing to make commitments the system cannot fulfill.

## Official and authoritative sources

- HeyGen API Quick Start: https://developers.heygen.com/docs/quick-start
- HeyGen API Key guide: https://developers.heygen.com/docs/api-key
- HeyGen Choosing the Right Video API: https://developers.heygen.com/docs/choosing-the-right-video-api
- HeyGen Create Video reference: https://developers.heygen.com/reference/create-video
- HeyGen Get Video reference: https://developers.heygen.com/reference/get-video
- HeyGen Digital Twin guide: https://developers.heygen.com/generate-avatar-video
- HeyGen Avatar Realtime guide: https://developers.heygen.com/avatar-realtime
- HeyGen Avatar Consent guide: https://developers.heygen.com/docs/avatar-consent
- HeyGen Create Avatar guide: https://developers.heygen.com/docs/create-avatar
- HeyGen Avatar Looks reference: https://developers.heygen.com/reference/list-avatar-looks
- HeyGen Voices reference: https://developers.heygen.com/reference/list-voices
- HeyGen Upload Assets guide: https://developers.heygen.com/docs/upload-assets
- HeyGen Self-Serve Pricing and limits: https://developers.heygen.com/docs/pricing
- HeyGen Enterprise Pricing and limits: https://developers.heygen.com/docs/enterprise-pricing
- HeyGen Changelog: https://developers.heygen.com/changelog
- HeyGen Moderation Policy: https://www.heygen.com/moderation-policy
- HeyGen Terms: https://www.heygen.com/terms
- HeyGen Privacy Policy: https://www.heygen.com/privacy
- HeyGen Avatar V research page: https://www.heygen.com/research/avatar-v-model
