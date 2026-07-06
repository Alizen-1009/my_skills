#!/usr/bin/env python3
"""Add an open source skill repository as a git submodule source."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest(path: Path) -> dict:
    if not path.exists():
        return {"sources": []}
    return json.loads(path.read_text(encoding="utf-8"))


def write_manifest(path: Path, manifest: dict) -> None:
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add a git repository to skill-sources.json and .gitmodules.",
    )
    parser.add_argument("source_id", help="Stable source id, e.g. obra-superpowers")
    parser.add_argument("repo", help="Git repository URL")
    parser.add_argument(
        "--path",
        help="Submodule path. Defaults to external/<source-id>.",
    )
    parser.add_argument(
        "--skills-path",
        default="skills",
        help="Path inside the repo that contains skill folders, or a single skill folder. Defaults to skills.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Discover SKILL.md files recursively under --skills-path.",
    )
    parser.add_argument(
        "--ref",
        help="Optional branch, tag, or commit to check out inside the submodule.",
    )
    args = parser.parse_args()

    source_id = args.source_id.strip()
    if not ID_RE.fullmatch(source_id):
        print("source_id must be lowercase hyphen-case", file=sys.stderr)
        return 1

    root = repo_root()
    manifest_path = root / "skill-sources.json"
    manifest = load_manifest(manifest_path)
    sources = manifest.setdefault("sources", [])
    if not isinstance(sources, list):
        print("skill-sources.json must contain a sources array", file=sys.stderr)
        return 1

    if any(source.get("id") == source_id for source in sources if isinstance(source, dict)):
        print(f"source already exists in skill-sources.json: {source_id}", file=sys.stderr)
        return 1

    submodule_path = args.path or f"external/{source_id}"
    submodule_dir = root / submodule_path

    if not submodule_dir.exists():
        run(["git", "submodule", "add", args.repo, submodule_path], cwd=root)
    else:
        print(f"Using existing directory: {submodule_path}")

    if args.ref:
        run(["git", "checkout", args.ref], cwd=submodule_dir)

    sources.append(
        {
            "id": source_id,
            "kind": "git-submodule",
            "repo": args.repo,
            "path": submodule_path,
            "skills_path": args.skills_path,
            "recursive": bool(args.recursive),
            "enabled": True,
        }
    )
    write_manifest(manifest_path, manifest)

    print(f"Added source: {source_id}")
    print("Run ./scripts/bootstrap.sh --dry-run to verify discovered skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
