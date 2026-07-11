# Evaluation: livestream-event-production

Do not expose this file to the agent being evaluated. Evaluate the agent using `SKILL.md` only, then score with this rubric.

## Evaluation Goals

The skill should make an agent capable of planning and troubleshooting provider-independent live or hybrid livestream productions. A strong answer should integrate production craft, live show control, network/transport reasoning, accessibility, moderation, incident response, and handoff. It should not collapse into a single platform tutorial or a post-production editing workflow.

## Critical Failure Conditions

Score the response as failing regardless of polish if it:

- treats the task as recutting, editing, or summarizing an already recorded stream instead of live production;
- depends on one named provider, dashboard, API, or platform as the core solution when the prompt asks for provider-independent production;
- omits run of show, crew/roles, audio, encoding/ingest, monitoring, and incident response from a production plan;
- recommends live streaming without addressing consent, rights, moderation, or accessibility when those are relevant to the scenario;
- invents standards/platform facts without citations, dates, or caveats;
- presents volatile platform settings as universal rules;
- gives unsafe operational advice such as sharing stream keys broadly, relying on untested failover, ignoring captions when required, or routing delayed program audio back to presenters.

## Scoring Rubric

Score out of 100.

### 1. Scope Fit And Production Framing (10 points)

- 10: Clearly frames the work as live/hybrid event production and covers show plus network/service operations.
- 7: Mostly correct but misses one major live-production dimension.
- 4: Generic streaming advice with limited show-control thinking.
- 0: Post-production, platform-only, or unrelated content.

### 2. Brief, Run Of Show, And Crew Plan (15 points)

- 15: Produces a timed run of show with cues, owners, sources, fallbacks, interaction moments, and clear crew accountability.
- 11: Covers run of show and crew but lacks cue/fallback specificity.
- 7: Mentions schedule and roles but not operationally useful during a live show.
- 0: No meaningful run of show or crew model.

### 3. Capture, Audio, Graphics, And Switching (12 points)

- 12: Plans camera/source inventory, audio routing/mix-minus, graphics states, slates, switching, and hybrid-room needs.
- 9: Covers most elements but underdevelops audio or graphics.
- 5: Lists gear without signal-flow or operator implications.
- 0: Ignores live capture/switching/audio.

### 4. Encoding, Ingest, Transport, And Latency Reasoning (18 points)

- 18: Correctly separates contribution, ingest, and delivery; explains appropriate RTMP(S), SRT, HLS, and WebRTC roles; ties latency to interaction design; states platform facts as volatile.
- 14: Good transport guidance with minor omissions or weak caveats.
- 9: Knows some protocols but confuses ingest with delivery or latency with bitrate.
- 4: Protocol name-dropping with little operational reasoning.
- 0: Fundamentally wrong transport guidance.

Expected substance:

- RTMP/RTMPS: common platform ingest/contribution; RTMPS encrypts when supported; not modern browser delivery.
- SRT: useful for controlled contribution over imperfect networks; latency/recovery/encryption/connection role support must be verified per tool.
- HLS: segmented HTTP adaptive delivery using playlists/segments/variants; good for broad scale, not exact synchronized interactivity.
- WebRTC: low-latency interactive media/data using ICE/STUN/TURN, DTLS-SRTP/RTP/SCTP; requires architecture such as SFU/relay for scale.

### 5. Network, Redundancy, Rehearsal, And Go/No-Go (12 points)

- 12: Plans bandwidth headroom, independent backup paths, failover levels, rehearsal types, and go/no-go checks.
- 9: Solid redundancy plan but misses rehearsal or go/no-go detail.
- 5: Says "have backup internet" without independence/load testing.
- 0: No redundancy or rehearsal thinking.

### 6. Accessibility, Captions, Moderation, Consent, And Rights (12 points)

- 12: Treats captions/accessibility as production requirements, references live caption needs, and includes moderation, consent, rights, privacy, and safety escalation.
- 9: Covers most but with shallow accessibility or rights handling.
- 5: Mentions captions/moderation without operational routing.
- 0: Ignores accessibility and safety constraints.

### 7. Monitoring, Incident Response, Recording, And Handoff (14 points)

- 14: Monitors local program, encoder, network, ingest, audience playback, captions, and recording; provides incident workflow and complete handoff package.
- 10: Good monitoring and incidents but incomplete recording/handoff.
- 6: Basic stream-health advice only.
- 0: No incident or handoff plan.

### 8. Evidence Quality And Fact Labeling (7 points)

- 7: Clearly distinguishes documented facts, volatile platform facts, and production heuristics with citations/dates.
- 5: Cites some facts but labels are inconsistent.
- 3: Mostly uncited or mixes heuristics with standards.
- 0: Fabricates or overclaims.

## Test Prompts

Use any combination of these prompts to evaluate performance.

### Test 1: Hybrid Panel Production Plan

Prompt:

> Plan a 75-minute hybrid executive panel for 500 online viewers and 80 in-room attendees. It needs captions, moderated Q&A, replay, two in-room cameras, one remote speaker, sponsor lower thirds, and a backup plan. Keep it provider-independent.

Strong answer should include:

- event assumptions and missing questions;
- crew plan with producer, TD/switcher, audio, stream engineer, moderator, captions lead, stage manager/guest wrangler, graphics, recording;
- timed run of show with opening, panel, Q&A, close, cues, graphics, sources, fallback;
- hybrid audio plan including room mics, lavs/handhelds, remote mix-minus, audience question mic, headphones/echo prevention;
- graphics package including lower thirds, sponsor bug, title, Q&A prompt, slates;
- remote speaker tech check and backup phone/audio or prerecorded fallback;
- ingest/delivery plan and latency choice for moderated Q&A;
- redundancy: wired primary, independent backup, backup ingest/encoder profile, local record;
- captions and accessibility route;
- moderation, consent, rights, privacy;
- monitoring and incident plan;
- recording/handoff package.

Weak answer signs:

- only recommends a platform;
- ignores captions route;
- no run of show or failure drill;
- treats chat/Q&A as magically synchronized without latency buffer.

### Test 2: Transport Decision

Prompt:

> I have three live needs: a venue camera feeding a remote control room, a large public audience, and four remote guests who must talk naturally with the host. Explain which transport patterns you would use and why.

Strong answer should say:

- venue camera to remote control room: SRT or a controlled contribution path may fit, with tested latency/recovery/encryption/firewall roles;
- large public audience: HLS/platform/CDN adaptive delivery for scale, with latency caveats;
- remote guests: WebRTC/conferencing/SFU-style contribution for conversational latency;
- final program to platform ingest: RTMPS if supported or platform-approved ingest path;
- contribution, ingest, and delivery are separate layers;
- tool/platform specifics must be verified before show day.

Weak answer signs:

- says WebRTC should always be used for every viewer without scaling caveats;
- says HLS is for remote guest conversation;
- treats RTMP as audience playback;
- ignores latency/reliability tradeoffs.

### Test 3: Incident Diagnosis

Prompt:

> Ten minutes into a live stream, viewers report buffering. The host looks fine on the local program monitor. The encoder shows intermittent dropped frames and the platform health dashboard says unstable bitrate. What do you do?

Strong answer should include:

- confirm symptom across local program, encoder, network, ingest, and independent audience monitor;
- preserve program by staying on host/slate as needed;
- check encoder CPU/GPU, output bitrate, keyframe, dropped frames, audio, reconnects;
- check upstream throughput, packet loss/jitter, router/interface/cellular/bonding status;
- lower bitrate/profile only if appropriate and preferably via rehearsed profile;
- switch to backup network/encoder/ingest if criteria are met;
- producer controls communication to host/moderator/audience;
- recording manager marks timestamp and verifies local record;
- avoid speculative blame and keep incident log.

Weak answer signs:

- tells the host to keep talking while operators randomly restart things;
- immediately restarts the stream with no containment;
- ignores local recording;
- ignores audience communication.

### Test 4: Accessibility And Compliance

Prompt:

> The client says, "Captions would be nice, but we can just turn on auto captions if there is time." The event is a public educational livestream with replay. How should the production plan respond?

Strong answer should include:

- identify captions/accessibility as a requirement to verify, not a nice-to-have;
- note that live video with audio may require live captions for WCAG Level AA contexts;
- automatic captions are insufficient unless confirmed fully accurate;
- plan professional live captioning/CART or verified accurate caption workflow;
- route captions into live stream and replay/transcript handoff;
- protect caption display area from graphics;
- provide captioner prep materials;
- verify jurisdiction/regulatory obligations and client policy.

Weak answer signs:

- accepts auto captions with no accuracy/correction plan;
- ignores replay captions/transcripts;
- treats captions as post-production only.

### Test 5: Go/No-Go Readiness

Prompt:

> Build a go/no-go checklist for a high-stakes livestream launch with a remote CEO, live product demo, captions, and media embargo constraints.

Strong answer should include:

- ingest and backup ingest ready;
- encoder, network, backup path, power, and monitoring checks;
- CEO remote audio/video/lighting/network/backup comms verified;
- demo source stable with prerecorded or screenshot fallback;
- captions live and monitored;
- lower thirds/legal/sponsor/media embargo copy verified;
- moderator and incident escalation ready;
- stream keys private;
- local and platform recording armed;
- stakeholder final approval;
- explicit no-go thresholds and who decides.

Weak answer signs:

- generic checklist without no-go thresholds;
- no embargo/privacy handling;
- no demo fallback;
- no caption verification.

## Answer Key Concepts

An evaluated agent should demonstrate these concepts without needing exact phrasing.

### Live Production Is A Control System

Good responses treat the show as a timed control surface with sources, cues, operators, fallbacks, comms, and audience-visible consequences. They avoid vague advice like "make sure everything works" unless backed by a rehearsal/checklist mechanism.

### Latency Is A Product Decision

Good responses choose latency based on interaction. Normal-latency delivery is acceptable for one-way broadcasts. Low latency matters for chat/Q&A timing. WebRTC or equivalent real-time architecture matters for bidirectional conversation. Lower latency should be presented as a reliability tradeoff.

### Protocols Have Roles

Good responses separate:

- contribution: camera/remote source into production;
- ingest: finished stream into platform/CDN/packager;
- delivery: player/audience playback.

They avoid saying one protocol solves every layer.

### Audio Is Priority

Good responses protect host/program audio, plan mix-minus, avoid echo, define return audio, and include backup audio. They do not focus only on camera quality.

### Accessibility Is Operational

Good responses route captions, monitor captions, prepare captioners, protect screen layout, and include replay/transcript handoff. They do not treat accessibility as a final note.

### Incidents Need Containment

Good responses first contain audience impact, then diagnose. They name who decides, who communicates, what is logged, and what fallback is used.

## Calibration Examples

### Excellent Response Excerpt

> I would treat the remote CEO as a contribution source, not as the delivery architecture. The CEO joins through a tested low-latency contribution path with headphones, backup phone audio, and a pre-cleared still/title fallback. The final program goes to the audience through the chosen platform/CDN path, with RTMPS ingest if supported and a backup ingest ready. Because audience interaction is Q&A rather than live caller video, I would use a low-latency platform mode only if it passed rehearsal; otherwise I would design moderated Q&A windows that tolerate audience delay.

Why excellent: separates source/contribution from delivery, selects latency by interaction, includes backup, does not overclaim platform details.

### Poor Response Excerpt

> Use WebRTC because it is always real time and better than HLS. Stream everything through one browser tab, turn on auto captions, and tell viewers to refresh if it buffers.

Why poor: overclaims WebRTC, ignores scale and redundancy, treats auto captions casually, lacks incident handling.

## Minimum Passing Standard

A minimum passing answer should:

- produce a workable run of show or checklist for the given scenario;
- assign named live-production responsibilities;
- choose transport/delivery patterns with correct high-level protocol roles;
- include captions/accessibility where relevant;
- include moderation/consent/rights where relevant;
- include monitoring, fallback, and recording/handoff;
- label uncertain or platform-specific facts.

Responses below this standard should not pass even if they are well-written.
