from __future__ import annotations

from collections.abc import Iterable


def tables_present(repository, table_names: Iterable[str]) -> bool:
    names = tuple(dict.fromkeys(str(name) for name in table_names))
    if not names:
        return True

    driver = str(getattr(repository, "driver", "sqlite")).strip().lower()
    placeholders = ", ".join("?" for _ in names)
    if driver in {"postgresql", "postgres"}:
        rows = repository.all(
            f"""
            SELECT table_name AS name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name IN ({placeholders})
            """,
            names,
        )
    else:
        rows = repository.all(
            f"SELECT name FROM sqlite_master WHERE type = 'table' AND name IN ({placeholders})",
            names,
        )

    present = {str(row.get("name") or row.get("table_name")) for row in rows}
    return len(present) == len(names)


def table_exists(repository, table_name: str) -> bool:
    return tables_present(repository, (table_name,))
