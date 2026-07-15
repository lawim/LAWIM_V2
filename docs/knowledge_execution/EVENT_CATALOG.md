# Event Catalog

**Domain:** Event Engine — Complete Event Type Registry
**Version:** 1.0
**Status:** CANONICAL
**Total Event Types:** 66

---

## Event Catalog Format

Each event entry follows this structure:

```
event_type: <name>
  producer: <engine>
  trigger: <condition that fires this event>
  payload: { <key>: <type> — description }
  privacy_level: <public|low|medium|high|critical>
  audit_visibility: <public|internal|confidential|restricted>
  consumers: [<consumer list>]
```

---

## Section 1: Conversation Events

### 1.1 `message.received`

```
event_type: message.received
  producer: Conversation Engine
  trigger: Incoming WhatsApp/Telegram message via webhook
  payload: {
    channel: string — source channel (whatsapp, telegram)
    sender_id: string — sender identifier on the channel
    raw_text: string — original message text
    message_id: string — provider message ID
    media_url: string? — attached media URL if any
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [CRM Pipeline, Language Engine, Qualification Engine]
```

### 1.2 `message.sent`

```
event_type: message.sent
  producer: Conversation Engine
  trigger: Outbound message dispatched to user
  payload: {
    channel: string — target channel
    recipient_id: string — recipient identifier
    template: string — template name used
    content: string — message content (redacted if privacy_level high)
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Audit System, Continuous Learning, Reporting]
```

### 1.3 `intent.detected`

```
event_type: intent.detected
  producer: Conversation Engine / CRM Pipeline
  trigger: Intent classification confidence >= threshold
  payload: {
    intent: string — detected intent (buy, rent, sell, invest)
    confidence: float — classification confidence [0-1]
    method: string — classification method (ml, rule, fallback)
    alternatives: [{ type: string, confidence: float }]
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Qualification Engine, CRM Engine, Search Engine, Decision Engine]
```

### 1.4 `fact.extracted`

```
event_type: fact.extracted
  producer: Conversation Engine / Qualification Engine
  trigger: Entity extraction identifies a structured fact from conversation
  payload: {
    fact_type: string — type (budget, city, property_type, phone, etc.)
    fact_value: any — extracted value
    extraction_method: string — method (ner, regex, llm)
    source_message_id: string — originating message
    confidence: float — extraction confidence
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Qualification Engine, Search Engine, Knowledge Registry, Decision Engine]
```

### 1.5 `fact.confirmed`

```
event_type: fact.confirmed
  producer: Qualification Engine
  trigger: User explicitly confirms or validates a previously extracted fact
  payload: {
    fact_type: string
    fact_value: any — confirmed value
    confirmation_method: string — explicit, cross_reference, inferred
    previous_value: any — value before confirmation
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Knowledge Registry, Search Engine, Decision Engine, Qualification Engine]
```

### 1.6 `fact.superseded`

```
event_type: fact.superseded
  producer: Qualification Engine
  trigger: An existing fact is replaced by newer information
  payload: {
    fact_type: string
    old_value: any
    new_value: any
    reason: string — why superseded (user_correction, recency, conflict_resolution)
    superseded_at: timestamp
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [Knowledge Registry, Decision Engine, Search Engine, Continuous Learning]
```

### 1.7 `question.selected`

```
event_type: question.selected
  producer: Qualification Engine / Conversation Engine
  trigger: NBA determines next question to ask user
  payload: {
    question_id: string — canonical question identifier
    question_text: string — localized question
    target_fact: string — which fact this question aims to collect
    priority: int — question priority in the queue
    follow_up_previous: string? — previous question_id if this is a follow-up
  }
  privacy_level: public
  audit_visibility: public
  consumers: [Conversation Engine, NBA Engine, Reporting]
```

---

## Section 2: Qualification Events

### 2.1 `qualification.updated`

```
event_type: qualification.updated
  producer: Qualification Engine
  trigger: Any change to qualification data (score, fields, readiness)
  payload: {
    qualification_id: string
    property_id: string? — linked property if applicable
    dossier_id: string? — linked dossier if applicable
    score: float — current qualification score
    score_breakdown: { type: score } — score per dimension
    fields_completed: int — number of completed fields
    fields_total: int — total required fields
    changes: [{ field: string, old: any, new: any }]
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Decision Engine, NBA Engine, CRM Engine, Reporting]
```

### 2.2 `readiness.changed`

```
event_type: readiness.changed
  producer: Qualification Engine
  trigger: Entity transitions between readiness levels (not_ready, partially_ready, ready)
  payload: {
    entity_type: string
    entity_id: string
    previous_readiness: string
    new_readiness: string
    missing_critical_fields: [string]
    readiness_score: float
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [Workflow Engine, NBA Engine, Decision Engine, SLA Monitor]
```

### 2.3 `field.completed`

```
event_type: field.completed
  producer: Qualification Engine
  trigger: A qualification field is filled with valid data
  payload: {
    entity_type: string
    entity_id: string
    field_name: string
    field_value: any (masked if PII)
    is_critical: boolean
    completion_method: string — user_input, extraction, inference, system
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Workflow Engine, NBA Engine, Reporting]
```

---

## Section 3: Search and Matching Events

### 3.1 `search.started`

```
event_type: search.started
  producer: Search Engine
  trigger: Search query submitted (after qualification completes)
  payload: {
    search_id: string
    query: { criteria: object — normalized search criteria }
    search_scope: string — initial, expanded, rematch
    entity_id: string — dossier or property being searched for
    trigger_rule: string? — rule that initiated the search
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Matching Engine, Reporting, Continuous Learning]
```

### 3.2 `search.completed`

```
event_type: search.completed
  producer: Search Engine
  trigger: Search execution finished with results
  payload: {
    search_id: string
    result_count: int
    execution_time_ms: int
    search_strategy: string — single, progressive, expanded
    expansions_used: [string] — list of expansion strategies applied
    top_score: float? — highest match score found
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Matching Engine, NBA Engine, Reporting, Continuous Learning]
```

### 3.3 `search.expanded`

```
event_type: search.expanded
  producer: Search Engine
  trigger: Search scope expanded due to insufficient initial results
  payload: {
    search_id: string
    expansion_reason: string — reason for expansion
    expansion_strategy: string — geography, budget, property_type
    original_criteria: object
    expanded_criteria: object
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [Matching Engine, Continuous Learning, Reporting]
```

### 3.4 `matching.started`

```
event_type: matching.started
  producer: Matching Engine
  trigger: Matching computation initiated for a dossier
  payload: {
    matching_id: string
    dossier_id: string
    property_count: int — number of properties in the pool
    scoring_dimensions: [string]
    rematch: boolean — whether this is a rematch
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Workflow Engine, Reporting]
```

### 3.5 `matching.completed`

```
event_type: matching.completed
  producer: Matching Engine
  trigger: Matching computation finished with scores
  payload: {
    matching_id: string
    dossier_id: string
    total_scores: int — properties scored
    top_5_scores: [float] — top 5 match scores
    avg_score: float — average score of top 10
    execution_time_ms: int
  }
  privacy_level: low
  audit_visibility: public
  consumers: [NBA Engine, Workflow Engine, Reporting, Continuous Learning]
```

### 3.6 `match.generated`

```
event_type: match.generated
  producer: Matching Engine
  trigger: A specific property-dossier pair is found compatible and scored
  payload: {
    match_id: string
    dossier_id: string
    property_id: string
    score: float — composite match score
    score_components: { dimension: float } — per-dimension scores
    rank: int — rank in the property list
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Relationship Engine, NBA Engine, Notification System, CRM Engine]
```

### 3.7 `match.rejected`

```
event_type: match.rejected
  producer: Matching Engine / Relationship Engine
  trigger: A proposed match is refused by either party
  payload: {
    match_id: string
    dossier_id: string
    property_id: string
    rejection_source: string — demandeur, holder, system
    rejection_reason: string — reason code
    rejection_detail: string? — free text detail
    previous_matches_count: int — total rejections for this dossier
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [Matching Engine, Continuous Learning, NBA Engine, Reporting]
```

### 3.8 `result.selected`

```
event_type: result.selected
  producer: Search Engine / Conversation Engine
  trigger: User selects a specific result from presented options
  payload: {
    result_id: string
    entity_type: string
    entity_id: string
    selection_context: string — search, matching, presentation
    rank: int — rank at selection time
    previous_selections: [string] — history for this session
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Matching Engine, Relationship Engine, NBA Engine, Continuous Learning]
```

### 3.9 `score.calculated`

```
event_type: score.calculated
  producer: Matching Engine
  trigger: A scoring dimension is computed for a match
  payload: {
    match_id: string
    dimension: string — real_estate, availability, document, holder_reliability, transaction_success
    score: float — dimension score
    factors: [{ name: string, weight: float, value: any }]
    calculation_method: string
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [Matching Engine, Continuous Learning]
```

---

## Section 4: CRM and Lead Events

### 4.1 `lead.created`

```
event_type: lead.created
  producer: CRM Engine
  trigger: Lead scoring produces score >= minimum threshold for a user
  payload: {
    lead_id: string
    person_id: string
    lead_type: string — tenant, buyer, seller, investor, diaspora_investor
    score: float — V5 composite score
    source: string — message, referral, import, system
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Notification System, NBA Engine, Relationship Engine, Reporting]
```

### 4.2 `lead.scored`

```
event_type: lead.scored
  producer: CRM Engine
  trigger: Lead score computed or recalculated
  payload: {
    lead_id: string
    score: float — numeric score
    factors: { factor: float } — score factor contributions
    boosters_applied: [string]
    penalties_applied: [string]
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [Workflow Engine, NBA Engine, Reporting]
```

### 4.3 `lead.classified`

```
event_type: lead.classified
  producer: CRM Engine
  trigger: Lead classification determined from score threshold
  payload: {
    lead_id: string
    class: string — HOT, WARM, COLD, LOW, SPAM
    priority: string — P0, P1, P2, P3
    sla_deadline: timestamp
    recommended_action: string
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Notification System, NBA Engine, Workflow Engine, Routing Engine]
```

### 4.4 `lead.routed`

```
event_type: lead.routed
  producer: CRM Engine
  trigger: Lead assigned to an agent or queued for routing
  payload: {
    lead_id: string
    routing_strategy: string — auto, zone, workload, manual
    assigned_to: string? — agent_id or null if queued
    routing_rules_applied: [string]
    queue_position: int? — position if not immediately assigned
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Notification System, NBA Engine, Reporting, Agent Dashboard]
```

### 4.5 `identity.resolved`

```
event_type: identity.resolved
  producer: CRM Engine / Identity Resolution Engine
  trigger: Identity resolution matches a message to known user (or creates new)
  payload: {
    person_id: string — resolved person ID
    resolution_method: string — exact_match, fuzzy_match, channel_match, new_creation
    matched_attributes: [string] — phone, email, name, device
    confidence: float — match confidence
    previous_person_id: string? — if merged
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [CRM Engine, Conversation Engine, Qualification Engine, Reporting]
```

### 4.6 `user.created`

```
event_type: user.created
  producer: Administration Engine
  trigger: New user account registered
  payload: {
    user_id: string
    channel: string — registration channel
    initial_role: string
    trust_level: int — initial trust level
    referral_source: string? — how user was acquired
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Workflow Engine, Notification System, CRM Engine, Reporting]
```

---

## Section 5: Relationship and Consent Events

### 5.1 `relationship.created`

```
event_type: relationship.created
  producer: Relationship Engine
  trigger: Double consent obtained, relationship record created between demandeur and holder
  payload: {
    relationship_id: string
    demandeur_id: string
    holder_id: string
    property_id: string
    dossier_id: string
    match_id: string
    relationship_type: string — direct, agent_mediated, partner_introduced
    consent_timestamp: timestamp
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Workflow Engine, Notification System, NBA Engine, Visit Engine, Reporting]
```

### 5.2 `relationship.expired`

```
event_type: relationship.expired
  producer: Relationship Engine
  trigger: Relationship reaches end of lifecycle (natural end, SLA timeout)
  payload: {
    relationship_id: string
    reason: string — inactivity, transaction_complete, timeout
    duration_days: int
    last_interaction: timestamp
    outcome: string — converted, abandoned, timeout
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [NBA Engine, Workflow Engine, Continuous Learning, Reporting]
```

### 5.3 `relationship.revoked`

```
event_type: relationship.revoked
  producer: Relationship Engine / Security Engine
  trigger: Relationship forcibly terminated by admin, fraud, or consent withdrawal
  payload: {
    relationship_id: string
    revoked_by: string — actor_id
    reason: string — consent_withdrawn, fraud, policy_violation, admin_action
    detail: string?
    consent_withdrawn: boolean — whether consent withdrawal triggered this
  }
  privacy_level: critical
  audit_visibility: restricted
  consumers: [Security Engine, Audit System, Workflow Engine, Notification System]
```

### 5.4 `consent.requested`

```
event_type: consent.requested
  producer: Relationship Engine
  trigger: System requests consent from a party for contact/information sharing
  payload: {
    consent_request_id: string
    requested_from: string — actor_id of the consenting party
    requested_by: string — actor_id of the requesting party
    consent_type: string — contact_sharing, data_access, location_tracking, marketing
    consent_channel: string — channel used for request
    expiry: timestamp? — consent validity period
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Conversation Engine, Notification System, Security Engine]
```

### 5.5 `consent.granted`

```
event_type: consent.granted
  producer: Relationship Engine
  trigger: Party explicitly grants consent
  payload: {
    consent_request_id: string
    consent_id: string
    granted_by: string — actor_id
    consent_type: string
    scope: string — scope of consent
    valid_until: timestamp?
    channel: string — channel where consent was given
  }
  privacy_level: critical
  audit_visibility: restricted
  consumers: [Relationship Engine, Workflow Engine, NBA Engine, Security Engine, Audit System]
```

### 5.6 `consent.refused`

```
event_type: consent.refused
  producer: Relationship Engine
  trigger: Party explicitly refuses consent or request times out
  payload: {
    consent_request_id: string
    refused_by: string — actor_id
    consent_type: string
    reason: string? — optional reason
    refusal_stage: string — explicit_refusal, timeout, channel_unavailable
    alternate_proposed: boolean — whether an alternative was offered
  }
  privacy_level: critical
  audit_visibility: restricted
  consumers: [Relationship Engine, NBA Engine, Conversation Engine, Continuous Learning]
```

---

## Section 6: Proposal and Negotiation Events

### 6.1 `proposal.created`

```
event_type: proposal.created
  producer: Negotiation Engine / Conversation Engine
  trigger: A formal proposal or offer is created
  payload: {
    proposal_id: string
    negotiation_id: string?
    proposal_type: string — initial, counter, final
    proposed_by: string — actor_id
    terms: { term: value } — key terms (price, conditions, deadlines)
    valid_until: timestamp?
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Negotiation Engine, Notification System, NBA Engine, Reporting]
```

### 6.2 `negotiation.started`

```
event_type: negotiation.started
  producer: Negotiation Engine
  trigger: Negotiation channel opened after positive visit or expression of intent
  payload: {
    negotiation_id: string
    relationship_id: string
    property_id: string
    dossier_id: string
    parties: [string] — actor_ids of all parties
    negotiable_elements: [string]
    opening_position: { element: value }
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Workflow Engine, Notification System, NBA Engine, Reporting]
```

### 6.3 `negotiation.accepted`

```
event_type: negotiation.accepted
  producer: Negotiation Engine
  trigger: Parties reach agreement in principle or final agreement
  payload: {
    negotiation_id: string
    agreement_type: string — in_principle, final
    agreed_terms: { term: value }
    accepted_by: [string] — actor_ids
    duration_days: int — total negotiation duration
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Workflow Engine, Transaction Engine, NBA Engine, Reporting]
```

### 6.4 `negotiation.rejected`

```
event_type: negotiation.rejected
  producer: Negotiation Engine
  trigger: Negotiation fails — party withdraws, timeout, or impasse
  payload: {
    negotiation_id: string
    reason: string — party_withdrawal, timeout, impasse, property_unavailable
    rejected_by: string? — actor_id
    final_positions: { party: { element: value } }
    duration_days: int
    rematch_proposed: boolean
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Workflow Engine, NBA Engine, Matching Engine, Continuous Learning]
```

### 6.5 `price.updated`

```
event_type: price.updated
  producer: Negotiation Engine
  trigger: Price term changes during negotiation
  payload: {
    negotiation_id: string
    property_id: string
    previous_price: float
    new_price: float
    changed_by: string — actor_id
    reason: string?
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Negotiation Engine, Reporting, Transaction Engine]
```

---

## Section 7: Property Events

### 7.1 `property.created`

```
event_type: property.created
  producer: Administration Engine / CRM Engine
  trigger: New property record created in the system
  payload: {
    property_id: string
    owner_id: string
    property_type: string — house, apartment, land, commercial
    operation: string — sale, rent
    location: { city: string, neighborhood: string?, coordinates: { lat: float, lng: float }? }
    initial_state: string — initial workflow state
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Workflow Engine, Geography Engine, Search Engine, Reporting]
```

### 7.2 `property.updated`

```
event_type: property.updated
  producer: Administration Engine / Qualification Engine
  trigger: Property details modified
  payload: {
    property_id: string
    updated_by: string — actor_id
    changes: [{ field: string, old: any, new: any }]
    reason: string? — modification reason
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Workflow Engine, Search Engine, Matching Engine, Reporting]
```

### 7.3 `property.archived`

```
event_type: property.archived
  producer: Workflow Engine
  trigger: Property reaches terminal archived state
  payload: {
    property_id: string
    reason: string — owner_request, obsolescence, auto_archival
    final_state: string
    lifetime_days: int
    match_count: int — total matches during lifetime
    visit_count: int
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Reporting, Continuous Learning, Storage Lifecycle Manager]
```

### 7.4 `property.published`

```
event_type: property.published
  producer: Workflow Engine
  trigger: Property validation completed, listing published
  payload: {
    property_id: string
    publication_channel: string — platform, sie
    reference_code: string? — SIE reference code
    visibility: string — public, private, agent_only
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Search Engine, Matching Engine, Notification System, Reporting]
```

### 7.5 `property.unavailable`

```
event_type: property.unavailable
  producer: Workflow Engine
  trigger: Property sold or rented, marked unavailable
  payload: {
    property_id: string
    reason: string — sold, rented, withdrawn
    transaction_id: string?
    final_price: float?
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Matching Engine, Notification System, Reporting, Continuous Learning]
```

---

## Section 8: State Transition and Workflow Events

### 8.1 `state.transitioned`

```
event_type: state.transitioned
  producer: Workflow Engine
  trigger: Any successful state machine transition in any workflow
  payload: {
    workflow_id: string — canonical workflow ID
    entity_type: string
    entity_id: string
    from_state: string
    to_state: string
    transition_event: string — event that triggered transition
    transition_duration_ms: int — time in previous state
    guard_results: [{ guard: string, passed: boolean }]
    sla_status: string — within_sla, approaching, breached
  }
  privacy_level: low
  audit_visibility: public
  consumers: [NBA Engine, SLA Monitor, Notification System, Reporting, Audit System, Continuous Learning]
```

### 8.2 `state_transition.failed`

```
event_type: state_transition.failed
  producer: Workflow Engine
  trigger: Transition guard fails or action execution fails
  payload: {
    workflow_id: string
    entity_type: string
    entity_id: string
    from_state: string
    to_state: string
    failure_reason: string
    failure_point: string — guard, action, persistence
    failed_guard: string? — name of failed guard
    failed_action: string? — name of failed action
    compensation_executed: boolean
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [NBA Engine, Audit System, SLA Monitor, Admin Dashboard]
```

### 8.3 `action.planned`

```
event_type: action.planned
  producer: NBA Engine / Decision Engine
  trigger: NBA resolved to a concrete action for an entity
  payload: {
    action_id: string
    entity_type: string
    entity_id: string
    action_type: string — call, message, visit, negotiate, etc.
    priority: int
    triggering_nba: string
    triggering_rule: string?
    scheduled_at: timestamp?
    blocking_conditions: [string]
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [Conversation Engine, Notification System, SLA Monitor, Workflow Engine]
```

### 8.4 `action.executed`

```
event_type: action.executed
  producer: Action Executor / Domain Engine
  trigger: A planned action is successfully executed
  payload: {
    action_id: string
    action_type: string
    entity_type: string
    entity_id: string
    execution_channel: string — channel used
    execution_result: string — success, partial
    execution_duration_ms: int
    nba_action_id: string? — linking back to NBA plan
    decision_id: string? — linking back to decision
  }
  privacy_level: low
  audit_visibility: public
  consumers: [NBA Engine, Continuous Learning, Reporting, SLA Monitor]
```

### 8.5 `action.failed`

```
event_type: action.failed
  producer: Action Executor / Domain Engine
  trigger: Action execution fails (channel, permission, system error)
  payload: {
    action_id: string
    action_type: string
    entity_type: string
    entity_id: string
    failure_reason: string
    failure_stage: string — validation, channel, permission, system
    retry_count: int
    max_retries_reached: boolean
    fallback_activated: boolean
    fallback_action: string?
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [NBA Engine, Notification System, SLA Monitor, Admin Dashboard, Continuous Learning]
```

### 8.6 `follow_up.scheduled`

```
event_type: follow_up.scheduled
  producer: Decision Engine / NBA Engine
  trigger: Follow-up timer created for an entity
  payload: {
    follow_up_id: string
    entity_type: string
    entity_id: string
    follow_up_type: string — reminder, SLA_monitor, reengagement, escalation
    scheduled_at: timestamp
    trigger_condition: string — time_elapsed, event, condition_met
    follow_up_action: string
    nba_action_id: string?
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [SLA Monitor, Notification System, Workflow Engine, Reporting]
```

### 8.7 `SLA.breached`

```
event_type: SLA.breached
  producer: SLA Monitor
  trigger: Entity remains in a state beyond SLA threshold
  payload: {
    entity_type: string
    entity_id: string
    workflow_id: string
    current_state: string
    sla_metric: string — time_in_state, response_time, action_completion
    threshold: string — SLA threshold value
    elapsed: string — actual elapsed time
    severity: string — warning, critical
    escalation_level: int — 1-4
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [NBA Engine, Notification System, Admin Dashboard, Escalation Handler]
```

### 8.8 `incident.created`

```
event_type: incident.created
  producer: Workflow Engine / Security Engine
  trigger: An incident is reported (dispute, claim, fraud suspicion, system failure)
  payload: {
    incident_id: string
    incident_type: string — fraud, dispute, claim, system_failure, policy_violation
    entity_type: string
    entity_id: string
    severity: string — critical, high, normal, low
    reported_by: string — actor_id or system
    description: string
    related_event_ids: [string]
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Security Engine, Workflow Engine, Admin Dashboard, Notification System, Audit System]
```

---

## Section 9: Visit Events

### 9.1 `visit.scheduled`

```
event_type: visit.scheduled
  producer: Visit Engine / Relationship Engine
  trigger: Visit date and time confirmed by both parties
  payload: {
    visit_id: string
    property_id: string
    dossier_id: string
    demandeur_id: string
    holder_id: string
    scheduled_date: timestamp
    scheduled_duration_minutes: int
    visit_type: string — physical, virtual
    confirmation_status: string — confirmed, pending
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Notification System, NBA Engine, SLA Monitor, Reporting]
```

### 9.2 `visit.completed`

```
event_type: visit.completed
  producer: Visit Engine
  trigger: Visit actually takes place (both parties confirm or system detects)
  payload: {
    visit_id: string
    actual_date: timestamp
    duration_minutes: int
    satisfaction: { demandeur: int?, holder: int? } — satisfaction scores
    outcome: string — positive, negative, neutral
    feedback: string?
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [NBA Engine, Negotiation Engine, Continuous Learning, Reporting, Workflow Engine]
```

### 9.3 `visit.cancelled`

```
event_type: visit.cancelled
  producer: Visit Engine
  trigger: Visit cancelled by either party
  payload: {
    visit_id: string
    cancelled_by: string — actor_id
    reason: string?
    cancellation_type: string — by_demandeur, by_holder, mutual, system
    reschedule_proposed: boolean
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [NBA Engine, Relationship Engine, Reporting, Continuous Learning]
```

### 9.4 `visit.rescheduled`

```
event_type: visit.rescheduled
  producer: Visit Engine
  trigger: Visit date/time changed
  payload: {
    visit_id: string
    previous_date: timestamp
    new_date: timestamp
    reason: string?
    changed_by: string — actor_id
    reschedule_count: int
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Notification System, NBA Engine, SLA Monitor]
```

---

## Section 10: Payment Events

### 10.1 `payment.requested`

```
event_type: payment.requested
  producer: Payment Engine (Campay)
  trigger: Payment session initiated for a service or transaction
  payload: {
    payment_id: string
    amount: float
    currency: string — XAF
    payment_method: string — mobile_money, card, bank
    service_type: string — boost, premium, agent_subscription, transaction_fee
    payer_id: string
    description: string
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Payment Engine, Notification System, Reporting, Transaction Engine]
```

### 10.2 `payment.success`

```
event_type: payment.success
  producer: Payment Engine (Campay)
  trigger: Payment confirmed by payment provider
  payload: {
    payment_id: string
    amount: float
    currency: string
    provider_reference: string
    payment_method: string
    service_type: string
    processing_time_ms: int
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Service Activation Engine, Notification System, Reporting, Workflow Engine, Continuous Learning]
```

### 10.3 `payment.failed`

```
event_type: payment.failed
  producer: Payment Engine (Campay)
  trigger: Payment declined, cancelled, expired, or errored
  payload: {
    payment_id: string
    amount: float
    failure_reason: string — insufficient_funds, cancelled, expired, provider_error, timeout
    failure_stage: string — initiation, processing, confirmation
    retry_count: int
    retry_possible: boolean
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Notification System, NBA Engine, Reporting, Continuous Learning]
```

### 10.4 `payment.refunded`

```
event_type: payment.refunded
  producer: Payment Engine (Campay)
  trigger: Payment returned to payer (full or partial)
  payload: {
    payment_id: string
    refund_amount: float
    refund_reason: string
    refunded_by: string — actor_id or system
    provider_reference: string
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Notification System, Reporting, Audit System]
```

### 10.5 `payment.disputed`

```
event_type: payment.disputed
  producer: Payment Engine / Security Engine
  trigger: Payer contests a completed payment
  payload: {
    payment_id: string
    disputed_by: string — actor_id
    dispute_reason: string
    dispute_amount: float
    evidence: [string] — references to evidence documents
  }
  privacy_level: critical
  audit_visibility: restricted
  consumers: [Security Engine, Admin Dashboard, Audit System, Notification System]
```

---

## Section 11: Security and Access Events

### 11.1 `access.granted`

```
event_type: access.granted
  producer: Security Engine
  trigger: Permission or access right granted to an actor
  payload: {
    access_id: string
    granted_to: string — actor_id
    granted_by: string — actor_id or system
    resource_type: string — property, dossier, conversation, report
    resource_id: string
    permission_level: string — read, write, admin
    valid_until: timestamp?
    reason: string
  }
  privacy_level: critical
  audit_visibility: restricted
  consumers: [Audit System, Notification System, NBA Engine]
```

### 11.2 `access.denied`

```
event_type: access.denied
  producer: Security Engine
  trigger: Access attempt rejected by permission check
  payload: {
    actor_id: string
    resource_type: string
    resource_id: string
    requested_permission: string
    denial_reason: string — insufficient_role, no_consent, suspended, resource_restricted
    denial_context: string — what the actor was trying to do
  }
  privacy_level: critical
  audit_visibility: restricted
  consumers: [Audit System, Security Engine, NBA Engine]
```

### 11.3 `permission.changed`

```
event_type: permission.changed
  producer: Security Engine / Administration Engine
  trigger: Role, permission, or trust level modified for an actor
  payload: {
    actor_id: string
    change_type: string — role_promotion, role_demotion, permission_grant, permission_revoke, trust_level_change
    previous_value: string
    new_value: string
    changed_by: string — actor_id or system
    reason: string
  }
  privacy_level: critical
  audit_visibility: restricted
  consumers: [Audit System, Notification System, Workflow Engine, Reporting]
```

### 11.4 `fraud.detected`

```
event_type: fraud.detected
  producer: Security Engine
  trigger: Fraud detection system flags suspicious activity
  payload: {
    alert_id: string
    fraud_type: string — identity_theft, fake_document, payment_fraud, platform_abuse, suspicious_pattern
    entity_type: string
    entity_id: string
    confidence: float — detection confidence
    indicators: [string] — specific signals
    recommended_action: string — suspend, warn, investigate, block
    severity: string — critical, high, medium
  }
  privacy_level: critical
  audit_visibility: restricted
  consumers: [Security Engine, Admin Dashboard, Audit System, Notification System]
```

### 11.5 `handover.requested`

```
event_type: handover.requested
  producer: Decision Engine / Security Engine
  trigger: System determines it cannot handle the situation, escalates to human
  payload: {
    handover_id: string
    reason: string — unresolvable_conflict, low_confidence, fraud_suspicion, SLA_escalation
    entity_type: string
    entity_id: string
    context_summary: string
    suggested_role: string — assistant, vice_master, master
    priority: string
    related_decision_id: string?
    related_event_ids: [string]
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Admin Dashboard, Notification System, Workflow Engine, NBA Engine]
```

---

## Section 12: System and Admin Events

### 12.1 `feature.flag.changed`

```
event_type: feature.flag.changed
  producer: Administration Engine
  trigger: Feature flag toggled or configuration updated
  payload: {
    feature_name: string
    previous_state: any
    new_state: any
    changed_by: string — actor_id
    reason: string
    rollout_percentage: int? — for gradual rollouts
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [All Engines (config reload), Reporting, Audit System]
```

### 12.2 `role.changed`

```
event_type: role.changed
  producer: Administration Engine
  trigger: User role or hierarchy level changes
  payload: {
    user_id: string
    previous_role: string
    new_role: string
    change_type: string — promotion, demotion, assignment
    changed_by: string — actor_id
    reason: string
  }
  privacy_level: high
  audit_visibility: confidential
  consumers: [Security Engine, Workflow Engine, Notification System, Audit System]
```

### 12.3 `system.config.updated`

```
event_type: system.config.updated
  producer: Administration Engine
  trigger: System-wide configuration parameter changed
  payload: {
    config_key: string
    previous_value: any
    new_value: any
    changed_by: string — actor_id
    requires_restart: boolean
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [All Engines, Audit System]
```

### 12.4 `notification.sent`

```
event_type: notification.sent
  producer: Notification Engine
  trigger: Notification dispatched to a user
  payload: {
    notification_id: string
    recipient_id: string
    channel: string — whatsapp, telegram, email, in_app
    template: string
    notification_type: string — reminder, alert, promotion, system
    related_event_id: string?
    delivery_status: string — queued, sent, delivered
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [Reporting, Continuous Learning, SLA Monitor]
```

### 12.5 `notification.failed`

```
event_type: notification.failed
  producer: Notification Engine
  trigger: Notification delivery fails permanently
  payload: {
    notification_id: string
    recipient_id: string
    channel: string
    template: string
    failure_reason: string
    retry_count: int
    fallback_channel: string? — alternative channel used
  }
  privacy_level: medium
  audit_visibility: internal
  consumers: [NBA Engine, Continuous Learning, Admin Dashboard]
```

---

## Section 13: Decision and Learning Events

### 13.1 `decision.made`

```
event_type: decision.made
  producer: Decision Engine
  trigger: Decision cycle completes with NBA and action plan
  payload: {
    decision_id: string
    entity_type: string
    entity_id: string
    selected_rule: string
    confidence: float
    nba: { action: string, priority: int }
    rejected_rules: [{ rule_id: string, reason: string }]
    conflicts_resolved: [{ conflict_id: string, strategy: string }]
    fallback_used: boolean
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Domain Engines, NBA Engine, Audit System, Reporting, Continuous Learning]
```

### 13.2 `rule.conflict`

```
event_type: rule.conflict
  producer: Decision Engine / Rule Resolver
  trigger: Multiple rules match with conflicting outcomes
  payload: {
    conflict_id: string
    rules_involved: [string]
    conflict_type: string — overlap, contradiction, circular, redundancy
    resolution_strategy: string — priority, specificity, recency, escalation
    winner: string? — resolved winner if not escalated
    explanation: string
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [Decision Engine, Audit System, Admin Dashboard, Continuous Learning]
```

### 13.3 `confidence.recalibrated`

```
event_type: confidence.recalibrated
  producer: Continuous Learning Engine
  trigger: Model confidence updated based on outcome feedback
  payload: {
    model_name: string
    rule_id: string?
    previous_confidence: float
    new_confidence: float
    feedback_samples: int — number of feedback events used
    recalibration_reason: string
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [Knowledge Registry, Decision Engine, Reporting]
```

### 13.4 `learning.signal`

```
event_type: learning.signal
  producer: Continuous Learning Engine
  trigger: Outcome data packaged for model retraining
  payload: {
    signal_id: string
    source_event_ids: [string]
    entity_type: string
    prediction: { rule_id: string, confidence: float }
    outcome: { result: string, accuracy: float }
    features: object — anonymized feature vector
    signal_timestamp: timestamp
  }
  privacy_level: low
  audit_visibility: internal
  consumers: [Knowledge Registry, Reporting]
```

---

## Section 14: Geography and Language Events

### 14.1 `geo.resolved`

```
event_type: geo.resolved
  producer: Geography Engine
  trigger: Location string normalized to canonical geography
  payload: {
    input_text: string — original location text
    resolved: { city: string, neighborhood: string?, region: string, country: string }
    coordinates: { lat: float?, lng: float? }
    resolution_method: string — exact, fuzzy, fallback
    confidence: float
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Search Engine, Matching Engine, Qualification Engine, Reporting]
```

### 14.2 `geo.proximity.calculated`

```
event_type: geo.proximity.calculated
  producer: Geography Engine
  trigger: Distance/proximity score computed between two locations
  payload: {
    source_id: string
    target_id: string
    distance_km: float
    proximity_score: float — normalized [0-1]
    calculation_method: string — haversine, driving_distance, custom
  }
  privacy_level: low
  audit_visibility: public
  consumers: [Matching Engine, Reporting]
```

### 14.3 `language.detected`

```
event_type: language.detected
  producer: Language Engine
  trigger: Language identified from message text
  payload: {
    message_id: string
    detected_language: string — ISO 639-1
    confidence: float
    alternative_languages: [{ lang: string, confidence: float }]
    normalized_text: string? — cleaned text after normalization
  }
  privacy_level: public
  audit_visibility: public
  consumers: [Conversation Engine, Qualification Engine, Reporting]
```

---

## Section 15: Heritage Gold CRM-004 Alignment

Heritage Gold CRM-004 defines 11 canonical event types. These are fully represented in the catalog above, mapped as follows:

| CRM-004 Event | Catalog Event(s) | Notes |
|---------------|------------------|-------|
| `message.received` | 1.1 `message.received` | Direct mapping |
| `intent.detected` | 1.3 `intent.detected` | Direct mapping |
| `user.created` | 4.6 `user.created` | Direct mapping |
| `property.created` | 7.1 `property.created` | Direct mapping |
| `lead.created` | 4.1 `lead.created` | Direct mapping |
| `match.generated` | 3.6 `match.generated` | Direct mapping |
| `payment.success` | 10.2 `payment.success` | Direct mapping |
| `subscription.renewed` | 11.3 `permission.changed` (when type=subscription_renewed) | Mapped via permission change |
| `boost.applied` | 10.1 `payment.requested` / 10.2 `payment.success` (service_type=boost) | Mapped via payment flow |
| `access.granted` | 11.1 `access.granted` | Direct mapping |
| `user.state_changed` | 8.1 `state.transitioned` (entity_type=user) | Mapped via state transition |
| `feedback.submitted` | 9.2 `visit.completed` (satisfaction field) | Embedded in visit outcome |
| `fraud.detected` | 11.4 `fraud.detected` | Direct mapping |

All 13 CRM-004 events are covered. Additional events in this catalog extend the 11 canonical types with finer-grained business events.

---

## Section 16: Workflow Transition Event Coverage

Every transition defined in the 21 state machines (STATE_MACHINE_CATALOG.md) emits one or more events:

| Workflow | Transition Events | Audit Event(s) |
|----------|-----------------|----------------|
| Machine 01: Property Lifecycle | `state.transitioned` (13 states) | `property.published`, `property.available`, `property.matching`, `property.visit_scheduled`, `property.negotiation_open`, `property.reserved`, `property.in_transaction`, `property.unavailable`, `property.reactivated`, `property.archived` |
| Machine 02: Dossier Lifecycle | `state.transitioned` (14 states) | `dossier.qualifying`, `dossier.matching`, `dossier.presented`, `dossier.awaiting_decision`, `dossier.contacting_holder`, `dossier.awaiting_holder`, `dossier.contact_established`, `dossier.visit_scheduled`, `dossier.negotiating`, `dossier.agreement`, `dossier.in_transaction`, `dossier.closed`, `dossier.archived` |
| Machine 03: Matching | `state.transitioned` (10 states) | `matching.started`, `matching.completed`, `match.generated`, `dossier.rematching` |
| Machine 04: Contact | `state.transitioned` (6 states) | `consent.requested`, `consent.granted`, `consent.refused`, `relationship.created`, `dossier.rematching` |
| Machine 05: Visit | `state.transitioned` (9 states) | `visit.scheduled`, `visit.completed`, `visit.cancelled` |
| Machine 06: Negotiation | `state.transitioned` (8 states) | `negotiation.started`, `negotiation.accepted`, `negotiation.rejected`, `proposal.created` |
| Machine 07: Transaction | `state.transitioned` (10 states) | `payment.requested`, `payment.success`, `payment.failed`, `property.in_transaction`, `property.unavailable` |
| Machine 08: Payment | `state.transitioned` (18 states) | `payment.requested`, `payment.success`, `payment.failed`, `payment.refunded`, `payment.disputed` |
| Machine 09: Incidents | `state.transitioned` (8 states) | `incident.created` |
| Machine 10: Closure/Archive | `state.transitioned` (4 states) | `property.archived`, `dossier.archived` |
| Machine 11: Mediation | `state.transitioned` (8 states) | `incident.created` |
| Machine 12: User Identity | `state.transitioned` (7 states) | `user.created`, `role.changed`, `permission.changed` |
| Machine 13: Organization | `state.transitioned` (8 states) | `role.changed`, `permission.changed` |
| Machine 14: Agent Invitation | `state.transitioned` (7 states) | `user.created`, `role.changed` |
| Machine 15: Publication | `state.transitioned` (11 states) | `property.published` |
| Machine 16: Redirection | `state.transitioned` (12 states) | System events (no specific audit event) |
| Machine 17: Conversion | `state.transitioned` (12 states) | `payment.success` (terminal) |
| Machine 18: CRM Pipeline | `state.transitioned` (8 stages) | `lead.created`, `lead.scored`, `lead.classified`, `lead.routed` |
| Machine 19: Agent Opt-In | `state.transitioned` (4 states) | `consent.granted` |
| Machine 20: Identity Resolution | `state.transitioned` (5 states) | `identity.resolved` |
| Machine 21: Cross-cutting | Delegates to sub-workflows | Delegates to sub-workflow events |

---

## Section 17: Event Type Index

### By Category

| Category | Events |
|----------|--------|
| Conversation | `message.received`, `message.sent`, `intent.detected`, `fact.extracted`, `fact.confirmed`, `fact.superseded`, `question.selected` |
| Qualification | `qualification.updated`, `readiness.changed`, `field.completed` |
| Search & Matching | `search.started`, `search.completed`, `search.expanded`, `matching.started`, `matching.completed`, `match.generated`, `match.rejected`, `result.selected`, `score.calculated` |
| CRM & Lead | `lead.created`, `lead.scored`, `lead.classified`, `lead.routed`, `identity.resolved`, `user.created` |
| Relationship & Consent | `relationship.created`, `relationship.expired`, `relationship.revoked`, `consent.requested`, `consent.granted`, `consent.refused` |
| Proposal & Negotiation | `proposal.created`, `negotiation.started`, `negotiation.accepted`, `negotiation.rejected`, `price.updated` |
| Property | `property.created`, `property.updated`, `property.archived`, `property.published`, `property.unavailable` |
| Workflow & State | `state.transitioned`, `state_transition.failed`, `action.planned`, `action.executed`, `action.failed`, `follow_up.scheduled`, `SLA.breached`, `incident.created` |
| Visit | `visit.scheduled`, `visit.completed`, `visit.cancelled`, `visit.rescheduled` |
| Payment | `payment.requested`, `payment.success`, `payment.failed`, `payment.refunded`, `payment.disputed` |
| Security & Access | `access.granted`, `access.denied`, `permission.changed`, `fraud.detected`, `handover.requested` |
| System & Admin | `feature.flag.changed`, `role.changed`, `system.config.updated`, `notification.sent`, `notification.failed` |
| Decision & Learning | `decision.made`, `rule.conflict`, `confidence.recalibrated`, `learning.signal` |
| Geography & Language | `geo.resolved`, `geo.proximity.calculated`, `language.detected` |

### Alphabetical Index

| Event Type | Section | Producer |
|------------|---------|----------|
| `access.denied` | 11.2 | Security Engine |
| `access.granted` | 11.1 | Security Engine |
| `action.executed` | 8.4 | Action Executor / Domain Engine |
| `action.failed` | 8.5 | Action Executor / Domain Engine |
| `action.planned` | 8.3 | NBA Engine / Decision Engine |
| `confidence.recalibrated` | 13.3 | Continuous Learning Engine |
| `consent.granted` | 5.5 | Relationship Engine |
| `consent.refused` | 5.6 | Relationship Engine |
| `consent.requested` | 5.4 | Relationship Engine |
| `decision.made` | 13.1 | Decision Engine |
| `fact.confirmed` | 1.5 | Qualification Engine |
| `fact.extracted` | 1.4 | Conversation / Qualification Engine |
| `fact.superseded` | 1.6 | Qualification Engine |
| `feature.flag.changed` | 12.1 | Administration Engine |
| `field.completed` | 2.3 | Qualification Engine |
| `follow_up.scheduled` | 8.6 | Decision / NBA Engine |
| `fraud.detected` | 11.4 | Security Engine |
| `geo.proximity.calculated` | 14.2 | Geography Engine |
| `geo.resolved` | 14.1 | Geography Engine |
| `handover.requested` | 11.5 | Decision / Security Engine |
| `identity.resolved` | 4.5 | CRM / Identity Resolution Engine |
| `incident.created` | 8.8 | Workflow / Security Engine |
| `intent.detected` | 1.3 | Conversation / CRM Engine |
| `language.detected` | 14.3 | Language Engine |
| `lead.classified` | 4.3 | CRM Engine |
| `lead.created` | 4.1 | CRM Engine |
| `lead.routed` | 4.4 | CRM Engine |
| `lead.scored` | 4.2 | CRM Engine |
| `learning.signal` | 13.4 | Continuous Learning Engine |
| `match.generated` | 3.6 | Matching Engine |
| `match.rejected` | 3.7 | Matching / Relationship Engine |
| `matching.completed` | 3.5 | Matching Engine |
| `matching.started` | 3.4 | Matching Engine |
| `message.received` | 1.1 | Conversation Engine |
| `message.sent` | 1.2 | Conversation Engine |
| `negotiation.accepted` | 6.3 | Negotiation Engine |
| `negotiation.rejected` | 6.4 | Negotiation Engine |
| `negotiation.started` | 6.2 | Negotiation Engine |
| `notification.failed` | 12.5 | Notification Engine |
| `notification.sent` | 12.4 | Notification Engine |
| `payment.disputed` | 10.5 | Payment / Security Engine |
| `payment.failed` | 10.3 | Payment Engine |
| `payment.refunded` | 10.4 | Payment Engine |
| `payment.requested` | 10.1 | Payment Engine |
| `payment.success` | 10.2 | Payment Engine |
| `permission.changed` | 11.3 | Security / Administration Engine |
| `price.updated` | 6.5 | Negotiation Engine |
| `property.archived` | 7.3 | Workflow Engine |
| `property.created` | 7.1 | Administration / CRM Engine |
| `property.published` | 7.4 | Workflow Engine |
| `property.unavailable` | 7.5 | Workflow Engine |
| `property.updated` | 7.2 | Administration / Qualification Engine |
| `proposal.created` | 6.1 | Negotiation / Conversation Engine |
| `qualification.updated` | 2.1 | Qualification Engine |
| `question.selected` | 1.7 | Qualification / Conversation Engine |
| `readiness.changed` | 2.2 | Qualification Engine |
| `relationship.created` | 5.1 | Relationship Engine |
| `relationship.expired` | 5.2 | Relationship Engine |
| `relationship.revoked` | 5.3 | Relationship / Security Engine |
| `result.selected` | 3.8 | Search / Conversation Engine |
| `role.changed` | 12.2 | Administration Engine |
| `rule.conflict` | 13.2 | Decision Engine / Rule Resolver |
| `score.calculated` | 3.9 | Matching Engine |
| `search.completed` | 3.2 | Search Engine |
| `search.expanded` | 3.3 | Search Engine |
| `search.started` | 3.1 | Search Engine |
| `SLA.breached` | 8.7 | SLA Monitor |
| `state.transitioned` | 8.1 | Workflow Engine |
| `state_transition.failed` | 8.2 | Workflow Engine |
| `system.config.updated` | 12.3 | Administration Engine |
| `user.created` | 4.6 | Administration Engine |
| `visit.cancelled` | 9.3 | Visit Engine |
| `visit.completed` | 9.2 | Visit Engine |
| `visit.rescheduled` | 9.4 | Visit Engine |
| `visit.scheduled` | 9.1 | Visit Engine |

**Total: 66 event types**
