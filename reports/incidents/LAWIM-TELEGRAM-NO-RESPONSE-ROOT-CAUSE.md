# LAWIM — Telegram No Response Root Cause

## Symptom
Telegram bot `@lawim_bot` did not respond to user messages.

## Root cause
The Telegram webhook URL was **not set** with the correct `secret_token`. The environment contained a valid `TELEGRAM_WEBHOOK_SECRET` (64-char hex) but the webhook was either never registered with Telegram's API or was registered with a mismatched token.

This caused the backend's `_handle_telegram_webhook()` to return **HTTP 401** (`"Valid Telegram webhook token required"`) for every incoming update.

## Evidence
- Docker logs showed repeated `POST /api/notifications/telegram/webhook → 401` entries
- `getWebhookInfo` for the bot returned no active webhook URL

## Fix
1. Set the Telegram webhook via the Bot API with the **correct** `secret_token` from the environment:
   ```bash
   curl -X POST "https://api.telegram.org/bot${TOKEN}/setWebhook" \
     -F "url=https://api.lawim.app/api/notifications/telegram/webhook" \
     -F "secret_token=${TELEGRAM_WEBHOOK_SECRET}" \
     -F "max_connections=10"
   ```
2. The webhook now returns `{"ok":true,"result":{"url":"https://api.lawim.app/api/notifications/telegram/webhook","ip_address":"164.132.44.192",...}}`
3. IPv4 is used (164.132.44.192 = OVH server IP)
4. Both IPv4 and IPv6 connectivity to api.telegram.org are functional (0.04s/0.05s)

## Verification
- Telegram API confirms webhook is set
- `pending_update_count: 0`
- No last error message
- Secret token validation passes (`compare_digest` match)
