#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

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

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "[fail] missing command: $1" >&2
    exit 1
  fi
}

require_cmd python3

PYTHON_VERSION="$(python3 - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)"
case "${PYTHON_VERSION}" in
  3.12|3.13)
    echo "[ok] python ${PYTHON_VERSION}"
    ;;
  *)
    echo "[warn] python ${PYTHON_VERSION} — LAWIM_V2 targets Python 3.12+" >&2
    ;;
esac

check "repository root" test -f "${ROOT}/code/lawim_v2/server.py"
check "compose base" test -f "${ROOT}/compose/docker-compose.base.yml"
check "env example" test -f "${ROOT}/env/development/.env.example"
check "data/runtime writable" mkdir -p "${ROOT}/data/runtime" && test -w "${ROOT}/data/runtime"

if command -v docker >/dev/null 2>&1; then
  check "docker available" true
else
  echo "[warn] docker not found — compose stacks optional" >&2
fi

if command -v node >/dev/null 2>&1; then
  check "node available" true
else
  echo "[warn] node not found — JS syntax check skipped in run-tests.sh" >&2
fi

if python3 -c "import pg8000" 2>/dev/null; then
  check "pg8000 installed" true
else
  echo "[warn] pg8000 not installed — PostgreSQL runtime optional (pip install -r requirements-postgresql.txt)" >&2
fi

exit "${failures}"
