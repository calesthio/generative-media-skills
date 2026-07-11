---
name: amazon-polly
description: "Use Amazon Polly for production text-to-speech work: selecting Standard, Neural, Long-form, or Generative engines and compatible voices; authoring SSML; creating speech marks for captions, word highlighting, or lip-sync; managing pronunciation lexicons; running synchronous, streaming, or asynchronous S3-backed synthesis; planning quotas, pricing, IAM, privacy, and QA for narration, audiobooks, accessibility audio, avatars, and multilingual media."
---

# Amazon Polly production TTS

Use Amazon Polly when the job needs AWS-hosted text-to-speech with predictable API operations, IAM governance, lexicons, SSML, and reusable generated audio. Treat Polly as a production TTS service, not a voice-cloning system: it provides AWS-managed voices and engines, not custom voice training or arbitrary speaker imitation.

Facts below were verified from official AWS documentation on 2026-07-10. Re-check AWS docs before relying on volatile facts such as prices, quotas, regions, voice lists, or engine feature compatibility.

## First decision: which operation and engine

Choose the operation first, because it defines latency, output custody, and timing options:

- `SynthesizeSpeech`: real-time request/response. Use for short narration lines, UI prompts, voice preview, batch segment synthesis, and speech-mark JSON. Input limit is 6,000 total characters, with no more than 3,000 billed characters; output audio is cut off after 10 minutes. Documented fact: https://docs.aws.amazon.com/polly/latest/dg/limits.html
- `StartSpeechSynthesisTask`: asynchronous synthesis to Amazon S3, optionally with SNS notification. Use for long articles, audiobook chapters, training modules, and server workflows that should not hold an HTTP audio stream open. Input limit is 200,000 total characters, with no more than 100,000 billed characters. Documented fact: https://docs.aws.amazon.com/polly/latest/APIReference/API_StartSpeechSynthesisTask.html
- `StartSpeechSynthesisStream`: bidirectional streaming input/output over HTTP/2. Use only when the application needs streamed generative audio while text is still arriving. Documented fact: AWS currently documents this operation as supporting only the `generative` engine and not JSON speech marks. Source: https://docs.aws.amazon.com/polly/latest/APIReference/API_StartSpeechSynthesisStream.html

Then select the engine:

- `standard`: broadest compatibility, lowest listed commercial price, strong for utility prompts, IVR, high-volume notification audio, and workflows where cost/coverage matter more than expressiveness. AWS describes Standard voices as concatenative synthesis.
- `neural`: better naturalness than standard, with all speech marks, many SSML tags, asynchronous synthesis, and selected Newscaster speaking style support. Good default for produced narration when speech marks or SSML control matter.
- `long-form`: designed for longer narrative content such as articles, training, and marketing videos. AWS documents only six long-form voices as of 2026-07-10: en-US Danielle, Gregory, Ruth, Patrick and es-ES Alba, Raúl; region availability is US East (N. Virginia) only. Use when long-duration delivery quality matters and the voice/language constraints fit.
- `generative`: most conversational and adaptive Polly family, with streaming support and higher humanlike variability. Use for conversational assistant lines, virtual trainers, and ad-like reads when its feature constraints fit. Important documented boundaries: speech marks are not currently available; Newscaster style is not supported; AWS warns the model can vary after updates and includes a hallucination/emergency-stop safety mechanism that reduces but does not eliminate risk of inappropriate or truncated output. Source: https://docs.aws.amazon.com/polly/latest/dg/generative-voices.html

Do not omit `Engine` in production. Some SDK/CLI paths default to `standard`; if the selected voice does not support Standard, the request can fail. Verify voice-engine-region compatibility with `DescribeVoices` or the current AWS voice pages before committing to a production voice.

## Capability boundaries that affect media production

Documented facts:

- Polly supports four voice engines: Generative, Long-form, Neural, and Standard. Source: https://docs.aws.amazon.com/polly/latest/dg/voice-engines-polly.html
- `SynthesizeSpeech` output formats include `mp3`, `ogg_vorbis`, `ogg_opus`, `pcm`, `mulaw`, `alaw`, and `json`; JSON is for speech marks. For `SynthesizeSpeech`, MP3/OGG Vorbis sample rates include 8000, 16000, 22050, 24000, 44100, and 48000 Hz; defaults are 22050 Hz for Standard and 24000 Hz for Neural, Long-form, and Generative. PCM is mono signed 16-bit little-endian with 8000 or 16000 Hz. Source: https://docs.aws.amazon.com/polly/latest/APIReference/API_SynthesizeSpeech.html
- `StartSpeechSynthesisTask` requires an output S3 bucket and can return task metadata including task ID, status, output URI, request characters, output format, sample rate, and SNS topic ARN. Source: https://docs.aws.amazon.com/polly/latest/APIReference/API_StartSpeechSynthesisTask.html
- Speech marks are line-delimited JSON records with millisecond `time`, `type` (`sentence`, `word`, `viseme`, or `ssml`), byte offsets for word/sentence marks, and a value. Source: https://docs.aws.amazon.com/polly/latest/dg/output.html
- Neural and Long-form voices support all speech marks; Generative voices currently do not support speech marks. Sources: https://docs.aws.amazon.com/polly/latest/dg/neural-voices.html, https://docs.aws.amazon.com/polly/latest/dg/long-form-voices.html, https://docs.aws.amazon.com/polly/latest/dg/generative-voices.html
- Pronunciation lexicons are stored per AWS Region, are W3C PLS-compliant, and apply only when the lexicon language matches the voice language. Up to five lexicons can be specified in a synthesis request. Sources: https://docs.aws.amazon.com/polly/latest/dg/managing-lexicons.html, https://docs.aws.amazon.com/polly/latest/APIReference/API_SynthesizeSpeech.html
- Quotas as of 2026-07-10 include: `SynthesizeSpeech` 80 TPS for Standard, 8 TPS for Neural, 8 TPS for Long-form, 8 TPS for Generative; `StartSpeechSynthesisTask` 10 TPS for Standard/Neural, 1 TPS for Long-form/Generative; lexicon management 5 TPS combined; 100 lexicons per account per Region; single lexicon size 40,000 characters. Source: https://docs.aws.amazon.com/polly/latest/dg/limits.html
- Commercial pricing as of 2026-07-10 is listed by AWS as $4.00 per 1M characters for Standard, $16.00 for Neural, $100.00 for Long-form, and $30.00 for Generative, outside free tier; speech marks are billed as processed characters for Standard/Neural/Long-form, while AWS’s pricing page lists Generative pricing for speech requests. Source: https://aws.amazon.com/polly/pricing/
- AWS says generated audio can be cached and replayed at no additional Polly cost. Source: https://aws.amazon.com/polly/pricing/

Production heuristics:

- Prefer Neural for most edited video narration if you need word/viseme marks, stable segment regeneration, SSML control, and broad voice coverage.
- Prefer Long-form for long chapters only when the limited voice/language/region set fits; otherwise chunk Neural synthesis at sentence boundaries and assemble audio locally.
- Prefer Generative for conversational realism, but add a QA pass that listens for inserted, truncated, or unexpected speech; do not use Generative when exact speech-mark timing is mandatory unless you can obtain timing through separate ASR after synthesis.
- Use Standard for high-volume utility audio, telephony where 8 kHz or μ-law/a-law matters, or when budget and high throughput dominate.

## SSML and pronunciation control

Use SSML when the script needs deterministic pauses, dates, acronyms, foreign-language spans, pronunciation fixes, or structural marks. Set `TextType="ssml"` and wrap the payload in `<speak>...</speak>`.

Documented facts:

- Standard voices support all Polly SSML tags except `<amazon:domain name="news">`; Neural, Long-form, and Generative support many but not all tags. Unsupported tags can return errors. Source: https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html
- `<break>` is fully available for Neural, Long-form, and Generative; individual `<break>` elements have a maximum duration of 10 seconds. Source: https://docs.aws.amazon.com/polly/latest/dg/limits.html
- `<emphasis>` is not available for Neural, Long-form, or Generative voices. Use wording, punctuation, `<break>`, or supported `<prosody>` controls instead. Source: https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html
- `<mark>` is fully available for Neural and Long-form and partially available for Generative, but Generative speech-mark output is not currently available; do not design a Generative workflow that depends on mark JSON. Sources: https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html, https://docs.aws.amazon.com/polly/latest/dg/generative-voices.html
- `<say-as>` is available for Long-form and Generative and partially available for Neural. For Neural, `say-as interpret-as="characters"` can cause the affected sentence to be synthesized with the corresponding Standard voice while still billed as Neural. Source: https://docs.aws.amazon.com/polly/latest/dg/say-as-tag.html
- In SSML, escape reserved XML characters such as `&`, `<`, and `>`. Source: https://docs.aws.amazon.com/polly/latest/dg/escapees.html

Production heuristics:

- Keep SSML minimal. Polly engines already infer prosody; too much markup creates robotic pacing and makes future voice swaps brittle.
- Use punctuation and sentence rewrites before extreme `<prosody rate>` or pitch controls.
- Place hard timing pauses only where the edit needs them. For natural narration, use sentence boundaries and commas rather than dense `<break>` tags.
- Store recurring brand/product pronunciations as lexicons, not inline `<phoneme>` tags in every script.
- For multilingual insertions, use a native voice for full-language content. Use `<lang>` only for short phrases or names, and expect accented pronunciation if the voice is not native to the language.

Example SSML for a product explainer:

```xml
<speak>
  <p>
    Meet <sub alias="Acme Cloud One">ACME C1</sub>.
    <break time="250ms"/>
    It turns noisy incident data into a ranked action plan.
  </p>
  <p>
    In <say-as interpret-as="date" format="mdy">07-10-2026</say-as> tests,
    teams cut triage time by <say-as interpret-as="cardinal">42</say-as> percent.
  </p>
  <p>
    <mark name="cta_start"/>Start with one service, then expand.
  </p>
</speak>
```

Why this structure works: `<sub>` avoids letter-by-letter acronym drift, `<break>` creates an edit point, `<say-as>` disambiguates data, and `<mark>` gives a deterministic cue for overlay timing when the chosen engine supports SSML speech marks.

## Speech marks for captions, highlighting, and lip sync

Use speech marks when the downstream artifact needs timing:

- `word`: karaoke captions, highlighted text, subtitle alignment, accessibility review.
- `sentence`: coarse captions or edit beats.
- `ssml`: cue points from `<mark name="..."/>` tags for visual overlays.
- `viseme`: mouth-shape timing for 2D/3D avatar rigs.

Documented facts:

- Speech mark output is JSON, not an audio stream. A speech mark object contains millisecond timing and either byte offsets/value for words and sentences, a viseme name, or an SSML mark value. Source: https://docs.aws.amazon.com/polly/latest/dg/output.html
- Speech marks are only available with `OutputFormat="json"`; requesting marks with another output format is an error. Source: https://docs.aws.amazon.com/polly/latest/APIReference/API_SynthesizeSpeech.html
- Speech mark metadata can differ by voice for the same text. Source: https://docs.aws.amazon.com/polly/latest/dg/output.html

Production workflow:

1. Finalize the narration text before generating timing.
2. Synthesize audio with the chosen engine, voice, text, text type, sample rate, and lexicons.
3. Make a second request with the exact same text, engine, voice, text type, and lexicons, but `OutputFormat="json"` and the needed `SpeechMarkTypes`.
4. Use the speech-mark JSON to build captions or mouth cues; do not edit the text afterward without regenerating both audio and marks.
5. Validate by playing the final mixed audio with overlays. Word marks are timing aids, not a substitute for human caption QA.

For lip sync, map Polly viseme names to the rig’s mouth-shape set and smooth transitions. Visemes are not phoneme-level ground truth; add blend windows and test plosives/fricatives visually.

If the selected voice/engine cannot provide speech marks, use a different compatible voice/engine or run forced alignment/ASR after synthesis. This is a production workaround, not an AWS-documented equivalence.

## Lexicons

Use lexicons for repeated pronunciation fixes: product names, acronyms, stylized spellings, names, jargon, and locale-specific terms.

Documented facts:

- Polly lexicons must conform to the W3C Pronunciation Lexicon Specification (PLS). Source: https://docs.aws.amazon.com/polly/latest/dg/managing-lexicons.html
- Lexicons are stored in a specific AWS Region and apply only when the lexicon language matches the selected voice language. Source: https://docs.aws.amazon.com/polly/latest/dg/managing-lexicons.html
- API constraints include up to 100 lexicons per account per Region, lexicon names up to 20 alphanumeric characters, each lexicon up to 40,000 characters, replacement values up to 100 characters, and up to five lexicons per synthesis request. Source: https://docs.aws.amazon.com/polly/latest/dg/limits.html
- Polly supports IPA and X-SAMPA pronunciations in lexicons. Source: https://docs.aws.amazon.com/polly/latest/dg/managing-lexicons-console-upload.html

Production heuristics:

- Keep a project lexicon and a brand lexicon separate so project overrides can be removed without affecting other productions.
- Test a lexicon with the exact voice and engine. Pronunciation fixes can affect cadence around the word.
- Avoid huge catch-all lexicons; they can add latency and make pronunciation debugging harder.
- If two lexicons could match the same grapheme, specify request order intentionally and document the expected override behavior for the production team.

Example PLS lexicon:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0"
  xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
  alphabet="ipa"
  xml:lang="en-US">
  <lexeme>
    <grapheme>ACME C1</grapheme>
    <alias>Acme Cloud One</alias>
  </lexeme>
  <lexeme>
    <grapheme>Qdrant</grapheme>
    <phoneme>ˈkjuː drænt</phoneme>
  </lexeme>
</lexicon>
```

## Output and mastering choices

For video editing, request a high enough sample rate to survive mixing and exports:

- Use MP3 for lightweight previews or web narration where lossy compression is acceptable.
- Use PCM when the audio will be heavily processed, normalized, or converted by a local mastering chain.
- Use OGG formats when the target runtime expects them.
- Use 24 kHz or higher for natural voice production if supported by the operation; normalize loudness in post rather than relying on TTS volume tags.
- For telephony, use the required narrowband format/rate such as 8 kHz μ-law/a-law or PCM, then test in the actual phone/audio path.

Production QA checklist:

- Listen to the full output, not just spot checks, for names, numbers, hallucinated words, clipped ends, unnatural breaths, and tonal mismatch.
- Compare the generated transcript or captions against the approved script.
- Verify the first and last 500 ms are not clipped after transcoding.
- Check target loudness and true peak after mixing with music/SFX.
- Re-render all segments for a voice/engine if AWS model updates or voice drift would make newly generated lines mismatch older lines. AWS specifically warns that Long-form and Generative technologies can vary after updates.
- For multi-segment edits, synthesize on sentence or paragraph boundaries and leave handles for crossfades.

## IAM, S3, custody, and privacy

Documented facts:

- Amazon Polly supports IAM identity-based policies, policy actions, policy resources, temporary credentials, and forward access sessions; it does not support resource-based policies, service-specific condition keys, ACLs, ABAC tags in policies, service roles, or service-linked roles. Source: https://docs.aws.amazon.com/polly/latest/dg/security_iam_service-with-iam.html
- Polly policy actions use the `polly:` prefix. Source: https://docs.aws.amazon.com/polly/latest/dg/security_iam_service-with-iam.html
- AWS recommends MFA, SSL/TLS, CloudTrail logging, AWS encryption solutions, and least-privilege IAM. Source: https://docs.aws.amazon.com/polly/latest/dg/data-protection.html
- AWS strongly recommends not putting sensitive identifying information into free-form fields because data entered into AWS services might be included in diagnostic logs. Source: https://docs.aws.amazon.com/polly/latest/dg/data-protection.html
- AWS says Amazon Polly does not retain the content of text submissions. Source: https://docs.aws.amazon.com/polly/latest/dg/security-best-practices.html
- `SynthesizeSpeech` is stateless and its output cannot be retrieved from Polly later; store/encrypt generated files in your own system or S3 if you need retention. Source: https://docs.aws.amazon.com/polly/latest/dg/encryption-at-rest.html
- Amazon Polly can be used with interface VPC endpoints powered by AWS PrivateLink for private connectivity from a VPC. Source: https://docs.aws.amazon.com/polly/latest/dg/using-polly-with-vpc-endpoints.html
- CloudTrail captures Polly API calls; CloudWatch Logs can monitor job status. Source: https://docs.aws.amazon.com/polly/latest/dg/sec-logging.html
- Third-party auditors assess Amazon Polly under AWS compliance programs including SOC, PCI, FedRAMP, and HIPAA; customer compliance responsibility depends on data sensitivity and applicable law. Source: https://docs.aws.amazon.com/polly/latest/dg/AMAZON-POLLY-compliance.html
- S3 encrypts new objects at rest by default with SSE-S3; use S3 bucket encryption settings or SSE-KMS when customer-managed key control is required. Source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html

Production security heuristics:

- Grant a synthesis worker only the needed Polly actions, the target S3 prefix for async output, optional SNS publish permission, CloudWatch/CloudTrail visibility as required, and KMS permissions only for the specific key if using SSE-KMS.
- Use separate S3 prefixes per project and environment (`tts/dev/...`, `tts/prod/...`) to simplify lifecycle policies and deletion.
- Do not submit secrets, account numbers, medical details, or personal identifiers unless the workflow has explicit privacy approval and retention controls.
- For regulated data, confirm that the chosen Region, S3 bucket, KMS key, logging, retention, and compliance program scope match the organization’s obligations; Polly’s compliance eligibility does not make the whole application compliant by itself.

## Rights, consent, and disclosure

Documented boundary: Polly provides AWS voices; it is not a custom voice clone service. Production policy still matters:

- Do not imply a real person spoke a line unless you have permission and the audience context makes that clear.
- Follow local synthetic-media disclosure laws, platform policies, ad rules, accessibility requirements, and client brand rules.
- Confirm rights to the text being synthesized. Polly output rights do not clear copyright in source scripts, books, articles, or translations.
- For public-facing characters, maintain a voice bible with engine, voice ID, region, sample rate, lexicons, pronunciation notes, and examples so future lines remain consistent.
- For children, health, finance, politics, or legal content, require script approval and human audio review before publication.

## Examples

### Example: short video narration with captions and mouth cues

Intent: produce a 30-second product narration with word captions and optional avatar mouth movement.

Decision:

- Engine: `neural`, because speech marks are supported and naturalness is stronger than Standard.
- Operation: `SynthesizeSpeech`, because each paragraph is short.
- Output: audio MP3 or PCM plus separate JSON speech marks.
- Timing marks: `word`, `sentence`, and `viseme`.

Python sketch:

```python
import boto3

polly = boto3.client("polly", region_name="us-east-1")

text = """<speak>
<p>Meet ACME Cloud One. <break time="200ms"/> It turns noisy incident data into a ranked action plan.</p>
<p><mark name="cta"/>Start with one service, then expand.</p>
</speak>"""

common = {
    "Engine": "neural",
    "VoiceId": "Joanna",
    "Text": text,
    "TextType": "ssml",
    "SampleRate": "24000",
    "LexiconNames": ["BrandLex"],
}

audio = polly.synthesize_speech(**common, OutputFormat="mp3")
with open("narration.mp3", "wb") as f:
    f.write(audio["AudioStream"].read())

marks = polly.synthesize_speech(
    **common,
    OutputFormat="json",
    SpeechMarkTypes=["word", "sentence", "viseme", "ssml"],
)
with open("narration.marks.jsonl", "wb") as f:
    f.write(marks["AudioStream"].read())
```

QA: check that `BrandLex` exists in `us-east-1`, that the voice language matches the lexicon language, and that generated captions match the approved script.

### Example: asynchronous chapter render to S3

Intent: convert a long training chapter into a single audio file without managing many short requests.

Decision:

- Operation: `StartSpeechSynthesisTask`, because the chapter exceeds real-time `SynthesizeSpeech` limits.
- Engine: `long-form` only if the voice/language/region requirements fit; otherwise use `neural` and segment locally.
- Custody: write to a project-specific S3 prefix with bucket encryption, lifecycle, and access policy already configured.

Python sketch:

```python
import boto3

polly = boto3.client("polly", region_name="us-east-1")

response = polly.start_speech_synthesis_task(
    Engine="long-form",
    VoiceId="Ruth",
    TextType="ssml",
    Text=open("chapter_01.ssml", encoding="utf-8").read(),
    OutputFormat="mp3",
    SampleRate="24000",
    OutputS3BucketName="company-media-prod",
    OutputS3KeyPrefix="tts/training-2026/chapter-01/",
    SnsTopicArn="arn:aws:sns:us-east-1:123456789012:polly-render-events",
)

print(response["SynthesisTask"]["TaskId"])
print(response["SynthesisTask"].get("OutputUri"))
```

QA: poll `GetSpeechSynthesisTask` or subscribe to SNS, verify the output file exists under the expected S3 prefix, listen end-to-end, and compare duration against the chapter estimate.

### Example: choosing against Generative for accessible captions

User asks: “Use the most human Amazon Polly voice and give me exact word-level captions.”

Strong production response: explain that Generative may sound most conversational but currently does not support speech-mark generation, so exact word-level captions require either a Neural/Long-form voice with Polly marks or a post-synthesis alignment workflow. Recommend Neural if captions are mandatory and the voice is acceptable; choose Generative only if the user accepts ASR/forced-alignment timing as an additional QA step.

## Troubleshooting

- `InvalidSsmlException`: validate XML, escape reserved characters, remove unsupported tags for the chosen engine, and simplify nested markup.
- `LexiconNotFoundException`: check Region, lexicon name spelling, request order, and whether the synthesis client is using the same Region where the lexicon was uploaded.
- `LanguageNotSupportedException` or voice/engine error: call `DescribeVoices` with the intended engine and Region; do not assume a voice supports every engine.
- `MarksNotSupportedForFormatException`: request marks with `OutputFormat="json"` only, and generate audio in a separate request.
- Throttling: respect per-engine TPS and concurrent request quotas, batch with backoff and jitter, and request quota increases when the traffic model requires them.
- Segment mismatch after pickups: regenerate the surrounding sentence or paragraph, not only the changed word, so cadence and room tone remain coherent.

## Official sources checked on 2026-07-10

- Amazon Polly voice engines: https://docs.aws.amazon.com/polly/latest/dg/voice-engines-polly.html
- Standard, Neural, Long-form, and Generative voice pages: https://docs.aws.amazon.com/polly/latest/dg/neural-voices.html, https://docs.aws.amazon.com/polly/latest/dg/long-form-voices.html, https://docs.aws.amazon.com/polly/latest/dg/generative-voices.html
- `SynthesizeSpeech`, `StartSpeechSynthesisTask`, and `StartSpeechSynthesisStream` API references: https://docs.aws.amazon.com/polly/latest/APIReference/API_SynthesizeSpeech.html, https://docs.aws.amazon.com/polly/latest/APIReference/API_StartSpeechSynthesisTask.html, https://docs.aws.amazon.com/polly/latest/APIReference/API_StartSpeechSynthesisStream.html
- SSML, speech marks, and lexicons: https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html, https://docs.aws.amazon.com/polly/latest/dg/output.html, https://docs.aws.amazon.com/polly/latest/dg/managing-lexicons.html
- Quotas, endpoints, and pricing: https://docs.aws.amazon.com/polly/latest/dg/limits.html, https://docs.aws.amazon.com/general/latest/gr/pol.html, https://aws.amazon.com/polly/pricing/
- Security, privacy, IAM, logging, VPC endpoints, compliance, and encryption: https://docs.aws.amazon.com/polly/latest/dg/data-protection.html, https://docs.aws.amazon.com/polly/latest/dg/security_iam_service-with-iam.html, https://docs.aws.amazon.com/polly/latest/dg/security-best-practices.html, https://docs.aws.amazon.com/polly/latest/dg/sec-logging.html, https://docs.aws.amazon.com/polly/latest/dg/using-polly-with-vpc-endpoints.html, https://docs.aws.amazon.com/polly/latest/dg/AMAZON-POLLY-compliance.html, https://docs.aws.amazon.com/polly/latest/dg/encryption-at-rest.html
