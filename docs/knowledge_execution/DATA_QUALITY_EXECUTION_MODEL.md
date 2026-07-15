# Data Quality Execution Model — LAWIM Heritage Gold

**Source:** CRM_MODEL.md §9, RULE_INDEX.md (PROP-006 to PROP-009)
**Mission:** H0 — LAWIM Heritage Gold
**Date:** 15 juillet 2026

---

## 1. Required Fields per Entity

### 1.1 Person

| Field | Required | Validation | Completeness Weight |
|-------|----------|------------|-------------------|
| `name` | YES | Non-empty, max 100 chars | 15% |
| `phone` | YES | Valid Cameroonian format (+237 6XXXXXXXX) | 20% |
| `email` | NO | Email format if provided | 5% |
| `city` | YES | Must exist in geo index | 15% |
| `neighborhood` | NO | Must exist in geo index | 5% |
| `role` | YES | Must be valid role from role registry | 10% |
| `source` | YES | Must be known source type | 10% |
| `intent_type` | NO | buy/rent/sell/invest | 10% |
| `budget_min` | NO | Positive integer | 5% |
| `budget_max` | NO | Positive integer, ≥ budget_min | 5% |

**Minimum viable person:** name + phone + city (50% completeness)

### 1.2 Property

| Field | Required | Validation | Completeness Weight |
|-------|----------|------------|-------------------|
| `title` | YES | Non-empty, max 200 chars | 10% |
| `description` | YES | Min 20 chars | 15% |
| `price` | YES | Positive integer | 15% |
| `city` | YES | Must exist in geo index | 10% |
| `neighborhood` | NO | Must exist in geo index if provided | 5% |
| `property_type` | YES | Must be valid type (maison, terrain, appartement, villa, local, immeuble, entrepôt) | 15% |
| `transaction_type` | YES | rent / sell | 5% |
| `images` | NO | Max 3 pts per image (up to 15%) | 15% (max) |
| `owner_phone` | YES | Valid phone | 5% |
| `status` | YES | available / pending / rented / sold / archived | 5% |

**Minimum viable property:** title + price + city + property_type + transaction_type (65% without images)

### 1.3 Lead

| Field | Required | Validation | Completeness Weight |
|-------|----------|------------|-------------------|
| `person_id` | YES | FK to persons | 15% |
| `intent` | YES | buy / rent / sell / invest | 15% |
| `score` | YES | Float 0–1 | 10% |
| `priority` | YES | P0 / P1 / P2 / P3 | 10% |
| `class` | YES | HOT / WARM / COLD / LOW / SPAM | 10% |
| `status` | YES | raw / qualified / scored / classified / assigned / contacted / engaged / converted / lost / recycled | 10% |
| `budget` | NO | Positive integer | 10% |
| `location_city` | NO | Must exist in geo index | 10% |
| `location_neighborhood` | NO | Must exist in geo index if provided | 5% |
| `property_type` | NO | Valid property type | 5% |

**Minimum viable lead:** person_id + intent + score + priority + class + status (70%)

### 1.4 Agent

| Field | Required | Validation | Completeness Weight |
|-------|----------|------------|-------------------|
| `person_id` | YES | FK to persons | 20% |
| `agency_id` | YES | FK to agencies | 15% |
| `phone` | YES | Valid phone | 15% |
| `zones` | YES | Array of valid zone IDs | 15% |
| `skills` | YES | Array of valid skill types | 10% |
| `rating` | NO | Float 1–5 | 5% |
| `subscription_tier` | YES | free / pro / business | 10% |
| `status` | YES | active / inactive / suspended | 10% |

### 1.5 Agency

| Field | Required | Validation | Completeness Weight |
|-------|----------|------------|-------------------|
| `name` | YES | Non-empty, max 100 chars | 20% |
| `responsible_name` | YES | Non-empty | 15% |
| `phone` | YES | Valid phone | 15% |
| `address` | YES | Non-empty | 10% |
| `city` | YES | Must exist in geo index | 15% |
| `cni` | YES | Valid CNI number | 10% |
| `rccm` | YES | Valid RCCM number | 10% |
| `tax_id` | YES | Valid tax ID | 5% |

### 1.6 Partner

| Field | Required | Validation | Completeness Weight |
|-------|----------|------------|-------------------|
| `partner_type` | YES | notaire / géomètre / banque / assurance / artisan / expert | 20% |
| `name` | YES | Non-empty | 20% |
| `phone` | YES | Valid phone | 20% |
| `email` | NO | Email format | 10% |
| `city` | YES | Must exist in geo index | 15% |
| `status` | YES | active / inactive | 15% |

---

## 2. Validation Rules

### 2.1 Format Validations

| Field | Rule | Error Message |
|-------|------|---------------|
| phone | Must match `^\+237[2-9]\d{8}$` after normalization | "Format téléphone invalide — utilisez +237 6XXXXXXXX" |
| email | Must match RFC 5322 basic pattern | "Format email invalide" |
| price | Must be positive integer, commas removed | "Le prix doit être un nombre positif" |
| budget | budget_max ≥ budget_min if both present | "Le budget max doit être supérieur au budget min" |
| name | 2–100 chars, no special chars except -' | "Le nom doit contenir entre 2 et 100 caractères" |
| city | Must be in geo index (10 priority cities) | "Ville non couverte — villes disponibles: Douala, Yaoundé, ..." |
| property_type | Enum: maison, terrain, appartement, villa, local, immeuble, entrepôt | "Type de bien invalide" |
| transaction_type | Enum: rent, sell | "Type de transaction invalide" |

### 2.2 Business Validations

| Rule | Condition | Action |
|------|-----------|--------|
| Property status integrity | If status=rented, must have a valid lease reference | Flag for review |
| Agent zone coverage | Agent.zones must be subset of agency's coverage | Flag for review |
| Lead-agent consistency | Agent assigned to lead must cover lead's city zone | Re-route |
| Diaspora service | diaspora_service requires non-CM phone or foreign IP | Validate |
| Duplicate phone | No two persons with same normalized phone | Identity resolution triggered |
| Boost expiry | boost.expires_at > NOW() | Invalid if expired |
| Subscription status | subscription.expires_at < NOW() → status=expired | Auto-update on check |

### 2.3 Constraint Validations

| Constraint | Scope | Enforcement |
|------------|-------|-------------|
| Unique phone | persons | DB unique index on normalized_phone |
| Unique WhatsApp ID | persons | DB unique index on wa_id |
| Unique email (non-null) | persons | Partial unique index WHERE email IS NOT NULL |
| FK person_id | leads, agents, contact_channels | CASCADE on delete |
| FK agency_id | agents, properties | RESTRICT on delete |
| FK property_id | leads_matches, boost_purchases | CASCADE on delete |

---

## 3. Completeness Scoring

### 3.1 Per-Entity Formula

```
Completeness = Σ(field_i × weight_i) for all required + optional fields
```

Where weight_i is the completeness weight percentage for that field (sum = 100% for required fields; optional fields add to a total up to 130%).

### 3.2 Normalized Score

```
normalized_score = min(100, completeness_raw)
```

### 3.3 Entity-Level Grades

| Entity | A+ (≥ 80) | A (≥ 60) | B (≥ 40) | C (≥ 20) | D (< 20) |
|--------|-----------|----------|----------|----------|----------|
| Person | All required + 2+ optional | All required | 3/4 required | 2/4 required | < 2 required |
| Property | All required + 2+ optional | All required | 4/5 required | 3/5 required | < 3 required |
| Lead | All required + 2+ optional | All required | 4/6 required | 3/6 required | < 3 required |
| Agent | All required | 5/6 required | 4/6 required | 3/6 required | < 3 required |
| Agency | All required | 6/8 required | 5/8 required | 4/8 required | < 4 required |

---

## 4. Data Freshness Requirements

| Entity | Freshness SLA | Stale After | Action on Stale |
|--------|---------------|-------------|-----------------|
| Property | < 7 days | > 30 days without update | Flag "stale", send refresh request to owner |
| Person profile | < 30 days | > 90 days without interaction | Downgrade to INACTIVE state |
| Lead | < 7 days | > 30 days without contact | Re-classify as COLD, reduce priority |
| Agent availability | < 24h | > 7 days without login | Mark "away", stop routing |
| Agency info | < 90 days | > 180 days | Flag for verification |
| Partner info | < 180 days | > 365 days | Flag for re-validation |
| Property images | < 30 days | > 90 days | Flag for re-upload |
| Price | < 7 days | > 30 days without price check | Flag "price not confirmed" |

### Freshness Score

```
freshness_score = max(0, 1 - (days_since_update / freshness_sla_days))
```

Used as a multiplier on data quality: `Quality Effective = Quality × min(1, freshness_score + 0.5)`

---

## 5. Duplicate Detection Thresholds

| Criterion | Score | Auto-Merge | Flag for Review | Low Confidence |
|-----------|-------|------------|-----------------|----------------|
| Same phone | 100 | ✅ ≥ 80 | — | — |
| Same email | 95 | ✅ ≥ 80 | — | — |
| Same WhatsApp ID | 100 | ✅ ≥ 80 | — | — |
| Similar name + same phone | 40–99 | ≥ 80 | 40–79 | — |
| Similar name + same email | 30–94 | ≥ 80 | 40–79 | 30–39 |
| Similar name + same city | 60–99 | ≥ 80 | 40–79 | — |
| Same phone + different name | 100 | ✅ | Flag if name differs > 10 chars | — |

**Detection frequency:**
- Real-time: on person create, person update, lead create
- Batch: daily at 02:00 full cross-scan
- On-demand: via admin API

**Cross-entity deduplication:**
- Person duplicates → merge → one canonical person
- Property duplicates (same address, same owner, same price) → merge listings
- Lead duplicates (same person_id, same intent within 7 days) → merge into existing lead

---

## 6. Cleanup Scheduling

| Job | Frequency | Query | Action |
|-----|-----------|-------|--------|
| Stale properties | Daily 03:00 | `WHERE status='available' AND updated_at < NOW() - 90d` | Set status = 'archived' |
| Inactive users | Daily 04:00 | `WHERE last_activity < NOW() - 90d AND state NOT IN ('inactive')` | Set state = 'inactive' |
| Expired boosts | Hourly | `WHERE boost.expires_at < NOW() AND boost.active = true` | Deactivate boost |
| Expired subscriptions | Daily 05:00 | `WHERE subscription.expires_at < NOW() AND status = 'active'` | Downgrade to free |
| Stale leads (> 30d no contact) | Daily 06:00 | `WHERE last_contact < NOW() - 30d AND status = 'engaged'` | Downgrade to COLD |
| Identity resolution batch | Daily 02:00 | Full cross-scan of persons table | Find candidates, score, group |
| Merge pending > 72h | Daily 08:00 | Pending duplicate_candidates > 72h | Escalate to vice_master |
| Data quality recalc | Daily 01:00 | All entities with grade < B | Recompute scores |
| Orphaned records | Weekly (Sun 03:00) | leads without person, properties without owner | Flag for admin |
| Audit log archive | Monthly (1st 04:00) | merge_audit > 12 months | Compress to cold storage |

---

## 7. Quality Reporting Metrics

### 7.1 Dashboard Metrics

| Metric | Definition | Target | Report |
|--------|-----------|--------|--------|
| Overall DQ score | avg(quality_score) across all entities | ≥ 70 | Daily |
| Completeness rate | avg(completeness) across all entities | ≥ 75% | Daily |
| Freshness rate | % entities within freshness SLA | ≥ 80% | Daily |
| Duplicate rate | % entities with open duplicate candidates | < 5% | Daily |
| Stale entity count | Count of entities past freshness SLA | < 10% of total | Daily |
| A+ grade % | % entities with quality ≥ 80 | ≥ 40% | Weekly |
| D grade % | % entities with quality < 20 | < 5% | Weekly |
| Merge accuracy | % auto-merges verified correct (post-audit) | ≥ 95% | Monthly |
| Resolution latency | avg time from candidate detection to resolution | < 48h | Weekly |

### 7.2 Per-Source Quality

| Source | Avg Completeness | Avg Reliability | Avg Quality | Volume |
|--------|-----------------|-----------------|-------------|--------|
| agent | 85% | 90 | 87 | tracked |
| google_form | 90% | 85 | 88 | tracked |
| import | 60% | 70 | 64 | tracked |
| whatsapp | 45% | 50 | 47 | tracked |
| unknown | 30% | 30 | 30 | tracked |

### 7.3 Quality Alerts

| Condition | Alert Level | Recipient | Action |
|-----------|-------------|-----------|--------|
| Source completeness drops > 10% in 7d | WARNING | assistant | Investigate source pipeline |
| Duplicate rate exceeds 10% | CRITICAL | vice_master | Halt auto-merge, audit |
| Overall DQ score < 50 | CRITICAL | master | Full data audit |
| Stale entities > 20% | WARNING | assistant | Trigger cleanup jobs |
| Merge accuracy < 90% | WARNING | vice_master | Review merge rules |
| Any entity with grade D > 7d | INFO | agent/owner | Send enrichment request |

### 7.4 Quality Score Formula (Reference)

```
Quality Score = Completeness × 0.6 + Reliability × 0.4
```

| Grade | Score | Action |
|-------|-------|--------|
| A+ | ≥ 80 | Direct use, high confidence |
| A | ≥ 60 | Use after minor verification |
| B | ≥ 40 | Needs completion |
| C | ≥ 20 | Enrichment required |
| D | < 20 | Re-qualification required |

### 7.5 Reliability by Source

| Source | Reliability | Justification |
|--------|-------------|---------------|
| agent | 90 | Data entered by trained agent |
| google_form | 85 | Structured form with validation |
| import | 70 | Batch import of existing data |
| whatsapp | 50 | Unstructured message, extracted by AI |
| unknown | 30 | Unidentified source |

---

*Model d'exécution patrimonial Gold — Qualité des données CRM LAWIM. Références: CRM_MODEL §9, PROP-006 à PROP-009*
