# Evaluation for amazon-transcribe

The evaluated agent receives only `SKILL.md` and the user task. Use this file as the scorer's answer key. Do not reveal this file to the evaluated agent.

Score with the point values below as weights, then normalize the awarded score to a 100-point scale. Passing requires at least 80/100 after normalization and no critical failure.

Critical failures:

- Claims Amazon Transcribe can process more than two channels for standard Transcribe.
- Treats PII/PHI redaction as legally complete without human review for sensitive or public-release use.
- Recommends Medical output for patient care without trained human review.
- Uses Call Analytics as a generic default for captions or ordinary transcripts without call-insight requirements.
- Ignores S3/IAM/KMS custody when the scenario is AWS- or regulated-data-focused.
- Mentions or relies on `EVAL.md` in the evaluated response.

## Knowledge questions

### 1. Batch versus streaming

Question: A user has a finished MP4 in S3 and needs SRT captions by tomorrow. Should the agent choose batch or streaming Transcribe, and why?

Expected answer:

- Choose batch transcription.
- Mention batch works from media files in S3 and can directly produce SRT/VTT plus JSON.
- Streaming is for live/real-time audio and is not the best path for an already finished file.
- Include QA/editing after generated subtitles.

Points: 8

### 2. Output formats and timestamps

Question: What output should an agent expect from a basic batch Amazon Transcribe job, and what extra subtitle formats are available?

Expected answer:

- JSON transcript output with paragraph transcript and item-level details.
- At minimum, word items include start time, end time, and confidence.
- Subtitle feature can produce SRT and VTT for batch video jobs.
- Should not claim DOCX, ASS, TTML, or speaker-name captions are native output unless post-processed.

Points: 8

### 3. Diarization versus channel identification

Question: A two-person interview was recorded with host on the left channel and guest on the right channel. The user asks for speaker-separated transcript. What should the agent choose?

Expected answer:

- Prefer channel identification because each participant is on a stable channel.
- Mention output channels are labeled `ch_0` and `ch_1`.
- Mention standard Transcribe supports up to two channels and not more.
- Explain diarization is better for multiple speakers mixed onto one channel and returns generic `spk_*` labels.

Points: 10

### 4. Custom vocabulary and vocabulary filters

Question: Explain the difference between a custom vocabulary and a vocabulary filter.

Expected answer:

- Custom vocabulary improves recognition of specific words such as product names, acronyms, names, or domain terms.
- Vocabulary filter masks/removes/tags exact word matches according to the chosen method.
- Strong answer notes table format is preferred for custom vocabularies and character/language constraints apply.
- Strong answer does not confuse filters with PII redaction.

Points: 8

### 5. Language identification boundaries

Question: What risk should an agent mention when combining automatic language identification with redaction?

Expected answer:

- Feature support is language-specific and must be checked.
- If redaction is enabled but audio includes unsupported languages, those languages may not be redacted and may not cause warnings/failures.
- For known-language regulated audio, specify language and verify redaction support.

Points: 8

### 6. Security and custody

Question: Name the AWS custody controls an agent should check before processing confidential audio with Amazon Transcribe.

Expected answer:

- Customer-owned S3 input and output buckets/prefixes.
- S3 encryption and optionally SSE-KMS/KMS key policy.
- Least-privilege IAM for Transcribe, S3, and KMS; trust/confused-deputy controls when roles are assumed.
- CloudTrail/logging and lifecycle deletion.
- AI services opt-out policy if required.
- Avoid sensitive values in tags, job names, and free-form fields.

Points: 12

### 7. Quotas and limits

Question: List important production limits for standard Amazon Transcribe verified in the skill.

Expected answer:

- Standard batch max audio length 28,800 seconds and max file size 2 GB.
- Minimum audio duration 500 ms.
- Channel identification limit of 2.
- Concurrent standard streams 25 and concurrent standard transcription jobs 250, noting quotas may be region-specific and some adjustable.
- 90-day job-record retention.

Award partial credit for any three with a note to verify current Service Quotas.

Points: 8

### 8. Pricing awareness

Question: How should an agent estimate Amazon Transcribe cost?

Expected answer:

- Price by audio duration and region, not file size.
- Check current AWS pricing before committing.
- Include feature/product differences such as standard batch/streaming, content redaction, Call Analytics, Medical, generative summaries, or custom language model add-ons.
- Include likely re-runs for sample/final/repair passes.

Points: 6

### 8b. Toxicity detection boundary

Question: What should an agent know before enabling Amazon Transcribe Toxicity Detection?

Expected answer:

- It is for batch transcriptions in US English (`en-US`).
- It flags/categorizes toxic speech with confidence scores and should be used as a moderation aid, not an automatic final decision.
- PII redaction can be combined in the documented console workflow, but most other listed options are not supported with Toxicity Detection.

Points: 6

## Production decision scenarios

### 9. Caption workflow for a public course video

Scenario: The user has a 42-minute edited course video, known English, several product names, and wants accessible captions and transcript. They use AWS and have an S3 bucket.

Strong answer must:

- Choose batch `StartTranscriptionJob`.
- Upload/extract final audio to S3 or use the media already in S3.
- Specify `LanguageCode` rather than language identification.
- Use a custom vocabulary for product names.
- Request SRT/VTT and JSON.
- Include human caption QA for line breaks, timing, punctuation, names, numbers, and non-speech cues.
- Include S3 retention/encryption and output bucket/prefix.

Unsafe or weak answer:

- Uses streaming because it is "faster" without a live requirement.
- Skips caption QA.
- Ignores vocabulary despite product names.
- Promises perfect ADA-compliant captions directly from ASR.

Points: 12

### 10. Regulated healthcare transcript

Scenario: A clinician wants to transcribe patient visits and use the transcript in records. What should the agent recommend?

Strong answer must:

- Consider Amazon Transcribe Medical, not just standard Transcribe.
- State Medical is US English only in the skill and available for batch/streaming.
- State it is not a substitute for medical advice/diagnosis/treatment.
- Require trained medical professional review before patient-care use.
- Discuss PHI/HIPAA eligibility only with AWS BAA/account/process controls and encryption in transit/at rest.
- Include S3/IAM/KMS/CloudTrail/lifecycle controls and opt-out if required.

Critical failure if:

- Suggests direct unsupervised insertion into medical records.

Points: 12

### 11. Support-call analytics versus transcript search

Scenario: A company has 100,000 stereo support calls. They first ask for searchable text; later the QA director asks for sentiment, interruptions, talk speed, issue/outcome summaries, and action items. How should the plan change?

Strong answer must:

- For searchable text, standard batch with channel identification is sufficient if channels map to agent/customer.
- For sentiment, interruptions, talk speed, summaries/action items, and categories, move to Call Analytics.
- Note Call Analytics is designed for customer-agent calls and has different pricing/quotas.
- Preserve channel/call metadata and verify region/quota.
- Include vocabulary/filter/redaction decisions as needed.

Points: 10

## Applied task

### 12. Write a provider plan

User request: "Use AWS to transcribe a 90-minute bilingual webinar into captions and a speaker-labeled transcript. It contains names, emails, and phone numbers. We need to publish captions publicly, but keep raw files private."

Expected output characteristics:

- Begins by identifying open questions: languages/dialects, whether speakers are channel-separated, public caption format, privacy policy, target region, AWS account/S3 buckets.
- Recommends batch Transcribe because the webinar is recorded and captions are needed.
- Handles bilingual carefully: use language identification or multiple-language identification only if supported for desired features; verify redaction language support before relying on it.
- Explains speaker labels: use channel identification if separate channels; otherwise diarization with generic `spk_*` and manual speaker-name mapping.
- Uses custom vocabulary for names and domain terms.
- Uses PII redaction as an assist but requires human privacy review before public captions.
- Requests SRT/VTT and JSON, with subtitle QA/edit pass.
- Specifies S3 private buckets, output prefix, encryption/SSE-KMS if needed, least-privilege IAM, CloudTrail, lifecycle deletion, no sensitive job names/tags, and AI opt-out if required.
- Mentions quota/pricing verification for 90 minutes in target region.

Rubric:

- Provider/product choice and feature selection: 10
- Language/redaction caution: 10
- Speaker/caption workflow: 10
- Security/custody: 10
- QA and release safety: 10

Critical failures:

- Publishes auto-redacted captions without human review.
- Promises speaker names from diarization automatically.
- Ignores bilingual redaction limitations.

Points: 50, scale to 20 when combining with the 100-point total by multiplying the awarded task score by 0.4.
