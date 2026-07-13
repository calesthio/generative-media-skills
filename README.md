# Generative Media Skills

**Give your coding agent a media production department, not a folder of prompts.**

Generative Media Skills is an agent-native production system for creating, directing, validating, and delivering image, video, audio, voice, music, 3D, avatar, and interactive media. It combines researched operating knowledge with executable guardrails so agents can move from a creative brief to a usable deliverable with provider context, production craft, safety boundaries, and technical checks.

**145 research-backed skills across 25 categories, with tested executable resources where deterministic checks are better than prose.**

Use it with **Claude Code**, **Codex**, **GitHub Copilot**, **Cursor**, **OpenClaw/Hermes-style agents**, or any runtime that can load Agent Skills. Connect it to [OpenMontage](https://github.com/calesthio/OpenMontage) when you want the same production intelligence inside an orchestrated media workflow.

> It is operating knowledge and executable production support that helps an agent make evidence-based media decisions and prepare shippable work.

## Start in One Prompt

Point your agent at the repository and name the production surfaces it should load:

```text
Use generative-media-skills.
Load:
- skills/providers/video-generation/seedance-2-0/SKILL.md
- skills/production/creative-direction/cinematic-shot-direction/SKILL.md
- skills/production/audio-craft/sound-design-foley/SKILL.md
- skills/production/governance-delivery/media-qc-delivery/SKILL.md

Create a 15-second premium product launch clip. Include the shot plan,
generation prompts, sound direction, rights/provenance notes, and final QA pass.
```

The agent gets researched judgment from the skills and can use bundled resources when the task benefits from deterministic execution.

## From Brief to Delivery

One repository covers the production chain:

1. **Choose the right system** - compare current providers, model families, APIs, gateways, local runtimes, costs, limits, and data paths.
2. **Direct the work** - apply cinematography, lighting, performance, production design, visual continuity, sound, music, editing, and accessibility craft.
3. **Build real deliverables** - produce ads, launch films, social shorts, explainers, game trailers, product imagery, podcasts, avatar videos, real-estate media, and more.
4. **Run deterministic checks** - inspect media, captions, 3D assets, ComfyUI graphs, HyperFrames timelines, gateway plans, loudness, checksums, and QA reports.
5. **Ship with evidence** - handle provenance, rights, consent, localization, platform requirements, manifests, and final delivery QA.

The agent gets judgment where judgment matters and executable validation where prose is not enough. When a skill includes executable resources, its `SKILL.md` explains when and how to use them.

## Why It Is Different

- **Current provider intelligence** - skills cite official docs, model cards, API references, pricing surfaces, limits, and verification dates for volatile facts.
- **Real production craft** - the library covers how to direct and finish media, not only how to call a model.
- **Executable guardrails** - deterministic work moves into tested scripts instead of being repeatedly improvised from code blocks.
- **Evaluation built in** - every skill has a repository-only `EVAL.md` with subject-specific scoring, applied tasks, and critical failures.
- **Provider-independent workflows** - production skills remain useful when models and vendors change.
- **Progressive disclosure** - agents load the entrypoint first, then scripts, references, or assets only when the task needs them.
- **Portable publication** - skills can be bundled without leaking hidden evaluations or repository-only tests.

## Full Catalog

Browse all 145 packages in [SKILL_INDEX.md](SKILL_INDEX.md).

At a glance:

| Family | Category | Skills |
|---|---:|---:|
| Providers | 3D generation | 3 |
| Providers | Audio enhancement | 1 |
| Providers | Avatar video | 5 |
| Providers | Image generation | 18 |
| Providers | Image understanding | 2 |
| Providers | Lip sync | 1 |
| Providers | Motion capture | 2 |
| Providers | Music generation | 5 |
| Providers | Sound generation | 2 |
| Providers | Source separation | 1 |
| Providers | Speech and voice | 6 |
| Providers | Speech to text | 3 |
| Providers | Text to speech | 9 |
| Providers | Video enhancement | 1 |
| Providers | Video generation | 19 |
| Providers | Video understanding | 1 |
| Providers | Voice agents | 4 |
| Providers | World models | 2 |
| Production | 3D craft | 2 |
| Production | Audio craft | 7 |
| Production | Content formats | 22 |
| Production | Creative direction | 8 |
| Production | Governance and delivery | 5 |
| Production | Post-production | 6 |
| Production | Runtime assembly | 10 |

## Repository Structure

```text
skills/
  providers/
    3d-generation/<skill-name>/
    image-generation/<skill-name>/
    image-understanding/<skill-name>/
    video-generation/<skill-name>/
    video-enhancement/<skill-name>/
    video-understanding/<skill-name>/
    world-models/<skill-name>/
    lip-sync/<skill-name>/
    motion-capture/<skill-name>/
    source-separation/<skill-name>/
    text-to-speech/<skill-name>/
    speech-to-text/<skill-name>/
    speech-and-voice/<skill-name>/
    music-generation/<skill-name>/
    sound-generation/<skill-name>/
    avatar-video/<skill-name>/
    voice-agents/<skill-name>/
    audio-enhancement/<skill-name>/
  production/
    3d-craft/<skill-name>/
    creative-direction/<skill-name>/
    audio-craft/<skill-name>/
    post-production/<skill-name>/
    governance-delivery/<skill-name>/
    content-formats/<skill-name>/
    runtime-assembly/<skill-name>/

<skill-name>/
  SKILL.md
  EVAL.md
  scripts/       optional, bundled when present
  references/    optional, bundled when present
  assets/        optional, bundled when present
  tests/         optional, repository-only

tools/
  repository maintenance tooling, such as package export
```

## What Is Inside a Skill

Every authoring package contains:

- `SKILL.md` - the production entrypoint: decisions, workflows, limitations, examples, and cited sources.
- `EVAL.md` - the hidden evaluator: expected answers, applied tasks, scoring, and critical failures.

When the subject benefits from progressive disclosure, a skill may also contain:

- `scripts/` - publishable executable helpers.
- `references/` - publishable on-demand documentation.
- `assets/` - publishable static resources.
- `tests/` - repository-only validation for bundled resources.

The producing agent receives the published package, never `EVAL.md` or repository tests.

## Built for Agent Workflows

Use the repository directly with Claude Code, Codex, GitHub Copilot, Cursor, OpenClaw/Hermes-style agents, or compatible Agent Skills runtimes. Skills are plain Markdown plus optional portable resources, so they can be inspected, copied, packaged, evaluated, and orchestrated without adopting a proprietary runtime.

The design principle is simple: **reason with evidence, execute deterministically, and keep final approval accountable.**

## Contributing

New skills are independently researched and separately reviewed. Executable resources must be materially better than prose, portable, safe by default, dependency-explicit, and covered by failure and safety tests. See [CONTRIBUTING.md](CONTRIBUTING.md) and [METHODOLOGY.md](METHODOLOGY.md).

## Agent Instructions

`AGENTS.md` is the canonical instruction file for this repository. Other agent entrypoints in this repo delegate back to it:

- `CLAUDE.md`
- `GEMINI.md`
- `.github/copilot-instructions.md`
- `.cursor/rules/generative-media-skills.mdc`
- `.windsurf/rules/generative-media-skills.md`
- `.clinerules`
- `.roo/rules/generative-media-skills.md`
- `OPENCLAW.md`
- `HERMES.md`

Before editing or reviewing skills, read [AGENTS.md](AGENTS.md) and [METHODOLOGY.md](METHODOLOGY.md).

If this project gives your agents a stronger production brain, a GitHub star helps more builders find it.

## License

MIT. See [LICENSE](LICENSE).
