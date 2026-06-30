#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VENV="${ROOT}/.packaging-venv"
rm -rf "${VENV}"
python3 -m venv "${VENV}"
# shellcheck disable=SC1091
source "${VENV}/bin/activate"

echo "Building editable install..."
python -m pip install --upgrade pip wheel >/dev/null
python -m pip install -e ".[postgresql]" >/dev/null

echo "Checking console entry point..."
python -m lawim_v2 --help >/dev/null
if command -v lawim-v2 >/dev/null 2>&1; then
  lawim-v2 --help >/dev/null
fi

echo "Running smoke from installed package..."
python "${ROOT}/scripts/smoke_runtime.py"

deactivate
rm -rf "${VENV}"

echo "PACKAGING VALIDATION OK"
