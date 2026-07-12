#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if [[ -f "${ROOT}/.env.platform" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT}/.env.platform"
elif [[ -f "${ROOT}/platform/platform.env.example" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT}/platform/platform.env.example"
fi

VENV="${LAWIM_PLATFORM_VENV:-.venv-platform}"
PYTHON="${VENV}/bin/python"

if [[ ! -x "${PYTHON}" ]]; then
  echo "Platform venv missing — run platform/setup-dev-venv.sh first" >&2
  exit 1
fi

if ! "${ROOT}/platform/wait-postgres.sh"; then
  echo "PostgreSQL not available — run platform/start-postgres.sh" >&2
  exit 1
fi

export PYTHONPATH="${ROOT}/code:${ROOT}/tests${PYTHONPATH:+:${PYTHONPATH}}"
export LAWIM_TEST_POSTGRES_URL="${LAWIM_TEST_POSTGRES_URL:-postgresql://lawim:lawim@127.0.0.1:${LAWIM_POSTGRES_PORT:-5433}/lawim_v2}"
export LAWIM_TEST_MODE=1

echo "Running PostgreSQL integration tests (${LAWIM_TEST_POSTGRES_URL})..."
"${PYTHON}" -m unittest \
  tests.test_productization.PostgreSQLIntegrationTest \
  tests.test_rc_postgresql \
  tests.test_financial_core.PostgreSQLFinancialCoreIntegrationTests \
  -v
"${PYTHON}" "${ROOT}/scripts/smoke_postgres.py"
