---
name: d-id-avatar-video
description: Use D-ID to plan, generate, stream, localize, and QA avatar/talking-head videos, including V2 Photo Avatar Talks, V3 Pro/Instant Avatar Clips, V4 Expressive Avatar Scenes, D-ID Agents, voices, consent, lifecycle, safety, and artifact custody.
---

# D-ID avatar video production

Use this skill when the selected provider is D-ID or when the user asks for a D-ID talking avatar, photo-to-speaking-video, presenter clip, expressive avatar, interactive visual agent, real-time avatar stream, or D-ID-powered localization/support/training workflow.

Do not treat D-ID as a general cinematic video generator. It is primarily for human-presenter video: a face or presenter speaks text or audio with lip sync. For scenes that need object interaction, product handling, full-body action choreography, multi-shot narrative motion, or cinematic camera movement, use a broader video-generation or composition pipeline and use D-ID only for the presenter segments.

Facts in this skill were verified against official D-ID documentation and policies on 2026-07-10. Re-check live docs before quoting prices, enabled models, supported languages, moderation categories, endpoint schemas, or plan limits in user-facing commitments.

## Choose the D-ID route before scripting

Pick the route from the deliverable, not from habit:

| Need | D-ID route | Use when | Avoid when |
|---|---|---|---|
| A specific still portrait speaks | V2 Photo Avatar / Talks API (`POST /talks`) | The user supplies or owns a clear face image; personalization matters more than body motion. | The face is low-resolution, side-facing, celebrity-like, or permission is uncertain. |
| A polished stock presenter speaks | V3 Pro Avatar / Clips API (`POST /clips`) | Marketing, learning, onboarding, support snippets, or brand explainers need Full-HD presenter footage and natural presenter movement. | The user needs a specific person's identity. |
| A reusable custom video avatar | V3 Instant Avatar or V4 Expressive Avatar creation | The subject can complete consent verification and the project needs many videos with one owned avatar. | There is no consent video or the source footage is poor. |
| Expressive emotion and next-generation avatar behavior | V4 Expressive Avatar / Scenes API (`POST /scenes`) | Sentiment/emotion, more human facial detail, expressive training/support/sales presenters, or V4 agents are required. | A simple one-off photo-to-video clip is enough. |
| Live conversation | D-ID Agents, Agents SDK, Streams API, Embed SDK | The output is a website/chat/support/training agent with real-time WebRTC/LiveKit avatar responses. | The deliverable is a finished MP4 only. |
| Bulk personalization | D-ID API jobs or Studio campaigns, depending on the user's tooling | Sales outreach, onboarding, L&D certificates, course feedback, or localized variants need many similar videos. | Each video needs bespoke editing or different visual design. |

Official docs describe D-ID video APIs as supporting avatar videos from images, text, and audio, with V4 Expressive Avatars, V3 Pro Avatars, V3 Instant Avatars, and V2 Photo Avatars as the main video families. The V2 Talks endpoint transforms a source photo into a speaking avatar; the V3 Clips endpoint uses presenter avatars and optional drivers; V4 Scenes use created avatars. Source: [D-ID Quickstart](https://docs.d-id.com/docs/quickstart), [Create a talk](https://docs.d-id.com/reference/createtalk), [Create a clip](https://docs.d-id.com/reference/createclip), [Create a Scene](https://docs.d-id.com/reference/create-scene), verified 2026-07-10.

## Production preflight

Before any paid or irreversible generation:

1. Confirm the D-ID API key and credits. D-ID's FAQ says API keys are generated in Studio and valid credits are required; the API includes `GET /credits` for remaining and total credit items. Verified 2026-07-10.
2. Confirm commercial rights and plan constraints. Trial/guest outputs may be watermarked or limited to non-commercial use under D-ID terms; paid plans affect watermarking, usage, and credits. Do not promise commercial use until the user's plan allows it.
3. Confirm the person/likeness rights. For any real person, get explicit permission to use their image, voice, and likeness for the intended output, audience, and duration.
4. Confirm whether the input may contain personal data. D-ID's privacy policy says photos, text, audio, video, voice cloning data, and account data may be processed; minimize unnecessary personal data.
5. Choose text-to-speech vs external audio:
   - Use text scripts for rapid iteration, localization, and simpler custody.
   - Use audio scripts when exact timing, a pre-approved voiceover, a human recording, or an external TTS voice must be preserved.
6. Decide custody: where input files live, where D-ID should write results if using `result_url`, where webhooks land, and where final MP4s and metadata will be stored after download.
7. Build a QA checklist before generation so the team knows what "good" means: identity permission, facial fit, lip sync, pronunciation, captions, safe content, brand tone, resolution, watermarks/synthetic marks, and final file custody.

## Input preparation

### Source image for V2 Photo Avatar / Talks

Use a front-facing, well-lit image with one clearly visible face. Crop for a stable head-and-shoulders composition with room around the chin and hair. Avoid extreme side angles, heavy occlusion, sunglasses, open mouths, busy foreground objects, and images that imply a real person without permission.

Production heuristics:

- Keep face detail high enough for close-up delivery. Upscale or choose another photo instead of hoping D-ID will repair a tiny face.
- Preserve natural skin texture; aggressive beautification can create uncanny lip/cheek motion.
- Prefer a neutral or slight-smile expression for business, support, education, and localization. Strong source emotions reduce believable range.
- Use consistent lighting and color if the avatar will be composited with slides or brand graphics.
- If the user asks to animate a celebrity, public figure, employee, customer, child, or private individual, pause until rights and policy fit are explicit.

### Presenter selection for V3 Pro / Clips

Use `GET /clips/presenters` to list supported V3 Pro Avatars and their `presenter_id` values. D-ID's docs also note that V3 Pro Avatars are used with `/clips` and that custom V3 Pro Avatars based on the user's own video footage require contacting D-ID. Verified 2026-07-10.

Choose a presenter by:

- audience trust fit: executive, educator, peer, support specialist, sales advisor;
- wardrobe/background fit: neutral office, green screen, home, outdoor, branded-safe;
- framing and gesture style: hands visible vs no-hands, energetic vs calm;
- localization continuity: one presenter per language family unless a localized face/persona is intentional.

Do not claim that the presenter can hold products, point to arbitrary UI elements, walk around a set, or interact physically with props unless that capability is explicitly available in the chosen D-ID presenter/driver workflow.

### Custom avatar and consent footage

For V3 Instant Avatars, D-ID docs state that a consent verification process is required before unlimited videos can be generated with that avatar. For Express Avatars, `POST /scenes/avatars` accepts a `source_url` for the source video and a `consent_id` for a valid consent video; `POST /consents` creates a consent flow for supported languages. Verified 2026-07-10.

Capture custom avatar source footage as if it were a miniature talent shoot:

- one person only, stable camera, eye-level framing, even light, clean background;
- no copyrighted music or third-party voices in the source;
- natural speaking pace and a few seconds of neutral face;
- wardrobe and background that can be reused across future videos;
- separate consent capture in the required language, tied to the intended person and account.

If consent fails or is missing, do not work around it with a still photo, lookalike, or cloned voice. Ask for valid consent or switch to a stock presenter.

## Script, voice, and language direction

D-ID can animate from text or audio scripts in relevant endpoints; `/tts/voices` lists voices and can be filtered by provider: Amazon, Microsoft, Azure OpenAI, ElevenLabs, or Google. Some endpoints include an `x-api-key-external` header for bringing an external ElevenLabs API key for IVC voices. Verified 2026-07-10.

Write for lip sync and trust:

- Use concise spoken sentences. A D-ID presenter is strongest when the face supports the message, not when it races through dense text.
- Keep one clear idea per sentence. Avatar videos punish long clauses because eye contact and facial motion make rambling feel artificial.
- Spell out uncommon pronunciations, acronyms, names, medicine/legal terms, and brand words.
- Add explicit pause strategy in the text or external audio. Use punctuation, SSML-like pauses if supported by the selected script/voice path, or pre-rendered audio with clean silences.
- Localize meaning, not just words. Adjust greeting, idioms, gesture expectations, and trust cues for the target culture.
- Match emotion to route. V4 expressive/sentiment paths can justify more emotional writing; V2 photo avatars should use restrained affect.

Prefer pre-rendered audio when:

- the user has a legally cleared human voiceover;
- the brand voice is already approved;
- pronunciation must be exact;
- another TTS provider is preferred;
- you need one master audio track reused across D-ID and non-D-ID edits.

When using audio upload, D-ID's `POST /audios` stores an uploaded audio/video input temporarily, converts the result to WAV at 16 kHz, supports `audio/` and `video/` MIME types, limits the file to 6 MB, and stores it for 24-48 hours unless routed differently by the endpoint parameters. Verified 2026-07-10. Download and preserve any source audio and generated result in your own project storage; do not rely on temporary upload URLs as the only copy.

## API lifecycle pattern

Use D-ID's async job model deliberately:

1. Create or select the avatar/presenter:
   - Talks: provide `source_url`.
   - Clips: provide `presenter_id` and optionally `driver_id`.
   - Scenes: create/select `avatar_id`; Express Avatar creation uses `POST /scenes/avatars`.
2. Provide the `script` as text or audio, with voice/provider configuration appropriate to the endpoint.
3. Add `name` and non-sensitive `user_data` for traceability. Never put secrets, private user data, or raw customer PII in `user_data`; D-ID docs describe it as echoed into responses and webhooks.
4. Prefer a webhook for production automation. If no webhook is configured, poll the matching `GET` endpoint (`/talks/{id}`, `/clips/{id}`, or scenes equivalent) until completion.
5. If using `result_url`, use a controlled HTTPS destination or presigned URL with the right permissions. Otherwise, download the returned video URL promptly into the project's asset store.
6. Store the request payload minus secrets, job id, endpoint, D-ID route, voice/provider, avatar/presenter id, consent id if applicable, source asset hashes, result URL, local final path, created/finished timestamps, cost/credit note, and QA result.

Common endpoint facts, verified 2026-07-10:

- `POST /talks` creates a V2 talking avatar video from a source image/studio actor plus a required text or audio script; it accepts `config`, `user_data`, `name`, `webhook`, and `result_url`; failures may include auth, insufficient credits, permission, and moderation errors.
- `POST /clips` creates a V3 presenter clip with `presenter_id`, optional `driver_id`, required text/audio script, `config`, `presenter_config`, `background`, `user_data`, `name`, `webhook`, and `result_url`; failures may include auth, credits, permissions, and image/text/audio moderation.
- `POST /scenes/avatars` creates an Express Avatar from a source video, optional valid `consent_id`, optional green-screen flag, `webhook`, `name`, and `user_data`.
- `POST /scenes` creates a scene using an `avatar_id` and required text/audio script; background color is only for avatars with green screen background.
- `GET /tts/voices` lists/filter voices by provider.
- `GET /credits` returns credit items with remaining/total credits and expiration.

## Realtime Agents and streaming

Use Agents when the user needs an interactive face, not a static MP4. D-ID docs describe Agents as autonomous AI assistants that answer from owner-uploaded knowledge and perform roles for business or individual use cases; common roles include marketing, customer engagement, education, and training. Verified 2026-07-10.

Agent production is a product design task, not just avatar generation:

- Define the agent's job, refusal boundaries, handoff rules, and user value.
- Choose presenter/avatar type from Photo Avatar, Video Avatar, or Expressive Avatar; D-ID's Agents API requires a presenter object when creating an agent.
- Choose LLM path: D-ID-managed built-in models, external OpenAI/Azure keys through Studio where available, or a custom OpenAI-compatible endpoint. D-ID docs state built-in options include several OpenAI model names as of 2026-07-10; re-check before committing exact names.
- Attach knowledge only after cleaning source docs for privacy, outdated claims, and unsupported advice.
- Provide starter messages and greetings that set expectations clearly.
- Enable embed/SDK only for approved domains. D-ID's SDK docs describe domain allowlisting and client key use as part of embed setup.
- Test latency, interruption behavior, microphone permissions, browser compatibility, fallback chat-only state, and logged conversation export/custody.

D-ID's Agents SDK supports Talks (V2) and Clips (V3) via WebRTC streaming, and Expressives (V4) via LiveKit-based streaming with microphone input and always-on fluent mode. The SDK is front-end oriented; Agent and Knowledge creation should be handled through the Agents API or Studio. Verified 2026-07-10.

## Safety, rights, and privacy gates

Pause and resolve before generation when any of these are true:

- The source face or voice is a real person and permission is absent, ambiguous, or narrower than the requested use.
- The subject is a child, employee, customer, patient, student, political figure, celebrity, public official, or otherwise sensitive identity.
- The script impersonates, deceives, fabricates endorsement, gives high-stakes advice, or hides that it is synthetic where disclosure is required.
- The source image/audio includes third-party IP, private locations, confidential documents, health/financial/legal data, or biometric data unnecessary for the output.
- The user asks to remove/hide D-ID synthetic marks, watermarks, or disclosures. D-ID terms restrict removing, hiding, or minimizing synthetic marks/watermarks without prior written approval. Verified 2026-07-10.
- The output will be used for ads, regulated industries, political persuasion, hiring, education assessment, medicine, finance, legal services, or public-service announcements without additional review.

User-facing disclosure should be plain: "This video uses an AI-generated avatar/lip-sync produced with D-ID." Keep the disclosure in metadata, captions, page copy, or intro/outro as appropriate to the distribution channel and applicable law.

## QA pass for finished D-ID avatar video

Review the final MP4 at normal speed, half speed for lip sync, and in the target layout/platform crop.

Must-pass checks:

- Consent and rights are documented for face, voice, script, music, and distribution.
- The avatar's identity is not misleading and does not imply an unapproved endorsement.
- Lip sync is believable on plosives, names, numbers, and non-English words.
- Audio is clean, normalized, and free from clipped consonants or awkward pauses.
- Eyes, teeth, jawline, cheeks, and hands do not exhibit distracting artifacts.
- The first frame, last frame, and poster frame are brand-safe.
- Captions/subtitles match spoken words and are readable in the final aspect ratio.
- No unapproved watermark/synthetic-mark removal occurred.
- Result URL has been downloaded to owned storage; temporary upload and result links are not the only copies.
- The job metadata is sufficient to reproduce or audit the generation.

Common failure modes and repairs:

- Weak lip sync on names: rewrite phonetically, switch voice, or use externally produced audio.
- Robotic delivery: shorten sentences, add pauses, choose a warmer voice, or switch to V4 expressive route.
- Uncanny still-photo motion: choose a more front-facing neutral image or switch to V3 presenter.
- Presenter mismatch: select a different V3 presenter/background/driver or use green-screen composition if supported.
- Moderation error: inspect whether the issue is image, text, audio, celebrity recognition, or rights-sensitive content; do not evade moderation.
- Credit or auth failure: check `GET /credits`, plan/API key status, endpoint permissions, and whether external TTS headers are configured correctly.
- Webhook not received: poll the job endpoint, verify HTTPS endpoint logs, and confirm no sensitive data is expected in `user_data`.

## Example: one-off personalized onboarding video from a supplied portrait

Intent: create a 35-second welcome video for a new customer using a portrait they provided and consented to use.

Route: V2 Photo Avatar / Talks, because the specific person's image matters and a simple head-and-shoulders delivery is enough.

Preflight:

- Confirm written permission to use the portrait for onboarding.
- Confirm D-ID credits and plan.
- Store source image in controlled HTTPS storage.
- Choose text script first for fast iteration; switch to audio only if pronunciation fails.

Example script:

> Hi Maya, welcome to Northstar Analytics. I'm glad you're here. In the next three minutes, we'll connect your dashboard, invite your team, and set your first weekly report. If anything feels unclear, use the help button in the lower right. Let's get you from setup to insight today.

Example API-shape plan:

```json
{
  "endpoint": "POST https://api.d-id.com/talks",
  "body": {
    "source_url": "https://your-controlled-storage.example/onboarding/maya-approved-headshot.jpg",
    "script": {
      "type": "text",
      "input": "Hi Maya, welcome to Northstar Analytics...",
      "provider": "microsoft",
      "voice_id": "choose-after-GET-/tts/voices"
    },
    "name": "maya-onboarding-welcome-v1",
    "user_data": "project=northstar-onboarding;variant=maya-v1",
    "webhook": "https://your-webhook.example/did/jobs",
    "result_url": "https://your-presigned-destination.example/maya-onboarding.mp4"
  }
}
```

Why this structure works: the still portrait is the differentiator, the script is short and direct, `user_data` is non-sensitive, and the webhook/result path supports custody.

Expected result: a close-up talking avatar MP4 suitable for an onboarding page.

Likely fixes: if "Northstar" is mispronounced, use a voice with better English business diction, phonetic spelling, or pre-rendered audio.

## Example: polished training presenter with stock avatar

Intent: create a 60-second compliance microlearning intro without using any real employee's likeness.

Route: V3 Pro Avatar / Clips, because a stock presenter avoids employee likeness risk and improves body/presenter movement over a single photo.

Preflight:

- Use `GET /clips/presenters` and pick a presenter with neutral wardrobe and background.
- Verify whether green-screen/background options are needed for downstream composition.
- Use external reviewed voiceover if legal phrasing must be exact.

Example script:

> Before you approve a vendor invoice, pause for three checks. First, confirm the purchase order matches the invoice amount. Second, verify the vendor name and payment details against the approved vendor record. Third, look for urgency language that pressures you to skip review. If any detail feels off, stop and route it to Finance Operations.

Example API-shape plan:

```json
{
  "endpoint": "POST https://api.d-id.com/clips",
  "body": {
    "presenter_id": "select-from-GET-/clips/presenters",
    "script": {
      "type": "text",
      "input": "Before you approve a vendor invoice...",
      "provider": "amazon",
      "voice_id": "choose-after-GET-/tts/voices"
    },
    "background": {
      "color": "#F6F7FB"
    },
    "name": "invoice-fraud-training-intro-v1",
    "user_data": "course=invoice-fraud;module=intro;version=1",
    "webhook": "https://your-webhook.example/did/jobs"
  }
}
```

Expected result: a professional presenter clip that can be placed before slides or interactive quiz content.

Likely fixes: if the presenter's gestures feel too energetic for compliance, choose a calmer presenter/driver or shorten the script to reduce overacting.

## Example: interactive support agent for a SaaS help center

Intent: deploy a visual agent that answers product setup questions on a documentation site.

Route: D-ID Agent with Embed or Agents SDK, not a pre-rendered clip.

Design:

- Presenter: Expressive Avatar if the brand wants more lifelike real-time interaction; otherwise use a simpler avatar for speed and lower complexity.
- LLM: D-ID built-in model for quick launch, or custom/external model when the company requires its own model routing and compliance review.
- Knowledge: approved help-center articles only; exclude internal tickets and customer data.
- Greeting: "Hi, I can help with setup and troubleshooting. I'm an AI support avatar, and I'll link to docs when useful."
- Boundaries: no billing changes, no legal/security promises, no account-specific diagnosis without authenticated support handoff.

QA:

- Test allowed-domain configuration.
- Test microphone permissions and text fallback.
- Ask five known FAQ questions and compare answers to source docs.
- Ask out-of-scope billing/legal/security questions and confirm safe handoff.
- Confirm chat logs and exports are stored according to the user's privacy policy.

Expected result: an embedded AI support avatar with voice/video/chat that can answer documentation-grounded questions and escalate safely.

## Sources

Primary sources used and verified 2026-07-10:

- [D-ID Quickstart](https://docs.d-id.com/docs/quickstart) for route families: Realtime, Agents, Talks, Clips, V4 Expressive Avatars, Video Translate, SDKs.
- [D-ID API Keys](https://docs.d-id.com/docs/api-keys) and [D-ID FAQ](https://www.d-id.com/faqs/) for Studio API key generation, credit requirements, and API documentation location.
- [Create a talk](https://docs.d-id.com/reference/createtalk), [Get a specific talk](https://docs.d-id.com/reference/gettalk), [Create a clip](https://docs.d-id.com/reference/createclip), [Get a specific clip](https://docs.d-id.com/reference/getclip), [Get presenters](https://docs.d-id.com/reference/getpresenters), [Create an Express Avatar](https://docs.d-id.com/reference/create-express-avatar), and [Create a Scene](https://docs.d-id.com/reference/create-scene) for endpoint behavior.
- [Upload audio file](https://docs.d-id.com/reference/upload-an-audio), [Get Voices](https://docs.d-id.com/reference/voices), and [Get credits](https://docs.d-id.com/reference/getcredits) for audio, TTS, and credit lifecycle.
- [Create a consent](https://docs.d-id.com/reference/create) and V3 Instant Avatar quickstart for consent flow requirements.
- [Agents SDK Overview](https://docs.d-id.com/reference/agents-sdk-overview), [Agents Embed Overview](https://docs.d-id.com/docs/embed-overview), [Create an Agent](https://docs.d-id.com/reference/createagent), [Create a video stream](https://docs.d-id.com/reference/createvideoagentstream), and [LLMs Overview](https://docs.d-id.com/docs/llms-overview) for realtime agent design.
- [D-ID Products Terms of Use](https://www.d-id.com/studio-end-user-license-agreement/) and [D-ID Privacy Policy](https://www.d-id.com/privacy-policy/) for rights, watermarks/synthetic marks, personal data, and privacy cautions.
