#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -f "${ROOT}/.env.platform" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT}/.env.platform"
elif [[ -f "${ROOT}/platform/platform.env.example" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT}/platform/platform.env.example"
fi

PORT="${LAWIM_POSTGRES_PORT:-5433}"
USER="${LAWIM_POSTGRES_USER:-lawim}"
DB="${LAWIM_POSTGRES_DB:-lawim_v2}"
export PGPASSWORD="${LAWIM_POSTGRES_PASSWORD:-lawim}"

TRIES="${LAWIM_POSTGRES_WAIT_TRIES:-30}"
SLEEP="${LAWIM_POSTGRES_WAIT_SLEEP:-1}"

for ((i = 1; i <= TRIES; i++)); do
  if command -v pg_isready >/dev/null 2>&1; then
    if pg_isready -h 127.0.0.1 -p "${PORT}" -U "${USER}" -d "${DB}" >/dev/null 2>&1; then
      echo "PostgreSQL ready on 127.0.0.1:${PORT}"
      exit 0
    fi
  elif command -v psql >/dev/null 2>&1; then
    if psql -h 127.0.0.1 -p "${PORT}" -U "${USER}" -d "${DB}" -c "SELECT 1" >/dev/null 2>&1; then
      echo "PostgreSQL ready on 127.0.0.1:${PORT}"
      exit 0
    fi
  else
    if podman ps --format '{{.Names}} {{.Status}}' 2>/dev/null | grep -q compose_postgres; then
      echo "PostgreSQL container running (pg_isready/psql not installed — assuming ready)"
      exit 0
    fi
  fi
  sleep "${SLEEP}"
done

echo "Timed out waiting for PostgreSQL on 127.0.0.1:${PORT}" >&2
exit 1
