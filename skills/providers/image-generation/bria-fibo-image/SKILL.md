---
name: bria-fibo-image
description: Build and operate rights-aware Bria FIBO and FIBO Lite image-generation workflows with structured prompts, reference images, asynchronous status handling, webhooks, cost gates, and safe artifact downloads. Use when a user asks for Bria/FIBO generation, refinement, inspiration, reproducibility, hosted API integration, or a licensed-data image workflow; do not use for FIBO Edit, video, generic image editing, or third-party FIBO gateways.
---

# Bria FIBO image generation

Use Bria's first-party hosted v2 API unless the user explicitly asks for local weights. Keep local-weight licensing separate from hosted-API terms. Never route a first-party request through fal.ai, Replicate, or another gateway.

## Evidence vocabulary

Use these labels when presenting material facts:

- **Documented fact** - stated by a cited first-party API schema, model card, paper, price page, or legal document.
- **Provider claim** - Bria's performance, training-data, safety, rights, compliance, or indemnity representation; do not restate it as independently verified fact.
- **Operational heuristic** - this skill's conservative recommendation, not a Bria limit or guarantee.
- **Unknown** - not established in the reviewed public first-party material. Ask Bria or inspect the user's executed agreement before relying on it.

Volatile facts and sources in this skill were checked **2026-07-10**. Recheck schemas, pricing, plan limits, model cards, and governing terms before production or procurement decisions.

## Start with a decision record

Before writing code or submitting work, capture:

1. Intent: `generate`, `inspire` from one reference, `refine` a saved structured prompt, or `recreate` from structured prompt plus seed.
2. Delivery: hosted Standard, hosted Lite, or local/on-prem evaluation.
3. Inputs: prompt, one reference image, saved `structured_prompt`, seed, and rights/consent provenance.
4. Output: aspect ratio, `png` or `jpeg`, Standard-only `1MP` or `4MP`, quantity, deadline, and acceptance criteria.
5. Governance: account/plan, permitted use, personal/confidential data classification, geography, retention requirement, and current agreement/DPA.
6. Spend: free-quota consumption or expected charge, maximum calls, maximum USD, and the person approving submission.

If rights, consent, or data classification are unclear, keep the work offline and ask. A public image URL is not evidence of permission.

## Choose the exact route

**Documented fact (v2 OpenAPI):** base URL is `https://engine.prod.bria-api.com/v2`; authentication is the `api_token` request header. Bria's LLM documentation also asks agent clients to send `User-Agent: BriaPlatform/APIdocs/LLMsAgent`, although that requirement is not represented in the endpoint OpenAPI. Include it.

| Need | Route | Bridge/model behavior | Important request fields |
| --- | --- | --- | --- |
| Highest-fidelity image | `POST /image/generate` | Bria documents Gemini 2.5 Flash as the VLM bridge, then full FIBO | `resolution`, `negative_prompt`, `steps_num` available |
| Faster/lower-cost iteration | `POST /image/generate/lite` | Bria documents its open-source FIBO-VLM bridge and FIBO Lite | no `resolution`, `negative_prompt`, or `steps_num` in current schema |
| Structured prompt only | `POST /structured_prompt/generate` | Standard VLM bridge; no image result | no image-output controls |
| Lite structured prompt only | `POST /structured_prompt/generate/lite` | Lite VLM bridge; no image result | no image-output controls |

**Provider claim:** Standard is positioned for maximum interpretation quality; FIBO Lite is positioned for speed and lower cost. The FIBO Lite model card calls it a distilled few-step variant with a quality tradeoff. Benchmark the user's own prompt set before choosing production defaults.

**Privacy consequence:** Standard documentation says Gemini 2.5 Flash participates in prompt/image-to-JSON translation. The reviewed public pages do not establish the exact hosted data path, Google subprocessors/terms, region, retention, or whether zero-data-retention applies. Do not send sensitive, regulated, personal, or confidential inputs until the executed contract/DPA and architecture answer those questions. Lite's hosted route still sends data to Bria; "local/on-prem" requires a separately licensed deployment.

### Current request contract

For the two image-generation routes, provide exactly one of these mutually exclusive combinations:

- `prompt`
- `images` (array, at most one item)
- `images` plus `prompt`
- `structured_prompt`
- `structured_prompt` plus `prompt`

For the two structured-prompt routes, current first-party schemas allow `prompt`, `images`, `images` plus `prompt`, or `structured_prompt` plus a refinement `prompt`; they do **not** allow `structured_prompt` alone. Enforce the selected route's schema rather than flattening the four endpoints into one contract.

For recreation or refinement, supply the saved `seed` with the saved structured prompt. `structured_prompt` is a **string containing JSON**, not a nested request object. Validate that it parses to a JSON object, but preserve the exact returned string as provenance.

Common documented image-generation fields:

- `model_version`: current enum is only `FIBO`. Send it to avoid silently omitting the field, but note that it does not pin an immutable backend revision.
- `aspect_ratio`: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, or `16:9`.
- `seed`: integer; the public OpenAPI gives no min/max. Do not invent a range.
- `sync`: defaults to `false`; use asynchronous operation for production.
- `webhook_url`: optional HTTPS callback for async work.
- `output_type`: `png` or `jpeg`; default `png`.
- `ip_signal`: default `false`; set `true` when IP warnings are useful to the workflow.
- `prompt_content_moderation`, `visual_input_content_moderation`, `visual_output_content_moderation`: current schema defaults to `true`. This skill always sends `true` and does not expose a disable switch.

Standard image-only fields:

- `resolution`: `1MP` or `4MP`, default `1MP`. Bria says 4MP adds about 30 seconds; treat latency as a provider estimate.
- `steps_num`: integer 35-50, default 50.
- `negative_prompt`: optional string.

The current Lite image schema does not accept those three Standard-only fields. The current structured-prompt routes do not accept image-output fields. Reject unknown fields locally instead of hoping the service ignores them.

The OpenAPI accepts an image as a public URL or raw base64 without a `data:image/...;base64,` prefix and lists JPEG/JPG/PNG/WEBP. It documents no FIBO-specific byte, pixel, URL-fetch, animation, metadata, or decompression limits. A client-side cap is an operational heuristic, not a provider limit.

## Compose controllable inputs

For initial text generation, make the prompt an auditable creative specification:

```text
Purpose: ecommerce hero image for a ceramic pour-over set.
Subject: one matte cobalt dripper and matching carafe; accurate circular rim; no people.
Composition: centered three-quarter view, object fills 65% of frame, clear negative space at upper right.
Environment: warm gray seamless studio sweep.
Lighting: large softbox camera-left, gentle rim light, grounded soft shadow.
Camera: eye-level, 70 mm product-photography perspective, all product edges sharp.
Palette/material: cobalt #164B8C ceramic, neutral background, physically plausible glaze.
Text: none. Logos/brands: none.
Acceptance: one product set, no duplicate handles, no floating parts, no clipped silhouette.
```

For typography, put exact visible characters in quotes and repeat them in acceptance criteria. Generated text still needs human proofreading.

For a reference image:

- confirm the user owns or is licensed to submit it, including privacy/publicity permission for people;
- use one image only; strip unnecessary EXIF/GPS when policy permits, while preserving an untouched source separately;
- say which attributes may transfer (palette, lighting, broad composition) and which must not (identity, logo, distinctive protected character, watermark);
- do not describe "inspire" as copyright clearance or guaranteed non-similarity.

For iteration, save the returned structured prompt and seed. Ask for one isolated change, such as "change only the camera angle to a low three-quarter view; preserve subject count, palette, lighting, and layout." Diff the parsed JSON for review, but retain the original byte-for-byte string too. **Provider claim:** Bria describes structured prompt plus seed as deterministic/exact recreation and isolated refinement. **Operational heuristic:** treat it as repeatability intent, not bitwise identity, because the hosted route exposes no immutable model revision; measure perceptual/semantic drift in your own regression set.

## Approval and cost policy

Preparing prompts, payloads, dry runs, validators, or local test fixtures is allowed. Any hosted generation or structured-prompt submission consumes quota and may incur fees.

Before a live request, require all four:

1. `SEND_BRIA_REQUEST=1`
2. `APPROVE_BRIA_PAID_CALL=YES` (also required for free-trial quota)
3. a numeric `BRIA_MAX_COST_USD` at least as large as the dated per-call estimate
4. `BRIA_APPROVED_REQUEST_SHA256` copied from the reviewed dry run, binding approval to the exact route, payload/reference bytes, output-host allowlist, controlled output directory, cost, ceiling, and client job key

Also state route, call count, estimated maximum, and whether a retry could create a second billable job. Do not perform speculative variants. Do not treat a failed client connection as proof that Bria created no job.

**Dated price-page fact (2026-07-10):** Development lists Fibo at `$0.03/image`, Fibo Lite at `$0.02/image`, and Fibo Structured Prompt at `$0.02/call`; Business and Enterprise are custom. The page also advertises 100 free generations. Taxes, credits, negotiated rates, failed-job billing, 4MP treatment, and structured-prompt Lite pricing are not fully resolved by the public schema/page; the account console and executed agreement control.

The example blocks a live 4MP Standard call or Lite structured-prompt call until `BRIA_ESTIMATED_CALL_USD` is set from the live account/contract. This operator-supplied estimate then must fit under `BRIA_MAX_COST_USD`; it is not presented as a public Bria price.

There is a public rate-limit conflict: the API overview lists Free Trial `10`, Starter `60`, and Pro/Enterprise `1000` requests/minute **per endpoint**, while the price comparison shows `10`, `60`, and `150` actions/minute plus custom enterprise throughput. Do not hard-code either as entitlement. Read response headers if present, obey `429`, and confirm the account's live limits.

## Complete hosted example: dry-run first

This single-file Python 3.11+ client uses only the standard library for API calls and Pillow for local image validation (`python -m pip install Pillow`). It supports all four first-party routes, prompt/reference/refine inputs, asynchronous polling, strict URL policies, bounded reads, atomic writes, and a provenance manifest. It never sends by default.

Copy it to `bria_fibo.py`:

```python
from __future__ import annotations

import base64
import hashlib
import ipaddress
import json
import math
import os
import random
import socket
import tempfile
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

BASE = "https://engine.prod.bria-api.com/v2"
API_HOST = "engine.prod.bria-api.com"
USER_AGENT = "BriaPlatform/APIdocs/LLMsAgent"
ROUTES: dict[str, float | None] = {
    "/image/generate": 0.03,
    "/image/generate/lite": 0.02,
    "/structured_prompt/generate": 0.02,
    "/structured_prompt/generate/lite": None,  # public price page is not explicit
}
RATIOS = {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9"}
MAX_JSON_BYTES = 16 * 1024 * 1024       # client heuristic, not a Bria limit
MAX_INPUT_BYTES = 12 * 1024 * 1024      # client heuristic, not a FIBO limit
MAX_OUTPUT_BYTES = 64 * 1024 * 1024     # client heuristic
MAX_PIXELS = 40_000_000                  # client heuristic
POLL_TIMEOUT_S = 600


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError(f"redirect refused ({code}); validate the new URL out of band")


class BriaHTTPError(RuntimeError):
    def __init__(self, status_code: int, message: str, retry_after: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.retry_after = retry_after


class AmbiguousTransportError(RuntimeError):
    pass


OPENER = build_opener(NoRedirect)


def env_bool(name: str) -> bool:
    return os.getenv(name, "") == "1"


def exact_https(url: str, allowed_hosts: set[str], path_prefix: str | None = None) -> str:
    p = urlsplit(url)
    if p.scheme != "https" or not p.hostname or p.username or p.password:
        raise ValueError("URL must be credential-free HTTPS")
    if p.port not in (None, 443) or p.hostname.lower() not in allowed_hosts:
        raise ValueError("URL host/port is not explicitly allowed")
    if path_prefix is not None and not p.path.startswith(path_prefix):
        raise ValueError("URL path is outside the allowed prefix")
    for item in socket.getaddrinfo(p.hostname, 443, type=socket.SOCK_STREAM):
        addr = ipaddress.ip_address(item[4][0])
        if not addr.is_global:
            raise ValueError("URL resolved to a non-public address")
    return url


def read_json_response(resp, cap: int = MAX_JSON_BYTES) -> dict[str, Any]:
    length = resp.headers.get("Content-Length")
    if length and int(length) > cap:
        raise RuntimeError("JSON response exceeds client cap")
    raw = resp.read(cap + 1)
    if len(raw) > cap:
        raise RuntimeError("JSON response exceeds client cap")
    ctype = resp.headers.get_content_type()
    if ctype != "application/json":
        raise RuntimeError(f"unexpected response Content-Type: {ctype}")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("expected a JSON object")
    return value


def api_json(
    method: str,
    url: str,
    token: str,
    body: dict[str, Any] | None = None,
    timeout: float = 60,
) -> dict[str, Any]:
    exact_https(url, {API_HOST}, "/v2/")
    raw = None if body is None else json.dumps(body, separators=(",", ":")).encode()
    if raw is not None and len(raw) > MAX_JSON_BYTES:
        raise ValueError("request exceeds client cap")
    headers = {"api_token": token, "Accept": "application/json", "User-Agent": USER_AGENT}
    if raw is not None:
        headers["Content-Type"] = "application/json"
    req = Request(url, data=raw, headers=headers, method=method)
    try:
        with OPENER.open(req, timeout=timeout) as resp:
            return read_json_response(resp)
    except HTTPError as exc:
        retry_after = exc.headers.get("Retry-After")
        try:
            raw_error = exc.read(16_385)[:16_384]
        finally:
            exc.close()
        try:
            error_data = json.loads(raw_error)
        except (UnicodeDecodeError, json.JSONDecodeError):
            error_data = {}
        if not isinstance(error_data, dict):
            error_data = {}
        error_obj = error_data.get("error")
        error_obj = error_obj if isinstance(error_obj, dict) else {}
        message = str(error_obj.get("message", ""))
        raise BriaHTTPError(
            exc.code,
            f"Bria HTTP {exc.code}; request_id={error_data.get('request_id')!r}; "
            f"error_code={error_obj.get('code')!r}; "
            f"message_sha256={hashlib.sha256(message.encode()).hexdigest() if message else None}",
            retry_after,
        ) from None
    except (TimeoutError, URLError) as exc:
        raise AmbiguousTransportError(
            "transport outcome is ambiguous; do not resubmit a create request automatically; "
            "reconcile by request_id/account logs first"
        ) from exc


def retry_after_seconds(value: str | None) -> float:
    if not value:
        return 0.0
    try:
        seconds = float(value)
    except ValueError:
        try:
            moment = parsedate_to_datetime(value)
            if moment.tzinfo is None:
                moment = moment.replace(tzinfo=timezone.utc)
            seconds = (moment - datetime.now(timezone.utc)).total_seconds()
        except (TypeError, ValueError, OverflowError):
            return 0.0
    return seconds if math.isfinite(seconds) and seconds > 0 else 0.0


def validate_local_image(path: Path, byte_cap: int = MAX_INPUT_BYTES) -> bytes:
    if not path.is_file() or path.stat().st_size > byte_cap:
        raise ValueError("reference is missing or exceeds the client cap")
    raw = path.read_bytes()
    if not (raw.startswith(b"\x89PNG\r\n\x1a\n") or raw.startswith(b"\xff\xd8\xff") or raw.startswith(b"RIFF") and raw[8:12] == b"WEBP"):
        raise ValueError("reference magic is not PNG/JPEG/WEBP")
    try:
        from PIL import Image, UnidentifiedImageError
        Image.MAX_IMAGE_PIXELS = MAX_PIXELS
        with Image.open(path) as im:
            if im.width * im.height > MAX_PIXELS or getattr(im, "n_frames", 1) != 1:
                raise ValueError("reference pixels/frames exceed client policy")
            im.verify()
        with Image.open(path) as im:
            im.load()
    except ImportError as exc:
        raise RuntimeError("install Pillow to validate image inputs") from exc
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("reference image failed full decode") from exc
    return raw


def load_structured_prompt(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("structured_prompt must encode a JSON object")
    return text


def build_payload(route: str) -> dict[str, Any]:
    prompt = os.getenv("BRIA_PROMPT", "").strip()
    ref_path = os.getenv("BRIA_REFERENCE_PATH", "").strip()
    struct_path = os.getenv("BRIA_STRUCTURED_PROMPT_PATH", "").strip()
    if ref_path and struct_path:
        raise ValueError("images and structured_prompt are mutually exclusive")
    payload: dict[str, Any] = {}
    if prompt:
        payload["prompt"] = prompt
    if ref_path:
        payload["images"] = [base64.b64encode(validate_local_image(Path(ref_path))).decode("ascii")]
    if struct_path:
        payload["structured_prompt"] = load_structured_prompt(Path(struct_path))
    if not any(k in payload for k in ("prompt", "images", "structured_prompt")):
        raise ValueError("set BRIA_PROMPT, BRIA_REFERENCE_PATH, or BRIA_STRUCTURED_PROMPT_PATH")
    if route.startswith("/structured_prompt/") and "structured_prompt" in payload and "prompt" not in payload:
        raise ValueError("structured-prompt routes require a prompt when refining a structured_prompt")

    seed_text = os.getenv("BRIA_SEED", "").strip()
    if struct_path and not seed_text:
        raise ValueError("recreation/refinement requires the saved BRIA_SEED")
    if seed_text:
        payload["seed"] = int(seed_text)

    payload.update({
        "sync": False,
        "ip_signal": True,
        "prompt_content_moderation": True,
        "visual_input_content_moderation": True,
    })
    if route.startswith("/image/"):
        ratio = os.getenv("BRIA_ASPECT_RATIO", "1:1")
        if ratio not in RATIOS:
            raise ValueError("unsupported aspect ratio")
        payload.update({
            "model_version": "FIBO",
            "aspect_ratio": ratio,
            "output_type": os.getenv("BRIA_OUTPUT_TYPE", "png"),
            "visual_output_content_moderation": True,
        })
        if payload["output_type"] not in {"png", "jpeg"}:
            raise ValueError("output type must be png or jpeg")
    if route == "/image/generate":
        resolution = os.getenv("BRIA_RESOLUTION", "1MP")
        steps = int(os.getenv("BRIA_STEPS", "50"))
        if resolution not in {"1MP", "4MP"} or not 35 <= steps <= 50:
            raise ValueError("invalid Standard resolution/steps")
        payload.update({"resolution": resolution, "steps_num": steps})
        if os.getenv("BRIA_NEGATIVE_PROMPT"):
            payload["negative_prompt"] = os.environ["BRIA_NEGATIVE_PROMPT"]
    return payload


def poll(request_id: str, token: str) -> dict[str, Any]:
    # Construct from the trusted request_id; never forward api_token to returned arbitrary URLs.
    if not request_id or "/" in request_id or len(request_id) > 256:
        raise RuntimeError("invalid request_id")
    url = f"{BASE}/status/{request_id}"
    deadline = time.monotonic() + POLL_TIMEOUT_S
    delay = 1.0
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(
                f"poll timeout for {request_id}; this does not cancel the job or prove it was not billed"
            )
        try:
            data = api_json("GET", url, token, timeout=max(0.001, min(60.0, remaining)))
        except BriaHTTPError as exc:
            if exc.status_code == 404:
                raise RuntimeError(f"status record is missing or expired for {request_id}") from exc
            if exc.status_code != 429 and exc.status_code < 500:
                raise
            print(f"status retry after HTTP {exc.status_code}")
            delay = max(min(delay * 1.7, 15.0), retry_after_seconds(exc.retry_after))
        except AmbiguousTransportError:
            # GET status is safe to retry; still bound the attempts by the deadline.
            print("status retry after transport failure")
            delay = min(delay * 1.7, 15.0)
        else:
            if data.get("request_id") not in (None, request_id):
                raise RuntimeError("status request_id mismatch")
            status = data.get("status")
            if status == "IN_PROGRESS":
                pass
            elif status == "COMPLETED":
                return data
            elif status in {"ERROR", "UNKNOWN"}:
                err = data.get("error") or {}
                if not isinstance(err, dict):
                    raise RuntimeError(f"Bria job {status} returned an invalid error object")
                message = str(err.get("message", ""))
                raise RuntimeError(
                    f"Bria job {status}: code={err.get('code')!r} "
                    f"message_sha256={hashlib.sha256(message.encode()).hexdigest() if message else None}"
                )
            else:
                raise RuntimeError(f"unknown Bria job status: {status!r}")
            delay = min(delay * 1.7, 15.0)
        remaining = deadline - time.monotonic()
        sleep_for = delay + random.uniform(0, min(delay * 0.2, 1.0))
        if sleep_for >= remaining:
            raise TimeoutError(
                f"poll deadline cannot accommodate retry delay for {request_id}; "
                "this does not cancel the job or prove it was not billed"
            )
        time.sleep(sleep_for)


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            fd = None
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    finally:
        if fd is not None:
            os.close(fd)
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def download_image(
    url: str,
    destination: Path,
    allowed_hosts: set[str],
    expected_content_type: str,
) -> tuple[str, int, str]:
    exact_https(url, allowed_hosts)
    req = Request(url, headers={"Accept": "image/png,image/jpeg", "User-Agent": USER_AGENT}, method="GET")
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=destination.name + ".", dir=destination.parent)
    digest = hashlib.sha256()
    size = 0
    ctype = ""
    try:
        with os.fdopen(fd, "wb") as out:
            fd = None
            with OPENER.open(req, timeout=60) as resp:
                ctype = resp.headers.get_content_type()
                if ctype != expected_content_type:
                    raise RuntimeError(f"unexpected image Content-Type: {ctype}")
                length = resp.headers.get("Content-Length")
                if length and int(length) > MAX_OUTPUT_BYTES:
                    raise RuntimeError("image exceeds client cap")
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > MAX_OUTPUT_BYTES:
                        raise RuntimeError("image exceeds client cap")
                    digest.update(chunk)
                    out.write(chunk)
            out.flush()
            os.fsync(out.fileno())
        with Path(tmp_name).open("rb") as check:
            raw_head = check.read(12)
        if ctype == "image/png" and not raw_head.startswith(b"\x89PNG\r\n\x1a\n"):
            raise RuntimeError("PNG magic mismatch")
        if ctype == "image/jpeg" and not raw_head.startswith(b"\xff\xd8\xff"):
            raise RuntimeError("JPEG magic mismatch")
        validate_local_image(Path(tmp_name), MAX_OUTPUT_BYTES)
        os.replace(tmp_name, destination)
        return digest.hexdigest(), size, ctype
    finally:
        if fd is not None:
            os.close(fd)
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def read_local_json(path: Path) -> dict[str, Any]:
    if path.stat().st_size > MAX_JSON_BYTES:
        raise RuntimeError("local job record exceeds JSON cap")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("local job record is not a JSON object")
    return value


def claim_job(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            fd = None
            json.dump(value, output, indent=2, sort_keys=True)
            output.flush(); os.fsync(output.fileno())
    finally:
        if fd is not None: os.close(fd)


def save_job(path: Path, value: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    route = os.getenv("BRIA_ROUTE", "/image/generate")
    if route not in ROUTES:
        raise ValueError("BRIA_ROUTE is not one of the four first-party FIBO routes")
    payload = build_payload(route)
    public_cost = ROUTES[route]
    override = os.getenv("BRIA_ESTIMATED_CALL_USD", "").strip()
    try: cost = float(override) if override else public_cost
    except ValueError as exc: raise RuntimeError("BRIA_ESTIMATED_CALL_USD must be numeric") from exc
    if route == "/image/generate" and payload.get("resolution") == "4MP" and not override:
        cost = None  # public page does not state whether 4MP changes billing
    if cost is not None and (not math.isfinite(cost) or cost <= 0):
        raise RuntimeError("estimated call cost must be finite and positive")
    if cost is not None and public_cost is not None and cost < public_cost:
        raise RuntimeError("operator estimate cannot undercut the dated public route price")
    try: max_cost = float(os.getenv("BRIA_MAX_COST_USD", "0"))
    except ValueError as exc: raise RuntimeError("BRIA_MAX_COST_USD must be numeric") from exc
    if not math.isfinite(max_cost) or max_cost < 0:
        raise RuntimeError("BRIA_MAX_COST_USD must be finite and non-negative")
    request_sha256 = hashlib.sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    client_job_key = os.getenv("BRIA_CLIENT_JOB_KEY", f"bria-{request_sha256[:20]}")
    output_hosts = {h.strip().lower() for h in os.getenv("BRIA_OUTPUT_HOSTS", "").split(",") if h.strip()}
    out_dir = Path(os.getenv("BRIA_OUTPUT_DIR", "bria-output")).resolve()
    approval_value = {"route": route, "request_sha256": request_sha256,
                      "estimated_call_usd": cost, "max_cost_usd": max_cost,
                      "client_job_key": client_job_key,
                      "output_hosts": sorted(output_hosts), "output_dir": str(out_dir)}
    approval_sha256 = hashlib.sha256(json.dumps(
        approval_value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    input_mode = "+".join(k for k in ("prompt", "images", "structured_prompt") if k in payload)
    print(json.dumps({
        "dry_run": not env_bool("SEND_BRIA_REQUEST"),
        "url": BASE + route,
        "input_mode": input_mode,
        "aspect_ratio": payload.get("aspect_ratio"),
        "resolution": payload.get("resolution"),
        "estimated_max_usd_2026_07_10": cost,
        "maximum_approved_usd": max_cost,
        "client_job_key": client_job_key,
        "request_sha256": request_sha256,
        "approval_sha256": approval_sha256,
        "output_hosts": sorted(output_hosts),
        "output_dir": str(out_dir),
        "moderation": "all applicable stages enabled",
    }, indent=2))
    if not env_bool("SEND_BRIA_REQUEST"):
        print("DRY RUN ONLY: no network request made")
        return
    if os.getenv("APPROVE_BRIA_PAID_CALL") != "YES":
        raise RuntimeError("set APPROVE_BRIA_PAID_CALL=YES after reviewing this request")
    if cost is None:
        raise RuntimeError("set BRIA_ESTIMATED_CALL_USD from the live account/contract before approval")
    if max_cost <= 0 or max_cost < cost:
        raise RuntimeError("BRIA_MAX_COST_USD is below the dated per-call estimate")
    if os.getenv("BRIA_APPROVED_REQUEST_SHA256") != approval_sha256:
        raise RuntimeError("approval hash does not match this exact request, cost, and client job key")
    token = os.getenv("BRIA_API_TOKEN", "")
    if not token:
        raise RuntimeError("BRIA_API_TOKEN is required only for a live call")
    if route.startswith("/image/") and not output_hosts:
        raise RuntimeError("preconfigure exact BRIA_OUTPUT_HOSTS from your Bria deployment/egress policy")

    job_token = hashlib.sha256(client_job_key.encode()).hexdigest()[:20]
    job_dir = out_dir / job_token
    ledger_path = job_dir / "job.json"
    manifest_path = job_dir / "manifest.json"
    ledger_base = {"client_job_key": client_job_key, "route": route,
                   "request_sha256": request_sha256, "approval_sha256": approval_sha256,
                   "estimated_call_usd": cost, "approved_max_cost_usd": max_cost}
    if manifest_path.exists():
        existing_manifest = read_local_json(manifest_path)
        if any(existing_manifest.get(key) != value for key, value in ledger_base.items()):
            raise RuntimeError("existing manifest does not match this approved request")
        print(json.dumps(existing_manifest, indent=2))
        return
    warnings: list[str] = []
    warning_hashes: list[str] = []
    warning_present = False
    if ledger_path.exists():
        existing = read_local_json(ledger_path)
        if any(existing.get(key) != value for key, value in ledger_base.items()):
            raise RuntimeError("existing job ledger does not match this approved request")
        request_id = existing.get("request_id")
        if not isinstance(request_id, str):
            raise RuntimeError(
                "existing create has no confirmed request_id; treat it as ambiguous and do not replay. "
                "Use a new explicit BRIA_CLIENT_JOB_KEY only after operator reconciliation and approval."
            )
        saved_hashes = existing.get("provider_warning_sha256", [])
        if not isinstance(saved_hashes, list) or not all(isinstance(value, str) for value in saved_hashes):
            raise RuntimeError("existing job ledger has invalid warning hashes")
        warning_hashes = saved_hashes
        warning_present = bool(existing.get("provider_warning_present"))
        final = poll(request_id, token)
    else:
        try:
            claim_job(ledger_path, {**ledger_base, "state": "pre_submit",
                                   "request_id": None, "updated_unix": time.time()})
        except FileExistsError as exc:
            raise RuntimeError(
                "another worker claimed this client job key; do not submit; retry later to resume"
            ) from exc
        try:
            initial = api_json("POST", BASE + route, token, payload)  # never auto-retry this create
        except AmbiguousTransportError:
            save_job(ledger_path, {**ledger_base, "state": "ambiguous_create",
                                   "request_id": None, "updated_unix": time.time()})
            raise
        except BriaHTTPError as exc:
            state = "ambiguous_create" if exc.status_code >= 500 else "create_rejected"
            save_job(ledger_path, {**ledger_base, "state": state,
                                   "request_id": None, "http_status": exc.status_code,
                                   "updated_unix": time.time()})
            raise
        request_id = initial.get("request_id")
        if not isinstance(request_id, str) or not request_id or "/" in request_id or len(request_id) > 256:
            save_job(ledger_path, {**ledger_base, "state": "invalid_create_response",
                                   "request_id": None, "updated_unix": time.time()})
            raise RuntimeError("missing or invalid request_id")
        warnings = [initial["warning"]] if isinstance(initial.get("warning"), str) else []
        warning_hashes = [hashlib.sha256(value.encode()).hexdigest() for value in warnings]
        warning_present = bool(warnings)
        save_job(ledger_path, {**ledger_base, "state": "accepted",
                               "request_id": request_id,
                               "provider_warning_present": warning_present,
                               "provider_warning_sha256": warning_hashes,
                               "updated_unix": time.time()})
        if "status_url" in initial:
            expected = f"{BASE}/status/{request_id}"
            if initial["status_url"] != expected:
                raise RuntimeError("unexpected status_url; token was not forwarded")
            final = poll(request_id, token)
        else:
            # Defensive support for a synchronous-shaped response, though this client sends sync=false.
            final = initial
    if isinstance(final.get("warning"), str):
        final_warning_hash = hashlib.sha256(final["warning"].encode()).hexdigest()
        if final_warning_hash not in warning_hashes: warning_hashes.append(final_warning_hash)
        warning_present = True
    if warning_present:
        print(f"Bria returned {len(warning_hashes)} distinct warning(s) for {request_id}; review required")
    result = final.get("result")
    if not isinstance(result, dict):
        raise RuntimeError("completed response has no result object")

    structured = result.get("structured_prompt")
    if isinstance(structured, str):
        parsed = json.loads(structured)
        if not isinstance(parsed, dict):
            raise RuntimeError("returned structured_prompt is not a JSON object")
        atomic_text(job_dir / "structured_prompt.json", structured)
    manifest: dict[str, Any] = {
        "request_id": request_id,
        "route": route,
        "client_job_key": client_job_key,
        "request_sha256": request_sha256,
        "approval_sha256": approval_sha256,
        "seed": result.get("seed"),
        "structured_prompt_sha256": hashlib.sha256(structured.encode()).hexdigest() if isinstance(structured, str) else None,
        "source_url_recorded": False,
        "provider_warning_present": warning_present,
        "provider_warning_sha256": warning_hashes,
        "moderation_flags": {
            "prompt": True,
            "visual_input": True,
            "visual_output": True if route.startswith("/image/") else None,
        },
        "estimated_call_usd_2026_07_10": cost,
        "estimated_call_usd": cost,
        "approved_max_cost_usd": max_cost,
    }
    if route.startswith("/image/"):
        image_url = result.get("image_url")
        if not isinstance(image_url, str):
            raise RuntimeError("completed image response has no image_url")
        suffix = ".png" if payload["output_type"] == "png" else ".jpg"
        expected_type = "image/png" if payload["output_type"] == "png" else "image/jpeg"
        sha256, size, ctype = download_image(
            image_url,
            job_dir / ("image" + suffix),
            output_hosts,
            expected_type,
        )
        manifest.update({"image_sha256": sha256, "image_bytes": size, "content_type": ctype})
    atomic_text(manifest_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    save_job(ledger_path, {**ledger_base, "state": "completed",
                           "request_id": request_id,
                           "provider_warning_present": warning_present,
                           "provider_warning_sha256": warning_hashes,
                           "updated_unix": time.time()})
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
```

Dry-run examples (PowerShell; none sends a request):

```powershell
$env:BRIA_PROMPT='A cobalt ceramic pour-over set on a warm gray studio sweep; no text or logos'
python .\bria_fibo.py

$env:BRIA_ROUTE='/image/generate/lite'
$env:BRIA_PROMPT='Use only the reference palette and soft side lighting; create a distinct unbranded product'
$env:BRIA_REFERENCE_PATH='C:\approved-inputs\reference.png'
python .\bria_fibo.py

$env:BRIA_ROUTE='/image/generate'
$env:BRIA_REFERENCE_PATH=''
$env:BRIA_STRUCTURED_PROMPT_PATH='C:\approved-inputs\structured_prompt.json'
$env:BRIA_SEED='123456'
$env:BRIA_PROMPT='Change only the background to pale warm gray; preserve every object and camera property'
python .\bria_fibo.py
```

Only after a human reviews the dry-run summary, confirms current account price/terms, and approves one call:

```powershell
$env:BRIA_API_TOKEN='<set securely; never paste into logs or source>'
$env:BRIA_OUTPUT_HOSTS='<exact host approved for your Bria result URLs>'
$env:BRIA_MAX_COST_USD='0.03'
$env:BRIA_APPROVED_REQUEST_SHA256='<copy approval_sha256 from the dry run with this same cost ceiling>'
$env:APPROVE_BRIA_PAID_CALL='YES'
$env:SEND_BRIA_REQUEST='1'
python .\bria_fibo.py
```

Unset `SEND_BRIA_REQUEST`, `APPROVE_BRIA_PAID_CALL`, `BRIA_APPROVED_REQUEST_SHA256`, and the API token immediately after the approved call. Do not commit `.env`, prompts containing confidential data, base64 references, signed result URLs, or API responses. The example intentionally logs no token, base64, prompt text, structured prompt, or signed URL.

## Asynchronous and webhook correctness

**Documented fact:** `sync=false` returns HTTP 202 with `request_id` and `status_url`; poll `GET /status/{request_id}` with `api_token`. Terminal statuses are `COMPLETED`, `ERROR`, and `UNKNOWN`; `IN_PROGRESS` continues. A job-level error normally still returns HTTP 200. A missing/expired request can return 404.

The status OpenAPI's success schema currently enumerates only `COMPLETED` even though its prose requires `IN_PROGRESS`; handle the prose-defined state. Never send `api_token` to an unvalidated returned URL. Construct the status URL from the trusted base and request ID, as the example does.

Do not automatically retry `POST` after timeout, connection reset, or ambiguous 5xx: no idempotency-key field or job lookup-by-client-key is documented. Reconcile by captured `request_id`, account logs, or support. Status GETs can use bounded backoff. Poll timeout does not cancel a job; no public cancellation endpoint was found.

For production callbacks, Bria recommends webhooks. The documented contract is:

- raw POST body plus `Bria-Webhook-Id`, `Bria-Webhook-Timestamp`, and `Bria-Webhook-Signature` (`v1=<base64>`);
- HMAC-SHA256 signing key `HMAC-SHA256(api_token, "bria-webhook-signing-v1")`;
- signed message `{webhook_id}.{timestamp}.{raw_body}`;
- acknowledge within 10 seconds;
- up to five delivery attempts over 45 minutes, with possible duplicates; deduplicate on the job/request ID.

Verify the raw bytes before JSON parsing and compare the expected/received signatures with `hmac.compare_digest` or an equivalent constant-time primitive before returning any success response. After verification and durable deduplication, enqueue heavy processing and acknowledge within 10 seconds; perform artifact acquisition and downstream work in the background. Bria's public page does not specify an allowed timestamp skew/replay window. Add a short, monitored freshness window (for example five minutes) as an **operational heuristic**, store processed IDs durably for longer than the 45-minute retry horizon, rotate tokens carefully because they derive the signing key, and confirm clock synchronization. Do not expose the callback to arbitrary payload sizes.

## Artifact and URL safety

Treat `image_url` and `status_url` as credentials-bearing or sensitive even when no query is visible. Public documentation does not state a FIBO output URL lifetime. Download immediately to controlled storage, then hash and inventory the durable copy.

At minimum:

- require HTTPS, default port, exact host allowlist, and public DNS;
- disable redirects; never forward `api_token` to an asset host;
- configure egress/DNS pinning at the network layer for stronger SSRF/rebinding protection;
- cap headers/body/time, check MIME plus file magic, fully decode, enforce pixel/frame limits, and reject archives/HTML/SVG;
- write to a same-directory temporary file, `fsync`, and atomically replace;
- preserve original bytes so C2PA or other provenance metadata is not accidentally stripped; separately verify provenance if required;
- store request ID, route, seed, structured-prompt hash, output hash, moderation/warning disposition, approval, price snapshot, and code/config revision;
- omit signed URLs, tokens, base64, personal data, and raw confidential prompts from ordinary logs.

## Quality and release checks

Evaluate against the written acceptance criteria, not visual appeal alone:

- subject count, anatomy/geometry, spatial relationships, cropping, text spelling, brand/IP leakage;
- reference over-similarity and identity/publicity risk;
- output dimensions/aspect, decode integrity, color mode, alpha behavior, and hash;
- required metadata/provenance behavior after downstream optimization;
- repeatability across saved prompt/seed/model route and drift after backend updates;
- a human review for high-impact, public, regulated, political, or identity-related use.

Moderation success is not permission, factual accuracy, non-infringement, or brand approval. Keep provider moderation enabled and add application policy checks.

## Rights, privacy, and licensing ledger

Record these separately; do not collapse them into "commercially safe":

- **Training data - provider claim:** Bria says FIBO was trained exclusively on licensed data and describes traceability/GDPR/EU AI Act alignment. The paper/model card are Bria-authored evidence, not an independent audit.
- **Hosted output rights/indemnity - contract-specific:** the price page markets standard or full IP/privacy indemnity by plan, while the Legal Lobby says online/free terms have limited warranties and enterprise terms provide extended protection. Governing terms, exclusions, caps, region, use restrictions, and the user's prompt/reference can change the result. Obtain legal review for reliance.
- **Input rights:** the user must own or license prompt/reference content and privacy/publicity rights. Bria's content guidelines prohibit infringing, deceptive, impersonating, unlawful, hateful, pornographic, malicious, and fraudulent uses, among others.
- **Output exclusivity:** older published terms state AI outputs may not be unique. Check the current agreement; never promise exclusivity or registrability.
- **Weights:** `briaai/FIBO` is gated and labeled `bria-fibo`; its model-card metadata links CC BY-NC 4.0 and says non-commercial use only. `briaai/Fibo-lite` is labeled CC BY-NC 4.0 and also says non-commercial only. Commercial local/on-prem use requires separate Bria permission/terms. "Open source" is Bria's wording; do not use it to override the non-commercial restriction or gated conditions. Review the exact accepted terms and all dependencies before download/deployment.
- **Training on customer data:** Bria's Legal Lobby states pilot customer content/output is not used to train or improve generative models absent express written agreement; a March 2025 enterprise document says similarly, with fine-tuning exceptions. Applicability to every current self-service plan is **unknown** without the current executed terms.
- **Retention/deletion:** the July 2024 privacy policy retains personal data as necessary for stated purposes and possible legal needs. Older public terms describe no storage unless documented and deletion within 30 days after termination, but current FIBO job/result retention and URL TTL are **unknown**. Do not promise zero retention.
- **Personal data:** older terms say Customer Content must not include personal data. Current plan-specific treatment is **unknown**. Conservatively prohibit it unless the current contract and DPA explicitly authorize the use.
- **Residency/subprocessors/security:** exact FIBO processing region, customer-selected residency, subprocessor list, encryption details, backups, incident commitments, and status-log retention are **unknown** from the reviewed public pages. Get a DPA/security package and architecture confirmation.

This is operational guidance, not legal advice.

## Current first-party sources

Checked 2026-07-10:

- [Image Generation v2 API and downloadable OpenAPI](https://docs.bria.ai/image-generation/v1-endpoints)
- [Generate Image endpoint](https://docs.bria.ai/image-generation/endpoints/image-generate)
- [Status Service](https://docs.bria.ai/status)
- [Webhook delivery and signing](https://docs.bria.ai/webhooks)
- [API overview: authentication, rate limits, async flow, input encoding](https://docs.bria.ai/)
- [Bria pricing](https://bria.ai/pricing)
- [Bria Legal Lobby](https://bria.ai/legal-lobby)
- [Current Content Guidelines linked by Bria's Legal Lobby (January 2026)](https://drive.google.com/file/d/1JQZzFJ2xR2nAN3ldYCWxwqWz8Jywfb9o/view)
- [Current Online Terms linked by Bria's Legal Lobby (March 2026)](https://drive.google.com/file/d/1KhDEDGZtvKZRtRt3zIJePl_KlnIz8Pg1/view)
- [Bria Content Guidelines (public first-party PDF; June 2024 indexed version)](https://bria.ai/hubfs/Terms%20and%20Conditions/Bria%20-%20AI%20Content%20Guidelines.pdf)
- [Bria Privacy Policy, last updated 2024-07-08](https://bria.ai/hubfs/Terms%20and%20Conditions/Bria-Privacy-Policy%20July%202024.pdf)
- [FIBO model card](https://huggingface.co/briaai/FIBO)
- [FIBO Lite model card](https://huggingface.co/briaai/Fibo-lite)
- [FIBO paper, arXiv:2511.06876](https://arxiv.org/abs/2511.06876)

When documents disagree, prefer the endpoint OpenAPI for wire format, the user's account/contract for commercial and operational entitlements, and the stricter safety/privacy posture until Bria resolves the conflict in writing.
