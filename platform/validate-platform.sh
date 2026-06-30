#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

failures=0
check() {
  local label="$1"
  shift
  if "$@"; then
    echo "[ok] ${label}"
  else
    echo "[fail] ${label}" >&2
    failures=$((failures + 1))
  fi
}

echo "=== LAWIM_V2 developer platform validation ==="

check "runtime detection" "${ROOT}/platform/detect-runtime.sh" >/dev/null
check "infra check-env" "${ROOT}/infra/check-env.sh"
check "platform venv" test -x "${ROOT}/.venv-platform/bin/python"

VENV="${ROOT}/.venv-platform/bin"
export PYTHONPATH="${ROOT}/code:${ROOT}/tests"

if [[ -x "${VENV}/python" ]]; then
  check "postgres container" "${ROOT}/platform/wait-postgres.sh"
  check "postgres integration tests" "${ROOT}/platform/run-postgres-tests.sh"
else
  echo "[skip] postgres tests — run platform/setup-dev-venv.sh and platform/start-postgres.sh" >&2
fi

check "sqlite test suite" "${ROOT}/scripts/run-tests.sh"
check "validate-install" "${ROOT}/scripts/validate-install.sh"
check "compose config (dev)" "${ROOT}/platform/compose.sh" -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml config >/dev/null
check "compose config (postgres)" "${ROOT}/platform/compose.sh" -f compose/docker-compose.base.yml -f compose/docker-compose.postgres.yml config >/dev/null

if ((failures)); then
  echo "PLATFORM VALIDATION FAILED (${failures} checks)" >&2
  exit 1
fi

echo "PLATFORM VALIDATION OK"
