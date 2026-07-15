# Program J Foundation — Identity • Unified Conversation • Exchange Taxonomy

**Document ID:** LAWIM-PROGRAM-J-FOUNDATION-V1
**Status:** CANONICAL
**Date:** 2026-07-15

---

## 1. Scope

Program J Foundation delivers J1 (Identity & Actor Registry), J2 (Unified Conversation), and J5 (Exchange Taxonomy) as a single bundle.

### Exclusions (future J steps)

- Publication and campaign tracking
- Marketing tracking codes
- Attribution (first-touch, last-touch, multi-touch)
- Aggregated statistics
- Dashboards
- Learning Machine
- Feature Management Center
- AI agents

---

## 2. Actor Registry

### 2.1 Actor Types

| Type | Code | Description |
|------|------|-------------|
| AI_ASSISTANT | AI | LAWIM AI assistant |
| LAWIM_STAFF | STAFF | LAWIM team member |
| USER | USER | Unregistered user |
| OWNER | OWNER | Property owner |
| BUYER | BUYER | Property buyer |
| TENANT | TENANT | Tenant |
| REAL_ESTATE_AGENT | AGENT | Real estate agent |
| AGENCY | AGENCY | Real estate agency |
| ARCHITECT | ARCHITECT | Architect |
| ENGINEER | ENGINEER | Engineer |
| TECHNICIAN | TECH | Technician |
| NOTARY | NOTARY | Notary |
| INVESTOR | INVESTOR | Investor |
| PARTNER | PARTNER | Partner |
| SYSTEM | SYSTEM | System |

### 2.2 Visual Role Registry

Central registry with emoji, display format, color, privacy level, and masking rules.

```text
🤖 LAWIM AI:
🧑‍💼 LAWIM (Nom):
👤 Utilisateur
🏠 Agent immobilier (Nom):
🏢 Agence (Nom):
📐 Architecte (Nom):
🧑‍🔧 Ingénieur (Nom):
⚖️ Notaire (Nom):
💰 Investisseur (Nom):
🔧 Technicien (Nom):
🤝 Partenaire (Nom):
🏡 Propriétaire (Nom):
🏡 Acheteur (Nom):
🏢 Locataire (Nom):
```

### 2.3 Identity Resolution

Order: verified provider identifier → verified endpoint → LAWIM user → business dossier → conversation → memory.

Never auto-attach identity from:
- display name alone
- unverified username
- unverified phone number
- unconfirmed email
- textual resemblance

---

## 3. Exchange Taxonomy

### 3.1 Direction

| Value | Description |
|-------|-------------|
| INBOUND | From user to system |
| OUTBOUND | From system to user |
| INTERNAL | System-internal |
| SYSTEM | Automated system event |

### 3.2 Content Type

| Value | Description |
|-------|-------------|
| TEXT | Plain text |
| IMAGE | Image file |
| AUDIO | Audio file |
| VIDEO | Video file |
| DOCUMENT | Document file |
| LOCATION | Geographic location |
| CONTACT | Contact card |
| PROPERTY | Property reference |
| PAYMENT | Payment event |
| SYSTEM_EVENT | System event |

### 3.3 Exchange Type

| Value | Description |
|-------|-------------|
| INFORMATION_REQUEST | General information |
| PROPERTY_SEARCH | Property search |
| PROPERTY_OFFER | Property offer |
| QUALIFICATION | Qualification |
| MATCHING | Matching |
| VISIT_REQUEST | Visit request |
| NEGOTIATION | Negotiation |
| DOCUMENT_REQUEST | Document request |
| PAYMENT | Payment |
| COMPLAINT | Complaint |
| SUPPORT | Support |
| RELATIONSHIP_FOLLOW_UP | Follow-up |
| HUMAN_HANDOVER | Human handover |

### 3.4 Exchange Result

| Value | Description |
|-------|-------------|
| RECEIVED | Received |
| UNDERSTOOD | Understood |
| ANSWERED | Answered |
| ACTION_TRIGGERED | Action triggered |
| ESCALATED | Escalated |
| FAILED | Failed |
| IGNORED | Ignored |
| DUPLICATE | Duplicate |

---

## 4. Unified Conversation Model

### 4.1 Conversation

A conversation remains unique even when a user changes channel.

### 4.2 Channel Sessions

Each channel keeps its own session within a shared conversation.

### 4.3 Message Provenance

Every message preserves:
- source channel
- provider
- external identifiers
- direction
- content type
- exchange type
- correlation ID

Messages are not duplicated (deduplication by provider message ID).

### 4.4 Participant Display

Each participant is rendered using the central visual role registry.
Sensitive data (phone numbers) are masked for USER-level roles.

---

## 5. Feature Flags

| Flag | Default | Purpose |
|------|---------|---------|
| `unified_conversation_enabled` | `false` | Unified conversation resolution |
| `actor_registry_enabled` | `false` | Actor registry API |
| `exchange_taxonomy_enabled` | `false` | Exchange taxonomy API |

---

## 6. Public Contracts

### Actor Registry
- `GET actors/roles` — list all visual roles
- `GET actors/roles/{code}` — get specific role

### Exchange Taxonomy
- `GET exchange/directions` — list directions
- `GET exchange/content-types` — list content types
- `GET exchange/types` — list exchange types
- `GET exchange/results` — list exchange results

All endpoints return `{"status": "disabled"}` when feature flag is off.

---

## 7. Privacy and Masking

- Phone numbers in display names are masked: `+237 6•• •• •• 67`
- User-named actors longer than 12 chars are truncated
- System actors use `INTERNAL` privacy level
- Email masking is available per visual role configuration

---

## 8. Examples

```text
🤖 LAWIM AI: Dans quelle ville recherchez-vous un bien ?
🧑‍💼 LAWIM (Abel): Bonjour, je reprends votre demande.
🏠 Agent immobilier (Jean): Une visite peut être organisée demain.
👤 +237 6•• •• •• 12: Je souhaite continuer sur WhatsApp.
```

---

## 9. Known Limitations

- Actor resolution from external endpoint relies on CRM contacts by phone matching
- Conversation persistence uses existing repository layer (no dedicated UnifiedConversation table yet)
- Channel normalizer reuses existing Green API and Telegram webhook parsers
- Exchange taxonomy is backward-compatible with existing communication direction constants

---

## 10. Tests

| Test Module | Tests | Scope |
|-------------|-------|-------|
| `test_program_j_foundation` | 137 | Models, services, taxonomy, display |
| Knowledge Runtime (H) | 445 | Non-regression |
| **Total** | **582** | |

---

## 11. Validators

| Validator | Result |
|-----------|--------|
| `validate_program_j_foundation.py` | PASS |
| `validate_knowledge_registries.py` | PASS |
| `validate_qualification_matrices.py` | PASS |
