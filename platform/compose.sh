#!/usr/bin/env bash
# Unified compose wrapper — auto-selects podman-compose or docker compose.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if [[ -f "${ROOT}/.env.platform" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT}/.env.platform"
fi

# shellcheck disable=SC1091
source "${ROOT}/platform/runtime-env.sh"
lawim_prepare_podman_runtime

COMPOSE="${LAWIM_COMPOSE:-}"
if [[ -z "${COMPOSE}" ]]; then
  if command -v podman-compose >/dev/null 2>&1; then
    docker_compose_version=""
    if command -v docker >/dev/null 2>&1; then
      docker_compose_version="$(docker compose version 2>&1 || true)"
    fi
    if [[ -n "${docker_compose_version}" ]] && grep -qi "Emulate Docker CLI using podman" <<<"${docker_compose_version}"; then
      COMPOSE="podman-compose"
    elif [[ -n "${docker_compose_version}" ]] && grep -qi "compose version v2" <<<"${docker_compose_version}"; then
      COMPOSE="docker compose"
    elif command -v podman >/dev/null 2>&1 && podman info >/dev/null 2>&1; then
      COMPOSE="podman-compose"
    elif command -v docker >/dev/null 2>&1; then
      COMPOSE="docker compose"
    else
      echo "No compose command available. Run platform/detect-runtime.sh" >&2
      exit 1
    fi
  elif command -v docker >/dev/null 2>&1; then
    COMPOSE="docker compose"
  else
    echo "No compose command available. Run platform/detect-runtime.sh" >&2
    exit 1
  fi
fi

if [[ "${COMPOSE}" == "podman-compose" ]]; then
  lawim_prepare_podman_runtime
fi

exec ${COMPOSE} "$@"
