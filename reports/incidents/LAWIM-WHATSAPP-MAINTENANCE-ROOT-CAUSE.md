# LAWIM — WhatsApp Maintenance Response Root Cause

## Symptom
Every inbound WhatsApp message received "LAWIM est momentanément indisponible." — the MAINTENANCE_RESPONSE text.

## Root cause
`communication/service.py` unconditionally called `_dispatch_maintenance_reply()` for every incoming WhatsApp and Telegram message, regardless of whether maintenance mode was active.

The code at line 807 (WhatsApp) and line 933 (Telegram) bypassed any check of `MAINTENANCE_FLAGS["lawim_core_rebuild_maintenance_mode"]`.

## Fix
Added a guard condition before dispatching the maintenance reply:
```python
if MAINTENANCE_FLAGS.get("lawim_core_rebuild_maintenance_mode", False):
    maintenance_reply = self._dispatch_maintenance_reply(...)
```

When maintenance is `False` (production mode), the message is logged and **no** MAINTENANCE_RESPONSE is sent back.

## Commit
`f140d356` — merged into `main` at `d793059c`

## Verification
- MAINTENANCE_FLAGS in container: all `False`
- Code inspection confirms guard present in both webhook handlers
- No MAINTENANCE_RESPONSE is returned when maintenance is inactive
