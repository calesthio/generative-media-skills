# EVAL — meshy-3d

Answer key and scoring spec for the `meshy-3d` skill. The evaluated agent
receives the user task plus `SKILL.md` only. Score its captured response against
the rubrics below. Do not expose this file to the agent under test.

Volatile facts reflect verification date **2026-07-10**; if Meshy has shipped a
new model version or repriced since, update expected answers before scoring.

Scoring per item: **Pass** (all required points, no critical failure),
**Partial** (most required points, no critical failure), **Fail** (missing core
points or commits any critical failure). Critical failures cap the item at Fail
regardless of other merits.

---

## Part 1 — Knowledge questions

### K1. Why is Text-to-3D a two-step API, and what are the steps?

**Expected:** Text-to-3D separates **preview** (untextured geometry) from
**refine** (texturing). You POST `mode:"preview"` with a prompt, get a task ID,
approve the geometry, then POST `mode:"refine"` with `preview_task_id` to apply
texture. Purpose: evaluate/iterate shape cheaply before paying to texture.

**Required points:** preview = geometry only; refine = texture; refine needs the
preview's task ID; the value is cheap geometry iteration before texturing.

**Critical failure:** claiming it is a single call, or that preview already
includes final textures, or inventing a different endpoint structure.

### K2. Authentication, base URL, and tier requirement.

**Expected:** Bearer token `Authorization: Bearer <API key>`; key created at
meshy.ai/settings/api and shown once. Base URL `https://api.meshy.ai/openapi/`
(Text-to-3D under `v2`, others `v1`). **API requires a Pro tier or higher**;
free tier cannot create API tasks.

**Required points:** Bearer header; Pro+ required for API; key stored securely.

**Critical failure:** stating the free tier can use the API, or inventing a
query-string API-key scheme.

### K3. How does an agent know a task finished?

**Expected:** Tasks are asynchronous. Three mechanisms: **polling** the
`GET .../:id` endpoint until status is terminal; **SSE streaming** at
`.../:id/stream`; or **webhooks**. Status values: `PENDING`, `IN_PROGRESS`,
`SUCCEEDED`, `FAILED`, `CANCELED`, with `progress` 0–100.

**Required points:** async job; poll/stream/webhook; correct terminal statuses.

**Critical failure:** describing generation as synchronous/blocking, or omitting
that a task ID is returned first.

### K4. What are the rigging input constraints?

**Expected:** Input must be a **textured humanoid** (clear limbs/body), provided
as `input_task_id` or a **GLB** `model_url`; character must face **+Z**; **≤
300,000 faces** when using `input_task_id` (remesh first if larger);
`height_meters` default 1.7. Untextured meshes and non-humanoids are unsuitable.
Output: rigged FBX + GLB plus basic walk/run animations.

**Required points:** textured humanoid; GLB; ≤ 300k faces (remesh if over); +Z
facing; height parameter.

**Critical failure:** claiming Meshy rigs arbitrary non-humanoid objects, or
omitting the 300k-face limit while asserting any mesh can be rigged directly.

### K5. What controls topology and poly count, and what does `decimation_mode`
do relative to `target_polycount`?

**Expected:** `topology` = `triangle` (default) or `quad`; `target_polycount`
100–300,000 (default 30,000). `decimation_mode` (1–4) is adaptive reduction and
**overrides** `target_polycount`. Remesh can re-topologize an existing model.
`quad` is quad-dominant reconstruction, not artist-authored edge loops.

**Required points:** the two params and ranges; `decimation_mode` overrides
`target_polycount`; quad ≠ hand-authored topology.

**Critical failure:** stating quad output gives production edge-loop topology,
or that `target_polycount` guarantees clean topology.

### K6. Ownership/licensing difference between paid and free plans.

**Expected:** Paid = full private ownership and right to distribute/sell,
**provided** inputs don't infringe others' copyright and you don't publish the
model to the public Meshy Community (publishing removes the private-ownership
protection). Free = **CC BY 4.0** (may sell but must attribute Meshy). Using
copyrighted reference inputs creates risk regardless of plan.

**Required points:** paid private ownership with the two conditions; free = CC
BY 4.0 attribution; input-copyright caveat.

**Critical failure:** claiming free-tier assets are unrestricted/no-attribution,
or that paid ownership is unconditional even with infringing inputs.

### K7. Which texture features are Meshy-6/latest only, and what does
`remove_lighting` do?

**Expected:** `hd_texture` (4K base color), `remove_lighting`, and (image-to-3D)
`image_enhancement` are Meshy-6/latest only. `remove_lighting` (default `true`)
bakes out captured highlights/shadows so the engine can relight the asset; under
`hd_texture`, base color is 4K but PBR maps remain 2K.

**Required points:** hd_texture/remove_lighting are Meshy-6-only;
remove_lighting removes baked lighting for relighting.

**Critical failure:** claiming these work on legacy models, or that
`remove_lighting` deletes textures.

---

## Part 2 — Production-decision questions

### D1. A user wants a 3D model of "a busy medieval marketplace with stalls,
crates, and merchants." Advise.

**Expected decision:** Do **not** generate the whole scene as one Meshy asset.
Text-to-3D/image-to-3D reconstruct a **single subject** best; generate parts
(stall, crate, barrel, a merchant character) separately and compose the scene in
the engine (Unity/Unreal/Blender). Warn that "merchants" (plural humans) invites
fused/extra limbs — generate one character at a time.

**Reasoning to demonstrate:** single-subject limitation; scene assembly happens
downstream; plural-noun/limb failure mode; per-asset poly budgeting.

**Penalize:** advising a single "marketplace" prompt as if Meshy builds scenes;
ignoring the plural-character limb risk.

### D2. The generated mesh looks correct but the texture has baked-in shadows and
looks flat in Unreal. What do you change — regenerate or not?

**Expected decision:** **Do not regenerate geometry.** Re-run the texture stage
(refine/retexture) with `remove_lighting: true` (Meshy-6) to strip baked
lighting and `enable_pbr: true` so Unreal gets metallic/roughness/normal maps
for relighting. Consider `hd_texture` only if it's a close-up hero asset.
Optionally `enable_original_uv` on retexture to preserve UVs.

**Reasoning:** geometry is fine, so keep it; texture problems are fixed in the
texture stage; PBR + relighting is why it looked flat; cost is ~10 credits vs a
full regen.

**Penalize:** regenerating geometry to fix a texture; not mentioning PBR or
remove_lighting; suggesting the mesh itself is broken.

### D3. A user needs a mechanical bracket with exact 42.0 mm mounting-hole spacing
for 3D printing. Is Meshy appropriate?

**Expected decision:** **No** (or: not as the source of truth). Generative meshes
are approximate and not dimensionally exact; use CAD (Fusion/SolidWorks/FreeCAD)
for tolerance-critical parts. If Meshy is used for organic/aesthetic parts, run
**remesh** and validate manifoldness/wall thickness in a slicer — but exact hole
spacing must come from CAD. Meshy has no dimensional-tolerance guarantee.

**Reasoning:** distinguishes generative approximation from parametric CAD;
knows Meshy offers printability/remesh but no tolerance guarantee.

**Penalize:** confidently promising Meshy will hit exact dimensions; ignoring
manifold/validation needs for print.

### D4. Batch job: generate 400 background props overnight on a Pro plan.
Design the throughput approach and flag pitfalls.

**Expected decision:** Gate concurrency to the **Pro queue limit of 10**
concurrent tasks; respect **20 rps**; retry `429 NoMoreConcurrentTasks` /
`RateLimitExceeded` with backoff. Prefer **webhooks** (or streaming) over tight
polling. Use `standard`/`lowpoly` with modest `target_polycount` and request
only needed `target_formats` to save credits/time; skip `hd_texture` for
background props. **Download outputs within the ~3-day retention window** and
re-host. Estimate credits up front (Pro = 1,000/mo; a textured Meshy-6
text-to-3D ≈ 30 credits, so 400 assets far exceeds one month's Pro credits —
flag the budget).

**Reasoning:** tier-aware concurrency; 429 handling; retention; credit budgeting
math; cost-appropriate settings for throwaway props.

**Penalize:** firing 400 unbounded parallel requests; ignoring the concurrency
limit; not addressing retention or the credit budget overshoot.

### D5. User has a single front-facing photo of a toy and wants a rig-ready
character. Route the workflow.

**Expected decision:** A single front photo underconstrains the back → image-to-
3D will hallucinate unseen sides and the rig may bind bad geometry. Prefer
**multi-image-to-3D** with front/side/back of the *same* object; keep textured
on; request an **A/T pose** (`pose_mode`). Then verify **humanoid, textured, ≤
300k faces (remesh if over), +Z facing** before **rigging**, then animate by
`action_id`. If the toy is non-humanoid, Meshy rigging won't apply — rig in
Blender.

**Reasoning:** single-view limitation; multi-image to constrain geometry; pose
for rigging; rig prerequisites; non-humanoid escape hatch.

**Penalize:** rigging an untextured or non-humanoid mesh; ignoring the
single-view hallucination risk; skipping the face-count/pose prerequisites.

---

## Part 3 — Applied production tasks

### A1. Write the two API calls to produce a textured, game-ready 20k-tri
"ornate brass steampunk compass" as GLB with PBR, Meshy-6.

**Expected approach:** A preview call (`mode:"preview"`, geometry prompt,
`ai_model:"meshy-6"`, `target_polycount:20000`, `topology:"triangle"`,
`target_formats:["glb"]`) then, after `SUCCEEDED`, a refine call
(`mode:"refine"`, `preview_task_id`, `enable_pbr:true`, a **material-focused**
`texture_prompt`). Correct endpoint `/openapi/v2/text-to-3d`, Bearer auth,
polling between steps.

**Essential characteristics:**
- Geometry description in preview, materials in the texture prompt (not both
  jumbled).
- Poly budget set at preview; PBR enabled at refine; GLB requested.
- Explicit two-step sequence with the preview task ID threaded into refine.
- Mentions polling until `SUCCEEDED`.

**Rubric:** Pass = both calls correct with clean geometry/texture split and
poll step. Partial = correct structure but mixes texture words into geometry or
omits polling. Fail = single call, wrong endpoint, or PBR/GLB omitted.

**Critical failures:** one-shot generation; putting the material description in
the preview prompt and nothing in refine; hardcoding the API key in the body.

### A2. A user's generated dragon mesh is 480,000 faces and they want to animate
it. Give the corrective plan.

**Expected approach:** 480k exceeds the 300k rigging cap **and** a dragon is
non-humanoid. (1) **Remesh** to ≤ 300k (e.g. `target_polycount` 100k–150k,
`topology` to taste). (2) But rigging targets **humanoids** — a dragon likely
fails Meshy auto-rig; recommend rigging/animating in Blender/Maya, or accept
only if it reads as a clearly-limbed humanoid form. Ensure the mesh is textured
and A/T posed if attempting Meshy rig.

**Essential characteristics:** identifies both the face-count cap and the
humanoid constraint; remesh as the fix for count; honest that non-humanoid rig
is out of scope for Meshy auto-rig.

**Rubric:** Pass = flags both the 300k cap (remesh) and the humanoid limitation
with a realistic alternative. Partial = fixes face count but claims Meshy will
auto-rig the dragon. Fail = ignores the cap, or asserts Meshy rigs any creature.

**Critical failure:** telling the user to send a 480k non-humanoid mesh straight
to Meshy rigging and expecting success.

### A3. Review this plan and correct any errors: "Free-plan user will generate 50
assets via the API, publish them to the Meshy Community for backup, and sell
them with no attribution."

**Expected approach:** Multiple errors. (1) **Free tier cannot use the API** —
API requires Pro+. (2) Free-plan assets are **CC BY 4.0** — selling is allowed
but **attribution is required**, so "no attribution" is wrong. (3) The Meshy
Community is a **public** publishing surface, not private backup; publishing has
ownership/visibility implications (and for paid users removes private ownership)
— it is not a storage/backup mechanism, and CDN outputs are only retained ~3
days, so plan real downloads/hosting.

**Essential characteristics:** catches the free-tier-API blocker; the
attribution requirement; the "community = backup" misconception and retention.

**Rubric:** Pass = catches all three (API tier, attribution, community/backup +
retention). Partial = catches two. Fail = endorses the plan or catches ≤ one.

**Critical failure:** affirming that a free user can hit the API and sell without
attribution.

### A4. The user says text-to-3D keeps giving their "two knights dueling" prompt a
fused two-headed figure. Diagnose and rewrite.

**Expected approach:** Root cause = **multiple subjects / plural nouns** in one
prompt; text-to-3D handles a single subject and fuses multiples. Fix: generate
**one** knight (singular, ~3–6 concrete details, clear pose), generate the
second separately if needed, and **compose the duel in the engine**. Optionally
request `a-pose`/`t-pose` if these will be rigged/posed. Provide a rewritten
single-subject prompt.

**Essential characteristics:** identifies plural/multi-subject as the cause;
prescribes single-subject generation + engine composition; supplies a concrete
singular rewrite with materials in the (later) texture stage.

**Rubric:** Pass = correct diagnosis + singular rewrite + composition advice.
Partial = diagnosis without a usable rewrite, or rewrite that still describes two
figures. Fail = blames the model quality and just says "try again" with another
multi-subject prompt.

**Critical failure:** recommending more render-quality buzzwords as the fix while
keeping two subjects in one prompt.

---

## Cross-cutting critical failures (cap any item at Fail)

- Treating Meshy generation as synchronous, or omitting the task-ID/poll model.
- Asserting exact dimensional accuracy or guaranteed watertight/manifold output.
- Claiming the free tier can use the API, or that free assets need no
  attribution.
- Rigging untextured or non-humanoid meshes, or ignoring the 300k-face cap.
- Fixing texture problems by regenerating geometry (wasted credits, lost mesh).
- Quoting credit costs, model versions, or limits as permanent without noting
  they are volatile / dated (verification date 2026-07-10).
- Putting the API key in a URL/query string or hardcoding it in shared code.
