# LAWIM — État Actuel

**Dernière mise à jour :** 2026-07-20
**HEAD :** (branche `feature/conversation-state-engine-20260720`)

## Transport

Le transport WhatsApp et Telegram fonctionne actuellement.

- Green API : `authorized`
- Telegram Bot `@lawim_bot` : `ok: true`
- Webhooks configurés et endpoints opérationnels
- Footer IA non-bloquant (try/except protège la réponse principale)
- Footer réduit à ≤10 mots (FR/EN/PCM)
- Parse_mode HTML Telegram avec fallback texte brut

## Conversation Runtime

```
Conversation Runtime : CANONIQUE ET VALIDÉ LOCALEMENT
Provider IA : FORMULATION UNIQUEMENT
ResponsePlan : OBLIGATOIRE
ResponseValidator : ACTIF
Canaux : CONNECTÉS AU RUNTIME CANONIQUE
Déploiement OVH : NON EFFECTUÉ
Recette utilisateur : EN ATTENTE
```
