---
name: openai-gpt-image
description: Generate, edit, composite, stream, and production-review still images with OpenAI GPT Image models. Use when an agent must choose between GPT Image 2 and legacy GPT Image/DALL-E integrations, select the Image API or Responses API, build prompts and reference-image workflows, use masks or multiple inputs, preserve identity or brand details, render in-image text, handle output files and partial images, estimate cost and rate limits, migrate deprecated image code, or apply OpenAI image safety, consent, privacy, provenance, and rights requirements. Do not use for OpenAI video or audio generation.
---

# Produce still images with OpenAI GPT Image

Use this skill for OpenAI still-image generation and editing. Do not route video, animation, speech, transcription, or music work through it.

## Read claims by evidence label

- **Documented fact** means OpenAI currently documents the behavior.
- **Production heuristic** means a practical workflow recommendation derived from documented behavior and production risk, not an API guarantee.
- **Inference** means a reasoned conclusion that must be validated on the actual workload.

Treat model names, prices, limits, supported parameters, regional availability, policy, and lifecycle dates as volatile. Recheck the linked official source immediately before building or quoting them to a user. The volatile facts below were verified **2026-07-09**.

## Start with the current lifecycle, not remembered model names

**Documented facts, verified 2026-07-09:**

| Model | Current role | Lifecycle / migration action |
|---|---|---|
| `gpt-image-2` | Current production default for generation and editing; alias plus snapshot `gpt-image-2-2026-04-21` | Use the alias for automatic updates or the snapshot when regression stability is required. |
| `gpt-image-1.5` | Previous model | Deprecated; scheduled API removal **2026-12-01**. Migrate to `gpt-image-2`. |
| `gpt-image-1` | Previous model | Deprecated; scheduled API removal **2026-10-23**. Migrate to `gpt-image-2`. |
| `gpt-image-1-mini` | Cost-efficient GPT Image 1 variant | Deprecated; scheduled API removal **2026-12-01**. Do not begin a new dependency on it; test `gpt-image-2` with `quality="low"`. |
| `dall-e-3`, `dall-e-2` | Legacy migration knowledge only | Deprecated and removed from the API **2026-05-12**. Replace, do not select. |

Sources: [GPT Image 2 model page](https://developers.openai.com/api/docs/models/gpt-image-2), [all-model catalog](https://developers.openai.com/api/docs/models/all), [deprecations](https://developers.openai.com/api/docs/deprecations).

**Production heuristic:** Default new work to `gpt-image-2`. Keep a deprecated GPT Image model only long enough to run a measured migration comparison against existing prompts. Do not choose a deprecated model merely because its per-image table appears cheaper.

**Production heuristic:** When repeatability matters, test and pin `gpt-image-2-2026-04-21`; when receiving ongoing improvements matters more, use `gpt-image-2`. Record the exact identifier, endpoint, parameters, prompt, source-image hashes, and output metadata in the asset ledger.

## Choose the surface deliberately

### Use the Image API for a direct operation

Use `POST /v1/images/generations` for text-to-image and `POST /v1/images/edits` for an edit, composite, reference-driven generation, or masked edit. Select the GPT Image model explicitly.

Choose this surface when the request is one operation, the application owns iteration state, or exact model selection is important. The API returns base64 image data for GPT Image models.

### Use the Responses API for a conversational image workflow

Use a mainline model that supports the built-in `image_generation` tool, then set the tool-level `model` to `gpt-image-2`. These are separate choices: the top-level Responses `model` reasons and orchestrates, while `tools[].model` selects the image model. Use `previous_response_id`, an image-generation call ID, a file ID, URL, or data URL to carry image context between turns. Use `action: "auto"`, `"generate"`, or `"edit"` to control intent; forcing `edit` without an image in context errors.

Choose this surface when the model should reason across conversation turns, mix text and image inputs, or apply successive high-fidelity changes. Inspect and log the tool call's `revised_prompt`. Account for mainline-model token charges in addition to image-generation charges.

**Critical distinction:** Do not pass `gpt-image-2` as the top-level Responses `model`. Select a current mainline model whose model page lists Image generation as a supported tool, and independently set `tools[].model="gpt-image-2"`. Omitting the tool-level selector can fall back to the schema's older default.

**Documented fact:** Both surfaces support streaming partial images. `partial_images` accepts `0` through `3`; the final image may arrive before every requested partial. Each partial costs an additional 100 image output tokens. Streaming is a sequence of previews plus a final result, not a substitute for final-image QA.

**Documented boundary:** The current image guide documents request/response and server-sent-event streaming, not a dedicated image job-ID/polling endpoint. The model and pricing pages list Batch support and Batch pricing for GPT Image 2, but verify the current Batch endpoint target contract before designing an asynchronous bulk system. Do not invent an image polling API.

Sources: [image generation guide](https://developers.openai.com/api/docs/guides/image-generation), [Images API reference](https://platform.openai.com/docs/api-reference/images), [image streaming reference](https://platform.openai.com/docs/api-reference/images-streaming), [Responses API](https://developers.openai.com/api/docs/guides/responses-vs-chat-completions).

## Run a production decision pass before generating

1. Confirm the deliverable: use, audience, aspect ratio or exact dimensions, required copy, brand or character invariants, number of variants, deadline, and review owner.
2. Confirm rights and consent for every input image, logo, person, character, artwork, and reference. Do not upload unnecessary personal or confidential material.
3. Recheck the model page, image guide, pricing, deprecations, and policies if the result will be customer-facing or costly.
4. Pick the API surface. Use Image API for one direct operation; use Responses for conversational reasoning and iterative state.
5. Pick parameters from the required output, not habit. Use a low-quality draft for composition testing, then promote only approved candidates.
6. Write the prompt as a production specification. Name what changes, what stays invariant, and how success will be reviewed.
7. Generate the smallest useful sample. Never silently turn sample approval into a large batch.
8. Save the final bytes immediately, preserve provenance where possible, and record response/request identifiers and usage.
9. Review against exact copy, factual claims, identity, geometry, brand details, composition, and safety before delivery.

## Control GPT Image 2 with current parameters

### Dimensions and quality

**Documented facts for the Images API, verified 2026-07-09:** `gpt-image-2` accepts `size="auto"` or any resolution satisfying all of these constraints:

- maximum edge at most `3840` pixels;
- both edges multiples of `16`;
- long-edge to short-edge ratio at most `3:1`;
- total pixels from `655,360` through `8,294,400`.

Common valid sizes include `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `3840x2160`, and `2160x3840`. Outputs above `2560x1440` total-pixel territory are documented as experimental and may vary more. Square is typically fastest.

The Responses `image_generation` tool has a narrower live schema: use `auto`, `1024x1024`, `1024x1536`, or `1536x1024`. Do not copy an arbitrary Images-API resolution into a Responses tool call without rechecking that schema.

Use `quality="low"`, `"medium"`, `"high"`, or `"auto"`.

- **Production heuristic:** Use `low` to test concept, layout, crop, and throughput.
- **Production heuristic:** Compare `medium` and `high` on small or dense text, close faces, identity-sensitive edits, intricate diagrams, and final high-resolution assets.
- **Production heuristic:** Do not assume high quality repairs a contradictory prompt or exact layout. Fix the specification first.

### Output format and background

GPT Image returns base64 data. `output_format` is `png` by default and can be `jpeg` or `webp`. For JPEG or WebP, set `output_compression` from `0` to `100`; current documentation says JPEG is faster than PNG.

**Documented fact:** `gpt-image-2` does **not** currently support transparent backgrounds. Do not send `background="transparent"` to it. Use `background="opaque"` or `"auto"`, generate against a clean contrasting matte, and use a downstream background-removal process if alpha is required.

Older GPT Image endpoint contracts offered transparent output where supported, with PNG or WebP required, but those models are deprecated. Do not start a legacy dependency solely for transparency.

### Multiplicity, moderation, and user identity

- `n` defaults to `1`; the Images endpoint contract allows `1` through `10`. Generate only as many variants as the approved sample/batch plan requires.
- `moderation="auto"` is standard filtering; `moderation="low"` is less restrictive filtering. It does not disable policy or output checks.
- Pass an end-user identifier through the supported `user` field when appropriate for abuse monitoring. Do not place raw personal data in it; use a stable pseudonymous identifier.
- Complex prompts may take up to two minutes. Handle client timeouts and rate limits explicitly.

### Image inputs and fidelity

The edits endpoint accepts one or more reference images; the current endpoint reference documents up to 16 PNG, WebP, or JPEG inputs under 50 MB each for GPT Image workflows. In Responses, inputs can be fully qualified URLs, base64 data URLs, or Files API IDs created with `purpose="vision"`.

**Current-guide rule:** `gpt-image-2` processes every image input at high fidelity automatically, so omit `input_fidelity`. This can increase input-image token cost. As of the verification date, the exact Images edit and Responses schemas still describe `input_fidelity` for GPT Image 1, 1.5, “and later,” which conflicts with the core GPT Image 2 guide. Prefer the model-specific guide's omission in new code, and recheck the exact endpoint schema if this conflict is resolved.

For migration only, `gpt-image-1.5` and `gpt-image-1` expose low/high input-fidelity behavior. `gpt-image-1-mini` does not support high input fidelity in the endpoint contract. Do not copy legacy `input_fidelity="high"` into GPT Image 2 code. Some older first-party cookbook snippets still do so; follow the current core image guide.

### Masks

A mask guides which area to change. For GPT Image, masking remains prompt-based and may not follow the contour exactly. With multiple inputs, the mask applies to the first image.

Input images may be PNG, WebP, or JPEG, up to 16 files under 50 MB each. The mask has a narrower contract: it must be a PNG under 4 MB, include an alpha channel, and match the first input image's dimensions. The mask does not need to share a JPEG/WebP source's format. Fully transparent mask areas indicate where editing is allowed. Validate mask type, byte size, dimensions, and alpha locally before paying for a call.

**Production heuristic:** Include both an edit instruction and an invariant list even when a mask is present. Never promise pixel-exact inpainting; compare changed pixels outside the intended area and reject drift.

Sources: [image generation guide: edits, masks, fidelity, and output](https://developers.openai.com/api/docs/guides/image-generation), [Images edit endpoint schema](https://developers.openai.com/api/reference/resources/images/methods/edit).

## Write prompts as visual specifications

Use whichever syntax is easiest to maintain. Clarity matters more than a magical keyword sequence. For complex work, order the prompt as:

1. intended deliverable and use;
2. background or scene;
3. primary subject and action;
4. composition, viewpoint, and negative space;
5. medium, material, lighting, color, and finish;
6. exact text and typography;
7. change list and invariant list;
8. exclusions and acceptance criteria.

**Documented prompting guidance:** Be concrete about materials, shapes, textures, and medium. State framing, angle, placement, lighting, and mood. For a photorealistic result, say `photorealistic` or describe a real-photo capture. Treat detailed camera settings as high-level look guidance, not exact physical simulation.

### Make text testable

- Put exact copy in quotes and label it `EXACT, verbatim`.
- Say how many times it appears and prohibit extra copy.
- Specify hierarchy, placement, font category, weight, contrast, and line breaks.
- For uncommon spellings, provide a character-by-character spelling cue.
- Use medium or high quality for small text, dense panels, or multiple fonts.
- Inspect the rendered image; improved text rendering is not guaranteed perfect. For legal copy or typography that must be exact, generate the art without text and typeset downstream.

### Make edits surgical

Use: `Change only X. Preserve A, B, C. Keep everything else unchanged.` Repeat critical invariants on every iteration. Lock identity, pose, body geometry, camera angle, crop, lighting direction, shadows, background objects, logos, and label copy as needed.

### Make multiple inputs unambiguous

Index and name inputs: `Image 1: base room; Image 2: chair reference; Image 3: fabric reference.` State the operation between them, placement, scale, perspective, lighting, occlusion, and which image controls the unchanged background. Do not rely on input order alone.

### Iterate one variable at a time

Start with a clean base prompt. Change one controllable property per follow-up, such as crop, warmth, copy, or one object. Save every accepted intermediate. When drift appears, return to the last accepted image instead of editing a degraded descendant.

Source: [OpenAI GPT Image prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide).

## Example 1 — Complete direct generation with output handling

**Example, not a mandatory formula.** Intent: create two customer-facing poster candidates, save exact bytes, and record request metadata. Prerequisites: `pip install --upgrade openai`; set `OPENAI_API_KEY`.

```python
import base64
import json
from pathlib import Path

from openai import OpenAI

client = OpenAI()
out_dir = Path("outputs/poster")
out_dir.mkdir(parents=True, exist_ok=True)

prompt = """
Deliverable: vertical launch poster for an original neighborhood astronomy club.
Scene: deep navy night sky above a small hilltop observatory; two adults and one child
silhouetted at a telescope; generous dark negative space in the upper third.
Style: refined screen-print illustration, limited palette of navy, cream, and coral,
crisp paper texture, high contrast, no photorealism.
Copy (EXACT, verbatim, once only):
"SEE FARTHER TOGETHER"
Typography: bold geometric sans-serif, cream, centered in the upper third, clean kerning.
Constraints: original design; no existing logos, trademarks, watermarks, or extra text.
Acceptance: readable at phone size; all figures anatomically coherent; telescope intact.
""".strip()

result = client.images.generate(
    model="gpt-image-2",
    prompt=prompt,
    size="1024x1536",
    quality="medium",
    output_format="png",
    background="opaque",
    moderation="auto",
    n=2,
)

for index, item in enumerate(result.data, start=1):
    (out_dir / f"candidate-{index}.png").write_bytes(
        base64.b64decode(item.b64_json)
    )

metadata = {
    "model": "gpt-image-2",
    "request_id": getattr(result, "_request_id", None),
    "size": "1024x1536",
    "quality": "medium",
    "output_format": "png",
    "background": "opaque",
    "prompt": prompt,
    "count": len(result.data),
}
(out_dir / "request.json").write_text(
    json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
)
```

Expected result: two opaque PNG candidates. Review exact copy, small-size legibility, extra text, edge crop, hands, and telescope geometry. Likely failures: misspelled copy, duplicate slogan, over-detailed silhouettes, or insufficient negative space. Variation: start with `quality="low"` for composition approval, then regenerate the selected direction at medium/high.

## Example 2 — Complete multi-reference masked edit

**Example, not a mandatory formula.** Intent: replace only a chair in a room while using a product reference. Required local files: `room.png` (base image), `chair-reference.png`, and `mask.png`. The mask must be a PNG under 4 MB, match `room.png` dimensions, and include alpha; its transparent area should cover the replaceable chair.

```python
import base64
from contextlib import ExitStack
from pathlib import Path

from openai import OpenAI

client = OpenAI()
output = Path("outputs/room-chair-edit.png")
output.parent.mkdir(parents=True, exist_ok=True)

prompt = """
Image 1 is the base room and must control the camera, architecture, crop, and background.
Image 2 is the chair reference and controls the replacement chair's design and material.
Change only the chair inside the masked area of Image 1. Replace it with the chair from
Image 2 at believable scale and perspective. Match the room's light direction, color
temperature, contact shadow, and floor reflection.
Preserve exactly: walls, windows, flooring, rug, table, plants, camera angle, crop,
exposure, white balance, and every object outside the masked area.
Add no text, people, decor, logos, or watermarks.
""".strip()

with ExitStack() as stack:
    room = stack.enter_context(open("room.png", "rb"))
    chair = stack.enter_context(open("chair-reference.png", "rb"))
    mask = stack.enter_context(open("mask.png", "rb"))
    result = client.images.edit(
        model="gpt-image-2",
        image=[room, chair],
        mask=mask,
        prompt=prompt,
        size="1536x1024",
        quality="high",
        output_format="png",
        background="opaque",
        moderation="auto",
    )

output.write_bytes(base64.b64decode(result.data[0].b64_json))
print(f"saved {output}; request_id={getattr(result, '_request_id', None)}")
```

Expected result: a plausible chair replacement with the room intact. Review a difference image outside the mask, chair identity, scale, shadow, and floor contact. Likely failures: mask-edge halos, changes outside the mask, chair redesign, altered crop, or inconsistent lighting. Repair by tightening the invariant list and mask, then edit from the original base rather than the failed result.

## Example 3 — Complete conversational generation and follow-up edit

**Example, not a mandatory formula.** Intent: use Responses so the mainline model maintains a visual conversation. This example creates an image, logs the revised prompt, then applies one follow-up change.

```python
import base64
import json
from pathlib import Path

from openai import OpenAI

client = OpenAI()
out_dir = Path("outputs/conversation")
out_dir.mkdir(parents=True, exist_ok=True)

first = client.responses.create(
    model="gpt-5.5",
    store=True,  # Intentional: previous_response_id below depends on retained response state.
    input=(
        "Create a 1024x1024 editorial illustration for an article about urban heat. "
        "Show the same city block split into two readable halves: treeless asphalt on "
        "the left and shaded trees with a cool pedestrian area on the right. "
        "Flat cut-paper style, no text, no logos, no watermark."
    ),
    tools=[{
        "type": "image_generation",
        "model": "gpt-image-2",
        "action": "generate",
        "size": "1024x1024",
        "quality": "medium",
        "output_format": "png",
        "background": "opaque",
        "moderation": "auto",
    }],
)

first_calls = [x for x in first.output if x.type == "image_generation_call"]
if not first_calls:
    raise RuntimeError("No image_generation_call returned")
out_dir.joinpath("urban-heat-v1.png").write_bytes(
    base64.b64decode(first_calls[0].result)
)

second = client.responses.create(
    model="gpt-5.5",
    store=True,
    previous_response_id=first.id,
    input=(
        "Edit the existing illustration only: make the right-side tree canopy broader "
        "and add two bicycles under it. Preserve the split layout, buildings, palette, "
        "camera, cut-paper style, and the entire left half. Add no text."
    ),
    tools=[{
        "type": "image_generation",
        "model": "gpt-image-2",
        "action": "edit",
        "size": "1024x1024",
        "quality": "medium",
        "output_format": "png",
        "background": "opaque",
        "moderation": "auto",
    }],
)

second_calls = [x for x in second.output if x.type == "image_generation_call"]
if not second_calls:
    raise RuntimeError("No follow-up image_generation_call returned")
out_dir.joinpath("urban-heat-v2.png").write_bytes(
    base64.b64decode(second_calls[0].result)
)

out_dir.joinpath("tool-calls.json").write_text(json.dumps({
    "first_response_id": first.id,
    "first_call_id": first_calls[0].id,
    "first_revised_prompt": first_calls[0].revised_prompt,
    "second_response_id": second.id,
    "second_call_id": second_calls[0].id,
    "second_revised_prompt": second_calls[0].revised_prompt,
}, indent=2), encoding="utf-8")
```

Expected result: an initial square illustration and an edited descendant. Likely failures: left-half drift, extra objects, or a new composition instead of an edit. Repair by retaining `action="edit"`, naming invariants, and reverting to the accepted response/image when drift accumulates.

This example intentionally accepts Responses application-state retention so `previous_response_id` can carry the first tool call. For confidential work, make the retention decision before choosing this pattern; `store=false` is not equivalent to approved Zero Data Retention and requires carrying context another supported way.

## Example 4 — Complete Image API partial-image stream

**Example, not a mandatory formula.** Intent: show progressive previews while saving the final image separately. Do not ship a partial as the final asset.

```python
import base64
from pathlib import Path

from openai import OpenAI

client = OpenAI()
out_dir = Path("outputs/stream")
out_dir.mkdir(parents=True, exist_ok=True)

stream = client.images.generate(
    model="gpt-image-2",
    prompt=(
        "A wide editorial still life of translucent blue glass laboratory vessels "
        "casting crisp cyan shadows on warm cream paper, top-down, no text or logos."
    ),
    size="1536x1024",
    quality="medium",
    output_format="jpeg",
    output_compression=90,
    background="opaque",
    stream=True,
    partial_images=2,
)

final_written = False
for event in stream:
    if event.type == "image_generation.partial_image":
        path = out_dir / f"preview-{event.partial_image_index}.jpg"
        path.write_bytes(base64.b64decode(event.b64_json))
        print(f"preview: {path}")
    elif event.type == "image_generation.completed":
        path = out_dir / "final.jpg"
        path.write_bytes(base64.b64decode(event.b64_json))
        print(f"final: {path}; usage={event.usage}")
        final_written = True

if not final_written:
    raise RuntimeError("Stream ended without image_generation.completed")
```

Expected behavior: zero to two preview files and exactly one final file. A fast generation may yield fewer previews. Budget for 100 extra image output tokens per partial.

## Handle failures by class

- Retry transient `429` and `5xx` failures with bounded exponential backoff and jitter. Respect rate-limit headers; log the request ID.
- Do not automatically retry `image_generation_user_error` without changing the request.
- Branch first on `error.code == "moderation_blocked"`. Treat `moderation_details` as optional; its stage may be `input`, `output`, or `unknown`, and its categories are coarse debugging labels. Give end users a generic message and use details only for safe remediation and logs.
- Never evade a safety block by obfuscating the same request or toggling moderation. Offer a compliant reformulation that changes the harmful intent.
- If text is wrong, shorten copy, increase hierarchy and quality, or typeset downstream.
- If an edit drifts, return to the last accepted source, reduce the change surface, name invariants, and use a tighter alpha mask.
- If multiple references blend, identify every input by index and assign one role to each.
- If the output crops badly, specify framing, safe margins, and negative-space location; test the actual delivery ratio.
- If a requested GPT Image 2 transparent background fails, use opaque generation plus downstream background removal.

## Estimate cost and capacity before batch work

**Documented pricing, verified 2026-07-09; prices per one million tokens:**

| Model | Standard text input | Standard image input / cached | Standard image output | Batch text input | Batch image input / cached | Batch image output |
|---|---:|---:|---:|---:|---:|---:|
| `gpt-image-2` | $5.00 | $8.00 / $2.00 | $30.00 | $2.50 | $4.00 / $1.00 | $15.00 |
| `gpt-image-1.5` | $5.00 | $8.00 / $2.00 | $32.00 | $2.50 | $4.00 / $1.00 | $16.00 |
| `gpt-image-1-mini` | $2.00 | $2.50 / $0.25 | $8.00 | $1.00 | $1.25 / $0.13 | $4.00 |

The current guide's output-only GPT Image 2 examples for common sizes are:

| Quality | `1024x1024` | `1024x1536` | `1536x1024` |
|---|---:|---:|---:|
| low | $0.006 | $0.005 | $0.005 |
| medium | $0.053 | $0.041 | $0.041 |
| high | $0.211 | $0.165 | $0.165 |

Add prompt text, input-image tokens, Responses mainline-model usage, streaming partials, retries, and downstream processing. Do not estimate a reference-heavy edit from output cost alone. High-fidelity GPT Image 2 inputs can dominate edit cost.

`gpt-image-1` legacy pricing is $5.00/M text input, $10.00/M image input, and $40.00/M image output; use only for migration accounting because its shutdown is scheduled.

**Documented GPT Image 2 rate limits, verified 2026-07-09:** Free unsupported; Tier 1 `100,000 TPM / 5 IPM`; Tier 2 `250,000 / 20`; Tier 3 `800,000 / 50`; Tier 4 `3,000,000 / 150`; Tier 5 `8,000,000 / 250`. Usage tiers change and may increase with spend, so recheck the model page.

Sources: [API pricing](https://developers.openai.com/api/docs/pricing), [image cost calculator and tables](https://developers.openai.com/api/docs/guides/image-generation), [GPT Image 1 model page](https://developers.openai.com/api/docs/models/gpt-image-1), [GPT Image 2 limits](https://developers.openai.com/api/docs/models/gpt-image-2).

## Preserve safety, consent, privacy, provenance, and rights

### Consent and real people

- Obtain express consent and all necessary rights before reproducing any person's likeness.
- Do not use visual capabilities to identify a person or solicit/infer private or sensitive information about them.
- Do not create non-consensual intimate content, sexualized minors, harassment, fraud, impersonation, or deceptive likeness use. Do not use someone's likeness without consent in a way that could confuse authenticity.
- Apply heightened review to news-like, political, medical, legal, safety, and historical imagery. Do not present a generated depiction as evidence of an event.

Sources: [Service Terms §6](https://openai.com/policies/service-terms/), [Usage Policies](https://openai.com/policies/usage-policies/).

### Rights and commercial review

OpenAI's business agreement says that, as between the customer and OpenAI and to the extent permitted by law, the customer retains input rights and owns output; the customer must still have the rights, licenses, and permissions for inputs and is responsible for output use. Output may not be unique. This is not a promise that the result is copyrightable, non-infringing, trademark-clear, factually correct, or exclusive.

**Production heuristic:** For commercial delivery, search for confusingly similar logos/trade dress, verify referenced licenses and releases, keep source provenance, and obtain legal review when risk warrants it. Prefer original style attributes over requests to imitate a living artist or protected franchise.

Source: [OpenAI Services Agreement §§3–4](https://openai.com/policies/services-agreement/), [Service Terms API indemnity limits](https://openai.com/policies/service-terms/).

### API data and retention

API data is not used to train OpenAI models unless the customer explicitly opts in. By default, abuse-monitoring logs may retain customer content for up to 30 days. `/v1/images/generations` and `/v1/images/edits` have no application-state retention in the current table and are eligible for approved Zero Data Retention when using GPT Image models. Responses has default application-state behavior documented separately; Files API objects persist until manually deleted or their configured `expires_after` policy runs, subject to the data-control terms.

**Production heuristic:** Minimize uploads, strip unnecessary metadata, avoid secrets and biometric identifiers, use direct image calls when conversational retention is unnecessary, set Responses storage controls appropriately, delete Files API uploads after the workflow, and confirm ZDR/data-residency eligibility before regulated work. `store=false` alone is not the same as approved Zero Data Retention.

Source: [Data controls in the OpenAI platform](https://developers.openai.com/api/docs/guides/your-data).

### Provenance

OpenAI says API-generated images include C2PA metadata and an embedded SynthID watermark. C2PA metadata may be stripped; the watermark may degrade; absence of either signal does not prove an image was human-made. The verifier can indicate OpenAI origin but not accuracy, lack of edits, ownership, or correct context.

**Production heuristic:** Preserve the original generated file and its metadata, avoid unnecessary transcodes, keep an internal generation ledger, label synthetic media where context requires, and never treat provenance as a factuality certificate.

Source: [C2PA and SynthID in OpenAI-generated images](https://help.openai.com/en/articles/8912793-c2pa-in-images), [ChatGPT Images 2.0 system card](https://deploymentsafety.openai.com/chatgpt-images-2-0/automated-evaluations-and-adversarial-testing).

## Review the final asset, not only the prompt

Use a human reviewer for customer-facing work and automate measurable checks where possible.

- **Instruction:** required subjects, count, action, style, crop, and exclusions.
- **Text:** exact spelling, line breaks, punctuation, duplication, legibility, and extra glyphs.
- **Edit invariants:** identity, geometry, pose, logo/label, palette, crop, camera, background, and unchanged pixels.
- **Visual integrity:** anatomy, hands, occlusion, reflections, repeated patterns, perspective, shadows, edge halos, and compression.
- **Factual integrity:** maps, diagrams, dates, numbers, scientific labels, cultural details, and any implied real event.
- **Delivery:** dimensions, ratio, file signature, alpha expectation, color behavior, file size, and mobile/print readability.
- **Safety and rights:** consent, releases, trademarks, private data, minors, authentic-context risk, and policy compliance.
- **Provenance:** original file retained, generation metadata recorded, and disclosure/ledger requirements met.

Do not claim success until the saved file—not a partial preview—passes the acceptance criteria.

## Official source index

All volatile facts in this skill were checked on 2026-07-09.

- [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [GPT Image prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- [GPT Image 2 model page](https://developers.openai.com/api/docs/models/gpt-image-2)
- [GPT Image 1.5 model page](https://developers.openai.com/api/docs/models/gpt-image-1.5)
- [GPT Image 1 model page](https://developers.openai.com/api/docs/models/gpt-image-1)
- [GPT Image 1 mini model page](https://developers.openai.com/api/docs/models/gpt-image-1-mini)
- [Model deprecations](https://developers.openai.com/api/docs/deprecations)
- [Images API reference](https://platform.openai.com/docs/api-reference/images)
- [Image streaming reference](https://platform.openai.com/docs/api-reference/images-streaming)
- [API pricing](https://developers.openai.com/api/docs/pricing)
- [Data controls](https://developers.openai.com/api/docs/guides/your-data)
- [Usage Policies](https://openai.com/policies/usage-policies/)
- [Service Terms](https://openai.com/policies/service-terms/)
- [OpenAI Services Agreement](https://openai.com/policies/services-agreement/)
- [C2PA and SynthID](https://help.openai.com/en/articles/8912793-c2pa-in-images)
- [ChatGPT Images 2.0 system card](https://deploymentsafety.openai.com/chatgpt-images-2-0/automated-evaluations-and-adversarial-testing)
