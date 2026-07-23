#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="deployment/backup"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_PATH="${BACKUP_DIR}/lawim-backup-${TIMESTAMP}"
DB_BACKUP="${BACKUP_PATH}/database.sql.gz"
CONFIG_BACKUP="${BACKUP_PATH}/config.tar.gz"
EVIDENCE_BACKUP="${BACKUP_PATH}/evidence.tar.gz"

mkdir -p "${BACKUP_PATH}"

echo "[$(date -Iseconds)] Starting LAWIM backup to ${BACKUP_PATH}"

echo "[$(date -Iseconds)] Backing up PostgreSQL..."
docker exec lawim-db pg_dump -U lawim lawim_v3 | gzip > "${DB_BACKUP}"

echo "[$(date -Iseconds)] Backing up configuration..."
tar czf "${CONFIG_BACKUP}" \
    deployment/secrets/production.env \
    deployment/compose/docker-compose.prod.yml \
    deployment/nginx/ \
    deployment/monitoring/

echo "[$(date -Iseconds)] Backing up runtime data..."
docker exec lawim-app tar czf - /app/data/runtime 2>/dev/null | cat > "${EVIDENCE_BACKUP}" || true

echo "[$(date -Iseconds)] Creating backup manifest..."
cat > "${BACKUP_PATH}/MANIFEST.txt" <<EOF
LAWIM Backup
Date: $(date -Iseconds)
Version: $(git rev-parse --short HEAD)
Files:
  database.sql.gz  - PostgreSQL dump (gzip)
  config.tar.gz    - Configuration files
  evidence.tar.gz  - Runtime data
Checksums:
EOF
cd "${BACKUP_PATH}" && sha256sum *.gz >> MANIFEST.txt

echo "[$(date -Iseconds)] Backup complete: ${BACKUP_PATH}"
ls -lh "${BACKUP_PATH}"
