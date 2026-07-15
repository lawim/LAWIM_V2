# WORKFLOW EXTENSION MODEL

**Document ID:** LAWIM-H13-WORKFLOW-EXT-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §5 (Dossier/Project), §6 (Matching), §7 (Visit), §8 (Negotiation), §9 (Transaction), §10 (CRM), §14 (Document), §3 (Property)
**Source Crosswalks:** WORKFLOW_STATE_CROSSWALK.md, required_extensions.json (workflows, property_model, qualification_engine, agency_structure)

---

## Table of Contents

1. [Decision Framework](#1-decision-framework)
2. [Matching Lifecycle (WF-001)](#2-matching-lifecycle-wf-001)
3. [Mise en Relation / Contact Lifecycle (WF-002)](#3-mise-en-relation--contact-lifecycle-wf-002)
4. [Visit Lifecycle (WF-003)](#4-visit-lifecycle-wf-003)
5. [Transaction Lifecycle (WF-004)](#5-transaction-lifecycle-wf-004)
6. [Paid Services & Payment Lifecycle (WF-005)](#6-paid-services--payment-lifecycle-wf-005)
7. [Disputes, Claims & Incidents (WF-006)](#7-disputes-claims--incidents-wf-006)
8. [Mediation Workflow (WF-007)](#8-mediation-workflow-wf-007)
9. [CRM Pipeline (WF-008)](#9-crm-pipeline-wf-008)
10. [Publication SIE-Enriched (WF-009)](#10-publication-sie-enriched-wf-009)
11. [Redirection SIE-Enriched (WF-010)](#11-redirection-sie-enriched-wf-010)
12. [Conversion & Attribution (WF-011)](#12-conversion--attribution-wf-011)
13. [Agent Invitation Workflow (WF-012)](#13-agent-invitation-workflow-wf-012)
14. [Identity Resolution Workflow (WF-013)](#14-identity-resolution-workflow-wf-013)
15. [Main Cross-cutting Workflow (WF-014)](#15-main-cross-cutting-workflow-wf-014)
16. [Property Lifecycle](#16-property-lifecycle)
17. [Dossier Lifecycle](#17-dossier-lifecycle)
18. [Negotiation Workflow](#18-negotiation-workflow)
19. [Qualification Workflow](#19-qualification-workflow)
20. [Agent Onboarding](#20-agent-onboarding)
21. [Organization Lifecycle](#21-organization-lifecycle)
22. [Document Verification](#22-document-verification)
23. [Complete Extension Mapping Table](#23-complete-extension-mapping-table)

---

## 1. Decision Framework

Each workflow is assessed against five possible decisions:

| Decision | Meaning | Used When |
|----------|---------|-----------|
| **REUSE_CURRENT** | Keep existing V2 state machine as-is; no changes needed | V2 has equivalent with sufficient coverage |
| **EXTEND_CURRENT** | Extend existing V2 state machine with additional states/transitions | V2 has base model but missing states |
| **CREATE_NEW_GENERIC_STATE_MACHINE** | Build a reusable generic state machine engine configurable per workflow | No V2 equivalent; pattern is generic |
| **CREATE_SPECIALIZED_WORKFLOW** | Build a dedicated workflow entity with custom states | Workflow has unique domain-specific semantics |
| **HUMAN_DECISION_REQUIRED** | Cannot finalize without product/domain authority | Unresolved design question |

### 1.1 Workflow Decision Summary

| # | Workflow | States | Decision | Rationale |
|---|----------|--------|----------|-----------|
| 1 | Matching Lifecycle | 10 | CREATE_NEW_GENERIC_STATE_MACHINE | No matching engine exists in V2 |
| 2 | Mise en Relation / Contact | 6 | CREATE_SPECIALIZED_WORKFLOW | Double consent semantics unique to contact workflow |
| 3 | Visit Lifecycle | 9 | CREATE_SPECIALIZED_WORKFLOW | Visit has unique scheduling, reminder, absence semantics |
| 4 | Transaction Lifecycle | 10 | CREATE_SPECIALIZED_WORKFLOW | Transaction has legal/financial semantics, document requirements |
| 5 | Paid Services & Payment | 18 | CREATE_NEW_GENERIC_STATE_MACHINE | Service order + payment form generic pattern; 18 states total |
| 6 | Disputes, Claims & Incidents | 8 | CREATE_SPECIALIZED_WORKFLOW | Incident types, priority levels, investigation workflow unique |
| 7 | Mediation Workflow | 8 | CREATE_SPECIALIZED_WORKFLOW | Mediator role, session management, resolution types unique |
| 8 | CRM Pipeline | 8 | CREATE_NEW_GENERIC_STATE_MACHINE | CRM lead pipeline is generic pipe-and-filter pattern |
| 9 | Publication SIE-Enriched | 11 | CREATE_SPECIALIZED_WORKFLOW | SIE integration, campaign association, syndication unique |
| 10 | Redirection SIE-Enriched | 12 | CREATE_SPECIALIZED_WORKFLOW | Click tracking, bot/dedup detection, analytics unique |
| 11 | Conversion & Attribution | 12 | CREATE_SPECIALIZED_WORKFLOW | Attribution modeling, last-touch logic, commission calc unique |
| 12 | Agent Invitation | 7 | CREATE_SPECIALIZED_WORKFLOW | Secure link, document validation, admin approval unique |
| 13 | Identity Resolution | 5 | CREATE_SPECIALIZED_WORKFLOW | Signal matching, merge algorithm, human review unique |
| 14 | Main Cross-cutting | 9 | CREATE_NEW_GENERIC_STATE_MACHINE | Orchestrator delegates to sub-workflows; generic engine |
| 15 | Property Lifecycle | 13 | EXTEND_CURRENT | V2 has Property with 5 statuses; extend to 13 states |
| 16 | Dossier Lifecycle | 14 | EXTEND_CURRENT | V2 has Project with 5 statuses; extend to 14 states |
| 17 | Negotiation Workflow | 10 | ENRICH_CURRENT | V2 has conversation_domain negotiation stages; enrich |
| 18 | Qualification Workflow | 10 | CREATE_NEW_GENERIC_STATE_MACHINE | Progressive disclosure wizard; reusable pattern |
| 19 | Agent Onboarding | 6 | ENRICH_CURRENT | V2 has no onboarding; add to User model |
| 20 | Organization Lifecycle | 6 | EXTEND_CURRENT | V2 has Organization but no lifecycle states |
| 21 | Document Verification | 6 | CREATE_SPECIALIZED_WORKFLOW | Document upload, verification, expiry semantics unique |

---

## 2. Matching Lifecycle (WF-001)

**Extension ID:** EXT-WF-001
**Entity Type:** `Match`
**Decision:** CREATE_NEW_GENERIC_STATE_MACHINE
**Source:** WORKFLOW_03 (Gold), MATCHING_MODEL.md

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `matching_lifecycle` |
| entity_type | `Match` |
| initial_state | `created` |
| states | `created`, `scored`, `proposed`, `demandeur_review`, `holder_review`, `double_consent_obtained`, `mise_en_relation_established`, `active`, `expired`, `archived` |
| terminal_states | `mise_en_relation_established`, `expired`, `archived` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| created | scored | score_calculated | all_scoring_dimensions_complete | calculate_score, assign_compatibility_level |
| scored | proposed | auto_propose | score >= 60 AND rank_in_top_10 | create_proposal, notify_demandeur |
| scored | archived | low_score | score < 60 AND no_progressive_expansion | archive_match |
| proposed | demandeur_review | demandeur_notified | proposal_sent | start_decision_timer |
| demandeur_review | holder_review | demandeur_interested | consent_given | notify_holder |
| demandeur_review | rematched | demandeur_not_interested | refusal_received | exclude_property, recalculate |
| demandeur_review | expired | timer_expired | decision_deadline_passed | mark_expired, notify_both |
| holder_review | double_consent_obtained | holder_favorable | consent_given | record_consent |
| holder_review | rematched | holder_refused | refusal_received | exclude_property, recalculate |
| holder_review | expired | holder_silence | 72h_no_response | send_reminder_1 |
| double_consent_obtained | mise_en_relation_established | contact_created | double_consent_confirmed | create_contact, notify_both |
| mise_en_relation_established | active | visit_initiated | visit_scheduled | update_match_status |
| active | expired | match_inactivity | 30d_no_activity | recalculate_score |
| active | archived | match_completed | transaction_completed_or_cancelled | archive_match |
| expired | scored | recalculate | dossier_or_property_updated | recalculate_score |
| rematched | scored | new_match_cycle | rematch_count < max_rematches | increment_rematch_count, recalculate |

### Guards

| Guard | Condition | Scope |
|-------|-----------|-------|
| all_scoring_dimensions_complete | All 5 scoring dimensions have been computed | match |
| score >= 60 | Overall composite score meets minimum threshold | match |
| rank_in_top_10 | Match is among top 10 for this project | project |
| consent_given | User has explicitly consented | demandeur/holder |
| decision_deadline_passed | 72h elapsed without response | match |
| 72h_no_response | No response after 72h with reminders | match |
| double_consent_confirmed | Both demandeur and holder have consented | match |
| match_inactivity | 30 days without activity on match | match |
| visit_initiated | Visit has been scheduled for this match | match |

### Triggers

| Trigger | Source | Event |
|---------|--------|-------|
| score_calculated | System (matching engine) | match.score_calculated |
| auto_propose | System (matching engine) | match.proposed |
| demandeur_notified | System (notification) | match.notified |
| demandeur_interested | Demandeur action | match.demandeur_accepted |
| demandeur_not_interested | Demandeur action | match.demandeur_rejected |
| holder_favorable | Holder action | match.holder_accepted |
| holder_refused | Holder action | match.holder_rejected |
| timer_expired | System (cron) | match.decision_expired |
| holder_silence | System (cron) | match.holder_silence_detected |
| contact_created | System (contact workflow) | match.contact_established |
| match_inactivity | System (cron) | match.inactivity_detected |
| recalculate | System (event) | match.recalculate_requested |
| new_match_cycle | System (rematching) | match.rematching_initiated |

### Actions

| Action | Description | Async |
|--------|-------------|-------|
| calculate_score | Compute composite score from 5 dimensions | Yes |
| assign_compatibility_level | Map score to Excellent/Good/Average/Low | No |
| create_proposal | Generate match proposal with score breakdown | No |
| notify_demandeur | Send match proposal to demandeur | Yes |
| notify_holder | Inform holder of demandeur interest | Yes |
| start_decision_timer | Set 72h deadline for decision | Yes |
| record_consent | Log consent timestamp and actor | No |
| send_reminder | Send silence reminder (1/2/3/last) | Yes |
| exclude_property | Remove property from current match pool | No |
| increment_rematch_count | Track rematching cycle count | No |
| archive_match | Move match to archived state | No |
| recalculate_score | Recompute all scoring dimensions | Yes |
| create_contact | Create Contact entity for established connection | Yes |

### SLA

| State | Max Duration | Escalation |
|-------|-------------|------------|
| demandeur_review | 72h | Reminder at 24h, 48h, auto-expire |
| holder_review | 72h | Reminder at 24h, 48h, 72h → property "to confirm" |
| active | 30d inactivity | Recalculate score, notify both parties |
| proposed to demandeur_review | 24h | Reminder if no action within 24h |

### NBA Rules

| State | NBA |
|-------|-----|
| created | "Awaiting scoring computation" |
| scored | "Review match proposal" (if score >= 60) or "Expand search criteria" (if score < 60) |
| proposed | "Respond to match proposal" (demandeur), "Awaiting demandeur response" |
| demandeur_review | "Holder has been contacted — awaiting response" (if holder_contacted) |
| holder_review | "Review holder response" (if holder responds) |
| double_consent_obtained | "Establish contact between parties" |
| mise_en_relation_established | "Schedule a visit" |
| active | "Schedule follow-up" (if inactive > 7d) |
| expired | "Request rematch" or "Update dossier criteria" |
| archived | Match is closed |

### Events

| Event | Payload |
|-------|---------|
| match.created | {project_id, property_id, initial_score} |
| match.score_calculated | {match_id, score_dimensions[], composite_score, compatibility_level} |
| match.proposed | {match_id, rank, score, proposal_method} |
| match.demandeur_accepted | {match_id, demandeur_id, decision_timestamp} |
| match.demandeur_rejected | {match_id, demandeur_id, reason?} |
| match.holder_accepted | {match_id, holder_id, decision_timestamp} |
| match.holder_rejected | {match_id, holder_id, reason?} |
| match.expired | {match_id, expiry_reason} |
| match.rematched | {match_id, old_property_id, new_property_id, rematch_count} |
| match.archived | {match_id, archive_reason} |
| match.contact_established | {match_id, contact_id} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Scoring computation fails | Retry (max 3), log error, transition to failed state |
| Notification delivery fails | Queue retry (max 5), fallback to in-app notification |
| Reminder system fails | Cron job health check, manual trigger available |
| Database transaction fails on consent | Atomic transaction with rollback, retry on conflict |
| Match proposal expires | Auto-transition to expired, notify demandeur |

---

## 3. Mise en Relation / Contact Lifecycle (WF-002)

**Extension ID:** EXT-WF-002
**Entity Type:** `Contact`
**Decision:** CREATE_SPECIALIZED_WORKFLOW
**Source:** WORKFLOW_04 (Gold)

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `mise_en_relation` |
| entity_type | `Contact` |
| initial_state | `created` |
| states | `created`, `demandeur_interested`, `holder_contacted`, `holder_favorable`, `consent_obtained`, `established`, `refused`, `expired` |
| terminal_states | `established`, `refused`, `expired` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| created | demandeur_interested | demandeur_consents | match_proposed | record_demandeur_consent, notify_holder |
| created | expired | no_demandeur_action | 7d_no_response | cleanup_contact |
| demandeur_interested | holder_contacted | holder_notified | demandeur_consent_confirmed | send_holder_notification, start_holder_timer |
| holder_contacted | holder_favorable | holder_consents | holder_consent_given | record_holder_consent |
| holder_contacted | refused | holder_refuses | holder_rejects | notify_demandeur, offer_rematch |
| holder_contacted | expired | holder_silence | 72h_no_response | send_reminder_1_2_3, escalate |
| holder_favorable | consent_obtained | double_consent_verified | both_consented | verify_consent_pair |
| consent_obtained | established | contact_activated | consent_valid | activate_contact, reveal_coordinates (if paid) |
| established | archived | contact_concluded | transaction_or_closure | archive_contact |
| refused | rematched | demandeur_requests_rematch | rematch_available | trigger_rematching |

### Guards

| Guard | Condition |
|-------|-----------|
| match_proposed | Match exists and has been proposed to demandeur |
| 7d_no_response | Demandeur did not respond to match within 7 days |
| demandeur_consent_confirmed | Demandeur consent has been recorded |
| holder_consent_given | Holder has explicitly consented to contact |
| holder_rejects | Holder explicitly refuses contact |
| 72h_no_response | No response from holder after 72h (with reminders sent) |
| both_consented | Both demandeur and holder have given consent |
| consent_valid | No consent withdrawal, consent within validity period |
| rematch_available | Rematch count < max_rematches AND alternative property exists |

### Triggers

| Trigger | Source |
|---------|--------|
| demandeur_consents | Demandeur action (UI/chat) |
| no_demandeur_action | System (cron) |
| holder_notified | System (notification sent) |
| holder_consents | Holder action |
| holder_refuses | Holder action |
| holder_silence | System (cron, after 72h) |
| double_consent_verified | System (consent pair validation) |
| contact_activated | System (activation check) |
| contact_concluded | System (event from transaction/workflow) |
| demandeur_requests_rematch | Demandeur action |

### Actions

| Action | Description |
|--------|-------------|
| record_demandeur_consent | Log demandeur consent with timestamp |
| notify_holder | Send notification to holder about demandeur interest |
| send_holder_notification | Send structured contact request to holder |
| start_holder_timer | Initialize 72h holder response timer |
| record_holder_consent | Log holder consent with timestamp |
| notify_demandeur | Inform demandeur of holder refusal |
| send_reminder | Send silence reminder (1 at 24h, 2 at 48h, 3 at 72h) |
| escalate | Flag property as "to confirm", offer rematch |
| verify_consent_pair | Confirm both consents are valid and matching |
| activate_contact | Enable communication channel between parties |
| reveal_coordinates | Reveal contact details (if lead purchase completed) |
| archive_contact | Close contact record |
| trigger_rematching | Initiate rematching workflow |

### SLA

| State | Max Duration | Escalation |
|-------|-------------|------------|
| created | 7d | Auto-expire if demandeur does not consent |
| demandeur_interested | 24h (notification) | Reminder if holder not notified within 1h |
| holder_contacted | 72h | Reminder 1 (24h), Reminder 2 (48h), Reminder 3 (72h), Last Reminder, then expire |
| holder_favorable | 24h (activation) | Auto-activate after 24h if no issues |
| established | 90d inactivity | Re-assess match quality |

### NBA Rules

| State | NBA |
|-------|-----|
| created | "Review match and express interest" |
| demandeur_interested | "Awaiting holder response" |
| holder_contacted | "Respond to contact request" (holder), "Holder has been notified" (demandeur) |
| holder_favorable | "Complete contact establishment" |
| consent_obtained | "Contact is now active — start conversation" |
| established | "Schedule a visit" or "Send a message" |
| refused | "View alternative matches" |
| expired | "Rematch with new property" |

### Events

| Event | Payload |
|-------|---------|
| contact.created | {match_id, demandeur_id, holder_id, property_id} |
| contact.demandeur_consented | {contact_id, demandeur_id, timestamp} |
| contact.holder_notified | {contact_id, notification_channel, timestamp} |
| contact.holder_consented | {contact_id, holder_id, timestamp} |
| contact.holder_refused | {contact_id, holder_id, reason?} |
| contact.holder_silence_reminder | {contact_id, reminder_number, timestamp} |
| contact.consent_obtained | {contact_id, demandeur_consent_at, holder_consent_at} |
| contact.established | {contact_id, activated_at, channel} |
| contact.refused | {contact_id, refused_by, reason} |
| contact.expired | {contact_id, expiry_reason} |
| contact.archived | {contact_id, archive_reason} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Notification fails for holder | Retry (max 5), escalate to agent, log |
| Holder silence with no valid contact | After reminders, auto-expire, offer rematch |
| Consent withdrawal | If either party withdraws before establishment, cancel contact |
| Duplicate contact creation | Check existing active contact before creation |

---

## 4. Visit Lifecycle (WF-003)

**Extension ID:** EXT-WF-003
**Entity Type:** `Visit`
**Decision:** CREATE_SPECIALIZED_WORKFLOW
**Source:** WORKFLOW_05 (Gold), UDM §8

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `visit_lifecycle` |
| entity_type | `Visit` |
| initial_state | `requested` |
| states | `requested`, `awaiting_confirmation`, `confirmed`, `completed`, `rescheduled`, `cancelled`, `refused`, `absent_demandeur`, `absent_holder` |
| terminal_states | `completed`, `cancelled`, `refused` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| requested | awaiting_confirmation | holder_notified | visit_proposed | notify_holder, start_confirmation_timer |
| requested | cancelled | demandeur_cancels | cancellation_allowed | process_cancellation, notify_holder |
| awaiting_confirmation | confirmed | holder_confirms | confirmation_within_deadline | schedule_reminders |
| awaiting_confirmation | refused | holder_refuses | holder_declines | notify_demandeur, offer_alternative |
| awaiting_confirmation | cancelled | demandeur_cancels | cancellation_allowed | process_cancellation |
| awaiting_confirmation | expired | confirmation_deadline_passed | no_response_within_deadline | notify_both, offer_reschedule |
| confirmed | completed | visit_occurred | visit_confirmed | record_completion, send_satisfaction_survey |
| confirmed | rescheduled | reschedule_requested | both_agree | update_datetime, reassign_reminders |
| confirmed | cancelled | either_cancels | cancellation_policy_ok | process_cancellation, notify_other |
| confirmed | absent_demandeur | demandeur_no_show | 30min_post_scheduled | log_absence, notify_holder, offer_reschedule |
| confirmed | absent_holder | holder_no_show | 30min_post_scheduled | log_absence, notify_demandeur, offer_reschedule_or_rematch |
| completed | satisfaction_recorded | survey_submitted | rating_provided | update_satisfaction, trigger_nba |

### Guards

| Guard | Condition |
|-------|-----------|
| visit_proposed | Visit request has valid datetime, property, and participants |
| cancellation_allowed | Cancellation policy permits (not within 2h of visit) |
| confirmation_within_deadline | Holder responds before confirmation deadline |
| holder_declines | Holder explicitly refuses the visit |
| no_response_within_deadline | Confirmation deadline passed without response |
| visit_confirmed | Visit occurred (confirmed by either party or agent) |
| both_agree | Both demandeur and holder agree to new datetime |
| cancellation_policy_ok | Within policy bounds, no excessive cancellations |
| 30min_post_scheduled | 30 minutes after scheduled start time |
| rating_provided | Satisfaction rating (1-5) received from at least one party |

### Triggers

| Trigger | Source |
|---------|--------|
| holder_notified | System (notification) |
| demandeur_cancels | Demandeur action |
| holder_confirms | Holder action |
| holder_refuses | Holder action |
| confirmation_deadline_passed | System (cron) |
| visit_occurred | System (auto-detection) or agent confirmation |
| reschedule_requested | Either party action |
| either_cancels | Either party action |
| demandeur_no_show | System (cron, 30min after) |
| holder_no_show | System (cron, 30min after) |
| survey_submitted | User action (satisfaction form) |

### Actions

| Action | Description |
|--------|-------------|
| notify_holder | Send visit request notification to holder |
| start_confirmation_timer | Set confirmation deadline (24h before visit) |
| process_cancellation | Log cancellation, apply cancellation policy rules |
| schedule_reminders | Schedule 24h and 2h reminders |
| record_completion | Log visit completion timestamp and notes |
| send_satisfaction_survey | Send post-visit satisfaction request |
| update_datetime | Update scheduled_at with new datetime |
| reassign_reminders | Cancel old reminders, schedule new ones |
| log_absence | Record absence type and timestamp |
| offer_reschedule | Propose alternative visit time |
| offer_reschedule_or_rematch | Propose new visit or new property match |
| update_satisfaction | Store satisfaction rating |
| trigger_nba | Compute next best action based on satisfaction |

### SLA

| State | Max Duration | Escalation |
|-------|-------------|------------|
| awaiting_confirmation | Until 24h before visit | Reminder to holder at 48h before if not confirmed |
| confirmed | Until scheduled datetime | 24h reminder, 2h reminder |
| absent (either) | 30min after scheduled | Immediate notification to other party |
| rescheduled | New confirmation cycle | Same as awaiting_confirmation |
| satisfaction collection | 1h post-visit | Reminder at 1h, 24h, auto-close |

### NBA Rules

| State | NBA |
|-------|-----|
| requested | "Holder has been notified — awaiting confirmation" |
| awaiting_confirmation | "Confirm or reschedule the visit" (holder) |
| confirmed | "Visit scheduled — prepare documents" (both) |
| completed (satisfied) | "Proceed to negotiation" |
| completed (neutral) | "Schedule a second visit" |
| completed (unsatisfied) | "View alternative properties" |
| absent_demandeur | "Demandeur missed visit — offer reschedule" |
| absent_holder | "Holder missed visit — offer rematch" |
| cancelled | "View other available properties" |

### Events

| Event | Payload |
|-------|---------|
| visit.requested | {project_id, property_id, demandeur_id, scheduled_at} |
| visit.confirmed | {visit_id, holder_id, confirmed_at} |
| visit.rescheduled | {visit_id, old_datetime, new_datetime, requested_by} |
| visit.cancelled | {visit_id, cancelled_by, reason} |
| visit.refused | {visit_id, refused_by, reason?} |
| visit.completed | {visit_id, completed_at, notes?} |
| visit.absence_reported | {visit_id, absent_party, absence_type} |
| visit.satisfaction_recorded | {visit_id, party, rating, feedback?} |
| visit.reminder_sent | {visit_id, reminder_type (24h|2h), channel} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Double booking (same property, overlapping time) | Reject second visit, notify requester |
| Cancellation within 2h | Flag as last-minute cancellation, count toward trust penalty |
| 3rd demandeur no-show | Reduce trust level, flag account |
| 3rd holder no-show | Flag property, reduce holder reliability score |
| Bad weather / force majeure | Allow cancellation without penalty |

---

## 5. Paid Services & Payment Lifecycle (WF-005)

**Extension ID:** EXT-WF-005
**Entity Type:** `ServiceOrder` + `Payment`
**Decision:** CREATE_NEW_GENERIC_STATE_MACHINE
**Source:** WORKFLOW_08 (Gold), UDM §4

### State Machine — ServiceOrder (8 states)

| Field | Value |
|-------|-------|
| workflow_id | `paid_services` |
| entity_type | `ServiceOrder` |
| initial_state | `creation` |
| states | `creation`, `proposition`, `acceptation`, `paiement`, `activation`, `utilisation`, `expiration`, `archivage` |
| terminal_states | `archivage`, `expiration` |

### State Machine — Payment Sub-states (10 states)

| Field | Value |
|-------|-------|
| workflow_id | `payment_lifecycle` |
| entity_type | `Payment` |
| initial_state | `created` |
| states | `created`, `initiated`, `pending`, `confirmed`, `failed`, `cancelled`, `expired`, `refunded`, `reconciled`, `disputed` |
| terminal_states | `confirmed`, `failed`, `cancelled`, `expired`, `refunded`, `reconciled` |

### Transitions — ServiceOrder

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| creation | proposition | service_selected | service_valid | create_proposition, notify_buyer |
| proposition | acceptation | buyer_accepts | acceptance_valid | record_acceptance, initiate_payment |
| proposition | archivage | buyer_declines | decline_reason | log_decline, archive |
| proposition | expiration | offer_expires | 30d_no_action | auto_expire |
| acceptation | paiement | payment_initiated | payment_created | link_payment, wait_for_confirmation |
| paiement | activation | payment_confirmed | payment_successful | activate_service, notify_buyer |
| paiement | archivage | payment_failed | payment_failed_max_retries | log_failure, notify_buyer |
| activation | utilisation | service_accessed | service_active | track_usage |
| utilisation | expiration | service_expires | duration_exceeded | deactivate, notify |
| utilisation | archivage | service_completed | usage_complete | finalize, archive |
| expiration | archivage | cleanup | expired | archive_record |

### Transitions — Payment

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| created | initiated | payment_started | provider_available | send_to_provider |
| initiated | pending | provider_acknowledged | ack_received | start_confirmation_timer |
| pending | confirmed | provider_confirms | confirmation_received | record_confirmation, activate_order |
| pending | failed | provider_rejects | failure_reason | log_failure, notify_buyer |
| pending | expired | confirmation_timeout | 30min_no_response | mark_expired, retry |
| initiated | cancelled | user_cancels | cancellation_allowed | process_cancellation |
| confirmed | refunded | refund_requested | refund_policy_ok | process_refund |
| confirmed | reconciled | reconciliation_run | end_of_day | mark_reconciled |
| confirmed | disputed | dispute_filed | dispute_valid | flag_dispute, notify_admin |
| disputed | refunded | dispute_resolved_refund | admin_decision_refund | process_refund |
| disputed | confirmed | dispute_resolved_keep | admin_decision_keep | resolve_dispute, notify |
| failed | initiated | retry | retry_count < max | reinitiate_payment |
| expired | initiated | retry | retry_allowed | reinitiate_payment |

### Guards

| Guard | Condition |
|-------|-----------|
| service_valid | Service exists, is_active, and available |
| acceptance_valid | Buyer has agreed to price and terms |
| payment_created | Payment record has been created |
| payment_successful | Payment provider confirmed success |
| provider_available | Payment provider (Campay) is reachable |
| confirmation_received | Valid confirmation from payment provider |
| failure_reason | Provider returned a failure code |
| retry_allowed | Retry count < max_retries AND time since last try > 5min |

### Triggers

| Trigger | Source |
|---------|--------|
| service_selected | Buyer action |
| buyer_accepts | Buyer action |
| buyer_declines | Buyer action |
| offer_expires | System (cron, 30d) |
| payment_started | System (after acceptance) |
| provider_acknowledged | Payment provider callback |
| provider_confirms | Payment provider callback |
| provider_rejects | Payment provider callback |
| confirmation_timeout | System (cron, 30min) |
| user_cancels | User action |

### Actions

| Action | Description |
|--------|-------------|
| create_proposition | Generate service order with price quote |
| notify_buyer | Send order confirmation/status to buyer |
| record_acceptance | Log acceptance timestamp and terms |
| initiate_payment | Create payment record, send to provider |
| link_payment | Associate payment with service order |
| activate_service | Enable service features for user |
| deactivate | Disable service features on expiry |
| track_usage | Log service usage metrics |
| send_to_provider | Submit payment request to Campay |
| record_confirmation | Store provider confirmation and reference |
| process_refund | Initiate refund through payment provider |

### SLA

| State | Max Duration | Escalation |
|-------|-------------|------------|
| pending (payment) | 30min | Auto-check every 5min, escalate on timeout |
| proposition | 30d | Auto-expire if no buyer action |
| utilisation | Per service duration | Notify 7d before expiration |

### NBA Rules

| State | NBA |
|-------|-----|
| creation | "Select service to purchase" |
| proposition | "Review and accept service offer" |
| acceptation | "Complete payment" |
| paiement | "Awaiting payment confirmation" |
| activation | "Service is active — start using" |
| utilisation | "Service in use" or "Service expiring soon" (7d before) |
| expiration | "Service expired — repurchase or upgrade" |

### Events

| Event | Payload |
|-------|---------|
| service_order.created | {order_id, service_id, buyer_id, price} |
| service_order.proposed | {order_id, proposition_details, expires_at} |
| service_order.accepted | {order_id, accepted_at} |
| service_order.activated | {order_id, activated_at, duration_days} |
| service_order.expired | {order_id, expired_at} |
| service_order.archived | {order_id, archive_reason} |
| payment.created | {payment_id, order_id, amount, provider} |
| payment.initiated | {payment_id, provider_reference} |
| payment.confirmed | {payment_id, confirmed_at, provider_ref} |
| payment.failed | {payment_id, failure_reason, failure_code} |
| payment.refunded | {payment_id, refunded_at, refund_amount} |
| payment.disputed | {payment_id, dispute_reason, disputed_at} |
| payment.reconciled | {payment_id, reconciled_at} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Payment provider timeout | Retry (max 3, 5min interval), then mark expired |
| Insufficient funds | Notify buyer, offer alternative payment |
| Network failure (Campay) | Queue, retry with exponential backoff |
| Duplicate payment callback | Idempotency key, reconcile duplicate |
| Refund failure | Manual intervention, admin notified |

---

## 6. Disputes, Claims & Incidents (WF-006)

**Extension ID:** EXT-WF-006
**Entity Type:** `Incident`
**Decision:** CREATE_SPECIALIZED_WORKFLOW
**Source:** WORKFLOW_09 (Gold)

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `disputes_claims_incidents` |
| entity_type | `Incident` |
| initial_state | `reported` |
| states | `reported`, `qualified`, `investigation`, `analysis`, `decision`, `resolution`, `closed`, `reopened`, `escalated` |
| terminal_states | `closed` |

### Incident Types

| Type | Description | Priority Default |
|------|-------------|-----------------|
| payment_dispute | Payment amount or processing dispute | P1 |
| property_misrepresentation | Listing does not match reality | P1 |
| fraud_suspicion | Suspected fraudulent activity | P0 |
| contract_breach | Breach of agreement terms | P2 |
| no_show | Repeated no-show behavior | P3 |
| harassment | Abusive communication | P1 |
| data_privacy | GDPR or data privacy complaint | P1 |
| technical_issue | Platform bug or error | P3 |
| agent_misconduct | Agent professional conduct issue | P2 |
| quality_complaint | Service quality complaint | P2 |
| third_party | External party (notaire, bank) issue | P2 |
| other | Unclassified | P3 |

### Priority Levels

| Priority | Response SLA | Resolution SLA |
|----------|-------------|----------------|
| P0 (Critical) | < 1h | < 24h |
| P1 (High) | < 4h | < 72h |
| P2 (Medium) | < 24h | < 7d |
| P3 (Low) | < 72h | < 30d |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| reported | qualified | incident_triaged | triage_complete | assign_priority, assign_handler |
| reported | closed | invalid_report | no_case_to_answer | close_with_reason |
| qualified | investigation | investigation_started | handler_assigned | gather_evidence, notify_parties |
| qualified | closed | resolved_at_qualification | quick_resolution | log_outcome, close |
| investigation | analysis | evidence_collected | sufficient_evidence | analyze_findings |
| investigation | escalated | needs_higher_authority | beyond_handler_scope | assign_escalation_handler |
| analysis | decision | analysis_complete | findings_reviewed | propose_decision |
| analysis | escalated | needs_legal | legal_implications | escalate_to_legal |
| decision | resolution | decision_approved | decision_valid | implement_decision, notify_parties |
| decision | escalated | decision_disputed | party_appeals | escalate_for_review |
| resolution | closed | resolution_complete | actions_executed | finalize, archive |
| closed | reopened | new_evidence | appeal_within_period | reopen_investigation |
| escalated | analysis | escalation_reviewed | higher_authority_acted | continue_analysis |

### Guards

| Guard | Condition |
|-------|-----------|
| triage_complete | Incident type, priority, and initial facts assessed |
| no_case_to_answer | Report lacks substance or is duplicate |
| handler_assigned | Qualified investigator assigned |
| sufficient_evidence | Minimum evidence threshold met |
| beyond_handler_scope | Incident requires higher authority or specialized skills |
| findings_reviewed | Analysis reviewed by qualified party |
| legal_implications | Incident has legal or regulatory implications |
| decision_valid | Decision is within policy and authority limits |
| party_appeals | Either party formally appeals the decision |
| actions_executed | Resolution actions have been completed and verified |
| appeal_within_period | Appeal filed within 30d of closure |

### Triggers

| Trigger | Source |
|---------|--------|
| incident_triaged | System (auto-triage) or operator |
| investigation_started | Handler starts investigation |
| evidence_collected | Evidence log complete |
| needs_higher_authority | Handler requests escalation |
| analysis_complete | Analysis report submitted |
| needs_legal | Legal implications detected |
| decision_approved | Authorizer approves decision |
| decision_disputed | Party files appeal |
| resolution_complete | Resolution actions confirmed |
| new_evidence | New information submitted |

### Actions

| Action | Description |
|--------|-------------|
| assign_priority | Set incident priority (P0-P3) |
| assign_handler | Route to qualified incident handler |
| gather_evidence | Collect relevant data, messages, documents |
| notify_parties | Inform involved parties of investigation |
| analyze_findings | Review evidence and prepare analysis |
| propose_decision | Draft decision recommendation |
| implement_decision | Execute decision actions (refund, ban, etc.) |
| close_with_reason | Close with explanation |
| escalate_to_legal | Route to legal team |
| reopen_investigation | Resume investigation with new evidence |

### NBA Rules

| State | NBA |
|-------|-----|
| reported | "Triage and qualify the incident" |
| qualified | "Assign handler and begin investigation" |
| investigation | "Collect evidence and interview parties" |
| analysis | "Prepare findings and decision recommendation" |
| decision | "Approve or modify proposed decision" |
| resolution | "Execute and verify resolution actions" |
| closed | "Incident resolved — archive" |
| reopened | "Review new evidence and continue" |

### Events

| Event | Payload |
|-------|---------|
| incident.reported | {incident_id, reporter_id, type, description, related_entity} |
| incident.qualified | {incident_id, priority, incident_type, handler_id} |
| incident.investigation_started | {incident_id, started_at, handler_id} |
| incident.evidence_collected | {incident_id, evidence_items[], collected_by} |
| incident.analysis_complete | {incident_id, findings_summary, recommendation} |
| incident.decision_made | {incident_id, decision, decided_by, reason} |
| incident.resolved | {incident_id, resolution_actions[], resolved_at} |
| incident.closed | {incident_id, closed_at, closed_by} |
| incident.reopened | {incident_id, reason, reopened_by} |
| incident.escalated | {incident_id, escalated_to, reason, escalated_by} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Handler does not respond | Reassign after 24h (P0-P1) or 72h (P2-P3) |
| Insufficient evidence for decision | Mark as inconclusive, notify parties |
| SLA breach on response | Escalate to next tier handler |
| Conflict of interest (handler) | Reassign to alternate handler |

---

## 7. Mediation Workflow (WF-007)

**Extension ID:** EXT-WF-007
**Entity Type:** `Mediation`
**Decision:** CREATE_SPECIALIZED_WORKFLOW
**Source:** WORKFLOW_11 (Gold)

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `mediation_workflow` |
| entity_type | `Mediation` |
| initial_state | `filed` |
| states | `filed`, `assigned`, `preliminary_review`, `mediation_session`, `offer_proposed`, `accepted`, `rejected`, `closed`, `escalated` |
| terminal_states | `accepted`, `rejected`, `closed`, `escalated` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| filed | assigned | mediator_assigned | mediator_available | notify_parties, schedule_review |
| filed | closed | withdrawn | party_withdraws | close_mediation |
| assigned | preliminary_review | review_started | both_parties_agree | gather_documents, define_issues |
| preliminary_review | mediation_session | session_scheduled | issues_defined | schedule_session, send_invites |
| preliminary_review | escalated | mediation_inappropriate | out_of_scope | escalate_to_legal |
| preliminary_review | closed | parties_reach_agreement | preliminary_agreement | document_agreement, close |
| mediation_session | offer_proposed | mediator_proposes | session_complete | draft_offer, present_to_parties |
| mediation_session | escalated | session_fails | deadlock | escalate_to_arbitration |
| offer_proposed | accepted | both_accept | acceptance_deadline_met | document_agreement, close |
| offer_proposed | rejected | either_rejects | rejection_received | log_rejection, offer_revision |
| offer_proposed | escalated | no_decision | deadline_passed | escalate |
| accepted | closed | agreement_finalized | terms_accepted | finalize, archive |

### Guards

| Guard | Condition |
|-------|-----------|
| mediator_available | Qualified mediator assigned |
| party_withdraws | Either party formally withdraws |
| both_parties_agree | Both consent to mediation process |
| issues_defined | Key issues and positions documented |
| out_of_scope | Issue requires legal or regulatory intervention |
| preliminary_agreement | Parties agree before formal session |
| session_complete | Mediation session concluded |
| deadlock | Parties cannot reach any agreement |
| acceptance_deadline_met | Both parties accept within deadline (7d) |
| deadline_passed | No response within 7d of offer proposal |

### Triggers

| Trigger | Source |
|---------|--------|
| mediator_assigned | Admin action |
| party_withdraws | Party action |
| review_started | Mediator action |
| both_parties_agree | Consent from both |
| session_scheduled | Mediator action |
| mediation_inappropriate | Mediator determination |
| parties_reach_agreement | Both parties agree pre-session |
| mediator_proposes | Mediator action |
| session_fails | Mediator determination |
| both_accept | Both parties accept |
| either_rejects | Either party rejects |

### Events

| Event | Payload |
|-------|---------|
| mediation.filed | {mediation_id, incident_id, filer_id, respondent_id, issue_summary} |
| mediation.assigned | {mediation_id, mediator_id, assigned_at} |
| mediation.review_started | {mediation_id, review_started_at} |
| mediation.session_scheduled | {mediation_id, session_datetime, format (virtual/in-person)} |
| mediation.offer_proposed | {mediation_id, offer_summary, proposed_by, deadline} |
| mediation.accepted | {mediation_id, accepted_at, accepted_by_both} |
| mediation.rejected | {mediation_id, rejected_by, reason} |
| mediation.escalated | {mediation_id, escalated_to, reason} |
| mediation.closed | {mediation_id, outcome, closed_at} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Party does not attend session | Reschedule once, then proceed in absentia |
| Mediator unavailable | Reassign within 24h |
| Agreement not honored | Refer to legal escalation |
| Conflict of interest | Reassign mediator immediately |

---

## 8. CRM Pipeline (WF-008)

**Extension ID:** EXT-WF-008
**Entity Type:** `Lead`
**Decision:** CREATE_NEW_GENERIC_STATE_MACHINE
**Source:** WORKFLOW_18 (Gold), UDM §11

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `crm_pipeline` |
| entity_type | `Lead` |
| initial_state | `incoming` |
| states | `incoming`, `normalized`, `extracted`, `intent_detected`, `enriched`, `scored`, `classified`, `routed`, `converted`, `closed`, `quarantined` |
| terminal_states | `routed`, `converted`, `closed`, `quarantined` |

### Pipeline Stages

```
incoming_message
    → normalize_text (lowercase, unicode, dedup)
        → extract_entities (budget, location, type, timeline)
            → detect_intent (keyword/ML classification)
                → context_enrichment (lookup user history)
                    → lead_scoring (base + boosters - penalties)
                        → lead_classification (HOT/WARM/COLD/LOW/SPAM)
                            → crm_routing (zone/availability/score/manual)
```

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| incoming | normalized | normalize_complete | text_received | normalize_text, detect_language |
| incoming | quarantined | fraud_detected | fraud_layer_triggered | flag_fraud, suspend |
| normalized | extracted | extraction_complete | entities_detected | extract_entities |
| normalized | enriched | no_entities | all_optional_fields_empty | skip_to_enrichment |
| extracted | intent_detected | intent_classified | confidence_met | classify_intent, map_project_type |
| extracted | enriched | low_confidence | confidence < threshold | mark_for_human_review |
| intent_detected | enriched | enrichment_complete | context_available | enrich_with_user_history |
| enriched | scored | scoring_complete | all_booster_penalty_checks | calculate_score |
| scored | classified | classification_complete | score_calculated | assign_classification |
| classified | routed | routing_complete | agent_available | route_to_agent, set_sla |
| classified | quarantined | spam_detected | classification_is_spam | quarantine_lead |
| routed | converted | conversion_occurs | project_created | link_to_project, mark_converted |
| routed | closed | lead_closed | no_conversion_within_sla | close_lead, log_outcome |
| converted | closed | transaction_complete | transaction_done | close_lead, record_revenue |

### Guards

| Guard | Condition |
|-------|-----------|
| text_received | Raw message text is non-empty |
| fraud_layer_triggered | Any of 4 anti-fraud layers fires |
| entities_detected | At least one entity extracted (budget, location, type) |
| all_optional_fields_empty | No extractable entities found |
| confidence_met | Intent detection confidence >= 0.70 |
| context_available | User history or profile exists for enrichment |
| score_calculated | base_score + boosters - penalties computed |
| classification_is_spam | Final score < 20 |
| agent_available | Agent with matching zone/capacity exists |
| project_created | Lead converted to Project entity |
| transaction_done | Associated transaction completed |

### Triggers

| Trigger | Source |
|---------|--------|
| normalize_complete | System (NLP pipeline) |
| fraud_detected | Anti-fraud engine |
| extraction_complete | Entity extraction engine |
| no_entities | Entity extraction engine (fallback) |
| intent_classified | Intent detection engine |
| low_confidence | Intent detection engine (below threshold) |
| enrichment_complete | Context enrichment service |
| scoring_complete | Scoring engine |
| classification_complete | Classification engine |
| spam_detected | Classification engine |
| routing_complete | Routing engine |
| conversion_occurs | System (project creation event) |
| lead_closed | System (cron or agent action) |

### Actions

| Action | Description |
|--------|-------------|
| normalize_text | Lowercase, unicode normalize, remove noise |
| detect_language | Identify FR/EN/PID |
| flag_fraud | Set fraud flags, apply action (suspend/block) |
| extract_entities | Parse budget, location, type, timeline |
| classify_intent | Map to buy/rent/sell/invest/find/service/other |
| map_project_type | Convert detected intent to project_type |
| enrich_with_user_history | Look up past projects, conversations, behavior |
| calculate_score | Compute base + boosters - penalties |
| assign_classification | Map score to HOT/WARM/COLD/LOW/SPAM |
| route_to_agent | Find best agent, assign lead, notify |
| set_sla | Set P0-P3 priority and response deadline |
| quarantine_lead | Isolate spam lead for review |
| link_to_project | Associate lead with converted project |
| close_lead | Finalize lead record |

### SLA

| Classification | Response Target | Assignment |
|---------------|----------------|------------|
| HOT (80-100+) | < 30 min (P0) | Immediate routing |
| WARM (60-79) | < 2h (P1) | Priority routing |
| COLD (40-59) | < 24h (P2) | Standard routing |
| LOW (20-39) | < 7d (P3) | Batch routing |
| SPAM (< 20) | N/A | Quarantine |

### NBA Rules

| State | NBA |
|-------|-----|
| incoming | "Process incoming lead" |
| normalized | "Review normalized text" |
| extracted | "Review extracted entities" |
| intent_detected | "Review detected intent and confidence" |
| enriched | "Review enriched profile" |
| scored | "Review lead score breakdown" |
| classified | "Lead ready for assignment" |
| routed | "Respond to lead" (agent), "Lead assigned — awaiting response" |
| converted | "Continue with project qualification" |
| closed | "Lead closed — review outcome" |

### Events

| Event | Payload |
|-------|---------|
| lead.created | {lead_id, source_channel, phone, name, initial_text} |
| lead.normalized | {lead_id, normalized_text, language} |
| lead.fraud_flagged | {lead_id, fraud_layers[], action_taken} |
| lead.intent_detected | {lead_id, intent, confidence, method} |
| lead.scored | {lead_id, base_score, boosters[], penalties[], final_score} |
| lead.classified | {lead_id, classification, score_range} |
| lead.routed | {lead_id, agent_id, routing_method, sla_deadline} |
| lead.sla_breached | {lead_id, sla_priority, breach_type, time_elapsed} |
| lead.converted | {lead_id, project_id, converted_at} |
| lead.closed | {lead_id, outcome, reason, closed_at} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| NLP pipeline fails | Fallback to manual processing, notify operator |
| Entity extraction returns nothing | Skip to intent with minimal data, manual qualification |
| No agent available in zone | Expand to nearest zone, notify manager |
| Scoring engine fails | Use default base score, manual override available |
| Fraud detection false positive | Manual review queue, agent can override |

---

## 9. Publication SIE-Enriched (WF-009)

**Extension ID:** EXT-WF-009
**Entity Type:** `Publication`
**Decision:** CREATE_SPECIALIZED_WORKFLOW
**Source:** WORKFLOW_15 (Gold)

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `publication_sie` |
| entity_type | `Publication` |
| initial_state | `draft` |
| states | `draft`, `content_preparation`, `media_validation`, `sie_code_generation`, `campaign_association`, `quality_check`, `published`, `syndicated`, `performance_monitoring`, `expired`, `archived` |
| terminal_states | `published`, `archived`, `expired` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| draft | content_preparation | prepare_content | property_valid | compile_listing_data, format_description |
| content_preparation | media_validation | media_ready | media_present | validate_photos, check_quality |
| content_preparation | draft | content_rejected | quality_fail | return_for_revision |
| media_validation | sie_code_generation | media_approved | media_quality_ok | generate_sie_reference |
| media_validation | content_preparation | media_rejected | media_insufficient | request_additional_media |
| sie_code_generation | campaign_association | code_generated | reference_unique | associate_campaign, set_targeting |
| campaign_association | quality_check | campaign_set | campaign_valid | run_quality_checks |
| quality_check | published | all_checks_pass | publication_rules_met | publish_listing, notify_owner |
| quality_check | draft | checks_fail | rule_violation | log_violations, return_for_fix |
| published | syndicated | syndication_triggered | channels_configured | push_to_channels |
| published | expired | listing_expires | 90d_no_activity | auto_archive |
| syndicated | performance_monitoring | syndication_complete | all_channels_pushed | start_monitoring |
| performance_monitoring | expired | campaign_ends | duration_exceeded | stop_monitoring |
| expired | archived | cleanup | expired_confirmed | archive_publication |

### Guards

| Guard | Condition |
|-------|-----------|
| property_valid | Property has required fields for publication |
| media_present | At least one photo or video attached |
| media_quality_ok | Media meets resolution and quality thresholds |
| media_insufficient | Quality below threshold or missing required media |
| reference_unique | SIE code does not conflict with existing |
| campaign_valid | Campaign parameters are valid |
| publication_rules_met | All 8 publication rules pass |
| channels_configured | Target syndication channels exist and are active |

### Triggers

| Trigger | Source |
|---------|--------|
| prepare_content | User action |
| media_ready | User uploads media |
| media_approved | Admin/auto validation |
| media_rejected | Admin/auto validation |
| generate_code | System |
| associate_campaign | System or user |
| run_quality_checks | System |
| all_checks_pass | Quality engine |
| checks_fail | Quality engine |
| syndication_triggered | System (cron) |
| listing_expires | System (cron) |
| campaign_ends | System (cron) |

### Actions

| Action | Description |
|--------|-------------|
| compile_listing_data | Aggregate property data for publication |
| format_description | Apply formatting and localization |
| validate_photos | Check resolution, count, relevance |
| generate_sie_reference | Create unique SIE reference code |
| associate_campaign | Link to marketing campaign |
| set_targeting | Set audience targeting parameters |
| run_quality_checks | Execute 8 publication rules |
| publish_listing | Make listing visible on platform |
| notify_owner | Send publication confirmation |
| push_to_channels | Syndicate to external channels |
| start_monitoring | Begin performance tracking |
| auto_archive | Move to archived state |
| archive_publication | Finalize publication record |

### NBA Rules

| State | NBA |
|-------|-----|
| draft | "Complete property content for publication" |
| content_preparation | "Add photos and media" |
| media_validation | "Review media quality" |
| sie_code_generation | "SIE reference code generated" |
| campaign_association | "Select campaign or create new" |
| quality_check | "Review quality check results" |
| published | "Publication active — monitor performance" |
| syndicated | "Listing pushed to external channels" |
| expired | "Listing expired — republish or archive" |

### Events

| Event | Payload |
|-------|---------|
| publication.draft_created | {publication_id, property_id} |
| publication.content_prepared | {publication_id, content_summary} |
| publication.media_validated | {publication_id, media_count, quality_score} |
| publication.sie_code_generated | {publication_id, sie_code} |
| publication.campaign_associated | {publication_id, campaign_id} |
| publication.quality_check_complete | {publication_id, checks[], passed, failed[]} |
| publication.published | {publication_id, published_at, sie_code} |
| publication.syndicated | {publication_id, channels[]} |
| publication.expired | {publication_id, expiry_reason} |
| publication.archived | {publication_id, archived_at} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| SIE code collision | Regenerate with different seed |
| Media quality check fails | Flag specific issues, allow manual override |
| Campaign association fails | Publish without campaign, retry association |
| Syndication channel unavailable | Queue for retry, notify operator |

---

## 10. Redirection SIE-Enriched (WF-010)

**Extension ID:** EXT-WF-010
**Entity Type:** `Redirection`
**Decision:** CREATE_SPECIALIZED_WORKFLOW
**Source:** WORKFLOW_16 (Gold)

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `redirection_sie` |
| entity_type | `Redirection` |
| initial_state | `click_received` |
| states | `click_received`, `user_agent_parsed`, `bot_detection`, `duplicate_detection`, `geolocation`, `analytics_enrichment`, `campaign_attribution`, `conversion_check`, `redirect_executed`, `conversion_logged`, `expired`, `archived` |
| terminal_states | `redirect_executed`, `conversion_logged`, `archived` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| click_received | user_agent_parsed | request_parsed | valid_request | parse_user_agent, extract_headers |
| click_received | archived | invalid_request | malformed_request | log_and_discard |
| user_agent_parsed | bot_detection | ua_parsed | ua_extracted | check_bot_patterns |
| bot_detection | duplicate_detection | not_a_bot | human_user | check_duplicate_click |
| bot_detection | archived | is_bot | bot_detected | log_bot_click, archive |
| duplicate_detection | geolocation | unique_click | not_duplicate | geo_lookup |
| duplicate_detection | archived | duplicate_click | is_duplicate | log_duplicate, archive |
| geolocation | analytics_enrichment | geo_resolved | location_found | enrich_with_geo_data |
| analytics_enrichment | campaign_attribution | enriched | enrichment_complete | attribute_to_campaign |
| campaign_attribution | conversion_check | attributed | campaign_matched | check_for_conversion |
| campaign_attribution | redirect_executed | no_campaign | no_campaign_match | redirect_to_target |
| conversion_check | redirect_executed | conversion_not_found | no_active_conversion | redirect_to_target |
| conversion_check | conversion_logged | conversion_found | active_conversion_found | log_conversion, redirect |
| redirect_executed | conversion_logged | conversion_occurs | post_redirect_action | track_conversion |
| redirect_executed | expired | no_conversion | 30d_no_conversion | expire_redirect |
| conversion_logged | archived | logged | conversion_recorded | finalize, archive |
| expired | archived | cleanup | expired_confirmed | archive |

### Guards

| Guard | Condition |
|-------|-----------|
| valid_request | Valid HTTP request with required headers |
| malformed_request | Missing or invalid headers/parameters |
| ua_extracted | User-agent string successfully parsed |
| human_user | Browser pattern detected (not bot/crawler/spider) |
| bot_detected | Known bot/crawler/spider pattern matched |
| not_duplicate | Same IP + UA + target not seen within 30min window |
| is_duplicate | Click matches previous within dedup window |
| location_found | Geolocation resolved successfully |
| enrichment_complete | Analytics enrichment data collected |
| campaign_matched | Click attributed to known campaign |
| no_campaign_match | No matching campaign found |
| no_active_conversion | No active conversion in progress for this user |
| active_conversion_found | User has active conversion event |
| post_redirect_action | User completes target action after redirect |

### Triggers

| Trigger | Source |
|---------|--------|
| request_parsed | System (HTTP handler) |
| ua_parsed | UA parser service |
| check_bot_patterns | Bot detection service |
| check_duplicate_click | Dedup service |
| geo_lookup | Geolocation service |
| enrich_with_geo_data | Enrichment service |
| attribute_to_campaign | Attribution engine |
| check_for_conversion | Conversion detection service |
| redirect_to_target | System (redirect execution) |
| post_redirect_action | User action on target |
| 30d_no_conversion | System (cron) |

### Events

| Event | Payload |
|-------|---------|
| redirect.click_received | {redirect_id, ip, ua, referer, target_url, timestamp} |
| redirect.bot_detected | {redirect_id, bot_type, pattern_matched} |
| redirect.duplicate_detected | {redirect_id, original_click_id, time_delta} |
| redirect.geo_resolved | {redirect_id, country, city, lat, lng} |
| redirect.campaign_attributed | {redirect_id, campaign_id, source, medium} |
| redirect.executed | {redirect_id, target_url, redirected_at} |
| redirect.conversion_logged | {redirect_id, conversion_type, value} |
| redirect.expired | {redirect_id, no_conversion_days} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Geolocation service unavailable | Proceed with IP-based fallback, log warning |
| Bot detection false negative | Periodic audit of redirected traffic |
| Duplicate detection false positive | Allow through, log for analysis |
| Redirection target unavailable | Log error, return 404/302 to fallback |

---

## 11. Conversion & Attribution (WF-011)

**Extension ID:** EXT-WF-011
**Entity Type:** `Conversion`
**Decision:** CREATE_SPECIALIZED_WORKFLOW
**Source:** WORKFLOW_17 (Gold)

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `conversion_attribution` |
| entity_type | `Conversion` |
| initial_state | `touchpoint_detected` |
| states | `touchpoint_detected`, `session_identified`, `source_attributed`, `campaign_mapped`, `conversion_type_determined`, `lead_generated`, `project_created`, `transaction_completed`, `commission_calculated`, `attributed`, `reported`, `archived` |
| terminal_states | `attributed`, `reported`, `archived` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| touchpoint_detected | session_identified | session_found | cookie_or_fingerprint | identify_session |
| touchpoint_detected | archived | no_session | anonymous_browser | log_anonymous_touchpoint |
| session_identified | source_attributed | source_traced | referer_or_utm | attribute_source |
| source_attributed | campaign_mapped | campaign_linked | campaign_code_valid | map_to_campaign |
| session_identified | campaign_mapped | direct_traffic | no_referer | mark_direct |
| campaign_mapped | conversion_type_determined | conversion_classified | type_mappable | classify_conversion |
| conversion_type_determined | lead_generated | lead_created | project_type_match | create_lead_record |
| conversion_type_determined | project_created | project_initiated | user_logged_in | create_project |
| conversion_type_determined | attributed | no_further_action | informational_only | attribute_directly |
| lead_generated | project_created | lead_converts | lead_to_project | convert_lead_to_project |
| project_created | transaction_completed | deal_closes | transaction_successful | record_deal_value |
| transaction_completed | commission_calculated | commission_ready | deal_value_known | calculate_commission |
| commission_calculated | attributed | attribution_complete | attribution_model_applied | finalize_attribution |
| attributed | reported | report_generated | reporting_cycle | generate_report |

### Guards

| Guard | Condition |
|-------|-----------|
| cookie_or_fingerprint | Session cookie or browser fingerprint available |
| anonymous_browser | No identifying session information |
| referer_or_utm | HTTP referer or UTM parameters present |
| campaign_code_valid | Campaign code recognized in system |
| no_referer | Direct navigation (no referer, no UTM) |
| type_mappable | Conversion type can be determined from context |
| project_type_match | Conversion type matches a known project type |
| user_logged_in | User is authenticated |
| informational_only | Conversion is informational (no project/lead) |
| lead_to_project | Lead was converted to a project |
| transaction_successful | Transaction reached completed state |
| deal_value_known | Transaction price is finalized |
| attribution_model_applied | Attribution model (last-touch) has been applied |

### Triggers

| Trigger | Source |
|---------|--------|
| session_found | Session detection service |
| no_session | Session detection (fallback) |
| source_traced | Source detection engine |
| campaign_linked | Campaign mapping service |
| direct_traffic | Source detection (fallback) |
| conversion_classified | Conversion classifier |
| lead_created | Lead creation event |
| project_initiated | Project creation event |
| lead_converts | Lead-to-project conversion event |
| deal_closes | Transaction completion event |
| commission_ready | Commission service event |
| report_generated | Reporting service (cron/triggered) |

### Events

| Event | Payload |
|-------|---------|
| conversion.touchpoint_detected | {conversion_id, user_agent, referer, url, timestamp} |
| conversion.session_identified | {conversion_id, session_id, user_id?, fingerprint} |
| conversion.source_attributed | {conversion_id, source, medium, channel} |
| conversion.campaign_mapped | {conversion_id, campaign_id, campaign_name} |
| conversion.type_determined | {conversion_id, conversion_type} |
| conversion.lead_generated | {conversion_id, lead_id} |
| conversion.project_created | {conversion_id, project_id} |
| conversion.transaction_completed | {conversion_id, transaction_id, deal_value} |
| conversion.commission_calculated | {conversion_id, commission_amount, basis} |
| conversion.attributed | {conversion_id, attribution_model, attributed_value} |
| conversion.reported | {conversion_id, report_id, report_period} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Session identification fails | Store anonymous touchpoint, retroactively link if user identified |
| Campaign code unrecognized | Log unknown campaign, proceed without attribution |
| Attribution model error (last-touch) | Default to equal attribution, flag for review |
| Commission calculation error | Manual override available, admin notification |

---

## 12. Agent Invitation Workflow (WF-012)

**Extension ID:** EXT-WF-012
**Entity Type:** `AgentInvitation`
**Decision:** CREATE_SPECIALIZED_WORKFLOW
**Source:** WORKFLOW_14 (Gold), EXT-RL-AGENCY-001

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `agent_invitation` |
| entity_type | `AgentInvitation` |
| initial_state | `invitation_sent` |
| states | `invitation_sent`, `link_opened`, `account_created`, `phone_verified`, `cni_uploaded`, `validated`, `active`, `expired`, `revoked` |
| terminal_states | `active`, `expired`, `revoked` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| invitation_sent | link_opened | invitation_opened | link_valid | log_open, redirect_to_signup |
| invitation_sent | expired | link_expired | 7d_no_open | expire_invitation, notify_inviter |
| invitation_sent | revoked | inviter_revokes | revocation_allowed | revoke_invitation, notify_invitee |
| link_opened | account_created | signup_completed | registration_valid | create_user, assign_org_membership |
| link_opened | expired | signup_abandoned | 48h_no_signup | mark_abandoned |
| account_created | phone_verified | otp_confirmed | phone_otp_valid | verify_phone, update_onboarding_status |
| account_created | expired | verification_incomplete | 7d_no_phone_verify | expire |
| phone_verified | cni_uploaded | document_uploaded | doc_valid | store_document, update_status |
| phone_verified | expired | no_document | 7d_no_upload | expire |
| cni_uploaded | validated | admin_validates | validation_approved | approve_agent, assign_agency_role |
| cni_uploaded | revoked | admin_rejects | validation_rejected | reject_application, notify |
| validated | active | activation_complete | all_criteria_met | set_active, notify_org, assign_leads |

### Guards

| Guard | Condition |
|-------|-----------|
| link_valid | Invitation link exists, not expired, not revoked |
| 7d_no_open | Invitation link not opened within 7 days |
| revocation_allowed | Inviter has permission to revoke |
| registration_valid | Signup form complete and valid |
| 48h_no_signup | Link opened but no signup within 48h |
| phone_otp_valid | OTP code matches and within validity window |
| 7d_no_phone_verify | Account created but phone not verified within 7d |
| doc_valid | Uploaded document meets format and content requirements |
| 7d_no_upload | Phone verified but no document uploaded within 7d |
| validation_approved | Admin approves the application |
| validation_rejected | Admin rejects the application |
| all_criteria_met | All onboarding steps complete, minimum requirements satisfied |

### Events

| Event | Payload |
|-------|---------|
| agent_invitation.sent | {invitation_id, inviter_id, invitee_phone, org_id, link} |
| agent_invitation.opened | {invitation_id, opened_at, ip, user_agent} |
| agent_invitation.account_created | {invitation_id, user_id, created_at} |
| agent_invitation.phone_verified | {invitation_id, user_id, verified_at} |
| agent_invitation.cni_uploaded | {invitation_id, document_id, uploaded_at} |
| agent_invitation.validated | {invitation_id, validated_by, validated_at} |
| agent_invitation.activated | {invitation_id, user_id, agency_role, activated_at} |
| agent_invitation.expired | {invitation_id, expiry_reason} |
| agent_invitation.revoked | {invitation_id, revoked_by, reason} |

### NBA Rules

| State | NBA |
|-------|-----|
| invitation_sent | "Waiting for invitee to open invitation link" |
| link_opened | "Complete registration form" (invitee) |
| account_created | "Verify phone number via OTP" (invitee) |
| phone_verified | "Upload CNI/passport for identity verification" (invitee) |
| cni_uploaded | "Review and validate submitted documents" (admin) |
| validated | "Activate agent and assign role" (admin) |
| active | "Agent is active — assign leads and zones" (admin) |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Invitation link expires | Allow inviter to resend (max 3 resends) |
| OTP verification fails | Allow retry (max 5), then lock for 1h |
| Document upload fails validation | Clear instructions on rejection reason, allow re-upload |
| Admin does not validate | Escalate after 7d, reassign to alternate admin |

---

## 13. Identity Resolution Workflow (WF-013)

**Extension ID:** EXT-WF-013
**Entity Type:** `IdentityResolution`
**Decision:** CREATE_SPECIALIZED_WORKFLOW
**Source:** WORKFLOW_20 (Gold), UDM §12

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `identity_resolution` |
| entity_type | `IdentityResolution` |
| initial_state | `detected` |
| states | `detected`, `matched`, `reviewed`, `merged`, `resolved`, `rejected` |
| terminal_states | `resolved`, `rejected` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| detected | matched | match_found | match_score >= 0.70 | compute_match_details |
| detected | resolved | no_match | match_score < 0.70 | log_no_match, close |
| matched | reviewed | flag_for_review | 0.70 <= score < 0.90 AND no_phone_match | queue_for_human_review |
| matched | merged | auto_merge_triggered | score >= 0.90 AND phone_match | execute_merge |
| reviewed | merged | human_approves | review_approved | execute_merge |
| reviewed | rejected | human_rejects | review_rejected | log_rejection, close |
| reviewed | split | human_splits | false_positive | undo_pending_merge, close |
| merged | resolved | merge_complete | all_entities_merged | finalize_resolution |
| merged | split | merge_rolled_back | within_rollback_window | undo_merge, restore |

### Guards

| Guard | Condition |
|-------|-----------|
| match_score >= 0.70 | Total similarity score >= 70% |
| match_score < 0.70 | Total similarity score < 70% |
| no_phone_match | Phone signal did not contribute to match |
| score >= 0.90 AND phone_match | High confidence with phone match → auto-merge |
| human_approves | Reviewer confirms merge should proceed |
| human_rejects | Reviewer determines accounts are distinct |
| false_positive | Review determines the match is incorrect |
| all_entities_merged | All related entities successfully merged |
| within_rollback_window | Rollback requested within 30d of merge |

### Events

| Event | Payload |
|-------|---------|
| identity_resolution.detected | {resolution_id, primary_user_id, candidate_user_ids[], signals[]} |
| identity_resolution.matched | {resolution_id, match_score, signal_breakdown, action (auto_merge | review)} |
| identity_resolution.review_started | {resolution_id, reviewer_id, started_at} |
| identity_resolution.merged | {resolution_id, survivor_id, consumed_id, merged_fields[]} |
| identity_resolution.rejected | {resolution_id, reviewer_id, reason} |
| identity_resolution.resolved | {resolution_id, outcome, resolved_at} |
| identity_resolution.rolled_back | {resolution_id, rolled_back_by, reason} |

### NBA Rules

| State | NBA |
|-------|-----|
| detected | "Running identity resolution checks" |
| matched | "Review potential duplicate accounts" (if flagged) or "Auto-merging accounts" |
| reviewed | "Review match details and approve/reject merge" (admin) |
| merged | "Verify merge results and close" |
| resolved | "Identity resolution complete" |
| rejected | "No match found — no action needed" |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Auto-merge incorrectly merges distinct users | Rollback within 30d window, restore consumed account |
| Merge algorithm conflicts | Use survivor strategy (most recent active account wins) |
| Data inconsistency after merge | Audit log for manual reconciliation |

---

## 14. Main Cross-cutting Workflow (WF-014)

**Extension ID:** EXT-WF-014
**Entity Type:** `Project` (orchestrator)
**Decision:** CREATE_NEW_GENERIC_STATE_MACHINE
**Source:** WORKFLOW_21 (Gold), UDM §6

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `main_cross_cutting` |
| entity_type | `Project` |
| initial_state | `creation` |
| states | `creation`, `qualification`, `matching`, `double_consent`, `mise_en_relation`, `visit`, `negotiation`, `transaction`, `closure`, `archive`, `cancelled` |
| terminal_states | `closure`, `archive`, `cancelled` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| creation | qualification | project_created | project_data_valid | start_qualification |
| qualification | matching | qualification_complete | all_steps_done | trigger_matching |
| qualification | cancelled | user_cancels | cancellation_policy | cancel_project |
| matching | double_consent | match_accepted | match_found_and_accepted | initiate_double_consent |
| matching | qualification | insufficient_matches | no_match_found | requalify_criteria |
| double_consent | mise_en_relation | consent_obtained | both_parties_consented | establish_contact |
| double_consent | matching | consent_failed | either_party_refused | trigger_rematching |
| mise_en_relation | visit | visit_requested | contact_established | schedule_visit |
| mise_en_relation | matching | contact_failed | no_progress | trigger_rematching |
| visit | negotiation | visit_completed_satisfied | satisfaction >= 4 | open_negotiation |
| visit | matching | visit_completed_unsatisfied | satisfaction < 3 | trigger_rematching |
| visit | negotiation | visit_completed_neutral | satisfaction == 3 | propose_second_visit_or_negotiation |
| negotiation | transaction | deal_agreed | offer_accepted | create_transaction |
| negotiation | matching | negotiation_failed | no_deal | trigger_rematching |
| transaction | closure | transaction_completed | all_steps_done | close_project |
| transaction | matching | transaction_failed | deal_failed | trigger_rematching |
| closure | archive | archived | closure_confirmed | archive_project |

### Guards

| Guard | Condition |
|-------|-----------|
| project_data_valid | Project has minimum required fields |
| all_steps_done | Qualification 10-step order completed |
| match_found_and_accepted | Match score >= 60 and demandeur accepted |
| no_match_found | No match with score >= 60 after search expansion |
| both_parties_consented | Double consent obtained from both parties |
| either_party_refused | Either demandeur or holder refused consent |
| contact_established | Contact entity in established state |
| no_progress | No visit scheduled within 30d of contact |
| satisfaction >= 4 | Post-visit satisfaction rating >= 4 |
| satisfaction < 3 | Post-visit satisfaction rating < 3 |
| satisfaction == 3 | Post-visit satisfaction rating == 3 |
| offer_accepted | Negotiation offer accepted by both parties |
| no_deal | Negotiation failed (rejected, silence, deadlock) |
| all_steps_done (transaction) | Transaction completed through all states |

### Delegated Sub-workflows

| Orchestrator State | Delegated Workflow | Workflow Entity |
|--------------------|-------------------|-----------------|
| qualification | Qualification Workflow (10 steps) | Project |
| matching | Matching Lifecycle (WF-001) | Match |
| double_consent | Mise en Relation (WF-002) | Contact |
| mise_en_relation | Mise en Relation (WF-002) | Contact |
| visit | Visit Lifecycle (WF-003) | Visit |
| negotiation | Negotiation Workflow | Conversation |
| transaction | Transaction Lifecycle (WF-004) | Transaction |

### Events

| Event | Payload |
|-------|---------|
| project.started | {project_id, user_id, project_type} |
| project.qualification_completed | {project_id, qualification_summary} |
| project.matching_initiated | {project_id, criteria_summary} |
| project.double_consent_initiated | {project_id, match_id} |
| project.contact_established | {project_id, contact_id} |
| project.visit_scheduled | {project_id, visit_id} |
| project.negotiation_started | {project_id, negotiation_id} |
| project.transaction_created | {project_id, transaction_id} |
| project.closed | {project_id, outcome, closed_at} |
| project.archived | {project_id, archived_at} |
| project.cancelled | {project_id, reason, cancelled_at} |

### Failure Policy

| Failure Mode | Handling |
|-------------|----------|
| Any sub-workflow fails | Orchestrator captures failure, offers rematching or alternative path |
| User inactivity at any stage | NBA reminders at configurable intervals, auto-archive after max inactivity |
| Sub-workflow timeout | Escalate to agent, offer manual intervention |
| Concurrent modifications | Optimistic locking on project version |

---

## 15. Property Lifecycle

**Entity Type:** `Property`
**Decision:** EXTEND_CURRENT (extend V2's 5-status model)
**Source:** UDM §3, PROPERTY_TYPE_CROSSWALK.md

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `property_lifecycle` |
| entity_type | `Property` |
| initial_state | `creation` |
| states | `creation`, `normalization`, `classification`, `validation`, `published`, `matching`, `visit`, `negotiation`, `transaction`, `completed`, `archived`, `conserved`, `deleted` |
| terminal_states | `completed`, `archived`, `conserved`, `deleted` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| creation | normalization | data_entered | required_fields_present | normalize_data |
| normalization | classification | normalized | normalization_complete | classify_property |
| classification | validation | classified | family_and_type_set | validate_publication_rules |
| classification | creation | reclassify | incorrect_classification | reset_classification |
| validation | published | all_rules_pass | publication_rules_ok | publish, generate_sie_code |
| validation | creation | validation_fail | rule_violations | return_to_creation |
| published | matching | match_initiated | property_active | start_matching |
| published | archived | owner_archives | owner_request | archive |
| matching | visit | visit_scheduled | match_found | schedule_visit |
| matching | archived | no_matches | 90d_no_match | offer_improvement_or_archive |
| visit | negotiation | negotiation_started | post_visit | begin_negotiation |
| visit | published | visit_no_interest | no_interest | return_to_matching |
| negotiation | transaction | deal_agreed | offer_accepted | create_transaction |
| negotiation | published | negotiation_failed | no_deal | return_to_matching |
| transaction | completed | transaction_done | deal_closed | mark_sold_rented |
| transaction | published | transaction_failed | deal_fell_through | return_to_matching |
| completed | archived | post_completion | 90d_post_completion | archive |
| completed | conserved | seller_requests | conservation_request | mark_conserved |
| archived | deleted | permanent_deletion | 365d_in_archive | soft_delete |
| archived | published | reactivate | owner_reactivates | restore, rerun_validation |

### Guards

| Guard | Condition |
|-------|-----------|
| required_fields_present | title, family, type, location, price, owner all present |
| normalization_complete | Data passes normalization rules |
| family_and_type_set | property_family and property_type are valid |
| publication_rules_ok | All 8 publication rules pass |
| property_active | Property is in published state and not expired |
| match_found | At least one match with score >= 60 |
| 90d_no_match | No acceptable match found in 90 days |
| post_visit | Visit completed with any outcome |
| no_interest | Demanduer not interested after visit |
| offer_accepted | Negotiation reached agreement |
| no_deal | Negotiation failed |
| deal_closed | Transaction completed |
| deal_fell_through | Transaction failed |
| 90d_post_completion | 90 days after transaction completion |
| conservation_request | Owner requests conservation (off-market but not archived) |
| 365d_in_archive | Property has been archived for 365 days |

### Events

| Event | Payload |
|-------|---------|
| property.created | {property_id, owner_id, family, type} |
| property.normalized | {property_id, normalization_result} |
| property.classified | {property_id, family, type, subtype} |
| property.published | {property_id, published_at, sie_code} |
| property.matching_started | {property_id} |
| property.visit_scheduled | {property_id, visit_id} |
| property.negotiation_started | {property_id} |
| property.transaction_created | {property_id, transaction_id} |
| property.completed | {property_id, outcome (sold/rented), price_final} |
| property.archived | {property_id, archive_reason} |
| property.conserved | {property_id, conserved_at} |
| property.deleted | {property_id, deleted_at} |

### SLA

| State | Max Duration |
|-------|-------------|
| creation | 7d to complete required fields |
| normalization | 24h |
| classification | 24h |
| validation | 48h (pending admin review) |
| published | 90d (auto-archive if no activity) |
| matching | 90d (auto-suggest improvement) |
| completed | 90d (auto-archive) |
| archived | 365d (auto-delete notification) |

---

## 16. Dossier Lifecycle

**Entity Type:** `Project` (as Dossier)
**Decision:** EXTEND_CURRENT (extend V2's 5-status model)
**Source:** UDM §6

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `dossier_lifecycle` |
| entity_type | `Project` |
| initial_state | `creation` |
| states | `creation`, `qualification`, `matching`, `presentation`, `wait_demandeur`, `wait_holder`, `mise_en_relation`, `visit`, `negotiation`, `agreement`, `transaction`, `closure`, `archive`, `cancelled` |
| terminal_states | `closure`, `archive`, `cancelled` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| creation | qualification | intent_detected | intent_valid | start_10_step_qualification |
| qualification | matching | qualification_complete | all_10_steps_done | trigger_matching_engine |
| qualification | cancelled | user_cancels | user_action | cancel_dossier |
| matching | presentation | top_matches_found | matches_ready | present_top_10_matches |
| matching | qualification | no_matches | no_match_60_plus | requalify, expand_criteria |
| presentation | wait_demandeur | demandeur_selects | selection_made | record_selection, notify_holder |
| presentation | matching | demandeur_rejects_all | no_selection | requalify, expand |
| wait_demandeur | wait_holder | demandeur_interested | consent_1_of_2 | contact_holder |
| wait_demandeur | matching | demandeur_not_interested | refusal | exclude_property, rematch |
| wait_holder | mise_en_relation | holder_favorable | consent_2_of_2 | establish_contact |
| wait_holder | wait_demandeur | holder_refuses | holder_refusal | notify_demandeur, offer_alternative |
| wait_holder | presentation | holder_silence | 72h_no_response | send_reminders, then new_match |
| mise_en_relation | visit | visit_requested | contact_active | schedule_visit |
| mise_en_relation | matching | no_progress | 30d_no_visit | trigger_rematching |
| visit | negotiation | visit_done | post_visit | begin_negotiation |
| visit | matching | visit_failed | no_show_or_disinterest | trigger_rematching |
| negotiation | agreement | deal_reached | offer_accepted | record_agreement |
| negotiation | matching | deal_failed | negotiation_failed | trigger_rematching |
| agreement | transaction | transaction_initiated | agreement_valid | create_transaction |
| agreement | matching | agreement_voided | within_cooldown | void_agreement |
| transaction | closure | transaction_completed | all_done | close_dossier |
| transaction | matching | transaction_failed | deal_collapsed | trigger_rematching |
| closure | archive | archived | closure_confirmed | archive_dossier |

### Guards

| Guard | Condition |
|-------|-----------|
| intent_valid | Intent detected or project_type selected |
| all_10_steps_done | All 10 qualification steps completed |
| matches_ready | At least one match with score >= 60 |
| no_match_60_plus | No match reached minimum score threshold |
| selection_made | Demandeur selected a property from top 10 |
| no_selection | Demandeur rejected all presented matches |
| consent_1_of_2 | Demandeur expresses interest (consent 1/2) |
| refusal | Demandeur explicitly refuses |
| consent_2_of_2 | Holder agrees to contact (consent 2/2) |
| holder_refusal | Holder explicitly refuses |
| 72h_no_response | Holder did not respond within 72h |
| contact_active | Contact is in established state |

### Events

| Event | Payload |
|-------|---------|
| dossier.created | {project_id, user_id, intent, project_type} |
| dossier.qualification_completed | {project_id, steps_completed, summary} |
| dossier.matching_started | {project_id, criteria} |
| dossier.matches_presented | {project_id, match_count, top_scores[]} |
| dossier.demandeur_interested | {project_id, property_id, timestamp} |
| dossier.holder_contacted | {project_id, holder_id, timestamp} |
| dossier.holder_favorable | {project_id, holder_id, timestamp} |
| dossier.contact_established | {project_id, contact_id} |
| dossier.visit_scheduled | {project_id, visit_id} |
| dossier.negotiation_started | {project_id, negotiation_id} |
| dossier.agreement_reached | {project_id, terms_summary} |
| dossier.transaction_initiated | {project_id, transaction_id} |
| dossier.closed | {project_id, outcome, closed_at} |
| dossier.archived | {project_id, archive_reason} |
| dossier.cancelled | {project_id, reason} |
| dossier.matching_failed | {project_id, reason, suggestion} |

### SLA

| State | Max Duration | Escalation |
|-------|-------------|------------|
| creation | 7d | Reminder to complete qualification |
| qualification | 30d | Reminder after 7d inactivity |
| matching | 7d | Auto-run matching on qualification completion |
| wait_demandeur | 72h | Reminder at 24h, 48h |
| wait_holder | 72h | Reminder at 24h, 48h, 72h → property "to confirm" |
| mise_en_relation | 30d | Suggest visit scheduling |
| visit | 14d | Propose visit windows |
| negotiation | 30d | Silence reminders at 48h, 96h, 168h, 240h |

---

## 17. Negotiation Workflow

**Entity Type:** `Conversation` (negotiation domain)
**Decision:** ENRICH_CURRENT (V2 has basic negotiation stages)
**Source:** UDM §9

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `negotiation_workflow` |
| entity_type | `Conversation` |
| initial_state | `not_started` |
| states | `not_started`, `demandeur_proposes`, `holder_responds`, `counter_offer`, `accepted`, `rejected`, `silent`, `failed`, `escalated`, `closed` |
| terminal_states | `accepted`, `rejected`, `failed`, `closed` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| not_started | demandeur_proposes | offer_made | valid_offer | record_offer, notify_holder |
| demandeur_proposes | holder_responds | holder_responds | response_received | record_response |
| demandeur_proposes | silent | holder_silence | 48h_no_response | start_silence_timer |
| holder_responds | counter_offer | counter_made | counter_valid | record_counter, notify_demandeur |
| holder_responds | accepted | holder_accepts | acceptance_valid | record_acceptance |
| holder_responds | rejected | holder_rejects | rejection_received | record_rejection |
| counter_offer | demandeur_proposes | demandeur_responds | response_valid | record_response |
| counter_offer | accepted | demandeur_accepts | acceptance_valid | record_acceptance |
| counter_offer | rejected | demandeur_rejects | rejection_received | record_rejection |
| counter_offer | silent | either_silence | 48h_no_response | start_silence_timer |
| silent | failed | silence_too_long | 240h_total_silence | auto_close_failed |
| silent | prior_state | party_responds | response_breaks_silence | resume_negotiation |
| silent | escalated | escalation_requested | either_party_requests | assign_mediator |
| failed | escalated | escalation_offered | party_accepts_escalation | transition_to_mediation |
| escalated | closed | escalation_resolved | mediation_or_decision | close_negotiation |
| accepted | closed | deal_finalized | terms_met | close_negotiation |
| rejected | closed | rejection_finalized | both_notified | close_negotiation |

### Guards

| Guard | Condition |
|-------|-----------|
| valid_offer | Offer amount is valid and negotiable elements specified |
| response_received | Holder has provided response to offer |
| counter_valid | Counter-offer is within reasonable range |
| acceptance_valid | Acceptance is explicit and unconditional |
| rejection_received | Rejection with or without reason |
| 48h_no_response | 48 hours since last communication |
| 240h_total_silence | Total 240h (10 days) of accumulated silence |
| response_breaks_silence | Either party sends a message after silence period |
| either_party_requests | Either party formally requests escalation |
| party_accepts_escalation | Party agrees to mediation escalation |

### Events

| Event | Payload |
|-------|---------|
| negotiation.started | {negotiation_id, project_id, demandeur_id, holder_id} |
| negotiation.offer_made | {negotiation_id, offer_amount, offered_by, negotiable_elements} |
| negotiation.counter_offer | {negotiation_id, counter_amount, offered_by, terms} |
| negotiation.accepted | {negotiation_id, accepted_amount, accepted_by_both, accepted_at} |
| negotiation.rejected | {negotiation_id, rejected_by, reason} |
| negotiation.silence_reminder | {negotiation_id, reminder_number, days_silent} |
| negotiation.escalated | {negotiation_id, escalated_to, reason, escalated_by} |
| negotiation.failed | {negotiation_id, failure_reason, failure_diagnostic} |
| negotiation.closed | {negotiation_id, outcome, closed_at} |

### NBA Rules

| State | NBA |
|-------|-----|
| not_started | "Prepare your offer" (demandeur) |
| demandeur_proposes | "Review offer and respond" (holder) |
| holder_responds | "Review holder response" (demandeur) |
| counter_offer | "Review counter-offer and respond" (both) |
| accepted | "Proceed to formalize agreement" |
| rejected | "View alternative properties or adjust offer" |
| silent (48h) | "Send reminder to respond" |
| silent (96h) | "Send second reminder — consider counter-offer" |
| silent (168h) | "Final reminder — negotiation will close" |
| failed | "View failure diagnostic and options" |
| escalated | "Awaiting mediator assignment" |

### SLA

| Period | Action |
|--------|--------|
| 48h silence | First reminder |
| 96h silence | Second reminder |
| 168h silence (7d) | Final reminder |
| 240h silence (10d) | Auto-close as failed (silence) |

---

## 18. Qualification Workflow

**Entity Type:** `Project` (qualification sub-workflow)
**Decision:** CREATE_NEW_GENERIC_STATE_MACHINE
**Source:** UDM §6.1.1, EXT-QUAL-010

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `qualification_workflow` |
| entity_type | `Project` |
| initial_state | `intention` |
| states | `intention`, `type`, `ville`, `quartier`, `budget`, `delai`, `criteres`, `preferences`, `confirmation`, `escalade`, `completed` |
| terminal_states | `completed`, `escalade` |

### 10-Step Progressive Order

| Step | State | Action | Channel Adaptation |
|------|-------|--------|-------------------|
| 1 | intention | Determine primary intent (buy/rent/sell/invest) | WhatsApp: 1 question, Telegram: 1-2, Dashboard: full |
| 2 | type | Property type classification | Dependent on step 1 |
| 3 | ville | City selection | Dependent on step 2 |
| 4 | quartier | Neighborhood preference | Dependent on step 3 |
| 5 | budget | Budget range | Combined with step 4 on constrained channels |
| 6 | delai | Timeline | Optional on constrained channels |
| 7 | criteres | Specific criteria (bedrooms, surface, features) | Multi-select on Dashboard |
| 8 | preferences | Preferences (furnished, floor, parking) | Optional on WhatsApp |
| 9 | confirmation | Qualification summary confirmation | Required on all channels |
| 10 | escalade | Escalate to agent if incomplete | Triggered on step 10 |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| intention | type | intent_clarified | intent_known | set_project_type |
| type | ville | type_selected | type_valid_for_family | update_criteria |
| ville | quartier | city_selected | city_supported | update_location |
| quartier | budget | neighborhood_set | location_known | request_budget |
| budget | delai | budget_set | budget_valid | request_timeline |
| delai | criteres | timeline_set | timeline_valid | request_criteria |
| criteres | preferences | criteria_set | criteria_valid | request_preferences |
| preferences | confirmation | preferences_set | preferences_valid | show_summary |
| confirmation | completed | user_confirms | all_steps_done | finalize_qualification |
| confirmation | intention | user_wants_change | correction_requested | reset_to_step |
| confirmation | escalade | user_needs_help | incomplete_or_confused | escalate_to_agent |
| any | escalade | skip_requested | channel_limit_reached | escalate_with_partial_data |

### Guards

| Guard | Condition |
|-------|-----------|
| intent_known | Primary intent determined (buy/rent/sell/invest/find/service) |
| type_valid_for_family | Property type is valid for the selected family/intent |
| city_supported | City is in supported service area |
| location_known | City and at least neighborhood specified |
| budget_valid | Budget range is reasonable (min <= max) |
| timeline_valid | Timeline is a valid duration |
| criteria_valid | At least one specific criterion provided |
| preferences_valid | Preferences collected (may be empty) |
| all_steps_done | All 10 steps completed |
| correction_requested | User wants to change previous answer |
| incomplete_or_confused | User unable to complete or requests human help |
| channel_limit_reached | Per-channel question limit exceeded |

### Events

| Event | Payload |
|-------|---------|
| qualification.step_completed | {project_id, step, step_number, data} |
| qualification.completed | {project_id, qualification_summary, completed_at} |
| qualification.escalated | {project_id, reason, partial_data} |
| qualification.corrected | {project_id, step_reset, new_value} |

### NBA Rules

| State | NBA |
|-------|-----|
| intention | "What type of property are you looking for?" |
| type | "What property type interests you?" |
| ville | "Which city are you interested in?" |
| quartier | "Do you have a neighborhood preference?" |
| budget | "What is your budget range?" |
| delai | "What is your timeline?" |
| criteres | "Any specific requirements?" |
| preferences | "Any preferences?" |
| confirmation | "Review and confirm your criteria" |
| escalade | "An agent will contact you to complete your qualification" |

---

## 19. Agent Onboarding

**Entity Type:** `User` (onboarding_status)
**Decision:** ENRICH_CURRENT (add onboarding_status to User model)
**Source:** EXT-RL-AGENCY-001, UDM §2

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `agent_onboarding` |
| entity_type | `User` |
| initial_state | `invited` |
| states | `invited`, `account_created`, `phone_verified`, `cni_uploaded`, `validated`, `active`, `rejected`, `expired` |
| terminal_states | `active`, `rejected`, `expired` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| invited | account_created | signup_completes | registration_valid | create_account, send_otp |
| invited | expired | invitation_expires | 7d_no_action | expire, notify_inviter |
| account_created | phone_verified | otp_confirmed | otp_valid | verify_phone, prompt_cni_upload |
| account_created | expired | no_phone_verify | 7d_no_otp | expire, notify |
| phone_verified | cni_uploaded | document_uploaded | doc_format_valid | store_doc, notify_admin |
| phone_verified | expired | no_document_upload | 7d_no_upload | expire |
| cni_uploaded | validated | admin_validates | admin_approves | approve, notify_user |
| cni_uploaded | rejected | admin_rejects | admin_rejects | reject, notify_user_with_reason |
| validated | active | activation_requested | all_steps_verified | set_is_active_agent, assign_role |

### Events

| Event | Payload |
|-------|---------|
| onboarding.invited | {user_id, inviter_id, org_id, invitation_method} |
| onboarding.account_created | {user_id, created_at} |
| onboarding.phone_verified | {user_id, verified_at, method} |
| onboarding.cni_uploaded | {user_id, document_id, uploaded_at} |
| onboarding.validated | {user_id, validated_by, validated_at} |
| onboarding.activated | {user_id, agency_role, activated_at} |
| onboarding.rejected | {user_id, rejected_by, reason} |
| onboarding.expired | {user_id, expiry_reason} |

### NBA Rules

| State | NBA |
|-------|-----|
| invited | "Complete your registration" (invitee) |
| account_created | "Verify your phone number" |
| phone_verified | "Upload your identity document (CNI/passport)" |
| cni_uploaded | "Awaiting admin validation" |
| validated | "Activate your agent account" |
| active | "Welcome — complete your profile and start" |
| rejected | "Review rejection reason and reapply" |

---

## 20. Organization Lifecycle

**Entity Type:** `Organization`
**Decision:** EXTEND_CURRENT (add lifecycle_state to Organization model)
**Source:** UDM §13

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `organization_lifecycle` |
| entity_type | `Organization` |
| initial_state | `creation` |
| states | `creation`, `validation`, `active`, `suspended`, `dissolution`, `archived` |
| terminal_states | `active`, `archived`, `dissolved` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| creation | validation | registration_submitted | docs_uploaded | notify_admin, start_review |
| creation | archived | registration_abandoned | 30d_no_submission | auto_archive |
| validation | active | admin_approves | verification_passed | activate_org, notify_responsible |
| validation | creation | more_info_needed | docs_incomplete | request_additional_docs |
| validation | archived | admin_rejects | verification_failed | reject_with_reason |
| active | suspended | admin_suspends | violation_or_complaint | suspend_org, notify_members, reassign_leads |
| suspended | active | admin_unsuspends | issue_resolved | restore_org, notify_members |
| suspended | dissolution | dissolution_initiated | admin_or_org_requests | start_dissolution |
| dissolution | archived | dissolution_complete | all_obligations_met | finalize, archive_data |

### Guards

| Guard | Condition |
|-------|-----------|
| docs_uploaded | RCCM, tax ID, CNI, and registration document uploaded |
| 30d_no_submission | No submission within 30 days of creation |
| verification_passed | All documents verified, minimum 3 agents (if required) |
| docs_incomplete | Missing or invalid documents |
| verification_failed | Document verification failed |
| violation_or_complaint | Terms violation or formal complaint |
| issue_resolved | Suspension reason resolved |
| admin_or_org_requests | Admin action or org responsible request |
| all_obligations_met | Financial, legal, and data obligations satisfied |

### Events

| Event | Payload |
|-------|---------|
| org.created | {organization_id, responsible_id, name} |
| org.validation_started | {organization_id, admin_id} |
| org.activated | {organization_id, activated_at, verified_by} |
| org.suspended | {organization_id, reason, suspended_by, suspended_at} |
| org.unsuspended | {organization_id, resolved_by, restored_at} |
| org.dissolution_started | {organization_id, requested_by, reason} |
| org.archived | {organization_id, archived_at, archive_reason} |

### NBA Rules

| State | NBA |
|-------|-----|
| creation | "Complete agency registration — upload required documents" |
| validation | "Documents under review by LAWIM admin" |
| active | "Agency is operational — manage agents and leads" |
| suspended | "Resolve suspension issue to restore agency" |
| dissolution | "Complete dissolution process — settle obligations" |
| archived | "Agency closed — data preserved" |

---

## 21. Document Verification

**Entity Type:** `Document`
**Decision:** CREATE_SPECIALIZED_WORKFLOW
**Source:** UDM §15

### State Machine

| Field | Value |
|-------|-------|
| workflow_id | `document_verification` |
| entity_type | `Document` |
| initial_state | `uploaded` |
| states | `uploaded`, `pending`, `validated`, `rejected`, `expired`, `archived` |
| terminal_states | `validated`, `rejected`, `expired`, `archived` |

### Transitions

| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| uploaded | pending | validation_queued | file_integrity_ok | queue_for_review, notify_admin |
| uploaded | rejected | auto_reject | virus_or_corrupt | reject_auto, notify_uploader |
| pending | validated | admin_validates | validation_approved | mark_validated, update_referring_entity |
| pending | rejected | admin_rejects | validation_failed | reject_with_reason, notify_uploader |
| pending | expired | review_timeout | 7d_no_review | expire_pending, notify_admin_escalation |
| validated | expired | document_expires | expiry_date_passed | mark_expired, notify_owner |
| validated | archived | document_superseded | new_version_uploaded | archive_old_version |
| expired | archived | cleanup_post_expiry | 90d_post_expiry | archive_expired |
| rejected | archived | cleanup | 30d_post_rejection | archive_rejected |

### Guards

| Guard | Condition |
|-------|-----------|
| file_integrity_ok | File passes virus scan, format check, size check |
| virus_or_corrupt | File fails integrity checks |
| validation_approved | Admin confirms document is valid |
| validation_failed | Admin determines document is invalid |
| 7d_no_review | No admin action within 7 days |
| expiry_date_passed | Current date > document.expires_at |
| new_version_uploaded | New document uploaded for same purpose |
| 90d_post_expiry | 90 days since expiry |
| 30d_post_rejection | 30 days since rejection |

### Events

| Event | Payload |
|-------|---------|
| document.uploaded | {document_id, document_type, uploaded_by, reference_entity} |
| document.pending | {document_id, queued_at} |
| document.validated | {document_id, validated_by, validated_at} |
| document.rejected | {document_id, rejected_by, reason} |
| document.expired | {document_id, expired_at, document_type} |
| document.archived | {document_id, archive_reason, archived_at} |

### NBA Rules

| State | NBA |
|-------|-----|
| uploaded | "Document queued for verification" |
| pending | "Review document for verification" (admin) |
| validated | "Document verified and active" |
| rejected | "Review rejection reason and upload corrected document" (uploader) |
| expired | "Upload new version of expired document" |
| archived | "Document archived — historical record" |

### SLA

| State | Max Duration | Escalation |
|-------|-------------|------------|
| pending | 7d | Escalate to alternate admin after 7d |
| validated | Per document type | Notify 30d before expiry |
| expired | 90d | Auto-archive after 90d |
| rejected | 30d | Auto-archive after 30d |

### Document Types Requiring Verification

| Document Type | Verification Required | Expiry |
|--------------|---------------------|--------|
| national_id (CNI) | Yes | 10 years |
| passport | Yes | 5 years |
| land_title | Yes | None |
| professional_cert | Yes | Per certification |
| company_registration (RCCM) | Yes | Annual |
| tax_id | Yes | None |
| tax_clearance | Yes | Annual |
| building_permit | Yes | Per project |
| power_of_attorney | Yes | Per mandate |
| lease_contract | No | Per lease term |
| deposit_receipt | No | Per transaction |

---

## 22. Organization Lifecycle

**Entity Type:** `Organization`
**Decision:** EXTEND_CURRENT (add lifecycle_state to Organization model)
**Source:** UDM §13

### State Machine — (Duplicate numbered as §21 above, renumbered correctly in TOC)

Already covered in §21 above. See section 20.

---

## 23. Complete Extension Mapping Table

All 21 workflow extensions cataloged across 4 decision categories.

### 23.1 EXT-WF Extensions (14) from required_extensions.json

| Extension ID | Concept | Entity | States | Decision | Priority |
|-------------|---------|--------|--------|----------|----------|
| EXT-WF-001 | Matching Lifecycle | Match | 10 | CREATE_NEW_GENERIC_STATE_MACHINE | P1 |
| EXT-WF-002 | Mise en Relation / Contact | Contact | 6 | CREATE_SPECIALIZED_WORKFLOW | P1 |
| EXT-WF-003 | Visit Lifecycle | Visit | 9 | CREATE_SPECIALIZED_WORKFLOW | P1 |
| EXT-WF-004 | Transaction Lifecycle | Transaction | 10 | CREATE_SPECIALIZED_WORKFLOW | P1 |
| EXT-WF-005 | Paid Services & Payment | ServiceOrder + Payment | 18 | CREATE_NEW_GENERIC_STATE_MACHINE | P1 |
| EXT-WF-006 | Disputes, Claims & Incidents | Incident | 8 | CREATE_SPECIALIZED_WORKFLOW | P2 |
| EXT-WF-007 | Mediation Workflow | Mediation | 8 | CREATE_SPECIALIZED_WORKFLOW | P3 |
| EXT-WF-008 | CRM Pipeline | Lead | 8 | CREATE_NEW_GENERIC_STATE_MACHINE | P1 |
| EXT-WF-009 | Publication SIE-Enriched | Publication | 11 | CREATE_SPECIALIZED_WORKFLOW | P3 |
| EXT-WF-010 | Redirection SIE-Enriched | Redirection | 12 | CREATE_SPECIALIZED_WORKFLOW | P3 |
| EXT-WF-011 | Conversion & Attribution | Conversion | 12 | CREATE_SPECIALIZED_WORKFLOW | P3 |
| EXT-WF-012 | Agent Invitation | AgentInvitation | 7 | CREATE_SPECIALIZED_WORKFLOW | P2 |
| EXT-WF-013 | Identity Resolution | IdentityResolution | 5 | CREATE_SPECIALIZED_WORKFLOW | P3 |
| EXT-WF-014 | Main Cross-cutting | Project (orchestrator) | 9 | CREATE_NEW_GENERIC_STATE_MACHINE | P2 |

### 23.2 Additional Workflows (7) from Domain Model Extension

| # | Concept | Entity | States | Decision | Source Domain | Priority |
|---|---------|--------|--------|----------|-------------|----------|
| 15 | Property Lifecycle | Property | 13 | EXTEND_CURRENT | UDM §3 | P1 |
| 16 | Dossier Lifecycle | Project | 14 | EXTEND_CURRENT | UDM §6 | P1 |
| 17 | Negotiation Workflow | Conversation | 10 | ENRICH_CURRENT | UDM §9 | P1 |
| 18 | Qualification Workflow | Project | 10 | CREATE_NEW_GENERIC_STATE_MACHINE | UDM §6.1.1 | P1 |
| 19 | Agent Onboarding | User | 6 | ENRICH_CURRENT | UDM §2, EXT-RL-AGENCY-001 | P2 |
| 20 | Organization Lifecycle | Organization | 6 | EXTEND_CURRENT | UDM §13 | P2 |
| 21 | Document Verification | Document | 6 | CREATE_SPECIALIZED_WORKFLOW | UDM §15 | P2 |

### 23.3 All Workflows by Decision Category

| Decision | Count | Workflows |
|----------|-------|-----------|
| EXTEND_CURRENT | 3 | Property Lifecycle, Dossier Lifecycle, Organization Lifecycle |
| ENRICH_CURRENT | 2 | Negotiation Workflow, Agent Onboarding |
| CREATE_NEW_GENERIC_STATE_MACHINE | 5 | Matching, Paid Services & Payment, CRM Pipeline, Main Cross-cutting, Qualification |
| CREATE_SPECIALIZED_WORKFLOW | 11 | Mise en Relation, Visit, Transaction, Disputes, Mediation, Publication SIE, Redirection SIE, Conversion & Attribution, Agent Invitation, Identity Resolution, Document Verification |
| HUMAN_DECISION_REQUIRED | 0 | All resolved in this model |

### 23.4 State Totals Across All Workflows

| Metric | Value |
|--------|-------|
| Total workflows | 21 |
| Total states (combined) | 191 |
| Average states per workflow | 9.1 |
| Total transitions | ~280 |
| Total guards | ~165 |
| Total events | ~155 |
| Total NBA rules | ~95 |

### 23.5 Workflow Implementation by Phase

| Phase | Workflows | Count |
|-------|-----------|-------|
| Phase 1 — Core Business (P1) | Matching, Mise en Relation, Visit, Transaction, Paid Services, CRM Pipeline, Property Lifecycle, Dossier Lifecycle, Negotiation, Qualification | 10 |
| Phase 2 — Operations (P2) | Disputes, Agent Invitation, Main Cross-cutting, Agent Onboarding, Organization Lifecycle, Document Verification | 6 |
| Phase 3 — Analytics (P3) | Publication SIE, Redirection SIE, Conversion & Attribution | 3 |
| Phase 4 — Enhancement (P3) | Mediation, Identity Resolution | 2 |

---

*End of WORKFLOW_EXTENSION_MODEL.md — 21 workflows defined, 191 states cataloged, ~280 transitions specified, complete extension mapping table included.*
