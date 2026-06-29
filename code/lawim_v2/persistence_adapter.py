from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from .persistence import build_postgresql_profile, build_persistence_profile

if TYPE_CHECKING:
    from .db import LawimRepository


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
    adapter_name = "postgresql-repository-prepared"

    def __init__(self, dsn: str | None = None) -> None:
        self.dsn = dsn or os.getenv("LAWIM_DATABASE_URL", "postgresql://lawim:lawim@localhost:5432/lawim_v2")

    def backend_profile(self, schema_version: int) -> dict[str, object]:
        profile = build_postgresql_profile(self.dsn, schema_version)
        profile["adapter"] = self.adapter_name
        return profile

    def create_repository(self, *, seed: object | None = None) -> "LawimRepository":
        raise RuntimeError(
            "PostgreSQL runtime is prepared but not activated. "
            "Set LAWIM_DB_DRIVER=sqlite or implement the PostgreSQL adapter in a future wave."
        )


def resolve_persistence_adapter(db_path: Path) -> SQLitePersistenceAdapter | PostgreSQLPersistenceAdapter:
    driver = os.getenv("LAWIM_DB_DRIVER", "sqlite").strip().lower()
    if driver == "postgresql":
        return PostgreSQLPersistenceAdapter()
    return SQLitePersistenceAdapter(db_path)
