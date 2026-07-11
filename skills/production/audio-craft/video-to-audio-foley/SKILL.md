---
name: video-to-audio-foley
description: "Use for video-conditioned audio and automated Foley production: adding synchronized sound effects, ambience, impacts, footsteps, cloth, prop, and environmental audio to silent or under-sounded video using video-to-audio models, text-to-sound tools, manual spot lists, editing, rights checks, and QA."
---

# Video-to-audio Foley

Use this skill to turn a silent, generated, animated, game, ad, social, or edit-ready video clip into a credible sound-effects bed. Treat video-to-audio (V2A) as a production accelerator, not as a finished mix. The job is to decide what should be automated, what must be hand-spotted, how to prompt and segment the model, how to preserve sync, and how to verify the result against the picture.

## Boundaries

Use automated V2A when:

- the clip is short enough for the available model or can be divided into coherent beats;
- the target is a believable first-pass Foley bed, social clip, animatic, ad temp track, game prototype, or atmospheric pass;
- the visible action has obvious sound causes such as water, footsteps, vehicles, impacts, machinery, crowd, fabric, animals, weather, UI gestures, or prop handling;
- the user can accept iteration and editorial repair.

Do not rely on automated V2A alone when:

- frame-exact sync is mission-critical, such as rhythm games, trailers with hard cuts, slapstick hits, weapon impacts, or product demos where every click matters;
- the output must be delivered as clean reusable game assets or separated stems;
- the source video contains private people, unreleased product footage, client-confidential material, or copyrighted audio you are not allowed to upload to a hosted provider;
- the desired sound is an identifiable real person's voice, a copyrighted sound logo, a famous film/game sound, or a protected musical cue;
- the user needs final dialogue, lip-sync, narration, mix mastering, or music composition rather than Foley/sound effects.

If the user asks for "add sound to this video," first clarify whether they want:

1. a single mixed audio track attached to the video;
2. separate ambience / Foley / impacts / props / music stems;
3. isolated reusable sound assets for a game or library;
4. only a prompt/workflow, not generated media.

## What is documented versus heuristic

Facts below are source-verified as of 2026-07-10 unless a current project/tool registry says otherwise. Provider endpoints, model IDs, costs, licenses, duration limits, output formats, and commercial-use terms are volatile; re-check live docs before making paid calls or promising a deliverable.

Documented facts:

- Google DeepMind described V2A as research that combines video pixels with natural-language prompts to produce synchronized soundtracks, including sound effects, dialogue, and score-like audio. Do not assume public API access unless current tooling confirms it.
- fal `fal-ai/controlfoley` is documented as a hosted video-to-audio model for synchronized sound effects shaped by text prompts. Its API accepts `video_url`, optional `prompt`, `negative_prompt`, optional 2-4 second `reference_audio_url`, `duration`, inference controls, and seed; it returns a video with audio and a 44.1 kHz mono WAV audio file.
- fal `fal-ai/thinksound/audio` is documented as a hosted V2A endpoint that generates realistic audio from a video with an optional text prompt; if no prompt is provided, the prompt may be extracted from the video. Its schema includes `video_url`, `prompt`, `seed`, `num_inference_steps`, and `cfg_scale`, and returns an audio file plus the prompt used.
- MMAudio is a CVPR 2025 open-source model/repo that generates synchronized audio from video and/or text; its README says the default output/training duration is 8 seconds, larger deviations may reduce quality, the default CLI model is `large_44k_v2`, and the authors tested on Ubuntu.
- FoleyCrafter is an open-source video-to-audio framework that uses a text-to-audio base model with a semantic adapter and temporal controller; it supports text prompt and negative prompt control in its repo examples.
- HunyuanVideo-Foley is a Tencent open-source text-video-to-audio framework; its repo documents single-video and batch inference with `infer.py`, an audio description prompt, and XL/XXL model sizes. Check current license and model terms before commercial use.
- ElevenLabs Sound Effects is text-to-sound, not video-conditioned V2A. It is useful for manual Foley layers and ambience loops; docs describe duration control from 0.1 to 30 seconds, looping for seamless atmospheres, and prompt-influence control.
- FoleyBench frames V2A Foley quality as both semantic alignment with visible events and temporal alignment with event timing. Use both dimensions in QA.

Production heuristics:

- Prefer one broad V2A pass for continuous ambience and low-risk motion, then layer manual text-to-SFX or library effects for important transients.
- Split clips by acoustic scene, not by arbitrary equal lengths. A cut from subway platform to kitchen should be two generations even if the model accepts the full duration.
- If the model cannot accept explicit timecodes, put the timing discipline in the edit: generate candidates, align transients in the DAW/NLE, trim, crossfade, and layer.
- A good prompt describes the acoustic world, material, perspective, density, and exclusions. It is not just a list of visible objects.
- For social video, "believable and not distracting" usually beats maximum realism. For game assets and hero ads, separation, repeatability, and legal custody matter more than one-click convenience.

## Source-video preparation

Before generation:

1. Duplicate the source video and preserve the original.
2. Confirm the user has rights to upload/process the footage and to publish synthetic audio with it.
3. Remove or mute existing audio unless it is intentionally used as a reference and the provider permits it.
4. Trim to the natural acoustic unit: one action, one location, one camera beat, or one ambience zone.
5. Keep handles of 6-12 frames where possible so crossfades do not cut off attacks or tails.
6. Export a clean review file with stable frame rate, visible action, no burn-in UI that changes timing, and the same duration as the intended audio.
7. Note frame rate, timecode start, duration, target platform, and desired deliverable format.
8. If using a hosted provider that requires public URLs, upload only approved footage; avoid personal data, watermarked client content, unreleased products, or sensitive locations.

For clips longer than the model's reliable duration, segment by scene/action and plan overlap:

- 0.25-0.5 seconds overlap for ambience or crowds;
- 2-6 frames around hard impacts where transients must align;
- no overlap when a cut intentionally changes the acoustic space abruptly.

## Spot the video before prompting

Create a spot list even if the model can analyze the video. The spot list is the contract between picture, generation, edit, and QA.

Minimum fields:

- timecode in / out;
- visible cause or implied off-screen cause;
- sound role: ambience, footstep, cloth, prop, impact, vehicle, creature, UI, whoosh, room tone, crowd, mechanical, water, weather, musical sting;
- sync priority: hero, supporting, background, optional;
- acoustic perspective: close mic, camera perspective, distant, muffled, underwater, indoor reflective, outdoor open, phone speaker, helmet cam;
- production method: V2A pass, text-to-SFX, library, manual Foley recording, silence;
- notes on rights, taste, and exclusions.

Example spot list:

| Timecode | Visual event | Sound role | Priority | Method |
|---|---|---:|---:|---|
| 00:00.000-00:08.000 | Wet alley, neon signs, light rain | rain bed, city hum | supporting | V2A or looped ambience |
| 00:01.420 | Boot enters puddle | splash, leather creak | hero | generated SFX + manual sync |
| 00:03.100-00:05.700 | Coat swings while walking | cloth movement | background | V2A if natural, otherwise subtle library/recorded cloth |
| 00:06.040 | Metal door slams shut | impact, tail reverb | hero | separate SFX; align transient |

Mark silence intentionally. Not every visible movement needs sound; over-Foley makes AI clips feel fake.

## Prompt construction

Build prompts from these layers:

1. Scene bed: place, room size, weather, crowd, machine tone, distance.
2. Hero actions: the 1-4 events the viewer must notice.
3. Materials and mechanics: rubber on concrete, glass clink, leather creak, metal scrape, plastic button, wet gravel.
4. Perspective and mix density: camera-perspective, close and dry, distant and reverberant, subtle background, no music.
5. Exclusions: avoid narration, speech, melody, unrelated animals, wind roar, extra explosions, crowd applause, copyrighted motifs.
6. Timing hints only if the provider/model/tool accepts or benefits from them. If not, use short segments and edit sync manually.

Useful wording:

- "camera-perspective production audio"
- "subtle natural Foley, not exaggerated cartoon sounds"
- "dry close-up prop handling with small room reflections"
- "continuous low city ambience under sparse footsteps"
- "single hard ceramic impact at the cut, no music, no voice"
- "avoid extra off-screen events"

Avoid:

- "make it cinematic" without naming the actual acoustic events;
- "perfect sync" as a prompt-only promise;
- overloading a single generation with every micro-movement;
- asking for copyrighted sound-alikes, celebrity voices, or branded sonic logos;
- letting a model add music when the job is Foley.

## Provider and model selection

Always inspect the current tool registry, provider docs, licenses, pricing, input schema, and safety terms before choosing. Then pick based on the production need:

| Need | Good fit | Watchouts |
|---|---|---|
| Hosted V2A with text and negative prompt control | fal ControlFoley or current equivalent | Requires upload/URL; API details and commercial label are volatile; reference audio must be cleared. |
| Hosted V2A that can infer a prompt from video | fal ThinkSound or current equivalent | Generated prompt may misread intent; review and override the prompt for brand work. |
| Local/open-source reproducibility | MMAudio, FoleyCrafter, HunyuanVideo-Foley, ThinkSound local, or current open model | Check GPU/OS requirements, model license, checkpoint provenance, and duration assumptions. |
| High-priority transient or isolated prop | text-to-SFX, recorded Foley, or licensed library effect | Needs manual spotting and sync; may be better than V2A for clean stems. |
| Continuous ambience loop | text-to-SFX loop tool, library ambience, or V2A bed | Verify seamless looping and avoid audible repetition/pumping. |
| Generated video with native audio | an audiovisual video-generation model | Not the same as adding Foley to an existing edit; less post control and harder to preserve picture lock. |

Decision rule: choose the least magical tool that gives enough sync and control. If a simple text-to-SFX footstep plus a timeline nudge will beat a full V2A pass, use the simple path.

## Recommended workflow

1. Define deliverables.
   - final muxed video only, audio WAV, stems, SFX pack, project file, or all of these;
   - target platform loudness/format;
   - whether music, dialogue, or voiceover already exists.

2. Prepare and segment the video.
   - create silent working copies;
   - trim by acoustic scenes;
   - record exact durations and frame rate;
   - decide if hosted upload is allowed.

3. Make the spot list.
   - identify hero transients first;
   - mark ambience separately from Foley;
   - note sounds that are implied but not visible;
   - mark anything that should remain silent.

4. Generate a first V2A bed.
   - use one scene-level prompt per segment;
   - set seed and parameters if available;
   - request no music/no voice unless intentionally desired;
   - save raw outputs unchanged.

5. Review against picture.
   - mute/unmute with the video;
   - mark drift, wrong sources, excess events, and missing hero hits;
   - decide whether to regenerate, segment further, or replace with manual SFX.

6. Layer precision sounds.
   - generate or source isolated hits/foley for hero events;
   - align transients at the frame or waveform level;
   - shape with fades, EQ, reverb, pitch, and volume automation.

7. Build the mix.
   - keep V2A ambience low enough that manual hero sounds read clearly;
   - duck ambience under dialogue/voiceover;
   - use crossfades at segment joins;
   - avoid clipping and uncontrolled low-frequency buildup.

8. QA and package.
   - export preview video and separate audio/stems as requested;
   - preserve the source video, spot list, prompts, seeds, model IDs, provider, generation date, license notes, and raw generations;
   - document any manual edits and rejected generations.

## Sync and editing guidance

For hero impacts, sync by transients, not by prompt. A hit should land on the visual contact frame or the frame the edit implies as contact. If the sound blooms late, cut earlier attack from another take or layer a small click/thump on the contact frame.

For footsteps, do not chase every foot if the legs are small or obscured. Sync the first clear step, establish cadence, then let room tone and cloth sell the motion. If the model adds too many steps, use a narrower segment or replace with manual footsteps.

For cloth, keep it quiet and close. Loud cloth movement reads amateur unless the shot is an extreme close-up or animation exaggeration.

For props, name material and action: "ceramic mug placed on wooden desk," "plastic latch clicks twice," "paper envelope crinkles in hand." Generic "object sound" prompts produce mush.

For vehicles and machinery, separate continuous engine/room tone from discrete events such as ignition, brake squeal, gear shift, door slam, pass-by, or shutdown.

For UI/product demos, generated Foley is usually risky. Use designed clicks, taps, whooshes, and interface ticks as separate assets so they match brand taste and exact timing.

For animation, decide the sound world before generating. A realistic foley bed on a stylized cartoon may feel wrong; a hyperreal product sound on a flat motion graphic may feel premium.

## Rights, consent, and safety

Before upload or publication:

- verify source-video rights, talent releases, client permissions, and any location/product restrictions;
- verify the provider's current commercial-use and retention terms;
- treat reference audio as copyrighted unless the user proves clearance;
- do not clone, imitate, or synthesize a real person's voice without consent;
- do not recreate famous sound trademarks, sonic logos, game weapon sounds, film creature calls, or identifiable music cues;
- avoid adding deceptive sounds to news, legal, medical, security, or evidence footage unless clearly labeled as reconstruction or dramatization;
- preserve provenance so downstream editors know what is synthetic, generated, licensed, recorded, or client-provided.

If the user asks to add sounds that change the factual meaning of real footage, state the risk and propose labeling, abstaining, or making a clearly fictional edit.

## QA checklist

Semantic fit:

- Are the audible sources plausible for what is visible or intentionally implied?
- Did the model hallucinate animals, voices, crowds, music, machinery, or weather?
- Are material cues believable: metal, glass, cloth, water, wood, rubber, skin, plastic?

Temporal fit:

- Do hero hits land on contact frames?
- Do footsteps match cadence well enough for shot size?
- Is there drift across the segment?
- Do cuts and transitions reset the acoustic space cleanly?

Acoustic fit:

- Does reverb match the location and camera distance?
- Is the bed too dry, too wet, too loud, too clean, or too noisy?
- Do close sounds feel attached to the camera perspective?
- Are layers fighting in the same frequency range?

Technical fit:

- No clipping, crackle, dropouts, double attacks, codec smear, or obvious loops.
- Exports are the requested sample rate, channels, codec, and duration.
- Final video and audio durations match; no tail is cut unless intentional.
- Stems and project assets are named and stored with provenance.

Editorial fit:

- The audio supports the story rather than showing off generation.
- Important visual events are audible; unimportant movements are restrained.
- The mix leaves space for dialogue, music, captions, and platform playback.

## Troubleshooting

Wrong sound source:

- Add a negative prompt for the wrong source.
- Shorten the segment so the model sees fewer possible causes.
- Use manual text-to-SFX for the intended source and lower the V2A bed.

Poor timing:

- Segment around the event.
- Generate multiple seeds.
- Align in the timeline; layer a separate transient on the contact frame.
- Use a model or workflow with temporal/event control if available.

Mushy or overfull output:

- Prompt for fewer events and lower density.
- Remove music/voice/crowd unless needed.
- Split ambience and Foley into separate passes.
- EQ/duck the V2A bed under clean hero sounds.

Bad ambience loop:

- Generate a longer bed and find a cleaner loop point.
- Crossfade in a DAW/NLE.
- Use a dedicated looping text-to-SFX or library ambience instead.

Off-screen action missing:

- Add it explicitly to the prompt or create a manual layer.
- If the off-screen sound changes story meaning, confirm with the user.

Hosted upload blocked:

- Use a local/open model if rights and hardware allow.
- Ask the user for a cleared proxy video.
- Provide a spot list and prompt pack without uploading footage.

Commercial/licensing uncertainty:

- Stop before final delivery.
- Re-check current model/provider terms.
- Replace uncertain assets with recorded, licensed, or user-provided sounds.

## Complete example: skateboard social clip

Production intent: add believable sound to an 8-second vertical shot of a skateboarder rolling into a curb grind, landing, and rolling away. Deliverable is one mixed MP4 for social and a separate WAV.

Inputs and constraints:

- picture locked at 23.976 fps, 8.0 seconds;
- no dialogue or music;
- user owns the clip and approves hosted V2A upload;
- hero sounds are wheels, grind, landing thump, rolling tail.

Spot list:

| Timecode | Event | Priority | Method |
|---|---|---:|---|
| 00:00-00:08 | outdoor skatepark air, distant city, concrete space | supporting | V2A bed |
| 00:00.400-00:02.600 | wheels rolling on concrete | hero | V2A + possible wheel loop |
| 00:02.750-00:04.100 | trucks grind on concrete curb | hero | V2A plus isolated scrape if weak |
| 00:04.220 | board lands | hero | separate impact layer |
| 00:04.300-00:08.000 | roll away | supporting | V2A bed |

Example V2A prompt:

```text
Camera-perspective outdoor skatepark Foley, skateboard urethane wheels rolling on rough concrete, a sharp gritty truck grind on a concrete ledge, one solid board landing thump, then wheels rolling away. Natural documentary sound, dry open-air ambience, no music, no voice, no crowd cheering, no extra crashes.
```

Example negative prompt:

```text
music, narration, applause, crowd chanting, car horns, explosions, cartoon boings, extra falls
```

Example parameters when the selected provider supports them:

```yaml
duration_seconds: 8
seed: fixed_for_review_iteration
guidance: medium_to_high
output: raw_audio_wav_and_preview_video
```

Expected result: a usable continuous bed with skateboard movement broadly aligned. If the grind or landing is late, keep the ambience/roll bed, generate or source a separate metal/concrete scrape and landing thump, and align those transients manually.

## Complete example: product demo interface sounds

Production intent: add restrained premium UI sound to a 12-second SaaS app promo where a cursor clicks three buttons, cards slide in, and a success state appears. Deliverable is stems for editor handoff.

Why not one-click V2A: UI clicks must land exactly, be brand-consistent, and remain clean under voiceover. Use V2A only if the clip has environmental footage; otherwise build manual text-to-SFX and designed whooshes.

Spot list:

| Timecode | Event | Sound | Method |
|---|---|---|---|
| 00:01.120 | cursor clicks "Import" | soft glassy click | text-to-SFX or library |
| 00:02.000-00:03.200 | data cards slide in | short airy whoosh, quiet | designed SFX |
| 00:05.480 | toggle switches on | tactile tick | designed SFX |
| 00:09.900 | success state appears | small positive chime | generated or composed, cleared |

Example sound brief:

```text
Create four short, clean SaaS interface sound effects: soft glass click, airy card slide whoosh, tactile toggle tick, and tiny positive success chime. Minimal, premium, non-musical except the final two-note chime, no retro arcade, no phone notification resemblance, no branded sonic logo.
```

Expected result: separate WAV files placed on exact frames. QA requires checking the first sample of each click/tick against the cursor event and lowering all UI sounds under narration.

## Complete example: fantasy creature short

Production intent: add sound to a 10-second generated fantasy shot: a small dragon shakes rain from its wings, claws across wet stone, exhales steam, and jumps off-screen. Deliverable is a mixed preview plus stems.

Workflow:

1. Segment into two passes: continuous rain/cave ambience, then creature Foley.
2. Use V2A for atmosphere and broad creature movement.
3. Generate or record separate wing cloth/leather shake, claws on stone, breath, and jump thump.
4. Avoid famous dragon/monster sound references; design an original creature palette.

Example V2A prompt:

```text
Dark stone cave entrance in heavy rain, small fantasy reptile moving close to camera. Wet claws scrape and tap on stone, leathery wings shake off water droplets, soft animal breathing, a short warm steam exhale, then a quick leap away. Natural creature Foley, damp cave reflections, no music, no human speech, no roaring, no thunder.
```

Expected result: an atmospheric bed with plausible wet motion. For hero creature identity, layer original breath and wing textures rather than trying to make one model output carry the entire design.

## Source notes

Sources checked 2026-07-10:

- Google DeepMind, "Generating audio for video": https://deepmind.google/blog/generating-audio-for-video/
- fal ControlFoley model/API docs: https://fal.ai/models/fal-ai/controlfoley and https://fal.ai/models/fal-ai/controlfoley/api
- fal ThinkSound audio model/API docs: https://fal.ai/models/fal-ai/thinksound/audio/api
- MMAudio official repository: https://github.com/hkchengrex/MMAudio
- FoleyCrafter project and repository: https://foleycrafter.github.io/ and https://github.com/open-mmlab/foleycrafter
- HunyuanVideo-Foley official repository and paper: https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley and https://arxiv.org/abs/2508.16930
- ThinkSound official repository and paper: https://github.com/FunAudioLLM/ThinkSound and https://arxiv.org/abs/2506.21448
- ElevenLabs Sound Effects docs: https://elevenlabs.io/docs/overview/capabilities/sound-effects
- Sony AI FoleyBench publication page: https://ai.sony/publications/foleybench-a-benchmark-for-video-to-audio-models
