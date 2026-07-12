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
export GREEN_API_API_URL="${GREEN_API_API_URL:-https://7107.api.greenapi.com}"
export GREEN_API_MEDIA_URL="${GREEN_API_MEDIA_URL:-https://7107.api.greenapi.com}"
export GREEN_API_ID_INSTANCE="${GREEN_API_ID_INSTANCE:-7107644927}"
export GREEN_API_TOKEN_INSTANCE="${GREEN_API_TOKEN_INSTANCE:-green-api-token-instance-placeholder}"
export GREEN_API_WEBHOOK_SECRET="${GREEN_API_WEBHOOK_SECRET:-green-api-webhook-secret-placeholder}"
export GREEN_API_WEBHOOK_URL="${GREEN_API_WEBHOOK_URL:-https://api.lawim.app/api/notifications/whatsapp/webhook}"
export GREEN_API_PHONE="${GREEN_API_PHONE:-237650000000}"
export TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-telegram-bot-token-placeholder}"
export TELEGRAM_WEBHOOK_SECRET="${TELEGRAM_WEBHOOK_SECRET:-telegram-webhook-secret-placeholder}"
export TELEGRAM_WEBHOOK_URL="${TELEGRAM_WEBHOOK_URL:-https://api.lawim.app/api/notifications/telegram/webhook}"
export AI_ORCHESTRATOR_ENABLED="${AI_ORCHESTRATOR_ENABLED:-true}"
export AI_PROVIDER_DEEPSEEK_ENABLED="${AI_PROVIDER_DEEPSEEK_ENABLED:-true}"
export AI_PROVIDER_OPENAI_ENABLED="${AI_PROVIDER_OPENAI_ENABLED:-true}"
export AI_PROVIDER_GEMINI_PRIMARY_ENABLED="${AI_PROVIDER_GEMINI_PRIMARY_ENABLED:-true}"
export AI_PROVIDER_GEMINI_SECONDARY_ENABLED="${AI_PROVIDER_GEMINI_SECONDARY_ENABLED:-true}"
export AI_PRIMARY_PROVIDER="${AI_PRIMARY_PROVIDER:-deepseek}"
export AI_COMPLEX_PROVIDER="${AI_COMPLEX_PROVIDER:-openai}"
export AI_FALLBACK_CHAIN="${AI_FALLBACK_CHAIN:-deepseek,openai,gemini_primary,gemini_secondary,internal}"
export AI_REQUEST_TIMEOUT_SECONDS="${AI_REQUEST_TIMEOUT_SECONDS:-30}"
export AI_TOTAL_TIMEOUT_SECONDS="${AI_TOTAL_TIMEOUT_SECONDS:-75}"
export AI_MAX_RETRIES_PER_PROVIDER="${AI_MAX_RETRIES_PER_PROVIDER:-1}"
export AI_CIRCUIT_BREAKER_ENABLED="${AI_CIRCUIT_BREAKER_ENABLED:-true}"
export AI_CIRCUIT_BREAKER_FAILURE_THRESHOLD="${AI_CIRCUIT_BREAKER_FAILURE_THRESHOLD:-5}"
export AI_CIRCUIT_BREAKER_WINDOW_SECONDS="${AI_CIRCUIT_BREAKER_WINDOW_SECONDS:-300}"
export AI_CIRCUIT_BREAKER_OPEN_SECONDS="${AI_CIRCUIT_BREAKER_OPEN_SECONDS:-600}"
export AI_CIRCUIT_BREAKER_HALF_OPEN_REQUESTS="${AI_CIRCUIT_BREAKER_HALF_OPEN_REQUESTS:-1}"
export AI_CREDIT_WARNING_PERCENT="${AI_CREDIT_WARNING_PERCENT:-20}"
export AI_CREDIT_CRITICAL_PERCENT="${AI_CREDIT_CRITICAL_PERCENT:-10}"
export AI_CREDIT_EXHAUSTED_PERCENT="${AI_CREDIT_EXHAUSTED_PERCENT:-2}"
export AI_PROVIDER_INACTIVITY_MONITORING_ENABLED="${AI_PROVIDER_INACTIVITY_MONITORING_ENABLED:-true}"
export AI_PROVIDER_INACTIVITY_WARNING_HOURS="${AI_PROVIDER_INACTIVITY_WARNING_HOURS:-24}"
export AI_PROVIDER_INACTIVITY_CRITICAL_HOURS="${AI_PROVIDER_INACTIVITY_CRITICAL_HOURS:-72}"
export AI_PROVIDER_HEALTHCHECK_INTERVAL_MINUTES="${AI_PROVIDER_HEALTHCHECK_INTERVAL_MINUTES:-30}"
export AI_RESPONSE_VALIDATION_ENABLED="${AI_RESPONSE_VALIDATION_ENABLED:-true}"
export AI_ALLOW_PROVIDER_RETRY="${AI_ALLOW_PROVIDER_RETRY:-false}"
export AI_COMPLEX_ROUTING_ENABLED="${AI_COMPLEX_ROUTING_ENABLED:-true}"
export AI_EXPENSIVE_MODEL_REQUIRES_COMPLEXITY="${AI_EXPENSIVE_MODEL_REQUIRES_COMPLEXITY:-true}"
export AI_MAX_CONTEXT_MESSAGES="${AI_MAX_CONTEXT_MESSAGES:-20}"
export AI_CONTEXT_SUMMARY_ENABLED="${AI_CONTEXT_SUMMARY_ENABLED:-true}"
export AI_CONTEXT_REDACTION_ENABLED="${AI_CONTEXT_REDACTION_ENABLED:-true}"
export COMMUNICATION_FALLBACK_ENABLED="${COMMUNICATION_FALLBACK_ENABLED:-true}"
export WHATSAPP_FALLBACK_ENABLED="${WHATSAPP_FALLBACK_ENABLED:-true}"
export TELEGRAM_FALLBACK_ENABLED="${TELEGRAM_FALLBACK_ENABLED:-true}"
export FALLBACK_WHEN_AI_UNCONFIGURED="${FALLBACK_WHEN_AI_UNCONFIGURED:-true}"
export FALLBACK_WHEN_AI_ERROR="${FALLBACK_WHEN_AI_ERROR:-true}"
export FALLBACK_WHEN_NO_ANSWER="${FALLBACK_WHEN_NO_ANSWER:-true}"
export FALLBACK_ESCALATE_TO_HUMAN="${FALLBACK_ESCALATE_TO_HUMAN:-true}"
export FALLBACK_DEFAULT_LANGUAGE="${FALLBACK_DEFAULT_LANGUAGE:-fr}"
export AI_LEARNING_ENABLED="${AI_LEARNING_ENABLED:-true}"
export AI_LEARNING_AUTO_PUBLISH="${AI_LEARNING_AUTO_PUBLISH:-false}"
export AI_LEARNING_REQUIRES_HUMAN_APPROVAL="${AI_LEARNING_REQUIRES_HUMAN_APPROVAL:-true}"
export AI_LEARNING_ANONYMIZATION_ENABLED="${AI_LEARNING_ANONYMIZATION_ENABLED:-true}"
export HUMAN_ESCALATION_ENABLED="${HUMAN_ESCALATION_ENABLED:-true}"
export HUMAN_ESCALATION_AFTER_FALLBACK_COUNT="${HUMAN_ESCALATION_AFTER_FALLBACK_COUNT:-2}"
export HUMAN_ESCALATION_ON_USER_REQUEST="${HUMAN_ESCALATION_ON_USER_REQUEST:-true}"
export HUMAN_ESCALATION_ON_ALL_PROVIDERS_FAILED="${HUMAN_ESCALATION_ON_ALL_PROVIDERS_FAILED:-true}"
export DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY:-deepseek-api-key-placeholder}"
export DEEPSEEK_MODEL="${DEEPSEEK_MODEL:-deepseek-v4-flash}"
export DEEPSEEK_BASE_URL="${DEEPSEEK_BASE_URL:-https://api.deepseek.com}"
export OPENAI_API_KEY="${OPENAI_API_KEY:-openai-api-key-placeholder}"
export OPENAI_MODEL="${OPENAI_MODEL:-gpt-4o-mini}"
export GEMINI_PRIMARY_API_KEY="${GEMINI_PRIMARY_API_KEY:-gemini-primary-api-key-placeholder}"
export GEMINI_PRIMARY_MODEL="${GEMINI_PRIMARY_MODEL:-gemini-3.5-flash}"
export GEMINI_SECONDARY_API_KEY="${GEMINI_SECONDARY_API_KEY:-gemini-secondary-api-key-placeholder}"
export GEMINI_SECONDARY_MODEL="${GEMINI_SECONDARY_MODEL:-gemini-2.5-flash}"

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
from hashlib import sha256
from lawim_v2.config import AppConfig

telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
telegram_webhook_secret = os.environ.get("TELEGRAM_WEBHOOK_SECRET") or sha256(telegram_bot_token.encode("utf-8")).hexdigest()

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
    green_api_api_url=os.environ["GREEN_API_API_URL"],
    green_api_media_url=os.environ["GREEN_API_MEDIA_URL"],
    green_api_id_instance=os.environ["GREEN_API_ID_INSTANCE"],
    green_api_token_instance=os.environ["GREEN_API_TOKEN_INSTANCE"],
    green_api_webhook_secret=os.environ["GREEN_API_WEBHOOK_SECRET"],
    green_api_webhook_url=os.environ["GREEN_API_WEBHOOK_URL"],
    green_api_phone=os.environ["GREEN_API_PHONE"],
    telegram_webhook_secret=telegram_webhook_secret,
    telegram_webhook_url=os.environ["TELEGRAM_WEBHOOK_URL"],
    ai_orchestrator_enabled=os.environ["AI_ORCHESTRATOR_ENABLED"].lower() == "true",
    ai_provider_deepseek_enabled=os.environ["AI_PROVIDER_DEEPSEEK_ENABLED"].lower() == "true",
    ai_provider_openai_enabled=os.environ["AI_PROVIDER_OPENAI_ENABLED"].lower() == "true",
    ai_provider_gemini_primary_enabled=os.environ["AI_PROVIDER_GEMINI_PRIMARY_ENABLED"].lower() == "true",
    ai_provider_gemini_secondary_enabled=os.environ["AI_PROVIDER_GEMINI_SECONDARY_ENABLED"].lower() == "true",
    ai_primary_provider=os.environ["AI_PRIMARY_PROVIDER"],
    ai_complex_provider=os.environ["AI_COMPLEX_PROVIDER"],
    ai_fallback_chain=tuple(part.strip() for part in os.environ["AI_FALLBACK_CHAIN"].split(",") if part.strip()),
    ai_request_timeout_seconds=int(os.environ["AI_REQUEST_TIMEOUT_SECONDS"]),
    ai_total_timeout_seconds=int(os.environ["AI_TOTAL_TIMEOUT_SECONDS"]),
    ai_max_retries_per_provider=int(os.environ["AI_MAX_RETRIES_PER_PROVIDER"]),
    ai_circuit_breaker_enabled=os.environ["AI_CIRCUIT_BREAKER_ENABLED"].lower() == "true",
    ai_circuit_breaker_failure_threshold=int(os.environ["AI_CIRCUIT_BREAKER_FAILURE_THRESHOLD"]),
    ai_circuit_breaker_window_seconds=int(os.environ["AI_CIRCUIT_BREAKER_WINDOW_SECONDS"]),
    ai_circuit_breaker_open_seconds=int(os.environ["AI_CIRCUIT_BREAKER_OPEN_SECONDS"]),
    ai_circuit_breaker_half_open_requests=int(os.environ["AI_CIRCUIT_BREAKER_HALF_OPEN_REQUESTS"]),
    ai_credit_warning_percent=int(os.environ["AI_CREDIT_WARNING_PERCENT"]),
    ai_credit_critical_percent=int(os.environ["AI_CREDIT_CRITICAL_PERCENT"]),
    ai_credit_exhausted_percent=int(os.environ["AI_CREDIT_EXHAUSTED_PERCENT"]),
    ai_provider_inactivity_monitoring_enabled=os.environ["AI_PROVIDER_INACTIVITY_MONITORING_ENABLED"].lower() == "true",
    ai_provider_inactivity_warning_hours=int(os.environ["AI_PROVIDER_INACTIVITY_WARNING_HOURS"]),
    ai_provider_inactivity_critical_hours=int(os.environ["AI_PROVIDER_INACTIVITY_CRITICAL_HOURS"]),
    ai_provider_healthcheck_interval_minutes=int(os.environ["AI_PROVIDER_HEALTHCHECK_INTERVAL_MINUTES"]),
    ai_response_validation_enabled=os.environ["AI_RESPONSE_VALIDATION_ENABLED"].lower() == "true",
    ai_allow_provider_retry=os.environ["AI_ALLOW_PROVIDER_RETRY"].lower() == "true",
    ai_complex_routing_enabled=os.environ["AI_COMPLEX_ROUTING_ENABLED"].lower() == "true",
    ai_expensive_model_requires_complexity=os.environ["AI_EXPENSIVE_MODEL_REQUIRES_COMPLEXITY"].lower() == "true",
    ai_max_context_messages=int(os.environ["AI_MAX_CONTEXT_MESSAGES"]),
    ai_context_summary_enabled=os.environ["AI_CONTEXT_SUMMARY_ENABLED"].lower() == "true",
    ai_context_redaction_enabled=os.environ["AI_CONTEXT_REDACTION_ENABLED"].lower() == "true",
    communication_fallback_enabled=os.environ["COMMUNICATION_FALLBACK_ENABLED"].lower() == "true",
    whatsapp_fallback_enabled=os.environ["WHATSAPP_FALLBACK_ENABLED"].lower() == "true",
    telegram_fallback_enabled=os.environ["TELEGRAM_FALLBACK_ENABLED"].lower() == "true",
    fallback_when_ai_unconfigured=os.environ["FALLBACK_WHEN_AI_UNCONFIGURED"].lower() == "true",
    fallback_when_ai_error=os.environ["FALLBACK_WHEN_AI_ERROR"].lower() == "true",
    fallback_when_no_answer=os.environ["FALLBACK_WHEN_NO_ANSWER"].lower() == "true",
    fallback_escalate_to_human=os.environ["FALLBACK_ESCALATE_TO_HUMAN"].lower() == "true",
    fallback_default_language=os.environ["FALLBACK_DEFAULT_LANGUAGE"],
    ai_learning_enabled=os.environ["AI_LEARNING_ENABLED"].lower() == "true",
    ai_learning_auto_publish=os.environ["AI_LEARNING_AUTO_PUBLISH"].lower() == "true",
    ai_learning_requires_human_approval=os.environ["AI_LEARNING_REQUIRES_HUMAN_APPROVAL"].lower() == "true",
    ai_learning_anonymization_enabled=os.environ["AI_LEARNING_ANONYMIZATION_ENABLED"].lower() == "true",
    human_escalation_enabled=os.environ["HUMAN_ESCALATION_ENABLED"].lower() == "true",
    human_escalation_after_fallback_count=int(os.environ["HUMAN_ESCALATION_AFTER_FALLBACK_COUNT"]),
    human_escalation_on_user_request=os.environ["HUMAN_ESCALATION_ON_USER_REQUEST"].lower() == "true",
    human_escalation_on_all_providers_failed=os.environ["HUMAN_ESCALATION_ON_ALL_PROVIDERS_FAILED"].lower() == "true",
    deepseek_api_key=os.environ["DEEPSEEK_API_KEY"],
    deepseek_model=os.environ["DEEPSEEK_MODEL"],
    deepseek_base_url=os.environ["DEEPSEEK_BASE_URL"],
    openai_api_key=os.environ["OPENAI_API_KEY"],
    openai_model=os.environ["OPENAI_MODEL"],
    gemini_primary_api_key=os.environ["GEMINI_PRIMARY_API_KEY"],
    gemini_primary_model=os.environ["GEMINI_PRIMARY_MODEL"],
    gemini_secondary_api_key=os.environ["GEMINI_SECONDARY_API_KEY"],
    gemini_secondary_model=os.environ["GEMINI_SECONDARY_MODEL"],
)
config.validate()
PY

if ((failures)); then
  echo "PRODUCTION VALIDATION FAILED (${failures})" >&2
  exit 1
fi

echo "PRODUCTION VALIDATION OK"
