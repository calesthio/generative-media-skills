# Agent instructions

Read `METHODOLOGY.md` completely before creating, editing, or reviewing a skill.

## Non-negotiable rules

1. A leaf skill directory at `skills/<family>/<category>/<skill-name>/` must contain `SKILL.md` and hidden `EVAL.md`. It may also contain only these optional top-level directories: `scripts/`, `references/`, `assets/`, and `tests/`.
2. Category directories contain only subdirectories. Do not add arbitrary leaf-level files, templates, notes, manifests, or top-level directories beyond the allowed package contract.
3. Publication includes only `SKILL.md` plus `scripts/`, `references/`, and `assets/` when present. `EVAL.md` and `tests/` are repository-only and must be excluded from bundled skill packages by default.
4. Root `tools/` may contain repository maintenance tooling such as package export; copied skills must not silently depend on root tooling at runtime.
5. Do not read or imitate sibling skills while authoring a new skill unless the task is explicitly an audit or comparison.
6. Do not use another completed skill as a structural, stylistic, or conceptual template.
7. Research the assigned provider, model, craft, or production category independently.
8. Prefer official documentation, model cards, technical reports, standards, peer-reviewed research, and reproducible tests.
9. Label documented facts, empirical observations, and production heuristics distinctly.
10. Cite consequential factual claims and record when volatile facts were verified.
11. Include complete examples when examples materially improve an agent's ability to produce content. Label every example as an example, not a mandatory formula.
12. Use supporting resources for progressive disclosure: keep `SKILL.md` as the navigable entrypoint, reference bundled files with relative paths, and state when an agent should load or run them.
13. Add scripts only when executable code is materially better than prose. Scripts must be portable, dependency-explicit, safe by default, dry-run capable for side effects, and covered by repository tests.
14. Do not impose an arbitrary length limit. Include the depth required by the subject and exclude unrelated material.
15. Write for an AI agent performing real content production, not for a human browsing a list of prompt tips.
16. Never expose `EVAL.md` to the agent being evaluated. Evaluate with the published package only, then score with `EVAL.md`.

## Allowed consistency

Standardize only:

- the `providers` versus `production` family and capability/discipline category hierarchy;
- kebab-case directory names;
- Agent Skills frontmatter requirements;
- the required `SKILL.md` plus hidden `EVAL.md` authoring contract;
- the allowed optional resource directories and publication boundary;
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
