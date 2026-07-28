#!/usr/bin/env python3
"""Install the Pi packages declared by this repository."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def pi_home() -> Path:
    override = os.environ.get("PI_CODING_AGENT_DIR")
    return Path(override).expanduser() if override else Path.home() / ".pi/agent"


def load_sources() -> list[tuple[str, str]]:
    manifest_path = repo_root() / "pi-packages.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"Missing Pi package manifest: {manifest_path}", file=sys.stderr)
        return []
    except json.JSONDecodeError as error:
        print(f"Invalid JSON in {manifest_path}: {error}", file=sys.stderr)
        return []

    entries = manifest.get("packages")
    if not isinstance(entries, list):
        print("pi-packages.json must contain a packages array", file=sys.stderr)
        return []

    sources: list[tuple[str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("enabled", True):
            continue
        package_id = str(entry.get("id", "")).strip()
        source = str(entry.get("source", "")).strip()
        if not package_id or not source:
            print(f"Skipping invalid Pi package entry: {entry}", file=sys.stderr)
            continue
        sources.append((package_id, source))
    return sources


def installed_sources(settings_path: Path) -> set[str]:
    if not settings_path.exists():
        return set()
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"Invalid JSON in {settings_path}: {error}", file=sys.stderr)
        return set()

    result: set[str] = set()
    for entry in settings.get("packages", []):
        if isinstance(entry, str):
            result.add(entry)
        elif isinstance(entry, dict) and isinstance(entry.get("source"), str):
            result.add(entry["source"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install version-controlled Pi package dependencies.",
        add_help=True,
    )
    parser.add_argument("--agent", help="Comma-separated harness targets from bootstrap.sh")
    parser.add_argument("--dest", help="Explicit skill destination; skips Pi package installation")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list", action="store_true")
    args, _unknown = parser.parse_known_args()

    sources = load_sources()
    if not sources:
        return 1

    if args.list:
        for package_id, source in sources:
            print(f"{package_id}\t{source}")
        return 0

    requested = {
        name.strip() for name in (args.agent or "").split(",") if name.strip()
    }
    if args.dest or (requested and "pi" not in requested):
        print("[SKIP] Pi packages were not requested")
        return 0

    pi = shutil.which("pi")
    home = pi_home()
    if not pi or (not requested and not home.is_dir()):
        print("[SKIP] Pi is not installed or detected")
        return 0

    settings_path = home / "settings.json"
    installed = installed_sources(settings_path)
    for package_id, source in sources:
        if source in installed:
            print(f"[OK] {package_id} already installed from {source}")
            continue
        if args.dry_run:
            print(f"[DRY] pi install {source}")
            continue
        print(f"[INSTALL] {package_id} from {source}")
        subprocess.run([pi, "install", source], check=True)
        installed = installed_sources(settings_path)
        if source not in installed:
            print(f"Pi did not record expected package source: {source}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
