# LAWIM — QA Dataset Catalog

**Document ID:** LAWIM-OPS-QA-DATA-V1  
**Status:** OPERATIONAL  
**Date:** 2026-07-15  
**Dataset Run ID:** QA-YYYYMMDD-HHMMSS (generated at seed time)

---

## Agencies

| Code | Name | City | Zone |
|------|------|------|------|
| QA-AG-01 | QA Agency 01 | Douala | Bonanjo |
| QA-AG-02 | QA Agency 02 | Yaoundé | Centre |

## Test Accounts (11)

See `LAWIM_QA_ACCOUNTS_REGISTER.md` for full list. All use `qa.*` login convention.

## Properties (10)

| Code | Type | City | Price (FCFA) | Status | Notes |
|------|------|------|-------------|--------|-------|
| DEMO-Studio-DLA | Studio | Douala | 15,000,000 | Available | Ground floor |
| DEMO-Apt-DLA | Apartment | Douala | 35,000,000 | Available | 3 bedrooms |
| DEMO-Villa-DLA | Villa | Douala | 80,000,000 | Reserved | Pool, garden |
| DEMO-Land-DLA | Land | Douala | 25,000,000 | Available | 500m², constructible |
| DEMO-Office-DLA | Office | Douala | 50,000,000 | Available | Bonanjo |
| DEMO-House-YDE | House | Yaoundé | 40,000,000 | Available | 4 bedrooms |
| DEMO-Apt-YDE | Apartment | Yaoundé | 25,000,000 | Available | 2 bedrooms |
| DEMO-Land-YDE | Land | Yaoundé | 15,000,000 | Available | 300m² |
| DEMO-Premium-Villa | Villa | Douala | 200,000,000 | Premium | Pool, 5 bedrooms |
| DEMO-Incomplete | Apartment | Douala | — | Incomplete | Missing price |

## Leads (4)

| Lead | Source | Status | Property |
|------|--------|--------|----------|
| qa.user.01 → Villa | Web | HOT | DEMO-Villa-DLA |
| WhatsApp lead | WhatsApp | WARM | DEMO-Apt-DLA |
| Facebook lead | Facebook | COLD | DEMO-Land-DLA |
| Incomplete lead | Telegram | DEAD | — |

## Conversations (4)

| Channel(s) | Participant | Agent Involved | Status |
|-----------|-------------|----------------|--------|
| WhatsApp | qa.user.01 | — | Active |
| Web → WhatsApp | qa.user.02 | qa.agent.agency01.01 | Active |
| Telegram | qa.agent.agency01.01 | — | Closed |
| AI Agent | qa.user.01 | AI (conversation) | Active |

## Qualifications (3)

| User | Property | Steps Completed | Status |
|------|----------|----------------|--------|
| qa.user.01 | DEMO-Villa-DLA | 10/10 | Completed |
| qa.user.02 | — | 5/10 | Partial |
| qa.user.02 | — | 2/10 | Abandoned |

## Matching (3)

| Demand | Offer | Score | Status |
|--------|-------|-------|--------|
| qa.user.01 villa | DEMO-Villa-DLA | 92/100 | Accepted |
| qa.user.02 apt | DEMO-Apt-DLA | 68/100 | Pending |
| qa.user.02 land | — | 0/100 | No results |

## Payments (sandbox)

| Reference | Amount | Provider | Status |
|-----------|--------|----------|--------|
| QA-PAY-001 | 500,000 | Campay sandbox | SUCCESS |
| QA-PAY-002 | 500,000 | Campay sandbox | FAILED |
| QA-PAY-003 | 500,000 | Campay sandbox | PENDING |

## Tracking

| Campaign | Channel | Code | Clicks | Conversions |
|----------|---------|------|--------|-------------|
| FB-QA-Camp-001 | Facebook | FB-LAWIM-999999-2026-07-001 | 12 | 2 |
| WA-QA-Camp-001 | WhatsApp | WA-LAWIM-999999-2026-07-001 | 8 | 1 |

## Reset

```bash
python3 scripts/qa/seed_qa_data.py --reset QA-YYYYMMDD-HHMMSS
```
