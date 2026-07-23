#!/usr/bin/env bash
# LAWIM — Provisionnement complet du serveur de production
# Usage: bash deployment/scripts/provision-server.sh lawim.cm
# Prérequis: Ubuntu 22.04+, accès root ou sudo, domaine pointant vers ce serveur

set -euo pipefail
DOMAIN="${1:?Usage: $0 <domain>}"
LAWIM_USER="lawim"
LAWIM_HOME="/home/${LAWIM_USER}"
LAWIM_REPO="${LAWIM_HOME}/LAWIM_V2"
ENV_FILE="${LAWIM_REPO}/deployment/secrets/production.env"

echo "=========================================="
echo " LAWIM — Provisionnement serveur"
echo " Domaine : ${DOMAIN}"
echo " Date    : $(date -Iseconds)"
echo "=========================================="

export DEBIAN_FRONTEND=noninteractive

# ---- 1. Mise à jour système ----
echo "[1/10] Mise à jour système..."
apt-get update && apt-get upgrade -y
apt-get install -y curl git ufw fail2ban unattended-upgrades

# ---- 2. Docker ----
echo "[2/10] Installation Docker..."
if ! command -v docker &>/dev/null; then
    curl -fsSL https://get.docker.com | bash
    usermod -aG docker "${LAWIM_USER}" 2>/dev/null || true
fi

# ---- 3. Docker Compose ----
echo "[3/10] Installation Docker Compose..."
if ! command -v docker compose &>/dev/null; then
    curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# ---- 4. Création utilisateur ----
echo "[4/10] Création utilisateur lawim..."
id -u "${LAWIM_USER}" &>/dev/null || useradd --system --create-home --shell /bin/bash "${LAWIM_USER}"
mkdir -p "${LAWIM_HOME}/.ssh" "${LAWIM_HOME}/deployment/backup" "${LAWIM_HOME}/deployment/journal"
chown -R "${LAWIM_USER}:${LAWIM_USER}" "${LAWIM_HOME}"

# ---- 5. Cloner le dépôt ----
echo "[5/10] Clonage du dépôt..."
if [ ! -d "${LAWIM_REPO}" ]; then
    git clone git@github-lawim:lawim/LAWIM_V2.git "${LAWIM_REPO}"
    chown -R "${LAWIM_USER}:${LAWIM_USER}" "${LAWIM_REPO}"
fi

cd "${LAWIM_REPO}"
git checkout release-1.0-20260723

# ---- 6. TLS (Let's Encrypt) ----
echo "[6/10] Configuration TLS..."
apt-get install -y nginx certbot python3-certbot-nginx
cat > "/etc/nginx/sites-available/${DOMAIN}" <<NGINX
server {
    listen 80;
    server_name ${DOMAIN};
    location / { proxy_pass http://127.0.0.1:3000; }
}
NGINX
ln -sf "/etc/nginx/sites-available/${DOMAIN}" /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
certbot --nginx -d "${DOMAIN}" --non-interactive --agree-tos --email admin@${DOMAIN} || true

# ---- 7. Pare-feu ----
echo "[7/10] Configuration pare-feu..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 9090/tcp   # Prometheus (interne)
ufw allow 3001/tcp   # Grafana (interne)

# ---- 8. Fichier .env ----
echo "[8/10] Création fichier .env (éditer manuellement les secrets)..."
if [ ! -f "${ENV_FILE}" ]; then
    cp "${LAWIM_REPO}/deployment/secrets/.env.example" "${ENV_FILE}"
    cat >> "${ENV_FILE}" <<ENV

# --- Configuration LAWIM ---
LAWIM_HOST=0.0.0.0
LAWIM_PORT=3000
PUBLIC_BASE_URL=https://${DOMAIN}
LOG_LEVEL=info
LAWIM_DB_DRIVER=postgresql
LAWIM_DATABASE_URL=postgresql://lawim:\${POSTGRES_PASSWORD}@db:5432/lawim_v3
LAWIM_SESSION_TTL_SECONDS=604800
LAWIM_METRICS_ENABLED=true

# --- Feature flags (activer progressivement) ---
LROS_AI_INTELLIGENCE_ENABLED=false
LROS_AI_EXTRACTION_ENABLED=false
LROS_AI_RESPONSE_WRITER_ENABLED=false
LROS_AI_SHADOW_MODE=true
LROS_AI_PROVIDER_CALLS_ENABLED=false

# --- AI Budget (décommenter pour activer) ---
# LROS_AI_BUDGET_MONTHLY_CENTS=5000
# LROS_AI_MAX_COST_PER_CALL_CENTS=5

# --- PostgreSQL ---
POSTGRES_USER=lawim
POSTGRES_PASSWORD=$(openssl rand -hex 20)
POSTGRES_DB=lawim_v3

# --- Grafana ---
GRAFANA_PASSWORD=$(openssl rand -hex 12)
ENV

    chmod 600 "${ENV_FILE}"
    echo "   Fichier créé : ${ENV_FILE}"
    echo "   ⚠ Éditer les secrets manquants avant de lancer"
fi

# ---- 9. Sauvegarde automatique ----
echo "[9/10] Configuration sauvegarde automatique..."
cat > /etc/cron.d/lawim-backup <<CRON
0 2 * * * ${LAWIM_USER} cd ${LAWIM_REPO} && bash deployment/scripts/backup.sh
0 3 * * 0 ${LAWIM_USER} rsync -avz ${LAWIM_REPO}/deployment/backup/ ${LAWIM_HOME}/backup-remote/
CRON

# ---- 10. Démarrage ----
echo "[10/10] Démarrage des services..."
cd "${LAWIM_REPO}"
docker compose -f deployment/compose/docker-compose.prod.yml --env-file "${ENV_FILE}" pull
docker compose -f deployment/compose/docker-compose.prod.yml --env-file "${ENV_FILE}" up -d

echo ""
echo "=========================================="
echo " PROVISIONNEMENT TERMINÉ"
echo "=========================================="
echo ""
echo " Prochaines étapes :"
echo " 1. Éditer ${ENV_FILE}"
echo "    - OPENAI_API_KEY"
echo "    - GREEN_API_INSTANCE + GREEN_API_TOKEN"
echo "    - TELEGRAM_BOT_TOKEN"
echo "    - CAMPAY_*"
echo ""
echo " 2. Lancer les migrations :"
echo "    docker compose exec app python3 -m lawim_runtime.production.migrate"
echo ""
echo " 3. Vérifier : curl https://${DOMAIN}/health"
echo ""
echo " 4. Activer les canaux un par un :"
echo "    - WhatsApp : whatsapp_adapter_enabled=true"
echo "    - Telegram : telegram_adapter_enabled=true"
echo "    - IA       : LROS_AI_INTELLIGENCE_ENABLED=true"
echo "=========================================="
