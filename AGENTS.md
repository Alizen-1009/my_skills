# AGENTS.md

## Repository boundaries

This repository is the portable, secret-free source of truth for the owner's Pi setup: pinned CLI/packages, portable configuration, and curated skills.

- Keep reproducible settings in `pi-config/settings.patch.json`. It merges into local settings; do not manage the dynamic `packages` list or machine-specific skill paths there.
- Keep extension configuration under `pi-config/`, with paths relative to `~/.pi/agent/`.
- Pin Pi and package versions in `pi-packages.json`; bootstrap must remain safe and idempotent.
- Maintain personal skills in `skills/`. Filter upstream skills through `skill-sources.json`; do not edit upstream copies.
- Never commit credentials, `auth.json`, sessions, trust decisions, caches, cookies, or machine-specific private paths. New-machine authentication remains a manual `/login` step.

## Execution

Complete authorized work through implementation and relevant verification. Resolve routine, reversible details from context; ask only when a missing decision materially changes scope, correctness, or safety. Approval is needed for destructive or external actions not already authorized, not for each local edit or check.

Keep changes within the request and preserve unrelated user work. Discovery interviews, prototypes, formal plans, acceptance quizzes, and independent reviews are optional techniques, not default gates. Use them when requested or when they resolve a concrete uncertainty. Delegate independent work when it saves time or improves confidence; avoid duplicating it in the parent.

## Verification

- Installer or bootstrap changes: run `python3 -m unittest discover -s tests`.
- Personal skill changes: run `python3 scripts/validate-skills.py`.
- Skill content or selection changes: regenerate `SKILLS.md` with `python3 scripts/install-skills.py --write-catalog`, then check with `--check-catalog`. For selection changes, also inspect the installer's `--dry-run` output.

Choose checks appropriate to the change. Once they pass, repeat or broaden them only for new edits, failures, or unresolved risks. Report what was verified and any remaining limitation; do not require a user quiz to finish authorized work.
