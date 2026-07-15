# CRM EXTENSION MODEL

**Document ID:** LAWIM-H13-CRM-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §11 (CRM Pipeline), §12 (Identity Model), §13 (Organization Model)
**Source Crosswalks:** required_extensions.json (crm, crm_monetized_services), CRM_MODEL.md (Gold)

---

## Table of Contents

1. [Lead Entity Model](#1-lead-entity-model)
2. [8-Stage CRM Pipeline](#2-8-stage-crm-pipeline)
3. [Lead Scoring Engine](#3-lead-scoring-engine)
4. [Lead Classification](#4-lead-classification)
5. [CRM Routing Engine](#5-crm-routing-engine)
6. [Anti-Fraud Detection Layers](#6-anti-fraud-detection-layers)
7. [Behavior Tracking Fields](#7-behavior-tracking-fields)
8. [SLA by Priority](#8-sla-by-priority)
9. [Agent Rating System](#9-agent-rating-system)
10. [Feedback Handling System](#10-feedback-handling-system)
11. [Complete Extension Mapping Table](#11-complete-extension-mapping-table)

---

## 1. Lead Entity Model

### 1.1 Core Lead Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `source_channel` | Enum | `whatsapp \| telegram \| dashboard \| api \| referral` |
| `source_text` | Text | Original incoming message |
| `normalized_text` | Text | Normalized text (lowercase, unicode normalized) |
| `language` | Enum | `fr \| en \| pid` |
| `pipeline_stage` | Enum | `incoming \| normalized \| extracted \| intent_detected \| enriched \| scored \| classified \| routed` |
| `detected_intent` | Enum? | Detected primary intent |
| `intent_confidence` | Float? | Intent detection confidence (0.0-1.0) |
| `lead_type` | Enum? | `tenant \| buyer \| seller \| investor \| diaspora_investor` |
| `base_score` | Int | Base score by lead type |
| `boosters_applied` | JSON[] | Array of booster `{type, value}` |
| `penalties_applied` | JSON[] | Array of penalty `{type, value}` |
| `total_boost` | Int | Sum of all boosters |
| `total_penalty` | Int | Sum of all penalties |
| `final_score` | Int | `base_score + total_boost - total_penalty` |
| `classification` | Enum | `hot \| warm \| cold \| low \| spam` |
| `routed_to_agent_id` | UUID? | Assigned agent |
| `routed_at` | DateTime? | Route assignment timestamp |
| `routing_method` | Enum? | `zone \| availability \| score \| manual` |
| `is_fraud` | Boolean | Flagged as potential fraud |
| `fraud_layers_triggered` | String[] | Which anti-fraud layers fired |
| `fraud_action_taken` | Enum? | `none \| flag \| temporary_suspend \| block` |
| `user_id` | UUID? | Linked to existing User if identified |
| `phone` | String | Contact phone |
| `email` | String? | Contact email |
| `name` | String | Contact name |
| `city` | String? | Detected city |
| `neighborhood` | String? | Detected neighborhood |
| `budget_min` | Decimal? | Detected budget range |
| `budget_max` | Decimal? | Detected budget range max |
| `urgency` | Enum? | `low \| medium \| high \| urgent` |
| `is_diaspora` | Boolean | Diaspora indicator |
| `cash_purchase` | Boolean | Cash purchase indicator |
| `sla_priority` | Enum | `p0 \| p1 \| p2 \| p3` |
| `sla_deadline` | DateTime | SLA response deadline |
| `first_response_at` | DateTime? | First agent response |
| `sla_breached` | Boolean | Whether SLA was breached |
| `converted_to_project` | Boolean | Whether lead converted to project |
| `converted_project_id` | UUID? | Reference to converted Project |
| `acquisition_cost` | Decimal? | Lead acquisition cost (if purchased) |
| `created_at` | DateTime | Lead creation |
| `assigned_at` | DateTime | Agent assignment |
| `resolved_at` | DateTime? | Lead resolution |

### 1.2 Lead Entity Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| User (lead) | 0:1 | Existing user if identified via identity resolution |
| User (agent) | N:1 | Assigned agent |
| Project | 0:1 | Converted project |
| Organization | N:1 | Target organization |
| LeadPurchase | 0:1 | If lead was purchased |
| Feedback | 0:N | Feedback records attached to lead |
| Event | 1:N | Audit trail events |

---

## 2. 8-Stage CRM Pipeline

The CRM pipeline processes every incoming lead through 8 sequential stages. Each stage transforms the lead data and produces enriched output consumed by the next stage.

```
incoming_message
    → normalize_text
        → extract_entities
            → detect_intent
                → context_enrichment
                    → lead_scoring
                        → lead_classification
                            → crm_routing
```

### 2.1 Stage Details

| Stage | Description | Input | Output | Engine |
|-------|-------------|-------|--------|--------|
| 1. **Incoming** | Raw message received from any channel | Source text, channel metadata, sender info | Lead record with `pipeline_stage=incoming` | Channel receiver (WhatsApp/Telegram/Dashboard/API) |
| 2. **Normalize** | Text normalization pipeline | `source_text` | `normalized_text`: lowercase, unicode normalized, whitespace collapsed, punctuation standardized | Normalizer service |
| 3. **Extract** | Entity extraction | `normalized_text` | Extracted entities: phone, email, name, city, neighborhood, budget, property type, timeline | Entity extractor (regex + keyword) |
| 4. **Intent Detect** | Intent classification | `normalized_text` + extracted entities | `detected_intent`, `intent_confidence`, `lead_type` | Intent classifier (KLASS engine) |
| 5. **Enrich** | Context enrichment | Lead data + extracted entities | Enriched fields: `is_diaspora`, `cash_purchase`, `urgency`, `language`, `user_id` (via identity resolution) | Enrichment service |
| 6. **Score** | Lead scoring calculation | All enriched fields | `base_score`, `boosters_applied[]`, `penalties_applied[]`, `total_boost`, `total_penalty`, `final_score` | Scoring engine |
| 7. **Classify** | Lead classification | `final_score` | `classification` (hot/warm/cold/low/spam), `sla_priority`, `sla_deadline` | Classification rules |
| 8. **Route** | CRM routing | Classified lead | `routed_to_agent_id`, `routed_at`, `routing_method` | Routing engine |

### 2.2 Pipeline Error Handling

| Error | Fallback |
|-------|----------|
| Entity extraction fails | Proceed with empty entities; score penalty applied |
| Intent detection confidence < 0.70 | Classify as LOW; route for manual qualification |
| Identity resolution failure | Proceed as unlinked lead; no user_id |
| Scoring overflow (final_score > 150) | Cap at 150 |
| No eligible agent for routing | Escalate to admin/manual routing queue |
| Fraud layer triggered | Suspend pipeline; apply fraud_action_taken before proceeding |

---

## 3. Lead Scoring Engine

### 3.1 Base Scores by Lead Type

| Lead Type | Base Score | Description |
|-----------|-----------|-------------|
| `tenant` | 40 | Rental seeker |
| `buyer` | 60 | Property buyer |
| `seller` | 50 | Property seller |
| `investor` | 80 | Real estate investor |
| `diaspora_investor` | 95 | Diaspora investor (highest priority) |

### 3.2 Score Boosters (13)

| # | Booster | Value | Detection Condition | Priority |
|---|---------|-------|--------------------|----------|
| 1 | `budget_detected` | +15 | Budget range (min/max) successfully extracted from text | High |
| 2 | `city_detected` | +10 | City name extracted and matched to known city list | High |
| 3 | `neighborhood_detected` | +10 | Neighborhood name extracted and matched to known neighborhoods | High |
| 4 | `urgency_detected` | +20 | Urgency keywords detected: `urgent`, `vite`, `rapidement`, `immédiat`, `ASAP`, `dès que possible`, `need now` | Medium |
| 5 | `diaspora` | +25 | Diaspora indicator detected: foreign country code, diaspora keywords (`diaspora`, `from abroad`, `de l'étranger`), international IP | High |
| 6 | `cash_purchase` | +15 | Cash purchase keywords: `cash`, `comptant`, `sans prêt`, `no loan`, `without mortgage` | High |
| 7 | `property_type_specified` | +5 | Property type extracted: `appartement`, `maison`, `villa`, `terrain`, `bureau`, `studio`, etc. | Low |
| 8 | `timeline_specified` | +10 | Timeline extracted: `this month`, `next week`, `d'ici 3 mois`, `avant décembre`, `immediately` | Medium |
| 9 | `multiple_criteria` | +10 | 3+ distinct criteria detected: budget + location + type + surface + bedrooms + features | Medium |
| 10 | `professional` | +15 | Professional profile detected: professional email domain, business keywords, RCCM mention, professional category match | High |
| 11 | `referral` | +10 | Referral detected: `recommendation`, `referred by`, `parrain`, `ami`, `colleague`, referral code in message | Medium |
| 12 | `complete_profile` | +10 | Complete contact info: phone + email + name all present, message contains 3+ contact fields | Low |
| 13 | `verified_phone` | +10 | Phone number matches an existing user with `phone_verified = true` in identity resolution | Low |

**Total maximum possible boost:** +165 (all boosters triggered)

### 3.3 Score Penalties (8)

| # | Penalty | Value | Detection Condition | Severity |
|---|---------|-------|--------------------|----------|
| 1 | `missing_budget` | -10 | No budget range extracted after entity extraction phase | Medium |
| 2 | `unclear_location` | -10 | No city or neighborhood extracted; location references are vague (`somewhere`, `en ville`, `là-bas`) | Medium |
| 3 | `spam_like` | -50 | Spam patterns: repeated characters (`achete!!!!`), ALL CAPS segments, excessive punctuation, known spam keywords (`free`, `win`, `gagnez`, `100%`) | Critical |
| 4 | `too_short` | -20 | Message length < 10 characters after normalization; single word messages | High |
| 5 | `external_links` | -30 | Message contains external URLs (http/https/ftp); contact sharing links (WhatsApp links, Telegram invites) | High |
| 6 | `duplicate_message` | -20 | Same normalized_text detected from same sender within 24h window; SHA-256 fingerprint match in recent leads | High |
| 7 | `aggressive_language` | -30 | Aggressive keywords: abuse, threats, harassment patterns; sentiment analysis score < -0.5 | High |
| 8 | `impossible_request` | -40 | Request contradicts known reality: budget < 1M FCFA for house in upscale neighborhood, rent > 5M FCFA for studio, contradictory criteria detected | Critical |

**Total maximum possible penalty:** -210 (all penalties triggered)

### 3.4 Score Formula

```
final_score = max(0, min(150, base_score + sum(boosters_applied[].value) - sum(penalties_applied[].value)))
```

- **Minimum final score:** 0
- **Maximum final score:** 150 (capped)
- **Score overflow protection:** scores above 150 are capped; scores below 0 are floored

### 3.5 Scoring Engine Implementation Notes

| Aspect | Detail |
|--------|--------|
| Execution | Synchronous within pipeline stage 6 |
| Idempotency | Re-scoring produces same result for same input data |
| Caching | Boosters/penalties stored as JSON arrays on Lead for audit |
| Re-scoring triggers | On entity update, on manual override, on identity link/unlink |
| Extensibility | Booster/penalty registry is configurable via admin interface |

---

## 4. Lead Classification

### 4.1 Classification Thresholds

| Classification | Score Range | SLA Priority | Target Response | Action |
|---------------|-------------|-------------|-----------------|--------|
| **HOT** | 80-150 | P0 | < 30 minutes | Immediate route; real-time notification to assigned agent; escalation if no response within 15min |
| **WARM** | 60-79 | P1 | < 2 hours | Route within priority queue; standard notification |
| **COLD** | 40-59 | P2 | < 24 hours | Route in standard queue; daily digest notification |
| **LOW** | 20-39 | P3 | J+1 to J+7 | Queue for batch processing; weekly assignment |
| **SPAM** | 0-19 | — | Block/Quarantine | Not routed; quarantined for admin review; sender may be rate-limited or blocked |

### 4.2 Classification Overrides

| Condition | Override Classification | Rationale |
|-----------|------------------------|-----------|
| Fraud layer 4 triggered (suspicious urgency) | SPAM regardless of score | Security precaution |
| Identity resolution matches blocked user | SPAM regardless of score | User-level block enforcement |
| Manual override by admin | As specified by admin | Human judgment supersedes algorithm |
| `is_fraud = true` and any fraud layer triggered | SPAM | Anti-fraud escalation |
| Diaspora + investor lead with score > 70 | Upgrade to HOT | Business rule: diaspora has priority |

---

## 5. CRM Routing Engine

### 5.1 Routing Methods

| Method | Algorithm | When Used | Fallback |
|--------|-----------|-----------|----------|
| **Zone-based** | Match lead's detected city/neighborhood to agent's assigned `zones[]`. Route to agent with matching zone and lowest current lead count. | Primary method: city or neighborhood detected | Fallback to availability-based if no zone match |
| **Availability-based** | Route to agent in the organization with lowest `current_leads / max_leads` ratio who is online and accepting leads. | Primary method: no geographic data | Fallback to score-based if all agents at capacity |
| **Score-based** | Route to agent with highest `agent_rating` who is in the lead's zone or general pool. | Tiebreaker: zone + availability produce multiple candidates | Manual if no agent meets threshold |
| **Manual** | Admin/manager selects agent from organization member list. | Override: admin manually assigns via dashboard | N/A |

### 5.2 Routing Decision Tree

```
Is city/neighborhood detected?
  └─ YES → Zone-based routing
       └─ Zone match found?
            ├─ YES → Route to matched zone agent (lowest load wins)
            └─ NO → Availability-based routing
  └─ NO → Availability-based routing
       └─ Agent available?
            ├─ YES → Route to least-loaded available agent
            └─ NO → Score-based routing
                 └─ Agent meets score threshold?
                      ├─ YES → Route to highest-rated eligible agent
                      └─ NO → Manual routing queue (admin notification)
```

### 5.3 Routing Rules

| Rule | Description |
|------|-------------|
| Agent opt-in | Agent must have `is_active_agent = true` and consent to lead routing |
| Lead capacity | Agent must have `current_leads < max_leads` |
| SPAM exclusion | SPAM-classified leads are never routed; sent to quarantine |
| Lead cap per agent | Configurable `max_leads` per agent (OrganizationMember setting) |
| Round-robin within zone | Equal distribution among agents in same zone |
| Re-routing on no-response | If agent does not respond within SLA deadline, re-route to next available agent |
| Admin escalation | If no agent available after 3 routing attempts, escalate to admin |

---

## 6. Anti-Fraud Detection Layers

### 6.1 Layer Definitions

| Layer | Name | Detection Signal | Score Impact | Action | Cooldown |
|-------|------|-----------------|-------------|--------|----------|
| 1 | **Broker spam** | Same phone or email submitting > 5 leads within 1 hour window | N/A (pipeline halted) | Flag lead `is_fraud=true`; rate-limit sender for 24h; notify admin | 24h |
| 2 | **Duplicate listing** | Same property details (address + type + price within 10%) from > 2 different sender accounts within 7 days | -50 penalty + layer recorded | Flag lead `is_fraud=true`; mark all duplicates for merge investigation; notify admin | 7d |
| 3 | **Fake price** | Requested price deviates > 300% from market average for same property type and neighborhood | -40 penalty (impossible_request booster not double-applied) | Flag for verification; require admin validation before routing | — |
| 4 | **Suspicious urgency** | Aggressive language + no extracted details + external links present | Classification override → SPAM | Flag `is_fraud=true`; temporary account suspension; admin review required | Pending admin review |

### 6.2 Fraud Action Matrix

| Action | Effect | Duration | Reversal |
|--------|--------|----------|----------|
| `flag` | Lead marked `is_fraud=true`; proceeds in pipeline with SPAM classification; visible in fraud review queue | Permanent (until admin clears) | Admin clears flag |
| `rate_limit` | Sender blocked from submitting new leads for cooldown period | 24h (Layer 1) / 7d (Layer 2) | Auto-expiry |
| `temporary_suspend` | Sender account temporarily suspended; all pending leads blocked | Until admin review | Admin unsuspends |
| `block` | Sender permanently blocked; existing leads archived | Permanent | Admin unblock (audit trail) |

### 6.3 Fraud Detection Pipeline

```
Lead Submitted
  → Layer 1 (Broker spam) — check frequency by phone/email
      → PASS → Layer 2 (Duplicate listing) — check property detail fingerprints
          → PASS → Layer 3 (Fake price) — check against market averages
              → PASS → Layer 4 (Suspicious urgency) — check language + details + links
                  → CLEAN → proceed to scoring
              → FAIL → SPAM override → admin notification
          → FAIL → penalty applied → flag for investigation
      → FAIL → rate-limit → flag for merge investigation
  → FAIL → rate-limit → admin notification
```

---

## 7. Behavior Tracking Fields

### 7.1 Tracked Behaviors

| # | Behavior | Field(s) on Lead/User | Tracking Method | Usage |
|---|----------|----------------------|-----------------|-------|
| 1 | **Message history** | Lead has `source_text` + all `events` with kind `lead.*` | Event audit trail: every pipeline transition, every agent response, every user message | Full conversation reconstruction; response quality analysis |
| 2 | **Response time** | `first_response_at - created_at` computed on Lead | Timestamp diff on `first_response_at` set | Agent SLA compliance; routing optimization; score input (faster response → higher trust) |
| 3 | **Response rate** | Stored on User: `response_rate` Float | Computed: messages responded to / total messages received per agent per period | Agent quality; routing score weight |
| 4 | **Budget changes** | JSON array on Lead: `budget_changes[]` with `{previous_min, previous_max, new_min, new_max, changed_at}` | Tracked on every Lead update where budget_min or budget_max changes | Lead stability signal; scoring re-evaluation trigger |
| 5 | **Visit requests** | Count on User derived from `events: visit.requested` | Sum of Event records with kind `visit.requested` for this user | Engagement signal; scoring booster |
| 6 | **Visit completion** | `visit_completion_rate` Float on User | Computed: visit.completed / visit.requested per user | Reliability signal; scoring factor |
| 7 | **Negotiation history** | JSON array summary on User: `negotiation_history[]` with `{count, success_rate, avg_offer_count, avg_duration}` | Aggregated from Transaction and Conversation events | Lead quality; success prediction |
| 8 | **Complaint history** | `complaint_count` Int + `complaint_types[]` String on User | Count and type from Event `complaint.*` events | Trust signal; fraud indicator; scoring penalty |

### 7.2 Behavior Scoring Integration

| Behavior | Scoring Impact | Weight |
|----------|---------------|--------|
| Fast response time (< 5min) | +5 to agent rating contribution | Indirect |
| High response rate (> 90%) | Priority in score-based routing | Routing weight |
| Frequent budget changes (> 3 in 30d) | -10 penalty on re-scoring (unstable lead) | Low |
| High visit completion (> 80%) | +10 booster (reliable lead) | Medium |
| Negotiation success rate (> 50%) | +5 booster converted lead bonus | Low |
| Complaint count > 3 | -20 penalty; flag for review | High |

---

## 8. SLA by Priority

### 8.1 SLA Thresholds

| Priority | Code | Target Response | Classification | Business Impact |
|----------|------|----------------|---------------|-----------------|
| **Priority 0** | P0 | < 30 minutes | HOT | Highest value leads (investors, diaspora); immediate loss if missed |
| **Priority 1** | P1 | < 2 hours | WARM | Qualified leads with clear intent; moderate value |
| **Priority 2** | P2 | < 24 hours | COLD | Standard leads; lower urgency but still viable |
| **Priority 3** | P3 | J+1 to J+7 | LOW | Exploration leads; batch-processed; lowest value |

### 8.2 SLA Enforcement

| Mechanism | Description |
|-----------|-------------|
| `sla_deadline` | Computed on classification: `created_at + SLA_duration[priority]` |
| `sla_breached` | Set to `true` when `now > sla_deadline AND first_response_at IS NULL` |
| Breach detection | Cron job runs every 5 minutes; checks all leads where `sla_breached = false AND first_response_at IS NULL AND now > sla_deadline` |
| Breach event | Fires `lead.sla_breached` event; notifies agent + admin |
| Breach action | P0 breach: immediate re-route to next available agent + admin alert; P1 breach: admin notification; P2/P3 breach: logged for reporting |
| Agent SLA stats | Aggregated per agent: `sla_breach_count`, `avg_response_time`, `sla_compliance_rate` |

### 8.3 SLA Monitoring

| Metric | Computation | Target |
|--------|-------------|--------|
| P0 response rate | `P0 leads responded within 30min / total P0 leads` | > 95% |
| P1 response rate | `P1 leads responded within 2h / total P1 leads` | > 90% |
| P2 response rate | `P2 leads responded within 24h / total P2 leads` | > 85% |
| P3 response rate | `P3 leads responded within 7d / total P3 leads` | > 75% |
| Overall SLA compliance | Weighted average across all priorities | > 85% |

---

## 9. Agent Rating System

### 9.1 Rating Scale

| Score | Label | Description |
|-------|-------|-------------|
| 5 | Excellent | Exceptional service; exceeds expectations |
| 4 | Good | Satisfactory service; meets expectations |
| 3 | Average | Acceptable service; neutral experience |
| 2 | Below Average | Unsatisfactory; needs improvement |
| 1 | Poor | Unacceptable; requires intervention |

### 9.2 Rating Collection

| Trigger | Channel | Timing | Target |
|---------|---------|--------|--------|
| Post-lead resolution | WhatsApp/Telegram | Within 1h of lead resolution | Lead → Agent interaction |
| Post-visit | WhatsApp/Telegram/Dashboard | Within 2h of visit completion | Visit → Agent accompaniment |
| Post-transaction | Dashboard/Email | Within 24h of transaction completion | Transaction → Agent service |
| Manual | Dashboard | Anytime by user | Any interaction |

### 9.3 Rating Calculation

```
agent_rating = weighted_average(
    sum(rating_n * weight_n) / sum(weight_n)
)
```

| Rating Source | Weight | Decay |
|---------------|--------|-------|
| Lead resolution feedback | 1.0 | None |
| Post-visit feedback | 1.5 | None |
| Post-transaction feedback | 2.0 | None |
| Manual dashboard rating | 1.0 | 50% after 90 days |

### 9.4 Rating Display

| Context | Display |
|---------|---------|
| Agent profile | `agent_rating` rounded to 1 decimal (e.g., 4.3) |
| Routing engine | Use as score-based routing dimension |
| Lead assignment UI | Star visualization + numeric score |
| Agent dashboard | Trend over time (30d, 90d, all time) |

---

## 10. Feedback Handling System

### 10.1 Feedback Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `lead_id` | UUID? | Source lead (if feedback originated from lead interaction) |
| `user_id` | UUID | User providing feedback |
| `agent_id` | UUID? | Agent being rated (if applicable) |
| `organization_id` | UUID? | Organization context |
| `feedback_type` | Enum | `rating \| complaint \| suggestion \| compliment \| report_issue` |
| `rating` | Int? | 1-5 rating (if feedback_type = rating) |
| `category` | Enum? | `service_quality \| response_time \| professionalism \| accuracy \| communication \| technical \| other` |
| `description` | Text | Free-form feedback text |
| `status` | Enum | `submitted \| acknowledged \| in_review \| resolved \| escalated \| closed` |
| `resolution_notes` | Text? | Admin/agent resolution notes |
| `resolved_by` | UUID? | Admin who resolved |
| `resolved_at` | DateTime? | Resolution timestamp |
| `escalated_to` | UUID? | Escalation target |
| `is_public` | Boolean | Whether feedback is publicly visible |
| `created_at` | DateTime | Submission timestamp |

### 10.2 Feedback Lifecycle

```
Submitted → Acknowledged → In Review → Resolved → Closed
                                   → Escalated → In Review → Resolved → Closed
```

### 10.3 Feedback Processing Rules

| Rule | Description |
|------|-------------|
| Auto-acknowledgment | Feedback `submitted` → `acknowledged` automatically within 5 minutes |
| Priority escalation | Rating ≤ 2 OR complaint type → auto-priority, assign to admin within 1h |
| Resolution SLA | Standard: 48h; Complaints: 24h; Escalated: 4h |
| Feedback aggregation | Daily/weekly/monthly reports generated for agent, organization, platform levels |
| Agent response | Agent can reply to feedback via dashboard; reply appended to feedback record |
| Public visibility | Ratings are public; complaint/suggestion details are private (admin only) |
| Feedback score | Aggregate `feedback_score`: `(positive_feedback - negative_feedback) / total_feedback * 100` |

### 10.4 Feedback Reports

| Report | Frequency | Audience | Content |
|--------|-----------|----------|---------|
| Agent feedback summary | Weekly | Agent | Rating trend, response rate, top categories |
| Organization feedback | Monthly | Agency admin | Per-agent breakdown, organizational trends |
| Platform feedback | Monthly | Platform admin | Overall satisfaction, category distribution, improvement areas |
| SLA compliance report | Weekly | Operations | Per-priority SLA stats, breach analysis |

---

## 11. Complete Extension Mapping Table

### 11.1 CRM Pipeline Extensions

| Extension ID | Source Concept | Target Entity | Proposed Structure | Priority | Human Decision |
|-------------|---------------|---------------|-------------------|----------|----------------|
| EXT-CRM-001 | Lead scoring engine (base + boosters - penalties) | Lead | Lead scoring engine module; base_scores, boosters_applied[], penalties_applied[] on Lead | P1 | N |
| EXT-CRM-002 | Score boosters (13 boosters) | Lead | Configurable booster registry; 13 boosters with values and detection conditions | P1 | Y — weights/criteria |
| EXT-CRM-003 | Score penalties (8 penalties) | Lead | Configurable penalty registry; 8 penalties with values and detection conditions | P1 | Y — weights/criteria |
| EXT-CRM-004 | Lead classification (5 classes) | Lead | Classification thresholds HOT/WARM/COLD/LOW/SPAM; class assignment logic | P1 | Y — thresholds |
| EXT-CRM-005 | CRM routing engine | Lead/OrganizationMember | Routing engine: zone, availability, score, manual methods; agent zone assignment | P1 | Y — strategy |
| EXT-CRM-006 | 7-factor CRM scoring | Lead | Extended scoring with 7 factors (budget, location, urgency, diaspora, cash, property, timeline) | P2 | Y — factor weights |
| EXT-CRM-007 | Behavior tracking fields | Lead/User | 8 tracked behaviors: message_history, response_time, response_rate, budget_changes, visit_requests, visit_completion, negotiation_history, complaint_history | P2 | N |
| EXT-CRM-008 | Anti-fraud detection (4 layers) | Lead | 4 fraud detection layers: broker_spam, duplicate_listing, fake_price, suspicious_urgency | P2 | Y — automation level |
| EXT-CRM-009 | Agent rating system | User/OrganizationMember | Post-interaction rating 1-5; weighted average calculation; display on agent profile | P2 | Y — calculation method |
| EXT-CRM-010 | Feedback handling system | Feedback (new entity) | Feedback entity with lifecycle; collection, aggregation, reporting module | P3 | N |
| EXT-CRM-011 | Lead SLA by priority | Lead | SLA thresholds P0<30min, P1<2h, P2<24h, P3=J+1 to J+7; breach detection and escalation | P1 | Y — thresholds |

### 11.2 CRM Monetized Service Extensions

| Extension ID | Source Concept | Target Entity | Proposed Structure | Priority | Human Decision |
|-------------|---------------|---------------|-------------------|----------|----------------|
| EXT-SVC-CRM-001 | Lead Bronze (1 contact at 500 FCFA) | LeadPurchase | LeadPurchase model with lead_bronze pack; 500 FCFA/lead | P1 | Y — pricing |
| EXT-SVC-CRM-002 | Lead Silver (5 contacts at 1,500 FCFA) | LeadPurchase | LeadPurchase with lead_silver pack; tiered pricing (300 FCFA/lead) | P1 | N |
| EXT-SVC-CRM-003 | Lead Gold (15 contacts at 3,000 FCFA) | LeadPurchase | LeadPurchase with lead_gold pack; tiered pricing (200 FCFA/lead) | P1 | N |
| EXT-SVC-CRM-004 | Déblocage coordonnées propriétaire (500 FCFA) | LeadPurchase | Coordinate unlock as distinct purchase type; separate from lead purchase | P1 | Y — mechanism |
| EXT-SVC-CRM-005 | Demandeur Premium (1,000 FCFA) | User | Premium seeker profile; priority visibility features | P4 | Y — features |
| EXT-SVC-CRM-006 | Diaspora Simple (25,000 FCFA) | ServiceOrder | Diaspora service tier; verified property access | P3 | Y — scope |
| EXT-SVC-CRM-007 | Diaspora Rapport (50,000 FCFA) | ServiceOrder | Diaspora mid-tier; accompaniment + property reports | P3 | N |
| EXT-SVC-CRM-008 | Diaspora Complet (75,000 FCFA) | ServiceOrder | Diaspora premium tier; full accompaniment package | P3 | N |
| EXT-SVC-CRM-009 | Agent Business subscription (25,000 FCFA/month) | ServiceOrder | Premium agent subscription; enhanced features and lead allocation | P2 | Y — features |

### 11.3 All CRM-* Fields Extension Table

| Field | Entity | Type | Extension Source | Description |
|-------|--------|------|------------------|-------------|
| `source_channel` | Lead | Enum | EXT-CRM-001 | Originating channel (whatsapp/telegram/dashboard/api/referral) |
| `source_text` | Lead | Text | EXT-CRM-001 | Original incoming message |
| `normalized_text` | Lead | Text | EXT-CRM-001 | Normalized text for processing |
| `language` | Lead | Enum | EXT-CRM-001 | Detected language (fr/en/pid) |
| `pipeline_stage` | Lead | Enum | EXT-CRM-001 | Current 8-stage pipeline position |
| `detected_intent` | Lead | Enum? | EXT-CRM-001 | Detected primary intent |
| `intent_confidence` | Lead | Float? | EXT-CRM-001 | Confidence score 0.0-1.0 |
| `lead_type` | Lead | Enum? | EXT-CRM-001 | tenant/buyer/seller/investor/diaspora_investor |
| `base_score` | Lead | Int | EXT-CRM-001 | Base score by lead type |
| `boosters_applied` | Lead | JSON[] | EXT-CRM-002 | Array of booster {type, value} |
| `penalties_applied` | Lead | JSON[] | EXT-CRM-003 | Array of penalty {type, value} |
| `total_boost` | Lead | Int | EXT-CRM-001 | Sum of all booster values |
| `total_penalty` | Lead | Int | EXT-CRM-001 | Sum of all penalty values |
| `final_score` | Lead | Int | EXT-CRM-001 | Computed: base + total_boost - total_penalty |
| `classification` | Lead | Enum | EXT-CRM-004 | hot/warm/cold/low/spam |
| `routed_to_agent_id` | Lead | UUID? | EXT-CRM-005 | Assigned agent |
| `routed_at` | Lead | DateTime? | EXT-CRM-005 | Route assignment timestamp |
| `routing_method` | Lead | Enum? | EXT-CRM-005 | zone/availability/score/manual |
| `is_fraud` | Lead | Boolean | EXT-CRM-008 | Fraud flag |
| `fraud_layers_triggered` | Lead | String[] | EXT-CRM-008 | Which layers fired |
| `fraud_action_taken` | Lead | Enum? | EXT-CRM-008 | none/flag/temporary_suspend/block |
| `user_id` | Lead | UUID? | EXT-CRM-001 | Linked user |
| `phone` | Lead | String | EXT-CRM-001 | Contact phone |
| `email` | Lead | String? | EXT-CRM-001 | Contact email |
| `name` | Lead | String | EXT-CRM-001 | Contact name |
| `city` | Lead | String? | EXT-CRM-006 | Detected city |
| `neighborhood` | Lead | String? | EXT-CRM-006 | Detected neighborhood |
| `budget_min` | Lead | Decimal? | EXT-CRM-006 | Budget range min |
| `budget_max` | Lead | Decimal? | EXT-CRM-006 | Budget range max |
| `urgency` | Lead | Enum? | EXT-CRM-006 | low/medium/high/urgent |
| `is_diaspora` | Lead | Boolean | EXT-CRM-002 | Diaspora indicator |
| `cash_purchase` | Lead | Boolean | EXT-CRM-002 | Cash purchase indicator |
| `sla_priority` | Lead | Enum | EXT-CRM-011 | p0/p1/p2/p3 |
| `sla_deadline` | Lead | DateTime | EXT-CRM-011 | SLA response deadline |
| `first_response_at` | Lead | DateTime? | EXT-CRM-011 | First agent response timestamp |
| `sla_breached` | Lead | Boolean | EXT-CRM-011 | SLA breach flag |
| `converted_to_project` | Lead | Boolean | EXT-CRM-001 | Conversion flag |
| `converted_project_id` | Lead | UUID? | EXT-CRM-001 | Reference to Project |
| `acquisition_cost` | Lead | Decimal? | EXT-SVC-CRM-001 | Lead cost |
| `created_at` | Lead | DateTime | EXT-CRM-001 | Lead creation |
| `assigned_at` | Lead | DateTime | EXT-CRM-005 | Agent assignment |
| `resolved_at` | Lead | DateTime? | EXT-CRM-001 | Lead resolution |
| `agent_rating` | User | Float | EXT-CRM-009 | 1-5 computed rating |
| `lead_capacity` | OrganizationMember | Int | EXT-CRM-005 | Max concurrent leads per agent |
| `current_leads` | OrganizationMember | Int | EXT-CRM-005 | Current active leads per agent |
| `zones` | OrganizationMember | String[] | EXT-CRM-005 | Assigned geographic zones |
| `response_rate` | User | Float | EXT-CRM-007 | Messages responded / total received |
| `response_time` | User | Float | EXT-CRM-007 | Average response time |
| `visit_completion_rate` | User | Float | EXT-CRM-007 | Visits completed / requested |
| `complaint_count` | User | Int | EXT-CRM-007 | Number of complaints |

### 11.4 New Entities

| Entity | Description | Extensions |
|--------|-------------|------------|
| `Lead` | Central CRM entity; represents inbound contact with full pipeline tracking | EXT-CRM-001 through EXT-CRM-011 |
| `Feedback` | User-submitted feedback on agent/service interactions | EXT-CRM-010 |
| `LeadPurchase` | Agent purchase of lead contact information | EXT-SVC-CRM-001 through EXT-SVC-CRM-004 |

---

*End of CRM_EXTENSION_MODEL.md — 11 sections, 11 CRM extensions, 9 monetized service extensions, 48 enriched fields, 3 new entities defined.*
