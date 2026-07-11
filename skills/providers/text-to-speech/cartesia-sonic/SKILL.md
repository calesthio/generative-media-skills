---
name: cartesia-sonic
description: "Use Cartesia Sonic and related Cartesia voice APIs for production speech: text-to-speech, realtime WebSocket TTS, voice selection, instant and professional voice cloning, pronunciation/language/emotion controls, voice localization, voice changer, pricing/concurrency planning, privacy/security review, and QA for narration, ads, localization, dubbing, avatars, and interactive voice agents."
---

# Cartesia Sonic production skill

Use this skill when a media-production agent is choosing, prompting, integrating, or reviewing Cartesia Sonic for speech output. Treat Sonic as a low-latency text-to-speech provider first; use adjacent Cartesia voice APIs only when the production need explicitly requires them.

All volatile facts below were checked against official Cartesia documentation or legal pages on 2026-07-10. Re-check before committing budgets, compliance claims, model IDs, pricing, concurrency, supported languages, or API behavior.

## Provider boundary

Documented facts:

- Sonic is Cartesia's text-to-speech model family. The current production default is `sonic-3.5`; API references also list `sonic-3` and `sonic-latest`.
- Sonic takes text and returns generated speech. It is suitable for realtime voice agents, narration, dubbing, avatars, notifications, ads, and localization when the workflow starts from a transcript.
- Cartesia also documents Ink speech-to-text, Line hosted voice agents, voice cloning, voice localization, infill, and voice changer. Do not present all of these as "Sonic TTS"; name the exact Cartesia surface being used.
- Voice changer is not TTS: it takes an input speech clip and returns speech with the same intonation in a different target voice.
- Speech-to-speech or voice conversion claims should be limited to the documented `voice-changer` endpoints unless Cartesia's docs explicitly add another supported path.

Production heuristics:

- Prefer Cartesia Sonic when low time-to-first-byte, conversational pacing, multilingual speech, and API streaming matter more than offline local rendering or maximal post-production editability.
- Prefer non-realtime batch TTS providers or local TTS when the project requires air-gapped processing, predictable no-network rendering, or a license/security posture not satisfied by Cartesia's current account settings.
- For a media pipeline, record the selected endpoint, model ID, voice ID, language, output format, Cartesia-Version, generation_config, pronunciation dictionary ID, and source transcript checksum in the asset manifest.

## Capability map

### Sonic text-to-speech

Documented facts:

- `sonic-3.5` is documented as Cartesia's fastest and most natural TTS model, with sub-90 ms latency and native support for 42 languages.
- The model is documented as following transcripts faithfully, handling alphanumerics such as order numbers and IDs naturally, and using context-aware English pronunciation for heteronyms.
- Sonic 3.5 is documented as generally available and production-ready in the 2026 changelog. Older Sonic models and several snapshots/languages were sunsetted on 2026-06-01.

Production heuristics:

- For new production, start with `sonic-3.5`, not old `sonic`, `sonic-english`, `sonic-multilingual`, `sonic-2`, or `sonic-turbo` identifiers.
- Use `sonic-3` only for regression compatibility or if a specific voice/control path has been validated there.
- Avoid pinning to `sonic-latest` in a locked edit/render pipeline unless the project explicitly wants automatic model changes. Use `sonic-3.5` for the latest stable snapshot, and use a dated `sonic-3.5-YYYY-MM-DD` snapshot when exact repeatability matters.

### Voices

Documented facts:

- Cartesia offers 500+ out-of-box voices and custom voices.
- Voices can be selected by ID for TTS requests.
- Cartesia's voice guidance distinguishes stable voices for production voice agents from more emotive voices for AI characters.
- Instant Voice Clone is available in the playground and API; it uses an uploaded or recorded clip up to 10 seconds. Training instant clones is documented as fast and free.
- Professional Voice Clone (PVC) is available on Startup tier or higher. It uses fine-tuning on larger voice data; Cartesia documents a 30-minute minimum and recommends 2 hours for a better quality/effort balance.
- PVC training is documented as taking about 3 hours; status values include Draft/Failed/Training/Completed in the playground and API fine-tune states include `created`, `training`, `completed`, and `failed`.
- PVCs are pinned to the base model used for the fine-tune. A future base model requires retraining, with another fine-tune cost.
- Professional Voice Clones are now available on Sonic 3.5 according to the 2026 changelog.

Production heuristics:

- For narration or ads with no rights-approved talent voice, audition several stock voices before cloning. Cloning adds rights, custody, and retention obligations.
- For interactive agents, test stable/realistic voices before highly emotive voices. A voice that sounds dramatic in a 10-second demo can be tiring or less intelligible in long calls.
- For character, game, or companion work, audition emotive voices and emotion controls against the actual script; some voices respond better to emotion direction than others.
- For brand voice clones, treat the voice ID like a licensed talent asset: store consent, allowed use, territory, term, revocation rules, and disclosure requirements alongside the project.

### Voice localization

Documented facts:

- Cartesia documents voice localization: making a voice sound native in new languages and accents.
- Pricing documentation lists localizing a voice as a one-time 225-credit cost.

Production heuristics:

- Use localization when the same approved speaker identity must carry across languages.
- Do not assume localization solves translation, cultural adaptation, script timing, lip-sync, or legal talent consent. Handle those as separate production tasks.
- QA localized voices with native reviewers for pronunciation, accent acceptability, intelligibility, and brand fit.

### Voice changer

Documented facts:

- The `voice-changer/bytes` and `voice-changer/sse` endpoints take a speech audio file and return speech with the same intonation but a different voice.
- Supported input audio formats include common containers such as FLAC, MP3/MPEG/MPGA, OGA/OGG, WAV, and WEBM.
- Output containers include `raw`, `wav`, and `mp3`; sample rates include 8000, 16000, 22050, 24000, 44100, and 48000 Hz.
- Voice changer is priced at 15 credits per second of input audio.

Production heuristics:

- Use voice changer for voice conversion of already-performed speech when preserving timing, intonation, and performance matters more than reconstructing from text.
- Use TTS from transcript when you need exact word control, pronunciation dictionaries, clean pickups, or translated/localized copy.
- For dubbing, decide explicitly between TTS from translated script, voice changer from a guide performance, and a hybrid. Do not silently replace one with another.

## Endpoint selection

Documented facts:

- `POST /tts/bytes`: best when the full transcript is known and the production needs streamed audio bytes in a single HTTP request. It is efficient for batch jobs, cached files, notifications, narration segments, and file export.
- `POST /tts/sse`: best when the full transcript is known and timestamps are needed without WebSocket, or the stack already consumes Server-Sent Events. Audio chunks are JSON/base64 SSE events.
- `WSS /tts/websocket`: best for long-lived sessions, text arriving incrementally from an LLM, lowest latency across many turns, timestamps, and multiple utterances on one socket.
- Bytes and SSE take one complete transcript per request. SSE `context_id` is echoed for logs but does not merge multiple HTTP requests into one utterance.
- WebSocket supports contexts and continuations. Reuse one `context_id` for one utterance, send partials with `continue: true`, and finalize with `continue: false`.
- Contexts expire automatically 1 second after the last audio output is streamed. Sending another input on an expired context is unsupported.

Decision rule:

- Use `bytes` for produced files: narration, ads, explainer voiceover, in-app notifications, batch localization, cacheable prompts.
- Use `sse` for produced files that need word/phoneme timing but cannot use WebSocket.
- Use `websocket` for live agents, LLM token streaming, barge-in/interruptible experiences, or any case where the full transcript is not available at once.

Failure modes:

- Sending LLM fragments as separate HTTP requests creates prosody seams. Use WebSocket continuations for one spoken utterance.
- Splitting a context without spaces or punctuation concatenates text verbatim and can mispronounce joined chunks.
- Changing model, voice, language, output format, or generation settings within one WebSocket context violates the documented input-format rule that only `transcript`, `continue`, and `duration` may vary on a context.
- Leaving idle WebSockets open can hit WebSocket limits and cause 429 errors.

## Core request fields

Documented facts:

- TTS requests require `model_id`, `transcript`, `voice`, and `output_format`.
- The language field tells the selected voice which language to speak. The exact availability can depend on the model.
- TTS supports word timestamps and phoneme timestamps on SSE; WebSocket also supports timestamp use cases. Bytes is audio-only.
- Pronunciation dictionaries are supported by `sonic-3` models and newer through `pronunciation_dict_id`.
- `generation_config` is available on `sonic-3` and `sonic-3.5`.
- The older top-level `speed` enum is deprecated; use `generation_config.speed` instead.
- API requests should include `Cartesia-Version` as the date when the integration was tested. For WebSockets, `cartesia_version` can be passed as a query parameter.

Production defaults:

```json
{
  "model_id": "sonic-3.5",
  "voice": { "mode": "id", "id": "VOICE_ID_APPROVED_FOR_THIS_PROJECT" },
  "language": "en",
  "output_format": {
    "container": "wav",
    "encoding": "pcm_s16le",
    "sample_rate": 48000
  },
  "generation_config": {
    "speed": 1.0,
    "volume": 1.0
  }
}
```

Heuristics:

- Use WAV/48 kHz for video-production masters unless the target pipeline needs another sample rate.
- Use MP3 only for delivery previews or app assets where smaller files matter more than editing headroom.
- Use raw PCM only when a realtime player, telephony system, or streaming stack requires it and the downstream encoding/sample-rate expectations are explicit.
- For telephony, match the downstream codec/sample rate rather than generating high-rate audio and transcoding repeatedly.

## Transcript writing for Sonic

Documented facts:

- Sonic 3.5 is designed to work with natural, well-punctuated transcript text with minimal prompt engineering.
- Cartesia recommends complete phrases and terminal punctuation.
- Sonic handles conventional written forms for numbers, currency, dates, phone numbers, addresses, email addresses, common acronyms, and initialisms.
- Heavy preprocessing, punctuation stripping, or forced casing can hurt output quality.
- All-caps may be interpreted as an initialism; use normal casing except when a token should be read letter-by-letter.
- `<spell>...</spell>` is recommended for alphanumeric codes and exact character-by-character readout.
- Break tags can insert fixed pauses, but repeated or chained break tags can reduce naturalness and cause failures.

Production heuristics:

- Treat the transcript as a performance script, not a prompt. Write what should be spoken, not notes to the model.
- Avoid markdown, bullets, headers, emoji, raw JSON, asterisks, and hashtags in spoken transcripts unless the symbol is meant to be read aloud.
- Keep timing notes outside the transcript unless they are valid SSML/Sonic tags that the integration preserves.
- For ads and social videos, write short sentences with intentional punctuation; do not rely on speed controls to fix an overlong script.
- For voice agents, constrain upstream LLM output to plain prose, terminal punctuation, no markdown, no unsupported symbols, and explicit `<spell>` tags for codes.

## Pronunciation, language, and accent control

Documented facts:

- Pronunciation dictionaries are search-and-replace rules that direct Sonic to use another string for matching words or phrases.
- Dictionary pronunciations can be IPA-like Cartesia syntax or "sounds-like" guidance.
- Once a dictionary is created, pass its ID as `pronunciation_dict_id` in TTS APIs.
- Sonic 3.5 supports 42 languages. API docs list language codes including `en`, `fr`, `de`, `es`, `pt`, `zh`, `ja`, `hi`, `it`, `ko`, `nl`, `pl`, `ru`, `sv`, `tr`, `tl`, `bg`, `ro`, `ar`, `cs`, `el`, `fi`, `hr`, `ms`, `sk`, `da`, `ta`, `uk`, `hu`, `no`, `vi`, `bn`, `th`, `he`, `ka`, `id`, `te`, `gu`, `kn`, `ml`, `mr`, and `pa`.

Production heuristics:

- Use dictionaries for brand names, product names, medical/legal terms, domain jargon, regional place names, and heteronyms that matter.
- Keep a per-project pronunciation sheet and convert only the tested entries into a Cartesia pronunciation dictionary.
- Do not pack every possible word into a dictionary. Over-specific replacements can create unnatural delivery or interact badly with context.
- For multilingual output, pick a voice whose primary language or localized target matches the language. Do not assume one English voice will be equally native in all languages without localization and QA.

## Speed, volume, emotion, and nonverbal performance

Documented facts:

- Sonic supports speed, volume, and emotion controls via the playground, `generation_config`, or SSML tags.
- `generation_config.speed` ranges from 0.6 to 1.5.
- `generation_config.volume` ranges from 0.5 to 2.0.
- Emotion controls are marked beta. Cartesia describes them as guidance rather than strict controls.
- Emotion direction works best when the emotion is consistent with the transcript.
- Sonic can respond to nonverbalisms and expressive text depending on the voice and content, but production reliability should be tested.

Production heuristics:

- Use punctuation, script wording, and voice choice first; use speed/volume/emotion as refinements.
- Test emotion control voice-by-voice. Record accepted values and rejected takes; do not assume the same emotion word works the same across voices.
- Avoid using volume controls as a substitute for mixing. Normalize and mix in post for video deliverables.
- For ads, make separate takes for "warm", "confident", "urgent", and "smiling" reads; choose by listening rather than relying on the label.
- For compliance or customer-support voice agents, avoid exaggerated emotion and keep prosody stable.

## Pricing, quotas, and throughput planning

Documented facts:

- Cartesia meters model usage in credits. Errors do not consume credits.
- Standard TTS costs approximately 1 credit per character, with slight variance due to transcript preprocessing.
- TTS with a Pro Voice Clone costs approximately 1.5 credits per character; Instant Voice Clones are billed at the standard TTS rate.
- Pro Voice Clone fine-tuning costs 1,000,000 credits on successful training.
- Voice changer costs 15 credits per second of input audio.
- Plan concurrency limits for TTS are documented as Free 2, Pro 3, Startup 5, Scale 15, Enterprise custom.
- WebSocket connections are limited to 10x the TTS concurrency limit.
- TTS concurrency is measured by unique active contexts. For HTTP, each request is one context; for WebSocket, each unique `context_id` is one context.
- Exceeding the TTS concurrency limit or WebSocket limit returns a 429 error.
- Idle TTS WebSockets close after 5 minutes.

Cost heuristic:

- Estimate credits before generation from the final transcript character count.
- For long narration, split by scene/paragraph for editability, but batch work through a queue respecting concurrency.
- For WebSocket agents, pool connections and close idle sockets. Count active utterance contexts, not just open sockets.
- For PVC work, get explicit user approval before starting a fine-tune because successful training has a large fixed credit cost.

## Privacy, security, rights, and disclosure

Documented facts:

- Server-side integrations should use API keys from trusted environments. Browser or mobile clients should use short-lived access tokens, not embedded API keys.
- Management endpoints such as usage and API-key metadata require admin API keys.
- Zero Data Retention (ZDR) is available to Enterprise customers for TTS and STT inference.
- With ZDR, TTS text input and TTS audio output are documented as not retained, while operational metadata such as request IDs, usage totals, account information, and service health data may be retained.
- ZDR does not apply to voice cloning, PVC, voice creation, or workflows where customer-provided source material must be retained or processed differently.
- Cartesia's acceptable use policy prohibits impersonating another person or business and says users may submit only their own voice/audio recordings or those of others with explicit consent and necessary rights.

Production requirements:

- Do not clone, localize, or voice-change a person, celebrity, employee, customer, or brand voice without documented consent and rights.
- Do not imply that ZDR covers cloning datasets or voice-creation source material.
- Keep API keys out of client apps, generated videos, logs, screenshots, and project artifacts.
- For synthetic or cloned voices in public-facing media, follow the project's disclosure policy and applicable law. At minimum, flag the asset as AI-generated or cloned in the production ledger when the voice identity could affect audience trust.
- For regulated or sensitive content, verify Enterprise/ZDR, DPA/BAA/compliance requirements, region/deployment needs, and retention expectations with the account owner before sending real content.

## Artifact custody

For every generated or transformed audio asset, store:

- transcript text or transcript checksum;
- model ID and Cartesia-Version;
- endpoint (`tts/bytes`, `tts/sse`, `tts/websocket`, `voice-changer/bytes`, etc.);
- voice ID, voice source class (stock, instant clone, PVC, localized), and rights/consent reference;
- language code and pronunciation dictionary ID/version;
- generation_config and SSML/tags used;
- output format container, encoding, sample rate, bit rate;
- usage estimate and actual credits if available;
- request ID or context ID where safe to retain;
- human QA status and notes;
- disclosure label if synthetic/cloned voice disclosure is required.

Do not store raw voice-clone source recordings in a project folder unless the production contract explicitly allows it. Prefer a controlled asset store with access logs and deletion policy.

## Production QA

Listen to every approved take; waveform inspection is not enough.

Check:

- transcript fidelity: no missing, inserted, repeated, or hallucinated words;
- pronunciation: names, acronyms, numbers, codes, product terms, addresses, money, dates;
- language/accent: native reviewer pass for localized output;
- performance: pace, pauses, emotion, emphasis, fatigue over long runs;
- technical quality: clicks, distortion, clipping, noise, unnatural silence, sample-rate mismatch;
- editability: handles at cut points, consistent loudness, scene-level separation;
- sync: word/phoneme timestamps align with captions, avatar/lip-sync, or UI events;
- rights: voice source and usage consent match final deliverable;
- safety/disclosure: cloned or synthetic voice labels and policy requirements are satisfied.

Common repair actions:

- Mispronunciation: add or revise pronunciation dictionary; rewrite the phrase naturally; test a shorter line with context preserved.
- Rushed read: shorten the script first; then test `generation_config.speed` below 1.0.
- Flat read: try a more expressive voice; add emotion guidance consistent with the text; revise punctuation and wording.
- Overacted read: remove emotion tags, choose a stable voice, and simplify punctuation.
- Prosody seam in live output: switch to WebSocket continuations with one context per utterance.
- Timestamps missing: use SSE or WebSocket and request timestamps; do not use bytes for timestamp-dependent workflows.
- Concurrency errors: queue requests, reduce parallel contexts, close idle WebSockets, or upgrade plan.

## Complete examples

### Example: batch narration for a 90-second product explainer

Production intent: create edit-ready scene narration files for a product video.

Workflow:

1. Finalize script by scene. Keep each line as a complete sentence with terminal punctuation.
2. Audition 3 stock voices in the target language with the first 2 scenes.
3. Choose `POST /tts/bytes` because the transcript is complete and the output will be edited as files.
4. Generate one WAV per scene at 48 kHz.
5. Store model, voice, language, output format, transcript checksum, and request ID in the asset manifest.
6. QA every line against the final script.

Example request body:

```json
{
  "model_id": "sonic-3.5",
  "transcript": "Meet Acme Lens, the field camera that tags every inspection before your team leaves the site.",
  "voice": { "mode": "id", "id": "APPROVED_STOCK_VOICE_ID" },
  "language": "en",
  "output_format": {
    "container": "wav",
    "encoding": "pcm_s16le",
    "sample_rate": 48000
  },
  "generation_config": {
    "speed": 0.96,
    "volume": 1.0,
    "emotion": "confident"
  }
}
```

Expected result: one clean narration file with natural product-announcement pacing and no markdown or spoken production notes.

Failure modes:

- The line is too long for the shot: shorten copy rather than forcing high speed.
- Brand name is wrong: add pronunciation dictionary and regenerate only affected lines.
- Emotion sounds exaggerated: remove emotion setting and rely on voice choice/punctuation.

Variations:

- Use MP3 for lightweight app previews.
- Use SSE if the same line must drive word-level kinetic captions.
- Use a PVC only after rights approval and cost approval.

### Example: realtime LLM voice agent

Production intent: speak assistant responses as the LLM streams tokens.

Workflow:

1. Configure the LLM to output plain speakable prose with no markdown, no bullets, no emoji, and terminal punctuation.
2. Open one Cartesia WebSocket per worker/session pool.
3. For each assistant turn, create one `context_id`.
4. Send chunks with `continue: true`; finalize the turn with `continue: false`.
5. Keep voice/model/language/output settings identical within the context.
6. Close idle sockets or recycle after idle periods.

Example chunk sequence:

```json
{
  "model_id": "sonic-3.5",
  "transcript": "I found three available appointment times: ",
  "voice": { "mode": "id", "id": "APPROVED_AGENT_VOICE_ID" },
  "language": "en",
  "context_id": "turn-8472",
  "continue": true,
  "output_format": {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 44100
  }
}
```

```json
{
  "transcript": "Monday at 9:30 AM, Tuesday at 2:00 PM, or Thursday at 11:15 AM.",
  "context_id": "turn-8472",
  "continue": false
}
```

Expected result: one seamless utterance with stable prosody across the two chunks.

Failure modes:

- Missing space after the first chunk produces joined words.
- Reusing the same context after it expires is unsupported.
- Opening too many idle sockets triggers 429 errors.

Variations:

- Use `<spell>` tags for confirmation codes.
- Use a telephony sample rate/encoding if the audio is streamed directly into a phone call.
- Use access tokens for browser clients; never expose the API key.

### Example: localization with brand voice

Production intent: localize an English product ad into Spanish and Japanese using the same approved speaker identity.

Workflow:

1. Confirm the talent agreement covers cloned/localized voice use in Spanish and Japanese, paid media, regions, and campaign term.
2. Localize or select voices for each target language. Do not assume the English voice is native in each language.
3. Translate/adapt the script for each market and re-time to the edit.
4. Create pronunciation entries for product names and region-specific words.
5. Generate takes with `language: "es"` and `language: "ja"` using `POST /tts/bytes` or SSE if caption timing is required.
6. Native reviewers score pronunciation, accent, emotional fit, and compliance.

Expected result: language-specific files that preserve the brand identity while sounding natural to native listeners.

Failure modes:

- Direct translation overfills the timing. Rewrite copy, do not just speed it up.
- Product name pronounces differently by market. Use a separate pronunciation dictionary per locale.
- Consent covers English only. Stop before voice localization or cloning.

Variations:

- Use voice changer from a human guide performance if preserving intonation/timing is more important than exact transcript control.
- Use separate stock voices per locale if brand identity is less important than native naturalness.

### Example: voice changer for a performed line

Production intent: preserve an actor's comic timing but convert the voice to an approved character voice.

Workflow:

1. Confirm rights to the source performance and target voice.
2. Clean the source clip: one speaker, no background music, no overlapping speech, no clipping.
3. Use `POST /voice-changer/bytes` with the target `voice[id]` and a production output format.
4. Compare output to the source clip for timing and intonation retention.
5. Mix in post; do not use volume controls as the final loudness process.

Expected result: same line timing and intonation in the target voice.

Failure modes:

- Background music/noise is carried into or disrupts the conversion.
- Multiple speakers confuse the conversion.
- Legal review rejects the target voice rights.

Variations:

- Use `voice-changer/sse` when a streaming event shape is useful.
- Use TTS from a transcript when exact wording, pronunciation dictionary, or clean pickups matter more than preserving the original performance.

## Source anchors verified 2026-07-10

- Cartesia overview and Sonic model positioning: https://docs.cartesia.ai/get-started/overview
- Sonic 3.5 model page and supported-language/model claims: https://docs.cartesia.ai/build-with-cartesia/tts-models/latest
- Deprecated/sunsetted models and stable offerings: https://docs.cartesia.ai/build-with-cartesia/tts-models/api-changes
- TTS endpoint comparison: https://docs.cartesia.ai/use-the-api/compare-tts-endpoints
- Realtime TTS quickstart: https://docs.cartesia.ai/get-started/realtime-text-to-speech-quickstart
- WebSocket contexts and continuations: https://docs.cartesia.ai/use-the-api/tts-websocket/contexts
- Prompting tips: https://docs.cartesia.ai/build-with-cartesia/capability-guides/prompting-tips
- Custom pronunciations: https://docs.cartesia.ai/build-with-cartesia/capability-guides/custom-pronunciations
- Volume, speed, and emotion: https://docs.cartesia.ai/build-with-cartesia/capability-guides/volume-speed-emotion
- Output format: https://docs.cartesia.ai/build-with-cartesia/capability-guides/tts-output-audio-format
- TTS API references: https://docs.cartesia.ai/api-reference/tts/bytes and https://docs.cartesia.ai/api-reference/tts/sse
- Voice selection and custom voice docs: https://docs.cartesia.ai/build-with-cartesia/capability-guides/choosing-a-voice
- Instant Voice Clone: https://docs.cartesia.ai/build-with-cartesia/capability-guides/clone-voices
- Pro Voice Clone: https://docs.cartesia.ai/build-with-cartesia/capability-guides/clone-voices-pro
- Voice clone API: https://docs.cartesia.ai/api-reference/voices/clone
- Voice localization API: https://docs.cartesia.ai/api-reference/voices/localize
- Voice changer API: https://docs.cartesia.ai/api-reference/voice-changer/bytes and https://docs.cartesia.ai/api-reference/voice-changer/sse
- Pricing: https://docs.cartesia.ai/pricing and https://www.cartesia.ai/pricing
- Concurrency and WebSocket limits: https://docs.cartesia.ai/use-the-api/concurrency-limits-and-timeouts
- API conventions, auth, versioning, errors: https://docs.cartesia.ai/use-the-api/api-conventions
- Zero Data Retention: https://docs.cartesia.ai/enterprise/zero-data-retention
- Data Protection Addendum: https://www.cartesia.ai/legal/dpa
- Acceptable Use Policy: https://www.cartesia.ai/legal/acceptable-use
