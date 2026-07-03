#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONPATH="${ROOT}/code:${ROOT}/tests${PYTHONPATH:+:${PYTHONPATH}}"
export LAWIM_TEST_MODE=1

if command -v node >/dev/null 2>&1; then
  echo "Checking frontend JavaScript syntax..."
  node --check "${ROOT}/code/lawim_v2/static/app.js"
fi

echo "Running LAWIM_V2 unit tests..."
python3 -m unittest discover -s tests -v "$@"

echo "Validating Prisma manifest..."
python3 "${ROOT}/scripts/validate_prisma_manifest.py"

echo "Running runtime smoke test..."
python3 "${ROOT}/scripts/smoke_runtime.py"
