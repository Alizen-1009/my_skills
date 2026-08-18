# my_skills

A portable, secret-free personal configuration repository for the [Pi coding agent](https://pi.dev/). It keeps my Pi CLI version, settings, extensions, packages, and curated skills reproducible across development machines, while still supporting skill installation for Codex and Claude Code.

## Purpose

This repository is the source of truth for the parts of my Pi environment that are safe and useful to share between machines:

- install the pinned Pi CLI version;
- restore portable Pi preferences;
- install pinned Pi packages and extension configuration;
- install personal skills and selected upstream skill collections;
- make a new machine usable with one bootstrap command.

It deliberately does **not** synchronize credentials, conversation history, trust decisions, caches, or other machine-specific runtime state.

## What is synchronized

| Resource | Repository source | Installed location |
| --- | --- | --- |
| Pi CLI | `piVersion` in `pi-packages.json` | global npm installation |
| Portable Pi settings | `pi-config/settings.patch.json` | merged into `~/.pi/agent/settings.json` |
| Extension configuration | `pi-config/` | matching paths under `~/.pi/agent/` |
| Pi packages | `pi-packages.json` | managed by `pi install` |
| Personal skills | `skills/` | `~/.pi/agent/skills/` by default |
| Upstream skills | `external/` + `skill-sources.json` | `~/.pi/agent/skills/` by default |

Package versions and Git revisions are pinned so two machines do not silently load different extension code.

## What is not synchronized

The following remain local and must never be committed:

- `~/.pi/agent/auth.json` and API keys;
- session history and compaction artifacts;
- `trust.json`, package caches, cloned package contents, and model-catalog caches;
- machine-specific absolute skill paths;
- secrets embedded in MCP or custom-provider configuration.

On a new machine, authenticate separately with `/login`. The default configuration currently uses `openai-codex`, so run `/login openai-codex` when required.

## New machine setup

Prerequisites:

- Git;
- Python `3.9` or newer;
- Node.js `22.19.0` or newer;
- npm available on `PATH`.

```bash
git clone --recurse-submodules git@github.com:Alizen-1009/my_skills.git
cd my_skills
./scripts/bootstrap.sh
```

Bootstrap performs these steps:

1. checks out the recorded submodule revisions;
2. installs or reconciles the pinned Pi CLI version;
3. installs the selected skills;
4. installs pinned Pi packages;
5. merges portable settings and synchronizes extension configuration.

Then start Pi and authenticate if needed:

```bash
pi
```

```text
/login openai-codex
```

Preview without changing the machine (including leaving submodules untouched):

```bash
./scripts/bootstrap.sh --dry-run
```

## Daily synchronization

Pull repository changes and reconcile the local machine:

```bash
git pull --recurse-submodules
./scripts/bootstrap.sh
```

To change a portable Pi preference, edit `pi-config/settings.patch.json` and run bootstrap. The file uses JSON Merge Patch semantics:

- objects merge recursively;
- arrays and scalar values replace the managed value;
- `null` removes a setting;
- settings not mentioned in the patch remain local.

This preserves Pi's package list, changelog state, and optional machine-specific skill paths while keeping the selected model, thinking level, compaction policy, retry policy, and UI preferences consistent.

## Managed Pi packages

`pi-packages.json` currently pins packages such as:

- `pi-goal-runtime` for persistent, verifiable goals;
- `pi-continue` for safe mid-run compaction and same-session continuation during long tool loops;
- planning, side-question, web access, MCP, subagent, and TUI extensions.

Pi's native compaction stays enabled and owns the threshold and persisted compaction format. `pi-continue` adds the long-running tool-loop handoff and resume behavior.

After changing package or extension configuration in a running Pi process, run `/reload` or restart Pi.

## Skills

Local skills live under `skills/`. Upstream skill repositories are Git submodules under `external/` and are filtered by `skill-sources.json`.

List the authoritative install set:

```bash
python3 scripts/install-skills.py --list
```

Validate personal skills:

```bash
python3 scripts/validate-skills.py
```

Regenerate and verify the committed catalog after changing local skills or source filters:

```bash
python3 scripts/install-skills.py --write-catalog
python3 scripts/install-skills.py --check-catalog
```

The installer prunes a symlink only when its name is explicitly excluded in `skill-sources.json` and its target exactly matches that excluded source path. Other links, copied directories, and machine-managed skills are left untouched.

Update upstream repositories intentionally, review the changes, and commit the new submodule revisions:

```bash
git submodule update --remote --merge
```

### Other harnesses

Pi is the default target. Skills can also be installed without configuring Pi:

```bash
./scripts/bootstrap.sh --agent codex
./scripts/bootstrap.sh --agent claude
./scripts/bootstrap.sh --agent pi,codex
./scripts/bootstrap.sh --dest <directory>
```

| Agent | Skills directory | Home override |
| --- | --- | --- |
| Pi | `~/.pi/agent/skills` | `PI_CODING_AGENT_DIR` |
| Codex | `~/.codex/skills` | `CODEX_HOME` |
| Claude Code | `~/.claude/skills` | — |

## Repository layout

- `pi-config/` — portable Pi settings patches and extension configuration.
- `pi-packages.json` — pinned Pi CLI and package versions.
- `skills/` — personal skills maintained in this repository.
- `external/` — upstream skill collections tracked as submodules.
- `skill-sources.json` — enabled sources, paths, and exclusions.
- `scripts/` — bootstrap, installation, source-management, and validation tools.
- `tests/` — installer and configuration regression tests.
- `SKILLS.md` — generated catalog of the authoritative default install set.
- `THIRD_PARTY.md` — upstream projects consulted when adapting skills.

## Adding a skill

Create a personal skill under `skills/<skill-name>/` with a `SKILL.md`, then validate it:

```bash
python3 scripts/validate-skills.py
```

Add an upstream skill collection as a submodule and register it:

```bash
python3 scripts/add-skill-source.py <name> <repo-url> [--recursive | --skills-path <path>]
./scripts/bootstrap.sh --dry-run
```

Use default discovery for `skills/*`, `--recursive` for nested skill folders, `--skills-path .` when the repository root is one skill, or `--skills-path <dir>` for a specific subdirectory.

## Security boundary

Before committing Pi configuration:

1. keep credentials in `auth.json`, environment variables, or an external secret manager;
2. reference secrets from MCP/custom-provider config through environment variables rather than literals;
3. check `git status` and the staged diff for tokens, cookies, private URLs, and machine-specific paths;
4. never force-add files ignored by the Pi security rules in `.gitignore`.
