# EVAL — topaz-video-enhancement

Answer key and scoring spec. Do not expose to the evaluated agent. The agent under
test receives only the user task and `SKILL.md`. Codes/prices are volatile
(verified 2026-07-10); accept a plausibly-updated code with a correct family/role and
penalize only wrong *family/role* choices, not a version-number drift, unless the
question is specifically about verification discipline.

---

## Part 1 — Knowledge questions

### K1. Name Topaz's video model families and the primary problem each solves.
**Expected:** Proteus (deterministic upscale + enhance, incl. Iris face recovery,
Artemis denoise+sharpen, Dione deinterlace, Gaia CGI/animation, Rhea 4× texture,
Theia sharpen); Starlight (diffusion restoration); Astra (creative diffusion upscale
adding new detail); Nyx (dedicated denoise); Frame interpolation (Apollo/Chronos/Aion
— frame-rate & slow-motion); Video utilities (Themis motion deblur, Colorization,
Hyperion SDR→HDR, Foreground removal).
**Required points:** distinguishes deterministic (Proteus) from diffusion
(Starlight/Astra); knows frame interpolation is separate from upscaling; names Dione
for interlacing and Nyx for denoise.
**Disqualifying:** claiming Topaz generates video from scratch; claiming frame
interpolation also upscales; treating "Proteus" as the only model.

### K2. Which model deinterlaces interlaced broadcast/camcorder footage, and why not just use Proteus?
**Expected:** Dione (TV variants e.g. `dtv-4`, DV variants e.g. `ddv-3`). Any model
can be told `video_type:"Interlaced"`, but Dione is purpose-built to reconstruct
progressive frames from fields; Starlight Mini also auto-deinterlaces small formats.
**Required points:** names Dione; understands `video_type`/`field_order` params exist;
notes Proteus can *accept* interlaced but Dione is the right tool.
**Disqualifying:** "just upscale it" with no deinterlace step; inventing a model name.

### K3. Describe the Video API job lifecycle and its cost/limit facts.
**Expected:** async multi-step: (1) POST `/video/` create (returns requestID, **free**),
(2) PATCH `/accept` → S3 upload URL(s), (3) PUT file to S3 (keep eTag), (4) PATCH
`/complete-upload` with `{partNum,eTag}` to start processing, (5) GET `/status` poll
until done → download. Auth `X-API-Key` header; HTTPS only; **500 MB** per-request
limit; 429 → exponential backoff; credits charged when the job processes (not at
create).
**Required points:** knows it is async/multi-step, not one call; create is free/
credits charged on processing; the 500 MB limit; API-key auth; polling for status.
**Disqualifying:** describing a single synchronous upload+result call; claiming create
costs credits.

### K4. Contrast Proteus, Starlight, and Astra on fidelity.
**Expected:** Proteus = deterministic, **preserves** source, reproducible, cheapest.
Starlight = diffusion, **restores** with intent preserved, recovers detail Proteus
can't, higher cost/risk. Astra = **creative** diffusion, deliberately **adds new**
detail/texture/stylization and can change objects/identity — only when transformation
is wanted.
**Required points:** orders them preserve → restore → transform; flags Astra's
identity-change risk; notes cost increases along that order.
**Disqualifying:** calling Astra a faithful upscaler; claiming Starlight/Astra are
free of hallucination risk.

### K5. Name the three artifact classes enhancement introduces and one mitigation each.
**Expected:** (a) over-smoothing/waxy faces → lighter settings, add grain back, face-
aware model; (b) temporal shimmer/flicker → temporally-aware model (Starlight/Nyx),
judge in motion; (c) face hallucination/identity drift → lower `creativity`, use
Proteus/Precise, check identity across whole clip. (Amplified warping and over-
interpolation also acceptable.)
**Required points:** at least two of the three with a correct mitigation; recognizes
these are motion/temporal problems, not just per-frame.
**Disqualifying:** claiming enhancement is artifact-free; "just increase sharpening"
as a cure-all.

---

## Part 2 — Production-decision questions

### D1. A 720p, temporally-stable AI-generated clip must ship at 1080p and must not invent new content. Budget matters. What do you choose and why?
**Expected decision:** Proteus (`prob-4`) deterministic upscale if artifacts are mild
(cheapest, preserves source); escalate to Starlight Precise 2.5 (`slp-2.5`) only if
Proteus can't hold detail. Explicitly reject Astra (adds new content) given the
no-invention constraint.
**Reasoning a strong answer shows:** matches "no new content" to preservation/
restoration models; sequences cheap-first, escalate-if-needed; prototypes on a short
clip before the full run.
**Penalize:** choosing Astra despite the constraint; jumping to the most expensive
model with no justification; ignoring cost.

### D2. Handheld action footage at 30 fps needs smooth 4× slow motion at 1080p (same resolution). How do you build it?
**Expected decision:** frame interpolation only — Apollo (`apo-8`) default, or Aion
(`aion-1`) for extreme slow-mo with heavy parallax/fast pans. Set `slowmo`/`fps` and
`duplicate`/`duplicateThreshold`; split on scene cuts. Do **not** expect or request
upscaling from the interpolation model — resolution stays 1080p.
**Reasoning:** knows interpolation ≠ upscaling; picks Aion vs Apollo by motion
character; handles duplicates/cuts to avoid morphing.
**Penalize:** expecting the interpolation model to upscale; ignoring duplicate/cut
handling; using Proteus to "add frames."

### D3. A batch of 1080i broadcast archival tapes, some heavily degraded, must become clean 1080p progressive. Design the pass.
**Expected decision:** Dione TV (`dtv-4`) with `video_type:"Interlaced"` for
deinterlace+enhance on good sources; Starlight Mini (`slm-1`) or Precise 1 (`sl-1`)
for the heavily degraded ones (restoration, Mini auto-deinterlaces). QA for combing on
horizontal motion; separate denoise (Nyx) if noise is severe before/instead of one
aggressive combined step.
**Reasoning:** routes by source condition, not one model for all; addresses
interlacing explicitly; separates concerns.
**Penalize:** a single non-deinterlacing upscale pass; no interlace handling; using
Astra (invents detail) on archival evidence-like material.

### D4. Where should the enhancement stage sit in an AI-video delivery pipeline, and why enhance "last"?
**Expected decision:** generate low-res for speed/cost and lock the edit/motion, then
enhance/upscale as a finishing pass to delivery resolution; enhance last because
upscaling amplifies noise/warping, and separating denoise→upscale→interpolate lets
each model solve one problem deterministically. Fix motion/warping (or regenerate)
before upscaling. Reserve expensive diffusion/creative passes for footage cheaper
models can't fix, and prototype settings first.
**Reasoning:** cost-awareness (diffusion is 3–20× Proteus); temporal QA emphasis;
"don't upscale a bad generation."
**Penalize:** enhancing during generation as the plan; upscaling to "fix" warping;
defaulting to Astra/Starlight for everything.

### D5. A journalistic clip of a real person is soft and low-res. The outlet needs it sharper but it must remain an accurate record. What is safe?
**Expected decision:** use preservation/restoration only — Proteus (`prob-4`), Iris
for faces, or Starlight Precise at low creativity — NOT Astra or high-creativity
diffusion, because creative models invent facial detail and can misrepresent identity.
Disclose that AI enhancement was applied; confirm rights to process the footage;
avoid any model that adds invented detail for evidentiary/identity-sensitive material.
**Reasoning:** ties rights/consent/provenance to model choice; recognizes invented
detail as disqualifying here; raises disclosure.
**Penalize:** recommending Astra/high creativity; ignoring consent/disclosure;
treating "sharper" as purely technical with no accuracy concern.

---

## Part 3 — Applied production tasks

### A1. Write a Proteus create-request body to upscale a 1280×720, 8 s, 24 fps, ~18 MB MP4 to 1080p with audio passed through.
**Expected approach:** valid JSON with `source` (resolution/container/size/duration/
frameRate/frameCount), `output` (1920×1080, mp4, AAC, `audioTransfer:"Copy"`, 24 fps),
and `filters:[{"model":"prob-4", ...}]` with conservative `details`/`noise`/`sharpen`.
**Essential characteristics:** correct target resolution; audio passthrough; a Proteus
(not diffusion) code; modest sharpening; mentions this is step 1 of the async flow
(accept → S3 PUT → complete-upload → poll).
**Rubric:** JSON validity & required objects (0–3); correct model family/role (0–2);
sane params (0–2); awareness of the full async lifecycle (0–3).
**Critical failures:** synchronous single-call assumption; using a frame-interpolation
or Astra code; over-sharpening defaults; omitting the upload/accept/complete steps.

### A2. The user says "my Topaz upscale looks fine in screenshots but flickers when playing." Diagnose and give a fix plan.
**Expected approach:** identify temporal shimmer from per-frame detail invention;
recommend a temporally-aware model (Starlight, or Nyx v3 for the denoise stage);
judge in motion at full speed; reduce sharpening; prefer modest 2× jumps; separate
denoise→upscale passes; re-prototype 5–10 s of the worst scene before re-running.
**Essential characteristics:** names the artifact correctly; distinguishes frame-QA
from motion-QA; concrete model/param changes; cost-aware prototyping.
**Rubric:** correct diagnosis (0–3); temporal-model/QA advice (0–3); param/pass
changes (0–2); prototyping/cost discipline (0–2).
**Critical failures:** "increase sharpening" to fix shimmer; judging only by a still;
no temporal model or multi-pass reasoning.

### A3. Choose models and outline stages to restore a noisy, low-light, compressed phone clip and deliver it at 4K without a plastic look.
**Expected approach:** stage 1 denoise with Nyx (`nyx-3`; XL only if severe), keeping
`details` low and re-adding a little grain (`grain≈0.03`, `grain_type` gaussian) to
avoid plastic; stage 2 upscale with Proteus (`prob-4`), preferring 2× steps toward 4K
rather than one 4× jump; QA faces and motion at full speed; escalate to Starlight only
if deterministic passes can't hold detail (note the ~3× cost of 4K and diffusion).
**Essential characteristics:** separates denoise and upscale; grain-back to avoid
waxiness; incremental upscaling; correct codes/roles; cost awareness.
**Rubric:** correct staging & separation (0–3); anti-plastic tactics (0–2); model/
param choices (0–2); QA + cost awareness (0–3).
**Critical failures:** one aggressive combined denoise+4× pass; no grain/anti-plastic
step; using Astra (invents detail) on real footage that must stay accurate; ignoring
that 4K/diffusion costs materially more.

### A4. The user wants Aion vs Apollo guidance for a fast-panning drone shot they want in extreme slow motion.
**Expected approach:** recommend Aion (`aion-1`) — built for extreme slow motion with
heavy parallax and fast camera movement, minimizing duplication/instability; Apollo
(`apo-8`) is the general default but can struggle with big parallax at extreme
stretch. Set `slowmo`/`fps`; handle `duplicate`; note interpolation does not upscale
(run a separate Proteus/Starlight pass if resolution must also increase).
**Rubric:** correct Aion-vs-Apollo reasoning tied to parallax/extreme slow-mo (0–3);
params (0–2); interpolation≠upscale reminder (0–2); QA for morphing/ghosting (0–2).
**Critical failures:** claiming the interpolation model upscales; picking by "quality
number" with no motion-character reasoning; ignoring duplicate/ghosting artifacts.

---

## Scoring guidance
- **Strong (pass):** correct model *family/role* routing by footage problem;
  understands the async multi-step API and its 500 MB / credit-on-processing facts;
  treats enhancement as repair with real artifact/cost trade-offs; QA in motion;
  raises rights/disclosure when the source is a real person or archival record.
- **Weak (fail):** treats "biggest/most expensive model" as universally best; assumes
  a single synchronous API call; ignores temporal artifacts or judges only stills;
  recommends creative/invented-detail models for accuracy-critical footage; no cost
  or consent awareness.
- Do not fail an answer solely for a drifted version suffix in a model code if the
  family and role are right — codes are volatile and the skill instructs verification
  against the live reference.
