#!/usr/bin/env bash
set -euo pipefail

PREVIOUS_VERSION="${1:?Usage: $0 <previous_version_commit_or_tag>}"
COMPOSE_FILE="deployment/compose/docker-compose.prod.yml"
ENV_FILE="deployment/secrets/production.env"
ROLLBACK_LOG="deployment/journal/rollback-$(date +%Y%m%d-%H%M%S).log"

mkdir -p deployment/journal

echo "[$(date -Iseconds)] LAWIM Rollback to ${PREVIOUS_VERSION}" | tee -a "${ROLLBACK_LOG}"

echo "[$(date -Iseconds)] Stopping current services..." | tee -a "${ROLLBACK_LOG}"
docker compose -f "${COMPOSE_FILE}" down

echo "[$(date -Iseconds)] Checking out previous version..." | tee -a "${ROLLBACK_LOG}"
git checkout "${PREVIOUS_VERSION}"

echo "[$(date -Iseconds)] Building images for ${PREVIOUS_VERSION}..." | tee -a "${ROLLBACK_LOG}"
LAWIM_VERSION="${PREVIOUS_VERSION}" docker compose -f "${COMPOSE_FILE}" --env-file "${ENV_FILE}" build

echo "[$(date -Iseconds)] Starting previous version..." | tee -a "${ROLLBACK_LOG}"
LAWIM_VERSION="${PREVIOUS_VERSION}" docker compose -f "${COMPOSE_FILE}" --env-file "${ENV_FILE}" up -d

echo "[$(date -Iseconds)] Running rollback database migrations..." | tee -a "${ROLLBACK_LOG}"
docker compose -f "${COMPOSE_FILE}" --env-file "${ENV_FILE}" run --rm app \
    python3 -m lawim_runtime.production.migrate --rollback

echo "[$(date -Iseconds)] Rollback to ${PREVIOUS_VERSION} complete." | tee -a "${ROLLBACK_LOG}"
