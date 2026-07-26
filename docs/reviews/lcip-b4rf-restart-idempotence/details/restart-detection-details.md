# Restart Detection Details — LCIP B.4R-F

## Event Detection

B000083 contains SERVICE_RESTART at messages[5] (system role).

## Detection Logic

```python
if msg.get("role") == "system" and "RESTART" in msg.get("text", "").upper():
    # Capture state before restart
    state_before = adapter.load_state(conversation_id)
    # Recreate adapter (new runtime instance, same DB)
    adapter = ProgramFEngineAdapter(db_path=db_path, ...)
    # Continue with next user turn
```

## Proof

The runtime instance is recreated (new ProgramFEngineAdapter + new ConversationJourneyOrchestrator).
The same SQLite database is used, so state persists.
