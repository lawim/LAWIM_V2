#!/usr/bin/env bash
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

CONTAINER_NAME="${LAWIM_POSTGRES_CONTAINER_NAME:-compose_postgres_1}"
if command -v podman >/dev/null 2>&1; then
  RUNTIME="podman"
elif command -v docker >/dev/null 2>&1; then
  RUNTIME="docker"
else
  echo "No container runtime available. Run platform/detect-runtime.sh" >&2
  exit 1
fi

echo "Stopping PostgreSQL dev container..."
"${RUNTIME}" rm -f "${CONTAINER_NAME}" 2>/dev/null || true
