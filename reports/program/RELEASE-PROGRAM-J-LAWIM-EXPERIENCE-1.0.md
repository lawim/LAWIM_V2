# RELEASE PROGRAM J - LAWIM EXPERIENCE 1.0

## Rapport de livraison et de mise en production

**Date de livraison**: 7 juillet 2026  
**Environnement**: OVH production (`https://lawim.app`)  
**Release family**: LAWIM Experience 1.0

## Résumé exécutif

La refonte de l'experience utilisateur LAWIM est livree et operationnelle en production. La page d'acces est sobre, sans demande de role, avec logo LAWIM et slogan visibles. Le login est pilote par le role retourne par l'API, puis redirige automatiquement vers le dashboard correspondant.

Le deploiement OVH a ete realise proprement depuis une release traçable. Les services `lawim-app`, `lawim-postgres` et `lawim-redis` sont revenus healthy. Les verifications HTTP et d'authentification sont concluantes.

## References de release

- Commit code principal: `778ab779bcd69a585a29e0ac42b74f331df7538e`
- Commit de packaging release: `0bbb39f8`
- Commit final du rapport: `a9a5cb5f`
- Tag de release cible: `release-program-j-lawim-experience-1.0`
- Artefact OVH: `release/ovh/artefacts/lawim-v2-postgresql-compat.tar.gz`
- SHA256 artefact: `6d9d5d8deb07f05e447676374d78da2de61b6b6b1ddf3fc4ad91ac339aa504d7`

## Source frontend officielle de production

Decision officielle: `code/lawim_v2/static`

Motifs:
- `code/lawim_v2/server.py` sert directement `/`, `/app.js` et `/styles.css` depuis cette arborescence.
- Le stack OVH actif rebuild `lawim-app` depuis `/opt/lawim/current` via `deployment/docker/Dockerfile.backend`.
- Le fichier `frontend/apps/web` reste une surface React de developpement et de tests, mais il ne constitue pas la source runtime de production.
- `frontend/dist` contient des artefacts de build, pas la source officielle de service.

## Travaux livres

- Page d'acces reconstruite avec:
  - email
  - mot de passe
  - logo LAWIM
  - slogan LAWIM
  - design sobre et professionnel
- Suppression de toute demande de role au login.
- Routage automatique vers le dashboard selon le role retourne par l'API.
- Normalisation des roles officiels:
  - `admin`
  - `agent`
  - `owner`
- Instrumentation preservee et utile:
  - `LOGIN_OK`
  - `ROLE_RESOLVED`
  - `DASHBOARD_SELECTED`
  - `DASHBOARD_RENDERED`
  - `APPLY_JOURNEY`
  - `REFRESH_START`
  - `REFRESH_DONE`
  - `RENDER_DONE`
- Messages d'erreur login durcis:
  - identifiants incorrects
  - serveur indisponible
  - session expiree
  - acces non autorise
- Comptes de validation prod alignes sur les trois roles officiels:
  - `admin@lawim.app`
  - `agent@lawim.app`
  - `owner@lawim.app`

## Validation locale

Les validations locales associees a cette mission ont ete executees avant la promotion OVH:

- Frontend Vitest: `npm test -- --run`
  - 28 fichiers passes
  - 119 tests passes
- Build frontend: `npm run build`
- Python unittest ciblees:
  - `tests.test_lawim_v2`
  - `tests.test_source_intelligence`
  - `tests.test_week002_production`
  - `tests.test_i18n_languages`
  - 43 tests passes

## Validation production

Services:
- `lawim-app` healthy
- `lawim-postgres` healthy
- `lawim-redis` healthy

HTTP:
- `https://lawim.app/` -> `200`
- `https://lawim.app/login` -> `200`
- `https://lawim.app/healthz` -> `200`

Authentification:
- `admin@lawim.app` -> role `admin`, token emis
- `agent@lawim.app` -> role `agent`, token emis
- `owner@lawim.app` -> role `owner`, token emis

Observations:
- La page d'acces ne montre pas de selecteur de role.
- Aucun compte demo n'est expose dans l'interface publique.
- Aucun HTTP 500 n'a ete observe sur les points verifies.

## Deploiement OVH

Sequence executee:
1. Backup pre-deploiement capture.
2. Release preparee sous `/opt/lawim/releases/0bbb39f8`.
3. `/opt/lawim/current` pointe vers `/opt/lawim/releases/0bbb39f8`.
4. `docker compose --env-file /opt/lawim/secrets/.env -f /opt/lawim/compose/docker-compose.ovh.yml up -d --build`
5. Relevement des services healthy.
6. Verifications HTTP et login.

Symlink actif:
- `/opt/lawim/current -> /opt/lawim/releases/0bbb39f8`

## Sauvegardes

Sauvegarde pre-deploiement creee:
- `/opt/lawim/backups/mission05_predeploy_20260707_220125.tar.gz`

Contenu logique de la sauvegarde:
- dump PostgreSQL
- medias
- configurations
- checksums

## Procedure de rollback

Rollback release:
1. Rebasculer `/opt/lawim/current` vers la release precedente.
2. Redemarrer `lawim-app` avec le compose OVH.
3. Revalider `/`, `/login` et `/healthz`.

Rollback donnees:
1. Restaurer la sauvegarde `mission05_predeploy_20260707_220125.tar.gz`.
2. Recharger PostgreSQL et les medias si necessaire.

Rollback credentials:
1. Repasser les comptes de validation par le runtime officiel si une remise a plat est requise.
2. Conserver les secrets hors Git.

## Rapport de cohérence

La coherence globale est maintenue sur les axes suivants:
- fonctionnel
- ergonomique
- technique
- documentaire
- operationnel
- commercial
- strategique

Le produit est coherent avec la doctrine LAWIM:
- le role n'est jamais demande au login
- la decision reste cote API
- l'UX reste sobre et lisible
- le frontend de production reste celui du runtime statique servi par `code/lawim_v2/static`

## Notes

- Les changements preexistants hors perimetre de mission ont ete conserves sans ecrasement.
- Le secret admin de validation a ete gere hors Git et n'est pas documente en clair dans ce depot.
