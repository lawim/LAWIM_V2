#!/usr/bin/env bash
set -euo pipefail

LAWIM_VERSION="${LAWIM_VERSION:-$(git rev-parse --short HEAD)}"
COMPOSE_FILE="deployment/compose/docker-compose.prod.yml"
ENV_FILE="deployment/secrets/production.env"
DEPLOY_LOG="deployment/journal/deploy-$(date +%Y%m%d-%H%M%S).log"

mkdir -p deployment/journal

echo "[$(date -Iseconds)] LAWIM Production Deployment v${LAWIM_VERSION}" | tee -a "${DEPLOY_LOG}"
echo "[$(date -Iseconds)] Compose file: ${COMPOSE_FILE}" | tee -a "${DEPLOY_LOG}"
echo "[$(date -Iseconds)] Env file: ${ENV_FILE}" | tee -a "${DEPLOY_LOG}"

if [ ! -f "${ENV_FILE}" ]; then
    echo "[ERROR] ${ENV_FILE} not found. Create it from deployment/secrets/.env.example" | tee -a "${DEPLOY_LOG}"
    exit 1
fi

echo "[$(date -Iseconds)] Pulling images..." | tee -a "${DEPLOY_LOG}"
docker compose -f "${COMPOSE_FILE}" --env-file "${ENV_FILE}" pull

echo "[$(date -Iseconds)] Running database migrations..." | tee -a "${DEPLOY_LOG}"
docker compose -f "${COMPOSE_FILE}" --env-file "${ENV_FILE}" run --rm app \
    python3 -m lawim_runtime.production.migrate

echo "[$(date -Iseconds)] Starting services..." | tee -a "${DEPLOY_LOG}"
docker compose -f "${COMPOSE_FILE}" --env-file "${ENV_FILE}" up -d

echo "[$(date -Iseconds)] Waiting for health checks..." | tee -a "${DEPLOY_LOG}"
sleep 10

for i in $(seq 1 12); do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/health 2>/dev/null || echo "000")
    if [ "${STATUS}" = "200" ]; then
        echo "[$(date -Iseconds)] Health check OK (attempt ${i})" | tee -a "${DEPLOY_LOG}"
        break
    fi
    echo "[$(date -Iseconds)] Waiting... (attempt ${i}, status=${STATUS})" | tee -a "${DEPLOY_LOG}"
    sleep 5
done

echo "[$(date -Iseconds)] Deployment complete." | tee -a "${DEPLOY_LOG}"
echo "=== Image versions ===" | tee -a "${DEPLOY_LOG}"
docker compose -f "${COMPOSE_FILE}" images | tee -a "${DEPLOY_LOG}"

echo "=== Running containers ===" | tee -a "${DEPLOY_LOG}"
docker compose -f "${COMPOSE_FILE}" ps | tee -a "${DEPLOY_LOG}"
