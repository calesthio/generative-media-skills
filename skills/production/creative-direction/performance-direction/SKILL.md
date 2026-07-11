---
name: performance-direction
description: Provider-independent performance direction for generated video, avatar/spokesperson clips, animation, ads, film scenes, social content, and voice-led media. Use when an agent must cast or direct synthetic performers, avatars, animated characters, talking heads, AI video characters, or voice performances; plan acting beats, objective/obstacle/action, blocking, gesture, eye-line, facial expression, body language, lip-sync, voice alignment, rehearsal prompts, iteration, continuity, consent, and performance QA.
---

# Performance direction for generated media

Use performance direction to make a generated person or character appear to want something, react to pressure, and communicate through voice, face, gaze, and body. Do not ask a model for a generic emotion and hope it supplies acting. Give playable circumstances, beat-level actions, physical behavior, vocal behavior, continuity constraints, and a way to judge the take.

## Evidence stance

Documented facts used by this skill:

- Stanislavski-derived actor training commonly analyzes a role through given circumstances, tasks/objectives, actions, beats, obstacles, and physical action; for AI use, translate these into concise, playable instructions rather than academic labels. Source cross-check: [Stanislavski system overview](https://en.wikipedia.org/wiki/Stanislavski%27s_system) and [NYFA summary of Stanislavski questions](https://www.nyfa.edu/student-resources/stanislavski-in-7-steps-better-understanding-stanisklavskis-7-questions/).
- Lip-sync systems often map speech sound to visemes, not one mouth shape per phoneme. Microsoft documents visemes as visual phoneme descriptions and notes many phonemes can share one viseme; Meta's Oculus Lipsync documentation describes interpolation between visemes over time. Verified 2026-07-10: [Microsoft viseme docs](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis-viseme), [Meta viseme reference](https://developers.meta.com/horizon/documentation/unreal/audio-ovrlipsync-viseme-reference/).
- Professional dubbing guidance treats timing, natural language, audio level, and physical mouth/gesture sync as production constraints. Verified 2026-07-10: [Netflix films/series dubbing guidelines](https://partnerhelp.netflixstudios.com/hc/en-us/articles/11220839130771-Dubbing-Creative-Guidelines-Films-Series-English), [Netflix nonfiction simil-sync guidance](https://partnerhelp.netflixstudios.com/hc/en-us/articles/11220999686163-Dubbing-Creative-Guidelines-Nonfiction-Unscripted-English).
- Current avatar tools expose different levels of performance control: some require clean training footage and consent capture, some accept a script and avatar selection, and some offer sentiment/emotional-state controls. Verified 2026-07-10: [Synthesia Studio Avatar requirements](https://docs.synthesia.io/docs/studio-avatars), [D-ID quickstart](https://docs.d-id.com/docs/quickstart), [HeyGen Digital Twin docs](https://developers.heygen.com/generate-avatar-video).
- Current AI video prompting can include character references, longer clips, extension, and batch workflows in some providers; treat capability limits as provider- and date-specific. Verified 2026-07-10: [OpenAI Sora 2 prompting guide](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide).
- Performer likeness, voice, and digital replica use raise consent, compensation, use-limit, storage, and disclosure duties. Verified 2026-07-10: [SAG-AFTRA AI resource page](https://www.sagaftra.org/contracts-industry-resources/member-resources/artificial-intelligence), [SAG-AFTRA Digital Replicas PDF](https://www.sagaftra.org/sites/default/files/sa_documents/DigitalReplicas.pdf), [NAVA synthetic voice guidance](https://navavoices.org/synth-ai-info/).
- Provenance/disclosure can be supported by metadata standards such as C2PA Content Credentials, but provenance support varies by platform and workflow. Verified 2026-07-10: [C2PA](https://c2pa.org/).

Empirical observations to collect on each job:

- Which performance details the chosen model obeys reliably: eye-line, gesture, expression intensity, hand accuracy, lip-sync, pauses, breath, camera blocking, and continuity.
- Whether the model responds better to actor-direction language ("tries to reassure") or visible-output language ("soft smile, shoulders lower, eyes return to lens").
- Which constraints degrade output when over-specified, especially in short clips or avatar tools with fixed pose libraries.

Production heuristics, not universal facts:

- Direct actions before emotions: "tries to win her trust" usually produces more coherent behavior than "is sad."
- Use one dominant objective per beat and one visible adjustment at the beat turn.
- Calibrate emotion on a 0-5 screen intensity scale; most business/avatar clips need 1-3, while animation, comedy, and social hooks can tolerate 3-5.
- Give every gesture a job. Random pointing, nodding, and hand waving read as synthetic.
- Lock voice timing before final avatar/lip-sync generation when the face is audio-driven.
- Repair the smallest failed layer first: script intent, voice read, facial expression, body action, camera, edit, or generation settings.

## Build the performance brief

For every speaking or acting subject, write a compact brief before prompting generation:

1. Medium and constraint: avatar presenter, cinematic AI video, rigged animation, generated ad, dubbing/localization, social UGC, or voice-only.
2. Casting: age range, presence, vocal texture, physical energy, style reference if licensed/allowed, and what not to imitate.
3. Given circumstances: where the character is, what just happened, who they believe they are speaking to, and what pressure is active.
4. Objective: what they want from the viewer or other character in this beat.
5. Obstacle: what makes that objective difficult.
6. Action verb: what they do to overcome it, such as reassure, challenge, charm, deflect, confess, teach, invite, or warn.
7. Beat turn: the moment when new information or resistance changes the tactic.
8. Visible behavior: posture, gaze, hands, facial muscles or expression, breath, stillness, movement path, proximity, and touch/no-touch boundaries.
9. Vocal behavior: pace, pitch range, volume, pauses, stress words, breath, laugh/hesitation, accent/dialect only when appropriate and safe.
10. Continuity: where the eyes, hands, body, prop, emotional state, and voice start/end so adjacent shots match.
11. Safety/rights: consent status, likeness/voice rights, permitted use, disclosure/provenance requirement, and prohibited resemblance.

Keep the brief short enough to fit into the generation prompt or handoff notes. If a provider has weak control over a dimension, move that dimension into QA and iteration rather than pretending it is guaranteed.

## Direct playable beats

Beat direction should answer:

- What changed?
- What does the performer want now?
- What tactic are they trying?
- What leaks through despite control?
- What exact visible/vocal behavior should change?

Use playable action verbs instead of result adjectives:

| Weak direction | Stronger performance direction |
|---|---|
| "She is worried." | "She tries to sound calm while checking whether the viewer understands; her eyes hold steady, then flick down for half a beat before she recovers." |
| "Make him confident." | "He invites the viewer in as if sharing a shortcut he has tested; relaxed shoulders, direct lens contact, small smile on the first proof point." |
| "Very emotional." | "He starts controlled, swallows the next word, then lets one breath land before saying the final sentence more quietly." |
| "Friendly avatar." | "Warm onboarding host: open chest, hands quiet at waist, nod only at the user's likely concern, pace 10% slower on setup steps." |

For short generated clips, limit each shot to one or two beat turns. If the scene needs several tactical shifts, split it into multiple shots or takes.

## Calibrate emotion and expression

Name the underlying emotion only after defining the action. Then specify screen intensity:

- 0: neutral task focus.
- 1: trace; readable mostly in eyes, breath, or timing.
- 2: natural professional expression.
- 3: clear dramatic/social read.
- 4: heightened genre or animated read.
- 5: caricature, panic, slapstick, or theatrical exaggeration.

Add contradiction when needed: "voice stays professional, face reveals concern." This prevents flat delivery and avoids asking the model to make every channel express the same emotion.

For faces, prefer observable cues:

- brow: relaxed, slight pinch, lifted inner brow, skeptical brow drop;
- eyes: direct lens, tracking another character, soft focus, brief eye dart, slower blink;
- mouth: closed-mouth smile, smile suppressed, lips press, jaw releases, half-laugh;
- head: still, small nod, tilt, recoil, lean-in, turn away.

Avoid stacking too many expression cues. A face cannot convincingly do "wide smile, clenched jaw, whispered grief, aggressive stare, relaxed warmth" in one beat unless the contradiction is intentional and physically coherent.

## Blocking, gesture, and eye-line

Blocking is performance meaning in space. State where the performer is, how they orient to the viewer/partner/camera, and why they move.

Use these defaults:

- Direct-to-camera presenter: lens is the listener. Use steady eye contact, occasional thinking glances away, and deliberate re-entry to lens for key claims.
- Dialogue: define each character's eye-line target and whether they avoid, challenge, seek, or break contact.
- Product/social ad: let the body discover or demonstrate the product; hands enter only when the story needs proof, comparison, or invitation.
- Film scene: block movement around power, avoidance, attraction, secrecy, or discovery. Distance and stillness can be more expressive than constant movement.
- Animation: make silhouettes and pose changes readable; use anticipation before large action and settle after emotional changes.

Gesture rules:

- Give each gesture a verb: reveal, stop, measure, protect, count, invite, dismiss.
- Match gesture scale to frame size. Close-ups need micro-gestures; wide shots can use full-body action.
- Do not ask for constant hand motion in avatar tools unless the tool supports gesture control and the brand style tolerates it.
- Keep hands away from faces, logos, small props, and occluded regions when the model is prone to artifacts.

Eye-line continuity matters. For multi-shot scenes, record who/what each character is looking at at the start and end of every shot. In AI video, inconsistent eye-line is often a continuity failure, not just a face failure.

## Align voice, lip-sync, and face

Voice performance drives perceived acting in avatar and voice-led media. Direct:

- intention: what the speaker is doing to the listener;
- pace: steady, urgent, deliberate, conversational, compressed;
- pauses: where the thought changes, not just where punctuation appears;
- emphasis: one or two key words per sentence;
- breath: calm inhale, held breath, laugh-breath, recovery breath;
- contour: where energy rises, falls, or resolves;
- articulation: crisp, relaxed, mumbled, hesitant, but only if it serves clarity.

For synthetic voices, write performance markup in the syntax the provider supports; if syntax is unknown, use plain text notes adjacent to the line. Verified 2026-07-10, ElevenLabs documents pacing as a major part of voice design and advises clear pacing language for voice outputs: [ElevenLabs Voice Design](https://elevenlabs.io/docs/eleven-creative/voices/voice-design).

For lip-sync/avatar generation:

1. Finalize or nearly finalize the script before generating a face.
2. Generate or select the voice take.
3. Check word timing, pauses, and emotional arc.
4. Generate avatar/lip-sync from the selected audio or script.
5. QA mouth open/close starts, final closures, bilabials (p/b/m), fricatives (f/v), and visible jaw rhythm.
6. If mismatch appears, repair the audio timing or line length before over-directing the face.

For dubbing/localization, maintain meaning and natural speech while respecting original timing and visible mouth/gesture openings. If perfect internal mouth-shape match makes language unnatural, choose the sync type explicitly: lip-sync, simil-sync, voice-over, narration, or subtitle-supported dub.

## Avatar and animation constraints

Do not direct every medium like live action.

Avatar presenter:

- Strengths: consistent framing, direct address, scalable delivery, training/explainer/social presenter formats.
- Risks: repetitive gestures, fixed posture, uncanny eye contact, emotional flattening, mismatch between voice clone and face.
- Direction style: concise presenter intent, frame, pace, sentiment, gesture density, allowed camera angle, and brand energy.

Talking photo:

- Strengths: fast personalization and face-led address.
- Risks: limited body language, weak gesture, head/eye artifacts, identity sensitivity.
- Direction style: voice-first; keep expressions simple and avoid complex physical action.

AI cinematic character:

- Strengths: richer movement, environment, camera, and scene dynamics when supported by the model.
- Risks: continuity drift, inconsistent acting across shots, uncontrolled hands/eyes, over-literal emotion.
- Direction style: shot-by-shot beats, physical blocking, camera relation, start/end continuity, references where permitted.

Rigged 2D/3D animation:

- Strengths: precise pose, gesture, timing, repeatability, exaggeration.
- Risks: stale poses, floaty transitions, weak weight/anticipation, lip-sync mismatches.
- Direction style: pose keys, timing, ease, silhouette, anticipations, holds, settles, facial control names if available.

Voice-only:

- Strengths: maximum control through rewrite, casting, pacing, and edits.
- Risks: monotonous read, overacting, unclear speaker relationship.
- Direction style: line-by-line intention, listener image, tempo map, pause map, emphasis, pickups.

## Casting, likeness, and consent

Before creating or directing a synthetic human, decide whether the performer is:

- fictional and non-identifiable;
- a stock/licensed avatar;
- a custom avatar based on a consenting person;
- a known public figure, employee, customer, influencer, actor, or deceased person;
- an imitation of a real voice, face, style, or performance.

Require written scope for custom or recognizable likeness/voice work:

- who gave consent and whether they are authorized to grant it;
- what media, script type, territory, duration, platform, and edits are allowed;
- whether the voice/likeness can train models, generate new lines, or be reused later;
- compensation, revocation, storage, exclusivity, and deletion terms when applicable;
- disclosure/provenance plan for synthetic media.

If consent is missing or ambiguous, redirect to a fictional/non-identifiable performer, licensed stock avatar, or human-recorded performance. Do not create a "soundalike" or "lookalike" workaround for a real person when the intent is recognizability.

## Rehearse through prompts

Use prompt rehearsal before expensive final renders:

1. Table read: generate or write two voice takes with different actions, not different emotions.
2. Pose rehearsal: ask for still frames or key poses when available; check silhouette, gaze, hand placement, and expression intensity.
3. Beat rehearsal: generate a short version of the scene with only the beat turn.
4. Continuity rehearsal: test adjacent shots with the same start/end states and references.
5. Final performance: add production detail only after the acting read works.

Iteration notes should be specific:

- "Reduce smile from 3 to 1; keep warmth in eyes, not teeth."
- "Hold eye contact through the objection, then look down only after the denial."
- "Gesture once on the proof point; hands still for the emotional admission."
- "The line is too fast for the mouth closure; add a 200-400 ms pause before the final word or choose a slower voice take."
- "The character is displaying fear, but the objective is to persuade. Re-direct as 'tries to reassure while managing fear.'"

## Performance QA

Review the output with the sound on, sound off, and audio-only.

Sound on:

- Does the performer pursue a clear objective?
- Does the voice match face/body energy?
- Are beat turns audible and visible?
- Do pauses feel like thought, not latency?
- Are dubbed/avatar mouth starts and endings acceptable for the chosen sync standard?

Sound off:

- Can you infer relationship, attention target, and pressure?
- Are gaze, posture, and hands motivated?
- Does the expression intensity match genre and brand?
- Are there uncanny loops, frozen blinks, hand artifacts, or random nods?

Audio-only:

- Does the read have a listener, tactic, and arc?
- Are key words stressed without sounding salesy or theatrical?
- Is the pace appropriate for platform, information density, and captions?

Continuity:

- Start/end emotion, body orientation, eye-line, prop state, wardrobe, and voice tone match adjacent shots.
- Character references, avatars, and voices are identified in the handoff.
- Consent/provenance notes travel with the asset.

## Handoff format

For each performer or character, hand off:

```text
Performer: <name or asset id>
Consent/rights: <fictional/licensed/custom consent status; allowed uses; disclosure>
Casting read: <age/presence/vocal/body energy; prohibited resemblance>
Scene objective: <what they want>
Obstacle: <what resists them>
Relationship/listener: <who they believe they address>
Beat map:
  00:00-00:03 <action, expression intensity, gaze/body/voice>
  00:03-00:07 <beat turn and new tactic>
Voice notes: <pace, pauses, emphasis, breath, pronunciation>
Blocking/gesture: <position, movement, hands, props, eye-line>
Continuity in/out: <start and end states>
QA priorities: <highest-risk performance details>
```

## Example: avatar onboarding clip

Production intent: 25-second SaaS onboarding video for a warm but credible avatar presenter. Medium: script-driven avatar with direct-to-camera framing.

Performance brief:

```text
Performer: licensed stock avatar, mid-30s, calm technical host.
Objective: reassure a new user that setup is quick and safe.
Obstacle: the user expects integration setup to be annoying.
Action: demystify, then invite.
Emotion scale: warmth 2, urgency 1, confidence 2.
Eye-line: lens as user.
Gesture density: low; one small open-hand gesture on "two minutes."
Voice: conversational, 145-155 wpm, slight smile in tone, pause after first sentence.
Consent/rights: stock avatar within platform license; disclose synthetic presenter if required by channel policy.
```

Script/performance direction:

```text
[steady lens contact; relaxed shoulders]
"You do not need to rebuild your workflow."
[small pause; softer smile, warmth 2]
"Connect your calendar, choose the approval rule, and we will show you the first safe draft before anything goes live."
[one open-hand gesture on "first safe draft"; pace slows 8%]
"Most teams finish setup in about two minutes."
[return hands still; invite, not pressure]
"Let us do the first pass together."
```

Why it is structured this way: the avatar gets one objective, one obstacle, a restrained gesture plan, and voice timing that supports lip-sync and trust. Likely failures: over-smiling, random nodding, too-fast line two. Repair by reducing expression intensity, removing extra gesture requests, or splitting the long sentence.

## Example: generated cinematic two-character scene

Production intent: 8-second dramatic shot for a short film teaser. Medium: AI video, over-the-shoulder close-up, no celebrity likeness.

Prompt-ready direction:

```text
Shot: close over Mira's shoulder toward Jonas at a rain-streaked bus shelter at night, 50mm, shallow depth of field. Fictional characters, no resemblance to real actors.
Given circumstances: Jonas has just been caught hiding the train ticket; Mira is waiting for an explanation off camera.
Jonas objective: persuade Mira not to leave.
Obstacle: he knows his excuse is weak and she has stopped trusting him.
Action: confess just enough to keep her there.
Beat 1 (00:00-00:03): Jonas holds Mira's eye-line slightly left of lens, jaw tight, breath held, face controlled at regret 2.
Beat turn (00:03): he sees she is about to walk away.
Beat 2 (00:03-00:08): his shoulders drop, eyes flick to the ticket then back to Mira; he says quietly, "I bought two." No smile. Voice low, slower on "two."
Blocking: Jonas remains still except the ticket hand lowers into frame; Mira is a blurred shoulder foreground, no speaking.
Continuity out: Jonas looking at Mira, ticket visible at chest height, rain and neon consistent.
QA: eye-line to Mira, hand artifact on ticket, no melodramatic crying, mouth closes after "two."
```

Why it is structured this way: the scene is directed through objective and obstacle, not "sad man." It gives the model one physical reveal and one emotional shift. Likely failures: ticket hand distortion, eyes to camera, overacted tears. Repair with a closer crop, clearer prop silhouette, or reduced emotion scale.

## Example: animated explainer character with voice

Production intent: 15-second cartoon character explains why password managers help. Medium: rigged 2D character with TTS and simple viseme lip-sync.

Direction:

```text
Character: small raccoon office helper, curious and practical, no real-person likeness.
Objective: convince the viewer to stop reusing passwords.
Obstacle: the viewer thinks password managers are extra work.
Action: make the danger concrete, then offer relief.
Animation constraints: use three poses only: lean-in warning, count-on-fingers, relaxed thumbs-up. Keep paws below chin to avoid mouth occlusion.
Emotion scale: concern 3 for first beat, relief 3 for final beat; animation style allows exaggeration.
Voice: bright, quick but clear; pause after "same key."

Line map:
00:00-00:05 lean-in warning, eyes wide, paws still:
"Using one password everywhere is like using the same key for your house, car, and diary."
00:05-00:10 count-on-fingers, one paw gesture only:
"A password manager makes different keys and remembers them for you."
00:10-00:15 relaxed thumbs-up, smile 3, slower final phrase:
"You remember one master password. That is the deal."

Lip-sync QA: check open vowels in "everywhere" and final mouth closure on "deal"; if weak, slow the final sentence or regenerate visemes from final audio.
```

Why it is structured this way: the acting is simple enough for a rig, gestures do not fight lip-sync, and each pose has a persuasive job.
