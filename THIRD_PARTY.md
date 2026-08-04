# Third-party inspirations

The personal academic skills in `skills/` were written for this repository after reviewing the following upstream projects. They are compact adaptations of workflows and general principles; no upstream hooks, agent definitions, executable scripts, proprietary Office resources, or large reference bundles are included.

## Research Writing Assistant

- Project: [Norman-bury/research-writing-skill](https://github.com/Norman-bury/research-writing-skill)
- Reviewed revision: `6f7959554b4614d879d79cb4ece9ed04a7c8a88c`
- License: MIT
- Author notice: Copyright (c) 2026 旬常
- Ideas adapted: evidence-driven writing, explicit separation of planning data from real results, literature-review verification, and staged manuscript self-review.

## Academic Research Skills

- Project: [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)
- Reviewed revision: `2cf3a51e159458b7a8c8784bb874248e79601f7b`
- License: CC BY-NC 4.0
- Author: Cheng-I Wu
- Attribution requested upstream: “Based on Academic Research Skills by Cheng-I Wu — https://github.com/Imbad0202/academic-research-skills”
- Ideas consulted: distinguishing citation existence from claim support, revision traceability, bounded claim strength, and integrity-oriented review gates.

The upstream implementation is not bundled because it is Claude Code-specific, carries a non-commercial license, and depends on its own hooks, scripts, schemas, and multi-agent runtime.

## Academic Skills for Claude Code & Codex

- Project: [zLanqing/codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills)
- Reviewed revision: `7ed6377f0efb6a38951b48ef03b19d996e454b1f`
- Repository license: MIT, subject to separate licenses on bundled third-party material
- Ideas adapted: concise Chinese-first academic-writing routing, preservation of technical notation, and explicit labeling of supplied evidence, inference, and suggestions.

The upstream Office and scientific reference bundles are not included. Some embedded files use licenses that are more restrictive than the repository-level MIT notice, and the Office functionality already exists in this environment's dedicated `docx`, `pptx`, `pdf`, and `xlsx` skills.

## Agent Skills Garden — Minimal Diff

- Project: [dhruvinrsoni/agentskills-garden](https://github.com/dhruvinrsoni/agentskills-garden)
- Source skill: [`minimal-diff`](https://github.com/dhruvinrsoni/agentskills-garden/tree/c94cf3f3d7463e7e77eaa08b54d04195a24cd533/skills/100-engineering/25-pragmatism/minimal-diff)
- Reviewed revision: `c94cf3f3d7463e7e77eaa08b54d04195a24cd533`
- License: Apache-2.0
- Ideas adapted: explicit diff envelopes, drive-by edit detection, proportional diff-size checks, concern separation, and reversibility review.

The local version is a compact rewrite for this repository. It removes dependencies on the upstream constitution, scratchpad, auditor, and other Agent Skills Garden runtime conventions.
