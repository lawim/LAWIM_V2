# Delivery Manager

**Date:** 2026-07-23
**Status:** COMPLETE
**File:** `lawim_runtime/interaction/delivery.py`

## Purpose

Reliable message delivery with idempotency, retry, and audit.

## Delivery Statuses

| Status | Meaning |
|--------|---------|
| CREATED | Delivery request created |
| QUEUED | Queued for sending |
| SENDING | Currently being sent |
| SENT | Sent to provider |
| DELIVERED | Delivered to recipient |
| READ | Read by recipient |
| FAILED | Delivery failed |
| RETRYING | Retry in progress |
| CANCELLED | Cancelled (e.g., empty plan) |
| UNKNOWN | Unknown status |

## Delivery Manager

- Max retries: 3 (configurable)
- Idempotency: same delivery_id never sent twice
- No double delivery: duplicate detection before send
- Provider_message_id captured for reconciliation
- Correlation preserved across delivery attempts

## Delivery Attempt

Each delivery records:
- `attempt_id` (unique)
- `attempt_number`
- `status` at each stage
- `provider_message_id` from channel
- `error` details if failed
- `attempted_at` timestamp

## Integration

```
InteractionResponsePlan
  -> DeliveryManager.deliver()
  -> ChannelAdapter.send()
  -> ChannelDeliveryResult
  -> DeliveryResult
  -> DeliveryRepository.save()
```

## Safety

- Empty response plans (NO_RESPONSE) are cancelled immediately
- Failed deliveries trigger audit and metrics (delivery_failed_total)
- Unknown provider status is preserved, never assumed
