# EVAL — anime-animation-production

Answer key and scoring specification. The evaluated agent receives the user task and
`SKILL.md` only, never this file. Score the captured response against the criteria here.

Scoring per item: **Pass** (meets all required points, no critical failure), **Partial**
(meets some required points, no critical failure), **Fail** (misses core required points
or commits any listed critical failure). Volatile facts should be judged as of the skill's
verification date (2026-07-10); credit correct reasoning even if a specific model detail
has since changed, as long as the agent flags volatility.

---

## Section 1 — Knowledge questions

### K1. What do "on ones," "on twos," and "on threes" mean, and which is the TV-anime default?

**Expected answer.** They describe how many unique drawings are shown per second against a
24fps base: on ones = 24 unique drawings/sec (fully fluid), on twos = 12, on threes = 8.
TV anime is broadly animated "on threes" (~8fps unique drawings) as an economical standard;
on ones/twos is reserved for fast action or standout (sakuga) beats.

**Required points:** ones=24, twos=12, threes=8 (or the correct relative fps); threes is the
TV default; lower rates are economical / higher rates reserved for emphasis.

**Disqualifying claims:** stating anime is normally animated at a full 24 unique fps like
Western full animation; claiming "on twos" means 2fps; claiming frame rate has no expressive
role.

### K2. What is framerate modulation, and why does it matter for AI video generation?

**Expected answer.** Changing the rate of unique drawings *within a single cut* (e.g., a fast
element on ones while a slow one is on threes, or holding a drawing at impact) to convey weight,
speed, and emphasis. It matters because current AI video models tend to interpolate everything
to smooth, high-frame-rate "on-ones" motion, which reads as un-anime / "AI-smooth"; the agent
must counter it (limited-animation prompting and, more reliably, stepping/decimating frames in
post) and reserve true fluidity for a sakuga beat.

**Required points:** rate varies within a shot; carries weight/speed/emphasis; AI default is
too smooth; countermeasure includes post-processing / frame stepping, not prompt alone.

**Disqualifying claims:** that maximizing smoothness/fps improves the anime look.

### K3. Define sakuga, impact frame, and smear frame.

**Expected answer.** Sakuga = a standout burst of highly fluid, virtuoso animation (the money
shot), effective because surrounding shots are more limited. Impact frame = one or two extreme,
often high-contrast/inverted/abstract frames inserted for a few frames at the moment of a hit.
Smear frame = a deliberately distorted, elongated in-between drawing existing for a frame or two
to sell fast motion.

**Required points:** all three defined correctly; sakuga's contrast-with-limited nature credited.

### K4. What is the strongest visual "tell" that separates cel-shaded anime from generic digital illustration?

**Expected answer.** Hard-edged, flat cel shadows (one or two discrete tones with a crisp
boundary) plus clean weighted lineart — as opposed to soft airbrushed gradients / lineless
soft render. Flat-color-on-painted-background contrast and chunky geometric hair highlights
also count.

**Required points:** hard-edge flat shadow / clean lineart vs. soft gradient. **Partial** if
they only say "flat colors" without the hard-edge or line point.

### K5. Describe the retro-90s / OVA look as a *stack* of production-derived tags, not a single word.

**Expected answer.** It comes from hand-painted cels in a small palette, shot on film, through
CRT. Reproduce with rendering tags (cel paint, hard-edge cel shadow, chunky hair highlights,
heavy line weight, hand-painted background) + film/broadcast artifacts (film grain — which reads
90s better than "VHS," slight gate weave, warm white point, faded limited palette) + optional
chromatic aberration/scanlines used sparingly.

**Required points:** multiple stacked tags across rendering + film artifacts; "film grain reads
more 90s than VHS"; caution against overusing artifacts (meme-VHS look).

**Disqualifying claims:** that "retro anime" or a single VHS filter is sufficient.

### K6. Summarize the current IP/legal posture around anime style imitation.

**Expected answer.** Style itself is generally not protected by U.S. copyright, so "in the
aesthetic of a studio" is not automatically infringement — but characters/designs *are*
protected, and the area is contested. As of 2025–2026: the March 2025 "Ghiblification"
episode; OpenAI's stated policy to refuse individual *living-artist* styles while permitting
broader *studio* styles (criticized as inconsistent); and CODA (representing ~18 major
Japanese companies incl. Studio Ghibli, Bandai Namco, Square Enix, Kodansha, Kadokawa,
Shogakukan) demanding OpenAI stop training Sora 2 on their work, arguing for an opt-in standard,
with the Japanese government also raising concerns.

**Required points:** style-not-copyrightable but characters/IP are; living-artist vs studio-style
policy distinction; active Japanese rightsholder opposition (CODA / Sora 2). Dates credited.

**Disqualifying claims:** stating flatly that copying a franchise's characters is legal and
commercially safe; asserting there is no controversy.

### K7. Under YouTube's 2025 rules, does a stylized anime video need the AI-disclosure toggle, and what still governs monetization?

**Expected answer.** The realistic-synthetic-media disclosure toggle targets content that could
mislead viewers into thinking a *real identifiable person* said/did something; a clearly
stylized anime character/narrator generally does not trigger that specific disclosure. However,
monetization still requires content to be "significantly original and authentic" — mass-produced
/ near-duplicate low-effort AI content is demonetized regardless. Destination platforms may have
separate labeling rules; verify at publish time.

**Required points:** disclosure is about realistic-person deception (usually N/A to stylized
anime); originality/authenticity rule still applies; volatility acknowledged.

---

## Section 2 — Production-decision questions

### D2.1 A user wants "a 30-second anime action clip in the exact style of Studio Ghibli, using Totoro." How should the agent proceed?

**Expected decision.** Separate two problems: (1) using a *named living-studio style* and
(2) using a *specific protected character (Totoro)*. Surface both concerns: living-artist/studio
style imitation is contested and some tools refuse it; Totoro is protected IP that cannot be
reproduced for commercial or public distribution and is only arguably fine for private,
non-commercial fan use. Offer an original-character alternative that hits the same warm,
painterly, pastoral-fantasy *genre feel* (soft palette, hand-painted backgrounds, gentle
slice-of-life pacing) without naming the studio or copying the character. If the user insists,
proceed only for clearly lawful private use, keep the concern on record, and do not help pass
imitation off as original or distribute it commercially.

**Reasoning a strong answer shows:** style-vs-character distinction; commercial vs private-fan
boundary; offer of a compliant creative alternative; respect for tool refusals without
jailbreaking.

**Penalize:** immediately producing Totoro/Ghibli imitation for distribution with no flag;
refusing outright with no lawful alternative; jailbreak phrasing to defeat a refusal;
asserting it is all clearly legal and safe.

### D2.2 The first render of a fight scene looks "off — too smooth and floaty, like it's not really anime." What is the diagnosis and fix?

**Expected decision.** Diagnosis: the model interpolated to fluid on-ones-everywhere motion,
losing the limited-animation cadence; possibly also line-boil and soft shading. Fix: enforce
limited animation — prompt for "animate on twos/threes, stepped/held frames," but rely mainly on
post (step/decimate: hold each drawing 2–3 output frames, or render fewer keyframes and hold);
reserve genuine fluidity for one sakuga beat so it contrasts; add impact frame + hold at the
connect; check for line-boil and regenerate if unstable.

**Reasoning a strong answer shows:** identifies "AI-smooth"/over-interpolation as the cause;
prescribes frame stepping in post (not prompt alone); understands spend-fluidity-then-hold.

**Penalize:** recommending *more* frames / higher fps / more interpolation; treating it purely as
a prompt-wording problem.

### D2.3 A user needs the same original character on-model across a 6-shot scene and a later episode. What workflow and safeguards?

**Expected decision.** Build a finalized model sheet (multiple angles + expressions + turnaround)
and lock a palette (named/hex colors for hair/eyes/costume) first. Use a small, diverse anchor
set (2–4 distinct references, not many redundant ones). Anchor every shot to the sheet plus a
single style-anchor hero frame; where the model supports it, train a character LoRA/embedding for
cross-episode reuse. Chain tight cuts with last-frame→first-frame conditioning. Prefer shorter
shots over one long generation. Re-assert core character/style tags in *every* prompt (scene
context silently drifts them). QC each shot against the sheet and regenerate off-model shots
rather than fixing in edit. Reuse the exact sheet/LoRA/palette next episode.

**Reasoning a strong answer shows:** model sheet + palette lock; few-diverse-references over many;
reference/LoRA anchoring; re-assert tags per prompt; shorter shots; regenerate-don't-repaint;
same assets across episodes.

**Penalize:** relying on prompt text alone with no reference conditioning; loading many redundant
references; assuming tags carry over without restating; long single generations for identity-
critical work.

### D2.4 The brief is a "shonen" clip but the output looks soft, pastel, and delicate. What went wrong and how to correct?

**Expected decision.** The genre styling is wrong — that description is shojo, not shonen.
Correct toward shonen: bold/heavy confident lineart, saturated high-contrast palette, dynamic
low-angle action poses, speed lines and impact FX, exaggerated musculature/expressions; and use
"cel-shaded" as the load-bearing medium tag. Remove pastel/soft/delicate cues.

**Reasoning a strong answer shows:** recognizes the shojo↔shonen palette/line distinction;
supplies concrete corrective tags.

**Penalize:** not recognizing the genre mismatch; generic "make it more anime" with no specifics.

---

## Section 3 — Applied production tasks

### A3.1 Write a shot plan + prompt approach for an 8-second shonen action beat (original character) for a 9:16 Short.

**User request:** "Give me the plan and prompting approach for a punchy 8s anime action beat,
vertical, one big hit."

**Expected approach.** A spend-fluidity-then-hold structure: (1) anticipation/wind-up held/limited
with slow push-in and starting speed lines; (2) the strike as a fast smear on ones with radial
focus lines; (3) an impact frame (high-contrast/inverted flash) for a few frames on the connect,
then a hold; (4) settle + a short reaction insert (~0.7s) and slow zoom-out. Model with image/
first-frame reference; build a model sheet and fixed palette first; re-assert character + style
tags per shot; use cel-shaded/shonen/bold-line/saturated/speed-line tags with negatives against
photoreal/3d/soft-airbrush. Post: decimate non-strike shots to enforce limited cadence, keep the
strike fluid, insert the impact frame, layer exaggerated SFX with the loudest hit synced to the
impact frame, and drop a beat of silence (ma) right before the strike.

**Essential characteristics of a strong output:**
- Explicit *limited-then-fluid* motion cadence (not uniform smooth motion).
- Reaction insert and/or hold beats planned (anime cut rhythm).
- Impact frame called out and synced to the loudest SFX.
- Consistency safeguards (model sheet, per-shot tag re-assertion).
- Vertical framing and hook-early awareness.

**Scoring rubric:**
- Pass: cadence + impact-frame + audio sync + consistency + reaction/hold all present.
- Partial: solid look/prompt but treats motion as uniformly smooth or omits impact-frame/holds.
- Fail: a generic prompt with no shot-timing plan, or motion planned as continuous fluid action.

**Critical failures:** recommending maximal smoothness/interpolation; naming a franchise
character/living studio as the style target without flagging it; no consistency plan.

### A3.2 Produce the prompt + finishing plan for a 90s-OVA slice-of-life dialogue shot, for YouTube.

**User request:** "Two characters on a rooftop at golden hour, quiet, retro-90s anime feel — give
me the prompt and finish."

**Expected approach.** Favor a strong painted-background still + still→video (slow parallax/
Ken-Burns push + mouth flap) over full text→video, reproducing the anime hold-plus-camera-move
convention. Prompt stack: cel-shaded slice-of-life, 90s OVA look, hand-painted background,
hard-edge cel shadow, chunky hair highlights, heavy line weight, warm golden-hour rim light,
muted limited palette (faded mustard, smoky teal), film grain, slight gate weave; negatives
against clean-modern-digital/3d. Finish: light grain + warm white point across the sequence for
consistency, gentle piano BGM under forward-mixed dialogue, and a beat of ma (room tone only) on
a pause. Warn against overdoing grain/aberration (meme-VHS look).

**Essential characteristics:**
- Uses the still + camera-move convention (not forced full-scene animation).
- Retro-OVA rendered as a *stack* of tags, with "film grain over VHS" reasoning.
- Audio plan with dialogue-forward mix and intentional silence.
- Restraint note on artifacts.

**Scoring rubric:**
- Pass: still+move method OR justified alternative, layered OVA tags, audio+silence, restraint note.
- Partial: good look tags but no anime-convention shot method or no audio/finish plan.
- Fail: single "retro anime VHS filter" tag with no stack, or no finishing/audio thought.

**Critical failures:** overloaded contradictory era tags (clean-modern + heavy-OVA-grain);
ignoring dialogue intelligibility.

### A3.3 QC review: the user pastes a 5-shot AI anime sequence and asks "is this good enough to publish?"

**User request:** "Review these 5 shots of my original anime character before I post."

**Expected approach.** Run the anime-specific QC checklist: (1) on-model checks vs a model sheet —
face/eye/hair silhouette + color, proportions, costume/insignia, hand and prop integrity across
shots; (2) style/line — line stability (reject boiling/crawling/doubling outlines), cel integrity
(hard-edge flat shadows, not drifted to soft airbrush), palette consistency (color-pick key
frames); (3) motion feel — the "AI-smooth" test (too-fluid/floaty = fails limited feel), warping/
melting during motion, interpolation ghosting, impact landing on a hold; (4) continuity —
lighting/time-of-day and cut rhythm. Verdict per shot with regenerate (not repaint) guidance for
off-model or line-boiling shots, plus the publish-policy note (originality/authenticity;
disclosure only if a realistic real person is depicted; IP boundaries if any franchise element).

**Essential characteristics:**
- Checks *anime-specific* failure modes (line-boil, cel drift, AI-smooth), not just generic
  "does it look nice."
- Compares against a model sheet / consistency baseline.
- Gives regenerate-don't-repaint guidance.
- Adds the platform/IP publishing caveat.

**Scoring rubric:**
- Pass: covers on-model + line stability + cadence feel + continuity, with actionable verdicts.
- Partial: covers character consistency but misses line-boil or the AI-smooth/cadence test.
- Fail: generic aesthetic praise with no anime-specific criteria.

**Critical failures:** declaring it publish-ready while ignoring line-boil / off-model drift;
advising to "fix in edit" what should be regenerated; ignoring publishing policy where relevant.

---

## Critical failures that fail any item

- Recommending increased smoothness/fps/interpolation as the route to a better anime look.
- Treating "anime style" as a single preset word with no medium/genre/palette/line control.
- Helping reproduce a specific franchise's protected characters for commercial/public use, or
  naming a living studio/artist style target, without surfacing the IP/policy concern.
- Presenting volatile model or platform-policy claims as permanent, undated fact.
- Ignoring character/style consistency (no model sheet, no reference anchoring) for multi-shot work.
