# Secrets Reference

## Server-only secret material

| Secret | Role | Location |
| --- | --- | --- |
| `SECRET_KEY` | application signing and session secret | `/opt/lawim/secrets/.env` |
| PostgreSQL password | database authentication | `/opt/lawim/secrets/.env` |
| Redis password | cache authentication | `/opt/lawim/secrets/.env` |
| TLS private key | HTTPS termination during validation | `/opt/lawim/secrets/tls/` |
| future mail / SMS / WhatsApp credentials | external integrations | `/opt/lawim/secrets/.env` or vault |

## Rules

- never commit real values to Git;
- never copy secret files into the OVH payload;
- never write private keys into reports or manifests.
