# Backup & Disaster Recovery

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Objectif

This tree is the canonical documentation for LAWIM backup, restore, retention, disaster recovery, and operator control.
It separates:

- the target policy;
- the current runtime reality;
- the historical references kept for traceability;
- the validation criteria used before any operational change.

## Politique officielle

- Google Drive: 02:00 and 14:30
- Timezone: Africa/Douala
- Local disk backup: continuous or near-continuous when the disk is connected
- External disk: weekly offline copy
- Cockpit LAWIM: control, history, alerts, and operator actions

## Etat reel actuel

The repository currently contains:

- versioned rehearsal helpers under `deployment/backup/`;
- a versioned systemd timer and service under `deployment/systemd/`;
- legacy production-oriented scripts under `scripts/ops/` kept for historical traceability only;
- historical reports describing Mission 12 and earlier backup states.

Current gaps:

- the versioned timer is still `daily`, not aligned with the target schedule;
- the runtime path declared by the unit file is not validated on this host;
- no full restore has been validated in this workspace;
- the Cockpit BDR module is still to be implemented.

## Components status

| Composant | Cible | Implante | Deploie | Teste | Valide |
|---|---|---|---|---|---|
| Sauvegarde PostgreSQL | Oui | Partiel | Non confirme | Dry-run only | Non |
| Medias | Oui | Partiel | Non confirme | Dry-run only | Non |
| Chiffrement | Oui | Partiel | Legacy script only | Non confirme | Non |
| Checksums | Oui | Partiel | Non confirme | Dry-run only | Non |
| Google Drive | Oui | Partiel | Non confirme | Non | Non |
| Disque local | Oui | Non | Non | Non | Non |
| Disque externe | Oui | Non | Non | Non | Non |
| Cockpit | Oui | Non | Non | Non | Non |
| Alertes | Oui | Partiel | Non confirme | Non | Non |
| Restauration | Oui | Partiel | Non confirme | Dry-run only | Non |
| Retention | Oui | Partiel | Non confirme | Non confirme | Non |
| Tests automatiques | Oui | Partiel | Non confirme | Non confirme | Non |

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
- [Consolidation matrix](CONSOLIDATION_MATRIX.md)

## Safety rules

- No secret is documented here.
- No path is asserted as deployed unless it is verified by the versioned runtime or by a validated server audit.
- Historical documents remain traceable, but the active policy is documented only in this tree.
- Do not confuse target, implemented, deployed, tested, and validated.

## Validation criteria

- The target schedule is documented and distinguishable from the deployed timer.
- The canonical documents do not repeat legacy text unnecessarily.
- The README root points here.
- Historical documents point back here.
- No secret or backup artifact is added to Git.
