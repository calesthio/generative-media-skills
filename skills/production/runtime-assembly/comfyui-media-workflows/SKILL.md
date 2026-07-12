---
name: comfyui-media-workflows
description: Provider-independent production workflow for agents assembling, auditing, executing, and handing off ComfyUI node-graph workflows for image, video, upscale, inpaint, conditioning, and batch media generation; use when a task involves ComfyUI workflow JSON/API graphs, model and custom-node inventories, reproducibility, provenance, safety/rights review, local or cloud execution hygiene, or production QA.
---

# ComfyUI media workflow production

Use this skill to turn a creative or technical brief into a production-ready ComfyUI workflow package. Treat ComfyUI as a graph-based media production runtime, not as a prompt box. Your output should make the graph reproducible, reviewable, safe to run, and easy for another operator or system to execute.

This is provider-independent. Do not assume a specific checkpoint, hosted Comfy service, custom node set, or cloud vendor unless the user or the existing project explicitly names one. Re-check ComfyUI, custom-node, model, license, and cloud API facts at production time because they change frequently.

## Operating principles

- Start from the deliverable and constraints, then choose graph topology, models, nodes, and runtime. Do not start by pasting a popular workflow.
- Separate documented facts from production heuristics. Documented facts come from current docs, model cards, licenses, API schemas, and direct tests. Heuristics are your production judgment.
- Keep two workflow artifacts when possible:
  - `workflow.json`: frontend/save-format graph with layout, grouping, notes, and operator readability.
  - `workflow_api.json`: API-format graph for programmatic execution.
- Keep enough metadata to recreate a run: workflow JSON, input files with hashes, model identifiers and hashes, custom-node repo revisions, ComfyUI version, parameters, seed policy, hardware/runtime, output paths, and QA notes.
- Prefer fewer custom nodes and fewer model dependencies unless the creative requirement genuinely needs them. Every custom node is code execution and supply-chain risk.
- Never treat model availability as rights clearance. A file being downloadable does not mean the project can use it commercially, use its outputs freely, train on outputs, or use a person's likeness.
- Decide intentionally whether workflow metadata should be embedded in outputs. Embedded graphs aid reproducibility, but may leak prompts, model names, private paths, client references, API node titles, or workflow IP.

## Required first pass

Produce a short production brief before building or modifying a graph:

1. **Deliverable:** media type, count, dimensions/aspect ratio, duration/fps if video, file formats, naming, platform or downstream editor.
2. **Creative intent:** subject, style, constraints, references, negative constraints, must-preserve elements, brand rules.
3. **Inputs:** text prompts, images, masks, video, audio, depth/pose/control maps, brand assets, identity/likeness permissions, source ownership.
4. **Runtime:** local ComfyUI, Comfy Cloud, another hosted Comfy-compatible service, or handoff-only; available GPU/VRAM, concurrency, storage, network and privacy constraints.
5. **Model inventory:** intended checkpoint/diffusion model, VAE, text encoders, LoRAs, ControlNets, adapters, upscalers, video models, audio/3D models if any.
6. **Custom-node inventory:** every non-core node package, install source, version/commit, license, dependency impact, trust level, and replacement plan.
7. **Rights and safety:** commercial status, client/counsel approval needs, likeness/voice consent, minors, regulated domains, impersonation/deception, prohibited content, platform restrictions.
8. **Reproducibility target:** exact rerun, near-match, or exploratory batch. Exact rerun requires stricter seeds, versions, hashes, and deterministic caveats.
9. **Handoff target:** another artist, an API service, a cloud deployment, a batch render queue, or an archive.

If any of these are missing, make a bounded assumption only when it does not change the workflow design materially. Otherwise ask.

## Workflow formats and API boundaries

ComfyUI workflows are JSON graphs. The frontend save format and API format are not equivalent:

- Save format is for editing in the UI. It includes layout, colors, groups, node sizes, and similar visual metadata.
- API format is for execution. It uses node IDs as keys with `class_type`, `inputs`, and optional `_meta`; it omits most UI layout data.
- For programmatic execution, export from the frontend with **File -> Export Workflow (API)** or otherwise use a conversion method verified against the target runtime.
- Before submitting an API workflow, validate that each `class_type` exists in the runtime's node registry and that each exposed input name matches the current node definition.

When you need a static preflight of an API-format workflow, use the bundled Python 3.11+ stdlib helper before runtime validation:

```bash
python scripts/inspect_workflow.py workflow_api.json --approved-classes approved_classes.txt --unknown-class warning --pretty
```

The helper inspects only local JSON. It validates the API-format shape, node IDs, `class_type`, `inputs`, optional `_meta`, link inputs shaped as `[node_id, output_index]`, dangling links, nonnegative integer output indexes, graph cycles, and warnings for secret-like keys/values or absolute/private-looking path strings. It emits a stable normalized JSON inventory with node, edge, class, and finding counts. Exit codes are `0` for no validation errors, `2` for validation errors, and `3` for parse or operational failures. If you provide a newline-delimited approved class list, class types absent from that list can be reported as warnings, errors, or ignored with `--unknown-class`.

This helper is not a substitute for ComfyUI runtime validation. It never executes the graph, submits to `/prompt`, installs missing custom nodes, loads models, verifies input names against `/object_info`, or proves that a workflow will fit VRAM or run on a target server.

For local ComfyUI server execution, the core pattern is:

1. Upload needed inputs through the runtime's upload route or place them in the expected input directory.
2. Submit the API-format graph to the prompt queue.
3. Monitor status through WebSocket messages or polling.
4. Retrieve outputs from the run history or view/download route.
5. Archive run metadata and outputs outside transient runtime directories.

For cloud execution, do not assume local-route semantics. Confirm authentication, endpoint prefixes, concurrency limits, storage behavior, signed URL behavior, timeouts, and partner-node key handling in the current cloud documentation.

## The production workflow card

For every non-trivial workflow, maintain a workflow card in the project notes or handoff message. It should be concise but complete:

```yaml
workflow_name: product-hero-sdxl-controlnet-v003
purpose: "Generate 6 square product hero image candidates with locked silhouette and color palette."
formats:
  save_graph: workflow.json
  api_graph: workflow_api.json
runtime_verified:
  comfyui_version: "record exact version/commit"
  execution_target: "local RTX 4090 / Comfy Cloud / other"
  verified_at: "YYYY-MM-DD"
models:
  - role: checkpoint
    id: "repository-or-file-name"
    file: "model.safetensors"
    sha256: "..."
    source_url: "..."
    license: "..."
    license_verified_at: "YYYY-MM-DD"
    approval: "approved / needs counsel / noncommercial only / unknown"
custom_nodes:
  - package: "repo-or-registry-id"
    version_or_commit: "..."
    source_url: "..."
    license: "..."
    risk: "low / medium / high"
    reason: "why needed"
exposed_inputs:
  positive_prompt_node: "6.inputs.text"
  negative_prompt_node: "7.inputs.text"
  seed_node: "3.inputs.seed"
  width_height_node: "5.inputs.width|height"
seed_policy: "fixed seeds for rerun; randomized only in variants manifest"
input_custody:
  source_assets: "paths, hashes, consent notes"
output_custody:
  destination: "..."
  metadata_policy: "embed workflow / strip workflow / add C2PA externally"
qa_status: "not run / smoke passed / approved / blocked"
known_limits:
  - "..."
```

Do not invent hashes, versions, license status, or approvals. Mark unknowns plainly.

## Model and license inventory

Inventory every model-like artifact, not only the main checkpoint:

- checkpoint or diffusion model
- VAE
- text encoder(s)
- LoRA, LyCORIS, embedding, textual inversion
- ControlNet, T2I adapter, IP/reference adapter, pose/depth/segmentation model
- upscaler, face restoration model, background remover
- video generation model, interpolation model, frame enhancer
- audio, 3D, captioning, or LLM/VLM model used by nodes

For each, record:

- exact file name and folder category expected by the loader node;
- source URL or repository ID;
- version, revision, or download date;
- file hash when available or computed locally;
- model card or license URL;
- license terms relevant to this job: commercial use, attribution, output use, derivatives/fine-tunes, redistribution, synthetic-data/training restrictions, content-use restrictions;
- known runtime requirements: dtype/quantization, minimum VRAM, required text encoders or VAE;
- who approved it and when, or what remains unresolved.

Use model-card metadata as a starting point, not as the full clearance. Hugging Face supports license metadata and model cards, but missing or ambiguous metadata is common enough that you must inspect the linked license or repository files for consequential work. If the model is a derivative or merge, verify upstream license compatibility when the project is commercial, public, client-facing, or redistributed.

Escalate to the client, rights owner, platform owner, or counsel when:

- the license is absent, contradictory, noncommercial, research-only, unclear about outputs, or incompatible with the intended use;
- the model is a merge or derivative with unknown upstreams;
- the workflow uses a person's likeness, a private reference, a living artist/style request, a trademarked character, a brand asset, or regulated-domain content;
- outputs will be sold, advertised, syndicated, used for political persuasion, used in a regulated domain, or used as training data;
- the workflow or custom-node package will be redistributed to others.

Do not provide legal advice. State the risk and the decision needed.

## Custom-node risk handling

Custom nodes are extensions that execute code inside the ComfyUI environment. Treat them as supply-chain dependencies.

Risk-rank each custom node:

- **Low:** official/core node, current registry package from a known publisher, active maintenance, clear license, no network behavior beyond documented model/API calls, pinned version.
- **Medium:** popular community node with active repo but broad dependencies, unclear release pinning, limited docs, or non-critical network/file behavior.
- **High:** obscure repo, no license, no pinned release, unreviewed install script, binary wheels from unknown source, broad filesystem/network access, credential handling, code obfuscation, stale issues about breakage/security, or required only for a minor convenience.

Required handling:

- Prefer core nodes and official templates when they satisfy the brief.
- If a custom node is necessary, pin a release or commit and record the install source. Avoid "latest" for production.
- Read the node README and installation requirements; check whether it requires models, external APIs, credentials, ffmpeg, CUDA extensions, compiler toolchains, or system packages.
- Install dependencies only into the intended ComfyUI environment. Do not contaminate system Python or unrelated projects.
- Do not run untrusted install scripts or post-install commands without approval.
- Do not pass secrets through node parameters that can be saved into workflow JSON, output metadata, logs, or screenshots unless the node's docs explicitly require that pattern and the user accepts it.
- When using a workflow from an external source, inspect unknown nodes before executing. A missing-node error is safer than blindly installing everything.

If a required custom node is high-risk and no safe replacement exists, stop and ask for approval with options: accept risk in a sandbox, replace the creative approach, use a hosted provider, or pause.

## Graph design patterns

Use these as production patterns, not rigid templates. Node names vary by ComfyUI version, model family, and custom-node package.

### Text-to-image stills

Common structure:

1. Load checkpoint or model family-specific model and required text encoders/VAE.
2. Encode positive and negative prompts.
3. Create latent at target dimensions or model-native dimensions.
4. Sample with a documented sampler/scheduler/steps/CFG/seed.
5. Decode.
6. Optional: upscale, color pass, face/detail pass, metadata/provenance pass.
7. Save with deterministic filename prefix.

Production notes:

- Expose positive prompt, negative prompt, seed, width, height, steps, CFG/guidance, sampler/scheduler, denoise, batch size, and output prefix.
- Keep model-native aspect and resolution constraints visible. Do not silently upscale tiny generations to final delivery unless quality permits.
- Use fixed seeds for approval candidates. Use variant manifests for randomized exploration.

### Image-to-image and stylization

Common structure:

1. Load source image.
2. Preprocess if needed: resize/crop/pad, color normalize, segment, depth, edges, pose, or reference embedding.
3. Encode image to latent or feed it to the relevant conditioning node.
4. Sample with denoise strength chosen for the preservation target.
5. Composite or restore details.
6. Save output and comparison contact sheet.

Heuristic denoise ranges:

- Low denoise for preservation and cleanup.
- Medium denoise for style transfer while retaining composition.
- High denoise for new image generation loosely inspired by the input.

Document the actual denoise value and expected preservation level. For client assets, preserve composition with explicit control inputs rather than hoping a prompt will retain it.

### Inpaint and outpaint

Common structure:

1. Load source image and mask.
2. Verify mask polarity and edge softness.
3. Crop to masked region if using a detail/inpaint crop path, or run full-frame if global consistency matters.
4. Encode image/mask to the inpaint model or conditioning path.
5. Sample with a preservation-appropriate denoise.
6. Composite back into original image.
7. QA seam quality, geometry, shadows, texture, and brand/product fidelity.

Production notes:

- Store the mask as a source artifact with hash; do not rely on a UI-only mask that cannot be handed off.
- Include a "mask check" output or screenshot before long runs.
- If the target is a product, logo, face, or medical/legal/technical object, use stricter review and ask whether AI reconstruction is allowed.

### Control and conditioning

Conditioning turns ambiguous prompt intent into controllable structure. Use it when layout, pose, depth, product silhouette, edge fidelity, camera angle, or identity-adjacent consistency matters.

Common controls:

- edge/lineart/canny for shape and hard contours;
- depth for spatial layout and camera perspective;
- pose/openpose-like skeletons for body positioning;
- segmentation for object regions;
- reference/image adapters for color, style, or identity-adjacent visual cues;
- LoRA or embeddings for repeatable style, subject, or product-family treatment.

Production notes:

- Record preprocessing model and parameters, not only the final control image.
- Prefer one strong control over many weak, conflicting controls.
- If using multiple controls, define priority: structure first, identity/reference second, style last, unless the brief says otherwise.
- QA control overfitting: outputs can look traced, rigid, distorted, or texture-poor when control strength is too high.

### Upscale and finishing

Common structure:

1. Generate at model-appropriate base size.
2. Choose latent upscale or pixel upscale based on artifact type.
3. Apply detail pass only when it improves the image rather than hallucinating new detail.
4. Save original, upscaled, and final files with linked metadata.

Production notes:

- Upscaling is not a substitute for correct base composition.
- Avoid face/detail restoration on people without checking likeness and consent implications.
- For print, inspect at final physical size and resolution. For web/social, inspect compression and crop safe areas.

### Video and motion workflows

Video workflows multiply every risk: VRAM, time, temporal artifacts, rights, and file custody.

Common structure:

1. Define motion spec: duration, fps, aspect ratio, camera/subject motion, source image or text prompt, loop/continuity needs.
2. Load video model and required encoders/VAE/motion modules.
3. Provide source image/video/control frames as needed.
4. Generate short clips before long clips.
5. Optional: interpolate, upscale, stabilize, restore, caption, or composite externally.
6. Save frames and final video with run metadata.

Production notes:

- Smoke-test at short duration, low resolution, and fixed seed before full-resolution runs.
- Lock fps, frame count, resolution, and seed policy. A "5 second" target is not enough; record exact frames and fps.
- Save intermediate frames when the downstream edit may need repairs or temporal QA.
- Watch for temporal identity drift, flicker, texture boiling, camera jumps, text/logo distortion, and motion that contradicts physics or brand requirements.
- For source footage, confirm rights to transform it and whether AI alteration must be disclosed.

### Batch variants

Batching is for controlled exploration, not chaos.

Use a variants manifest:

```yaml
base_workflow: workflow_api.json
locked:
  checkpoint: "..."
  dimensions: "1024x1024"
  negative_prompt: "..."
  control_image_sha256: "..."
variants:
  - id: A01
    seed: 101
    prompt_delta: "warmer backlight, softer shadows"
  - id: A02
    seed: 102
    prompt_delta: "cooler palette, sharper product edge"
```

Change one or two variables per batch unless the purpose is broad exploration. Name outputs with variant IDs and seed. Generate contact sheets or review grids for human selection.

## Prompt, seed, and parameter control

Expose prompts as inputs, but do not leave them as the only control surface.

Prompt handling:

- Split prompt intent into subject, composition, medium/style, lighting, camera/lens, material/texture, constraints, and brand terms when the model responds well to such structure.
- Keep negative prompts focused on actual failure modes. Giant negative lists are hard to debug.
- Record prompt versions. A one-word change can alter approval.
- Remove private client names, unreleased product codenames, personal data, or secret URLs from prompts if outputs or workflow JSON will be shared.

Seed handling:

- For approval, use fixed seeds and record them.
- For exploration, define a seed range or list and record the generator policy.
- If exact reproducibility matters, state that seeds alone are insufficient; model files, node versions, sampler, scheduler, precision, hardware/backend, and preprocessing must also match.

Parameter handling:

- Record sampler/scheduler, steps, CFG/guidance, denoise, dimensions, batch size, model weights, LoRA strengths, control strengths, start/end percentages, upscale scale, fps/frame count, and filename prefix.
- Do not silently leave values at defaults when they materially affect the result. If using defaults, say so.

## VRAM, performance, and reliability

Do not promise a graph will run just because it is valid JSON.

Performance checklist:

- Query or record runtime system information where available: GPU, VRAM, Python/torch/CUDA or equivalent stack, ComfyUI version, free disk, and relevant environment flags.
- Estimate cost drivers: model size, precision, resolution, batch size, frame count, number of samplers, ControlNets/adapters, tiled passes, upscalers, and keeping multiple large models loaded.
- Reduce first: batch size, frame count, resolution, simultaneous controls, high-res/detail pass, then model size/precision if quality permits.
- For video, scale duration and resolution gradually. A graph that runs for 16 frames may fail at 120 frames.
- Use cached intermediate outputs intentionally, but clear caches or rerun from source when validating final reproducibility.
- If a run fails with out-of-memory, document the failing node and change only one resource variable at a time.
- For cloud, record timeout, concurrency, queue behavior, signed URL expiration, and storage retention.

Use `/system_stats` or the target runtime's equivalent when available; use `/free` or the UI equivalent to unload models only when it is safe for other running jobs.

## Input and output custody

Treat every input and generated output as an asset with custody.

Inputs:

- Store source images, masks, videos, audio, and control maps in a project-owned input directory or approved cloud storage.
- Hash client-provided inputs and references.
- Record license/consent status for people, voices, private property, logos, trademarks, and copyrighted artwork.
- Redact or replace confidential paths and names before sharing workflow JSON externally.
- Never use user-provided private assets for unrelated model training or examples.

Outputs:

- Save outputs to a controlled project directory, not only ComfyUI's default output folder.
- Use filename prefixes that include workflow name, variant ID, seed, and date when practical.
- Preserve originals, selected finals, and rejected variants according to the project retention policy.
- For handoff, include outputs plus a manifest of workflow, inputs, parameters, source model details, and QA status.
- If the platform requires disclosure or provenance metadata, add it as part of finishing, not as an afterthought.

## Provenance and metadata

ComfyUI's SaveImage node can save images to the output directory and may embed workflow metadata such as the prompt. The core workflow docs describe generated-image metadata as a way to reopen the graph, and standalone JSON as useful when the media format does not support metadata.

Production decision:

- **Embed workflow metadata** when reproducibility, internal review, or handoff to a trusted ComfyUI operator matters more than confidentiality.
- **Strip or avoid workflow metadata** when sharing public/client files would leak prompts, model names, file paths, unreleased references, custom-node IP, or private data.
- **Add external provenance** when disclosure, authenticity, or platform policy matters. C2PA/Content Credentials can record signed provenance and AI-edit assertions, but it is opt-in, can be incomplete, and is not DRM.

If using C2PA or similar provenance:

- Record whether content was AI-generated, AI-edited, or composited from ingredients.
- Include tool names and material transformations at a level appropriate for disclosure.
- Avoid including sensitive identity or client-confidential details unless approved.
- Verify that the final export format and platform preserve the metadata, or provide a sidecar/hosted manifest path if the workflow supports it.

## Local and cloud execution hygiene

Local execution:

- Use the intended ComfyUI environment and dependency set.
- Keep models in expected `ComfyUI/models/<category>` folders or configured extra model paths.
- Keep custom nodes pinned and documented.
- Avoid executing unreviewed external workflows in a privileged environment.
- Do not expose local ComfyUI ports publicly without authentication and network controls.
- Clean temporary files and outputs containing confidential references.

Cloud execution:

- Verify current API base URL, authentication header, job submission shape, polling/WebSocket behavior, upload/download routes, concurrency, storage retention, and billing.
- Keep API keys in environment variables or secret stores, never in workflow JSON.
- Understand partner/API nodes that call external providers; record which third-party services receive inputs.
- Download outputs before signed URLs expire and store them in project custody.
- Do not assume cloud outputs are private forever; check the service terms and project requirements.

## QA before handoff

Minimum QA:

- JSON opens in ComfyUI frontend if a frontend graph is provided.
- API graph validates against the runtime: all `class_type` values exist; required inputs are present; loader nodes point to available files.
- Model and custom-node inventory is complete enough for another operator to reproduce installation.
- Smoke run passes with a cheap setting or one representative seed.
- Outputs appear in expected location and are named correctly.
- The workflow card names all exposed inputs and fixed parameters.
- Rights/safety status is not "unknown" for public, paid, client, or redistributed work.
- Metadata/provenance policy is explicit.

Visual QA for stills:

- composition matches brief;
- subject identity, product geometry, logos/text, hands/faces, reflections, shadows, and perspective are acceptable;
- no unwanted watermark/signature/text or private reference leakage;
- crop safe areas and final dimensions are correct;
- upscaling/detail pass did not hallucinate defects.

Visual QA for video:

- temporal consistency, no flicker/boiling beyond acceptable style;
- subject and object continuity across frames;
- motion direction and camera movement match brief;
- no frame drops, broken loops, unstable text/logos, or unwanted morphing;
- fps, duration, codec/container, and audio/caption expectations are met.

Technical QA:

- rerun one fixed-seed output after changes when reproducibility is required;
- inspect logs for warnings about missing nodes/models, fallback precision, skipped inputs, failed downloads, or API-node errors;
- compare file hashes or perceptual matches when exact rerun is required;
- verify output metadata is present or absent according to policy.

## Handoff package

Hand off:

- `workflow.json` for UI editing when available;
- `workflow_api.json` for execution when available;
- workflow card or manifest;
- input assets and masks/control maps, or approved storage URLs;
- output samples/finals;
- model inventory with licenses and hashes;
- custom-node inventory with versions/commits and install notes;
- run log: seed, prompt, parameters, runtime, output filenames, errors;
- QA notes and open risks;
- metadata/provenance decision.

If redistribution is intended, include only assets and model links that can legally and practically be redistributed. Otherwise provide installation instructions and source URLs rather than bundling restricted model files.

## Example: controlled product hero stills

Example intent: Generate square ecommerce hero images for a new bottle while preserving silhouette and label placement. The user provides an approved product render and brand palette. Commercial release is planned.

Approach:

- Use image-to-image plus edge/depth conditioning rather than pure text-to-image.
- Keep the product render and mask as hashed inputs.
- Use a commercially cleared checkpoint and a small number of core/control nodes.
- Run six fixed-seed variants with controlled lighting changes.
- Strip embedded workflow metadata from public finals, but preserve internal workflow files.

Example workflow card excerpt:

```yaml
workflow_name: bottle-hero-control-v001
purpose: "Generate six 1:1 product hero candidates preserving bottle geometry."
exposed_inputs:
  prompt: "CLIPTextEncode positive text"
  negative_prompt: "CLIPTextEncode negative text"
  seed: "KSampler seed"
  control_strength: "ControlNet strength"
locked:
  dimensions: "1024x1024"
  source_product_sha256: "record actual hash"
  mask_sha256: "record actual hash"
  model_license_status: "approved for commercial use by client on YYYY-MM-DD"
variant_policy:
  seeds: [50101, 50102, 50103, 50104, 50105, 50106]
  changed_fields: ["seed", "lighting phrase only"]
qa_focus:
  - "label text/logo not reconstructed incorrectly"
  - "bottle silhouette matches reference"
  - "no invented claims on packaging"
metadata_policy: "strip from delivered finals; archive workflow internally"
```

Why this works: the graph protects hard product constraints with control inputs and uses prompts for mood rather than asking the model to invent the product shape.

Likely failures: label distortion, extra cap seams, unrealistic reflections, control overfitting, insufficient commercial clearance for a downloaded LoRA.

## Example: inpainted campaign image repair

Example intent: Remove a distracting object from an approved campaign image without changing the model's face, clothing, or background identity.

Approach:

- Use a masked inpaint workflow.
- Keep the original image immutable.
- Store a mask file and a mask-preview output.
- Use low-to-medium denoise and composite back into the original.
- QA at full resolution and compare to original.

Example agent plan:

```text
I will build an inpaint-only workflow, not a full img2img restyle. Fixed inputs are the original campaign image and mask. The only creative prompt will describe the missing background texture. I will preserve the person, wardrobe, and lighting, and I will stop if the mask overlaps face, body, logo, or other protected areas.
```

Expected handoff notes:

- original image hash;
- mask hash and polarity;
- denoise value;
- inpaint model/checkpoint license;
- before/after comparison;
- statement that no face/body alteration was intended;
- open approval item if any person/brand element was changed.

## Example: short image-to-video batch

Example intent: Create three 4-second vertical animated loops from an approved poster frame for a social teaser.

Approach:

- Verify rights for AI transformation of the poster.
- Use image-to-video or video model workflow with fixed frame count and fps.
- Start with a low-resolution 1-second smoke test.
- Batch only motion prompt and seed after the smoke run passes.
- Save both video files and intermediate frames if downstream editing is expected.

Example manifest excerpt:

```yaml
workflow_name: poster-loop-i2v-v002
delivery:
  aspect_ratio: "9:16"
  fps: 24
  frames: 96
  duration_seconds: 4
smoke_test:
  frames: 24
  resolution: "reduced"
  status: "passed/failed"
variants:
  - id: loop-a
    seed: 7201
    motion: "subtle parallax push-in, fabric barely moving, no face morph"
  - id: loop-b
    seed: 7202
    motion: "slow lateral camera drift, particles in background only"
  - id: loop-c
    seed: 7203
    motion: "gentle light sweep, subject locked"
qa_focus:
  - "identity consistency"
  - "no text/logo warping"
  - "loop seam if looped"
  - "no unauthorized transformation of protected artwork"
```

Likely failures: face drift, text/logo warping, high VRAM use at final frame count, model license unclear for commercial social use, temporal artifacts hidden by small previews.

## Source notes and verification

Facts in this skill were grounded in these sources, verified on 2026-07-11:

- ComfyUI official documentation: ComfyUI is a node-based interface/inference engine for generative AI and can run locally; docs also describe local and cloud APIs. https://docs.comfy.org/
- ComfyUI Workflow API Format: frontend save format differs from API format; API format uses node IDs and omits UI layout data; export through `File -> Export Workflow (API)`. https://docs.comfy.org/development/api-development/workflow-api-format
- ComfyUI Workflow JSON specification: workflow JSON schema and versioned workflow structure. https://docs.comfy.org/specs/workflow_json
- ComfyUI Server API routes: `/prompt`, `/object_info`, `/history`, `/queue`, `/upload/image`, `/upload/mask`, `/view`, `/system_stats`, `/free`, and `/ws` route purposes. https://docs.comfy.org/development/comfyui-server/comms_routes
- ComfyUI Cloud API docs: API-format workflow submission, upload, job monitoring, output download, API-key handling, and concurrency behavior for Comfy Cloud; cloud API is labeled experimental in the docs. https://docs.comfy.org/development/cloud/overview and https://docs.comfy.org/development/cloud/api-reference
- ComfyUI workflow docs and SaveImage docs: workflows can be saved as JSON and generated images can contain workflow/prompt metadata. https://docs.comfy.org/development/core-concepts/workflow and https://docs.comfy.org/built-in-nodes/SaveImage
- ComfyUI custom-node installation docs: custom nodes extend ComfyUI and should be reviewed carefully because malicious plugins can pose security risks. https://docs.comfy.org/installation/install_custom_node
- ComfyUI templates docs: workflow templates can embed required model links and model folder information; supported model-link behavior and template dependency versions are volatile. https://docs.comfy.org/interface/features/template
- Hugging Face model card and license docs: model cards can specify license metadata, datasets, versions, and task metadata; repository licenses should be respected. https://huggingface.co/docs/hub/en/model-cards and https://huggingface.co/docs/hub/en/repositories-licenses
- C2PA Content Credentials explainer and FAQ: Content Credentials are signed provenance metadata, are opt-in, can be incomplete or removed, can include AI-use assertions, and are not DRM. https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html and https://c2pa.org/faqs/

Volatile facts to re-check at production time:

- ComfyUI route details, API request/response shapes, cloud API status, endpoint prefixes, concurrency limits, and billing.
- Current ComfyUI desktop/manager behavior, registry standards, and template model-link safety rules.
- Every custom-node package version, install method, dependency tree, publisher identity, and security posture.
- Every model/checkpoint/LoRA/control/upscaler/video model license and output-use terms.
- Platform disclosure, provenance, authenticity, and AI-generated media policies.
