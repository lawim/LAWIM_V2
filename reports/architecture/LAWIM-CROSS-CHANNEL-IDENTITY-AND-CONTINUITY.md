# LAWIM Cross-Channel Identity and Continuity

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 3 — Conversation Memory

## 1. IdentityConfidence Levels

| Level | Value | Description | Auto-Merge |
|-------|-------|-------------|------------|
| 5 | `VERIFIED` | Verified via phone, email, or authenticated account | Yes |
| 4 | `HIGH_CONFIDENCE` | Matched by user_id or strong heuristics | Yes |
| 3 | `PROBABLE` | Probabilistic match (behavioural, IP) | No |
| 2 | `UNVERIFIED` | No verification performed | No |
| 1 | `CONFLICT` | Conflicting identity information detected | No |

## 2. IdentityBinding Model

| Field | Type | Description |
|-------|------|-------------|
| `binding_id` | `str` | UUID primary key |
| `actor_id` | `str` | Unified actor identifier |
| `channel` | `str` | Channel (e.g. `whatsapp`, `telegram`, `web`) |
| `channel_identifier` | `str` | Channel-specific user ID |
| `source` | `IdentitySource` | How this binding was established |
| `confidence` | `IdentityConfidence` | Current confidence level |
| `created_at` | `str` | ISO 8601 creation timestamp |
| `verified_at` | `str\|None` | ISO 8601 verification timestamp |

### IdentitySource Enum

- `UNVERIFIED` — No verification source
- `USER_ID` — Matched by internal user ID
- `PHONE_VERIFIED` — Verified via phone confirmation
- `EMAIL_VERIFIED` — Verified via email confirmation
- `WHATSAPP_CHAT_ID` — WhatsApp chat identifier
- `TELEGRAM_USER_ID` — Telegram user identifier
- `WEB_SESSION` — Web session identifier
- `AUTHENTICATED_ACCOUNT` — Authenticated account login

## 3. CrossChannelConsent

| Field | Type | Description |
|-------|------|-------------|
| `consent_id` | `str` | UUID primary key |
| `consent_type` | `str` | Always `cross_channel_continuity` |
| `actor_id` | `str` | Actor granting consent |
| `source_channel` | `str` | Original channel |
| `target_channel` | `str` | Target channel for continuity |
| `status` | `str` | `PENDING` / `GRANTED` / `REVOKED` |
| `granted_at` | `str\|None` | ISO 8601 grant timestamp |
| `expires_at` | `str\|None` | ISO 8601 expiry timestamp |
| `revoked_at` | `str\|None` | ISO 8601 revocation timestamp |
| `evidence` | `str` | Evidence of consent (message ID) |
| `created_at` | `str` | ISO 8601 creation timestamp |

### Consent Lifecycle

```
PENDING
  │
  ├── grant_consent() → GRANTED
  │     │
  │     ├── (auto-expire) → EXPIRED
  │     └── revoke_consent() → REVOKED
  │
  └── revoke_consent() → REVOKED
```

- Default expiry: none (permanent until revoked)
- `CrossChannelConsent.is_active()` returns `True` only if `status == "GRANTED"` and `expires_at` (if set) is in the future

## 4. Resolution Logic

`CrossChannelIdentityResolver.resolve()`:

1. Look up `IdentityBinding` by `(channel, channel_identifier)`
2. If no binding → return `UNVERIFIED` identity
3. If binding exists → return `ResolvedIdentity` with actor_id and confidence
4. If `VERIFIED` → collect all channels bound to the same actor, detect conflicts

`resolve_with_consent()`:

1. Resolve identity
2. If confidence allows auto-merge (`VERIFIED` or `HIGH_CONFIDENCE`)
3. Look up active consent for `source_channel → target_channel`
4. Return `(identity, has_consent)`

### Auto-Merge Rules

- `VERIFIED` identities from the same actor automatically merge
- `HIGH_CONFIDENCE` identities merge with user confirmation
- `PROBABLE` and below require explicit user verification
- `CONFLICT` requires human intervention

## 5. Cross-Channel Continuity Scenarios

### WhatsApp → Telegram (W→T)

1. User identified on WhatsApp via phone
2. User messages LAWIM on Telegram
3. `CrossChannelIdentityResolver` links both to same actor via consent
4. User can resume conversation on Telegram with full context

### Telegram → WhatsApp (T→W)

1. User identified on Telegram via user_id
2. User messages LAWIM on WhatsApp
3. If phone matches existing binding → auto-merge (VERIFIED)
4. Resume case on WhatsApp

### WhatsApp → WhatsApp (W→W)

1. Same channel, different device or session
2. `IdentityBinding` by chat_id maps to same actor
3. Full continuity without additional consent

## 6. Privacy & Consent

- Cross-channel continuity requires explicit user consent
- Consent can be revoked at any time
- Revoked consent breaks continuity but does not delete existing data
- All consent events are audited
- Consent expiration auto-deactivates continuity
