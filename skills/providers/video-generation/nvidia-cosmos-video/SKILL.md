---
name: nvidia-cosmos-video
description: Select, run, and govern NVIDIA Cosmos world-video generation across Cosmos 3 Generator, Predict2.5, Transfer2.5, downloadable checkpoints, self-hosted NIMs, and hosted preview surfaces. Use for text/image/video-to-world, controlled world transfer, multiview or action-conditioned physical-AI video, local checkpoint pinning, hardware planning, inference approval, and output validation; do not use for Cosmos Reason/Embed-only tasks.
---

# NVIDIA Cosmos video

Use Cosmos as a **world-generation and world-simulation system**, not as proof of physics. Choose the task, artifact, and runtime together. Names, schemas, licenses, parameter counts, and hardware claims are surface-specific.

This guide was verified against first-party NVIDIA repositories, model cards, NIM documentation, licenses, and technical reports on **2026-07-10**. Recheck every linked model card, release note, support matrix, and embedded license immediately before downloading, deploying, post-training, or serving.

## Route by family and task

| Family/artifact | What it does | Inputs and outputs | Status/boundary |
|---|---|---|---|
| **Cosmos 3 Generator** (`Cosmos3-Nano`, `Cosmos3-Super`) | General omnimodal world generation; text/image to video, and on supported open runtimes video, sound, and action modes | Full open checkpoint cards describe text/image/video/audio/action input and image/video/audio/action output | Newest open family, released 2026-05-31. Use Generator for media; the separate Reasoner produces text reasoning, not video |
| **Cosmos3-Super-Image2Video** | Specialized image-to-video checkpoint | One image + text → video | Do not assume Nano/Super and this specialization are interchangeable |
| **Cosmos-Predict2.5 2B/14B** | Future-world prediction, unified Text2World/Image2World/Video2World; specialized AV/robot variants | Text plus optional first image/video; some variants consume actions or multiview inputs | Current Predict2.5 repository; 2B and 14B pre-trained/post-trained bases, distilled and domain checkpoints have different capabilities |
| **Cosmos-Transfer2.5-2B** | World-to-world transformation with structural control | Source RGB video + prompt + edge/depth/segmentation/visual-blur controls → transformed video | Current control model; use for Sim2Real/Real2Real structure preservation, not unconstrained text-to-video |
| **Predict2 / Predict1 / Transfer1** | Earlier families | Varying text/image/video/control contracts | Predict2 repository is archived and explicitly recommends migration to Predict2.5. Predict1 remains available in NIM. No public universal EOL date was found; call these earlier/legacy, not unsupported unless the exact artifact says so |
| **Cosmos Reason, Embed, Tokenizer, Curator, Evaluator** | Reasoning, embeddings, compression/data/evaluation | Not a video-generation endpoint | Do not route a generation request to these merely because they carry the Cosmos name |

### The Cosmos 3 size labels are not interchangeable

- The Hugging Face model cards count the full omni checkpoints as **16B Nano** and **64B Super**.
- The `cosmos3-generator` NIM packages the generation path as **8B nano** and **32B super**, selected with `NIM_MODEL_SIZE=nano|super`.
- Record the exact artifact and surface. Do not “correct” one count using the other or assume their memory requirements match.

### Choose the production path

| Need | Recommended path | Why |
|---|---|---|
| New general text/image-to-video | Cosmos 3 Generator, Nano for development; consider Super only after quality evidence and capacity approval | Current general family; NIM exposes the same T2V/I2V request shape for nano/super |
| Predict future state from an initial video | Predict2.5 Video2World | Its contract explicitly accepts video conditioning and sliding-window continuation |
| Preserve geometry while changing domain, weather, materials, or appearance | Transfer2.5 | Edge/depth/seg/blur controls express structure directly |
| Seven-camera AV or robot multiview | The matching Predict2.5/Transfer2.5 specialized checkpoint | General single-view checkpoints do not create calibrated multiview data by prompt alone |
| Action-conditioned rollout | Matching Predict2.5 robot/action or Cosmos 3 compatible embodiment | Action dimension, normalization, camera view, and checkpoint must match the embodiment exactly |
| Synchronized generated sound | Cosmos 3 open Framework/Diffusers/vLLM-Omni path with sound modules | The current Cosmos3 Generator NIM `/v1/infer` contract documents video-only T2V/I2V; do not send open-runtime sound fields to it |
| Text analysis, grounding, planning | Cosmos3-Reasoner or Cosmos-Reason2 | Separate VLM/NIM; it does not replace Generator |

## Keep runtime contracts separate

### Open checkpoints and repositories

- Best for research, deterministic revision pinning, local data control, post-training, and specialized variants.
- A Hugging Face model may be gated: accepting its license and sharing account/contact data is part of the download flow. First inference may auto-download checkpoints unless an approved immutable cache is supplied.
- Pin a 40-character Hugging Face commit revision or immutable local snapshot, repository commit/tag, dependency lock, and container digest. Never use mutable `main` or `latest` in a production record.
- After prefetch, use an immutable snapshot path and `local_files_only=True`; set `HF_HUB_OFFLINE=1` where supported. Do not enable `trust_remote_code` without an independent code review and exact commit pin.

### Self-hosted NVIDIA NIM

- NIM is a containerized, synchronous HTTP service at `POST /v1/infer`; it returns JSON containing base64 MP4 (`b64_video`). NIM output MP4 is documented as VP9.
- Each model family has its own container. Current release notes list `cosmos-predict1-7b-*`, `cosmos-transfer2.5-2b`, `cosmos-predict2.5-2b`, and `cosmos3-generator`.
- NIM chooses an optimized profile from hardware unless pinned with `NIM_MODEL_PROFILE` or `NIM_TAGS_SELECTOR`. Record `/v1/metadata`, `/v1/version` where available, image tag **and digest**, active profile, checkpoint reference, precision, and guardrail configuration.
- Container startup can download model artifacts from NGC. Warm and verify the cache under separate approval, then use `NIM_DISABLE_MODEL_DOWNLOAD=1` for a controlled offline launch when the selected container supports it.
- NIM software/container use is governed by the exact agreement embedded at `/opt/nim/LICENSE`, in addition to checkpoint and component notices. Developer Program NIM access is for prototyping/research/development/testing; production licensing/support is a separate NVIDIA AI Enterprise or provider contract.

### NVIDIA-hosted Preview API / API Catalog

- Treat `build.nvidia.com` availability, endpoint URL, authentication, quota, price, retention, processing region, and SLA as account- and date-specific. Use only the signed-in catalog-generated endpoint/schema and current terms; do not synthesize a URL from a model name.
- The Cosmos3 Nano catalog card says hosted Preview output includes safety guardrails and SynthID. Do not transfer that claim to a local open checkpoint.
- Public documentation did not establish a stable universal hosted price, retention period, region, or idempotency key. Obtain exact approval and enterprise/DPA terms before confidential or regulated uploads.

## Exact NIM request contracts

All examples below target a **running, already-approved self-hosted NIM** at loopback. They do not install software, download weights, or start a container.

### Cosmos3 Generator NIM

Mode is inferred; no `mode` field exists. Unknown fields produce HTTP 422.

- T2V: non-empty `prompt`, no `image`.
- I2V: `image` as raw base64, data URI, or permitted public URL; prompt optional. JPEG/PNG/WebP; request field maximum 20,000,000 characters.
- `resolution`: `256`, `480`, or `720`, optionally suffixed `_16_9`, `_1_1`, `_9_16`, `_4_3`, `_3_4`.
- `num_output_frames`: 4k+1 cadence from 25–397; tier caps are 397 at 256, 297 at 480, and 197 at 720. Default 189.
- `fps`: 1–60, recommended 10–30; the encoder preserves fractional FPS but the model rounds to the nearest integer.
- `guidance_scale`: 1–7, default 6. `steps`: 1–100, default 35. Set a nonnegative seed.

**Example — one approved 7.875-second T2V request:**

```json
{
  "prompt": "Fixed waist-height camera in a clean robot-cell aisle. A yellow mobile robot rolls forward two meters, slows beside shelf B4, and stops; its wheels rotate consistently, the shelf and floor markings remain fixed, and no people enter frame.",
  "negative_prompt": "object morphing, sliding wheels, changing shelf geometry, camera shake, text overlays, logos",
  "resolution": "720_16_9",
  "num_output_frames": 189,
  "fps": 24.0,
  "steps": 35,
  "guidance_scale": 6.0,
  "seed": 18427
}
```

Why: `189 / 24 = 7.875` seconds, the frame count follows 4k+1, and the prompt expresses a visible initial state, one state transition, camera constraint, and invariants. Likely failures are wheel slip, object morphing, and an inaccurate stop position; measure them rather than describing the result as “physics-aware.”

### Predict2.5-2B NIM

- Required prompt; add **one of** `image` or `video`, not both. Neither means Text2World; image means Image2World; MP4 video means Video2World.
- `resolution` keys: `256`, `480`, `512`, `720` plus the same five aspect suffixes. Examples: `480_16_9` is 768×432; `720_16_9` is 1280×704.
- Default `num_output_frames` is 93. Larger values use an autoregressive sliding-window loop. The NIM schema does not expose an FPS field for Predict2.5; inspect the returned MP4 instead of inferring duration.
- `guidance_scale` 1–20, default 7; `steps` 1–50, default 35; seed range 0–4294967295.

**Example — Image2World motion test:**

```json
{
  "prompt": "The same white robot arm closes its gripper around the red block and raises it vertically by ten centimeters. The workbench, camera, gripper design, and all other blocks remain unchanged.",
  "negative_prompt": "extra blocks, changing gripper, camera movement, object morphing, flicker",
  "image": "data:image/png;base64,APPROVED_BASE64_IMAGE",
  "resolution": "480_16_9",
  "num_output_frames": 93,
  "steps": 35,
  "guidance_scale": 7.0,
  "seed": 92014
}
```

The open 2B model card separately describes 5-second, 16-FPS 720p/480p checkpoint variants and specific 1280×704 or 832×480 conditioning media. Do not use that checkpoint contract to override the current NIM schema.

### Transfer2.5-2B NIM

- Required: MP4 source `video`, prompt, and at least one of `edge`, `depth`, `vis` (visual blur), or `seg`.
- Source length: 93–480 frames. `resolution` (`256|480|512|720`) is internal processing resolution; output resolution matches the input.
- Controls can supply a base64/URL `control`, optional mask, and `control_weight` 0–1. To auto-extract a control, omit `control` entirely—`null` or `""` is an error.
- Multiple weights totaling over 1 are proportionally normalized. Use aligned controls derived from the same source with identical spatial and temporal dimensions.
- `guidance` is 0–7, default 3; `num_steps` default 35; `num_conditional_frames` is 1 or 2.

**Example — controlled Sim2Real variation:**

```json
{
  "video": "data:video/mp4;base64,APPROVED_SOURCE_VIDEO",
  "prompt": "Photorealistic industrial inspection cell under cool overhead LEDs. Preserve the robot, conveyor, camera path, timing, contacts, and all object positions; replace only synthetic materials and lighting with realistic metal, rubber, and painted concrete.",
  "negative_prompt": "changed geometry, new objects, missing conveyor, altered camera path, inconsistent contacts, text overlays",
  "seed": 7312,
  "guidance": 3,
  "num_steps": 35,
  "resolution": "480",
  "num_conditional_frames": 1,
  "edge": {"control_weight": 0.6},
  "depth": {"control_weight": 0.4}
}
```

This asks the NIM to derive edge/depth from the source. For safety-critical synthetic data, prefer explicit, hashed control maps and measure alignment. A visually plausible output is not a labeled ground truth sample.

## Prompt for world state, not vibes

Documented guidance: Predict2.5 local model cards recommend fewer than 300 words for the 5-second clip and concrete scene, objects, motion, and background; Cosmos3 NIM recommends a concise sentence or two.

Production heuristics:

1. Declare the sensor/camera frame first: fixed, dashcam, wrist camera, third-person, lens/height, and permitted motion.
2. State the initial world: count objects; give stable color/material/position/identity; name contact relationships.
3. Describe one chronological transition with distances, direction, speed trend, and stop/end condition.
4. State invariants: what cannot move, morph, appear, disappear, relabel, or change view.
5. Put rendering/style changes after geometry and dynamics. For Transfer, let controls carry structure and let text describe the target domain.
6. Use negative prompts for observable failure classes, not policy evasion or a long list of vague quality adjectives.
7. Hold revision, runtime, precision, prompt, controls, and seed fixed while changing one parameter. Seeds aid comparisons but do not guarantee bitwise identity across kernels, quantizations, GPUs, or revisions.
8. For sliding-window output, inspect every seam and measure drift per chunk. More frames expand the error surface; they do not extend physical memory for free.

## Local checkpoint and revision control

Before any model fetch or first container boot, create and approve a deployment manifest:

```json
{
  "surface": "self-hosted-nim",
  "container": "nvcr.io/nim/nvidia/cosmos3-generator@sha256:APPROVED_DIGEST",
  "license_sha256": "HASH_OF_/opt/nim/LICENSE",
  "model_size": "nano",
  "precision": "fp8",
  "nim_model_profile": "APPROVED_PROFILE_ID",
  "metadata_sha256": "HASH_OF_CANONICAL_/v1/metadata",
  "guardrail_manifest_sha256": "APPROVED_HASH",
  "driver_cuda_gpu": "RECORDED_HOST_FACTS",
  "network_policy": "offline-after-cache-warm",
  "input_manifest_sha256": "APPROVED_INPUT_HASH",
  "output_root": "/approved/immutable/run-root"
}
```

- Hash every checkpoint shard/control/input and retain provider filenames, byte counts, source URL, license, and acquisition time. Verify safetensors/index consistency or framework-specific checkpoint structure before loading.
- Mount BYOC checkpoints read-only. For Cosmos3 NIM, `NIM_FT_CHECKPOINT` must be an absolute in-container path with `transformer/`, `vae/`, `scheduler/`, and `model_index.json`; NIM discovers size/precision and rejects profile mismatches. Confirm the live checkpoint via `/v1/metadata`.
- Transfer2.5 NIM accepts separate `NIM_EDGE_CHECKPOINT`, `NIM_VIS_CHECKPOINT`, `NIM_DEPTH_CHECKPOINT`, and `NIM_SEG_CHECKPOINT`. Record which are custom versus bundled. FP8 first boot may spend hours calibrating/building TensorRT engines; the cache is an artifact and `/v1/health/ready` is the readiness signal.
- Post-training uses different checkpoint formats: distributed DCP for resume and consolidated `.pt` for inference/initial training. Never load a DCP directory as though it were a consolidated inference file. Record base revision, data manifest/license, code commit, config, optimizer state, step, and parent checkpoint.
- Treat pickle-backed `.pt` as executable-risk input. Load only trusted, hashed checkpoints in an isolated environment. Prefer safetensors where the supported surface provides it.

## Hardware and precision are surface-specific

- **Cosmos3 open Diffusers/model card:** Linux; BF16 is the tested precision; tested hardware includes H100 and GB200. No generic local VRAM minimum is published on the card. Do not promise consumer-GPU support.
- **Cosmos3 Generator NIM:** Hopper or newer (CC ≥9.0). Nano needs ≥79 GiB per device. Super FP8 needs ≥121 GiB on one device or ≥79 GiB on each of two; Super BF16 needs ≥150 GiB on one, ≥92 GiB on two, or ≥65 GiB on four. NVFP4 needs Blackwell (CC ≥10.0); do not apply NIM quantization claims to open Diffusers.
- **Predict2.5 open 2B Video2World:** model card reports about 32.54 GB VRAM, Linux, BF16 tested. Open repository supports Ampere or newer. The optimized Predict2.5 NIM instead requires CC ≥8.9; use its current GPU/profile matrix.
- **Transfer2.5 open 2B:** about 65.4 GB VRAM, Linux, BF16 tested; 720p/16-FPS/93-frame benchmarks take minutes even on data-center GPUs. Its AV multiview model requires at least eight 80-GB GPUs. Transfer NIM requires Hopper or later and substantial host RAM/disk per its current prerequisites.
- Before approval, measure free VRAM, host RAM, disk/cache headroom, GPU topology/P2P, driver/CUDA compatibility, expected cold-start build time, wall time, and energy/cloud cost. A parameter-count comparison is not a capacity plan.

## Dry-run-first NIM client

This complete Python example targets a loopback Cosmos3 Generator NIM only. Default mode prints the canonical approval envelope and performs **no network call or write**. Execution requires exact deployment identity, request digest, output path, and wall-time ceiling. It makes one synchronous POST and never retries an ambiguous result.

```python
import base64, hashlib, json, os, pathlib, urllib.parse, urllib.request

MODE = os.getenv("COSMOS_MODE", "dry-run")
output = pathlib.Path(os.getenv("COSMOS_OUTPUT", "./cosmos3-t2v.mp4")).resolve()
body = {
    "prompt": "Fixed waist-height camera in a clean robot-cell aisle. A yellow mobile robot rolls forward two meters, slows beside shelf B4, and stops; shelf and floor markings remain fixed.",
    "negative_prompt": "object morphing, sliding wheels, changing geometry, camera shake, text overlays",
    "resolution": "720_16_9", "num_output_frames": 189, "fps": 24.0,
    "steps": 35, "guidance_scale": 6.0, "seed": 18427,
}
deployment = {
    "surface": "self-hosted-nim", "model": "cosmos3-generator",
    "container_digest": os.getenv("COSMOS_CONTAINER_DIGEST", "<required>"),
    "model_size": "nano", "precision": "fp8",
    "profile_id": os.getenv("COSMOS_PROFILE_ID", "<required>"),
    "metadata_sha256": os.getenv("COSMOS_METADATA_SHA256", "<required>"),
    "guardrail_manifest_sha256": os.getenv("COSMOS_GUARDRAIL_SHA256", "<required>"),
}
envelope = {"deployment": deployment, "endpoint": "http://127.0.0.1:8000/v1/infer",
            "request": body, "output": str(output), "allowed_generation_calls": 1}
wire = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
approval_wire = json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode()
digest = hashlib.sha256(approval_wire).hexdigest()
print(json.dumps({"mode": MODE, "approval_sha256": digest, "expected_duration_seconds": 7.875,
                  "approval_envelope": envelope}, indent=2))
if MODE == "dry-run":
    raise SystemExit(0)
if MODE != "execute" or os.getenv("COSMOS_APPROVED_SHA256") != digest:
    raise SystemExit("Exact approval digest is required")
if any(v == "<required>" for v in deployment.values()):
    raise SystemExit("Pin container, profile, metadata, and guardrail identities")
timeout = int(os.getenv("COSMOS_MAX_WALL_SECONDS", "0"))
if timeout < 60:
    raise SystemExit("Set the approved wall-time ceiling")
if output.exists():
    raise SystemExit("Output exists; refusing overwrite")

state_dir = pathlib.Path(os.getenv("COSMOS_STATE_DIR", ".cosmos-state")).resolve()
state_dir.mkdir(parents=True, exist_ok=True)
state = state_dir / f"{digest}.json"
try:
    fd = os.open(state, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
except FileExistsError:
    raise SystemExit("Digest already claimed; refusing duplicate inference")
with os.fdopen(fd, "w", encoding="utf-8") as f:
    json.dump({"state": "PREPARED", "approval_sha256": digest}, f); f.flush(); os.fsync(f.fileno())

def replace_state(value):
    temp = state.with_suffix(f".tmp-{os.getpid()}")
    with open(temp, "x", encoding="utf-8") as f:
        json.dump(value, f); f.flush(); os.fsync(f.fileno())
    os.replace(temp, state)

req = urllib.request.Request(envelope["endpoint"], data=wire, method="POST",
    headers={"Content-Type": "application/json", "Accept": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read(512 * 1024 * 1024 + 1)
        if len(raw) > 512 * 1024 * 1024:
            raise RuntimeError("response exceeds 512 MiB")
        result = json.loads(raw)
        if result.get("error"):
            raise RuntimeError("NIM returned an error")
        video = base64.b64decode(result["b64_video"], validate=True)
        if len(video) < 16 or b"ftyp" not in video[:64]:
            raise RuntimeError("response is not an MP4")
except Exception as exc:
    replace_state({"state": "UNKNOWN", "approval_sha256": digest,
                   "error_type": type(exc).__name__})
    raise SystemExit("Outcome UNKNOWN; inspect NIM logs/metrics before any rerun") from exc

output.parent.mkdir(parents=True, exist_ok=True)
temp_output = output.with_suffix(output.suffix + f".tmp-{os.getpid()}")
with open(temp_output, "xb") as f:
    f.write(video); f.flush(); os.fsync(f.fileno())
os.replace(temp_output, output)
replace_state({"state": "RECEIVED", "approval_sha256": digest,
               "output": str(output), "sha256": hashlib.sha256(video).hexdigest(), "bytes": len(video)})
print(json.dumps({"output": str(output), "sha256": hashlib.sha256(video).hexdigest()}))
```

Before execute mode, confirm `GET /v1/health/ready`, capture `/v1/metadata` and `/v1/version`, and hash their canonical responses. This example intentionally has no hosted-auth path and no retry loop.

## Lifecycle and artifact custody

1. Preflight rights, license, safety, immutable deployment, input/control hashes, output destination, GPU/time/cloud ceiling, and exactly allowed calls. Model or precision changes require new approval.
2. Write a run ledger before inference. A synchronous client timeout is **UNKNOWN**, not proof of failure. Inspect NIM logs, GPU metrics, request correlation, and output staging before rerunning.
3. Stream or strictly bound base64 responses; decode with validation. Write to a new temporary file, fsync, then atomically rename. Never overwrite an accepted result.
4. Use `ffprobe` plus a full `ffmpeg -v error -i output.mp4 -f null -` decode. Verify container/codec, actual frames, duration, FPS, dimensions, pixel format, timestamps, and audio streams. For Cosmos3 generated sound, require 48-kHz stereo AAC and review synchronization/content.
5. Review frame ranges for prompt/state compliance, object count/permanence, contact, trajectories, camera stability, morphing, labels/text, faces, unsafe content, and I2V first-frame fidelity. For Transfer, compute edge/depth/seg alignment; for multiview, measure temporal and cross-camera consistency.
6. Preserve source output, prompt/negative prompt, controls, seed, revision, container/profile/precision, guardrail results, GPU/software facts, output hash, QC report, and disclosure/provenance record. Do not call an edited clip the raw model result.
7. Treat every generated trajectory/world state as a hypothesis. Never feed it directly into a robot, vehicle, safety controller, or life-critical decision without independent simulation, real-data validation, redundancy, and domain safety analysis.

## Licenses, rights, safety, and privacy

- **Predict2.5/Transfer2.5:** repository code is Apache-2.0; model weights are under the NVIDIA Open Model License. That model license allows commercial use and derivative models, disclaims NVIDIA ownership of outputs, requires specified notices/“Built on NVIDIA Cosmos” in covered distributions/services/training uses, incorporates Trustworthy AI terms, and terminates rights if a contained guardrail is bypassed without a substantially similar use-case-appropriate guardrail. Read the exact accompanying revision.
- **Cosmos 3 open release:** code and model materials are under **OpenMDW-1.1**, which requires retaining the license and applicable origin/copyright notices when distributing Model Materials and imposes no output-use obligations. It leaves third-party rights clearance and consent to the user. Do not import NVIDIA Open Model License attribution/guardrail clauses into OpenMDW by analogy.
- **NIM:** obey `/opt/nim/LICENSE` and all component notices. A current catalog card may describe a different model license from the open checkpoint. Archive the license attached to the exact container/checkpoint; never choose a license from a summary page.
- Preserve enabled guardrails. Cosmos guardrail stages include prompt/blocklist checks, video safety filtering, and face blur. Hosted Cosmos3 Preview also claims SynthID. Local Cosmos3 repositories expose ways to disable guardrails, but technical possibility is not approval; do not disable or weaken them without legal/security review and a documented substantially similar safeguard where the artifact license requires it.
- Obtain rights/consent for every person, voice, health/personal datum, trademark, copyrighted asset, simulator dataset, control map, and post-training record. NVIDIA model cards warn generated media may neither blur people nor preserve their proportions.
- Prohibit illegal surveillance/biometrics, non-consensual intimate imagery, CSAM, deception, harassment, abuse, fraud, and unsafe operational deployment. Disclose synthetic media and model limitations; retain SynthID/watermarks/provenance rather than stripping them.
- Self-hosting does not automatically prove zero egress: first boot, Hugging Face/NGC downloads, telemetry, guardrails, log sinks, and remote controls must be inspected and network-controlled. Hosted Preview privacy, retention, training use, deletion, and region were not fully specified in the public model contract reviewed; require written terms for sensitive data.

## Known unknowns and conflict policy

- No public universal EOL schedule was found for all Cosmos families. Predict2 is archived; that fact does not establish dates for Predict1 or Predict2.5.
- Hosted Preview availability, endpoint routing, rate limits, pricing, retention, and regions can differ by account and rollout.
- Cosmos3 open-checkpoint VRAM requirements are not the Cosmos3 NIM VRAM matrix; 16B/64B full-model counts are not the NIM's 8B/32B Generator labels.
- The latest NIM docs list Cosmos3 Generator GA and Predict2.5 NIM even where older introduction/blog text omits them or says “coming.” Prefer the exact current release notes, support matrix, and running `/v1/metadata`.
- NIM and open-repository schemas differ. Reject unknown NIM fields rather than copying Framework/vLLM arguments into `/v1/infer`.
- Benchmark results are model-, checkpoint-, prompt-set-, GPU-, precision-, guardrail-, and runtime-specific. Treat NVIDIA comparisons as first-party measurements, not universal ranking.
- If model card, repo, NIM page, and embedded license conflict: stop; preserve the evidence; prefer the exact artifact's embedded license/schema plus current release notes; obtain NVIDIA clarification before distribution or production.

## Primary sources

- [NVIDIA Cosmos repository / Cosmos 3](https://github.com/NVIDIA/cosmos), [Cosmos3-Nano model card](https://huggingface.co/nvidia/Cosmos3-Nano), [Cosmos 3 technical report](https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf), [Cosmos 3 research page](https://research.nvidia.com/labs/cosmos-lab/cosmos3/)
- [Predict2.5 repository](https://github.com/nvidia-cosmos/cosmos-predict2.5), [Predict2.5 model card](https://huggingface.co/nvidia/Cosmos-Predict2.5-2B), [Predict2.5 report](https://research.nvidia.com/labs/dir/cosmos-predict2.5/)
- [Transfer2.5 repository](https://github.com/nvidia-cosmos/cosmos-transfer2.5), [Transfer2.5 model card](https://huggingface.co/nvidia/Cosmos-Transfer2.5-2B), [Transfer2.5 report](https://research.nvidia.com/labs/dir/cosmos-transfer2.5/)
- [NIM introduction](https://docs.nvidia.com/nim/cosmos/latest/introduction.html), [release notes](https://docs.nvidia.com/nim/cosmos/latest/release-notes.html), [sampling controls](https://docs.nvidia.com/nim/cosmos/latest/sampling-params.html), [support matrix](https://docs.nvidia.com/nim/cosmos/latest/support-matrix.html), [BYOC](https://docs.nvidia.com/nim/cosmos/latest/bring-your-own-checkpoint.html), [configuration](https://docs.nvidia.com/nim/cosmos/latest/configuration.html), [EULA](https://docs.nvidia.com/nim/cosmos/latest/EULA.html)
- [Cosmos Guardrail](https://docs.nvidia.com/cosmos/latest/guardrail.html), [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/), [Trustworthy AI terms](https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/), [OpenMDW-1.1](https://openmdw.ai/license/1-1/)
