#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

git submodule update --init --recursive
python3 scripts/install-skills.py "$@"
python3 scripts/install-pi-packages.py "$@"
