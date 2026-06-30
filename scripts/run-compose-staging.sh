#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

COMPOSE="${COMPOSE:-docker compose}"
BASE="${ROOT}/compose/docker-compose.base.yml"
OVERLAY="${ROOT}/compose/docker-compose.staging.yml"

echo "Validating staging compose configuration..."
${COMPOSE} -f "${BASE}" -f "${OVERLAY}" config >/dev/null

echo "Starting LAWIM_V2 staging stack..."
exec ${COMPOSE} -f "${BASE}" -f "${OVERLAY}" up --build "$@"
