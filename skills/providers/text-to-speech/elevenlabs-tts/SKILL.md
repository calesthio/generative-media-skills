---
name: elevenlabs-tts
description: Produce, direct, integrate, and quality-control ElevenLabs text-to-speech for narration, character performance, multilingual media, long-form voiceover, and streamed or batch AI-content audio. Use when selecting ElevenLabs models or voices; preparing spoken text; controlling pronunciation, pacing, emotion, and code-switching; using TTS APIs; cloning or designing a voice with consent; repairing artifacts; mastering deliverables; or evaluating generated speech. Excludes music, sound-effect generation, conversational-agent design, and general speech recognition except transcription used to verify TTS.
---

# ElevenLabs TTS production

Treat speech generation as casting, script adaptation, performance direction, rendering, and finishing—not as a single API call. Optimize for the listener and delivery channel, then for latency or cost.

## Evidence labels

Interpret guidance by its label:

- **Documented** — ElevenLabs documentation, API reference, or current policy states this.
- **Standard** — a named speech/audio standard states this.
- **Production heuristic** — a practical starting point; validate it on the actual voice, model, script, and channel.
- **Inference** — a conclusion drawn from documented behavior; test before relying on it.

Volatile ElevenLabs facts in this skill were checked on **2026-07-09**. Before a consequential production run, query `GET /v1/models`, inspect the chosen voice, and recheck the current API reference, plan entitlements, policies, and terms. Never infer current availability from an old voice name or model list.

## Scope boundary

Use this skill for rendered speech and voice production. Do not expand into:

- music or sound-effect generation;
- dialogue-system logic, turn-taking, tools, telephony orchestration, or conversational-agent prompting;
- speech-to-speech except to explain why it is not TTS;
- general transcription, dubbing, or localization workflows;
- legal conclusions. Flag rights questions for qualified review.

Speech-to-text may be used only as one TTS QA signal. It must not replace listening.

## Start with a production contract

Before selecting a model, write down:

1. audience, language, regional accent, and accessibility needs;
2. medium and destination: video narration, audiobook, ad, game character, course, IVR, or live playback;
3. performance: credible, intimate, restrained, comic, urgent, dramatic, etc.;
4. target duration and synchronization constraints;
5. latency mode: offline, complete-text streaming, or incremental-text streaming;
6. volume of text and revision pattern;
7. identity requirement: stock/library, designed, IVC, or PVC;
8. pronunciation list: names, brands, acronyms, numbers, URLs, formulae, and code;
9. delivery format, sample rate, channels, loudness specification, and caption/timing need;
10. rights, consent, disclosure, privacy, plan, and budget constraints.

Do not approve a voice from a showcase sentence. Audition finalists with the actual script's hardest 20–40 seconds: emotional turns, proper nouns, numbers, and language switches.

## Choose the model by the job

**Documented, verified 2026-07-09:** current core TTS model IDs and per-request limits are listed on the [ElevenLabs models page](https://elevenlabs.io/docs/overview/models). Query the models endpoint before execution.

| Model | Use it when | Important limits and tradeoffs |
|---|---|---|
| `eleven_v3` | Performance, dramatic range, inline audio tags, broad multilingual work, or native IPA control are central. | 5,000 characters/request; 70+ languages. The TTS input WebSocket and request stitching do not support v3. It does not support SSML break tags. Speaker Boost is unavailable. Greater expressiveness can increase variance and artifact risk. |
| `eleven_multilingual_v2` | Stable long-form narration, professional voiceover, and high-fidelity multilingual content matter more than minimum latency. | 10,000 characters/request; 29 languages. Official guidance identifies it as the most stable long-form model. `language_code` is not supported for this model. Use alias dictionaries rather than phoneme tags. |
| `eleven_flash_v2_5` | Low latency, scale, or incremental TTS matters and the content spans its 32 supported languages. | 40,000 characters/request; roughly 75 ms model inference for typical short inputs, excluding network/application latency. Normalize numbers, dates, currencies, URLs, and abbreviations before synthesis. |
| `eleven_flash_v2` | English-only low-latency work needs phoneme-tag support. | English only; 30,000 characters/request. It supports phoneme tags and TTS WebSocket input streaming. |

**Documented:** ElevenLabs describes Turbo v2/v2.5 as functionally equivalent to corresponding Flash models but slower on average, and recommends Flash instead. Legacy `eleven_monolingual_v1` and `eleven_multilingual_v1` were scheduled for removal on 2026-07-09; do not start new work on them. Treat any still-visible legacy ID as migration-only.

**Production heuristic:** render the same difficult audition on two plausible model/voice combinations. Select by blind listening, pronunciation accuracy, timing, and revision stability—not provider marketing adjectives.

## Cast the voice before tuning settings

**Documented:** ElevenLabs' product guide ranks voice selection ahead of model selection and settings. A voice carries its source accent, cadence, timbre, recording traits, and performance range.

Choose among:

- **Voice Library / community PVC:** fastest route to a production voice. Filter by language, accent, category, age, and Studio Quality. Check the voice's notice period and `disable_at_unix`; shared voices can become unavailable. Preserve an approved fallback voice and a migration test.
- **Voice Design:** use when no suitable existing voice exists and a synthetic identity is acceptable. Describe native language and dialect first, then perceived age, vocal weight/timbre, pacing, persona, emotion, and recording quality. Preview with script text that actually expresses the intended performance.
- **Instant Voice Clone (IVC):** use for rapid exploration or personalization with explicit authorization. **Documented:** approximately 1–2 minutes of clean, consistent, single-speaker audio is recommended; more than three minutes may not help. IVC imitates performance and recording defects as well as voice traits.
- **Professional Voice Clone (PVC):** use when identity fidelity and repeatable production quality justify a curated dataset and verification. **Documented, verified 2026-07-09:** PVC creation is limited to cloning your own voice; speaker authorization is not a mechanism for a producer to create somebody else's PVC. The current product guide recommends at least one hour and ideally close to three hours of clean, single-speaker spoken audio. Singing is not supported for PVC training. The voice owner must create and verify their own PVC through the supported flow, then use approved sharing/workspace controls where available.

### Audition matrix

Keep the text, model, and output format fixed while comparing voices. Score each 1–5 on:

- semantic intelligibility;
- target accent and phoneme accuracy;
- credibility for role and audience;
- emotional range without overacting;
- pacing and breath behavior;
- voice identity consistency across three renders;
- sibilance, plosives, reverb, noise, clicks, warble, and distortion;
- performance on code-switches and difficult terms;
- latency, access continuity, and licensing fit.

Reject a voice whose source performance conflicts with the requested direction. A tag such as `[whispers]` cannot reliably turn a shout-trained voice into an intimate whisper.

## Prepare text for speech, not for reading

Create a spoken-text version separate from the editorial script. Preserve the original for traceability.

1. Resolve ambiguous meaning before synthesis.
2. Expand tokens according to intended speech, locale, and context:
   - `01/02/2026` → choose “January second, twenty twenty-six” or “the first of February, twenty twenty-six”;
   - `$1.05` → choose “one dollar and five cents,” not a mechanical character reading;
   - `Dr.` → decide “Doctor” versus “Drive”;
   - `IV` → decide “four,” “the fourth,” or “I V”;
   - URLs, email addresses, units, shortcuts, and product codes → spell the listener-facing form explicitly.
3. Break dense written sentences into speakable clauses. Replace nested parentheses, slash choices, and table-like prose.
4. Use punctuation as performance notation, not decoration.
5. Mark pronunciation and emphasis separately from caption text when the spoken form differs.
6. Read the spoken-text version aloud. If a human cannot deliver it naturally in one pass, TTS will probably expose the same problem.

**Documented:** Multilingual v2 generally normalizes complex numeric text more naturally than Flash v2.5. The API exposes `apply_text_normalization` as `auto`, `on`, or `off`; plan/model behavior can differ. Do not assume the normalizer knows the business meaning of an ambiguous number.

**Production heuristic:** normalize deterministically in your application for brand names, IDs, prices, dates, and compliance statements. Store both display text and spoken text.

## Control pronunciation with the least fragile method

Use this escalation ladder:

1. Rewrite the spoken text unambiguously.
2. Try a native voice that matches the target language and accent.
3. Use an alias rule in a pronunciation dictionary.
4. Use model-supported phonetic control.
5. Generate the word or phrase as an isolated repair only if it can be edited without an audible seam.

### Model-specific pronunciation

- **Eleven v3:** **Documented:** place standard IPA directly in the text between forward slashes, including stress marks where needed, for example `The enzyme /ˌrɪbəʊnjuːˈkleɪeɪs/ breaks the bond.` V3 IPA is not perfectly deterministic; audition multiple renders when exactness matters.
- **Flash v2:** **Documented:** SSML-like `<phoneme>` tags support CMU Arpabet or IPA for individual words. CMU Arpabet is the documented consistency preference for English.
- **Multilingual v2 and Flash v2.5:** use pronunciation-dictionary aliases or spoken-text substitutions; phoneme rules are skipped where unsupported.
- **Dictionaries:** **Documented:** PLS files are case-sensitive. API requests accept up to three `pronunciation_dictionary_locators`, applied in order. Pin both dictionary ID and version ID in the render manifest.

Never paste unsupported XML and assume it will be interpreted. Test a dictionary using the exact voice/model pair; a correct lexicon can still sound wrong in context.

## Direct pacing and expression by model

### V2 and Flash family

- Start from the voice's stored settings and change one control at a time.
- **Documented:** `stability` spans 0–1. Lower values broaden emotional variation; higher values reduce variation and can become monotone.
- **Documented:** `similarity_boost` spans 0–1 and controls adherence to the source voice. Very high similarity may reproduce source defects.
- **Documented:** `style` exaggerates source style, can increase latency and instability, and should normally begin at `0`.
- **Documented:** `use_speaker_boost` can subtly increase identity similarity at a latency cost.
- **Documented:** `speed` supports 0.7–1.2, with 1.0 neutral; extremes can reduce quality.
- Use `<break time="1.2s" />` only on models that support break tags. **Documented:** breaks can be up to three seconds; excessive tags may introduce speed changes or artifacts.

**Production heuristic:** do not compensate for a bad cast with extreme settings. Test a compact grid around the stored voice settings, then lock the chosen settings in the manifest.

### Eleven v3

- Choose Creative, Natural, or Robust stability behavior in the available interface. Creative is more expressive and more failure-prone; Natural balances source fidelity and direction; Robust is steadier but less responsive.
- Use short, audible inline directions such as `[whispers]`, `[sighs]`, `[curious]`, or `[excited]` only when they fit the voice and scene.
- Use ellipses for weight, capitalization sparingly for emphasis, and conventional punctuation for phrasing.
- Do not use SSML break tags. Direct pauses with punctuation, line structure, or suitable v3 audio tags.
- Do not add environmental SFX tags in a TTS-only production. Keep the speech stem clean and create non-speech material in its proper workflow.

**Production heuristic:** tags are performance suggestions, not deterministic commands. Generate variants, select the take, and log the exact text, voice, model, settings, seed, and request ID. A seed is only a best-effort repeatability aid; the API does not guarantee determinism.

## Multilingual speech and code-switching

**Documented:** use a voice trained in the target language and region for the most natural accent. A voice used outside its training language may retain or drift toward its source accent. Website language detection can be confused by multiple languages in one prompt; the API's optional ISO 639-1 `language_code` can disambiguate supported models and normalization, but is not supported by Multilingual v2.

For one target language:

1. use a native or appropriately trained voice;
2. localize meaning, number reading, politeness, and sentence rhythm—not words alone;
3. create a locale-specific pronunciation list;
4. audition native listeners using the target distribution device.

For code-switching:

1. identify the intended base language and the exact switch boundaries;
2. test a single multilingual voice first if identity continuity is important;
3. if language detection, accent, or rhythm drifts, render at natural clause boundaries per language;
4. use matched voices or the same verified multilingual voice, then edit with room-tone-consistent gaps and loudness matching;
5. do not force a single `language_code` across genuinely mixed-language text;
6. inspect proper nouns that are intentionally pronounced in one language inside another.

**Inference:** v3's broader language coverage may reduce the need to split some mixed-language performances, but its higher expressive variance can still create accent or timing discontinuities. Test the actual combination.

## Long-form narration

Prefer ElevenCreative Studio when editors need paragraph-level generation history, locking, timing edits, pronunciation dictionaries, collaboration, and chapter/project export. Use the API when the pipeline needs deterministic manifests, automated batching, programmatic retry, or custom assembly.

For API long-form work:

1. split on paragraphs or sentence boundaries, never arbitrary character counts unless a single sentence exceeds the model limit;
2. keep a scene or coherent rhetorical beat together when possible;
3. carry the same voice, model, settings, dictionary version, output format, and text-normalization policy;
4. include `previous_text` and `next_text` for boundary context, or use request stitching with prior request IDs where supported;
5. **Documented:** request stitching is not available for v3; request IDs must be fully processed and should be no older than two hours; it is unavailable when zero-retention mode removes history;
6. regenerate a bad middle chunk with both preceding and following context or request IDs;
7. leave edit handles at chunk boundaries, then crossfade only if it does not smear consonants or timing;
8. listen across every seam at normal speed and on headphones.

**Production heuristic:** a paragraph is a useful editing unit, not a universal chunk size. Very short chunks lose prosodic context; very long chunks make repair expensive and can drift. Choose chunks by discourse and revision risk.

## Choose API behavior deliberately

### Complete response (`POST /v1/text-to-speech/{voice_id}`)

Use when the complete text is known, simplicity matters, and playback can wait for the full response.

### HTTP streaming (`.../{voice_id}/stream`)

Use when the complete text is known but a listener should hear audio before the render finishes. It changes time-to-first-audio, not the need for textual context.

### Input WebSocket (`.../{voice_id}/stream-input`)

Use when text arrives incrementally. **Documented:** it does not support `eleven_v3`. Prefer `auto_mode`; otherwise keep the default `chunk_length_schedule` until measured evidence justifies a change. Smaller text thresholds can reduce latency but commit prosody before enough context exists. Send `flush: true` at a turn boundary where supported; an empty text string closes the connection, while a single space can keep it alive. The current guide states that idle connections close after 20 seconds.

### Timing endpoints

Use speech-with-timestamps or stream-with-timestamps when captions, word highlighting, lip-sync guides, or edit alignment are required. The response contains base64 audio and character alignment for original and normalized text. Validate timing after final text and audio edits.

### Output format

- Choose PCM/WAV at the editing sample rate when plan access and storage permit; avoid repeated lossy transcodes.
- Use MP3 for compact review/delivery when accepted by the destination.
- Use 8 kHz μ-law or A-law only for telephony paths that require them.
- **Documented:** the endpoint default is `mp3_44100_128`; higher-quality formats can require higher tiers. Treat plan entitlements as volatile.

### Production integration rules

- Load `ELEVENLABS_API_KEY` from a secret store; never log or ship it to a client.
- Query models and voices during preflight. Do not hardcode a display name as identity; pin `voice_id`.
- Cache by a hash of all output-affecting inputs: spoken text, voice ID, model ID, settings, dictionary/version, language/normalization flags, and output format.
- Preserve request IDs and response metadata unless privacy mode forbids it.
- Bound parallelism below the current plan's concurrency limit and inspect `current-concurrent-requests` / `maximum-concurrent-requests` headers.
- On `429`, distinguish rate limit from concurrent-limit error and use exponential backoff with jitter or wait for active work to finish. Retry transient `5xx`; do not blindly retry authentication or invalid payloads.
- Treat `optimize_streaming_latency` as deprecated.
- Parse additive response fields leniently and monitor the weekly changelog.

## Example 1 — complete offline explainer narration

**Example, not a mandatory formula.**

**Intent:** produce a polished 45-second English product explainer with two brand names, a price, and caption timing. Latency is irrelevant; stable delivery and clean revision are primary.

**Selection:** audition native regional narration voices on the hardest paragraph; choose `eleven_multilingual_v2` for steady professional narration. Use an alias dictionary for the brand name because Multilingual v2 does not use phoneme tags.

**Spoken text:**

```text
Meet Auralis. It turns a forty-nine-dollar monthly workflow into one clear production board.

Import the brief, approve each voice take, and export a review link—without renaming files by hand.
```

**Alias dictionary excerpt (`auralis-brand.pls`):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0"
  xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
  alphabet="ipa"
  xml:lang="en-US">
  <lexeme>
    <grapheme>Auralis</grapheme>
    <alias>aw RAL iss</alias>
  </lexeme>
</lexicon>
```

**Render manifest excerpt:**

```yaml
provider: elevenlabs
model_id: eleven_multilingual_v2
voice_id: <auditioned-native-narration-voice-id>
output_format: mp3_44100_128
voice_settings:
  stability: 0.62
  similarity_boost: 0.76
  style: 0.0
  use_speaker_boost: true
  speed: 0.97
pronunciation_dictionary:
  id: <dictionary-id>
  version_id: <pinned-version-id>
text_normalization: auto
```

**Complete Python call:**

```python
import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from elevenlabs.play import PronunciationDictionaryVersionLocator

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

audio = client.text_to_speech.convert(
    voice_id=os.environ["ELEVENLABS_VOICE_ID"],
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
    text=(
        "Meet Auralis. It turns a forty-nine-dollar "
        "monthly workflow into one clear production board.\n\n"
        "Import the brief, approve each voice take, and export a review link—"
        "without renaming files by hand."
    ),
    voice_settings=VoiceSettings(
        stability=0.62,
        similarity_boost=0.76,
        style=0.0,
        use_speaker_boost=True,
        speed=0.97,
    ),
    pronunciation_dictionary_locators=[
        PronunciationDictionaryVersionLocator(
            pronunciation_dictionary_id=os.environ["ELEVENLABS_DICT_ID"],
            version_id=os.environ["ELEVENLABS_DICT_VERSION"],
        )
    ],
)

with open("narration.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

**Why:** the text expands price and hyphenates spoken phrasing; the dictionary makes the brand reusable; moderate stability preserves life without making revisions chaotic; style begins at zero.

**Expected result:** credible, restrained narration with the price and brand pronounced consistently. Generate a timestamped version separately if the SDK surface in use requires a distinct method.

**Likely failures and repairs:**

- “Auralis” still wrong → test the alias in context, then compare an alternate native voice.
- first paragraph too promotional → reduce textual hype and audition a calmer voice before raising stability.
- dash creates an overlong pause → replace it with a comma or split the sentence.
- captions disagree with spoken expansion → retain display text separately and map timestamps to the spoken version.

**Variation:** for a live preview, keep the same model/voice but use HTTP streaming; do not move to the input WebSocket because the full script is already known.

## Example 2 — expressive v3 character beat

**Example, not a mandatory formula.**

**Intent:** create a 15-second game teaser line that moves from confidential to delighted while precisely pronouncing a fictional name.

**Selection:** use a consent-cleared designed voice whose source range already supports whisper and excitement; choose `eleven_v3` for inline performance direction and native IPA.

**Complete input:**

```text
[whispers] They told us the vault beneath /keɪˈlɔːrə/ was empty...

[restrained excitement] They were VERY wrong. [soft laugh]
```

**Parameters:** `model_id=eleven_v3`, selected v3-compatible voice, HTTP complete or HTTP stream endpoint, v3 Natural stability behavior, `speed=1.0`, `output_format=mp3_44100_128`, fixed seed only as a best-effort comparison aid. Do not send SSML breaks or Speaker Boost.

**Why:** the cast already supports the intended range; tags describe audible delivery; IPA is selective; punctuation provides the pause.

**Expected result:** a controlled whisper, a weighted pause, then contained excitement without changing speaker identity.

**Likely failures and repairs:**

- word or tags are spoken literally → verify the v3 model ID and exact syntax.
- whisper collapses or hisses → choose a more suitable voice or make the direction less extreme.
- laughter overwhelms dialogue → remove it or render a cleaner take; do not rely on trimming if it masks a word.
- pronunciation varies → verify stress marks, render several candidates, or use a spoken alias.

**Variation:** for a stable 20-minute narrator, switch the production design to Multilingual v2 and paragraph chunks rather than forcing v3 to behave like a long-form stability model.

## Example 3 — bilingual code-switching fallback plan

**Example, not a mandatory formula.**

**Intent:** narrate an English tutorial containing a Spanish customer quote while preserving one narrator identity.

**Inputs:** native bilingual voice audition, English base text, reviewed Spanish quote, locale-specific pronunciations, 48 kHz edit timeline.

**Workflow:**

1. Test the full paragraph on v3 and Multilingual v2 with the bilingual voice.
2. If the switch is natural, keep one generation and log the winning model.
3. If the Spanish segment drifts, split at clause boundaries:
   - English: “The customer described the setup in one sentence:”
   - Spanish: “Por fin, todo está en un solo lugar.”
   - English: “That is the entire promise.”
4. Render each clause with the same voice where it performs natively. Do not force one `language_code` over the mixed paragraph.
5. Assemble with the intended pauses, match integrated loudness, and listen through both seams.

**Expected result:** intelligible switches without an accidental caricatured accent or identity jump.

**Likely failures:** language detector chooses the wrong language on the short quote; English proper nouns acquire Spanish phonology; split clips change room tone or energy. Repair by extending contextual text, selecting a genuinely bilingual voice, or using a separately cast and disclosed speaker when identity continuity is less important than native delivery.

## Post-production

1. Keep an untouched source render and a reversible edit session.
2. Remove leading/trailing dead air, accidental breaths, spoken direction text, clicks, and failed takes without cutting plosives or word tails.
3. Repair locally. Regenerate the smallest coherent phrase, with surrounding context, rather than rerendering an approved chapter.
4. Use gentle crossfades at zero crossings where needed; never hide a mismatched performance under a long crossfade.
5. Apply corrective EQ/de-essing only when the problem is consistent. A defective voice/render is better repaired upstream than heavily processed.
6. Apply compression conservatively; preserve speech dynamics appropriate to the role.
7. Measure loudness and true peak with an ITU-R BS.1770-compatible meter. Match the destination specification, not an internet “universal LUFS” number.
8. **Standard:** EBU R 128 specifies −23 LUFS programme loudness for its broadcast context and uses Loudness Range and Maximum True Peak descriptors. Use it only when that delivery context applies.
9. Export a high-quality master and derive delivery encodes from it. Recheck captions and sync after the final audio render.

## Listening and QA gate

Automated checks catch defects; listeners decide whether the voice communicates.

### Technical checks

- file decodes; duration is plausible; expected sample rate/channels/codec are present;
- no clipping, truncation, duplicated audio, long unintended silence, or corrupt boundary;
- measured loudness/true peak meet the destination spec;
- requested words are present in order;
- timestamps remain aligned after edits;
- manifest records text hash, voice/model/settings, dictionary version, output format, request IDs, and edit version.

### Linguistic checks

- exact words, names, acronyms, numbers, currencies, dates, and URLs;
- correct target language, dialect, accent, stress, and code-switch boundary;
- no inserted, omitted, repeated, or hallucinated speech;
- caption text reflects intended display text while spoken expansions remain traceable.

### Performance checks

- role and emotion are credible;
- emphasis serves meaning;
- pace, pause, breath, and sentence endings feel human;
- identity and energy remain consistent across chunks;
- no synthetic warble, buzzy harmonics, phasing, metallic tails, mouth noise, excessive sibilance, or unstable pitch;
- no seam is audible in room tone, cadence, loudness, or timbre.

### Evaluation protocol

**Standard:** use ITU-T P.800-style controlled listening or ITU-T P.808 guidance for crowdsourced listening when running formal tests. Keep test conditions and instructions consistent; randomize and blind samples where practical.

**Production heuristic:** have at least one target-language native listener and one production listener rate:

1. naturalness;
2. intelligibility;
3. pronunciation accuracy;
4. role/affect fit;
5. identity consistency;
6. absence of artifacts;
7. overall acceptability.

Use a 1–5 scale with written defect timecodes. Compare against the prior approved take and, where licensed, a human reference. Do not average away a critical mispronunciation or rights failure.

An ASR transcript or word-error comparison may flag omissions and substitutions, but it cannot judge acting, accent appropriateness, prosody, or subtle artifacts.

## Failure recovery

Diagnose before changing parameters:

| Failure | First checks | Repair order |
|---|---|---|
| Wrong word/number | spoken-text normalization, locale, dictionary support/version | rewrite → alias/IPA/phoneme if supported → alternate native voice/model |
| Flat delivery | cast, source performance, stability too high, weak text cues | improve cast/text → lower stability cautiously → v3 with suitable tags |
| Overacting/hallucinated sounds | v3 tags, Creative behavior, stability too low, mismatched voice | remove tags → use Natural/Robust behavior → select calmer voice/model |
| Identity drift | chunk length, voice quality, similarity, model/settings changes | restore fixed manifest → add context/stitching → raise consistency cautiously → recast |
| Audible seams | arbitrary splits, missing context, loudness/room mismatch | split at clauses → previous/next context or request IDs → local edit/crossfade |
| Numeric errors on Flash | unnormalized text, normalization policy | deterministic spoken expansion → enable supported normalization → Multilingual v2 |
| High latency | measured TTFA components, model, protocol, buffer, voice type, geography | HTTP stream known text → WebSocket incremental text → Flash/voice/buffer tuning |
| `429` | rate vs concurrency code and response headers | reduce/queue concurrency → exponential backoff with jitter |
| `4xx` payload/auth | model access, voice access, key, limit, format | fix request; do not blind-retry |
| Persistent `5xx` | provider status, request ID, minimal reproduction | bounded retry with backoff → preserve failure metadata → escalate |

Change one variable per diagnostic render. Preserve the failed audio and its manifest so the lesson is reproducible.

## Rights, consent, safety, and privacy gate

Before cloning or deploying any recognizable voice:

1. obtain explicit, documented authorization covering creation, intended uses, territories, duration, distribution, edits, model/voice sharing, and revocation/notice expectations;
2. verify the speaker's identity and authority; do not treat public audio as permission;
3. prohibit unauthorized, deceptive, or harmful impersonation and do not evade voice verification;
4. never impersonate political candidates or elected officials; current policy prohibits it even with authorization in election contexts;
5. disclose synthetic/AI interaction where required. **Documented:** organizations using ElevenLabs to power AI agents must clearly and prominently tell users they are interacting with AI;
6. preserve a consent ledger tied to voice ID and uses; stop new generations when consent or voice access expires;
7. review the current Terms, Prohibited Use Policy, Privacy Policy, Voice Library Addendum, and applicable law before release;
8. confirm commercial rights for the actual plan and feature. **Documented, verified 2026-07-09:** free-plan output is non-commercial and requires attribution when published; paid-plan output can be commercial subject to rights, terms, policy, and non-Beta status; Beta output is not for commercial or production use;
9. apply the current regional content terms before uploading confidential scripts or voice data. **Documented, non-EEA Terms verified 2026-07-09:** the published terms grant ElevenLabs a perpetual, irrevocable, worldwide, sublicensable license to Content and User Voice Models for service provision, improvement, and product development. Account settings can opt out of future Content use for training, but do not undo prior uses. Other regions may have different terms; verify the agreement governing the account;
10. protect scripts and voice data. **Documented:** API `enable_logging=false` activates Zero Retention Mode only for eligible Enterprise customers and disables history-dependent features such as request stitching. Default processing otherwise follows the applicable Privacy Policy and terms. Decide explicitly whether confidentiality or history-dependent continuity wins;
11. do not advertise detection as proof of authenticity. ElevenLabs' signed-in Audio Detector checks SynthID where present and falls back to a statistical classifier; coverage is not universal, and modified audio may evade statistical detection.

When a rights or safety gate fails, stop. A technically excellent render is not releasable without authorization.

## Source map

All volatile ElevenLabs sources below were checked **2026-07-09**.

### Official ElevenLabs documentation and references

- [Models and current model IDs, languages, limits, deprecations, and concurrency](https://elevenlabs.io/docs/overview/models)
- [Create speech API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
- [Stream speech API](https://elevenlabs.io/docs/api-reference/text-to-speech/stream)
- [Stream speech with timing API](https://elevenlabs.io/docs/api-reference/text-to-speech/stream-with-timestamps)
- [TTS best practices: pauses, pronunciation, normalization, and v3 prompting](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [Default voice settings reference](https://elevenlabs.io/docs/api-reference/voices/settings/get-default/)
- [Pronunciation dictionaries guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries)
- [Request stitching guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching)
- [Understanding audio streaming](https://elevenlabs.io/docs/eleven-api/concepts/audio-streaming)
- [Realtime TTS WebSocket guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/websockets/realtime-tts)
- [API errors](https://elevenlabs.io/docs/eleven-api/resources/errors)
- [Text to Speech product guide](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech)
- [Voice Library](https://elevenlabs.io/docs/eleven-creative/voices/voice-library)
- [Voice Design](https://elevenlabs.io/docs/eleven-creative/voices/voice-design/)
- [Instant Voice Cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning)
- [Professional Voice Cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning)
- [ElevenCreative Studio](https://elevenlabs.io/docs/eleven-creative/products/studio)
- [Zero Retention Mode](https://elevenlabs.io/docs/eleven-api/resources/zero-retention-mode)
- [Audio Detector](https://elevenlabs.io/docs/eleven-creative/audio-tools/audio-detector)
- [Prohibited Use Policy](https://elevenlabs.io/use-policy)
- [Terms of Service for non-EEA regions](https://elevenlabs.io/terms-of-use)
- [Terms of Service for EEA, Switzerland, and UK; use the linked regional terms where applicable](https://elevenlabs.io/terms-of-use-eu)
- [Commercial-use help article](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform)
- [Voice Library Addendum](https://elevenlabs.io/vla)

### Speech and audio standards

- [ITU-T P.800: methods for subjective determination of transmission quality](https://www.itu.int/rec/t-rec-p.800)
- [ITU-T P.808: crowdsourced subjective speech-quality evaluation](https://www.itu.int/rec/T-REC-P.808-202106-I/en)
- [ITU-R BS.1770: programme loudness and true-peak measurement algorithms](https://www.itu.int/rec/R-REC-BS.1770)
- [EBU R 128: broadcast loudness normalization](https://tech.ebu.ch/publications/r128)
