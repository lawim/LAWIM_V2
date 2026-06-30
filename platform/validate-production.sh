#!/usr/bin/env bash
# Validate production-oriented environment variables without starting the app.
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

ENV_FILE="${LAWIM_PRODUCTION_ENV:-${ROOT}/env/production/.env.example}"
if [[ ! -f "${ENV_FILE}" ]]; then
  echo "[fail] production env file not found: ${ENV_FILE}" >&2
  exit 1
fi

# shellcheck disable=SC1090
set -a
source "${ENV_FILE}"
set +a

export APP_ENV="${APP_ENV:-production}"
export LAWIM_DB_DRIVER="${LAWIM_DB_DRIVER:-postgresql}"
export LAWIM_DB_FALLBACK="${LAWIM_DB_FALLBACK:-false}"
export LAWIM_PUBLIC_MEDIA="${LAWIM_PUBLIC_MEDIA:-false}"
export LAWIM_DATABASE_URL="${LAWIM_DATABASE_URL:-postgresql://lawim:lawim@postgres:5432/lawim_v2}"
export PUBLIC_BASE_URL="${PUBLIC_BASE_URL:-https://lawim.example}"

check "APP_ENV is production" test "${APP_ENV}" = "production"
check "PUBLIC_BASE_URL uses https" bash -c '[[ "${PUBLIC_BASE_URL}" == https://* ]]'
check "LAWIM_DB_FALLBACK disabled for PG" test "${LAWIM_DB_FALLBACK}" = "false"
check "LAWIM_PUBLIC_MEDIA disabled" test "${LAWIM_PUBLIC_MEDIA}" = "false"
check "SECRET_PROVIDER external" test "${SECRET_PROVIDER:-external}" = "external"

code_dir="${ROOT}/code"
export PYTHONPATH="${code_dir}${PYTHONPATH:+:${PYTHONPATH}}"
check "production AppConfig validates" python3 - <<'PY'
from pathlib import Path
import os
from lawim_v2.config import AppConfig

config = AppConfig(
    host="0.0.0.0",
    port=3000,
    db_path=Path("data/runtime/lawim.sqlite3"),
    db_driver=os.environ.get("LAWIM_DB_DRIVER", "postgresql"),
    database_url=os.environ.get("LAWIM_DATABASE_URL", "postgresql://lawim:lawim@postgres:5432/lawim_v2"),
    db_fallback=os.environ.get("LAWIM_DB_FALLBACK", "false").lower() == "true",
    app_env="production",
    stack_profile="production",
    log_level="info",
    public_base_url=os.environ["PUBLIC_BASE_URL"],
    secret_provider="external",
    seed_demo_data=False,
    session_ttl_seconds=604800,
    media_storage_path=Path("data/runtime/media"),
    max_upload_bytes=5 * 1024 * 1024,
    geocoding_provider="local",
    geocoding_base_url="https://example.test",
    geocoding_api_key=None,
    cdn_base_url=None,
    metrics_enabled=True,
    match_min_score=10.0,
    max_json_body_bytes=1_048_576,
    cors_allowed_origins=("https://lawim.example",),
    auth_rate_limit_max=30,
    auth_rate_limit_window_seconds=300,
    public_media=False,
)
config.validate()
PY

if ((failures)); then
  echo "PRODUCTION VALIDATION FAILED (${failures})" >&2
  exit 1
fi

echo "PRODUCTION VALIDATION OK"
