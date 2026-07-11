# EVAL — moonvalley-marey

Answer key and scoring specification for the `moonvalley-marey` skill. The
evaluated agent receives the user task and `SKILL.md` only. The evaluator scores
the captured response against this file. Do not expose this file to the agent
under test.

Volatile facts are dated to 2026-07-10. If re-running after that date, confirm
current values before penalizing an answer that reflects a later change.

---

## Part 1 — Knowledge questions

### K1. What is Marey, and what is its core differentiator?

**Expected answer.** Marey (current production model: Marey Realism v1.5) is
Moonvalley's generative video model aimed at professional filmmakers, studios,
and brands. Its core differentiator is training-data **provenance** — Moonvalley
markets it as trained exclusively on owned/licensed footage, not scraped
content — plus a set of director-style controls. It is not positioned as the
highest raw-fidelity model.

**Required points:** licensed/owned training-data claim as the differentiator;
filmmaker/studio audience; director controls. **Bonus:** notes it is a
first-party claim.

**Disqualifying:** stating the licensed-data claim as independently verified
fact with no qualification; calling it a general-purpose "best" video model.

### K2. State the documented hard limits: resolution, frame rate, duration, audio.

**Expected answer.** Native 1080p (default 1920×1080); 24 fps; clips of 5s or
10s per generation on v1.5 (original launch was ~5s), with shot extension to
lengthen; **no audio** — Marey outputs silent video.

**Required points:** 1080p, 24fps, ~5–10s clips, no native audio. **Critical
failure:** claiming Marey generates audio/dialogue natively, or claiming native
4K.

### K3. Does "commercially safe" mean users are indemnified against IP claims?

**Expected answer.** No. "Commercially safe" is a first-party marketing claim
about training-data provenance (reduces input-side risk). The actual consumer
Terms of Service run the opposite way: the **user indemnifies Moonvalley**, and
Moonvalley's liability is **capped at the greater of $500 or amount paid**.
Reporting indicates Moonvalley indemnifies its **data-collection contractors**,
not end users — unlike Adobe Firefly, which offers enterprise output
indemnification. Any user/output indemnity would have to be negotiated in an
enterprise agreement.

**Required points:** user indemnifies Moonvalley (not vice versa); liability
cap; provenance ≠ output indemnity; enterprise agreement needed for any
guarantee. **Bonus:** the Adobe Firefly contrast; the ~$500 figure.

**Critical failure:** asserting Marey outputs are "legally cleared" or
"guaranteed safe" for the user on the strength of the marketing claim.

### K4. Name the filmmaker controls Marey exposes.

**Expected answer (any solid subset, named correctly).** Camera Control, Motion
Transfer, Pose Control / Pose Transfer, Trajectory Control, Keyframing,
Reference (per-character/object conditioning), Shot Extension, multi-layer
spatial composition (3D-aware). **Required:** at least motion transfer, pose
transfer/control, and camera control, with a correct one-line purpose each.

### K5. What are the access routes and the fal per-generation pricing?

**Expected answer.** Routes: Moonvalley web app / Voyager (first-party), the fal
API (`t2v`, `i2v`, `motion-transfer`, `pose-transfer`), ComfyUI, and some
third-party platforms (Adobe, Scenario). fal pricing: **$1.50 for 5s, $3.00 for
10s**. Moonvalley web credit packs: $14.99/100, $34.99/250, $149.99/1,000.

**Required points:** at least fal + Moonvalley web; the $1.50/$3.00 figures.
**Penalize:** invented pricing or endpoints stated with false confidence.

### K6. What prompt length and structure does Marey reward?

**Expected answer.** At least ~50 words, structured roughly as [camera movement]
+ [scale/perspective] + [core visual/action] + [environmental details, layered
FG/MG/BG] + [lighting/technical specs]. One clear core action, not several
simultaneous ones.

**Required points:** ≥50 words; layered/structured prompt; camera-first;
lighting/technical last. **Penalize:** advising terse one-line prompts.

---

## Part 2 — Production-decision questions

### D1. A brand agency wants AI B-roll for a national ad and says "we'll use Marey because it's commercially safe, so we can skip legal." Respond.

**Expected decision.** Endorse Marey as a *reasonable candidate* for
provenance-sensitive brand work, but **correct the "skip legal" conclusion**.
Explain: the licensed-training claim lowers one risk category (training-data
suits) but the standard ToS shifts indemnification onto the user and caps
liability at ~$500; there is no blanket user/output indemnity. Legal review
still required; any indemnity guarantee must be secured in a written enterprise
agreement. Also note the agency's own inputs (references, first frames,
brand/likeness) are their responsibility, not covered by the training claim.

**Strong answer demonstrates:** the marketing-vs-ToS distinction; that legal
review is still needed; enterprise-agreement path for real indemnity.

**Penalize / critical failure:** agreeing that legal can be skipped; presenting
"commercially safe" as a legal guarantee.

### D2. A director needs a 20-second, single-take, photoreal two-person dialogue scene with synced speech. Is Marey the right tool?

**Expected decision.** No. Marey has no native audio, produces 5–10s clips (not
a 20s single take), and photoreal talking-head dialogue is a documented weak
spot (stiff/plastic performance, temporal instability). Recommend an
audio-native model (Veo 3) for the dialogue coverage, and/or reserve Marey for
silent establishing/cutaway plates with audio built in post and the scene cut
from short shots.

**Strong answer demonstrates:** the no-audio limit; the short-clip limit; the
photoreal-dialogue weakness; a concrete alternative.

**Critical failure:** claiming one Marey generation can deliver this.

### D3. A studio wants a specific, repeatable camera orbit that prompted text-to-video keeps rendering with flicker. What do you change?

**Expected decision.** Stop trying to prompt the motion. Use **Camera Control**
(cinematic move from a single image) or **Motion Transfer** with a reference
clip that already contains the orbit, so a real reference drives the trajectory
instead of adjectives. Prefer i2v to lock composition; slow the move and/or
shorten the clip to reduce flicker.

**Strong answer demonstrates:** reference-driven motion over prompted motion;
naming the correct control; i2v/first-frame control; shorten/slow to reduce
jitter.

**Penalize:** just adding more descriptive words to the prompt.

### D4. Budgeting: a client asks for eight usable 5-second Marey shots on fal. Give a realistic cost range and why.

**Expected reasoning.** Base cost is $1.50 per 5s generation, but Marey's
inconsistency means multiple attempts per keeper — a reasonable planning
assumption is ~3–8 attempts per usable shot. So 8 shots ≈ 24–64 generations ≈
roughly $36–$96 in raw generation, plus post (upscale, color, audio) and labor.
The point: quote by *attempts*, not one-shot success.

**Strong answer demonstrates:** correct per-generation price; iteration
multiplier; that inconsistency drives real cost; post/labor exist beyond
generation. **Penalize:** quoting 8 × $1.50 = $12 as the expected cost with no
iteration buffer.

---

## Part 3 — Applied production tasks

### A1. Write a Marey prompt for the model's sweet spot.

**Task given to agent.** "Write a Marey (fal i2v) prompt and parameter set for a
5-second brand-safe hero shot of a wristwatch, going through legal review."

**Expected approach.** Use i2v from a supplied product still (to lock the dial/
logo). Prompt ≥50 words in the camera→scale→core→environment→lighting structure:
a slow controlled move, single subject near-static, controlled studio lighting,
lens/technical spec, shallow DoF. Params: `duration: 5`, fixed `seed`, default
1920×1080. Note review steps (label/logo stability across full 5s; confirm the
client cleared the supplied still).

**Successful output characteristics:** i2v chosen and justified; ≥50-word
structured prompt; single core action; lighting/lens specified; fixed seed for
iteration; correct duration; a legal/review note about the *input* asset.

**Scoring rubric (5 pts):** (1) i2v + rationale; (2) prompt length & structure;
(3) single controlled action suited to Marey; (4) correct params; (5)
review/legal note on inputs.

**Critical failures:** relying on the model to render legible logo text without
an input still; a terse prompt; multi-action overload; claiming the output is
automatically legally cleared.

### A2. Triage a bad generation.

**Task given to agent.** "My Marey clip looks great on the first frame but props
disappear and the character's hands warp by second three. Fix it."

**Expected approach.** Diagnose as Marey's known temporal-consistency and
hand-articulation weakness plus prompt overload. Fixes: simplify to one core
action; move to i2v to pin the scene; avoid tight hand close-ups or drive
gestures via pose transfer with a clean reference; shorten the clip; fix the seed
and change one variable at a time; add observed failure terms to the negative
prompt. Set expectation that some artifacts are inherent and the shot may need to
be reframed to hide hands/keep motion minimal.

**Scoring rubric (5 pts):** (1) correct diagnosis (temporal/hands, not a random
bug); (2) simplify action / i2v pinning; (3) pose transfer or reframe for hands;
(4) shorten + fixed-seed single-variable iteration; (5) negative-prompt tuning
and realistic expectation-setting.

**Critical failures:** attributing the artifacts to a fixable "setting" that
would make Marey photoreal-stable under complex motion; recommending simply
"regenerate with the same prompt."

### A3. Model-selection memo.

**Task given to agent.** "In three sentences, tell our post team when to reach
for Marey and when not."

**Expected content.** Reach for Marey when provenance/brand-safety and
directorial control matter and the shot is single-subject/controlled or
reference-driven (motion/pose transfer, previz). Avoid it when you need native
audio/synced dialogue, sustained complex/multi-character motion, photoreal
talking heads, or first-try prompt adherence at low cost — Veo 3 (audio) and
other peers win there. Add: whatever you choose, still run legal review; Marey's
marketing is not an indemnity.

**Scoring rubric (3 pts):** (1) correct "use" cases incl. provenance + control +
single-subject/reference; (2) correct "avoid" cases incl. audio + complex motion
+ dialogue, with a named alternative; (3) the legal-review caveat.

**Critical failure:** recommending Marey as a general default or as an
audio-capable / legally-guaranteed solution.

---

## Global critical failures (any response)

- Presenting the "trained on licensed data / commercially safe" claim as
  independently established fact or as a user output indemnity.
- Advising that legal review can be skipped because of Marey's marketing.
- Claiming native audio, native 4K, or long single-take clips.
- Inventing pricing, endpoints, or version numbers stated with false confidence.
- Recommending Marey for photoreal multi-character dialogue as a one-shot
  solution.
