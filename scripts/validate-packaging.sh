#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VENV="${ROOT}/.packaging-venv"
rm -rf "${VENV}"
python3 -m venv --system-site-packages "${VENV}"
# shellcheck disable=SC1091
source "${VENV}/bin/activate"

PYTHON_VERSION="$(python3 - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)"
PLATFORM_SITE_PACKAGES="${ROOT}/.venv-platform/lib/python${PYTHON_VERSION}/site-packages"
if [[ -d "${PLATFORM_SITE_PACKAGES}" ]]; then
  export PYTHONPATH="${PLATFORM_SITE_PACKAGES}${PYTHONPATH:+:${PYTHONPATH}}"
fi

PACKAGING_TIMEOUT_SECONDS="${LAWIM_PACKAGING_TIMEOUT_SECONDS:-300}"
run_with_timeout() {
  if command -v timeout >/dev/null 2>&1; then
    timeout --kill-after=10s "${PACKAGING_TIMEOUT_SECONDS}" "$@"
  else
    "$@"
  fi
}

echo "Building editable install..."
run_with_timeout python -m pip install --upgrade --no-index pip wheel >/dev/null
run_with_timeout python -m pip install --no-index --no-build-isolation -e ".[postgresql]" >/dev/null

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
