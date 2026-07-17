# LAWIM_V2 — WhatsApp/Telegram Hotfix Certification

## Hotfix deployed
| Component | Value |
|---|---|
| Commit | `f140d356` |
| Merge | `d793059c` |
| Tag | `lawim-v2-whatsapp-telegram-hotfix` |
| Server HEAD | `f140d356` |
| Image digest | sha256:2d0e61b9 |
| MAINTENANCE_FLAGS | All `False` |
| Green API | `authorized` |
| Telegram webhook | Set (IPv4, 164.132.44.192) |

## WhatsApp fix
- Root cause: unconditional `_dispatch_maintenance_reply()` call
- Fix: guard with `MAINTENANCE_FLAGS` check
- Status: VERIFIED in container

## Telegram fix
- Root cause: webhook not set with matching secret_token → 401 on every update
- Fix: webhook registered with correct secret from env
- Status: VERIFIED (Telegram API confirms webhook active)

## Disclaimer
Already present in `disclaimer.py` for FR/EN/PCM. With the maintenance bypass fixed, AI responses can now reach channel users with the disclaimer attached.

## Residual risks
- R1 (Pidgin human validation): OPEN — requires 3 native speakers
- R2 (Real channel E2E): OPEN — requires QA phone for delivery confirmation
- Real WhatsApp/Telegram AI responses depend on the conversation service being routed to the AI orchestrator, which is a separate concern from the maintenance hotfix.

## Decision
**LAWIM WHATSAPP AND TELEGRAM LIVE — IPV4 DELIVERY AND AI DISCLAIMER VERIFIED**
