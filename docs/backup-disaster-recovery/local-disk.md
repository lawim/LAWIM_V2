# Local Disk

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Role

The local backup disk provides near-real-time recovery for recent files without downloading an archive.

## Identification

- UUID
- label
- mount point
- read permission
- write permission
- free space
- mount date

The mere existence of a directory does not prove that the disk is mounted.

## Policy target

- Replication interval: 5 to 10 minutes when the disk is connected
- Copy mode: incremental and non-destructive
- Recovery target: file, image, and recent document restore in minutes

## Current state

| Aspect | Target | Implemented | Deployed | Tested | Validated |
|---|---|---|---|---|---|
| Disk identification | Yes | Not yet | No | No | No |
| Free-space checks | Yes | Not yet | No | No | No |
| Incremental replication | Yes | Not yet | No | No | No |
| Safe restore of recent files | Yes | Not yet | No | No | No |

## Failure behavior

- If the disk is absent, local backup operations continue on other destinations.
- The absence is recorded as an alert, not as a fatal stop for the whole subsystem.

