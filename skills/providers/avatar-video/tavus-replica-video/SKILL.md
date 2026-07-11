---
name: tavus-replica-video
description: Use for producing Tavus AI-human videos and real-time avatar conversations with Tavus Faces/Replicas, PALs/Personas, async Video Generation, CVI conversations, consent-safe likeness workflows, webhooks, backgrounds, localization, and avatar QA.
---

# Tavus replica video production

Use this skill when a task involves Tavus avatars, replicas, faces, PALs/personas, generated talking-head files, real-time conversational video agents, or Tavus-powered lip-synced presenter output.

Documented facts in this skill were checked against official Tavus docs, policies, and pricing on 2026-07-10. Treat API names, model names, plan limits, stock replica availability, language support, pricing, and policy wording as volatile; verify them again before committing spend, launch scope, or regulated workflows.

## The current Tavus object model

Tavus docs now use:

- **Face**: the on-screen likeness and voice rendered by Phoenix. A custom face can be trained from a video URL or image URL. Stock faces/replicas can also be used.
- **PAL**: behavior, knowledge, pipeline, LLM/TTS/perception/turn-taking/conferencing configuration for real-time CVI.
- **Conversation**: a real-time video call/session with a PAL and face.

Legacy terms still appear in APIs and production requests:

- `replica_id` in the Video Generation API is the Face ID returned by `/v2/faces`.
- `/v2/personas`, `persona_id`, `/v2/replicas`, `default_replica_id`, and related aliases may still exist for backward compatibility.

Do not force the user to rename their mental model. Translate cleanly: "your Tavus replica ID is the face ID needed by the video endpoint."

## Choose the Tavus path first

Pick the path by deliverable, not by habit.

1. **One-way talking-head file**: use async Video Generation. Call `POST /v2/videos` with `replica_id` plus either `script` or `audio_url`; poll `GET /v2/videos/{video_id}` until `ready`, then capture `download_url`, `stream_url`, and `hosted_url`.
2. **Interactive AI human / live agent**: use CVI. Create or select a Face, create or select a PAL, then call `POST /v2/conversations` with `face_id` and `pal_id`.
3. **Need a new likeness**: create/train the Face first with `POST /v2/faces`. Use video training for highest fidelity and customer-facing work; use image training when speed/setup simplicity matters more than personalized expressions.
4. **Need exact audio, approved voiceover, or non-Tavus TTS**: use the async Video API with `audio_url` rather than `script`, or use CVI echo mode when the app supplies utterances in real time.
5. **Need an existing speaker video re-lip-synced**: Tavus Terms define LipSync as a platform feature, but do not assume an endpoint or schema from memory. Check the current OpenAPI contract before promising this path. If no documented endpoint is available, route through async avatar generation with `audio_url` or choose another documented lip-sync provider.

## Consent and rights are a hard gate

Before any custom face, likeness, voice, or biometric material is uploaded, require evidence that the depicted person has granted explicit, informed consent for:

- creating the face/replica;
- using the training media;
- generating the specific scripts, languages, contexts, and distribution channels;
- retaining, backing up, and reusing generated outputs;
- revocation handling.

Reject or pause when consent is absent, ambiguous, expired, or outside scope. Do not create replicas of real people, public figures, employees, customers, minors, or private individuals without explicit consent. Do not use Tavus stock replicas in ways that imply the actor personally endorses opinions, conditions, identity attributes, political positions, fundraising, news, or sensitive current-event claims unless Tavus has provided the required permission. Clearly disclose to end users when they are interacting with AI-generated content or an AI-powered agent.

Tavus policy and privacy notes to carry into production:

- Tavus requires necessary rights, licenses, consents, and permissions for uploaded likeness, voice, and content.
- The Acceptable Use Policy requires explicit informed consent for Customer Replicas and prohibits replicas depicting or appearing to depict minors.
- Tavus says some submitted audio/video samples may include biometric data such as voiceprints and facial geometry.
- The customer is responsible for generated media use, backups, API keys, and consequences of distribution.

## Face creation and training workflow

Use Face creation when the user needs their own presenter, a branded character, or a consented person rather than a stock face.

### Video-to-face

Documented facts, verified 2026-07-10:

- API: `POST https://tavusapi.com/v2/faces`
- Body field: `train_video_url`
- Do not send `train_image_url` in the same request.
- Training video URLs must be publicly reachable direct-download links, such as presigned S3 URLs.
- Tavus recommends keeping submitted asset URLs valid for at least 24 hours after submission.
- Default face model in docs is `phoenix-4`; `phoenix-3` can be requested with `model_name` when needed.
- The Video-to-Face guide says training usually takes 3-4 hours and can report by polling or callback.
- Troubleshooting docs state upload media must be H.264, and file-size errors indicate a 750 MB training video or audio file limit.
- Face training error docs list common failures: private/bad download URL, file too large, non-MP4, non-H.264, too short, too low FPS, multiple faces, or obstructions.

Production heuristic:

- Prefer video training for customer-facing, executive, sales, education, support, or any output where likeness fidelity matters.
- Record/choose a clean head-and-shoulders training video: one consenting adult, visible face, stable lighting, minimal shadows, no occlusions, no other faces, neutral background, clear voice, no music.
- Keep source footage and consent documents out of public buckets after training. Use expiring signed URLs and record expiration times in the production ledger.

Example API skeleton:

```json
{
  "face_name": "consented-founder-presenter",
  "train_video_url": "https://example-bucket.s3.amazonaws.com/founder-training.mp4?...",
  "callback_url": "https://example.com/tavus/webhook",
  "model_name": "phoenix-4"
}
```

### Image-to-face

Documented facts, verified 2026-07-10:

- API: `POST /v2/faces`
- Body field: `train_image_url`
- `voice_name` is required when `train_image_url` is used.
- Do not send `train_video_url` in the same request.
- Tavus documents an `auto_fix_training_image` option for image-based training.

Production heuristic:

- Use image training for prototypes, synthetic/non-human brand characters, internal mockups, or when the user lacks webcam capture.
- Expect more generalized facial expression behavior than video training.
- Confirm the selected `voice_name` is available with Tavus's current voice list and is approved for the character/persona.

## Async Video Generation

Use async Video Generation when the desired artifact is a finished video file for sharing, embedding, ads, outbound sales, enablement, product support, or localization variants.

Documented facts, verified 2026-07-10:

- API: `POST https://tavusapi.com/v2/videos`
- Required body: `replica_id` and either `script` or `audio_url`.
- `replica_id` is the Face ID, even though the endpoint still uses the legacy field name.
- Optional: `video_name`, `callback_url`, `background_url`, `background_source_url`, `fast`, `transparent_background`, `watermark_image_url`, and `properties`.
- `background_url` records a public website as the background.
- `background_source_url` uses a public downloadable video as the background.
- Without a background field, the output is full-screen face only.
- `transparent_background: true` only works with `fast: true` and produces `.webm`.
- `fast: true` uses a faster barebones rendering process and disables some features such as background generation, thumbnail images, and streaming URLs.
- Status values for `GET /v2/videos/{video_id}` include `queued`, `generating`, `ready`, `deleted`, and `error`.

API skeleton from text:

```json
{
  "replica_id": "r90bbd427f71",
  "script": "Hi Maya, I reviewed your onboarding workflow and saw three places where we can remove manual follow-up...",
  "video_name": "maya-onboarding-followup",
  "background_url": "https://example.com/product",
  "callback_url": "https://example.com/tavus/video-webhook"
}
```

API skeleton from approved audio:

```json
{
  "replica_id": "r90bbd427f71",
  "audio_url": "https://example-bucket.s3.amazonaws.com/approved-es-mx-voiceover.wav?...",
  "video_name": "support-intro-es-mx",
  "background_source_url": "https://example-bucket.s3.amazonaws.com/product-loop.mp4?..."
}
```

### Script writing for Tavus generated audio

These are production heuristics, not Tavus API requirements.

- Write exactly what should be spoken. Avoid bracketed stage directions unless you want the model to speak them.
- Favor short sentences, clean punctuation, and conversational phrasing. Avatar video exposes stiff copy immediately.
- Put unfamiliar names, acronyms, and product terms into phonetic or plain-language form when exact pronunciation matters, or use an externally approved audio track.
- Keep personalized outbound scripts brief and specific: one reason for relevance, one value claim, one call to action.
- For training/support, use "show, then say": pair a short spoken line with a website or product-loop background rather than overloading the presenter.
- For emotional tone, write it into the words, not as hidden direction. "I'm sorry that happened - let's fix it together" works better than "[empathetic]."
- For localization, do not simply translate. Re-time the script for spoken cadence, localize idioms, review pronunciation, and regenerate from approved localized audio when brand voice matters.

## CVI / PAL conversations

Use CVI when the avatar must listen, see, respond, remember, coach, support, interview, qualify, or interact in a live room.

Documented facts, verified 2026-07-10:

- API: `POST /v2/pals` creates a PAL that configures CVI behavior.
- `default_face_id` is required on `POST /v2/pals`.
- `system_prompt` is required unless using echo mode.
- PAL `pipeline_mode` can be `full` or `echo`.
- `full` provides the default end-to-end experience.
- `echo` turns off most steps and lets the PAL sync video with audio/text passed through Echo events.
- PAL layers can configure perception, STT, conversational flow, LLM, TTS, and conferencing.
- `POST /v2/conversations` starts a real-time video conversation with `face_id` and `pal_id`.
- Conversation requests can include `callback_url`, `conversation_name`, `conversational_context`, `custom_greeting`, `memory_stores`, `document_ids`, `document_tags`, `document_retrieval_strategy`, `test_mode`, `meeting_url`, `require_auth`, and `max_participants`.
- `test_mode: true` creates the conversation without the PAL joining and avoids affecting concurrency limits, according to Tavus docs.

Production heuristics for PAL authoring:

- Separate identity from behavior. The Face provides presence; the PAL prompt defines role, boundaries, tone, objective, and escalation behavior.
- Write the PAL prompt like a live agent playbook: role, job-to-be-done, audience, allowed claims, refusal/escalation rules, data handling, conversation success criteria, and closing behavior.
- Use knowledge documents for factual product/company material instead of putting every fact into the system prompt.
- Use guardrails and objectives when the PAL is deployed to users, not only a prompt.
- Use echo mode for custom app orchestration, external ASR/LLM/TTS, deterministic scripts, or workflows where Tavus should render speech rather than decide it.
- Use `require_auth` and meeting tokens for private rooms.
- For Google Meet or third-party conferencing, verify the current conferencing layer requirements and credentials before promising deployment.

Example PAL planning payload:

```json
{
  "pal_name": "returns-support-pal",
  "pipeline_mode": "full",
  "default_face_id": "r90bbd427f71",
  "system_prompt": "You are a calm retail returns specialist. Help customers understand return eligibility, collect only the minimum needed order context, never promise refunds outside policy, and escalate billing disputes to a human agent.",
  "document_tags": ["returns_policy", "shipping_policy"],
  "guardrail_tags": ["customer_support_safety"]
}
```

Example conversation payload:

```json
{
  "face_id": "r90bbd427f71",
  "pal_id": "pcb7a34da5fe",
  "conversation_name": "returns-support-demo",
  "custom_greeting": "Hi, I can help you check return options. What did you order?",
  "callback_url": "https://example.com/tavus/conversation-webhook",
  "require_auth": true,
  "max_participants": 2
}
```

## Webhooks, lifecycle, and custody

Always design a lifecycle plan before running production jobs.

For async videos:

- Save request payload, `video_id`, `video_name`, `replica_id`/Face ID, script or audio URL, background URL, created/updated timestamps, status, progress, `download_url`, `hosted_url`, `stream_url`, status details, and callback payloads.
- Poll with backoff or consume `callback_url` events. Do not block forever on `generating`.
- When `status` is `ready`, download and archive the file under the project's asset custody rules; Tavus-hosted links are convenient delivery links, not your only archive.
- When `status` is `error`, capture `status_details`, classify as auth, invalid ID, inaccessible URL, media format, provider error, policy/safety, or transient backend failure before retrying.

For face training:

- Save consent artifact references, source media inventory, signed URL expiry, `face_id`, `face_name`, model name, training path, callback payloads, and final status.
- Keep face IDs secret enough to prevent unauthorized use within your app. Treat API keys as secrets.

For CVI:

- Save PAL ID, Face ID, PAL prompt/version, knowledge document IDs/tags, guardrails/objectives, conversation IDs, conversation URLs, meeting tokens, callbacks, transcripts, recordings, and deletion/retention decisions.
- Decide whether conversation recordings/transcripts are permitted by user consent and the deployment jurisdiction.

## QA checklist

Run QA on both the media and the governance record.

### Identity and consent

- Correct consenting person or approved stock face.
- Consent scope covers script, language, use case, audience, distribution, retention, and revocation.
- No minors or unapproved public figures.
- AI disclosure is present where users/viewers interact with or may rely on the avatar.

### Performance and voice

- Name, company, product terms, and acronyms are pronounced correctly.
- Lip sync is acceptable throughout; inspect plosives, fricatives, pauses, and non-English phrases.
- Facial motion does not look frozen, over-expressive, or emotionally mismatched.
- Audio is clean, not clipped, and suitable for the platform.
- Script sounds like a person speaking, not a paragraph being read.

### Framing, background, and delivery

- Face framing, wardrobe, and background fit brand and channel.
- Website backgrounds load publicly and scroll as intended.
- Transparent `.webm` was requested only with `fast: true`.
- Captions, subtitles, and accessibility assets are present when needed.
- Final file is downloaded, named, checksummed when appropriate, and stored locally.

### CVI-specific QA

- PAL joins reliably in the intended environment.
- Greeting, turn-taking, interruptibility, latency, background-noise behavior, and escalation all match the experience promise.
- Knowledge retrieval gives accurate answers and does not hallucinate policy.
- Guardrails fire safely for disallowed requests.
- Private rooms require authentication when promised.
- Webhook receiver handles `event_type`, `message_type`, retries, duplicate events, and missing optional fields.

## Common failure modes and fixes

- **Invalid access token**: check API key, environment, and header name `x-api-key`.
- **Invalid `replica_id` / `face_id`**: confirm whether the endpoint wants legacy `replica_id` or current `face_id`; verify the ID exists under the active Tavus account.
- **Training URL cannot be downloaded**: use a direct public/signed download URL, not a web preview page; keep it valid long enough for Tavus to fetch it.
- **Training video rejected**: confirm MP4/H.264, duration, FPS, file size, one unobstructed face, and no extra faces.
- **Video stuck generating**: poll with timeout, inspect webhooks, check Tavus status, then escalate with `video_id` and payload rather than repeatedly submitting duplicates.
- **Background missing or wrong**: verify the website/video URL is public, stable, and allowed to be captured; for custom video backgrounds use `background_source_url`, not `background_url`.
- **Bad pronunciation or language**: switch from `script` to approved `audio_url`, shorten sentences, or use voice/pronunciation features where available.
- **CVI responds to background noise**: configure voice isolation in the conversational-flow layer and test in realistic environments.
- **PAL does not join**: check Tavus status, conversation callback events, conferencing configuration, concurrency limits, `test_mode`, and whether a valid PAL/default Face is configured.

## Complete example: personalized outbound product video

Example production intent: create short, consent-safe, personalized sales videos from an approved Tavus stock or company-owned Face.

Approach:

1. Confirm the face is approved for commercial outbound use and does not imply personal endorsement beyond the approved presenter role.
2. Use async Video Generation, not CVI, because the deliverable is a shareable file.
3. Generate one pilot first; do not batch until QA passes.
4. Use a public product landing page as `background_url` only if it is stable and safe to capture.
5. Store each request/response in the campaign ledger.

Example script:

> Hi Jordan - I saw your team is hiring onboarding specialists, which usually means your customer handoffs are getting more complex. Acme Flow can turn each kickoff into a guided checklist, so your team spends less time chasing updates and more time helping customers launch. If you want, I can send over a two-minute walkthrough built around your onboarding page.

Example request:

```json
{
  "replica_id": "r90bbd427f71",
  "script": "Hi Jordan - I saw your team is hiring onboarding specialists, which usually means your customer handoffs are getting more complex. Acme Flow can turn each kickoff into a guided checklist, so your team spends less time chasing updates and more time helping customers launch. If you want, I can send over a two-minute walkthrough built around your onboarding page.",
  "video_name": "jordan-acme-flow-outbound-pilot",
  "background_url": "https://example.com/onboarding",
  "callback_url": "https://example.com/webhooks/tavus-video"
}
```

QA focus:

- Does the script sound personal but not creepy?
- Does the stock/custom face have permission for this sales context?
- Does the website background capture properly?
- Are the hosted/download URLs archived?
- Is there an AI-generated video disclosure in the delivery context?

## Complete example: real-time support PAL

Example production intent: deploy an AI human that answers basic support questions and hands off uncertain cases.

Approach:

1. Create or select a Face approved for support use.
2. Create a PAL with a support-specific system prompt, knowledge docs, guardrails, and objectives.
3. Start a test conversation with `test_mode: true` for payload validation, then a real private room for QA.
4. Capture callbacks and transcripts for review only if the user consent and privacy posture allow.

Example PAL prompt:

> You are Nova, a customer support PAL for Acme Flow. Your job is to help users understand onboarding checklists, integrations, and billing-plan boundaries. Use only the attached knowledge documents for factual product claims. If the customer asks for legal advice, refunds outside policy, account deletion, security incidents, or anything involving personal data you cannot verify, explain that a human specialist must help and offer to create a support ticket. Keep answers under 90 words unless the user asks for detail.

Example conversation context:

```json
{
  "face_id": "r90bbd427f71",
  "pal_id": "pcb7a34da5fe",
  "conversation_name": "support-qa-session-001",
  "conversational_context": "The user is testing whether Acme Flow supports Slack notifications for onboarding checklist changes.",
  "custom_greeting": "Hi, I'm Nova. I can help with Acme Flow onboarding questions. What would you like to check?",
  "require_auth": true,
  "max_participants": 2,
  "callback_url": "https://example.com/webhooks/tavus-cvi"
}
```

QA focus:

- Does the PAL answer from docs and admit uncertainty?
- Does it avoid unsupported policy promises?
- Does turn-taking feel natural?
- Are transcripts/recordings handled according to consent?

## Complete example: localization with approved audio

Example production intent: create Spanish and French versions of a founder explainer with exact reviewed translations and voice delivery.

Approach:

1. Confirm the founder's consent covers localized versions and the target distribution.
2. Translate and transcreate the script; have native reviewers approve pronunciation-sensitive names.
3. Generate or record final localized audio externally if exact voice, pacing, and legal copy are important.
4. Use `audio_url` with the async Video API for each locale.
5. QA lip sync, subtitles, and localized CTA separately per locale.

Example request:

```json
{
  "replica_id": "r90bbd427f71",
  "audio_url": "https://example-bucket.s3.amazonaws.com/founder-explainer-es-mx-approved.wav?...",
  "video_name": "founder-explainer-es-mx-v1",
  "background_source_url": "https://example-bucket.s3.amazonaws.com/product-loop-16x9.mp4?...",
  "callback_url": "https://example.com/webhooks/tavus-video"
}
```

QA focus:

- Do localized names and legal claims match approved text?
- Does the mouth track the language acceptably?
- Are captions/subtitles localized rather than auto-translated blindly?
- Does the archive identify locale, audio version, and reviewer approval?

## Source notes

Official/authoritative sources used for documented claims:

- Tavus API overview: https://docs.tavus.io/api-reference/overview
- Tavus introduction and PAL/Face terminology: https://docs.tavus.io/sections/introduction
- Create Face API: https://docs.tavus.io/api-reference/faces/create-face
- Face training path comparison: https://docs.tavus.io/sections/faces/which-training-path
- Video-to-Face guide: https://docs.tavus.io/sections/faces/video-to-face-quickstart
- Face overview and platform-policy note: https://docs.tavus.io/sections/faces/overview
- Generate Video API: https://docs.tavus.io/api-reference/video-request/create-video
- Video quickstart: https://docs.tavus.io/sections/video/quickstart
- Get Video API: https://docs.tavus.io/api-reference/video-request/get-video
- Background customization: https://docs.tavus.io/sections/video/background-customizations
- Create PAL API: https://docs.tavus.io/api-reference/pals/create-pal
- Create Conversation API: https://docs.tavus.io/api-reference/conversations/create-conversation
- Webhooks and callbacks: https://docs.tavus.io/sections/webhooks-and-callbacks
- Errors and status details: https://docs.tavus.io/sections/errors-and-status-details
- Troubleshooting: https://docs.tavus.io/sections/troubleshooting
- Acceptable Use Policy: https://www.tavus.io/acceptable-use-policy
- Terms of Service: https://www.tavus.io/terms-of-service
- Privacy Policy / biometric data policy: https://www.tavus.io/privacy-policy
- Pricing page, for volatile plan/language/concurrency context only: https://www.tavus.io/pricing
