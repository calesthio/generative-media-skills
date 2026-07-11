---
name: elevenlabs-music
description: Generate and iterate music with ElevenLabs Eleven Music for production deliverables. Use when planning, prompting, API-calling, editing, inpainting, reviewing, or licensing AI-generated songs, instrumental beds, ad music, soundtrack cues, video-to-music scores, stems, or music assets using the ElevenLabs Music API or ElevenCreative Music product.
---

# ElevenLabs Music production skill

Use this skill to turn a content brief into a usable music asset with ElevenLabs Eleven Music. Treat it as a production workflow: choose the right generation route, write legally safe musical direction, preserve artifact custody, and review the result against the edit before publishing.

Source-backed facts in this skill were verified on 2026-07-10 from official ElevenLabs documentation and terms. Re-check live docs before relying on pricing, limits, model defaults, licensing terms, or endpoint schemas in a paid or public production.

## Hard boundaries before prompting

Do not submit prompts, lyrics, references, uploads, or metadata that name or clearly target a protected work or identifiable artist. ElevenLabs Music Terms prohibit Music inputs that include any artist real/stage name, songwriter real/stage name, song title, album title, music publisher name, label name, or substantial/distinct song lyric excerpt intended to reference a song. They also prohibit prompting likely infringement and misleading mimicry of an identifiable recording artist.

Use genre, era, region, instrumentation, production language, tempo, mood, arrangement, mix references, and functional intent instead:

- Unsafe: "Make it sound like [artist]'s [song title]."
- Safer: "late-1970s glossy disco-pop, four-on-the-floor drums, octave bassline, bright string stabs, celebratory chorus, 118 BPM, no artist imitation."
- Unsafe: "Write a hook like this copyrighted lyric line..."
- Safer: "uplifting two-line chorus about starting fresh, original lyrics only."

For commercial release, check the active plan and Music Model-Specific Terms. As verified 2026-07-10, self-serve plans differ by generation/download limits, attribution, streaming rights, API features, concurrency, and permitted media. Self-serve media rights were documented as allowing online/offline commercial use except film, TV, radio, and Studio Games; Enterprise Music was documented as allowing all online/offline commercial use. Do not imply a client has broadcast, film, TV, Studio Games, reseller, or music-library/repository rights unless their plan/contract explicitly grants them.

## Capability snapshot

Documented Eleven Music capabilities include text-to-music generation, optional vocals or instrumental output, multilingual lyrics, section/lyric editing, composition plans, inpainting with `music_v2`, video-to-music, upload for inpainting, and stem separation. API access is for paid users.

Key API facts verified 2026-07-10:

- Basic compose endpoint: `POST /v1/music`.
- Detailed compose endpoint: `POST /v1/music/detailed`, returning audio plus composition plan and song metadata.
- Composition-plan endpoint: creates a plan without generation cost, though rate limits apply.
- Video-to-music endpoint: accepts up to 10 videos, total combined video size up to 200 MB, and total video duration up to 600 seconds.
- Prompt and `composition_plan` are mutually exclusive in compose calls.
- `music_length_ms` with prompt generation accepts 3,000-600,000 ms.
- Official duration documentation was not perfectly aligned: the API reference documented 3,000-600,000 ms for `music_length_ms`, while the overview and pricing pages also described a 5-minute generation/duration limit. Verify live account/API behavior before promising a cue longer than 5 minutes.
- `prompt` accepts up to 4,100 characters.
- `model_id` values documented for music include `music_v1` and `music_v2`.
- On the overview page, `music_v2` was documented as the UI default while API default remained `music_v1` during a transition period. Set `model_id` explicitly instead of depending on defaults.
- Default `output_format="auto"` selects MP3 format according to the model: documented as `mp3_44100_128` for v1 and `mp3_48000_192` for v2.
- `seed` can improve consistency with the same parameters, but exact reproducibility is not guaranteed and outputs may change across system updates.
- `force_instrumental=true` guarantees an instrumental result with prompt generation and cannot be used with composition plans.
- API pricing was documented as $0.15/minute for Eleven Music on the API pricing page. Confirm before estimating cost.

## Choose the generation route

For fast creative exploration, use a prompt with explicit duration and `model_id="music_v2"` unless a project requires v1 compatibility. Ask for 2-4 variants when using the web UI; with API, create separate generations and track seeds, prompt versions, and selected take.

For an edit-locked cue, use a composition plan. Plans give explicit chunk durations, section labels, lyrics placement, positive styles, negative styles, and context adherence. Use plans when the cue must hit voiceover gaps, chapter changes, trailer beats, looping regions, or a precise chorus/outro.

For scoring an existing cut, use video-to-music when the footage itself should guide the background music. Still provide a concise `description` and up to 10 style tags so the model understands brand tone and edit purpose. Combine videos beforehand when possible to reduce request duration and avoid ordering mistakes.

For revision after a good take, use `music_v2` inpainting instead of regenerating the entire song. Generate with `store_for_inpainting=true` or upload an owned/non-infringing file, keep good slices as audio-reference chunks, and regenerate only weak sections.

For mix control, request or derive stems when you need to duck vocals under narration, remove drums during dialogue, create a social cutdown, or hand off to a sound mixer. Expect high latency on stem separation for longer files.

## Prompt construction

A strong Eleven Music prompt answers five questions in musical language:

1. What is the asset for? State the production function: "15-second pre-roll ad bed," "loopable game menu music," "60-second explainer background under narration," "end-card sting."
2. What should the audience feel? Use emotional and tonal words, not just genre names.
3. What should be heard? Specify instrumentation, rhythm section, tempo/BPM range, key or harmonic color when useful, vocal presence, and mix density.
4. How should it move over time? Include structure, transitions, rise/fall, drops, breaks, stingers, or section timing.
5. What must not happen? Add negative direction such as no vocals, no busy lead melody, no copyrighted references, no harsh cymbals, no sudden ending, no artist imitation.

ElevenLabs' best-practices docs state that high-level intent prompts can work, but production prompts should still include constraints that protect the edit: duration, vocal policy, density under dialogue, timing cues, and deliverable context.

Use "instrumental only" in the prompt and `force_instrumental=true` for prompt-based API calls when vocals would conflict with narration. If lyrics are acceptable, provide original lyrics and timing cues such as "lyrics begin at 15 seconds" or "instrumental only after 1:45." When lyrics are not provided, the model may generate structured lyrics that match the prompt and duration.

For isolated elements, use targeted phrasing: "solo piano," "solo nylon-string guitar," or "a cappella female vocal texture." For a full mix, specify that those elements should sit inside a full arrangement.

## Composition plan guidance

Use `music_v2` chunk-style plans for most production work. A plan can contain up to 30 chunks. Generation chunks include:

- `text`: section label in square brackets, original lyrics, or inline directions.
- `duration_ms`: 3,000-120,000 ms for each generation chunk.
- `positive_styles`: up to 50 style/direction terms.
- `negative_styles`: up to 50 terms to avoid.
- `context_adherence`: `high`, `medium`, or `low`.
- Optional `conditioning_ref` and `condition_strength` for reference-conditioned regeneration.

The first chunk strongly sets the overall tone. Give early chunks at least 6-7 concrete style terms until the direction is established. Use `context_adherence="high"` for seamless edits and `medium` or `low` only when a section should noticeably change.

Audio-reference chunks preserve slices of a stored song unchanged:

```json
{
  "song_id": "stored_song_id",
  "range": { "start_ms": 0, "end_ms": 30000 }
}
```

Conditioning references can guide a generation chunk; the documented maximum conditioning reference length is 30 seconds. Use `condition_strength` `low`, `medium`, `high`, or `xhigh` depending on how tightly the new chunk should follow the stored source.

## Workflow for a real production

Start with a music brief:

- deliverable and platform;
- exact duration or edit timecode map;
- whether the track sits under narration/dialogue;
- instrumental/vocal policy;
- brand tone and audience;
- energy arc by section;
- forbidden references, industries, and rights constraints;
- target loudness/format needs for the downstream editor.

Then run this loop:

1. Rights and safety check: remove artist/song/title/label/publisher names and copyrighted lyric fragments. Confirm the client plan permits the intended distribution.
2. Route choice: prompt, composition plan, video-to-music, inpainting, upload, or stems.
3. Generate short first when possible. For songs, start with a 10-30 second proof of the core texture or a composition plan preview, then scale to the full duration after the direction is approved.
4. Log every request: model, endpoint/tool, prompt or plan, duration, seed if used, output format, time, cost estimate, and resulting file path.
5. Review in context, not solo. Place the track under the edit/narration and test whether it supports the story without stealing attention.
6. Revise surgically. If 80% works, inpaint or regenerate chunks; do not burn budget re-rolling the whole track unless the premise is wrong.
7. Freeze assets. Store the final audio, prompt/plan, metadata, license/plan notes, and QA notes together.

## QA checklist

Before handing off an ElevenLabs Music asset, verify:

- The track duration matches the edit within the allowed tolerance.
- Instrumental/vocal policy is correct.
- No artist, song, label, publisher, or copyrighted lyric reference appears in prompts, metadata, filenames, or lyrics.
- The generated lyrics, if any, are original, pronounceable, non-infringing, and suitable for the brand.
- The arrangement leaves room for dialogue/voiceover: no lead vocal or busy midrange during speech.
- Transitions, drops, stingers, and endings hit the required beats.
- Loops crossfade cleanly or have a purpose-built glue/transition chunk.
- Stems or alternate mixes exist when the editor needs dialogue ducking, no-drums, instrumental, or social cutdowns.
- Output format and sample rate fit the delivery pipeline; convert downstream copies as needed, but keep the original generated master.
- The active ElevenLabs plan/contract permits the intended use, including streaming, ads, games, broadcast, or client distribution.
- The project record includes source docs verification date for volatile terms.

## Common failure modes and fixes

- Vocals appear in background music: regenerate with `force_instrumental=true` for prompt mode, add "instrumental only," add "no vocals, no lyrics, no choir, no vocal chops," or use stems to remove/duck vocal content if the track is otherwise strong.
- Track is too generic: add production details, specific instrumentation, tempo range, mix texture, rhythmic pattern, section arc, and platform purpose instead of only a genre.
- Track imitates a known artist too closely: stop using it, rewrite the prompt to describe broad musical traits, and regenerate. Do not try to publish a near-mimic.
- Wrong section timing: switch to a composition plan with explicit chunk durations. For `music_v2`, section durations are enforced in composition plans.
- Great intro, weak outro: generate/store with inpainting support, keep the intro as an audio-reference chunk, regenerate the outro with a new generation chunk.
- Dialogue is masked: reduce density in the prompt, request fewer midrange leads, create stems, or ask for a sparse underbed with soft percussion and no lead melody during voiceover sections.
- Bad prompt or bad composition plan error: treat ElevenLabs' returned suggestion as a compliance rewrite, then inspect it for musical intent before regenerating. Harmful-material errors may not include a suggested replacement.
- Costs rise unexpectedly: shorten tests, use composition-plan creation before audio generation, avoid uploading copyrighted material for inpainting, and confirm current pricing.

## Example: 30-second SaaS launch ad bed

Production intent: Create a paid-social music bed that supports a crisp voiceover and lands a product reveal at 24 seconds.

Route: `POST /v1/music` or SDK `music.compose`; prompt mode is enough because the structure is simple. Use `force_instrumental=true`.

Example prompt:

```text
30-second instrumental-only music bed for a polished SaaS launch ad. Confident, modern, optimistic, and premium without sounding corporate-stale. Start with muted pulsing synth bass and soft tick percussion under voiceover. Add warm analog pads at 8 seconds, subtle handclap groove at 14 seconds, and a clean uplifting product-reveal lift at 24 seconds. 112-118 BPM, tight low end, bright but not harsh, no vocals, no lyrics, no vocal chops, no busy lead melody during narration, no artist imitation, no copyrighted references. End with a short resolved logo sting.
```

Example API parameters:

```json
{
  "model_id": "music_v2",
  "music_length_ms": 30000,
  "force_instrumental": true,
  "output_format": "auto"
}
```

Expected review: The track should be sparse in the midrange until the reveal, feel polished at mobile-speaker volume, and have a usable final sting. If the model creates an intrusive hook, regenerate with stronger negative styles around lead melody and vocal-like synths.

## Example: edit-locked trailer cue with a composition plan

Production intent: Score a 60-second cinematic product trailer with hard beats at 0:18, 0:38, and 0:55.

Route: composition plan with `model_id="music_v2"` so timing is explicit.

Example composition plan:

```json
{
  "chunks": [
    {
      "text": "[Cold Open]",
      "duration_ms": 18000,
      "positive_styles": [
        "cinematic",
        "minimal low strings",
        "subtle clock-like percussion",
        "tense",
        "premium technology",
        "80 BPM",
        "dark spacious mix",
        "slow riser"
      ],
      "negative_styles": ["vocals", "lyrics", "rock drums", "comic", "bright pop"],
      "context_adherence": "high"
    },
    {
      "text": "[First Reveal]",
      "duration_ms": 20000,
      "positive_styles": [
        "larger hybrid orchestra",
        "deep braam accent at the start",
        "pulsing synth bass",
        "controlled intensity",
        "wide percussion",
        "rising brass swells"
      ],
      "negative_styles": ["busy melody", "sung vocals", "cheerful"],
      "context_adherence": "high"
    },
    {
      "text": "[Final Build]",
      "duration_ms": 17000,
      "positive_styles": [
        "accelerating percussion",
        "heroic but restrained",
        "layered strings",
        "sub-bass pulses",
        "big hit at final second"
      ],
      "negative_styles": ["fade out too early", "lyrics", "soft ending"],
      "context_adherence": "high"
    },
    {
      "text": "[Logo Sting]",
      "duration_ms": 5000,
      "positive_styles": ["short resolved logo sting", "clean tail", "premium"],
      "negative_styles": ["new melody", "vocals", "long unresolved reverb"],
      "context_adherence": "high"
    }
  ]
}
```

Expected review: Confirm the edit points hit, then inpaint only the weak chunk if the overall sonic identity works.

## Example: video-to-music for a montage

Production intent: Generate background music that follows a 75-second travel montage without manually timecoding every cut.

Route: video-to-music with the final locked reference video. Combine clips in order before uploading when possible.

Example request fields:

```json
{
  "description": "Instrumental background score for a warm, cinematic travel montage. Starts intimate and curious, grows into open-road optimism, then resolves gently for an end card. Leave room for natural location sound and occasional captions.",
  "tags": ["cinematic", "warm", "instrumental", "travel", "optimistic", "acoustic", "soft percussion"],
  "model_id": "music_v2",
  "output_format": "auto"
}
```

Expected review: The score should follow broad visual energy but may not perfectly hit every cut. If exact hit points matter, move to a composition plan using the edit timecode map.

## Example: inpaint a stronger ending

Production intent: Keep the first 45 seconds of an approved track, replace a weak ending with a cleaner CTA sting.

Route: generate or upload a stored song, then pass a mixed audio-reference/generation plan to `music.compose` with `model_id="music_v2"`.

Example plan:

```json
{
  "chunks": [
    {
      "song_id": "stored_song_id",
      "range": { "start_ms": 0, "end_ms": 45000 }
    },
    {
      "text": "[CTA Ending]",
      "duration_ms": 12000,
      "positive_styles": [
        "same premium electronic palette",
        "clean rising transition",
        "confident final logo sting",
        "short reverb tail",
        "instrumental"
      ],
      "negative_styles": ["new genre", "vocals", "lyrics", "messy cymbals", "fade out"],
      "context_adherence": "high"
    }
  ]
}
```

Expected review: The splice should feel intentional. If the regenerated ending ignores the original palette, add a `conditioning_ref` from the last 10-20 seconds of the stored source and use `condition_strength="high"`.

## Source notes

Official sources verified 2026-07-10:

- Eleven Music overview: https://elevenlabs.io/docs/overview/capabilities/music
- Music API quickstart: https://elevenlabs.io/docs/eleven-api/guides/cookbooks/music
- Music prompting best practices: https://elevenlabs.io/docs/overview/capabilities/music/best-practices
- Composition plans guide: https://elevenlabs.io/docs/eleven-api/guides/how-to/music/composition-plans
- Music inpainting guide: https://elevenlabs.io/docs/eleven-api/guides/how-to/music/inpainting
- Compose, detailed compose, composition-plan, video-to-music, upload, and stem-separation API reference pages under https://elevenlabs.io/docs/api-reference/music/
- API pricing: https://elevenlabs.io/pricing/api
- Music Terms: https://elevenlabs.io/music-terms
- Eleven Music Model-Specific Terms: https://elevenlabs.io/eleven-music-model-specific-terms
- Prohibited Use Policy: https://elevenlabs.io/use-policy
