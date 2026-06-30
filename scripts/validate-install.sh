#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== LAWIM_V2 install validation ==="

"${ROOT}/infra/check-env.sh"

export PYTHONPATH="${ROOT}/code:${ROOT}/tests${PYTHONPATH:+:${PYTHONPATH}}"

echo "Compiling Python sources..."
python3 -m compileall code tests scripts >/dev/null

echo "Running unit tests..."
python3 -m unittest discover -s tests -q

echo "Validating Prisma / schema contract..."
python3 "${ROOT}/scripts/validate_prisma_manifest.py"

echo "Running runtime smoke..."
python3 "${ROOT}/scripts/smoke_runtime.py"

COMPOSE="${COMPOSE:-docker compose}"
validate_compose() {
  local base="$1"
  local overlay="$2"
  ${COMPOSE} -f "${ROOT}/${base}" -f "${ROOT}/${overlay}" config >/dev/null
}

if command -v docker >/dev/null 2>&1; then
  echo "Validating Compose stacks..."
  validate_compose compose/docker-compose.base.yml compose/docker-compose.dev.yml
  validate_compose compose/docker-compose.base.yml compose/docker-compose.postgres.yml
  validate_compose docker/compose/docker-compose.base.yml docker/compose/docker-compose.development.yml
  validate_compose docker/compose/docker-compose.base.yml docker/compose/docker-compose.postgres.yml
else
  echo "[warn] docker not available — skipping compose validation"
fi

if command -v node >/dev/null 2>&1; then
  node --check "${ROOT}/code/lawim_v2/static/app.js"
fi

echo "Validating pip packaging..."
"${ROOT}/scripts/validate-packaging.sh"

echo "=== INSTALL VALIDATION OK ==="
