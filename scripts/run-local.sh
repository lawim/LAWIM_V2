#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONPATH="${ROOT}/code${PYTHONPATH:+:${PYTHONPATH}}"
export APP_ENV="${APP_ENV:-development}"
export STACK_PROFILE="${STACK_PROFILE:-development}"
export LAWIM_DB_PATH="${LAWIM_DB_PATH:-${ROOT}/data/runtime/lawim.sqlite3}"
export LAWIM_MEDIA_STORAGE_PATH="${LAWIM_MEDIA_STORAGE_PATH:-${ROOT}/data/runtime/media}"
export LAWIM_HOST="${LAWIM_HOST:-127.0.0.1}"
export LAWIM_PORT="${LAWIM_PORT:-3000}"

mkdir -p "$(dirname "${LAWIM_DB_PATH}")" "${LAWIM_MEDIA_STORAGE_PATH}"

echo "Starting LAWIM_V2 on http://${LAWIM_HOST}:${LAWIM_PORT}"
echo "Database: ${LAWIM_DB_PATH}"
exec python3 -m lawim_v2 --host "${LAWIM_HOST}" --port "${LAWIM_PORT}" --db "${LAWIM_DB_PATH}" "$@"
