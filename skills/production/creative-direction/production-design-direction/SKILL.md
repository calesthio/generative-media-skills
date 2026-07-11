---
name: production-design-direction
description: Provider-independent production design direction for AI-generated media. Use when translating narrative, brand, advertising, product, social, film, or worldbuilding intent into sets, locations, props, color and material palettes, era research, graphic and environmental design, continuity bibles, image/video prompt planning, reference strategy, production constraints, iteration notes, handoff specs, and QA.
---

# Production design direction for generated media

Use this skill to act as a production designer for generated images, videos, campaigns, and mixed-media sequences. Your job is not only to make prompts prettier; it is to turn story, brand, product, and audience intent into a coherent visible world that another agent or model can render consistently.

Production design direction covers:

- spaces: sets, locations, geography, architecture, room logic, negative space;
- objects: hero props, set dressing, packaging, signage, furniture, tools, wear, evidence of use;
- visual systems: color, value, material, texture, scale, pattern, typography, graphics, UI-in-environment;
- world rules: era, culture, class, climate, technology level, maintenance, history, constraints;
- continuity: what must repeat, what may evolve, and what must never appear;
- generation planning: reference use, prompt decomposition, shot-by-shot design notes, QA, and repair.

## Ground truth to keep separate

### Documented facts

- Production design starts from the script or brief and visualizes the whole look of a film or screen work; ScreenSkills lists production-designer skills including color theory, architecture/interior-design history, camera/lens/lighting awareness, budgeting, scheduling, and collaboration with art, set decoration, buying, and props roles. Source: [ScreenSkills production designer profile](https://www.screenskills.com/job-profiles/browse/film-and-tv-drama/craft/production-designer-film-and-tv-drama/).
- The set decorator is responsible for furnishings and visible objects on set; art and standby art roles break down scripts, track props, graphics, animals, vehicles, food, drink, and solve on-set design problems. Source: [ScreenSkills production designer profile](https://www.screenskills.com/job-profiles/browse/film-and-tv-drama/craft/production-designer-film-and-tv-drama/).
- Historic design research benefits from primary visual collections and preservation standards. The Library of Congress offers free-to-use/reuse sets including architecture, gardens, and original designs; the National Park Service separates preservation, rehabilitation, restoration, and reconstruction according to significance, condition, documentation, and interpretive goals. Sources: [Library of Congress Free to Use and Reuse](https://www.loc.gov/free-to-use/) and [NPS Treatment Standards](https://www.nps.gov/orgs/1739/secretary-standards-treatment-historic-properties.htm).
- Accessibility affects production design when text, UI, labels, wayfinding, charts, product callouts, or social overlays are part of the image. WCAG 2.2 requires at least 4.5:1 contrast for normal text and 3:1 for large text; WCAG 2.1 non-text contrast calls for meaningful visual cues to reach 3:1 against adjacent colors. Sources: [W3C contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) and [W3C non-text contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html).
- Advertising and brand constraints are production-design constraints. FTC endorsement guidance says endorsements must be honest and not misleading, and USPTO trademark guidance flags likelihood of confusion when similar marks and related goods/services may cause consumers to believe goods or services come from the same source. Sources, verified 2026-07-10: [FTC advertisement endorsements](https://www.ftc.gov/news-events/topics/truth-advertising/advertisement-endorsements) and [USPTO likelihood of confusion](https://www.uspto.gov/trademarks/search/likelihood-confusion).
- AI copyright and likeness rules remain volatile. The U.S. Copyright Office AI page, verified 2026-07-10, lists Part 1 on digital replicas, Part 2 on copyrightability, and Part 3 on generative AI training. Treat copyrightability, digital replica, union, platform, and jurisdictional claims as legal-review triggers, not as design assumptions. Source: [U.S. Copyright Office: Copyright and Artificial Intelligence](https://www.copyright.gov/ai/).

### Empirical observations to verify on the current model

These are common behaviors in generated image/video workflows, not universal facts:

- Models often render one strong hero object better than many equally important props. Prioritize the hero prop and reduce background prop count when the scene is failing.
- Vague era labels such as "retro," "futuristic," or "luxury" tend to collapse into clichés. Era, class, material, and maintenance details usually control the image better than style labels alone.
- Graphic design inside generated footage is error-prone: readable text, exact logos, charts, package labels, and UI should be composited or post-produced when fidelity matters.
- Video models may drift object placement, material, and color across shots. Use continuity anchors and repeat them in every shot plan.
- Over-specified references can cause imitation. Use references as separated evidence for materials, silhouette, camera mood, or era, rather than asking for a whole image's look.

### Production heuristics

- Design from story pressure. Every visible choice should either reveal character, sell product truth, clarify function, establish world rules, or guide the viewer's eye.
- Treat production design as a system, not a moodboard. A palette without material rules, prop logic, and continuity rules will not survive multi-shot generation.
- Prefer "lived-in specificity" over decoration. A mug ring, scuffed floor edge, taped label, worn handle, or mismatched replacement part can say more than a generic beautiful room.
- Make constraints explicit. If the brand, era, region, legal risk, accessibility requirement, or platform crop changes what can appear, include it in the design bible and prompt plan.
- Separate desire from renderability. Keep the ideal art direction, then create a model-safe prompt version that prioritizes the few details the generator must preserve.

## First pass: turn the brief into a design problem

Before describing any set, answer these questions:

1. What must the viewer understand in the first three seconds?
2. What is the emotional temperature: awe, relief, danger, intimacy, competence, comic absurdity, status, nostalgia, proof?
3. Who owns the world: brand, character, community, institution, product, antagonist, environment?
4. What is the production format: hero film, paid social ad, UGC-style spot, product page loop, explainer, trailer, still key art, pitch deck, or series bible?
5. What must be real or accurate: product geometry, logo, claims, historical setting, cultural signifiers, safety conditions, accessibility, regulatory language?
6. What should be avoided: competitor lookalikes, protected marks, stereotypes, unsafe use, inaccurate era details, platform-unfriendly clutter, fake endorsements?

Write a one-sentence design thesis:

Example: "A premium-but-practical kitchen world where a calm morning routine is interrupted by visible micro-messes that the product resolves, using warm matte ceramics, honest daylight, and one repeated cobalt accent to link app, packaging, and hero prop."

## Build the production design bible

For any multi-asset or multi-shot job, create a design bible. Keep it concise enough to use, but specific enough to prevent drift.

### 1. World premise

Define the visible rules of the world:

- time: exact year/decade or invented era; avoid generic era words without evidence;
- place: region, climate, architecture, density, socioeconomic context, interior/exterior logic;
- institutions: household, office, lab, marketplace, school, spaceship, boutique, civic space;
- technology level: what exists, what is rare, what looks repaired, what looks new;
- maintenance: pristine, neglected, improvised, sterile, repaired, weathered, premium-careful;
- realism level: documentary, commercial-polished, stylized, speculative, theatrical, graphic.

### 2. Set and location direction

Specify the set as a functional environment, not just a backdrop:

- room or location type and why the scene happens there;
- camera-visible zones: foreground, action plane, background, depth frames;
- blocking affordances: where people or products move, sit, enter, discover, reveal;
- architectural language: ceiling height, openings, thresholds, surfaces, wall treatment;
- scale clues: human-scale objects, furniture, handles, signage, floor grid, windows;
- unwanted defaults: empty white cyclorama, luxury hotel lobby, generic startup office, random neon, impossible room geometry.

For generated video, assign a continuity anchor to each set: a doorway shape, window grid, dominant material, hero wall color, floor pattern, or repeated object that should remain stable across shots.

### 3. Props and set dressing

Break props into four classes:

- Hero prop: the product or story object the viewer must recognize.
- Action props: handled, moved, opened, spilled, broken, scanned, measured, repaired.
- Evidence props: objects that explain backstory, time, identity, work, status, or stakes.
- Texture props: minor dressing that adds lived-in specificity but may be simplified.

For each important prop, define:

- silhouette and scale;
- material and finish;
- color/value relationship to the background;
- condition: new, worn, repaired, dusty, heirloom, prototype, mass-produced;
- interaction: how hands, light, motion, water, dust, or packaging affect it;
- continuity: must stay identical, may vary, or should not reappear.

Avoid prop overload. If five props compete for narrative importance, choose one hero, two supporting props, and move the rest into background texture.

### 4. Color, value, and material system

Color direction should describe hue, value, chroma/saturation, and material behavior. The Munsell tradition separates color by hue, value, and chroma; use that separation as practical vocabulary even when working in hex, LAB, HSL, or plain language. Source: [RIT Munsell Color Science Laboratory educational resources](https://www.rit.edu/science/munsell-color-science-lab-educational-resources).

Define:

- base palette: dominant environmental colors;
- accent palette: one or two colors used for attention or brand memory;
- forbidden colors: competitor colors, off-brand hues, mood-breaking colors;
- value plan: where dark, mid, and light masses sit in the frame;
- chroma plan: what is saturated and what is muted;
- material palette: wood, brushed metal, glossy plastic, ceramic, paper, concrete, textile, glass, organic matter;
- aging: patina, scratches, oxidization, sun-fading, fingerprints, dust, water spots.

Use color as a story control, not decoration. A restrained environment can make a product color feel deliberate; a high-chroma world can make a neutral product feel calm or premium.

### 5. Graphic and environmental design

Plan all visible designed information:

- logos and marks;
- package fronts, labels, seals, warning stickers;
- UI screens, dashboards, maps, charts, QR-like elements;
- wayfinding, posters, menus, certificates, license plates, newspapers;
- social captions, lower thirds, callouts, price cards.

If exact text must be legible or legally compliant, mark it for post/compositing rather than relying on image/video generation. When text is generated directly, specify it as "unreadable abstract label blocks" or "blank label area for later compositing" unless readability is non-critical.

Brand/legal guardrails:

- Do not create confusingly similar marks for real competitors or imply affiliation.
- Do not show fake seals, awards, reviews, or endorsements.
- Keep health, finance, safety, sustainability, and performance claims out of background graphics unless verified by the user.
- For paid social, reserve readable disclosure space when endorsements, sponsorships, or material connections are part of the concept.

### 6. Era, culture, and worldbuilding research

Use references as evidence, not as a copying target. For historical or culturally specific work:

- collect references from primary or institutional sources where possible;
- separate architecture, interior objects, clothing-adjacent environment, typography, materials, and public signage;
- record the date range and geography for each reference;
- avoid mixing decades only because they share a vibe;
- identify what can be stylized and what must stay accurate;
- flag living cultures, sacred items, uniforms, badges, political signs, and stereotypes for extra review.

For speculative worlds, write rules equivalent to historical constraints:

- What materials are abundant or scarce?
- What technology has matured and what remains improvised?
- What does wealth look like? What does neglect look like?
- What are everyday objects made from?
- What symbols, signage, or civic systems organize the world?

### 7. Prompt planning

Convert the design bible into prompts by layer:

- Scene layer: place, architecture, time of day, weather, mood.
- Set dressing layer: major surfaces, furniture, visible props, background texture.
- Hero layer: product/character/object with scale, silhouette, color, material.
- Graphic layer: blank label areas, compositing zones, readable-safe overlays.
- Camera/light layer: lens feel, angle, depth, lighting quality, reflections.
- Continuity layer: repeated anchors, forbidden changes, stable colors/materials.
- Negative constraints: style clichés, wrong eras, competitor cues, clutter, illegible text if relevant.

For video, make each shot prompt answer:

- what must stay stable from the previous shot;
- what changes through motion;
- which object is allowed to transform;
- where the viewer should look;
- whether the shot is an establishing, reveal, detail, action, proof, or payoff shot.

## Constraint profiles by deliverable

### Paid social ad

Prioritize fast comprehension, safe claims, platform crop, disclosure space, and brand distinctness. Keep set design readable on a phone: one dominant space, one hero product, one color memory, few props. Avoid fine-print graphics that will fail at mobile size.

### Product film or product-page loop

Prioritize product geometry, material truth, scale, and repeatable hero angles. Keep the environment supportive and lower-detail than the product. If product labels/logos must be exact, plan for compositing or image editing rather than pure generation.

### Film trailer, teaser, or narrative scene

Prioritize world rules, character backstory, symbolic props, and continuity across shots. Let the design carry subtext: who has power, who is trapped, what changed before the scene, what is about to break.

### Explainer or educational visual

Prioritize clarity, contrast, labels, readable spatial metaphors, and progressive disclosure. Treat diagrams, signs, and UI as designed environments, not decoration. Check contrast when important information is carried by text, shapes, or color.

### UGC-style or documentary-style spot

Design should feel discovered rather than art-directed, but it still needs rules. Use plausible domestic or workplace clutter, imperfect light, non-matching objects, and believable camera-access spaces. Avoid making the "casual" world look accidentally unsafe, unhygienic, or off-brand.

### Luxury, fashion, or beauty content

Use restraint. Fewer materials, stronger value control, precise reflections, and intentional negative space usually read more premium than adding gold, marble, smoke, or chandeliers. Define what luxury means for the specific brand: heritage, precision, sensuality, scarcity, ritual, sustainability, or performance.

## Iteration workflow

When outputs miss the design intent, diagnose by layer:

1. Story miss: the space does not communicate the intended emotion or status.
2. Set miss: architecture, geography, or room logic is wrong.
3. Prop miss: hero object is incorrect, lost, or competing with background props.
4. Palette miss: wrong value/chroma relationship or off-brand color intrusion.
5. Material miss: surfaces look plastic, glossy, dirty, sterile, or fake in the wrong way.
6. Graphic miss: text, logos, labels, UI, or claims are unreadable or risky.
7. Continuity miss: anchors drift between shots.
8. Rights/safety miss: copied references, confusing marks, protected likeness, unsafe use, or misleading claims.

Repair with the smallest effective change:

- simplify the set before changing the whole style;
- isolate the hero prop;
- replace abstract adjectives with physical details;
- repeat continuity anchors;
- move exact text/logos to post;
- remove a risky reference rather than trying to disguise it;
- create a style-frame test before generating a full sequence.

## Handoff format

For another generation or composition agent, hand off:

- design thesis;
- audience, platform, aspect ratio, duration, and delivery constraints;
- visual bible: set/location, props, palette, materials, graphics, era/world rules;
- reference ledger: source, date, what it informs, rights/usage status, what not to copy;
- shot or asset plan with continuity anchors;
- prompt pack with positive and negative constraints;
- post-production notes for exact logos, text, disclosures, UI, charts, and labels;
- QA checklist and known risks.

Do not hand off only mood adjectives. Include concrete surfaces, object classes, color/value relationships, and continuity rules.

## QA checklist

Review every production-design output for:

- brief fit: visible world supports the story, product, or brand promise;
- hierarchy: viewer can identify the hero subject quickly;
- set logic: space could plausibly exist or intentionally obeys invented rules;
- prop logic: important objects have purpose, scale, material, and continuity;
- palette: colors serve story/brand and maintain value readability;
- material truth: surfaces react plausibly to light and use;
- graphics: exact text/logos/claims are either correct or reserved for post;
- accessibility: important text and visual cues have adequate contrast;
- historical/cultural care: no lazy era mixing, stereotypes, or unsupported symbols;
- rights/safety: no confusing marks, copied reference designs, unapproved likenesses, fake endorsements, or unsafe product use;
- multi-shot continuity: anchors, product design, set layout, colors, and props remain stable unless intentionally changed.

## Complete example: SaaS launch ad production-design plan

User request: "Make a 20-second vertical launch ad for a privacy-focused team-notes app. It should feel warm and human, not cyberpunk."

Design thesis: A quiet team workspace where privacy is shown through trust, soft partitions, and controlled reveal, not locks, hacker imagery, or blue neon.

Documented constraints:

- Paid social: reserve upper/lower safe zones for captions and disclosure/call-to-action.
- Avoid security clichés that suggest fear or surveillance.
- App UI text and brand mark should be composited if exact.

Set/location:

- Small creative studio at 9:00 a.m., warm daylight, plaster walls, oak worktable, linen pinboard, translucent room divider.
- No generic glass startup office, no server room, no hooded figures, no matrix code.
- Continuity anchor: curved frosted divider behind the hero laptop, small amber desk lamp, matte sage wall.

Props:

- Hero: laptop with blank app screen area for later UI composite; matte charcoal body; visible but not exact logo.
- Action: handwritten meeting card turned face-down, ceramic mug, pencil, closed notebook.
- Evidence: small team photo with faces out of focus, color-coded sticky tabs with no readable text.
- Texture: cable clips, plant shadow, paper grain.

Palette/materials:

- Base: warm off-white plaster, pale oak, muted sage.
- Accent: one amber privacy indicator and one deep ink-blue UI placeholder.
- Chroma: low-to-medium saturation; no electric blue or neon green.
- Materials: matte, tactile, low-glare; privacy feels physical and calm.

Shot prompt plan:

1. Establishing: vertical frame, warm studio table, frosted divider, laptop closed, morning light; stable amber lamp and sage wall.
2. Detail: hand turns meeting card face-down beside laptop; shallow depth of field; product privacy metaphor without text.
3. Hero: laptop opens to blank compositing-safe screen area; UI glow is soft ink-blue, not cyberpunk; no readable generated text.
4. Payoff: team gathers softly out of focus behind divider; laptop sharp, amber indicator visible; caption space preserved.

QA focus:

- Does the ad read "privacy with people" before it reads "security tech"?
- Is exact UI/logotype left for compositing?
- Are props intentional rather than random desk clutter?
- Does the vertical crop preserve the hero laptop and CTA space?

## Complete example: historical short-form scene direction

User request: "Create a 10-second image-to-video scene of a 1930s railway waiting room, bittersweet, no people, just the space."

Research plan:

- Use primary visual references for railway architecture, benches, lamps, signage, luggage, and poster styles from the target country/region and decade.
- Record exact source dates. Do not mix 1950s fluorescent lighting, modern safety signage, or contemporary luggage with 1930s design unless the brief changes.
- If using public-domain or institutional images as reference, note whether they inform architecture, object type, or material patina.

Design thesis: An emptied public room that still carries the emotional residue of departures: durable civic materials, worn touchpoints, soft winter light, and one abandoned paper ticket as the narrative prop.

Set/location:

- Regional railway waiting room, high ceiling, timber benches, tiled lower wall, plaster upper wall, brass clock, frosted window light.
- No modern LED signs, plastic chairs, stainless turnstiles, digital displays, or contemporary posters.
- Continuity anchor: brass clock above center doorway, checker tile border, dark green bench paint worn at edges.

Props:

- Hero evidence prop: single paper ticket on bench, visible as paper shape but not relying on readable text.
- Support props: period-appropriate suitcase near bench, enamel station sign with unreadable or post-produced text.
- Texture: scuffed tile, water-darkened threshold, soot-softened ceiling edge.

Palette/materials:

- Base: muted green paint, cream plaster, dark walnut, dull brass, charcoal soot.
- Accent: faded red poster in background, kept soft.
- Light: cold window light with warm brass reflection; bittersweet without melodrama.

Video prompt:

- "Slow inward dolly through an empty 1930s regional railway waiting room, high plaster ceiling, timber benches painted dark muted green with worn edges, checker tile border, brass clock above center doorway, frosted winter window light, a single paper ticket left on the nearest bench, dull brass and cream plaster, quiet bittersweet atmosphere, no people, no modern signage, no digital displays, no plastic furniture, no readable generated text."

Expected risks:

- Model may add people, modern LED signage, or readable nonsense text.
- Repair by repeating "empty room, no people," moving signage to blank/post-produced areas, and foregrounding physical materials over era adjectives.

## Complete example: product image direction with graphic constraints

User request: "Generate e-commerce hero images for a refillable countertop cleaner bottle. Minimal, sustainable, but not greenwashed."

Design thesis: Practical reuse shown through durable materials and refill ritual, not leaves, fake eco badges, or vague nature symbolism.

Set/location:

- Real kitchen counter corner, soft side light, stone or composite counter, ceramic tile backsplash, enough negative space for product title.
- Avoid forest backgrounds, floating leaves, fake certification seals, excessive green, or luxury spa clichés.

Props:

- Hero: refillable bottle, exact silhouette supplied by product reference; label area blank if exact copy is not provided.
- Action: refill pouch partially visible, measuring cap, damp cotton cloth.
- Evidence: faint water ring, small droplet trail, clean but not sterile counter.

Palette/materials:

- Base: warm white, stone gray, pale clay, clear liquid highlights.
- Accent: restrained brand color on cap or blank label zone.
- Material truth: slightly translucent bottle body, satin pump, paper label texture if label is composited later.

Prompt skeleton:

- "Photoreal e-commerce hero image of a refillable countertop cleaner bottle on a warm stone kitchen counter, soft side daylight, ceramic tile backsplash, clean practical home setting, refill pouch and cotton cloth as secondary props, blank label area for later graphic compositing, restrained warm neutral palette, satin plastic pump, subtle water ring and droplets, premium but practical, no leaves, no fake eco badges, no certification seals, no readable generated text, no competitor packaging cues."

QA focus:

- Does sustainability come from reuse and materials rather than symbolic clichés?
- Is product silhouette correct?
- Are claims, badges, and labels absent unless verified?
- Is there enough negative space for e-commerce layout?

## Source notes

Facts above were grounded in professional or authoritative sources: ScreenSkills for production design/art department roles; Library of Congress and National Park Service for historical visual research and treatment concepts; RIT/X-Rite for hue/value/chroma vocabulary; W3C for contrast; FTC, USPTO, and U.S. Copyright Office for advertising, trademark, and AI-rights risk triggers. Legal and platform-sensitive facts were checked on 2026-07-10 and should be rechecked for live commercial work.
