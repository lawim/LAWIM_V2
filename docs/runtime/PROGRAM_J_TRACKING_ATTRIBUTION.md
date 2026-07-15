# Program J — Publication Tracking, Attribution and Conversion Foundation

**Document ID:** LAWIM-PROGRAM-J-TRACKING-V1
**Status:** CANONICAL
**Date:** 2026-07-15

---

## 1. Scope

J3 — Publication & Tracking Registry, J4 — Attribution Engine, J8A — Conversion Event Chain, delivered together.

### Exclusions

- Aggregated statistics dashboards
- Continuous Learning recommendations
- Full Feature Management Center
- AI agents
- New CRM/matching/payment business functions

---

## 2. External Channel Registry

| Code | Name | Provider |
|------|------|----------|
| FB | Facebook | facebook |
| WA | WhatsApp | green_api |
| TG | Telegram | telegram |
| IG | Instagram | — |
| TK | TikTok | — |
| EM | Email | — |
| SM | SMS | — |
| QR | QR Code | — |
| PS | Site partenaire | — |
| LW | LAWIM Web | — |
| MA | Application mobile | — |
| AG | Agence | — |
| AT | Agent | — |
| DR | Direct | — |
| OT | Autre | — |

---

## 3. Tracking Code Format

```
{CHANNEL_CODE}-LAWIM-{PUBLICATION_ID:06d}-{YEAR:04d}-{MONTH:02d}-{SEQ:03d}
```

| Segment | Description | Example |
|---------|-------------|---------|
| CHANNEL_CODE | 2-letter channel code | FB |
| LAWIM | Fixed prefix | LAWIM |
| PUBLICATION_ID | 6-digit zero-padded | 000128 |
| YEAR | 4-digit year | 2026 |
| MONTH | 2-digit month | 06 |
| SEQ | 3-digit sequence within month | 001 |

### Examples

```
FB-LAWIM-000128-2026-06-001
WA-LAWIM-000014-2026-06-014
TG-LAWIM-000045-2026-07-003
```

### Generation

`generate_tracking_code(channel_code, publication_seq, year, month, sequence)`

### Validation

`parse_tracking_code(code)` returns parsed segments or `None`.
`TrackingResolutionService.validate_tracking_code(code)` returns bool.

Codes are:
- **unique**: combination of all segments ensures global uniqueness
- **stable**: same inputs always produce same output
- **immutable**: never modified after publication
- **shareable**: human-readable, safe for URLs

---

## 4. External Campaign

| Attribute | Type | Description |
|-----------|------|-------------|
| campaign_id | str | UUID |
| campaign_code | str | Business code |
| campaign_name | str | Display name |
| campaign_type | str | social, email, etc. |
| campaign_objective | str | awareness, conversion, etc. |
| campaign_owner_actor_id | str | Reference to actor |
| organization_id | int? | Organization |
| status | CampaignStatus | DRAFT/ACTIVE/PAUSED/COMPLETED/CANCELLED/ARCHIVED |

---

## 5. External Publication

| Attribute | Type | Description |
|-----------|------|-------------|
| publication_id | str | UUID |
| tracking_code | str | Canonical tracking code |
| campaign_id | str | Parent campaign |
| channel_code | ExternalChannelCode | Published channel |
| actor_id | str | Publishing actor |
| actor_role_at_publication | str | Historical role snapshot |
| title | str | Publication title |
| content_reference | str | URL or reference |
| status | PublicationStatus | DRAFT/PUBLISHED/SCHEDULED/ARCHIVED/FAILED |

---

## 6. Redirect Log

Records each click/redirect event with:

- tracking_code, occurred_at, session_id
- device/browser/OS classification
- geo: country, city, lawim_zone
- bot detection, duplicate detection
- correlation_id for event chaining

---

## 7. Touchpoint

Types: IMPRESSION, CLICK, QR_SCAN, REDIRECT, CONVERSATION_OPEN, ACCOUNT_CREATION, QUALIFICATION, MATCHING, VISIT, TRANSACTION, PAYMENT, CONVERSION

Each touchpoint preserves:
- subject, channel, tracking_code, actor_id, actor_role_at_event
- occurred_at, correlation_id, deduplication_key

---

## 8. Lead Source

Reuses and extends existing `crm_lead_sources` with:
- tracking_code, campaign_id, publication_id, channel, actor_id
- first_touch_at, resolution_method, confidence

---

## 9. Attribution Models

### First Touch

Earliest touchpoint within the attribution window.

### Last Touch

Latest touchpoint within the attribution window.

### Multi-touch

Equal weight distributed across all touchpoints in window.

### LAWIM Attribution

Type-weighted and value-adjusted attribution:

| Touchpoint Type | Base Weight |
|-----------------|-------------|
| CONVERSATION_OPEN | 0.15 |
| QUALIFICATION | 0.10 |
| MATCHING | 0.10 |
| VISIT | 0.10 |
| REDIRECT/CLICK | 0.08-0.10 |
| ACCOUNT_CREATION | 0.10 |
| TRANSACTION/PAYMENT | 0.05 |
| IMPRESSION | 0.02 |

Weights are adjusted proportionally by touchpoint monetary value (capped at 2x).

---

## 10. Conversion Event Chain

Links: conversation → qualification → matching → visit → transaction → payment

Each ConversionEvent preserves:
- All upstream IDs (conversation, matching, visit, transaction, payment)
- tracking_code, actor_id with role at conversion
- monetary_value, currency
- deduplication_key for idempotency

---

## 11. Deduplication

- Tracking codes: format validation + uniqueness via segment combination
- Touchpoints: SHA-256 deduplication key (type + subject + timestamp + channel)
- Conversion events: SHA-256 deduplication key (conversation + matching + transaction + payment + type)
- Redirects: correlation_id + external_message_id (existing)

---

## 12. Feature Flags

| Flag | Default | Purpose |
|------|---------|---------|
| publication_tracking_enabled | false | Publication and tracking APIs |
| attribution_engine_enabled | false | Attribution calculation APIs |
| conversion_event_chain_enabled | false | Conversion chain APIs |

---

## 13. Public Contracts

### Tracking
- `GET tracking/channels` — list external channels
- `GET tracking/format` — tracking code format specification
- `GET tracking/validate/{code}` — validate tracking code
- `GET tracking/resolve/{code}` — resolve tracking code segments

### Attribution
- `GET attribution/models` — list attribution models

### Conversion
- `GET conversion/taxonomy` — list touchpoint types

---

## 14. Privacy

- No raw IP addresses stored in redirect logs (minimized metadata)
- Tracking codes do not contain personal information
- Actor roles are snapshotted, not live references
- Monetary values are stored without PII

---

## 15. Known Limitations

- No redirect short-link route implemented (requires server integration)
- Attribution currently calculates in-memory (no dedicated DB table)
- Conversion events are model-only (no dedicated DB table yet)
- Existing CRM campaigns and communication campaigns remain separate
- Email click/open tracking tables exist but are not populated
- No UTM parameter parsing for external URLs
