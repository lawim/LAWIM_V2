# Identity Resolution Contract — LAWIM Heritage Gold

**Source:** CRM_MODEL.md §8, RULE_INDEX.md (CRM-008)
**Mission:** H0 — LAWIM Heritage Gold
**Date:** 15 juillet 2026

---

## 1. Scoring Rules

| Criterion | Score | Algorithm | Match Condition |
|-----------|-------|-----------|-----------------|
| Phone (exact) | 100 | Exact match after normalization (+237 format) | `normalize_phone(a) == normalize_phone(b)` |
| Email (exact) | 95 | Case-insensitive exact match | `lower(a) == lower(b)` |
| WhatsApp ID | 100 | Exact match | `a == b` |
| Name + phone (similar) | ≥ 40 | Levenshtein on name (max 3 edits) + normalized phone | `lev(name_a, name_b) <= 3 AND phone_a == phone_b` |
| Name + email (similar) | ≥ 30 | Levenshtein on name (max 3 edits) + email exact | `lev(name_a, name_b) <= 3 AND email_a == email_b` |
| Name + city (exact) | ≥ 60 | Levenshtein on name + exact city match | `lev(name_a, name_b) <= 3 AND city_a == city_b` |

### Phone Normalization

| Input Format | Normalized | Example |
|-------------|------------|---------|
| 6XXXXXXXX | +237 6XXXXXXXX | +237 691234567 |
| 00237 6XXXXXXXX | +237 6XXXXXXXX | +237 691234567 |
| +237 6XXXXXXXX | +237 6XXXXXXXX | +237 691234567 |
| 691234567 | +237 691234567 | +237 691234567 |

### Match Decision

```
total_score = max(matching_criteria_scores)

if total_score >= 80:  auto_merge (high confidence)
if 40 <= total_score < 80:  flag as duplicate_candidate (pending review)
if 30 <= total_score < 40:  flag as low_confidence_candidate (optional review)
if total_score < 30:  no match
```

---

## 2. Matching Algorithm

### Step-by-Step Process

| Step | Operation | Description |
|------|-----------|-------------|
| 1 | **Normalize identifiers** | Phone → +237 format; email → lowercase; name → trim, normalize whitespace |
| 2 | **Hash indices** | Build lookup indices: phone_index, email_index, wa_id_index, name_index |
| 3 | **Exact match scan** | Scan phone, email, WhatsApp ID indices for exact matches → candidate set |
| 4 | **Fuzzy match scan** | Scan name index with Levenshtein distance ≤ 3 → expand candidate set |
| 5 | **Score computation** | For each candidate pair, compute all criteria scores, take max |
| 6 | **Threshold filter** | Filter candidates by threshold: keep ≥ 30 |
| 7 | **Deduplicate candidates** | Remove duplicate pairs (A,B) == (B,A); keep highest score |
| 8 | **Action dispatch** | auto_merge (≥ 80), pending (40–79), low_confidence (30–39), discard (< 30) |

### Pseudocode

```
def resolve_identity(person, existing_persons):
    candidates = []
    
    # Exact matches
    candidates += find_exact(person.phone, phone_index)      # score 100
    candidates += find_exact(person.email, email_index)      # score 95
    candidates += find_exact(person.wa_id, wa_id_index)      # score 100
    
    # Fuzzy matches
    for existing in name_fuzzy_match(person.name, name_index, max_dist=3):
        if person.phone and existing.phone == person.phone:
            candidates += (existing, score=40+)
        if person.email and existing.email == person.email:
            candidates += (existing, score=30+)
        if person.city and existing.city == person.city:
            candidates += (existing, score=60+)
    
    scored = [(c, max_score_for_pair(person, c)) for c in dedup(candidates)]
    return [c for c, s in scored if s >= 30]  // threshold
```

---

## 3. Merge Rules

### 3.1 Conflict Resolution

When merging two person records with conflicting attribute values:

| Attribute | Resolution Strategy | Priority Order |
|-----------|-------------------|----------------|
| phone | Most recent verified | LIFO if both verified, else prefer verified |
| email | Most recent | LIFO |
| name | Longest + most complete | Prefer full name over partial |
| city | Most recent interaction | LIFO |
| budget | Highest budget wins | Conservative: prefer higher |
| intent_type | Merge all as array | Union of all intents |
| status | Most recent activity | LIFO by last_activity |
| source | Prefer higher reliability | agent (90) > google_form (85) > import (70) > whatsapp (50) > unknown (30) |
| created_at | Earliest wins | Preserve original creation date |
| updated_at | Latest wins | Use merge timestamp |

### 3.2 Merge Algorithm

```
def merge_persons(primary, secondary):
    merged = primary.copy()
    
    for attr in conflict_attributes:
        resolved = resolve_conflict(primary[attr], secondary[attr], attr)
        merged[attr] = resolved
    
    # Merge history
    merged.message_history = merge_sorted(primary.message_history, secondary.message_history)
    merged.visit_requests = merge_union(primary.visit_requests, secondary.visit_requests)
    merged.budget_changes = merge_sorted(primary.budget_changes, secondary.budget_changes)
    merged.property_views = merge_union(primary.property_views, secondary.property_views)
    
    # Merge relationships
    merged.properties = merge_union(primary.properties, secondary.properties)
    merged.leads = merge_union(primary.leads, secondary.leads)
    merged.contact_channels = merge_union(primary.contact_channels, secondary.contact_channels)
    
    # Merge flags
    merged.is_diaspora = primary.is_diaspora or secondary.is_diaspora
    merged.is_agent = primary.is_agent or secondary.is_agent
    
    # Source
    merged.source_reliability = max(primary.source_reliability, secondary.source_reliability)
    
    return merged
```

### 3.3 Merge Transaction

```
BEGIN TRANSACTION
  1. SELECT primary person (higher reliability / older / most active)
  2. UPDATE all foreign keys referencing secondary → primary
  3. INSERT merge_audit record with before/after snapshot
  4. UPDATE person SET merged_into = primary.id WHERE person_id = secondary.id
  5. Mark secondary as merged (is_merged = true)
  6. Recalculate data quality score for merged entity
COMMIT
```

---

## 4. Deduplication Strategy

### 4.1 Detection Triggers

| Trigger | Timing | Scope |
|---------|--------|-------|
| On person creation | Before INSERT | Scan all persons |
| On person update | After UPDATE | Scan updated fields |
| On lead creation | Before INSERT | Scan persons matching lead contact |
| On import batch | Batch completion | Full cross-import scan |
| Scheduled (daily) | Daily at 02:00 | Full scan for missed duplicates |

### 4.2 Deduplication Pipeline

```
trigger → normalize → index_lookup → score → threshold → group → resolve → merge/flag
```

### 4.3 Groups

A **group** is a set of person records believed to represent the same real-world entity. Groups are formed by:

1. All pairwise matches with score ≥ 30
2. Transitive closure: if A matches B and B matches C, group = {A, B, C}
3. Even if A—C score < 30, they enter same group via B

### 4.4 Group Resolution

```
for each group:
  if all members score >= 80 pairwise: auto_merge to oldest/highest-reliability member
  if any member scores 40-79: flag as duplicate_candidate, set status = 'pending'
  if any member scores 30-39: flag as low_confidence, set status = 'optional'
  if all members < 30: no action (edge case — possible false group)
```

---

## 5. Manual Review Triggers

### 5.1 Review Required

| Condition | Action | Reviewer |
|-----------|--------|----------|
| Group has ≤ 3 members with scores 40–79 | Queue for manual review | assistant |
| Group has > 3 members | Queue for manual review | vice_master |
| Group contains conflicting roles (agent + demandeur) | Queue for review | master |
| Group contains blocked user + normal user | Queue for review | vice_master |
| Merge would affect active subscription | Queue for review | assistant |
| Merge involves diaspora_simple/rapport/complet service | Queue for review | vice_master |

### 5.2 Manual Review Interface

```
For each duplicate_candidate:
  
  Person A: {name, phone, email, city, role, source, created_at}
  Person B: {name, phone, email, city, role, source, created_at}
  
  Match score: XX (criteria: phone=100, email=95, name+phone=40, ...)
  
  Conflict list:
    - name: "Jean Dupont" vs "Jean D." → Auto-resolve: "Jean Dupont"
    - phone: +237 691234567 vs +237 691234567 → Match
    - email: j@gmail.com vs NULL → Auto-resolve: j@gmail.com
    - role: demandeur vs agent → CONFLICT: manual required
  
  Actions:
    [MERGE] [REJECT] [EDIT A] [EDIT B] [SKIP]
```

### 5.3 Review SLA

| Priority | Max Review Time | Escalation |
|----------|----------------|------------|
| score ≥ 80 (auto) | Instant | None |
| score 70–79 | < 24h | If pending > 24h → vice_master |
| score 60–69 | < 48h | If pending > 48h → vice_master |
| score 40–59 | < 72h | If pending > 72h → vice_master |
| score 30–39 | < 7 days | Optional — can be discarded |

---

## 6. Audit Trail

### 6.1 Merge Audit Log Schema

```sql
CREATE TABLE merge_audit (
    audit_id          BIGSERIAL PRIMARY KEY,
    merged_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    primary_person_id BIGINT NOT NULL REFERENCES persons(person_id),
    secondary_person_id BIGINT NOT NULL REFERENCES persons(person_id),
    merge_type        VARCHAR(20) NOT NULL CHECK (merge_type IN ('auto', 'manual', 'batch')),
    triggered_by      VARCHAR(50),       -- system_event, user_id, batch_id
    match_score       INTEGER NOT NULL,
    matching_criteria JSONB,             -- {phone:100, email:95, ...}
    before_snapshot   JSONB NOT NULL,    -- full secondary record before merge
    after_snapshot    JSONB NOT NULL,    -- full primary record after merge
    conflicts         JSONB,             -- [{attribute, a_value, b_value, resolution}]
    reviewed_by       BIGINT REFERENCES persons(person_id),
    status            VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('completed', 'rejected', 'pending'))
);

CREATE INDEX idx_merge_audit_primary ON merge_audit(primary_person_id);
CREATE INDEX idx_merge_audit_secondary ON merge_audit(secondary_person_id);
CREATE INDEX idx_merge_audit_merged_at ON merge_audit(merged_at);
```

### 6.2 Audit Events

| Event | Logged When | Data Captured |
|-------|-------------|---------------|
| `identity.candidates_found` | New duplicate candidates detected | {primary_id, secondary_id[], scores[]} |
| `identity.merge.auto` | Auto-merge executed | Full before/after snapshots |
| `identity.merge.manual` | Manual merge approved/rejected | Reviewer, decision, reason |
| `identity.merge.rejected` | Merge candidate rejected | Reviewer, reason |
| `identity.group.created` | New resolution group formed | {group_id, member_ids, max_score} |
| `identity.group.resolved` | Group fully resolved | {group_id, merge_audit_ids[]} |

### 6.3 Rollback

If a merge is later found to be incorrect:

1. Create inverse merge record in `merge_audit` with `status = 'rejected'`
2. Restore secondary person from `before_snapshot`
3. Revert merged attributes on primary using `after_snapshot` + conflict history
4. Log rollback event

---

## 7. Data Quality Impact

After each merge, the data quality score of the resulting entity is recalculated:

```
post_merge_quality = completeness(merged) × 0.6 + reliability(merged) × 0.4
```

Where:
- Completeness improves (merged fields from both records)
- Reliability = max(source reliability of all merged records)

**Expected improvement:** Merged entities typically gain 10–20 quality points due to combined fields.

---

## 8. Edge Cases

| Case | Handling |
|------|----------|
| Same person creates two accounts (different phones) | Matched via name+city (≥60) → flagged for manual review if no email match |
| Person changes phone number | Both phones kept in contact_channels; phone_index has both |
| Agent also a property seeker | Both roles merged → is_agent=true, role array includes both |
| Spammer creates multiple accounts | Cross-account matching via WhatsApp ID (100) → all flagged, merged to blocked |
| Diaspora user with local proxy | Name+phone match via proxy's phone → flagged for review (different locations) |
| Import from CSV with imperfect data | Name fuzzy matching catches most; manual review for edge cases |

---

*Contract patrimonial Gold — Identity Resolution pour le CRM LAWIM. Référence: CRM-008*
