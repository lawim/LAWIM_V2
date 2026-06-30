#!/usr/bin/env bash
# Detect container runtime and compose command for LAWIM_V2 developer platform.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

runtime="none"
compose_cmd=""
socket_ok="false"
socket_path=""
notes=()

if command -v podman >/dev/null 2>&1; then
  if podman info >/dev/null 2>&1; then
    runtime="podman"
  fi
fi

if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    if [[ "${runtime}" == "podman" ]] && docker info 2>&1 | grep -qi "Emulate Docker CLI using podman"; then
      notes+=("docker CLI is a Podman emulation shim")
    elif [[ "${runtime}" == "none" ]]; then
      runtime="docker"
    fi
  fi
fi

if [[ -S /var/run/docker.sock ]]; then
  socket_path="/var/run/docker.sock"
  if [[ -r /var/run/docker.sock && -w /var/run/docker.sock ]]; then
    socket_ok="true"
  else
    notes+=("/var/run/docker.sock exists but is not readable/writable by $(id -un)")
  fi
elif [[ -n "${XDG_RUNTIME_DIR:-}" && -S "${XDG_RUNTIME_DIR}/podman/podman.sock" ]]; then
  socket_path="${XDG_RUNTIME_DIR}/podman/podman.sock"
  socket_ok="true"
fi

# Prefer podman-compose when docker compose delegates to docker-compose v1 (socket required).
if [[ "${runtime}" == "podman" ]] && command -v podman-compose >/dev/null 2>&1; then
  compose_cmd="podman-compose"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  if docker compose version 2>&1 | grep -qi "docker-compose version 1"; then
    if command -v podman-compose >/dev/null 2>&1 && [[ "${runtime}" == "podman" ]]; then
      compose_cmd="podman-compose"
      notes+=("docker compose v1 shim detected — using podman-compose instead")
    else
      compose_cmd="docker compose"
      if [[ "${socket_ok}" != "true" ]]; then
        notes+=("docker compose v1 requires a working /var/run/docker.sock")
      fi
    fi
  else
    compose_cmd="docker compose"
  fi
elif command -v podman-compose >/dev/null 2>&1; then
  compose_cmd="podman-compose"
elif command -v docker-compose >/dev/null 2>&1; then
  compose_cmd="docker-compose"
fi

cat <<EOF
LAWIM_V2 runtime detection
  repository: ${ROOT}
  runtime:    ${runtime}
  compose:    ${compose_cmd:-<none>}
  socket:     ${socket_path:-<none>} (ok=${socket_ok})
EOF

if ((${#notes[@]})); then
  echo "  notes:"
  for note in "${notes[@]}"; do
    echo "    - ${note}"
  done
fi

if [[ "${runtime}" == "none" ]]; then
  exit 1
fi

if [[ -z "${compose_cmd}" ]]; then
  exit 2
fi
