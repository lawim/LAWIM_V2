from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from urllib.parse import urlparse
from hashlib import sha256
import os

from .financial.constants import FINANCIAL_CURRENCIES


def _parse_cors_origins(raw: str | None, public_base_url: str) -> tuple[str, ...]:
    if raw is not None and raw.strip():
        origins = tuple(origin.strip() for origin in raw.split(",") if origin.strip())
        if origins:
            return origins
    parsed = urlparse(public_base_url)
    if parsed.scheme and parsed.netloc:
        return (f"{parsed.scheme}://{parsed.netloc}",)
    return ("http://127.0.0.1:3000",)


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be an integer") from exc


def _float_env(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be a number") from exc


def _optional_int_env(name: str) -> int | None:
    value = os.getenv(name)
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    try:
        return int(stripped)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be an integer") from exc


def _optional_float_env(name: str) -> float | None:
    value = os.getenv(name)
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    try:
        return float(stripped)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be a number") from exc


def _text_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None:
        return default
    stripped = value.strip()
    return stripped or None


def _csv_env(name: str, default: tuple[str, ...] = ()) -> tuple[str, ...]:
    value = os.getenv(name)
    if value is None:
        return default
    items = tuple(part.strip() for part in value.split(",") if part.strip())
    return items or default


def _telegram_webhook_secret_from_token(token: str | None) -> str | None:
    if not token:
        return None
    return sha256(token.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class AppConfig:
    host: str
    port: int
    db_path: Path
    db_driver: str
    database_url: str
    db_fallback: bool
    app_env: str
    stack_profile: str
    log_level: str
    public_base_url: str
    secret_provider: str
    seed_demo_data: bool
    session_ttl_seconds: int
    media_storage_path: Path
    media_provider: str = "local"
    max_upload_bytes: int = 5 * 1024 * 1024
    geocoding_provider: str = "local"
    geocoding_base_url: str = "https://nominatim.openstreetmap.org/search"
    geocoding_api_key: str | None = None
    cdn_base_url: str | None = None
    metrics_enabled: bool = True
    match_min_score: float = 10.0
    max_json_body_bytes: int = 1_048_576
    cors_allowed_origins: tuple[str, ...] = ()
    auth_rate_limit_max: int = 30
    auth_rate_limit_window_seconds: int = 300
    public_media: bool = True
    financial_core_enabled: bool = True
    payments_enabled: bool = True
    refunds_enabled: bool = True
    subscriptions_enabled: bool = True
    commissions_enabled: bool = True
    payouts_enabled: bool = True
    financial_admin_enabled: bool = True
    campay_enabled: bool = False
    campay_sandbox_enabled: bool = True
    campay_environment: str = "sandbox"
    campay_base_url: str = ""
    campay_app_username: str | None = None
    campay_app_password: str | None = None
    campay_token: str | None = None
    campay_webhook_secret: str | None = None
    campay_webhook_url: str | None = None
    campay_redirect_url: str | None = None
    campay_default_currency: str = "XAF"
    campay_timeout_seconds: int = 30
    campay_max_retries: int = 3
    campay_status_check_interval: int = 60
    campay_provider_priority: int = 10
    campay_widget_enabled: bool = False
    campay_payment_links_enabled: bool = False
    campay_disbursement_enabled: bool = False
    campay_dev_mode: bool = True
    campay_prod_mode: bool = False
    green_api_api_url: str | None = None
    green_api_media_url: str | None = None
    green_api_id_instance: str | None = None
    green_api_token_instance: str | None = None
    green_api_webhook_secret: str | None = None
    green_api_webhook_url: str | None = None
    green_api_phone: str | None = None
    telegram_webhook_secret: str | None = None
    telegram_webhook_url: str | None = None
    ai_orchestrator_enabled: bool = False
    ai_provider_deepseek_enabled: bool = False
    ai_provider_openai_enabled: bool = False
    ai_provider_gemini_primary_enabled: bool = False
    ai_provider_gemini_secondary_enabled: bool = False
    ai_primary_provider: str = "deepseek"
    ai_complex_provider: str = "openai"
    ai_fallback_chain: tuple[str, ...] = (
        "deepseek",
        "openai",
        "gemini_primary",
        "gemini_secondary",
        "internal",
    )
    ai_request_timeout_seconds: int = 30
    ai_total_timeout_seconds: int = 75
    ai_max_retries_per_provider: int = 1
    ai_circuit_breaker_enabled: bool = True
    ai_circuit_breaker_failure_threshold: int = 5
    ai_circuit_breaker_window_seconds: int = 300
    ai_circuit_breaker_open_seconds: int = 600
    ai_circuit_breaker_half_open_requests: int = 1
    ai_credit_warning_percent: int = 20
    ai_credit_critical_percent: int = 10
    ai_credit_exhausted_percent: int = 2
    ai_provider_inactivity_monitoring_enabled: bool = True
    ai_provider_inactivity_warning_hours: int = 24
    ai_provider_inactivity_critical_hours: int = 72
    ai_provider_healthcheck_interval_minutes: int = 30
    ai_response_validation_enabled: bool = True
    ai_allow_provider_retry: bool = False
    ai_complex_routing_enabled: bool = True
    ai_expensive_model_requires_complexity: bool = True
    ai_max_context_messages: int = 20
    ai_max_context_tokens: int | None = None
    ai_context_summary_enabled: bool = True
    ai_context_redaction_enabled: bool = True
    ai_daily_budget_limit: float | None = None
    ai_monthly_budget_limit: float | None = None
    ai_max_cost_per_request: float | None = None
    ai_max_cost_per_conversation: float | None = None
    ai_alerts_enabled: bool = True
    ai_alert_email_enabled: bool = False
    ai_alert_whatsapp_enabled: bool = False
    ai_alert_telegram_enabled: bool = False
    ai_alert_admin_recipients: tuple[str, ...] = ()
    communication_fallback_enabled: bool = True
    whatsapp_fallback_enabled: bool = True
    telegram_fallback_enabled: bool = True
    fallback_when_ai_unconfigured: bool = True
    fallback_when_ai_error: bool = True
    fallback_when_no_answer: bool = True
    fallback_escalate_to_human: bool = True
    fallback_default_language: str = "fr"
    fallback_message: str = (
        "Bonjour et bienvenue sur LAWIM.\n\n"
        "Votre message a bien été reçu. Nos assistants intelligents ne sont pas disponibles pour le moment, "
        "mais votre demande a été enregistrée.\n\n"
        "Merci de préciser brièvement l’objet de votre demande. Un membre de notre équipe pourra reprendre la conversation si nécessaire."
    )
    ai_learning_enabled: bool = True
    ai_learning_auto_publish: bool = False
    ai_learning_requires_human_approval: bool = True
    ai_learning_anonymization_enabled: bool = True
    human_escalation_enabled: bool = True
    human_escalation_after_fallback_count: int = 2
    human_escalation_on_user_request: bool = True
    human_escalation_on_all_providers_failed: bool = True
    deepseek_api_key: str | None = None
    deepseek_model: str | None = "deepseek-v4-flash"
    deepseek_base_url: str | None = "https://api.deepseek.com"
    openai_api_key: str | None = None
    openai_model: str | None = "gpt-4o-mini"
    gemini_primary_api_key: str | None = None
    gemini_primary_model: str | None = "gemini-3.5-flash"
    gemini_secondary_api_key: str | None = None
    gemini_secondary_model: str | None = "gemini-2.5-flash"

    @classmethod
    def legacy_construct(
        cls,
        *,
        host: str,
        port: int,
        db_path: Path,
        db_driver: str,
        database_url: str,
        db_fallback: bool,
        app_env: str,
        stack_profile: str,
        log_level: str,
        public_base_url: str,
        secret_provider: str,
        seed_demo_data: bool,
        session_ttl_seconds: int,
        media_storage_path: Path,
        media_provider: str = "local",
        max_upload_bytes: int = 5 * 1024 * 1024,
        geocoding_provider: str = "local",
        geocoding_base_url: str = "https://nominatim.openstreetmap.org/search",
        geocoding_api_key: str | None = None,
        cdn_base_url: str | None = None,
        metrics_enabled: bool = True,
        match_min_score: float = 10.0,
        max_json_body_bytes: int = 1_048_576,
        cors_allowed_origins: tuple[str, ...] = (),
        auth_rate_limit_max: int = 30,
        auth_rate_limit_window_seconds: int = 300,
        public_media: bool = True,
    ) -> "AppConfig":
        return cls(
            host=host,
            port=port,
            db_path=db_path,
            db_driver=db_driver,
            database_url=database_url,
            db_fallback=db_fallback,
            app_env=app_env,
            stack_profile=stack_profile,
            log_level=log_level,
            public_base_url=public_base_url,
            secret_provider=secret_provider,
            seed_demo_data=seed_demo_data,
            session_ttl_seconds=session_ttl_seconds,
            media_storage_path=media_storage_path,
            media_provider=media_provider,
            max_upload_bytes=max_upload_bytes,
            geocoding_provider=geocoding_provider,
            geocoding_base_url=geocoding_base_url,
            geocoding_api_key=geocoding_api_key,
            cdn_base_url=cdn_base_url,
            metrics_enabled=metrics_enabled,
            match_min_score=match_min_score,
            max_json_body_bytes=max_json_body_bytes,
            cors_allowed_origins=cors_allowed_origins,
            auth_rate_limit_max=auth_rate_limit_max,
            auth_rate_limit_window_seconds=auth_rate_limit_window_seconds,
            public_media=public_media,
        )

    @classmethod
    def from_env(cls) -> "AppConfig":
        db_path = Path(os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")).expanduser()
        media_storage_path = Path(os.getenv("LAWIM_MEDIA_STORAGE_PATH", "data/runtime/media")).expanduser()
        geocoding_api_key = os.getenv("LAWIM_GEOCODING_API_KEY")
        cdn_base_url = os.getenv("LAWIM_CDN_BASE_URL")
        public_base_url = os.getenv("PUBLIC_BASE_URL", "http://localhost:3000")
        app_env = os.getenv("APP_ENV", "development")
        telegram_bot_token = _text_env("TELEGRAM_BOT_TOKEN")
        public_media_default = app_env in {"development", "test", "staging"}
        campay_environment = os.getenv("LAWIM_CAMPAY_ENVIRONMENT", "sandbox").strip().lower()
        campay_base_url = os.getenv("LAWIM_CAMPAY_BASE_URL", "").strip()
        if not campay_base_url:
            campay_base_url = "https://www.campay.net" if campay_environment == "production" else "https://demo.campay.net"
        campay_dev_mode_default = campay_environment != "production"
        campay_prod_mode_default = campay_environment == "production"
        ai_fallback_chain = _csv_env(
            "AI_FALLBACK_CHAIN",
            ("deepseek", "openai", "gemini_primary", "gemini_secondary", "internal"),
        )
        ai_admin_recipients = _csv_env("AI_ALERT_ADMIN_RECIPIENTS")
        return cls(
            host=os.getenv("LAWIM_HOST", "0.0.0.0"),
            port=_int_env("LAWIM_PORT", 3000),
            db_path=db_path,
            db_driver=os.getenv("LAWIM_DB_DRIVER", "sqlite"),
            database_url=os.getenv("LAWIM_DATABASE_URL", "postgresql://lawim:lawim@localhost:5432/lawim_v2"),
            db_fallback=_bool_env("LAWIM_DB_FALLBACK", True),
            app_env=app_env,
            stack_profile=os.getenv("STACK_PROFILE", "development"),
            log_level=os.getenv("LOG_LEVEL", "info"),
            public_base_url=public_base_url,
            secret_provider=os.getenv("SECRET_PROVIDER", "external"),
            seed_demo_data=_bool_env("LAWIM_SEED_DEMO_DATA", True),
            session_ttl_seconds=_int_env("LAWIM_SESSION_TTL_SECONDS", 7 * 24 * 60 * 60),
            media_storage_path=media_storage_path,
            media_provider=os.getenv("LAWIM_MEDIA_PROVIDER", "local").strip().lower(),
            max_upload_bytes=_int_env("LAWIM_MAX_UPLOAD_BYTES", 5 * 1024 * 1024),
            geocoding_provider=os.getenv("LAWIM_GEOCODING_PROVIDER", "local"),
            geocoding_base_url=os.getenv("LAWIM_GEOCODING_BASE_URL", "https://nominatim.openstreetmap.org/search"),
            geocoding_api_key=geocoding_api_key.strip() if geocoding_api_key else None,
            cdn_base_url=cdn_base_url.strip() if cdn_base_url else None,
            metrics_enabled=_bool_env("LAWIM_METRICS_ENABLED", True),
            match_min_score=_float_env("LAWIM_MATCH_MIN_SCORE", 10.0),
            max_json_body_bytes=_int_env("LAWIM_MAX_JSON_BODY_BYTES", 1_048_576),
            cors_allowed_origins=_parse_cors_origins(os.getenv("LAWIM_CORS_ORIGINS"), public_base_url),
            auth_rate_limit_max=_int_env("LAWIM_AUTH_RATE_LIMIT_MAX", 30),
            auth_rate_limit_window_seconds=_int_env("LAWIM_AUTH_RATE_LIMIT_WINDOW_SECONDS", 300),
            public_media=_bool_env("LAWIM_PUBLIC_MEDIA", public_media_default),
            financial_core_enabled=_bool_env("LAWIM_FINANCIAL_CORE_ENABLED", True),
            payments_enabled=_bool_env("LAWIM_PAYMENTS_ENABLED", True),
            refunds_enabled=_bool_env("LAWIM_REFUNDS_ENABLED", True),
            subscriptions_enabled=_bool_env("LAWIM_SUBSCRIPTIONS_ENABLED", True),
            commissions_enabled=_bool_env("LAWIM_COMMISSIONS_ENABLED", True),
            payouts_enabled=_bool_env("LAWIM_PAYOUTS_ENABLED", True),
            financial_admin_enabled=_bool_env("LAWIM_FINANCIAL_ADMIN_ENABLED", True),
            campay_enabled=_bool_env("LAWIM_CAMPAY_ENABLED", False),
            campay_sandbox_enabled=_bool_env("LAWIM_CAMPAY_SANDBOX_ENABLED", True),
            campay_environment=campay_environment,
            campay_base_url=campay_base_url,
            campay_app_username=(os.getenv("LAWIM_CAMPAY_APP_USERNAME") or None),
            campay_app_password=(os.getenv("LAWIM_CAMPAY_APP_PASSWORD") or None),
            campay_token=(os.getenv("LAWIM_CAMPAY_TOKEN") or None),
            campay_webhook_secret=(os.getenv("LAWIM_CAMPAY_WEBHOOK_SECRET") or None),
            campay_webhook_url=(os.getenv("LAWIM_CAMPAY_WEBHOOK_URL") or None),
            campay_redirect_url=(os.getenv("LAWIM_CAMPAY_REDIRECT_URL") or None),
            campay_default_currency=os.getenv("LAWIM_CAMPAY_DEFAULT_CURRENCY", "XAF").strip().upper(),
            campay_timeout_seconds=_int_env("LAWIM_CAMPAY_TIMEOUT_SECONDS", 30),
            campay_max_retries=_int_env("LAWIM_CAMPAY_MAX_RETRIES", 3),
            campay_status_check_interval=_int_env("LAWIM_CAMPAY_STATUS_CHECK_INTERVAL", 60),
            campay_provider_priority=_int_env("LAWIM_CAMPAY_PROVIDER_PRIORITY", 10),
            campay_widget_enabled=_bool_env("LAWIM_CAMPAY_WIDGET_ENABLED", False),
            campay_payment_links_enabled=_bool_env("LAWIM_CAMPAY_PAYMENT_LINKS_ENABLED", False),
            campay_disbursement_enabled=_bool_env("LAWIM_CAMPAY_DISBURSEMENT_ENABLED", False),
            campay_dev_mode=_bool_env("LAWIM_CAMPAY_DEV_MODE", campay_dev_mode_default),
            campay_prod_mode=_bool_env("LAWIM_CAMPAY_PROD_MODE", campay_prod_mode_default),
            green_api_api_url=_text_env("GREEN_API_API_URL"),
            green_api_media_url=_text_env("GREEN_API_MEDIA_URL"),
            green_api_id_instance=_text_env("GREEN_API_ID_INSTANCE"),
            green_api_token_instance=_text_env("GREEN_API_TOKEN_INSTANCE"),
            green_api_webhook_secret=_text_env("GREEN_API_WEBHOOK_SECRET"),
            green_api_webhook_url=_text_env("GREEN_API_WEBHOOK_URL"),
            green_api_phone=_text_env("GREEN_API_PHONE"),
            telegram_webhook_secret=_text_env("TELEGRAM_WEBHOOK_SECRET")
            or _telegram_webhook_secret_from_token(telegram_bot_token),
            telegram_webhook_url=_text_env("TELEGRAM_WEBHOOK_URL"),
            ai_orchestrator_enabled=_bool_env("AI_ORCHESTRATOR_ENABLED", False),
            ai_provider_deepseek_enabled=_bool_env("AI_PROVIDER_DEEPSEEK_ENABLED", False),
            ai_provider_openai_enabled=_bool_env("AI_PROVIDER_OPENAI_ENABLED", False),
            ai_provider_gemini_primary_enabled=_bool_env("AI_PROVIDER_GEMINI_PRIMARY_ENABLED", False),
            ai_provider_gemini_secondary_enabled=_bool_env("AI_PROVIDER_GEMINI_SECONDARY_ENABLED", False),
            ai_primary_provider=os.getenv("AI_PRIMARY_PROVIDER", "deepseek").strip().lower(),
            ai_complex_provider=os.getenv("AI_COMPLEX_PROVIDER", "openai").strip().lower(),
            ai_fallback_chain=ai_fallback_chain,
            ai_request_timeout_seconds=_int_env("AI_REQUEST_TIMEOUT_SECONDS", 30),
            ai_total_timeout_seconds=_int_env("AI_TOTAL_TIMEOUT_SECONDS", 75),
            ai_max_retries_per_provider=_int_env("AI_MAX_RETRIES_PER_PROVIDER", 1),
            ai_circuit_breaker_enabled=_bool_env("AI_CIRCUIT_BREAKER_ENABLED", True),
            ai_circuit_breaker_failure_threshold=_int_env("AI_CIRCUIT_BREAKER_FAILURE_THRESHOLD", 5),
            ai_circuit_breaker_window_seconds=_int_env("AI_CIRCUIT_BREAKER_WINDOW_SECONDS", 300),
            ai_circuit_breaker_open_seconds=_int_env("AI_CIRCUIT_BREAKER_OPEN_SECONDS", 600),
            ai_circuit_breaker_half_open_requests=_int_env("AI_CIRCUIT_BREAKER_HALF_OPEN_REQUESTS", 1),
            ai_credit_warning_percent=_int_env("AI_CREDIT_WARNING_PERCENT", 20),
            ai_credit_critical_percent=_int_env("AI_CREDIT_CRITICAL_PERCENT", 10),
            ai_credit_exhausted_percent=_int_env("AI_CREDIT_EXHAUSTED_PERCENT", 2),
            ai_provider_inactivity_monitoring_enabled=_bool_env("AI_PROVIDER_INACTIVITY_MONITORING_ENABLED", True),
            ai_provider_inactivity_warning_hours=_int_env("AI_PROVIDER_INACTIVITY_WARNING_HOURS", 24),
            ai_provider_inactivity_critical_hours=_int_env("AI_PROVIDER_INACTIVITY_CRITICAL_HOURS", 72),
            ai_provider_healthcheck_interval_minutes=_int_env("AI_PROVIDER_HEALTHCHECK_INTERVAL_MINUTES", 30),
            ai_response_validation_enabled=_bool_env("AI_RESPONSE_VALIDATION_ENABLED", True),
            ai_allow_provider_retry=_bool_env("AI_ALLOW_PROVIDER_RETRY", False),
            ai_complex_routing_enabled=_bool_env("AI_COMPLEX_ROUTING_ENABLED", True),
            ai_expensive_model_requires_complexity=_bool_env("AI_EXPENSIVE_MODEL_REQUIRES_COMPLEXITY", True),
            ai_max_context_messages=_int_env("AI_MAX_CONTEXT_MESSAGES", 20),
            ai_max_context_tokens=_optional_int_env("AI_MAX_CONTEXT_TOKENS"),
            ai_context_summary_enabled=_bool_env("AI_CONTEXT_SUMMARY_ENABLED", True),
            ai_context_redaction_enabled=_bool_env("AI_CONTEXT_REDACTION_ENABLED", True),
            ai_daily_budget_limit=_optional_float_env("AI_DAILY_BUDGET_LIMIT"),
            ai_monthly_budget_limit=_optional_float_env("AI_MONTHLY_BUDGET_LIMIT"),
            ai_max_cost_per_request=_optional_float_env("AI_MAX_COST_PER_REQUEST"),
            ai_max_cost_per_conversation=_optional_float_env("AI_MAX_COST_PER_CONVERSATION"),
            ai_alerts_enabled=_bool_env("AI_ALERTS_ENABLED", True),
            ai_alert_email_enabled=_bool_env("AI_ALERT_EMAIL_ENABLED", False),
            ai_alert_whatsapp_enabled=_bool_env("AI_ALERT_WHATSAPP_ENABLED", False),
            ai_alert_telegram_enabled=_bool_env("AI_ALERT_TELEGRAM_ENABLED", False),
            ai_alert_admin_recipients=ai_admin_recipients,
            communication_fallback_enabled=_bool_env("COMMUNICATION_FALLBACK_ENABLED", True),
            whatsapp_fallback_enabled=_bool_env("WHATSAPP_FALLBACK_ENABLED", True),
            telegram_fallback_enabled=_bool_env("TELEGRAM_FALLBACK_ENABLED", True),
            fallback_when_ai_unconfigured=_bool_env("FALLBACK_WHEN_AI_UNCONFIGURED", True),
            fallback_when_ai_error=_bool_env("FALLBACK_WHEN_AI_ERROR", True),
            fallback_when_no_answer=_bool_env("FALLBACK_WHEN_NO_ANSWER", True),
            fallback_escalate_to_human=_bool_env("FALLBACK_ESCALATE_TO_HUMAN", True),
            fallback_default_language=os.getenv("FALLBACK_DEFAULT_LANGUAGE", "fr").strip().lower(),
            fallback_message=os.getenv(
                "FALLBACK_MESSAGE",
                (
                    "Bonjour et bienvenue sur LAWIM.\n\n"
                    "Votre message a bien été reçu. Nos assistants intelligents ne sont pas disponibles pour le moment, "
                    "mais votre demande a été enregistrée.\n\n"
                    "Merci de préciser brièvement l’objet de votre demande. Un membre de notre équipe pourra reprendre la conversation si nécessaire."
                ),
            ).strip(),
            ai_learning_enabled=_bool_env("AI_LEARNING_ENABLED", True),
            ai_learning_auto_publish=_bool_env("AI_LEARNING_AUTO_PUBLISH", False),
            ai_learning_requires_human_approval=_bool_env("AI_LEARNING_REQUIRES_HUMAN_APPROVAL", True),
            ai_learning_anonymization_enabled=_bool_env("AI_LEARNING_ANONYMIZATION_ENABLED", True),
            human_escalation_enabled=_bool_env("HUMAN_ESCALATION_ENABLED", True),
            human_escalation_after_fallback_count=_int_env("HUMAN_ESCALATION_AFTER_FALLBACK_COUNT", 2),
            human_escalation_on_user_request=_bool_env("HUMAN_ESCALATION_ON_USER_REQUEST", True),
            human_escalation_on_all_providers_failed=_bool_env("HUMAN_ESCALATION_ON_ALL_PROVIDERS_FAILED", True),
            deepseek_api_key=_text_env("DEEPSEEK_API_KEY"),
            deepseek_model=_text_env("DEEPSEEK_MODEL", "deepseek-v4-flash"),
            deepseek_base_url=_text_env("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            openai_api_key=_text_env("OPENAI_API_KEY"),
            openai_model=_text_env("OPENAI_MODEL", "gpt-4o-mini"),
            gemini_primary_api_key=_text_env("GEMINI_PRIMARY_API_KEY"),
            gemini_primary_model=_text_env("GEMINI_PRIMARY_MODEL", "gemini-3.5-flash"),
            gemini_secondary_api_key=_text_env("GEMINI_SECONDARY_API_KEY"),
            gemini_secondary_model=_text_env("GEMINI_SECONDARY_MODEL", "gemini-2.5-flash"),
        )

    def validate(self) -> None:
        errors: list[str] = []
        if not (1 <= self.port <= 65535):
            errors.append(f"LAWIM_PORT must be between 1 and 65535 (got {self.port})")
        if self.db_driver not in {"sqlite", "postgresql"}:
            errors.append(f"LAWIM_DB_DRIVER must be sqlite or postgresql (got {self.db_driver!r})")
        if self.session_ttl_seconds < 60:
            errors.append("LAWIM_SESSION_TTL_SECONDS must be at least 60 seconds")
        if self.max_upload_bytes < 1:
            errors.append("LAWIM_MAX_UPLOAD_BYTES must be positive")
        if self.max_json_body_bytes < 1_024:
            errors.append("LAWIM_MAX_JSON_BODY_BYTES must be at least 1024")
        if not (0.0 <= self.match_min_score <= 100.0):
            errors.append("LAWIM_MATCH_MIN_SCORE must be between 0 and 100")
        if self.app_env not in {"development", "staging", "production", "test"}:
            errors.append(f"APP_ENV has unsupported value: {self.app_env!r}")
        if self.app_env == "production" and self.seed_demo_data:
            errors.append("LAWIM_SEED_DEMO_DATA must be false when APP_ENV=production")
        if self.db_driver == "postgresql" and not self.database_url.strip():
            errors.append("LAWIM_DATABASE_URL is required when LAWIM_DB_DRIVER=postgresql")
        if self.app_env == "production":
            if self.db_driver == "postgresql" and self.db_fallback:
                errors.append("LAWIM_DB_FALLBACK must be false when APP_ENV=production and LAWIM_DB_DRIVER=postgresql")
            if not self.public_base_url.lower().startswith("https://"):
                errors.append("PUBLIC_BASE_URL must use https when APP_ENV=production")
            if self.public_media:
                errors.append("LAWIM_PUBLIC_MEDIA must be false when APP_ENV=production")
        if not self.media_provider:
            errors.append("LAWIM_MEDIA_PROVIDER must be set to a non-empty provider name")
        if self.campay_environment not in {"sandbox", "production"}:
            errors.append(f"LAWIM_CAMPAY_ENVIRONMENT must be sandbox or production (got {self.campay_environment!r})")
        if self.campay_default_currency not in FINANCIAL_CURRENCIES:
            errors.append(f"LAWIM_CAMPAY_DEFAULT_CURRENCY must be one of {sorted(FINANCIAL_CURRENCIES)}")
        if self.campay_enabled:
            if not self.campay_base_url:
                errors.append("LAWIM_CAMPAY_BASE_URL is required when LAWIM_CAMPAY_ENABLED=true")
            if not self.campay_webhook_url:
                errors.append("LAWIM_CAMPAY_WEBHOOK_URL is required when LAWIM_CAMPAY_ENABLED=true")
            if not self.campay_webhook_secret:
                errors.append("LAWIM_CAMPAY_WEBHOOK_SECRET is required when LAWIM_CAMPAY_ENABLED=true")
            if not (self.campay_token or (self.campay_app_username and self.campay_app_password)):
                errors.append("LAWIM_CAMPAY_TOKEN or APP_USERNAME/APP_PASSWORD is required when LAWIM_CAMPAY_ENABLED=true")
            if self.campay_dev_mode == self.campay_prod_mode:
                errors.append("Exactly one of LAWIM_CAMPAY_DEV_MODE or LAWIM_CAMPAY_PROD_MODE must be true when Campay is enabled")
            if self.campay_timeout_seconds < 1:
                errors.append("LAWIM_CAMPAY_TIMEOUT_SECONDS must be positive")
            if self.campay_max_retries < 0:
                errors.append("LAWIM_CAMPAY_MAX_RETRIES must be non-negative")
            if self.campay_status_check_interval < 5:
                errors.append("LAWIM_CAMPAY_STATUS_CHECK_INTERVAL must be at least 5 seconds")
        if bool(self.green_api_webhook_url) != bool(self.green_api_webhook_secret):
            errors.append("GREEN_API_WEBHOOK_URL and GREEN_API_WEBHOOK_SECRET must be set together")
        if bool(self.telegram_webhook_url) != bool(self.telegram_webhook_secret):
            errors.append("TELEGRAM_WEBHOOK_URL and TELEGRAM_WEBHOOK_SECRET must be set together")
        if self.ai_orchestrator_enabled or any(
            (
                self.ai_provider_deepseek_enabled,
                self.ai_provider_openai_enabled,
                self.ai_provider_gemini_primary_enabled,
                self.ai_provider_gemini_secondary_enabled,
            )
        ):
            if self.ai_primary_provider not in {"deepseek", "openai", "gemini_primary", "gemini_secondary", "internal"}:
                errors.append("AI_PRIMARY_PROVIDER has unsupported value")
            if self.ai_complex_provider not in {"deepseek", "openai", "gemini_primary", "gemini_secondary", "internal"}:
                errors.append("AI_COMPLEX_PROVIDER has unsupported value")
            if "internal" not in self.ai_fallback_chain:
                errors.append("AI_FALLBACK_CHAIN must include internal")
            if self.ai_request_timeout_seconds < 1:
                errors.append("AI_REQUEST_TIMEOUT_SECONDS must be positive")
            if self.ai_total_timeout_seconds < self.ai_request_timeout_seconds:
                errors.append("AI_TOTAL_TIMEOUT_SECONDS must be greater than or equal to AI_REQUEST_TIMEOUT_SECONDS")
            if self.ai_max_retries_per_provider < 0:
                errors.append("AI_MAX_RETRIES_PER_PROVIDER must be non-negative")
            if self.ai_circuit_breaker_failure_threshold < 1:
                errors.append("AI_CIRCUIT_BREAKER_FAILURE_THRESHOLD must be positive")
            if self.ai_circuit_breaker_window_seconds < 1:
                errors.append("AI_CIRCUIT_BREAKER_WINDOW_SECONDS must be positive")
            if self.ai_circuit_breaker_open_seconds < 1:
                errors.append("AI_CIRCUIT_BREAKER_OPEN_SECONDS must be positive")
            if self.ai_circuit_breaker_half_open_requests < 1:
                errors.append("AI_CIRCUIT_BREAKER_HALF_OPEN_REQUESTS must be positive")
            if not (0 <= self.ai_credit_exhausted_percent <= self.ai_credit_critical_percent <= self.ai_credit_warning_percent <= 100):
                errors.append("AI_CREDIT_*_PERCENT values must satisfy 0 <= exhausted <= critical <= warning <= 100")
            if self.ai_max_context_messages < 1:
                errors.append("AI_MAX_CONTEXT_MESSAGES must be positive")
            if self.ai_max_context_tokens is not None and self.ai_max_context_tokens < 1:
                errors.append("AI_MAX_CONTEXT_TOKENS must be positive when set")
            if self.ai_provider_inactivity_warning_hours < 1:
                errors.append("AI_PROVIDER_INACTIVITY_WARNING_HOURS must be positive")
            if self.ai_provider_inactivity_critical_hours < self.ai_provider_inactivity_warning_hours:
                errors.append("AI_PROVIDER_INACTIVITY_CRITICAL_HOURS must be greater than or equal to AI_PROVIDER_INACTIVITY_WARNING_HOURS")
            if self.ai_daily_budget_limit is not None and self.ai_daily_budget_limit < 0:
                errors.append("AI_DAILY_BUDGET_LIMIT must be non-negative when set")
            if self.ai_monthly_budget_limit is not None and self.ai_monthly_budget_limit < 0:
                errors.append("AI_MONTHLY_BUDGET_LIMIT must be non-negative when set")
            if self.ai_max_cost_per_request is not None and self.ai_max_cost_per_request < 0:
                errors.append("AI_MAX_COST_PER_REQUEST must be non-negative when set")
            if self.ai_max_cost_per_conversation is not None and self.ai_max_cost_per_conversation < 0:
                errors.append("AI_MAX_COST_PER_CONVERSATION must be non-negative when set")
            if self.human_escalation_after_fallback_count < 1:
                errors.append("HUMAN_ESCALATION_AFTER_FALLBACK_COUNT must be positive")
            if self.ai_provider_deepseek_enabled:
                if not self.deepseek_api_key:
                    errors.append("DEEPSEEK_API_KEY is required when AI_PROVIDER_DEEPSEEK_ENABLED=true")
                if not self.deepseek_model:
                    errors.append("DEEPSEEK_MODEL is required when AI_PROVIDER_DEEPSEEK_ENABLED=true")
                if not self.deepseek_base_url:
                    errors.append("DEEPSEEK_BASE_URL is required when AI_PROVIDER_DEEPSEEK_ENABLED=true")
            if self.ai_provider_openai_enabled:
                if not self.openai_api_key:
                    errors.append("OPENAI_API_KEY is required when AI_PROVIDER_OPENAI_ENABLED=true")
                if not self.openai_model:
                    errors.append("OPENAI_MODEL is required when AI_PROVIDER_OPENAI_ENABLED=true")
            if self.ai_provider_gemini_primary_enabled:
                if not self.gemini_primary_api_key:
                    errors.append("GEMINI_PRIMARY_API_KEY is required when AI_PROVIDER_GEMINI_PRIMARY_ENABLED=true")
                if not self.gemini_primary_model:
                    errors.append("GEMINI_PRIMARY_MODEL is required when AI_PROVIDER_GEMINI_PRIMARY_ENABLED=true")
            if self.ai_provider_gemini_secondary_enabled:
                if not self.gemini_secondary_api_key:
                    errors.append("GEMINI_SECONDARY_API_KEY is required when AI_PROVIDER_GEMINI_SECONDARY_ENABLED=true")
                if not self.gemini_secondary_model:
                    errors.append("GEMINI_SECONDARY_MODEL is required when AI_PROVIDER_GEMINI_SECONDARY_ENABLED=true")
        if errors:
            raise ValueError("Invalid LAWIM_V2 configuration: " + "; ".join(errors))

    def ensure_runtime_dir(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.media_storage_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def for_test(
        cls,
        *,
        db_path: Path,
        media_storage_path: Path,
        **overrides: object,
    ) -> "AppConfig":
        config = cls(
            host="127.0.0.1",
            port=3000,
            db_path=db_path,
            db_driver="sqlite",
            database_url="postgresql://lawim:lawim@localhost:5432/lawim_v2",
            db_fallback=True,
            app_env="test",
            stack_profile="test",
            log_level="debug",
            public_base_url="http://127.0.0.1:3000",
            secret_provider="external",
            seed_demo_data=True,
            session_ttl_seconds=3600,
            media_storage_path=media_storage_path,
            media_provider="local",
            max_upload_bytes=5 * 1024 * 1024,
            geocoding_provider="local",
            geocoding_base_url="https://nominatim.openstreetmap.org/search",
            geocoding_api_key=None,
            cdn_base_url=None,
            metrics_enabled=True,
            match_min_score=10.0,
            max_json_body_bytes=1_048_576,
            cors_allowed_origins=("http://127.0.0.1:3000",),
            auth_rate_limit_max=100,
            auth_rate_limit_window_seconds=300,
            public_media=True,
        )
        if overrides:
            config = replace(config, **overrides)  # type: ignore[arg-type]
        return config
