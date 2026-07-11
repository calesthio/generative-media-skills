---
name: sound-design-foley
description: Provider-independent sound design and Foley direction for generated media. Use when an agent must plan, prompt, source, generate, edit, mix, hand off, repair, or QA sound effects, Foley, ambience, impacts, transitions, UI/product audio, emotional sound design, or accessibility-safe captions for videos, ads, trailers, animation, avatar clips, explainers, games/trailers, product films, and social edits.
---

# Sound Design and Foley Direction

Use this skill to make generated media sound intentional instead of merely accompanied by music. Treat sound as story, timing, texture, space, and information. The goal is not to fill every frame with effects; it is to decide what the audience must feel, notice, understand, or believe at each moment, then design sounds that support that job.

## Evidence stance

Documented facts below are drawn from professional and standards sources verified on 2026-07-10:

- Berklee describes Foley artists as devising and recording everyday sounds for films, television, and video games, and notes that Foley work begins with a spotting session that catalogs needed effects before recording to picture.
- ITU-R BS.1770-5 specifies algorithms for measuring programme loudness and true-peak audio level; many platform specs derive from or reference ITU loudness methods.
- EBU R 128 recommends -23 LUFS for broadcast normalization in its domain, with EBU Mode momentary, short-term, and integrated metering.
- W3C WCAG guidance for prerecorded captions says captions include dialogue plus meaningful non-speech sound information.
- Section508.gov similarly says sounds needed to understand and enjoy synchronized media should be captioned, and that caption style should be consistent.
- Creative Commons licenses can permit reuse under defined conditions such as attribution, noncommercial limits, share-alike, or no-derivatives. These conditions must be checked per asset.
- YouTube Audio Library terms, verified on 2026-07-10, describe its music and sound effects as copyright-safe for YouTube use, while warning that only Audio Library assets are known to YouTube to be copyright-safe and that YouTube does not provide legal guidance for off-platform use.
- Freesound, verified on 2026-07-10, hosts Creative Commons-licensed sounds; some sounds cannot be used commercially and many require attribution.

Empirical observations are practical listening checks and workflow tests an agent can perform on the actual cut: muting layers, playing small speakers, measuring peaks, checking sync frame by frame, and comparing against references.

Production heuristics are experienced working rules. They are useful defaults, not universal laws. Override them when the brief, distribution spec, genre, accessibility need, or director preference requires it.

## First pass: spot the cut before creating sounds

Do a spotting pass from picture and script before prompting a sound provider, searching a library, or writing an edit plan.

Create a spotting list with one row per audible event or bed:

- timecode in/out or frame range;
- visual trigger, narrative beat, or interaction;
- sound family: dialogue-support, Foley feet, Foley cloth/moves, Foley props, designed effect, impact, whoosh/transition, ambience/room tone, UI/product, creature/vehicle/magic, musical sting, silence;
- diegetic status: inside the world, subjective/internal, interface/brand layer, or editorial punctuation;
- sync strictness: frame-locked, loose sync, rhythmic, background, or offscreen;
- perspective: macro/close, normal, distant, offscreen left/right, occluded, through wall/glass/helmet, underwater/phone/radio;
- material clues: shoe, floor, cloth, metal, paper, glass, plastic, liquid, skin, wood, dust, sand, snow, electronics;
- emotional job: trust, danger, speed, luxury, intimacy, comedy, scale, surprise, calm, unease;
- rights/source plan: record, synthesize/generate, licensed library, user-owned, public domain/CC-compatible, or needs clearance;
- mix priority: foreground, midground, background, subliminal, or mute.

Do not treat the spotting list as a shopping list where every visible action needs a sound. In short ads and social edits, too many literal sounds can fight the voiceover and music. Prioritize events that clarify causality, sell materiality, heighten rhythm, or carry emotional information.

## The sound families

### Foley feet

Use Foley feet for character presence, weight, pacing, surface, and scale. Specify:

- shoe or foot: sneaker, boot, heel, bare foot, paw, robot foot, tiny toy feet;
- surface: concrete, wet asphalt, dry leaves, polished wood, marble, carpet, gravel, snow, hollow metal;
- gait: cautious, hurried, confident, exhausted, comedic tiptoe, heavy landing;
- distance and room: close dry step, hallway slap, warehouse echo, distant upstairs thump;
- sync pattern: exact steps, partial sweeteners, or abstract rhythm.

Heuristic: when generated visuals show walking but the soundtrack is mostly narration, choose two or three anchor steps rather than a full step for every footfall.

### Foley cloth and moves

Use cloth/move sounds for human intimacy, performance, and animation believability. Include jacket rustle, backpack strap, cape sweep, leather creak, armor jingle, hair movement, sleeve brush, or body shift.

Heuristic: cloth should usually be felt more than noticed. If the viewer says "nice cloth sound," it is often too loud unless the fabric is the product.

### Foley props and hand interactions

Props sell contact. Specify object size, material, handling force, and hand state:

- ceramic mug set down gently on wood;
- phone lifted from desk, glass-on-wood tap plus tiny finger slide;
- cardboard box opened with tape peel and flap flex;
- premium pen click, cap twist, and paper drag;
- sword draw, key turn, latch, zipper, dish rattle, tool clack.

For product films, keep prop sounds clean and elevated. A luxury product usually wants fewer, more detailed sounds: micro-clicks, precise snaps, soft leather, smooth magnetic closures, controlled low-end sweeteners.

### Ambience and room tone

Ambience creates place and prevents dead air. Design ambience in layers:

- base bed: room tone, city air, office HVAC, forest bed, vehicle cabin, distant crowd;
- local details: neon buzz, bird, elevator ding, printer, distant siren, wind against window;
- time/weather: morning birds, night insects, rain roof, winter muffling, summer street;
- perspective: open exterior, small room, cavern, car interior, phone speaker, underwater;
- motion: static bed, evolving bed, passing element, entering/leaving space.

Heuristic: keep a very low-level continuous bed under scenes unless the intended effect is silence. Generated video often feels synthetic when every sound is an isolated one-shot with no air around it.

### Designed effects

Designed effects are not merely recordings; they are layered sounds that express a concept. Use them for sci-fi interfaces, magic, glitches, reveals, brand mnemonic sounds, abstract data flows, power-ups, drones, monsters, trailer moments, and emotional transitions.

Build a designed effect as layers with jobs:

- transient: click, snap, hit, spark, consonant-like start;
- body: tonal hum, motor, roar, whoosh, texture, pressure;
- tail: reverb, delay, debris, shimmer, reverse, decay;
- sub/weight: low thump or boom used sparingly;
- detail: grit, servo, sparkle, air, particles;
- perspective filter: muffled, phone, underwater, through helmet, far away.

Heuristic: if a sound is meant to feel huge, do not only add low end. Add contrast: small pre-click, silence before impact, wide air, debris tail, and a short drop in competing layers.

### Impacts, hits, and trailer punctuation

Impacts must follow picture energy and edit rhythm. Specify size, material, frequency range, and tail:

- soft UI tap, dry and close;
- medium punch, skin slap plus cloth movement, no exaggerated gore;
- product reveal hit, tight low thump plus elegant glass shimmer;
- trailer impact, sub drop, metal slam, air burst, long reverb tail;
- comedic impact, cartoon pop, hollow boing, or deliberately undersized knock.

Heuristic: reserve the largest impacts for the few moments that truly need them. A 30-second spot with 12 maximum hits becomes fatiguing and loses hierarchy.

### Transitions and whooshes

Transitions connect edits and motion. Match the whoosh to what the viewer sees:

- camera whip: airy stereo whoosh, fast attack, short tail;
- object pass: tonal Doppler or material-specific air;
- graphic slide: clean synthetic swish;
- glitch cut: digital tick, bit-crush, data tear;
- luxury dissolve: soft breath, silk sweep, tonal shimmer;
- horror reveal: reverse swell into low impact.

Heuristic: transition sounds should often start before the visual cut and resolve just after it. That anticipates movement and makes edits feel motivated.

### UI and product sounds

For app demos, explainers, SaaS ads, device launches, and product films, UI sounds must be informative without becoming toy-like. Decide:

- interaction class: tap, confirm, error, hover, drag, snap, completion, loading, notification;
- brand personality: warm, clinical, playful, premium, secure, fast, human;
- frequency zone: avoid masking narration; keep harsh 2-5 kHz ticks controlled;
- system consistency: related actions share a palette but differ in pitch, envelope, or texture;
- accessibility: do not rely on sound alone to convey essential state in the final video.

Heuristic: a brand UI palette can be built from three base gestures: a short affirmative tick, a soft negative/blocked tone, and a completion flourish. Vary them instead of inventing unrelated sounds for each screen.

### Emotional and subjective sound

Use subjective sound for memory, fear, wonder, focus, intoxication, stress, relief, or point-of-view changes. Common moves:

- narrow bandwidth, heartbeat, tinnitus tone, breath, muffled world for panic or impact;
- warm room tone, soft cloth, close breath, low noise floor for intimacy;
- high shimmer, airy rise, harmonic bloom for wonder;
- brittle ticks, distant metallic groan, reversed texture for unease;
- silence or near-silence before revelation.

Heuristic: emotional design works when it is motivated by the character or edit, not pasted over the whole sequence. Use it as a lens that turns on and off.

## Prompt planning for sound generation providers

Provider tools differ, but good sound prompts usually include the same production facts. Provide the generator or sound designer with:

- exact duration target and whether it may loop;
- sync cue and visible action;
- source identity and material;
- performance: gentle, violent, playful, precise, clumsy, hurried, heavy;
- perspective: close mic, medium, distant, left/right, stereo width, occluded;
- environment: dry studio, tiled bathroom, office, forest, warehouse, street, underwater;
- layer role: transient, body, tail, ambience bed, UI cue, impact, sweetener;
- emotional adjectives tied to audible properties: "tense" should become low rumble, brittle high ticks, sparse air, or similar;
- avoid list: no music, no dialogue, no crowd, no recognizable brand jingle, no copyrighted melody, no clipping, no excessive reverb, no tonal pitch if it should be neutral;
- file handoff: sample rate, mono/stereo, loopable, stems, handles, loudness target if known.

Weak prompt: "Add sci-fi sounds."

Better prompt: "Create a 1.2-second close, dry, non-musical sci-fi confirmation sound for a premium medical app. It should start with a tiny glassy tap, bloom into a soft warm electronic chime, and end cleanly with no long reverb. Avoid gamey arcade tones, alarm beeps, voices, and melodies recognizable as a tune."

For long scenes, do not ask for one giant mixed sound unless the provider is specifically built for full-scene audio. Ask for separate assets or stems: ambience loop, key Foley hits, transitions, impacts, UI cues, and designed sweeteners. Stems are easier to sync, license, caption, and repair.

## Layering and perspective

Every important sound should answer three questions:

1. What physically caused it?
2. Where is it relative to the camera/listener?
3. What story emotion should it add?

Use material and distance to avoid generic results:

- Glass is bright, short, brittle, and can ring.
- Wood is warm, hollow, knock-like, and varies by size.
- Plastic is lighter, duller, sometimes squeaky.
- Metal can ping, scrape, rattle, ring, thud, or scream depending on mass.
- Fabric is broadband, soft, noisy, and useful for human movement.
- Liquid has bubbles, splashes, droplets, viscosity, and container resonance.
- Snow, sand, gravel, leaves, and mud are defined by granular texture and compression.

Perspective controls credibility:

- Close: more transient detail, dry texture, less environment, stronger stereo placement if appropriate.
- Medium: natural room reflections and less microscopic detail.
- Distant: less high end, more reverb/air, softer transients, often mono-ish or diffuse.
- Occluded: low-pass filtering, muffled attack, room or barrier coloration.
- Macro/product: exaggerated tiny detail, very low noise floor, precise timing.

## Edit and mix handoff

When handing off to an editor, mixer, or automated mix stage, provide:

- spotting list with timecodes and priorities;
- asset manifest with filename, source/license, prompt or recording notes, duration, sample rate, channels, and intended use;
- stems grouped as DX/dialogue/narration, MX/music, FX, Foley, ambience, UI/product, designed sweeteners, and optional M&E when localization is expected;
- sync notes for frame-locked events and acceptable slip range;
- loop instructions for ambience beds;
- alternate versions for risky sounds: dry/wet, loud/soft, realistic/stylized;
- loudness and true-peak target requested by the platform or delivery spec;
- accessibility notes: which non-speech sounds require caption labels;
- known risks: temporary library audio, unverified rights, possible masking, possible harshness, or client approval needed.

For localization, keep dialogue/narration separate from music and effects. If the final may be dubbed, avoid baking language-specific UI narration or verbal sound effects into the FX stem.

## Loudness, safety, and accessibility

Do not invent one universal loudness target. Ask for or infer the delivery context, then follow that platform, broadcaster, client, or festival spec. If no spec exists, make a conservative web/social rough mix and document that it is not a formal delivery master.

Use ITU-R BS.1770-style loudness and true-peak measurement when possible. EBU R 128 is relevant for many broadcast workflows; Netflix and other platforms publish their own delivery specs. These are not interchangeable.

Safety checks:

- avoid clipping and intersample peak issues; leave true-peak headroom appropriate to the spec;
- avoid sudden painful high-frequency spikes, especially in headphones;
- avoid excessive sub-bass that collapses on phones or distorts small speakers;
- check dialogue/narration intelligibility with music and FX active;
- check headphone and phone-speaker playback, not only studio monitors;
- avoid using alarms, sirens, emergency alerts, or medical-device-like beeps unless the story requires them;
- avoid startle spikes in content for children, wellness, education, or accessibility-sensitive contexts unless explicitly intended.

Caption meaningful non-speech audio. Include sounds that carry story, timing, warnings, speaker identity, music mood, offscreen action, or emotional information. Keep caption labels concise and consistent, for example: "[door unlocks]", "[soft notification chime]", "[distant thunder]", "[music swells]". Do not caption every tiny Foley rustle if it adds no meaning.

## Rights-safe sourcing and generation

For each sound, record provenance. A useful rights ledger includes:

- filename and short description;
- source type: recorded by project, generated by provider, purchased library, user-owned, platform library, CC/public-domain source;
- license or terms URL;
- attribution text if required;
- commercial-use status;
- modification/adaptation status;
- territory/platform limits;
- verification date;
- whether the asset is approved for final or temporary only.

Prefer:

- original recorded Foley when feasible;
- generated sounds whose provider terms permit the intended commercial use;
- paid libraries with clear sync/use rights;
- CC0 or CC BY assets when attribution is acceptable and license conditions are compatible;
- platform libraries only within their stated context.

Avoid:

- ripping sounds from films, games, trailers, TikToks, YouTube videos, or copyrighted songs;
- using "royalty-free" claims without reading the actual license;
- using CC NonCommercial assets in ads, product films, client work, monetized videos, or anything commercially directed;
- using NoDerivatives assets when you need to edit, layer, transform, or redistribute an adapted version;
- using recognizable branded notification sounds, OS sounds, game sounds, or signature creature/weapon sounds without clearance.

## Iteration and repair

Diagnose sound problems by muting and soloing layers. Do not regenerate the whole mix until you know which layer failed.

Common failures and repairs:

- Late/early sync: nudge the sound by frames; align transient to visible contact, not clip start.
- Generic whoosh: add material, direction, motion speed, and tail length; reduce broad noise.
- Foley feels fake: change surface/material, add room tone, reduce volume, and vary performance timing.
- Impact lacks weight: add pre-silence, transient, low body, debris tail, and duck competing layers briefly.
- Dialogue is masked: lower music/FX in 1-4 kHz, duck around speech, shorten reverb, reduce stereo clutter.
- Ambience loops obviously: use longer loop, crossfade, add randomized one-shots, or reduce repeated details.
- UI is annoying: shorten decay, lower level, remove harsh partials, use softer envelope, reduce repetition.
- Mix is fatiguing: reduce density, reserve highs/lows, create quiet moments, and lower transition count.
- Sound does not match picture scale: adjust perspective, reverb, low end, and transient detail.
- Rights unclear: replace before final; never bury an uncleared sound in a mixed stem.

## Sound QA checklist

Run this checklist before final handoff:

- All key visual contacts with narrative importance have either sound or an intentional reason for silence.
- No sound contradicts material, distance, scale, or point of view unless stylized intentionally.
- Dialogue/narration remains intelligible on laptop/phone speakers.
- Music, Foley, ambience, and effects do not all peak emotionally at the same time unless that is the moment.
- Transitions motivate cuts without calling attention to themselves.
- Ambience beds have clean starts/ends and no obvious loop clicks.
- UI/product sounds match brand tone and do not mimic protected platform sounds.
- No clipping, harsh spikes, or unsafe startle levels are present.
- Loudness/true-peak has been measured or flagged as rough/unmastered.
- Caption plan includes meaningful non-speech audio.
- Rights ledger is complete enough for a client or publisher to audit.
- Stems and filenames are organized for revision.

## Complete examples

### Example: 20-second AI trailer sound plan

Production intent: a vertical sci-fi trailer for a generated short. The picture has a quiet astronaut helmet close-up, a door opening to a huge alien structure, three rapid action cuts, and a title reveal.

Spotting and direction:

| Time | Picture | Sound plan | Notes |
|---|---|---|---|
| 00:00-00:04 | Helmet close-up, breath fog | Close helmet breath, faint suit servo, low cabin tone | Subjective interior, intimate, no music hit yet |
| 00:04-00:07 | Door opens | Hydraulic seal release, metal groan, widening alien wind bed | Sync seal to first visible gap; wind grows as space opens |
| 00:07-00:11 | Alien structure reveal | Subtle sub bloom, vast reverb tail, distant harmonic shimmer | Awe, not horror; avoid choir if music owns emotion |
| 00:11-00:16 | Rapid danger cuts | Three distinct impacts: rock debris, creature pass, alarm pulse | Each hit different; leave gaps for rhythm |
| 00:16-00:20 | Title appears | Reverse swell into clean trailer hit, debris tail fades | Title hit is biggest moment |

Example generation prompts:

- "Create a 4-second close interior space-helmet ambience loop: soft human breath behind visor, faint suit electronics, muffled low cabin tone, no speech, no alarm, seamless loop, stereo but centered."
- "Create a 1.5-second heavy sci-fi door seal release synchronized to a vertical blast door opening: rubber pressure hiss, hydraulic piston, dark metal groan, medium distance, no music."
- "Create a 2-second alien-megastructure awe sweetener: deep controlled sub bloom, wide airy shimmer, long reverb tail, mysterious but not horror, no choir, no melody."

Likely failure modes: provider creates music instead of effects; door is too game-like; impact overpowers title. Repair by splitting assets, requesting no music/no melody, and lowering earlier impacts.

### Example: premium product film for a foldable device

Production intent: a 30-second product video with macro shots of a hinge, glass surface, magnetic close, UI cards sliding, and final hero pose.

Sound palette:

- hinge: soft precision mechanical whisper, tiny polished-metal ticks, no squeak;
- glass: fingertip slide with controlled high-end detail;
- magnetic close: short low-mid thock plus clean high snap;
- UI cards: soft synthetic swipes, restrained pitch movement, no arcade bleeps;
- ambience: quiet studio air with almost inaudible low warmth;
- transitions: silk-like air sweeps, short and elegant.

Handoff note: provide dry versions of hinge, glass, and magnetic close separately so the mixer can sync to final edit. Keep UI cues in a separate stem because localization or platform adaptation may require lowering them.

Example prompt:

"Create six separate premium product Foley one-shots for a foldable phone: (1) tiny polished hinge tick 0.2s, (2) smooth hinge glide 0.8s, (3) fingertip on glass micro-swipe 0.5s, (4) magnetic close 0.4s with soft low thock and crisp snap, (5) elegant UI card swipe 0.35s, (6) final confirmation chime 0.7s. Clean studio sound, high-end consumer electronics, no music, no brand-identifiable OS sounds, no cartoon beeps, no harsh highs."

### Example: explainer/avatar clip with captions

Production intent: a 60-second animated explainer with avatar narration, simple diagrams, and light UI interactions.

Sound decisions:

- narration is top priority; all other sounds duck under speech;
- use sparse diagram sounds: pen line draw, soft node pop, gentle connection whoosh;
- room tone is minimal but present to avoid dead silence;
- no loud impacts during educational definitions;
- caption meaningful non-speech only: "[soft chime]", "[diagram line draws]", "[error buzz]" if those sounds convey meaning.

QA focus: check intelligibility on phone speakers; verify no UI cue sounds like a real emergency alert; confirm captions do not clutter the screen with every tiny pop.

## Sources checked

- Berklee College of Music, "Foley Artist" career role, verified 2026-07-10: https://www.berklee.edu/careers/roles/foley-artist
- ITU-R BS.1770-5, "Algorithms to measure audio programme loudness and true-peak audio level", verified 2026-07-10: https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-5-202311-I!!PDF-E.pdf
- EBU Technology & Innovation, "Loudness", verified 2026-07-10: https://tech.ebu.ch/loudness
- W3C WAI, "Understanding Success Criterion 1.2.2: Captions (Prerecorded)", verified 2026-07-10: https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
- Section508.gov, "Video and Other Synchronized Media", verified 2026-07-10: https://www.section508.gov/create/synchronized-media/
- YouTube Help, "Use music and sound effects from the Audio Library", verified 2026-07-10: https://support.google.com/youtube/answer/3376882
- Creative Commons, "The CC Licenses", verified 2026-07-10: https://creativecommons.org/cc-licenses/
- Freesound FAQ, verified 2026-07-10: https://freesound.org/help/faq/
- Netflix Partner Help, "Netflix Dolby Atmos Home Mix Deliverable Requirements v2.3", used as an example of platform-specific delivery requirements rather than a universal target, verified 2026-07-10: https://partnerhelp.netflixstudios.com/hc/en-us/articles/115001539991-Netflix-Dolby-Atmos-Home-Mix-Deliverable-Requirements-v2-3
