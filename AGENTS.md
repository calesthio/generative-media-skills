# Agent instructions

Read `METHODOLOGY.md` completely before creating, editing, or reviewing a skill.

## Non-negotiable rules

1. A skill directory contains exactly `SKILL.md` and `EVAL.md`. Category directories contain only subdirectories; the package rule applies to the leaf skill directory at `skills/<family>/<category>/<skill-name>/`.
2. Do not create references, scripts, assets, templates, notes, or sidecar manifests inside a skill directory.
3. Do not read or imitate sibling skills while authoring a new skill unless the task is explicitly an audit or comparison.
4. Do not use another completed skill as a structural, stylistic, or conceptual template.
5. Research the assigned provider, model, craft, or production category independently.
6. Prefer official documentation, model cards, technical reports, standards, peer-reviewed research, and reproducible tests.
7. Label documented facts, empirical observations, and production heuristics distinctly.
8. Cite consequential factual claims and record when volatile facts were verified.
9. Include complete examples when examples materially improve an agent's ability to produce content. Label every example as an example, not a mandatory formula.
10. Do not impose an arbitrary length limit. Include the depth required by the subject and exclude unrelated material.
11. Write for an AI agent performing real content production, not for a human browsing a list of prompt tips.
12. Never expose `EVAL.md` to the agent being evaluated. Evaluate with `SKILL.md` only, then score with `EVAL.md`.

## Allowed consistency

Standardize only:

- the `providers` versus `production` family and capability/discipline category hierarchy;
- kebab-case directory names;
- Agent Skills frontmatter requirements;
- the two-file package;
- evidence quality;
- evaluation integrity;
- Markdown correctness.

Do not standardize:

- heading order;
- prose voice;
- prompt structure;
- creative methodology;
- example format beyond clear labeling;
- conclusions that should instead follow from subject-specific research.
