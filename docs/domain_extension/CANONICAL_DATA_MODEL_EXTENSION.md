# Canonical Data Model Extension — LAWIM_V2

**Document ID:** LAWIM-DM-EXT-V1  
**Status:** CANONICAL  
**Date:** 2026-07-15  
**Version:** 1.0  
**Base Document:** `04_CANONICAL_DATA_MODEL.md`  
**Extension Source:** `REQUIRED_EXTENSIONS.md` · 175 Heritage Gold concepts

---

## 1. Purpose

This document defines the complete conceptual data model extension for LAWIM_V2. It covers **26 entities** — 6 enriched from the existing canonical model and 20 new entities. Each entity specification includes fields, value objects, relations, indexes, uniqueness constraints, lifecycle, privacy, audit, and migration source.

---

## 2. Entity Inventory

| # | Entity | Domain | Status | Enrich/New |
|---|--------|--------|--------|-----------|
| 1 | User | Identity | ENRICHED | ENRICH |
| 2 | Organization | Organizations | ENRICHED | ENRICH |
| 3 | OrganizationMember | Organizations | ENRICHED | ENRICH |
| 4 | Property | Properties | ENRICHED | ENRICH |
| 5 | Project | Projects | ENRICHED | ENRICH |
| 6 | Event | Audit & Observability | ENRICHED | ENRICH |
| 7 | Intent | Intent Detection | NEW | NEW |
| 8 | Match | Matching | NEW | NEW |
| 9 | Visit | Visits | NEW | NEW |
| 10 | Transaction | Transactions | NEW | NEW |
| 11 | Service | Services | NEW | NEW |
| 12 | ServiceOrder | Services | NEW | NEW |
| 13 | Payment | Financial Core | NEW | NEW |
| 14 | AgentCredit | Financial Core | NEW | NEW |
| 15 | LeadPurchase | CRM | NEW | NEW |
| 16 | Lead | CRM | NEW | NEW |
| 17 | Document | Documents & GED | NEW | NEW |
| 18 | ApprovalWorkflow | Permissions | NEW | NEW |
| 19 | Mediation | Dispute Resolution | NEW | NEW |
| 20 | Incident | Incident Management | NEW | NEW |
| 21 | AgentInvitation | Onboarding | NEW | NEW |
| 22 | IdentityResolution | Identity | NEW | NEW |
| 23 | ProfessionalProfile | Professionals | NEW | NEW |
| 24 | FinancingRequest | Financing | NEW | NEW |
| 25 | GeographicUnit | Geography | NEW | NEW |
| 26 | Consent | Relationship | ENRICHED | ENRICH |

---

## 3. Entity Specifications

---

### 3.1 User (ENRICH)

| Attribute | Value |
|-----------|-------|
| **entity_name** | User |
| **domain** | Identity |
| **purpose** | Represents a platform user (client, agent, admin) with enriched trust, verification, role, and onboarding semantics |
| **existing_or_new** | ENRICH — extends existing `User` model in Prisma schema |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | Heritage Gold | Primary key |
| email | String | Heritage Gold | Unique email |
| username | String? | Heritage Gold | Unique username |
| full_name | String | Heritage Gold | Display name |
| phone_e164 | String? | Heritage Gold | Phone in E.164 format |
| preferred_language | String | Heritage Gold | Default "fr" |
| role | String | Heritage Gold | Platform role |
| organization_id | Int? | Heritage Gold | FK to Organization |
| password_salt | String | Heritage Gold | Auth salt |
| password_hash | String | Heritage Gold | Auth hash |
| **trust_level** | Int | **NEW** | 1-6 trust level (1=new account, 6=reference account) |
| **phone_verified** | Boolean | **NEW** | Phone verified via OTP |
| **email_verified** | Boolean | **NEW** | Email verified flag |
| **identity_verified** | Boolean | **NEW** | Identity document verified |
| **professional_docs_verified** | Boolean | **NEW** | Professional documents validated |
| **professional_verified** | Boolean | **NEW** | Full professional verification |
| **reference_account** | Boolean | **NEW** | Admin-granted reference status |
| **owner_verified** | Boolean | **NEW** | Property ownership verified |
| **is_active_agent** | Boolean | **NEW** | Actively onboarded agent |
| **onboarding_status** | String | **NEW** | Agent onboarding step: invited, account_created, phone_verified, cni_uploaded, validated, active |
| **agency_role** | String? | **NEW** | Role within agency: responsible, admin, agent, assistant |
| **agent_rating** | Float? | **NEW** | 1.0-5.0 average rating |
| **badges** | JSON | **NEW** | Array of badge_type strings derived from verification flags |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| Badge | { type: String, label: String, granted_at: DateTime } | Derived trust signal badge |
| TrustLevel | Enum(1..6) | Graduated trust levels |
| AgencyRole | Enum(responsible, admin, agent, assistant) | Agency hierarchy role |
| OnboardingStatus | Enum(invited, account_created, phone_verified, cni_uploaded, validated, active) | Onboarding state |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| organization | Organization | N:1 | Agency membership |
| sessions | Session | 1:N | Auth sessions |
| conversations | Conversation | 1:N | User conversations |
| messages | Message | 1:N | Sent messages |
| notifications | Notification | 1:N | User notifications |
| projects | Project | 1:N | User projects |
| **leads** | Lead | **1:N** | Leads owned/assigned to user |
| **agent_credits** | AgentCredit | **1:1** | Agent credit balance |
| **invitations_sent** | AgentInvitation | **1:N** | Invitations sent by user |
| **professional_profile** | ProfessionalProfile | **1:1** | Professional profile |
| **approved_workflows** | ApprovalWorkflow | **1:N** | Workflows reviewed by user |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_users_trust_level | trust_level, id | Trust-level based queries |
| idx_users_onboarding | onboarding_status, id | Agent onboarding pipeline |
| idx_users_agency_role | agency_role, organization_id | Agency role queries |
| idx_users_agent_rating | agent_rating, id | Agent ranking queries |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| user_email_unique | email |
| user_username_unique | username (if set) |
| user_phone_unique | phone_e164 (if set) |

#### Lifecycle

draft → active → suspended → closed → deleted

Transitions audited via AuditEvent. Trust levels progress monotonically 1→6 (admin override allowed).

#### Privacy

| Classification | Fields |
|----------------|--------|
| PUBLIC | badges, agent_rating, is_active_agent |
| INTERNAL | trust_level, onboarding_status, agency_role |
| SENSITIVE | phone_e164, email, identity_verified, professional_docs_verified |
| CONFIDENTIAL | password_hash, password_salt, reference_account |

#### Audit

Required for: trust_level changes, verification flag changes, role changes, onboarding_status transitions, agent_rating significant changes

#### Migration Source

Heritage Gold `user` table + trust level + badge + agency role fields

---

### 3.2 Organization (ENRICH)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Organization |
| **domain** | Organizations |
| **purpose** | Represents an agency or company with enriched registration, verification, and lifecycle semantics |
| **existing_or_new** | ENRICH — extends existing `Organization` model |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | Heritage Gold | Primary key |
| name | String | Heritage Gold | Organization name |
| slug | String | Heritage Gold | URL-friendly identifier |
| kind | String | Heritage Gold | Default "agency" |
| city | String? | Heritage Gold | City location |
| **rccm** | String? | **NEW** | Trade register number |
| **tax_id** | String? | **NEW** | Tax identification number |
| **trust_level** | Int | **NEW** | 1-6 agency trust level |
| **verification_status** | String | **NEW** | verification status: unverified, pending, verified, rejected |
| **agency_verified** | Boolean | **NEW** | Agency verification badge flag |
| **lifecycle_state** | String | **NEW** | draft, active, suspended, closed, archived |
| **zones** | JSON | **NEW** | Geographic zones of operation |
| **agent_count** | Int | **NEW** | Count of active agents |
| **operational_status** | String | **NEW** | operational, non_operational (based on min agent threshold) |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| Zone | { code: String, label: String } | Geographic zone assignment |
| VerificationStatus | Enum(unverified, pending, verified, rejected) | Verification state |
| LifecycleState | Enum(draft, active, suspended, closed, archived) | Organization lifecycle |
| OperationalStatus | Enum(operational, non_operational) | Operational readiness |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| users | User | 1:N | Organization members |
| properties | Property | 1:N | Owner organization |
| conversations | Conversation | 1:N | Organization conversations |
| projects | Project | 1:N | Organization projects |
| **members** | OrganizationMember | **1:N** | Membership records with roles |
| **leads** | Lead | **1:N** | Leads assigned to organization |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_org_verification | verification_status, lifecycle_state | Verification pipeline queries |
| idx_org_operational | operational_status, agent_count | Operational agency queries |
| idx_org_trust | trust_level, id | Trust-based queries |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| org_slug_unique | slug |
| org_rccm_unique | rccm (if set) |
| org_tax_id_unique | tax_id (if set) |

#### Lifecycle

draft → active → suspended → closed → archived

Auto-suspend if agent_count < 3 for >30 days.

#### Privacy

| Classification | Fields |
|----------------|--------|
| PUBLIC | name, slug, agency_verified, trust_level, zones |
| INTERNAL | verification_status, lifecycle_state, operational_status |
| SENSITIVE | rccm, tax_id |

#### Audit

Required for: lifecycle_state transitions, verification_status changes, rccm/tax_id updates

#### Migration Source

Heritage Gold `agence` table + registration fields + verification

---

### 3.3 OrganizationMember (ENRICH)

| Attribute | Value |
|-----------|-------|
| **entity_name** | OrganizationMember |
| **domain** | Organizations |
| **purpose** | Tracks user membership within an organization with agency role, zone assignments, and lead management limits |
| **existing_or_new** | ENRICH — extends concept (currently implicit via User.organization_id) |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| organization_id | Int | NEW | FK to Organization |
| user_id | Int | NEW | FK to User |
| agency_role | String | NEW | responsible, admin, agent, assistant |
| zones | JSON | NEW | Geographic zones assigned to this member |
| max_leads | Int | NEW | Maximum leads this member can handle |
| is_active | Boolean | NEW | Active membership flag |
| joined_at | String | NEW | Membership start date |
| left_at | String? | NEW | Membership end date |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| organization | Organization | N:1 | Parent organization |
| user | User | N:1 | Member user |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_org_member_org | organization_id, agency_role | Org role queries |
| idx_org_member_user | user_id | User membership lookup |
| idx_org_member_active | organization_id, is_active | Active members queries |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| org_member_unique | organization_id, user_id |

#### Lifecycle

active → inactive (left_at set) — membership is terminated, not deleted

#### Privacy

INTERNAL

#### Audit

Required for: role changes, zone changes, membership termination

#### Migration Source

Derived from Heritage Gold `agent_agence` + `agent_zone` tables

---

### 3.4 Property (ENRICH)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Property |
| **domain** | Properties & Listings |
| **purpose** | Core property listing with enriched family/type hierarchy, multi-level pricing, lifecycle states, boost, and quality scoring |
| **existing_or_new** | ENRICH — extends existing `Property` model |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | Heritage Gold | Primary key |
| listing_code | String? | Heritage Gold | Unique listing code |
| title | String | Heritage Gold | Property title |
| summary | String | Heritage Gold | Property description |
| address_line | String? | Heritage Gold | Street address |
| city | String | Heritage Gold | City |
| region | String? | Heritage Gold | Region/state |
| postal_code | String? | Heritage Gold | Postal code |
| country | String | Heritage Gold | Country |
| latitude | Float? | Heritage Gold | Latitude |
| longitude | Float? | Heritage Gold | Longitude |
| price_min | Int? | Heritage Gold | Minimum price |
| price_max | Int? | Heritage Gold | Maximum price |
| currency | String | Heritage Gold | Currency code |
| status | String | Heritage Gold | Property status |
| availability | String | Heritage Gold | available, pending, rented, sold, archived |
| property_type | String | Heritage Gold | Property type |
| owner_organization_id | Int? | Heritage Gold | FK to Organization |
| bedrooms | Int | Heritage Gold | Bedroom count |
| bathrooms | Int | Heritage Gold | Bathroom count |
| area_sqm | Float | Heritage Gold | Area in sqm |
| metadata_json | String | Heritage Gold | JSON metadata |
| **property_family** | String | **NEW** | residential, commercial, industrial, land, agricultural, hotel, project |
| **property_subtype** | String? | **NEW** | Specific subtype within family |
| **price_displayed** | Int? | **NEW** | Display price |
| **price_negotiable** | Boolean | **NEW** | Price negotiable flag |
| **price_final** | Int? | **NEW** | Final agreed price |
| **price_estimation** | Int? | **NEW** | Estimated value |
| **price_history** | JSON | **NEW** | Historical prices array |
| **quality_score** | Float? | **NEW** | 0-100 quality score |
| **quality_grade** | String? | **NEW** | A+, A, B, C, D grade |
| **boost_level** | Int | **NEW** | 0=none, 1=basic, 2=premium boost |
| **boost_expires_at** | String? | **NEW** | Boost expiration timestamp |
| **is_premium** | Boolean | **NEW** | Premium listing flag |
| **verification_status** | String | **NEW** | unverified, pending, verified, rejected |
| **verified_at** | String? | **NEW** | Verification timestamp |
| **data_completeness** | Float? | **NEW** | 0-100 completeness score |
| **lifecycle_state** | String | **NEW** | reception, normalization, classification, validation, publication, matching, mise_en_relation, follow_up, archiving, conservation |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| PropertyFamily | Enum(7 families) | Top-level classification |
| PriceLevel | { type, amount, currency } | Typed price entry |
| QualityGrade | Enum(A+, A, B, C, D) | Data quality grade |
| BoostLevel | Enum(0, 1, 2) | Visibility boost level |
| VerificationStatus | Enum(unverified, pending, verified, rejected) | Verification state |
| LifecycleState | Enum(10 states) | Property lifecycle |
| AvailabilityState | Enum(available, pending, rented, sold, archived) | Availability |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| owner_organization | Organization | N:1 | Owning agency |
| media | Media | 1:N | Property media |
| conversations | Conversation | 1:N | Related conversations |
| **visits** | Visit | **1:N** | Property visits |
| **matches** | Match | **1:N** | Matches involving this property |
| **leads** | Lead | **1:N** | Leads referencing this property |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_prop_family | property_family, property_type | Family/type queries |
| idx_prop_quality | quality_score, quality_grade | Quality-based queries |
| idx_prop_boost | boost_level, boost_expires_at | Boost queries |
| idx_prop_lifecycle | lifecycle_state, status | Lifecycle queries |
| idx_prop_verification | verification_status, verified_at | Verification queries |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| prop_listing_code_unique | listing_code (if set) |

#### Lifecycle

10 states: reception → normalization → classification → validation → publication → matching → mise_en_relation → follow_up → archiving → conservation

#### Privacy

| Classification | Fields |
|----------------|--------|
| PUBLIC | title, summary, city, region, property_family, property_type, price_displayed, quality_grade, boost_level, is_premium |
| INTERNAL | quality_score, data_completeness, lifecycle_state, verification_status |
| SENSITIVE | address_line, latitude, longitude, price_history, price_final |

#### Audit

Required for: lifecycle_state transitions, verification_status changes, boost_level changes, quality_score recalculations

#### Migration Source

Heritage Gold `bien` table + property taxonomy + pricing model + lifecycle states

---

### 3.5 Project (ENRICH)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Project |
| **domain** | Projects & Dossiers |
| **purpose** | User's real estate objective with enriched dossier semantics, double consent workflow, and rematching support |
| **existing_or_new** | ENRICH — extends existing `Project` model |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | Heritage Gold | Primary key |
| user_id | Int | Heritage Gold | FK to User |
| organization_id | Int? | Heritage Gold | FK to Organization |
| title | String | Heritage Gold | Project title |
| project_type | String | Heritage Gold | buy, rent, sell, invest, etc. |
| objective | String | Heritage Gold | Project objective |
| budget_min | Int? | Heritage Gold | Minimum budget |
| budget_max | Int? | Heritage Gold | Maximum budget |
| currency | String | Heritage Gold | Default "XAF" |
| location_city | String? | Heritage Gold | Target city |
| location_region | String? | Heritage Gold | Target region |
| location_country | String? | Heritage Gold | Default "Cameroon" |
| status | String | Heritage Gold | Project status |
| priority | String | Heritage Gold | normal, high, urgent |
| **dossier_status** | String | **NEW** | Dossier lifecycle: intent, qualification, matching, mise_en_relation, visit, negotiation, transaction, closure, archiving |
| **consent_status** | String | **NEW** | Double consent: none, demandeur_interested, holder_contacted, holder_favorable, double_consent_obtained |
| **rematching_count** | Int | **NEW** | Number of rematch cycles |
| **urgency_level** | String | **NEW** | low, medium, high, critical |
| **intent_source** | String? | **NEW** | Source intent that created this project |
| **intent_confidence** | Float? | **NEW** | Confidence score of intent detection |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| DossierStatus | Enum(9 states) | Full dossier lifecycle |
| ConsentStatus | Enum(5 states) | Double consent workflow |
| UrgencyLevel | Enum(low, medium, high, critical) | Urgency classification |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| user | User | N:1 | Project owner |
| organization | Organization | N:1 | Owning organization |
| steps | ProjectStep | 1:N | Project steps |
| checklist_items | ProjectChecklistItem | 1:N | Checklist items |
| step_history | ProjectStepHistory | 1:N | Step history |
| **intent** | Intent | **N:1** | Source intent |
| **match** | Match | **1:N** | Project matches |
| **visits** | Visit | **1:N** | Project visits |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_project_dossier | dossier_status, status | Dossier pipeline queries |
| idx_project_consent | consent_status, id | Consent workflow queries |
| idx_project_rematch | rematching_count, id | Rematch queries |
| idx_project_urgency | urgency_level, priority | Urgency-based queries |

#### Lifecycle

9-state dossier lifecycle: intent → qualification → matching → mise_en_relation → visit → negotiation → transaction → closure → archiving

#### Privacy

| Classification | Fields |
|----------------|--------|
| PUBLIC | title, project_type, objective |
| INTERNAL | dossier_status, consent_status, rematching_count, urgency_level |
| SENSITIVE | budget_min, budget_max, location fields |

#### Audit

Required for: dossier_status transitions, consent_status changes, rematching events

#### Migration Source

Heritage Gold `projet` + `dossier` tables + consent workflow + rematching

---

### 3.6 Intent (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Intent |
| **domain** | Intent Detection |
| **purpose** | Captures detected user intent from conversation messages with confidence scoring, multi-intent support, and urgency detection |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| user_id | Int | NEW | FK to User who expressed intent |
| conversation_id | Int? | NEW | FK to source conversation |
| message_id | Int? | NEW | FK to source message |
| intent_type | String | NEW | buy, rent, sell, invest, find, finance, service, visit, estimate |
| confidence | Float | NEW | 0.0-1.0 detection confidence |
| is_primary | Boolean | NEW | Primary intent flag for multi-intent |
| multi_intent_group | String? | NEW | Group ID for multi-intent batches |
| urgency_score | Float? | NEW | 0.0-1.0 urgency score |
| extracted_entities | JSON | NEW | Entities extracted: budget, location, type, timeline |
| role_mapping | String | NEW | Mapped role: buyer, tenant, seller, investor, visitor |
| detection_pipeline | String | NEW | Pipeline version/stage that detected this |
| raw_input | String | NEW | Original user message |
| created_at | String | NEW | Detection timestamp |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| IntentType | Enum(buy, rent, sell, invest, find, finance, service, visit, estimate) | Detected intent types |
| ExtractedEntity | { type, value, confidence } | Entity extraction result |
| RoleMapping | Enum(buyer, tenant, seller, investor, visitor, professional) | Mapped platform role |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| user | User | N:1 | User who expressed intent |
| conversation | Conversation | N:1 | Source conversation |
| message | Message | N:1 | Source message |
| projects | Project | 1:N | Projects created from this intent |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_intent_user | user_id, created_at | User intent history |
| idx_intent_type | intent_type, confidence | Type-based queries |
| idx_intent_urgency | urgency_score, created_at | Urgent intent queries |
| idx_intent_conversation | conversation_id | Conversation intent lookup |

#### Lifecycle

detected → confirmed → mapped → fulfilled → expired

#### Privacy

| Classification | Fields |
|----------------|--------|
| INTERNAL | intent_type, confidence, is_primary, urgency_score, role_mapping |
| SENSITIVE | raw_input, extracted_entities |

#### Audit

Required for: intent detection events, confidence threshold breaches, role mapping changes

#### Migration Source

NEW — intent detection pipeline

---

### 3.7 Match (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Match |
| **domain** | Matching |
| **purpose** | Records the result of matching between a project/dossier and a property with scoring dimensions and compatibility level |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| project_id | Int | NEW | FK to Project |
| property_id | Int | NEW | FK to Property |
| score_real_estate | Float | NEW | Real estate dimension score (0-100) |
| score_availability | Float | NEW | Availability dimension score |
| score_document | Float | NEW | Document dimension score |
| score_reliability | Float | NEW | Holder reliability score |
| score_transaction_success | Float | NEW | Transaction success probability |
| score_geographic | Float | NEW | Geographic proximity score |
| score_overall | Float | NEW | Weighted composite score |
| compatibility_level | String | NEW | excellent, good, average, low |
| ranking_position | Int | NEW | Position in ranked results |
| exclusion_reason | String? | NEW | Reason if excluded |
| match_status | String | NEW | pending, proposed, accepted, rejected, expired |
| rematching_cycle | Int | NEW | Rematch cycle number |
| proposed_at | String | NEW | Match proposal timestamp |
| decided_at | String? | NEW | Decision timestamp |
| created_at | String | NEW | Record creation |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| ScoreDimension | { name, value, weight } | Individual scoring dimension |
| CompatibilityLevel | Enum(excellent, good, average, low) | Match quality level |
| MatchStatus | Enum(pending, proposed, accepted, rejected, expired) | Match lifecycle |
| ScoringProfile | { dimensions[], weights[] } | Complete scoring profile |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| project | Project | N:1 | Matched project |
| property | Property | N:1 | Matched property |
| visits | Visit | 1:N | Visits resulting from match |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_match_project | project_id, score_overall | Project match ranking |
| idx_match_property | property_id, score_overall | Property match ranking |
| idx_match_status | match_status, compatibility_level | Status-based queries |
| idx_match_rematch | rematching_cycle, project_id | Rematch queries |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| match_unique_per_cycle | project_id, property_id, rematching_cycle |

#### Lifecycle

scoring → proposed → accepted → contact_initiated | rejected → rematching (cycle++) | expired

#### Privacy

INTERNAL — match scores are platform-internal

#### Audit

Required for: match creation, status transitions, rematching events, score recalculation

#### Migration Source

NEW — matching engine

---

### 3.8 Visit (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Visit |
| **domain** | Visits |
| **purpose** | Manages property visit scheduling with 9-state lifecycle, reminders, and satisfaction tracking |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| project_id | Int | NEW | FK to Project |
| property_id | Int | NEW | FK to Property |
| match_id | Int? | NEW | FK to Match that triggered this visit |
| requested_by_user_id | Int | NEW | FK to User requesting visit |
| organized_by_user_id | Int? | NEW | FK to agent organizing visit |
| scheduled_at | String | NEW | Scheduled datetime |
| confirmed_at | String? | NEW | Confirmation timestamp |
| completed_at | String? | NEW | Completion timestamp |
| cancelled_at | String? | NEW | Cancellation timestamp |
| cancellation_reason | String? | NEW | Reason for cancellation |
| visit_status | String | NEW | 9-state lifecycle |
| visit_type | String | NEW | initial, contre_visite, expertise |
| reminder_24h_sent | Boolean | NEW | 24h reminder sent |
| reminder_2h_sent | Boolean | NEW | 2h reminder sent |
| satisfaction_score | Int? | NEW | 1-5 post-visit satisfaction |
| satisfaction_feedback | String? | NEW | Post-visit comments |
| no_show_party | String? | NEW | demandeur, detenteur if no-show |
| created_at | String | NEW | Record creation |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| VisitStatus | Enum(9 states) | demandee, awaiting_confirmation, confirmed, rescheduled, cancelled, completed, refused, no_show_demandeur, no_show_detenteur |
| VisitType | Enum(initial, contre_visite, expertise) | Visit classification |
| SatisfactionLevel | Enum(1..5) | Post-visit satisfaction |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| project | Project | N:1 | Associated project |
| property | Property | N:1 | Property to visit |
| match | Match | N:1 | Source match |
| requester | User | N:1 | User requesting visit |
| organizer | User | N:1 | Agent organizing |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_visit_project | project_id, visit_status | Project visit queries |
| idx_visit_property | property_id, scheduled_at | Property visit schedule |
| idx_visit_status | visit_status, scheduled_at | Status-based filters |
| idx_visit_satisfaction | satisfaction_score, id | Satisfaction analysis |

#### Lifecycle

9 states: demandee → awaiting_confirmation → confirmed → rescheduled → cancelled | completed | refused | no_show_demandeur | no_show_detenteur

#### Privacy

| Classification | Fields |
|----------------|--------|
| INTERNAL | visit_status, visit_type, scheduled_at |
| SENSITIVE | satisfaction_feedback, no_show_party |

#### Audit

Required for: all status transitions, satisfaction submission, no-show events

#### Migration Source

Heritage Gold `visite` table + lifecycle states

---

### 3.9 Transaction (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Transaction |
| **domain** | Transactions |
| **purpose** | End-to-end transaction processing with 7-state lifecycle, document requirements per transaction type |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| project_id | Int | NEW | FK to Project |
| property_id | Int | NEW | FK to Property |
| visit_id | Int? | NEW | FK to Visit |
| transaction_type | String | NEW | sale, purchase, rental, lease, commercial_lease, short_stay |
| status | String | NEW | 7-state lifecycle |
| agreed_price | Int? | NEW | Agreed transaction price |
| currency | String | NEW | Currency code |
| commission_amount | Int? | NEW | LAWIM commission |
| commission_percentage | Float? | NEW | Commission rate |
| deposit_amount | Int? | NEW | Security deposit |
| expected_closing_date | String? | NEW | Target closing date |
| closed_at | String? | NEW | Actual closing date |
| cancelled_at | String? | NEW | Cancellation date |
| cancellation_reason | String? | NEW | Cancellation reason |
| doc_checklist | JSON | NEW | Document checklist per transaction type |
| doc_submission_status | String | NEW | pending, partial, complete |
| created_at | String | NEW | Record creation |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| TransactionType | Enum(sale, purchase, rental, lease, commercial_lease, short_stay) | Type of transaction |
| TransactionStatus | Enum(7 states) | agreement, preparation, documents, payment, signature, handover, completed, archived, failed |
| DocumentRequirement | { type, required, submitted, verified } | Per-document tracking |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| project | Project | N:1 | Associated project |
| property | Property | N:1 | Property being transacted |
| visit | Visit | N:1 | Triggering visit |
| documents | Document | 1:N | Transaction documents |
| payments | Payment | 1:N | Transaction payments |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_trx_project | project_id, status | Project transaction queries |
| idx_trx_property | property_id, status | Property transaction queries |
| idx_trx_status | status, transaction_type | Status-type queries |
| idx_trx_closing | expected_closing_date, status | Closing pipeline queries |

#### Lifecycle

7 states: agreement → preparation → documents → payment → signature → handover → completed | archived | failed

#### Privacy

| Classification | Fields |
|----------------|--------|
| INTERNAL | transaction_type, status, doc_submission_status |
| SENSITIVE | agreed_price, deposit_amount, commission_amount, commission_percentage |

#### Audit

Required for: all status transitions, price changes, document submissions, cancellation

#### Migration Source

Heritage Gold `transaction` table + lifecycle workflow

---

### 3.10 Service (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Service |
| **domain** | Services |
| **purpose** | Service catalog definition with pricing, type classification, and lifecycle management |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| code | String | NEW | Unique service code |
| name | String | NEW | Service display name |
| description | String? | NEW | Service description |
| service_category | String | NEW | monetized, real_estate, professional, crm |
| service_type | String | NEW | boost_7j, boost_30j, premium_listing, agent_pro, visit_accompaniment, transaction_accompaniment, lead_bronze, lead_silver, lead_gold, etc. |
| base_price | Int | NEW | Base price in FCFA |
| currency | String | NEW | Default "XAF" |
| billing_model | String | NEW | one_time, recurring_monthly, pay_per_use |
| duration_days | Int? | NEW | Service duration if applicable |
| status | String | NEW | active, inactive, deprecated |
| metadata | JSON | NEW | Additional service metadata |
| created_at | String | NEW | Record creation |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| ServiceCategory | Enum(monetized, real_estate, professional, crm) | Service category |
| BillingModel | Enum(one_time, recurring_monthly, pay_per_use) | Billing model |
| ServiceStatus | Enum(active, inactive, deprecated) | Service lifecycle |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| orders | ServiceOrder | 1:N | Orders for this service |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_svc_category | service_category, status | Category queries |
| idx_svc_type | service_type, status | Type-based queries |
| idx_svc_price | base_price, service_category | Price-based queries |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| svc_code_unique | code |
| svc_type_unique | service_type |

#### Lifecycle

active → inactive → deprecated

#### Privacy

PUBLIC — service catalog is platform-public

#### Audit

Required for: price changes, status transitions

#### Migration Source

Heritage Gold service catalog + pricing matrices

---

### 3.11 ServiceOrder (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | ServiceOrder |
| **domain** | Services |
| **purpose** | Tracks the lifecycle of a service purchase from creation through fulfillment and expiration |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| service_id | Int | NEW | FK to Service |
| user_id | Int | NEW | FK to User placing order |
| organization_id | Int? | NEW | FK to Organization |
| property_id | Int? | NEW | FK to Property (if service is property-specific) |
| project_id | Int? | NEW | FK to Project |
| status | String | NEW | 8-state lifecycle |
| price_paid | Int | NEW | Actual price paid |
| currency | String | NEW | Currency code |
| quantity | Int | NEW | Default 1 |
| activation_date | String? | NEW | When service becomes active |
| expiration_date | String? | NEW | When service expires |
| payment_link | String? | NEW | Campay payment link |
| payment_id | Int? | NEW | FK to Payment |
| metadata | JSON | NEW | Order metadata |
| created_at | String | NEW | Record creation |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| ServiceOrderStatus | Enum(8 states) | created, proposed, accepted, payment_pending, activated, in_use, expired, archived |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| service | Service | N:1 | Ordered service |
| user | User | N:1 | Ordering user |
| organization | Organization | N:1 | Ordering organization |
| property | Property | N:1 | Associated property |
| project | Project | N:1 | Associated project |
| payment | Payment | N:1 | Associated payment |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_so_user | user_id, status | User order queries |
| idx_so_service | service_id, status | Service order queries |
| idx_so_status | status, expiration_date | Expiration queries |
| idx_so_payment | payment_id | Payment lookup |

#### Lifecycle

8 states: created → proposed → accepted → payment_pending → activated → in_use → expired → archived

#### Privacy

| Classification | Fields |
|----------------|--------|
| INTERNAL | status, price_paid, quantity |
| SENSITIVE | payment_link, payment_id |

#### Audit

Required for: all status transitions, payment events, price changes

#### Migration Source

Heritage Gold `commande_service` table

---

### 3.12 Payment (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Payment |
| **domain** | Financial Core |
| **purpose** | Payment processing with 10-state sub-machine, Campay integration, and reconciliation |
| **existing_or_new** | NEW — replaces basic Payment concept from canonical model |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| service_order_id | Int? | NEW | FK to ServiceOrder |
| transaction_id | Int? | NEW | FK to Transaction |
| user_id | Int | NEW | FK to User making payment |
| amount | Int | NEW | Payment amount in FCFA |
| currency | String | NEW | Default "XAF" |
| status | String | NEW | 10-state lifecycle |
| payment_method | String? | NEW | campay, orange_money, mobile_money, card |
| provider_reference | String? | NEW | Campay transaction reference |
| provider_status | String? | NEW | Raw provider status |
| payment_link | String? | NEW | Campay payment URL |
| failure_reason | String? | NEW | Failure reason if applicable |
| refund_reason | String? | NEW | Refund reason if applicable |
| refunded_at | String? | NEW | Refund timestamp |
| reconciled_at | String? | NEW | Reconciliation timestamp |
| disputed_at | String? | NEW | Dispute timestamp |
| metadata | JSON | NEW | Payment metadata |
| created_at | String | NEW | Record creation |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| PaymentStatus | Enum(10 states) | created, initiated, pending, confirmed, failed, cancelled, expired, refunded, reconciled, disputed |
| PaymentMethod | Enum(campay, orange_money, mobile_money, card) | Supported methods |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| service_order | ServiceOrder | N:1 | Related service order |
| transaction | Transaction | N:1 | Related transaction |
| user | User | N:1 | Paying user |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_payment_user | user_id, status | User payment queries |
| idx_payment_status | status, created_at | Status-based queries |
| idx_payment_provider | provider_reference | Provider lookup |
| idx_payment_so | service_order_id | Service order payment |

#### Lifecycle

10 states: created → initiated → pending → confirmed → failed | cancelled | expired → refunded → reconciled → disputed

#### Privacy

| Classification | Fields |
|----------------|--------|
| INTERNAL | amount, status, payment_method |
| SENSITIVE | provider_reference, payment_link, failure_reason, refund_reason |

#### Audit

Required for: all status transitions, refund events, dispute events, reconciliation

#### Migration Source

Heritage Gold `paiement` table + Campay integration

---

### 3.13 AgentCredit (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | AgentCredit |
| **domain** | Financial Core |
| **purpose** | Manages agent credit balance for lead purchases and service consumption |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| user_id | Int | NEW | FK to User (agent) |
| balance | Int | NEW | Current credit balance in FCFA |
| total_purchased | Int | NEW | Lifetime credits purchased |
| total_spent | Int | NEW | Lifetime credits spent |
| last_recharge_at | String? | NEW | Last recharge timestamp |
| last_usage_at | String? | NEW | Last credit usage timestamp |
| auto_recharge_enabled | Boolean | NEW | Auto-recharge when low |
| auto_recharge_threshold | Int? | NEW | Balance threshold for auto-recharge |
| auto_recharge_amount | Int? | NEW | Amount for auto-recharge |
| created_at | String | NEW | Record creation |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| CreditTransaction | { type, amount, balance_after, reference, timestamp } | Individual credit movement |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| user | User | 1:1 | Agent owning credits |
| transactions | CreditTransaction | 1:N | Credit movement history |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_ac_balance | balance, user_id | Low balance alerts |
| idx_ac_user | user_id | User lookup |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| agent_credit_user_unique | user_id |

#### Lifecycle

active (balance ≥ 0) → depleted (balance = 0) → recharged

#### Privacy

SENSITIVE — credit balance is financial data

#### Audit

Required for: all balance changes, recharge events, spend events, threshold breaches

#### Migration Source

Heritage Gold `credit_agent` table

---

### 3.14 LeadPurchase (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | LeadPurchase |
| **domain** | CRM |
| **purpose** | Tracks lead purchase transactions between agents and the platform; core monetization mechanism |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| user_id | Int | NEW | FK to User (purchasing agent) |
| lead_id | Int | NEW | FK to Lead |
| organization_id | Int? | NEW | FK to Organization |
| purchase_type | String | NEW | lead_bronze, lead_silver, lead_gold, coordinate_unlock |
| price_paid | Int | NEW | Price paid in FCFA |
| currency | String | NEW | Default "XAF" |
| payment_id | Int? | NEW | FK to Payment |
| credit_id | Int? | NEW | FK to AgentCredit transaction |
| status | String | NEW | completed, refunded, disputed |
| purchased_at | String | NEW | Purchase timestamp |
| refunded_at | String? | NEW | Refund timestamp |
| created_at | String | NEW | Record creation |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| PurchaseType | Enum(lead_bronze, lead_silver, lead_gold, coordinate_unlock) | Lead purchase pack |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| user | User | N:1 | Purchasing agent |
| lead | Lead | N:1 | Purchased lead |
| organization | Organization | N:1 | Purchasing agency |
| payment | Payment | N:1 | Associated payment |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_lp_user | user_id, purchased_at | Agent purchase history |
| idx_lp_lead | lead_id | Lead purchase lookup |
| idx_lp_status | status, purchased_at | Status queries |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| lead_purchase_unique | lead_id, user_id (for lead_bronze type) |

#### Lifecycle

completed → refunded | disputed

#### Privacy

SENSITIVE — financial transaction data

#### Audit

Required for: all purchases, refunds, disputes

#### Migration Source

Heritage Gold `achat_lead` table

---

### 3.15 Lead (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Lead |
| **domain** | CRM |
| **purpose** | CRM pipeline entity with scoring, classification, routing, and SLA tracking |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| user_id | Int | NEW | FK to User (lead source) |
| assigned_to_user_id | Int? | NEW | FK to assigned agent |
| organization_id | Int? | NEW | FK to Organization |
| property_id | Int? | NEW | FK to Property |
| project_id | Int? | NEW | FK to Project |
| source_conversation_id | Int? | NEW | FK to source conversation |
| lead_type | String | NEW | tenant, buyer, seller, investor, diaspora_investor |
| lead_status | String | NEW | new, contacted, qualified, proposal, negotiation, won, lost, spam |
| base_score | Int | NEW | Base score by lead type |
| score_boosters | Int | NEW | Accumulated booster points |
| score_penalties | Int | NEW | Accumulated penalty points |
| score_total | Int | NEW | Final computed score |
| classification | String | NEW | HOT, WARM, COLD, LOW, SPAM |
| routing_zone | String? | NEW | Geographic zone for routing |
| urgency_level | String | NEW | low, medium, high, critical |
| sla_priority | String | NEW | P0, P1, P2, P3 |
| sla_deadline | String? | NEW | SLA response deadline |
| sla_breached | Boolean | NEW | SLA breach flag |
| behavior_data | JSON | NEW | message_history, response_time, budget_changes, visit_requests |
| fraud_flags | JSON | NEW | Anti-fraud detection results |
| score_breakdown | JSON | NEW | Detailed scoring dimensions |
| first_response_at | String? | NEW | First agent response |
| last_activity_at | String? | NEW | Last activity timestamp |
| converted_at | String? | NEW | Conversion timestamp |
| created_at | String | NEW | Record creation |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| LeadType | Enum(tenant, buyer, seller, investor, diaspora_investor) | Lead classification |
| LeadStatus | Enum(8 stages) | CRM pipeline stages |
| Classification | Enum(HOT, WARM, COLD, LOW, SPAM) | Lead tier |
| ScoreBooster | { type, points } | Individual booster |
| ScorePenalty | { type, points } | Individual penalty |
| FraudFlag | { type, severity, detected_at } | Fraud detection result |
| SLAPriority | Enum(P0, P1, P2, P3) | SLA priority level |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| user | User | N:1 | Source user |
| assigned_to | User | N:1 | Assigned agent |
| organization | Organization | N:1 | Assigned agency |
| property | Property | N:1 | Referenced property |
| project | Project | N:1 | Referenced project |
| conversation | Conversation | N:1 | Source conversation |
| purchases | LeadPurchase | 1:N | Lead purchase records |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_lead_assigned | assigned_to_user_id, lead_status | Agent lead queue |
| idx_lead_classification | classification, score_total | Classification queries |
| idx_lead_org | organization_id, lead_status | Org lead pipeline |
| idx_lead_sla | sla_priority, sla_deadline, sla_breached | SLA monitoring |
| idx_lead_fraud | fraud_flags | Fraud detection queries |
| idx_lead_created | created_at, lead_type | Lead creation queries |

#### Lifecycle

8-stage pipeline: new → contacted → qualified → proposal → negotiation → won | lost | spam

#### Privacy

| Classification | Fields |
|----------------|--------|
| INTERNAL | lead_type, lead_status, classification, score_total, urgency_level |
| SENSITIVE | behavior_data, fraud_flags, score_breakdown |

#### Audit

Required for: status transitions, score recalculations, classification changes, assignment changes, SLA breaches

#### Migration Source

Heritage Gold `lead` + CRM pipeline

---

### 3.16 Document (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Document |
| **domain** | Documents & GED |
| **purpose** | Typed, verifiable document attached to entities, supporting per-transaction-type document requirements |
| **existing_or_new** | NEW — extends concept from canonical `Document` model |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| document_type | String | NEW | cni, passport, land_title, contract, deposit_proof, inventory, power_of_attorney, tax_receipt, rccm, proof_of_address, etc. |
| entity_type | String | NEW | user, organization, property, transaction, project |
| entity_id | Int | NEW | FK to the owning entity |
| transaction_id | Int? | NEW | FK to Transaction |
| file_url | String | NEW | Document file URL |
| file_hash | String? | NEW | File integrity hash |
| file_size | Int? | NEW | File size in bytes |
| mime_type | String? | NEW | MIME type |
| verification_status | String | NEW | pending, verified, rejected |
| verified_by_user_id | Int? | NEW | FK to verifying user |
| verified_at | String? | NEW | Verification timestamp |
| rejection_reason | String? | NEW | Reason if rejected |
| is_mandatory | Boolean | NEW | Mandatory for transaction type |
| expires_at | String? | NEW | Document expiry (e.g. CNI) |
| metadata | JSON | NEW | Document metadata |
| created_at | String | NEW | Upload timestamp |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| DocumentType | Enum(extensive) | Supported document types |
| VerificationStatus | Enum(pending, verified, rejected) | Document verification state |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| transaction | Transaction | N:1 | Related transaction |
| verified_by | User | N:1 | Verifying admin |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_doc_entity | entity_type, entity_id | Entity document lookup |
| idx_doc_type | document_type, verification_status | Type-verification queries |
| idx_doc_transaction | transaction_id, document_type | Transaction document checklist |
| idx_doc_verifier | verified_by_user_id | Verifier queries |
| idx_doc_expiry | expires_at, verification_status | Expiry monitoring |

#### Lifecycle

uploaded → pending → verified | rejected | expired

#### Privacy

| Classification | Fields |
|----------------|--------|
| INTERNAL | document_type, verification_status, is_mandatory |
| SENSITIVE | file_url, file_hash, rejection_reason |
| CONFIDENTIAL | file content (not stored in DB) |

#### Audit

Required for: upload, verification, rejection, expiry events

#### Migration Source

Heritage Gold `document` table + GED

---

### 3.17 Event (ENRICH)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Event |
| **domain** | Audit & Observability |
| **purpose** | Typed event catalog for all domain events, state transitions, and audit trails; enriched with structured payloads and actor tracking |
| **existing_or_new** | ENRICH — extends existing `Event` model |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | Heritage Gold | Primary key |
| kind | String | Heritage Gold | Event type identifier |
| payload | String | Heritage Gold | Event payload JSON |
| created_at | String | Heritage Gold | Event timestamp |
| **actor_user_id** | Int? | **NEW** | FK to User who triggered event |
| **entity_type** | String? | **NEW** | Type of entity affected |
| **entity_id** | Int? | **NEW** | ID of entity affected |
| **event_version** | Int | **NEW** | Schema version of payload |
| **correlation_id** | String? | **NEW** | Correlation ID for event chains |
| **causation_id** | String? | **NEW** | ID of causing event |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| EventKind | Enum(catalog) | Standardized event types |
| EventEnvelope | { kind, version, actor, entity, payload, metadata } | Enriched event envelope |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| actor | User | N:1 | User who triggered event |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_event_actor | actor_user_id, created_at | Actor event history |
| idx_event_entity | entity_type, entity_id | Entity event history |
| idx_event_correlation | correlation_id | Event chain tracing |
| idx_event_kind_entity | kind, entity_type, entity_id | Kind-entity queries |

#### Lifecycle

N/A — append-only event log

#### Privacy

| Classification | Fields |
|----------------|--------|
| INTERNAL | kind, entity_type, entity_id, actor_user_id |
| SENSITIVE | payload (may contain personal data) |

#### Audit

Event entity IS the audit log

#### Migration Source

Heritage Gold `evenement` table + event catalog standardization

---

### 3.18 ApprovalWorkflow (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | ApprovalWorkflow |
| **domain** | Permissions |
| **purpose** | Generic approval workflow for agency creation, listing validation, professional verification, and other approval processes |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| approval_type | String | NEW | agency_creation, listing_validation, professional_verification, org_verification, document_verification |
| target_type | String | NEW | organization, property, user, document |
| target_id | Int | NEW | ID of target entity |
| requester_user_id | Int | NEW | FK to requesting user |
| reviewer_user_id | Int? | NEW | FK to reviewer/approver |
| status | String | NEW | pending, approved, rejected, cancelled |
| review_notes | String? | NEW | Reviewer notes |
| approved_at | String? | NEW | Approval timestamp |
| rejected_at | String? | NEW | Rejection timestamp |
| rejection_reason | String? | NEW | Reason for rejection |
| escalation_level | Int | NEW | 1, 2, 3 escalation tier |
| created_at | String | NEW | Request timestamp |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| ApprovalType | Enum(5 types) | Type of approval |
| ApprovalStatus | Enum(pending, approved, rejected, cancelled) | Workflow state |
| EscalationLevel | Enum(1, 2, 3) | Escalation tier |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| requester | User | N:1 | Requesting user |
| reviewer | User | N:1 | Reviewing user |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_aw_target | target_type, target_id | Target lookup |
| idx_aw_status | status, approval_type | Status queries |
| idx_aw_reviewer | reviewer_user_id, status | Reviewer queue |
| idx_aw_escalation | escalation_level, status | Escalation queries |

#### Lifecycle

pending → approved | rejected | cancelled

Escalation: level 1 → level 2 → level 3 on timeout

#### Privacy

INTERNAL

#### Audit

Required for: all status transitions, escalation events

#### Migration Source

Heritage Gold `approbation` workflow

---

### 3.19 Mediation (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Mediation |
| **domain** | Dispute Resolution |
| **purpose** | Dispute resolution process with mediator appointment, exchange facilitation, and solution proposal |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| incident_id | Int | NEW | FK to Incident |
| project_id | Int? | NEW | FK to Project |
| transaction_id | Int? | NEW | FK to Transaction |
| mediator_user_id | Int? | NEW | FK to mediator user |
| demandeur_user_id | Int | NEW | FK to demandeur |
| detenteur_user_id | Int | NEW | FK to detenteur |
| status | String | NEW | 8-state lifecycle |
| mediation_type | String | NEW | visit_dispute, transaction_dispute, contract_dispute, quality_dispute |
| demandeur_acceptance | Boolean? | NEW | Demandeur accepts mediation |
| detenteur_acceptance | Boolean? | NEW | Detenteur accepts mediation |
| proposed_solution | String? | NEW | Mediator's proposed solution |
| solution_accepted_by_demandeur | Boolean? | NEW | Solution accepted by demandeur |
| solution_accepted_by_detenteur | Boolean? | NEW | Solution accepted by detenteur |
| resolution_notes | String? | NEW | Final resolution notes |
| created_at | String | NEW | Record creation |
| resolved_at | String? | NEW | Resolution timestamp |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| MediationStatus | Enum(8 states) | incident_reported, mediation_proposed, parties_accepted, mediator_nominated, exchanges, solution_proposed, resolved, closed |
| MediationType | Enum(4 types) | Type of dispute |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| incident | Incident | 1:1 | Source incident |
| project | Project | N:1 | Related project |
| transaction | Transaction | N:1 | Related transaction |
| mediator | User | N:1 | Assigned mediator |
| demandeur | User | N:1 | Demandeur party |
| detenteur | User | N:1 | Detenteur party |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_med_incident | incident_id | Incident lookup |
| idx_med_status | status, created_at | Status queries |
| idx_med_mediator | mediator_user_id, status | Mediator caseload |

#### Lifecycle

8 states: incident_reported → mediation_proposed → parties_accepted → mediator_nominated → exchanges → solution_proposed → resolved → closed

#### Privacy

SENSITIVE — dispute information is confidential

#### Audit

Required for: all status transitions, party acceptances, solution proposals

#### Migration Source

Heritage Gold `mediation` workflow

---

### 3.20 Incident (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Incident |
| **domain** | Incident Management |
| **purpose** | Tracks incidents, disputes, claims, and fraud reports with priority levels and resolution workflow |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| incident_type | String | NEW | property_unavailable, inaccurate_info, visit_cancellation, participant_absence, fraud, fake_documents, platform_abuse, payment_dispute, contract_dispute |
| priority | String | NEW | critical, high, normal, low |
| status | String | NEW | 8-state lifecycle |
| reporter_user_id | Int | NEW | FK to reporting user |
| assigned_to_user_id | Int? | NEW | FK to assigned handler |
| target_type | String? | NEW | user, property, transaction, organization |
| target_id | Int? | NEW | ID of affected entity |
| description | String | NEW | Incident description |
| evidence_links | JSON | NEW | Links to evidence |
| fraud_actions_taken | JSON? | NEW | Fraud actions: account_suspension, property_hide, listing_block, contact_block |
| resolution | String? | NEW | Resolution description |
| resolved_at | String? | NEW | Resolution timestamp |
| created_at | String | NEW | Record creation |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| IncidentType | Enum(9 types) | Incident classification |
| IncidentPriority | Enum(critical, high, normal, low) | Priority levels |
| IncidentStatus | Enum(8 states) | reporting, qualification, analysis, information_gathering, decision, resolution, closure, archiving |
| FraudAction | { type, applied_at, reversed_at } | Fraud mitigation action |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| reporter | User | N:1 | Reporting user |
| assigned_to | User | N:1 | Assigned handler |
| mediation | Mediation | 1:1 | Resulting mediation (if any) |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_inc_type | incident_type, priority | Type-priority queries |
| idx_inc_status | status, created_at | Status queries |
| idx_inc_assigned | assigned_to_user_id, status | Handler caseload |
| idx_inc_target | target_type, target_id | Target lookup |

#### Lifecycle

8 states: reporting → qualification → analysis → information_gathering → decision → resolution → closure → archiving

#### Privacy

SENSITIVE — incident data is confidential

#### Audit

Required for: all status transitions, fraud actions, assignment changes

#### Migration Source

Heritage Gold `incident` workflow

---

### 3.21 AgentInvitation (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | AgentInvitation |
| **domain** | Onboarding |
| **purpose** | Manages the agent invitation and onboarding flow with secure link generation and step tracking |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| organization_id | Int | NEW | FK to Organization |
| invited_by_user_id | Int | NEW | FK to inviting user |
| invitee_email | String | NEW | Invitee email address |
| invitee_phone | String? | NEW | Invitee phone number |
| secure_link_token | String | NEW | Unique secure token |
| secure_link_expires_at | String | NEW | Link expiration |
| status | String | NEW | 7-state lifecycle |
| onboarding_step | String | NEW | Current onboarding step |
| account_created_at | String? | NEW | Account creation timestamp |
| phone_verified_at | String? | NEW | Phone verification timestamp |
| cni_uploaded_at | String? | NEW | CNI upload timestamp |
| validated_at | String? | NEW | LAWIM validation timestamp |
| activated_at | String? | NEW | Agent activation timestamp |
| created_at | String | NEW | Record creation |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| InvitationStatus | Enum(7 states) | invitation_sent, link_clicked, account_created, phone_verified, cni_uploaded, validated, activated |
| OnboardingStep | Enum(6 steps) | Current step in onboarding flow |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| organization | Organization | N:1 | Inviting organization |
| invited_by | User | N:1 | Inviting user |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_ai_org | organization_id, status | Org invitation queries |
| idx_ai_token | secure_link_token | Token lookup |
| idx_ai_status | status, created_at | Status queries |
| idx_ai_email | invitee_email | Email dedup check |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| invitation_token_unique | secure_link_token |
| invitation_email_unique | organization_id, invitee_email |

#### Lifecycle

7 states: invitation_sent → link_clicked → account_created → phone_verified → cni_uploaded → validated → activated

#### Privacy

| Classification | Fields |
|----------------|--------|
| INTERNAL | status, onboarding_step |
| SENSITIVE | invitee_email, invitee_phone, secure_link_token |

#### Audit

Required for: all status transitions, link generation, acceptance

#### Migration Source

Heritage Gold `invitation_agent` workflow

---

### 3.22 IdentityResolution (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | IdentityResolution |
| **domain** | Identity |
| **purpose** | Duplicate user detection and resolution using matching signals and merging workflows |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| user_id_primary | Int | NEW | FK to primary (kept) user |
| user_id_duplicate | Int | NEW | FK to duplicate (merged) user |
| match_confidence | Float | NEW | 0.0-1.0 confidence score |
| match_signals | JSON | NEW | Matched signals: phone, email, name_similarity, device_fingerprint |
| status | String | NEW | 5-state lifecycle |
| resolution_type | String | NEW | merge, false_positive, manual_review_required |
| reviewed_by_user_id | Int? | NEW | FK to reviewing admin |
| reviewed_at | String? | NEW | Review timestamp |
| merged_at | String? | NEW | Merge completion timestamp |
| created_at | String | NEW | Detection timestamp |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| ResolutionStatus | Enum(5 states) | potential_match_detected, confidence_evaluation, human_review, merged, false_positive_discarded |
| MatchSignal | { signal_type, value, confidence } | Individual match signal |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| primary_user | User | N:1 | Primary/kept user |
| duplicate_user | User | N:1 | Duplicate/merged user |
| reviewer | User | N:1 | Reviewing admin |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_ir_primary | user_id_primary, status | Primary user lookups |
| idx_ir_duplicate | user_id_duplicate | Duplicate lookups |
| idx_ir_status | status, match_confidence | Status-confidence queries |
| idx_ir_reviewer | reviewed_by_user_id, status | Reviewer queue |

#### Lifecycle

5 states: potential_match_detected → confidence_evaluation → human_review → merged | false_positive_discarded

#### Privacy

CONFIDENTIAL — identity resolution data is highly sensitive

#### Audit

Required for: all status transitions, merge events, false positive decisions

#### Migration Source

Heritage Gold `resolution_identite` workflow

---

### 3.23 ProfessionalProfile (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | ProfessionalProfile |
| **domain** | Professionals |
| **purpose** | Professional registry for service providers with type classification, verification, and rating |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| user_id | Int | NEW | FK to User |
| professional_type | String | NEW | agent_immobilier, mason, carpenter, painter, tiler, roofer, real_estate_expert, appraiser, condo_manager, drone_videographer, broker, security_guard, admin_service_provider, etc. |
| license_number | String? | NEW | Professional license number |
| years_of_experience | Int? | NEW | Years in profession |
| service_area_zones | JSON | NEW | Geographic service zones |
| rating | Float? | NEW | 1.0-5.0 average rating |
| total_reviews | Int | NEW | Review count |
| verification_status | String | NEW | unverified, pending, verified, rejected |
| verified_at | String? | NEW | Verification timestamp |
| is_available | Boolean | NEW | Available for hire |
| business_hours | JSON? | NEW | Business hours if applicable |
| portfolio_urls | JSON? | NEW | Portfolio links |
| metadata | JSON | NEW | Professional metadata |
| created_at | String | NEW | Record creation |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| ProfessionalType | Enum(extensive) | Type of professional |
| VerificationStatus | Enum(unverified, pending, verified, rejected) | Verification state |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| user | User | 1:1 | User owning this profile |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_pp_type | professional_type, verification_status | Type-verification queries |
| idx_pp_rating | rating, total_reviews | Rating queries |
| idx_pp_available | is_available, service_area_zones | Availability queries |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| prof_profile_user_unique | user_id |

#### Lifecycle

draft → unverified → pending → verified → rejected → suspended

#### Privacy

| Classification | Fields |
|----------------|--------|
| PUBLIC | professional_type, rating, total_reviews, is_available, service_area_zones |
| INTERNAL | verification_status, years_of_experience |
| SENSITIVE | license_number, portfolio_urls |

#### Audit

Required for: verification status changes, rating changes, suspension

#### Migration Source

Heritage Gold `profil_professionnel` table + business profiles

---

### 3.24 FinancingRequest (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | FinancingRequest |
| **domain** | Financing |
| **purpose** | Captures financing qualification data for loan/mortgage pre-qualification requests |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| user_id | Int | NEW | FK to User |
| project_id | Int | NEW | FK to Project |
| property_id | Int? | NEW | FK to Property |
| financing_type | String | NEW | mortgage, personal_loan, construction_loan, bridging_loan |
| requested_amount | Int | NEW | Requested loan amount |
| currency | String | NEW | Default "XAF" |
| monthly_income | Int? | NEW | Applicant monthly income |
| employment_status | String? | NEW | employed, self_employed, unemployed, retired |
| employer_name | String? | NEW | Employer name |
| years_in_employment | Int? | NEW | Years with current employer |
| existing_loans | Int? | NEW | Existing loan obligations |
| credit_score | Int? | NEW | Credit score if available |
| down_payment | Int? | NEW | Available down payment |
| status | String | NEW | draft, submitted, under_review, approved, rejected, conditions_pending, funded |
| reviewed_by_user_id | Int? | NEW | FK to reviewer |
| reviewed_at | String? | NEW | Review timestamp |
| decision_notes | String? | NEW | Underwriting notes |
| created_at | String | NEW | Record creation |
| updated_at | String | NEW | Last update |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| FinancingType | Enum(mortgage, personal_loan, construction_loan, bridging_loan) | Type of financing |
| FinancingStatus | Enum(draft, submitted, under_review, approved, rejected, conditions_pending, funded) | Application lifecycle |
| EmploymentStatus | Enum(employed, self_employed, unemployed, retired) | Employment type |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| user | User | N:1 | Applicant |
| project | Project | N:1 | Related project |
| property | Property | N:1 | Related property |
| reviewer | User | N:1 | Reviewing officer |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_fr_user | user_id, status | User finance requests |
| idx_fr_status | status, financing_type | Status-type queries |
| idx_fr_reviewer | reviewed_by_user_id, status | Reviewer queue |

#### Lifecycle

draft → submitted → under_review → approved | rejected | conditions_pending → funded

#### Privacy

CONFIDENTIAL — financial information is highly sensitive

#### Audit

Required for: all status transitions, amount changes, review decisions

#### Migration Source

Heritage Gold `demande_financement` + 10 financing matrices

---

### 3.25 GeographicUnit (NEW)

| Attribute | Value |
|-----------|-------|
| **entity_name** | GeographicUnit |
| **domain** | Geography |
| **purpose** | Canonical geography reference hierarchy: country, region, department, city, district, neighborhood, zone |
| **existing_or_new** | NEW |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | NEW | Primary key |
| level | String | NEW | country, region, department, city, district, neighborhood, zone |
| code | String | NEW | Geographic code |
| name | String | NEW | Geographic name |
| parent_id | Int? | NEW | FK to parent GeographicUnit |
| latitude | Float? | NEW | Centroid latitude |
| longitude | Float? | NEW | Centroid longitude |
| bounding_box | JSON? | NEW | GeoJSON bounding box |
| timezone | String? | NEW | IANA timezone |
| is_active | Boolean | NEW | Active flag |
| metadata | JSON | NEW | Additional geodata |
| created_at | String | NEW | Record creation |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| GeoLevel | Enum(country, region, department, city, district, neighborhood, zone) | Hierarchy level |
| GeoPoint | { lat, lng } | Geographic point |
| BoundingBox | { sw, ne } | GeoJSON bounding box |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| parent | GeographicUnit | N:1 | Parent unit |
| children | GeographicUnit | 1:N | Child units |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_gu_level | level, code | Level-code queries |
| idx_gu_parent | parent_id | Parent-child lookup |
| idx_gu_name | name, level | Name search |
| idx_gu_active | is_active, level | Active units queries |

#### Uniqueness Constraints

| Constraint | Fields |
|------------|--------|
| geo_unit_code_unique | level, code |

#### Lifecycle

active → inactive

#### Privacy

PUBLIC — geographic data is non-sensitive

#### Audit

Required for: code changes, activation/deactivation

#### Migration Source

Heritage Gold geographic reference data

---

### 3.26 Consent (ENRICH)

| Attribute | Value |
|-----------|-------|
| **entity_name** | Consent |
| **domain** | Relationship |
| **purpose** | Tracks explicit double consent between parties for contact establishment and data sharing |
| **existing_or_new** | ENRICH — extends existing canonical `Consent` concept |

#### Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| id | Int (auto) | Heritage Gold | Primary key |
| **consent_type** | String | **NEW** | contact_sharing, data_sharing, marketing, mediation |
| **granted_by_user_id** | Int | **NEW** | FK to User granting consent |
| **granted_to_user_id** | Int? | **NEW** | FK to User receiving consent |
| **granted_to_organization_id** | Int? | **NEW** | FK to Organization receiving consent |
| **project_id** | Int? | **NEW** | FK to Project context |
| **status** | String | **NEW** | pending, granted, withdrawn, expired |
| **consent_channel** | String | **NEW** | platform, whatsapp, email, sms |
| **granted_at** | String | **NEW** | Consent grant timestamp |
| **expires_at** | String? | **NEW** | Consent expiry |
| **withdrawn_at** | String? | **NEW** | Withdrawal timestamp |
| **purpose_description** | String? | **NEW** | Why consent was requested |
| created_at | String | Heritage Gold | Record creation |

#### Value Objects

| Value Object | Type | Description |
|-------------|------|-------------|
| ConsentType | Enum(contact_sharing, data_sharing, marketing, mediation) | Type of consent |
| ConsentStatus | Enum(pending, granted, withdrawn, expired) | Lifecycle state |
| ConsentChannel | Enum(platform, whatsapp, email, sms) | Channel of consent |

#### Relations

| Relation | Target | Cardinality | Description |
|----------|--------|-------------|-------------|
| granted_by | User | N:1 | Granting user |
| granted_to_user | User | N:1 | Receiving user |
| granted_to_organization | Organization | N:1 | Receiving organization |
| project | Project | N:1 | Related project |

#### Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| idx_consent_granted_by | granted_by_user_id, status | User consent history |
| idx_consent_granted_to | granted_to_user_id, status | Receiving user queries |
| idx_consent_project | project_id, consent_type | Project consent context |
| idx_consent_expiry | expires_at, status | Expiry monitoring |

#### Lifecycle

pending → granted → withdrawn | expired

#### Privacy

SENSITIVE — consent records involve personal data sharing permissions

#### Audit

Required for: grant, withdrawal, expiry events

#### Migration Source

Heritage Gold `consentement` table

---

## 4. Cross-Entity Index Summary

| Entity | New Fields | Value Objects | Relations | Indexes | Uniques |
|--------|-----------|--------------|-----------|---------|---------|
| User | 14 | 4 | 6 new | 4 | 3 |
| Organization | 9 | 4 | 2 new | 3 | 3 |
| OrganizationMember | 8 | 0 | 2 | 3 | 1 |
| Property | 17 | 6 | 3 new | 5 | 1 |
| Project | 6 | 3 | 3 new | 4 | 0 |
| Intent | 14 | 3 | 4 | 4 | 0 |
| Match | 16 | 4 | 1 new | 4 | 1 |
| Visit | 17 | 3 | 5 | 4 | 0 |
| Transaction | 17 | 3 | 2 new | 4 | 0 |
| Service | 12 | 3 | 1 | 3 | 2 |
| ServiceOrder | 15 | 1 | 6 | 4 | 0 |
| Payment | 16 | 2 | 3 | 4 | 0 |
| AgentCredit | 11 | 1 | 2 | 2 | 1 |
| LeadPurchase | 11 | 1 | 4 | 3 | 1 |
| Lead | 24 | 7 | 5 | 6 | 0 |
| Document | 17 | 2 | 2 | 5 | 0 |
| Event | 6 | 2 | 1 | 4 | 0 |
| ApprovalWorkflow | 13 | 3 | 2 | 4 | 0 |
| Mediation | 16 | 2 | 5 | 3 | 0 |
| Incident | 16 | 4 | 2 | 4 | 0 |
| AgentInvitation | 14 | 2 | 2 | 4 | 2 |
| IdentityResolution | 13 | 2 | 3 | 4 | 0 |
| ProfessionalProfile | 17 | 2 | 1 | 3 | 1 |
| FinancingRequest | 17 | 3 | 4 | 3 | 0 |
| GeographicUnit | 11 | 3 | 2 | 4 | 1 |
| Consent | 9 | 3 | 4 | 4 | 0 |

---

## 5. Domain Allocation Summary

| Domain | Count | Entities |
|--------|-------|----------|
| Identity | 3 | User, IdentityResolution, ProfessionalProfile |
| Organizations | 2 | Organization, OrganizationMember |
| Properties | 1 | Property |
| Projects | 1 | Project |
| Intent Detection | 1 | Intent |
| Matching | 1 | Match |
| Visits | 1 | Visit |
| Transactions | 1 | Transaction |
| Services | 2 | Service, ServiceOrder |
| Financial Core | 2 | Payment, AgentCredit |
| CRM | 2 | Lead, LeadPurchase |
| Documents | 1 | Document |
| Permissions | 1 | ApprovalWorkflow |
| Dispute Resolution | 2 | Mediation, Incident |
| Onboarding | 1 | AgentInvitation |
| Financing | 1 | FinancingRequest |
| Geography | 1 | GeographicUnit |
| Relationship | 1 | Consent |
| Audit & Observability | 1 | Event |

---

*End of CANONICAL_DATA_MODEL_EXTENSION.md*
