# Contributing

Contributions should make AI agents materially better at a specific media-production task.

## Before authoring

1. Read `METHODOLOGY.md`.
2. Define a narrow, coherent skill scope.
3. Check that the proposed skill is not merely a rename of an existing scope.
4. Work in an isolated branch or worktree.
5. Do not inspect completed sibling skills for a structure or writing style to copy.

## Authoring

Create exactly:

```text
skills/<family>/<category>/<skill-name>/SKILL.md
skills/<family>/<category>/<skill-name>/EVAL.md
```

Use `providers` for provider/model/runtime skills and `production` for provider-independent media-production practice. Select the narrowest capability or discipline category already present; add a new category only with its first accepted skill. Use a lowercase kebab-case skill directory name. The `name` in `SKILL.md` frontmatter must match the leaf directory.

Research the subject independently and cite consequential claims. Include complete, labeled examples when they improve production performance. Build evaluations from the subject's actual capabilities, decisions, and failure modes.

## Review checklist

- [ ] The directory contains only `SKILL.md` and `EVAL.md`.
- [ ] The skill was independently researched.
- [ ] The skill does not imitate a sibling skill's flavor or conclusions.
- [ ] The frontmatter name and directory match.
- [ ] The description clearly states what triggers the skill.
- [ ] Documented facts, observations, and heuristics are distinguishable.
- [ ] Consequential claims have authoritative sources.
- [ ] Volatile facts have verification dates.
- [ ] Examples are complete and labeled as examples.
- [ ] `EVAL.md` includes expected answers or scoring criteria.
- [ ] Applied tasks test real production ability.
- [ ] Evaluation can run without exposing `EVAL.md` to the tested agent.
- [ ] Safety, consent, privacy, and rights issues are addressed where relevant.

## Licensing

The project license has not yet been selected. Do not copy or vendor third-party skill text. Preserve source attribution for factual research and avoid importing material whose license is incompatible with the future repository license.
