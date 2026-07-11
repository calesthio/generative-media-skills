# EVAL — tripo-3d

Answer key and scoring spec for the `tripo-3d` skill. The evaluated agent receives only the user task and
`SKILL.md`. The evaluator scores the captured response with this file. Do not expose this file to the agent
under test. Facts here were verified 2026-07-10; Tripo changes often, so treat exact numbers as
point-in-time and score reasoning as heavily as recall.

---

## Part A — Knowledge questions

### A1. Describe the Tripo API task lifecycle.
**Expected:** It is an **asynchronous task** API. Submit `POST /v2/openapi/task` with a `type` field →
receive a `task_id` → **poll** `GET /v2/openapi/task/{task_id}` until `status` is terminal → read output
model URLs from the response `output`. Base URL `https://api.tripo3d.ai/v2/openapi`; auth via
`Authorization: Bearer <API_KEY>`.
**Required points:** async/task-based; create then poll (or webhook); statuses progress
queued→running→success (failed/cancelled etc.); output URLs read on success; bearer-token auth.
**Disqualifying:** claims it is a synchronous request that returns the mesh in one call; invents a
GraphQL/WebSocket-only interface.

### A2. What are the three primary generation input modes, and which gives the most control?
**Expected:** `text_to_model`, `image_to_model`, `multiview_to_model`. **Multiview** (ordered
front/left/back/right, front required, ≥2 views) gives the most geometric fidelity/control because it
constrains the unseen sides; image-to-3D beats text; text is the most ambiguous about hidden geometry.
**Required points:** names all three task types; ranks multiview ≥ image > text for control/fidelity;
front view mandatory for multiview.
**Disqualifying:** says text-to-3D is most faithful; claims multiview needs exactly 4 real photos.

### A3. Name the current generation model versions and when you'd choose each.
**Expected:** **v3.0** (`v3.0-20250812`, stable general default, high detail, retopo later); **v3.1**
(`v3.1-20260211`, denser geometry + stronger PBR, "hero" detail, more cost/time); **P1** (Smart Mesh P1.0,
native-3D-diffusion, **game-ready low-poly** with `face_limit` 48–20,000 and `orientation` control, fast,
premium credits). Legacy Turbo-v1.0 / v1.4 / H2 exist.
**Required points:** at least v3.0/v3.1/P1 with a correct distinguishing reason each; P1 = controllable
low-poly + orientation; drive API off exact `model_version` string.
**Disqualifying:** claims P1 is a cheap/legacy model; says v3.1 is lower quality than v3.0.

### A4. How is a Tripo asset rigged and animated, and what should precede paying to rig?
**Expected:** Run **check_riggable** (free) first to confirm the mesh supports auto-rigging; then
**rig_model** (25 cr; `out_format` glb/fbx, `rig_type`, `spec`); then **retarget_animation** (10 cr per
animation) with `"preset:<name>"` values (idle/walk/run/jump/climb/dive/etc., plus quadruped/serpentine/etc.
variants). Expect an upright, symmetric, limb-separated single character for best results.
**Required points:** pre-rig check gates rigging; three-stage check→rig→retarget flow; preset animation
naming; humanoid/quadruped distinction.
**Disqualifying:** rigs before checking riggability; claims arbitrary custom motion-capture upload is the
documented path.

### A5. What formats does Tripo output/convert to, and how do they map to targets?
**Expected:** Native generation output is **GLB**. `convert_model` targets **GLTF, USDZ, FBX, OBJ, STL,
3MF**. Mapping: Unity/Unreal → FBX or glTF/GLB; Blender → GLB/glTF or FBX; USD/AR Quick Look → USDZ; 3D
printing → STL (no color) or 3MF (keeps color/material).
**Required points:** GLB native; convert to the listed set; correct printing (STL/3MF) and AR (USDZ) mapping.
**Disqualifying:** claims STL carries textures/color; omits that conversion is a separate chained task.

### A6. Explain Tripo's credit model and rate/concurrency limits.
**Expected:** Credits, **$1 = 100 credits**, **300 free credits (~2 weeks)** for new accounts; each task
returns exact `consumed_credit`. Example prices: v3.x text 10/20 (no-tex/tex), image 20/30; P1 text 30/40,
image 40/50; add-ons detailed texture +10, smart low-poly +10, quad +5, parts +20; rig 25, retarget 10/anim,
convert 5. **429** on rate-limit exceed; **concurrent-task** limits are plan-dependent (free ≈ 1). Errors
carry `code`/`message`/`suggestion`.
**Required points:** credit basis + $1=100; free-credit grant; texture toggle changes cost; 429 + plan-based
concurrency; per-task `consumed_credit`.
**Disqualifying:** quotes fixed dollar-per-model with no dating/uncertainty; says there are no concurrency
limits.

### A7. Who owns / how is a generated model licensed?
**Expected:** Free/Basic tier → models typically **published publicly** under a **CC BY 4.0**-style license
(attribution; not private/exclusive). Paid plans → **private** models + **commercial-use rights** to the
generated asset. Tripo's entity retains IP in its software/models/tech. The user is still responsible for
input rights (no copyrighted/branded/real-person inputs they lack rights to). Confirm current Terms; don't
overstate ownership.
**Required points:** free = public/attribution, not exclusive; paid = private + commercial; platform retains
its own IP; input-rights responsibility; verify terms.
**Disqualifying:** asserts "you fully own it with unrestricted commercial rights" regardless of plan;
ignores input-side infringement risk.

---

## Part B — Production-decision questions

### B1. A studio needs 200 game props at ~5k tris each, delivered as FBX, this week.
**Expected decision:** Batch via the API, not the web UI. Use **P1** with an explicit `face_limit (~5000)`
per prop so meshes land at budget instead of needing decimation; `texture:true`, `pbr:true`. Generate from
concept images (image_to_model) where available for fidelity. Chain a **convert_model → FBX** task per
asset. Respect **concurrency limits** (queue to the plan's cap; handle **429** with backoff), track
`consumed_credit`, and download outputs promptly (URLs expire). Budget credits up front (~P1 image 40–50 cr +
convert 5 each).
**Strong-answer reasoning:** picks model by *output budget* (P1 low-poly) not just "best quality"; treats
concurrency/429 as a real constraint; plans conversion + storage; estimates cost.
**Penalize:** choosing v3.1 hero-detail then hand-decimating 200 assets; ignoring concurrency/429; assuming
synchronous calls; forgetting FBX conversion is a separate task.

### B2. Client wants a rigged, walk-cycling humanoid character for a mobile game.
**Expected decision:** Generate the character (image/multiview for a consistent, upright, symmetric mesh),
verify quality, then **check_riggable** → **rig_model** (out_format fbx/glb) → **retarget_animation** with
`preset:walk` (add idle/run as needed). Because it will **deform**, insist on clean topology: use `quad`
/ `smart_lowpoly` so skinning doesn't tear on raw triangulation. Confirm a **paid plan** for private +
commercial rights.
**Strong-answer reasoning:** gates rigging on riggability; demands deform-friendly topology; ties licensing
to a paid plan; uses preset animation correctly.
**Penalize:** rigging a scene/multi-object mesh; skipping check_riggable; shipping raw triangulated topology
for a deforming character; assuming free-tier output is fine for a commercial game.

### B3. Single image-to-3D keeps producing a blurry, wrong-looking back and baked-in shadows.
**Expected decision:** Root causes: single-image input hallucinates unseen sides, and harsh reference
lighting bakes shadows into texture/geometry. Fixes: switch to **multiview_to_model** with consistent
front/back/left/right renders; re-shoot/clean the reference (neutral even lighting, plain background,
centered subject); use `enable_image_autofix`; set `orientation`/`texture_alignment`; if only the surface is
wrong, keep the geometry and re-run **texture_model**. Vary `model_seed` before rewriting anything.
**Strong-answer reasoning:** attributes the artifact to input/mode, not "the model is bad"; escalates
single→multiview; separates geometry vs texture repair; changes input before spending on higher tiers.
**Penalize:** just jumping to the most expensive model; regenerating from scratch when only texture is wrong;
no mention of lighting/background of the input.

### B4. A client wants to 3D-print and sell figurines generated on their free Tripo account.
**Expected decision:** Two blockers. (1) **Licensing:** free-tier output is public/CC-BY-attribution and not
commercial-exclusive — move to a **paid plan** for private + commercial rights, and confirm the current
Terms; also verify the *design* isn't infringing and that inputs were rights-clean. (2) **Print-readiness:**
verify the mesh is **watertight/manifold**, check scale (`auto_size`), wall thickness, flipped normals;
export **STL** (color lost) or **3MF** (color kept). Flag that this is a rights/quality gate, not just a
generate-and-sell step.
**Strong-answer reasoning:** raises licensing *and* manifold/printability; distinguishes STL vs 3MF;
verifies inputs and terms rather than asserting ownership.
**Penalize:** "free plan is fine, you own it, just print and sell"; ignores manifold/scale checks; no
STL/3MF distinction.

---

## Part C — Applied production tasks

### C1. Write the API call plan (with a concrete request body) to generate a stylized low-poly treasure chest for Unity from a text prompt, targeting ~3k tris with PBR, then export FBX.
**Expected approach:** A `text_to_model` (P1, or v3.x + face_limit) create task with a concrete object-level
prompt, `face_limit ~3000`, `texture:true`, `pbr:true`, optional `negative_prompt`; poll until success; then
a chained `convert_model` → FBX. Example body:
```json
{ "type":"text_to_model", "model_version":"p1",
  "prompt":"a low-poly stylized wooden treasure chest with iron bands and a brass lock, closed lid",
  "negative_prompt":"extra parts, floating geometry, text",
  "face_limit":3000, "texture":true, "pbr":true }
```
then poll `GET /v2/openapi/task/{task_id}`, then `{ "type":"convert_model", "original_model_task_id":"...",
"format":"FBX" }`.
**Essential characteristics:** correct `type` and generation task; object-level prompt (subject + material +
form + style); `face_limit` for the budget; PBR on for a lit Unity pipeline; async poll; FBX as a **separate
chained** convert task referencing `original_model_task_id`.
**Rubric (5 pts):** correct async create+poll flow (1); valid `text_to_model` body with prompt + face_limit +
texture/pbr (2); FBX via chained convert_model by task id (1); a sensible model choice for a low-poly budget
with brief justification (1).
**Critical failures:** treats it as a synchronous call; puts scene/multi-object language in the prompt;
"exports FBX directly" with no convert task; hallucinated endpoints/params.

### C2. Given a generated GLB that is ~900k tris with good shape but harsh baked lighting and messy triangulation, propose the exact repair pipeline (no full regeneration).
**Expected approach:** Keep the geometry, fix in place: (1) **smart_lowpoly** (with `face_limit` to target,
`quad:true` for cleaner edge flow, `bake:true`) to hit budget and improve topology; (2) **texture_model** to
re-texture away the baked lighting (supply a clean `text_prompt`/`style_image`, `pbr:true`); (3) if parts
need separating, **mesh_segmentation**; (4) **convert_model** to the delivery format. All reference the
original task id — no re-generation.
**Rubric (5 pts):** identifies re-use of task id / no regeneration (1); smart_lowpoly for density+topology
with face_limit/quad (2); texture_model to fix baked lighting rather than regenerating geometry (1); correct
ordering + final convert (1).
**Critical failures:** regenerates from scratch; tries to fix baked lighting by re-rolling geometry seeds;
invents a nonexistent "remove lighting" flag; applies rigging to fix topology.

### C3. Draft the licensing/rights guidance you'd give a user before they build a commercial AR product using Tripo assets.
**Expected approach:** (1) Generate on a **paid plan** so assets are **private** and carry **commercial
rights**; free-tier output is public/CC-BY-attribution. (2) **Verify the current Terms** (tripo3d.ai/terms) —
don't assert unrestricted ownership; the CC BY commercial-with-attribution nuance is easy to misstate. (3)
The user is responsible for **input rights** — no copyrighted/branded characters, trademarks, or identifiable
real people without rights. (4) Note Tripo retains IP in its own software/models. (5) For USD/AR delivery,
export **USDZ**. Keep it as a checklist and recommend the user confirm with their own counsel for a
commercial launch.
**Rubric (5 pts):** paid-plan → private+commercial (1); verify terms / no overclaiming ownership (1);
input-rights responsibility (1); platform retains its IP (1); correct AR export format + practical framing
(1).
**Critical failures:** flatly asserts "you own it, unlimited commercial use" without plan/terms caveats;
ignores input infringement; recommends free tier for a commercial launch; treats generation as a rights
launder for branded/real-person inputs.

---

## Scoring guidance
- **Weight reasoning over recall.** Exact credit numbers, `model_version` date strings, and tier prices are
  volatile (verified 2026-07-10); a correct process with a "verify current value" caveat scores full marks,
  and a confidently wrong *un-dated* absolute is worse than an approximate dated one.
- **Automatic fail across any section** if the agent: (a) treats the API as synchronous / skips polling;
  (b) asserts unrestricted ownership/commercial rights with no plan or terms check; (c) ships a deforming/
  rigged asset on raw triangulated topology with no retopo/quad step; (d) invents endpoints, task types, or
  parameters not in the documented set; or (e) encourages laundering copyrighted/branded/real-person inputs
  into "generated" assets.
