# Production Deployment Guide

## Pre-Deployment Checklist

### Infrastructure Readiness

- [ ] Server hardware meets minimum requirements
  - CPU: 16+ cores
  - RAM: 64+ GB
  - Storage: 1TB+ SSD
  - Network: 1Gbps+ connectivity
- [ ] Operating system: Linux (Ubuntu 22.04 LTS recommended)
- [ ] Docker installed (latest version)
- [ ] Docker Compose installed (v2.0+)
- [ ] SSL/TLS certificates obtained
- [ ] Domain names registered and configured
- [ ] DNS records configured

### Configuration Readiness

- [ ] `.env.production` created with all secrets
- [ ] Database password (32+ characters, random)
- [ ] Redis password (32+ characters, random)
- [ ] JWT secret (32+ characters, random)
- [ ] External API keys configured
- [ ] SMTP credentials configured
- [ ] Backup storage configured

### Monitoring Readiness

- [ ] Monitoring tools installed (Prometheus, Grafana, etc.)
- [ ] Alerting configured for critical services
- [ ] Log aggregation configured
- [ ] Status page created
- [ ] On-call schedules established

### Documentation Readiness

- [ ] Runbooks created
- [ ] Disaster recovery plan documented
- [ ] Emergency contact list created
- [ ] Escalation procedures documented

## Deployment Procedure

### Step 1: Server Setup

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y docker.io docker-compose git curl wget htop vim

# Add user to docker group
sudo usermod -aG docker $USER
```

### Step 2: Clone Repository

```bash
git clone https://github.com/lawim/LAWIM_V2.git
cd LAWIM_V2
git checkout develop/2.0-intelligent-platform
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp deployment/.env.example deployment/.env.production

# Edit with production values
nano deployment/.env.production

# Verify configuration
docker-compose config -f deployment/compose/docker-compose.prod.yml
```

### Step 4: SSL/TLS Setup

```bash
# Copy certificates
mkdir -p deployment/nginx/ssl
cp /path/to/lawim.crt deployment/nginx/ssl/
cp /path/to/lawim.key deployment/nginx/ssl/
chmod 600 deployment/nginx/ssl/lawim.key
```

### Step 5: Deploy Services

```bash
# Start deployment
export ENVIRONMENT=production
./deployment/scripts/deploy.sh

# Verify services
docker-compose -f deployment/compose/docker-compose.prod.yml ps

# Check health
docker-compose exec backend python deployment/health/health_checker.py
```

### Step 6: Initialize Database

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed initial data (if needed)
docker-compose exec backend python -m scripts.seed_data
```

### Step 7: Verify Deployment

```bash
# Test frontend
curl -k https://lawim.app/

# Test API
curl -k https://api.lawim.app/health

# Test microservices
curl -k https://api.lawim.app/brain/health
curl -k https://api.lawim.app/agents/health
curl -k https://api.lawim.app/knowledge/health
```

## Post-Deployment Validation

### Functional Tests

- [ ] User can register account
- [ ] User can login
- [ ] User can search properties
- [ ] User can view property details
- [ ] User can add to favorites
- [ ] Brain service routes intents correctly
- [ ] Knowledge search works
- [ ] Workflow execution succeeds

### Performance Tests

- [ ] Homepage loads in <2 seconds
- [ ] API responses in <500ms
- [ ] Can handle 100 concurrent users
- [ ] Microservices respond healthily

### Security Tests

- [ ] HTTPS enforced
- [ ] Security headers present
- [ ] CORS properly restricted
- [ ] Rate limiting works
- [ ] Authentication required for protected endpoints

### Backup/Recovery Tests

- [ ] Initial backup created successfully
- [ ] Backup file integrity verified
- [ ] Restore process tested

## High Availability Setup

### Database Replication

```yaml
# postgres-replica.yml
services:
  postgres-primary:
    environment:
      POSTGRES_REPLICATION_MODE: master
      
  postgres-replica:
    environment:
      POSTGRES_REPLICATION_MODE: slave
      POSTGRES_MASTER_SERVICE: postgres-primary
```

### Redis Clustering

```yaml
services:
  redis-cluster:
    image: redis:7-alpine
    command: redis-server --cluster-enabled yes
```

### Service Replication

Already configured in `docker-compose.prod.yml`:
- Backend: 3 replicas
- Agents: 3 replicas
- Workers: 4 replicas
- Knowledge: 2 replicas

## Scaling Strategy

### Horizontal Scaling

As load increases, scale services:

```bash
# Scale backend
docker-compose up -d --scale backend=10

# Scale agents
docker-compose up -d --scale agents=20

# Scale workers
docker-compose up -d --scale worker=16
```

### Vertical Scaling

If single server not sufficient:
1. Separate database to dedicated server
2. Separate Redis to dedicated server
3. Distribute microservices across multiple nodes

## Maintenance Operations

### Weekly

- [ ] Review error logs
- [ ] Check disk space usage
- [ ] Verify backup completion
- [ ] Monitor performance metrics

### Monthly

- [ ] Database optimization (REINDEX, ANALYZE)
- [ ] SSL certificate expiration check
- [ ] Dependency security updates
- [ ] Disaster recovery drill

### Quarterly

- [ ] Major version updates
- [ ] Capacity planning review
- [ ] Security audit
- [ ] Performance benchmarking

## Incident Response

### Service Outage

1. Check health: `docker-compose ps`
2. Review logs: `docker-compose logs --tail=100`
3. Restart service: `docker-compose restart <service>`
4. If not recovered: Execute rollback procedure

### Database Issues

1. Check connectivity: `docker-compose exec postgres psql -U lawim -d lawim`
2. Check disk space: `docker exec postgres df /var/lib/postgresql/data`
3. Verify replication status if applicable

### Memory Pressure

1. Review memory usage: `docker stats`
2. Identify consuming service
3. Increase memory limit or restart service
4. Scale horizontally if needed

## Rollback Procedure

```bash
# If deployment fails:

# 1. Stop services
docker-compose down

# 2. Restore from backup
./deployment/scripts/restore.sh /path/to/backup.tar.gz

# 3. Verify restoration
docker-compose ps
docker-compose exec backend python deployment/health/health_checker.py

# 4. If still issues, contact support
```

## Secrets Management

### Recommended Approach

Use HashiCorp Vault or cloud provider secrets:

```bash
# Example with Vault
vault kv put secret/lawim/production \
  db_password="..." \
  redis_password="..." \
  jwt_secret="..."

# Load in deployment script
export DB_PASSWORD=$(vault kv get -field=db_password secret/lawim/production)
```

### Never

- ✗ Commit `.env.production` to git
- ✗ Log sensitive values
- ✗ Share secrets via email
- ✗ Use default passwords

## Support & Escalation

**Issue Type** → **Response Time** → **Escalation**
- Critical (complete outage) → 15 min → CTO
- High (degraded service) → 1 hour → Engineering Lead
- Medium (non-critical bug) → 4 hours → Team Lead
- Low (enhancement) → 24 hours → Product Manager
