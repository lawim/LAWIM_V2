# LAWIM_V2 Product Technical Snapshot

- Date: 2026-06-29
- Scope: etat technique reel du depot apres validation de la baseline executable
- Baseline: `executable-baseline`

## 1. Etat reel du produit

LAWIM_V2 est aujourd hui un monolithe Python 3.12 executable depuis la racine du depot via `python -m lawim_v2`.

- La logique applicative vit dans `code/lawim_v2/`.
- Le paquet racine `lawim_v2/` et `sitecustomize.py` servent de pont pour rendre `code/` importable.
- Le produit expose un serveur HTTP simple, une persistence SQLite, un moteur de matching deterministe et une console navigateur statique.
- La base de donnees embarque les tables `organizations`, `users`, `sessions`, `properties`, `media`, `conversations`, `messages` et `events`.

Le produit reel est donc une baseline executable fonctionnelle, pas encore une plateforme production durcie.

## 2. Ce qui est executable maintenant

- Lancement CLI: `python3 -m lawim_v2`
- Aide CLI: `python3 -m lawim_v2 --help`
- Options visibles: `--host`, `--port`, `--db`, `--no-seed`
- Lancement conteneur: `CMD ["python", "-m", "lawim_v2"]` dans le `Dockerfile`
- API de lecture:
  - `GET /healthz`
  - `GET /api/health`
  - `GET /api/bootstrap`
  - `GET /api/me`
  - `GET /api/organizations`
  - `GET /api/users`
  - `GET /api/properties`
  - `GET /api/properties/{id}`
  - `GET /api/properties/{id}/media`
  - `GET /api/conversations`
  - `GET /api/conversations/{id}`
  - `GET /api/conversations/{id}/messages`
  - `GET /api/matches`
  - `GET /api/media`
- API d'ecriture:
  - `POST /api/auth/login`
  - `POST /api/auth/register`
  - `POST /api/auth/logout`
  - `POST /api/organizations`
  - `POST /api/users`
  - `POST /api/properties`
  - `POST /api/media`
  - `POST /api/conversations`
  - `POST /api/conversations/{id}/messages`
- Frontend statique:
  - login/logout
  - bootstrap runtime
  - recherche de matching
  - creation de property
  - lecture d'une conversation et reponse

Les validations locales ont passe sur:

- compilation Python
- suite `unittest`
- aide CLI
- verification `git diff --check`
- resolution Compose pour les overlays `compose/` et `docker/compose/`

## 3. Ce qui est seulement simule ou minimal

- Le seed demo reste fixe: 3 organisations, 3 utilisateurs, 3 biens, 1 conversation.
- Les medias de demo sont des SVG inline stockes comme URL texte en base.
- Le frontend est du HTML/CSS/JS statique, sans `package.json`, sans framework SPA et sans pipeline de build.
- La couche HTTP ne gere que GET et POST; il n'y a pas de PUT, PATCH ni DELETE.
- Le champ `role` existe, mais il n'y a pas encore d'autorisation basee sur les roles.
- Les workflows GitHub presents dans `.github/workflows/*.example` sont documentaires, pas actifs.
- Les fichiers `docker/Dockerfile.base` et `nginx/` existent comme artefacts, mais les stacks Compose actifs construisent le `Dockerfile` racine et ne branchent pas de service Nginx.

## 4. Ce qui manque

- Une gestion de schema de type migrations versionnees.
- Une persistence non SQLite pour un usage durable.
- Un stockage reel pour les medias et fichiers.
- Des routes de mise a jour et de suppression pour les objets metier.
- Une authorization exploitable par roles et permissions.
- Un vrai packaging Python standard (`pyproject.toml`, `setup.py` ou equivalent) pour une installation classique.
- Une chaine CI/CD active, plus des tests d'integration ou smoke tests contre un processus HTTP reel.
- Les prochains blocs fonctionnels de la roadmap qui ne sont pas encore codes: notifications, dashboard/reporting, paiements, mobile et services IA au-dela du matching deterministe.

## 5. Priorites techniques

1. Stabiliser la persistence avec schema versionne et tests de migration.
2. Durcir le contrat d'API avec vrai CRUD, validation plus stricte et autorisation par roles.
3. Externaliser les actifs persistants, surtout les medias.
4. Ajouter des tests d'integration et un pipeline CI actif sur le vrai runtime.

## 6. Recommandation de la prochaine vague

Recommandation: `WAVE_001 - Durcissement du socle executable`.

Cette vague doit transformer la baseline demo en socle exploitable durablement, sans ouvrir encore les blocs metier plus larges.

- versionner le schema de donnees;
- ajouter l'autorisation par roles et les operations de mise a jour/suppression;
- sortir les medias du stockage inline;
- brancher un chemin de deploiement actif et teste;
- couvrir le runtime avec des smoke tests contre un processus HTTP reel.

## 7. Commandes validees

- `git status --short --branch` PASS, branche `develop`, depot propre
- `git diff --check` PASS
- `git log --oneline -5` PASS
- `git tag --sort=-creatordate | head -10` PASS
- `python3 -m compileall lawim_v2 code/lawim_v2 tests/test_lawim_v2.py` PASS
- `python3 -m unittest discover -s tests -v` PASS, 3 tests
- `python3 -m lawim_v2 --help` PASS
- `docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml config` PASS
- `docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.staging.yml config` PASS
- `docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.prod.yml config` PASS
- `docker compose -f docker/compose/docker-compose.base.yml -f docker/compose/docker-compose.development.yml config` PASS
- `docker compose -f docker/compose/docker-compose.base.yml -f docker/compose/docker-compose.staging.yml config` PASS
- `docker compose -f docker/compose/docker-compose.base.yml -f docker/compose/docker-compose.production.yml config` PASS

## 8. Bloc YAML final

```yaml
program: LAWIM_V2
phase: PRODUCT_DEVELOPMENT
baseline: VALIDATED
snapshot: COMPLETE
blocking_risk: false
recommended_next_wave: WAVE_001
decision_required: true
```
