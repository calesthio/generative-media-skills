---
name: visual-style-direction
description: Translate a creative brief, brand system, or reference set into an original, portable visual-direction system for image and video production. Use for art direction, reference analysis without imitation, design tokens, palette and contrast, typography, composition, texture and material, lighting, lens and camera language, motion language, cross-shot continuity, accessibility, production handoff, visual review, and repair; do not use for provider-specific API syntax or model-specific prompt recipes.
---

# Direct the visual system

Create a visual grammar that another production agent can execute repeatedly, not a pile of adjectives and not a clone of a reference. Translate intent into observable rules, encode the rules in portable artifacts, prove them on representative frames or shots, and repair the system rather than patching isolated outputs.

## Evidence labels used here

- **Documented fact** — a statement supported by a standard, first-party technical document, or institutional source.
- **Research finding** — a result from a cited empirical study; apply only within the study's limits.
- **Production heuristic** — a practical rule of thumb. Treat it as a testable default, not a law.

Keep these categories distinct in the direction packet. Never present taste, convention, or a provider behavior as a standard.

## Deliverable contract

Produce a **visual direction packet** that is usable without access to the original conversation. It must contain:

1. brief interpretation and unresolved assumptions;
2. a one-sentence direction thesis;
3. reference ledger and originality analysis;
4. invariants, controlled variables, and explicit anti-patterns;
5. palette, contrast pairs, typography, layout, texture/material, lighting, camera/lens, and motion systems;
6. continuity rules for recurring subjects, locations, graphics, and shots;
7. accessibility and rights constraints;
8. portable design tokens plus non-token production rules;
9. image and video adaptation rules, including aspect-ratio behavior;
10. representative proof-frame or proof-shot specifications;
11. handoff metadata, acceptance tests, and a repair log.

Do not bury decisions in prose. Every consequential choice needs a stable name, rationale, allowed range, and test.

## Scope boundaries

Use this skill to decide **what the work should look and move like** across tools. Hand the resulting system to image-generation, video-generation, animation, editing, layout, or finishing skills.

Do not:

- prescribe a provider, endpoint, model identifier, seed syntax, or provider-specific prompt grammar;
- substitute a mood board for a production specification;
- promise that a generated sample guarantees continuity across a batch;
- infer permission to use brand assets, likenesses, locations, fonts, footage, or reference works;
- claim legal clearance. Surface the facts and request review when risk is material.

## Start with constraints, not aesthetics

Extract the following before proposing a direction:

| Area | Questions to resolve |
|---|---|
| Communication | What must the viewer understand, feel, remember, or do? |
| Audience | Who is included, excluded, represented, or potentially misread? |
| Brand | Which supplied assets and rules are authoritative? Which are only examples? |
| Deliverables | Still, sequence, film, social cutdowns, thumbnails, UI, print; required ratios and durations? |
| Production | Live action, generated media, 2D/3D, compositing, edit, or a hybrid? What can actually be controlled downstream? |
| Continuity | Which subjects, products, spaces, props, wardrobe, marks, and facts recur? |
| Accessibility | Captions, audio description, reduced-motion version, text alternatives, contrast target, reading conditions? |
| Rights | Source, owner, license, territory, term, model/property releases, trademark constraints, synthetic-media disclosure? |
| Color | SDR/HDR, display/print targets, working space, output transform, embedded profile, review environment? |
| Approval | Who approves the route, proof frames, continuity sheet, and final master? |

If a missing answer changes the direction materially, ask. If it only changes an implementation detail, state a reversible assumption and continue.

## Analyze references without imitating them

### Build a reference ledger

Record every reference with:

- identifier and source;
- who supplied it;
- known owner and usage permission;
- intended use: content, mood, composition, material, lighting, optical, motion, typography, or production technique;
- **observed evidence**: what is visibly or audibly present;
- **interpretation**: the effect that evidence creates;
- **transferable mechanism**: an abstract rule that can be reused;
- **identity-bearing details to exclude**: protected artwork, distinctive character design, logo, trade dress, exact layout, signature motif, unique prop, recognizable sequence, or artist-specific combination;
- confidence and unresolved questions.

Use descriptions such as “low-key side light with rapid falloff and a small warm practical in the background,” not “cinematic like Reference A.”

### Decompose at four levels

1. **Purpose** — what communication job is the reference doing?
2. **Mechanism** — how do hierarchy, rhythm, contrast, staging, or camera choices perform that job?
3. **Surface** — which palette, texture, type, props, and motifs make it recognizable?
4. **Identity** — which exact expressive choices or brand signals belong to that source?

Transfer purpose and general mechanisms. Rebuild surface choices from the new brief. Exclude identity-bearing details unless supplied and licensed for use.

**Research finding:** Controlled design-fixation experiments found that examples can cause designers to reproduce example features and narrow conceptual output. The finding originated in engineering-design tasks, so use it as a warning about reference exposure, not proof that every mood board causes fixation. Counter it by analyzing multiple functionally different sources, delaying surface decisions until the brief is stated, and documenting exclusions. See Jansson and Smith, “Design Fixation,” *Design Studies* 12(1), 1991 ([DOI page](https://doi.org/10.1016/0142-694X(91)90003-F)).

### Run an originality pass before route approval

Ask:

- If the reference were hidden, would the proposed system still follow from the brief?
- Are its distinctive composition, palette relationship, motif, typography, and camera sequence all retained together? If so, redesign.
- Does one reference dominate more than one identity-bearing layer?
- Can each major choice be justified by audience, message, production, or brand evidence?
- Is the result likely to imply affiliation with another source or brand?
- Could a reviewer point to a particular frame or work and identify copied expressive details?

**Documented fact, U.S. context:** The U.S. Copyright Office notes that style standing alone is generally not protected by copyright, while original pictorial and graphic expression can be protected and permission may be needed to use another person's work. That distinction does not make imitation risk-free: individual expressive elements, derivative-work rights, contract, publicity, and trademark issues remain. The USPTO explains that confusing similarity can arise from appearance, meaning, or overall commercial impression. Use this as a risk screen, not legal advice. See the [Copyright Office Digital Replicas report](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-1-Digital-Replicas-Report.pdf), [Copyright for Visual and Graphic Artists](https://www.copyright.gov/engage/visual-artists/), and [USPTO likelihood-of-confusion guidance](https://www.uspto.gov/trademarks/search/likelihood-confusion).

When a user names a living artist or asks for a near-copy, decline the identity-bearing imitation and offer a mechanism-based direction using broader era, medium, lighting, composition, material, and emotional attributes.

## Create contrastive routes, then converge

Propose two to four routes that solve the same communication problem through meaningfully different systems. Change at least three structural dimensions across routes, such as:

- hierarchy and information density;
- spatial organization and negative space;
- chroma/value strategy;
- material logic;
- lighting logic;
- optical distance and camera behavior;
- motion energy and transition logic;
- typography role.

Do not make “Route B” a color swap of Route A.

For each route, provide:

- name and one-sentence thesis;
- three governing principles;
- signature move;
- proof-frame description;
- likely strength;
- likely failure mode;
- cost/complexity implication;
- reference mechanisms used and identity details excluded.

Recommend one route against the brief. Preserve rejected routes as decision history; do not silently blend them into the approved route.

## Write the direction thesis and grammar

The thesis must contain a communication intent, a visual tension, and a behavioral rule.

Weak: “Premium, modern, cinematic.”

Strong: “Make technical precision feel tactile: rigid editorial geometry contains warm, imperfect materials, while the camera moves only when a relationship becomes clearer.”

Translate the thesis into:

- **invariants** — must remain stable across every asset;
- **controlled variables** — may change within named ranges;
- **exceptions** — allowed only in stated narrative conditions;
- **anti-patterns** — tempting moves that would break the direction.

### Invariant/variable test

| Element | Invariant | Controlled variable | Failure signal |
|---|---|---|---|
| Subject | recognizable silhouette, product geometry | pose, crop, expression | anatomy/mark changes between shots |
| Composition | one dominant mass, upper-left text reserve | subject scale 35–60% frame height | equal-weight clutter |
| Light | large cool key, narrow warm practical | key angle ±15°, practical position | flat frontal fill or mixed-white imbalance |
| Motion | purposeful translation, no idle drift | amplitude by beat importance | constant motion with no information role |

## Encode a portable token layer

Use tokens for reusable atomic and semantic values. Use prose or structured ledgers for relationships that are not reducible to a value, such as “camera movement must reveal causality.”

Separate:

1. **primitive tokens** — raw color, dimension, duration, typeface, weight;
2. **semantic tokens** — `color.text.primary`, `color.surface.hero`, `motion.duration.emphasis`;
3. **application rules** — “hero text uses `color.text.on-dark` only over surfaces passing the target contrast test.”

Avoid names tied to a current value (`blue-500`) when the role matters (`accent-action`). Keep source values and output-space values distinct.

When a color token carries redundant representations such as numeric `components` and a fallback `hex`, validate that they encode the same color in the declared color space. Prefer one authoritative representation over contradictory convenience fields. Run a token parser or color-conversion check before handoff; a syntactically valid token with mismatched values is not portable.

**Documented fact:** The Design Tokens Community Group describes tokens as a platform-agnostic way to exchange design decisions. Its first stable format, 2025.10, uses typed tokens with `$value`, supports groups and references, and defines types including color, typography, dimension, duration, stroke, gradient, and shadow. Verified 2026-07-09. Follow the stable specification when interchange is required; keep camera, lighting, composition, and continuity ledgers beside it rather than inventing nonstandard token types. See [DTCG Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/).

### Example: portable DTCG token excerpt

This is an example, not a mandatory palette.

```json
{
  "color": {
    "ink": {
      "$type": "color",
      "deep": {
        "$value": {
          "colorSpace": "srgb",
          "components": [0.055, 0.071, 0.09],
          "hex": "#0E1217"
        }
      }
    },
    "text": {
      "$type": "color",
      "on-dark": {
        "$value": {
          "colorSpace": "srgb",
          "components": [0.957, 0.941, 0.902],
          "hex": "#F4F0E6"
        }
      }
    }
  },
  "motion": {
    "duration": {
      "$type": "duration",
      "settle": { "$value": { "value": 420, "unit": "ms" } }
    }
  },
  "type": {
    "title": {
      "$type": "typography",
      "$value": {
        "fontFamily": ["Approved Display Family", "sans-serif"],
        "fontSize": { "value": 64, "unit": "px" },
        "fontWeight": 650,
        "lineHeight": 1.02
      }
    }
  }
}
```

Also provide a human-readable token table with role, value, allowed use, prohibited use, contrast partners, and fallback.

Label numeric layout, type, motion, and safe-area ranges as proof-set starting points until they have been tested against the actual regulated copy, device sizes, platform UI, viewing distance, and encoded deliverables. Promote them to approved constraints only after the relevant proof gate passes.

## Build the color and contrast system

Define color by function and relationship:

- canvas/surface hierarchy;
- primary text and secondary text;
- brand/accent roles;
- semantic states;
- data-series colors;
- skin/product protection ranges if relevant;
- highlight/shadow hue bias;
- saturation budget;
- monochrome fallback;
- output color space and review transform.

Specify dominant/support/accent proportions as flexible ranges, not decorative arithmetic. Test all important pairs on actual textured, graded, and moving backgrounds—not only flat swatches.

**Documented fact:** WCAG 2.2 Level AA specifies at least 4.5:1 contrast for normal text, 3:1 for large text, and 3:1 for graphical objects needed to understand content. It also states that color must not be the only visual means of conveying information. These are web-content criteria, not a universal cinema-grading standard; use them as minimum acceptance tests for web/UI overlays, captions, diagrams, and related assets, then test in the real delivery environment. See [WCAG 2.2 §§1.4.1, 1.4.3, 1.4.11](https://www.w3.org/TR/WCAG22/).

For moving footage, evaluate worst-case frames. Add a backing plate, local darkening, outline, shadow, repositioning, or alternate color token when a pair fails. Never “solve” contrast solely by making everything white or black if hierarchy is lost.

### Color-management handoff

Record:

- source and working color spaces;
- transfer function/gamma where applicable;
- display/view transform used for approvals;
- target deliverable space and peak luminance where applicable;
- embedded ICC profile or equivalent metadata;
- LUT/look-transform name, version, and whether it is creative or technical;
- review-monitor assumptions;
- SDR/HDR trim strategy;
- gamut and clipping checks.

**Documented fact:** ICC profiles connect color encodings across devices, and embedded profiles support interpretation of image data across systems. ACES separates a creative Look Transform from an Output Transform for a specific display and viewing condition; ACES Metadata Files can track input, look, and output transforms. Do not bake an unknown display look into source assets and call it portable. See the [ICC profile-format introduction](https://www.color.org/iccprofile.xalter), [ACES system overview](https://docs.acescentral.com/background/overview/), [ACES Look Transforms](https://docs.acescentral.com/system-components/look-transforms/), and [ACES Output Transforms](https://docs.acescentral.com/system-components/output-transforms/).

## Specify typography as behavior

For each role—display, heading, body, caption, data label, supers, legal—specify:

- approved family and licensed files;
- fallback stack;
- supported scripts/languages and missing-glyph plan;
- weight, width, optical size, case, tracking, leading;
- minimum rendered size at each delivery resolution;
- maximum line length/line count;
- alignment and rag behavior;
- background treatment;
- safe-area behavior;
- entrance, hold, emphasis, and exit behavior for time-based work;
- localization expansion tolerance.

Do not describe a typeface only as “bold sans.” Test the exact family at final pixel size, compression, motion, and viewing distance. Keep essential copy editable until final render; generation systems are not reliable typesetters.

For captions, reserve a predictable region, include speaker and non-speech information when required, and prevent important visual content from occupying that region. WCAG defines captions as synchronized equivalents for speech and needed non-speech audio and requires captions for prerecorded synchronized media at Level A; it requires audio description for prerecorded video at Level AA when visual information is not already conveyed. See [WCAG 2.2 time-based media](https://www.w3.org/TR/WCAG22/#time-based-media).

## Design a composition system

Define a small set of compositional behaviors rather than one frozen layout:

- focal hierarchy: primary, secondary, ambient;
- grid and safe regions by aspect ratio;
- dominant mass and counterweight;
- negative-space ownership;
- text/image collision policy;
- horizon and eye-line bands;
- depth layers and overlap rules;
- edge energy and cropping rules;
- symmetry/asymmetry preference;
- allowable camera-facing product or logo zones;
- data/diagram legibility rules.

Specify **recomposition**, not cropping, for each required ratio. State which relationship survives when horizontal space becomes vertical space. For example: “In 9:16, preserve the subject-to-title diagonal and move proof points below the subject; do not center-stack every element.”

**Production heuristic:** Use one deliberate rule-breaking event per sequence. A centered, flat, or full-bleed exception reads as emphasis only when the baseline grammar is stable.

## Define texture, material, and image construction

Name materials through observable properties:

- roughness/specularity;
- translucency/opacity;
- scale of grain or imperfection;
- edge wear and surface history;
- fabrication method;
- interaction with light;
- whether texture lives on the object, lens, atmosphere, or final image.

Avoid contradictory bundles such as “matte mirror chrome” unless the contradiction is intentional and explained. Separate:

- **world texture** — paper fiber, brushed metal, skin, cloth;
- **capture texture** — grain, halation, diffusion, motion blur, lens artifacts;
- **graphic texture** — dithering, screen print, noise field;
- **compression artifacts** — usually defects, not style.

Set an imperfection budget. If every surface is distressed, nothing reads as intentional.

## Define lighting as a repeatable setup

Describe:

- key source size, direction, height, hardness, and color;
- fill ratio or shadow intent;
- negative fill;
- back/rim separation;
- practical lights and their narrative role;
- ambient/environment contribution;
- exposure priority and highlight protection;
- time-of-day and weather constraints;
- continuity tolerances;
- forbidden setups.

Use diagrams or clock positions when useful. “Moody” is not a setup.

### Example: lighting rule

This is an example, not a universal recipe.

> One large cool key 35–50° camera-left and slightly above eye line; negative fill camera-right; one dim warm practical at least one subject-width behind; protect pale product labels from clipping; no frontal ring-light catchlight; keep shadow direction consistent across adjacent shots.

## Define lens and camera language

Describe the viewer–subject relationship first, then the optical means:

- intimacy or observation;
- camera height and subject distance;
- angle of view or full-frame-equivalent focal-length family;
- sensor/crop assumption;
- depth-of-field intent and focus behavior;
- camera support: locked, handheld, dolly, gimbal, crane, virtual;
- movement trigger, path, amplitude, speed, and stop condition;
- shutter/motion-blur intent;
- distortion and breathing tolerance;
- transition between shot sizes;
- prohibited moves.

**Documented fact:** Shorter focal lengths give a wider angle of view and longer focal lengths a narrower one; keeping a subject the same size while changing focal length requires changing camera position, which changes the visible background and perspective impression. Sensor format also changes angle of view for the same focal length. Therefore record angle-of-view intent, subject distance, and sensor assumption—not a millimeter number alone. See Sony's first-party [Lens Basics](https://www.sony.com/electronics/support/articles/00268239) and Nikon's [Understanding Focal Length](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/understanding-focal-length).

### Example: camera grammar

This is an example for a calm technical product film.

- Establish spaces at a moderate-wide angle from human eye height; keep verticals disciplined.
- Explain assembly with a normal-angle three-quarter view and deep enough focus to preserve part relationships.
- Reserve close, shallow-focus shots for material proof, never for critical instructions.
- Move only to reveal a hidden relationship; start and end on stable compositions.
- Do not orbit continuously, use simulated drone moves indoors, or alternate extreme-wide and long-lens portraits without a narrative reason.

## Define motion as a semantic system

For each motion class, specify **purpose, object, path, duration range, easing character, overlap, sound relationship, and reduced-motion alternative**.

Useful classes include:

- reveal;
- orient/reframe;
- compare/transform;
- emphasize;
- transition;
- ambient/world motion;
- camera motion;
- type motion;
- logo/brand motion.

Build a tempo map for the sequence. Identify rests, accents, accelerations, and the maximum number of simultaneous moving groups. Preserve object identity when transitioning between states.

**Research finding:** In two controlled experiments on transitions between statistical graphics, appropriately designed animated transitions improved graphical perception; the result is specific to related data graphics, not proof that animation always helps. Apply it when motion clarifies correspondence or change, not as a reason to animate decoration. See Heer and Robertson, “Animated Transitions in Statistical Data Graphics,” IEEE TVCG 13(6), 2007 ([paper page](https://idl.uw.edu/papers/animated-transitions)).

**Practitioner guidance with limited scope:** Apple's interface guidelines advise purposeful, optional, brief motion and alternatives for motion-sensitive users. Material Design's published duration values are platform conventions, not universal film timing; use its deeper principle—scale duration with distance and complexity—without copying its milliseconds into unrelated media. See [Apple Motion](https://developer.apple.com/design/human-interface-guidelines/motion) and [Material duration and easing](https://m1.material.io/motion/duration-easing.html).

### Motion safety

- Do not use flashing as emphasis. WCAG 2.2 prohibits content that flashes more than three times in one second unless it remains below defined thresholds.
- Provide a reduced-motion version when motion is not essential; replace large translation, parallax, zoom, and simulated depth with cuts, dissolves, highlights, or opacity changes that preserve meaning.
- Do not encode essential meaning only through movement.
- For interactive work, respect the platform's reduced-motion preference.

See [WCAG 2.2 §2.3](https://www.w3.org/TR/WCAG22/#seizures-and-physical-reactions) and Apple's [Reduced Motion evaluation criteria](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria).

## Build continuity before generating a batch

Create a continuity bible for every recurring entity:

- canonical name and ID;
- approved reference views;
- silhouette and proportion anchors;
- face/hair/skin or product geometry;
- wardrobe, props, logos, labels, and text;
- palette/material values;
- lighting and time-of-day state;
- location layout and screen direction;
- camera/lens and depth-of-field state;
- action start/end states;
- facts that may change and the beat where they change;
- non-negotiable exclusions.

Maintain a shot ledger with scene, shot, story time, entity state, screen direction, eye line, camera height, angle of view, focus target, lighting state, props, approved take/asset, and exceptions.

**Documented fact:** ScreenSkills describes script supervision as maintaining written and photographic records of action, costume, props, eye lines, camera, and lens details so shots made out of sequence can edit together consistently. Adapt that recordkeeping discipline to generated and hybrid media. See [ScreenSkills: Script Supervisor](https://www.screenskills.com/job-profiles/browse/film-and-tv-drama/technical/script-supervisor-film-and-tv-drama/).

Generate or shoot a **continuity anchor set** before the batch: neutral front/three-quarter/profile views, key expression or product states, material close-ups, lighting reference, and one difficult interaction. Reject a direction that cannot survive these tests.

## Design for accessibility from the beginning

Include:

- contrast-tested foreground/background pairs;
- non-color redundancy for states and data;
- text alternatives for informative stills and complete equivalents for complex diagrams;
- caption region, styling, and collision rules;
- audio-description plan for information conveyed only visually;
- reading-time and hold-time checks;
- reduced-motion version;
- flash analysis;
- localization and script support;
- small-screen and low-bandwidth variants;
- review by people using relevant assistive technology when feasible.

**Documented fact:** W3C's image tutorial says text alternatives should convey an image's purpose, and complex graphics need a complete text equivalent of their data or information. See [WAI Images Tutorial](https://www.w3.org/WAI/tutorials/images/).

Do not claim that a contrast score alone makes a visual accessible. Test comprehension, sequencing, captions, audio description, and motion alternatives in context.

## Preserve rights and provenance in the handoff

For every supplied or produced asset, record:

- asset ID and filename;
- creator/source;
- creation method;
- license/permission and restrictions;
- model/property release status where applicable;
- modifications;
- required credit;
- expiration/territory/placement limits;
- synthetic or composite disclosure requirements;
- link to original and approval evidence;
- color profile and technical metadata.

**Documented fact:** IPTC Photo Metadata provides descriptive, rights, and administrative fields, including copyright notice, rights-usage terms, instructions, credits, and digital-source information. C2PA Content Credentials provide a technical structure for recording media provenance and history; they establish provenance claims, not truth by themselves. The current C2PA specification shown by its official site was 2.4 when verified 2026-07-09. See [IPTC Photo Metadata 2025.1](https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata-2025.1.html) and [C2PA specifications](https://spec.c2pa.org/about/).

## Assemble the production handoff

Use this minimum structure:

```markdown
# Visual Direction: <project>

## Status
Version, owner, date, approval state, target deliverables

## Direction thesis
One sentence

## Brief interpretation
Audience, message, response, constraints, assumptions

## References and originality
Ledger; mechanisms adopted; identity details excluded; rights status

## Visual grammar
Invariants; controlled variables; exceptions; anti-patterns

## Systems
Color/contrast; typography; composition; texture/material; lighting;
camera/lens; motion; continuity; accessibility; color management

## Tokens
DTCG-compatible token block plus human-readable mapping

## Adaptation matrix
Still/video; 16:9, 9:16, 1:1, other targets; SDR/HDR; localization

## Proof set
Representative frames/shots, difficult cases, expected pass criteria

## Asset and rights ledger
Source, license, releases, credits, provenance, technical metadata

## Acceptance tests
Binary checks and subjective review questions

## Decision and repair log
Change, reason, affected rules/assets, approver
```

Add machine-readable JSON or YAML only if the production pipeline consumes it. Keep the prose packet as the semantic source of truth and ensure identifiers match across both.

## Review the system, not just the beauty frame

Review at five gates.

### Gate 1 — Brief fidelity

- Does the hierarchy communicate the intended message without explanation?
- Is the emotional read appropriate to the audience and context?
- Are all assumptions visible?

### Gate 2 — Originality and rights

- Can every adopted reference mechanism be named abstractly?
- Have identity-bearing details been removed or licensed?
- Does the result imply an unintended brand affiliation?
- Are font, image, likeness, location, and asset permissions recorded?

### Gate 3 — System coherence

- Do palette, type, composition, material, light, camera, and motion express the same thesis?
- Are invariants stable across easy and difficult cases?
- Are exceptions deliberate and logged?

### Gate 4 — Production resilience

- Does the direction work in every target ratio and at thumbnail size?
- Can it survive localization, compression, low light, mixed footage, and batch generation?
- Are color transforms and metadata reproducible?
- Can another agent implement it without guessing?

### Gate 5 — Accessibility and continuity

- Do overlays and essential graphics meet the declared contrast target on worst-case frames?
- Is information redundant beyond color and motion?
- Are captions, text alternatives, audio description, and reduced motion planned?
- Do recurring entities and spatial relationships remain consistent?

## Repair by diagnosis

Do not respond to “it feels off” with more adjectives. Locate the failing layer.

| Symptom | Likely cause | Repair order |
|---|---|---|
| Assets look individually good but unrelated | invariants too vague; too many uncontrolled variables | freeze 3–5 invariants; rebuild anchor set; regenerate/regrade outliers |
| Looks like the reference | surface/identity copied instead of mechanism | remove signature combination; introduce brief-derived composition, material, and type changes; rerun originality pass |
| Brand feels pasted on | logo treated as the only brand signal | move brand values into hierarchy, palette roles, material, voice, and motion; reduce logo dependence |
| “Cinematic” but empty | optical effects substituted for story hierarchy | restate communication beat; simplify camera; assign each move a reveal or relationship |
| Text passes on swatches but fails in video | dynamic background and compression ignored | test worst-case frames; add backing treatment or reposition; retest after encode |
| Batch continuity drifts | no canonical states or change ledger | build anchor views; assign entity IDs; lock shot ledger; repair highest-visibility contradictions first |
| Motion feels mechanical | identical timing/easing and no semantic classes | define reveal/orient/emphasize classes; vary by distance and importance; add rests |
| Direction collapses in 9:16 | cropping used instead of recomposition | preserve relationship hierarchy; define ratio-specific grid and negative-space ownership |
| Grade differs across systems | missing color-management contract | identify source/working/output spaces; restore transforms and profiles; reapprove on declared display |

Repair in this order:

1. communication and factual correctness;
2. rights, safety, and accessibility;
3. continuity and identity;
4. hierarchy and composition;
5. light, color, and material;
6. camera and motion;
7. surface polish.

Changing grain while the hierarchy is wrong is not a repair.

## Complete example: original visual direction from mixed references

This is a complete example, not a mandatory formula.

### Production intent

Create a 30-second launch film plus six stills for a repairable modular desk lamp. Audience: design-conscious renters. Desired response: “This is engineered, calm, and made to last.” Deliverables: 16:9 hero, 9:16 cutdown, 1:1 stills. The client supplies a logo, CAD renders, product colors, one 1970s industrial catalog, one contemporary museum campaign, and macro photographs of anodized aluminum.

### Reference ledger excerpt

| Reference | Observed evidence | Transferable mechanism | Exclude |
|---|---|---|---|
| Industrial catalog | orthographic product views; dense part labels; warm off-white stock | evidence-led diagrams; numbered assembly logic; restrained warm ground | exact grid, typeface, illustrations, page damage |
| Museum campaign | one oversized object; wide negative space; title at edge | scale contrast and edge tension | signature crop, exact red/black palette, logo placement |
| Aluminum macros | directional brushing; cool highlight; soft falloff | material proof through grazing light | source photographs unless licensed |

### Direction thesis

“Turn repairability into quiet theater: precise diagram geometry meets tactile, softly worn materials, and every camera move reveals how one part connects to another.”

### Invariants

- one dominant object or assembly relationship per frame;
- warm mineral canvas with charcoal type and one oxidized-copper accent;
- brushed material texture remains directional and physically plausible;
- camera starts or ends on a stable diagram-like view;
- motion reveals connection, rotation, or replacement—never idle orbiting;
- labels are live type and never generated into imagery.

### Controlled variables

- canvas from light mineral to deep charcoal by narrative beat;
- object scale 45–85% of frame height;
- accent occupies 2–10% of visible area;
- focus ranges from deep for assembly to shallow for non-instructional material proof;
- texture age from pristine to lightly handled; no heavy distress.

### Anti-patterns

- glossy black “luxury tech” staging;
- neon cyberpunk rim light;
- floating exploded parts with no clear assembly path;
- archival catalog imitation;
- constant parallax, speed ramps, or lens flares;
- copper accent used as a full-frame wash.

### Core palette

| Token role | Example sRGB | Use | Pairing test |
|---|---:|---|---|
| `surface.mineral` | `#E9E3D7` | primary canvas | charcoal normal text ≥4.5:1 |
| `surface.charcoal` | `#15191C` | night/closing canvas | mineral normal text ≥4.5:1 |
| `text.primary` | `#1D2327` | primary text on mineral | verify after texture/encode |
| `accent.connection` | `#A84F35` | fasteners, active relationship, key label | never sole state cue; add shape/label |
| `material.aluminum` | measured/graded, not a flat swatch | product surface | preserve neutral highlights |

### Typography

- Display: approved humanist grotesk, medium width, sentence case, 1.02–1.08 line height.
- Technical labels: approved mono or tabular face, minimum size set per output resolution after encode test.
- Maximum: one title plus three labels in a hero frame.
- Labels attach by fine rules but remain outside moving hardware paths.
- 9:16: labels shift below the object; they do not shrink below minimum.

### Composition

- 16:9 hero: object centered 8% right of frame; title owns upper-left; action enters from lower-left.
- 9:16: object moves to upper two-thirds; title precedes it; labels form a bottom evidence band.
- 1:1 still: use one assembly relationship or material fact, never the whole exploded view.

### Lighting and camera

- Large soft key 40° camera-left; narrow harder graze from rear-right reveals brushing; negative fill below lens.
- Assembly: moderate-normal angle, camera near product mid-height, deep-enough focus for relationship.
- Material proof: close view with a longer angle and shallow focus, but keep the brushed direction and edge geometry readable.
- No extreme wide-angle product distortion.

### Motion

| Class | Purpose | Timing character | Reduced-motion version |
|---|---|---|---|
| Orient | move from whole lamp to joint | slow-in, decisive settle | cut from whole to joint with matched position |
| Reveal | expose replaceable fastener | short masked slide tied to part movement | two-state cut plus highlight |
| Compare | old module to new module | staged, one change at a time | side-by-side static comparison |
| Emphasize | confirm connection | brief copper line pulse; no flashing | persistent copper outline and label |

### Continuity anchors

- CAD-verified front, rear, side, and three-quarter silhouettes;
- joint geometry and fastener count;
- cable exit position;
- product color values under neutral review light;
- brushed direction per part;
- approved logo size and orientation;
- assembly state at the beginning and end of each shot.

### Proof set

1. Hero whole-product frame with title and contrast test.
2. Difficult close-up showing aluminum, dark joint, and label.
3. Exploded assembly frame with three labels and clear ordering.
4. 9:16 recomposition.
5. Reduced-motion comparison frame.
6. Worst-case compressed frame for caption/label review.

### Acceptance tests

- Viewer can state the replaceable part after a silent viewing.
- No frame relies only on copper color to identify the active part.
- All product geometry matches the approved anchor set.
- Normal web text/labels meet the declared 4.5:1 target on worst-case frames.
- Every moving part begins and ends in a logged assembly state.
- A reviewer cannot identify one supplied reference as the visual template.
- Source, license, font, product, color-profile, and synthetic-media metadata are present.

### Likely failures and repairs

- If it resembles the catalog, remove its exact grid and typography; keep only numbered evidence logic.
- If the product feels cold, adjust material wear and warm canvas before adding orange light.
- If 9:16 feels cramped, reduce simultaneous labels and create a bottom evidence band; do not miniaturize.
- If continuity drifts, return to CAD silhouette and joint anchor frames before changing style.

## Complete example: respond to an imitation request

This is a complete example of a safe, useful redirection.

### User request

“Make my skincare campaign exactly like this living photographer's feed: same peach shadows, tight crops, wet glass, and serif.”

### Expected response and workflow

1. Acknowledge the desired communication read: intimate, tactile, editorial skincare.
2. Decline an exact imitation of a living creator's recognizable combination.
3. Decompose the mechanisms: warm low-angle color contrast, macro material evidence, partial crops, translucent surfaces, restrained editorial type.
4. Rebuild from the client's product and audience:
   - mineral green and amber instead of peach;
   - dry carved stone plus condensation, not the same wet-glass world;
   - top-lit still-life geometry instead of the same crop family;
   - a licensed contemporary sans with narrow technical captions instead of the reference serif;
   - slow vertical focus transitions only when ingredient layers change.
5. Provide two proof-frame specifications and an originality test.

### Resulting thesis

“Show clinical transparency through geological tactility: translucent product layers rest against carved mineral forms, with top light exposing ingredients and motion reserved for changes in layer or focus.”

### Expected result

The campaign preserves the requested intimacy and tactile evidence but has a different palette structure, material world, composition, typography, and camera behavior. It can be defended from the brief rather than from the photographer's identity.

## Sources and verification notes

- Design Tokens Community Group, [Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/). Stable-version status verified 2026-07-09.
- W3C, [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/) and [Images Tutorial](https://www.w3.org/WAI/tutorials/images/). Accessed 2026-07-09.
- Academy Software Foundation / Academy of Motion Picture Arts and Sciences, [ACES documentation](https://docs.acescentral.com/background/overview/). ACES 2 terminology and documentation checked 2026-07-09.
- International Color Consortium, [Introduction to the ICC profile format](https://www.color.org/iccprofile.xalter). Accessed 2026-07-09.
- C2PA, [Specifications](https://spec.c2pa.org/about/). Current displayed version 2.4 verified 2026-07-09.
- IPTC, [Photo Metadata Standard 2025.1](https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata-2025.1.html). Version verified 2026-07-09.
- U.S. Copyright Office and USPTO sources cited above reflect U.S. law and agency guidance; jurisdiction and contracts can change the analysis. Accessed 2026-07-09.
- Jansson & Smith (1991) and Heer & Robertson (2007) are peer-reviewed research findings applied here within their studied domains.
- Apple and Material sources are first-party platform guidance, used as bounded practitioner guidance rather than universal timing standards.
