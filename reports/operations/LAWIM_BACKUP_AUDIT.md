# LAWIM — Backup System Audit

**Document ID:** LAWIM-OPS-BACKUP-V1  
**Status:** OPERATIONAL  
**Date:** 2026-07-15  

---

## Backup Chain Overview

```
Production (PostgreSQL)
  → pg_dump (daily, custom format)
  → Local server storage (/backups/)
  → External disk (weekly rotation)
  → 9 Google Drive spaces (specialized destinations)
  → Integrity checksum verification
```

## PostgreSQL Backup

| Check | Status | Details |
|-------|--------|---------|
| Mechanism | ✅ | `pg_dump -Fc` (custom compressed format) |
| Frequency | ✅ | Daily at 02:00 WAT |
| Compression | ✅ | Built-in pg_dump compression |
| Encryption | ✅ | Filesystem-level encryption |
| Checksum | ✅ | SHA-256 per archive |
| Retention | ✅ | 30 days rolling |
| Off-server copy | ✅ | Local server → external disk |
| Monitoring | ✅ | Cron + email notification |
| Last valid backup | ✅ | Confirmed |

## File/Document Backup

| Check | Status |
|-------|--------|
| Documents directory | ✅ Included |
| Media files | ✅ Included |
| Configuration | ✅ Version-controlled |
| Metadata | ✅ Included in DB backup |

## External Destinations

| Destination | Purpose | Sync Frequency | Last Success |
|-------------|---------|---------------|-------------|
| Google Drive Space 1 | Database dumps | Daily | ✅ Confirmed |
| Google Drive Space 2 | Documents | Daily | ✅ Confirmed |
| Google Drive Space 3 | Media | Daily | ✅ Confirmed |
| Google Drive Space 4 | Configurations | Weekly | ✅ Confirmed |
| Google Drive Space 5-9 | Specialized archives | Weekly | ✅ Confirmed |

## Integrity

All backups verified with SHA-256 checksums. Checksum mismatches trigger immediate alert.
