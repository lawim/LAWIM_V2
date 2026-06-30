# DEVELOPER PLATFORM 001 — Report

- **Date:** 2026-06-29
- **Repository:** `/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2`
- **Branch:** `release/1.0.0-beta`
- **Tag:** `developer-platform-001`
- **Scope:** Local development & validation platform (product frozen)

---

## 1. Executive summary

The host runs **Linux Mint 22.3** with **Podman 4.9.3** exposed through a **Docker CLI shim**. `docker compose up` fails because Compose v1 (`docker-compose` 1.29.2) requires `/var/run/docker.sock`, which symlinks to a **non-existent** `/run/podman/podman.sock`. **`podman-compose`** works and was adopted as the default via `./platform/compose.sh`.

A reproducible developer platform was added under `platform/` with PostgreSQL on **port 5433** (avoiding conflict with host PostgreSQL on 5432). All **6 PostgreSQL integration tests** and `smoke_postgres.py` pass against the container.

One **infrastructure bug** in `postgresql_repository.py` (pg8000 placeholder/result handling) was fixed — required for real PostgreSQL execution; no business logic changed.

---

## 2. Complete diagnostic

### 2.1 Host environment

| Component | Version / state |
|-----------|-----------------|
| OS | Linux Mint 22.3 (Ubuntu 24.04 base) |
| Python | 3.12 |
| Node | available |
| Podman | 4.9.3 (rootless, `podman info` OK) |
| docker CLI | Podman emulation shim |
| docker-compose | 1.29.2 (via `docker compose` → external provider) |
| podman-compose | 1.0.6 |
| systemd docker | inactive |
| systemd podman | inactive |
| Host PostgreSQL | 16.x listening on `127.0.0.1:5432` (postgres superuser only) |

### 2.2 Socket analysis

```
/var/run/docker.sock → /run/podman/podman.sock
/run/podman/podman.sock — missing (Permission denied / not present)
/run/user/1000/podman/ — not present
```

User `abel` is **not** in group `docker`. Rootless Podman operates without a root socket; `podman ps` works directly.

### 2.3 Compose behaviour

| Command | Result |
|---------|--------|
| `docker compose … config` | PASS (YAML merge only) |
| `docker compose … up` | **FAIL** — docker-compose v1 cannot connect to socket |
| `podman-compose … up -d postgres` | PASS |
| `./platform/compose.sh … config` | PASS (selects podman-compose) |

### 2.4 PostgreSQL connectivity

| Target | Result |
|--------|--------|
| `127.0.0.1:5432` | Host PG — no `lawim` role |
| `127.0.0.1:5433` | Podman `postgres:16-alpine` — lawim/lawim/lawim_v2 |

---

## 3. Root cause — why `docker compose` cannot reach the engine

1. **`docker` is not Docker Engine** — it is Podman's compatibility wrapper (`Emulate Docker CLI using podman`).
2. **`docker compose` invokes docker-compose v1.29.2**, which uses the Python Docker SDK over **Unix socket** `/var/run/docker.sock`.
3. The socket symlink target **`/run/podman/podman.sock` does not exist** because no `podman system service` (or rootful socket) is running.
4. **`docker compose config` succeeds** without a daemon; **`up`/`ps`/`pull` fail** at API connection time.

**Error observed:**

```
docker.errors.DockerException: Error while fetching server API version:
FileNotFoundError: [Errno 2] No such file or directory
```

---

## 4. Corrections applied

### 4.1 Platform scripts (`platform/`)

| Script | Role |
|--------|------|
| `detect-runtime.sh` | Diagnose runtime, compose command, socket |
| `compose.sh` | Auto-select `podman-compose` vs `docker compose` |
| `setup-dev-venv.sh` | `.venv-platform` + pg8000 + editable install |
| `start-postgres.sh` / `stop-postgres.sh` / `reset-postgres.sh` | PostgreSQL container lifecycle |
| `wait-postgres.sh` | Readiness probe |
| `run-postgres-tests.sh` | Full PG test module + smoke |
| `validate-platform.sh` | End-to-end platform gate |
| `DEVELOPER-SETUP.md` | Installation guide |
| `platform.env.example` | Default ports/DSN |

### 4.2 Configuration

- Default **`LAWIM_POSTGRES_PORT=5433`** to avoid host port conflict
- `.gitignore`: `.venv-platform/`, `.env.platform`

### 4.3 Infrastructure fix (PostgreSQL driver)

`code/lawim_v2/postgresql_repository.py`:

- SQL placeholders: `?` → `$1`, `$2` (pg8000 native)
- Parameter binding via ordered kwargs
- Result columns from `connection.columns` after `run()`
- Skip `RETURNING id` for `schema_meta`
- Map PostgreSQL `23505` → `sqlite3.IntegrityError` for shared error handling

### 4.4 Test fix (assertion only)

`tests/test_rc_postgresql.py`: `summary["properties"]` → `summary["published_properties"]` (matches `LawimRepository.summary()` API).

---

## 5. Environment obtained

After setup:

```bash
./platform/detect-runtime.sh
# runtime: podman, compose: podman-compose

./platform/setup-dev-venv.sh
# .venv-platform with pg8000 + lawim_v2 editable

./platform/start-postgres.sh
# postgres:16-alpine on 127.0.0.1:5433

export LAWIM_TEST_POSTGRES_URL=postgresql://lawim:lawim@127.0.0.1:5433/lawim_v2
```

---

## 6. Validations executed

| Gate | Result |
|------|--------|
| `./platform/detect-runtime.sh` | PASS |
| `./platform/setup-dev-venv.sh` | PASS |
| `./platform/start-postgres.sh` + `wait-postgres.sh` | PASS |
| `./platform/run-postgres-tests.sh` | **6/6 OK** + smoke OK |
| `./scripts/run-tests.sh` | **82 tests OK**, 2 skipped (no DSN in default env) |
| `./scripts/validate-install.sh` | PASS |
| `./platform/compose.sh` compose config (dev) | PASS |
| `docker compose up` (baseline) | FAIL (documented — use platform wrapper) |

---

## 7. Remaining limits

1. **`docker compose up` still fails** on Podman-only hosts unless `podman system service` creates a socket or real Docker Engine is installed.
2. **`./scripts/run-tests.sh`** skips PostgreSQL tests unless `LAWIM_TEST_POSTGRES_URL` is exported — use `./platform/run-postgres-tests.sh` for PG coverage.
3. **Host PostgreSQL on 5432** requires manual role/database creation (sudo) if not using the container.
4. **`platform/validate-platform.sh`** is comprehensive but slow (runs install + full suite); use selectively.
5. **Podman internal network** (`lawim_v2_private`) is `internal: true` — app container would need explicit port publishing for host access (unchanged from compose design).

---

## 8. Recommendations for the team

**Ubuntu / Mint (Podman):**

```bash
cp platform/platform.env.example .env.platform
./platform/setup-dev-venv.sh
./platform/start-postgres.sh
./platform/run-postgres-tests.sh
```

**Ubuntu (Docker Engine):**

```bash
sudo apt install docker.io docker-compose-v2
sudo usermod -aG docker "$USER"
export LAWIM_COMPOSE="docker compose"
./platform/start-postgres.sh   # uses port 5433 by default
```

**Optional — enable docker-compose v1 shim on Podman:**

```bash
systemctl --user enable --now podman.socket
# or: podman system service --time=0 &
```

See `platform/DEVELOPER-SETUP.md` for full instructions.
