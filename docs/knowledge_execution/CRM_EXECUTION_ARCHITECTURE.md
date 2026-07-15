# CRM Execution Architecture — LAWIM Heritage Gold

**Source:** CRM_MODEL.md, RULE_INDEX.md (CRM-001 to CRM-015), ROLE_MODEL.md
**Mission:** H0 — LAWIM Heritage Gold
**Date:** 15 juillet 2026

---

## 1. Rule Consumption — CRM-001 to CRM-015

| Rule | Domain | Consumption Pattern | Engine Component |
|------|--------|-------------------|-----------------|
| CRM-001 | 7 roles hierarchy | Role loader on startup, cached in `role_registry` | `crm_engine/role_manager.py` |
| CRM-002 | 7×7 permission matrix | Matrix loaded into `permission_gate` — each API call checked against role+resource | `crm_engine/permission_gate.py` |
| CRM-003 | 7 user states | State machine transitions enforced by `user_state_machine` — guards prevent illegal transitions | `crm_engine/state_machine.py` |
| CRM-004 | 11 event types | Event bus dispatches typed events to registered handlers; each event triggers pipeline stage | `crm_engine/event_bus.py` |
| CRM-005 | Agent Opt-In 4 steps | `optin_service` intercepts agent assignment; checks consent in `agent_optins` before sharing | `crm_engine/optin_service.py` |
| CRM-006 | Agent Rating 1-5 | `rating_service` aggregates feedback after each interaction; stored in `agents.rating` | `crm_engine/rating_service.py` |
| CRM-007 | Lead price 500 FCFA | `pricing_service` calculates lead cost; overridable by agent tier | `crm_engine/pricing_service.py` |
| CRM-008 | Identity resolution | `identity_resolver` runs duplicate detection on create/update; scores merge candidates | `crm_engine/identity_resolver.py` |
| CRM-009 | Master Dashboard password | `auth_service` validates master credentials; separate from user auth chain | `crm_engine/auth_service.py` |
| CRM-010 | 20 CRM tables | Schema loaded from `implement_all.sql`; ORM models in `crm_engine/models/` | `crm_engine/models/` |
| CRM-011 | Diaspora services | `diaspora_service` manages service_type, price, status per client_phone | `crm_engine/diaspora_service.py` |
| CRM-012 | 6 external partners | `partner_registry` maps partner type to contact/API endpoint; used in routing | `crm_engine/partner_registry.py` |
| CRM-013 | 18 actors | `actor_resolver` resolves entity to one of 18 actor types; used in permission checks | `crm_engine/actor_resolver.py` |
| CRM-014 | CRM scoring V5 7 factors | `scoring_engine` applies weighted factors; result normalized 0-1 | `crm_engine/scoring_engine.py` |
| CRM-015 | Role hierarchy | `hierarchy_resolver` resolves transitive permissions: Master→Vice-Master→Assistant→Agence→Agent→Vendeur→Demandeur | `crm_engine/hierarchy_resolver.py` |

### Rule Evaluation Pipeline

```
incoming_event → rule_selector → rule_evaluator → action_dispatcher
                      │                │
                      ↓                ↓
              rule_conditions     rule_actions
              (preconditions)     (side effects)
```

- **Rule Selector:** Matches event type + entity state to applicable rules
- **Rule Evaluator:** Evaluates conditions; short-circuits on first match
- **Action Dispatcher:** Executes side effects (state change, notification, routing)

---

## 2. Role Hierarchy (CRM-001, CRM-015)

| Level | Role | Parent | Permission Inheritance |
|-------|------|--------|----------------------|
| 1 | demandeur | — | Base read-only |
| 2 | vendeur/propriétaire | demandeur | Inherits L1 + create/edit own |
| 3 | agent | vendeur | Inherits L2 + manage leads |
| 4 | agence | agent | Inherits L3 + manage agents |
| 5 | assistant | agence | Inherits L4 + limited admin |
| 6 | vice_master | assistant | Inherits L5 + full admin (except critical) |
| 7 | master | vice_master | Inherits L6 + full system access |

**Inheritance rule:** Each level inherits all permissions of the level below, plus additional grants. Permission check traverses from L7 → L1.

### Role Families (from ROLE_MODEL.md)

| Family | Roles | Description |
|--------|-------|-------------|
| Demandeur | demandeur, buyer, tenant, investor, property_seeker | Search for property |
| Propriétaire | owner, seller, détenteur | List property |
| Agent | agent_immobilier, broker | Professional intermediary |
| Opérateur | responsable_agence, administrateur_agence, assistant | Agency operations |
| Superviseur | conseiller, médiateur, responsable_opérationnel | Oversight |
| Admin | administrateur, administrateur_principal, vice_master, master | System administration |

> **ARCHITECTURE_DECISION:** The 7-level role hierarchy and permission matrix are sourced from Heritage Gold CRM-001/CRM-002. Role-to-system-user mapping is an architecture decision for implementation.
> **DISTINCTION:** Role métier (demandeur, vendeur, agent) ≠ Rôle système (admin, moderator) ≠ Statut CRM (NEW_USER, SEARCHING_PROPERTY) ≠ Permission (read, write, admin). These four dimensions are orthogonal and must be implemented as separate attributes.

---

## 3. User States (CRM-003)

| State | Code | Entry Condition | Exit Condition | Next States |
|-------|------|-----------------|----------------|-------------|
| NEW_USER | `new_user` | User created | First interaction | SEARCHING_PROPERTY, PROPERTY_OWNER, INACTIVE |
| SEARCHING_PROPERTY | `searching_property` | Intent detected (buy/rent/invest) | Lead created or inactive >90d | LEAD_CREATED, INACTIVE |
| PROPERTY_OWNER | `property_owner` | Property published | Property archived or inactive >90d | LEAD_CREATED, INACTIVE |
| AGENT | `agent` | Agent onboarding complete | Subscription expires or deactivation | PREMIUM_AGENT, INACTIVE |
| LEAD_CREATED | `lead_created` | Lead score ≥ threshold | Lead converted or expired | SEARCHING_PROPERTY, INACTIVE |
| PREMIUM_AGENT | `premium_agent` | Agent activates paid subscription | Subscription lapses | AGENT, INACTIVE |
| INACTIVE | `inactive` | No activity for >90 days | User re-engages | NEW_USER |

### State Transition Guards

```
NEW_USER → SEARCHING_PROPERTY : intent_detected == true
NEW_USER → PROPERTY_OWNER      : property_created == true
NEW_USER → INACTIVE            : last_activity > 90d
SEARCHING_PROPERTY → LEAD_CREATED : lead_score ≥ threshold
SEARCHING_PROPERTY → INACTIVE     : last_activity > 90d
PROPERTY_OWNER → LEAD_CREATED     : lead_score ≥ threshold (as seller lead)
PROPERTY_OWNER → INACTIVE         : last_activity > 90d
AGENT → PREMIUM_AGENT             : subscription_active == true
AGENT → INACTIVE                  : deactivated || last_activity > 90d
LEAD_CREATED → SEARCHING_PROPERTY : re_engaged
LEAD_CREATED → INACTIVE           : last_activity > 90d
PREMIUM_AGENT → AGENT             : subscription_expired
PREMIUM_AGENT → INACTIVE          : deactivated || last_activity > 90d
INACTIVE → NEW_USER               : re_engaged
```

---

## 4. Event Types (CRM-004)

| Event | Trigger | Payload | Handlers |
|-------|---------|---------|----------|
| `message.received` | Incoming WhatsApp/Telegram | {channel, text, sender, timestamp} | normalize_text, extract_entities |
| `intent.detected` | Intent classifier | {intent, confidence, entities} | context_enrichment, lead_scoring |
| `user.created` | Registration | {user_id, role, channel} | state_machine → NEW_USER, identity_resolution |
| `user.state_changed` | State transition | {user_id, from_state, to_state, reason} | notification_service, audit_log |
| `property.created` | New listing | {property_id, owner_id, attributes} | matching_engine, index_service |
| `lead.created` | Lead qualified | {lead_id, person_id, score, priority} | routing_engine, agent_notification |
| `match.generated` | Lead × property match | {lead_id, property_id, score, rank} | notification_service, conversation_engine |
| `payment.success` | Payment confirmed | {transaction_id, service, amount, user_id} | subscription_service, access_grant |
| `subscription.renewed` | Subscription cycle | {subscription_id, agent_id, tier, expires_at} | state_machine, billing_service |
| `boost.applied` | Boost activated | {boost_id, property_id, type, expires_at} | visibility_service, index_update |
| `access.granted` | Permission granted | {user_id, resource, permission_level, granted_by} | permission_gate, audit_log |
| `feedback.submitted` | Rating received | {user_id, target_id, rating, comment} | rating_service, agent_profile |
| `fraud.detected` | Fraud signal | {alert_id, signal_type, entity_id, severity} | anti_fraud_service, block_user |

### Event Bus Architecture

```
Producer → Event Bus → [Queue] → Consumer Pool
                              ↓
                        Event Handlers
                        (fan-out by type)
```

- Events are idempotent where possible
- Failed handlers retry 3× with exponential backoff
- Dead-letter queue for events exceeding max retries

---

## 5. Permission Matrix 7×7 (CRM-002)

| Resource | Demandeur (L1) | Vendeur (L2) | Agent (L3) | Agence (L4) | Assistant (L5) | Vice-Master (L6) | Master (L7) |
|----------|:--------:|:--------:|:------:|:-------:|:---------:|:-----------:|:--------:|
| View public property | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| View own property | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create property | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Edit own property | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Edit any property | ❌ | ❌ | mandate | mandate | agency | ✅ | ✅ |
| Delete property | ❌ | own | mandate | mandate | agency | ✅ | ✅ |
| View leads | ❌ | own | assigned | agency | agency | ✅ | ✅ |
| Create lead | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Assign lead | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| View users | ❌ | ❌ | ❌ | team | agency | ✅ | ✅ |
| Create user | self | self | self | ✅ | ✅ | ✅ | ✅ |
| Edit user role | ❌ | ❌ | ❌ | agent | agent | ✅ | ✅ |
| Create agency | ❌ | request | request | ❌ | ❌ | ✅ | ✅ |
| Validate agency | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| View reports | ❌ | ❌ | own | agency | agency | ✅ | ✅ |
| System config | ❌ | ❌ | ❌ | ❌ | ❌ | limited | ✅ |
| Audit logs | ❌ | ❌ | ❌ | ❌ | limited | ✅ | ✅ |
| Manage partners | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

**Rule:** Permission resolution follows role hierarchy CRM-015: a Master inherits all grants of lower roles. Denials are explicit and override inheritance at the same level.

---

## 6. Pipeline Management

### 6.1 Lead Lifecycle

```
incoming → qualification → scoring → classified → assigned → contacted → negotiating → converted → closed
   ↑                                                                                                      │
   └────────────────────────────────────── recycle ──────────────────────────────────────────────────────┘
```

| Stage | Entry Criteria | Exit Criteria | Owner |
|-------|---------------|--------------|-------|
| incoming | Message received | Entities extracted | pipeline_engine |
| qualification | Entities + intent known | Score calculated | scoring_engine |
| scoring | Lead profile complete | Classification assigned | classifier |
| classified | Score ≥ threshold | Agent assigned | router |
| assigned | Agent confirmed | First contact made | agent |
| contacted | First message sent | Response received | agent |
| negotiating | Active discussion | Agreement or rejection | agent |
| converted | Transaction signed | Lead closed | agent |
| closed | Final status set | — | system |

### 6.2 Contact Lifecycle

```
lead_contact → first_response → follow_up_1 → follow_up_7 → follow_up_30 → follow_up_90 → archived
```

| Milestone | Timing | Action |
|-----------|--------|--------|
| first_response | < 1h (P0), < 2h (P1), < 24h (P2), J+1–7 (P3) | Template message |
| follow_up_1 | J+1 | Re-engage |
| follow_up_7 | J+7 | Send new listings |
| follow_up_30 | J+30 | Check budget changes |
| follow_up_90 | J+90 | Final re-engagement |
| archived | > 12 months inactive | Moved to long-term storage |

### 6.3 Customer Lifecycle

```
prospect → qualified_lead → active_customer → repeat_customer → advocate → churned
```

| Stage | Criteria |
|-------|----------|
| prospect | First interaction, no qualification |
| qualified_lead | Intent + contact info captured |
| active_customer | Transaction completed |
| repeat_customer | ≥ 2 transactions |
| advocate | Referrals generated |
| churned | No activity > 365 days |

### 6.4 Partner Lifecycle

```
identified → vetted → onboarded → active → inactive
```

| Stage | Criteria | Assignment |
|-------|----------|-----------|
| identified | Partner type matched (notaire, géomètre, etc.) | system |
| vetted | Credentials verified | assistant/master |
| onboarded | Service agreement signed | assistant |
| active | Currently accepting referrals | partner |
| inactive | Opted out or non-responsive | system |

### 6.5 Agent Lifecycle

```
registered → verified → active → premium → inactive
```

| Stage | Criteria | Actions |
|-------|----------|---------|
| registered | Account created | Receive basic leads |
| verified | Phone + CNI validated | Full lead access |
| active | Onboarding complete | Lead routing eligible |
| premium | Subscription active | Priority routing, more leads |
| inactive | Subscription lapsed or deactivated | No lead routing |

---

## 7. Assignment Rules

### 7.1 Zone-Based Routing

```
lead.location → agent_zones.match(location) → rank_by_proximity → assign_top
```

| Rule | Priority | Description |
|------|----------|-------------|
| exact_zone | Highest | Agent covers the exact district/neighborhood |
| city_zone | High | Agent covers the city |
| region_zone | Medium | Agent covers the region (fallback) |

### 7.2 Skill-Based Routing

```
lead.type + lead.intent → agent_skills.match( type, intent ) → rank_by_match → assign_top
```

| Skill Domain | Lead Types |
|-------------|------------|
| residential | buyer, tenant |
| commercial | investor |
| land | land_buyer |
| diaspora | diaspora_investor |
| luxury | high_budget_buyer |

### 7.3 Availability-Based Routing

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Current lead load | 0.4 | Fewer active leads = higher priority |
| Response time (avg) | 0.3 | Faster response = higher priority |
| Last active | 0.2 | Recently active = higher priority |
| Rating | 0.1 | Higher rated = higher priority |

### Assignment Algorithm

```
score = (1 - load_factor) × 0.4 + response_time_score × 0.3 + recency_score × 0.2 + rating_score × 0.1
```

---

## 8. Priority Rules (P0–P3)

| Priority | Score Range | Lead Types | SLA | Action |
|----------|-------------|------------|-----|--------|
| **P0** | 100–95 | diaspora_investor, buyer > 50M FCFA | < 30 min | call_immediately, human agent |
| **P1** | 90–85 | seller, land_buyer, urgent buyer | < 2h | send_listings + call |
| **P2** | 75–60 | standard buyer, standard investor | < 24h | send_listings |
| **P3** | 40 | tenant, non-qualified prospect | J+1 to J+7 | follow_up automated |

### Priority Escalation

```
P3 → P2 : user re-engages + provides budget
P2 → P1 : user requests visit + has budget
P1 → P0 : user confirms cash purchase + diaspora detected
```

---

## 9. CRM Scoring V5 — 7 Factors (CRM-014)

| Factor | Weight | Computation | Source |
|--------|--------|-------------|--------|
| Lead type score | 0.20 | Base by type (tenant=40, buyer=60, seller=50, investor=80, diaspora=95), normalized 0-1 | lead_classifier_v1.json |
| Budget alignment | 0.20 | Explicit budget / market range; missing=0 | extracted entities |
| Location specificity | 0.15 | City+neighborhood: exact=1, city-only=0.6, vague=0.2 | GEO model |
| Urgency signal | 0.15 | Keywords detected (urgent, vite, asap)=1, implicit=0.5, none=0 | intent classifier |
| Completeness | 0.10 | Required fields filled / total fields | data quality engine |
| Engagement | 0.10 | Message length, response time, visit requests | behavior tracker |
| Diaspora flag | 0.10 | Foreign indicator + phone prefix + location abroad = 1, else 0 | diaspora detector |

```
V5 Score = Σ(factor_i × weight_i)  →  range [0, 1]
```

---

## 10. Data Quality Management

| Dimension | Metric | Threshold | Action |
|-----------|--------|-----------|--------|
| Completeness | % required fields filled | ≥ 80% A+, ≥ 60% A, ≥ 40% B | Grade assigned; C/D trigger enrichment |
| Reliability | Source score | agent=90, google_form=85, import=70, whatsapp=50, unknown=30 | Used in quality formula |
| Freshness | Last update timestamp | < 7 days (properties), < 30 days (profiles) | Stale flag → refresh request |
| Uniqueness | Duplicate score | ≥ 40 → candidate, ≥ 80 → auto-merge | Deduplication workflow |
| Validity | Format/conformity checks | 100% required | Validation gate blocks bad data |

**Quality Score Formula:**

```
Quality = Completeness × 0.6 + Reliability × 0.4
```

**Grades:**
| Grade | Score | Action |
|-------|-------|--------|
| A+ | ≥ 80 | Direct use |
| A | ≥ 60 | Minor verification |
| B | ≥ 40 | Needs completion |
| C | ≥ 20 | Enrichment required |
| D | < 20 | Re-qualification |

---

## 11. Behavior Tracking

| Behavior | Data Collected | Update Frequency | Used For |
|----------|---------------|------------------|----------|
| message_history | All messages, timestamps, entities | Real-time | Context enrichment, V5 scoring |
| response_time | Average response time per user | Per interaction | Engagement score, follow-up timing |
| budget_changes | Budget mentions over time | Per mention | Dynamic scoring, negotiation signal |
| visit_requests | Visit requests count, status (requested/scheduled/done/missed) | Per request | Closing propensity, scoring |
| property_views | Properties viewed, time spent | Per view | Affinity matching |
| document_requests | Documents requested, provided | Per request | Trust level, seriousness |
| call_attempts | Call attempts, duration, outcome | Per call | Agent performance, follow-up |
| referral_source | Source of acquisition | Once (initial) | ROI, channel optimization |

---

## 12. Action Recommendation

| Action | Trigger | Target Priority | SLA | Channel |
|--------|---------|-----------------|-----|---------|
| call_immediately | P0 lead, diaspora_investor, visit request with budget | P0 | < 1h | Phone + WhatsApp |
| send_listings | WARM lead, matching score ≥ 60, lead has budget+location | P1–P2 | < 24h | WhatsApp |
| request_budget | COLD lead, missing budget or location | P2–P3 | < 48h | WhatsApp |
| follow_up | LOW lead, inactive > 7d, stale lead | P3 | J+7, J+30, J+90 | WhatsApp |
| ignore | SPAM classification, duplicate + blocked, fraud detected | — | Immediate | None |

### Action Decision Tree

```
Lead scored → priority assigned → action selected:
  P0 → call_immediately
  P1 → send_listings (if qualified) OR call_immediately (if urgent)
  P2 → send_listings (if location+budget known) OR request_budget (if missing info)
  P3 → follow_up (if any engagement) OR ignore (if no signal)
```

---

## 13. Engine Integration

### 13.1 Conversation Engine

```
crm_engine → event_bus → [message.received] → conversation_engine → response
                ↑                                                     │
                └────────────────── feedback ─────────────────────────┘
```

- CRM provides user context + state to conversation
- Conversation returns intents + entities + feedback to CRM

### 13.2 Qualification Engine

```
crm_engine → lead.created → qualification_engine → enriched_profile → crm_scoring
```

- CRM triggers qualification when lead score is below threshold
- Qualification enriches missing fields → triggers re-scoring

### 13.3 Matching Engine

```
crm_engine → match.generated → matching_engine → ranked_properties → notification
                ↑                                      │
                └──── lead.profile + criteria ──────────┘
```

- CRM supplies lead criteria to matching
- Matching returns ranked properties; CRM handles notification

### 13.4 Relationship Engine

```
crm_engine → user.state_changed → relationship_engine → trust_update → permission_update
```

- CRM state transitions trigger relationship trust recalculation
- Relationship engine feeds back into CRM scoring (engagement factor)

---

## 14. Anti-Fraud Integration

| Layer | Detection | CRM Integration |
|-------|-----------|----------------|
| broker_spam | Repeated promotional messages | Blocks user 60 min, flags broker |
| duplicate_listing | Same property multiple accounts | Flag, merge, warn |
| fake_price | Price >50% below market | Flag, manual verification |
| suspicious_urgency | Artificial pressure for fast payment | Alert, enhanced verification |

**Fraud → CRM action:**
1. Fraud signal detected → `fraud.detected` event emitted
2. CRM event bus receives → applies penalty or block
3. Lead score adjusted (-50 for spam)
4. User state may transition (INACTIVE or blocked)

---

## 15. Agent Opt-In System (CRM-005)

| Step | Action | CRM Component |
|------|--------|---------------|
| 1 | Detect need (zone, property type match) | routing_engine |
| 2 | Request permission: "Voulez-vous recevoir le contact d'un agent?" | conversation_engine |
| 3 | Log consent in `agent_optins` table | optin_service |
| 4 | Conditional share: ONLY if accepted | routing_engine |
| 5 | Decline: no share, no agent follow-up | optin_service |

**Golden rule:** No agent contact shared without explicit user consent.

---

## 16. Agent Rating System (CRM-006)

| Element | Specification |
|---------|---------------|
| Scale | 1–5 stars |
| Calculation | Average of all received ratings |
| Storage | `agents` table, `rating` column |
| Display | "⭐ X/5" or "🆕" (new agent, no ratings) |
| Update | After each client feedback |
| Weight | Recent 10 ratings weighted 2× |

---

---

## 17. NBA Integration

The CRM Engine integrates with the NBA Engine to determine the next best action for each user based on state, score, and activity:

| User State | NBA | Trigger |
|------------|-----|---------|
| NEW_USER | `qualify.initial` | First interaction detected |
| SEARCHING_PROPERTY | `qualify.continue` | Incomplete qualification |
| LEAD_CREATED | `match.search` | Lead qualified |
| INACTIVE | `conversation.reengagement` | Inactivity > 90 days |
| BLOCKED | `security.review` | Fraud or spam flag |

Every CRM action generates an `audit_event` recording the rule, user, state, and outcome.

---

*Architecture patrimoniale Gold — Références: CRM-001 à CRM-015, CRM_MODEL.md, ROLE_MODEL.md*
