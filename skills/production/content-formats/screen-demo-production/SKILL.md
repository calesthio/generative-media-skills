---
name: screen-demo-production
description: Provider-independent workflow for producing terminal, IDE, documentation, browser, desktop, and application demonstration videos. Use when choosing authentic capture, browser automation, synthetic UI, or hybrid treatment; scripting actions and narration; resetting demo state; protecting secrets and personal data; directing cursor/callouts; creating crop variants; and reviewing workflow truth, readability, accessibility, and provenance.
---

# Screen demo production

Use this skill when the central evidence is an interface being operated over time: commands run, files change, controls activate, application state changes, or a workflow completes.

This is broader than SaaS marketing. It covers instructional, support, onboarding, engineering, release-note, internal-training, terminal, IDE, browser, desktop, remote-desktop, and multi-application demonstrations.

## Evidence stance

- **Documented fact:** behavior from official capture/automation, accessibility, privacy, or security sources.
- **Production heuristic:** a practical direction choice to test with the audience and final raster.
- **Empirical observation:** a result verified in the actual product/build, rehearsal, capture, or render.

Tool and OS behavior is volatile. Facts were verified **2026-07-12**. Record product/build, browser/OS, automation/capture versions, fixtures, mocks, and permissions.

## Classify the truth claim

Every demo must declare one:

- **Authentic capture:** pixels come from the stated product or OS during an actual run.
- **Controlled authentic capture:** the real UI runs with seeded data, fixed time, mocked dependencies, automation, or other material controls. Disclose them.
- **Illustrative synthetic:** terminal or UI is recreated for explanation or pacing. Never describe it as a recording of a real run.
- **Hybrid:** authentic pixels combined with synthetic cursor, typing, callouts, timing reconstruction, or other layers. Record each component.

Choose the least invasive mode that supports the intended claim. Synthetic UI is appropriate for conceptual or privacy-sensitive explanation; browser automation for repeatable real web flows; OS/window capture when native chrome, terminal/IDE behavior, permissions, or cross-app interaction matters.

Do not present simulated data or mocked services as proof of live performance, security, a transaction, benchmark, or customer outcome.

## Boundaries

This skill owns capture-mode choice, workflow scripting, reset, privacy review, readability, cursor/callout direction, narration/caption synchronization, aspect variants, retakes, QA, and provenance.

It does not replace generic Playwright/test architecture, campaign positioning, website visual showcases without an operational workflow, general editing craft, or application accessibility conformance testing.

## Build the demo contract

Define:

- audience, task, prerequisite, expected result, and truthful claim;
- product/build/commit, environment, account role, locale, timezone, clock, viewport, DPI/scale, theme, and feature flags;
- authentic/controlled/synthetic/hybrid classification;
- fixture data and reset procedure;
- actions, readiness signals, failure branches, narration, captions, cursor, callouts, and holds;
- do-not-show list and privacy/security approvers;
- master and variant dimensions, duration, fps, caption/callout safe areas;
- capture tool, codec, audio sources, and post-produced layers;
- provenance ledger and review gates.

Use a shot ledger:

```text
beat | claim | start state | action | readiness signal | result | narration | cursor/callout | hold | reset
```

## Reset by construction

Prefer disposable directories, dedicated demo accounts, seeded fixtures, idempotent reset endpoints, fixed locale/timezone/clock, pinned dependencies, blocked notifications, and versioned mocks.

A fresh browser context isolates browser storage such as cookies and local storage, but it does not reset external database or account state. Test reset plus workflow repeatedly before recording. Every nondeterministic branch becomes an explicit branch, controlled dependency, or reason to change capture mode.

## Browser automation capture

**Documented facts from Playwright:**

- Browser contexts isolate session state.
- Locator actions auto-wait for actionability such as visibility, stability, event reception, and enabled state where applicable.
- Playwright discourages `networkidle` as a readiness signal and identifies fixed `waitForTimeout()` delays as flaky.
- Videos are finalized when the browser context closes; viewport and video size should be explicit because default video scaling can reduce the output.
- Stored authentication state can impersonate an account and should not be committed.
- Traces and HAR files can contain screenshots, DOM, network, console, headers, cookies, bodies, timing, and optionally source files.

Wait for business-observable states: exact URL, response, heading, status message, enabled control, updated row, or persisted result. Separate machine readiness from viewer pacing: assert the state, then add an editorial hold.

Mock only what the truth claim permits. Disclose mocked external systems or fixed clocks. A controlled authentic UI can remain valid evidence of interface behavior, but not of the mocked provider's real response or speed.

Treat video, trace, HAR, logs, storage state, screenshots, and console output as separate sensitive artifacts. Scrubbing one does not sanitize the others.

## Real screen/window capture

Browser `getDisplayMedia()` requires current user activation and a fresh user choice of surface; audio support varies. Operating-system capture may require permission and may display capture indicators.

For real capture:

- select the narrowest window/surface;
- close private apps, notifications, password managers, personal browser profiles, and unrelated terminals;
- use a clean desktop/account and neutral wallpaper/menu bar where needed;
- hide bookmarks, history, local paths, usernames, hostnames, API keys, tokens, email, customer data, clocks, and internal URLs;
- test native dialogs, permissions, scaling, cursor, and audio;
- capture handles before/after each action for editing.

Do not rely on crop or blur as the only privacy strategy. Avoid recording sensitive pixels in the first place.

## Synthetic terminal and UI

Synthetic output is useful when commands/results are known, validated, privacy-sensitive, or need exact narration timing.

- Validate commands/results in a disposable fixture when claiming they are representative.
- Preserve exact line wrapping, prompt, width, timing, errors, and state transitions.
- Label fixture-validated synthetic output accordingly; if not validated, label it illustrative.
- Do not invent product capabilities, benchmark numbers, network responses, or security outcomes.
- Keep source transcript and generation rules in provenance.

Synthetic reconstruction should improve legibility and pacing, not falsify what happened.

## Direct actions, cursor, and callouts

Narrate intent before action and interpret the result afterward. Avoid speaking a changing label at the exact moment it changes.

Production heuristics:

- park the cursor while narration carries meaning;
- move directly, settle, click once, and leave only when needed;
- do not circle targets continuously;
- use one emphasis device at a time;
- never cover the target, focus indicator, error, or result;
- distinguish a post-produced cursor/click ring from authentic pixels in provenance;
- hold complex results long enough to read at final size.

An automation assertion can complete faster than a viewer can comprehend. Add an editorial hold after readiness, not arbitrary sleeps before it.

## Narration, captions, and visual description

Narration should explain purpose and consequence, not repeat every control label. Use exact UI names where they help task completion.

Prerecorded synchronized media with meaningful audio needs captions. Important visual-only state changes should be conveyed in narration, transcript, or audio description as required. Captions must not cover controls, errors, code, or output.

Run three tests:

- muted: can a viewer follow actions/results through captions and visual direction?
- audio-only: are essential outcomes described?
- final-size: can UI, code, terminal text, callouts, and captions be read?

## Privacy, security, and claims

Minimize collection and capture only what serves the declared purpose. Establish access controls, retention, deletion, and reviewer responsibility for raw captures and diagnostic artifacts.

Scrub:

- secrets, API keys, tokens, passwords, auth state, cookies, QR codes;
- names, emails, faces, avatars, customer IDs, payments, health/HR/legal data;
- internal hosts, paths, tickets, analytics, unreleased flags, admin controls;
- notifications, autofill, clipboard, browser history, source maps, logs;
- metadata and filenames as well as visible pixels.

Do not claim that a digital signature or C2PA record proves the depicted workflow occurred or that every assertion is true. Provenance can make signed records tamper-evident and record ingredients/actions.

## Readability and variants

Design from the final delivery raster:

- enlarge terminal/IDE/UI text before capture;
- remove irrelevant panels and chrome;
- choose viewport and device scale deliberately;
- keep contrast and focus indicators readable;
- zoom into evidence, then restore context;
- avoid compression-sensitive tiny text and one-pixel lines.

Author portrait and square variants as compositions. Center-cropping desktop footage often removes navigation, labels, or result state. Re-run or recompose when the workflow does not fit.

## Retakes and continuity

Retake by state-bounded beat or chapter. Save handles around transitions. Keep a take log with fixture/build, start/end state, failures, and selected take.

Editing may remove waits, but must not create impossible causal order, hide an error that changes the claim, or present a later success as the immediate result of a failed action.

## QA and provenance

Verify:

1. claim and truth classification;
2. exact build, account role, fixture, mocks, clock, locale, and reset;
3. repeated workflow success and handled failures;
4. no PII/secrets across video, audio, trace, HAR, logs, captions, metadata, thumbnails;
5. action-result continuity and honest timing edits;
6. cursor/callout restraint and final-size readability;
7. captions, visual description, contrast, and flashing;
8. aspect variants preserve all required steps/results;
9. codec, dimensions, fps, audio, and output integrity;
10. provenance ledger and hashes.

## Example 1: fixture-validated synthetic CLI

This is a complete example, not a mandatory formula.

**Intent:** 32-second tutorial of fictional `acme deploy` without showing a real shell or secrets.

Validate commands in a disposable fixture using UTC, fixed locale/terminal width, temporary home, seed `demo-17`, and a local fake endpoint. Save only approved output. Render synthetic terminal at 1920x1080 with large mono type and make a separate 1080x1920 layout.

```text
$ acme init storefront --seed demo-17
Created storefront/acme.yaml

$ acme deploy --environment preview
Building 6 assets...
Preview ready: https://preview.example.test/storefront

$ acme status
storefront  preview  healthy  revision 8c41d2
```

Timeline: establish objective; type/run init; hold created-file result; deploy with deterministic progress; hold URL; run status; hold healthy state. Narration introduces intent and interprets result. Rebuild from transcript for every take and label it “synthetic terminal demonstration based on fixture-validated output.”

**Likely failure:** output was not actually validated. Relabel as illustrative or validate before publication.

## Example 2: controlled authentic browser flow

This is a complete example, not a mandatory formula.

**Intent:** 45-second support training showing an operator resolving a staged order issue.

Seed a dedicated account/order/ticket through an idempotent reset. Freeze time/locale, block notifications/analytics, and disclose a mocked external shipping provider. Use a fresh context, protected auth state, and explicit 1920x1080 viewport/video size.

Wait for exact headings/statuses and response/state changes; do not use sleeps or `networkidle`. Rehearse with trace, then scrub/delete diagnostic artifacts and capture a clean run. A post-produced cursor settles before targets. Run reset and flow three times. QA PII, captions, console/network errors, mocked-service disclosure, final crops, and ledger of build/fixture/automation/cursor edits.

**Likely failure:** the success UI appears but persistence is not verified. Add an observable persisted-state assertion before the editorial hold.

## Sources

Verified 2026-07-12:

- Playwright actionability, contexts, locators, navigation, network, mocking, video, tracing, auth, and clock: https://playwright.dev/docs/
- W3C Screen Capture and MDN `getDisplayMedia`: https://www.w3.org/TR/screen-capture/ and https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getDisplayMedia
- Microsoft screen capture: https://learn.microsoft.com/en-us/windows/apps/develop/media-authoring-processing/screen-capture
- Apple ScreenCaptureKit: https://developer.apple.com/documentation/screencapturekit
- WCAG 2.2 captions, audio description, contrast, reflow, and flashing: https://www.w3.org/WAI/WCAG22/Understanding/
- W3C Privacy Principles: https://www.w3.org/TR/privacy-principles/
- NIST SP 800-122 and Privacy Framework: https://csrc.nist.gov/pubs/sp/800/122/final and https://www.nist.gov/privacy-framework
- C2PA specification index: https://spec.c2pa.org/