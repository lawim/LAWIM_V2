# LAWIM_V2 — Guide de diffusion Beta 1.0.0

Guide destiné aux **testeurs autorisés** pour installer, valider et évaluer LAWIM_V2 Beta 1.0.0 en environnement contrôlé.

| Référence | Valeur |
|-----------|--------|
| Version | **v1.0.0-beta** |
| Branche | `release/1.0.0-beta` |
| Tag recommandé | `v1.0.0-beta-validated` |
| Validation | [reports/program/BETA-1.0.0-RELEASE-VALIDATION-REPORT.md](reports/program/BETA-1.0.0-RELEASE-VALIDATION-REPORT.md) |

---

## 1. Prérequis

### Obligatoires

| Composant | Version / note |
|-----------|----------------|
| **Python** | 3.12 ou 3.13 |
| **Git** | pour cloner ou checkout du tag |
| **OS** | Linux ou macOS recommandé ; WSL2 acceptable |
| **Espace disque** | ~500 Mo (dépôt + venv + données runtime) |
| **Port local** | 3000 disponible (configurable via `LAWIM_PORT`) |

### Optionnels

| Composant | Usage |
|-----------|--------|
| **Docker + Compose** | stack conteneurisée dev / postgres |
| **Node.js** | vérification syntaxe JS (CI locale) ; non requis pour tester l'UI |
| **pg8000** | driver PostgreSQL (`pip install -r requirements-postgresql.txt`) |

### Accès

- Dépôt ou archive fournie par l'équipe LAWIM (ne pas publier publiquement sans accord).
- Aucun secret réel requis pour la Beta : comptes démo inclus (§7).

---

## 2. Installation

### Option A — depuis Git (recommandé)

```bash
git clone <url-fournie> lawim_v2
cd lawim_v2
git checkout v1.0.0-beta-validated   # ou v1.0.0-beta
./scripts/install.sh
```

Variables d'installation optionnelles :

| Variable | Effet |
|----------|--------|
| `LAWIM_INSTALL_POSTGRES_DRIVER=1` | installe `pg8000` |
| `LAWIM_INSTALL_PACKAGE=1` | `pip install -e ".[postgresql]"` |

Un fichier `.env.local` est créé depuis `env/development/.env.example` s'il n'existe pas.

### Option B — paquet Python (editable)

```bash
pip install -e ".[postgresql]"
python -m lawim_v2 --help
```

### Vérification post-install

```bash
./infra/check-env.sh
```

---

## 3. Validation

Exécuter la gate reproductibilité **avant** de tester l'UI :

```bash
./scripts/validate-install.sh
```

Résultat attendu : `=== INSTALL VALIDATION OK ===`

Validations individuelles (optionnel) :

```bash
./scripts/validate-packaging.sh
./scripts/run-tests.sh
python3 scripts/validate_prisma_manifest.py
python3 scripts/smoke_runtime.py
```

En cas d'échec : noter la commande, le message d'erreur complet et joindre au retour (§9).

---

## 4. Lancement local (SQLite)

```bash
./scripts/run-local.sh
```

| URL | Rôle |
|-----|------|
| http://127.0.0.1:3000 | Console web |
| http://127.0.0.1:3000/api/health | Health minimal public |
| http://127.0.0.1:3000/api/bootstrap | Données initiales UI |

Variables utiles :

| Variable | Défaut |
|----------|--------|
| `LAWIM_HOST` | `127.0.0.1` |
| `LAWIM_PORT` | `3000` |
| `LAWIM_DB_PATH` | `data/runtime/lawim.sqlite3` |
| `LAWIM_SEED_DEMO_DATA` | `true` |

Arrêt : `Ctrl+C` dans le terminal du serveur.

---

## 5. Lancement Docker Compose

### Dev (SQLite, code monté)

```bash
./scripts/run-compose-dev.sh
```

UI : http://localhost:3000

Arrêt :

```bash
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml down
```

### Staging / production (référence)

```bash
./scripts/run-compose-staging.sh    # profil staging
./scripts/run-compose-prod.sh       # profil prod, seed demo off par défaut
```

Documentation Compose : [compose/README.md](compose/README.md)

---

## 6. Activation PostgreSQL optionnelle

PostgreSQL **n'est pas obligatoire**. SQLite reste le moteur par défaut.

### Via Compose

```bash
./scripts/run-compose-postgres.sh
```

Variables par défaut (placeholders locaux — **ne pas utiliser en production réelle**) :

| Variable | Défaut |
|----------|--------|
| `LAWIM_DB_DRIVER` | `postgresql` |
| `LAWIM_DATABASE_URL` | `postgresql://lawim:lawim@postgres:5432/lawim_v2` |
| `LAWIM_DB_FALLBACK` | `true` (retour SQLite si PG indisponible) |

### Native (sans Docker)

```bash
export LAWIM_INSTALL_POSTGRES_DRIVER=1
./scripts/install.sh
export LAWIM_DB_DRIVER=postgresql
export LAWIM_DATABASE_URL=postgresql://lawim:lawim@localhost:5432/lawim_v2
export LAWIM_DB_FALLBACK=false
./scripts/run-local.sh
```

Schéma et migrations : [docs/MIGRATIONS.md](docs/MIGRATIONS.md)

---

## 7. Parcours à tester

Mot de passe démo : **`lawim-demo`**

| Compte | Email | Rôle |
|--------|-------|------|
| Admin | `admin@lawim.local` | supervision, orgs, users |
| Agent | `agent@lawim.local` | agent immobilier |
| Owner | `owner@lawim.local` | propriétaire / vendeur |

### Parcours Guest (sans login)

1. Ouvrir http://127.0.0.1:3000
2. Vérifier le chargement bootstrap
3. Parcourir les listings publics (`GET /api/properties`)
4. Lancer une recherche matching (`/api/matches?city=Douala`)
5. Confirmer que `/api/health` ne expose pas d'audit sans auth

### Parcours Buyer

1. Login `owner@lawim.local` / `lawim-demo`
2. Rechercher des biens (filtres ville, budget)
3. Consulter les matches et le détail score
4. Ouvrir ou créer une conversation sur un bien
5. Envoyer un message ; vérifier les notifications

### Parcours Seller

1. Login agent ou owner
2. Créer un bien (draft) via l'UI ou `POST /api/properties`
3. Ajouter un média (JPEG valide)
4. Publier le bien (`POST /api/properties/{id}/publish`)
5. Vérifier visibilité dans la liste publique

### Parcours Admin

1. Login `admin@lawim.local`
2. Lister users et organizations
3. Consulter `/api/events` (journal audit)
4. Health détaillé avec token admin
5. Tenter une action interdite en tant qu'owner (doit retourner 403)

### Checklist rapide

- [ ] Install + validate-install OK
- [ ] Login / logout
- [ ] CRUD property (draft → publish)
- [ ] Upload média JPEG
- [ ] Matching avec critères ville/budget
- [ ] Conversation + message
- [ ] Erreurs API lisibles `[code] message` dans l'UI

---

## 8. Limites connues

| Limite | Impact |
|--------|--------|
| Pas de rate limiting HTTP | ne pas exposer sur Internet public |
| Médias `/media/*` sans auth | chemins prévisibles ; usage lab uniquement |
| UI statique vanilla | pas de build SPA ; pas de tests E2E navigateur fournis |
| PostgreSQL local non testé par défaut | skip CI local ; optionnel via Compose |
| Pas de registry / CD public | installation depuis source ou archive interne |
| Directive v1.0 complète | aspirational ; voir `docs/OPERATIONS-RC.md` pour le runtime réel |
| Mots de passe démo fixes | **interdit en production** |

---

## 9. Procédure de retour

1. Remplir [BETA_TESTER_FEEDBACK_TEMPLATE.md](BETA_TESTER_FEEDBACK_TEMPLATE.md)
2. Joindre :
   - OS, Python version (`python3 --version`)
   - Résultat `./scripts/validate-install.sh` (OK / échec + log)
   - Captures ou description des écarts
   - Steps to reproduce pour tout bug
3. Envoyer au canal défini par l'équipe LAWIM (email / ticket / repo privé)
4. Ne **pas** committer de secrets, dumps DB réels, ni captures contenant des données personnelles

Priorité des retours :

| Priorité | Exemple |
|----------|---------|
| P0 | crash, perte de données, faille sécurité |
| P1 | parcours bloqué, régression API |
| P2 | UX, doc, suggestion |

---

## 10. Consignes de sécurité

1. **Environnement lab uniquement** — ne pas déployer la Beta sur un réseau public sans durcissement additionnel.
2. **Comptes démo** — changer ou désactiver avant toute démo externe ; mot de passe connu (`lawim-demo`).
3. **Secrets** — ne jamais committer `.env.local` avec secrets réels ; utiliser `env/*/.secrets.example` comme référence de forme.
4. **PostgreSQL Compose** — mots de passe `lawim/lawim` sont des placeholders locaux.
5. **Production** — `LAWIM_SEED_DEMO_DATA=false` et `APP_ENV=production` requis ; seed demo interdit en production par validation config.
6. **Données** — utiliser uniquement des données fictives ; supprimer `data/runtime/` après tests si nécessaire.
7. **Mises à jour** — rester sur le tag `v1.0.0-beta-validated` sauf instruction contraire de l'équipe.

---

## Documents associés

| Document | Contenu |
|----------|---------|
| [CHANGELOG_BETA_1.0.0.md](CHANGELOG_BETA_1.0.0.md) | Notes de version |
| [BETA_TESTER_FEEDBACK_TEMPLATE.md](BETA_TESTER_FEEDBACK_TEMPLATE.md) | Formulaire retour |
| [docs/OPERATIONS-RC.md](docs/OPERATIONS-RC.md) | Exploitation RC |
| [README.md](README.md) | Vue d'ensemble technique |
