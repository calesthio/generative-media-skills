---
name: qwen3-tts
description: Produce text-to-speech with Alibaba/Qwen Qwen3-TTS through DashScope/Model Studio or open-weight Qwen3-TTS checkpoints. Use when an agent must choose Qwen3-TTS models, voices, realtime versus non-realtime synthesis, voice cloning, voice design, instruction/prosody controls, multilingual or dialect speech, audio artifact handling, regional routing, pricing/privacy/licensing constraints, or production QA for narration, characters, assistants, audiobooks, ads, localization, or voice-enabled media.
---

# Qwen3-TTS production guidance

Use this skill to plan, invoke, review, and document Qwen3-TTS speech generation. Treat every model ID, price, region, quota, voice list, and limit below as volatile; the facts marked "verified 2026-07-10" were checked against official Alibaba/Qwen sources on that date.

## What Qwen3-TTS is, and which boundary matters

Documented facts:

- Qwen3-TTS is Alibaba/Qwen's multilingual text-to-speech model family for expressive, controllable, streaming-capable speech generation, with hosted DashScope/Model Studio routes and open-weight research/deployment checkpoints. Qwen's technical report describes 12Hz and 25Hz model variants, 0.6B and 1.7B sizes, voice cloning, voice design, multilingual generation, streaming, and Apache-2.0 model/tokenizer release intent. Source: https://arxiv.org/html/2601.15621v1 and https://github.com/QwenLM/Qwen3-TTS (verified 2026-07-10).
- Alibaba Cloud Model Studio exposes Qwen-TTS/Qwen3-TTS via HTTP/SSE non-real-time synthesis and WebSocket real-time synthesis. The non-real-time user guide says it is suited to latency-tolerant audiobook, e-learning, and content-production work, while real-time synthesis is designed for low-latency assistants, audiobook streaming, and customer service. Sources: https://help.aliyun.com/en/model-studio/non-realtime-tts-user-guide and https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide (verified 2026-07-10).
- Hosted Qwen3-TTS is not one universal endpoint. It has different model families for built-in voices, instruction control, voice design, voice cloning, and realtime variants. Verify the chosen region and model list immediately before production. Source: https://help.aliyun.com/en/model-studio/non-realtime-tts-user-guide (verified 2026-07-10).

Production heuristic:

- Use hosted DashScope when you need managed infrastructure, built-in voices, quick custom voice creation, or production traceability. Use open weights only when you have GPU capacity, need local/private inference, need to inspect or adapt model behavior, or cannot send script/audio data to a hosted provider.

## Model and route selection

Select the route by production need, not by the newest model name.

| Need | Prefer | Why |
|---|---|---|
| Short to medium content with built-in voices and simple delivery | `qwen3-tts-flash` through non-real-time HTTP/SSE | Character-billed hosted model, broad voice list, easy file URL handling. |
| Expressive direction such as "warm but urgent" or "radio-drama villain" | `qwen3-tts-instruct-flash` or realtime instruct model | Supports natural-language `instructions`; instruction text supports Chinese and English and has a 1,600-token limit in the API reference. |
| Brand/new character voice from a written description | Qwen-TTS Voice Design, then synthesize with `qwen3-tts-vd-*` | Voice Design creates custom voices from natural-language descriptions without an audio sample. |
| Consented clone of a speaker from a sample | Qwen-TTS Voice Cloning, then synthesize with `qwen3-tts-vc-*` | Voice Cloning creates custom voices from a 10- to 20-second sample according to Alibaba's user guide. |
| Conversational app that must start speaking while text is still arriving | Qwen3-TTS realtime WebSocket | Supports streaming input/output, server or client commit modes, incremental audio events, and low-latency playback. |
| Local/open deployment or research | `Qwen/Qwen3-TTS-*` open checkpoints | Apache-2.0 open-weight path; requires local inference engineering and QA. |

Documented model/region snapshot (verified 2026-07-10):

- Non-real-time Beijing and Singapore list includes `qwen3-tts-flash`, `qwen3-tts-flash-2025-11-27`, `qwen3-tts-flash-2025-09-18`, `qwen3-tts-instruct-flash`, `qwen3-tts-instruct-flash-2026-01-26`, `qwen3-tts-vd-2026-01-26`, and `qwen3-tts-vc-2026-01-22`. Stable aliases may map to a dated snapshot. Source: https://help.aliyun.com/en/model-studio/non-realtime-tts-user-guide.
- Real-time Qwen3-TTS SDK supports system voices for `Qwen3-TTS-Instruct-Flash-Realtime` and `Qwen3-TTS-Flash-Realtime`; custom cloned voices only for `Qwen3-TTS-VC-Realtime`; custom voice-design voices only for `Qwen3-TTS-VD-Realtime`. Source: https://help.aliyun.com/en/model-studio/qwen-tts-realtime-python-sdk.
- Region-specific API keys are not interchangeable. Model Studio docs list regional differences in endpoints/base URLs, supported models, features, and pricing. Source: https://www.alibabacloud.com/help/en/model-studio/what-is-model-studio.

## Invocation patterns and artifact custody

### Non-real-time HTTP/SSE

Use this for batches, narration segments, ads, localization lines, and renders where seconds of latency do not matter.

Documented facts:

- Non-real-time Qwen3-TTS uses the multimodal generation endpoint with model, input text, voice, and optional `language_type`; adding `X-DashScope-SSE: enable` enables streaming output. Source: https://help.aliyun.com/en/model-studio/qwen-tts-api.
- For the Qwen API reference, `text` is required, `voice` is required, `language_type` defaults to `Auto`, and supported specific language values include Chinese, English, German, Italian, Portuguese, Spanish, Japanese, Korean, French, and Russian. The same reference says specific language selection usually improves quality over `Auto` for single-language text. Source: https://help.aliyun.com/en/model-studio/qwen-tts-api.
- The API response includes `request_id` for troubleshooting. Complete audio is exposed through `output.audio.url`, which is valid for 24 hours; in streaming mode, the complete URL appears in the final chunk, while intermediate chunks contain Base64 audio data. Source: https://help.aliyun.com/en/model-studio/qwen-tts-api.
- Qwen3-TTS-Flash usage reports `characters`; older Qwen-TTS usage reports token fields. Source: https://help.aliyun.com/en/model-studio/qwen-tts-api.

Production requirements:

1. Split scripts into semantic units before the documented per-request text limit. The Qwen API reference says maximum input is 512 tokens for Qwen-TTS or 600 characters for other models; treat Qwen3-TTS-Flash as character-limited unless current docs say otherwise.
2. Download every returned audio URL immediately. Never leave a production asset referenced only by a 24-hour provider URL.
3. Save a manifest entry for each segment: model ID, region, endpoint, voice ID, language_type, instruction text if used, request_id, provider usage, local file path, source text hash, and generation timestamp.
4. For long narration, generate paragraph-sized segments with consistent room tone and post-process joins; do not depend on one enormous request.

Example: non-real-time built-in voice narration

```bash
curl -X POST "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-tts-flash",
    "input": {
      "text": "Today we will turn a dense product update into a story your sales team can remember.",
      "voice": "Cherry",
      "language_type": "English"
    }
  }'
```

Why this is structured this way: specify `language_type` because the line is single-language; use the workspace-specific Singapore endpoint when using a Singapore-region key; preserve `request_id` and download the returned URL immediately. If the line needs emotional or performance direction, switch to the instruct family instead of stuffing direction into the spoken text.

### Real-time WebSocket

Use this for assistants, interactive readers, live chat avatars, or applications that stream LLM text into speech.

Documented facts:

- The Qwen realtime Python SDK requires DashScope Python SDK 1.25.11 or later. Source: https://help.aliyun.com/en/model-studio/qwen-tts-realtime-python-sdk (verified 2026-07-10).
- Realtime request parameters include model, URL, voice, language_type, mode, output format, sample rate, speech rate, volume, pitch, bitrate for Opus, instructions, and instruction optimization. Supported realtime output formats include `pcm`, `wav`, `mp3`, and `opus`; supported sample rates are 8000, 16000, 24000, and 48000 Hz, while legacy Qwen-TTS-Realtime supports only PCM/24000 according to the SDK doc. Source: https://help.aliyun.com/en/model-studio/qwen-tts-realtime-python-sdk.
- Realtime modes include `server_commit`, where the server decides when to synthesize buffered text, and `commit`, where the client triggers synthesis manually. Source: https://help.aliyun.com/en/model-studio/qwen-tts-realtime-python-sdk.

Production heuristic:

- Choose `server_commit` for assistants that receive unpredictable text chunks because it protects sentence integrity. Choose `commit` only when your client can buffer complete phrases and you are optimizing for lowest latency.
- Default to PCM or WAV during QA and post-production. Use MP3 or Opus for delivery bandwidth only after checking pronunciation, edits, and loudness.

### Open-weight path

Documented facts:

- Qwen's GitHub repository describes open-source Qwen3-TTS models and tokenizers under Apache-2.0 and shows local usage for Base, CustomVoice, and VoiceDesign checkpoints such as `Qwen/Qwen3-TTS-12Hz-1.7B-Base`, `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`, and `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`. Source: https://github.com/QwenLM/Qwen3-TTS.
- The technical report states that Qwen3-TTS was trained on over 5 million hours of multilingual speech data and was evaluated across multilingual, cross-lingual, controllable, target-speaker, and long-speech tasks. Source: https://arxiv.org/html/2601.15621v1.

Production heuristic:

- For local deployment, define your own service contract: maximum text length, sample rate, file format, voice enrollment storage, logging, redaction, GPU memory envelope, concurrency, and moderation. The open model does not automatically inherit hosted DashScope retention, billing, quota, or audit behavior.

## Voices, multilingual speech, dialects, and pronunciation

Documented facts:

- The Qwen-TTS voice list includes built-in system voices such as Cherry, Serena, Ethan, Chelsie, Momo, Vivian, Moon, Maia, Kai, Nofish, Jennifer, Ryan, Katerina, and many others. Voice availability varies by model, and each voice row lists supported languages and model IDs. Source: https://help.aliyun.com/en/model-studio/qwen-tts-voice-list (verified 2026-07-10).
- Many Qwen3-TTS built-in voices list support for Chinese Mandarin, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, and Korean. Some voice-list entries are dialect-specific, including Cantonese voices. Source: https://help.aliyun.com/en/model-studio/qwen-tts-voice-list.
- For Qwen-TTS dialect handling, Alibaba's non-real-time guide says built-in voices can use dialect-supporting voices, but voice clone and voice design do not support dialects. Source: https://help.aliyun.com/en/model-studio/non-realtime-tts-user-guide.

Production requirements:

1. For single-language text, set `language_type` explicitly.
2. For mixed-language text, use `Auto`, but expect pronunciation misses. QA every proper noun, acronym, number, and code-switch boundary.
3. Do not promise dialect output from cloned or designed voices; use dialect-capable built-in voices only where the current voice list confirms support.
4. Maintain a pronunciation sheet. If Qwen3-TTS misreads a brand, name, URL, or abbreviation, rewrite text phonetically in the script or isolate that token in a retake.

## Instruction control, voice design, and voice cloning

### Instruction control

Documented facts:

- Qwen3-TTS instruction control uses the `instructions` parameter. For Qwen3-TTS-Instruct-Flash family, supported instruction languages are Chinese and English, and maximum instruction length is 1,600 tokens. Sources: https://help.aliyun.com/en/model-studio/non-realtime-tts-user-guide and https://help.aliyun.com/en/model-studio/qwen-tts-api.
- Alibaba's docs were inconsistent on 2026-07-10 about instruction scope: the non-real-time guide demonstrates `qwen3-tts-instruct-flash` with `instructions`, while the API reference scope line names the Qwen3-TTS-Instruct-Flash-Realtime series. Re-check the target route before committing a production workflow.
- Alibaba recommends concrete, multidimensional, objective, original, concise voice descriptions; it explicitly advises describing vocal qualities rather than imitating public figures because imitation is unsupported and may involve copyright risks. Source: https://help.aliyun.com/en/model-studio/non-realtime-tts-user-guide.

Production heuristic:

- Treat `instructions` as performance direction, not script content. Keep spoken text clean. Put delivery notes in `instructions` only: age, pace, pitch, emotion, timbre, use case, articulation, and intensity.
- Use `optimize_instructions: true` for high-stakes expressive work after a dry run; because it rewrites internal directives semantically, regression-test critical brand or character intent.

Example: expressive ad read with instruction control

```json
{
  "model": "qwen3-tts-instruct-flash",
  "input": {
    "text": "Your first invoice should feel like momentum, not paperwork.",
    "voice": "Ryan",
    "language_type": "English",
    "instructions": "Male young-adult commercial narrator. Confident, rhythmic, lightly amused. Medium-fast pace, crisp consonants, small smile in the voice. Build energy on 'momentum' and land 'not paperwork' with a dry, friendly contrast.",
    "optimize_instructions": true
  }
}
```

Expected result: a punchy, directed read without polluting the spoken line with bracketed stage directions. Failure modes: overacting, too much pitch movement, clipped consonants, or the model not honoring the contrast. Repair by reducing adjectives and specifying one or two observable delivery changes.

### Voice Design

Documented facts:

- Qwen-TTS Voice Design creates custom voices from text descriptions alone and supports real-time and non-real-time synthesis. Alibaba's Voice Design guide says Qwen-TTS has a 2,048-character voice description limit and is available in Beijing and Singapore. Source: https://help.aliyun.com/en/model-studio/voice-design-user-guide.
- The guide says the same description may produce slightly different voices each time; generate multiple voices, listen, and choose the best. It also says `voice_prompt` currently supports Chinese and English only, while the generated voice can synthesize speech in multiple languages. Source: https://help.aliyun.com/en/model-studio/voice-design-user-guide.
- Qwen-TTS custom voice quotas and cleanup: each Model Studio account has a separate limit of 1,000 Qwen-TTS custom voices; if a voice is not used in any speech synthesis request for one year, the system automatically deletes it. Source: https://help.aliyun.com/en/model-studio/voice-design-user-guide.

Production workflow:

1. Write a voice brief with age range, gender or neutrality, pitch, pace, emotion, timbre, accent if supported, articulation, and production use.
2. Create 3-5 candidates when budget allows. Voice Design is nondeterministic.
3. Audition each candidate against the actual script genre, not only the provider preview.
4. Save selected `voice_id`, creation request, preview audio, selection notes, and rights/approval record.
5. Delete unused custom voices after the project if the provider account is near quota or the voice should not persist.

Example: designed voice for a learning app

Voice prompt:

```text
Neutral young-adult educator, approximately 28 years old, clear mid pitch, moderate pace, precise articulation, warm but not childish, calm enthusiasm, low vocal fry, suitable for explaining math and science concepts to high-school students.
```

Preview text:

```text
Let's slow the problem down and look for the pattern hiding in the numbers.
```

Why this works: it gives observable vocal features and use context without asking for a named person. Audition it on definitions, equations, and encouragement lines; reject candidates that sound too theatrical, condescending, or breathy.

### Voice Cloning

Documented facts:

- Alibaba's Qwen Voice Cloning guide says Voice Cloning creates a custom voice from a 10- to 20-second audio sample without model training; Qwen-TTS cloning supports both real-time and non-real-time synthesis and is available in China (Beijing) and Singapore. Source: https://help.aliyun.com/en/model-studio/voice-cloning-user-guide.
- The Voice Cloning workflow is: prepare audio, create voice with the Voice Cloning API and a `target_model`, then synthesize speech with the returned voice ID. Source: https://help.aliyun.com/en/model-studio/voice-cloning-user-guide.

Production requirements:

- Clone only with documented consent and rights to the sample and resulting synthetic voice. Keep the consent record with the production manifest.
- Do not clone a public figure, client executive, employee, actor, child, or private person unless the project has explicit written authorization for that exact use, duration, territory, and distribution channel.
- Use clean, dry, close-mic source audio; avoid music beds, room echo, multiple speakers, compression artifacts, or emotional extremes unless those are the desired identity.
- Do not use cloning as a pronunciation workaround. If identity is not required, prefer built-in voices or Voice Design.

## Pricing, quota, privacy, and compliance

Documented facts verified 2026-07-10:

- Alibaba's pricing page states Qwen3-TTS non-real-time and realtime are billed by input text characters and output is not charged. It lists `qwen3-tts-flash` at 0.733924 CNY per 10,000 characters for international deployment, `qwen3-tts-instruct-flash` at 0.8 CNY per 10,000 characters for international deployment, and realtime Qwen3-TTS Flash/Instruct/VD/VC variants around 0.954101 to 1 CNY per 10,000 characters depending on service deployment scope and model section. Source: https://help.aliyun.com/zh/model-studio/model-pricing.
- The same pricing page lists `qwen-voice-enrollment` at 0.01 CNY per custom voice and `qwen-voice-design` at 0.2 CNY per custom voice, with China-mainland free quotas in some sections and no free quota for other deployment scopes. Source: https://help.aliyun.com/zh/model-studio/model-pricing.
- Alibaba Cloud Model Studio privacy documentation says Model Studio will not use customer data for model training and that data transmitted during application building and model training is encrypted with AES-256; it also says Model Studio has SOC 2 compliance with an unqualified opinion. Source: https://www.alibabacloud.com/help/en/model-studio/privacy-notice.
- Alibaba Cloud's general privacy policy describes personal-data transfer, retention, security, deletion, and rights terms; it says retention depends on purpose, legal requirements, and ongoing business need. Source: https://www.alibabacloud.com/help/en/legal/latest/alibaba-cloud-international-website-privacy-policy.

Production requirements:

1. Re-check pricing and free quota before each paid batch. Do not treat the prices above as permanent.
2. Keep API keys in environment variables. Do not paste keys into scripts, logs, notebooks, prompts, or generated manifests.
3. Treat input scripts, reference voice samples, cloned voice IDs, preview audio, and generated voice assets as sensitive production data.
4. If a project involves health, children, legal, financial, employee, celebrity, or biometric voice identity data, escalate for legal/privacy review before synthesis.
5. Record whether hosted or local inference was used. Hosted Model Studio privacy assurances do not automatically cover local deployments, third-party gateways, or downloaded open weights.

## QA checklist before delivery

Run these checks on every final or client-review audio asset:

- Text fidelity: no omitted words, hallucinated words, repeated phrases, wrong numbers, wrong units, or subtitle mismatch.
- Pronunciation: names, brands, acronyms, URLs, multilingual words, dialect claims, and code-switching.
- Performance: pace, emotion, authority, friendliness, age impression, genre fit, and instruction adherence.
- Voice identity: built-in voice or custom `voice_id` matches the approved decision; no accidental model/region fallback.
- Technical audio: clicks, clipping, silence, truncation, obvious compression artifacts, mismatched sample rate, channel count, loudness, head/tail padding, and segment seam clicks.
- Rights/privacy: consent file for clones, acceptable source text, no public-figure imitation, no unapproved minor voice, and no leaked provider URL.
- Custody: local immutable file exists; manifest has model, voice, region, request_id/session_id, text hash, usage, and generation time.

For long-form productions, audition in context with music and visuals. Qwen3-TTS can sound excellent in isolation while failing timing, lip-sync, or emotional continuity once cut into a video.

## Troubleshooting

- Robotic or flat read: switch to instruct model, reduce vague adjectives, specify concrete pace/pitch/articulation, and retake shorter clauses.
- Overacted read: remove stacked emotion words, lower intensity, choose a calmer built-in voice, or disable instruction optimization for a retake.
- Mispronounced proper noun: set exact `language_type`, rewrite phonetically, isolate line, and document the spelling used.
- Mixed-language errors: use `Auto` only when needed, split by language where natural, or generate separate segments with explicit language settings.
- Custom voice does not match brief: generate multiple Voice Design candidates; it is documented as nondeterministic.
- Cloned voice unstable: use cleaner source audio, verify consent/sample identity, create a new voice, and test against several representative lines before batch synthesis.
- Realtime cuts off phrases: use `server_commit` or buffer complete clauses before `commit`.
- Missing full audio file: for SSE, wait for the final chunk; the complete URL is returned only at the end.
- Expired URL: regenerate or use the previously downloaded local copy; the provider URL is documented as 24-hour only.

## Source trail

Official and primary sources used for this skill, all verified on 2026-07-10:

- Alibaba Cloud Model Studio, Non-real-time speech synthesis: https://help.aliyun.com/en/model-studio/non-realtime-tts-user-guide
- Alibaba Cloud Model Studio, Qwen-TTS API reference: https://help.aliyun.com/en/model-studio/qwen-tts-api
- Alibaba Cloud Model Studio, realtime Qwen TTS Python SDK: https://help.aliyun.com/en/model-studio/qwen-tts-realtime-python-sdk
- Alibaba Cloud Model Studio, Qwen-TTS voice list: https://help.aliyun.com/en/model-studio/qwen-tts-voice-list
- Alibaba Cloud Model Studio, Voice Design: https://help.aliyun.com/en/model-studio/voice-design-user-guide
- Alibaba Cloud Model Studio, Voice Cloning: https://help.aliyun.com/en/model-studio/voice-cloning-user-guide
- Alibaba Cloud Model Studio, pricing: https://help.aliyun.com/zh/model-studio/model-pricing
- Alibaba Cloud Model Studio, security certifications and privacy: https://www.alibabacloud.com/help/en/model-studio/privacy-notice
- Alibaba Cloud International Website Privacy Policy: https://www.alibabacloud.com/help/en/legal/latest/alibaba-cloud-international-website-privacy-policy
- Qwen3-TTS GitHub repository: https://github.com/QwenLM/Qwen3-TTS
- Qwen3-TTS Technical Report: https://arxiv.org/html/2601.15621v1
