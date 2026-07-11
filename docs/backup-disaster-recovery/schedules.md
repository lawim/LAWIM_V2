# Schedules

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Policy target

- Google Drive: 02:00 and 14:30, Africa/Douala
- Local replication: continuous or near-continuous when the disk is connected
- External disk: weekly offline copy
- Restore tests: daily checksum, weekly isolated PostgreSQL, monthly full restore, quarterly DR exercise

## Deployment status

STATUT : IMPLÉMENTATION CANONIQUE

The target policy is documented here. The versioned timer now matches the target schedule in the repository, but the live host still needs direct validation.

## Configuration versioned

| Task | Versioned mechanism | Target | Status | Last validation | Next validation | Responsible |
|---|---|---|---|---|---|---|
| Google Drive backup | `deployment/systemd/lawim-backup.timer` | 02:00 and 14:30 WAT | IMPLÉMENTÉ | Validated locally with `systemd-analyze calendar` | Awaiting live host confirmation | Backend + Ops |
| Local replication | Not yet declared in a validated unit | 5-10 minute target when connected | À DÉFINIR | Not validated | During provider implementation | Backend |
| External disk copy | Not yet declared in a validated unit | Weekly | À DÉFINIR | Not validated | During provider implementation | Backend + Ops |
| Checksum verification | Not yet declared in a validated unit | Daily | À DÉFINIR | Not validated | During scheduler implementation | Backend |
| PostgreSQL isolated restore | Not yet declared in a validated unit | Weekly | À DÉFINIR | Not validated | During restore service implementation | Backend |
| Full restore | Not yet declared in a validated unit | Monthly | À DÉFINIR | Not validated | During restore service implementation | Backend + Ops |
| DR exercise | Not yet declared in a validated unit | Quarterly | À DÉFINIR | Not validated | During DR program planning | Ops + Security |

## Configuration deployed

| Element | Deployed state | Evidence | Status | Last validation | Responsible |
|---|---|---|---|---|---|
| `lawim-backup.timer` | `OnCalendar=*-*-* 02:00:00 Africa/Douala` and `14:30:00 Africa/Douala` | `deployment/systemd/lawim-backup.timer` | DÉPLOYÉ À CONFIRMER | Validated locally with `systemd-analyze calendar` | Ops |
| `lawim-backup.service` | Calls `/opt/lawim/current/deployment/backup/backup.sh` | `deployment/systemd/lawim-backup.service` | DÉPLOYÉ À CONFIRMER | Not validated on a live host | Ops |
| Rehearsal backup script | Dry-run helper | `deployment/backup/backup.sh` | IMPLÉMENTÉ | Inspected locally | Backend |
| Rehearsal restore script | Dry-run helper | `deployment/backup/restore.sh` | IMPLÉMENTÉ | Inspected locally | Backend |

## Last verification

- Calendar syntax: validated in this workspace with `systemd-analyze calendar '02:00:00 Africa/Douala'` and `systemd-analyze calendar '14:30:00 Africa/Douala'`
- Deployed timer alignment: not validated
- Full restore: not validated

## Note d evolution

The schedules described in `reports/product_reviews/Mission_12_Report.md` correspond to the Mission 12 validated state.
The active policy is now documented in this file.
