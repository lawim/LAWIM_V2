#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

COMPOSE="${COMPOSE:-docker compose}"
BASE="${ROOT}/compose/docker-compose.base.yml"
DEV="${ROOT}/compose/docker-compose.dev.yml"

echo "Validating compose configuration..."
${COMPOSE} -f "${BASE}" -f "${DEV}" config >/dev/null

echo "Starting LAWIM_V2 development stack (SQLite default)..."
exec ${COMPOSE} -f "${BASE}" -f "${DEV}" up --build "$@"
