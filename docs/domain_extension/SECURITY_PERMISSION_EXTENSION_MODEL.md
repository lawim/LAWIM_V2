# SECURITY & PERMISSION EXTENSION MODEL

**Document ID:** LAWIM-EXT-SEC-V1
**Status:** DRAFT — Extension to LAWIM_UNIFIED_DOMAIN_MODEL.md (Domain 13)
**Date:** 2026-07-15

---

## Table of Contents

1. [Overview & Extension Classification](#1-overview--extension-classification)
2. [4-Level Permission Model](#2-4-level-permission-model)
3. [Permission Matrix (Role × Resource)](#3-permission-matrix-role--resource)
4. [Permission Scope](#4-permission-scope)
5. [ApprovalWorkflow Entity Definition](#5-approvalworkflow-entity-definition)
6. [Consent Management Model](#6-consent-management-model)
7. [Permission Audit Logging](#7-permission-audit-logging)
8. [Temporary Permission Grants](#8-temporary-permission-grants)
9. [Organization-Level Permission Hierarchy](#9-organization-level-permission-hierarchy)
10. [Permission Derivation from Consent](#10-permission-derivation-from-consent)
11. [Relationship-Based Permissions](#11-relationship-based-permissions)

---

## 1. Overview & Extension Classification

### 1.1 Extension Categories

| Category | Definition | Examples |
|----------|-----------|----------|
| **System permissions** | Global platform-wide permissions granted by role | System config access, user management, approval authority |
| **Organization permissions** | Permissions scoped within an organization, determined by agency_role | Org property management, agent lead assignment |
| **Relationship permissions** | Permissions derived from relational proximity between entities | Property owner access, project participant edit |
| **Transaction permissions** | Permissions granted by participation in a transaction workflow | Sign transaction, upload deal documents |
| **Consent-derived permissions** | Permissions that activate upon explicit consent from another party | Contact revelation after double consent |
| **Temporary permissions** | Time-bound permission grants with automatic revocation | Delegated authority, time-limited access |

### 1.2 CRUD-VSRA Operations

Each extension defines who can perform the following operations:

| Operation | Code | Description |
|-----------|------|-------------|
| Create | C | Create a new instance |
| Read | R | View/access the resource |
| Modify | M | Modify/update existing instance |
| Delete | D | Delete/remove instance |
| Validate | V | Approve/reject or verify correctness |
| Share | S | Grant access to another party |
| Revoke | Rv | Remove previously granted access |
| Audit | A | View audit trail/history |

### 1.3 Source References

| Source | Description |
|--------|-------------|
| `LAWIM_UNIFIED_DOMAIN_MODEL.md §14` | Domain 13: Permission/Security Model |
| `required_extensions.json §permission_model` | EXT-PERM-001 through EXT-PERM-004 |
| `ROLE_CROSSWALK.md` | Role hierarchy and agency structure |
| `GOLD-RL-014` through `GOLD-RL-017` | Gold permission levels |

---

## 2. 4-Level Permission Model

### 2.1 Permission Levels

| Level | Code | Description | Implicit Rights |
|-------|------|-------------|-----------------|
| Read | R | View/can access the resource | — |
| Create | C | Create new instances of the resource | — |
| Edit | E | Modify existing instances | R (must read to edit) |
| Approve | A | Approve/reject actions on the resource | R, E (must review to approve) |

### 2.2 Permission Hierarchy

```
Approve (A)
  └─ Edit (E)
       └─ Read (R)
```

Create (C) is independent — a role may Create without Read (e.g., submit a form).

### 2.3 Permission Types by Extension Category

| Extension Category | Applicable Levels | Notes |
|--------------------|-------------------|-------|
| System permissions | A (system config), R (system health) | Only admin level |
| Organization permissions | R, C, E, A | Scoped by org membership |
| Relationship permissions | R, C, E | Derived from relationship proximity |
| Transaction permissions | R, C, E, A | Scoped to transaction parties |
| Consent-derived permissions | R (contact data) | Conditional on consent |
| Temporary permissions | R, C, E | Time-bound |

---

## 3. Permission Matrix (Role × Resource)

### 3.1 V2 Official Roles

| Role | Description |
|------|-------------|
| admin | Full system access |
| manager | Organizational management |
| operator | Operational staff |
| partner | External partner (notaire, géomètre, etc.) |
| user | End user (demandeur, propriétaire, etc.) |

### 3.2 Complete Permission Matrix

| Resource \ Role | admin | manager | operator | partner | user |
|-----------------|-------|---------|----------|---------|------|
| **Property (own)** | RCEA | RCEA | RCEA | RCE | RCE |
| **Property (org)** | RCEA | RCEA | RCEA | R | — |
| **Property (all)** | RCEA | R | — | — | — |
| **Project (own)** | RCEA | RCEA | RCEA | RCEA | RCEA |
| **Project (org)** | RCEA | RCEA | RCEA | R | — |
| **Project (all)** | RCEA | R | — | — | — |
| **Transaction (own)** | RCEA | RCEA | RCE | — | — |
| **Transaction (org)** | RCEA | RCEA | R | — | — |
| **Transaction (all)** | RCEA | R | — | — | — |
| **User (own)** | RCEA | RCEA | RCE | RCE | RCE |
| **User (org)** | RCEA | RCEA | R | R | — |
| **User (all)** | RCEA | R | — | — | — |
| **Organization (own)** | RCEA | RCE | — | — | — |
| **Organization (all)** | RCEA | — | — | — | — |
| **OrganizationMember** | RCEA | RCEA | R | R | — |
| **Service** | RCEA | RCEA | RCEA | RCE | R |
| **ServiceOrder** | RCEA | RCEA | RCE | RCE | RCE |
| **Payment** | RCEA | RCEA | R | — | — |
| **Lead** | RCEA | RCEA | RCE | RCE | — |
| **LeadPurchase** | RCEA | RCEA | RCE | — | — |
| **Document (own)** | RCEA | RCEA | RCEA | RCEA | RCEA |
| **Document (org)** | RCEA | RCEA | RCEA | RCE | — |
| **Document (all)** | RCEA | RCE | — | — | — |
| **Visit** | RCEA | RCEA | RCEA | RCE | R (own) |
| **Match** | RCEA | RCEA | RCEA | R | R (own) |
| **Conversation** | RCEA | RCEA | RCEA | RCE | RCE (own) |
| **Negotiation** | RCEA | RCEA | RCEA | RCE | R (own) |
| **AgentCredit** | RCEA | RCEA | R | — | — |
| **Lead (zone assignment)** | RCEA | RCEA | RCE | — | — |
| **CRM settings** | RCEA | RA | — | — | — |
| **System config** | A | — | — | — | — |
| **ApprovalWorkflow** | RCEA | RA | R | R | R (own) |
| **Consent record** | RCEA | RCEA | RCE | RCE | RCE (own) |
| **PermissionAuditLog** | RCEA | RA | R | — | — |
| **TemporaryPermission** | RCEA | RCEA | RCE | — | — |
| **Permission grant** | RCEA | RCEA | RCE | — | — |
| **Event/Audit** | RCEA | RCEA | R | — | — |

### 3.3 Agency Hierarchy Role Implications

The agency_role (responsible > admin > agent > assistant) acts as a **sub-role** within the organization scope. It further refines permissions for resources scoped by `organization_id`:

| Agency Role | Permission Implication |
|-------------|----------------------|
| **responsible** | Full org permissions (RCEA across all org resources) |
| **admin** | RCEA on org resources except org settings (RCE) |
| **agent** | RCE on own resources + R on org resources |
| **assistant** | R on org resources, CE on assigned resources only |

---

## 4. Permission Scope

### 4.1 Scope Levels

| Scope | Code | Description |
|-------|------|-------------|
| Own | own | Resources owned by or assigned to the user |
| Managed | managed | Resources under user's management/responsibility (e.g., team leads) |
| Organization | org | Resources belonging to user's organization |
| All | all | All resources in the system (admin only) |

### 4.2 Scope Resolution Logic

```
function resolvePermission(user, resource, required_level):
  if user.role == admin → always ALL scope
  if user owns resource → OWN scope applies
  if user manages resource (team lead, project lead) → MANAGED scope applies
  if resource.organization_id == user.organization_id → ORG scope applies
  otherwise → no permission (unless relationship-derived)
```

### 4.3 Scope Mapping by Resource

| Resource | Own (owner/creator) | Managed (assignee/lead) | Organization | All |
|----------|--------------------|------------------------|--------------|-----|
| Property | owner_id == user | agent_id == user | org match | admin |
| Project | creator_id == user | assigned_agent == user | org match | admin |
| Transaction | demandeur_id/holder_id | agent_id == user | org match | admin |
| Document | uploaded_by == user | — | org match | admin |
| Lead | — | routed_to_agent == user | org match | admin |
| Visit | demandeur_id/holder_id | agent_id == user | — | admin |
| Conversation | participant | — | — | admin |
| Organization | — | responsible == user | member | admin |

---

## 5. ApprovalWorkflow Entity Definition

### 5.1 Entity: ApprovalWorkflow

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `approval_type` | Enum | `agency_creation \| listing_validation \| professional_verification \| organization_validation \| refund_approval \| account_suspension \| account_deletion \| permission_grant \| temporary_permission \| document_validation \| transaction_validation \| lead_purchase_refund` |
| `target_type` | String | Entity type being approved |
| `target_id` | UUID | Entity ID being approved |
| `requested_by` | UUID | User requesting approval |
| `assigned_to` | UUID | Approver user |
| `status` | Enum | `pending \| approved \| rejected \| cancelled \| escalated` |
| `reviewed_by` | UUID? | Reviewer who acted |
| `reviewed_at` | DateTime? | Review timestamp |
| `approval_notes` | Text? | Approver notes |
| `rejection_reason` | String? | Reason if rejected |
| `escalated_to` | UUID? | Escalated approver |
| `escalated_at` | DateTime? | Escalation timestamp |
| `escalation_reason` | String? | Reason for escalation |
| `approval_deadline` | DateTime? | SLA deadline for approval |
| `sla_breached` | Boolean | Whether SLA was breached |
| `auto_approve_on_timeout` | Boolean | Whether to auto-approve on timeout |
| `created_at` | DateTime | Creation timestamp |

### 5.2 Approval Routing Rules

| Approval Type | Assigned To | Escalation Path | Deadline |
|---------------|-------------|-----------------|----------|
| agency_creation | admin | — | 48h |
| listing_validation | operator → manager | manager → admin | 24h |
| professional_verification | manager | manager → admin | 72h |
| organization_validation | admin | — | 48h |
| refund_approval | manager | manager → admin | 24h |
| account_suspension | manager | manager → admin | 12h |
| account_deletion | admin | — | 72h |
| permission_grant | manager | manager → admin | 24h |
| temporary_permission | operator → manager | manager → admin | 4h |
| document_validation | operator | operator → manager | 24h |
| transaction_validation | manager | manager → admin | 48h |

### 5.3 CRUD-VSRA by Role (ApprovalWorkflow)

| Operation | admin | manager | operator | partner | user |
|-----------|-------|---------|----------|---------|------|
| Create | ✓ | ✓ | ✓ | ✓ | ✓ (own) |
| Read | ✓ | ✓ | ✓ | ✓ | ✓ (own) |
| Modify | ✓ | ✓ (assigned) | — | — | — |
| Delete | ✓ | — | — | — | — |
| Validate | ✓ | ✓ (assigned) | ✓ (assigned) | — | — |
| Share | ✓ | ✓ | — | — | — |
| Revoke | ✓ | ✓ | — | — | — |
| Audit | ✓ | ✓ | ✓ | — | — |

---

## 6. Consent Management Model

### 6.1 Entity: Consent

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `consent_type` | Enum | `data_sharing \| contact_revelation \| lead_routing \| marketing \| gdpr_processing \| double_consent_demandeur \| double_consent_holder \| agent_opt_in \| data_retention \| third_party_sharing` |
| `granted_by` | UUID | User giving consent |
| `granted_to` | UUID? | User/organization receiving consent |
| `target_type` | String? | Entity type consent relates to (Property, Project, User) |
| `target_id` | UUID? | Entity ID |
| `status` | Enum | `active \| revoked \| expired \| superseded` |
| `scope` | Enum | `single_use \| limited \| ongoing \| permanent` |
| `expires_at` | DateTime? | Consent expiration |
| `revoked_at` | DateTime? | When consent was revoked |
| `revoked_by` | UUID? | Who revoked (self or admin) |
| `consent_channel` | Enum | `whatsapp \| telegram \| dashboard \| api \| in_app` |
| `consent_proof` | JSON? | Audit proof (timestamp, IP, device) |
| `terms_version` | String | Version of terms consented to |
| `created_at` | DateTime | Consent grant timestamp |

### 6.2 Consent Types and Derivation Rules

| Consent Type | Derives Permission | Default | Revocable |
|-------------|-------------------|---------|-----------|
| data_sharing | Read basic profile data for matching | Required | Yes |
| contact_revelation | Read contact details (phone, email) | Required | Yes |
| lead_routing | Receive leads as agent | Opt-in | Yes |
| marketing | Receive marketing communications | Opt-in | Yes |
| gdpr_processing | Process personal data | Required | Limited |
| double_consent_demandeur | Contact demandeur | Explicit step | Yes |
| double_consent_holder | Contact holder | Explicit step | Yes |
| agent_opt_in | Agent accepts lead assignment | Required | Yes |
| data_retention | Retain data after account closure | Required | Limited |
| third_party_sharing | Share data with partners | Opt-in | Yes |

### 6.3 CRUD-VSRA by Role (Consent)

| Operation | admin | manager | operator | partner | user |
|-----------|-------|---------|----------|---------|------|
| Create | ✓ | ✓ | ✓ | — | ✓ (own) |
| Read | ✓ | ✓ | ✓ | ✓ (related) | ✓ (own) |
| Modify | ✓ | — | — | — | ✓ (own) |
| Delete | ✓ | — | — | — | — |
| Validate | ✓ | ✓ | ✓ | — | — |
| Share | ✓ | ✓ | ✓ | — | — |
| Revoke | ✓ | ✓ | — | — | ✓ (own) |
| Audit | ✓ | ✓ | ✓ | — | ✓ (own) |

---

## 7. Permission Audit Logging

### 7.1 Entity: PermissionAuditLog

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `event_type` | Enum | `permission_granted \| permission_revoked \| permission_denied \| permission_escalated \| role_changed \| scope_changed \| consent_granted \| consent_revoked \| temporary_grant_issued \| temporary_grant_expired \| temporary_grant_revoked \| approval_requested \| approval_granted \| approval_rejected \| approval_escalated \| breach_detected \| sharing_activated \| sharing_deactivated` |
| `actor_id` | UUID | User who performed the action |
| `target_user_id` | UUID? | User affected |
| `resource_type` | String | Resource type affected |
| `resource_id` | UUID? | Resource ID |
| `permission_level` | Enum? | R \| C \| E \| A |
| `permission_scope` | Enum? | own \| managed \| org \| all |
| `previous_state` | JSON? | Previous permission state |
| `new_state` | JSON? | New permission state |
| `grant_source` | Enum | `role_inherited \| org_role \| relationship \| consent \| temporary_grant \| direct_assignment \| system_default` |
| `reason` | String? | Reason for change |
| `ip_address` | String? | Request origin IP |
| `user_agent` | String? | Request user agent |
| `session_id` | UUID? | Session identifier |
| `correlation_id` | UUID? | Link to related events |
| `created_at` | DateTime | Event timestamp |

### 7.2 Audit Retention Policy

| Event Type | Retention | Purpose |
|-----------|-----------|---------|
| permission_granted | 5 years | Security audit trail |
| permission_revoked | 5 years | Security audit trail |
| permission_denied | 1 year | Intrusion detection |
| consent_granted | 5 years | GDPR compliance |
| consent_revoked | 5 years | GDPR compliance |
| temporary_grant | 2 years | Operational audit |
| approval events | 3 years | Compliance |
| breach_detected | 1 year | Security monitoring |

### 7.3 CRUD-VSRA by Role (PermissionAuditLog)

| Operation | admin | manager | operator | partner | user |
|-----------|-------|---------|----------|---------|------|
| Create | ✓ (system) | — | — | — | — |
| Read | ✓ | ✓ (org scope) | ✓ (own scope) | — | — |
| Modify | — | — | — | — | — |
| Delete | — | — | — | — | — |
| Validate | ✓ | — | — | — | — |
| Share | ✓ | ✓ | — | — | — |
| Revoke | — | — | — | — | — |
| Audit | ✓ | ✓ | ✓ | — | — |

---

## 8. Temporary Permission Grants

### 8.1 Entity: TemporaryPermission

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `granted_by` | UUID | Admin/manager who granted |
| `granted_to` | UUID | User receiving permission |
| `resource_type` | String | Resource type |
| `resource_id` | UUID? | Specific resource (null = all of type) |
| `permission_level` | Enum | `read \| create \| edit \| approve` |
| `permission_scope` | Enum | `own \| managed \| org \| all` |
| `reason` | String | Business reason |
| `starts_at` | DateTime | Grant start time |
| `expires_at` | DateTime | Auto-revoke time |
| `max_extensions` | Int | Maximum re-grants (default 0) |
| `extension_count` | Int | Number of times extended |
| `status` | Enum | `active \| expired \| revoked \| extended` |
| `revoked_at` | DateTime? | If revoked early |
| `revoked_by` | UUID? | Who revoked |
| `revocation_reason` | String? | Revocation reason |
| `created_at` | DateTime | Grant creation |

### 8.2 Temporary Grant Scenarios

| Scenario | Permission | Duration | Approval Required |
|----------|-----------|----------|-------------------|
| Delegation (manager away) | Edit org resources | 7 days | Manager self-service |
| Emergency access | Read all resources | 4 hours | Admin approval |
| Time-limited agent role | Edit assigned leads | 30 days | Manager approval |
| Cross-org collaboration | Read specific project | 14 days | Both org admins |
| Auditor access | Read org data | 90 days | Admin approval |
| Support access | Edit user data | 24 hours | Manager approval |

### 8.3 CRUD-VSRA by Role (TemporaryPermission)

| Operation | admin | manager | operator | partner | user |
|-----------|-------|---------|----------|---------|------|
| Create | ✓ | ✓ | — | — | — |
| Read | ✓ | ✓ (org) | ✓ (own) | — | — |
| Modify | ✓ | ✓ (own grants) | — | — | — |
| Delete | ✓ | — | — | — | — |
| Validate | ✓ | ✓ | — | — | — |
| Share | ✓ | ✓ | — | — | — |
| Revoke | ✓ | ✓ | ✓ (own) | — | — |
| Audit | ✓ | ✓ | ✓ (own) | — | — |

---

## 9. Organization-Level Permission Hierarchy

### 9.1 Agency Role Hierarchy

```
responsible (highest)
  └─ admin
       └─ agent
            └─ assistant (lowest)
```

| Agency Role | Scope | Can Assign | Can Approve | Permissions Over |
|-------------|-------|------------|-------------|------------------|
| **responsible** | org | admin, agent, assistant | org actions | all org resources |
| **admin** | org | agent, assistant | agent actions | org resources (except org settings) |
| **agent** | own + assigned | — | — | own resources, assigned leads |
| **assistant** | assigned only | — | — | assigned tasks only |

### 9.2 Permission Mapping: Agency Role × V2 Role

| V2 Role \ Agency Role | responsible | admin | agent | assistant |
|------------------------|-------------|-------|-------|-----------|
| admin | Full org control | Full org control | — | — |
| manager | Org management | Org management | — | — |
| operator | Operational + org | Operational + org | Operational only | Read-only assigned |
| partner | Read org resources | Read org resources | Own resources | — |
| user | — | — | — | — |

### 9.3 CRUD-VSRA by Agency Role

| Operation | responsible | admin | agent | assistant |
|-----------|-------------|-------|-------|-----------|
| Create | ✓ org-wide | ✓ org-wide | ✓ own | — |
| Read | ✓ org-wide | ✓ org-wide | ✓ own + assigned | ✓ assigned |
| Modify | ✓ org-wide | ✓ org-wide | ✓ own | ✓ assigned |
| Delete | ✓ org-wide | — | — | — |
| Validate | ✓ org-wide | ✓ assigned | — | — |
| Share | ✓ org-wide | ✓ org-wide | — | — |
| Revoke | ✓ org-wide | ✓ org-wide | — | — |
| Audit | ✓ org-wide | ✓ org-wide | ✓ own | ✓ assigned |

---

## 10. Permission Derivation from Consent

### 10.1 Consent-to-Permission Mapping

| Consent Type | Derives Permission | Condition | Duration |
|-------------|-------------------|-----------|----------|
| data_sharing | Read basic profile | Consent active | While active |
| double_consent_demandeur | Read demandeur contact | Both consents obtained | Single use |
| double_consent_holder | Read holder contact | Both consents obtained | Single use |
| contact_revelation | Read full contact details | Payment + consent | Per lead |
| agent_opt_in | Receive lead assignment | Consent + availability | Ongoing |
| lead_routing | Access lead data | Agent opt-in + assignment | Ongoing |
| gdpr_processing | Process personal data | Must be active | While required |
| marketing | Send communications | Must be active | While active |
| data_retention | Retain data after deactivation | Must be active | Retention period |
| third_party_sharing | Share with partners | Explicit + active | Per partner |

### 10.2 Permission Derivation Rules

1. **Double consent** — Contact data is revealed only after both demandeur and holder have explicitly consented. Prior to that, only anonymized/aggregate data is visible.
2. **Lead purchase** — Agent can read lead contact only after purchasing the lead (payment processed) and lead owner consent is active.
3. **Agent opt-in cascade** — Agent must opt in to receive leads → triggers zone assignment → enables lead routing → enables lead data access.
4. **GDPR override** — If gdpr_processing consent is revoked, all derived permissions are immediately suspended.
5. **Consent revocation cascade** — Revoking a consent type revokes all permissions derived from it and triggers audit logging.

### 10.3 CRUD-VSRA by Consent Derivation

| Derived Permission | Create | Read | Modify | Delete | Validate | Share | Revoke | Audit |
|--------------------|--------|------|--------|--------|----------|-------|--------|-------|
| Contact read (double consent) | System (on consent) | Both parties + agent | — | — | — | — | Consent revocation | System |
| Lead data access | System (on purchase) | Purchasing agent | — | — | — | — | Lead close | System |
| Profile read (data sharing) | User (consent) | Matched parties | — | — | — | — | Consent revocation | System |
| Agent lead assignment | System (on routing) | Assigned agent | Agent (opt-out) | — | Manager | Manager | Manager | System |

---

## 11. Relationship-Based Permissions

### 11.1 Relationship Types and Permission Mapping

| Relationship | Source | Target | Derived Permissions |
|-------------|--------|--------|---------------------|
| Property owner | User (owner_id) | Property | RCE (full control over property) |
| Property agent | User (agent_id) | Property | RCE (management) |
| Project creator | User (creator_id) | Project | RCEA (full control) |
| Project assignee | User (assigned_agent) | Project | RCE (management) |
| Transaction demandeur | User (demandeur_id) | Transaction | RCE (participant) |
| Transaction holder | User (holder_id) | Transaction | RCE (participant) |
| Transaction agent | User (agent_id) | Transaction | RCEA (management) |
| Visit demandeur | User (demandeur_id) | Visit | R (own participation) |
| Visit holder | User (holder_id) | Visit | R (own participation) |
| Visit agent | User (agent_id) | Visit | RCE (management) |
| Conversation participant | User | Conversation | RCE (own conversations) |
| Document uploader | User (uploaded_by) | Document | RCE (own documents) |
| Lead agent | User (routed_to_agent) | Lead | RCE (assigned lead) |
| Organization membership | User (org member) | Organization resources | Per agency_role |
| Approval requester | User (requested_by) | ApprovalWorkflow | R (own request) |
| Consent granter | User (granted_by) | Consent | RCE (own consent) |
| Organization responsible | User (agency_role=responsible) | Organization | RCEA (full control) |

### 11.2 Relationship Distance and Permission Strength

| Distance | Definition | Permission Strength | Example |
|----------|-----------|-------------------|---------|
| **Direct** | Explicit FK relationship | Full RCE/A as defined | owner → property |
| **Assigned** | Explicit assignment | RCE (management) | agent → lead |
| **Participant** | Party to workflow | R ± E (contextual) | demandeur → transaction |
| **Org member** | Same organization | Per agency_role | agent → org properties |
| **Consent-derived** | Via consent chain | R (conditional) | matched user → profile |
| **Public** | No relationship | R (public data) | visitor → published property |

### 11.3 Relationship Graph for Permission Resolution

```
User
  ├── Direct: owns Property, creates Project, uploads Document
  ├── Assigned: manages Property (agent), assigned Lead, assigned Visit
  ├── Participant: Transaction party, Visit party, Conversation participant
  ├── Organizational: OrganizationMember → org resources
  ├── Consent-derived: via Consent → matched resources
  └── Role-inherited: V2 role → system-wide permissions
```

### 11.4 CRUD-VSRA by Relationship Type

| Relationship | Create | Read | Modify | Delete | Validate | Share | Revoke | Audit |
|-------------|--------|------|--------|--------|----------|-------|--------|-------|
| Direct (owner) | ✓ | ✓ | ✓ | ✓ | — | ✓ (transfer) | — | ✓ |
| Assigned (agent) | ✓ (on behalf) | ✓ | ✓ | — | — | — | — | ✓ |
| Participant | — | ✓ | ✓ (contextual) | — | — | — | — | ✓ |
| Org member | ✓ (scope-limited) | ✓ (scope-limited) | ✓ (scope-limited) | — | — | — | — | ✓ (scope) |
| Consent-derived | — | ✓ (conditional) | — | — | — | — | ✓ (consent) | — |
| Public | — | ✓ (public data) | — | — | — | — | — | — |

---

## Appendix A: Extension Summary

| Extension ID | Concept | Category | Priority | Source |
|-------------|---------|----------|----------|--------|
| EXT-PERM-001 | Approve permission level (Niveau 4) | System | P1 | GOLD-RL-017 |
| EXT-PERM-002 | Read permission level (Niveau 1) | System | P2 | GOLD-RL-014 |
| EXT-PERM-003 | Create permission level (Niveau 2) | System | P2 | GOLD-RL-015 |
| EXT-PERM-004 | Edit permission level (Niveau 3) | System | P2 | GOLD-RL-016 |
| EXT-PERM-005 | Permission matrix (Role × Resource) | System | P1 | Domain 13 §14.3 |
| EXT-PERM-006 | Permission scope (own/managed/org/all) | System | P2 | Domain 13 §14.3 |
| EXT-PERM-007 | ApprovalWorkflow entity | System | P1 | Domain 13 §14.4 |
| EXT-PERM-008 | Consent management model | System | P1 | Domain 13 §14.5 |
| EXT-PERM-009 | Permission audit logging | System | P1 | Domain 15 §16 |
| EXT-PERM-010 | Temporary permission grants | System | P2 | EXT-PERM-004 derived |
| EXT-PERM-011 | Organization permission hierarchy | Organization | P1 | EXT-RL-AGENCY-007 |
| EXT-PERM-012 | Permission derivation from consent | Consent-derived | P2 | Domain 13 §14.5 |
| EXT-PERM-013 | Relationship-based permissions | Relationship | P2 | Domain 13 implicit |
| EXT-PERM-014 | Agency role permissions (responsible/admin/agent/assistant) | Organization | P2 | EXT-RL-AGENCY-007 |
| EXT-PERM-015 | System configuration permissions | System | P1 | Domain 13 §14.3 |
| EXT-PERM-016 | Transaction permission scoping | Transaction | P1 | Domain 13 §14.3 |

## Appendix B: Permission Inheritance Chain

```
System permission (V2 role: admin/manager/operator/partner/user)
  └─ Organization permission (agency_role: responsible/admin/agent/assistant)
       └─ Relationship permission (direct/assigned/participant/org)
            └─ Consent-derived permission (conditional on consent)
                 └─ Temporary permission (time-bound override)
```

Each level adds constraints. A user's effective permission is the **intersection** of all applicable levels.

## Appendix C: Deny-by-Default Policy

1. All permissions default to **deny** unless explicitly granted.
2. Permission resolution follows **first-match-wins** with explicit deny taking precedence.
3. Unlisted resources in the permission matrix default to **admin-only**.
4. Scope narrowing always takes precedence: if matrix says `RCEA` but scope says `own`, effective scope is `own`.
5. Temporary permissions expire automatically at `expires_at` — no manual revocation needed.
6. Consent revocation immediately invalidates all derived permissions.
7. All permission denials at resource access time MUST be logged to `PermissionAuditLog`.
