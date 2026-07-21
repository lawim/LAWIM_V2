# LAWIM Conversation Memory Architecture

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 3 — Conversation Memory

## 1. Canonical Memory Hierarchy

LAWIM defines seven levels of memory, each with distinct scope, persistence, and access semantics.

| Level | Name | Scope | Persistence | TTL / Retention |
|-------|------|-------|-------------|-----------------|
| L1 | TURN_MEMORY | Current turn (message, extraction, decision, delivery) | Volatile (in-memory) | Duration of request |
| L2 | CONVERSATION_MEMORY | Conversation state (actor, language, intent, slots, last question) | Database (`conversation_states`) | 365 days |
| L3 | CASE_MEMORY | Case/dossier (LawimCase with qualification, property, handover) | Database (`lawim_cases`) | 1825 days |
| L4 | USER_PREFERENCE_MEMORY | Persistent preferences (language, channel, contact times) | Database (`conversation_facts`) | 1825 days |
| L5 | RELATIONSHIP_MEMORY | Relationship history (consent, satisfaction, engagement) | Database (`conversation_facts`) | 1825 days |
| L6 | AGENT_WORKING_MEMORY | Agent working context (in-memory, TTL-managed) | In-memory cache | Configurable TTL |
| L7 | KNOWLEDGE_REFERENCE_MEMORY | Knowledge base references | Static / indexed | Permanent |

### L1 — Turn Memory

Carries data for the current message processing cycle only:

- Raw incoming message
- Normalised message
- Slot extractions
- Intent decision
- Response delivery status

Not persisted. Reconstructed from raw stores if needed for audit.

### L2 — Conversation Memory

Stored in `conversation_states` table. Contains:

- `conversation_id`, `actor_id`, `channel`
- `language`, `current_intent`, `previous_intent`
- `known_slots`, `missing_slots`, `changed_slots`
- `last_user_message`, `last_lawim_message`
- `qualification_status`, `qualification_step`
- `handover_status`, `state_version`
- Timestamps: `created_at`, `updated_at`

Versioned via `state_version` (optimistic locking).

### L3 — Case Memory

Stored in `lawim_cases` table. Each case represents a business dossier:

- `case_id`, `case_code`, `case_type`, `status`
- `primary_actor_id`, `title`, `active_intent`, `journey_code`
- `active_language`, `qualification_state`, `readiness_status`
- `property_reference`, `assigned_agent`, `handover_status`
- `known_slots`, `last_question_key`, `last_question_slot`
- `summary`, `version` (optimistic locking)
- Timestamps: `created_at`, `updated_at`, `closed_at`

### L4 — User Preference Memory

Stored as facts in `conversation_facts`. Captures:

- Preferred language per channel
- Preferred contact times
- Notification preferences
- Channel preference

### L5 — Relationship Memory

Stored as facts in `conversation_facts`. Captures:

- Cross-channel consent history
- Satisfaction indicators
- Engagement frequency
- Relationship lifecycle events

### L6 — Agent Working Memory

In-memory context for the active agent. Includes:

- Current provider context (LLM-limited view)
- Recent turn history (up to `recent_turn_window`)
- Summary of compacted earlier turns
- Managed by `MemoryCompactionService`

### L7 — Knowledge Reference Memory

Static references loaded from knowledge packs:

- FAQ entries
- Business rules
- Policy documents
- Property taxonomy
- Legal references

## 2. Data Flow

```
Incoming message
  ⇩
ConversationStateEngine.process_turn()
  ⇩  resolves actor, conversation, case
ActiveCaseResolver.resolve()
  ⇩  determines active case or creates DRAFT
MemoryContextBuilder
  ⇩
  ├── build_business_context()   → BusinessMemoryContext   (internal services)
  ├── build_provider_context()   → ProviderMemoryContext   (LLM-limited view)
  └── build_handover_context()   → HumanHandoverContext    (human handover snapshot)
  ⇩
Business/Provider/Handover context delivered to:
  - Planning engine
  - Provider (LLM)
  - Notification services
```

## 3. Storage Tables

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `conversation_states` | Per-conversation state | `conversation_id`, `state_version` |
| `lawim_cases` | Business case dossiers | `case_id`, `version`, `status` |
| `conversation_facts` | Fact/slot storage with supersession | `fact_id`, `supersedes_fact_id` |
| `identity_bindings` | Cross-channel identity links | `binding_id`, `channel`, `channel_identifier` |
| `cross_channel_consents` | Cross-channel continuity consent | `consent_id`, `actor_id` |
| `handover_records` | Agent handover snapshots | `handover_id`, `case_id` |
| `retention_audit_logs` | Destructive operation audit | `log_id`, `action`, `category` |

## 4. Versioning

### Optimistic Locking

- `conversation_states.state_version` — incremented on every state mutation
- `lawim_cases.version` — incremented on every case mutation
- Writers CHECK current version before UPDATE; `VersionConflictError` raised on mismatch
- `MemoryService` retries on version conflict (configurable max retries)

## 5. Correction Flow

Facts support a SUPERSEDED mechanism via `supersedes_fact_id`:

1. User provides new value for an already-confirmed slot
2. `MemoryService.handle_correction()` creates a new fact with:
   - `supersedes_fact_id` pointing to the old fact
   - `confirmation_status` = `CONFIRMED` (or `EXPLICIT`)
3. Old fact gets `confirmation_status` = `SUPERSEDED` and `valid_to` set
4. `FactCollection.add_fact()` automatically marks superseded facts
5. `FactCollection.get_active()` returns only non-superseded facts

## 6. Cross-Channel Identity

See dedicated document: `LAWIM-CROSS-CHANNEL-IDENTITY-AND-CONTINUITY.md`

## 7. Handover

`AgentHandover` captures full case+conversation state for human intervention:

- `handover_id`, `case_id`, `conversation_id`, `actor_id`
- `context_snapshot` — serialised state at handover time
- `status` lifecycle: `REQUESTED` → `ACCEPTED` → `IN_PROGRESS` → `RESOLVED` / `RETURNED_TO_LAWIM`
- `HandoverSnapshot` preserves conversation state for resume

## 8. Context Limitation

`ProviderMemoryContext` (LLM view) MUST NOT include:

- Raw message history beyond compacted summary
- Internal conversation_ids or state_version numbers
- Secrets, tokens, or credentials
- Other actors' case data
- Internal error details
- Database primary keys

## 9. Retention

See dedicated document: `LAWIM-MEMORY-RETENTION-POLICY.md`
