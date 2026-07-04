#!/usr/bin/env bash
# Restore script for LAWIM V2
# Restores from backup files

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup-file.tar.gz>"
    exit 1
fi

BACKUP_FILE="$1"
ENVIRONMENT=${ENVIRONMENT:-production}
TEMP_DIR="/tmp/lawim_restore_$$"

echo "================================"
echo "LAWIM V2 Restore"
echo "Environment: $ENVIRONMENT"
echo "Backup File: $BACKUP_FILE"
echo "================================"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "✗ Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Extract backup
echo ""
echo "Extracting backup..."
mkdir -p "$TEMP_DIR"
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
BACKUP_DIR=$(find "$TEMP_DIR" -maxdepth 1 -type d -name "lawim_backup_*" | head -1)

if [ -z "$BACKUP_DIR" ]; then
    echo "✗ Invalid backup file format"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "✓ Backup extracted"

# Verify checksums
echo ""
echo "Verifying backup integrity..."
cd "$BACKUP_DIR"
if md5sum -c CHECKSUMS.md5 > /dev/null 2>&1; then
    echo "✓ All files verified"
else
    echo "✗ Backup integrity check failed"
    exit 1
fi
cd - > /dev/null

# Load environment
export $(cat "deployment/.env.${ENVIRONMENT}" | grep -v '^#' | xargs)

# Stop services
echo ""
echo "Stopping services..."
docker-compose -f "deployment/compose/docker-compose.${ENVIRONMENT}.yml" down || true

# Restore database
echo ""
echo "Restoring database..."
if [ -f "${BACKUP_DIR}/database.sql" ]; then
    docker-compose -f "deployment/compose/docker-compose.${ENVIRONMENT}.yml" up -d postgres
    sleep 10
    docker-compose -f "deployment/compose/docker-compose.${ENVIRONMENT}.yml" exec -T postgres \
        psql -U lawim lawim < "${BACKUP_DIR}/database.sql"
    echo "✓ Database restored"
fi

# Restore uploads
echo ""
echo "Restoring uploads..."
if [ -f "${BACKUP_DIR}/uploads.tar.gz" ]; then
    tar -xzf "${BACKUP_DIR}/uploads.tar.gz"
    echo "✓ Uploads restored"
fi

# Restore configuration
echo ""
echo "Restoring configuration..."
if [ -f "${BACKUP_DIR}/config.tar.gz" ]; then
    tar -xzf "${BACKUP_DIR}/config.tar.gz"
    echo "✓ Configuration restored"
fi

# Clean up
rm -rf "$TEMP_DIR"

# Start services
echo ""
echo "Starting services..."
docker-compose -f "deployment/compose/docker-compose.${ENVIRONMENT}.yml" up -d

# Health check
echo ""
echo "Running health checks..."
sleep 10
if docker-compose -f "deployment/compose/docker-compose.${ENVIRONMENT}.yml" exec -T backend \
    python deployment/health/health_checker.py > /dev/null 2>&1; then
    echo "✓ Services healthy"
else
    echo "⚠ Some services may not be healthy yet"
fi

echo ""
echo "================================"
echo "✓ Restore completed!"
echo "================================"
