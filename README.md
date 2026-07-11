# generative-media-skills

Supercharge your AI Agents as media generation experts. Introducing **more than 100 research-backed Agent Skills** for premium generative media production across **more than 15 categories**: image generation, video generation, text-to-speech, speech-to-text, music, sound effects, avatar video, voice agents, cinematic direction, post-production, content formats, delivery QA, provenance, and runtime assembly.

This is not a prompt-pack repo. It is a production-grade skill library for coding agents that need to make real media decisions: which provider to use, how to brief it, how to handle rights and provenance, how to QA the result, and how to ship usable creative assets.

Use it with **Claude Code**, **Codex**, **GitHub Copilot**, **Cursor**, **OpenClaw/Hermes-style agents**, or any agent runtime that can load markdown skills. Plug it into an [OpenMontage](https://github.com/calesthio/OpenMontage) workflow and give your agent a serious media-production brain.

## What is inside

- **Provider skills** for models and platforms like OpenAI image/audio, Google Veo/Gemini/Lyria, Runway, Luma, Kling, Seedance, Midjourney, ElevenLabs, Azure Speech, Amazon Nova/Polly/Transcribe, NVIDIA, Alibaba, xAI, and more.
- **Production skills** for cinematic shot direction, lighting, storyboard/previs, color, VFX, captions, sound design, music supervision, localization, media QA, provenance, and final delivery.
- **Format skills** for real deliverables: UGC ads, brand launch films, SaaS demos, music videos, game trailers, ecommerce product imagery, fashion campaigns, food/beverage content, real estate listings, avatar spokesperson videos, educational animation, and more.
- **Runtime assembly skills** for Remotion, HyperFrames, FFmpeg, ComfyUI, and Manim.

Every skill includes:

- `SKILL.md` — production guidance for the agent, with workflows, limitations, examples, and cited sources.
- `EVAL.md` — evaluator questions, expected answers, applied tasks, scoring guidance, and critical-failure checks.

The result: agents can do more than generate pretty outputs. They can reason about production intent, platform constraints, provider limits, safety, rights, QA, and delivery.

## Skill index

The full catalog lives in [SKILL_INDEX.md](SKILL_INDEX.md).

At a glance:

| Family | Category | Skills |
|---|---:|---:|
| Providers | Audio enhancement | 1 |
| Providers | Avatar video | 5 |
| Providers | Image generation | 18 |
| Providers | Music generation | 4 |
| Providers | Sound generation | 2 |
| Providers | Speech and voice | 6 |
| Providers | Speech to text | 3 |
| Providers | Text to speech | 7 |
| Providers | Video generation | 15 |
| Providers | Voice agents | 3 |
| Production | Audio craft | 7 |
| Production | Content formats | 17 |
| Production | Creative direction | 7 |
| Production | Governance and delivery | 5 |
| Production | Post-production | 5 |
| Production | Runtime assembly | 5 |

## Repository structure

```text
skills/
  providers/
    image-generation/<skill-name>/
    video-generation/<skill-name>/
    text-to-speech/<skill-name>/
    speech-to-text/<skill-name>/
    speech-and-voice/<skill-name>/
    music-generation/<skill-name>/
    sound-generation/<skill-name>/
    avatar-video/<skill-name>/
    voice-agents/<skill-name>/
    audio-enhancement/<skill-name>/
  production/
    creative-direction/<skill-name>/
    audio-craft/<skill-name>/
    post-production/<skill-name>/
    governance-delivery/<skill-name>/
    content-formats/<skill-name>/
    runtime-assembly/<skill-name>/

<skill-name>/
  SKILL.md
  EVAL.md
```

## How to use with agents

Point your agent at this repo and tell it to load the relevant skill before media work.

Example:

```text
Use generative-media-skills.
For this task, load:
- skills/providers/video-generation/seedance-2-0/SKILL.md
- skills/production/creative-direction/cinematic-shot-direction/SKILL.md
- skills/production/governance-delivery/media-qc-delivery/SKILL.md

Create a 15-second premium product launch clip and include a QA pass.
```

For evaluation, keep `EVAL.md` hidden from the producing agent. Use it only after the agent has completed the work.

## Why this matters

Generative media quality increasingly depends on orchestration, not just model access. The best outputs come from agents that understand provider behavior, creative direction, production craft, legal and platform constraints, asset continuity, and delivery requirements.

This repo gives those agents the missing layer: compact, research-backed operating knowledge for media production.

## Agent instructions

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

## License

MIT. See [LICENSE](LICENSE).
