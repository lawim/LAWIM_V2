import os
import tempfile
from lawim_runtime.production.migrate import run_migrations, MIGRATIONS, ROLLBACK_MIGRATIONS


def test_migrations_run_clean():
    with tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False) as f:
        db_path = f.name
    try:
        run_migrations(db_path)
        import sqlite3
        conn = sqlite3.connect(db_path)
        tables = set(row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
        assert "sessions" in tables
        assert "profiles" in tables
        assert "deliveries" in tables
        assert "events" in tables
        assert "_migrations" in tables
        conn.close()
    finally:
        os.unlink(db_path)


def test_migrations_idempotent():
    with tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False) as f:
        db_path = f.name
    try:
        run_migrations(db_path)
        import sqlite3
        conn = sqlite3.connect(db_path)
        count_before = conn.execute("SELECT COUNT(*) FROM _migrations").fetchone()[0]
        conn.close()
        run_migrations(db_path)
        conn = sqlite3.connect(db_path)
        count_after = conn.execute("SELECT COUNT(*) FROM _migrations").fetchone()[0]
        assert count_before == count_after
        conn.close()
    finally:
        os.unlink(db_path)


def test_migrations_rollback():
    with tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False) as f:
        db_path = f.name
    try:
        run_migrations(db_path)
        run_migrations(db_path, rollback=True)
        import sqlite3
        conn = sqlite3.connect(db_path)
        tables = set(row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
        assert "_migrations" in tables
        conn.close()
    finally:
        os.unlink(db_path)
