# Idempotence Isolation Details — LCIP B.4R-F

## Isolation Per Scenario

- Each conversation: isolated SQLite database (tempfile)
- Each replay: same database, same adapter
- Idempotency keys are scoped per conversation_id
- Different conversations with same last message do NOT share idempotency state

## Cross-Conversation Test

```python
# Same message, different conversation_id -> not considered duplicate globally
# This is guaranteed by the idempotency_key format: pf:{conversation_id}:property_search
```

## Isolation Verification

| Property | Status |
|----------|--------|
| conversation_id distinct per scenario | PASS |
| idempotency_key distinct per conversation_id | PASS |
| SQLite repository isolated per scenario | PASS |
| No state leak between scenarios | PASS |
