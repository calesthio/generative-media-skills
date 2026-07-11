---
name: minimax-hailuo-video
description: Use MiniMax's first-party Hailuo video API safely and reproducibly across global and mainland-China platforms. Covers current text-to-video, image-to-video, first/last-frame, and subject-reference models; prompt and camera craft; region/account routing; exact cost approval; asynchronous jobs and callbacks; artifact provenance; and rights, likeness, disclosure, and data-governance review. Use when designing, implementing, debugging, or evaluating direct MiniMax/Hailuo video-generation API workflows. Do not use for the consumer Hailuo site, Video Agent templates, gateways, or unrelated MiniMax modalities.
---

# MiniMax Hailuo video

Build a reviewed request, obtain exact cost approval, create at most one paid task, then preserve the result and its evidence. Treat documentation gaps as unknowns, not defaults.

## Start with the boundary

Choose one service region and keep its account, key, billing, host, and terms together:

| Region | Console/docs | API host | Billing currency |
|---|---|---|---|
| Global | `platform.minimax.io` | `https://api.minimax.io` | USD |
| Mainland China | `platform.minimaxi.com` | `https://api.minimaxi.com` | CNY |

The two platforms are separate service regions. A key or plan bought on one must not be assumed to work on the other. A `401` can be a wrong-region symptom. Use a pay-as-you-go API key for the examples below; a Token Plan/Subscription Key has separate quotas and model access.

Keep these products out of this workflow:

- `hailuoai.video` is the consumer Hailuo product with separate terms, privacy behavior, features, and commercial-use implications.
- Video Agent/template generation is a different template API. Its deprecated query endpoint and nine-hour link statement do not define general video generation.
- Image, speech, music, and text endpoints are separate modalities. General Hailuo video generation does not document an audio input, audio prompt, or generated-audio control.
- Gateways and resellers have their own schemas, retention, pricing, and support. Do not call them â€œthe MiniMax API.â€

## Route by mode before choosing a model

Current first-party general video generation uses `POST /v1/video_generation` for four modes. The API overview highlights the Hailuo 2.3 family and Hailuo-02; detailed endpoint pages also enumerate older models.

| Mode | Required media field(s) | Documented models | Documented output choices |
|---|---|---|---|
| Text-to-video (T2V) | none; `prompt` required | `MiniMax-Hailuo-2.3`, `MiniMax-Hailuo-02`; T2V endpoint also lists `T2V-01-Director`, `T2V-01` | 2.3/02: 768P at 6 or 10 s; 1080P at 6 s; 24 fps |
| Image-to-video (I2V) | `first_frame_image` | `MiniMax-Hailuo-2.3`, `MiniMax-Hailuo-2.3-Fast`, `MiniMax-Hailuo-02`; endpoint also lists `I2V-01-Director`, `I2V-01-live`, `I2V-01` | 2.3/Fast/02: 768P at 6 or 10 s; 1080P at 6 s. 02 also: 512P at 6 or 10 s; 24 fps |
| First/last frame | `first_frame_image`, `last_frame_image` | `MiniMax-Hailuo-02` | 768P at 6 or 10 s; 1080P at 6 s; 24 fps. The endpoint explicitly says 512P is unsupported |
| Subject reference | `subject_reference` array | `S2V-01` | **Unknown:** its endpoint omits duration, resolution, and current price; the general guide example nevertheless sends 6 s and 1080P |

`MiniMax-Hailuo-2.3-Fast` is I2V-only. Do not select it for T2V. Detailed pages describe older `*-01*` models as 720P/6 s, but current pay-as-you-go pricing omits them; verify availability and price in the correct console before any paid use. Do the same for `S2V-01` rather than borrowing another model's price.

Current pay-as-you-go prices, checked 2026-07-10:

| Combination | Global | Mainland China |
|---|---:|---:|
| 2.3-Fast, 768P, 6 s | $0.19 | Â¥1.35 |
| 2.3-Fast, 768P, 10 s | $0.32 | Â¥2.25 |
| 2.3-Fast, 1080P, 6 s | $0.33 | Â¥2.31 |
| 2.3 or 02, 768P, 6 s | $0.28 | Â¥2.00 |
| 2.3 or 02, 768P, 10 s | $0.56 | Â¥4.00 |
| 2.3 or 02, 1080P, 6 s | $0.49 | Â¥3.50 |
| 02 I2V, 512P, 6 s | $0.10 | Â¥0.60 |
| 02 I2V, 512P, 10 s | $0.15 | Â¥1.00 |

These are per generated video, not timeless constants. Recheck the region's official pricing page immediately before approval. Packages deduct units and raise RPM; Token Plans use plan quotas. Never turn a package's blended cost or another region's currency into a pay-as-you-go quote.

## Build a request dossier

Before calling create, record:

- region, console/account identifier, key type, model, mode, resolution, duration, variant count, currency, unit price, and pricing-page retrieval time;
- exact prompt, `prompt_optimizer`, `fast_pretreatment`, and every non-default parameter;
- source file SHA-256, MIME type, byte length, dimensions, aspect ratio, provenance, license/consent, and any face/identity present;
- intended audience, jurisdiction, AI disclosure/watermark plan, retention class, and reviewer;
- an attempt ID generated locally before the POST.

For first/last-frame and I2V inputs, official constraints are JPG/JPEG, PNG, or WebP; under 20 MB; short edge over 300 px; aspect ratio from 2:5 through 5:2; public URL or Base64 data URL. The first image determines output aspect/resolution. In first/last mode, a differently sized last image is cropped to match the first. Pre-align composition, subject scale, lighting, and topology to avoid an implausible transition.

The S2V reference documents a different exact shape: `"subject_reference": [{"type": "character", "image": ["https://authorized.example/reference.jpg"]}]`. `type` is `character`; `image` is an array containing the authorized face-reference URL. Do not transpose I2V fields or assume I2V's media transport rules where the S2V page is silent.

A public source URL lets MiniMax fetch that asset and may expose it through URL logs or access controls. Prefer an appropriately scoped URL or bounded Base64 only when policy allows. Never accept arbitrary user URLs into your own downloader without SSRF controls. Hash the original asset; do not log Base64 bodies or signed download URLs.

## Write prompts for this motion system

The prompt limit is 2,000 characters. Hailuo supports explicit camera commands on the documented 2.3, 02, and Director workflows:

`[Truck left]`, `[Truck right]`, `[Pan left]`, `[Pan right]`, `[Push in]`, `[Pull out]`, `[Pedestal up]`, `[Pedestal down]`, `[Tilt up]`, `[Tilt down]`, `[Zoom in]`, `[Zoom out]`, `[Shake]`, `[Tracking shot]`, `[Static shot]`.

Commands in one bracket happen together; official guidance recommends at most three combined commands. Commands placed sequentially express a sequence. They are directional controls, not frame-accurate timecodes.

Use this compact prompt order:

1. Establish subject and initial composition.
2. Describe one physically coherent action arc.
3. State the dominant camera command or simple sequence.
4. Specify a visible end state and stable details that must persist.

For I2V, describe change from the supplied frame instead of contradicting its static appearance. For first/last-frame generation, describe a plausible bridge between the two known states. For a designed shot, set `prompt_optimizer: false`; otherwise the optimizer may rewrite wording or camera intent. `prompt_optimizer` defaults to `true`. `fast_pretreatment` defaults to `false`, requires the optimizer, and is documented for current Hailuo I2V models.

The following are craft heuristics, not API guarantees: one primary action and one dominant camera move usually fit a 6â€“10 second clip better than dense choreography; explicit end-state language improves reviewability; generated physics, faces, text, hands, occlusion, and identity should still be inspected frame by frame. MiniMax's claims about improved motion, expression, realism, and adherence are provider claims, not independent benchmark findings.

The general endpoint documents no seed, negative prompt, arbitrary aspect-ratio parameter, audio input, audio prompt, or audio-output switch. Do not invent them. Treat the presence and nature of an output audio track as unknown until the actual file is inspected; add separately licensed sound downstream when required.

Across the mode-specific references, `model` is required; T2V requires `prompt`, while I2V and first/last describe the text prompt as optional; prompts may be at most 2,000 characters. `first_frame_image`, `last_frame_image`, and `subject_reference` are required only by their respective modes. `callback_url` is optional. `duration` and `resolution` must follow the model/mode matrix above rather than generic CLI defaults. The current mainland-China T2V page additionally exposes `aigc_watermark` as a boolean defaulting to `false`; the current global T2V page does not.

## Make the paid boundary explicit

Default to dry-run. Show the redacted request, exact one-video cost, variant multiplier, currency, authoritative pricing timestamp/evidence digest, source hashes, local job key, output destination, and exact-host download policy. Canonically hash that complete envelope. Require a human to approve the digest and a finite positive maximum in the same currency; amount-only approval is insufficient because it does not bind the model, prompt, source, region, or custody policy. If the combination has no current published price, stop with `UNKNOWN` and send the operator to the correct console or MiniMax support.

Before POSTing, acquire the job ledger with exclusive-create semantics and persist an `intent-recorded` entry. After a response, persist only an allowlisted result summaryâ€”task ID, provider code, status-message/body digests, and timestampsâ€”not raw prompts, Base64, error bodies, or signed URLs. MiniMax documents no idempotency key for video creation. Therefore:

- Retry authenticated GET/poll/download operations with bounded backoff.
- Do not automatically retry a create POST.
- If create times out or the connection breaks before a `task_id` is captured, mark it `create-outcome-unknown`. Reconcile billing/console/support before authorizing a replacement task.
- Treat a 5xx, provider timeout/internal code, malformed envelope, or nominal success with an unusable task ID as equally ambiguous and persist that state before stopping.
- A replay is a new potentially billable video unless the earlier create is conclusively known not to exist.

HTTP success alone is not provider success. Require `base_resp.status_code == 0` and a nonempty `task_id`. Preserve `base_resp.status_code` and `status_msg` for diagnosis. Common codes include 1001 timeout, 1002 rate limit, 1004 authentication, 1008 insufficient balance, 1026 input sensitive, 1027 output sensitive, 2013 invalid parameters, 2049 invalid key, and 2056 usage limit. Never evade a content-safety response.

The published default global video limit is currently 5 requests/minute across the Hailuo 2.3 and 02 series; packages publish higher limits. Treat this as account/plan-specific and recheck the console. Pace polls separately; the guide recommends a 10-second interval.

Check <https://status.minimax.io/> during incidents, but do not infer healthy video generation merely from another listed component's status if video is not shown separately.

## Complete dry-run-first client

This Python 3.11+ client covers currently priced T2V, I2V, and first/last-frame combinations in both regions. It does not execute `S2V-01` or unpriced legacy models. It never retries create, acquires an exclusive attempt ledger before create, resumes known task IDs, checks MiniMax's envelope, polls every 10 seconds, downloads with an exact-host/public-DNS policy and no bearer token, and crash-resumably validates MP4 with `ffprobe` plus a full `ffmpeg` decode. Save it as `hailuo_generate.py` outside the skill directory. Python 3.11+, `ffprobe`, and `ffmpeg` are required.

```python
#!/usr/bin/env python3
import argparse, base64, hashlib, http.client, ipaddress, json, os, pathlib, random, socket, ssl, subprocess, sys, tempfile, threading, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

HOSTS = {"global": "https://api.minimax.io", "cn": "https://api.minimaxi.com"}
PRICES = {
    "global": {"currency": "USD", "table": {
        ("MiniMax-Hailuo-2.3-Fast", "768P", 6): "0.19", ("MiniMax-Hailuo-2.3-Fast", "768P", 10): "0.32",
        ("MiniMax-Hailuo-2.3-Fast", "1080P", 6): "0.33", ("MiniMax-Hailuo-2.3", "768P", 6): "0.28",
        ("MiniMax-Hailuo-2.3", "768P", 10): "0.56", ("MiniMax-Hailuo-2.3", "1080P", 6): "0.49",
        ("MiniMax-Hailuo-02", "512P", 6): "0.10", ("MiniMax-Hailuo-02", "512P", 10): "0.15",
        ("MiniMax-Hailuo-02", "768P", 6): "0.28", ("MiniMax-Hailuo-02", "768P", 10): "0.56",
        ("MiniMax-Hailuo-02", "1080P", 6): "0.49"}},
    "cn": {"currency": "CNY", "table": {
        ("MiniMax-Hailuo-2.3-Fast", "768P", 6): "1.35", ("MiniMax-Hailuo-2.3-Fast", "768P", 10): "2.25",
        ("MiniMax-Hailuo-2.3-Fast", "1080P", 6): "2.31", ("MiniMax-Hailuo-2.3", "768P", 6): "2.00",
        ("MiniMax-Hailuo-2.3", "768P", 10): "4.00", ("MiniMax-Hailuo-2.3", "1080P", 6): "3.50",
        ("MiniMax-Hailuo-02", "512P", 6): "0.60", ("MiniMax-Hailuo-02", "512P", 10): "1.00",
        ("MiniMax-Hailuo-02", "768P", 6): "2.00", ("MiniMax-Hailuo-02", "768P", 10): "4.00",
        ("MiniMax-Hailuo-02", "1080P", 6): "3.50"}}
}
MODELS = {
    "text": {"MiniMax-Hailuo-2.3", "MiniMax-Hailuo-02"},
    "image": {"MiniMax-Hailuo-2.3", "MiniMax-Hailuo-2.3-Fast", "MiniMax-Hailuo-02"},
    "first-last": {"MiniMax-Hailuo-02"},
}
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
MAX_JSON = 256 * 1024
MAX_VIDEO = 250 * 1024 * 1024
MAX_TOOL_OUTPUT = 512 * 1024
NONTERMINAL = {"Preparing", "Queueing", "Processing"}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None

NO_REDIRECT = urllib.request.build_opener(NoRedirect)

class APIProblem(Exception):
    def __init__(self, kind, http_status=None, body_sha256=None):
        super().__init__(kind); self.kind = kind; self.http_status = http_status; self.body_sha256 = body_sha256

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256_bytes(value): return hashlib.sha256(value).hexdigest()
def utc_now(): return datetime.now(timezone.utc).isoformat()

def fsync_directory(path):
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)

def image_dimensions(data, suffix):
    if suffix == ".png" and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if suffix in {".jpg", ".jpeg"} and data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xff: i += 1; continue
            marker = data[i + 1]; i += 2
            if marker in {0xd8, 0xd9} or 0xd0 <= marker <= 0xd7: continue
            if i + 2 > len(data): break
            length = int.from_bytes(data[i:i + 2], "big")
            if marker in {0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf}:
                return int.from_bytes(data[i + 5:i + 7], "big"), int.from_bytes(data[i + 3:i + 5], "big")
            if length < 2: break
            i += length
    if suffix == ".webp" and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        kind = data[12:16]
        if kind == b"VP8X" and len(data) >= 30:
            return 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
        if kind == b"VP8L" and len(data) >= 25 and data[20] == 0x2f:
            b0, b1, b2, b3 = data[21:25]
            return 1 + b0 + ((b1 & 0x3f) << 8), 1 + (b1 >> 6) + (b2 << 2) + ((b3 & 0x0f) << 10)
        if kind == b"VP8 " and len(data) >= 30 and data[23:26] == b"\x9d\x01\x2a":
            return int.from_bytes(data[26:28], "little") & 0x3fff, int.from_bytes(data[28:30], "little") & 0x3fff
    raise SystemExit("Image signature or dimensions are invalid/unsupported")

def atomic_json(path, value):
    path = pathlib.Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".hailuo-", suffix=".json", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as out:
            out.write(canonical(value) + b"\n"); out.flush(); os.fsync(out.fileno())
        os.replace(name, path); fsync_directory(path.parent)
    finally:
        if os.path.exists(name): os.unlink(name)

def exclusive_json(path, value):
    path = pathlib.Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "wb") as out:
        out.write(canonical(value) + b"\n"); out.flush(); os.fsync(out.fileno())
    fsync_directory(path.parent)

def read_json(path):
    raw = pathlib.Path(path).read_bytes()
    if len(raw) > MAX_JSON: raise SystemExit("Ledger exceeds JSON cap")
    value = json.loads(raw)
    if not isinstance(value, dict): raise SystemExit("Ledger is not an object")
    return value

def bounded_process(argv, timeout, cap=MAX_TOOL_OUTPUT):
    process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chunks, total, overflow, lock = [], [0], threading.Event(), threading.Lock()
    def drain(stream):
        while True:
            data = stream.read(65536)
            if not data: return
            with lock:
                total[0] += len(data)
                if total[0] > cap:
                    overflow.set(); process.kill(); return
                chunks.append(data)
    threads = [threading.Thread(target=drain, args=(stream,), daemon=True) for stream in (process.stdout, process.stderr)]
    for thread in threads: thread.start()
    try: code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill(); process.wait(); raise RuntimeError(f"tool timeout: {pathlib.Path(argv[0]).name}")
    for thread in threads: thread.join(timeout=2)
    output = b"".join(chunks)
    if overflow.is_set(): raise RuntimeError(f"tool output cap exceeded: {pathlib.Path(argv[0]).name}")
    if code: raise RuntimeError(f"tool failed: {pathlib.Path(argv[0]).name}; diagnostics_sha256={sha256_bytes(output)}")
    return output

def media(path_text):
    path = pathlib.Path(path_text)
    if not path.is_file() or path.suffix.lower() not in MIME or path.stat().st_size >= 20 * 1024 * 1024:
        raise SystemExit("Image must be JPG/JPEG, PNG, or WebP and strictly under 20 MB")
    data = path.read_bytes()
    width, height = image_dimensions(data, path.suffix.lower())
    ratio = width / height
    if min(width, height) <= 300 or not 0.4 <= ratio <= 2.5:
        raise SystemExit("Image short edge must exceed 300 px and aspect ratio must be within 2:5â€“5:2")
    bounded_process(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "null", "-"], 60)
    return {
        "wire": f"data:{MIME[path.suffix.lower()]};base64,{base64.b64encode(data).decode('ascii')}",
        "evidence": {"path": str(path.resolve()), "sha256": hashlib.sha256(data).hexdigest(),
                     "bytes": len(data), "mime": MIME[path.suffix.lower()],
                     "width": width, "height": height, "aspect_ratio": ratio}
    }

def api_json(method, url, key, body=None, retries=0):
    encoded = None if body is None else canonical(body)
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=encoded, method=method,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "Accept": "application/json"})
        try:
            with NO_REDIRECT.open(req, timeout=40) as response:
                raw = response.read(MAX_JSON + 1)
            if len(raw) > MAX_JSON: raise APIProblem("response-too-large")
            try: result = json.loads(raw)
            except json.JSONDecodeError: raise APIProblem("invalid-json", response.status, sha256_bytes(raw))
            if not isinstance(result, dict): raise APIProblem("non-object-json", response.status, sha256_bytes(raw))
            return result
        except urllib.error.HTTPError as exc:
            raw = exc.read(MAX_JSON + 1)
            problem = APIProblem("http-error", exc.code, sha256_bytes(raw))
            if attempt == retries or exc.code not in {408, 429, 500, 502, 503, 504}: raise problem
        except APIProblem: raise
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempt == retries: raise APIProblem("transport-" + type(exc).__name__)
        time.sleep(min(8, 2 ** attempt) * (1 + random.random() * 0.25))
    raise AssertionError("unreachable")

def provider_result(result):
    base = result.get("base_resp")
    if not isinstance(base, dict) or not isinstance(base.get("status_code"), int):
        raise APIProblem("missing-provider-envelope", body_sha256=sha256_bytes(canonical(result)))
    return base["status_code"], sha256_bytes(str(base.get("status_msg", "")).encode("utf-8"))

def exact_hosts(raw):
    hosts = []
    for item in raw.split(","):
        host = item.strip().rstrip(".").lower()
        if not host: continue
        if "*" in host or "/" in host or ":" in host: raise SystemExit("Output hosts must be exact DNS names")
        try: ipaddress.ip_address(host)
        except ValueError: pass
        else: raise SystemExit("Output host policy rejects IP literals")
        hosts.append(host)
    if not hosts: raise SystemExit("Provide at least one reviewed exact --output-host")
    return tuple(sorted(set(hosts)))

def validate_output_url(url, allowed_hosts):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        raise RuntimeError("Output URL must be HTTPS with hostname, no userinfo, and no fragment")
    if parsed.port not in (None, 443): raise RuntimeError("Output URL must use default HTTPS port")
    host = parsed.hostname.rstrip(".").lower()
    try: ipaddress.ip_address(host)
    except ValueError: pass
    else: raise RuntimeError("Output URL rejects IP literals")
    if host not in allowed_hosts: raise RuntimeError("Output host is outside the approved exact-host policy")
    addresses = []
    for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        address = ipaddress.ip_address(item[4][0])
        if not address.is_global: raise RuntimeError("Output host resolves to a non-public address")
        addresses.append(str(address))
    if not addresses: raise RuntimeError("Output host did not resolve")
    target = parsed.path or "/"
    if parsed.query: target += "?" + parsed.query
    return host, target, sorted(set(addresses))

class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, address, timeout):
        super().__init__(host, 443, timeout=timeout, context=ssl.create_default_context()); self.address = address
    def connect(self):
        raw = socket.create_connection((self.address, 443), self.timeout)
        try: self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except Exception: raw.close(); raise

def verify_mp4(path):
    path = pathlib.Path(path); size = path.stat().st_size
    if size <= 0 or size > MAX_VIDEO: raise RuntimeError("Artifact size is outside policy")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        header = stream.read(32)
        if len(header) < 12 or header[4:8] != b"ftyp": raise RuntimeError("Artifact lacks ISO-BMFF ftyp signature")
        stream.seek(0)
        for chunk in iter(lambda: stream.read(1024 * 1024), b""): digest.update(chunk)
    raw = bounded_process(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], 30, MAX_JSON)
    metadata = json.loads(raw); streams = metadata.get("streams", [])
    video = next((item for item in streams if item.get("codec_type") == "video"), None)
    if not video: raise RuntimeError("Artifact has no video stream")
    bounded_process(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "null", "-"], 300)
    return {"bytes": size, "sha256": digest.hexdigest(), "qa": {
        "container": metadata.get("format", {}).get("format_name"), "video_codec": video.get("codec_name"),
        "width": video.get("width"), "height": video.get("height"), "fps": video.get("avg_frame_rate"),
        "duration": metadata.get("format", {}).get("duration"),
        "audio_present": any(item.get("codec_type") == "audio" for item in streams), "full_decode": "passed"}}

def safe_download(url, destination, allowed_hosts, ledger_path, record):
    destination = pathlib.Path(destination); destination.parent.mkdir(parents=True, exist_ok=True)
    stage = destination.with_name("." + destination.name + ".hailuo-stage")
    expected = record.get("artifact_staged") or record.get("artifact")
    if destination.exists():
        if not isinstance(expected, dict): raise RuntimeError("Existing artifact has no durable expected digest")
        artifact = verify_mp4(destination)
        if (artifact["sha256"], artifact["bytes"]) != (expected.get("sha256"), expected.get("bytes")):
            raise RuntimeError("Existing artifact does not match durable evidence")
        return artifact
    if stage.exists() and isinstance(expected, dict):
        artifact = verify_mp4(stage)
        if (artifact["sha256"], artifact["bytes"]) != (expected.get("sha256"), expected.get("bytes")):
            raise RuntimeError("Staged artifact does not match durable evidence")
        os.replace(stage, destination); fsync_directory(destination.parent); return artifact
    host, target, addresses = validate_output_url(url, allowed_hosts)
    url_hash = sha256_bytes(url.encode("utf-8"))
    if record.get("download_url_sha256") not in (None, url_hash): raise RuntimeError("Download URL changed during an incomplete transfer")
    record.update(state="downloading", download_url_sha256=url_hash, download_host=host, download_started_at=record.get("download_started_at") or utc_now())
    atomic_json(ledger_path, record)
    if stage.exists(): stage.unlink()
    connection = PinnedHTTPSConnection(host, addresses[0], timeout=90)
    try:
        connection.request("GET", target, headers={"Host": host, "Accept": "video/mp4", "User-Agent": "hailuo-artifact-client/2"})
        response = connection.getresponse()
        if response.status != 200: raise RuntimeError(f"Output returned HTTP {response.status}")
        media_type = response.getheader("Content-Type", "").split(";", 1)[0].lower()
        if media_type not in {"video/mp4", "application/octet-stream"}: raise RuntimeError("Unexpected output media type")
        announced = response.getheader("Content-Length")
        if announced is not None and (not announced.isdigit() or int(announced) > MAX_VIDEO): raise RuntimeError("Invalid or excessive Content-Length")
        fd = os.open(stage, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600); total = 0
        try:
            with os.fdopen(fd, "wb") as out:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk: break
                    total += len(chunk)
                    if total > MAX_VIDEO: raise RuntimeError("Download exceeded byte cap")
                    out.write(chunk)
                out.flush(); os.fsync(out.fileno())
        except BaseException:
            stage.unlink(missing_ok=True); raise
    finally: connection.close()
    artifact = verify_mp4(stage)
    record.update(state="artifact-staged", artifact_staged=artifact, artifact_validated_at=utc_now())
    atomic_json(ledger_path, record)
    os.replace(stage, destination); fsync_directory(destination.parent)
    return artifact

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--region", choices=HOSTS, required=True)
    p.add_argument("--mode", choices=MODELS, required=True)
    p.add_argument("--model", required=True); p.add_argument("--prompt", required=True)
    p.add_argument("--resolution", choices=["512P", "768P", "1080P"], required=True)
    p.add_argument("--duration", type=int, choices=[6, 10], required=True)
    p.add_argument("--first-frame"); p.add_argument("--last-frame")
    p.add_argument("--optimizer", action=argparse.BooleanOptionalAction, default=False)
    p.add_argument("--fast-pretreatment", action="store_true")
    p.add_argument("--execute", action="store_true")
    p.add_argument("--job-key", required=True)
    p.add_argument("--output-host", required=True, help="Comma-separated reviewed exact DNS hostnames")
    p.add_argument("--pricing-checked-at", required=True, help="Timezone-aware ISO-8601 time of the live regional price check")
    p.add_argument("--pricing-evidence-sha256", required=True)
    p.add_argument("--rights-sha256", required=True); p.add_argument("--moderation-sha256", required=True)
    p.add_argument("--qa-plan-sha256", required=True)
    p.add_argument("--approval-sha256")
    p.add_argument("--max-cost"); p.add_argument("--max-cost-currency", choices=["USD", "CNY"])
    p.add_argument("--show-full-plan", action="store_true")
    p.add_argument("--ledger", default="hailuo-attempt.json")
    p.add_argument("--output", default="hailuo-output.mp4")
    a = p.parse_args()
    if not a.job_key or any(not (character.isalnum() or character in "-_") for character in a.job_key):
        raise SystemExit("job-key accepts letters, digits, hyphen, and underscore")
    if a.model not in MODELS[a.mode]: raise SystemExit("Model is not valid for the selected mode")
    if len(a.prompt) > 2000: raise SystemExit("Prompt exceeds 2,000 characters")
    if a.fast_pretreatment and not a.optimizer: raise SystemExit("fast_pretreatment requires optimizer")
    if a.mode in {"image", "first-last"} and not a.first_frame: raise SystemExit("First frame required")
    if a.mode == "first-last" and not a.last_frame: raise SystemExit("Last frame required")
    key = (a.model, a.resolution, a.duration)
    unit = PRICES[a.region]["table"].get(key)
    if unit is None: raise SystemExit("UNKNOWN current price/combination; verify in the correct MiniMax console")
    if a.model == "MiniMax-Hailuo-02" and a.mode == "text" and a.resolution == "512P":
        raise SystemExit("512P pricing/availability is documented for Hailuo-02 I2V, not T2V")
    if a.mode == "first-last" and a.resolution == "512P":
        raise SystemExit("The first/last-frame endpoint explicitly does not support 512P")
    request = {"model": a.model, "prompt": a.prompt, "resolution": a.resolution,
               "duration": a.duration, "prompt_optimizer": a.optimizer}
    evidence = {}
    if a.mode in {"image", "first-last"}:
        item = media(a.first_frame); request["first_frame_image"] = item["wire"]; evidence["first_frame"] = item["evidence"]
    if a.mode == "first-last":
        item = media(a.last_frame); request["last_frame_image"] = item["wire"]; evidence["last_frame"] = item["evidence"]
    if a.fast_pretreatment: request["fast_pretreatment"] = True
    currency = PRICES[a.region]["currency"]
    output_hosts = exact_hosts(a.output_host)
    for name, value in (("pricing evidence", a.pricing_evidence_sha256), ("rights", a.rights_sha256),
                        ("moderation", a.moderation_sha256), ("QA plan", a.qa_plan_sha256)):
        if len(value) != 64 or any(character not in "0123456789abcdefABCDEF" for character in value):
            raise SystemExit(f"{name} must be a SHA-256 digest")
    redacted = dict(request)
    for field in ("first_frame_image", "last_frame_image"):
        if field in redacted: redacted[field] = f"<base64 redacted; sha256={evidence[field.split('_image')[0]].get('sha256', 'see evidence')}>"
    redacted["prompt"] = "sha256:" + sha256_bytes(a.prompt.encode("utf-8"))
    request_hash = sha256_bytes(canonical(request))
    output_policy = {"exact_hosts": list(output_hosts), "https": True, "redirects": "reject",
                     "reject_ip_literals": True, "public_dns": True,
                     "dns_pinning": "connect-IP-with-TLS-SNI-and-host-certificate",
                     "max_bytes": MAX_VIDEO, "container": "mp4", "full_decode": True}
    envelope = {"schema_version": 1, "job_key": a.job_key, "region": a.region, "api_origin": HOSTS[a.region],
                "endpoint": "/v1/video_generation", "mode": a.mode, "model": a.model,
                "request_sha256": request_hash, "redacted_request": redacted, "source_evidence": evidence,
                "output": str(pathlib.Path(a.output).resolve()), "output_policy": output_policy,
                "price": {"amount": unit, "currency": currency, "checked_at": a.pricing_checked_at,
                          "evidence_sha256": a.pricing_evidence_sha256.lower()},
                "governance": {"rights_sha256": a.rights_sha256.lower(),
                               "moderation_sha256": a.moderation_sha256.lower(),
                               "qa_plan_sha256": a.qa_plan_sha256.lower()}}
    approval = sha256_bytes(canonical(envelope))
    print(json.dumps({"approval_sha256": approval, "plan": envelope}, indent=2, ensure_ascii=False))
    if a.show_full_plan: print(json.dumps({"protected_payload": request}, indent=2, ensure_ascii=False))
    print(f"DRY RUN: one task, exact maximum {currency} {unit}; no network request sent", file=sys.stderr)
    if not a.execute: return
    if a.approval_sha256 != approval: raise SystemExit("Exact approval digest mismatch")
    try: maximum = Decimal(a.max_cost or "")
    except InvalidOperation: raise SystemExit("max-cost must be a decimal")
    if not maximum.is_finite() or maximum <= 0 or maximum < Decimal(unit):
        raise SystemExit("max-cost must be finite, positive, and at least the quoted amount")
    if a.max_cost_currency != currency: raise SystemExit("max-cost currency does not match the selected region")
    try: checked_at = datetime.fromisoformat(a.pricing_checked_at.replace("Z", "+00:00"))
    except ValueError: raise SystemExit("pricing-checked-at must be ISO-8601")
    if checked_at.tzinfo is None: raise SystemExit("pricing-checked-at must include a timezone")
    age = datetime.now(timezone.utc) - checked_at.astimezone(timezone.utc)
    if age.total_seconds() < -300 or age.total_seconds() > 86400:
        raise SystemExit("Live regional pricing evidence must be no more than 24 hours old")
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key: raise SystemExit("Set MINIMAX_API_KEY only in the environment")
    ledger_path = pathlib.Path(a.ledger)
    if ledger_path.exists():
        intent = read_json(ledger_path)
        if intent.get("request_sha256") != request_hash or intent.get("approval_sha256") != approval:
            raise SystemExit("Existing job ledger belongs to a different approved request")
        task_id = intent.get("task_id")
        if not task_id: raise SystemExit(f"Ledger state {intent.get('state')!r} has no task ID; never replay this job key")
    else:
        intent = {"schema_version": 1, "state": "intent-recorded", "created_at": utc_now(),
                  "job_key": a.job_key, "request_sha256": request_hash, "approval_sha256": approval,
                  "region": a.region, "host": HOSTS[a.region], "mode": a.mode, "model": a.model,
                  "redacted_request": redacted, "source_evidence": evidence, "output_policy": output_policy,
                  "price": envelope["price"], "governance": envelope["governance"]}
        try: exclusive_json(ledger_path, intent)
        except FileExistsError: raise SystemExit("Another process acquired this job ledger")
        intent.update(state="create-started", create_started_at=utc_now()); atomic_json(ledger_path, intent)
        try: created = api_json("POST", HOSTS[a.region] + "/v1/video_generation", api_key, request, retries=0)
        except APIProblem as exc:
            intent.update(state="create-outcome-unknown", create_outcome_at=utc_now(), error_kind=exc.kind,
                          http_status=exc.http_status, error_body_sha256=exc.body_sha256, replay_allowed=False)
            atomic_json(ledger_path, intent)
            raise SystemExit("Create outcome unknown; do not replay until billing/console/support is reconciled")
        try: provider_code, provider_message_sha256 = provider_result(created)
        except APIProblem as exc:
            intent.update(state="create-outcome-unknown", create_outcome_at=utc_now(), error_kind=exc.kind,
                          response_sha256=exc.body_sha256, replay_allowed=False); atomic_json(ledger_path, intent)
            raise SystemExit("Create success envelope is unusable; do not replay")
        if provider_code != 0:
            uncertain = provider_code in {1001, 1024, 1033}
            intent.update(state="create-outcome-unknown" if uncertain else "create-rejected",
                          create_outcome_at=utc_now(), provider_status_code=provider_code,
                          provider_status_message_sha256=provider_message_sha256, replay_allowed=False)
            atomic_json(ledger_path, intent)
            raise SystemExit("MiniMax rejected or could not confirm create; this job key cannot be replayed")
        task_id = created.get("task_id")
        if not isinstance(task_id, (str, int)) or not str(task_id).isdigit():
            intent.update(state="create-outcome-unknown", create_outcome_at=utc_now(),
                          error_kind="unusable-success-task-id", response_sha256=sha256_bytes(canonical(created)),
                          replay_allowed=False); atomic_json(ledger_path, intent)
            raise SystemExit("Create returned an unusable task ID; do not replay")
        task_id = str(task_id)
        intent.update(state="task-created", task_id=task_id, submitted_at=utc_now(),
                      provider_status_code=0, provider_status_message_sha256=provider_message_sha256)
        atomic_json(ledger_path, intent)
    deadline = time.monotonic() + 30 * 60
    while time.monotonic() < deadline:
        query = HOSTS[a.region] + "/v1/query/video_generation?" + urllib.parse.urlencode({"task_id": task_id})
        try: status = api_json("GET", query, api_key, retries=3)
        except APIProblem as exc:
            intent.update(poll_error_kind=exc.kind, poll_http_status=exc.http_status,
                          poll_error_body_sha256=exc.body_sha256); atomic_json(ledger_path, intent); raise SystemExit("Polling failed; resume this task ID later")
        provider_code, provider_message_sha256 = provider_result(status)
        if provider_code != 0:
            intent.update(poll_provider_status_code=provider_code,
                          poll_provider_status_message_sha256=provider_message_sha256); atomic_json(ledger_path, intent)
            raise SystemExit("MiniMax query returned a provider error; resume after diagnosis")
        if status.get("task_id") not in (None, task_id, int(task_id)):
            raise SystemExit("Query task ID mismatch")
        name = status.get("status")
        intent.update(state="polling", last_status=name, last_polled_at=utc_now()); atomic_json(ledger_path, intent)
        if name == "Success":
            file_id = status.get("file_id")
            if not isinstance(file_id, (str, int)) or not str(file_id).isdigit(): raise RuntimeError("Success returned invalid file_id")
            file_id = str(file_id)
            retrieve = HOSTS[a.region] + "/v1/files/retrieve?" + urllib.parse.urlencode({"file_id": file_id})
            retrieved = api_json("GET", retrieve, api_key, retries=3)
            retrieve_code, retrieve_message_sha256 = provider_result(retrieved)
            if retrieve_code != 0: raise RuntimeError("MiniMax retrieve returned a provider error")
            file_record = retrieved.get("file") or {}
            if str(file_record.get("file_id")) not in {"None", file_id}: raise RuntimeError("Retrieve file ID mismatch")
            url = file_record.get("download_url") or retrieved.get("download_url")
            if not url: raise RuntimeError("Retrieve returned no download_url")
            artifact = safe_download(url, a.output, set(output_hosts), ledger_path, intent)
            expected_dimensions = (status.get("video_width"), status.get("video_height"))
            actual_dimensions = (artifact["qa"].get("width"), artifact["qa"].get("height"))
            try: actual_duration = Decimal(str(artifact["qa"].get("duration")))
            except InvalidOperation: actual_duration = Decimal("NaN")
            qa_state = "automated-passed"
            if expected_dimensions != actual_dimensions or not actual_duration.is_finite() or abs(actual_duration - Decimal(a.duration)) > Decimal("1"):
                qa_state = "quarantined-metadata-mismatch"
            intent.update(state="artifact-downloaded" if qa_state == "automated-passed" else "artifact-quarantined",
                          file_id=file_id, retrieve_provider_message_sha256=retrieve_message_sha256,
                          artifact=dict(artifact, path=str(pathlib.Path(a.output).resolve())),
                          expected_dimensions={"width": expected_dimensions[0], "height": expected_dimensions[1]},
                          qa_state=qa_state, human_review="pending", stored_at=utc_now())
            atomic_json(ledger_path, intent); print(json.dumps({"artifact": intent["artifact"], "qa_state": qa_state}, indent=2)); return
        if name == "Fail":
            intent.update(state="generation-failed", terminal_at=utc_now(),
                          failure_sha256=sha256_bytes(str(status.get("error_message", "")).encode("utf-8")))
            atomic_json(ledger_path, intent); raise SystemExit("MiniMax generation failed")
        if name not in NONTERMINAL: raise RuntimeError("Unknown task status; fail closed")
        time.sleep(10)
    intent.update(state="poll-deadline-reached", deadline_at=utc_now()); atomic_json(ledger_path, intent)
    raise SystemExit("Polling deadline reached; task may still be runningâ€”resume query, do not recreate")

if __name__ == "__main__": main()
```

Dry-run a global 6-second 768P T2V request without a key or network call. First re-open the global pay-as-you-go page, record the current timezone-aware check time, hash a protected capture of that evidence, and provide the protected rights/moderation/QA evidence digests. The output host must be an exact reviewed CDN hostname learned from a non-sensitive staging workflow or provider confirmation; do not use a wildcard:

```bash
python hailuo_generate.py --region global --mode text --model MiniMax-Hailuo-2.3 --resolution 768P --duration 6 --job-key kite-v1 --output-host '<reviewed-exact-download-host>' --pricing-checked-at '2026-07-10T12:00:00Z' --pricing-evidence-sha256 '<64-hex-digest>' --rights-sha256 '<64-hex-digest>' --moderation-sha256 '<64-hex-digest>' --qa-plan-sha256 '<64-hex-digest>' --prompt "A red paper kite rises above a quiet salt flat. [Tracking shot] The camera follows low and steady; the kite settles centered against the horizon."
```

After reviewing the protected payload and unchanged dossier, repeat the same arguments and add the printed digest, currency-matched ceiling, and explicit execute gate:

```bash
export MINIMAX_API_KEY='replace-in-your-shell-only'
python hailuo_generate.py <the-exact-unchanged-dry-run-arguments> --execute --approval-sha256 '<printed-digest>' --max-cost 0.28 --max-cost-currency USD
```

For PowerShell, set the key with `$env:MINIMAX_API_KEY = '...'`. Do not paste a real key into scripts, notebooks, logs, chat, browser code, or version control. The client deliberately does not add China's `aigc_watermark` field: current China T2V documentation exposes it, while current global documentation does not. If using it on the China route, add it only after verifying the exact mode's current China reference; it does not replace jurisdiction-specific public disclosure.

## Finish the asynchronous lifecycle

Polling states are case-sensitive: `Preparing`, `Queueing`, `Processing`, `Success`, `Fail`. On success, obtain `file_id`, call `GET /v1/files/retrieve?file_id=...`, and download immediately. Current general file docs do not state a download-URL lifetime or a generated-file retention period. A historical page and the separate template API mention nine hours; that is not a current general-video guarantee.

Treat the authenticated retrieve response's signed URL as untrusted. Download without the bearer token; require HTTPS, no userinfo/fragment, default port, an approved exact hostname, all-public DNS, IP-literal rejection, DNS-pinned connection with TLS SNI/certificate validation for the approved hostname, no redirects, and hard type/byte/time bounds. Durably stage, hash, `ffprobe`, and fully decode with bounded `ffmpeg` stdout/stderr before atomic promotion. On restart, adopt an existing final/staged file only when its size and digest match durable ledger evidence.

Inspect the entire clip for safety, identity drift, physics, and acceptance criteria. Record container/codecs, duration, dimensions, frame rate, audio streams, byte length, SHA-256, prompt hash or protected prompt, request/approval digest, task/file IDs, model, source hashes and rights evidence, price evidence, automated and human review, and downstream lineage. Store signed URLs and keys outside ordinary logs; the reference client records only the URL hash and exact host.

Callbacks are optional. MiniMax verifies a callback by POSTing `challenge`, which the endpoint must echo within three seconds. Update payloads use lowercase `processing`, `success`, `failed`, unlike poll responses. No callback signature or shared-secret mechanism is documented. Use TLS, an unguessable path, body/rate limits, and an allowlist of expected task IDs; treat the callback only as a wake-up signal and re-query the authenticated status endpoint before terminal action or download.

## Apply rights, likeness, disclosure, and data controls

Use only prompts and media you are authorized to submit. For identifiable people, record informed consent for this purpose, territory, audience, duration, editing, and synthetic transformation; obtain any publicity, performer, labor, or minor/guardian approvals that apply. Never imply endorsement, impersonate for fraud, create intimate imagery without consent, or bypass safety filters. A face photo used by `S2V-01` is biometric-adjacent sensitive material even if the API labels it merely a reference image.

MiniMax's current API terms require compliance with law, public marking of deep-synthesis content, and applicable technical identifiers/filings. Add a visible disclosure and preserve provenance even when a route offers an `aigc_watermark` flag. Recheck local election, advertising, child-safety, privacy, biometrics, and AI-labeling rules before publication.

Do not promise â€œno trainingâ€ or fixed deletion. Current global API terms allow processing of input/output to provide, maintain, develop, improve, secure, and enforce the service; the privacy policy describes purpose-based retention and US data centers but does not give general video inputs a fixed deletion window. The provider may delete stored/generated information. Minimize personal data, set your own retention/deletion schedule, restrict ledger/artifact access, and execute a data-transfer assessment when region, subjects, or law require it. Re-read the exact region's current terms and privacy notice before sensitive production work.

## Resolve facts and conflicts deliberately

Classify every important statement as one of:

- **FACT:** current first-party reference, pricing, terms, or status documentation directly states it.
- **PROVIDER CLAIM:** MiniMax describes model quality or capability without independent validation.
- **HEURISTIC:** operational or creative practice inferred from experience and system constraints.
- **UNKNOWN:** current first-party material is silent, conflicting, or does not price the combination.

Known documentation conflicts/limits as of 2026-07-10:

- S2V reference omits duration/resolution while the guide example supplies 6 s/1080P; price is absent.
- Overview pages emphasize 2.3/Fast/02 while endpoint references retain legacy model names whose current pay-as-you-go prices are absent.
- China T2V reference exposes `aigc_watermark`; the global T2V reference does not.
- General file docs omit URL lifetime; do not inherit nine hours from a historical release or deprecated template endpoint.
- Poll statuses are title-case; callback statuses are lowercase.

When a conflict affects money, rights, compatibility, or retention, stop and verify in the correct console or with MiniMax support. Record the answer and retrieval time instead of silently choosing the convenient interpretation.

## First-party source map

Use only the matching region's current first-party pages for implementation facts:

- Global documentation index: <https://platform.minimax.io/docs/llms.txt>
- Global video guide and API references: <https://platform.minimax.io/docs/guides/video-generation>, <https://platform.minimax.io/docs/api-reference/video-generation-t2v>, <https://platform.minimax.io/docs/api-reference/video-generation-i2v>, <https://platform.minimax.io/docs/api-reference/video-generation-fl2v>, <https://platform.minimax.io/docs/api-reference/video-generation-s2v>, <https://platform.minimax.io/docs/api-reference/video-generation-query>, <https://platform.minimax.io/docs/api-reference/video-generation-download>
- Global pricing, limits, errors, and release notes: <https://platform.minimax.io/docs/guides/pricing-paygo>, <https://platform.minimax.io/docs/guides/pricing-video>, <https://platform.minimax.io/docs/guides/rate-limits>, <https://platform.minimax.io/docs/api-reference/errorcode>, <https://platform.minimax.io/docs/release-notes/apis>, <https://platform.minimax.io/docs/release-notes/models>
- Global API terms and privacy: <https://platform.minimax.io/protocol/terms-of-service>, <https://platform.minimax.io/protocol/privacy-policy>
- Mainland China documentation index and pay-as-you-go pricing: <https://platform.minimaxi.com/docs/llms.txt>, <https://platform.minimaxi.com/docs/guides/pricing-paygo>
- Region/key distinction: <https://platform.minimax.io/docs/token-plan/minimax-cli>
- Official service health: <https://status.minimax.io/>
- Separate consumer terms/privacy: <https://hailuoai.video/doc/terms-of-service.html>, <https://hailuoai.video/doc/privacy-policy.html>

The current documentation index contains no dedicated Hailuo 2.3 technical model card or safety card. Treat architecture, training corpus, benchmark methodology, systematic safety evaluation, and demographic performance as unknown unless MiniMax publishes a first-party artifact.


