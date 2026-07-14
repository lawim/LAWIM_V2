# Deploiement Operations Et Reprise

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Fondations conservees
PostgreSQL, Redis, Docker, infrastructure de deploiement, monitoring, backup et disaster recovery sont KEEP_AND_CLEAN.

## Runbooks
Les runbooks operationnels peuvent rester dans `OPS/`, `deployment/`, `docker/` ou les dossiers de reprise s'ils documentent l'exploitation et pointent vers le canon pour les responsabilites produit.

## Regles
Aucune validation de deploiement ne valide un comportement metier sans tests d'acceptation. Les procedures de restauration doivent prouver donnees, secrets, medias, base et version applicative.

## Mission 2 - Mode Maintenance

Le deploiement Mission 2 doit exposer:

- `GET /api/v2/maintenance/status`
- `POST /api/v2/maintenance/messages`
- `POST /api/v2/maintenance/handover`

Avant deploiement OVH:

- sauvegarde PostgreSQL;
- verification des Recovery Bundles;
- verification des flags `lawim_core_rebuild_maintenance_mode=true` et services decommissionnes `false`;
- verification des webhooks WhatsApp et Telegram comme transports techniques;
- verification qu'aucune route assistant, matching ou relation legacy ne repond autrement que 404.

Validation locale Mission 2 realisee: compilation Python, tests maintenance, tests backend cibles, typecheck frontend, build frontend, tests frontend et validation documentaire canonique. Le deploiement OVH et les tests live Web/WhatsApp/Telegram restent a executer dans l'environnement d'exploitation.
