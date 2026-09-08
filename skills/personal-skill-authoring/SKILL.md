---
name: personal-skill-authoring
description: Create, adapt, or maintain personal skills in this repository, including structure, triggers, and local validation.
---

# Personal Skill Authoring

Maintain personal skills under `skills/<skill-name>/SKILL.md`. Before adding one, check for an existing skill covering the same need. Filter upstream selections in `skill-sources.json`; leave upstream copies unchanged.

## Skill design

- Use frontmatter with `name` and a short `description` stating distinct task triggers. Avoid triggers such as “every edit” or “before finishing any task.”
- Keep project invariants and tool-specific pitfalls; omit generic coaching the model can already apply.
- Put shared essentials in `SKILL.md`. For multiple workflows, link branch-specific material from a small router with explicit reading conditions.
- Add `scripts/` for deterministic helpers, `references/` for on-demand detail, and `assets/` for deliverable resources only when useful.
- Prefer outcome and safety boundaries to fixed itineraries, mandatory skill chains, or blanket approval/test/search requirements.
- Keep skill guidance subordinate to the user's explicit task within applicable safety and repository constraints.

Optional UI metadata belongs in `agents/openai.yaml`. Keep its default prompt consistent with the skill; do not reintroduce removed workflow gates there. Use `disable-model-invocation: true` only for deliberately manual skills; Pi then exposes them through `/skill:name` without adding their descriptions to the model prompt.

When adapting upstream material, read the source skill and retain attribution in repository documentation. Keep repository installation instructions outside individual skill folders.

## Validation

Run `python3 scripts/validate-skills.py` after personal skill edits. Regenerate the catalog with `python3 scripts/install-skills.py --write-catalog` and verify it with `--check-catalog`. No model benchmark or unrelated installer test run is required for a prose-only edit unless a concrete risk calls for one.
