# LAWIM — État Actuel

**Dernière mise à jour :** 2026-07-20
**HEAD :** `31d4d6e4`

## Transport

Le transport WhatsApp et Telegram fonctionne actuellement.

- Green API : `authorized`
- Telegram Bot `@lawim_bot` : `ok: true`
- Webhooks configurés et endpoints opérationnels
- Footer IA non-bloquant (try/except protège la réponse principale)
- Parse_mode HTML Telegram avec fallback texte brut

## État conversationnel

Le comportement conversationnel reste non conforme.

### Défauts observés

- Perte de contexte entre les tours de conversation
- Réponse au dernier message sans tenir compte de l'historique complet
- Redirection vers des services immobiliers externes (Jumia House, SeLoger, groupes Facebook)
- `ProgressiveWizard` non maître du dialogue
- LLM trop libre dans la formulation des réponses
- Identité conversationnelle encore à vérifier selon les surfaces
- Footer trop long dans la version actuellement testée

### Scénario de reproduction

```
Utilisateur :
Bonjour

Utilisateur :
Je cherche un appartement de deux chambres à Douala.

Utilisateur :
Mon budget est de 180 000 FCFA par mois.

Utilisateur :
Je préfère Bonamoussadi.
```

### État attendu

```yaml
intent: rental_search
property_type: apartment
bedrooms: 2
city: Douala
budget_xaf: 180000
district: Bonamoussadi
qualification_status: in_progress
```

### État constaté

La perte de contexte entre les tours empêche la construction de cet état.

## Infrastructure

- Hôte : `vps-6da158cc.vps.ovh.net` (164.132.44.192)
- Stockage : 72G (31G utilisé, 42G libre)
- Docker : `lawim-app`, `lawim-postgres`, `lawim-redis` — tous healthy
- Base de données : PostgreSQL, schéma v19
- Reverse proxy : Nginx

## Prochaine étape

La prochaine mission doit corriger la mémoire conversationnelle et remettre `ProgressiveWizard` au centre du dialogue.
