#!/usr/bin/env python3
"""Validate local Codex skills in this repository."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, "missing or invalid YAML frontmatter"

    values: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            return {}, f"invalid frontmatter line: {raw_line}"
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if not key:
            return {}, f"invalid frontmatter line: {raw_line}"
        values[key] = value
    return values, None


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return ["missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    frontmatter, error = parse_frontmatter(text)
    if error:
        return [error]

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()

    if not name:
        errors.append("frontmatter is missing name")
    elif not NAME_RE.fullmatch(name):
        errors.append("name must be lowercase hyphen-case")
    elif name != skill_dir.name:
        errors.append(f"name {name!r} does not match folder {skill_dir.name!r}")

    if not description:
        errors.append("frontmatter is missing description")
    elif len(description) > 1024:
        errors.append("description must be 1024 characters or fewer")

    if "TODO" in text or "[TODO" in text:
        errors.append("contains unresolved TODO placeholder")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local skills.")
    parser.add_argument(
        "skills_dir",
        nargs="?",
        default="skills",
        help="Directory containing skill folders. Defaults to ./skills.",
    )
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    if not skills_dir.exists():
        print(f"Skill directory not found: {skills_dir}", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not skill_dirs:
        print(f"No skill folders found in {skills_dir}", file=sys.stderr)
        return 1

    failed = False
    for skill_dir in skill_dirs:
        errors = validate_skill(skill_dir)
        if errors:
            failed = True
            print(f"[FAIL] {skill_dir}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"[OK] {skill_dir}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
