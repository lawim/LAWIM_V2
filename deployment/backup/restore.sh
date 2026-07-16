#!/usr/bin/env bash
set -euo pipefail

RESTORE_ID="${1:-}"
BACKUP_ROOT="${BACKUP_ROOT:-${LAWIM_BACKUP_ROOT:-/var/backups/lawim}}"
PG_HOST="${PG_HOST:-localhost}"
PG_PORT="${PG_PORT:-5432}"
PG_USER="${PG_USER:-lawim}"
PG_DB="${PG_DB:-lawim}"
PG_PASSWORD="${PG_PASSWORD:-}"

if [ -z "$RESTORE_ID" ]; then
    echo "Usage: $0 <backup-id>"
    echo ""
    echo "Available backups:"
    ls -1 "$BACKUP_ROOT" 2>/dev/null | grep "LAWIM-PROD-" || echo "(none found in $BACKUP_ROOT)"
    exit 1
fi

BACKUP_DIR="$BACKUP_ROOT/$RESTORE_ID"
MANIFEST="$BACKUP_DIR/manifest.txt"

if [ ! -f "$MANIFEST" ]; then
    echo "ERROR: Backup not found: $BACKUP_DIR"
    exit 1
fi

echo "=== LAWIM V2 Restore ==="
echo "Restore ID: $RESTORE_ID"
echo "Manifest  : $MANIFEST"
echo ""
cat "$MANIFEST"
echo ""

# --- Verification ---
DB_DUMP_FILE=$(ls "$BACKUP_DIR"/*.sql.gz 2>/dev/null | head -1)
if [ -z "$DB_DUMP_FILE" ]; then
    echo "ERROR: No database dump found in $BACKUP_DIR"
    exit 1
fi

echo "Verifying checksum..."
STORED_CHECKSUM=$(grep "Dump-Checksum-SHA256:" "$MANIFEST" | cut -d' ' -f2)
ACTUAL_CHECKSUM=$(sha256sum "$DB_DUMP_FILE" | cut -d' ' -f1)

if [ "$STORED_CHECKSUM" != "$ACTUAL_CHECKSUM" ]; then
    echo "ERROR: Checksum mismatch!"
    echo "  Stored: $STORED_CHECKSUM"
    echo "  Actual: $ACTUAL_CHECKSUM"
    exit 1
fi
echo "Checksum: OK"

if [ -n "$PG_PASSWORD" ]; then
    export PGPASSWORD="$PG_PASSWORD"
fi

echo ""
echo "WARNING: This will OVERWRITE the current database ($PG_DB)."
echo "Target: ${PG_HOST}:${PG_PORT}/${PG_DB}"
echo ""
echo "To execute, uncomment the restore command below:"
echo ""
echo "# psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c \"DROP SCHEMA public CASCADE; CREATE SCHEMA public;\""
echo "# gunzip -c \"$DB_DUMP_FILE\" | psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB"
echo ""
echo "=== Restore rehearsal complete ==="
echo "No data was modified."
unset PGPASSWORD
