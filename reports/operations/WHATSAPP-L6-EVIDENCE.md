# WhatsApp L6 Validation Report

**Programme:** G.6
**Service:** WhatsApp Green API
**Status:** NOT VALIDATED
**Date:** 2026-07-23

---

## Prérequis non satisfaits

Ce test nécessite :

- `GREEN_API_INSTANCE` — non configuré
- `GREEN_API_TOKEN` — non configuré
- Numéro de téléphone réel pour envoyer et recevoir des messages
- Compte Green API actif avec webhook configuré

## Procédure de validation

Une fois les credentials disponibles, exécuter :

```bash
# 1. Vérifier que l'instance Green API est active
curl -X GET "https://api.green-api.com/waInstance{GREEN_API_INSTANCE}/getStateInstance/{GREEN_API_TOKEN}"

# 2. Envoyer un message WhatsApp réel via l'adaptateur
python3 -c "
from lawim_runtime.interaction.adapters.whatsapp_green_api import send_green_api_message
from lawim_runtime.interaction.adapters import ChannelDeliveryRequest
req = ChannelDeliveryRequest(
    channel='whatsapp',
    recipient_id='+237XXXXXXXXX',
    text='🤖 LAWIM AI — Test de validation WhatsApp L6',
    correlation_id='g6-whatsapp-validation',
)
result = send_green_api_message(req)
print(f'Success: {result.success}, ProviderID: {result.provider_message_id}')
"

# 3. Vérifier la réception sur le téléphone cible
# 4. Envoyer un message depuis le téléphone vers le webhook Green API
# 5. Vérifier les logs LAWIM pour le correlation_id
# 6. Vérifier la réponse automatique
```

## Scénarios à valider

| # | Scénario | Statut | Preuve |
|---|----------|--------|--------|
| 1 | Message entrant reçu via webhook | NON VALIDÉ | Requiert test réel |
| 2 | Message sortant envoyé | NON VALIDÉ | Requiert test réel |
| 3 | Conversation continue (5+ échanges) | NON VALIDÉ | Requiert test réel |
| 4 | Reprise après interruption réseau | NON VALIDÉ | Requiert test réel |
| 5 | Pièce jointe reçue | NON VALIDÉ | Requiert média réel |
| 6 | Plusieurs utilisateurs simultanés | NON VALIDÉ | Requiert test réel |
| 7 | correlation_id conservé E2E | NON VALIDÉ | Requiert test réel |

## Logs attendus

```
[Date] green_api webhook received: external_message_id=..., chatId=...
[Date] envelope created: interaction_id=..., correlation_id=...
[Date] delivery sent: provider_message_id=..., status=SENT
```

## Conclusion

**WhatsApp L6 : NON VALIDÉ.** L'adaptateur est implémenté (L3) mais aucun test réel n'a été exécuté. La validation nécessite des credentials Green API actifs et un numéro de téléphone réel.
