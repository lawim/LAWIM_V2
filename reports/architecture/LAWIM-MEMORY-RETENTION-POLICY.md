# LAWIM Memory Retention Policy

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 3 — Conversation Memory

## 1. RetentionCategories

| Category | Scope | Default Retention | Auto-Delete | Auto-Archive | Legal Exception |
|----------|-------|-------------------|-------------|--------------|-----------------|
| `TURN_MEMORY` | Per-turn conversation data | 7 days | Yes | No | No |
| `CONVERSATION_MEMORY` | Conversation state | 365 days | No | Yes | No |
| `CASE_MEMORY` | Business case dossiers | 1825 days (5 years) | No | Yes | No |
| `USER_PREFERENCE` | User preferences | 1825 days (5 years) | No | No | No |
| `RELATIONSHIP_MEMORY` | Relationship history | 1825 days (5 years) | No | No | No |
| `CONSENT_RECORD` | Consent records | 3650 days (10 years) | No | No | Yes |
| `HANDOVER_RECORD` | Handover snapshots | 1825 days (5 years) | No | Yes | No |
| `AUDIT_LOG` | Retention audit logs | 3650 days (10 years) | No | No | Yes |
| `TRANSACTION_RECORD` | Financial transactions | 3650 days (10 years) | No | No | Yes |

## 2. MemoryRetentionPolicy Defaults

| Setting | Default | Description |
|---------|---------|-------------|
| `retention_days` | 365 | Maximum age in days before action |
| `auto_archive` | False | Whether to archive before deletion |
| `auto_anonymize` | False | Whether to anonymize before deletion |
| `auto_delete` | False | Whether to delete automatically at expiry |
| `requires_approval` | False | Whether human approval is required |
| `legal_exception` | False | Exempt from deletion for legal reasons |
| `legal_exception_note` | "" | Reason for legal exception |

### Per-Category Overrides

```python
RETENTION_POLICIES = {
    TURN_MEMORY:         {retention_days: 7,    auto_delete: True},
    CONVERSATION_MEMORY: {retention_days: 365,  auto_archive: True, auto_anonymize: True},
    CASE_MEMORY:         {retention_days: 1825, auto_archive: True},
    USER_PREFERENCE:     {retention_days: 1825},
    RELATIONSHIP_MEMORY: {retention_days: 1825},
    CONSENT_RECORD:      {retention_days: 3650, legal_exception: True,
                          legal_exception_note: "Consent records retained for legal compliance"},
    HANDOVER_RECORD:     {retention_days: 1825, auto_archive: True},
    AUDIT_LOG:           {retention_days: 3650, legal_exception: True,
                          legal_exception_note: "Audit logs retained for legal compliance"},
    TRANSACTION_RECORD:  {retention_days: 3650, legal_exception: True,
                          legal_exception_note: "Transaction records retained for legal compliance"},
}
```

## 3. MemoryDeletionService

### Soft Delete

- Marks records with `deleted_at` timestamp
- Data remains in database but excluded from active queries
- Reversible by clearing `deleted_at`

### Hard Delete

- Permanently removes expired records from database
- Executed by `hard_delete_expired(category, before_date)`
- All deletions are audited

```python
# Soft delete
service.soft_delete("conversation_states", record_id, "User requested deletion")

# Hard delete expired
service.hard_delete_expired(RetentionCategory.TURN_MEMORY, cutoff_date)
```

## 4. MemoryAnonymizationService

Replaces personally identifiable information with masked tokens:

| Input | Output |
|-------|--------|
| `"+237690000000"` | `[ANONYMIZED-1]` |
| `"Douala"` | `[ANONYMIZED-2]` |
| `"john@email.com"` | `[ANONYMIZED-3]` |

- Consistent mapping within a single anonymization session
- `anonymize_actor_data(actor_id)` — anonymizes all records for an actor
- `is_anonymized(value)` — checks if a value is already masked

## 5. Legal Exceptions

Records with `legal_exception = True` are NEVER automatically deleted:

- **Consent records**: retained for regulatory compliance (10 years)
- **Audit logs**: retained for legal and security auditing (10 years)
- **Transaction records**: retained for financial compliance (10 years)

These categories require manual review for any deletion.

## 6. Audit Logging

All destructive operations write a `RetentionAuditLog`:

| Field | Description |
|-------|-------------|
| `log_id` | UUID |
| `action` | `SOFT_DELETE`, `HARD_DELETE`, `ANONYMIZE` |
| `category` | Retention category (e.g. `TURN_MEMORY`) |
| `target_id` | Record UUID |
| `actor` | Who performed the action (`system`, `admin`, `user`) |
| `reason` | Why the action was performed |
| `performed_at` | ISO 8601 timestamp |
| `details` | JSON metadata |

Audit logs are stored in `retention_audit_logs` table with 10-year retention.
