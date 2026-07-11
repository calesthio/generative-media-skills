---
name: food-beverage-content-production
description: Provider-independent production guidance for AI agents creating or retouching appetizing food and beverage images, recipe videos, restaurant/menu visuals, CPG ads, ecommerce product images, beverage pours, packaging/lifestyle shots, and social food clips, including truthfulness, labeling/claims discipline, styling, prompt translation, platform variants, accessibility, rights, alcohol, and QA.
---

# Food and beverage content production

Use this skill when producing food or beverage visuals for commercial, editorial, ecommerce, social, recipe, menu, packaging, or product-ad contexts. Treat the food as both a sensory subject and a regulated product: make it appetizing, but do not let aesthetics create a false product, false serving, false ingredient, false label, or unsupported claim.

This skill is not legal, nutrition, medical, or regulatory advice. For anything that could become a label claim, health claim, allergen representation, alcohol compliance issue, child-directed ad, marketplace listing, or paid media submission, prepare the creative and flag the approval required from counsel, regulatory, the brand owner, the platform, or the client.

## Operating stance

Separate facts, client-provided claims, and production heuristics.

- Documented fact: information from the client brief, product label, recipe spec, signed asset library, official regulatory source, or platform requirement.
- Client claim: a statement the client wants to communicate. Require substantiation or approval before turning it into copy, packaging text, super, caption, or alt text.
- Production heuristic: a craft technique that improves appetite appeal but must stay truthful to the product.

Core rule: visuals may polish the product; they must not materially change what the customer would believe they are buying, eating, drinking, preparing, receiving, or ordering.

## First-pass intake

Before prompting, generating, retouching, editing, or exporting, collect or infer enough of this checklist to avoid unsafe assumptions:

1. Deliverable type: restaurant menu item, recipe tutorial, packaged product ecommerce, paid social ad, organic social, packaging/lifestyle image, beverage pour, food-service display, marketplace listing, or editorial.
2. Product truth: exact SKU/menu item/recipe name, ingredients, visible inclusions, size, count, weight/volume, package version, current label art, claims allowed, claims banned, geographic market, and any reference photo that must be matched.
3. Risk surface: allergens, nutrition/health claims, "free-from" claims, organic/non-GMO/keto/vegan/gluten-free/healthy claims, alcohol, caffeine, supplements, infant/child audience, minors on screen, raw/undercooked food, medical/diet messaging, pricing, promotions, endorsements, or comparisons.
4. Required variants: aspect ratios, safe zones, language/locales, captions, alt text, marketplace main image versus lifestyle modules, print versus web color, and file naming.
5. Rights/provenance: brand assets, packaging art, fonts, music, locations, recognizable people, identifiable private property, stock assets, AI-generated elements, and allowed usage territories/duration.

If the brief lacks label art, package photos, recipe specs, or allowed claims for a commercial product, pause before producing final commercial assets. You can create mood boards or clearly marked placeholders, but not final factual packaging, nutrition, allergen, or claim copy.

## Claim and compliance discipline

### Advertising truthfulness

Documented fact: FTC advertising guidance states that advertising should be truthful, not misleading, and supported before dissemination for objective claims; health-related product claims need appropriate substantiation. See FTC [Health Products Compliance Guidance](https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance) and FTC [Health Claims](https://www.ftc.gov/business-guidance/advertising-marketing/health-claims). Verified 2026-07-11.

Apply this by default:

- Do not invent "clinically proven," "boosts immunity," "heart healthy," "detox," "low sugar," "high protein," "natural," "zero," "no artificial," "non-GMO," "organic," "gluten-free," "vegan," "sustainable," or "doctor recommended" claims.
- Treat implied claims as claims. A glowing shield icon, before/after body change, lab coat, medical-looking chart, athletic performance scene, or "guilt-free" framing can imply benefits even if the words are absent.
- For comparisons such as "30% less sugar," "more protein than leading brand," or "better for kids," require the exact comparison basis and substantiation.
- For testimonials, influencers, UGC, reviews, and creator-style ads, require material-connection disclosure and typicality review. FTC endorsement guidance is context-dependent; see FTC [Endorsements, Influencers, and Reviews](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews) and [Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers). Verified 2026-07-11.
- For native or editorial-style content, ensure the commercial nature is clear; do not disguise an ad as independent food journalism or a recipe recommendation. See FTC [Native Advertising: A Guide for Businesses](https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses). Verified 2026-07-11.

Escalate for approval when copy, graphics, voiceover, captions, or alt text state or imply a regulated or health-related claim.

### FDA-related food labeling and menu facts

Documented facts for U.S. work, verified 2026-07-11:

- FDA's food labeling guidance summarizes required statements for many packaged foods and recommends manufacturers/importers understand applicable law before distribution: [Food Labeling Guide](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/guidance-industry-food-labeling-guide).
- FDA identifies the major food allergens as milk, eggs, fish, Crustacean shellfish, tree nuts, peanuts, wheat, soybeans, and sesame: [Food Allergies](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/food-allergies).
- FDA menu labeling applies to covered chain restaurants and similar retail food establishments with 20 or more locations under the same name offering substantially the same menu items, with calorie and additional written nutrition-information requirements for standard items: [Menu Labeling Requirements](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/menu-labeling-requirements).
- FDA's "gluten-free" rule uses a less-than-20-ppm threshold for unavoidable gluten in foods bearing the claim: FDA [Questions and Answers on the Gluten-Free Food Labeling Final Rule](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/questions-and-answers-gluten-free-food-labeling-final-rule).
- FDA updated the "healthy" nutrient content claim by final rule; this is a volatile area and must be rechecked before production use: FDA [Use of the "Healthy" Claim on Food Labeling](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/use-healthy-claim-food-labeling).

Production application:

- Never generate Nutrition Facts, Supplement Facts, ingredient lists, allergen "Contains" statements, front-of-pack claims, certifications, net quantity, barcode, manufacturer address, legal disclaimers, or seals from memory.
- If packaging is visible, match the provided current artwork. If exact artwork is unavailable, use generic placeholder packaging with no factual claims or mark the frame as a concept mockup not for publication.
- If an ingredient is visible, make sure it is present in the recipe/product or clearly identified as garnish/serving suggestion when allowed. Do not show nuts, dairy, seafood, alcohol, sesame, wheat, soy, or egg as garnish unless approved.
- If calories, macros, serving sizes, "light," "low," "reduced," "free," "healthy," "gluten-free," "organic," "plant-based," or allergen statements appear, require client/regulatory approval and source values.
- For menu boards and restaurant assets, do not invent calories, prices, location-specific availability, or portion sizes. Confirm the item's standard build.

### Food safety cues

Documented fact: U.S. government food-safety sources publish safe internal temperature and raw-food handling guidance; see USDA FSIS [Safe Minimum Internal Temperature Chart](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart), FoodSafety.gov [Safe Minimum Internal Temperatures](https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures), and FDA [Flour Is a Raw Food](https://www.fda.gov/consumers/consumer-updates/flour-raw-food-and-other-safety-facts). Verified 2026-07-11.

Do not turn food safety into medical advice. For recipe content, avoid unsafe implied behavior:

- Do not show tasting raw dough/batter, raw ground meat, unsafe raw milk claims, or unsafe cross-contamination unless the piece explicitly warns against it.
- If the recipe gives cooking temperature or doneness instructions, use the client recipe or official source and flag for culinary review.
- If visual doneness is stylized, avoid stating that color alone proves safety.

### Alcohol

For beverage alcohol, treat every frame, caption, repost, influencer asset, and product page as potentially regulated advertising.

Documented facts, verified 2026-07-11:

- TTB says alcohol advertisements and retail cartons generally do not require TTB preapproval before broadcast/publication/printing, but TTB can review them for compliance on request: TTB [Alcohol Beverage Advertising](https://www.ttb.gov/what-we-do/program-areas/advertising).
- TTB social media guidance states that advertising rules, including prohibited practices/statements, apply to social media advertising; posts on owned pages and certain reposted/liked third-party content may be considered advertising: TTB [Industry Circular 2024-1](https://www.ttb.gov/public-information/industry-circulars/ttb-industry-circular-2024-1).
- U.S. alcohol industry self-regulatory codes emphasize legal-drinking-age adult audiences and responsible content. See DISCUS [Code of Responsible Practices](https://distilledspirits.org/code-of-responsible-practices/), Beer Institute [Advertising & Marketing Code](https://www.beerinstitute.org/policy-responsibility/responsibility/advertising-marketing-code/), and Wine Institute [Ad Code](https://wineinstitute.org/our-work/responsibility/social/ad-code/).

Alcohol creative guardrails:

- Do not depict minors, youth-coded styling, school/campus settings, cartoonish kid appeal, pregnant people drinking, intoxication, chugging, drinking games, pressure to drink, "liquid courage," therapeutic benefits, sexual/social success due to alcohol, or consumption before/during driving, boating, machinery, sports, or other alertness activities.
- Do not invent ABV, class/type, appellation, vintage, "low calorie," "zero sugar," "gluten-free," origin, age statement, awards, or responsible-drinking disclaimers.
- For cocktail recipes, verify product class, ABV, garnish, glassware, serving size, and whether any "mocktail" or "non-alcoholic" representation is legally and brand-approved.
- Escalate all alcohol paid media, influencer posts, age-gated landing pages, social repost strategy, and marketplace listings to the client's alcohol compliance reviewer.

## Food styling and appetite appeal

Use appetite cues that are truthful to the SKU, recipe, or menu item:

- Color: preserve brand/product color. Warm highlights can make crust, sauce, syrup, cheese, coffee crema, citrus, and grilled surfaces appetizing, but avoid shifting color enough to imply different flavor, freshness, roast level, doneness, or ingredient.
- Texture: emphasize crumb, gloss, char, bubbles, condensation, frost, sauce cling, foam, crisp edges, steam, and pour viscosity. Keep texture consistent with the actual product after normal preparation.
- Composition: design a clear hero hierarchy: product/package/menu item first, appetite cue second, usage context third, claim/copy last.
- Scale: include honest cues such as hand, utensil, plate, can, bottle, bowl, slice count, scoop size, or pack size. Do not make small portions look like family-size servings unless the asset is explicitly illustrative.
- Plating: control mess deliberately. A few crumbs, drips, seeds, herbs, bubbles, or ice beads can sell freshness; random splatter reads careless.
- Freshness: use appropriate garnish only if included, suggested, or clearly optional. Avoid "ingredient theater" that misleads, such as surrounding a naturally flavored product with whole fruit/nuts it barely contains unless legally and brand-approved.
- Beverage: control glass clarity, meniscus, condensation, ice geometry, foam head, crema, bubbles, pour arc, and liquid level. Avoid impossible pours, floating ice, wrong carbonation, cloudy clear drinks, or inconsistent fill across cuts.

Production heuristic: appetite appeal usually comes from specific texture plus believable imperfection, not from maximum saturation or generic gloss.

## Generated image and video prompt translation

When converting a food brief into an AI generation prompt, build the prompt from factual locks plus controlled creative variables.

Prompt components:

1. Product lock: exact product/menu item, required visible ingredients, excluded ingredients, packaging art reference, portion size, number of pieces, serving vessel, preparation state, and any required label/copy.
2. Appetite target: crisp, creamy, airy, juicy, chilled, fizzy, roasted, caramelized, flaky, steamed, velvety, glossy, fresh-cut, charred, fermented, layered, or hand-pulled.
3. Scene: tabletop, kitchen pass, bar, picnic, delivery unboxing, grocery shelf, ecommerce white sweep, restaurant interior, farm/source context, lifestyle moment, or recipe step.
4. Camera and lighting: macro, three-quarter hero, overhead flat lay, hand-held UGC, slow push-in, locked ecommerce, backlit steam, polarised bottle/glass, softbox reflection, hard sunlight, or moody bar practicals.
5. Motion beats for video: pour begins, stream stretches, splash/contact, foam/steam bloom, ingredient drop, pull-apart, drizzle, bite, wipe, pack reveal, label turn, end card.
6. Constraints: no extra ingredients, no malformed hands, no unreadable label text, no invented claims, no warped logo, keep package upright, match color reference, leave safe-zone space, no minors/alcohol, no utensils crossing label.
7. Output variants: aspect ratio, duration, fps, background transparency if needed, platform safe zones, caption space, and localization copy zones.

Use reference images whenever factual appearance matters. For exact packaging, logos, labels, menu boards, nutrition panels, or product geometry, prefer compositing/retouching from approved product photography over text-to-image generation.

### Prompt pattern

Use this pattern flexibly; do not treat it as mandatory syntax:

```text
Create [deliverable] for [brand/product/menu item].
Factual locks: [exact SKU/menu/recipe facts], [portion/serving/pack size], [approved visible ingredients], [excluded ingredients], [label/package reference must match].
Appetite direction: [texture, temperature, freshness, sensory cue].
Scene and styling: [surface, props, hands, vessel, garnish, background], [scale cue].
Camera/lighting: [lens/angle/movement], [lighting/reflection/steam/condensation].
For video: [timed action beats], [start/end state].
Truth constraints: no invented claims, no extra ingredients, no label changes, no unsupported nutrition/allergen/health copy, no misleading scale.
Delivery: [ratio/resolution/duration/safe zones/caption area/file type].
```

For negative prompts or repair instructions, target the specific failure:

- "Remove all almonds and nut fragments; this SKU is nut-free in the provided brief and must not imply nuts."
- "Keep the Nutrition Facts panel out of focus; do not invent readable numbers."
- "Match the bottle label from reference; do not reinterpret the logo or vintage."
- "Reduce steam; product is a chilled bottled tea."
- "Make the serving two 42 g bars, not a full tray."

## Format-specific guidance

### Restaurant and menu visuals

- Confirm standard build, portion, garnish, plating, calories/prices if shown, location availability, and whether modifiers can be displayed.
- Use the actual dish as the hero. If hero ingredients are shown around the dish, confirm they are primary ingredients or label as serving suggestion where allowed.
- For delivery/app thumbnails, prioritize recognizability at small sizes: fewer props, stronger shape, clean edges, and clear category cue.
- For menu boards, leave enough clear space for prices, calories, dietary icons, and localization. Do not create icons unless approved.

### Recipe videos

- Use a recipe truth table: ingredient, amount, preparation state, visible moment, substitution, allergen flag, and source.
- Show method-critical steps in order. Do not skip a proof/rest/chill/cook step if skipping would make the recipe misleading or unsafe.
- Make timing honest: compress with edits, but do not imply a 4-hour process happens in 10 minutes unless copy clarifies "after chilling," "after rising," or similar.
- Use captions for ingredient amounts and heat/time, but verify them against the recipe.
- For ASMR/social clips, keep the sensory hook tied to real technique: crackle, whisk, sizzle, pour, slice, pull, fizz, crunch.

### CPG and ecommerce product images

- Main-image rules vary by marketplace and change often. Re-check current marketplace requirements at production time. For Amazon, the official product image guide says images should accurately represent the product and match the product title; see Amazon Seller Central [Product Image Guide](https://sellercentral.amazon.com/help/hub/reference/external/G1881?locale=en-US). Verified 2026-07-11.
- Use approved packshots for exact packaging. For generated environments, composite the packshot rather than regenerate label text.
- Preserve pack count, flavor, net weight/volume, label hierarchy, closure, cap, can/bottle shape, multipack arrangement, and tamper seals.
- For lifestyle modules, clarify what is included versus serving suggestion. Do not imply accessories, bulk quantities, or prepared dishes are included unless they are.
- For marketplace alt images, use one asset per job: ingredient story, scale, usage occasion, texture, nutrition/claim panel, comparison, or bundle contents. Avoid stuffing every claim into one image.

### Beverage pours and liquid action

- Define liquid physics before generation: viscosity, carbonation, clarity, foam persistence, ice interaction, condensation, temperature, pour height, glass shape, and splash tolerance.
- Time video shots around action:
  - 0.0-0.4s: container tilt or opener crack.
  - 0.4-1.2s: stream forms and catches light.
  - 1.2-2.0s: contact, splash, foam/crema/ice movement.
  - 2.0-3.5s: bubbles/steam/condensation settle.
  - 3.5s+: hero hold with label or glass visible.
- For coffee, beer, sparkling drinks, smoothies, milk, spirits, tea, and sauces, specify a plausible foam, crema, head, bubble, or surface behavior. Generic "liquid splash" often looks synthetic.

### Packaging and label mockups

- Use "concept mockup" only when packaging is not final. Do not place mockups in marketplace or paid media without approval.
- Lock text from source files; do not let OCR or generative models rewrite regulated panels.
- Check seams, folds, dielines, cap orientation, label wrap, nutrition panel legibility, barcode placement, certification marks, and trademark use.
- If a label is intentionally blurred or backgrounded, ensure no hallucinated readable claims remain.

### Social food clips

- Start with an immediately readable sensory action: pour, cut, pull, steam, crunch, dip, drizzle, pack tear, spoon plunge, or first bite.
- Design for sound-off comprehension: captions, supers, visual step changes, and end card.
- Keep safe zones clear for platform UI; re-check current platform specs. Official, volatile references include Meta [Ads Guide](https://www.facebook.com/business/ads-guide/update), TikTok [In-Feed Ads specs](https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads), and Google Ads [video ad specs](https://support.google.com/google-ads/answer/13547298). Verified 2026-07-11.
- Do not use "UGC-style" to hide an ad, sponsorship, or material connection.

## Localization and cultural fit

- Localize units, serving sizes, dietary terms, allergens, language, reading direction, utensils, meal occasions, holidays, alcohol norms, and claims rules.
- Do not translate regulated claims literally without local regulatory approval.
- Adapt appetite cues by market: sweetness, spice, portion size, breakfast/lunch/dinner norms, ice usage, alcohol context, hand eating, chopsticks/cutlery, and color symbolism.
- Check whether pack artwork differs by market; do not show a U.S. Nutrition Facts panel in a market that requires a different label format.

## Accessibility and alt text

Documented fact: W3C WAI guidance says alternative text depends on image usage, context, and content; see W3C WAI [Images Tutorial](https://www.w3.org/WAI/tutorials/images/) and [Alt Decision Tree](https://www.w3.org/WAI/tutorials/images/decision-tree/). Section508.gov also advises meaningful alternative text and treating informative background images as content: [Authoring Meaningful Alternative Text](https://www.section508.gov/create/alternative-text/). Verified 2026-07-11.

Write alt text that communicates the content's function, not every prop. Avoid adding claims not visible or approved.

Examples:

- Ecommerce packshot: "Front of a 12-ounce bottle of Brand X cold brew coffee, vanilla flavor."
- Recipe step: "Dough folded over a cinnamon filling before being sliced into rolls."
- Decorative background: empty alt text or decorative handling if the same information is in surrounding copy.
- Claim-sensitive image: "Granola bar beside almonds and oats" only if almonds and oats are approved visible ingredients or serving suggestions.

For video, include captions, important on-screen text in transcript/description when possible, and non-audio cues for critical steps such as "timer shows 20 minutes" or "thermometer reads 165°F" if such facts are approved.

## Rights, releases, and provenance

Documented fact: U.S. Copyright Office guidance on AI-generated material says copyright protection may be claimed for human contributions, while AI-generated material must be identified/disclaimed in registration contexts; see U.S. Copyright Office [Copyright and Artificial Intelligence](https://www.copyright.gov/ai/) and Federal Register [AI-generated material registration guidance](https://www.federalregister.gov/documents/2023/03/16/2023-05321/copyright-registration-guidance-works-containing-material-generated-by-artificial-intelligence). Verified 2026-07-11.

Production application:

- Track provenance for product photos, packaging art, logos, fonts, music, locations, stock assets, generated images/videos, model versions, seeds, prompts, retouching, and compositing.
- Use approved brand files for logos, labels, certification marks, and trade dress. Do not generate lookalike competitor packaging or trademark-adjacent props.
- Obtain appropriate model releases for recognizable people in commercial food/beverage ads, and property/location releases for private restaurants, bars, kitchens, farms, factories, homes, or recognizable interiors. Releases and personality/privacy rights vary by jurisdiction; escalate to production/legal.
- For AI-generated or synthetic people, avoid implying a real person's endorsement or creating a lookalike without approval.
- For restaurants and chefs, confirm rights to recipes, plating signatures, menus, uniforms, interiors, and staff likenesses.

## QA checklist

Run this before final delivery:

Product truth:

- Does every visible ingredient, garnish, flavor, pack, size, count, and serving match the brief?
- Are any extra allergens or excluded ingredients visible?
- Does the package/label match approved art? Are hallucinated readable words removed?
- Are scale and serving size honest?
- Are colors faithful to product, brand, and doneness?

Claims and approvals:

- Are nutrition, health, allergen, "free-from," organic, gluten-free, alcohol, sustainability, comparative, price, promotion, endorsement, and certification claims sourced and approved?
- Are disclosures visible and platform-appropriate?
- Is alcohol content adult-oriented and responsible?

Craft:

- Is the appetite cue specific and plausible?
- Are steam, condensation, bubbles, foam, pour, pull, melt, and texture physically coherent across frames?
- Is the hero readable at thumbnail size?
- Are hands, utensils, packaging edges, labels, shadows, reflections, and liquid surfaces clean?
- Does the final crop protect safe zones and copy areas?

Delivery:

- Are variants exported to current platform specs, with filenames and color profiles appropriate to use?
- Are captions, alt text, transcripts, localization, and accessible contrast included where needed?
- Are source files, prompts, seeds/model versions, references, approvals, and release notes recorded?

## Escalation triggers

Stop and request approval or specialist review when any of these appear:

- New or edited regulated copy, label panel, Nutrition Facts, ingredient list, allergen statement, supplement/drug-like claim, medical/diet/weight-loss claim, or child-directed nutrition claim.
- "Healthy," "gluten-free," "organic," "natural," "non-GMO," "no sugar," "low calorie," "high protein," "clean," "detox," "immune," "probiotic," "sustainable," "compostable," or similar claims without source approval.
- Alcohol, cannabis, CBD, caffeine/energy products, supplements, infant/toddler foods, school meals, or vulnerable audiences.
- Paid influencer/creator content, testimonials, UGC reviews, native ads, or endorsements.
- Exact marketplace listings or paid media assets where specs and policies may have changed.
- Missing product/package references for final commercial work.
- Recognizable people, minors, private property, chef/restaurant interiors, unlicensed music, stock assets, or AI-generated people.
- Any request to make food look larger, fresher, more ingredient-rich, healthier, lower-calorie, safer, or more available than the source supports.

## Complete examples

### Example 1: Ecommerce hero plus lifestyle module for a snack bar

Production intent: create an ecommerce image set for a 6-count dark chocolate oat bar without inventing claims.

Inputs and constraints:

- Approved packshot: front of 6-count box and single wrapped bar.
- Approved visible ingredients: oats, dark chocolate chips, sea salt flakes.
- Excluded: nuts, peanuts, dairy glass, "high protein," "low sugar."
- Deliverables: marketplace main image, lifestyle snack image, texture close-up, scale image.

Workflow:

1. Use the approved packshot for the main image; do not regenerate package text.
2. Create lifestyle background separately and composite packshot.
3. Prompt texture close-up using only approved inclusions.
4. Keep Nutrition Facts out of frame unless client provides exact panel.
5. Export marketplace-ready ratios after rechecking current marketplace specs.

Example prompt:

```text
Create a lifestyle ecommerce image for a 6-count dark chocolate oat snack bar. Use the approved packshot as the exact package reference; preserve all label art and do not rewrite text. Scene: clean afternoon kitchen counter with one unwrapped bar broken in half on parchment, visible oats, dark chocolate chips, and a few sea salt flakes. Appetite direction: chewy oat crumb, glossy chocolate chips, crisp broken edge. Scale cue: one adult hand placing the bar beside the 6-count box. Lighting: soft side daylight, realistic shadows. Truth constraints: no nuts, peanuts, milk glass, fruit, protein powder, nutrition claims, or unreadable invented package copy. Leave top-right negative space for approved ecommerce callout. Output: 4:5 lifestyle image and 1:1 crop.
```

Expected result: a truthful lifestyle image that sells texture and scale without implying unapproved ingredients or claims.

Likely failures: hallucinated label words, nuts appearing as texture, bar enlarged beyond pack size, extra "protein" badge, overly melted chocolate that changes product expectation.

### Example 2: Recipe reel for skillet pasta

Production intent: create a 20-second vertical recipe video for a restaurant's creamy tomato pasta kit.

Inputs and constraints:

- Recipe source: client-provided method and exact ingredient amounts.
- Visible ingredients: pasta, tomato sauce, cream, basil, parmesan garnish.
- Allergens: wheat and milk are present; do not call it vegan or gluten-free.
- Must show final kit branding but not Nutrition Facts.

Workflow:

1. Build a recipe truth table from the client method.
2. Use vertical 9:16 with bottom caption safe zone checked against current platform UI.
3. Show a truthful step sequence: boil, sauce, combine, finish, serve.
4. Use captions only from the approved recipe.
5. End on plated pasta plus kit box, with allergens handled by client-approved copy if needed.

Example video direction:

```text
0.0-2.0s: Close macro of pasta dropping into boiling salted water; caption "Cook pasta until al dente" only if approved by recipe.
2.0-5.0s: Tomato sauce poured into skillet, steam visible, spoon swirl.
5.0-8.0s: Cream added in a thin stream; sauce color shifts from red to orange-pink.
8.0-12.0s: Pasta transferred into skillet and tossed; sauce clings to ridges.
12.0-16.0s: Parmesan and basil added as approved garnish; no extra vegetables.
16.0-20.0s: Hero bowl with package in background, label from approved packshot, no invented nutrition panel.
```

Expected result: sensory and fast, but still a truthful recipe compression.

Likely failures: adding shrimp or mushrooms for visual interest, claiming "gluten-free," showing a generic box with hallucinated text, unsafe raw ingredient handling, captions that change the recipe.

### Example 3: Alcohol cocktail pour for paid social

Production intent: create a premium 6-second whiskey highball clip for adult paid social.

Inputs and constraints:

- Approved bottle packshot, ABV, and label.
- Adult audience only; no minors, driving, athletic activity, intoxication, or health/performance claims.
- Requires compliance review before posting.

Example prompt:

```text
Create a 6-second vertical paid-social cocktail pour for an adult whiskey brand. Use the approved bottle reference exactly; do not rewrite the label, age statement, ABV, or origin. Scene: premium bar top at night, clear highball glass with large ice spear, measured pour of whiskey followed by sparkling water, subtle citrus twist as an approved garnish. Motion: 0-1s bottle enters with label readable; 1-3s amber liquid pours over ice with realistic refraction; 3-4.5s sparkling water creates gentle bubbles; 4.5-6s hero hold with glass and bottle, no drinking shown. Tone: restrained, adult, responsible, elegant. Truth constraints: no minors, no intoxication, no driving, no sports, no medical or performance claims, no invented awards, no exaggerated ABV, no "low calorie" copy. Leave top and bottom safe zones clear for platform UI and legal/disclosure copy.
```

Expected result: adult-oriented product beauty shot ready for compliance review, not a final posted ad.

Likely failures: unreadable or altered label, party scene with youth appeal, drinking-before-driving implication, exaggerated splash, invented "award-winning" or "smoothest" claim.

### Example 4: Menu thumbnail repair

Problem: generated image for "sesame-free chicken bowl" shows sesame seeds and a bowl twice the standard portion.

Repair instruction:

```text
Revise the image to match the approved sesame-free chicken bowl. Remove all sesame seeds and sesame-like garnish. Use the standard 14-ounce bowl as the scale reference, with one portion of chicken, rice, cucumber, carrot, and scallion only. Keep the sauce in a small side cup if approved. Do not add nuts, sesame, egg, or extra protein. Maintain appetizing color and steam, but keep serving size realistic for a single menu item.
```

Expected result: allergen-risk visual corrected without reducing appetite appeal.

Critical check: if "sesame-free" is a claim intended for publication, escalate for allergen/regulatory approval even after the visual repair.

## Source notes

Use these sources as starting points, not as a substitute for current legal/platform review. Regulations, platform specs, and marketplace rules are volatile and jurisdiction-specific.

- FTC: [Health Products Compliance Guidance](https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance), [Health Claims](https://www.ftc.gov/business-guidance/advertising-marketing/health-claims), [Endorsements, Influencers, and Reviews](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews), [Native Advertising](https://www.ftc.gov/business-guidance/resources/native-advertising-guide-businesses).
- FDA/food safety: [Food Labeling Guide](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/guidance-industry-food-labeling-guide), [Food Allergies](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/food-allergies), [Menu Labeling Requirements](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/menu-labeling-requirements), [Nutrition Facts Label](https://www.fda.gov/food/nutrition-education-resources-materials/nutrition-facts-label), [Gluten-Free Q&A](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/questions-and-answers-gluten-free-food-labeling-final-rule), [Use of "Healthy" Claim](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/use-healthy-claim-food-labeling), USDA FSIS [Safe Temperature Chart](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart), FDA [Flour Is a Raw Food](https://www.fda.gov/consumers/consumer-updates/flour-raw-food-and-other-safety-facts).
- Alcohol: TTB [Alcohol Beverage Advertising](https://www.ttb.gov/what-we-do/program-areas/advertising), TTB [Industry Circular 2024-1](https://www.ttb.gov/public-information/industry-circulars/ttb-industry-circular-2024-1), DISCUS [Code of Responsible Practices](https://distilledspirits.org/code-of-responsible-practices/), Beer Institute [Advertising & Marketing Code](https://www.beerinstitute.org/policy-responsibility/responsibility/advertising-marketing-code/), Wine Institute [Ad Code](https://wineinstitute.org/our-work/responsibility/social/ad-code/).
- Platform/accessibility/rights: Amazon Seller Central [Product Image Guide](https://sellercentral.amazon.com/help/hub/reference/external/G1881?locale=en-US), Meta [Ads Guide](https://www.facebook.com/business/ads-guide/update), TikTok [In-Feed Ads](https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads), Google Ads [Video Ad Specs](https://support.google.com/google-ads/answer/13547298), W3C WAI [Images Tutorial](https://www.w3.org/WAI/tutorials/images/), Section508.gov [Alternative Text](https://www.section508.gov/create/alternative-text/), U.S. Copyright Office [AI](https://www.copyright.gov/ai/).
