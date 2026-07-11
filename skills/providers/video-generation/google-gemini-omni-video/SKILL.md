---
name: google-gemini-omni-video
description: Generate, reference, and conversationally edit short videos with Google's Gemini Omni Flash through the Gemini Developer API or Gemini Enterprise Agent Platform. Use when a task specifically needs Gemini Omni video, multimodal reference roles, time-directed prompting, audio-aware generation, Interactions API state, or a precise comparison with Veo, Nano Banana, consumer Gemini, or gateway routes.
---

# Google Gemini Omni video

Use this skill for the first-party Google model `gemini-omni-flash-preview`. Treat all availability, prices, limits, and preview behavior below as verified on **2026-07-10** and re-check the cited first-party pages before a production launch.

## Establish scope before acting

Ask which backend, data region, source media, edit mode, aspect ratio, desired duration, audio/dialogue, intended audience, rights status, and spend approval apply. Do not silently translate an Omni request into a different product.

| Surface | Contract in scope | Do not conflate it with |
|---|---|---|
| Gemini Developer API | `POST https://generativelanguage.googleapis.com/v1beta/interactions`; API/auth key; paid tier only for Omni | Consumer Gemini app, AI Studio UI behavior, or Google Cloud data controls |
| Gemini Enterprise Agent Platform | `POST .../v1beta1/projects/{project}/locations/{location}/interactions`; OAuth/IAM; Agent Platform API; exact host depends on verified location contract | A drop-in Developer API endpoint or the legacy Veo operation schema |
| Gemini Omni Flash | Native short video generation, references, audio generation, and conversational editing | Veo, which is a specialized video family with different endpoints and features such as extension/interpolation in supported Veo versions |
| Gemini native image (â€œNano Bananaâ€) | Separate image generation/editing models | Omni video output |
| Gemini app, Flow, YouTube | Consumer/creator products with their own access, settings, and terms | A promise about API retention, schema, availability, or provenance metadata |
| Third-party gateway/reseller | Out of scope for this skill | First-party Google billing, privacy, safety, or retry guarantees |

**FACT:** Gemini Omni Flash is a preview model, although the Interactions API itself is GA. The Developer API model page specifies text/image/video input, video output, a 1,048,576-token context, and 3â€“10 second 720p/24 FPS output. The Cloud model page publishes a different 131,072-token input limit and 57,920-token output limit. Apply limits only to the backend that documents them.

**FACT:** The Cloud preview page publishes a June 30, 2027 retirement date. The Developer API page does not promise the same lifecycle. Pin the model ID, monitor release notes, and keep a provider-bound migration test.

## Choose the backend deliberately

Use the Developer API for the shortest first-party integration and conversational state through an API key. New AI Studio keys are authorization keys bound to service accounts; unrestricted standard keys stopped working June 19, 2026, and all standard keys are scheduled for rejection in September 2026. Keep keys server-side, restrict them, and use `GEMINI_API_KEY` or `GOOGLE_API_KEY` (`GOOGLE_API_KEY` wins if both exist).

Use Gemini Enterprise Agent Platform when Cloud IAM, Cloud contracts, audit/security controls, GCS delivery, or Cloud data governance is required. Authenticate with Application Default Credentials or a short-lived OAuth access token. The dedicated Omni video guide currently shows `location=global`, whose endpoint gives no regional processing control. The newer Cloud deployment page, however, lists Omni under `eu` and `us` multi-regions and says those endpoints keep ML processing within the selected jurisdiction. Treat that as a first-party route-documentation conflict: for regulated workloads, use the `aiplatform.eu.rep.googleapis.com` or `aiplatform.us.rep.googleapis.com` Interactions route only after the project console, SDK smoke test, contract, or support confirms that exact Omni route; otherwise stop rather than falling back to global.

Do not infer Cloud availability from Developer availability or vice versa. As of the verification date, the Cloud model page itself is inconsistent: it marks Pay-as-you-go unsupported and fixed quota supported, yet also lists Standard PayGo in `global`. Treat Cloud consumption mode, quota allocation, and price as **UNKNOWN** until the project console or Google support confirms them. Do not submit a Cloud create based only on the Developer price.

## Apply the current capability contract

Developer API facts:

- Output is one 720p video with audio, 3â€“10 seconds, at 24 FPS; supported aspect ratios are `16:9` and `9:16` (landscape default).
- Tasks are `text_to_video`, `image_to_video`, `reference_to_video`, and `edit` under `generation_config.video_config.task`; omission lets the model infer.
- Each `previous_interaction_id` edit creates a new video. The parent interaction must be stored.
- For direct REST, read video content from `steps[].type == "model_output"`; `output_video` is an SDK convenience field.
- Generated videos include invisible SynthID. The Developer API guide does not promise C2PA. Cloud docs separately promise automatic C2PA signing for Omni output; non-C2PA-aware post-processing can invalidate it.
- English is evaluated; other languages are unevaluated. Generation time varies.
- Safety filters apply to prompt and output and depend on region. Interactions does not support custom safety settings.

Current Developer API exclusions:

- No audio-reference upload, voice editing, video extension, first/last-frame interpolation, multi-video reasoning, system instructions, `temperature`, `top_p`, stop sequences, dedicated `negative_prompts`, provisioned throughput, or YouTube media source.
- Video references up to 3 seconds pass the schema but are not processed correctly; do not use them.
- Uploaded-video editing is unavailable in the EEA, Switzerland, and UK; model-generated videos remain editable there.
- Image upload/edit involving minors is unsupported in the EEA, Switzerland, and UK. Some recognizable people are unsupported more broadly.

**DOCUMENTATION CONFLICT:** Googleâ€™s model card describes a native multimodal model that accepts audio, and the Developer pricing table lists audio input pricing, but the current Developer Omni guide expressly says uploaded audio references are unsupported. Follow the API guide: describe desired speech, music, ambience, and effects in text. The Cloud model page says audio is input-only, but verify the exact Cloud request guide before sending it.

**DOCUMENTATION CONFLICT:** The generic Interactions model table (updated 2026-07-09) omits Omni, while the dedicated Omni guide and changelog require Interactions. Use the dedicated guide and model endpoint, and keep a smoke test because this is a new preview.

## Plan cost, quota, and approval

Developer Omni has no free tier. The published standard prices are $1.50 per million input tokens for text/image/video/audio, $9 per million text output tokens, and $17.50 per million video output tokens including thinking. Google meters 720p output at 5,792 tokens/second, approximately $0.10/second. Exact video-only arithmetic is $0.10136/second; a 10-second output is $1.0136 before input and any text output.

Before every create or edit:

1. Count requested variants and turns; every edit produces another output and can incur another charge.
2. Show a conservative estimate: `turns Ã— ($1.0136 maximum video output + estimated inputs/text output)` for Developer API. Label this an estimate, not a hard provider cap.
3. Obtain explicit approval naming backend, number of paid creates, estimated maximum, retention choice, and source media.
4. Check live project limits in AI Studio. Limits are per project, vary by tier/model, are more restrictive for preview models, and are not guaranteed. Do not hard-code an RPM value.
5. Treat `429 RESOURCE_EXHAUSTED` as a capacity/quota signal. Honor any retry hint and back off polling/read operations; do not automatically replay a create with an unknown outcome.

## Secure source and artifact handling

- Require source/brand/performance rights and documented likeness consent; model acceptance is not clearance. Reject intimate abuse, impersonation, biometric/privacy violations, child exploitation, surveillance, and prohibited uses; escalate ads, public figures, politics, sensitive traits, and material decisions.
- Hash sources and record MIME/bytes in a source-output ledger. Content-validate, cap before reading/decoding, reject active/polyglot files, and keep uploads private. Never log keys, base64, signed URIs, secret-bearing prompts, or thoughts.
- Developer Files API uploads allow 2 GB per file and 20 GB per project, persist 48 hours, cannot be downloaded through that API, and can be manually deleted. Delete early after use.
- Developer paid Interactions default to 55-day storage, configurable to 7/14/28/55 days; delete by ID. `store=false` disables parent state/background. Separate abuse retention is 55 days and may involve authorized review. Paid content is not used for product improvement, but abuse logging remains; consumer/unpaid terms do not transfer.
- Cloud async retention is up to 14 days. No-training terms still have abuse/Advanced-AI/logging exceptions; isolated memory caching defaults to 24 hours unless disabled. Confirm agreement, exceptions, caching, and GCS IAM/residency/encryption/logging/lifecycle.
- Verify MP4 duration, dimensions, FPS, audio, full decode, size, and hash; review frames, dialogue, text, logos, faces, continuity, safety, and factual/brand claims before release.

## Build prompts that can be tested

Specify subject, action, environment, shot, lens/camera motion, lighting, palette, pacing, physics, and sound. For one shot, say `single continuous unbroken shot; no scene cuts`. Put exclusions in ordinary text: `No dialogue. No extra sound effects.`

Use natural timing or timecodes:

```text
Single continuous unbroken 9:16 shot; no scene cuts.
[0-3s] A paper kite rises above a quiet dawn beach; slow handheld push-in.
[3-6s] The kite crosses the sun and the camera tilts upward.
Audio: soft surf and light wind. No dialogue, no music.
Keep all lettering and logos out of frame.
```

Timecodes are prompt direction, not a frame-accurate editing guarantee. Inspect the result.

For image roles, keep media order stable and bind it explicitly:

- `<FIRST_FRAME>` uses the image as the starting frame.
- `<IMAGE_REF_N>` identifies a reference image; numbering begins at 0.
- For ambiguity, use Googleâ€™s explicit source/reference prefixes, such as `[# Sources <FIRST_FRAME>@Image1]` or `[# References <IMAGE_REF_0>@Image1]`.

Google shows multiple references but the Developer guide does not publish a numeric maximum. Do not invent one. The Cloud model page separately publishes up to 10 images per prompt.

For edits, make one change per turn: `Make the room lighting warmer. Keep everything else the same.` Identity, layout, motion, text, and audio consistency can drift across edits. The model card calls consistency across edits, complex motion, and perfect text known limitations; verify rather than claiming preservation.

## Use a safe Developer API workflow

Prefer URI delivery for output over 4 MB. Save the initial interaction ID and URI immediately: a later `GET /interactions/{id}` currently returns inline base64 even if the create requested URI, so the URI is guaranteed only in the initial response or SSE stream. Poll the corresponding File resource until `ACTIVE`; fail on `FAILED` or deadline; then download with authentication into a temporary file, validate, and atomically rename.

There is no documented Omni create idempotency key. Before `POST`, persist an attempt record containing a client attempt UUID, request hash, approval, and `posting` state. If the connection fails after submission and no interaction ID is available, mark `create_outcome_unknown`, stop, and reconcile project logs/billing with an operator. Never â€œretry just in case.â€ `GET`, file-state polling, and downloads are read-only and may use bounded jittered retries.

The following complete Python example covers text, stateful conversational, and separately staged uploaded-video editing. It defaults to offline dry-run and makes no paid call. Install `google-genai>=2.3.0` only for execution.

```python
#!/usr/bin/env python3
import argparse, base64, hashlib, http.client, ipaddress, json, os, random; import socket, ssl, subprocess, tempfile, threading, time, uuid; from decimal import Decimal, InvalidOperation; from fractions import Fraction
from pathlib import Path; from urllib.parse import parse_qs, urlsplit; MODEL = "gemini-omni-flash-preview"; ESTIMATED_MAX_USD = 1.10  # one 10s Developer turn; estimate, not a provider cap
MAX_VIDEO_BYTES = 80 * 1024 * 1024; MAX_TOOL_BYTES = 1024 * 1024; DOWNLOAD_HOST = "generativelanguage.googleapis.com"
def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
def claim_once(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(value, f, indent=2, sort_keys=True); f.flush(); os.fsync(f.fileno())
def read_record(path: Path) -> dict:
    if path.stat().st_size > MAX_TOOL_BYTES: raise RuntimeError("Attempt record size rejected")
    with path.open("rb") as source: raw = source.read(MAX_TOOL_BYTES + 1)
    if not raw or len(raw) > MAX_TOOL_BYTES: raise RuntimeError("Attempt record size rejected")
    value = json.loads(raw)
    if not isinstance(value, dict): raise RuntimeError("Attempt record must be an object")
    return value
def run_bounded(argv, timeout, cap=MAX_TOOL_BYTES):
    proc = subprocess.Popen(argv, shell=False, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE); out, err, lock, overflow = bytearray(), bytearray(), threading.Lock(), threading.Event()
    total = 0
    def drain(stream, bucket):
        nonlocal total
        while True:
            chunk = stream.read1(65536) if hasattr(stream, "read1") else stream.read(65536)
            if not chunk: break
            with lock:
                room = max(0, cap - total); bucket.extend(chunk[:room]); total += len(chunk)
                if total > cap: overflow.set()
            if overflow.is_set():
                try: proc.kill()
                except OSError: pass
    threads = [threading.Thread(target=drain, args=(proc.stdout, out), daemon=True), threading.Thread(target=drain, args=(proc.stderr, err), daemon=True)]
    for thread in threads: thread.start()
    timed_out = False
    try: code = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True; proc.kill(); code = proc.wait()
    for thread in threads: thread.join()
    return {"code": code, "stdout": bytes(out), "stderr": bytes(err), "timeout": timed_out, "overflow": overflow.is_set()}
class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, ip, timeout=30):
        super().__init__(host, 443, timeout=timeout, context=ssl.create_default_context()); self.ip = ip
    def connect(self):
        sock = socket.create_connection((self.ip, self.port), self.timeout); self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
def generated_file_name(uri: str) -> str:
    parsed = urlsplit(uri)
    if (parsed.scheme != "https" or parsed.hostname != DOWNLOAD_HOST or parsed.username or parsed.password or parsed.fragment or parsed.port not in (None, 443)):
        raise RuntimeError("Generated file URI policy rejected")
    prefix = "/v1beta/files/"
    if not parsed.path.startswith(prefix) or not parsed.path.endswith(":download"):
        raise RuntimeError("Generated file URI path rejected")
    name = parsed.path[len(prefix):-len(":download")]
    if not name or not name.isalnum() or parse_qs(parsed.query) != {"alt": ["media"]}:
        raise RuntimeError("Generated file URI identifier/query rejected")
    return "files/" + name
def download_generated(uri: str, api_key: str, parent: Path) -> Path:
    name = generated_file_name(uri).split("/", 1)[1]; addresses = sorted({item[4][0] for item in socket.getaddrinfo(DOWNLOAD_HOST, 443, type=socket.SOCK_STREAM)})
    if not addresses or any(not ipaddress.ip_address(item).is_global for item in addresses):
        raise RuntimeError("Generated file host did not resolve publicly")
    conn, temp_path = PinnedHTTPSConnection(DOWNLOAD_HOST, addresses[0], timeout=60), None
    try:
        conn.request("GET", f"/v1beta/files/{name}:download?alt=media", headers={"x-goog-api-key": api_key, "Accept": "video/mp4"}); response = conn.getresponse()
        if 300 <= response.status < 400: raise RuntimeError("Generated file redirects are rejected")
        if response.status != 200: raise RuntimeError(f"Generated file HTTP {response.status}")
        mime = response.getheader("Content-Type", "").split(";", 1)[0].lower()
        if mime != "video/mp4": raise RuntimeError("Generated file MIME rejected")
        length = response.getheader("Content-Length")
        if length is not None and (not length.isdigit() or int(length) > MAX_VIDEO_BYTES):
            raise RuntimeError("Generated file declared size rejected")
        fd, name_on_disk = tempfile.mkstemp(prefix=".omni-", suffix=".mp4", dir=parent); temp_path = Path(name_on_disk); total = 0
        with os.fdopen(fd, "wb") as f:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk: break
                total += len(chunk)
                if total > MAX_VIDEO_BYTES: raise RuntimeError("Generated file crossed byte cap")
                f.write(chunk)
            f.flush(); os.fsync(f.fileno())
        return temp_path
    except BaseException:
        if temp_path is not None and temp_path.exists(): temp_path.unlink()
        raise
    finally:
        conn.close()
def inline_generated(data: str, parent: Path) -> Path:
    if len(data) > ((MAX_VIDEO_BYTES + 2) // 3) * 4 + 4:
        raise RuntimeError("Inline video encoding exceeds byte cap")
    blob = base64.b64decode(data, validate=True)
    if not blob or len(blob) > MAX_VIDEO_BYTES: raise RuntimeError("Inline video size rejected")
    fd, name = tempfile.mkstemp(prefix=".omni-", suffix=".mp4", dir=parent)
    with os.fdopen(fd, "wb") as f: f.write(blob); f.flush(); os.fsync(f.fileno())
    return Path(name)
def validate_and_publish(temp_path: Path, destination: Path) -> dict:
    try:
        with temp_path.open("rb") as f: header = f.read(12)
        if len(header) < 12 or header[4:8] != b"ftyp": raise RuntimeError("MP4 signature rejected")
        probe = run_bounded(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate", "-of", "json", str(temp_path)], 30)
        if probe["timeout"] or probe["overflow"] or probe["code"] != 0: raise RuntimeError("ffprobe failed")
        metadata = json.loads(probe["stdout"]); streams = metadata.get("streams", []); videos = [item for item in streams if item.get("codec_type") == "video"]
        if len(videos) != 1 or not any(item.get("codec_type") == "audio" for item in streams):
            raise RuntimeError("Expected one video stream and generated audio")
        width, height = videos[0].get("width"), videos[0].get("height")
        if sorted((width, height)) != [720, 1280]: raise RuntimeError("Expected 720p dimensions")
        if abs(float(Fraction(videos[0].get("r_frame_rate", "0/1"))) - 24.0) > 0.1:
            raise RuntimeError("Expected 24 FPS")
        duration = float(metadata.get("format", {}).get("duration", 0))
        if not 2.9 <= duration <= 10.1: raise RuntimeError("Video duration outside 3-10 seconds")
        decode = run_bounded(["ffmpeg", "-v", "error", "-i", str(temp_path), "-f", "null", "-"], 300)
        if decode["timeout"] or decode["overflow"] or decode["code"] != 0: raise RuntimeError("Full decode failed")
        if destination.exists(): raise RuntimeError("Output already exists")
        digest = hashlib.sha256()
        with temp_path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""): digest.update(chunk)
        artifact = {"path": str(destination), "bytes": temp_path.stat().st_size, "sha256": digest.hexdigest(), "probe": metadata}; os.replace(temp_path, destination); temp_path = None
        return artifact
    finally:
        if temp_path is not None and temp_path.exists(): temp_path.unlink()
def retry_after(exc) -> float | None:
    response = getattr(exc, "response", None); headers = getattr(response, "headers", {}) or {}; raw = headers.get("retry-after") or headers.get("Retry-After")
    try: value = float(raw)
    except (TypeError, ValueError): return None
    return value if 0 <= value <= 60 else None
def safe_read(call, deadline, attempts=5):
    for attempt in range(attempts):
        try: return call()
        except Exception as exc:
            if attempt + 1 == attempts or time.monotonic() >= deadline: raise
            delay = retry_after(exc) or min(20.0, 2 ** attempt) * (1 + random.random() * .25)
            if time.monotonic() + delay >= deadline: raise
            time.sleep(delay)
def find_video(interaction):
    convenience = getattr(interaction, "output_video", None)
    if convenience: return convenience
    for step in getattr(interaction, "steps", []) or []:
        if getattr(step, "type", None) == "model_output":
            for item in getattr(step, "content", []) or []:
                if getattr(item, "type", None) == "video": return item
    raise RuntimeError("No video output in completed interaction")
def delete_remote_files(client, items) -> list[dict]:
    results = []
    for role, name in items:
        try:
            client.files.delete(name=name)  # one cleanup attempt; ambiguity is recorded for an operator; results.append({"role": role, "name": name, "status": "deleted"})
        except Exception as exc:
            results.append({"role": role, "name": name, "status": "delete_outcome_unknown", "errorType": type(exc).__name__})
    return results
def load_source_manifest(path: Path, jurisdiction: str | None) -> dict:
    if jurisdiction in {"eea", "ch", "uk"}:
        raise RuntimeError("Uploaded-video editing is unavailable in this jurisdiction")
    if jurisdiction != "other":
        raise RuntimeError("--source-jurisdiction other is required for an uploaded-video edit")
    if path.is_symlink() or not path.is_file(): raise RuntimeError("Source manifest path rejected")
    if path.stat().st_size > MAX_TOOL_BYTES: raise RuntimeError("Source manifest size rejected")
    with path.open("rb") as source_file: raw = source_file.read(MAX_TOOL_BYTES + 1)
    if not raw or len(raw) > MAX_TOOL_BYTES: raise RuntimeError("Source manifest size rejected")
    value = json.loads(raw)
    if not isinstance(value, dict): raise RuntimeError("Source manifest must be an object")
    required = {"name", "uri", "sha256", "bytes", "mime", "state", "deleteAfterUse", "durationSeconds", "localFullDecodePassed", "rightsApproved"}
    if set(value) != required: raise RuntimeError("Source manifest schema rejected")
    name = value["name"]
    if not isinstance(name, str) or not name.startswith("files/") or not name[6:].isalnum():
        raise RuntimeError("Source File resource name rejected")
    parsed = urlsplit(value["uri"] if isinstance(value["uri"], str) else "")
    if (parsed.scheme != "https" or parsed.hostname != DOWNLOAD_HOST or parsed.username or parsed.password or parsed.port not in (None, 443) or parsed.query or parsed.fragment or parsed.path != "/v1beta/" + name):
        raise RuntimeError("Source File URI rejected")
    sha = value["sha256"]
    if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
        raise RuntimeError("Source SHA-256 rejected")
    if (type(value["bytes"]) is not int or not 0 < value["bytes"] <= 2 * 1024 * 1024 * 1024 or value["mime"] != "video/mp4" or value["state"] != "ACTIVE" or value["deleteAfterUse"] is not True or value["localFullDecodePassed"] is not True or value["rightsApproved"] is not True):
        raise RuntimeError("Source validation/lifecycle assertions rejected")
    try: duration = Decimal(str(value["durationSeconds"]))
    except InvalidOperation as exc: raise RuntimeError("Source duration rejected") from exc
    if not duration.is_finite() or not Decimal("0") < duration <= Decimal("10"):
        raise RuntimeError("Uploaded source must be no longer than 10 seconds")
    return value
def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--prompt", required=True); p.add_argument("--aspect", choices=("16:9", "9:16"), default="16:9")
    p.add_argument("--stateful", action="store_true", help="store this turn so it can be edited later"); p.add_argument("--previous-id", help="stored parent interaction for a paid edit turn")
    p.add_argument("--source-manifest", type=Path, help="bounded manifest for an already ACTIVE, locally validated Developer File upload"); p.add_argument("--source-jurisdiction", choices=("other", "eea", "ch", "uk"))
    p.add_argument("--output", type=Path, default=Path("omni-output.mp4")); p.add_argument("--attempt-log", type=Path, default=Path("omni-attempt.json"))
    p.add_argument("--attempt-id", required=True, help="fresh canonical UUIDv4 used for this one paid turn"); p.add_argument("--execute", action="store_true")
    p.add_argument("--resume", action="store_true", help="read/query a claimed attempt; never create"); p.add_argument("--max-usd", default="1.10"); p.add_argument("--approval-sha256")
    p.add_argument("--show-full-plan", action="store_true"); a = p.parse_args()
    if not a.prompt.strip() or len(a.prompt.encode("utf-8")) > 8000:
        raise SystemExit("Prompt must be 1..8000 UTF-8 bytes")
    if a.output.suffix.lower() != ".mp4": raise SystemExit("Output must end in .mp4")
    try: attempt = uuid.UUID(a.attempt_id); maximum = Decimal(a.max_usd)
    except (ValueError, InvalidOperation) as exc: raise SystemExit("Attempt ID or maximum USD is invalid") from exc
    if attempt.version != 4 or str(attempt) != a.attempt_id.lower(): raise SystemExit("Attempt ID must be canonical UUIDv4")
    if not maximum.is_finite() or maximum <= 0 or maximum < Decimal("1.10"):
        raise SystemExit("Maximum USD must be finite, positive, and cover 1.10")
    output, attempt_log = a.output.resolve(), a.attempt_log.resolve()
    if output == attempt_log: raise SystemExit("Output and attempt record must differ")
    if a.source_jurisdiction and not a.source_manifest:
        raise SystemExit("--source-jurisdiction requires --source-manifest")
    if a.source_manifest and a.previous_id:
        raise SystemExit("Choose either an uploaded-video edit or a previous-interaction edit")
    source = load_source_manifest(a.source_manifest.resolve(), a.source_jurisdiction) if a.source_manifest else None
    request = { "model": MODEL, "input": a.prompt, "response_format": {"type": "video", "delivery": "uri", "aspect_ratio": a.aspect}, "background": False, "stream": False, "store": a.stateful or bool(a.previous_id), }
    if source:
        request["input"] = [{"type": "document", "uri": source["uri"]}, {"type": "text", "text": a.prompt}]; request["generation_config"] = {"video_config": {"task": "edit"}}
    if a.previous_id: request["previous_interaction_id"] = a.previous_id
    request_hash = hashlib.sha256(canonical(request)).hexdigest()
    envelope = {"backend": "gemini-developer-api", "endpoint": "/v1beta/interactions", "model": MODEL, "request": request, "sourceHashes": ([] if not source else [{"sha256": source["sha256"], "bytes": source["bytes"], "mime": source["mime"], "fileName": source["name"], "jurisdiction": a.source_jurisdiction, "deleteAfterUse": True}]), "attemptId": str(attempt), "attemptRecord": str(attempt_log), "outputPolicy": {"path": str(output), "mime": "video/mp4", "maxBytes": MAX_VIDEO_BYTES, "ffprobe": True, "fullDecode": True, "requireAudio": True}, "cost": {"estimatedMaxUsd": "1.10", "approvedMaxUsd": format(maximum, "f"), "priceAsOf": "2026-07-10", "paidCreates": 1}, "retention": {"storeInteraction": request["store"], "previousInteractionId": a.previous_id}}
    approval = hashlib.sha256(canonical(envelope)).hexdigest(); redacted_input = f"sha256:{hashlib.sha256(a.prompt.encode()).hexdigest()}"
    if source:
        redacted_input = [{"type": "document", "uriSha256": hashlib.sha256(source["uri"].encode()).hexdigest()}, {"type": "text", "sha256": hashlib.sha256(a.prompt.encode()).hexdigest()}]
    safe_envelope = {**envelope, "request": {**request, "input": redacted_input}}; print(json.dumps({"dry_run": not a.execute, "approval_sha256": approval, "plan": safe_envelope}, indent=2))
    if a.show_full_plan: print(json.dumps({"protected_full_envelope": envelope}, indent=2))
    if not a.execute: return 0
    if a.approval_sha256 != approval: raise SystemExit("Exact approval hash mismatch")
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY or GOOGLE_API_KEY server-side")
    from google import genai; from google.genai import types; create_client = genai.Client(api_key=api_key, http_options=types.HttpOptions( timeout=600000, retry_options=types.HttpRetryOptions(attempts=1)))
    read_client = genai.Client(api_key=api_key, http_options=types.HttpOptions( timeout=30000, retry_options=types.HttpRetryOptions(attempts=1)))
    if source:
        info = safe_read(lambda: read_client.files.get(name=source["name"]), time.monotonic() + 120); state = getattr(getattr(info, "state", None), "name", getattr(info, "state", None))
        if state != "ACTIVE" or getattr(info, "uri", None) != source["uri"]:
            raise RuntimeError("Approved source upload is not the same ACTIVE File resource")
    if a.resume:
        if not attempt_log.exists(): raise SystemExit("Resume record does not exist")
        record = read_record(attempt_log)
        if (record.get("attempt_id") != str(attempt) or record.get("approval_sha256") != approval or record.get("request_sha256") != request_hash):
            raise SystemExit("Resume record does not match this exact approval")
        interaction_id = record.get("interaction_id")
        if not isinstance(interaction_id, str) or not interaction_id:
            raise SystemExit("Create outcome is unknown without an interaction ID; do not replay")
        interaction = safe_read(lambda: read_client.interactions.get(interaction_id), time.monotonic() + 120)
    else:
        record = {"attempt_id": str(attempt), "backend": "gemini-developer-api", "model": MODEL, "approval_sha256": approval, "request_sha256": request_hash, "status": "posting", "approved_max_usd": format(maximum, "f"), "interaction_id": None, "source_file_name": source["name"] if source else None, "output_uri_sha256": None, "created_unix": int(time.time())}
        try: claim_once(attempt_log, record)
        except FileExistsError as exc: raise SystemExit("Attempt is already claimed; use --resume, never replay") from exc
        try:
            interaction = create_client.interactions.create(**request)  # exactly one network attempt
        except Exception as exc:
            record.update(status="create_outcome_unknown", error_type=type(exc).__name__, updated_unix=int(time.time())); atomic_json(attempt_log, record)
            raise RuntimeError("Create outcome unknown; reconcile logs/billing, do not retry") from exc
        interaction_id = getattr(interaction, "id", None)
        if not isinstance(interaction_id, str) or not interaction_id:
            record.update(status="create_outcome_unknown", error_type="MissingInteractionId"); atomic_json(attempt_log, record)
            raise RuntimeError("Create returned no interaction ID; do not retry")
        record.update(interaction_id=interaction_id, status="interaction_id_saved", updated_unix=int(time.time())); atomic_json(attempt_log, record)  # first action after create: preserve provider identity
    video = find_video(interaction); uri = getattr(video, "uri", None); data = getattr(video, "data", None)
    if uri:
        file_name = generated_file_name(uri); record.update(status="output_uri_saved", output_uri_sha256=hashlib.sha256(uri.encode()).hexdigest(), generated_file_name=file_name, updated_unix=int(time.time()))
        atomic_json(attempt_log, record)
    else: file_name = None
    if uri:
        deadline = time.monotonic() + 900
        while True:
            info = safe_read(lambda: read_client.files.get(name=file_name), deadline); state = getattr(getattr(info, "state", None), "name", getattr(info, "state", None))
            if state == "ACTIVE": break
            if state == "FAILED": raise RuntimeError("Provider file processing failed")
            if state not in {"PROCESSING", "PENDING", None}: raise RuntimeError(f"Unknown file state {state!r}")
            if time.monotonic() >= deadline: raise TimeoutError("File processing exceeded 15 minutes")
            time.sleep(5 + random.random())
        output.parent.mkdir(parents=True, exist_ok=True); temp_path = download_generated(uri, api_key, output.parent)
    elif data:
        output.parent.mkdir(parents=True, exist_ok=True); temp_path = inline_generated(data, output.parent)
    else:
        raise RuntimeError("Video has neither URI nor data")
    try:
        artifact = validate_and_publish(temp_path, output)
    except BaseException as exc:
        cleanup_items = ([] if not file_name else [("generated_output", file_name)])
        if source: cleanup_items.append(("uploaded_source", source["name"]))
        cleanup_results = delete_remote_files(read_client, cleanup_items); cleanup_unknown = any(item["status"] != "deleted" for item in cleanup_results)
        record.update(status="artifact_validation_failed_cleanup_pending" if cleanup_unknown else "artifact_validation_failed", error_type=type(exc).__name__, remote_file_cleanup=cleanup_results, cleanup_action=("Inspect/delete the recorded File resources; do not replay create" if cleanup_unknown else None), updated_unix=int(time.time()))
        atomic_json(attempt_log, record); raise
    cleanup_items = ([] if not file_name else [("generated_output", file_name)])
    if source: cleanup_items.append(("uploaded_source", source["name"]))
    record.update(status="artifact_saved_cleanup_pending" if cleanup_items else "artifact_saved", artifact=artifact, retention=envelope["retention"], rights_review="required", creative_qa="pending", synthetic_disclosure="required", synthid_expected=True, developer_c2pa="not_documented", updated_unix=int(time.time()))
    atomic_json(attempt_log, record)
    if cleanup_items:
        cleanup_results = delete_remote_files(read_client, cleanup_items); cleanup_unknown = any(item["status"] != "deleted" for item in cleanup_results)
        record.update(status="artifact_saved_cleanup_pending" if cleanup_unknown else "artifact_saved", remote_file_cleanup=cleanup_results, cleanup_action=("Inspect/delete the recorded File resources; do not replay create" if cleanup_unknown else None), updated_unix=int(time.time()))
        atomic_json(attempt_log, record)
        if cleanup_unknown:
            raise RuntimeError("Artifact saved, but remote File cleanup needs operator reconciliation")
    print(json.dumps(record, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
```

Dry-run first:

```bash
python omni_generate.py --attempt-id "7f8f06b7-9e68-4f0a-bf16-3eaf3ee9d6c4" --prompt "Single continuous shot of rain on a greenhouse roof. Audio: rain only. No dialogue."
```

After approval, execute exactly one paid turn:

```bash
python omni_generate.py --execute --approval-sha256 "<exact unchanged digest>" --max-usd 1.10 --attempt-id "7f8f06b7-9e68-4f0a-bf16-3eaf3ee9d6c4" --prompt "Single continuous shot of rain on a greenhouse roof. Audio: rain only. No dialogue."
```

For a first turn you intend to edit, add `--stateful` before dry-run and keep it unchanged for execution; a default standalone result is stateless and cannot later become a parent. Record the retention choice in approval. Recover a known interaction with the same arguments plus `--resume --execute`; resume never enters the create branch.

For image input, replace `input` with ordered items and set the task explicitly:

```python
request["input"] = [
    {"type": "image", "data": base64.b64encode(image_bytes).decode(), "mime_type": "image/png"},
    {"type": "text", "text": "<FIRST_FRAME> single unbroken shot; the paper boat drifts forward. Keep its design unchanged. Audio: creek only."},
]
request["generation_config"] = {"video_config": {"task": "image_to_video"}}
```

Before image substitution, bound/content-validate/hash bytes and approve rights. For uploaded-video edit, separately approve staging: reject symlinks/polyglots, cap at 2 GB, require MP4 â‰¤10 seconds, bounded-probe/full-decode/hash, upload once, then poll `PROCESSING â†’ ACTIVE|FAILED`. Record Googleâ€™s exact values:

```json
{"name":"files/abc123","uri":"https://generativelanguage.googleapis.com/v1beta/files/abc123","sha256":"<64 lowercase hex>","bytes":1234567,"mime":"video/mp4","state":"ACTIVE","deleteAfterUse":true,"durationSeconds":8.0,"localFullDecodePassed":true,"rightsApproved":true}
```

Pass `--source-manifest source.json --source-jurisdiction other` unchanged to dry-run/execution; use protected `--show-full-plan` to inspect exact prompt/URI. Execution rechecks the ACTIVE URI, uses document input, and deletes source/generated Files after validation. Record ambiguous create/cleanup for reconciliation, never replay. Stop in `eea`, `ch`, or `uk`; never use the broken â‰¤3-second reference path.

## Use the Cloud contract separately

Cloudâ€™s documented synchronous request supports explicit `duration` strings from `3s` through `10s`, GCS URI delivery, and a list-valued `response_format`. Do not copy these fields into Developer code without checking its reference.

Use this fail-closed transaction contract only after the exact project route, quota mode, and price have been verified; until then, prepare a dry-run but do not offer a generic production request:

1. Require a canonical UUIDv4 attempt ID, exact project/location/origin, private GCS prefix, full request JSON, output path/policy, current price evidence, finite positive estimate, and finite covering maximum. Canonicalize those fields and print their SHA-256; execution requires the unchanged digest, not a boolean approval.
2. Default to offline dry-run: no ADC lookup, directory creation, GCS call, or network. For execution, use OAuth/ADC and a fresh mode-0700 attempt directory created atomically. If it exists, fail; a separately selected resume branch may only GET a durable known interaction ID.
3. Send one bounded POST with no automatic retry. Put the protected request body in a mode-0600 attempt-local temporary file so prompt/media details are not exposed in the process list. Persist the returned ID immediately. A timeout or parse failure without a durable ID becomes `create_outcome_unknown`; reconcile rather than replay.
4. Bound GET retries and honor `Retry-After`. Persist only a protected interaction ID, request/approval hash, exact cleanup URI, response hash, and sanitized stateâ€”never the raw response or model thoughts. Require exactly one returned video URI under the approved GCS prefix.
5. Bound metadata, download, and tool time/output. Require `video/mp4`, a declared and observed byte cap, MP4 `ftyp` magic, exactly one 720p/approximately-24-FPS video stream, generated audio, 3â€“10 second duration, bounded `ffprobe`, full bounded `ffmpeg` decode, and a successful current `c2patool` validation. Refuse an existing destination; publish by atomic rename and hash.
6. After the local artifact and protected manifest are durable, delete the GCS object with a bounded call. If deletion is ambiguous, leave `artifact_saved_cleanup_pending` with the exact URI; never create again to solve cleanup. Revalidate C2PA after any publication transform.

For `background:true`, apply the same create/identity rules and bounded read-only polling; Cloud documents async retention up to 14 days. The controlling Cloud agreement, abuse-monitoring exception, optional request/response logging, 24-hour in-memory cache setting, bucket IAM/residency/retention, and interaction/object deletion remain separate approval fields.

## Handle failures by phase

- **Preflight/schema/auth/region:** fix configuration; no create occurred if the service conclusively rejects before acceptance.
- **Create returns an ID:** persist it and poll/read that interaction; never create a replacement merely because generation is slow.
- **Create connection failure without ID:** outcome is unknown; stop and reconcile. There is no documented idempotency key.
- **Safety block:** do not weaken or evade controls. Revise only if the request is legitimate and compliant; escalate ambiguous likeness/rights cases.
- **File `PROCESSING`:** bounded polling with jitter; `FAILED` is terminal. URI loss cannot be repaired by assuming `GET interaction` will return it.
- **Artifact validation failure:** quarantine the output and retain metadata; do not publish. A fresh paid turn requires a new approval.
- **Preview drift or 404/unsupported field:** re-open the model page, Omni guide, changelog, and backend reference; do not guess a replacement model.

## Separate evidence from judgment

Use these labels in plans and reports:

- **FACT:** directly documented current API behavior, model limit, price, policy, or term.
- **PROVIDER CLAIM:** Googleâ€™s qualitative statements or internally reported benchmark/model-card results; do not present them as independent proof.
- **OBSERVATION:** a result from a dated local dry-run or paid test, including backend, model ID, SDK version, region, and request hash.
- **HEURISTIC:** prompt advice such as one edit per turn or â€œkeep everything else the same.â€
- **UNKNOWN:** undocumented maximum reference count on Developer API, hard latency SLA, create idempotency, Developer C2PA, Cloud consumption-mode conflict, or any unverified SDK behavior.

## Re-verify these first-party sources

- Developer guide and prompt syntax: https://ai.google.dev/gemini-api/docs/omni
- Developer model details: https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash
- Interactions state/retention/SDK floor: https://ai.google.dev/gemini-api/docs/interactions-overview
- Pricing and live limits: https://ai.google.dev/gemini-api/docs/pricing and https://ai.google.dev/gemini-api/docs/rate-limits
- Files API: https://ai.google.dev/gemini-api/docs/files
- API keys: https://ai.google.dev/gemini-api/docs/api-key
- Release notes: https://ai.google.dev/gemini-api/docs/changelog
- Terms, regions, and abuse monitoring: https://ai.google.dev/gemini-api/terms, https://ai.google.dev/gemini-api/docs/available-regions, and https://ai.google.dev/gemini-api/docs/usage-policies
- Prohibited use: https://policies.google.com/terms/generative-ai/use-policy
- DeepMind product and model card: https://deepmind.google/models/gemini-omni/ and https://deepmind.google/models/model-cards/gemini-omni-flash/
- Cloud model/backend: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/omni-flash-preview and https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-text
- Cloud C2PA and endpoint residency: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/content-credentials and https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations


