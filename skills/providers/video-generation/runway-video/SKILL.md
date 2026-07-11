---
name: runway-video
description: Build and operate production-safe Runway API video generation, video editing, and character-performance workflows with native Runway models, explicit paid-call approval, duplicate-create protection, asynchronous task handling, secure media transfer, and evidence-aware governance.
---

# Runway Video

Use this skill for server-side integrations with the documented Runway Developer API at `https://api.dev.runwayml.com`. It covers Runway-native video models and makes partner models, still-image generation, the consumer web app, Recipes, Workflows, Characters, and third-party gateways explicit out-of-scope branches.

Research cutoff: **2026-07-10**.

## Evidence language

Interpret statements in this skill as follows:

- **Fact** â€” stated in a first-party Runway source or visible in the official OpenAPI-generated SDK.
- **Claim** â€” Runway marketing or policy language that may depend on plan or contract.
- **Heuristic** â€” an operational recommendation derived from the facts; validate it for the deployment.
- **Unknown** â€” not established by the reviewed first-party public material. Do not silently fill it in.

When a volatile fact affects money, safety, payload validity, or data governance, re-open the cited first-party page before production use.

## Start with scope, consent, and an execution mode

Before designing a request, obtain all of the following:

1. The desired mode: text-to-video, image-to-video, video edit, or performance transfer.
2. Whether Runway-native models are required or a partner model is acceptable.
3. Output duration, dimensions, delivery format, audio expectation, and iteration budget.
4. Rights to every prompt, image, video, face, voice, performance, mark, and music input.
5. Explicit permission from each depicted or heard person. Runway's Usage Policy prohibits using another person's image, video, or audio without permission.
6. A disclosure/provenance plan when realistic synthetic media could mislead viewers.
7. Data classification, approved regions/subprocessors, retention requirement, and whether the organization's contract actually provides no-training or zero-data-retention terms.
8. One of these execution modes:
   - **Plan/dry-run** â€” default. Validate, price, and print an approval digest. Perform no paid API creation.
   - **Approved create** â€” only after an exact request digest, bounded maximum cost, and explicit environment gates match.
   - **Resume** â€” poll an already recorded task ID; never create a replacement.
   - **Cancel/delete** â€” a separate destructive operation with a separate approval. Never infer it from a timeout.

Refuse requests that lack necessary rights or consent, seek moderation evasion, impersonation, fraud, non-consensual intimate imagery, sexual content involving minors, or another prohibited category. Do not â€œfixâ€ blocked content by obfuscating it.

## Route the request

### Current Runway-native video surface

| Model | Documented API mode | Endpoint | Required anchors | Current public price |
|---|---|---|---|---|
| `gen4.5` | Text â†’ video | `POST /v1/text_to_video` | `promptText`, `ratio`, integer `duration` 2â€“10 | 12 credits/s |
| `gen4.5` | First image + text â†’ video | `POST /v1/image_to_video` | `promptImage`, `promptText`, `ratio`, integer `duration` 2â€“10 | 12 credits/s |
| `gen4_turbo` | First image (+ optional motion text) â†’ video | `POST /v1/image_to_video` | `promptImage`, `ratio`; duration 2â€“10 | 5 credits/s |
| `aleph2` | Existing video + optional text/keyframes â†’ edited video | `POST /v1/video_to_video` | `videoUri`; up to five timed keyframes | 28 credits/s, 56-credit minimum |
| `act_two` | Character image/video + driving performance video â†’ video | `POST /v1/character_performance` | `character`, `reference`, model `act_two` | 5 credits/s; public Act-Two guide states a 3-second minimum |

**Facts:** `gen4.5`, `gen4_turbo`, `aleph2`, and `act_two` are in the current API model catalog. `gen4_aleph` is deprecated and scheduled to sunset on 2026-07-30. Do not start new work on it.

### Native mode details

- **Gen-4.5 text-to-video:** ratios are `1280:720` and `720:1280`. The request schema requires a non-empty prompt of at most 1,000 UTF-16 code units, a ratio, and an integer duration from 2 through 10.
- **Gen-4.5 image-to-video:** ratios are `1280:720`, `720:1280`, `1104:832`, `832:1104`, `1584:672`, and `960:960`. The current SDK schema accepts one first-frame image, either as a URI or an array item with `position: "first"`.
- **Gen-4 Turbo:** image input is required. It supports the six ratios above and any duration from 2 through 10 seconds. It is the lower-cost native image-driven option.
- **Aleph 2.0:** input video must be 2â€“30 seconds, at most 30 fps, and no more than 1080p. Output preserves input resolution up to 1080p. The API accepts optional `promptText`, `seed`, `contentModeration`, `targetAspectRatio`, and up to five keyframes. Each keyframe uses a URI and either absolute `seconds` or normalized `at`; optional edit ranges require all keyframes to use ranges or none to use them.
- **Act-Two:** `character` is `{type: "image"|"video", uri}`, and `reference` is `{type: "video", uri}`. The driving performance is 3â€“30 seconds. The API also accepts `bodyControl`, `expressionIntensity` 1â€“5, `ratio`, `seed`, and `contentModeration`. Body/gesture transfer is intended for character-image inputs; a character video retains its own environmental/camera movement and does not offer the same gesture-control behavior.

**Documented conflict:** the Inputs page also lists Gen-4.5 portrait ratio `672:1584`, but the reviewed current OpenAPI-generated SDK type omits it. Treat that ratio as unresolved rather than guessing; use one of the common values above or recheck the live API reference/SDK before approving `672:1584`.

### Partner models are a separate decision

Runway also exposes partner video models: `seedance2`, `seedance2_fast`, `seedance2_mini`, `veo3`, `veo3.1`, `veo3.1_fast`, `happyhorse_1_0`, and `gemini_omni_flash`. Magnific video upscaling is also a partner capability. They have different schemas, prices, audio behavior, moderation diagnostics, failure modes, subprocessors, and possibly different contractual controls.

Do not silently replace a native model with one of these. If the user chooses a partner model, re-research that model's current first-party Runway schema and provider-specific rights/data conditions, create a new cost formula, and obtain a new approval digest. Runway's enterprise FAQ says its enterprise terms and DPAs cover partner models and that providers have no-training commitments; that is not proof that every self-serve API account has the same terms.

### Explicitly out of scope

- Still-image routes (`/v1/text_to_image`) are a staging option, not video generation. A still-image call is separately billable and requires its own skill/workflow and approval.
- The consumer web app, Explore Mode, Apps, Edit Studio UI, and web credits are not API contracts. Web-app credits and Developer API credits are separate.
- Recipes, published Workflows, real-time Characters, avatar videos, audio-only endpoints, and video upscaling are separate products/endpoints.
- Replicate, fal, ComfyUI wrappers, reverse-engineered endpoints, browser automation, and other gateways are not the Runway Developer API.

## Build a shot specification before a prompt

Record a compact shot spec:

```yaml
intent: "one continuous 6-second product reveal"
mode: "gen4.5 text-to-video"
subject: "matte cobalt travel mug on pale limestone"
action: "a bead of condensation rolls down the mug"
environment: "quiet studio, soft morning window light"
camera: "slow 20-degree dolly arc, medium close-up"
timing: "hold composition for first second, then arc"
style: "natural commercial cinematography, restrained contrast"
ratio: "1280:720"
duration_seconds: 6
audio: "none requested; add licensed sound in post"
continuity_anchors: ["cobalt color", "logo orientation", "limestone texture"]
acceptance: ["single shot", "logo not distorted", "no camera cut"]
```

Then write a direct, positive prompt. For Gen-4.5 text-to-video, describe both what is visible and how it moves. For image-to-video, the image already establishes subject, composition, color, lighting, and style, so emphasize subject, camera, and environmental motion. Add one variable at a time during iteration.

**Heuristics:**

- Prefer one shot and one main action per short clip.
- Use concrete camera language: â€œlocked camera,â€ â€œslow dolly in,â€ â€œhandheld tracking,â€ or â€œoverhead static frame.â€
- Replace negatives with positive outcomes. Use â€œlocked cameraâ€ instead of â€œno camera movement.â€
- Do not ask the model to render critical legal copy or logos reliably; composite approved text and marks in post.
- Keep a fixed seed only when comparing prompt variants. A repeated seed is a similarity aid, not a determinism guarantee.

Example Gen-4.5 text prompt:

> A matte cobalt travel mug stands on pale limestone in soft morning window light. A bead of condensation slowly rolls down its side. The camera performs a restrained 20-degree dolly arc in a single continuous medium close-up. Natural commercial cinematography, crisp product silhouette, gentle background falloff.

For Aleph, use an action verb plus a targeted transformation: â€œRelight the room with cool moonlight while preserving the actor, wardrobe, camera motion, and set layout.â€ Start with the smallest edit. Use a keyframe when exact appearance matters; use `promptText` for motion or a transformation that is not visible in the keyframe.

For Act-Two, quality comes primarily from references rather than prose: one subject, visible face throughout, waist-up or closer, even lighting, no cuts, hands visible at the start if body control is enabled, and natural motion. Begin with `expressionIntensity: 3`. Higher values can add expression and artifacts; lower values can improve stability.

## API and asset contracts

Every API request uses:

```text
Base URL: https://api.dev.runwayml.com
Authorization: Bearer $RUNWAYML_API_SECRET
X-Runway-Version: 2024-11-06
Content-Type: application/json
```

Keep the secret server-side. Never put it in source, logs, prompts, browser code, asset URLs, approval records, or output-download requests. Pin the API base URL; do not accept it from end users.

### Input media

Runway accepts HTTPS URLs, data URIs, and `runway://` ephemeral-upload URIs.

| Input | HTTPS URL | Data URI | Ephemeral upload |
|---|---:|---:|---:|
| Image | 16 MB | 5 MB encoded | 200 MB |
| Video | 32 MB | 16 MB encoded | 200 MB |
| Audio | 32 MB | 16 MB encoded | 200 MB |

HTTPS inputs must use a hostname rather than an IP, respond to `HEAD`, return accurate `Content-Type` and `Content-Length`, and return 200 without redirects. Runway's fetch timeout is documented as 10 seconds. Supported image encodings are JPEG, PNG, and WebP; GIF is unsupported. Supported video containers/codecs are documented on the Inputs page.

**Heuristic:** use a private, exact-host allowlist and short-lived signed object URL when an approved object store already exists. Otherwise use the official ephemeral-upload API. Validate content locally before upload and bind its SHA-256 to the approval. Never let an end user supply an arbitrary fetch URL; that becomes an SSRF and data-exfiltration surface in your application even though Runway applies its own URL restrictions.

`runway://` ephemeral uploads expire after 24 hours, are rate limited, require purchased credits, and are 512 bytesâ€“200 MB. A failed multipart upload must not be retried; create a new upload session. An upload is stateful, so record the URI without putting the API secret or source bytes in logs.

### Output media

A successful task returns an `output` array of one or more URLs. Runway says these URLs expire within 24â€“48 hours and must be downloaded into durable storage; do not expose them as product URLs. The official SDK type notes that retrieving the task again can return fresh URLs.

Treat output URLs as untrusted signed URLs:

- Never attach `Authorization` to them.
- Require HTTPS, no userinfo, default port, public DNS, an exact output-host allowlist, bounded redirects with every hop revalidated, bounded byte count, expected media type, and a container signature.
- Download into a private temporary file, compute SHA-256, run `ffprobe`, fully decode with `ffmpeg -v error -i â€¦ -f null -`, then atomically publish.
- Store task ID, request digest, model, endpoint, prompt hash or protected prompt, source hashes, approval, timestamps, output hash, codec/dimensions/fps/duration/audio-stream presence, and disclosure/rights records. Do not store signed query strings unless a security-reviewed incident workflow needs them.

The public API output page does not promise a single container/codec for every current model. A validator that supports only MP4 must fail closed on other output types rather than renaming them.

## Price before creating

Developer credits are publicly priced at $0.01 each before applicable tax.

Use these formulas for native modes:

```text
gen4.5:      credits = 12 Ã— requested_output_seconds
gen4_turbo:  credits =  5 Ã— requested_output_seconds
aleph2:      credits_upper_bound = max(56, 28 Ã— ceil(input_video_seconds))
act_two:     credits_upper_bound = 5 Ã— max(3, ceil(driving_performance_seconds))
usd_upper_bound = credits_upper_bound Ã— 0.01
```

The Aleph and Act-Two ceiling formulas are conservative **heuristics** for approval when source duration is fractional. Public materials do not establish API rounding behavior for fractional seconds. Aleph's consumer Edit Studio says a ranged edit uses credits only for the range, but the reviewed API pricing page does not state the API's range-billing rule; price the full source duration unless the Developer API documentation or contract confirms otherwise.

Examples:

| Request | Credits | USD before tax |
|---|---:|---:|
| Gen-4.5, 6 s | 72 | $0.72 |
| Gen-4 Turbo, 6 s | 30 | $0.30 |
| Aleph 2.0, 5 s input | 140 | $1.40 |
| Act-Two, 8 s performance | 40 | $0.40 |

Moderated generations cost the same as successful generations. Do not use a paid Runway call as a moderation preflight. Pre-moderate in your application and include moderation failures in the budget.

Runway's public API documents tier-dependent concurrency, rolling 24-hour generation limits, and 30-day spend caps. Over concurrency, a task becomes `THROTTLED` and remains queued; over the daily create limit, creation returns 429. There is no general requests-per-minute cap documented, but this is not permission to create without your own queue, budget, and abuse controls.

## Exact paid approval

A paid request must satisfy all of these at the moment of creation:

1. Dry-run produced a canonical request envelope containing endpoint, model, exact JSON payload, input SHA-256 values, local job key, output policy, current price source date, and a conservative maximum USD cost.
2. A human reviewed the non-redacted request in a protected interface.
3. The human approved that exact envelope digest, not merely â€œuse Runway.â€
4. `SEND_RUNWAY_REQUEST=1` is set.
5. `APPROVE_RUNWAY_PAID_CALL=YES` is set.
6. `RUNWAY_APPROVAL_SHA256` exactly matches the printed SHA-256.
7. `RUNWAY_MAX_COST_USD` is present and is at least the computed upper bound.
8. The create ledger acquired the job key exclusively before the POST.

Any change to prompt, model, endpoint, seed, duration, ratio, references, content-moderation setting, price table, or source hash invalidates approval.

## Duplicate-create control and asynchronous lifecycle

Runway creation returns a task ID. The reviewed API reference and OpenAPI-generated SDK expose no documented idempotency-key parameter for these creation endpoints. Therefore:

- Create a local job record with exclusive-create semantics before the POST.
- Store a request digest and `state: creating` first.
- Send each create POST once. Disable automatic retries for create calls.
- Persist the returned task ID immediately and durably.
- If the client times out, disconnects, crashes, receives malformed success, or gets a 5xx after bytes may have been sent but before a task ID is stored, mark the job **ambiguous**. Do not create again automatically. Reconcile through provider support/usage records or accept a human-authorized possible duplicate under a new job key.
- If a task ID is known, resume `GET /v1/tasks/{id}`. Never replace it with a new generation merely because polling timed out.

The official SDK retries connection errors, 408, 409, 429, and 5xx twice by default. That is convenient for reads, but unsafe for a paid create without a provider idempotency contract. If using the SDK, instantiate the create client with `max_retries=0`; a separate read client may retry safe GETs.

Poll no more often than every five seconds. Add jitter and exponential backoff for retryable read errors. Recognize exactly:

| Status | Meaning | Action |
|---|---|---|
| `PENDING` | accepted, waiting | continue polling |
| `THROTTLED` | stored but not enqueued due to concurrency | continue polling; do not recreate |
| `RUNNING` | active; may include progress | continue polling |
| `SUCCEEDED` | terminal; output URLs available | download and validate immediately |
| `FAILED` | terminal; inspect `failureCode` and sanitized `failure` | do not blindly retry |
| `CANCELLED` | terminal | stop |

`CANCELLED` uses two â€œlâ€ characters in the official SDK schema.

A polling deadline or SDK wait timeout does **not** cancel a task. `DELETE /v1/tasks/{id}` is overloaded: it cancels `PENDING`, `THROTTLED`, or `RUNNING` tasks, but deletes other tasks and their persistent output data. A read-before-delete has a race if the task completes between calls. Never invoke DELETE automatically; require a separate explicit destructive approval that acknowledges possible terminal-task deletion. The public docs do not state the refund/charge rule for cancellation, so cancellation is not a cost-control guarantee.

## Complete production reference

The following standard-library Python client implements Gen-4.5 text-to-video directly and accepts a validated source plan for native image-to-video, Aleph, or Act-Two. It is dry-run by default, binds exact approval to the paid payload, source evidence, price, output host/network policy, and governance evidence, uses an exclusive local ledger, never retries create, safely retries polling, refuses automatic cancellation, downloads without the API bearer token, and validates MP4 with `ffprobe` plus a full `ffmpeg` decode.

Python 3.11+, `ffprobe`, and `ffmpeg` are required. The companion source-plan builder after the payload templates supplies the other native modes without weakening this lifecycle.

```python
#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import http.client
import ipaddress
import json
import os
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
import uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from pathlib import Path

API_ORIGIN = "https://api.dev.runwayml.com"
API_VERSION = "2024-11-06"
CREATE_PATH = "/v1/text_to_video"
PRICE_CREDITS_PER_SECOND = 12
USD_PER_CREDIT = Decimal("0.01")
NONTERMINAL = {"PENDING", "THROTTLED", "RUNNING"}
TERMINAL = {"SUCCEEDED", "FAILED", "CANCELLED"}
MAX_JSON = 256 * 1024
MAX_VIDEO = 512 * 1024 * 1024
MAX_TOOL_OUTPUT = 512 * 1024
UNRESOLVED_GOVERNANCE = [
    "training-use-controlling-terms", "retention-and-deletion-SLA", "zero-data-retention",
    "data-residency", "human-review", "partner-subprocessors", "incident-notification",
]
LEDGER_KEYS = {
    "schemaVersion", "state", "createdAt", "requestHash", "approvalSha256", "model", "endpoint",
    "apiVersion", "promptSha256", "sources", "outputPolicy", "evidence", "price",
    "unresolvedGovernance", "taskId", "submittedAt", "createOutcomeAt", "errorKind", "httpStatus",
    "errorBodySha256", "replayAllowed", "responseSha256", "terminalAt", "failureCode", "artifactError",
    "outputUrlSha256", "stageName", "downloadStartedAt", "artifactStaged", "artifactValidatedAt",
    "storedAt", "artifact", "manifestSha256", "costReconciliation",
}


class APIProblem(Exception):
    def __init__(self, kind: str, status: int | None = None, body_sha256: str | None = None):
        super().__init__(kind)
        self.kind, self.status, self.body_sha256 = kind, status, body_sha256


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


NO_REDIRECT = urllib.request.build_opener(NoRedirect)


def die(message: str) -> "NoReturn":
    raise SystemExit(message)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def fsync_directory(path: Path) -> None:
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".ledger-", suffix=".json", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(canonical(value) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
        fsync_directory(path.parent)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def exclusive_ledger(path: Path, initial: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(canonical(initial) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def read_json(path: Path) -> dict:
    raw = path.read_bytes()
    if len(raw) > MAX_JSON:
        die("ledger exceeds JSON cap")
    value = json.loads(raw)
    if not isinstance(value, dict):
        die("ledger is not an object")
    return value


def exact_hosts(raw: str, name: str) -> tuple[str, ...]:
    result = []
    for item in raw.split(","):
        host = item.strip().rstrip(".").lower()
        if not host:
            continue
        if "*" in host or "/" in host or ":" in host:
            die(f"{name} accepts exact DNS hostnames only")
        try:
            ipaddress.ip_address(host)
        except ValueError:
            pass
        else:
            die(f"{name} rejects IP literals")
        result.append(host)
    if not result:
        die(f"{name} must contain at least one reviewed exact hostname")
    return tuple(sorted(set(result)))


def validate_public_https(url: str, allowed_hosts: set[str]) -> tuple[str, str, list[str]]:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        die("output URL must be HTTPS with a hostname and no userinfo")
    if parsed.port not in (None, 443):
        die("output URL must use default HTTPS port")
    host = parsed.hostname.rstrip(".").lower()
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        die("output URL must not use an IP literal")
    if host not in allowed_hosts:
        die(f"output host {host!r} is not in RUNWAY_OUTPUT_HOSTS; resume after review")
    addresses = []
    for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        address = ipaddress.ip_address(item[4][0])
        if not address.is_global:
            die(f"output host resolves to non-public address {address}")
        addresses.append(str(address))
    if not addresses:
        die("output host did not resolve")
    target = parsed.path or "/"
    if parsed.query:
        target += "?" + parsed.query
    return host, target, sorted(set(addresses))


class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host: str, address: str, timeout: float):
        super().__init__(host, 443, timeout=timeout, context=ssl.create_default_context())
        self.address = address

    def connect(self) -> None:
        raw = socket.create_connection((self.address, 443), self.timeout)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except Exception:
            raw.close()
            raise


def bounded_process(argv: list[str], timeout: int, cap: int = MAX_TOOL_OUTPUT) -> bytes:
    process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chunks: list[bytes] = []
    total = 0
    overflow = threading.Event()
    lock = threading.Lock()

    def drain(stream) -> None:
        nonlocal total
        while True:
            data = stream.read(65536)
            if not data:
                return
            with lock:
                total += len(data)
                if total > cap:
                    overflow.set()
                    process.kill()
                    return
                chunks.append(data)

    threads = [threading.Thread(target=drain, args=(stream,), daemon=True) for stream in (process.stdout, process.stderr)]
    for thread in threads:
        thread.start()
    try:
        code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        die(f"tool timeout: {Path(argv[0]).name}")
    for thread in threads:
        thread.join(timeout=2)
    if overflow.is_set():
        die(f"tool output exceeds cap: {Path(argv[0]).name}")
    if code != 0:
        die(f"tool failed: {Path(argv[0]).name}; diagnosticsSha256={sha256_bytes(b''.join(chunks))}")
    return b"".join(chunks)


def api_json(method: str, path: str, body: dict | None, retry_reads: bool) -> dict:
    secret = os.environ.get("RUNWAYML_API_SECRET", "")
    if not secret:
        die("RUNWAYML_API_SECRET is required for network operations")
    url = API_ORIGIN + path
    headers = {
        "Authorization": f"Bearer {secret}",
        "Accept": "application/json",
        "X-Runway-Version": API_VERSION,
    }
    data = None
    if body is not None:
        data = canonical(body)
        headers["Content-Type"] = "application/json"
    attempts = 5 if retry_reads else 1
    for attempt in range(attempts):
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with NO_REDIRECT.open(request, timeout=30) as response:
                raw = response.read(MAX_JSON + 1)
                if len(raw) > MAX_JSON:
                    raise APIProblem("response-too-large")
                try:
                    value = json.loads(raw or b"{}")
                except json.JSONDecodeError:
                    raise APIProblem("invalid-json", response.status, sha256_bytes(raw))
                if not isinstance(value, dict):
                    raise APIProblem("non-object-json", response.status, sha256_bytes(raw))
                return value
        except urllib.error.HTTPError as exc:
            error_body = exc.read(MAX_JSON + 1)
            body_hash = sha256_bytes(error_body)
            retryable = retry_reads and exc.code in {429, 502, 503, 504}
            if not retryable or attempt + 1 == attempts:
                raise APIProblem("http-error", exc.code, body_hash)
        except APIProblem:
            raise
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if not retry_reads:
                raise APIProblem("transport-" + type(exc).__name__)
            if attempt + 1 == attempts:
                raise APIProblem("poll-transport-" + type(exc).__name__)
        time.sleep(min(30.0, 2 ** attempt) * (1.0 + random.random() * 0.5))
    die("unreachable")


def validate_task_id(value: object) -> str:
    if not isinstance(value, str):
        die("missing task id")
    try:
        uuid.UUID(value)
    except ValueError:
        die("task id is not a UUID")
    return value


def evidence_sha(name: str) -> str:
    value = os.environ.get(name, "").strip().lower()
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        die(f"{name} must be the SHA-256 of the reviewed protected evidence")
    return value


def finite_positive_decimal(name: str) -> Decimal:
    try:
        value = Decimal(os.environ.get(name, ""))
    except InvalidOperation:
        die(f"{name} must be a decimal")
    if not value.is_finite() or value <= 0:
        die(f"{name} must be finite and positive")
    return value


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sanitized_sources(sources: list[dict]) -> list[dict]:
    return [{key: value for key, value in item.items() if key not in {"localPath", "uri"}} for item in sources]


def redacted_payload(payload: dict) -> dict:
    def redact(value, key=""):
        if key in {"uri", "videoUri", "promptImage"} and isinstance(value, str):
            return "sha256:" + sha256_bytes(value.encode("utf-8"))
        if key == "promptText" and isinstance(value, str):
            return "sha256:" + sha256_bytes(value.encode("utf-8"))
        if isinstance(value, dict):
            return {child_key: redact(child, child_key) for child_key, child in value.items()}
        if isinstance(value, list):
            return [redact(child, key) for child in value]
        return value
    return redact(payload)


def reprobe_source(path: Path, kind: str) -> dict:
    with path.open("rb") as stream:
        header = stream.read(32)
    if kind == "image" and not (
        header.startswith(b"\xff\xd8\xff") or header.startswith(b"\x89PNG\r\n\x1a\n")
        or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")
    ):
        die("source image signature is not JPEG, PNG, or WebP")
    raw = bounded_process(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], 30, MAX_JSON
    )
    try:
        metadata = json.loads(raw)
        video = next(item for item in metadata["streams"] if item.get("codec_type") == "video")
        result = {"width": int(video["width"]), "height": int(video["height"])}
        if kind == "video":
            duration = Decimal(str(metadata["format"]["duration"]))
            numerator, denominator = str(video["avg_frame_rate"]).split("/", 1)
            fps = Decimal(numerator) / Decimal(denominator)
            if not duration.is_finite() or duration <= 0 or not fps.is_finite() or fps <= 0:
                die("re-probed source timing is invalid")
            result.update({"durationSeconds": duration, "fps": fps})
    except (KeyError, StopIteration, TypeError, ValueError, InvalidOperation, ZeroDivisionError, json.JSONDecodeError):
        die("source probe metadata is unusable")
    bounded_process(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "null", "-"], 300)
    return result


def load_source_plan(path: Path) -> tuple[str, str, dict, list[dict], Decimal]:
    plan = read_json(path)
    if set(plan) != {"schemaVersion", "model", "endpoint", "payload", "sources", "billingSeconds"}:
        die("source plan has unexpected or missing top-level fields")
    model = plan.get("model")
    endpoint = plan.get("endpoint")
    expected = {
        "gen4.5": "/v1/image_to_video", "gen4_turbo": "/v1/image_to_video",
        "aleph2": "/v1/video_to_video", "act_two": "/v1/character_performance",
    }
    if model not in expected or endpoint != expected[model]:
        die("source plan model/endpoint mismatch")
    payload, sources = plan.get("payload"), plan.get("sources")
    if not isinstance(payload, dict) or payload.get("model") != model or not isinstance(sources, list) or not sources:
        die("source plan payload/sources are invalid")
    if model in {"gen4.5", "gen4_turbo"}:
        image = payload.get("promptImage")
        uris = [image] if isinstance(image, str) else [item.get("uri") for item in image or [] if isinstance(item, dict)]
    elif model == "aleph2":
        uris = [payload.get("videoUri")] + [item.get("uri") for item in payload.get("keyframes", []) if isinstance(item, dict)]
    else:
        uris = [payload.get("character", {}).get("uri"), payload.get("reference", {}).get("uri")]
    if len(uris) != len(sources) or any(not isinstance(uri, str) for uri in uris):
        die("payload URI/source evidence cardinality mismatch")
    allowed_source_keys = {
        "role", "kind", "transport", "localPath", "bytes", "sha256", "uriSha256",
        "contentType", "width", "height", "fps", "durationSeconds", "uploadReceiptSha256",
        "approvedHost", "validatedAt", "uploadState",
    }
    for uri, source in zip(uris, sources):
        if not isinstance(source, dict) or not set(source).issubset(allowed_source_keys):
            die("source evidence contains a non-allowlisted field")
        local = Path(source.get("localPath", "")).resolve()
        if not local.is_file() or local.stat().st_size != source.get("bytes") or file_sha256(local) != source.get("sha256"):
            die("source changed after validation; generate a new plan and approval")
        if source.get("kind") not in {"image", "video"}:
            die("source kind is invalid")
        fresh = reprobe_source(local, source["kind"])
        if fresh["width"] != source.get("width") or fresh["height"] != source.get("height"):
            die("source dimensions differ from plan evidence")
        if source["kind"] == "video":
            try:
                recorded_duration = Decimal(str(source.get("durationSeconds")))
                recorded_fps = Decimal(str(source.get("fps")))
            except InvalidOperation:
                die("recorded source timing is invalid")
            if fresh["durationSeconds"] != recorded_duration or fresh["fps"] != recorded_fps:
                die("source timing differs from plan evidence")
        if source.get("transport") not in {"https", "ephemeral-upload"}:
            die("source transport must be approved HTTPS or ephemeral-upload")
        if source.get("uriSha256") != sha256_bytes(uri.encode("utf-8")):
            die("payload URI does not match its source evidence")
        if source.get("transport") == "ephemeral-upload":
            parsed = urllib.parse.urlsplit(uri)
            if parsed.scheme != "runway" or parsed.query or parsed.fragment or not source.get("uploadReceiptSha256"):
                die("ephemeral upload URI/receipt evidence is invalid")
        else:
            approved_host = source.get("approvedHost")
            if not isinstance(approved_host, str):
                die("HTTPS source lacks its exact approved hostname")
            validate_public_https(uri, {approved_host})
    try:
        seconds = Decimal(str(plan.get("billingSeconds")))
    except InvalidOperation:
        die("source billingSeconds must be decimal")
    if not seconds.is_finite() or seconds <= 0:
        die("source billingSeconds must be finite and positive")
    if model in {"gen4.5", "gen4_turbo"}:
        if len(sources) != 1 or sources[0].get("role") != "first-frame" or sources[0].get("kind") != "image":
            die("image-to-video requires one validated first-frame image")
        if payload.get("ratio") not in {"1280:720", "720:1280", "1104:832", "832:1104", "1584:672", "960:960"}:
            die("image-to-video ratio is invalid")
        if model == "gen4.5" and not isinstance(payload.get("promptText"), str):
            die("Gen-4.5 image-to-video requires promptText")
        requested = payload.get("duration")
        if not isinstance(requested, int) or not 2 <= requested <= 10 or seconds != requested:
            die("image-to-video billingSeconds must equal integer duration 2..10")
        credits = Decimal(12 if model == "gen4.5" else 5) * seconds
    elif model == "aleph2":
        if len(payload.get("keyframes", [])) > 5:
            die("Aleph accepts no more than five keyframes")
        if sources[0].get("role") != "edit-video" or sources[0].get("kind") != "video" or seconds != Decimal(str(sources[0].get("durationSeconds"))):
            die("Aleph billing must equal the re-probed edit-video duration")
        if seconds < 2 or seconds > 30:
            die("Aleph verified source duration must be 2..30 seconds")
        if Decimal(str(sources[0].get("fps"))) > 30 or max(sources[0]["width"], sources[0]["height"]) > 1920 or min(sources[0]["width"], sources[0]["height"]) > 1080:
            die("Aleph source exceeds fps or 1080p constraints")
        credits = max(Decimal(56), Decimal(28) * seconds.to_integral_value(rounding=ROUND_CEILING))
    else:
        character = payload.get("character", {})
        reference = payload.get("reference", {})
        if (character.get("type") not in {"image", "video"} or reference.get("type") != "video"
                or payload.get("expressionIntensity", 3) not in {1, 2, 3, 4, 5}):
            die("Act-Two character/reference/expression fields are invalid")
        performances = [item for item in sources if item.get("role") == "consented-driving-performance" and item.get("kind") == "video"]
        if len(performances) != 1 or seconds != Decimal(str(performances[0].get("durationSeconds"))):
            die("Act-Two billing must equal the re-probed performance duration")
        if seconds < 3 or seconds > 30:
            die("Act-Two verified performance duration must be 3..30 seconds")
        credits = Decimal(5) * max(Decimal(3), seconds.to_integral_value(rounding=ROUND_CEILING))
    return model, endpoint, payload, sources, credits


def poll(task_id: str, deadline_seconds: int) -> dict:
    deadline = time.monotonic() + deadline_seconds
    while True:
        try:
            task = api_json("GET", f"/v1/tasks/{task_id}", None, retry_reads=True)
        except APIProblem as exc:
            die(f"poll failed: {exc.kind}; status={exc.status}; bodySha256={exc.body_sha256}")
        if task.get("id") != task_id:
            die("task response id mismatch")
        status = task.get("status")
        if status in TERMINAL:
            return task
        if status not in NONTERMINAL:
            die(f"unknown task status {status!r}; stop rather than guess")
        if time.monotonic() >= deadline:
            die(f"poll deadline reached for {task_id}; task remains live; resume later")
        time.sleep(5.0 + random.random() * 1.5)


def verify_mp4(path: Path) -> dict:
    size = path.stat().st_size
    if size <= 0 or size > MAX_VIDEO:
        die("artifact byte count is outside policy")
    with path.open("rb") as stream:
        if stream.read(12)[4:8] != b"ftyp":
            die("output lacks ISO BMFF ftyp signature")
        digest = hashlib.sha256()
        stream.seek(0)
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    raw = bounded_process(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], 30, MAX_JSON
    )
    try:
        metadata = json.loads(raw)
    except json.JSONDecodeError:
        die("ffprobe returned invalid JSON")
    streams = metadata.get("streams")
    if not isinstance(streams, list) or not any(item.get("codec_type") == "video" for item in streams):
        die("output has no video stream")
    bounded_process(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "null", "-"], 300)
    video = next(item for item in streams if item.get("codec_type") == "video")
    return {
        "bytes": size,
        "sha256": digest.hexdigest(),
        "qa": {
            "container": metadata.get("format", {}).get("format_name"),
            "videoCodec": video.get("codec_name"),
            "width": video.get("width"), "height": video.get("height"),
            "fps": video.get("avg_frame_rate"),
            "duration": metadata.get("format", {}).get("duration"),
            "audioPresent": any(item.get("codec_type") == "audio" for item in streams),
            "fullDecode": "passed",
        },
    }


def download_mp4(url: str, destination: Path, allowed_hosts: set[str], ledger: Path, record: dict) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = destination.with_name("." + destination.name + ".runway-stage")
    url_hash = sha256_bytes(url.encode("utf-8"))
    expected = record.get("artifactStaged") or record.get("artifact")

    if destination.exists():
        if not isinstance(expected, dict) or not expected.get("sha256"):
            die("existing destination has no durable expected digest; refusing adoption")
        artifact = verify_mp4(destination)
        if artifact["sha256"] != expected["sha256"] or artifact["bytes"] != expected["bytes"]:
            die("existing destination differs from the durable staged artifact")
        return artifact

    if stage.exists() and isinstance(expected, dict) and expected.get("sha256"):
        artifact = verify_mp4(stage)
        if artifact["sha256"] != expected["sha256"] or artifact["bytes"] != expected["bytes"]:
            die("staged artifact differs from the durable expected digest")
        os.replace(stage, destination)
        fsync_directory(destination.parent)
        return artifact

    host, target, addresses = validate_public_https(url, allowed_hosts)
    if record.get("outputUrlSha256") not in (None, url_hash):
        die("task output URL identity changed during artifact recovery")
    record.update({
        "state": "downloading", "outputUrlSha256": url_hash,
        "stageName": stage.name, "downloadStartedAt": record.get("downloadStartedAt") or utc_now(),
    })
    atomic_json(ledger, record)

    artifact = None
    if stage.exists():
        try:
            artifact = verify_mp4(stage)
        except SystemExit:
            stage.unlink()
    if artifact is None:
        connection = PinnedHTTPSConnection(host, addresses[0], timeout=60)
        try:
            connection.request("GET", target, headers={"Accept": "video/mp4", "Host": host})
            response = connection.getresponse()
            if response.status != 200:
                die(f"output returned HTTP {response.status}")
            media_type = response.getheader("Content-Type", "").split(";", 1)[0].strip().lower()
            if media_type != "video/mp4":
                die(f"reference client only accepts video/mp4, got {media_type!r}")
            announced = response.getheader("Content-Length")
            try:
                announced_size = int(announced) if announced is not None else None
            except ValueError:
                die("invalid output Content-Length")
            if announced_size is not None and (announced_size < 0 or announced_size > MAX_VIDEO):
                die("output exceeds byte cap")
            fd = os.open(stage, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            total = 0
            try:
                with os.fdopen(fd, "wb") as stream:
                    fd = None
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        total += len(chunk)
                        if total > MAX_VIDEO:
                            die("output crossed byte cap")
                        stream.write(chunk)
                    stream.flush()
                    os.fsync(stream.fileno())
            except BaseException:
                if stage.exists():
                    stage.unlink()
                raise
            finally:
                if fd is not None:
                    os.close(fd)
        finally:
            connection.close()
        artifact = verify_mp4(stage)

    record.update({"state": "artifact_staged", "artifactStaged": artifact, "artifactValidatedAt": utc_now()})
    atomic_json(ledger, record)
    os.replace(stage, destination)
    fsync_directory(destination.parent)
    return artifact


def main() -> None:
    prompt = os.environ.get("RUNWAY_PROMPT", "").strip()
    ratio = os.environ.get("RUNWAY_RATIO", "1280:720")
    duration_text = os.environ.get("RUNWAY_DURATION", "")
    job_key = os.environ.get("RUNWAY_JOB_KEY", "").strip()
    output = Path(os.environ.get("RUNWAY_OUTPUT", "runway-output.mp4")).resolve()
    if not job_key or not all(character.isalnum() or character in "-_" for character in job_key):
        die("RUNWAY_JOB_KEY must contain only letters, digits, hyphen, underscore")

    output_hosts = exact_hosts(os.environ.get("RUNWAY_OUTPUT_HOSTS", ""), "RUNWAY_OUTPUT_HOSTS")
    rights_sha = evidence_sha("RUNWAY_RIGHTS_RECORD_SHA256")
    moderation_sha = evidence_sha("RUNWAY_MODERATION_RECORD_SHA256")
    qa_plan_sha = evidence_sha("RUNWAY_QA_PLAN_SHA256")
    governance_sha = evidence_sha("RUNWAY_GOVERNANCE_RECORD_SHA256")
    test_record_sha = evidence_sha("RUNWAY_TEST_RECORD_SHA256")

    source_plan_name = os.environ.get("RUNWAY_SOURCE_PLAN", "").strip()
    ledger_root = Path(os.environ.get("RUNWAY_LEDGER_DIR", ".runway-video-jobs")).resolve()
    if source_plan_name:
        model, endpoint, payload, sources, credits = load_source_plan(Path(source_plan_name).resolve())
        prompt = str(payload.get("promptText", ""))
    else:
        if not prompt or len(prompt.encode("utf-16-le")) // 2 > 1000:
            die("RUNWAY_PROMPT must be 1..1000 UTF-16 code units")
        if ratio not in {"1280:720", "720:1280"}:
            die("unsupported Gen-4.5 text-to-video ratio")
        try:
            duration = int(duration_text)
        except ValueError:
            die("RUNWAY_DURATION must be an integer")
        if not 2 <= duration <= 10:
            die("RUNWAY_DURATION must be 2..10")
        model, endpoint, sources = "gen4.5", CREATE_PATH, []
        payload = {"model": model, "promptText": prompt, "ratio": ratio, "duration": duration}
        credits = Decimal(PRICE_CREDITS_PER_SECOND) * Decimal(duration)
    usd = USD_PER_CREDIT * credits
    if not credits.is_finite() or credits <= 0 or not usd.is_finite() or usd <= 0:
        die("computed credits and USD must be finite and positive")
    output_policy = {
        "format": "video/mp4", "maxBytes": MAX_VIDEO, "fullDecode": True,
        "exactHosts": list(output_hosts), "redirects": "reject", "publicDns": True,
        "rejectIpLiterals": True, "dnsPinning": "connect-IP-with-TLS-SNI-and-host-certificate",
    }
    envelope = {
        "apiOrigin": API_ORIGIN,
        "apiVersion": API_VERSION,
        "downloadPolicy": output_policy,
        "endpoint": endpoint,
        "jobKey": job_key,
        "ledgerDir": str(ledger_root),
        "output": str(output),
        "payload": payload,
        "price": {
            "asOf": "2026-07-10",
            "credits": format(credits, "f"),
            "usdBeforeTax": format(usd, ".2f"),
        },
        "sources": sources,
        "evidence": {
            "rightsSha256": rights_sha, "moderationSha256": moderation_sha,
            "qaPlanSha256": qa_plan_sha, "governanceSha256": governance_sha,
            "testRecordSha256": test_record_sha,
        },
    }
    approval = sha256_bytes(canonical(envelope))
    safe_plan = dict(envelope)
    safe_plan["payload"] = redacted_payload(payload)
    safe_plan["sources"] = sanitized_sources(sources)
    print(json.dumps({"approvalSha256": approval, "plan": safe_plan}, indent=2))
    if os.environ.get("RUNWAY_SHOW_FULL_PLAN") == "YES":
        print(json.dumps({"protectedFullEnvelope": envelope}, indent=2))

    if os.environ.get("SEND_RUNWAY_REQUEST") != "1":
        print("DRY RUN: no network request sent", file=sys.stderr)
        return
    if os.environ.get("APPROVE_RUNWAY_PAID_CALL") != "YES":
        die("APPROVE_RUNWAY_PAID_CALL=YES is required")
    if os.environ.get("RUNWAY_APPROVAL_SHA256", "") != approval:
        die("approval digest mismatch")
    maximum = finite_positive_decimal("RUNWAY_MAX_COST_USD")
    if maximum < usd:
        die(f"cost bound {maximum} is below {usd}")

    ledger = ledger_root / f"{job_key}.json"
    request_hash = sha256_bytes(canonical({"endpoint": endpoint, "payload": payload}))
    if ledger.exists():
        record = read_json(ledger)
        if not set(record).issubset(LEDGER_KEYS):
            die("ledger contains a non-allowlisted field")
        if record.get("requestHash") != request_hash:
            die("job key already belongs to a different request")
        if record.get("approvalSha256") != approval:
            die("ledger approval differs from the current exact plan")
        task_id = record.get("taskId")
        if not task_id:
            die(f"{record.get('state', 'ambiguous_create')} ledger has no task id; do not recreate")
        task_id = validate_task_id(task_id)
    else:
        record = {
            "schemaVersion": 1, "state": "creating", "createdAt": utc_now(),
            "requestHash": request_hash, "approvalSha256": approval,
            "model": model, "endpoint": endpoint, "apiVersion": API_VERSION,
            "promptSha256": sha256_bytes(prompt.encode("utf-8")), "sources": sanitized_sources(sources),
            "outputPolicy": output_policy,
            "evidence": envelope["evidence"], "price": envelope["price"],
            "unresolvedGovernance": UNRESOLVED_GOVERNANCE,
        }
        try:
            exclusive_ledger(ledger, record)
        except FileExistsError:
            die("another process acquired this job key")
        try:
            created = api_json("POST", endpoint, payload, retry_reads=False)
        except APIProblem as exc:
            ambiguous = exc.status is None or exc.status >= 500 or exc.status in {408, 409, 429}
            record.update({
                "state": "ambiguous_create" if ambiguous else "create_rejected",
                "createOutcomeAt": utc_now(), "errorKind": exc.kind,
                "httpStatus": exc.status, "errorBodySha256": exc.body_sha256,
                "replayAllowed": False,
            })
            atomic_json(ledger, record)
            die(f"create stopped: {record['state']}; status={exc.status}; bodySha256={exc.body_sha256}")
        try:
            task_id = validate_task_id(created.get("id"))
        except SystemExit:
            record.update({
                "state": "ambiguous_create", "createOutcomeAt": utc_now(),
                "errorKind": "unusable-success", "responseSha256": sha256_bytes(canonical(created)),
                "replayAllowed": False,
            })
            atomic_json(ledger, record)
            die("ambiguous_create: unusable success response; do not recreate")
        record.update({"state": "submitted", "taskId": task_id, "submittedAt": utc_now()})
        atomic_json(ledger, record)

    task = poll(task_id, int(os.environ.get("RUNWAY_POLL_DEADLINE", "900")))
    record.update({"state": task["status"].lower(), "taskId": task_id, "terminalAt": utc_now()})
    if task["status"] == "FAILED":
        record["failureCode"] = task.get("failureCode")
        atomic_json(ledger, record)
        die(f"task failed: {task.get('failureCode')!r}")
    if task["status"] == "CANCELLED":
        atomic_json(ledger, record)
        die("task was cancelled")
    outputs = task.get("output")
    if not isinstance(outputs, list) or len(outputs) != 1 or not isinstance(outputs[0], str):
        record.update({"state": "artifact_blocked", "artifactError": "invalid-output-shape"})
        atomic_json(ledger, record)
        die("reference client requires exactly one output URL")
    artifact = download_mp4(outputs[0], output, set(output_hosts), ledger, record)
    actual_raw = os.environ.get("RUNWAY_ACTUAL_CREDITS", "").strip()
    if actual_raw:
        try:
            actual = Decimal(actual_raw)
        except InvalidOperation:
            die("RUNWAY_ACTUAL_CREDITS must be a decimal")
        if not actual.is_finite() or actual < 0:
            die("RUNWAY_ACTUAL_CREDITS must be finite and non-negative")
        reconciliation = {
            "status": "matched" if actual == credits else "variance-stop-further-creates",
            "estimatedCredits": format(credits, "f"), "actualCredits": format(actual, "f"),
            "varianceCredits": format(actual - credits, "f"),
        }
    else:
        reconciliation = {"status": "pending-stop-further-creates", "estimatedCredits": format(credits, "f")}
    manifest = {
        "schemaVersion": 1, "taskId": task_id, "jobKey": job_key, "state": "stored",
        "timestamps": {
            "created": record.get("createdAt"), "submitted": record.get("submittedAt"),
            "terminal": record.get("terminalAt"), "validated": record.get("artifactValidatedAt"),
            "stored": utc_now(),
        },
        "model": model, "endpoint": endpoint, "apiVersion": API_VERSION,
        "requestHash": request_hash, "approvalSha256": approval,
        "promptSha256": sha256_bytes(prompt.encode("utf-8")), "sources": sanitized_sources(sources),
        "outputPolicy": output_policy, "artifact": dict(artifact, path=str(output)),
        "price": envelope["price"], "costReconciliation": reconciliation,
        "rightsModeration": {"rightsSha256": rights_sha, "moderationSha256": moderation_sha},
        "qa": {"planSha256": qa_plan_sha, "automated": artifact["qa"], "humanReview": "pending"},
        "tests": {
            "recordSha256": test_record_sha, "ffprobe": "passed", "fullDecode": "passed",
            "adversarialSuite": ["non-finite-cost", "host-policy-binding", "DNS-IP-literal", "publish-crash-resume", "sensitive-error-redaction", "ambiguous-create", "tool-output-flood", "concurrency-status"],
        },
        "governance": {"recordSha256": governance_sha, "unresolved": UNRESOLVED_GOVERNANCE},
    }
    manifest_path = output.with_suffix(output.suffix + ".manifest.json")
    atomic_json(manifest_path, manifest)
    record.update({
        "state": "stored", "storedAt": manifest["timestamps"]["stored"],
        "artifact": artifact, "manifestSha256": sha256_bytes(canonical(manifest)),
        "costReconciliation": reconciliation,
    })
    atomic_json(ledger, record)
    print(json.dumps({"taskId": task_id, "artifact": dict(artifact, path=str(output)), "manifest": str(manifest_path)}, indent=2))


if __name__ == "__main__":
    main()
```

Example dry-run in PowerShell:

```powershell
$env:RUNWAY_PROMPT = 'A matte cobalt travel mug stands on pale limestone in soft morning window light. A bead of condensation slowly rolls down its side. The camera performs a restrained 20-degree dolly arc in a single continuous medium close-up.'
$env:RUNWAY_RATIO = '1280:720'
$env:RUNWAY_DURATION = '6'
$env:RUNWAY_JOB_KEY = 'mug-reveal-v1'
$env:RUNWAY_OUTPUT = 'C:\approved-output\mug-reveal-v1.mp4'
$env:RUNWAY_OUTPUT_HOSTS = '<reviewed exact output hostname>'
$env:RUNWAY_RIGHTS_RECORD_SHA256 = '<64-hex protected rights-record digest>'
$env:RUNWAY_MODERATION_RECORD_SHA256 = '<64-hex protected moderation-record digest>'
$env:RUNWAY_QA_PLAN_SHA256 = '<64-hex protected QA-plan digest>'
$env:RUNWAY_GOVERNANCE_RECORD_SHA256 = '<64-hex protected governance-record digest>'
$env:RUNWAY_TEST_RECORD_SHA256 = '<64-hex protected adversarial-test-record digest>'
python .\runway_video.py
```

Expected cost: 72 credits, $0.72 before tax. Copy the printed digest only after reviewing the protected full envelope, then make the deliberate paid invocation:

```powershell
$env:SEND_RUNWAY_REQUEST = '1'
$env:APPROVE_RUNWAY_PAID_CALL = 'YES'
$env:RUNWAY_APPROVAL_SHA256 = '<exact digest from this unchanged plan>'
$env:RUNWAY_MAX_COST_USD = '0.72'
$env:RUNWAYML_API_SECRET = '<secret injected by a secret manager>'
python .\runway_video.py
```

Do not put the actual secret in shell history. In production, inject it from the process supervisor or secret manager.

### Native payload templates

These are complete request bodies as of the research cutoff. They are not permission to send a paid request; run them through the same plan, source-hash, budget, approval, and ledger controls.

Gen-4.5 first-frame image-to-video, 5 seconds, $0.60 before tax:

```json
{
  "model": "gen4.5",
  "promptImage": [{"uri": "runway://APPROVED_UPLOAD", "position": "first"}],
  "promptText": "The subject lifts the mug once and takes a small sip. The locked camera holds a medium close-up. Steam drifts gently upward in soft morning light.",
  "ratio": "1104:832",
  "duration": 5,
  "seed": 18421,
  "contentModeration": {"publicFigureThreshold": "auto"}
}
```

Gen-4 Turbo image-to-video, 6 seconds, $0.30 before tax:

```json
{
  "model": "gen4_turbo",
  "promptImage": "runway://APPROVED_UPLOAD",
  "promptText": "The fabric ripples in a light breeze while the camera slowly pushes in.",
  "ratio": "1280:720",
  "duration": 6,
  "contentModeration": {"publicFigureThreshold": "auto"}
}
```

Aleph 2.0 with one absolute keyframe, priced conservatively from the entire verified input duration:

```json
{
  "model": "aleph2",
  "videoUri": "runway://APPROVED_VIDEO_UPLOAD",
  "promptText": "Relight the room with cool moonlight while preserving the performer, wardrobe, camera motion, and set layout.",
  "keyframes": [
    {"uri": "runway://APPROVED_KEYFRAME_UPLOAD", "seconds": 2.5}
  ],
  "seed": 18421,
  "contentModeration": {"publicFigureThreshold": "auto"}
}
```

Act-Two with a character image and an 8-second driving performance, upper bound $0.40 before tax:

```json
{
  "model": "act_two",
  "character": {"type": "image", "uri": "runway://CONSENTED_CHARACTER_IMAGE"},
  "reference": {"type": "video", "uri": "runway://CONSENTED_DRIVING_PERFORMANCE"},
  "bodyControl": true,
  "expressionIntensity": 3,
  "ratio": "720:1280",
  "seed": 18421,
  "contentModeration": {"publicFigureThreshold": "auto"}
}
```

### Runnable source pipeline for image-to-video, Aleph, and Act-Two

Save the production reference as `runway_video.py` and the following companion as `runway_source_plan.py`. The companion validates and fully decodes local mirror files, checks a reviewed HTTPS source with DNS pinning and a no-redirect `HEAD`, or requires a receipt digest for an already completed official ephemeral upload. It writes a source plan; `RUNWAY_SOURCE_PLAN` makes the production client re-hash every local mirror, recompute the conservative price, bind the exact source payload/evidence into approval, and then use the same exclusive create, poll, and crash-resumable artifact lifecycle. The upload itself is intentionally a separately recorded stateful operation: a failed multipart upload gets a new session and never a blind retry.

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import urllib.parse
from decimal import Decimal
from pathlib import Path

import runway_video as rv

IMAGE_RATIOS = {"1280:720", "720:1280", "1104:832", "832:1104", "1584:672", "960:960"}


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        rv.die(f"{name} is required")
    return value


def probe_local(path: Path, kind: str) -> dict:
    if not path.is_file():
        rv.die(f"missing local {kind} mirror")
    with path.open("rb") as stream:
        header = stream.read(32)
    if kind == "image" and not (
        header.startswith(b"\xff\xd8\xff") or header.startswith(b"\x89PNG\r\n\x1a\n")
        or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")
    ):
        rv.die("image must be JPEG, PNG, or WebP by signature")
    raw = rv.bounded_process(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], 30, rv.MAX_JSON
    )
    try:
        metadata = json.loads(raw)
    except json.JSONDecodeError:
        rv.die("ffprobe returned invalid JSON")
    streams = metadata.get("streams", [])
    video = next((item for item in streams if item.get("codec_type") == "video"), None)
    if not video:
        rv.die(f"{kind} mirror has no visual stream")
    rv.bounded_process(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-f", "null", "-"], 300)
    result = {"width": video.get("width"), "height": video.get("height")}
    if not all(isinstance(result[key], int) and result[key] > 0 for key in ("width", "height")):
        rv.die("invalid source dimensions")
    if kind == "video":
        try:
            duration = Decimal(str(metadata.get("format", {}).get("duration")))
            numerator, denominator = str(video.get("avg_frame_rate", "0/1")).split("/", 1)
            fps = Decimal(numerator) / Decimal(denominator)
        except Exception:
            rv.die("video duration/fps are unusable")
        if not duration.is_finite() or duration <= 0 or not fps.is_finite() or fps <= 0:
            rv.die("video duration/fps must be finite and positive")
        result.update({"durationSeconds": format(duration, "f"), "fps": format(fps, "f")})
    return result


def checked_source(index: int, role: str, kind: str, input_hosts: set[str]) -> tuple[str, dict]:
    prefix = f"RUNWAY_SOURCE_{index}_"
    local = Path(required(prefix + "LOCAL")).resolve()
    uri = required(prefix + "URI")
    details = probe_local(local, kind)
    size = local.stat().st_size
    parsed = urllib.parse.urlsplit(uri)
    if parsed.scheme == "runway":
        if not uri.startswith("runway://") or len(uri) > 2048 or parsed.query or parsed.fragment:
            rv.die("invalid ephemeral-upload URI")
        receipt = required(prefix + "UPLOAD_RECEIPT_SHA256").lower()
        if len(receipt) != 64 or any(character not in "0123456789abcdef" for character in receipt):
            rv.die("upload receipt must be a SHA-256")
        transport, host = "ephemeral-upload", None
        cap = 200 * 1024 * 1024
    elif parsed.scheme == "https":
        host, target, addresses = rv.validate_public_https(uri, input_hosts)
        connection = rv.PinnedHTTPSConnection(host, addresses[0], timeout=10)
        try:
            connection.request("HEAD", target, headers={"Host": host})
            response = connection.getresponse()
            if response.status != 200:
                rv.die(f"source HEAD returned HTTP {response.status}; redirects are rejected")
            announced = response.getheader("Content-Length")
            media_type = response.getheader("Content-Type", "").split(";", 1)[0].lower()
            expected_types = {"image": {"image/jpeg", "image/png", "image/webp"}, "video": {"video/mp4", "video/quicktime", "video/webm"}}
            if announced is None or int(announced) != size or media_type not in expected_types[kind]:
                rv.die("source HEAD length/type does not match the validated local mirror")
        finally:
            connection.close()
        receipt, transport = None, "https"
        cap = (16 if kind == "image" else 32) * 1024 * 1024
    else:
        rv.die("source URI must be reviewed HTTPS or runway:// ephemeral upload")
    if size < 512 or size > cap:
        rv.die("source byte count is outside the selected transport limit")
    evidence = {
        "role": role, "kind": kind, "transport": transport, "localPath": str(local),
        "bytes": size, "sha256": rv.file_sha256(local), "uriSha256": rv.sha256_bytes(uri.encode()),
        "contentType": "locally-probed", "validatedAt": rv.utc_now(), **details,
    }
    if host:
        evidence["approvedHost"] = host
    if receipt:
        evidence.update({"uploadReceiptSha256": receipt, "uploadState": "completed-do-not-retry-session"})
    return uri, evidence


def main() -> None:
    mode = required("RUNWAY_SOURCE_MODE")
    input_hosts = set(rv.exact_hosts(os.environ.get("RUNWAY_INPUT_HOSTS", ""), "RUNWAY_INPUT_HOSTS"))
    prompt = os.environ.get("RUNWAY_PROMPT", "").strip()
    ratio = os.environ.get("RUNWAY_RATIO", "1280:720")
    if ratio not in IMAGE_RATIOS:
        rv.die("unsupported ratio")
    if len(prompt.encode("utf-16-le")) // 2 > 1000:
        rv.die("prompt exceeds 1,000 UTF-16 code units")
    sources = []
    if mode in {"gen45-image", "gen4-turbo"}:
        uri, source = checked_source(1, "first-frame", "image", input_hosts)
        sources.append(source)
        duration = int(required("RUNWAY_DURATION"))
        if not 2 <= duration <= 10:
            rv.die("duration must be 2..10")
        model = "gen4.5" if mode == "gen45-image" else "gen4_turbo"
        if model == "gen4.5" and not prompt:
            rv.die("Gen-4.5 image-to-video requires RUNWAY_PROMPT")
        endpoint = "/v1/image_to_video"
        payload = {"model": model, "promptImage": uri, "ratio": ratio, "duration": duration, "contentModeration": {"publicFigureThreshold": "auto"}}
        if prompt:
            payload["promptText"] = prompt
        billing = Decimal(duration)
    elif mode == "aleph2":
        uri, source = checked_source(1, "edit-video", "video", input_hosts)
        sources.append(source)
        billing = Decimal(source["durationSeconds"])
        if (billing < 2 or billing > 30 or Decimal(source["fps"]) > 30
                or max(source["width"], source["height"]) > 1920
                or min(source["width"], source["height"]) > 1080):
            rv.die("Aleph source must be 2..30 s, <=30 fps, and <=1080p")
        payload = {"model": "aleph2", "videoUri": uri, "contentModeration": {"publicFigureThreshold": "auto"}}
        if prompt:
            payload["promptText"] = prompt
        if os.environ.get("RUNWAY_SOURCE_2_LOCAL"):
            key_uri, key_source = checked_source(2, "absolute-keyframe", "image", input_hosts)
            sources.append(key_source)
            at = finite = Decimal(required("RUNWAY_KEYFRAME_SECONDS"))
            if not finite.is_finite() or finite < 0 or finite > billing:
                rv.die("keyframe seconds must be finite and inside the source")
            payload["keyframes"] = [{"uri": key_uri, "seconds": float(at)}]
        model, endpoint = "aleph2", "/v1/video_to_video"
    elif mode == "act-two":
        character_kind = required("RUNWAY_CHARACTER_TYPE")
        if character_kind not in {"image", "video"}:
            rv.die("RUNWAY_CHARACTER_TYPE must be image or video")
        character_uri, character = checked_source(1, "consented-character", character_kind, input_hosts)
        performance_uri, performance = checked_source(2, "consented-driving-performance", "video", input_hosts)
        sources.extend([character, performance])
        billing = Decimal(performance["durationSeconds"])
        if billing < 3 or billing > 30:
            rv.die("Act-Two performance must be 3..30 seconds")
        intensity = int(os.environ.get("RUNWAY_EXPRESSION_INTENSITY", "3"))
        if not 1 <= intensity <= 5:
            rv.die("expression intensity must be 1..5")
        payload = {
            "model": "act_two", "character": {"type": character_kind, "uri": character_uri},
            "reference": {"type": "video", "uri": performance_uri}, "bodyControl": character_kind == "image",
            "expressionIntensity": intensity, "ratio": ratio, "contentModeration": {"publicFigureThreshold": "auto"},
        }
        model, endpoint = "act_two", "/v1/character_performance"
    else:
        rv.die("RUNWAY_SOURCE_MODE must be gen45-image, gen4-turbo, aleph2, or act-two")
    plan = {"schemaVersion": 1, "model": model, "endpoint": endpoint, "payload": payload, "sources": sources, "billingSeconds": format(billing, "f")}
    rv.atomic_json(Path(required("RUNWAY_SOURCE_PLAN_OUT")).resolve(), plan)
    print(json.dumps({"sourcePlanSha256": rv.sha256_bytes(rv.canonical(plan)), "sourceCount": len(sources)}, indent=2))


if __name__ == "__main__":
    main()
```

Set `RUNWAY_SOURCE_PLAN` to the generated file before the dry run. Also set the exact output-host policy and all four protected evidence digests before computing approval. Never place source URIs, signed queries, faces, prompts, or upload handles in ordinary logs; the companion prints only a plan digest and count.

`publicFigureThreshold: "low"` is documented as less strict about recognizable public figures. It is not a consent bypass and must never be used to defeat policy or rights checks. Default to `auto`; require a documented authorized use and renewed approval for `low`.

## Failure handling

Use `failureCode` before the human-readable `failure` string:

- `SAFETY.*` and `INPUT_PREPROCESSING.SAFETY.TEXT` â€” policy/moderation failure. Do not retry the same request or obfuscate it. Review your own screening; repeated moderated requests can suspend the account and are still charged.
- `ASSET.INVALID` â€” validate source availability, format, size, dimensions, duration, fps, and aspect ratio. Correct the asset under a new approval digest.
- `INPUT_PREPROCESSING.INTERNAL` â€” input processing failed. Verify the asset first; if retrying is justified, use a new explicit paid approval and job key.
- `THIRD_PARTY.UNAVAILABLE` â€” relevant to partner models. Wait or choose a model only with user authorization and a new digest.
- `INTERNAL.BAD_OUTPUT`, `INTERNAL`, or null â€” may be transient, but a retry is another paid creation unless Runway has refunded it. Check credit usage and obtain a new approval.

Runway's web help says ordinary generation errors are refunded, while API moderation docs explicitly say moderated generations cost the same as success. Do not generalize the web-app refund statement to every API failure code. The public API docs do not give a complete refund matrix; reconcile credits before retrying.

## Rights, audio, provenance, and data governance

### Rights and likeness

Runway's Terms say it does not claim ownership of user inputs or outputs and does not restrict commercial use of outputs, subject to compliance. That is a provider/user allocation, not a warranty of copyrightability, exclusivity, trademark clearance, publicity rights, music rights, or freedom from similarity to third-party works.

Maintain a rights ledger that identifies every source, licensor, license scope, consent, territory, term, model release, voice release, and intended distribution. For Act-Two, both the depicted character and the driving performer/voice require permission. Do not use a living artist's style when prohibited by Runway's Usage Policy.

### Audio

The current API schemas for `gen4.5` and `gen4_turbo` expose no audio-generation toggle. Consumer UI or marketing material mentioning native audio is not an API contract. Plan licensed sound design in post unless a refreshed API schema adds an audio field.

Act-Two's product guide says the driving performance transfers speech/audio characteristics, but the API schema exposes no independent audio switch. Inspect the returned streams and do not promise lip-sync, voice identity, or audio retention before a test with consented material. Partner models have their own audio flags and prices.

### Attribution and disclosure

API-integrated end-user interfaces must prominently show â€œPowered by Runwayâ€ and link to `runwayml.com` under the Terms and attribution page. Runway's consumer usage-rights FAQ says finished works do not need formal credit; that does not override the API integration UI obligation.

Runway says it implements C2PA provenance signals, but the reviewed public API output contract does not promise that every downloaded file carries C2PA. Preserve any embedded metadata, avoid destructive transcoding before capture, inspect with a C2PA verifier when required, and store your own signed provenance manifest. Clearly label realistic synthetic people/events where context could mislead.

### Privacy and retention

Runway's public API marketing page claims â€œNo training on your data,â€ while the standard Terms state that inputs and outputs may be used to train and improve models. A 2026 Runway Dev announcement describes contractual no-training commitments and zero-data-retention support, and enterprise pages describe separate protections. These public statements are not fully reconciled for an arbitrary self-serve account.

Treat training use, retention, zero retention, residency, deletion SLA, human review, partner subprocessors, and incident notification as **unknown until the controlling order form, Terms version, and DPA for the organization resolve them**. Do not send confidential, regulated, biometric, minor, or client-restricted media on the strength of a marketing heading.

The Privacy Policy treats submitted faces and voices as potentially biometric data and says face scans/voiceprints are retained no longer than the earlier of purpose completion or three years after last interaction; it also says certain customer-directed processing is governed by customer agreements rather than the public Privacy Policy. Obtain required biometric notice/consent, complete a DPIA where applicable, minimize sources, and set deletion schedules in both provider and local systems.

Deleting a task uses the same DELETE endpoint as cancellation and makes the task unavailable. This is not documented as erasing every log, safety record, backup, or legal-retention copy. Use contractual deletion mechanisms for regulated erasure.

## Production acceptance checklist

- Native versus partner model choice is explicit.
- Current model ID, endpoint, API version, schema, price, and sunset status were rechecked.
- Every input is consented, licensed, locally validated, hashed, and free of unnecessary sensitive data.
- Prompt and reference strategy match the mode.
- Dry-run cost and protected full payload were reviewed.
- Exact approval digest, maximum cost, and exclusive job key are present.
- Create retries are disabled; ambiguous creation cannot automatically recreate.
- Task ID is durably stored; polling handles `THROTTLED` and `CANCELLED` correctly.
- Poll timeout does not cancel. DELETE has a separate destructive approval.
- Moderation is performed before the paid call; blocked requests are not evaded.
- Output is downloaded before expiry, host/size/type validated, fully decoded, hashed, and durably stored.
- Audio streams, duration, fps, dimensions, continuity, artifacts, and acceptance criteria are reviewed by a human.
- â€œPowered by Runwayâ€ appears in applicable API integration UI.
- Rights, consent, disclosure, C2PA inspection, provenance, data terms, retention, and deletion evidence are recorded.
- Credit usage is reconciled against the estimate; discrepancies stop further creates.

## First-party sources

Accessed 2026-07-10 unless noted:

- [Available AI Models](https://docs.dev.runwayml.com/guides/models/)
- [API Changelog](https://docs.dev.runwayml.com/api-details/api_changelog/)
- [API Pricing](https://docs.dev.runwayml.com/guides/pricing/)
- [Using the API](https://docs.dev.runwayml.com/guides/using-the-api/)
- [API Reference](https://docs.dev.runwayml.com/api/)
- [Official Python SDK and OpenAPI-generated types](https://github.com/runwayml/sdk-python)
- [SDK task polling guidance](https://docs.dev.runwayml.com/api-details/sdks/)
- [API Inputs](https://docs.dev.runwayml.com/assets/inputs/)
- [Ephemeral Uploads](https://docs.dev.runwayml.com/assets/uploads/)
- [API Outputs](https://docs.dev.runwayml.com/assets/outputs/)
- [Content Moderation](https://docs.dev.runwayml.com/api-details/moderation/)
- [Task Failures](https://docs.dev.runwayml.com/errors/task-failures/)
- [HTTP Errors](https://docs.dev.runwayml.com/api-details/errors/)
- [Usage Tiers](https://docs.dev.runwayml.com/usage/tiers/)
- [Attribution](https://docs.dev.runwayml.com/usage/attribution/)
- [Gen-4.5 Prompting](https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5)
- [Text-to-Video Prompting Guide](https://help.runwayml.com/hc/en-us/articles/42460036199443-Text-to-Video-Prompting-Guide)
- [Aleph 2.0 Prompting Guide](https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide)
- [Act-Two Guide](https://help.runwayml.com/hc/en-us/articles/42311337895827-Performance-Capture-with-Act-Two)
- [Reference Media Guidelines](https://docs.dev.runwayml.com/recipes/reference-media/)
- [Terms of Use](https://runwayml.com/terms-of-use)
- [Usage Policy](https://runwayml.com/safety/usage-policy)
- [Privacy Policy](https://runwayml.com/privacy-policy)
- [Runway Security](https://runwayml.com/data-security)
- [Runway Dev announcement](https://runwayml.com/news/introducing-runway-dev)
- [Enterprise third-party-model FAQ](https://help.runwayml.com/hc/en-us/articles/51248305153683-Enterprise-FAQ-Third-party-Models-in-Runway)
- [Usage Rights FAQ](https://help.runwayml.com/hc/en-us/articles/18927776141715-Usage-rights)
- [Safety and provenance](https://runwayml.com/safety)


