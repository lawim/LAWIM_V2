# API EXTENSION CONTRACTS — Future API Resources for LAWIM_V2

**Document ID:** LAWIM-API-EXT-CONTRACTS-V1
**Status:** CANONICAL — API contract definitions (DO NOT create routes)
**Date:** 2026-07-15
**Extends:** Existing LAWIM_V2 API surface (v3)

---

## Table of Contents

1. [Intent Resources](#1-intents)
2. [Matching Resources](#2-matches)
3. [Visit Resources](#3-visits)
4. [Transaction Resources](#4-transactions)
5. [Service Catalog Resources](#5-services)
6. [Service Order Resources](#6-service-orders)
7. [Payment Resources](#7-payments)
8. [Agent Credit Resources](#8-agent-credits)
9. [Lead Purchase Resources](#9-lead-purchases)
10. [Lead Resources](#10-leads)
11. [Document Resources](#11-documents)
12. [Approval Workflow Resources](#12-approval-workflows)
13. [Incident Resources](#13-incidents)
14. [Mediation Resources](#14-mediations)
15. [Agent Invitation Resources](#15-agent-invitations)
16. [Identity Resolution Resources](#16-identity-resolutions)
17. [Professional Profile Resources](#17-professional-profiles)
18. [Financing Request Resources](#18-financing-requests)
19. [Geography Resources](#19-geography)
20. [Relationship/Consent Resources](#20-relationships)
21. [Consent Tracking Resources](#21-consents)

---

> **Legend:**
> - `{id}` = UUID or integer primary key
> - `?` = nullable/optional field
> - `→ Entity` = reference to another resource
> - `[...]` = array type
> - Permissions use roles: `user`, `agent`, `operator`, `manager`, `admin`, `system`

---

## 1. /intents — Intent Detection CRUD

**Purpose:** Create, read, and manage detected user intents from NLP/keyword pipeline.

### POST /intents
| Field | Detail |
|-------|--------|
| **Purpose** | Submit raw text for intent detection |
| **Idempotence** | Idempotent via `idempotency_key` header; duplicate detection within 5 min window |
| **Permissions** | `user`, `agent`, `operator` |
| **Events** | `intent.detected` → `intent.below_threshold` → `intent.multi_detected` |

**Request Schema:**
```json
{
  "source_text": "Je cherche un terrain à Bastos pour construire",
  "language": "fr",
  "source_channel": "whatsapp",
  "session_id": "sess_abc123",
  "idempotency_key": "key_001"
}
```

**Response Schema (201):**
```json
{
  "id": 1,
  "primary_intent": "buy",
  "confidence": 0.85,
  "language": "fr",
  "is_multi_intent": false,
  "sub_intents": [],
  "urgency_score": 0.3,
  "urgency_level": "medium",
  "extracted_entities": {
    "property_type": "terrain",
    "city": "Yaoundé",
    "neighborhood": "Bastos"
  },
  "detection_method": "keyword",
  "project_type_mapping": "buy",
  "project_id": null,
  "created_at": "2026-07-15T10:00:00Z"
}
```

### GET /intents
| Field | Detail |
|-------|--------|
| **Purpose** | List intents with filtering |
| **Permissions** | `agent`, `operator`, `admin` |
| **Query params** | `?user_id=`, `?primary_intent=`, `?session_id=`, `?created_after=`, `?page=`, `?per_page=` |
| **Response** | Paginated array of Intent objects |

### GET /intents/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Get single intent detail |
| **Permissions** | `user` (own), `agent`, `operator`, `admin` |
| **Response** | Full Intent object |

### POST /intents/detect
| Field | Detail |
|-------|--------|
| **Purpose** | Pure detection endpoint (no persistence) |
| **Permissions** | `user`, `agent`, `operator`, `system` |
| **Idempotence** | Not idempotent (stateless) |
| **Response** | Detection result without saving |

**Privacy:** `source_text` is PII; stored encrypted at rest. Extracted entities are non-PII unless they contain names.

---

## 2. /matches — Matching Engine Results

**Purpose:** Access property-demandeur matching results produced by the scoring engine.

### GET /matches
| Field | Detail |
|-------|--------|
| **Purpose** | List matches for a project or agent |
| **Permissions** | `user` (own project), `agent` (assigned), `operator`, `admin` |
| **Query params** | `?project_id=`, `?property_id=`, `?agent_id=`, `?is_active=`, `?compatibility_level=`, `?page=`, `?per_page=` |
| **Events** | `match.created` → `match.proposed` → `match.accepted` → `match.rejected` |
| **Privacy** | Match scores are internal; holder identity hidden until double consent |
| **Response** | Paginated array of Match objects (score_breakdown visible to agents only) |

### GET /matches/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Get single match with score breakdown |
| **Permissions** | `user` (own project), `agent`, `operator`, `admin` |
| **Response** | Full Match object with score_breakdown |

### POST /matches/{id}/propose
| Field | Detail |
|-------|--------|
| **Purpose** | Propose match to demandeur (auto-triggered by engine) |
| **Permissions** | `system`, `agent`, `operator` |
| **Idempotence** | Idempotent — proposing an already proposed match returns current state |
| **Response** | Updated Match with `is_proposed=true` and `proposed_at` |

### POST /matches/{id}/decide
| Field | Detail |
|-------|--------|
| **Purpose** | Record demandeur or holder decision |
| **Permissions** | `user` (own match), `agent`, `operator` |
| **Request Schema:** | `{"party": "demandeur|holder", "decision": "interested|not_interested|favorable|refused"}` |
| **Idempotence** | Idempotent per party per decision |

### POST /matches/{id}/rematch
| Field | Detail |
|-------|--------|
| **Purpose** | Trigger rematch for declined/expired match |
| **Permissions** | `system`, `agent` |
| **Idempotence** | Not idempotent — each call creates new rematch cycle |
| **Response** | New Match record for next-ranked property |

**Privacy:** Contact details (phone, email) are NEVER exposed in match responses. Only revealed after double consent via Contact resource.

---

## 3. /visits — Visit Scheduling

**Purpose:** Schedule, confirm, and track property visits.

### POST /visits
| Field | Detail |
|-------|--------|
| **Purpose** | Schedule a property visit |
| **Permissions** | `user` (demandeur), `agent` (on behalf), `operator` |
| **Idempotence** | Idempotent via `idempotency_key`; prevents duplicate scheduling within 1h |
| **Events** | `visit.scheduled` → `visit.confirmed` → `visit.completed` → `visit.cancelled` → `visit.no_show` |

**Request Schema:**
```json
{
  "match_id": 42,
  "property_id": 7,
  "demandeur_id": 101,
  "holder_id": 202,
  "agent_id": 303,
  "scheduled_at": "2026-07-20T14:00:00Z",
  "visit_type": "first_visit",
  "notes": "Visiteur intéressé par le jardin"
}
```

**Response Schema (201):**
```json
{
  "id": 1,
  "match_id": 42,
  "status": "requested",
  "scheduled_at": "2026-07-20T14:00:00Z",
  "reminder_24h_sent": false,
  "reminder_2h_sent": false,
  "created_at": "2026-07-15T10:00:00Z"
}
```

### GET /visits
| Field | Detail |
|-------|--------|
| **Purpose** | List visits with filtering |
| **Permissions** | `user` (own), `agent`, `operator`, `admin` |
| **Query params** | `?user_id=`, `?property_id=`, `?status=`, `?from=`, `?to=` |
| **Privacy** | Address hidden until visit confirmed; only scheduled_at shown before confirmation |

### PATCH /visits/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Update visit status (confirm, reschedule, cancel, complete) |
| **Permissions** | `user` (own), `agent`, `operator` |
| **Request Schema:** | `{"status": "confirmed|cancelled|completed", "cancellation_reason": "..."?, "satisfaction_level": "..."?}` |
| **Idempotence** | Idempotent per status transition |

### POST /visits/{id}/remind
| Field | Detail |
|-------|--------|
| **Purpose** | Trigger reminder for upcoming visit |
| **Permissions** | `system` (auto), `agent`, `operator` |
| **Idempotence** | Idempotent per reminder type (24h, 2h) |

---

## 4. /transactions — Transaction Management

**Purpose:** Manage end-to-end property transaction lifecycle.

### POST /transactions
| Field | Detail |
|-------|--------|
| **Purpose** | Create a new transaction after negotiation accepted |
| **Permissions** | `agent`, `operator`, `system` |
| **Idempotence** | Idempotent via `idempotency_key` |

**Request Schema:**
```json
{
  "project_id": 15,
  "property_id": 7,
  "match_id": 42,
  "transaction_type": "sale",
  "demandeur_id": 101,
  "holder_id": 202,
  "agent_id": 303,
  "notaire_id": 404,
  "price_agreed": 50000000,
  "currency": "XAF",
  "payment_milestones": [
    {"type": "deposit", "amount": 5000000, "due_at": "2026-08-01"},
    {"type": "balance", "amount": 45000000, "due_at": "2026-09-15"}
  ]
}
```

**Response Schema (201):**
```json
{
  "id": 1,
  "status": "agreement",
  "transaction_type": "sale",
  "price_agreed": 50000000,
  "created_at": "2026-07-15T10:00:00Z"
}
```

### GET /transactions
| Field | Detail |
|-------|--------|
| **Purpose** | List transactions |
| **Permissions** | `user` (own), `agent`, `operator`, `admin` |
| **Query params** | `?user_id=`, `?property_id=`, `?status=`, `?type=` |

### GET /transactions/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Get transaction detail with all related entities |
| **Permissions** | `user` (own), `agent`, `operator`, `admin` |
| **Includes** | Documents, payment milestones, negotiation history |

### PATCH /transactions/{id}/status
| Field | Detail |
|-------|--------|
| **Purpose** | Advance transaction to next state |
| **Permissions** | `system`, `agent`, `operator` |
| **Events** | `transaction.status_changed` with previous/current state |

**Privacy:** Financial details visible only to transacting parties, their agents, and admins.

---

## 5. /services — Service Catalog

**Purpose:** Browse and manage the LAWIM service catalog.

### GET /services
| Field | Detail |
|-------|--------|
| **Purpose** | List all available services |
| **Permissions** | `public`, `user`, `agent`, `operator`, `admin` |
| **Query params** | `?category=`, `?is_active=`, `?service_type=` |
| **Response** | Paginated array of Service objects |

### GET /services/{code}
| Field | Detail |
|-------|--------|
| **Purpose** | Get service detail by code |
| **Permissions** | `public`, `user`, `agent`, `operator`, `admin` |
| **Response** | Full Service object with description, price, duration |

### POST /services
| Field | Detail |
|-------|--------|
| **Purpose** | Create a new service (admin only) |
| **Permissions** | `admin` |
| **Idempotence** | Idempotent via `service_code` uniqueness |

### PATCH /services/{code}
| Field | Detail |
|-------|--------|
| **Purpose** | Update service (price, active status, etc.) |
| **Permissions** | `admin` |
| **Events** | `service.price_changed` → `service.status_changed` |

**Privacy:** Service catalog is public; pricing is non-sensitive.

---

## 6. /service-orders — Service Ordering

**Purpose:** Purchase and track service fulfillment.

### POST /service-orders
| Field | Detail |
|-------|--------|
| **Purpose** | Order a service from the catalog |
| **Permissions** | `user`, `agent`, `operator` |
| **Idempotence** | Idempotent via `idempotency_key`; dedup within 5 min |

**Request Schema:**
```json
{
  "service_code": "boost_7d",
  "property_id": 7,
  "quantity": 1,
  "price_paid": 2000,
  "currency": "XAF"
}
```

**Response Schema (201):**
```json
{
  "id": 1,
  "service_id": 3,
  "status": "created",
  "price_paid": 2000,
  "expires_at": null,
  "created_at": "2026-07-15T10:00:00Z"
}
```

### GET /service-orders
| Field | Detail |
|-------|--------|
| **Purpose** | List service orders |
| **Permissions** | `user` (own), `agent` (org), `operator`, `admin` |
| **Query params** | `?user_id=`, `?status=`, `?service_code=` |

### PATCH /service-orders/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Update order status (cancel) |
| **Permissions** | `user` (own), `agent`, `operator` |
| **Events** | `service_order.activated` → `service_order.expired` → `service_order.cancelled` |

**Privacy:** Order history visible to purchaser and org admins.

---

## 7. /payments — Payment Processing

**Purpose:** Process and reconcile payments via Campay and other providers.

### POST /payments
| Field | Detail |
|-------|--------|
| **Purpose** | Initiate a payment |
| **Permissions** | `user`, `agent`, `operator` |
| **Idempotence** | Idempotent via `idempotency_key`; critical for financial operations |

**Request Schema:**
```json
{
  "service_order_id": 1,
  "amount": 2000,
  "currency": "XAF",
  "payment_method": "campay",
  "return_url": "https://app.lawim.cm/payments/callback"
}
```

**Response Schema (201):**
```json
{
  "id": 1,
  "status": "created",
  "amount": 2000,
  "payment_method": "campay",
  "provider_reference": null,
  "payment_url": "https://campay.net/pay/abc123",
  "created_at": "2026-07-15T10:00:00Z"
}
```

### GET /payments
| Field | Detail |
|-------|--------|
| **Purpose** | List payments |
| **Permissions** | `user` (own), `agent` (org), `operator`, `admin`, `finance` |
| **Query params** | `?user_id=`, `?status=`, `?payment_method=`, `?from=`, `?to=` |

### GET /payments/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Get payment detail |
| **Permissions** | `user` (own), `agent` (org), `operator`, `admin`, `finance` |

### POST /payments/{id}/retry
| Field | Detail |
|-------|--------|
| **Purpose** | Retry a failed payment |
| **Permissions** | `user` (own), `agent`, `operator` |
| **Idempotence** | Idempotent — same retry key returns same result |

### POST /payments/{id}/refund
| Field | Detail |
|-------|--------|
| **Purpose** | Process refund |
| **Permissions** | `admin`, `finance` |
| **Events** | `payment.refunded` → `service_order.cancelled` (if linked) |

**Privacy:** Financial data is PCI-sensitive; agent sees minimal info. Provider references encrypted at rest.

---

## 8. /agent-credits — Agent Credit Management

**Purpose:** Manage agent credit balances for lead purchases and boosts.

### GET /agent-credits
| Field | Detail |
|-------|--------|
| **Purpose** | Get agent credit balance |
| **Permissions** | `agent` (own), `operator`, `admin` |
| **Query params** | `?user_id=` (admin only) |

**Response:**
```json
{
  "user_id": 303,
  "credits": 500,
  "total_earned": 5000,
  "total_spent": 4500,
  "last_recharge_at": "2026-07-10T10:00:00Z"
}
```

### POST /agent-credits/topup
| Field | Detail |
|-------|--------|
| **Purpose** | Top up agent credits (via payment) |
| **Permissions** | `agent` (own), `admin` |
| **Request Schema:** | `{"user_id": 303, "amount": 5000, "payment_method": "campay"}` |
| **Idempotence** | Idempotent — each topup key processed once |

### POST /agent-credits/transfer
| Field | Detail |
|-------|--------|
| **Purpose** | Transfer credits between agents (admin only) |
| **Permissions** | `admin` |
| **Request Schema:** | `{"from_user_id": 303, "to_user_id": 304, "amount": 100}` |

**Privacy:** Credit balances visible to agent and org admin.

---

## 9. /lead-purchases — Lead Purchase Tracking

**Purpose:** Track agent purchases of lead contacts.

### POST /lead-purchases
| Field | Detail |
|-------|--------|
| **Purpose** | Purchase a lead (reveal contact info) |
| **Permissions** | `agent` |
| **Idempotence** | Idempotent via `idempotency_key`; prevents double-charge |

**Request Schema:**
```json
{
  "lead_id": 50,
  "pack_type": "lead_bronze",
  "payment_id": 10
}
```

**Response Schema (201):**
```json
{
  "id": 1,
  "lead_id": 50,
  "pack_type": "lead_bronze",
  "price_paid": 500,
  "contacts_revealed": true,
  "revealed_at": "2026-07-15T10:00:00Z",
  "lead_contact": {
    "name": "Jean Dupont",
    "phone": "+2376XXXXXXXX",
    "email": "jean@example.com"
  }
}
```

### GET /lead-purchases
| Field | Detail |
|-------|--------|
| **Purpose** | List lead purchases |
| **Permissions** | `agent` (own), `operator`, `admin` |
| **Query params** | `?agent_id=`, `?lead_id=`, `?from=`, `?to=` |

**Privacy:** Lead contact info revealed ONLY upon purchase. Purchase history visible to agent and org admin.

---

## 10. /leads — CRM Lead Management

**Purpose:** Full CRM lead pipeline — scoring, classification, routing.

### POST /leads
| Field | Detail |
|-------|--------|
| **Purpose** | Create a new lead from inbound message or manual entry |
| **Permissions** | `system`, `agent`, `operator` |
| **Idempotence** | Idempotent via message fingerprint (source_text hash + source_channel) |

**Request Schema:**
```json
{
  "source_channel": "whatsapp",
  "source_text": "Bonjour, je cherche un appartement à Douala",
  "language": "fr",
  "user_id": 101,
  "conversation_id": 25
}
```

**Response Schema (201):**
```json
{
  "id": 1,
  "pipeline_stage": "incoming",
  "lead_type": "tenant",
  "base_score": 40,
  "final_score": 65,
  "classification": "warm",
  "boosters_applied": [{"type": "city_detected", "value": 10}, {"type": "budget_detected", "value": 15}],
  "penalties_applied": [],
  "routed_to_agent_id": null,
  "sla_deadline": "2026-07-15T12:00:00Z",
  "created_at": "2026-07-15T10:00:00Z"
}
```

### GET /leads
| Field | Detail |
|-------|--------|
| **Purpose** | List leads with pipeline filtering |
| **Permissions** | `agent` (routed to), `operator`, `admin` |
| **Query params** | `?pipeline_stage=`, `?classification=`, `?routed_to_agent_id=`, `?sla_breached=`, `?from=`, `?to=` |

### GET /leads/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Get lead detail with full scoring breakdown |
| **Permissions** | `agent` (routed to), `operator`, `admin` |

### PATCH /leads/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Update lead (change classification, reassign) |
| **Permissions** | `agent`, `operator`, `admin` |
| **Events** | `lead.scored` → `lead.classified` → `lead.routed` → `lead.sla_breached` |

**Privacy:** Lead source_text is PII. Only routed agent sees full lead. Operator sees masked version. Scoring is internal.

---

## 11. /documents — Document Management

**Purpose:** Upload, validate, and manage documents across entities.

### POST /documents
| Field | Detail |
|-------|--------|
| **Purpose** | Upload a document |
| **Permissions** | `user` (own), `agent`, `operator` |
| **Idempotence** | Not idempotent (each upload is unique) |

**Request Schema:** `multipart/form-data`
```
file: [binary]
entity_type: "transaction|property|user|project"
entity_id: 42
document_type: "national_id"
```

**Response Schema (201):**
```json
{
  "id": 1,
  "document_type": "national_id",
  "filename": "cni_jean_dupont.pdf",
  "status": "pending",
  "size_bytes": 245000,
  "created_at": "2026-07-15T10:00:00Z"
}
```

### GET /documents
| Field | Detail |
|-------|--------|
| **Purpose** | List documents by entity |
| **Permissions** | `user` (own), `agent`, `operator`, `admin` |
| **Query params** | `?entity_type=`, `?entity_id=`, `?document_type=`, `?status=` |

### GET /documents/{id}/download
| Field | Detail |
|-------|--------|
| **Purpose** | Download document (signed URL) |
| **Permissions** | `user` (own), `agent` (org), `operator`, `admin` |
| **Response** | Redirect to signed S3/storage URL (expires in 15 min) |

### PATCH /documents/{id}/validate
| Field | Detail |
|-------|--------|
| **Purpose** | Validate or reject a document |
| **Permissions** | `operator`, `admin` |
| **Request Schema:** | `{"status": "validated|rejected", "rejection_reason": "..."?}` |
| **Events** | `document.validated` → `document.rejected` |

**Privacy:** Documents contain PII and legal data. Access strictly controlled per entity ownership. Download URLs time-limited.

---

## 12. /approval-workflows — Approval Management

**Purpose:** Create and manage approval workflows for verifications, validations, and onboarding.

### POST /approval-workflows
| Field | Detail |
|-------|--------|
| **Purpose** | Submit an item for approval |
| **Permissions** | `agent`, `operator` |
| **Idempotence** | Idempotent per target_type + target_id + workflow_type |

**Request Schema:**
```json
{
  "target_type": "user",
  "target_id": 101,
  "workflow_type": "verification",
  "notes": "Vérification d'identité pour Jean Dupont"
}
```

### GET /approval-workflows
| Field | Detail |
|-------|--------|
| **Purpose** | List pending/reviewed approvals |
| **Permissions** | `operator`, `admin` |
| **Query params** | `?status=`, `?workflow_type=`, `?reviewed_by=` |

### PATCH /approval-workflows/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Approve or reject a workflow |
| **Permissions** | `operator`, `admin` |
| **Request Schema:** | `{"status": "approved|rejected", "rejection_reason": "..."?}` |
| **Events** | `approval.approved` → `approval.rejected` |

**Privacy:** Approval notes visible to requester and reviewer.

---

## 13. /incidents — Incident Reporting

**Purpose:** Report and manage disputes, claims, and platform incidents.

### POST /incidents
| Field | Detail |
|-------|--------|
| **Purpose** | Report an incident |
| **Permissions** | `user`, `agent`, `operator` |
| **Idempotence** | Idempotent per entity_type + entity_id (one open incident per entity) |

**Request Schema:**
```json
{
  "entity_type": "transaction",
  "entity_id": 1,
  "incident_type": "payment_dispute",
  "priority": "normale",
  "description": "Le paiement a été effectué mais le propriétaire nie l'avoir reçu"
}
```

### GET /incidents
| Field | Detail |
|-------|--------|
| **Purpose** | List incidents with priority queue |
| **Permissions** | `operator`, `admin` |
| **Query params** | `?status=`, `?priority=`, `?incident_type=`, `?assigned_to=` |

### PATCH /incidents/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Update incident (assign, escalate, resolve) |
| **Permissions** | `operator`, `admin` |
| **Events** | `incident.escalated` → `incident.resolved` |

**Privacy:** Incident details visible only to operator/admin. Reporter identity may be anonymized.

---

## 14. /mediations — Mediation Management

**Purpose:** Manage mediation workflow between parties.

### POST /mediations
| Field | Detail |
|-------|--------|
| **Purpose** | Propose mediation for an incident or transaction |
| **Permissions** | `system`, `operator`, `admin` |
| **Idempotence** | Idempotent per incident_id |

**Request Schema:**
```json
{
  "incident_id": 5,
  "demandeur_id": 101,
  "holder_id": 202,
  "proposed_by": "system"
}
```

### GET /mediations
| Field | Detail |
|-------|--------|
| **Purpose** | List mediations |
| **Permissions** | `operator`, `admin`, `mediator` |
| **Query params** | `?status=`, `?mediator_id=` |

### PATCH /mediations/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Update mediation status (accept, propose solution, close) |
| **Permissions** | `user` (own), `mediator`, `operator`, `admin` |
| **Events** | `mediation.proposed` → `mediation.accepted` → `mediation.solution_proposed` → `mediation.closed` |

**Privacy:** Mediation exchanges visible only to parties and mediator.

---

## 15. /agent-invitations — Agent Onboarding

**Purpose:** Structured agent invitation and onboarding flow.

### POST /agent-invitations
| Field | Detail |
|-------|--------|
| **Purpose** | Invite a new agent to an organization |
| **Permissions** | `operator` (org admin), `admin` |
| **Idempotence** | Idempotent per email + organization |

**Request Schema:**
```json
{
  "organization_id": 3,
  "invited_email": "nouvelagent@example.com",
  "invited_phone": "+2376XXXXXXXX"
}
```

**Response Schema (201):**
```json
{
  "id": 1,
  "organization_id": 3,
  "invited_email": "nouvelagent@example.com",
  "status": "sent",
  "secure_token": "inv_abc123def456",
  "expires_at": "2026-07-22T10:00:00Z",
  "invitation_url": "https://app.lawim.cm/invite/inv_abc123def456"
}
```

### GET /agent-invitations
| Field | Detail |
|-------|--------|
| **Purpose** | List invitations for organization |
| **Permissions** | `operator`, `admin` |
| **Query params** | `?organization_id=`, `?status=` |

### POST /agent-invitations/{token}/accept
| Field | Detail |
|-------|--------|
| **Purpose** | Accept invitation (create account or link existing) |
| **Permissions** | `public` (valid token) |
| **Idempotence** | Idempotent — accepting the same token returns same result |

**Privacy:** Invitation token is sensitive — treat as password. Store hashed.

---

## 16. /identity-resolutions — Identity Resolution

**Purpose:** Detect and resolve duplicate user identities.

### POST /identity-resolutions
| Field | Detail |
|-------|--------|
| **Purpose** | Report potential duplicate (auto-detected or manual) |
| **Permissions** | `system`, `operator`, `admin` |
| **Idempotence** | Idempotent per user pair |

**Request Schema:**
```json
{
  "primary_user_id": 101,
  "duplicate_user_id": 202,
  "match_signals": {
    "phone": true,
    "email": true,
    "name": 0.85
  },
  "confidence_score": 0.92
}
```

### GET /identity-resolutions
| Field | Detail |
|-------|--------|
| **Purpose** | List pending resolution candidates |
| **Permissions** | `operator`, `admin` |
| **Query params** | `?status=`, `?confidence_min=` |

### POST /identity-resolutions/{id}/resolve
| Field | Detail |
|-------|--------|
| **Purpose** | Merge or discard duplicate |
| **Permissions** | `operator`, `admin` |
| **Request Schema:** | `{"resolution": "merged|false_positive"}` |
| **Events** | `identity.merged` → `identity.false_positive` |

**Privacy:** HIGH — involves merging user accounts with PII. Full audit trail required. Irreversible operation.

---

## 17. /professional-profiles — Professional Registry

**Purpose:** Manage professional service provider profiles.

### POST /professional-profiles
| Field | Detail |
|-------|--------|
| **Purpose** | Create or claim a professional profile |
| **Permissions** | `user`, `agent`, `operator` |
| **Idempotence** | Idempotent per user_id (one profile per user) |

**Request Schema:**
```json
{
  "user_id": 303,
  "professional_type": "agent_immobilier",
  "professional_name": "Agence Duplex Sarl",
  "years_experience": 8,
  "coverage_zones": ["Douala", "Yaoundé"],
  "pricing_model": "fixed",
  "pricing_min": 5000,
  "pricing_max": 50000
}
```

### GET /professional-profiles
| Field | Detail |
|-------|--------|
| **Purpose** | Search professional directory |
| **Permissions** | `public`, `user`, `agent`, `operator` |
| **Query params** | `?professional_type=`, `?is_verified=`, `?city=`, `?min_rating=`, `?page=`, `?per_page=` |

### GET /professional-profiles/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Get professional profile detail |
| **Permissions** | `public` (basic), `authenticated` (full, with rating) |

### PATCH /professional-profiles/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Update professional profile |
| **Permissions** | `user` (own), `operator`, `admin` |

### POST /professional-profiles/{id}/verify
| Field | Detail |
|-------|--------|
| **Purpose** | Verify a professional (admin) |
| **Permissions** | `operator`, `admin` |
| **Events** | `professional.verified` |

**Privacy:** Contact info visible only to authenticated users. Verification documents stored securely.

---

## 18. /financing-requests — Financing Qualification

**Purpose:** Submit and manage financing/loan requests.

### POST /financing-requests
| Field | Detail |
|-------|--------|
| **Purpose** | Submit a financing request |
| **Permissions** | `user`, `agent` (on behalf) |
| **Idempotence** | Idempotent per user + project (one active request per pair) |

**Request Schema:**
```json
{
  "user_id": 101,
  "project_id": 15,
  "loan_amount": 30000000,
  "loan_purpose": "Achat terrain",
  "monthly_income": 1500000,
  "existing_commitments": 200000
}
```

### GET /financing-requests
| Field | Detail |
|-------|--------|
| **Purpose** | List financing requests |
| **Permissions** | `user` (own), `agent`, `operator`, `admin`, `finance` |
| **Query params** | `?user_id=`, `?status=`, `?from=`, `?to=` |

### PATCH /financing-requests/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Update status (under_review, approved, rejected, disbursed) |
| **Permissions** | `operator`, `admin`, `finance` |
| **Events** | `financing.submitted` → `financing.approved` → `financing.disbursed` |

**Privacy:** Financial data is highly sensitive. Strict access control. Encrypted at rest.

---

## 19. /geography — Geographic Entities

**Purpose:** Manage geographic reference data for matching, routing, and search.

### GET /geography
| Field | Detail |
|-------|--------|
| **Purpose** | List geographic units by level |
| **Permissions** | `public` |
| **Query params** | `?level=`, `?parent_id=`, `?search=` |

### GET /geography/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Get geographic unit with children |
| **Permissions** | `public` |
| **Response** | GeographicUnit with nested children |

### GET /geography/search
| Field | Detail |
|-------|--------|
| **Purpose** | Search geographic units by name or alias |
| **Permissions** | `public` |
| **Query params** | `?q=`, `?level=`, `?limit=` |

### POST /geography
| Field | Detail |
|-------|--------|
| **Purpose** | Add a geographic unit |
| **Permissions** | `admin` |
| **Idempotence** | Idempotent per code |

**Privacy:** Geographic data is public. No PII involved.

---

## 20. /relationships — Relationship/Consent Management

**Purpose:** Manage established relationships between users after double consent.

### GET /relationships
| Field | Detail |
|-------|--------|
| **Purpose** | List user's active relationships |
| **Permissions** | `user` (own), `agent`, `operator`, `admin` |
| **Query params** | `?user_id=`, `?status=`, `?type=` |

**Response:**
```json
{
  "id": 1,
  "user_a_id": 101,
  "user_b_id": 202,
  "type": "demandeur_holder",
  "status": "active",
  "match_id": 42,
  "transaction_id": 1,
  "established_at": "2026-07-15T10:00:00Z"
}
```

### POST /relationships
| Field | Detail |
|-------|--------|
| **Purpose** | Create relationship after double consent |
| **Permissions** | `system` (auto), `operator` |
| **Idempotence** | Idempotent per match_id |

### PATCH /relationships/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Update relationship status |
| **Permissions** | `user` (own), `operator`, `admin` |
| **Events** | `relationship.established` → `relationship.suspended` → `relationship.ended` |

### POST /relationships/{id}/end
| Field | Detail |
|-------|--------|
| **Purpose** | End a relationship (unilateral or mutual) |
| **Permissions** | `user` (own), `operator`, `admin` |
| **Events** | `relationship.ended` |

**Privacy:** Relationship existence is visible only to the two parties, their agents, and admins.

---

## 21. /consents — Consent Tracking

**Purpose:** Track explicit user consents for data sharing and platform actions.

### POST /consents
| Field | Detail |
|-------|--------|
| **Purpose** | Record a user consent action |
| **Permissions** | `user` (own), `system` |
| **Idempotence** | Idempotent per user + consent_type (upsert behavior) |

**Request Schema:**
```json
{
  "user_id": 101,
  "consent_type": "data_sharing_match",
  "granted": true,
  "scope": "match_engine",
  "expires_at": "2027-07-15T10:00:00Z"
}
```

### GET /consents
| Field | Detail |
|-------|--------|
| **Purpose** | List user's active consents |
| **Permissions** | `user` (own), `operator`, `admin` |
| **Query params** | `?user_id=`, `?consent_type=`, `?granted=` |

### GET /consents/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Get consent detail |
| **Permissions** | `user` (own), `operator`, `admin` |

### PATCH /consents/{id}
| Field | Detail |
|-------|--------|
| **Purpose** | Update consent (revoke, extend) |
| **Permissions** | `user` (own), `operator`, `admin` |
| **Events** | `consent.granted` → `consent.revoked` → `consent.expired` |

**Privacy:** Consent records are audit-critical. Immutable history. Each consent has a unique audit ID.

---

## Appendix A: Cross-Resource Event Catalog

| Event | Source Resource | Subscribers | Purpose |
|-------|----------------|-------------|---------|
| `intent.detected` | /intents | CRM, Project, Matching | New intent triggers lead creation |
| `match.created` | /matches | Notification, Visit | New match triggers proposal |
| `match.accepted` | /matches | Contact, Notification | Acceptance triggers consent flow |
| `visit.scheduled` | /visits | Notification, Reminder | Schedule triggers reminders |
| `visit.completed` | /visits | Transaction, NBA | Completion triggers next action |
| `transaction.status_changed` | /transactions | Document, Payment, Notification | State change triggers workflows |
| `payment.confirmed` | /payments | ServiceOrder, AgentCredit | Confirmation activates service |
| `payment.failed` | /payments | Notification, Retry | Failure triggers retry flow |
| `lead.scored` | /leads | CRM, Routing | Score update triggers routing |
| `lead.sla_breached` | /leads | Notification, Escalation | Breach triggers escalation |
| `document.validated` | /documents | Transaction, ApprovalWorkflow | Validation advances workflow |
| `approval.approved` | /approval-workflows | User, Property, Organization | Approval unlocks feature |
| `incident.resolved` | /incidents | Mediation, Transaction | Resolution closes loop |
| `professional.verified` | /professional-profiles | Badge, Notification | Verification triggers badge |
| `identity.merged` | /identity-resolutions | User, CRM, All entities | Merge cascades to all refs |
| `consent.revoked` | /consents | Relationship, Data access | Revocation restricts access |

## Appendix B: Permission Matrix

| Resource | PUBLIC | user | agent | operator | admin | system |
|----------|--------|------|-------|----------|-------|--------|
| /services | GET | GET | GET | GET | CRUD | — |
| /geography | GET | GET | GET | GET | CRUD | — |
| /intents | — | POST, GET(own) | CRUD | CRUD | CRUD | POST |
| /matches | — | GET(own), DECIDE | CRUD | CRUD | CRUD | POST |
| /visits | — | CRUD(own) | CRUD | CRUD | CRUD | — |
| /transactions | — | GET(own) | CRUD | CRUD | CRUD | POST |
| /service-orders | — | CRUD(own) | CRUD | CRUD | CRUD | — |
| /payments | — | POST, GET(own) | GET(org) | CRUD | CRUD | POST |
| /agent-credits | — | — | GET(own) | GET | CRUD | — |
| /lead-purchases | — | — | POST, GET(own) | GET | CRUD | — |
| /leads | — | — | GET(routed) | CRUD | CRUD | POST |
| /documents | — | CRUD(own) | CRUD(org) | CRUD | CRUD | — |
| /approval-workflows | — | — | POST | CRUD | CRUD | POST |
| /incidents | — | POST | POST | CRUD | CRUD | — |
| /mediations | — | PATCH(own) | — | CRUD | CRUD | POST |
| /agent-invitations | POST(token) | — | — | CRUD | CRUD | — |
| /identity-resolutions | — | — | — | POST, RESOLVE | CRUD | POST |
| /professional-profiles | GET | POST, PATCH(own) | POST, PATCH(own) | CRUD | CRUD | — |
| /financing-requests | — | POST, GET(own) | POST | GET | CRUD | — |
| /relationships | — | GET(own) | GET(org) | CRUD | CRUD | POST |
| /consents | — | CRUD(own) | CRUD(own) | GET | CRUD | POST |

## Appendix C: Idempotency Guarantees

| Guarantee Level | Resources | Mechanism |
|-----------------|-----------|-----------|
| **Strict** (exactly-once) | /payments, /lead-purchases, /identity-resolutions/{id}/resolve | Idempotency key required; server dedup for 24h |
| **Strong** (at-most-once) | /intents, /matches/{id}/decide, /visits, /transactions, /service-orders | Idempotency key recommended; dedup for 5 min |
| **Natural** (by constraint) | /agent-invitations, /consents, /approval-workflows, /financing-requests, /documents/validate | Natural uniqueness (unique constraint on resource) |
| **None** | /documents (upload), /incidents | Each call creates new resource |

---

*End of API_EXTENSION_CONTRACTS.md — 21 resource groups, ~60 endpoints defined.*
