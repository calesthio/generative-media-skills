---
name: xai-grok-imagine-video
description: Produce, edit, extend, and govern short videos with xAI's direct Grok Imagine Video API. Use for text-to-video, image-to-video, multi-reference video, natural-language video edits, video continuation, exact media-cost approval, asynchronous request recovery, Files/Batch integration, moderation review, and API privacy or residency decisions. Covers `grok-imagine-video` and image-only `grok-imagine-video-1.5`; excludes Grok consumer subscriptions, Grok on X, still-image generation, voice APIs, and third-party gateways.
---

# xAI Grok Imagine video

Use the direct xAI API as a controlled media-production service: freeze the creative brief and source rights, derive a priced request, persist intent before the paid POST, reconcile its asynchronous result, then preserve the artifact and its evidence.

All volatile facts and prices below were checked against xAI first-party sources on **2026-07-10**.

## Choose the correct production lane

The direct endpoint is `https://api.x.ai`. Authenticate server-side with `Authorization: Bearer $XAI_API_KEY`. API keys belong to xAI Console teams and use prepaid credit or invoiced API billing.

Do not blend these separate surfaces:

- Grok on `grok.com` and the mobile apps uses consumer plans, weekly allowances, consumer data controls, and consumer terms. â€œVideo 1.5 Fastâ€ is advertised there but is not a direct-API model slug.
- Grok on X is governed by X terms and privacy rules. An X Premium or SuperGrok subscription is not API credit.
- Grok Imagine image models use `/v1/images/*`; voice and speech use other endpoints. Their parameters and prices do not transfer to video.
- Partner platforms and gatewaysâ€”including services named in xAI marketingâ€”may wrap xAI models but add their own schema, moderation, retention, pricing, and regions.
- Azure, Google Cloud, and other managed offerings have separate authentication, quotas, feature parity, billing, and data-governance contracts. This skill describes xAI's direct API.

The public API uses `api.x.ai`. xAI advertises multiple inference clusters and enterprise data-residency options, while its status page shows US and EU regional API services. Do not select a regional hostname or promise residency from a page label alone. Use only the endpoint, region, and contractual controls provisioned for the team in xAI Console or its order form/DPA.

## Model and mode decision board

Exactly one mode may be active per request.

| Goal | Endpoint and REST fields | Valid model | Output controls |
|---|---|---|---|
| Text-to-video | `POST /v1/videos/generations`; `prompt` | `grok-imagine-video` | `duration` 1â€“15 s; listed aspect ratios; 480p/720p |
| Image-to-video | generations; `prompt` + `image` | either model | 1â€“15 s; listed aspect ratios; base: 480p/720p; 1.5: 480p/720p/1080p |
| Reference-to-video | generations; `prompt` + `reference_images` | `grok-imagine-video` only | 1â€“10 s; listed aspect ratios; 480p/720p; 1â€“7 references |
| Edit video | `POST /v1/videos/edits`; `prompt` + `video` | `grok-imagine-video` only | no custom duration/aspect/resolution; input â‰¤8.7 s; output inherits duration/aspect and resolution capped at 720p |
| Extend video | `POST /v1/videos/extensions`; `prompt` + `video` | `grok-imagine-video` only | input 2â€“15 s; extension 2â€“10 s, default 6; output inherits aspect/resolution capped at 720p |

`grok-imagine-video-1.5` is GA image-to-video only. It does not support text-to-video or reference-to-video, and its model page declares only image input. Current aliases are `grok-imagine-video-1.5-preview` and `grok-imagine-video-1.5-2026-05-30`; prefer the GA slug unless a recorded reproducibility decision requires the dated alias. Do not confuse the consumer â€œ1.5 Fastâ€ label with an API identifier.

Allowed generation aspect ratios are `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, and `2:3`; default is `16:9`. In image-to-video, omission follows the input image's aspect ratio. Supplying `aspect_ratio` overrides that and **stretches** the image, so crop/pad deliberately before submission when distortion is unacceptable. Default resolution is `480p`. The 1080p option is exclusive to 1.5 image-to-video.

Reference images guide people, products, clothing, or style without becoming the first frame. REST shape:

```json
{
  "model": "grok-imagine-video",
  "prompt": "The cyclist from <IMAGE_1> rides past the cafe from <IMAGE_2>.",
  "reference_images": [
    {"file_id": "file_authorized_subject"},
    {"url": "https://authorized.example/cafe.jpg"}
  ],
  "duration": 8,
  "aspect_ratio": "16:9",
  "resolution": "720p"
}
```

Use `image`, `reference_images`, or `video`, never a mixture. `image + reference_images` is explicitly invalid. Images may be PNG/JPEG/WebP and videos MP4 when referenced through Files; each locator may be an HTTPS URL, Base64 data URI, or private `file_id`. The current general Files guide says 48 MB while the upload reference says 50 MB. Treat the accepted maximum as a documentation conflict: stay below 48 MB or verify the exact endpoint before upload. Public/Base64 media limits outside Files are not stated.

An HTTPS locator authorizes xAI to fetch that resource and exposes the URL to request handling/logging; query strings may contain bearer-like secrets. Prefer a private `file_id` with a deliberate TTL for repeat use. Never log Base64 or signed URLs, and do not let your own application proxy or fetch arbitrary user URLs without DNS/IP/redirect SSRF controls and byte/time limits.

xAI's launch and 1.5 announcement describe native generated audio, including effects, ambience, and dialogue synchronized with action. This is a **provider claim**. The current video REST schema does not document an audio enable/disable field, a separate audio prompt, language controls, sample rate, channels, codec, or loudness. Frame rate is likewise undocumented. Put desired sound/dialogue sparingly in the main prompt, then inspect actual streams and never guarantee audio presence or fidelity before the result exists.

## Price the entire media transformation

Current direct-API USD rates:

| Model | Media input | 480p output | 720p output | 1080p output |
|---|---:|---:|---:|---:|
| `grok-imagine-video` | image $0.002 each; video $0.01/source second | $0.05/output second | $0.07/output second | unsupported |
| `grok-imagine-video-1.5` | image $0.01 | $0.08/output second | $0.14/output second | $0.25/output second |

Text input has no listed media charge. Calculate before approval:

- T2V: `duration Ã— output rate`.
- I2V: one image charge plus `duration Ã— output rate`.
- Reference: `number of reference images Ã— $0.002` plus `duration Ã— output rate`.
- Edit: `source duration Ã— $0.01` video-input charge plus `output duration Ã— inherited/capped-resolution output rate`. Output duration equals source duration.
- Extension: `source duration Ã— $0.01` plus `extension duration Ã— inherited/capped-resolution output rate`. xAI labels extension pricing promotional and subject to change; recheck immediately before approval.

Examples: a base-model 6-second 720p T2V is `$0.42`; a 1.5 12-second 1080p I2V is `$0.01 + $3.00 = $3.01`; a base 8-second 720p reference request with three images is `$0.006 + $0.56 = $0.566`. Quote each variant as a separate potentially billable request. Batch media requests receive **no batch discount**.

After completion, `usage.cost_in_usd_ticks` is the actual per-request charge; `10,000,000,000` ticks equal USD 1. Persist the integer and compare it with the approved quote. A price estimate does not authorize silent overage.

## Direct motion rather than decorating nouns

xAI publishes natural-language examples, not a formal camera-command grammar. Do not invent bracket commands, negative-prompt fields, seeds, CFG, FPS, or timecode guarantees.

Shape a generation prompt around five pieces:

1. Fix the opening composition and persistent identity/material facts.
2. Give the subject one causal action arc with visible weight and contact.
3. Name one dominant camera behavior in ordinary cinematography language: slow push-in, pan right, dolly out, tilt up, locked-off, handheld follow.
4. Sequence only a few beats with â€œfirst,â€ â€œthen,â€ and an observable ending.
5. Add lighting/style and, if important, a short sound or dialogue cue.

This is a **production heuristic**, not a parameter contract. A useful 8-second brief might read: â€œWide dawn shot of a blue ceramic cup on a rain-dark cafe table. A hand enters, lifts the cup, and steam curls toward the lens; the camera makes one slow push-in. End on the cup held steady beside the window. Quiet room tone, one soft ceramic clink.â€ Review motion causality, occlusion, hands, text, reflections, and audio sync rather than trusting descriptive adjectives.

Mode-specific direction:

- **1.5 or base I2V:** the image is the starting frame. Describe the deltaâ€”what begins moving, how the camera departs, and the end state. Avoid redescribing a conflicting composition. Crop/pad outside the API instead of stretching with an incompatible aspect ratio.
- **Reference-to-video:** assign one purpose per ordered reference and use `<IMAGE_1>`, `<IMAGE_2>`, etc. in the prompt, as xAI's example does. State which identity wears which product and which reference supplies environment/style. Fewer non-conflicting references are easier to audit than seven loosely related ones.
- **Edit:** ask for the smallest change and state invariants: â€œChange only the umbrella to matte yellow; preserve faces, timing, camera path, rain, signage, and audio.â€ xAI markets strong preservation, but that remains a provider claim until the entire edit is compared with its source.
- **Extension:** begin from the last visible motion, camera velocity, lighting, and sound bed. Describe only the next action. The returned file contains the original plus the extension; inspect the seam, duplicated frames, rhythm, identity, and audio transition.

## Establish the paid boundary before transport

Create a dossier containing the exact endpoint/body, model or dated alias, price-page timestamp, quote formula, source durations/resolutions, variant count, prompt, aspect/resolution, source hashes and rights, target region/team, retention/public-sharing choice, and moderation/disclosure reviewer.

Default to a local dry-run that needs no key, makes no network request, and does not consume the exclusive create ledger. Redact prompts, file IDs, Base64, and complete signed URLs to hashes. Canonically bind the exact endpoint/body digest, model/mode, ordered source hashes, local job key, input/output exact-host policies, destination, fresh price evidence, ZDR requirement, rights/moderation/QA evidence, USD quote, and one-create count. Require the matching digest plus a finite positive USD ceiling. Write the intent record with exclusive-create semantics **before** POSTing.

The video endpoints document no idempotency key. Therefore, never automatically retry a create POST. If a timeout, connection reset, or 5xx occurs without a captured `request_id`, record `create-outcome-unknown`; reconcile xAI Console billing, cost records, and support before approving a replacement. A known 4xx rejection may be fixed and resubmitted under a new attempt. Authenticated status GETs and the final media download may use bounded backoff.

`service_unavailable` is documented as retryable later, but this does not make a paid create idempotent. Other terminal codes include `invalid_argument`, `permission_denied`, and `failed_precondition`. General HTTP failures include 400, 401, 403, 404, 415, 422, and 429. Do not modify a blocked prompt to evade moderation.

First-party rate-limit renders conflicted during verification: the current limits/model surfaces returned 1 RPS, 10 RPS, and 70 RPM for video depending on render/cluster. The exact operational limit is therefore **UNKNOWN from public docs**. Use the team-specific xAI Console limit as authoritative and pace creates conservatively. This conflict does not justify concurrency at the largest displayed number.

## Example: runnable guarded REST client

Save this Python 3.11+ example as `xai_video_guard.py` outside the skill directory. It supports all five direct modes, quotes both media-input and output charges, defaults to dry-run, requires an exact digest and ceiling, stores intent before create, never retries create, resumes known request IDs, records ZDR headers, verifies moderation, and captures xAI's actual cost ticks. It downloads through an exact-host public-DNS-pinned TLS connection with no bearer or redirects, durably stages, probes, fully decodes, and crash-resumably publishes the MP4. Python 3.11+, `ffprobe`, and `ffmpeg` are required.

For every media locator, provide an ordered local mirror with `--source-local`. The program hashes and fully decodes each mirror; for edit/extend it re-probes duration/resolution and refuses dossier mismatches. A single source uses its file SHA-256; multiple references use the canonical ordered-list digest printed by the dossier process. HTTPS locators additionally require an exact `--input-host`; private `file_...` IDs do not.

```python
#!/usr/bin/env python3
import argparse
import hashlib
import http.client
import ipaddress
import json
import os
import pathlib
import random
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

API = "https://api.x.ai/v1"
OUT_RATE = {
    "grok-imagine-video": {"480p": Decimal("0.05"), "720p": Decimal("0.07")},
    "grok-imagine-video-1.5": {"480p": Decimal("0.08"), "720p": Decimal("0.14"), "1080p": Decimal("0.25")},
}
IMAGE_RATE = {"grok-imagine-video": Decimal("0.002"), "grok-imagine-video-1.5": Decimal("0.01")}
VIDEO_INPUT_RATE = Decimal("0.01")
ASPECTS = {"1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"}
MAX_JSON = 256 * 1024
MAX_VIDEO = 512 * 1024 * 1024
MAX_TOOL_OUTPUT = 512 * 1024

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None

NO_REDIRECT = urllib.request.build_opener(NoRedirect)

class APIProblem(Exception):
    def __init__(self, kind, status=None, body_sha256=None):
        super().__init__(kind); self.kind, self.status, self.body_sha256 = kind, status, body_sha256

def canonical(value): return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
def sha256_bytes(value): return hashlib.sha256(value).hexdigest()
def utc_now(): return datetime.now(timezone.utc).isoformat()

def fsync_directory(path):
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)

def save_record(path, record):
    target = pathlib.Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".xai-video-", suffix=".json", dir=target.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as out:
            out.write(canonical(record) + b"\n"); out.flush(); os.fsync(out.fileno())
        os.replace(name, target); fsync_directory(target.parent)
    finally:
        if os.path.exists(name): os.unlink(name)

def exclusive_record(path, record):
    target = pathlib.Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "wb") as out:
        out.write(canonical(record) + b"\n"); out.flush(); os.fsync(out.fileno())
    fsync_directory(target.parent)

def read_record(path):
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
                if total[0] > cap: overflow.set(); process.kill(); return
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

def exact_hosts(raw, label):
    hosts = []
    for item in raw.split(","):
        host = item.strip().rstrip(".").lower()
        if not host: continue
        if "*" in host or "/" in host or ":" in host: raise SystemExit(f"{label} accepts exact DNS hostnames only")
        try: ipaddress.ip_address(host)
        except ValueError: pass
        else: raise SystemExit(f"{label} rejects IP literals")
        hosts.append(host)
    if not hosts: raise SystemExit(f"{label} requires at least one reviewed exact host")
    return tuple(sorted(set(hosts)))

def public_addresses(host):
    addresses = []
    for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        address = ipaddress.ip_address(item[4][0])
        if not address.is_global: raise SystemExit("Media host resolves to a non-public address")
        addresses.append(str(address))
    if not addresses: raise SystemExit("Media host did not resolve")
    return sorted(set(addresses))

def locator(value, allowed_hosts):
    if value.startswith("file_"):
        if len(value) > 256 or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for character in value):
            raise SystemExit("Invalid xAI file_id")
        return {"file_id": value}
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.fragment or parsed.port not in (None, 443):
        raise SystemExit("Media locator must be an xAI file_id or public HTTPS URL")
    host = parsed.hostname.rstrip(".").lower()
    try:
        ipaddress.ip_address(host)
    except ValueError: pass
    else: raise SystemExit("IP-literal media URLs are forbidden")
    if host not in allowed_hosts: raise SystemExit("Media URL host is outside the approved exact-host policy")
    return {"url": value}

def redact(value):
    if "url" in value:
        p = urllib.parse.urlsplit(value["url"])
        return {"url_host": p.hostname, "url_sha256": sha256_bytes(value["url"].encode("utf-8"))}
    if "file_id" in value: return {"file_id_sha256": sha256_bytes(value["file_id"].encode("utf-8"))}
    return {"locator_sha256": sha256_bytes(canonical(value))}

def request_json(method, url, api_key, payload=None, retries=0):
    body = None if payload is None else canonical(payload)
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=body, method=method, headers={
            "Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "Accept": "application/json"})
        try:
            with NO_REDIRECT.open(req, timeout=45) as response:
                raw = response.read(MAX_JSON + 1)
                zdr = response.headers.get("x-zero-data-retention")
            if len(raw) > MAX_JSON: raise APIProblem("response-too-large")
            try: data = json.loads(raw)
            except json.JSONDecodeError: raise APIProblem("invalid-json", response.status, sha256_bytes(raw))
            if not isinstance(data, dict): raise APIProblem("non-object-json", response.status, sha256_bytes(raw))
            return data, None if zdr is None else zdr.lower()
        except urllib.error.HTTPError as exc:
            raw = exc.read(MAX_JSON + 1)
            problem = APIProblem("http-error", exc.code, sha256_bytes(raw))
            if 400 <= exc.code < 500 or attempt == retries:
                raise problem
        except APIProblem: raise
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempt == retries: raise APIProblem("transport-" + type(exc).__name__)
        time.sleep(min(2 ** attempt, 8) * (1 + random.random() * 0.25))

def source_evidence(args):
    required = 0 if args.mode == "text" else (len(args.reference) if args.mode == "reference" else 1)
    if len(args.source_local) != required: raise SystemExit(f"Provide exactly {required} ordered --source-local mirrors")
    evidence = []
    for path_text in args.source_local:
        path = pathlib.Path(path_text).resolve()
        if not path.is_file() or path.stat().st_size <= 0 or path.stat().st_size >= 48 * 1024 * 1024:
            raise SystemExit("Source mirror must exist and remain below the conservative 48 MiB Files limit")
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            header = stream.read(32); stream.seek(0)
            for chunk in iter(lambda: stream.read(1024 * 1024), b""): digest.update(chunk)
        kind = "video" if args.mode in {"edit", "extend"} else "image"
        if kind == "image" and not (header.startswith(b"\xff\xd8\xff") or header.startswith(b"\x89PNG\r\n\x1a\n") or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")):
            raise SystemExit("Image mirror must be JPEG, PNG, or WebP by signature")
        if kind == "video" and (len(header) < 12 or header[4:8] != b"ftyp"):
            raise SystemExit("Video mirror must be MP4 by signature")
        raw = bounded_process(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], 30, MAX_JSON)
        metadata = json.loads(raw); streams = metadata.get("streams", [])
        visual = next((item for item in streams if item.get("codec_type") == "video"), None)
        if not visual: raise SystemExit("Source mirror has no visual stream")
        bounded_process(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "null", "-"], 300)
        item = {"path": str(path), "sha256": digest.hexdigest(), "bytes": path.stat().st_size,
                "kind": kind, "width": visual.get("width"), "height": visual.get("height")}
        if kind == "video":
            try: duration = Decimal(str(metadata.get("format", {}).get("duration")))
            except InvalidOperation: raise SystemExit("Source video duration is invalid")
            if not duration.is_finite() or duration <= 0: raise SystemExit("Source duration must be finite and positive")
            short_edge = min(int(visual.get("width")), int(visual.get("height")))
            resolution = "480p" if short_edge <= 480 else ("720p" if short_edge <= 720 else "1080p")
            item.update(duration=str(duration), codec=visual.get("codec_name"), resolution=resolution)
        evidence.append(item)
    if evidence and args.source_sha256:
        expected = evidence[0]["sha256"] if len(evidence) == 1 else sha256_bytes(canonical([item["sha256"] for item in evidence]))
        if args.source_sha256.lower() != expected: raise SystemExit("source-sha256 does not match the validated local mirror evidence")
    if evidence and args.mode in {"edit", "extend"}:
        actual_duration = Decimal(evidence[0]["duration"])
        if args.source_duration is not None and abs(args.source_duration - actual_duration) > Decimal("0.05"):
            raise SystemExit("Declared source duration differs from ffprobe evidence")
        if args.source_resolution is not None and args.source_resolution != evidence[0]["resolution"]:
            raise SystemExit("Declared source resolution differs from ffprobe evidence")
        args.source_duration, args.source_resolution = actual_duration, evidence[0]["resolution"]
    return evidence

def quote(args):
    if args.mode == "edit":
        output_seconds = Decimal(str(args.source_duration))
        output_resolution = "720p" if args.source_resolution in {"720p", "1080p"} else "480p"
        return output_seconds * (VIDEO_INPUT_RATE + OUT_RATE[args.model][output_resolution])
    if args.mode == "extend":
        output_resolution = "720p" if args.source_resolution in {"720p", "1080p"} else "480p"
        return Decimal(str(args.source_duration)) * VIDEO_INPUT_RATE + Decimal(args.duration) * OUT_RATE[args.model][output_resolution]
    result = Decimal(args.duration) * OUT_RATE[args.model][args.resolution]
    if args.mode == "image":
        result += IMAGE_RATE[args.model]
    elif args.mode == "reference":
        result += IMAGE_RATE[args.model] * len(args.reference)
    return result

def validate(args):
    if not args.prompt.strip(): raise SystemExit("A non-empty prompt is required")
    if args.model == "grok-imagine-video-1.5" and args.mode != "image":
        raise SystemExit("grok-imagine-video-1.5 is image-to-video only")
    if args.mode in {"text", "image", "reference"}:
        if args.duration is None or not 1 <= args.duration <= 15: raise SystemExit("Generation duration must be 1â€“15 seconds")
        if args.mode == "reference" and args.duration > 10: raise SystemExit("Reference-to-video maximum is 10 seconds")
        if args.resolution not in OUT_RATE[args.model]: raise SystemExit("Resolution unsupported by selected model")
        if args.aspect_ratio not in ASPECTS: raise SystemExit("Unsupported aspect ratio")
    if args.mode == "image" and not args.image: raise SystemExit("--image is required")
    if args.mode == "reference" and not 1 <= len(args.reference) <= 7: raise SystemExit("Provide 1â€“7 references")
    if args.mode in {"edit", "extend"}:
        if not args.video or args.source_duration is None or args.source_resolution is None:
            raise SystemExit("Video mode requires --video, --source-duration, --source-resolution, and a local mirror")
        if args.model != "grok-imagine-video": raise SystemExit("Editing and extension require grok-imagine-video")
        if not args.source_duration.is_finite(): raise SystemExit("Source duration must be finite")
    if args.mode == "edit" and not 0 < args.source_duration <= 8.7:
        raise SystemExit("Edit input must be at most 8.7 seconds")
    if args.mode == "extend":
        if not 2 <= args.source_duration <= 15: raise SystemExit("Extension input must be 2â€“15 seconds")
        if args.duration is None or not 2 <= args.duration <= 10: raise SystemExit("Extension duration must be 2â€“10 seconds")
    if args.mode != "text" and not args.source_sha256:
        raise SystemExit("Media mode requires --source-sha256 provenance evidence")
    if args.source_sha256 and (len(args.source_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in args.source_sha256)):
        raise SystemExit("--source-sha256 must be exactly 64 hexadecimal characters")

def build(args, input_hosts):
    endpoint = "/videos/generations"
    body = {"model": args.model, "prompt": args.prompt}
    if args.mode in {"text", "image", "reference"}:
        body.update(duration=args.duration, aspect_ratio=args.aspect_ratio, resolution=args.resolution)
    if args.mode == "image": body["image"] = locator(args.image, input_hosts)
    if args.mode == "reference": body["reference_images"] = [locator(x, input_hosts) for x in args.reference]
    if args.mode == "edit": endpoint = "/videos/edits"; body["video"] = locator(args.video, input_hosts)
    if args.mode == "extend":
        endpoint = "/videos/extensions"; body["video"] = locator(args.video, input_hosts); body["duration"] = args.duration
        body.pop("aspect_ratio", None); body.pop("resolution", None)
    return endpoint, body

def redacted_body(body):
    clean = dict(body)
    for key in ("image", "video"):
        if key in clean: clean[key] = redact(clean[key])
    if "reference_images" in clean: clean["reference_images"] = [redact(x) for x in clean["reference_images"]]
    return clean

class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, address, timeout):
        super().__init__(host, 443, timeout=timeout, context=ssl.create_default_context()); self.address = address
    def connect(self):
        raw = socket.create_connection((self.address, 443), self.timeout)
        try: self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except Exception: raw.close(); raise

def output_target(url, allowed_hosts):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.fragment or parsed.port not in (None, 443):
        raise RuntimeError("Output URL violates HTTPS authority policy")
    host = parsed.hostname.rstrip(".").lower()
    try: ipaddress.ip_address(host)
    except ValueError: pass
    else: raise RuntimeError("Output URL rejects IP literals")
    if host not in allowed_hosts: raise RuntimeError("Output host is outside the approved exact-host policy")
    addresses = public_addresses(host); target = parsed.path or "/"
    if parsed.query: target += "?" + parsed.query
    return host, target, addresses

def verify_mp4(path):
    path = pathlib.Path(path); size = path.stat().st_size
    if size <= 0 or size > MAX_VIDEO: raise RuntimeError("Artifact size is outside policy")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        if stream.read(12)[4:8] != b"ftyp": raise RuntimeError("Artifact lacks MP4 ftyp signature")
        stream.seek(0)
        for chunk in iter(lambda: stream.read(1024 * 1024), b""): digest.update(chunk)
    raw = bounded_process(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], 30, MAX_JSON)
    metadata = json.loads(raw); streams = metadata.get("streams", [])
    video = next((item for item in streams if item.get("codec_type") == "video"), None)
    if not video: raise RuntimeError("Artifact has no video stream")
    bounded_process(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "null", "-"], 300)
    return {"bytes": size, "sha256": digest.hexdigest(), "qa": {"container": metadata.get("format", {}).get("format_name"),
            "video_codec": video.get("codec_name"), "width": video.get("width"), "height": video.get("height"),
            "fps": video.get("avg_frame_rate"), "duration": metadata.get("format", {}).get("duration"),
            "audio_present": any(item.get("codec_type") == "audio" for item in streams), "full_decode": "passed"}}

def download_mp4(url, output, allowed_hosts, ledger_path, record):
    target = pathlib.Path(output); target.parent.mkdir(parents=True, exist_ok=True)
    stage = target.with_name("." + target.name + ".xai-stage"); expected = record.get("artifact_staged") or record.get("artifact")
    if target.exists():
        if not isinstance(expected, dict): raise RuntimeError("Existing artifact has no durable expected evidence")
        artifact = verify_mp4(target)
        if (artifact["sha256"], artifact["bytes"]) != (expected.get("sha256"), expected.get("bytes")): raise RuntimeError("Existing artifact mismatch")
        return artifact
    if stage.exists() and isinstance(expected, dict):
        artifact = verify_mp4(stage)
        if (artifact["sha256"], artifact["bytes"]) != (expected.get("sha256"), expected.get("bytes")): raise RuntimeError("Staged artifact mismatch")
        os.replace(stage, target); fsync_directory(target.parent); return artifact
    host, path_query, addresses = output_target(url, allowed_hosts); url_hash = sha256_bytes(url.encode("utf-8"))
    if record.get("output_url_sha256") not in (None, url_hash): raise RuntimeError("Output URL changed during incomplete transfer")
    record.update(state="downloading", output_url_sha256=url_hash, output_host=host, download_started_at=record.get("download_started_at") or utc_now())
    save_record(ledger_path, record); stage.unlink(missing_ok=True)
    connection = PinnedHTTPSConnection(host, addresses[0], 120)
    try:
        connection.request("GET", path_query, headers={"Host": host, "Accept": "video/mp4", "User-Agent": "xai-video-guard/2"})
        response = connection.getresponse()
        if response.status != 200: raise RuntimeError(f"Output returned HTTP {response.status}")
        media_type = response.getheader("Content-Type", "").split(";", 1)[0].lower()
        if media_type not in {"video/mp4", "application/octet-stream"}: raise RuntimeError("Unexpected output media type")
        announced = response.getheader("Content-Length")
        if announced is not None and (not announced.isdigit() or int(announced) > MAX_VIDEO): raise RuntimeError("Invalid/excessive Content-Length")
        fd = os.open(stage, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600); total = 0
        try:
            with os.fdopen(fd, "wb") as dst:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk: break
                    total += len(chunk)
                    if total > MAX_VIDEO: raise RuntimeError("Output exceeded byte cap")
                    dst.write(chunk)
                dst.flush(); os.fsync(dst.fileno())
        except BaseException: stage.unlink(missing_ok=True); raise
    finally: connection.close()
    artifact = verify_mp4(stage); record.update(state="artifact-staged", artifact_staged=artifact, artifact_validated_at=utc_now())
    save_record(ledger_path, record); os.replace(stage, target); fsync_directory(target.parent); return artifact

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["text", "image", "reference", "edit", "extend"], required=True)
    parser.add_argument("--model", choices=list(OUT_RATE), required=True)
    parser.add_argument("--prompt", required=True); parser.add_argument("--duration", type=int)
    parser.add_argument("--resolution", choices=["480p", "720p", "1080p"], default="480p")
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--image"); parser.add_argument("--reference", action="append", default=[]); parser.add_argument("--video")
    parser.add_argument("--source-duration", type=Decimal); parser.add_argument("--source-resolution", choices=["480p", "720p", "1080p"])
    parser.add_argument("--source-sha256", help="SHA-256 of source file, or a dossier hash covering ordered references")
    parser.add_argument("--source-local", action="append", default=[], help="Ordered local mirror; repeat for references")
    parser.add_argument("--job-key", required=True)
    parser.add_argument("--input-host", default="", help="Comma-separated reviewed exact source URL hosts; omit for file_id-only inputs")
    parser.add_argument("--output-host", required=True, help="Comma-separated reviewed exact result hosts")
    parser.add_argument("--pricing-checked-at", required=True); parser.add_argument("--pricing-evidence-sha256", required=True)
    parser.add_argument("--rights-sha256", required=True); parser.add_argument("--moderation-sha256", required=True); parser.add_argument("--qa-plan-sha256", required=True)
    parser.add_argument("--ledger", required=True); parser.add_argument("--output", default="xai-video.mp4")
    parser.add_argument("--execute", action="store_true"); parser.add_argument("--approval-sha256"); parser.add_argument("--max-cost-usd")
    parser.add_argument("--require-zdr", action="store_true")
    args = parser.parse_args()
    if not args.job_key or any(not (character.isalnum() or character in "-_") for character in args.job_key): raise SystemExit("Invalid job-key")
    validate(args)
    input_hosts = () if not args.input_host.strip() else exact_hosts(args.input_host, "input-host")
    output_hosts = exact_hosts(args.output_host, "output-host")
    endpoint, body = build(args, set(input_hosts)); sources = source_evidence(args); amount = quote(args)
    if not amount.is_finite() or amount <= 0: raise SystemExit("Computed cost must be finite and positive")
    for label, value in (("pricing", args.pricing_evidence_sha256), ("rights", args.rights_sha256), ("moderation", args.moderation_sha256), ("QA", args.qa_plan_sha256)):
        if len(value) != 64 or any(character not in "0123456789abcdefABCDEF" for character in value): raise SystemExit(f"{label} evidence must be SHA-256")
    safe_body = redacted_body(body); safe_body["prompt"] = "sha256:" + sha256_bytes(args.prompt.encode("utf-8"))
    safe_sources = [{key: value for key, value in item.items() if key != "path"} | {"path_sha256": sha256_bytes(item["path"].encode("utf-8"))} for item in sources]
    output_policy = {"exact_hosts": list(output_hosts), "https": True, "redirects": "reject", "public_dns": True,
                     "reject_ip_literals": True, "dns_pinning": "connect-IP-with-TLS-SNI-and-host-certificate",
                     "max_bytes": MAX_VIDEO, "container": "mp4", "full_decode": True}
    request_hash = sha256_bytes(canonical(body))
    envelope = {"schema_version": 1, "job_key": args.job_key, "api_origin": API, "endpoint": endpoint,
                "mode": args.mode, "model": args.model, "request_sha256": request_hash, "redacted_request": safe_body,
                "sources": safe_sources, "input_exact_hosts": list(input_hosts), "output": str(pathlib.Path(args.output).resolve()),
                "output_policy": output_policy, "quoted_usd": format(amount, "f"), "create_count": 1,
                "pricing": {"checked_at": args.pricing_checked_at, "evidence_sha256": args.pricing_evidence_sha256.lower()},
                "governance": {"rights_sha256": args.rights_sha256.lower(), "moderation_sha256": args.moderation_sha256.lower(),
                               "qa_plan_sha256": args.qa_plan_sha256.lower(), "require_zdr": args.require_zdr}}
    approval = sha256_bytes(canonical(envelope))
    print(json.dumps({"approval_sha256": approval, "plan": envelope}, indent=2, ensure_ascii=False))
    print(f"DRY RUN â€” exact maximum USD {format(amount, 'f')}; one create; no network request sent", file=sys.stderr)
    if not args.execute: return
    if args.approval_sha256 != approval: raise SystemExit("Exact approval digest mismatch")
    try: maximum = Decimal(args.max_cost_usd or "")
    except InvalidOperation: raise SystemExit("max-cost-usd must be decimal")
    if not maximum.is_finite() or maximum <= 0 or maximum < amount: raise SystemExit("max-cost-usd must be finite, positive, and at least the quote")
    try: checked_at = datetime.fromisoformat(args.pricing_checked_at.replace("Z", "+00:00"))
    except ValueError: raise SystemExit("pricing-checked-at must be ISO-8601")
    if checked_at.tzinfo is None: raise SystemExit("pricing-checked-at must include timezone")
    age = datetime.now(timezone.utc) - checked_at.astimezone(timezone.utc)
    if age.total_seconds() < -300 or age.total_seconds() > 86400: raise SystemExit("Pricing check must be no more than 24 hours old")
    for item in body.values():
        locators = item if isinstance(item, list) else [item]
        for locator_item in locators:
            if isinstance(locator_item, dict) and "url" in locator_item: public_addresses(urllib.parse.urlsplit(locator_item["url"]).hostname)
    if args.require_zdr and os.environ.get("XAI_ZDR_CONFIRMED") != "1":
        raise SystemExit("Verify ZDR in xAI Console, then set XAI_ZDR_CONFIRMED=1 for this governed run")
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key: raise SystemExit("Set XAI_API_KEY in the server-side environment")
    ledger_path = pathlib.Path(args.ledger)
    if ledger_path.exists():
        record = read_record(ledger_path)
        if record.get("request_sha256") != request_hash or record.get("approval_sha256") != approval: raise SystemExit("Ledger belongs to a different approved request")
        request_id = record.get("request_id")
        if not request_id: raise SystemExit(f"Ledger state {record.get('state')!r} has no request ID; never replay")
        zdr = record.get("create_zdr_header")
    else:
        record = {"schema_version": 1, "state": "intent-recorded", "recorded_at": utc_now(), "job_key": args.job_key,
                  "request_sha256": request_hash, "approval_sha256": approval, "endpoint": endpoint, "mode": args.mode,
                  "model": args.model, "redacted_request": safe_body, "sources": safe_sources, "output_policy": output_policy,
                  "quoted_usd": format(amount, "f"), "pricing": envelope["pricing"], "governance": envelope["governance"]}
        try: exclusive_record(ledger_path, record)
        except FileExistsError: raise SystemExit("Another process acquired this job ledger")
        record.update(state="create-started", create_started_at=utc_now()); save_record(ledger_path, record)
        try: created, zdr = request_json("POST", API + endpoint, api_key, body, retries=0)
        except APIProblem as exc:
            ambiguous = exc.status is None or exc.status >= 500 or exc.status in {408, 409}
            record.update(state="create-outcome-unknown" if ambiguous else "create-rejected-known", error_kind=exc.kind,
                          http_status=exc.status, error_body_sha256=exc.body_sha256, replay_allowed=False, create_outcome_at=utc_now())
            save_record(ledger_path, record)
            raise SystemExit("Create stopped; ambiguous jobs must be reconciled and no job key is replayable")
        request_id = created.get("request_id")
        if not isinstance(request_id, str) or not request_id or len(request_id) > 128:
            record.update(state="create-outcome-unknown", error_kind="unusable-success-request-id",
                          response_sha256=sha256_bytes(canonical(created)), replay_allowed=False, create_outcome_at=utc_now())
            save_record(ledger_path, record); raise SystemExit("No usable request_id returned; reconcile before replacement")
        record.update(state="request-pending", request_id=request_id, create_zdr_header=zdr, submitted_at=utc_now()); save_record(ledger_path, record)
    if args.require_zdr and zdr != "true":
        record["zdr_mismatch"] = True; save_record(ledger_path, record)
        raise SystemExit("ZDR header was not true; stop handling and escalate immediately")
    deadline = time.monotonic() + 20 * 60
    while time.monotonic() < deadline:
        try: result, poll_zdr = request_json("GET", API + "/videos/" + urllib.parse.quote(request_id, safe=""), api_key, retries=3)
        except APIProblem as exc:
            record.update(poll_error_kind=exc.kind, poll_http_status=exc.status, poll_error_body_sha256=exc.body_sha256); save_record(ledger_path, record)
            raise SystemExit("Polling failed; resume the known request ID later")
        status = result.get("status"); record.update(last_status=status, poll_zdr_header=poll_zdr, progress=result.get("progress"), last_polled_at=utc_now()); save_record(ledger_path, record)
        if args.require_zdr and poll_zdr != "true":
            record["zdr_mismatch"] = True; save_record(ledger_path, record)
            raise SystemExit("A poll response did not confirm ZDR; stop handling and escalate")
        if status == "done":
            video = result.get("video") or {}
            if video.get("respect_moderation") is not True:
                record.update(state="moderation-blocked", moderation_value=video.get("respect_moderation")); save_record(ledger_path, record)
                raise SystemExit("Output did not pass moderation; do not publish or bypass")
            url = video.get("url")
            if not url: raise RuntimeError("Done response has no video URL")
            artifact = download_mp4(url, args.output, set(output_hosts), ledger_path, record)
            ticks = (result.get("usage") or {}).get("cost_in_usd_ticks")
            if not isinstance(ticks, int) or ticks < 0: reconciliation = {"status": "missing-or-invalid-stop-further-creates"}
            else:
                actual = Decimal(ticks) / Decimal(10_000_000_000)
                reconciliation = {"status": "matched" if actual == amount else "variance-stop-further-creates",
                                  "actual_usd": format(actual, "f"), "variance_usd": format(actual - amount, "f")}
                if actual > maximum: reconciliation["status"] = "ceiling-exceeded-stop-further-creates"
            record.update(state="artifact-secured", artifact=dict(artifact, path=str(pathlib.Path(args.output).resolve())),
                          output_duration=video.get("duration"), cost_in_usd_ticks=ticks, cost_reconciliation=reconciliation,
                          result_model=result.get("model"), human_review="pending", stored_at=utc_now())
            save_record(ledger_path, record); print(json.dumps({"artifact": record["artifact"], "cost_reconciliation": reconciliation}, indent=2)); return
        if status in {"failed", "expired"}:
            record.update(state="request-" + status, error_sha256=sha256_bytes(str(result.get("error", "")).encode("utf-8"))); save_record(ledger_path, record)
            raise SystemExit(f"Video request {status}")
        if status != "pending": raise RuntimeError(f"Unknown status {status!r}")
        time.sleep(5)
    record["state"] = "local-poll-timeout"; save_record(ledger_path, record)
    raise SystemExit("Local polling ended; resume GET by request_id, never create a replacement")

if __name__ == "__main__":
    main()
```

Example dry-run: one 6-second 720p T2V, quoted at USD 0.42, with no key or network request. Replace each evidence placeholder with a protected 64-hex digest and use the current timezone-aware price-check time:

```bash
python xai_video_guard.py --mode text --model grok-imagine-video --duration 6 --resolution 720p --aspect-ratio 16:9 --job-key cup-v1 --output-host vidgen.x.ai --pricing-checked-at 2026-07-10T12:00:00Z --pricing-evidence-sha256 '<64-hex>' --rights-sha256 '<64-hex>' --moderation-sha256 '<64-hex>' --qa-plan-sha256 '<64-hex>' --prompt "Wide dawn shot of a blue ceramic cup on a rain-dark cafe table. A hand lifts it while the camera makes one slow push-in. End beside the window. Quiet room tone and one soft ceramic clink." --ledger attempt-cup.json
```

After protected payload/current-price review, repeat the exact unchanged arguments and add `--execute --approval-sha256 '<printed-digest>' --max-cost-usd 0.42`; export `XAI_API_KEY` only in the server-side shell. Never paste a real key into the file, shared command history, browser code, logs, or chat.

Example 1.5 I2V dry-run: a 12-second 1080p output costs USD 3.010. The source must be rights-cleared and its SHA-256 recorded:

```bash
python xai_video_guard.py --mode image --model grok-imagine-video-1.5 --duration 12 --resolution 1080p --aspect-ratio 16:9 --image file_authorized_waterfall --source-local ./authorized-waterfall.png --source-sha256 REPLACE_WITH_LOCAL_FILE_SHA256 --job-key waterfall-v1 --output-host vidgen.x.ai --pricing-checked-at 2026-07-10T12:00:00Z --pricing-evidence-sha256 '<64-hex>' --rights-sha256 '<64-hex>' --moderation-sha256 '<64-hex>' --qa-plan-sha256 '<64-hex>' --prompt "The waterfall surges from the starting frame; mist rolls toward the lens as the camera slowly dollies back. End on the full cliff. Deep rushing water and distant birds." --ledger attempt-waterfall.json
```

The example deliberately downloads rather than requesting `storage_options`. Add server-side persistence only after deciding its privacy lifecycle.

## Treat asynchronous state as evidence

Create returns `request_id`. Poll `GET /v1/videos/{request_id}` every few seconds; xAI examples use five seconds. Exact statuses are `pending`, `done`, `expired`, and `failed`. A local SDK timeout does not mean provider failure: preserve the request ID and resume polling.

On `done`, verify `video.respect_moderation` is true, capture `model`, `progress`, `duration`, and integer cost ticks, then download the temporary `vidgen.x.ai` URL promptly. The ordinary URL has no published exact lifetime. Batch image/video result URLs are a separate case and expire after one hour.

Run `ffprobe` and decode the full file. Record container, video codec, dimensions, duration, frame rate, every audio stream/codec/channel/sample-rate, bytes, and SHA-256. Review opening-frame fidelity, temporal identity, contact physics, camera continuity, edit invariants or extension seam, audio sync, speech accuracy, unwanted text/logos, moderation, and public-disclosure readiness.

## Choose storage, Files, and Batch intentionally

Prefer a private Files `file_id` over a public source URL for repeated governed inputs. xAI Files accepts PNG/JPEG/WebP and MP4 for Imagine references; files are team-scoped. Uploads persist until deletion unless `expires_after` is set from 3,600 to 2,592,000 seconds (one hour to 30 days). Delete them when the production record no longer requires them.

Files storage is separately priced at `$0.025/GiB/day`; Files downloads are `$0.20/GiB` on the current pricing page. Include this time/volume-dependent cost whenever `file_id` or `storage_options` persistence is part of the approved workflow. The guarded example avoids these variable storage charges by using the ordinary ephemeral result and a local governed download.

`storage_options` can persist an Imagine output privately:

```json
{"filename":"approved-cut.mp4","expires_after":86400,"public_url":false}
```

Omitting `expires_after` makes the file permanent until deletion. `public_url: true` creates an unauthenticated share link; without an expiry it can be indefinite. Prefer private storage. If public delivery is necessary, set the shortest 1-hour-to-30-day expiry, log its audience and expiry, and revoke it after delivery. A public URL never outlives its file. Do not record signed/unguessable URLs in ordinary logs.

The compatibility of ZDR with persistent Files or `storage_options` is not clearly documented. Persistent storage is conceptually different from transient inference. For strict ZDR work, avoid Files persistence until xAI confirms the contracted behavior; keep your own governed encrypted copy.

Batch supports `/v1/videos/generations`, `/edits`, and `/extensions`, including mixed JSONL jobs. It charges standard media ratesâ€”no video discountâ€”and most batches complete within 24 hours. Use it only for reviewed bulk work with a total-cost ceiling, stable `custom_id`s, and per-item rights records. Its returned media URLs expire after one hour. Batch is not an idempotency workaround for uncertain real-time creates.

## Moderate, disclose, and protect people

xAI marks videos as subject to content-policy review. `respect_moderation: true` is necessary but not sufficient for publication. Do not evade provider safeguards or remove provenance metadata/watermarks; the AUP expressly prohibits both safeguard circumvention and stripping embedded provenance.

Obtain rights to all prompts, source images/video, brands, locations, music, voices, and performances. For an identifiable person, document informed authorization covering likeness/voice, synthetic manipulation, edit scope, audience, territory, duration, and commercial context. The AUP prohibits deceptive impersonation, nonconsensual intimate or pornographic likenesses, defamatory/false-light depictions, privacy/publicity infringement, fraud, and sexual exploitation of children. A celebrity image found online is not consent.

Under the current Enterprise Terms, the customer retains input rights and owns output as between xAI and the customer, subject to applicable law and excluding xAI technology. That allocation does not create rights in third-party people, brands, performances, or copyrighted sources; output may also be non-unique. The Terms prohibit representing output as human-generated and prohibit using it to train the customerâ€™s or its providersâ€™ ML/AI models.

Clearly disclose material AI generation or alteration where viewers could be misled, and apply jurisdiction/platform-specific political, advertising, biometrics, child-safety, and synthetic-media labels. Preserve original media, hashes, prompts, model alias, xAI request/cost evidence, edits, and disclosure decisions. Never claim xAI moderation establishes truth, endorsement, copyright clearance, or legal compliance.

## Set the API data contract, not the consumer one

For direct API customers, xAI's Enterprise Terms, DPA, and AUP govern; the public consumer Privacy Policy explicitly says it does not cover xAI API data processed for business customers. It also says Grok on X is governed by X policies.

xAI's API security FAQ states that API input/output is not used for training without explicit permission and is normally retained for 30 days for abuse audit, then deleted. Enterprise Terms state User Content is not used to train foundation/AI systems and specify deletion no later than 30 days after the interaction, subject to stated legal, safety, security, moderation, and investigation exceptions.

ZDR is enterprise-only and team-wide. Verify it in xAI Console and record the `x-zero-data-retention: true` response header on create and polls. Moderation still runs. The FAQ says data is never persisted and no record remains after delivery; the current Enterprise Terms more precisely allow transient processing artifacts until the earlier of delivery or one hour after completion, with no durable logs/backups afterward. Treat the legal terms and order form as controlling, record this wording difference, and do not advertise â€œzero processingâ€ or bypass your own audit/retention duties.

The current Enterprise Terms require customers to prevent intentional Personal Data submission outside a ZDR-enabled API. Route any Personal Data only through the contracted ZDR team and the appropriate DPA, lawful basis, notices, minimization, transfer assessment, access controls, and deletion plan. PHI additionally requires a BAA and ZDR. EU residency is an enterprise option, not a default inferred from `api.x.ai`. Confirm cluster, subprocessors, cross-border transfer mechanism, and failover behavior contractually.

## Keep claims in their proper category

- **Documented fact:** request field, limit, price, status, policy text, or observed response property in a current xAI first-party source.
- **Provider claim:** xAI's statements about quality, physics, instruction following, preservation, audio, latency, or benchmark standing.
- **Production heuristic:** prompt structure, reference reduction, camera simplicity, review strategy, or continuity practice derived from filmmaking and risk control.
- **Unknown:** anything the current schema and contract do not settleâ€”FPS, exact ephemeral URL lifetime, audio specifications/controls, seed, negative prompt, Base64/public input size, precise ZDR/Files interaction, or residency without an enterprise configuration.

Resolve consequential conflicts in favor of the newer endpoint-specific reference, xAI Console, and signed contract; otherwise stop and ask xAI support. Known conflicts on 2026-07-10 include:

- public rate-limit/model renders disagree among 1 RPS, 10 RPS, and 70 RPM;
- Files guide says 48 MB while upload reference says 50 MB;
- ZDR FAQ says nothing persists after delivery, while Enterprise Terms spell out an earlier-of-delivery-or-one-hour transient boundary;
- xAI's launch/news pages describe native audio, but the REST reference exposes no audio controls or technical specification;
- default Imagine output URLs are merely â€œtemporary,â€ whereas the one-hour lifetime is explicitly documented only for Batch results.

## First-party evidence map

- Video guide and REST reference: <https://docs.x.ai/developers/model-capabilities/video/generation>, <https://docs.x.ai/developers/rest-api-reference/inference/videos>
- I2V, references, edits, extensions: <https://docs.x.ai/developers/model-capabilities/video/image-to-video>, <https://docs.x.ai/developers/model-capabilities/video/reference-to-video>, <https://docs.x.ai/developers/model-capabilities/video/editing>, <https://docs.x.ai/developers/model-capabilities/video/extension>
- Model pages and pricing: <https://docs.x.ai/developers/models/grok-imagine-video>, <https://docs.x.ai/developers/models/grok-imagine-video-1.5>, <https://docs.x.ai/developers/pricing>
- Models discovery, costs, limits, errors, releases: <https://docs.x.ai/developers/rest-api-reference/inference/models>, <https://docs.x.ai/developers/cost-tracking>, <https://docs.x.ai/developers/rate-limits>, <https://docs.x.ai/developers/debugging>, <https://docs.x.ai/developers/release-notes>
- Files and Batch: <https://docs.x.ai/developers/model-capabilities/imagine/files>, <https://docs.x.ai/developers/model-capabilities/imagine/files/inputs>, <https://docs.x.ai/developers/model-capabilities/imagine/files/outputs>, <https://docs.x.ai/developers/files/managing-files>, <https://docs.x.ai/developers/files/public-urls>, <https://docs.x.ai/developers/advanced-api-usage/batch-api>
- API security and legal: <https://docs.x.ai/developers/faq/security>, <https://x.ai/legal/terms-of-service-enterprise>, <https://x.ai/legal/data-processing-addendum>, <https://x.ai/legal/acceptable-use-policy>
- Consumer/X boundary: <https://docs.x.ai/grok/overview>, <https://x.ai/legal/terms-of-service>, <https://x.ai/legal/privacy-policy>
- Native-audio provider claims and 1.5 release: <https://x.ai/news/grok-imagine-api>, <https://x.ai/news/grok-imagine-video-1-5>
- Direct service health: <https://status.x.ai/>

No dedicated first-party technical model card or safety card for Grok Imagine Video was located in the current xAI documentation/research index. Treat architecture, training corpus, demographic performance, watermark implementation, detailed safety evaluation, and benchmark generalization as unknown unless xAI publishes a specific first-party artifact.


