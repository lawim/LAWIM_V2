# Monitoring

## Log sources

- application container logs;
- PostgreSQL container logs;
- Redis container logs;
- Nginx logs on the host;
- backup service logs.

## Operational signals

- endpoint latency;
- 4xx and 5xx response spikes;
- container restarts;
- disk growth under `/opt/lawim/data` and `/opt/lawim/backups`;
- backup success or failure;
- authentication failures and rate-limit events.

## Practical commands

- `docker logs lawim-app`
- `docker logs lawim-postgres`
- `docker logs lawim-redis`
- `journalctl -u nginx`
- `journalctl -u lawim-backup.service`
- `docker stats`
