---
name: amazon-transcribe
description: "Use Amazon Transcribe for AWS-based speech-to-text production: batch S3 transcription, real-time streaming, captions/subtitles, diarization, channel identification, custom vocabularies, vocabulary filters, language identification, PII/PHI handling, toxicity detection, Call Analytics, Medical, and secure S3/IAM/KMS workflows."
---

# Amazon Transcribe

Use this skill when an agent needs to plan, run, review, or troubleshoot Amazon Transcribe as a speech-to-text provider inside an AWS-controlled workflow. Treat Amazon Transcribe as an AWS custody option first: it is strongest when the media already belongs in S3, the organization needs IAM/KMS/CloudTrail governance, captions must be generated from batch files, or real-time transcripts must flow through AWS streaming endpoints.

Do not use this skill as a generic "best transcription model" ranking. Compare accuracy, latency, cost, language coverage, and custody requirements against the actual job. For healthcare, call-center analytics, and sensitive audio, separate the general Transcribe path from the Medical and Call Analytics products before choosing.

Facts below were verified against AWS documentation on 2026-07-10 unless a line says otherwise.

## Choose the right Amazon Transcribe surface

Documented fact: Amazon Transcribe is an automatic speech recognition service that converts audio to text. It can be used through asynchronous batch jobs for media files or real-time streaming for live audio. Sources: [What is Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html), [Streaming audio](https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html), [StartTranscriptionJob API](https://docs.aws.amazon.com/transcribe/latest/APIReference/API_StartTranscriptionJob.html).

Use this decision map:

- Batch transcription: use for files in Amazon S3, offline transcripts, subtitles, captions, podcast/video backlogs, archives, QA review, and workflows that can wait for job completion. Batch requires the media file to be in S3 before `StartTranscriptionJob`.
- Streaming transcription: use for live captions, call assistants, meetings, voice input, or low-latency partial/final transcripts. Streaming uses bidirectional HTTP/2 or WebSockets and requires a language choice or language identification, media encoding, and sample rate. Source: [StartStreamTranscription API](https://docs.aws.amazon.com/transcribe/latest/APIReference/API_streaming_StartStreamTranscription.html).
- Call Analytics: use only when the media is a customer-agent or sales/support call and the desired output includes call-specific insights such as turn-based output, sentiment, interruptions, non-talk time, talk speed, categories, summaries, or action items. Do not use it as a generic captioning path. Sources: [Call Analytics](https://docs.aws.amazon.com/transcribe/latest/dg/call-analytics.html), [post-call output](https://docs.aws.amazon.com/transcribe/latest/dg/tca-output-batch.html).
- Medical: use only for medical-related speech such as clinician dictation, telemedicine, or clinician-patient conversations. Amazon Transcribe Medical is available for batch and streaming, is US English (`en-US`) only, and AWS says it is not a substitute for professional medical advice, diagnosis, or treatment; patient-care uses require trained human review. Source: [Amazon Transcribe Medical](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-medical.html).

Production heuristic: for edited media and caption deliverables, prefer batch unless the user explicitly needs live text. For two-person recordings with each speaker isolated on a channel, prefer channel identification over diarization. For unknown single-channel speakers, use diarization and plan a human speaker-name pass.

## Input and output contract

Documented facts:

- Batch input formats include AMR, FLAC, M4A, MP3, MP4, Ogg, WebM, and WAV; streaming formats include FLAC, Ogg Opus, and PCM encoding. AWS recommends lossless formats such as FLAC or WAV with PCM 16-bit encoding where possible. Source: [Data input and output](https://docs.aws.amazon.com/transcribe/latest/dg/how-input.html).
- Amazon Transcribe supports single-channel and dual-channel media. Media with more than two channels is not supported for standard Transcribe. Sources: [Data input and output](https://docs.aws.amazon.com/transcribe/latest/dg/how-input.html), [channel identification](https://docs.aws.amazon.com/transcribe/latest/dg/channel-id.html).
- Batch transcript output is JSON. The JSON includes a paragraph transcript and item-level data; at minimum, word items include start time, end time, and confidence score. Source: [Data input and output](https://docs.aws.amazon.com/transcribe/latest/dg/how-input.html).
- Batch video subtitle output supports WebVTT (`.vtt`) and SubRip (`.srt`). When subtitles are requested, AWS produces both the subtitle file(s) and the regular JSON transcript in the same destination. Source: [Creating video subtitles](https://docs.aws.amazon.com/transcribe/latest/dg/subtitles.html).

Production heuristic:

- Normalize production audio before upload: extract the final mix intended for captions, downmix only if you do not need channel identification, remove long silence where editorially safe, and keep a copy of the exact audio used to generate captions.
- Use the JSON transcript as the source of truth for QA and downstream alignment. Treat AWS-generated SRT/VTT as a starting point; review line breaks, reading speed, punctuation, brand terms, speaker changes, and shot-change collisions before delivery.
- For subtitle accessibility, plan a separate editorial pass for non-speech information such as `[music]`, `[laughter]`, or meaningful sound effects. Amazon Transcribe's transcript is speech-to-text, not a full human caption authoring system.

## Feature boundaries that matter in production

### Speaker labels versus channel identification

Documented facts:

- Speaker diarization partitions speakers and can label up to 30 unique speakers as `spk_0` through `spk_29`; it is available for batch and streaming. Source: [Partitioning speakers](https://docs.aws.amazon.com/transcribe/latest/dg/diarization.html).
- Channel identification transcribes two-channel audio separately and labels channels `ch_0` and `ch_1`; Amazon Transcribe does not support more than two channels. Source: [Transcribing multi-channel audio](https://docs.aws.amazon.com/transcribe/latest/dg/channel-id.html).

Production heuristic:

- Use channel identification for call-center stereo, interviewer/interviewee split tracks, or any file where each speaker side has a stable separate channel.
- Use diarization for one-channel meetings, panels, podcasts, or camera audio, but do not promise human names. Build a mapping pass: `spk_0 = host`, `spk_1 = guest`, and verify the mapping after speaker turns change.
- Do not enable both channel identification and diarization unless the current API documentation explicitly supports the exact combination for the chosen request type. If you need both "which channel?" and "which person?", create separated workflows or post-process manually.

### Custom vocabulary, custom language models, and vocabulary filters

Documented facts:

- Custom vocabularies improve recognition of specific words such as brand names, acronyms, proper nouns, and domain terms. They can be used with all supported languages, but only characters in the language's supported character set are allowed. Source: [Custom vocabularies](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html).
- AWS says table format is the preferred custom vocabulary format. Tables contain `Phrase`, `SoundsLike`, `IPA`, and `DisplayAs`; `Phrase` is required and must not contain spaces. Source: [Creating a custom vocabulary using a table](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary-create-table.html).
- Custom vocabulary filters modify exact word matches using a selected method and can be applied to batch and streaming requests. Source: [Vocabulary filtering](https://docs.aws.amazon.com/transcribe/latest/dg/vocabulary-filtering.html).
- When language identification is combined with custom vocabularies, custom language models, or vocabulary filters, `LanguageIdSettings` is required for each language; multi-language identification does not support custom language models. Source: [Batch language identification](https://docs.aws.amazon.com/transcribe/latest/dg/lang-id-batch.html).

Production heuristic:

- Use a custom vocabulary for "please recognize this correctly"; use a vocabulary filter for "mask, remove, or flag this exact word if it appears."
- For brand-safe captions, custom vocabulary and vocabulary filters solve different problems. A product name belongs in vocabulary; profanity or embargoed terms belong in a vocabulary filter.
- Build a vocabulary from the script, guest names, product names, acronyms, unusual spellings, and campaign terms before the first production job. Re-run a short representative audio sample to verify it helps rather than hurts.
- For multilingual or dialect-ambiguous media, constrain `LanguageOptions` when possible. AWS warns that mismatched language options can produce inaccurate transcripts, and dialect mismatch can prevent language-specific customizations from applying.

### Language identification

Documented facts:

- Batch supports automatic language identification and automatic multiple-language identification. Source: [Batch language identification](https://docs.aws.amazon.com/transcribe/latest/dg/lang-id-batch.html).
- Streaming supports automatic language identification through the console, HTTP/2, or WebSockets. Source: [Streaming language identification](https://docs.aws.amazon.com/transcribe/latest/dg/lang-id-stream.html).
- Supported languages and language-specific features vary; AWS tells users to verify that the feature they need is supported for the language before proceeding. Source: [Supported languages and language-specific features](https://docs.aws.amazon.com/transcribe/latest/dg/supported-languages.html).

Production heuristic:

- If the user knows the language, specify it. Use language identification when language is genuinely unknown or the workflow must accept multiple languages.
- For regulated redaction, do not rely on broad auto language detection unless the redaction feature supports every likely language. AWS documents that when language identification is combined with content redaction, only supported redaction languages are redacted and unsupported languages may not generate warnings or failures.

### PII, PHI, redaction, and toxicity

Documented facts:

- Streaming PII redaction replaces each identified PII instance with `[PII]`. Source: [PII redaction in real-time streams](https://docs.aws.amazon.com/transcribe/latest/dg/pii-redaction-stream.html).
- Batch language identification plus content redaction has a critical boundary: if the audio contains languages other than supported redaction languages, only supported-language content is redacted and other languages are not redacted without warnings or job failure. Source: [Batch language identification](https://docs.aws.amazon.com/transcribe/latest/dg/lang-id-batch.html).
- Toxicity Detection identifies and classifies voice-based toxic content across categories such as sexual harassment, hate speech, threat, abuse, profanity, insult, and graphic content; AWS says it uses audio and text cues. It is available only for batch transcriptions in US English (`en-US`). AWS's console workflow also notes that PII redaction can be enabled with Toxicity Detection, but other listed options are not supported with it. Sources: [Detecting toxic speech](https://docs.aws.amazon.com/transcribe/latest/dg/toxicity.html), [Using toxic speech detection](https://docs.aws.amazon.com/transcribe/latest/dg/toxicity-using.html).
- Amazon Transcribe Medical is HIPAA eligible according to AWS documentation, but Medical output intended for patient care must be reviewed by trained medical professionals. Sources: [Amazon Transcribe Medical](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-medical.html), [Amazon Transcribe FAQ](https://aws.amazon.com/transcribe/faqs/).

Production heuristic:

- Treat PII/PHI redaction as a safety assist, not a legal guarantee. For public release, legal discovery, medical records, HR, minors, law enforcement, or financial use, route output through a human privacy review.
- Never put sensitive data in job names, tags, free-form fields, or external URLs. AWS warns that those fields may appear in billing or diagnostic logs. Source: [Data protection](https://docs.aws.amazon.com/transcribe/latest/dg/data-protection.html).
- For toxicity detection, do not convert category confidence into a moderation decision without human policy review. Use it as a flagging layer and preserve context.

## AWS custody, security, and permissions

Documented facts:

- Batch jobs use S3 for input audio and output transcripts. If you specify your own output bucket, the transcript remains in that bucket until you remove it. Source: [Data input and output](https://docs.aws.amazon.com/transcribe/latest/dg/how-input.html).
- Amazon Transcribe supports encryption at rest with S3-managed keys or AWS KMS keys and uses TLS in transit. Source: [Data encryption](https://docs.aws.amazon.com/transcribe/latest/dg/data-encryption.html).
- AWS's shared responsibility model applies: AWS protects the infrastructure, and customers are responsible for content control, security configuration, and service management. AWS recommends least-privilege IAM, MFA, TLS, CloudTrail logging, encryption, and Macie for sensitive S3 data discovery. Source: [Data protection](https://docs.aws.amazon.com/transcribe/latest/dg/data-protection.html).
- By default, AWS documentation says Amazon Transcribe stores and uses processed voice inputs to develop and improve the service; customers can opt out through an AWS Organizations AI services opt-out policy. Source: [Opting out](https://docs.aws.amazon.com/transcribe/latest/dg/opt-out.html).
- IAM roles used by Amazon Transcribe need S3 access; if KMS is used, the relevant KMS key permissions are also required. AWS provides policies for S3 input `GetObject`/`ListBucket`, output `PutObject`, KMS permissions, and confused deputy prevention using `aws:SourceArn` and `aws:SourceAccount`. Source: [Identity-based policy examples](https://docs.aws.amazon.com/transcribe/latest/dg/security_iam_id-based-policy-examples.html).
- Amazon Transcribe supports identity-based policies, policy actions/resources/condition keys, temporary credentials, and service roles; it does not support resource-based policies, ACLs, or service-linked roles. Source: [How Amazon Transcribe works with IAM](https://docs.aws.amazon.com/transcribe/latest/dg/security_iam_service-with-iam.html).

Production checklist:

1. Confirm the AWS account, region, and data residency requirement before upload.
2. Use customer-owned S3 buckets for regulated or long-lived transcripts; avoid service-managed output when retention, lifecycle, or auditability matters.
3. Enable bucket encryption and choose SSE-KMS if the customer needs key-policy control or KMS audit trails.
4. Grant only the required actions: `transcribe:StartTranscriptionJob`, `transcribe:GetTranscriptionJob`, `transcribe:ListTranscriptionJobs` as needed, S3 read on the input prefix, S3 write on the output prefix, and KMS decrypt/encrypt/generate-data-key only when necessary.
5. Configure CloudTrail and lifecycle deletion for raw media, JSON, SRT/VTT, temporary derivatives, and redacted/unredacted variants.
6. If privacy policy requires no AI-service content improvement use, confirm the AWS Organizations opt-out policy before processing sensitive audio.

## Quotas, pricing, and regional availability

Volatile facts verified 2026-07-10:

- Standard Transcribe quotas include maximum audio file length of 28,800 seconds, maximum audio file size of 2 GB, minimum audio duration of 500 ms, two-channel channel identification, 25 concurrent standard streaming sessions, 250 concurrent standard transcription jobs, 100 total vocabularies, 100 vocabulary filters, and 90 days of job-record retention. Many quotas are adjustable; some are not. Source: [Amazon Transcribe endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/transcribe.html).
- Call Analytics batch quotas differ: 14,400 seconds maximum audio length and 500 MB maximum file size for Call Analytics batch jobs. Source: [Amazon Transcribe endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/transcribe.html).
- AWS pricing is region-specific and changes over time. The public pricing examples for US East (N. Virginia) showed standard streaming at `$0.01` per minute and batch at `$0.006` per minute, with separate pricing for Call Analytics, content redaction, Medical, and add-ons. Source: [Amazon Transcribe pricing](https://aws.amazon.com/transcribe/pricing/).
- Region availability varies by API and product. Always check the AWS General Reference and the product-specific region tables before committing a production region. Sources: [endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/transcribe.html), [Medical region availability](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-medical.html), [Call Analytics region availability](https://docs.aws.amazon.com/transcribe/latest/dg/call-analytics.html).

Production heuristic:

- Price by audio duration, not file size. Include re-runs in estimates: one sample pass, one final pass, and possible redaction/caption re-run.
- Before a large batch, query Service Quotas in the target region and design a queue with retry/backoff for throttling.
- For high-volume captions, pre-segment long videos at natural boundaries only if necessary for workflow control; avoid splitting in the middle of speech because it can harm punctuation and context.

## Example: batch caption job for an edited video

Example intent: create English captions and a JSON transcript for a final video already uploaded to S3. The job needs a custom vocabulary for product names, diarization is not needed, and output should land in a customer-owned S3 prefix.

```python
import time
import boto3

region = "us-west-2"
job_name = "launch-video-captions-20260710"
input_uri = "s3://example-prod-media/final/launch-video.wav"
output_bucket = "example-prod-transcripts"
output_key = "captions/launch-video/"

transcribe = boto3.client("transcribe", region_name=region)

transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={"MediaFileUri": input_uri},
    OutputBucketName=output_bucket,
    OutputKey=output_key,
    LanguageCode="en-US",
    Settings={
        "VocabularyName": "launch-product-terms-en-us"
    },
    Subtitles={
        "Formats": ["srt", "vtt"],
        "OutputStartIndex": 1
    },
    Tags=[
        {"Key": "project", "Value": "launch-video"},
        {"Key": "data-class", "Value": "public-after-review"}
    ],
)

while True:
    job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    status = job["TranscriptionJob"]["TranscriptionJobStatus"]
    if status in ("COMPLETED", "FAILED"):
        break
    time.sleep(15)

print(status)
print(job["TranscriptionJob"])
```

Why this structure:

- It uses batch because captions are an offline deliverable.
- It requests both SRT and VTT plus the full JSON transcript.
- It uses a custom vocabulary because brand/product spellings matter.
- It avoids diarization because speaker labels would add noise to normal captions unless the edit actually needs speaker attribution.

Review before delivery:

- Check product names against the script and vocabulary.
- Review punctuation, sentence segmentation, line breaks, reading speed, and sync at scene cuts.
- Add editorial non-speech captions manually if required by the target platform or accessibility standard.
- Verify output retention and deletion policy for both the S3 input audio and transcript outputs.

## Example: call-center stereo transcription choice

Example intent: transcribe recorded support calls where the agent is on the left channel and the customer is on the right channel. The product team wants text for search and QA, not sentiment or automatic call summaries.

Recommended approach:

1. Use standard batch Transcribe with `ChannelIdentification`, not Call Analytics.
2. Set `LanguageCode` if known; use language identification only if calls may arrive in multiple languages.
3. Use a vocabulary for product names and a vocabulary filter for terms that must be masked or flagged.
4. Keep channel labels in the transcript and map `ch_0`/`ch_1` to the recording system's channel convention.
5. Escalate to Call Analytics only if the user asks for call categories, sentiment, talk-time metrics, interruptions, or generative call summaries.

Reasoning:

- Channel identification is designed for two-channel audio and avoids guessing speaker turns.
- Call Analytics is more expensive and product-specific; using it for plain transcripts can add unnecessary cost and governance scope.

## Example: real-time stream constraints

Example intent: add live captions to an internal event.

Plan:

1. Use streaming Transcribe over HTTP/2 or WebSocket.
2. Feed real-time audio in a supported streaming format: FLAC, Ogg Opus, or PCM.
3. Provide the language code if known; otherwise use streaming language identification.
4. Use partial results for on-screen provisional captions and final results for logs.
5. If captions are published after the event, rerun the final recording through batch and edit the subtitles rather than relying only on live output.

Production heuristic: live captions optimize latency, not perfect editorial quality. For a public recording, batch-transcribe the final mixed audio afterward and perform a subtitle QA pass.

## Production QA rubric

Review every consequential transcript before release:

- Accuracy: sample at least the opening, dense terminology sections, names, numbers, acronyms, overlapping speech, and low-SNR sections.
- Timing: verify start/end times against the final media, not a draft export.
- Speaker handling: confirm whether `spk_*` or `ch_*` labels are meaningful to the end user; replace generic labels with names only after evidence.
- Captions: check line length, reading speed, segmentation, shot-change timing, missing non-speech audio, and platform format requirements.
- Redaction: compare unredacted and redacted outputs in a secure review environment; verify PII/PHI categories and unsupported-language risk.
- Custody: verify S3 bucket, prefix, encryption, KMS key, lifecycle, IAM role, CloudTrail, and AI services opt-out requirements.
- Cost: record region, duration, feature add-ons, re-run count, and whether Call Analytics/Medical pricing applies.

## Official sources

- [What is Amazon Transcribe](https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html)
- [StartTranscriptionJob API](https://docs.aws.amazon.com/transcribe/latest/APIReference/API_StartTranscriptionJob.html)
- [StartStreamTranscription API](https://docs.aws.amazon.com/transcribe/latest/APIReference/API_streaming_StartStreamTranscription.html)
- [Data input and output](https://docs.aws.amazon.com/transcribe/latest/dg/how-input.html)
- [Supported languages and language-specific features](https://docs.aws.amazon.com/transcribe/latest/dg/supported-languages.html)
- [Speaker diarization](https://docs.aws.amazon.com/transcribe/latest/dg/diarization.html)
- [Channel identification](https://docs.aws.amazon.com/transcribe/latest/dg/channel-id.html)
- [Video subtitles](https://docs.aws.amazon.com/transcribe/latest/dg/subtitles.html)
- [Custom vocabularies](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html)
- [Vocabulary filtering](https://docs.aws.amazon.com/transcribe/latest/dg/vocabulary-filtering.html)
- [Batch language identification](https://docs.aws.amazon.com/transcribe/latest/dg/lang-id-batch.html)
- [Streaming language identification](https://docs.aws.amazon.com/transcribe/latest/dg/lang-id-stream.html)
- [PII redaction in real-time streams](https://docs.aws.amazon.com/transcribe/latest/dg/pii-redaction-stream.html)
- [Toxicity detection](https://docs.aws.amazon.com/transcribe/latest/dg/toxicity.html)
- [Call Analytics](https://docs.aws.amazon.com/transcribe/latest/dg/call-analytics.html)
- [Post-call analytics output](https://docs.aws.amazon.com/transcribe/latest/dg/tca-output-batch.html)
- [Amazon Transcribe Medical](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-medical.html)
- [Data protection](https://docs.aws.amazon.com/transcribe/latest/dg/data-protection.html)
- [Data encryption](https://docs.aws.amazon.com/transcribe/latest/dg/data-encryption.html)
- [Opting out of service improvement data use](https://docs.aws.amazon.com/transcribe/latest/dg/opt-out.html)
- [IAM policy examples](https://docs.aws.amazon.com/transcribe/latest/dg/security_iam_id-based-policy-examples.html)
- [How Amazon Transcribe works with IAM](https://docs.aws.amazon.com/transcribe/latest/dg/security_iam_service-with-iam.html)
- [Endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/transcribe.html)
- [Pricing](https://aws.amazon.com/transcribe/pricing/)
