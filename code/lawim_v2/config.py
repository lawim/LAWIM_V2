from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import os


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
    max_upload_bytes: int
    geocoding_provider: str
    geocoding_base_url: str
    geocoding_api_key: str | None
    cdn_base_url: str | None
    metrics_enabled: bool
    match_min_score: float
    max_json_body_bytes: int

    @classmethod
    def from_env(cls) -> "AppConfig":
        db_path = Path(os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")).expanduser()
        media_storage_path = Path(os.getenv("LAWIM_MEDIA_STORAGE_PATH", "data/runtime/media")).expanduser()
        geocoding_api_key = os.getenv("LAWIM_GEOCODING_API_KEY")
        cdn_base_url = os.getenv("LAWIM_CDN_BASE_URL")
        return cls(
            host=os.getenv("LAWIM_HOST", "0.0.0.0"),
            port=_int_env("LAWIM_PORT", 3000),
            db_path=db_path,
            db_driver=os.getenv("LAWIM_DB_DRIVER", "sqlite"),
            database_url=os.getenv("LAWIM_DATABASE_URL", "postgresql://lawim:lawim@localhost:5432/lawim_v2"),
            db_fallback=_bool_env("LAWIM_DB_FALLBACK", True),
            app_env=os.getenv("APP_ENV", "development"),
            stack_profile=os.getenv("STACK_PROFILE", "development"),
            log_level=os.getenv("LOG_LEVEL", "info"),
            public_base_url=os.getenv("PUBLIC_BASE_URL", "http://localhost:3000"),
            secret_provider=os.getenv("SECRET_PROVIDER", "external"),
            seed_demo_data=_bool_env("LAWIM_SEED_DEMO_DATA", True),
            session_ttl_seconds=_int_env("LAWIM_SESSION_TTL_SECONDS", 7 * 24 * 60 * 60),
            media_storage_path=media_storage_path,
            max_upload_bytes=_int_env("LAWIM_MAX_UPLOAD_BYTES", 5 * 1024 * 1024),
            geocoding_provider=os.getenv("LAWIM_GEOCODING_PROVIDER", "local"),
            geocoding_base_url=os.getenv("LAWIM_GEOCODING_BASE_URL", "https://nominatim.openstreetmap.org/search"),
            geocoding_api_key=geocoding_api_key.strip() if geocoding_api_key else None,
            cdn_base_url=cdn_base_url.strip() if cdn_base_url else None,
            metrics_enabled=_bool_env("LAWIM_METRICS_ENABLED", True),
            match_min_score=_float_env("LAWIM_MATCH_MIN_SCORE", 10.0),
            max_json_body_bytes=_int_env("LAWIM_MAX_JSON_BODY_BYTES", 1_048_576),
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
            max_upload_bytes=5 * 1024 * 1024,
            geocoding_provider="local",
            geocoding_base_url="https://nominatim.openstreetmap.org/search",
            geocoding_api_key=None,
            cdn_base_url=None,
            metrics_enabled=True,
            match_min_score=10.0,
            max_json_body_bytes=1_048_576,
        )
        if overrides:
            config = replace(config, **overrides)  # type: ignore[arg-type]
        return config
