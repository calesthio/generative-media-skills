---
name: midjourney-video
description: Plan and direct Midjourney Video V1 image-to-video work through the official website or Discord, with human operator handoff, motion prompts, start/end frames, loops, extensions, resolution and batch budgeting, privacy, rights, safety, and delivery QA. Use when creating Midjourney videos or when determining whether a requested API, automation, plan, or production workflow is supported.
---

# Midjourney Video

Treat Midjourney Video as a human-operated creative service, not a developer API. Prepare inputs, motion direction, settings, budget, and acceptance criteria; then hand the approved plan to the subscribed account owner for manual execution on `midjourney.com` or in Discord.

## Keep the interface boundary absolute

As of 2026-07-10, Midjourney's official Community Guidelines say it does not provide an API except for rare explicitly granted exceptions and prohibits automated tools, third-party scripts, and automated interaction. The current Terms also prohibit automated access and one account may be used by only one person.

Therefore:

- Do not write or run browser automation, Discord self-bots, reverse-engineered HTTP calls, cookie/token replay, scraping, queued submission scripts, or unofficial â€œMidjourney APIâ€ clients.
- Do not ask for account credentials, session cookies, Discord tokens, or remote control of the user's session.
- Do not call a third-party gateway an official Midjourney API. Do not send content to one without separate user approval and a terms/privacy review.
- Do not promise unattended backend integration, webhooks, deterministic job submission, programmatic seeds, or an SLA.
- Route requirements for supported programmatic generation to a provider with a documented public API. Use this skill only for planning and a manual operator handoff unless the customer can show an explicit written Midjourney automation exception.

Never perform the manual UI steps yourself. A human operator must inspect the account state, approve the visible GPU-time impact, submit the job, choose candidates, extend, and download.

Treat that manual execution as a revision-bound authorization, not delegated autonomy. Freeze the exact handoff text, input hashes, settings, prompt, submission count, and Fast-minute cap before approval. Approval covers only that revision and those listed submissions. Any operator edit, changed account state, extra variation or extension, visibility mismatch, or undocumented UI behavior voids the approval and requires a new handoff.

## Establish the current contract

The following facts were verified from first-party documentation on 2026-07-10 and are volatile:

- The public video model is **Video V1**, introduced in June 2025. The current default **image** model is V8.1; that does not make the video model â€œV8.1.â€
- Video is image-to-video: one starting image is required and a text motion prompt is optional. There is no documented direct text-to-video workflow.
- Any Midjourney gallery image can be animated regardless of the image-model version that created it. Original image parameters are removed during video generation.
- An external starting image can be uploaded on the website or supplied through a valid online image URL in Discord.
- An initial job creates 5-second videos. The default batch is four; `--bs 1`, `--bs 2`, or `--bs 4` changes it.
- Each extension adds four seconds. Extend at most four times, for 5, 9, 13, 17, or 21 seconds total.
- Supported video controls are `--motion low`, `--motion high`, `--raw`, `--loop`, `--end`, and `--bs`. Do not append image-only controls such as `--v`, `--ar`, `--seed`, style references, Image Prompts, or Omni References to a video job.
- Low Motion is the default and favors subtle subject/camera movement. High Motion permits larger movement but raises the risk of implausible motion and glitches.
- `--raw` reduces Midjourney's added creative treatment so the motion prompt has more influence.
- A second image may be used as an ending frame. Reusing the start as the end (`--loop`) requests a loop.
- SD is described as 480p; HD as 720p. The starting image determines the output shape, and Midjourney may adjust the aspect ratio slightly.
- Official docs expose no frame-rate, codec-profile, audio-generation, negative-prompt, or video-seed control. Do not invent one. Treat the result as a visual asset, inspect the downloaded file, and plan sound separately.

Published example dimensions are:

| Starting aspect | Video aspect | SD | HD |
|---|---|---:|---:|
| 1:1 | 1:1 | 624Ã—624 | 960Ã—960 |
| 4:3 | 77:58 | 720Ã—544 | 1104Ã—832 |
| 2:3 | 2:3 | 512Ã—768 | 784Ã—1168 |
| 16:9 | 91:51 | 832Ã—464 | 1280Ã—720 |
| 1:2 | 1:2 | 448Ã—880 | 672Ã—1360 |

These are documented mappings, not an arbitrary-size menu. Probe the result because Midjourney says it may adjust the aspect slightly.

Do not rely on launch posts for current availability. For example, the 2025 HD launch announcement restricted HD to Pro/Mega, while the current plan and video docs allow HD on Standard, Pro, and Mega in Fast Mode. Prefer the current documentation and date the decision.

## Choose the manual surface

Prefer the website for production handoff because its Starting Frame, Ending Frame, Loop, resolution, batch, motion, privacy, organize, and download controls are visible together.

Website flow for the human operator:

1. Open the Create page and confirm the correct account, plan, Fast/Relax mode, visibility, video resolution, batch size, and motion default. Website and Discord settings sync, so do not assume yesterday's defaults.
2. Load an image into **Starting Frame**. Add a distinct **Ending Frame** or enable **Loop** only if requested.
3. Choose **Animate Manually** to enter reviewed motion direction. Auto animation delegates the direction to Midjourney and is unsuitable when an approved shot specification matters.
4. Confirm the visible settings and GPU-time estimate, then manually submit.
5. Review every returned candidate. Extend only the selected branch, using **Extend Manual** when the next beat changes.
6. Download **Raw Video** for the archive. Download **for Social** only as a derivative delivery; GIF is a review/communication derivative, not a master.

Discord remains a supported manual surface:

- For a Midjourney image, separate the chosen grid item with `U1`â€“`U4`, then click Animate Low/High. Enable Remix Mode before clicking if the operator needs to edit the motion prompt.
- For an external image, manually submit an online image URL followed by the motion prompt and `--video`. Add only video-compatible parameters.
- Use `--loop` to reuse the start as the end, or `--end <image-url>` for a distinct end frame.
- A private server or direct message organizes work but does not by itself make content private on Midjourney's website.

Example Discord handoff text, for the operator to paste manually:

```text
https://approved.example/start-frame.jpg The cyclist pedals steadily through light rain while the camera tracks alongside at matching speed; coat fabric and wheel spray move naturally, background traffic drifts slowly, and the framing settles without a cut. --video --motion low --raw --bs 1 --end https://approved.example/end-frame.jpg
```

This is a handoff example, not an executable API request. Confirm that both URLs are approved and safe to expose to Discord/Midjourney before using it.

## Match plan, speed, resolution, and queue

Current plan facts verified 2026-07-10:

| Plan | Monthly price | Fast time/month | Video resolution | Video concurrency | Relax video | Stealth |
|---|---:|---:|---|---|---|---|
| Basic | $10 | 3.3 h / 200 min | SD | 1 Fast | No | No |
| Standard | $30 | 15 h | SD + HD | 3 Fast | No | No |
| Pro | $60 | 30 h | SD + HD | 6 Fast or 3 Relax | SD only | Yes |
| Mega | $120 | 60 h | SD + HD | 12 Fast or 3 Relax | SD only | Yes |

All plans auto-renew unless canceled. Annual plans are paid upfront at a published 20% discount. Extra Fast time is currently $4 per GPU hour. The published maximum queue is 10 jobs, with plan-specific Relax-video queue notes. Concurrency is not a throughput SLA; Relax wait is documented as variable and can reach roughly 30 minutes.

HD video is Fast-only. Pro/Mega Relax video is SD-only. Basic supports SD Fast only. Never tell a Basic customer that buying extra Fast time unlocks HD; resolution entitlement is plan-based.

### Calculate GPU-time exposure

| Resolution | Batch 1 | Batch 2 | Batch 4 (default) |
|---|---:|---:|---:|
| SD | 2 min | 4 min | 8 min |
| HD | 7 min | 13 min | 26 min |

Each extension consumes the same GPU time as an initial generation at the chosen batch/resolution. Estimate:

```text
fast_minutes = (1 initial job + extension jobs) Ã— documented minutes for resolution/batch
```

Examples:

- One 5-second SD candidate with `--bs 1`: about 2 Fast minutes.
- One 5-second HD candidate with `--bs 1`: about 7 Fast minutes.
- One selected 21-second path in HD, using batch 1 for the initial job and all four extensions: about 35 Fast minutes.
- Leaving the default at batch 4 for that same five-job path: about 130 Fast minutes.

These are GPU-time estimates, not wall-clock guarantees or per-clip cash charges. Relax jobs do not consume the monthly Fast pool but still use the service and queue. The video docs say blocked jobs do not deduct GPU time; moderation success is not permission to use the result.

Set a hard handoff cap in Fast minutes and number of submissions. The operator must stop before exceeding it and return for approval. Do not upgrade, purchase extra hours, or modify auto-renewal without explicit authorization.

## Prepare a strong starting frame

The starting frame carries appearance, composition, aspect ratio, lighting, and identity. Resolve these before animation:

- Use a clean image under the website's current 10 MB upload limit. Verify rights, consent, orientation, crop, color, and absence of unintended text/logos.
- Leave spatial room in the direction of travel and avoid limbs or objects clipped exactly at the edge.
- Prefer a readable pose with clear depth layers; extreme occlusion leaves the motion model little evidence.
- For a distinct end frame, use the same intended aspect, compatible subject scale, camera axis, lighting logic, and scene layout. This is a production heuristic, not a documented hard requirement.
- Do not expect Image Prompt, Style Reference, or Omni Reference to maintain identity during video. Those reference types are explicitly incompatible with the video job. Create the approved appearance in the starting/end frames first.

## Direct motion, not a new still image

Write a concise continuous shot in temporal order. The starting frame already describes what exists; use the motion prompt to say what changes.

Include, when relevant:

1. Primary subject action and direction.
2. Camera move and framing behavior.
3. Secondary/environmental motion.
4. Tempo, weight, or physical quality.
5. The final pose/composition or seamless-loop condition.

Prefer one camera move and one dominant subject action per five-second segment. Avoid edit-language that implies several shots, instantaneous costume/location changes, conflicting camera moves, or three unrelated actions. Use Low Motion for restrained product shots, portraits, slow atmospheres, and identity-sensitive work. Use High Motion for running, broad camera moves, or energetic environments only when distortion risk is acceptable.

Use `--raw` when literal motion direction matters. It does not guarantee compliance. Treat exact logo/text preservation, hands, faces, lip movement, cloth physics, reflections, and contact events as review risks.

## Build an operator handoff

Return this filled specification to the human operator before generation:

```text
MIDJOURNEY VIDEO HANDOFF
Handoff revision: [immutable revision ID and SHA-256 of the canonical body below, excluding this line and Approval]
Approval: [approver, timestamp, approved revision ID/hash, and exact authorized submission/extension count]
Surface: website | Discord (manual only)
Account owner: [named authorized operator]
Plan/speed: [Basic/Standard/Pro/Mega] / [Fast or SD Relax]
Visibility: [Public or Stealth]; Discord space: [web/DM/private/shared]
Starting frame: [approved filename or URL], SHA-256: [hash]
Ending frame: [none / same for loop / approved filename or URL], SHA-256: [hash]
Rights/consent record: [location and approver]
Resolution: [SD or HD]
Batch: [1, 2, or 4]
Motion: [Low or High]
Raw: [on/off]
Initial motion prompt: [exact approved text]
Extension prompts: [none or exact ordered list, maximum four]
Estimate: [Fast minutes]; hard cap: [minutes and submission count]
Acceptance: [duration, composition, identity, motion, seam, safety requirements]
Return: raw MP4, optional social MP4/GIF, creation URL/job identifier, chosen candidate index, exact prompts/settings, timestamps, and operator notes
Stop conditions: blocked/moderated input, wrong visibility, settings mismatch, cap reached, rights uncertainty, identity drift, unsafe output, or undocumented UI behavior
```

Hash locally approved frames before upload; do not embed confidential source files in the handoff itself. When Discord requires a public HTTPS image URL, use only an approved, least-privilege URL with no embedded account credentials, expose it only for the minimum practical time, and keep the raw URL out of durable logs; retain the asset hash and controlled asset record instead. The operator must not alter the frozen prompt, inputs, settings, or cap. The operator must return what the UI actually showed, because labels, entitlements, costs, and controls can change without an API schema or changelog contract.

## Complete example 1: restrained product reveal

**Intent:** Create one polished 5-second 16:9 HD candidate from an approved fictional product image while minimizing shape drift.

**Plan:** Website, Pro account in Stealth, Fast, HD, batch 1, Low Motion, Raw. Estimated exposure: 7 Fast minutes. Starting frame already contains the final product design and cleared background. No end frame.

**Example motion prompt:**

> The camera makes a slow, smooth twenty-degree clockwise arc around the bottle while keeping the label centered and the bottle shape rigid. A narrow highlight travels gently across the glass; condensation beads remain attached and catch the light. The background falls slightly out of focus and nothing enters the frame. The camera eases to a complete stop on a clean three-quarter hero angle, with no cut.

**Operator action:** Verify Stealth/Fast/HD/batch 1/Low/Raw, use Animate Manually, submit once, download the Raw MP4 only if the candidate passes.

**Acceptance:** correct 5-second duration, expected HD dimensions for the starting aspect, stable silhouette and label, physically plausible highlight, no new objects, smooth ease-out, full decode.

**Likely failures:** warped typography, breathing geometry, sliding condensation, excessive parallax. If motion is too weak, revise the camera arc before switching to High Motion; High Motion may worsen product deformation.

## Complete example 2: controlled start-to-end performance

**Intent:** Move a fictional dancer between two cleared 2:3 frames while preserving screen direction.

**Plan:** Website or manual Discord, Standard account, Fast, SD batch 2 for exploration, Low Motion, Raw, distinct end frame. Estimated exposure: 4 Fast minutes. Both frames share crop, costume, lighting, and camera axis.

**Example motion prompt:**

> In one continuous take, the dancer turns once to her left with grounded, natural weight, then steps forward into the final raised-arm pose. The camera stays locked at waist height; loose fabric follows the turn with a slight delay and settles naturally. Background curtains move only from the passing air. Finish precisely in the ending-frame composition without a cut or sudden speed change.

**Expected result:** two five-second alternatives interpolating toward the supplied end composition.

**Likely failures:** forced morph near the end, limb duplication, reversed turn, abrupt final snap. Prefer the candidate with the cleanest whole-body path, not merely the closest final frame. If both snap, simplify the end pose or make start/end states more compatible.

## Complete example 3: 21-second one-shot progression

**Intent:** Produce a continuous illustrated night-train shot with four story beats and no scene cut.

**Plan:** Website, HD Fast batch 1, Low Motion + Raw, one initial generation and four manual extensions. Estimated exposure: 35 Fast minutes. Approve each branch before paying for its next extension.

**Example ordered prompts:**

1. Initial 5 s: â€œThe camera glides slowly down the empty train aisle as warm carriage lamps sway slightly; rain streaks move across the windows and the red suitcase at the far end remains centered. Continuous shot, no cut.â€
2. Extend to 9 s: â€œContinue the same forward glide. A gloved hand reaches from the right seat and pulls the red suitcase gently into the aisle; preserve the carriage, lighting, direction, and pace.â€
3. Extend to 13 s: â€œThe suitcase rolls away from the camera down the center aisle with believable wheel motion. The camera follows at the same slow speed; window rain and lamp sway continue.â€
4. Extend to 17 s: â€œA conductor steps calmly into the far doorway and stops the suitcase with one shoe. Keep the camera axis and all design details unchanged; no cut.â€
5. Extend to 21 s: â€œThe camera eases to a stop as the conductor lifts the suitcase handle and looks toward the left window. Rain continues; lamps settle; hold the final composition.â€

**Acceptance at every branch:** last-frame continuity, stable aisle geometry, consistent suitcase, plausible contact, no jump in camera speed, no new characters before requested. Stop and regenerate from the last clean branch instead of extending a damaged one.

## Protect privacy, rights, and people

Midjourney is open by default. Public creations may be visible and remixable. Stealth is available only on Pro/Mega and is described as a best-efforts promise not to publish; it controls website visibility, not what people in a shared Discord channel can see. Enabling Stealth later does not automatically privatize old work, and trashing is not the same as making private.

For the strongest available product privacy, use Pro/Mega Stealth on the website, in a Discord direct message, or in a private Discord server. This still is not a confidentiality, residency, deletion, or no-training guarantee.

Current policies state:

- Inputs, prompts, uploads, outputs, and account data may be collected. The privacy FAQ says personal information Midjourney handles is stored on US servers and retained as necessary for service, improvement, legal, and other stated purposes; it gives no fixed routine retention period.
- Discord controls data stored on Discord under its own policies.
- The Terms grant Midjourney a perpetual, worldwide, sublicensable, royalty-free, irrevocable license over submitted Content and generated Assets; the license survives termination.
- Account deletion has a seven-day reversal window and the FAQ says associated data is deleted within 30 days after a successful request, subject to the governing policy. Do not present this as per-job deletion.

Do not upload unreleased products, client-confidential footage, biometric/medical data, minors, regulated data, or residency-constrained assets until the customer's legal/security team accepts the current contracts. Use a provider with an appropriate enterprise/DPA/API contract when manual consumer-service terms are insufficient.

Obtain necessary rights and permission from every depicted person and source owner. The current Terms say customers own generated Assets to the fullest extent possible under applicable law, subject to the Agreement and third-party rights. Companies or employees of companies with over USD 1 million annual revenue must use Pro or Mega to own their Assets under the Terms. This is not a guarantee of copyright, exclusivity, trademark clearance, likeness clearance, or non-infringement; obtain counsel for consequential commercial use.

Follow the current SFW Community Guidelines everywhere, including Stealth, private servers, direct messages, and hidden/deleted content. Do not create adult/gore content, abusive or harmful depictions of real people, sexualized deepfakes, misinformation/disinformation, political-campaign/election-influence media, deception/fraud, illegal content, or misleading claims about generated media. A prompt passing the filter does not make it permitted. Label synthetic footage when omission could mislead viewers.

## Validate and finish outside Midjourney

Archive the Raw MP4 as a no-overwrite master before any transcode. Verify its hash after transfer. Record its hash, file size, creation URL/job identifier, candidate index, prompts, settings, account plan/speed/visibility, handoff revision, and operator timestamp. Treat creation URLs as access-controlled metadata; do not record credentials or expiring/private source URLs.

Inspect what Midjourney actually delivered instead of assuming undocumented technical properties:

```bash
ffprobe -v error -show_streams -show_format -of json midjourney-raw.mp4
ffmpeg -v error -i midjourney-raw.mp4 -f null -
```

Verify duration, dimensions, display aspect, frame rate, codec/profile, color metadata, playable frames, and whether an audio stream exists. Review at native scale and delivery scale for first/last-frame fidelity, identity, anatomy, text/logo stability, object permanence, camera path, contact physics, flicker, warping, loop/end-frame behavior, and every extension seam.

Build sound, captions, disclosure, edit, color-management, and final delivery in a separate post-production workflow. A â€œDownload for Socialâ€ MP4 is a convenience derivative, not proof of platform-specific compliance. Encode and QC each required deliverable against its destination specification.

## Re-check these first-party sources

- [Video documentation](https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video)
- [Comparing plans](https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans)
- [GPU Speed: Fast, Relax, Turbo](https://docs.midjourney.com/hc/en-us/articles/32016412137741-GPU-Speed-Fast-Relax-Turbo)
- [Creating on Web](https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web)
- [Stealth Mode](https://docs.midjourney.com/hc/en-us/articles/32019750070669-Stealth-Mode)
- [Community Guidelines](https://docs.midjourney.com/hc/en-us/articles/32013696484109-Community-Guidelines)
- [Terms of Service](https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service)
- [Privacy Policy](https://docs.midjourney.com/hc/en-us/articles/32083472637453-Privacy-Policy)
- [Data Deletion and Privacy FAQ](https://docs.midjourney.com/hc/en-us/articles/32084462534541-Data-Deletion-and-Privacy-FAQ)
- [Using Images & Videos Commercially](https://docs.midjourney.com/hc/en-us/articles/27870375276557-Using-Images-Videos-Commercially)
- [Video V1 announcement](https://updates.midjourney.com/introducing-our-v1-video-model/)

Re-check official docs immediately before handoff. Model labels, UI controls, supported parameters, dimensions, GPU costs, plans, concurrency, visibility, moderation, legal terms, and privacy practices can change without a stable developer schema.


