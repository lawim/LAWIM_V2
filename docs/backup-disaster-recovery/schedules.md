# Schedules

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Policy target

- Google Drive: 02:00 and 14:30, Africa/Douala
- Local replication: continuous or near-continuous when the disk is connected
- External disk: weekly offline copy
- Restore tests: daily checksum, weekly isolated PostgreSQL, monthly full restore, quarterly DR exercise

## Deployment status

STATUT : A DEPLOYER

The target policy is documented here, but the versioned timer is still `daily` and is not yet aligned to the active target schedule.

## Configuration versioned

| Task | Versioned mechanism | Target | Status | Last validation | Next validation | Responsible |
|---|---|---|---|---|---|---|
| Google Drive backup | `deployment/systemd/lawim-backup.timer` | 02:00 and 14:30 WAT | A DEPLOYER | Not validated | After timer alignment | Backend + Ops |
| Local replication | Not yet declared in a validated unit | 5-10 minute target when connected | A DEFINIR | Not validated | During provider implementation | Backend |
| External disk copy | Not yet declared in a validated unit | Weekly | A DEFINIR | Not validated | During provider implementation | Backend + Ops |
| Checksum verification | Not yet declared in a validated unit | Daily | A DEFINIR | Not validated | During scheduler implementation | Backend |
| PostgreSQL isolated restore | Not yet declared in a validated unit | Weekly | A DEFINIR | Not validated | During restore service implementation | Backend |
| Full restore | Not yet declared in a validated unit | Monthly | A DEFINIR | Not validated | During restore service implementation | Backend + Ops |
| DR exercise | Not yet declared in a validated unit | Quarterly | A DEFINIR | Not validated | During DR program planning | Ops + Security |

## Configuration deployed

| Element | Deployed state | Evidence | Status | Last validation | Responsible |
|---|---|---|---|---|---|
| `lawim-backup.timer` | `OnCalendar=daily` | `deployment/systemd/lawim-backup.timer` | A DEPLOYER | Not validated on a live host | Ops |
| `lawim-backup.service` | Calls `/opt/lawim/deployment/backup/backup.sh` | `deployment/systemd/lawim-backup.service` | A DEPLOYER | Not validated on a live host | Ops |
| Rehearsal backup script | Dry-run helper | `deployment/backup/backup.sh` | IMPLEMENTE | Inspected locally | Backend |
| Rehearsal restore script | Dry-run helper | `deployment/backup/restore.sh` | IMPLEMENTE | Inspected locally | Backend |

## Last verification

- Calendar syntax: validated in this workspace with `TZ=Africa/Douala systemd-analyze calendar '02:00:00'` and `TZ=Africa/Douala systemd-analyze calendar '14:30:00'`
- Deployed timer alignment: not validated
- Full restore: not validated

## Note d evolution

The schedules described in `reports/product_reviews/Mission_12_Report.md` correspond to the Mission 12 validated state.
The active policy is now documented in this file.
