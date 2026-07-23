# LAWIM Multichannel Continuity

**Date:** 2026-07-23
**Certification:** Program E.5

## Identity Continuity

- `IdentityResolver` links multiple channel identities to a single LAWIM user
- WhatsApp phone number, Telegram chat ID, Web user ID can all map to the same actor
- No automatic merging of unverified identities
- Unconfirmed cross-channel identity returns ANONYMOUS

## Session Continuity

- Sessions are user-scoped, not channel-scoped
- A user can be active on multiple channels simultaneously with separate sessions
- Session timeout (30 min) is configurable
- Expired sessions create new sessions; projects persist

## Project Continuity

- Projects are user-scoped and survive sessions and channels
- `ProjectResolver` finds the active project for the user regardless of channel
- Same profile is enriched from any channel
- Ambiguity (multiple active projects) is detected, never auto-merged

## Tested Scenarios

| Scenario | Channels | Result |
|----------|----------|--------|
| Same user, WhatsApp + Telegram | whatsapp, telegram | PASS |
| Unconfirmed cross-channel | whatsapp + telegram (different user) | PASS (ANONYMOUS) |
| Session expiry and resume | whatsapp | PASS |
| Project survives channels | whatsapp -> telegram | PASS |
