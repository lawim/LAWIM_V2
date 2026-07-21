# LAWIM — Écart Local / Production

**Date :** 2026-07-21
**HEAD (local) :** 1258fe19
**Serveur OVH :** vps-6da158cc.vps.ovh.net (164.132.44.192)

## Comparaison

| Élément | Local (HEAD) | Production (OVH) | Écart |
|---------|-------------|-------------------|-------|
| Commit HEAD | 1258fe19 | NON DÉPLOYÉ | N/A |
| Branch | release/final-acceptance-and-ovh-readiness-20260721 | N/A | N/A |
| Schéma DB | Chantiers 1–4 + conversation_v2 | NON DÉPLOYÉ | N/A |
| Image Docker API | lawim_v2/app:local | NON DÉPLOYÉE | N/A |
| Image Docker backend | build local | NON DÉPLOYÉE | N/A |
| Variables d'environnement | .env.local | NON CONFIGURÉES | N/A |
| Secrets | deployment/secrets/*.env | NON CONFIGURÉS | N/A |
| Nginx configuration | deployment/nginx/ | NON DÉPLOYÉE | N/A |
| Frontend build | frontend/dist/ | NON DÉPLOYÉ | N/A |
| Certificats SSL | deployment/nginx/ssl/ | NON CONFIGURÉS | N/A |
| Base PostgreSQL | locale (SQLite/PostgreSQL) | NON DÉPLOYÉE | N/A |
| Redis | local | NON DÉPLOYÉ | N/A |

## État de l'infrastructure OVH existante

Le serveur OVH VPS (vps-6da158cc.vps.ovh.net) existe et est accessible.
Les déploiements précédents (programmes A–T, missions 1–4) ont été effectués sur ce serveur, mais la reconstruction conversationnelle complète (Chantiers 1–5) n'a jamais été déployée.

Les composants suivants sont présents sur OVH (déploiement legacy) :

- Docker Engine et Docker Compose
- PostgreSQL 16 (données programmes A–T)
- Redis 7
- Nginx avec certificats SSL Let's Encrypt
- Images Docker legacy taguées

## Écart constaté

Aucun écart à signaler — LAWIM_V2 conversation rebuild (Chantier 1–5) n'a jamais été déployé sur OVH. Le déploiement de la version actuelle constituera le premier déploiement de cette reconstruction complète.

## Recommandation

1. Procéder au déploiement contrôlé après validation du release candidate (2.0.0-rc.1)
2. Sauvegarder la base de données OVH existante avant déploiement
3. Utiliser le runbook de déploiement OVH documenté
4. Exécuter les smoke tests post-déploiement
5. En cas d'échec, exécuter le rollback immédiat
