#!/usr/bin/env bash
set -euo pipefail

BACKUP_ROOT="${BACKUP_ROOT:-${LAWIM_BACKUP_ROOT:-/var/backups/lawim}}"
BACKUP_ID="${BACKUP_ID:-LAWIM-PROD-$(date +%Y%m%d-%H%M%S)}"
BACKUP_DIR="$BACKUP_ROOT/$BACKUP_ID"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# --- Configuration ---
PG_HOST="${PG_HOST:-localhost}"
PG_PORT="${PG_PORT:-5432}"
PG_USER="${PG_USER:-lawim}"
PG_DB="${PG_DB:-lawim}"
PG_PASSWORD="${PG_PASSWORD:-}"
RCLONE_REMOTE="${RCLONE_REMOTE:-gdrive}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-90}"

mkdir -p "$BACKUP_DIR"

echo "=== LAWIM V2 Production Backup ==="
echo "Backup ID  : $BACKUP_ID"
echo "Timestamp  : $TIMESTAMP"
echo "Target     : $BACKUP_DIR"

# --- Database backup ---
DB_DUMP_FILE="$BACKUP_DIR/lawim_prod_${BACKUP_ID}.sql.gz"
if [ -n "$PG_PASSWORD" ]; then
    export PGPASSWORD="$PG_PASSWORD"
fi
echo "Backing up PostgreSQL database..."
if pg_dump -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" --no-owner --no-acl 2>/dev/null | gzip > "$DB_DUMP_FILE"; then
    echo "Database backup: OK ($DB_DUMP_FILE)"
else
    echo "ERROR: Database backup failed"
    rm -rf "$BACKUP_DIR"
    exit 1
fi
unset PGPASSWORD

# --- Configuration backup ---
CONFIG_BACKUP_DIR="$BACKUP_DIR/config"
mkdir -p "$CONFIG_BACKUP_DIR"
if [ -d "/opt/lawim" ]; then
    cp -r /opt/lawim/* "$CONFIG_BACKUP_DIR/" 2>/dev/null || true
fi

# --- Manifest ---
DB_DUMP_SIZE=$(stat -c%s "$DB_DUMP_FILE" 2>/dev/null || echo 0)
DB_DUMP_CHECKSUM=$(sha256sum "$DB_DUMP_FILE" | cut -d' ' -f1)

cat > "$BACKUP_DIR/manifest.txt" <<EOF
LAWIM V2 Production Backup
Backup-ID: $BACKUP_ID
Timestamp: $TIMESTAMP
Source: ${PG_HOST}:${PG_PORT}/${PG_DB}
Dump-File: $(basename "$DB_DUMP_FILE")
Dump-Size-Bytes: $DB_DUMP_SIZE
Dump-Checksum-SHA256: $DB_DUMP_CHECKSUM
Schema-Version: $(PGPASSWORD="${PG_PASSWORD:-}" psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" -t -c "SELECT MAX(version) FROM _schema_registry;" 2>/dev/null || echo "unknown")
Retention-Days: $BACKUP_RETENTION_DAYS
EOF

echo "Manifest: $BACKUP_DIR/manifest.txt"
cat "$BACKUP_DIR/manifest.txt"

# --- Retention cleanup ---
find "$BACKUP_ROOT" -maxdepth 1 -type d -name "LAWIM-PROD-*" -mtime +$BACKUP_RETENTION_DAYS -exec rm -rf {} \; 2>/dev/null || true

# --- Remote sync (if enabled) ---
if [ "${BACKUP_REMOTE_ENABLED:-false}" = "true" ] && command -v rclone &>/dev/null; then
    echo "Syncing to remote: $RCLONE_REMOTE"
    rclone sync "$BACKUP_DIR" "$RCLONE_REMOTE:lawim-backups/$BACKUP_ID" --progress 2>&1 || echo "WARNING: Remote sync failed"
fi

echo "=== Backup complete: $BACKUP_ID ==="
echo "Restore command: ./deployment/backup/restore.sh $BACKUP_ID"
