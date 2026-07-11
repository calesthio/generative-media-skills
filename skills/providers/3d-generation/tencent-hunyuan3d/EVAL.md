# EVAL — tencent-hunyuan3d

Answer key and scoring specification. The evaluated agent is given the user task
and `SKILL.md` only, never this file. Score the captured response against the
rubrics below. All facts verified 2026-07-10; if re-run later, re-verify volatile
items before penalizing an agent for a value that has since changed.

Scoring: each item lists **required points**, a **rubric**, and **critical failures**
(any one caps the item at a failing score regardless of other merits).

---

## Part 1 — Knowledge questions

### K1. Which Hunyuan3D models can be self-hosted from open weights, and which are API-only?

**Expected answer.**
- Open-weight / self-hostable: **Hunyuan3D-2.0** and its variants (**2mini, 2mv,
  Turbo/Fast, FlashVDM**), **Hunyuan3D-2.1** (fully open incl. training code), and
  the world models **HunyuanWorld-1.0** and **HY-World 2.0 / WorldMirror 2.0**.
- **API / closed-source only:** **Hunyuan3D-2.5**, **Hunyuan3D-PolyGen**,
  **Hunyuan3D-3.0**, **Hunyuan3D-3.1**.

**Required points:** names 2.1 (and/or 2.0) as the open object baseline; identifies
2.5/PolyGen/3.x as hosted/closed; does not claim 3.0 or PolyGen weights are
downloadable.

**Critical failures:** stating that Hunyuan3D-3.0 / 3.1 / 2.5 / PolyGen weights are
open/downloadable; claiming all Hunyuan3D is closed, or all is open.

### K2. What are the two stages of the pipeline and what does each produce?

**Expected answer.** Stage 1 **Hunyuan3D-DiT + ShapeVAE** — flow/diffusion over a
vectset latent, marching cubes → a **watertight untextured mesh**. Stage 2
**Hunyuan3D-Paint** — mesh-conditioned multi-view diffusion → material maps baked to
UVs. In **2.1** these are **PBR** maps (albedo/metallic/roughness, Disney Principled
BRDF, illumination-invariant albedo). The stages are modular and can run
independently (Paint can texture an imported mesh).

**Required points:** shape-then-texture separation; shape = DiT, texture = Paint; 2.1
outputs PBR; stages are independent.

**Critical failures:** describing it as a single end-to-end model; claiming text
input goes directly to 3D without an intermediate image; asserting 2.0 already
produced full PBR (2.1 is the first open PBR).

### K3. State the three license restrictions that most affect commercial deployment.

**Expected answer.**
1. **Territory** — grant is worldwide **excluding the EU, the UK, and South Korea**;
   use outside the Territory is prohibited.
2. **1,000,000 MAU gate** — above 1M MAU (preceding calendar month, on release date)
   the licensee must request a commercial license from Tencent; below it, commercial
   use is free **within the Territory**.
3. **Prohibited uses / attribution** — no training competing models, military, harm
   to minors, disinformation, malware, high-stakes automated decisions; requires
   NOTICE file and "Powered by Tencent Hunyuan" marking.

**Required points:** names EU + UK + South Korea specifically; the 1M-MAU number;
recognizes it is the **Tencent Hunyuan 3D Community License**, not MIT/Apache.

**Critical failures:** claiming the open weights are MIT/Apache/"free for any use";
omitting or fabricating the Territory (e.g. saying "US-only" or "China-only");
inventing a different MAU number (700M/100M is HunyuanVideo, not Hunyuan3D).

### K4. What GPU/VRAM does a self-hosted Hunyuan3D-2.1 need, and how does a 24 GB card cope?

**Expected answer.** `[fact]` 2.1 reports ~10 GB shape-only, ~21 GB texture-only,
~29 GB for both combined. A **24 GB card runs it by executing shape then texture
sequentially with model offload**, not both resident at once. 2mini (~5 GB) is the
low-VRAM option for shape on 8 GB cards.

**Required points:** ~29 GB combined; sequential/offload strategy for 24 GB; mentions
2mini as the low-VRAM path.

**Critical failures:** claiming 2.1 runs comfortably in ≤8 GB with textures; asserting
it needs no GPU.

### K5. What is the topology of the open 2.x meshes, and what post-processing does it imply?

**Expected answer.** Marching-cubes over a diffusion field → **watertight but dense,
uniformly triangulated, non-quad, no artist edge loops**; auto UVs. Implies
**retopology** before animation, **decimation** (+ normal-map baking) for real-time
budgets, UV re-layout for hand editing, and scale/orientation normalization. **PolyGen**
(hosted) exists to produce clean topology directly.

**Required points:** dense/triangulated/non-quad; retopo needed for animation;
decimation for real-time; names PolyGen or manual retopo as the topology fix.

**Critical failures:** claiming the meshes come game-ready with clean quad topology;
saying no post-processing is needed for animation.

### K6. Does ComfyUI natively texture Hunyuan3D meshes?

**Expected answer.** No. `[fact]` Native ComfyUI supports the **geometry stage only**
(Hunyuan3D-2, 2mv, 2mv-turbo → GLB); **texture/material generation is not native** and
needs a community wrapper (e.g. ComfyUI-Hunyuan3DWrapper).

**Critical failures:** claiming ComfyUI natively produces PBR-textured output.

---

## Part 2 — Production-decision questions

### D1. A game studio in Seoul, South Korea wants to self-host Hunyuan3D-2.1 for commercial asset production. Advise.

**Expected decision.** Self-hosting the open weights is **not licensed** — South
Korea is **excluded from the Territory** of the Community License. Do not proceed on
the open weights. Options: use a **hosted API whose own ToS permits the use** (and
confirm that ToS), or obtain a specific written agreement from Tencent. Recommend the
user get a legal read before shipping.

**Reasoning a strong answer shows:** recognizes the Territory exclusion as a hard
legal blocker (not a soft preference); does not hand-wave it; distinguishes the
license on weights from a host's ToS; refuses to assert a clearance it can't source.

**Penalize:** telling the studio to self-host anyway; ignoring the geography;
claiming the license permits it; inventing that a NOTICE file cures the Territory
problem.

### D2. A team needs to generate 2,000 textured props over the next month, marginal cost matters, all data is private, they're in the US and tiny (few thousand users), and they have one RTX 4090 (24 GB). Self-host or hosted API?

**Expected decision.** **Self-host Hunyuan3D-2.1.** High volume makes per-call API
fees expensive; privacy favors local; US + tiny user base means in-Territory and far
under 1M MAU → free commercial use with attribution; a 24 GB card runs 2.1 shape→
texture sequentially with offload.

**Reasoning:** connects volume→marginal cost, privacy→local, geography/MAU→license
fit, hardware→sequential execution. Adds the NOTICE/attribution obligation. May flag
that topology post-processing is still required.

**Penalize:** defaulting to a hosted API without weighing volume/privacy; missing the
license fit; claiming both stages must be resident (OOM) on 24 GB.

### D3. A user's blocker is that self-hosted 2.1 meshes have messy topology that breaks their rigging. What do you recommend?

**Expected decision.** Topology is the known weakness of marching-cubes output. Two
paths: (a) **retopologize** — manual or auto-retopo tool — before rigging; or (b) use
**Hunyuan3D-PolyGen** (hosted, art-grade quad/tri topology) which was built for this.
Switching to a different 2.x checkpoint will **not** fix topology.

**Reasoning:** identifies topology as inherent to the open pipeline, not a bad seed;
names PolyGen and/or retopo; explicitly rejects "try 2mini/turbo/2.5 instead" as a
topology fix (2.5 improves resolution, not artist topology).

**Penalize:** suggesting a different open checkpoint as the topology cure; claiming
the mesh is already animation-ready.

### D4. A user says "use Hunyuan3D 3.0's open weights to build an offline batch pipeline." Respond.

**Expected decision.** Flag the contradiction: **Hunyuan3D-3.0 is API-only / closed
weights** (verified 2026-07-10) — there are no downloadable 3.0 weights for an offline
pipeline. Offer alternatives: self-host the **open 2.1** offline, or build against the
**hosted 3.0 API** (which is online, not offline). Ask which constraint dominates
(offline vs 3.0-quality).

**Reasoning:** catches the false premise; explains the two-track split; proposes the
correct substitute for each intent.

**Penalize:** proceeding as if 3.0 weights are downloadable; inventing a 3.0 local
setup.

---

## Part 3 — Applied production tasks

### A1. Task: "Turn this single front photo of a sneaker into a game-ready 3D asset."

**Expected approach.** A complete answer should:
- Choose **Hunyuan3D-2.1** (open, PBR) or a hosted tier, with a stated reason.
- Note the **single front view limitation** — the back/sole will be hallucinated;
  recommend supplying additional views and using **2mv**, or accept/verify the
  invented geometry.
- Prep input: **background removal**, single clean subject, even lighting.
- Run **shape → PBR texture**; validate albedo has **no baked shadows**.
- **Post-process for "game-ready":** decimate to a poly budget, **bake normals** from
  the dense mesh, **retopologize** if the shoe deforms/animates, re-layout/validate
  UVs and the albedo/metallic/roughness set, normalize scale/orientation.
- Mention the **Community License** obligations if commercial.

**Essential characteristics of a good output:** treats "game-ready" as requiring
decimation + topology work, not raw generator output; addresses the single-view back
problem; separates shape and texture steps; flags the albedo-lighting pitfall.

**Rubric (5 pts):** model choice w/ reason (1); single-view/2mv handling (1);
shape-then-texture with PBR validation (1); concrete game-ready post-processing —
decimate/retopo/normals/UV/scale (1); license note if commercial (1).

**Critical failures:** presenting raw generator output as game-ready; ignoring that a
front-only photo can't determine the back/sole; recommending text-to-3D instead of
using the provided image.

### A2. Task: "We're an EU startup, 300k users, want to add AI 3D-asset generation to our product commercially. Plan it."

**Expected approach.** Lead with the **legal blocker**: an EU entity is **outside the
Territory** of the Hunyuan3D Community License, so **self-hosting the open weights is
not permitted**. Viable routes: a **hosted Hunyuan3D API whose ToS permits commercial
use from the EU** (verify that ToS), or a **different 3D model with EU-clear
licensing** if none qualifies. 300k users is under the 1M-MAU gate but that gate is
moot while the Territory exclusion applies. Recommend a legal review before launch.
Only after clearing licensing should the plan discuss which tier (quality/topology/
cost) fits.

**Essential characteristics:** license/geography analysis comes **first** and gates
everything; does not default to "just self-host 2.1"; separates the weights license
from a host's ToS; recommends legal confirmation; sequences technical choices after
compliance.

**Rubric (5 pts):** identifies EU Territory exclusion as the gating issue (2);
distinguishes hosted-ToS from open-weights license (1); notes the 1M-MAU gate but
correctly subordinates it to Territory here (1); defers technical/tier choice until
compliance is settled and advises legal review (1).

**Critical failures:** recommending self-hosting the open weights for an EU company;
asserting a definitive commercial clearance the agent cannot source; ignoring
geography entirely.

### A3. Task: "Review this generated asset for us." (agent is shown a Hunyuan3D mesh + textures)

**Expected approach.** Apply a structured review: silhouette/proportions from all
sides; **hallucinated back/side geometry**; floaters/non-manifold marching-cubes
artifacts; geometry density vs need; **topology suitability** (static vs animated);
**PBR correctness** (albedo lighting-free; plausible metallic/roughness); UV seams/
stretching and texture resolution; scale/orientation normalized. Conclude with a
**fitness-for-purpose verdict** tied to the intended use (prop vs hero vs animated).

**Rubric (5 pts):** checks geometry all-around incl. unseen faces (1); topology vs
animation need (1); PBR/albedo-lighting check (1); UV/texture-resolution check (1);
purpose-tied verdict rather than a generic "looks good" (1).

**Critical failures:** approving without checking the back/unseen faces; not
mentioning topology for an animation use case; declaring PBR correct without checking
albedo for baked lighting.

---

## Global critical failures (any one is a serious miss on any item)

- Treating the open weights as MIT/Apache or "free for any use."
- Omitting or fabricating the **EU/UK/South Korea Territory exclusion** when
  geography is relevant.
- Claiming closed tiers (2.5, PolyGen, 3.0, 3.1) are self-hostable.
- Presenting raw marching-cubes output as animation- or game-ready without
  retopology/decimation.
- Recommending text-to-3D when a usable reference image was provided.
- Asserting a legal commercial clearance the agent cannot ground in the license or a
  host's ToS.
