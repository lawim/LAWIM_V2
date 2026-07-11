# Backup & Disaster Recovery

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Objectif

This tree is the single source of truth for LAWIM backup, restore, retention, disaster recovery, and operator control.
It separates the target policy, the current runtime contract, and the validation criteria used before any operational change.

## Active policy

- Google Drive: 02:00 and 14:30 WAT
- Timezone: Africa/Douala
- Local disk backup: continuous or near-continuous when the disk is connected
- External disk: weekly offline copy
- Cockpit LAWIM: control, history, alerts, and operator actions

## Current state

- Versioned helper files live in `deployment/backup/`.
- Versioned systemd units live in `deployment/systemd/`.
- The declared deployed backup path is `/opt/lawim/current/deployment/backup/backup.sh`.
- Live host validation is still pending because `systemctl` is not available in this workspace.
- The dedicated backend backup module skeleton is present, but persistence and cockpit wiring still need to be completed.

## Components status

| Component | Target | Implemented | Deployed | Tested | Validated |
|---|---|---|---|---|---|
| PostgreSQL backup | Yes | Partial | Not confirmed | Rehearsal helper | No |
| Media backup | Yes | Partial | Not confirmed | Rehearsal helper | No |
| Encryption | Yes | Partial | Not confirmed | Script support only | No |
| Checksums | Yes | Partial | Not confirmed | Rehearsal helper | No |
| Google Drive | Yes | Partial | Not confirmed | No | No |
| Local disk | Yes | Not yet | Not yet | No | No |
| External disk | Yes | Not yet | Not yet | No | No |
| Cockpit | Yes | Not yet | Not yet | No | No |
| Alerts | Yes | Partial | Not confirmed | No | No |
| Restore | Yes | Partial | Not confirmed | Rehearsal helper | No |
| Retention | Yes | Partial | Not confirmed | Not confirmed | No |
| Automated tests | Yes | Partial | Not confirmed | Not confirmed | No |

## Canonical documents

- [Architecture](architecture.md)
- [Operations](operations.md)
- [Schedules](schedules.md)
- [Storage providers](storage-providers.md)
- [Google Drive](google-drive.md)
- [Local disk](local-disk.md)
- [External disk](external-disk.md)
- [Encryption](encryption.md)
- [Retention](retention.md)
- [Monitoring and alerts](monitoring-alerts.md)
- [Cockpit](cockpit.md)
- [Restore database](restore-database.md)
- [Restore media](restore-media.md)
- [Restore complete](restore-complete.md)
- [Disaster recovery plan](disaster-recovery-plan.md)
- [Incident response](incident-response.md)
- [Restore tests](restore-tests.md)
- [Maintenance](maintenance.md)
- [Troubleshooting](troubleshooting.md)
- [Audit checklist](audit-checklist.md)

## Safety rules

- Do not document secrets here.
- Do not assert a deployed path unless it is confirmed by a host audit.
- Do not confuse target, implemented, deployed, tested, and validated.
- Do not add backup artifacts to Git.

## Validation criteria

- The target schedule is documented and distinguishable from the deployed timer.
- The canonical documents do not repeat removed paths.
- The README root points here.
- No secret or backup artifact is added to Git.
