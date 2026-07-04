#!/usr/bin/env bash
# Backup script for LAWIM V2
# Creates full or partial backups of database, files, and knowledge base

set -e

ENVIRONMENT=${ENVIRONMENT:-production}
BACKUP_PATH="deployment/backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="${BACKUP_PATH}/lawim_backup_${TIMESTAMP}"

echo "================================"
echo "LAWIM V2 Backup"
echo "Environment: $ENVIRONMENT"
echo "Backup Directory: $BACKUP_DIR"
echo "================================"

mkdir -p "$BACKUP_DIR"

# Load environment
export $(cat "deployment/.env.${ENVIRONMENT}" | grep -v '^#' | xargs)

# Backup Database
echo ""
echo "Backing up PostgreSQL database..."
docker-compose -f "deployment/compose/docker-compose.${ENVIRONMENT}.yml" exec -T postgres \
    pg_dump -U lawim lawim > "${BACKUP_DIR}/database.sql"
echo "✓ Database backed up ($(du -h ${BACKUP_DIR}/database.sql | cut -f1))"

# Backup Uploads
echo ""
echo "Backing up user uploads..."
if [ -d "data/uploads" ]; then
    tar -czf "${BACKUP_DIR}/uploads.tar.gz" data/uploads/
    echo "✓ Uploads backed up ($(du -h ${BACKUP_DIR}/uploads.tar.gz | cut -f1))"
fi

# Backup Configuration
echo ""
echo "Backing up configuration..."
tar -czf "${BACKUP_DIR}/config.tar.gz" \
    deployment/nginx/conf.d/ \
    deployment/nginx/ssl/ \
    deployment/.env.${ENVIRONMENT}
echo "✓ Configuration backed up"

# Create checksum
echo ""
echo "Creating checksums..."
cd "$BACKUP_DIR"
find . -type f ! -name "*.md5" -exec md5sum {} \; > CHECKSUMS.md5
cd - > /dev/null
echo "✓ Checksums created"

# Compress backup
echo ""
echo "Compressing backup..."
tar -czf "${BACKUP_DIR}.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"
echo "✓ Backup compressed ($(du -h ${BACKUP_DIR}.tar.gz | cut -f1))"

# Upload to remote if configured
if [ "$BACKUP_REMOTE_ENABLED" = "true" ]; then
    echo ""
    echo "Uploading to remote storage..."
    rclone copy "${BACKUP_DIR}.tar.gz" "${RCLONE_REMOTE}:lawim-backups/" \
        --config "${RCLONE_CONFIG_PATH}" \
        --verbose
    echo "✓ Backup uploaded to remote storage"
fi

echo ""
echo "================================"
echo "✓ Backup completed successfully!"
echo "Location: ${BACKUP_DIR}.tar.gz"
echo "================================"
