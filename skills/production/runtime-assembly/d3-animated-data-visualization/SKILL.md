---
name: d3-animated-data-visualization
description: Production guidance for converting sourced data and approved claims into truthful, accessible, deterministic animated visualizations with D3. Use for data-driven charts, maps, networks, hierarchies, transitions, annotations, responsive video variants, frame-by-frame browser rendering, and visualization QA; not for generic dashboards, unsourced decorative charts, or ordinary motion graphics without a data contract.
---

# D3 animated data visualization

Use this skill when data determines the marks, scales, layout, labels, and animation of a rendered-media sequence. D3 is useful when standard chart components cannot express the required encoding or choreography with sufficient control.

The job is not to make numbers move. The job is to preserve meaning while controlling attention over time. Source integrity, denominator, units, uncertainty, scale, and transformations are production inputs, not footer decoration.

## Evidence stance

- **Documented fact:** behavior or requirement from official D3, W3C, or cited standards documentation.
- **Production heuristic:** a practical choice that depends on the dataset, audience, and delivery.
- **Empirical observation:** a measured result from the actual data, layout, rendered frames, or encoded output.

D3 packages and APIs are versioned independently. Facts were checked **2026-07-12**. Record exact module versions and re-check official documentation when the installed set differs.

## When to use D3

Use D3 for:

- custom visual encodings built from scales, shapes, axes, and SVG or Canvas marks;
- timelines, distributions, hierarchies, geographic projections, flows, and networks;
- data joins where stable identities must persist between states;
- precise annotations and source notes tied to data;
- deterministic frame evaluation inside browser-rendered video;
- responsive chart variants that require recalculated scales and layout.

Prefer a standard chart component when it already supports the truthful chart, labeling, accessibility, and export needs. Prefer a motion compositor when data is already reduced to a few approved values and no data-driven layout remains. Do not use D3 to lend false authority to illustrative or invented numbers.

## Establish the data and claim contract

Before selecting a chart, record:

- question and intended takeaway;
- source organization, dataset/table, URL or identifier, access date, license, and owner;
- population, geography, timeframe, sample, denominator, unit, currency basis, and definitions;
- missing values, exclusions, revisions, censoring, and known collection changes;
- transformations: aggregation, normalization, indexing, inflation adjustment, smoothing, rolling windows, interpolation, projection, or model output;
- uncertainty, confidence interval, margin of error, scenario range, or estimate status;
- approved claim and claims the visualization must not imply;
- aspect ratios, duration, fps, caption/source-note area, and accessible alternative;
- data checksum and visualization configuration version.

If these fields cannot be resolved, label the output as exploratory or block publication. Do not silently repair missing data, infer denominators, or choose a favorable date range.

## Select an encoding that answers the question

Choose the chart from the comparison task:

| Question | Typical starting point | Main integrity risk |
|---|---|---|
| Compare categories | ordered bars or dot plot | truncated length baseline, unstable ordering |
| Show change over time | line, step, area, or small multiples | smoothing implies observations, missing intervals hidden |
| Show distribution | histogram, strip/dot, box, density | bin/bandwidth manipulation, hidden sample size |
| Show relationship | scatterplot with annotation | correlation implied as causation, overplotting |
| Part-to-whole | stacked bars or carefully labeled areas | totals not equal, small segments unreadable |
| Geography | projected map plus normalized measure | raw counts mistaken for rates, projection distortion |
| Hierarchy | tree, treemap, partition | area/angle hard to compare, hierarchy ambiguity |
| Network/flow | node-link, Sankey, chord | layout mistaken for geography or importance |

Production heuristics:

- Prefer position on a common scale, then length, before relying on area, angle, or hue for precise comparison.
- Bar charts that encode magnitude by length should normally begin at zero. A line chart may use a restricted range when it is clearly labeled and context is preserved.
- Avoid dual axes unless the relationship and independent scales are essential, conspicuous, and resistant to false correlation.
- Avoid 3D perspective on quantitative marks when it distorts position, length, area, or occlusion.
- Use small multiples when simultaneous series become unreadable.
- Sort categories when rank is the message; preserve semantic or chronological order when sorting would mislead.

Do not smooth a line merely because it looks polished. Curves can overshoot or imply unmeasured intermediate behavior. Use linear or step interpolation when that better represents the observations; explain any smoothing method.

## Build scales, axes, and marks

**Documented fact:** D3 scales map a domain to a range. D3 provides continuous, sequential, diverging, quantize, threshold, ordinal, band, point, time, and other scale families. Axes render human-readable ticks from scales. Shape generators convert data into path geometry.

Implementation contract:

- derive the domain from the approved data and policy, not from the desired visual drama;
- include zero for length-based magnitude marks unless a documented exception is justified;
- handle invalid, missing, zero, and negative values explicitly;
- use log scales only for positive domains and label them clearly; use symlog or another defensible approach when signed values matter;
- choose tick formats that preserve units and significant meaning;
- keep axis, unit, source, and uncertainty visible during the final hold;
- use stable IDs for data marks and annotations.

Example scale setup:

```js
const x = d3.scaleBand()
  .domain(data.map((row) => row.category))
  .range([plotLeft, plotRight])
  .padding(0.22);

const y = d3.scaleLinear()
  .domain([0, d3.max(data, (row) => row.value)])
  .nice()
  .range([plotBottom, plotTop]);
```

This is an example for positive bar magnitudes, not a universal scale recipe.

## Preserve identity with data joins

**Documented fact:** `selection.data(data, key)` binds data to selected elements. `selection.join()` can handle entering, updating, and exiting elements. Without a key, matching is by index.

Use a stable semantic key so a mark represents the same entity across states:

```js
const marks = plot.selectAll("rect.bar")
  .data(rows, (row) => row.id)
  .join(
    (enter) => enter.append("rect").attr("class", "bar"),
    (update) => update,
    (exit) => exit.remove(),
  );
```

Index keys can make bars appear to transform into unrelated categories after sorting or filtering. Test additions, removals, ties, and reordered categories.

## Design animation as explanation

Each animation beat should answer one of these:

- What is the frame of reference?
- What data arrives or changes?
- Which comparison matters?
- What uncertainty or caveat qualifies it?
- What final state should the viewer remember?

Recommended reveal order:

1. title/question and unit;
2. axes or comparison frame;
3. marks;
4. highlighted relationship;
5. annotation and source/caveat;
6. stable final hold.

Avoid animated counts that imply measurement precision the source does not support. Do not overshoot quantitative marks with spring/elastic easing: a bar temporarily exceeding its value visually states a false quantity. Easing may control reveal progress, but the held mark must encode the exact value and misleading intermediate states should be avoided.

## Deterministic rendering

**Documented fact:** D3 transitions are scheduled over elapsed time using D3's timer system. They suit interactive browser animation, but a video renderer may request frames out of order or without real-time playback.

For fixed media, calculate visual state directly from the requested frame:

```js
function renderFrame(frame, fps) {
  const raw = clamp01((frame - startFrame) / durationFrames);
  const progress = d3.easeCubicInOut(raw);

  bars
    .attr("y", (row) => d3.interpolateNumber(y(0), y(row.value))(progress))
    .attr("height", (row) => d3.interpolateNumber(0, y(0) - y(row.value))(progress));
}
```

Better still, prebuild interpolators when data is frozen. Use explicit start/end state for entering, updating, and exiting marks. Derive annotations, axis transitions, labels, and source notes from the same frame state.

Requirements:

- no live fetch during capture;
- no wall-clock time or event-dependent transition state;
- seeded or precomputed random layouts;
- stable font files and text measurement;
- backward and out-of-order frame correctness;
- repeated stress-frame comparison.

For a force layout, run a fixed number of ticks with fixed initial positions and random source, store the resulting coordinates, then animate from those frozen coordinates. Do not run an unconstrained live force simulation independently in every render worker.

## Maps, networks, and hierarchies

### Geographic maps

- state whether the metric is count, rate, share, change, or index;
- normalize by population/exposure when the claim requires it;
- choose and disclose a projection appropriate to the spatial question;
- distinguish no data from zero;
- preserve geographic source/version and joins between geometry and data;
- include non-map comparison when area or projection makes values hard to compare.

### Networks and flows

- define what a node, edge, direction, width, and distance mean;
- disclose filtered edges and layout rules;
- do not imply that force-layout proximity is a measured distance unless it is;
- freeze layout before deterministic capture;
- show flow conservation or explain leakage/aggregation where applicable.

### Hierarchies

- validate parent-child structure and totals;
- avoid double counting descendants and parents;
- state whether area, angle, depth, or order encodes value;
- provide labels or a table for small nodes that cannot be read.

## Responsive variants

Design each output from the same data/claim contract but recompute layout for its canvas.

- Change margins, tick density, label placement, annotation order, and chart form when needed.
- Use small multiples or a ranked subset for vertical video rather than shrinking a dense desktop chart.
- Preserve units, source, uncertainty, and comparison context in every cutdown.
- Test typography at intended physical playback size.
- Do not use viewport-width font scaling as a substitute for layout decisions in fixed video.

## Accessibility

**Documented facts from WCAG 2.2:** color cannot be the only visual means of conveying information; normal text generally needs at least 4.5:1 contrast and large text at least 3:1; meaningful graphical objects and states generally need at least 3:1 non-text contrast against adjacent colors.

For every visualization:

- pair color with direct labels, position, shape, texture, line style, or symbols;
- use palettes whose ordering and contrast fit the data type;
- write a concise text takeaway and provide the underlying accessible table or structured data when the delivery surface permits;
- include uncertainty and source information in text, not color alone;
- caption narration and meaningful audio;
- keep animation from making labels unreadable;
- check flashing if marks, backgrounds, or highlights pulse.

For interactive publication, provide keyboard and screen-reader semantics appropriate to the host and a non-visual equivalent. For prerecorded video, narration, captions, transcript, and an accessible data table are the practical alternatives. Sonification can supplement, but does not automatically replace, a structured data alternative.

## Performance and output quality

Use SVG when inspectable vector marks and text are valuable and DOM size is manageable. Consider Canvas for very dense marks, but plan accessible equivalents and crisp text separately. Reduce data only with a documented method that preserves the claimed pattern.

Measure:

- DOM/mark count and layout time;
- frame render time at delivery resolution;
- font and label measurement stability;
- memory during long renders;
- path complexity and overdraw;
- encoded legibility of thin lines, small labels, grids, and color gradients.

Do not set universal point-count thresholds. The chart type, browser, renderer, hardware, and effects determine the actual limit.

## Provenance and QA

Keep a visualization manifest containing:

- input file names and checksums;
- source, access date, license, and retrieval method;
- transformations and code/config version;
- D3 package versions;
- chart type, domains, ranges, bins, projection, layout seed/ticks, color scheme, and easing;
- output dimensions, fps, duration, and render environment;
- approved claim, caveats, and reviewer.

QA passes:

1. **Data:** reproduce totals, samples, transformations, missing values, and uncertainty.
2. **Encoding:** verify scale, baseline, units, area/length/position, sorting, projection, and legend.
3. **Animation:** inspect entering/updating/exiting identity, truthful intermediates, labels, annotations, and final hold.
4. **Determinism:** compare repeated frames, reorders, and backward seeks.
5. **Accessibility:** color alternatives, contrast, captions, text takeaway, and data table.
6. **Delivery:** crop variants, source-note legibility, frame count, compression, and metadata.

Critical failures include an unsupported claim, omitted source or denominator, deceptive scale, incorrect totals, uncertainty hidden where consequential, color-only meaning, nondeterministic layout, or source notes unreadable in the delivered version.

## Example 1: pilot outcome comparison

This is a complete example, not a mandatory formula.

**Intent:** create a seven-second 9:16 evidence card for an approved statement: "Pilot teams recorded 31% fewer manual escalations."

**Data contract:** internal pilot; eight teams; measurement period April-June 2026; comparison is the same teams' January-March 2026 workflow; data accessed 2026-07-05; value is a relative reduction; source is not a randomized study; exact counts and approved disclosure are supplied.

**Design:** two horizontal bars with a zero baseline: `Prior workflow` and `Pilot period`. Direct labels include counts; a separate `31% fewer` annotation states the relative comparison. Source and sample note remain visible during the final two seconds. Color is reinforced by labels and different hatch/solid treatments.

**Animation:**

```text
00:00.00-00:00.60  Question, axis, unit, and baseline appear.
00:00.60-00:01.50  Prior bar grows linearly to its exact count.
00:01.20-00:02.10  Pilot bar grows to its exact count.
00:02.20-00:03.00  Difference bracket and "31% fewer" annotation appear.
00:03.00-00:05.00  Hold comparison.
00:05.00-00:07.00  Hold comparison plus source/sample disclosure.
```

Evaluate every mark from frame-derived progress; do not use elastic overshoot. Export the underlying two-row table with the delivery.

**Expected result:** exact values, fair length comparison, clear denominator/timeframe, readable source, and identical frames across clean renders.

**Likely failures:** animating 31% from zero without showing the compared counts; omitting that this is an internal pilot; truncating the bar baseline; source visible too briefly; color-only distinction.

**Variation:** if exact counts cannot be published, use a clearly labeled indexed comparison (`prior workflow = 100`) and explain the transformation instead of fabricating bar values.

## Example 2: regional drought anomaly map

This is a complete example, not a mandatory formula.

**Intent:** make a 20-second documentary insert showing standardized precipitation anomaly across watersheds and then comparing the five most affected basins.

**Data contract:** named meteorological dataset/version; watershed geometry source/version; monthly anomaly relative to a stated 30-year baseline; missing stations and interpolation method documented; values are anomaly scores, not raw rainfall.

**Workflow:**

1. Validate geometry/data join keys and classify missing watersheds separately from zero anomaly.
2. Choose an equal-area projection appropriate to the region and disclose it in production notes.
3. Use a diverging scale centered at zero with direct legend labels and textured boundary around severe categories.
4. Reveal the map by month using explicit frame interpolation between frozen monthly values.
5. At the selected month, annotate the five basins, then transition to an ordered dot plot for precise comparison.
6. Keep baseline definition, source, and interpolation caveat in the final hold and transcript.

**Expected result:** viewers see the spatial pattern, then receive a precise ranked comparison without mistaking map area for anomaly magnitude.

**Likely failures:** raw station count drives color; no-data regions look like normal; projection is unstated; interpolation is presented as direct observation; live force/collision labels differ between workers; map-only delivery lacks an accessible table.

**Variation:** for a short social cut, omit monthly animation and use one approved month plus the ordered dot plot; preserve the baseline and caveat.

## Sources

Official and authoritative sources checked 2026-07-12:

- D3 documentation: https://d3js.org/
- D3 selection joining: https://d3js.org/d3-selection/joining
- D3 scales: https://d3js.org/d3-scale
- D3 axes: https://d3js.org/d3-axis
- D3 shapes: https://d3js.org/d3-shape
- D3 interpolation and easing: https://d3js.org/d3-interpolate and https://d3js.org/d3-ease
- D3 timers and transitions: https://d3js.org/d3-timer and https://d3js.org/d3-transition
- D3 geographic projections: https://d3js.org/d3-geo
- D3 force simulation: https://d3js.org/d3-force/simulation
- D3 license (ISC): https://github.com/d3/d3/blob/main/LICENSE
- W3C WCAG 2.2, Use of Color: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- W3C WCAG 2.2, Contrast Minimum: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C WCAG 2.2, Non-text Contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- Royal Statistical Society, Best Practices for Data Visualisation: https://royal-statistical-society.github.io/datavisguide/