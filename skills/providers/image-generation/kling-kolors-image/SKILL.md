---
name: kling-kolors-image
description: Plan, generate, edit, reference, and quality-control still images with Kling AI's hosted IMAGE surfaces or Kuaishou's open Kolors checkpoints. Use for Kling IMAGE 3.0/3.0 Omni/O1/2.1 web, official Kling CLI/MCP or Open Platform integration, and local Kolors text-to-image, image-to-image, IP-Adapter, ControlNet, inpainting, or LoRA work. Do not use for Kling video, avatars, lip-sync, unofficial gateway APIs, or for assuming that current hosted Kling Image models are identical to the 2024 open Kolors weights.
---

# Produce still images with Kling and Kolors

Begin by resolving the name. “Kling image,” “Kolors,” and “可图” now refer to related but non-interchangeable surfaces.

| Surface | What it is | Appropriate use |
|---|---|---|
| Kling AI IMAGE 3.0 | Current hosted still-image generation and natural-language editing, with multi-reference support | Single stills, product/character continuity, restyling, localized edits |
| Kling AI IMAGE 3.0 Omni | Current hosted narrative-image model with image-series workflows and direct 2K/4K options | Storyboards, connected image sequences, high-resolution masters |
| Kling IMAGE O1 / 2.1 and older Open Platform pages | Earlier hosted workflows that may remain account/API dependent | Reproduce an existing approved pipeline only after live capability discovery |
| Open Kolors checkpoint | A 2024 Kuaishou latent-diffusion model distributed as weights and code | Local bilingual text-to-image and the separately released img2img, IP-Adapter, ControlNet, inpainting, FaceID, and DreamBooth-LoRA workflows |

**Documented fact, verified 2026-07-10:** Kling’s overview says its hosted image capabilities are based on Kuaishou’s Kolors technology, but it does not publish evidence that IMAGE 3.0, IMAGE 3.0 Omni, or O1 is the same checkpoint or API contract as `Kwai-Kolors/Kolors-diffusers`. Never move parameters, licenses, or benchmark conclusions between those surfaces without direct support.

## Frame the production decision

Record a short brief before opening a generation surface:

- deliverable, placement, crop/aspect, required pixels, number of final images, and deadline;
- subject, action, environment, composition, lighting, materials, palette, and any exact visible text;
- whether references control identity, product geometry, pose/composition, environment, or style;
- which details must remain invariant and which may change;
- rights to every reference, trademark/logo constraints, likeness consent, and privacy classification;
- hosted versus local execution, region/account, retention requirement, and cost ceiling;
- pass/fail criteria at full resolution.

Choose the path from the need, not from a version number:

1. Use IMAGE 3.0 for one-off creation, multi-reference composition, style transfer, or a plain-language edit.
2. Use IMAGE 3.0 Omni when the deliverable depends on series mode or a directly generated 2K/4K image. Treat “native” and quality claims as provider descriptions until the returned dimensions and file are inspected.
3. Use local open Kolors when data must stay on controlled infrastructure, deterministic seeds/schedulers matter, or the open adapters are required. Confirm the custom model license before downloading weights.
4. Use an older hosted model only when `who_am_i`, the live console, or the current official API page proves entitlement and parameters. Do not select a legacy model from memory.

Default to one image at the lowest acceptable resolution. Do not turn a sample into a nine-image batch, enable 4K, add references, or change models without re-estimating cost and obtaining approval.

## Know what is actually documented

The following hosted facts were current on 2026-07-10:

- Kling launched IMAGE 3.0 and IMAGE 3.0 Omni globally in February 2026. Official guides describe up to ten reference images for the current 3.0 creation workflow.
- IMAGE 3.0 covers text creation, reference-led creation, style/character/portrait guidance, multi-image blending, and localized natural-language edits.
- IMAGE 3.0 Omni adds text-to-image, image-to-image, and multi-image series workflows plus direct 2K/4K output.
- First-party June 2026 marketing pages are inconsistent about whether direct 2K/4K is unique to Omni or applies across the IMAGE 3.0 family. The model-comparison guide assigns that differentiator to Omni, while other posts describe it more broadly. Confirm the live model selector and returned pixels instead of promising it from the family name.
- The general web image guide supports Chinese and English prompts, JPG/PNG references up to 10 MB with both dimensions at least 300 px, seven listed 1K ratios, and up to nine outputs. Those web limits are not automatically API or CLI limits.
- The current global Open Platform uses `https://api-singapore.klingai.com` for servers outside China. New API keys cover all models; legacy AccessKey/SecretKey JWT credentials cover only 3.0 and earlier models according to the authentication page.
- The official Kling MCP/CLI exposes `who_am_i`, `text_to_image`, `image_to_image`, `query_tasks`, file upload, and credit/membership discovery. Its FAQ says result URLs last 24 hours, submitted tasks cannot be canceled, the assistant-facing interface is limited to 5 QPS, and only paid Personal-workspace credits are currently usable there; bonus and Team-workspace credits are excluded.

The public current image API pages exist for multiple generations, but their client-rendered request tables were not reliably readable without an entitled session during this verification. Therefore:

- use `kling who_am_i`, `kling text_to_image --help`, and `kling image_to_image --help` immediately before constructing a CLI call;
- use the signed-in Open Platform page or exported official example for REST fields and endpoint-specific prices;
- never substitute a fal.ai, Replicate, Kie, PiAPI, Atlas, or other gateway schema for Kling’s native schema;
- treat image model tokens, prices, concurrency, batch maxima, reference encodings, task result shapes, and output hostnames as volatile unless live discovery confirms them.

The former standalone `kolors.kuaishou.com` creation service closed on 2024-08-23 and directed users to the Chinese Kling platform; its notice also said historical creations would not migrate. Do not promise account, credit, asset, or credential portability between the Chinese platform and global `kling.ai`. No current first-party mainland API hostname suitable for general use was verified; obtain it from a Chinese account contract rather than guessing.

## Direct the image in Kling’s vocabulary

Kling’s own beginner guide uses 5W1H as a teaching device. Use it as a coverage check, not a keyword ritual:

```text
Subject and defining features; action or state; environment and time.
Framing, viewpoint, and spatial relationships. Lighting and palette.
Materials or rendering medium. Exact visible text: “...”.
Preserve: [invariants]. Change: [target and desired result].
```

Production heuristics:

- Lead with the subject and relationship that must read first. Put camera, light, and finish after the scene logic.
- Name observable geometry: “three-quarter view, handle visible on the right,” not “dynamic commercial angle.”
- For text, quote the exact string, identify its surface and hierarchy, generate few variants, then inspect every glyph. Provider claims about improved text rendering are not a spelling guarantee.
- Avoid prestige-word piles such as “8K, masterpiece, ultra-detail” when they do not specify a visual property.
- Change one constraint at a time. Save the prompt, chosen surface/model label, account-discovered parameters, references and hashes, output IDs, dimensions, credits, and selection reason.

For a localized edit, use the provider’s direct pattern:

```text
Keep everything else unchanged. Change [specific object/property in a named region]
from [current state] to [desired state]. Preserve [identity, logo geometry,
composition, lighting, shadows, material texture, and background as applicable].
```

For several references, assign each one a role in plain language: “Image 1 supplies the product shape and label; Image 2 supplies the marble surface; Image 3 supplies only the cool window-light mood.” Do not assume that “reference” means identity lock. Higher reference strength on the general web workflow moves the result toward the reference and away from the prompt; tune it by holding the prompt and seed/other controls constant.

For a series, write a continuity sheet before generating:

- immutable character/product facts;
- environment map, time of day, palette, and lens language;
- one action and composition per frame;
- allowed continuity changes between adjacent frames;
- final sequence order and crop-safe zones.

Generate a small continuity proof before a long series. Review adjacent frames together; a strong single image can still fail the sequence.

## Operate the hosted service without inventing a schema

Prefer the official CLI for a terminal workflow and the official MCP for a conversational workflow. Install one, not both, for the same assistant so routing is deterministic. The CLI has separate packages for global-site and China-site accounts; both install `kling`, but credentials and account region are not interchangeable. The official setup documented on 2026-07-10 is:

```bash
npm install -g @klingai/cli-global@0.1.3 --registry=https://registry.npmjs.org
# China-site account only: npm install -g @klingai/cli-cn@0.1.3 --registry=https://registry.npmjs.org
kling login
kling who_am_i
kling text_to_image --help
kling image_to_image --help
```

`kling login` stores an OAuth token under the CLI credential store. Keep that store out of repositories, screenshots, support bundles, and task logs. Pin and record the installed package version and integrity for production. For direct REST, keep an API key or AK/SK only on the server; never embed it in browser/mobile code or send it to an output host.

Before a paid submission:

1. Capture `who_am_i` model and parameter discovery for the intended tool.
2. Obtain the exact credit estimate from the current official console/pricing surface. Image pricing was not stable enough to freeze here.
3. State the model token/label, mode, ratio/resolution, output count, references, and exact generation command/request.
4. Set a finite positive estimate and a finite positive covering ceiling.
5. Produce a hash over that plan and all reference SHA-256 values; wait for the user to approve that hash.
6. Persist the plan before submission. A CLI timeout or malformed response after submission is ambiguous: do not replay automatically. Reconcile with `kling query_tasks`, account history, and credits.

### Complete example: single-use official CLI submission and acquisition

Use the current `@klingai/cli-global` or `@klingai/cli-cn` README plus live `who_am_i` and per-command help. This guard constructs the documented still-image argv itself: positional prompt, explicit `--model`, `--aspectRatio`, `--imgResolution`, and fixed `--imageCount 1`; image-to-image adds one or more local `--image` snapshots. The operator supplies a current-console estimate for that exact argv—the script does not derive provider pricing. Dry run is the default.

Before dry run, capture `kling who_am_i --quiet` and pass its exact JSON with `--who-am-i-json`. Use a fresh UUIDv4 attempt ID, an operator-reviewed result-host allowlist, and a scanner argv containing exactly one `{path}` placeholder. Approve the printed hash once. Execution rechecks the CLI path/hash/version and full `who_am_i` document, claims the attempt with `O_EXCL`, and cannot be replayed or run concurrently under that attempt ID.

```python
#!/usr/bin/env python3
import argparse, hashlib, http.client, io, ipaddress, json, math, os, shutil
import socket, ssl, stat, subprocess, tempfile, threading, time, uuid
from pathlib import Path
from urllib.parse import urlsplit
from PIL import Image, UnidentifiedImageError

MAX_REFERENCE_BYTES = 10 * 1024 * 1024
MAX_PIXELS = 40_000_000
MAX_CLI_BYTES = 1024 * 1024
Image.MAX_IMAGE_PIXELS = MAX_PIXELS

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                prefix=path.name, suffix=".tmp", delete=False) as f:
            tmp = Path(f.name); os.chmod(tmp, 0o600)
            json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path); tmp = None
    finally:
        if tmp is not None and tmp.exists(): tmp.unlink()

def claim_once(path, value):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            fd = None
            json.dump(value, f, sort_keys=True); f.flush(); os.fsync(f.fileno())
    finally:
        if fd is not None: os.close(fd)

def read_json(path, cap=MAX_CLI_BYTES):
    raw = path.read_bytes()
    if not raw or len(raw) > cap: raise ValueError("ledger JSON size rejected")
    try: value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("ledger JSON invalid") from exc
    if not isinstance(value, dict): raise ValueError("ledger JSON must be an object")
    return value

class LaunchError(Exception): pass

def run_bounded(argv, timeout, cap=MAX_CLI_BYTES, stdout_json_callback=None):
    try:
        proc = subprocess.Popen(argv, shell=False, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as exc:
        raise LaunchError(str(exc)) from exc
    out, err, lock, overflow = bytearray(), bytearray(), threading.Lock(), threading.Event()
    callback_done, callback_error = False, []
    total = 0
    def drain(stream, bucket, inspect_json=False):
        nonlocal total, callback_done
        while True:
            chunk = stream.read1(65536) if hasattr(stream, "read1") else stream.read(65536)
            if not chunk: break
            candidate = None
            with lock:
                room = max(0, cap - total); bucket.extend(chunk[:room]); total += len(chunk)
                if total > cap: overflow.set()
                if inspect_json and stdout_json_callback is not None and not callback_done:
                    candidate = bytes(out)
            if candidate is not None:
                try: text = candidate.decode("utf-8-sig")
                except UnicodeDecodeError: text = ""
                candidates = [text] + [line for line in text.splitlines() if line.strip()]
                for item in candidates:
                    try: value = json.loads(item)
                    except json.JSONDecodeError: continue
                    try: callback_done = bool(stdout_json_callback(value))
                    except BaseException as exc:
                        callback_error.append(exc); overflow.set(); break
                    if callback_done: break
            if overflow.is_set():
                try: proc.kill()
                except OSError: pass
    threads = [threading.Thread(target=drain, args=(proc.stdout, out, True), daemon=True),
               threading.Thread(target=drain, args=(proc.stderr, err, False), daemon=True)]
    for thread in threads: thread.start()
    timed_out = False
    try: code = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True; proc.kill(); code = proc.wait()
    for thread in threads: thread.join()
    if callback_error: raise RuntimeError("could not persist generation ID from stdout") from callback_error[0]
    return {"launched": True, "code": code, "stdout": bytes(out), "stderr": bytes(err),
            "timeout": timed_out, "overflow": overflow.is_set()}

def require_good(run, stage):
    if run["timeout"] or run["overflow"] or run["code"] != 0:
        raise RuntimeError(f"{stage} failed or exceeded a local bound")
    try: return json.loads(run["stdout"].decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{stage} returned invalid JSON") from exc

def cli_fingerprint():
    found = shutil.which("kling")
    if not found: raise ValueError("kling is not on PATH")
    path = Path(found).resolve(strict=True)
    if not path.is_file() or not 0 < path.stat().st_size <= 16 * 1024 * 1024:
        raise ValueError("unexpected CLI launcher size")
    data = path.read_bytes()
    run = run_bounded([str(path), "--version"], 30, 65536)
    if run["timeout"] or run["overflow"] or run["code"] != 0: raise ValueError("cannot verify CLI version")
    version = run["stdout"].decode("utf-8", "strict").strip()
    if not version or len(version) > 200: raise ValueError("invalid CLI version output")
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "version": version}

def load_reference(path):
    if path.is_symlink(): raise ValueError("reference symlinks are rejected")
    resolved = path.resolve(strict=True)
    with resolved.open("rb") as f:
        info = os.fstat(f.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_REFERENCE_BYTES:
            raise ValueError("reference must be a bounded regular file")
        data = f.read(MAX_REFERENCE_BYTES + 1)
    if len(data) != info.st_size: raise ValueError("reference changed while reading")
    head = data[:12]
    if head.startswith(b"\xff\xd8\xff"): fmt, exts, mime = "JPEG", {"jpg", "jpeg"}, "image/jpeg"
    elif head.startswith(b"\x89PNG\r\n\x1a\n"): fmt, exts, mime = "PNG", {"png"}, "image/png"
    else: raise ValueError("reference must be JPEG or PNG by signature")
    if resolved.suffix.lower().lstrip(".") not in exts: raise ValueError("extension/signature mismatch")
    try:
        with Image.open(io.BytesIO(data)) as im:
            dims, decoded = im.size, im.format
            if min(dims) < 300 or dims[0] * dims[1] > MAX_PIXELS: raise ValueError("reference dimensions rejected")
            im.verify()
        with Image.open(io.BytesIO(data)) as im: im.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError("reference did not fully decode") from exc
    if decoded != fmt: raise ValueError("decoder/signature mismatch")
    return resolved, data, {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                            "dimensions": list(dims), "mime": mime}

def build_argv(cli, operation, model, prompt, ratio, resolution, references):
    argv = [cli, operation, "--model", model]
    for reference in references: argv += ["--image", reference]
    return argv + [prompt, "--aspectRatio", ratio, "--imgResolution", resolution,
                   "--imageCount", "1", "--quiet"]

def find_first(value, keys):
    if isinstance(value, dict):
        for key in keys:
            if key in value: return value[key]
        for child in value.values():
            found = find_first(child, keys)
            if found is not None: return found
    elif isinstance(value, list):
        for child in value:
            found = find_first(child, keys)
            if found is not None: return found
    return None

def generation_id_from(value):
    generation_id = find_first(value, ("generation_id", "generationId"))
    if generation_id is None: return None
    if not isinstance(generation_id, str) or not generation_id.strip() or len(generation_id) > 512:
        raise ValueError("generation_id invalid")
    return generation_id.strip()

def task_state(value):
    raw = find_first(value, ("task_status", "taskStatus", "status", "state"))
    status = str(raw).strip().lower() if raw is not None else "unknown"
    if status in {"success", "succeed", "succeeded", "complete", "completed"}: return "success"
    if status in {"failed", "failure", "rejected", "cancelled", "canceled"}: return "failure"
    if status in {"submitted", "queued", "pending", "processing", "running"}: return "nonterminal"
    return "unknown"

def result_url(value):
    works = find_first(value, ("works",))
    if not isinstance(works, list) or len(works) != 1 or not isinstance(works[0], dict):
        raise ValueError("success must contain exactly one work")
    url = works[0].get("url")
    if not isinstance(url, str) or not url: raise ValueError("work URL missing")
    return url, works[0].get("work_id") or works[0].get("id")

def allowed_host(host, rules):
    for rule in rules:
        rule = rule.lower().rstrip(".")
        if rule.startswith(".") and (host == rule[1:] or host.endswith(rule)): return True
        if host == rule: return True
    return False

class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, ip, timeout=30):
        super().__init__(host, 443, timeout=timeout, context=ssl.create_default_context()); self.ip = ip
    def connect(self):
        sock = socket.create_connection((self.ip, self.port), self.timeout)
        self.sock = self._context.wrap_socket(sock, server_hostname=self.host)

def acquire(url, attempt_dir, rules, byte_cap, scanner_template):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.username or parsed.password or parsed.fragment or parsed.port not in (None, 443):
        raise ValueError("result URL policy violation")
    host = (parsed.hostname or "").encode("idna").decode("ascii").lower().rstrip(".")
    if not host or not allowed_host(host, rules): raise ValueError("result host is not allowlisted")
    addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)})
    if not addresses or any(not ipaddress.ip_address(item).is_global for item in addresses):
        raise ValueError("result DNS is not globally routable")
    conn, tmp = PinnedHTTPSConnection(host, addresses[0]), None
    try:
        target = parsed.path or "/"
        if parsed.query: target += "?" + parsed.query
        conn.request("GET", target, headers={"Accept": "image/png,image/jpeg", "User-Agent": "kling-artifact-guard/1"})
        response = conn.getresponse()
        if 300 <= response.status < 400: raise ValueError("redirects are rejected")
        if response.status != 200: raise ValueError("artifact request failed")
        mime = response.getheader("Content-Type", "").split(";", 1)[0].lower()
        if mime not in {"image/png", "image/jpeg"}: raise ValueError("artifact MIME rejected")
        length = response.getheader("Content-Length")
        if length is not None and (not length.isdigit() or int(length) > byte_cap): raise ValueError("declared size rejected")
        digest, total = hashlib.sha256(), 0
        with tempfile.NamedTemporaryFile("wb", dir=attempt_dir, prefix="artifact-", suffix=".part", delete=False) as f:
            tmp = Path(f.name); os.chmod(tmp, 0o600)
            while True:
                chunk = response.read(65536)
                if not chunk: break
                total += len(chunk)
                if total > byte_cap: raise ValueError("streamed size rejected")
                digest.update(chunk); f.write(chunk)
            f.flush(); os.fsync(f.fileno())
        head = tmp.read_bytes()[:12]
        if head.startswith(b"\xff\xd8\xff"): fmt, expected_mime, suffix = "JPEG", "image/jpeg", ".jpg"
        elif head.startswith(b"\x89PNG\r\n\x1a\n"): fmt, expected_mime, suffix = "PNG", "image/png", ".png"
        else: raise ValueError("artifact signature rejected")
        if mime != expected_mime: raise ValueError("MIME/signature mismatch")
        with Image.open(tmp) as image:
            dims, decoded = image.size, image.format
            if dims[0] * dims[1] > MAX_PIXELS: raise ValueError("artifact pixel cap exceeded")
            image.verify()
        with Image.open(tmp) as image: image.load()
        if decoded != fmt: raise ValueError("artifact decoder/signature mismatch")
        scanner_argv = [str(tmp) if item == "{path}" else item for item in scanner_template]
        scan = run_bounded(scanner_argv, 300, MAX_CLI_BYTES)
        if scan["timeout"] or scan["overflow"] or scan["code"] != 0: raise ValueError("scanner rejected artifact")
        destination = attempt_dir / ("artifact" + suffix)
        if destination.exists(): raise ValueError("artifact destination already exists")
        os.replace(tmp, destination); tmp = None
        return {"path": str(destination), "sha256": digest.hexdigest(), "bytes": total,
                "dimensions": list(dims), "mime": expected_mime, "sourceHost": host,
                "connectedIp": addresses[0], "scannerOutputSha256":
                hashlib.sha256(scan["stdout"] + scan["stderr"]).hexdigest()}
    finally:
        conn.close()
        if tmp is not None and tmp.exists(): tmp.unlink()

parser = argparse.ArgumentParser()
parser.add_argument("--operation", choices=("text_to_image", "image_to_image"), required=True)
parser.add_argument("--region", choices=("global", "china"), required=True)
parser.add_argument("--attempt-id", required=True)
parser.add_argument("--who-am-i-json", required=True)
parser.add_argument("--model", required=True); parser.add_argument("--prompt", required=True)
parser.add_argument("--aspect-ratio", required=True); parser.add_argument("--img-resolution", required=True)
parser.add_argument("--reference", action="append", type=Path, default=[])
parser.add_argument("--estimated-credits", type=float, required=True)
parser.add_argument("--max-credits", type=float, required=True)
parser.add_argument("--allowed-result-host", action="append", default=[])
parser.add_argument("--max-artifact-bytes", type=int, default=50 * 1024 * 1024)
parser.add_argument("--scanner-argv-json", required=True)
parser.add_argument("--query-timeout", type=int, default=1800)
parser.add_argument("--run-dir", type=Path, default=Path("kling-runs"))
parser.add_argument("--execute", action="store_true")
parser.add_argument("--resume", action="store_true", help="query only an already claimed attempt with a recorded generation ID")
args = parser.parse_args()
try: attempt = uuid.UUID(args.attempt_id); who_am_i = json.loads(args.who_am_i_json); scanner = json.loads(args.scanner_argv_json)
except (ValueError, json.JSONDecodeError) as exc: raise SystemExit("attempt/identity/scanner input invalid") from exc
if attempt.version != 4 or str(attempt) != args.attempt_id.lower(): raise SystemExit("attempt-id must be canonical UUIDv4")
if not isinstance(who_am_i, dict): raise SystemExit("who-am-i-json must be the exact JSON object")
if not isinstance(scanner, list) or not scanner or not all(isinstance(x, str) and x for x in scanner) or scanner.count("{path}") != 1:
    raise SystemExit("scanner argv must be a string array with one {path}")
if not math.isfinite(args.estimated_credits) or args.estimated_credits <= 0: raise SystemExit("estimate must be finite and positive")
if not math.isfinite(args.max_credits) or args.max_credits <= 0 or args.estimated_credits > args.max_credits:
    raise SystemExit("covering ceiling must be finite and positive")
if not 0 < args.max_artifact_bytes <= 250 * 1024 * 1024 or not 1 <= args.query_timeout <= 7200:
    raise SystemExit("output policy bounds rejected")
if args.resume and not args.execute: raise SystemExit("--resume requires --execute")
if args.operation == "text_to_image" and args.reference: raise SystemExit("text_to_image cannot have references")
if args.operation == "image_to_image" and not args.reference: raise SystemExit("image_to_image requires references")
cli = cli_fingerprint(); loaded = [load_reference(path) for path in args.reference]
run_root = args.run_dir.resolve()
attempt_dir = run_root / str(attempt)
placeholders = [f"<reference:{item[2]['sha256']}>" for item in loaded]
argv = build_argv(cli["path"], args.operation, args.model, args.prompt, args.aspect_ratio, args.img_resolution, placeholders)
policy = {"imageCount": 1, "urlField": "works[0].url", "allowedHosts": sorted(set(args.allowed_result_host)),
          "httpsOnly": True, "redirects": False, "maxBytes": args.max_artifact_bytes,
          "maxPixels": MAX_PIXELS, "scannerArgv": scanner}
plan = {"attemptId": str(attempt), "region": args.region, "cli": cli, "whoAmI": who_am_i,
        "runRoot": str(run_root), "attemptDirectory": str(attempt_dir),
        "argv": argv, "settings": {"model": args.model, "aspectRatio": args.aspect_ratio,
        "imgResolution": args.img_resolution, "imageCount": 1},
        "promptSha256": hashlib.sha256(args.prompt.encode()).hexdigest(),
        "references": [item[2] for item in loaded], "estimatedCredits": args.estimated_credits,
        "maxCredits": args.max_credits, "costBasis": "operator estimate from current console for exact argv",
        "outputPolicy": policy}
approval = hashlib.sha256(canonical(plan)).hexdigest()
print(json.dumps({"dryRun": not args.execute, "approvalSha256": approval, "plan": plan}, indent=2))
if not args.execute: raise SystemExit(0)
if not policy["allowedHosts"]: raise SystemExit("execution requires an operator-reviewed result-host allowlist")
if os.environ.get("KLING_APPROVED_SHA256") != approval: raise SystemExit("approval hash mismatch")
if cli_fingerprint() != cli: raise SystemExit("CLI identity changed after approval")
live_identity_run = run_bounded([cli["path"], "who_am_i", "--quiet"], 60)
live_identity = require_good(live_identity_run, "who_am_i")
if canonical(live_identity) != canonical(who_am_i): raise SystemExit("account/workspace/capabilities changed after approval")
run_root.mkdir(parents=True, exist_ok=True)
if run_root.resolve(strict=True) != Path(plan["runRoot"]): raise SystemExit("approved run root changed")
if attempt_dir.parent.resolve(strict=True) != run_root.resolve(strict=True): raise SystemExit("attempt directory escaped approved run root")
ledger = attempt_dir / "submission.json"
def ledger_value(state, **extra):
    value = {"state": state, "approvalSha256": approval, "attemptId": str(attempt),
             "runRoot": str(run_root), "updatedUnix": time.time()}
    value.update(extra); return value

if args.resume:
    if not attempt_dir.is_dir(): raise SystemExit("approved attempt directory does not exist")
    claim = read_json(attempt_dir / "claim.json"); current = read_json(ledger)
    for record in (claim, current):
        if record.get("approvalSha256") != approval or record.get("attemptId") != str(attempt) or record.get("runRoot") != str(run_root):
            raise SystemExit("attempt record does not match this approval and run root")
    generation_id = generation_id_from(current)
    if generation_id is None: raise SystemExit("ambiguous attempt has no recoverable generation ID; do not create")
else:
    attempt_dir.mkdir(mode=0o700, parents=False, exist_ok=True)
    claim_once(attempt_dir / "claim.json", ledger_value("claimed"))
    atomic_json(ledger, ledger_value("claimed", plan=plan))
    observed = {"generationId": None}
    def persist_generation_id(value):
        generation_id = generation_id_from(value)
        if generation_id is None: return False
        if observed["generationId"] not in (None, generation_id): raise RuntimeError("conflicting generation IDs")
        observed["generationId"] = generation_id
        atomic_json(ledger, ledger_value("generation_id_observed", generationId=generation_id,
                    note="Create is consumed; query this ID only"))
        return True
    try:
        with tempfile.TemporaryDirectory(prefix="kling-approved-") as td:
            private = Path(td); os.chmod(private, 0o700); snapshot_paths = []
            for index, (_, data, evidence) in enumerate(loaded):
                snapshot = private / f"reference-{index}.img"
                with snapshot.open("xb") as f:
                    os.chmod(snapshot, 0o600); f.write(data); f.flush(); os.fsync(f.fileno())
                if hashlib.sha256(snapshot.read_bytes()).hexdigest() != evidence["sha256"]: raise RuntimeError("snapshot mismatch")
                snapshot_paths.append(str(snapshot))
            exec_argv = build_argv(cli["path"], args.operation, args.model, args.prompt,
                                   args.aspect_ratio, args.img_resolution, snapshot_paths)
            atomic_json(ledger, ledger_value("submitting"))
            try: submitted = run_bounded(exec_argv, 1800, stdout_json_callback=persist_generation_id)
            except LaunchError:
                atomic_json(ledger, ledger_value("local_launch_failed_consumed")); raise
            submit_json = None
            try: submit_json = json.loads(submitted["stdout"].decode("utf-8-sig"))
            except (UnicodeDecodeError, json.JSONDecodeError): pass
            if submit_json is not None: persist_generation_id(submit_json)
            if submitted["timeout"] or submitted["overflow"] or submitted["code"] != 0:
                raise RuntimeError("submission outcome is ambiguous")
            submit_json = require_good(submitted, "submission")
            generation_id = generation_id_from(submit_json)
            if generation_id is None: raise RuntimeError("generation_id missing")
            atomic_json(ledger, ledger_value("submitted", generationId=generation_id, submitOutputSha256=
                        hashlib.sha256(submitted["stdout"] + submitted["stderr"]).hexdigest()))
    except LaunchError as exc: raise SystemExit(f"CLI did not launch; attempt is consumed: {exc}") from exc
    except BaseException as exc:
        current = ledger_value("ambiguous", note="Never resubmit; reconcile query_tasks/account credits")
        if observed["generationId"] is not None: current["generationId"] = observed["generationId"]
        if "submitted" in locals():
            current.update({"submitOutputSha256": hashlib.sha256(submitted["stdout"] + submitted["stderr"]).hexdigest(),
                            "submitExitCode": submitted["code"], "submitTimedOut": submitted["timeout"],
                            "submitOverflow": submitted["overflow"]})
        atomic_json(ledger, current); raise SystemExit("post-launch outcome is ambiguous") from exc

deadline, failures, terminal = time.monotonic() + args.query_timeout, 0, None
while time.monotonic() < deadline:
    try:
        queried = run_bounded([cli["path"], "query_tasks", generation_id, "--quiet"], 60)
        query_json = require_good(queried, "query_tasks"); failures = 0
        state = task_state(query_json)
        if state in {"success", "failure"}: terminal = state; break
    except (LaunchError, RuntimeError):
        failures += 1
        if failures >= 3: break
    time.sleep(min(10, 2 ** failures))
if terminal != "success":
    atomic_json(ledger, ledger_value("terminal_failure" if terminal == "failure" else "submitted_unreconciled",
                generationId=generation_id,
                note="Do not create a duplicate; query this generation ID"))
    raise SystemExit("task did not reach a retrievable success")
try:
    url, work_id = result_url(query_json)
    artifact = acquire(url, attempt_dir, policy["allowedHosts"], policy["maxBytes"], scanner)
    manifest = {"generationId": generation_id, "workId": work_id, "artifact": artifact,
                "model": args.model, "settings": plan["settings"], "references": plan["references"],
                "estimatedCredits": args.estimated_credits, "approvalSha256": approval,
                "review": {"syntheticDisclosure": "required", "creativeQa": "pending", "rightsReview": "required"}}
    atomic_json(attempt_dir / "manifest.json", manifest)
    atomic_json(ledger, ledger_value("artifact_saved", generationId=generation_id,
                artifactSha256=artifact["sha256"]))
    print(json.dumps(manifest, indent=2))
except BaseException as exc:
    atomic_json(ledger, ledger_value("artifact_failed", generationId=generation_id,
                note="Recover this task; never regenerate solely for the artifact"))
    raise SystemExit("task succeeded but secure artifact acquisition failed") from exc
```

The wrapper never prints or persists raw task JSON or signed URLs. Its approval binds the resolved run root and attempt directory, and every claim/ledger record repeats that root so copying the same UUID and approval elsewhere cannot authorize execution. It streams bounded CLI output and persists any complete `generation_id` JSON as soon as it appears—even if the process later times out, floods output, or exits nonzero. `--resume --execute` verifies the same approval/root records and issues `query_tasks` only; it never enters the create branch. The wrapper pins the validated public DNS address through TLS hostname verification, rejects redirects, validates declared and streamed size plus MIME/signature/full decode/pixels, runs an exact approved scanner command, and atomically promotes the artifact and allowlisted manifest. The consumed attempt remains consumed after every failure. Recover an existing `generation_id`; never make a replacement generation merely to obtain another URL.

## Run the open Kolors checkpoint deliberately

The first-party repository describes Kolors as a bilingual Chinese/English latent-diffusion model with a 256-token context. Its 2024 evaluation used more than 1,000 prompts, 14 categories, 12 dimensions, and 50 image experts; treat the reported results as the team’s own April-2024-version benchmark, not a current universal ranking.

The repository recommends the default Euler scheduler at guidance 5.0 and 50 steps, or EDM DPM-Solver Multistep at guidance 5.0 and 25 steps. It separately publishes img2img, IP-Adapter-Plus, FaceID-Plus, Canny/depth/pose ControlNets, inpainting, and DreamBooth-LoRA. Select one control mechanism at a time before combining them.

### Complete example: local bilingual text-to-image

This example is dry-run-first, refuses an implicit network download, and binds an immutable 40-hex checkpoint commit, dependency-lock hash, and reviewed `MODEL_LICENSE` hash to approval. It uses the provider-recommended Euler/50-step baseline and records actual runtime versions. It is an example, not a claim that these settings fit every prompt.

The dependency lock is UTF-8 JSON with schema `kolors-runtime-lock/v1`. It contains exactly `schema`, `python`, and `packages`; `python` contains exact `implementation` and `version` strings, and every package entry contains exact `version` and `recordSha256` values. `recordSha256` is the lowercase SHA-256 of the installed distribution's UTF-8 `RECORD` text. The lock must cover at least `torch`, `diffusers`, `transformers`, and `Pillow`; every listed distribution is checked before any ML module is imported. For example:

```json
{
  "schema": "kolors-runtime-lock/v1",
  "python": {"implementation": "CPython", "version": "3.11.9"},
  "packages": {
    "torch": {"version": "2.2.1", "recordSha256": "<64 lowercase hex>"},
    "diffusers": {"version": "0.25.0", "recordSha256": "<64 lowercase hex>"},
    "transformers": {"version": "4.37.2", "recordSha256": "<64 lowercase hex>"},
    "Pillow": {"version": "10.2.0", "recordSha256": "<64 lowercase hex>"}
  }
}
```

```python
#!/usr/bin/env python3
import argparse, hashlib, importlib.metadata, json, os, platform, re, stat, tempfile
from pathlib import Path

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()

def evidence(path, cap):
    if path.is_symlink(): raise ValueError("symlinks are rejected")
    resolved = path.resolve(strict=True)
    with resolved.open("rb") as f:
        info = os.fstat(f.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= cap: raise ValueError("evidence file rejected")
        data = f.read(cap + 1)
    if len(data) != info.st_size: raise ValueError("evidence file changed while reading")
    return resolved, data, hashlib.sha256(data).hexdigest()

def validate_dependency_lock(path, data, digest):
    try: lock = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("dependency lock must be UTF-8 JSON") from exc
    if not isinstance(lock, dict) or set(lock) != {"schema", "python", "packages"}:
        raise ValueError("dependency lock keys rejected")
    if lock["schema"] != "kolors-runtime-lock/v1": raise ValueError("dependency lock schema rejected")
    python_spec = lock["python"]
    if not isinstance(python_spec, dict) or set(python_spec) != {"implementation", "version"}:
        raise ValueError("dependency lock Python record rejected")
    actual_python = {"implementation": platform.python_implementation(), "version": platform.python_version()}
    if python_spec != actual_python: raise ValueError("Python runtime does not match dependency lock")
    packages = lock["packages"]
    if not isinstance(packages, dict) or not packages: raise ValueError("dependency packages rejected")
    validated = {}
    for requested_name, spec in packages.items():
        if not isinstance(requested_name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", requested_name):
            raise ValueError("dependency distribution name rejected")
        normalized = re.sub(r"[-_.]+", "-", requested_name).lower()
        if normalized in validated: raise ValueError("duplicate normalized dependency name")
        if not isinstance(spec, dict) or set(spec) != {"version", "recordSha256"}:
            raise ValueError("dependency package record rejected")
        version, expected_record = spec["version"], spec["recordSha256"]
        if not isinstance(version, str) or not version or len(version) > 200:
            raise ValueError("dependency version rejected")
        if not isinstance(expected_record, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_record):
            raise ValueError("dependency RECORD hash rejected")
        try: distribution = importlib.metadata.distribution(requested_name)
        except importlib.metadata.PackageNotFoundError as exc:
            raise ValueError(f"locked distribution is not installed: {requested_name}") from exc
        record = distribution.read_text("RECORD")
        if not isinstance(record, str) or not record: raise ValueError(f"installed distribution lacks RECORD: {requested_name}")
        actual_record = hashlib.sha256(record.encode("utf-8")).hexdigest()
        if distribution.version != version or actual_record != expected_record:
            raise ValueError(f"installed distribution does not match lock: {requested_name}")
        validated[normalized] = {"distribution": distribution.metadata["Name"], "version": distribution.version,
                                 "recordSha256": actual_record}
    required = {"torch", "diffusers", "transformers", "pillow"}
    if not required.issubset(validated): raise ValueError("dependency lock omits a required distribution")
    return {"path": str(path), "sha256": digest, "schema": lock["schema"],
            "python": actual_python, "validatedPackages": validated}

def atomic_json(path, value):
    tmp = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, suffix=".tmp", delete=False) as f:
            tmp = Path(f.name); os.chmod(tmp, 0o600)
            json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path); tmp = None
    finally:
        if tmp is not None and tmp.exists(): tmp.unlink()

parser = argparse.ArgumentParser()
parser.add_argument("--prompt", required=True)
parser.add_argument("--negative", default="")
parser.add_argument("--seed", type=int, default=66)
parser.add_argument("--output", type=Path, default=Path("kolors-output.png"))
parser.add_argument("--revision", required=True, help="immutable 40-hex Hugging Face commit")
parser.add_argument("--dependency-lock", type=Path, required=True)
parser.add_argument("--model-license", type=Path, required=True)
parser.add_argument("--allow-download", action="store_true")
parser.add_argument("--execute", action="store_true")
args = parser.parse_args()
if not re.fullmatch(r"[0-9a-fA-F]{40}", args.revision): raise SystemExit("revision must be an immutable 40-hex commit")
lock_path, lock_data, lock_hash = evidence(args.dependency_lock, 10 * 1024 * 1024)
license_path, _, license_hash = evidence(args.model_license, 1024 * 1024)
try: lock_info = validate_dependency_lock(lock_path, lock_data, lock_hash)
except ValueError as exc: raise SystemExit(f"dependency lock validation failed: {exc}") from exc
target = args.output.resolve()
plan = {"checkpoint": "Kwai-Kolors/Kolors-diffusers", "revision": args.revision.lower(),
        "scheduler": "EulerDiscreteScheduler",
        "guidanceScale": 5.0, "steps": 50, "seed": args.seed,
        "promptSha256": hashlib.sha256(args.prompt.encode()).hexdigest(),
        "negativeSha256": hashlib.sha256(args.negative.encode()).hexdigest(),
        "output": str(target), "allowDownload": args.allow_download,
        "dependencyLock": lock_info,
        "modelLicense": {"path": str(license_path), "sha256": license_hash}}
approval = hashlib.sha256(canonical(plan)).hexdigest()
print(json.dumps({"dryRun": not args.execute, "approvalSha256": approval, "plan": plan}, indent=2))
if not args.execute: raise SystemExit(0)
if os.environ.get("KOLORS_APPROVED_SHA256") != approval: raise SystemExit("plan approval mismatch")
if os.environ.get("KOLORS_MODEL_LICENSE_ACCEPTED_SHA256") != license_hash:
    raise SystemExit("review MODEL_LICENSE and accept this exact SHA-256")
if target.exists() or target.with_suffix(target.suffix + ".json").exists(): raise SystemExit("output already exists")

import PIL, diffusers, torch, transformers
from diffusers import EulerDiscreteScheduler, KolorsPipeline
from PIL import Image
module_versions = {"torch": str(torch.__version__), "diffusers": str(diffusers.__version__),
                   "transformers": str(transformers.__version__), "pillow": str(PIL.__version__)}
for name, version in module_versions.items():
    if version != lock_info["validatedPackages"][name]["version"]:
        raise SystemExit(f"imported module version does not match validated lock: {name}")
Image.MAX_IMAGE_PIXELS = 40_000_000
pipe = KolorsPipeline.from_pretrained(
    plan["checkpoint"], torch_dtype=torch.float16, variant="fp16",
    revision=plan["revision"], local_files_only=not args.allow_download,
).to("cuda")
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
generator = torch.Generator(device=pipe.device).manual_seed(args.seed)
image = pipe(prompt=args.prompt, negative_prompt=args.negative, guidance_scale=5.0,
             num_inference_steps=50, generator=generator).images[0]
target.parent.mkdir(parents=True, exist_ok=True)
with tempfile.NamedTemporaryFile(dir=target.parent, suffix=".png", delete=False) as f:
    tmp = Path(f.name)
try:
    image.save(tmp, format="PNG")
    with Image.open(tmp) as check:
        dimensions = list(check.size)
        if check.size[0] * check.size[1] > Image.MAX_IMAGE_PIXELS: raise ValueError("pixel cap exceeded")
        check.verify()
    with Image.open(tmp) as check: check.load()
    digest = hashlib.sha256(tmp.read_bytes()).hexdigest()
    os.replace(tmp, target)
finally:
    if tmp.exists(): tmp.unlink()
manifest = dict(plan, artifact={"path": str(target), "sha256": digest,
                                 "dimensions": dimensions, "mime": "image/png"},
                runtime={"python": lock_info["python"], "modules": module_versions,
                         "dependencyLockSha256": lock_info["sha256"],
                         "validatedPackages": lock_info["validatedPackages"]},
                review={"syntheticDisclosure": "required", "creativeQa": "pending",
                        "rightsReview": "required"})
manifest_path = target.with_suffix(target.suffix + ".json")
try: atomic_json(manifest_path, manifest)
except BaseException:
    if target.exists(): target.unlink()
    raise
print(json.dumps(manifest, indent=2))
```

Local execution avoids sending prompts/references to Kling, but it does not remove licensing, dataset, consent, safety, disclosure, or output-review duties. Pin the checkpoint revision and dependency versions for reproducibility; a seed is not a cross-hardware or cross-version byte-identity guarantee.

## Treat failures by stage

| Failure | Response |
|---|---|
| Capability/model missing from `who_am_i` | Stop; choose an entitled current model only with user approval |
| Invalid prompt/reference/ratio | Fix locally; do not retry unchanged |
| Auth failure | Rotate or correct server-side credential; never print it |
| Content moderation failure | Do not evade filters; revise or reject against policy and rights |
| Credit/resource depletion | Stop; do not auto-purchase or switch workspace |
| 429 / concurrency code 1303 | Respect live package limit; bounded backoff with jitter |
| 5xx/read failure while querying | Retry the read with bounded backoff |
| Timeout/5xx/malformed response after create | Treat as ambiguous; reconcile history, task query, and deductions before resubmission |
| Expired 24-hour result URL | Re-query the existing task if supported; do not create a duplicate solely to recover a URL |
| Local CUDA OOM | Reduce dimensions/batch, enable documented memory controls, or change hardware with approval; preserve the prompt/seed/config |

Public documentation does not promise a native create idempotency key for every current image surface. Never infer one from a gateway or from a client-generated label.

## Govern rights, data, and disclosure

Separate hosted-service terms from the open-model license.

For the paid global API, the terms effective 2026-04-21 say Kling will not use customer data to train or improve models, treats prompts/responses as a data processor, and logs prompts and responses for 30 days. The API privacy policy says data is stored on servers in Singapore, may be accessed by global support/engineering/moderation teams and transferred internationally, and otherwise uses purpose/legal-need retention with deletion exceptions. Do not generalize the paid-API no-training promise to the consumer web app, Chinese service, feedback programs, public sharing, or an unrelated contract.

The global consumer terms effective 2026-04-21 say the user owns Content under applicable law or it belongs to the rightful owner, while Kling does not claim ownership. Ownership is not the whole permission analysis: those terms also grant Kling broad operational and development rights in Content, expressly allow use of Input for model development/training, prohibit commercial use, reproduction, distribution, modification, and derivatives of Output without written permission, and require Kling branding or a prominent “generated by Kling AI” indication. The paid-API terms separately say commercial use of API output is not restricted; the paid-member policy may separately authorize member output subject to its own restrictions. Determine whether the run is consumer web, a paid member, paid API, or an enterprise order before uploading private references or approving commercial distribution. This is operational guidance, not legal advice.

For open Kolors:

- repository code is Apache-2.0, but weights and derivatives use the separate `MODEL_LICENSE`;
- commercial users must register with the licensor when their and affiliates’ aggregate products/services stay at or below 300 million monthly active users; above that threshold they need an express license before exercising rights;
- the license requires source/license notices for distribution, imposes use restrictions, says outputs alone are not model derivatives, and prohibits using the model works or outputs to improve another model except Kolors/model derivatives;
- the model and outputs are provided without accuracy, safety, non-infringement, or fitness warranties.

In every path, obtain rights to inputs and consent for recognizable people. Do not use a face reference to impersonate, deceive, sexualize without consent, or infer sensitive traits. Verify logos, product claims, cultural symbols, uniforms, maps, public figures, minors, and regulated uses with human review. Do not remove a watermark unless the user owns the underlying work and removal is lawful. Preserve source and output hashes, disclose synthetic origin, and follow applicable AI-labeling rules; no first-party source reviewed here guarantees C2PA credentials on every output.

## Review before delivery

Inspect each candidate at full size and in the delivery crop:

- prompt and edit adherence; unintended changes outside the target region;
- subject count, spatial relations, anatomy, hands, eyes, reflections, shadows, and perspective;
- identity/product geometry and cross-frame continuity against references;
- every character of text, logo proportions, trademark use, and prohibited artifacts;
- edge halos, repeated texture, warped patterns, seams, compression, color banding, and alpha expectations;
- exact dimensions, aspect, MIME, byte size, color profile, and downstream compatibility;
- moderation result, rights/consent, privacy, disclosure, and retention/deletion plan.

Reject an attractive image that fails a required fact. Use conventional image editing for deterministic typography, exact packaging geometry, or pixel-perfect local changes when generative iteration cannot reliably converge.

## First-party evidence register

Verified 2026-07-10 unless a source date is stated:

- Kling Open Platform overview/authentication, API errors, and outside-China endpoint: https://kling.ai/document-api/quickStart%2FproductIntroduction%2Foverview and https://kling.ai/document-api/apiReference/commonInfo
- Current image API landing pages (schema must be read signed in): https://kling.ai/document-api/api/image/2-1, https://kling.ai/document-api/api/image/o1/image-generation, https://kling.ai/document-api/api/image/3-0-omni/image-generation
- Official CLI/MCP guide: https://kling.ai/app/mcp/guide
- IMAGE 3.0 and 3.0 Omni guides: https://kling.ai/quickstart/klingai-image-3-model-user-guide and https://kling.ai/quickstart/klingai-image-3-omni-user-guide
- Official image prompt, ratio, and reference guides: https://kling.ai/quickstart/ai-image-prompt-formula, https://kling.ai/quickstart/ai-image-size-guide, and https://kling.ai/quickstart/ai-image-reference-guide
- Kuaishou 3.0 launch announcement: https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-launches-30-model-ushering-era-where-everyone-can-be
- Paid API terms and privacy policy, effective/released 2026-04-21: https://kling.ai/document-api/protocols/paidServiceProtocol and https://kling.ai/document-api/protocols/privacyPolicy
- Global user terms: https://kling.ai/docs/user-policy
- Retired standalone Kolors service notice: https://kolors.kuaishou.com/
- Open Kolors repository, technical report, and model license: https://github.com/Kwai-Kolors/Kolors, https://github.com/Kwai-Kolors/Kolors/blob/master/imgs/Kolors_paper.pdf, and https://github.com/Kwai-Kolors/Kolors/blob/master/MODEL_LICENSE


