# Integrations

This document captures the official connector catalog for LAWIM 1.x, focusing on configuration, validation, health, logs, retries, and documentation.

## Green API WhatsApp

- Public webhook URL: `https://api.lawim.app/api/notifications/whatsapp/webhook`
- Auth header: `Authorization: Bearer <GREEN_API_WEBHOOK_SECRET>`
- Instance settings: `GREEN_API_API_URL`, `GREEN_API_MEDIA_URL`, `GREEN_API_ID_INSTANCE`, `GREEN_API_TOKEN_INSTANCE`, `GREEN_API_WEBHOOK_URL`, `GREEN_API_WEBHOOK_SECRET`, `GREEN_API_PHONE`
- Incoming notifications handled: `incomingMessageReceived`, `outgoingAPIMessageReceived`, `outgoingMessageStatus`, `stateInstanceChanged`
- Persistence targets: `communication_messages`, `communication_events`, `communication_logs`
- Idempotence key: derived from `typeWebhook` plus `idMessage`, `status`, `stateInstance`, or payload hash when Green API does not provide a stable identifier

## Telegram Bot

- Public bot URL: `https://t.me/lawim_bot`
- Public webhook URL: `https://api.lawim.app/api/notifications/telegram/webhook`
- Auth header: `X-Telegram-Bot-Api-Secret-Token: <TELEGRAM_WEBHOOK_SECRET>`
- Instance settings: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_URL`, `TELEGRAM_WEBHOOK_SECRET`
- Secret handling: LAWIM derives a stable webhook secret from `TELEGRAM_BOT_TOKEN` when `TELEGRAM_WEBHOOK_SECRET` is omitted
- Update types handled: `message`, `edited_message`, `callback_query`, `my_chat_member`, `chat_member`
- Persistence targets: `communication_messages`, `telegram_updates`, `communication_events`, `communication_logs`
- Idempotence key: Telegram `update_id`, with a payload hash fallback only when `update_id` is absent

## AI Orchestrator

- Orchestrator flag: `AI_ORCHESTRATOR_ENABLED=true`
- Primary chain: `AI_PRIMARY_PROVIDER=deepseek`, `AI_COMPLEX_PROVIDER=openai`
- Fallback chain: `AI_FALLBACK_CHAIN=deepseek,openai,gemini_primary,gemini_secondary,internal`
- Provider credentials: `DEEPSEEK_API_KEY`, `OPENAI_API_KEY`, `GEMINI_PRIMARY_API_KEY`, `GEMINI_SECONDARY_API_KEY`
- Provider models: `DEEPSEEK_MODEL`, `OPENAI_MODEL`, `GEMINI_PRIMARY_MODEL`, `GEMINI_SECONDARY_MODEL`
- Safety controls: timeouts, circuit breakers, response validation, fallback, and learning approval are all configured through environment variables and persisted catalog tables
- Telegram transport: outbound API calls should prefer IPv4 when the deployment path requires it
