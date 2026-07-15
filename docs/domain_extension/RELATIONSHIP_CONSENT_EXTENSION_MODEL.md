# RELATIONSHIP & CONSENT EXTENSION MODEL

**Document ID:** LAWIM-H13-RC-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §7 (Relationship), §8 (Consent), §11 (CRM Pipeline)
**Source Crosswalks:** required_extensions.json (workflows, sla, nba), CONSENT_EXECUTION_CONTRACT.md, RELATIONSHIP_LIFECYCLE.md, RELATIONSHIP_EXECUTION_ARCHITECTURE.md

---

## Table of Contents

1. [Match Model with Consent Tracking](#1-match-model-with-consent-tracking)
2. [Proposal Workflow](#2-proposal-workflow)
3. [Double Consent Model](#3-double-consent-model)
4. [Relationship Entity](#4-relationship-entity)
5. [Participant Roles in a Relationship](#5-participant-roles-in-a-relationship)
6. [Introduction Tracking](#6-introduction-tracking)
7. [Shared Data Scope Per Relationship](#7-shared-data-scope-per-relationship)
8. [Consent Lifecycle](#8-consent-lifecycle)
9. [Revocation Workflow](#9-revocation-workflow)
10. [Expiration Handling](#10-expiration-handling)
11. [Idempotency Guarantees](#11-idempotency-guarantees)
12. [Audit Trail for All Consent Changes](#12-audit-trail-for-all-consent-changes)
13. [Human Handover Workflow](#13-human-handover-workflow)

---

## 1. Match Model with Consent Tracking

### 1.1 Consent-Aware Match Entity

The `Match` entity extends the matching engine concept with full consent tracking. Every match carries the consent state of both parties throughout its lifecycle.

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to Project (demandeur dossier) |
| `property_id` | UUID | Reference to Property |
| `agent_id` | UUID? | Reference to assigned agent |
| `overall_score` | Float | Composite score (0-100) |
| `compatibility_level` | Enum | `excellent \| good \| average \| low` |
| `rank` | Int | Ranking position for this project |
| `is_active` | Boolean | Whether match is currently active |
| `is_proposed` | Boolean | Whether match has been proposed to demandeur |
| `demandeur_decision` | Enum? | `pending \| interested \| not_interested` |
| `holder_decision` | Enum? | `pending \| favorable \| refused` |
| `demandeur_consent_id` | UUID? | Reference to demandeur consent record |
| `holder_consent_id` | UUID? | Reference to holder consent record |
| `double_consent_obtained_at` | DateTime? | Timestamp when both consents were granted |
| `decision_deadline` | DateTime? | Deadline for current decision step |
| `rematch_count` | Int | Number of rematches for this pair |
| `rematch_reason` | String? | Reason for rematch trigger |
| `match_pool` | Enum | `primary \| expansion_geo \| expansion_budget \| expansion_type` |
| `created_at` | DateTime | Match creation timestamp |
| `expires_at` | DateTime | Match expiration |
| `proposed_at` | DateTime? | When match was proposed |
| `demandeur_decided_at` | DateTime? | When demandeur decided |
| `holder_decided_at` | DateTime? | When holder decided |

### 1.2 Consent-Tracking State Machine

```
created → scored → proposed → demandeur_consent_pending
                                   ↓
                           demandeur_consent_granted
                                   ↓
                            holder_consent_pending
                                   ↓
                     double_consent_obtained → relationship_established → active → closed/archived
```

| State | Consent Tracking | Description |
|-------|-----------------|-------------|
| `created` | No consent | Match record created by scoring engine |
| `scored` | No consent | Scores computed, awaiting proposal threshold |
| `proposed` | No consent | Match proposed to demandeur |
| `demandeur_consent_pending` | Awaiting C1 | Demandeur asked to consent |
| `demandeur_consent_granted` | C1 obtained | Demandeur consented, holder not yet contacted |
| `holder_consent_pending` | C1 valid, awaiting C2 | Holder asked to consent |
| `double_consent_obtained` | C1 + C2 obtained | Both consents granted, relationship ready |
| `relationship_established` | C1 + C2 active | Relationship entity created |
| `active` | C1 + C2 active | Relationship is live |
| `expired` | Consent expired | Match validity elapsed |
| `closed` | Consent terminated | Match concluded |
| `archived` | Archived | Final archival state |

---

## 2. Proposal Workflow

### 2.1 Proposal Creation

When a match score >= 60 and rank is in the top 10, the system creates a proposal for the demandeur.

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `match_id` | UUID | Reference to the match |
| `project_id` | UUID | Demandeur dossier |
| `property_id` | UUID | Proposed property |
| `proposal_version` | Int | Version counter for amendments |
| `status` | Enum | `draft \| sent \| accepted \| rejected \| withdrawn \| expired` |
| `presentation` | JSON | Score breakdown, property highlights, comparison |
| `sent_at` | DateTime? | When proposal was delivered |
| `responded_at` | DateTime? | When demandeur responded |
| `response` | Enum? | `interested \| not_interested \| need_more_info` |
| `created_at` | DateTime | Proposal creation |
| `expires_at` | DateTime | Proposal validity deadline |

### 2.2 Proposal Flow

```
             ┌──────────────┐
             │   MATCHED    │
             │  score ≥ 60  │
             └──────┬───────┘
                    ▼
             ┌──────────────┐
             │   PROPOSAL   │
             │    DRAFT     │
             └──────┬───────┘
                    ▼
             ┌──────────────┐
             │   PROPOSAL   │
             │    SENT      │
             └──────┬───────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │INTERESTED│ │NOT_INTER│ │NEED_MORE│
   │         │ │  ESTED  │ │  INFO   │
   └────┬────┘ └────┬────┘ └────┬────┘
        ▼           ▼           ▼
   Consent C1    Rematch    Answer Qs
   workflow     triggered   → re-send
```

### 2.3 SLA by Proposal

| Step | Max Duration | Timer Starts | Action on Expiry |
|------|-------------|-------------|------------------|
| Proposal visibility | 7 days | On creation | Auto-withdraw proposal |
| Demandeur response | 48h | On proposal sent | Reminder at 24h, expiry at 48h |
| Info request response | 24h | On info provided | Escalate to agent |

---

## 3. Double Consent Model

### 3.1 Double Consent Principle

LAWIM enforces a mandatory two-sided consent model before any relationship is established. The demandeur (C1) must consent first, then the holder (C2) must consent. Both consents are required; neither party can unilaterally create a relationship.

### 3.2 Consent C1 — Demandeur Consent

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `match_id` | UUID | Reference to the match |
| `party_id` | UUID | Demandeur user ID |
| `party_role` | Enum | `demandeur` |
| `consent_type` | Enum | `demandeur_consent` |
| `status` | Enum | `requested \| granted \| declined \| expired \| revoked` |
| `scope` | JSON | `{"purpose": "contact_holder", "proposal_id": "..."}` |
| `channel` | Enum | `whatsapp \| telegram \| web \| mobile \| api` |
| `response_time` | Int? | Seconds between request and response |
| `requested_at` | DateTime | When consent was requested |
| `responded_at` | DateTime? | When party responded |
| `decline_reason` | String? | Optional reason for decline |
| `expires_at` | DateTime | Consent validity deadline |
| `created_at` | DateTime | Record creation |

**Request Template:**
```
System to Demandeur:
"Souhaitez-vous que nous contactions le détenteur de [property] 
pour organiser une mise en relation ?
- ✅ Oui, contactez le détenteur
- ❌ Non, pas pour le moment
- ℹ️ Plus d'informations sur ce bien"
```

**Side Effects on Demandeur Consent:**

| Action | Effect |
|--------|--------|
| `granted` | Relationship transitions to `consent_holder_pending`, holder notification prepared |
| `declined` | Match marked refused, rematching triggered |
| `expired` | Match expired, demandeur notified |
| `revoked` | Relationship terminated if active |

### 3.3 Consent C2 — Holder Consent

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `match_id` | UUID | Reference to the match |
| `party_id` | UUID | Holder user ID |
| `party_role` | Enum | `holder` |
| `consent_type` | Enum | `holder_consent` |
| `status` | Enum | `requested \| granted \| declined \| expired \| revoked` |
| `scope` | JSON | `{"purpose": "accept_contact", "property_id": "..."}` |
| `channel` | Enum | `whatsapp \| telegram \| web \| mobile \| api` |
| `response` | Enum? | `accept \| refuse \| delay \| alternative \| unavailable` |
| `alternative_property_id` | UUID? | If holder proposed alternative property |
| `delay_duration` | Int? | Requested delay in days |
| `reminder_count` | Int | Number of reminders sent (0-3) |
| `last_reminder_at` | DateTime? | Last reminder timestamp |
| `silence_workflow_exhausted` | Boolean | Whether silence workflow completed |
| `requested_at` | DateTime | When consent was requested |
| `responded_at` | DateTime? | When holder responded |
| `decline_reason` | String? | Optional reason |
| `expires_at` | DateTime | Consent validity deadline |
| `created_at` | DateTime | Record creation |

**Request Template:**
```
System to Holder:
"Une personne intéressée par votre bien [ref] ([address]) 
souhaite vous rencontrer.

- ✅ Accepter la mise en relation
- ❌ Refuser
- ⏳ Plus tard (me rappeler dans X jours)
- 🔄 Proposer un autre bien
- 🚫 Déclarer le bien indisponible"
```

**Side Effects on Holder Consent:**

| Response | Effect | Next Action |
|----------|--------|-------------|
| `accept` | Consent granted, relationship activated | Notify both parties, lift anonymity |
| `refuse` | Consent declined, relationship closed | Notify demandeur, trigger rematching |
| `delay` | Timer set, status stays `requested` | Schedule reminder at requested date |
| `alternative` | Alternative property proposal created | Initiate new proposal on alternative |
| `unavailable` | Property marked unavailable | Notify demandeur, trigger rematching |

### 3.4 Double Consent Integrity Rules

| Rule | Description |
|------|-------------|
| **Ordering** | C1 (demandeur) MUST precede C2 (holder). System never contacts holder before demandeur consents. |
| **Independence** | C1 and C2 are independently revocable. Revoking C1 after C2 is granted terminates the relationship. |
| **Freshness** | C1 has a default validity of 90 days. If C1 expires before C2 is requested, C1 must be re-obtained. |
| **Scope match** | C2 scope must match or be compatible with C1 scope. A holder consent for a different property initiates a new proposal. |
| **No coercion** | Both parties are explicitly informed that consent is voluntary and revocable at any time. |
| **Audit trail** | Every consent event is immutably logged with full context. |

---

## 4. Relationship Entity

### 4.1 Core Relationship Attributes

The `Relationship` entity is established after double consent is obtained. It represents the active Mise en Relation between a demandeur and a holder for a specific property.

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `match_id` | UUID | Reference to originating match |
| `proposal_id` | UUID | Reference to the accepted proposal |
| `demandeur_id` | UUID | Demandeur user reference |
| `holder_id` | UUID | Holder user reference |
| `property_id` | UUID | Property reference |
| `demandeur_consent_id` | UUID | C1 consent record |
| `holder_consent_id` | UUID | C2 consent record |
| `status` | Enum | `proposed \| consent_demandeur_pending \| consent_demandeur_granted \| consent_holder_pending \| active \| follow_up \| expired \| revoked \| closed \| archived` |
| `introduction_id` | UUID? | Reference to introduction record |
| `shared_data_scope_id` | UUID? | Current data sharing scope |
| `anonymity_lifted` | Boolean | Whether identities are revealed |
| `anonymity_lifted_at` | DateTime? | When identities were revealed |
| `interlocutor` | Enum? | `proprietaire \| agent \| notaire \| autre` |
| `agent_id` | UUID? | Assigned agent reference |
| `visit_count` | Int | Number of visits completed |
| `negotiation_status` | Enum? | `not_started \| in_progress \| successful \| failed` |
| `transaction_id` | UUID? | Reference to resulting transaction |
| `health_score` | Int? | Computed relationship health (0-100) |
| `health_level` | Enum? | `excellent \| normal \| monitor \| critical` |
| `last_activity_at` | DateTime | Last party or system activity |
| `inactivity_alert_sent` | Boolean | Whether inactivity alert was sent |
| `follow_up_count` | Int | Number of follow-ups sent |
| `created_at` | DateTime | Relationship creation |
| `activated_at` | DateTime? | When double consent obtained |
| `closed_at` | DateTime? | When relationship closed |
| `expires_at` | DateTime | Relationship validity expiry |
| `version` | Int | Optimistic locking version |

### 4.2 Relationship State Machine

```
PROPOSED → C_DEMANDEUR_PENDING → C_DEMANDEUR_GRANTED → C_HOLDER_PENDING → ACTIVE
                                                                                ↓
                                                                          FOLLOW_UP
                                                                          ↓       ↓
                                                                     ACTIVE    CLOSED
                                                                        ↓
                                                                   EXPIRED / REVOKED / CLOSED → ARCHIVED
```

Full transition table is defined in `RELATIONSHIP_LIFECYCLE.md`.

### 4.3 SLA by Relationship State

| State | Max Duration | Timer Starts | Escalation |
|-------|-------------|-------------|------------|
| `PROPOSED` | 7 days | On proposition | Reminder J+3, close J+7 |
| `C_DEMANDEUR_PENDING` | 48h | On consent request | Reminder 24h, close 48h |
| `C_DEMANDEUR_GRANTED` | 24h | On demandeur consent | Auto-transition to holder contact |
| `C_HOLDER_PENDING` | Per property type | On holder contact | Silence workflow (§9.1) |
| `ACTIVE` | 90d inactivity | On last activity | Follow-up cadence (§10) |
| `FOLLOW_UP` | 7 days | On follow-up trigger | Escalation to LAWIM |
| `EXPIRED` | 90 days | On expiry | Auto-archive |
| `REVOKED` | 90 days | On revocation | Auto-archive |
| `CLOSED` | 90 days | On closure | Auto-archive |

---

## 5. Participant Roles in a Relationship

### 5.1 Core Roles

| Role | Code | Participant | Consent Required | Visibility |
|------|------|-------------|-----------------|------------|
| Demandeur | `demandeur` | Property seeker | C1 (demandeur_consent) | Identity masked until double consent |
| Holder | `holder` | Property owner | C2 (holder_consent) | Identity masked until double consent |
| Agent | `agent` | Managing agent | Agent opt-in | Visible to both parties after opt-in |
| LAWIM Collaborator | `lawim_collaborator` | Platform staff | N/A (admin) | Full visibility (admin) |

### 5.2 Extended Roles

| Role | Code | Context | Description |
|------|------|---------|-------------|
| Co-Demandeur | `co_demandeur` | Joint purchase | Additional property seeker (buyer/tenant) |
| Guarantor | `guarantor` | Rental | Financial guarantor for demandeur |
| Notaire | `notaire` | Transaction | Legal professional for deed |
| Professional | `professional` | Service | Inspector, estimator, photographer |

### 5.3 Role Permissions Within Relationship

| Action | Demandeur | Holder | Agent | LAWIM |
|--------|-----------|--------|-------|-------|
| View property details | ✅ | ✅ | ✅ | ✅ |
| View masked counterparty | ✅ (masked) | ✅ (masked) | ✅ | ✅ |
| View full counterparty identity | ✅ (post C2) | ✅ (post C1) | ✅ (post opt-in) | ✅ |
| Send message | ✅ | ✅ | ✅ (if assigned) | ✅ |
| Schedule visit | ✅ | ✅ | ✅ | ✅ |
| Revoke consent | ✅ | ✅ | ❌ | ❌ |
| Close relationship | ✅ | ✅ | ✅ (admin) | ✅ |
| Extend consent expiry | ❌ | ❌ | ❌ | ✅ |
| Access audit trail | Own only | Own only | Assigned | Full |
| Escalate to human | ✅ | ✅ | ✅ | N/A |

### 5.4 Agent Assignment

An agent can be assigned to a relationship at any point. Agent assignment requires:

1. Agent opt-in from the demandeur (see §4 of CONSENT_EXECUTION_CONTRACT.md)
2. Agent affirmation of availability and interest
3. Relationship owner (demandeur or holder) notification

| Assignment Source | Method | Consent Required |
|------------------|--------|-----------------|
| System routing (CRM) | Automatic zone-based | Agent opt-in |
| Demandeur request | Manual selection | None beyond opt-in |
| Holder assignment | Manual selection | Holder authorisation |
| Manual (LAWIM) | Admin override | Admin authorisation |

---

## 6. Introduction Tracking

### 6.1 Introduction Entity

Every relationship records how the two parties were introduced. This provides traceability for commission tracking, referral rewards, and marketing attribution.

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `relationship_id` | UUID | Reference to the relationship |
| `introduction_method` | Enum | `matching_engine \| referral \| agent_introduction \| direct_search \| manual` |
| `introducer_id` | UUID? | User who made the introduction |
| `introducer_role` | Enum? | `agent \| user \| lawim \| system` |
| `referral_code` | String? | Referral code used (if referral) |
| `referral_reward_claimed` | Boolean | Whether referral reward was claimed |
| `commission_eligible` | Boolean | Whether introducer is eligible for commission |
| `commission_amount` | Decimal? | Commission amount if applicable |
| `commission_paid` | Boolean | Whether commission was paid |
| `match_id` | UUID | Source match (if from matching engine) |
| `proposal_id` | UUID | Source proposal |
| `created_at` | DateTime | Introduction record creation |

### 6.2 Introduction Methods

| Method | Description | Introducer | Commission |
|--------|-------------|------------|------------|
| `matching_engine` | System matched demandeur to property | System | N/A |
| `referral` | Existing user referred the demandeur | Referring user | Eligible |
| `agent_introduction` | Agent introduced parties | Agent | Eligible |
| `direct_search` | Demandeur found property directly | Self | N/A |
| `manual` | LAWIM collaborator manually linked | LAWIM | N/A |

### 6.3 Referral Tracking Flow

```
1. Referrer shares referral link/code
2. Referee signs up with referral code
3. When referee creates a successful relationship:
   a. Introduction record created with method=referral
   b. Referral reward eligibility computed
   c. Reward credited upon transaction completion
4. Referral status tracked: pending → eligible → claimed → paid
```

---

## 7. Shared Data Scope Per Relationship

### 7.1 Data Visibility by Relationship Phase

| Phase | Demandeur Sees About Holder | Holder Sees About Demandeur |
|-------|---------------------------|----------------------------|
| Pre-consent (match/proposal) | Property details, city, price range, holder type | Nothing about demandeur |
| C1 granted (demandeur consented) | Same as pre-consent | Demandeur first name, property interest |
| C2 granted (holder consented) | Full holder identity (name, phone, email) | Full demandeur identity (name, phone, email) |
| Active relationship | Holder identity + property address | Demandeur identity |
| Visit phase | Holder identity + GPS coordinates | Demandeur identity + contact |
| Data sharing consent | Unlocked additional holder fields | Unlocked additional demandeur fields |

### 7.2 Shared Data Scope Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `relationship_id` | UUID | Relationship reference |
| `scope_level` | Enum | `basic_contact \| full_contact \| professional_contact \| temporary_access` |
| `fields_shared` | String[] | Array of field names shared |
| `granted_by_party` | UUID | Party who granted this sharing |
| `granted_at` | DateTime | When sharing was granted |
| `expires_at` | DateTime? | Sharing validity |
| `is_active` | Boolean | Whether sharing is active |
| `revoked_at` | DateTime? | When sharing was revoked |
| `revoke_reason` | String? | Reason for revocation |

### 7.3 Scope Levels

| Level | Fields Shared | Validity | Revocable |
|-------|--------------|----------|-----------|
| `basic_contact` | Phone number | Single relationship | Yes |
| `full_contact` | Phone + email + address | Single relationship | Yes |
| `professional_contact` | Phone + email + agency address | All relationships with same agent | Yes |
| `temporary_access` | Phone only | 7 days | Yes |

### 7.4 H0.5 Privacy Alignment

Per `PRIVACY_AND_SENSITIVE_FIELDS.md`, every field shared is classified by H0.5 privacy level:

| H0.5 Level | Consent Required Before Sharing | Allowed Scope |
|------------|-------------------------------|---------------|
| PUBLIC | Never | Always visible |
| PRIVATE | Relationship consent (C1/C2) | `basic_contact`, `full_contact` |
| SENSITIVE | Explicit data sharing consent | `full_contact` only |
| CONFIDENTIAL | Legal basis + NDA | Never through platform |

---

## 8. Consent Lifecycle

### 8.1 Single Consent Lifecycle

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

### 8.2 State Definitions

| State | Code | Description | Entered When | Can Transition To |
|-------|------|-------------|-------------|-------------------|
| `requested` | `REQUESTED` | Consent has been asked but not yet answered | System sends consent request | `granted`, `declined`, `expired` |
| `granted` | `GRANTED` | Party has explicitly consented | Party responds affirmatively | `revoked`, `expired` |
| `declined` | `DECLINED` | Party has explicitly refused | Party responds negatively | None (terminal) |
| `revoked` | `REVOKED` | Party has withdrawn consent | Party requests revocation | None (terminal) |
| `expired` | `EXPIRED` | Consent validity period elapsed | Timer expires | None (terminal) |

### 8.3 SLA by Consent Type

| Consent Type | Request → Grant SLA | Grant → Expiry | Reminder Cadence |
|-------------|--------------------|----------------|------------------|
| `demandeur_consent` | 48h | 90 days | 24h reminder, close at 48h |
| `holder_consent` | Per property type | 90 days | Silence workflow (3 reminders) |
| `agent_optin` | No SLA | At will | No reminders |
| `data_sharing` | No SLA | Per scope level | No reminders |

### 8.4 Consent Principles (Reaffirmed)

| Principle | Enforcement |
|-----------|-------------|
| **Explicit** | Consent must be active opt-in. Pre-checked boxes, implied consent, or opt-out are not permitted. |
| **Informed** | Each consent request MUST include: what is being consented to, who will receive the data/data access, how long consent is valid, and how to revoke. |
| **Specific** | Consent is scoped to a specific purpose (contact holder, accept contact, share coordinates). No blanket consent. |
| **Revocable** | Every consent record has a revocation path. Revocation is immediate and irreversible. |
| **Recorded** | Every consent event is immutably logged with cryptographic audit trail. |
| **Time-bound** | Every consent has an expiration. Auto-renewal requires explicit re-consent. |
| **Auditable** | Full lifecycle traceability: who requested, when, through which channel, what response, when response occurred, changes over time. |

---

## 9. Revocation Workflow

### 9.1 Revocation Trigger Points

| Source | Channel | Authentication | Notes |
|--------|---------|---------------|-------|
| User sends revocation keyword | WhatsApp/Telegram | Identity verification via OTP or session | Keywords: "JE REVOQUE", "REVOKE", "RETRACTE" |
| User clicks "Revoke consent" | Web/Mobile | Session authentication | Prominent in consent management UI |
| User calls support | Phone | Support agent verification | Support agent logs revocation on behalf |
| System detects consent expiry | System | N/A | Auto-revocation on SLA breach |

### 9.2 Revocation by Consent Type

| Consent Type | Immediate Effect | Party Notification | Data State |
|-------------|-----------------|-------------------|------------|
| `demandeur_consent` (C1) | Relationship terminated | Holder notified | Relationship archived |
| `holder_consent` (C2) | Relationship terminated | Demandeur notified | Relationship archived |
| `agent_optin` | Agent access revoked | Agent notified | Opt-in marked revoked |
| `data_sharing` | Coordinates re-masked | Requesting party notified | Sharing log updated |

### 9.3 Revocation State Machine

```
                    ┌──────────────┐
                    │   GRANTED    │
                    └──────┬───────┘
                           │ party revokes
                           ▼
                    ┌──────────────┐
                    │  REVOKED     │
                    └──────┬───────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
           ┌──────────────┐  ┌──────────────┐
           │  Terminate   │  │  Re-mask     │
           │ Relationship │  │  Data        │
           └──────────────┘  └──────────────┘
```

### 9.4 Revocation Timeline

| Phase | Time | Action |
|-------|------|--------|
| Immediate | T+0s | Consent status set to `revoked` |
| Side effects | T+1h | Relationship terminated, notifications sent, data re-masked |
| Dependent processes | T+24h | All dependent workflows terminated |
| Audit | T+0s | Revocation recorded with timestamp, actor, reason, evidence |

### 9.5 Irreversibility

> Consent revocation is irreversible. A new consent must be obtained for any future operation. The revocation record is immutable and retained for audit purposes.

### 9.6 Legal Hold Override

If the relationship has an active legal proceeding or mediation, revocation enters a `pending_review` state instead of immediate `revoked`:

| Condition | Behavior |
|-----------|----------|
| No legal hold | Immediate revocation |
| Active mediation | Pending review — LAWIM collaborator notified within 24h |
| Active dispute | Pending review — mediator decision within 72h |
| Legal injunction | Cannot revoke until injunction lifted |

---

## 10. Expiration Handling

### 10.1 Expiration Sources

| Source | Trigger | Subject |
|--------|---------|---------|
| Match expiry | `expires_at` reached | Match |
| Proposal expiry | 7 days from creation | Proposal |
| Demandeur consent SLA | 48h timer | Consent C1 |
| Demandeur consent validity | 90 days from grant | Consent C1 |
| Holder consent SLA | Per property type timer | Consent C2 |
| Holder consent validity | 90 days from grant | Consent C2 |
| Relationship inactivity | 90d without activity | Relationship |
| Data sharing scope | Per scope level | SharedDataScope |
| Proposal temporary | 7 days | Temp proposal |

### 10.2 Expiration Handling Table

| Subject | Pre-Expiry Warning | Action on Expiry | Recovery |
|---------|-------------------|-----------------|----------|
| Match | Warning at T-7d | Mark as expired, archive if no response | New match required |
| Proposal | Warning at T-24h | Auto-withdraw, notify demandeur | Re-propose |
| Consent C1 (SLA) | Reminder at T-24h | Close consent, mark match expired | Re-request consent |
| Consent C1 (validity) | Warning at T-7d | Auto-revoke | Re-request consent |
| Consent C2 (SLA) | 3 reminders during SLA period | Silence workflow: property "to confirm" | Re-request via fresh match |
| Consent C2 (validity) | Warning at T-7d | Auto-revoke | Re-request consent |
| Relationship | Yellow at T-14d, Orange at T-21d, Red at T-21d+ | Auto-close, archive | Reactivation (admin) |
| Data sharing | Warning at T-3d | Re-mask coordinates | Re-request sharing |

### 10.3 Consent Renewal

When a consent is approaching expiry (T-7d), the system MAY request renewal:

```
System: "Votre consentement pour [purpose] expire dans 7 jours.
         Souhaitez-vous le renouveler ?
         - ✅ Oui, renouveler pour 90 jours
         - ❌ Non, laisser expirer"
```

| Response | Action |
|----------|--------|
| Accept renewal | Consent validity extended 90 days, new expiry computed |
| Decline/No response | Consent expires at original expiry date |

### 10.4 Post-Expiry Cleanup

| Duration After Expiry | Action |
|-----------------------|--------|
| T+0 | Consent marked `expired`, side effects executed |
| T+90d | Relationship auto-archived |
| T+180d | Anonymization of personal references (GDPR) |

---

## 11. Idempotency Guarantees

### 11.1 Idempotency Key Definition

Every consent, relationship, and data-sharing operation is protected by an idempotency key to prevent duplicate processing.

### 11.2 Idempotency Keys by Operation

| Operation | Idempotency Key | Uniqueness Scope |
|-----------|----------------|------------------|
| Create consent request | `(match_id, party_id, consent_type)` | Per match-party-type triple |
| Grant consent | `(consent_id, party_id)` | Per consent record |
| Create relationship | `(match_id)` | One relationship per match |
| Create introduction | `(relationship_id)` | One introduction per relationship |
| Create shared data scope | `(relationship_id, granting_party_id)` | One active scope per party per relationship |
| Revoke consent | `(consent_id, revocation_request_id)` | Once per revocation request |
| Renew consent | `(consent_id, renewal_request_id)` | Once per renewal request |

### 11.3 Idempotency Enforcement

| Layer | Mechanism |
|-------|-----------|
| API gateway | Idempotency-Key header with 24h retention |
| Service layer | Database unique constraint on idempotency key |
| Database | Composite unique indexes on business keys |
| Event bus | Deduplication by event ID (event sourcing) |

### 11.4 Duplicate Prevention Rules

| Scenario | Prevention | Handling |
|----------|-----------|----------|
| Duplicate consent request (same match-party-type) | Unique index | Return existing consent request |
| Duplicate consent grant | State machine guard | Reject, return current status |
| Duplicate relationship creation | Unique index on match_id | Return existing relationship |
| Duplicate revocation | State machine guard | No-op, log attempt |
| Duplicate data sharing scope | Unique index on (relationship_id, party) | Return existing scope |
| Race condition (double response) | First response wins | Second response logged and ignored |

### 11.5 Idempotency Error Response

```json
{
  "error": "IDEMPOTENCY_CONFLICT",
  "message": "Operation already processed",
  "existing_record_id": "UUID",
  "existing_status": "granted",
  "idempotency_key": "match_123_demandeur_consent"
}
```

---

## 12. Audit Trail for All Consent Changes

### 12.1 Audit Event Catalog

Every consent operation produces an immutable audit event. Events are written to the `consent_events` append-only table.

| Event | Trigger | Key Data |
|-------|---------|----------|
| `consent.requested` | System sends consent request | `consent_id`, `party_id`, `consent_type`, `scope`, `channel`, `requested_at` |
| `consent.granted` | Party accepts | `consent_id`, `party_id`, `response_time_seconds`, `channel` |
| `consent.declined` | Party refuses | `consent_id`, `party_id`, `decline_reason` (optional) |
| `consent.revoked` | Party withdraws | `consent_id`, `party_id`, `revoke_reason`, `source` |
| `consent.expired` | Timer elapses | `consent_id`, `expiry_date`, `expiry_source` (SLA/validity) |
| `consent.renewed` | Party renews | `consent_id`, `new_expiry_date`, `renewal_channel` |
| `consent.sla_reminder_sent` | System sends reminder | `consent_id`, `reminder_number`, `channel` |
| `consent.silence_workflow_step` | Silence workflow progresses | `consent_id`, `step`, `step_number` |
| `consent.auto_closed` | System closes due to SLA | `consent_id`, `sla_exceeded`, `auto_action` |
| `consent.legal_hold_applied` | Legal proceedings started | `consent_id`, `hold_reason`, `authority` |
| `consent.legal_hold_removed` | Legal proceedings resolved | `consent_id`, `resolution` |
| `consent.human_handover` | Escalated to human agent | `consent_id`, `lawim_collaborator_id`, `reason` |
| `consent.human_resolved` | Human resolves consent | `consent_id`, `resolution`, `resolved_by` |

### 12.2 Relationship Audit Events

| Event | Trigger | Key Data |
|-------|---------|----------|
| `relationship.created` | Double consent obtained | `relationship_id`, `demandeur_id`, `holder_id`, `property_id` |
| `relationship.status_changed` | Any state transition | `relationship_id`, `old_status`, `new_status`, `transition_event` |
| `relationship.party_added` | Agent assigned | `relationship_id`, `party_id`, `role` |
| `relationship.party_removed` | Agent unassigned | `relationship_id`, `party_id`, `role` |
| `relationship.anonymity_lifted` | Identities revealed | `relationship_id`, `lifted_at` |
| `relationship.data_shared` | Data sharing scope created | `relationship_id`, `scope_level`, `fields_shared` |
| `relationship.data_shared_revoked` | Data sharing revoked | `relationship_id`, `scope_level` |
| `relationship.visit_scheduled` | Visit arranged | `relationship_id`, `visit_id`, `scheduled_at` |
| `relationship.negotiation_opened` | Negotiation started | `relationship_id`, `negotiation_id` |
| `relationship.closed` | Relationship ended | `relationship_id`, `final_state`, `reason` |
| `relationship.archived` | Archival | `relationship_id`, `previous_state` |
| `relationship.reactivated` | Admin reactivation | `relationship_id`, `admin_id`, `reason` |

### 12.3 Audit Record Structure

```json
{
  "audit_id": "UUID",
  "event_type": "consent.granted",
  "timestamp": "2026-07-15T10:30:00Z",
  "consent_id": "UUID",
  "relationship_id": "UUID?",
  "party_id": "UUID",
  "actor_id": "UUID",
  "actor_role": "demandeur",
  "old_status": "requested",
  "new_status": "granted",
  "scope": {
    "purpose": "contact_holder",
    "relationship_type": "buy",
    "proposal_id": "UUID"
  },
  "metadata": {
    "channel": "whatsapp",
    "response_time_seconds": 120,
    "ip_address": "string?",
    "user_agent": "string?",
    "session_id": "string?"
  },
  "state_snapshot": {
    "match_id": "UUID",
    "relationship_status": "consent_holder_pending",
    "demandeur_consent": "granted",
    "holder_consent": "requested",
    "anonymity": "masked"
  },
  "signature": "hash_of_previous_event + payload_hash"
}
```

### 12.4 Audit Storage Guarantees

| Guarantee | Mechanism |
|-----------|-----------|
| Append-only | No updates, deletes, or overwrites. Only new records. |
| Immutable | Cryptographic hash chain linking consecutive events. |
| Timestamped | All events have authoritative timestamp (NTP-synchronized). |
| Traceable | Every event includes `consent_id` and `relationship_id` for full traversal. |
| Retention | Audit records are NEVER deleted. |
| Queryable | Events indexed by consent_id, relationship_id, party_id, event_type, timestamp. |

---

## 13. Human Handover Workflow

### 13.1 Handover Trigger Conditions

Automated consent workflows may fail for multiple reasons. When failure is detected, the system escalates to a LAWIM human collaborator.

| Trigger | Condition | Urgency |
|---------|-----------|---------|
| Silence exhaustion | Holder silence workflow completed without response | High |
| Technical failure | Consent request undeliverable after 3 retries | Medium |
| Ambiguous response | Party response cannot be classified as yes/no | Medium |
| Dispute flagged | Party reports issue with consent process | High |
| Legal hold | Party invokes legal right or proceeding | Urgent |
| Fraud suspicion | Anti-fraud layers triggered during consent | Urgent |
| Consent race condition | Double response with conflicting answers | Low |
| Repeated expiry | Same consent expired 3+ times | Low |

### 13.2 Handover Process

```
                     ┌────────────────┐
                     │  Auto-Consent  │
                     │   Workflow     │
                     └───────┬────────┘
                             │ failure detected
                             ▼
                     ┌────────────────┐
                     │  Assessment    │
                     │  (System)      │
                     └───────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │  Retry     │ │  Escalate  │ │  Close     │
       │  (auto)    │ │  (human)   │ │  (no-op)   │
       └─────┬──────┘ └──────┬─────┘ └────────────┘
             │               │
             ▼               ▼
       ┌────────────┐ ┌────────────┐
       │Resolution  │ │  LAWIM     │
       │  or next   │ │  Dashboard │
       │  step      │ │  Ticket #  │
       └────────────┘ └──────┬─────┘
                             │
                             ▼
                     ┌────────────────┐
                     │  Human         │
                     │  Resolution    │
                     └───────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │  Consent   │ │  Contact   │ │  Close     │
       │  Manual    │ │  Parties   │ │  Ticket    │
       │  Record    │ │  Offline   │ │  No Res.   │
       └────────────┘ └────────────┘ └────────────┘
```

### 13.3 Handover Ticket

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `consent_id` | UUID | Reference to stuck consent |
| `relationship_id` | UUID? | Reference to relationship (if exists) |
| `trigger` | Enum | Trigger condition code |
| `trigger_detail` | String | Human-readable description |
| `urgency` | Enum | `low \| medium \| high \| urgent` |
| `status` | Enum | `open \| assigned \| in_progress \| resolved \| closed` |
| `assigned_to` | UUID? | LAWIM collaborator |
| `assigned_at` | DateTime? | Assignment timestamp |
| `resolution` | Enum? | `consent_recorded \| parties_contacted \| system_retried \| ticket_closed` |
| `resolution_note` | String? | Human resolution notes |
| `escalation_count` | Int | Number of times escalated |
| `created_at` | DateTime | Ticket creation |
| `resolved_at` | DateTime? | Resolution timestamp |

### 13.4 Human Resolution Actions

| Action | Description | System Integration |
|--------|-------------|-------------------|
| Record consent manually | Collaborator records party's verbal consent | Creates consent record, triggers side effects |
| Contact parties offline | Collaborator calls/texts to resolve confusion | Logs interaction, updates ticket |
| Force relationship close | Collaborator closes consent workflow | Terminates consent, triggers cleanup |
| Override SLA timeout | Collaborator extends SLA for valid reason | Resets consent SLA timer |
| Mark property confirmed | Collaborator manually confirms availability | Updates property status |
| Trigger rematch | Collaborator initiates rematch | Rematch engine triggered |
| Escalate to legal | Legal issue detected | Transfers to legal team |

### 13.5 Handover SLA

| Urgency | Assignment SLA | Resolution SLA |
|---------|---------------|----------------|
| Urgent | 15 min | 2h |
| High | 1h | 24h |
| Medium | 4h | 48h |
| Low | 24h | 72h |

### 13.6 Escalation Chain

If the assigned LAWIM collaborator cannot resolve within SLA:

```
Level 1: LAWIM collaborator (assigned)
  → Level 2: LAWIM manager (if unresolved at L1 SLA)
    → Level 3: Legal/Compliance team (if legal implications)
      → Level 4: Executive decision (if platform-wide impact)
```

### 13.7 Human Handover Audit

Every handover event is logged:

| Event | Data |
|-------|------|
| `consent.human_handover` | consent_id, trigger, urgency, ticket_id |
| `consent.human_assigned` | ticket_id, collaborator_id, assigned_at |
| `consent.human_resolved` | ticket_id, resolution, resolved_by, resolved_at |
| `consent.human_escalated` | ticket_id, level, reason |

---

## Appendix A: Verification Checklist

| Requirement | Status | Section |
|-------------|--------|---------|
| Double consent (C1 + C2) | ✅ | §3 |
| Sharing scope | ✅ | §7 |
| Masking/anonymity | ✅ | §7.1 |
| Revocation | ✅ | §9 |
| Expiration | ✅ | §10 |
| Idempotence | ✅ | §11 |
| Audit | ✅ | §12 |
| Human handover | ✅ | §13 |
| Match ↔ consent link | ✅ | §1 |
| Proposal workflow | ✅ | §2 |
| Relationship entity | ✅ | §4 |
| Participant roles | ✅ | §5 |
| Introduction tracking | ✅ | §6 |

## Appendix B: References

| Reference | File |
|-----------|------|
| Heritage Gold — Double Consent Rule | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §25 |
| Heritage Gold — Mise en Relation Lifecycle | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §5 |
| Heritage Gold — CRM Agent Opt-In | `docs/lawim_heritage_gold/CRM_MODEL.md` §11 |
| Consent Execution Contract | `docs/knowledge_execution/CONSENT_EXECUTION_CONTRACT.md` |
| Relationship Lifecycle | `docs/knowledge_execution/RELATIONSHIP_LIFECYCLE.md` |
| Relationship Execution Architecture | `docs/knowledge_execution/RELATIONSHIP_EXECUTION_ARCHITECTURE.md` |
| Data Sharing Policy | `docs/knowledge_execution/DATA_SHARING_POLICY.md` |
| H0.5 Privacy & Sensitive Fields | `docs/semantic_harmonization/PRIVACY_AND_SENSITIVE_FIELDS.md` |
| Search & Matching Extensions | `docs/domain_extension/SEARCH_MATCHING_EXTENSION_MODEL.md` |
| Workflow Extension Model | `docs/domain_extension/WORKFLOW_EXTENSION_MODEL.md` |
