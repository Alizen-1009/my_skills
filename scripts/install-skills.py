#!/usr/bin/env python3
"""Install this repository's skills into every agent harness found on this machine."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Skill:
    name: str
    path: Path
    source: str


@dataclass(frozen=True)
class Source:
    id: str
    root: Path
    source: str
    recursive: bool
    include: frozenset[str]
    exclude: frozenset[str]


@dataclass(frozen=True)
class Target:
    id: str
    home: Path
    skills_dir: Path
    restart_hint: str


def agent_home(env_var: str, default: str) -> Path:
    override = os.environ.get(env_var)
    if override:
        return Path(override).expanduser()
    return Path.home() / default


def known_targets() -> list[Target]:
    """Agent harnesses this repo can install into, in install order."""
    codex_home = agent_home("CODEX_HOME", ".codex")
    pi_home = agent_home("PI_CODING_AGENT_DIR", ".pi/agent")
    claude_home = Path.home() / ".claude"
    return [
        Target("codex", codex_home, codex_home / "skills", "Restart Codex"),
        Target("pi", pi_home, pi_home / "skills", "Restart pi"),
        Target("claude", claude_home, claude_home / "skills", "Restart Claude Code"),
    ]


def detect_targets(requested: list[str] | None) -> tuple[list[Target], list[str]]:
    """Resolve --agent names, or auto-detect harnesses whose home directory exists."""
    targets = {target.id: target for target in known_targets()}
    if requested:
        unknown = [name for name in requested if name not in targets]
        if unknown:
            return [], unknown
        return [targets[name] for name in dict.fromkeys(requested)], []
    return [target for target in targets.values() if target.home.is_dir()], []


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_sources(root: Path) -> list[Source]:
    manifest_path = root / "skill-sources.json"
    if not manifest_path.exists():
        print(f"Missing source manifest: {manifest_path}", file=sys.stderr)
        return []

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"Invalid JSON in {manifest_path}: {error}", file=sys.stderr)
        return []

    entries = manifest.get("sources")
    if not isinstance(entries, list):
        print("skill-sources.json must contain a sources array", file=sys.stderr)
        return []

    sources: list[Source] = []
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("enabled", True):
            continue

        source_id = str(entry.get("id", "")).strip()
        kind = str(entry.get("kind", "")).strip()
        path = str(entry.get("path", "")).strip()
        if not source_id or not kind or not path:
            print(f"Skipping invalid source entry: {entry}", file=sys.stderr)
            continue

        if kind == "local":
            source_root = root / path
        elif kind == "git-submodule":
            skills_path = str(entry.get("skills_path", "skills")).strip() or "."
            source_root = root / path / skills_path
        else:
            print(f"Skipping unknown source kind {kind!r} for {source_id}", file=sys.stderr)
            continue

        include = frozenset(str(name) for name in entry.get("include", []))
        exclude = frozenset(str(name) for name in entry.get("exclude", []))
        label = str(entry.get("repo") or source_id)
        sources.append(
            Source(
                id=source_id,
                root=source_root,
                source=label,
                recursive=bool(entry.get("recursive", False)),
                include=include,
                exclude=exclude,
            )
        )

    return sources


def discover_skills(source: Source) -> list[Skill]:
    root = source.root
    if not root.exists():
        return []

    skill_files: list[Path] = []
    root_skill = root / "SKILL.md"
    if root_skill.exists():
        skill_files.append(root_skill)

    if source.recursive:
        skill_files.extend(sorted(root.rglob("SKILL.md")))
    else:
        skill_files.extend(sorted(root.glob("*/SKILL.md")))

    skills: list[Skill] = []
    seen_paths: set[Path] = set()
    for skill_file in skill_files:
        skill_file = skill_file.resolve()
        if skill_file in seen_paths:
            continue
        seen_paths.add(skill_file)

        skill_dir = skill_file.parent
        if source.include and skill_dir.name not in source.include:
            continue
        if skill_dir.name in source.exclude:
            continue
        skills.append(Skill(name=skill_dir.name, path=skill_dir.resolve(), source=source.source))
    return skills


def discover_all(root: Path) -> tuple[list[Skill], list[str]]:
    chosen: dict[str, Skill] = {}
    warnings: list[str] = []

    for source in load_sources(root):
        for skill in discover_skills(source):
            existing = chosen.get(skill.name)
            if existing:
                warnings.append(
                    f"duplicate skill {skill.name!r}: keeping {existing.source}, skipping {source.source}"
                )
                continue
            chosen[skill.name] = skill

    return list(chosen.values()), warnings


def is_link_to(path: Path, target: Path) -> bool:
    return path.is_symlink() and path.resolve() == target.resolve()


def read_description(skill: Skill) -> str:
    skill_md = skill.path / "SKILL.md"
    try:
        text = skill_md.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = skill_md.read_text(errors="ignore")

    if not text.startswith("---"):
        return ""

    end = text.find("\n---", 4)
    if end == -1:
        return ""

    for raw_line in text[4:end].splitlines():
        line = raw_line.strip()
        if line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip("\"'")
            return " ".join(description.split())
    return ""


def print_skill_list(skills: list[Skill], warnings: list[str]) -> None:
    for warning in warnings:
        print(f"[WARN] {warning}")

    for skill in sorted(skills, key=lambda item: item.name):
        description = read_description(skill)
        if description:
            print(f"{skill.name}\t{skill.source}\t{description}")
        else:
            print(f"{skill.name}\t{skill.source}")


def install_skill(skill: Skill, dest_dir: Path, mode: str, force: bool, dry_run: bool) -> str:
    dest = dest_dir / skill.name

    if dest.exists() or dest.is_symlink():
        if is_link_to(dest, skill.path):
            return f"[OK] {skill.name} already linked"
        if not force:
            return f"[SKIP] {skill.name} exists at {dest}"
        if dry_run:
            return f"[DRY] replace {dest} with {mode} from {skill.path}"
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        else:
            shutil.rmtree(dest)

    if dry_run:
        return f"[DRY] install {skill.name} from {skill.source}"

    dest_dir.mkdir(parents=True, exist_ok=True)
    if mode == "copy":
        shutil.copytree(skill.path, dest, symlinks=True)
    else:
        dest.symlink_to(skill.path, target_is_directory=True)

    return f"[OK] installed {skill.name} from {skill.source}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install local and linked upstream skills into every detected agent harness.",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        help="Install into one explicit directory instead of the detected harnesses.",
    )
    parser.add_argument(
        "--agent",
        help="Comma-separated harnesses to install into: codex, pi, claude. "
        "Defaults to every harness whose home directory exists.",
    )
    parser.add_argument(
        "--mode",
        choices=("symlink", "copy"),
        default="symlink",
        help="Install by symlink for easy updates or copy for a standalone install.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing destination skill folders or symlinks.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without changing files.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List discovered skills with source and frontmatter description.",
    )
    args = parser.parse_args()
    if args.dest and args.agent:
        print("Use either --dest or --agent, not both.", file=sys.stderr)
        return 1

    root = repo_root()
    skills, warnings = discover_all(root)
    if not skills:
        print("No skills found. Did you initialize submodules?", file=sys.stderr)
        print("Run: git submodule update --init --recursive", file=sys.stderr)
        return 1

    if args.list:
        print_skill_list(skills, warnings)
        return 0

    for warning in warnings:
        print(f"[WARN] {warning}")

    if args.dest:
        targets = [Target("dest", args.dest.expanduser(), args.dest.expanduser(), "Restart the agent")]
    else:
        requested = [name.strip() for name in args.agent.split(",") if name.strip()] if args.agent else None
        targets, unknown = detect_targets(requested)
        if unknown:
            valid = ", ".join(target.id for target in known_targets())
            print(f"Unknown agent(s): {', '.join(unknown)}. Valid: {valid}", file=sys.stderr)
            return 1
        if not targets:
            valid = ", ".join(f"{t.id} ({t.home})" for t in known_targets())
            print("No agent harness detected. Looked for: " + valid, file=sys.stderr)
            print("Pass --dest <dir> to install somewhere else.", file=sys.stderr)
            return 1

    sorted_skills = sorted(skills, key=lambda item: item.name)
    for target in targets:
        dest_dir = target.skills_dir
        print()
        print(f"=== {target.id} -> {dest_dir}")
        for skill in sorted_skills:
            print(install_skill(skill, dest_dir, args.mode, args.force, args.dry_run))

    print()
    for target in targets:
        print(f"{target.restart_hint} to pick up installed or updated skills in {target.skills_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
