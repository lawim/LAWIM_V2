#!/usr/bin/env bash
# Shared runtime environment helpers for Podman-based local tooling.
set -euo pipefail

lawim_prepare_podman_runtime() {
  local runtime_dir="${XDG_RUNTIME_DIR:-}"

  if [[ -n "${runtime_dir}" && -d "${runtime_dir}" && -w "${runtime_dir}" ]]; then
    return 0
  fi

  runtime_dir="${LAWIM_PODMAN_RUNTIME_DIR:-/tmp/lawim_v2_podman_runtime}"
  export XDG_RUNTIME_DIR="${runtime_dir}"
  export TMPDIR="${runtime_dir}"

  mkdir -p "${runtime_dir}/podman" \
    "${runtime_dir}/containers" \
    "${runtime_dir}/libpod/tmp/events"
  chmod 700 "${runtime_dir}" 2>/dev/null || true
}
