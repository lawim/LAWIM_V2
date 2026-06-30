#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if [[ -f "${ROOT}/.env.platform" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT}/.env.platform"
fi

export LAWIM_POSTGRES_PORT="${LAWIM_POSTGRES_PORT:-5433}"
VOLUME="${LAWIM_VOLUME_POSTGRES_NAME:-lawim_v2_postgres}"

echo "Resetting PostgreSQL volume ${VOLUME}..."
"${ROOT}/platform/stop-postgres.sh" || true

if command -v podman >/dev/null 2>&1; then
  podman volume rm "${VOLUME}" 2>/dev/null || true
elif command -v docker >/dev/null 2>&1; then
  docker volume rm "${VOLUME}" 2>/dev/null || true
fi

"${ROOT}/platform/start-postgres.sh"
