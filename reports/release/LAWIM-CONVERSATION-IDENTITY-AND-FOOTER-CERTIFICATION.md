# LAWIM V2 — Conversation Identity & AI Footer Certification

## Release Information
| Field | Value |
|-------|-------|
| Commit | `31d4d6e4` |
| Tag | `lawim-v2-conversation-identity-footer-runtime-verified` |
| Date | 2026-07-20 |
| Branch | main |

## Changes

### Backend (`code/lawim_v2/communication/service.py`)
- `AI_FOOTER_TEXTS` — canonical trilingual footer (FR/EN/PCM)
- `_format_ai_footer(language, channel)` — non-blocking footer formatter
  - WhatsApp: `\n\n──────────────\n_{text}_`
  - Telegram: `\n\n──────────────\n<i>{text}</i>`
  - Other channels: `""` (empty, client renders)
- `_generate_ai_reply()` — footer append wrapped in try/except
- `_greeting_response()` — footer append wrapped in try/except

### Delivery (`code/lawim_v2/communication/delivery.py`)
- `send_telegram_message()` — `parse_mode=HTML` added
- HTML escaping via `html.escape()` with safe `<i>` tag restoration
- Fallback retry without `parse_mode` on entity parse error

### Frontend (`frontend/packages/ui/src/components/AIConversationFooter.tsx`)
- Component: `AIConversationFooter`
- Props: `generatedByAI`, `language`, `compact`, `className`
- Full/compact text variants
- `role="note"` for accessibility
- Style: 10px, italic, low contrast, non-selectable

### Conversation Model (`frontend/packages/conversation/src/index.ts`)
- `ConversationMessage` now includes: `generatedByAI`, `language`, `authorDisplayName`, `authorIcon`

### Web UI (`frontend/apps/web/src/lawim-cockpits.tsx`)
- `ConversationStudioPage` imports `AIConversationFooter`
- Shows `🤖 LAWIM AI` identity
- Footer displayed with user's active language

## AI Identity Rules
| Interlocutor | Display |
|-------------|---------|
| User (authenticated) | `👤 <name/ID>` |
| User (anonymous) | `👤 Vous` |
| LAWIM (all channels) | `🤖 LAWIM AI` |

## Test Results
| Suite | Status |
|-------|--------|
| Communication delivery | 8/8 PASS |
| Green API webhook | 3/3 PASS |
| Telegram webhook | 3/3 PASS |
| Frontend build | OK |

## Deployment
Git tag pushed to `origin/main`. Deploy to OVH via bundle transfer to `/opt/lawim`.
