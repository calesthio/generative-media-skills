---
name: character-design-continuity
description: Provider-independent character design and continuity direction for generated media. Use when an agent must create, preserve, revise, or QA a recurring character across AI-generated images, video clips, avatars, animation, comics, ads, product mascots, serialized social posts, or multi-shot campaigns; especially when building character bibles, reference packs, prompts, expression/pose ranges, costume/hair/makeup/prop continuity, identity and likeness safeguards, iteration plans, handoff notes, or continuity reviews.
---

# Character Design Continuity

Use this skill to make a character stay recognizably the same while still acting, aging, changing costume, moving through shots, or adapting to a campaign's style. Treat continuity as a production system, not a single prompt trick.

## Ground rules

Separate three kinds of guidance in your reasoning:

- **Documented facts**: cite a source or the user's approved materials.
- **Empirical observations**: describe what happened in the latest generation or test batch.
- **Production heuristics**: useful craft rules that improve odds but are not guarantees.

Do not promise perfect identity preservation from text prompts alone. Current image and video systems can drift on facial structure, body proportions, hands, age, wardrobe, markings, props, and style. Strong continuity comes from a character bible, reference strategy, constrained prompt planning, iterative selection, and QA.

## Start with the continuity intent

Before designing or repairing a character, identify:

1. **Continuity target**: exact likeness, fictional identity, brand mascot, archetypal role, or loose style family.
2. **Delivery form**: stills, multi-shot video, avatar, rigged animation, comic panels, ad variants, social serial, game/UI asset.
3. **Allowed variation**: expression range, pose range, wardrobe changes, age/time jumps, lighting, camera angle, art style changes, season/event variants.
4. **Hard invariants**: features that must not drift.
5. **Rights status**: fictional original, licensed IP, employee/customer likeness, public figure, minor, deceased person, or composite inspired by real people.
6. **Model/reference capabilities**: whether the provider supports reference images, image-to-image, masks, seeds, character-reference tokens, identity adapters, fine-tuning, LoRA/DreamBooth-like personalization, or only text.

If exact likeness or a recognizable real person is involved, pause for consent and scope before prompt writing. As of verification on 2026-07-10, U.S. law is still a patchwork for publicity/privacy/digital replicas, and the U.S. Copyright Office has recommended federal digital-replica legislation. SAG-AFTRA's current AI materials and digital replica bulletins emphasize clear consent, fair compensation, control over performances, specific intended use descriptions, and compensation for covered performers. Do not treat "publicly available photo" as consent.

## Build the character bible

A useful character bible is compact but operational. Include enough detail for another agent to generate, review, and repair the character without guessing.

### Identity lock

Define the character in layered specificity:

- Name or codename.
- Species/body type/age range, avoiding stigmatizing or overdetermined language.
- Role and personality in one or two sentences.
- Silhouette: the outline that should still read when blacked out.
- Shape language: dominant shapes and the emotional read they support. The Walt Disney Family Museum teaches shape language and silhouette as core character design fundamentals; treat this as a design vocabulary, not a deterministic psychology.
- Face/head anchors: head shape, eye spacing, brow shape, nose/mouth proportion, jaw/chin, ears, facial hair, scars, freckles, markings.
- Body anchors: height impression, posture, shoulder/hip proportion, limb length, gait or default stance.
- Color anchors: skin/fur/material palette, hair color, eye color, signature accent color, forbidden colors if brand-critical.
- Signature items: glasses, hat, pendant, tool, backpack, mascot logo, prosthetic, mobility device, weapon, prop, or UI accessory.
- Negative identity: what the character is not, especially common model confusions.

### Continuity tolerances

State tolerances explicitly:

- **Locked**: must remain constant unless user approves a redesign.
- **Flexible**: can vary by scene or emotion.
- **Story-changing**: can vary only when the narrative calls for it, such as aging, injury, disguise, weathering, or campaign-season wardrobe.

Example tolerance table:

| Element | Continuity rule |
|---|---|
| Hair | Locked: short silver bob with blunt bangs; no long hair, ponytail, or brown hair. |
| Jacket | Flexible: teal bomber can be open, zipped, wet, or windblown; same cut and color family. |
| Tool belt | Locked in work scenes; absent only in formal-event variant. |
| Age | Locked: reads late 30s. Do not make childlike or elderly unless user requests a time jump. |
| Facial scar | Locked: small diagonal scar on left eyebrow; verify screen-left vs character-left in review. |

### Model-sheet substitutes for AI

In traditional animation, turnarounds, expression sheets, pose sheets, color sheets, and prop sheets keep artists on-model. For AI production, create an equivalent reference pack:

- Neutral full-body front, 3/4, side, and back views when possible.
- Neutral close-up portrait.
- Expression range: neutral, smile, anger, fear, surprise, sadness, concentration, brand-specific emotion.
- Pose/action range: default stance, walk/run, seated, reaching, holding signature prop, hero pose, small gesture.
- Costume sheet: default outfit plus approved variants.
- Hair/makeup/grooming sheet: front/side/back notes, color, texture, styling, facial hair, prosthetics.
- Prop sheet: scale, shape, material, which hand/side it appears on, and how it opens/closes or transforms.
- Palette chips and material descriptors.
- "Do not generate" sheet for frequent wrong variants.

For avatar or rigged animation, add pivot points, articulation limits, mouth shapes/visemes, blink style, idle posture, and any features that must deform consistently.

## Reference strategy

Choose the lightest reference method that can meet the continuity target:

- **Text only**: acceptable for archetypes, loose mascots, and early concept exploration. Expect drift; batch-generate and curate.
- **Single reference image**: useful for style and broad identity, but can overfit pose, lighting, facial angle, or outfit.
- **Multi-reference pack**: stronger for recurring characters; include multiple views, expressions, and the default costume.
- **Image-to-image or masked edit**: useful for preserving composition or repairing a drifted element; avoid accidentally freezing unwanted artifacts.
- **Personalization/fine-tuning/identity adapter**: use when repeated exactness is worth setup cost and rights are clear. Document training/reference provenance and limitations.
- **Rigged/vector character**: best when the project requires deterministic reuse, controlled expression, or lots of episodes.

Documented AI research supports this tradeoff: DreamBooth-style personalization fine-tunes from a few subject images to synthesize the subject in new contexts, while newer consistency research such as StoryDiffusion and "The Chosen One" addresses multi-image storytelling consistency. These are technical approaches, not universal guarantees; availability depends on provider/runtime and may change.

## Prompt planning for continuity

Write prompts as a continuity bundle:

1. **Character anchor paragraph**: invariant identity and silhouette.
2. **Scene paragraph**: action, environment, camera, emotion.
3. **Continuity paragraph**: costume state, prop side, story day, prior shot link.
4. **Style paragraph**: visual medium, line/texture, lens/render style, brand palette.
5. **Negative/avoid paragraph**: likely drifts, forbidden outfit/age/body changes, wrong accessories.

Keep the anchor wording stable across shots unless you intentionally revise the design. Move scene-specific changes into the scene paragraph so the model does not reinterpret the identity.

### Provider-independent prompt skeleton

Use this as a planning scaffold, not a mandatory formula:

```text
Character anchor: [name/codename], [age/species/body read], [silhouette], [face/head anchors], [body/posture anchors], [signature colors], [signature item]. Preserve these identity anchors across the series.

Scene: [shot number], [action], [environment], [camera/framing], [emotion/performance], [lighting/time].

Continuity: Story day [x], follows [prior shot/panel]. Outfit state: [exact costume]. Hair/makeup/props: [exact state and side]. Required changes from prior shot: [only the intended changes].

Style: [medium/style], [line/render/texture], [palette], [level of realism], [brand or comic rules].

Avoid: changing age, face shape, body proportions, skin/fur tone, hair length/color, signature accessory, costume cut, prop side; avoid extra logos, extra limbs/fingers, mismatched scar side, unapproved makeup.
```

## Multi-shot and serial continuity

Create a continuity ledger before producing the batch. Do not rely on memory.

Track per shot/panel:

- shot ID and output filename;
- story day/time and location;
- character state entering/exiting shot;
- costume/hair/makeup/prop state;
- emotional beat and pose;
- camera/view angle;
- source references used;
- model/provider/settings/seed when available;
- approved take and rejected drift notes;
- repair instructions.

Borrow the discipline of script supervision: professional script supervisors track story chronology, action, dialogue, wardrobe, props, hair/makeup, eyelines, camera details, and continuity changes. For generated media, the agent becomes the continuity department by logging visual state before the next generation.

### Continuity tiers

Use the strictest tier that the deliverable needs:

- **Tier 1: Recognizable concept** for mood boards and early ideation. Review silhouette, palette, role.
- **Tier 2: Series character** for comics/social/ad variants. Review face, body, outfit, props, style, expression range.
- **Tier 3: Identity-critical** for avatars, spokespeople, licensed mascots, real-person likeness, or paid brand campaigns. Require consent/provenance, reference pack, controlled generation/editing, stricter QA, and human approval.
- **Tier 4: Deterministic production asset** for long serials, animation rigs, games, and repeated brand use. Prefer a rig/model sheet/vector asset or approved canonical renders rather than re-inventing the character every prompt.

## Designing expression and pose ranges

Do not only define a neutral portrait. Characters drift when the first approved image is asked to do a new emotion or action.

For each major character, specify:

- default posture and gesture vocabulary;
- high/low emotional intensity;
- expressions that are on-character and expressions to avoid;
- mouth/eye/brow changes for each expression;
- asymmetries, such as a one-sided smirk or raised left brow;
- performance limits, such as "never manic," "controlled warmth," or "bouncy childlike energy";
- action limits, such as agility, limp, assistive device use, fighting style, or comedic clumsiness.

When designing characters with disabilities, assistive technology, gender expression, race/ethnicity, religion, body size, age, or other identity markers, avoid making the marker the whole character. Use respectful, specific, user-approved descriptors. GLAAD's media guide notes there is no single way to describe LGBTQ people and recommends asking people how they describe themselves; UN guidance calls for accurate and balanced disability portrayal as part of everyday life. For avatar design, recent HCI research highlights appearance, body dynamics, assistive technology, peripherals, and customization control as disability-representation dimensions.

## Costume, hair, makeup, and props

Costume and grooming are continuity infrastructure:

- Name every garment and layer: "cropped teal bomber jacket with ribbed cuffs," not "cool jacket."
- Record closures, sleeve length, collar shape, hem, fabric, wear/damage, and logo placement.
- Define how fabric moves in action: stiff denim, reflective nylon, soft knit, armored plates.
- Specify hair length, part, texture, volume, facial hair, roots, accessories, and wet/wind variants.
- Specify makeup placement, intensity, color, injuries, dirt, sweat, tattoos, scars, nail color, and which side of the body.
- Record prop scale relative to the character, material, grip, wear, screen side, and story state.

Use "stateful" notes for story changes:

```text
Story day 2, shots 08-12: left sleeve torn at cuff after climbing fence; cheek has small soot mark under right eye; backpack strap broken and tied with red cord. Carry these changes until cleanup scene 13.
```

## Age, identity, and likeness rights

Use conservative rules for rights-sensitive characters:

- Do not generate a recognizable living person, employee, customer, influencer, performer, child, or private individual without documented permission and intended-use limits.
- Do not disguise a real person by saying "inspired by" while keeping distinctive face, body, voice, name, or signature styling.
- For minors, require parent/guardian consent and avoid sexualized, humiliating, exploitative, or age-shifted contexts.
- For deceased people, check estate/publicity rights and cultural sensitivity; do not assume public domain.
- For public figures, distinguish commentary/parody/editorial from endorsement, advertising, impersonation, and commercial character reuse.
- Keep consent records out of prompts unless needed; do not expose private identity data to providers unnecessarily.
- When exact identity is not legally or ethically cleared, design an original composite: change face geometry, proportions, styling, name, biography, and signature markers enough that it is not a recognizable substitute.

As a production heuristic, use a "three-distance" test before generating commercial media: does the character remain non-identifying at thumbnail silhouette, portrait crop, and written description? If any distance points to a real person or protected character, escalate for rights review.

## Iteration and repair workflow

Use a controlled loop:

1. **Generate exploration batch** with broad but bounded identity anchors.
2. **Select a canonical take** based on silhouette, face, body, palette, and rights safety.
3. **Extract the bible** from the canonical take: do not leave the design implicit.
4. **Generate reference views** before story scenes.
5. **Run a continuity batch** across expected emotions and poses.
6. **Classify drift**: identity, style, costume, prop, pose, anatomy, age, rights, or story-state error.
7. **Repair using the narrowest tool**: prompt revision, reference change, mask edit, image-to-image, reroll with seed, model switch, or rigged asset.
8. **Update ledger** with approved outputs and known failure modes.

When repairing, change one variable at a time when practical. If a prompt adds "same character" but also changes lighting, costume, lens, and pose, you will not know what caused improvement or drift.

### Common failures and repairs

| Failure | Likely cause | Repair |
|---|---|---|
| Same outfit but different face | Costume over-specified, face under-specified | Add face/head anchors and use portrait reference or personalization. |
| Face stays, body/proportions drift | Portrait-only references | Add full-body references and body anchor paragraph. |
| Hair changes every shot | Hair described as mood adjective | Specify cut, length, part, texture, volume, color, accessories. |
| Scar/tattoo flips sides | Mirroring or screen-side ambiguity | State character-left/character-right and verify in QA. |
| Prop appears/disappears | Prop treated as decoration | Add prop to locked invariants and shot ledger. |
| Childlike or aged drift | Age cue weak or style pushes proportions | Lock age read, adult/child proportions, facial maturity cues. |
| Style consistency but identity drift | Style prompt too dominant | Separate style from identity; reduce artist/style references that override character anchors. |
| Exact likeness risk | Reference resembles real person/IP | Redesign anchors, remove distinctive markers, or obtain clearance. |

## QA checklist

Review each output at three scales: thumbnail, normal view, and zoomed details.

Pass only if:

- silhouette and shape language still read as the same character;
- face/head anchors match the bible;
- body proportions and posture are within tolerance;
- skin/fur/material, hair, and eye colors match;
- costume state matches story day and shot ledger;
- props appear on the correct side and scale;
- expression and pose are in-range for the character;
- style matches the approved visual system without overriding identity;
- anatomy artifacts do not compromise the character;
- no unapproved logos, IP, celebrity likeness, or private-person resemblance appears;
- sensitive identity markers are respectful and relevant rather than stereotyped;
- files, prompts, references, settings, and repair notes are recorded for handoff.

For multi-shot video, also check frame-to-frame and shot-to-shot continuity: face morphology, costume, hands, hair motion, accessory position, eyeline, screen direction, and story-state changes.

## Handoff package

When handing to another agent or tool, provide:

- character bible;
- approved reference images or canonical renders with filenames;
- prompt anchor paragraph and negative drift list;
- style guide excerpt;
- continuity ledger;
- rights/consent status and limits;
- shot list with per-shot state;
- QA checklist and unresolved risks;
- repair notes from rejected generations.

Never hand off only a final image and "make this same character." That loses the reasoning needed to preserve continuity.

## Example: original product mascot for serialized ads

Production intent: create a provider-independent mascot that can appear in six short social ads for a privacy app.

Continuity plan:

```text
Character bible excerpt:
Codename: Mica.
Role: helpful privacy-firefly mascot, curious and calm rather than frantic.
Silhouette: tiny rounded body, oversized translucent wings shaped like two vertical leaves, single antenna curl, small satchel.
Shape language: mostly circles and soft ovals for friendliness; one small square satchel for reliability.
Locked: warm amber glow core, two leaf wings, one curl antenna, navy satchel with no logo, tiny mitten hands, reads non-human.
Flexible: glow intensity, wing blur, facial expression, flight pose.
Forbidden: humanoid child body, realistic insect anatomy, stinger, branded lock icon, extra wings, scary mandibles.
Rights: original fictional mascot; no real-person likeness.
```

Example prompt for shot 03:

```text
Character anchor: Mica, an original non-human privacy-firefly mascot with a tiny rounded amber-glowing body, two oversized translucent leaf-shaped wings, one curled antenna, tiny mitten hands, and a small navy square satchel. Preserve the soft oval silhouette, warm amber glow core, two wings only, one antenna curl, and satchel across the series.

Scene: Shot 03, Mica hovers beside a floating phone screen and gently pulls a translucent privacy curtain across it. Three-quarter view, medium close-up, friendly concentration, soft evening light.

Continuity: Story day 1. Outfit/props unchanged from approved reference: navy satchel across body, no logo, satchel on character's right hip. Wings slightly motion-blurred but still leaf-shaped.

Style: clean 3D clay-like mascot, soft gradients, rounded forms, privacy-app palette of amber, navy, and mist blue, polished social ad look.

Avoid: realistic insect horror, humanoid child, extra arms, extra wings, stinger, lock logo, changing satchel color, green glow, aggressive expression.
```

Why it is structured this way: the non-human identity and locked silhouette prevent the model from turning the mascot into either a child or a realistic insect; the continuity paragraph keeps the satchel and wing state stable across ads.

Expected result: a warm, readable mascot with stable body, wings, antenna, satchel, and palette.

Likely failure modes: extra wings, missing satchel, childlike humanoid face, generic cybersecurity lock icon. Repair by strengthening the locked invariants and using the approved reference image.

## Example: multi-panel comic character with story-state changes

Production intent: preserve a detective character over an eight-panel noir comic while allowing rain damage and emotional escalation.

Continuity ledger excerpt:

```text
Character: Detective Vale
Locked identity: angular long face, tired narrow eyes, short black hair combed back, tan skin, tall lean frame, slightly hunched posture, camel trench coat, red thread bracelet on character-left wrist.
Flexible: coat open/closed, wetness, facial expression, cigarette absent by default.
Panel 01: dry coat, neutral suspicion, alley entrance.
Panel 04: rain begins; hair damp but still combed back; coat shoulders darkened by water.
Panel 06: right cheek scratched; red bracelet still visible on character-left wrist.
Panel 08: coat soaked; scratch remains; no new injuries.
```

Example prompt for panel 06:

```text
Character anchor: Detective Vale, original noir detective, tall lean frame with a slight hunch, angular long face, tired narrow eyes, short black hair combed back, tan skin, camel trench coat, red thread bracelet on character-left wrist. Preserve face shape, tired eyes, lean posture, hair length, coat color, and bracelet.

Scene: Comic panel 06, Vale turns sharply toward an unseen sound in the rain, one hand braced against a brick wall, close three-quarter crop, tense suspicion.

Continuity: Story night 1 after panel 04. Rain has darkened the coat shoulders and dampened the combed-back hair; a small fresh scratch crosses Vale's right cheek. Red thread bracelet remains on character-left wrist. No cigarette.

Style: high-contrast noir comic ink, limited camel/red/blue-gray palette, crisp panel art, dramatic rain streaks.

Avoid: changing to a fedora, adding beard, changing bracelet side, making hair long or curly, changing trench coat to black leather, adding extra scars, making the character older than late 40s.
```

Why it is structured this way: the story-state changes are explicit, so the model can add rain and scratch without treating them as a redesign.

Expected result: same detective, now wetter and scratched, not a new noir archetype.

Likely failure modes: fedora appears from noir stereotype, bracelet flips sides, coat turns black. Repair with masked edit or stronger negative prompt.

## Sources consulted

- Walt Disney Family Museum, "Character Design" and "Shape Language" worksheet: shape language, silhouette, and personality traits as character design fundamentals. Verified 2026-07-10. https://www.waltdisney.org/education/field-trips/character-design and https://www.waltdisney.org/sites/default/files/2020-04/T%26T_ShapeLang_v9.pdf
- ScreenSkills, "Script supervisor skills": continuity breakdowns, story days, costume, makeup, props, action, eyelines, camera notes. Verified 2026-07-10. https://www.screenskills.com/skills-checklists/scripted-film-and-tv/script-supervisor-department/script-supervisor-skills/
- U.S. Copyright Office, "Copyright and Artificial Intelligence" reports: Part 1 digital replicas, Part 2 copyrightability, Part 3 pre-publication training report status. Verified 2026-07-10. https://www.copyright.gov/ai/
- SAG-AFTRA, "Artificial Intelligence" member resource page and "Digital Replicas" contract bulletin: clear consent, fair compensation, control over performances, performer digital replica categories, informed consent, specific intended use, and compensation in covered contexts. Verified 2026-07-10. https://www.sagaftra.org/contracts-industry-resources/member-resources/artificial-intelligence and https://www.sagaftra.org/sites/default/files/sa_documents/DigitalReplicas.pdf
- Davis Wright Tremaine, "Washington Becomes the Latest State to Expand Right of Publicity Protections to Digital Replicas": 2026 state-law example supporting the patchwork/publicity-rights caution. Verified 2026-07-10. https://www.dwt.com/insights/2026/06/washington-state-right-of-publicity-ai-replicas
- Ruiz et al., "DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation," CVPR 2023/arXiv: few-image personalization and subject preservation in new contexts. Verified 2026-07-10. https://arxiv.org/abs/2208.12242
- Zhou et al., "StoryDiffusion: Consistent Self-Attention for Long-Range Image and Video Generation," arXiv 2024: training-free consistency across generated storytelling images and video transitions. Verified 2026-07-10. https://arxiv.org/html/2405.01434v1
- Avrahami et al., "The Chosen One: Consistent Characters in Text-to-Image Diffusion Models," SIGGRAPH 2024/arXiv: consistency remains a known challenge; iterative identity extraction from prompt-generated clusters. Verified 2026-07-10. https://arxiv.org/html/2311.10093v4
- GLAAD Media Reference Guide, 11th edition: fair and accurate LGBTQ representation, self-description and pronoun practice. Verified 2026-07-10. https://glaad.org/reference/
- United Nations Enable, "Disability and the Media": accurate and balanced portrayal of disability as part of everyday life. Verified 2026-07-10. https://www.un.org/development/desa/disabilities/resources/disability-and-the-media.html
- Zhang et al., "Inclusive Avatar Guidelines for People with Disabilities," arXiv 2025: disability expression dimensions for avatars. Verified 2026-07-10. https://arxiv.org/abs/2502.09811
