# Docker Configuration Guide

## Dockerfile Specifications

### Frontend Dockerfile

```dockerfile
- Base: node:18-alpine (multi-stage build)
- Build stage: Installs dependencies, builds production bundle
- Runtime stage: Minimal Alpine image with serve utility
- Exposed port: 3000
- Health check: HTTP health endpoint
- Environment: NODE_ENV, VITE_LAWIM_API_URL, VITE_LAWIM_USE_MOCKS
```

### Backend Dockerfile

```dockerfile
- Base: python:3.11-slim
- Dependencies: PostgreSQL client, GCC (for binary packages)
- Exposed port: 8000
- Health check: /health endpoint
- Environment: DATABASE_URL, REDIS_URL, JWT_SECRET
- Frozen: No modifications to backend code allowed
```

### Microservice Dockerfiles

All microservices (Brain, Agents, Knowledge, Communication, Campay) follow similar pattern:

```dockerfile
- Base: python:3.11-slim
- Port: 8001-8005 (sequential)
- Health check: Service-specific /health endpoint
- Environment: Service-specific configuration
- Resource limits: CPU and memory constraints
```

### Worker & Scheduler Dockerfiles

```dockerfile
- Base: python:3.11-slim
- Worker: Celery worker process for async tasks
- Scheduler: Celery Beat scheduler for periodic tasks
- Dependencies: Celery, Redis, RedBeat
- Connection: Redis for message broker
```

### Nginx Dockerfile

```dockerfile
- Base: nginx:alpine
- Configuration: Loaded from deployment/nginx/
- SSL: Configured with certificates
- Exposed ports: 80 (HTTP), 443 (HTTPS)
- Health check: wget health check
```

## Docker Compose Configuration

### Development (docker-compose.dev.yml)

- **Services**: 11 (frontend, backend, postgres, redis, workers, microservices)
- **Networking**: Single Docker bridge network
- **Volumes**: Development code volumes for hot reload
- **Restart**: unless-stopped policy
- **Resource limits**: None (development only)

### Staging (docker-compose.staging.yml)

- **Services**: 12 (adds nginx reverse proxy)
- **Replicas**: 2x workers (except postgres, redis)
- **Resource limits**: CPU and memory constraints
- **Networking**: Production-like setup
- **Volumes**: Persistent data volumes
- **Restart**: always policy

### Production (docker-compose.prod.yml)

- **Services**: 12 (full stack)
- **Replicas**: HA setup (backend: 3, agents: 3, workers: 4)
- **Resource limits**: Strict CPU and memory limits
- **Update policy**: Rolling updates with no downtime
- **Health checks**: Comprehensive health monitoring
- **Logging**: JSON logging format
- **Networking**: Secure bridge network

## Build Process

### Local Development Build

```bash
docker-compose -f deployment/compose/docker-compose.dev.yml build

# Or specific service
docker-compose build frontend
```

### Staging Build

```bash
docker-compose -f deployment/compose/docker-compose.staging.yml build --no-cache
```

### Production Build

```bash
# Build with specific tags
docker build -f deployment/docker/Dockerfile.backend -t lawim/backend:v2.0.0 .
docker build -f deployment/docker/Dockerfile.frontend -t lawim/frontend:v2.0.0 .

# Push to registry
docker push lawim/backend:v2.0.0
docker push lawim/frontend:v2.0.0
```

## Image Optimization

### Size Reduction

- **Alpine Linux**: Minimal base images
- **Multi-stage builds**: Frontend build optimization
- **Layer caching**: Efficient Dockerfile structure

### Typical Image Sizes

- Frontend: ~150MB
- Backend: ~200MB
- Microservices: ~180MB each
- Nginx: ~20MB

## Registry Configuration

### Docker Hub

```bash
docker tag lawim/backend:v2.0.0 myregistry.azurecr.io/lawim/backend:v2.0.0
docker push myregistry.azurecr.io/lawim/backend:v2.0.0
```

### Private Registry

Configure in docker-compose.yml:

```yaml
services:
  backend:
    image: myregistry.example.com/lawim/backend:v2.0.0
```

## Best Practices

1. **Pin versions**: Use specific image tags, not latest
2. **Minimal base images**: Prefer Alpine over full OS images
3. **Security scanning**: Scan images for vulnerabilities
4. **Layer caching**: Order Dockerfile commands by change frequency
5. **Health checks**: Define for all services
6. **Resource limits**: Set CPU and memory constraints
7. **Logging**: Use structured JSON logging
8. **Documentation**: Document all environment variables
