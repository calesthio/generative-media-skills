---
name: tencent-hunyuanvideo
description: Generate and operate Tencent Hunyuan video through the managed TokenHub HY-Video-1.5 API or official local HunyuanVideo repositories. Use for text-to-video, image-to-video, hosted job lifecycle, pricing and region planning, local checkpoint selection, hardware and acceleration, prompt design, licensing, safety, provenance, and delivery QA.
---

# Tencent HunyuanVideo

Separate every request into one of three contracts before taking action:

1. **TokenHub `hy-video-1.5`** — current managed Tencent Cloud T2V/I2V interface for new integrations.
2. **Legacy Tencent Cloud `vclm` API 3.0** — older TC3-signed `SubmitHunyuanToVideoJob` surface retained for existing customers while sales and model capabilities migrate to TokenHub.
3. **HunyuanVideo-1.5 open weights** — the official 8.3B local T2V/I2V repository, checkpoints, dependencies, infrastructure, and community license.

Do not infer that the managed model is byte-identical to a public checkpoint. Do not apply the open-weight license to cloud output, or Tencent Cloud terms to downloaded weights.

## Gate execution first

Before a paid request, asset upload, model download, environment installation, or training job:

- State the surface, exact model/action or checkpoint family, region/territory, mode, input, target resolution/duration, audio plan, disclosure, estimated charge or infrastructure footprint, output paths, and QA gates.
- Require explicit approval. For hosted work require a monetary cap; for local work require approved disk/network/GPU scope and license acceptance.
- Default every supplied example to plan-only. Never silently enable postpaid billing, purchase credits/concurrency, download the roughly 372 GB current model repository, or contact a prompt-rewrite service.
- Persist provider request/job IDs or local revision hashes before long-running work. A submit timeout with no job ID is an unknown state; do not blindly resubmit because neither hosted surface documents an idempotency key.

## Choose the correct family

| Family | Purpose | Key boundary |
|---|---|---|
| TokenHub HY-Video-1.5 | Managed text or image to 5 s video | Custom `/v1/api/video/submit` and `/query`; model `hy-video-1.5`; current action schema exposes only 720p |
| Legacy `vclm` Hunyuan | Existing Tencent Cloud integration | TC3-HMAC-SHA256, API version `2024-05-23`, region `ap-guangzhou`, action names rather than a model field |
| HunyuanVideo-1.5 | Current lightweight local foundation model | 8.3B; 480p/720p base generation; separate SR to 720p/1080p; T2V/I2V |
| HunyuanVideo (original) | Legacy local 13B foundation model | Separate checkpoints/code; approximately 45 GB VRAM at 544×960×129f and 60 GB at 720×1280×129f in official tests |
| HunyuanVideo-Avatar | Audio-driven human animation | Separate repository/model; not an audio switch on HunyuanVideo-1.5 |
| HunyuanCustom | Subject customization and separate image/audio/video-conditioned workflows | Separate repository/checkpoints and license review |
| HunyuanVideo-Foley | Generate synchronized audio from video/text | Separate video-to-audio model; it does not generate picture |

Do not route Tencent Cloud's listed YT-Video-2.0, YT-Video-FX, YT-Video-HumanActor, Kling, or Vidu endpoints as HunyuanVideo. They are distinct Tencent Youtu or third-party products sharing a catalog.

## Operate TokenHub for new hosted work

Current facts verified 2026-07-10:

- Domestic base: `https://tokenhub.tencentmaas.com`; Singapore/global base: `https://tokenhub-intl.tencentmaas.com`. Tencent says calls cannot cross the service's enabled region/site. Confirm `hy-video-1.5` is enabled for the chosen account and site rather than inferring availability from a catalog.
- Authenticate with `Authorization: Bearer <API key>`. The video endpoints are `POST /v1/api/video/submit` and `POST /v1/api/video/query`. They are described as OpenAI-compatible but are custom video paths, not Chat Completions.
- Submit with `model: "hy-video-1.5"`; query with the same model plus returned `id`. Fields inherited from the Hunyuan action use lowercase snake case.
- `prompt` is required, documented as a Chinese positive prompt, and limited to 200 UTF-8 characters excluding outer whitespace.
- Optional `image` accepts either `url` or `base64`. URL inputs are at most 10 MB; base64 at most 8 MB. Formats: JPG/JPEG, PNG, WebP, BMP, TIFF. Each side must be 50–5000 pixels and aspect ratio 1:4 through 4:1.
- The linked action schema currently accepts only `resolution: "720p"` and defaults to 720p. Its pricing description identifies a fixed 5-second result. No duration, aspect, seed, negative prompt, camera-control, FPS, codec, or audio field is exposed.
- The submit example returns `id`, `request_id`, `status: "queued"`; the query example returns `status: "completed"`, progress, and `data.url`. The underlying legacy describe contract documents `WAIT/RUN/FAIL/DONE` instead. Keep adapters/status grammars separate.
- The underlying result URL is documented as valid for 24 hours. Download promptly, hash it, and validate locally.
- The current TokenHub model list gives HY-Video-1.5 a default concurrency of five. Legacy `vclm` gives one active job, 30 submit requests/s, and 20 query requests/s. Request rate is not active-job concurrency.

The current TokenHub pricing page charges 1.5 credits per HY-Video-1.5 invocation at 1.0 CNY per credit, so the dated list-price estimate is **1.5 CNY per successful 5-second job**. Discounts, prepaid credits, free quota, and tax can alter invoices. Tencent states failed generation jobs do not consume credits. Re-fetch price and billing state before submission; TokenHub billing is T+1 for some breakdowns, so do not treat the console as a real-time hard stop. The legacy `vclm` billing page's 1.2 CNY credit price belongs to that older surface and must not be used to price TokenHub.

Tencent's older pricing table lists a 1080p SKU, but the current `SubmitHunyuanToVideoJob` schema says only 720p. Do not send 1080p until the exact current TokenHub schema and account entitlement both show it.

### Keep AI disclosure enabled

`logo_add` defaults to `1`, adding an “AI generated” mark. Setting it to `0` requires console approval for the customer to provide the visible label themselves. Tencent's FAQ says users must apply legally compliant AI-generated labeling and must not mislead viewers. Keep the default mark unless a reviewed replacement-label workflow is approved; never disable it merely for aesthetics.

### Use this dry-run-first TokenHub client

This complete standard-library example plans a 720p job by default. It submits only with `--execute`, an exact `TENCENT_APPROVED_DIGEST`, and `TENCENT_APPROVE_MAX_CNY >= 1.5`. It creates a durable claim before the one allowed POST, never retries an ambiguous submission, resumes only after a job ID was saved, bounds query polling and result downloads, refuses overwrite, hashes the artifact, and validates the MP4. Pass one or more reviewed `--result-host-suffix` values for the provider's signed-download host; execution refuses an open-ended result host policy.

```python
#!/usr/bin/env python3
import argparse, hashlib, ipaddress, json, os, random, socket, subprocess, tempfile, time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

BASES = {
    "cn": "https://tokenhub.tencentmaas.com",
    "intl": "https://tokenhub-intl.tencentmaas.com",
}
ESTIMATE_CNY = 1.5  # verified 2026-07-10; re-check before use
MAX_JSON = 1_000_000
MAX_VIDEO = 2_000_000_000

class RetryableQuery(Exception):
    def __init__(self, delay, message): self.delay, self.message = delay, message

def read_json(response):
    raw = response.read(MAX_JSON + 1)
    if len(raw) > MAX_JSON: raise RuntimeError("response JSON exceeds 1 MB")
    return json.loads(raw.decode("utf-8"))

def request_json(req, timeout=45, retryable_query=False):
    try:
        with urlopen(req, timeout=timeout) as r:
            return read_json(r)
    except HTTPError as e:
        if retryable_query and e.code in (429, 500, 502, 503, 504):
            try: delay = min(30.0, max(1.0, float(e.headers.get("Retry-After", "5"))))
            except ValueError: delay = 5.0
            raise RetryableQuery(delay, f"query HTTP {e.code}")
        raise RuntimeError(f"provider HTTP {e.code}; inspect restricted provider logs")
    except URLError as e:
        if retryable_query:
            raise RetryableQuery(5.0, "query transport failure")
        raise RuntimeError("transport failure; submission state may be unknown")

def write_state(path, value, create=False):
    data = (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode()
    if create:
        with path.open("xb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        return
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(temp_name, path)
    finally:
        try: os.unlink(temp_name)
        except FileNotFoundError: pass

def approved_https(url, suffixes):
    u = urlparse(url)
    host = (u.hostname or "").rstrip(".").lower()
    if u.scheme != "https" or not host or u.username or u.password or u.port not in (None, 443):
        raise RuntimeError("result URL must be credential-free HTTPS on port 443")
    if not any(host == s or host.endswith("." + s) for s in suffixes):
        raise RuntimeError("result host is outside the approved suffixes")
    for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        if not ipaddress.ip_address(item[4][0]).is_global:
            raise RuntimeError("result host resolved to a non-public address")
    return url

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None

def download(url, suffixes, part):
    opener = build_opener(NoRedirect)
    for _ in range(4):
        approved_https(url, suffixes)
        try:
            response = opener.open(Request(url, headers={"Accept":"video/*"}), timeout=120)
        except HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location"):
                url = urljoin(url, e.headers["Location"]); continue
            raise RuntimeError(f"download HTTP {e.code}")
        with response, part.open("xb") as f:
            length = response.headers.get("Content-Length")
            if length and int(length) > MAX_VIDEO: raise RuntimeError("output exceeds 2 GB safety cap")
            content_type = response.headers.get_content_type()
            if not (content_type.startswith("video/") or content_type == "application/octet-stream"):
                raise RuntimeError(f"unexpected result content type: {content_type}")
            digest, total = hashlib.sha256(), 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk: break
                total += len(chunk)
                if total > MAX_VIDEO: raise RuntimeError("output exceeds 2 GB safety cap")
                digest.update(chunk); f.write(chunk)
            f.flush(); os.fsync(f.fileno())
        return digest.hexdigest(), total
    raise RuntimeError("too many download redirects")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--site", choices=BASES, default="cn")
    p.add_argument("--image-url")
    p.add_argument("--output", type=Path, default=Path("hy-video-1.5.mp4"))
    p.add_argument("--result-host-suffix", action="append", default=[])
    p.add_argument("--max-wait", type=int, default=1800)
    p.add_argument("--execute", action="store_true")
    a = p.parse_args()
    prompt = a.prompt.strip()
    if not prompt or len(prompt) > 200: p.error("prompt must contain 1–200 characters")
    payload = {"model":"hy-video-1.5","prompt":prompt,"resolution":"720p","logo_add":1}
    if a.image_url:
        u = urlparse(a.image_url)
        if u.scheme != "https" or not u.hostname or u.username or u.password:
            p.error("image URL must be credential-free HTTPS")
        payload["image"] = {"url": a.image_url}
    output = a.output.resolve()
    suffixes = sorted({s.strip(".").lower() for s in a.result_host_suffix if s.strip(".")})
    manifest = {
        "provider": "Tencent TokenHub", "site": a.site,
        "submit": BASES[a.site] + "/v1/api/video/submit",
        "query": BASES[a.site] + "/v1/api/video/query",
        "payload": payload,
        "estimated_cny": ESTIMATE_CNY,
        "price_verified": "2026-07-10", "maximum_submit_calls": 1,
        "submission_retry": "never after transmission", "output": str(output),
        "result_host_suffixes": suffixes,
        "note": "confirm account/site entitlement and current price before execute",
    }
    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    plan = {"approval_digest": digest, **manifest}
    print(json.dumps(plan, ensure_ascii=True, indent=2))
    if not a.execute: return
    if not suffixes: raise SystemExit("at least one reviewed --result-host-suffix is required")
    if output.exists(): raise SystemExit(f"refusing overwrite: {output}")
    if not output.parent.is_dir(): raise SystemExit("output parent must already exist")
    if os.environ.get("TENCENT_APPROVED_DIGEST") != digest:
        raise SystemExit("TENCENT_APPROVED_DIGEST must exactly match this dry-run plan")
    approved = float(os.environ.get("TENCENT_APPROVE_MAX_CNY", "0"))
    if approved < ESTIMATE_CNY: raise SystemExit("TENCENT_APPROVE_MAX_CNY must be at least 1.5")
    key = os.environ.get("TENCENT_TOKENHUB_API_KEY")
    if not key: raise SystemExit("TENCENT_TOKENHUB_API_KEY is required")
    state_path = output.with_suffix(output.suffix + ".job.json")
    if state_path.exists():
        saved = json.loads(state_path.read_text(encoding="utf-8"))
        if saved.get("approval_digest") != digest: raise SystemExit("state belongs to a different plan")
        job_id = saved.get("id")
        if not job_id: raise SystemExit("submission is CLAIMED/UNKNOWN; reconcile with Tencent, never resubmit")
    else:
        saved = {"approval_digest":digest,"status":"CLAIMED","site":a.site,"id":None}
        write_state(state_path, saved, create=True)  # durable claim before paid POST
        headers = {"Authorization":f"Bearer {key}","Content-Type":"application/json"}
        submit = Request(manifest["submit"], data=json.dumps(payload).encode(), method="POST", headers=headers)
        try: job = request_json(submit)
        except Exception:
            saved["status"] = "UNKNOWN_AFTER_SUBMIT"; write_state(state_path, saved)
            raise SystemExit("submit outcome unknown; reconcile with Tencent, never resubmit")
        job_id = job.get("id")
        if not job_id:
            saved["status"] = "UNKNOWN_NO_JOB_ID"; write_state(state_path, saved)
            raise SystemExit("submit returned no job id; reconcile with Tencent, never resubmit")
        saved.update({"status":"SUBMITTED","id":str(job_id),"request_id":job.get("request_id")})
        write_state(state_path, saved)
    headers = {"Authorization":f"Bearer {key}","Content-Type":"application/json"}
    deadline = time.monotonic() + a.max_wait
    while time.monotonic() < deadline:
        time.sleep(5 + random.random())
        q = Request(manifest["query"], data=json.dumps({"model":"hy-video-1.5","id":job_id}).encode(), method="POST", headers=headers)
        try: state = request_json(q, retryable_query=True)
        except RetryableQuery as e:
            print(e.message); time.sleep(e.delay + random.random()); continue
        status = str(state.get("status", "")).lower()
        if status == "completed": break
        if status in ("failed", "error", "cancelled"):
            saved["status"] = status.upper(); write_state(state_path, saved)
            raise SystemExit(f"provider terminal status: {status}; inspect restricted provider logs")
    else: raise SystemExit(f"poll timeout; resume id {job_id}; do not resubmit")
    result_url = (state.get("data") or {}).get("url")
    if not result_url: raise SystemExit("completed job has no result URL")
    part = output.with_suffix(output.suffix + ".part")
    if part.exists(): raise SystemExit(f"refusing overwrite: {part}")
    sha256, size = download(result_url, suffixes, part)
    try:
        subprocess.run(["ffprobe","-v","error","-show_streams","-show_format",str(part)], check=True)
        subprocess.run(["ffmpeg","-v","error","-i",str(part),"-f","null","-"], check=True)
    except Exception:
        saved["status"] = "VALIDATION_FAILED"; write_state(state_path, saved); raise
    part.replace(output)
    saved.update({"status":"DELIVERED","sha256":sha256,"bytes":size})
    write_state(state_path, saved)
    print(json.dumps({"output":str(output),"sha256":sha256,"bytes":size}))

if __name__ == "__main__": main()
```

Use a separate project API key and do not put it in source, command history, state files, or logs. If TokenHub request logging is enabled, choose audit-only metadata unless raw prompts/inputs/outputs are intentionally required; Tencent warns call logs may contain all of them and incur separate CLS cost/retention. Configure log access and lifecycle explicitly.

### Maintain the legacy adapter only when necessary

The legacy API uses `https://vclm.tencentcloudapi.com`, action `SubmitHunyuanToVideoJob` or `DescribeHunyuanToVideoJob`, version `2024-05-23`, and currently documents only region `ap-guangzhou`. Use official Tencent Cloud SDK/TC3-HMAC-SHA256 with short-lived credentials and CAM operation-level permissions. Do not translate TokenHub bearer keys, lowercase fields, top-level responses, or statuses into the legacy adapter.

New model sales are migrating to TokenHub; the older platform says it will stop adding model capabilities and supporting new purchases while existing purchases remain temporarily available. Build new integrations against TokenHub unless Tencent gives the customer a different supported path.

## Handle cloud assets and governance

- Probe image dimensions, format, size, orientation, rights, and consent before upload. Prefer a short-lived, least-public COS signed URL; do not log it. Base64 avoids a fetch URL but enlarges request/log data.
- The current TokenHub access table distinguishes Guangzhou/China-mainland resource scheduling from Singapore/global scheduling and disallows cross-site calls. This does not by itself establish contractual data residency, retention, or training use. Obtain the current TokenHub privacy policy, service agreement/DPA, subprocessor and deletion terms for regulated or confidential material.
- A 24-hour result URL is an availability window, not proof that prompt/input/output data is deleted. Download, hash, and move the result to customer-controlled storage with an explicit lifecycle.
- Keep AI-generated labeling, consent, likeness, IP, and brand clearance. Tencent's FAQ says outputs may be similar across users; do not promise exclusivity.
- The international SLA describes 99.5% service availability under its calculation and exclusions. Do not convert that to per-job success, latency, queue, or model-quality guarantees.

## Operate HunyuanVideo-1.5 locally

Use the official `Tencent-Hunyuan/HunyuanVideo-1.5` repository and `tencent/HunyuanVideo-1.5` model repository. Pin immutable Git and Hugging Face revisions. The current HF `main` tree is about 372 GB in full; older reviewed revisions were about 338 GB, so inspect the pinned revision's tree and approve an exact file manifest before download.

### Select compatible artifacts

| Task | Base artifact | Acceleration boundary |
|---|---|---|
| 480p T2V | 480P-T2V or 480P-T2V-cfg-distill | CFG-distilled still requires 50 steps; CFG scale 1 |
| 480p I2V | 480P-I2V, CFG-distill, or I2V step-distill | Step-distill is only 480p I2V; use 8 or 12 steps (4 trades quality) |
| 720p T2V | 720P-T2V | Listed 720p T2V CFG/sparse-distilled artifacts were still “coming soon” in the current repo table; do not invent them |
| 720p I2V | 720P-I2V, CFG-distill, or sparse CFG-distill | Sparse attention is 720p/H-series only and requires the matching checkpoint |
| 480→720 or 720→1080 | Separate SR step-distilled transformer | Super-resolution is post-generation; do not call 1080p a native base checkpoint |

The full layout also needs text/vision encoders. Official instructions currently recommend Qwen2.5-VL-7B-Instruct as the MLLM, Google ByT5-small plus ModelScope Glyph-SDXL-v2, and the SigLIP component from gated FLUX.1-Redux-dev. These have separate licenses/access terms. Pin and review each; never assume the Hunyuan license covers them.

### Size hardware honestly

The official inference floor is NVIDIA CUDA, Linux, Python 3.10+, and 14 GB VRAM **with model offloading**. This is not a guarantee for every resolution/length/accelerator, and it is not a training requirement. Offloading shifts pressure to system RAM and transfer time; overlapping group offload can substantially increase RAM. Record actual peak GPU/RAM/disk and latency in a small acceptance run.

The native CLI defaults to 121 frames and the official Diffusers example exports at 24 fps, approximately five seconds. Use frame counts compatible with the 3D VAE (`4n+1`), and validate any longer sequence such as 241 frames before committing capacity. Base generation supports 480p or 720p; `--sr` is a separate upsampling pass and defaults on in the current CLI.

Acceleration choices are not interchangeable:

- Standard and CFG-distilled checkpoints use 50 steps. CFG distillation changes guidance computation, not step count.
- Only the 480p I2V step-distilled checkpoint uses 8 or 12 recommended steps.
- Sparse attention requires H-series GPUs, 720p compatible artifacts, and Flex-Block-Attention; enabling it auto-selects CFG-distilled behavior.
- SageAttention automatically disables Flex-Block-Attention. Do not enable Sage and sparse paths together expecting both.
- FP8 GEMM uses `sgl-kernel==0.3.18` and `--use_fp8_gemm` with a documented quantization type. Test hardware/kernel/checkpoint compatibility and quality before production.
- DeepCache/TeaCache/TaylorCache may improve speed but change the computation path. Benchmark against a non-cached golden seed and retain the exact cache configuration.

HunyuanVideo-1.5 does not generate a supported audio track as part of its T2V/I2V pipeline. Plan sound separately; use HunyuanVideo-Foley for a separately licensed video-to-audio workflow or HunyuanVideo-Avatar/HumanActor for audio-driven people.

### Audit metadata before any download

```bash
git ls-remote https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5.git HEAD
curl -fsS https://huggingface.co/api/models/tencent/HunyuanVideo-1.5 > hunyuanvideo-1.5-metadata.json
# Review territory, license, files, sizes, dependencies, disk, GPU, and approved revisions.
```

After explicit approval, use immutable revisions and the reviewed manifest. This complete example shows the official broad download path; the current tree is roughly 372 GB before encoders, environment, and outputs, and size can change by revision:

```bash
git clone https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5.git
cd HunyuanVideo-1.5
git checkout <reviewed-git-commit>
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
hf download tencent/HunyuanVideo-1.5 --revision <reviewed-hf-commit> --local-dir ./ckpts
hf download Qwen/Qwen2.5-VL-7B-Instruct --revision <reviewed-qwen-commit> --local-dir ./ckpts/text_encoder/llm
hf download google/byt5-small --revision <reviewed-byt5-commit> --local-dir ./ckpts/text_encoder/byt5-small
modelscope download --model AI-ModelScope/Glyph-SDXL-v2 --revision <reviewed-glyph-revision> --local_dir ./ckpts/text_encoder/Glyph-SDXL-v2
hf download black-forest-labs/FLUX.1-Redux-dev --revision <reviewed-flux-commit> --local-dir ./ckpts/vision_encoder/siglip
find ckpts -type f -not -path '*/.cache/*' -print0 | sort -z | xargs -0 -r sha256sum > CHECKPOINTS.sha256
test ! -e outputs/t2v-480.mp4
torchrun --nproc_per_node=1 generate.py \
  --model_path ./ckpts --image_path none --resolution 480p --aspect_ratio 16:9 \
  --video_length 121 --num_inference_steps 50 --seed 42 \
  --prompt 'A slow eye-level dolly follows a red tram through light rain; wet rails reflect warm windows, pedestrians remain distant, and the tram stops smoothly under a station clock, continuous realistic shot.' \
  --negative_prompt 'flicker, warped rails, duplicate tram, abrupt cut, illegible text' \
  --rewrite false --cfg_distilled true --sr false --output_path outputs/t2v-480.mp4
ffprobe -v error -show_streams -show_format outputs/t2v-480.mp4
ffmpeg -v error -i outputs/t2v-480.mp4 -f null -
```

The placeholder revisions must be replaced with reviewed immutable IDs. The broad HF download is intentional in this official-layout example; production should use a reviewed `--include` manifest to fetch only the compatible task/SR components. Do not use shell `find` over untrusted paths; keep the workspace fixed and verify resulting manifest coverage.

Disable prompt rewrite for local/offline privacy. The native repository defaults rewrite on but skips it when no compatible vLLM endpoint exists. If rewrite is intentionally enabled, use a reviewed self-hosted endpoint, record original and rewritten prompts, and treat the rewrite model as another data processor and versioned dependency.

## Apply the local license before deployment

HunyuanVideo-1.5 is not Apache-2.0 or an OSI license. It uses the Tencent Hunyuan Community License Agreement dated with the 2025-11-21 release. Check the actual pinned license with counsel. Consequential current terms include:

- The licensed territory excludes the **European Union, United Kingdom, and South Korea**. Use, reproduction, modification, distribution, display, and even Outputs outside the Territory are unlicensed under this agreement. Do not deploy the open weights or deliver their outputs there without a separate Tencent license.
- A licensee whose products/services exceeded 100 million monthly active users in the month before the version release must request a separate license and receives no grant until Tencent approves.
- Model Derivatives include modifications, distillation, and models trained using weights, intermediate representations, synthetic outputs, or similar pattern transfer to perform similarly. Outputs alone are not Model Derivatives.
- Distribution and hosted-service deployment carry agreement, change-notice, Notice-file, provider-identity, downstream-use, and non-affiliation disclosure duties. Do not imply Tencent sponsors the service.
- Hunyuan Works or outputs may not be used to improve another AI model except Hunyuan/its Model Derivatives.
- Tencent claims no rights in generated Outputs, but gives no title, non-infringement, quality, or fitness warranty; the operator remains responsible.
- The embedded AUP requires machine-generated disclosure for public content and prohibits guardrail circumvention, harmful/deceptive/election manipulation, non-consensual impersonation, high-stakes automated decisions, military use, discrimination, exploitation, and unlicensed professional practice.

Third-party encoders and libraries retain their own terms. A permissively licensed dependency does not relicense the Hunyuan model.

## Prompt and evaluate for motion

For local 1.5, detailed bilingual prompts generally outperform short tags. Describe a single temporal progression: framing and camera, subject appearance, primary action in order, secondary/environmental motion, lighting/color, physical behavior, and final state. For I2V, emphasize motion and change; the input already establishes appearance.

Hosted prompts must stay within the 200-character Chinese-positive-prompt contract. Example:

> 低机位中景，红色电车在细雨中沿湿润轨道缓慢驶近，车窗暖光倒映在地面，镜头平稳后退保持车头居中，远处行人自然走动，电车最终在站钟下平稳停住，写实电影质感，连续镜头。

Do not encode sound cues as if HunyuanVideo-1.5 will render audio. Treat exact text, logos, hands, faces, reflections, contact, rapid motion, and object permanence as review risks.

## Validate every artifact

1. Full-decode the file; inspect duration, frame count/rate, dimensions, codec/profile, color metadata, and stream inventory. Confirm silence or unexpected audio rather than assuming.
2. Review first/middle/last frames and every second at native scale for prompt/input consistency, anatomy, identity, text/logo fidelity, structural stability, temporal flicker, camera motion, physics, contacts, and abrupt cuts.
3. For I2V compare the first frame and intended identity/composition. For SR compare pre-SR and post-SR; reject invented textures, ringing, temporal shimmer, and aspect drift.
4. Record hosted model/site, request and job IDs, charge estimate/actual, disclosure, prompt, image hash, output hash, timestamps, and source URL expiry—or local Git/HF/dependency revisions, checkpoint hashes, hardware, acceleration/offload/cache, seed, original/rewritten prompt, pre/post-SR files, and command.
5. Apply safety, consent, likeness, IP, territory, policy, and synthetic-media disclosure gates before distribution. Keep the default hosted AI mark unless a compliant replacement is approved.

## Re-check first-party sources

- [TokenHub video generation](https://cloud.tencent.com/document/product/1823/130081)
- [TokenHub API endpoints and regions](https://cloud.tencent.com/document/product/1823/130078)
- [TokenHub model list](https://cloud.tencent.com/document/product/1823/130051)
- [TokenHub model pricing](https://cloud.tencent.com/document/product/1823/130055)
- [Submit Hunyuan video action](https://cloud.tencent.com/document/api/1616/126160)
- [Describe Hunyuan video action](https://cloud.tencent.com/document/api/1616/126162)
- [Tencent video-generation billing](https://cloud.tencent.com/document/product/1616/118994)
- [Tencent disclosure/output FAQ](https://cloud.tencent.com/document/product/1616/106109)
- [Official HunyuanVideo-1.5 repository](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5)
- [Official HunyuanVideo-1.5 model repository](https://huggingface.co/tencent/HunyuanVideo-1.5)
- [HunyuanVideo-1.5 technical report](https://arxiv.org/abs/2511.18870)
- [HunyuanVideo-1.5 license and AUP](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/LICENSE)
- [Original HunyuanVideo repository](https://github.com/Tencent-Hunyuan/HunyuanVideo)

Treat model identifiers, endpoint paths, region/site availability, concurrency, prices, input limits, resolution, duration, result lifetime, checkpoint publication, repository flags, dependencies, licenses, policies, and terms as volatile. Record the verification date at every production approval.
