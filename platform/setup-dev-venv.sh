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
PIP="${VENV}/bin/pip"

if [[ ! -d "${VENV}" ]]; then
  echo "Creating platform virtualenv at ${VENV}..."
  python3 -m venv "${VENV}"
fi

echo "Installing LAWIM_V2 + PostgreSQL driver into ${VENV}..."
"${PIP}" install -q --upgrade pip
"${PIP}" install -q -r "${ROOT}/requirements-postgresql.txt"
"${PIP}" install -q -e "${ROOT}"

echo "Platform venv ready: ${VENV}"
echo "Activate: source ${VENV}/bin/activate"
