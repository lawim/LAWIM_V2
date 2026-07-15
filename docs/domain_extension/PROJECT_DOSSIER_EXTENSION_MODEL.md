# PROJECT / DOSSIER EXTENSION MODEL

**Document ID:** LAWIM-H13-DOSSIER-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §5 (Dossier/Project Model), §6 (Matching Engine), §4 (Service Model)
**Source Crosswalks:** INTENT_TRANSACTION_CROSSWALK.md, required_extensions.json (workflows, qualification_engine, matching, nba)

---

## Table of Contents

1. [Conceptual Architecture](#1-conceptual-architecture)
2. [Entity: Project (Dossier-Enriched)](#2-entity-project-dossier-enriched)
3. [Entity: ProjectParticipant](#3-entity-projectparticipant)
4. [Entity: ProjectPropertyLink](#4-entity-projectpropertylink)
5. [Entity: ProjectServiceLink](#5-entity-projectservicelink)
6. [Entity: ProjectProfessionalLink](#6-entity-projectprofessionallink)
7. [Entity: ActiveRequest](#7-entity-activerequest)
8. [Double Consent Workflow](#8-double-consent-workflow)
9. [Holder Decision Chain](#9-holder-decision-chain)
10. [10-Step Qualification Order](#10-10-step-qualification-order)
11. [Rematching Logic](#11-rematching-logic)
12. [Participant Tracking](#12-participant-tracking)
13. [Health Score Calculation](#13-health-score-calculation)
14. [NBA Decision Engine Integration](#14-nba-decision-engine-integration)
15. [SLA Mapping per Dossier State](#15-sla-mapping-per-dossier-state)
16. [Complete Extension Mapping Table](#16-complete-extension-mapping-table)

---

## 1. Conceptual Architecture

The Project entity in LAWIM_V2 is enriched with full dossier semantics from Heritage Gold. A single user journey (Project) may manage multiple operational units (Dossiers), each tracking a distinct matching-consent-contact-transaction pipeline.

### 1.1 Core Concepts

| Concept | Entity | Description |
|---------|--------|-------------|
| **Project Goal** | `Project.project_goal` | The user-facing objective that the platform helps achieve |
| **Project Type** | `Project.project_type` | Enum classifying the nature of the project (`buy`, `rent`, `sell`, `invest`, `find`, `service`, `other`) |
| **Dossier** | `Project` (dossier-enriched) | Operational unit tracking a specific matching-consent-transaction pipeline |
| **Dossier Type** | `Project.dossier_type` | Sub-classification of the dossier within a project |
| **Dossier State** | `Project.dossier_state` | Current position in the 14-state dossier lifecycle |
| **Active Request** | `ActiveRequest` | The current pending action/request awaiting a response |
| **Participant** | `ProjectParticipant` | A user with a defined role in the project/dossier |
| **Health Score** | `Project.health_score` | Computed metric indicating dossier health (0-100) |

### 1.2 Entity Relationship Diagram

```
User (owner/creator)
  ├── Project (goal + type container)
  │     ├── Dossier (operational unit) [Project itself with dossier_state]
  │     │     ├── ActiveRequest (current pending action)
  │     │     ├── ProjectParticipant (owner, holder, demandeur, agent, professional)
  │     │     ├── ProjectPropertyLink (linked property with match details)
  │     │     ├── ProjectServiceLink (linked service orders)
  │     │     ├── ProjectProfessionalLink (linked professionals)
  │     │     ├── Match (scores for N properties)
  │     │     ├── Visit (scheduled visits)
  │     │     ├── Negotiation (offer exchange)
  │     │     └── Transaction (deal closing)
  │     └── Dossier 2..N (multi-dossier projects)
  │
  ├── Property (as owner)
  ├── Service (as provider/consumer)
  └── Professional (as verified professional)
```

### 1.3 Multi-Dossier Project Model

A single project goal may require multiple operational dossiers. Example: "I want to buy a house and find a notary" → Project with goal "buy + find professional" spawns two dossiers.

```
Project (id: P-001)
  goal: "Acheter maison + trouver notaire"
  type: multi
  │
  ├── Dossier 1 (id: D-001)
  │     type: buy
  │     state: matching
  │     owner: User-123
  │     linked_properties: [PR-456, PR-789]
  │
  └── Dossier 2 (id: D-002)
        type: find
        state: qualification
        owner: User-123
        linked_professionals: [PRO-001]
```

---

## 2. Entity: Project (Dossier-Enriched)

The Project entity retains its V2 identity but is enriched with all Heritage Gold dossier semantics. For multi-dossier projects, each dossier is represented as a sub-project linked via `parent_project_id`.

### 2.1 Key Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `id` | UUID | V2 | Primary identifier |
| `title` | String | V2 | Project title |
| `project_type` | Enum | V2 | `buy \| rent \| sell \| invest \| find \| service \| other \| multi` |
| `project_goal` | String | **ENRICH** | User-facing objective description (free text) |
| `status` | Enum | V2 | Retained for backward compatibility |
| `parent_project_id` | UUID? | **ENRICH** | Parent project (for multi-dossier hierarchy) |
| `is_multi_dossier` | Boolean | **ENRICH** | Whether project has multiple operational dossiers |
| `dossier_count` | Int | **ENRICH** | Number of active dossiers under this project |

### 2.2 Dossier-Specific Enriched Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `dossier_type` | Enum | **ENRICH** | `purchase \| rental \| sale \| investment \| professional_search \| service_request \| financing \| other` |
| `dossier_state` | Enum | **ENRICH** | `creation \| qualification \| matching \| presentation \| wait_demandeur \| wait_holder \| mise_en_relation \| visit \| negotiation \| agreement \| transaction \| closure \| archive` |
| `matching_status` | Enum | **ENRICH** | `not_started \| in_progress \| completed \| rematching \| failed` |
| `double_consent_status` | Enum | **ENRICH** | `not_started \| demandeur_interested \| holder_contacted \| holder_favorable \| consent_obtained \| refused \| expired` |
| `rematching_count` | Int | **ENRICH** | Number of rematching cycles for this dossier |
| `max_rematches` | Int | **ENRICH** | Maximum allowed rematches (default: 3) |
| `holder_id` | UUID? | **ENRICH** | Current property holder being negotiated with |
| `matched_property_id` | UUID? | **ENRICH** | Currently matched property |
| `decision_deadline` | DateTime | **ENRICH** | Deadline for current decision step |
| `qualification_step` | Int | **ENRICH** | Current step in 10-step qualification order (0-10) |
| `qualification_completed` | Boolean | **ENRICH** | Whether all 10 qualification steps are complete |
| `qualification_data` | JSON | **ENRICH** | Captured qualification answers keyed by step |

### 2.3 Channel & Communication Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `source_channel` | Enum | **ENRICH** | `whatsapp \| telegram \| dashboard \| api \| referral \| agent_assisted` |
| `channel_session_id` | String? | **ENRICH** | External channel session identifier |
| `language` | Enum | **ENRICH** | `fr \| en \| pid` — preferred communication language |
| `communication_preference` | Enum | **ENRICH** | `whatsapp \| telegram \| email \| sms \| dashboard` |

### 2.4 Owner & Participant Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `owner_id` | UUID | V2 | User who created/owns the project |
| `participant_count` | Int | **ENRICH** | Number of active participants |
| `participants` | Relation | **ENRICH** | Linked via ProjectParticipant entity |
| `primary_demandeur_id` | UUID? | **ENRICH** | Primary demandeur (buyer/tenant/seeker) |
| `primary_holder_id` | UUID? | **ENRICH** | Primary holder (seller/owner) |
| `assigned_agent_id` | UUID? | **ENRICH** | Agent assigned to manage this dossier |

### 2.5 Linked Entities

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `linked_properties` | Relation | **ENRICH** | N:M via ProjectPropertyLink |
| `linked_services` | Relation | **ENRICH** | N:M via ProjectServiceLink |
| `linked_professionals` | Relation | **ENRICH** | N:M via ProjectProfessionalLink |
| `active_request_id` | UUID? | **ENRICH** | Current active request (if any) |

### 2.6 Health & SLA Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `health_score` | Int | **ENRICH** | Computed dossier health score (0-100) |
| `health_score_components` | JSON | **ENRICH** | Breakdown: completeness, recency, responsiveness, progress, risk |
| `health_last_computed_at` | DateTime | **ENRICH** | When health score was last recalculated |
| `priority` | Enum | **ENRICH** | `p0 \| p1 \| p2 \| p3` — dossier priority level |
| `sla_state_deadline` | DateTime? | **ENRICH** | SLA deadline for current dossier state |
| `sla_breached` | Boolean | **ENRICH** | Whether current state SLA has been breached |
| `sla_breach_count` | Int | **ENRICH** | Total SLA breaches for this dossier |

### 2.7 NBA Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `nba_action` | String? | **ENRICH** | Current next best action recommendation |
| `nba_priority` | Int? | **ENRICH** | NBA priority level (1-9, 1=highest) |
| `nba_generated_at` | DateTime? | **ENRICH** | When NBA was last generated |
| `nba_context` | JSON? | **ENRICH** | Context data for the NBA recommendation |
| `follow_up_at` | DateTime? | **ENRICH** | Scheduled follow-up timestamp |
| `follow_up_action` | String? | **ENRICH** | Scheduled follow-up action |

### 2.8 Relationships Summary

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| User (owner) | N:1 | Project creator/owner |
| User (holder) | N:1 | Current property holder |
| User (demandeur) | N:1 | Primary demandeur |
| User (agent) | N:1 | Assigned agent |
| Project (parent) | N:1 | Parent project (multi-dossier) |
| Project (child) | 1:N | Child dossiers (multi-dossier) |
| Property | N:M | Via ProjectPropertyLink |
| Service | N:M | Via ProjectServiceLink |
| Professional | N:M | Via ProjectProfessionalLink |
| Match | 1:N | Match scores |
| Visit | 0:N | Scheduled visits |
| Negotiation | 0:1 | Negotiation record |
| Transaction | 0:1 | Completed transaction |
| Intent | 0:1 | Source intent detection |
| ActiveRequest | 0:1 | Current active request |
| ProjectParticipant | 1:N | Participants with roles |

---

## 3. Entity: ProjectParticipant

Tracks all users associated with a project/dossier and their specific roles.

### 3.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to Project |
| `user_id` | UUID | Reference to User |
| `role` | Enum | `owner \| demandeur \| holder \| agent \| notaire \| professional \| assistant \| observer` |
| `status` | Enum | `active \| pending \| removed \| declined` |
| `invited_at` | DateTime? | When user was invited to participate |
| `joined_at` | DateTime? | When user accepted/accepted role |
| `removed_at` | DateTime? | When user was removed |
| `removal_reason` | String? | Reason for removal |
| `permissions` | JSON[] | Role-specific permission overrides |
| `is_primary` | Boolean | Whether this participant is the primary for their role |
| `metadata` | JSON | Role-specific metadata |

### 3.2 Participant Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| `owner` | Project creator; full control | Read, Create, Edit, Approve, Remove participants |
| `demandeur` | Primary seeker (buyer/tenant) | Read own data, Edit own profile, Request actions |
| `holder` | Property holder (seller/owner) | Read dossier, Respond to requests, Approve contact |
| `agent` | Managing agent | Read, Edit, Propose matches, Schedule visits, Manage workflow |
| `notaire` | Notary (transaction phase) | Read transaction documents, Upload signed docs |
| `professional` | Service provider (expert, evaluator) | Read assigned scope, Upload deliverables |
| `assistant` | Agent assistant | Read, Edit limited fields, Send messages |
| `observer` | Read-only access | Read only |

### 3.3 Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | N:1 | Parent project |
| User | N:1 | Participant user |

---

## 4. Entity: ProjectPropertyLink

Links properties to a project/dossier with match context.

### 4.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to Project |
| `property_id` | UUID | Reference to Property |
| `match_score` | Float? | Match score (0-100) if computed |
| `compatibility_level` | Enum? | `excellent \| good \| average \| low` |
| `link_type` | Enum | `matched \| proposed \| interested \| visited \| negotiated \| transacted \| rejected \| archived` |
| `demandeur_decision` | Enum? | `pending \| interested \| not_interested` |
| `holder_decision` | Enum? | `pending \| favorable \| refused` |
| `linked_at` | DateTime | When property was linked |
| `unlinked_at` | DateTime? | When property was unlinked |
| `unlink_reason` | String? | Reason for unlinking |
| `rank` | Int | Display rank for this property link |

### 4.2 Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | N:1 | Parent project |
| Property | N:1 | Linked property |

---

## 5. Entity: ProjectServiceLink

Links service orders to a project/dossier.

### 5.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to Project |
| `service_order_id` | UUID | Reference to ServiceOrder |
| `service_code` | String | Service code (for quick reference) |
| `status` | Enum | `pending \| active \| fulfilled \| cancelled` |
| `linked_at` | DateTime | When service was linked |
| `fulfilled_at` | DateTime? | When service was fulfilled |

### 5.2 Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | N:1 | Parent project |
| ServiceOrder | N:1 | Linked service order |

---

## 6. Entity: ProjectProfessionalLink

Links professionals to a project/dossier.

### 6.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to Project |
| `professional_id` | UUID | Reference to User (professional) |
| `profession` | String | Professional role (notaire, geometre, architecte, etc.) |
| `status` | Enum | `suggested \| engaged \| active \| completed \| cancelled` |
| `engagement_scope` | String | Description of the professional's scope |
| `linked_at` | DateTime | When professional was linked |
| `completed_at` | DateTime? | When engagement completed |

### 6.2 Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | N:1 | Parent project |
| User (professional) | N:1 | Professional user |

---

## 7. Entity: ActiveRequest

Represents the current pending action/request in the dossier workflow. At any given time, a dossier has zero or one active request awaiting a response.

### 7.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to Project |
| `request_type` | Enum | `qualification_answer \| match_review \| consent_demandeur \| consent_holder \| holder_decision \| visit_confirmation \| visit_reschedule \| offer_response \| document_upload \| information_request \| payment_confirmation \| signature` |
| `requested_from_id` | UUID | User from whom the response is expected |
| `requested_by_id` | UUID? | User/system who initiated the request |
| `status` | Enum | `pending \| fulfilled \| declined \| expired \| cancelled` |
| `deadline` | DateTime | Response deadline |
| `reminder_count` | Int | Number of reminders sent |
| `last_reminder_at` | DateTime? | Last reminder timestamp |
| `response_data` | JSON? | Data provided in the response |
| `responded_at` | DateTime? | When the response was received |
| `created_at` | DateTime | When request was created |
| `context` | JSON | Request-specific context (property_id, offer_amount, etc.) |

### 7.2 Request Types

| Request Type | Expected From | When Created | Resolution |
|-------------|---------------|-------------|------------|
| `qualification_answer` | Demandeur | During qualification | Answer recorded → next step |
| `match_review` | Demandeur | After matching | Interested / Not interested |
| `consent_demandeur` | Demandeur | Match proposed | Consent given / Refused |
| `consent_holder` | Holder | Demandeur interested | Favorable / Refused |
| `holder_decision` | Holder | During negotiation | Accept / Counter / Reject |
| `visit_confirmation` | Holder | Visit requested | Confirm / Reschedule / Cancel |
| `offer_response` | Counter-party | Offer made | Accept / Counter / Reject |
| `document_upload` | Any participant | Document required | Document uploaded |
| `signature` | Both parties | Transaction phase | Signed / Refused |

### 7.3 Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | 1:1 | Parent dossier |
| User (requested_from) | N:1 | Expected responder |
| User (requested_by) | N:1 | Request initiator |

---

## 8. Double Consent Workflow

Both parties (demandeur and holder) must explicitly consent before contact information is exchanged. This is a legal and privacy requirement.

### 8.1 State Machine

```
Matching Complete
    → Demandeur Proposed (top matches shown)
        → Demandeur Interested (consent 1/2)
            → Holder Contacted (demandeur profile shared)
                → Holder Favorable (consent 2/2)
                    → Double Consent Obtained
                        → Contact Information Revealed
                        → Mise en Relation Established
                → Holder Refuses
                    → Rematching Triggered
                → Holder Silence (72h)
                    → Reminder 1 (24h)
                    → Reminder 2 (48h)
                    → Last Reminder (72h)
                    → Property Flagged "to confirm"
                    → Rematching Triggered
            → Demandeur Not Interested
                → Rematching Triggered
        → Demandeur Silence (72h)
            → Reminder 1 (24h)
            → Reminder 2 (48h)
            → Last Reminder (72h)
            → Dossier Paused
```

### 8.2 State Definitions

| State | Description | Entry Condition | Max Duration | Exit |
|-------|-------------|----------------|-------------|------|
| `not_started` | No consent flow initiated | Match complete, top 10 proposed | — | Demandeur expresses interest |
| `demandeur_interested` | Demandeur has consented (1/2) | Demandeur clicks "interested" | 72h | Demandeur interest confirmed |
| `holder_contacted` | Holder notified of interested demandeur | Demandeur consent recorded | 72h | Holder responds |
| `holder_favorable` | Holder has consented (2/2) | Holder clicks "favorable" | — | Consent obtained |
| `consent_obtained` | Both parties consented | Holder favorable | — | Contact revealed |
| `refused` | Either party refused | Holder refuses / Demandeur not interested | — | Rematching |
| `expired` | Consent deadline passed | No response within 72h | — | Rematching or pause |

### 8.3 Consent Entity Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `consent_id` | UUID | Consent record identifier |
| `project_id` | UUID | Reference to Project |
| `demandeur_id` | UUID | Demandeur user |
| `holder_id` | UUID | Holder user |
| `property_id` | UUID | Property under consent |
| `demandeur_consented_at` | DateTime? | When demandeur gave consent |
| `demandeur_consent_method` | Enum | `click \| message \| verbal_confirmed` |
| `holder_consented_at` | DateTime? | When holder gave consent |
| `holder_consent_method` | Enum | `click \| message \| verbal_confirmed` |
| `consent_obtained_at` | DateTime? | When both consents were obtained |
| `contact_revealed_at` | DateTime? | When contact was revealed to both parties |
| `expires_at` | DateTime? | Consent expiry |
| `status` | Enum | Current consent status |

### 8.4 Consent Expiry and Renewal

| Scenario | Action |
|----------|--------|
| Consent obtained but no action for 30 days | Consent expires; re-consent required |
| Holder revokes consent | Consent revoked; demandeur notified; rematch |
| Demandeur revokes consent | Consent revoked; property delisted from dossier |
| Consent expired during silence | New consent flow required with same or different property |

---

## 9. Holder Decision Chain

Represents the sequential decision-making process involving property holders during matching and negotiation.

### 9.1 Decision Chain Flow

```
Property Match Proposed
    → Holder Availability Check
        → Holder Contact Preference (phone, whatsapp, telegram)
        → Holder Response to Demandeur Interest
            → Favorable → Proceed to Mise en Relation
            → Not Favorable (reason collected)
                → Price disagreement
                → Timeline mismatch
                → Already negotiating with another
                → Property no longer available
                → Other
            → Conditional (e.g., "only if price >= X")
                → Counter condition communicated to demandeur
                → Demandeur accepts condition → proceed
                → Demandeur declines → rematch
        → Holder Silence
            → Escalation Chain (see 9.3)
```

### 9.2 Holder Decision States

| State | Description | Duration | Next |
|-------|-------------|----------|------|
| `pending` | Holder has not yet responded | 0-72h | responded / silence |
| `favorable` | Holder agrees to mise en relation | — | proceed to double consent |
| `refused` | Holder explicitly refuses | — | collect reason → rematch |
| `conditional` | Holder accepts with conditions | 48h for demandeur response | condition_met / condition_failed |
| `condition_met` | Demandeur accepts conditions | — | proceed to mise en relation |
| `condition_failed` | Demandeur declines conditions | — | rematch |
| `silence` | No response within deadline | 72h total | escalation chain |

### 9.3 Holder Silence Escalation Chain

| Tier | Time | Action |
|------|------|--------|
| 1 | 24h | First reminder: "A demandeur is interested in your property" |
| 2 | 48h | Second reminder: "You have an interested party waiting" |
| 3 | 72h | Final reminder: "Without response, property will be deprioritized" |
| 4 | 72h+ | Property flagged "to_confirm"; rematching triggered; admin notified |

### 9.4 Holder Decision Record

| Attribute | Type | Description |
|-----------|------|-------------|
| `decision_id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to Project |
| `holder_id` | UUID | Holder user |
| `property_id` | UUID | Property under decision |
| `decision` | Enum | `pending \| favorable \| refused \| conditional \| silence` |
| `refusal_reason` | Enum? | Reason if refused |
| `refusal_detail` | String? | Free text explanation |
| `condition_type` | Enum? | `price \| timeline \| terms \| other` |
| `condition_value` | JSON? | Condition parameters |
| `decided_at` | DateTime? | When decision was made |
| `responded_via` | Enum? | `whatsapp \| telegram \| dashboard \| phone` |
| `escalation_tier` | Int | Current escalation tier (0-4) |

---

## 10. 10-Step Qualification Order

Progressive qualification collects user criteria in a structured 10-step order. Each step corresponds to a question or set of questions presented to the demandeur.

### 10.1 Step Definitions

| Step | Name | Question | Required | Data Captured |
|------|------|----------|----------|---------------|
| 0 | — | (Not started) | — | — |
| 1 | Intention | "Que souhaitez-vous faire?" | Yes | `intent`: buy, rent, sell, invest, find, service |
| 2 | Type | "Quel type de bien cherchez-vous?" | Yes | `property_type`: apartment, house, land, commercial, etc. |
| 3 | Ville | "Dans quelle ville?" | Yes | `city`: gazetteer-validated city |
| 4 | Quartier | "Quel quartier préférez-vous?" | No | `neighborhood`: optional, if specified |
| 5 | Budget | "Quel est votre budget?" | Yes | `budget_min`, `budget_max`: price range |
| 6 | Délai | "Quel est votre horizon temporel?" | Yes | `timeline`: immediate, 1-3 months, 3-6 months, 6-12 months, 12+ months |
| 7 | Critères | "Quels critères spécifiques?" | No | `criteria`: bedrooms, surface, floor, parking, etc. (multi-select) |
| 8 | Préférences | "Avez-vous des préférences?" | No | `preferences`: furnished, pet_friendly, accessibility, etc. |
| 9 | Confirmation | "Confirmez-vous ces informations?" | Yes | `confirmed`: boolean — summary review |
| 10 | Escalade | "Souhaitez-vous être assisté par un agent?" | No | `escalate_to_agent`: boolean — if incomplete or user opts in |

### 10.2 Per-Step SLA

| Step | Max Duration | Reminder | Escalation |
|------|-------------|----------|------------|
| 1-4 | 7 days total | 48h, 96h | After 7d: pause dossier |
| 5-8 | 7 days total | 48h, 96h | After 7d: suggest agent assistance |
| 9 | 24h | 12h | After 24h: auto-confirm with current data |
| 10 | — | — | If yes: route to available agent |

### 10.3 Step Progression Rules

| Rule | Description |
|------|-------------|
| Required steps | 1, 2, 3, 5, 6, 9 must be completed before proceeding |
| Optional steps | 4, 7, 8 may be skipped |
| Skip logic | Steps may be auto-skipped based on intent/type (e.g., sell intent skips step 2) |
| Back-navigation | User may go back to any previous step to modify answers |
| Re-qualification | If no matches found after step 9, user may re-enter qualification (step 5 reset) |
| Channel adaptation | WhatsApp/Telegram shows 1 question per message; Dashboard shows grouped |

### 10.4 Qualification Data Storage

Captured qualification data is stored as JSON on the Project:

```json
{
  "step_1_intention": { "intent": "buy", "detected_via": "explicit" },
  "step_2_type": { "property_type": "apartment", "property_subtype": "T3" },
  "step_3_ville": { "city": "Yaoundé", "gazetteer_match": true },
  "step_4_quartier": { "neighborhood": "Bastos", "optional": true },
  "step_5_budget": { "budget_min": 30000000, "budget_max": 50000000, "currency": "XAF" },
  "step_6_delai": { "timeline": "3-6_months", "urgency": "normal" },
  "step_7_criteres": { "bedrooms": 3, "surface_min": 80, "parking": true },
  "step_8_preferences": { "furnished": false, "pet_friendly": true },
  "step_9_confirmation": { "confirmed": true, "confirmed_at": "2026-07-15T10:30:00Z" },
  "step_10_escalade": { "escalate_to_agent": false }
}
```

---

## 11. Rematching Logic

When a match fails (refusal, silence, expired consent, failed negotiation), the rematching engine is triggered to find alternative properties or professionals.

### 11.1 Rematching Triggers

| Trigger | Source | Action |
|---------|--------|--------|
| Demandeur refuses match | User action | Exclude property, recalculate, propose next best |
| Holder refuses contact | Holder action | Exclude property, recalculate, propose next best |
| Double consent expires | System (72h timeout) | Flag holder as slow, recalculate, propose next best |
| Visit fails (no-show) | System | Offer rematch with same property (re-schedule) or new |
| Negotiation fails | System | Offer rematch with new property |
| Match expires (30d inactivity) | System | Recalculate scores, re-propose if still valid |
| New property listed | System | Evaluate against all active dossiers |
| Dossier updated | System | Recalculate all matches for this dossier |
| Holder silence escalation | System (72h) | Property flagged to_confirm, rematch triggered |
| Holder marks property unavailable | Holder action | Property excluded, rematch triggered |

### 11.2 Rematching Counters

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `rematching_count` | Int | 0 | Current rematch cycle number |
| `max_rematches` | Int | 3 | Maximum rematch cycles before escalation |
| `rematches_remaining` | Int | 3 | Computed: max_rematches - rematching_count |
| `rematch_history` | JSON[] | [] | Array of rematch records {trigger, excluded_property_id, new_property_id, timestamp} |

### 11.3 Rematch Exclusion Rules

| Rule | Description |
|------|-------------|
| Exclude refused property | Property where holder refused is excluded for 30 days |
| Exclude visited & failed | Property where visit failed or negotiation failed — excluded for 14 days |
| Exclude expired consent | Property where consent expired — excluded for 7 days |
| Down-rank slow holders | Properties whose holders triggered silence escalation get -20 score penalty |
| Progressive expansion | Each rematch expands search radius: same city → same region → neighboring regions |
| Preference relaxation | Each rematch relaxes non-essential criteria by one level |

### 11.4 Rematch Escalation

| Rematch # | Action |
|-----------|--------|
| 1 | Propose next best match (same criteria) |
| 2 | Expand geographic radius, relax secondary criteria |
| 3 | Maximum rematches reached — escalate to agent for manual intervention |
| 3+ | Dossier flagged for agent review; health score set to critical |

### 11.5 Progressive Search Expansion

| Level | Radius | Criteria Relaxation |
|-------|--------|-------------------|
| Initial | Exact city + neighborhood | Full criteria set |
| Rematch 1 | Same city, any neighborhood | Budget ±10%, surface ±15% |
| Rematch 2 | Same region | Budget ±20%, surface ±25%, type expanded |
| Rematch 3 | Any region | Budget ±30%, criteria relaxed to minimum |
| Agent escalation | Agent-defined | Agent defines new search parameters |

---

## 12. Participant Tracking

Each dossier tracks all participants with their roles, status, and engagement history.

### 12.1 Participant Lifecycle

```
Invited → Pending → Active → Removed
                         → Left (voluntary)
                         → Declined
```

### 12.2 Participant Engagement Metrics

| Metric | Tracking | Computation |
|--------|----------|-------------|
| `response_time_avg` | Average time to respond to requests | SUM(response_time) / response_count |
| `response_rate` | Percentage of requests responded to | responded_count / total_requests × 100 |
| `message_count` | Total messages sent | Count of messages in project context |
| `last_active_at` | Last interaction timestamp | Max(timestamps of all participant actions) |
| `engagement_score` | Composite engagement metric | Weighted: response_rate × 0.4 + response_time_score × 0.3 + message_count_score × 0.3 |

### 12.3 Participant History Log

| Attribute | Type | Description |
|-----------|------|-------------|
| `log_id` | UUID | Entry identifier |
| `participant_id` | UUID | Reference to ProjectParticipant |
| `action` | Enum | `invited \| joined \| responded \| messaged \| uploaded_doc \| changed_role \| removed \| left` |
| `performed_at` | DateTime | When action occurred |
| `context` | JSON? | Action context data |
| `performed_by_id` | UUID? | User who performed the action (if different from participant) |

---

## 13. Health Score Calculation

The dossier health score provides a single metric (0-100) indicating how healthy/viable a dossier is. It is composed of five weighted dimensions.

### 13.1 Score Dimensions

| Dimension | Weight | Description | Calculation |
|-----------|--------|-------------|-------------|
| **Completeness** | 0.25 | How complete is the qualification data | completed_steps / total_required_steps × 100 |
| **Recency** | 0.20 | How recent was the last activity | days_since_last_activity mapped to score curve |
| **Responsiveness** | 0.20 | How responsive are participants | participant_response_rate × 100 |
| **Progress** | 0.20 | How far along in the dossier lifecycle | current_state_progress / total_states × 100 |
| **Risk** | 0.15 | Risk factors (SLA breaches, rematches, silence) | 100 - weighted_risk_penalties |

### 13.2 Score Formula

```
health_score = (
    completeness_score × 0.25 +
    recency_score × 0.20 +
    responsiveness_score × 0.20 +
    progress_score × 0.20 +
    risk_score × 0.15
)
```

Where each component score is 0-100 and the result is clamped to 0-100.

### 13.3 Component Calculations

#### Completeness Score

| Criteria | Points |
|----------|--------|
| Step 1 (intention) completed | +15 |
| Step 2 (type) completed | +15 |
| Step 3 (city) completed | +15 |
| Step 5 (budget) completed | +15 |
| Step 6 (timeline) completed | +15 |
| Step 9 (confirmation) completed | +10 |
| All optional steps completed | +15 |
| **Maximum** | **100** |

#### Recency Score

| Days Since Last Activity | Score |
|--------------------------|-------|
| < 1 day | 100 |
| 1-3 days | 80 |
| 4-7 days | 60 |
| 8-14 days | 40 |
| 15-30 days | 20 |
| 31-60 days | 10 |
| > 60 days | 0 |

#### Responsiveness Score

| Average Response Rate | Score |
|----------------------|-------|
| > 90% | 100 |
| 75-90% | 80 |
| 50-74% | 60 |
| 25-49% | 40 |
| 10-24% | 20 |
| < 10% or no data | 0 |

#### Progress Score

| Dossier State | Progress Score |
|--------------|---------------|
| creation | 0 |
| qualification | 10 |
| matching | 20 |
| presentation | 30 |
| wait_demandeur | 35 |
| wait_holder | 40 |
| mise_en_relation | 50 |
| visit | 60 |
| negotiation | 70 |
| agreement | 80 |
| transaction | 90 |
| closure / archive | 100 |

#### Risk Score

| Risk Factor | Penalty |
|-------------|---------|
| Per SLA breach | -15 |
| Per rematch cycle | -10 |
| Holder silence event | -10 |
| Demandeur silence event | -10 |
| Visit no-show (any party) | -15 |
| Failed negotiation | -20 |
| Pending > 30 days with no progress | -25 |
| **Base** | **100** |

### 13.4 Health Score Interpretation

| Score Range | Status | Color | Action |
|-------------|--------|-------|--------|
| 80-100 | Healthy | Green | No action needed; monitor normally |
| 60-79 | Attention | Yellow | Review; consider NBA suggestions |
| 40-59 | Warning | Orange | Agent intervention recommended |
| 20-39 | Critical | Red | Escalate to agent/admin; immediate action required |
| 0-19 | Stalled | Dark Red | Dossier at risk of auto-archive; admin review |

### 13.5 Health Score Recalculation Triggers

| Trigger | Timing |
|---------|--------|
| State transition | Immediate |
| Participant action (response, message) | Immediate |
| SLA breach detected | Immediate |
| Daily cron | Every 24h for all active dossiers |
| Manual recalc | On demand via admin dashboard |

---

## 14. NBA Decision Engine Integration

The Next Best Action engine recommends the optimal action for each dossier based on its current state, health score, and context.

### 14.1 NBA per Dossier State

| Dossier State | Default NBA | Condition | Alternative NBA |
|--------------|-------------|-----------|-----------------|
| `creation` | Start qualification | — | — |
| `qualification` | Ask next question | Step incomplete | Escalate to agent (step 10) |
| `matching` | Launch/refresh search | Matches < 3 | Expand criteria |
| `presentation` | Propose top match | — | Show comparison view |
| `wait_demandeur` | Send reminder | Silence > 24h | Propose alternative match |
| `wait_holder` | Send holder reminder | Silence > 24h | Escalate to agent |
| `mise_en_relation` | Schedule visit | Both consented | Send contact info |
| `visit` | Confirm visit | Visit scheduled | Send reminders |
| `negotiation` | Make offer | — | Send counter-offer |
| `agreement` | Create transaction | Agreement reached | — |
| `transaction` | Request documents | — | Process payment |
| `closure` | Collect feedback | — | Schedule follow-up |
| `archive` | — | — | — |

### 14.2 NBA Priority Levels

| Level | Description | Response SLA |
|-------|-------------|-------------|
| 1 | Critical — immediate action | < 15 min |
| 2 | Urgent — requires prompt action | < 1 hour |
| 3 | High — important but not blocking | < 4 hours |
| 4 | Medium — standard priority | < 24 hours |
| 5 | Low — can be deferred | < 48 hours |
| 6 | Background — no immediate action | < 7 days |
| 7 | Informational — notification only | — |
| 8 | Monitoring — observe only | — |
| 9 | Idle — no action needed | — |

### 14.3 NBA Context Fields

| Field | Type | Description |
|-------|------|-------------|
| `dossier_state` | Enum | Current state |
| `health_score` | Int | Current health score |
| `health_status` | Enum | healthy / attention / warning / critical / stalled |
| `last_activity_at` | DateTime | Last activity timestamp |
| `days_in_current_state` | Int | Days spent in current state |
| `pending_request_type` | Enum? | Type of active request if any |
| `pending_request_deadline` | DateTime? | Deadline of active request |
| `rematch_count` | Int | Number of rematches |
| `sla_breach_count` | Int | Number of SLA breaches |
| `participant_count` | Int | Active participants |
| `response_rate` | Float | Overall response rate |

---

## 15. SLA Mapping per Dossier State

### 15.1 State SLA Thresholds

| Dossier State | Max Duration | SLA Priority | Breach Action |
|--------------|-------------|-------------|---------------|
| `creation` | 24h | P3 | Reminder to complete qualification |
| `qualification` | 7 days | P2 | Escalate to agent for assistance |
| `matching` | 48h (auto) | P1 | Refresh matching engine |
| `presentation` | 7 days | P2 | Reminder to review matches |
| `wait_demandeur` | 72h | P1 | Reminder cycle → pause dossier |
| `wait_holder` | 72h | P1 | Holder silence escalation chain |
| `mise_en_relation` | 7 days | P2 | Reminder to schedule visit |
| `visit` | 14 days | P2 | Offer reschedule or rematch |
| `negotiation` | 30 days | P1 | Negotiation silence escalation |
| `agreement` | 7 days | P1 | Reminder to create transaction |
| `transaction` | 90 days | P1 | Transaction SLA per state |
| `closure` | 7 days | P3 | Auto-archive if no feedback |

### 15.2 SLA Tier Escalation

| Tier | Trigger | Action |
|------|---------|--------|
| 1 | 50% of max duration | Soft reminder to responsible party |
| 2 | 80% of max duration | Firm reminder + agent notification |
| 3 | 100% of max duration (breach) | Escalate to agent; NBA recalculated; dossier flagged |
| 4 | 150% of max duration | Escalate to admin; health score penalty applied |

---

## 16. Complete Extension Mapping Table

### 16.1 Dossier/Project Extensions

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-DOS-001 | Multi-dossier project model | Project | `parent_project_id`, `is_multi_dossier`, `dossier_count` | P2 |
| EXT-DOS-002 | 14-state dossier lifecycle | Project | `dossier_state` (14 states) | P1 |
| EXT-DOS-003 | Dossier type classification | Project | `dossier_type` (8 types) | P2 |
| EXT-DOS-004 | Project goal (free-text) | Project | `project_goal` | P2 |
| EXT-DOS-005 | Double consent workflow | Project + Consent | `double_consent_status`, consent entity | P1 |
| EXT-DOS-006 | Holder decision chain | Project + HolderDecision | Decision states, silence escalation | P1 |
| EXT-DOS-007 | 10-step qualification order | Project | `qualification_step`, `qualification_data` | P1 |
| EXT-DOS-008 | Rematching engine | Project + Match | `rematching_count`, `max_rematches`, rematch triggers | P1 |
| EXT-DOS-009 | Participant tracking | ProjectParticipant (new) | Roles, status, engagement metrics | P2 |
| EXT-DOS-010 | Active request management | ActiveRequest (new) | Request types, deadlines, reminders | P2 |
| EXT-DOS-011 | Linked properties registry | ProjectPropertyLink (new) | Match context, decisions per property | P2 |
| EXT-DOS-012 | Linked services registry | ProjectServiceLink (new) | Service orders linked to dossier | P2 |
| EXT-DOS-013 | Linked professionals registry | ProjectProfessionalLink (new) | Professional engagement tracking | P3 |
| EXT-DOS-014 | Source channel tracking | Project | `source_channel`, `language`, `communication_preference` | P2 |
| EXT-DOS-015 | Dossier health score | Project | `health_score`, `health_score_components` | P2 |
| EXT-DOS-016 | Dossier priority & SLA | Project | `priority`, `sla_state_deadline`, `sla_breached` | P1 |
| EXT-DOS-017 | NBA decision engine integration | Project | `nba_action`, `nba_priority`, `follow_up_at` | P2 |
| EXT-DOS-018 | Progressive search expansion | Match + Project | Expansion levels, criteria relaxation rules | P2 |
| EXT-DOS-019 | Consent expiry & renewal | Consent | `expires_at`, renewal workflow | P2 |
| EXT-DOS-020 | Holder silence escalation | HolderDecision | 4-tier escalation with reminders | P1 |

### 16.2 Entity Summary

| Entity | Type | Description |
|--------|------|-------------|
| Project | ENRICH | Core entity with all dossier semantics added as enriched fields |
| ProjectParticipant | NEW | Participant with role, status, and engagement tracking |
| ProjectPropertyLink | NEW | N:M link between Project and Property with match context |
| ProjectServiceLink | NEW | N:M link between Project and ServiceOrder |
| ProjectProfessionalLink | NEW | N:M link between Project and Professional User |
| ActiveRequest | NEW | Current pending action/request in dossier workflow |
| Consent | NEW | Double consent record with timestamps and methods |
| HolderDecision | NEW | Holder decision record with refusal reasons and conditions |

---

*End of PROJECT_DOSSIER_EXTENSION_MODEL.md — 16 sections, 20 extensions, 7 entities (1 enriched + 6 new), full dossier semantics defined.*
