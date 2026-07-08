# my_skills

Personal Codex skills and linked upstream skill collections.

## Layout

- `skills/` — my own installable Codex skills.
- `external/` — upstream skill packs as git submodules (e.g. `mattpocock/skills`, `addyosmani/agent-skills`). References, not copies.
- `skill-sources.json` — manifest of skill sources to install.
- `scripts/` — maintenance and install helpers.

## Setup

Clone with submodules and install everything:

```bash
git clone --recurse-submodules git@github.com:Alizen-1009/my_skills.git
cd my_skills
./scripts/bootstrap.sh
```

Already cloned without submodules? Run `git submodule update --init --recursive` first.

Restart Codex after installing or updating skills.

By default the installer symlinks into `${CODEX_HOME:-$HOME/.codex}/skills`, so re-running after a `git pull` updates everything in place. Use `--mode copy` for a standalone install, or `--force` to replace existing skills.

## Update upstream sources

```bash
git submodule update --remote --merge
```

Commit the submodule pointer changes to track newer upstream commits.

## Add a skill

**Personal skill** — create `skills/<skill-name>/` with a `SKILL.md` (and optionally `agents/openai.yaml`, `scripts/`, `references/`, `assets/`). Validate with:

```bash
python3 scripts/validate-skills.py
```

**Upstream source** — add a third-party repo as a submodule and register it:

```bash
python3 scripts/add-skill-source.py <name> <repo-url> [--recursive | --skills-path <path>]
./scripts/bootstrap.sh --dry-run   # preview, then run without --dry-run to install
```

Pick the path flag by repo shape: default for `skills/*`, `--recursive` for nested skill folders, `--skills-path .` when the repo root is a single skill, or `--skills-path <dir>` for one skill in a subdirectory.
