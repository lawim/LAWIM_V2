#!/usr/bin/env bash
# LAWIM — Rapport quotidien
# Usage: bash deployment/scripts/daily-report.sh
# Produit les métriques du jour directement depuis l'application.

set -euo pipefail

API_BASE="${1:-http://localhost:3000}"
DATE=$(date +%Y-%m-%d)

echo "=========================================="
echo " LAWIM — Rapport quotidien"
echo " Date : ${DATE}"
echo "=========================================="

# Health
echo ""
echo "--- Santé ---"
curl -s "${API_BASE}/health" | python3 -m json.tool 2>/dev/null || echo "Health check: INDISPONIBLE"

# Métriques (via endpoint /metrics si disponible)
echo ""
echo "--- Métriques du jour ---"
if curl -s "${API_BASE}/metrics" -o /dev/null; then
    curl -s "${API_BASE}/metrics" | grep -E "^interaction_|^ai_|^delivery_" | sort
else
    echo "Endpoint /metrics non disponible"
fi

# Logs récents
echo ""
echo "--- Dernières interactions ---"
docker compose logs --since="24h" app 2>/dev/null | grep -i "correlation_id" | tail -20 || echo "Aucune interaction aujourd'hui"

echo ""
echo "--- Erreurs (24h) ---"
docker compose logs --since="24h" app 2>/dev/null | grep -i "error\|exception\|traceback" | tail -10 || echo "Aucune erreur"

echo ""
echo "=========================================="
echo " FIN DU RAPPORT"
echo "=========================================="
