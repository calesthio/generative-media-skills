---
name: tripo-3d
description: >-
  Produce 3D assets with Tripo (tripo3d.ai / Tripo AI by VAST) through its OpenAPI and Studio
  platform — text-to-3D, image-to-3D, and multiview-to-3D generation; PBR texturing; auto-rigging
  and preset animation; retopology/low-poly and quad remesh; format conversion (GLB/FBX/OBJ/USDZ/STL/3MF)
  and engine import (Unity/Unreal/Blender/3D printing). Use when an agent must drive the async task-based
  Tripo API (create task, poll or webhook, download), choose a model version (v3.0 / v3.1 / P1), write
  prompts or prepare input images, control mesh/texture parameters, estimate credits and respect rate
  limits, review generated mesh quality (topology, UVs, poly count, texture fidelity), run iteration and
  repair workflows, or reason about the rights/licensing of Tripo-generated assets. Trigger on requests to
  generate, texture, rig, animate, retopologize, convert, or evaluate a 3D model with Tripo, or to integrate
  the Tripo API into a pipeline. Not for choosing a 3D renderer, editing meshes by hand, or non-Tripo
  generators.
---

# Tripo 3D asset generation

Tripo (product of VAST AI Research; consumer brand "Tripo AI") turns text, single images, and multi-view
image sets into textured 3D meshes, then post-processes them into engine-ready assets: PBR texturing,
retopology, auto-rigging, preset animation, and format conversion. It ships as a web Studio, mobile apps,
and an async **task-based REST API** ("Tripo OpenAPI"). This skill is about producing production-usable
assets through that API and Studio.

> Evidence labels used below: **[Doc]** = official Tripo documentation/SDK; **[1P]** = first-party
> Tripo blog/marketing claim (directional, not independently verified); **[3P]** = disclosed third-party
> source; **[Heuristic]** = production judgment, not a documented guarantee. Volatile facts carry a
> **verified 2026-07-10** date; re-check them, because Tripo ships model and pricing changes frequently.

## When to use Tripo, and when not to

Tripo's strength is **speed and coverage**: a usable single-object mesh in tens of seconds to a couple of
minutes, across a huge range of props, characters, and hard-surface objects, with texturing/rigging/format
export in one API. **[Heuristic]** Reach for it when you need many game/AR/previz/3D-print assets fast, when
you have a concept image or clean reference, or when you want a first-pass base mesh to refine by hand.

Do **not** rely on Tripo (or set expectations accordingly) for:

- **Clean production topology out of the box.** Raw generation output is typically dense, organic
  triangulation. Use quad remesh, smart low-poly, or retopo in a DCC tool before deforming/subdividing.
  **[Heuristic]**
- **Full scenes / multi-object layouts.** It generates one object per task. Compose scenes yourself.
- **Precise dimensional/CAD accuracy.** It is a generative reconstruction, not a measured model. For
  3D printing, verify scale, wall thickness, and manifold-ness.
- **Guaranteed likeness of real, identifiable people, or reproduction of copyrighted/branded characters.**
  Treat these as rights risks (see Rights & licensing).
- **Text, fine logos, thin lattices, transparent/refractive materials.** These are common failure classes.
  **[Heuristic]**

## The task model (how the API actually works) — **[Doc]**, verified 2026-07-10

Everything is an **asynchronous task**. You submit a task, receive a `task_id`, then poll (or receive a
webhook) until it succeeds, then read output URLs.

- **Base URL:** `https://api.tripo3d.ai/v2/openapi`
- **Auth:** header `Authorization: Bearer YOUR_API_KEY`. Create keys at `platform.tripo3d.ai/api-keys`.
- **Create a task:** `POST /v2/openapi/task` with a JSON body whose `type` selects the operation.
- **Poll a task:** `GET /v2/openapi/task/{task_id}`. Response carries `status`, `progress`, `output`
  (download URLs), and `consumed_credit` (exact credits charged for that task).
- **Status values:** `queued` → `running` → `success` (also `failed`, `cancelled`, `banned`, `expired`,
  `unknown`). Poll until terminal; read model URLs from `output` on `success`.
- **Uploads:** input images may be passed as a `url` (public JPEG/PNG, max 20 MB), a `file_token` from
  direct upload, or an `object` from STS upload (`bucket: "tripo-data"`, `key: <resource_uri>`). STS upload
  is Tripo's recommended path. Output download URLs are **time-limited** — fetch and store them promptly.
- **Chaining:** post-process tasks reference a prior task by id
  (`original_model_task_id` / `draft_model_task_id`), so a model → texture → rig → convert pipeline is a
  chain of tasks, not a re-upload each time.

**[Heuristic]** Poll with backoff (e.g., 2 s, then 3–5 s) rather than tight loops; generation is
seconds-to-minutes depending on model/options. For batch/production, prefer webhooks if your integration
path supports them (native webhook support varies by API surface and by proxy providers such as fal/Runware,
which expose an `X-Webhook-URL`-style header **[3P]**, verified 2026-07-10; confirm against current Tripo docs
before depending on it, otherwise poll).

## Model versions — **[Doc]/[1P]**, verified 2026-07-10

Select with `model_version` on generation tasks. Volatile — re-check the changelog.

| Family | API `model_version` / selector | Character | Face/poly envelope |
|---|---|---|---|
| v3.0 (HD / "H3") | `v3.0-20250812` | Stable, general default | up to ~1M–1.5M tris **[Doc]** |
| v3.1 (HD / "H3.1") | `v3.1-20260211` | Higher geometric density, sharper edges, stronger PBR | up to ~1.5M–2M tris **[Doc]** |
| P1 (Smart Mesh P1.0) | `p1` selector (premium tier) | Native 3D-diffusion, **game-ready low-poly**, orientation control, seeds; very fast | ~48–20,000 faces **[Doc/1P]** |

- **v3.0** — safe general-purpose default when you want maximum detail and will retopo later. **[Heuristic]**
- **v3.1** — pick for "hero" detail: denser geometry and better PBR response; costs more compute/time.
  Marketed for hero game assets, cinematics, product shots. **[1P]**
- **P1** — pick when you want **engine-ready, controllable low-poly directly**: a target face budget
  (`face_limit` 48–20,000) and `orientation` control (`default` or `align_image`) so the asset faces a
  predictable axis. Announced at GDC 2026 as a native-3D-diffusion architecture producing low-poly assets in
  seconds. **[1P]** Costs more credits than v3.x per task. Older `Turbo-v1.0`, `v1.4`, and `H2` versions also
  exist for legacy/cheaper paths. **[Doc]**

The marketing "Hxx" names and the API `model_version` strings are not identical spellings — always drive the
API off the exact `model_version` string from the current docs, not the blog name.

## Generation tasks and their parameters — **[Doc]**, verified 2026-07-10

### text_to_model
- `type: "text_to_model"`, `model_version`, `prompt` (≤ 1024 chars; multilingual; no emoji/exotic Unicode).
- Optional: `negative_prompt` (≤ 255), `image_seed`, `model_seed`, `texture_seed`, `style`.

### image_to_model
- `type: "image_to_model"`, `model_version`, and a `file` (via `file_token` | `url` | `object`).
- `enable_image_autofix` cleans up the input; `texture_alignment` and `orientation` control how texture and
  the asset's facing follow the image.

### multiview_to_model
- `type: "multiview_to_model"`, `files` = an **ordered** list `[front, left, back, right]`.
- **Front is required**; other views may be omitted (pass empty for that slot). Use **at least 2** views.
  More consistent views → better back/side reconstruction. **[Doc]**

### Shared generation controls
- `texture` (bool, default `true`; ~10 credits cheaper when `false` for geometry-only).
- `pbr` (bool, default `true`) — emit PBR maps (base color / metallic-roughness / normal) for lit pipelines.
- `texture_quality`: `"standard"` (default) or `"detailed"` (+10 credits).
- `geometry_quality`: `"standard"` or `"detailed"` (+20 credits) on supported versions.
- `face_limit` (int) — cap output triangles; the practical lever for engine budgets.
- `quad` (bool, default `false`, +5 credits) — quad-dominant remesh for cleaner edge flow / subdivision.
- `smart_low_poly` (bool, default `false`, +10 credits) — automatic low-poly-ization at generation time.
- `auto_size` (bool) — normalize real-world scale; `compress` for smaller GLB; `export_uv`; `generate_parts`
  (+20 credits) to split into named parts; `style` for stylized geometry presets.

## Post-processing pipeline — **[Doc]**, verified 2026-07-10

Each references a prior task id, so you refine without re-generating:

- **texture_model** — re-texture an existing mesh. Key inputs: `original_model_task_id`, `texture`, `pbr`,
  `texture_quality`, `texture_alignment`, `texture_seed`, `part_names`, `bake`, plus a `text_prompt`,
  `image_prompt`, or `style_image` to redirect the look.
- **refine_model** — refine a draft mesh (`draft_model_task_id`).
- **mesh_segmentation** (40 cr) / **mesh_completion** (50 cr) — split into parts / fill holes and finish
  partial geometry.
- **smart_lowpoly** (30 cr) — retopo high-poly → low-poly with `face_limit`, `quad`, `bake`, `part_names`.
- **stylize_model** — apply a stylization `style`: `LEGO`, `VOXEL`, `VORONOI`, `MINECRAFT`, with `block_size`.

### Rigging & animation — **[Doc]**, verified 2026-07-10
1. **check_riggable** (`type: "check_riggable"`, free) — validate a mesh can be auto-rigged **before** paying
   to rig. Always gate on this for characters.
2. **rig_model** (25 cr) — auto-rig. Params: `original_model_task_id`, `out_format` (`"glb"` | `"fbx"`),
   `rig_type`, `spec` (skeleton spec, e.g. humanoid). Auto-rigging expects a roughly upright,
   symmetric, single-character mesh with clearly separated limbs. **[Heuristic]**
3. **retarget_animation** (10 cr per animation) — apply preset motions to the rigged mesh.
   `animation` takes one or a list of `"preset:<name>"` values: `preset:idle`, `preset:walk`, `preset:run`,
   `preset:jump`, `preset:climb`, `preset:dive`, `preset:fall`, `preset:turn`, `preset:slash`,
   `preset:shoot`, `preset:hurt`, plus quadruped/hexapod/octopod/serpentine/aquatic variants for non-humanoids.
   `out_format`, `bake_animation`, and `export_with_geometry` control the exported clip.

### Format conversion / export — **[Doc]**, verified 2026-07-10
- **convert_model** — `original_model_task_id` + `format` ∈ `GLTF`, `USDZ`, `FBX`, `OBJ`, `STL`, `3MF`
  (base 5 cr, +5 with extra options). Native generation output is **GLB**; convert to your target.
  - Engine/tool mapping **[Heuristic]**: Unity/Unreal → **FBX** or **glTF/GLB**; Blender → **GLB/glTF** or
    **FBX**; USD pipelines / Apple AR Quick Look → **USDZ**; 3D printing → **STL** or **3MF** (STL drops
    color; 3MF keeps color/material).

## Prompt and input-image strategy — **[Heuristic]** unless marked

**Text-to-3D prompts** describe an *object*, not a scene: subject + form + material + style. Be concrete
about silhouette and material ("a low-poly stylized wooden treasure chest with iron bands, closed lid").
Use `negative_prompt` to suppress recurring artifacts ("extra limbs, floating parts, text"). Text-to-3D has
inherent ambiguity about unseen sides; expect to iterate on `model_seed`/`image_seed`.

**Image-to-3D / multiview beats text for fidelity and control.** For the best single-image result:
- Clean, centered subject on a plain/transparent background; fills most of the frame.
- Even, neutral lighting; avoid hard shadows/specular blowout that the model bakes into geometry/texture.
- A roughly 3/4 "hero" angle reads volume better than a flat orthographic front for single-image input.
- Set `orientation`/`texture_alignment` so the generated asset faces and textures consistently with the image.

**Multiview** is the highest-control path: supply consistent front/left/back/right renders of the *same*
object (same lighting, same scale). It resolves the "hallucinated back" problem that plagues single-image and
text input. Front is mandatory; add as many real views as you have.

## Iteration and repair workflow — **[Heuristic]**

1. **Cheap first pass:** generate at `texture:false` (geometry only) or a lower tier to judge form before
   paying for texture. Lock the silhouette, then re-texture the winning geometry with **texture_model**
   rather than regenerating.
2. **Vary seeds, not prompts, first.** If geometry is 80% right, re-roll `model_seed` a few times before
   rewriting the prompt.
3. **Move up the model ladder deliberately:** v3.0 → v3.1 for detail; use P1 when you specifically need a
   controlled low-poly/oriented game asset. Don't pay for v3.1 detail you'll immediately decimate.
4. **Fix, don't regenerate:** holes → **mesh_completion**; too dense → **smart_lowpoly**/`quad`; wrong parts
   granularity → **mesh_segmentation**; bad texture only → **texture_model**.
5. **Gate rigging:** run **check_riggable** before **rig_model**; if it fails, the mesh usually needs a
   cleaner, upright, limb-separated topology first.

## Reviewing generated mesh quality — **[Heuristic]**

Before shipping a Tripo asset, check:
- **Poly count vs. budget** — did `face_limit` land where you need it? Overshoot → smart_lowpoly.
- **Topology** — raw output is triangulated and often uneven; if the asset will deform (rigged) or subdivide,
  demand quad remesh/retopo. Straight-to-static-prop tolerates raw triangulation.
- **Watertight / manifold** — required for 3D printing; check for holes, non-manifold edges, flipped normals.
- **UVs & texture** — seams, stretching, baked-in lighting, low-res detail on text/logos. PBR maps present if
  `pbr:true`. Re-texture if the geometry is good but the surface is not.
- **Scale & pivot/orientation** — confirm real-world size (`auto_size`) and that the pivot/facing matches your
  engine's convention (P1 `orientation` helps here).
- **Symmetry & floaters** — check for asymmetry, detached fragments, fused parts (use generate_parts /
  segmentation to separate).

## Credits, cost, and rate limits — **[Doc]/[3P]**, verified 2026-07-10

Billing is in **credits**: **$1.00 = 100 credits**. New accounts get **300 free credits, valid ~2 weeks**.
Each task response reports exact `consumed_credit`. Representative task prices **[Doc]** (subject to change):

| Operation | v3.0/v3.1 (H2/H3) | P1 |
|---|---|---|
| text_to_model | 10 (no tex) / 20 (tex) | 30 / 40 |
| image_to_model | 20 / 30 | 40 / 50 |
| multiview_to_model | 20 / 30 | 40 / 50 |
| import model | free | — |

Add-ons **[Doc]**: detailed texture +10, smart low-poly +10, quad +5, generate parts +20,
detailed geometry +20. Post-process: rig 25, retarget 10 per animation, pre-rig check free,
mesh_segmentation 40, mesh_completion 50, smart_lowpoly 30, convert 5 (+5 with options).

Consumer/Studio subscriptions differ from API credit purchasing. Reported tiers **[3P]**, verified
2026-07-10: **Basic** free (~300 credits/month, 1 concurrent task), **Pro/Professional** ~$15.90/mo
(~3,000 credits, ~10 concurrent), **Advanced** ~$39.90/mo (~8,000 credits, ~15 concurrent). Treat exact
dollar/credit figures and tier names as unstable; confirm on `tripo3d.ai/pricing` before quoting.

**Rate limits:** exceeding limits returns **HTTP 429**; **concurrent-task** limits are plan-dependent
(free ≈ 1). Errors carry a `code`, `message`, and `suggestion` (e.g. code `2002` = unsupported task type).
Handle 429 with backoff and respect the concurrency cap by queueing. **[Doc/3P]**

## Rights & licensing — read carefully, this is a real risk surface

**[Doc/1P]**, verified 2026-07-10:
- On the **free/Basic** plan, generated models are typically **published publicly** and released under a
  **Creative Commons CC BY 4.0**-style license — i.e., others may use them **with attribution**, and you do
  not get private/exclusive assets. Do not treat free-tier output as confidential or exclusive.
- **Paid plans** unlock **private** models and grant **commercial-use rights** to the geometry you generate,
  which is what production/retail/print use requires.
- Tripo's operating entity retains all IP in its **software, models, and technology** (Background IP); the
  license concerns the *asset you generate*, not the platform.

**[Heuristic]** Practical guidance for agents:
- For any commercial deliverable, generate on a **paid plan** and confirm the current Terms yourself
  (`tripo3d.ai/terms`) — licensing wording changes and CC BY 4.0's "commercial-with-attribution" nuance is
  easy to misread. Do not assert "you own it, full commercial rights" without checking the plan and terms.
- You are still responsible for the **input**: do not feed copyrighted/branded characters, trademarked
  designs, or images of identifiable real people you lack rights to, and don't launder those into a
  "generated" asset. The generator does not grant you rights you didn't have in the source.
- For **3D printing** commercial sales, verify both the Tripo license tier **and** that the design itself
  isn't infringing.

## Complete worked example (illustration, not a required formula)

**Intent:** produce an engine-ready, game-budget stylized barrel prop for Unity, from a concept image, then
convert to FBX. **Provider/model:** Tripo OpenAPI, P1 (want controlled low-poly + oriented asset).

```bash
# 1) Create an image_to_model task with P1, budgeting ~4k faces, PBR on, image-aligned orientation.
curl -s https://api.tripo3d.ai/v2/openapi/task \
  -H "Authorization: Bearer $TRIPO_API_KEY" -H "Content-Type: application/json" \
  -d '{
        "type": "image_to_model",
        "model_version": "p1",
        "file": { "type": "png", "url": "https://example.com/barrel_ref.png" },
        "face_limit": 4000,
        "texture": true,
        "pbr": true,
        "texture_quality": "detailed",
        "orientation": "align_image",
        "auto_size": true
      }'
# -> { "code":0, "data": { "task_id": "TASK_A" } }

# 2) Poll until success, then read output URLs and consumed_credit.
curl -s https://api.tripo3d.ai/v2/openapi/task/TASK_A \
  -H "Authorization: Bearer $TRIPO_API_KEY"
# status: queued -> running -> success; data.output has the GLB URL. Download it promptly (URL expires).

# 3) Convert the finished GLB to FBX for the Unity project (chained by task id).
curl -s https://api.tripo3d.ai/v2/openapi/task \
  -H "Authorization: Bearer $TRIPO_API_KEY" -H "Content-Type: application/json" \
  -d '{ "type":"convert_model", "original_model_task_id":"TASK_A", "format":"FBX" }'
```

**Why structured this way:** P1 with an explicit `face_limit` yields a game-budget mesh directly instead of a
million-triangle mesh you'd have to decimate; `orientation:"align_image"` keeps the pivot/facing predictable
for level design; texture+PBR give lit-pipeline maps; conversion is a cheap chained task off the same id.
**Expected result:** a ~4k-tri textured barrel, GLB then FBX. **Likely failure modes:** baked-in shadows from
a harsh reference photo (fix: cleaner lighting or `enable_image_autofix`); hallucinated back detail (fix:
supply a multiview set); topology too triangulated for later deformation (fix: `quad:true` or a
`smart_lowpoly` pass). **Variations:** swap to `multiview_to_model` with front/back/left/right renders for a
faithful hero prop; drop to v3.0 and `texture:false` for a rapid geometry-only silhouette review before
committing credits.

## Sources (verified 2026-07-10)

- Tripo OpenAPI docs — Introduction, Quick Start, Pricing, model-generation pages: `https://docs.tripo3d.ai/`
- Official Python SDK API reference (task types, params, animation presets):
  `https://github.com/VAST-AI-Research/tripo-python-sdk/blob/master/docs/API.md`
- Tripo platform docs (billing, rate limit, error handling, animation): `https://platform.tripo3d.ai/docs`
- Tripo API product page: `https://www.tripo3d.ai/api`; Pricing: `https://www.tripo3d.ai/pricing`
- Tripo blog — H3.1 / Smart Mesh P1.0 announcements (first-party claims): `https://www.tripo3d.ai/blog`
- Terms / licensing: `https://www.tripo3d.ai/terms` and 3D-print copyright guide on tripo3d.ai
- Third-party (disclosed, secondary): apidog developer guide `https://apidog.com/blog/how-to-use-tripo-3d-api/`;
  3D AI Studio Tripo P1 docs; fal / Runware Tripo model pages (proxy webhook behavior)
