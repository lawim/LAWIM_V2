#!/usr/bin/env bash
# Deployment entrypoint for LAWIM V2
# Handles startup, migrations, and service orchestration

set -e

ENVIRONMENT=${ENVIRONMENT:-development}
COMPOSE_FILE="deployment/compose/docker-compose.${ENVIRONMENT}.yml"

echo "================================"
echo "LAWIM V2 Deployment"
echo "Environment: $ENVIRONMENT"
echo "================================"

# Load environment variables
if [ -f "deployment/.env.${ENVIRONMENT}" ]; then
    export $(cat "deployment/.env.${ENVIRONMENT}" | grep -v '^#' | xargs)
    echo "✓ Loaded environment: deployment/.env.${ENVIRONMENT}"
else
    echo "✗ Environment file not found: deployment/.env.${ENVIRONMENT}"
    exit 1
fi

# Create networks if not exists
docker network create lawim-network 2>/dev/null || true

# Start services
echo ""
echo "Starting services (${ENVIRONMENT})..."
docker-compose -f "$COMPOSE_FILE" up -d

# Wait for services to be healthy
echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Run health checks
echo ""
echo "Running health checks..."
if docker-compose -f "$COMPOSE_FILE" exec -T backend python deployment/health/health_checker.py; then
    echo "✓ All services healthy"
else
    echo "✗ Some services unhealthy"
    docker-compose -f "$COMPOSE_FILE" logs --tail=50
    exit 1
fi

echo ""
echo "================================"
echo "✓ Deployment successful!"
echo "================================"
