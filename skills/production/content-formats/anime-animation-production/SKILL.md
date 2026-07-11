---
name: anime-animation-production
description: >-
  Produce anime-style and stylized 2D animation with generative image and video
  tools as a craft discipline, not a filter. Use when a request asks for anime,
  manga-style, cel-shaded, sakuga, shonen/shojo/seinen/slice-of-life, mecha, or
  retro-90s-OVA animation; when planning shots, motion, and cutting rhythm to anime
  convention; when holding a character on-model and preventing style drift across
  shots or episodes; when choosing prompting vocabulary that actually controls anime
  look; when pairing voice, music, and impact SFX to stylized action; and when
  navigating the cultural, IP, and platform-policy sensitivities of AI anime
  (studio/artist style imitation, fan-art and IP boundaries, disclosure and
  monetization). This is provider-neutral; models are named only as illustrative
  options.
---

# Anime and stylized 2D animation production

Anime is not a preset. It is a set of production conventions born from hand-drawn
cel animation under tight schedules: flat color, hard-edged shading, deliberately
uneven frame timing, and a shot grammar that spends motion where it matters and
freezes everywhere else. Generative tools can reproduce the *surface* of that look
easily, and the *grammar* almost never by default. The value an agent adds is the
grammar — knowing which convention a given genre and beat calls for, encoding it into
prompts and shot plans, and reviewing output against the things that actually break
the illusion.

This skill covers the craft as production knowledge. It is provider-independent. Any
model named (Sora, Kling, Vidu, Wan, PixVerse, Midjourney, etc.) is an illustrative
option, dated where its behavior is volatile — never the method itself.

## Three labels used throughout

To keep evidence honest, claims here are tagged:

- **[Fact]** — documented in provider docs, animation references, standards, or news
  of record, with a source and (for volatile items) a verification date.
- **[Convention]** — a craft practice established in professional 2D/anime animation,
  independent of any tool.
- **[Heuristic]** — a production rule of thumb for generative tools, empirical and
  model-dependent; verify against your actual model and re-test when models change.

Volatile facts in this document were verified on **2026-07-10**. Model capabilities
and platform policies change fast; re-verify before relying on any dated claim.

---

## When to use / when not to use

Use this skill when the deliverable should *read as anime or stylized 2D animation* —
cel-shaded characters, limited-animation feel, anime shot grammar — regardless of the
underlying model.

Do **not** reach for this skill for photoreal or 3D-CG-realistic pieces, for Western
cartoon styles (Disney full animation, Cartoon Network flat-vector, cutout/Flash), or
for generic "illustrated" video that has no anime intent. Those are different craft
traditions with different timing and shading logic; applying anime conventions to them
produces an uncanny hybrid. If the user says "animated" without specifying anime,
confirm the tradition before committing to this grammar.

---

## Part 1 — The visual grammar of anime as production knowledge

### 1.1 The cel look: line and flat color

The defining surface of anime comes from the celluloid process: an ink outline drawn
on a clear cel, backed by flat painted color, over a separately painted background.
[Fact — the "cel" in cel-shading names the celluloid sheet used in traditional
production; painters laid flat color behind ink outlines. Sources: Wave Motion Cannon;
cel-shading references, 2026-07-10.] Its production-relevant properties:

- **Clean, weighted linework.** A continuous outline of controlled thickness, usually
  darker than a pure black (often a brown-black or color-holds on hair/skin). Line
  weight varies by era: heavier, chunkier lines in Akira-era/OVA work; thinner, more
  uniform lines in modern digital TV anime. [Convention]
- **Flat color fills with hard shadow boundaries.** No soft airbrush gradients on the
  character. Shading is one or two discrete tones with a *crisp* edge, not a blur.
  A second shadow tone ("2-shadow") appears in higher-budget or dramatic work. This
  hard-edge cel shadow is the single strongest tell of "anime" versus generic
  digital painting. [Convention]
- **Specular hair highlights.** Chunky, geometric highlight blocks on hair (not soft
  sheen). [Convention]
- **Painterly backgrounds against flat characters.** The character/background contrast
  is deliberate: characters are flat cel, backgrounds are lush painted (watercolor,
  gouache, or digital matte in the Kanmanagement/Kobayashi tradition). This flat-on-painted
  contrast reads as "anime" even in a still. [Convention]

**Production implication:** if your output shows soft, blurred, airbrushed shading on
faces, or lineless "soft render," it has drifted toward generic digital illustration
and away from cel. That is a QC failure (see Part 8), not a style choice, unless the
brief explicitly wants a painterly/"Makoto Shinkai" soft look.

### 1.2 Limited animation and framerate modulation

Anime evolved *limited* animation — fewer unique drawings per second than full Western
animation — as an economic necessity that became an expressive language. This is the
most important and most-ignored convention in AI anime.

Frame timing vocabulary [Fact — Anime News Network lexicon; Wave Motion Cannon,
2026-07-10]:

| Term | Unique drawings/sec (at 24fps base) | Feel |
|------|-------------------------------------|------|
| On ones | 24 | Fully fluid, expensive; sakuga, fast action |
| On twos | 12 | Standard "full" animation cadence |
| On threes | 8 | **TV-anime default**; economical, slightly stepped |
| On fours | 6 | Very sparse; slow/held or background motion |

- [Fact/Convention] TV anime is broadly animated "on threes" (~8 unique drawings/sec)
  as a production standard adopted after the 1960s; Osamu Tezuka's *Astro Boy* (1963)
  pioneered limited techniques under budget pressure.
- **Framerate modulation** = changing the rate *within a single cut*: a thrown weapon
  snaps on ones, a lumbering giant crawls on threes or fours, an impact holds a single
  drawing for several frames. Different rates carry different weight and speed; the
  brain fills the gaps. [Convention — popularized through the Otsuka/Kanada lineages.]
- **Element-wise rates.** In one shot a fast foreground effect can run on ones while a
  large slow object runs on twos, steering the eye. [Convention]

**Production implication for generative video:** most AI video models interpolate to
smooth, high-frame-rate, "on-ones-everywhere" motion — which reads as *too fluid*,
uncanny, "AI-smooth," and un-anime. Countermeasures [Heuristic, 2026-07-10]:

- Ask the model for "limited animation," "animate on twos/threes," "stepped animation,"
  "held frames," "8fps anime cadence," "TV anime motion." Effectiveness varies by model;
  many still smooth it out.
- More reliable: **post-process to reduce effective frame rate.** Render at the model's
  native rate, then step/decimate frames (hold every drawing 2–3 output frames) or
  render fewer keyframes and hold. This gives the stepped cadence that prompts alone
  usually cannot. [Heuristic]
- Reserve genuine on-ones fluidity for one or two **sakuga** moments; make everything
  else more limited so the fluid beat lands.

### 1.3 Sakuga, impact frames, smears, and the effects vocabulary

- **Sakuga** (作画, "drawing pictures"): in fan usage, a standout burst of highly fluid,
  detailed, virtuoso animation — the money shot. [Fact — term/definition per animation
  references, 2026-07-10.] Producing it means spending your fluidity budget on a short
  beat while keeping surrounding shots limited, so it contrasts.
- **Impact frame**: at the moment of a hit, one or two extreme frames — often a
  high-contrast, inverted, monochrome, or abstract "flash" drawing — inserted for
  1–3 frames to punch the collision. [Convention] In generation, produce as an inserted
  still or a hard cut, not as smooth motion.
- **Smear frames**: deliberately distorted, elongated in-between drawings that only
  exist for a frame or two to sell speed (a hand becomes a blur of multiple fingers).
  [Convention]
- **Speed lines / motion lines**: graphic straight or radial lines overlaid to indicate
  velocity or focus (radial "focus lines" for emphasis/reaction). Structural to the
  medium, not decoration. [Convention]
- **Effects animation (FX)**: fire, water, smoke, energy, and debris in the stylized
  "Kanada style" (angular, geometric flame/lightning shapes; "wakame"/seaweed-shaped
  shadows). [Convention — Kanada lineage.]
- **Bank shots / held cels**: reused animation (transformation sequences, stock attacks)
  and long holds on a single drawing with only a camera move or a mouth flap. [Convention]
  The mouth-flap-over-a-hold and the slow pan/zoom over a still are the workhorses of TV
  anime economy and are *easy* to reproduce with a still + a camera move.

### 1.4 Screen tone and halftone

From manga heritage: **screen tone** (halftone dot patterns and hatching for gray values
and texture) and halftone impact bursts. In color anime these appear as retro/manga-panel
stylings, flashback textures, and comedic cutaways. [Convention] Useful as a deliberate
stylistic tag ("halftone screentone shading, manga panel"), not a default.

---

## Part 2 — Genre and demographic styling

Anime "style" is really several styles keyed to demographic and genre. Getting this
right is the difference between generic-anime and on-target. Characteristics below are
[Convention] for the traditions and [Heuristic] for the prompt tags.

- **Shonen (action, young-male-skewed):** bold, dynamic poses; heavier confident
  linework; saturated high-contrast palette; kinetic FX (speed lines, energy, impact
  frames); exaggerated musculature and expressions. Tags: *cel-shaded, dynamic action
  pose, bold outlines, saturated colors, speed lines, impact frame.*
- **Shojo (romance/drama, young-female-skewed):** large expressive eyes with detailed
  catchlights; delicate, flowing linework; soft pastel palette; emotive environmental
  effects (floating petals, sparkles, screen-tone bloom, backgrounds that mirror mood).
  Tags: *soft pastel palette, delicate linework, large sparkling eyes, floral bokeh.*
- **Seinen (mature, adult-male-skewed):** more realistic proportions and anatomy; finer
  detailed linework and denser shading; muted/desaturated palette with selective accent
  color; psychologically complex, restrained expressions. Bridges anime and Western
  illustration. Tags: *realistic proportions, muted desaturated palette, detailed
  shading, subdued expression.*
- **Josei (mature, adult-female-skewed):** grounded, elegant character design; softer
  realism than seinen; naturalistic palette. Tags: *naturalistic palette, refined
  realistic features.*
- **Slice-of-life / iyashikei:** clean approachable character designs; detailed,
  realistic everyday backgrounds (Japanese suburbia, classrooms); muted naturalistic
  light; warmth over spectacle. Tags: *soft natural lighting, detailed realistic
  background, gentle muted palette, everyday setting.*
- **Mecha:** hard-surface mechanical detail, line-heavy panel lines, metallic cel
  highlights, often combined with dramatic FX. Tags: *mechanical detail, hard-surface
  shading, panel lines.*
- **Chibi / super-deformed (SD):** 2–3 head-height proportions, simplified features, for
  comedy inserts. Tags: *chibi, super deformed, simplified.*

### Retro-90s / OVA cel look

A distinct and popular target. The look comes from a real production chain: hand-painted
cels in a small fixed palette, shot on 16/35mm film, broadcast through CRT. [Fact — 90s
production-stack references, 2026-07-10.] Reproduce it with an explicit *stack* of tags
rather than a generic "retro" word [Heuristic, 2026-07-10]:

- Rendering: *cel paint, hard-edge cel shadow, chunky hair highlights, heavy line weight
  (Akira-era), hand-painted background.*
- Film/broadcast artifacts: *film grain* (this reads more "90s" than "VHS," which skews
  80s), *slight gate weave, warm white point, faded/limited palette (muted red, smoky
  teal, faded mustard).*
- Optional artifacts: *chromatic aberration, scanlines* — but sparingly; overuse creates
  the "meme VHS filter" look rather than authentic OVA.

Reference touchstones for the era's feel (as descriptors, not to imitate a specific
protected work): *Akira*, *Cowboy Bebop*, *Evangelion*, *Sailor Moon*-era palettes.

---

## Part 3 — Prompting vocabulary that controls anime style

[Heuristic, model-dependent, 2026-07-10.] Vague "anime style" produces a generic
soft-modern-digital look. Control comes from stacking four categories:

1. **Medium/technique tag** — the single most load-bearing word. Prefer **"cel-shaded"**
   (or "cel shading," "anime cel") over "anime style." Add "flat colors, hard-edge
   shadows, clean lineart."
2. **Genre/demographic tag** — from Part 2 (shonen/shojo/seinen/slice-of-life/retro-OVA).
3. **Palette and lighting** — explicit colors and light quality ("muted desaturated
   palette," "warm sunset rim light," "high-key soft daylight").
4. **Line and shading specifics** — "bold line weight," "thin uniform lineart," "two-tone
   cel shadow," "chunky specular hair highlights."

Additional levers:

- Negative direction (where supported): exclude "photorealistic, 3d render, blurry
  gradients, soft airbrush, lineless" to hold the cel look.
- Camera/lens language still applies ("wide establishing shot," "low-angle hero shot,"
  "shallow depth of field bokeh background") and composes with style tags.
- Do **not** over-stack contradictory tags (retro OVA grain + hyper-clean modern digital)
  — pick one coherent era.
- Provider-specific note: some models expose dedicated anime/illustration modes or
  anime-tuned checkpoints/LoRAs that respond better to *booru-style tag lists* (comma-
  separated attributes) than to prose; others (large general video/image models) respond
  better to natural-language scene descriptions. Match prompt shape to the model.
  [Heuristic, 2026-07-10.]

---

## Part 4 — Style consistency across shots and episodes

This is the hardest technical problem and where most AI anime fails. Two distinct
consistency targets:

- **Character consistency (on-model):** same face, hair, proportions, costume, and color
  scheme across every shot. [Fact — character/"identity" drift is documented across
  essentially all current major video models; subtle changes to face, hair, and
  proportions appear between shots and worsen over longer clips and scene changes.
  Sources: multiple 2025–2026 model comparisons, 2026-07-10.]
- **Style consistency (whole-look):** same line weight, shading logic, palette, grain,
  and rendering across shots and episodes, so nothing drifts between "flat cel" and
  "soft painterly" or between two different color temperaturas.

Note [Heuristic]: stylized anime characters tend to drift *less* than photoreal humans,
because exaggerated proportions and high-contrast features are easier for models to
reproduce — a genuine advantage of the medium. It is a smaller problem, not a solved one.

### Workflow that holds consistency

1. **Build a character model sheet first.** Generate (or assemble) a reference sheet:
   front / three-quarter / profile / back, a neutral and one expressive face, and a
   full-body turnaround, all in the *final* style. This is the anime-production
   "settei"/model-sheet concept adapted to generative work. [Convention + Heuristic]
2. **Curate a small, diverse anchor set.** For per-shot reference-conditioning, use a
   few *distinct* angles/expressions rather than many similar ones. [Heuristic — 2–4
   well-chosen references typically outperform 5–6 redundant ones; overlap gives the
   model no new information; 2026-07-10.]
3. **Anchor every generation to references.** Use whatever conditioning the model offers:
   image reference / character reference (some models accept multiple simultaneous
   references), first-frame image, or a trained character LoRA/embedding for repeated
   use. [Fact — as of 2026-07-10, reference-image and first/last-frame conditioning are
   available in several video models, e.g. Kling's reference and start/end-frame modes,
   Sora's image reference / storyboard keyframes, Vidu's multi-reference mode; treat
   exact feature names/limits as volatile and verify.]
4. **Lock a style anchor.** Keep one "hero" frame or style reference and condition
   toward it so the whole sequence doesn't drift between photoreal and illustration or
   between lighting regimes. [Heuristic]
5. **Chain shots.** Use the last good frame of shot N as the first-frame reference for
   shot N+1 where continuity is tight; for episodic consistency, keep the same model
   sheet, seed strategy, and LoRA across the whole batch.
6. **Validate every shot against the sheet** before accepting (Part 8). Reject and
   regenerate off-model shots rather than "fixing in the edit."

### Style drift traps [Heuristic, 2026-07-10]

- Adding scene context ("in the rain," "at night," "in a crowd") can silently soften
  edges, mute colors, or re-render fabric/hair — changing the character's signature.
  Re-assert the core style/character tags in every prompt; don't assume they carry over.
- Palette drift across a batch is common; specify exact hex-or-named colors for hair,
  eyes, and signature costume in every prompt, and QC color-pick key frames.
- Longer single clips drift more than short ones; prefer shorter shots stitched in the
  edit over one long generation when identity matters.

---

## Part 5 — Shot planning and motion direction adapted to anime

Anime editing rhythm is distinctive and generative shots should be planned to it, not
to a generic "smooth continuous" video model default.

### Cutting rhythm and shot types

- **The hold + camera-move shot.** A large fraction of TV anime is a *still* (or near-
  still) drawing with a slow pan, zoom, or rack, plus a mouth flap or hair sway. This is
  economical *and* the model reproduces it reliably: generate a strong still, then apply
  a slow Ken-Burns/parallax move. Use it for dialogue and establishing beats. [Convention
  + Heuristic]
- **Reaction inserts.** Anime cuts frequently to a brief static reaction (eyes widen,
  sweat drop, focus lines) — often 0.5–1s. Build these as short beats; they carry emotion
  and cover the fact that most shots are held. [Convention]
- **The 3-hit action beat.** Action often reads as: anticipation pose (hold) → fast
  in-between/smear (on ones) → impact frame + hold on the connect. Plan action as this
  spend-fluidity-then-hold cadence rather than uniform continuous motion. [Convention]
- **Establishing pillow shots (pan over background).** Slow drift across a painted
  background to set place/mood between scenes (the "pillow shot" / kire). [Convention]

### Motion direction levers for stylized action

- Request **stepped/limited motion** for most shots and **fluid on-ones** only for the
  sakuga beat, to create contrast (Part 1.2).
- Direct **weight and timing explicitly**: "heavy anticipation, then a single fast frame,
  then hold on impact" reads more anime than "character punches smoothly."
- Add **speed lines and impact flashes** as overlays or inserted frames rather than
  expecting the base render to include them convincingly.
- Keep the camera **anime-grammar**: whip pans, snap zooms to a face, dramatic low/Dutch
  angles for tension, and long slow pushes for emotion.

---

## Part 6 — Audio pairing conventions

Anime sound is stylized and expressive, and pairing it correctly does as much for the
"anime" read as the visuals. [Convention, with sourced anime-sound references, 2026-07-10.]

- **Voice (seiyuu tradition).** Performances are emotionally heightened and clearly
  delivered; dialogue sits forward in the mix and stays intelligible over music and FX.
  For AI/synth VO, direct expressive, character-distinct performances; keep dialogue
  the priority channel.
- **Exaggerated, layered SFX.** Impacts are larger than life — a punch layered with a
  synth kick/tom, an energy blast built from synth + whoosh. Footsteps, cloth, and small
  motions are often over-emphasized. Layer designed hits rather than using dry realistic
  thumps.
- **Impact stingers on the beat.** Sync the loudest hit to the impact frame; a musical
  or percussive stinger on the connect sells action.
- **Ma (間) — expressive silence.** Anime deliberately drops music and SFX to near-silence
  for emotional or tense beats (breath, room tone only). Don't wall-to-wall the music;
  plan silence as a tool.
- **Music as mood/pacing bed.** BGM supports rather than competes; it swells for climaxes
  and drops out for ma. Genre cues matter (city-pop/jazz for a Bebop feel, orchestral for
  epic shonen, gentle piano/acoustic for slice-of-life).

Mixing order of priority: dialogue intelligible first, then impact hits, then music bed,
with silence used intentionally.

---

## Part 7 — Cultural, legal, and platform sensitivities

This is a live, contested area. Handle it explicitly; do not treat AI anime as
consequence-free.

### Studio- and artist-style imitation

- [Fact, 2026-07-10] **Style is not, in itself, protected by U.S. copyright** — generating
  images "in the aesthetic of" a studio is not automatically infringement. But this is a
  legal *characterization of style*, not permission to copy characters, and it is disputed
  across jurisdictions.
- [Fact, 2026-07-10] The **"Ghiblification" episode (March 2025)**: OpenAI's image tools
  produced viral Studio-Ghibli-style images. OpenAI stated it **refuses the style of
  individual living artists but permits broader studio styles** (a policy critics note is
  in tension, since Ghibli's style is inseparable from living artist Hayao Miyazaki, who
  has publicly expressed strong opposition to AI animation). Sources: TechCrunch,
  Fast Company, 2025.
- [Fact, 2026-07-10] **Japanese rightsholders are actively opposing training on their
  work.** In late October 2025, **CODA** (Content Overseas Distribution Association),
  representing ~18+ major Japanese companies including **Studio Ghibli, Bandai Namco,
  Square Enix, Kodansha, Kadokawa, and Shogakukan**, publicly demanded OpenAI stop using
  their content to train **Sora 2**, arguing Japanese copyright law implies an **opt-in**
  standard and that reproduction during training can itself infringe. The Japanese
  government/Cabinet Office also formally raised concerns. Sources: Variety, TechCrunch,
  Game Developer, 2025.

**Practical guidance for an agent:**

- Prefer **original character and world designs** and a **generic genre style**
  ("cel-shaded shonen action," "90s-OVA look") over "in the style of [named living
  studio/artist]." Naming a living studio/artist as a style target is legally gray,
  ethically contested, and may be blocked or filtered by the tool.
- **Never reproduce or closely imitate protected characters or IP** (existing anime
  characters, logos, exact designs) for anything beyond clearly-permitted, private,
  non-commercial fan use — and even then flag the IP boundary to the user. Do not present
  fan-art of a franchise as ownable or commercially safe output.
- If a user explicitly requests a named living-studio/artist style or a specific
  franchise's characters, **surface the concern** (living-artist policies, active
  rightsholder objections, commercial risk) and offer an original-design alternative
  that hits the same genre feel. Follow the user's decision for lawful private use, but
  do not help pass off imitation as original or infringe for commercial distribution.
- Respect model/platform **refusals** for living-artist styles; route around them with
  genuine original direction, not with jailbreak phrasing.

### Platform policy and disclosure

- [Fact, 2026-07-10] **YouTube** (policy effective ~July 15, 2025): monetized content must
  be **"significantly original and authentic"**; mass-produced or repetitious near-
  duplicate AI content is demonetized under the "inauthentic content" rules. A separate
  **AI-disclosure toggle** is required for *realistic synthetic media that could mislead*
  viewers into thinking a real identifiable person said/did something — a clearly
  stylized anime narrator/character generally does **not** trigger the realistic-person
  disclosure, but originality/authenticity rules still apply. Sources: YouTube policy
  coverage, 2025.
- [Heuristic/practice] Add human authorship — story, editing, direction, commentary —
  and avoid template-farmed batches, both to satisfy monetization/originality rules and
  because it is what makes the work worth making.
- Other platforms (TikTok, Instagram, Meta) have their own AI-content labeling
  requirements; check the destination platform's current rules before publishing.
  [Volatile — verify at publish time.]

### Consent and likeness

- Do not generate a real, identifiable person as an anime character without their consent,
  and never for deceptive or defamatory use. Cameo/likeness features in some tools require
  the person's opt-in; respect it.

---

## Part 8 — QC review criteria specific to stylized animation

Review every shot against these before accepting. Generic video QC misses the failures
that specifically break *anime*.

**On-model / character checks (compare to the model sheet):**

- Face: eye shape/spacing, catchlight style, nose/mouth treatment consistent across shots.
- Hair: silhouette, parting, highlight shape, and *color* consistent; watch for hue drift.
- Proportions: head-to-body ratio stable; no morphing between shonen-tall and chibi.
- Costume: design, color, and insignia identical shot to shot; count fingers and
  accessories (hands and small props are common failure points).

**Style / line / shading checks:**

- **Line stability:** outlines should be clean and *stable*, not boiling/crawling
  (jittering line edges frame to frame), not breaking up or doubling. Line-boil is the
  #1 tell of AI-generated "animation" and a common rejection cause.
- **Cel integrity:** shadows stay hard-edged and flat; reject shots that drift into soft
  airbrushed gradients or lineless "soft render" unless intended.
- **Palette consistency:** color-pick key frames; hair/eye/costume colors match across
  the sequence and across episodes.

**Frame-rate / motion feel:**

- **"AI-smooth" test:** does motion feel too fluid/liquid/uncanny (everything on ones)?
  If so, it fails the limited-animation feel — step/decimate or re-plan (Part 1.2).
- Warping/melting during motion (faces or hands deforming mid-move), background objects
  drifting or popping, and interpolation ghosting are rejects.
- Impact beats land on a hold, not on a mushy smear-through.

**Continuity:**

- Lighting direction, time of day, and background consistent within a scene.
- Cut rhythm feels like anime (holds + reactions + spent-fluidity action), not like a
  continuous drifting AI clip.

Rule of thumb: if a shot is off-model or line-boiling, **regenerate**, don't paint over
it — the error usually recurs and compounds across the sequence.

---

## Part 9 — Delivery formats

Match encode and framing to destination.

- **Social vertical (TikTok/Reels/Shorts):** 9:16, 1080×1920, H.264/H.265, ~24–30fps
  container even if the *animation cadence* is limited (container fps ≠ animation rate),
  captions safe-area aware, hook in first ~2s. Keep the anime cadence but ensure the
  container frame rate is standard so playback isn't judder-flagged.
- **Streaming/YouTube horizontal:** 16:9, 1080p or 4K, 24fps (film cadence suits anime)
  or 23.976, H.264/H.265, stereo or 5.1 for premium. Add the required AI/originality
  handling from Part 7.
- **Music video:** cut to the track's beat grid; plan sakuga/impact beats to musical hits;
  deliver at the platform's spec (often 16:9 4K/1080p, 24–30fps). Lyric/typography overlays
  should respect the anime palette.
- **General note on cadence vs. container:** anime "on threes" is an *animation* choice; you
  still encode into a standard container frame rate (24/25/30). Decimate/hold at the
  animation layer, then encode normally, so players don't misread the file as low-fps.

---

## Complete worked examples

These are **examples**, not mandatory formulas. Adapt to the model, brief, and rights
posture. Prompt wording is [Heuristic] and model-dependent; the *structure and decisions*
are the transferable part.

### Example A — 8-second shonen action beat (original character), for Shorts

- **Intent:** A single punchy action beat: hero winds up and lands one hit, with a sakuga
  spike, for a 9:16 Short. Original character (no franchise IP).
- **Model class:** any image→video model with image-reference/first-frame conditioning.
- **Inputs/constraints:** model sheet built first (front / three-quarter / action pose,
  final cel-shaded style); fixed palette (hair #2b2b3a, eyes #d64545, jacket #e8e2d0).
- **Shot plan (spend-fluidity-then-hold):**
  1. 0.0–2.0s — anticipation: hero drops into a wind-up stance, slow push-in, near-held
     (limited, on threes feel), speed lines starting.
  2. 2.0–2.5s — the strike: fast smear in-between, on ones, radial focus lines.
  3. 2.5–3.0s — impact frame: 2–3 frames of a high-contrast inverted flash on the connect,
     then hold.
  4. 3.0–8.0s — settle + reaction insert: hold on the follow-through pose, small hair sway,
     cut to a 0.7s reaction (eyes narrow, dust settles), slow zoom out.
- **Prompt sketch (per shot, re-asserting identity every time):** "cel-shaded shonen anime,
  bold clean lineart, saturated high-contrast palette, [character from reference], dynamic
  low-angle action pose, speed lines, hard-edge cel shadows, dramatic rim light; [shot-
  specific action]; NOT photorealistic, NOT 3d, NOT soft airbrush."
- **Post:** decimate/hold the non-strike shots to enforce limited cadence; keep the strike
  fluid so it pops; add impact-frame insert; layer SFX (synth kick + whoosh + cloth) with
  the loudest hit synced to the impact frame; short silence (ma) right before the strike.
- **Expected result:** reads as a limited-animation shonen cut with one fluid money-frame.
- **Likely failures:** whole clip renders too smooth (fix: step frames); character face
  drifts between shots (fix: re-anchor to sheet, shorten shots); impact reads as mush
  (fix: insert real impact frame + hold); palette drift (fix: restate hex colors).
- **Variation:** slower seinen version — mute the palette, remove speed lines, hold longer,
  drop the flash for a grounded thud.

### Example B — Slice-of-life dialogue shot, 90s-OVA look, for YouTube

- **Intent:** Two characters on a rooftop at golden hour, quiet dialogue, retro-OVA texture.
- **Model class:** strong still image model + still→video (Ken-Burns/parallax) is often more
  controllable here than full text→video, and reproduces the anime "hold + camera move"
  convention directly.
- **Shot plan:** generate a strong painted-background still with cel characters (flat-on-
  painted contrast), then a slow parallax push and mouth flaps; cut to a 1s reaction insert.
- **Prompt sketch:** "cel-shaded slice-of-life anime, 90s OVA look, hand-painted background,
  hard-edge cel shadow, chunky hair highlights, heavy line weight, warm golden-hour rim
  light, muted limited palette (faded mustard, smoky teal), film grain, slight gate weave;
  two students on a rooftop; NOT clean modern digital, NOT 3d."
- **Post:** light film grain and a warm white point on the whole sequence for consistency;
  gentle piano BGM under dialogue, dialogue forward in the mix, a beat of ma (room tone
  only) on a pause.
- **Expected result:** authentic OVA warmth without the "meme VHS filter" look.
- **Likely failures:** grain/aberration overdone (dial back); background too flat/CG (push
  "hand-painted, painterly background"); characters too modern-clean (add "heavy line
  weight, cel paint").
- **Variation:** modern-TV slice-of-life — drop grain/gate-weave, thin the lineart, brighten
  to a clean daylight palette.

### Example C — Episodic consistency across a 5-shot scene

- **Intent:** Keep one original character on-model and on-style across five shots of a scene,
  and across a later episode.
- **Approach:** (1) finalize the model sheet and palette; (2) if the model supports it, train
  a character LoRA/embedding on the sheet for reuse across episodes, else keep the sheet as
  a persistent multi-image reference; (3) generate shots, each anchored to the sheet AND a
  single style-anchor hero frame; (4) chain continuity by feeding shot N's last good frame as
  shot N+1's first-frame reference where cuts are tight; (5) QC every shot against the sheet
  (Part 8) and regenerate off-model shots; (6) reuse the exact sheet/LoRA/palette in the next
  episode so the style doesn't drift between episodes.
- **Likely failures:** drift accumulates over long single generations (use shorter shots);
  adding scene context silently alters the character (re-assert core tags every prompt);
  cross-episode palette drift (lock exact colors and reuse the same reference assets).

---

## Sources (verified 2026-07-10 unless noted)

Craft and animation references:
- Wave Motion Cannon, "An Introduction to Framerate Modulation" —
  https://wavemotioncannon.com/2016/12/31/an-introduction-to-framerate-modulation/
- Anime News Network encyclopedia lexicon, "Shot on threes (ones, twos, etc.)" —
  https://www.animenewsnetwork.com/encyclopedia/lexicon.php?id=61
- Ani-Gamers, "The 12 Principles of Anime" — https://anigamers.com/posts/12-principles-of-anime/
- Animation Obsessive, "Frame-Rate Modulation Is a Subtle Art with Visceral Power" —
  https://animationobsessive.substack.com/p/a-subtle-art-with-visceral-power
- Animétudes, "The Kanada style in context" / "The Kanada style now" —
  https://animetudes.com/2021/03/06/the-kanada-style-in-context/
- 344 Audio / 344 SFX, anime sound design articles —
  https://www.344audio.com/post/article-secrets-of-anime-sound-design ;
  https://www.344sfx.com/blog-posts/inside-anime-sound-design-techniques-tricks-and-subtle-brilliance
- Crunchyroll, "How Anime Voice Over and Music Get Made" —
  https://www.crunchyroll.com/news/deep-dives/2023/3/23/feature-how-anime-voice-over-and-music-get-made

IP, policy, and platform (dated, volatile):
- TechCrunch (2025-03-26), "OpenAI's viral Studio Ghibli moment highlights AI copyright concerns" —
  https://techcrunch.com/2025/03/26/openais-viral-studio-ghibli-moment-highlights-ai-copyright-concerns/
- Fast Company (2025), "OpenAI's Studio Ghibli-style images renew the debate over AI and copyright" —
  https://www.fastcompany.com/91308222/
- Variety (2025-11), CODA letter to OpenAI re: Sora 2 —
  https://variety.com/2025/digital/news/studio-ghibli-openai-sora2-japanese-trade-group-coda-letter-1236568751/
- TechCrunch (2025-11-03), "Studio Ghibli and other Japanese publishers want OpenAI to stop training on their work" —
  https://techcrunch.com/2025/11/03/
- Game Developer (2025), "Japanese studios warn OpenAI over copyright concerns" —
  https://www.gamedeveloper.com/business/japanese-game-studios-demand-openai-stop-pilfering-their-work
- YouTube AI monetization/disclosure policy coverage (2025) — e.g.
  https://onewrk.com/youtubes-ai-disclosure-requirements-the-complete-2025-guide/

Generative-tool capability and consistency (dated, volatile — verify against the model in use):
- Model consistency/drift analyses (2025–2026): Magic Hour "How to Keep Characters Consistent in AI Video (2026)"
  https://magichour.ai/blog/how-to-keep-characters-consistent-in-ai-video ; longstories.ai
  https://longstories.ai/blog/maintaining-style-consistency-ai-animation
- Reference/keyframe features: Kling reference & start/end-frame docs (fal.ai/RunComfy),
  Sora 2 storyboard/keyframe & image-reference (OpenAI cookbook/API), Vidu multi-reference —
  https://cookbook.openai.com/examples/sora/sora2_prompting_guide ;
  https://www.runcomfy.com/models/kling/kling-video-o1/image-to-video/reference
- Anime style/prompt tag references (2026): 90s/retro-OVA and genre-tag guides —
  https://nanoimagine.art/blog/best-80s/90s-retro-anime-prompts ;
  https://autoweeb.com/blog/how-to-choose-the-best-anime-art-style-for-ai-anime-generations
