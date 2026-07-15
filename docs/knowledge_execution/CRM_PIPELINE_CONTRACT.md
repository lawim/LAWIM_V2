# CRM Pipeline Contract — LAWIM Heritage Gold

**Source:** CRM_MODEL.md §1, RULE_INDEX.md (QUAL-006, QUAL-007)
**Mission:** H0 — LAWIM Heritage Gold
**Date:** 15 juillet 2026

---

## 1. 8-Stage Pipeline

```
incoming → normalize → extract → detect_intent → context → scoring → classification → routing
```

### Stage Definitions

| # | Stage | Input | Processing | Output | Rules |
|---|-------|-------|------------|--------|-------|
| 1 | **incoming** | Raw WhatsApp/Telegram message | Channel detection, format normalization, metadata capture | Normalized message envelope | CRM-004 (event: message.received) |
| 2 | **normalize** | Normalized message | Orthographic correction, typo fixing, slang normalization, language detection | Cleaned text | LANG-001 to LANG-014 |
| 3 | **extract** | Cleaned text | NER extraction: budget, city, neighborhood, property_type, phone, price | Structured entities | GEO-004 to GEO-006, QUAL-010 |
| 4 | **detect_intent** | Entities + text | Intent classification: buy/rent/sell/invest + confidence score | Intent + confidence | QUAL-008, CONV-005 |
| 5 | **context** | Intent + entities | History lookup, behavior tracking, profile enrichment | Full context envelope | QUAL-010 to QUAL-012, CONV-010 |
| 6 | **scoring** | Full context | V5 scoring 7 factors: type, budget, location, urgency, completeness, engagement, diaspora | Numeric score [0,1] | QUAL-001 to QUAL-003, CRM-014 |
| 7 | **classification** | Score | Threshold mapping → HOT/WARM/COLD/LOW/SPAM + priority P0–P3 | Class + priority | QUAL-004, QUAL-005, QUAL-018 |
| 8 | **routing** | Class + priority | Agent assignment, dashboard placement, auto-response, notification | Action dispatched | CRM-005, CRM-012, assignment rules |

### Stage SLA

| Stage | Max Processing Time | Retry | Failure Action |
|-------|-------------------|-------|----------------|
| incoming | < 100ms | 0 | Dead letter queue |
| normalize | < 500ms | 1 | Fallback: use raw text |
| extract | < 1s | 1 | Partial entities, continue |
| detect_intent | < 2s | 2 | Default intent: "unknown" |
| context | < 500ms | 1 | Use current message only |
| scoring | < 500ms | 1 | Default score: 0 |
| classification | < 100ms | 0 | Default: LOW |
| routing | < 1s | 2 | Queue for manual routing |

### Data Contracts Between Stages

```
incoming → normalize:
  { channel, raw_text, sender_id, timestamp, message_id }

normalize → extract:
  { channel, clean_text, language, sender_id, message_id }

extract → detect_intent:
  { clean_text, entities: { budget?, city?, neighborhood?, property_type?, phone?, price? }, language }

detect_intent → context:
  { text, entities, intent: { type, confidence }, language }

context → scoring:
  { person_id, intent, entities, history: { message_count, avg_response_time, budget_changes[], visit_requests[] },
    behavior: { last_interaction, total_interactions } }

scoring → classification:
  { score: float [0,1], factors: { type_score, budget_score, location_score, urgency_score,
    completeness_score, engagement_score, diaspora_score } }

classification → routing:
  { score, class: HOT|WARM|COLD|LOW|SPAM, priority: P0|P1|P2|P3, action: call_immediately|send_listings|request_budget|follow_up|ignore }
```

---

## 2. Lead Lifecycle Stages

| Stage | Code | Entry Criteria | Exit Criteria | Max Duration | Owner |
|-------|------|----------------|---------------|--------------|-------|
| Raw lead | `raw` | Message received, no entities extracted | Entities extracted | 5 min | pipeline |
| Qualified lead | `qualified` | Entities + intent known | Score computed | 2 min | pipeline |
| Scored lead | `scored` | V5 score ≥ threshold (≥ 0.3 for COLD+) | Classification assigned | 1 min | pipeline |
| Classified lead | `classified` | Class + priority assigned | Routed to agent/dashboard | 1 min | pipeline |
| Assigned lead | `assigned` | Agent confirmed (or auto-routed) | First contact made | P0: 30min, P1: 2h, P2: 24h, P3: 7d | agent |
| Contacted lead | `contacted` | First outreach sent | Lead responds | 48h | agent |
| Engaged lead | `engaged` | Lead responded, active conversation | Visit scheduled or deal closed | — | agent |
| Visit scheduled | `visit_scheduled` | Visit date confirmed | Visit occurs | 7 days | agent |
| Visit done | `visit_done` | Visit completed | Decision made | 48h | agent |
| Negotiating | `negotiating` | Price/terms discussion active | Agreement or rejection | 30 days | agent |
| Converted | `converted` | Transaction signed | Lead closed | — | agent |
| Lost | `lost` | Lead rejected or unresponsive | — | — | agent |
| Recycled | `recycled` | Lost but re-engages | Re-enters pipeline | — | pipeline |

---

## 3. Contact Lifecycle

| Milestone | Timing | Channel | Template | Trigger |
|-----------|--------|---------|----------|---------|
| Welcome | Immediate | WhatsApp | `welcome` template | user.created |
| First response | P0: < 1h, P1: < 2h, P2: < 24h, P3: J+1–7 | WhatsApp | Personalized + listing (if matched) | lead.created |
| Follow-up J+1 | 24h post-first | WhatsApp | Re-engagement | timer |
| Follow-up J+7 | 168h post-first | WhatsApp | New listings, open question | timer |
| Follow-up J+30 | 720h post-first | WhatsApp | Check budget change, new inventory | timer |
| Follow-up J+90 | 2160h post-first | WhatsApp | Final re-engagement | timer |
| Long-term archive | > 365 days | — | Move to cold storage | timer |

**Multi-channel support** (Phase 3): Telegram, Facebook, Email — same lifecycle, different templates.

---

## 4. Conversion Tracking

| Metric | Definition | Calculation | Target |
|--------|-----------|-------------|--------|
| Lead-to-contact rate | % classified → contacted | contacted / classified × 100 | ≥ 90% |
| Contact-to-engagement | % contacted → responded | engaged / contacted × 100 | ≥ 60% |
| Engagement-to-visit | % engaged → visit scheduled | visit_scheduled / engaged × 100 | ≥ 40% |
| Visit-to-conversion | % visited → converted | converted / visit_done × 100 | ≥ 30% |
| Overall conversion | % raw → converted | converted / raw × 100 | ≥ 5% |
| Time-to-first-contact | Avg time from lead.created to first contact | Duration | P0 < 30min, overall < 2h |
| Time-to-close | Avg time from lead.created to converted | Duration | < 60 days |

### Conversion Funnel

```
Raw Leads:            100%
  → Qualified:        85%   (-15% incomplete data)
    → Scored:         80%   (-5% below threshold)
      → Classified:   75%   (-5% spam/fraud)
        → Assigned:   70%   (-5% no available agent)
          → Contacted: 63%  (-7% agent missed SLA)
            → Engaged: 38%  (-25% no response)
              → Visit:  15%  (-23% not interested)
                → Converted: 6%  (-9% negotiation failed)
```

---

## 5. Pipeline Metrics

### Count Metrics

| Metric | Source | Update Frequency |
|--------|--------|-----------------|
| Incoming messages (24h) | message.received event | Real-time |
| Qualified leads (24h) | lead.created event | Real-time |
| Active leads | leads WHERE status NOT IN (lost, converted, archived) | Real-time |
| Leads by class | leads GROUP BY class | Real-time |
| Leads by priority | leads GROUP BY priority | Real-time |
| Unassigned leads | leads WHERE agent_id IS NULL | Real-time |
| Stale leads (> 7d no contact) | leads WHERE last_contact < NOW() - 7d | Daily batch |
| Agent workload | leads GROUP BY agent_id | Real-time |

### Conversion Rates

| Rate | Formula | Refresh |
|------|---------|---------|
| Pipeline conversion | converted / total (30d rolling) | Daily |
| Stage conversion | stage_exits_success / stage_entries (30d rolling) | Daily |
| Agent conversion | converted_by_agent / assigned_to_agent (30d) | Daily |
| Channel conversion | converted_by_channel / leads_by_channel | Daily |

### Velocity

| Metric | Formula | Target |
|--------|---------|--------|
| Stage velocity | avg(duration_in_stage) over 30d | Varies by stage |
| Pipeline velocity | avg(time_from_raw_to_converted) | < 60 days |
| Response velocity | avg(time_from_assigned_to_contacted) | < 2h (P0–P2) |
| Follow-up velocity | avg(time_between_contacts) | 3–7 days |

---

## 6. SLA per Pipeline Stage

| Stage | P0 | P1 | P2 | P3 | Escalation on Miss |
|-------|----|----|----|----|-------------------|
| incoming → normalize | < 1s | < 1s | < 1s | < 1s | Auto-retry, then queue |
| normalize → extract | < 2s | < 2s | < 2s | < 2s | Fallback extraction |
| extract → intent | < 3s | < 3s | < 3s | < 3s | Default intent |
| intent → scoring | < 1s | < 1s | < 1s | < 1s | Default 0 score |
| scoring → classification | < 500ms | < 500ms | < 500ms | < 500ms | Default LOW |
| classification → routing | < 1s | < 1s | < 5s | < 10s | Queue for manual |
| **Routing → agent contact** | **< 30 min** | **< 2h** | **< 24h** | **J+1 to J+7** | Escalate up chain |
| Agent first response | < 1h | < 4h | < 48h | J+7 | Escalate to agence |
| Follow-up J+1 | — | — | — | J+1 | Auto-reminder |
| Follow-up J+7 | — | — | — | J+7 | Auto-reminder |
| Follow-up J+30 | — | — | — | J+30 | Auto-reminder |
| Follow-up J+90 | — | — | — | J+90 | Archive if no response |

---

## 7. Escalation Rules

### 7.1 SLA Miss Escalation

```
Level 1 (SLA miss on routing):
  → Notify agent
  → If no action within 50% of SLA: notify agence
  
Level 2 (agent misses first contact SLA):
  → Re-assign lead to next available agent (same zone)
  → Notify original agent
  → Log SLA miss in agent_performance
  
Level 3 (no agent available in zone):
  → Escalate to agence for manual assignment
  → If agence unresponsive > 4h: escalate to assistant
  
Level 4 (critical — P0 lead unassigned > 1h):
  → Escalate directly to vice_master
  → Auto-assign to top-rated agent nationally (override zone)
```

### 7.2 Priority Escalation Path

| From Priority | Escalates To | Condition | Action |
|---------------|-------------|-----------|--------|
| P3 | P2 | User provides budget + location | Re-score |
| P2 | P1 | Visit requested + budget confirmed | Re-score, reassign |
| P1 | P0 | Diaspora detected + cash purchase | Re-score, re-route |
| Any | vice_master | Complaint or dispute lodged | Manual review |

### 7.3 Escalation Chain by Role

```
Lead Issue:
  agent → agence → assistant → vice_master → master

Technical Issue:
  assistant → vice_master → master

Fraud/Security:
  agent → assistant → vice_master → master (immediate)

Partner Escalation:
  agent → agence → vice_master
```

---

## 8. Pipeline Data Store

### Stage Transition Log

```
pipeline_log:
  { lead_id, stage_from, stage_to, transition_time, triggered_by, duration_ms, status }
```

### Current Pipeline Snapshot

```
pipeline_state:
  { lead_id, current_stage, entered_at, sla_deadline, owner_id, priority }
```

### Metrics Aggregation

```
pipeline_metrics_daily:
  { date, stage, entries, exits_success, exits_fail, avg_duration_ms, p50, p95, p99 }
```

---

## 9. Quality Gates per Stage

| Stage | Quality Gate | Rejection Condition | Remediation |
|-------|-------------|-------------------|-------------|
| incoming | Valid channel + non-empty | Empty message, unknown channel | Drop with log |
| normalize | Language detected | Language detection fails | Default to FR |
| extract | At least 1 entity | Zero entities extracted | Flag as "low_info" |
| detect_intent | Confidence ≥ 0.3 | Confidence < 0.3 | Default BUY + flag |
| context | Profile exists | Unknown person_id | Create minimal profile |
| scoring | All 7 factors computable | Factor computation fails | Use 0 for that factor |
| classification | Valid threshold | Score outside [0,1] | Clamp + log |
| routing | Agent identified | No matching agent | Queue for manual routing |

---

*Contract patrimonial Gold — Pipeline exécutable pour le CRM LAWIM*
