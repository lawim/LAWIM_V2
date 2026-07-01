# RELEASE PROGRAM I — Marketplace • Partner Ecosystem • Service Provider Platform

**Programme :** RELEASE PROGRAM I  
**Date :** 2026-07-01  
**Branche :** `develop/2.0-intelligent-platform`  
**Tag :** `release-program-i`  
**Schema :** v15  
**Prérequis :** Programs A–H (gelés, sans régression)

---

## 1. Résumé exécutif

RELEASE PROGRAM I transforme LAWIM_V2 en **écosystème immobilier numérique ouvert** : marketplace intelligent, annuaire professionnel, catalogue de prestations, demandes/devis/contrats/missions, réputation, litiges, abonnements et commissions — orchestrant les moteurs A–H sans duplication.

**1300+ tests** passent.

---

## 2. Architecture

Package : `code/lawim_v2/marketplace/`

Extension de Program B (`partner_profiles`, `service_catalog`) via FK — routes `/api/v2/partners` et `/api/v2/services` **inchangées**.

Nouvelles routes : `/api/v2/marketplace/*`

Préfixe tables : `marketplace_*` (30 tables, schema v15).

---

## 3. Domaines métier

| Domaine | Implémentation |
|---------|----------------|
| Partner Management | `marketplace_partner_registrations` → `partner_profiles` |
| Professional Directory | `marketplace_provider_profiles` + certifications + portfolio |
| Service Catalog | `marketplace_catalog_*` + lien `service_catalog` |
| Service Requests | `marketplace_service_requests` + documents |
| Quotation Engine | `marketplace_quotes` + quote_lines |
| Contract Management | `marketplace_contracts` + workflow F |
| Mission Management | missions, milestones, deliverables |
| Availability | `marketplace_availability` |
| Reputation & Reviews | reviews, moderation, reputation snapshots |
| Disputes | disputes + messages + workflow |
| Subscriptions | plans + subscriptions |
| Commissions | rules + commissions |
| Payment Preparation | `marketplace_payment_preparations` (sans paiement réel) |
| Matching | sessions + results (A–H engines) |

---

## 4. Intégrations A–H

| Programme | Usage Marketplace |
|-----------|-------------------|
| A | Projects, policy, intelligent core |
| B | `partner_profiles`, `service_catalog`, `/api/v2/partners` |
| C | Cognition decisions |
| D | Assistant marketplace |
| E | RAG certifications/réglementations |
| F | Workflow contrats/missions/litiges |
| G | REI property_id sur demandes/missions |
| H | CRM contact_id, Customer 360 |

---

## 5. API v2 marketplace

Endpoints : partners, providers, catalog, requests, quotes, contracts, missions, reviews, reputation, matching, recommendations, commissions, subscriptions, disputes, analytics, dashboard, stats, payments/prepare, integrations.

---

## 6. Observabilité

`marketplace_requests_total` + métriques détaillées via `crm_metrics` dict (prefixes marketplace_*, partner_*, provider_*, etc.).

---

## 7. Compatibilité

Programs A–H : aucune régression. Program B ecosystem routes préservées.
