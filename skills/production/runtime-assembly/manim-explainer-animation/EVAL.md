# Evaluation: manim-explainer-animation

Use this file to evaluate whether an agent correctly used the `manim-explainer-animation` skill. The evaluated agent should receive only the user task and `SKILL.md`, not this file.

Score for production usefulness, factual discipline, and whether the agent behaves like a Manim explainer producer rather than a generic code generator.

## Knowledge questions

### 1. When should an agent choose Manim instead of a compositor or video model?

Expected answer:

- Choose Manim for precise, programmable, reproducible explanatory motion involving math, science, graphs, diagrams, algorithms, formulas, coordinate systems, or symbolic transformations.
- Prefer other tools for live action, photorealism, rich character performance, cinematic brand motion, UI capture, or social-first motion graphics when precision/programmatic visual logic is not central.
- Hybridizing is acceptable: render Manim segments and finish in another compositor.

Required points:

- Mentions precision/reproducibility/programmatic animation.
- Mentions at least three appropriate content categories such as math, data, diagrams, algorithms, formulas, coordinate systems.
- Provides at least one case where Manim is not the right primary tool.
- Avoids claiming Manim is universally best for all explainers.

Critical failures:

- Recommends Manim solely because it is "AI video" or because it is visually cinematic.
- Ignores user delivery constraints and visual style.
- Claims Manim is a generic replacement for all compositing/video production.

### 2. What should be planned before writing Manim code?

Expected answer:

- A production brief with audience, learning objective, misconception/tension, claims needing approval, runtime/aspect/delivery, accessibility and brand constraints.
- A concept breakdown with objects, symbols, actions, cognitive load, and verification checks.
- A storyboard with timing, narration, visual state, animation, learning purpose, assets/data, and QA.

Required points:

- Starts from explanation/storyboard rather than code.
- Includes audience and learning objective.
- Includes symbol/object ledger or equivalent.
- Includes source/SME review for consequential claims.
- Includes QA and accessibility considerations.

Critical failures:

- Jumps directly to code without script or storyboard for a non-trivial explainer.
- Treats equations/data/medical/scientific claims as style decisions only.

### 3. What is the difference between scene coordinates and graph coordinates in Manim?

Expected answer:

- Scene coordinates are screen/frame coordinates; mathematical graph coordinates should be converted through the axis/plane object.
- Use methods such as `axes.c2p()`/`coords_to_point()` and graphing helpers so points, lines, labels, and dots align with conceptual axes.

Required points:

- Explains that `(2, 2, 0)` in the scene is not always the same as `(2, 2)` on custom axes.
- Recommends axis conversion helpers.
- Identifies misplaced graph objects as a common QA issue.

Critical failures:

- Places data points with raw scene coordinates on custom axes without conversion.
- Does not label axes or units in a data/math explainer.

### 4. How should formulas and symbols be handled?

Expected answer:

- Use `Text` for plain language and `Tex`/`MathTex` for formulas.
- Isolate formula substrings or split formula arguments when highlighting or transforming symbols.
- Maintain a symbol/color ledger and keep meanings consistent.
- Narrate formula meaning; do not rely on visual math alone.
- Test LaTeX and required packages/templates.

Required points:

- Mentions `MathTex`/`Tex`.
- Mentions substring isolation or split formula parts.
- Mentions consistent color/meaning.
- Mentions LaTeX/package/font testing.

Critical failures:

- Uses inconsistent symbol colors without explanation.
- Displays dense formulas without narration or stepwise derivation.
- Ignores missing LaTeX/package risk.

### 5. What accessibility checks are required for a narrated Manim video?

Expected answer:

- Provide captions for prerecorded narrated synchronized media unless it is a clearly labeled media alternative for text.
- Include meaningful non-speech audio cues when relevant.
- Consider transcripts, especially for education/compliance/no-audio use.
- Avoid flashing more than three times per second unless under applicable thresholds; avoid rapid full-screen or red flashes.
- Check contrast, color-independent meaning, mobile readability, and motion comfort.

Required points:

- Mentions captions for prerecorded audio.
- Mentions flashing risk.
- Mentions color independence or contrast.
- Mentions transcript or visual description when visual content carries meaning.

Critical failures:

- Treats captions as optional for all narrated videos.
- Uses rapid flashing/pulsing as a default attention device.
- Encodes important states only by color.

### 6. How should provenance and asset custody be handled?

Expected answer:

- Maintain an asset ledger: source/path, owner/creator if known, license/permission, date accessed, transformations, final use, privacy/consent/data risks.
- Record generated assets, models/tools, prompts/settings when relevant, and dates.
- Treat C2PA/Content Credentials as provenance/tamper-evident metadata, not proof of factual truth.
- Re-check C2PA/platform support and verify after final post-processing when required.
- Escalate for copyrighted, proprietary, personal, regulated, or permission-unclear assets.

Required points:

- Mentions a ledger with source and rights/license/permission.
- Mentions generated media metadata.
- Correctly frames C2PA as provenance rather than truth.
- Includes escalation triggers.

Critical failures:

- Claims C2PA proves content is true.
- Uses copyrighted/proprietary/data-sensitive assets without permission review.
- Drops provenance after FFmpeg/post-processing.

### 7. What should be included in a reproducible handoff?

Expected answer:

- Source code, render command, dependency file or lockfile, Manim version, OS/container details if relevant, source assets/data, captions/transcript, final rendered output, thumbnails, asset/provenance ledger, review notes, known limitations, and re-render instructions.

Required points:

- Includes source code and exact render command.
- Includes dependencies and Manim version.
- Includes assets/data and captions.
- Includes final output and review/provenance notes.

Critical failures:

- Delivers only an MP4 for a code-reproducibility brief.
- Omits dependency/version information.

## Production-decision questions

### 8. Scenario: A user asks for a 90-second explanation of neural network backpropagation with exact matrix shapes and formulas, but also wants it to look like a cinematic product trailer. What should the agent recommend?

Expected decision:

- Recommend Manim for the precise formula/matrix/algorithm portions.
- Consider hybrid finishing in a compositor for cinematic title cards, music, brand packaging, or transitions.
- Explain tradeoffs: Manim ensures exact symbolic continuity; compositor improves cinematic polish.
- Plan SME review for technical correctness.

Strong answer must demonstrate:

- Runtime/tool choice follows the educational need, not just style.
- Symbols/matrix shapes need a ledger.
- Storyboard should manage cognitive load.
- Final delivery can combine Manim renders with post-production.

Penalize:

- Choosing a video model alone for exact formulas without verification.
- Choosing Manim alone while ignoring the cinematic style request.

### 9. Scenario: A client wants a 30-second vertical social video explaining a public-health statistic from a spreadsheet. What should the agent do before animating?

Expected decision:

- Verify/record data source, date, transformations, units, and whether public-health claims need SME/client approval.
- Plan a vertical-safe chart with labels, captions, and no tiny formulas.
- Decide whether Manim is appropriate for the chart/animation or whether a simpler data-viz/compositor workflow is better.
- Add accessibility checks and platform delivery re-checks.

Strong answer must demonstrate:

- Data provenance and claim escalation.
- Mobile/vertical layout considerations.
- Caption and contrast requirements.

Penalize:

- Animating the spreadsheet directly with no source or methodology note.
- Cropping a horizontal chart into vertical without redesign.

### 10. Scenario: A rendered scene shows a dot visibly off the curve while explaining tangent slope. How should the agent debug?

Expected decision:

- Isolate the scene and render a quick preview.
- Check whether the dot uses raw scene coordinates instead of `axes.c2p()`/axis conversion.
- Confirm the dot and curve use the same function, axis range, and coordinate system.
- Patch minimal code and rerender the scene before full render.

Strong answer must demonstrate:

- Render-in-the-loop repair.
- Understanding of coordinate conversion.
- Avoids guessing at style-only fixes.

Penalize:

- Moving the dot by eye with magic coordinates.
- Re-rendering the whole video repeatedly without isolating the failing scene.

### 11. Scenario: The final narration is generated by a TTS provider and the user asks for "full source transparency." What should the handoff include?

Expected decision:

- Include final script, timed captions, TTS provider/model/voice/settings, generated audio file paths, generation date, terms/rights notes, and replacement instructions.
- Record that API outputs may not be exactly reproducible unless provider guarantees seed/settings reproducibility.
- Include provenance notes for any AI-generated or third-party assets.

Strong answer must demonstrate:

- Asset custody for generated media.
- Distinguishes reproducible code from potentially non-deterministic API outputs.

Penalize:

- Treating generated voice as a black box.
- Omitting provider/voice metadata.

## Applied production tasks

### 12. Task: Produce a storyboard for "Why binary search is O(log n)" for beginners.

Successful output characteristics:

- Defines audience and learning objective.
- Uses a sorted array, target, low/mid/high pointers, discarded halves, and an invariant.
- Shows halving over multiple iterations and connects it to logarithmic growth.
- Uses consistent colors/labels for pointers and active/discarded ranges.
- Includes narration beats, timing, visual state, animation, learning purpose, and QA.
- Includes accessibility notes for captions, contrast, and color-independent states.

Scoring rubric:

- 3 points: clear pedagogical progression from search problem to repeated halving to O(log n).
- 2 points: Manim-suitable visual architecture with objects, pointers, and transformations.
- 2 points: symbol/color/state ledger and cognitive-load management.
- 2 points: timing/narration alignment.
- 1 point: QA/accessibility/provenance notes.

Critical failures:

- Merely lists pseudocode without visual pedagogy.
- Does not explain why halving implies logarithmic steps.
- Uses color only to mark discarded ranges.

### 13. Task: Write a Manim scene architecture plan for a 2-minute explainer about Fourier series.

Successful output characteristics:

- Splits into scene classes or chapters: intuition, rotating vectors, waveform build-up, formula, applications/recap.
- Defines reusable helpers for axes, rotating vectors/phasors, waveform plot, formula labels, and color palette.
- Includes symbol ledger for frequency, amplitude, phase, time, and partial sum.
- Describes coordinate systems and how graph points/phasors are converted.
- Plans narration timing and pauses for complex transformations.
- Includes render settings, dependency notes, and QA.

Scoring rubric:

- 3 points: appropriate decomposition into scenes and helper functions.
- 2 points: correct handling of graphs/coordinate systems.
- 2 points: formula/symbol continuity.
- 1 point: voiceover/caption timing.
- 1 point: accessibility and motion comfort.
- 1 point: reproducibility handoff.

Critical failures:

- Attempts one dense scene with all formulas and no staged reveal.
- Does not distinguish circular motion from waveform graph coordinates.
- No plan for correctness review of formulas.

### 14. Task: Review a proposed Manim delivery plan that says, "We'll render 1080p, add a flashing red warning around the key theorem, skip captions because the visuals are self-explanatory, and use a textbook diagram found online."

Expected critique:

- Flashing red warning is risky; avoid rapid flashes and use slower emphasis such as outline, arrow, circumscribe, or label.
- Captions are needed for prerecorded narrated synchronized media unless it is clearly a media alternative for text; transcripts may also be appropriate.
- The textbook diagram needs rights/license/source review and likely permission; consider redrawing from first principles if allowed.
- 1080p alone is not a full delivery plan; include aspect ratio, frame rate, codec, platform specs, safe areas, captions format, and QA.
- Include provenance ledger and escalation triggers.

Scoring rubric:

- 3 points: catches flashing/accessibility issue.
- 2 points: catches caption issue.
- 2 points: catches copyright/provenance issue.
- 2 points: improves delivery/render spec.
- 1 point: provides safe alternatives.

Critical failures:

- Approves the plan as-is.
- Gives legal advice instead of escalation for rights uncertainty.

### 15. Task: Provide a repair plan for a Manim formula animation where `set_color_by_tex("x")` colors too much or too little.

Successful output characteristics:

- Explains that formula parts should be isolated or split into separate arguments.
- Suggests `substrings_to_isolate`, double-brace grouping, or separate string arguments depending on the formula.
- Renders a minimal test scene before patching the full video.
- Maintains symbol color ledger and checks transforms still match.

Scoring rubric:

- 4 points: correct technical repair options.
- 2 points: minimal render-in-the-loop workflow.
- 2 points: preserves pedagogical/symbol consistency.
- 1 point: mentions LaTeX escaping/package issues if relevant.
- 1 point: final QA check.

Critical failures:

- Suggests manually overlaying a colored text object without checking alignment or transform continuity as the only solution.
- Does not test the formula in isolation.

## Overall scoring guidance

An excellent response:

- Starts from educational intent and storyboard before code.
- Chooses Manim only when it is technically and pedagogically justified.
- Shows command of Manim scene/mobject/formula/axis concepts without becoming only a syntax tutorial.
- Plans voiceover/captions/timing as part of production, not afterthoughts.
- Includes QA, accessibility, provenance, and reproducibility.
- Identifies volatile facts and instructs re-checking current package/platform/provider behavior.
- Escalates consequential claims, rights questions, regulated content, and formal accessibility/legal requirements.

A weak response:

- Generates isolated Manim snippets with no storyboard, QA, or handoff.
- Uses magic coordinates and inconsistent symbols.
- Ignores captions, flashing risk, color accessibility, provenance, or source rights.
- Treats render success as the only quality bar.
- Makes unsupported claims about current versions, platform rules, or legal compliance.
