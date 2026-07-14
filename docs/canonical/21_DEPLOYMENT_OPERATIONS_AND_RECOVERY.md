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
