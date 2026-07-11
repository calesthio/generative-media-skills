---
name: azure-speech
description: "Use Microsoft Azure Speech in Foundry Tools for media-production speech workflows: speech-to-text, fast and batch transcription, diarization, captions/subtitles, real-time transcription, text-to-speech neural and HD voices, SSML, custom/personal voices, text-to-speech avatars, speech/video translation, localization, quotas, regions, privacy, consent, rights, and production QA."
---

# Azure Speech for media production agents

Use this skill when Azure Speech in Foundry Tools is a candidate provider for transcription, captions, subtitles, narration, synthetic voices, avatar speech, speech translation, video localization, or production speech QA.

Treat Azure Speech as a family of related services, not one model. Select the narrowest official capability that matches the job, then verify region, quota, language, pricing, and access status before committing.

Facts below were verified against Microsoft/Azure documentation on 2026-07-10. Volatile items such as supported locales, regions, pricing, quota values, API versions, and preview/limited-access status must be rechecked before paid or production use.

## First decision: what job is the user actually asking for?

Documented facts:

- Azure Speech exposes speech to text, text to speech, speech translation, custom speech, custom voice, personal voice, text-to-speech avatar, video translation, LLM Speech, Speech SDK, Speech CLI, REST APIs, and containers in different combinations by region and access tier. Sources: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/overview and https://learn.microsoft.com/en-us/azure/ai-services/speech-service/regions
- Speech-to-text modes include real-time transcription, fast transcription, batch transcription, and custom speech. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text
- Text-to-speech modes include real-time synthesis, asynchronous batch synthesis for long-form audio, standard/prebuilt neural voices, HD voices, custom voice, personal voice, and avatar outputs. Sources: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech and https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-synthesis

Production routing:

1. Live captions, live dictation, live customer-support assist, or interactive voice UI → real-time speech to text through Speech SDK, Speech CLI, or real-time REST where supported.
2. One prerecorded file where the editor needs quick transcript/subtitle timing → fast transcription API, if the file and region fit.
3. Many prerecorded files, long back catalog, storage-based processing, diarization at scale, or custom speech model use → batch transcription.
4. Narration, voiceover, accessibility read-aloud, or generated dialogue → text to speech with a selected standard/HD/custom/personal voice and SSML.
5. Audiobook, long lesson, long article, or thousands of narration segments → batch synthesis; do not force real-time synthesis for long-form work.
6. Source speech in one language with output text or spoken translation → speech translation or LLM Speech depending on latency, prompt-tuning, and output needs.
7. Existing video localization with translated video output → video translation.
8. Talking avatar driven by Azure Speech voice output → text-to-speech avatar. Use only when the avatar itself is part of the deliverable; otherwise generate audio and composite separately.
9. Domain jargon or acoustic mismatch causing transcription errors → phrase list/custom speech evaluation, then custom speech training if the measured gain justifies it.

Do not represent diarization as speaker identity. Azure Speech diarization labels speakers such as Guest1/Guest2 and is not designed to identify individuals. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/speech-to-text/transparency-note

## Speech to text for captions, transcripts, and editorial logging

### Real-time transcription

Use real-time transcription when the user needs immediate partial/final results for live captions, live notes, dictation, or a responsive voice application.

Documented facts:

- Real-time speech to text can produce intermediate results for live audio inputs and is available through Speech SDK, Speech CLI, and short-audio REST paths. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text
- Real-time diarization is available through the real-time diarization workflow, but the short-audio REST API does not support real-time diarization. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-stt-diarization
- Real-time diarization had a documented Standard (S0) maximum audio length of 240 minutes per session on 2026-07-10. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-services-quotas-and-limits

Production heuristics:

- For live captions, optimize for latency and readability first; preserve a post-event correction pass for names, jargon, and sentence breaks.
- Ask whether captions are for accessibility, live monitoring, edit prep, or legal/archive transcript. These require different tolerances.
- For action-triggering voice interfaces, show or play back recognized text and ask for confirmation before irreversible actions.

### Fast transcription

Use fast transcription when the user needs a synchronous transcript for one audio/video file with predictable latency, for example quick subtitles, edit prep, meeting notes, or voicemail.

Documented facts:

- Fast transcription returns results synchronously and is designed to be faster than real time. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/fast-transcription-create
- It returns display-form transcription, not lexical form. Display form includes human-readable punctuation and capitalization. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/fast-transcription-create
- As of 2026-07-10, fast transcription documented support included transcription, diarization, one/two-channel handling, profanity filtering, locale specification, phrase lists for the default mode, segment-level timestamps, and word-level timestamps; LLM Speech variants changed the feature matrix. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/fast-transcription-create
- Fast transcription had documented Standard (S0) limits of audio input size under 500 MB, audio length under 5 hours per file, and 600 requests per minute on 2026-07-10. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-services-quotas-and-limits

Production heuristics:

- Prefer fast transcription for a single urgent editorial job; prefer batch for a library, queue, or repeatable pipeline.
- Specify the known locale when possible to improve accuracy and latency. Use language identification only when genuinely unknown or multilingual.
- For subtitles, request word/segment timing, then run a subtitle segmentation pass; raw transcript timing is not automatically broadcast-ready line breaking.

### Batch transcription

Use batch transcription when the user has many prerecorded files, long material, storage-based ingest, asynchronous processing, diarization, word-level timestamps, or a custom speech model.

Documented facts:

- Batch transcription submits audio, processes asynchronously, and stores results in a storage container for retrieval. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription
- Batch is designed for large amounts of audio in storage; provide multiple files per request or point to an Azure Blob Storage container for concurrent processing. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription
- Batch jobs are best-effort scheduled; Microsoft documents that at peak hours jobs might take up to 30 minutes to start and up to 24 hours to complete. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription-get
- On 2026-07-10, batch transcription documented limits included REST API 600 requests/minute, up to 1 GB audio input file size, up to 1,000 files per transcription request when using multiple content URLs, and 240 minutes per file when diarization is enabled. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-services-quotas-and-limits
- Custom speech models can be used with batch transcription without deploying a hosted custom endpoint if only batch transcription is needed. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-speech-overview

Production heuristics:

- Build the batch job around storage provenance: source URI/SAS, locale, model, diarization, word timestamps, profanity policy, TTL, output storage, and a retry plan.
- For archive media, separate ingest metadata from transcript text: file ID, show/episode, rights owner, input language, expected speakers, and noise notes.
- Poll asynchronously with exponential backoff and make the UI truthful: “queued/running/succeeded/failed,” not a fake progress bar.

### Diarization and speaker separation

Documented facts:

- Diarization differentiates speakers and adds speaker information to transcribed segments. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-stt-diarization
- The Speech transparency note says diarization is not speaker recognition and cannot be used to identify individuals; guest labels are random per conversation. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/speech-to-text/transparency-note
- In data-processing documentation, speaker separation/diarization uses voice-characteristic signals temporarily for annotating output; signal data is discarded after processing and does not support tracking speakers across multiple files. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/speech-to-text/data-privacy-security

Production heuristics:

- If the user needs “Alice vs Bob,” diarization alone is insufficient. Use it as a draft segmentation aid, then map labels to names manually or through a supervised editorial process.
- Diarization is most useful when speakers are acoustically separable. It degrades with overlap, heavy noise, distant mics, and many speakers.
- Keep separate QA tracks for word accuracy and speaker-turn accuracy; a transcript can be textually accurate while assigning words to the wrong speaker.

### Captions and subtitles

Documented facts:

- Microsoft positions fast transcription for quick audio/video transcription, subtitles, and edit workflows. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/fast-transcription-create
- Azure Speech and Whisper-via-Azure-Speech are recommended by Microsoft for large-file batch transcription, diarization, and word-level timestamps, while Azure OpenAI Whisper is positioned for individual fast files and prompting/translation-to-English use cases. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/whisper-overview

Production heuristics:

- Generate captions in two passes: transcription/timing first, caption formatting second.
- Caption QA should check line length, reading speed, shot-change collisions, punctuation, speaker labels, music/SFX cues where required, profanity policy, and burned-in vs sidecar deliverables.
- For professional subtitles, do not trust raw punctuation blindly; edit sentence boundaries around meaning and cadence.
- If legal compliance matters, ask the user for the target standard, platform, or region rather than assuming an accessibility spec.

## Text to speech for narration and synthetic voices

### Voice selection

Documented facts:

- Standard/prebuilt neural voices are available out of the box; the supported voice list varies by language, region, endpoint, and feature. Sources: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech and https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support
- Azure Speech HD voices include DragonHD and DragonHDOmni families; the HD voice page documents different voice counts and feature positioning that can change over time. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/high-definition-voices
- Some voices do not support all SSML tags, including HD voices, personal voices, and embedded voices. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech

Production heuristics:

- Choose a voice by role and medium: authoritative explainer, warm tutorial, crisp product demo, accessible read-aloud, character dialogue, or localized dub.
- Always test the exact target locale, region, voice, output format, and SSML tags. “Supports TTS” does not mean “supports this style tag.”
- For brand work, make a voice shortlist and render the same 20–30 second audition script for each candidate.
- For multilingual narration, test native pronunciation in every target language. Cross-lingual timbre preservation does not guarantee native-sounding delivery for every script.

### SSML as the production control surface

Documented facts:

- SSML can control pitch, pronunciation, speaking rate, volume, structure, pauses, silence, voice/language/name/style/role, multiple voices, emphasis, prerecorded audio insertion, phonemes, and custom lexicons. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup
- Azure bills converted characters including punctuation; some SSML control elements such as phonemes and pitch count as billable characters even though the SSML document itself is not billable. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup
- Custom voice pronunciation cannot be customized through professional voice fine-tuning itself; use SSML for pronunciation control. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/faq-tts

Production heuristics:

- Use SSML surgically. Over-controlling prosody can sound less natural than using a strong voice with minimal pauses and pronunciation fixes.
- Put pronunciation fixes into reusable lexicons or phoneme tags for product names, acronyms, people, math, and brand terms.
- Mark breaths and pauses by editorial intention, not by punctuation alone.
- For multiple voices in one script, keep each turn in its own `voice` block and export stems separately when mixing with music/SFX.

### Batch synthesis for long audio

Documented facts:

- Batch synthesis is generally available and creates text-to-speech audio asynchronously for long and short text input, including content longer than 10 minutes. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-synthesis
- The retired Long Audio API is being replaced by batch synthesis; Microsoft documents Long Audio API retirement on 2027-04-01. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-synthesis
- Batch synthesis input can be plain text or SSML, with polling and download after success. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-synthesis

Production heuristics:

- Split long narration into semantically meaningful chapters or scenes even when batch synthesis can handle long input; this makes pickups, retakes, and mix changes cheaper.
- Keep a manifest mapping script IDs to output audio paths, voice names, SSML version, sample rate, and approval status.
- For audiobooks and courses, render a short proof chapter first and verify tone, pronunciation, loudness, chapter slates, and silence before batch-rendering all text.

### Custom voice, personal voice, and consent boundaries

Documented facts:

- Custom voice is a limited-access text-to-speech feature for creating a customized synthetic voice from human speech samples; access depends on eligibility and usage criteria. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-neural-voice
- Custom voice creation involves voice persona design, voice talent setup, consent statement, fine-tuning data, model training, testing, deployment, and use through REST API, Speech SDK, or Speech Studio. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-neural-voice
- Professional custom voice requires explicit voice-talent consent, and Microsoft documents contractual requirements around written permission, disclosure to the talent, and permission for Microsoft processing/retention needed for verification. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent
- Personal voice is limited access and requires registration/approval; it creates a voice from a short human voice sample and explicit consent. Sources: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-overview and https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-create-consent
- On 2026-07-10, the personal voice overview documented one minute of human speech, less than five seconds training time, restricted/approved use cases, and API access limited to eligible customers. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-overview
- Microsoft documents custom neural voice and custom text-to-speech avatar as Limited Access features intended to protect rights, foster transparent human-computer interaction, and counter harmful deepfakes/misleading content. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/limited-access

Production heuristics:

- Do not propose cloning a celebrity, employee, customer, deceased person, or “soundalike” unless the user provides rights, explicit consent, approved use case, and legal clearance.
- For brand voices, separate “voice design” from “voice cloning.” Often a standard neural/HD voice with SSML and casting direction is sufficient.
- Require a rights packet before production use: talent consent, scope of use, territories, channels, duration, revocation policy, synthetic disclosure plan, and approval contact.
- For personal voice, confirm that the use case is one of the approved/registered use cases and that the end user controls creation/use of their own voice.

## Speech translation, LLM Speech, and video localization

Documented facts:

- Speech translation supports real-time speech-to-text translation, speech-to-speech translation, multilingual speech translation, Live Interpreter, and multiple target languages with pricing implications. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-translation
- LLM Speech supports transcription and translation with LLM-enhanced mode, prompt tuning, inline or public-URL audio, and Microsoft Entra ID authentication as the recommended keyless path. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/llm-speech
- Video translation translates and generates localized videos in multiple languages; Microsoft documents portal and REST workflows and target/source language tables. Sources: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/video-translation-overview and https://learn.microsoft.com/en-us/azure/ai-services/speech-service/video-translation-get-started
- The text-to-speech transparency note says video translation with prebuilt neural voices is available for all users and content can be edited with prebuilt neural voice or authorized personal voice. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/transparency-note

Production heuristics:

- Localization requires more than transcription: translate for meaning, adapt idioms, retime captions, pronounce names, match speaker tone, and QA lip/cadence if video is regenerated.
- For source videos, preserve a source transcript, translated script, edited approved script, synthesized audio, and final muxed video as separate artifacts.
- If the target is a dubbed marketing video, include native-speaker review before final delivery.
- For multilingual live scenarios, test network conditions and target-language latency; live interpreter quality is not the same risk profile as post-produced dubbing.

## Text-to-speech avatars

Documented facts:

- Text-to-speech avatar can synthesize a digital video of a photorealistic avatar speaking with a standard or custom voice, in batch or real-time modes. Sources: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar and https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/transparency-note
- Standard avatar language support follows text-to-speech language support. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar
- Custom video avatar requires video recordings and consent from avatar talent; custom photo avatar can be created from one photo. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar
- Custom avatar creation documentation requires consent under applicable laws, a recorded statement, and Microsoft verification of the talent. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/custom-avatar-create

Production heuristics:

- Use Azure avatars for presenter-led training, support, or localization when a synthetic presenter is acceptable. Do not use them to imply a real person said something they did not authorize.
- Ask whether the deliverable needs an avatar or only voiceover. Avatar video adds consent, rendering, uncanny-valley, disclosure, and review obligations.
- For custom avatar work, require the same rights packet as custom voice plus likeness rights and model-use restrictions.

## Regions, quota, pricing, and governance checks

Before accepting an Azure Speech plan, run these checks:

1. Region: verify that the chosen Azure Speech resource region supports the exact feature: fast transcription, batch synthesis, avatar, LLM Speech, Voice Live, personal voice, or video translation. Microsoft states that core features are broad but some features require specific regions. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/regions
2. Data residency: Azure Speech documentation states data is stored or processed only in the region where the Speech resource is created. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/regions
3. Language/voice: verify target locale and voice support for the exact feature. Language support varies by functionality. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support
4. Quotas: verify F0/S0 tier, concurrency, request rate, file size, duration, endpoint, dataset, avatar, LLM Speech, and batch limits. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-services-quotas-and-limits
5. Pricing: verify current region/currency pricing and billing units. Microsoft’s pricing page bills STT in audio time, TTS per character, avatar per second/minute depending on table section, custom training/hosting separately, and notes fast transcription requires REST API 2024-11-15 or later for fast transcription pricing. Source: https://azure.microsoft.com/en-us/pricing/details/speech/
6. Access: verify Limited Access approval for custom neural voice, personal voice, and custom avatar. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/limited-access
7. Authentication: prefer Microsoft Entra ID/keyless authentication for production where documented; protect API keys if used. Source: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/llm-speech
8. Retention: for batch transcription, set output storage and `timeToLive` intentionally. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/speech-to-text/data-privacy-security

Operational observations:

- Azure docs and branding changed from Azure AI Speech toward Azure Speech in Foundry Tools; user-facing portals, resource names, and older SDK examples may still use older terms. Treat the current Learn page as authoritative for the implementation path.
- Pricing pages can display placeholders or vary by region/currency/account. Never hardcode a dollar estimate into a user quote without checking the calculator or billing account.

## Privacy, safety, consent, and rights

Documented facts:

- Audio of humans speaking and related transcripts may be personal and/or sensitive data, and users are responsible for permissions, licenses, proprietary rights, and legal compliance. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/speech-to-text/data-privacy-security
- For real-time speech to text, Microsoft documents processing in server memory with no data stored at rest, and encrypted in-transit data. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/speech-to-text/data-privacy-security
- For batch transcription, customers control storage and retention for input/output when specifying storage; Microsoft storage outputs can be deleted by API or TTL. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/speech-to-text/data-privacy-security
- Microsoft’s transparency note says speech to text is not intended for covert audio surveillance or uses outside reasonable user expectations. Source: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/speech-to-text/transparency-note
- Custom neural voice and custom avatar require explicit talent consent and disclosure; deployment must disclose synthetic nature and support feedback/reporting channels as documented in limited-access obligations. Sources: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent and https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/limited-access

Production heuristics:

- Treat every voice and face as rights-bearing media, even when the user supplies it.
- For interviews, meetings, calls, or public-space recordings, ask for consent status and jurisdiction-sensitive constraints before transcription.
- For minors, medical, employment, legal, or financial contexts, escalate data handling and consent review; do not improvise policy.
- For synthetic narration, disclose synthetic voice when the audience could reasonably believe the voice is a real human performance or when required by platform, client, law, or Microsoft terms.
- Refuse or redirect requests to impersonate a real person, bypass consent, hide synthetic origin, evade detection/watermarking, or use diarization for identity.

## Production QA checklist

For transcription/captions:

- Verify source audio sample rate, channels, codec, duration, clipping, noise, reverb, overlap, and target locale.
- Confirm selected mode: real-time, fast, batch, LLM Speech, or custom speech.
- Check word accuracy with WER-style sampling against human reference for at least representative sections.
- Check token/caption readability: punctuation, casing, numerals, names, jargon, profanity policy, language switches, timestamps, and speaker labels.
- For diarization, review WDER-like speaker assignment errors separately from text errors.
- For batch, validate every file has a result or report error; do not silently drop failed files.

For TTS/narration:

- Audition exact voice, locale, output format, SSML tags, sample rate, and speaking style.
- Verify pronunciation of names, acronyms, product terms, math, URLs, currencies, dates, and multilingual passages.
- Check pacing against edit timeline; retime via SSML or edit script, not by post-stretching beyond transparent limits.
- Loudness-normalize and de-ess after synthesis when mixing with music/SFX.
- Keep approved script, SSML, voice, region, render date, and audio hash for reproducibility.

For localization/dubbing:

- Preserve source meaning, culturally adapt idioms, and validate with a native speaker.
- Check target-language expansion/contraction against scene timing.
- Verify subtitles and dub are consistent after edits.
- Review synthetic voice disclosure and rights for every locale.

## Example: fast subtitle draft for an urgent product demo

Example intent: Generate draft English subtitles for a 14-minute product walkthrough within an editing session.

Applicable Azure capability: Fast transcription API, if the resource region supports it and the file is under current limits.

Inputs and constraints:

- One `demo_walkthrough.mp4` exported from the edit system.
- Known language: `en-US`.
- Need display-form transcript, word timestamps, profanity masked, speaker diarization off unless two speakers are present.
- Output will be converted to SRT/VTT by the editing pipeline after transcription.

Workflow:

1. Verify region supports fast transcription and confirm current file-size/duration limits.
2. Upload inline if small; use public URL for long file.
3. Call fast transcription with known locale, word-level timestamps, and desired profanity policy.
4. Convert result to captions with editorial line breaking.
5. QA a beginning/middle/end sample against audio before burning in.

Expected result: A quickly returned human-readable transcript with timing data suitable for draft subtitles.

Failure modes:

- Unsupported region or API version.
- File exceeds fast transcription limits.
- Locale mismatch lowers accuracy.
- Raw caption lines are too long or badly segmented.
- Product names need phrase-list or SSML-like pronunciation handling in later TTS, not just transcript correction.

Variation: If there are 250 videos, switch to batch transcription and process from Blob Storage instead of calling fast transcription one file at a time.

## Example: batch transcription with diarization for a podcast archive

Example intent: Transcribe 600 podcast episodes for searchable show notes and speaker-labeled editorial review.

Applicable Azure capability: Batch transcription.

Inputs and constraints:

- Audio in Azure Blob Storage with SAS access.
- Known locale: `en-US`.
- Two to four recurring hosts plus guests, but no requirement to identify speakers automatically.
- Need word timestamps, speaker labels, output retention policy, and failure report.

Workflow:

1. Confirm batch transcription region, quotas, pricing, and storage permissions.
2. Submit batches by show/season, not all files in one fragile job.
3. Enable diarization and word-level timestamps.
4. Set output storage and `timeToLive`.
5. Poll job status; collect transcript and report artifacts.
6. Map Guest labels to real speaker names manually during editorial QA.
7. Sample WER and WDER-like errors by episode type: studio, remote, live, noisy.

Expected result: Asynchronous transcript files with text, timestamps, and guest speaker labels for each episode.

Failure modes:

- SAS URLs expire before processing.
- Peak service load delays start.
- Overlapped speech causes diarization errors.
- Guest labels do not remain consistent across episodes.
- Archive includes multilingual or music-heavy segments that need special handling.

Variation: If domain jargon creates repeated errors, use custom speech evaluation and train a custom model only after measuring baseline error patterns.

## Example: SSML narration for a polished explainer

Example intent: Generate a calm, premium 60-second narration for a SaaS launch video.

Applicable Azure capability: Real-time text to speech or batch synthesis depending on volume; standard neural or HD voice after audition.

Example SSML:

```xml
<speak version="1.0" xml:lang="en-US"
       xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts">
  <voice name="en-US-AvaMultilingualNeural">
    <prosody rate="-6%" pitch="-1st">
      Your team does not need another dashboard.
      <break time="350ms"/>
      It needs one place where risk, revenue, and work in progress finally agree.
    </prosody>
    <break time="500ms"/>
    <prosody rate="-3%">
      Meet Contoso Atlas: the operating layer for decisions that cannot wait.
    </prosody>
  </voice>
</speak>
```

Parameters:

- Voice: auditioned exact voice in target region.
- Output: 48 kHz WAV for post-production when available; otherwise highest practical PCM format before mix.
- Render: one file per scene or paragraph for easier retakes.

Why structured this way: moderate pauses and slower rate create edit points without over-stylizing the voice.

Expected result: Clean narration stem ready for loudness normalization and mix.

Failure modes:

- Selected voice does not support requested SSML style/control.
- Overuse of prosody creates robotic delivery.
- Brand/product pronunciation is wrong.
- Billing estimate misses SSML-controlled billable characters.

Variation: For a long training course, use batch synthesis and a manifest of chapter IDs rather than real-time calls.

## Example: custom voice request triage

Example user request: “Clone our CEO’s voice for all investor update videos.”

Correct approach:

1. Treat this as custom neural voice or personal voice only if official limited-access requirements, approved use case, and explicit consent are satisfied.
2. Ask for proof of authorization, talent consent, intended contexts, disclosure plan, usage term, channels, territories, and revocation policy.
3. If the user only needs a similar executive tone, recommend auditioning standard/HD voices instead of cloning.
4. If authorized, build a voice persona and test script before collecting training data.

Expected result: Either a compliant custom voice plan or a safer standard-voice casting plan.

Failure modes:

- Proceeding from a casual “the CEO said it’s fine” without written consent.
- Using a model to impersonate someone outside approved contexts.
- Failing to disclose synthetic voice.
- Assuming personal voice API access exists without approval.

Variation: For a presenter avatar, require likeness rights and avatar talent consent in addition to voice rights.

## Sources verified on 2026-07-10

- Azure Speech overview: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/overview
- Speech to text overview: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text
- Fast transcription: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/fast-transcription-create
- Batch transcription: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription
- Batch transcription results/latency notes: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription-get
- Real-time diarization: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-stt-diarization
- Custom speech: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-speech-overview
- Whisper via Azure Speech vs Azure OpenAI: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/whisper-overview
- Text to speech overview: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech
- SSML overview: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup
- Batch synthesis: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-synthesis
- Custom neural voice: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-neural-voice
- Personal voice overview: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-overview
- Personal voice consent: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-create-consent
- Text-to-speech avatar: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar
- Custom avatar creation: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech-avatar/custom-avatar-create
- Speech translation: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-translation
- LLM Speech: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/llm-speech
- Video translation overview: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/video-translation-overview
- Video translation getting started: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/video-translation-get-started
- Regions: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/regions
- Language and voice support: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support
- Quotas and limits: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-services-quotas-and-limits
- Pricing: https://azure.microsoft.com/en-us/pricing/details/speech/
- Speech-to-text transparency note: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/speech-to-text/transparency-note
- Speech-to-text data/privacy/security: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/speech-to-text/data-privacy-security
- Text-to-speech transparency note: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/transparency-note
- Text-to-speech limited access: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/limited-access
- Voice/avatar talent disclosure: https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent
