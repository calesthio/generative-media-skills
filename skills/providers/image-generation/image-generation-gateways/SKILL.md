---
name: image-generation-gateways
description: Select, integrate, and operate multi-model image-generation gateways with model-specific schema discovery, version policy, asynchronous jobs, webhooks, spend approval, safe inputs and artifacts, data-governance review, and billing observability. Use for comparing or building against fal.ai, Replicate, or Together AI image APIs, including controlled failover; do not use for direct model-provider APIs, local inference, training, dedicated endpoint provisioning, video generation, or general image editing.
---

# Image generation through gateways

A gateway standardizes account access, not model behavior. Keep gateway, model publisher, model/version, execution path, schema, price, safety behavior, and downstream terms as separate facts in every plan and ledger row.

This skill covers three current multi-model serverless gateways:

- **fal.ai Model APIs**: direct or persistent queue calls to model endpoint IDs, with queue status, cancellation, and signed webhooks.
- **Replicate predictions**: prediction resources around official, community, marketplace, or version-pinned models.
- **Together AI serverless images**: a synchronous OpenAI-compatible image endpoint spanning models with different parameter subsets.

These gateways were selected because their first-party contracts expose three materially different operating patterns. Do not add another gateway merely because it offers the same model name. Research its control plane, billing unit, data path, lifecycle, schema, and terms first.

Volatile facts here were checked **2026-07-10**. Use four evidence labels in user-facing work:

- **FACT**: directly documented by the cited gateway, model publisher, or governing terms.
- **PROVIDER CLAIM**: a quality, commercial-use, training, security, equivalence, or infrastructure representation that was not independently audited here.
- **HEURISTIC**: a conservative production practice in this skill, not a gateway limit.
- **UNKNOWN**: public first-party evidence was insufficient; resolve through the account, contract, DPA, model publisher, or support.

## Build the routing record before code

Capture a signed-off record with:

1. production intent and image acceptance tests;
2. gateway and account/project;
3. exact endpoint/model ID, publisher, official/community/partner status, and version policy;
4. schema URL or API-discovered schema plus retrieval time and hash;
5. complete input fields, reference provenance, output count/format/size, safety controls, and seed;
6. execution path: sync, queue/poll, or webhook;
7. billing unit, unit price snapshot, estimated maximum, credits/discounts, and approver;
8. input/output rights, model terms, gateway terms, downstream processor/data path, retention, training setting, and region;
9. artifact destination, byte/pixel limits, provenance fields, and deletion schedule;
10. retry, reconciliation, cancellation, and failover policy.

If any consequential entry is missing, prepare a dry run and stop before submission.

## Select for the workload, not the logo

| Requirement | fal.ai | Replicate | Together AI |
| --- | --- | --- | --- |
| Long-running serverless control | Queue returns request/status/response/cancel URLs; webhooks available | Async prediction is default; poll, cancel, or webhook | Current `/v1/images/generations` is synchronous; no image-job resource documented |
| Version behavior | Endpoint ID does not by itself prove an immutable model revision | Community predictions can use an immutable version ID; official model endpoint follows maintained latest | Model string may be deprecated or redirected; dedicated endpoint is the documented escape hatch for an original version |
| Schema discovery | Every model page exposes its own schema; common fields are not platform fields | `models.get` exposes `latest_version.openapi_schema`; version pages preserve version-specific schema | `/v1/models` exposes model metadata, but image parameter support still requires image docs and model-specific pages |
| Output path | Public `fal.media` CDN URLs unless a model returns inline data | Current clients expose `FileOutput`; URLs use `replicate.delivery` and expire after one hour | Request `response_format: base64` to avoid a second URL fetch |
| Data controls | `X-Fal-Store-IO: 0`; separate CDN lifecycle control | API prediction inputs, outputs, logs, and files removed after one hour by default | Account ZDR/privacy setting; public documents conflict on the default, so verify it |
| Hidden routing risk | Queue retries and supported-model fallbacks are enabled by default | Official model can advance to a new version | Deprecation policy permits redirects for selected model IDs |

No cell means "best." Benchmark the actual brief using fixed acceptance tests. The same seed across gateways or model builds is not comparable reproducibility.

## Freeze each model contract

Do not implement a universal payload containing `prompt`, `width`, `steps`, and `seed` and send it everywhere. For every approved adapter:

1. retrieve the current model-specific schema from the first-party page/API;
2. permit only fields in that schema, with local type/range checks;
3. save a canonical schema hash and model/page URL in the release record;
4. test a dry request fixture and mocked success/failure responses;
5. require review when the schema hash, endpoint ID, returned model/version, price unit, publisher terms, or safety defaults change.

### fal.ai facts that change design

- REST authentication is `Authorization: Key <FAL_KEY>`.
- The production queue for endpoint `fal-ai/flux/schnell` is `POST https://queue.fal.run/fal-ai/flux/schnell`; queue states are `IN_QUEUE`, `IN_PROGRESS`, and `COMPLETED`, after which the response URL is retrieved.
- Queue requests can retry up to ten times on selected server/connection failures. For supported models, fal may route to an "equivalent" fallback endpoint after retries. This is a **PROVIDER CLAIM** of equivalence, not proof of identical model, weights, schema, license, safety, or output.
- Use `X-Fal-No-Retry: 1` and `x-app-fal-disable-fallback: 1` when one approved submission must mean one approved endpoint execution. A client timeout does not stop server processing.
- `X-Fal-Store-IO: 0` prevents platform JSON input/output history storage, but not CDN media. Default JSON payload retention is documented as 30 days. `X-Fal-Object-Lifecycle-Preference` controls generated-media expiration; account default may be forever if not configured.
- fal media URLs are public to anyone holding the URL. Files uploaded as inputs to fal CDN are not removed when request payloads are deleted.
- Model pricing is per endpoint and may be per image, megapixel, or compute second. Query `GET https://api.fal.ai/v1/models/pricing?endpoint_id=...` and use account-specific results.
- fal webhooks use ED25519 with public keys from `https://rest.fal.ai/.well-known/jwks.json`, four `X-Fal-Webhook-*` headers, SHA-256 of the raw body, and a documented +/-300-second timestamp check.

### Replicate facts that change design

- REST authentication is `Authorization: Bearer <REPLICATE_API_TOKEN>`.
- Generic pinned prediction: `POST https://api.replicate.com/v1/predictions` with `version` and `input`. Official model: `POST /v1/models/{owner}/{name}/predictions` without a version; Replicate keeps it current.
- Prediction states are `starting`, `processing`, `succeeded`, `failed`, and `canceled`. Async is default. `Prefer: wait=n` only holds the HTTP call for 1-60 seconds and can still return an incomplete prediction. `Cancel-After` sets a server deadline from 5 seconds to 24 hours.
- API prediction input, output, files, and logs are deleted after one hour by default. Web-created prediction data is kept indefinitely until deletion.
- Official models have a stable API and output-based price, but the backing version is maintained latest. Community versions can be pinned, but have creator-controlled support/schema and commonly runtime/hardware billing.
- The current output-file guide says SDK `FileOutput` should replace URL/auth handling and that `replicate.delivery` URLs need no Authorization logic. The general HTTP reference still says file URLs need Authorization. Treat this as a documentation conflict: prefer current SDK `FileOutput`, or fetch only documented `replicate.delivery` URLs without forwarding the API token; do not "fix" a 401 by attaching credentials to an arbitrary host.
- Replicate webhooks are HMAC-SHA256 over `{webhook-id}.{webhook-timestamp}.{raw-body}`, using the base64 portion of the per-user/org `whsec_` secret. Deliveries can duplicate and arrive out of order; terminal deliveries retry on backoff until roughly one minute after completion.
- Current default limits are documented as 600 prediction creates/minute and 3000 other calls/minute, with stricter low-credit conditions. Live 429 recovery text controls.

### Together AI facts that change design

- Current base is `https://api.together.ai/v1`; use Bearer authentication. Older first-party model pages still show `api.together.xyz`, so use the current API/compatibility docs and SDK default.
- `POST /v1/images/generations` returns the image response synchronously. A transport timeout is an ambiguous create; no public idempotency key or image-job lookup was found.
- The endpoint has common fields, but availability differs by model. The image overview says FLUX Schnell uses `aspect_ratio`, while the current FLUX Schnell model page demonstrates `width`/`height` and the endpoint reference exposes those fields. Treat this as a first-party documentation conflict, freeze a tested schema/SDK version, and do not infer support. `image_url` and `reference_images` also apply to different model sets.
- `response_format` is `url` or `base64`; `n` is documented as 1-4. Keep `disable_safety_checker` false. Some models do not run the gateway safety checker, so application policy is still required.
- Serverless image pricing is model-specific, generally per image or megapixel, and steps above a listed default may add cost. Dynamic model-specific rate limits are returned in response headers.
- The deprecation policy documents both no-redirect removals and active redirects. Compare the returned `model` with the requested model and quarantine a mismatch. A model string is not always an immutable revision.
- Together's Privacy and Security page says it does not store inputs/outputs by default, while its current Privacy Policy and Terms describe enabling ZDR by selecting "No" for storage/training. Treat the default as **UNKNOWN**; verify the project setting and executed contract. ZDR is prospective, not retroactive.

## Paid-call barrier

Schema reads, pricing reads, plans, and local/mocked validation do not authorize generation. Free endpoints and prepaid credits still consume a limited resource.

Before every live generation require a canonical UUIDv4 attempt, a same-day price/schema/terms snapshot, positive reviewed unit price and estimate, and a finite positive ceiling. Hash one canonical authorization record containing the attempt, approval reference, exact endpoint/model/payload/count, output destination and policy, schema hash, price source/unit/floor/estimate/ceiling, and governance dispositions. `GATEWAY_APPROVAL_SHA256` must exactly equal that record; a free-form ticket string is not the gate.

Create the attempt ledger with `O_CREAT|O_EXCL` before POST. The attempt UUID and approval digest are single-use. Persist the provider ID immediately, before polling, output validation, or asset download. A later process may use `GATEWAY_RESUME=1` only for the same durable fal/Replicate identity; a Together timeout or an attempt without an ID must be reconciled rather than resubmitted.

Never auto-generate exploratory variants. A retry or cross-gateway failover is a new approved create unless the provider proves it is the same job.

**Example price observations, not defaults (2026-07-10):** fal documents `fal-ai/flux/schnell` at `$0.003/MP`; Replicate's official `black-forest-labs/flux-schnell` page shows `$3/1000 output images`; Together lists `black-forest-labs/FLUX.1-schnell` at `$0.0027/MP` with four default steps. Account discounts, rounding, requested size/count/steps, model revisions, and taxes can change the estimate. Query again.

## Complete adapter example

The following Python 3.11+ example is deliberately three adapters, not one translated payload. It uses text-to-image only so reference-upload policy cannot be mistaken for a universal contract. It defaults to an offline plan, binds exact approval and positive spend floors, preflights Replicate model/version OpenAPI, writes an exclusive pre-create ledger, disables fal retries/fallback, resumes only known async IDs, requests Together base64, refuses redirects, validates image bytes with Pillow, and writes a sanitized release/billing/provenance manifest.

Install Pillow for decode checks: `python -m pip install Pillow`. Copy as `gateway_image.py`.

```python
from __future__ import annotations

import base64
import binascii
import hashlib
import ipaddress
import json
import math
import os
import platform
import random
import socket
import tempfile
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from email.utils import parsedate_to_datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

JSON_CAP = 48 * 1024 * 1024
IMAGE_CAP = 48 * 1024 * 1024
PIXEL_CAP = 36_000_000
POLL_DEADLINE_S = 360
CREATE_DEADLINE_S = 90
ASSET_DEADLINE_S = 120
READ_SLICE_S = 5
SCHEMA_CHECKED = "2026-07-10"
PRICE_CHECKED = "2026-07-10"
OUTPUT_POLICY_VERSION = "image-v1"


class StopRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError(f"redirect refused: {code}")


HTTP = build_opener(StopRedirects)


class GatewayHTTPError(RuntimeError):
    def __init__(self, code: int, safe_message: str):
        super().__init__(safe_message)
        self.code = code


class GatewayTerminalError(RuntimeError):
    pass


class AmbiguousCreate(RuntimeError):
    pass


@dataclass(frozen=True)
class Plan:
    gateway: str
    model: str
    url: str
    payload: dict[str, Any]
    lifecycle: str
    version_policy: str
    schema_url: str
    price_source: str
    price_unit: str
    known_unit_price: Decimal
    billable_units: Decimal


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def require_sha256(name: str, value: str) -> str:
    value = value.strip().lower()
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{name} must be a 64-character lowercase hex SHA-256")
    return value


def parse_positive_money(name: str, value: str, required: bool) -> Decimal | None:
    value = value.strip()
    if not value:
        if required:
            raise ValueError(f"{name} is required")
        return None
    try:
        amount = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{name} must be a finite positive decimal") from exc
    if not amount.is_finite() or amount <= 0:
        raise ValueError(f"{name} must be a finite positive decimal")
    return amount


def valid_attempt_id(value: str) -> str:
    try:
        parsed = uuid.UUID(value)
    except ValueError as exc:
        raise ValueError("GATEWAY_ATTEMPT_ID must be a UUIDv4") from exc
    normalized = str(parsed)
    if parsed.version != 4 or value.lower() != normalized:
        raise ValueError("GATEWAY_ATTEMPT_ID must be a canonical UUIDv4")
    return normalized


def valid_provider_id(value: Any, provider: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 256:
        raise AmbiguousCreate(f"{provider} create returned no usable identity")
    if any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for char in value):
        raise AmbiguousCreate(f"{provider} create returned an unsafe identity")
    return value


def public_https(url: str, allowed: tuple[str, ...]) -> str:
    parsed = urlsplit(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host or parsed.username or parsed.password or parsed.fragment:
        raise ValueError("asset must be credential-free fragment-free HTTPS")
    if parsed.port not in (None, 443):
        raise ValueError("asset port is not allowed")
    if not any(host == suffix or host.endswith("." + suffix) for suffix in allowed):
        raise ValueError("asset host is not provider-approved")
    for answer in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        if not ipaddress.ip_address(answer[4][0]).is_global:
            raise ValueError("asset resolved to a non-public address")
    return url


def api_url(url: str, host: str, prefix: str) -> str:
    parsed = urlsplit(url)
    expected_path = parsed.path == prefix or parsed.path.startswith(prefix.rstrip("/") + "/")
    if (
        parsed.scheme != "https"
        or parsed.hostname != host
        or parsed.port not in (None, 443)
        or parsed.username
        or parsed.password
        or parsed.fragment
        or not expected_path
    ):
        raise ValueError("unexpected API URL")
    return url


def retry_after_seconds(headers: Any, now: datetime | None = None) -> float | None:
    value = headers.get("Retry-After") if headers is not None else None
    if not value:
        return None
    try:
        seconds = float(value)
        return max(0.0, min(seconds, 60.0)) if math.isfinite(seconds) else None
    except ValueError:
        try:
            target = parsedate_to_datetime(value)
            if target.tzinfo is None:
                target = target.replace(tzinfo=timezone.utc)
            current = now or datetime.now(timezone.utc)
            return max(0.0, min((target - current).total_seconds(), 60.0))
        except (TypeError, ValueError, OverflowError):
            return None


def bounded_read(response: Any, cap: int, deadline: float, expected_type: str | None) -> bytes:
    if time.monotonic() >= deadline:
        raise TimeoutError("response deadline reached")
    length = response.headers.get("Content-Length")
    if length:
        try:
            declared = int(length)
        except ValueError as exc:
            raise RuntimeError("invalid Content-Length") from exc
        if declared < 0 or declared > cap:
            raise RuntimeError("response exceeds client cap")
    if expected_type and response.headers.get_content_type() != expected_type:
        raise RuntimeError("unexpected response content type")
    chunks: list[bytes] = []
    size = 0
    reader = getattr(response, "read1", response.read)
    while True:
        if time.monotonic() >= deadline:
            raise TimeoutError("response deadline reached")
        chunk = reader(min(64 * 1024, cap + 1 - size))
        if not chunk:
            break
        size += len(chunk)
        if size > cap:
            raise RuntimeError("response exceeds client cap")
        chunks.append(chunk)
    return b"".join(chunks)


def safe_error_hash(exc: HTTPError, deadline: float) -> str:
    try:
        raw = bounded_read(exc, 16_384, deadline, None)
    except Exception:
        raw = b""
    finally:
        try:
            exc.close()
        except OSError:
            pass
    return hashlib.sha256(raw).hexdigest()


def post_json(
    url: str,
    expected_host: str,
    path_prefix: str,
    auth_header: str,
    payload: dict[str, Any],
    extra_headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    api_url(url, expected_host, path_prefix)
    body = json.dumps(payload, separators=(",", ":")).encode()
    headers = {
        "Accept": "application/json",
        "Authorization": auth_header,
        "Content-Type": "application/json",
    }
    headers.update(extra_headers or {})
    deadline = time.monotonic() + CREATE_DEADLINE_S
    try:
        timeout = max(0.1, min(READ_SLICE_S, deadline - time.monotonic()))
        with HTTP.open(Request(url, data=body, headers=headers, method="POST"), timeout=timeout) as response:
            raw = bounded_read(response, JSON_CAP, deadline, "application/json")
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise RuntimeError("gateway create response is not an object")
        return value
    except HTTPError as exc:
        error_hash = safe_error_hash(exc, deadline)
        wait = retry_after_seconds(exc.headers)
        suffix = f"; retry_after={wait:g}s" if wait is not None else ""
        if exc.code >= 500:
            raise AmbiguousCreate(
                f"create returned HTTP {exc.code}; body_sha256={error_hash}; reconcile before resubmission"
            ) from exc
        raise GatewayHTTPError(
            exc.code, f"gateway rejected create with HTTP {exc.code}; body_sha256={error_hash}{suffix}"
        ) from None
    except GatewayHTTPError:
        raise
    except AmbiguousCreate:
        raise
    except Exception as exc:
        raise AmbiguousCreate(
            "create transport or 2xx response failed before a durable identity; do not resubmit"
        ) from exc


def sleep_with_deadline(seconds: float, deadline: float) -> None:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("gateway deadline reached")
    time.sleep(min(max(0.0, seconds), remaining))


def get_json(
    url: str,
    expected_host: str,
    path_prefix: str,
    auth_header: str,
    deadline: float,
    event: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    api_url(url, expected_host, path_prefix)
    delay = 1.0
    while True:
        if time.monotonic() >= deadline:
            raise TimeoutError("read-only gateway deadline reached")
        headers = {"Accept": "application/json", "Authorization": auth_header}
        try:
            timeout = max(0.1, min(READ_SLICE_S, deadline - time.monotonic()))
            with HTTP.open(Request(url, headers=headers, method="GET"), timeout=timeout) as response:
                raw = bounded_read(response, JSON_CAP, deadline, "application/json")
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise RuntimeError("gateway response is not an object")
            return value
        except HTTPError as exc:
            retryable = exc.code == 429 or exc.code >= 500
            error_hash = safe_error_hash(exc, deadline)
            if not retryable:
                raise GatewayHTTPError(
                    exc.code, f"gateway read failed with HTTP {exc.code}; body_sha256={error_hash}"
                ) from None
            wait = retry_after_seconds(exc.headers)
            pause = wait if wait is not None else delay + random.uniform(0, delay * 0.15)
            if event:
                event({"kind": "read_retry", "http_status": exc.code, "wait_seconds": pause})
        except (TimeoutError, URLError, RuntimeError, json.JSONDecodeError) as exc:
            if time.monotonic() >= deadline:
                raise TimeoutError("read-only gateway deadline reached") from exc
            pause = delay + random.uniform(0, delay * 0.15)
            if event:
                event({"kind": "read_retry", "error": type(exc).__name__, "wait_seconds": pause})
        sleep_with_deadline(pause, deadline)
        delay = min(delay * 1.7, 12.0)


def check_image(blob: bytes) -> tuple[str, str, int, int]:
    if not blob or len(blob) > IMAGE_CAP:
        raise ValueError("image is empty or exceeds client cap")
    if blob.startswith(b"\x89PNG\r\n\x1a\n"):
        kind, suffix = "image/png", ".png"
    elif blob.startswith(b"\xff\xd8\xff"):
        kind, suffix = "image/jpeg", ".jpg"
    elif blob.startswith(b"RIFF") and blob[8:12] == b"WEBP":
        kind, suffix = "image/webp", ".webp"
    else:
        raise ValueError("output magic is not PNG, JPEG, or WebP")
    try:
        from PIL import Image, UnidentifiedImageError

        Image.MAX_IMAGE_PIXELS = PIXEL_CAP
        with Image.open(BytesIO(blob)) as image:
            width, height = image.size
            if width * height > PIXEL_CAP or getattr(image, "n_frames", 1) != 1:
                raise ValueError("output exceeds pixel/frame policy")
            image.verify()
        with Image.open(BytesIO(blob)) as image:
            image.load()
    except ImportError as exc:
        raise RuntimeError("Pillow is required for artifact validation") from exc
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("output failed full image decode") from exc
    return kind, suffix, width, height


def fetch_asset(url: str, domains: tuple[str, ...], deadline: float) -> bytes:
    public_https(url, domains)
    request = Request(
        url,
        headers={"Accept": "image/png,image/jpeg,image/webp", "User-Agent": "gateway-image-example/1"},
        method="GET",
    )
    if time.monotonic() >= deadline:
        raise TimeoutError("asset deadline reached")
    timeout = max(0.1, min(READ_SLICE_S, deadline - time.monotonic()))
    try:
        with HTTP.open(request, timeout=timeout) as response:
            content_type = response.headers.get_content_type()
            if content_type not in {"image/png", "image/jpeg", "image/webp"}:
                raise RuntimeError("asset response is not an approved image MIME")
            blob = bounded_read(response, IMAGE_CAP, deadline, None)
    except HTTPError as exc:
        error_hash = safe_error_hash(exc, deadline)
        raise GatewayHTTPError(
            exc.code, f"asset fetch failed with HTTP {exc.code}; body_sha256={error_hash}"
        ) from None
    mime, _, _, _ = check_image(blob)
    if content_type != mime:
        raise RuntimeError("asset MIME/magic mismatch")
    return blob


def atomic_bytes(path: Path, blob: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle: int | None = None
    temp_name: str | None = None
    try:
        handle, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
        try:
            stream = os.fdopen(handle, "wb")
            handle = None
            with stream:
                stream.write(blob)
                stream.flush()
                os.fsync(stream.fileno())
        except Exception:
            if handle is not None:
                try:
                    os.close(handle)
                except OSError:
                    pass
                handle = None
            raise
        os.replace(temp_name, path)
        temp_name = None
    finally:
        if handle is not None:
            try:
                os.close(handle)
            except OSError:
                pass
        if temp_name and os.path.exists(temp_name):
            try:
                os.unlink(temp_name)
            except OSError:
                pass


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    atomic_bytes(path, (json.dumps(value, indent=2, sort_keys=True) + "\n").encode())


def exclusive_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    handle: int | None = None
    created = False
    try:
        handle = os.open(path, flags, 0o600)
        created = True
        try:
            stream = os.fdopen(handle, "wb")
            handle = None
            with stream:
                stream.write((json.dumps(value, indent=2, sort_keys=True) + "\n").encode())
                stream.flush()
                os.fsync(stream.fileno())
        except Exception:
            if handle is not None:
                try:
                    os.close(handle)
                except OSError:
                    pass
                handle = None
            raise
    except Exception:
        if created:
            try:
                os.unlink(path)
            except OSError:
                pass
        raise
    finally:
        if handle is not None:
            try:
                os.close(handle)
            except OSError:
                pass


def read_local_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if len(raw) > JSON_CAP:
        raise RuntimeError("local ledger exceeds cap")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("local ledger is not an object")
    return value


def update_ledger(path: Path, **changes: Any) -> dict[str, Any]:
    current = read_local_json(path)
    current.update(changes)
    atomic_json(path, current)
    return current


def append_ledger_event(path: Path, event: dict[str, Any]) -> None:
    current = read_local_json(path)
    events = current.get("events")
    if not isinstance(events, list):
        events = []
    if len(events) >= 100:
        events = events[-99:]
    events.append({"at": utc_now(), **event})
    current["events"] = events
    current["updated_at"] = utc_now()
    atomic_json(path, current)


def make_plan() -> Plan:
    gateway = os.getenv("IMG_GATEWAY", "fal").lower()
    prompt = os.getenv("IMAGE_PROMPT", "").strip()
    if not prompt:
        raise ValueError("IMAGE_PROMPT is required")
    seed = int(os.getenv("IMAGE_SEED", "1"))
    if gateway == "fal":
        model = "fal-ai/flux/schnell"
        return Plan(
            gateway,
            model,
            "https://queue.fal.run/fal-ai/flux/schnell",
            {
                "prompt": prompt,
                "image_size": "square_hd",
                "num_inference_steps": 4,
                "num_images": 1,
                "seed": seed,
                "enable_safety_checker": True,
                "output_format": "png",
            },
            "queue",
            "floating endpoint ID; schema snapshot required",
            "https://fal.ai/docs/model-api-reference/image-generation-api/flux-schnell",
            "https://api.fal.ai/v1/models/pricing?endpoint_id=fal-ai/flux/schnell",
            "megapixel-rounded-up",
            Decimal("0.003"),
            Decimal("2"),
        )
    if gateway == "replicate":
        model = "black-forest-labs/flux-schnell"
        version = os.getenv("REPLICATE_VERSION_ID", "").strip().lower()
        inputs = {
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "num_outputs": 1,
            "num_inference_steps": 4,
            "seed": seed,
            "output_format": "webp",
            "output_quality": 90,
            "disable_safety_checker": False,
            "go_fast": False,
            "megapixels": "1",
        }
        if version:
            require_sha256("REPLICATE_VERSION_ID", version)
            return Plan(
                gateway,
                model,
                "https://api.replicate.com/v1/predictions",
                {"version": version, "input": inputs},
                "prediction",
                "immutable version requested and preflight-required",
                f"https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/versions/{version}",
                "https://replicate.com/black-forest-labs/flux-schnell/api",
                "output-image",
                Decimal("0.003"),
                Decimal("1"),
            )
        return Plan(
            gateway,
            model,
            "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions",
            {"input": inputs},
            "prediction",
            "official model follows maintained latest; schema preflight-required",
            "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell",
            "https://replicate.com/black-forest-labs/flux-schnell/api",
            "output-image",
            Decimal("0.003"),
            Decimal("1"),
        )
    if gateway == "together":
        model = "black-forest-labs/FLUX.1-schnell"
        return Plan(
            gateway,
            model,
            "https://api.together.ai/v1/images/generations",
            {
                "model": model,
                "prompt": prompt,
                "width": 1024,
                "height": 1024,
                "steps": 4,
                "n": 1,
                "seed": seed,
                "response_format": "base64",
                "output_format": "png",
                "disable_safety_checker": False,
            },
            "synchronous",
            "model ID may redirect; response identity enforced",
            "https://docs.together.ai/reference/post-images-generations",
            "https://www.together.ai/pricing",
            "megapixel",
            Decimal("0.0027"),
            Decimal("1.048576"),
        )
    raise ValueError("IMG_GATEWAY must be fal, replicate, or together")


def merge_schema(schema: dict[str, Any]) -> dict[str, Any]:
    if "allOf" not in schema:
        return schema
    merged: dict[str, Any] = {"properties": {}, "required": []}
    for part in schema.get("allOf", []):
        if isinstance(part, dict):
            part = merge_schema(part)
            merged["properties"].update(part.get("properties", {}))
            merged["required"].extend(part.get("required", []))
    return merged


def replicate_input_schema(openapi: dict[str, Any]) -> dict[str, Any]:
    schemas = openapi.get("components", {}).get("schemas", {})
    candidate = schemas.get("Input") if isinstance(schemas, dict) else None
    if not isinstance(candidate, dict):
        raise RuntimeError("Replicate OpenAPI has no Input schema")
    candidate = merge_schema(candidate)
    if not isinstance(candidate.get("properties"), dict):
        raise RuntimeError("Replicate Input schema has no properties")
    return candidate


def validate_schema_value(name: str, value: Any, schema: dict[str, Any]) -> None:
    expected = schema.get("type")
    valid = {
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "array": isinstance(value, list),
        "object": isinstance(value, dict),
    }
    if expected in valid and not valid[expected]:
        raise RuntimeError(f"Replicate input {name!r} violates schema type")
    if "enum" in schema and value not in schema["enum"]:
        raise RuntimeError(f"Replicate input {name!r} violates schema enum")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise RuntimeError(f"Replicate input {name!r} is below schema minimum")
        if "maximum" in schema and value > schema["maximum"]:
            raise RuntimeError(f"Replicate input {name!r} exceeds schema maximum")


def validate_replicate_inputs(openapi: dict[str, Any], inputs: dict[str, Any]) -> None:
    schema = replicate_input_schema(openapi)
    properties = schema["properties"]
    unknown = sorted(set(inputs) - set(properties))
    missing = sorted(set(schema.get("required", [])) - set(inputs))
    if unknown or missing:
        raise RuntimeError(f"Replicate schema mismatch; unknown={unknown}; missing={missing}")
    for name, value in inputs.items():
        field = properties[name]
        if not isinstance(field, dict):
            raise RuntimeError(f"Replicate input schema for {name!r} is invalid")
        validate_schema_value(name, value, field)


def preflight_replicate(plan: Plan, token: str, expected_hash: str) -> dict[str, Any]:
    deadline = time.monotonic() + CREATE_DEADLINE_S
    auth = "Bearer " + token
    info = get_json(plan.schema_url, "api.replicate.com", "/v1/models/black-forest-labs/flux-schnell", auth, deadline)
    requested_version = plan.payload.get("version")
    if requested_version:
        if info.get("id") != requested_version:
            raise RuntimeError("Replicate version preflight did not return the requested version")
        version = requested_version
        openapi = info.get("openapi_schema")
    else:
        if info.get("owner") not in (None, "black-forest-labs") or info.get("name") not in (
            None,
            "flux-schnell",
        ):
            raise RuntimeError("Replicate model preflight returned a different model")
        latest = info.get("latest_version")
        if not isinstance(latest, dict) or not isinstance(latest.get("id"), str):
            raise RuntimeError("Replicate model preflight has no latest version")
        version = latest["id"]
        openapi = latest.get("openapi_schema")
    if not isinstance(openapi, dict):
        raise RuntimeError("Replicate preflight has no OpenAPI schema")
    actual_hash = hashlib.sha256(canonical(openapi)).hexdigest()
    if actual_hash != expected_hash:
        raise RuntimeError("Replicate schema hash drifted; do not create")
    validate_replicate_inputs(openapi, plan.payload["input"])
    return {
        "url": plan.schema_url,
        "sha256": actual_hash,
        "checked_at": utc_now(),
        "version": version,
        "validation": "model/version identity and Input allowlist passed before create",
    }


def wait_fal(
    plan: Plan,
    token: str,
    on_identity: Callable[[str, dict[str, Any]], None],
    on_state: Callable[[str], None],
    on_retry: Callable[[dict[str, Any]], None],
    resume_id: str | None = None,
) -> tuple[str, dict[str, Any], list[bytes]]:
    auth = "Key " + token
    deadline = time.monotonic() + POLL_DEADLINE_S
    if resume_id:
        request_id = valid_provider_id(resume_id, "fal")
    else:
        initial = post_json(
            plan.url,
            "queue.fal.run",
            "/fal-ai/flux/schnell",
            auth,
            plan.payload,
            {
                "X-Fal-Store-IO": "0",
                "X-Fal-No-Retry": "1",
                "x-app-fal-disable-fallback": "1",
                "X-Fal-Object-Lifecycle-Preference": json.dumps(
                    {"expiration_duration_seconds": 3600}
                ),
            },
        )
        request_id = valid_provider_id(initial.get("request_id"), "fal")
        on_identity(request_id, initial)
    root = f"https://queue.fal.run/{plan.model}/requests/{request_id}"
    while True:
        state = get_json(
            root + "/status",
            "queue.fal.run",
            f"/{plan.model}/requests",
            auth,
            deadline,
            on_retry,
        )
        if state.get("request_id") not in (None, request_id):
            raise RuntimeError("fal request_id mismatch")
        status = state.get("status")
        on_state(str(status))
        if status == "COMPLETED":
            if state.get("error"):
                raise GatewayTerminalError(f"fal completed with an error; id={request_id}")
            result = get_json(
                root + "/response",
                "queue.fal.run",
                f"/{plan.model}/requests",
                auth,
                deadline,
                on_retry,
            )
            images = result.get("images")
            if not isinstance(images, list) or len(images) != 1 or not isinstance(images[0], dict):
                raise RuntimeError("fal output does not match frozen schema")
            url = images[0].get("url")
            if not isinstance(url, str):
                raise RuntimeError("fal image URL missing")
            asset_deadline = min(deadline, time.monotonic() + ASSET_DEADLINE_S)
            return request_id, result, [fetch_asset(url, ("fal.media",), asset_deadline)]
        if status not in {"IN_QUEUE", "IN_PROGRESS"}:
            raise GatewayTerminalError(f"unexpected fal queue state: {status!r}; id={request_id}")
        sleep_with_deadline(1.0, deadline)


def wait_replicate(
    plan: Plan,
    token: str,
    expected_version: str,
    on_identity: Callable[[str, dict[str, Any]], None],
    on_state: Callable[[str], None],
    on_retry: Callable[[dict[str, Any]], None],
    resume_id: str | None = None,
) -> tuple[str, dict[str, Any], list[bytes]]:
    auth = "Bearer " + token
    deadline = time.monotonic() + POLL_DEADLINE_S
    if resume_id:
        prediction_id = valid_provider_id(resume_id, "Replicate")
        current = get_json(
            f"https://api.replicate.com/v1/predictions/{prediction_id}",
            "api.replicate.com",
            "/v1/predictions",
            auth,
            deadline,
            on_retry,
        )
    else:
        current = post_json(
            plan.url,
            "api.replicate.com",
            "/v1",
            auth,
            plan.payload,
            {"Cancel-After": "2m"},
        )
        prediction_id = valid_provider_id(current.get("id"), "Replicate")
        on_identity(prediction_id, current)
    while True:
        if current.get("id") != prediction_id:
            raise RuntimeError("Replicate prediction id mismatch")
        status = current.get("status")
        on_state(str(status))
        if status == "succeeded":
            break
        if status in {"failed", "canceled"}:
            raise GatewayTerminalError(f"Replicate prediction {status}; id={prediction_id}")
        if status not in {"starting", "processing"}:
            raise GatewayTerminalError(f"unexpected Replicate state: {status!r}; id={prediction_id}")
        sleep_with_deadline(1.0, deadline)
        current = get_json(
            f"https://api.replicate.com/v1/predictions/{prediction_id}",
            "api.replicate.com",
            "/v1/predictions",
            auth,
            deadline,
            on_retry,
        )
    if current.get("version") != expected_version:
        raise RuntimeError("Replicate returned a version different from the preflighted version")
    if current.get("model") not in (None, plan.model):
        raise RuntimeError("Replicate returned a different model ID")
    output = current.get("output")
    if not isinstance(output, list) or len(output) != 1 or not isinstance(output[0], str):
        raise RuntimeError("Replicate output does not match frozen URI-array schema")
    asset_deadline = min(deadline, time.monotonic() + ASSET_DEADLINE_S)
    return prediction_id, current, [
        fetch_asset(output[0], ("replicate.delivery",), asset_deadline)
    ]


def run_together(
    plan: Plan,
    token: str,
    on_identity: Callable[[str, dict[str, Any]], None],
    on_state: Callable[[str], None],
) -> tuple[str, dict[str, Any], list[bytes]]:
    response = post_json(
        plan.url,
        "api.together.ai",
        "/v1/images/generations",
        "Bearer " + token,
        plan.payload,
    )
    request_id = valid_provider_id(response.get("id"), "Together")
    on_identity(request_id, response)
    if response.get("model") != plan.model:
        raise RuntimeError("Together returned a different model ID; quarantine this run")
    data = response.get("data")
    if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], dict):
        raise RuntimeError("Together output does not match frozen schema")
    encoded = data[0].get("b64_json")
    encoded_cap = (IMAGE_CAP * 4 // 3) + 8
    if not isinstance(encoded, str) or len(encoded) > encoded_cap:
        raise RuntimeError("Together base64 output missing or oversized")
    try:
        blob = base64.b64decode(encoded, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise RuntimeError("Together returned invalid base64") from exc
    check_image(blob)
    on_state("succeeded")
    return request_id, response, [blob]


def safe_metrics(response: dict[str, Any]) -> dict[str, Any] | None:
    candidate = response.get("metrics")
    if not isinstance(candidate, dict):
        candidate = response.get("timings")
    if not isinstance(candidate, dict):
        return None
    safe: dict[str, Any] = {}
    for key, value in candidate.items():
        if isinstance(key, str) and len(key) <= 64 and isinstance(value, (int, float, str, bool)):
            safe[key] = value
    return safe


def client_version() -> str:
    try:
        import PIL

        pillow = PIL.__version__
    except ImportError:
        pillow = "missing"
    return f"Python {platform.python_version()}; urllib stdlib; Pillow {pillow}"


def approval_record(
    plan: Plan,
    attempt_id: str,
    approval_id: str,
    schema_hash: str,
    price_snapshot_hash: str,
    reviewed_unit_price: Decimal,
    estimate: Decimal,
    maximum: Decimal,
    destination: Path,
    governance: dict[str, str],
) -> dict[str, Any]:
    output_policy = {
        "version": OUTPUT_POLICY_VERSION,
        "destination_sha256": hashlib.sha256(str(destination).encode()).hexdigest(),
        "artifact_naming": f"image-{attempt_id}-{{index}}.<decoded-extension>",
        "manifest_naming": f"manifest-{attempt_id}.json",
        "allowed_formats": ["png", "jpeg", "webp"],
        "max_bytes_each": IMAGE_CAP,
        "max_pixels_each": PIXEL_CAP,
        "max_frames_each": 1,
        "source_urls_stored": False,
        "atomic_same_directory": True,
    }
    return {
        "attempt_id": attempt_id,
        "approval_id_sha256": hashlib.sha256(approval_id.encode()).hexdigest(),
        "gateway": plan.gateway,
        "endpoint": plan.url,
        "model": plan.model,
        "version_policy": plan.version_policy,
        "payload_sha256": hashlib.sha256(canonical(plan.payload)).hexdigest(),
        "prompt_sha256": hashlib.sha256(os.environ["IMAGE_PROMPT"].encode()).hexdigest(),
        "count": 1,
        "schema": {
            "url": plan.schema_url,
            "sha256": schema_hash,
            "checked": SCHEMA_CHECKED,
        },
        "pricing": {
            "source": plan.price_source,
            "snapshot_sha256": price_snapshot_hash,
            "checked": PRICE_CHECKED,
            "unit": plan.price_unit,
            "reviewed_unit_price_usd": str(reviewed_unit_price),
            "billable_units": str(plan.billable_units),
            "known_public_unit_floor_usd": str(plan.known_unit_price),
            "estimated_usd": str(estimate),
            "max_usd": str(maximum),
        },
        "output_policy": output_policy,
        "governance": governance,
    }


def main() -> None:
    plan = make_plan()
    live = os.getenv("GATEWAY_SEND") == "1"
    resume_requested = os.getenv("GATEWAY_RESUME") == "1"
    estimate = parse_positive_money(
        "GATEWAY_ESTIMATED_USD", os.getenv("GATEWAY_ESTIMATED_USD", ""), live
    )
    maximum = parse_positive_money("GATEWAY_MAX_USD", os.getenv("GATEWAY_MAX_USD", ""), live)
    reviewed_unit_price = parse_positive_money(
        "GATEWAY_REVIEWED_UNIT_PRICE_USD",
        os.getenv("GATEWAY_REVIEWED_UNIT_PRICE_USD", ""),
        live,
    )
    if reviewed_unit_price is not None and reviewed_unit_price < plan.known_unit_price:
        raise ValueError("reviewed unit price is below the dated known public floor")
    if estimate is not None and reviewed_unit_price is not None:
        reviewed_floor = reviewed_unit_price * plan.billable_units
        if estimate < reviewed_floor:
            raise ValueError(f"GATEWAY_ESTIMATED_USD is below reviewed plan floor {reviewed_floor}")
    if estimate is not None and maximum is not None and maximum < estimate:
        raise ValueError("GATEWAY_MAX_USD is below the reviewed estimate")

    attempt_text = os.getenv("GATEWAY_ATTEMPT_ID", "").strip()
    approval_id = os.getenv("GATEWAY_APPROVAL_ID", "").strip()
    schema_text = os.getenv("GATEWAY_SCHEMA_SHA256", "").strip()
    price_snapshot_text = os.getenv("GATEWAY_PRICE_SNAPSHOT_SHA256", "").strip()
    rights_text = os.getenv("GATEWAY_RIGHTS_TERMS_SHA256", "").strip()
    governance = {
        "data_class": os.getenv("GATEWAY_DATA_CLASS", "").strip(),
        "retention_review": os.getenv("GATEWAY_RETENTION_REVIEW", "").strip(),
        "moderation_disposition": os.getenv("GATEWAY_MODERATION_DISPOSITION", "").strip(),
        "human_review_disposition": os.getenv("GATEWAY_HUMAN_REVIEW_DISPOSITION", "").strip(),
        "provenance_result": os.getenv("GATEWAY_PROVENANCE_RESULT", "").strip(),
        "rights_terms_sha256": rights_text.lower(),
    }
    destination = Path(os.getenv("IMAGE_OUTPUT_DIR", "gateway-output")).resolve()

    required_hash: str | None = None
    record: dict[str, Any] | None = None
    ready = all(
        [
            attempt_text,
            approval_id,
            schema_text,
            price_snapshot_text,
            rights_text,
            estimate is not None,
            maximum is not None,
            reviewed_unit_price is not None,
            *governance.values(),
        ]
    )
    if ready:
        attempt_id = valid_attempt_id(attempt_text)
        schema_hash = require_sha256("GATEWAY_SCHEMA_SHA256", schema_text)
        price_snapshot_hash = require_sha256(
            "GATEWAY_PRICE_SNAPSHOT_SHA256", price_snapshot_text
        )
        governance["rights_terms_sha256"] = require_sha256(
            "GATEWAY_RIGHTS_TERMS_SHA256", rights_text
        )
        if governance["provenance_result"] not in {
            "passed",
            "not-present-accepted",
            "not-applicable",
        }:
            raise ValueError("GATEWAY_PROVENANCE_RESULT is not an approved disposition")
        record = approval_record(
            plan,
            attempt_id,
            approval_id,
            schema_hash,
            price_snapshot_hash,
            reviewed_unit_price,
            estimate,
            maximum,
            destination,
            governance,
        )
        required_hash = hashlib.sha256(canonical(record)).hexdigest()

    summary = {
        "dry_run": not live,
        "gateway": plan.gateway,
        "model": plan.model,
        "lifecycle": plan.lifecycle,
        "version_policy": plan.version_policy,
        "schema_checked": SCHEMA_CHECKED,
        "price_checked": PRICE_CHECKED,
        "known_public_unit_floor_usd": str(plan.known_unit_price),
        "billable_units": str(plan.billable_units),
        "count": 1,
        "estimated_usd": str(estimate) if estimate is not None else None,
        "max_usd": str(maximum) if maximum is not None else None,
        "suggested_attempt_id": None if attempt_text else str(uuid.uuid4()),
        "approval_sha256_required": required_hash,
        "approval_record_ready": ready,
        "safety": "gateway control enabled where schema supports it",
    }
    print(json.dumps(summary, indent=2))
    if not live:
        print("OFFLINE PLAN ONLY")
        return
    if not ready or record is None or required_hash is None:
        raise RuntimeError("live generation requires every approval, schema, price, and governance field")
    if not resume_requested and datetime.now(timezone.utc).date().isoformat() != PRICE_CHECKED:
        raise RuntimeError("dated price floor is stale; refresh constants and approval")
    supplied_hash = require_sha256(
        "GATEWAY_APPROVAL_SHA256", os.getenv("GATEWAY_APPROVAL_SHA256", "")
    )
    if supplied_hash != required_hash:
        raise RuntimeError("approval hash does not exactly match this call and output policy")

    key_name = {
        "fal": "FAL_KEY",
        "replicate": "REPLICATE_API_TOKEN",
        "together": "TOGETHER_API_KEY",
    }[plan.gateway]
    token = os.getenv(key_name, "")
    if not token:
        raise RuntimeError(f"{key_name} is required only after exact approval")

    attempt_id = record["attempt_id"]
    state_dir = destination / ".gateway-attempts"
    ledger_path = state_dir / f"{attempt_id}.json"
    lock_path = state_dir / f"{attempt_id}.lock"
    try:
        exclusive_json(
            lock_path,
            {
                "attempt_id": attempt_id,
                "approval_sha256": supplied_hash,
                "pid": os.getpid(),
                "acquired_at": utc_now(),
                "policy": "stale lock requires operator reconciliation; never auto-break",
            },
        )
    except FileExistsError as exc:
        raise RuntimeError("attempt is already active or has a stale crash lock; reconcile first") from exc

    provider_id: str | None = None
    mutable_ledger = False
    schema_meta: dict[str, Any]
    try:
        if ledger_path.exists():
            if not resume_requested:
                raise RuntimeError("attempt ledger already exists; replay refused")
            ledger = read_local_json(ledger_path)
            if (
                ledger.get("approval_sha256") != supplied_hash
                or ledger.get("payload_sha256") != record["payload_sha256"]
                or ledger.get("gateway") != plan.gateway
            ):
                raise RuntimeError("resume does not match the durable attempt")
            if ledger.get("state") in {"complete", "terminal_failed", "create_rejected"}:
                raise RuntimeError("terminal attempt cannot be replayed")
            provider_id = ledger.get("provider_id")
            if not isinstance(provider_id, str) or plan.gateway == "together":
                raise RuntimeError("this unresolved attempt has no safe public resume path")
            schema_meta = ledger["schema"]
            mutable_ledger = True
            append_ledger_event(ledger_path, {"kind": "resume_started", "provider_id": provider_id})
        else:
            if resume_requested:
                raise RuntimeError("resume requested but no durable attempt ledger exists")
            if plan.gateway == "replicate":
                schema_meta = preflight_replicate(plan, token, record["schema"]["sha256"])
            else:
                schema_meta = {
                    "url": plan.schema_url,
                    "sha256": record["schema"]["sha256"],
                    "checked_at": utc_now(),
                    "version": None,
                    "validation": "reviewed frozen adapter hash supplied and approval-bound",
                }
            created_at = utc_now()
            exclusive_json(
                ledger_path,
                {
                    "attempt_id": attempt_id,
                    "state": "authorized_unsubmitted",
                    "created_at": created_at,
                    "updated_at": created_at,
                    "gateway": plan.gateway,
                    "endpoint": plan.url,
                    "requested_model": plan.model,
                    "version_policy": plan.version_policy,
                    "payload_sha256": record["payload_sha256"],
                    "prompt_sha256": record["prompt_sha256"],
                    "approval_id_sha256": record["approval_id_sha256"],
                    "approval_sha256": supplied_hash,
                    "approval_record_sha256": sha256_value(record),
                    "schema": schema_meta,
                    "pricing": record["pricing"],
                    "output_policy": record["output_policy"],
                    "governance": governance,
                    "provider_id": None,
                    "provider_status": None,
                    "events": [{"at": created_at, "kind": "ledger_created_before_submit"}],
                },
            )
            mutable_ledger = True

        def on_identity(identity: str, response: dict[str, Any]) -> None:
            nonlocal provider_id
            provider_id = identity
            returned = response.get("version") if plan.gateway == "replicate" else response.get("model")
            now = utc_now()
            update_ledger(
                ledger_path,
                state="submitted",
                provider_id=identity,
                returned_model_or_version=returned,
                submitted_at=now,
                identity_persisted_at=now,
                updated_at=now,
            )

        def on_state(status: str) -> None:
            update_ledger(
                ledger_path,
                state="polling" if status not in {"succeeded", "COMPLETED"} else "provider_succeeded",
                provider_status=status,
                last_state_at=utc_now(),
                updated_at=utc_now(),
            )

        def on_retry(event: dict[str, Any]) -> None:
            append_ledger_event(ledger_path, event)

        if plan.gateway == "fal":
            request_id, response, blobs = wait_fal(
                plan, token, on_identity, on_state, on_retry, provider_id
            )
        elif plan.gateway == "replicate":
            request_id, response, blobs = wait_replicate(
                plan,
                token,
                schema_meta["version"],
                on_identity,
                on_state,
                on_retry,
                provider_id,
            )
        else:
            if provider_id is not None:
                raise RuntimeError("Together synchronous creates cannot be resumed")
            request_id, response, blobs = run_together(plan, token, on_identity, on_state)

        terminal_at = utc_now()
        update_ledger(
            ledger_path,
            state="provider_succeeded",
            terminal_state="succeeded",
            terminal_at=terminal_at,
            provider_status="succeeded",
            updated_at=terminal_at,
        )
        artifacts: list[dict[str, Any]] = []
        for index, blob in enumerate(blobs):
            mime, suffix, width, height = check_image(blob)
            path = destination / f"image-{attempt_id}-{index}{suffix}"
            atomic_bytes(path, blob)
            artifacts.append(
                {
                    "file": path.name,
                    "sha256": hashlib.sha256(blob).hexdigest(),
                    "bytes": len(blob),
                    "mime": mime,
                    "width": width,
                    "height": height,
                    "frames": 1,
                    "decode": "Pillow verify plus full load passed",
                }
            )
        artifact_at = utc_now()
        update_ledger(
            ledger_path,
            state="artifact_durable",
            artifact_at=artifact_at,
            artifacts=artifacts,
            updated_at=artifact_at,
        )
        ledger = read_local_json(ledger_path)
        returned_identity = (
            response.get("version") if plan.gateway == "replicate" else response.get("model")
        )
        manifest = {
            "attempt_id": attempt_id,
            "gateway": plan.gateway,
            "request_id": request_id,
            "requested": {
                "endpoint": plan.url,
                "model": plan.model,
                "version_policy": plan.version_policy,
                "payload_sha256": record["payload_sha256"],
                "prompt_sha256": record["prompt_sha256"],
                "seed": plan.payload.get("seed", plan.payload.get("input", {}).get("seed")),
                "count": 1,
            },
            "returned_model_or_version": returned_identity,
            "terminal_state": "succeeded",
            "timestamps": {
                "ledger_created": ledger.get("created_at"),
                "submitted": ledger.get("submitted_at"),
                "identity_persisted": ledger.get("identity_persisted_at"),
                "terminal": terminal_at,
                "artifact_durable": artifact_at,
                "manifest_durable": utc_now(),
            },
            "schema": {
                **schema_meta,
                "client_version": client_version(),
            },
            "approval": {
                "approval_id_sha256": record["approval_id_sha256"],
                "approval_sha256": supplied_hash,
                "output_policy": record["output_policy"],
            },
            "pricing": {
                **record["pricing"],
                "actual_usage": safe_metrics(response),
                "actual_cost_usd": None,
                "actual_cost_status": "provider billing line not returned; reconciliation required",
                "credits_discounts": os.getenv("GATEWAY_CREDITS_DISCOUNTS", "not reported"),
            },
            "lifecycle": {
                "retry_events": ledger.get("events", []),
                "provider_internal_retry": "disabled" if plan.gateway == "fal" else "not requested",
                "fallback": "disabled" if plan.gateway == "fal" else "none",
                "failover": "none",
                "cancel": "none",
                "unresolved_ambiguity": False,
            },
            "data_and_rights": {
                **governance,
                "data_control": {
                    "fal": "store-io=0; generated CDN expiry requested at 3600s",
                    "replicate": "API prediction default cleanup documented at 1h",
                    "together": "account ZDR setting separately verified by approval",
                }[plan.gateway],
            },
            "review": {
                "moderation_disposition": governance["moderation_disposition"],
                "human_review_disposition": governance["human_review_disposition"],
                "provenance_check": governance["provenance_result"],
            },
            "artifacts": artifacts,
            "source_urls_stored": False,
            "deletion_state": {
                "provider_source": "not retained in manifest; provider lifecycle applies",
                "local": "durable artifact retained under approved destination",
            },
        }
        manifest_path = destination / f"manifest-{attempt_id}.json"
        atomic_json(manifest_path, manifest)
        manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        completed_at = utc_now()
        update_ledger(
            ledger_path,
            state="complete",
            completed_at=completed_at,
            terminal_state="succeeded",
            manifest_file=manifest_path.name,
            manifest_sha256=manifest_hash,
            updated_at=completed_at,
        )
        print(json.dumps(manifest, indent=2))
    except AmbiguousCreate as exc:
        if mutable_ledger and ledger_path.exists():
            update_ledger(
                ledger_path,
                state="unresolved_ambiguous_create",
                unresolved_ambiguity=True,
                error_type=type(exc).__name__,
                error_at=utc_now(),
                updated_at=utc_now(),
            )
        raise
    except GatewayTerminalError as exc:
        if mutable_ledger and ledger_path.exists():
            update_ledger(
                ledger_path,
                state="terminal_failed",
                terminal_state="failed_or_canceled",
                error_type=type(exc).__name__,
                error_at=utc_now(),
                updated_at=utc_now(),
            )
        raise
    except GatewayHTTPError as exc:
        if mutable_ledger and ledger_path.exists():
            state = "needs_reconciliation" if provider_id else "create_rejected"
            update_ledger(
                ledger_path,
                state=state,
                error_type=type(exc).__name__,
                http_status=exc.code,
                error_at=utc_now(),
                updated_at=utc_now(),
            )
        raise
    except Exception as exc:
        if mutable_ledger and ledger_path.exists():
            state = "needs_reconciliation" if provider_id else "pre_submit_failed"
            update_ledger(
                ledger_path,
                state=state,
                error_type=type(exc).__name__,
                error_at=utc_now(),
                updated_at=utc_now(),
            )
        raise
    finally:
        try:
            os.unlink(lock_path)
        except OSError:
            pass


if __name__ == "__main__":
    main()
```

### Example dry runs

All three commands are offline because `GATEWAY_SEND` is unset. First set a UUIDv4 attempt and the hashes of the reviewed schema, price snapshot, and rights/terms snapshot. The dry summary prints the exact `approval_sha256_required`; if it is `null`, a required review field is missing.

```powershell
$env:IMAGE_PROMPT='Editorial product photograph of one unbranded cobalt desk lamp, three-quarter view, soft side light, neutral seamless background, no text'
$env:IMAGE_OUTPUT_DIR='C:\approved\gateway-output'
$env:GATEWAY_ATTEMPT_ID='<new canonical UUIDv4>'
$env:GATEWAY_APPROVAL_ID='change-ticket-or-human-approval-reference'
$env:GATEWAY_SCHEMA_SHA256='<64-hex reviewed schema hash>'
$env:GATEWAY_PRICE_SNAPSHOT_SHA256='<64-hex same-day account price snapshot hash>'
$env:GATEWAY_RIGHTS_TERMS_SHA256='<64-hex terms snapshot hash>'
$env:GATEWAY_DATA_CLASS='public'
$env:GATEWAY_RETENTION_REVIEW='approved for this provider path'
$env:GATEWAY_MODERATION_DISPOSITION='approved for generation'
$env:GATEWAY_HUMAN_REVIEW_DISPOSITION='required before release'
$env:GATEWAY_PROVENANCE_RESULT='not-applicable' # or passed / not-present-accepted

$env:IMG_GATEWAY='fal'
$env:GATEWAY_REVIEWED_UNIT_PRICE_USD='0.003'
$env:GATEWAY_ESTIMATED_USD='0.006' # square_hd is >1 MP and fal rounds up MP
$env:GATEWAY_MAX_USD='0.01'
python .\gateway_image.py

$env:IMG_GATEWAY='replicate'
# Optional strict version: obtain a reviewed 64-hex version and its schema from Replicate.
$env:REPLICATE_VERSION_ID=''
$env:GATEWAY_REVIEWED_UNIT_PRICE_USD='0.003'
$env:GATEWAY_ESTIMATED_USD='0.003'
$env:GATEWAY_MAX_USD='0.01'
python .\gateway_image.py

$env:IMG_GATEWAY='together'
$env:GATEWAY_REVIEWED_UNIT_PRICE_USD='0.0027'
$env:GATEWAY_ESTIMATED_USD='0.003' # 1024x1024 exceeds one decimal MP
$env:GATEWAY_MAX_USD='0.01'
python .\gateway_image.py
```

After reviewing the exact summary and obtaining approval for that exact record, copy its digest without changing any bound field:

```powershell
$env:IMG_GATEWAY='together'
$env:TOGETHER_API_KEY='<secret-store injection>'
$env:GATEWAY_APPROVAL_SHA256='<approval_sha256_required from the unchanged dry summary>'
$env:GATEWAY_SEND='1'
python .\gateway_image.py
```

Unset approval and send variables immediately after the approved call. The code never logs prompts, tokens, raw responses, base64, or source URLs. If a process exits after an async provider ID is durable, rerun the identical environment with `GATEWAY_RESUME=1`; never use resume for Together. An existing `.lock` after an abrupt process death is deliberately not auto-broken: reconcile the recorded attempt before an operator removes it.

## Webhook control planes are not interchangeable

For fal:

- verify raw body before parsing;
- require the four documented `X-Fal-Webhook-Request-Id`, `User-Id`, `Timestamp`, and `Signature` headers;
- reject timestamps outside the documented 300-second window;
- hash the raw body and verify the newline-delimited message with a cached ED25519 JWKS key; refresh keys within 24 hours;
- deduplicate both `request_id` and `gateway_request_id`, because retries can make them differ;
- note webhook terminal status is `OK`/`ERROR`, not queue `COMPLETED`.

For Replicate:

- retrieve and securely cache the org/user signing secret from `/v1/webhooks/default/secret`;
- verify raw `{id}.{timestamp}.{body}` using HMAC-SHA256 and any `v1,` signature in the space-delimited header with constant-time comparison;
- apply a documented-in-your-system timestamp tolerance (Replicate requires a tolerance but does not prescribe a number on the reviewed page);
- deduplicate on `webhook-id` plus prediction ID, accept out-of-order intermediates, and never regress or reopen a terminal prediction;
- request `webhook_events_filter: ["completed"]` unless partial logs/output are genuinely needed.

Together's reviewed real-time image endpoint has no webhook lifecycle. Do not wrap a synchronous timeout in a fake "job ID."

## Reconcile before retrying

No reviewed create endpoint exposes a client idempotency key. On a connect/read timeout after a POST body may have reached the gateway:

1. do not resubmit automatically;
2. retain the local attempt ID, time window, gateway/model, payload hash, and billing estimate;
3. if a gateway request/prediction ID was received, poll that exact resource;
4. use fal usage lines, Replicate predictions/billing, or Together cost analytics/account support to reconcile;
5. classify the attempt as succeeded, terminally failed, canceled, or unresolved;
6. require a new approval before a new create while unresolved billing/output remains possible.

Canceling is not equivalent to never running. Replicate documents that official-model cancellations may still be charged and time-billed runs charge elapsed execution. fal provides a cancel URL, but current billing documentation should be checked for the chosen model. Together's synchronous image route exposes no public cancel operation.

## Failover must preserve intent, not parameters

Disable silent fal fallback for governed production. For an application-managed secondary gateway:

- preapprove a second model, schema, publisher/license, data path, price ceiling, and acceptance baseline;
- fail over only after the primary create is terminal or financially reconciled;
- create a new provider-specific payload rather than renaming fields;
- do not expect seeds, safety decisions, aspect presets, image counts, negative prompts, or reference strength to transfer;
- mark the artifact with the actual gateway/model/version and do not mix it into a regression baseline silently;
- run semantic, geometry, text, similarity, and policy checks again.

If exact visual reproducibility is required, failover is unavailable. Use a pinned model build/deployment and a validated deterministic configuration instead.

## Inputs and artifact custody

Never send a reference merely because it has a public URL. Verify copyright/license, privacy/publicity consent, biometric/child/regulated status, and permitted transformation. Keep a source hash and rights record.

Gateway-specific input cautions:

- fal SDK uploads produce public CDN URLs; the payload-deletion API does not delete input CDN files. Avoid confidential references unless a suitable private enterprise path is contractually confirmed.
- Replicate clients accept hosted URLs, local files up to 100 MB, or data URIs recommended only below 1 MB. API prediction data is normally removed after one hour, but marketplace/third-party terms still apply.
- Together image editing uses `image_url` for some models and `reference_images` for others; the public docs do not establish a universal private upload path for these image routes.

For every output, immediately create a controlled durable copy. Enforce HTTPS/provider origin for URL outputs, no redirects, no gateway credentials on asset hosts, byte/time caps, MIME plus magic, full decode, pixel/frame limits, atomic writes, and cryptographic hashes. Preserve raw bytes so embedded provenance is not stripped. Inspect C2PA/watermark metadata separately if the model or release policy requires it; a gateway URL is not provenance.

## Rights and data-governance boundary

Model availability does not grant rights. Record gateway terms plus exact model/publisher terms as they existed at execution.

- **fal FACT:** each model has its own license; models can be marked commercial or research-only. Partner API models can transfer client content to the third-party provider. fal's "Enterprise Ready" badge is a provider classification, not legal advice.
- **Replicate FACT:** current terms make output rights subject to Third-Party Terms and include provider-specific restrictions for BFL, Ideogram, Stability, and others. Community models are creator-maintained. The official FLUX Schnell page currently advertises commercial use and "Zero training"; treat badges as model-page representations and check the incorporated terms.
- **Together FACT:** current terms say third-party model terms govern conflicts. Its FLUX Schnell page identifies Apache 2.0 weights, but output/input obligations still require the current BFL and Together terms. Together says third-party model authors do not receive requests because models run on Together infrastructure; treat that as a provider representation and confirm partner-specific exceptions.

Do not promise copyrightability, exclusivity, non-infringement, indemnity, or trademark/publicity clearance. Safety filters are neither permission nor legal review.

Data posture checked 2026-07-10:

- fal documents 30-day default JSON payload storage, optional `X-Fal-Store-IO: 0`, separately controlled public CDN retention, vendors/service providers, and team visibility into requests. Customer-input training, exact processing region, and Partner API retention are **UNKNOWN** absent the applicable contract/model path.
- Replicate documents one-hour API prediction cleanup and US-located subprocessors. Its terms authorize service processing and resultant-data use; marketplace models can introduce separate processors/terms. Model-page "Zero training" is not a platform-wide guarantee.
- Together's Privacy Policy says training use is opt-in and describes ZDR; its privacy/security documentation says no input/output storage by default. Because the activation wording conflicts, verify settings and contract rather than infer the default. Enterprise residency/private networking is available by arrangement; a universal region is **UNKNOWN**.

For personal, confidential, regulated, or residency-bound content, require an executed DPA/security review and exact routing confirmation. A gateway's generic policy cannot answer a downstream proprietary-model path by itself.

## Release and billing ledger

Do not mark a run complete until its ledger row includes:

- local attempt ID; gateway request/prediction/response ID; timestamps and terminal state;
- requested gateway/endpoint/model/version and returned gateway/model/version;
- schema URL/hash/date and client/SDK version;
- payload hash, seed, count, requested/actual dimensions and format;
- pricing source/time, unit, estimated maximum, actual usage line if available, credits/discounts, approval ID;
- retry/fallback/failover/cancel events and unresolved ambiguity;
- retention/ZDR/store-IO setting, execution/data-path classification, rights/terms snapshot;
- moderation and human-review disposition;
- durable artifact hashes, byte sizes, decode metadata, provenance check, and deletion state.

Alert on requested-versus-returned identity mismatch, schema/price drift, charge without a known request ID, successful request without an artifact, duplicate charge/output, or artifact without approval.

## First-party source set

Checked 2026-07-10:

### fal.ai

- [Model APIs overview](https://fal.ai/docs/documentation/model-apis/overview)
- [Asynchronous queue](https://fal.ai/docs/documentation/model-apis/inference/queue)
- [Reliability, retries, and fallbacks](https://fal.ai/docs/documentation/model-apis/inference/reliability)
- [Platform headers and retention controls](https://fal.ai/docs/documentation/model-apis/common-parameters)
- [Webhook verification](https://fal.ai/docs/documentation/model-apis/inference/webhooks)
- [Pricing and pricing API](https://fal.ai/docs/documentation/model-apis/pricing)
- [FLUX Schnell schema](https://fal.ai/docs/model-api-reference/image-generation-api/flux-schnell)
- [FAQ: public media and model-specific licenses](https://fal.ai/docs/documentation/model-apis/faq)
- [API Services terms](https://fal.ai/legal/api-services), [Terms](https://fal.ai/legal/terms-of-service), and [Privacy](https://fal.ai/legal/privacy-policy)

### Replicate

- [HTTP prediction API and statuses](https://replicate.com/docs/reference/http)
- [Official models](https://replicate.com/docs/topics/models/official-models) and [community models](https://replicate.com/docs/topics/models/community-models)
- [Model/version schema discovery](https://replicate.com/docs/reference/openapi)
- [Prediction creation and deadlines](https://replicate.com/docs/topics/predictions/create-a-prediction)
- [Input files](https://replicate.com/docs/topics/predictions/input-files), [output files](https://replicate.com/docs/topics/predictions/output-files), and [retention](https://replicate.com/docs/topics/predictions/data-retention)
- [Webhook delivery](https://replicate.com/docs/topics/webhooks/receive-webhook) and [signature verification](https://replicate.com/docs/topics/webhooks/verify-webhook)
- [Billing](https://replicate.com/docs/topics/billing), [pricing](https://replicate.com/pricing), and [rate limits](https://replicate.com/docs/topics/predictions/rate-limits)
- [FLUX Schnell model/API page](https://replicate.com/black-forest-labs/flux-schnell/api), [Terms](https://replicate.com/terms), [Privacy](https://replicate.com/privacy), and [subprocessors](https://replicate.com/docs/topics/site-policy/subprocessors)

### Together AI

- [Image endpoint reference](https://docs.together.ai/reference/post-images-generations)
- [Image overview](https://docs.together.ai/docs/inference/images/overview), [parameters](https://docs.together.ai/docs/inference/images/parameters), and [reference images](https://docs.together.ai/docs/inference/images/reference-images)
- [Current serverless model catalog](https://docs.together.ai/docs/serverless/models) and [models metadata API](https://docs.together.ai/reference/models)
- [Model lifecycle/deprecations](https://docs.together.ai/docs/deprecations)
- [Dynamic rate limits](https://docs.together.ai/docs/serverless/rate-limits), [billing analytics](https://docs.together.ai/docs/billing-usage-limits), and [pricing](https://www.together.ai/pricing)
- [Privacy and security](https://docs.together.ai/docs/privacy-and-security), [Privacy Policy](https://www.together.ai/privacy), and [Terms](https://www.together.ai/terms-of-service)
- [FLUX Schnell model page](https://www.together.ai/models/flux-1-schnell-2)

When sources conflict, do not silently select the convenient statement. Record the conflict, use the narrower secure behavior, and obtain account/contract confirmation before live or sensitive work.


