#!/usr/bin/env bash
# LAWIM V2 — Restore Backup Locally
# Downloads a backup from Google Drive and restores it to local Docker.
set -euo pipefail

usage() {
    echo "Usage: $0 <backup-id> [--decrypt-key KEY]"
    echo "Backup ID format: YYYYMMDD_HHMMSS (from manifest.json)"
    exit 1
}

[ $# -ge 1 ] || usage
BACKUP_ID="$1"
DECRYPT_KEY="${2:-${LAWIM_BACKUP_KEY:-}}"
RCLONE_REMOTE="${RCLONE_REMOTE:-lawim-drive}"
RCLONE_PATH="${RCLONE_PATH:-LAWIM_Backups/production}"

RESTORE_DIR="/tmp/lawim-restore-${BACKUP_ID}"

echo "=== Restoring local LAWIM from backup: ${BACKUP_ID} ==="

# Find backup in Google Drive
echo "[1/5] Finding backup in Google Drive..."
BACKUP_REMOTE="${RCLONE_REMOTE}:${RCLONE_PATH}/$(echo $BACKUP_ID | cut -c1-4)/$(echo $BACKUP_ID | cut -c5-6)/${BACKUP_ID}"

if rclone ls "${BACKUP_REMOTE}" 2>/dev/null | head -5; then
    echo "Found in Drive. Downloading..."
    rclone copy "${BACKUP_REMOTE}" "${RESTORE_DIR}" --progress
else
    echo "Not in Drive. Checking local cache..."
    if [ -d "/opt/lawim/backups/${BACKUP_ID}" ]; then
        echo "Found locally."
        cp -r "/opt/lawim/backups/${BACKUP_ID}" "${RESTORE_DIR}"
    elif [ -d "/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/backups/${BACKUP_ID}" ]; then
        echo "Found in local workspace."
        cp -r "$_LAWIM_ROOT/backups/${BACKUP_ID}" "${RESTORE_DIR}"
    else
        echo "Backup not found anywhere."
        echo "Expected: ${BACKUP_REMOTE}"
        exit 1
    fi
fi

echo "[2/5] Verifying checksums..."
(cd "${RESTORE_DIR}" && sha256sum -c checksums.sha256) || {
    echo "Checksum mismatch! Aborting."
    exit 1
}

echo "[3/5] Decrypting..."
if ls "${RESTORE_DIR}"/*.enc 2>/dev/null; then
    [ -n "$DECRYPT_KEY" ] || { echo "Encryption key required"; exit 1; }
    for f in "${RESTORE_DIR}"/*.enc; do
        out="${f%.enc}"
        openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
            -in "$f" -out "$out" -pass "pass:${DECRYPT_KEY}"
    done
fi

echo "[4/5] Restoring PostgreSQL..."
if [ -f "${RESTORE_DIR}/postgres.dump" ]; then
    PG_CONTAINER=$(docker ps --filter "name=compose-postgres" --format "{{.Names}}" 2>/dev/null | head -1)
    if [ -n "$PG_CONTAINER" ]; then
        docker cp "${RESTORE_DIR}/postgres.dump" "${PG_CONTAINER}:/tmp/restore.dump"
        docker exec "$PG_CONTAINER" pg_restore -U lawim -d lawim_v2 --clean --if-exists /tmp/restore.dump || true
        docker exec "$PG_CONTAINER" rm /tmp/restore.dump 2>/dev/null || true
        echo "✓ PostgreSQL restored"
    fi
fi

echo "[5/5] Restoring files..."
for archive in "${RESTORE_DIR}"/files.tar.*; do
    [ -f "$archive" ] || continue
    MEDIA_DIR="${LAWIM_MEDIA_DIR:-media}"
    mkdir -p "$MEDIA_DIR"
    case "$archive" in
        *.zst) tar --zstd -xf "$archive" -C "$MEDIA_DIR" 2>/dev/null || true ;;
        *.gz) tar -xzf "$archive" -C "$MEDIA_DIR" 2>/dev/null || true ;;
    esac
done

echo ""
echo "=== Restore complete ==="
echo "Data restored from: ${RESTORE_DIR}"
echo "Verify: curl http://localhost:3000/api/health"
echo "Cleanup: rm -rf ${RESTORE_DIR}"
