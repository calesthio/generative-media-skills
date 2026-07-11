---
name: twelvelabs-video-understanding
description: >-
  Use when an agent must make TwelveLabs do real video-understanding work:
  indexing footage, semantic/visual search across an archive, generating
  descriptions, summaries, chapters, highlights, and tags from video, producing
  multimodal embeddings, or wiring TwelveLabs into a media-production pipeline
  (NLE panels, logging, compliance review, metadata). Covers the current model
  families (Marengo for search/embeddings, Pegasus for video-to-text analysis),
  the v1.3 Video Understanding API (indexes, assets, tasks, search, analyze,
  embed), prompt construction for analysis, capability and format limits,
  pricing/quota math, output quality review (hallucination and timestamp
  accuracy), and privacy/rights obligations when footage shows real people.
  Not for generating or editing video pixels — this is analysis and retrieval.
---

# TwelveLabs video understanding

TwelveLabs builds **video foundation models** that read footage the way a human editor does — across visuals, on-screen text, motion, sound, speech, and music — and expose that understanding through a REST API, SDKs (Python, Node), an MCP server, and NLE plugins. This skill is for driving that platform to log, search, describe, segment, and tag video for production work. It is **not** a video *generator*; TwelveLabs does not synthesize or edit pixels.

All volatile facts below carry a **verification date**. Everything moves fast here — re-verify model names, limits, and pricing against `docs.twelvelabs.io` before quoting them to a user as current.

## When this skill applies

Reach for TwelveLabs when the job is any of:

- **Archive / footage search** — "find every shot where the CEO is on stage," "clips with a red car at night," "where does someone say 'quarterly earnings'." Natural-language, image, or combined queries against indexed video.
- **Logging & tagging** — auto-generate loggable metadata (who/what/where/action) for raw footage or dailies.
- **Segmentation** — chapters, scene breaks, highlights, speaker changes, sports plays, ad-break points.
- **Video-to-text** — summaries, descriptions, captions, Q&A over a clip, structured JSON extraction (e.g. shot lists, compliance flags).
- **Embeddings** — multimodal vectors for a custom recommender, dedup, similarity, or a RAG-over-video store.
- **Compliance / brand-safety review** — locate logos, on-screen text, spoken phrases, or sensitive content across a library.

**Do not** use it to create video, apply visual effects, transcode, or as a general speech-to-text tool (it does speech *understanding* for search/analysis, but a dedicated ASR is cheaper if plain transcripts are all you need).

## The two model families

*[Documented — docs.twelvelabs.io/docs/concepts/models, verified 2026-07-10]*

TwelveLabs is not one model. Pick by task:

| | **Marengo** | **Pegasus** |
|---|---|---|
| Purpose | Search + embeddings (retrieval) | Analysis + text generation |
| Output | Ranked video segments; vectors | Natural-language / structured text |
| Current version | **Marengo 3.0** (GA Nov 2025) | **Pegasus 1.5** (Apr 2026); 1.2 still available |
| You call it via | `/search`, `/embed` | `/analyze` |
| Modalities read | visual, audio, on-screen text/OCR, logos, speech, music | visual, audio, speech, on-screen text |

**Rule of thumb:** if the answer is *"which moments/videos?"* → Marengo (search). If the answer is *"tell me / describe / summarize / extract"* → Pegasus (analyze). Embeddings for your own vector DB → Marengo (embed). An index can enable one or both; enable only what you'll use, because each model you enable is billed at index time.

### Marengo 3.0 facts *[Documented, verified 2026-07-10]*

- Unifies video, image, audio, and text into one representation space; **512-dimensional** embeddings.
- Fine-grained: detects brand logos, small objects, on-screen text, shot techniques, and can count objects.
- Video input: **4 seconds to 4 hours**, **≤ 4 GB**, resolution **360×360 to 5184×2160**, aspect ratio between 1:1 and 1:2.4 (either orientation), any FFmpeg-decodable container.
- **36 languages plus English** for speech/search.
- Text query / text embedding input: up to **500 tokens** (raised from 77).
- Marengo **2.7 was sunset on 2026-03-30** — indexes built only on 2.7 can no longer be searched or have embeddings retrieved. If you inherit an old index, check its model version first.

### Pegasus 1.5 facts *[Documented, verified 2026-07-10]*

- Video-to-text over multiple modalities. Introduced (vs 1.2): **structured video segmentation**, multimodal prompts with up to **4 reference images**, per-clip time ranges (`start_time`/`end_time`), and a much larger context window.
- **Context window: 261,120 tokens** shared across input + output. **Max response: 98,304 tokens** (raised from 65,536 on 2026-05-28). Default response 4,096 tokens, set via `max_tokens`.
- Video input: **4 seconds to 2 hours**, **≤ 2 GB** (note: tighter than Marengo). The **synchronous** `/analyze` endpoint accepts clips up to **1 hour**; longer content uses the async analyze task.
- Direct video **URLs only** — no YouTube or cloud-share links.
- Pegasus 1.2 remains for general analysis; it has smaller token limits (≈2,000-token prompt, ≤4,096 response) and cheaper input pricing. Use 1.5 for segmentation, reference images, or long structured output; 1.2 to save cost on short simple prompts.

## The API in practice

*[Documented — base `https://api.twelvelabs.io`, version **v1.3**, verified 2026-07-10]*

Everything hangs off an **index**. An index is a collection of videos configured with the model(s) that will process them.

### Core object flow

```
Index  ──►  Asset / video upload  ──►  Indexing task (async)  ──►  ready video
                                                                      │
                     ┌────────────────────────────────────────────────┤
                     ▼                        ▼                        ▼
             /search (Marengo)        /analyze (Pegasus)        /embed (Marengo)
```

### 1. Create an index

Configure which models are enabled and which modalities each analyzes. Enabling Marengo makes videos searchable; enabling Pegasus makes them analyzable. Enable both only if you need both.

### 2. Upload & index a video (async)

Two paths, both real as of 2026-07-10:

- **Legacy single call** — `POST /v1.3/tasks` with `index_id` and either `video_url` (public URL up to **4 GB**) or `video_file` (local, up to **2 GB**; larger via the Multipart Upload API, up to **10 GB**). Optional `enable_video_stream` (default true; stores an HLS proxy) and `user_metadata` (JSON of string/int/float/bool tags — set these at upload so you can filter searches later). Returns a task `_id` and the `video_id`.
- **Newer asset-based flow** — `POST /assets` to register the media, then `POST /indexes/{index-id}/indexed-assets` to index it. This separates "the file exists" from "index it into this index," which is cleaner when the same asset feeds multiple indexes. *[Documented; the docs mark the single-call `/tasks` route as the older pattern — verified 2026-07-10. Confirm which your SDK version defaults to.]*

Indexing is **asynchronous**. Poll task status until `ready` (other states seen include `validating`, `pending`, `indexing`, and `failed`). SDKs offer `task.wait_for_done()` so you don't hand-roll the poll loop. **Processing takes real wall-clock time** — plan for minutes per video, more for long footage; never assume a just-uploaded video is immediately searchable.

### 3. Search (Marengo) — `POST /v1.3/search`

- **Query types:** text (natural language, ≤500 tokens), **image** (find visually similar moments; up to ~10 images), or **combined** text+image for precision.
- **`search_options`:** which modalities to match — `visual` and/or `audio`. Combine with `operator: "or"` (default, broader recall) or `"and"` (both must match, higher precision).
- **`transcription_options`:** `lexical`, `semantic`, or both — controls whether spoken-word matching is exact-phrase or meaning-based.
- **Scope:** one index per request. There is no cross-index search — design indexes around the archives you'll query together.
- **Results:** ranked segments with `video_id`, `start`/`end` (seconds), a relevance `score`/`confidence`, and `rank` (1 = best). Use the confidence tier and your own threshold to decide what's worth surfacing to an editor; low-confidence hits are candidates, not answers.

### 4. Analyze (Pegasus) — `POST /v1.3/analyze`

The single generative endpoint since **`/gist` and `/summarize` were removed on 2026-02-15**. `/analyze` produces *any* text you prompt for — summaries, chapter lists, action items, shot logs, compliance memos — and can return **structured JSON** via `response_format` (a JSON schema).

Key parameters *[Documented, verified 2026-07-10]*:

| Parameter | Notes |
|---|---|
| `video` / `video_id` | source: asset id, direct URL, or base64; `video_id` for pre-indexed (Pegasus 1.2 path) |
| `prompt` | the instruction |
| `prompt_v2` | structured prompt with reference images (Pegasus 1.5) |
| `temperature` | 0–1, default **0.2** — keep low for factual logging/compliance |
| `max_tokens` | 512–98,304 (1.5); 2–4,096 (1.2) |
| `stream` | NDJSON streaming, **default true** (`stream_start` → `text_generation` → `stream_end`) |
| `response_format` | JSON schema for deterministic structured output |
| `start_time`/`end_time` | analyze only a clip (1.5) |

Synchronous for clips ≤ 1 hour; for longer video or batch, use the async analyze task (batch supports up to 1,000 requests per call).

### 5. Embed (Marengo) — Embed API v2

*[Documented, verified 2026-07-10]* Two endpoints: a **synchronous** one for text, image, audio, and video **under 10 minutes**; an **asynchronous** one for audio/video up to **4 hours**. Async flow: `embed.v_2.tasks.create` → poll `retrieve` (`processing` → `ready`) → read vectors from `data`. Per-media pricing (see below). Store vectors in your own DB (Qdrant, Elastic, pgvector, etc.) — TwelveLabs gives you the embeddings; you own the index.

## Prompting Pegasus for production

Analysis quality is mostly a prompting problem. Heuristics below are production practice, not vendor guarantees.

*[Heuristic]*

- **Say what to ignore, not just what to find.** "Describe the on-field action; ignore crowd shots, replays, and graphics overlays" beats "describe the video."
- **Ask for timestamps explicitly and cross-check them.** Pegasus can report times, but timestamp precision is a known soft spot — for frame-accurate cuts, use Marengo *search* (which returns real segment boundaries) rather than trusting a time Pegasus writes into prose. Treat analyze timecodes as approximate until verified against search or the footage.
- **Force structure for anything downstream.** If a spreadsheet, bin, or edit-decision list consumes the output, use `response_format` with an explicit JSON schema and fixed enums. Free prose is for humans; JSON is for pipelines.
- **Low temperature for facts.** 0.1–0.3 for logging, compliance, and metadata; higher only for creative copy (marketing blurbs, teaser lines).
- **One question per call when precision matters.** Long multi-part prompts dilute attention; separate calls for "list the chapters" and "flag any brand logos" are more reliable and independently checkable.
- **Anchor claims to evidence.** Ask Pegasus to cite *what in the video* supports each statement ("quote the on-screen text," "name the sound you heard") so a reviewer can falsify hallucinations quickly.

### Example — footage logging to structured JSON *(illustrative example, not a required format)*

Intent: auto-log a 30-min interview reel so an assistant editor can populate bins.
Model: Pegasus 1.5, `temperature: 0.2`, `response_format` = schema below.

Prompt:
```
Log this interview footage for an editor. For each distinct segment, report:
the speaker (or "unknown"), the topic in <=8 words, whether the shot is a
close-up/medium/wide, and any on-screen lower-third text you can read verbatim.
Ignore color bars, slates, and dead air. If you cannot read text, use null —
do not guess names.
```
`response_format` schema (abridged):
```json
{ "type": "object", "properties": { "segments": { "type": "array", "items": {
  "type": "object",
  "properties": {
    "start": {"type":"number"}, "end": {"type":"number"},
    "speaker": {"type":["string","null"]},
    "topic": {"type":"string"},
    "shot_size": {"type":"string","enum":["close-up","medium","wide"]},
    "lower_third": {"type":["string","null"]}
  }, "required": ["start","end","topic","shot_size"] } } } }
```
Why: enums keep `shot_size` clean; `null` instead of a guessed name curbs hallucinated identities; the "verbatim / do not guess" instruction is the main defense against confident fabrication.
Likely failure modes: invented lower-third names (mitigated by the null rule), timestamps drifting by 1–3 s (verify against search before cutting), over-segmentation of a single continuous shot.
Variation: add `"brand_logos": {"type":"array"}` to double as a brand-safety pass, or drop `response_format` and ask for a prose synopsis for a producer.

### Example — precise clip retrieval for an edit *(illustrative example)*

Intent: pull every moment a specific product appears, for a sizzle reel.
Model: Marengo 3.0 search (not analyze — you need real segment boundaries).

Request shape:
```
POST /v1.3/search
index_id: <reel_index>
query_text: "close-up of the blue running shoe, product clearly visible"
search_options: ["visual"]
operator: "and"          # tighten precision; drop to "or" if recall is low
threshold / page_limit applied client-side on the returned score
```
Why visual-only + `and`: the target is a visual object, audio is irrelevant, and precision matters more than catching every borderline frame in a highlight reel.
Expected result: ranked segments with usable `start`/`end` you can push straight to a timeline (this is exactly what the Premiere plugin does under the hood).
Failure modes: the model matches similar-looking shoes (add an **image query** of the actual product to disambiguate — combined text+image is far stronger for a specific SKU); very brief appearances rank low (lower your threshold and review manually).

## Media-production integration patterns

*[Documented, verified 2026-07-10]*

- **Adobe Premiere Pro plugin** — panel with **Project / Ingest / Search / Segment / Settings** tabs. Ingest uploads and indexes as **proxy** files; Search returns a thumbnail grid you preview in the source monitor or drop onto the timeline with **in/out points already set**; Segment auto-generates chapters/highlights you can add as clips. Requires Premiere Pro CC 2024–2025; only footage ingested through the plugin is searchable; disable auto-scan on shared projects. This is the fastest path for editors who don't want to touch the API.
- **Avid Media Composer** integration exists *[first-party/community reports, 2026]* for the same ingest→search→cut loop in Avid shops.
- **MCP server** — exposes indexing, semantic search, analysis, and embeddings as MCP tools so an agent (Claude Desktop, Cursor, Windsurf, a custom agent, or the TwelveLabs Claude Code plugin) can "search video" and "analyze video" as first-class actions. Use this when *you* are the orchestrating agent rather than calling REST yourself.
- **Amazon Bedrock** — Marengo and Pegasus are available on Bedrock, useful when a shop is standardized on AWS/IAM and wants managed access.
- **MASV, Mux, Elastic, Qdrant, n8n** — transfer (set→editor handoff), streaming/compliance, and vector-store / automation glue around the core models.

## Capability limits & gotchas

*[Documented unless marked]*

- **Format/size ceilings differ by model** — Marengo up to 4 h / 4 GB, Pegasus up to 2 h / 2 GB, sync analyze up to 1 h. Uploads: URL ≤ 4 GB, local ≤ 2 GB single-call, ≤ 10 GB multipart. Check the *tighter* of the two limits for your task.
- **Async everywhere it matters** — indexing and long analyze/embed are jobs, not instant calls. Build polling/`wait_for_done` in; surface "processing" state to users.
- **One index per search.** Plan index boundaries around what you query together.
- **No pixel output.** No trims, transcodes, or renders — TwelveLabs tells you *where* and *what*; your NLE or ffmpeg does the cut.
- **Free plan constraints** *(verified 2026-07-10)*: 600 free indexing minutes, index accessible **90 days**, **100 videos/index**, 5 concurrent tasks. Not for sustained production.
- **Deprecations bite** — `/gist` and `/summarize` gone (2026-02-15); Marengo 2.7 sunset (2026-03-30); cloud-to-cloud integrations deprecated (2025-10-31). Old tutorials will reference dead endpoints.

## Pricing & quota math

*[Documented — Developer (pay-as-you-go) plan, `twelvelabs.io/pricing`, verified 2026-07-10. Re-verify before quoting; use the official pricing calculator for a real estimate.]*

| Operation | Price |
|---|---|
| Video indexing (one-time) | **$0.042 / min** |
| Storage/infra (monthly) | $0.0015 / min |
| Search API | **$4 / 1,000 queries** |
| Analyze — input video (Pegasus 1.5) | $0.0292 / min (1.2: $0.021/min) |
| Analyze — output text | **$0.0075 / 1,000 tokens** |
| Embed — video | $0.042 / min |
| Embed — audio | $0.0083 / min |
| Embed — image | $0.10 / 1,000 requests |
| Embed — text | $0.07 / 1,000 requests |

Worked estimate *(illustrative, 2026-07-10 rates)*: index **100 hours** of footage once = 6,000 min × $0.042 ≈ **$252** one-time, + ~$9/mo storage. Then 1,000 searches ≈ **$4**. A summary of a 20-min clip: 20 × $0.0292 (input) + ~2k output tokens × $0.0075/1k ≈ **$0.60/clip**. The cost driver in a logging pipeline is usually **analyze input-minutes**, not output tokens — analyze only the clips you must, and prefer *search* (per-query pricing) for pure retrieval.

Rate limits are **multi-dimensional** (separate video/audio/image/text budgets) and **tiered by monthly spend**; you start at Tier 1 on adding a payment method and auto-upgrade with spend, with a one-month grace period on downgrade. Exact RPM per tier isn't published as a stable figure — read `429` headers and back off rather than hard-coding assumptions. *[Documented structure; exact numbers not fixed — verified 2026-07-10.]*

## Output quality review

Never ship model output unreviewed. Two failure classes dominate:

**1. Hallucination in generative (Pegasus) output** *[Heuristic]*
Summaries and logs can state confident, plausible, wrong facts — invented names, misattributed quotes, events that didn't happen. Defenses: low temperature; "do not guess / use null" instructions; ask for evidence anchors (verbatim on-screen text, described sounds) so a reviewer can spot-check; keep prompts single-purpose. For anything with legal, compliance, or publication weight, **a human verifies against the footage** — treat Pegasus as a fast first-pass logger, not a source of record.

**2. Timestamp accuracy** *[Heuristic + documented limits]*
Times Pegasus writes *into prose* are approximate and can drift a few seconds — fine for a producer's chapter list, not for a frame-accurate cut. When boundaries must be right, get them from **Marengo search** results (`start`/`end`), which are the model's actual segment detections, and confirm on the timeline. Search confidence is a real signal: set a threshold, treat sub-threshold hits as leads to review, not results.

Also review: **completeness** (did it miss a segment? long video + small `max_tokens` truncates silently — check `finish_reason`), **language coverage** (36+ languages, but verify non-English speech matching on a sample), and **false positives in brand/compliance search** (visually similar ≠ the actual logo/product; confirm with an image query).

## Privacy, consent & rights

*[Documented — twelvelabs.io/privacy-policy — plus production obligation, verified 2026-07-10]*

Indexing footage of real people creates **biometric-adjacent processing** (faces, voices, identifiable individuals). TwelveLabs' policy makes the **customer responsible** for having a lawful basis and appropriate consent for the personal data they put through the service; TwelveLabs acts as processor and supports data-subject rights (access, correction, deletion, portability) for EEA/UK individuals.

Before indexing footage of identifiable people, the agent should:

- Confirm the user has **rights/releases** to the footage and a lawful basis to process faces/voices — biometric laws (e.g. Illinois BIPA, GDPR special-category data) can require explicit consent and carry real penalties. This is a **prohibited-to-assume** area: don't index third-party or scraped footage of people on the user's say-so without flagging the obligation.
- Prefer **minimal retention** — the Free plan already expires indexes at 90 days; for production, delete indexes/assets when the job ends. Note that as of **2026-04-26**, delete requests for referenced assets are denied by default, so plan deletion around dependencies.
- Avoid building **standing identity databases** ("find this named person across all footage forever") without a documented legal basis and the subject's consent — that's a facial-recognition use with heightened legal exposure, not routine logging.
- Keep generated metadata (which can assert who a person is / what they said) under the same review and access controls as the footage.

When a user asks to index or search footage of real people they may not have rights to, surface the consent/rights question rather than silently proceeding.

## Primary sources

*[All verified 2026-07-10]*

- Models overview & concepts — `https://docs.twelvelabs.io/docs/concepts/models`, `/models/marengo`, `/models/pegasus`
- Release notes (versions, sunsets, token limits) — `https://docs.twelvelabs.io/docs/get-started/release-notes`
- API introduction, search guide, analyze & embed references — `https://docs.twelvelabs.io/api-reference/introduction`, `/docs/guides/search`, `/api-reference/analyze-videos/analyze`, `/api-reference/create-embeddings-v2`
- Upload/tasks — `https://docs.twelvelabs.io/api-reference/upload-content/tasks/create`
- Pricing & rate limits — `https://www.twelvelabs.io/pricing`, `https://docs.twelvelabs.io/docs/get-started/rate-limits`
- Adobe Premiere plugin & partner integrations — `https://docs.twelvelabs.io/docs/resources/partner-integrations/adobe-premiere-pro-plugin`
- MCP server — `https://docs.twelvelabs.io/docs/advanced/model-context-protocol`, `https://www.twelvelabs.io/blog/twelve-labs-mcp-server`
- Marengo 3.0 launch — `https://press.aboutamazon.com/aws/2025/12/twelvelabs-launches-its-most-powerful-video-understanding-model-marengo-3-0-on-twelvelabs-and-amazon-bedrock`
- Privacy policy — `https://www.twelvelabs.io/privacy-policy`
- Python SDK — `https://github.com/twelvelabs-io/twelvelabs-python`
