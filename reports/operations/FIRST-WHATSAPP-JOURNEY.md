# LAWIM — Premier Parcours Immobilier WhatsApp

**Date:** 2026-07-23
**Status:** FIRST_WHATSAPP_JOURNEY_IN_PROGRESS

---

## Infrastructure validée

| Composant | Statut | Preuve |
|-----------|--------|--------|
| Green API instance | authorized | `getStateInstance()` → authorized |
| Envoi message | ✅ SUCCESS | ID `3EB0A8F21BF215210986C7` |
| Webhook endpoint | ✅ accessible | `POST /api/notifications/whatsapp/webhook` |
| Conversation engine | ✅ actif | AI_ORCHESTRATOR_ENABLED=true |
| DeepSeek IA | ✅ SUCCESS | deepseek-v4-flash → `Yaoundé` |
| OpenAI IA | ✅ SUCCESS | gpt-4o-mini → `Yaoundé` |
| Domaine + HTTPS | ✅ lawim.app | Let's Encrypt TLS, HTTP 200 |

## Corrections appliquées (commit 6379981c)

| Correction | Fichier | Cause |
|-----------|---------|-------|
| Message d'accueil | `greetings.py`, `engine.py` | Ancien message générique remplacé par nouvelle formulation invitant à décrire le projet |
| `APARTMENT` / `ROOM` dans réponses | `engine.py` | Ajout de `_PROPERTY_TYPE_LABELS` et `_TRANSACTION_TYPE_LABELS` pour traduction FR |
| "Très bien" supprimé | `engine.py:_build_acknowledgement_text` | Remplacé par "Je récapitule" / "Let me summarize" |
| property_type=ROOM erroné | `property_types.py` | Regex bloquant "X chambres" (numérique) → ROOM |
| Budget "200 000 F" non reconnu | `money.py` | Ajout pattern `[fF](?:\s|$|\.|,|;|par...)` |
| Budget "250k" → 250 au lieu de 250000 | `money.py` | Correction `num < 100` → `num < 1000` |
| "deux cent mille" → 100000 | `money.py` | Ajout des multi-mots à `AMOUNT_WORDS` |
| "Yaoundé" (accent) non reconnu | `geography.py` | Ajout `"yaoundé": "Yaoundé"` à `KNOWN_CITIES` |
| "Je veux visiter" sans bien | `planner.py` | Vérification `selected_property_id` avant transition VISIT |

## Tests ajoutés

| Fichier | Tests |
|---------|-------|
| `tests/test_conversation_journey.py` | 13 tests couvrant les 8 corrections ci-dessus |

## Blocage principal

Le pipeline conversationnel complet nécessite un message **entrant réel** depuis l'application WhatsApp. Les messages envoyés via l'API Green API sont classés `outgoingAPIMessageReceived` et ne déclenchent pas `_generate_ai_reply`.

**Action :** envoyer un message WhatsApp réel au `+237686822667` depuis l'application WhatsApp d'un vrai téléphone.

## Identifiants

| Élément | Valeur |
|---------|--------|
| Instance Green API | 7107644927 |
| Numéro LAWIM | +237686822667 |
| Domaine | lawim.app |
| HEAD déployé | 6379981c |
| Tests LROS | 721 PASS |
| Tests V2 journey | 13 PASS |
