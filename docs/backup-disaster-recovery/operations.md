# Operations

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Purpose

This document explains how the BDR documentation set is used operationally.
It is not a backup procedure by itself. It is the reading order and responsibility map.

## Operating model

1. Read `schedules.md` before touching any timer or cron-like behavior.
2. Read `google-drive.md`, `local-disk.md`, and `external-disk.md` before touching any storage provider.
3. Read `restore-database.md`, `restore-media.md`, and `restore-complete.md` before any restore attempt.
4. Use `cockpit.md` as the operator-facing control surface target.
5. Use `monitoring-alerts.md` for health, alerts, and metrics vocabulary.

## Responsibilities

- Backup service: creates backup artifacts and manifests.
- Provider layer: stores, retrieves, verifies, and reports availability.
- Scheduler: runs planned jobs.
- Retention: removes only verified expired or superseded artifacts.
- Restore service: restores isolated or complete environments.
- Cockpit: displays state and executes permitted actions only.

## Status vocabulary

- `CIBLE`: the required end state.
- `IMPLEMENTE`: present in code or documentation, but not necessarily deployed.
- `DEPLOYE`: present on the target runtime and confirmed.
- `TESTE`: exercised in a controlled test.
- `VALIDE`: exercised and accepted against the documented criteria.

## Current operational reality

- The versioned backup helpers under `deployment/backup/` are rehearsal-safe and do not prove the final production design.
- The timer under `deployment/systemd/` is aligned with the active schedule in the repository, but the live host remains unvalidated.
- The declared deployed path is `/opt/lawim/current/deployment/backup/backup.sh`.
- No validated full recovery has been recorded in this workspace.

## OVH deployment path

Use `deployment/backup/install-systemd.sh` once the host has been audited:

1. Install the systemd units from `deployment/systemd/`.
2. Back up any existing unit files before replacing them.
3. Run `systemd-analyze verify` on the installed units.
4. Reload systemd with `daemon-reload`.
5. Enable only the validated timers.
6. Inspect the next trigger times before enabling any destructive restore workflow.

Do not enable local or external disk timers until the corresponding storage path, UUID, label, and permissions have been validated on the server.
