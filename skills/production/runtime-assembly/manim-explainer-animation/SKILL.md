---
name: manim-explainer-animation
description: Provider-independent production workflow for creating Manim-based explainer animations. Use when an agent must plan, code, render, QA, or hand off precise math, science, data, diagram, algorithm, or concept animations with Manim, including storyboard, scene architecture, formulas, coordinate systems, voiceover timing, accessibility, reproducibility, provenance, and delivery decisions.
---

# Manim Explainer Animation

Use this skill to produce explainer animations where the explanation depends on precise symbolic, geometric, graphical, algorithmic, or diagrammatic motion. Treat Manim as a programmable explanation instrument, not as a generic video renderer.

## Evidence labels

- **Documented fact** means behavior or requirements grounded in official documentation or standards listed in Sources.
- **Production heuristic** means a practical rule for reliable explainer production; adapt it to the brief.
- **Escalation trigger** means stop and ask the user, subject-matter expert, counsel, or platform owner before proceeding.
- **Volatile fact** means package versions, CLI flags, platform delivery rules, API behavior, pricing, and model/provider availability. Re-check them at production time.

## Choose Manim deliberately

Choose Manim when at least one of these is central to the deliverable:

- Equations, transformations, proofs, geometry, vector fields, graphs, number lines, coordinate systems, algorithms, state machines, data graphics, or technical diagrams need exact positions and repeatable motion.
- The visual argument should be reproducible from code and easy to revise after expert feedback.
- The animation needs symbol continuity: the same variable, color, axis, object, or state must retain meaning over time.
- The project benefits from render-in-the-loop iteration: code, render, inspect, patch, and render again.

Prefer another compositor or video tool when:

- The piece is primarily live action, cinematic camera language, textured brand motion, character performance, UI capture, or social-first kinetic typography.
- The user wants a photorealistic or heavily designed motion-graphics look that would be faster in After Effects, Remotion, HyperFrames/GSAP, Blender, or a video model.
- The explanation can be communicated with a static diagram plus narration and does not need precise temporal construction.

Hybridize when useful: render Manim scenes as transparent or full-frame segments, then finish in a compositor for music, captions, brand lower-thirds, live footage, or platform-specific packaging.

## Start with the explanation, not the code

Before writing Manim code, produce a short production brief:

1. Audience and prerequisite knowledge.
2. One-sentence learning objective.
3. Core misconception or tension.
4. Exact facts, formulas, datasets, or domain claims that need SME/source approval.
5. Runtime, aspect ratio, expected narration style, and delivery platform.
6. Constraints: brand palette, fonts, captions, localization, accessibility, source attribution, or no-audio viewing.

Then create a concept breakdown:

- **Objects:** every meaningful visual object and what it represents.
- **Symbols:** variables, colors, labels, units, coordinate frames, and their meanings.
- **Actions:** what changes over time and why each change teaches something.
- **Cognitive load:** what is visible, highlighted, hidden, or faded at each beat.
- **Verification:** what a reviewer can check visually and mathematically.

Escalate before production if the script makes medical, legal, financial, safety, engineering, scientific, or educational claims whose correctness matters beyond style.

## Storyboard as teachable beats

Write the storyboard as a table or structured list with these fields:

- `time`: planned start and end seconds.
- `narration`: exact or near-final line.
- `visual_state`: what is on screen at the start of the beat.
- `animation`: specific Manim action, transformation, camera move, graph reveal, or diagram update.
- `learning_purpose`: why this visual action helps.
- `assets_or_data`: formulas, data files, SVGs, images, fonts, or cited sources.
- `qa_checks`: render, math, contrast, layout, captions, and flashing checks.

Production heuristics:

- One conceptual change per beat. If the narration says two things, either split the beat or use a clear visual hierarchy.
- Prefer transformation over replacement. Viewers learn continuity when `a` becomes `a^2`, a dot moves along the curve, or a node changes state instead of disappearing.
- Use reveal order as pedagogy: show the question, then the object, then the rule, then the consequence.
- Keep a persistent anchor: an equation, axis, diagram skeleton, or legend that stays stable while details change.
- Use pauses intentionally. A short `wait()` after a difficult transformation often teaches more than another animation.

## Scene architecture

Documented fact: Manim scripts generally define classes derived from `Scene`, put animation code in `construct()`, manage visual objects as mobjects, and play animations with `Scene.play()`.

Build scenes as production code:

- Use one class per logical chapter or render segment, not one giant scene for the whole video unless it is very short.
- Put palette, fonts, dimensions, durations, and symbol colors in named constants.
- Write helper functions for repeated constructs such as axes, formula rows, callout boxes, graph labels, and algorithm nodes.
- Keep a symbol ledger near the top of the file: `x = yellow`, `rate = blue`, `area = green`, etc.
- Keep units explicit in code comments when coordinates are conceptual rather than screen-space.
- Avoid magic coordinates. Use named anchors, `next_to`, `align_to`, `to_edge`, `arrange`, `VGroup`, and axis conversion methods such as `c2p()`/`coords_to_point()` where appropriate.
- Prefer small scene methods: `introduce_problem()`, `build_axes()`, `show_invariant()`, `compare_cases()`, `conclude()`.
- Use deterministic inputs. Pin the Python package set, record Manim version, keep source data local, and set explicit random seeds when randomness is used.

Example project skeleton:

```text
project/
  pyproject.toml or requirements.txt
  scenes/
    main.py
    theme.py
    data/
      measurements.csv
    assets/
      logo.svg
  renders/
  captions/
  README-production-notes.md  # outside this skill; for the user's project handoff
```

Example `theme.py` pattern:

```python
from manim import *

BG = "#0B1020"
FG = "#F6F7FB"
MUTED = "#8A93A6"
ACCENT = "#FFD166"
BLUE = "#4CC9F0"
GREEN = "#80ED99"
RED = "#FF5C8A"

TITLE_SIZE = 46
BODY_SIZE = 30
FORMULA_SIZE = 42

def title(text: str) -> Text:
    return Text(text, font="Inter", color=FG, font_size=TITLE_SIZE)

def caption(text: str) -> Text:
    return Text(text, font="Inter", color=MUTED, font_size=24)
```

## Coordinate systems and layout

Documented fact: Manim provides mobjects for coordinate systems such as `Axes` and `NumberPlane`, and `Axes` exposes methods including coordinate-to-point conversion, graph labels, and line graph plotting.

Production rules:

- Distinguish scene coordinates from mathematical coordinates. A scene point `(2, 2, 0)` is not necessarily the point `(2, 2)` on your conceptual axes unless the plane is the default frame or you convert through the axis object.
- Build all points on a graph through the graphing object: `axes.c2p(x, y)`, `axes.plot(...)`, `axes.get_lines_to_point(...)`.
- Leave a safe margin for captions, platform UI, and mobile cropping.
- Reserve stable areas: formulas top/left, visualization center, explanatory labels near objects, captions lower third unless burned captions require another layout.
- When using 3D, first ask if 3D is necessary. 3D can clarify surfaces and vector geometry, but it can also hide relationships. Provide orientation cues, axes labels, and camera moves that are slow enough to track.
- In vertical videos, reduce simultaneous objects and use stacked transformations; do not simply crop a 16:9 coordinate plane.

## Typography, formulas, and symbol continuity

Documented fact: Manim supports normal text mobjects and LaTeX-based `Tex`/`MathTex`; extra LaTeX packages can be added through a `TexTemplate`; `MathTex` can isolate substrings so parts can be colored or transformed reliably.

Production rules:

- Use `Text` for plain language labels and `MathTex`/`Tex` for mathematical notation.
- Keep formulas large. If an equation has more than one line, animate it as a derivation, not as a dense paragraph.
- Use `substrings_to_isolate`, double-brace splitting, or separate string arguments for symbols that need highlighting or transformation.
- Never color a symbol inconsistently without explaining the change.
- Use a formula ledger: symbol, meaning, color, first use, and any unit.
- For accessibility, write narration that says what the formula means; do not rely on viewers reading visual math alone.
- Test LaTeX locally before promising delivery. Missing TeX packages, fonts, and OS differences are common production blockers.

Formula transformation pattern:

```python
start = MathTex(r"A", r"=", r"\pi", r"r^2", font_size=56)
expanded = MathTex(r"A", r"=", r"\pi", r"\cdot", r"3^2", font_size=56)
for mob in (start, expanded):
    mob.set_color_by_tex("A", YELLOW)
    mob.set_color_by_tex("r", BLUE)
self.play(Write(start))
self.play(TransformMatchingTex(start, expanded))
```

## Graph, data, diagram, and algorithm animation

For graphs:

- Define axis ranges and units before plotting.
- Label axes and units, even in stylized explainers.
- Animate the domain first, then the function or data, then annotations.
- Prefer a moving dot, tangent, area fill, or threshold line to communicate change over time.
- For datasets, record data source, timestamp, transformations, and any smoothing. Escalate if the data supports a consequential claim.

For diagrams:

- Separate logical model from visual style. First define nodes, edges, states, and transitions; then decide colors and motion.
- Keep spatial metaphors stable: left-to-right for time, top-to-bottom for hierarchy, concentric for containment, network for relationships.
- Use edge animation to show causality; use color/state changes to show status.
- If the diagram resembles an official architecture, system, or protocol, confirm with the source or SME.

For algorithms:

- Show input, invariant, state, operation, and output.
- Display a small worked example rather than a full-size problem.
- Use a pointer/cursor mobject for current index/state.
- Use a table or `VGroup` for memory/state when the algorithm depends on stored values.
- Narrate why an operation is valid, not just what line of pseudocode is running.

## Voiceover and timing alignment

Documented fact: Manim Voiceover is an official Manim Community plugin pathway that allows voiceover text to be attached to scene code and exposes duration tracking for aligning animations.

Use one of three timing modes:

1. **Silent/visual-first:** no narration; all meaning must be readable from visuals, titles, labels, and captions.
2. **Narration-led:** record or synthesize voice first, then time animations to the audio.
3. **Code-led with voiceover plugin:** use Manim Voiceover or a similar workflow to bind narration text to scene blocks and use tracker durations.

Production heuristics:

- Keep narration near 120-160 spoken words per minute for technical material unless the user requests a different style.
- Let difficult visuals breathe: avoid speaking a new concept while an equation is still transforming.
- Align visual emphasis with spoken emphasis. If narration says "the slope," highlight the slope at that moment.
- Export or create captions from the final timed script, not from an early draft.
- If using TTS, record the provider, model/voice, parameters, license constraints, and generated file paths. Re-check provider terms and availability at production time.

Voiceover timing pattern:

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class SlopeIntro(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService())
        axes = Axes(x_range=[0, 4], y_range=[0, 4]).add_coordinates()
        line = axes.plot(lambda x: x, x_range=[0, 3], color=YELLOW)

        with self.voiceover(text="A line's slope tells us how fast y rises as x moves right.") as tracker:
            self.play(Create(axes), run_time=tracker.duration * 0.35)
            self.play(Create(line), run_time=tracker.duration * 0.65)
```

## Accessibility and safety

Documented fact: WCAG 2.2 requires captions for prerecorded audio in synchronized media at Level A, except when the media is clearly labeled as a media alternative for text. WCAG 2.2 also includes a Level A flashing criterion: content should not flash more than three times in any one-second period unless below defined thresholds.

Production requirements:

- Provide captions for narrated exports unless the user explicitly states the video is a labeled media alternative for text.
- Include meaningful non-speech audio in captions when it affects understanding.
- Provide a transcript for educational, compliance, or no-audio contexts; include visual descriptions when the visuals carry essential meaning not spoken aloud.
- Avoid rapid full-screen flashes, high-contrast blinking, and repeated red flashes. If a visual alert is needed, use a slow pulse, outline, arrow, or label instead.
- Check color contrast for text and important labels. Do not encode meaning by color alone; pair color with labels, shape, position, or pattern.
- Avoid tiny formulas on mobile. Render a vertical preview or inspect at the expected device size.
- For motion sensitivity, avoid unnecessary camera spins, fast zooms, and jitter. Use direct cuts or slow transitions for dense technical content.

Escalate if the client requires formal accessibility conformance, regulated education compliance, medical/safety instruction, or public-sector delivery. Provide production evidence, but do not give legal advice.

## Asset custody and provenance

Maintain an asset ledger for every external input:

- source URL or local path;
- creator/owner if known;
- license or permission status;
- date accessed;
- transformations performed;
- whether the asset appears in the final render;
- whether there are privacy, consent, brand, or data-use concerns.

Documented fact: C2PA Content Credentials store provenance data in C2PA manifests; the specification explicitly warns that provenance data should not be treated as a value judgment about whether content is good or bad.

Production rules:

- Keep source code, datasets, rendered frames/video, audio, captions, and provenance notes together in the project handoff.
- If the platform or client requires Content Credentials/C2PA, use a compatible signing workflow and verify the final exported file after any post-processing. Re-check support for the target format at delivery time.
- Do not claim that C2PA proves truth. It can communicate origin, edits, and tamper-evident metadata when correctly implemented.
- For AI-generated narration, music, images, or code assistance, record tools, model names, prompts where appropriate, dates, and rights/terms notes.

Escalate for copyrighted textbook figures, proprietary datasets, brand assets without permission, student/medical/personal data, or any requirement that provenance metadata be legally binding.

## Render settings and delivery

Documented fact: Manim renders scene classes from files and writes output under a `media` directory by default, with quality-dependent output folders. Manim v0.19.0 documentation states that external FFmpeg was replaced with PyAV for core Manim installation, but FFmpeg remains useful for post-processing and delivery transcodes.

Development workflow:

- Render fast previews first: low quality and a single scene.
- Render exact sections when debugging layout or timing.
- Render final at the target aspect ratio, frame rate, and resolution.
- Inspect the final video after any post-processing, not just the Manim output.

Typical Manim commands to adapt after checking current docs:

```bash
manim -pql scenes/main.py SceneName      # quick local preview
manim -pqm scenes/main.py SceneName      # medium review
manim -pqh scenes/main.py SceneName      # high-quality review
manim -p --format=png scenes/main.py SceneName  # spot-check stills if supported in current version
```

Typical FFmpeg finishing tasks:

- combine separately rendered scene files;
- add or mux audio;
- transcode to H.264/AAC MP4 for broad compatibility;
- generate thumbnails or review stills;
- normalize loudness when required;
- burn captions only when the platform/client requires open captions.

Re-check platform delivery specs at production time. Social, LMS, broadcast, conference, and ad platforms change accepted codecs, aspect ratios, caption formats, file size limits, and safe-area overlays.

## Reproducibility package

For every serious Manim explainer, hand off:

- source code and exact render command;
- dependency file (`requirements.txt`, `pyproject.toml`, lockfile, or environment export);
- Manim version and renderer notes;
- OS or container details if relevant;
- source assets and data;
- final script and caption files;
- rendered output and thumbnails;
- asset/provenance ledger;
- known limitations and review notes;
- instructions for re-rendering a single scene and the final composition.

If the project uses generated voice, generated music, or external APIs, include enough metadata to reproduce or replace the asset. Do not assume API outputs are exactly reproducible unless the provider guarantees it and seeds/settings were recorded.

## QA workflow

Run QA in layers:

1. **Code QA:** imports cleanly, scene class names correct, no missing files, no hardcoded absolute paths unless intentional, dependencies recorded.
2. **Render QA:** preview render completes; final render completes; no cropped labels, overlapping captions, invisible text, missing glyphs, broken SVGs, or stuttering.
3. **Pedagogy QA:** each beat answers "what should the viewer learn now?"; no unexplained symbols; no visual contradiction with narration.
4. **Technical correctness QA:** formulas, units, graph scales, algorithms, and data transformations are reviewed by sources/SME when needed.
5. **Accessibility QA:** captions/transcript, contrast, color independence, mobile readability, flashing risk, motion comfort.
6. **Delivery QA:** final file opens, audio sync is correct, duration/aspect/codec meet target specs, captions are in the requested format.
7. **Provenance QA:** sources and generated assets are logged; required permissions and Content Credentials workflow are handled or escalated.

Use render-in-the-loop repair. When a render fails, inspect the first traceback, isolate the smallest scene, patch the cause, and rerender that scene before attempting the full video.

Common failure modes and repairs:

- **Formula will not compile:** simplify LaTeX, add required package to `TexTemplate`, check escaping, render a minimal test scene.
- **Symbol cannot be highlighted:** isolate substrings or split the formula into separate arguments.
- **Objects drift or overlap:** use layout containers and anchors rather than fixed coordinates.
- **Graph point is misplaced:** convert with `axes.c2p()` instead of scene coordinates.
- **Narration feels rushed:** split the beat, add pauses, or remove simultaneous motion.
- **Final output differs from preview:** check render quality, frame rate, aspect ratio, font availability, and post-processing command.

## Example: calculus micro-explainer

Example intent: create a 45-second narrated animation explaining "derivative as instantaneous rate of change" for high-school students.

Storyboard excerpt:

| Time | Narration | Visual | Animation | QA |
|---|---|---|---|---|
| 0-5s | "Average speed is distance over time." | Two points on a curve | Draw secant line between points | Labels readable |
| 5-15s | "Shrink the time window." | Same curve and secant | Move second point toward first | Dot follows curve; no axis mismatch |
| 15-28s | "The secant becomes a tangent." | Tangent at point | Transform secant to tangent | Formula matches visual |
| 28-40s | "That limiting slope is the derivative." | `f'(x)` formula | Highlight `\Delta x \to 0` then `f'(x)` | Formula color ledger |
| 40-45s | Recap | Curve, tangent, concise caption | Fade nonessential labels | Caption safe area |

Example Manim scene:

```python
from manim import *

class DerivativeAsLimit(Scene):
    def construct(self):
        self.camera.background_color = "#0B1020"
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 5, 1],
            x_length=7,
            y_length=4.5,
            axis_config={"color": "#8A93A6", "include_numbers": True},
        ).to_edge(DOWN)
        labels = axes.get_axis_labels(MathTex("t"), MathTex("s(t)"))

        curve = axes.plot(lambda x: 0.45 * (x - 1) ** 2 + 1, x_range=[0.2, 3.8], color="#4CC9F0")

        x0 = 1.35
        dx_tracker = ValueTracker(1.8)

        p0 = always_redraw(lambda: Dot(axes.c2p(x0, 0.45 * (x0 - 1) ** 2 + 1), color="#FFD166"))
        p1 = always_redraw(lambda: Dot(
            axes.c2p(x0 + dx_tracker.get_value(), 0.45 * (x0 + dx_tracker.get_value() - 1) ** 2 + 1),
            color="#80ED99",
        ))

        secant = always_redraw(lambda: Line(
            p0.get_center(),
            p1.get_center(),
            color="#FFD166",
        ).set_stroke(width=5))

        formula = MathTex(
            r"\text{slope}", r"=", r"\frac{\Delta s}{\Delta t}",
            font_size=48,
        ).to_edge(UP)
        formula.set_color_by_tex(r"\Delta", "#FFD166")

        limit_formula = MathTex(
            r"f'(t)", r"=", r"\lim_{\Delta t \to 0}", r"\frac{\Delta s}{\Delta t}",
            font_size=48,
        ).to_edge(UP)
        limit_formula.set_color_by_tex(r"\Delta", "#FFD166")
        limit_formula.set_color_by_tex(r"f'", "#80ED99")

        self.play(Create(axes), Write(labels))
        self.play(Create(curve))
        self.play(FadeIn(p0), FadeIn(p1), Create(secant), Write(formula))
        self.wait(0.5)
        self.play(dx_tracker.animate.set_value(0.18), run_time=4, rate_func=smooth)
        self.play(TransformMatchingTex(formula, limit_formula))
        self.play(Circumscribe(limit_formula[0], color="#80ED99"))
        self.wait(1)
```

Why this structure works:

- The two dots and secant are tied to the same axes through `axes.c2p()`.
- The shrinking interval is visible as motion, not merely described.
- The formula transforms only after the viewer has seen the geometric limit.
- Colors carry stable meaning: yellow for finite change, green for the derivative result.

Likely revisions:

- Add narration timing with Manim Voiceover.
- Add a lower-third caption zone and transcript.
- Add a second scene with a real velocity example if the audience needs concrete context.

## Example: algorithm explainer

Example intent: 60-second animation explaining binary search to a beginner.

Production plan:

- Use a row of sorted boxes for the array.
- Use three persistent pointers: `low`, `mid`, `high`.
- Gray out discarded halves; never remove them instantly.
- Show the invariant: "if the target exists, it is still inside the active range."
- Use one target value and three iterations.

Example visual state structure:

```python
values = [2, 5, 8, 12, 16, 23, 38]
boxes = VGroup(*[
    VGroup(Square(side_length=0.7), Text(str(v), font_size=24)).arrange(ORIGIN)
    for v in values
]).arrange(RIGHT, buff=0.12)

low_arrow = Arrow(DOWN, UP, color=BLUE).scale(0.45)
mid_arrow = Arrow(DOWN, UP, color=YELLOW).scale(0.45)
high_arrow = Arrow(DOWN, UP, color=GREEN).scale(0.45)
```

QA checks:

- The row remains sorted and readable.
- The pointer labels do not collide.
- The narration explains why the discarded half is safe to ignore.
- The final found/not-found state is explicit.

## Example: data explainer

Example intent: animate a small dataset showing how a moving average smooths noise.

Production plan:

- Show raw points first.
- Label axes with units and source.
- Animate a window bracket moving across the x-axis.
- Draw the moving-average line after the window demonstrates the rule.
- Keep a note: "Smoothing reveals trend but hides short-term variation."

QA checks:

- The data source and transformation are logged.
- The smoothing method and window size are stated.
- The animation does not imply prediction unless the script says so and the method supports it.
- Any real-world claim from the chart is source-reviewed.

## Sources and verification dates

Sources accessed July 11, 2026:

- Manim Community documentation, Quickstart: https://docs.manim.community/en/stable/tutorials/quickstart.html
- Manim Community documentation, building blocks and mobjects: https://docs.manim.community/en/stable/tutorials/building_blocks.html
- Manim Community documentation, Scene reference: https://docs.manim.community/en/stable/reference/manim.scene.scene.Scene.html
- Manim Community documentation, output settings: https://docs.manim.community/en/stable/tutorials/output_and_config.html
- Manim Community documentation, rendering text and formulas: https://docs.manim.community/en/stable/guides/using_text.html
- Manim Community documentation, Axes reference: https://docs.manim.community/en/stable/reference/manim.mobject.graphing.coordinate_systems.Axes.html
- Manim Community documentation, adding voiceovers: https://docs.manim.community/en/stable/guides/add_voiceovers.html
- Manim Community documentation, v0.19.0 changelog: https://docs.manim.community/en/stable/changelog/0.19.0-changelog.html
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- W3C Understanding WCAG 2.3.1 Three Flashes or Below Threshold: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- C2PA Technical Specification 2.4: https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html
- FFmpeg documentation: https://ffmpeg.org/ffmpeg.html
- FFmpeg codecs documentation: https://ffmpeg.org/ffmpeg-codecs.html

Volatile facts to re-check at production time:

- Current Manim Community version, CLI flags, renderer behavior, and plugin compatibility.
- Current LaTeX/Pango/font installation requirements for the operating system or container.
- Manim Voiceover supported services and API behavior.
- FFmpeg build features and codec availability, especially `libx264`/AAC support.
- Platform delivery rules for aspect ratio, codec, captions, duration, bitrate, file size, thumbnails, and provenance metadata.
- Accessibility or legal requirements that are specific to the client, jurisdiction, institution, or distribution platform.
