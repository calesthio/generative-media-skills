---
name: meshy-3d
description: >-
  Produce 3D assets with Meshy (meshy.ai) through its REST API and web
  platform — text-to-3D, image-to-3D, multi-image-to-3D, AI texturing/PBR,
  remesh/topology control, UV, and auto-rigging/animation. Use this skill when
  an agent must generate a mesh from a prompt or reference image, control
  polygon count and topology, apply or restyle textures, rig a humanoid for
  animation, export to GLB/FBX/OBJ/USDZ/STL for Unity/Unreal/Blender, drive
  Meshy's asynchronous job API (auth, polling, streaming, webhooks, credits,
  rate limits), review generated meshes for game/film/print readiness, or
  decide whether Meshy is the right tool at all. Not for editing an existing
  hand-modeled asset's geometry, hard-surface CAD with exact dimensions, or
  guaranteed-watertight manufacturing parts.
---

# Meshy 3D generation

Meshy is a hosted generative-3D service. You give it text or images; it returns
a textured mesh (GLB/FBX/OBJ/USDZ/STL/3MF), with optional PBR maps, remeshing,
UV, auto-rigging, and library animations. Everything runs as **asynchronous
jobs**: you POST a task, get a task ID, then poll, stream (SSE), or receive a
webhook until `SUCCEEDED`.

This skill covers driving Meshy well: choosing the right generation mode,
writing prompts that separate geometry from texture, controlling topology and
poly count, texturing and re-texturing, rigging and animating, exporting into a
game/film/print pipeline, and judging whether the output is usable.

## Evidence labels used below

- **[Doc]** — stated in official Meshy documentation, API reference, or help
  center (URLs in Sources). Volatile items carry a verification date.
- **[1P-claim]** — a first-party Meshy claim (marketing/blog/help) not
  independently verified. Treat as a claim, not a guarantee.
- **[Heuristic]** — production judgment from how generative-3D pipelines behave;
  verify against your own output.

Volatile facts (model IDs, credit costs, limits, formats) were verified
**2026-07-10** against docs.meshy.ai. Re-check the changelog and pricing pages
before quoting numbers to a user, because Meshy ships model versions and
adjusts credit costs and promotions frequently.

## When to use Meshy — and when not to

Use Meshy when you need:

- A single, coherent **prop, character, or creature** fast from a prompt or a
  reference image (concept-to-asset, game jam, previz, background dressing,
  crowd fillers, marketplace assets, 3D-print blanks). [Heuristic]
- A **textured** starting mesh you will clean up downstream rather than a
  final production hero asset. [Heuristic]
- Bulk asset generation where **throughput and cost per asset** matter more
  than authored topology. [Heuristic]

Do **not** reach for Meshy when:

- You need **exact real-world dimensions or CAD tolerances** (mechanical parts,
  enclosures, mounting brackets). Generative meshes are approximate; use CAD.
  [Heuristic]
- You need **guaranteed-watertight, manifold** geometry for manufacturing. Meshy
  offers printability analysis/repair and remesh, but does not guarantee a
  manifold result; validate in a slicer/mesh-repair tool. [Heuristic]
- You must **edit the geometry of an existing hand-authored asset** — Meshy
  regenerates, it does not surgically edit your mesh.
- The subject is a **full scene** (room, environment, multiple interacting
  objects). Text-to-3D and image-to-3D reconstruct one subject best; build the
  scene from separately generated parts in your engine. [Doc/Heuristic]
- You require **clean animation-ready quad topology with edge loops around
  deformation areas** authored to spec. Meshy's `quad` remesh is quad-dominant
  reconstruction, not artist-placed edge flow. [Heuristic]
- Licensing forbids AI-generated assets, or your reference images are
  copyrighted in a way that would taint ownership (see Rights & licensing).

## Model versions and mode selection

`ai_model` accepts `meshy-6`, `meshy-5`, or `latest`; `latest` resolves to the
current generation, which is **Meshy-6** as of 2026-07-10. **[Doc, verified
2026-07-10]** Meshy-4 was retired and its API requests are no longer supported.
**[Doc]** Pin an explicit version (`meshy-5` or `meshy-6`) when you need
reproducible behavior across a batch; use `latest` only when you want Meshy's
newest default and can tolerate behavior changes. [Heuristic]

`model_type` selects `standard` (default) or `lowpoly`. **[Doc]** `lowpoly`
produces stylized low-polygon output and, per the image-to-3D reference,
**overrides remesh, PBR, and poly-count settings**, so do not combine it with
fine topology control. **[Doc, verified 2026-07-10]**

Meshy-6-only / latest-only texture features: `hd_texture` (4K base color),
`remove_lighting` (bakes out captured shadows/highlights), and, for
image-to-3D, `image_enhancement`. **[Doc, verified 2026-07-10]**

## Deprecated parameters — do not use

- `art_style` (Text-to-3D preview) — unsupported by Meshy-6; formerly
  `realistic` / `sculpture`. **[Doc]**
- `symmetry_mode` — no longer functional. **[Doc]**
- `is_a_t_pose` — replaced by `pose_mode` (`a-pose`, `t-pose`, or `""`).
  **[Doc]**
- Remesh `resize_height`, `resize_longest_side`, `auto_size`, `origin_at` —
  documented as deprecated on the remesh endpoint. **[Doc]**

Passing deprecated params generally no-ops; prefer the current replacements so
your integration survives cleanups.

## The async job model

**Base URL** `https://api.meshy.ai/openapi/v1` (Text-to-3D uses the `v2` path
`/openapi/v2/text-to-3d`; other endpoints are `v1`). **[Doc, verified
2026-07-10]**

**Auth** Bearer token: `Authorization: Bearer $MESHY_API_KEY`. Create the key
at meshy.ai/settings/api; it is shown once — store it (env var, secret
manager), never hardcode. **API access requires a Pro tier or higher**
subscription; the free tier cannot create API tasks. **[Doc]**

**Task lifecycle** Every generation POST returns a task `id` immediately. Status
progresses `PENDING → IN_PROGRESS → SUCCEEDED` (or `FAILED` / `CANCELED`), with
`progress` 0–100 and, while `PENDING`, `preceding_tasks` (queue position).
**[Doc]**

**Three ways to learn a task finished** [Doc]:
1. **Poll** `GET /openapi/v1/<endpoint>/:id` on an interval until terminal
   status. Simplest; use a backoff (e.g. 2–5 s) and stop on
   `SUCCEEDED`/`FAILED`/`CANCELED`. [Heuristic]
2. **Stream** `GET .../:id/stream` — SSE `message`/`error` events; partial
   frames carry only `id`, `progress`, `status`.
3. **Webhook** — register a callback to be notified on completion. Prefer for
   server integrations to avoid poll load. [Heuristic]

**Rate limits** (verified 2026-07-10) [Doc]: 20 requests/second on Pro,
Premium, Ultra, Studio; 100/s on Enterprise. Concurrent "queue" tasks (Text to
3D, Image to 3D, Text to Texture, Remesh): Pro **10**, Studio **20**, Premium
**30**, Ultra **100**, Enterprise **50** (customizable). Exceeding rps →
`429 RateLimitExceeded`; exceeding concurrency → `429 NoMoreConcurrentTasks`.
Design a client-side concurrency gate to your tier's queue limit and retry 429s
with backoff. [Heuristic]

**Error codes** [Doc]: `400` bad/invalid params or over-limit prompt, `401`
bad key, `402` insufficient credits, `404` unknown task, `429` rate/queue.
Failed tasks return `task_error.message`; `consumed_credits` is `0` on failure.

**Asset retention** Generated files are retained ~**3 days** on non-Enterprise
plans. **[Doc, verified 2026-07-10]** Download and re-host output URLs
promptly; do not treat Meshy CDN URLs as permanent storage. [Heuristic]

## Text-to-3D: the two-step preview → refine workflow

Text-to-3D is deliberately two calls so you can approve geometry before paying
to texture it. **[Doc]**

**Step 1 — preview (geometry only).** `POST /openapi/v2/text-to-3d` with
`mode: "preview"` and a `prompt` (≤ 600 chars). Key controls: **[Doc, verified
2026-07-10]**

- `ai_model` `meshy-6` | `meshy-5` | `latest`
- `model_type` `standard` | `lowpoly`
- `topology` `triangle` (default) | `quad`
- `target_polycount` 100–300,000 (default 30,000); or `decimation_mode` 1–4
  (adaptive; overrides `target_polycount`)
- `should_remesh` (default `false` on Meshy-6, `true` otherwise)
- `pose_mode` `""` | `a-pose` | `t-pose` — request an A/T pose when the mesh
  will be rigged
- `target_formats` any of `glb, obj, fbx, stl, usdz, 3mf` (all except `3mf` by
  default)
- `auto_size` + `origin_at` (`bottom`/`center`) for real-world scale
- `alpha_thumbnail`, `moderation`

**Step 2 — refine (texture).** POST again with `mode: "refine"` and
`preview_task_id` = the succeeded preview's ID. Texture controls: `enable_pbr`
(metallic/roughness/normal/emission maps), `hd_texture` (4K base color, Meshy-6),
`texture_prompt` (≤ 600 chars), `texture_image_url` (URL or base64 style
reference), `remove_lighting` (default `true`, Meshy-6). **[Doc]**

Outputs include `model_urls` (per format), `texture_urls` (array with
`base_color` and, under PBR, `metallic`/`normal`/`roughness`/`emission`),
`thumbnail_url`. **[Doc]**

Because these are separate billed steps, **iterate cheaply**: regenerate or
re-prompt at preview until the silhouette/topology is right, then refine once.
[Heuristic]

## Image-to-3D and Multi-Image-to-3D

`POST /openapi/v1/image-to-3d` reconstructs one subject from **one** image
(`image_url` as public URL or base64 data URI, `.jpg/.jpeg/.png`), or from a
prior text-to-image / image-to-image task via `input_task_id`. **[Doc]**
Texturing and topology params mirror text-to-3D refine plus:
`should_texture` (default true), `image_enhancement` (Meshy-6, default true),
`save_pre_remeshed_model`, `multi_view_thumbnails`. **[Doc, verified
2026-07-10]**

`POST /openapi/v1/multi-image-to-3d` accepts **1–4 images of the same object
from different angles** (`image_urls`) for better reconstruction. **[Doc]**

Reference-image guidance [Heuristic]:

- Use a **clean subject on a plain background**, well lit, minimal occlusion,
  the whole object in frame. Busy backgrounds bleed into reconstruction.
- For multi-image, shoot/collect **consistent, non-conflicting views** (e.g.
  front, side, back) of the *same* object at the *same* scale and lighting;
  contradictory views produce fused or averaged geometry.
- Image-to-3D infers unseen sides — expect invention on the back of a
  single-front-view input; add views (multi-image) to constrain it.
- `texture_prompt` and `texture_image_url` guide *texture*, not shape; text is
  prioritized if both are given (per the image-to-3D reference). **[Doc]**

## Texturing, PBR, and re-texturing

Texture quality is separable from geometry. Options across the texturing-capable
endpoints [Doc]:

- `enable_pbr` — produce metallic/roughness/normal (+ emission on Meshy-6) maps
  for physically based rendering in Unity/Unreal/Blender. Leave off for flat
  base-color-only assets.
- `hd_texture` — 4K (4096²) **base color**; PBR maps stay 2K. Meshy-6/latest
  only. Use for hero assets seen close up; skip for background props to save
  credits/time. [Doc/Heuristic]
- `remove_lighting` — bakes out captured highlights/shadows so your engine can
  relight; default `true`, Meshy-6/latest. Keep on when the asset must react to
  scene lighting. [Doc]

**Retexture / restyle an existing mesh:** `POST /openapi/v1/retexture` with
`input_task_id` or `model_url` (`.glb/.gltf/.obj/.fbx/.stl`) plus a style via
`text_style_prompt` (≤ 600 chars) or `image_style_url`; if both are given,
`image_style_url` wins. **[Doc, verified 2026-07-10]** Key flag:
`enable_original_uv` — reuse the model's existing UV layout instead of
generating new UVs (preserves existing textures; if the model has no UVs,
quality suffers). Also supports `enable_pbr`, `hd_texture`, `remove_lighting`,
`ai_model`, `target_formats`. **[Doc]** Use retexture to re-skin one mesh into
many variants (color/material swaps) without regenerating geometry. [Heuristic]

## Topology, poly count, and remesh

- `topology: triangle` — default; fine for static props, rendering, and most
  engine import. `topology: quad` — quad-dominant reconstruction, friendlier to
  subdivision and some DCC workflows, but **not** artist-authored edge loops.
  [Doc/Heuristic]
- `target_polycount` (100–300,000): pick to budget. As rough starting targets
  [Heuristic]: background/mobile props ~1k–10k; standard game assets ~10k–50k;
  film/close-up hero or 3D-print masters higher (tens–hundreds of thousands).
  These are budgets, not quality guarantees — a high count can still hide bad
  topology.
- `decimation_mode` 1–4 gives adaptive reduction and **overrides**
  `target_polycount`. [Doc]

**Remesh** `POST /openapi/v1/remesh` re-topologizes/exports an existing task or
uploaded model (`input_task_id` or `model_url`; `.glb/.gltf/.obj/.fbx/.stl`).
Params: `target_formats` (adds `blend`), `topology`, `target_polycount`
(100–300,000, default 30,000), `decimation_mode` 1–4. **[Doc, verified
2026-07-10]** Reach for remesh when the raw generation has **too many faces,
messy topology, or you need a watertight-oriented mesh for printing**, and
**before rigging if the mesh exceeds 300,000 faces** (the rigging cap). [Doc]

Recommended post-processing order (Meshy's own guidance):
**Remesh → Unwrap UV → AI Texturing → Rigging → Animate → export.** **[Doc]**

## Rigging and animation

`POST /openapi/v1/rigging` rigs a **textured humanoid** GLB. **[Doc, verified
2026-07-10]** Requirements and params:

- Input: `input_task_id` (a textured model task) **or** `model_url` (GLB /
  `.glb` only, public URL or data URI). [Doc]
- `height_meters` (default 1.7, must be positive); optional
  `texture_image_url` (UV-unwrapped base-color PNG). [Doc]
- **Constraints:** humanoid with clearly defined limbs; character must face the
  **+Z** axis (glTF forward); **≤ 300,000 faces** when using
  `input_task_id` (remesh first if larger). Untextured meshes, non-humanoids,
  and unclear limb structure are unsuitable. [Doc]
- Output: rigged character in **FBX and GLB**, plus basic walk/run animations
  (skinned and armature-only variants). [Doc]

**Animation** `POST /openapi/v1/animations` applies a library clip to a rigged
model via `action_id`. The library holds **500+ animations** (categories like
DailyActions, WalkAndRun, Fighting, Dancing, BodyMovements); look up the
`action_id` in the Animation Library reference. **[Doc, verified 2026-07-10]**
For custom or non-humanoid motion, rig/animate in Blender/Maya instead. [Heuristic]

## Export and engine import

Formats: `glb, obj, fbx, stl, usdz, 3mf` (remesh adds `blend`). Request only
what you need via `target_formats` to keep responses small. **[Doc]**

Practical routing [Heuristic]:

- **Unity / Unreal / three.js / web:** `glb` (or `fbx` for skinned rigs). GLB
  carries PBR maps in one file. Assign `metallic`/`roughness`/`normal`/
  `emission` from `texture_urls` if you re-import maps separately.
- **Blender / DCC editing:** `glb` or, from remesh, `blend`; `fbx` for rigs.
- **AR (iOS Quick Look):** `usdz`.
- **3D printing:** `stl` or `3mf`; run remesh first for topology/scale, then
  validate manifoldness and wall thickness in a slicer.
- Set real scale with `auto_size` + `origin_at`, or `height_meters` at rigging,
  so the asset imports at usable size rather than arbitrary units.

## Prompt construction: separate geometry from texture

Geometry is decided at **preview / generation**; surface look is decided at
**refine / texture**. Write for each stage. [Doc/Heuristic]

**Geometry prompt** (subject + form + a few concrete features). One object, ~3–6
key details. Name the object type first, then defining shape/parts, then scale
and intended use. Prefer singular nouns — plurals ("warriors") invite fused or
extra limbs. Avoid full scenes, abstract concepts, and micro-detail like
individual hair strands. **[1P-claim, Meshy prompt guide]**

**Texture prompt** (materials, colors, finish, style) belongs in
`texture_prompt` / retexture: e.g. "brushed brass and dark oak, matte finish"
rather than restating the shape. Concrete material words ("smooth gold metal")
beat vague praise ("looks beautiful"). **[1P-claim]**

Render-quality buzzwords ("8k, Unreal Engine, Octane, cinematic lighting") are
image-model habits; they mainly affect Meshy's *texture/albedo*, not geometry —
use them in the texture stage, not to try to improve the mesh. [Heuristic]

## Quality review: is the mesh usable?

Inspect before accepting. Check [Heuristic]:

- **Silhouette / proportions** from multiple angles (use
  `multi_view_thumbnails` or open the GLB). Generative meshes often look right
  from the front and wrong from behind or top.
- **Topology & poly count** — is it within budget? Is it a dense blob that
  needs remesh? `quad` requested where subdivision/deformation is needed?
- **UVs & seams** — visible seams or stretched texels? If you must hand-paint,
  Unwrap UV first; for restyles, `enable_original_uv` preserves layout.
- **Watertightness / manifold** for print — do not assume; verify in a mesh
  tool. Meshy provides printability analysis/repair but no guarantee. [Doc]
- **Texture artifacts** — baked-in lighting (turn on `remove_lighting`),
  smeared or hallucinated detail on unseen faces, resolution (upgrade to
  `hd_texture` only where it shows).
- **Rig readiness** — humanoid, +Z facing, ≤ 300k faces, in A/T pose, textured
  before you send it to rigging.
- **Symmetry/limbs** — extra/fused limbs or asymmetry from ambiguous prompts or
  conflicting reference views → re-prompt or add views.

## Iteration and repair workflow

1. **Preview cheaply, refine once.** Approve geometry before texturing. [Doc]
2. **Wrong shape?** Re-prompt geometry (singular noun, clearer form, add
   reference image / more views). Small wording changes shift results. [1P]
3. **Right shape, wrong surface?** Keep the mesh; re-run
   **refine**/**retexture** with a better `texture_prompt` or
   `image_style_url`. Don't regenerate geometry to fix a texture. [Heuristic]
4. **Too heavy / bad topology?** **Remesh** to target poly count / `quad`. [Doc]
5. **Seams / hand-paint needed?** **Unwrap UV** before texturing. [Doc]
6. **Needs animation?** Ensure textured + A/T pose + ≤ 300k faces (remesh if
   not) → **rig** → **animate** by `action_id`. [Doc]
7. **Batch:** gate concurrency to your tier's queue limit; retry 429s; download
   outputs within the retention window. [Heuristic]

## Credits and pricing (verified 2026-07-10)

API usage bills per operation in credits (Pro+ subscription required). Costs
depend on model: Meshy-6 and low-poly cost more than legacy models. **[Doc]**

| Operation | Meshy-6 / low-poly | Other models |
|---|---|---|
| Text-to-3D **preview** | 20 | 5 |
| Text-to-3D **refine** (texture) | 10 | 10 |
| Image-to-3D (no texture / with texture) | 20 / 30 | 5 / 15 |
| Multi-Image-to-3D (no texture / with texture) | 20 / 30 | 5 / 15 |
| Retexture / Text-to-Texture | 10 | 10 |
| Remesh | 5 | 5 |
| Auto-rigging | 5 | 5 |
| Animation | 3 | 3 |

**[Doc, docs.meshy.ai/en/api/pricing, verified 2026-07-10]** A full textured
Meshy-6 text-to-3D via API is therefore ~30 credits (20 preview + 10 refine).
Failed tasks charge 0. Promotions and per-model costs change — re-read the
pricing page before quoting. Web-app pricing can differ from API per-operation
pricing. [Doc/Heuristic]

## Rights and licensing (verified 2026-07-10)

- **Paid plans:** you retain **full private ownership** of assets you create and
  may distribute/sell them, provided (a) you did not use materials that infringe
  others' copyright as input, and (b) you do **not** publish the model to the
  public Meshy Community — publishing to the community removes that private
  ownership protection. **[Doc, Meshy help center]**
- **Free plan:** models are licensed **CC BY 4.0** — you may use, modify, and
  even sell them, but must give attribution (Meshy suggests "Model created with
  Meshy – CC BY 4.0 License"). **[Doc]**
- **Input hygiene:** feeding copyrighted/trademarked reference images (a
  character, a logo, a real person) can taint ownership and create infringement
  risk regardless of plan. Use references you have rights to. [Heuristic]
- Confirm current terms at meshy.ai/terms-of-use before shipping commercially;
  these terms are volatile.

## Complete examples (illustrative — not fixed formulas)

### Example A — Textured game prop, text-to-3D, Meshy-6

Intent: a game-ready treasure chest, ~20k tris, PBR, GLB for Unity.

Preview (geometry):
```bash
curl -s https://api.meshy.ai/openapi/v2/text-to-3d \
  -H "Authorization: Bearer $MESHY_API_KEY" -H 'Content-Type: application/json' \
  -d '{
    "mode": "preview",
    "prompt": "a sturdy wooden treasure chest with iron banding and a domed lid, ornate lock plate, medieval fantasy style",
    "ai_model": "meshy-6",
    "topology": "triangle",
    "target_polycount": 20000,
    "target_formats": ["glb"]
  }'
# -> { "result": "<preview_id>" }  then poll GET /openapi/v2/text-to-3d/<preview_id>
```
Refine (texture) once preview is `SUCCEEDED`:
```bash
curl -s https://api.meshy.ai/openapi/v2/text-to-3d \
  -H "Authorization: Bearer $MESHY_API_KEY" -H 'Content-Type: application/json' \
  -d '{
    "mode": "refine",
    "preview_task_id": "<preview_id>",
    "enable_pbr": true,
    "texture_prompt": "aged oak planks, dark iron fittings, worn brass lock, matte finish"
  }'
```
Why: geometry words in preview, material words in the texture stage; PBR for
engine relighting; poly budget set at preview. Expected: a chest GLB with
base-color + metallic/roughness/normal maps. Failure modes: over-detailed prompt
→ mushy carving; skipping `enable_pbr` → flat look in Unreal. Variation: add
`hd_texture: true` for a close-up hero chest.

### Example B — Character from concept art, then rig + walk

Intent: reference image → riggable humanoid → walking animation.

```bash
# 1) multi-image reconstruction (front + side + back of the SAME character)
curl -s https://api.meshy.ai/openapi/v1/multi-image-to-3d \
  -H "Authorization: Bearer $MESHY_API_KEY" -H 'Content-Type: application/json' \
  -d '{ "image_urls": ["https://.../front.png","https://.../side.png","https://.../back.png"],
        "ai_model":"meshy-6", "should_texture": true, "pose_mode": "a-pose" }'
# poll -> SUCCEEDED, note <model_task_id>; confirm faces <= 300000 (remesh if not)

# 2) rig the textured humanoid
curl -s https://api.meshy.ai/openapi/v1/rigging \
  -H "Authorization: Bearer $MESHY_API_KEY" -H 'Content-Type: application/json' \
  -d '{ "input_task_id": "<model_task_id>", "height_meters": 1.8 }'
# poll -> <rig_task_id>

# 3) apply a walk animation by action_id (look up in Animation Library)
curl -s https://api.meshy.ai/openapi/v1/animations \
  -H "Authorization: Bearer $MESHY_API_KEY" -H 'Content-Type: application/json' \
  -d '{ "input_task_id": "<rig_task_id>", "action_id": 1 }'
```
Why: `a-pose` at generation makes rigging reliable; multi-image constrains the
back so the rig binds a real mesh, not a hallucinated one; rig needs a textured
humanoid ≤ 300k faces facing +Z. Failure modes: single front image → bad back +
failed rig; non-humanoid subject → rig rejects it; > 300k faces → remesh first.

### Example C — Restyle one mesh into color variants (retexture)

Intent: reuse an approved sword mesh as three material variants without
regenerating geometry.
```bash
curl -s https://api.meshy.ai/openapi/v1/retexture \
  -H "Authorization: Bearer $MESHY_API_KEY" -H 'Content-Type: application/json' \
  -d '{ "input_task_id": "<sword_task_id>",
        "text_style_prompt": "corroded bronze blade, verdigris patina, leather-wrapped grip",
        "enable_original_uv": true, "enable_pbr": true }'
```
Why: `enable_original_uv` preserves the existing UV layout so variants stay
UV-consistent; only the surface changes; 10 credits per variant vs. re-running a
full generation. Failure mode: model lacking UVs → weaker result (unwrap first).

## Sources (verified 2026-07-10)

- Text-to-3D API — https://docs.meshy.ai/en/api/text-to-3d
- Image-to-3D API — https://docs.meshy.ai/en/api/image-to-3d
- Multi-Image-to-3D API — https://docs.meshy.ai/en/api/multi-image-to-3d
- Retexture / Text-to-Texture API — https://docs.meshy.ai/en/api/retexture
- Remesh API — https://docs.meshy.ai/en/api/remesh
- Rigging & Animation API — https://docs.meshy.ai/en/api/rigging-and-animation
- Animation Library — https://docs.meshy.ai/en/api/animation-library
- Quickstart / auth — https://docs.meshy.ai/en/api/quick-start
- Rate limits — https://docs.meshy.ai/en/api/rate-limits
- API pricing — https://docs.meshy.ai/en/api/pricing
- Changelog — https://docs.meshy.ai/en/api/changelog
- Post-processing decision guide — https://docs.meshy.ai/en/webapp/guides/choosing/post-processing
- Prompt best practices — https://help.meshy.ai/en/articles/11972484-best-practices-for-creating-a-text-prompt
  and https://www.meshy.ai/blog/meshy-5-text-to-3d
- Ownership — https://help.meshy.ai/en/articles/10137554-what-is-the-ownership-of-the-generated-models
- Commercial use — https://help.meshy.ai/en/articles/9992001-can-i-use-my-generated-assets-for-commercial-projects
- Credit costs (help) — https://help.meshy.ai/en/articles/10000507-how-many-credits-does-each-generation-task-cost
- Plans/pricing — https://www.meshy.ai/pricing
