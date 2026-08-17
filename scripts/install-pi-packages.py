#!/usr/bin/env python3
"""Install the Pi packages declared by this repository."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


MANAGED_CONFIG_DIRECTORIES = {"extensions"}
PROTECTED_SETTINGS_KEYS = {"lastChangelogVersion", "packages", "skills"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def normalize_source(source: str, base_dir: Path) -> str:
    path = Path(source).expanduser()
    if path.is_absolute() or source.startswith(("./", "../", "~/")):
        if not path.is_absolute():
            path = base_dir / path
        return str(path.resolve())
    return source


def resolve_source(source: str) -> str:
    return normalize_source(source, repo_root())


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
            result.add(normalize_source(entry, settings_path.parent))
        elif isinstance(entry, dict) and isinstance(entry.get("source"), str):
            result.add(normalize_source(entry["source"], settings_path.parent))
    return result


def npm_package_is_current(source: str, home: Path) -> bool:
    spec = source.removeprefix("npm:")
    package_name, separator, expected_version = spec.rpartition("@")
    if not separator or not package_name or not expected_version:
        return False

    package_json = home / "npm/node_modules" / package_name / "package.json"
    try:
        metadata = json.loads(package_json.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return False
    return (
        metadata.get("name") == package_name
        and metadata.get("version") == expected_version
    )


def git_package_is_current(source: str, home: Path) -> bool:
    repository_url, separator, expected_revision = source.rpartition("@")
    parsed = urlparse(repository_url)
    if not separator or parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False

    repository_path = parsed.path.strip("/")
    if repository_path.endswith(".git"):
        repository_path = repository_path[:-4]
    checkout = home / "git" / parsed.hostname / repository_path
    if not (checkout / ".git").exists():
        return False

    head = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if head.returncode != 0:
        return False
    head_revision = head.stdout.strip()
    if head_revision == expected_revision:
        return True

    resolved = subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "rev-parse",
            "--verify",
            f"{expected_revision}^{{commit}}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return resolved.returncode == 0 and resolved.stdout.strip() == head_revision


def package_is_current(source: str, home: Path) -> bool:
    if source.startswith("npm:"):
        return npm_package_is_current(source, home)
    if source.startswith(("http://", "https://")):
        return git_package_is_current(source, home)
    path = Path(source)
    return path.is_absolute() and path.exists()


def merge_json_patch(current: object, patch: object) -> object:
    """Apply RFC 7396-style merge-patch semantics to JSON-compatible values."""
    if not isinstance(patch, dict):
        return patch

    result = dict(current) if isinstance(current, dict) else {}
    for key, value in patch.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = merge_json_patch(result.get(key), value)
    return result


def load_json_object(path: Path, missing_ok: bool = False) -> dict[str, object]:
    if missing_ok and not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Missing JSON config: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"JSON config must contain an object: {path}")
    return value


def sync_settings_patch(source: Path, destination: Path, dry_run: bool) -> None:
    patch = load_json_object(source)
    protected = sorted(PROTECTED_SETTINGS_KEYS.intersection(patch))
    if protected:
        joined = ", ".join(protected)
        raise ValueError(f"settings.patch.json contains protected Pi setting(s): {joined}")

    current = load_json_object(destination, missing_ok=True)
    merged = merge_json_patch(current, patch)
    if merged == current:
        print("[OK] Pi config settings.json is up to date")
        return
    if dry_run:
        print("[DRY] merge Pi config settings.patch.json -> settings.json")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(destination.stat().st_mode) if destination.exists() else 0o600
    temporary = destination.with_name(f".{destination.name}.tmp")
    temporary.write_text(
        f"{json.dumps(merged, indent=2, ensure_ascii=False)}\n",
        encoding="utf-8",
    )
    temporary.chmod(mode)
    temporary.replace(destination)
    print("[SYNC] Pi config settings.patch.json -> settings.json")


def sync_config_tree(config_root: Path, home: Path, dry_run: bool) -> None:
    if not config_root.is_dir():
        return

    settings_patch = config_root / "settings.patch.json"
    if settings_patch.is_file():
        sync_settings_patch(settings_patch, home / "settings.json", dry_run)

    for source in sorted(path for path in config_root.rglob("*") if path.is_file()):
        if source == settings_patch:
            continue
        relative_path = source.relative_to(config_root)
        if relative_path.parts[0] not in MANAGED_CONFIG_DIRECTORIES:
            raise ValueError(f"Refusing to sync unmanaged Pi state: {relative_path}")
        destination = home / relative_path
        if destination.is_file() and destination.read_bytes() == source.read_bytes():
            print(f"[OK] Pi config {relative_path} is up to date")
            continue
        if dry_run:
            print(f"[DRY] sync Pi config {relative_path}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        print(f"[SYNC] Pi config {relative_path}")


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

    sources = [(package_id, resolve_source(source)) for package_id, source in sources]

    requested = {
        name.strip() for name in (args.agent or "").split(",") if name.strip()
    }
    if args.dest or (requested and "pi" not in requested):
        print("[SKIP] Pi packages were not requested")
        return 0

    pi = shutil.which("pi")
    home = pi_home()
    if not args.dry_run and (not pi or (not requested and not home.is_dir())):
        print("[SKIP] Pi is not installed or detected")
        return 0

    settings_path = home / "settings.json"
    installed = installed_sources(settings_path)
    for package_id, source in sources:
        if source in installed and package_is_current(source, home):
            print(f"[OK] {package_id} already installed from {source}")
            continue
        if args.dry_run:
            print(f"[DRY] pi install {source}")
            continue
        print(f"[INSTALL] {package_id} from {source}")
        assert pi is not None
        subprocess.run([pi, "install", source], check=True)
        installed = installed_sources(settings_path)
        if source not in installed or not package_is_current(source, home):
            print(f"Pi did not materialize expected package source: {source}", file=sys.stderr)
            return 1

    try:
        sync_config_tree(repo_root() / "pi-config", home, args.dry_run)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
