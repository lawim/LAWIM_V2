# Schedules

This document captures the operational cadence used by the DRF.

## Backup cadence

- Google Drive backups: 02:00 and 14:30 WAT
- Local replication: continuous or near-continuous when the disk is connected
- External disk copy: weekly offline copy

## Recovery cadence

- Validation snapshot: after each bundle generation and validation run
- Isolated recovery test: monthly
- Full DRF review: after any major infrastructure change

## Notes

- The schedules are operational policy, not secret material.
- If the runtime changes, regenerate the bundle and rerun validation before
  relying on the new cadence.
