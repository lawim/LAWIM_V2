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
- Retention: removes only verified obsolete artifacts.
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
- The timer under `deployment/systemd/` is still `daily`.
- Legacy production-oriented scripts still exist under `scripts/ops/` as historical references only.
- No validated full recovery has been recorded in this workspace.
