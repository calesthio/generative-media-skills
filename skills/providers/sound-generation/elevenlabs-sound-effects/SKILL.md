---
name: elevenlabs-sound-effects
description: Produce, direct, generate, QA, and integrate non-speech audio with ElevenLabs Text to Sound Effects / Sound Effects API. Use when an agent needs custom SFX, foley, ambience, loops, stingers, impacts, UI sounds, musical one-shots, trailer braams, or sound-design layers for video, ads, social edits, games, apps, podcasts, audiobooks, or interactive media using ElevenLabs.
---

# ElevenLabs sound effects

Use this skill to turn a production need into a usable sound asset: a clear sound-design brief, an ElevenLabs prompt, API settings, custody metadata, and QA notes that make the audio easy to place in an edit, game, app, or ad.

The subject is non-speech audio. Use a text-to-speech or voice skill for narration, dialogue, synthetic voices, dubbing, or voice cloning. Use a music-generation skill when the deliverable is a full song, score, or long-form bed. ElevenLabs Sound Effects can create short musical elements such as drum loops, brass stabs, risers, pads, and stingers, but do not treat it as a replacement for a full music composition workflow.

## Current documented facts

Treat this section as volatile. It was verified from official ElevenLabs documentation on 2026-07-10.

- API endpoint: `POST https://api.elevenlabs.io/v1/sound-generation`.
- Request body: `text` is required; `duration_seconds`, `prompt_influence`, `loop`, and `model_id` are optional.
- Default model ID: `eleven_text_to_sound_v2`.
- `loop` is documented as available only for `eleven_text_to_sound_v2`.
- API reference duration range: 0.5 to 30 seconds. The overview page also mentions 0.1 to 30 seconds, so prefer the stricter API-reference range unless a live call proves otherwise.
- `duration_seconds: null` or omitted lets ElevenLabs choose duration from the prompt.
- `prompt_influence` ranges from 0 to 1 and defaults to 0.3. Higher values follow the prompt more literally with less variation; lower values allow more creative variation.
- `output_format` is a query parameter formatted as `codec_sample_rate_bitrate`, e.g. `mp3_44100_128`. Higher-quality formats may require higher subscription tiers; the API docs state MP3 192 kbps requires Creator or above, and PCM 44.1 kHz requires Pro or above.
- The response is an audio file. Persist it immediately to a project asset path with metadata; do not leave it as an unnamed stream.
- The ElevenCreative playground creates four sound-effect candidates per generation and supports downloading MP3 44.1 kHz or WAV 48 kHz. The API reference describes a single audio response.
- Pricing is volatile. The API pricing page documented Sound Effects at `$0.120` per minute and says Sound Effects are metered per generation. Another ElevenLabs pricing page describes approximate credit cost as 200 credits per generation; reconcile against the user’s actual plan before budget-sensitive batch work.

Official sources:

- Sound Effects overview: https://elevenlabs.io/docs/overview/capabilities/sound-effects
- Sound Effects API reference: https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert
- Sound Effects quickstart: https://elevenlabs.io/docs/eleven-api/guides/cookbooks/sound-effects
- Sound Effects playground guide: https://elevenlabs.io/docs/eleven-creative/playground/sound-effects
- ElevenAPI pricing: https://elevenlabs.io/pricing/api
- ElevenLabs Terms: https://elevenlabs.io/terms-of-use
- ElevenLabs Prohibited Use Policy: https://elevenlabs.io/use-policy

## Decide whether ElevenLabs is the right tool

Use ElevenLabs Sound Effects when the asset can be described as an acoustic event, a texture, a short sequence, a loopable bed, or a one-shot:

- foley: fabric rustle, footsteps, key turn, phone drop, page flip, ceramic scrape;
- ambience: rain on a tin roof, neon alley hum, server room, forest at dusk, spaceship ventilation;
- cinematic design: braams, hits, whooshes, risers, tension pulses, sub drops, logo stingers;
- game/app UI: button tap, achievement sparkle, error buzz, inventory pickup, menu hover;
- social/video accents: transition whoosh, reveal sparkle, comedic record scratch, notification pop;
- short musical components: 90 BPM drum loop, vintage brass stab, synth pad swell, tonal riser.

Choose another route when:

- the sound must sync sample-accurately to a performance or already recorded impact; use foley recording, library search, or manual editing;
- the request requires a recognizable copyrighted sample, theme, logo sound, celebrity voice, or brand sonic mark without rights;
- the user needs a licensed stock-library asset with indemnity rather than generated audio;
- the sound must be physically exact, e.g. forensic, safety-critical, medical, or legal reconstruction;
- the need is a full score, song, or long loop with harmonic development; use a music workflow and reserve Sound Effects for stems or accents.

## Production workflow

1. Translate the user request into a sound-design brief.
   - Name the sound’s function: establish space, sell impact, transition, punctuate UI, intensify tension, cover an edit, or loop under action.
   - Capture where it will live: platform, scene, timecode, speaker target, mix context, and whether dialogue/music will compete.
   - Decide if the asset is a one-shot, sequence, loop, ambience bed, stem, or collection.

2. Choose generation settings before calling the API.
   - Use auto duration for exploratory ideation and natural one-shots.
   - Use explicit duration when syncing to a cut, animation, interaction, game event, or ad beat.
   - Use `loop: true` for ambience, room tones, machinery beds, weather, drones, menu music-like textures, and any asset intended to repeat.
   - Use `prompt_influence` around 0.25-0.4 for creative exploration, 0.45-0.7 for planned production assets, and 0.75-1.0 only when literal compliance matters more than pleasant variation.
   - Choose `mp3_44100_128` for quick previews or social drafts; choose PCM/WAV-style output when available for editing, game engines, archival masters, or heavy post-processing.

3. Generate in small batches with purposeful variation.
   - For a critical hero sound, create 3-6 candidates with controlled prompt variations rather than repeatedly using the same prompt.
   - Vary only one or two axes at a time: material, distance, room, intensity, transient shape, or tail length.
   - Save rejected candidates when useful; they may become layers.

4. Edit and integrate.
   - Trim leading silence and awkward tails.
   - Normalize loudness for the target context rather than simply maximizing volume.
   - Fade in/out ambience loops at zero crossings and test at least three repetitions.
   - Layer generated SFX with stock/recorded foley when a single generation lacks body, transient detail, or realism.
   - Keep dry and processed versions when the edit may change.

5. Record custody metadata.
   - Store prompt, settings, model ID, output format, generation date, source URL/API endpoint, account/license notes, and usage rights assumptions beside the asset manifest.
   - Mark whether the output is intended as standalone SFX, embedded in a larger work, or an internal draft.

## Prompt construction

Write prompts as production notes, not merely labels. A strong prompt usually specifies:

- source: what makes the sound;
- action: what happens over time;
- material: metal, wood, glass, fabric, gravel, water, plastic, rubber;
- environment: close studio, tiled bathroom, forest, warehouse, cockpit, cave, underwater;
- perspective: close-mic, distant, muffled, offscreen, first-person, wide cinematic;
- dynamics: soft, sharp, explosive, compressed, swelling, decaying, sparse, dense;
- duration intent: quick one-shot, 2-second whoosh, 12-second ambience, 30-second seamless loop;
- mix constraints: no music, no speech, no melody, low-end impact, high-frequency sparkle, mono-compatible;
- emotional role: ominous, playful, premium, tactile, futuristic, cozy, alarming.

Useful pattern:

```text
[source/action], [materials], [environment and perspective], [time structure], [mix/quality constraints], [emotional or functional role].
```

Do not over-pack prompts with mutually incompatible cues. If a sound must be both realistic foley and cinematic hyperbole, generate separate layers: one realistic transient, one designed tail, one sub impact.

### Prompting by asset type

For foley, emphasize material, contact, weight, and microphone distance:

```text
Close-mic foley of heavy leather gloves gripping and twisting a dry metal valve, small squeaks and gritty friction, no music, no voice, realistic studio recording.
```

For ambience, emphasize space, density, loopability, and foreground events:

```text
Seamless loop of a quiet cyberpunk alley at night, distant rain on metal awnings, soft neon electrical hum, occasional far traffic wash, no sirens, no voices, subtle and non-distracting.
```

For cinematic impacts, define transient, body, and tail:

```text
Massive cinematic trailer hit: sharp metal slam transient, deep sub boom body, long dark reverb tail, ominous sci-fi tone, no melody, no vocals, suitable for a title reveal.
```

For UI/game sounds, keep prompts short and functional:

```text
Premium mobile app success chime, short glassy sparkle with soft tactile click, under 0.6 seconds, friendly, clean, no melody phrase, no voice.
```

For musical elements, include tempo/key only when they matter:

```text
Old-school funky brass stabs from a vinyl sample, 88 BPM, F-sharp minor, short loopable stem, warm tape texture, no drums, no vocals.
```

## Parameter guidance

`duration_seconds`

- 0.5-1.0: UI click, error buzz, notification pop, button hover, camera shutter.
- 1-3: hits, whooshes, transitions, logo stingers, short foley actions.
- 3-8: multi-part foley sequences, impacts with tails, creature sounds, short risers.
- 8-15: establishing ambiences, machinery beds, weather snippets, tension textures.
- 15-30: loopable ambiences, background beds, game level atmospheres, long drones.

If a prompt describes a sequence with multiple events, allocate enough duration for each event and its tail. If the generated file feels rushed, increase duration before adding more words.

`prompt_influence`

- 0.2-0.35: use for ideation, textures, and happy accidents.
- 0.35-0.55: use for first production pass where style matters and variation is welcome.
- 0.55-0.75: use when the event order, material, or emotional target must be clear.
- 0.75-1.0: use sparingly for literal prompts; expect less variety and occasionally less organic sound.

`loop`

- Turn on for ambience, drones, room tones, machinery, weather, vehicle interiors, game menu beds, and any background layer that may repeat.
- Leave off for transient one-shots, impacts, UI sounds, sync whooshes, and foley sequences with a clear start/end.
- Always audition loop seams in the target engine or timeline. A model’s loop setting does not remove the need for editorial QA.

`output_format`

- Use MP3 for previews, fast review, chat handoff, and lower-stakes social assets.
- Prefer PCM/WAV-like formats when the asset will be processed, layered, mastered, edited frame-accurately, or imported into game audio middleware.
- Verify subscription tier before requesting premium formats. If the API rejects an output format, fall back to an available format and log the change.

## API lifecycle

Before generation:

- Confirm an API key is configured as a managed secret such as `ELEVENLABS_API_KEY`; never paste the key into logs, prompts, file names, or metadata.
- Verify plan/license requirements for commercial work, premium output formats, and expected batch volume.
- Estimate generations. Sound Effects pricing and included generations can change; check current pricing for budget-sensitive work.
- Create a deterministic output path under the active project, for example `assets/audio/sfx/scene-04-door-valve-v01.mp3`.

REST shape:

```bash
curl -X POST "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Close-mic foley of a heavy wooden door creaking open in a dusty hallway, slow hinge groan, no music, no voice",
    "duration_seconds": 3.0,
    "prompt_influence": 0.55,
    "model_id": "eleven_text_to_sound_v2",
    "loop": false
  }' \
  --output scene-02-door-creak-v01.mp3
```

Python SDK shape from the official quickstart:

```python
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
audio = client.text_to_sound_effects.convert(
    text="Cinematic braam, horror",
)

with open("cinematic-braam-v01.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

After generation:

- Write the file to the project asset directory immediately.
- Inspect actual duration, sample rate, channels, codec, and loudness with the local audio tools available in the host environment.
- Rename the final selected asset with a stable role-based name, not just a prompt slug.
- Store a sidecar or asset-manifest entry with prompt/settings/model/source/license notes.

## Safety, rights, and commercial-use checks

Do these checks before publishing or client delivery:

- Confirm the user’s ElevenLabs plan permits the intended commercial use. ElevenLabs Terms documented on 2026-07-10 allow commercial use for paid users and restrict free users to non-commercial purposes.
- Do not sell, license, or distribute generated Sound Effects output as standalone isolated files, sample packs, sound libraries, music/sound collections, or similar products. ElevenLabs Prohibited Use Policy specifically restricts standalone commercial exploitation of Sound Effects output.
- Do not use outputs or service access to build, train, test, or improve competing AI models or datasets.
- Do not request copyrighted, trademarked, celebrity, brand, game, film, or song-identifying sounds unless the user has rights. Use descriptive sonic traits instead of protected names.
- Avoid generating deceptive emergency alerts, public warning tones, official-sounding sirens, or realistic crisis sounds for contexts where listeners could be misled or harmed.
- Treat violent, horror, weapon, creature, and disaster SFX as fictional production assets; do not assist threats, harassment, intimidation, or real-world abuse.
- If the asset contains or resembles voices, speech, chants, names, or recognizable persons, re-evaluate under voice/impersonation rules and get rights/consent where needed.
- If the output will be used in advertising, games, children’s media, healthcare, public-sector, or regulated contexts, check current ElevenLabs policy and applicable local law.

## Sound QA checklist

Use ears first, then meters.

Creative fit:

- Does the sound communicate the intended object/action within one listen?
- Does it match scale, material, era, environment, and emotional tone?
- Does it support the cut rather than stealing attention?
- Does it avoid unintended speech, melody, brand resemblance, or comedic artifacts?

Technical fit:

- Check actual duration against the edit or interaction.
- Check leading silence and tail length.
- Check loop seams after at least three repetitions.
- Check clicks, pops, abrupt fades, warble, metallic AI smear, pumping, or low-end mud.
- Check mono compatibility for mobile/social and phase issues for game engines.
- Check loudness in context with dialogue, music, and platform playback.
- Check codec/sample rate meets the delivery target.

Integration fit:

- In video, audition against picture at final frame rate; impacts should land 0-2 frames early only if it improves perceived sync.
- In ads/social, test on phone speakers; many sub-heavy impacts disappear unless layered with midrange transient detail.
- In games, export clean one-shots and loop beds separately; leave headroom for middleware randomization, pitch variation, and distance attenuation.
- In podcasts/audiobooks, reduce high-frequency surprise and keep ambiences below narration priority.

## Iteration tactics

If the sound is too generic, add material, perspective, space, and function.

Weak:

```text
Magic sound.
```

Stronger:

```text
Short magical UI reward sparkle, tiny glass bells and soft dust shimmer, close and clean, under 1 second, premium mobile game, no voice, no melody.
```

If the sound is too busy, remove secondary events and lower prompt influence.

If the sound is too literal or dry, add room, tail, emotion, and lower prompt influence slightly.

If the sound misses timing, set `duration_seconds` explicitly and describe the timing structure: "quick attack, half-second swell, 2-second tail."

If the loop seam is noticeable, regenerate with `loop: true`, simplify foreground events, and avoid unique one-time transients.

If generated foley lacks realism, layer a generated designed element under a recorded or stock foley transient.

If low end overwhelms the mix, regenerate with "controlled low end, no sub boom" or EQ after generation; do not rely only on volume reduction.

## Complete examples

### Example 1: 15-second vertical ad transition kit

Production intent: create a small SFX kit for a premium skincare ad: three quick transitions, one product reveal sparkle, and one logo stinger. The edit has soft music and whispery narration, so SFX must be elegant and not harsh.

Workflow:

1. Generate each asset separately, not as one sequence.
2. Use MP3 previews for client review; regenerate or convert masters at higher quality if approved and available.
3. Keep prompt influence moderate because "premium" is subjective.
4. QA on phone speakers because the ad is for Reels/TikTok/Shorts.

Candidate calls:

```json
[
  {
    "filename": "sfx-transition-silk-whoosh-v01.mp3",
    "text": "Soft silk fabric whoosh for a luxury skincare video transition, close and airy, gentle high-frequency shimmer, under 1 second, no voice, no music, premium and clean",
    "duration_seconds": 0.8,
    "prompt_influence": 0.5,
    "loop": false,
    "model_id": "eleven_text_to_sound_v2",
    "output_format": "mp3_44100_128"
  },
  {
    "filename": "sfx-product-reveal-glass-sparkle-v01.mp3",
    "text": "Elegant product reveal sparkle, tiny glass particles and soft bell-like glint, close-mic, quick attack with smooth 1.5 second tail, no melody, no voice, refined luxury beauty ad",
    "duration_seconds": 2.0,
    "prompt_influence": 0.55,
    "loop": false,
    "model_id": "eleven_text_to_sound_v2",
    "output_format": "mp3_44100_128"
  },
  {
    "filename": "sfx-logo-stinger-soft-luxe-v01.mp3",
    "text": "Minimal luxury logo stinger, soft tactile click followed by warm airy shimmer, calm and expensive, no drums, no voice, no recognizable melody, suitable for final brand card",
    "duration_seconds": 2.5,
    "prompt_influence": 0.5,
    "loop": false,
    "model_id": "eleven_text_to_sound_v2",
    "output_format": "mp3_44100_128"
  }
]
```

Expected result: short, polished, high-frequency detail with no distracting musical phrase. Likely failures: harsh glass, too much melody, or assets that mask the narrator. Fix by adding "subtle, low volume, no bright piercing highs" or reducing duration.

### Example 2: Loopable sci-fi game ambience

Production intent: create a 30-second ambience loop for an abandoned spaceship corridor. It must sit under gameplay for minutes without obvious repetition.

Workflow:

1. Use `loop: true` and maximum duration for a less repetitive bed.
2. Keep foreground events sparse because unique alarms or footsteps reveal the loop point.
3. Generate alternate layers: base room tone, intermittent mechanical creak, distant energy pulse. Let the game engine randomize secondary layers.

Primary prompt:

```json
{
  "filename": "amb-spaceship-corridor-base-loop-v01.wav",
  "text": "Seamless 30-second loop of an abandoned spaceship corridor, low ventilation rumble, faint electrical buzz, distant hull stress creaks, dark spacious metal interior, no alarms, no voices, no footsteps, subtle and playable under exploration",
  "duration_seconds": 30,
  "prompt_influence": 0.62,
  "loop": true,
  "model_id": "eleven_text_to_sound_v2",
  "output_format": "pcm_48000"
}
```

Expected result: a dark loopable bed. Likely failures: obvious repeating clang, too much sub, or non-looping tail. Fix by simplifying foreground events, reducing prompt influence, or generating separate randomized one-shots for creaks.

### Example 3: Documentary foley replacement

Production intent: replace a noisy on-location close-up of a museum curator opening an archival box. The sound must feel real, quiet, and non-dramatic.

Workflow:

1. Generate a realistic layer with no cinematic language.
2. Use explicit duration matching the shot.
3. Keep generated audio quiet; do not normalize aggressively.
4. If needed, layer with a recorded room tone from the documentary.

Prompt:

```json
{
  "filename": "foley-archive-box-open-v01.mp3",
  "text": "Realistic close-mic foley of cotton-gloved hands opening an old cardboard archival box on a wooden table, soft paper friction, gentle lid scrape, quiet museum room, natural and understated, no music, no voice, no cinematic impact",
  "duration_seconds": 4.2,
  "prompt_influence": 0.7,
  "loop": false,
  "model_id": "eleven_text_to_sound_v2",
  "output_format": "mp3_44100_128"
}
```

Expected result: believable tactile foley. Likely failures: exaggerated creaks, room reverb, or too many handling sounds. Fix by reducing action count and specifying "single lid opening, no extra movements."

### Example 4: Game UI sound family

Production intent: create a coherent family for a cozy puzzle game: hover, select, error, reward. The sounds should share a soft wooden/toy-box identity.

Workflow:

1. Define a sonic palette first: felt, wood, tiny bells, warm room, no sharp digital beeps.
2. Generate short one-shots separately.
3. QA for fatigue by playing repeated interactions quickly.

Palette statement:

```text
Warm cozy puzzle UI, soft woodblock, felt dampening, tiny toy-bell accents, gentle room tone, no harsh beeps, no voices, no long melodies.
```

Prompts:

```json
[
  {
    "filename": "ui-hover-soft-wood-v01.mp3",
    "text": "Cozy puzzle game hover sound, tiny soft wood tap with felt damping, very short, warm and friendly, no beep, no voice",
    "duration_seconds": 0.35,
    "prompt_influence": 0.6,
    "loop": false
  },
  {
    "filename": "ui-select-toy-click-v01.mp3",
    "text": "Cozy puzzle game select sound, soft wooden toy click with small warm bell glint, under half a second, satisfying but gentle, no melody, no voice",
    "duration_seconds": 0.5,
    "prompt_influence": 0.6,
    "loop": false
  },
  {
    "filename": "ui-error-felt-thunk-v01.mp3",
    "text": "Cozy puzzle game invalid move sound, muted felt-covered wooden thunk, soft downward tone, not alarming, under 0.6 seconds, no voice",
    "duration_seconds": 0.6,
    "prompt_influence": 0.65,
    "loop": false
  },
  {
    "filename": "ui-reward-tiny-bells-v01.mp3",
    "text": "Cozy puzzle game reward sound, small wooden click followed by tiny warm bell sparkle, playful and soft, one second, no voice, no long melody",
    "duration_seconds": 1.0,
    "prompt_influence": 0.58,
    "loop": false
  }
]
```

Expected result: consistent UI family. Likely failures: reward becomes musical, error becomes too negative, hover too loud. Fix through post-gain and shorter durations as much as regeneration.

## Handoff format

When delivering generated or planned SFX to another agent or pipeline stage, include:

```json
{
  "asset_id": "scene-04-door-creak-v02",
  "role": "foley_sync",
  "file_path": "projects/example/assets/audio/sfx/scene-04-door-creak-v02.mp3",
  "provider": "ElevenLabs",
  "endpoint": "POST /v1/sound-generation",
  "model_id": "eleven_text_to_sound_v2",
  "prompt": "Close-mic foley of a heavy wooden door creaking open...",
  "settings": {
    "duration_seconds": 3.0,
    "prompt_influence": 0.55,
    "loop": false,
    "output_format": "mp3_44100_128"
  },
  "verified_date": "2026-07-10",
  "qa": {
    "duration_checked": true,
    "loop_checked": false,
    "loudness_checked_in_context": true,
    "rights_notes": "Paid-plan commercial use must be confirmed; do not distribute standalone."
  }
}
```

## Final reminder

The best generated SFX rarely come from one perfect prompt. Work like a sound editor: define the role, generate focused candidates, select by listening in context, trim and layer, and keep rights/custody notes with the asset.
