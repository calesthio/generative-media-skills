---
name: hume-octave
description: "Use Hume Octave for emotionally expressive speech and voice production: text-to-speech, voice design, voice cloning, voice conversion, streaming/realtime TTS, multilingual narration, dialogue continuity, timestamps/lip-sync, safety/rights review, and production QA."
---

# Hume Octave production guidance

Use Hume Octave when the speech performance matters as much as the words: character narration, emotionally varied voiceover, interactive playback, branded voices, multilingual narration, voice cloning with consent, voice conversion, or audio that needs word/phoneme timestamps.

Do not treat Octave as a generic flat TTS engine. It is strongest when the request needs semantic context, emotional delivery, voice identity, or continuity across related utterances.

Do not use Octave for music, singing, non-speech sound effects, full audio mixing/mastering, source separation, or video generation. Use a separate audio post tool for loudness, noise cleanup, ducking, fades, file normalization, and final mix delivery.

Verification note: provider facts in this skill were checked against official Hume documentation, API reference, pricing, changelog, terms, privacy, and API data-usage pages on 2026-07-10. Re-check volatile facts before quoting exact pricing, plan limits, language lists, model status, or retention controls.

## What Octave can and cannot do

Documented facts:

- Octave is Hume's speech-language model behind its TTS and voice features. Hume describes it as using language-model intelligence to understand text semantically and emotionally, rather than only reading phonemes. Source: https://dev.hume.ai/docs/text-to-speech-tts/overview
- The TTS API supports streaming HTTP output, WebSocket bidirectional streaming, and non-streaming HTTP responses. Source: https://dev.hume.ai/docs/text-to-speech-tts/overview
- Main TTS endpoints are `/v0/tts`, `/v0/tts/file`, `/v0/tts/stream/json`, `/v0/tts/stream/file`, and WebSocket `wss://api.hume.ai/v0/tts/stream/input`. Source: https://dev.hume.ai/reference/text-to-speech-tts/synthesize-json and https://dev.hume.ai/reference/text-to-speech-tts/stream-input
- Octave 1 supports English and Spanish. Octave 2 preview supports English, Japanese, Korean, Spanish, French, Portuguese, Italian, German, Russian, Hindi, and Arabic. Source: https://dev.hume.ai/docs/text-to-speech-tts/overview
- Hume documents model latency around `~200ms` for Octave 1 and `~100ms` for Octave 2 preview, excluding network transit. Streaming instant mode typically has first audio ready around `~200ms`, depending on load and input complexity. Source: https://dev.hume.ai/docs/text-to-speech-tts/overview
- The TTS API limit is 5,000 characters per utterance, 1,000 characters per utterance description, up to 5 generations per request, and output formats `MP3`, `WAV`, and `PCM`. Source: https://dev.hume.ai/docs/text-to-speech-tts/overview
- An utterance can include `text`, optional `voice`, optional `description`, `speed`, and `trailing_silence`. Source: https://dev.hume.ai/reference/text-to-speech-tts/synthesize-json
- `speed` is a non-linear scale from `0.5` to `2.0`; `1.0` is normal. Source: https://dev.hume.ai/docs/text-to-speech-tts/acting-instructions
- `description` acting instructions are documented for Octave 1 only; Hume says Octave 2 support is coming soon. `speed` and `trailing_silence` are supported in all models. Source: https://dev.hume.ai/docs/text-to-speech-tts/acting-instructions
- If you specify `version: "2"`, Hume requires a `voice`; dynamic voice generation without a predefined voice is rejected for Octave 2. Source: https://dev.hume.ai/reference/text-to-speech-tts/synthesize-json
- Voice design from natural-language descriptions currently requires Octave 1, and voices designed with Octave 1 are compatible with Octave 2 requests. Hume says multilingual voice design for Octave 2 is coming soon. Source: https://dev.hume.ai/docs/voice/voice-design
- Voices may be referenced by `id` or by `name`; when using a name, include `provider: "HUME_AI"` for Hume Voice Library voices or `provider: "CUSTOM_VOICE"` for saved custom voices. Source: https://dev.hume.ai/docs/text-to-speech-tts/voice
- Voice cloning can be created from a microphone recording or uploaded audio sample from a consenting speaker; access depends on subscription tier. Hume's TTS overview says cloning can work with as little as 15 seconds of audio. Source: https://dev.hume.ai/docs/voice/voice-cloning and https://dev.hume.ai/docs/text-to-speech-tts/overview
- Voice conversion accepts speech audio plus a target voice and returns converted audio while preserving the source speech patterns, timing, and emotional expression. Source: https://dev.hume.ai/docs/text-to-speech-tts/voice-conversion
- Voice conversion input audio should be human speech, clear, at least 12 seconds and less than 3 minutes, with supported input formats `MP3`, `WAV`, `M4A`, and `OGG`; 44.1 kHz is recommended. Source: https://dev.hume.ai/docs/text-to-speech-tts/voice-conversion
- Octave 2 can return word- and phoneme-level timestamps when requested via `include_timestamp_types`; timestamp requests require `version: "2"`. Source: https://dev.hume.ai/docs/text-to-speech-tts/timestamps
- Phoneme-level timestamps use IPA symbols, with IPA-compatible extensions for some languages. Source: https://dev.hume.ai/docs/text-to-speech-tts/timestamps
- Pricing, monthly included TTS characters, request-per-minute limits, voice cloning availability, and commercial-use permissions vary by plan. Source: https://www.hume.ai/pricing and https://www.hume.ai/terms-of-use
- Hume's terms say Free and Starter plans are limited to non-commercial use, while Creator and above may be used commercially subject to Hume policies. Source: https://www.hume.ai/terms-of-use
- Hume's API Data Usage Policy says customer-submitted API data is not used to train Hume models or improve service offerings. The Terms of Use and Privacy pages should still be checked for license, retention, account settings, and non-API Playground behavior. Sources: https://www.hume.ai/api-data-usage-policy, https://www.hume.ai/terms-of-use, https://dev.hume.ai/docs/resources/privacy

Production heuristics:

- Choose Octave when performance direction is a key creative variable: anxiety, irony, warmth, tension, intimacy, authority, grief, awe, sarcasm, character role, or contextual pronunciation.
- Avoid Octave for scripts that only need ultra-cheap utilitarian readouts, unless Hume is already the available provider and the quota/cost fit.
- For deterministic brand narration, save and reuse a selected voice by ID; do not rely on generating a new voice from the same description every time.
- For hero voiceover, generate 2-5 candidates in exploration, shortlist by listening, save the winning voice, then render final takes against that saved voice.
- For long-form work, split by natural performance beats, not arbitrary character count. Keep each utterance small enough to review and replace independently.
- For real-time apps, stream. For batch rendering, compliance review, or deterministic file management, prefer non-streaming file or JSON.

## Model and endpoint decisions

Use this decision path before building a request:

1. Need a designed voice from a text prompt?
   - Use Octave 1 for the design generation because Hume documents voice design as requiring Octave 1.
   - Generate several candidates, listen, then save the winning generation as a custom voice.
   - Use that saved voice in later Octave 1 or Octave 2 synthesis.
2. Need the latest multilingual support, timestamps, or lower model latency?
   - Use `version: "2"` with a saved or library voice.
   - Do not omit the voice.
3. Need natural-language acting instructions through `description`?
   - Use Octave 1 if the instruction needs to change emotional delivery directly through `description`.
   - For Octave 2, use voice choice, script wording, punctuation, `speed`, `trailing_silence`, and context; do not promise `description` acting-instruction support until Hume documents it as live.
4. Need immediate playback?
   - Use `/v0/tts/stream/file` if the player wants bytes.
   - Use `/v0/tts/stream/json` if the app needs audio plus chunk metadata.
   - Use WebSocket `/v0/tts/stream/input` when text arrives incrementally and audio should return continuously.
5. Need captions, karaoke highlighting, avatar lip sync, or precise edit points?
   - Use Octave 2 with `include_timestamp_types: ["word"]` or `["word", "phoneme"]`.
6. Need multiple audition candidates?
   - Use `num_generations` up to 5.
   - Disable instant mode if the request is streaming and uses dynamic voice generation or multiple generations.
7. Need a simple finished file?
   - Use non-streaming `/v0/tts/file` for an audio file response or `/v0/tts` for base64 JSON plus metadata.

## Voice strategy

Separate voice identity from performance direction.

Voice identity answers: who is speaking? Age impression, accent, vocal register, personality, role, brand feel, texture, default energy, trustworthiness, and relation to the listener.

Performance direction answers: how is this utterance delivered right now? Whispered, urgent, relieved, skeptical, conspiratorial, laughing through disbelief, paced for meditation, pausing after a reveal, or brightening at a call to action.

For a reusable production voice:

1. Write a voice description that describes a person or role, not a pile of adjectives.
2. Pair it with a sample line that naturally demonstrates the intended delivery.
3. Generate multiple candidates.
4. Save the best candidate.
5. Lock future production to the saved voice ID or name.
6. Keep acting instructions short and local to each utterance.

Good voice descriptions usually include:

- Role: narrator, support agent, product guide, folklore storyteller, field researcher, exhausted astronaut.
- Relationship to listener: trusted colleague, private confidant, mentor, host, mischievous friend.
- Sound: warm alto, crisp baritone, gravelly, breathy, resonant, nasal, clean, slight rasp.
- Accent and language: only when necessary and appropriate.
- Pace and clarity: measured, rapid, deliberate, precise, conversational.
- Emotional baseline: calm curiosity, restrained excitement, sardonic amusement, grounded empathy.
- Performance context: intimate headphone narration, stadium announcement, whispered museum audio guide, tense mission-control update.

Avoid voice descriptions that:

- Request a real person, celebrity, politician, living performer, or copyrighted character voice unless rights and consent are explicit and the use is legally cleared.
- Stack contradictory traits without priority, such as "flat but highly emotional, very fast with long pauses."
- Use visual-only details without translating them into sound.
- Depend on emojis, Markdown, HTML, or non-speech markup. Hume recommends clean standard formatting for prompts.

## Acting, pacing, and dialogue direction

Documented controls:

- `description`: natural-language delivery instruction for an utterance, documented for Octave 1 acting instructions.
- `speed`: non-linear speaking-rate control from `0.5` to `2.0`.
- `trailing_silence`: seconds of silence after an utterance.
- punctuation and script wording: used by the model as performance cues.
- `context`: prior generation or context utterances that guide style and prosody but are not themselves converted to output.

Production heuristics:

- Put stable identity in the voice; put momentary emotion in the utterance description.
- Prefer specific playable actor direction over abstract labels. "Trying not to sound worried while reporting bad news" is better than "anxious."
- Avoid over-controlling every clause. Give the model the emotional arc and let punctuation carry smaller beats.
- Use commas, em dashes, sentence breaks, and short paragraphs as performance structure, but keep text readable as speech.
- Use `trailing_silence` for deliberate pauses between beats, not for full edit timing; final silence and fades should be handled in audio post.
- For comedy or sarcasm, name the social situation and target. Sarcasm without context often becomes generic snark.
- For accessibility and training narration, choose clarity over theatricality; expressive does not mean melodramatic.

## Continuation and long-form speech

Use continuation when the listener must feel one continuous performance across paragraphs, scenes, or turns.

Documented options:

- Put multiple utterances in one request. Each utterance continues from the immediately previous utterance.
- Continue from a previous call using `context.generation_id`.
- Provide context utterances that guide delivery without being converted to speech. Source: https://dev.hume.ai/docs/text-to-speech-tts/continuation

Production heuristics:

- Use continuation for audiobooks, podcasts, multi-scene narration, recurring characters, and ambiguous pronunciation that depends on previous context.
- Avoid long single utterances. Use multiple utterances to preserve reviewability and allow replacements.
- When context would leak unwanted emotion into a new scene, reset by starting a new request without context.
- Keep speaker turns as separate utterances with explicit voices if the script uses more than one speaker.
- Store `generation_id`, voice ID, text, model version, format, and timestamp settings with every approved take for later patching.

## Multilingual and pronunciation workflow

Documented facts:

- Octave 2 preview supports 11 listed languages as of 2026-07-10; Octave 1 supports English and Spanish.
- Octave 2 provides word/phoneme timestamps when requested.
- Hume's Octave 2 launch material says Octave 2 improves pronunciation of uncommon words, repeated words, numbers, and symbols. Source: https://www.hume.ai/blog/octave-2-launch

Production heuristics:

- For non-English work, use Octave 2 with a compatible saved or library voice.
- Confirm the selected voice sounds native or intentionally accented in the target language. Do not assume a voice ID is equally strong in every language.
- For names, brands, acronyms, and domain terms, generate a pronunciation test sentence before rendering the full script.
- Write numbers, dates, URLs, and units the way they should be spoken if exact delivery matters.
- Use word timestamps for subtitle alignment and phoneme timestamps only when lipsync or phonetic timing is required.
- If a pronunciation keeps failing, rewrite the word phonetically in the script for that take, document the substitution, and verify the transcript/caption still uses the correct spelling.

## Voice cloning and voice conversion

Only proceed with cloning or conversion after rights and consent are explicit.

Required safety checks:

- Confirm the speaker owns the voice sample or has permission from the speaker/rightsholder.
- Confirm the intended use, distribution, territory, duration, and commercial status.
- Do not clone or convert voices for impersonation, deception, fraud, political misrepresentation, harassment, explicit content involving a non-consenting identity, or evasion of platform safeguards.
- For paid/commercial client work, keep a consent record outside the generated asset folder: speaker name or pseudonym, consent scope, allowed channels, expiration if any, and whether revocation is supported.
- If the request names a famous person, politician, coworker, private individual, or "make it sound like X," stop and ask for proof of rights or redirect to a new synthetic voice with similar non-identifying qualities.

Voice cloning production notes:

- Use clean, dry speech with minimal background noise, music, reverb, overlap, or room echo.
- The documented UI recording session is short, but production cloning benefits from a clear sample with varied vowels, normal speaking pace, and no performative exaggeration unless that style should be cloned.
- Audition cloned voices in multiple emotional contexts before committing to a campaign.

Voice conversion production notes:

- Use conversion when the source performance timing and emotional expression are valuable and the vocal identity needs to change.
- Respect Hume's input guidance: human speech, clear audio, at least 12 seconds and less than 3 minutes, supported format, 44.1 kHz recommended.
- Test a 12-30 second section first, then scale.
- Check for timing drift, artifacts on breaths/fricatives, accent mismatch, and loss of intelligibility.

## Request construction patterns

### Example: audition and save a designed voice

Intent: create a reusable brand narrator, then use the saved voice for future renders.

Model choice: Octave 1 for voice design because Hume documents voice design as requiring Octave 1. Generate multiple candidates and save the selected `generation_id` as a voice.

Example request:

```bash
curl https://api.hume.ai/v0/tts \
  -H "X-Hume-Api-Key: $HUME_API_KEY" \
  --json '{
    "version": "1",
    "num_generations": 3,
    "instant_mode": false,
    "utterances": [
      {
        "text": "Here is the part most teams miss: speed is not the same thing as momentum.",
        "description": "The speaker is a calm, sharp product strategist in their late 30s with a warm, precise voice. They sound trusted by founders: quietly confident, conversational, never salesy, with a slight smile when revealing an insight."
      }
    ],
    "format": { "type": "mp3" }
  }'
```

Then save the winning generation:

```bash
curl https://api.hume.ai/v0/tts/voices \
  -H "X-Hume-Api-Key: $HUME_API_KEY" \
  --json '{
    "generation_id": "WINNING_GENERATION_ID",
    "name": "quiet-strategist-brand-narrator"
  }'
```

Expected result: several distinct but related narrator candidates. Choose the one that feels on-brand, save it, and use its ID for production. Failure modes: description too broad, candidates too theatrical, or sample line not representative of the campaign.

### Example: Octave 2 multilingual narration with timestamps

Intent: generate a Spanish product explainer line with word timestamps for subtitle highlighting.

Model choice: Octave 2 for multilingual support and timestamps. Use a saved or library voice because Octave 2 requests require a voice.

Example request:

```bash
curl https://api.hume.ai/v0/tts/stream/json \
  -H "X-Hume-Api-Key: $HUME_API_KEY" \
  --json '{
    "version": "2",
    "include_timestamp_types": ["word"],
    "utterances": [
      {
        "voice": { "id": "YOUR_COMPATIBLE_VOICE_ID" },
        "text": "En menos de un minuto, tu equipo puede convertir una idea en una campana lista para revisar.",
        "speed": 0.95,
        "trailing_silence": 0.35
      }
    ],
    "format": { "type": "mp3" }
  }'
```

Expected result: streamed chunks with audio and word-timestamp objects. Failure modes: voice not suitable for Spanish, punctuation creating odd emphasis, or downstream caption code expecting a single finished file rather than streamed chunks.

### Example: long-form audiobook-style continuity

Intent: preserve the narrator's emotional state across a scene shift.

Model choice: use a saved voice and either multiple utterances in one request or `context.generation_id` from the previous approved take.

Example request:

```bash
curl https://api.hume.ai/v0/tts \
  -H "X-Hume-Api-Key: $HUME_API_KEY" \
  --json '{
    "version": "1",
    "utterances": [
      {
        "voice": { "name": "quiet-strategist-brand-narrator", "provider": "CUSTOM_VOICE" },
        "text": "The office was silent by then. Even the monitors seemed to be waiting.",
        "description": "Low and restrained, as if holding back the conclusion until the listener leans in."
      },
      {
        "text": "Then the dashboard refreshed, and every number turned green.",
        "description": "Relief arrives slowly at first, then opens into a small, disbelieving smile."
      }
    ],
    "split_utterances": true,
    "format": { "type": "wav" }
  }'
```

Expected result: two reviewable snippets that still feel emotionally connected. Failure modes: overacted second line, insufficient pause, or too much carryover into the next unrelated scene.

### Example: consent-gated voice conversion

Intent: convert an approved voice actor's guide performance into a saved brand voice while preserving timing.

Workflow:

1. Verify written consent covers voice conversion and the final distribution.
2. Prepare a clean 12-30 second pilot clip in WAV or high-quality MP3.
3. Select a target saved voice or Hume Voice Library voice.
4. Run `/v0/tts/voice_conversion/file`.
5. QA the pilot for timing, intelligibility, artifacts, and emotional preservation.
6. Convert the rest only after the pilot passes.

Example request:

```bash
curl --location "https://api.hume.ai/v0/tts/voice_conversion/file" \
  -H "X-Hume-Api-Key: $HUME_API_KEY" \
  --output converted-pilot.wav \
  -F "audio=@pilot.wav" \
  -F "voice[name]=Inspiring Man" \
  -F "voice[provider]=HUME_AI"
```

Expected result: target vocal identity with the source timing and expression. Critical failures: no consent record, source contains music/noise, conversion loses key words, or output creates deceptive impersonation risk.

## QA checklist

Run this review before accepting generated speech:

- Rights: voice, script, references, cloned samples, converted audio, and commercial plan permissions are cleared.
- Model/version: chosen version matches the need; Octave 2 requests include a valid voice.
- Language: supported by the chosen version; voice sounds appropriate in that language.
- Delivery: emotion is specific and useful, not generically "dramatic."
- Intelligibility: names, numbers, acronyms, technical terms, and brand words are correct.
- Continuity: long-form segments do not jump in energy, accent, pacing, room tone, or character intent.
- Timing: duration matches the edit; pauses are intentional; no clipped starts/ends.
- Format: output format fits downstream use; sample rate and channel needs are handled in post if needed.
- Metadata: save request ID, generation ID, voice ID/name/provider, version, endpoint, timestamp settings, and final file path.
- Streaming: player handles chunk ordering, headers, binary/base64 format, and final chunk status.
- Timestamps: requested only when needed; verify alignment against actual audio.
- Privacy: sensitive text and audio comply with account settings and client policy; PHI is not sent unless the required agreements are in place.
- Disclosure: for synthetic or cloned voices, follow project, jurisdiction, platform, and client disclosure requirements.

## Cost, limits, and privacy handling

Treat pricing and limits as volatile. As of 2026-07-10, Hume's pricing page lists plan-dependent monthly included TTS characters, additional character costs, request-per-minute limits, unlimited voice cloning creation/use on listed plans, and commercial licensing only on Creator and above. Re-check before committing a quote or production budget. Source: https://www.hume.ai/pricing

For budget planning:

- Estimate characters from the final script before generation.
- Add exploration budget for candidate voices and alternate takes.
- Use non-streaming file outputs for batch renders that can be retried cleanly.
- Keep `num_generations` for auditions, not final production at scale.
- Archive only approved takes and metadata needed for regeneration.

For privacy:

- Hume's API Data Usage Policy says API customer data is not used to train or improve Hume models. Source: https://www.hume.ai/api-data-usage-policy
- Hume's privacy docs describe account controls for data retention/training opt-out, primarily around EVI, and say non-API consumer products such as Playground/Demo may differ. Source: https://dev.hume.ai/docs/resources/privacy
- Hume's Terms include licenses and restrictions that must be reviewed for the exact project, especially if using non-API tools, cloning, PHI, or commercial deployment. Source: https://www.hume.ai/terms-of-use
- For regulated or confidential work, confirm whether the client requires a DPA, BAA, zero-retention behavior, no Playground use, or enterprise plan before uploading sensitive audio/text.

## Common failure modes and repairs

- Voice sounds good once but cannot be reproduced: save the selected generation as a voice and reference the voice ID.
- Octave 2 request fails: check that a voice is provided and that the voice is compatible with Octave 2.
- Acting instruction ignored on Octave 2: `description` acting instructions are documented for Octave 1 only; switch to Octave 1 for that take or adjust script, speed, silence, voice, and context.
- Latency too high for interactive UX: use streaming, instant mode, a predefined voice, one generation, shorter utterances, and avoid heavy context.
- Dynamic voice generation does not work with instant mode: disable instant mode or use a saved voice.
- Multiple candidates fail with instant mode: disable instant mode and keep `num_generations` between 1 and 5.
- Caption alignment missing: request Octave 2 timestamps with `include_timestamp_types`.
- Long utterance distorts when `split_utterances: false`: re-enable splitting or break the text into shorter utterances.
- Pronunciation fails: test a short line, rewrite the problematic token for speech, use context, and document the intended spelling for captions.
- Voice conversion artifacting: shorten the source, improve source audio, remove background music/noise, and test a different target voice.
- Rights risk: replace an identifying cloned/imitation request with a new synthetic voice described by non-identifying traits.

## Source map

Official sources verified 2026-07-10:

- Hume TTS overview and limits: https://dev.hume.ai/docs/text-to-speech-tts/overview
- TTS API reference: https://dev.hume.ai/reference/text-to-speech-tts/synthesize-json
- Streaming JSON reference: https://dev.hume.ai/reference/text-to-speech-tts/synthesize-json-streaming
- WebSocket stream input reference: https://dev.hume.ai/reference/text-to-speech-tts/stream-input
- Voice overview: https://dev.hume.ai/docs/voice/overview
- Voice design: https://dev.hume.ai/docs/voice/voice-design
- Voice guide for TTS: https://dev.hume.ai/docs/text-to-speech-tts/voice
- Voice cloning: https://dev.hume.ai/docs/voice/voice-cloning
- Acting instructions: https://dev.hume.ai/docs/text-to-speech-tts/acting-instructions
- Continuation: https://dev.hume.ai/docs/text-to-speech-tts/continuation
- Timestamps: https://dev.hume.ai/docs/text-to-speech-tts/timestamps
- Voice conversion: https://dev.hume.ai/docs/text-to-speech-tts/voice-conversion
- Octave 2 launch/changelog context: https://www.hume.ai/blog/octave-2-launch and https://dev.hume.ai/changelog
- Pricing: https://www.hume.ai/pricing
- Terms: https://www.hume.ai/terms-of-use
- Privacy: https://dev.hume.ai/docs/resources/privacy
- API data usage policy: https://www.hume.ai/api-data-usage-policy
