# RELEASE PROGRAM K — Communication • Notification • Omnichannel Platform

## Phase 0 — Cartographie

### Réutilisation (sans duplication)

| Existant | Stratégie Program K |
|----------|---------------------|
| `notifications` (core v1) | Façade legacy ; transport via plateforme K |
| `crm_*_messages` (Program H) | Enregistrements CRM ; envoi délégué à K |
| `automation_notifications` (F) | Pont événementiel |
| `ecosystem_notifications` (B) | Pont événementiel |
| `contact.py` | Handles officiels `@lawimofficial`, `@lawim_assistant_bot` |
| `events` / `record_event()` | Bus grossier ; `communication_events` pour payload riche |
| `risk_alerts` (J) | Source `SecurityAlertRaised`, pas de duplication |

### Interdictions respectées

- Aucun connecteur SMTP/SMS/WhatsApp/Telegram/Push réel
- Routes `/api/notifications`, `/api/conversations/*`, `/api/v2/crm/*` inchangées
- Programs A–J non modifiés (extension mixin uniquement)

## Schema v17 — 81 tables

Communication Core (10), Notification (10), Email (10), SMS (6), WhatsApp (7), Telegram (4), Push (5), In-App (4), Campaigns (8), Queue (5), Templates (4), Preferences (5), Analytics (3).

## Package `code/lawim_v2/communication/`

22 fichiers : `schema_v17_ddl.py`, `engines.py`, `repository.py`, `service.py`, `dto.py`, modules canal (`email.py`, `sms.py`, `whatsapp.py`, `telegram.py`, `push.py`), `queue.py`, `notifications.py`, `campaigns.py`, `templates.py`, `preferences.py`, `analytics.py`, `integrations.py`.

## API `/api/v2/communication/*`

Messages, channels, conversations, history, groups, events, templates, preferences, campaigns, notifications, email/sms/whatsapp/telegram/push/inapp, queue, statistics, dashboard, analytics, reports, search, export/import, integrations, health.

## Observabilité

`communication_requests_total` + compteurs détaillés (`communication_messages_total`, `email_messages_total`, etc.) via `/api/metrics`.

## Tests

`tests/test_release_program_k.py` — 412 tests, 11 classes.
