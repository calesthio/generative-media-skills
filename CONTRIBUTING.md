# Contributing

Contributions should make AI agents materially better at a specific media-production task.

## Before authoring

1. Read `METHODOLOGY.md`.
2. Define a narrow, coherent skill scope.
3. Check that the proposed skill is not merely a rename of an existing scope.
4. Work in an isolated branch or worktree.
5. Do not inspect completed sibling skills for a structure or writing style to copy.

## Authoring

Create the required authoring files:

```text
skills/<family>/<category>/<skill-name>/SKILL.md
skills/<family>/<category>/<skill-name>/EVAL.md
```

Leaf skills may also include only these optional top-level directories:

- `scripts/` for publishable executable helpers;
- `references/` for publishable on-demand documentation;
- `assets/` for publishable static resources;
- `tests/` for repository-only tests.

Use `providers` for provider/model/runtime skills and `production` for provider-independent media-production practice. Select the narrowest capability or discipline category already present; add a new category only with its first accepted skill. Use a lowercase kebab-case skill directory name. The `name` in `SKILL.md` frontmatter must match the leaf directory.

Research the subject independently and cite consequential claims. Include complete, labeled examples when they improve production performance. Build evaluations from the subject's actual capabilities, decisions, and failure modes.

Keep `SKILL.md` as the entrypoint and use optional resources for progressive disclosure. Reference bundled files with relative paths and state when an agent should open a reference, use an asset, or run a script. Do not add arbitrary leaf-level files, sidecar manifests, notes, templates, or extra top-level directories.

Add scripts only when executable code is materially warranted. Scripts must be portable outside this repository, dependency-explicit, safe by default, dry-run capable for side effects, and covered by repository tests. Do not require root `tools/` as an unstated runtime dependency of a copied skill.

The publication boundary is `SKILL.md` plus `scripts/`, `references/`, and `assets/` when present. `EVAL.md` and `tests/` are repository-only and excluded from default bundles. Root `tools/` may hold repository maintenance tooling such as package export.

## Updating catalog references

Skill directories are the source of truth. Two catalog files must stay in sync with them and are updated as a separate integration step, not by the skill author during isolated authoring (this keeps parallel authors from editing shared files and from seeing sibling scopes).

When a skill is added to an existing category:

1. `SKILL_INDEX.md` - add the skill under its category list (keep the list alphabetical) and update the total package count in the intro line.
2. `README.md` - increment the category's skill count in the "At a glance" table.

When a skill introduces a new category, additionally:

3. `SKILL_INDEX.md` - add the category heading in alphabetical order within its family (`Providers` or `Production`).
4. `README.md` - add a row for the category in the "At a glance" table.
5. `README.md` - add the category directory to the "Repository structure" tree.
6. `README.md` - update the skill and category counts (and category examples, if listed) in the introduction.

Apply the same reference updates in reverse when a skill or category is renamed or removed. No other files require per-skill updates: `AGENTS.md`, `METHODOLOGY.md`, and the delegating entrypoints (`CLAUDE.md`, `GEMINI.md`, editor rule files) are catalog-independent.

## Review checklist

- [ ] The directory contains required `SKILL.md` and hidden `EVAL.md`, plus only allowed optional directories when needed.
- [ ] The skill was independently researched.
- [ ] The skill does not imitate a sibling skill's flavor or conclusions.
- [ ] The frontmatter name and directory match.
- [ ] The description clearly states what triggers the skill.
- [ ] Documented facts, observations, and heuristics are distinguishable.
- [ ] Consequential claims have authoritative sources.
- [ ] Volatile facts have verification dates.
- [ ] Examples are complete and labeled as examples.
- [ ] Optional resources are progressively disclosed from `SKILL.md` and referenced with relative paths.
- [ ] Scripts are warranted, portable, dependency-explicit, safe by default, and dry-run capable for side effects.
- [ ] Repository tests cover bundled scripts/resources, including failure and safety cases.
- [ ] `EVAL.md` includes expected answers or scoring criteria.
- [ ] Applied tasks test real production ability.
- [ ] Evaluation can run against the published package without exposing `EVAL.md` or `tests/` to the tested agent.
- [ ] Safety, consent, privacy, and rights issues are addressed where relevant.
- [ ] `SKILL_INDEX.md` lists the skill and its total package count is correct.
- [ ] `README.md` category table - and, for a new category, the repository-structure tree and introduction counts - reflect the change.

## Licensing

The project is licensed under MIT (see `LICENSE`). Do not copy or vendor third-party skill text. Preserve source attribution for factual research and avoid importing material whose license is incompatible with the repository's MIT license.
