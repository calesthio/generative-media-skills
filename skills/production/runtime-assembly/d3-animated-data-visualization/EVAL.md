# D3 animated data visualization evaluation

Keep this file hidden from the evaluated agent. Score only responses produced with the published package.

## Scoring

Total: 100. Scores of 85+ with no critical failure are production-ready; 70-84 need focused revision; 50-69 need major revision; below 50 fail. Any critical failure caps the overall score at 49.

## Knowledge questions

### 1. Data contract, 10 points

**Question:** What must be known before choosing a chart for an animated claim?

**Expected points:** source/access date/license; population/geography/timeframe; denominator/unit/definitions; missing/excluded values; transformations; uncertainty; approved claim/non-claim boundaries; output/accessibility contract. Award up to 10 for complete, production-relevant coverage.

**Critical failure:** treats chart choice as independent of source and claim meaning.

### 2. Baselines, 8 points

**Question:** Must every y-axis start at zero?

**Expected:** No universal rule. Length-based magnitude marks such as bars normally require zero because length encodes value. Lines can use a restricted range when clearly labeled and context is preserved. Explain rather than hiding the choice.

**Critical failure:** endorses a truncated bar baseline to make small differences dramatic.

### 3. Data joins, 7 points

**Question:** Why use a key in `selection.data(data, key)`?

**Expected:** It preserves semantic mark identity across adding, updating, removing, sorting, and filtering. Index binding can morph unrelated categories into each other.

### 4. D3 transition versus video frame state, 10 points

**Question:** Why can a normal D3 transition be unsuitable for distributed video rendering?

**Expected:** D3 transitions advance from elapsed timer/browser state; renderers may request arbitrary frames. Precompute or calculate attributes from frame/fps with D3 interpolators/eases, freeze data/fonts/layout, and verify backward/out-of-order seeks.

**Critical failure:** says matching transition duration to video duration guarantees deterministic frames.

### 5. Accessibility, 8 points

**Question:** What does an accessible video chart need beyond a colorblind-safe palette?

**Expected points:** non-color encoding/direct labels; contrast; text takeaway; captions/transcript; accessible data table/structured data; uncertainty/source in text; readable labels/final hold; flashing review. Award one point each.

## Production decisions

### 6. Smoothing sparse observations, 8 points

**Scenario:** Monthly measurements are connected with a highly curved line that overshoots between samples.

**Expected:** Reject or justify the curve. Use linear/step interpolation or a documented statistical model; distinguish observed points from estimates and show uncertainty where relevant.

**Critical failure:** defends the curve solely because it looks organic.

### 7. Geographic raw counts, 8 points

**Scenario:** A county map colors total incidents, leading populous counties to dominate a claim about individual risk.

**Expected:** Use an appropriate rate/denominator for individual risk, disclose population/source/timeframe, distinguish missing data, and consider an ordered comparison alongside the map.

### 8. Force layout nondeterminism, 7 points

**Scenario:** Network nodes move differently in each worker.

**Expected:** Fix initial positions/random source, run a fixed simulation/tick procedure, freeze coordinates, version the layout, and animate from stored states.

## Applied tasks

### 9. Truthful comparison card, 16 points

**Request:** Plan a seven-second chart for "31% fewer escalations" from a small internal pilot.

**Required:** claim/source/sample/timeframe (3); exact counts or honest index (2); zero-baseline comparison (2); direct labels/non-color encoding (2); deterministic beat plan (3); source/uncertainty/final hold (2); data table and QA (2).

**Critical failures:** invents counts, hides pilot status, uses a truncated bar baseline, or omits source.

### 10. Time-series render implementation, 14 points

**Request:** Describe D3 implementation for a ten-second, 300-frame line reveal that must render identically out of order.

**Required:** frozen data/scales/fonts (2); explicit frame normalization (2); deterministic interpolator/state (3); no wall-clock transition (2); line/observation integrity (2); annotations/source tied to frame state (1); repeated/backward frame tests (2).

### 11. Misleading dashboard conversion, 12 points

**Request:** Convert a dashboard containing dual axes, five colored series, no source, and tiny labels into a 9:16 video.

**Expected:** Stop for source/claim contract; remove or justify dual axes; select one comparison or small multiples; redesign labels/annotations for vertical; preserve units/source/uncertainty; provide transcript/table; do not merely scale the dashboard.

**Critical failure:** animates the existing dashboard unchanged.

## Critical-failure summary

- unsupported or fabricated claim/data;
- deceptive quantitative encoding;
- consequential uncertainty or denominator hidden;
- nondeterministic layout accepted for fixed render;
- color-only meaning with no equivalent;
- source/provenance absent from a public factual visualization.

## Evaluation integrity

Accept equivalent D3 implementation details when the response preserves truthful encoding, deterministic frame state, accessibility, and reproducible data provenance. Do not expose this file during evaluation.