# LAWIM_V2 — Developer Platform Setup (Ubuntu / Linux Mint)

Reproducible local development and validation without modifying application business logic.

## Quick start

```bash
cd /path/to/LAWIM_V2

# 1. Diagnose Docker/Podman
./platform/detect-runtime.sh

# 2. Optional: copy platform env
cp platform/platform.env.example .env.platform

# 3. Python tooling (venv + pg8000 + editable install)
./platform/setup-dev-venv.sh

# 4. PostgreSQL dev database (Podman container on port 5433 by default)
./platform/start-postgres.sh

# 5. Run PostgreSQL integration tests
./platform/run-postgres-tests.sh

# 6. Full platform validation
./platform/validate-platform.sh
```

## Native SQLite dev (no containers)

```bash
./scripts/run-local.sh
./scripts/run-tests.sh
```

## Container runtime matrix

| Setup | `docker compose up` | Recommended command |
|-------|----------------------|---------------------|
| Docker Engine + Compose v2 | Works | `docker compose` |
| Podman + podman-compose | Works | `podman-compose` or `./platform/compose.sh` |
| Podman docker shim + compose v1 | **Fails** (no socket) | Use `podman-compose` via `./platform/compose.sh` |

### Why `docker compose` fails on Podman-only hosts

On this machine, `docker` is a **Podman emulation shim**. `docker compose` delegates to **docker-compose v1**, which connects to `/var/run/docker.sock`. That socket symlinks to `/run/podman/podman.sock`, which is **not running** in rootless mode without `podman system service`.

**Symptom:**

```
docker.errors.DockerException: Error while fetching server API version:
FileNotFoundError: [Errno 2] No such file or directory
```

**Fix:** use `./platform/compose.sh` (auto-selects `podman-compose`) or export `LAWIM_COMPOSE=podman-compose`.

`docker compose config` may still work (YAML parse only); `up` requires a live engine API.

## PostgreSQL

Default dev DSN (port **5433** avoids conflict with host PostgreSQL on 5432):

```
LAWIM_TEST_POSTGRES_URL=postgresql://lawim:lawim@127.0.0.1:5433/lawim_v2
```

Scripts:

| Script | Purpose |
|--------|---------|
| `platform/start-postgres.sh` | Start postgres:16-alpine container |
| `platform/stop-postgres.sh` | Stop container |
| `platform/reset-postgres.sh` | Drop volume + fresh database |
| `platform/wait-postgres.sh` | Health wait |
| `platform/run-postgres-tests.sh` | Integration + smoke |

## Ubuntu package hints

```bash
sudo apt install python3.12 python3.12-venv nodejs postgresql-client
# Podman path:
sudo apt install podman podman-compose
# Docker path:
sudo apt install docker.io docker-compose-v2
sudo usermod -aG docker "$USER"
```

## Environment files

| File | Purpose |
|------|---------|
| `platform/platform.env.example` | Platform defaults (ports, DSN, venv path) |
| `.env.platform` | Local overrides (gitignored) |
| `env/development/.env.example` | Application runtime config |

## CI parity

GitHub Actions uses Docker Engine with a `postgres:16-alpine` service on port 5432. Locally, use port 5433 via `.env.platform` to avoid clashing with a system PostgreSQL instance.

See `reports/platform/DEVELOPER-PLATFORM-001-REPORT.md` for full diagnostic report.
