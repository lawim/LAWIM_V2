# Telegram L6 Validation Report

**Programme:** G.6
**Service:** Telegram Bot API
**Status:** NOT VALIDATED
**Date:** 2026-07-23

---

## Prérequis non satisfaits

Ce test nécessite :

- `TELEGRAM_BOT_TOKEN` — non configuré
- Bot Telegram actif créé via BotFather
- Webhook HTTPS configuré pointant vers LAWIM
- Compte Telegram réel pour envoyer/recevoir

## Procédure de validation

Une fois les credentials disponibles, exécuter :

```bash
# 1. Vérifier le bot
curl -X GET "https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"

# 2. Configurer le webhook
curl -X POST "https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url=https://{DOMAIN}/telegram/webhook&secret_token={SECRET}"

# 3. Envoyer un message Telegram via l'adaptateur
python3 -c "
from lawim_runtime.interaction.adapters.telegram_bot_api import send_telegram_message
from lawim_runtime.interaction.adapters import ChannelDeliveryRequest
req = ChannelDeliveryRequest(
    channel='telegram',
    recipient_id='{CHAT_ID}',
    text='🤖 LAWIM AI — Test de validation Telegram L6',
    correlation_id='g6-telegram-validation',
)
result = send_telegram_message(req)
print(f'Success: {result.success}, ProviderID: {result.provider_message_id}')
"

# 4. Envoyer un message depuis Telegram vers le bot
# 5. Vérifier les logs LAWIM pour le correlation_id
```

## Scénarios à valider

| # | Scénario | Statut | Preuve |
|---|----------|--------|--------|
| 1 | Webhook configuré et réception | NON VALIDÉ | Requiert token + domaine |
| 2 | Message sortant (sendMessage) | NON VALIDÉ | Requiert chat_id réel |
| 3 | Retry après échec temporaire | NON VALIDÉ | Requiert test réel |
| 4 | Conversation continue (5+ échanges) | NON VALIDÉ | Requiert utilisateur réel |
| 5 | Session conservée entre messages | NON VALIDÉ | Requiert test réel |
| 6 | correlation_id conservé E2E | NON VALIDÉ | Requiert test réel |

## Conclusion

**Telegram L6 : NON VALIDÉ.** L'adaptateur est implémenté (L3) mais aucun test réel n'a été exécuté. La validation nécessite un token Bot Telegram, un domaine HTTPS, et un compte Telegram réel.
