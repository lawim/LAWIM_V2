#!/usr/bin/env bash
# LAWIM — Script de mise en service progressive
# Usage: sudo bash deployment/scripts/go-live.sh
# Ce script est conçu pour être exécuté étape par étape sur le serveur de production.

set -euo pipefail

DOMAIN="${1:-lawim.cm}"
REPO_DIR="/home/lawim/LAWIM_V2"
ENV_FILE="${REPO_DIR}/deployment/secrets/production.env"

echo "=========================================="
echo " LAWIM — Mise en service"
echo "=========================================="
echo ""

# ---- Étape 0 : Vérification ----
echo "=== [0] Vérification préalable ==="
if [ ! -f "${ENV_FILE}" ]; then
    echo "ERREUR: ${ENV_FILE} introuvable. Exécuter d'abord provision-server.sh"
    exit 1
fi
source "${ENV_FILE}" 2>/dev/null || true

# Vérifier que les services tournent
docker compose -f "${REPO_DIR}/deployment/compose/docker-compose.prod.yml" ps 2>/dev/null || {
    echo "ERREUR: Docker Compose ne répond pas. Démarrer avec provision-server.sh"
    exit 1
}

echo "OK — Services actifs."

# ---- Étape 1 : Santé ----
echo ""
echo "=== [1] Health Check ==="
curl -s "https://${DOMAIN}/health" | python3 -m json.tool || echo "ATTENTION: health check échoué"

# ---- Étape 2 : Migrations ----
echo ""
echo "=== [2] Migrations ==="
docker compose -f "${REPO_DIR}/deployment/compose/docker-compose.prod.yml" run --rm app \
    python3 -m lawim_runtime.production.migrate || echo "ERREUR: migrations"

# ---- Étape 3 : Backup initial ----
echo ""
echo "=== [3] Backup initial ==="
bash "${REPO_DIR}/deployment/scripts/backup.sh"

# ---- Étape 4 : Feature flags progressifs ----
echo ""
echo "=== [4] Activation des feature flags ==="
echo ""
echo "Activer dans ${ENV_FILE} dans cet ordre :"
echo ""
echo "  Étape 4a — Pipeline déterministe uniquement"
echo "    interaction_gateway_enabled=true"
echo ""
echo "  Étape 4b — WhatsApp"
echo "    whatsapp_adapter_enabled=true"
echo "    GREEN_API_INSTANCE=..."
echo "    GREEN_API_TOKEN=..."
echo ""
echo "  Étape 4c — Telegram"
echo "    telegram_adapter_enabled=true"
echo "    TELEGRAM_BOT_TOKEN=..."
echo ""
echo "  Étape 4d — IA (optionnel)"
echo "    LROS_AI_INTELLIGENCE_ENABLED=true"
echo "    LROS_AI_EXTRACTION_ENABLED=true"
echo "    LROS_AI_RESPONSE_WRITER_ENABLED=true"
echo "    LROS_AI_SHADOW_MODE=false"
echo "    LROS_AI_PROVIDER_CALLS_ENABLED=true"
echo "    OPENAI_API_KEY=..."
echo "    LROS_AI_BUDGET_MONTHLY_CENTS=5000"

# ---- Étape 5 : Redémarrage ----
echo ""
echo "=== [5] Redémarrage avec les nouveaux flags ==="
echo "  docker compose -f deployment/compose/docker-compose.prod.yml down"
echo "  docker compose -f deployment/compose/docker-compose.prod.yml up -d"
echo "  docker compose logs -f"

# ---- Étape 6 : Test manuel ----
echo ""
echo "=== [6] Test manuel ==="
echo "  Après redémarrage, envoyer un message WhatsApp au numéro LAWIM."
echo "  Vérifier les logs : docker compose logs app | grep 'correlation_id'"
echo "  Vérifier la réponse : le bot doit répondre."
echo ""

echo "=========================================="
echo " PROCHAINES ÉTAPES"
echo "=========================================="
echo ""
echo "  1. Vérifier les logs toutes les 5 minutes"
echo "  2. Surveiller les métriques Prometheus"
echo "  3. Créer le premier bien immobilier"
echo "  4. Inviter le premier utilisateur"
echo "  5. NOTER le premier bug et le CORRIGER"
echo "  6. Mesurer : conversations, projets, temps de réponse"
echo "=========================================="
