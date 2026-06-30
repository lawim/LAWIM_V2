#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if [[ -f "${ROOT}/.env.platform" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT}/.env.platform"
elif [[ -f "${ROOT}/platform/platform.env.example" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT}/platform/platform.env.example"
fi

export LAWIM_POSTGRES_PORT="${LAWIM_POSTGRES_PORT:-5433}"
BASE="${ROOT}/compose/docker-compose.base.yml"
PG="${ROOT}/compose/docker-compose.postgres.yml"

echo "Starting PostgreSQL dev container on port ${LAWIM_POSTGRES_PORT}..."
LAWIM_POSTGRES_PORT="${LAWIM_POSTGRES_PORT}" "${ROOT}/platform/compose.sh" -f "${BASE}" -f "${PG}" up -d postgres "$@"

echo "Waiting for PostgreSQL..."
"${ROOT}/platform/wait-postgres.sh"

echo "LAWIM_TEST_POSTGRES_URL=${LAWIM_TEST_POSTGRES_URL:-postgresql://lawim:lawim@127.0.0.1:${LAWIM_POSTGRES_PORT}/lawim_v2}"
