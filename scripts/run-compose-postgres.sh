#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

COMPOSE="${COMPOSE:-docker compose}"
BASE="${ROOT}/compose/docker-compose.base.yml"
DEV="${ROOT}/compose/docker-compose.dev.yml"
PG="${ROOT}/compose/docker-compose.postgres.yml"

export LAWIM_DB_DRIVER="${LAWIM_DB_DRIVER:-postgresql}"
export LAWIM_DB_FALLBACK="${LAWIM_DB_FALLBACK:-true}"

echo "Validating compose configuration (PostgreSQL optional overlay)..."
${COMPOSE} -f "${BASE}" -f "${DEV}" -f "${PG}" config >/dev/null

echo "Starting LAWIM_V2 with optional PostgreSQL (SQLite fallback enabled by default)..."
exec ${COMPOSE} -f "${BASE}" -f "${DEV}" -f "${PG}" up --build "$@"
