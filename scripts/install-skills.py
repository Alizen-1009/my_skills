#!/usr/bin/env python3
"""Install this repository's skills into a supported agent harness."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass, replace
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
    """Resolve --agent names, defaulting to Pi when none are provided."""
    targets = {target.id: target for target in known_targets()}
    requested = requested or ["pi"]
    unknown = [name for name in requested if name not in targets]
    if unknown:
        return [], unknown
    return [targets[name] for name in dict.fromkeys(requested)], []


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_sources(root: Path) -> list[Source]:
    manifest_path = root / "skill-sources.json"
    if not manifest_path.exists():
        raise ValueError(f"Missing source manifest: {manifest_path}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {manifest_path}: {error}") from error

    entries = manifest.get("sources")
    if not isinstance(entries, list):
        raise ValueError("skill-sources.json must contain a sources array")

    sources: list[Source] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"source entry {index} must be an object")
        if not entry.get("enabled", True):
            continue

        source_id = str(entry.get("id", "")).strip()
        kind = str(entry.get("kind", "")).strip()
        path = str(entry.get("path", "")).strip()
        if not source_id or not kind or not path:
            raise ValueError(f"invalid enabled source entry {index}: {entry}")

        if kind == "local":
            source_root = root / path
        elif kind == "git-submodule":
            skills_path = str(entry.get("skills_path", "skills")).strip() or "."
            source_root = root / path / skills_path
        else:
            raise ValueError(f"unknown kind {kind!r} for source {source_id}")

        include_value = entry.get("include", [])
        exclude_value = entry.get("exclude", [])
        if not isinstance(include_value, list) or not isinstance(exclude_value, list):
            raise ValueError(f"include/exclude must be arrays for source {source_id}")
        include = frozenset(str(name) for name in include_value)
        exclude = frozenset(str(name) for name in exclude_value)
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


def discover_sources(sources: list[Source]) -> tuple[list[Skill], list[str]]:
    chosen: dict[str, Skill] = {}
    warnings: list[str] = []

    for source in sources:
        for skill in discover_skills(source):
            existing = chosen.get(skill.name)
            if existing:
                warnings.append(
                    f"duplicate skill {skill.name!r}: keeping {existing.source}, skipping {source.source}"
                )
                continue
            chosen[skill.name] = skill

    return list(chosen.values()), warnings


def discover_all(root: Path) -> tuple[list[Skill], list[str]]:
    return discover_sources(load_sources(root))


def excluded_skill_targets(sources: list[Source]) -> dict[str, frozenset[Path]]:
    targets: dict[str, set[Path]] = {}
    for source in sources:
        excluded_paths: dict[str, set[Path]] = {
            name: set() for name in source.exclude
        }
        if source.recursive and source.root.is_dir():
            for skill_file in source.root.rglob("SKILL.md"):
                if skill_file.parent.name in excluded_paths:
                    excluded_paths[skill_file.parent.name].add(
                        skill_file.parent.resolve()
                    )
        for name, paths in excluded_paths.items():
            if not paths and not source.recursive:
                paths.add((source.root / name).resolve())
            if paths:
                targets.setdefault(name, set()).update(paths)
    return {name: frozenset(paths) for name, paths in targets.items()}


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

    frontmatter_lines = text[4:end].splitlines()
    for index, raw_line in enumerate(frontmatter_lines):
        line = raw_line.strip()
        if line.startswith("description:"):
            description = line.split(":", 1)[1].strip()
            if description in {">", ">-", ">+", "|", "|-", "|+"}:
                description_lines: list[str] = []
                for continuation in frontmatter_lines[index + 1 :]:
                    if continuation and not continuation[0].isspace():
                        break
                    if continuation.strip():
                        description_lines.append(continuation.strip())
                return " ".join(" ".join(description_lines).split())
            if (
                len(description) >= 2
                and description[0] == description[-1]
                and description[0] in {"\"", "'"}
            ):
                description = description[1:-1]
            return " ".join(description.split())
    return ""


def is_manual_only(skill: Skill) -> bool:
    lines = (skill.path / "SKILL.md").read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines or lines[0] != "---":
        return False
    for line in lines[1:]:
        if line == "---":
            break
        if line.startswith("disable-model-invocation:"):
            value = line.split(":", 1)[1].split("#", 1)[0].strip()
            return value.lower() == "true"
    return False


def escape_markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_skill_catalog(skills: list[Skill]) -> str:
    grouped: dict[str, list[Skill]] = {}
    for skill in skills:
        grouped.setdefault(skill.source, []).append(skill)

    lines = [
        "# 已安装 Skills 清单",
        "",
        "> 此文件由 `python3 scripts/install-skills.py --write-catalog` 自动生成，请勿手工维护。",
        "",
        f"当前默认安装集共 **{len(skills)}** 个 Skills。",
        "",
        "## 来源统计",
        "",
        "| 来源 | 数量 |",
        "| --- | ---: |",
    ]
    for source, source_skills in grouped.items():
        lines.append(f"| {escape_markdown_cell(source)} | {len(source_skills)} |")

    lines.extend(["", "## Skills", ""])
    for source, source_skills in grouped.items():
        lines.extend(
            [
                f"### {source}",
                "",
                "| Skill | 调用方式（Pi） | Description |",
                "| --- | --- | --- |",
            ]
        )
        for skill in sorted(source_skills, key=lambda item: item.name):
            description = escape_markdown_cell(read_description(skill))
            invocation = (
                f"**仅手动调用**：`/skill:{skill.name}`"
                if is_manual_only(skill) else "自动或手动"
            )
            lines.append(f"| `{skill.name}` | {invocation} | {description} |")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def print_skill_list(skills: list[Skill], warnings: list[str]) -> None:
    for warning in warnings:
        print(f"[WARN] {warning}")

    for skill in sorted(skills, key=lambda item: item.name):
        description = read_description(skill)
        if description:
            print(f"{skill.name}\t{skill.source}\t{description}")
        else:
            print(f"{skill.name}\t{skill.source}")


def prune_stale_managed_links(
    dest_dir: Path,
    prunable: dict[str, frozenset[Path]],
    dry_run: bool,
) -> list[str]:
    if not dest_dir.is_dir():
        return []

    messages: list[str] = []
    for destination in sorted(dest_dir.iterdir()):
        expected_targets = prunable.get(destination.name)
        if not destination.is_symlink() or not expected_targets:
            continue
        if destination.resolve(strict=False) not in expected_targets:
            continue

        if dry_run:
            messages.append(f"[DRY] prune {destination.name}")
        else:
            destination.unlink()
            messages.append(f"[PRUNE] {destination.name}")
    return messages


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
        description="Install local and linked upstream skills into a supported agent harness.",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        help="Install into one explicit directory instead of the detected harnesses.",
    )
    parser.add_argument(
        "--agent",
        help="Comma-separated harnesses to install into: codex, pi, claude. "
        "Defaults to pi.",
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
    output_mode = parser.add_mutually_exclusive_group()
    output_mode.add_argument(
        "--list",
        action="store_true",
        help="List discovered skills with source and frontmatter description.",
    )
    output_mode.add_argument(
        "--write-catalog",
        action="store_true",
        help="Regenerate SKILLS.md from the authoritative install set.",
    )
    output_mode.add_argument(
        "--check-catalog",
        action="store_true",
        help="Fail when SKILLS.md does not match the authoritative install set.",
    )
    args = parser.parse_args()
    if args.dest and args.agent:
        print("Use either --dest or --agent, not both.", file=sys.stderr)
        return 1

    root = repo_root()
    try:
        sources = load_sources(root)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    unusable_sources = [
        source
        for source in sources
        # An initialized source can legitimately have every skill excluded.
        if not source.root.is_dir()
        or not discover_skills(replace(source, exclude=frozenset()))
    ]
    if unusable_sources:
        for source in unusable_sources:
            print(f"Unusable skill source {source.id}: {source.root}", file=sys.stderr)
        print("Run: git submodule update --init --recursive", file=sys.stderr)
        return 1

    skills, warnings = discover_sources(sources)
    if not skills:
        print("No skills found. Did you initialize submodules?", file=sys.stderr)
        print("Run: git submodule update --init --recursive", file=sys.stderr)
        return 1

    if args.list:
        print_skill_list(skills, warnings)
        return 0

    catalog_path = root / "SKILLS.md"
    if args.write_catalog:
        catalog_path.write_text(render_skill_catalog(skills), encoding="utf-8")
        print(f"[OK] wrote {catalog_path}")
        return 0
    if args.check_catalog:
        expected = render_skill_catalog(skills)
        actual = catalog_path.read_text(encoding="utf-8") if catalog_path.exists() else ""
        if actual != expected:
            print(
                "SKILLS.md is stale; run: python3 scripts/install-skills.py --write-catalog",
                file=sys.stderr,
            )
            return 1
        print("[OK] SKILLS.md matches the authoritative install set")
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

    sorted_skills = sorted(skills, key=lambda item: item.name)
    prunable = excluded_skill_targets(sources)
    for target in targets:
        dest_dir = target.skills_dir
        print()
        print(f"=== {target.id} -> {dest_dir}")
        for message in prune_stale_managed_links(
            dest_dir,
            prunable,
            args.dry_run,
        ):
            print(message)
        for skill in sorted_skills:
            print(install_skill(skill, dest_dir, args.mode, args.force, args.dry_run))

    print()
    for target in targets:
        print(f"{target.restart_hint} to pick up installed or updated skills in {target.skills_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
