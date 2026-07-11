---
name: music-video-production
description: Provider-independent production workflow for AI agents creating music videos, lyric videos, visualizers, performance/narrative/dance videos, social cutdowns, album or single launch assets, and generated-media clips synchronized to songs. Use when planning, directing, prompting, editing, reviewing, or delivering video content built around a recorded song, artist performance, lyrics, beat timing, choreography, platform variants, music rights, likeness consent, accessibility, or synthetic-media disclosure.
---

# Music Video Production

Use this skill to turn a song into a coherent, rights-aware, platform-ready video package. Treat the song as the fixed spine: the video exists to amplify its structure, artist identity, lyrics, and release goal.

Do not treat this as generic video generation. Music videos need beat maps, phrase maps, lyric accuracy, sync review, rights notes, performance direction, platform-specific cutdowns, and approval checkpoints.

## Ground rules

- Keep the master audio unchanged unless the artist, label, or client approves a radio edit, clean edit, stem edit, speed change, fade, or shortened version.
- Never invent rights clearance. Record what is cleared, unknown, platform-provided, licensed, royalty-free, public-domain, or generated.
- Do not provide legal advice. Flag clearance, likeness, endorsement, union, label, distributor, or platform-risk questions for the client, rights holder, label, manager, or counsel.
- Re-check platform rules at production time. Music libraries, AI labels, commercial disclosure tools, ad specs, and upload limits change often.
- Separate documented facts from production heuristics. Facts should trace to current sources; heuristics are creative recommendations.
- Preserve provenance: song source, lyric source, stems, edits, models, prompts, seeds when available, consent documents, licenses, platform checks, and review notes.

## Intake

Collect enough information before concepting:

1. Song package
   - final audio file, duration, sample rate, bit depth, loudness target if known
   - song title, artist name, featured artists, version name, ISRC/UPC if released
   - approved lyrics, explicit/clean status, lyric translation if needed
   - optional stems: vocal, instrumental, drums, bass, melody, ad-libs
   - BPM, key, time signature, section labels if known
2. Release and audience
   - goal: premiere, visualizer, lyric video, fan engagement, paid campaign, tour promo, album rollout, short-form hook testing
   - target platforms and aspect ratios
   - due date, review approvers, approval order, locked brand/artist guidelines
3. Rights and safety
   - who owns or controls the master and composition
   - whether sync use, social use, paid ad use, territory, term, and platform rights are cleared
   - whether any samples, interpolations, remixes, covers, or third-party stems are present
   - whether any brand, product, venue, artwork, tattoo, logo, prop, or recognizable person needs clearance
   - whether AI-generated video, voice, likeness, choreography references, or style references will be used
4. Creative references
   - 2-5 reference videos with what to borrow: pacing, lighting, blocking, edit rhythm, typographic treatment, camera language, color, surrealism level
   - what not to copy: artist likenesses, exact choreography, protected logos, distinctive set pieces, shot-for-shot structures

If rights status is unknown, proceed only with planning or internal mockups. Do not recommend publishing, paid promotion, distribution delivery, or public release until clearance is resolved.

## Choose the concept route

Pick one primary route and one secondary texture. A video can blend modes, but it should not feel like six unrelated concepts.

- Performance video: artist or performer carries the emotional center. Best when charisma, vocal delivery, band energy, or star identity matters.
- Narrative video: story scenes dramatize the song's emotional arc. Best when lyrics imply conflict, transformation, memory, romance, rebellion, grief, or triumph.
- Lyric video: typography, timing, and design carry the experience. Best before the official video, when lyrics are a key hook, or when budget/time is tight.
- Visualizer: repeated motif, loop, ambient world, generative motion, or symbolic animation supports listening. Best for albums, streaming canvases, and low-friction rollout assets.
- Dance or choreography video: movement is the hook. Best for rhythmic tracks, short-form challenges, fan participation, and performance-led social campaigns.
- Abstract/generated-media video: AI clips, animation, collage, simulations, or surreal imagery create a dream logic around the song. Best when the artist world is more important than literal story.
- Launch asset suite: combine hero video, vertical hook cuts, teaser loops, Canvas-style loops, lyric snippets, behind-the-scenes, and platform thumbnails.

Production heuristic: if the song has a memorable chorus lyric, design at least one repeatable visual signature for that phrase. If the song has an instrumental drop, design a non-lyric visual payoff: dance hit, camera move, color switch, surreal transformation, or montage burst.

## Build the song map

Create a beat-and-phrase map before writing shot lists or prompts.

Minimum map:

- timecode in `mm:ss.mmm`
- section: intro, verse, pre-chorus, chorus, post-chorus, bridge, breakdown, outro
- bar or phrase count if available
- key lyric fragments and vocal entrances
- beat accents, fills, drops, stops, pickup notes, ad-libs
- emotional intensity from 1-5
- edit density target: long holds, medium cuts, rapid cuts, strobe risk, silence
- visual event: reveal, movement change, text entry, performance close-up, transition, story beat

Example beat map row:

```text
00:45.200-01:07.900 | Chorus 1 | hook repeats twice | intensity 5 | cut on snare every 2 bars; hold final hook for 2.5s | lyric text enters on vocal, not before | hero blue-to-red lighting shift
```

Phrase mapping matters more than raw BPM. Cut on musical reasons: downbeats, lyric starts, drum fills, breath gaps, rhyme completions, bass drops, harmonic changes, and silence. Avoid cutting mechanically on every beat unless the genre and concept reward that intensity.

## Script, treatment, and shot list

Write a short treatment before prompts or filming.

Treatment should include:

- one-sentence promise: what the viewer will remember
- artist portrayal: iconic, vulnerable, playful, untouchable, documentary, mythic, anonymous, animated
- world: location, era, color, texture, weather, lighting, lens feel
- structure by song section
- recurring motifs and how they evolve
- what appears in chorus 1, chorus 2, final chorus, and why each escalates
- rules for lyrics/on-screen text
- rules for generated clips: realism level, camera language, continuity anchors, negative constraints
- approval risks: rights, likeness, flashing, explicit content, brand safety

Shot list fields:

```text
ID | Timecode | Section | Shot size | Subject | Action | Camera/motion | Lighting/color | Sync requirement | Asset/source | Notes
```

Sync requirement examples:

- `lip-sync exact to lead vocal`
- `dance hit on downbeat`
- `lyric word appears on syllable`
- `cutaway only; no mouth movement`
- `loop must restart invisibly every 4 bars`
- `AI clip can drift; use under instrumental texture`

## Performance and choreography direction

For performance:

- Use playback on set or in generated/lip-sync direction. The performer must hear the final approved audio version or a timecode-aligned playback version.
- Direct emotional beats by section, not just "sing with energy." Example: verse 1 restrained eye contact, pre-chorus pacing, chorus direct-to-lens, bridge turned away, final chorus full-body release.
- Capture sync-safe coverage: locked close-up of mouth, medium performance, wide body, detail inserts, overcranked movement, non-singing cutaways.
- Avoid visible singing in shots not intended for exact sync unless the mouth is obscured or off-axis.
- For bands, map featured instruments to audible moments. Do not cut to a drummer during a guitar-only fill unless intentionally ironic.

For dance:

- Mark counts against the song map. Note the move name, body direction, camera direction, and hit frame.
- Keep a clean master wide for choreography continuity, then add close-ups and detail shots.
- Plan short-form challenge sections around 5-15 seconds of memorable movement.
- If AI-generated dancers are used, prompt for broad rhythm and pose change but verify manually; generated motion may not obey exact counts.

## Lyric and on-screen text

Use approved lyrics only. If lyrics are not provided, ask for them or transcribe and mark as unapproved.

Lyric video rules:

- Align words to the lead vocal, not to the instrumental grid.
- Keep line breaks musical: phrase, rhyme, breath, or semantic unit.
- Design hierarchy for lead vocal, background vocal, ad-lib, and non-lyric captions.
- Do not obscure the artist's face at emotional moments unless the concept is typographic-first.
- Preserve safe margins for vertical UI overlays and captions.
- Provide a clean textless master when feasible for localization and future edits.

On-screen text can include title cards, credits, warnings, release date, merch/tour CTA, and disclosures. Keep disclosures readable and near the claim or content they clarify.

## Generated-video prompt translation

When using AI image/video tools, translate music-video direction into production prompts. Do not ask a model to "make a music video" and hope for sync. Most generated-video systems are weak at exact lip sync, lyric timing, text fidelity, and continuity unless the provider specifically supports those controls.

Prompt components:

- shot duration and aspect ratio
- subject identity or fictional character description; avoid unauthorized real-person likeness
- action in one clear motion phrase
- camera movement and shot size
- lighting, lens, color, texture, location
- timing anchor from the song map
- continuity anchors: wardrobe, prop, color, environment
- negative constraints: no readable random text, no extra fingers, no logo, no mouth singing, no face morphing, no flicker

Example generated-clip prompt:

```text
4-second vertical 9:16 shot for the final chorus of an indie-pop music video. A fictional silver-jacketed performer runs through a rain-slick neon alley, turns sharply toward camera on the downbeat, and throws a handful of glitter that becomes floating stars. Handheld tracking shot, 35mm lens feel, saturated cyan and magenta, wet pavement reflections, high-energy chorus payoff. No real celebrity likeness, no readable signs, no lip-sync mouth movement, no strobing, no brand logos.
```

Use generated clips where they are strongest: surreal inserts, visualizers, environments, transitions, symbolic action, dream sequences, and texture. Use specialist lip-sync or avatar tools, live footage, or carefully directed animation when mouth sync is mission-critical.

## Edit rhythm

Music-video editing should feel musically intentional without becoming predictable.

- Establish a visual grammar in the intro.
- Use verses for story, intimacy, or world-building.
- Use pre-choruses for acceleration: camera movement, shorter cuts, rising text density, color transition.
- Use choruses for the most repeatable visual idea.
- Save one escalation for the final chorus: new location, wider shot, choreography group, color inversion, rain/fire/confetti, crowd, or abstract transformation.
- Let important lyrics breathe. A powerful line often lands better with a hold than with more cuts.
- Create contrast: dense montage after a long hold, silence after chaos, close-up after wide choreography.
- Avoid flash patterns above accessibility thresholds; do not use rapid full-frame strobing as a default "energy" solution.

Use cutdowns intentionally:

- 6-8 seconds: hook/teaser/Canvas-like loop; one idea only.
- 10-15 seconds: social challenge or chorus hook.
- 20-30 seconds: paid social or release announcement.
- 45-60 seconds: extended short-form excerpt.
- Full-length: canonical music video or visualizer.

## Lip-sync and playback sync

For live-action or avatar/lip-sync work:

- Lock the audio version before generating or filming sync shots.
- Use slate/timecode or visible clap for live shoots where possible.
- Align mouth shapes to consonants and phrase starts; vowels alone are forgiving, plosives are not.
- Check sync at normal speed and half speed.
- If a shot is slightly off, use cutaways over the worst syllables instead of stretching the master audio.
- Do not alter pitch, tempo, or timing of the released song to fit generated visuals unless explicitly approved.

For lyric sync:

- Spot check all chorus repeats; copy-pasted timing often drifts because vocal phrasing changes.
- Confirm censored/clean lyric treatment matches the distributed audio version.

## Rights, credits, and disclosure checkpoints

Escalate to the client, rights holder, label, manager, distributor, platform specialist, or counsel when any of these appear:

- copyrighted song is not owned/controlled by the artist or client
- cover, remix, sample, interpolation, beat lease, stock loop, or third-party vocal is present
- the video will be used in paid ads, brand partnerships, political contexts, regulated industries, or endorsements
- real person likeness, voice clone, digital replica, archival footage, fan footage, minors, private locations, tattoos, logos, or artwork appear
- platform-native music library is being used outside its allowed context
- generated media imitates a living artist, celebrity, dancer, photographer, director, or recognizable visual style too closely
- union performer, label contract, distributor, or venue rules may apply

Documented facts to apply, verified July 11, 2026:

- YouTube requires creators to disclose realistic altered or synthetic content that viewers could mistake for a real person, place, scene, or event; YouTube says clearly unrealistic, animated, special-effects, or production-assistance uses are not generally required under that tool. Source: YouTube Blog, "How we're helping creators disclose altered or synthetic content" and YouTube Help "How this content was made" disclosure pages.
- TikTok says creators must label realistic AI-generated content and offers creator and automatic AI labels; misleadingly labeling unaltered content as AI-generated may violate its terms. Source: TikTok Help, "About AI-generated content."
- Meta's misinformation policy states that organic content with photorealistic video or realistic-sounding audio must be disclosed using its AI-disclosure tool. Source: Meta Transparency Center, "Misinformation."
- FTC endorsement guidance requires clear and conspicuous disclosure of unexpected material connections between an endorser and advertiser. Source: FTC Endorsement Guides and 16 CFR Part 255.
- TikTok says business/promotional content should use its Commercial Music Library because music outside that library is not licensed for commercial use in content. Source: TikTok Help, "Commercial use of music on TikTok" and TikTok Ads Help, "About the Commercial Music Library."
- YouTube Audio Library tracks may require attribution, especially Creative Commons tracks; YouTube Creator Music includes upfront licensing and revenue-share options with availability limits. Source: YouTube Help Audio Library and Creator Music pages.
- U.S. Copyright Office guidance on AI copyrightability emphasizes human authorship; mere prompting alone is not treated as sufficient authorship for copyright protection in its 2025 Part 2 report summary. Source: U.S. Copyright Office AI report pages.

Treat these as compliance prompts, not legal conclusions. Platform rules, law, and licensing terms vary by country, account type, content type, and date.

## Accessibility and audience safety

Documented facts, verified July 11, 2026:

- WCAG 2.2 Success Criterion 1.2.2 requires captions for prerecorded audio content in synchronized media, except when the media is a clearly labeled media alternative for text.
- WCAG 2.2 Success Criterion 2.3.1 says content should not flash more than three times in any one-second period unless below general and red flash thresholds.

Production requirements:

- Provide captions or subtitles for dialogue, spoken intros/outros, and non-lyric information. For lyric videos, also provide platform captions or a transcript when feasible; stylized lyric text alone may not be accessible or parseable.
- Include meaningful non-speech audio where it matters: `[crowd chanting]`, `[thunder]`, `[music stops]`.
- Avoid full-screen flashes, hard black-white strobes, high-saturation red flashes, and rapid flicker transitions.
- Run a flashing-risk review on final exports, especially EDM, hyperpop, metal, glitch, nightclub, or fast typography treatments.
- Keep text legible on mobile: high contrast, enough dwell time, safe margins, no essential text behind platform UI.
- For explicit content or sensitive themes, follow the target platform's age, ad, and community rules.

## Platform variants and delivery

Create a master first, then derive variants. Do not crop a finished 16:9 frame into 9:16 if the artist's face, dance, lyrics, or credits become unusable.

Useful deliverables:

- full-length master: 16:9, 4K or 1080p, textless when possible
- vertical master: 9:16, reframed or separately designed
- square/portrait feed: 1:1 or 4:5 when requested
- chorus cutdown: 15-30 seconds
- teaser: 6-10 seconds
- lyric snippets: one per key lyric/hook
- visualizer loop: seamless 3-8 seconds or platform-specific duration
- thumbnail/cover frames: no accidental closed eyes, random AI text, or unclear artist identity
- captions/subtitles: SRT/VTT plus burned-in version if required
- credits/disclosure notes: song, artist, director/editor, AI tools where required, music/license attribution where required

Volatile platform facts to re-check at delivery:

- YouTube upload encoding recommendations include progressive scan, high profile, closed GOP, 4:2:0 chroma subsampling, and matching the source frame rate; official bitrate recommendations vary by resolution/frame rate. Source verified July 11, 2026: YouTube Help, "Recommended upload encoding settings."
- YouTube Shorts support videos up to 3 minutes in the Shorts creation/upload context. YouTube says square-or-taller videos uploaded by standard channels on or after October 15, 2024 are categorized as Shorts; Official Artist Channels and channels linked to a music Content Owner use December 8, 2025 as the corresponding cutoff. Shorts over one minute with active Content ID claims may be blocked globally. Source verified July 11, 2026: YouTube Help and YouTube Blog.
- Instagram Reels Help says uploads can use aspect ratios from 1.91:1 to 9:16 and should meet minimum 30 FPS and minimum resolution requirements. Source verified July 11, 2026: Instagram Help, "Reel size & aspect ratios."
- TikTok Non-Spark auction in-feed ad specs list vertical 9:16 at least 540x960, square 1:1 at least 640x640, horizontal 16:9 at least 960x540, supported video formats, up to 10 minutes, and file size limits; Spark Ads can differ, so re-check the chosen ad format. Source verified July 11, 2026: TikTok Ads Help, "TikTok Auction In-Feed Ads."

Prefer current platform help pages over memory. Specs differ for organic posts, ads, Stories, Reels, Shorts, Canvas-like loops, distributor portals, and account types.

## Review cycles

Use staged approvals:

1. Intake approval: audio version, lyrics, rights status, target platforms, concept route.
2. Treatment approval: story, style, references, disclosure and risk notes.
3. Beat map and shot list approval: sync moments, lyric treatment, performance/choreography plan.
4. Asset approval: generated clips, filmed selects, typography tests, visualizer loops.
5. Rough cut approval: structure and emotional read, not final polish.
6. Fine cut approval: sync, lyrics, performance, color, text, credits.
7. Delivery approval: exports, captions, disclosures, filenames, metadata, thumbnails.

Ask approvers specific questions. "Thoughts?" produces vague notes. Better:

- Is the chorus visual signature approved?
- Are these lyrics and clean/explicit treatments correct?
- Is the artist portrayal on-brand?
- Are there any rights issues with locations, people, brands, artwork, or styling?
- Is the AI/synthetic disclosure plan acceptable for each platform?
- Which cutdown should lead the launch?

## Music-video QA checklist

Run this before handoff:

- Audio
  - final audio matches approved version
  - no unintended pitch, speed, fade, clipping, or offset
  - loudness and true peak meet delivery target if specified
- Sync
  - lead vocal lip-sync passes at normal and half speed
  - lyric text hits syllables and phrase starts
  - dance hits and edit accents match the beat map
  - generated clips without reliable sync avoid visible singing
- Lyrics/text
  - lyrics match approved source
  - spelling, names, title, featuring credits, release date, CTA, and hashtags are correct
  - text stays inside safe areas for each aspect ratio
- Visual continuity
  - artist identity, wardrobe, props, environment, color, and motifs are consistent enough for the concept
  - no unwanted AI artifacts: warped hands, face drift, random words, logo hallucinations, flicker, melting objects
  - no accidental brand logos or uncleared artwork
- Rights and disclosure
  - music license/provenance logged
  - third-party footage, photos, fonts, artwork, locations, and performers logged
  - likeness/voice/digital replica consent logged where applicable
  - platform AI and commercial disclosures checked for each release context
  - credits and required attribution included
- Accessibility/safety
  - captions/subtitles/transcript prepared as needed
  - flashing/strobe risk reviewed
  - text contrast and dwell time checked on phone-size playback
- Delivery
  - master and variants exported to requested specs
  - thumbnails/cover frames selected
  - filenames include title, version, aspect ratio, duration, date, and approval status
  - textless and clean versions exported if requested

## Example: lyric video for a single launch

Production intent: a 2:48 pop single needs a fast-launch lyric video plus vertical chorus cutdowns.

Inputs:

- approved WAV and lyrics
- cover art and artist logo
- no performer footage
- platforms: YouTube full-length, Instagram/TikTok chorus snippets

Approach:

1. Build a phrase map from the vocal, not just a BPM grid.
2. Choose a typographic concept based on the cover art: chrome serif title words, handwritten ad-libs, soft grain background.
3. Create full-length 16:9 first with safe-centered lyrics, then design a separate 9:16 layout with larger line breaks.
4. Use visual escalation: verse small and intimate, chorus full-frame kinetic type, bridge minimal black field, final chorus adds cover-art motif.
5. Export textless motion background and lyric-burned master.

Example direction:

```text
The video is a nocturnal lyric object, not a karaoke screen. Each verse line appears like a private text message reflected in chrome. Chorus phrases arrive as large sculptural type that bends with the vocal. Ad-libs appear smaller, handwritten, and offset. No random decorative words. Every lyric is from the approved sheet. Avoid flashes; use smooth brightness pulses under WCAG flash threshold.
```

Expected failure modes:

- copied chorus timing drifts on final chorus
- vertical crop hides long lyric lines
- AI background generates fake readable text
- attribution missing for cover-art elements or fonts

## Example: narrative/performance hybrid with generated inserts

Production intent: an alternative R&B artist wants a moody official video with live performance and surreal generated dream inserts.

Inputs:

- final song, lyrics, artist appearance release, two filmed performance setups
- generated clips allowed for symbolic sequences
- no real celebrity likeness references

Approach:

1. Map the song into verse memory scenes, pre-chorus tension, chorus performance-to-camera, bridge dream collapse.
2. Use filmed artist shots for all visible singing.
3. Use generated clips only for cutaways: flooded hallway, floating red phone, room of flickering TVs, flowers opening in reverse.
4. Keep continuity anchors: red coat, rain on window, tungsten practicals, 50mm lens feel.
5. Cut generated clips on instrumental fills and line endings, not over critical mouth sync.

Example generated insert prompt:

```text
3-second 16:9 cinematic insert for an alternative R&B music video bridge. A red rotary phone floats just above a dark flooded apartment floor, its cord slowly moving like a snake. Tungsten lamp reflection, shallow depth of field, gentle push-in, melancholic and surreal, 50mm lens feel, realistic water ripples. No people, no readable text, no brand marks, no strobe, no horror gore.
```

QA focus:

- generated clip does not imply unauthorized actor likeness
- dream inserts do not break the artist's established color world
- performance shots carry all vocal sync
- bridge visual intensity escalates without unsafe flashing

## Key sources checked

Verified July 11, 2026 unless noted. Re-check before release.

- YouTube Help, "Recommended upload encoding settings": https://support.google.com/youtube/answer/1722171
- YouTube Blog, "How we're helping creators disclose altered or synthetic content": https://blog.youtube/news-and-events/disclosing-ai-generated-content/
- YouTube Help, "Understanding 'How this content was made' disclosures on YouTube": https://support.google.com/youtube/answer/15447836
- YouTube Help, "Understand three-minute YouTube Shorts": https://support.google.com/youtube/answer/15424877
- TikTok Help, "About AI-generated content": https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content
- TikTok Help, "Commercial use of music on TikTok": https://support.tiktok.com/en/business-and-creator/creator-and-business-accounts/commercial-use-of-music-on-tiktok
- TikTok Ads Help, "About the Commercial Music Library": https://ads.tiktok.com/help/article/commercial-music-library
- TikTok Ads Help, "TikTok Auction In-Feed Ads": https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads
- Instagram Help, "Reel size & aspect ratios on Instagram": https://help.instagram.com/1038071743007909
- Meta Transparency Center, "Misinformation": https://transparency.meta.com/policies/community-standards/misinformation/
- FTC, "The FTC's Endorsement Guides: What People Are Asking": https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- Electronic Code of Federal Regulations, 16 CFR Part 255: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255
- W3C WCAG 2.2, Captions (Prerecorded): https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
- W3C WCAG 2.2, Three Flashes or Below Threshold: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- U.S. Copyright Office, "Copyright and Artificial Intelligence": https://www.copyright.gov/ai/
- U.S. Copyright Office, "What Musicians Should Know about Copyright": https://www.copyright.gov/engage/musicians/
- BMI, "BMI and Performing Rights": https://www.bmi.com/licensing/entry/business_using_music_bmi_and_performing_rights
- SAG-AFTRA, "Artificial Intelligence": https://www.sagaftra.org/contracts-industry-resources/member-resources/artificial-intelligence
