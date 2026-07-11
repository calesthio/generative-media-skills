# Evaluation: music-supervision-scoring

Use this file as the answer key and scoring guide for evaluating an agent that had access to `SKILL.md` only. Do not expose this file to the evaluated agent.

The evaluated agent should demonstrate rights-aware, story-aware, technically practical music supervision and scoring direction for audiovisual production. Reward concrete, timecoded, production-usable decisions. Penalize generic mood adjectives, unsupported legal certainty, artist soundalike prompting, and ignoring mix/accessibility constraints.

## Scoring overview

Score out of 100:

- Production diagnosis and spotting: 20
- Music-source and rights reasoning: 20
- Score/AI-music prompting craft: 20
- Mix, stems, loudness, and delivery handoff: 15
- Accessibility and platform constraints: 10
- Iteration/repair and QA: 10
- Evidence discipline and dated volatile facts: 5

Critical failures can cap the score even if other parts are strong:

- Cap at 40 if the response recommends using a famous copyrighted song or soundalike in a commercial deliverable without clearance.
- Cap at 45 if it treats "royalty-free," "platform-safe," or "AI-generated" as universally rights-cleared without license scope verification.
- Cap at 55 if it gives a music prompt only, with no spotting, rights, mix, or delivery plan for a real video.
- Cap at 60 if it invents cue sheet metadata, rights ownership, or legal conclusions.
- Cap at 70 if it ignores voice/dialogue intelligibility in a dialogue-led video.

## Knowledge questions

### 1. What is a spotting map and why should an agent make one before generating music?

Expected answer:

- It is a cue-by-cue plan with stable cue IDs, in/out timecodes, cue type, dramatic function, sync points, emotional turns, avoid list, and handoff needs.
- It prevents generic music, missed edit hits, overuse of music, and late rights/mix surprises.
- It should include silence and exits, not only music starts.

Required points:

- Mentions timecodes and cue IDs.
- Mentions dramatic/emotional function.
- Mentions sync points or edit hits.
- Mentions silence or music exits.
- Mentions downstream handoff or revision stability.

Penalize:

- Defining spotting as only "choosing a genre."
- Omitting timecodes.
- Treating music as a single whole-video bed when the scenario needs multiple cues.

### 2. Explain the composition/master rights issue for a needle drop.

Expected answer:

- A musical work/composition and a sound recording are separate copyright-protected works often owned/licensed separately.
- A commercial recording normally needs clearance for both publishing/composition synchronization and the master recording.
- A cover/re-record may avoid the original master but not the composition side.
- The agent should not provide legal certainty; it should flag clearance/professional counsel for final rights decisions.

Required points:

- Separates musical work and sound recording.
- Identifies publishing/composition and master/recording sides.
- Explains cover/re-record distinction.
- Avoids pretending fair use or short duration automatically solves it.

Disqualifying claim:

- "Under 10 seconds is safe."
- "AI can recreate the song so no license is needed."

### 3. What belongs in a cue sheet or cue log?

Expected answer:

- Production title/version, cue ID/title, source, composer/writer, publisher, PRO, master/recording owner when relevant, identifiers if available, in/out/duration, usage type, rights notes, asset path/version.
- Unknown fields should be marked pending, not invented.
- Timings must be updated for cutdowns and localization versions.

Required points:

- Includes timing and usage.
- Includes composer/publisher/PRO or rights parties.
- Includes source/asset version.
- Includes "do not invent missing metadata."

### 4. Why is "make it like [famous artist/song]" a poor AI music prompt?

Expected answer:

- It creates soundalike/copyright/rights/brand risks and may violate provider policies or client requirements.
- It gives the model a reference identity instead of production attributes.
- Convert to neutral musical attributes: tempo, instrumentation, texture, arrangement density, harmony, rhythmic feel, emotional arc, mix constraints.

Required points:

- Mentions legal/rights or soundalike risk.
- Mentions policy/brand risk or originality risk.
- Provides attribute-based alternative.

### 5. What are LUFS and dBTP doing in a delivery review?

Expected answer:

- LUFS is used to measure programme loudness; dBTP/true peak estimates inter-sample peak/headroom.
- ITU-R BS.1770 is the loudness/true-peak measurement basis; EBU R 128 is a broadcast recommendation with -23 LUFS target and -1 dBTP max true peak for linear production.
- Final target depends on the actual platform/client/broadcaster spec; web/social heuristics are not universal.

Required points:

- Separates loudness from peak.
- Mentions programme/final mix measurement, not only raw music file.
- Mentions spec-dependent delivery.

Penalize:

- Saying "always master everything to -14 LUFS."
- Ignoring true peak.

## Production-decision scenarios

### 6. Branded TikTok ad wants a trending mainstream song

Scenario:

A brand asks for a 20-second TikTok paid ad using a trending mainstream track from a personal creator's post because "everyone is using it."

Strong decision:

- Do not proceed with the mainstream track unless the brand obtains appropriate rights.
- Explain that platform music availability differs for personal/general use versus business/commercial use; TikTok's Commercial Music Library is the safer in-platform source for brand/business content, but its scope should still be verified.
- Offer alternatives: CML track, commissioned/generated original, licensed needle drop with clearance, or client-supplied cleared music.
- Create a short spotting/prompt plan for the alternative.

Scoring:

- 4 pts: flags commercial rights risk.
- 4 pts: distinguishes general library/trending sound from business-cleared option.
- 4 pts: offers rights-safe alternatives.
- 4 pts: keeps creative intent alive rather than only saying no.
- 4 pts: records license-scope verification need.

Critical failure:

- Recommends ripping or recreating the trending track.

### 7. Documentary cue under sensitive interview

Scenario:

A 90-second documentary sequence includes a survivor describing a loss. The editor says the scene feels flat and asks for "sad piano."

Expected decision:

- Score subtext and ethical stance, not simply sadness.
- Spot exact entry/exit and leave room for words, breath, and possible audio description.
- Recommend restrained instrumentation, sparse register, minimal harmonic manipulation, and silence around key lines.
- Provide a prompt or composer brief with emotional arc: grief to reflection or unresolved dignity, not melodrama.
- Include mix notes: low density, no busy lead in speech band, duck around key lines, stems.

Scoring:

- 5 pts: rejects generic "sad piano" as insufficient.
- 5 pts: addresses ethics/subtext.
- 5 pts: includes spotting/time structure.
- 3 pts: includes dialogue/accessibility space.
- 2 pts: includes stems/mix handoff.

### 8. Product explainer needs AI-generated music quickly

Scenario:

A 45-second SaaS explainer has continuous narration, UI clicks, and a logo button. The user asks for a one-shot AI music prompt.

Expected output:

- A concise music plan with cue function and structure.
- Prompt includes duration, instrumental/no vocals, sections by time, tempo/feel, instrumentation, mix space for narration, logo sting, no artist imitation, no copyrighted melody/lyrics, and stem/alt request if supported.
- Notes to capture provider, terms snapshot, generation date, prompt/settings, and final asset path.
- Mix handoff mentions ducking and dialogue intelligibility.

Scoring:

- 5 pts: time-structured prompt.
- 4 pts: narration-space mix constraints.
- 3 pts: safe prompt negatives.
- 3 pts: deliverables/stems/variants.
- 3 pts: rights/provider documentation.
- 2 pts: logo/button/edit sync.

### 9. Game trailer with gameplay loop

Scenario:

A 75-second game trailer needs a music plan. It has an opening world reveal, gameplay mechanics, combat escalation, boss reveal, and logo.

Expected decision:

- Break into acts with time ranges and musical function.
- Include motif/theme for world or antagonist if useful.
- Request loopable gameplay section with bar-aligned loop point and separate final sting.
- Request stems for percussion, bass/synth, tonal/orchestral, risers/hits.
- Warn against references to existing franchises or composers.
- Include loudness/headroom and final mix measurement against platform spec.

Scoring:

- 5 pts: act map.
- 4 pts: loopability.
- 4 pts: stems/handoff.
- 3 pts: motif/theme use.
- 2 pts: rights-safe prompt language.
- 2 pts: delivery/mix QA.

### 10. Client-supplied "royalty-free" library track

Scenario:

The client provides a downloaded "royalty-free" MP3 and wants it used across YouTube, paid Instagram ads, a trade-show booth, and a broadcast TV buy.

Expected decision:

- Do not assume the license covers all uses.
- Request license document, source, purchaser/account, track title, composer/publisher info, permitted media, territory, term, paid ads, broadcast, public performance, sublicensing/client transfer, edits, attribution, and cue sheet needs.
- If license is insufficient, propose replacement paths.
- Maintain cue log and final asset version.

Scoring:

- 6 pts: challenges "royalty-free" assumption.
- 5 pts: checks scope across all media.
- 4 pts: requests concrete documentation.
- 3 pts: proposes alternatives.
- 2 pts: cue log/metadata.

## Applied production tasks

### 11. Write a spotting table for a 30-second ad

User request to evaluated agent:

"Make a music plan for a 30-second premium coffee ad: 0-5 sec dawn kitchen, 5-12 beans grinding, 12-20 pour-over macro shots, 20-27 first sip and smile, 27-30 logo. No dialogue, just supers."

Strong output characteristics:

- Uses timecoded cues/sections.
- Musical arc moves tactile/intimate to warm lift.
- Leaves room for sound design: grinder, pour, cup, breath.
- Does not over-score the whole piece; may spot silence or near-silence.
- Includes instrumentation, tempo/texture, logo button, deliverables/stems, loop/cutdown if relevant.
- Includes rights path recommendation: original/generated/library; no famous-song dependency.

Rubric, 20 points:

- 5: timecoded spotting.
- 4: music-sound-design relationship.
- 4: coherent emotional/brand arc.
- 3: deliverables/handoff.
- 2: rights-safe source plan.
- 2: QA/loudness/accessibility notes as relevant.

### 12. Repair a bad prompt

Bad prompt:

"Make a song like Billie Eilish for our skincare ad, with whisper vocals and the same dark vibe as bad guy. 15 seconds."

Expected repair:

- Explains the soundalike/named artist/song risk.
- Rewrites using attributes: intimate close vocal texture only if original lyrics and rights are cleared, or safer instrumental breathy textures; sparse sub bass, finger snaps, minimal percussion, dark pop-inspired production without imitation.
- Adds brand safety, duration, structure, no recognizable melody/lyrics, no artist references, no copyrighted hook.
- Notes vocal/lyric risks and suggests instrumental for easier commercial use.

Rubric, 15 points:

- 5: identifies artist/song imitation risk.
- 5: high-quality attribute-based rewrite.
- 3: commercial rights/vocal/lyric caution.
- 2: production details and deliverables.

### 13. Create a cue sheet draft row

User request:

"Here's final timing: M01 custom AI underscore 'Launch Pulse' starts 00:00:00:00 and ends 00:00:30:00 in our 30-second launch ad. I don't know the composer/publisher because it's generated. What should we log?"

Expected response:

- Provides row fields with known values and pending/unknowns.
- Does not invent composer/publisher/PRO.
- Logs AI provider, model/version if available, prompt/settings, generation date, asset path, license/terms snapshot, source as AI-generated/original generated, usage background/underscore, production title/version.
- Advises confirming provider terms and client policy; some cue-sheet systems may need special handling for generated music.

Rubric, 15 points:

- 4: complete known timing/usage fields.
- 4: no invented metadata.
- 4: AI provenance and terms snapshot.
- 3: next steps for missing fields/compliance.

### 14. Music QA review

User request:

"Review this plan: use YouTube Audio Library track in a YouTube video, then repost the same exported video as a paid TikTok ad and in a sales conference keynote. Master the whole video to -5 LUFS so it sounds loud. Captions only need spoken words."

Expected review:

- Flags platform/library scope issue; YouTube Audio Library safety does not automatically extend to TikTok paid ad or conference use.
- Flags excessive loudness target and recommends following delivery specs, measuring final programme LUFS/true peak, preserving dynamics and speech clarity.
- Flags captions should include meaningful non-speech/music cues where relevant.
- Recommends options: verify license portability, choose cross-platform library/license, CML for TikTok, original/generated music with rights review, separate exports.
- Suggests cue log and asset/license record.

Rubric, 20 points:

- 6: rights/platform issue.
- 5: loudness/headroom correction.
- 4: accessibility correction.
- 3: concrete safer alternatives.
- 2: metadata/cue log.

## Evidence discipline

A strong evaluated answer should:

- Mark legal/platform/provider facts as verified on a date when relevant.
- Prefer "verify the active license/terms" over blanket claims.
- Avoid unsupported claims that any provider, genre, or loudness value is universally best.
- Separate documented facts from observations and heuristics when the distinction matters.

Award the evidence-discipline 5 points as follows:

- 5: clearly distinguishes facts, observations, and heuristics; dates volatile facts; does not overclaim.
- 3: generally cautious but not explicit about dates or evidence type.
- 1: some correct facts but mixed with unsupported universals.
- 0: gives confident legal/platform/provider claims without support.
