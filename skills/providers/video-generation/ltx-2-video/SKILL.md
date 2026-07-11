---
name: ltx-2-video
description: Generate and edit synchronized audio-video with LTX-2.3 using the official hosted LTX API or official local/open-weight LTX-2 repository. Use for text-to-video, image-to-video, audio-to-video, retake, extend, HDR conversion, local inference, checkpoint selection, quantization, and LTX-specific production planning.
---

# LTX-2 Video

Use LTX-2.3 when a workflow needs jointly generated video and audio, first/last-frame conditioning, audio-driven video, partial retakes, extension, or an official self-hosted path. Keep the hosted API contract, local weight contract, and research claims separate.

## Start with a plan

1. State the requested mode, duration, aspect ratio, resolution, frame rate, audio requirement, delivery codec, and whether inputs contain people or sensitive data.
2. Choose `hosted` or `local` with the routing table below. Do not infer that â€œopenâ€ means cost-free, unrestricted, or operationally easy.
3. Write a dry-run plan before any paid request, asset upload, or model download. Include the exact endpoint/model or checkpoint filenames, estimated hosted charge, output paths, and validation steps.
4. Require explicit approval before the first billable API submission or multi-gigabyte download. Never enable auto top-up on the user's behalf.
5. Preserve provenance: prompt, seed where available, model/checkpoint, API request/job ID, source asset hashes, generation parameters, license review date, and output hash.

## Route deliberately

| Need | Preferred route | Contract |
|---|---|---|
| Managed T2V/I2V with 4K options | Hosted async V2 | `ltx-2-3-fast` for iteration or longer 1080p clips; `ltx-2-3-pro` for fidelity |
| Existing 2â€“20 s audio drives visuals | Hosted A2V | Pro only; prompt or image is required; billed by input audio seconds |
| Replace a section of a video | Hosted retake | Pro only; billed by the entire input video duration, not only the edit span |
| Add material at start/end | Hosted extend | Pro only; extension plus context is billable and capped at 505 total frames |
| Convert SDR video for HDR grading | Hosted HDR | Async only; returns a ZIP of linear EXR frames, not a finished MP4 |
| Data control, reproducibility, custom LoRAs, offline work | Official local repo | Own GPU, dependencies, checkpoints, Gemma terms, output pipeline, and license compliance |
| Node-based local workflow | Official ComfyUI-LTXVideo | Pin workflow and custom-node revisions; treat it as a separate execution surface |

Prefer async V2 for production. The sync V1 endpoints return an MP4 in one long request and are suitable only for short experiments where connection lifetime is acceptable. Async V2 is still labeled Beta in the official changelog as of 2026-07-10; isolate its adapter and test status parsing defensively.

## Pin the current model family

Use hosted IDs `ltx-2-3-fast` and `ltx-2-3-pro`. As announced on 2026-07-02, `ltx-2-fast` and `ltx-2-pro` deprecate on 2026-07-15, are temporarily served by 2.3 at old pricing, and are removed on 2026-08-15. Reject those old IDs in new work and re-check the deprecation page after that date.

Current hosted generation envelope, verified 2026-07-10:

- T2V/I2V Fast: 1080p at 24/25 fps supports 6, 8, 10, 12, 14, 16, 18, or 20 seconds; 1080p at 48/50 fps and all 1440p/4K combinations support 6, 8, or 10 seconds.
- T2V/I2V Pro: 1080p, 1440p, or 4K at 24/25/48/50 fps supports 6, 8, or 10 seconds.
- Hosted aspect ratios are 16:9 or 9:16. Use documented exact dimensions rather than inventing arbitrary sizes.
- `generate_audio` defaults to true. Make silence explicit when required.
- `last_frame_uri` is available only on 2.3 I2V model IDs.

Do not project the original LTX-2 paper's 19B architecture onto every 2.3 artifact. The January 2026 technical report describes a 14B video stream plus 5B audio stream. The current Hugging Face filenames are 22B LTX-2.3 checkpoints. Cite each claim to its version and avoid parameter arithmetic across releases.

## Select a hosted operation

Use `https://api.ltx.video` with `Authorization: Bearer $LTXV_API_KEY`.

| Operation | Submit | Key constraints |
|---|---|---|
| Text to video | `POST /v2/text-to-video` | prompt â‰¤5000 chars; model, duration, resolution required |
| Image to video | `POST /v2/image-to-video` | first-frame `image_uri`; optional 2.3-only `last_frame_uri` |
| Audio to video | `POST /v2/audio-to-video` | Pro; audio 2â€“20 s; image or prompt required; output 25 fps |
| Retake | `POST /v2/retake` | Pro; input â‰¥73 frames, â‰¤4K; edit duration â‰¥2 s; replace audio, video, or both |
| Extend | `POST /v2/extend` | Pro; add 2â€“20 s at `start` or `end`; 16:9/9:16 input; preserves input resolution |
| SDR to HDR | `POST /v2/video-to-video-hdr` | 2.3 Pro; async only; result key is `exr_frames_url` |

For all async jobs, persist the returned `id` before polling `GET /v2/{operation}/{id}` every five seconds. Accept only `pending`, `processing`, `completed`, or `failed`. On completion, read `result.video_url`, except HDR uses `result.exr_frames_url`. Job state and output URLs expire 24 hours after a terminal state. Download promptly, hash locally, then validate.

The public API does not document an idempotency key. If a submit request times out without a response, do not blindly POST again: inspect the developer console or contact support with the timestamp and any `x-request-id`. It may be impossible to prove whether the first request created a billable job.

Respect 429 `Retry-After` and distinguish `concurrency_limit_error` from `rate_limit_error`. The published default concurrency is two, but quotas are plan-specific. Bound GET retries with jitter; never retry validation/auth/payment errors. Log `x-request-id` without logging the bearer key or signed asset URL.

## Budget before submitting

Hosted pricing verified 2026-07-10, in USD per second:

| Surface | 1080p | 1440p | 4K | Billing basis |
|---|---:|---:|---:|---|
| 2.3 Fast T2V/I2V | .06 | .12 | .24 | output duration |
| 2.3 Pro T2V/I2V | .08 | .16 | .32 | output duration |
| 2.3 Pro A2V | .10 | â€” | â€” | input audio duration |
| 2.3 Pro retake | .10 | â€” | â€” | full input video duration |
| 2.3 Pro extend | .10 | â€” | â€” | extension + context, capped at 505 frames |
| 2.3 Pro HDR | .20 | .40 | .80 | input duration at its resolution tier |

Re-fetch pricing immediately before production use. A quote is an estimate until inputs are probed and the request is accepted. Keep prepaid balance small and require a project-level cap.

## Handle inputs conservatively

- Prefer a short-lived HTTPS URL or `/v1/upload`. The upload flow returns a pre-signed PUT URL valid for one hour; forward all `required_headers`. Uploaded `storage_uri` values last 24 hours and files are limited to 100 MB.
- Public HTTPS inputs must be directly reachable without redirects or IP-address hosts. Published limits are 15 MB/10 s fetch for images and 32 MB/30 s for audio/video. Data URIs allow 7 MB images or 15 MB audio/video.
- Images: PNG, JPEG, or WebP. Video: MP4/MOV/MKV with H.264 or H.265. Audio: WAV/MP3/M4A/OGG with supported codecs; PCM and HE-AAC are not accepted, and AAC must be AAC-LC.
- Probe video/audio locally with `ffprobe` before upload. Check duration, dimensions, frame rate, frame count, streams, rotation, codec, and audio channel layout.
- Do not claim zero retention or no training. The current API agreement permits processing Usage Data and textual prompts for analytics, product improvement, research, and development when aggregated and anonymized. The 24-hour job/output window is not a complete data-retention statement. For personal data, regulated content, residency requirements, or confidential footage, obtain the current DPA and contractual answers or self-host.

## Write prompts for joint audio-video

Use one literal, chronological paragraph, usually under 200 words. Describe subject and setting, then actions in order, camera motion, lighting/color, dialogue, Foley, ambience, and the final beat. Avoid contradictory cuts, too many simultaneous actions, and vague mood-only wording.

Example:

> Medium-wide shot inside a quiet midnight diner, rain tracing the windows. A tired cyclist enters from frame left, removes a yellow helmet, and sits at the counter. The camera slowly dollies closer as the server places a steaming mug beside them. The cyclist says softly, â€œI made it before the storm.â€ Ceramic taps wood; rain and a distant refrigerator hum continue underneath. Neon cyan and warm tungsten reflections ripple across the counter. Hold on their relieved smile for the final second, with no cut.

For I2V, describe motion and change rather than redescribing every static pixel. For A2V, anchor speakers, performance, and camera behavior to audible beats. Treat exact speech, identity, hand detail, and text rendering as QA risks, not guarantees.

## Run a hosted dry-run-first client

This complete standard-library client plans a current T2V request by default. It submits only with `--execute` and an approval digest that binds the exact request, finite cost ceiling, fresh pricing evidence, attempt ledger, output policy, and exact delivery hosts. It never retries POST, persists the job ID atomically, resumes only by GET, downloads without the API credential through a pinned public address, and verifies before crash-resumable atomic publication.

```python
#!/usr/bin/env python3
import argparse, hashlib, http.client, ipaddress, json, os, random, socket, ssl
import subprocess, sys, tempfile, threading, time, uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

API = "https://api.ltx.video"
RATES = {
    ("ltx-2-3-fast", "1920x1080"): Decimal("0.06"),
    ("ltx-2-3-fast", "2560x1440"): Decimal("0.12"),
    ("ltx-2-3-fast", "3840x2160"): Decimal("0.24"),
    ("ltx-2-3-pro", "1920x1080"): Decimal("0.08"),
    ("ltx-2-3-pro", "2560x1440"): Decimal("0.16"),
    ("ltx-2-3-pro", "3840x2160"): Decimal("0.32"),
}
MAX_JSON = 1024 * 1024
MAX_VIDEO = 2_000_000_000
MAX_TOOL = 1024 * 1024

class APIError(RuntimeError):
    def __init__(self, message, status=None, retry_after=None, body_sha256=None, request_id=None):
        super().__init__(message); self.status = status; self.retry_after = retry_after
        self.body_sha256 = body_sha256; self.request_id = request_id

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
            json.dump(value, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n"); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path); fsync_directory(path.parent)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def claim_once(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n"); f.flush(); os.fsync(f.fileno())
    fsync_directory(path.parent)

def read_record(path):
    if path.stat().st_size > MAX_JSON: raise RuntimeError("attempt record exceeds cap")
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict): raise RuntimeError("attempt record must be an object")
    return value

def call_json(req, timeout=45):
    try:
        with urlopen(req, timeout=timeout) as r:
            body = r.read(MAX_JSON + 1)
            if len(body) > MAX_JSON: raise RuntimeError("API response exceeds cap")
            try: value = json.loads(body)
            except json.JSONDecodeError as exc:
                raise APIError("API returned invalid JSON", r.status, body_sha256=hashlib.sha256(body).hexdigest(),
                               request_id=r.headers.get("x-request-id")) from exc
            if not isinstance(value, dict): raise RuntimeError("API response is not an object")
            return value, r.headers.get("x-request-id")
    except HTTPError as e:
        body = e.read(MAX_JSON + 1)
        if len(body) > MAX_JSON: body = body[:MAX_JSON]
        try: delay = min(30.0, max(0.0, float(e.headers.get("Retry-After"))))
        except (TypeError, ValueError): delay = None
        raise APIError(f"API HTTP {e.code}", e.code, delay, hashlib.sha256(body).hexdigest(),
                       e.headers.get("x-request-id")) from e

def safe_get(req, deadline, attempts=5):
    last = None
    for attempt in range(attempts):
        try: return call_json(req(), timeout=45)
        except APIError as exc:
            if exc.status not in {429, 500, 503, 504, 529}: raise
            last = exc
            delay = exc.retry_after or min(20, 2 ** attempt) * (1 + random.random() * 0.25)
        except URLError as exc:
            last = exc
            delay = min(20, 2 ** attempt) * (1 + random.random() * 0.25)
        if attempt + 1 == attempts or time.monotonic() + delay >= deadline: raise last
        time.sleep(delay)

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

def inspect_mp4(path, output, resolution, duration, fps, silent):
    with path.open("rb") as f: head = f.read(12)
    if len(head) < 12 or head[4:8] != b"ftyp": raise RuntimeError("MP4 signature rejected")
    args = ["ffprobe", "-v", "error", "-show_entries",
            "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate", "-of", "json", str(path)]
    code, out, _, timed_out, overflow = run_bounded(args, 30)
    if code or timed_out or overflow: raise RuntimeError("bounded ffprobe failed")
    probe = json.loads(out); streams = probe.get("streams", []); videos = [s for s in streams if s.get("codec_type") == "video"]
    if len(videos) != 1: raise RuntimeError("expected one video stream")
    width, height = videos[0].get("width"), videos[0].get("height")
    expected = tuple(int(item) for item in resolution.split("x"))
    if (width, height) != expected: raise RuntimeError("dimensions do not match approval")
    audio_count = sum(s.get("codec_type") == "audio" for s in streams)
    if (not silent and audio_count < 1) or (silent and audio_count): raise RuntimeError("audio streams do not match approval")
    try: actual = Decimal(str(probe.get("format", {}).get("duration", "")))
    except InvalidOperation as exc: raise RuntimeError("invalid media duration") from exc
    if not actual.is_finite() or abs(actual - Decimal(duration)) > Decimal("0.75"):
        raise RuntimeError("media duration outside tolerance")
    rate = str(videos[0].get("r_frame_rate", "0/1")).split("/", 1)
    try: actual_fps = Decimal(rate[0]) / Decimal(rate[1])
    except (InvalidOperation, ZeroDivisionError, IndexError) as exc: raise RuntimeError("invalid frame rate") from exc
    if not actual_fps.is_finite() or abs(actual_fps - Decimal(fps)) > Decimal("0.01"):
        raise RuntimeError("frame rate does not match approval")
    code, _, _, timed_out, overflow = run_bounded(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], 300)
    if code or timed_out or overflow: raise RuntimeError("bounded full decode failed")
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): digest.update(chunk)
    return {"path": str(output), "bytes": path.stat().st_size, "sha256": digest.hexdigest(),
            "media": {"duration": str(actual), "width": width, "height": height, "fps": str(actual_fps),
                      "videoCodec": videos[0].get("codec_name"), "audioStreams": audio_count}}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--model", choices=["ltx-2-3-fast", "ltx-2-3-pro"], default="ltx-2-3-fast")
    p.add_argument("--duration", type=int, choices=[6,8,10,12,14,16,18,20], default=6)
    p.add_argument("--resolution", choices=["1920x1080","1080x1920","2560x1440","1440x2560","3840x2160","2160x3840"], default="1920x1080")
    p.add_argument("--fps", type=int, choices=[24,25,48,50], default=24)
    p.add_argument("--silent", action="store_true")
    p.add_argument("--attempt-id", required=True); p.add_argument("--attempt-record", type=Path, default=Path("ltx-attempt.json"))
    p.add_argument("--max-usd", required=True); p.add_argument("--approval-sha256")
    p.add_argument("--pricing-checked-at", required=True); p.add_argument("--pricing-evidence-sha256", required=True)
    p.add_argument("--delivery-host", action="append", required=True, help="exact approved result host; repeat as needed")
    p.add_argument("--execute", action="store_true"); p.add_argument("--resume", action="store_true")
    p.add_argument("--max-wait", type=int, default=1800)
    p.add_argument("--output", type=Path, default=Path("ltx-output.mp4"))
    p.add_argument("--show-full-plan", action="store_true")
    a = p.parse_args()
    if not 1 <= len(a.prompt) <= 5000 or len(a.prompt.encode()) > 20000:
        p.error("prompt must be 1..5000 characters and at most 20000 UTF-8 bytes")
    if not 60 <= a.max_wait <= 7200: p.error("max wait must be 60..7200 seconds")
    if a.model.endswith("pro") and a.duration not in (6,8,10): p.error("Pro supports only 6/8/10 s")
    if (a.duration > 10) and not (a.model.endswith("fast") and a.resolution in ("1920x1080","1080x1920") and a.fps in (24,25)):
        p.error("12â€“20 s requires Fast, 1080p, and 24/25 fps")
    if a.duration > 10 or a.resolution not in ("1920x1080","1080x1920") or a.fps not in (24,25):
        if a.duration not in (6,8,10): p.error("this model/resolution/fps combination supports only 6/8/10 s")
    landscape = a.resolution if int(a.resolution.split("x")[0]) > int(a.resolution.split("x")[1]) else "x".join(reversed(a.resolution.split("x")))
    estimate = RATES[(a.model, landscape)] * Decimal(a.duration)
    try: attempt = uuid.UUID(a.attempt_id); ceiling = Decimal(a.max_usd)
    except (ValueError, InvalidOperation) as exc: p.error(f"attempt ID or maximum invalid: {exc}")
    if attempt.version != 4 or str(attempt) != a.attempt_id.lower(): p.error("attempt ID must be canonical UUIDv4")
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
    output, record_path = a.output.resolve(), a.attempt_record.resolve()
    stage_path = output.with_name("." + output.name + ".ltx-stage")
    if output.suffix.lower() != ".mp4" or record_path in {output, stage_path}: p.error("output/record path rejected")
    payload = {"prompt":a.prompt,"model":a.model,"duration":a.duration,"resolution":a.resolution,"fps":a.fps,"generate_audio":not a.silent}
    request_hash = hashlib.sha256(canonical(payload)).hexdigest()
    endpoint = f"{API}/v2/text-to-video"
    envelope = {"backend":"ltx-hosted-async-v2", "endpoint":endpoint, "payload":payload,
        "attemptId":str(attempt), "attemptRecord":str(record_path),
        "outputPolicy":{"path":str(output), "stagePath":str(stage_path), "exactDeliveryHosts":allowed_hosts,
                        "maxBytes":MAX_VIDEO, "mime":["video/mp4","application/octet-stream"],
                        "noOverwrite":True, "fullDecode":True},
        "cost":{"pricingCheckedAt":checked_at.isoformat(), "pricingEvidenceSha256":a.pricing_evidence_sha256,
                "rateUsdPerSecond":str(RATES[(a.model, landscape)]), "seconds":a.duration,
                "creates":1, "estimatedMaxUsd":str(estimate), "approvedMaxUsd":str(ceiling)}}
    approval = hashlib.sha256(canonical(envelope)).hexdigest()
    safe_payload = {**payload, "prompt":"sha256:" + hashlib.sha256(a.prompt.encode()).hexdigest()}
    print(json.dumps({"dryRun":not a.execute, "approvalSha256":approval,
        "plan":{**envelope,"payload":safe_payload}}, indent=2, ensure_ascii=False))
    if a.show_full_plan: print(json.dumps({"protectedFullPlan":envelope}, indent=2, ensure_ascii=False))
    if not a.execute: return 0
    if a.approval_sha256 != approval: raise SystemExit("exact approval digest mismatch")
    age = datetime.now(timezone.utc) - checked_at.astimezone(timezone.utc)
    if age.total_seconds() < -300 or age.total_seconds() > 86400:
        raise SystemExit("pricing evidence must be rechecked within 24 hours of execution")
    if a.resume:
        if not record_path.exists(): raise SystemExit("resume record missing")
        record = read_record(record_path)
        if record.get("approval_sha256") != approval or record.get("request_sha256") != request_hash:
            raise SystemExit("resume does not match exact approved request")
        job_id = record.get("job_id")
        if not isinstance(job_id, str) or not job_id: raise SystemExit("no known job ID; never replay create")
        expected_artifact = record.get("artifact_staged") or record.get("artifact")
        candidate = output if output.exists() else stage_path if stage_path.exists() else None
        if candidate is not None:
            if not isinstance(expected_artifact, dict):
                if record.get("status") == "downloading" and candidate == stage_path:
                    stage_path.unlink(); fsync_directory(stage_path.parent)
                else: raise SystemExit("unclaimed output/stage exists; refusing overwrite or adoption")
            else:
                artifact = inspect_mp4(candidate, output, a.resolution, a.duration, a.fps, a.silent)
                if (artifact.get("sha256") != expected_artifact.get("sha256")
                        or artifact.get("bytes") != expected_artifact.get("bytes")):
                    raise SystemExit("recovered artifact does not match durable staged evidence")
                if candidate == stage_path:
                    if output.exists(): raise SystemExit("output appeared during recovery")
                    os.replace(stage_path, output); fsync_directory(output.parent)
                record.update(status="artifact_saved", artifact=artifact, updated_unix=int(time.time()))
                record.pop("artifact_staged", None); atomic_json(record_path, record)
                print(json.dumps(record, indent=2)); return 0
        key = os.environ.get("LTXV_API_KEY")
        if not key: raise SystemExit("LTXV_API_KEY is required to resume polling")
    else:
        if output.exists() or stage_path.exists(): raise SystemExit("output or stage already exists")
        key = os.environ.get("LTXV_API_KEY")
        if not key: raise SystemExit("LTXV_API_KEY is required")
        output.parent.mkdir(parents=True, exist_ok=True)
        record = {"attempt_id":str(attempt), "approval_sha256":approval, "request_sha256":request_hash,
                  "status":"posting", "job_id":None, "created_unix":int(time.time())}
        try: claim_once(record_path, record)
        except FileExistsError as exc: raise SystemExit("attempt already claimed; use resume") from exc
    if not a.resume:
        req = Request(endpoint, data=canonical(payload), method="POST",
                      headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
        try: job, request_id = call_json(req, timeout=120)
        except Exception as exc:
            known_rejection = (isinstance(exc, APIError) and exc.status in {400,401,402,404,422})
            record.update(status="create_rejected" if known_rejection else "create_outcome_unknown",
                          error_type=type(exc).__name__, http_status=getattr(exc,"status",None),
                          error_body_sha256=getattr(exc,"body_sha256",None), request_id=getattr(exc,"request_id",None))
            atomic_json(record_path, record)
            if known_rejection: raise RuntimeError("provider rejected create before acceptance") from exc
            raise RuntimeError("create outcome unknown; reconcile console/support, never replay") from exc
        job_id = job.get("id")
        if (not isinstance(job_id, str) or not 1 <= len(job_id) <= 200
                or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_." for c in job_id)):
            record.update(status="create_outcome_unknown", error_type="MissingOrInvalidJobId",
                          create_response_sha256=hashlib.sha256(canonical(job)).hexdigest())
            atomic_json(record_path, record); raise RuntimeError("create returned no safe job ID; reconcile")
        record.update(status="job_id_saved", job_id=job_id, created_at=job.get("created_at"), request_id=request_id,
                      create_response_sha256=hashlib.sha256(canonical(job)).hexdigest(), updated_unix=int(time.time()))
        atomic_json(record_path, record)
    deadline = time.monotonic() + a.max_wait
    state = None
    while time.monotonic() < deadline:
        state, poll_request_id = safe_get(lambda: Request(f"{API}/v2/text-to-video/{job_id}",
            headers={"Authorization":f"Bearer {key}"}), deadline)
        status = state.get("status")
        if status == "failed":
            error = state.get("error") or {}; message = str(error.get("message", "")) if isinstance(error, dict) else str(error)
            record.update(status="generation_failed", error_type=error.get("type") if isinstance(error,dict) else None,
                          error_message_sha256=hashlib.sha256(message.encode()).hexdigest(), request_id=poll_request_id)
            atomic_json(record_path, record); raise RuntimeError("generation failed")
        if status == "completed": break
        if status not in ("pending","processing"): raise RuntimeError("unknown job status")
        if time.monotonic() + 5 >= deadline: break
        time.sleep(5 + random.random())
    if state is None or state.get("status") in {"pending","processing"}:
        record.update(status="polling_paused", updated_unix=int(time.time())); atomic_json(record_path, record)
        raise TimeoutError(f"poll timeout; resume job {job_id}, do not resubmit")
    video_url = state.get("result",{}).get("video_url")
    if not isinstance(video_url, str) or not video_url: raise RuntimeError("completed job omitted result URL")
    record.update(status="downloading", result_response_sha256=hashlib.sha256(canonical(state)).hexdigest(),
                  result_url_sha256=hashlib.sha256(video_url.encode()).hexdigest(), request_id=poll_request_id,
                  actual_cost_estimate_usd=str(estimate), billing_reconciliation="console_required",
                  stage_path=str(stage_path), updated_unix=int(time.time()))
    atomic_json(record_path, record)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        download_video(video_url, stage_path, set(allowed_hosts))
        artifact = inspect_mp4(stage_path, output, a.resolution, a.duration, a.fps, a.silent)
    except BaseException as exc:
        record.update(status="artifact_validation_failed", error_type=type(exc).__name__)
        atomic_json(record_path, record); raise
    record.update(status="artifact_staged", artifact_staged=artifact, updated_unix=int(time.time()))
    atomic_json(record_path, record)
    if output.exists(): raise RuntimeError("output appeared before publication")
    os.replace(stage_path, output); fsync_directory(output.parent)
    record.update(status="artifact_saved", artifact=artifact, rights_review="required", moderation_review="required",
                  creative_qa="pending", ai_disclosure="required", provenance_credentials="not_documented",
                  updated_unix=int(time.time()))
    record.pop("artifact_staged", None); atomic_json(record_path, record)
    print(json.dumps(record, indent=2)); return 0

if __name__ == "__main__": main()
```

Plan first, using the exact current result host documented for the accountâ€™s delivery path:

```bash
python ltx_hosted.py --attempt-id 7f8f06b7-9e68-4f0a-bf16-3eaf3ee9d6c4 --max-usd 0.36 --pricing-checked-at 2026-07-10T12:00:00Z --pricing-evidence-sha256 "$BILLING_SHA256" --delivery-host "$LTX_RESULT_HOST" --prompt "A single six-second chronological audiovisual shot of a red kite rising over a salt flat at dawn."
```

Execute the identical request once:

```bash
LTXV_API_KEY=... python ltx_hosted.py --execute --approval-sha256 "<exact digest>" --attempt-id 7f8f06b7-9e68-4f0a-bf16-3eaf3ee9d6c4 --max-usd 0.36 --pricing-checked-at 2026-07-10T12:00:00Z --pricing-evidence-sha256 "$BILLING_SHA256" --delivery-host "$LTX_RESULT_HOST" --prompt "A single six-second chronological audiovisual shot of a red kite rising over a salt flat at dawn."
```

`BILLING_SHA256` is the digest of the dated first-party pricing evidence actually reviewed. `LTX_RESULT_HOST` is an exact hostname authorized by the current API delivery contract, never a wildcard inferred from the returned URL. Execution rejects pricing evidence older than 24 hours. Use the unchanged arguments with `--execute --resume` only when the durable attempt record contains a job ID; `posting` or `create_outcome_unknown` must be reconciled in the developer console or with support and never replayed.

Adapt only the endpoint and payload for other operations; retain the approval, persistence, no-resubmit, polling, download, and decode guards. For HDR, download `exr_frames_url` as ZIP, reject path traversal during extraction, verify frame count/dimensions/channels, and perform explicit color management before delivery.

## Operate local/open weights separately

Use only the official `Lightricks/LTX-2` repository and `Lightricks/LTX-2.3` model repository unless the user explicitly approves a third-party runtime. Pin a reviewed Git commit and Hugging Face revision/commit. Do not use moving `main` or unpinned `huggingface-cli download` in a reproducible job.

Current official checkpoint roles, verified 2026-07-10:

- `ltx-2.3-22b-dev.safetensors` (~46.1 GB): BF16 development checkpoint; flexible and trainable; use for LoRA/fine-tuning and quality-oriented pipelines.
- `ltx-2.3-22b-distilled-1.1.safetensors` (~46.1 GB): step-distilled inference checkpoint; current 1.1 aesthetic/audio update; the official distilled pipeline uses eight first-stage and four second-stage denoising steps.
- `ltx-2.3-22b-distilled-1.0.safetensors`: older release; do not select for new work without a compatibility reason.
- Distilled LoRA 1.1 (~7.61 GB): apply to the dev checkpoint when the selected pipeline expects a distilled adapter; it is not a replacement for the base checkpoint.
- `ltx-2.3-spatial-upscaler-x2-1.1.safetensors` (~996 MB) or x1.5 (~1.09 GB): required by current two-stage implementations. The temporal x2 upscaler is described as supported/future-pipeline material, not a current universal requirement.
- Gemma 3 assets from `google/gemma-3-12b-it-qat-q4_0-unquantized`: required text encoder directory; accept Google's separate access terms and pin its revision.

The official open-source system requirements currently say NVIDIA GPU with 32 GB+ VRAM, 32 GB RAM, 100 GB free storage, CUDA 11.8+, and Python 3.10+, while the repository/model card may state newer tested versions. Treat documentation as a floor, not a guarantee. The official trainer recommends 80 GB+ VRAM for standard training and a low-VRAM INT8 configuration for 32 GB cards. Do not turn an inference minimum into a training promise.

Use a clean Linux/CUDA environment for the official trainer. Record GPU model/VRAM, driver, CUDA, PyTorch, Python, repository commit, package lock, attention backend, quantization, and offload mode. Before downloads, ensure roughly 100 GB free for one full checkpoint, Gemma assets, upscaler, environment, and outputs; larger caches or multiple variants need more.

### Choose an official pipeline

| Pipeline | Use |
|---|---|
| `TI2VidTwoStagesPipeline` | Default production T2V/I2V plus spatial upsampling |
| `TI2VidTwoStagesHQPipeline` | Quality-oriented second-order sampling |
| `TI2VidOneStagePipeline` | Fast lower-resolution prototype |
| `DistilledPipeline` | Lowest-step official path with distilled checkpoint |
| `ICLoraPipeline` | Compatible image/video transformations with an exact IC-LoRA |
| `KeyframeInterpolation` | Interpolate controlled keyframes |
| `A2VidPipelineTwoStage` | Local audio-driven video |
| `RetakePipeline` | Local audiovisual retake |
| `LipDubPipeline` | Distilled lip-dub path with its specified IC-LoRA |
| `HDRICLoraPipeline` | Video-only linear float frames for EXR/tonemapping; caller owns color pipeline |

Confirm adapter base/version compatibility. The repository contains both 2.3 22B adapters and older filenames such as `LTX-2-19b-*`; do not load a 19B LoRA into 22B 2.3 merely because the feature name matches.

### Audit, approve, then run

Perform a metadata-only plan first:

```bash
git ls-remote https://github.com/Lightricks/LTX-2.git HEAD
curl -fsS https://huggingface.co/api/models/Lightricks/LTX-2.3 > ltx-2.3-metadata.json
# Review commits, filenames, sizes, license, Gemma access, disk, and GPU before approval.
```

After explicit approval, substitute reviewed immutable revisions:

```bash
git clone https://github.com/Lightricks/LTX-2.git
cd LTX-2 && git checkout <reviewed-git-commit> && uv sync --frozen
huggingface-cli download Lightricks/LTX-2.3 \
  ltx-2.3-22b-distilled-1.1.safetensors \
  ltx-2.3-spatial-upscaler-x2-1.1.safetensors \
  --revision <reviewed-hf-commit> --local-dir ./models/ltx-2.3
huggingface-cli download google/gemma-3-12b-it-qat-q4_0-unquantized \
  --revision <reviewed-gemma-commit> --local-dir ./models/gemma-3
sha256sum models/ltx-2.3/* > models/SHA256SUMS
uv run python -m ltx_pipelines.distilled \
  --distilled-checkpoint-path models/ltx-2.3/ltx-2.3-22b-distilled-1.1.safetensors \
  --spatial-upsampler-path models/ltx-2.3/ltx-2.3-spatial-upscaler-x2-1.1.safetensors \
  --gemma-root models/gemma-3 --seed 42 --output-path output.mp4 \
  --prompt 'A single chronological audiovisual paragraph here.'
ffprobe -v error -show_streams -show_format output.mp4
ffmpeg -v error -i output.mp4 -f null -
```

Add `--quantization fp8-cast --offload cpu` only when the selected CLI supports both and after a small acceptance test. `fp8-cast` downcasts BF16 transformer linear weights during loading. `fp8-scaled-mm` is for FP8 checkpoints with TensorRT-LLM and is recommended on Hopper; it is not interchangeable with BF16 `fp8-cast`. The repository documents FlashAttention 4 only for the exact verified B200/PyTorch combination; use xFormers on other CUDA GPUs, including Hopper. Offload can reduce VRAM but increase RAM, disk I/O, and latency; some pipelines explicitly disable quantization when offload is active. Follow that pipeline's help/README, not a global assumption.

Respect latent geometry: width and height must be divisible by 32 and frame count must be `8n+1` for official local pipelines. Validate the exact CLI with `--help` at the pinned revision because flags evolve.

## License and policy gate

Do not call the model weights Apache-licensed. The official code/repository may contain components with permissive licenses, and LTX Desktop is Apache-2.0, but LTX-2 model materials use the LTX-2 Community License Agreement dated 2026-01-05.

Before local use or distribution, review the current legal text with counsel when material:

- Entities with aggregated annual revenue under USD 10M receive the community grant; the legal text requires entities at or above USD 10M to obtain a paid commercial-use license. Aggregate affiliates and entities under common control.
- â€œDerivative Modelsâ€ is broad and includes fine-tunes/adapted weights, architectural modifications, distillation, and certain models trained on outputs to perform similarly. Distribution carries license, notice, and downstream-use obligations.
- The license restricts directly competing products/services, certain output-to-model training, prohibited uses, sanctions/export violations, and non-consensual impersonation.
- Machine-generated content must carry an intelligible disclosure. Obtain consent for recognizable people and never create deceptive identity claims.
- The licensor generally claims no rights in outputs, subject to restrictions; that is not a warranty of copyright, clearance, or non-infringement.

Hosted API use is governed separately by the current API agreement and Acceptable Use Policy. Do not assume the community model license controls hosted use.

## Validate every delivery

1. Verify container decode end-to-end, duration tolerance, dimensions, frame rate, video/audio codecs, audible track presence or intentional silence, sync, and no corrupt frames.
2. Review first/middle/last frames and shot boundaries; listen to the full audio. Check identity, anatomy, lips, speech, text, temporal continuity, flicker, clipping, and abrupt ambience.
3. For conditioned work, compare first/last frames and source identity. For retake, inspect both edit seams and confirm untouched regions. For extend, inspect the join and audio continuity.
4. For HDR, verify EXR sequence integrity, linear-light interpretation, metadata, gamut, mastering/tonemap transform, and an SDR viewing transform. Never relabel an H.264 preview as HDR master.
5. Scan policy and disclosure requirements, clear people/brands/music/footage, and retain manifests without secrets or expiring signed URLs.
6. Reject or regenerate when technical or policy gates fail; do not hide failures with transcoding alone.

## Sources to re-check

- [Official LTX API documentation](https://docs.ltx.video/)
- [Supported models](https://docs.ltx.video/api-documentation/supported-models)
- [Async jobs](https://docs.ltx.video/api-documentation/async-jobs)
- [Pricing](https://docs.ltx.video/pricing)
- [Input formats](https://docs.ltx.video/api-documentation/input-formats)
- [API changelog](https://docs.ltx.video/api-changelog)
- [Official LTX-2 repository](https://github.com/Lightricks/LTX-2)
- [Official LTX-2.3 model repository](https://huggingface.co/Lightricks/LTX-2.3)
- [Official open-source system requirements](https://docs.ltx.video/open-source-model/getting-started/system-requirements)
- [LTX-2 technical report](https://arxiv.org/abs/2601.03233)
- [LTX-2 Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE)
- [LTX API License Agreement](https://static.lightricks.com/legal/ltx-2-api-license-agreement.pdf)
- [LTX Acceptable Use Policy](https://static.lightricks.com/legal/ltx-acceptable-use-policy.pdf)

Treat model menus, pricing, limits, Beta status, deprecation dates, legal terms, checkpoint names/sizes, and hardware guidance as volatile. Re-check them at execution time and record the review date.


