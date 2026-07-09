from __future__ import annotations

from dataclasses import dataclass
import logging
import os
from typing import cast

from .config import AppConfig
from .db import LawimRepository
from .persistence_adapter import resolve_persistence_adapter
from .services import LawimServices

LOGGER = logging.getLogger(__name__)


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
        synced_accounts = repository.sync_standard_demo_accounts()
        if synced_accounts:
            LOGGER.info("Synced standard demo accounts for %s account(s)", len(synced_accounts))
        admin_password = os.getenv("LAWIM_ADMIN_PASSWORD", "").strip()
        if admin_password and config.app_env != "production":
            updated_users = repository.sync_demo_credentials(
                admin_password,
                emails=("admin@lawim.app", "admin@lawim.local"),
            )
            if updated_users:
                LOGGER.info("Synced bootstrap credentials for %s demo account(s)", len(updated_users))
        elif admin_password:
            LOGGER.info("Ignored LAWIM_ADMIN_PASSWORD in production to preserve the standard demo credentials")
        services = LawimServices(repository, config)
    except Exception:
        try:
            repository.close()
        except Exception:
            pass
        raise
    return ApplicationRuntime(config=config, repository=repository, services=services)
