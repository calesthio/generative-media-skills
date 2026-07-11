---
name: moonvalley-marey
description: >-
  Produce video with Moonvalley's Marey model family (Marey Realism v1.5) — a
  filmmaker-oriented, 1080p/24fps generative video model marketed as trained
  exclusively on licensed data. Use this skill when a task asks for Marey or
  Moonvalley specifically, when a brief demands brand-safe / legally reviewed AI
  video for commercial or studio work, or when the request needs Marey's
  director-style controls (camera trajectory, motion transfer, pose transfer,
  keyframing, reference conditioning). It covers what "commercially safe" really
  means versus the actual terms of service, access routes (Moonvalley web /
  Voyager, the fal API, ComfyUI), pricing, capability limits, prompt and
  reference strategy, where Marey fits production versus where other models win,
  iteration, and quality review. Do not use it for audio generation, for
  photoreal talking-head dialogue, or as a generic "best video model" default.
---

# Moonvalley Marey

Marey is Moonvalley's generative video model, aimed at professional filmmakers,
studios, and brand teams that need AI video they can put through legal review.
Its differentiator is not raw fidelity — it is **provenance**: Moonvalley
markets Marey as trained exclusively on owned or licensed footage, and pairs it
with a set of director-style controls. This skill helps an agent decide when
Marey is the right tool, use it correctly, and — critically — represent its
legal posture accurately rather than repeating marketing.

Verification date for all volatile facts below: **2026-07-10**. Re-check
version, pricing, endpoints, and the terms of service before relying on any
dated claim.

## Company and model status (verified 2026-07-10)

- **Company**: Moonvalley (moonvalley.com), an "imagination research company."
  Marey was built with the animation studio Asteria. Moonvalley raised an
  additional $84M in July 2025 (investors incl. General Catalyst, CAA, Comcast
  Ventures, CoreWeave, Khosla Ventures, Y Combinator), reportedly ~$154M total.
  The company is active and funded — not shut down or pivoted. [businesswire,
  variety, techcrunch — see Sources]
- **Model**: The publicly available production model is **Marey Realism v1.5**.
  It first entered public availability July 2025 after an earlier limited
  release (March 2025). [techcrunch, fal]
- **Platform**: Moonvalley also markets **Voyager**, a higher-end platform/UI
  that exposes Marey's fuller control set for studio workflows. [businesswire]
- Named after Étienne-Jules Marey, a chronophotography pioneer — a signal of the
  "cinematography-first" brand positioning.

Treat "v1.5" as volatile. Moonvalley has publicly promised further controls
(lighting, deeper object trajectories, character libraries); a newer point
release may exist by the time you read this.

## Documented capabilities and hard limits

These are documented on the fal model pages and Moonvalley/partner docs
(verified 2026-07-10). Distinguish them from marketing claims below.

| Property | Value | Note |
|---|---|---|
| Output resolution | Native 1080p (default 1920×1080) | Trained on native 1080p; other dimensions selectable |
| Frame rate | 24 fps | Cinema-standard cadence |
| Clip duration | 5s or 10s per generation (v1.5 on fal); shot-extension to lengthen | Original 2025 launch capped at ~5s; v1.5 adds 10s + extension |
| Audio | **None** | Marey is silent video only — no native dialogue, SFX, or music. Add audio in post |
| Training content | "Owned or fully licensed," native 1080p, no user-generated content (first-party claim) | See legal section |

Consequences an agent must plan around:

- **No audio track.** Any brief needing lip-synced dialogue or sound must layer
  audio separately (ElevenLabs, a DAW, licensed music). If the brief's value is
  in synced sound, Marey is not the model — Veo 3 generates audio natively.
- **Short clips.** Narrative beats must be built from 5–10s shots and assembled
  in an NLE. Plan a shot list, not a single long generation.
- **1080p ceiling.** For 4K delivery you upscale in post; Marey does not
  natively deliver 4K.

## The licensed-data value proposition — and what the terms actually say

This is the single most important thing to get right, because it is where an
agent most easily misleads a user.

### The first-party claim (label it as a claim)

Moonvalley markets Marey as **"the world's first commercially safe video model
... trained only on licensed, high-resolution footage. No scraped content. No
user submissions."** Reporting indicates roughly **80%** of training footage
came from filmmakers/agencies who intentionally licensed B-roll, with archive
material secured through partnerships (e.g. Vimeo); the remainder from other
owned/licensed sources. This is a **first-party claim about training-data
provenance**, corroborated by press but not independently audited. Present it as
"Moonvalley states / claims," never as an established fact. [moonvalley, cined,
techcrunch]

### Why provenance matters

The plausible legal benefit is at the **input** side: a model trained only on
cleared footage is far less exposed to the training-data copyright suits now
facing scraped-data competitors. For a risk-averse studio or brand, that reduces
one specific category of risk — the "was this model built on my/others' stolen
work" question — and that is a real, defensible reason to choose Marey.

### What "commercially safe" does NOT mean — read the ToS

Do not equate "trained on licensed data" with "you are indemnified." The actual
consumer Terms of Service (help.moonvalley.com, verified 2026-07-10) run the
other way:

- **The user indemnifies Moonvalley**, not the reverse. Users agree to
  "defend, indemnify, and hold harmless" Moonvalley from claims arising out of
  the user's use of the service, their content, or infringement of others'
  rights — including paying defense costs. [moonvalley ToS]
- **Liability is capped** at the greater of **$500** or the amount the user paid.
  Moonvalley disclaims indirect/consequential/special damages. [moonvalley ToS]
- Reporting (TechCrunch, citing a Moonvalley spokesperson) indicates Moonvalley
  provides indemnification **for its data-collection contractors** — not a
  blanket output indemnity to end users. This is materially different from
  **Adobe Firefly**, which offers enterprise customers indemnification for using
  its video model. [techcrunch]
- Moonvalley has said it *intends* to offer a user indemnity policy and
  content-removal/data-deletion options, and it markets bespoke **enterprise /
  studio agreements** (including custom fine-tunes on partners' IP). Any real
  output indemnity for a specific customer would live in a negotiated enterprise
  contract, not the public ToS. [techcrunch, deadline]

**Agent rule:** When a user cites "commercially safe" as a reason to skip legal
review, correct the framing. The honest position is: *Marey lowers
training-data provenance risk and is a strong candidate for brand-safe work, but
the standard terms shift indemnification onto the user and cap liability — so
studios must still run legal review, and any indemnity guarantee must be secured
in an enterprise agreement, in writing.* Never tell a user their Marey output is
"legally cleared" or "guaranteed" on the strength of marketing copy alone.

## Access routes (verified 2026-07-10)

- **Moonvalley web app / Voyager** (moonvalley.com): the first-party product;
  exposes the fullest control set and the credit store.
- **fal API** (`fal.ai/models/moonvalley/marey/...`): programmatic access to
  `t2v`, `i2v`, `motion-transfer`, and `pose-transfer` endpoints. Best route for
  agent automation and pipelines.
- **ComfyUI**: Marey Realism v1.5 is referenced for node-based workflows.
- **Third-party creative platforms**: Marey has appeared via partners
  (e.g. Adobe integrations, Scenario). Availability and feature parity vary;
  verify per platform.

### fal API parameters (v1.5 t2v/i2v, verified 2026-07-10)

- `prompt` (required): descriptive text; **minimum ~50 words recommended**.
- `image_url` (i2v only, required): the starting frame.
- `negative_prompt` (optional): ships with sensible defaults; customizable.
- `seed` (optional): default `9`; use `-1` for random. Fix the seed to iterate
  one variable at a time; randomize to explore.
- `dimensions` (optional): resolution/aspect via dropdown; default 1920×1080.
- `duration` (optional): 5s or 10s.

## Pricing (verified 2026-07-10)

- **fal, per generation**: **$1.50 for 5s**, **$3.00 for 10s**. [fal]
- **Moonvalley web credit packs**: $14.99 / 100 credits, $34.99 / 250 credits,
  $149.99 / 1,000 credits. A 5s request is billed like the $1.50 tier, 10s like
  $3.00. [techcrunch]
- Custom fine-tuning is available to studios (enterprise pricing, not public).

Budget implication: iteration is the real cost. At ~$1.50–$3.00 per attempt and
Marey's inconsistency (below), a single usable 5s shot may take several
generations. Estimate 3–8 attempts per keeper shot when quoting a budget.

## Filmmaker controls (feature names verbatim, verified 2026-07-10)

Marey's pitch is directorial control, not one-shot prompting. Feature names as
Moonvalley lists them:

- **Camera Control** — "Create cinematic camera moves using just a single image."
  Near-360° moves, handheld/dolly simulation.
- **Motion Transfer** — "Pull motion from any reference video and apply it to new
  subjects." Use a reference clip as a motion template; restyle the visuals.
- **Pose Control / Pose Transfer** — drive human movement, gesture, and body
  motion from reference images, videos, or performance inputs.
- **Trajectory Control** — "Draw the path. Define the action." Direct object/
  motion paths.
- **Keyframing** — "Upload multiple reference images and place them on a
  timeline."
- **Reference** — "Use separate reference images for each character or object"
  (per-subject conditioning / character consistency).
- **Shot Extension** — "Seamlessly extend video duration" beyond a single
  generation.
- **Multi-layer spatial composition** — independent control of foreground,
  middle ground, background (Marey is marketed as "3D-aware").

Heuristic: reach for these controls precisely because Marey's blind text-to-video
is inconsistent. Motion transfer and pose transfer replace fragile prompted
motion with a real reference, which is where Marey earns its place — previz,
restyling a plate, or matching a specific camera move.

## Prompt strategy

Marey rewards long, structured, cinematographer's prompts far more than terse
ones. Moonvalley's own guidance recommends **at least ~50 words** and a
layered structure. A documented formula (Moonvalley help center):

> **[Camera movement] + [Scale / perspective] + [Core visual] + [Environmental
> details] + [Lighting / technical specs]**

Practical construction:

1. **Camera first.** Name a concrete move and angle — dolly-in, aerial sweep,
   low-angle push, over-the-shoulder, plunge, orbit.
2. **Scale / perspective.** Anchor size with real-world references (monolith,
   canyon, building) so the model stages depth.
3. **Core visual / action.** The single primary subject and action. Keep it to
   *one* clear action — Marey degrades when asked to juggle multiple
   simultaneous actions or props.
4. **Environment, in layers.** Separate foreground / middle ground / background;
   this plays to the multi-layer composition strength.
5. **Lighting and technical spec last.** Lens (35mm), sensor, film stock, noir
   lighting, motion blur, shallow focus, golden hour.

Negative prompt: keep the shipped defaults and add specific failure terms you
observe (e.g. `warped hands, flicker, morphing, extra fingers, plastic skin`).

Don't: pack a paragraph with several characters each doing different things; ask
for readable text/logos; expect synced lips or spoken words.

## Where Marey fits production — and where other models win

**Choose Marey when:**

- The client is a **brand or studio with legal review** and training-data
  provenance is a gating requirement.
- The shot is a **single-subject, controlled** piece — product hero shot, slow
  aerial/establishing, an environment where motion is minimal, or a stylized/2D
  look that hides temporal artifacts.
- You have a **reference** to drive motion or pose (motion/pose transfer), or a
  **previz** need where directorial control matters more than final fidelity.
- You are combining Marey with its own ecosystem (Voyager controls, keyframing,
  shot extension) rather than expecting one clean text-to-video generation.

**Prefer another model when:**

- The brief needs **native audio / dialogue** → Veo 3.
- The brief needs **sustained, complex, multi-character motion**, crowd
  choreography, or reliable photoreal talking heads → Marey's temporal
  consistency is weak; competitors (Veo, Kling, Seedance, Sora-class) handle
  these more reliably per independent hands-on reviews.
- You need **maximum prompt adherence on the first try** at low cost — Marey's
  adherence is documented as inconsistent, so iteration cost is high.
- Provenance is *not* a requirement and you simply want the best-looking result
  fast.

This is a first-party-claim-vs-independent-review split: Marey's licensing story
is genuinely differentiated, but a hands-on practitioner review (Curious Refuge,
2025) scored its output quality low (~3/10) versus peers, citing temporal
instability, collapsing hands/gestures, flicker on camera moves, and plastic
skin. Treat that as one disclosed-method practitioner report, not a benchmark —
but it aligns with the "brittle under motion" pattern. The honest summary:
**Marey buys legal peace of mind and directorial control, often at a cost in raw
motion fidelity.**

## Iteration workflow

1. **Lock the concept as a shot list**, each shot ≤10s. Marey builds sequences
   from short clips, not long takes.
2. **Storyboard / previz cheaply** with text-to-video, then commit budget.
3. **Fix the seed** and change one variable per generation (prompt clause,
   duration, dimension). Randomize only when exploring fresh directions.
4. **Replace fragile prompted motion with references.** If a camera move or
   gesture won't hold, drive it with motion transfer / pose transfer / camera
   control instead of more adjectives.
5. **Prefer i2v for control.** Generate or source a strong first frame (an image
   model or a real still), then animate it — this pins composition and identity
   far better than blind t2v.
6. **Use keyframing and shot extension** to stitch beats and lengthen usable
   shots rather than regenerating whole sequences.
7. **Finish in post**: upscale toward delivery resolution, color, and add all
   audio. Marey outputs a silent 1080p/24fps plate.

## Quality review criteria

Before accepting a Marey shot, check specifically for its known failure modes:

- **Temporal consistency**: do props/objects persist across the whole clip, or
  vanish/morph? Watch the full duration, not the first frame.
- **Hands and gestures**: fingers and hand articulation are a frequent collapse
  point — scrutinize any gesture.
- **Camera-move flicker**: pans, orbits, and dollies expose jitter/flicker;
  inspect motion segments frame-by-frame.
- **Skin and faces**: check for plastic/waxy skin and mannequin-stiff
  performance in any human shot.
- **Prompt adherence**: did every requested element appear and survive? Multi-
  element prompts commonly drop details.
- **Delivery fit**: 1080p and 24fps — confirm this matches the deliverable spec
  before committing (e.g. a 30fps social spec or 4K broadcast spec needs a plan).
- **Legal**: confirmed brand/likeness/trademark clearance for anything *you*
  fed in (references, first frames) — the licensed-training claim does not cover
  your inputs, and the ToS makes those your responsibility.

## Failure modes and repairs

| Symptom | Likely cause | Repair |
|---|---|---|
| Props/details vanish mid-clip | Overloaded prompt, too many simultaneous elements | Simplify to one core action; use i2v to pin the scene; add missing item to negative-of-absence via reference |
| Warped hands / collapsing gestures | Known weak spot in fine articulation | Avoid tight hand close-ups; use pose transfer with a clean reference; hide hands or keep them still |
| Flicker on camera movement | Motion instability | Use Camera Control from a single image instead of prompted motion; slow the move; shorten the clip |
| Plastic/stiff human performance | Photoreal-dialogue is not a strength | Reconsider model for talking heads; use stylized look; drive performance via pose/motion transfer |
| Weak prompt adherence | Terse or unstructured prompt | Rewrite to ≥50 words in the camera→scale→action→environment→lighting structure |
| Needs sound | Marey is silent | Add audio in post; if synced audio is the point, switch to an audio-native model |

## Examples (illustrative — adapt, do not copy verbatim)

### Example A — brand-safe product hero (Marey's sweet spot)

- **Intent**: 5s hero shot of a perfume bottle for a brand ad going through legal
  review; provenance matters, motion is minimal.
- **Route**: fal `i2v`. Start from a rendered product still to lock the label.
- **Prompt (~55 words)**: "Slow dolly-in, eye-level. A single frosted-glass
  perfume bottle stands like a monolith on wet black stone, foreground droplets
  catching light, soft gradient studio backdrop behind. Warm key from
  camera-left, cool rim light. Shallow depth of field, 50mm lens, gentle motion
  blur, high-contrast luxury lighting, pristine reflections, cinematic product
  photography."
- **Params**: `duration: 5`, `seed: 9` (fixed to iterate), default dimensions.
- **Why**: single subject, near-static, controlled light — plays to strengths;
  i2v pins the label so it doesn't morph.
- **Likely failures**: minor reflection flicker; label text warping if relied on
  the model instead of the input still.
- **Review**: confirm the label stays legible and stable across all 5s; confirm
  the *brand* cleared the still they supplied — the training claim doesn't cover
  their asset.

### Example B — motion transfer for previz (control over fidelity)

- **Intent**: restyle a rehearsal handheld clip into a noir look for a director's
  previz.
- **Route**: fal `motion-transfer` — reference video supplies the camera/subject
  motion; prompt supplies style.
- **Prompt**: describe the target look and lighting only ("noir, hard chiaroscuro
  key, rain-slick street, 35mm, heavy shadow, desaturated") and let the reference
  carry motion.
- **Why**: replaces fragile prompted camera motion with a real move — the
  reliable way to get a specific camera trajectory out of Marey.
- **Failures**: gesture detail may still collapse; keep it a previz, not final.

### Example C — when to say no

- **Request**: "30s photoreal two-person dialogue scene with synced speech."
- **Correct response**: Marey is the wrong tool — no native audio, 5–10s clips,
  and weak photoreal-dialogue consistency. Recommend an audio-native model
  (Veo 3) for the talking coverage, or Marey only for cutaway/establishing plates
  with audio and dialogue built separately. Do not promise a single Marey
  generation can deliver this.

## Sources (verified 2026-07-10)

First-party (Moonvalley / partners):
- Moonvalley product & Marey page — moonvalley.com, /marey (capabilities,
  control names, "commercially safe" claim)
- Moonvalley Terms of Service — help.moonvalley.com/en/articles/10207682
  (user indemnification, ~$500 liability cap)
- Moonvalley prompting guidance — help.moonvalley.com (≥50-word prompt formula)
- fal model pages — fal.ai/models/moonvalley/marey/t2v and /i2v
  (v1.5, pricing $1.50/5s & $3.00/10s, 1920×1080 default, seed default 9,
  endpoints)
- fal blog — blog.fal.ai (v1.5 endpoints incl. motion/pose transfer)
- Businesswire — $84M raise, Voyager, "first fully-licensed" claim

Secondary / reporting (labeled):
- TechCrunch (2025-03-12, 2025-07-08, 2025-04-07) — public availability,
  indemnity-for-contractors-not-users distinction vs Adobe Firefly, pricing tiers
- CineD, VentureBeat, Deadline, PetaPixel, Variety, SiliconANGLE — commercial-
  safety framing, ~80% licensed figure, Vimeo partnership, funding

Independent practitioner report (disclosed method, single reviewer):
- Curious Refuge, "Marey by Moonvalley — An Honest Review" (2025) — hands-on
  quality scoring (~3/10), temporal/motion/adherence weaknesses vs Veo 3 /
  Seedance. Treat as one practitioner report, not a benchmark.

Re-verify every dated fact — versions, endpoints, pricing, and especially the
terms of service — before relying on it.
