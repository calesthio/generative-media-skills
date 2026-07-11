---
name: lighting-direction
description: Provider-independent lighting direction for AI-generated images, video clips, ads, film scenes, avatars, product shots, interviews, beauty work, and social content. Use when an agent must specify, translate, maintain, troubleshoot, or QA motivated lighting, key/fill/back/rim/practical lights, hard or soft light, color temperature, exposure, contrast, time-of-day, continuity, reference strategy, or safety/accessibility risks in generated media.
---

# Lighting direction for generated media

Use lighting as story structure, not decoration. State what the audience should understand from the light, then specify the visible lighting behavior that an image or video model can render: source motivation, direction, quality, color, contrast, exposure, falloff, catchlights, separation, practicals, and continuity.

This skill is provider-independent. Translate the guidance into the syntax of the chosen image, video, avatar, or composition tool after reading that tool's own instructions.

## Evidence labels

Use these labels in plans, prompts, and reviews when claims matter:

- **Documented fact**: supported by a cited lighting, cinematography, color, accessibility, or manufacturer source.
- **Empirical observation**: based on direct inspection of generated outputs or references in the current project.
- **Production heuristic**: a repeatable craft rule that often works but should be tested against the brief and model behavior.

Do not present a heuristic as a universal law. ARRI's lighting handbook explicitly frames hard-versus-soft choices as judgment calls rather than right/wrong rules, while documenting that physical source size and diffusion strongly affect shadow softness.

## First decision: what should the light do?

Before writing a prompt, answer five questions:

1. **Narrative motivation**: What real or implied source explains the light: window, sun, skylight, street sign, laptop, vanity mirror, car headlights, softbox, studio cyc, product light tent, neon practical?
2. **Emotional contrast**: Should shadows feel open, friendly, premium, clinical, suspenseful, nocturnal, nostalgic, harsh, sweaty, or sculptural?
3. **Subject hierarchy**: What must be brightest, sharpest, or separated from the background? What can fall into shadow?
4. **Surface behavior**: Are the important surfaces skin, hair, glass, chrome, matte packaging, fabric, liquid, screen UI, jewelry, food, or architecture?
5. **Continuity requirement**: Is this a one-off still, a multi-shot scene, a talking avatar, or a product/ad sequence that must preserve the same lighting geometry?

If any answer is unknown, make a conservative assumption and label it.

## Core vocabulary that models can render

### Motivated and practical light

**Documented fact**: Motivated lighting reads as coming from a realistic source inside the scene; practical lights are visible in-frame sources such as lamps, candles, or monitors. Rosco's film-lighting vocabulary gives examples of hidden daylight-balanced fixtures reading as window sun and warm fixtures reading as lamp light.

Direction for agents:

- Name the visible or implied source: "late afternoon window camera-left," "warm bedside lamp in frame," "overhead fluorescent office panels," "cool laptop glow under face."
- Make every non-obvious source plausible. If the face is lit by a lamp on the right, do not ask for a left-side shadow unless there is a second source.
- Use practicals as exposure anchors, not only props: "lamp shade glows but does not clip; warm practical motivates a soft key on the actor's near cheek."
- For fantasy, sci-fi, and surreal content, still give a physical logic: "blue reactor core below frame motivates underlight; amber warning strips create rim accents."

### Key, fill, back/rim, background, and accents

**Documented fact**: ARRI defines the key as the primary subject light; fill as light used to lift shadows created by the key; separation/hair light as a way to visually separate subject from background; and background light as a way to add texture, color, or separation. ASC cinematographer Stephen H. Burum describes the key as setting exposure and creating shadow, texture, roundness, and three-dimensionality.

Use role names only when they clarify visible behavior:

- **Key**: main modeling source; specify side, height, softness, and color.
- **Fill**: shadow control; specify whether it is soft, near-lens, bounced, negative fill, or absent.
- **Back/rim/kicker/hair**: edge separation; specify side and whether it should be subtle or graphic.
- **Background light**: controls depth behind the subject; specify gradient, pools, texture, silhouettes, or practical glows.
- **Catchlight/eye light**: small reflection in eyes; useful for portraits, avatars, beauty, and interviews.

Avoid asking for "three-point lighting" by itself. Instead describe the visible result: "soft key from camera-left at 45 degrees, weak fill near camera, narrow warm rim on hair, background two stops darker."

### Hard and soft light

**Documented fact**: ARRI's handbook states that light quality is characterized by the shadow edge and is determined by the physical size of the acting source, not intensity; larger or more diffused sources generally produce softer light. It also notes that soft light is forgiving for people but harder to control because spill can contaminate the background.

Use these promptable cues:

- **Hard light**: sharp shadow edges, defined nose shadow, crisp venetian-blind stripes, sun slash, noir texture, strong speculars, visible cut pattern.
- **Soft light**: broad source, wraparound skin, gradual shadow transfer, cloudy-day softness, diffused window, book light, softbox, bounce, silk.
- **Controlled soft light**: add "flagged spill," "negative fill on shadow side," "egg-crate/grid-like control," or "background remains darker despite soft key."

Production heuristic: If generated portraits look flat, do not merely ask for "cinematic." Add a directional key, reduced fill, negative fill, or a darker background plane.

### Color temperature, white balance, and color rendering

**Documented fact**: IES defines correlated color temperature (CCT) as the blackbody temperature whose chromaticity most closely resembles the source. IES defines color rendering index (CRI) as a measure of object color shift under a light compared with a reference source of comparable color temperature. ARRI's handbook describes tungsten fixtures as 3200K and warm relative to daylight, and stresses white-balancing for the subject area.

For generative prompts, Kelvin numbers are useful but not sufficient. Pair numbers with perceived color and motivation:

- Warm tungsten/practical: "warm 3000-3200K lamp glow," "amber practicals," "candlelike warmth."
- Neutral studio/daylight: "clean 5000-5600K daylight-balanced key," "neutral white product light."
- Cool shade/moon/monitor: "cool blue skylight," "cyan phone glow," "cold office fluorescents."
- Mixed color: "warm practical key plus cool moonlit window rim" or "cool overhead office ambience with a warm desk lamp accent."

Production heuristic: When asking for accurate product, food, makeup, or skin color, include "neutral white balance, high color fidelity, no colored cast on the product/skin unless specified." For mood pieces, allow color bias but protect brand-critical colors.

### Exposure, contrast, and ratios

**Documented fact**: Film/video lighting practice distinguishes key exposure, fill level, background level, and shadow detail; Burum emphasizes that day/night differences often come from the volume of highlights and blacks, not simply overexposure or underexposure. Rosco describes lighting ratio as key-to-fill comparison, with higher ratios creating more contrast.

For AI generation, express ratios as stops or plain-language shadow density:

- Low contrast / high key: "1:1 to 2:1 key-fill feel, open shadows, bright background, cheerful commercial exposure."
- Moderate cinematic: "key side at normal exposure, fill side one to two stops under, background slightly darker."
- Dramatic low key: "fill side three stops under, deep blacks but readable eyes, small rim separates silhouette."
- Silhouette: "subject mostly black against bright window, minimal facial detail, clear outline."

Avoid "underexposed face" unless the story requires it. Prefer "face at key exposure with darker environment" or "skin one stop under with catchlights preserved."

### Falloff and distance

**Documented fact**: Rosco summarizes the inverse-square law: light intensity decreases with the square of distance. For generated media, this matters as a visible cue even if the model is not physically simulating light.

Promptable cues:

- "rapid falloff into a dark background"
- "soft even light across the group"
- "bright near practical, darker corners"
- "subject moves through a pool of light and exits into shadow"
- "background remains two stops under despite the soft foreground key"

## Translate lighting into prompts

Use this structure when the model accepts natural-language prompting. Omit irrelevant fields, but preserve the order of thinking.

1. **Intent**: production type, mood, subject hierarchy.
2. **Motivation**: visible/implied light sources and why they exist.
3. **Lighting geometry**: source side, height, direction, softness, distance/falloff.
4. **Contrast/exposure**: key level, fill density, background value, highlights.
5. **Color**: white balance, color temperature, mixed sources, protected colors.
6. **Surface/camera cues**: skin texture, speculars, glass reflections, catchlights, product edges.
7. **Continuity constraints**: shot-to-shot consistency, time-of-day, same source direction.
8. **Negative constraints**: avoid flat frontal flash, blown highlights, muddy shadows, inconsistent light direction, random neon, plastic skin, extra catchlights.

Provider-independent prompt fragment:

```text
Lighting direction: motivated late-afternoon window light from camera-left, large soft source with gentle wrap, key side at normal exposure, fill side about two stops darker with negative fill, warm practical lamp visible in the background but not clipping, subtle cool rim from the window edge, background one stop under, natural skin texture, single clean catchlight, no flat front flash, no random colored light.
```

## Reference strategy

Do not hand the model an unlabeled moodboard and hope it infers lighting. Extract the lighting plan:

- Mark **source motivation**: "window," "practical lamp," "overcast sky," "softbox reflection."
- Mark **direction**: camera-left/right, overhead, below, back, three-quarter, near-lens.
- Mark **quality**: hard, soft, book light, bounced, gridded, bare bulb, fluorescent, neon, sun.
- Mark **contrast**: approximate key/fill/background relationship.
- Mark **color**: warm/cool/neutral and whether mixed sources are intentional.
- Mark **surface clues**: catchlights, specular streaks, rim edges, shadow transfer, reflection cards.

Use references ethically and operationally:

- Use lighting references for source geometry and contrast, not for copying a living artist's overall style or a competitor's protected trade dress.
- If matching a real person, product, location, or brand, preserve identity/brand details while varying lighting only within approved bounds.
- For multi-shot generation, reuse a small "lighting bible": source direction, CCT/mood, contrast level, practicals, background value, and forbidden artifacts.

## Common production setups

Treat these as starting points, not formulas.

### Interview / expert talking head

Goal: trustworthy face, readable eyes, dimensional background, stable continuity.

- Key: soft three-quarter key, usually slightly above eye level.
- Fill: soft near-camera fill or bounce; reduce for drama.
- Separation: small hair/rim if background tone is close to hair/clothing.
- Background: practicals or soft pools, darker than face unless intentionally high-key.
- QA: skin not waxy, eyes not dead, background not brighter than speaker unless motivated, no shifting light direction across cuts.

Prompt cues:

```text
calm premium interview lighting, large soft key from camera-left slightly above eye level, gentle shadow on camera-right cheek, weak near-lens fill, subtle hair light separating dark blazer from charcoal background, warm defocused practical lamp behind subject, face at natural exposure, clean catchlights, no flat webcam lighting, no blown forehead.
```

### Beauty, skincare, cosmetics, avatar close-up

Goal: flattering shape without erasing facial structure or product truth.

- Key: large soft frontal or three-quarter source; clamshell/butterfly works for glamour.
- Fill: reflector or lower soft fill to keep shadows delicate.
- Rim/accent: controlled edge light on hair/jawline if needed.
- Color: neutral or gently warm; protect makeup and skin tone.
- QA: pores may be softened but not plastic; eyes need catchlights; avoid hard nose shadows unless editorial.

Production heuristic: For avatars, add "consistent catchlights, stable face illumination, no flickering exposure between frames."

### Product / ecommerce

Goal: shape, material, color, and edge readability.

**Documented fact**: Broncolor notes that ecommerce setups must handle variation in product color, size, and glossiness, and describes clean background/reflection consistency as a business efficiency concern.

- Matte product: soft broad key plus subtle shadow to show form.
- Glossy product: control what the product reflects; specify white cards, black flags, long strip highlights, or gradient reflections.
- Transparent product: backlight or edge light to define contour; avoid muddy gray fill.
- Packaging: neutral white balance, controlled speculars, readable label, no color cast.
- Jewelry/liquid/metal: crisp intentional highlights, dark cards for edge definition, avoid chaotic reflections.

Prompt cues:

```text
studio product lighting on a white seamless set, large diffused softbox reflection across the left side of the glossy bottle, narrow black-card edge defining the right contour, clean white background with soft floor reflection, neutral daylight-balanced color, label evenly readable, controlled highlights, no random environment reflections, no blown logo.
```

### Cinematic interior

Goal: motivated mood and depth.

- Start from real sources: window, lamp, TV, streetlight, doorway, fireplace.
- Build layers: key for face, fill or negative fill for mood, practical glow for motivation, rim/background for depth.
- Use darkness intentionally: decide what must remain readable.
- QA: all faces in a dialogue scene should share a believable lighting world even if close-ups are sweetened.

### Day exterior / golden hour / overcast

Goal: believable time-of-day.

- Noon sun: high hard shadows, squint risk, strong contrast, short shadows.
- Golden hour: low warm directional sun, long shadows, warm rim, cooler sky fill.
- Overcast: large soft sky source, low contrast, saturated colors, weak cast shadows.
- Open shade: soft cool skylight, subject protected from direct sun, possible warm background.

For generated video, specify whether the sun direction remains constant as the camera moves.

### Night, neon, and screen-lit scenes

Goal: readable low light without arbitrary colored mush.

- Define at least one exposure anchor: practical lamp, sign, phone, car headlight, moon window, streetlight.
- Preserve a middle reference when possible: face, table surface, wardrobe, wall patch.
- Use colored light sparingly unless the genre calls for it.
- QA: blacks can be rich, but subject silhouette, eyes, or action should remain legible unless hiddenness is the point.

## Continuity for multi-shot images and video

Create a lighting bible before generating shot 2:

```text
Scene lighting bible:
- Time: late afternoon interior.
- Motivation: large window camera-left; warm table lamp in background camera-right.
- Key: soft window key, slightly above eye level, camera-left.
- Fill: negative fill camera-right; cheek shadow two stops under.
- Rim/background: subtle cool rim from window edge; background one stop under face.
- Color: neutral skin, warm practical glow, no neon.
- Continuity: same shadow direction in wide, medium, close-up; practical lamp remains visible or implied; face exposure stable.
```

For close-ups, allow sweetening but keep the same apparent source direction. If a model changes light direction between cuts, regenerate with explicit "same source direction as previous shot" and restate the bible.

## Iteration and troubleshooting

Diagnose lighting failures by visible symptom:

- **Flat image**: add directional key, darker fill, negative fill, background separation, or a controlled rim.
- **Unmotivated neon/random color**: remove generic "cinematic," specify motivated sources, forbid extra colored lights.
- **Muddy face**: bring face to key exposure, add catchlight, lift fill one stop, or move practical behind subject instead of on face.
- **Blown highlights**: specify "retain detail in lamp shade/forehead/logo," lower practical intensity, use soft rolloff.
- **Plastic skin**: ask for natural skin texture, broad soft source, no beauty-retouch haze, no over-smoothed speculars.
- **Chaotic product reflections**: specify the reflected environment: white cards, black flags, strip softbox, clean studio, no room clutter.
- **Inconsistent shot sequence**: restate lighting bible and regenerate the outlier only.
- **Wrong time of day**: describe shadow length, sun height, color, and sky fill; do not rely on "morning" or "night" alone.
- **Avatar flicker**: request stable exposure and consistent catchlights; avoid moving practicals and rapid color changes.

When iterating, change one lighting variable at a time unless the output is fundamentally wrong. Keep seeds/reference frames when the provider supports them.

## Accessibility, safety, and rights

**Documented fact**: W3C WCAG guidance warns that flashing content above three flashes per second, when large/bright enough, can trigger seizures; it also notes saturated red flashing is a special concern.

Apply this to generated media:

- Avoid strobe, lightning, muzzle flash, rapidly flickering signage, and hard cuts between full-screen bright/dark frames unless essential.
- For public ads, social content, avatars, and explainers, keep flashes at or below three per second or below recognized flash thresholds; when unsure, remove the effect or add a warning and test with an appropriate tool.
- Avoid using lighting to obscure required legal, medical, financial, or safety text.
- Do not use skin-lightening, age-erasing, or culturally biased "beauty" lighting as a default. Preserve the subject's intended complexion and identity.
- Do not mimic the lighting signature of a specific living photographer/cinematographer as a style target; translate observable lighting properties instead.

## QA checklist

Review the output frame by frame when video is involved:

- Is the primary light source motivated or intentionally stylized?
- Does shadow direction match the stated source?
- Are key subject, face, product, logo, or action readable?
- Is the fill level appropriate to the mood?
- Are hard/soft shadow edges intentional?
- Are skin tones, product colors, and brand colors protected?
- Do highlights retain important detail?
- Does the background support subject separation?
- Are catchlights and rim lights plausible rather than duplicated randomly?
- Does time-of-day read from shadow length, color, and background behavior?
- Do multi-shot outputs keep light direction, color, and exposure continuity?
- Are flashes, flickers, and bright cuts safe for the delivery context?

## Complete examples

### Example: cinematic one-shot prompt

Production intent: 8-second generated clip for a suspense trailer, interior hallway, no explicit violence.

Direction:

```text
An 8-second cinematic tracking shot down a narrow apartment hallway at night. Lighting is motivated by a warm practical table lamp visible at the far end and cool moonlight leaking through blinds from camera-left. The warm lamp creates a small pool of amber light on the floor and wall; the rest of the hallway falls into deep but readable shadow. Hard striped moonlight crosses the wall and briefly rims the subject's shoulder as they pass, while the face remains mostly in silhouette with one small catchlight. Low-key contrast, background blacks rich but not crushed, no random neon colors, no strobe, no flicker, no overexposed lamp shade. Keep the cool window direction consistent during the camera move.
```

Why it is structured this way: the prompt states motivation, direction, hard/soft quality, exposure, color contrast, action continuity, and safety constraints.

Likely failure modes: model adds colorful cyberpunk light; lamp clips to white; subject face becomes fully front-lit; moon stripes move inconsistently.

### Example: product lighting repair

User complaint: "The watch looks expensive, but the face is unreadable and the metal reflects a messy room."

Revision direction:

```text
Regenerate as a controlled studio product shot. Keep the luxury watch angle and black background, but replace environmental reflections with a clean reflected setup: long white strip softbox reflection along the left metal case edge, narrow black flag reflection defining the right case edge, soft overhead card for readable dial detail, small crisp highlight on the crystal that does not cover the logo or hands. Neutral white balance, premium low-key contrast, background fully clean, no room reflections, no blown dial, no distorted logo.
```

Why it is structured this way: glossy objects show the reflected environment, so the repair specifies what should be reflected rather than only asking for "better lighting."

### Example: interview continuity bible

Production intent: three social clips from one generated avatar/expert setup.

Lighting bible:

```text
Lighting bible for all shots:
- Premium editorial interview, dark teal office background.
- Large soft key from camera-left, slightly above eye level, natural skin texture.
- Fill side one and a half stops darker, not crushed.
- Small warm practical lamp behind camera-right, visible as soft bokeh, not a face key.
- Subtle cool rim on hair from camera-left rear.
- One clean catchlight per eye; no exposure flicker; no color temperature shifts across cuts.
- Background remains darker than the face and never competes with the speaker.
```

Shot prompt:

```text
Medium close-up of the same expert speaking calmly to camera, using the exact lighting bible: soft camera-left key, gentle darker fill side, warm practical bokeh behind camera-right, subtle cool hair rim, stable catchlights and exposure, natural skin, no flat webcam light, no shifting shadow direction.
```

## Sources and verification notes

Consequential craft facts were checked against the following sources on 2026-07-10:

- ARRI, "Lighting Handbook" page and linked ARRI Lighting Handbook PDF: lighting quality, hard/soft light, 3200K tungsten note, white balance, key/fill/separation/background definitions, spill control. https://www.arri.com/en/learn-help/lighting/lighting-handbook and https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf
- Illuminating Engineering Society glossary: CCT and CRI definitions. https://ies.org/definitions/correlated-color-temperature-cct-of-a-light-source/ and https://ies.org/definitions/color-rendering-index-cri-of-a-light-source/
- American Cinematographer, "Lighting a Set with Stephen H. Burum, ASC": key light, exposure, fill, shadow, day/night value structure, coverage continuity. https://theasc.com/article/lighting-a-set/
- Rosco Spectrum, "The Basics of Film Lighting": film-lighting vocabulary, three-point roles, inverse-square summary, hard/soft, practical and motivated lighting. https://spectrum.rosco.com/the-basics-of-film-lighting
- Academy of Motion Picture Arts and Sciences, ACES overview: device-independent color-management context. https://www.oscars.org/science-technology/sci-tech-projects/aces
- Broncolor, "The Ultimate Product Photography Lighting Setup": ecommerce variation in product color, size, glossiness, and consistency goals. https://broncolor.us/stories/the-ultimate-product-photography-lighting-setup/
- W3C, Understanding WCAG 2.2 Success Criterion 2.3.1: flash/seizure risk, three-flashes guidance, red-flash thresholds, and HDR testing context. https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html

No provider-specific model limits, pricing, or API parameters are specified in this skill; any such volatile facts must be verified in the selected provider skill or official docs at production time.
