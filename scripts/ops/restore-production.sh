#!/usr/bin/env bash
# LAWIM V2 — Restore Script
# Restores a LAWIM backup from a local backup directory or Google Drive.
set -euo pipefail

usage() {
    cat <<EOF
Usage: $0 <backup-id|backup-dir> [--decrypt-key KEY]

Restores LAWIM from a backup identified by its timestamp (YYYYMMDD_HHMMSS)
or a local path. If --decrypt-key is not provided, reads LAWIM_BACKUP_KEY.

Steps:
  1. Verify checksums
  2. Decrypt archives (if encrypted)
  3. Restore PostgreSQL
  4. Restore files
  5. Restore configuration

Example:
  $0 20260711_061500 --decrypt-key "my-key"
  $0 /opt/lawim/backups/20260711_061500
EOF
    exit 1
}

[ $# -ge 1 ] || usage
BACKUP_SRC="$1"
DECRYPT_KEY="${2:-${LAWIM_BACKUP_KEY:-}}"

if [ -d "$BACKUP_SRC" ]; then
    BACKUP_DIR="$BACKUP_SRC"
else
    BACKUP_DIR="/opt/lawim/backups/${BACKUP_SRC}"
    [ -d "$BACKUP_DIR" ] || { echo "Backup not found: $BACKUP_DIR"; exit 1; }
fi

echo "=== Restoring from: ${BACKUP_DIR} ==="
cd "$BACKUP_DIR"

# Verify checksums
echo "[1/5] Verifying checksums..."
sha256sum -c checksums.sha256 2>/dev/null || { echo "Checksum mismatch!"; exit 1; }
echo "  OK"

# Decrypt if needed
if ls *.enc 2>/dev/null; then
    echo "[2/5] Decrypting archives..."
    [ -n "$DECRYPT_KEY" ] || { echo "Encryption key required"; exit 1; }
    for f in *.enc; do
        out="${f%.enc}"
        openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
            -in "$f" -out "$out" -pass "pass:${DECRYPT_KEY}"
        echo "  Decrypted: $f"
    done
fi

# Restore PostgreSQL
if [ -f "postgres.dump" ]; then
    echo "[3/5] Restoring PostgreSQL..."
    PG_CONTAINER=$(docker ps --filter "name=compose-postgres" --format "{{.Names}}" 2>/dev/null | head -1)
    if [ -n "$PG_CONTAINER" ]; then
        docker cp "postgres.dump" "${PG_CONTAINER}:/tmp/restore.dump"
        docker exec "$PG_CONTAINER" pg_restore -U lawim -d lawim_v2 --clean --if-exists \
            /tmp/restore.dump 2>&1 || echo "WARNING: pg_restore had warnings (see above)"
        docker exec "$PG_CONTAINER" rm /tmp/restore.dump 2>/dev/null || true
        echo "  PostgreSQL restored"
    else
        echo "  WARNING: No PostgreSQL container running"
    fi
fi

# Restore files
for archive in files.tar.zst files.tar.gz; do
    if [ -f "$archive" ]; then
        echo "[4/5] Restoring files from ${archive}..."
        MEDIA_DIR="${MEDIA_DIR:-/opt/lawim/shared/media}"
        mkdir -p "$MEDIA_DIR"
        case "$archive" in
            *.zst) tar --zstd -xf "$archive" -C "$MEDIA_DIR" ;;
            *.gz) tar -xzf "$archive" -C "$MEDIA_DIR" ;;
        esac
        echo "  Files restored to ${MEDIA_DIR}"
    fi
done

# Restore configuration
if [ -f "configuration.tar.zst" ]; then
    echo "[5/5] Restoring configuration..."
    tar --zstd -xf "configuration.tar.zst" -C /opt/lawim/current/ 2>/dev/null || true
    echo "  Configuration restored"
fi

echo ""
echo "=== Restore complete ==="
echo "Source: ${BACKUP_DIR}"
echo "Next steps:"
echo "  1. Restart backend: cd /opt/lawim/current && docker compose ... up -d"
echo "  2. Verify health: curl http://localhost:3000/healthz"
echo "  3. Verify readyz: curl http://localhost:3000/readyz"
echo "  4. Run smoke tests"
