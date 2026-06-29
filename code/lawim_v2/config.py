from __future__ import annotations

from dataclasses import dataclass
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

    @classmethod
    def from_env(cls) -> "AppConfig":
        db_path = Path(os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")).expanduser()
        media_storage_path = Path(os.getenv("LAWIM_MEDIA_STORAGE_PATH", "data/runtime/media")).expanduser()
        geocoding_api_key = os.getenv("LAWIM_GEOCODING_API_KEY")
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
        )

    def ensure_runtime_dir(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.media_storage_path.mkdir(parents=True, exist_ok=True)
