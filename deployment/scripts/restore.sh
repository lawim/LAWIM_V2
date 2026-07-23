#!/usr/bin/env bash
set -euo pipefail

RESTORE_PATH="${1:?Usage: $0 <backup_path>}"

if [ ! -f "${RESTORE_PATH}/database.sql.gz" ]; then
    echo "[ERROR] No database backup found in ${RESTORE_PATH}"
    exit 1
fi

echo "[$(date -Iseconds)] Starting LAWIM restore from ${RESTORE_PATH}"

echo "[$(date -Iseconds)] Verifying backup integrity..."
cd "${RESTORE_PATH}" && sha256sum -c MANIFEST.txt

echo "[$(date -Iseconds)] Restoring PostgreSQL database..."
gunzip -c "${RESTORE_PATH}/database.sql.gz" | docker exec -i lawim-db psql -U lawim lawim_v3

echo "[$(date -Iseconds)] Restoring configuration..."
tar xzf "${RESTORE_PATH}/config.tar.gz" -C /

echo "[$(date -Iseconds)] Restoring runtime data..."
if [ -f "${RESTORE_PATH}/evidence.tar.gz" ]; then
    gunzip -c "${RESTORE_PATH}/evidence.tar.gz" | docker exec -i lawim-app tar xzf - -C /
fi

echo "[$(date -Iseconds)] Restarting services..."
docker compose -f deployment/compose/docker-compose.prod.yml restart

echo "[$(date -Iseconds)] Restore complete."
