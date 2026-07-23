from __future__ import annotations

import os
import sys


REQUIRED_PROD_VARS: list[str] = [
    "PUBLIC_BASE_URL",
]

REQUIRED_IF_ENABLED: dict[str, list[str]] = {
    # clé = feature flag, valeurs = vars requises si ce flag est true
    "AI_PROVIDER_OPENAI_ENABLED": ["OPENAI_API_KEY"],
    "AI_PROVIDER_DEEPSEEK_ENABLED": ["DEEPSEEK_API_KEY"],
    "AI_PROVIDER_GEMINI_PRIMARY_ENABLED": ["GEMINI_PRIMARY_API_KEY"],
    "AI_PROVIDER_GEMINI_SECONDARY_ENABLED": ["GEMINI_SECONDARY_API_KEY"],
    "GREEN_API_ID_INSTANCE": ["GREEN_API_ID_INSTANCE", "GREEN_API_TOKEN_INSTANCE", "GREEN_API_WEBHOOK_SECRET"],
    "TELEGRAM_BOT_TOKEN": ["TELEGRAM_BOT_TOKEN", "TELEGRAM_WEBHOOK_SECRET"],
    "LAWIM_CAMPAY_ENABLED": ["LAWIM_CAMPAY_APP_USERNAME", "LAWIM_CAMPAY_APP_PASSWORD", "LAWIM_CAMPAY_WEBHOOK_SECRET"],
}

ALL_VARS: list[str] = sorted({
    "APP_ENV", "LOG_LEVEL", "PUBLIC_BASE_URL", "LAWIM_HOST", "LAWIM_PORT",
    "LAWIM_DB_DRIVER", "LAWIM_DATABASE_URL", "LAWIM_DB_PATH",
    "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB",
    "LAWIM_SESSION_TTL_SECONDS", "LAWIM_METRICS_ENABLED",
    "LAWIM_MEDIA_PROVIDER", "LAWIM_MEDIA_STORAGE_PATH",
    "LAWIM_GEOCODING_PROVIDER", "LAWIM_GEOCODING_API_KEY",
    "LAWIM_CORS_ORIGINS", "LAWIM_MAX_UPLOAD_BYTES", "LAWIM_MAX_JSON_BODY_BYTES",
    "LAWIM_MATCH_MIN_SCORE", "LAWIM_SEED_DEMO_DATA", "LAWIM_VAULT_KEY",
    "SECRET_PROVIDER", "STACK_PROFILE",
    "OPENAI_API_KEY", "OPENAI_MODEL",
    "DEEPSEEK_API_KEY", "DEEPSEEK_MODEL", "DEEPSEEK_BASE_URL",
    "GEMINI_PRIMARY_API_KEY", "GEMINI_PRIMARY_MODEL",
    "GEMINI_SECONDARY_API_KEY", "GEMINI_SECONDARY_MODEL",
    "AI_ORCHESTRATOR_ENABLED", "AI_PRIMARY_PROVIDER", "AI_COMPLEX_PROVIDER",
    "AI_FALLBACK_CHAIN", "AI_REQUEST_TIMEOUT_SECONDS",
    "AI_CIRCUIT_BREAKER_ENABLED", "AI_DAILY_BUDGET_LIMIT", "AI_MONTHLY_BUDGET_LIMIT",
    "AI_PROVIDER_OPENAI_ENABLED", "AI_PROVIDER_DEEPSEEK_ENABLED",
    "AI_PROVIDER_GEMINI_PRIMARY_ENABLED", "AI_PROVIDER_GEMINI_SECONDARY_ENABLED",
    "GREEN_API_ID_INSTANCE", "GREEN_API_TOKEN_INSTANCE",
    "GREEN_API_WEBHOOK_SECRET", "GREEN_API_WEBHOOK_URL", "GREEN_API_PHONE",
    "GREEN_API_API_URL", "GREEN_API_MEDIA_URL",
    "TELEGRAM_BOT_TOKEN", "TELEGRAM_WEBHOOK_SECRET", "TELEGRAM_WEBHOOK_URL",
    "LAWIM_CAMPAY_ENABLED", "LAWIM_CAMPAY_APP_USERNAME", "LAWIM_CAMPAY_APP_PASSWORD",
    "LAWIM_CAMPAY_WEBHOOK_SECRET", "LAWIM_CAMPAY_WEBHOOK_URL",
    "LAWIM_CAMPAY_ENVIRONMENT", "LAWIM_CAMPAY_BASE_URL",
    "LAWIM_CAMPAY_DEFAULT_CURRENCY", "LAWIM_CAMPAY_TIMEOUT_SECONDS",
    "LROS_AI_INTELLIGENCE_ENABLED", "LROS_AI_EXTRACTION_ENABLED",
    "LROS_AI_RESPONSE_WRITER_ENABLED", "LROS_AI_SHADOW_MODE",
    "LROS_AI_PROVIDER_CALLS_ENABLED", "LROS_AI_BUDGET_MONTHLY_CENTS",
    "LROS_INTERACTION_GATEWAY_ENABLED", "LROS_WHATSAPP_ADAPTER_ENABLED",
    "LROS_TELEGRAM_ADAPTER_ENABLED",
})


def check_env(quiet: bool = False) -> list[str]:
    missing: list[str] = []

    for var in REQUIRED_PROD_VARS:
        if not os.getenv(var):
            missing.append(var)

    for flag_var, deps in REQUIRED_IF_ENABLED.items():
        if os.getenv(flag_var, "").strip().lower() in ("true", "1"):
            for dep in deps:
                if not os.getenv(dep):
                    missing.append(f"{dep} (required because {flag_var}=true)")

    if missing and not quiet:
        print("=== LAWIM — Environment variable check ===", file=sys.stderr)
        print(f"Missing {len(missing)} required variable(s):", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Create /home/abel/.config/lawim/.env.production with these values.", file=sys.stderr)
        print("See deployment/compose/docker-compose.prod.yml for the expected path.", file=sys.stderr)

    return missing


if __name__ == "__main__":
    errors = check_env()
    if errors:
        sys.exit(1)
    print("All required environment variables are set.")
