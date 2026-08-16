# my_skills

Personal agent skills, linked upstream skill collections, and managed Pi packages. Installs into Codex, pi, and Claude Code.

## Layout

- `skills/` — my own installable skills.
- `external/` — upstream skill packs tracked as git submodules. References, not copies.
- `skill-sources.json` — manifest of skill sources to install.
- `pi-packages.json` — pinned Pi packages to install when Pi is targeted.
- `scripts/` — maintenance and install helpers.
- `SKILLS.md` — catalog of installable skills grouped by source.
- `THIRD_PARTY.md` — upstream projects consulted when adapting personal skills.

## Skill sources

Bootstrap installs enabled skills from the local collection and these upstream repositories:

- [mattpocock/skills](https://github.com/mattpocock/skills)
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- [anthropics/skills](https://github.com/anthropics/skills)
- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
- [powerycy/goutoujunshi](https://github.com/powerycy/goutoujunshi)

See `skill-sources.json` for enabled sources, selected paths, and exclusions. Run `python3 scripts/install-skills.py --list` for the authoritative installable-skill list.

## Setup

Clone with submodules and install everything:

```bash
git clone --recurse-submodules git@github.com:Alizen-1009/my_skills.git
cd my_skills
./scripts/bootstrap.sh
```

Already cloned without submodules? Run `git submodule update --init --recursive` first.

Restart the agent after installing or updating skills.

### Install targets

The installer auto-detects every agent harness whose home directory exists and installs into all of them:

| Agent | Skills directory | Home override |
| --- | --- | --- |
| Codex | `~/.codex/skills` | `CODEX_HOME` |
| pi | `~/.pi/agent/skills` | `PI_CODING_AGENT_DIR` |
| Claude Code | `~/.claude/skills` | — |

```bash
./scripts/bootstrap.sh                    # every detected harness
./scripts/bootstrap.sh --agent pi         # one harness (or --agent pi,codex)
./scripts/bootstrap.sh --dest <dir>       # an explicit directory
```

Skills install as symlinks into this repo, so re-running after a `git pull` updates everything in place. Existing entries the installer did not create are reported as `[SKIP]` and left alone — pass `--force` to replace them. Use `--mode copy` for a standalone install.

When Pi is among the selected targets, bootstrap also installs the pinned packages in `pi-packages.json`. Package refs are intentionally pinned; update the manifest explicitly after reviewing a newer revision.

## Managed Pi packages

The current package set includes `pi-goal-runtime`, which adds persistent `/goal` commands and automatic continuation for long-running Pi tasks. Install or reconcile Pi resources with:

```bash
./scripts/bootstrap.sh --agent pi
```

After package changes, restart Pi or run `/reload`.

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
