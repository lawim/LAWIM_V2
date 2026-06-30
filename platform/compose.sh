#!/usr/bin/env bash
# Unified compose wrapper — auto-selects podman-compose or docker compose.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if [[ -f "${ROOT}/.env.platform" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT}/.env.platform"
fi

COMPOSE="${LAWIM_COMPOSE:-}"
if [[ -z "${COMPOSE}" ]]; then
  if command -v podman-compose >/dev/null 2>&1 && podman info >/dev/null 2>&1; then
    if docker compose version 2>&1 | grep -qi "docker-compose version 1"; then
      COMPOSE="podman-compose"
    elif [[ -z "$(docker compose version 2>/dev/null | grep -i 'compose version v2')" ]]; then
      COMPOSE="podman-compose"
    else
      COMPOSE="docker compose"
    fi
  elif command -v docker >/dev/null 2>&1; then
    COMPOSE="docker compose"
  else
    echo "No compose command available. Run platform/detect-runtime.sh" >&2
    exit 1
  fi
fi

exec ${COMPOSE} "$@"
