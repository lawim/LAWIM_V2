# Incident Runbook

## Application does not start

- inspect container logs;
- verify `/opt/lawim/secrets/.env`;
- verify `/opt/lawim/current`;
- restart the application stack after the correction.

## PostgreSQL is unhealthy

- verify the data volume under `/opt/lawim/data/postgres`;
- verify the database URL and credentials;
- restore the latest validated backup if corruption is confirmed.

## Redis is unhealthy

- verify the data volume under `/opt/lawim/data/redis`;
- verify the cache credentials;
- restart Redis and recheck the health endpoints.

## Nginx returns 502

- confirm the application container listens on the expected local port;
- confirm the host proxy configuration;
- confirm the application health endpoint returns `200`.

## Security incident

- rotate exposed secrets immediately;
- invalidate tokens or sessions if exposure is confirmed;
- preserve logs and export them before cleanup;
- document the incident in `DEPLOYMENT_HISTORY.md`.
