---
name: midjourney-image
description: Plan, prompt, iterate, edit, migrate, and quality-check still-image work made with Midjourney's documented website and Discord interfaces. Use for Midjourney model and parameter selection, image/style/Omni references, Draft or Conversational workflows, typography-aware production, privacy and rights review, or troubleshooting a Midjourney image pipeline; do not use it to invent or automate an unsupported Midjourney API.
---

# Midjourney image production

## Operating boundary

Use this skill to prepare and supervise image work in Midjourney's documented consumer surfaces:

- the Imagine bar, Create/Organize pages, Editor, Personalize page, and Moodboards page on `midjourney.com`;
- the Midjourney Bot and documented slash commands in Discord.

Do **not** translate those buttons, slash commands, parameters, job IDs, or image URLs into a supposed REST endpoint, SDK, webhook, environment variable, or machine-to-machine contract. As verified 2026-07-09, Midjourney's Terms prohibit automated tools from accessing, interacting with, or generating through the Services, and its Community Guidelines say that, with rare explicitly granted exceptions, Midjourney does not provide an API or authorized third-party scripts. A Discord command is a user-interface action, not an API.

For an agent-safe workflow:

1. Prepare the brief, prompts, parameter matrix, reference manifest, consent record, and QA checklist offline.
2. Ask the authorized account holder to submit approved jobs manually in the official website or Discord UI.
3. Have the user return downloaded outputs and, when useful, the job ID, seed, final prompt, version, and parameter record.
4. Perform selection, comparison, rights review, compositing, typography, metadata, and QA in authorized local tools.
5. Never drive the website or Discord with browser automation, self-bots, unofficial clients, scraping, macros, or simulated clicks. Never share an account.

If a customer says they have a rare written Midjourney automation exception, require the actual provider-issued agreement and its technical documentation. Treat that separately from this consumer-interface skill; do not infer authorization from a subscription, bot access, or an internal wrapper.

This skill is about still images. Midjourney documents an **Animate** creation action that can turn a suitable still into a five-second video, but that is a handoff to a video workflow, not an image-generation parameter recipe here.

## Current capability map

The following snapshot is volatile and was verified against first-party documentation on **2026-07-09**.

| Choice | Use it for | Production constraints |
|---|---|---|
| **V8.1** | Current default general-image model; prompt fidelity, detail, SD/HD stills | Released 2026-04-30 and default since 2026-06-10. `--sd` is nominally 1024 px; `--hd` nominally 2048 px. HD supports aspect ratios only through 4:1; SD through 14:1. The current compatibility chart does not support the Quality parameter in V8.1. The dedicated Draft page documents website-only V8.1 Draft, despite a conflicting mark in the Version chart. Turbo is not supported. |
| **V7** | Omni Reference, established V7 personalization, and V7 Draft/Conversational production | Omni Reference forces V7 and costs about twice a normal image prompt. V7 quality 2/4 consumes roughly 2x/4x GPU time. |
| **Niji 7** | Anime and Eastern illustration aesthetics, line work, literal/stylized graphic rendering | Select with the Niji model setting or `--niji 7`. Image-weight range differs from V8.1/V7. Do not assume photoreal or brand-identity behavior. |
| **V6.1** | Compatibility target for current Editor, Pan, Zoom, and region editing; legacy workflows | Current V8.1 edits may internally generate with V6.1, changing model character and detail. Character Reference belongs to V6/Niji 6; V7 uses Omni Reference. |

V8.0 Alpha, V7, V6.1, and V6 remain lifecycle or compatibility choices, not aliases for the default. Record the actual model version on every approved asset. Old seeds, style codes, and prompt behavior are not a promise of future reproduction.

**First-party documentation conflict:** checked 2026-07-09, the Version compatibility chart marks Draft unavailable for V8.1, while the newer, feature-specific Draft and Conversational Modes page explicitly documents V8.1 website Draft with 24 previews at 512×512 for about 0.4 GPU minutes. Prefer the specific Draft page for an exploratory manual workflow, but verify the live website before scheduling or budgeting a batch and retain a non-Draft SD fallback.

### Resolution and edit lifecycle

- V8.1 SD jobs are documented at about 0.8 GPU minutes and HD at about 1.3 GPU minutes. V8.1 Draft produces 24 previews at 512×512 for about 0.4 GPU minutes.
- HD is a generation mode, not merely a lossless export switch. An HD result cannot be upscaled further by the V8.1 upscalers.
- Pan, Zoom, Editor, and Vary Region on a V8.1 image currently route through V6.1. Editing an HD image downscales the result to SD; upscale again only after the structural edit is approved.
- The V8.1 Subtle and Creative upscalers take SD output to roughly 2× linear resolution. Creative may invent or alter detail; Subtle aims to preserve more closely. Neither guarantees pixel identity.
- Resolution labels are nominal. Exact dimensions vary with aspect ratio, and the provider says HD dimensions may vary slightly.

## Access, capacity, and budget

Plan facts below were verified 2026-07-09 and can change. Confirm the Manage Subscription page before committing money or a schedule.

| Plan | Monthly price | Included Fast time | Relax images | Image concurrency | Stealth |
|---|---:|---:|---|---|---|
| Basic | $10 | 3.3 h / 200 min | No | 3 Fast | No |
| Standard | $30 | 15 h | Unlimited | 3 Fast **or** Relax | No |
| Pro | $60 | 30 h | Unlimited | 12 Fast **or** 3 Relax | Yes |
| Mega | $120 | 60 h | Unlimited | 12 Fast **or** 3 Relax | Yes |

Annual plans are advertised at a 20% discount paid for the year up front. Extra Fast time is listed at $4/hour. Unused subscription Fast time does not roll over.

- Relax image jobs are unlimited on Standard, Pro, and Mega but may wait from 0–30 minutes depending on demand and prior use.
- Turbo uses twice the Fast time and is experimental; it is unavailable in V8.1. A job can fall back to Fast when Turbo is unavailable.
- Repeat and permutations are unavailable in Relax. Their per-submission caps are 4 jobs on Basic, 10 on Standard, and 40 on Pro/Mega; every expanded job consumes time.
- Queued-job limits and running concurrency are not throughput guarantees. Schedule a small calibration batch before a deadline.
- Use `/info` in Discord or the website's account information to inspect remaining time and running/queued jobs; this is a manual UI check.

Budget by **jobs and transformations**, not only final images. Initial grids, Omni references, quality multipliers, upscales, variations, region edits, and remixes all consume GPU capacity. A defensible estimate states assumptions and keeps a reserve for repair.

## Build a production brief before prompting

Turn an aesthetic request into testable constraints:

1. **Deliverable:** channel, crop, pixel need, number of finals, deadline, and whether exact text or logos are required.
2. **Subject invariants:** identity, silhouette, product geometry, materials, wardrobe, pose, count, and prohibited changes.
3. **Scene:** environment, time, weather, spatial relationship, and required negative space.
4. **Visual language:** medium, era, palette, lighting, lens/composition language, texture, and finish.
5. **References:** what each reference should control—content/composition, style, or identity/object consistency—and proof that the user may upload it.
6. **Risk:** public visibility, confidentiality, real-person consent, trademarks, sensitive content, deception, and disclosure/provenance needs.
7. **Acceptance checks:** framing, anatomy, text, product/logo fidelity, reference resemblance, seam quality, forbidden content, and technical export.

Separate hard constraints from preferences. Midjourney is generative, so a prompt cannot make exact geometry, identity, text, or logos deterministic. If an invariant must be exact, reserve it for photography, 3D, vector work, or post-compositing.

## Prompt construction

Midjourney's documented prompt syntax is compact. Describe what should be visible, then place parameters at the end.

```text
[subject and action], [environment], [medium/material], [composition and camera], [lighting], [palette/mood], [specific visible constraints] --parameters
```

This is a production heuristic, not mandatory prose. Prefer concrete visual nouns and modifiers over instructions about the model's thought process.

### Prompt rules

- Put image prompt URLs at the beginning in Discord; on the website, add images through the image control and assign their role.
- Put all parameters at the end, preceded by a space: `... --ar 4:5 --s 150`. Do not attach punctuation after a parameter value.
- Keep the positive scene description coherent. Long lists of commands and negations can compete.
- Specify count, placement, crop, and relationships explicitly: “one ceramic bottle centered, cap visible, label area blank.”
- Treat camera terms as visual direction, not physically exact simulation. Pair a lens or shot phrase with distance, angle, depth, and composition.
- For generated text, enclose a short Latin-alphabet phrase in **double quotes**. Single quotes are not the documented text syntax.
- Save the submitted prompt, resulting prompt metadata, model, parameters, references, seed, and job ID before revision.

### Negative prompting

Use `--no item1, item2` for visible exclusions. It is equivalent to negative multi-prompt weighting, not a semantic policy engine. Moderation evaluates terms independently, so `--no modern clothing` may be interpreted as containing “no clothing.” Prefer a positive alternative such as “Victorian formalwear” and keep `--no` to unambiguous objects like `--no watermark, border`.

## Reference strategy: give each image one job

Uploading an image never promises a copy. Crop references near the target aspect ratio and use clean, representative files. Supported upload formats documented for image prompts include PNG, GIF, WebP, JPG, and JPEG; the website upload limit is 10 MB.

### Image Prompt — content, composition, and palette

Use an Image Prompt when the reference should influence subject matter, composition, or colors.

- Website: upload and choose **Image Prompt**.
- Discord: place one or more direct image URLs before the text prompt.
- Control influence with `--iw`. The documented range is 0–3 for V8.1/V7 and 0–2 for Niji 7; default is 1.
- One image generally needs a text prompt. Multiple images can be blended without text, though text usually makes the production intent auditable.
- An image-only prompt cannot use `--stylize` or `--weird`.

Use a low-to-moderate `--iw` first. If structure drifts, increase it; if the result merely imitates the reference and ignores the brief, reduce it or improve the text.

### Style Reference — visual treatment, not depicted content

Use Style Reference for color, medium, texture, lighting, and overall treatment while describing new content in text.

- Website: assign the upload as a **Style Reference**. Discord: append `--sref URL`.
- Multiple style references are supported. Discord supports per-reference relative weights such as `--sref URL_A::2 URL_B::1`.
- `--sw` controls style influence from 0–1000; default 100.
- A numeric style code can be used as `--sref code`; `--sref random` explores random codes. A style image cannot be converted into a numeric code.
- In V7, `--sv 6` is the current default style-reference system and `--sv 4` preserves the older pre-2025-06-16 behavior. Pin `--sv` when migrating a style-sensitive campaign.
- Moodboards are not compatible with `--sw` or `--sv`.

Do not expect the people, objects, or words in a style reference to transfer. Describe all required content in the text prompt.

### Omni Reference — one person, object, vehicle, or creature

Use Omni Reference for stronger identity/object continuity across a new V7 scene.

- It is V7-only; adding one Omni reference forces V7. Only one Omni image is accepted, and a text prompt is required.
- Website: assign **Omni Reference**. Discord: append `--oref URL`.
- `--ow` ranges from 1–1000 and defaults to 100. Midjourney recommends staying below 400 in typical work unless intentionally combining with strong stylization.
- It costs roughly twice a standard image prompt.
- It is compatible with Personalization, moodboards, `--stylize`, Style References, and Image Prompts.
- It is not compatible with Draft, Conversational mode, Fast mode, `--q 4`, or direct V6.1-based Pan/Zoom/Vary Region editing.

To edit an Omni result, open it in the Editor and remove the Omni image and `--oref`/`--ow`; expect continuity to weaken because the edit currently uses V6.1. Exact faces, hands, small emblems, logos, and product details remain a QA problem.

Only upload a real person's image with the necessary consent and rights. Do not create sexualized, abusive, derogatory, inflammatory, deceptive, or otherwise disallowed manipulations. A blocked job is not evidence that the underlying request would have been permitted.

### Character Reference — legacy compatibility

`--cref` and `--cw` belong to V6/Niji 6 workflows. `--cw` ranges 0–100 and defaults to 100. For a V7 workflow, migrate to Omni Reference; do not silently keep `--cref`. Neither system guarantees an exact real person or exact logos/details.

### Personalization and Moodboards

Personalization applies a learned profile with `--p`; the global V7/V8 profile must first be unlocked by selecting images. Profiles and moodboards have IDs that resolve to versioned codes. Save the resolved code for campaign reproducibility rather than relying only on a mutable profile ID.

Moodboards are broader curated aesthetic guides and work with V6, V7, and V8.1. They can be selected in the web UI or used as `--p mID`/the resolved code. `--stylize` controls their strength, but moodboards cannot be combined with `--sw` or `--sv`. Do not stack Personalization, a moodboard, and style references reflexively; isolate one influence at a time during calibration.

## Parameter decisions

These are documented controls, not universal “best settings.” Change one material variable at a time during diagnosis.

| Parameter | Current documented behavior | Production use and caution |
|---|---|---|
| `--ar W:H` | Aspect ratio; default 1:1; integer ratios | Match the delivery crop at generation time. V8.1 limits: SD through 14:1, HD through 4:1. Extreme ratios are experimental and ratio is not pixel size. |
| `--chaos N` / `--c N` | 0–100, default 0 | Increase breadth among a grid; higher values reduce predictability and can weaken adherence. Use higher chaos for ideation, lower for controlled revisions. |
| `--stylize N` / `--s N` | 0–1000, default 100 | Higher values increase Midjourney's aesthetic influence and may reduce literal adherence. Lower it for layout, product, or text-sensitive work. |
| `--weird N` / `--w N` | Experimental, 0–3000 | Explore unusual aesthetics. Behavior can change and is not fully compatible with deterministic seed comparisons. |
| `--quality N` / `--q N` | V7 accepts 1, 2, 4; q2/q4 costs about 2x/4x. The current V8.1 chart marks Quality unsupported. | In V7, spend quality after composition is promising. Quality affects the initial job, not later variations, inpainting, outpainting, or upscaling. V7 `--q 4` is incompatible with Omni. Do not copy a V7 quality flag into V8.1. |
| `--seed N` | Integer 0–4,294,967,295 | Useful for controlled comparisons, not archival determinism. V8.1 is documented as highly repeatable under like conditions, but seeds can drift across sessions, models, settings, and Turbo. |
| `--tile` | Makes a single seamless repeating tile | Preview the repeated pattern externally. Upscaling can break the seam; test the exact exported asset. |
| `--no ...` | Negative multi-prompt influence | Keep exclusions unambiguous; moderation parses each word. Positive replacement is often safer. |
| `--raw` | Reduces default Midjourney styling/automation | Useful for literal, photographic, layout, or text-sensitive work; combine with precise direction, not vague prompts. |
| `--iw N` | Image Prompt influence | V8.1/V7 0–3; Niji 7 0–2; default 1. Tune against text adherence. |
| `--sref`, `--sw`, `--sv` | Style image/code, strength, system version | Pin references and `--sv` for style migration. `--sw` default 100, range 0–1000. |
| `--oref`, `--ow` | V7 Omni image and strength | One image, text required, default 100, range 1–1000, about 2x GPU, compatibility limits. |
| `--p` | Personalization profile or moodboard | Save resolved codes because profiles evolve. |
| `--draft` | Draft generation | V8.1 website Draft is a 24-image 512×512 exploration board; V7 Draft uses half standard GPU cost and generates four images. Enhance or vary a selected concept before judging finish. |
| `--fast`, `--relax`, `--turbo` | Per-job speed mode | Relax availability is plan-limited; repeat/permutations do not work in Relax; Turbo costs 2x and does not support V8.1. |
| `--repeat N` / `--r N` | Repeat a prompt | Fast/Turbo only; plan caps 4/10/40. Treat every repeat as a paid job. |
| `{a,b,c}` | Permutation syntax | Expands prompt/parameter variants in Fast/Turbo only. Confirm the job count before submission. Escape a literal comma inside braces with `\,`. |
| `--stealth`, `--public` | Per-job visibility on the website | Pro/Mega only for Stealth. Does not hide a creation from people in a shared Discord channel. |
| `--v`, `--niji`, `--sd`, `--hd` | Model family and V8.1 resolution | Pin them in a production record. Omni can force V7. HD limits editing/upscaling and aspect ratio. |

The live Parameter List also includes video-only controls. Do not copy `--motion`, `--loop`, `--end`, `--bs`, or `--video` into a still-image prompt merely because they appear in the same documentation.

## Draft and Conversational modes

Use Draft to search a concept space cheaply, not to approve fine detail.

### V8.1 Draft

On the website, Draft creates 24 square 512×512 previews. Select candidates, then Vary or Remix them to SD/HD. It is ideal for composition, palette, silhouette, and art-direction search, but too coarse for typography, fingers, packaging, textures, or delivery QA.

### V7 Draft

V7 Draft returns four images at about half standard GPU cost. Use **Enhance** to generate a higher-quality interpretation. Enhancement can change details, so re-check all invariants.

### Conversational mode

Conversational mode is a website prompt-writing assistant available for V7/V8.1. It accepts typed or spoken natural language and can rewrite a request into a prompt. Typed conversation can work with or without Draft; voice requires Draft. Treat its rewritten prompt as an editable proposal: inspect the actual submitted text, parameters, version, and references. It is not an autonomous API or a substitute for rights/safety review.

## Controlled iteration and repair

Use a funnel rather than changing the entire prompt after every result.

1. **Explore:** choose the model and target aspect ratio; run a Draft or low-cost standard calibration with moderate settings.
2. **Select structure:** judge silhouette, layout, pose, crop, and negative space before surface detail.
3. **Lock variables:** save prompt, model, parameter set, references, resolved profile/style codes, job ID, and seed.
4. **Vary:** use Subtle when the composition is right and Strong when the concept needs movement. Variations are related generations, not exact edits.
5. **Remix:** change prompt text or compatible parameters while making a variation/edit. On web, Remix populates the Imagine bar or Editor; in Discord, enable Remix in settings or `/prefer remix`. Changing aspect ratio via Remix stretches rather than outpaints—use Pan, Custom Zoom, or Editor to add canvas.
6. **Repair locally:** use Editor erase/restore, Smart Select, layers, Pan, Zoom, or region editing. Mask enough context for the model to solve the boundary. Current edits route through V6.1, so compare identity and style again.
7. **Retexture:** use when the structure is acceptable but the whole treatment must change. It regenerates the full image while retaining broad structure; it is not a pixel-preserving material swap.
8. **Upscale last:** choose Subtle for preservation or Creative for invented detail. Run a difference/side-by-side check.
9. **Finish externally:** composite exact typography, logos, legal copy, product geometry, or color-managed assets in a suitable editor.

### Editor privacy nuance

The current Editor documentation makes a specific visibility distinction. Ordinary Editor creations are saved in the Editor and do not appear in Create/Organize unless upscaled. When a workflow uses externally uploaded images in the Editor or multiple layers, however, both the uploads and edited results—including upscales—are documented as visible only to that user, absent from other users on midjourney.com, and unavailable to Discord's `show` command. This is a useful Basic-plan non-public route for a genuine external-image editing job; it is not a general privacy switch for Imagine, Image Prompt, Style Reference, or Omni jobs.

Do not equate this product-visibility behavior with contractual confidentiality or local processing. Midjourney still receives, stores, and processes the content; its Terms, Privacy Policy, broad content license, external-image rules, and account security still apply. Require client/data-policy approval before uploading confidential material, minimize the input, and prefer a local or contractually approved system when non-disclosure is essential.

## Typography and graphic design

Midjourney supports short generated text in V6 and later, with these documented tactics:

- put a short Latin-alphabet phrase in double quotes;
- use `--raw` and/or reduce `--stylize` when letter accuracy matters;
- repair with Editor/Vary Region when the concept is good;
- simplify the scene so text has a clean surface and clear hierarchy.

Generated typography is still probabilistic. For a brand name, trademark, price, URL, accessibility text, legal copy, medical label, packaging facts, or any phrase where one character matters, generate a blank or placeholder area and composite approved text afterward. QA spelling, punctuation, glyph shape, reading order, contrast, safe area, and export resolution. Do not describe a Midjourney-rendered logo as an exact brand asset.

## Privacy, rights, safety, and provenance

### Public-by-default and Stealth

Midjourney is open by default. Creations can appear on Explore even when generated in a private Discord server or direct message unless Stealth is active.

- Stealth is available only on Pro and Mega. It controls visibility on the Midjourney website.
- Stealth does not hide messages or images from participants in a shared Discord channel. For the strongest available privacy, use Stealth with the web Create page, a direct message, or a private server.
- Turning Stealth on does not retroactively privatize existing creations; make them private individually or in bulk.
- Trashing a creation is not the same as making it private; trashed work may still be discoverable.
- Private content stays private after downgrade, but the Terms describe Stealth as a best-efforts non-publication commitment, not an absolute confidentiality guarantee.
- Making a private image a profile image, banner, or spotlight can make it—and related grid images—public.

Before uploading unreleased products, client work, personal data, or trade secrets, compare this model with the organization's data policy. The Privacy Policy says Midjourney collects information including text/image prompts, public chats, account/contact data, IP address, and billing-related information. Discord separately controls Discord data. Account/data deletion is initiated through the account page, cancels the subscription, has a seven-day reversal window, and is documented as completing within 30 days, subject to policy/legal exceptions.

### Rights and consent

Under the Terms effective 2026-05-27, a compliant user owns Assets to the fullest extent possible under applicable law, subject to third-party rights and stated exceptions. A company above US$1 million annual gross revenue must use Pro or Mega to own its Assets under those Terms. Upscaling someone else's work does not transfer ownership from its creator.

The user grants Midjourney a broad, perpetual license to submitted Content and generated Assets. Therefore:

- verify rights to every prompt image, style reference, Omni image, upload, logo, and source asset;
- obtain documented consent for identifiable people and sensitive portrayals;
- do not use the service to infringe copyright, patent, or trademark rights;
- do not promise copyrightability, exclusivity, non-infringement, or trademark clearance; escalate consequential uses to counsel;
- review third-party likeness, location, cultural, and product rights independently.

### Safety and truthful provenance

The Community Guidelines apply to public, private, hidden, deleted, Stealth, direct-message, and website work. They require SFW content; prohibit abusive or harmful material, misinformation/disinformation, political-campaign or election-influence images, and deception/fraud; and say not to intentionally mislead recipients about a generated image's nature or source. Passing automated moderation does not prove that a request is allowed.

For every final, keep a production ledger with:

- creation date, account/plan context, model/version, full prompt and parameters;
- job ID, seed, visibility mode, input/reference file hashes or stable IDs, and resolved style/profile codes;
- source, license, and consent for each input;
- selected output, variations/edits/upscales, and all post-production changes;
- reviewer, safety/rights disposition, and any AI disclosure required by the channel.

Do not claim Midjourney supplies cryptographic provenance, C2PA credentials, or guaranteed watermarking unless the actual exported file is independently verified to contain it. Add durable provenance or disclosure in the downstream publishing workflow when required.

## QA gates

### Before manual submission

- The official UI, actual account holder, plan, speed, visibility, and budget are identified.
- The model supports every reference and parameter combination.
- References have a documented role and upload rights; real-person consent is recorded.
- Exact text, logo, product, and geometry needs have a post-production plan.
- The prompt is SFW, non-deceptive, and consistent with the Terms and applicable law.
- The projected expansion from repeats/permutations is confirmed.

### Before approval

- **Brief:** correct subject count, pose/action, composition, crop, palette, mood, and negative space.
- **Continuity:** face, hair, wardrobe, props, product form, and distinctive marks checked against authorized references.
- **Image integrity:** hands, eyes, teeth, edges, reflections, shadows, occlusion, repeated structures, and impossible geometry inspected at 100%.
- **Text/brand:** every glyph and logo replaced or verified; no accidental watermark, pseudo-signature, or competing brand.
- **Pattern:** a `--tile` output tested in at least a 3×3 repeat at the final file resolution; seam checked after any upscale.
- **Edit drift:** pre/post Editor, Retexture, variation, and upscale compared for lost invariants.
- **Delivery:** pixel dimensions, aspect, color profile, alpha/background, compression, file naming, and safe areas meet the destination specification.
- **Governance:** visibility, rights, consent, safety, disclosure, and provenance ledger complete.

Reject and repair rather than rationalize a missed hard constraint.

## Common failure diagnoses

| Symptom | Likely cause | Repair |
|---|---|---|
| Prompt looks attractive but ignores layout | Stylize/reference influence too high; too many competing clauses | Lower `--s`, `--sw`, `--iw`, or `--ow`; simplify; state spatial relationships; test one influence at a time. |
| Character/object drifts between scenes | Wrong reference class, V8.1 selected with Omni intent, or edit crossed into V6.1 | Use one clean V7 Omni ref; pin `--v 7`; moderate `--ow`; minimize current Editor round trips; composite exact details. |
| Campaign style changed after rerun | Mutable personalization, unpinned `--sv`, model default changed, or seed over-trusted | Save resolved codes, pin model/`--sv`, archive refs and prompt, compare against golden outputs. |
| Aspect remix looks stretched | Remix changed ratio without adding canvas | Use Pan, Custom Zoom, or Editor; rebuild composition at target `--ar`. |
| Upscaled tile has seams | Upscaler altered edge pixels | Use the pre-upscale tile or repair edges externally; validate the final export in 3×3 repetition. |
| Text is almost correct | Generative typography limitation | Reduce phrase length, use double quotes/Raw/lower stylize for concepting, then replace exact copy in post. |
| “Private” job is visible | Stealth absent, used a shared channel, existing job not privatized, or private image published via profile/spotlight | Verify Pro/Mega Stealth before creation; use web/DM/private server; privatize existing jobs; audit profile/Explore state. |
| Old `--cref` workflow fails in V7 | Character Reference is a V6/Niji 6 feature | Replace with one Omni image, `--oref`, and `--ow`; rebaseline because behavior differs. |
| Agent proposes a Discord bot or endpoint | UI concepts were mistaken for an integration contract | Stop. Return to offline preparation + manual official-UI submission; require explicit provider authorization for any exception. |

## Complete examples

Each example is illustrative, not a required formula. Replace subjects, rights context, and parameters to match the brief.

### Example 1 — controlled product campaign with exact label in post

**Intent:** produce a 4:5 hero concept for a licensed ceramic skincare bottle while preserving a clean label zone.

**Interface/model:** authorized user submits manually in the website Imagine bar, V8.1 SD for exploration, then HD or approved upscale after layout lock.

**Inputs and constraints:** one authorized bottle photo assigned as Image Prompt; exact logo and legal copy must not be generated; warm limestone set; one bottle only; label faces camera.

**Complete prompt:**

```text
one matte ivory ceramic skincare bottle standing upright on a pale limestone plinth, cap fully visible, front label panel blank and facing camera, soft late-afternoon window light from camera left, restrained sand and cream palette, premium editorial product photography, eye-level three-quarter view, crisp bottle silhouette, gentle realistic contact shadow, generous clean negative space above and to the right --v 8.1 --sd --ar 4:5 --raw --s 70 --iw 1.2 --chaos 4 --no text, logo, watermark, flowers
```

**Why:** Raw and low stylize favor literal layout; moderate image weight carries form without asking for an exact copy; low chaos stabilizes comparisons; the blank panel creates a post-production target.

**Expected result:** multiple product-photo concepts with one centered bottle, readable silhouette, and a clean label surface.

**Likely failures and response:** warped cap or changed bottle proportions → reduce style/reference conflict and composite the licensed packshot; pseudo-lettering → repair/paint blank; unwanted crop → regenerate at 4:5 rather than stretch with Remix. Add approved vector label, legal copy, and exact color externally, then inspect reflections and contact shadow.

**Meaningful variation:** test `--s {40,70,110}` as a three-job Fast permutation only after the account holder confirms cost.

### Example 2 — V7 character continuity across a new scene

**Intent:** depict an authorized fictional mascot in a rainy transit station while keeping recognizable costume and silhouette.

**Interface/model:** one clean full-body design sheet assigned as Omni Reference on the website; manual V7 submission in Relax mode on a Standard, Pro, or Mega plan. Verify the live mode before submitting because an account-level Fast default is incompatible with Omni.

**Inputs and constraints:** user owns the mascot; one Omni image; no region editing until continuity approval; no exact typography.

**Complete prompt:**

```text
the same friendly teal courier mascot waiting beneath a glass transit canopy in light rain, yellow messenger coat zipped halfway, red rectangular satchel across the body, full body visible, three-quarter standing pose, wet pavement reflections, quiet blue-hour city, cinematic illustrated advertising frame, medium-wide eye-level composition, soft rim light, clear silhouette --v 7 --ar 16:9 --s 120 --oref <AUTHORIZED_MASCOT_IMAGE_URL> --ow 220 --chaos 3 --relax --no text, logo, crowd, umbrella
```

**Why:** V7 is pinned because Omni requires it; one identity reference has one job; `--ow 220` is strong but below the typical 400 caution; low chaos prioritizes continuity.

**Expected result:** scene and pose change while major colors, costume, satchel, and silhouette remain recognizable.

**Likely failures and response:** emblem/satchel geometry drifts → composite exact brand elements; over-literal reference pose → lower `--ow` and strengthen pose language; need to fix a hand → remove Omni before current Editor use, make the smallest contextual repair, then compare identity because the edit routes through V6.1.

**Meaningful variation:** add an authorized Style Reference at `--sw 80` to move lighting/texture while retaining the same Omni image; test it separately before combining.

### Example 3 — seamless textile concept

**Intent:** make a repeatable botanical motif for concept approval, not a production-separated print file.

**Interface/model:** manual V8.1 website or Discord image job.

**Inputs and constraints:** flat two-color motif, no gradients, no text, seamless export required.

**Complete prompt:**

```text
small hand-cut gingko leaves and round seed pods arranged as a balanced scattered textile motif, flat screen-print shapes, two inks only: deep forest green and warm parchment, consistent element scale, generous breathing room, clean crisp edges, no central focal point --v 8.1 --sd --tile --ar 1:1 --raw --s 90 --chaos 8 --no text, border, frame, gradient, shadow
```

**Why:** square tile and `--tile` establish repeat intent; flat positive constraints are clearer than relying on negatives; modest chaos explores arrangements.

**Expected result:** a single square pattern unit whose opposite edges are designed to repeat.

**Likely failures and response:** apparent seam only after upscale → use/test SD output or repair final edges externally; motif collisions in a repeat → choose another variation; unintended third color → separate/recolor in print software.

**QA:** assemble a 3×3 preview from the exact delivered file, inspect all seams and obvious repetition, then perform color separation and trapping outside Midjourney.

### Example 4 — poster concept with reliable final typography

**Intent:** art-direct a vertical festival poster whose final title must read exactly “NIGHT ORBIT / 18 OCT”.

**Interface/model:** V8.1 Draft on the website for composition search, then manual SD/HD refinement; final typography in a layout tool.

**Draft direction to Conversational mode:**

```text
Explore 24 vertical poster compositions for an experimental astronomy festival. Use one luminous orbital ring above a dark horizon, cobalt and fluorescent coral, Swiss-modernist spacing, and reserve a clean upper-left title block. Do not render final copy.
```

**Approved refinement prompt:**

```text
experimental astronomy festival poster background, one luminous orbital ring suspended above a dark geometric horizon, cobalt black field with fluorescent coral glow, precise Swiss-modernist grid, clean upper-left rectangular area reserved for typography, dramatic scale contrast, subtle paper grain, no readable words --v 8.1 --hd --ar 2:3 --raw --s 140 --chaos 2 --no text, letters, logo, watermark, stars
```

**Why:** Draft selects hierarchy and palette, not detail; the refinement explicitly reserves a type zone; exact copy is omitted from generation.

**Expected result:** a typographically useful background with controlled negative space.

**Likely failures and response:** pseudo-glyphs → remove/repair them before layout; glow enters title block → region repair or choose another candidate; HD edit needed → accept that Editor downshifts to SD and upscale only after approval.

**Finish:** place the exact title and date as vector text; verify spelling, hierarchy, contrast, safe area, bleed, and print/export profile.

### Example 5 — migration and reproducibility audit

**Intent:** update a V6 campaign that used Character Reference and an old style-reference behavior without pretending outputs can be pixel-matched.

**Inputs:** archived prompts, V6 outputs, source character image, style image/code, `--cref`, `--cw`, model/version, seed, and rights records.

**Workflow:**

1. Reproduce one control with the original supported V6 settings where available; archive it as the baseline.
2. Create a V7 branch: replace `--cref`/`--cw` with one `--oref`/`--ow`, pin `--v 7`, switch to a verified Omni-compatible mode such as Relax on Standard+, and begin near `--ow 100–250` rather than copying `--cw` numerically.
3. Pin the old Style Reference behavior with `--sv 4` for the first comparison; then test current `--sv 6` as a separate branch.
4. Keep prompt, aspect ratio, stylize, reference files, and selection rubric constant. Do not use the same seed as proof of equivalence.
5. Score identity silhouette, costume colors, style palette, composition, anatomy, text/logo drift, and policy/rights compliance. Approve a new golden output and record that migration is perceptual, not deterministic.

**Example migrated prompt:**

```text
one fictional lighthouse keeper matching the authorized reference, walking along a windswept cliff path, navy wool coat, brass lantern in right hand, full figure, graphic gouache illustration, muted storm palette, broad simplified shapes --v 7 --ar 3:2 --s 160 --oref <AUTHORIZED_KEEPER_IMAGE_URL> --ow 180 --sref <AUTHORIZED_STYLE_IMAGE_URL> --sw 100 --sv 4 --chaos 2 --relax --no text, logo
```

**Failure conditions:** asserting the seed guarantees the old asset; leaving `--cref` in V7; changing `--sv`, model, prompt, and reference simultaneously; or approving without a rights/consent audit.

## First-party source ledger

All links below were checked 2026-07-09. Treat dates, defaults, prices, availability, limits, and policy language as volatile and re-check before consequential work.

- [Version and model lifecycle](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)
- [Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)
- [Prompt Basics](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics)
- [Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts)
- [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
- [Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
- [Character Reference](https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference)
- [Aspect Ratio](https://docs.midjourney.com/hc/en-us/articles/31894244298125-Aspect-Ratio), [Chaos](https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety), [Stylize](https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize), [Weird](https://docs.midjourney.com/hc/en-us/articles/32390120435085-Weird), [Quality](https://docs.midjourney.com/hc/en-us/articles/32176522101773-Quality), [Seeds](https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds), [Tile](https://docs.midjourney.com/hc/en-us/articles/32197978340109-Tile), [No](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No), and [Raw](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw)
- [Draft and Conversational Modes](https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes)
- [Editor](https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor), [Remix](https://docs.midjourney.com/hc/en-us/articles/32799074515213-Remix), [Vary Region](https://docs.midjourney.com/hc/en-us/articles/32794723105549-Vary-Region), [Pan](https://docs.midjourney.com/hc/en-us/articles/32570788043405-Pan), [Zoom Out](https://docs.midjourney.com/hc/en-us/articles/32595476770957-Zoom-Out), [Variations](https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations), and [Upscalers](https://docs.midjourney.com/hc/en-us/articles/32804058614669-Upscalers)
- [Text Generation](https://docs.midjourney.com/hc/en-us/articles/32502277092109-Text-Generation)
- [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization) and [Moodboards](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards)
- [Permutations](https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations) and [Repeat](https://docs.midjourney.com/hc/en-us/articles/32757107922061-Repeat)
- [Comparing Plans](https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans), [GPU Speed](https://docs.midjourney.com/hc/en-us/articles/32016412137741-GPU-Speed-Fast-Relax-Turbo), and [Info Command](https://docs.midjourney.com/hc/en-us/articles/32084927086861-Info-Command)
- [Stealth Mode](https://docs.midjourney.com/hc/en-us/articles/32019750070669-Stealth-Mode), [Keeping Creations Private](https://docs.midjourney.com/hc/en-us/articles/28014645615373-Keeping-Your-Creations-Private), and [Managing Image Uploads](https://docs.midjourney.com/hc/en-us/articles/33329380893325-Managing-Image-Uploads)
- [Terms of Service, effective 2026-05-27](https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service), [Community Guidelines](https://docs.midjourney.com/hc/en-us/articles/32013696484109-Community-Guidelines), [Commercial Use](https://docs.midjourney.com/hc/en-us/articles/27870375276557-Using-Images-Videos-Commercially), [Privacy Policy](https://docs.midjourney.com/docs/privacy-policy), and [Data Deletion and Privacy FAQ](https://docs.midjourney.com/hc/en-us/articles/32084462534541-Data-Deletion-and-Privacy-FAQ)
