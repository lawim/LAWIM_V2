# Services

| Service | Type | Purpose |
| --- | --- | --- |
| `lawim-app` | Docker container | application runtime |
| `lawim-postgres` | Docker container | PostgreSQL data store |
| `lawim-redis` | Docker container | Redis cache |
| `nginx` | host service | TLS reverse proxy |
| `lawim-stack.service` | systemd service | stack bootstrap helper |
| `lawim-backup.service` | systemd service | backup job runner |
| `lawim-backup.timer` | systemd timer | scheduled backups |

The application listens locally on port `3000` behind Nginx.
