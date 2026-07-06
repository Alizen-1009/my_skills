---
name: personal-skill-authoring
description: Create and maintain personal Codex skills inside a reusable skills repository. Use when adding a new personal skill, adapting an upstream skill into this repo, deciding what belongs in SKILL.md versus scripts/references/assets, validating skill structure, or preparing a skill for local installation.
---

# Personal Skill Authoring

## Overview

Use this skill to add, adapt, and maintain skills in a personal Codex skills repository. Keep each skill small, installable, and focused on instructions another Codex session can reliably follow.

## Repository Workflow

1. Confirm whether the work is a new personal skill, an adaptation of an upstream skill, or a maintenance update.
2. Search existing `skills/` entries before creating a new one.
3. Review relevant upstream examples under `external/` when useful, but avoid copying large sections blindly.
4. Create or edit only the skill folder under `skills/<skill-name>/`.
5. Validate the changed skill before finishing.

## Skill Structure

Every personal skill must have:

```text
skills/<skill-name>/
  SKILL.md
```

Recommended UI metadata:

```text
skills/<skill-name>/
  agents/openai.yaml
```

Add optional resources only when they materially improve repeatability:

- `scripts/` for executable helpers that should be deterministic.
- `references/` for detailed docs, schemas, examples, or policies loaded only when needed.
- `assets/` for templates, images, fonts, starter files, or other output resources.

Do not add README, quick reference, changelog, or installation guide files inside an individual skill. Put repository-level documentation at the repo root.

## Writing SKILL.md

Use this frontmatter shape:

```markdown
---
name: skill-name
description: Clear description of what the skill does and exactly when to use it.
---
```

Keep the body concise:

- Start with a short overview.
- Give the operational workflow.
- Link to resource files only when they should be read.
- Prefer imperative instructions over general explanation.
- Include examples only when they prevent ambiguity.

## Adapting Upstream Skills

When adapting from `external/mattpocock-skills` or `external/addyosmani-agent-skills`:

1. Identify the source skill and read its `SKILL.md`.
2. Decide whether to use it as-is, fork a personal variant, or combine ideas into an existing personal skill.
3. Preserve the useful workflow, but rewrite triggers, paths, tools, and assumptions for this repository.
4. Keep attribution in commit messages or repo docs when copying meaningful content.
5. Validate the resulting personal skill as its own installable artifact.

## Validation

Run:

```bash
python3 scripts/validate-skills.py
```

Fix any invalid frontmatter, missing `SKILL.md`, mismatched folder/name, or stale template placeholders before finishing.
