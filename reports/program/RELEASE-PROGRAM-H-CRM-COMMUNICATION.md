# RELEASE PROGRAM H — CRM • Customer Experience • Communication Platform

**Programme :** RELEASE PROGRAM H  
**Date :** 2026-07-01  
**Branche :** `develop/2.0-intelligent-platform`  
**Tag :** `release-program-h`  
**Schema :** v14  
**Prérequis :** Programs A–G (gelés, sans régression)

---

## 1. Résumé exécutif

RELEASE PROGRAM H livre en une seule release :

1. **Phase 0** — Normalisation globale des contacts officiels LAWIM (source unique `code/lawim_v2/contact.py`)
2. **Phase 1** — Plateforme CRM complète (leads, contacts, clients, pipelines, communications omnicanales, campagnes, scoring, satisfaction, Customer 360°)

Intégration complète avec les programmes A–G. **1000+ tests** passent.

---

## 2. Phase 0 — Normalisation des contacts

### Source officielle unique

Fichier : `code/lawim_v2/contact.py`

| Constante | Valeur officielle |
|-----------|-------------------|
| `COMPANY_NAME` | LAWIM |
| `PHONE_NUMBER` | 686 822 667 |
| `WHATSAPP_NUMBER` / `GREEN_API_NUMBER` | 686 822 667 |
| `FACEBOOK_USERNAME` | @lawimofficial |
| `WHATSAPP_USERNAME` | @lawimofficial |
| `TELEGRAM_BOT` | @lawim_assistant_bot |
| `DEFAULT_COUNTRY` | Cameroon |

### Propagation

- `bootstrap_payload` inclut `official_contact`
- API publique : `GET /api/v2/crm/official-contact`
- Communications CRM utilisent exclusivement `contact.py`
- Documentation branding mise à jour (`documentation/branding/FACEBOOK_PAGE_REFERENCE_V1.md`)
- **Aucune occurrence** de l'ancien numéro officiel supprimé dans le dépôt (validation automatisée)

---

## 3. Architecture CRM

Package : `code/lawim_v2/crm/`

```
CRM Platform
├── Lead / Contact / Customer / Opportunity management
├── Sales Pipeline (configurable, compatible Workflow F)
├── Communication Center (WhatsApp, Telegram, Email, SMS)
├── Campaign & Segmentation engines
├── Customer 360° + Journey + Timeline
├── Scoring + Satisfaction (NPS)
└── AI Integration Bridge → Programs A–G
```

Préfixe tables : `crm_*` (31 tables, schema v14).

---

## 4. Schema v14

31 tables : contacts, leads, customers, opportunities, pipelines, communications (whatsapp/telegram/email/sms), reminders, followups, campaigns, segments, scores, satisfaction, notes, documents, AI suggestions, analytics.

Tables v1–v13 **intactes**.

---

## 5. API v2 CRM

Base : `/api/v2/crm/*`

Endpoints : contacts, leads, customers, organizations (via existing), opportunities, pipelines, journeys, timelines, communications, whatsapp, telegram, email, sms, reminders, followups, campaigns, analytics, dashboard, scoring, satisfaction, notes, search, official-contact.

---

## 6. Interface administration

Panel **Customer Relationship Management** dans `static/index.html` / `static/app.js` : stats CRM, contacts, recherche, contacts officiels LAWIM.

---

## 7. Observabilité

Compteurs CRM via `crm_*`, `lead_*`, `contact_*`, `customer_*`, `campaign_*`, `communication_*`, `whatsapp_*`, `telegram_*`, `email_*`, `sms_*`, `followup_*`, `journey_*`, `pipeline_*`, `analytics_*` dans `observability.py` (`crm_metrics` dict + `crm_requests_total`).

---

## 8. Compatibilité Programs A–G

Tous les tests de non-régression passent. CRM réutilise workflow automation, knowledge platform, real estate intelligence, assistant, cognition, ecosystem sans doublon fonctionnel.

---

## 9. Tests

- `tests/test_release_program_h.py` : 281 tests Program H
- Tests normalisation contacts (scan repo anti-legacy)
- Total suite : **1000+ tests**
