---
name: alibaba-wan-video
description: Plan, implement, and review Alibaba Wan video generation using Alibaba Cloud Model Studio/DashScope hosted APIs or official Wan 2.1/2.2 open-weight checkpoints. Use for Wan text-to-video, image-to-video, first/last-frame or continuation, reference-to-video, video editing, speech-driven video, character animation, regional deployment, billing, licensing, and production safety.
---

# Alibaba Wan video

Use this skill to choose and operate the correct Wan surface. Treat hosted model IDs and downloadable checkpoints as different products even when their version numbers look related.

## Route first

1. Ask for the task, inputs, output duration/resolution/aspect ratio, audio requirement, deployment region/data boundary, budget, latency, GPU capacity, and whether managed inference is acceptable.
2. Choose one route:
   - **Hosted Model Studio** for current Wan 2.7 quality, 2â€“15 second clips, generated/custom audio, 1080P, managed scaling, reference-to-video, continuation, or hosted editing.
   - **Official open weights** for offline processing, weight access, reproducible checkpoint pinning, adaptation, or self-hosting. The current official public family is Wan 2.2 (plus Wan 2.1 legacy), not hosted Wan 2.7.
3. Never silently substitute a hosted alias, an older API protocol, a community quantization, or a third-party gateway.
4. Before any billable request or large checkpoint download, show the exact model/revision, region, inputs, output settings, estimated charge or storage, and obtain explicit approval. A dry run must make no network mutation.

Facts and prices below were verified **2026-07-10**. Recheck the linked first-party pages at execution time; availability, aliases, snapshots, limits, and prices are volatile.

## Keep the product families separate

| Surface | Current production choices | What it provides | Boundary |
|---|---|---|---|
| Hosted Wan 2.7 | `wan2.7-t2v-2026-06-12`, `wan2.7-i2v-2026-04-25`, `wan2.7-r2v-2026-06-12`, `wan2.7-videoedit`; moving aliases also exist | T2V; first/last-frame I2V; continuation; entity/voice reference; editing; 720P/1080P; generated or supplied audio | Closed managed service under Model Studio terms. No official Wan 2.7 checkpoint is implied by the API name. Pin dated snapshots when stability matters. |
| Hosted Wan 2.6 | `wan2.6-t2v`, `wan2.6-i2v`, `wan2.6-i2v-flash`, `wan2.6-r2v`, `wan2.6-r2v-flash`; `-us` T2V/I2V variants in Virginia | Broader region choice, legacy API schema, audio-capable generation; flash can be cheaper | Uses the legacy `size` protocol. Do not send Wan 2.7 `resolution`/`ratio` bodies to it. |
| Hosted legacy | Wan 2.5 preview; Wan 2.2/2.1 T2V, I2V, keyframe/VACE, speech/animate variants | Compatibility and specialized workflows | Capabilities, fixed durations, resolution tiers, naming (`wanx2.1-*` in Beijing), and pricing differ. Consult the exact legacy reference. A hosted `wan2.2-*` ID is not proof that it serves the public checkpoint bit-for-bit. |
| Open Wan 2.2 | T2V-A14B, I2V-A14B, TI2V-5B, S2V-14B, Animate-14B | Offline T2V/I2V, speech-driven video, character animation/replacement; Apache-2.0 checkpoints and code | No hosted SLA, automatic safety service, or managed scaling. A14B official examples require at least 80 GB VRAM; TI2V-5B is documented for at least 24 GB. |
| Open Wan 2.1 | T2V-14B/1.3B, I2V-14B, FLF2V-14B, VACE-14B/1.3B | Older, well-documented T2V/I2V, first-last-frame, and editing/control workflows | Apache-2.0, but older architecture. Official T2V-1.3B guidance favors 480P and reports 8.19 GB VRAM. |

Wan 2.2 A14B is a two-expert MoE: roughly 27B total parameters with about 14B active per denoising step. TI2V-5B uses a high-compression VAE and officially supports 1280x704/704x1280 output at 24 fps. These facts do not make 5B and A14B interchangeable quality tiers.

## Hosted Model Studio

### Region and endpoint contract

Region, API key, model availability, service deployment scope, and endpoint must match. Keys are not cross-region credentials.

| Access region | Production base | Service scope relevant to Wan | Notes |
|---|---|---|---|
| Singapore | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` | International: inference nodes globally except the Chinese mainland | Recommended workspace-dedicated domain. The shared `https://dashscope-intl.aliyuncs.com` remains functional for existing integrations. Wan 2.7 is documented here. |
| China (Beijing) | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` | Chinese mainland: inference restricted to China | Recommended workspace-dedicated domain. The shared `https://dashscope.aliyuncs.com` remains functional. Wan 2.7 is documented here. |
| Germany (Frankfurt) | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com` | Global for the currently listed Wan 2.6 models | Frankfurt supports Global and EU workspace scopes in general, but current Wan pricing lists T2V/I2V/R2V 2.6 only as Global. Do not assume those models are offered in an EU-scoped workspace; verify the console. Wan 2.7 is not currently listed. |
| US (Virginia) | `https://dashscope-us.aliyuncs.com` | Global, or US with `-us` model IDs | Current pricing lists Wan 2.6 global and `wan2.6-t2v-us`/`wan2.6-i2v-us`; workspace-dedicated domains are not yet supported. |

Workspace-dedicated domains isolate traffic to the workspace and are the documented production recommendation. Do not infer data residency merely from the access URL: the **service deployment scope** determines inference location, while the access region determines storage location. Record both.

### Wan 2.7 request shapes

All current Wan 2.7 video modes use asynchronous HTTP:

- Create: `POST {base}/api/v1/services/aigc/video-generation/video-synthesis`
- Required headers: `Authorization: Bearer ...`, `Content-Type: application/json`, `X-DashScope-Async: enable`
- Poll: `GET {base}/api/v1/tasks/{task_id}`
- States: `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELED`, `UNKNOWN`
- Poll about every 15 seconds with bounded backoff. Save the first `task_id`; do not POST again merely because generation is slow.
- Task queries and signed `video_url` values expire after 24 hours. Download promptly. Successful output is MP4/H.264.

Prefer HTTP when one worker must support every 2.7 mode. The current SDK matrix is uneven: DashScope Python/Java T2V wrappers support Wan 2.6 and earlier only (minimum documented versions 1.25.8/2.22.6), while the 2.7 I2V and R2V wrappers require Python 1.25.16 or Java 2.22.14. SDK "synchronous" calls merely wrap and block on the asynchronous service; they do not change job duration, billing, or result expiry. Recheck versions before pinning dependencies.

Core T2V body:

```json
{
  "model": "wan2.7-t2v-2026-06-12",
  "input": {
    "prompt": "Generate a single-shot video. Wide shot of a red paper kite rising above a quiet salt flat at dawn; slow dolly forward, soft wind and natural ambience.",
    "negative_prompt": "text overlays, logos, warped kite, abrupt cuts"
  },
  "parameters": {
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 5,
    "prompt_extend": false,
    "watermark": true,
    "seed": 104729
  }
}
```

Wan 2.7 T2V accepts Chinese or English prompts up to 5,000 characters and negative prompts up to 500; longer text is truncated, so validate locally. `duration` is an integer 2â€“15 (default 5); `resolution` is `720P` or `1080P` (default 1080P); ratios are `16:9`, `9:16`, `1:1`, `4:3`, or `3:4`. Prompt extension defaults true, watermark defaults false, and a fixed seed improvesâ€”but does not guaranteeâ€”reproducibility. Control single versus multi-shot in natural-language prompt structure; the old `shot_type` has no effect on 2.7.

Change only `input`/`model` for other 2.7 modes:

```jsonc
// First and last frame I2V. Use only first_frame for first-frame generation.
{
  "model": "wan2.7-i2v-2026-04-25",
  "input": {"prompt": "The lantern drifts downstream as dusk deepens.", "media": [
    {"type": "first_frame", "url": "https://assets.example/first.webp"},
    {"type": "last_frame", "url": "https://assets.example/last.webp"}
  ]},
  "parameters": {"resolution": "720P", "duration": 6, "prompt_extend": false, "watermark": true}
}
```

```jsonc
// Continuation. first_clip may be combined with last_frame when supported by the exact model docs.
{
  "model": "wan2.7-i2v-2026-04-25",
  "input": {"prompt": "Continue the same camera move and weather.", "media": [
    {"type": "first_clip", "url": "https://assets.example/source.mp4"}
  ]},
  "parameters": {"resolution": "720P", "duration": 10, "prompt_extend": false, "watermark": true}
}
```

```jsonc
// Reference-to-video. Refer to assets by their one-based Image/Video order in the prompt.
{
  "model": "wan2.7-r2v-2026-06-12",
  "input": {"prompt": "Video 1 enters and gives Image 1 the compass.", "media": [
    {"type": "reference_video", "url": "https://assets.example/person.mp4", "reference_voice": "https://assets.example/voice.wav"},
    {"type": "reference_image", "url": "https://assets.example/robot.webp"}
  ]},
  "parameters": {"resolution": "720P", "ratio": "16:9", "duration": 8, "prompt_extend": false, "watermark": true}
}
```

For I2V, an input image may be JPEG/JPG/PNG without alpha, BMP, or WEBP, up to 20 MB, 240â€“8,000 pixels per side, and aspect ratio 1:8â€“8:1. A continuation `first_clip` must be MP4/MOV, 2â€“10 seconds, up to 100 MB, 240â€“4,096 pixels per side, and aspect ratio 1:8â€“8:1. In continuation, `duration` means the **final total** video length, not the number of new seconds; output ratio follows the clip and the full output duration is billed.

For R2V, duration is 2â€“10 seconds when a reference video is present and 2â€“15 without one. It accepts at most one first frame plus 1â€“5 combined reference images/videos; a character reference must contain only one character. Reference images have the same 20 MB limits above. Reference videos are MP4/MOV, 1â€“30 seconds, up to 100 MB, and 240â€“4,096 pixels per side; `reference_voice` is WAV/MP3, 1â€“10 seconds, up to 15 MB. A supplied first frame overrides `ratio`. For video editing, use `wan2.7-videoedit`, one `{"type":"video"}` plus up to four `reference_image` assets; its billing includes both input and output video duration. Always re-open the exact API page for volatile constraints before upload.

### Billable, dry-run-first T2V client

This complete example pins the Singapore snapshot, prints a redacted free plan by default, binds the exact request/workspace/output policy plus fresh pricing evidence to approval, creates at most one task, persists a crash-resumable sanitized ledger, downloads through an exact-host and public-IP policy without forwarding the API key, and validates before atomic no-overwrite publication. It deliberately does not accept arbitrary base URLs or output URLs.

```python
#!/usr/bin/env python3
import argparse, hashlib, http.client, ipaddress, json, os, random, socket, ssl
import pathlib, subprocess, sys, tempfile, threading, time, uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit
import requests

MODEL = "wan2.7-t2v-2026-06-12"
PRICE_USD_PER_SECOND = {"720P": Decimal("0.10"), "1080P": Decimal("0.15")}
REGION_SUFFIX = {"sg": "ap-southeast-1.maas.aliyuncs.com"}
TERMINAL = {"SUCCEEDED", "FAILED", "CANCELED", "UNKNOWN"}
MAX_JSON = 1024 * 1024
MAX_VIDEO = 1024 * 1024 * 1024
MAX_TOOL = 1024 * 1024
EXPECTED = {
    ("720P", "16:9"): (1280, 720), ("720P", "9:16"): (720, 1280),
    ("720P", "1:1"): (960, 960), ("720P", "4:3"): (1104, 832),
    ("720P", "3:4"): (832, 1104), ("1080P", "16:9"): (1920, 1080),
    ("1080P", "9:16"): (1080, 1920), ("1080P", "1:1"): (1440, 1440),
    ("1080P", "4:3"): (1648, 1248), ("1080P", "3:4"): (1248, 1648)}

class APIError(RuntimeError):
    def __init__(self, message, status=None, retry_after=None, body_sha256=None):
        super().__init__(message); self.status = status; self.retry_after = retry_after; self.body_sha256 = body_sha256

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()

def fsync_directory(path):
    if os.name == "nt": return
    fd = os.open(path, os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)

def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(value, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n"); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path); fsync_directory(path.parent)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def read_record(path):
    if path.stat().st_size > MAX_JSON: raise RuntimeError("attempt record exceeds cap")
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict): raise RuntimeError("attempt record must be an object")
    return value

def run_bounded(argv, timeout):
    process = subprocess.Popen(argv, shell=False, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err, total, lock, overflow = bytearray(), bytearray(), [0], threading.Lock(), threading.Event()
    def drain(stream, bucket):
        while True:
            chunk = stream.read(65536)
            if not chunk: break
            with lock:
                room = max(0, MAX_TOOL - total[0]); bucket.extend(chunk[:room]); total[0] += len(chunk)
                if total[0] > MAX_TOOL: overflow.set()
            if overflow.is_set():
                try: process.kill()
                except OSError: pass
    threads = [threading.Thread(target=drain, args=(process.stdout, out), daemon=True),
               threading.Thread(target=drain, args=(process.stderr, err), daemon=True)]
    for thread in threads: thread.start()
    timed_out = False
    try: code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True; process.kill(); code = process.wait()
    for thread in threads: thread.join()
    return code, bytes(out), bytes(err), timed_out, overflow.is_set()

def api_json(session, method, url, payload=None, timeout=(10, 60)):
    with session.request(method, url, json=payload, timeout=timeout, allow_redirects=False, stream=True) as response:
        raw = bytearray()
        for chunk in response.iter_content(65536):
            raw.extend(chunk)
            if len(raw) > MAX_JSON: raise RuntimeError("API response exceeds cap")
        digest = hashlib.sha256(raw).hexdigest()
        if not 200 <= response.status_code < 300:
            retry = response.headers.get("Retry-After")
            try: retry = min(60.0, max(0.0, float(retry)))
            except (TypeError, ValueError): retry = None
            raise APIError(f"API HTTP {response.status_code}", response.status_code, retry, digest)
        try: value = json.loads(raw)
        except json.JSONDecodeError as exc: raise APIError("API returned invalid JSON", response.status_code, body_sha256=digest) from exc
        if not isinstance(value, dict): raise RuntimeError("API response is not an object")
        return value

def safe_get(call, deadline, attempts=5):
    for attempt in range(attempts):
        try: return call()
        except APIError as exc:
            if exc.status != 429 and (exc.status is None or exc.status < 500): raise
            if attempt + 1 == attempts or time.monotonic() >= deadline: raise
            delay = exc.retry_after or min(20, 2 ** attempt) * (1 + random.random() * 0.25)
        except requests.RequestException:
            if attempt + 1 == attempts or time.monotonic() >= deadline: raise
            delay = min(20, 2 ** attempt) * (1 + random.random() * 0.25)
        if time.monotonic() + delay >= deadline: raise TimeoutError("poll retry would cross deadline")
        time.sleep(delay)

class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, address):
        super().__init__(host, 443, timeout=120, context=ssl.create_default_context()); self.address = address
    def connect(self):
        sock = socket.create_connection((self.address, 443), self.timeout)
        try: self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
        except BaseException:
            sock.close(); raise

def download_video(url, stage_path, allowed_hosts):
    parsed = urlsplit(url); host = (parsed.hostname or "").lower()
    if (parsed.scheme != "https" or parsed.username or parsed.password or parsed.fragment
            or parsed.port not in (None, 443) or not parsed.path or host not in allowed_hosts):
        raise RuntimeError("result URL is not an exact approved HTTPS host")
    try: ipaddress.ip_address(host); raise RuntimeError("IP-literal result host rejected")
    except ValueError: pass
    addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)})
    if not addresses or any(not ipaddress.ip_address(address).is_global for address in addresses):
        raise RuntimeError("result host did not resolve only to public addresses")
    connection = PinnedHTTPSConnection(host, addresses[0]); created = False
    try:
        target = parsed.path + (("?" + parsed.query) if parsed.query else "")
        connection.request("GET", target, headers={"Accept": "video/mp4,application/octet-stream"})
        response = connection.getresponse()
        if 300 <= response.status < 400: raise RuntimeError("result redirect rejected")
        if response.status != 200: raise RuntimeError(f"result HTTP {response.status}")
        mime = response.getheader("Content-Type", "").split(";", 1)[0].lower()
        if mime not in {"video/mp4", "application/octet-stream"}: raise RuntimeError("result MIME rejected")
        length = response.getheader("Content-Length")
        if length and (not length.isdigit() or int(length) > MAX_VIDEO): raise RuntimeError("declared result size rejected")
        fd = os.open(stage_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600); created = True; total = 0
        with os.fdopen(fd, "wb") as f:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk: break
                total += len(chunk)
                if total > MAX_VIDEO: raise RuntimeError("result crossed byte cap")
                f.write(chunk)
            f.flush(); os.fsync(f.fileno())
        return stage_path
    except BaseException:
        if created and stage_path.exists(): stage_path.unlink()
        raise
    finally: connection.close()

def inspect_mp4(path, output, resolution, ratio, duration):
    with path.open("rb") as f: head = f.read(12)
    if len(head) < 12 or head[4:8] != b"ftyp": raise RuntimeError("MP4 signature rejected")
    args = ["ffprobe", "-v", "error", "-show_entries",
            "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate", "-of", "json", str(path)]
    code, out, _, timed_out, overflow = run_bounded(args, 30)
    if code or timed_out or overflow: raise RuntimeError("bounded ffprobe failed")
    probe = json.loads(out); streams = probe.get("streams", []); videos = [s for s in streams if s.get("codec_type") == "video"]
    if len(videos) != 1 or videos[0].get("codec_name") != "h264": raise RuntimeError("expected one H.264 stream")
    width, height = videos[0].get("width"), videos[0].get("height")
    if (width, height) != EXPECTED[(resolution, ratio)]: raise RuntimeError("dimensions do not match approval")
    try: actual = Decimal(str(probe.get("format", {}).get("duration", "")))
    except InvalidOperation as exc: raise RuntimeError("invalid media duration") from exc
    if not actual.is_finite() or abs(actual - Decimal(duration)) > Decimal("0.75"):
        raise RuntimeError("media duration outside tolerance")
    code, _, _, timed_out, overflow = run_bounded(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], 300)
    if code or timed_out or overflow: raise RuntimeError("bounded full decode failed")
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): digest.update(chunk)
    return {"path": str(output), "bytes": path.stat().st_size, "sha256": digest.hexdigest(),
            "media": {"duration": str(actual), "width": width, "height": height,
                      "videoCodec": "h264", "audioStreams": sum(s.get("codec_type") == "audio" for s in streams)}}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--negative-prompt", default="text overlays, logos, deformed objects")
    p.add_argument("--region", choices=sorted(REGION_SUFFIX), default="sg")
    p.add_argument("--resolution", choices=sorted(PRICE_USD_PER_SECOND), default="720P")
    p.add_argument("--ratio", choices=["16:9", "9:16", "1:1", "4:3", "3:4"], default="16:9")
    p.add_argument("--duration", type=int, default=5)
    p.add_argument("--seed", type=int, default=104729)
    p.add_argument("--workspace-id", required=True, help="non-secret Singapore Model Studio workspace ID")
    p.add_argument("--out-dir", type=pathlib.Path, default=pathlib.Path("wan-run"))
    p.add_argument("--attempt-id", required=True)
    p.add_argument("--max-usd", required=True)
    p.add_argument("--pricing-checked-at", required=True)
    p.add_argument("--pricing-evidence-sha256", required=True)
    p.add_argument("--delivery-host", action="append", required=True,
                   help="exact approved result host; repeat for each host")
    p.add_argument("--approval-sha256")
    p.add_argument("--execute", action="store_true"); p.add_argument("--resume", action="store_true")
    p.add_argument("--show-full-plan", action="store_true")
    a = p.parse_args()

    if not 1 <= len(a.prompt) <= 5000 or len(a.negative_prompt) > 500:
        p.error("prompt must be 1..5000 chars; negative prompt <=500")
    if not 2 <= a.duration <= 15 or not 0 <= a.seed <= 2147483647:
        p.error("duration must be 2..15 and seed 0..2147483647")
    try: attempt = uuid.UUID(a.attempt_id); ceiling = Decimal(a.max_usd)
    except (ValueError, InvalidOperation) as exc: p.error(f"attempt ID or maximum invalid: {exc}")
    if attempt.version != 4 or str(attempt) != a.attempt_id.lower(): p.error("attempt ID must be canonical UUIDv4")
    estimate = PRICE_USD_PER_SECOND[a.resolution] * a.duration
    if not ceiling.is_finite() or ceiling <= 0 or ceiling < estimate:
        p.error("maximum must be finite, positive, and cover the estimate")
    if (len(a.pricing_evidence_sha256) != 64
            or any(c not in "0123456789abcdef" for c in a.pricing_evidence_sha256)):
        p.error("pricing evidence must be a lowercase SHA-256")
    try: checked_at = datetime.fromisoformat(a.pricing_checked_at.replace("Z", "+00:00"))
    except ValueError as exc: p.error(f"pricing timestamp must be ISO-8601: {exc}")
    if checked_at.tzinfo is None: p.error("pricing timestamp must include a timezone")
    allowed_hosts = sorted(set(host.lower().rstrip(".") for host in a.delivery_host))
    if (not allowed_hosts or len(allowed_hosts) > 8
            or any(not host or len(host) > 253
                   or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-." for c in host) for host in allowed_hosts)):
        p.error("delivery hosts must be 1..8 exact DNS names")
    for host in allowed_hosts:
        try: ipaddress.ip_address(host); p.error("delivery hosts cannot be IP literals")
        except ValueError: pass
    out_dir = a.out_dir.resolve(); record_path = out_dir / "attempt.json"
    video_path = out_dir / "output.mp4"; stage_path = out_dir / ".output.mp4.wan-stage"
    body = {"model": MODEL, "input": {"prompt": a.prompt,
            "negative_prompt": a.negative_prompt}, "parameters": {
            "resolution": a.resolution, "ratio": a.ratio, "duration": a.duration,
            "prompt_extend": False, "watermark": True, "seed": a.seed}}
    workspace = a.workspace_id
    if (not workspace or len(workspace) > 100
            or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for c in workspace)):
        p.error("workspace ID contains unsupported characters")
    host = f"{workspace}.{REGION_SUFFIX[a.region]}"
    request_hash = hashlib.sha256(canonical(body)).hexdigest()
    envelope = {"backend": "alibaba-model-studio-hosted", "region": a.region,
        "serviceDeploymentScope": "International", "host": host,
        "endpoint": "/api/v1/services/aigc/video-generation/video-synthesis",
        "request": body, "attemptId": str(attempt), "attemptRecord": str(record_path),
        "outputPolicy": {"path": str(video_path), "stagePath": str(stage_path),
                         "exactDeliveryHosts": allowed_hosts, "maxBytes": MAX_VIDEO,
                         "mime": ["video/mp4", "application/octet-stream"], "noOverwrite": True,
                         "requiredCodec": "h264", "fullDecode": True},
        "cost": {"pricingCheckedAt": checked_at.isoformat(), "pricingEvidenceSha256": a.pricing_evidence_sha256,
                 "rateUsdPerOutputSecond": str(PRICE_USD_PER_SECOND[a.resolution]),
                 "seconds": a.duration, "creates": 1, "estimatedMaxUsd": str(estimate),
                 "approvedMaxUsd": str(ceiling)}}
    approval = hashlib.sha256(canonical(envelope)).hexdigest()
    safe_body = {**body, "input": {"prompt": "sha256:" + hashlib.sha256(a.prompt.encode()).hexdigest(),
                                    "negative_prompt": "sha256:" + hashlib.sha256(a.negative_prompt.encode()).hexdigest()}}
    print(json.dumps({"dryRun": not a.execute, "approvalSha256": approval,
        "plan": {**envelope, "request": safe_body}}, ensure_ascii=False, indent=2))
    if a.show_full_plan: print(json.dumps({"protectedFullPlan": envelope}, ensure_ascii=False, indent=2))
    if not a.execute:
        print("PLAN ONLY: no API request was made", file=sys.stderr)
        return 0
    if a.approval_sha256 != approval: raise SystemExit("exact approval digest mismatch")
    age = datetime.now(timezone.utc) - checked_at.astimezone(timezone.utc)
    if age.total_seconds() < -300 or age.total_seconds() > 86400:
        raise SystemExit("pricing evidence must be rechecked within 24 hours of execution")
    base = f"https://{workspace}.{REGION_SUFFIX[a.region]}"
    if a.resume:
        if not record_path.exists(): raise SystemExit("resume record missing")
        record = read_record(record_path)
        if record.get("approval_sha256") != approval or record.get("request_sha256") != request_hash:
            raise SystemExit("resume does not match exact approved request")
        task_id = record.get("task_id")
        if not isinstance(task_id, str) or not task_id: raise SystemExit("no known task ID; never replay create")
        expected_artifact = record.get("artifact_staged") or record.get("artifact")
        candidate = video_path if video_path.exists() else stage_path if stage_path.exists() else None
        if candidate is not None:
            if not isinstance(expected_artifact, dict):
                if record.get("status") == "downloading" and candidate == stage_path:
                    stage_path.unlink(); fsync_directory(stage_path.parent)
                else: raise SystemExit("unclaimed output/stage exists; refusing overwrite or adoption")
            else:
                artifact = inspect_mp4(candidate, video_path, a.resolution, a.ratio, a.duration)
                if (artifact.get("sha256") != expected_artifact.get("sha256")
                        or artifact.get("bytes") != expected_artifact.get("bytes")):
                    raise SystemExit("recovered artifact does not match durable staged evidence")
                if candidate == stage_path:
                    if video_path.exists(): raise SystemExit("output appeared during recovery")
                    os.replace(stage_path, video_path); fsync_directory(video_path.parent)
                record.update(status="artifact_saved", artifact=artifact, updated_unix=int(time.time()))
                record.pop("artifact_staged", None); atomic_json(record_path, record)
                print(json.dumps(record, indent=2)); return 0
        key = os.environ.get("DASHSCOPE_API_KEY")
        if not key: raise SystemExit("Set DASHSCOPE_API_KEY to resume polling")
        session = requests.Session(); session.headers.update({"Authorization": f"Bearer {key}",
            "Content-Type": "application/json", "X-DashScope-Async": "enable"})
    else:
        key = os.environ.get("DASHSCOPE_API_KEY")
        if not key: raise SystemExit("Set DASHSCOPE_API_KEY")
        session = requests.Session(); session.headers.update({"Authorization": f"Bearer {key}",
            "Content-Type": "application/json", "X-DashScope-Async": "enable"})
        out_dir.parent.mkdir(parents=True, exist_ok=True)
        try: out_dir.mkdir(exist_ok=False)
        except FileExistsError as exc: raise SystemExit("attempt directory already claimed; use resume") from exc
        record = {"attempt_id": str(attempt), "approval_sha256": approval, "request_sha256": request_hash,
                  "status": "posting", "task_id": None, "created_unix": int(time.time())}
        atomic_json(record_path, record)
        try: created = api_json(session, "POST", base + envelope["endpoint"], body, (10, 120))
        except Exception as exc:
            known_rejection = (isinstance(exc, APIError) and exc.status is not None and 400 <= exc.status < 500
                               and exc.status not in {408, 409, 425, 429})
            record.update(status="create_rejected" if known_rejection else "create_outcome_unknown",
                          error_type=type(exc).__name__, http_status=getattr(exc, "status", None),
                          error_body_sha256=getattr(exc, "body_sha256", None))
            atomic_json(record_path, record)
            if known_rejection: raise RuntimeError("provider rejected create before acceptance") from exc
            raise RuntimeError("create outcome unknown; reconcile billing/logs, never replay") from exc
        task_id = created.get("output", {}).get("task_id")
        if (not isinstance(task_id, str) or not 1 <= len(task_id) <= 200
                or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_." for c in task_id)):
            record.update(status="create_outcome_unknown", error_type="MissingOrInvalidTaskId",
                          create_response_sha256=hashlib.sha256(canonical(created)).hexdigest())
            atomic_json(record_path, record)
            raise RuntimeError("create returned no safe task ID; reconcile, never replay")
        record.update(status="task_id_saved", task_id=task_id, request_id=created.get("request_id"),
                      create_response_sha256=hashlib.sha256(canonical(created)).hexdigest(), updated_unix=int(time.time()))
        atomic_json(record_path, record)

    deadline = time.monotonic() + 12 * 60
    result = None
    while time.monotonic() < deadline:
        result = safe_get(lambda: api_json(session, "GET", base + f"/api/v1/tasks/{task_id}", timeout=(10, 30)), deadline)
        status = result.get("output", {}).get("task_status")
        print(f"task={task_id} status={status}", file=sys.stderr)
        if status in TERMINAL:
            break
        if status not in {"PENDING", "RUNNING"}: raise RuntimeError("unrecognized task status")
        if time.monotonic() + 15 >= deadline: break
        time.sleep(15)
    if result is None or result.get("output", {}).get("task_status") in {"PENDING", "RUNNING"}:
        record.update(status="polling_paused", updated_unix=int(time.time())); atomic_json(record_path, record)
        raise TimeoutError(f"Polling timed out; resume GET with task_id {task_id}, do not POST")
    output = result.get("output", {})
    if output.get("task_status") != "SUCCEEDED":
        message = str(output.get("message", ""))
        record.update(status="generation_" + str(output.get("task_status", "unknown")).lower(),
                      service_code=output.get("code"), message_sha256=hashlib.sha256(message.encode()).hexdigest())
        atomic_json(record_path, record); raise RuntimeError("task ended without a successful artifact")
    url = output.get("video_url", "")
    if not isinstance(url, str) or not url: raise RuntimeError("successful task omitted result URL")
    usage = result.get("usage") or {}; actual_cost = None
    try:
        seconds = Decimal(str(usage.get("output_video_duration")))
        if seconds.is_finite() and seconds >= 0: actual_cost = PRICE_USD_PER_SECOND[a.resolution] * seconds
    except InvalidOperation: pass
    record.update(status="downloading", result_response_sha256=hashlib.sha256(canonical(result)).hexdigest(),
                  result_url_sha256=hashlib.sha256(url.encode()).hexdigest(), usage=usage,
                  actual_cost_usd=None if actual_cost is None else str(actual_cost),
                  actual_cost_within_approval=None if actual_cost is None else actual_cost <= ceiling,
                  stage_path=str(stage_path), updated_unix=int(time.time()))
    atomic_json(record_path, record)
    try:
        download_video(url, stage_path, set(allowed_hosts))
        artifact = inspect_mp4(stage_path, video_path, a.resolution, a.ratio, a.duration)
    except BaseException as exc:
        record.update(status="artifact_validation_failed", error_type=type(exc).__name__)
        atomic_json(record_path, record); raise
    record.update(status="artifact_staged", artifact_staged=artifact, updated_unix=int(time.time()))
    atomic_json(record_path, record)
    if video_path.exists(): raise RuntimeError("output appeared before publication")
    os.replace(stage_path, video_path); fsync_directory(video_path.parent)
    record.update(status="artifact_saved", artifact=artifact, rights_review="required",
                  moderation_review="required", creative_qa="pending", ai_disclosure="required",
                  provenance_credentials="not_documented", updated_unix=int(time.time()))
    record.pop("artifact_staged", None); atomic_json(record_path, record)
    print(json.dumps(record, ensure_ascii=False, indent=2)); return 0

if __name__ == "__main__":
    main()
```

Install `requests`, then run the plan first. Only the second command can create a paid task:

```bash
python wan_hosted.py --workspace-id "$WAN_WORKSPACE_ID" --attempt-id 7f8f06b7-9e68-4f0a-bf16-3eaf3ee9d6c4 --max-usd 0.50 --pricing-checked-at 2026-07-10T12:00:00Z --pricing-evidence-sha256 "$BILLING_SHA256" --delivery-host "$WAN_RESULT_HOST" --prompt "Generate a single-shot video. A red kite rises over a salt flat at dawn."
DASHSCOPE_API_KEY=... python wan_hosted.py --execute --approval-sha256 "<exact digest>" --workspace-id "$WAN_WORKSPACE_ID" --attempt-id 7f8f06b7-9e68-4f0a-bf16-3eaf3ee9d6c4 --max-usd 0.50 --pricing-checked-at 2026-07-10T12:00:00Z --pricing-evidence-sha256 "$BILLING_SHA256" --delivery-host "$WAN_RESULT_HOST" --prompt "Generate a single-shot video. A red kite rises over a salt flat at dawn."
```

`BILLING_SHA256` is the digest of the dated first-party pricing evidence actually reviewed. `WAN_RESULT_HOST` is an exact hostname allowed by the current Model Studio/OSS delivery contract, never a wildcard inferred from the returned URL. Repeat `--delivery-host` only for additional exact approved hosts. Execution rejects pricing evidence older than 24 hours. Use the unchanged arguments with `--execute --resume` only when the durable attempt record already contains a task ID; `posting` or `create_outcome_unknown` requires billing/log/support reconciliation and must never be replayed.

The executable deliberately accepts only `--region sg`. For Beijing or another region, first replace the region allowlist and price table with values from the current pricing page and re-review the endpoint/model contract; do not bypass that fail-closed boundary.

### Cost and capacity controls

Current standard unit rates in USD per billable second:

| Access region / scope | Models | 720P | 1080P |
|---|---|---:|---:|
| Singapore / International | Wan 2.7 T2V, I2V, R2V, video edit | $0.10 | $0.15 |
| Beijing / Chinese mainland | Wan 2.7 T2V, I2V, R2V, video edit | $0.086012 | $0.143353 |
| Frankfurt / Global | Wan 2.6 T2V, I2V, R2V | $0.086012 | $0.143353 |
| Virginia / Global | Wan 2.6 T2V, I2V, R2V | $0.086012 | $0.143353 |
| Virginia / US | `wan2.6-t2v-us`, `wan2.6-i2v-us` | $0.10 | $0.15 |

Billing basis still differs by mode. I2V and T2V input is free, so their billable duration is the successful output duration. For Wan 2.7 R2V with `N` reference videos, each reference video is billed for `min(actual duration, 5/N seconds)` and those input amounts are added to the output duration; images and the first frame are excluded from `N`. Video editing bills input-video duration plus output-video duration. Failed requests are not billed and do not consume the free quota. Flash, legacy, and silent-output prices are different; consult the live table rather than extrapolating. Do not treat a promotional/free quota as a budget control.

Singapore and Beijing rate-limit the listed Wan 2.7 T2V/I2V/R2V/edit models at 5 task submissions/second and 5 concurrent tasks per Alibaba Cloud account. Limits aggregate RAM users, workspaces, and keys. A rate limit is not a cumulative spend limit: use account budget alerts, a local job queue, concurrency semaphore, and a per-job cost ceiling. Recheck because these values can change.

## Official open-weight deployment

Use only official `Wan-Video` GitHub and `Wan-AI` Hugging Face/ModelScope artifacts unless the user explicitly accepts a community port or quantization. Record:

- repository URL and immutable Git commit;
- checkpoint repository and immutable revision/commit;
- every file hash, package lock, CUDA/PyTorch/driver version, GPU type, prompt, negative prompt, seed, size, frame count, sampling settings, and output hash;
- the license texts shipped with each pinned artifact and all dependency licenses.

Do not download weights as an incidental step. First run `git ls-remote` or inspect the registry metadata, present expected storage and license, get approval, then pin the reviewed hashes. The official Wan 2.2 repository has no GitHub release artifacts as of verification; `main` is not a production version.

Example after the operator has approved and pinned both revisions:

```bash
git clone https://github.com/Wan-Video/Wan2.2.git
cd Wan2.2
git checkout --detach "$REVIEWED_WAN_GIT_COMMIT"
python -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r requirements.lock
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B \
  --revision "$REVIEWED_HF_COMMIT" --local-dir ./Wan2.2-TI2V-5B
sha256sum -c checkpoint.sha256
python generate.py --task ti2v-5B --size '1280*704' \
  --ckpt_dir ./Wan2.2-TI2V-5B --offload_model True --convert_model_dtype \
  --t5_cpu --base_seed 104729 --save_file ./wan-ti2v-5b.mp4 \
  --prompt "Wide shot of a red paper kite rising above a quiet salt flat at dawn."
ffprobe -v error -show_streams -show_format ./wan-ti2v-5b.mp4
ffmpeg -v error -i ./wan-ti2v-5b.mp4 -f null -
```

`requirements.lock` and `checkpoint.sha256` are organization-generated review artifacts, not files supplied by the Wan repository. Create them in a controlled dependency-resolution stage; never invent their contents. The official repo requires PyTorch >=2.4.0. Its baseline A14B T2V/I2V commands use `1280*720`; the TI2V-5B command uses `1280*704` and CPU/offload flags for a documented 24 GB minimum. Capacity claims are baseline guidance, not guarantees for other frame counts, drivers, or colocated workloads.

Open Wan 2.1 and 2.2 code/checkpoints are labeled Apache License 2.0. Preserve notices and satisfy Apache conditions when redistributing the work or derivatives. The Wan team says it claims no rights in generated content, but that is not a warranty of non-infringement or ownership: outputs can resemble protected material, people, brands, or other users' outputs. Audit input rights, publicity/privacy/biometric consent, music/voice licenses, and the laws of the deployment jurisdiction. Community LoRAs, quantizations, text encoders, TTS components, containers, and datasets can carry different licenses.

## Safety, privacy, and release gates

- Obtain documented authorization for every recognizable person, voice, reference performance, source video, logo, and copyrighted input. Never infer consent from public availability.
- Refuse deceptive impersonation, non-consensual intimate content, exploitation, targeted harassment, or instructions designed to evade safeguards. Clearly label synthetic media where law, platform policy, or context requires it.
- Hosted Model Studio treats input and output as customer Member Content. Its current product terms say Alibaba Cloud does not claim output ownership and will not use Member Content to develop or improve Model Studio models without separate consent. The customer remains responsible for rights, consents, data protection, and output use. This is not a promise that API payloads have zero retention; obtain the applicable DPA/retention terms for sensitive workloads.
- The `watermark` API option adds a visible lower-right `AI Generated` mark. Do not disable, crop, or remove provenance when policy or law requires it. Add durable provenance/metadata in the publishing pipeline rather than relying only on a visible mark.
- Open-weight deployment moves moderation, access control, abuse monitoring, key/asset isolation, logging, incident response, and deletion duties to the operator. Run input and output moderation before publication.
- Never log API keys or signed output URLs. Use a secrets manager, least-privilege workspace keys, short-lived source URLs, separate staging storage, and lifecycle deletion. Signed result links expire; archive only approved outputs.

Release only after checking: task/model/revision receipts; exact duration, dimensions, frame rate, codec, audio presence/sync; full decode; black/frozen/duplicate frames; prompt and reference adherence; identity drift; temporal artifacts; text/logo defects; safety/moderation; provenance; rights approvals; and actual billed usage against the approved ceiling. Keep the rejected output and diagnostic metadata only if policy permits.

## First-party sources

- [Wan 2.7 text-to-video API](https://www.alibabacloud.com/help/en/model-studio/text-to-video-api-reference)
- [Wan 2.7 image-to-video API](https://www.alibabacloud.com/help/en/model-studio/image-to-video-general-api-reference)
- [Wan reference-to-video API](https://www.alibabacloud.com/help/en/model-studio/wan-video-to-video-api-reference)
- [Wan 2.7 video editing API](https://www.alibabacloud.com/help/en/model-studio/wan-video-editing-api-reference)
- [Legacy Wan T2V API](https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference)
- [Regional access and deployment scopes](https://www.alibabacloud.com/help/en/model-studio/regions/)
- [Model pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing)
- [Rate limits](https://www.alibabacloud.com/help/en/model-studio/rate-limit)
- [Model Studio product terms](https://www.alibabacloud.com/help/en/legal/latest/alibaba-cloud-international-website-product-terms-of-service-v-3-8-0)
- [Model Studio security and privacy](https://www.alibabacloud.com/help/en/model-studio/privacy-notice)
- [Official Wan 2.2 repository](https://github.com/Wan-Video/Wan2.2) and [Apache-2.0 license](https://raw.githubusercontent.com/Wan-Video/Wan2.2/main/LICENSE.txt)
- [Official Wan 2.1 repository](https://github.com/Wan-Video/Wan2.1) and [technical report](https://arxiv.org/abs/2503.20314)
- [Official Wan 2.2 TI2V-5B model card](https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B)


