from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from .persistence import build_postgresql_profile, build_persistence_profile

if TYPE_CHECKING:
    from .db import LawimRepository

LOGGER = logging.getLogger("lawim_v2.persistence")


class SQLitePersistenceAdapter:
    driver = "sqlite"
    adapter_name = "sqlite-repository"

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)

    def create_repository(self, *, seed: object | None = None) -> "LawimRepository":
        from .db import DemoSeed, LawimRepository

        demo_seed = seed if isinstance(seed, DemoSeed) else None
        return LawimRepository(self.db_path, seed=demo_seed)

    def backend_profile(self, schema_version: int) -> dict[str, object]:
        profile = build_persistence_profile(self.db_path, schema_version)
        profile["adapter"] = self.adapter_name
        return profile


class PostgreSQLPersistenceAdapter:
    driver = "postgresql"
    adapter_name = "postgresql-repository"

    def __init__(self, dsn: str, *, fallback_db_path: Path | None = None, allow_sqlite_fallback: bool = True) -> None:
        self.dsn = dsn
        self.fallback_db_path = fallback_db_path
        self.allow_sqlite_fallback = allow_sqlite_fallback

    def backend_profile(self, schema_version: int) -> dict[str, object]:
        profile = build_postgresql_profile(self.dsn, schema_version)
        profile["adapter"] = self.adapter_name
        profile["status"] = "active"
        return profile

    def create_repository(self, *, seed: object | None = None) -> "LawimRepository":
        from .db import DemoSeed, LawimRepository
        from .postgresql_repository import PostgreSQLLawimRepository, check_postgres_connection, postgres_available

        demo_seed = seed if isinstance(seed, DemoSeed) else None
        if postgres_available() and check_postgres_connection(self.dsn):
            LOGGER.info("Using PostgreSQL repository at %s", self.dsn)
            return PostgreSQLLawimRepository(self.dsn, seed=demo_seed)
        if self.allow_sqlite_fallback and self.fallback_db_path is not None:
            LOGGER.warning("PostgreSQL unavailable — falling back to SQLite at %s", self.fallback_db_path)
            return LawimRepository(self.fallback_db_path, seed=demo_seed)
        raise RuntimeError(
            "PostgreSQL runtime requested but unavailable. "
            "Install requirements-postgresql.txt, start PostgreSQL, or set LAWIM_DB_FALLBACK=sqlite."
        )


def resolve_persistence_adapter(
    db_path: Path,
    *,
    db_driver: str,
    database_url: str,
    allow_sqlite_fallback: bool,
) -> SQLitePersistenceAdapter | PostgreSQLPersistenceAdapter:
    driver = db_driver.strip().lower()
    if driver == "postgresql":
        return PostgreSQLPersistenceAdapter(
            database_url,
            fallback_db_path=db_path,
            allow_sqlite_fallback=allow_sqlite_fallback,
        )
    return SQLitePersistenceAdapter(db_path)
