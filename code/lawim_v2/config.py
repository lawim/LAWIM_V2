from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from urllib.parse import urlparse
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
        public_media_default = app_env in {"development", "test", "staging"}
        campay_environment = os.getenv("LAWIM_CAMPAY_ENVIRONMENT", "sandbox").strip().lower()
        campay_base_url = os.getenv("LAWIM_CAMPAY_BASE_URL", "").strip()
        if not campay_base_url:
            campay_base_url = "https://www.campay.net" if campay_environment == "production" else "https://demo.campay.net"
        campay_dev_mode_default = campay_environment != "production"
        campay_prod_mode_default = campay_environment == "production"
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
