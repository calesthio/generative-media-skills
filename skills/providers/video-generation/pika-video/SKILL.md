---
name: pika-video
description: >-
  Produce short-form video with Pika (pika.art) — its effect-driven tools
  (Pikaffects, Pikadditions, Pikaswaps, Pikaframes, Pikascenes, Pikatwists) and
  audio-driven lip sync (Pikaformance), plus text-to-video and image-to-video.
  Use when a task calls for playful, stylized, meme-able social clips, or for
  applying generative effects and object swaps to real uploaded footage, and
  when deciding whether Pika is the right engine versus a higher-fidelity model.
  Covers model versions, credit/plan economics, the fal.ai API route, prompt
  construction, iteration/repair, capability limits, and consent/rights rules
  for uploaded real-person media. Not a general "best video model" chooser.
---

# Pika video generation

Pika (the company was branded "Pika Labs" during its Discord beta; the product
and domain are now **pika.art**) is a generative-video platform whose distinctive
value is **effect-driven, short-form, stylized clips** and **generative edits to
real footage**, not photoreal long-form filmmaking. Treat this skill as the guide
for choosing Pika, driving its specific tools, and knowing when to route elsewhere.

All volatile facts below (model names, prices, credits, limits, feature
availability) were **verified 2026-07-10** against the cited sources. Pika ships
frequently; re-verify version and pricing before quoting them to a user.

## When to use Pika vs. something else

**Reach for Pika when the job is** (production heuristic):

- Playful / meme / social short-form: TikTok, Reels, Shorts, ad-grade hooks.
- Applying a **transformation effect** to an existing image or clip — inflate,
  melt, explode, squash, crush, "cake-ify," etc. (Pikaffects). This is Pika's
  signature and is hard to reproduce cleanly elsewhere.
- **Editing real footage generatively**: adding an object/character into a clip
  (Pikadditions), or swapping an object/background while preserving motion and
  lighting (Pikaswaps).
- **Keyframe transitions / morphs** between 2–5 stills (Pikaframes).
- **Talking-avatar / lip sync** from a still + audio (Pikaformance).
- Fast iteration where a stylized 5–10s clip at 720p/1080p is the deliverable.

**Route to a higher-fidelity model instead when the job needs** (heuristic):

- Photoreal humans holding identity across a longer take, accurate hands, or
  legible on-screen text baked into the render.
- Sustained (multi-take, >~25s) coherent narrative from a single generation.
- Rigorous physical simulation (fluids, crowds, reflections) at documentary
  fidelity.

In those cases Pika will often "invent" motion badly, drift faces, or garble
text. Named competitors change too fast to rank here; the decision rule is the
capability profile above, not a fixed leaderboard.

## Current models and what powers each tool

Verified against the official plan page and feature descriptions, 2026-07-10.

- **Pika 2.5** — the current flagship engine for text-to-video and
  image-to-video, and the engine behind most tools. Paid plans unlock all
  resolutions; the free plan is limited to **480p** on Pika 2.5.
  [pika.art/pricing]
- **Pika 2.2** — still the engine specifically behind **Pikascenes**
  (multi-image "ingredients" composition) and available for Pikaframes.
  [pika.art/pricing]
- **Turbo / Pro** model variants — used for the editing tools
  (Pikadditions, Pikaswaps, Pikatwists); "Pro" variants on paid tiers give
  higher quality than the free "Turbo" path. [pika.art/pricing]
- **Pikaformance** — a **separate audio-driven performance model** for lip sync
  and facial performance, distinct from the scene models.

Caveat (source-quality flag): several third-party blogs assert a "Pika 2.3,"
"Pika 3.0," or "v3" and attach specific claims (e.g., integrated automatic sound
effects, near-perfect text rendering). **None of those version numbers appear on
pika.art's own pricing/feature surfaces as of 2026-07-10**; treat "3.0" claims as
unverified marketing until confirmed first-party. Quote **Pika 2.5** as the
current flagship and re-check before promising newer-version behavior.

## The distinctive feature set (what each tool actually does)

Terminology and behavior below; treat the mechanics as documented facts from
Pika's own feature pages and consistent third-party reporting (2026-07-10).

- **Pikaffects** — one-click physics-style transformations applied to a subject.
  Documented effects include Inflate, Melt, Explode, Squash, Crush, and
  "Cake-ify," among others. Input is usually an image (image-to-video); the
  effect is the whole point of the clip. Free tier gets Pikaffects only on the
  image-to-video path.
- **Pikadditions** — video inpainting/insertion: upload a short clip plus a
  reference image of a new element (object, character), and Pika composites it
  into the scene matching lighting, shadow, and motion. Good for "put this
  product/character into my footage."
- **Pikaswaps** — targeted replacement: select/brush an object, character, or
  background in an existing video and replace it (via prompt or reference image)
  while camera move, motion, and lighting are preserved across frames.
- **Pikaframes** — keyframe transition generator: supply **2–5 images** (start /
  middle / end frames) and Pika generates the in-between motion and camera moves.
  On fal, total duration can chain up to **25s** across transitions.
- **Pikascenes** — build one shot from multiple **"ingredients"** images
  (character, outfit, prop, environment); the model figures out each reference's
  role and composes them into a coherent scene. This is the successor concept to
  earlier "Scene Ingredients" language, and it is the strongest lever for
  **character/asset consistency** in Pika.
- **Pikatwists** — appends a surprise/plot-twist change near the end of a clip
  (e.g., "scene ends with the character floating into space") for meme or
  story-punchline payoff.
- **Pikaformance** — audio-driven lip sync and performance from a still face plus
  an audio file (speech, singing). First-party framing emphasizes fast,
  expressive results; use a clean, front-facing, well-lit face and clean audio.

## Capability limits (verify per generation)

Documented / consistently reported, 2026-07-10:

- **Duration**: native clips are typically **5–10s**; **scene extension** and
  **Pikaframes** chaining push effective length toward **~25s**. Do not promise
  minute-long single takes.
- **Resolution**: up to **1080p**; tiers are 480p / 720p / 1080p. Free = 480p.
- **Aspect ratios** (documented for the 2.2-era pipeline): 16:9, 9:16, 1:1, 4:5,
  5:4, 3:2, 2:3 — covers YouTube, TikTok/Reels/Shorts, and square/portrait feeds.
- **Realism ceiling**: strong at stylized/animated looks and effects; weaker at
  sustained photoreal human identity, hands, and baked-in text.

## Access routes

- **Web app** — pika.art (primary authoring surface; all tools).
- **iOS app** — Pika's mobile/social app (some tools, feed-style creation).
- **Discord** — community; the historical beta ran here. Legacy `-flag` prompt
  syntax (below) originated in the Discord bot.
- **API** — **there is no first-party Pika REST API as of 2026-07-10.** Pika's
  own `pika.art/api` page **directs developers to fal.ai**, which hosts Pika
  models as endpoints. Label this to users clearly: it is an
  **officially-pointed-to third-party host (fal.ai)**, not a Pika-operated API.
  - fal exposes **Pika 2.2 text-to-video, image-to-video, Pikascenes, and
    Pikaframes**.
  - fal does **not** expose **Pikaffects, Pikaformance (lip sync), or sound
    effects** — those are web/app-only. If a user needs Pikaffects in an
    automated pipeline, that is currently not possible via API.
  - fal pricing (2026-07-10): **Pikaframes** $0.04/s at 720p, $0.06/s at 1080p,
    5-billable-second minimum ($0.20 / $0.30). **Pikascenes** ~$0.20 for a 5s
    720p clip. fal uses its own API keys and per-request billing.
  - Other resellers exist (e.g., generic "Pika API" gateways). Label any of
    these as **unofficial** unless the user is specifically on fal.

## Pricing and credit economics

From **pika.art/pricing, verified 2026-07-10** (annual-billing prices shown; the
plan page states these unlock levels). Credits are consumed per generation and
scale with resolution and length.

| Plan | Price (annual) | Monthly credits | Model access | Watermark | Commercial |
|------|----------------|-----------------|--------------|-----------|------------|
| Free | $0 | 80 | Pika 2.5 **480p only**, Pikascenes, Pikadditions, Pikaswaps, Pikatwists, Pikaffects (image-to-video only) | Yes | No |
| Standard | $8/mo | 700 | Pika 2.5 (all res), Pikaframes, Pikascenes, Pikadditions, Pikaswaps, Pikatwists, all Pikaffects; fast | No | Yes |
| Pro | $28/mo | 2,300 | Same tools, faster generation, "Best value" | No | Yes |
| Fancy | $76/mo | 6,000 | Same tools, fastest generation | No | Yes |

- **Credit sizing** (third-party-reported example, treat as approximate and
  verify in-app): a 720p 5s text-to-video ≈ **20 credits**; a 1080p 10s clip ≈
  **80 credits**. So Pro's 2,300 credits is on the order of dozens of 1080p
  clips per month. Do not quote exact per-clip credit costs as fact without
  checking the live generator, which prices each job before you spend.
- **Watermark and commercial rights**: the **free/Standard split matters** — free
  outputs are watermarked and **not licensed for commercial use**; paid plans
  remove the watermark and grant commercial rights. Flag this before any client
  work.
- Paid plans support buying additional / rollover credits.

## Prompt construction

Heuristics (practitioner-reported, corroborated across multiple guides; treat as
guidance, not a formula):

- **Structure**: subject → action → setting → style → camera → lighting. Keep it
  a clear single beat: *what is in frame, what it does, how it's shot.*
- **Specific-but-lean beats overloaded.** Stacking many contradictory styles
  ("hyper-real, anime, Pixar, Ghibli, cyberpunk, watercolor, cinematic") degrades
  results. Fewer, more precise words win.
- **Motion is the deliverable.** State the one motion you want. If the motion is
  ambiguous, Pika invents it, often badly. Prefer **gentle camera moves** (slow
  push in/out, gentle pan) over wild orbits, especially around faces.
- **Stabilize faces**: "soft frontal light" / "even studio lighting," minimal
  camera movement around the head. This reduces identity drift.
- **Do not rely on baked-in text.** Legible signage/labels are unreliable; add
  critical text in post (an editor or a caption/overlay tool) rather than
  prompting it into the render.
- **Legacy Discord flags** (`-camera`, `-motion`, `-fps`, `-ar`, `-neg`) come
  from the older Discord bot. In the modern web app these are **UI controls
  (sliders / pickers), not text flags** — do not paste `-camera zoom` into the
  web prompt box and expect it to parse. Know both so you can read old guides
  correctly.

## Iteration and repair

- **Re-roll, then simplify.** If a generation drifts or mangles motion, the first
  move is to **reduce complexity** — fewer subjects, simpler background, one clear
  motion — before adding more prompt words.
- **Control the first frame.** For a specific look, generate a strong still in an
  image model (or upload one) and use **image-to-video / Pikascenes** rather than
  pure text-to-video. This constrains composition and identity far better.
- **Consistency across a series**: reuse the **same reference images**
  (Pikascenes ingredients) for a recurring character/prop across clips.
- **Extend length** via **Pikaframes** (feed the last frame as the next start
  frame) or scene extension, instead of asking for one long generation.
- **Fix a bad element in real footage** with **Pikaswaps** (replace it) or
  **Pikadditions** (add what's missing) rather than regenerating from scratch.
- **Failure-mode triage**: face morph → stabilize lighting + cut camera motion;
  flicker → newer engine (2.5) + shorter clip; bad hands/text → hide, crop, or
  add in post; chaotic motion → lower intensity, simplify scene.

## Safety, consent, and rights (uploaded real-person footage)

Pika's **Acceptable Use Policy** (pika.art/acceptable-use-policy) includes a
dedicated "Use of Photographs or Portraits" section and consent/disclosure
requirements. Documented rules (verified 2026-07-10):

- **You may only upload photographs/portraits that are your own or for which you
  have explicit consent** and the necessary rights.
- **Do not generate content depicting identifiable real individuals without their
  consent.** Uploading someone's photo to animate it, or prompting a specific real
  person, without permission violates the policy and can carry legal exposure.
- No harmful impersonation or deceptive content; the user is **solely responsible
  for all inputs and outputs**, including their legality and appropriateness.

Operating rules for an agent using this skill:

- Before animating a real person's face (very relevant to **Pikaformance** lip
  sync and to **Pikadditions/Pikaswaps** on real footage), confirm the user has
  rights/consent. Do not proceed with a named public figure or an
  ambiguously-sourced face on the user's say-so alone; surface the consent
  requirement.
- Treat likeness, voice, minors, and trademarked/branded content as consent- and
  rights-gated. Refuse or flag deceptive/impersonation intent.
- Remember the **commercial-use gate**: free-tier outputs are watermarked and not
  licensed for commercial use — do not hand a free-tier clip to a paying client.

## Output review criteria

Check a Pika clip against: (1) **the intended motion actually happens** and reads
cleanly; (2) **no identity drift** on faces across the clip; (3) hands, text, and
fine detail are either correct or deliberately hidden; (4) the **effect landed**
(for Pikaffects/Pikaswaps/Pikadditions the edit should be seamless — matched
lighting/shadow, no ghosting at the swap boundary); (5) **aspect ratio and
resolution** match the target platform; (6) **watermark/licensing** matches the
usage (paid tier for anything commercial); (7) length is within the honest
range (don't sell a padded/looped clip as a native long take).

---

### Example A — signature Pikaffect for a social hook (labeled example)

*Intent*: a scroll-stopping 5s TikTok clip of a product "cake-ify" gag.
*Route*: pika.art web app, Pikaffects, image-to-video. *Input*: a clean product
photo on plain background. *Steps*: upload image → choose Pikaffects → select
**Cake-ify** → 9:16 → 720p → generate. *Prompt (kept minimal)*:
"the sneaker slowly reveals it is made of cake, a knife slices through."
*Why*: the effect is the payload; overloading the prompt with style words would
fight the effect. *Expected*: a satisfying transformation reveal. *Failure modes*:
messy slice geometry or warped logo — reroll, or crop out the mangled area.
*Variation*: swap Cake-ify for Explode/Inflate for a different punchline.
*Note*: Pikaffects is **web/app-only**, not available on the fal API — plan the
workflow accordingly.

### Example B — consistent character across a 3-clip series (labeled example)

*Intent*: three 8s clips of the same original mascot in different settings.
*Route*: Pikascenes (ingredients) on Pika 2.2. *Inputs*: one clean character
sheet image + per-scene setting reference. *Method*: reuse the **same character
ingredient image** in every generation; vary only the environment ingredient and
the action line. *Prompt pattern*: "[character] [one clear action] in [setting],
soft even lighting, slow push-in." *Why*: reusing the ingredient is the main
lever for identity consistency; a slow push-in minimizes drift. *Expected*:
recognizably the same character across clips. *Failure modes*: outfit/color drift
between clips — tighten the reference and avoid fast camera moves. *Then*: stitch
in an editor; add any on-screen text in post, not in-model.

### Example C — API-driven keyframe morph at scale (labeled example)

*Intent*: batch of brand transition stings from 2 stills each.
*Route*: **fal.ai** `fal-ai/pika/v2.2/pikaframes` (the officially-pointed-to
host; **not** a first-party Pika API). *Inputs*: 2–5 image URLs per job, optional
per-transition prompt, target resolution. *Cost*: 720p ≈ $0.04/s (5s min → $0.20);
1080p ≈ $0.06/s (→ $0.30); up to ~25s total across transitions
(fal, 2026-07-10). *Why fal*: automatable and cheap per clip. *Constraint to flag
to the user*: Pikaffects, Pikaformance lip sync, and sound effects are **not**
exposed on the API — if those are required, the job must run in the web app.

## Sources (verified 2026-07-10)

- Pika subscription/plan and feature-tier page — https://pika.art/pricing
- Pika API landing (redirects developers to fal.ai) — https://pika.art/api
- Pika Acceptable Use Policy (photographs/portraits, consent) — https://pika.art/acceptable-use-policy
- fal.ai Pika v2.2 Pikaframes model (API params, pricing) — https://fal.ai/models/fal-ai/pika/v2.2/pikaframes
- fal.ai Pika v2.2 Pikascenes model — https://fal.ai/models/fal-ai/pika/v2.2/pikascenes
- Pika 2.2 release / Pikaframes & aspect-ratio reporting — https://www.aibase.com/news/15808
- Feature descriptions (Pikadditions, Pikaswaps, Pikascenes, Pikatwists, Pikaformance, lip sync) corroborated across third-party guides, e.g. https://pikaais.com/tools/ and https://pika-art.net/scene-ingredients/ (third-party; treat feature names as documented, specific numeric claims as approximate)
- Prompting/limitation heuristics (practitioner-reported) — https://pikaais.com/troubleshooting/ and https://medium.com/@mattmajewski/exploring-pika-labs-the-ultimate-guide-to-creating-amazing-video-clips-cd947e6eee1f

Source-quality note: pika.art pages are first-party and authoritative for
plans/policy. fal.ai pages are authoritative for the API route it hosts.
`pikaais.com`, `pika-art.net`, `pikaslabs.com`, and similar are **third-party**
sites (not Pika-operated); their feature *names* are consistent with Pika's own
surfaces, but their **version numbers (e.g. "3.0") and exact credit/pricing
figures should be treated as unverified** until confirmed first-party.
