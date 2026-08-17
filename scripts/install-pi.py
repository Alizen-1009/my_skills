#!/usr/bin/env python3
"""Install the repository-pinned Pi CLI version when Pi is targeted."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


PI_PACKAGE = "@earendil-works/pi-coding-agent"
VERSION_PATTERN = re.compile(r"(?<!\d)(\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)(?!\d)")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def should_manage_pi(agent: str | None, dest: str | None) -> bool:
    if dest:
        return False
    requested = {name.strip() for name in (agent or "").split(",") if name.strip()}
    return not requested or "pi" in requested


def load_pinned_version() -> str:
    manifest_path = repo_root() / "pi-packages.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Missing Pi package manifest: {manifest_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {manifest_path}: {error}") from error

    version = str(manifest.get("piVersion", "")).strip()
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError("pi-packages.json must contain a valid piVersion")
    return version


def get_pi_version(pi: str) -> str | None:
    result = subprocess.run(
        [pi, "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    match = VERSION_PATTERN.search(f"{result.stdout}\n{result.stderr}")
    return match.group(1) if result.returncode == 0 and match else None


def ensure_pi(version: str, dry_run: bool) -> int:
    pi = shutil.which("pi")
    current_version = get_pi_version(pi) if pi else None
    if current_version == version:
        print(f"[OK] Pi CLI {version} is installed")
        return 0

    npm = shutil.which("npm")
    if not npm:
        print(
            "npm is required to install Pi. Install Node.js 22.19 or newer and retry.",
            file=sys.stderr,
        )
        return 1

    package_spec = f"{PI_PACKAGE}@{version}"
    if dry_run:
        action = "install" if current_version is None else f"replace Pi {current_version} with"
        print(
            f"[DRY] npm install --global --ignore-scripts {package_spec} "
            f"({action} {version})"
        )
        return 0

    if current_version is None:
        print(f"[INSTALL] Pi CLI {version}")
    else:
        print(f"[INSTALL] Reconcile Pi CLI {current_version} -> {version}")
    subprocess.run(
        [npm, "install", "--global", "--ignore-scripts", package_spec],
        check=True,
    )

    installed_pi = shutil.which("pi")
    installed_version = get_pi_version(installed_pi) if installed_pi else None
    if installed_version != version:
        print(
            f"Pi installation did not produce expected version {version}; found {installed_version or 'none'}",
            file=sys.stderr,
        )
        return 1
    print(f"[OK] Pi CLI {version} installed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install the repository-pinned Pi CLI version.",
        add_help=True,
    )
    parser.add_argument("--agent", help="Comma-separated harness targets from bootstrap.sh")
    parser.add_argument("--dest", help="Explicit skill destination; skips Pi installation")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list", action="store_true")
    args, _unknown = parser.parse_known_args()

    if not should_manage_pi(args.agent, args.dest):
        print("[SKIP] Pi CLI was not requested")
        return 0

    try:
        version = load_pinned_version()
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if args.list:
        print(f"pi\tnpm:{PI_PACKAGE}@{version}")
        return 0
    return ensure_pi(version, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
