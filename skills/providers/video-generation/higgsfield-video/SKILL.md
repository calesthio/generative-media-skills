---
name: higgsfield-video
description: Produce video (and its supporting stills) through Higgsfield (higgsfield.ai), a multi-model creative platform that fronts third-party video models (Kling, Veo, Seedance, Wan, MiniMax, and, until retirement, Sora) plus Higgsfield's own control layer — Soul / Soul ID image generation, the DoP camera-preset engine, and the Cinema Studio filmmaking suite. Use this skill when a request routes generation through Higgsfield specifically, when the user wants aggregator-level model switching and cinematic camera/effect presets in one workspace, when planning character consistency via Soul ID, or when deciding whether to go through Higgsfield versus direct to an underlying model provider. Covers model selection, per-model prompt strategy, credit economics, the (partial) API surface, capability limits, and rights/consent policy for generated and uploaded real-person footage.
---

# Higgsfield video

## What Higgsfield is, and the one fact that governs everything

Higgsfield (higgsfield.ai) is an **aggregator plus a control layer**. It is not a single model. It is a workspace that:

1. **Fronts third-party video models** you could otherwise reach directly (Kling, Veo, Seedance, Wan, MiniMax, and — until its shutdown — Sora), and
2. **Adds its own in-house layer** on top: `Soul` (image generation + `Soul ID` character identity), `DoP` (an image-to-video engine built around 100+ camera-motion presets), `Popcorn` (editing/inpaint), and `Cinema Studio` (a multi-shot filmmaking environment that orchestrates all of the above).

**The governing fact (documented):** *an aggregator inherits its models' limits.* Any claim about duration, resolution, physics, audio, or content moderation applies to **the specific underlying model**, not to "Higgsfield." When you reason about a task, first decide which model runs the shot, then apply that model's constraints. A statement like "Higgsfield does 4K with native audio" is only true for the models that do (Veo, Seedance) and false for the ones that don't. Track the model, not the brand.

Verified 2026-07-10. Model lineups, versions, and prices below are volatile — re-verify the live in-app model picker and pricing page before committing credits or quoting a client.

## When Higgsfield is the right tool (and when it isn't)

**Route through Higgsfield when:**
- You want to **compare several models on the same prompt** without holding accounts and billing at Kling, Google, ByteDance, etc. — side-by-side model switching in one workspace is the core value. (First-party claim.)
- You need Higgsfield's **distinctive control layer** — `Soul ID` character consistency, the `DoP` camera-preset library, or `Cinema Studio`'s multi-shot rig controls — which do not exist at the raw model providers.
- You want **one credit wallet and one content policy** across a mixed-model shoot.
- The user explicitly names Higgsfield, Soul, DoP, or Cinema Studio.

**Go direct to the model provider instead when:**
- You need a model capability, tier, or region that Higgsfield doesn't expose, or the **newest model version lands at the source first** (aggregators lag).
- You need **provider-grade API SLAs, rate limits, or enterprise terms** — Higgsfield's own API surface is narrower and younger than Google's/Kling's (see "API surface").
- **Unit economics at scale** matter and the aggregator's credit markup exceeds the provider's direct price. Aggregators bundle convenience into the credit price; a high-volume pipeline on a single model is often cheaper direct.
- You need a **data-handling posture** Higgsfield's terms don't offer (Higgsfield may use inputs/outputs to train its models on some plans — see "Rights, consent, and data").

**Heuristic:** Higgsfield wins on *breadth, iteration speed, and cinematic control* for one-off and small-batch creative work. Direct providers win on *depth, latest versions, throughput, and contractual control* for production pipelines locked to one model.

## The model lineup (verified 2026-07-10 — re-check the in-app picker)

### Video models fronted by Higgsfield

| Model | In-house or third-party | What it is documented to be best at | Key limits noted by first-party comparison |
|---|---|---|---|
| **Kling 3.0** | Third-party (Kuaishou) | Photorealism, character-driven stories, multi-shot storyboarding (up to ~6 camera cuts in one pass), 4K, native voice binding across languages. **Most credit-efficient of the premium set.** | Requires shot-by-shot setup; 4K and longer clips cost more credits. Up to ~15s. |
| **Kling 2.6** | Third-party | The "proven engine" for fast, stable, consistent character animation. Fallback when 3.0 drifts. | — |
| **Kling o1** | Third-party | Reasoning model for complex, multi-layered scene composition. | Newer/slower. |
| **Seedance 2.0** | Third-party (ByteDance) | **Native audio-video**: synced lip-sync, SFX, and music planned together from up to ~9 reference inputs; physics-aware motion (cloth, liquid, collisions); multi-shot films/ads. | Highest credit cost of the tested set; strict content moderation; ~15s max, 720p on entry, 4K on higher tiers. |
| **Veo 3.1** | Third-party (Google) | Atmospheric/outdoor scenes, global illumination, weather, wind, depth of field; crisp 4K; strong color grade. | Credit-intensive; documented to *soften on tight human-face close-ups*. |
| **Wan 2.7** | Third-party (Alibaba) | Video-reference **style transfer / restyle** existing footage without re-filming; product shots; native audio + lip-sync. | Depends heavily on a supplied reference clip; weak at pure text-to-video. |
| **MiniMax (Hailuo 2.3)** | Third-party | Fast short-form iteration, stylized/anime looks, sharp on-screen text, color/style stability. | Trades cinematic depth for speed; not for 4K finals. |
| **Sora 2** | Third-party (OpenAI) | Deep world simulation, object permanence, physics. | **Being retired.** OpenAI wound Sora down: web/app off ~2026-04-26; Sora API scheduled off ~2026-09-24. Treat as unavailable for new production; migrate prompts to Seedance 2.0 or Veo 3.1. (Reported; verify current status.) |

### In-house control layer

- **Soul / Soul 2.0** — Higgsfield's high-fidelity **image** model. Ships 20+ built-in style presets (editorial, high-fashion, Y2K street, warm ambient, etc.). This is the still-image engine that feeds image-to-video shots.
- **Soul ID** — a trained **character-identity layer** (see "Soul ID" section).
- **DoP (Director of Photography)** — an **image-to-video** engine built around 100+ camera-motion presets baked into the model (see "DoP camera presets"). Exposed on third-party API resellers as `dop-lite` / `dop-preview` / `dop-turbo`.
- **Popcorn** — editing/inpaint model for fixing details.
- **Cinema Studio (3.x / 3.5)** — the multi-shot filmmaking suite that orchestrates image models, video models, camera rig controls, reusable Elements, and an AI co-director in one project (see "Cinema Studio").

### Supporting image models available in the same workspace
Seedream 4.x (up to 4.5 at 4K on top tiers), Flux.2 Pro, Nano Banana / Nano Banana Pro, GPT Image. These matter for video because most cinematic Higgsfield workflows are **image-first**: generate a hero still in Soul/Seedream, lock identity with Soul ID, then animate with DoP or a video model.

## Model selection: a decision framework

Pick the model from the *job*, not from a favorite. (Synthesized from first-party model comparison, 2026-07-10.)

- **Multi-shot narrative that needs synced dialogue/SFX/music** → **Seedance 2.0** (audio and picture planned together). Budget for its high credit cost.
- **Character-driven story, consistent faces/voices, on a budget** → **Kling 3.0** (most credit-efficient premium model; multi-cut storyboarding; voice binding).
- **Wide landscapes, weather, atmosphere, golden-hour exteriors** → **Veo 3.1**. Avoid it for tight face close-ups.
- **Restyle or "reshoot" existing footage without re-filming** → **Wan 2.7** (video-reference style transfer). Always supply the reference clip.
- **Fast daily short-form, drafts, stylized/anime, on-screen text** → **MiniMax / Hailuo**.
- **Precise cinematic camera moves from a single hero still** → **DoP** presets, or **Cinema Studio** for a full rig.
- **A whole multi-shot scene with continuity of characters/locations** → **Cinema Studio**, which can route individual shots to the model that fits each.

**Production heuristic — "draft cheap, finish expensive":** iterate composition, timing, and prompt in a low-cost model (Kling, MiniMax) until the beat works, then spend premium credits (Seedance, Veo) only on the final render. This is the single biggest credit-saver on the platform.

## Soul ID — character consistency (verified 2026-07-10)

Soul ID is Higgsfield's answer to character drift. It is a **trained identity layer**, not a per-prompt trick.

- **How to create one (documented):** upload **20+ photos** of one person → train (~3–5 minutes) → name it → select it when generating in Soul 2.0.
- **Reference quality beats quantity:** recent photos (within ~4–5 months), well lit, no sunglasses/heavy shadow, varied angles and expressions, and at least one full-height shot for body proportion.
- **What it does:** locks facial identity across style presets, lighting, camera angle, and prompt, so you *direct through preset choice* instead of fighting the model.
- **Documented limitations:**
  - It is primarily an **image** system; a trained Soul ID stabilizes the *stills* you then animate. Carrying identity into motion happens by animating those consistent stills (image-to-video), not by a separate "video Soul ID." (First-party pages document image use; treat any "identity in raw text-to-video" claim as unverified.)
  - Identities **stay inside Higgsfield's ecosystem** — not exportable.
  - Works best for **real people**, less so for invented characters.
  - Extreme style shifts or unusual angles can still introduce minor drift.

**Workflow pattern (heuristic):** train Soul ID → generate hero stills with locked identity (vary via presets) → optionally set them as first/last frames → animate in a video model (Kling for character work) or DoP for a camera move. This keeps the face stable through the whole shot instead of hoping a text-to-video model reinvents it consistently.

## DoP camera presets — the distinctive motion library (verified 2026-07-10)

`DoP` is an image-to-video model **trained on camera movement itself**, so a preset like "Dolly Zoom" produces the actual move rather than hoping a text prompt describes it. Higgsfield markets **100+ presets**. Named examples from documentation include:

- **Moves:** Dolly Zoom, 360 Orbit, Truck Left / Truck Right, Push to Glass, Head Tracking, Crane Up / Crane Down, Pan Left / Pan Right, Tilt Up / Tilt Down.
- **Look/optics:** Anamorphic Flares, Film Stock, Depth-of-Field Control.
- Plus ~90 more not individually enumerated in first-party marketing (verify the live library; well-known Higgsfield presets discussed by practitioners include Crash Zoom, Bullet Time, FPV drone, and Robo Arm — treat un-sourced preset names as *to-verify* rather than fact).

**How to use (heuristic):** supply the hero still, pick a preset, set motion strength (0–1 on the API), and let the preset own the camera language — keep the text prompt for *subject and scene*, not for redundant camera description. Stacking too many conflicting moves fights the preset.

## Cinema Studio — the multi-shot rig (Cinema Studio 3 documented ~2026-03/04; verified 2026-07-10)

Cinema Studio is Higgsfield's flagship for directed, multi-shot work. Documented capabilities:

- **Virtual camera physics:** choose a **camera body** (6 professional bodies, from modular 8K digital to 16mm film), a **lens** (11 cinema lenses incl. anamorphic, macro, vintage prime, tilt), **focal length** (8mm ultra-wide → 85mm portrait), and **aperture** (f/1.4 shallow, f/4 balanced, f/11 deep) for real depth-of-field control.
- **Per-shot duration:** assign each shot **1–12 seconds** so you edit pacing before rendering.
- **Reusable Elements:** up to **~9 reference images** combining characters and locations to establish a consistent visual world across shots.
- **AI co-director:** a cinematic-reasoning engine — "describe what should happen; the model figures out how to shoot it" — so full rig control is optional, not required.
- **Model routing:** Cinema Studio can call the image and video models across the platform, picking per shot; it produces synced audio and character consistency across a sequence.
- **Format:** HD standard, cinematic **21:9** supported, 16-bit cinematic-grade output; 4K depends on the underlying model and tier.

**When to reach for Cinema Studio vs. a single model call:** use it when you need *continuity across multiple shots* (same character, same location, controlled pacing). For a single hero clip, a direct model call or DoP preset is faster and cheaper.

## Prompt strategy per underlying model (heuristics, grounded in first-party model notes)

Because the aggregator inherits each model's behavior, prompt *for the model that will run the shot*:

- **Seedance 2.0:** feed it multi-modal references (up to ~9: images, video, audio) and describe the *whole beat* — action, dialogue intent, and sound — since it plans picture and audio together. Lean on it for lip-sync and physics.
- **Kling 3.0:** define **shot sizes, perspective, and character voices upfront**; supply reference images for face/voice consistency; storyboard the cuts you want (it can produce several in a pass).
- **Veo 3.1:** write **longer, environmental** prompts — lighting direction, weather, wind, spatial relationships. Don't rely on it for intimate face close-ups.
- **Wan 2.7:** **always** supply a reference clip/image; describe the *style change*, not the base motion (the motion comes from the reference).
- **MiniMax / Hailuo:** keep prompts **short and clear**; fast mode rewards sparse direction.
- **DoP / Cinema Studio:** let presets/rig own the camera; reserve text for subject and scene.

**Model-agnostic drafting (heuristic):** with models being added and retired (Sora's exit is the cautionary case), keep prompts portable — describe subject, action, camera, and mood in structured plain language rather than model-specific incantations, so a shot can be re-run on a different model when one is deprecated or a cheaper one suffices.

## Credit economics (verified 2026-07-10 — pricing is volatile; confirm on higgsfield.ai/pricing)

Higgsfield bills by **credits**, allocated per subscription tier. **Exact tier names and prices differ between Higgsfield's own pages and third-party trackers and change often** — the numbers below are a dated snapshot; verify live before quoting.

- **Tiers (snapshot, ~Q2 2026):** an entry tier around **$5/mo (~70 credits)**; a **Plus** tier around **$39/yr–$49/mo (~1,000 credits/mo)**; an **Ultra** tier around **$99/yr–$129/mo (~3,000 credits/mo, scalable toward 9,000)**; plus **Business/Team** (per-seat, ~$62–$71/seat with a seat minimum) and custom **Enterprise**. (Some trackers list a "Starter $15" instead of "$5" — treat tier names as unstable and read the live page.)
- **Credits do not roll over** month to month.
- **Top-up packs:** ~**$5 per 100 credits**, reported to **expire ~90 days** after purchase.
- **"Unlimited" access is mostly image-side and time-boxed:** Plus and higher have included 365-day unlimited access to *select image tools* (e.g., Soul 2.0 & Cinema, Seedream variants, Flux.2 Pro, Nano Banana, GPT Image) and short (~7-day) unlimited windows on select models. **Ultra (annual)** has added unlimited **Kling 3.0** video access and 4K Seedream. Read "unlimited" carefully — it is model-specific and plan-specific, not a blanket unlimited-video promise.

**Per-generation credit costs vary by model, resolution, and duration.** Dated sample rates (verify in-app, they change):
- Kling 3.0 720p: ~**6–7 credits** per 5-second clip (cheapest premium video).
- Seedance 2.0 720p: ~**25 credits** per 5-second clip (~**90 credits** per 15-second clip).
- Veo 3.1 (with audio, 720p): ~**40–70 credits** per clip (one tracker cites ~58 credits per 8-second Veo clip).
- Nano Banana Pro image: ~**2 credits** per image.

**Budgeting heuristic:** estimate a shoot as (number of *final* renders × premium per-clip cost) + (drafts × cheap per-clip cost). Because credits expire and don't roll over, buy for the month you'll actually produce in, and do all cheap iteration before spending premium credits.

## API surface — verify carefully, it is partial (verified 2026-07-10)

Be precise and honest about what exists; this is where confident overstatement is easy.

- **Official Higgsfield Cloud API:** there is a first-party cloud/API product at **cloud.higgsfield.ai** with API-key auth (`Authorization: Bearer …`; SDK env vars `HF_KEY` or `HF_API_KEY`/`HF_API_SECRET`) and an **official Python SDK** (`higgsfield-ai/higgsfield-client`, sync + async, submit/wait, polling, callbacks, file uploads). **Caveat:** the SDK's *documented examples emphasize text-to-image* (e.g., a Seedream `text-to-image` model id). Treat the video side of the official API as **present but under-documented** — confirm the exact video endpoints and model ids in the live cloud dashboard rather than assuming parity with the web app's model picker.
- **Third-party resellers/gateways** also expose Higgsfield capability — notably **Pixazo**, **Segmind**, **VideoGenAPI**, and Make integrations. Example (Pixazo gateway): a single `POST /v1/image-to-video` with model variants **`dop-lite`** (~$0.14/5s), **`dop-turbo`** (~$0.42/5s), **`dop-preview`** (~$0.57/5s), taking a prompt, seed (1–1,000,000), **motion preset id + strength (0–1)**, input image URL(s), optional end-frame for interpolation, and an NSFW-detection toggle. These are **not** first-party Higgsfield pricing and add a reseller markup; label them as third-party when you rely on them.
- **Practical guidance:** for programmatic use, start from the official cloud dashboard and SDK; verify each model id and mode against the live docs; and if a specific video model isn't in the official API yet, either use the web app / Cinema Studio for that model or reach the underlying provider (Kling/Google/ByteDance) directly. Do not promise API access to a model without confirming it exists in the official API on the day of the task.

## Rights, consent, and data (verified 2026-07-10 — read the live Terms before advising a client)

- **Ownership / commercial use (documented):** Higgsfield does not claim ownership of inputs or outputs. On **paid plans** you retain full ownership and commercial rights to generated files. On the **Free plan**, Higgsfield retains a non-exclusive license to use your generated content for platform promotion and model improvement.
- **Model training on your content (documented):** inputs and outputs *may be used by Higgsfield to train/improve its models* and for marketing — significant for confidential or client-sensitive material. If a client needs their footage kept out of training, this is a reason to check the current plan's terms or go direct to a provider with a no-training/enterprise posture.
- **Real people, deepfakes, consent (documented policy):** you may upload reference images of a real person **only with their consent**, and Higgsfield's terms require you to **confirm consent at upload**. Prohibited: content that impersonates or misleadingly depicts real, identifiable individuals without consent; deceptive "they said/did this" fabrications; unauthorized celebrity likenesses. Permitted: yourself, consenting employees, or licensed stock-model images.
- **Agent obligations (heuristic, enforce these):**
  1. Before generating with any real-person reference, **confirm the user has rights/consent**; if they can't, decline the real-person elements and offer AI-generated or licensed alternatives.
  2. Warn when a task implies a **deceptive** use of a real person (fake statements/events) — that's against policy and likely against law.
  3. Flag the **training-on-inputs** term for confidential/branded material, and flag that **Free-plan** outputs carry a promotional license (so client work should be on a paid plan).
  4. Never advise entering payment or account credentials into anything; direct the user to Higgsfield's own billing UI.

## Quality-review checklist (heuristic)

Judge output against the *model that produced it* and the brief:

- **Identity:** does the face/body match the Soul ID or reference across the whole clip? Check the last frame, not just the first — drift shows late.
- **Motion coherence:** limbs, hands, and object permanence hold up? (Sora's strength was physics; its replacements vary — Seedance is strong on physics, Veo softer on faces.)
- **Camera:** did the intended DoP preset / rig move actually happen and stay motivated, or did the model fight it?
- **Audio (Seedance/Wan/Veo):** lip-sync locked? SFX/music appropriate and synced? For silent models, plan audio in post.
- **Resolution/format:** delivered at the tier/model's real max (don't promise 4K on a model/tier that caps at 720p).
- **Continuity (Cinema Studio):** characters, locations, lighting, and pacing consistent shot-to-shot?
- **Policy:** any real-person likeness cleared? Any deceptive framing to remove?
- **Cost sanity:** was this render worth premium credits, or should the beat have been drafted cheaply first?

## Complete example (labeled example, not a required formula)

**Production intent:** a 20-second, three-shot brand teaser for a fictional founder "Mara," delivered in 16:9, with consistent face across shots and a synced voiceover line in the final beat.

**Platform/model plan:**
1. **Soul ID:** train "Mara" on 24 clean, recent, varied photos incl. one full-height (train ~4 min).
2. **Hero stills:** in Soul 2.0, generate 3 identity-locked stills (office, street, close-up) via style presets — *draft here, it's image-cheap*.
3. **Shot A & B (camera + no dialogue):** animate the office and street stills with **DoP** presets (A: "Push to Glass"; B: "360 Orbit"), motion strength ~0.5, keeping the text prompt on subject/scene only. Draft on `dop-lite`-class settings, finish one notch up.
4. **Shot C (dialogue):** the close-up needs synced speech → run it on **Seedance 2.0** (native audio) with the Mara still as reference plus the VO line; budget ~25 credits for a 5s 720p render, more for 4K.
5. **Assemble** the three shots in Cinema Studio (or an external editor) at 16:9; set per-shot durations (~6s/8s/6s).

**Why structured this way:** identity is locked *before* motion (Soul ID → stills → animate), so faces don't reinvent per shot; camera moves come from DoP presets rather than fragile prompt phrasing; the *only* premium-audio spend is the one shot that needs lip-sync (draft-cheap/finish-expensive).

**Expected result:** consistent-face teaser with two clean camera moves and one synced-dialogue beat.

**Likely failure modes:** face drift on Shot B's orbit (fix: stronger/more varied Soul ID training set, or set the still as first frame); Veo-style face softening if you'd used Veo for the close-up (Seedance was chosen deliberately); over-spend if Shot C is re-rendered at 4K repeatedly (lock timing at 720p first).

**Variations:** swap Wan 2.7 for Shot C if you have real footage of a presenter to *restyle*; use MiniMax for a rapid social cutdown; use Cinema Studio's Elements + AI co-director end-to-end if you need more than three shots with strict continuity.

## Sources (accessed / verified 2026-07-10)

First-party (Higgsfield):
- AI Video hub — https://higgsfield.ai/ai-video
- First-party model comparison — https://higgsfield.ai/blog/5-Best-AI-Video-Models-2026-Tested-Compared
- Cinema Studio product — https://higgsfield.ai/cinematic-video-generator and https://higgsfield.ai/blog/cinema-studio-3
- Soul ID — https://higgsfield.ai/blog/Soul-ID-AI-Character-Consistency
- Pricing — https://higgsfield.ai/pricing
- Terms of Use — https://higgsfield.ai/terms-of-use-agreement ; Trust & Safety — https://higgsfield.ai/trust
- Official Cloud API — https://cloud.higgsfield.ai/ ; Python SDK — https://github.com/higgsfield-ai/higgsfield-client

Secondary (disclosed-method reviews / third-party API resellers — labeled as secondary):
- Pricing snapshot — https://www.imagine.art/blogs/higgsfield-ai-pricing
- DoP preset list — https://kolbo.ai/blog/higgsfield-suite-100-camera-presets
- Cinema Studio rig detail — https://vidpros.com/higgsfield-cinema-studio/
- Third-party API (reseller) — https://www.pixazo.ai/models/higgsfield ; https://apidog.com/blog/higgsfield-api/

Volatile facts (model lineup/versions, prices, credit costs, API endpoints, Sora retirement dates) are dated 2026-07-10 and must be re-verified against live first-party pages before production or client-facing use.
