from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from .config import AppConfig
from .db import LawimRepository
from .persistence_adapter import resolve_persistence_adapter
from .services import LawimServices


@dataclass(slots=True)
class ApplicationRuntime:
    config: AppConfig
    repository: LawimRepository
    services: LawimServices

    def close(self) -> None:
        self.repository.close()


def build_runtime(config: AppConfig) -> ApplicationRuntime:
    config.validate()
    config.ensure_runtime_dir()
    adapter = resolve_persistence_adapter(
        config.db_path,
        db_driver=config.db_driver,
        database_url=config.database_url,
        allow_sqlite_fallback=config.db_fallback,
    )
    repository = cast(LawimRepository, adapter.create_repository())
    try:
        repository.initialize(seed_demo_data=config.seed_demo_data)
        services = LawimServices(repository, config)
    except Exception:
        try:
            repository.close()
        except Exception:
            pass
        raise
    return ApplicationRuntime(config=config, repository=repository, services=services)
