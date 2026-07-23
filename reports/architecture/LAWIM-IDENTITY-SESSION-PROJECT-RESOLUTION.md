# Identity, Session & Project Resolution

**Date:** 2026-07-23
**Status:** COMPLETE

## Identity Resolution

**File:** `lawim_runtime/interaction/identity.py`

### Purpose

Map a channel-specific identity (WhatsApp number, Telegram chat ID, Web user ID) to a LAWIM user.

### Statuses

| Status | Meaning |
|--------|---------|
| RESOLVED | User found via channel mapping |
| ANONYMOUS | No matching user, but not blocked |
| AMBIGUOUS | Multiple users match (edge case) |
| CONFLICTED | Conflicting identity data |
| BLOCKED | User or channel explicitly blocked |

### Rules

- One channel identity maps to one user
- One user can have multiple channel identities
- No automatic merging of identities without proof
- No LLM involvement in resolution

## Session Management

**File:** `lawim_runtime/interaction/session.py`

### Purpose

Manage user session lifecycle across channels.

### Statuses

| Status | Meaning |
|--------|---------|
| ACTIVE | Session in use, within timeout |
| WAITING | Waiting for external input |
| SUSPENDED | Temporarily suspended |
| EXPIRED | No activity within timeout (30 min) |
| CLOSED | Explicitly closed |

### Key Behaviors

- Session timeout: 30 minutes of inactivity
- `resume_or_create`: reuses active session if available
- A project can survive multiple sessions
- A project can continue across channels

## Project Resolution

**File:** `lawim_runtime/interaction/project_resolution.py`

### Purpose

Determine which project an interaction belongs to.

### Statuses

| Status | Meaning |
|--------|---------|
| RESOLVED | Exactly one active project |
| NEW_PROJECT | No existing project, create new |
| AMBIGUOUS | Multiple active projects |
| SUSPENDED | Project is suspended |
| CLOSED | Project is closed |
| NOT_FOUND | No user or no projects |

### Rules

- No LLM involvement in project selection
- Ambiguity produces structured clarification, never auto-merge
- Projects are not created from conversation state alone
