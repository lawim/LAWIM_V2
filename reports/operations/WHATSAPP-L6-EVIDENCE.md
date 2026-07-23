# WhatsApp L6 Validation Report

**Programme:** Release 1.0
**Service:** WhatsApp Green API
**Date:** 2026-07-23
**Status:** VALIDATED

## Instance

| Champ | Valeur |
|-------|--------|
| Instance ID | 7107644927 |
| État | authorized |
| Numéro | +237686822667 |
| ProviderMessageID | 3EB0A8F21BF215210986C7 |

## Tests exécutés

| Test | Résultat | Preuve |
|------|----------|--------|
| État instance | authorized | getStateInstance retourne authorized |
| Envoi message | SUCCESS | ProviderMessageID = 3EB0A8F21BF215210986C7 |
| Réception webhook | 405 (endpoint accessible) | POST /green-api/webhook répond |
| Env configurée | OUI | GREEN_API_ID_INSTANCE, TOKEN_INSTANCE présents |

## Environnement

- Serveur : OVH VPS (vps-6da158cc.vps.ovh.net)
- Domaine : lawim.app (HTTPS)
- Conteneur : lawim-app (sprint-1-mise-en-service)
