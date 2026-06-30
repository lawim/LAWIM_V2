#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "LAWIM_V2 install — preparing host environment"

"${ROOT}/infra/check-env.sh"

mkdir -p "${ROOT}/data/runtime/media"
chmod +x "${ROOT}/scripts/"*.sh "${ROOT}/infra/"*.sh 2>/dev/null || true

ENV_LOCAL="${ROOT}/.env.local"
ENV_EXAMPLE="${ROOT}/env/development/.env.example"
if [[ ! -f "${ENV_LOCAL}" && -f "${ENV_EXAMPLE}" ]]; then
  cp "${ENV_EXAMPLE}" "${ENV_LOCAL}"
  echo "Created ${ENV_LOCAL} from env/development/.env.example"
else
  echo "Env file present or example missing — skipping .env.local bootstrap"
fi

if [[ "${LAWIM_INSTALL_POSTGRES_DRIVER:-0}" == "1" ]]; then
  echo "Installing optional PostgreSQL driver..."
  python3 -m pip install --user -r "${ROOT}/requirements-postgresql.txt"
fi

export PYTHONPATH="${ROOT}/code${PYTHONPATH:+:${PYTHONPATH}}"

echo ""
echo "Install bootstrap complete."
echo "Next steps:"
echo "  ./scripts/run-local.sh          # native SQLite dev server"
echo "  ./scripts/run-tests.sh          # unit tests + validators"
echo "  ./scripts/validate-install.sh   # full reproducibility gate"
echo "  ./scripts/run-compose-dev.sh    # optional Docker stack"
