#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "code") not in sys.path:
    sys.path.insert(0, str(ROOT / "code"))

from lawim_v2.config import AppConfig
from lawim_v2.errors import NotFoundError, RepositoryError
from lawim_v2.persistence_adapter import resolve_persistence_adapter
from lawim_v2.services import LawimServices

SYSTEM_ADMIN_ACTOR = {"id": 0, "role": "admin"}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reset a user's password through the official LAWIM_V2 administration service.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--email", required=True, help="Email address of the user whose password will be reset")
    parser.add_argument("--password", required=True, help="New password for the user")
    return parser.parse_args(argv)


def load_config() -> AppConfig:
    config = AppConfig.from_env()
    config.validate()
    return config


def create_repository(config: AppConfig):
    if config.db_driver == "sqlite" and not config.db_path.exists():
        raise FileNotFoundError(
            f"SQLite database file not found: {config.db_path}. "
            "Set LAWIM_DB_PATH to the production database file."
        )
    adapter = resolve_persistence_adapter(
        config.db_path,
        db_driver=config.db_driver,
        database_url=config.database_url,
        allow_sqlite_fallback=config.db_fallback,
    )
    return adapter.create_repository()


def reset_password(email: str, password: str) -> int:
    config = load_config()
    repository = create_repository(config)
    try:
        user = repository.get_user_by_email(email)
    except NotFoundError:
        print(f"User not found: {email}")
        return 1

    services = LawimServices(repository, config)
    try:
        services.update_user(actor=SYSTEM_ADMIN_ACTOR, user_id=int(user["id"]), password=password)
    except RepositoryError as exc:
        print(f"Failed to reset password: {exc}")
        return 1

    print(f"Password reset successfully for user: {email}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    return reset_password(args.email, args.password)


if __name__ == "__main__":
    sys.exit(main())
