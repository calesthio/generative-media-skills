# EVAL — world-labs-marble

Answer key and scoring specification for the `world-labs-marble` skill. The
evaluated agent receives the user task and `SKILL.md` only — never this file.
Score the captured response against the criteria below. Facts are dated to
2026-07-10; if the model line, pricing, or access routes have since changed,
re-verify before penalizing a "wrong" answer that reflects newer reality.

Passing bar: substantially correct on all Knowledge items, defensible decisions
on the Decision items, and no Critical Failure anywhere.

---

## Part 1 — Knowledge questions

### K1. What kind of output does Marble produce, and how does that differ from a streaming/real-time world model?
- **Expected:** Marble produces a **persistent, downloadable 3D environment**
  (Gaussian splats and/or meshes) that you own as a file — not frames
  hallucinated on the fly as you move. It is a bounded, **static** 3D asset.
- **Required points:** persistent/downloadable; real 3D geometry (splats/mesh);
  static/bounded, not infinite streaming.
- **Disqualifying:** claiming Marble streams an infinite real-time world, or that
  it only outputs a video/image.

### K2. List Marble's input modes and the key constraint on each.
- **Expected:** Text; single image (auto-detects equirectangular pano);
  multi-image (**up to 4**, up to **8 in API reconstruction mode**, direction/
  azimuth tagged); video (MP4/WebM/MOV/AVI, **max 100 MB**); 360 panorama
  (equirectangular, most spatial control).
- **Required points:** at least four of the five modes named; the 100 MB video
  cap **or** the multi-image count; panorama = most control.
- **Disqualifying:** inventing unsupported modes (audio, live camera) as fact.

### K3. Name the current Marble models and when to use each.
- **Expected:** `marble-1.1` (recommended default, fixed cost); `marble-1.1-plus`
  (auto-expanding larger worlds, variable cost); `marble-1.0` (legacy);
  `marble-1.0-draft` (fast/cheap scouting, lower fidelity).
- **Required points:** 1.1 as default; 1.1 Plus = bigger/variable-cost; draft =
  cheap iteration.
- **Disqualifying:** presenting 1.0 as the current default, or claiming draft is
  full fidelity.

### K4. What is Chisel and what problem does it solve?
- **Expected:** A coarse-3D blocking tool that **decouples structure from
  style** — box/plane/wall/extrude primitives plus **GLB/FBX import**, with a
  positioned panorama camera; the prompt styles the blocked geometry. Solves the
  "right style, wrong floor plan" problem where layout must be controlled.
- **Required points:** structure vs. style separation; used when layout/
  proportions/door placement matter.
- **Disqualifying:** describing Chisel as a text-prompt or image tool with no
  3D blocking.

### K5. Which export format for visual fidelity vs. physics/collision, and the tier/format facts?
- **Expected:** **Gaussian splats (SPZ native / PLY portable)** for highest
  visual fidelity; **collider mesh (GLB, ~100–200k tris)** for physics only
  (Standard+); **high-quality mesh (GLB, ~600k textured / ~1M vertex-colored,
  up to ~1 hr, Pro)** for editable visual geometry. SPZ = Marble-native/compact,
  PLY = broad compatibility.
- **Required points:** splat = fidelity, mesh = interaction; collider vs.
  high-quality distinction; SPZ vs PLY.
- **Disqualifying:** claiming collider mesh is for display, or that meshes beat
  splats on visual quality.

### K6. App credits vs. API credits — and API credit economics.
- **Expected:** **Separate wallets** — app credits can't be used on the API and
  vice versa. API: **$1/1,250 credits**, **$5 minimum**, credits **don't
  expire**; a full 1.1 world ≈ 1,500 credits ≈ ~$1.20, draft ≈ ~$0.12–0.20.
- **Required points:** the wallets are separate; API is prepaid credits, app is
  subscription.
- **Disqualifying:** stating a single shared balance covers both.

### K7. Rights: who owns a world, and what gates commercial use?
- **Expected:** **Free-tier output** — World Labs retains rights; user gets a
  **personal, non-commercial** license only. **Paid-tier output** — user owns it
  and may use it **commercially** (excluding World Labs' own IP), per TOS. In
  Marble's product tiering, commercial rights attach to **Pro/Max**; treat
  **Standard as effectively non-commercial** and verify the live TOS. User is
  responsible for input rights (no unlicensed images/likenesses).
- **Required points:** Free = non-commercial; commercial delivery needs Pro/Max
  (or paid API); input-rights responsibility.
- **Disqualifying:** claiming Free-tier worlds can be used commercially, or that
  all paid tiers are unambiguously commercial without caveat.

### K8. State three expected artifact/limitation classes.
- **Expected (any three):** thin structures; transparent/reflective surfaces;
  occluded/unseen regions (backs, undersides); warped ground plane; finite world
  size; static geometry (dynamism only in video export); mobile support limited;
  HQ mesh slow (~1 hr) and rate-limited.
- **Disqualifying:** asserting Marble reconstructs unseen areas accurately, or
  that exported geometry contains animation/dynamics.

---

## Part 2 — Production-decision questions

### D1. Client wants an explorable web VR scene of a fictional temple, delivered commercially.
- **Expected decision:** Panorama (or multi-image) input for surround control →
  scout on draft → finalize on `marble-1.1` → Expand if larger → export **SPZ**,
  render on web with **Spark** → deliver on a **Pro/Max** plan for commercial
  rights.
- **Reasoning a strong answer shows:** panorama gives VR-grade surround
  coherence; splats give best fidelity and web-renderable via Spark; **commercial
  = Pro/Max**, not Free/Standard.
- **Penalize:** recommending Free/Standard for a commercial deliverable
  (rights error); mesh-only when splats would look far better; ignoring VR head-
  movement coherence.

### D2. Team must generate ~50 varied environments overnight, unattended, on a fixed budget.
- **Expected decision:** **World API** with `marble-1.1` (fixed cost),
  async generate → poll `/operations/{id}` → export; **scout prompts on draft**
  first; enable **auto-refill**; budget ~1,500 credits (~$1.20) each.
- **Reasoning:** API is the only automated route; fixed-cost model makes budget
  predictable; draft scouting avoids burning full-cost credits on bad prompts.
- **Penalize:** proposing the web app for a 50-item unattended batch; choosing
  1.1 Plus (variable cost) without budget justification; forgetting async polling.

### D3. Text prompts give the right look but the wrong room layout; a door must be in a specific place.
- **Expected decision:** Use **Chisel** — block the walls/door in 3D, position
  the panorama camera, then prompt for style; export **collider mesh + splat** if
  headed to an engine.
- **Reasoning:** layout is the constraint; Chisel decouples structure from style,
  which text alone can't pin.
- **Penalize:** re-rolling text prompts hoping for the right plan; suggesting a
  DCC fix before trying Chisel.

### D4. Output must drop into Unity with collision and good-looking visuals.
- **Expected decision:** Export **PLY splat** (visual, via Unity splat plugin)
  **plus collider mesh GLB** (physics); verify the engine has a working splat
  renderer, else fall back to **high-quality mesh**. Mind the OpenCV→OpenGL
  coordinate flip.
- **Reasoning:** splat = looks, collider = physics; splat rendering depends on a
  third-party plugin; coordinate systems differ.
- **Penalize:** assuming Unity renders splats natively; exporting only a collider
  mesh and expecting good visuals; ignoring the coordinate-system caveat.

### D5. User on the Free plan asks to ship a generated world in a paid indie game.
- **Expected decision:** **Do not ship on Free** — Free output is personal/
  non-commercial. Advise upgrading to **Pro/Max** (or a paid API entitlement) for
  commercial rights, and confirm the live TOS grant for that tier; also confirm
  the user has rights to any input images used.
- **Penalize (Critical):** greenlighting commercial shipment of Free-tier output.

---

## Part 3 — Applied production tasks

### T1. Write a first-generation plan for: "a photo of my empty studio, turned into an explorable 3D set."
- **Expected approach:** Single-image (or better, capture a **360 panorama** or
  multiple angles for coverage) → draft scout → `marble-1.1` → review occluded/
  back regions and ground plane → Expand weak areas → export per target (splat
  for web/VR, mesh for engine collision). Recommend a plan matching intended use.
- **Success characteristics:** names input mode with justification, includes a
  draft→final step, includes a review/QA step, ties export format to the target,
  and raises rights if the studio/set will be used commercially.
- **Rubric (5 pts):** input choice + rationale (1); model/draft strategy (1);
  QA/review step (1); correct export mapping (1); rights/plan advice (1).
- **Critical failures:** no review step; recommending a format that doesn't fit
  the target; ignoring that single-image backs will be invented/weak.

### T2. Diagnose: "my exported world looks torn and floaty where I clicked Expand, and railings are broken."
- **Expected approach:** Recognize **expansion seams** and **thin-structure
  artifacts** as known failure modes; advise orbiting to confirm whether artifacts
  are on the intended camera path; fix by **re-Expand/edit** or **re-generate with
  a stronger input** (panorama/multi-image) rather than DCC patching; consider
  **splats over mesh** for thin railings. Check coordinate/scale if geometry looks
  wrong on import.
- **Success characteristics:** correctly attributes the artifacts, distinguishes
  on-camera vs off-camera severity, proposes an in-Marble fix before DCC surgery.
- **Rubric (4 pts):** identifies expansion seam + thin-structure causes (1);
  on/off-camera triage (1); in-Marble repair path (1); format/coordinate check
  (1).
- **Critical failures:** claiming these are avoidable entirely; jumping straight
  to manual mesh cleanup without trying Expand/edit/regenerate.

### T3. Produce an illustrative World API request for a private "cyberpunk alley at night" world, and describe how to retrieve the result.
- **Expected approach:** `POST api.worldlabs.ai/marble/v1/worlds:generate` with
  header **`WLT-Api-Key`**; body with `world_prompt` (type `text`), `model`
  (`marble-1.1`), optional `seed`, `permission: { public: false }`; then **poll
  `/operations/{operation_id}`** until `done` and call the **export** endpoint;
  note `cost` reported on success and 402 on empty balance.
- **Success characteristics:** correct endpoint/auth header, valid prompt
  structure, **async poll** step, private permission, export step.
- **Rubric (5 pts):** endpoint + auth header (1); valid prompt/model body (1);
  private permission (1); async polling (1); export retrieval (1).
- **Critical failures:** treating generation as synchronous (no polling);
  inventing an auth scheme (e.g., bearer token) as fact; using app credits for the
  API.

### T4. Recommend a plan/route for a hobbyist making non-commercial VR scenes a few times a month.
- **Expected approach:** **Free** (~4/mo) if volume is tiny and truly non-
  commercial and single-image/pano input suffices; step up to **Standard** (~$20,
  ~12/mo) if they need multi-image/video/Chisel or more volume — while noting
  Standard is still effectively non-commercial. No commercial claim on either.
- **Success characteristics:** matches volume + input needs to tier; correctly
  keeps non-commercial framing; does not oversell Pro/Max for a hobbyist.
- **Rubric (3 pts):** volume/feature-to-tier match (1); correct commercial
  framing (1); avoids unnecessary upsell (1).
- **Critical failures:** telling the hobbyist Free grants commercial rights;
  recommending the API when a subscription clearly fits.

---

## Cross-cutting critical failures (any one = fail)

- Says commercial delivery is fine on the **Free** tier.
- Claims Marble outputs **animated/dynamic 3D geometry** or an **infinite real-
  time** world.
- Treats app and API credits as a **shared** balance.
- Presents unverifiable prices/model names as certain **without dating** them,
  when SKILL.md flags them volatile.
- Recommends the wrong **export format for the target** (e.g., collider mesh for
  visuals, splat where the engine can't render it) with no fallback.
- Fabricates an API auth scheme, endpoint, or synchronous behavior.
