#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

COMPOSE="${COMPOSE:-docker compose}"
BASE="${ROOT}/compose/docker-compose.base.yml"
OVERLAY="${ROOT}/compose/docker-compose.prod.yml"

export APP_ENV="${APP_ENV:-production}"
export STACK_PROFILE="${STACK_PROFILE:-production}"
export LAWIM_SEED_DEMO_DATA="${LAWIM_SEED_DEMO_DATA:-false}"

echo "Validating production compose configuration..."
${COMPOSE} -f "${BASE}" -f "${OVERLAY}" config >/dev/null

echo "Starting LAWIM_V2 production stack (seed demo disabled by default)..."
exec ${COMPOSE} -f "${BASE}" -f "${OVERLAY}" up --build "$@"
