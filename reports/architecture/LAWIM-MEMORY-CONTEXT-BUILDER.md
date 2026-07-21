# LAWIM Memory Context Builder

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 3 — Conversation Memory

## 1. Context Types

### BusinessMemoryContext

Used by internal services (planning, qualification, case management).

| Field | Source | Description |
|-------|--------|-------------|
| `conversation_state` | `ConversationStateRepository` | Full state object |
| `case` | `LawimCaseService` | Active case object |
| `active_slots` | Merged from state + case | Currently confirmed slots |
| `missing_slots` | State | Slots still needed for qualification |
| `last_question` | State | Last LAWIM message text |
| `intent` | State | Current business intent |
| `journey_code` | State → readiness | Qualification journey identifier |
| `readiness` | State | Qualification readiness status |
| `language` | State | Active language |
| `handover_status` | State | Handover status if any |
| `recent_decisions` | State | Recent decision history |

### ProviderMemoryContext

Used by the LLM provider (limited view to prevent prompt injection and context leakage).

| Field | Description |
|-------|-------------|
| `language` | Active language (ISO 639-1) |
| `intent` | Current business intent |
| `active_facts` | Currently confirmed slot values (key-value only) |
| `last_question_text` | Last LAWIM message to user |
| `response_instructions` | Instructions for the LLM (what to do next) |
| `prohibitions` | Forbidden behaviours (no external referrals, no neutral assistant) |
| `summary` | Compacted conversation summary string |

### HumanHandoverContext

Used when handing over to a human agent.

| Field | Source | Description |
|-------|--------|-------------|
| `case_id` | Case | Case UUID |
| `case_code` | Case | Human-readable case code |
| `actor_id` | Case | Actor identifier |
| `summary` | Builder | Auto-generated handover summary |
| `known_information` | Case | All confirmed slots |
| `missing_information` | Case | Slots still needed |
| `recent_interactions` | Case | Last N interactions |
| `handover_reason` | Case | Why handover was triggered |
| `expected_actions` | Case | Suggested next actions |
| `limitations` | Case | Why LAWIM cannot proceed |
| `language` | Case | Active language |
| `contact_info` | Case | Actor contact information |

## 2. What ProviderMemoryContext MUST NOT Include

| Category | Examples | Reason |
|----------|----------|--------|
| Raw message history | Full turn-by-turn messages | Context window, prompt injection |
| Internal IDs | `conversation_id`, `state_version`, `case_id` version | Security, leak prevention |
| Secrets / tokens | API keys, database credentials, provider keys | Security |
| Other case data | Other actors' cases, unrelated dossiers | Data isolation |
| Internal errors | Stack traces, database errors | OPSEC, leak prevention |
| Primary keys | `id` columns, internal sequence numbers | Defence in depth |
| Provider details | Model names, temperature settings, fallback chain | Brand consistency |

## 3. MemoryContextBuilder Dependencies

| Dependency | Service | Method Used |
|------------|---------|-------------|
| `ConversationStateRepository` | Reads conversation state | `load_by_conversation_id()` |
| `LawimCaseService` | Reads case data | `get_case()` |
| `FactRepository` | Reads conversation facts | `get_active_facts()` |

### Construction Flow

```
MemoryContextBuilder.__init__(case_service, state_repo, fact_repo)
  │
  ├── build_business_context(conversation_id, case_id)
  │     ├── _load_state()        → ConversationState
  │     ├── _load_case()         → LawimCase
  │     ├── _collect_active_slots() → dict
  │     ├── _compute_readiness() → dict
  │     └── → BusinessMemoryContext
  │
  ├── build_provider_context(conversation_id, case_id, max_chars)
  │     ├── _load_state()        → ConversationState
  │     ├── _collect_active_slots() → dict
  │     ├── _build_summary_snippet() → str (truncated to max_chars)
  │     ├── _build_response_instructions() → list[str]
  │     ├── _build_prohibitions() → list[str]
  │     └── → ProviderMemoryContext
  │
  └── build_handover_context(case_id)
        ├── _load_case()         → LawimCase
        ├── _to_case_dict()      → dict
        ├── _build_handover_summary() → str
        └── → HumanHandoverContext
```
