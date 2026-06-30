#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONPATH="${ROOT}/code:${ROOT}/tests${PYTHONPATH:+:${PYTHONPATH}}"

echo "Running LAWIM_V2 unit tests..."
python3 -m unittest discover -s tests -v "$@"

echo "Running runtime smoke test..."
python3 "${ROOT}/scripts/smoke_runtime.py"
