#!/usr/bin/env bash
# deploy_program_f_acceptance.sh
# Deploy Program F conversation engine on OVH.
# Run this from the LAWIM_V2 root on the OVH server.
set -Eeuo pipefail

EXPECTED_BRANCH="feature/program-f-conversation-engine"
COMPOSE_FILE="deployment/compose/docker-compose.prod.yml"
COMM_SERVICE="communication"
HEALTH_URL="https://api.lawim.app/healthz"

echo "=== Program F Deployment ==="
echo "Expected branch: $EXPECTED_BRANCH"
echo ""

# 1. Branch check
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "$EXPECTED_BRANCH" ]; then
    echo "ERROR: Expected branch '$EXPECTED_BRANCH', got '$BRANCH'"
    exit 1
fi
echo "✅ Branch: $BRANCH"

# 2. Fetch and pull
git fetch origin --prune
git pull --ff-only origin "$EXPECTED_BRANCH"
HEAD=$(git rev-parse --short HEAD)
echo "✅ HEAD: $HEAD"

# 3. Verify lawim_runtime is present
if [ ! -d "lawim_runtime" ]; then
    echo "ERROR: lawim_runtime directory not found"
    exit 1
fi
echo "✅ lawim_runtime present"

# 4. Build images
echo ""
echo "=== Building Docker images ==="
docker compose -f "$COMPOSE_FILE" build
echo "✅ Build complete"

# 5. Volumes check
echo ""
echo "=== Volume check ==="
docker volume ls | grep lawim || echo "No lawim volumes found (may use bind mounts)"
echo "✅ Volume check done"

# 6. Restart services
echo ""
echo "=== Starting services ==="
docker compose -f "$COMPOSE_FILE" up -d
echo "✅ Services started"

# 7. Healthcheck
echo ""
echo "=== Waiting for healthcheck ==="
if curl --retry 30 --retry-delay 3 --retry-connrefused --fail -fsS "$HEALTH_URL" > /dev/null 2>&1; then
    echo "✅ Healthcheck passed ($HEALTH_URL)"
else
    echo "⚠️  Healthcheck did not respond within timeout"
fi

# 8. Check logs for Program F
echo ""
echo "=== Program F engine check ==="
docker compose -f "$COMPOSE_FILE" logs --since=2m "$COMM_SERVICE" 2>/dev/null | \
    grep -Ei "program_f|journey|fallback|error|exception|import" | \
    tail -30 || echo "(no relevant log lines found)"

echo ""
echo "=== Deployment complete ==="
echo "HEAD: $HEAD"
echo "To verify fallback is NOT active, run:"
echo "  docker compose -f $COMPOSE_FILE logs --since=5m $COMM_SERVICE | grep -i 'fallback'"
