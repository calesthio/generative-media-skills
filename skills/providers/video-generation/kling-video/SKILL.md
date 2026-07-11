---
name: kling-video
description: Plan, prompt, generate, reference, edit, motion-control, and quality-review videos with Kuaishou's direct Kling AI video platform and API, especially Kling VIDEO 3.0, 3.0 Omni, 3.0 Turbo, native audio, multi-shot, elements, start/end frames, and image/video references. Use for first-party Kling video production or API integration, not Kolors image generation, avatars, standalone audio, consumer-only membership advice, or third-party Kling gateways.
---

# Produce video with Kling AI

Treat model availability, API fields, prices, policies, and limits as volatile. The facts below were verified against first-party Kling/Kuaishou sources on **2026-07-10**; reopen the linked model page, billing table, update log, and terms before spending or shipping.

## Keep the surface and job coherent

Ask for the delivery surface (direct API or Kling web/app), geography, task, input media, duration, aspect ratio, resolution, audio/dialogue, shot structure, audience, rights/consent, privacy needs, variant count, and approved spend.

| Surface | Use it for | Keep separate |
|---|---|---|
| Direct international API | Server workflows at `https://api-singapore.klingai.com`; API-key auth; per-second API billing | Old `api.klingai.com`, China-host routing, consumer credits, or a reseller schema |
| Kling web/app | Interactive creation, Elements library, memberships, free/paid UI features | A promise that UI controls, credits, watermark benefits, or defaults exist in API |
| `kling-v3` / VIDEO 3.0 | Prompt-led text/image/start-end generation, native audio, flexible duration, multi-shot | Omni video editing/reference inputs |
| `kling-v3-omni` / VIDEO 3.0 Omni | Reference-driven generation, video/reference inputs, Elements, editing, native audio, multi-shot | Kling Image 3.0 Omni or Kolors |
| `kling-3.0-turbo` | Current faster, scale-oriented 3.0 option with native audio | An assumption that every 3.0 or Omni field is accepted unchanged |
| Motion Control | Transfer one driving performance to a referenced character | Avatar, lip-sync, face recognition, or standalone audio APIs |

**FACT:** The current API documentation requires the new API-key format for all models. Legacy AccessKey/SecretKey JWT credentials remain valid only for 3.0-and-earlier access and do not unlock new models. Use a server-side `KLING_API_KEY`; never expose it in a browser or mobile client. The current international host is Singapore, while China deployments have a different Beijing host. Do not select a host as a data-residency guarantee. [Authentication](https://kling.ai/document-api/apiReference/commonInfo)

**FACT:** VIDEO 3.0 and 3.0 Omni support text-to-video, image-to-video, native audio, multi-shot storytelling, and flexible **3â€“15 second** output. VIDEO 3.0 is the prompt-led path; Omni adds richer image/video/Element reference and editing workflows. First-party descriptions of â€œperfect,â€ â€œultimate,â€ or â€œindustrial-gradeâ€ consistency, physics, text, lip-sync, or quality are **PROVIDER CLAIMS**, not delivery guarantees. [VIDEO 3.0 guide](https://kling.ai/quickstart/klingai-video-3-model-user-guide), [VIDEO 3.0 Omni guide](https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide), [Kuaishou release](https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-launches-30-model-ushering-era-where-everyone-can-be/)

**FACT:** Kling-Omni is described in the Kling teamâ€™s technical report as a unified multimodal framework for generation, editing, and multimodal instruction following. Benchmark and preference results in provider-authored reports remain provider evidence; do not turn them into an independent ranking. [Kling-Omni report](https://arxiv.org/abs/2512.16776)

## Route the current family deliberately

- Choose `kling-v3` when the scene can be driven by prompt, a start image, or start/end frames. Use single-shot mode when continuity matters more than coverage; use multi-shot only when cuts are intentional.
- Choose `kling-v3-omni` when the request depends on a reference video, several image/Element references, subject/voice binding, or in-video editing. Reopen the exact Omni endpoint page because reference combinations change quickly.
- Choose `kling-3.0-turbo` only after its current task page confirms the requested task and fields. The official platform calls it faster and more reliable at scale; treat those as provider claims until a dated workload test verifies them.
- Keep `kling-video-o1`, `kling-v2-6`, `kling-v2-5-turbo`, and earlier IDs only for an existing compatibility/cost requirement. Do not silently downgrade when a 3.0 field is rejected.
- Use Motion Control for performance transfer. Its input and likeness risks differ enough that it needs explicit driving-video and performer consent, not merely an image-generation approval.

For VIDEO 3.0 native speech, the current product guide lists Chinese, English, Japanese, Korean, and Spanish plus some dialects/accents. Verify language, model, and API support for the exact account. Do not promise voice identity, pronunciation, timing, or lip-sync accuracy; record pronunciations and review the actual audio.

## Price the exact configuration

The direct API billing page currently prices each generated second. At 1080p, `kling-v3` is **$0.112/s silent** and **$0.168/s with native audio**; 720p is $0.084/s and $0.126/s. Native 4K for eligible `kling-v3`/`kling-v3-omni` configurations is listed at **$0.42/s**. `kling-3.0-turbo` with native audio is $0.112/s at 720p and $0.14/s at 1080p. Omni price depends on whether video input and native audio are used. [Current API billing](https://kling.ai/document-api/productBilling/billingMethod)

Before each paid create:

1. Reopen the billing table and exact model task page; bind model, task, mode/resolution, sound, duration, references, and variant count to the estimate.
2. Multiply the dated per-second rate by duration and count. A 5-second 1080p silent `kling-v3` create is currently `$0.112 Ã— 5 = $0.56`; with native audio it is `$0.168 Ã— 5 = $0.84`.
3. Treat each reroll, edit, extension, or variant as a new potential charge. Do not assume failed/shortened tasks are refunded; Motion Control explicitly warns that extracting a shorter valid motion segment can remain non-refundable.
4. Obtain explicit approval of the exact request digest and a finite covering maximum. A UI â€œGenerateâ€ confirmation or generic â€œuse Klingâ€ instruction is not spend approval.
5. Check balance, package validity, model permission, concurrency, QPS, and IP allowlisting. Codes `1101/1102` concern balance/packages; `1302/1303` concern rate/concurrency. Do not buy, recharge, or change account settings without authority.

## Build prompts around time and coverage

For one shot, specify subject and persistent traits; physical action; setting; framing/lens; camera movement; lighting/color/texture; temporal beats; and sound. Keep the number of actions realistic for 3â€“15 seconds.

```text
Single continuous 5-second shot, no cuts. A hand-thrown ceramic cup sits on a dark walnut table.
[0â€“2s] Macro close-up; a ribbon of steam curls upward in quiet morning light.
[2â€“5s] Slow 10 cm dolly left reveals a rain-streaked window; keep the cup shape and glaze unchanged.
Natural shallow depth of field, restrained blue-gray palette, believable steam and reflections.
No people, no lettering, no logo. Audio off.
```

For image-to-video, treat the image as the identity/composition anchor and prompt primarily the change: what moves, what must remain fixed, camera behavior, and the end condition. For start/end frames, demand a plausible bridge rather than unrelated events.

For multi-shot, make every cut purposeful. VIDEO 3.0 offers automatic Multi-Shot and custom shot-level duration/framing/viewpoint/action/camera control. Custom plans can contain up to six shots; shot durations must sum to the total. Avoid squeezing six unrelated ideas into 15 seconds.

```json
{
  "model_name": "kling-v3",
  "multi_shot": true,
  "shot_type": "customize",
  "multi_prompt": [
    {"index": 1, "duration": "3", "prompt": "Wide dawn exterior: a cyclist stops outside a small bakery; gentle locked camera."},
    {"index": 2, "duration": "2", "prompt": "Close-up: the same gloved hand lifts the warm paper bag; steam in backlight."}
  ],
  "duration": "5",
  "mode": "pro",
  "aspect_ratio": "16:9",
  "sound": "off"
}
```

This is an **example**, not a universal template. Confirm the live 3.0 task schema before use. With `multi_shot=true`, custom shot prompts replace the single prompt; keep indices continuous and durations exact.

For native audio, name the speaker before each quoted line, language/accent only when necessary, vocal intent, ambience, effects, and exclusions. Keep dialogue short enough to speak naturally. Separate factual copy, legal claims, exact music, and brand text into post-production when correctness is mandatory.

## Manage references and motion as production assets

The 3.0 Omni guide currently documents:

- Up to seven images, each at least 300 px in both dimensions, at most 10 MB, JPG/JPEG/PNG.
- One reference video, 3â€“10 seconds, at most 200 MB, resolution no greater than 2K.
- With a video, no more than four total images/Elements; without a video, up to seven.
- A multi-image Element can use up to four views. A character voice binding may use 5â€“30 seconds of clean single-person speech; a video character Element may use a 3â€“8 second single-character clip.

**FIELD-SCOPED LIMITS, NOT ONE GLOBAL LIMIT:** The current Omni guide says a *generated VIDEO 3.0/3.0 Omni output* can be 3â€“15 seconds, but its FAQ separately caps an *uploaded reference video* at 3â€“10 seconds. Do not reinterpret the 15-second generation announcement as a 15-second upload allowance. Keep the reference-video input at 10 seconds unless the exact current API task schema explicitly changes that input field; retain the evidence and date for any override. Likewise, confirm that a requested reference-video/native-audio/4K combination is supported rather than combining separate feature announcements.

Hash and content-validate every source before upload; record byte size, MIME, rights, consent, purpose, and remote identifier. Use private, short-lived fetch URLs or accepted base64â€”not public buckets. Never log signed URLs or base64. Reference tags/Element names must map unambiguously to their actual assets; a tag does not guarantee identity, product color, costume, text, or voice preservation.

Motion Control transfers body, face, and hand dynamics from a driving video to one character image. Match full/half-body framing; keep the body/head visible; prefer a continuous 3â€“30 second single-character take with moderate motion and no cuts/camera movement. The official guide warns that multi-person input selects the largest on-screen person, complex/fast motion may be truncated, and generated duration can be shorter while credits remain consumed. Element binding uses facial reference information, not clothing, hair, makeup, or props. [Motion Control guide](https://kling.ai/quickstart/motion-control-user-guide), [technical report and impact statement](https://arxiv.org/abs/2603.03160)

Require documented consent from the referenced person **and** the driving performer for motion, face, voice, dialogue, distribution, and material transformations. Reject intimate abuse, deceptive impersonation, harassment, exploitation of minors, unlawful surveillance, and unauthorized political/public-figure persuasion. Do not weaken a `1300/1301` safety response or move the request to a gateway to evade it.

## Use a fail-closed direct API transaction

The direct API is asynchronous. Current video results are provider-hosted delivery artifacts, not durable storage; first-party API materials say generated images/videos are purged after 30 days, while paid API terms say prompts and responses are logged for 30 days. Download promptly into controlled storage. `external_task_id` helps reconciliation but is **not documented as an idempotency key**. If POST outcome is ambiguous and no provider task ID is durable, stop and reconcile; never â€œretry just in case.â€

The following complete **example** submits one prompt-led `kling-v3` text-to-video task through the current international API. It defaults to offline dry-run, binds exact approval plus fresh pricing evidence and an exact delivery-host allowlist, performs at most one POST, uses only bounded GET retries, downloads without forwarding the API key, validates the MP4, and never overwrites an artifact. Its durable staged-artifact record also closes the crash window between validation, atomic publication, and final ledger state. It intentionally excludes 4K, Omni references, callbacks, and automatic create replay.

```python
#!/usr/bin/env python3
import argparse, hashlib, http.client, ipaddress, json, os, random, socket, ssl
import subprocess, tempfile, threading, time, uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlsplit

API_HOST = "api-singapore.klingai.com"
MODEL = "kling-v3"
MAX_JSON = 1024 * 1024
MAX_VIDEO = 250 * 1024 * 1024
MAX_TOOL = 1024 * 1024
RATES = {("std", "off"): Decimal("0.084"), ("std", "on"): Decimal("0.126"),
         ("pro", "off"): Decimal("0.112"), ("pro", "on"): Decimal("0.168")}

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
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path); fsync_directory(path.parent)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def claim_once(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())
    fsync_directory(path.parent)

def read_small_json(path):
    if path.stat().st_size > MAX_JSON: raise RuntimeError("record exceeds cap")
    with path.open("rb") as f: raw = f.read(MAX_JSON + 1)
    value = json.loads(raw)
    if not isinstance(value, dict): raise RuntimeError("record must be an object")
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

def api_json(method, path, key, payload=None, timeout=60):
    body = canonical(payload) if payload is not None else None
    headers = {"Authorization": "Bearer " + key, "Accept": "application/json"}
    if body is not None: headers["Content-Type"] = "application/json"
    connection = http.client.HTTPSConnection(API_HOST, 443, timeout=timeout, context=ssl.create_default_context())
    try:
        connection.request(method, path, body=body, headers=headers); response = connection.getresponse()
        raw = response.read(MAX_JSON + 1)
        if len(raw) > MAX_JSON: raise RuntimeError("API response exceeds cap")
        if response.status < 200 or response.status >= 300:
            retry = response.getheader("Retry-After")
            try: retry = min(60.0, max(0.0, float(retry)))
            except (TypeError, ValueError): retry = None
            raise APIError(f"API HTTP {response.status}", response.status, retry, hashlib.sha256(raw).hexdigest())
        try: value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise APIError("API returned invalid JSON", response.status, body_sha256=hashlib.sha256(raw).hexdigest()) from exc
        if not isinstance(value, dict): raise RuntimeError("API response is not an object")
        return value
    finally: connection.close()

def safe_get(call, deadline, attempts=5):
    for attempt in range(attempts):
        try: return call()
        except Exception as exc:
            if attempt + 1 == attempts or time.monotonic() >= deadline: raise
            delay = getattr(exc, "retry_after", None) or min(20, 2 ** attempt) * (1 + random.random() * 0.25)
            if time.monotonic() + delay >= deadline: raise
            time.sleep(delay)

class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, address):
        super().__init__(host, 443, timeout=60, context=ssl.create_default_context()); self.address = address
    def connect(self):
        sock = socket.create_connection((self.address, 443), self.timeout)
        try: self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
        except BaseException:
            sock.close(); raise

def download_video(url, stage_path, allowed_hosts):
    parsed = urlsplit(url)
    host = (parsed.hostname or "").lower()
    if (parsed.scheme != "https" or parsed.username or parsed.password or parsed.fragment
            or parsed.port not in (None, 443) or not parsed.path
            or host not in allowed_hosts):
        raise RuntimeError("delivery URL host is not an exact approved host")
    try: ipaddress.ip_address(host); raise RuntimeError("IP-literal delivery URL rejected")
    except ValueError: pass
    addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)})
    if not addresses or any(not ipaddress.ip_address(item).is_global for item in addresses):
        raise RuntimeError("delivery host did not resolve publicly")
    connection = PinnedHTTPSConnection(host, addresses[0]); created = False
    try:
        target = parsed.path + (("?" + parsed.query) if parsed.query else "")
        connection.request("GET", target, headers={"Accept": "video/mp4"}); response = connection.getresponse()
        if 300 <= response.status < 400: raise RuntimeError("delivery redirect rejected")
        if response.status != 200: raise RuntimeError(f"delivery HTTP {response.status}")
        if response.getheader("Content-Type", "").split(";", 1)[0].lower() != "video/mp4":
            raise RuntimeError("delivery MIME rejected")
        length = response.getheader("Content-Length")
        if length and (not length.isdigit() or int(length) > MAX_VIDEO): raise RuntimeError("declared size rejected")
        fd = os.open(stage_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600); created = True
        total = 0
        with os.fdopen(fd, "wb") as f:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk: break
                total += len(chunk)
                if total > MAX_VIDEO: raise RuntimeError("download crossed byte cap")
                f.write(chunk)
            f.flush(); os.fsync(f.fileno())
        return stage_path
    except BaseException:
        if created and stage_path.exists(): stage_path.unlink()
        raise
    finally: connection.close()

def inspect_mp4(path, output, mode, aspect, duration, sound):
    with path.open("rb") as f: head = f.read(12)
    if len(head) < 12 or head[4:8] != b"ftyp": raise RuntimeError("MP4 signature rejected")
    args = ["ffprobe", "-v", "error", "-show_entries",
            "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate", "-of", "json", str(path)]
    code, out, _, timed_out, overflow = run_bounded(args, 30)
    if code or timed_out or overflow: raise RuntimeError("ffprobe failed")
    probe = json.loads(out); streams = probe.get("streams", []); videos = [s for s in streams if s.get("codec_type") == "video"]
    if len(videos) != 1: raise RuntimeError("expected one video stream")
    if sound == "on" and not any(s.get("codec_type") == "audio" for s in streams):
        raise RuntimeError("native audio was requested but absent")
    width, height = videos[0].get("width"), videos[0].get("height"); expected = 720 if mode == "std" else 1080
    if not isinstance(width, int) or not isinstance(height, int) or min(width, height) != expected:
        raise RuntimeError("resolution does not match approved mode")
    expected_ratio = {"16:9": Decimal(16) / 9, "9:16": Decimal(9) / 16, "1:1": Decimal(1)}[aspect]
    if abs(Decimal(width) / Decimal(height) - expected_ratio) > Decimal("0.02"):
        raise RuntimeError("aspect ratio does not match approval")
    try: actual = Decimal(str(probe.get("format", {}).get("duration", "")))
    except InvalidOperation as exc: raise RuntimeError("invalid media duration") from exc
    if not actual.is_finite() or abs(actual - Decimal(duration)) > Decimal("0.75"):
        raise RuntimeError("duration outside tolerance")
    code, _, _, timed_out, overflow = run_bounded(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], 300)
    if code or timed_out or overflow: raise RuntimeError("full decode failed")
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): digest.update(chunk)
    return {"path": str(output), "bytes": path.stat().st_size, "sha256": digest.hexdigest(),
            "media": {"duration": str(actual), "width": width, "height": height,
                      "videoCodec": videos[0].get("codec_name"),
                      "audioStreams": sum(s.get("codec_type") == "audio" for s in streams)}}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True); parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--duration", type=int, choices=range(3, 16), default=5)
    parser.add_argument("--aspect", choices=("16:9", "9:16", "1:1"), default="16:9")
    parser.add_argument("--mode", choices=("std", "pro"), default="pro")
    parser.add_argument("--sound", choices=("off", "on"), default="off")
    parser.add_argument("--attempt-id", required=True); parser.add_argument("--attempt-record", type=Path, default=Path("kling-attempt.json"))
    parser.add_argument("--output", type=Path, default=Path("kling-output.mp4"))
    parser.add_argument("--max-usd", required=True); parser.add_argument("--approval-sha256")
    parser.add_argument("--pricing-checked-at", required=True)
    parser.add_argument("--pricing-evidence-sha256", required=True)
    parser.add_argument("--delivery-host", action="append", required=True,
                        help="exact approved Kling delivery host; repeat for each host")
    parser.add_argument("--execute", action="store_true"); parser.add_argument("--resume", action="store_true")
    parser.add_argument("--show-full-plan", action="store_true")
    args = parser.parse_args()
    if not args.prompt.strip() or len(args.prompt) > 2500 or len(args.prompt.encode()) > 10000:
        raise SystemExit("prompt must be 1..2500 characters and at most 10000 UTF-8 bytes")
    if len(args.negative_prompt) > 2500 or len(args.negative_prompt.encode()) > 10000:
        raise SystemExit("negative prompt exceeds local cap")
    try: attempt = uuid.UUID(args.attempt_id); maximum = Decimal(args.max_usd)
    except (ValueError, InvalidOperation) as exc: raise SystemExit("attempt ID or maximum invalid") from exc
    if attempt.version != 4 or str(attempt) != args.attempt_id.lower(): raise SystemExit("attempt ID must be canonical UUIDv4")
    if (len(args.pricing_evidence_sha256) != 64
            or any(c not in "0123456789abcdef" for c in args.pricing_evidence_sha256)):
        raise SystemExit("pricing evidence must be a lowercase SHA-256")
    try: checked_at = datetime.fromisoformat(args.pricing_checked_at.replace("Z", "+00:00"))
    except ValueError as exc: raise SystemExit("pricing timestamp must be ISO-8601") from exc
    if checked_at.tzinfo is None: raise SystemExit("pricing timestamp must include a timezone")
    allowed_hosts = sorted(set(host.lower().rstrip(".") for host in args.delivery_host))
    if (not allowed_hosts or len(allowed_hosts) > 8
            or any(not host or len(host) > 253 or "*" in host or "/" in host or "@" in host for host in allowed_hosts)):
        raise SystemExit("delivery hosts must be 1..8 exact DNS names")
    for host in allowed_hosts:
        try: ipaddress.ip_address(host); raise SystemExit("delivery hosts cannot be IP literals")
        except ValueError: pass
    estimate = RATES[(args.mode, args.sound)] * args.duration
    if not maximum.is_finite() or maximum <= 0 or maximum < estimate: raise SystemExit("maximum must be finite and cover estimate")
    output, record_path = args.output.resolve(), args.attempt_record.resolve()
    stage_path = output.with_name("." + output.name + ".kling-stage")
    if output.suffix.lower() != ".mp4" or output == record_path or stage_path in {output, record_path}:
        raise SystemExit("output path rejected")
    request = {"model_name": MODEL, "prompt": args.prompt, "negative_prompt": args.negative_prompt,
               "duration": str(args.duration), "mode": args.mode, "aspect_ratio": args.aspect,
               "sound": args.sound, "external_task_id": str(attempt)}
    request_hash = hashlib.sha256(canonical(request)).hexdigest()
    envelope = {"backend": "kling-direct-international", "endpoint": "/v1/videos/text2video", "host": API_HOST,
        "request": request, "attemptId": str(attempt), "attemptRecord": str(record_path),
        "outputPolicy": {"path": str(output), "stagePath": str(stage_path), "exactDeliveryHosts": allowed_hosts,
                         "maxBytes": MAX_VIDEO, "mime": "video/mp4", "fullDecode": True, "noOverwrite": True},
        "cost": {"pricingCheckedAt": checked_at.isoformat(), "pricingEvidenceSha256": args.pricing_evidence_sha256,
                 "rateUsdPerSecond": str(RATES[(args.mode, args.sound)]),
                 "seconds": args.duration, "creates": 1, "estimatedMaxUsd": str(estimate), "approvedMaxUsd": str(maximum)}}
    approval = hashlib.sha256(canonical(envelope)).hexdigest()
    safe_request = {**request, "prompt": "sha256:" + hashlib.sha256(args.prompt.encode()).hexdigest(),
                    "negative_prompt": "sha256:" + hashlib.sha256(args.negative_prompt.encode()).hexdigest()}
    print(json.dumps({"dryRun": not args.execute, "approvalSha256": approval,
        "plan": {**envelope, "request": safe_request}}, indent=2))
    if args.show_full_plan: print(json.dumps({"protectedFullPlan": envelope}, indent=2))
    if not args.execute: return 0
    if args.approval_sha256 != approval: raise SystemExit("exact approval digest mismatch")
    age = datetime.now(timezone.utc) - checked_at.astimezone(timezone.utc)
    if age.total_seconds() < -300 or age.total_seconds() > 86400:
        raise SystemExit("pricing evidence must be rechecked within 24 hours of execution")
    key = os.getenv("KLING_API_KEY")
    if not key: raise SystemExit("set server-side KLING_API_KEY")
    if args.resume:
        if not record_path.exists(): raise SystemExit("resume record missing")
        record = read_small_json(record_path)
        if record.get("approval_sha256") != approval or record.get("request_sha256") != request_hash:
            raise SystemExit("resume does not match exact request")
        task_id = record.get("task_id")
        if not isinstance(task_id, str) or not task_id: raise SystemExit("no known task ID; do not replay create")
        expected_artifact = record.get("artifact_staged") or record.get("artifact")
        candidate = output if output.exists() else stage_path if stage_path.exists() else None
        if candidate is not None:
            if not isinstance(expected_artifact, dict):
                if record.get("status") == "downloading" and candidate == stage_path:
                    stage_path.unlink(); fsync_directory(stage_path.parent)
                else: raise SystemExit("unclaimed output/stage exists; refusing overwrite or adoption")
            else:
                artifact = inspect_mp4(candidate, output, args.mode, args.aspect, args.duration, args.sound)
                if (artifact.get("sha256") != expected_artifact.get("sha256")
                        or artifact.get("bytes") != expected_artifact.get("bytes")):
                    raise SystemExit("recovered artifact does not match durable staged evidence")
                if candidate == stage_path:
                    if output.exists(): raise SystemExit("output appeared during recovery")
                    os.replace(stage_path, output); fsync_directory(output.parent)
                record.update(status="artifact_saved", artifact=artifact, updated_unix=int(time.time()))
                record.pop("artifact_staged", None); atomic_json(record_path, record)
                print(json.dumps(record, indent=2)); return 0
    else:
        if output.exists() or stage_path.exists(): raise SystemExit("output or stage already exists")
        record = {"attempt_id": str(attempt), "approval_sha256": approval, "request_sha256": request_hash,
                  "status": "posting", "task_id": None, "created_unix": int(time.time())}
        try: claim_once(record_path, record)
        except FileExistsError as exc: raise SystemExit("attempt already claimed; use resume") from exc
        try: response = api_json("POST", "/v1/videos/text2video", key, request, 120)
        except Exception as exc:
            known_rejection = (isinstance(exc, APIError) and exc.status is not None and 400 <= exc.status < 500
                               and exc.status not in {408, 409, 425, 429})
            record.update(status="create_rejected" if known_rejection else "create_outcome_unknown",
                          error_type=type(exc).__name__, http_status=getattr(exc, "status", None),
                          error_body_sha256=getattr(exc, "body_sha256", None))
            atomic_json(record_path, record)
            if known_rejection: raise RuntimeError("provider rejected create before acceptance") from exc
            raise RuntimeError("create outcome unknown; reconcile account, never replay") from exc
        if response.get("code") != 0:
            record.update(status="create_rejected", service_code=response.get("code")); atomic_json(record_path, record)
            raise RuntimeError("provider rejected create")
        data = response.get("data") or {}; task_id = data.get("task_id")
        if (not isinstance(task_id, str) or not 1 <= len(task_id) <= 200
                or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_." for c in task_id)):
            record.update(status="create_outcome_unknown", error_type="MissingOrInvalidTaskId"); atomic_json(record_path, record)
            raise RuntimeError("create returned no safe task ID; reconcile")
        record.update(status="task_id_saved", task_id=task_id, request_id=response.get("request_id"), updated_unix=int(time.time()))
        atomic_json(record_path, record)
    deadline = time.monotonic() + 1200
    while True:
        response = safe_get(lambda: api_json("GET", "/v1/videos/text2video/" + task_id, key, timeout=45), deadline)
        if response.get("code") != 0: raise RuntimeError("task query failed")
        data = response.get("data") or {}; status = data.get("task_status")
        if status == "succeed": break
        if status == "failed":
            message = str(data.get("task_status_msg", ""))
            record.update(status="generation_failed", task_status_msg_sha256=hashlib.sha256(message.encode()).hexdigest())
            atomic_json(record_path, record)
            raise RuntimeError("generation failed")
        if status not in {"submitted", "processing"}: raise RuntimeError("unknown task status")
        if time.monotonic() >= deadline: raise TimeoutError("generation exceeded 20 minutes")
        time.sleep(8 + random.random() * 2)
    videos = ((data.get("task_result") or {}).get("videos") or [])
    if len(videos) != 1 or not isinstance(videos[0], dict) or not isinstance(videos[0].get("url"), str):
        raise RuntimeError("expected exactly one video URL")
    url = videos[0]["url"]; output.parent.mkdir(parents=True, exist_ok=True)
    record.update(status="downloading", delivery_url_sha256=hashlib.sha256(url.encode()).hexdigest(), stage_path=str(stage_path))
    atomic_json(record_path, record)
    try:
        download_video(url, stage_path, set(allowed_hosts))
        artifact = inspect_mp4(stage_path, output, args.mode, args.aspect, args.duration, args.sound)
    except BaseException as exc:
        record.update(status="artifact_validation_failed", error_type=type(exc).__name__); atomic_json(record_path, record); raise
    record.update(status="artifact_staged", artifact_staged=artifact, final_unit_deduction=data.get("final_unit_deduction"),
        remote_purge_expected_within_days=30, rights_review="required", creative_qa="pending",
        ai_disclosure="required", provenance_credentials="not_documented", updated_unix=int(time.time()))
    atomic_json(record_path, record)
    if output.exists(): raise RuntimeError("output appeared before publication")
    os.replace(stage_path, output); fsync_directory(output.parent)
    record.update(status="artifact_saved", artifact=artifact, updated_unix=int(time.time()))
    record.pop("artifact_staged", None); atomic_json(record_path, record)
    print(json.dumps(record, indent=2)); return 0

if __name__ == "__main__": raise SystemExit(main())
```

Dry-run and approve the printed digest:

```bash
python kling_generate.py --attempt-id 7f8f06b7-9e68-4f0a-bf16-3eaf3ee9d6c4 --max-usd 0.56 --pricing-checked-at 2026-07-10T12:00:00Z --pricing-evidence-sha256 "$BILLING_SHA256" --delivery-host "$KLING_DELIVERY_HOST" --prompt "Single continuous five-second macro dolly shot of steam rising from a ceramic cup; rain outside; no people, text, or logo."
```

Execute the unchanged request once:

```bash
python kling_generate.py --execute --approval-sha256 "<exact digest>" --attempt-id 7f8f06b7-9e68-4f0a-bf16-3eaf3ee9d6c4 --max-usd 0.56 --pricing-checked-at 2026-07-10T12:00:00Z --pricing-evidence-sha256 "$BILLING_SHA256" --delivery-host "$KLING_DELIVERY_HOST" --prompt "Single continuous five-second macro dolly shot of steam rising from a ceramic cup; rain outside; no people, text, or logo."
```

`BILLING_SHA256` is the SHA-256 of the dated first-party billing evidence actually reviewed; `KLING_DELIVERY_HOST` is an exact hostname authorized by the current direct-API delivery contract, not a wildcard or a host inferred from an untrusted URL. Repeat `--delivery-host` only for additional exact approved hosts. Execution refuses pricing evidence older than 24 hours.

Use the same arguments plus `--resume --execute` only when the record already holds a task ID. Do not use `--resume` to recover `posting` or `create_outcome_unknown`; reconcile `external_task_id`, account usage, request ID, logs, or support first. A resume may adopt only a staged/published artifact whose bytes and SHA-256 match durable ledger evidence. Verify the endpoint and field types on the live `kling-v3` text-to-video page before production because the documentation UI is actively being restructured.

## Govern data, rights, and release

**FACT:** Paid API terms say Kling acts as a data processor, does not use paid API prompts/files/responses to improve models, and logs prompts/responses for 30 days for service/safety purposes. The API privacy policy says data is stored on servers in Singapore and may be accessed/transferred internationally by operational teams/providers. Retention can extend for legal, compliance, dispute, or legitimate purposes. This is not zero retention or EU residency. [API paid terms](https://kling.ai/document-api/protocols/paidServiceProtocol), [API privacy](https://kling.ai/document-api/protocols/privacyPolicy)

**FACT:** The paid API terms allow commercial use, but require the operator to hold rights/authorization for input and warn that generated output can still infringe. Ownership/copyrightability depends on applicable law. General Kling terms require prominent Kling AI identification when output is distributed unless written permission provides otherwise. Apply the stricter controlling account/API agreement and local synthetic-media law; do not infer that â€œwatermark-freeâ€ means disclosure-free. [API paid terms](https://kling.ai/document-api/protocols/paidServiceProtocol), [Kling terms](https://kling.ai/docs/user-policy)

No first-party source reviewed promises C2PA or a durable cryptographic provenance credential for direct Kling video output. Treat provenance as **UNKNOWN**. Preserve request/source hashes and the original file; add a clear AI disclosure and any required brand mark without claiming it is provider-signed.

Before release, inspect every frame and listen end-to-end. Confirm dimensions, duration, frame rate, audio streams, full decode, loudness/peaks, dialogue/lip-sync/speaker assignment, temporal logic, faces/hands/anatomy, identity/costume/product continuity, logos/text/color, unsafe content, factual/advertising claims, rights, disclosure, and platform specs. A technically valid MP4 is not an approved creative master.

## Handle failures by phase

- **Before POST:** fix schema, rights, auth, balance, model access, or exact approval; no generation has been accepted.
- **POST returns a task ID:** persist it, then query that task. Slow processing, `429`, `500`, `503`, or `504` does not authorize a second create.
- **POST outcome unknown:** stop. `external_task_id` is a reconciliation handle, not a documented idempotency guarantee.
- **Safety rejection:** do not rephrase to evade controls or route through a reseller. Reassess legitimacy and consent.
- **Failed task or shortened motion:** record status and actual deduction; do not promise a refund.
- **Delivery URL or media invalid:** quarantine/delete the temporary file, retain sanitized evidence, and do not publish. A new paid generation needs a new attempt ID and approval.
- **Preview/update drift:** reopen official auth, model, billing, update, and policy pages. Do not guess a replacement ID or mix a gateway contract into the direct API.

## Label evidence honestly

- **FACT:** current first-party API field, model capability, price, term, or limit.
- **PROVIDER CLAIM:** Kling/Kuaishou quality, benchmark, â€œnative,â€ consistency, physics, or efficiency statement not independently verified.
- **OBSERVATION:** a dated result from a reproducible task, including surface, model, request hash, inputs, account region, and output checks.
- **HEURISTIC:** production advice such as limiting actions, matching motion-reference framing, or using one change per edit.
- **UNKNOWN:** undocumented hard latency, exact create idempotency, direct API C2PA, guaranteed identity/text/audio accuracy, or any field not visible on the current task page.

Reverify first-party sources: [API overview](https://kling.ai/document-api), [authentication/errors](https://kling.ai/document-api/apiReference/commonInfo), [billing](https://kling.ai/document-api/productBilling/billingMethod), [3.0 task index](https://kling.ai/document-api/3-0/model-access/ai-video-generation), [3.0 guide](https://kling.ai/quickstart/klingai-video-3-model-user-guide), [3.0 Omni guide](https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide), [Motion Control guide](https://kling.ai/quickstart/motion-control-user-guide), [API paid terms](https://kling.ai/document-api/protocols/paidServiceProtocol), [API privacy](https://kling.ai/document-api/protocols/privacyPolicy), [Kling-Omni report](https://arxiv.org/abs/2512.16776), and [Motion Control report](https://arxiv.org/abs/2603.03160).


