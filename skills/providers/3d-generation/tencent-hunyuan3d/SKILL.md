---
name: tencent-hunyuan3d
description: >-
  Generate 3D assets with Tencent's Hunyuan3D family — open-weight self-hosted
  models (Hunyuan3D-2.0/2.1 and HunyuanWorld / HY-World for scenes) and the
  hosted, closed API tiers (2.5, PolyGen, 3.0/3.1 via Tencent Cloud and third-party
  hosts). Use when a task involves image-to-3D or text-to-3D mesh generation, the
  shape-then-texture (DiT + Paint / PBR) workflow, choosing between self-hosting
  and a hosted API, checking the Community License's Territory (EU/UK/South Korea)
  and 1M-MAU commercial gate, sizing GPU/VRAM for local inference, ComfyUI
  integration, or reviewing and post-processing (retopology, UVs, decimation) the
  meshes these models produce. Not for image, video, or general LLM tasks.
---

# Tencent Hunyuan3D

Hunyuan3D is Tencent's family of generative 3D models. Its defining trait is a
**two-stage, shape-then-texture pipeline**: one model generates untextured
geometry from an image (or text), a second model paints materials onto that
geometry. The family spans **open-weight releases you can self-host** and
**closed tiers available only through a hosted API**. Choosing correctly between
those two tracks — and reading the license before you ship anything commercial —
is the core production judgment this skill supports.

**All version, license, hardware, and access facts below were verified 2026-07-10.**
These are volatile; re-verify against first-party repos before relying on them.
Facts are labeled `[fact]` (documented in a primary source), `[first-party claim]`
(Tencent's own benchmark/marketing, not independently reproduced), or `[heuristic]`
(production judgment, not a documented guarantee).

---

## When this skill applies

Use it when the request involves:

- generating a 3D **object/asset** from an image or text prompt;
- generating a 3D **scene/world** (panorama, explorable environment) — the
  HunyuanWorld / HY-World branch;
- deciding **self-host vs hosted API**, or which Hunyuan3D tier fits;
- **license/compliance** questions (commercial use, Territory, MAU, attribution);
- **GPU sizing** for local inference or ComfyUI setup;
- **reviewing or post-processing** Hunyuan3D output (topology, UVs, PBR maps).

Do **not** use it for 2D image generation (that is HunyuanImage), video
(HunyuanVideo), or the Hunyuan text LLMs (Hunyuan/Hy3) — those are separate model
families that happen to share the "Hunyuan" brand.

---

## The version landscape (verified 2026-07-10)

Two tracks. Getting the track right is the first decision, because it determines
cost model, control, and legal footing.

### Track A — Open-weight, self-hostable (download from GitHub + Hugging Face)

| Model | Released | Params (shape / paint) | What it adds | License |
|---|---|---|---|---|
| **Hunyuan3D-2.0** | Jan 2025 | DiT-v2-0 ~1.1B / Paint-v2-0 ~1.3B (+ Delight) | Original open two-stage object model | Tencent Hunyuan 3D 2.0 Community License |
| **Hunyuan3D-2mini** | Mar 18 2025 | DiT-v2-mini 0.6B | Low-VRAM shape (~5 GB) | same 2.0 license |
| **Hunyuan3D-2mv** | Mar 18 2025 | DiT-v2-mv ~1.1B | **Multi-view** shape input (front+back+sides) | same 2.0 license |
| **-Turbo / -Fast + FlashVDM** | Mar 19 2025 | distilled variants of above | Step/guidance distillation; fast decode | same 2.0 license |
| **Hunyuan3D-2.1** | Jun 13–14 2025 | DiT-v2-1 ~3.0B / Paint-v2-1 ~1.3–2B | **First fully open PBR** + full training code | Tencent Hunyuan 3D 2.1 Community License |
| **HunyuanWorld-1.0** | Jul 26 2025 | — | Open **scene/world** gen: panorama proxy → layered mesh + 3DGS, 360° | Tencent Hunyuan community license |
| **HY-World 2.0 / WorldMirror 2.0** | Apr 16 2026 | — | Text/image/multiview/**video** → meshes + 3DGS + point clouds; editable, engine-ready | open (GitHub + HF) |

`[fact]` **Hunyuan3D-2.1 is the reference open baseline for object generation.**
It is the version to self-host when you need PBR and want everything (weights *and*
training code) under an open license. Sources: GitHub `Tencent-Hunyuan/Hunyuan3D-2.1`,
arXiv 2506.15442.

`[fact]` **FlashVDM** accelerates the shape decoder: Tencent reports a Lightning
Vectset Decoder with >45x speedup and Progressive Flow Distillation sampling in as
few as 5 steps (`[first-party claim]` on the speedup magnitude). Enable via the
turbo checkpoints / `--enable_flashvdm`.

### Track B — Closed, hosted API only (no downloadable weights, verified 2026-07-10)

| Model | Released | Distinguishing capability | Availability |
|---|---|---|---|
| **Hunyuan3D-2.5** | Apr 2025 | ~10B params, 1024 geometric resolution, 4K textures, bump maps, "LATTICE" shape model, skeletal skinning | Tencent Cloud API + 3rd-party hosts |
| **Hunyuan3D-PolyGen** | Jul 8 2025 | **Art-grade topology** — clean quad/tri meshes, autoregressive mesh (BPT tokenization), intelligent retopology | API / Tencent internal game pipelines |
| **Hunyuan3D-3.0** | Sep 2025 | 3D-DiT "hierarchical sculpting," ~1536³ resolution | Tencent Cloud API |
| **Hunyuan3D-3.1** | later 2025/2026 | Hosted refinement of 3.0 | Tencent Cloud + hosts (fal, Replicate, etc.) |

`[fact]` The 2.5 / PolyGen / 3.x tiers are **closed-source**: accessible only
through hosted APIs, not as weights. The Tencent Cloud International Station and
Hunyuan3D API for overseas users launched **Nov 26 2025**. If a task says "use the
open weights" and also "use 3.0/PolyGen," that is contradictory — surface it.
Sources: Tencent Cloud doc 1284/75539; hunyuan3d.cc version notes; Tencent press.

`[heuristic]` **PolyGen exists specifically to solve the biggest weakness of the
open 2.x meshes: topology.** If your blocker is that self-hosted meshes are dense
triangle soup, PolyGen (hosted) or a manual retopology pass is the answer — not a
different 2.x checkpoint.

---

## The license — read this before any commercial deployment

This is the single most consequential production fact in the family. The open
weights are **not** MIT/Apache. They ship under the **Tencent Hunyuan 3D Community
License Agreement** (versioned per model, e.g. "TENCENT HUNYUAN 3D 2.1 COMMUNITY
LICENSE AGREEMENT"). `[fact]` Verified 2026-07-10 from the LICENSE files in
`Tencent-Hunyuan/Hunyuan3D-2` and `Hunyuan3D-2.1`.

Three restrictions that routinely surprise people:

1. **Territory exclusion `[fact]`.** The license grant is worldwide **excluding
   the European Union, the United Kingdom, and South Korea.** Use "outside the
   Territory" is prohibited. A team in Berlin, London, or Seoul is not licensed to
   use the open weights under this agreement. This is a hard legal blocker, not a
   preference — flag it whenever a user's location or target market is in those
   regions.

2. **1 million MAU commercial gate `[fact]`.** If, on the model's release date, the
   products/services made available by or for the licensee had **> 1,000,000
   monthly active users** in the preceding calendar month, the licensee **must
   request a separate license from Tencent** (email hunyuan3d@tencent.com with
   company name, sector, and use case). Below 1M MAU, commercial use is permitted
   **within the Territory** at no charge.

3. **Prohibited uses `[fact]`.** Among ~20 clauses: no use to improve competing AI
   models; no military use; no generating content that harms minors; no election
   disinformation; no malware; no undisclosed AI-generated content; no "high-stakes
   automated decisions affecting an individual's safety, rights, or wellbeing."

**Attribution `[fact]`:** redistribution requires a NOTICE file
("Tencent Hunyuan 3D 2.1 is licensed under the Tencent Hunyuan 3D 2.1 Community
License Agreement, Copyright © 2025 Tencent."), and products are expected to be
marked "Powered by Tencent Hunyuan."

`[heuristic]` **The hosted API does not erase these questions — it changes which
document governs.** Tencent Cloud and third-party hosts (fal, Replicate, etc.) each
impose their own Terms of Service. Do not assume "hosted = unrestricted commercial";
check the specific host's ToS, and if a user is in EU/UK/KR, using a *hosted* API is
often the cleaner route than self-hosting weights they aren't Territory-licensed for
— but confirm the host permits it. When a commercial deployment is on the line and
the facts are ambiguous, tell the user to get their own legal read; do not assert a
clearance you cannot source.

---

## How generation actually works (the two-stage pipeline)

`[fact]` (arXiv 2506.15442, Hunyuan3D-2.1) The pipeline is deliberately **modular** —
you can run either stage alone.

**Stage 1 — Shape (Hunyuan3D-DiT + ShapeVAE):**
- Input: a single image (background removed), or multi-view images (2mv), or text
  (which is routed through text-to-image first).
- A flow-based diffusion model over a vectset latent produces a signed-distance /
  occupancy field; **marching cubes** extracts a **watertight** triangle mesh.
- `octree_resolution` is the primary geometry-density / quality knob.
- Output: an untextured mesh (GLB/OBJ, trimesh object).

**Stage 2 — Texture / material (Hunyuan3D-Paint):**
- Input: the mesh from Stage 1 (Hunyuan3D's own, or **your own imported mesh**).
- A mesh-conditioned **multi-view diffusion** model renders the object from several
  viewpoints (training used 512×512 views) and generates view-consistent material
  maps, then bakes them into UV textures.
- `[fact]` 2.1 produces **PBR** maps under the Disney Principled BRDF: **albedo**
  (light-free, via an illumination-invariant training strategy), **metallic**, and
  **roughness**. It uses a 3D-aware RoPE for cross-view consistency. 2.0's Paint
  output was closer to baked diffuse color; 2.1 is the first open PBR.

`[heuristic]` Because Stage 2 accepts arbitrary meshes, a strong workflow is: use
Hunyuan3D only for texturing an existing (hand-modeled or retopologized) mesh, or
only for shape and texture elsewhere. Treat the two stages as independent tools.

### Input strategy: image beats text for control

`[heuristic]` Text-to-3D internally does text→image→3D, so you surrender control at
the image step. **Feed your own reference image** whenever geometry matters. Good
shape inputs:
- **single, clearly separated subject**, whole object in frame, not cropped;
- **plain / removable background** (the pipeline runs background removal; a busy
  background degrades it);
- **front-facing, roughly orthographic** framing, even lighting, minimal harsh
  shadow (shadows can be baked into geometry);
- for objects where the **back or sides matter**, use **2mv** with multiple views —
  a single front image forces the model to *hallucinate* the unseen faces, and it
  often gets concavities, back detail, and thin structures wrong.

---

## Self-hosting: hardware and setup (verified 2026-07-10)

`[fact]` VRAM footprints (from the model READMEs — note the two open lines report
slightly different numbers, so plan for the larger):

| Task | Hunyuan3D-2.0 line | Hunyuan3D-2.1 line |
|---|---|---|
| Shape only | ~6 GB (2mini ~5 GB) | ~10 GB |
| Texture only | — | ~21 GB |
| Shape + texture combined | ~12–16 GB | ~29 GB |

`[heuristic]` Practical reading: **a 24 GB card (RTX 3090/4090) runs 2.1 shape and
texture** if you offload between stages rather than holding both in memory at once;
running both simultaneously wants ~29 GB, i.e. a 32–48 GB card or sequential
execution with model offloading. **2mini** is the choice for 8 GB consumer cards
(shape only). The distilled **Turbo + FlashVDM** path is for fast iteration, not
maximum fidelity.

`[fact]` Reference environment for 2.1: Python 3.10, PyTorch 2.5.1 + CUDA 12.4.
Setup compiles a **custom rasterizer** and a **DifferentiableRenderer / mesh
painter** (C++/CUDA extensions) — budget time for the build step and a matching
CUDA toolchain. Real-ESRGAN weights are fetched separately for texture upscaling.
A Gradio app (`gradio_app.py`) and a REST endpoint (`/generate`, base64 image in →
GLB out) ship in the repo. Source: `Hunyuan3D-2.1` README.

### ComfyUI

`[fact]` (docs.comfy.org, verified 2026-07-10) ComfyUI has **native support for the
shape/geometry stage only** — workflows for `Hunyuan3D-2`, `2mv`, and `2mv-turbo`
generate untextured GLB into `ComfyUI/output/mesh`. **Texture/material generation is
not in the native nodes.** For PBR texturing inside ComfyUI, use a community wrapper
(e.g. ComfyUI-Hunyuan3DWrapper). Plan the texture stage separately if you are
ComfyUI-only.

---

## Hosted access routes (verified 2026-07-10)

- **Tencent Cloud "Hunyuan 3D APIs"** (doc `1284/75539`) — first-party; International
  Station live since Nov 26 2025. Backs the closed 2.5 / PolyGen / 3.x tiers.
- **Hugging Face Space** `tencent/Hunyuan3D-2.1` — a free demo of the open model,
  good for a quick capability check, not for production volume.
- **Third-party hosts** — fal.ai, Replicate, 3D AI Studio, Atlas Cloud, and others
  wrap Hunyuan3D behind their own APIs and billing.

`[fact]` Tier/pricing signals seen across hosts (indicative, varies by provider):
"Rapid" tiers finish in ~2–3 min with fixed mid-range polygon budgets and ~1K
textures; "Pro" tiers invoke the full model with configurable polygon counts
(~40K–1.5M) and up to 4K PBR. Per-model prices around **$0.02–$0.38** were observed;
one credit scheme charged Pro 60 credits (+20 PBR, +20 multi-view, cap 100) vs Rapid
35 (+20 PBR, cap 55). **Treat all prices as volatile — quote the host's live pricing,
never these numbers, to a user.**

---

## Mesh output characteristics and required post-processing

`[fact]` Open 2.x meshes come from **marching cubes over a diffusion field**. That
means they are **watertight** but also **dense, uniformly-triangulated, non-quad,
and lacking artist topology (no edge loops)**. UVs are auto-generated for texturing,
not laid out for hand-editing.

`[heuristic]` Consequences for a production pipeline — plan these passes:

- **Retopology.** Raw meshes are unsuitable for rigging/animation or clean
  deformation. Retopologize (manual, an auto-retopo tool, or route the asset through
  **PolyGen**, which was built for exactly this) before animating.
- **Decimation.** For real-time (game/AR/web) budgets, decimate the dense mesh to a
  target triangle/polygon count; expect to bake normal maps from the high-res mesh to
  preserve detail.
- **UV re-layout** if a human needs to paint or edit textures, rather than only
  consuming the auto-baked PBR set.
- **Scale / orientation / origin normalization** — generated assets rarely come in
  your engine's units, up-axis, or pivot convention.
- **PBR map validation** — confirm albedo, metallic, and roughness channels all
  exported and are separated correctly (some export paths flatten to diffuse).

---

## Reviewing generated assets — quality checklist

`[heuristic]` Before accepting an asset, check:

1. **Silhouette & proportions** from all sides (orbit it) — front-only inputs
   frequently produce a plausible front and a mangled back.
2. **Unseen-face invention** — concavities, undercuts, and thin features (straps,
   handles, hair) are the common failure zone; verify they exist and are solid.
3. **Floaters / disconnected shells / non-manifold artifacts** from marching cubes.
4. **Geometry density vs need** — is it far denser than the use case warrants
   (decimate) or too coarse (raise `octree_resolution` / use 2.5/3.0)?
5. **Topology** — acceptable for a static prop as-is; **not** acceptable for
   animation without retopology.
6. **PBR correctness** — albedo should be lighting-free (no baked highlights or cast
   shadows); metallic/roughness should read physically (metal vs dielectric).
7. **Texture seams and stretching** at UV boundaries; resolution adequacy (1K vs 4K
   depending on tier and camera proximity).
8. **Scale/orientation** normalized to target engine.

---

## Production decision: open self-host vs hosted commercial

`[heuristic]` **Self-hosting an open 2.x model wins when:**
- you generate **high volume** — marginal cost per asset approaches zero vs per-call
  API fees;
- **data cannot leave your environment** (unreleased IP, private client assets);
- you need **PBR at no per-asset cost** and full pipeline determinism/integration;
- you want the **training code** (2.1 ships it) to fine-tune on a domain;
- and — the gating condition — you are **inside the Territory** (not EU/UK/KR) and
  **under 1M MAU**, or have Tencent's commercial license.

`[heuristic]` **A hosted API wins when:**
- you need **peak fidelity or resolution** (2.5, 3.0) or **clean topology**
  (PolyGen) that the open weights don't provide;
- you have **no suitable GPU** or don't want to maintain the CUDA/build toolchain;
- volume is **low or spiky** (pay-per-use beats idle GPU);
- you are in **EU/UK/KR** and self-hosting the open weights is not Territory-licensed
  (use a host that permits your use — and still check its ToS).

`[first-party claim]` On Tencent's own benchmarks, Hunyuan3D-DiT (2.1) edges
comparable open models on shape metrics (Uni3D-T 0.2556 vs TripoSG 0.2506,
Step1X-3D 0.2554) and 2.1's Paint improves texture CLIP-FID to 24.78 from 2.0's
26.44. These are vendor-reported; treat "best" claims skeptically and, for a real
selection, run your **own** assets through candidates rather than trusting a
leaderboard.

---

## Complete example (labeled example, not a required formula)

**Intent:** A studio outside the EU/UK/KR needs ~500 stylized prop meshes for a
mobile game, textured, on an in-house pipeline, no per-asset cloud fee, budget for
one 24 GB GPU.

**Decision & reasoning:**
- **Track:** self-host — high volume + fixed GPU makes marginal cost ~0, and 500
  assets would be a recurring API bill.
- **License:** studio is in-Territory and well under 1M MAU → free commercial use;
  add the NOTICE file and "Powered by Tencent Hunyuan" mark. `[fact]`
- **Model:** **Hunyuan3D-2.1** — need PBR for the game's lighting, want the open
  weights + code. On a 24 GB card, run **shape then texture sequentially with
  offload** (combined would want ~29 GB). `[fact]`/`[heuristic]`
- **Input:** provide a **front reference image per prop** (concept art), background
  removed; for props with important back detail, capture two views and use **2mv**.
  `[heuristic]`
- **Iterate** with the **Turbo/FlashVDM** checkpoint to lock silhouette and framing
  cheaply, then re-run the **full** model for the final. `[heuristic]`
- **Post-process each asset:** decimate to the mobile poly budget; **bake normals**
  from the dense mesh; **retopologize** any prop that will deform/animate (or send
  those few through hosted **PolyGen**); validate the albedo/metallic/roughness set;
  normalize scale/up-axis to the engine. `[heuristic]`

**Expected result:** watertight, PBR-textured props at controlled poly counts, no
per-asset fee, license-clean.

**Likely failure modes:** hallucinated back faces on single-view props (mitigate with
2mv); dense triangle topology unusable for the few animated props (retopo/PolyGen);
albedo with baked shadows if lighting in the reference was harsh (use flat, even
reference lighting).

**Variation:** the same studio in **Germany** cannot use the open weights under the
Community License at all — it must switch to a **hosted API whose ToS permits the
use**, changing the economics and the whole plan. `[fact]`

---

## Common failure modes (summary)

- **Back/side geometry wrong** from single-view input → use 2mv or multiple views.
- **Topology unusable for animation** → retopologize or use PolyGen; the open meshes
  are marching-cubes triangle soup by design. `[fact]`
- **VRAM OOM** running shape+texture together → run stages sequentially with offload,
  or drop to 2mini for shape. `[heuristic]`
- **Baked shadows/highlights in "albedo"** → the input reference had directional
  lighting; re-shoot flat. `[heuristic]`
- **Assuming open = unrestricted** → it is the Community License: Territory-limited
  (no EU/UK/KR), 1M-MAU gate, prohibited-use clauses, attribution. `[fact]`
- **Assuming ComfyUI gives you textures** → native ComfyUI is geometry-only; texture
  needs a community wrapper. `[fact]`
- **Confusing tracks** → 2.5/PolyGen/3.x are API-only; you cannot download their
  weights. `[fact]`

---

## Primary sources (all verified 2026-07-10)

- GitHub `Tencent-Hunyuan/Hunyuan3D-2` — 2.0 model zoo, variants, FlashVDM, VRAM.
- GitHub `Tencent-Hunyuan/Hunyuan3D-2.1` — 2.1 weights + training code, setup, VRAM.
- LICENSE files in both repos — Tencent Hunyuan 3D 2.0 / 2.1 Community License
  (Territory, 1M MAU, prohibited uses, attribution).
- arXiv 2506.15442 — Hunyuan3D 2.1 technical report (two-stage architecture, PBR /
  Disney BRDF, benchmark numbers).
- arXiv 2506.16504 — Hunyuan3D 2.5 technical report.
- GitHub `Tencent-Hunyuan/HunyuanWorld-1.0` and `Tencent-Hunyuan/HY-World-2.0`;
  arXiv 2507.21809 — world/scene models.
- docs.comfy.org Hunyuan3D-2 tutorial — ComfyUI native geometry-only support.
- Tencent Cloud "Hunyuan 3D APIs" (doc 1284/75539) and Tencent press releases —
  hosted API, International Station launch (Nov 26 2025).
- hunyuan3d.cc version notes; Tencent Hunyuan announcements — PolyGen (Jul 8 2025),
  2.5, 3.0/3.1 timeline and closed-source status.
