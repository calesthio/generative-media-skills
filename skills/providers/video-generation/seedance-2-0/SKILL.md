---
name: seedance-2-0
description: Direct ByteDance Dreamina Seedance 2.0 Standard, Fast, and Mini video production across BytePlus ModelArk and verified gateways. Use for text/image/reference-to-video, native synchronized audio and dialogue, multimodal image-video-audio reference, first/last-frame animation, video editing or extension, model/gateway selection, prompt construction, async task handling, failure recovery, QA, and rights-safe production.
---

# Direct Seedance 2.0 production

Treat this as a provider- and model-family-specific operating guide, not a generic video-prompt recipe. Establish the exact gateway contract before writing a request. “Seedance 2.0” does not imply one portable model ID or schema.

Evidence labels used here:

- **Documented** — stated in ByteDance/BytePlus or gateway documentation, verified 2026-07-09.
- **Production heuristic** — a recommended operating practice inferred from documented behavior and normal video-production constraints; validate on the current deployment.
- **Independent evidence** — third-party measurement or observation with its limits stated.

## Decide whether Seedance 2.0 fits

Prefer this family when the shot benefits from one or more of:

- synchronized picture, dialogue, ambience, music, or effects generated in one pass;
- reference images for subject/product/style/layout, a reference video for motion/camera/editing, or reference audio for timbre/rhythm;
- a short self-contained shot, multi-shot beat, edit, or extension lasting 4–15 seconds;
- a first-frame or strict first-and-last-frame transition;
- a multimodal edit in which an element from one asset modifies a different source video.

Choose another workflow, or plan post-production, when the requirement is:

- a single generated clip longer than 15 seconds;
- frame-exact editorial timing, exact choreography, deterministic simulation, or guaranteed seed reproducibility on direct ModelArk;
- exact long-form typography, legal text, captions, UI, pack copy, or a pixel-exact logo;
- direct upload of ordinary real-person face assets to ModelArk without its authorization/trusted-asset process;
- local weights or offline execution;
- direct BytePlus use from the United States: BytePlus's service-specific terms state that its Model Services are not available there. Check gateway and customer-specific availability rather than assuming a third-party route has the same territorial contract.

Do not call Seedance 2.0 “best” in the abstract. ByteDance's published comparisons include internal evaluation, and public leaderboards change. Select it against the shot's references, audio, control, delivery, cost, latency, and compliance needs.

## Lock the route and model before prompting

### BytePlus ModelArk, the direct documented contract

The official API is asynchronous:

- create: `POST https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks`
- retrieve: `GET https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks/{id}`
- authenticate with a ModelArk API key;
- store the returned task ID, poll or use a callback, and copy the output to durable storage immediately.

Use the current model catalog, not an invented alias:

| Variant | ModelArk ID verified 2026-07-09 | Choose when | Documented output ceiling |
|---|---|---|---|
| Seedance 2.0 | `dreamina-seedance-2-0-260128` | maximum family quality; 1080p or 4K required | 480p, 720p, 1080p, 4K; 4K is 10-bit HEVC |
| Seedance 2.0 Fast | `dreamina-seedance-2-0-fast-260128` | lower latency/cost matters more than the last quality increment | 480p, 720p |
| Seedance 2.0 Mini | `dreamina-seedance-2-0-mini-260615` | best family cost efficiency for drafts or scaled workloads | 480p, 720p |

Standard, Fast, and Mini are documented as largely sharing the core creation modes, but output and platform controls differ. Confirm the live model card and activation status before spending.

### Gateway contracts are different APIs

Do not translate calls by changing only the model name.

| Contract | Identifier/endpoint pattern | Important differences verified 2026-07-09 |
|---|---|---|
| BytePlus ModelArk | model ID in one content-generation endpoint | heterogeneous `content[]` items with `role`; `ratio`; integer `duration` or `-1`; direct Seedance 2.0 does **not** support `seed`, `frames`, or `camera_fixed`; asynchronous task ID |
| fal | `bytedance/seedance-2.0/{text-to-video,image-to-video,reference-to-video}` and `/fast/...` | separate mode endpoints; `aspect_ratio`; `duration` is an enum such as `"auto"` or `"4"`–`"15"`; first/last fields and modality URL arrays; exposes `seed`; exact resolution options differ by endpoint/tier, so read that endpoint's live schema |
| Replicate | `bytedance/seedance-2.0` | unified wrapper; `image`, `last_frame_image`, `reference_images`, `reference_videos`, `reference_audios`; integer `duration` with `-1`; `aspect_ratio`; exposes `seed`; returns a file/URI |

Gateway-exposed seed fields do not prove that direct ModelArk has seed control. Treat reproducibility as gateway-specific and verify by repeated tests; even a fixed supported seed need not yield byte-identical output.

Gateway prompt labels also differ. ModelArk documentation refers to media by ordered type as `Image 1`, `Video 1`, and `Audio 1`. fal pages use forms such as `@Image1` and, on other pages, `[Image1]`; Replicate documents `[Image1]`. Follow the active endpoint's schema and example exactly. Never reference an asset ID in prose when the contract expects an ordinal media label.

Do not hardcode prices, rate limits, or route availability into a production plan. Fetch them at preflight; record retrieval time, model/tier, resolution, duration, audio setting, input-video surcharge rules, and currency.

## Direct ModelArk request envelope

Use top-level JSON parameters, not legacy prompt suffixes.

| Field | Direct behavior verified 2026-07-09 |
|---|---|
| `model` | current model ID or an activated endpoint ID |
| `content` | ordered text/image/video/audio items; roles determine first/last/reference behavior |
| `resolution` | default 720p; Standard alone supports 1080p and 4K under the current contract |
| `ratio` | `adaptive`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, or `9:16`; default `adaptive` for the 2.0 series |
| `duration` | integer 4–15, default 5; `-1` delegates integer duration selection to the model and affects billing |
| `generate_audio` | default `true`; `false` produces silent output; generated audio is mono |
| `watermark` | default `false`; `true` adds an “AI Generated” mark in the lower right; do not remove required provenance signals |
| `return_last_frame` | default `false`; request a PNG last frame for continuity workflows |
| `callback_url` | optional status callback; authenticate and make callback handling idempotent |
| `execution_expires_after` | 3,600–259,200 seconds; default 172,800 (48 h) |
| `safety_identifier` | stable, unique end-user identifier, at most 64 characters; hash an internal ID rather than send personal data |
| `priority` | Standard Seedance 2.0 only; integer 0–9 within the same endpoint queue; not an execution-speed guarantee |

Do not send `frames`, `seed`, `camera_fixed`, `draft`, or `service_tier: "flex"` for the direct 2.0 family merely because another Seedance version or gateway accepts them. The official API documents `frames`, `seed`, and `camera_fixed` as unsupported for Seedance 2.0, draft mode as a 1.5 Pro feature, and the 2.0 series as online-inference only.

### Build `content[]` correctly

Text item:

```json
{"type":"text","text":"<complete prompt>"}
```

First-frame image:

```json
{"type":"image_url","image_url":{"url":"<public URL, data URI, or asset:// ID>"},"role":"first_frame"}
```

Strict first-and-last frame mode requires exactly two image items with `first_frame` and `last_frame`. Reference mode uses `reference_image`, `reference_video`, and `reference_audio` roles.

First-frame, first-and-last-frame, and multimodal-reference modes are mutually exclusive at the role level. In reference mode, prompt language can ask an image to influence the opening or ending, but only first/last-frame roles strictly anchor those frames.

### Validate media before submission

Direct ModelArk documents these limits:

- reference images: 1–9; JPEG, PNG, WebP, BMP, TIFF, GIF, HEIC, or HEIF; each under 30 MB; width and height each between 300 and 6000 px; width/height ratio greater than 0.4 and less than 2.5;
- reference videos: 0–3; each 2–15 s, combined duration at most 15 s; MP4 or MOV with supported H.264/H.265 video and AAC/MP3 audio; each at most 200 MB; 24–60 fps; dimensions and total pixels must meet the current API table;
- reference audio: 0–3; each 2–15 s, combined duration at most 15 s; WAV or MP3; each at most 15 MB;
- audio cannot be the only non-text reference: include at least one image or video;
- base64 request bodies are limited; prefer durable public/object-storage URLs for large media.

Use `ffprobe` or equivalent before paying for generation. Verify codec, duration, fps, dimensions, aspect ratio, audio stream, and file size. Normalize orientation metadata. Strip accidental captions, watermarks, unrelated faces, and conflicting backgrounds when they are not intended references.

## Assign one job to each reference

Use the smallest reference set that can express the shot. The official prompt guide warns against automatically filling every available slot: too many references obscure feature priority and can cause style conflicts, weak subject identification, and drift.

Create an asset ledger before writing the prompt:

| Ordinal | Asset | Rights/consent | Intended dimension | Must preserve | May change |
|---|---|---|---|---|---|
| Image 1 | product hero | owned | exact geometry, label colors | silhouette, materials | environment |
| Video 1 | motion plate | licensed | camera path and hand motion | timing, interaction | original product |
| Audio 1 | approved voice sample | performer release | timbre and pace | voice character | exact words |

Order high-priority assets first. Reference only the dimension needed: subject identity, product geometry, wardrobe, environment, composition, camera movement, action, effect, voice timbre, melody, or rhythm. “Use everything from every reference” creates conflicts.

For characters, the official guide recommends a clean headshot plus one full-body/styling image rather than a multi-view collage. A small face inside a busy sheet receives weak identity weight; multiple views may be interpreted as different people and increase identity drift or duplicates. On ModelArk, use its trusted-output, preset-character, or authorized-real-person asset paths rather than trying to bypass face moderation.

## Write prompts as executable direction

Start with the shot's invariant, then its temporal behavior:

1. define each subject with 2–3 stable, discriminative features and bind it to an ordered asset;
2. state what reference dimension to inherit and what must remain unchanged;
3. describe the setting and spatial relationships;
4. describe action through body part, direction, magnitude, speed, force, and transition/inertia;
5. organize complex clips as `Shot 1`, `Shot 2`, `Shot 3` in event order;
6. give one principal camera movement per shot;
7. specify dialogue, voice character, ambience, effects, and music behavior;
8. close with style, lighting, image-quality, and negative constraints.

Use the same subject label every time. Re-bind it when ambiguity is possible: `the amber bottle from Image 1`, not later just `it` when several props exist.

Prefer causal verbs and observable performance:

- weak: `She is nervous and the shot is cinematic.`
- stronger: `Her shoulders tighten; she glances twice toward the locked door, exhales through parted lips, then slowly reaches for the handle. A restrained handheld medium close-up follows her hand.`

For multi-shot generation, describe order rather than demanding frame-accurate timecodes. BytePlus explicitly documents unstable compliance with exact segment timing such as “0–3 seconds.” Use approximate beats, generate shots separately when a cut must land exactly, and finish timing in an editor.

Do not stack push-in, orbit, pan, tilt, zoom, crane, and shake into one shot. The official guide recommends one camera movement per shot because combined movement increases instability.

For dialogue:

- put exact spoken words in double quotation marks;
- name the speaker on every line and specify delivery briefly;
- keep spoken language consistent; avoid casual bilingual mixing except proper nouns;
- budget words to duration and performance rather than cramming a paragraph into 8 seconds;
- request clean room tone or explicit ambience; generated audio is mono on direct ModelArk;
- expect pronunciation, voice match, end-clicks, or cut-off noise to need regeneration or post repair.

For on-screen text, keep phrases short and common. Even though the model supports slogans, subtitles, and speech bubbles, do not trust generated typography for legal copy or final brand delivery. Prefer clean footage plus deterministic text and logo compositing in post.

## Mode-specific direction

### Text to video

Describe subject, environment, action sequence, camera, lighting, visual finish, audio, and exclusions. Use this for original shots when reference fidelity is not required.

### First frame or first-and-last frames

Describe motion away from the first frame and, for two-frame mode, the causal transformation that arrives at the last. Match input and output aspect ratios; mismatched dimensions can cause center crop, stretching, compression, or abrupt frame jumps. Use `ratio: "adaptive"` when exact delivery framing is not yet locked, or pre-crop both frames to the documented target raster.

### Multimodal reference

Use explicit bindings such as:

```text
Define the matte amber pump bottle in Image 1 as PRODUCT.
Use only the clockwise hand rotation and camera path from Video 1.
Use the warm, low female timbre from Audio 1 for the quoted line.
PRODUCT keeps its exact silhouette, pump geometry, amber glass, and cream label throughout.
...
```

Do not submit reference audio alone. When voice matching matters, describe voice traits in words as well as attaching the approved sample, and keep new lines close to the sample's register and delivery.

### Video editing

Name the source and scope, then state what changes and what stays:

```text
Strictly edit Video 1. Replace only the silver can with PRODUCT from Image 1. Preserve the actor's hands, grip, finger occlusion, camera movement, lighting direction, reflections, background, timing, and all other content.
```

For removal, name both the object to remove and the background/occlusion behavior that must be reconstructed. For combined tasks, distinguish the reference source from the video being edited.

### Extension and track completion

State forward or backward extension, the new action, and continuity constraints for subject, lighting, camera, motion, ambience, and narrative. With 2–3 source clips, describe the transition sequence explicitly.

Expect iterative extension to degrade detail and faces. Limit continuation depth, keep high-quality anchors, and regenerate from a clean state rather than extending an already degraded result repeatedly. Official guidance notes that joins can jump or roll back; align and trim in post and hide difficult joins on motivated cuts.

## Complete prompt examples

These are examples, not mandatory formulas. Translate field names and media labels to the active gateway.

### Example 1 — original vertical dialogue scene on direct ModelArk

**Intent:** create one 8-second, audio-on, 9:16 social shot without external references.

**Request:**

```json
{
  "model": "dreamina-seedance-2-0-260128",
  "content": [{
    "type": "text",
    "text": "Photorealistic vertical lifestyle scene. A fictional woman in her early thirties stands at a sunlit kitchen island holding an unbranded ceramic travel mug. She has a short black bob, a mustard linen shirt, and a calm, candid manner. Single shot: medium close-up with a gentle handheld drift only. She turns the mug once in both hands, looks toward the hallway, smiles slightly, and says in a warm conversational voice: \"Train in ten. Let's go.\" A soft ceramic tap lands as she sets it down. Natural room tone, distant morning traffic, no music. Soft window light, realistic skin texture, neutral color grade. No subtitles, no logos, no watermark-like graphics, no duplicate fingers, no extra people."
  }],
  "resolution": "1080p",
  "ratio": "9:16",
  "duration": 8,
  "generate_audio": true,
  "watermark": true,
  "return_last_frame": false,
  "safety_identifier": "<stable-end-user-hash>"
}
```

**Why structured this way:** one speaker, one action arc, one camera motion, quoted speech, and explicit sound priorities fit the duration. The actor is fictional, the object is unbranded, and the line makes no testimonial or product-performance claim.

**Expected result:** a usable hero take with synchronized speech and a motivated object sound.

**Likely failures and repair:** if the line truncates, shorten it or increase duration; if unwanted captions appear, reinforce `no subtitles` and plan deterministic captioning in post; if fingers deform during the turn, simplify to a slower quarter-turn or split the set-down into another shot.

**Variation:** set `generate_audio: false` for a controlled external voiceover workflow.

### Example 2 — product fidelity plus motion and approved voice reference

**Intent:** make an 11-second landscape launch insert using two product images, one motion reference, and one consented voice sample.

**Inputs in request order:** Image 1 front product hero; Image 2 side/detail view; Video 1 licensed hand-and-camera motion plate; Audio 1 consented performer reference.

**Complete prompt:**

```text
Define the matte navy portable speaker shown in Image 1 and Image 2 as SPEAKER. Preserve SPEAKER's exact rounded-rectangle silhouette, grille pattern, two coral buttons, seam placement, and logo-free front.

Use only the slow hand placement and 30-degree clockwise camera arc from Video 1. Use the clear, low, lightly textured female timbre and measured pace from Audio 1 for the quoted line; do not reuse words from Audio 1.

Shot 1: On a dark walnut desk at blue hour, a hand places SPEAKER beside a rain-speckled window. Medium close-up; the camera performs the same restrained clockwise arc from Video 1. SPEAKER remains rigid and correctly proportioned.
Shot 2: Cut to a macro close-up of one coral button depressing once. A soft tactile click is synchronized with the press; a narrow rim light travels across the grille.
Shot 3: Return to the three-quarter hero angle. Off-camera, the woman says: "Small room. Full sound." A restrained low-frequency music pulse rises after the line, then ends cleanly.

Premium product cinematography, realistic materials, controlled reflections, navy-and-coral palette, shallow depth of field. No subtitles, no added labels, no altered button count, no warped grille, no hands touching the grille, no duplicate product, no third-party logo.
```

**Direct parameters:** Standard model; `resolution: "1080p"`; `ratio: "16:9"`; `duration: 11`; `generate_audio: true`; every media item uses the relevant `reference_*` role.

**Expected result:** product identity comes from Images 1–2, camera/action from Video 1, and voice character from Audio 1 without copying its content.

**Likely failures and repair:** if product geometry drifts, remove the lower-priority side image or reduce camera rotation; if the model copies source-video styling, state `reference only motion and camera path`; if voice match is weak, describe timbre/register more precisely and make the new line closer in cadence to the sample.

**Variation:** use Fast at 720p for motion-layout tests, then switch to Standard only after approval; record the model switch as a new paid generation decision.

### Example 3 — strict first/last-frame transformation

**Intent:** create a silent 6-second transition from a closed paper package to the same package opened with contents arranged.

**Inputs:** two owned images pre-cropped to the same 1:1 raster; `first_frame` then `last_frame`.

**Complete prompt:**

```text
Single locked overhead shot. Beginning exactly from the closed kraft-paper package in the first frame, two gloved hands enter from the lower edge, slowly untie the black cotton cord, unfold the top flap, and place the three tea sachets into a neat fan. Every movement is continuous and physically causal, arriving exactly at the supplied last frame. Preserve the package dimensions, paper texture, cord color, sachet count, tabletop grain, lighting direction, and all printed artwork from the supplied frames. Silent video. No additional objects, no camera motion, no text changes, no hand crossing over the printed mark.
```

**Direct parameters:** `resolution: "1080p"`; `ratio: "1:1"`; `duration: 6`; `generate_audio: false`.

**Expected result:** exact boundary frames with model-generated causal motion between them.

**Likely failures and repair:** if the pack jumps or stretches, verify both images have identical raster/aspect and match the chosen output table; simplify the knot action; try `adaptive` only if delivery framing is flexible. Do not replace strict roles with `reference_image` if exact end-frame arrival is required.

### Example 4 — reference-driven video edit

**Intent:** replace one prop in a licensed 7-second source plate while preserving performance and lighting.

**Inputs:** Image 1 owned cream jar; Video 1 licensed source plate with a generic jar and no unconsented face.

**Complete prompt:**

```text
Define the frosted pale-green cream jar with the flat white lid in Image 1 as JAR.

Strictly edit Video 1. Replace only the generic jar in the actor's right hand with JAR. Keep JAR's exact cylindrical proportions, frosted glass, flat lid, and blank label panel. Preserve the actor's hands and finger placement, natural occlusion around the jar, wrist motion, original camera path, rack focus, scene duration, background, wardrobe, lighting direction, shadows, reflections, and all audio from Video 1. Do not change the face, body, hand count, grip, or background. Do not add text, logos, subtitles, or a second jar.
```

**Direct parameters:** reference mode; `resolution: "1080p"`; `ratio: "adaptive"`; `duration: 7`; `generate_audio: true` if source audio continuity is required.

**Expected result:** local prop replacement with preserved plate motion.

**Likely failures and repair:** if the hand changes, repeat `replace only the jar` and slow/shorten the source plate; if lighting mismatches, add a product reference rendered under similar light; if exact brand graphics matter, composite the final label deterministically after generation.

### Example 5 — continuity chain with last-frame handoff

**Intent:** build a 24-second sequence as three separately approved 8-second clips.

**Workflow:**

1. Generate Clip A with `return_last_frame: true`; download both video and PNG immediately.
2. Use that PNG as Clip B's `first_frame`; describe only the next action and preserve subject, lens height, light, weather, screen direction, wardrobe, and ambience.
3. Repeat for Clip C.
4. Review each boundary frame before the next paid call; do not blindly propagate a malformed hand or face.
5. Join on motivated movement or a cutaway. Normalize codec, color, loudness, and room tone in post.

**Clip B prompt:**

```text
Continue exactly from the supplied first frame. The same red delivery bicycle moves left-to-right through the wet alley; the rider pedals twice, then brakes beside the blue doorway. Preserve the bicycle frame geometry, rider's yellow raincoat and black helmet, wet cobblestone reflections, overcast light, 35 mm eye-level perspective, left-to-right screen direction, and light rain ambience. One lateral tracking movement only. The brake squeak lands as the rear wheel stops; no speech or music. No new riders, no duplicated wheels, no change of weather, no subtitles or logos.
```

**Direct parameters:** Standard or Fast consistently across the chain; `ratio: "16:9"`; `duration: 8`; `generate_audio: true`; `return_last_frame: true`.

**Likely failures and repair:** repeated continuation may compound degradation. Regenerate from the last clean approved anchor rather than extend a degraded clip; use a cutaway to mask discontinuity; do not assume last-frame handoff guarantees identity or motion continuity.

## Production loop

1. **Preflight:** verify territory/account, active gateway and endpoint schema, model availability, quota/concurrency, live price, output rights, media rights, and face-asset path.
2. **Normalize assets:** inspect technical properties, crop for the intended ratio, remove accidental reference conflicts, and hash/store source provenance.
3. **Make a cheap proof:** test composition and motion at 480p/720p on Fast or Mini when that route reflects the final capability. Do not imply a draft proves Standard 4K quality.
4. **Generate a small candidate set:** vary one factor at a time—prompt, reference selection/order, duration, or model—not all simultaneously.
5. **Log every run:** gateway, endpoint/model, request JSON, ordered asset hashes, task/request ID, timestamps, cost, moderation outcome, returned metadata, and output checksum.
6. **Download immediately:** direct task records are retained for a limited period and result/last-frame URLs can expire. Store media in project-controlled durable storage.
7. **Review before scaling:** reject structural, rights, audio, or continuity failures before batch generation.
8. **Finish conventionally:** edit, stabilize, retime, add exact captions/logos/legal copy, mix audio, transcode, and verify delivery specs.

For callbacks, validate origin/signature if the gateway provides one, accept duplicate delivery, transition task state idempotently, and fall back to bounded polling with exponential backoff and jitter. Treat `queued`, `running`, `succeeded`, `failed`, `expired`, and `cancelled` explicitly. Do not endlessly resubmit a moderation failure.

## Diagnose before regenerating

| Symptom | Likely cause | First repair |
|---|---|---|
| subject identity drifts | face/subject too small, collage/multi-view ambiguity, weak binding | use a clean close-up plus one styling image; define and repeat one subject label; order identity first |
| duplicate people/products | ambiguous multiple views or crowded prompt | use single-subject references; bind every role; prohibit duplicates; split crowded action into shots |
| wrong product geometry | motion/style references overpower product reference | reduce references; state exact invariant features; use a slower, smaller rotation; composite fine label detail later |
| style drifts realistic | realistic source conflicts with requested stylization | name the target style globally and state which source dimensions not to inherit |
| unexpected subtitles/logo | speech or source text triggers graphic priors | remove irrelevant source text; state no generated text; try landscape; finish text/logo in post; accept that prompts cannot guarantee absence |
| first/last transition jumps | mismatched aspect/raster or over-complex transformation | pre-crop both frames to the same supported raster; simplify action; use adaptive ratio only when acceptable |
| exact beat ignored | model timing is approximate | use ordered shots without tight timestamps; generate separate shots and edit timing deterministically |
| camera unstable | too many simultaneous camera commands | keep one principal move per shot; reduce subject dynamics |
| dialogue truncates/mispronounces | too many words, uncommon/polyphonic terms, duration pressure | shorten/rephrase phonetically, simplify diction, extend duration, or dub in post |
| audio clicks at tail | generated phrase/music ends on clip boundary | regenerate with a clean ending or apply a short post-production fade/envelope |
| extension join jumps | rollback or discontinuity at generated boundary | trim/align around the join, cut on action, insert a cutaway, or regenerate from a cleaner transition |
| extension quality decays | repeated re-encoding/generation from degraded outputs | limit chain depth; reuse high-quality identity anchors; regenerate from the last clean state |
| moderation rejects a real face | direct upload is not a trusted/authorized portrait path | use ModelArk's authorized-real-person asset flow, approved preset character, or eligible same-account trusted output; never evade filters |
| request rejected | wrong schema, role combination, format, duration, region, quota, or unsupported parameter | validate against the exact live endpoint; remove cross-gateway fields; inspect structured error before changing creative intent |

Regenerate only after classifying the failure as contract, asset, prompt, model variance, moderation, or post-production. Preserve successful components rather than rewriting the whole prompt.

## Review the output as a deliverable

Inspect the complete file, not only a thumbnail or first frame.

**Picture and motion**

- subject/product identity, count, proportions, hands, faces, contact, occlusion, reflections, shadows;
- action order, causal continuity, physical plausibility, velocity, screen direction;
- camera path, focus, horizon, composition, crop, transitions, duplicated background figures;
- reference fidelity by assigned dimension rather than vague similarity;
- text/logo accuracy and any unwanted provenance-like marks.

**Audio**

- dialogue wording, speaker attribution, intelligibility, pronunciation, emotion, lip sync;
- sound-event timing, ambience continuity, music appropriateness, clipping, clicks, noise, abrupt tail;
- mono compatibility, loudness, true peak, and phase after the final mix.

**Technical**

- duration, frame rate, resolution, aspect ratio, codec/profile, pixel format, bit depth, audio stream, file integrity;
- 4K Standard output is documented as 10-bit H.265/HEVC; transcode a review proxy when the approval environment cannot decode it, while retaining the master;
- no expired remote URL is treated as the master asset.

**Editorial and safety**

- the shot fulfills the brief at normal playback speed;
- every person, voice, trademark, artwork, source clip, and music reference has documented permission;
- no deceptive impersonation, misleading claim, privacy leak, policy violation, or undisclosed synthetic depiction;
- required disclosure, watermark, metadata, and provenance are retained.

Require human review for public release, advertising claims, realistic people, political/news contexts, health/finance/safety claims, minors, or any high-impact use.

## Rights, consent, and safe operation

Before uploading, record source, owner, license, permitted transformations, territory, term, model-training restrictions, and release status for every asset. A technically accepted upload is not evidence of permission.

Obtain explicit, scoped permission for a person's face, body, performance, and voice. ModelArk's authorized-real-person library uses verification and authorization; use that path when applicable. Do not depict a living or dead person without appropriate rights, impersonate them deceptively, create non-consensual intimate content, or bypass face/public-figure filters.

Do not request copyrighted characters, franchise worlds, celebrity likenesses, signature performances, protected logos, or living-artist imitation merely because the model can approximate them. Use owned/public-domain/original direction, or document a license. BytePlus's terms make the customer responsible for input and output legality and say outputs may be non-unique; BytePlus does not warrant non-infringement.

Do not remove or conceal required AI indicators, watermarks, credentials, identifiers, metadata, or other provenance signals. Disclose synthetic media where context or law requires it. Keep raw generations, request records, consent records, and final-edit provenance.

Never work around moderation. If a benign request is blocked, inspect the provider error, remove ambiguity, use the documented authorized-asset route, or escalate to provider support. A gateway accepting content does not make the use lawful or safe.

## Source register

Volatile facts above were re-verified 2026-07-09. Re-check before production because model IDs, limits, access, schemas, and prices can change.

Primary and official:

- [ByteDance Seed — Seedance 2.0 model page](https://seed.bytedance.com/en/seedance2_0) — architecture/capability positioning and internal-benchmark disclosure.
- [Team Seedance, “Seedance 2.0: Advancing Video Generation for World Complexity”](https://arxiv.org/abs/2604.14148) — official model card; native multimodal audio-video generation, input modalities, original 4–15 s and reference limits.
- [BytePlus ModelArk — Seedance 2.0 series tutorial](https://docs.byteplus.com/en/docs/ModelArk/2291680) — variants, IDs, creation modes, 4K, portrait asset paths, limits, and operational troubleshooting.
- [BytePlus ModelArk — prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2222480) — subject binding, shot sequencing, camera/action guidance, asset priority, and documented failure recovery.
- [BytePlus ModelArk — create video generation task](https://docs.byteplus.com/en/docs/modelark/1520757) — authoritative direct request schema and media constraints.
- [BytePlus ModelArk — retrieve task](https://docs.byteplus.com/en/docs/modelark/1521309) — statuses, output metadata, usage, and result handling.
- [BytePlus ModelArk — product updates](https://docs.byteplus.com/en/docs/modelark/1159177) — 1080p/4K-era platform changes and input format updates.
- [BytePlus video-generation service terms](https://docs.byteplus.com/en/docs/modelark/Specific_Terms_for_the_BytePlus_Video_Generation_Model_Services) and [GenAI Acceptable Use Policy](https://docs.byteplus.com/en/docs/legal/acceptable_use_policy_byteplus_genai/) — territory, rights, provenance, consent, and safety obligations.
- [BytePlus Content Pre-filter FAQ](https://docs.byteplus.com/en/docs/modelark/content_pre_filter_faq) — public-figure face/voice similarity filtering and privacy notice.

Verified gateway documentation, not the direct BytePlus contract:

- [fal text-to-video schema](https://fal.ai/models/bytedance/seedance-2.0/text-to-video/api), [fal image-to-video](https://fal.ai/models/bytedance/seedance-2.0/image-to-video), and [fal reference-to-video](https://fal.ai/models/bytedance/seedance-2.0/reference-to-video).
- [Replicate Seedance 2.0 schema](https://replicate.com/bytedance/seedance-2.0/api/schema) and [usage guide](https://replicate.com/bytedance/seedance-2.0/readme).

Independent evidence, use narrowly:

- [Artificial Analysis Seedance family page](https://artificialanalysis.ai/video/model-families/Seedance) reports blind user-preference arena results plus price and generation-time measurements. Treat it as a dated comparative signal, not proof of fitness for a specific reference/edit/audio task; inspect sample counts, tested route, resolution, and methodology before citing a rank.
- [An independent TechRadar production analysis](https://www.techradar.com/ai-platforms-assistants/ive-been-watching-seedance-2-0-videos-so-you-dont-have-to-and-they-are-a-nightmare-dreamscape) described odd blinking, body motion, duplicated extras, plastic skin, and substantial conventional post-production in longer assembled pieces. This is a journalistic observation, not a controlled estimate of failure frequency. The official prompt guide's own identity, duplicate, subtitle, extension, and audio troubleshooting is the stronger basis for the recovery procedures above.
