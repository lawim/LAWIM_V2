# RELATIONSHIP EXECUTION ARCHITECTURE

**Domain:** Relationship Engine — Mise en Relation Execution
**Version:** 1.0
**Status:** CANONICAL
**Source:** Heritage Gold — WORKFLOW_EXTRACTION_COMPLETE.md §5, CRM_MODEL.md, ROLE_MODEL.md
**Prerequisite:** MATCHING_MODEL.md, CONSENT_EXECUTION_CONTRACT.md, RELATIONSHIP_LIFECYCLE.md

---

## 0. H0.5 Integration — Sensitive/Confidential Field Handling & Alignment

### 0.1 H0.5 Privacy-Aware Relationship Flow

The H0.5 qualification matrices classify fields by privacy level (`PRIVACY_AND_SENSITIVE_FIELDS.md`). The Relationship Engine enforces these classifications throughout the relationship lifecycle:

| Relationship Phase | H0.5 Fields Active | Privacy Constraint |
|--------------------|-------------------|--------------------|
| Proposition | PUBLIC fields only (city, property_type, neighborhood) | No identity/budget exposed to holder |
| Demandeur Consent | PRIVATE fields revealed with consent (nom, téléphone) | Consent required from demandeur |
| Introduction (post-double-consent) | PRIVATE fields (nom, téléphone, email) shared bidirectionally | Both parties consented |
| Visit | PRIVATE fields (adresse_exacte, coordonnees_gps) shared | Visit consent obtained |
| Transaction | SENSITIVE + CONFIDENTIAL fields (financing, num_titre, litiges) | Legal basis + NDA required |

### 0.2 H0.5 Per-Matrix Sensitive Field Enforcement

Each matrix in `qualification_matrices.json` has a `sensitive_fields` array. The Relationship Engine must:

1. Load the active matrix for the relationship's dossier
2. Identify all sensitive/confidential fields
3. Enforce consent gates before sharing each field
4. Never share CONFIDENTIAL fields through the platform

```typescript
function enforcePrivacy(relationship: Relationship): PrivacyGate[] {
  const matrix = loadMatrix(relationship.dossier.matrix_id);
  return matrix.sensitive_fields.map(field => ({
    field_id: field,
    privacy_level: fieldDictionary.fields[field].privacy_level,
    sharing_allowed: canShareField(relationship, field),
    consent_required: fieldDictionary.fields[field].privacy_level !== "public",
    consent_obtained: hasConsent(relationship, field)
  }));
}
```

### 0.3 H0.5 Privacy Level → Data Visibility Alignment

Comparison of this contract's anonymity phases with H0.5 privacy levels:

| This Contract §4 Phase | H0.5 Max Privacy Level Exposed | Alignment |
|------------------------|-------------------------------|-----------|
| Before Double Consent (§4.1) | PUBLIC only | ✅ Aligned — See §2.1 Data Visibility |
| After Double Consent (§4.2) | PRIVATE (with consent) | ✅ Aligned — See §2.3 Data Visibility |
| Agent Opt-In (§4.3) | PRIVATE (with consent) | ✅ Aligned — See §2.4 Agent Opt-In |

### 0.4 H0.5 → H1 Contradiction Resolution

| H0.5 Rule | H1 Rule | Resolution |
|-----------|---------|------------|
| per-matrix sensitive_fields | Fixed field sensitivity in DATA_SHARING_POLICY.md | **ARCHITECTURE_DECISION_RETAINED** — H1 fixed visibility tables apply at policy level; per-matrix sensitive_fields add an additional enforcement layer |
| CONFIDENTIAL fields never shared via platform | Coordinate unlock via paid service (500 FCFA) | **ARCHITECTURE_DECISION_RETAINED** — Paid coordinate unlock applies to PRIVATE fields only; CONFIDENTIAL fields remain excluded |
| INTRODUCTION_READY as readiness level | Relationship created post-consent | **RESOLVED_BY_H05** — The INTRODUCTION_READY readiness level (from READINESS_MODEL.md) acts as the gate before relationship creation |

---

## 1. H1 Heritage Layer — Relationship Engine Overview

The Relationship Engine is the domain engine responsible for orchestrating the Mise en Relation lifecycle — from match selection through relationship creation, active management, and eventual closure. It enforces the double consent model, anonymity principle, and all SLA/NBA rules governing demandeur-holder interactions.

### Position in the Execution Pipeline

```
Decision Engine (resolves NBA: "Contact the holder")
        │
        ▼
Relationship Engine ─────────────────────────────────────────────┐
        │                                                        │
        ├──→ Matching Engine (validate match, compute scores)    │
        ├──→ Consent Engine (manage double consent)             │
        ├──→ Conversation Engine (enable direct messaging)      │
        ├──→ CRM Engine (route to agent if opt-in)              │
        └──→ Audit Engine (trace every transition)              │
        │                                                        │
        ▼                                                        │
Action Executor (create relationship, update state, notify)      │
        │                                                        │
        ▼                                                        │
Relationship Store (persist state, enforce idempotency) ─────────┘
```

### Engine Responsibilities

| Responsibility | Description |
|---|---|
| **Match Reception** | Accept match propositions from the Matching Engine after demandeur interest is confirmed |
| **Consent Orchestration** | Manage the double consent workflow — demandeur consent first, then holder consent |
| **Anonymity Enforcement** | Keep demandeur identity masked from holder until consent is obtained |
| **Relationship State Machine** | Execute state transitions per RELATIONSHIP_LIFECYCLE.md |
| **Idempotency** | Guarantee that no duplicate relationship is created for the same demandeur-holder-property triple |
| **Expiration Timer Management** | Enforce SLAs per state; trigger NBA when timers expire |
| **Follow-up Scheduling** | Schedule NBA-driven follow-ups during active relationships |
| **Escalation** | Escalate stalled relationships to LAWIM collaborators |
| **Revocation & Closure** | Handle revocation requests, closure conditions, and archival |

---

## 2. Full Relationship Lifecycle

### 2.1 Lifecycle Flow

```
Match Selected (by demandeur)
        │
        ▼
Proposition (system presents property to demandeur)
        │
        ▼
Data Disclosure Preview (demandeur sees masked info)
        │
        ▼
Demandeur Consent (demandeur confirms interest)
        │
        ▼
Holder Contact (system contacts holder with masked demandeur)
        │
        ▼
Holder Consent (holder accepts/refuses/delays)
        │
        ▼
Relationship Created (double consent obtained)
        │
        ▼
Introduction (interlocutor visibility changes from 🤖 to 👤)
        │
        ▼
Active (follow-up, visit scheduling, negotiation)
        │
        ▼
Follow-up (NBA-driven periodic engagement)
        │
        ▼
Expiration / Revocation / Closure (terminal states)
```

### 2.2 Phase Details

#### Phase 1: Match Selected → Proposition

| Step | Action | System Behavior |
|---|---|---|
| 1.1 | Demandeur selects a match from propositions | Matching Engine records selection |
| 1.2 | System validates dossier is active, property is available | Guard check |
| 1.3 | System generates a proposition record | Status: `proposed` |
| 1.4 | NBA computed: `present_property` | Decision Engine logs NBA |

#### Phase 2: Data Disclosure Preview

| Data Field | Demandeur Sees | Holder Sees |
|---|---|---|
| Property address | Full | Full |
| Property photos | Full | Full |
| Property price | Full | Full |
| Holder identity | Masked ("Propriétaire") | Full |
| Holder phone | Hidden | Full |
| Demandeur identity | Full | Masked ("Personne intéressée") |
| Demandeur phone | Full | Hidden |

#### Phase 3: Demandeur Consent

- System asks: "Souhaitez-vous que nous contactions le détenteur de ce bien ?"
- Demandeur response: `accept` / `decline` / `request_more_info`
- On accept → consent record created (`consent_demandeur_pending` → `consent_granted`)
- On decline → relationship closed, rematching triggered
- On `request_more_info` → system provides additional details from disclosure preview

#### Phase 4: Holder Consent

- System contacts holder via preferred channel (WhatsApp/Telegram)
- Message template: "Une personne intéressée par votre bien [property_ref] souhaite vous rencontrer. Acceptez-vous d'être mis en relation ?"
- Holder response: `accept` / `refuse` / `delay` / `alternative` / `declare_unavailable`
- On accept → relationship progresses
- On refuse → relationship closed, rematching triggered
- On delay → reminder timer set per SLA
- On alternative → holder proposes alternative property
- On `declare_unavailable` → property marked unavailable, rematching

#### Phase 5: Introduction

- Interlocutor changes from `🤖 LAWIM AI` to `👤 Propriétaire` / `🏢 Agence` / `🤝 Introduceur`
- Demandeur and holder can now communicate directly via LAWIM channels
- Contact coordinates may be shared if authorized (paid service or consent)

#### Phase 6: Active & Follow-up

- NBA engine computes next actions per RELATIONSHIP_LIFECYCLE.md
- Possible NBAs: `schedule_visit`, `send_follow_up`, `open_negotiation`, `request_feedback`
- Follow-up cadence: J1, J7, J30, J90 (or custom per SLA)
- Health score tracked per relationship

#### Phase 7: Terminal States

| State | Trigger | Action |
|---|---|---|
| `expired` | Timer exceeded without activity | Notification to both parties, relationship archived |
| `revoked` | Party requests revocation | Consent revoked, relationship closed, data retained per policy |
| `closed` | Objective achieved or abandoned | Satisfaction survey, relationship archived |

---

## 3. Double Consent Model

### 3.1 Principle

> No relationship is created without explicit, recorded consent from BOTH parties. No exceptions.
> — Heritage Gold CONST-006 / Double Consent Rule (WORKFLOW_EXTRACTION_COMPLETE.md §25)

### 3.2 Consent Flow

```
                    ┌──────────────────────────────┐
                    │   Match Selected              │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │   Demandeur Consent Check     │
                    │  - Is demandeur interested?   │
                    └──────┬───────────────┬───────┘
                           │               │
                        Yes │               │ No
                           │               ▼
                           ▼     ┌──────────────────┐
            ┌────────────────┐   │  Close Proposition│
            │  Demandeur      │   │  → Rematching     │
            │  Consent stored │   └──────────────────┘
            └───────┬────────┘
                    │
                    ▼
            ┌──────────────────────────────┐
            │   Holder Consent Request      │
            │   (demandeur identity masked) │
            └──────┬───────────────┬───────┘
                   │               │
                Yes │               │ No
                   │               ▼
                   ▼     ┌──────────────────┐
        ┌────────────────┐│  Close Proposition│
        │  Holder         ││  → Rematching     │
        │  Consent stored │└──────────────────┘
        └───────┬────────┘
                │
                ▼
        ┌──────────────────────────────┐
        │   Relationship Created        │
        │   Double Consent = Granted    │
        │   Anonymity Lifted            │
        └──────────────────────────────┘
```

### 3.3 Consent Persistence

Each consent is recorded as an immutable audit entry:

| Field | Description |
|---|---|
| `consent_id` | UUID |
| `relationship_id` | FK to relationship |
| `party_id` | UUID of consenting party |
| `party_role` | `demandeur` / `holder` / `agent` |
| `consent_type` | `demandeur_consent` / `holder_consent` / `agent_optin` / `data_sharing` |
| `scope` | JSON describing what is consented to |
| `status` | `granted` / `revoked` / `expired` |
| `granted_at` | Timestamp |
| `revoked_at` | Nullable timestamp |
| `expires_at` | Nullable expiration |
| `source` | `whatsapp` / `telegram` / `web` / `system` |
| `audit_trail` | Full conversation context |

---

## 4. Anonymity Principle

### 4.1 Before Double Consent

- Demandeur identity is NEVER revealed to holder
- Holder identity is masked (shown as generic role: "Propriétaire", "Agence")
- Only LAWIM AI mediates communication
- Contact coordinates are NEVER shared

### 4.2 After Double Consent

- Demandeur identity is revealed to holder (name, profile)
- Holder identity is revealed to demandeur (name, agency, role)
- Contact coordinates shared only if:
  - Both parties consent to data sharing
  - Or a paid service has unlocked coordinates (e.g., `deblocage_coordonnees`)

### 4.3 Agent Opt-In

Per CRM_MODEL §11 — Agent Opt-In 4-step process:

| Step | Description |
|---|---|
| 1. **Detection** | System identifies that an agent may be needed (zone, property type) |
| 2. **Permission Request** | "Voulez-vous recevoir le contact d'un agent spécialisé dans votre zone ?" |
| 3. **Consent Log** | Recorded in `agent_optins` table (accepted/declined) |
| 4. **Conditional Share** | Contact shared ONLY if accepted |

> Golden Rule: No agent contact shared without explicit user consent. — CRM_MODEL §11

---

## 5. Integration with Other Engines

### 5.1 Matching Engine

| Integration Point | Direction | Contract |
|---|---|---|
| Match selection notification | Matching → Relationship | `{match_id, dossier_id, property_id, scores}` |
| Proposition validation | Relationship → Matching | `{proposition_id, status}` |
| Rematching trigger | Relationship → Matching | `{dossier_id, reason}` |
| Match score refresh | Matching → Relationship | `{match_id, new_scores}` |

### 5.2 Conversation Engine

| Integration Point | Direction | Contract |
|---|---|---|
| Interlocutor change notification | Relationship → Conversation | `{relationship_id, new_interlocutor}` |
| Direct message enable | Relationship → Conversation | `{relationship_id, permission_granted}` |
| Message relay (pre-consent) | Conversation → Relationship | `{message_id, masked_sender}` |

### 5.3 CRM Engine

| Integration Point | Direction | Contract |
|---|---|---|
| Lead enrichment from relationship | Relationship → CRM | `{relationship_id, outcome}` |
| Agent routing request | Relationship → CRM | `{zone, property_type, demandeur_id}` |
| Agent opt-in check | CRM → Relationship | `{agent_id, optin_status}` |
| Lead scoring update | CRM → Relationship | `{demandeur_id, new_score}` |

### 5.4 Qualification Engine

| Integration Point | Direction | Contract |
|---|---|---|
| Dossier qualification level | Qualification → Relationship | `{dossier_id, qualification_level}` |
| New criteria affecting match | Relationship → Qualification | `{dossier_id, criteria_update}` |

### 5.5 Notification Engine

| Integration Point | Direction | Contract |
|---|---|---|
| Holder contact notification | Relationship → Notification | `{holder_id, template, context}` |
| Demandeur introduction notification | Relationship → Notification | `{demandeur_id, template, context}` |
| Follow-up reminders | Relationship → Notification | `{party_id, due_date, nba}` |
| Expiration warnings | Relationship → Notification | `{party_id, days_remaining}` |

---

## 6. Idempotency Guarantees

### 6.1 Idempotency Key

Every relationship creation uses an idempotency key derived from:

```
idempotency_key = hash(demandeur_id + holder_id + property_id + relationship_type)
```

### 6.2 Idempotency Rules

| Scenario | Behavior |
|---|---|
| Duplicate relationship creation | Returns existing relationship ID, no new record |
| Duplicate consent submission | Returns existing consent record, updates timestamp |
| Duplicate revocation | No-op if already revoked |
| Duplicate follow-up trigger | No-op if follow-up already scheduled within SLA window |

### 6.3 Deduplication Checks

| Check Point | Condition | Action |
|---|---|---|
| Pre-creation | Existing relationship with same triple in non-terminal state | Return existing ID |
| Pre-consent | Consent already recorded for same party + relationship | Return existing consent record |
| Pre-revocation | Relationship already in terminal state | No-op, log attempt |

### 6.4 Race Condition Prevention

- Database-level unique constraint on `(demandeur_id, holder_id, property_id, status != terminal)`
- Optimistic locking on relationship state transitions (version field)
- Distributed lock on idempotency key for concurrent requests

---

## 7. Data Model

### 7.1 Relationship Core

| Field | Type | Description |
|---|---|---|
| `relationship_id` | UUID | Primary key |
| `dossier_id` | UUID | FK to dossier |
| `property_id` | UUID | FK to property |
| `demandeur_id` | UUID | FK to person (demandeur) |
| `holder_id` | UUID | FK to person (holder) |
| `agent_id` | UUID | Nullable FK to agent (if opt-in) |
| `match_id` | UUID | FK to match proposition |
| `relationship_type` | ENUM | `buy` / `rent` / `invest` |
| `status` | ENUM | Current lifecycle state |
| `double_consent_obtained` | BOOLEAN | True when both parties consented |
| `anonymity_lifted_at` | TIMESTAMP | When identities were revealed |
| `idempotency_key` | VARCHAR(64) | Unique deduplication key |
| `created_at` | TIMESTAMP | Record creation |
| `updated_at` | TIMESTAMP | Last state change |
| `expires_at` | TIMESTAMP | SLA-based expiration |
| `version` | INTEGER | Optimistic locking |

### 7.2 Relationship Events

| Field | Type | Description |
|---|---|---|
| `event_id` | UUID | Primary key |
| `relationship_id` | UUID | FK to relationship |
| `event_type` | ENUM | See RELATIONSHIP_LIFECYCLE.md audit events |
| `old_status` | ENUM | Previous state |
| `new_status` | ENUM | New state |
| `actor_id` | UUID | Who triggered the transition |
| `actor_role` | ENUM | Role of actor |
| `reason` | TEXT | Transition reason |
| `metadata` | JSONB | Arbitrary context |
| `created_at` | TIMESTAMP | Event timestamp |

### 7.3 Consent Records

| Field | Type | Description |
|---|---|---|
| `consent_id` | UUID | Primary key |
| `relationship_id` | UUID | FK to relationship |
| `party_id` | UUID | FK to person |
| `party_role` | ENUM | `demandeur` / `holder` / `agent` |
| `consent_type` | ENUM | As defined in §3.3 |
| `scope` | JSONB | Consented data scope |
| `status` | ENUM | `granted` / `revoked` / `expired` |
| `granted_at` | TIMESTAMP | When consent was given |
| `revoked_at` | TIMESTAMP | When consent was revoked |
| `expires_at` | TIMESTAMP | Consent expiration |
| `audit_trail` | JSONB | Conversation context |

---

## 8. Error States & Fallbacks

| Error Condition | Fallback | Alert |
|---|---|---|
| Holder unreachable after SLA | Mark property "to confirm", trigger rematching | LAWIM collaborator notified |
| Demandeur unreachable | Follow-up cadence per SLA, then auto-close | LAWIM collaborator notified |
| Consent timeout | Relationship moved to `expired` | Both parties notified |
| Double consent mismatch | System logs conflict, requires manual resolution | LAWIM collaborator assigned |
| Race condition on creation | Retry with backoff, log conflict | System alert if >3 retries |
| Database constraint violation | Return existing relationship | None (idempotent) |

---

## 9. NBA Integration

### 9.1 Relationship-Specific NBAs

| Relationship State | NBA |
|---|---|
| `proposed` | Present property details, ask for demandeur interest |
| `consent_demandeur_pending` | Follow up with demandeur for decision |
| `consent_holder_pending` | Contact holder, send reminders per silence workflow |
| `active` | Schedule visit, send follow-up, open negotiation |
| `follow_up` | Check activity, suggest next step |
| `expired` | Propose renewal, trigger rematching |

### 9.2 NBA Priority (Decision Engine)

Per Heritage Gold Decision Engine Priority (Ch88):

| Priority | Action |
|---|---|
| 1 | Correct an incoherence |
| 2 | Complete a critical field |
| 3 | Matching |
| 4 | **Present a property** |
| 5 | **Contact the holder** |
| 6 | **Organize a visit** |
| 7 | **Follow up** |
| 8 | Notifications |
| 9 | Dossier optimization |

Relationship Engine handles priorities 4-7 primarily.

---

## 10. Audit & Traceability

Every relationship operation MUST produce an immutable audit record:

```
┌────────────────────────────────────────────┐
│           AUDIT RECORD                      │
│  • relationship_id                          │
│  • event_type + timestamp                   │
│  • old_status → new_status                  │
│  • actor_id + actor_role                    │
│  • input_state_snapshot                     │
│  • all_applicable_rules                     │
│  • selected_rule + reason                   │
│  • rejected_rules + reasons                 │
│  • NBA resolved                             │
│  • execution_outcome                        │
└────────────────────────────────────────────┘
```

---

## 11. References

| Reference | File |
|---|---|
| Heritage Gold — Mise en Relation Lifecycle | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §5 |
| Heritage Gold — Double Consent Rule | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §25 |
| Heritage Gold — CRM Agent Opt-In | `docs/lawim_heritage_gold/CRM_MODEL.md` §11 |
| Heritage Gold — Role Model | `docs/lawim_heritage_gold/ROLE_MODEL.md` |
| Heritage Gold — Decision Engine Priority | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §4 |
| Consent Execution Contract | `docs/knowledge_execution/CONSENT_EXECUTION_CONTRACT.md` |
| Relationship Lifecycle State Machine | `docs/knowledge_execution/RELATIONSHIP_LIFECYCLE.md` |
| Data Sharing Policy | `docs/knowledge_execution/DATA_SHARING_POLICY.md` |
| Conversation Execution Architecture | `docs/knowledge_execution/CONVERSATION_EXECUTION_ARCHITECTURE.md` |
