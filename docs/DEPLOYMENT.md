# LAWIM V2 - Deployment Platform Documentation

## Architecture Overview

The LAWIM V2 deployment platform is a production-grade infrastructure built on Docker and Docker Compose, designed for:

- **Multi-environment support**: Development, Staging, Production
- **High availability**: Service replication and load balancing
- **Auto-scaling**: Horizontal scaling capabilities
- **Health monitoring**: Real-time service health checks
- **Backup & restore**: Comprehensive data protection
- **Security**: HTTPS, security headers, rate limiting, JWT auth

## Services Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NGINX Reverse Proxy                       │
│            (Load Balancing, SSL/TLS, Rate Limiting)          │
└────────┬──────────────────────────────┬──────────────────────┘
         │                              │
    ┌────▼─────┐                   ┌────▼────────┐
    │ Frontend  │                   │   Backend    │
    │(React SPA)│                   │  (FastAPI)   │
    └────┬─────┘                   └────┬────────┘
         │                              │
    ┌────▼──────────┬──────────────┬────▼───────┐
    │   Brain       │   Agents     │  Knowledge │
    │  (Intent)     │ (Business)   │   (RAG)    │
    └───────────────┴──────────────┴────────────┘

    ┌──────────────────────────────────────────┐
    │     Core Infrastructure                  │
    ├──────────────────────────────────────────┤
    │ PostgreSQL (Main DB) | Redis (Cache)    │
    │ Celery Workers      | Celery Beat        │
    │ Communication | Campay | Monitoring      │
    └──────────────────────────────────────────┘
```

## Deployment Workflows

### Development Deployment

```bash
cd /path/to/LAWIM_V2
export ENVIRONMENT=development
./deployment/scripts/deploy.sh
```

Services start in development mode with hot-reload enabled.

### Staging Deployment

```bash
export ENVIRONMENT=staging
./deployment/scripts/deploy.sh
```

Staging includes monitoring and backup capabilities with production-like configuration.

### Production Deployment

```bash
export ENVIRONMENT=production
./deployment/scripts/deploy.sh
```

Production deployment includes:
- Service replication for HA
- Resource limits enforcement
- Comprehensive monitoring
- Automated backup procedures
- Security hardening

## Environment Configuration

### Configuration Hierarchy

1. `.env.example` - Template with all available variables
2. `.env.{environment}` - Environment-specific overrides
3. Runtime environment variables - Docker/system env vars

### Required Environment Variables

**Database:**
- `DATABASE_URL`: PostgreSQL connection string
- `DATABASE_PASSWORD`: Secure database password

**Cache:**
- `REDIS_URL`: Redis connection string
- `REDIS_PASSWORD`: Secure Redis password

**Security:**
- `JWT_SECRET`: JWT signing key (min 32 characters)
- `ALLOWED_ORIGINS`: CORS configuration

**External Services:**
- `CAMPAY_API_KEY`: Payment gateway credentials
- `SMTP_SERVER`, `SMTP_USER`, `SMTP_PASSWORD`: Email configuration
- `WHATSAPP_API_KEY`: WhatsApp Business API credentials

**Backup:**
- `BACKUP_LOCAL_PATH`: Local backup directory
- `BACKUP_REMOTE_ENABLED`: Enable remote backup

## Service Scaling

### Manual Scaling

```bash
# Scale backend to 5 replicas
docker-compose -f deployment/compose/docker-compose.prod.yml up -d --scale backend=5

# Scale agents to 10 replicas
docker-compose -f deployment/compose/docker-compose.prod.yml up -d --scale agents=10
```

### Auto-Scaling Metrics

Services are scaled based on:
- CPU utilization (target: 60-70%)
- Memory usage (target: 80%)
- Request latency (target: <500ms)
- Error rate (target: <1%)

## Monitoring

### Health Checks

All services include health check endpoints:
- Frontend: `/` (HTTP 200)
- Backend: `/health` (JSON)
- Brain: `/health` (JSON)
- Agents: `/health` (JSON)
- Knowledge: `/health` (JSON)
- Campay: `/health` (JSON)
- Communication: `/health` (JSON)

### Monitoring Dashboard

Access the admin deployment console at:
- Development: `http://localhost:8000/admin/deployment`
- Production: `https://api.lawim.app/admin/deployment`

Monitor:
- Service status and uptime
- Resource usage (CPU, memory)
- Recent backups
- Error rates and logs

## Backup & Restore

### Automated Backups

Backups follow the active BDR policy documented in `docs/backup-disaster-recovery/schedules.md`:
02:00 and 14:30 WAT (Africa/Douala).

```bash
# Manual backup
./deployment/backup/backup.sh

# Backup includes:
# - PostgreSQL database dump
# - User uploads (files)
# - Configuration (nginx, secrets)
# - Checksums for integrity verification
```

### Backup Retention

- **Development**: 7 days
- **Staging**: 30 days
- **Production**: 90 days

### Remote Backup

Configure rclone for remote backup to Google Drive, S3, or other services:

```bash
# Configure rclone
rclone config

# Upload backups
./deployment/backup/backup.sh
```

### Restore Operations

```bash
# Restore from backup file
./deployment/backup/restore.sh /path/to/backup.tar.gz

# Restore validates:
# - Backup file integrity
# - Database compatibility
# - Configuration validity
```

## Security

### HTTPS/TLS Configuration

- **Certificate**: Self-signed or Let's Encrypt
- **Protocols**: TLSv1.2, TLSv1.3
- **Ciphers**: HIGH grade ciphers only
- **Session caching**: 10 minute TTL

### Security Headers

```
Strict-Transport-Security: max-age=31536000
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: restrictive policy
```

### Rate Limiting

- **General API**: 100 requests/min per IP
- **Authentication**: 5 requests/min per IP
- **File uploads**: 20 requests/min per IP

### JWT Authentication

- Algorithm: HS256
- Expiration: 24 hours (access token)
- Refresh: 30 days (refresh token)

## Maintenance Operations

### System Updates

```bash
# Update images
docker pull <image>

# Rolling update with zero downtime
docker-compose -f docker-compose.prod.yml up -d
```

### Database Migrations

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Rollback if needed
docker-compose exec backend alembic downgrade -1
```

### Cache Cleanup

```bash
# Clear Redis cache
docker-compose exec redis redis-cli FLUSHDB

# Clear Nginx cache
docker-compose exec nginx rm -rf /var/cache/nginx/*
```

## Troubleshooting

### Service Not Starting

1. Check logs: `docker-compose logs <service>`
2. Verify environment variables: `docker-compose config`
3. Check dependencies: `docker-compose ps`
4. Restart service: `docker-compose restart <service>`

### Database Connection Issues

```bash
# Test connection
docker-compose exec backend python -c "import psycopg2; psycopg2.connect('...')"

# Check PostgreSQL logs
docker-compose logs postgres | tail -50
```

### Performance Issues

```bash
# Monitor resource usage
docker stats

# Check slow queries
docker-compose exec postgres psql -U lawim -d lawim -c "SELECT * FROM pg_stat_statements;"

# Analyze indexes
docker-compose exec postgres psql -U lawim -d lawim -c "REINDEX DATABASE lawim;"
```

## Production Checklist

- [ ] Environment variables configured securely
- [ ] SSL/TLS certificates installed
- [ ] Backup system tested and verified
- [ ] Monitoring and alerting configured
- [ ] Rate limiting enabled
- [ ] CORS properly restricted
- [ ] Database backups scheduled
- [ ] Log aggregation configured
- [ ] Security headers enabled
- [ ] Regular backup verification scheduled
- [ ] Disaster recovery plan documented
- [ ] On-call support established

## Support & Emergency Contacts

For deployment issues:
1. Check deployment logs: `./deployment/scripts/logs.sh`
2. Run health checks: `docker-compose exec backend python deployment/health/health_checker.py`
3. Review error traces in monitoring dashboard
4. Contact infrastructure team for infrastructure-level issues

## References

- Docker Compose Documentation: https://docs.docker.com/compose
- Nginx Documentation: https://nginx.org/en/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs
- Redis Documentation: https://redis.io/documentation
- FastAPI Documentation: https://fastapi.tiangolo.com
