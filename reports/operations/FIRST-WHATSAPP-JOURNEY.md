# LAWIM — Premier Parcours Immobilier WhatsApp

**Date:** 2026-07-23
**Status:** FIRST_WHATSAPP_JOURNEY_IN_PROGRESS

---

## Infrastructure validée

| Composant | Statut | Preuve |
|-----------|--------|--------|
| Green API instance | authorized | `getStateInstance()` → authorized |
| Envoi message API | ✅ SUCCESS | ID `3EB0A8F21BF215210986C7` |
| Webhook endpoint | ✅ accessible | `POST /api/notifications/whatsapp/webhook` |
| Auth webhook | ✅ validé | 401 sans secret, 200 avec secret valide |
| Conversation engine | ✅ configuré | AI_ORCHESTRATOR_ENABLED=true, DeepSeek+OpenAI actifs |
| Base de données | ✅ PostgreSQL | connectée, tables V2 présentes |
| Domaine + HTTPS | ✅ lawim.app | Let's Encrypt TLS, HTTP 200 |

## Blocage identifié

Le parcours complet nécessite un message **entrant réel** depuis l'application WhatsApp.

Les messages envoyés via l'API Green API sont classés `outgoingAPIMessageReceived` et ne déclenchent pas le pipeline conversationnel (`_generate_ai_reply`). Pour déclencher le pipeline, Green API doit envoyer un webhook de type `incomingMessageReceived`, ce qui ne se produit que lorsqu'un **véritable utilisateur WhatsApp** envoie un message au numéro LAWIM.

**Action requise :** envoyer un message WhatsApp réel au `+237686822667` depuis l'application WhatsApp d'un vrai téléphone.

## Tests exécutés

| Étape | Statut | Détail |
|-------|--------|--------|
| Envoi message test | ✅ | 10+ messages envoyés via API, tous reçus (HTTP 200) |
| Webhook reachable | ✅ | HTTPS, authentifié, répond |
| Pipeline conversationnel | 🔲 Déclenché uniquement sur message réel | Engine OK, providers IA OK |
| Réponse générée | 🔲 Bloqué | Dépend du déclencheur entrant |
| Réponse livrée sur WhatsApp | 🔲 Bloqué | Dépend du déclencheur entrant |
| Demande de visite créée | 🔲 Bloqué | Dépend du déclencheur entrant |

## Identifiants de bout en bout

| Élément | Valeur |
|---------|--------|
| Instance Green API | 7107644927 (authorized) |
| Numéro LAWIM | +237686822667 |
| Domaine | lawim.app (Let's Encrypt) |
| Endpoint webhook | `POST /api/notifications/whatsapp/webhook` |
| Provider IA | DeepSeek (deepseek-v4-flash) + OpenAI (gpt-4o-mini) |

## Prochaine action

Envoyer un message WhatsApp réel au `+237686822667` depuis l'application WhatsApp.
