# Field Extension Catalog — LAWIM_V2 Canonical Data Model

**Document ID:** LAWIM-FEC-V1  
**Status:** CANONICAL  
**Date:** 2026-07-15

---

## 1. Purpose

This catalog documents every new field being added across all 26 entities in the LAWIM_V2 Canonical Data Model Extension. Fields are categorized by source (Heritage Gold heritage vs. NEW), with validation rules, indexing, privacy classification, and audit requirements.

---

## 2. Field Catalog

### 2.1 User (14 new fields)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | trust_level | Int | NEW | 1-6 trust level | 1 ≤ value ≤ 6, default 1 | Yes | INTERNAL | Yes |
| 2 | phone_verified | Boolean | NEW | Phone verified via OTP | Default false | No | SENSITIVE | Yes |
| 3 | email_verified | Boolean | NEW | Email verified | Default false | No | SENSITIVE | Yes |
| 4 | identity_verified | Boolean | NEW | Identity document verified | Default false | No | SENSITIVE | Yes |
| 5 | professional_docs_verified | Boolean | NEW | Professional docs validated | Default false | No | SENSITIVE | Yes |
| 6 | professional_verified | Boolean | NEW | Full professional verification | Default false | No | SENSITIVE | Yes |
| 7 | reference_account | Boolean | NEW | Admin-granted reference | Default false | No | CONFIDENTIAL | Yes |
| 8 | owner_verified | Boolean | NEW | Property ownership verified | Default false | No | INTERNAL | Yes |
| 9 | is_active_agent | Boolean | NEW | Fully onboarded active agent | Default false | No | PUBLIC | No |
| 10 | onboarding_status | String | NEW | Onboarding step | One of: invited, account_created, phone_verified, cni_uploaded, validated, active | Yes | INTERNAL | Yes |
| 11 | agency_role | String? | NEW | Role within agency | One of: responsible, admin, agent, assistant | Yes | INTERNAL | Yes |
| 12 | agent_rating | Float? | NEW | 1.0-5.0 avg rating | 1.0 ≤ value ≤ 5.0 | Yes | PUBLIC | Yes |
| 13 | badges | JSON | NEW | Derived badge types array | Array of valid badge_type strings | No | PUBLIC | No |

### 2.2 Organization (9 new fields)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | rccm | String? | NEW | Trade register number | Alphanumeric, unique if set | No | SENSITIVE | Yes |
| 2 | tax_id | String? | NEW | Tax identification number | Alphanumeric, unique if set | No | SENSITIVE | Yes |
| 3 | trust_level | Int | NEW | 1-6 agency trust | 1 ≤ value ≤ 6, default 1 | Yes | INTERNAL | Yes |
| 4 | verification_status | String | NEW | Verification state | One of: unverified, pending, verified, rejected | Yes | INTERNAL | Yes |
| 5 | agency_verified | Boolean | NEW | Agency badge flag | Default false | No | PUBLIC | Yes |
| 6 | lifecycle_state | String | NEW | Org lifecycle | One of: draft, active, suspended, closed, archived | Yes | INTERNAL | Yes |
| 7 | zones | JSON | NEW | Geographic operation zones | Array of zone codes | No | PUBLIC | No |
| 8 | agent_count | Int | NEW | Active agent count | ≥ 0, default 0 | Yes | PUBLIC | No |
| 9 | operational_status | String | NEW | Operational readiness | One of: operational, non_operational | No | PUBLIC | No |

### 2.3 OrganizationMember (8 new fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | organization_id | Int | NEW | FK to Organization | Required, valid org | Yes | INTERNAL | No |
| 2 | user_id | Int | NEW | FK to User | Required, valid user | Yes | INTERNAL | No |
| 3 | agency_role | String | NEW | Role in agency | One of: responsible, admin, agent, assistant | Yes | INTERNAL | Yes |
| 4 | zones | JSON | NEW | Assigned geographic zones | Array of zone codes | No | INTERNAL | Yes |
| 5 | max_leads | Int | NEW | Max lead capacity | ≥ 0, default 50 | No | INTERNAL | No |
| 6 | is_active | Boolean | NEW | Active membership | Default true | Yes | INTERNAL | No |
| 7 | joined_at | String | NEW | Membership start | Valid ISO datetime | No | INTERNAL | No |
| 8 | left_at | String? | NEW | Membership end | Valid ISO datetime, ≥ joined_at | No | INTERNAL | No |

### 2.4 Property (17 new fields)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | property_family | String | NEW | Family classification | One of: residential, commercial, industrial, land, agricultural, hotel, project | Yes | PUBLIC | No |
| 2 | property_subtype | String? | NEW | Specific subtype | Valid subtype for family | No | PUBLIC | No |
| 3 | price_displayed | Int? | NEW | Display/asking price | ≥ 0 | No | PUBLIC | No |
| 4 | price_negotiable | Boolean | NEW | Price negotiable flag | Default false | No | PUBLIC | No |
| 5 | price_final | Int? | NEW | Final agreed price | ≥ 0, ≤ price_displayed | No | SENSITIVE | Yes |
| 6 | price_estimation | Int? | NEW | Estimated value | ≥ 0 | No | SENSITIVE | No |
| 7 | price_history | JSON | NEW | Historical prices array | Array of {price, date, type} | No | SENSITIVE | Yes |
| 8 | quality_score | Float? | NEW | 0-100 data quality | 0 ≤ value ≤ 100 | Yes | INTERNAL | Yes |
| 9 | quality_grade | String? | NEW | A+, A, B, C, D grade | One of: A+, A, B, C, D | Yes | PUBLIC | No |
| 10 | boost_level | Int | NEW | Visibility boost | 0, 1, or 2, default 0 | Yes | PUBLIC | Yes |
| 11 | boost_expires_at | String? | NEW | Boost expiration | Valid ISO datetime | Yes | PUBLIC | No |
| 12 | is_premium | Boolean | NEW | Premium listing flag | Default false | No | PUBLIC | Yes |
| 13 | verification_status | String | NEW | Property verification | One of: unverified, pending, verified, rejected | Yes | INTERNAL | Yes |
| 14 | verified_at | String? | NEW | Verification timestamp | Valid ISO datetime | Yes | INTERNAL | Yes |
| 15 | data_completeness | Float? | NEW | 0-100 completeness | 0 ≤ value ≤ 100 | No | INTERNAL | No |
| 16 | lifecycle_state | String | NEW | 10-state lifecycle | One of: reception, normalization, classification, validation, publication, matching, mise_en_relation, follow_up, archiving, conservation | Yes | INTERNAL | Yes |

### 2.5 Project (6 new fields)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | dossier_status | String | NEW | Dossier lifecycle | One of: intent, qualification, matching, mise_en_relation, visit, negotiation, transaction, closure, archiving | Yes | INTERNAL | Yes |
| 2 | consent_status | String | NEW | Double consent | One of: none, demandeur_interested, holder_contacted, holder_favorable, double_consent_obtained | Yes | INTERNAL | Yes |
| 3 | rematching_count | Int | NEW | Rematch cycles | ≥ 0, default 0 | Yes | INTERNAL | Yes |
| 4 | urgency_level | String | NEW | Urgency classification | One of: low, medium, high, critical | Yes | INTERNAL | No |
| 5 | intent_source | String? | NEW | Source intent type | Valid IntentType | No | INTERNAL | No |
| 6 | intent_confidence | Float? | NEW | Intent confidence score | 0.0 ≤ value ≤ 1.0 | No | INTERNAL | No |

### 2.6 Intent (14 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | user_id | Int | NEW | FK to User | Required, valid user | Yes | INTERNAL | No |
| 3 | conversation_id | Int? | NEW | FK to Conversation | Valid conversation | Yes | INTERNAL | No |
| 4 | message_id | Int? | NEW | FK to Message | Valid message | No | INTERNAL | No |
| 5 | intent_type | String | NEW | Detected intent type | One of: buy, rent, sell, invest, find, finance, service, visit, estimate | Yes | INTERNAL | Yes |
| 6 | confidence | Float | NEW | Detection confidence | 0.0 ≤ value ≤ 1.0 | Yes | INTERNAL | No |
| 7 | is_primary | Boolean | NEW | Primary flag for multi-intent | Default true | No | INTERNAL | No |
| 8 | multi_intent_group | String? | NEW | Batch group ID | UUID format | No | INTERNAL | No |
| 9 | urgency_score | Float? | NEW | Urgency level | 0.0 ≤ value ≤ 1.0 | Yes | INTERNAL | Yes |
| 10 | extracted_entities | JSON | NEW | Extracted entities | Valid JSON | No | SENSITIVE | No |
| 11 | role_mapping | String | NEW | Mapped platform role | One of: buyer, tenant, seller, investor, visitor, professional | No | INTERNAL | Yes |
| 12 | detection_pipeline | String | NEW | Pipeline identifier | Version string | No | INTERNAL | No |
| 13 | raw_input | String | NEW | Original user message | Non-empty | No | SENSITIVE | No |
| 14 | created_at | String | NEW | Detection timestamp | Valid ISO datetime | Yes | INTERNAL | No |

### 2.7 Match (16 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | project_id | Int | NEW | FK to Project | Required, valid project | Yes | INTERNAL | No |
| 3 | property_id | Int | NEW | FK to Property | Required, valid property | Yes | INTERNAL | No |
| 4 | score_real_estate | Float | NEW | RE dimension score | 0-100 | No | INTERNAL | No |
| 5 | score_availability | Float | NEW | Availability score | 0-100 | No | INTERNAL | No |
| 6 | score_document | Float | NEW | Document score | 0-100 | No | INTERNAL | No |
| 7 | score_reliability | Float | NEW | Reliability score | 0-100 | No | INTERNAL | No |
| 8 | score_transaction_success | Float | NEW | Success probability | 0-100 | No | INTERNAL | No |
| 9 | score_geographic | Float | NEW | Geographic score | 0-100 | No | INTERNAL | No |
| 10 | score_overall | Float | NEW | Composite score | 0-100 | Yes | INTERNAL | Yes |
| 11 | compatibility_level | String | NEW | Match quality | One of: excellent, good, average, low | Yes | INTERNAL | No |
| 12 | ranking_position | Int | NEW | Rank in results | ≥ 1 | No | INTERNAL | No |
| 13 | exclusion_reason | String? | NEW | Exclusion reason | String | No | INTERNAL | Yes |
| 14 | match_status | String | NEW | Match lifecycle | One of: pending, proposed, accepted, rejected, expired | Yes | INTERNAL | Yes |
| 15 | rematching_cycle | Int | NEW | Rematch cycle | ≥ 0, default 0 | Yes | INTERNAL | No |
| 16 | proposed_at | String | NEW | Proposal time | Valid ISO datetime | No | INTERNAL | No |
| 17 | decided_at | String? | NEW | Decision time | Valid ISO datetime | No | INTERNAL | Yes |
| 18 | created_at | String | NEW | Creation time | Valid ISO datetime | No | INTERNAL | No |

### 2.8 Visit (17 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | project_id | Int | NEW | FK to Project | Required | Yes | INTERNAL | No |
| 3 | property_id | Int | NEW | FK to Property | Required | Yes | INTERNAL | No |
| 4 | match_id | Int? | NEW | FK to Match | Valid match | No | INTERNAL | No |
| 5 | requested_by_user_id | Int | NEW | FK requester | Required | Yes | INTERNAL | No |
| 6 | organized_by_user_id | Int? | NEW | FK agent organizer | Valid user | No | INTERNAL | No |
| 7 | scheduled_at | String | NEW | Scheduled datetime | Valid ISO datetime | Yes | INTERNAL | No |
| 8 | confirmed_at | String? | NEW | Confirmation time | Valid ISO datetime | No | INTERNAL | Yes |
| 9 | completed_at | String? | NEW | Completion time | Valid ISO datetime | No | INTERNAL | Yes |
| 10 | cancelled_at | String? | NEW | Cancellation time | Valid ISO datetime | No | INTERNAL | Yes |
| 11 | cancellation_reason | String? | NEW | Reason | String | No | INTERNAL | Yes |
| 12 | visit_status | String | NEW | 9-state status | One of: demandee, awaiting_confirmation, confirmed, rescheduled, cancelled, completed, refused, no_show_demandeur, no_show_detenteur | Yes | INTERNAL | Yes |
| 13 | visit_type | String | NEW | Visit type | One of: initial, contre_visite, expertise | No | INTERNAL | No |
| 14 | reminder_24h_sent | Boolean | NEW | 24h reminder | Default false | No | INTERNAL | No |
| 15 | reminder_2h_sent | Boolean | NEW | 2h reminder | Default false | No | INTERNAL | No |
| 16 | satisfaction_score | Int? | NEW | 1-5 satisfaction | 1 ≤ value ≤ 5 | Yes | INTERNAL | Yes |
| 17 | satisfaction_feedback | String? | NEW | Comments | String | No | SENSITIVE | No |
| 18 | no_show_party | String? | NEW | No-show party | One of: demandeur, detenteur | No | SENSITIVE | Yes |
| 19 | created_at | String | NEW | Creation | Valid ISO datetime | No | INTERNAL | No |

### 2.9 Transaction (17 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | project_id | Int | NEW | FK to Project | Required | Yes | INTERNAL | No |
| 3 | property_id | Int | NEW | FK to Property | Required | Yes | INTERNAL | No |
| 4 | visit_id | Int? | NEW | FK to Visit | Valid visit | No | INTERNAL | No |
| 5 | transaction_type | String | NEW | Transaction type | One of: sale, purchase, rental, lease, commercial_lease, short_stay | Yes | INTERNAL | No |
| 6 | status | String | NEW | 7-state lifecycle | One of: agreement, preparation, documents, payment, signature, handover, completed, archived, failed | Yes | INTERNAL | Yes |
| 7 | agreed_price | Int? | NEW | Agreed price | ≥ 0 | No | SENSITIVE | Yes |
| 8 | currency | String | NEW | Currency | ISO 4217, default "XAF" | No | INTERNAL | No |
| 9 | commission_amount | Int? | NEW | LAWIM commission | ≥ 0 | No | SENSITIVE | Yes |
| 10 | commission_percentage | Float? | NEW | Commission rate | 0.0 ≤ value ≤ 100.0 | No | SENSITIVE | Yes |
| 11 | deposit_amount | Int? | NEW | Security deposit | ≥ 0 | No | SENSITIVE | No |
| 12 | expected_closing_date | String? | NEW | Target closing | Valid ISO datetime | Yes | INTERNAL | No |
| 13 | closed_at | String? | NEW | Actual closing | Valid ISO datetime | No | INTERNAL | Yes |
| 14 | cancelled_at | String? | NEW | Cancellation | Valid ISO datetime | No | INTERNAL | Yes |
| 15 | cancellation_reason | String? | NEW | Reason | String | No | INTERNAL | Yes |
| 16 | doc_checklist | JSON | NEW | Document checklist | Array of doc requirements | No | INTERNAL | No |
| 17 | doc_submission_status | String | NEW | Docs status | One of: pending, partial, complete | No | INTERNAL | Yes |
| 18 | created_at | String | NEW | Creation | Valid ISO datetime | No | INTERNAL | No |
| 19 | updated_at | String | NEW | Updated | Valid ISO datetime | No | INTERNAL | No |

### 2.10 Service (12 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | code | String | NEW | Unique service code | Alphanumeric, unique | Yes | PUBLIC | No |
| 3 | name | String | NEW | Display name | Non-empty | No | PUBLIC | No |
| 4 | description | String? | NEW | Description | String | No | PUBLIC | No |
| 5 | service_category | String | NEW | Category | One of: monetized, real_estate, professional, crm | Yes | PUBLIC | No |
| 6 | service_type | String | NEW | Type code | Valid type, unique | Yes | PUBLIC | No |
| 7 | base_price | Int | NEW | Base price FCFA | ≥ 0 | Yes | PUBLIC | Yes |
| 8 | currency | String | NEW | Currency | ISO 4217, default "XAF" | No | PUBLIC | No |
| 9 | billing_model | String | NEW | Billing | One of: one_time, recurring_monthly, pay_per_use | No | PUBLIC | No |
| 10 | duration_days | Int? | NEW | Duration | ≥ 1 if applicable | No | PUBLIC | No |
| 11 | status | String | NEW | Lifecycle | One of: active, inactive, deprecated | Yes | PUBLIC | Yes |
| 12 | metadata | JSON | NEW | Additional metadata | Valid JSON | No | INTERNAL | No |
| 13 | created_at | String | NEW | Creation | Valid ISO datetime | No | — | No |
| 14 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.11 ServiceOrder (15 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | service_id | Int | NEW | FK to Service | Required | Yes | INTERNAL | No |
| 3 | user_id | Int | NEW | FK ordering user | Required | Yes | INTERNAL | No |
| 4 | organization_id | Int? | NEW | FK ordering org | Valid org | No | INTERNAL | No |
| 5 | property_id | Int? | NEW | FK to Property | Valid property | No | INTERNAL | No |
| 6 | project_id | Int? | NEW | FK to Project | Valid project | No | INTERNAL | No |
| 7 | status | String | NEW | 8-state lifecycle | One of: created, proposed, accepted, payment_pending, activated, in_use, expired, archived | Yes | INTERNAL | Yes |
| 8 | price_paid | Int | NEW | Actual price paid | ≥ 0 | No | INTERNAL | Yes |
| 9 | currency | String | NEW | Currency | ISO 4217, default "XAF" | No | INTERNAL | No |
| 10 | quantity | Int | NEW | Quantity | ≥ 1, default 1 | No | INTERNAL | No |
| 11 | activation_date | String? | NEW | Activation time | Valid ISO datetime | No | INTERNAL | Yes |
| 12 | expiration_date | String? | NEW | Expiration time | Valid ISO datetime | Yes | INTERNAL | Yes |
| 13 | payment_link | String? | NEW | Campay payment link | Valid URL | No | SENSITIVE | No |
| 14 | payment_id | Int? | NEW | FK to Payment | Valid payment ID | Yes | SENSITIVE | No |
| 15 | metadata | JSON | NEW | Order metadata | Valid JSON | No | INTERNAL | No |
| 16 | created_at | String | NEW | Creation | Valid ISO datetime | No | — | No |
| 17 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.12 Payment (16 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | service_order_id | Int? | NEW | FK to ServiceOrder | Valid service order | Yes | INTERNAL | No |
| 3 | transaction_id | Int? | NEW | FK to Transaction | Valid transaction | No | INTERNAL | No |
| 4 | user_id | Int | NEW | FK paying user | Required | Yes | INTERNAL | No |
| 5 | amount | Int | NEW | Amount FCFA | ≥ 0 | No | INTERNAL | Yes |
| 6 | currency | String | NEW | Currency | ISO 4217, default "XAF" | No | INTERNAL | No |
| 7 | status | String | NEW | 10-state lifecycle | One of: created, initiated, pending, confirmed, failed, cancelled, expired, refunded, reconciled, disputed | Yes | INTERNAL | Yes |
| 8 | payment_method | String? | NEW | Method | One of: campay, orange_money, mobile_money, card | No | INTERNAL | No |
| 9 | provider_reference | String? | NEW | Provider txn ref | String | Yes | SENSITIVE | Yes |
| 10 | provider_status | String? | NEW | Raw provider status | String | No | INTERNAL | No |
| 11 | payment_link | String? | NEW | Campay payment URL | Valid URL | No | SENSITIVE | No |
| 12 | failure_reason | String? | NEW | Failure reason | String | No | SENSITIVE | Yes |
| 13 | refund_reason | String? | NEW | Refund reason | String | No | SENSITIVE | Yes |
| 14 | refunded_at | String? | NEW | Refund time | Valid ISO datetime | No | INTERNAL | Yes |
| 15 | reconciled_at | String? | NEW | Reconciliation | Valid ISO datetime | No | INTERNAL | Yes |
| 16 | disputed_at | String? | NEW | Dispute time | Valid ISO datetime | No | INTERNAL | Yes |
| 17 | metadata | JSON | NEW | Payment metadata | Valid JSON | No | INTERNAL | No |
| 18 | created_at | String | NEW | Creation | Valid ISO datetime | No | — | No |
| 19 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.13 AgentCredit (11 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | user_id | Int | NEW | FK to User (agent) | Required, unique | Yes | SENSITIVE | No |
| 3 | balance | Int | NEW | Current balance FCFA | ≥ 0 | Yes | SENSITIVE | Yes |
| 4 | total_purchased | Int | NEW | Lifetime purchased | ≥ 0 | No | SENSITIVE | No |
| 5 | total_spent | Int | NEW | Lifetime spent | ≥ 0 | No | SENSITIVE | No |
| 6 | last_recharge_at | String? | NEW | Last recharge | Valid ISO datetime | No | SENSITIVE | Yes |
| 7 | last_usage_at | String? | NEW | Last usage | Valid ISO datetime | No | SENSITIVE | No |
| 8 | auto_recharge_enabled | Boolean | NEW | Auto-recharge | Default false | No | SENSITIVE | Yes |
| 9 | auto_recharge_threshold | Int? | NEW | Low balance threshold | ≥ 0 | No | SENSITIVE | No |
| 10 | auto_recharge_amount | Int? | NEW | Recharge amount | ≥ 0 | No | SENSITIVE | No |
| 11 | created_at | String | NEW | Creation | Valid ISO datetime | No | — | No |
| 12 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.14 LeadPurchase (11 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | user_id | Int | NEW | FK purchasing agent | Required | Yes | SENSITIVE | No |
| 3 | lead_id | Int | NEW | FK to Lead | Required | Yes | SENSITIVE | No |
| 4 | organization_id | Int? | NEW | FK to Organization | Valid org | No | SENSITIVE | No |
| 5 | purchase_type | String | NEW | Pack type | One of: lead_bronze, lead_silver, lead_gold, coordinate_unlock | No | SENSITIVE | No |
| 6 | price_paid | Int | NEW | Price FCFA | ≥ 0 | No | SENSITIVE | Yes |
| 7 | currency | String | NEW | Currency | ISO 4217, default "XAF" | No | SENSITIVE | No |
| 8 | payment_id | Int? | NEW | FK to Payment | Valid payment | No | SENSITIVE | No |
| 9 | credit_id | Int? | NEW | FK credit txn | Valid credit txn | No | SENSITIVE | No |
| 10 | status | String | NEW | Status | One of: completed, refunded, disputed | Yes | SENSITIVE | Yes |
| 11 | purchased_at | String | NEW | Purchase time | Valid ISO datetime | Yes | SENSITIVE | Yes |
| 12 | refunded_at | String? | NEW | Refund time | Valid ISO datetime | No | SENSITIVE | Yes |
| 13 | created_at | String | NEW | Creation | Valid ISO datetime | No | — | No |

### 2.15 Lead (24 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | user_id | Int | NEW | FK source user | Required | Yes | INTERNAL | No |
| 3 | assigned_to_user_id | Int? | NEW | FK assigned agent | Valid user | Yes | INTERNAL | Yes |
| 4 | organization_id | Int? | NEW | FK assigned org | Valid org | Yes | INTERNAL | No |
| 5 | property_id | Int? | NEW | FK to Property | Valid property | No | INTERNAL | No |
| 6 | project_id | Int? | NEW | FK to Project | Valid project | No | INTERNAL | No |
| 7 | source_conversation_id | Int? | NEW | FK Conversation | Valid conversation | No | INTERNAL | No |
| 8 | lead_type | String | NEW | Lead classification | One of: tenant, buyer, seller, investor, diaspora_investor | Yes | INTERNAL | No |
| 9 | lead_status | String | NEW | CRM pipeline stage | One of: new, contacted, qualified, proposal, negotiation, won, lost, spam | Yes | INTERNAL | Yes |
| 10 | base_score | Int | NEW | Base score by type | 0-100 | No | INTERNAL | No |
| 11 | score_boosters | Int | NEW | Booster points | ≥ 0 | No | INTERNAL | Yes |
| 12 | score_penalties | Int | NEW | Penalty points | ≥ 0 | No | INTERNAL | Yes |
| 13 | score_total | Int | NEW | Final score | 0-100 | Yes | INTERNAL | Yes |
| 14 | classification | String | NEW | Lead tier | One of: HOT, WARM, COLD, LOW, SPAM | Yes | INTERNAL | Yes |
| 15 | routing_zone | String? | NEW | Geographic zone | Valid zone code | No | INTERNAL | No |
| 16 | urgency_level | String | NEW | Urgency | One of: low, medium, high, critical | No | INTERNAL | No |
| 17 | sla_priority | String | NEW | SLA priority | One of: P0, P1, P2, P3 | Yes | INTERNAL | No |
| 18 | sla_deadline | String? | NEW | SLA response by | Valid ISO datetime | Yes | INTERNAL | Yes |
| 19 | sla_breached | Boolean | NEW | SLA breach flag | Default false | Yes | INTERNAL | Yes |
| 20 | behavior_data | JSON | NEW | Behavior tracking | Valid JSON | No | SENSITIVE | No |
| 21 | fraud_flags | JSON | NEW | Fraud detection | Valid JSON | Yes | SENSITIVE | Yes |
| 22 | score_breakdown | JSON | NEW | Score details | Valid JSON | No | SENSITIVE | No |
| 23 | first_response_at | String? | NEW | First response | Valid ISO datetime | No | INTERNAL | Yes |
| 24 | last_activity_at | String? | NEW | Last activity | Valid ISO datetime | No | INTERNAL | No |
| 25 | converted_at | String? | NEW | Conversion | Valid ISO datetime | No | INTERNAL | Yes |
| 26 | created_at | String | NEW | Creation | Valid ISO datetime | Yes | — | No |
| 27 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.16 Document (17 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | document_type | String | NEW | Document type | One of: cni, passport, land_title, contract, deposit_proof, inventory, power_of_attorney, tax_receipt, rccm, proof_of_address, etc. | Yes | INTERNAL | No |
| 3 | entity_type | String | NEW | Owning entity type | One of: user, organization, property, transaction, project | Yes | INTERNAL | No |
| 4 | entity_id | Int | NEW | Owning entity ID | Required, valid entity | Yes | INTERNAL | No |
| 5 | transaction_id | Int? | NEW | FK to Transaction | Valid transaction | Yes | INTERNAL | No |
| 6 | file_url | String | NEW | Document URL | Valid URL | No | SENSITIVE | Yes |
| 7 | file_hash | String? | NEW | Integrity hash | SHA-256 hex | No | SENSITIVE | No |
| 8 | file_size | Int? | NEW | Size bytes | ≥ 0 | No | INTERNAL | No |
| 9 | mime_type | String? | NEW | MIME type | Valid MIME | No | INTERNAL | No |
| 10 | verification_status | String | NEW | Verification state | One of: pending, verified, rejected | Yes | INTERNAL | Yes |
| 11 | verified_by_user_id | Int? | NEW | FK verifier | Valid user | Yes | INTERNAL | Yes |
| 12 | verified_at | String? | NEW | Verification time | Valid ISO datetime | No | INTERNAL | Yes |
| 13 | rejection_reason | String? | NEW | Rejection reason | String | No | SENSITIVE | Yes |
| 14 | is_mandatory | Boolean | NEW | Mandatory flag | Default false | No | INTERNAL | No |
| 15 | expires_at | String? | NEW | Document expiry | Valid ISO datetime | Yes | INTERNAL | No |
| 16 | metadata | JSON | NEW | Document metadata | Valid JSON | No | INTERNAL | No |
| 17 | created_at | String | NEW | Upload time | Valid ISO datetime | No | — | No |
| 18 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.17 Event (6 new fields)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | actor_user_id | Int? | NEW | FK triggering user | Valid user | Yes | INTERNAL | Yes |
| 2 | entity_type | String? | NEW | Affected entity type | String | Yes | INTERNAL | Yes |
| 3 | entity_id | Int? | NEW | Affected entity ID | Valid entity ID | Yes | INTERNAL | Yes |
| 4 | event_version | Int | NEW | Payload schema version | ≥ 1, default 1 | No | INTERNAL | No |
| 5 | correlation_id | String? | NEW | Correlation ID | UUID format | Yes | INTERNAL | No |
| 6 | causation_id | String? | NEW | Causing event ID | UUID format | No | INTERNAL | No |

### 2.18 ApprovalWorkflow (13 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | approval_type | String | NEW | Type of approval | One of: agency_creation, listing_validation, professional_verification, org_verification, document_verification | Yes | INTERNAL | No |
| 3 | target_type | String | NEW | Target entity type | One of: organization, property, user, document | Yes | INTERNAL | No |
| 4 | target_id | Int | NEW | Target entity ID | Valid ID | Yes | INTERNAL | No |
| 5 | requester_user_id | Int | NEW | FK requester | Required | Yes | INTERNAL | No |
| 6 | reviewer_user_id | Int? | NEW | FK reviewer | Valid user | Yes | INTERNAL | Yes |
| 7 | status | String | NEW | Workflow status | One of: pending, approved, rejected, cancelled | Yes | INTERNAL | Yes |
| 8 | review_notes | String? | NEW | Reviewer notes | String | No | INTERNAL | Yes |
| 9 | approved_at | String? | NEW | Approval time | Valid ISO datetime | No | INTERNAL | Yes |
| 10 | rejected_at | String? | NEW | Rejection time | Valid ISO datetime | No | INTERNAL | Yes |
| 11 | rejection_reason | String? | NEW | Reason | String | No | INTERNAL | Yes |
| 12 | escalation_level | Int | NEW | Escalation tier | 1, 2, or 3, default 1 | Yes | INTERNAL | Yes |
| 13 | created_at | String | NEW | Request time | Valid ISO datetime | No | — | No |
| 14 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.19 Mediation (16 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | incident_id | Int | NEW | FK to Incident | Required | Yes | SENSITIVE | No |
| 3 | project_id | Int? | NEW | FK to Project | Valid project | No | SENSITIVE | No |
| 4 | transaction_id | Int? | NEW | FK to Transaction | Valid transaction | No | SENSITIVE | No |
| 5 | mediator_user_id | Int? | NEW | FK mediator | Valid user | Yes | SENSITIVE | Yes |
| 6 | demandeur_user_id | Int | NEW | FK demandeur | Required | No | SENSITIVE | No |
| 7 | detenteur_user_id | Int | NEW | FK detenteur | Required | No | SENSITIVE | No |
| 8 | status | String | NEW | 8-state lifecycle | One of: incident_reported, mediation_proposed, parties_accepted, mediator_nominated, exchanges, solution_proposed, resolved, closed | Yes | SENSITIVE | Yes |
| 9 | mediation_type | String | NEW | Dispute type | One of: visit_dispute, transaction_dispute, contract_dispute, quality_dispute | No | SENSITIVE | No |
| 10 | demandeur_acceptance | Boolean? | NEW | Demandeur accepts | Boolean | No | SENSITIVE | Yes |
| 11 | detenteur_acceptance | Boolean? | NEW | Detenteur accepts | Boolean | No | SENSITIVE | Yes |
| 12 | proposed_solution | String? | NEW | Mediator proposal | String | No | SENSITIVE | Yes |
| 13 | solution_accepted_by_demandeur | Boolean? | NEW | Accepted by demandeur | Boolean | No | SENSITIVE | Yes |
| 14 | solution_accepted_by_detenteur | Boolean? | NEW | Accepted by detenteur | Boolean | No | SENSITIVE | Yes |
| 15 | resolution_notes | String? | NEW | Final notes | String | No | SENSITIVE | Yes |
| 16 | created_at | String | NEW | Creation | Valid ISO datetime | No | — | No |
| 17 | resolved_at | String? | NEW | Resolution | Valid ISO datetime | No | SENSITIVE | Yes |
| 18 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.20 Incident (16 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | incident_type | String | NEW | Type of incident | One of: property_unavailable, inaccurate_info, visit_cancellation, participant_absence, fraud, fake_documents, platform_abuse, payment_dispute, contract_dispute | Yes | SENSITIVE | No |
| 3 | priority | String | NEW | Priority level | One of: critical, high, normal, low | Yes | SENSITIVE | No |
| 4 | status | String | NEW | 8-state lifecycle | One of: reporting, qualification, analysis, information_gathering, decision, resolution, closure, archiving | Yes | SENSITIVE | Yes |
| 5 | reporter_user_id | Int | NEW | FK reporter | Required | Yes | SENSITIVE | No |
| 6 | assigned_to_user_id | Int? | NEW | FK handler | Valid user | Yes | SENSITIVE | Yes |
| 7 | target_type | String? | NEW | Target entity type | One of: user, property, transaction, organization | No | SENSITIVE | No |
| 8 | target_id | Int? | NEW | Target entity ID | Valid ID | Yes | SENSITIVE | No |
| 9 | description | String | NEW | Incident description | Non-empty | No | SENSITIVE | No |
| 10 | evidence_links | JSON | NEW | Evidence URLs | Array of URLs | No | SENSITIVE | Yes |
| 11 | fraud_actions_taken | JSON? | NEW | Fraud mitigation | Array of {type, applied_at, reversed_at} | No | SENSITIVE | Yes |
| 12 | resolution | String? | NEW | Resolution text | String | No | SENSITIVE | Yes |
| 13 | resolved_at | String? | NEW | Resolution time | Valid ISO datetime | No | SENSITIVE | Yes |
| 14 | created_at | String | NEW | Creation | Valid ISO datetime | Yes | — | No |
| 15 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.21 AgentInvitation (14 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | organization_id | Int | NEW | FK to Organization | Required | Yes | INTERNAL | No |
| 3 | invited_by_user_id | Int | NEW | FK inviting user | Required | No | INTERNAL | No |
| 4 | invitee_email | String | NEW | Invitee email | Valid email format | Yes | SENSITIVE | No |
| 5 | invitee_phone | String? | NEW | Invitee phone | E.164 format | No | SENSITIVE | No |
| 6 | secure_link_token | String | NEW | Unique token | UUID, unique | Yes | SENSITIVE | Yes |
| 7 | secure_link_expires_at | String | NEW | Link expiry | Valid ISO datetime | No | INTERNAL | No |
| 8 | status | String | NEW | 7-state lifecycle | One of: invitation_sent, link_clicked, account_created, phone_verified, cni_uploaded, validated, activated | Yes | INTERNAL | Yes |
| 9 | onboarding_step | String | NEW | Current step | One of: invited, account_created, phone_verified, cni_uploaded, validated, active | No | INTERNAL | No |
| 10 | account_created_at | String? | NEW | Account creation | Valid ISO datetime | No | INTERNAL | Yes |
| 11 | phone_verified_at | String? | NEW | Phone verified | Valid ISO datetime | No | INTERNAL | Yes |
| 12 | cni_uploaded_at | String? | NEW | CNI uploaded | Valid ISO datetime | No | INTERNAL | Yes |
| 13 | validated_at | String? | NEW | Validated | Valid ISO datetime | No | INTERNAL | Yes |
| 14 | activated_at | String? | NEW | Activated | Valid ISO datetime | No | INTERNAL | Yes |
| 15 | created_at | String | NEW | Creation | Valid ISO datetime | Yes | — | No |
| 16 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.22 IdentityResolution (13 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | user_id_primary | Int | NEW | FK primary user | Required, ≠ user_id_duplicate | Yes | CONFIDENTIAL | No |
| 3 | user_id_duplicate | Int | NEW | FK duplicate user | Required, ≠ user_id_primary | Yes | CONFIDENTIAL | No |
| 4 | match_confidence | Float | NEW | 0.0-1.0 confidence | 0.0 ≤ value ≤ 1.0 | Yes | CONFIDENTIAL | No |
| 5 | match_signals | JSON | NEW | Matched signals | Array of {signal_type, value, confidence} | No | CONFIDENTIAL | No |
| 6 | status | String | NEW | 5-state lifecycle | One of: potential_match_detected, confidence_evaluation, human_review, merged, false_positive_discarded | Yes | CONFIDENTIAL | Yes |
| 7 | resolution_type | String | NEW | Resolution type | One of: merge, false_positive, manual_review_required | No | CONFIDENTIAL | Yes |
| 8 | reviewed_by_user_id | Int? | NEW | FK reviewer | Valid user | Yes | CONFIDENTIAL | Yes |
| 9 | reviewed_at | String? | NEW | Review time | Valid ISO datetime | No | CONFIDENTIAL | Yes |
| 10 | merged_at | String? | NEW | Merge time | Valid ISO datetime | No | CONFIDENTIAL | Yes |
| 11 | created_at | String | NEW | Detection time | Valid ISO datetime | No | — | No |
| 12 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.23 ProfessionalProfile (17 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | user_id | Int | NEW | FK to User | Required, unique | Yes | INTERNAL | No |
| 3 | professional_type | String | NEW | Type of professional | Valid type from catalog | Yes | PUBLIC | No |
| 4 | license_number | String? | NEW | Professional license | String | No | SENSITIVE | Yes |
| 5 | years_of_experience | Int? | NEW | Years in profession | ≥ 0 | No | INTERNAL | No |
| 6 | service_area_zones | JSON | NEW | Service zones | Array of zone codes | Yes | PUBLIC | No |
| 7 | rating | Float? | NEW | 1.0-5.0 avg rating | 1.0 ≤ value ≤ 5.0 | Yes | PUBLIC | Yes |
| 8 | total_reviews | Int | NEW | Review count | ≥ 0, default 0 | Yes | PUBLIC | No |
| 9 | verification_status | String | NEW | Verification | One of: unverified, pending, verified, rejected | Yes | INTERNAL | Yes |
| 10 | verified_at | String? | NEW | Verification time | Valid ISO datetime | No | INTERNAL | Yes |
| 11 | is_available | Boolean | NEW | Available for hire | Default true | Yes | PUBLIC | No |
| 12 | business_hours | JSON? | NEW | Business hours | Valid JSON schedule | No | PUBLIC | No |
| 13 | portfolio_urls | JSON? | NEW | Portfolio links | Array of URLs | No | SENSITIVE | No |
| 14 | metadata | JSON | NEW | Additional metadata | Valid JSON | No | INTERNAL | No |
| 15 | created_at | String | NEW | Creation | Valid ISO datetime | No | — | No |
| 16 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.24 FinancingRequest (17 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | user_id | Int | NEW | FK applicant | Required | Yes | CONFIDENTIAL | No |
| 3 | project_id | Int | NEW | FK to Project | Required | Yes | CONFIDENTIAL | No |
| 4 | property_id | Int? | NEW | FK to Property | Valid property | No | CONFIDENTIAL | No |
| 5 | financing_type | String | NEW | Type of financing | One of: mortgage, personal_loan, construction_loan, bridging_loan | Yes | CONFIDENTIAL | No |
| 6 | requested_amount | Int | NEW | Loan amount | ≥ 0 | No | CONFIDENTIAL | Yes |
| 7 | currency | String | NEW | Currency | ISO 4217, default "XAF" | No | CONFIDENTIAL | No |
| 8 | monthly_income | Int? | NEW | Monthly income | ≥ 0 | No | CONFIDENTIAL | Yes |
| 9 | employment_status | String? | NEW | Employment | One of: employed, self_employed, unemployed, retired | No | CONFIDENTIAL | No |
| 10 | employer_name | String? | NEW | Employer | String | No | CONFIDENTIAL | No |
| 11 | years_in_employment | Int? | NEW | Years employed | ≥ 0 | No | CONFIDENTIAL | No |
| 12 | existing_loans | Int? | NEW | Existing obligations | ≥ 0 | No | CONFIDENTIAL | Yes |
| 13 | credit_score | Int? | NEW | Credit score | 0-1000 | No | CONFIDENTIAL | Yes |
| 14 | down_payment | Int? | NEW | Available down payment | ≥ 0 | No | CONFIDENTIAL | Yes |
| 15 | status | String | NEW | Application status | One of: draft, submitted, under_review, approved, rejected, conditions_pending, funded | Yes | CONFIDENTIAL | Yes |
| 16 | reviewed_by_user_id | Int? | NEW | FK reviewer | Valid user | Yes | CONFIDENTIAL | Yes |
| 17 | reviewed_at | String? | NEW | Review time | Valid ISO datetime | No | CONFIDENTIAL | Yes |
| 18 | decision_notes | String? | NEW | Underwriting notes | String | No | CONFIDENTIAL | Yes |
| 19 | created_at | String | NEW | Creation | Valid ISO datetime | No | — | No |
| 20 | updated_at | String | NEW | Updated | Valid ISO datetime | No | — | No |

### 2.25 GeographicUnit (11 fields — NEW entity)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | id | Int (auto) | NEW | Primary key | Auto-increment | Yes | — | No |
| 2 | level | String | NEW | Hierarchy level | One of: country, region, department, city, district, neighborhood, zone | Yes | PUBLIC | No |
| 3 | code | String | NEW | Geographic code | Unique per level | Yes | PUBLIC | No |
| 4 | name | String | NEW | Geographic name | Non-empty | Yes | PUBLIC | No |
| 5 | parent_id | Int? | NEW | FK parent unit | Valid GeographicUnit | Yes | PUBLIC | No |
| 6 | latitude | Float? | NEW | Centroid lat | -90 to 90 | No | PUBLIC | No |
| 7 | longitude | Float? | NEW | Centroid lng | -180 to 180 | No | PUBLIC | No |
| 8 | bounding_box | JSON? | NEW | GeoJSON bbox | Valid GeoJSON | No | PUBLIC | No |
| 9 | timezone | String? | NEW | IANA timezone | Valid IANA | No | PUBLIC | No |
| 10 | is_active | Boolean | NEW | Active flag | Default true | Yes | PUBLIC | No |
| 11 | metadata | JSON | NEW | Additional data | Valid JSON | No | PUBLIC | No |
| 12 | created_at | String | NEW | Creation | Valid ISO datetime | No | — | No |

### 2.26 Consent (9 new fields)

| # | Field | Type | Source | Description | Validation | Indexed | Privacy | Audit |
|---|-------|------|--------|-------------|------------|---------|---------|-------|
| 1 | consent_type | String | NEW | Type of consent | One of: contact_sharing, data_sharing, marketing, mediation | Yes | SENSITIVE | Yes |
| 2 | granted_by_user_id | Int | NEW | FK granting user | Required | Yes | SENSITIVE | No |
| 3 | granted_to_user_id | Int? | NEW | FK receiving user | Valid user | Yes | SENSITIVE | No |
| 4 | granted_to_organization_id | Int? | NEW | FK receiving org | Valid org | No | SENSITIVE | No |
| 5 | project_id | Int? | NEW | FK context project | Valid project | Yes | SENSITIVE | No |
| 6 | status | String | NEW | Consent state | One of: pending, granted, withdrawn, expired | Yes | SENSITIVE | Yes |
| 7 | consent_channel | String | NEW | Consent channel | One of: platform, whatsapp, email, sms | No | SENSITIVE | Yes |
| 8 | granted_at | String | NEW | Grant timestamp | Valid ISO datetime | No | SENSITIVE | Yes |
| 9 | expires_at | String? | NEW | Expiry | Valid ISO datetime | Yes | SENSITIVE | No |
| 10 | withdrawn_at | String? | NEW | Withdrawal | Valid ISO datetime | No | SENSITIVE | Yes |
| 11 | purpose_description | String? | NEW | Purpose | String | No | SENSITIVE | No |

---

## 3. Field Count Summary

| Entity | New Fields | Entity | New Fields |
|--------|-----------|--------|-----------|
| User | 13 | ServiceOrder | 15 |
| Organization | 9 | Payment | 16 |
| OrganizationMember | 8 | AgentCredit | 11 |
| Property | 16 | LeadPurchase | 11 |
| Project | 6 | Lead | 24 |
| Intent | 14 | Document | 17 |
| Match | 16 | Event | 6 |
| Visit | 17 | ApprovalWorkflow | 13 |
| Transaction | 17 | Mediation | 16 |
| Service | 12 | Incident | 13 |

| Entity | New Fields | Entity | New Fields |
|--------|-----------|--------|-----------|
| AgentInvitation | 14 | ProfessionalProfile | 16 |
| IdentityResolution | 11 | FinancingRequest | 17 |
| GeographicUnit | 11 | Consent | 9 |

**Total new fields: 336** (across 26 entities, 18 domains)

---

## 4. Field Distribution by Source

| Source | Count | Percentage |
|--------|-------|-----------|
| Heritage Gold (existing migration) | 0 | 0% |
| **NEW (domain extension)** | **336** | **100%** |

---

## 5. Field Distribution by Privacy Level

| Privacy Level | Count | Percentage |
|--------------|-------|-----------|
| PUBLIC | 44 | 13.1% |
| INTERNAL | 181 | 53.9% |
| SENSITIVE | 83 | 24.7% |
| CONFIDENTIAL | 28 | 8.3% |

---

## 6. Field Distribution by Audit Requirement

| Audit Required | Count | Percentage |
|---------------|-------|-----------|
| Yes | 208 | 61.9% |
| No | 128 | 38.1% |

---

*End of FIELD_EXTENSION_CATALOG.md*
