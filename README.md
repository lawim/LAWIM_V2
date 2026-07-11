# LAWIM_V2

Plateforme immobilière camerounaise : conversation intelligente, matching biens/partenaires, consentement et mise en relation.

**État actuel** : Mission 12 clôturée — Sauvegardes, reprise après sinistre, environnements local/préproduction.
**Mission suivante** : Mission 13 — Paiements CamPay, facturation, activation des services.

## Architecture active

```
Frontend React (Vite/TS)  ←→  API SDK  ←→  Backend Python 3.12  ←→  PostgreSQL 16 + Redis 7
                                   ↑                                    ↑
                            Docker Compose                        Serveur OVH
```

## Prérequis

- Python 3.12+, Docker Compose, Node.js 20+
- **Production** : serveur OVH, PostgreSQL 16, Redis 7, Let's Encrypt, Nginx

## Démarrage local rapide

```bash
./scripts/dev/start-local.sh      # Build + démarre Docker (postgres + backend)
./scripts/dev/stop-local.sh       # Arrête
./scripts/dev/reset-local.sh      # Arrête + reset volumes
./scripts/dev/run-tests.sh        # Tests backend + frontend
./scripts/dev/restore-backup.sh   # Restaure une sauvegarde depuis Drive
```

Démarrage alternatif (sans Docker) :
```bash
./scripts/run-local.sh            # SQLite direct
```

## Tests

```bash
./scripts/dev/run-tests.sh                  # Tout
cd frontend && npm test -- --run            # Frontend seulement (138 tests)
PYTHONPATH=code python3 -m pytest code/lawim_v2/brain/tests.py -v  # Backend (67 tests)
```

## Production OVH

| Composant | Statut |
|-----------|--------|
| Backend | Docker, port 3000, Python 3.12 |
| Frontend | Servi par Nginx, build Vite |
| PostgreSQL | 16 alpine, 420 tables |
| Redis | 7 alpine |
| SSL | Let's Encrypt, HTTP/2 |
| Nginx | Reverse proxy + static files |
| Stockage média | Volume Docker `/app/data/runtime/media` |

## Sauvegardes automatisées

- **Fréquence** : 03:00 et 15:00 (fuseau WAT, basse activité)
- **Contenu** : PostgreSQL dump, fichiers médias, configuration
- **Chiffrement** : AES-256-CBC + PBKDF2
- **Checksums** : SHA-256 vérifiés
- **Destination** : Google Drive via rclone (OAuth 2.0)
- **Rétention** : 48h complet → 7j → 4 sem → 3 mois
- **Service** : `lawim-backup.service` (systemd oneshot)
- **Scripts** : `scripts/ops/backup-production.sh`, `scripts/ops/restore-production.sh`

**Restauration** :
```bash
sudo /opt/lawim/current/scripts/ops/restore-production.sh <BACKUP_ID> --decrypt-key "votre-cle"
```

## Santé

```bash
curl https://lawim.app/healthz     # → "ok"
curl https://lawim.app/readyz      # → {"status":"ready","database":true,"storage":true}
```

## Missions clôturées

| Mission | Description | Rapport |
|---------|-------------|---------|
| 10 | Brain conversationnel | `reports/product_reviews/Mission_10_Report.md` |
| 11 | Moteur relationnel | `reports/product_reviews/Mission_11_Report.md` |
| 12 | Sauvegardes, DR, local, préproduction | `reports/product_reviews/Mission_12_Report.md` |

## Documentation active

| Document | Contenu |
|----------|---------|
| `docs/PRODUCT_BIBLE/` | Spécifications produit |
| `docs/Directive/` | Références métier |
| `OPS/OVH/` | Déploiement, sauvegardes, incidents |
| `reports/handover/` | Document maître de passation |
| `compose/` | Docker Compose canonique |
| `scripts/ops/` | Sauvegarde et restauration |

## Branche officielle

**`main`** — seule branche de production. Toute modification transite par : local → Git → préproduction → production.
