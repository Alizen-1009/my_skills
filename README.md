# my_skills

Personal Codex skills and linked upstream skill collections.

## Layout

- `skills/` - my own installable Codex skills.
- `skill-sources.json` - manifest of local and upstream skill sources to install.
- `external/mattpocock-skills` - linked upstream repo: `https://github.com/mattpocock/skills`.
- `external/addyosmani-agent-skills` - linked upstream repo: `https://github.com/addyosmani/agent-skills`.
- `scripts/` - repository maintenance helpers.

The `external/` repositories are git submodules. They are references to upstream projects, not copied source. The installer reads `skill-sources.json`, so adding another open source skill pack should not require editing installer code.

## Clone With External Sources

```bash
git clone --recurse-submodules git@github.com:Alizen-1009/my_skills.git
```

If the repository was cloned without submodules:

```bash
git submodule update --init --recursive
```

## Update External Sources

```bash
git submodule update --remote --merge
git status --short
```

Commit `.gitmodules` and the submodule pointer changes when you want this repo to track newer upstream commits.

## Add An Open Source Skill Source

Use `scripts/add-skill-source.py` to add a third-party repo as a submodule and register it in `skill-sources.json`:

```bash
python3 scripts/add-skill-source.py obra-superpowers https://github.com/obra/superpowers --recursive
./scripts/bootstrap.sh --dry-run
```

Common source shapes:

- Repo contains many skill folders under `skills/`: use the defaults.
- Repo contains nested skill folders under `skills/`: add `--recursive`.
- Repo root is a single skill folder with `SKILL.md`: use `--skills-path .`.
- Repo has one skill at a specific subdirectory: use `--skills-path path/to/skill`.

Examples:

```bash
python3 scripts/add-skill-source.py obra-superpowers https://github.com/obra/superpowers --recursive
python3 scripts/add-skill-source.py fockus-find-skill https://github.com/fockus/claude-skill-find-skill --skills-path .
python3 scripts/add-skill-source.py vercel-skills https://github.com/vercel-labs/skills --skills-path skills/find-skills
```

After checking the dry-run output, install:

```bash
./scripts/bootstrap.sh
```

## Add A Personal Skill

Put new skills under `skills/<skill-name>/`. Each skill must include:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml  # recommended
```

Optional directories inside a skill:

- `scripts/` for deterministic helpers.
- `references/` for longer docs loaded only when needed.
- `assets/` for templates, images, fonts, or other files used in outputs.

Validate local skills with:

```bash
python3 scripts/validate-skills.py
```

List the skills that would be installed:

```bash
python3 scripts/install-skills.py --list
```

## Install Skills Into Codex

After cloning this repository on a new machine, initialize the linked upstream repositories and install all discovered skills:

```bash
./scripts/bootstrap.sh
```

Restart Codex after installing or updating a skill.

By default the installer creates symlinks in `${CODEX_HOME:-$HOME/.codex}/skills`, so pulling this repo and rerunning the script updates installed skills without copying files around.

For a standalone install that does not depend on this repo path staying in place:

```bash
./scripts/bootstrap.sh --mode copy
```

If a destination skill already exists, the installer skips it. To replace existing installs:

```bash
./scripts/bootstrap.sh --force
```
