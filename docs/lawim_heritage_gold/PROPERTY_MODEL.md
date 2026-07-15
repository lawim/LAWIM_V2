# LAWIM Property Model — Certified Gold Reference

---

## Overview

This document captures the complete LAWIM property model: families, inheritance, workflow, attributes, lifecycle states, publication rules, pricing concepts, data quality scoring, and source reliability. All entries are sourced and confidence-rated.

---

## 1. Seven Property Families

| ID | Family | Code | Sub-referentiel | Source | Confidence |
|----|--------|------|-----------------|--------|------------|
| GOLD-PR-001 | Résidentiel | residential | Directive/02A-RESIDENTIAL-REFERENCE.md | Directive/02-PROPERTY-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-002 | Commercial | commercial | Directive/02B-COMMERCIAL-REFERENCE.md | Directive/02-PROPERTY-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-003 | Industriel | industrial | Directive/02C-INDUSTRIAL-REFERENCE.md | Directive/02-PROPERTY-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-004 | Foncier (Terrain) | land | Directive/02D-LAND-REFERENCE.md | Directive/02-PROPERTY-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-005 | Agricole | agricultural | Directive/02E-AGRICULTURAL-REFERENCE.md | Directive/02-PROPERTY-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-006 | Hôtelier | hotel | Directive/02F-HOTEL-REFERENCE.md | Directive/02-PROPERTY-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-007 | Projet immobilier | project | Directive/02G-PROJECT-REFERENCE.md | Directive/02-PROPERTY-REFERENCE.md, Ch.4 | HIGH |

---

## 2. Inheritance Principle

| ID | Concept | Description | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-PR-008 | Master model | All property types share a common master model; specialized rules per family are defined in sub-referentials only | Directive/02-PROPERTY-REFERENCE.md, Ch.2 | HIGH |
| GOLD-PR-009 | No duplication | It is forbidden to copy general rules into sub-referentials | Directive/02-PROPERTY-REFERENCE.md, Ch.2 | HIGH |
| GOLD-PR-010 | Common concepts | All properties share: family, type, operation, détenteur, status, availability, location, media, documentation, price, archiving, matching score | Directive/02-PROPERTY-REFERENCE.md, Ch.5 | HIGH |

---

## 3. Ten-Step Common Workflow

| ID | Step | Name | Description | Source | Confidence |
|----|------|------|-------------|--------|------------|
| GOLD-PR-011 | 1 | Réception | Reception or entry of property data | Directive/02-PROPERTY-REFERENCE.md, Ch.7 | HIGH |
| GOLD-PR-012 | 2 | Normalisation | Data normalization (currency, location, type) | Directive/02-PROPERTY-REFERENCE.md, Ch.7 | HIGH |
| GOLD-PR-013 | 3 | Classification | Family and type classification | Directive/02-PROPERTY-REFERENCE.md, Ch.7 | HIGH |
| GOLD-PR-014 | 4 | Validation | Consistency checks (type/family, operation/usage, location, price, documentation) | Directive/02-PROPERTY-REFERENCE.md, Ch.9 | HIGH |
| GOLD-PR-015 | 5 | Publication | Publication or hold based on completeness rules | Directive/02-PROPERTY-REFERENCE.md, Ch.8 | HIGH |
| GOLD-PR-016 | 6 | Matching | Compatibility scoring with user requests | Directive/02-PROPERTY-REFERENCE.md, Ch.10 | HIGH |
| GOLD-PR-017 | 7 | Mise en relation | Connection between demandeur and détenteur | Directive/02-PROPERTY-REFERENCE.md, Ch.7 | HIGH |
| GOLD-PR-018 | 8 | Suivi | Transaction follow-up | Directive/02-PROPERTY-REFERENCE.md, Ch.7 | HIGH |
| GOLD-PR-019 | 9 | Archivage | Archiving when sold, rented, withdrawn, or obsolete | Directive/02-PROPERTY-REFERENCE.md, Ch.11 | HIGH |
| GOLD-PR-020 | 10 | Conservation historique | Historical preservation for legal/audit purposes | Directive/02-PROPERTY-REFERENCE.md, Ch.7 | HIGH |

---

## 4. Thirteen Common Attributes

| ID | Attribute | Description | Source | Confidence |
|----|-----------|-------------|--------|------------|
| GOLD-PR-021 | famille_de_bien | Property family (residential, commercial, etc.) | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-022 | type_de_bien | Property type (apartment, house, etc.) | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-023 | opération_autorisée | Authorized transaction (rent, buy, sell, etc.) | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-024 | ville | City | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-025 | quartier_ou_zone | Neighborhood or zone | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-026 | coordonnées_gps | GPS coordinates or geographic reference | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-027 | disponibilité | Availability status | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-028 | état_de_publication | Publication state | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-029 | état_d_archivage | Archive state | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-030 | prix_ou_fourchette | Price or price range | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-031 | source_d_origine | Original source (agent, google_form, import, whatsapp) | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-032 | détenteur | Holder/owner of the property record | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |
| GOLD-PR-033 | documents_de_preuve | Supporting documents (title deed, etc.) | Directive/02-PROPERTY-REFERENCE.md, Ch.6 | HIGH |

---

## 5. Eleven Property Types (from property-qualification-reference.md)

| ID | Type | Family | Description | Source | Confidence |
|----|------|--------|-------------|--------|------------|
| GOLD-PR-034 | appartement | residential | Apartment | property-qualification-reference.md (legacy KNOWLEDGE/) | MEDIUM |
| GOLD-PR-035 | maison | residential | House | property-qualification-reference.md | MEDIUM |
| GOLD-PR-036 | villa | residential | Villa | property-qualification-reference.md | MEDIUM |
| GOLD-PR-037 | studio | residential | Studio | property-qualification-reference.md | MEDIUM |
| GOLD-PR-038 | duplex | residential | Duplex | property-qualification-reference.md | MEDIUM |
| GOLD-PR-039 | chambre | residential | Single room | property-qualification-reference.md | MEDIUM |
| GOLD-PR-040 | immeuble | residential | Apartment building | property-qualification-reference.md | MEDIUM |
| GOLD-PR-041 | terrain | land | Land plot | property-qualification-reference.md | MEDIUM |
| GOLD-PR-042 | boutique | commercial | Shop | property-qualification-reference.md | MEDIUM |
| GOLD-PR-043 | entrepôt | industrial | Warehouse | property-qualification-reference.md | MEDIUM |
| GOLD-PR-044 | bureau | commercial | Office | property-qualification-reference.md | MEDIUM |

---

## 6. Property Lifecycle State Machine

| ID | Concept | Description | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-PR-045 | States | 5 states: available, pending, rented, sold, archived | code/lawim_v2/property_domain.py (AVAILABILITY_STATUSES) | HIGH |
| GOLD-PR-046 | Transition: available→pending | Property enters transaction process | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-047 | Transition: available→archived | Direct archiving | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-048 | Transition: pending→rented | Rental confirmed | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-049 | Transition: pending→sold | Sale confirmed | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-050 | Transition: pending→available | Transaction cancelled | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-051 | Transition: pending→archived | Transaction failed | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-052 | Transition: rented→archived | Rental ended | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-053 | Transition: sold→archived | Sale finalized | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-054 | Transition: archived→available | Re-listing | property_lifecycle_engine.py (recovered) | HIGH |

### State Machine Diagram

```
available ──► pending ──► rented ──► archived
  │            │  │         │
  │            │  └──► sold ────► archived
  │            │
  └──► archived  └──► available
```

---

## 7. Auto-Archive After 90 Days

| ID | Concept | Description | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-PR-055 | Auto-archive trigger | 90 days of inactivity → auto-archive | property_lifecycle_engine.py (recovered): `auto_archive_expired(self, days=90)` | HIGH |
| GOLD-PR-056 | Rule | `if days_since_last_activity > 90: auto_archive()` | property_lifecycle_engine.py (recovered) | HIGH |

---

## 8. Property Status Display (Emoji + Label)

| ID | Status | Emoji | Label (FR) | Source | Confidence |
|----|--------|-------|------------|--------|------------|
| GOLD-PR-057 | available | 🏠 | Disponible | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-058 | pending | ⏳ | En cours de transaction | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-059 | rented | 🔑 | Loué | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-060 | sold | 💰 | Vendu | property_lifecycle_engine.py (recovered) | HIGH |
| GOLD-PR-061 | archived | 📦 | Archivé | property_lifecycle_engine.py (recovered) | HIGH |

---

## 9. Publication Rules

| ID | Rule | Description | Source | Confidence |
|----|------|-------------|--------|------------|
| GOLD-PR-062 | Family identified | Property must have a family | Directive/02-PROPERTY-REFERENCE.md, Ch.8 | HIGH |
| GOLD-PR-063 | Type coherent | Property type must be consistent with family | Directive/02-PROPERTY-REFERENCE.md, Ch.8 | HIGH |
| GOLD-PR-064 | Location known | Minimum location must be known | Directive/02-PROPERTY-REFERENCE.md, Ch.8 | HIGH |
| GOLD-PR-065 | Price provided | Price must be provided per pricing reference | Directive/02-PROPERTY-REFERENCE.md, Ch.8 | HIGH |
| GOLD-PR-066 | Détenteur identifiable | Holder must be identifiable | Directive/02-PROPERTY-REFERENCE.md, Ch.8 | HIGH |
| GOLD-PR-067 | Critical info normalized | All critical information must be normalized | Directive/02-PROPERTY-REFERENCE.md, Ch.8 | HIGH |
| GOLD-PR-068 | Documents present | Required documents must be present (per family) | Directive/02-PROPERTY-REFERENCE.md, Ch.8 | HIGH |
| GOLD-PR-069 | Code check | `can_publish()` checks: title, city, price exist; deleted_at is null | code/lawim_v2/property_domain.py:166-173 | HIGH |

---

## 10. Price Concepts (6 Levels)

| ID | Price Concept | Description | Source | Confidence |
|----|---------------|-------------|--------|------------|
| GOLD-PR-070 | Prix affiché | Displayed/listed price | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-071 | Prix négociable | Negotiable price | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-072 | Prix final | Final agreed price | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-073 | Estimation | Estimated value by engine or authorized actor | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-074 | Fourchette de marché | Market price range | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-075 | Historique de variation | Historical price variation series | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |

### Additional Price Types (from 02I-PRICING-REFERENCE.md)

| ID | Price Type | Context | Source | Confidence |
|----|------------|---------|--------|------------|
| GOLD-PR-076 | Loyer | Monthly rent | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-077 | Caution | Security deposit | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-078 | Avance | Rent advance | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-079 | Dépôt de garantie | Guarantee deposit | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-080 | Mensualité | Monthly payment | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-081 | Frais de service | Service fees (LAWIM) | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |
| GOLD-PR-082 | Taxes | Applicable taxes | Directive/02I-PRICING-REFERENCE.md, Ch.4 | HIGH |

---

## 11. Normalisation Rules

| ID | Rule | Description | Source | Confidence |
|----|------|-------------|--------|------------|
| GOLD-PR-083 | Currency | Every price must be associated with a currency (XAF, EUR, USD, GBP, XOF) | Directive/02I-PRICING-REFERENCE.md, Ch.5 | HIGH |
| GOLD-PR-084 | Period | Validity period if necessary | Directive/02I-PRICING-REFERENCE.md, Ch.5 | HIGH |
| GOLD-PR-085 | Source | Price source identification | Directive/02I-PRICING-REFERENCE.md, Ch.5 | HIGH |
| GOLD-PR-086 | Context | Business context for the price | Directive/02I-PRICING-REFERENCE.md, Ch.5 | HIGH |
| GOLD-PR-087 | Negotiation level | Negotiation stage indicator | Directive/02I-PRICING-REFERENCE.md, Ch.5 | HIGH |
| GOLD-PR-088 | History | Price change history | Directive/02I-PRICING-REFERENCE.md, Ch.5 | HIGH |
| GOLD-PR-089 | Free format conversion | Free formats must be converted to canonical representation | Directive/02I-PRICING-REFERENCE.md, Ch.5 | HIGH |

---

## 12. Pricing Expressions

| ID | Expression Pattern | Example | Source | Confidence |
|----|--------------------|---------|--------|------------|
| GOLD-PR-090 | Thousands (50k-500k) | "150k" → 150 000 FCFA | pricing_expressions.json (legacy KNOWLEDGE/) | MEDIUM |
| GOLD-PR-091 | Millions (1M-100M) | "5M" → 5 000 000 FCFA | pricing_expressions.json (legacy KNOWLEDGE/) | MEDIUM |
| GOLD-PR-092 | FCFA explicit | "100 000 FCFA" | pricing_expressions.json (legacy KNOWLEDGE/) | MEDIUM |
| GOLD-PR-093 | Range detection | "entre 100 et 200" → min=100000, max=200000 | pricing_expressions.json (legacy KNOWLEDGE/) | MEDIUM |
| GOLD-PR-094 | Negotiation terms | "à débattre", "négociable", "Prix à discuter" | pricing_expressions.json (legacy KNOWLEDGE/) | MEDIUM |

---

## 13. Property Data Quality Scoring

| ID | Concept | Description | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-PR-095 | Scoring formula | `quality_score = int(completeness * 0.6 + reliability * 0.4)` | data_quality_engine.py:76 (recovered) | HIGH |
| GOLD-PR-096 | Completeness weight | 60% of total score | data_quality_engine.py:76 (recovered) | HIGH |
| GOLD-PR-097 | Source reliability weight | 40% of total score | data_quality_engine.py:76 (recovered) | HIGH |

### Completeness Breakdown (60%)

| ID | Field | Weight | Condition | Source | Confidence |
|----|-------|--------|-----------|--------|------------|
| GOLD-PR-098 | Title | 10% | Present | data_quality_engine.py (recovered) | HIGH |
| GOLD-PR-099 | Description | 15% | >100 chars=15pts, >50=10pts, >20=5pts | data_quality_engine.py (recovered) | HIGH |
| GOLD-PR-100 | Price | 15% | Present | data_quality_engine.py (recovered) | HIGH |
| GOLD-PR-101 | Location | 15% | Present | data_quality_engine.py (recovered) | HIGH |
| GOLD-PR-102 | Property type | 15% | Present | data_quality_engine.py (recovered) | HIGH |
| GOLD-PR-103 | Images | 15% | Max 3pts/image, cap 15pts | data_quality_engine.py (recovered) | HIGH |

### Source Reliability Weights (40%)

| ID | Source | Reliability Score | Description | Source | Confidence |
|----|--------|-------------------|-------------|--------|------------|
| GOLD-PR-104 | agent | 90 | Professional real estate agent | data_quality_engine.py:19-25 (recovered) | HIGH |
| GOLD-PR-105 | google_form | 85 | Google Form submission | data_quality_engine.py:19-25 (recovered) | HIGH |
| GOLD-PR-106 | import | 70 | Bulk import | data_quality_engine.py:19-25 (recovered) | HIGH |
| GOLD-PR-107 | whatsapp | 50 | WhatsApp message | data_quality_engine.py:19-25 (recovered) | HIGH |
| GOLD-PR-108 | unknown | 30 | Unknown source | data_quality_engine.py:19-25 (recovered) | HIGH |

### Quality Grading Scale

| ID | Grade | Score Range | Icon | Source | Confidence |
|----|-------|-------------|------|--------|------------|
| GOLD-PR-109 | A+ | ≥ 80 | 🟢 | data_quality_engine.py:146-155 (recovered) | HIGH |
| GOLD-PR-110 | A | ≥ 60 | 🟢 | data_quality_engine.py:146-155 (recovered) | HIGH |
| GOLD-PR-111 | B | ≥ 40 | 🟡 | data_quality_engine.py:146-155 (recovered) | HIGH |
| GOLD-PR-112 | C | ≥ 20 | 🔴 | data_quality_engine.py:146-155 (recovered) | HIGH |
| GOLD-PR-113 | D | < 20 | 🔴 | data_quality_engine.py:146-155 (recovered) | HIGH |

---

## 14. Specific Fields per Category

| ID | Category | Fields | Source | Confidence |
|----|----------|--------|--------|------------|
| GOLD-PR-114 | Logement (residential) | rooms, bedrooms, bathrooms, floor, has_elevator, is_furnished | property_types.py:36 (SPECIFIC_FIELDS["logement"]) | HIGH |
| GOLD-PR-115 | Terrain (land) | surface, is_agricultural, is_constructible, has_water, has_electricity | property_types.py:37 | HIGH |
| GOLD-PR-116 | Commerce (commercial) | surface, front_window, parking_spots, has_signage | property_types.py:38 | HIGH |
| GOLD-PR-117 | Industriel (industrial) | access_camion, hauteur_sous_plafond, charge_sol, quai_chargement, puissance_electrique | Directive/02C-INDUSTRIAL-REFERENCE.md, Ch.3 | HIGH |

---

## 15. Minimum Fields for a Listing

| ID | Field | Requirement | Source | Confidence |
|----|-------|-------------|--------|------------|
| GOLD-PR-118 | Type de bien | Mandatory | minimum-fields-property.md (legacy KNOWLEDGE/) | MEDIUM |
| GOLD-PR-119 | Transaction | Mandatory | minimum-fields-property.md | MEDIUM |
| GOLD-PR-120 | Prix | Mandatory | minimum-fields-property.md | MEDIUM |
| GOLD-PR-121 | Ville | Mandatory | minimum-fields-property.md | MEDIUM |
| GOLD-PR-122 | Description | Mandatory | minimum-fields-property.md | MEDIUM |

---

*Certified Gold — 2026-07-15 — All entries sourced and confidence-rated.*
