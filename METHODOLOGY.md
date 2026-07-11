# Research and authoring methodology

## Purpose

This repository equips AI agents to perform real media-production work. Skills should improve provider selection, creative direction, prompt construction, iteration, troubleshooting, and quality review for a specific subject.

The repository shares a file contract and evidence standard. It does not share a universal content template.

## Skill boundaries

A skill should cover one coherent subject, such as:

- a provider or model family;
- a production discipline such as cinematography or sound design;
- a deliverable category such as a product advertisement;
- a finishing or quality-assurance task.

Split skills when capabilities require substantially different research, production reasoning, or evaluation. Do not split a coherent subject merely to keep files short.

## Required package

```text
skills/<family>/<category>/<skill-name>/
├── SKILL.md
└── EVAL.md
```

Use `providers` as the family for vendor, model-family, API, gateway, or hosted/open-weight runtime skills. Use `production` for provider-independent craft, direction, deliverable, finishing, and quality-assurance skills. Choose a capability-specific category such as `image-generation`, `video-generation`, `text-to-speech`, `creative-direction`, or `content-formats`. Create a new category only when an accepted skill requires it; do not add empty category directories.

`SKILL.md` must use valid Agent Skills frontmatter with a kebab-case `name` matching its directory and a specific `description` explaining what the skill does and when an agent should use it.

No other files belong inside a skill directory.

## Independent authoring

Parallel authors must begin from an isolated research assignment. They must not receive a completed sibling skill as an example and must not inspect sibling skill directories during authoring.

Each assignment should provide only:

- the skill name;
- the intended scope;
- the two-file contract;
- the evidence policy;
- the evaluation-integrity rules.

The author determines the organization, production vocabulary, examples, and conclusions from research into the assigned subject.

## Evidence policy

Use sources in this order of preference:

1. Official provider documentation, API references, model cards, SDKs, changelogs, policies, and first-party examples.
2. Peer-reviewed papers, official technical reports, professional standards, and authoritative production manuals.
3. Reproducible first-party experiments performed for the skill.
4. Independent benchmarks or practitioner reports with a disclosed method.
5. Community observations, clearly labeled and never used as the sole basis for consequential technical claims.

For volatile facts such as model identifiers, supported inputs, duration limits, pricing, regional availability, or API behavior, record the verification date next to the claim or in a source section.

Do not present provider marketing language as an independently established fact. Do not state that a model is "best" or a universal default without dated, relevant evidence and explicit evaluation criteria.

## Writing SKILL.md

`SKILL.md` should contain whatever an agent needs to succeed at the subject. Its structure must follow the subject rather than a repository-wide outline.

Depending on the skill, useful material can include:

- activation and non-activation boundaries;
- capability and limitation analysis;
- production decision frameworks;
- provider- or category-specific terminology;
- input and reference strategy;
- prompt construction;
- camera, motion, lighting, performance, audio, layout, or editing guidance;
- parameter and model selection;
- iteration and repair workflows;
- common failure modes;
- output-review criteria;
- safety, consent, privacy, and rights considerations;
- complete examples;
- cited sources and verification dates.

This list is not a mandatory heading structure.

### Complete examples

Examples must be labeled as examples rather than required formulas. When relevant, a complete example should include:

- the production intent;
- the applicable provider, model, or category;
- inputs and constraints;
- the complete prompt, direction, or workflow;
- parameters;
- why the example is structured that way;
- expected results;
- likely failure modes;
- meaningful variations.

Examples should cover distinct production problems, not merely substitute different subjects into the same prompt.

## Writing EVAL.md

`EVAL.md` is an answer key and scoring specification. It should be independently tailored to the risk surface and production demands of the skill.

Use the relevant combination of:

### Knowledge questions

Test factual understanding, capability boundaries, terminology, limitations, and supported workflows.

Each question should include:

- the question;
- the expected answer;
- required points;
- incorrect or disqualifying claims where useful.

### Production-decision questions

Test whether the agent can choose an appropriate approach and explain tradeoffs under realistic constraints.

Each question should include:

- the production scenario;
- the expected decision;
- the reasoning that a strong answer must demonstrate;
- unsafe, unsupported, or low-quality decisions to penalize.

### Applied production tasks

Test whether the agent can produce a useful prompt, plan, direction, edit decision, review, or troubleshooting response.

Each task should include:

- the user request;
- the expected approach;
- essential characteristics of a successful output;
- a scoring rubric;
- critical failures.

There is no fixed number of questions. Coverage should reflect the subject's complexity.

## Evaluation integrity

The evaluated agent receives the user task and `SKILL.md`, but not `EVAL.md`.

The evaluator then uses `EVAL.md` to score the captured response. For isolated forward tests, install or copy only `SKILL.md` into the test environment.

Do not link to `EVAL.md` from `SKILL.md` or instruct a production agent to read it.

## Review process

Use separate authors and reviewers whenever practical.

Reviewers assess:

- source quality and factual support;
- subject specificity;
- production usefulness;
- completeness and accuracy of examples;
- separation of fact, observation, and heuristic;
- evaluation coverage;
- unsupported assumptions or rankings;
- overlap with the declared scope of other skills;
- safety and rights risks.

Reviewers must not rewrite independent skills into a shared voice or heading structure.

## Definition of done

A skill is ready for review when:

- its directory contains only `SKILL.md` and `EVAL.md`;
- its scope is coherent and distinct;
- its consequential claims are supported;
- volatile facts are dated;
- complete examples are included where useful;
- its evaluation measures applied production competence;
- an evaluated agent can be tested without seeing the answer key;
- the skill reflects its own subject rather than the flavor of another skill.
