# Evaluation specification for `sound-design-foley`

This file is the scoring guide for evaluating whether an agent can use the `sound-design-foley` skill competently. The evaluated agent should receive the user task and `SKILL.md` only. Use this file after capturing the response.

## Core scoring dimensions

Score out of 100:

- Spotting and prioritization: 15
- Foley and sound-family competence: 15
- Prompt/source planning and rights safety: 15
- Layering, perspective, materials, and emotional intent: 15
- Edit/mix handoff and technical QA: 15
- Loudness, safety, accessibility, and captions: 15
- Communication quality and applicability to the user’s deliverable: 10

Passing threshold: 80. A response below 70 should be considered not production-ready. A response with any critical failure listed below should fail even if it has strong prose.

## Critical failures

Fail the response if it:

- recommends ripping or copying recognizable sounds from films, games, songs, TikToks, YouTube videos, apps, OS notification palettes, or brand assets without clearance;
- treats "royalty-free" as sufficient without checking license terms, attribution, commercial-use, derivative, or platform limits;
- asserts one universal loudness target for all media, platforms, and clients;
- ignores dialogue/narration intelligibility in a sound-heavy plan;
- tells the agent to bake all effects into one final mixed file when revision, localization, or sync work requires stems;
- omits meaningful non-speech captions for sounds that carry story or comprehension;
- gives only a list of generic SFX names without timing, sync, perspective, material, or purpose;
- relies on EVAL-style answer-key leakage or mentions this evaluation file as something a production agent should read.

## Knowledge questions

### 1. What is the purpose of a spotting pass?

Expected answer: A spotting pass reviews the picture/script before creation to identify audible events, timecodes, priorities, sync strictness, perspective, source/rights plan, and emotional/narrative purpose. It prevents overfilling the cut and guides generation, library search, recording, editing, and mix handoff.

Required points:

- mentions timecoded review before sound creation;
- includes prioritization, not merely inventory;
- connects spotting to sync, source/provenance, and mix handoff;
- recognizes intentional silence or omission as valid.

Penalize: "Add sound to everything visible"; no mention of timecodes or priority.

### 2. Distinguish Foley from broader sound effects or designed sound.

Expected answer: Foley is performed/created to match on-screen human/object action such as footsteps, cloth, and prop handling; broader sound effects may include edited library recordings, ambience, impacts, vehicles, UI, or designed synthetic layers. Designed sound can be conceptual and layered rather than a literal performed reproduction.

Required points:

- feet/cloth/props or everyday action examples;
- sync-to-picture emphasis;
- broader effects/design distinction;
- accepts overlap in real workflows.

Penalize: treating Foley as all audio; treating Foley as only footsteps.

### 3. What should a sound generation prompt include?

Expected answer: Duration, loopability, visual sync cue, source/material, performance intensity, perspective/distance, environment, layer role, emotional job translated into audible properties, avoid list, and delivery/stem specs.

Required points:

- includes duration and sync;
- includes material and perspective;
- includes negative constraints such as no music/no dialogue/no clipping when relevant;
- includes handoff format or stem consideration.

Penalize: only adjectives like "cinematic" or "epic."

### 4. Why is provenance necessary for sound assets?

Expected answer: Sound assets need rights and revision traceability. A ledger should capture source, license/terms URL, attribution, commercial-use status, modification/adaptation rights, platform/territory restrictions, verification date, and approval status.

Required points:

- license/terms and attribution;
- commercial-use and derivative/adaptation checks;
- source/provenance per asset;
- recognizes platform-specific limitations.

Penalize: "Use any free sound library."

### 5. How should loudness be handled?

Expected answer: Use the delivery spec for the platform/client/context. ITU-R BS.1770-style loudness/true-peak measurement is a common measurement basis; EBU R 128 and Netflix specs are context-specific examples, not universal targets. If no spec exists, create a conservative rough mix and disclose that it is not a formal master.

Required points:

- no universal target;
- mentions loudness and true peak measurement;
- differentiates broadcast/platform/client specs;
- flags rough/unmastered when appropriate.

Penalize: always saying -14 LUFS, -16 LUFS, -23 LUFS, or -27 LKFS without context.

### 6. What non-speech sounds should be captioned?

Expected answer: Caption meaningful non-speech audio that conveys story, emotion, offscreen action, warnings, speaker/music context, or comprehension-critical information. Do not caption every incidental rustle if it is not meaningful. Keep labels concise and consistent.

Required points:

- meaningful non-speech sounds;
- consistency and concision;
- distinguishes important vs incidental sounds;
- ties to accessibility/comprehension.

Penalize: captions only dialogue; captions every tiny sound indiscriminately.

## Production-decision scenarios

### Scenario A: 30-second SaaS product ad

User request: "Make this screen-demo ad feel more premium with sound. It has narration, cursor clicks, dashboard cards sliding in, an error state, then a success state."

Strong response should:

- prioritize narration intelligibility;
- create a small UI/product palette: click, slide, error, success, possibly completion flourish;
- specify restrained, clean, non-arcade sounds;
- avoid real OS notification sounds and emergency-like alarms;
- use ducking or frequency restraint under voice;
- provide stems or separate one-shots;
- caption meaningful error/success cues if they convey state;
- include provenance/licensing plan.

Poor response:

- adds loud whooshes to every card;
- uses familiar iPhone/Mac/Windows sounds;
- ignores narration;
- exports one flattened mix with no UI stem.

### Scenario B: Animated explainer for children

User request: "Add fun Foley and sound effects to a 90-second educational animation about volcanoes."

Strong response should:

- spot key educational and comedic beats rather than every motion;
- use child-safe levels and avoid painful startling impacts;
- support narration clarity;
- design gentle lava bubbles, rock rumbles, drawing/diagram sounds, and character Foley;
- avoid realistic emergency sirens unless carefully justified;
- caption meaningful sounds like eruption rumble or warning tone if comprehension-critical;
- propose review on small speakers/headphones.

Critical risks:

- excessive sub-bass or jump scares;
- masking educational voiceover;
- scary disaster sounds that conflict with age/tone.

### Scenario C: Horror trailer

User request: "Sound-design a 45-second horror trailer from generated clips."

Strong response should:

- use silence/near-silence, subjective tones, distant ambiences, reverse swells, impacts, and controlled stingers;
- make a beat-by-beat hierarchy so only major reveals get maximum impact;
- specify perspective and materials for doors, footsteps, breath, cloth, creature pass-bys;
- include safety note about startle spikes/headphone playback;
- separate trailer hits, ambiences, Foley, and music;
- warn against copying recognizable horror trailer sounds or franchise motifs.

Poor response:

- says "add scary music and loud bangs everywhere";
- no timecoded plan;
- no safety or rights checks.

### Scenario D: Generated game trailer

User request: "Create sound prompts for a 20-second trailer of a magic combat game."

Strong response should:

- separate linear trailer needs from actual interactive implementation;
- design layers for spells: transient, body, tail, low-end, particles, material/element identity;
- differentiate player action, enemy attack, UI confirmation, impacts, and ambience;
- avoid overusing full-range impacts;
- request clean one-shots/stems and possibly loopable ambience;
- specify no copyrighted game sounds or recognizable franchise-like assets.

Bonus:

- suggests variations for repeated attacks so the trailer does not sound copy-pasted.

## Applied tasks and rubrics

### Task 1: Produce a spotting list and sound plan

Prompt to evaluated agent:

"I have a 15-second vertical product launch video: 0-3s black screen with a thin line of light, 3-6s macro shot of a matte-black charging case opening, 6-9s earbuds levitate out, 9-12s UI app card shows noise cancellation turning on, 12-15s logo lockup. Give me a sound design plan."

Expected approach:

- timecoded spotting list;
- premium product Foley for hinge/case/material;
- levitation designed sound, not generic magic;
- UI cue for noise cancellation;
- restrained reveal/logo hit;
- ambience/air bed;
- narration/music considerations if present;
- rights/source and stem handoff notes;
- QA for harsh highs, sub, and platform playback.

Scoring, 20 points:

- 5 timecoded, prioritized spotting;
- 4 material/perspective specificity;
- 4 product/UI palette coherence;
- 3 mix/handoff/stem plan;
- 2 rights/provenance;
- 2 QA/accessibility.

Critical failure: using a real Apple/Samsung/OS notification or copied brand sound.

### Task 2: Write sound generation prompts

Prompt to evaluated agent:

"Write prompts for the three most important sound assets in a cinematic AI scene: a glass orb cracking in a character's hand, a portal opening behind them, and a hard cut to silence after the portal swallows the room."

Expected approach:

- three separate prompts, not one full mix;
- exact-ish durations;
- sync trigger;
- materials: glass, hand, energy/air/space;
- close perspective for orb, larger spatial perspective for portal;
- silence treated as an edit/mix decision with optional tail cutoff;
- negative constraints: no music/dialogue, no clipping, avoid cliché if relevant;
- layer thinking.

Scoring, 15 points:

- 3 separate asset strategy;
- 3 sync/duration clarity;
- 3 material/perspective detail;
- 3 emotional/story role;
- 2 avoid constraints;
- 1 handoff/variation note.

### Task 3: Diagnose a bad mix

Prompt to evaluated agent:

"The client says the sound pass feels fake and tiring. Foley is late, UI beeps are annoying, the voiceover is hard to understand, and the ambience loop is obvious. What do you do?"

Expected approach:

- diagnose by muting/soloing layers rather than regenerate all;
- nudge Foley to visual contact transients;
- soften/shorten UI cues and reduce harsh frequencies/repetition;
- duck/lower music/FX or carve masking ranges around voice;
- lengthen/replace/crossfade ambience loop and remove repeated identifiable details;
- check phone/laptop/headphones;
- document changes and keep stems.

Scoring, 15 points:

- 3 systematic diagnosis;
- 3 sync repair;
- 3 UI repair;
- 3 intelligibility repair;
- 2 ambience repair;
- 1 QA/handoff.

### Task 4: Rights and accessibility review

Prompt to evaluated agent:

"A teammate used five downloaded 'free' sounds, two Freesound clips marked CC BY-NC, one YouTube Audio Library effect, and a ripped Netflix trailer boom. The final is a paid ad. Review the risk."

Expected approach:

- flags ripped Netflix trailer boom as unacceptable/replace;
- flags CC BY-NC as incompatible with a paid ad unless separate permission is obtained;
- says "free" needs actual license terms and provenance;
- notes YouTube Audio Library terms are platform-specific and should be verified for the intended distribution;
- requires attribution where applicable;
- creates a replacement plan using generated/original/cleared/commercial assets;
- includes rights ledger fields;
- checks captions for meaningful sounds.

Scoring, 20 points:

- 5 identifies commercial-use/license risks;
- 4 rejects ripped/copyrighted audio;
- 3 handles platform-library limitations carefully;
- 3 proposes replacement and provenance plan;
- 3 covers attribution/derivative verification;
- 2 accessibility/caption note.

Critical failure: approves the ripped trailer boom or CC BY-NC paid-ad use without permission.

## Overall quality indicators

Excellent answers:

- sound like a supervising sound editor giving actionable direction;
- translate emotion into audible properties;
- include time, sync, perspective, material, and mix priority;
- separate stems and preserve revision paths;
- handle legal/accessibility/technical constraints without derailing creativity;
- distinguish documented facts from heuristics when making broad claims;
- tailor the approach to genre and deliverable.

Weak answers:

- over-index on generic prompt adjectives;
- treat music as the whole soundtrack;
- ignore ambience and silence;
- ignore rights and captioning;
- provide no timecode or no sync detail;
- lack a repair strategy.
