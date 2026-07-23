# Channel Adapters

**Date:** 2026-07-23
**Status:** COMPLETE
**Directory:** `lawim_runtime/interaction/adapters/`

## Purpose

Channel adapters convert protocol-specific webhook payloads into `InteractionEnvelope` and deliver prepared responses back. They contain zero business logic.

## Contract

```python
class InboundChannelAdapter(ABC):
    def parse_webhook(raw_payload, headers) -> InteractionEnvelope | None
    def extract_identifiers(raw_payload) -> dict[str, str]

class OutboundChannelAdapter(ABC):
    def send(request: ChannelDeliveryRequest) -> ChannelDeliveryResult
    def validate_webhook(headers, raw_body) -> bool
```

## Implemented Adapters

### WhatsApp (`whatsapp.py`)

| Aspect | Detail |
|--------|--------|
| Inbound | Green API webhook format |
| Identity | `senderData.sender` / `senderData.chatId` |
| Message types | TEXT, IMAGE, AUDIO, VIDEO, DOCUMENT, LOCATION |
| Outbound | Simulated or Green API real |
| Fallback | Hash-based ID when no external_message_id |

### Telegram (`telegram.py`)

| Aspect | Detail |
|--------|--------|
| Inbound | Telegram Bot API webhook |
| Identity | `message.from.id` / `message.chat.id` |
| Message types | TEXT, IMAGE, AUDIO, VIDEO, DOCUMENT, LOCATION, BUTTON |
| Callback | Button presses via `callback_query` |
| Outbound | Simulated or Telegram Bot API real |

### Web/API (`web_api.py`)

| Aspect | Detail |
|--------|--------|
| Inbound | JSON with `message`/`text`, `user_id`/`userId` |
| Authentication | Token-based via headers |
| Correlation | Supports `correlation_id`/`correlationId` |
| Outbound | Structured JSON response |

## Restrictions

- Adapters never call ProjectBrain, DecisionEngine, or any LLM
- Adapters never modify ProjectProfile
- Adapters never decide the response content
- Adapters never bypass InteractionOrchestrator

## Deployment

All adapters are feature-flagged and disabled by default:
- `lros_whatsapp_adapter_enabled: false`
- `lros_telegram_adapter_enabled: false`
- `lros_web_interaction_enabled: false`
- `lros_api_interaction_enabled: false`
