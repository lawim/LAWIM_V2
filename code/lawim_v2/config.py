from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True, slots=True)
class AppConfig:
    host: str
    port: int
    db_path: Path
    app_env: str
    stack_profile: str
    log_level: str
    public_base_url: str
    secret_provider: str
    seed_demo_data: bool
    session_ttl_seconds: int

    @classmethod
    def from_env(cls) -> "AppConfig":
        db_path = Path(os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3"))
        return cls(
            host=os.getenv("LAWIM_HOST", "0.0.0.0"),
            port=int(os.getenv("LAWIM_PORT", "3000")),
            db_path=db_path,
            app_env=os.getenv("APP_ENV", "development"),
            stack_profile=os.getenv("STACK_PROFILE", "development"),
            log_level=os.getenv("LOG_LEVEL", "info"),
            public_base_url=os.getenv("PUBLIC_BASE_URL", "http://localhost:3000"),
            secret_provider=os.getenv("SECRET_PROVIDER", "external"),
            seed_demo_data=_bool_env("LAWIM_SEED_DEMO_DATA", True),
            session_ttl_seconds=int(os.getenv("LAWIM_SESSION_TTL_SECONDS", str(7 * 24 * 60 * 60))),
        )

    def ensure_runtime_dir(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
