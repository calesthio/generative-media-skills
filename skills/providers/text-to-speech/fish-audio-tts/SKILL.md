---
name: fish-audio-tts
description: >-
  Produce speech and clone voices with Fish Audio — its hosted TTS API (S2.1-Pro / S2-Pro / S1 model lineup, REST + WebSocket streaming, instant and persistent voice cloning) and its open-weight OpenAudio S1-mini / Fish-Speech models for self-hosting. Use this skill when an agent must generate narration or dialogue through Fish Audio, choose between Fish Audio's hosted models and open weights, clone a voice from reference audio, author emotion/tone/special markers for expressive delivery, estimate cost from UTF-8 bytes, wire real-time streaming for a voice agent, decide whether self-hosting beats the API, or review Fish Audio TTS output for production. Do not use it to pick a different provider — it covers Fish Audio specifically.
---

# Fish Audio text-to-speech and voice cloning

Fish Audio is a TTS and voice-cloning provider with two distinct product surfaces that share a lineage but differ in licensing and operation:

1. **Hosted API** (`api.fish.audio`) — the commercial service. Current lineup is branded **S2.1-Pro / S2-Pro / S1**. Paid per UTF-8 byte, streaming, cloning, and a free tier.
2. **Open weights** — released under the **OpenAudio** brand (and earlier as **Fish-Speech**). Downloadable from Hugging Face and GitHub for self-hosting.

The single most important fact to get right: **the hosted API and the open weights are not the same models, and their licenses differ**. The full flagship weights are hosted-only; only smaller distilled weights are openly published, and those carry a **non-commercial** license. Never assume "Fish is open source, so I can self-host it commercially" — verify which artifact and which license apply. See *Open weights and self-hosting* below.

All model names, prices, endpoints, and limits below are volatile. **Verification date for every dated claim in this document: 2026-07-10.** Re-verify against `docs.fish.audio` before quoting these to a user as current.

Labels used throughout:
- **[Doc]** — stated in official Fish Audio / OpenAudio documentation, model cards, or their published technical reports.
- **[Claim]** — a first-party marketing or benchmark claim from Fish Audio/OpenAudio; treat as their assertion, not independently established.
- **[Heuristic]** — a production judgment from practice, not a documented guarantee.

---

## When to use Fish Audio (and when not to)

**Reach for Fish Audio when:**
- You need low-cost, expressive multilingual TTS with strong voice cloning from short reference audio.
- You want fine-grained emotional/paralinguistic control through inline markers, not just SSML prosody.
- You need a real-time streaming voice for an agent (WebSocket, sub-second time-to-first-audio). **[Claim]**
- You want the *option* to self-host later, or to prototype locally on the open weights before committing to the API.

**Prefer something else when:**
- You need certified, contractual voice likeness rights for a specific celebrity/brand voice — Fish Audio does not pre-clear individual use cases and puts the consent burden on you. **[Doc]**
- Your deployment is commercial and you specifically want to run *self-hosted open weights* — the published weights are non-commercial-licensed, so commercial self-hosting needs the hosted API or a separate commercial license. **[Doc]**
- You need a provider with a formal, audited enterprise compliance posture (e.g., signed BAA/DPA guarantees on the free tier) — the free tier explicitly carries no such guarantees. **[Doc]**
- The languages you need fall outside the S1 supported set (see *Languages*) and you need documented, tested quality there.

This skill does not choose *between providers*. If the user is still deciding whether to use Fish Audio at all versus ElevenLabs, Cartesia, etc., surface the tradeoffs but recognize a provider-comparison skill governs that decision.

---

## Hosted API

### Endpoints [Doc, 2026-07-10]
- **REST (batch/stream):** `POST https://api.fish.audio/v1/tts`
- **WebSocket (bidirectional streaming):** `wss://api.fish.audio/v1/tts/live`
- **Create voice model (cloning):** `POST https://api.fish.audio/model`
- **ASR / transcription:** `transcribe-1` model (separate endpoint; $0.36 per audio hour).

Required headers on TTS calls: `Authorization: Bearer <FISH_API_KEY>`, `model: <model-name>`, and `Content-Type: application/json` or `application/msgpack`. The `model` header — **not** a body field — selects the model. **[Doc]**

### Model lineup [Doc, 2026-07-10]

| Model header value | Role | Marker syntax | Notes |
|---|---|---|---|
| `s2.1-pro` | Recommended for production | square-bracket tags `[...]` | Improved quality, latency, throughput over S2-Pro. **[Claim]** |
| `s2.1-pro-free` | Free tier, same weights as `s2.1-pro` | `[...]` | $0. No time-to-first-audio (TTFA) or DPA guarantees. For dev/prototyping/smaller use. **[Doc]** |
| `s2-pro` | Previous-generation default | `[...]` | Multi-speaker, natural-language expression control. **[Doc]** |
| `s1` | Earlier generation | parenthesis tags `(...)` | Emotion markers via parentheses. **[Doc]** |

**Critical marker-syntax difference [Heuristic, grounded in Doc]:** S1 uses **parentheses** — `(excited)`, `(whispering)`. The S2 family uses **square brackets** — `[excited]`, `[whispers]`. Markers written for the wrong model are often read aloud literally or ignored. Match marker syntax to the `model` header.

**"OpenAudio S1" ≠ the hosted `s1` model.** OpenAudio S1 is the open-weight release brand (below). The hosted `s1` is the corresponding hosted endpoint. Keep the two mentally separate when a user says "S1."

### Core request parameters [Doc, 2026-07-10]

| Parameter | Type / range | Purpose |
|---|---|---|
| `text` | string | Content to synthesize. In WebSocket mode, usually empty at `start` and streamed via `text` events. |
| `reference_id` | string | ID of a saved voice (library or a cloned model). |
| `references` | array | Instant cloning: raw reference audio + transcript inline, no persistent model. |
| `format` | `mp3` (default), `wav`, `pcm`, `opus` | Output container. |
| `mp3_bitrate` | 64 / 128 / 192 | MP3 quality. |
| `sample_rate` | Hz | For WAV output. |
| `speed` | 0.5–2.0 | Speech rate. |
| `latency` | `normal` (default) / `balanced` | `balanced` trades a little stability for lower latency. |
| `chunk_length` | 100–300 (default 200) | Text batching size per synthesis chunk. |
| `normalize` | boolean | Expands numbers/dates/abbreviations for natural reading. |
| `temperature` | float | Lower = more deterministic/stable. |
| `top_p` | float | Sampling diversity. |
| `repetition_penalty` | >1.0 | Suppresses looping/repeated artifacts. |
| `max_new_tokens` | int | Caps audio length per chunk. |

**Format selection [Heuristic]:** `wav` or `pcm` for downstream editing and telephony pipelines; `opus` for streaming to browsers/mobile; `mp3` when you just need a portable file. `pcm` avoids container/decoder latency in real-time loops.

### Streaming

Three generation modes in the Python SDK **[Doc]**:
- `tts.convert()` — returns complete audio bytes (simplest; use for files/batch).
- `tts.stream()` — iterator of audio chunks (memory-efficient long-form).
- `tts.stream_websocket()` — real-time bidirectional streaming for agents.

**WebSocket protocol [Doc, 2026-07-10]** at `/v1/tts/live`, MessagePack-serialized:
- Client → server events: `start` (config: format, chunk_length, reference_id, latency), `text` (append text as it's produced upstream, e.g. token-by-token from an LLM), `flush` (force immediate synthesis of buffered text — the key lever for low latency in interactive apps), `stop` (end of stream).
- Server → client events: `audio` (a chunk of bytes in the requested format — concatenate all chunks for the full clip), `finish` (session end, with a reason).

**Real-time heuristic [Heuristic]:** stream the LLM's tokens into `text` events and issue `flush` at sentence or clause boundaries. Waiting for a whole paragraph before the first `flush` defeats the point of streaming. Fish's own material describes sub-500 ms end-to-end and ~450 ms perceived first-audio when streaming instead of waiting for the full file. **[Claim]**

### Pricing and rate limits [Doc, 2026-07-10]

- **All TTS models: $15.00 per 1,000,000 UTF-8 bytes.** `s2.1-pro-free` is $0.
- Reference scale: ~1M UTF-8 bytes ≈ 180,000 English words ≈ ~12 hours of speech. **[Claim]**
- **Byte-based billing is the cost trap.** Billing is by UTF-8 *bytes*, not characters. ASCII/Latin text is ~1 byte/char, but Chinese/Japanese/Korean/Arabic/Hindi characters are typically **3–4 bytes each**. The same *word count* in Japanese costs several times more than in English. Estimate cost as `len(text.encode("utf-8")) / 1e6 * 15` USD, not from character count.
- ASR `transcribe-1`: $0.36 per audio hour. Voice design `voice-design-1`: $0.01 per successful request.
- **Concurrency tiers** (by cumulative prepaid spend): < $100 → 5 concurrent; ≥ $100 → 15; ≥ $1,000 → 50; enterprise → custom.
- Free tier (`s2.1-pro-free`) carries no TTFA or DPA guarantees. **[Doc]**

---

## Voice cloning

Two paths **[Doc, 2026-07-10]**:

1. **Persistent model** — `POST /model` with `type=tts`, `title`, `voices` (one or more reference audio files), `visibility` (`private`/`public`), optional `description`. Returns a voice `id`; pass it as `reference_id` in TTS. Models move through `created → trained`; a "fast" train mode returns a usable voice immediately. `enhance_audio_quality` (default on) denoises and normalizes the reference.
2. **Instant cloning** — skip model creation; send the reference audio + its transcript in the `references` field of a TTS call. Best for one-off voices.

**Reference-audio requirements [Doc + Heuristic]:**
- **Length:** ≥ 10 seconds minimum; 30–60 seconds (up to 1–2 minutes) generally yields noticeably better similarity and stability. **[Doc]**
- **Cleanliness:** mono, single speaker, no background music, no reverb, no overlapping voices. Clean input dominates clone quality more than length. **[Doc]**
- **Delivery:** natural conversational speech, not exaggerated performance; include varied phonemes and intonation so the clone generalizes. **[Doc]**
- **Formats:** `.wav`, `.mp3`, `.m4a`, `.opus`. **[Doc]**
- **[Heuristic]** If a clone sounds robotic or clips consonants, the reference — not the model — is usually the problem. Re-record a cleaner, longer sample before tuning generation parameters.

---

## Emotion, tone, and paralinguistic markers

Fish Audio's differentiator is inline expressive control. Markers are written into the text itself. **[Doc]**

**S1 (parentheses) [Doc, 2026-07-10]:** 40+ markers across three groups.
- Emotion: `(angry)`, `(sad)`, `(excited)`, `(surprised)`, `(sarcastic)`, `(joyful)`, `(empathetic)`, and more.
- Tone: `(in a hurry tone)`, `(shouting)`, `(screaming)`, `(whispering)`, `(soft tone)`.
- Special/paralinguistic: `(laughing)`, `(chuckling)`, `(sobbing)`, `(sighing)`, `(panting)`, `(crowd laughing)`.

**S2 family (square brackets) [Doc, 2026-07-10]:** a much larger open tag vocabulary (Fish cites 15,000+ tags) plus free-form natural-language descriptions. Documented examples include `[pause]`, `[short pause]`, `[emphasis]`, `[laughing]`, `[chuckle]`, `[sigh]`, `[inhale]`, `[exhale]`, `[whisper]`, `[shouting]`, `[screaming]`, `[loud]`, `[low volume]`, `[volume up]`, `[volume down]`, `[excited]`, `[angry]`, `[sad]`, `[surprised]`, `[singing]`, `[echo]`, `[with strong accent]`, `[clearing throat]`, `[audience laughter]`, and free-form forms like `[whisper in a small voice]`. **[Doc/Claim — the 15,000 figure is a first-party claim.]**

**Marker heuristics [Heuristic]:**
- One dominant emotion per sentence. Stacking `(angry)(sad)(excited)` in one clause produces incoherent delivery.
- Place a marker immediately before the span it should color; it influences what follows, not the whole paragraph retroactively.
- Special markers like `(laughing)` / `[laughing]` insert a *non-verbal* event — don't also spell out "haha" unless you want both.
- Free-form S2 tags are powerful but non-deterministic. If a specific effect must land every render, prefer a documented tag and lower `temperature`.
- Always confirm the marker syntax matches the `model` header (see the S1-vs-S2 warning above). This is the most common expressive-TTS failure with Fish.

---

## Text preparation for natural delivery [Heuristic unless noted]

- Enable `normalize` (**[Doc]**) so "$1,200", "Dr.", "3/4", and "2026" are expanded, or pre-expand them yourself for full control. Un-normalized numerics are a frequent source of wrong readings.
- Write punctuation for breath: commas and periods drive pacing more reliably than `[pause]` for ordinary prose. Reserve pause markers for deliberate dramatic beats.
- Break very long inputs into sentence/paragraph units and let `chunk_length` batch them; extremely long single chunks raise the odds of drift, repetition, or a runaway `(laughing)`.
- Spell tricky proper nouns/acronyms phonetically if the model mispronounces them (e.g., "N. A. S. A." vs "NASA"), or add a light accent/emphasis tag.
- For dialogue with multiple characters, use separate cloned voices / `reference_id`s per speaker rather than trying to shift one voice with markers alone.

---

## Open weights and self-hosting

Fish Audio publishes open weights under the **OpenAudio** brand (successor branding to **Fish-Speech**). This is a *separate track* from the hosted API. **[Doc, 2026-07-10]**

### What is actually open [Doc, 2026-07-10]
- **OpenAudio S1-mini** — 0.5B-parameter distilled model, publicly downloadable (Hugging Face `fishaudio/openaudio-s1-mini`). Released alongside S1 on **June 3, 2025**.
- **OpenAudio S1 (4B)** — the full flagship is described as proprietary/hosted; the openly published artifact is the **mini**, not the full 4B S1.
- **Fish-Speech 1.4 / 1.5** — earlier open releases (~0.5B class), still available.
- The GitHub project (`fishaudio/fish-speech`) also describes a larger **S2-Pro (4B)** open weight in its README. **[Doc]** Confirm exactly which weight file and license you are downloading before relying on it.

### Licensing — read carefully [Doc, 2026-07-10]
- **OpenAudio S1-mini weights: CC-BY-NC-SA-4.0** (per the Hugging Face model card). CC-BY-**NC**-SA means **non-commercial**, attribution, share-alike. **You cannot use these weights in a commercial product without a separate commercial license.**
- The **OpenAudio** GitHub *code* is Apache-2.0; its *weights* are CC-BY-NC-SA-4.0. **[Doc]**
- The **`fishaudio/fish-speech`** repository's README states code **and** weights under the **Fish Audio Research License** (with an explicit "we will act against violations" notice). **[Doc]**
- **[Heuristic / caution]** Third-party review sites sometimes claim these weights are "MIT-licensed." That contradicts the primary model card and repo license and is **unverified** — do not rely on it. When commercial use is on the table, treat the open weights as non-commercial and route commercial workloads through the paid hosted API (or negotiate a commercial license).

### Hardware [Doc + practitioner reports, 2026-07-10]
- **Inference minimum:** ~12 GB VRAM (documented self-hosting minimum). **[Doc]**
- **S1-mini specifically:** ~3.5 GB download, ~5 GB VRAM to run — fits comfortably on 8–12 GB consumer GPUs. **[Practitioner reports — labeled secondary]**
- **S2-Pro (4B):** substantially heavier; ~24 GB VRAM recommended for comfortable inference. **[Practitioner reports — labeled secondary]**
- Real-time factor scales with the GPU: e.g., ~100 ms TTFA and RTF ~0.195 on a single NVIDIA H200 in Fish's own S2 report **[Claim]**; consumer cards (RTX 3060/4090) are usable but slower. **[Secondary]**
- Stack: Linux or WSL; audio deps (`ffmpeg`, `libsox`, `portaudio`); install via conda or `uv`; vLLM / SGLang backends for throughput. **[Doc]**

### When self-hosting beats the API [Heuristic]
- **Self-host when:** you need data to stay on-prem; you run very high, steady volume where $15/M bytes exceeds amortized GPU cost; you need offline/air-gapped operation; or you are doing research/personal/non-commercial work where the CC-BY-NC-SA license is fine.
- **Use the hosted API when:** you need the full-quality flagship weights (not published openly); you need commercial rights without a bespoke license; you want managed scaling, streaming SLAs, and the newest S2.1 quality; or your volume is low/bursty enough that GPU idle time makes self-hosting more expensive than per-byte billing.

---

## Benchmark standing (disclosed methods, labeled)

Treat these as vendor and third-party claims with stated methods, **not** as neutral ground truth. All dated 2026-07-10 as read.

- **OpenAudio S1 — TTS-Arena-V2 (Hugging Face), human subjective ELO:** ranked **#1** as of **June 3, 2025**. **[Claim, first-party announcement; method = crowd human preference.]**
- **OpenAudio S1 — Seed-TTS-Eval (transcription-based WER/CER):** S1 WER 0.008 / CER 0.004; S1-mini WER 0.011 / CER 0.005 (English). **[Claim, first-party; method = ASR-scored intelligibility.]**
- **Artificial Analysis speech arena:** OpenAudio S1 ELO ≈ 1,074. **[Third-party, disclosed-arena method.]**
- **Fish Audio S2 technical report:** Seed-TTS-Eval WER 0.54% (Chinese) / 0.99% (English); **EmergentTTS-Eval** 81.88% win rate; Audio Turing Test posterior mean 0.515; RTF 0.195 and TTFA ~100 ms on H200. **[Claim, first-party technical report; EmergentTTS-Eval is a NeurIPS'25 benchmark using an audio-LLM judge across six prosodic/expressive scenarios.]**

**How to use benchmarks in production advice [Heuristic]:** low WER/CER means *intelligible*, not *expressive or preferred*. Arena ELO reflects listener preference on the arena's prompt mix, which may not match your domain (long-form audiobook vs. short agent turns). Always validate on your own scripts, voices, and languages before committing.

---

## Voice-clone consent and misuse safeguards [Doc, 2026-07-10]

Non-negotiable, and the agent should enforce these when a user asks to clone a voice:

- **Clone only voices you have the right to use:** your own voice, a voice whose owner has given explicit consent, or a properly licensed voice. Fish Audio's terms put this obligation on the user. **[Doc]**
- The user is responsible for having the **rights, consents, and disclosures** required, and for complying with local law on name, likeness, and AI-generated media. **[Doc]**
- Fish Audio does **not** pre-clear individual use cases and **may remove content or accounts** that violate its terms or applicable law, at its discretion and without notice. **[Doc]**
- Do **not** produce deceptive impersonation, non-consensual clones of real people (public figures included), fraudulent/scam audio, or content that hides its synthetic nature where disclosure is required.
- **[Heuristic]** If a user asks to clone a named celebrity or a private individual without evidence of consent/rights, decline the clone and offer a licensed stock voice or a synthetic non-matching voice instead. Recommend disclosing AI generation to end listeners.
- Cloned voice models can be deleted from the account; treat reference audio and clones as sensitive data (see privacy note).

---

## Failure modes and repair [Heuristic unless noted]

| Symptom | Likely cause | Fix |
|---|---|---|
| Markers read aloud literally ("open paren excited close paren") | Wrong marker syntax for the model | Match `(...)` to `s1`, `[...]` to S2 family |
| Robotic / low-similarity clone | Noisy, short, or multi-speaker reference | Re-record clean mono ≥30 s; keep `enhance_audio_quality` on |
| Repetition / looping / runaway laughter | Long chunk, high temperature, or stacked markers | Shorten chunks, raise `repetition_penalty`, lower `temperature`, one marker per span |
| Numbers/dates/acronyms misread | Normalization off | Set `normalize=true` or pre-expand text |
| Bill far higher than expected | Non-Latin script billed at 3–4 bytes/char | Estimate from `utf-8` byte length, not char count |
| High first-audio latency in an agent | Waiting for full text before synthesis | Use WebSocket, stream `text`, `flush` at clause boundaries, `format=pcm`, `latency=balanced` |
| Commercial/legal exposure from self-host | Used CC-BY-NC-SA weights commercially | Move to hosted API or obtain a commercial license |

**Production review checklist [Heuristic]:** intelligibility (no dropped/garbled words), correct pronunciation of names/numbers, appropriate and non-literal marker rendering, consistent voice identity across chunks, natural pacing/breaths, no repetition or clipping at chunk seams, target loudness, and — for clones — documented consent on file.

---

## Complete examples (illustrative, not mandatory formulas)

### Example A — Expressive narration with S2.1-Pro (REST, cost-aware)
**Intent:** a 2-sentence dramatic voiceover with a whispered aside, delivered as a WAV for editing; estimate cost first.
**Model:** `s2.1-pro` (square-bracket markers).

```bash
TEXT='The vault was empty. [whisper] Someone had been here first.'
# Cost estimate: bytes / 1e6 * $15
python -c "print(len(open('/dev/stdin').read().encode())/1e6*15)" <<< "$TEXT"

curl -s https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer $FISH_API_KEY" \
  -H "model: s2.1-pro" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The vault was empty. [whisper] Someone had been here first.",
    "reference_id": "<your-voice-id>",
    "format": "wav",
    "sample_rate": 44100,
    "normalize": true,
    "temperature": 0.7,
    "repetition_penalty": 1.2
  }' --output vault.wav
```

**Why structured this way:** brackets match the S2 model; the whisper marker precedes only the aside; `normalize` guards stray numerics; modest `temperature` with a repetition penalty keeps the dramatic line stable. **Likely failure:** if the voice were an `s1` clone you'd need `(whisper)` instead. **Variation:** switch to `s2.1-pro-free` for a zero-cost test render before spending on the paid model.

### Example B — Persistent voice clone, then reuse (Python SDK)
**Intent:** clone a consented narrator once, reuse across many lines.

```python
from fishaudio import FishAudio
client = FishAudio()

# 1) Create the model from a clean 45-second mono sample (consent on file).
voice = client.voices.create(
    title="Narrator - Priya (consented 2026-07-10)",
    voices=[open("priya_45s_clean.wav", "rb").read()],
    description="Studio sample, single speaker, no music",
    visibility="private",
)

# 2) Reuse by reference_id.
audio = client.tts.convert(
    text="Chapter one. (soft tone) It began on a grey morning.",
    reference_id=voice.id,   # this clone was trained on s1-style pipeline; use (..) markers
)
open("ch1.mp3", "wb").write(audio)
```

**Why:** the reference is long, clean, mono, and consented; the clone is private; markers match the model family. **Failure:** a public reference sample with background music degrades every downstream render. **Variation:** for a single throwaway line, use `references=[...]` instant cloning instead of creating a persistent model.

### Example C — Real-time voice agent (WebSocket)
**Intent:** speak an LLM's tokens as they arrive with minimal first-audio latency.

Pattern (pseudocode over `wss://api.fish.audio/v1/tts/live`, MessagePack):
```
send start   { format:"pcm", latency:"balanced", chunk_length:200, reference_id:"..." }
for token in llm_stream:
    send text { text: token }
    if token ends a clause:   send flush {}
send stop {}
# concatenate every server `audio` event's bytes until `finish`
```
**Why:** `pcm` avoids decode latency; `flush` at clause boundaries emits audio without waiting for the full reply; `balanced` shaves latency. **Failure:** flushing only at the end reintroduces the ~1 s+ full-file wait. **Variation:** raise `chunk_length` for smoother prosody on long, non-interactive narration where latency doesn't matter.

### Example D — Self-host decision
**Intent:** user has 40 hours/month of internal, non-commercial research narration and one RTX 4090.
**Decision:** OpenAudio **S1-mini** self-hosted is reasonable — fits the 4090, non-commercial use satisfies CC-BY-NC-SA, and steady volume amortizes the GPU. **[Heuristic]** But if that narration ships in a paid product, self-hosting the NC weights is a license violation → use the hosted API instead. Confirm the actual downloaded weight's license before deploying.

---

## Privacy note [Heuristic]

Reference audio for cloning is biometric-adjacent personal data. Keep clone models `private`, store consent records with the voice, avoid uploading third-party voices you cannot substantiate rights for, and delete clones and source audio when the project ends. Do not send user PII inside TTS text to a third-party API without the user's awareness.

---

## Primary sources (verified 2026-07-10)

- Fish Audio TTS API reference — https://docs.fish.audio/developer-guide/core-features/text-to-speech
- Fish Audio pricing & rate limits — https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits
- Fish Audio WebSocket TTS streaming — https://docs.fish.audio/api-reference/endpoint/websocket/tts-live
- Fish Audio voice cloning (SDK guide) — https://docs.fish.audio/developer-guide/sdk-guide/javascript/voice-cloning
- Fish Audio self-hosting / local setup — https://docs.fish.audio/developer-guide/self-hosting/local-setup
- Fish Audio terms of service — https://fish.audio/terms/
- OpenAudio S1 announcement — https://openaudio.com/blogs/s1
- OpenAudio S1-mini model card — https://huggingface.co/fishaudio/openaudio-s1-mini
- Fish-Speech / OpenAudio GitHub — https://github.com/fishaudio/fish-speech
- Fish-Speech docs (open weights) — https://speech.fish.audio/
- EmergentTTS-Eval (NeurIPS'25 benchmark, third-party method) — https://github.com/boson-ai/EmergentTTS-Eval-public
- Fish Audio S2 technical report (first-party) — https://arxiv.org/pdf/2603.08823
