---
name: black-forest-labs-flux
description: Plan, prompt, execute, troubleshoot, and quality-control Black Forest Labs FLUX image generation and editing across the BFL direct API and licensed local/open-weight deployments. Use for FLUX.2 model selection, text-to-image, single- or multi-reference editing, typography, exact-color work, mask-based erase/inpainting, outpainting, API integration, reproducibility, deployment licensing, and production rights or safety decisions; also use when migrating or maintaining legacy FLUX.1/FLUX1.1 workflows.
---

# Produce images with Black Forest Labs FLUX

Use this evidence notation throughout your work:

- **[Documented]** means BFL documentation, a BFL model card/repository, BFL legal terms, or a BFL-authored paper states the fact.
- **[Inference]** means a conclusion follows from documented facts but BFL does not state it directly.
- **[Heuristic]** means production advice to validate against actual outputs.

Treat all endpoint names, limits, prices, licenses, and terms as volatile. The facts below were verified **2026-07-09**. Recheck the current BFL API reference, release notes, model card, and governing license before a consequential run.

## Keep the execution surfaces separate

Identify the surface before selecting parameters or stating rights.

1. **BFL direct API** — requests go to an official `api.bfl.ai` endpoint with an `x-key`. BFL defines the request schema, moderation, billing, asynchronous result contract, and service terms. [Documented: D1, D2, D9]
2. **Third-party hosted gateway** — the gateway, not BFL's direct API, defines model slugs, accepted parameters, retention, moderation, pricing, and version pinning. Never assume a BFL field or limit works unchanged. Verify that provider's current documentation and contract. [Inference]
3. **Local/open-weight deployment** — weights and inference run on infrastructure under the checkpoint's own license. There is no automatic BFL API moderation, retention policy, or signed-result URL. Implement filtering, provenance, storage controls, and capacity planning yourself. [Documented: D10, D11]

Do not call every downloadable FLUX checkpoint “open source.” FLUX.2 [klein] 4B is Apache-2.0; FLUX.2 [klein] 9B and FLUX.2 [dev] are downloadable/open-weight but governed by the FLUX Non-Commercial License unless a commercial weights license applies. [Documented: D10]

## Select the family deliberately

### Current FLUX.2 paths

| Need | Choose | Surface and consequential facts |
|---|---|---|
| Most production generation/editing | **FLUX.2 [pro]** | BFL's recommended starting point. Direct endpoints include mutable `flux-2-pro-preview` and pinned `flux-2-pro`. Up to 8 references through the API and 10 in the BFL playground. [Documented: D1, D2] |
| Hardest edit, strongest adherence, highest final quality | **FLUX.2 [max]** | Direct API/Playground, up to 8 API references. It is the FLUX.2 path with grounding search. Use only when that quality or current-context feature justifies its cost. [Documented: D1, D2] |
| Typography, small-detail preservation, tunable sampling | **FLUX.2 [flex]** | Direct API. Exposes `guidance` 1.5–10 and `steps` 1–50; supports prompt upsampling and up to 8 API references. Higher guidance can trade realism for adherence. [Documented: D1, D2] |
| Latency-sensitive preview, interactive tool, high volume | **FLUX.2 [klein] 4B or 9B** | Direct API and downloadable weights; up to 4 references. No prompt upsampling, so write complete prompts. 4B is Apache-2.0; 9B is FLUX NCL unless separately licensed. [Documented: D1, D10] |
| Local customization or research with full sampling control | **FLUX.2 [dev]** or a **[klein] Base** checkpoint | Local/open-weight, not the BFL public API. BFL recommends at most 6 references for [dev]. Distilled klein is a short-step production path; Base variants retain full training signal for fine-tuning and diversity. Verify the exact checkpoint license. [Documented: D1, D10] |

Use a preview endpoint for current quality/speed only when a changing underlying snapshot is acceptable. Use a fixed endpoint for regression baselines, approvals, or compliance-sensitive reproducibility. The request contract may match while outputs change on preview. [Documented: D1, D12]

### Specialized and legacy paths

- Use **FLUX Erase** for mask-driven removal and background reconstruction. It uses a fixed erase instruction; the caller supplies no semantic prompt. [Documented: D7]
- Use **FLUX Outpainting** to extend a canvas. Its current direct endpoint offers `high` and `fast` modes. [Documented: D7]
- Use **FLUX.1 Fill [pro]** or licensed **Fill [dev]** when a black/white or alpha mask must be filled with specifically prompted content. It remains a legacy path in the current API reference. [Documented: D7, D10]
- Keep **FLUX.1 Kontext [pro]/[max]** for an already-approved or compatibility-bound iterative edit workflow. BFL recommends FLUX.2 for new projects. The BFL paper supports Kontext's unified generation/editing and evaluates multi-turn consistency, but that does not make it the current default. [Documented: D13]
- Keep **FLUX1.1 [pro]/Ultra/Raw**, FLUX.1 [dev]/[schnell], Depth, Canny, and Redux only when their specific legacy behavior, adapters, or deployed assets are required. Do not silently migrate a locked workflow; run a side-by-side acceptance test. [Documented: D9, D10]

## Convert the brief into a generation contract

Before prompting, record:

- final use, audience, territories, and whether the use is commercial;
- exact execution surface, endpoint/checkpoint, version strategy, and license;
- output count, size/aspect ratio, format, deadline, and cost ceiling;
- subject, action/state, environment, composition, style/medium, light, palette, and required text;
- non-negotiable identity/product/logo geometry and what may vary;
- each input image's owner, consent status, role, sensitivity, and permitted transformations;
- acceptance tests for text, color, identity, product geometry, factuality, and artifacts.

Stop if the model license, input rights, consent, or requested representation is unresolved. Do not interpret a provider accepting a request as clearance to publish it.

## Prompt from visible target state

Write natural-language prompts as a clear visual description. Front-load the highest-priority content. A useful ordering is:

`image type + subject + action/state + composition + environment + style/medium + lighting + palette + material/detail + required text`

This is an aid, not a mandatory formula. Add only details that change visible output. FLUX.2 supports very long prompts, but BFL advises starting short and adding useful specificity. [Documented: D3]

Use positive replacement language because most FLUX paths do not expose useful negative prompting. Replace “no people” with “an empty pedestrian plaza”; replace “no blur” with “sharp focus throughout.” [Documented: D4]

For a complex automated brief, pass a JSON-shaped string as the **prompt value**; do not invent an undocumented top-level JSON control schema. Useful prompt-internal keys include `scene`, `subjects`, `composition`, `camera`, `lighting`, `color_palette`, `style`, and `text`. FLUX interprets the structure as language. [Documented: D1, D5]

### Prompt upsampling

- On [pro]/[max], prompt upsampling is on by default; set `disable_pup: true` when wording must be used as written. [Documented: D2]
- On [flex], control it with `prompt_upsampling`. [Documented: D2]
- [klein] has no prompt upsampling. Supply the full visual direction yourself. [Documented: D4]
- **[Heuristic]** Disable upsampling for exact brand copy, tightly specified layouts, controlled A/B tests, and repair prompts; leave it on for broad ideation.

## Direct API operating pattern

For current FLUX.2 direct endpoints:

1. POST JSON with `prompt`, optional `input_image` through `input_image_8` (only through `_4` on klein), dimensions, optional `seed`, moderation setting, format, and optional webhook fields. Use only fields documented for that endpoint. [Documented: D2]
2. Capture `id`, `polling_url`, reported cost, input megapixels, and output megapixels.
3. Poll the returned URL until `Ready`; handle moderated, error, and task-not-found states explicitly. Do not poll forever.
4. Download the asset immediately. BFL's signed result URL is valid for 10 minutes. Store the original response, endpoint, prompt, parameters, input hashes, output hash, and timestamps. [Documented: D5, D9]
5. Never log API keys, raw sensitive input URLs, or webhook secrets. Authenticate webhook callbacks with the configured secret.

An optional `seed` supports reproducibility, but do not promise identical pixels across a changing preview endpoint, different gateway, different local runtime, or changed weights. [Documented + Inference: D1, D2]

## Build reference edits as explicit contracts

### Single reference

State both the edit and preservation constraints:

`Replace the paper label with a matte navy label in color #102A43. Keep the bottle silhouette, cap, glass reflections, camera angle, hand position, shadows, and background unchanged.`

Name exact old and new text in quotation marks. For example: `Replace "NORTH" with "EMBER"; retain the letter height, baseline, kerning character, embossing, and perspective.` BFL explicitly recommends quoted text and precise change/preservation language. [Documented: D5]

### Multiple references

Assign one role per image before writing the prompt:

| Input | Role example | Must preserve |
|---|---|---|
| image 1 | base composition | camera, background, scale |
| image 2 | product identity | silhouette, label geometry, material |
| image 3 | person identity | facial structure, hair, skin details |
| image 4 | wardrobe | cut, pattern, trim |
| image 5 | style reference | palette, contrast, texture only |

Then name those roles: `Use image 1 as the base scene; place the bottle from image 2 on the table; use the person from image 3 wearing the jacket from image 4; apply only the color grade and grain of image 5.` BFL recommends naming “image 1,” “image 2,” and each role. [Documented: D6]

Use the fewest references that carry independent information. Resolve contradictory pose, lighting, lens, identity, or style cues before generation. On the BFL direct API, current caps are 8 for [max]/[pro]/[flex], 4 for [klein], and a recommended 6 for local [dev]. The [pro] guide also documents a 9MP total input-plus-output budget, so increasing output resolution can reduce usable reference count. [Documented: D1, D6]

**[Heuristic]** Build a contact sheet with input index, role, crop, provenance, and hash. Run identity/product and style references separately first; combine only after each contract works.

## Control typography, color, and layout

### Typography

1. Prefer [flex] when embedded text and small design details dominate; use [max] for a hard final edit when maximum consistency matters. [Documented: D1, D2]
2. Put exact copy in quotes, near the front of the prompt.
3. Specify placement, hierarchy, size class, alignment, font character, color, and substrate: `Large centered headline "MOVE LIGHT" in condensed bold sans-serif, color #F7F3E8, printed flat on the upper third.` [Documented: D5]
4. Keep generated strings short. Generate headline, subhead, and CTA in separate passes if needed. [Documented + Heuristic: D5]
5. Proofread at 100–200% zoom. Check every glyph, number, punctuation mark, baseline, line break, and brand spelling.
6. **[Heuristic]** For legal copy, pricing, long body text, or accessibility-critical text, generate the visual plate and typeset final copy deterministically in a design/compositing tool.

### Color

Associate each hex code with a named object or component; do not provide an unattached palette and expect deterministic assignment. BFL documents object-bound hex steering. [Documented: D1, D5]

Example prompt fragment: `Bottle body: color #0B3D2E. Cap: color #F2C94C. Wordmark "MOSS": color #FFFFFF. Background: uniform color #E9E3D5.`

**[Heuristic]** Treat “exact color” as a steering claim, not proof of a color-managed deliverable. Sample multiple pixels in the final exported file, check color space/profile and compression, and correct in post when a brand tolerance is contractual.

### Composition and sampling

- Match width/height to intended framing before generation; do not rely on a later crop to repair composition. FLUX.2 direct endpoints accept flexible dimensions and output up to 4MP where documented. [Documented: D1, D4]
- Use [flex] guidance only when needed. Raise it in small increments for missed instructions; lower it when faces, materials, or light become synthetic. [Documented + Heuristic: D2]
- Increase [flex] steps only after the prompt and references are sound. More steps cannot resolve a contradictory brief. [Documented + Heuristic: D2]
- Keep seed, dimensions, endpoint, upsampling choice, and inputs fixed when testing one prompt change. Change one variable per diagnostic run. [Heuristic]

## Use mask-driven operations correctly

Choose the semantic operation, not just a model name:

- **Remove an object and reconstruct background:** use FLUX Erase. Supply same-size black/white PNG mask; white removes, black keeps. Start with documented `dilate_pixels: 10`, then enlarge for halos or soft edges. The current range is 0–25. [Documented: D7]
- **Fill a region with specified content:** use FLUX.1 Fill [pro] direct API or a properly licensed Fill [dev] checkpoint. Supply a same-size black/white mask (white=inpaint, black=preserve) or alpha mask, plus the target-state prompt. [Documented: D7]
- **Extend beyond borders:** use current FLUX Outpainting. Set target canvas and reference placement with `reference_offset_x` / `reference_offset_y`; decide whether `auto_crop` may crop an out-of-bounds placement or whether a 422 should stop the job. Choose `high` for detail/consistency and `fast` for speed on suitable scenes. Current `fast` mode requires base64 image input rather than an image URL, a placed reference at least 64 px on each side with aspect ratio no greater than 8:1, and canvas plus internal padding below 4 MP. Validate the exact current contract before execution. [Documented: D7]
- **Make an unmasked contextual change:** use FLUX.2 editing with an input image and explicit preserve list. [Documented: D5]

Inspect mask edges at full resolution. Include shadows, reflections, contact patches, and occluded parts when they belong to the removed object. Visible seams or halos are usually a mask/transition problem before they are a prompt problem. [Heuristic]

## Iterate by failure class

| Failure | Diagnose first | Repair action |
|---|---|---|
| Main subject or crop is wrong | Priority/order or aspect ratio | Front-load subject and framing; simplify context; set final dimensions. |
| Reference identities blend | Ambiguous roles or too many references | Label each image's role; remove redundant references; run identity and pose separately. |
| Unrequested areas drift | Edit instruction lacks invariants | Add a compact preserve list; make one local edit per pass; reuse the approved output only after QA. |
| Text is misspelled | Too much copy, poor hierarchy, wrong model | Switch to [flex] or [max]; quote and front-load shorter copy; typeset long text in post. |
| Brand color misses | Hex is not bound to an object or export altered it | Bind code to component; disable upsampling; sample output; correct in a color-managed post step. |
| [flex] looks overcooked | Guidance too high or prompt overloaded | Lower guidance; remove generic quality adjectives; preserve steps while testing. |
| Masked removal leaves halo | Mask excludes edge/shadow | Expand mask or `dilate_pixels`; include shadow/reflection; rerun Erase. |
| Inpaint seam or texture discontinuity | Tight mask or insufficient context | Feather/expand mask in the local pipeline; include surrounding material/light in prompt; inspect Fill limitations. |
| Multi-turn quality decays | Repeated re-encoding and cumulative drift | Return to the last approved master; branch edits; compare immutable regions; composite locally if practical. |
| API result disappears | Signed URL expired | Poll and download within 10 minutes; persist output immediately. |
| Same seed changes output | Preview/model/runtime changed | Pin endpoint/checkpoint and environment; store hashes; treat prior seed as only one part of provenance. |

Do not respond to every defect by adding adjectives. Reduce ambiguity, isolate variables, or change the tool/model when the failure class demands it.

## Run production QA

Reject or repair an output that fails any applicable gate:

- **Brief:** correct subject, action, count, setting, aspect ratio, composition, and emotional read.
- **Identity/product:** stable face, silhouette, proportions, package geometry, logo, materials, and distinguishing marks.
- **Editing:** requested pixels changed; protected content, framing, lighting, and shadows remain acceptably stable.
- **Typography:** exact copy, case, punctuation, glyph integrity, line breaks, hierarchy, and safe margins.
- **Color:** named component receives intended hex appearance; final file passes any measured tolerance after export.
- **Anatomy/physics:** hands, joints, reflections, contact shadows, perspective, occlusion, and repeated structures are plausible.
- **Technical:** required pixel dimensions, format, alpha, color profile, compression, and no seams, halos, banding, or unintended crop.
- **Series:** contact-sheet consistency across character/product, wardrobe, palette, lens, light, and style.
- **Rights/safety:** input rights and consent logged; no prohibited or misleading use; synthetic status disclosed where required; privacy and confidential-data handling approved.
- **Provenance:** endpoint/checkpoint, surface/provider, prompt, parameters, seed, input/output hashes, model/license version, date, and human approval retained.

For current or factual imagery, verify every depicted claim independently. FLUX.2 [max] grounding search is not a substitute for editorial fact-checking, source provenance, or permission to depict a real person/event. [Documented + Heuristic: D1, D11]

## Rights, privacy, and safety

- Confirm ownership or permission for every reference, logo, product image, likeness, style asset, and dataset. BFL requires users to respect third-party IP, privacy, and publicity rights. [Documented: D11]
- Obtain explicit authority for identifiable-person edits. Do not create non-consensual intimate imagery, harmful impersonation, harassment, privacy invasion, or deceptive “real event” imagery. [Documented: D11]
- Follow the current BFL Usage Policy, which restricts unlawful, abusive, surveillance/biometric, political-campaigning, harmful-personal-data, discriminatory high-impact, and misleading uses among others. [Documented: D11]
- Treat API input/output privacy as a contract question. BFL's published API terms grant BFL broad rights to use inputs and outputs to operate and improve services. Do not upload confidential, regulated, or client-sensitive material unless the applicable agreement and organizational policy permit it. [Documented: D11]
- BFL says it claims no ownership in outputs, but the user remains responsible for output use and third-party rights; output similarity and copyrightability remain jurisdiction- and fact-dependent. Do not promise exclusive rights. [Documented + Inference: D11]
- For self-hosting, apply the exact checkpoint license to **model use**. The published FLUX NCL permits compliant outputs to be used commercially but restricts using the model/derivatives for commercial or production purposes; do not run an NCL checkpoint as a paid product or production service without the necessary commercial weights license. Also implement the filtering or review and disclosure measures required by the license. [Documented: D10]
- Preserve AI disclosure and provenance. The official FLUX.2 repository recommends invisible watermarking and C2PA-style metadata; do not strip required provenance. [Documented: D10]

## Complete examples

### Example 1 — Direct API product key visual

**Intent:** Create a 4:5 campaign master with controlled brand color and a short headline.

**Selection:** BFL direct `flux-2-pro` for a pinned production snapshot. Use [flex] instead if typography repeatedly fails; use [max] only after the prompt is proven and the final-quality benefit is needed.

**Complete prompt:**

```text
Premium studio product photograph of one reusable aluminum water bottle, centered slightly below frame with generous clean space above. Bottle body strictly color #0B3D2E, cap strictly color #F2C94C, small white wordmark "MOSS" printed horizontally on the front. The large headline "MOVE LIGHT" appears above the bottle in bold condensed sans-serif, color #0B3D2E, exact spelling and two words on one line. Warm off-white seamless background color #E9E3D5. Soft diffused key light from upper left, subtle grounded shadow to lower right, crisp product edges, realistic brushed aluminum, 85mm studio product photography, straight-on camera, no perspective distortion.
```

**Complete request and retrieval pattern:**

```python
import hashlib, json, os, time, requests
from datetime import datetime, timezone
from pathlib import Path

PROMPT = """Premium studio product photograph of one reusable aluminum water
bottle, centered slightly below frame with generous clean space above. Bottle
body strictly color #0B3D2E, cap strictly color #F2C94C, small white wordmark
"MOSS" printed horizontally on the front. The large headline "MOVE LIGHT"
appears above the bottle in bold condensed sans-serif, color #0B3D2E, exact
spelling and two words on one line. Warm off-white seamless background color
#E9E3D5. Soft diffused key light from upper left, subtle grounded shadow to
lower right, crisp product edges, realistic brushed aluminum, 85mm studio
product photography, straight-on camera, no perspective distortion."""

headers = {
    "x-key": os.environ["BFL_API_KEY"],
    "Content-Type": "application/json",
    "accept": "application/json",
}
payload = {
    "prompt": PROMPT,
    "disable_pup": True,
    "width": 1280,
    "height": 1600,
    "seed": 240709,
    "safety_tolerance": 2,
    "output_format": "png",
}
job = requests.post(
    "https://api.bfl.ai/v1/flux-2-pro", headers=headers, json=payload, timeout=60
)
job.raise_for_status()
meta = job.json()
manifest = {
    "submitted_at": datetime.now(timezone.utc).isoformat(),
    "endpoint": "https://api.bfl.ai/v1/flux-2-pro",
    "request": payload,
    "submission_response": meta,
}
Path("moss-key-visual.manifest.json").write_text(
    json.dumps(manifest, indent=2), encoding="utf-8"
)

deadline = time.monotonic() + 300
while time.monotonic() < deadline:
    result = requests.get(meta["polling_url"], headers=headers, timeout=30)
    result.raise_for_status()
    body = result.json()
    if body.get("status") == "Ready":
        download = requests.get(body["result"]["sample"], timeout=60)
        download.raise_for_status()
        output_path = Path("moss-key-visual.png")
        output_path.write_bytes(download.content)
        manifest.update({
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "retrieval_response": body,
            "output_sha256": hashlib.sha256(download.content).hexdigest(),
            "output_path": str(output_path),
        })
        Path("moss-key-visual.manifest.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )
        break
    if body.get("status") in {"Error", "Request Moderated", "Content Moderated", "Task not found"}:
        raise RuntimeError(body)
    time.sleep(0.75)
else:
    raise TimeoutError(meta["id"])
```

**Why:** The pinned endpoint supports regression review; upsampling is disabled to protect copy/layout; every hex is bound to a component; dimensions match the delivery ratio.

**Expected result:** One bottle, correct component colors, clean space, short readable headline, grounded product lighting.

**Likely failures and recovery:** If headline glyphs fail, switch to [flex] with the same prompt, `guidance: 4.5`, and `steps: 40`, then typeset in post if still imperfect. If color misses, verify the exported PNG and correct in a color-managed step.

**Variation:** Remove the headline clause and generate a clean plate for deterministic downstream typography.

### Example 2 — Multi-reference campaign composite

**Intent:** Place a known product with a known person in a new scene while borrowing only a style grade.

**Inputs:** image 1 base room; image 2 approved bottle packshot; image 3 consented person; image 4 pose; image 5 color-grade reference. Record provenance and hashes.

**Selection and parameters:** BFL direct `flux-2-flex`; `1280×1600`; `prompt_upsampling: false`; `guidance: 4.5`; `steps: 40`; fixed seed; PNG.

**Complete prompt:**

```text
Use image 1 as the base room and preserve its camera position, architecture, furniture, and window light. Place the exact bottle from image 2 upright on the front-right table; preserve its silhouette, cap, label geometry, wordmark, and brushed-aluminum material. Use the exact adult person from image 3 in the body pose from image 4, standing behind the table; preserve facial structure, hair, skin details, and body proportions. Apply only the muted olive-and-amber color grade and fine film grain from image 5; do not import its objects or composition. The person looks toward the bottle with a relaxed expression. Maintain realistic scale, contact shadows, reflections, occlusion, and a coherent 50mm photographic perspective. Keep all existing room objects unchanged.
```

**Payload-specific mapping:** `input_image`=image 1, `input_image_2`=image 2, through `input_image_5`=image 5. Do not call these “style images” in metadata when their actual roles differ.

**Expected result:** Room and person identity remain stable; product geometry and logo remain recognizable; pose and grade transfer without foreign objects.

**Likely failures and recovery:** If identity blends with the pose reference, crop image 4 to a faceless silhouette or replace it with a non-identifying pose guide. If product text drifts, create the scene without the product and composite the approved packshot, or run a targeted single-reference repair.

**Variation:** For fast previews, test [klein] with at most four references by removing the grade reference and expressing the grade in text; do not assume preview acceptance predicts final [flex] fidelity.

### Example 3 — Mask operation decision

**Intent:** Remove a microphone and reconstruct the wall, then place a small framed print in a different version.

**Removal branch:** Use `POST /v1/flux-tools/erase-v1`. Supply the photo and same-size binary PNG mask as base64; white covers microphone, cable, contact shadow, and wall reflection; black preserves everything else. Start `dilate_pixels: 10`, `output_format: "png"`. No prompt is sent.

**Prompted inpaint branch:** Use legacy `POST /v1/flux-pro-1.0-fill` only for the framed-print version. Use the same mask convention and prompt:

```text
A small thin black metal picture frame centered on this wall region, containing a simple cream paper print with one dark green circle, matching the existing wall perspective and warm side lighting, realistic contact shadow, preserve all unmasked pixels.
```

Set `steps: 40`, `guidance: 35`, `prompt_upsampling: false`, fixed seed, PNG. These parameters belong to FLUX.1 Fill; do not copy them to FLUX.2 [flex].

**Expected result:** Erase version contains coherent wall texture; Fill version contains one perspective-correct frame; unmasked content stays stable.

**Likely failures and recovery:** A halo means the mask/dilation missed edges. A texture seam means more transition context is needed. An incorrect frame is a Fill prompt/mask problem, not a reason to send semantic text to Erase.

## Sources

All volatile source checks below were performed 2026-07-09.

- **D1 — BFL model scope and selection:** [FLUX.2 overview](https://docs.bfl.ai/flux_2/flux2_overview), [BFL model catalog](https://bfl.ai/models), [release notes](https://docs.bfl.ai/release-notes).
- **D2 — Direct API schemas:** [FLUX.2 max](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bmax%5D), [pro](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bpro%5D), [flex](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bflex%5D), and [klein 4B](https://docs.bfl.ai/api-reference/models/generate-or-edit-an-image-with-flux2-%5Bklein%5D-4b).
- **D3 — Prompt construction:** [Prompting basics](https://docs.bfl.ai/guides/prompting_unified_basics), [building a good prompt](https://docs.bfl.ai/guides/prompting_unified_building).
- **D4 — Parameters and positive prompting:** [Technical parameters](https://docs.bfl.ai/guides/prompting_unified_technical), [prompt reference](https://docs.bfl.ai/guides/prompting_unified_reference).
- **D5 — Typography, color, and single-reference editing:** [Style, aesthetics and text](https://docs.bfl.ai/guides/prompting_unified_style), [single-reference editing](https://docs.bfl.ai/guides/prompting_editing_single_reference), [FLUX.2 prompting guide](https://docs.bfl.ai/guides/prompting_guide_flux2).
- **D6 — Multi-reference limits and methods:** [Image editing overview](https://docs.bfl.ai/guides/prompting_editing_overview), [multi-reference editing](https://docs.bfl.ai/guides/prompting_editing_multi_reference).
- **D7 — Mask and canvas tools:** [FLUX Erase](https://docs.bfl.ai/flux_tools/flux_erase), [FLUX Outpainting](https://docs.bfl.ai/flux_tools/flux_outpainting), [FLUX.1 Fill API](https://docs.bfl.ai/api-reference/models/inpaint-an-image-with-flux1-fill-%5Bpro%5D-using-an-input-image-and-mask), [FLUX.1 Fill dev model card](https://huggingface.co/black-forest-labs/FLUX.1-Fill-dev).
- **D8 — Architecture/research context:** [FLUX.2 official inference repository](https://github.com/black-forest-labs/flux2), [FLUX.2 representation research index](https://bfl.ai/research/representation-comparison).
- **D9 — API lifecycle:** [FLUX.2 text-to-image](https://docs.bfl.ai/flux_2/flux2_text_to_image), [FLUX.2 image editing](https://docs.bfl.ai/flux_2/flux2_image_editing), [get-result schema](https://docs.bfl.ai/api-reference/utility/get-result).
- **D10 — Weights and licenses:** [FLUX.2 klein 4B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B), [klein 9B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B), [FLUX.2 dev model card](https://huggingface.co/black-forest-labs/FLUX.2-dev), [FLUX non-commercial terms](https://bfl.ai/legal/non-commercial-license-terms), [commercial weights licensing](https://bfl.ai/licensing), [official FLUX.1 repository/model table](https://github.com/black-forest-labs/flux).
- **D11 — Rights and safety:** [BFL Usage Policy](https://bfl.ai/legal/usage-policy), [FLUX API Service Terms](https://bfl.ai/legal/flux-api-service-terms), [Website and FLUX Terms](https://bfl.ai/legal/terms-of-service), [Intellectual Property Policy](https://bfl.ai/legal/intellectual-property-policy).
- **D12 — Endpoint volatility:** [BFL release notes](https://docs.bfl.ai/release-notes).
- **D13 — Previous-generation context:** [FLUX.1 Kontext overview](https://docs.bfl.ai/kontext/kontext_overview), [Kontext editing guide](https://docs.bfl.ai/kontext/kontext_image_editing), [FLUX.1 Kontext paper](https://arxiv.org/abs/2506.15742).
