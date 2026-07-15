# PRISMA EXTENSION BLUEPRINT — Database Schema Extension for LAWIM_V2

**Document ID:** LAWIM-DB-EXT-BLUEPRINT-V1
**Status:** CANONICAL — Schema extension blueprint (DO NOT modify prisma/schema.prisma directly)
**Date:** 2026-07-15
**Extends:** prisma/schema.prisma v19

---

## Table of Contents

1. [Status Summary](#1-status-summary)
2. [Existing Tables to Keep (Unchanged)](#2-existing-tables-to-keep-unchanged)
3. [Existing Tables to Enrich](#3-existing-tables-to-enrich)
4. [New Tables Required](#4-new-tables-required)
5. [Enum Strategy](#5-enum-strategy)
6. [Relations Map (All New Foreign Keys)](#6-relations-map-all-new-foreign-keys)
7. [Index Recommendations](#7-index-recommendations)
8. [Uniqueness Constraints](#8-uniqueness-constraints)
9. [Data Migration Requirements](#9-data-migration-requirements)
10. [Risks & Mitigations](#10-risks--mitigations)
11. [Rollback Plan](#11-rollback-plan)

---

## 1. Status Summary

| Category | Count | Details |
|----------|-------|---------|
| Existing tables kept unchanged | 4 | Media, Notification, Session, Message, SchemaMeta |
| Existing tables enriched | 5 | User, Property, Project, Organization, Event |
| New tables required | 22 | Intent, Match, Visit, Transaction, Service, ServiceOrder, Payment, AgentCredit, LeadPurchase, Lead, Document, ApprovalWorkflow, Mediation, Incident, AgentInvitation, IdentityResolution, ProfessionalProfile, FinancingRequest, GeographicUnit, Contact, Negotiation, Subscription |
| Enums extended | 4 | property status, project type, conversation status, transaction type |
| Enums replaced by reference tables | 2 | property_type → PropertyType lookup, professional_category → ProfessionalCategory lookup |
| New relations (FKs) | ~48+ | Detailed in §6 |
| Indexes recommended | ~35+ | Detailed in §7 |
| Uniqueness constraints | ~18 | Detailed in §8 |
| Data migrations required | 6 | Detailed in §9 |

---

## 2. Existing Tables to Keep (Unchanged)

These tables require NO schema changes. They remain exactly as defined in prisma/schema.prisma v19.

| Table | Model | Reason |
|-------|-------|--------|
| Media | `Media` | Attachments and media storage; sufficient for current needs |
| Notification | `Notification` | User notification system; sufficient |
| Session | `Session` | Auth sessions; sufficient |
| Message | `Message` | Conversation messages; sufficient |
| SchemaMeta | `SchemaMeta` | Schema version tracking; sufficient |
| ProjectStep | `ProjectStep` | Step tracking within projects; extended implicitly via Project enrichment |
| ProjectChecklistItem | `ProjectChecklistItem` | Checklist items; sufficient |
| ProjectStepHistory | `ProjectStepHistory` | Step audit trail; sufficient |

---

## 3. Existing Tables to Enrich

### 3.1 User — Enrichments

| New Field | Type | Attributes | Purpose | Source (Gold) |
|-----------|------|-----------|---------|---------------|
| `trust_level` | Int | default 1, min 1, max 6 | Graduated trust system | GOLD-RL-018–023 |
| `phone_verified` | Boolean | default false | Phone verification flag | GOLD-RL-019 |
| `email_verified` | Boolean | default false | Email verification flag | GOLD-RL-025 |
| `identity_verified` | Boolean | default false | ID document verified | GOLD-RL-020 |
| `professional_docs_verified` | Boolean | default false | Professional docs validated | GOLD-RL-021 |
| `professional_verified` | Boolean | default false | Full professional verification | GOLD-RL-022 |
| `reference_account` | Boolean | default false | Admin-granted reference status | GOLD-RL-023 |
| `owner_verified` | Boolean | default false | Property ownership verified | GOLD-RL-027 |
| `is_active_agent` | Boolean | default false | Fully onboarded active agent | GOLD-RL-031 |
| `onboarding_status` | String | default "invited" | Agent onboarding flow step | EXT-RL-AGENCY-001 |
| `agency_role` | String? | enum: responsible, admin, agent, assistant | Agency hierarchy role | EXT-RL-AGENCY-007 |
| `agent_rating` | Float? | default null, min 1.0, max 5.0 | Post-interaction quality rating | GOLD-RL-040 |
| `last_activity_at` | DateTime? | — | Last user activity timestamp | EXT-MAT-BEHAVIORAL |
| `no_show_count` | Int | default 0 | Missed visit count | EXT-MAT-BEHAVIORAL |

### 3.2 Property — Enrichments

| New Field | Type | Attributes | Purpose | Source (Gold) |
|-----------|------|-----------|---------|---------------|
| `property_family` | String | enum: residential, commercial, industrial, land, agricultural, hotel, project | Classification backbone | EXT-PROP-001 |
| `boost_level` | String? | enum: none, boost_7d, boost_30d | Visibility boost status | EXT-SVC-MON-001/002 |
| `boost_expires_at` | DateTime? | — | Boost expiration | EXT-SVC-MON-001/002 |
| `is_premium` | Boolean | default false | Premium listing flag | EXT-SVC-MON-003 |
| `verification_status` | String? | enum: unverified, pending, verified, rejected | Property verification | EXT-SVC-MON-010 |
| `verified_at` | DateTime? | — | Verification timestamp | EXT-SVC-MON-010 |
| `price_displayed` | Int? | — | Display price (may differ from min/max) | EXT-PROP-006 |
| `price_negotiable` | Boolean | default false | Price negotiable flag | EXT-PROP-006 |
| `price_negotiable_min` | Int? | — | Minimum negotiable price | EXT-PROP-006 |
| `price_historical` | JSON? | default "[]" | Historical price changes | EXT-PROP-006 |
| `data_quality_score` | Int? | default null, 0-100 | Quality score for listing | EXT-PROP-008 |
| `data_quality_grade` | String? | enum: A+, A, B, C, D | Quality grade | EXT-PROP-008 |
| `auto_archive_at` | DateTime? | — | Scheduled auto-archive (90d inactivity) | EXT-PROP-011 |
| `publish_status` | String | default "draft" | Extended publication state machine | EXT-PROP-004 |
| `matched_count` | Int | default 0 | Number of times matched | EXT-MAT |
| `view_count` | Int | default 0 | Listing view count | EXT-MAT |

### 3.3 Project — Enrichments

| New Field | Type | Attributes | Purpose | Source (Gold) |
|-----------|------|-----------|---------|---------------|
| `business_role` | String? | enum: buyer, seller, tenant, investor, visitor, client | Intent-derived role | EXT-INT-006 |
| `urgency_score` | Float? | default null, 0.0-1.0 | Detected urgency | EXT-INT-004 |
| `urgency_level` | String? | enum: low, medium, high, urgent | Urgency classification | EXT-INT-004 |
| `journey_stage` | String | default "discovery" | Current funnel stage | EXT-WF-014 |
| `multi_intent_group_id` | String? | UUID | Multi-intent group linkage | EXT-INT-003 |
| `matching_status` | String? | enum: not_started, active, proposed, failed, completed | Matching state | EXT-MAT-001 |
| `rematch_count` | Int | default 0 | Rematching cycles | EXT-MAT-005 |
| `dossier_health_score` | Int? | default null, 0-100 | Dossier quality score | EXT-MAT-009 |

### 3.4 Organization — Enrichments

| New Field | Type | Attributes | Purpose | Source (Gold) |
|-----------|------|-----------|---------|---------------|
| `agency_verified` | Boolean | default false | Agency registration verified | GOLD-RL-028 |
| `trust_level` | Int? | default null, 1-6 | Agency-level trust | EXT-RL-AGENCY-008 |
| `rccm` | String? | — | Business registration number | EXT-RL-AGENCY-009 |
| `tax_id` | String? | — | Tax identification number | EXT-RL-AGENCY-009 |
| `cni_document` | String? | — | CNI document reference | EXT-RL-AGENCY-009 |
| `operational_status` | String | default "pending" | Agency operational status | EXT-RL-AGENCY-002 |
| `agent_count_min` | Int | default 3 | Minimum agents for operational status | EXT-RL-AGENCY-002 |

### 3.5 Event — Enrichment

| New Field | Type | Attributes | Purpose |
|-----------|------|-----------|---------|
| `entity_type` | String? | — | Polymorphic entity type reference |
| `entity_id` | String? | — | Polymorphic entity ID reference |
| `actor_id` | Int? | — | Who triggered the event |
| `severity` | String? | enum: info, warning, error, critical | Event severity |

### 3.6 Conversation — Enrichment

| New Field | Type | Attributes | Purpose |
|-----------|------|-----------|---------|
| `conversation_type` | String? | enum: inquiry, negotiation, support, mediation | Conversation classification |
| `match_id` | Int? | FK → Match | Link to originating match |
| `transaction_id` | Int? | FK → Transaction | Link to active transaction |

---

## 4. New Tables Required

### 4.1 Intent

Proposed Prisma model for detected user intents from NLP/keyword pipeline.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `user_id` | Int | required | FK → User |
| `source_text` | String | required | Original user utterance |
| `language` | String | required | fr, en, pid |
| `primary_intent` | String | required | buy, rent, sell, invest, search_property, find_professional, service, finance, other |
| `confidence` | Float | required | 0.0-1.0 |
| `threshold` | Float | default 0.70 | Configurable threshold |
| `is_multi_intent` | Boolean | default false | Multi-intent flag |
| `sub_intents` | String | default "[]" | JSON array of sub-intents |
| `urgency_score` | Float? | 0.0-1.0 | Urgency level |
| `urgency_level` | String? | low, medium, high, urgent | Urgency classification |
| `extracted_entities` | String | default "{}" | JSON of extracted entities |
| `detection_method` | String | default "keyword" | keyword, explicit_selection, hybrid |
| `keyword_scores` | String | default "{}" | Per-keyword contribution |
| `project_type_mapping` | String? | — | Mapped project type |
| `session_id` | String? | — | Chat session ID |
| `source_channel` | String | default "api" | whatsapp, telegram, dashboard, api |
| `project_id` | Int? | FK → Project | Optional link to created project |
| `created_at` | DateTime | @map("created_at") | Creation timestamp |

**Relations:**
- `user` → User (N:1)
- `project` → Project (0:1)
- `service_requests` → ServiceRequest (1:N)

**Indexes:**
- `[@index([user_id, created_at])]` — User intent history
- `[@index([primary_intent, confidence])]` — Intent classification queries
- `[@index([session_id])]` — Session lookup

**Migration Source:** EXT-INT-001–006, INTENT_MODEL.md (Gold)

---

### 4.2 Match

Proposed Prisma model for property-demandeur matching results.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `project_id` | Int | required | FK → Project |
| `property_id` | Int | required | FK → Property |
| `agent_id` | Int? | FK → User | Assigned agent |
| `overall_score` | Float | required | 0-100 composite score |
| `compatibility_level` | String | required | excellent, good, average, low |
| `rank` | Int | required | Ranking position |
| `is_active` | Boolean | default true | Active match flag |
| `is_proposed` | Boolean | default false | Proposed to demandeur |
| `demandeur_decision` | String? | pending, interested, not_interested | Demandeur response |
| `holder_decision` | String? | pending, favorable, refused | Holder response |
| `decision_deadline` | DateTime? | — | Decision deadline |
| `rematch_count` | Int | default 0 | Rematch cycles |
| `rematch_reason` | String? | — | Why rematched |
| `match_pool` | String | default "primary" | primary, expansion_geo, expansion_budget, expansion_type |
| `score_breakdown` | String | default "{}" | JSON of per-dimension scores |
| `expires_at` | DateTime? | — | Match expiration |
| `proposed_at` | DateTime? | — | When proposed |
| `demandeur_decided_at` | DateTime? | — | Demandeur decision time |
| `holder_decided_at` | DateTime? | — | Holder decision time |
| `created_at` | DateTime | @map("created_at") | Creation timestamp |

**Relations:**
- `project` → Project (N:1)
- `property` → Property (N:1)
- `agent` → User (N:1)
- `contact` → Contact (0:1)
- `visits` → Visit (1:N)
- `negotiation` → Negotiation (0:1)

**Indexes:**
- `[@index([project_id, overall_score])]` — Per-project match ranking
- `[@index([property_id, is_active])]` — Active property matches
- `[@index([agent_id, created_at])]` — Agent match history
- `[@index([overall_score, compatibility_level])]` — Score-based queries
- `[@index([expires_at, is_active])]` — Expiration sweep

**Uniqueness:** `@@unique([project_id, property_id, match_pool])` — One match per pair per pool

**Migration Source:** EXT-MAT-001–013, SEARCH_MATCHING_EXTENSION_MODEL.md

---

### 4.3 Visit

Proposed Prisma model for property visit scheduling.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `match_id` | Int | required | FK → Match |
| `property_id` | Int | required | FK → Property |
| `demandeur_id` | Int | required | FK → User (visitor) |
| `holder_id` | Int | required | FK → User (owner/agent) |
| `agent_id` | Int? | FK → User (accompanying agent) |
| `scheduled_at` | DateTime | required | Planned visit time |
| `status` | String | required | See state machine |
| `visit_type` | String | default "first_visit" | first_visit, contre_visite |
| `absence_type` | String? | demandeur_no_show, holder_no_show | No-show tracking |
| `cancellation_reason` | String? | — | Why cancelled |
| `satisfaction_level` | String? | tres_satisfait, mitige, insatisfait | Post-visit feedback |
| `notes` | String? | — | Visit notes |
| `reminder_24h_sent` | Boolean | default false | 24h reminder sent |
| `reminder_2h_sent` | Boolean | default false | 2h reminder sent |
| `created_at` | DateTime | @map("created_at") | Creation timestamp |
| `confirmed_at` | DateTime? | — | Confirmation time |
| `completed_at` | DateTime? | — | Completion time |

**Relations:**
- `match` → Match (N:1)
- `property` → Property (N:1)
- `demandeur` → User (N:1)
- `holder` → User (N:1)
- `agent` → User? (N:1)

**Indexes:**
- `[@index([property_id, scheduled_at])]` — Property visit schedule
- `[@index([demandeur_id, status])]` — User visit history
- `[@index([holder_id, status])]` — Holder visit management
- `[@index([scheduled_at, status])]` — Upcoming visits
- `[@index([match_id])]` — Match visit lookup

**Migration Source:** EXT-WF-003, Visit Lifecycle (9 states), Heritage Gold WORKFLOW_03

---

### 4.4 Transaction

Proposed Prisma model for deal-closing entity.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `project_id` | Int? | FK → Project | Originating project |
| `property_id` | Int | required | FK → Property |
| `match_id` | Int? | FK → Match | Originating match |
| `transaction_type` | String | required | See transaction types |
| `status` | String | required | 7-state lifecycle |
| `demandeur_id` | Int | required | FK → User (buyer/tenant) |
| `holder_id` | Int | required | FK → User (seller/owner) |
| `agent_id` | Int? | FK → User (managing agent) |
| `notaire_id` | Int? | FK → User (notary) |
| `price_agreed` | Decimal? | @map("price_agreed") | Agreed price |
| `currency` | String | default "XAF" | Currency |
| `payment_milestones` | String | default "[]" | JSON array of milestones |
| `negotiation_id` | Int? | FK → Negotiation | Link to negotiation |
| `signature_demandeur_at` | DateTime? | — | Demandeur signed |
| `signature_holder_at` | DateTime? | — | Holder signed |
| `handover_at` | DateTime? | — | Key handover |
| `completed_at` | DateTime? | — | Completion |
| `failed_at` | DateTime? | — | Failure time |
| `failure_reason` | String? | — | Why failed |
| `follow_up_at` | DateTime? | — | Post-completion follow-up |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `project` → Project (0:1)
- `property` → Property (N:1)
- `match` → Match (0:1)
- `demandeur` → User (N:1)
- `holder` → User (N:1)
- `agent` → User? (N:1)
- `notaire` → User? (N:1)
- `negotiation` → Negotiation (0:1)
- `documents` → Document (1:N)

**Indexes:**
- `[@index([property_id, status])]` — Property transaction status
- `[@index([demandeur_id, status])]` — User transaction history
- `[@index([holder_id, status])]` — Holder transaction view
- `[@index([transaction_type, status])]` — Type-based aggregation
- `[@index([created_at])]` — Chronological queries

**Migration Source:** EXT-WF-004, INTENT_REQUEST_TRANSACTION_MODEL.md

---

### 4.5 Contact

Proposed Prisma model for double-consent contact establishment.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `match_id` | Int | required | FK → Match |
| `demandeur_id` | Int | required | FK → User |
| `holder_id` | Int | required | FK → User |
| `status` | String | required | 6-state lifecycle |
| `demandeur_consented` | Boolean | default false | Demandeur consent |
| `holder_consented` | Boolean | default false | Holder consent |
| `consent_demandeur_at` | DateTime? | — | When demandeur consented |
| `consent_holder_at` | DateTime? | — | When holder consented |
| `silence_reminder_count` | Int | default 0 | Holder silence reminders |
| `established_at` | DateTime? | — | Double consent obtained |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `match` → Match (N:1)
- `demandeur` → User (N:1)
- `holder` → User (N:1)

**Uniqueness:** `@@unique([match_id])` — One contact per match

**Migration Source:** EXT-WF-002, Mise en Relation / Contact Lifecycle

---

### 4.6 Negotiation

Proposed Prisma model for offer/counter-offer tracking.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `transaction_id` | Int? | FK → Transaction | Parent transaction |
| `match_id` | Int? | FK → Match | Parent match |
| `status` | String | required | 9-state lifecycle |
| `current_offer_amount` | Decimal? | — | Latest offer |
| `price_gap_percentage` | Float? | — | Gap from asking price |
| `reminders_sent` | Int | default 0 | Silence reminders |
| `failure_reason` | String? | — | Why failed |
| `created_at` | DateTime | @map("created_at") | Creation |
| `last_activity_at` | DateTime | — | Last activity |

**Relations:**
- `transaction` → Transaction (0:1)
- `match` → Match (0:1)

**Indexes:**
- `[@index([transaction_id])]` — Transaction negotiation
- `[@index([match_id])]` — Match negotiation

**Migration Source:** INTENT_REQUEST_TRANSACTION_MODEL.md §12

---

### 4.7 Service

Proposed Prisma model for service catalog.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `service_code` | String | @unique | Unique service identifier |
| `name` | String | required | Display name |
| `description` | String? | — | Service description |
| `category` | String | required | monetized, real_estate, professional, crm |
| `service_type` | String | required | boost, premium, subscription, lead_pack, accompaniment, etc. |
| `base_price` | Int | required | Price in FCFA |
| `currency` | String | default "XAF" | Currency |
| `duration_days` | Int? | — | Service duration |
| `is_recurring` | Boolean | default false | Subscription flag |
| `is_active` | Boolean | default true | Available for purchase |
| `metadata_json` | String | default "{}" | Flexible attributes |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `service_orders` → ServiceOrder (1:N)

**Migration Source:** EXT-SVC-MON-001–013, EXT-SVC-RES-001–024, SERVICE_TAXONOMY_EXTENSION_MODEL.md

---

### 4.8 ServiceOrder

Proposed Prisma model for service purchase/fulfillment.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `service_id` | Int | required | FK → Service |
| `user_id` | Int | required | FK → User (buyer) |
| `organization_id` | Int? | FK → Organization (buyer org) |
| `property_id` | Int? | FK → Property (linked listing) |
| `status` | String | required | 8-state lifecycle |
| `price_paid` | Int | required | Actual price paid |
| `currency` | String | default "XAF" | Currency |
| `quantity` | Int | default 1 | Service units |
| `activated_at` | DateTime? | — | Service activation |
| `expires_at` | DateTime? | — | Service expiration |
| `cancelled_at` | DateTime? | — | Cancellation time |
| `cancellation_reason` | String? | — | Why cancelled |
| `metadata_json` | String | default "{}" | Flexible attributes |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `service` → Service (N:1)
- `user` → User (N:1)
- `organization` → Organization? (N:1)
- `property` → Property? (N:1)
- `payments` → Payment (1:N)

**Indexes:**
- `[@index([user_id, status])]` — User order history
- `[@index([service_id, status])]` — Service fulfillment
- `[@index([expires_at, status])]` — Expiration sweep

**Migration Source:** EXT-SVC-LIFE-001, Service Lifecycle (8 states)

---

### 4.9 Payment

Proposed Prisma model for payment processing.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `service_order_id` | Int? | FK → ServiceOrder | Parent order |
| `transaction_id` | Int? | FK → Transaction | Parent transaction |
| `user_id` | Int | required | FK → User (payer) |
| `amount` | Int | required | Amount in FCFA |
| `currency` | String | default "XAF" | Currency |
| `status` | String | required | 10-state sub-machine |
| `payment_method` | String? | campay, orange_money, mobile_money, card, bank_transfer |
| `provider_reference` | String? | — | Campay/3rd-party ref |
| `provider_payload` | String | default "{}" | Provider response data |
| `payment_type` | String | required | service_payment, lead_purchase, credit_topup, transaction_deposit |
| `failure_reason` | String? | — | Why payment failed |
| `refunded_at` | DateTime? | — | Refund timestamp |
| `reconciled_at` | DateTime? | — | Reconciliation |
| `disputed_at` | DateTime? | — | Dispute start |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `service_order` → ServiceOrder? (N:1)
- `transaction` → Transaction? (N:1)
- `user` → User (N:1)

**Indexes:**
- `[@index([user_id, status])]` — User payment history
- `[@index([service_order_id])]` — Order payments
- `[@index([transaction_id])]` — Transaction payments
- `[@index([provider_reference])]` — Provider reconciliation
- `[@index([created_at, status])]` — Reconciliation sweep

**Migration Source:** EXT-SVC-LIFE-002, Payment Sub-states (10 states), Campay integration

---

### 4.10 AgentCredit

Proposed Prisma model for agent credit/boost system.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `user_id` | Int | @unique? | FK → User (agent) |
| `credits` | Int | default 0 | Available credits |
| `total_earned` | Int | default 0 | Lifetime credits earned |
| `total_spent` | Int | default 0 | Lifetime credits spent |
| `last_recharge_at` | DateTime? | — | Last top-up |
| `created_at` | DateTime | @map("created_at") | Creation |
| `updated_at` | DateTime | @map("updated_at") | Last update |

**Relations:**
- `user` → User (N:1)
- `purchases` → LeadPurchase (1:N)

**Uniqueness:** `@@unique([user_id])` — One credit balance per agent

**Migration Source:** EXT-RL-AGENCY-005, Agent credits & boosts

---

### 4.11 LeadPurchase

Proposed Prisma model for pay-per-connection lead buying.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `agent_id` | Int | required | FK → User (buying agent) |
| `lead_id` | Int | required | FK → Lead (purchased lead) |
| `pack_type` | String | required | lead_bronze, lead_silver, lead_gold, deblocage_coordonnees |
| `price_paid` | Int | required | Cost in FCFA |
| `payment_id` | Int? | FK → Payment | Payment reference |
| `status` | String | default "completed" | Purchase status |
| `contacts_revealed` | Boolean | default false | Contact info unlocked |
| `revealed_at` | DateTime? | — | When contacts shown |
| `created_at` | DateTime | @map("created_at") | Purchase time |

**Relations:**
- `agent` → User (N:1)
- `lead` → Lead (N:1)
- `payment` → Payment? (N:1)

**Uniqueness:** `@@unique([agent_id, lead_id])` — One purchase per lead per agent

**Migration Source:** EXT-SVC-CRM-001–004, EXT-RL-AGENCY-004

---

### 4.12 Lead

Proposed Prisma model for CRM lead management.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `user_id` | Int? | FK → User (if known) |
| `source_channel` | String | required | whatsapp, telegram, dashboard, api, referral |
| `source_text` | String? | — | Original message |
| `normalized_text` | String? | — | Normalized text |
| `language` | String | default "fr" | fr, en, pid |
| `pipeline_stage` | String | required | 8-stage pipeline |
| `detected_intent` | String? | — | Primary intent |
| `intent_confidence` | Float? | — | 0.0-1.0 |
| `lead_type` | String? | tenant, buyer, seller, investor, diaspora_investor |
| `base_score` | Int | default 0 | Base score by type |
| `boosters_applied` | String | default "[]" | JSON booster array |
| `penalties_applied` | String | default "[]" | JSON penalty array |
| `total_boost` | Int | default 0 | Sum boosters |
| `total_penalty` | Int | default 0 | Sum penalties |
| `final_score` | Int | default 0 | Composite score |
| `classification` | String? | hot, warm, cold, low, spam |
| `routed_to_agent_id` | Int? | FK → User | Assigned agent |
| `routed_at` | DateTime? | — | Assignment time |
| `routed_zone` | String? | — | Geographic zone |
| `sla_deadline` | DateTime? | — | Response SLA deadline |
| `sla_breached` | Boolean | default false | SLA breach flag |
| `contact_id` | Int? | FK → User | Matched existing user |
| `conversation_id` | Int? | FK → Conversation | Linked conversation |
| `assigned_project_id` | Int? | FK → Project | Created project |
| `is_purchased` | Boolean | default false | Lead bought by agent |
| `fraud_flags` | String | default "[]" | JSON fraud flags |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `user` → User? (N:1)
- `routed_agent` → User? (N:1)
- `conversation` → Conversation? (N:1)
- `project` → Project? (N:1)
- `purchases` → LeadPurchase (1:N)

**Indexes:**
- `[@index([pipeline_stage, classification])]` — Pipeline query
- `[@index([final_score, classification])]` — Scoring queries
- `[@index([routed_to_agent_id, created_at])]` — Agent lead history
- `[@index([source_channel, created_at])]` — Channel analytics
- `[@index([sla_deadline, sla_breached])]` — SLA monitoring
- `[@index([created_at])]` — Chronological queries

**Migration Source:** EXT-CRM-001–011, CRM_EXTENSION_MODEL.md

---

### 4.13 Document

Proposed Prisma model for document management across entities.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `user_id` | Int | required | FK → User (uploader) |
| `entity_type` | String | required | Polymorphic: transaction, property, user, project |
| `entity_id` | Int | required | FK to respective entity |
| `document_type` | String | required | See document type enum |
| `filename` | String | required | Original filename |
| `storage_path` | String | required | Storage URI |
| `mime_type` | String? | — | File MIME type |
| `size_bytes` | Int? | — | File size |
| `status` | String | default "pending" | pending, validated, rejected |
| `validated_by` | Int? | FK → User (validator) |
| `validated_at` | DateTime? | — | Validation time |
| `rejection_reason` | String? | — | Why rejected |
| `expires_at` | DateTime? | — | Document expiry |
| `created_at` | DateTime | @map("created_at") | Upload time |

**Relations:**
- `user` → User (N:1)
- `validator` → User? (N:1)

**Indexes:**
- `[@index([entity_type, entity_id])]` — Polymorphic lookup
- `[@index([user_id, document_type])]` — User document by type
- `[@index([status, entity_type])]` — Validation sweep
- `[@index([expires_at])]` — Expiry sweep

**Migration Source:** EXT-WF-004 §13, Document Requirements Per Transaction Type

---

### 4.14 ApprovalWorkflow

Proposed Prisma model for approval/review workflows.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `target_type` | String | required | Polymorphic: user, property, organization, document |
| `target_id` | Int | required | FK to respective entity |
| `workflow_type` | String | required | verification, validation, onboarding, publication |
| `status` | String | required | pending, approved, rejected, cancelled |
| `requested_by` | Int | required | FK → User (requester) |
| `reviewed_by` | Int? | FK → User (reviewer) |
| `reviewed_at` | DateTime? | — | Review time |
| `rejection_reason` | String? | — | Why rejected |
| `notes` | String? | — | Internal notes |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `requester` → User (N:1)
- `reviewer` → User? (N:1)

**Indexes:**
- `[@index([target_type, target_id])]` — Polymorphic lookup
- `[@index([status, workflow_type])]` — Pending approvals
- `[@index([reviewed_by, status])]` — Reviewer workload

**Migration Source:** EXT-PERM-001, Approval Workflow

---

### 4.15 Incident

Proposed Prisma model for dispute/incident reporting.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `reporter_id` | Int | required | FK → User |
| `entity_type` | String | required | Polymorphic |
| `entity_id` | Int | required | FK to respective entity |
| `incident_type` | String | required | See 12 incident types |
| `priority` | String | required | critique, elevee, normale, faible |
| `status` | String | required | 8-state lifecycle |
| `description` | String | required | Incident details |
| `resolution` | String? | — | Resolution notes |
| `fraud_action_taken` | String? | suspension, warning, none |
| `fraud_action_detail` | String? | — | What was suspended |
| `assigned_to` | Int? | FK → User | Assigned handler |
| `resolved_by` | Int? | FK → User | Resolver |
| `resolved_at` | DateTime? | — | Resolution time |
| `escalated_at` | DateTime? | — | Escalation time |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `reporter` → User (N:1)
- `assignee` → User? (N:1)
- `resolver` → User? (N:1)

**Indexes:**
- `[@index([entity_type, entity_id])]` — Entity incidents
- `[@index([status, priority])]` — Priority queue
- `[@index([assigned_to, status])]` — Handler workload

**Migration Source:** EXT-WF-006, Disputes, Claims & Incidents Lifecycle (8 states)

---

### 4.16 Mediation

Proposed Prisma model for mediation workflow.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `incident_id` | Int? | FK → Incident | Source incident |
| `transaction_id` | Int? | FK → Transaction | Source transaction |
| `demandeur_id` | Int | required | FK → User |
| `holder_id` | Int | required | FK → User |
| `mediator_id` | Int? | FK → User (assigned mediator) |
| `status` | String | required | 8-state lifecycle |
| `proposed_by` | String? | system, demandeur, holder, agent |
| `proposed_at` | DateTime? | — | Proposal time |
| `accepted_demandeur_at` | DateTime? | — | Demandeur acceptance |
| `accepted_holder_at` | DateTime? | — | Holder acceptance |
| `solution_proposed` | String? | — | Mediator solution |
| `solution_accepted` | Boolean? | — | Solution accepted |
| `resolution_notes` | String? | — | Final resolution |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `incident` → Incident? (N:1)
- `transaction` → Transaction? (N:1)
- `demandeur` → User (N:1)
- `holder` → User (N:1)
- `mediator` → User? (N:1)

**Indexes:**
- `[@index([incident_id])]` — Incident mediation
- `[@index([mediator_id, status])]` — Mediator caseload

**Migration Source:** EXT-WF-007, Mediation Workflow (8 states)

---

### 4.17 AgentInvitation

Proposed Prisma model for structured agent onboarding.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `organization_id` | Int | required | FK → Organization |
| `invited_by` | Int | required | FK → User (inviting admin) |
| `invited_email` | String | required | Email of invitee |
| `invited_phone` | String? | — | Phone of invitee |
| `secure_token` | String | @unique | Invitation link token |
| `status` | String | required | 7-state lifecycle |
| `expires_at` | DateTime | required | Link expiry |
| `accepted_at` | DateTime? | — | Account creation |
| `created_user_id` | Int? | FK → User (created account) |
| `onboarding_step` | String | default "account_created" | Current onboarding step |
| `reminder_count` | Int | default 0 | Reminder count |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `organization` → Organization (N:1)
- `inviter` → User (N:1)
- `created_user` → User? (N:1)

**Indexes:**
- `[@index([organization_id, status])]` — Org invitations
- `[@index([secure_token])]` — Token lookup
- `[@index([expires_at, status])]` — Expiry sweep

**Migration Source:** EXT-WF-012, Agent Invitation Workflow (7 states)

---

### 4.18 IdentityResolution

Proposed Prisma model for duplicate user detection/merging.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `primary_user_id` | Int | required | FK → User (survivor) |
| `duplicate_user_id` | Int | required | FK → User (to merge) |
| `match_signals` | String | required | JSON: phone, email, name, device |
| `confidence_score` | Float | required | 0.0-1.0 |
| `status` | String | required | 5-state lifecycle |
| `reviewed_by` | Int? | FK → User (human reviewer) |
| `reviewed_at` | DateTime? | — | Review time |
| `resolution` | String? | merged, false_positive |
| `merged_at` | DateTime? | — | Merge time |
| `created_at` | DateTime | @map("created_at") | Detection time |

**Relations:**
- `primary_user` → User (N:1)
- `duplicate_user` → User (N:1)
- `reviewer` → User? (N:1)

**Uniqueness:** `@@unique([primary_user_id, duplicate_user_id])`

**Migration Source:** EXT-WF-013, Identity Resolution Workflow (5 states)

---

### 4.19 ProfessionalProfile

Proposed Prisma model for professional service providers.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `user_id` | Int | @unique | FK → User |
| `professional_type` | String | required | Primary category |
| `secondary_types` | String | default "[]" | JSON array |
| `professional_name` | String? | — | Business name |
| `professional_email` | String? | — | Professional email |
| `professional_phone` | String? | — | Professional phone |
| `business_address` | String? | — | Registered address |
| `website` | String? | — | Website URL |
| `social_links` | String | default "{}" | JSON social profiles |
| `bio` | String? | — | Professional summary |
| `years_experience` | Int | default 0 | Years of experience |
| `employee_count` | Int? | — | Number of employees |
| `professional_status` | String | default "active" | active, inactive, suspended, archived |
| `is_verified` | Boolean | default false | Verification status |
| `verification_doc_ref` | String? | — | Verification document |
| `license_number` | String? | — | Professional license |
| `license_expires_at` | DateTime? | — | License expiry |
| `insurance_proof` | String? | — | Insurance document ref |
| `coverage_zones` | String | default "[]" | JSON geographic zones |
| `pricing_model` | String? | fixed, hourly, per_project, negotiable |
| `pricing_min` | Int? | — | Min service price |
| `pricing_max` | Int? | — | Max service price |
| `rating` | Float? | default null, 1.0-5.0 | Aggregate rating |
| `rating_count` | Int | default 0 | Number of ratings |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `user` → User (1:1)

**Indexes:**
- `[@index([professional_type, is_verified])]` — Professional directory
- `[@index([professional_status])]` — Status sweep

**Migration Source:** EXT-SVC-PRO-001–012, PROFESSIONAL_EXTENSION_MODEL.md

---

### 4.20 FinancingRequest

Proposed Prisma model for financing qualification.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `user_id` | Int | required | FK → User (applicant) |
| `project_id` | Int? | FK → Project | Linked project |
| `status` | String | required | draft, submitted, under_review, approved, rejected, disbursed |
| `loan_amount` | Int | required | Requested amount |
| `currency` | String | default "XAF" | Currency |
| `loan_purpose` | String? | — | Purpose of loan |
| `monthly_income` | Int? | — | Applicant income |
| `existing_commitments` | Int? | — | Existing debt |
| `collateral_description` | String? | — | Collateral details |
| `partner_bank` | String? | — | Partner bank ref |
| `credit_score` | Int? | — | Internal credit score |
| `submitted_at` | DateTime? | — | Submission time |
| `decision_at` | DateTime? | — | Decision time |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `user` → User (N:1)
- `project` → Project? (N:1)

**Migration Source:** EXT-TRX-006, Financing Request, EXT-QUAL-005

---

### 4.21 GeographicUnit

Proposed Prisma model for geographic reference data.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `code` | String | @unique | Geo code |
| `name` | String | required | Display name |
| `level` | String | required | country, region, department, city, neighborhood, zone |
| `parent_id` | Int? | FK → GeographicUnit | Hierarchical parent |
| `latitude` | Float? | — | Center latitude |
| `longitude` | Float? | — | Center longitude |
| `bounding_box` | String? | — | JSON bounding box |
| `aliases` | String | default "[]" | JSON alternate names |
| `is_active` | Boolean | default true | Active flag |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `parent` → GeographicUnit? (N:1)
- `children` → GeographicUnit (1:N)

**Indexes:**
- `[@index([level, parent_id])]` — Hierarchy navigation
- `[@index([parent_id])]` — Children lookup
- `[@index([level])]` — Level-based queries
- `[@index([name])]` — Name search

**Migration Source:** EXT-MAT-003, Geographic Scoring, GEOGRAPHY_MODEL.md (Gold)

---

### 4.22 Subscription

Proposed Prisma model for agent subscriptions.

| Field | Type | Attributes | Purpose |
|-------|------|-----------|---------|
| `id` | Int | @id @default(autoincrement()) | Primary key |
| `user_id` | Int | required | FK → User (subscriber) |
| `organization_id` | Int? | FK → Organization (org subscription) |
| `subscription_type` | String | required | agent_pro, agent_business |
| `status` | String | required | active, cancelled, expired, past_due |
| `price` | Int | required | Price per cycle |
| `currency` | String | default "XAF" | Currency |
| `billing_cycle` | String | default "monthly" | monthly, yearly |
| `current_period_start` | DateTime | required | Billing period start |
| `current_period_end` | DateTime | required | Billing period end |
| `cancelled_at` | DateTime? | — | Cancellation time |
| `created_at` | DateTime | @map("created_at") | Creation |

**Relations:**
- `user` → User (N:1)
- `organization` → Organization? (N:1)

**Indexes:**
- `[@index([user_id, status])]` — User subscriptions
- `[@index([current_period_end, status])]` — Renewal sweep

**Migration Source:** EXT-SVC-MON-004, EXT-SVC-CRM-009

---

## 5. Enum Strategy

### 5.1 Enums to Extend (Add Values to Existing String Fields)

| Field | Current Values | New Values | Impact |
|-------|---------------|------------|--------|
| `Property.status` | draft, published, sold, rented, archived | `pending_validation`, `suspended`, `maintenance` | Add values; existing code must handle new values |
| `Property.availability` | available, pending, sold, rented, archived | `reserved`, `under_negotiation` | Add values |
| `Project.project_type` | buy, rent, sell, invest, find, service, finance, other | `short_stay`, `lease`, `bail_commercial` | Add 3 new transaction types |
| `Project.status` | draft, active, paused, completed, archived, cancelled | `qualifying`, `matching`, `negotiating` | Add journey-aligned states |
| `Conversation.status` | active, pending, closed, archived | `negotiating`, `mediated`, `escalated` | Add conversation sub-types |
| `Conversation.negotiation_stage` | inquiry, visit, offer, negotiation, closing, completed | `mediation`, `incident`, `follow_up` | Add post-completion stages |
| `User.role` | user, operator, manager, admin | (no new roles, but add validation) | Keep existing; add `agency_role` separately |

### 5.2 Enums to Replace with Reference Tables

| Current String Field | Reference Table | Values |
|---------------------|----------------|--------|
| `Property.property_type` | `PropertyType` | residential.apartment, residential.villa, residential.house, residential.studio, residential.duplex, commercial.office, commercial.shop, commercial.warehouse, industrial.factory, industrial.warehouse, land.residential, land.agricultural, land.commercial, agricultural.farm, agricultural.plantation, hotel.hotel, hotel.guest_house, project.construction, project.renovation |
| `ProfessionalProfile.professional_type` | `ProfessionalCategory` | agent_immobilier, notaire, geometre, architecte, avocat, expert_immobilier, evaluateur, macon, menuisier, peintre, carreleur, couvreur, syndic, courtier, gardiennage, prestataire_administratif, constructeur, drone_operator, photographer, insurance_broker, tax_advisor, legal_advisor, renovation_contractor, moving_service, cleaning_service, security_service |
| `Service.category` | `ServiceCategory` | monetized, real_estate, professional, crm |
| `GeographicUnit.level` | `GeoLevel` | country, region, department, city, neighborhood, zone |

### 5.3 New Enums (String-Based for Prisma Compatibility)

| Field | Values |
|-------|--------|
| `Property.property_family` | residential, commercial, industrial, land, agricultural, hotel, project |
| `Property.publish_status` | draft, pending_validation, validated, published, suspended, archived |
| `Property.verification_status` | unverified, pending, verified, rejected |
| `Property.boost_level` | none, boost_7d, boost_30d |
| `User.trust_level` | 1, 2, 3, 4, 5, 6 (Int) |
| `User.agency_role` | responsible, admin, agent, assistant |
| `User.onboarding_status` | invited, account_created, phone_verified, cni_uploaded, validated, active |
| `Project.business_role` | buyer, seller, tenant, investor, visitor, client |
| `Project.urgency_level` | low, medium, high, urgent |
| `Project.journey_stage` | discovery, qualification, matching, presentation, contact, visit, negotiation, transaction, completed |
| `Project.matching_status` | not_started, active, proposed, failed, completed |
| `Match.compatibility_level` | excellent, good, average, low |
| `Match.demandeur_decision` | pending, interested, not_interested |
| `Match.holder_decision` | pending, favorable, refused |
| `Match.match_pool` | primary, expansion_geo, expansion_budget, expansion_type |
| `Visit.status` | requested, pending_confirmation, confirmed, rescheduled, cancelled, completed, refused, absence_demandeur, absence_holder |
| `Visit.visit_type` | first_visit, contre_visite |
| `Transaction.status` | agreement, preparation, documents, payment, signature, handover, completed, failed, archived |
| `Transaction.transaction_type` | sale, rental, short_stay, lease, bail_commercial, cession_bail, cession, finance, find, service |
| `ServiceOrder.status` | created, proposed, accepted, paid, activated, used, expired, archived |
| `Payment.status` | created, initiated, pending, confirmed, failed, cancelled, expired, refunded, reconciled, disputed |
| `Lead.pipeline_stage` | incoming, normalized, extracted, intent_detected, enriched, scored, classified, routed |
| `Lead.classification` | hot, warm, cold, low, spam |
| `Document.status` | pending, validated, rejected |
| `Document.document_type` | land_title, national_id, passport, lease_contract, sale_agreement, power_of_attorney, tax_clearance, rccm, tax_id, proof_of_income, bank_statement, inventory_of_fixtures, deposit_receipt, financial_statement, business_license, insurance_cert, building_permit, cadastral_plan, landlord_consent |
| `ApprovalWorkflow.status` | pending, approved, rejected, cancelled |
| `ApprovalWorkflow.workflow_type` | verification, validation, onboarding, publication |
| `Incident.status` | reported, qualified, analyzing, collecting_info, decision, resolved, closed, archived |
| `Incident.priority` | critique, elevee, normale, faible |
| `Incident.incident_type` | property_unavailable, inaccurate_info, visit_cancellation, participant_absence, fraud, fake_documents, platform_abuse, payment_dispute, contract_breach, data_violation, harassment, other |
| `Mediation.status` | proposed, accepted_demandeur, accepted_holder, mediator_nominated, exchanges, solution_proposed, accepted, closed |
| `AgentInvitation.status` | sent, link_opened, account_created, phone_verified, cni_uploaded, validated, active |
| `IdentityResolution.status` | detected, evaluating, human_review, merged, false_positive |
| `FinancingRequest.status` | draft, submitted, under_review, approved, rejected, disbursed |
| `Subscription.status` | active, cancelled, expired, past_due |
| `Negotiation.status` | not_started, demandeur_proposes, holder_responds, counter_offer, accepted, rejected, silent, failed, escalated |
| `Contact.status` | initiated, demandeur_interested, holder_contacted, holder_decision, double_consent, established |

---

## 6. Relations Map (All New Foreign Keys)

### 6.1 New FKs on Existing Tables

| Source Table | FK Field | Target Table | Type | Purpose |
|-------------|----------|-------------|------|---------|
| Conversation | `match_id` | Match | Optional 1:1 | Link conversation to match |
| Conversation | `transaction_id` | Transaction | Optional 1:1 | Link conversation to transaction |
| Event | `entity_type`, `entity_id` | Polymorphic | Optional | Event source entity |
| Event | `actor_id` | User | Optional | Event actor |
| Project | `multi_intent_group_id` | (self) | Optional | Linked multi-intent projects |

### 6.2 Intra-New-Table FKs

| Source Table | FK Field | Target Table | Type |
|-------------|----------|-------------|------|
| Intent | `user_id` | User | Required N:1 |
| Intent | `project_id` | Project | Optional N:1 |
| Match | `project_id` | Project | Required N:1 |
| Match | `property_id` | Property | Required N:1 |
| Match | `agent_id` | User | Optional N:1 |
| Visit | `match_id` | Match | Required N:1 |
| Visit | `property_id` | Property | Required N:1 |
| Visit | `demandeur_id` | User | Required N:1 |
| Visit | `holder_id` | User | Required N:1 |
| Visit | `agent_id` | User | Optional N:1 |
| Transaction | `project_id` | Project | Optional N:1 |
| Transaction | `property_id` | Property | Required N:1 |
| Transaction | `match_id` | Match | Optional N:1 |
| Transaction | `demandeur_id` | User | Required N:1 |
| Transaction | `holder_id` | User | Required N:1 |
| Transaction | `agent_id` | User | Optional N:1 |
| Transaction | `notaire_id` | User | Optional N:1 |
| Transaction | `negotiation_id` | Negotiation | Optional N:1 |
| Contact | `match_id` | Match | Required 1:1 |
| Contact | `demandeur_id` | User | Required N:1 |
| Contact | `holder_id` | User | Required N:1 |
| Negotiation | `transaction_id` | Transaction | Optional N:1 |
| Negotiation | `match_id` | Match | Optional N:1 |
| ServiceOrder | `service_id` | Service | Required N:1 |
| ServiceOrder | `user_id` | User | Required N:1 |
| ServiceOrder | `organization_id` | Organization | Optional N:1 |
| ServiceOrder | `property_id` | Property | Optional N:1 |
| Payment | `service_order_id` | ServiceOrder | Optional N:1 |
| Payment | `transaction_id` | Transaction | Optional N:1 |
| Payment | `user_id` | User | Required N:1 |
| AgentCredit | `user_id` | User | Required 1:1 |
| LeadPurchase | `agent_id` | User | Required N:1 |
| LeadPurchase | `lead_id` | Lead | Required N:1 |
| LeadPurchase | `payment_id` | Payment | Optional N:1 |
| Lead | `user_id` | User | Optional N:1 |
| Lead | `routed_to_agent_id` | User | Optional N:1 |
| Lead | `conversation_id` | Conversation | Optional N:1 |
| Lead | `assigned_project_id` | Project | Optional N:1 |
| Document | `user_id` | User | Required N:1 |
| Document | `validated_by` | User | Optional N:1 |
| ApprovalWorkflow | `requested_by` | User | Required N:1 |
| ApprovalWorkflow | `reviewed_by` | User | Optional N:1 |
| Incident | `reporter_id` | User | Required N:1 |
| Incident | `assigned_to` | User | Optional N:1 |
| Incident | `resolved_by` | User | Optional N:1 |
| Mediation | `incident_id` | Incident | Optional N:1 |
| Mediation | `transaction_id` | Transaction | Optional N:1 |
| Mediation | `demandeur_id` | User | Required N:1 |
| Mediation | `holder_id` | User | Required N:1 |
| Mediation | `mediator_id` | User | Optional N:1 |
| AgentInvitation | `organization_id` | Organization | Required N:1 |
| AgentInvitation | `invited_by` | User | Required N:1 |
| AgentInvitation | `created_user_id` | User | Optional N:1 |
| IdentityResolution | `primary_user_id` | User | Required N:1 |
| IdentityResolution | `duplicate_user_id` | User | Required N:1 |
| IdentityResolution | `reviewed_by` | User | Optional N:1 |
| ProfessionalProfile | `user_id` | User | Required 1:1 |
| FinancingRequest | `user_id` | User | Required N:1 |
| FinancingRequest | `project_id` | Project | Optional N:1 |
| GeographicUnit | `parent_id` | GeographicUnit | Optional N:1 (self-referential) |
| Subscription | `user_id` | User | Required N:1 |
| Subscription | `organization_id` | Organization | Optional N:1 |

---

## 7. Index Recommendations

### 7.1 Performance Indexes

| Table | Index | Type | Columns | Rationale |
|-------|-------|------|---------|-----------|
| Match | `idx_match_project_score` | B-tree | `project_id`, `overall_score DESC` | Per-project ranking |
| Match | `idx_match_property_active` | B-tree | `property_id`, `is_active` | Active property matches |
| Match | `idx_match_expires` | B-tree | `expires_at` | Expired match cleanup |
| Visit | `idx_visit_scheduled_status` | B-tree | `scheduled_at`, `status` | Upcoming visit queries |
| Visit | `idx_visit_demandeur` | B-tree | `demandeur_id`, `status` | User visit history |
| Transaction | `idx_transaction_status` | B-tree | `transaction_type`, `status` | Type-based aggregation |
| Transaction | `idx_transaction_party` | B-tree | `demandeur_id`, `holder_id` | Party lookup |
| Payment | `idx_payment_provider_ref` | B-tree | `provider_reference` | Reconciliation |
| Payment | `idx_payment_reconciliation` | B-tree | `created_at`, `status` | Pending reconciliation |
| Lead | `idx_lead_pipeline` | B-tree | `pipeline_stage`, `classification` | Pipeline throughput |
| Lead | `idx_lead_scoring` | B-tree | `final_score`, `classification` | Scoring distribution |
| Lead | `idx_lead_sla` | B-tree | `sla_deadline`, `sla_breached` | SLA monitoring |
| Document | `idx_document_entity` | B-tree | `entity_type`, `entity_id` | Polymorphic lookup |
| Document | `idx_document_validation` | B-tree | `status`, `entity_type` | Validation sweep |
| Incident | `idx_incident_priority` | B-tree | `status`, `priority` | Priority queue |
| IdentityResolution | `idx_id_resolution_confidence` | B-tree | `confidence_score`, `status` | Auto-merge candidates |
| GeographicUnit | `idx_geo_hierarchy` | B-tree | `level`, `parent_id` | Geo tree navigation |
| LeadPurchase | `idx_leadpurchase_agent` | B-tree | `agent_id`, `created_at` | Agent purchase history |
| ServiceOrder | `idx_serviceorder_expiry` | B-tree | `expires_at`, `status` | Expired service cleanup |
| AgentInvitation | `idx_invitation_expiry` | B-tree | `expires_at`, `status` | Stale invitation cleanup |

### 7.2 Full-Text Search Indexes

| Table | Columns | Type | Purpose |
|-------|---------|------|---------|
| Property | `title`, `summary` | GIN (tsvector) | Property search |
| GeographicUnit | `name`, `aliases` | GIN (tsvector) | Location search |
| Lead | `source_text`, `normalized_text` | GIN (tsvector) | Lead text search |

### 7.3 Partial Indexes

| Table | Condition | Columns | Purpose |
|-------|-----------|---------|---------|
| Match | `is_active = true` | `project_id`, `overall_score` | Active matches only |
| Visit | `status NOT IN ('completed', 'cancelled')` | `scheduled_at` | Upcoming visits |
| Lead | `pipeline_stage != 'routed'` | `created_at` | Unrouted leads |
| Document | `status = 'pending'` | `entity_type`, `entity_id` | Pending documents |
| Incident | `status NOT IN ('closed', 'archived')` | `priority`, `created_at` | Open incidents |

---

## 8. Uniqueness Constraints

| Table | Constraint | Columns | Rationale |
|-------|-----------|---------|-----------|
| Match | `uq_match_project_property_pool` | `project_id`, `property_id`, `match_pool` | One match per pair per pool |
| Contact | `uq_contact_match` | `match_id` | One contact per match |
| AgentCredit | `uq_agent_credit_user` | `user_id` | One credit balance per agent |
| LeadPurchase | `uq_lead_purchase_agent_lead` | `agent_id`, `lead_id` | One purchase per lead per agent |
| IdentityResolution | `uq_identity_resolution_pair` | `primary_user_id`, `duplicate_user_id` | One resolution pair |
| ProfessionalProfile | `uq_professional_profile_user` | `user_id` | One profile per user |
| Service | `uq_service_code` | `service_code` | Unique service identifier |
| GeographicUnit | `uq_geo_code` | `code` | Unique geo code |
| GeographicUnit | `uq_geo_name_level_parent` | `name`, `level`, `parent_id` | Unique name within hierarchy |
| AgentInvitation | `uq_invitation_token` | `secure_token` | Unique invitation link |
| Intent | `uq_intent_session_sequence` | `session_id`, `created_at` | Unique intent per session moment |
| Document | `uq_document_type_entity` | `entity_type`, `entity_id`, `document_type` | One doc of each type per entity |
| ApprovalWorkflow | `uq_approval_target_type` | `target_type`, `target_id`, `workflow_type` | One active workflow per target |
| Subscription | `uq_active_subscription_user` | `user_id`, `subscription_type`, `status` | One active subscription per type |
| FinancingRequest | (none) | — | Multiple requests allowed |

---

## 9. Data Migration Requirements

### 9.1 Migration 1: Enrich Existing Users

**Source:** Current `users` table
**Target:** Add new columns with defaults
**Script:** `ALTER TABLE users ADD COLUMN ... DEFAULT ...;`
**Data:** Backfill existing users:
- `trust_level = 1` for all existing users
- `phone_verified = true` if `phone_e164` is not null
- `email_verified = true` (all registered users have email)
- `onboarding_status = 'active'` for existing active users
- `last_activity_at = COALESCE(updatedAt, createdAt)` from conversations/messages
**Risk:** Low — additive columns with defaults
**Rollback:** `ALTER TABLE users DROP COLUMN ...;`

### 9.2 Migration 2: Enrich Existing Properties

**Source:** Current `properties` table
**Target:** Add new columns with defaults
**Data:** Backfill:
- `property_family` derived from `property_type` mapping (see PROPERTY_TYPE_CROSSWALK.md)
- `publish_status = 'published'` if `published_at` is not null, else `'draft'`
- `boost_level = 'none'` (default)
- `is_premium = false` (default)
- `verification_status = 'unverified'` (default)
- `price_displayed = priceMin` (if set)
- `data_quality_score = 50` (neutral baseline)
**Risk:** Low — additive columns; property_family mapping requires validation
**Rollback:** `ALTER TABLE properties DROP COLUMN ...;`

### 9.3 Migration 3: Enrich Existing Organizations

**Source:** Current `organizations` table
**Target:** Add new columns with defaults
**Data:**
- `operational_status = 'active'` for organizations with >0 users
- `agency_verified = false` (default)
**Risk:** Low
**Rollback:** `ALTER TABLE organizations DROP COLUMN ...;`

### 9.4 Migration 4: Create Reference Tables and Seed Data

**Source:** Current enum strings in code
**Target:** New reference tables
**Tables to create and seed:**
- `PropertyType` — 19+ types with hierarchy
- `ProfessionalCategory` — 24+ categories
- `ServiceCategory` — 4 categories
- `GeoLevel` — 6 levels
**Data:** Seed from code constants in `property_domain.py`, `business_profiles.py`, etc.
**Risk:** Medium — existing code references string values; need backward-compatible views or application-level mapping
**Rollback:** Drop reference tables; revert to string-based enums

### 9.5 Migration 5: Data Type Expansion

**Source:** Current `Property.property_type` (string)
**Target:** Foreign key to `PropertyType` table
**Strategy:**
- Phase 1: Add `property_type_id` FK column (nullable)
- Phase 2: Create PropertyType lookup rows from current values
- Phase 3: Update all existing properties to set `property_type_id`
- Phase 4: Make `property_type_id` required (NOT NULL)
- Phase 5: Deprecate old `property_type` string column (keep for backward compat)
**Risk:** HIGH — affects core Property model; requires application-level code changes
**Rollback:** Revert to string column; drop FK

### 9.6 Migration 6: New Table Creation

**Tables to CREATE (in dependency order):**

```
Phase A (no dependencies):
  - GeographicUnit
  - Service
  - PropertyType
  - ProfessionalCategory
  - ServiceCategory
  - GeoLevel

Phase B (depends on User, Property, Project, Organization):
  - Intent
  - ProfessionalProfile
  - FinancingRequest
  - GeographicUnit (self-referencing)

Phase C (depends on Phase B + core models):
  - Match
  - Lead
  - Subscription
  - AgentInvitation

Phase D (depends on Phase C):
  - Contact
  - Negotiation
  - Visit
  - ServiceOrder
  - Transaction

Phase E (depends on Phase D):
  - Payment
  - Document
  - LeadPurchase
  - AgentCredit

Phase F (cross-cutting):
  - Incident
  - Mediation
  - ApprovalWorkflow
  - IdentityResolution
```

**Rollback per phase:** `DROP TABLE ... CASCADE;` in reverse-phase order

---

## 10. Risks & Mitigations

| # | Risk | Severity | Probability | Mitigation |
|---|------|----------|-------------|------------|
| 1 | Property type migration (string → FK) breaks existing API contracts | HIGH | MEDIUM | Dual-write phase: keep string column + FK; migrate callers gradually |
| 2 | New table creation causes connection pool exhaustion during migration | MEDIUM | LOW | Run migrations off-peak; use batching; monitor pool |
| 3 | Polymorphic FKs (entity_type + entity_id) lack referential integrity | MEDIUM | HIGH | Application-level checks; audit constraints; scheduled integrity scans |
| 4 | Large `properties` table update blocks writes during backfill | HIGH | LOW | Batch updates in chunks (1000 rows); use pgroll or similar |
| 5 | Enum value mismatch between existing data and new reference tables | MEDIUM | MEDIUM | Pre-migration audit of all distinct values; map all edge cases |
| 6 | Existing conversations reference properties that fail new constraints | MEDIUM | LOW | Make new FKs nullable initially; backfill; then enforce |
| 7 | Performance degradation from new indexes on insert-heavy tables | LOW | MEDIUM | Concurrent index creation; monitor write latency |
| 8 | Race condition between migration and running application | HIGH | LOW | Use exclusive migration lock; maintain backward-compatible views |
| 9 | Stale data in `Event` table references deleted entities | LOW | HIGH | Acceptable; events are append-only audit records |
| 10 | Seed data for reference tables incomplete | MEDIUM | MEDIUM | Comprehensive pre-seed audit against all known Heritage Gold values |

---

## 11. Rollback Plan

### 11.1 Rollback Strategy

| Scenario | Action | Data Loss | Downtime |
|----------|--------|-----------|----------|
| Migration 1-3 fail (column add) | `ALTER TABLE ... DROP COLUMN` | None | Minutes |
| Migration 4 fails (seed data) | `DELETE FROM reference_tables` | Seed data | Minutes |
| Migration 5 fails (property_type FK) | Remove FK, keep string column | None | Hours |
| Migration 6 fails (new table) | `DROP TABLE ... CASCADE` | New data | Minutes |
| Catastrophic failure | Restore from pre-migration snapshot | < 1 hour data | Hours |

### 11.2 Pre-Migration Requirements

Before any migration:
1. Full database backup
2. Application in read-only maintenance mode
3. All migration scripts verified in staging
4. Rollback scripts pre-generated and tested
5. Feature flags toggled OFF for dependent functionality

### 11.3 Rollback Scripts

Each migration **MUST** have a corresponding rollback script:

```
M1_rollback.sql  → DROP COLUMNS from users
M2_rollback.sql  → DROP COLUMNS from properties
M3_rollback.sql  → DROP COLUMNS from organizations
M4_rollback.sql  → DROP TABLE reference_tables
M5_rollback.sql  → DROP FK; RESTORE string column
M6_rollback.sql  → DROP TABLE ... CASCADE (reverse phase order)
```

### 11.4 Rollback Verification

After rollback:
1. Run pre-migration data integrity checks
2. Verify all API endpoints return pre-migration responses
3. Confirm application starts without errors
4. Re-run all tests
5. Monitor error logs for 24 hours

---

*End of PRISMA_EXTENSION_BLUEPRINT.md — 22 new tables, 5 enriched tables, ~48 new relations cataloged.*
