# Architecture

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Target flow

```text
PostgreSQL + medias
        |
        +-- creation locale verifiee
        |
        +-- chiffrement
        |
        +-- checksums
        |
        +-- Google Drive 02:00 / 14:30
        |
        +-- replication disque local
        |
        +-- copie disque externe hebdomadaire
        |
        +-- supervision Cockpit
```

## Layers

- LAWIM application data
- Backup orchestration
- Storage providers
- Verification and restore
- Cockpit supervision

## Sources of truth

| Source | Role |
|---|---|
| Application configuration | Non-sensitive runtime parameters |
| Versioned systemd units | Declared schedule and service wiring |
| `deployment/backup/` | Versioned rehearsal/runtime helper files |
| Manifest files | Backup identity and verification trace |
| Logs | Operational evidence and failures |
| Cockpit | Operator-facing state and actions |

## Runtime vs documentation

- Repository path: `deployment/backup/`
- Declared deployment path in the current service file: `/opt/lawim/current/deployment/backup/backup.sh`
- Current local audit result: `systemctl` access is not available in this workspace, so the deployed state is not confirmed here
- Therefore, this document treats the deployed path as declared but not validated

## Current state

- The versioned backup helpers are simple rehearsal utilities.
- The versioned timer is aligned with the target policy in the repository, but the live deployment remains unconfirmed.
- Provider abstraction is still documented conceptually and not yet delivered as a dedicated module.
