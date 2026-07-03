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
VOLUME="${LAWIM_VOLUME_POSTGRES_NAME:-lawim_v2_postgres}"
CONTAINER_NAME="${LAWIM_POSTGRES_CONTAINER_NAME:-compose_postgres_1}"

if command -v podman >/dev/null 2>&1; then
  RUNTIME="podman"
elif command -v docker >/dev/null 2>&1; then
  RUNTIME="docker"
else
  echo "No container runtime available. Run platform/detect-runtime.sh" >&2
  exit 1
fi

echo "Starting PostgreSQL dev container on port ${LAWIM_POSTGRES_PORT}..."
"${RUNTIME}" rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
"${RUNTIME}" run -d \
  --name "${CONTAINER_NAME}" \
  --network host \
  -e POSTGRES_DB="${LAWIM_POSTGRES_DB:-lawim_v2}" \
  -e POSTGRES_USER="${LAWIM_POSTGRES_USER:-lawim}" \
  -e POSTGRES_PASSWORD="${LAWIM_POSTGRES_PASSWORD:-lawim}" \
  -v "${VOLUME}:/var/lib/postgresql/data" \
  postgres:16-alpine \
  -c "port=${LAWIM_POSTGRES_PORT}" \
  "$@" >/dev/null

echo "Waiting for PostgreSQL..."
"${ROOT}/platform/wait-postgres.sh"

echo "LAWIM_TEST_POSTGRES_URL=${LAWIM_TEST_POSTGRES_URL:-postgresql://lawim:lawim@127.0.0.1:${LAWIM_POSTGRES_PORT}/lawim_v2}"
