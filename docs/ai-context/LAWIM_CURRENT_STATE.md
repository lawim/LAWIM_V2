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

## État conversationnel

ConversationStateEngine localement validé.
ProgressiveWizard connecté au runtime.
Déploiement OVH encore requis.
Validation utilisateur réelle encore requise.

### Composants construits

- `ConversationState` — état conversationnel avec slots connus, intention, métadonnées
- `ConversationStateRepository` — persistance SQLite de l'état
- `ConversationResolver` — résolution de session par canal (WhatsApp/Telegram/Web)
- `ConversationStateEngine.process_turn()` — point d'entrée canonique
- `ProgressiveWizard` avec persistance DB optionnelle
- Handover détecté via mots-clés (`parler à une personne`, etc.)
- Footer ≤10 mots dans toutes les langues

### Tests de baseline : 57 PASS, 0 XFAIL

Les sept défauts de baseline sont corrigés localement.
Conversation State Engine : VALIDÉ LOCALEMENT
ProgressiveWizard : CONNECTÉ AU RUNTIME
AIOrchestrator : CONTRAINT PAR RESPONSEPLAN
Déploiement OVH : NON EFFECTUÉ
Recette utilisateur réelle : EN ATTENTE

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

## Infrastructure

- Hôte : `vps-6da158cc.vps.ovh.net` (164.132.44.192)
- Stockage : 72G (31G utilisé, 42G libre)
- Docker : `lawim-app`, `lawim-postgres`, `lawim-redis` — tous healthy
- Base de données : PostgreSQL, schéma v19
- Reverse proxy : Nginx

## Prochaine étape

Déployer le Conversation State Engine sur OVH et exécuter
la recette réelle complète sur Web, WhatsApp et Telegram.
