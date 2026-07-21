# LAWIM Case Continuity Model

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 3 — Conversation Memory

## 1. CaseStatus

| Status | Meaning |
|--------|---------|
| `DRAFT` | Initial creation, not yet active |
| `ACTIVE` | Case is being actively processed |
| `WAITING_USER` | Awaiting user input |
| `WAITING_LAWIM` | Awaiting LAWIM processing |
| `READY` | Qualification complete, ready for next step |
| `IN_PROGRESS` | Active processing (e.g., search, matching) |
| `SUSPENDED` | Temporarily suspended |
| `HANDED_OVER` | Transferred to human agent |
| `COMPLETED` | Successfully completed |
| `CANCELLED` | Cancelled by user or system |
| `ARCHIVED` | Archived for retention compliance |

Active statuses (used by `ActiveCaseResolver`): `ACTIVE`, `WAITING_USER`, `WAITING_LAWIM`, `READY`, `IN_PROGRESS`.

## 2. CaseType

| Type | Description |
|------|-------------|
| `BUY` | Property purchase intent |
| `RENT` | Rental search intent |
| `SELL` | Property selling intent |
| `LIST` | Listing request (owner) |
| `PUBLISH` | Publication request |
| `DOCUMENT_REQUEST` | Document collection |
| `COMPLAINT` | Complaint management |
| `OTHER` | Other / uncategorised |

## 3. LawimCase Fields

| Field | Type | Description |
|-------|------|-------------|
| `case_id` | `str` | UUID primary key |
| `case_code` | `str` | Human-readable code (e.g. `CS-A1B2C3D4`) |
| `case_type` | `str` | One of `CaseType` |
| `primary_actor_id` | `str` | Actor associated with this case |
| `title` | `str` | Human-readable title |
| `active_intent` | `str` | Current business intent |
| `journey_code` | `str` | Qualification journey identifier |
| `status` | `CaseStatus` | Current lifecycle status |
| `active_language` | `str` | Active language (ISO 639-1) |
| `qualification_state` | `dict` | Qualification progress state |
| `readiness_status` | `str` | Qualification readiness level |
| `property_reference` | `str\|None` | Linked property reference |
| `assigned_agent` | `str\|None` | Assigned human agent |
| `handover_status` | `str\|None` | Handover status if any |
| `active_conversation_id` | `str\|None` | Currently linked conversation |
| `known_slots` | `dict` | Currently confirmed slot values |
| `last_question_key` | `str` | Last qualification question key |
| `last_question_slot` | `str` | Last qualification question slot |
| `summary` | `str` | Auto-generated case summary |
| `created_at` | `str` | ISO 8601 creation timestamp |
| `updated_at` | `str` | ISO 8601 last update timestamp |
| `closed_at` | `str\|None` | ISO 8601 closure timestamp |
| `version` | `int` | Optimistic lock version |

## 4. CaseConversationLink

Links a case to a conversation for cross-channel continuity:

| Field | Type | Description |
|-------|------|-------------|
| `link_id` | `str` | UUID primary key |
| `case_id` | `str` | Associated case |
| `conversation_id` | `str` | Associated conversation |
| `channel` | `str` | Channel identifier |
| `actor_id` | `str` | Actor identifier |
| `linked_at` | `str` | ISO 8601 link creation timestamp |
| `is_active` | `bool` | Whether the link is active |
| `unlinked_at` | `str\|None` | ISO 8601 unlink timestamp |

## 5. ActiveCaseResolver Resolution Priorities

```
1. Explicit case_id provided → load directly
2. Property/transaction reference (PR-*, TR-*) → search by reference
3. Conversation link → load case linked to current conversation
4. Active case matching intent for actor → filter by intent
5. Controlled resume — any non-terminal case for actor
6. No match → return None (caller creates DRAFT)
```

If `multiple_active` is detected at any priority level, resolution returns `None` and the caller handles disambiguation.

## 6. Multi-Project Distinction

Each case belongs to exactly one project via `case_type` and `journey_code`. A single actor may have:

- One active case per project intent
- Multiple cases across different projects
- Terminal cases (COMPLETED, CANCELLED, ARCHIVED) do not interfere with active resolution

## 7. Case Lifecycle

```
DRAFT
  │
  ▼
ACTIVE ──────────────────────────────────────┐
  │  │          │          │                  │
  │  ▼          ▼          ▼                  │
  │  WAITING_USER  WAITING_LAWIM  IN_PROGRESS  │
  │  │          │          │                  │
  │  └──────────┴──────────┘                  │
  │           │                               │
  │           ▼                               │
  │         READY                             │
  │           │                               │
  ├───────────┼───────────────────────────────┘
  │           │
  ▼           ▼
SUSPENDED   HANDED_OVER
  │           │
  │           ├── RESOLVED → COMPLETED
  │           └── RETURNED_TO_LAWIM → ACTIVE
  │
  ▼           ▼
COMPLETED   CANCELLED
  │
  ▼
ARCHIVED
```
