#!/usr/bin/env bash
# LAWIM V2 — Production Backup Script
set -euo pipefail

BACKUP_ROOT="${LAWIM_BACKUP_ROOT:-/opt/lawim/backups}"
ENCRYPTION_KEY="${LAWIM_BACKUP_KEY:-}"
DRIVE_UPLOAD="${LAWIM_DRIVE_UPLOAD:-true}"

STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="${BACKUP_ROOT}/${STAMP}"
LOGFILE="${BACKUP_ROOT}/backup-${STAMP}.log"
exec > >(tee -a "$LOGFILE") 2>&1

log()  { echo "[$(date +%H:%M:%S)] $*"; }
fail() { log "FAILED: $*"; exit 1; }

RELEASE_NAME=$(basename "$(readlink -f /opt/lawim/current 2>/dev/null)" 2>/dev/null || echo "unknown")

log "=== LAWIM V2 Backup — ${STAMP} ==="
log "Release: ${RELEASE_NAME}"
mkdir -p "${BACKUP_DIR}"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

PG_CONTAINER=$(docker ps --filter "name=compose-postgres" --format "{{.Names}}" 2>/dev/null | head -1)
if [ -n "$PG_CONTAINER" ]; then
    log "Dumping PostgreSQL..."
    docker exec "$PG_CONTAINER" pg_dump -U lawim -d lawim_v2 --format=c --compress=9 \
        -f "/tmp/lawim-pg-${STAMP}.dump" 2>/dev/null || fail "pg_dump failed"
    docker cp "${PG_CONTAINER}:/tmp/lawim-pg-${STAMP}.dump" "${BACKUP_DIR}/postgres.dump"
    docker exec "$PG_CONTAINER" rm "/tmp/lawim-pg-${STAMP}.dump" 2>/dev/null || true
    PG_SIZE=$(stat -c%s "${BACKUP_DIR}/postgres.dump" 2>/dev/null || echo 0)
    log "PostgreSQL: $(numfmt --to=iec $PG_SIZE)"
fi

REDIS_CONTAINER=$(docker ps --filter "name=lawim-redis" --format "{{.Names}}" 2>/dev/null | head -1)
if [ -n "$REDIS_CONTAINER" ]; then
    log "Saving Redis state..."
    docker exec "$REDIS_CONTAINER" redis-cli SAVE 2>/dev/null || true
    docker cp "${REDIS_CONTAINER}:/data/dump.rdb" "${BACKUP_DIR}/redis.rdb" 2>/dev/null || true
    RDB_SIZE=$(stat -c%s "${BACKUP_DIR}/redis.rdb" 2>/dev/null || echo 0)
    log "Redis: $(numfmt --to=iec $RDB_SIZE)"
fi

log "Archiving files..."
FILE_ARCHIVE="${BACKUP_DIR}/files.tar.zst"
if command -v zstd &>/dev/null; then
    tar --zstd -cf "$FILE_ARCHIVE" -C /opt/lawim/shared/media . 2>/dev/null || true
else
    tar -czf "${BACKUP_DIR}/files.tar.gz" -C /opt/lawim/shared/media . 2>/dev/null || true
    FILE_ARCHIVE="${BACKUP_DIR}/files.tar.gz"
fi
FILE_SIZE=$(stat -c%s "$FILE_ARCHIVE" 2>/dev/null || echo 0)
log "Files: $(numfmt --to=iec $FILE_SIZE)"

log "Archiving configuration..."
tar --zstd -cf "${BACKUP_DIR}/configuration.tar.zst" \
    -C /opt/lawim/current compose/docker-compose.*.yml Dockerfile .env 2>/dev/null || true

cat > "${BACKUP_DIR}/release.json" <<EOF
{"release":"${RELEASE_NAME}","hostname":"$(hostname)","application_version":"2.0"}
EOF

if [ -n "$ENCRYPTION_KEY" ]; then
    log "Encrypting archives..."
    for f in "${BACKUP_DIR}"/*.dump "${BACKUP_DIR}"/*.tar.zst "${BACKUP_DIR}"/*.tar.gz "${BACKUP_DIR}"/*.rdb; do
        [ -f "$f" ] || continue
        openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 \
            -in "$f" -out "${f}.enc" -pass "pass:${ENCRYPTION_KEY}"
        rm -f "$f"
    done
    log "Encryption complete"
else
    log "WARNING: No encryption key. Archives UNENCRYPTED."
fi

log "Computing SHA256 checksums..."
(cd "${BACKUP_DIR}" && sha256sum * > checksums.sha256 && sha256sum -c checksums.sha256) || fail "Checksum failed"

COMPLETED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
BACKUP_SIZE=$(du -sb "${BACKUP_DIR}" | cut -f1)
cat > "${BACKUP_DIR}/manifest.json" <<EOF
{
  "backup_id": "${STAMP}",
  "started_at": "${STARTED_AT}",
  "completed_at": "${COMPLETED_AT}",
  "environment": "production",
  "hostname": "$(hostname)",
  "release": "${RELEASE_NAME}",
  "backup_type": "full",
  "total_size": ${BACKUP_SIZE},
  "encryption": "$([ -n "$ENCRYPTION_KEY" ] && echo 'aes-256-cbc' || echo 'none')",
  "checksum_algorithm": "sha256",
  "status": "completed"
}
EOF

if [ "$DRIVE_UPLOAD" = "true" ] && command -v rclone &>/dev/null; then
    RCLONE_CONFIG="${RCLONE_CONFIG:-/home/ubuntu/.config/rclone/rclone.conf}"
    DRIVE_PATH="LAWIM_Backups/production/$(date +%Y)/$(date +%m)/${STAMP}"
    log "Uploading to Google Drive: ${DRIVE_PATH} ..."
    rclone --config "$RCLONE_CONFIG" mkdir "lawim-drive:${DRIVE_PATH}" 2>/dev/null || true
    rclone --config "$RCLONE_CONFIG" copy "${BACKUP_DIR}" "lawim-drive:${DRIVE_PATH}" \
        --progress --checksum \
        2>&1 | tail -3 || log "WARNING: Drive upload failed"
    log "Upload complete"
fi

log "Applying retention..."
PYTHONPATH=/opt/lawim/current/code python3 -c "
import os, re, time, shutil
root = '${BACKUP_ROOT}'
now = time.time()
for b in sorted(os.listdir(root)):
    bdir = os.path.join(root, b)
    if not os.path.isdir(bdir) or not re.match(r'^\d{8}_\d{6}$', b):
        continue
    mtime = os.path.getmtime(bdir)
    age_h = (now - mtime) / 3600
    if age_h < 48: continue
    shutil.rmtree(bdir)
    print(f'Removed: {b}')
" 2>&1 || log "WARNING: Retention failed"

log "=== Backup complete: ${BACKUP_DIR} ==="
log "Size: $(du -sh ${BACKUP_DIR} | cut -f1)"
