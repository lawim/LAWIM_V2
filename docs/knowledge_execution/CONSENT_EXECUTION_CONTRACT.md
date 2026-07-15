# CONSENT EXECUTION CONTRACT

**Domain:** Consent Management — Relationship Engine
**Version:** 1.0
**Status:** CANONICAL
**Source:** Heritage Gold — CRM_MODEL.md §11, WORKFLOW_EXTRACTION_COMPLETE.md §5, §25
**Prerequisite:** RELATIONSHIP_EXECUTION_ARCHITECTURE.md, DATA_SHARING_POLICY.md

---

## 0. H0.5 Integration — Consent & Privacy Field Alignment

### 0.1 H0.5 Privacy Levels → Consent Requirements

The H0.5 qualification matrices assign privacy levels to every field (from `PRIVACY_AND_SENSITIVE_FIELDS.md`). These levels determine when consent is required:

| H0.5 Privacy Level | Consent Required Before | Consent Type (This Contract) |
|--------------------|------------------------|------------------------------|
| **PUBLIC** | Never | No consent required |
| **PRIVATE** | Sharing with counterparty | `data_sharing` (§6) |
| **SENSITIVE** | Collection + sharing | Explicit opt-in per field |
| **CONFIDENTIAL** | Collection (with legal basis) + sharing (with NDA) | Legal basis + `data_sharing` + NDA |

### 0.2 H0.5 Per-Matrix Consent-Aware Fields

Each matrix in `qualification_matrices.json` defines `sensitive_fields`. The Consent Engine must check these before consent requests:

```typescript
function get_consent_requirements(matrix_id: string): ConsentRequirement[] {
  const matrix = loadMatrix(matrix_id);
  return matrix.sensitive_fields.map(field => ({
    field_id: field,
    privacy_level: fieldDictionary.fields[field].privacy_level,
    required_for: "sharing",
    consent_type: mapPrivacyToConsentType(fieldDictionary.fields[field].privacy_level)
  }));
}
```

### 0.3 H0.5 Privacy Alignment with Consent Types

| This Contract Consent Type | Corresponding H0.5 Privacy Level | Required For |
|---------------------------|----------------------------------|--------------|
| `demandeur_consent` (§3) | PRIVATE (identity) | Reveal demandeur identity to holder |
| `holder_consent` (§4) | PRIVATE (property/identity) | Reveal holder identity to demandeur |
| `agent_optin` (§5) | PRIVATE (contact) | Share contact with agent |
| `data_sharing` (§6) | PRIVATE + SENSITIVE | Share phone, email, financial data |
| `gdpr_deletion` (§7) | ALL | Anonymize personal data |

Alignment is verified: consent collection timing matches H0.5 privacy levels — PUBLIC fields never require consent, PRIVATE fields require sharing consent, SENSITIVE fields require explicit collection + sharing consent, CONFIDENTIAL fields require legal basis.

### 0.4 H0.5 Sensitive Field Handling During Consent

From `PRIVACY_AND_SENSITIVE_FIELDS.md` §6 (Consent Management):

> For SENSITIVE fields: "Nous avons besoin de votre consentement explicite pour collecter [field]. Ceci est nécessaire pour [purpose]."
>
> For CONFIDENTIAL fields: "Ces informations seront partagées uniquement avec [professional] sous accord de confidentialité."

The Consent Engine implements these templates for consent requests involving H0.5 sensitive/confidential fields.

---

## 1. H1 Heritage Layer — Consent Model Overview

Consent is the foundational permission mechanism in LAWIM. No relationship, no data sharing, and no agent introduction occurs without explicit, recorded, and auditable consent from the relevant party.

### 1.1 Consent Types

| Type | Code | Description | Required For |
|---|---|---|---|
| **Demandeur Consent** | `demandeur_consent` | Demandeur confirms interest in contacting holder | Relationship creation |
| **Holder Consent** | `holder_consent` | Holder accepts contact from demandeur | Relationship creation |
| **Agent Opt-In** | `agent_optin` | User accepts contact from a professional agent | Agent introduction |
| **Data Sharing Consent** | `data_sharing` | Party agrees to share specific data fields | Coordinate disclosure |
| **GDPR Deletion Request** | `gdpr_deletion` | User requests deletion of their data | Data erasure |

### 1.2 Consent Principles

| Principle | Description |
|---|---|
| **Explicit** | Consent must be actively given (opt-in, never opt-out) |
| **Informed** | Party must understand what they are consenting to |
| **Specific** | Consent is scoped to a specific purpose |
| **Revocable** | Consent can be withdrawn at any time |
| **Recorded** | Every consent is immutably logged |
| **Time-bound** | Consent may have an expiration |
| **Auditable** | Full trace of consent lifecycle is maintained |

---

## 2. Consent Lifecycle

### 2.1 Lifecycle States

```
                    ┌──────────────┐
                    │   REQUESTED  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
              ┌─────│   GRANTED    │─────┐
              │     └──────┬───────┘     │
              │            │             │
              │            ▼             │
              │     ┌──────────────┐     │
              │     │   REVOKED    │     │
              │     └──────────────┘     │
              │                          │
              │            ▼             │
              │     ┌──────────────┐     │
              └────►│   EXPIRED    │◄────┘
                    └──────────────┘
```

### 2.2 State Definitions

| State | Description | Entered When | Can Transition To |
|---|---|---|---|
| `requested` | Consent has been asked but not yet answered | System sends consent request | `granted`, `expired` |
| `granted` | Party has explicitly consented | Party responds affirmatively | `revoked`, `expired` |
| `revoked` | Party has withdrawn consent | Party requests revocation | None (terminal) |
| `expired` | Consent validity period has elapsed | Timer expires without renewal | None (terminal) |

### 2.3 State Transitions

| From | To | Trigger | Guard | Action |
|---|---|---|---|---|
| `requested` | `granted` | Party accepts | Party is authorized, request is valid | Log consent, execute side effects |
| `requested` | `expired` | SLA timeout | Timer expired | Notify party, close pending action |
| `granted` | `revoked` | Party withdraws | Party is authorized, consent was active | Log revocation, execute rollback |
| `granted` | `expired` | Validity period elapsed | Timer expired | Log expiration, notify party |

### 2.4 SLA Per State

| State | Default SLA | Escalation |
|---|---|---|
| `requested` (demandeur) | 48h | Reminder at 24h, then close at 48h |
| `requested` (holder) | Per property type (24h-30d) | Silence workflow: 3 reminders |
| `granted` (demandeur) | 90 days | Renewal request before expiry |
| `granted` (holder) | 90 days | Renewal request before expiry |

> **ARCHITECTURE_DECISION:** Default SLA durations (48h demandeur, 24h-30d holder, 90d consent validity) are architecture-defined defaults. Actual durations must be validated with business stakeholders during implementation.

> **ARCHITECTURE_DECISION:** The idempotency triple (demandeur_id, holder_id, property_id) distinguishes technical duplicates from legitimate new propositions (e.g., same property re-listed after expiration). See RELATIONSHIP_LIFECYCLE.md for full discussion.

---

## 3. Demandeur Consent

### 3.1 Trigger

Demandeur selects a matched property and indicates interest.

### 3.2 Consent Request

```
System: "Souhaitez-vous que nous contactions le détenteur de [property_address]
         pour organiser une mise en relation ?
         - ✅ Oui, contactez le détenteur
         - ❌ Non, pas pour le moment
         - ℹ️ Plus d'informations sur ce bien"
```

### 3.3 Consent Recording

| Field | Value |
|---|---|
| `consent_type` | `demandeur_consent` |
| `party_role` | `demandeur` |
| `scope` | `{"purpose": "contact_holder", "relationship_type": "buy/rent"}` |
| `status` | `granted` on acceptance |
| `channel` | As per interaction channel |

### 3.4 Side Effects on Grant

- Relationship state transitions to `consent_holder_pending`
- NBA computed: `contact_holder`
- Notification sent to holder with masked demandeur identity

### 3.5 Side Effects on Denial

- Relationship state transitions to `closed`
- Match recorded as refused
- Rematching triggered per MATCH-017 rules

---

## 4. Holder Consent

### 4.1 Trigger

Demandeur consent is obtained and holder contact is initiated.

### 4.2 Consent Request

```
System: "Une personne intéressée par votre bien [property_ref]
         ([property_address]) souhaite vous rencontrer.
         
         - ✅ Accepter la mise en relation
         - ❌ Refuser
         - ⏳ Plus tard (me rappeler dans X jours)
         - 🔄 Proposer un autre bien
         - 🚫 Déclarer le bien indisponible"
```

### 4.3 Consent Recording

| Field | Value |
|---|---|
| `consent_type` | `holder_consent` |
| `party_role` | `holder` |
| `scope` | `{"purpose": "accept_contact", "property_id": "..."}` |
| `status` | `granted` on acceptance |

### 4.4 Holder Response Handling

| Response | Action | Side Effect |
|---|---|---|
| `accept` | Consent recorded as granted | Relationship activated, anonymity lifted |
| `refuse` | Consent recorded as declined | Relationship closed, rematching triggered |
| `delay` | Timer set for requested duration | Reminder scheduled, status stays `requested` |
| `alternative` | System records alternative proposal | Rematching on alternative property |
| `declare_unavailable` | Property marked unavailable | Relationship closed, property status updated |

### 4.5 Holder Silence Workflow

Per Heritage Gold WORKFLOW_EXTRACTION_COMPLETE.md §5:

```
First reminder (at 1x SLA)
        ↓
Second reminder (at 2x SLA)
        ↓
Last reminder (at 3x SLA)
        ↓
Property marked "to confirm"
        ↓
Rematching triggered
        ↓
LAWIM collaborator notified
```

---

## 5. Agent Opt-In (4-Step Process)

Per Heritage Gold CRM_MODEL.md §11:

### 5.1 Step 1: Detection

```
Trigger: A dossier or relationship matches conditions requiring agent intervention
Condition: property type in agent zone, demandeur requests professional help
Detection: System evaluates agent_zones, property_type, demandeur preference
```

### 5.2 Step 2: Permission Request

```
System: "Voulez-vous recevoir le contact d'un agent spécialisé
         dans votre zone pour vous accompagner dans votre recherche ?
         - ✅ Oui, contactez un agent
         - ❌ Non, merci"
```

### 5.3 Step 3: Consent Log

| Field | Value |
|---|---|
| `consent_type` | `agent_optin` |
| `party_role` | `demandeur` |
| `scope` | `{"purpose": "agent_contact", "zone": "...", "property_type": "..."}` |
| `status` | `accepted` / `declined` |
| `source` | `whatsapp` / `telegram` / `web` |
| Stored in | `agent_optins` table |

### 5.4 Step 4: Conditional Share

- If `accepted`: System routes demandeur contact to appropriate agent via CRM routing
- If `declined`: No share, no agent follow-up, no repeated request within 30 days

### 5.5 Agent Opt-In Refusal Rules

| Rule | Behavior |
|---|---|
| First refusal | No agent contact, no follow-up request for 30 days |
| Second refusal (same zone) | No agent contact, permanent opt-out for that zone |
| Opt-out across all zones | Global agent opt-out flag set on user profile |
| Opt-in reversal | User may re-enable agent opt-in at any time via settings |

---

## 6. Data Sharing Consent

### 6.1 Trigger

When either party requests direct contact coordinates (phone, email, address) outside the LAWIM-mediated channel, explicit data sharing consent is required.

### 6.2 Request

```
System: "[Party Name] souhaite partager ses coordonnées de contact
         avec vous. Acceptez-vous ?
         
         Coordonnées partagées : [phone, email]
         
         - ✅ Oui, partager mes coordonnées
         - ❌ Non, rester sur LAWIM"
```

### 6.3 Scope Definition

| Scope Level | Data Shared | Validity |
|---|---|---|
| `basic_contact` | Phone number only | Single relationship |
| `full_contact` | Phone + email + address | Single relationship |
| `professional_contact` | Phone + email + agency address | All relationships with same agent |
| `temporary_access` | Phone only | 7 days |

### 6.4 Side Effects

- Coordinates are revealed to the authorized party
- Record logged in `data_sharing_log`
- Revocable at any time
- If revoked, coordinates are re-masked

---

## 7. GDPR Deletion Request

### 7.1 Trigger

User sends "SUPPRIMER MES DONNÉES" (or equivalent in supported languages).

### 7.2 7-Day Delay

Per RGPD compliance and LAWIM heritage rules:

```
Day 0: User request received
        → System acknowledges request
        → Sets deletion_timer = NOW() + 7 days
        → Notifies user of 7-day delay and consequences

Day 1-6: User may cancel deletion request
         → "delete.request_cancelled" event logged
         → Timer cleared

Day 7: Deletion executed (if not cancelled)
       → All personal data anonymized per DATA_SHARING_POLICY.md
       → Consent records marked as `revoked`
       → Active relationships closed
       → User notified of completion
```

### 7.3 Deletion Scope

| Data Category | Action |
|---|---|
| Personal identity (name, email, phone) | Anonymized (replaced with hash) |
| Conversation history | Anonymized (party references removed) |
| Relationship data | Anonymized (party references removed) |
| Consent records | Retained (immutable audit, party reference anonymized) |
| Transaction history | Retained (anonymized for statistics) |
| Activity logs | Retained (anonymized) |
| Financial records | Retained per legal obligation |

### 7.4 Deletion Execution

| Step | Action |
|---|---|
| 1 | Cancel all pending consent requests for user |
| 2 | Revoke all active consents for user |
| 3 | Close all active relationships involving user |
| 4 | Anonymize user personal data in `persons` table |
| 5 | Anonymize user references in `relationships`, `consents`, `conversations` |
| 6 | Update `anonymization_requests` table with completion timestamp |
| 7 | Log `gdpr.deletion_completed` event |

---

## 8. Revocation Handling

### 8.1 Revocation Request Sources

| Source | Channel | Validation |
|---|---|---|
| User sends "Je révoque mon consentement" | WhatsApp/Telegram | Identity verification |
| User clicks "Revoke consent" | Web/Mobile app | Session authentication |
| User calls support | Phone | Support agent verification |

### 8.2 Revocation Effects by Consent Type

| Consent Type | Revocation Effect | Data State |
|---|---|---|
| `demandeur_consent` | Relationship terminated, holder notified | Relationship archived |
| `holder_consent` | Relationship terminated, demandeur notified | Relationship archived |
| `agent_optin` | Agent contact disabled, no new agent routing | Opt-in record marked revoked |
| `data_sharing` | Coordinates re-masked, access revoked | Sharing log updated |

### 8.3 Revocation Timeline

| Phase | Action |
|---|---|
| Immediate | Consent status set to `revoked` |
| Within 1h | Side effects executed (notifications, state updates) |
| Within 24h | All dependent processes terminated |
| Audit | Revocation recorded with timestamp, actor, reason |

### 8.4 Irreversibility

> Consent revocation is irreversible. A new consent must be obtained for any future operation. The revocation record is immutable and retained for audit purposes.

---

## 9. Consent Persistence & Audit

### 9.1 Storage

All consent records are stored in the `consents` table with immutability guarantees:

| Guarantee | Mechanism |
|---|---|
| Append-only | No updates to granted/revoked records, only status transitions |
| Immutable audit | Consent events are written to `consent_events` table |
| Cryptographic chain | Optional: hash-linked consent events for tamper evidence |
| Retention | Consent records are NEVER deleted (per LAWIM heritage principle) |

### 9.2 Audit Events

| Event | Trigger | Data |
|---|---|---|
| `consent.requested` | System sends consent request | `consent_id`, `party_id`, `type`, `scope` |
| `consent.granted` | Party accepts | `consent_id`, `channel`, `response_time` |
| `consent.declined` | Party refuses | `consent_id`, `reason` (optional) |
| `consent.revoked` | Party withdraws | `consent_id`, `reason` |
| `consent.expired` | Timer elapses | `consent_id`, `expiry_date` |
| `consent.auto_closed` | System closes due to SLA | `consent_id`, `sla_exceeded` |
| `gdpr.deletion_requested` | User requests deletion | `person_id`, `request_channel` |
| `gdpr.deletion_completed` | Deletion executed | `person_id`, `anonymized_fields` |

### 9.3 Audit Record Structure

```json
{
  "audit_id": "UUID",
  "event_type": "consent.granted",
  "timestamp": "2026-07-15T10:30:00Z",
  "consent_id": "UUID",
  "party_id": "UUID",
  "actor_id": "UUID",
  "old_status": "requested",
  "new_status": "granted",
  "scope": {
    "purpose": "contact_holder",
    "relationship_type": "buy"
  },
  "metadata": {
    "channel": "whatsapp",
    "response_time_seconds": 120,
    "conversation_id": "UUID"
  },
  "signature": "hash_of_previous_event + payload_hash"
}
```

---

## 10. Error States & Fallbacks

| Error | Fallback | Alert |
|---|---|---|
| Consent request undeliverable | Retry 3x with backoff, then mark failed | LAWIM collaborator notified |
| Party responds with unclear answer | Request clarification ("Je n'ai pas bien compris. Pouvez-vous répondre par Oui ou Non ?") | Logged for NLP learning |
| Consent race condition (double response) | First response wins, second is logged | None |
| Consent expiry during processing | Treat as expired, notify both parties | System event logged |
| GDPR deletion during active relationship | Close relationship first, notify other party | LAWIM collaborator assigned |
| Revocation of already-revoked consent | No-op, log attempt | None |

---

## 11. References

| Reference | File |
|---|---|
| Heritage Gold — Agent Opt-In (4 steps) | `docs/lawim_heritage_gold/CRM_MODEL.md` §11 |
| Heritage Gold — Double Consent Rule | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §25 |
| Heritage Gold — Mise en Relation Lifecycle | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §5 |
| Heritage Gold — CRM Database Tables | `docs/lawim_heritage_gold/CRM_MODEL.md` §19 |
| Relationship Execution Architecture | `docs/knowledge_execution/RELATIONSHIP_EXECUTION_ARCHITECTURE.md` |
| Data Sharing Policy | `docs/knowledge_execution/DATA_SHARING_POLICY.md` |
| Relationship Lifecycle | `docs/knowledge_execution/RELATIONSHIP_LIFECYCLE.md` |
