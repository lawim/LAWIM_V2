# Incident Root Cause Analysis — AI Footer Channel Regression

## Incident ID
LAWIM-FOOTER-REGRESSION-20260718

## Impact
- WhatsApp: **P0 — Complete silence**
- Telegram: **P0 — Complete silence**
- Web: **Footer not wired in renderer**

## Timeline
| Date | Event |
|------|-------|
| 2026-07-18 01:14 | `6f648c95` — AI footer feature committed |
| 2026-07-18 01:15 | `c65d033a` — Merged to main |
| 2026-07-18 | Deployed to OVH |
| 2026-07-18 | WhatsApp/Telegram stop responding |
| 2026-07-20 | Incident response initiated |

## Root Cause

1. **Non-blocking footer**: The `_format_ai_footer()` method was called directly without try/except. Any exception in footer formatting would silently propagate and prevent the AI reply from being returned, resulting in empty message delivery.

2. **Telegram `parse_mode` missing**: `send_telegram_message()` did not set `parse_mode=HTML`. Messages containing `<i>` HTML tags would be sent as plain text showing raw tags. If the Telegram API rejected the message due to entity parsing errors (e.g., unmatched tags), the message would fail delivery.

3. **No HTML escaping**: The message body sent to Telegram with `parse_mode=HTML` could contain characters that break HTML entity parsing (`<`, `>`, `&`), causing "can't parse entities" errors.

4. **Web footer not wired**: `AIConversationFooter` component was created and exported but never imported in any conversation renderer.

## Resolution

All 4 root causes addressed in commit `31d4d6e4`:
- `_format_ai_footer` wrapped in try/except → returns `""` on any error
- `send_telegram_message` sets `parse_mode=HTML` with HTML escaping
- Fallback retry without `parse_mode` on entity parse error
- `AIConversationFooter` wired in `ConversationStudioPage`

## Verification
- All 14 communication/webhook tests PASS
- Frontend build OK
- Tag `lawim-v2-conversation-identity-footer-runtime-verified` created
