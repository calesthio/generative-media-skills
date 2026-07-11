---
name: livestream-event-production
description: Use this skill to plan, direct, troubleshoot, and hand off provider-independent live or hybrid livestream event productions, including run of show, crew, capture, audio, graphics, switching, guests, encoding, ingest, transport choices, latency, redundancy, accessibility, moderation, monitoring, incidents, recording, and delivery.
---

# Livestream Event Production

Use this skill when the user needs an AI agent to plan, direct, rehearse, run, troubleshoot, or hand off a live or hybrid livestream event. The event may be a webinar, conference session, town hall, launch, panel, class, fundraiser, worship service, performance, creator show, press briefing, or multi-room hybrid event.

This is a provider-independent production skill. It should produce a practical production plan, not a single-platform integration recipe.

Do not use this skill for:

- recutting, packaging, or editing an already recorded livestream after the fact;
- single-provider API integration, account setup, or dashboard-specific click paths;
- purely cinematic prerecorded video production with no live switching, live guests, ingest, monitoring, or incident plan;
- generic social short editing, podcast editing, or talking-head recut tasks unless the output is a live event plan.

## Evidence Labels

When making claims, keep these categories distinct:

- **Documented fact:** a standard, first-party documentation page, regulator page, or formal technical report supports the claim.
- **Volatile platform fact:** a platform-specific setting, codec table, bitrate recommendation, ingest limit, feature availability, or dashboard behavior. State the verification date.
- **Production heuristic:** field-tested operating guidance that is not a standard. Present it as a decision aid, not as a universal requirement.

## Operating Model

A livestream is a live show plus a live network service. Treat it as both.

The agent should produce or request these artifacts:

- event brief: audience, objective, platform destinations, privacy level, rights, language, accessibility, duration, success metrics;
- run of show: exact segments, timings, cues, sources, speakers, slides, graphics, lower thirds, videos, polls, Q&A, sponsor reads, breaks, backup content;
- crew plan: producer, technical director/switcher, audio engineer, graphics operator, stream engineer, stage manager, moderator, caption lead, guest wrangler, recording/media manager, incident lead;
- signal plan: cameras, screen shares, remote guests, playback, audio buses, graphics, program, clean feed, confidence monitors, comms, records, platform ingest;
- network and transport plan: contribution, ingest, delivery, latency profile, primary/backup paths, bandwidth headroom, monitoring points;
- rehearsal and go/no-go plan;
- incident plan and handoff package.

## Intake Questions

Ask only for unknowns that change production risk. If the user gives a partial brief, proceed with assumptions and mark them.

Critical questions:

- Is the event live-only, hybrid, or live-to-tape with live interaction?
- What is the audience size, destination list, privacy model, and replay requirement?
- Which interactions must feel live: chat, Q&A, polls, caller questions, auctions, donation moments, live interpretation, backstage speaker changes?
- What latency is acceptable for those interactions?
- Who appears on camera, from where, and with what network/control conditions?
- Are captions, sign language, audio description, translation, or compliance obligations required?
- What is the failure tolerance: can the show pause, cut to slate, switch to audio-only, replay a recording, or must it continue uninterrupted?
- What must be recorded: program, clean feed, isolated cameras, isolated guest feeds, multitrack audio, captions, chat/Q&A, slides, telemetry?

## Run Of Show

The run of show is the control document. It should be timed, cueable, and useful during stress.

Include:

- absolute event time and relative show time;
- segment title and owner;
- source on program, next source on preview, audio source, graphics state, caption/interpreter state;
- exact cue language for host, producer, TD, audio, graphics, moderator, stage manager, and remote guests;
- expected duration, hard out, and overrun plan;
- interaction trigger and latency implication;
- fallback if the source is unavailable.

Production heuristic: any segment that requires a human to remember an off-screen dependency should have a row in the run of show. Slides, videos, speaker arrivals, sponsor reads, polls, captioner handoffs, language-channel changes, and moderation transitions are all rows, not vibes.

## Crew And Communications

Assign roles by accountability, even when one person holds multiple roles.

- **Producer:** owns show intent, timing, go/no-go calls, client/stakeholder channel, and incident escalation.
- **Technical director/switcher:** owns program switching, preview, macros, camera/source readiness, slates, and emergency visual fallback.
- **Stream engineer:** owns encoder, ingest, network, redundancy, platform health, stream telemetry, and failover.
- **Audio engineer:** owns mix-minus, gain staging, loudness consistency, echo prevention, music/playback routing, talkback isolation, and backup audio.
- **Graphics operator:** owns lower thirds, bugs, titles, timers, holding slates, captions display routing where applicable, and sponsor/legal graphics.
- **Stage manager/guest wrangler:** owns speaker check-in, green room, countdowns, muting discipline, camera framing, consent, and remote speaker backups.
- **Moderator/community lead:** owns chat rules, Q&A triage, escalation, blocked terms, link policy, removal, and safety interventions.
- **Caption/accessibility lead:** owns live captions, interpreter windows if any, caption platform path, transcript handoff, and accessibility checks.
- **Recording/media manager:** owns program record, ISOs, file naming, storage, backups, captions/transcripts, and post-event package.

Use separate channels for:

- show calling: producer, TD, audio, graphics, stream engineer, stage manager;
- speaker green room: host, guests, guest wrangler;
- stakeholder/client notes: producer only or producer plus client lead;
- incident escalation: small, named, decision-capable group.

Production heuristic: keep presenters out of the technical channel unless they are trained operators. Most live mistakes are made worse by too many people hearing the wrong countdown.

## Capture, Switching, Audio, And Graphics

### Cameras And Sources

For each visual source, document:

- source name and owner;
- physical or remote location;
- resolution, frame rate, color space if known, and aspect ratio;
- expected shot type or screen content;
- primary and backup path;
- whether it needs sync with audio, slides, captions, or another camera.

Production heuristics:

- Prefer stable, named sources over ad hoc screen shares for critical slides or videos.
- For hybrid rooms, treat the room audience and online audience as different audiences. Online viewers need closer framing, intelligible room questions, and explicit visual context.
- Keep a holding slate, event title card, break loop, technical-difficulty slate, and end card loaded before rehearsal.

### Audio

Audio failure is usually more damaging than video failure.

Plan:

- microphone list, owner, and battery/power plan;
- program mix and any clean/mix-minus feeds;
- remote guest return audio;
- playback and music levels;
- echo cancellation boundaries;
- room PA interaction for hybrid events;
- backup audio path, such as phone bridge, spare USB mic, room ambience mic, or secondary interface.

Production heuristics:

- For remote panels, every guest should use headphones unless echo cancellation has been tested with the exact platform and routing.
- Never send a participant their own delayed program audio as return.
- Test mute/unmute ownership. If guests can self-mute, the stage manager must know how to recover quickly.
- Keep host audio as the highest-priority source in failure plans. A black screen with clear host audio can be survived; unintelligible audio cannot.

### Graphics

Build graphics as live-operable states:

- lower thirds and name pronunciation notes;
- title cards, agenda cards, break slates, holding slates, technical difficulty slate;
- timers, countdowns, sponsor/legal bugs, QR/link graphics;
- poll/Q&A results;
- captions/interpreter layout accommodations.

Graphics must not cover captions, sign language interpreters, legally required disclosures, or critical slide content.

## Encoding, Ingest, Transport, And Delivery

Separate contribution, ingest, and audience delivery. Confusing them causes bad plans.

- **Contribution:** a camera, venue, encoder, or remote guest sends a feed into the production system.
- **Ingest:** the production encoder sends the finished or intermediate stream into a platform, CDN, cloud switcher, packager, or relay.
- **Delivery:** the audience receives playback, commonly through HTTP adaptive streaming, a platform player, an app, or an interactive real-time service.

### RTMP And RTMPS

Operational guidance: RTMP remains common as a live contribution/ingest path into streaming platforms and encoders. RTMPS is RTMP carried over TLS and is preferred when a destination supports encrypted ingest. Treat RTMP(S) primarily as a contribution/ingest protocol, not as the modern browser audience playback layer.

Volatile platform fact verified 2026-07-11: YouTube's live encoder documentation lists RTMP and RTMPS ingest, recommends RTMPS because the stream is encrypted into and through Google servers, and recommends testing before going live and monitoring stream health. The same page lists platform-specific codec, keyframe, bitrate, and audio guidance that must be rechecked before production. Source: https://support.google.com/youtube/answer/2853702

Production heuristics:

- Keep stream keys private and out of run-of-show documents shared widely.
- Use a backup ingest URL/key when the destination supports it.
- If using RTMP over the public internet, prioritize network stability and encoder health because retransmission behavior and platform buffering vary by implementation.

### SRT

Documented fact: the SRT Internet-Draft, "The SRT Protocol," describes SRT as a user-level protocol over UDP for reliable and secure transport optimized for low-latency live video streaming. It describes caller-listener and rendezvous connection configurations, SRT buffer latency negotiated during handshake as the maximum latency proposed by the peers, ARQ/NAK-based packet retransmission with too-late packet drop for live streams, and AES-CTR payload encryption using key material exchange. The draft expired in 2021, so treat it as a protocol description and pair it with current implementation documentation. Source verified 2026-07-11: https://datatracker.ietf.org/doc/html/draft-sharabayko-srt-00

Documented fact: Haivision's public SRT API documentation describes binding/listening/accepting, caller connection with `srt_connect`, rendezvous setup with `SRTO_RENDEZVOUS` or `srt_rendezvous`, Live transmission defaults, socket options such as `SRTO_RCVLATENCY`, `SRTO_PEERLATENCY`, `SRTO_TLPKTDROP`, `SRTO_NAKREPORT`, `SRTO_PASSPHRASE`, `SRTO_PBKEYLEN`, and key-material state options. Source verified 2026-07-11: https://github.com/Haivision/srt/blob/master/docs/API/API.md and https://github.com/Haivision/srt/blob/master/docs/API/API-socket-options.md

Operational guidance: SRT is commonly used for contribution over imperfect networks where low latency, packet recovery, encryption options, and caller/listener/rendezvous connection modes may matter. Exact behavior is implementation-specific: encoder/decoder builds, exposed socket options, firewall/NAT behavior, cloud receiver policy, and version support determine what can be configured and monitored.

Use SRT when:

- a venue or remote camera must contribute to a production control room over public internet;
- the network is variable but can tolerate a configured latency buffer;
- the team controls both sender and receiver configuration;
- firewall/NAT roles can be tested in advance.

Production heuristics:

- Set SRT latency as a production tradeoff: lower values feel faster but reduce recovery time; higher values improve resilience but add delay.
- Rehearse with the same network path and time of day if possible.
- Confirm encryption, passphrase policy, port direction, caller/listener/rendezvous roles, and fallback before show day.

### HLS

Documented fact: HTTP Live Streaming (HLS) uses playlists and media segments. RFC 8216 defines Media Playlists, Master Playlists, Media Segments, Variant Streams, Renditions, target duration, sequence/discontinuity behavior, and WebVTT subtitle carriage. Source: RFC 8216, https://www.rfc-editor.org/rfc/rfc8216

Use HLS for broad audience delivery when scale, device support, CDN distribution, and adaptive bitrate playback matter more than sub-second interaction.

Planning implications:

- HLS delivery delay is affected by encoder settings, segment duration, playlist behavior, packager/origin behavior, CDN, player buffer, and player live-edge policy.
- Master playlists let players choose among variants/renditions; those variants need synchronized content for seamless switching.
- WebVTT can be used for subtitles/captions in HLS workflows, but platform-specific caption ingest and display behavior must be verified.

Production heuristic: if chat or Q&A depends on exact audience timing, do not assume all HLS viewers see the same moment. Design interaction windows with buffer.

### WebRTC

Documented fact: W3C WebRTC 1.0 specifies real-time communication between browsers, including peer connections, media tracks, data channels, ICE, DTLS transport, RTP media, and statistics surfaces. Source: W3C Recommendation, 13 March 2025, https://www.w3.org/TR/webrtc/

Documented fact: RFC 8835 describes WebRTC transport protocols, including UDP/TCP assumptions, ICE/STUN/TURN for NAT and firewall traversal, DTLS-SRTP for media keying, SCTP over DTLS over ICE for data channels, and QoS/prioritization considerations. Source: RFC 8835, https://www.rfc-editor.org/rfc/rfc8835

Documented fact: RFC 8834 describes media transport and RTP use in WebRTC, including RTP/RTCP, SRTP/SRTCP, congestion control requirements, RTCP feedback, and performance monitoring via packet-loss and jitter statistics. Source: RFC 8834, https://www.rfc-editor.org/rfc/rfc8834

Use WebRTC when:

- remote guests must converse naturally;
- audience interaction must be very low latency;
- the workflow needs browser-based contribution, data channels, or conferencing-style topology;
- the expected audience size and architecture support it.

Planning implications:

- WebRTC is not automatically a mass-broadcast delivery system. Large audiences usually require SFUs, relays, bridges, or conversion to an HTTP delivery format.
- TURN capacity can become the hidden bottleneck for remote guests and interactive viewers.
- Monitor ICE state, selected candidate pair, round-trip time, jitter, packets lost, frames dropped, quality limitation reason, available outgoing bitrate, audio levels, and freezes where the implementation exposes them. The W3C WebRTC Statistics API defines many of these identifiers, but it is a Candidate Recommendation Draft and should be treated as a work in progress for exact field availability. Source: https://www.w3.org/TR/webrtc-stats/

## Latency And Interactivity

Pick the latency profile from the audience interaction, not from a generic desire to be fast.

| Need | Recommended profile | Notes |
| --- | --- | --- |
| One-way keynote, large audience, replay priority | Standard/normal latency HTTP delivery | More stable; chat can be asynchronous. |
| Live Q&A with host selecting questions from chat | Low-latency HTTP/platform mode if supported | Add moderation delay and phrase questions with time buffer. |
| Bidirectional panel, remote callers, auctions, live classroom | WebRTC/conferencing path or purpose-built low-latency service | Requires stronger guest control, TURN/network planning, and moderation. |
| Critical broadcast, compliance, captions, multiple CDNs | Stability-first latency | Use rehearsed failover and avoid untested low-latency modes. |

Volatile platform fact verified 2026-07-11: YouTube's encoder settings page says 4K/2160 content is not available for low-latency streaming and is optimized for normal-latency quality. Recheck before relying on this because platform features change. Source: https://support.google.com/youtube/answer/2853702

Production heuristic: lowering latency spends reliability budget. Spend it only where the show format earns it.

## Bandwidth And Redundancy

Calculate bandwidth from the entire path, not just the encoder bitrate.

Include:

- program bitrate plus audio and protocol overhead;
- backup stream if simultaneous;
- return feeds, comms, monitoring, captions, remote guest feeds, cloud switching, and file transfers;
- other venue traffic and Wi-Fi contention;
- upload, download, packet loss, jitter, and sustained throughput.

Production heuristics:

- Provision sustained upstream capacity at least 2x the total planned outbound streaming load on controlled networks; use more headroom on shared, wireless, cellular, or unknown paths.
- Do not count a backup path as redundant if it shares the same last-mile failure, power source, router, switch, SIM carrier, or account quota.
- Bonded/cellular paths are useful but not magic. Test congestion, data caps, thermal behavior, antenna placement, and failover under load.
- Keep an offline fallback asset loaded: technical slate, host dial-in script, prerecorded emergency opener, or audio-only bridge.

Redundancy levels:

- **Level 0:** one encoder, one network, one destination. Use only for low-stakes streams.
- **Level 1:** primary plus backup encoder profile or backup ingest on same network. Protects some software/config failures.
- **Level 2:** separate encoder or separate machine plus separate network path. Protects more local failures.
- **Level 3:** parallel production or cloud failover, separate power/network, backup operator, destination failover or multi-CDN. Needed for high-stakes public events.

## Rehearsal And Go/No-Go

Run at least three checks:

- **Technical line check:** every source, mic, graphic, playback item, caption path, remote guest path, record path, and destination ingest.
- **Cue-to-cue rehearsal:** transitions, openings, breaks, speaker changes, interaction moments, lower thirds, video rolls, emergency slates.
- **Full dress rehearsal:** real timing, real operators, real network, real destinations or private test destinations, real caption/moderation workflow.

Go/no-go should include:

- primary and backup ingest live/ready;
- program audio intelligible and meters stable;
- caption path verified if required;
- recording paths armed and storage checked;
- comms stable;
- guest names/pronunciations/lower thirds confirmed;
- rights/consent/clearances confirmed;
- moderation rules active;
- incident lead named;
- stakeholder approval for final start.

Production heuristic: do not declare rehearsal complete until someone has practiced a failure: lost guest, bad mic, dead slide source, encoder warning, platform health warning, or emergency slate.

## Captions, Accessibility, And Inclusion

Documented fact: WCAG 2.x Success Criterion 1.2.4 requires captions for live audio content in synchronized media at Level AA. W3C WAI explains that live captions are usually provided by professional real-time captioners/CART writers and that automatic captions are not sufficient unless confirmed fully accurate. Source verified 2026-07-11: https://www.w3.org/WAI/media/av/captions/ and https://www.w3.org/WAI/media/av/planning/

Documented fact: the FCC provides U.S. closed-captioning rules and quality/responsibility resources for television video programming, including 47 CFR Part 79 references. Jurisdiction and applicability must be verified for each distribution context. Source verified 2026-07-11, page updated April 8, 2026: https://www.fcc.gov/general/closed-captioning-video-programming-television

Documented fact: 47 CFR § 79.4 covers closed captioning of video programming delivered using Internet protocol. It defines IP-delivered video programming roles and requirements, including obligations for covered video programming owners to send required captions with at least the same quality as the television captions for the same programming, and obligations for covered distributors/providers to enable rendering or pass-through of required captions to end users. Applicability depends on whether the programming is nonexempt covered video programming under the rule. Source verified 2026-07-11 via eCFR, Title 47 displayed current as of 2026-07-09: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-C/part-79/section-79.4

Plan for:

- live caption provider or accurate verified automatic captions;
- caption source and route into platform/player/recording;
- caption display area that graphics do not cover;
- transcript handoff after the event;
- language interpretation, sign language interpreter framing, or audio description if required;
- accessible slides with readable type, contrast, and verbalization of visual-only content;
- moderator protocol for accessibility requests during the stream.

Production heuristics:

- If captions are required, treat caption loss as a show incident, not a cosmetic defect.
- Captioners need prep: names, jargon, acronyms, agenda, speaker list, URLs, sponsor names, and technical terms.
- Sign language interpreter windows need stable framing, priority in layouts, and protection from lower thirds.

## Moderation, Consent, Rights, And Safety

Plan before going live:

- who may appear on camera and whether consent is recorded;
- whether audience chat/Q&A is public, private, delayed, or moderated;
- blocked terms, link policy, spam handling, escalation, and removal authority;
- speaker release, music rights, stock/media rights, sponsor/legal copy, and replay rights;
- privacy handling for minors, patients, students, employees, confidential information, or restricted events;
- emergency stop criteria and who can cut stream, mute guest, hide chat, or remove a caller.

Production heuristic: moderation must have a faster path than the incident. If a harmful message, private information, or unsafe caller appears, the moderator should not need to ask five people for permission.

## Monitoring And Incident Response

Monitor at multiple points:

- local program output before encoding;
- encoder health: CPU/GPU, dropped frames, output bitrate, keyframe interval, audio sample rate, reconnects;
- network: upstream throughput, packet loss, jitter, route changes, interface failover, cellular signal;
- ingest health: platform/server receiving, backup ingest state, stream status messages;
- audience playback: independent viewer on a non-production network, captions, audio sync, chat/Q&A;
- recording: program record, clean feed, ISOs, audio multitrack, captions/transcript.

Incident workflow:

1. Name the symptom: what changed, who sees it, when it began, and which monitoring point detected it.
2. Contain audience impact: hold slate, host vamp, mute bad source, cut to backup, switch network, lower bitrate, pause interaction, or shift to audio-only.
3. Preserve evidence: timestamp, screenshots/logs, platform health messages, encoder stats, operator notes.
4. Decide: continue, degrade, fail over, pause, restart, or abort.
5. Communicate: one producer-approved message to host, stakeholders, chat/moderators, and post-event notes.

Production heuristics:

- Avoid live debugging on program output. Cut to a stable source first.
- If audio and video drift, decide whether to fix, switch, or simplify before viewers become the monitoring system.
- Keep incident language factual and calm: "We are restoring the remote guest feed" beats "Everything is broken."

## Recording, ISOs, And Handoff

Define records before the event:

- program with graphics and captions as seen by audience;
- clean feed without graphics;
- isolated camera feeds;
- isolated remote guest feeds;
- multitrack audio or stems;
- slides, playback files, graphics package, caption files, transcript, chat/Q&A export;
- telemetry, incident log, run of show with actual times.

Handoff package should include:

- final recording locations and checksums if needed;
- file naming and storage owner;
- known issues and timestamps;
- rights/usage limits;
- caption/transcript status;
- replay publishing instructions;
- postmortem notes and recommended fixes.

Production heuristic: record locally when possible even if the platform records. Platform recordings can start late, omit clean feeds, miss ISOs, downmix audio, or exclude captions/chat.

## Example: 75-Minute Hybrid Panel Plan

This is an example, not a mandatory formula.

Brief:

- Audience: 800 online, 120 in room.
- Format: hybrid keynote plus panel plus moderated Q&A.
- Requirement: captions, replay, sponsor lower thirds, chat questions.
- Latency: low enough for Q&A but not bidirectional audience video.
- Failure tolerance: stream can cut to host or slate, but not stop.

Recommended plan:

- Delivery: platform/CDN HTTP delivery in low-latency mode if destination supports it; avoid WebRTC audience delivery because only Q&A text needs interactivity.
- Contribution: in-room cameras/switcher local; remote panelist via tested conferencing/WebRTC contribution into production; backup phone audio for remote panelist.
- Audio: room lavs plus audience question mic; remote panelist mix-minus; host mic priority; spare handheld on stage.
- Graphics: title, agenda, lower thirds, sponsor bug, Q&A prompt, break/technical slates.
- Crew: producer, TD, audio, stream engineer, stage manager, moderator, caption lead, graphics operator, recording manager.
- Redundancy: primary wired internet plus separate cellular/bonded backup; backup encoder profile to backup ingest; local program record plus platform record; remote panelist backup slides/video if they drop.
- Rehearsal: line check day before; remote panelist 30-minute tech check; cue-to-cue with host and moderator; failure drill for lost remote panelist.

Sample run-of-show rows:

| Time | Segment | Program | Audio | Graphics | Cue | Fallback |
| --- | --- | --- | --- | --- | --- | --- |
| -00:10 | Holding | animated slate | music low | event title + captions notice | stream engineer confirms ingest | static slate from encoder |
| 00:00 | Open | camera 1 host | host lav | lower third host | producer: "Host, live in 5" | keep slate, host audio only |
| 00:08 | Remote panelist intro | 2-box host/guest | host + guest mix-minus | guest lower third | stage manager confirms guest ready | host summarizes guest point |
| 00:45 | Q&A | host camera, question cards | host + room mic | Q&A lower third | moderator feeds approved questions | prepared backup questions |
| 01:10 | Close | camera 1 host | host lav | thank-you/end card | producer: "Hard out in 2" | end card plus music |

## Example: Incident Decision Tree

This is an example, not a mandatory formula.

Symptom: platform reports unstable stream and audience monitor shows buffering.

1. Stream engineer checks encoder dropped frames, output bitrate, CPU/GPU, and network upload.
2. If encoder is overloaded: lower output profile or switch to backup encoder scene/profile.
3. If upload path is unstable: switch to backup network or bonded path; keep bitrate conservative until stable.
4. If platform ingest is unhealthy but local and network are stable: switch to backup ingest/destination if prepared.
5. If audience playback only is affected: check independent audience monitor, platform status, CDN/player reports, and chat volume before disrupting program.
6. Producer decides whether host acknowledges, moderator posts a status note, or show continues silently.
7. Recording manager marks incident timestamp and verifies local record is clean.

## Example: Transport Choice Summary

This is an example, not a mandatory formula.

| Scenario | Likely choice | Why |
| --- | --- | --- |
| Encoder to mainstream platform ingest | RTMPS if supported, otherwise platform-approved RTMP/SRT path | Common platform ingest pattern; encrypt ingest when available. |
| Venue camera to remote control room | SRT or managed contribution service | Tunable latency/recovery and controlled endpoints. |
| Large public audience playback | HLS or platform/CDN adaptive delivery | Broad device/CDN scale and adaptive bitrate. |
| Remote guests talking naturally | WebRTC/conferencing/SFU path | Low-latency interactive media and data/control surfaces. |
| Audience asks text questions during keynote | HLS/platform delivery plus moderated chat/Q&A | Text can tolerate delivery latency if moderation windows are designed. |
| Live caller joins program | WebRTC/conferencing contribution into switched program | Requires moderation, consent, IFB/return audio, and quick removal path. |

## Source Notes Verified 2026-07-11

- HLS documented facts: RFC 8216, "HTTP Live Streaming," August 2017, https://www.rfc-editor.org/rfc/rfc8216
- WebRTC API documented facts: W3C Recommendation, "WebRTC: Real-Time Communication in Browsers," 13 March 2025, https://www.w3.org/TR/webrtc/
- WebRTC transport documented facts: RFC 8835, "Transports for WebRTC," January 2021, https://www.rfc-editor.org/rfc/rfc8835
- WebRTC RTP/media documented facts: RFC 8834, "Media Transport and Use of RTP in WebRTC," January 2021, https://www.rfc-editor.org/rfc/rfc8834
- WebRTC stats documented facts with volatility note: W3C Candidate Recommendation Draft, "Identifiers for WebRTC's Statistics API," latest fetched version dated 25 September 2025, https://www.w3.org/TR/webrtc-stats/
- Accessibility/captions documented facts: W3C WAI captions and planning pages, updated 17 September 2024, https://www.w3.org/WAI/media/av/captions/ and https://www.w3.org/WAI/media/av/planning/
- U.S. captioning regulatory reference: FCC, "Closed Captioning of Video Programming on Television," page updated April 8, 2026, https://www.fcc.gov/general/closed-captioning-video-programming-television
- U.S. IP-delivered video captioning regulatory reference: eCFR, 47 CFR § 79.4, "Closed captioning of video programming delivered using Internet protocol," fetched 2026-07-11, Title 47 displayed current as of 2026-07-09, https://www.ecfr.gov/current/title-47/chapter-I/subchapter-C/part-79/section-79.4
- SRT protocol/source notes: Internet-Draft, "The SRT Protocol," draft-sharabayko-srt-00, expired 9 September 2021, https://datatracker.ietf.org/doc/html/draft-sharabayko-srt-00; Haivision SRT API and SRT API Socket Options, fetched 2026-07-11, https://github.com/Haivision/srt/blob/master/docs/API/API.md and https://github.com/Haivision/srt/blob/master/docs/API/API-socket-options.md
- Volatile platform facts: YouTube Help, "Choose live encoder settings, bitrates, and resolutions," fetched 2026-07-11, https://support.google.com/youtube/answer/2853702
