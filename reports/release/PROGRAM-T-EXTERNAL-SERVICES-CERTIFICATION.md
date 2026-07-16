# PROGRAM T — External Services Certification

## WhatsApp Green API

| Check | Status |
|-------|--------|
| Instance configured | ✅ In .env.example |
| Credentials | ✅ Environment variables |
| Webhook endpoint | ✅ /api/notifications/whatsapp/webhook |
| Webhook validation | ✅ validate_webhook_authorization |
| Deduplication | ✅ Conversation registry |
| Chat ID handling | ✅ |
| Message format | ✅ JSON |
| Error handling | ✅ Retry with backoff |
| Logging | ✅ Structured logging |
| Green API phone | ✅ +237686822667 |

## Telegram

| Check | Status |
|-------|--------|
| Bot token | ✅ Environment variable |
| Webhook endpoint | ✅ /api/notifications/telegram/webhook |
| Webhook validation | ✅ validate_webhook_authorization |
| Chat ID handling | ✅ chat_id_raw preserved |
| Message handling | ✅ |
| Error handling | ✅ Retry mechanism |
| Deduplication | ✅ |

## Facebook

| Check | Status |
|-------|--------|
| Channel configured | ✅ Tracking codes (FB-LAWIM-*) |
| Attribution | ✅ Program J tracking |
| Publications | ✅ Campaign model |
| Messenger | ❌ NOT IN LAUNCH SCOPE |
| Will NOT block Go-Live | ✅ Explicitly documented |

## Email (SMTP)

| Check | Status |
|-------|--------|
| SMTP configured | ✅ In .env config |
| Templates | ✅ notification_domain |
| SPF/DKIM/DMARC | ⚠️ Requires domain verification |
| Error handling | ✅ Retry mechanism |
| From address | noreply@lawim.app |

## SMS

| Check | Status |
|-------|--------|
| Provider | ⚠️ NOT IN LAUNCH SCOPE |
| Will NOT block Go-Live | ✅ Explicitly documented |

## Campay

### Sandbox (DEV)

| Check | Status |
|-------|--------|
| Sandbox URL | ✅ demo.campay.net |
| Credentials | ✅ Environment variables |
| Payment initiation | ✅ Tested |
| Callback handling | ✅ /api/v2/financial/providers/campay/webhook |
| Idempotency | ✅ |
| Error handling | ✅ Timeout and retry |

### Production

| Check | Status |
|-------|--------|
| PROD mode | ⚠️ DISABLED (campay_prod_mode=false) |
| Will NOT block Go-Live | ✅ Sandbox certified; production activation post-launch |

## LLM Providers

| Provider | Enabled | API Key Required | Tested |
|----------|---------|-----------------|--------|
| DeepSeek | ✅ (prod) | ✅ DEEPSEEK_API_KEY | ✅ |
| OpenAI | ✅ (prod) | ✅ OPENAI_API_KEY | ✅ |
| Gemini Primary | ✅ (prod) | ✅ GEMINI_PRIMARY_API_KEY | ✅ |
| Gemini Secondary | ✅ (prod) | ✅ GEMINI_SECONDARY_API_KEY | ✅ |
| Circuit breaker | ✅ Enabled | - | ✅ |
| Fallback chain | ✅ deepseek→openai→gemini_primary→gemini_secondary | - | ✅ |

## Verdict

```
EXTERNAL SERVICES: ✅ CERTIFIED
WhatsApp: ✅
Telegram: ✅
Campay (sandbox): ✅
Facebook: OUT OF SCOPE (non-blocking)
SMS: OUT OF SCOPE (non-blocking)
```
