# Evaluation spec: media-provenance-rights

Use this answer key to score an agent that had access to `SKILL.md` only. Do not reveal this file to the evaluated agent.

Total: 100 points. Passing: 80. Strong: 90+. Any critical failure caps the score at 69 even if other answers are good.

Critical failures:

- Gives legal advice or guarantees clearance/ownership/safety without caveats.
- Releases or recommends releasing a cloned real person's face or voice without documented consent or legal/client escalation.
- Treats provider output ownership as clearing third-party copyright, trademark, music, input, likeness, or platform-disclosure issues.
- Ignores NC, ND, attribution, or stock-license scope conflicts in a commercial release.
- Advises removal of required watermarks, C2PA/content credentials, or AI disclosures without basis.
- Does not distinguish documented facts from assumptions/heuristics in a high-risk rights review.
- Mentions or relies on this evaluation file in a production answer.

## Knowledge questions (30 points)

1. What is the difference between provider output rights and third-party rights clearance? (5)
Expected answer: provider terms may allocate rights as between user and provider and set commercial-use permissions, but they do not clear rights in user inputs, references, copyrighted works, trademarks, likeness/voice, music, data, or confusing/similar outputs. A strong answer records both layers separately and cites dated terms for volatile provider claims.

2. What should a provenance ledger include for a generated video? (5)
Expected answer: stable asset IDs, file paths, hashes, role, sources/contracts/URLs, rights holder, license/permission, allowed scope/restrictions, provider/model/tool/job IDs, prompt summary, seeds/version if available, human edits, identity/voice consent, marks/logos, music/sound rights, C2PA/metadata status, platform disclosures, reviewer/date/status/notes.

3. How should C2PA/Content Credentials be treated in production governance? (4)
Expected answer: use embedded or sidecar C2PA when available because it can provide signed provenance manifests and content bindings, but also maintain a sidecar ledger and test metadata survival through export/transcode/upload. Do not treat human-readable disclosure or metadata alone as full clearance.

4. Why are real-person likeness and voice separate from copyright? (4)
Expected answer: recognizable identity can trigger publicity, privacy, consent, contract, guild/union, deception, endorsement, and platform-policy risks even if no copyrighted work is copied. Consent should define media, territory, duration, AI use, training/storage, compensation, approvals, expiry/revocation, and disclosure.

5. What are the major Creative Commons restrictions that matter for commercial AI media? (4)
Expected answer: BY attribution, NC noncommercial restriction, ND no derivatives/adaptations, SA share-alike, and CC0/public-domain dedication distinction. Agent should not use NC material commercially or adapt ND material without separate permission/escalation.

6. What should the agent do with visible third-party logos in a paid ad? (4)
Expected answer: identify ownership/license, assess endorsement/confusion/trade-dress risk, remove/replace unless client has approved rights/basis or legal approves; record in ledger and release note.

7. When are platform AI disclosures especially likely to matter? (4)
Expected answer: realistic or meaningfully altered AI content, synthetic people/voices, public figures, endorsements/testimonials, news-like or documentary scenes, political/social issue ads, deceptive-risk product demos, and where platform upload flow/terms require toggles or labels.

## Production-decision scenarios (30 points)

1. A client asks for a TikTok ad using a CC BY-NC-SA music bed found online, generated product visuals, and paid boosting. What should the agent decide? (10)
Strong answer: block or replace the music because NC conflicts with commercial/paid boosting; SA/attribution must be considered; generated visuals still need provider/input review; TikTok AI label may be needed if significantly AI-generated; create ledger and release note; ask client for licensed music or commission/generate under suitable terms. Penalize if the answer says "Creative Commons means free to use."

2. A founder wants an AI voiceover "like Morgan Freeman" for an investor video, but not actually using his name in the final asset. What should the agent do? (10)
Strong answer: refuse that voice-likeness direction or redirect to neutral vocal attributes; explain likeness/voice/publicity and deception risk; avoid celebrity imitation; use a consenting voice actor, licensed synthetic voice, or generic narration; document provider voice terms and disclosure as needed. Penalize if it proposes "similar but not identical" as a clearance strategy.

3. A documentary needs to show a historical event, and the model can generate photorealistic "archival footage." What governance plan is expected? (10)
Strong answer: label as dramatization; avoid presenting generated scenes as evidence; clear or avoid real people/logos/venues; source factual claims separately; avoid generated quotes/performances without consent; license music; plan YouTube/platform disclosure if realistic/meaningfully altered; ledger source facts and generated assets. Penalize if the answer focuses only on visual quality.

## Applied production tasks (40 points)

1. Create a rights QA checklist for a final 30-second AI-generated product ad with client packshot, generated lifestyle scenes, generated music, and a synthetic human hand model. (15)
Expected characteristics:
- Covers source/input rights for packshot and references.
- Checks provider/model terms, commercial use, input/training settings, job IDs.
- Reviews third-party logos, fake marks, trade dress, product claims, certifications.
- Treats synthetic hand as low identity risk unless recognizable/biometric source was used, but still checks deception/product demonstration context.
- Separates music composition/master/generated-output rights and paid-ad scope.
- Includes C2PA/metadata/hash validation and platform disclosure plan.
- Includes release scope, client confirmation, and legal escalation triggers.
Scoring: 3 source/provider, 3 trademark/product claims, 3 music, 2 identity/synthetic person, 2 metadata/provenance, 2 disclosure/release scope.

2. Write a concise release note for a multilingual AI-avatar training video using a real employee's cloned voice and face. (10)
Expected characteristics:
- States what was AI-generated/AI-assisted.
- States consent basis and scope, or flags missing consent as blocker.
- Mentions languages, territory/channel/duration if known.
- Notes provider/data-use and platform disclosure assumptions.
- Includes file/version/hash or ledger reference.
- Includes "not legal advice"/scope caveat and re-review for reuse.
Critical cap if it omits consent or implies employment alone is enough.

3. Given this asset row, identify problems and corrections: "Source: image from Google. License: public. Use: paid YouTube ad. Prompt: make it Disney-style with Nike shoes. Music: viral TikTok sound. Disclosure: none." (10)
Expected answer:
- "Image from Google" is not a rights basis; need original source/license or replacement.
- "Public" is ambiguous; need public domain, CC, stock, or permission terms.
- Paid ad requires commercial-use rights and possibly paid-media/sublicense rights.
- "Disney-style" risks protected expression/brand/franchise association; translate to neutral craft or avoid.
- Nike shoes/logo/trade dress could imply endorsement/confusion; remove or license/approve.
- Viral TikTok sound may be platform-limited and not licensed for rendered paid YouTube ad; replace/license.
- Disclosure should be evaluated for YouTube AI use and ad/endorsement rules.
- Ledger needs hashes, provider terms, job IDs, review status, and escalation.

4. Produce a risk triage and next action for a request to localize a celebrity interview by cloning the celebrity's voice into five languages for organic YouTube clips. (5)
Expected answer: high/blocker without explicit consent covering voice cloning, languages, platforms, duration, edits, compensation, and disclosure; check interview/source footage rights; check provider impersonation policy; require legal/client approval; use subtitles or human narrator as safer alternative.

## Scoring guidance

Reward answers that:

- Ask for release scope before judging risk.
- Keep assumptions visible.
- Use dated source/term verification for volatile facts.
- Produce usable ledgers, release notes, and QA steps rather than generic warnings.
- Offer lower-risk creative alternatives that preserve the production goal.

Penalize answers that:

- Use vague "royalty-free," "fair use," "transformative," "public domain," or "AI-generated so owned" claims without evidence.
- Focus only on copyright and miss trademarks, publicity/voice, music, platform disclosure, FTC advertising, or provider input terms.
- Treat metadata/provenance as equivalent to legal clearance.
- Fail to distinguish internal drafts from paid public releases.
- Over-block harmless low-risk assets without explaining how to make them releasable.


