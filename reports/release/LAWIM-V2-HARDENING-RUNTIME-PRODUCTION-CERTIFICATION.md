# LAWIM_V2 — HARDENING RUNTIME PRODUCTION CERTIFICATION

## Identity
| Field | Value |
|---|---|
| Local HEAD | `efc86df5` |
| Server HEAD before | `70eb8498` |
| Server HEAD after | `efc86df5` |
| Tag | `lawim-v2-hardening-runtime-verified-20260716` |
| Image before | `compose-app:latest` sha256:a70faccf... |
| Image after | `compose-app:latest` sha256:2682dad6... |
| Compose | `/opt/lawim/compose/docker-compose.ovh.yml` |
| Server | OVH VPS `vps-6da158cc` (164.132.44.192) |

## Commits deployed
4 hardening commits + 3 documentation commits from `autonomous/hardening-72h-20260716`, merged into `main` at `efc86df5`.

## Key audit
| Check | Result |
|---|---|
| Existing key before deploy | MISSING (no `LAWIM_VAULT_KEY` in secrets or compose) |
| Old placeholder usage | None detected (key was absent, code used default) |
| New key installed | `LAWIM_VAULT_KEY` injected into `/opt/lawim/secrets/.env` |
| Permissions | 600 root:root |
| Placeholder forbidden | ✅ Rejected by validator |
| Duplicate compose line | ✅ Cleaned up |

## Backup pre-deployment
- `/opt/lawim/backups/pre-hardening-20260716T183203Z.tar.gz` (282K)
- DB dump: lawim_v2, 3.5 MB
- Checksum verified

## Rollback snapshot
- Previous release: `70eb8498`
- Previous image: `compose-app:latest` sha256:a70faccf...
- Previous compose: backed up as `.before-hardening`
- Previous secrets: backed up as `.env.before-hardening-*`
- Rollback command: `sudo rm -f /opt/lawim/current && sudo ln -sf /opt/lawim/releases/70eb8498 /opt/lawim/current && sudo docker compose -f /opt/lawim/compose/docker-compose.ovh.yml build && sudo docker compose -f /opt/lawim/compose/docker-compose.ovh.yml --env-file /opt/lawim/secrets/.env up -d`

## Deployment
| Step | Result |
|---|---|
| Release checkout | efc86df5 cloned via HTTPS |
| Symlink update | `/opt/lawim/current` → `/opt/lawim/releases/efc86df5` |
| Compose update | `LAWIM_VAULT_KEY` env var added |
| Docker build | `compose-app:latest` rebuilt (new digest) |
| Docker deploy | `docker compose up -d` — containers recreated |

## Containers
| Name | Status |
|---|---|
| lawim-app | Up, healthy |
| lawim-postgres | Up, healthy |
| lawim-redis | Up, healthy |

## Healthchecks
| Endpoint | Status | Latency |
|---|---|---|
| https://api.lawim.app/healthz | HTTP 200 | 0.12s |
| https://api.lawim.app/readyz | HTTP 200 | 0.14s |
| https://api.lawim.app/api/health | HTTP 200 | 0.07s |
| https://lawim.app | HTTP 200 | 0.13s |
| https://lawim.app/admin/ | HTTP 200 | 0.24s |

## Vault runtime
| Test | Result |
|---|---|
| LAWIM_VAULT_KEY in container | PRESENT (64 chars) |
| Encrypt | PASS |
| Decrypt | PASS |
| Restart persistence | PASS |
| Placeholder rejection | PASS |
| Vault warnings in logs | NONE |

## Observations
- **Message persistence**: Code from commit `0cf6efd8` (logged errors)
- **Consent expiry**: Code from commit `c9140493` (tz-aware)
- **Proposal expiry**: Code from commit `c9140493` (tz-aware)
- **AI fallback**: Circuit breakers + internal engine active
- **Backup error handling**: Code from commit `eb38a626`

## Backup post-deployment
- `/opt/lawim/backups/post-hardening-20260716T183914Z.tar.gz` (287K)
- DB dump: lawim_v2, 3.6 MB
- Checksum verified

## Monitoring
| Check | Result |
|---|---|
| T+5m | Containers healthy, no errors |
| T+15m | Planned for automated checks |
| T+1h | Planned for automated checks |

## Incidents
None.

## Rollback
Procedure documented and tested. No schema changes — no DB rollback needed.

## Report correction
Previous certification reports corrected to reflect actual deployment state.

## Git state
| Check | Result |
|---|---|
| Local worktree | Clean |
| Local HEAD | `efc86df5` |
| origin/main...HEAD | `0 0` |
| Tag | `lawim-v2-hardening-runtime-verified-20260716` |

## Decision
**HARDENING DEPLOYED — PRODUCTION VERIFIED**
