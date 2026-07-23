# Interaction Gateway

**Date:** 2026-07-23
**Status:** COMPLETE
**File:** `lawim_runtime/interaction/gateway.py`

## Purpose

The Interaction Gateway is the first line of defense for incoming interactions. It validates envelopes, enforces structural requirements, and prepares data for downstream processing.

## Interface

```python
class InteractionGateway:
    def validate_envelope(envelope: InteractionEnvelope) -> GatewayValidationResult
    def prepare_envelope(channel, external_message_id, ...) -> InteractionEnvelope
```

## Validation Rules

| Rule | Condition | Error |
|------|-----------|-------|
| Channel required | `envelope.channel` is empty | "channel is required" |
| Content or attachment | No raw_content and no attachments | "raw_content or attachments required" |
| System/Command exemption | SYSTEM or COMMAND type without content | Allowed |

## Envelope Preparation

The `prepare_envelope` factory method creates an `InteractionEnvelope` with:
- Auto-generated `interaction_id` (UUID hex)
- `received_at` timestamp in ISO format
- Copy of `raw_content` to `normalized_content` (full normalization deferred to `MessageNormalizer`)
- Empty tuple for `attachments` if not provided

## Flow

```
Webhook Payload
  -> ChannelAdapter.parse_webhook()
  -> InteractionEnvelope
  -> InteractionGateway.validate_envelope()
  -> [if invalid: SAFE_FALLBACK response]
  -> InteractionDeduplicator.check()
  -> continue pipeline
```
