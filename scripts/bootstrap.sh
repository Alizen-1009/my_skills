#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if printf '%s\n' "$@" | grep -qx -- '--dry-run'; then
  echo "[DRY] git submodule update --init --recursive"
else
  git submodule update --init --recursive
fi
python3 scripts/install-pi.py "$@"
python3 scripts/install-skills.py "$@"
python3 scripts/install-pi-packages.py "$@"
