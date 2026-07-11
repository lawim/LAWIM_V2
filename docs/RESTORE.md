# STATUT : ARCHIVE HISTORIQUE
# NON APPLICABLE A LA VERSION ACTUELLE
#
# Documentation active :
# `backup-disaster-recovery/restore-database.md`
# `backup-disaster-recovery/restore-media.md`
# `backup-disaster-recovery/restore-complete.md`

# Restore Operations Guide

## Overview

The restore system is designed for rapid recovery from various failure scenarios while maintaining data integrity and system consistency.

## Pre-Restore Checklist

Before initiating any restore operation:

- [ ] Backup file exists and is accessible
- [ ] Backup file integrity verified (checksums match)
- [ ] Target environment identified (dev/staging/prod)
- [ ] Database size compatible with available storage
- [ ] Required permissions available
- [ ] Stakeholders notified
- [ ] Restore procedure documented
- [ ] Rollback plan available

## Restore Scenarios

### Scenario 1: Application Bug / Data Corruption

**When:** Data corrupted due to application bug
**RTO:** 30-60 minutes
**Steps:**

```bash
# 1. Identify corruption
docker-compose exec postgres psql -U lawim -d lawim -c "SELECT COUNT(*) FROM users WHERE created_at > NOW();"

# 2. Stop application services (keep DB)
docker-compose stop frontend backend worker scheduler

# 3. Restore database only
tar -xzf lawim_backup_20240703_023000.tar.gz
docker-compose exec postgres psql -U lawim lawim < lawim_backup_20240703_023000/database.sql

# 4. Verify data
docker-compose exec postgres psql -U lawim -d lawim -c "SELECT COUNT(*) FROM users;"

# 5. Restart services
docker-compose up -d

# 6. Run health checks
docker-compose exec backend python deployment/health/health_checker.py
```

### Scenario 2: Configuration Error

**When:** Nginx/secrets misconfigured
**RTO:** 10-15 minutes
**Steps:**

```bash
# 1. Extract configuration from backup
tar -xzf lawim_backup_20240703_023000.tar.gz
tar -xzf lawim_backup_20240703_023000/config.tar.gz

# 2. Copy configuration back
cp -r deployment/nginx deployment/nginx.backup
cp -r <extracted>/deployment/nginx/* deployment/nginx/

# 3. Reload Nginx
docker-compose exec nginx nginx -t  # Test config
docker-compose exec nginx nginx -s reload

# 4. Verify functionality
curl -k https://lawim.app/health
```

### Scenario 3: File/Upload Loss

**When:** User files accidentally deleted
**RTO:** 20-30 minutes
**Steps:**

```bash
# 1. Extract file archive from backup
tar -xzf lawim_backup_20240703_023000.tar.gz
tar -xzf lawim_backup_20240703_023000/uploads.tar.gz

# 2. Verify file count
find data/uploads -type f | wc -l

# 3. Restore specific files
cp -r data/uploads/* <destination>/

# 4. Verify permissions
chmod -R 755 data/uploads/

# 5. No service restart needed - files already accessible
```

### Scenario 4: Complete Service Failure

**When:** Multiple services down / database unavailable
**RTO:** 1-2 hours
**Steps:**

```bash
# 1. Full system restore
./deployment/scripts/restore.sh /path/to/latest/backup.tar.gz

# Script automatically:
# - Stops all services
# - Extracts backup
# - Restores database
# - Restores files
# - Restores configuration
# - Starts all services
# - Runs health checks

# 2. Post-restore verification
docker-compose ps  # All containers running
docker-compose exec backend python deployment/health/health_checker.py

# 3. Smoke testing
# - Access frontend
# - Login with test account
# - Verify data
# - Test key workflows
```

### Scenario 5: Full Server Failure (Disaster Recovery)

**When:** Server hardware failure / complete data loss
**RTO:** 2-4 hours
**Steps:**

```bash
# 1. Provision new server with Docker installed
# (See PRODUCTION.md for server setup)

# 2. Clone LAWIM_V2
git clone https://github.com/lawim/LAWIM_V2.git
cd LAWIM_V2

# 3. Configure environment
cp deployment/.env.example deployment/.env.production
# Edit with production values

# 4. Download backup from remote storage
# Option A: Google Drive
rclone copy gdrive:lawim-backups/lawim_backup_20240703_023000.tar.gz .

# Option B: S3
aws s3 cp s3://lawim-backups/lawim_backup_20240703_023000.tar.gz .

# 5. Deploy services
export ENVIRONMENT=production
./deployment/scripts/deploy.sh

# 6. Restore from backup
./deployment/scripts/restore.sh ./lawim_backup_20240703_023000.tar.gz

# 7. Verify restoration
docker-compose exec backend python deployment/health/health_checker.py

# 8. Update DNS to point to new server
# (DNS propagation: 15 min - 24 hours)
```

## Detailed Restore Steps

### Step 1: Prepare Restore Environment

```bash
# Create restore directory
mkdir -p /restore
cd /restore

# Verify backup file exists
ls -lh lawim_backup_*.tar.gz

# Create temporary extraction directory
mkdir -p temp_backup
cd temp_backup
```

### Step 2: Extract and Verify Backup

```bash
# Extract backup
tar -xzf ../lawim_backup_*.tar.gz

# Verify extraction
ls -la

# Verify checksums
cd lawim_backup_*
md5sum -c CHECKSUMS.md5

# If checksum fails:
echo "⚠ Checksum mismatch - backup may be corrupted!"
exit 1
```

### Step 3: Stop Services (if needed)

```bash
# For partial restore, stop only affected services
docker-compose stop frontend backend

# For full restore, stop everything
docker-compose down

# Give services time to gracefully shut down
sleep 5
```

### Step 4: Restore Database

```bash
# Start PostgreSQL if not running
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
sleep 10

# Drop current database (WARNING: destructive!)
docker-compose exec postgres psql -U lawim -c "DROP DATABASE IF EXISTS lawim;"

# Recreate empty database
docker-compose exec postgres psql -U lawim -c "CREATE DATABASE lawim;"

# Restore from backup
docker-compose exec postgres psql -U lawim lawim < database.sql

# Verify restoration
docker-compose exec postgres psql -U lawim lawim -c "SELECT COUNT(*) FROM pg_tables WHERE schemaname='public';"
```

### Step 5: Restore Files

```bash
# Backup current files (just in case)
tar -czf uploads.backup.tar.gz data/uploads/

# Extract uploaded files
tar -xzf uploads.tar.gz

# Set proper permissions
find data/uploads -type f -exec chmod 644 {} \;
find data/uploads -type d -exec chmod 755 {} \;

# Verify restoration
find data/uploads -type f | wc -l
```

### Step 6: Restore Configuration

```bash
# Extract configuration
tar -xzf config.tar.gz

# Verify Nginx configuration
docker-compose exec nginx nginx -t

# Verify SSL certificates exist
ls -la deployment/nginx/ssl/

# Verify environment file
cat deployment/.env.production | head -20
```

### Step 7: Verify Data Integrity

```bash
# Test database integrity
docker-compose exec postgres psql -U lawim lawim -c "ANALYZE;"

# Check for errors
docker-compose exec postgres psql -U lawim lawim -c "SELECT datname, stats_reset FROM pg_stat_database WHERE datname='lawim';"

# Verify key tables
docker-compose exec postgres psql -U lawim lawim << EOF
SELECT COUNT(*) as users FROM users;
SELECT COUNT(*) as properties FROM properties;
SELECT COUNT(*) as favorites FROM favorites;
EOF
```

### Step 8: Restart Services

```bash
# Start all services
docker-compose up -d

# Wait for services to initialize
sleep 15

# Check service status
docker-compose ps

# Verify all containers are running
docker-compose ps | grep -c "Up" | grep -q "12" && echo "✓ All services running"
```

### Step 9: Post-Restore Testing

```bash
# Run health checks
docker-compose exec backend python deployment/health/health_checker.py

# Test application functionality
curl -k https://localhost/
curl -k https://localhost/api/health
curl -k https://localhost/api/properties

# Verify user data
docker-compose exec backend python -c "from app import db; print(f'Users: {db.session.query(User).count()}')"

# Check logs for errors
docker-compose logs --tail=50 backend
docker-compose logs --tail=50 postgres
```

## Monitoring Restore Progress

### Real-Time Progress

```bash
# Monitor database restore
watch -n 1 'docker-compose exec postgres psql -U lawim lawim -c "SELECT COUNT(*) FROM users;"'

# Monitor file restore
watch -n 5 'find data/uploads -type f | wc -l'

# Monitor service startup
watch -n 2 'docker-compose ps'
```

### Restore Logs

```bash
# View restoration logs
tail -f /var/log/lawim-restore.log

# Search for errors
grep -i "error\|failed\|corrupted" /var/log/lawim-restore.log
```

## Rollback Procedures

### If Restore Fails

```bash
# 1. Stop services
docker-compose down

# 2. Restore previous state
docker volume rm lawim_postgres_data  # Remove corrupted data
docker volume rm lawim_redis_data

# 3. Start with different backup
./deployment/scripts/restore.sh /path/to/older/backup.tar.gz

# 4. If still failing, contact support
```

### Manual Rollback

```bash
# If automated rollback fails:

# 1. Stop services
docker-compose kill

# 2. Restore from snapshots (if available)
lvm restore /dev/backup/postgres_snapshot

# 3. Or use filesystem snapshots
btrfs subvolume snapshot /mnt/data/.snapshots/postgres_backup /mnt/data/postgres

# 4. Restart services
docker-compose up -d
```

## Testing Restore Procedures

### Monthly Restore Drill

```bash
# 1. Use staging backup on test server
# 2. Extract and verify backup
# 3. Document any issues
# 4. Calculate actual RTO
# 5. Update procedures if needed
# 6. Archive drill report
```

### Validation Checklist

- [ ] Backup extraction succeeds
- [ ] Checksum verification passes
- [ ] Database restore completes in < 30 min
- [ ] File restore completes in < 15 min
- [ ] All services start successfully
- [ ] Health checks pass
- [ ] Application is fully functional
- [ ] No data corruption detected

## Emergency Support

**For restore issues:**
1. Check restore logs: `/var/log/lawim-restore.log`
2. Verify backup integrity: `md5sum -c CHECKSUMS.md5`
3. Check disk space: `df -h`
4. Contact infrastructure team with:
   - Exact error message
   - Backup file name
   - Target environment
   - Steps taken so far
