---
name: resemble-chatterbox
description: Use Resemble AI Chatterbox for text-to-speech and voice-cloning workflows, including local open-weight Chatterbox, Chatterbox Multilingual, Chatterbox Turbo, and Resemble-hosted Chatterbox API routes. Apply when an agent must choose a Chatterbox variant, prepare reference-voice inputs, control emotion/paralinguistic delivery, plan multilingual TTS, handle PerTh watermarking, or make production decisions about consent, privacy, licensing, latency, and audio QA.
---

# Resemble Chatterbox

Use Chatterbox when the production needs expressive AI speech, zero-shot/reference-voice behavior, local or on-prem deployment, or Resemble-hosted TTS with Chatterbox-family voices. Do not use it as a generic "celebrity impersonation" tool. Treat every reference voice as biometric/personal data and require documented rights before generation.

Volatile facts in this skill were verified on 2026-07-10 from official Resemble AI, GitHub, Hugging Face, and Resemble documentation sources listed at the end.

## Choose the route first

Documented facts:

- Local/open route: Resemble publishes Chatterbox-family code and weights through the official `resemble-ai/chatterbox` GitHub repository and `ResembleAI/chatterbox` Hugging Face model card under MIT license. The local package installs with `pip install chatterbox-tts` and exposes Python classes such as `ChatterboxTTS` and `ChatterboxMultilingualTTS`.
- Hosted route: Resemble's synthesis API uses `https://f.cluster.resemble.ai/synthesize` for synchronous TTS and a streaming HTTP endpoint for chunked WAV. Requests authenticate with `Authorization: Bearer YOUR_API_KEY`.
- Hosted Chatterbox model versions documented by Resemble include Chatterbox, Chatterbox-Turbo, and Chatterbox Multilingual. Hosted Turbo is selected with the `model` value `chatterbox-turbo`; Resemble's model-version page also lists version codes `tts-v4` and `tts-v4-turbo`.

Production decision:

- Prefer local/open Chatterbox when the project requires on-prem control, no vendor audio upload, custom batching, offline evaluation, or permissive model modification.
- Prefer hosted Resemble when the project needs managed voices, streaming API delivery, low ops burden, team voice libraries, billing support, or production scale without managing GPU inference.
- Prefer Turbo for low-latency agents or dialog loops where its documented paralinguistic tag support matters.
- Prefer Multilingual V3 for cross-language voice cloning or localization; use Single Language Pack models when a priority language or regional dialect needs tighter pronunciation quality.
- Prefer original English Chatterbox when the job is English narration/character voice with emotion exaggeration and local creative control, and multilingual coverage is not required.

## Capability boundaries

Documented facts:

- Chatterbox is a family of open-source text-to-speech models by Resemble AI. The model card presents Chatterbox Multilingual V3 as a 500M-parameter general-purpose multilingual model, with Single Language Pack finetunes for selected languages and original Chatterbox for English creative controls.
- Official docs and model cards describe zero-shot/reference-voice synthesis. The open model card shows `audio_prompt_path` for conditioning on a different voice. Resemble marketing pages describe 5-second reference cloning for open Chatterbox/Turbo; hosted Resemble model-version docs list 10+ seconds as the dataset requirement for Chatterbox-family voice cloning.
- Chatterbox has emotion/intensity control through an `exaggeration` parameter in local examples. Resemble's hosted Chatterbox-Turbo docs describe native paralinguistic tags such as `[cough]`, `[laugh]`, and `[chuckle]`; the Turbo page also shows `[sigh]`, `[gasp]`, `[cough]`, `[laugh]`, `[whisper]`, and `[breath]`.
- Resemble's hosted synchronous endpoint accepts text or SSML, up to 3,000 characters, and can return `wav` or `mp3`; the hosted streaming HTTP endpoint accepts up to 2,000 characters and returns chunked WAV. The model-version page lists a 2,000-character limit for Chatterbox variants and notes some SSML tags are not supported, so treat the stricter endpoint/model limit as binding unless your current endpoint response proves otherwise.
- Public hosted docs say Chatterbox-Turbo is supported for Rapid English voices and Pre Built Library voices, and is not supported with Chatterbox Multilingual. Do not assume a custom multilingual voice can use `model: "chatterbox-turbo"` unless current account/API evidence proves support.
- Hosted API outputs include response metadata such as duration, synthesis duration, sample rate, and `issues`.
- Chatterbox outputs are described by Resemble as PerTh-watermarked by default. The open model card says generated audio includes PerTh watermarks that survive MP3 compression, audio editing, and common manipulations while maintaining nearly 100% detection accuracy; Resemble's PerTh materials describe imperceptible watermarking and later detection.

Boundaries and cautions:

- Do not promise perfect speaker identity, perfect accent transfer, or no hallucination. V3 is documented as reducing hallucinations, not eliminating them.
- Do not assume every official Resemble page has the same language list. The open GitHub/Hugging Face Chatterbox card lists 23 languages for general-purpose multilingual support; Resemble hosted/model pages have overlapping but not identical lists and newer marketing pages mention additional languages/Single Language Packs. Verify the target language against the exact model card or hosted model page at job time.
- Do not rely on PerTh watermarking as a substitute for consent, disclosure, or abuse review. Watermarking is provenance support, not permission.
- Do not remove or attempt to defeat PerTh. Resemble states that watermark removal is against intended use.
- Do not represent hosted API data as zero-retention unless the user has a Resemble contract or documentation explicitly covering that TTS route. Resemble's public privacy materials say personal data, including biometric/sensory data, is retained as needed to provide services; the Trust Center references retention and disposal controls based on customer requirements and contracts.

## Reference voice handling

Documented facts:

- Local examples use `audio_prompt_path` to specify a reference recording.
- Resemble's Chatterbox pages describe zero-shot cloning from short reference clips with no fine-tuning.
- Hosted Resemble voice creation and terms require the user to have necessary rights, consents, and permissions; Resemble may require consent from the individual whose voice is cloned.

Production requirements:

1. Confirm voice rights before using any reference clip: owner identity, allowed use, geography/platform, duration, revocation terms, and whether the output must be labeled synthetic.
2. Keep reference clips clean: one consenting speaker, dry speech, no music, no heavy noise reduction artifacts, no overlapping voices, and enough phonetic/prosodic variety for the target use.
3. Match reference language and target language when possible. If transferring across languages, expect accent leakage and run accent/pronunciation QA.
4. For public, political, medical, financial, or celebrity-like voices, require explicit written authorization and escalate any ambiguity.
5. Store reference clips and generated outputs in access-controlled project storage. Avoid sending local-only reference assets to hosted APIs unless the user approves the vendor route.

Production heuristics:

- For local zero-shot: start with 5-20 seconds of clean speech if the exact local model card supports short prompts; if similarity or stability is weak, test longer clean clips before changing models.
- For hosted voice creation: plan for the documented 10+ seconds minimum and follow the account's current voice-creation workflow.
- Normalize input audio before inference: mono, speech-focused, no clipping, moderate loudness, and trim long silences. Preserve natural breaths if they define the speaker; remove unrelated room noise.

## Prompting and delivery control

Documented facts:

- Local model-card tips say default settings around `exaggeration=0.5` and `cfg`/`cfg_weight=0.5` work for most prompts.
- Official tips say lowering `cfg` to about `0.3` can improve pacing for fast reference speakers; expressive/dramatic speech can use lower `cfg` and higher `exaggeration` such as around `0.7`.
- Official tips warn that higher `exaggeration` tends to speed up speech, and lowering `cfg` can compensate with more deliberate pacing.
- Turbo supports text paralinguistic tags in hosted docs and Resemble materials.
- Resemble accepts SSML, but hosted model docs list unsupported Chatterbox SSML tags including `<prosody>`, `<emotion>`, `<phonemes>`, `<substitutions>`, `<emphasis>`, and `<say-as>`.

Production heuristics:

- Write TTS text as performance copy, not prose. Short clauses, natural punctuation, and intentional paragraph breaks matter more than dense instructions.
- Use capitalization and punctuation only where they serve the delivery; Resemble's Chatterbox page shows capitalization affecting emphasis, but overusing caps can make speech sound unnatural.
- Treat bracketed paralinguistic tags as performance events, not decorations. Use them sparingly, usually at sentence boundaries.
- Segment long scripts into semantically complete chunks. Keep each chunk under the strictest relevant limit, then crossfade or room-tone-match in post.
- For multilingual localization, localize the script idiomatically before synthesis. Do not feed literal translations and expect the model to fix rhythm.

Suggested starting points:

- Neutral narration: `exaggeration=0.5`, `cfg_weight=0.5`; clean reference; standard punctuation.
- Dramatic character read: `exaggeration=0.65-0.85`, `cfg_weight=0.25-0.4`; shorter sentences; test pacing.
- Fast reference speaker: reduce `cfg_weight` toward `0.3`; add punctuation pauses before lowering speed in post.
- Cross-language clone: use Chatterbox Multilingual V3 or the relevant Single Language Pack; match `language_id`; QA accent and off-language phonemes.
- Agent/IVR Turbo: use hosted or local Turbo where available; keep utterances short; include only necessary tags such as `[chuckle]` or `[breath]`.

## Integration patterns

### Local/open Python pattern

Use when the project can install Python dependencies and run inference locally. Pin package and model revisions for production.

Example:

```python
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

device = "cuda"  # use "mps" or "cpu" only after performance testing
model = ChatterboxTTS.from_pretrained(device=device)

script = (
    "The first launch window opens at dawn. "
    "Keep your voice calm, precise, and just a little awed."
)

wav = model.generate(
    script,
    audio_prompt_path="approved_reference_voice.wav",
    exaggeration=0.55,
    cfg_weight=0.45,
)

ta.save("scene_01_narration.wav", wav, model.sr)
```

Why this works: it keeps reference-voice conditioning explicit, starts near documented defaults, and writes an uncompressed WAV suitable for editing and QA.

### Local multilingual pattern

Example:

```python
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

model = ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3")

wav = model.generate(
    "Bonjour, votre colis est pret pour le retrait.",
    language_id="fr",
    audio_prompt_path="approved_french_reference.wav",
    exaggeration=0.5,
    cfg_weight=0.5,
)

ta.save("pickup_fr.wav", wav, model.sr)
```

Why this works: it selects V3 explicitly, supplies the language ID, and avoids cross-language accent transfer unless intentionally tested.

### Hosted synchronous API pattern

Use when the user has a Resemble API key and a `voice_uuid`.

Example request:

```bash
curl -X POST "https://f.cluster.resemble.ai/synthesize" \
  -H "Authorization: Bearer $RESEMBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "voice_uuid": "YOUR_APPROVED_VOICE_UUID",
    "data": "Thanks for calling. I can help you check your appointment time.",
    "model": "chatterbox-turbo",
    "output_format": "wav",
    "precision": "PCM_16",
    "sample_rate": 48000,
    "use_hd": false
  }'
```

Why this works: it explicitly requests Turbo for lower latency/paralinguistic support and asks for edit-friendly WAV. Decode `audio_content` from base64, store duration/sample rate/`issues`, and retry only safe transient failures with backoff.

### Hosted streaming pattern

Use streaming for interactive voice agents where time-to-first-sound matters. Keep `data` short, expect chunked WAV, and preflight whether the selected voice supports Turbo. Fall back to synchronous only if latency is acceptable and the user approves any experience change.

## Production QA

Minimum review before delivery:

- Rights: reference voice, script content, and intended distribution are authorized.
- Model route: local/open vs hosted route is recorded with model variant, package/model revision or API model value, date, and settings.
- Text accuracy: no omitted words, hallucinated continuation, unexpected repetition, or off-script phrases.
- Voice quality: similarity is acceptable without impersonation risk beyond the approved use; no identity drift across chunks.
- Performance: pacing, emphasis, affect, breathing, and paralinguistic tags match the scene.
- Language: pronunciation, accent, names, numbers, and code-switching are correct for the audience.
- Audio engineering: no clipping, dropouts, long silences, robotic artifacts, room-tone mismatch, or discontinuities at chunk joins.
- Watermark/provenance: PerTh behavior is not disabled or stripped; provenance requirements are documented.
- Privacy/security: hosted inputs were approved for upload; local reference files are not leaked into logs or public artifacts.
- Accessibility and disclosure: where required by law, platform policy, or user brief, disclose that the voice is AI-generated.

## Failure modes and repairs

- Off-prompt continuation or repetition: shorten the chunk, tighten punctuation, reduce expressive settings, try V3 for multilingual, and regenerate with a clean seed/run record.
- Too fast: lower `cfg_weight`, add punctuation breaks, avoid excessive `exaggeration`, and test a calmer reference clip.
- Too flat: raise `exaggeration` in small increments, rewrite text with clearer emotional beats, and choose a reference with the desired energy.
- Accent leakage in cross-language cloning: use a same-language reference, set the exact language ID, test `cfg_weight` changes, or move to a Single Language Pack.
- Paralinguistic tag spoken literally: confirm Turbo/tag support for the runtime, adjust tag syntax, or remove the tag and edit in a separate SFX/breath asset.
- API truncation or bad request: split text below the endpoint/model limit, remove unsupported SSML, and inspect `issues` returned by the API.
- Watermark concern after post-processing: run PerTh detection where available; keep a pre-master WAV and an exported distribution file for comparison.

## Official sources verified on 2026-07-10

- [Resemble AI Chatterbox GitHub repository](https://github.com/resemble-ai/chatterbox)
- [ResembleAI/chatterbox Hugging Face model card](https://huggingface.co/ResembleAI/chatterbox)
- [Resemble Chatterbox model page](https://www.resemble.ai/learn/models/chatterbox)
- [Resemble Chatterbox Turbo model page](https://www.resemble.ai/learn/models/chatterbox-turbo)
- [Resemble Chatterbox Multilingual model page](https://www.resemble.ai/learn/models/chatterbox-multilingual)
- [Resemble synchronous TTS API reference](https://docs.resemble.ai/api-reference/text-to-speech/synthesize)
- [Resemble streaming TTS API reference](https://docs.resemble.ai/api-reference/text-to-speech/stream-synthesize)
- [Resemble authentication docs](https://docs.resemble.ai/getting-started/authentication)
- [Resemble rate-limit docs](https://docs.resemble.ai/getting-started/rate-limits)
- [Resemble model-version docs](https://docs.resemble.ai/getting-started/model-versions)
- [Resemble SSML reference](https://docs.resemble.ai/getting-started/ssml)
- [Resemble pricing page](https://www.resemble.ai/pricing)
- [Resemble Terms of Service](https://www.resemble.ai/terms-of-service)
- [Resemble Privacy Policy](https://www.resemble.ai/privacy-policy)
- [Resemble Trust Center](https://trust.resemble.ai/)
- [Resemble PerTh GitHub repository](https://github.com/resemble-ai/Perth)
- [Resemble PerTh model page](https://www.resemble.ai/learn/models/perth)
