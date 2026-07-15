# ACCEPTANCE TEST MATRIX — Heritage Gold Rule Acceptance Criteria

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL

---

## 1. Criticality Classification

Every Heritage Gold rule is classified by business criticality, determining minimum test requirements:

| Criticality | Definition | Minimum Test Coverage | Total Tests Per Rule |
|-------------|------------|----------------------|---------------------|
| **HIGH** | Rule failure causes direct business impact (incorrect matching, wrong lead classification, data loss, compliance violation) | Nominal (2) + Negative (1) + Idempotence (1) + Audit (1) | 5 |
| **MEDIUM** | Rule failure causes degraded experience but no data loss or compliance issue | Nominal (1) + Negative (1) | 2 |
| **LOW** | Rule failure causes cosmetic or minor functional issue | Nominal (1) | 1 |

---

## 2. Complete Acceptance Test Matrix

### 2.1 Constitution Domain

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| CONST-001 | Zero commission on transactions | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONST-002 | Revenue via services | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONST-003 | RGPD data protection | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONST-004 | WhatsApp as primary channel | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONST-005 | Multi-channel strategy | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONST-006 | Matching as core engine | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONST-007 | Qualification as foundation | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONST-008 | Agents and clients at center | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONST-009 | Offline-first architecture | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| CONST-010 | DeepSeek as primary AI | HIGH | 2 tests | 1 test | 1 test | 1 test | — |

### 2.2 Property Domain

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| PROP-001 | 7 property families | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| PROP-002 | 5 mandatory listing fields | MEDIUM | 1 test | 1 test | — | — | — |
| PROP-003 | 5-state lifecycle | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| PROP-004 | Valid state transitions | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| PROP-005 | Auto-archive after 90 days | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| PROP-006 | DQ Score formula | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| PROP-007 | Completeness weights | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| PROP-008 | Source reliability | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| PROP-009 | Quality grades A+ to D | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| PROP-010 | Price scoring | MEDIUM | 1 test | 1 test | — | — | — |
| PROP-011 | Price formats (k, mille) | MEDIUM | 1 test | 1 test | — | — | — |

### 2.3 Matching Domain

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| MATCH-001 | V1 scoring dimensions | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-002 | DE scoring dimensions | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-003 | Budget tolerances | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-004 | Boost: exact_neighborhood_match | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-005 | Boost: exact_city_match | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-006 | Boost: budget_within_range | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-007 | Boost: title_foncier | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-008 | Boost: diaspora_investor | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-009 | Minimum match score 60 | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-010 | Max results V1=10, DE=5 | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-011 | Score <60% never proposed | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-012 | 4 compatibility levels | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-013 | Non-compensation principle | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-014 | Refusal learning (3 refusals→priority) | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| MATCH-015 | Rematching never starts from zero | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| MATCH-016 | Rematching only concerned dossiers | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| MATCH-017 | Refused property never reproposed | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-018 | Reproposition exceptions | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-019 | Star rating (5-level) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-020 | V5 scoring weights | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-021 | V4 filter (status, city, budget) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-022 | Exclusions (archived, tolerance, city, sent) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-023 | Exclusions (operation, type, availability) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-024 | Transaction Success Score (8 indicators) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-025 | Availability score (100/70/30/0) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-026 | Document score (100/80/60/40) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-027 | Holder score formula | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-028 | Budget flexibility rule | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-029 | Reasoning priority order | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-030 | 7-step reasoning pipeline | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| MATCH-031 | Reasoning confidence threshold 0.70 | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-032 | Diversity rule (avoid identical) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-033 | Explainability (top 3 criteria) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| MATCH-034 | Absolute rules (never incompatible/sold/twice) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |

### 2.4 Geography Domain

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| GEO-001 | Territorial hierarchy 8 levels | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| GEO-002 | 10 priority cities | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| GEO-003 | Neighborhood inventory for 11+ cities | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| GEO-004 | Levenshtein normalization threshold=3 | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| GEO-005 | Location extraction patterns | MEDIUM | 1 test | 1 test | — | — | — |
| GEO-006 | Extraction confidence formula | MEDIUM | 1 test | 1 test | — | — | — |
| GEO-007 | GPS data for neighborhoods | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| GEO-008 | City affinity workflow (5 steps) | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| GEO-009 | Geographic prohibitions | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| GEO-010 | Real distance (GPS-based) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| GEO-011 | Geo score: city+neighborhood+GPS+distance+time | HIGH | 2 tests | 1 test | 1 test | 1 test | — |

### 2.5 Qualification Domain

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| QUAL-001 | Base scores per intent | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-002 | Boosters (budget, city, neighborhood, urgent, diaspora, cash) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-003 | Penalties (missing_budget, unclear_location, spam) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-004 | V1 thresholds (HOT/WARM/COLD/LOW) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-005 | V5 thresholds (HOT/WARM/COLD/SPAM) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-006 | V5 pipeline 8 steps | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| QUAL-007 | 10-step qualification flow | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| QUAL-008 | Intent→role mapping | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-009 | Actions per class (5 actions) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-010 | 25 USER_FIELDS extraction | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-011 | 10 LEAD_FIELDS | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-012 | 4 tracked behaviors | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-013 | Channel message limits (WA 1, TG 2-3) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-014 | No re-ask, no restart, correction overwrites | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-015 | Stop criteria (5 conditions) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-016 | Diaspora indicators (13 locations + 4 prefixes) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-017 | Lead scoring weights (7 factors) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-018 | Priority levels (P0/P1/P2/P3) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| QUAL-019 | Additional types (seeker, agent, owner, broker) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |

### 2.6 Conversation Domain

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| CONV-001 | Intermediary positioning | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-002 | Professional tone, vouvoiement | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-003 | 3 languages supported | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-004 | Legal question→notary | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| CONV-005 | DeepSeek entity extraction | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-006 | Match→notify agent/owner | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-007 | Paid accompaniment 50k | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-008 | SIGNALER command | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-009 | RGPD deletion (7 days) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-010 | Familiarity levels J1-J4 | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-011 | Summary format | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-012 | New property simulation (random 1-5) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-013 | Long-term retention 365 days | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-014 | Lead >12mo recontactable | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-015 | Previous satisfaction check | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-016 | Follow-up schedule (J1/J7/J30/J90) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-017 | Response hierarchy (DeepSeek→Rules→Templates) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-018 | DeepSeek JSON format | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-019 | 7 multilingual templates (FR/EN/PID) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-020 | Property display format | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-021 | Feedback scoring (👍=5, 👎=1) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CONV-022 | 10 buyer fears, 8 seller fears | MEDIUM | 1 test | 1 test | — | — | — |
| CONV-023 | Intent signals (3/7 implemented) | MEDIUM | 1 test | 1 test | — | — | — |

### 2.7 Negotiation Domain

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| NEGO-001 | 4 buyer profiles | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| NEGO-002 | 3 seller profiles | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| NEGO-003 | 12 buyer fears | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| NEGO-004 | 8 seller fears | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| NEGO-005 | 6 LAWIM arguments | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| NEGO-006 | 5 property arguments | LOW | 1 test | — | — | — | — |
| NEGO-007 | 4 key moments | LOW | 1 test | — | — | — | — |
| NEGO-008 | Price negotiation expressions | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| NEGO-009 | 5 tone principles | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| NEGO-010 | 5-step trust sequence | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| NEGO-011 | Follow-up calendar (J1/J7/J30/J90) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| NEGO-012 | Urgency signals | MEDIUM | 1 test | 1 test | — | — | — |
| NEGO-013 | Investor signals | MEDIUM | 1 test | 1 test | — | — | — |
| NEGO-014 | Diaspora signals | MEDIUM | 1 test | 1 test | — | — | — |

### 2.8 CRM Domain

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| CRM-001 | 7 role levels 1-7 | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| CRM-002 | 7x7 permission matrix | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-003 | 7 user states | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| CRM-004 | 11 event types | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-005 | Agent Opt-In 4 steps | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| CRM-006 | Agent Rating 1-5 | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-007 | Lead price 500 FCFA | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-008 | Identity resolution (phone/email/name) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-009 | Master Dashboard password | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-010 | 20 CRM tables | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-011 | Diaspora services table | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-012 | 6 external partners | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-013 | 18 actors | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-014 | CRM scoring V5 (7 factors) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| CRM-015 | Role hierarchy (Master→Demandeur) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |

### 2.9 Language Domain

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| LANG-001 | Default French | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-002 | Detection hierarchy | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-003 | LANGUE command with persistence | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-004 | 7 multilingual templates (FR/EN/PID) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-005 | 33 entity linking entries | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-006 | 5 typo databases | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-007 | 7 WhatsApp language files | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-008 | 5 i18n documents | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-009 | 38 country phone codes | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-010 | Cameroon format 237+9 digits | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-011 | WhatsApp link format | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| LANG-012 | Pidgin detection (12-14 words) | MEDIUM | 1 test | 1 test | — | — | — |
| LANG-013 | French keywords (18 max) | LOW | 1 test | — | — | — | — |
| LANG-014 | English keywords (18 max) | LOW | 1 test | — | — | — | — |

### 2.10 Security Domain

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| SEC-001 | Anti-spam max 10 msg/min | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| SEC-002 | Auto-block 60 minutes | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| SEC-003 | blocked_users table | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| SEC-004 | Anti-fraud 4 layers | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| SEC-005 | RGPD anonymisation 7 days | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| SEC-006 | Implicit trust levels | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| SEC-007 | 25 fraud signals | HIGH | 2 tests | 1 test | 1 test | 1 test | — |

---

### 2.11 H0.5 Qualification Matrix Domain (NEW)

| Rule ID | Description | Criticality | Nominal | Negative | Idempotence | Audit | State Transition |
|---------|-------------|-------------|---------|----------|-------------|-------|------------------|
| H05-ATM-001 | Matrix selection by intent + property_type + transaction_type | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| H05-ATM-002 | Readiness calculation matching H0.5 7 levels | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| H05-ATM-003 | Next question selection matching question_priority | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| H05-ATM-004 | Forbidden question enforcement | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| H05-ATM-005 | Sensitive field protection (privacy gating) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |
| H05-ATM-006 | Search readiness gating (cardinal rule) | HIGH | 2 tests | 1 test | 1 test | 1 test | 1 test |
| H05-ATM-007 | Matching semantics application (9 roles) | HIGH | 2 tests | 1 test | 1 test | 1 test | — |

---

## 3. Summary Statistics

| Domain | Total Rules | HIGH | MEDIUM | LOW | Total Nominal | Total Negative | Total Idempotence | Total Audit | State Transition | Grand Total |
|--------|------------:|-----:|-------:|----:|--------------:|---------------:|------------------:|------------:|-----------------:|------------:|
| Constitution | 10 | 10 | 0 | 0 | 20 | 10 | 10 | 10 | 1 | 51 |
| Property | 11 | 9 | 2 | 0 | 20 | 11 | 9 | 9 | 3 | 52 |
| Matching | 34 | 34 | 0 | 0 | 68 | 34 | 34 | 34 | 4 | 174 |
| Geography | 11 | 9 | 2 | 0 | 20 | 11 | 9 | 9 | 1 | 50 |
| Qualification | 19 | 19 | 0 | 0 | 38 | 19 | 19 | 19 | 2 | 97 |
| Conversation | 23 | 21 | 2 | 0 | 44 | 23 | 21 | 21 | 1 | 110 |
| Negotiation | 14 | 10 | 2 | 2 | 24 | 12 | 10 | 10 | 1 | 57 |
| CRM | 15 | 15 | 0 | 0 | 30 | 15 | 15 | 15 | 3 | 78 |
| Language | 14 | 11 | 1 | 2 | 25 | 12 | 11 | 11 | 0 | 59 |
| Security | 7 | 7 | 0 | 0 | 14 | 7 | 7 | 7 | 3 | 38 |
| H0.5 Matrices | 7 | 7 | 0 | 0 | 14 | 7 | 7 | 7 | 3 | 38 |
| **TOTAL** | **165** | **152** | **9** | **4** | **317** | **161** | **152** | **152** | **22** | **804** |

---

## 4. Acceptance Criteria Per Domain

### 4.1 Constitution

| Criterion | Verification |
|-----------|-------------|
| Zero commission enforced on all property transactions | CONST-001 nominal tests pass; no commission calculated |
| Revenue model uses service fees only | CONST-002 audit trail shows service revenue |
| GDPR compliance applies to all data processing | CONST-003 triggers on personal data events |
| WhatsApp message format < 1024 chars | CONST-004 channel format validation |
| Multi-channel routing respects channel constraints | CONST-005 tests pass for WA, TG, Dashboard |
| Matching is invoked for every qualified lead | CONST-006 integration test passes |
| Qualification runs on every new message | CONST-007 pipeline test passes |
| Agent/client role respected in all operations | CONST-008 permission tests pass |
| Offline queue buffers messages during disconnection | CONST-009 state transition test passes |
| DeepSeek API used for AI operations | CONST-010 mock integration test passes |

### 4.2 Property

| Criterion | Verification |
|-----------|-------------|
| Property belongs to exactly one of 7 families | PROP-001 classification tests cover all families |
| Listing requires type, transaction, price, city, description | PROP-002 validation tests for missing fields |
| Lifecycle follows 5 states with valid transitions only | PROP-003/004 state machine tests cover all transitions |
| Property auto-archives after 90 days inactivity | PROP-005 boundary test at day 89/90/91 |
| Data Quality Score calculated correctly | PROP-006 formula tests verify completeness*0.6 + reliability*0.4 |
| Completeness weights sum to 100% | PROP-007 weight distribution test |
| Source reliability values correct | PROP-008 all 6 source values verified |
| Grade assignment matches score ranges | PROP-009 boundary tests at A+/A/B/C/D thresholds |
| Price scoring applied correctly | PROP-010 calculation tests |
| Price formats parsed correctly | PROP-011 k/mille format parsing tests |

### 4.3 Matching

| Criterion | Verification |
|-----------|-------------|
| Scoring dimensions respect defined weights | MATCH-001/002 weight distribution tests |
| Budget tolerances applied per transaction type | MATCH-003 rent±20%/buy±15%/invest±25% verified |
| Boost values correct for all conditions | MATCH-004-008 boost addition tests |
| Minimum score 60 enforced | MATCH-009 boundary at 59/60/61 |
| Max results limit respected | MATCH-010 result count tests (V1=10, DE=5) |
| Score <60 never proposed | MATCH-011 hard block test |
| 4 compatibility levels assigned correctly | MATCH-012 classification tests |
| Non-compensation prevents type mismatch | MATCH-013 cross-type rejection test |
| 3 refusals trigger priority adjustment | MATCH-014 learning state transition test |
| Rematching preserves existing context | MATCH-015 context preservation test |
| Rematching only re-evaluates affected dossiers | MATCH-016 scope limitation test |
| Refused property blacklisted permanently | MATCH-017 blacklist persistence test |
| Exceptions allow reproposal only under specific conditions | MATCH-018 exception trigger tests |
| Star rating maps scores correctly | MATCH-019 5-level mapping test |
| V5 scoring formula matches specification | MATCH-020 formula comparison test |
| V4 filter applied correctly | MATCH-021 filter condition test |
| All exclusions enforced | MATCH-022/023 combination test |
| Transaction Success Score calculated from 8 indicators | MATCH-024 multi-indicator test |
| Availability score tiers correct | MATCH-025 100/70/30/0 breakdown test |
| Document score tiers correct | MATCH-026 100/80/60/40 breakdown test |
| Holder score computed from 4 metrics | MATCH-027 formula verification |
| Budget flexibility allows slight over-budget for excellent candidates | MATCH-028 conditional override test |
| Reasoning priority order respected | MATCH-029 priority chain test |
| 7-step reasoning pipeline produces correct output | MATCH-030 pipeline integration test |
| Confidence <0.70 triggers escalation | MATCH-031 threshold boundary test |
| Duplicate properties deduplicated | MATCH-032 near-identical removal test |
| Top 3 criteria explained in natural language | MATCH-033 explanation content test |
| Absolute rules never violated | MATCH-034 invariant check (hard constraints) |

### 4.4 Geography

| Criterion | Verification |
|-----------|-------------|
| Location resolves through correct hierarchy level | GEO-001 hierarchy depth test |
| 10 priority cities ranked and recognized | GEO-002 priority ordering test |
| All 382 neighborhoods matchable | GEO-003 inventory lookup test |
| Typo tolerance max edit distance 3 | GEO-004 Levenshtein boundary test |
| Location extraction patterns match real messages | GEO-005 pattern corpus test |
| Confidence score formula produces correct values | GEO-006 formula test |
| GPS lookup returns coordinates for covered districts | GEO-007 GPS coverage test |
| City affinity workflow progresses through 5 steps | GEO-008 step-by-step progression test |
| Geographic prohibitions prevent invalid cross-city matching | GEO-009 prohibition pair test |
| Distance calculation uses real road distance | GEO-010 GPS distance test |
| Geo score combines all 5 factors correctly | GEO-011 multi-factor test |

### 4.5 Qualification

| Criterion | Verification |
|-----------|-------------|
| Base score assigned correctly per intent | QUAL-001 all 5 intent values verified |
| Boosters applied cumulatively | QUAL-002 booster combination test |
| Penalties applied and floor enforced | QUAL-003 penalty floor test (min score) |
| V1 thresholds map scores to HOT/WARM/COLD/LOW | QUAL-004 boundary test at 79/80, 59/60, 39/40 |
| V5 thresholds map scores to HOT/WARM/COLD/SPAM | QUAL-005 boundary test at 0.79/0.80, 0.49/0.50, 0.29/0.30 |
| Pipeline executes all 8 steps in order | QUAL-006 step sequence test |
| Qualification asks 10 questions in strict order | QUAL-007 question order test |
| Intent correctly maps to role | QUAL-008 mapping table test |
| Action selected matches lead classification | QUAL-009 all 5 action-class pairs verified |
| 25 USER_FIELDS extracted correctly | QUAL-010 field extraction completeness test |
| 10 LEAD_FIELDS populated correctly | QUAL-011 field population test |
| All 4 behaviors tracked | QUAL-012 behavior detection test |
| Message limits per channel satisfied | QUAL-013 WA=1, TG=2-3 enforcement test |
| No re-ask, no restart, correction overwrites | QUAL-014 conversation flow test |
| Stop criteria halt qualification when conditions met | QUAL-015 all 5 stop conditions verified |
| Diaspora detection uses 13 locations + 4 prefixes | QUAL-016 indicator completeness test |
| Lead scoring weights sum to 100 | QUAL-017 weight sum test |
| Priority levels assigned per score ranges | QUAL-018 boundary test P0/P1/P2/P3 |
| Additional types recognized correctly | QUAL-019 all 4 types verified |

### 4.6 Conversation

| Criterion | Verification |
|-----------|-------------|
| Response positions LAWIM as intermediary | CONV-001 content template test |
| Tone uses vouvoiement and professional language | CONV-002 language analysis test |
| Response in FR/EN/PID only | CONV-003 language filter test |
| Legal questions escalate to notary | CONV-004 escalation trigger test |
| Type/location/budget extracted by DeepSeek | CONV-005 extraction integration test |
| Agent/owner notified on match | CONV-006 notification trigger test |
| 50k accompaniment offered on request | CONV-007 service offer test |
| SIGNALER creates incident record | CONV-008 incident creation test |
| RGPD deletion scheduled within 7 days | CONV-009 deletion scheduling test |
| Familiarity level assigned correctly | CONV-010 J1/J2/J3/J4 time-based test |
| Summary uses correct template format | CONV-011 template rendering test |
| New property count is random 1-5 | CONV-012 distribution test (100 iterations) |
| Conversation retained for 365 days | CONV-013 expiration boundary test |
| Lead >12mo flagged for recontact | CONV-014 age check test |
| Previous satisfaction checked on re-engagement | CONV-015 satisfaction lookup test |
| Follow-up scheduled at 4 intervals | CONV-016 interval precision test |
| Response uses correct hierarchy | CONV-017 priority routing test |
| DeepSeek response follows JSON schema | CONV-018 schema validation test |
| Templates render in correct language | CONV-019 language-template mapping test |
| Property displayed in correct format | CONV-020 format template test |
| Feedback score computed correctly | CONV-021 👍/👎 score test |
| Buyer/seller fears addressable | CONV-022 objection matching test |
| Intent signals detected correctly | CONV-023 signal matching test |

### 4.7 Negotiation

| Criterion | Verification |
|-----------|-------------|
| Buyer profile assigned correctly | NEGO-001 4-profile classification test |
| Seller profile assigned correctly | NEGO-002 3-profile classification test |
| Buyer fears mapped to responses | NEGO-003 fear-response mapping test |
| Seller fears mapped to responses | NEGO-004 fear-response mapping test |
| LAWIM arguments presented on relevant objections | NEGO-005 argument-objection mapping test |
| Property arguments available (non-validated) | NEGO-006 content inventory test |
| Key moments identified (non-validated) | NEGO-007 timing detection test |
| Price expressions parsed correctly | NEGO-008 expression parsing test |
| Tone follows 5 principles | NEGO-009 tone compliance test |
| Trust sequence progresses through 5 steps | NEGO-010 step progression test |
| Follow-up respects calendar schedule | NEGO-011 interval test |
| Urgency signals detected | NEGO-012 keyword matching test |
| Investor signals detected | NEGO-013 keyword matching test |
| Diaspora signals detected | NEGO-014 keyword matching test |

### 4.8 CRM

| Criterion | Verification |
|-----------|-------------|
| Role assigned at correct level | CRM-001 all 7 levels verified |
| Permission check prevents unauthorized actions | CRM-002 7x7 matrix tested, 49 cells verified |
| User state transitions follow state machine | CRM-003 all 7 states, valid transitions tested |
| Events logged with correct type | CRM-004 all 11 event types verified |
| Agent Opt-In complete 4-step workflow | CRM-005 step-by-step progression test |
| Agent rating averaged correctly | CRM-006 aggregation test |
| Lead priced at default 500 FCFA | CRM-007 pricing test |
| Identity resolution scores correct | CRM-008 phone=100, email=95, name+phone≥40 verified |
| Master Dashboard authentication works | CRM-009 auth credentials test |
| CRM tables exist with correct schema | CRM-010 schema validation test |
| Diaspora services stored correctly | CRM-011 data model test |
| 6 partner types registered | CRM-012 partner completeness test |
| All 18 actors in registry | CRM-013 actor completeness test |
| CRM scoring V5 uses 7 weighted factors | CRM-014 factor weight test |
| Role hierarchy enforced | CRM-015 permission delegation test |

### 4.9 Language

| Criterion | Verification |
|-----------|-------------|
| Default language is French | LANG-001 initial state test |
| Language detection follows hierarchy | LANG-002 fallback chain test |
| LANGUE command persists preference | LANG-003 persistence test |
| Templates render in user's language | LANG-004 language-template mapping test |
| Entity linking resolves synonyms/typos | LANG-005 all 5 relation types tested |
| Typo correction uses correct database | LANG-006 database routing test |
| WhatsApp expressions matched to intents | LANG-007 intent matching test |
| i18n documentation referenced | LANG-008 doc existence test |
| 38 country phone codes recognized | LANG-009 code completeness test |
| Cameroon phone validated as 237+9 digits | LANG-010 format validation test |
| WhatsApp link generated correctly | LANG-011 URL format test |
| Pidgin words detected | LANG-012 keyword detection test |
| French keyword count ≤18 | LANG-013 count test |
| English keyword count ≤18 | LANG-014 count test |

### 4.10 Security

| Criterion | Verification |
|-----------|-------------|
| Rate limit blocks at 11th msg/min | SEC-001 boundary test |
| Auto-block activates for 60 minutes | SEC-002 block duration test |
| Spammers tracked in blocked_users | SEC-003 persistence test |
| Fraud detected through 4 layers | SEC-004 all 4 layer tests |
| Data anonymization within 7 day deadline | SEC-005 deadline enforcement test |
| Trust levels assigned correctly | SEC-006 level assignment test |
| All 25 fraud signals detected | SEC-007 signal completeness test |

### 4.11 H0.5 Qualification Matrices

| Criterion | Verification |
|-----------|-------------|
| Matrix selected matches user intent + property_type + transaction_type | H05-ATM-001: Verify that for RESIDENTIAL_SEARCH + studio + RENT, matrix MATRIX-RES-SEARCH-003 is selected |
| Readiness progression follows 7-level model with correct transitions | H05-ATM-002: Verify each of the 7 levels transitions correctly with the right field conditions |
| Next question selected by priority within current readiness level | H05-ATM-003: Verify question priority formula: `priority = base - (impact×10) + (sensitivity×5) - (ambiguity×3)` |
| Forbidden questions suppressed per matrix and cross-matrix | H05-ATM-004: Verify nombre_de_pieces not asked for any matrix; chambres not asked for studio |
| Sensitive fields protected by consent gate | H05-ATM-005: Verify PRIVATE fields require consent before sharing; SENSITIVE/CONFIDENTIAL require explicit opt-in |
| Search launched immediately at MINIMUM_SEARCH_READY | H05-ATM-006: Verify that once city+neighborhood+budget+property_type+transaction collected, search launches without further questions |
| Matching semantics applied correctly for all 9 roles | H05-ATM-007: Verify hard_constraint excludes, soft_constraint scores, boost adds, penalty subtracts, transaction_blocker gates |

---

## 5. Traceability to Heritage Gold Documents

| Domain | Heritage Gold Source | Knowledge Inventory Reference |
|--------|---------------------|------------------------------|
| Constitution | `Directive/00-CONSTITUTION.md` | `RULE_INDEX.md §Constitution` |
| Property | `Directive/02-PROPERTY-REFERENCE.md`, `property_lifecycle_engine.py`, `data_quality_engine.py` | `RULE_INDEX.md §Property`, `PROPERTY_MODEL.md` |
| Matching | `Directive/04-DECISION-ENGINE-REFERENCE.md`, `property_matching_v1.json`, `property_matcher_v5.py` | `RULE_INDEX.md §Matching`, `MATCHING_MODEL.md` |
| Geography | `district_hierarchy.json`, `neighborhoods/*.json`, `city-affinity-matrix.md` | `RULE_INDEX.md §Geography`, `GEOGRAPHY_MODEL.md` |
| Qualification | `lead_classifier_v1.json`, `RULE_ENGINE_V5.json`, `knowledge_builder.py` | `RULE_INDEX.md §Qualification`, `QUALIFICATION_MODEL.md` |
| Conversation | `RESPONSE_POLICY.md`, `conversation_memory.py`, `follow_up_system.py` | `RULE_INDEX.md §Conversation`, `CONVERSATION_MODEL.md` |
| Negotiation | `Directive/48-LAWIM-SALES-PLAYBOOK.md`, `trust-and-objection-patterns.md` | `RULE_INDEX.md §Negotiation`, `NEGOTIATION_MODEL.md` |
| CRM | `implement_all.sql`, `user_roles.json`, `USER_STATES.json`, `identity_resolution.py` | `RULE_INDEX.md §CRM`, `CRM_MODEL.md` |
| Language | `language_handler.py`, `language_detector_ia.py`, `multilingual_responses.py`, `entity_linking.json` | `RULE_INDEX.md §Language`, `LANGUAGE_MODEL.md` |
| Security | `anti_spam.py`, `Directive/15-SECURITY-REFERENCE.md`, `fraud-signals-and-verification.md` | `RULE_INDEX.md §Security` |
| H0.5 Matrices | `docs/lawim_heritage_gold/qualification_matrices/` (29 files) | `reports/knowledge_execution/H0.5_INVENTORY_REPORT.md` |

---

## 6. Contract Validation Rules

1. Every rule in `RULE_INDEX.md` MUST have an entry in this matrix.
2. Every rule MUST satisfy its criticality-based test requirements (Section 1).
3. Each test required in this matrix MUST correspond to a test contract in `RULE_TEST_CONTRACT.md`.
4. Tests MUST be implemented and passing before a rule is considered "accepted."
5. A rule's criticality MAY be elevated (HIGHER) but MUST NOT be reduced without architecture review.
6. Rules marked `NON_VALIDE` in Heritage Gold SHOULD be tested at LOW to track regression when validated.
7. Rules marked `PARTIAL` in Heritage Gold MUST be tested at MEDIUM minimum.
