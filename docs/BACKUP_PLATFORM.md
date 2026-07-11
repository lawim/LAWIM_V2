# STATUT : ARCHIVE HISTORIQUE
# NON APPLICABLE A LA VERSION ACTUELLE
#
# Documentation active :
# `backup-disaster-recovery/architecture.md`

# Backup & Restore Platform Documentation

## Backup Architecture

```
┌─────────────────────────────────────────────┐
│     Local Backup Service                    │
├─────────────────────────────────────────────┤
│ Database Dump          | File Archives      │
│ Configuration Files    | Checksums (MD5)    │
└──────────┬──────────────────────────────────┘
           │
      ┌────▼────────────────────────┐
      │  Backup Storage             │
      ├────────────────────────────┤
      │ Daily Backups (7-90 days)  │
      │ Rotation & Compression     │
      │ Checksum Verification      │
      └────┬────────────────────────┘
           │
      ┌────▼────────────────────────┐
      │  Remote Storage Integration │
      ├────────────────────────────┤
      │ Google Drive via rclone    │
      │ S3 / Cloud Storage         │
      │ FTP / SFTP Server          │
      └────────────────────────────┘
```

## Backup Types

### Full Backup

Complete backup of entire system (database + files + config):

```bash
./deployment/scripts/backup.sh

# Includes:
# - PostgreSQL full dump (all tables, indexes, functions)
# - All user uploads and files
# - Nginx configuration and SSL certificates
# - Application configuration
# - Checksums for all files
```

### Incremental Backup

Backups only changed data (future enhancement):

```bash
./deployment/scripts/backup.sh --incremental
```

### Database-Only Backup

Just the PostgreSQL database:

```bash
docker-compose exec postgres pg_dump -U lawim lawim > database.sql
```

### Point-in-Time Recovery

Using PostgreSQL WAL archives:

```bash
# Enable WAL archiving in PostgreSQL configuration
# Configure retention period
# Perform point-in-time recovery if needed
```

## Backup Retention Policy

| Environment | Frequency | Retention | Location |
|------------|-----------|-----------|----------|
| Development | Daily | 7 days | Local |
| Staging | Daily | 30 days | Local + Remote |
| Production | Daily | 90 days | Local + Remote |

## Backup Storage

### Local Storage

```
/data/backups/
├── lawim_backup_20240704_023000.tar.gz
├── lawim_backup_20240703_023000.tar.gz
├── lawim_backup_20240702_023000.tar.gz
└── lawim_backup_20240701_023000.tar.gz
```

### Remote Storage Configuration

#### Google Drive (via rclone)

```bash
# Configure rclone
rclone config

# Create folder in Google Drive
# Set rclone remote name and folder ID

# Backup script handles upload automatically
export RCLONE_REMOTE=gdrive
export BACKUP_REMOTE_ENABLED=true
./deployment/scripts/backup.sh
```

#### Amazon S3

```bash
# Configure AWS credentials
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...

# Configure rclone
[s3]
type = s3
access_key_id = $AWS_ACCESS_KEY_ID
secret_access_key = $AWS_SECRET_ACCESS_KEY
region = us-east-1

# Backup automatically uploads to S3
```

#### FTP/SFTP Server

```bash
# Configure rclone for SFTP
[sftp]
type = sftp
host = backup.example.com
user = lawim
pass = <encrypted-password>
port = 22

# Backup uploads via SFTP
```

## Backup Process

### Automated Scheduling

Using system cron or Docker container:

```bash
# Add to crontab (runs daily at 2:30 AM)
30 2 * * * cd /path/to/LAWIM_V2 && ./deployment/scripts/backup.sh >> /var/log/lawim-backup.log 2>&1
```

### Manual Backup

```bash
# Trigger immediate backup
cd /path/to/LAWIM_V2
export ENVIRONMENT=production
./deployment/scripts/backup.sh
```

### Backup Contents

```
lawim_backup_20240704_023000/
├── database.sql                    # PostgreSQL full dump
├── uploads.tar.gz                  # All user files
├── config.tar.gz                   # Configuration files
│   ├── nginx/
│   ├── ssl/
│   └── .env.production
└── CHECKSUMS.md5                   # File integrity verification
```

## Verification & Integrity

### Checksum Verification

```bash
# During backup creation
md5sum -c CHECKSUMS.md5

# Before restore
tar -xzf lawim_backup_*.tar.gz
cd lawim_backup_*
md5sum -c CHECKSUMS.md5
```

### Backup Testing

**Weekly backup verification:**

```bash
# Extract and verify (on test server)
tar -xzf lawim_backup_20240704_023000.tar.gz
cd lawim_backup_20240704_023000

# Verify database dump
psql -U lawim -d lawim < database.sql

# Verify file integrity
md5sum -c CHECKSUMS.md5 | grep -v OK && echo "Verification failed"
```

## Restore Process

### Full System Restore

```bash
# Restore from backup file
./deployment/scripts/restore.sh /path/to/backup.tar.gz

# Script performs:
# 1. Extract backup
# 2. Verify checksums
# 3. Stop services
# 4. Restore database
# 5. Restore files
# 6. Restore configuration
# 7. Start services
# 8. Health check
```

### Database-Only Restore

```bash
# Extract database from backup
tar -xzf lawim_backup_*.tar.gz
cd lawim_backup_*/

# Restore to current database
docker-compose exec postgres psql -U lawim lawim < database.sql
```

### Selective Restore

```bash
# Restore specific files from backup
tar -xzf lawim_backup_*.tar.gz lawim_backup_*/uploads/specific_file

# Restore specific configuration
tar -xzf lawim_backup_*.tar.gz lawim_backup_*/config.tar.gz
tar -xzf config.tar.gz deployment/nginx/ssl/
```

### Point-in-Time Recovery

```bash
# If PostgreSQL WAL archiving is enabled
PGPASSWORD=<password> pg_restore \
  -h localhost \
  -U lawim \
  -d lawim \
  --target-time='2024-07-04 10:30:00' \
  database.sql
```

## Backup Monitoring

### Backup Success Verification

```bash
# Check recent backups
ls -lh /data/backups/ | tail -10

# Verify latest backup
tar -tzf /data/backups/lawim_backup_*.tar.gz > /dev/null && echo "OK"

# Check backup size (typical: 2-5 GB)
du -h /data/backups/lawim_backup_latest.tar.gz
```

### Backup Logs

```bash
# View backup logs
tail -f /var/log/lawim-backup.log

# Search for errors
grep ERROR /var/log/lawim-backup.log
```

### Monitoring Dashboard

Check backup status in Admin Deployment Console:
- Last backup date and time
- Backup size
- Success/failure status
- Remote upload status

## Recovery Time Objectives (RTO)

| Scenario | RTO | RPO |
|----------|-----|-----|
| Single service restart | 5 min | 0 |
| Database recovery | 30 min | 24 hours |
| Full system recovery | 2 hours | 24 hours |
| Disaster recovery | 4 hours | 24 hours |

## Disaster Recovery Plan

### Scenario: Database Corruption

1. Detect via health check alerts
2. Stop services to prevent further corruption
3. Restore database from backup
4. Verify data integrity
5. Restart services
6. Run full test suite

### Scenario: Complete Data Loss

1. Access remote backup (Google Drive/S3)
2. Download latest backup file
3. Verify checksum integrity
4. Run full restore procedure
5. Verify all services healthy
6. Run smoke tests

### Scenario: Server Failure

1. Provision new server
2. Install Docker and dependencies
3. Clone LAWIM_V2 repository
4. Configure environment files
5. Deploy services
6. Restore from backup
7. Run health checks
8. Update DNS if needed

## Best Practices

1. **Test restoration regularly** - Minimum monthly
2. **Keep backups offsite** - Use remote storage
3. **Verify checksum integrity** - Prevent corruption
4. **Document procedures** - Create runbooks
5. **Monitor backup jobs** - Alert on failures
6. **Maintain backup inventory** - Track all backups
7. **Encrypt backups** - Protect sensitive data
8. **Document RTO/RPO** - Know recovery targets

## Security Considerations

### Encryption

- Encrypt backups in transit (HTTPS/SFTP)
- Encrypt backups at rest (GPG, managed keys)
- Never store unencrypted passwords in backups

### Access Control

- Restrict backup access (read-only for operations team)
- Audit backup access logs
- Rotate credentials regularly

### Compliance

- GDPR: Export user data from backups if requested
- Retention: Follow data retention policies
- Audit: Document all restore operations

## References

- PostgreSQL Backup & Recovery: https://www.postgresql.org/docs/current/backup.html
- rclone Configuration: https://rclone.org/
- Disaster Recovery Planning: https://en.wikipedia.org/wiki/Disaster_recovery
