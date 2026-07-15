# Entity Relationship Map — LAWIM_V2 Canonical Data Model Extension

**Document ID:** LAWIM-ERM-V1  
**Status:** CANONICAL  
**Date:** 2026-07-15

---

## 1. Legend

```
[Entity]          — Canonical entity
───               — Relationship line
|C|               — Cardinality: 1 (one), N (many), M (many)
(FK)              — Foreign key
[1:1]             — One-to-one relationship
[1:N]             — One-to-many relationship
[N:M]             — Many-to-many relationship (via junction)
```

---

## 2. Core Identity & Organization Cluster

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                    IDENTITY & ORGANIZATION CLUSTER               │
  └─────────────────────────────────────────────────────────────────┘

  ┌──────────┐       ┌────────────────────┐       ┌──────────────┐
  │   User   │ 1──N  │ OrganizationMember │ N──1  │ Organization │
  └────┬─────┘       └────────────────────┘       └──────┬───────┘
       │                                                  │
       │ 1:1                                              │ 1:N
       │                                                  │
       ├──────────────────┐                               │
       │                  │                               │
  ┌────┴──────┐   ┌──────┴───────┐               ┌──────┴───────┐
  │AgentCredit│   │Professional  │               │    Lead      │
  │  [1:1]    │   │  Profile     │               │   [1:N]      │
  └───────────┘   │  [1:1]       │               └──────────────┘
                  └──────────────┘

  ┌─────────────────────┐      ┌───────────────────────────┐
  │  IdentityResolution │      │     AgentInvitation       │
  │                     │      │                           │
  │  user_id_primary ───┼──FK──→ User                      │
  │  user_id_duplicate ─┼──FK──→ User            N──1 ───→ Organization │
  │  reviewed_by ───────┼──FK──→ User            1──N ───→ User (invited_by)
  └─────────────────────┘      └───────────────────────────┘

Key Relationships:
  User 1──N OrganizationMember N──1 Organization
    A user belongs to one organization via membership record.
    OrganizationMember captures agency_role, zones, max_leads.

  User 1──1 AgentCredit
    Each agent (user with agency_role) has exactly one credit balance.

  User 1──1 ProfessionalProfile
    Each user can have at most one professional profile.

  Organization 1──N AgentInvitation
    An organization can send many agent invitations.

  IdentityResolution N──1 User (primary)
  IdentityResolution N──1 User (duplicate)
    Links two users as potential duplicates.
```

---

## 3. Property Cluster

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                       PROPERTY CLUSTER                          │
  └─────────────────────────────────────────────────────────────────┘

  ┌──────────────┐       ┌──────────────┐       ┌─────────────┐
  │ Organization │ 1──N  │   Property   │ 1──N  │    Media    │
  └──────────────┘       └──────┬───────┘       └─────────────┘
                                │
                           1──N │
                                │
                    ┌───────────┴───────────┐
                    │                       │
               ┌────┴─────┐          ┌─────┴─────┐
               │  Visit   │          │  Match    │
               │  [N:1]   │          │  [N:1]    │
               └──────────┘          └───────────┘
                    │
                    │ 1──N
                    │
               ┌────┴─────────┐
               │ Transaction  │
               │   [N:1]      │
               └──────────────┘

Key Relationships:
  Organization 1──N Property
    An organization owns many properties. Property.owner_organization_id (FK).

  Property 1──N Media
    A property has many media items (photos, videos, documents).

  Property 1──N Visit
    A property receives many visit requests.

  Property 1──N Match
    A property is matched to many projects.

  Property 1──N Transaction
    A property can have many transactions over time.
```

---

## 4. Project & Intent Cluster

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                     PROJECT & INTENT CLUSTER                    │
  └─────────────────────────────────────────────────────────────────┘

  ┌──────────┐       ┌──────────────┐       ┌────────────┐
  │   User   │ 1──N  │   Project    │ N──1  │  Intent    │
  └──────────┘       └──────┬───────┘       └────────────┘
                            │
                     N──1   │         N──1
                    ┌───────┴───────┐
                    │               │
               ┌────┴─────┐   ┌────┴─────┐
               │  Match   │   │  Visit   │
               │  [1:N]   │   │  [1:N]   │
               └──────────┘   └──────────┘
                    │
                    │ 1──N
                    │
               ┌────┴─────────┐
               │ Transaction  │
               │   [1:N]      │
               └──────────────┘

Key Relationships:
  User 1──N Project
    A user can have many real estate projects.

  Intent 1──N Project
    An intent detection can spawn multiple projects (multi-intent).

  Project 1──N Match
    A project generates many property matches.

  Project 1──N Visit
    A project schedules many visits.

  Project 1──N Transaction
    A project can result in multiple transactions.
```

---

## 5. Services & Financial Cluster

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                    SERVICES & FINANCIAL CLUSTER                  │
  └─────────────────────────────────────────────────────────────────┘

  ┌──────────┐       ┌──────────────┐       ┌──────────────┐
  │ Service  │ 1──N  │ ServiceOrder │ N──1  │   Payment    │
  └──────────┘       └──────┬───────┘       └──────────────┘
                            │
                      N──1  │          N──1
                    ┌───────┴───────┐
                    │               │
               ┌────┴─────┐   ┌────┴──────────┐
               │   User   │   │ Organization   │
               │ [N:1]    │   │   [N:1]        │
               └──────────┘   └────────────────┘

  ┌──────────────┐       ┌──────────────────┐
  │ AgentCredit  │ 1──N  │ CreditTxn (impl.)│
  └──────┬───────┘       └──────────────────┘
         │
         │ 1:1
         │
    ┌────┴─────┐
    │   User   │
    └──────────┘

  ┌──────────────┐       ┌──────────┐       ┌──────────────┐
  │ LeadPurchase │ N──1  │   User   │ N──1  │    Lead      │
  └──────┬───────┘       └──────────┘       └──────────────┘
         │
         │ N:1
         │
    ┌────┴──────────┐
    │   Payment     │
    └───────────────┘

Key Relationships:
  Service 1──N ServiceOrder
    A service catalog item can be ordered many times.

  ServiceOrder N──1 Payment
    Each service order has one associated payment.

  ServiceOrder N──1 User (ordering user)
  ServiceOrder N──1 Organization (ordering org)

  User 1──1 AgentCredit
    One credit balance per agent.

  LeadPurchase N──1 Lead
    A lead can be purchased by multiple agents? No — uniqueness constraint on lead_id, user_id for lead_bronze.
    One lead purchase per lead per agent.

  LeadPurchase N──1 Payment
    Each lead purchase has an associated payment.
```

---

## 6. CRM & Lead Cluster

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                       CRM & LEAD CLUSTER                        │
  └─────────────────────────────────────────────────────────────────┘

  ┌──────────┐       ┌──────────────┐       ┌──────────────┐
  │   User   │ 1──N  │     Lead     │ N──1  │ Conversation │
  └────┬─────┘       └──────┬───────┘       └──────────────┘
       │                    │
       │ 1:N (assigned_to)  │ N:1
       │                    │
       │              ┌─────┴──────┐
       │              │            │
       │         ┌────┴────┐  ┌───┴────────┐
       │         │ Property│  │  Project   │
       │         │ [N:1]   │  │  [N:1]     │
       │         └─────────┘  └────────────┘
       │
       │ 1:N (lead_purchases)
       │
  ┌────┴──────────┐
  │ LeadPurchase  │
  └───────────────┘

Key Relationships:
  User 1──N Lead (source user)
    A user can generate many leads.

  User 1──N Lead (assigned_to — agent)
    An agent can be assigned many leads.

  Lead N──1 Conversation
    A lead originates from a conversation.

  Lead N──1 Property
    Lead may reference a specific property.

  Lead N──1 Project
    Lead may reference a specific project.

  Lead 1──N LeadPurchase
    A lead can be purchased once per agent type.
```

---

## 7. Document Cluster

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                       DOCUMENT CLUSTER                          │
  └─────────────────────────────────────────────────────────────────┘

  ┌──────────────┐       ┌──────────────┐
  │ Transaction  │ 1──N  │   Document   │
  └──────────────┘       └──────┬───────┘
                                │
                           N──1 │
                                │
                          ┌─────┴─────┐
                          │   User    │
                          │ (verifier)│
                          └───────────┘

  Document also supports polymorphic entity attachment:
    entity_type: "user" | "organization" | "property" | "transaction" | "project"
    entity_id:   <ID of the owning entity>

Key Relationships:
  Transaction 1──N Document
    A transaction requires multiple documents (per transaction type).

  Document N──1 User (verified_by)
    A document is verified by an admin.

  Document is a polymorphic entity — attached to any entity via
    (entity_type, entity_id) composite.
```

---

## 8. Approval & Incident Cluster

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                    APPROVAL & INCIDENT CLUSTER                  │
  └─────────────────────────────────────────────────────────────────┘

  ┌──────────────────┐       ┌──────────────┐       ┌──────────────┐
  │ ApprovalWorkflow │       │   Incident   │ 1──1  │  Mediation   │
  └──────┬───────────┘       └──────┬───────┘       └──────────────┘
         │                          │
    N──1 │                     N──1 │
         │                          │
    ┌────┴─────┐               ┌────┴─────┐
    │   User   │               │   User   │
    │(requester│               │(reporter)│
    │ reviewer)│               │(assigned)│
    └──────────┘               └──────────┘

  ApprovalWorkflow target: polymorphic (target_type, target_id)
    target_type: "organization" | "property" | "user" | "document"

  Mediation N──1 User (mediator)
  Mediation N──1 User (demandeur)
  Mediation N──1 User (detenteur)

Key Relationships:
  ApprovalWorkflow N──1 User (requester)
  ApprovalWorkflow N──1 User (reviewer)
    Approval requests and reviews.

  Incident N──1 User (reporter)
  Incident N──1 User (assigned_to)
    Incident reporting and assignment.

  Incident 1──1 Mediation
    An incident may (optionally) lead to mediation.

  Mediation N──1 Project (optional)
  Mediation N──1 Transaction (optional)
```

---

## 9. Geography Cluster

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                      GEOGRAPHY CLUSTER                          │
  └─────────────────────────────────────────────────────────────────┘

  ┌────────────────┐
  │ GeographicUnit │─── self-referencing parent-child hierarchy
  └───────┬────────┘
          │
    1──N  │ (parent_id)
          │
  ┌───────┴────────┐
  │ GeographicUnit │
  │   (children)   │
  └────────────────┘

  Hierarchy levels:
    country (level 1)
      └── region (level 2)
            └── department (level 3)
                  └── city (level 4)
                        └── district (level 5)
                              └── neighborhood (level 6)
                                    └── zone (level 7)

  Referenced by:
    - Property (city, region via name or FK)
    - Organization zones (JSON array of zone codes)
    - OrganizationMember zones (JSON array of zone codes)
    - Lead routing_zone
    - ProfessionalProfile service_area_zones
    - Project location fields

Key Relationships:
  GeographicUnit 1──N GeographicUnit (self-referencing)
    Parent-child hierarchy for geographic subdivisions.
```

---

## 10. Full Entity Relationship Diagram (Textual)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           LAWIM_V2 FULL ENTITY RELATIONSHIP MAP                       │
└─────────────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐         ┌──────────────────────┐         ┌──────────────┐
  │ AgentCredit  │ 1:1     │        User          │ 1:N     │  AgentInv.   │
  │              │─────────│                      │─────────│              │
  └──────────────┘         │                      │         └──────────────┘
                           │                      │ 1:N
  ┌──────────────┐         │                      │─────────┐
  │Professional  │ 1:1     │                      │         │
  │  Profile     │─────────│                      │         │
  └──────────────┘         │                      │         │
                           │                      │ 1:N     │
  ┌──────────────┐         │                      │─────────│
  │IdentityRes.  │ N:1     │                      │         │
  │ (primary)    │─────────│                      │         │
  └──────────────┘         │                      │         │
                           │                      │ 1:N     │
  ┌──────────────┐         │                      │─────────│
  │IdentityRes.  │ N:1     │                      │         │
  │ (duplicate)  │─────────│                      │         │
  └──────────────┘         │                      │         │
                           │                      │ 1:N     │
  ┌──────────────┐         │                      │─────────│
  │  Intent      │ N:1     │                      │         │
  └──────────────┘         └──────────┬───────────┘         │
                                      │                     │
                          ┌───────────┴───────────┐         │
                          │                       │         │
                     ┌────┴─────┐           ┌─────┴──────┐  │
                     │Project   │           │    Lead    │  │
                     │          │           │ (source)   │  │
                     └────┬─────┘           └─────┬──────┘  │
                          │                       │         │
                     ┌────┴─────┐           ┌─────┴──────┐  │
                     │  Match   │           │LeadPurchase│  │
                     └────┬─────┘           └─────┬──────┘  │
                          │                       │         │
                     ┌────┴─────┐           ┌─────┴──────┐  │
                     │  Visit   │           │  Payment   │  │
                     └────┬─────┘           └─────┬──────┘  │
                          │                       │         │
                     ┌────┴─────────┐       ┌─────┴──────┐  │
                     │ Transaction  │       │ServiceOrder│  │
                     └────┬─────────┘       └─────┬──────┘  │
                          │                       │         │
                     ┌────┴─────┐           ┌─────┴──────┐  │
                     │ Document │           │  Service   │  │
                     └──────────┘           └────────────┘  │

                           ┌──────────────────┐              │
               ┌───────────│  Organization    │──────────────┘
               │           └────────┬─────────┘
               │                    │
          ┌────┴─────┐        ┌─────┴─────────┐
          │  OrgMem  │        │   Property    │
          └──────────┘        └──────┬────────┘
                                     │
                               ┌─────┴─────────┐
                               │     Media     │
                               └───────────────┘

  ┌──────────────────┐    ┌──────────────┐    ┌──────────────┐
  │ApprovalWorkflow  │    │   Incident   │1:1 │  Mediation   │
  └──────┬───────────┘    └──────────────┘    └──────────────┘
         │
    ┌────┴───────────┐
    │ GeographicUnit │  (self-ref: parent_id)
    └────────────────┘

  ┌──────────────────┐
  │ FinancingRequest │
  └──────┬───────────┘
         │
    ┌────┴───────────┐
    │    Event       │
    └────────────────┘
```

---

## 11. Cardinality Summary Table

| Entity A | Cardinality | Entity B | Key FK | Description |
|----------|-------------|----------|--------|-------------|
| User | 1:1 | AgentCredit | user_id | Agent credit balance |
| User | 1:1 | ProfessionalProfile | user_id | Professional profile |
| User | 1:N | OrganizationMember | user_id | Membership records |
| User | 1:N | Project | user_id | User projects |
| User | 1:N | Intent | user_id | User intents |
| User | 1:N | Lead (source) | user_id | Source leads |
| User | 1:N | Lead (assigned) | assigned_to_user_id | Assigned leads |
| User | 1:N | LeadPurchase | user_id | Lead purchases |
| User | 1:N | AgentInvitation | invited_by_user_id | Sent invitations |
| User | 1:N | ApprovalWorkflow (requester) | requester_user_id | Approval requests |
| User | 1:N | ApprovalWorkflow (reviewer) | reviewer_user_id | Reviews performed |
| User | 1:N | Incident (reporter) | reporter_user_id | Reported incidents |
| User | 1:N | Incident (assigned) | assigned_to_user_id | Assigned incidents |
| User | 1:N | Document (verifier) | verified_by_user_id | Verified documents |
| User | 1:N | IdentityResolution (reviewer) | reviewed_by_user_id | Reviewed resolutions |
| User | N:M | IdentityResolution (primary) | user_id_primary | Primary identity |
| User | N:M | IdentityResolution (duplicate) | user_id_duplicate | Duplicate identity |
| User | 1:N | Mediation (mediator) | mediator_user_id | Mediations handled |
| User | 1:N | Mediation (demandeur) | demandeur_user_id | Mediations as party |
| User | 1:N | Mediation (detenteur) | detenteur_user_id | Mediations as party |
| User | 1:N | FinancingRequest | user_id | Finance requests |
| Organization | 1:N | OrganizationMember | organization_id | Memberships |
| Organization | 1:N | Property | owner_organization_id | Owned properties |
| Organization | 1:N | Lead | organization_id | Assigned leads |
| Organization | 1:N | AgentInvitation | organization_id | Sent invitations |
| Organization | 1:N | Consent (recipient) | granted_to_organization_id | Received consents |
| OrganizationMember | N:1 | User | user_id | Member user |
| OrganizationMember | N:1 | Organization | organization_id | Parent org |
| Property | 1:N | Media | property_id | Property media |
| Property | 1:N | Visit | property_id | Property visits |
| Property | 1:N | Match | property_id | Property matches |
| Property | 1:N | Transaction | property_id | Property transactions |
| Project | 1:N | ProjectStep | project_id | Project steps |
| Project | 1:N | Match | project_id | Project matches |
| Project | 1:N | Visit | project_id | Project visits |
| Project | 1:N | Transaction | project_id | Project transactions |
| Project | N:1 | Intent | intent_id | Source intent |
| Intent | 1:N | Project | intent_id | Created projects |
| Match | N:1 | Project | project_id | Parent project |
| Match | N:1 | Property | property_id | Matched property |
| Match | 1:N | Visit | match_id | Triggered visits |
| Visit | N:1 | Project | project_id | Parent project |
| Visit | N:1 | Property | property_id | Visited property |
| Visit | N:1 | Match | match_id | Source match |
| Visit | N:1 | User (requester) | requested_by_user_id | Visit requester |
| Visit | N:1 | User (organizer) | organized_by_user_id | Organizing agent |
| Transaction | N:1 | Project | project_id | Parent project |
| Transaction | N:1 | Property | property_id | Transacted property |
| Transaction | N:1 | Visit | visit_id | Source visit |
| Transaction | 1:N | Document | transaction_id | Transaction docs |
| Transaction | 1:N | Payment | transaction_id | Transaction payments |
| Service | 1:N | ServiceOrder | service_id | Service orders |
| ServiceOrder | N:1 | Service | service_id | Ordered service |
| ServiceOrder | N:1 | User | user_id | Ordering user |
| ServiceOrder | N:1 | Organization | organization_id | Ordering org |
| ServiceOrder | N:1 | Property | property_id | Associated property |
| ServiceOrder | N:1 | Project | project_id | Associated project |
| ServiceOrder | N:1 | Payment | payment_id | Payment |
| Payment | N:1 | ServiceOrder | service_order_id | Parent order |
| Payment | N:1 | Transaction | transaction_id | Parent transaction |
| Payment | N:1 | User | user_id | Paying user |
| Lead | N:1 | User (source) | user_id | Source user |
| Lead | N:1 | User (assigned) | assigned_to_user_id | Assigned agent |
| Lead | N:1 | Organization | organization_id | Assigned org |
| Lead | N:1 | Property | property_id | Referenced property |
| Lead | N:1 | Project | project_id | Referenced project |
| Lead | N:1 | Conversation | source_conversation_id | Source conversation |
| Lead | 1:N | LeadPurchase | lead_id | Purchase records |
| LeadPurchase | N:1 | User | user_id | Purchasing agent |
| LeadPurchase | N:1 | Lead | lead_id | Purchased lead |
| LeadPurchase | N:1 | Organization | organization_id | Purchasing org |
| LeadPurchase | N:1 | Payment | payment_id | Payment |
| Document | N:1 | Transaction | transaction_id | Transaction docs |
| Document | N:1 | User (verifier) | verified_by_user_id | Verifier |
| Event | N:1 | User (actor) | actor_user_id | Triggering user |
| ApprovalWorkflow | N:1 | User (requester) | requester_user_id | Requestor |
| ApprovalWorkflow | N:1 | User (reviewer) | reviewer_user_id | Reviewer |
| Incident | N:1 | User (reporter) | reporter_user_id | Reporter |
| Incident | N:1 | User (assigned) | assigned_to_user_id | Handler |
| Incident | 1:1 | Mediation | incident_id | Mediation |
| Mediation | N:1 | User (mediator) | mediator_user_id | Mediator |
| Mediation | N:1 | User (demandeur) | demandeur_user_id | Party A |
| Mediation | N:1 | User (detenteur) | detenteur_user_id | Party B |
| Mediation | N:1 | Project | project_id | Related project |
| Mediation | N:1 | Transaction | transaction_id | Related transaction |
| AgentInvitation | N:1 | Organization | organization_id | Inviting org |
| AgentInvitation | N:1 | User (inviter) | invited_by_user_id | Inviting user |
| IdentityResolution | N:1 | User (primary) | user_id_primary | Kept identity |
| IdentityResolution | N:1 | User (duplicate) | user_id_duplicate | Merged identity |
| IdentityResolution | N:1 | User (reviewer) | reviewed_by_user_id | Reviewer |
| ProfessionalProfile | 1:1 | User | user_id | Profile owner |
| FinancingRequest | N:1 | User | user_id | Applicant |
| FinancingRequest | N:1 | Project | project_id | Related project |
| FinancingRequest | N:1 | Property | property_id | Related property |
| FinancingRequest | N:1 | User (reviewer) | reviewed_by_user_id | Reviewer |
| GeographicUnit | 1:N | GeographicUnit | parent_id | Parent-child |
| Consent | N:1 | User (grantor) | granted_by_user_id | Granting user |
| Consent | N:1 | User (grantee) | granted_to_user_id | Receiving user |
| Consent | N:1 | Organization (grantee) | granted_to_organization_id | Receiving org |
| Consent | N:1 | Project | project_id | Context project |

---

## 12. Polymorphic Relationships

| Entity | Discriminator Field | Target Types | Purpose |
|--------|-------------------|--------------|---------|
| Document | entity_type + entity_id | user, organization, property, transaction, project | Polymorphic document attachment |
| ApprovalWorkflow | target_type + target_id | organization, property, user, document | Generic approval system |
| Incident | target_type + target_id | user, property, transaction, organization | Incident target |
| Lead | property_id, project_id, source_conversation_id | property, project, conversation | Flexible lead source |

---

*End of ENTITY_RELATIONSHIP_MAP.md*
