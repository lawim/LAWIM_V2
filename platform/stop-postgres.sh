#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if [[ -f "${ROOT}/.env.platform" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT}/.env.platform"
fi

BASE="${ROOT}/compose/docker-compose.base.yml"
PG="${ROOT}/compose/docker-compose.postgres.yml"

echo "Stopping PostgreSQL dev container..."
"${ROOT}/platform/compose.sh" -f "${BASE}" -f "${PG}" stop postgres 2>/dev/null || true
"${ROOT}/platform/compose.sh" -f "${BASE}" -f "${PG}" rm -f postgres 2>/dev/null || true
