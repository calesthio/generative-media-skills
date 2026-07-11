---
name: world-labs-marble
description: >-
  Generate persistent, explorable 3D worlds/environments with Marble by World
  Labs — from text, a single image, multiple images, video, or a 360 panorama,
  plus coarse-structure blocking with Chisel. Use this skill when a task needs a
  navigable 3D scene, VR/immersive backdrop, virtual-production environment,
  previz set, game-blockout, or web/engine-ready Gaussian splat or mesh, and you
  must choose an input mode, a Marble model, an export format, and a plan/API
  route, then review world quality. Covers the Marble web app and the World API,
  editing/expansion, output formats and what each supports downstream, import
  into Unity/Unreal/Blender/Houdini/web, pricing/credits, capability limits, and
  rights/licensing. Not for flat text-to-image, text-to-video clips, or
  real-time on-the-fly world models (Marble outputs are downloadable, static 3D
  environments).
---

# World Labs Marble

Marble is World Labs' commercial multimodal **world model**: it lifts a text
prompt, image(s), video, panorama, or coarse 3D blocking into a **persistent,
downloadable 3D environment** you can navigate, edit, expand, and export. World
Labs was co-founded by Fei-Fei Li; Marble reached general availability on
**2025-11-12** and a programmatic **World API** was announced **2026-01-21**.
(Documented; verified 2026-07-10.)

The defining property, and the thing that separates Marble from most
"generative video" or interactive world models: the world is **materialized as
persistent 3D geometry** (Gaussian splats and/or meshes) that you own as a file,
rather than hallucinated frame-by-frame as you walk. That makes it usable as a
production **asset**, not just a demo you watch. (Documented — worldlabs.ai blog;
verified 2026-07-10.)

## When to use this skill

Use it when the deliverable is a **3D space**:

- An explorable environment for VR (Quest 3, Vision Pro), a web viewer, or a
  game engine.
- A virtual-production / previz backdrop, a set blockout, or an environment
  concept that must hold up from multiple camera angles.
- A programmatic pipeline that needs many worlds generated on demand (World API).
- Turning a single photo, concept art, or a location video into a navigable set.

**Do not** reach for Marble when the user wants a flat image (use an image
model), a short talking/action video clip (use a video model), or a real-time
game engine that streams infinite world on the fly. Marble worlds are bounded,
static environments — extremely detailed, but not simulations with moving actors
or physics baked in.

## Access routes (verify — these are volatile)

As of **2026-07-10** there are two first-party routes; both are live:

| Route | Where | Auth | Billing | Best for |
|---|---|---|---|---|
| **Marble web app** | `marble.worldlabs.ai` | Account login | Monthly subscription (Free/Standard/Pro/Max) | Hands-on authoring, Chisel, Studio (Compose/Record), interactive editing |
| **World API** | `platform.worldlabs.ai`, endpoint base `api.worldlabs.ai/marble/v1` | `WLT-Api-Key` header | Prepaid credits (separate wallet) | Automated/batch generation, product integrations |

Critical, easily-missed fact: **app credits and API credits are separate
wallets.** Credits bought for the Marble app cannot be spent on the API, and vice
versa. Budget them independently. (Documented — docs.worldlabs.ai/api/pricing;
verified 2026-07-10.)

There is a published **AI-agent skill** for the API
(`docs.worldlabs.ai/api/agent-skill`) intended for coding agents that drive the
World API directly.

## Models (choose deliberately — cost and quality differ)

Documented model line as of 2026-07-10 (docs.worldlabs.ai/marble/models,
release notes 2026-04-02):

- **`marble-1.1`** — the recommended default. Improved quality at a **fixed**
  generation cost. Start here for most single-scene work.
- **`marble-1.1-plus`** — auto-expanding worlds: covers more 3D space in one
  shot when the scene allows. **Variable cost** (bigger world = more credits).
  Use when you need a genuinely large, walkable expanse from one generation.
- **`marble-1.0`** — legacy; keep only for continuing older projects.
- **`marble-1.0-draft`** — fastest and ~10× cheaper. Use for **prompt/iteration
  scouting** before committing a full-quality generation. Draft output is lower
  fidelity by design.

Heuristic (production): iterate prompts and framing on **draft**, then promote
the winning prompt/seed to **1.1**; reserve **1.1 Plus** for hero shots that must
be large. Reusing the `seed` keeps a concept stable while you change one variable.

## Input modes and their constraints

Marble accepts five prompt types. Match the mode to how much control you have and
need (documented — docs.worldlabs.ai/marble/create and API generate reference;
verified 2026-07-10):

- **Text** — describe the world in natural language. Most freedom, least
  control over exact appearance. Good for ideation and stylized worlds.
- **Single image** — lifts a photo or artwork into 3D. The image fixes the look
  from one direction; Marble invents the rest. Marble auto-detects an
  equirectangular panorama if you supply one.
- **Multiple images** — up to **4 images** (up to **8 in reconstruction mode**
  via the API), each tagged with a direction/azimuth (Front/Back/Left/Right) or
  Auto Layout. Use when you must control what the world looks like from several
  angles.
- **Video** — a short clip of a real location. Formats MP4/WebM/MOV/AVI, **max
  100 MB** (API limit raised to 100 MB on 2026-01-29). Best for rotational or
  walk-through coverage of an existing place.
- **360 panorama** — an equirectangular image. **Maximum spatial control** of
  any 2D input because it pins the full surround; the API can also generate a
  panorama for you (`/pano` endpoints).

The more the input constrains geometry (panorama > multi-image > single image >
text), the more predictable the world — but the less Marble invents. Pick the
weakest constraint that still gets the look you need. (Production heuristic.)

## Chisel — structure/layout control

**Chisel** (documented; the current name as of 2026-07-10) is Marble's
coarse-3D blocking tool. It **decouples structure from style**: you lay out the
spatial skeleton in 3D, then a text (or image) prompt paints the look onto it.

What Chisel gives you (docs.worldlabs.ai/marble/create/chisel-tools):

- Primitives — boxes and planes; a **wall tool** for vertical segments (room
  boundaries) and an **extrude** function for depth/volume.
- **Import existing 3D assets** — **GLB and FBX** models can be brought in as
  blocking and restyled cohesively into the generated world.
- A **panorama camera** you position to set where the detailed generation
  originates.

Use Chisel when **layout matters**: room proportions, door/window placement,
architectural footprints, or matching a real set's dimensions. It is the right
tool when a pure text or image prompt keeps giving you the right *style* but the
wrong *floor plan*. (Production heuristic.)

## Editing, expansion, and Studio tools

- **Create & Edit / AI-native editing** — remove or swap objects, touch up
  regions, or restyle the whole world with prompts. Surfaced through the omnibox
  (release notes 2026-04-02).
- **Pano Edit** — natural-language edits targeted at regions of the panorama.
- **Expand** — select a region and grow the world beyond its original bounds
  (the "click and expand" idea), or add detail to weak/low-fidelity areas.
  Expansion is gated to **Pro/Max** subscription tiers.
- **Variations** — generate alternate versions that keep the core scene.
- **Compose** (Studio) — arrange **multiple worlds** together with full control
  of layout; supports importing meshes into the Composer (release notes
  2026-01-29).
- **Record** (Studio) — author cinematic camera flythroughs with pixel-accurate
  paths and export video, including "enhanced video" that adds detail and
  **dynamic elements** (e.g. smoke, flowing water) to the render.

Note the important distinction: dynamic elements live in the **video export**,
not in the exported 3D geometry. The splat/mesh you download is **static**.
(First-party + production observation; verified 2026-07-10.)

## Output formats and what each supports downstream

Documented export specs (docs.worldlabs.ai/marble/export/specs and mesh;
verified 2026-07-10):

| Format | Detail | Downstream fit | Tier/limit |
|---|---|---|---|
| **Gaussian splat — SPZ** | Marble-native, size-optimized; ~2M or ~500k splats | Marble's own renderer; Spark (web/Three.js) | Highest visual fidelity |
| **Gaussian splat — PLY** | Uncompressed, broad tool compatibility | Blender/Houdini/Unity/Unreal splat plugins | Same fidelity, larger files |
| **Collider mesh (GLB)** | ~100–200k triangles, ~3–4 MB, instant | Physics/collision in engines | **Standard+**; not for display |
| **High-quality mesh (GLB)** | ~600k tris (textured) **and** ~1M tris (vertex-colored), 100–200 MB | Editable geometry for DCC/engines | **Pro**; up to ~1 hr to generate; rate-limited ~4/hr; owner-only |
| **360 panorama (PNG)** | Equirectangular, 2560×1280 | Skyboxes, matte refs | — |
| **Video** | Camera-path render, optional enhancement | Previz, social, edit | Enhancement/expansion gated to Pro+ |

Decision rule: **Gaussian splats for visual fidelity, meshes for interaction.**
If you need the best-looking result and the target can render splats (web via
Spark, or an engine plugin), export SPZ/PLY. If you need collision, physics, or a
watertight editable object, export the mesh — collider mesh for physics only,
high-quality mesh for visuals-plus-geometry. Both mesh variants exist because
reconstruction quality varies by scene; pick whichever version reconstructs your
scene better. (Documented + heuristic.)

Coordinate gotcha: exports default to **OpenCV** coordinates. For OpenGL-based
software, scale Y and Z by −1 (or choose the OpenGL option added 2026-01-01) or
the world imports inverted. (Documented; verified 2026-07-10.)

## Importing into engines and DCC tools

Marble documents Gaussian-splat import paths for **Unity, Unreal Engine,
Blender, and Houdini** (each via that tool's Gaussian-splatting plugin) and
**Spark** for custom web/Three.js apps; there are open-source interactive
examples that combine a world with rendering and physics
(docs.worldlabs.ai/marble/export). Practical path:

- **Web / lightweight interactive** → SPZ + Spark (`sparkjs.dev`).
- **Unity / Unreal** → PLY splat via the engine's splat plugin for visuals;
  **collider mesh GLB** alongside it for physics.
- **Blender / Houdini** (look-dev, matte, VFX) → PLY splat or high-quality mesh.

Because splat rendering still relies on third-party plugins in most engines,
confirm the target engine/version has a working Gaussian-splat renderer before
you commit a splat-only pipeline; fall back to the high-quality mesh where it
doesn't. (Production heuristic.)

## Pricing and credits (volatile — verify at purchase time)

**Marble app subscription tiers** (secondary-source-corroborated: The Batch /
deeplearning.ai and docs; verified 2026-07-10 — confirm live figures before
relying on them):

| Tier | Price | Generations/mo | Notable unlocks |
|---|---|---|---|
| **Free** | $0 | ~4 | Text, single image, or 360 panorama |
| **Standard** | ~$20/mo | ~12 | Multi-image, video, 3D-layout inputs; editing; collider-mesh export |
| **Pro** | ~$35/mo | ~25 | Expansion, video enhancement, high-quality mesh export, **commercial rights** |
| **Max** | ~$95/mo | ~75 | All features, highest volume |

**World API credits** (documented — docs.worldlabs.ai/api/pricing; verified
2026-07-10):

- **$1.00 per 1,250 credits**; **minimum purchase $5.00** (6,250 credits).
- **API credits do not expire**; auto-refill configurable; 402 on empty balance.
- Cost per generation: **draft** ~150–250 credits (cheapest for
  pano-from-image); **1.0 / 1.1** ~1,500–1,600 credits; **1.1 Plus** ~1,500 base
  scaling up to ~3,000 depending on world size (variable "dynamic cube" cost).

Rough rule of thumb: a full-quality API world (~1,500 credits) ≈ **$1.20**; a
draft ≈ **$0.12–$0.20**. Budget accordingly and scout on draft.

## Capability limits (state these to users up front)

- **Static, bounded worlds.** No baked-in moving actors, animation, or
  simulation in the exported geometry; dynamism appears only in video renders.
- **World size** is finite; **1.1 Plus** and **Expand** push the bounds but do
  not produce infinite streaming worlds.
- **Reconstruction artifacts** are expected in **thin structures, transparent
  or reflective surfaces, and areas the input never showed** (occluded backs,
  undersides). Marble invents unseen regions plausibly, not accurately.
- **High-quality mesh** takes up to ~1 hour, is rate-limited (~4/hr), and is
  Pro-tier/owner-only.
- **Mobile app support is limited** vs desktop.

(Documented + first-party; verified 2026-07-10.)

## Quality review criteria for a generated world

When reviewing a Marble world for production use, walk (don't glance) and check:

1. **Seams and holes** — orbit the camera; look for tears where expansion or
   panorama edges meet, and floating/missing geometry behind foreground objects.
2. **Ground plane** — is the floor coherent and level, or does it dish/warp?
   Matters most for game blockouts and physics.
3. **Occluded regions** — the sides/backs the input never saw are the weakest;
   judge whether your camera will ever see them.
4. **Thin/transparent/reflective elements** — railings, foliage, glass, water:
   the usual artifact sources. Decide if a mesh export will hold up or if you
   should stay in splats.
5. **Scale** — with real-world unit scaling (added 2026-01-01), confirm
   dimensions match your set/engine before importing.
6. **Style consistency** — after edits/compose, confirm lighting and style read
   as one coherent space, not stitched fragments.
7. **Format fit** — did you export the right thing (splat for looks, collider
   for physics), and does the target renderer actually support it?

If artifacts sit only outside the intended camera path, the world may be
production-ready as-is. If they're on-camera, prefer **Expand**/edit or a
**re-generation with a stronger input** (add a panorama or multi-image) over
patching in a DCC. (Production heuristic.)

## Rights and licensing (get this right — it gates commercial delivery)

Documented / first-party (worldlabs.ai Terms of Service and product docs;
verified 2026-07-10):

- **Free-tier output**: World Labs **retains rights**; the user gets a
  revocable, non-exclusive license for **personal, non-commercial use only**.
- **Paid-tier output**: the user **owns** the outputs and may use them
  **commercially**, excluding World Labs' own products/technology/IP — subject to
  the TOS.
- In the **Marble product's own tiering**, commercial rights are attached to
  **Pro and Max**. Treat **Standard as effectively non-commercial** for delivery
  purposes despite being a paid tier, and **verify the current tier's commercial
  grant in the live TOS** before shipping client work. (This app-tier gating vs.
  the TOS "paid account" language is a known ambiguity — resolve it against the
  live terms for the specific plan, do not assume.)
- You are responsible for your **inputs**: don't feed copyrighted images,
  trademarked material, or a real person's likeness you have no rights to into a
  world you intend to distribute.

When advising a user, always tie the recommended **plan to the intended use**: a
commercial deliverable needs **Pro or above** (or a paid API entitlement) —
recommending the Free tier for client work is a rights error.

---

## Complete examples (labeled; adapt, do not copy verbatim)

### Example A — VR walkthrough of a fictional location (web app, panorama input)

- **Intent:** an explorable VR scene of a "moss-covered abandoned subway
  platform" for a Quest 3 web experience.
- **Model/route:** Marble web app; scout on `marble-1.0-draft`, finalize on
  `marble-1.1`.
- **Input & why:** start from a **360 panorama** (rendered or shot) rather than
  text — a panorama pins the full surround so the platform reads coherently in
  every head direction, which VR demands.
- **Workflow:** draft-generate → check ground plane and seams → promote prompt +
  seed to 1.1 → **Expand** the tunnel mouths to lengthen the platform → export
  **SPZ** → render on the web with **Spark**.
- **Parameters:** reuse `seed` across draft→final; keep world private until
  reviewed.
- **Expected result:** a seamless, walkable platform holding up under free head
  movement.
- **Likely failure modes:** warped ground, artifacts on tunnel-mouth edges after
  expansion, thin railing tearing — review by orbiting before export.
- **Variations:** multi-image (4 angles) if you have reference photos; mesh
  export if the VR app needs collision.

### Example B — Game environment blockout matching a set floor plan (Chisel)

- **Intent:** a first-pass playable blockout of a two-room interior with a
  specific door position, for greyboxing in Unity.
- **Route/model:** web app, Chisel → `marble-1.1`.
- **Input & why:** **Chisel**, because *layout* is the constraint. Text prompts
  gave the right style but the wrong floor plan; blocking walls/door in 3D fixes
  geometry, and the prompt only styles it.
- **Workflow:** wall-tool the two rooms and the doorway → position the panorama
  camera at the play-start point → prompt "warehouse office, worn concrete,
  fluorescent light" → generate → export **collider mesh GLB** (physics) +
  **PLY splat** (visual) → import both into Unity (splat plugin + collider).
- **Expected result:** proportions and door placement match the intended plan;
  greyboxing can start against real collision.
- **Likely failure modes:** collider mesh too coarse for precise interactions
  (it's meant to be simple); high-quality mesh needed later for visual polish.
- **Variations:** import an existing **GLB/FBX** prop into Chisel to have it
  restyled into the scene.

### Example C — Batch backdrops via the World API (programmatic)

- **Intent:** generate 30 varied "alien desert" backdrops for a virtual-
  production pre-light, unattended overnight.
- **Route/model:** World API, `marble-1.1` (fixed cost for predictable budget).
- **Request (illustrative JSON body to
  `POST api.worldlabs.ai/marble/v1/worlds:generate`, header `WLT-Api-Key`):**

  ```json
  {
    "world_prompt": { "type": "text",
      "text_prompt": "vast alien desert, twin suns, wind-carved rock arches" },
    "display_name": "alien-desert-07",
    "model": "marble-1.1",
    "seed": 7,
    "tags": ["previz", "desert"],
    "permission": { "public": false }
  }
  ```

- **Async handling:** the call returns an `operation_id`; **poll**
  `/operations/{operation_id}` until `done`, then read the world and call the
  **export** endpoint for SPZ. Charge (`cost`) is reported on success.
- **Budget:** ~1,500 credits each ≈ ~$1.20 × 30 ≈ ~$36 in API credits; scout one
  or two prompts on **draft** first to lock the wording.
- **Expected result:** 30 distinct, private worlds ready to pull into the
  virtual-production toolchain.
- **Likely failure modes:** 402 on empty credit balance (enable auto-refill);
  same-seed sameness across prompts (vary seed **and** prompt); over-spend from
  jumping straight to 1.1 Plus without draft scouting.

---

## Sources (verified 2026-07-10 unless noted)

Primary / first-party:

- Marble docs home & index — https://docs.worldlabs.ai/ , https://docs.worldlabs.ai/llms.txt
- Models — https://docs.worldlabs.ai/marble/models.md
- Create / input modes — https://docs.worldlabs.ai/marble/create/index.md and prompt guides
- Chisel — https://docs.worldlabs.ai/marble/create/chisel-tools/chisel-basics.md
- Export specs & mesh — https://docs.worldlabs.ai/marble/export/specs.md , https://docs.worldlabs.ai/marble/export/mesh.md
- API pricing — https://docs.worldlabs.ai/api/pricing
- API generate reference — https://docs.worldlabs.ai/api/reference/worlds/generate.md
- Subscriptions & billing — https://docs.worldlabs.ai/marble/support/account-billing
- Release notes — https://docs.worldlabs.ai/marble/release-notes.md
- Marble launch blog — https://www.worldlabs.ai/blog/marble-world-model (2025-11-12)
- World API announcement — https://www.worldlabs.ai/blog/announcing-the-world-api (2026-01-21)
- Bigger & Better Worlds — https://www.worldlabs.ai/blog/bigger-better-worlds (beta 2025-09-16)
- Terms of Service — https://www.worldlabs.ai/terms-of-service

Secondary (disclosed-method, used only where first-party pages were SPA shells,
e.g. exact consumer dollar tiers):

- The Batch / deeplearning.ai — https://www.deeplearning.ai/the-batch/world-labs-makes-its-marble-generative-world-model-public-adds-chisel-editing-tool/
- TechCrunch — https://techcrunch.com/2025/11/12/fei-fei-lis-world-labs-speeds-up-the-world-model-race-with-marble-its-first-commercial-product/

Volatile facts (model names, credit costs, subscription prices, access routes,
export limits) are dated above; re-verify against the live docs and pricing pages
before relying on them for a purchase or a delivery decision.
