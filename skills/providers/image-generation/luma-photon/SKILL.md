---
name: luma-photon
description: Use Luma AI's first-party Photon and Photon Flash image API for text-to-image, image/style/character references, image modification, asynchronous generation, secure artifact handling, production prompting, cost control, and policy-aware delivery. Trigger for Luma Photon API integration or production work; do not use for Ray video, UNI image models, the Luma consumer app, or third-party Photon gateways.
---

# Luma Photon production guide

Use this skill for the legacy-path Luma API image surface backed by `photon-1` and `photon-flash-1`. Keep it separate from Ray video generation, newer UNI image workflows, Luma Agents, the consumer app, ComfyUI wrappers, and hosted third-party gateways. The string `dream-machine` remains in the documented Photon REST path even though Luma's current brand guidance calls that terminology retired.

All volatile facts below were verified against first-party sources on **2026-07-09**. Recheck the API reference, billing dashboard, rate-limit page, and governing agreement immediately before production commitments.

## Choose Photon deliberately

The documented image model IDs are:

- `photon-1` — the default Photon model. Luma positions it for higher-fidelity generation.
- `photon-flash-1` — the faster, lower-cost iteration model.

Treat those descriptions as provider positioning, not independent quality findings. Run a fixed brief-and-reference bake-off using the intended deliverable, then compare prompt adherence, source fidelity, text, anatomy, material continuity, latency, rejection rate, and actual account charge. Use Flash for broad exploration when it meets the bar; promote only finalists to Photon when measured quality justifies the cost.

Do not send Photon work to `/generations/video`, Ray models, Luma Agents, a consumer-session endpoint, or an OpenAI-compatible gateway. The first-party Photon create route is:

```text
POST https://api.lumalabs.ai/dream-machine/v1/generations/image
Authorization: Bearer $LUMAAI_API_KEY
Content-Type: application/json
```

The shared management routes are:

```text
GET    /dream-machine/v1/generations/{id}
GET    /dream-machine/v1/generations?limit=100&offset=0
DELETE /dream-machine/v1/generations/{id}
GET    /dream-machine/v1/credits
```

The official Python package is `lumaai`; its image create surface is `client.generations.image.create(...)`, while polling uses `client.generations.get(id=...)`. Direct REST is used in the complete example so timeout, redirect, byte, decode, and persistence behavior stays explicit.

## Request contract

The [image guide](https://docs.lumalabs.ai/docs/image-generation), [endpoint reference](https://docs.lumalabs.ai/reference/generateimage), and [first-party OpenAPI](https://github.com/lumalabs/lumaai-api/blob/main/openapi.yaml) document this request shape:

| Field | Production interpretation |
|---|---|
| `model` | Required by the schema; use exactly `photon-1` or `photon-flash-1`. |
| `prompt` | Natural-language image direction. The general error guide documents 3–5000 characters; keep critical text and constraints explicit. |
| `aspect_ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9`, or `9:21`; default `16:9`. |
| `format` | `jpg` or `png`; default `jpg`. Verify the returned bytes rather than trusting this request value. |
| `callback_url` | Optional HTTPS endpoint that receives repeated generation objects. No callback signature or custom-auth header is documented. |
| `image_ref` | Array of `{url, weight}` references for concept/composition/variation guidance. |
| `style_ref` | Array of `{url, weight}` style references. Use one until a broader count is contractually confirmed. |
| `character_ref` | Object with documented `identity0: {images: [...]}`; up to four images of the same identity in the guide. |
| `modify_image_ref` | One `{url, weight}` source image to modify by instruction. |
| `sync`, `sync_timeout` | Listed in the OpenAPI/reference with defaults `false` and `60`, but contradicted by the image guides' statement that polling is the only supported retrieval path. |

There is no documented Photon seed, negative-prompt field, mask, guidance scale, step count, base64/data-URI input, multipart upload, output `n`, arbitrary pixel size, or resolution selector. One create call yields one generation object with a singular `assets.image`. Make separately budgeted requests for variants.

### Dated documentation conflicts

Fail conservatively where first-party sources disagree:

- The image guides say `image_ref` supports up to four images. Luma's official `luma-api-mcp` README says eight. Cap production requests at **four** until the live reference or Luma support resolves the discrepancy.
- The REST/OpenAPI reference lists `sync` and `sync_timeout`; the Python and JavaScript image guides say polling is currently the only supported way to obtain an image. Keep `sync: false` and use bounded polling.
- The Photon product page publishes Photon Flash at **$0.004** per 2MP/1080p image, while the older v1.2 API changelog publishes **$0.002**. Both publish Photon at **$0.015**. Budget Flash at the higher public figure and reconcile the account charge; do not quote either as a guaranteed current tariff.
- The public Photon reference does not publish a numeric output-URL lifetime, a fixed API Input/Output retention period, a regional endpoint, data-residency selection, an idempotency key, or a per-generation cost field. Do not invent any of them.

## Reference and modify strategy

Photon currently accepts reference inputs only as URLs that Luma's servers can fetch. It does not document authenticated fetch headers. Host approved assets on an owned HTTPS origin or short-lived signed CDN URL, allow only the exact source hosts your application controls, and keep each URL alive until the job reaches a terminal state. Never use a workstation path, `file:` URL, private network URL, bearer credential, permanent public bucket, or a third-party upload service merely for convenience.

Choose one semantic control for each source:

- `image_ref`: carry concept, composition, pose, object, or broad visual cues into a new image. Label each reference's role in the prompt.
- `style_ref`: transfer rendering language, palette, texture, or lighting without claiming pixel-level preservation.
- `character_ref`: build the documented `identity0` from one to four clean images of the same authorized person or character. Distinct angles should agree on defining features.
- `modify_image_ref`: begin from one image and describe one localized change. Higher weights are documented as staying closer to the input with less diversity. The docs recommend `0.0`–`0.1` specifically when a color change is difficult; they do not publish a general numeric range.

Do not promise exact identity, logo, typography, layout, or unchanged-region preservation. Reference generation is conditioning, not a deterministic compositor. For an edit, state the changed element, then the small set of protected invariants. Compare every output with the source at full resolution.

Example request bodies, not mandatory formulas:

```json
{
  "model": "photon-flash-1",
  "prompt": "Use the reference only for the cobalt ceramic shape and three-quarter camera angle. Place that object on warm white paper under soft overhead light; editorial product photograph, open negative space on the left.",
  "aspect_ratio": "16:9",
  "format": "png",
  "image_ref": [
    {"url": "https://assets.example.com/signed/product-reference.png", "weight": 0.8}
  ],
  "sync": false
}
```

```json
{
  "model": "photon-1",
  "prompt": "Replace only the white daisies with yellow sunflowers. Preserve the vase geometry, tabletop, camera angle, crop, lighting direction, shadows, and background.",
  "aspect_ratio": "4:3",
  "format": "png",
  "modify_image_ref": {
    "url": "https://assets.example.com/signed/approved-vase.png",
    "weight": 1.0
  },
  "sync": false
}
```

Hash reference bytes before upload and record rights/consent, purpose, owner, source MIME/dimensions, checksum, signed-URL expiry, and the role assigned in the prompt. Store only a hash or query-redacted form of signed URLs in logs.

## Asynchronous lifecycle

Default to the documented create-and-poll path:

1. Validate the brief, policy, source rights, model, request count, conservative unit price, monthly ceiling, and current credit balance.
2. Persist a client job key and request hash before the create call. This is an application ledger, not provider idempotency.
3. `POST /generations/image`. A `201` response returns a generation object with a UUID `id`.
4. Poll `GET /generations/{id}` with a deadline and capped jittered backoff. The OpenAPI enumerates `queued`, `dreaming`, `completed`, and `failed`.
5. On `failed`, record `failure_reason`; do not assume a refund. On `completed`, require `assets.image` and immediately acquire it into controlled storage.
6. Record the terminal object, credit-balance delta when uncontaminated by concurrent account use, and final artifact manifest.

Treat a create timeout or connection loss before a valid generation ID as **ambiguous**: the paid job may exist. The public contract exposes no idempotency key and list pagination has no client-reference filter. Do not blindly replay the POST. Reconcile account usage, list recent generations, match request/model/time cautiously, and require an operator decision if uniqueness matters. After an ID is known, retry only safe GET polls and artifact downloads.

Callbacks are optional hints, not the source of truth. The guide says Luma POSTs `dreaming`, `completed`, and `failed` updates, may call repeatedly, uses a five-second timeout, and retries a non-200 response up to three times with 100 ms delay. Because no first-party signature scheme is documented, place a high-entropy opaque token in a query-free callback path, rate-limit the endpoint, cap and parse JSON, accept duplicate/out-of-order events, validate the UUID/state, and then re-fetch the generation with bearer-authenticated GET before acting.

## Complete example: dry-run-first REST job

This is an **example, not a mandatory formula**. Install Pillow (`python -m pip install Pillow`) first. It supports text, image-reference, style-reference, character-reference, and modify modes; defaults to a redacted dry run; requires explicit paid-send opt-in; never forwards the Luma bearer token to source or output hosts; polls with a deadline; validates every output redirect hop; caps bytes and pixels; fully decodes; atomically persists; and records a manifest.

Environment controls:

- `LUMA_MODE`: `text` (default), `image-reference`, `style-reference`, `character-reference`, or `modify`.
- `LUMA_REFERENCE_URLS_JSON`: JSON array of owned HTTPS URLs for non-text modes.
- `LUMA_INPUT_HOSTS`: comma-separated exact host allowlist for those inputs.
- `LUMA_ASSET_HOSTS`: exact output/redirect hosts. Default is the host used in Luma's public examples, `storage.cdn-luma.com`; fail closed if production returns another host and verify it before adding.
- `LUMA_REFERENCE_WEIGHT`: example weight, default `0.8`.
- `LUMA_MODEL`: one of the two exact Photon IDs.
- `SEND_LUMA_REQUEST=1`: required to enable API and asset network calls.

```python
import hashlib
import ipaddress
import json
import math
import os
import pathlib
import random
import socket
import tempfile
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import urllib.error
import urllib.parse
import urllib.request
import uuid

from PIL import Image, UnidentifiedImageError

API_ROOT = "https://api.lumalabs.ai/dream-machine/v1"
CREATE_URL = f"{API_ROOT}/generations/image"
OUT = pathlib.Path("luma-photon-output")
MAX_JSON_BYTES = 2 * 1024 * 1024
MAX_IMAGE_BYTES = 30 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000
MAX_POLL_SECONDS = 600
Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


api_opener = urllib.request.build_opener(NoRedirect())


class LumaHTTPError(RuntimeError):
    def __init__(self, code, detail, retry_after=None):
        super().__init__(f"Luma HTTP {code}: {detail}")
        self.code = code
        self.retry_after = retry_after


def host_set(name, defaults=()):
    values = {value.strip().lower() for value in os.getenv(name, "").split(",") if value.strip()}
    return values | set(defaults)


def redact_url(url):
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def validate_url_shape(url, allowed_hosts):
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname is None
        or parsed.hostname.lower() not in allowed_hosts
        or parsed.username
        or parsed.password
        or parsed.fragment
        or parsed.port not in (None, 443)
    ):
        raise ValueError("URL must be HTTPS on an approved exact host without credentials, fragment, or non-443 port")


def validate_public_dns(url, allowed_hosts):
    validate_url_shape(url, allowed_hosts)
    parsed = urllib.parse.urlsplit(url)
    addresses = {info[4][0] for info in socket.getaddrinfo(parsed.hostname, 443)}
    if not addresses or any(not ipaddress.ip_address(value).is_global for value in addresses):
        raise ValueError("URL host did not resolve exclusively to public addresses")


def bounded_json(request, expected_status, timeout):
    try:
        # Never follow an API redirect with the bearer token attached. The fixed
        # api.lumalabs.ai origin must answer directly or the request fails closed.
        with api_opener.open(request, timeout=timeout) as response:
            if response.status != expected_status:
                raise RuntimeError(f"Unexpected HTTP status {response.status}")
            raw = response.read(MAX_JSON_BYTES + 1)
    except urllib.error.HTTPError as exc:
        try:
            retry_after = exc.headers.get("Retry-After")
            detail = exc.read(64 * 1024).decode("utf-8", "replace")
        finally:
            exc.close()
        raise LumaHTTPError(exc.code, detail, retry_after) from exc
    if len(raw) > MAX_JSON_BYTES:
        raise RuntimeError("Luma JSON response exceeded configured cap")
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Luma response was not valid bounded JSON") from exc
    if not isinstance(value, dict):
        raise RuntimeError("Luma response was not a JSON object")
    return value


def api_request(method, path, key, payload=None, expected_status=200, timeout=90):
    body = None if payload is None else json.dumps(payload, separators=(",", ":")).encode("utf-8")
    headers = {"Authorization": f"Bearer {key}", "Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        f"{API_ROOT}{path}", data=body, method=method, headers=headers
    )
    return bounded_json(request, expected_status, timeout)


def safe_credit_balance(key):
    try:
        value = api_request("GET", "/credits", key)
        return float(value["credit_balance"])
    except (KeyError, TypeError, ValueError, RuntimeError, urllib.error.URLError) as exc:
        print({"credit_balance_warning": str(exc)})
        return None


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".luma-manifest-")
    try:
        with os.fdopen(fd, "wb") as output:
            fd = None
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    except Exception:
        if fd is not None:
            os.close(fd)
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def read_local_json(path):
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ValueError("Local ledger exceeded JSON cap")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Local ledger was not a JSON object")
    return value


def retry_after_seconds(value):
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


def get_generation_with_retry(generation_id, key, deadline, initial_wait=0.0):
    wait = max(0.0, initial_wait)
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("generation GET deadline exceeded")
        if wait:
            sleep_for = wait + random.random()
            if sleep_for >= remaining:
                raise TimeoutError("required generation GET delay exceeds remaining deadline")
            time.sleep(sleep_for)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("generation GET deadline exceeded after wait")
        try:
            return api_request("GET", f"/generations/{generation_id}", key,
                               timeout=max(0.001, min(90.0, remaining)))
        except LumaHTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504}:
                raise
            provider_wait = retry_after_seconds(exc.retry_after)
            wait = max(min(max(wait, 2.0) * 1.6, 30.0), provider_wait, 2.0)
        except (urllib.error.URLError, TimeoutError):
            wait = min(max(wait, 2.0) * 1.6, 30.0)


def download_image(url, allowed_hosts, directory, requested_format):
    opener = urllib.request.build_opener(NoRedirect())
    current = url
    response = None
    for _ in range(6):
        validate_public_dns(current, allowed_hosts)
        # Deliberately no LUMAAI_API_KEY header on any asset hop.
        request = urllib.request.Request(
            current, headers={"Accept": "image/jpeg,image/png"}
        )
        try:
            response = opener.open(request, timeout=90)
            break
        except urllib.error.HTTPError as exc:
            if exc.code in {301, 302, 303, 307, 308}:
                location = exc.headers.get("Location")
                exc.close()
                if not location:
                    raise ValueError("Artifact redirect omitted Location")
                current = urllib.parse.urljoin(current, location)
                continue
            try:
                detail = exc.read(64 * 1024).decode("utf-8", "replace")
            finally:
                exc.close()
            raise RuntimeError(f"Artifact HTTP {exc.code}: {detail}") from exc
    else:
        raise ValueError("Too many artifact redirects")

    directory.mkdir(parents=True, exist_ok=True)
    fd = None
    temporary = None
    total = 0
    prefix = b""
    hasher = hashlib.sha256()
    try:
        with response:
            mime = response.headers.get_content_type()
            if mime not in {"image/jpeg", "image/png"}:
                raise ValueError(f"Unexpected artifact MIME: {mime}")
            declared = response.headers.get("Content-Length")
            if declared:
                try:
                    if int(declared) > MAX_IMAGE_BYTES:
                        raise ValueError("Artifact exceeds declared-size cap")
                except ValueError as exc:
                    raise ValueError("Invalid or excessive Content-Length") from exc
            fd, temporary = tempfile.mkstemp(dir=directory, prefix=".luma-image-")
            with os.fdopen(fd, "wb") as output:
                fd = None
                while True:
                    chunk = response.read(64 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_IMAGE_BYTES:
                        raise ValueError("Artifact exceeded streaming byte cap")
                    prefix += chunk[: max(0, 12 - len(prefix))]
                    hasher.update(chunk)
                    output.write(chunk)
                output.flush()
                os.fsync(output.fileno())

        if prefix.startswith(b"\xff\xd8\xff"):
            expected_mime, expected_format, suffix = "image/jpeg", "JPEG", ".jpg"
        elif prefix.startswith(b"\x89PNG\r\n\x1a\n"):
            expected_mime, expected_format, suffix = "image/png", "PNG", ".png"
        else:
            raise ValueError("Artifact signature is neither JPEG nor PNG")
        if mime != expected_mime:
            raise ValueError("Artifact MIME/signature mismatch")
        requested_mime = {"jpg": "image/jpeg", "png": "image/png"}[requested_format]
        if mime != requested_mime:
            raise ValueError("Artifact MIME did not match the requested output format")

        try:
            with Image.open(temporary) as probe:
                dimensions = probe.size
                if dimensions[0] * dimensions[1] > MAX_IMAGE_PIXELS:
                    raise ValueError(f"Artifact exceeds pixel cap: {dimensions}")
                decoded_format = probe.format
                probe.verify()
            with Image.open(temporary) as probe:
                probe.load()
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
            raise ValueError("Artifact failed bounded full decode") from exc
        if decoded_format != expected_format:
            raise ValueError("Artifact decoder/signature mismatch")

        destination = directory / f"image{suffix}"
        os.replace(temporary, destination)
        temporary = None
        return {
            "path": str(destination),
            "bytes": total,
            "mime_type": mime,
            "dimensions": list(dimensions),
            "sha256": hasher.hexdigest(),
        }
    except Exception:
        if fd is not None:
            os.close(fd)
        try:
            if temporary is not None:
                os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


model = os.getenv("LUMA_MODEL", "photon-flash-1")
mode = os.getenv("LUMA_MODE", "text")
if model not in {"photon-1", "photon-flash-1"}:
    raise SystemExit("LUMA_MODEL must be photon-1 or photon-flash-1")
if mode not in {"text", "image-reference", "style-reference", "character-reference", "modify"}:
    raise SystemExit("Unsupported LUMA_MODE")

prompt = (
    "16:9 editorial product photograph of a cobalt ceramic tea set on warm white "
    "paper at dawn, tabletop camera height, soft overhead light, restrained cool "
    "shadows, clean negative space on the left, realistic glaze and contact shadows. "
    "No added lettering or logos."
)
payload = {
    "model": model,
    "prompt": prompt,
    "aspect_ratio": "16:9",
    "format": "png",
    "sync": False,
}

reference_urls = []
if mode != "text":
    try:
        reference_urls = json.loads(os.getenv("LUMA_REFERENCE_URLS_JSON", "[]"))
    except json.JSONDecodeError as exc:
        raise SystemExit("LUMA_REFERENCE_URLS_JSON must be a JSON array") from exc
    if not isinstance(reference_urls, list) or not all(isinstance(url, str) for url in reference_urls):
        raise SystemExit("LUMA_REFERENCE_URLS_JSON must contain only URL strings")
    expected = (1, 4) if mode in {"image-reference", "character-reference"} else (1, 1)
    if not expected[0] <= len(reference_urls) <= expected[1]:
        raise SystemExit(f"{mode} requires {expected[0]}..{expected[1]} reference URLs")
    input_hosts = host_set("LUMA_INPUT_HOSTS")
    if not input_hosts:
        raise SystemExit("Set LUMA_INPUT_HOSTS to the exact owned source hosts")
    for url in reference_urls:
        validate_url_shape(url, input_hosts)
    weight = float(os.getenv("LUMA_REFERENCE_WEIGHT", "0.8"))
    if not math.isfinite(weight):
        raise SystemExit("LUMA_REFERENCE_WEIGHT must be finite")
    if mode == "image-reference":
        payload["image_ref"] = [{"url": url, "weight": weight} for url in reference_urls]
    elif mode == "style-reference":
        payload["style_ref"] = [{"url": reference_urls[0], "weight": weight}]
    elif mode == "character-reference":
        payload["character_ref"] = {"identity0": {"images": reference_urls}}
    else:
        payload["modify_image_ref"] = {"url": reference_urls[0], "weight": weight}

body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
request_sha256 = hashlib.sha256(body).hexdigest()
client_job_key = os.getenv("LUMA_CLIENT_JOB_KEY", f"local-{request_sha256[:20]}")
display_payload = json.loads(json.dumps(payload))
for key in ("image_ref", "style_ref"):
    for value in display_payload.get(key, []):
        value["url"] = redact_url(value["url"])
if display_payload.get("character_ref"):
    display_payload["character_ref"]["identity0"]["images"] = [
        redact_url(url) for url in reference_urls
    ]
if display_payload.get("modify_image_ref"):
    display_payload["modify_image_ref"]["url"] = redact_url(reference_urls[0])

public_price_snapshot = {"photon-1": 0.015, "photon-flash-1": 0.004}[model]
print(json.dumps({
    "dry_run": os.getenv("SEND_LUMA_REQUEST") != "1",
    "client_job_key": client_job_key,
    "request": display_payload,
    "request_sha256": request_sha256,
    "conservative_public_unit_price_usd_snapshot_2026_07_09": public_price_snapshot,
    "price_requires_dashboard_verification": True,
}, indent=2))

if os.getenv("SEND_LUMA_REQUEST") != "1":
    raise SystemExit("Dry run only; set SEND_LUMA_REQUEST=1 after approving the paid call")
key = os.getenv("LUMAAI_API_KEY")
if not key:
    raise SystemExit("Set LUMAAI_API_KEY before the paid call")

job_token = hashlib.sha256(client_job_key.encode("utf-8")).hexdigest()[:20]
job_dir = OUT / job_token
ledger_path = job_dir / "job.json"
manifest_path = job_dir / "manifest.json"


def save_job(state, generation_id=None, failure_reason=None, note=None):
    value = {
        "client_job_key": client_job_key,
        "request_sha256": request_sha256,
        "model": model,
        "state": state,
        "generation_id": generation_id,
        "failure_reason": failure_reason,
        "note": note,
        "updated_unix": time.time(),
        "reference_url_sha256": [
            hashlib.sha256(url.encode("utf-8")).hexdigest() for url in reference_urls
        ],
    }
    atomic_write(ledger_path, json.dumps(value, indent=2).encode("utf-8"))


def claim_new_job():
    value = {
        "client_job_key": client_job_key,
        "request_sha256": request_sha256,
        "model": model,
        "state": "submitting",
        "generation_id": None,
        "failure_reason": None,
        "note": "Exclusive local claim created before any paid call",
        "updated_unix": time.time(),
        "reference_url_sha256": [
            hashlib.sha256(url.encode("utf-8")).hexdigest() for url in reference_urls
        ],
    }
    job_dir.mkdir(parents=True, exist_ok=True)
    fd = os.open(ledger_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            fd = None
            json.dump(value, output, indent=2)
            output.flush(); os.fsync(output.fileno())
    finally:
        if fd is not None: os.close(fd)

if reference_urls:
    for url in reference_urls:
        validate_public_dns(url, input_hosts)

if manifest_path.exists():
    print(json.dumps(read_local_json(manifest_path), indent=2))
    raise SystemExit("This client job is already complete; choose a new LUMA_CLIENT_JOB_KEY for a new paid job")

credit_before = None
deadline = time.monotonic() + MAX_POLL_SECONDS
if ledger_path.exists():
    existing = read_local_json(ledger_path)
    if existing.get("client_job_key") != client_job_key or existing.get("request_sha256") != request_sha256:
        raise SystemExit("Existing ledger does not match this client job/request")
    generation_id = existing.get("generation_id")
    if not generation_id:
        raise SystemExit(
            "Existing create has no confirmed generation ID; treat it as ambiguous and reconcile. "
            "Use a new explicit LUMA_CLIENT_JOB_KEY only after an operator approves a new paid job."
        )
    try: uuid.UUID(str(generation_id))
    except (ValueError, AttributeError) as exc:
        raise SystemExit("Existing ledger contains an invalid generation UUID") from exc
    try:
        generation = get_generation_with_retry(generation_id, key, deadline)
    except TimeoutError as exc:
        raise SystemExit("Resume GET deadline exceeded; keep the ID and reconcile later") from exc
else:
    try:
        claim_new_job()
    except FileExistsError as exc:
        raise SystemExit(
            "Another worker claimed this client job key; do not submit. Retry later to resume its ledger."
        ) from exc
    credit_before = safe_credit_balance(key)
    try:
        generation = api_request(
            "POST", "/generations/image", key, payload, expected_status=201, timeout=180
        )
    except (urllib.error.URLError, TimeoutError) as exc:
        save_job("ambiguous_create", note="Do not replay; reconcile recent generations and credits")
        raise SystemExit(
            "Ambiguous create outcome: do not replay; reconcile recent generations and credits"
        ) from exc
    generation_id = generation.get("id")
    try:
        uuid.UUID(str(generation_id))
    except (ValueError, AttributeError) as exc:
        save_job("invalid_create_response", note="Create returned no valid generation UUID")
        raise SystemExit("Create response lacked a valid generation UUID") from exc
    save_job("accepted", generation_id)

delay = 2.0
while True:
    state = generation.get("state")
    save_job(state, generation_id, generation.get("failure_reason"))
    if state == "completed":
        break
    if state == "failed":
        raise SystemExit(f"Luma generation failed: {generation.get('failure_reason')}")
    if state not in {"queued", "dreaming"}:
        raise SystemExit(f"Unexpected generation state: {state!r}")
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        save_job(state, generation_id, note="Polling deadline exceeded; reconcile later")
        raise SystemExit("Polling deadline exceeded; keep the ID and reconcile later")
    try:
        generation = get_generation_with_retry(generation_id, key, deadline, initial_wait=delay)
        delay = min(delay * 1.6, 10.0)
    except TimeoutError as exc:
        save_job(state, generation_id, note="Polling/retry deadline exceeded; reconcile later")
        raise SystemExit("Polling deadline exceeded; keep the ID and reconcile later") from exc

asset_url = (generation.get("assets") or {}).get("image")
if not asset_url:
    raise SystemExit("Completed generation has no assets.image URL")
asset_hosts = host_set("LUMA_ASSET_HOSTS", {"storage.cdn-luma.com"})
artifact = download_image(asset_url, asset_hosts, job_dir, payload["format"])
credit_after = safe_credit_balance(key)
delta_cents = None
if credit_before is not None and credit_after is not None:
    delta_cents = credit_before - credit_after

manifest = {
    "generation_id": generation_id,
    "state": generation.get("state"),
    "model_requested": model,
    "model_reported": generation.get("model"),
    "client_job_key": client_job_key,
    "request_sha256": request_sha256,
    "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
    "reference_url_sha256": [hashlib.sha256(url.encode("utf-8")).hexdigest() for url in reference_urls],
    "public_unit_price_snapshot_usd": public_price_snapshot,
    "credit_balance_before_cents": credit_before,
    "credit_balance_after_cents": credit_after,
    "observed_balance_delta_cents": delta_cents,
    "artifact": artifact,
    "review_status": "pending",
    "downstream_ai_notice": "required for every API user",
    "public_ai_disclosure_review": "required when output identifies or resembles a person",
}
atomic_write(manifest_path, json.dumps(manifest, indent=2).encode("utf-8"))
print(json.dumps(manifest, indent=2))
```

The balance delta is only attributable when no other job uses the account during the measurement window. Treat it as reconciliation evidence, not a universal tariff. If a new artifact host appears, do not weaken validation to “any HTTPS URL”; verify ownership and purpose, then add the exact host to configuration.

## Prompt, iterate, and review

Photon's first-party material recommends natural, detailed language and presents the family as capable of prompt adherence, iterative editing, text, and references. Those are provider claims. Convert them into a controlled production loop:

1. State deliverable and audience: hero image, packaging concept, editorial frame, poster, storyboard, or character key art.
2. Describe subject and action, then spatial layout and camera/viewpoint.
3. Specify light, palette, materials, environment, and one coherent style anchor.
4. Quote required visible text exactly and name its placement, hierarchy, and casing. Still require OCR and human proofreading.
5. Name only meaningful exclusions. Photon has no documented negative-prompt field; exclusions remain ordinary prompt language.
6. For references, map each input to one role and repeat immutable identity/product/brand features.
7. Generate a bounded exploration set. Select by the brief, not novelty alone.
8. Modify one semantic change per turn. Re-anchor to the approved source rather than repeatedly editing a drifting derivative.
9. Restart from the last approved artifact when identity, geometry, typography, or lighting accumulates drift.

Production heuristic: use a compact structured prompt such as “deliverable → subject/action → composition/camera → light/palette → materials/style → exact text → protected invariants.” This is not provider syntax.

Review decoded full-resolution pixels against the source and brief:

- **Brief:** deliverable, aspect, safe area, subject count, crop, hierarchy, negative space.
- **Reference/edit:** identity, product geometry, pose, label/logo, background, lighting, shadows, and every protected region.
- **Text:** OCR followed by human spelling, punctuation, casing, line-break, kerning, and legibility review.
- **Visual:** faces/hands, repeated structures, reflections, occlusion, perspective, material continuity, edge halos, noise, and compression.
- **Technical:** MIME/magic/decoder agreement, dimensions, pixel area, color/profile metadata, file size, hash, and storage lifetime.
- **Rights/safety:** source authorization, likeness consent, trademark context, moderation, disclosure, and provenance preservation.

Maintain a regression set for both models, every aspect ratio used, JPG/PNG, text-only, one/four image references, style, one/four character views, low/high modify weights, difficult color edits, moderation failures, 429, create timeout, poll timeout, redirects, corrupt MIME, oversized files, and expired input/output URLs.

## Failures, rate control, and cost

The [error guide](https://docs.lumalabs.ai/docs/errors) lists pre-submission validation failures and post-submission `failure_reason` values including moderation, inaccessible inputs, prompt processing, dispatch, job, and callback errors. Treat prompt/schema/auth/moderation/source-access failures as nonretryable until corrected. Treat GET timeouts, 429, and transient 5xx as retryable with capped exponential backoff, jitter, `Retry-After` when present, a total deadline, and concurrency admission control.

The [rate-limit page](https://docs.lumalabs.ai/docs/rate-limits) publishes, for the Build tier, 40 concurrent Photon/Photon Flash generations, 80 create requests per minute, and a $5,000 monthly usage limit; Scale is described only as higher. These are ceilings, not targets. Apply lower application caps per user, project, and day, and re-read the live account limits before launch.

The [credits endpoint](https://docs.lumalabs.ai/reference/getcredits) returns `credit_balance` in USD cents. The generation schema exposes no per-job cost. Estimate before submission, record pre/post balances for isolated canaries, reconcile invoices/dashboard, and alert on mismatches. The latest public Photon-specific prices found on 2026-07-09 conflict as described above; never hide the uncertainty. Separate Luma app credits from API credits.

## Artifact, credential, and source security

- Keep `LUMAAI_API_KEY` server-side, scoped to the integration, out of URLs, prompts, callbacks, logs, browsers, and output manifests. The API Terms require notice to Luma within 24 hours of discovering compromised credentials.
- Send bearer auth only to `api.lumalabs.ai`. Source images and generated CDN artifacts never receive it.
- Require owned HTTPS source hosts, public-network DNS, least-lived signed URLs, and no embedded user/password or fragments. Avoid submitting sensitive inputs that cannot safely be made provider-retrievable.
- Treat `assets.image` as a transport location, not durable storage. The public docs state no numeric lifetime. Download immediately, follow redirects manually, validate every hop, cap declared/running bytes, require MIME↔magic↔decoder agreement, enforce dimensions before full decode, scan per application policy, retain original bytes, hash, and atomically promote.
- Do not log signed queries. Revoke or expire source URLs after terminal state and generated URLs after acquisition when you control them.
- `DELETE /generations/{id}` deletes the generation resource, but the docs do not say that it revokes an asset URL or satisfies legal erasure. Do not claim either.
- Preserve provider-added watermark, content credentials, or provenance metadata. The Terms reserve Luma's right to embed them and forbid removal; the Photon API does not promise that any specific output will contain C2PA or a visible mark.

## Data, rights, and safety gate

Read the agreement that actually governs the account. As of the verification date:

- The [API Terms](https://lumalabs.ai/legal/api-terms-of-use) state that Luma will not use API Input or API Output to train, fine-tune, or develop its AI/ML models. This API-specific clause controls over conflicting general Terms language. It does **not** promise zero retention, zero human/automated moderation, zero Usage/Aggregated Data, or zero processing.
- The [Terms of Service](https://lumalabs.ai/legal/terms-of-service) say, as between the parties and to the greatest extent permitted by law, the customer owns Output and Luma assigns its interest. That does not convey third-party rights, guarantee uniqueness/copyrightability/noninfringement/accuracy, or by itself authorize commercial use. Commercial use requires an active paid subscription/Order that permits it.
- Public documents provide no fixed API Input/Output retention window or regional/data-residency endpoint. The [Privacy Policy](https://lumalabs.ai/legal/privacy) uses purpose- and law-based retention criteria, and enterprise processing may be governed by the [DPA](https://lumalabs.ai/learning-hub/legal/enterprise-dpa) and Order. Obtain written commitments for retention, deletion, subprocessors, residency, security, and incident response when required.
- The Terms define Prohibited Data to include GDPR Article 9 special categories, PHI, PCI data, COPPA/GLBA-regulated data, government IDs, and similar regulated data. Luma says the Services are not designed for HIPAA compliance and it is not a Business Associate. Do not submit such data.
- Inform every downstream API user that generated Output is AI-generated. Separately, obtain documented rights and consent for every source, face, likeness, character, logo, trademark, copyrighted work, and location; if Output identifies or resembles a person, the Terms require public AI disclosure. The Terms also prohibit misrepresenting Output as human-generated.
- The Terms contain a specific license affecting people depicted in uploaded photographs. Route real-person reference programs through counsel rather than assuming ordinary source ownership resolves every subject right.
- The [Content Moderation Policy](https://lumalabs.ai/legal/content-moderation-policy) and Terms prohibit categories including sexual/NSFW content, harmful or illegal content, hate/discrimination, infringement, deceptive deepfakes/impersonation, political manipulation/misinformation, fraud, child sexualization, and other abusive uses. Apply an application-level preflight and human review; provider moderation is not a rights clearance.
- API customers must bind downstream users to written restrictions at least as protective as Luma's AUP, operate a complaint process, and comply with Luma suspension/termination requests. The API Terms also prohibit using the API or Output to build AI training, fine-tuning, **evaluation**, or other model-development datasets.

Record an auditable manifest containing the brief ID, request/prompt hashes, model, reference hashes and rights/consent records, generation ID/state/failure, timestamps, output MIME/dimensions/hash, price source and estimate, observed credit delta, moderation/reviewer outcome, AI disclosure decision, provenance state, controlled storage path, retention/deletion schedule, and publication approval.

## First-party sources

Verified 2026-07-09:

- [Photon REST image guide](https://docs.lumalabs.ai/docs/image-generation)
- [Generate-image API reference](https://docs.lumalabs.ai/reference/generateimage)
- [Official OpenAPI repository](https://github.com/lumalabs/lumaai-api/blob/main/openapi.yaml)
- [Official Python SDK image guide](https://docs.lumalabs.ai/docs/python-image-generation)
- [Official JavaScript SDK image guide](https://docs.lumalabs.ai/docs/javascript-image-generation)
- [Generation, list, delete, and credits references](https://docs.lumalabs.ai/reference/getgeneration)
- [Errors](https://docs.lumalabs.ai/docs/errors) and [rate limits](https://docs.lumalabs.ai/docs/rate-limits)
- [Photon product page](https://lumalabs.ai/photon) and [Photon API changelog](https://docs.lumalabs.ai/changelog/luma-photon-photon-flash-api)
- [Luma app-versus-API credit separation](https://lumalabs.ai/learning-hub/dream-machine-support-pricing-information)
- [Official Luma API MCP repository](https://github.com/lumalabs/luma-api-mcp)
- [Current Luma brand/API note](https://lumalabs.ai/llm-info)
- [API Terms](https://lumalabs.ai/legal/api-terms-of-use), [Terms of Service](https://lumalabs.ai/legal/terms-of-service), [Privacy Policy](https://lumalabs.ai/legal/privacy), [Content Moderation Policy](https://lumalabs.ai/legal/content-moderation-policy), [Enterprise DPA](https://lumalabs.ai/learning-hub/legal/enterprise-dpa), and [Subprocessors](https://lumalabs.ai/legal/subprocessors)


