# Incident Runbook

## Application does not start

- inspect container logs
- verify `.env` values in `/opt/lawim/secrets/`
- confirm the release symlink points to `/opt/lawim/releases/bc46a686`
- restart the application container after correction

## PostgreSQL is unhealthy

- verify the volume under `/opt/lawim/data/postgres`
- confirm `LAWIM_DATABASE_URL`
- restore the latest backup if data corruption is confirmed

## Redis is unhealthy

- verify the Redis password
- confirm the data volume under `/opt/lawim/data/redis`
- restart the Redis container and recheck the health endpoint

## Nginx returns 502

- confirm the app container listens on the expected port
- confirm the host proxy points to the local runtime port
- check that the application health endpoint returns `200`

## Rollback

- stop the current stack
- restore the previous release
- restore backups only when data rollback is required
- validate the health checks before reopening access

