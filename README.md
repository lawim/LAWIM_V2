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

## Sauvegarde et reprise après sinistre

- Google Drive cible: 02:00 et 14:30 WAT
- Réplication locale: continue ou quasi continue lorsque le disque est connecté
- Disque externe: copie hebdomadaire hors serveur
- Cockpit: pilotage, historique et alertes
- Tests de restauration: hebdomadaires, mensuels et trimestriels selon le niveau
- Documentation canonique: [docs/disaster-recovery/README.md](docs/disaster-recovery/README.md)

Les details operatoires, les statuts `CIBLE / IMPLEMENTE / DEPLOYE / TESTE / VALIDE` et les chemins actifs sont centralises dans la documentation BDR canonique.

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
| `docs/disaster-recovery/` | Canonical Disaster Recovery Framework documentation |
| `OPS/OVH/` | Déploiement, sauvegardes, incidents |
| `reports/handover/` | Document maître de passation |
| `compose/` | Docker Compose canonique |

## Branche officielle

**`main`** — seule branche de production. Toute modification transite par : local → Git → préproduction → production.
