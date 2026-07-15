# Residential Search Qualification Matrices — LAWIM Heritage Gold

**Document ID:** LAWIM-GOLD-MATRICES-RESIDENTIAL-SEARCH-V1
**Mission:** LAWIM Heritage Gold — Qualification des demandes de recherche résidentielle
**Date:** 2026-07-15
**Statut:** CANONICAL — Reference document for architecture H1
**Principe:** Matrices exhaustives et validées pour chaque type de bien résidentiel LAWIM

---

# Table of Contents

| # | Property Type | Matrix ID | Transaction Types |
|---|---------------|-----------|-------------------|
| 1 | chambre_simple | MATRIX-RES-SEARCH-001 | RENT |
| 2 | chambre_moderne | MATRIX-RES-SEARCH-002 | RENT |
| 3 | studio | MATRIX-RES-SEARCH-003 | RENT |
| 4 | studio_moderne | MATRIX-RES-SEARCH-004 | RENT |
| 5 | studio_meuble | MATRIX-RES-SEARCH-005 | RENT |
| 6 | appartement_non_meuble | MATRIX-RES-SEARCH-006 | RENT, BUY |
| 7 | appartement_meuble | MATRIX-RES-SEARCH-007 | RENT, BUY |
| 8 | villa | MATRIX-RES-SEARCH-008 | RENT, BUY |
| 9 | villa_basse | MATRIX-RES-SEARCH-009 | RENT, BUY |
| 10 | duplex | MATRIX-RES-SEARCH-010 | RENT, BUY |
| 11 | triplex | MATRIX-RES-SEARCH-011 | RENT, BUY |
| 12 | maison_individuelle | MATRIX-RES-SEARCH-012 | RENT, BUY |
| 13 | maison_de_ville | MATRIX-RES-SEARCH-013 | RENT, BUY |
| 14 | chambre_hotel | MATRIX-RES-SEARCH-014 | RENT (short-term) |
| 15 | appartement_courte_duree | MATRIX-RES-SEARCH-015 | RENT (short-term) |
| 16 | residence_meublee | MATRIX-RES-SEARCH-016 | RENT (short-term, long-term) |
| 17 | colocation | MATRIX-RES-SEARCH-017 | RENT |
| 18 | cite_universitaire | MATRIX-RES-SEARCH-018 | RENT |

---

# Common Rules for All Residential Search Matrices

## Qualification Order

All matrices follow this qualification order, per LAWIM heritage (QUALIFICATION_MODEL.md §5):

| Order | Step | Field(s) |
|:-----:|------|----------|
| 1 | Intention | FLD-TRANSACTION, FLD-INTENT |
| 2 | Type de bien | FLD-PROPERTY_TYPE |
| 3 | Ville | FLD-CITY |
| 4 | Quartier | FLD-NEIGHBORHOOD, FLD-ZONE |
| 5 | Budget | FLD-BUDGET_MAX, FLD-BUDGET_TYPE |
| 6 | Délai | FLD-DISPONIBILITE, FLD-DELAI |
| 7 | Critères spécifiques au type | Per-matrix fields |
| 8 | Préférences | Per-matrix optional fields |
| 9 | Confirmation | Récapitulatif |
| 10 | Escalade | Décision: résultats, visite, transfert humain |

## Channel Adaptation Rules

| Channel | Pace | Format | Reference |
|---------|------|--------|-----------|
| WhatsApp | 1 question per message | Minimal, mobile-first | CONVERSATION_MODEL.md §2 |
| Telegram | 2-3 fields per message | Structured with lists | CONVERSATION_MODEL.md §2 |
| Dashboard | Full form | Complete and actionable | QUALIFICATION_MODEL.md §7 |

## Universal Stop Criteria

Qualification stops early when:
- The city is not covered by LAWIM's active workflow
- Inventory is empty for the given criteria
- User explicitly asks for a human agent
- Thread becomes repetitive (3 exchanges without progress)
- User changes intention mid-qualification

## Progressive Qualification Principle

From QUALIFICATION_MODEL.md §8 and DOMAIN_MODEL.md §10:

1. **One question at a time** on WhatsApp, 2-3 on Telegram
2. **Never re-ask** a field already collected
3. **Correction replaces** — user correction overrides previous value
4. **Deduce, don't ask** — never ask what can be derived
5. **Match early** — launch search as soon as MINIMUM_SEARCH_READY is achieved
6. **Budget is blocking** — no matching without budget (QUALIFICATION_MODEL.md §2.2, qualification-implementation-backlog.md)

## Matching Role Semantics

| Role | Description | Example |
|------|-------------|---------|
| hard_constraint | Must match exactly; otherwise excluded | city, transaction |
| soft_constraint | Strong preference but flexible; penalized if not matched | neighborhood, chambres |
| ranking_preference | Used to rank results only | etage, balcony |
| exclusion | Properties matching this are excluded | previously rejected |
| boost | Score boost if matched (+10 to +25) | exact_neighborhood +25 |
| penalty | Score penalty if not matched | missing_budget -10 |
| informational_only | For display/recommendation only, does not affect score | nom, email |
| verification_only | For transaction readiness only | telephone |
| transaction_blocker | Must be resolved before transaction | caution, financing |

## Source Status Definitions

| Status | Meaning |
|--------|---------|
| HERITAGE_VALIDATED | Explicit rule from LAWIM heritage documents |
| HERITAGE_NORMALIZED | Normalized from multiple heritage sources |
| EXTERNAL_CONFIRMED | Confirmed by non-LAWIM sources (market research) |
| EXPERT_PROPOSAL | Proposed by domain expert (not from heritage) |
| HUMAN_VALIDATION_REQUIRED | Needs human review before production use |

## Common Forbidden Questions (All Matrices)

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Avez-vous un autre critère important à ajouter ?" | Question vide, inefficace |
| 2 | "Comme le nombre de pièces ou le standing ?" | Suggestive, biaise la réponse |
| 3 | "Quel est votre standing souhaité ?" | Standing doit être déduit du budget/quartier |
| 4 | "Combien de pièces ?" | "Pièces" est ambigu au Cameroun, utiliser "chambres" |
| 5 | "Quelle est votre fourchette de prix exacte ?" | Budget maximum suffit |
| 6 | "Avez-vous des critères supplémentaires ?" | Trop vague |
| 7 | "Quel type de résidence ?" | Déjà couvert par le type de bien |
| 8 | "Avez-vous une préférence pour le propriétaire ?" | Hors scope de qualification |
| 9 | "Quel est votre revenu mensuel ?" | Trop intrusif, non nécessaire |
| 10 | "Pourquoi cherchez-vous un nouveau logement ?" | Hors scope |
| 11 | "Avez-vous déjà visité des biens ?" | Non pertinent pour la qualification |
| 12 | "Quel est votre quartier actuel ?" | Non nécessaire pour la recherche |

## Register of Validated Field IDs (Master Catalog)

The following table defines every field used across all 18 matrices. Each matrix references these FIELD-IDs and provides matrix-specific overrides where applicable.

| FIELD-ID | label | data_type | allowed_values | privacy | source | confidence |
|----------|-------|-----------|----------------|--------|--------|------------|
| FLD-TRANSACTION | Transaction | enum | RENT, BUY | public | HERITAGE_VALIDATED | HIGH |
| FLD-INTENT | Intention | enum | RENT_PROPERTY, BUY_PROPERTY, INVESTOR_INTENT | public | HERITAGE_VALIDATED | HIGH |
| FLD-PROPERTY_TYPE | Type de bien | enum | 18 residential types | public | HERITAGE_VALIDATED | HIGH |
| FLD-CITY | Ville | string | LAWIM city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-NEIGHBORHOOD | Quartier | string | Per-city neighborhood list | public | HERITAGE_VALIDATED | HIGH |
| FLD-ZONE | Zone | string | Free text | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-BUDGET_MAX | Budget maximum | integer | Positive integer | private | HERITAGE_VALIDATED | HIGH |
| FLD-BUDGET_MIN | Budget minimum | integer | Positive integer < BUDGET_MAX | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-BUDGET_TYPE | Type de budget | enum | MONTHLY_RENT, TOTAL_PRICE, PRICE_PER_NIGHT, PRICE_PER_SQM | private | HERITAGE_VALIDATED | HIGH |
| FLD-BUDGET_CURRENCY | Devise | enum | XAF, EUR, USD, GBP, XOF | private | HERITAGE_VALIDATED | HIGH |
| FLD-BUDGET_NEGOTIABLE | Négociable | boolean | true, false | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DISPONIBILITE | Disponibilité | date | Date or relative | private | HERITAGE_VALIDATED | HIGH |
| FLD-DELAI | Délai | enum | IMMEDIATE, <1_MONTH, 1-3_MONTHS, 3-6_MONTHS, NO_RUSH | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-URGENCE | Urgence | enum | URGENT, MODERATE, NOT_URGENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CHAMBRES | Chambres | integer | 1-10+ | public | HERITAGE_VALIDATED | HIGH |
| FLD-DOUCHES | Douches | integer | 1-5+ | public | HERITAGE_VALIDATED | HIGH |
| FLD-SALONS | Salons | integer | 0-5 | public | HERITAGE_VALIDATED | HIGH |
| FLD-CUISINE | Cuisine | enum | INTERNE, EXTERNE, EQUIPEE, NON_EQUIPEE, INDIFFERENT | public | HERITAGE_VALIDATED | HIGH |
| FLD-MEUBLE | Meublé | enum | MEUBLE, NON_MEUBLE, SEMI_MEUBLE, INDIFFERENT | public | HERITAGE_VALIDATED | HIGH |
| FLD-SURFACE | Surface habitable | integer | 10-1000 | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-SURFACE_TERRAIN | Surface terrain | integer | 50-10000 | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-ETAGE | Étage | enum | REZ_DE_CHAUSSEE, BAS, MILIEU, HAUT, TOIT_TERRASSE, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-ASCENSEUR | Ascenseur | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PARKING | Parking | enum | OUI, NON, INDIFFERENT, GARAGE | public | HERITAGE_VALIDATED | HIGH |
| FLD-COUR | Cour | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CLOTURE | Clôture | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DEPENDANCES | Dépendances | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-BALCON | Balcon | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-JARDIN | Jardin | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PISCINE | Piscine | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CLIMATISATION | Climatisation | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-FORAGE | Forage | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-INTERNET | Internet | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-SECURITE | Sécurité | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-GARDIENNAGE | Gardiennage | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | LOW |
| FLD-EAU | Eau | enum | PERMANENTE, INTERMITTENTE, FORAGE, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-ELECTRICITE | Électricité | enum | PERMANENTE, INTERMITTENTE, GROUPE, SOLAIRE, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CHARGES | Charges | enum | INCLUSES, NON_INCLUSES, PARTIELLES | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-ACCES_ROUTE | Accès route | enum | GOUDRONNEE, PISTE, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CAUTION | Caution | integer | Positive integer | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-FINANCING | Financement | enum | CASH, LOAN, MORTGAGE, ASSISTANCE | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-NOM | Nom | string | Free text | private | HERITAGE_VALIDATED | HIGH |
| FLD-TELEPHONE | Téléphone | string | Valid phone | private | HERITAGE_VALIDATED | HIGH |
| FLD-EMAIL | Email | string | Valid email | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CANAL_PREFERE | Canal préféré | enum | WHATSAPP, TELEGRAM, SMS, EMAIL, APPEL | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LANGUE | Langue | enum | FRANCAIS, ANGLAIS, PIDGIN | private | HERITAGE_VALIDATED | HIGH |
| FLD-PROXIMITY_PREFERENCES | Proximité | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-MOBILITY | Mobilité | enum | STRICT, FLEXIBLE, VERY_FLEXIBLE | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-USAGE | Usage | enum | RESIDENCE, INVESTISSEMENT, MIXTE | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DUREE_LOCATION | Durée location | enum | COURT_TERME, MOYEN_TERME, LONG_TERME, INDIFFERENT | private | EXPERT_PROPOSAL | LOW |
| FLD-DUREE_SEJOUR | Durée séjour | enum | NUIT, WEEKEND, SEMAINE, 2_SEMAINES, MOIS, LONG_SEJOUR | public | HERITAGE_VALIDATED | HIGH |
| FLD-NOMBRE_PERSONNES | Nombre personnes | integer | 1-20 | public | HERITAGE_NORMALIZED | HIGH |
| FLD-PETIT_DEJEUNER | Petit-déjeuner | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-MENAGE | Ménage | boolean | true, false, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-SERVICES_INCLUS | Services inclus | string | Free text | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LINGE | Linge | boolean | true, false, INDIFFERENT | public | EXPERT_PROPOSAL | LOW |
| FLD-GENRE_PREFERENCE | Préférence genre | enum | MIXTE, HOMMES, FEMMES, INDIFFERENT | sensitive | HERITAGE_NORMALIZED | HIGH |
| FLD-AGE_RANGE | Tranche d'âge | string | Free text | sensitive | EXPERT_PROPOSAL | LOW |
| FLD-NOMBRE_COLOCATAIRES | Nombre colocataires | integer | 2-10 | public | HERITAGE_NORMALIZED | HIGH |
| FLD-ESPACES_PARTAGES | Espaces partagés | string | Free text | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-REGLEMENT_INTERIEUR | Règlement intérieur | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-UNIVERSITE | Université | string | Free text | public | EXPERT_PROPOSAL | HIGH |
| FLD-TYPE_CHAMBRE_UNIV | Type chambre univ. | enum | INDIVIDUELLE, PARTAGEE_2, PARTAGEE_3_PLUS, INDIFFERENT | public | EXPERT_PROPOSAL | HIGH |
| FLD-ANNEE_ETUDES | Année d'études | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-RESTAURATION | Restauration | boolean | true, false, INDIFFERENT | public | EXPERT_PROPOSAL | LOW |
| FLD-BOURSE | Bourse | boolean | true, false | sensitive | EXPERT_PROPOSAL | LOW |
| FLD-DATE_ARRIVEE | Date d'arrivée | date | Valid date | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DATE_DEPART | Date de départ | date | Valid date after arrival | private | HERITAGE_NORMALIZED | MEDIUM |

---

## Derived Fields (Used Across All Matrices)

These fields are deduced by the system, never asked directly.

| FIELD-ID | label | Derivation Rule | matching_role | confidence |
|----------|-------|-----------------|---------------|------------|
| FLD-DERIVED-STANDING | Standing estimé | Deduced from budget + quartier + property type | informational_only | MEDIUM |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | Compare budget vs market data per type/neighborhood | verification_only | MEDIUM |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | Deduced from delai + message language | ranking_preference | LOW |
| FLD-DERIVED-PROFIL_ACHETEUR | Profil acheteur | Deduced from transaction + language + budget | informational_only | LOW |
| FLD-DERIVED-PRIX_M2_ESTIME | Prix au m² estimé | budget / surface (when both available) | informational_only | LOW |
| FLD-DERIVED-COMPATIBILITE | Compatibilité quartier | Derived from budget + type + quartier market data | verification_only | LOW |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier context | informational_only | LOW |
| FLD-DERIVED-PROFIL | Profil demandeur | message language + references + budget | informational_only | LOW |

---


## MATRIX 1: chambre_simple

### matrix_id
MATRIX-RES-SEARCH-001

### canonical_name
Chambre Simple — Basic Room

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT

### property_or_service_type
chambre_simple

### requester_typology
tenant

### journey_stage
SEARCH

### description
Qualification matrix for a basic single room (chambre simple) rental search. A chambre simple is the most basic residential unit — a single room without internal private bathroom or kitchen. The tenant shares common facilities (douche, cuisine) with other occupants. This is the most affordable rental option in Cameroon, common in quartiers populaires.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget mensuel maximum pour le loyer ?" | 50 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOUCHES | Douche | always | "Préférez-vous une douche interne ou externe à la chambre ?" | 45 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-MEUBLE | Meublé | always | "Vous cherchez une chambre meublée ou non meublée ?" | 75 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CUISINE | Cuisine | if not specified | "Avez-vous besoin d'une cuisine ?" | 52 |
| FLD-CLIMATISATION | Climatisation | hot city | "Climatisation nécessaire ?" | 67 |
| FLD-EAU | Eau | not specified | "Accès à l'eau important ?" | 68 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CAUTION | Caution | always | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | always | "Charges incluses ?" | 73 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-SECURITE | Sécurité | soft_constraint | 74 |
| FLD-ACCES_ROUTE | Accès route | ranking_preference | 76 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-BALCON | Balcon | ranking_preference |
| FLD-FORAGE | Forage | boost (+10) |
| FLD-EMAIL | Email | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-SURFACE | if user mentions size | informational_only |
| FLD-INTERNET | if user mentions digital work | boost (+15) |
| FLD-GROUPE_ELECTROGENE | city in high power-cut zone | boost (+10) |
| FLD-MOBILITY | if multiple neighborhoods | soft_constraint |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-EMAIL | Personal contact |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Chambre simple = 1 chambre par définition |
| 2 | "Combien de salons ?" | Non applicable pour une chambre simple |
| 3 | "À quel étage ?" | Non pertinent pour chambre simple |
| 4 | "Besoin de parking ?" | Rarement applicable |
| 5 | "Quel standing ?" | Doit être déduit du budget/quartier |
| 6 | "Combien de pièces ?" | Terminologie non canonique au Cameroun |

---

## MATRIX 2: chambre_moderne

### matrix_id
MATRIX-RES-SEARCH-002

### canonical_name
Chambre Moderne — Modern Room with Private Shower

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT

### property_or_service_type
chambre_moderne

### requester_typology
tenant

### journey_stage
SEARCH

### description
Qualification matrix for a modern room (chambre moderne) rental search. A chambre moderne is an upgraded room with private internal shower (douche interne) and often a kitchenette. Unlike chambre simple, the bathroom is private. Popular among young professionals and students with modest budgets.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget mensuel maximum ?" | 50 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOUCHES | Douche | always | "Douche interne (privée) ou partagée ?" | 45 |
| FLD-CUISINE | Cuisine | always | "Kitchenette ou cuisine équipée ?" | 52 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-MEUBLE | Meublé | always | "Meublée ou non meublée ?" | 75 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CLIMATISATION | Climatisation | hot city | "Climatisation nécessaire ?" | 67 |
| FLD-EAU | Eau | not specified | "Eau courante importante ?" | 68 |
| FLD-ELECTRICITE | Électricité | not specified | "Électricité importante ?" | 69 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CAUTION | Caution | always | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | always | "Charges incluses ?" | 73 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-INTERNET | Internet | ranking_preference | 66 |
| FLD-SECURITE | Sécurité | soft_constraint | 74 |
| FLD-ACCES_ROUTE | Accès route | ranking_preference | 76 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-SURFACE | Surface | informational_only | 64 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-BALCON | Balcon | ranking_preference |
| FLD-EMAIL | Email | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-FORAGE | water-scarce city | boost (+10) |
| FLD-GROUPE_ELECTROGENE | frequent power cuts | boost (+10) |
| FLD-MOBILITY | multiple zones | soft_constraint |
| FLD-ETAGE | if building with floors | ranking_preference |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-EMAIL | Personal contact |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Chambre = 1 chambre par définition |
| 2 | "Combien de salons ?" | Rarement applicable |
| 3 | "Besoin de parking ?" | Rarement applicable |
| 4 | "Quel standing ?" | Déduire du budget/quartier |
| 5 | "Combien de pièces ?" | Terminologie non canonique |

---

## MATRIX 3: studio

### matrix_id
MATRIX-RES-SEARCH-003

### canonical_name
Studio — Basic Studio Apartment

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT

### property_or_service_type
studio

### requester_typology
tenant

### journey_stage
SEARCH

### description
Qualification matrix for a basic studio apartment rental search. A studio is a self-contained unit combining bedroom, living area, and kitchenette in one open space, with a separate bathroom (douche). Budget-friendly option for singles and students.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget mensuel maximum ?" | 50 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOUCHES | Douche | always | "La douche est-elle interne (privée) ?" | 45 |
| FLD-CUISINE | Cuisine | always | "Kitchenette ou cuisine séparée ?" | 52 |
| FLD-MEUBLE | Meublé | always | "Studio meublé ou non meublé ?" | 75 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-ETAGE | Étage | if building context | "À quel étage ?" | 62 |
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-SECURITE | Sécurité | not specified | "Sécurité de l'immeuble ?" | 74 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CAUTION | Caution | always | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | always | "Charges incluses ?" | 73 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PARKING | Parking | soft_constraint | 63 |
| FLD-INTERNET | Internet | ranking_preference | 66 |
| FLD-EAU | Eau | ranking_preference | 68 |
| FLD-ELECTRICITE | Électricité | ranking_preference | 69 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-ACCES_ROUTE | Accès route | ranking_preference | 76 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-SURFACE | Surface du studio | informational_only |
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-BALCON | Balcon | ranking_preference |
| FLD-ASCENSEUR | Ascenseur (si étage élevé) | ranking_preference |
| FLD-EMAIL | Email | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-GROUPE_ELECTROGENE | power-cut zone | boost (+10) |
| FLD-FORAGE | water issues area | boost (+10) |
| FLD-MOBILITY | multiple neighborhoods | soft_constraint |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-SALONS | Salon | always 0 for studio (open plan) |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Studio = pas de chambre séparée par définition |
| 2 | "Combien de salons ?" | Studio = espace unique (open plan) |
| 3 | "Quel standing ?" | Déduire du budget/quartier |
| 4 | "Combien de pièces ?" | Terminologie non canonique |

---

## MATRIX 4: studio_moderne

### matrix_id
MATRIX-RES-SEARCH-004

### canonical_name
Studio Moderne — Modern Studio (internal shower)

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT

### property_or_service_type
studio_moderne

### requester_typology
tenant

### journey_stage
SEARCH

### description
Qualification matrix for a modern studio apartment rental search. A studio_moderne features a private internal shower (douche interne), often a separate or semi-separate kitchen, tiled floors, and modern finishes. Higher standard than basic studio. Popular among young professionals and diaspora visitors.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget mensuel maximum ?" | 50 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CUISINE | Cuisine | always | "Cuisine équipée souhaitée ?" | 52 |
| FLD-MEUBLE | Meublé | always | "Studio meublé ou non meublé ?" | 75 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-ETAGE | Étage | always | "À quel étage préférez-vous ?" | 62 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PARKING | Parking | always | "Besoin de parking ?" | 63 |
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation nécessaire ?" | 67 |
| FLD-SECURITE | Sécurité | always | "Sécurité importante ?" | 74 |
| FLD-INTERNET | Internet | always | "Besoin d'internet ?" | 66 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CAUTION | Caution | always | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | always | "Charges incluses ?" | 73 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-EAU | Eau | ranking_preference | 68 |
| FLD-ELECTRICITE | Électricité | ranking_preference | 69 |
| FLD-ACCES_ROUTE | Accès route | ranking_preference | 76 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-SURFACE | Surface | informational_only | 64 |
| FLD-BALCON | Balcon | ranking_preference | 65 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-ASCENSEUR | Ascenseur (si étage élevé) | ranking_preference |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) |
| FLD-EMAIL | Email | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-FORAGE | water-scarce area | boost (+10) |
| FLD-MOBILITY | multiple zones | soft_constraint |
| FLD-GARDIENNAGE | high-end studio | boost (+10) |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-DOUCHES | Douche | always INTERNE for studio_moderne by definition |
| FLD-SALONS | Salon | always 0 for studio |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Studio = pas de chambre séparée |
| 2 | "Douche externe ou interne ?" | Studio_moderne a toujours douche interne |
| 3 | "Quel standing ?" | Déduire du budget/quartier |
| 4 | "Combien de pièces ?" | Terminologie non canonique |

---

## MATRIX 5: studio_meuble

### matrix_id
MATRIX-RES-SEARCH-005

### canonical_name
Studio Meublé — Furnished Studio

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT

### property_or_service_type
studio_meuble

### requester_typology
tenant

### journey_stage
SEARCH

### description
Qualification matrix for a furnished studio rental search. A studio_meuble is a studio apartment that comes fully furnished with bed, wardrobe, seating, often appliances (fridge, cooker), and sometimes TV. Target audience includes professionals, diaspora, and short to medium-term tenants.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget mensuel maximum ?" | 50 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CUISINE | Cuisine | always | "Cuisine équipée souhaitée ?" | 52 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-ETAGE | Étage | always | "À quel étage ?" | 62 |
| FLD-PARKING | Parking | always | "Besoin de parking ?" | 63 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation nécessaire ?" | 67 |
| FLD-INTERNET | Internet | always | "Besoin d'internet ?" | 66 |
| FLD-SECURITE | Sécurité | always | "Sécurité importante ?" | 74 |
| FLD-EAU | Eau | not specified | "Eau courante ?" | 68 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CAUTION | Caution | always | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | always | "Charges incluses ?" | 73 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-SURFACE | Surface | informational_only | 64 |
| FLD-BALCON | Balcon | ranking_preference | 65 |
| FLD-ACCES_ROUTE | Accès route | ranking_preference | 76 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 70 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-ASCENSEUR | Ascenseur | ranking_preference |
| FLD-FORAGE | Forage | boost (+10) |
| FLD-EMAIL | Email | informational_only |
| FLD-GARDIENNAGE | Gardien | boost (+10) |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-MOBILITY | multiple zones | soft_constraint |
| FLD-LINGE | if short-term context | informational_only |
| FLD-ELECTRICITE | not specified | ranking_preference |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-MEUBLE | Meublé | always MEUBLE by definition |
| FLD-DOUCHES | Douche | always INTERNE for studio |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Studio = pas de chambre séparée |
| 2 | "Meublé ou non meublé ?" | Déjà meublé par définition |
| 3 | "Douche externe ou interne ?" | Toujours interne |
| 4 | "Quel standing ?" | Déduire du budget/quartier |

---

## MATRIX 6: appartement_non_meuble

### matrix_id
MATRIX-RES-SEARCH-006

### canonical_name
Appartement Non Meublé — Unfurnished Apartment

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT, BUY

### property_or_service_type
appartement_non_meuble

### requester_typology
tenant, buyer

### journey_stage
SEARCH

### description
Qualification matrix for an unfurnished apartment rental or purchase search. An appartement_non_meuble is a multi-room apartment (2+ chambres) with separate living room (salon), kitchen, and bathroom(s). No furniture included. This is the most common residential type for families and professionals in Cameroon.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget maximum ?" | 50 |
| FLD-CHAMBRES | Chambres | always | "Combien de chambres ?" | 42 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOUCHES | Douches | always | "Combien de douches ?" | 44 |
| FLD-SALONS | Salons | always | "Combien de salons ?" | 46 |
| FLD-CUISINE | Cuisine | always | "Cuisine équipée ou non ?" | 52 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT or TOTAL_PRICE) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-ETAGE | Étage | always | "À quel étage ?" | 62 |
| FLD-PARKING | Parking | always | "Besoin de parking ?" | 63 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-INTERNET | Internet | not specified | "Internet ?" | 66 |
| FLD-SECURITE | Sécurité | not specified | "Sécurité ?" | 74 |
| FLD-ASCENSEUR | Ascenseur | if etage > 2 | "Ascenseur nécessaire ?" | 64 |
| FLD-SURFACE | Surface | not specified | "Surface souhaitée ?" | 48 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CAUTION | Caution | RENT only | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | RENT only | "Charges incluses ?" | 73 |
| FLD-FINANCING | Financement | BUY only | "Comptant ou crédit ?" | 71 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-BALCON | Balcon | ranking_preference | 65 |
| FLD-EAU | Eau | ranking_preference | 68 |
| FLD-ELECTRICITE | Électricité | ranking_preference | 69 |
| FLD-ACCES_ROUTE | Accès route | ranking_preference | 76 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 70 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-GARDIENNAGE | Gardien | boost (+10) |
| FLD-FORAGE | Forage | boost (+10) |
| FLD-EMAIL | Email | informational_only |
| FLD-MOBILITY | Flexibilité | soft_constraint |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-JARDIN | ground floor apartment | ranking_preference |
| FLD-COUR | ground floor | ranking_preference |
| FLD-CLOTURE | if security concern | soft_constraint |
| FLD-USAGE | BUY only (résidence/investissement) | informational_only |
| FLD-FINANCING | BUY transaction | transaction_blocker |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-FINANCING | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-MEUBLE | Meublé | always NON_MEUBLE by definition |
| FLD-DERIVED-NOMBRE_PIECES | Nombre de pièces | chambres + salons |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Meublé ou non meublé ?" | Déjà spécifié dans le type |
| 2 | "Quel standing ?" | Déduire du budget/quartier |
| 3 | "Combien de pièces ?" | Utiliser chambres + salons |
| 4 | "Avez-vous d'autres critères ?" | Trop vague |

### matrix_notes

- For BUY transaction: replace budget semantics with total purchase budget, add FINANCING (FLD-FINANCING)
- For BUY transaction: SURFACE becomes more important in matching score
- For BUY transaction: no CAUTION/CHARGES needed; replace with FINANCING and USAGE

---

## MATRIX 7: appartement_meuble

### matrix_id
MATRIX-RES-SEARCH-007

### canonical_name
Appartement Meublé — Furnished Apartment

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT, BUY

### property_or_service_type
appartement_meuble

### requester_typology
tenant, buyer

### journey_stage
SEARCH

### description
Qualification matrix for a furnished apartment rental or purchase search. An appartement_meuble is a multi-room apartment (2+ chambres) with furniture included (beds, sofas, dining, often appliances). Target audience includes expatriates, diaspora, professionals who want move-in readiness.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget maximum ?" | 50 |
| FLD-CHAMBRES | Chambres | always | "Combien de chambres ?" | 42 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOUCHES | Douches | always | "Combien de douches ?" | 44 |
| FLD-SALONS | Salons | always | "Combien de salons ?" | 46 |
| FLD-CUISINE | Cuisine | always | "Cuisine équipée ?" | 52 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT or TOTAL_PRICE) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-ETAGE | Étage | always | "À quel étage ?" | 62 |
| FLD-PARKING | Parking | always | "Besoin de parking ?" | 63 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-INTERNET | Internet | always | "Internet nécessaire ?" | 66 |
| FLD-SECURITE | Sécurité | always | "Sécurité importante ?" | 74 |
| FLD-ASCENSEUR | Ascenseur | if etage > 2 | "Ascenseur ?" | 64 |
| FLD-SURFACE | Surface | not specified | "Surface souhaitée ?" | 48 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CAUTION | Caution | RENT only | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | RENT only | "Charges incluses ?" | 73 |
| FLD-FINANCING | Financement | BUY only | "Comptant ou crédit ?" | 71 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-BALCON | Balcon | ranking_preference | 65 |
| FLD-EAU | Eau | ranking_preference | 68 |
| FLD-ELECTRICITE | Électricité | ranking_preference | 69 |
| FLD-ACCES_ROUTE | Accès route | ranking_preference | 76 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 70 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-GARDIENNAGE | Gardien | boost (+10) |
| FLD-FORAGE | Forage | boost (+10) |
| FLD-EMAIL | Email | informational_only |
| FLD-MOBILITY | Flexibilité | soft_constraint |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-JARDIN | ground floor | ranking_preference |
| FLD-COUR | ground floor | ranking_preference |
| FLD-LINGE | if furnished with linen service | informational_only |
| FLD-USAGE | BUY only | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-FINANCING | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-MEUBLE | Meublé | always MEUBLE by definition |
| FLD-DERIVED-NOMBRE_PIECES | Nombre de pièces | chambres + salons |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Meublé ou non meublé ?" | Déjà spécifié dans le type |
| 2 | "Quel standing ?" | Déduire du budget/quartier |
| 3 | "Combien de pièces ?" | Utiliser chambres + salons |

---

## MATRIX 8: villa

### matrix_id
MATRIX-RES-SEARCH-008

### canonical_name
Villa — Standalone Villa

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT, BUY

### property_or_service_type
villa

### requester_typology
tenant, buyer, investor

### journey_stage
SEARCH

### description
Qualification matrix for a standalone villa rental or purchase search. A villa is a standalone residential building on its own plot of land with courtyard (cour), parking, often a garden, and multiple bedrooms. Villas range from standard family homes to luxury properties with pools and extensive grounds.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget maximum ?" | 50 |
| FLD-CHAMBRES | Chambres | always | "Combien de chambres ?" | 42 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOUCHES | Douches | always | "Combien de douches ?" | 44 |
| FLD-SALONS | Salons | always | "Combien de salons ?" | 46 |
| FLD-CUISINE | Cuisine | always | "Cuisine équipée ou non ?" | 52 |
| FLD-COUR | Cour | always | "Cour extérieure souhaitée ?" | 47 |
| FLD-PARKING | Parking | always | "Besoin de parking/garage ?" | 63 |
| FLD-SURFACE_TERRAIN | Surface terrain | always | "Quelle taille de terrain ?" | 48 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT or TOTAL_PRICE) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-CLOTURE | Clôture | always | "Clôture importante ?" | 53 |
| FLD-SECURITE | Sécurité | always | "Sécurité importante ?" | 74 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-SURFACE | Surface habitable | not specified | "Surface habitable souhaitée ?" | 49 |
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-EAU | Eau | always | "Alimentation en eau ?" | 68 |
| FLD-ELECTRICITE | Électricité | always | "Alimentation électrique ?" | 69 |
| FLD-ACCES_ROUTE | Accès route | always | "Accès routier souhaité ?" | 76 |
| FLD-JARDIN | Jardin | not specified | "Jardin souhaité ?" | 54 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CAUTION | Caution | RENT only | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | RENT only | "Charges incluses ?" | 73 |
| FLD-FINANCING | Financement | BUY only | "Comptant ou crédit ?" | 71 |
| FLD-DEPENDANCES | Dépendances | always | "Besoin de dépendances ?" | 56 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PISCINE | Piscine | boost (+15) | 57 |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 70 |
| FLD-FORAGE | Forage | boost (+10) | 71 |
| FLD-GARDIENNAGE | Gardien | boost (+10) | 72 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-BALCON | Balcon | ranking_preference | 65 |
| FLD-INTERNET | Internet | ranking_preference | 66 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-MOBILITY | Flexibilité | soft_constraint |
| FLD-EMAIL | Email | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-USAGE | BUY only (résidence/investissement) | informational_only |
| FLD-FINANCING | BUY only | transaction_blocker |
| FLD-BALCON | if multi-level villa | ranking_preference |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-FINANCING | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-MEUBLE | Meublé | NON_MEUBLE (unless variant) |
| FLD-DERIVED-NOMBRE_PIECES | Nombre de pièces | chambres + salons + dépendances |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Quel standing ?" | Déduire du budget/quartier/chambres |
| 2 | "Combien de pièces ?" | Utiliser chambres + salons |
| 3 | "Avez-vous d'autres critères importants ?" | Trop vague |
| 4 | "Piscine ? en premier critère" | Ne pas demander comme critère primaire |

---

## MATRIX 9: villa_basse

### matrix_id
MATRIX-RES-SEARCH-009

### canonical_name
Villa Basse — Single-Story Villa / Bungalow

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT, BUY

### property_or_service_type
villa_basse

### requester_typology
tenant, buyer

### journey_stage
SEARCH

### description
Qualification matrix for a single-story villa (villa basse / bungalow) rental or purchase search. A villa basse is a single-level standalone house with no stairs, ideal for elderly residents, families with young children, or those with mobility concerns. Includes courtyard, parking, and garden areas.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget maximum ?" | 50 |
| FLD-CHAMBRES | Chambres | always | "Combien de chambres ?" | 42 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOUCHES | Douches | always | "Combien de douches ?" | 44 |
| FLD-SALONS | Salons | always | "Combien de salons ?" | 46 |
| FLD-CUISINE | Cuisine | always | "Cuisine équipée ou non ?" | 52 |
| FLD-COUR | Cour | always | "Cour extérieure importante ?" | 47 |
| FLD-PARKING | Parking | always | "Parking/garage ?" | 63 |
| FLD-SURFACE_TERRAIN | Surface terrain | always | "Quelle taille de terrain ?" | 48 |
| FLD-BUDGET_TYPE | Type budget | always | Derived | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-CLOTURE | Clôture | always | "Clôture nécessaire ?" | 53 |
| FLD-SECURITE | Sécurité | always | "Sécurité ?" | 74 |
| FLD-JARDIN | Jardin | always | "Jardin souhaité ?" | 54 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-SURFACE | Surface habitable | not specified | "Surface habitable ?" | 49 |
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-EAU | Eau | always | "Eau ?" | 68 |
| FLD-ELECTRICITE | Électricité | always | "Électricité ?" | 69 |
| FLD-ACCES_ROUTE | Accès route | always | "Accès routier ?" | 76 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CAUTION | Caution | RENT only | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | RENT only | "Charges incluses ?" | 73 |
| FLD-FINANCING | Financement | BUY only | "Comptant ou crédit ?" | 71 |
| FLD-DEPENDANCES | Dépendances | always | "Dépendances ?" | 56 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 70 |
| FLD-FORAGE | Forage | boost (+10) | 71 |
| FLD-GARDIENNAGE | Gardien | boost (+10) | 72 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-PISCINE | Piscine | boost (+15) | 57 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-MOBILITY | Flexibilité | soft_constraint |
| FLD-EMAIL | Email | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-BALCON | RDC — rarely applicable | informational_only |
| FLD-USAGE | BUY only | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-FINANCING | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-ETAGE | Étage | always REZ_DE_CHAUSSEE by definition |
| FLD-MEUBLE | Meublé | NON_MEUBLE (unless variant) |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "À quel étage ?" | Villa basse = rez-de-chaussée par définition |
| 2 | "Ascenseur ?" | Non applicable (RDC) |
| 3 | "Quel standing ?" | Déduire du budget/quartier |
| 4 | "Combien de pièces ?" | Utiliser chambres + salons |

---

## MATRIX 10: duplex

### matrix_id
MATRIX-RES-SEARCH-010

### canonical_name
Duplex — Two-Story Residence

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT, BUY

### property_or_service_type
duplex

### requester_typology
tenant, buyer, investor

### journey_stage
SEARCH

### description
Qualification matrix for a duplex rental or purchase search. A duplex is a two-level residential unit connected by an internal staircase. Typically the lower floor contains living areas (salon, cuisine, douche invité) and the upper floor contains bedrooms (chambres). Popular among families and professionals seeking space.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget maximum ?" | 50 |
| FLD-CHAMBRES | Chambres | always | "Combien de chambres ?" | 42 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOUCHES | Douches | always | "Combien de douches ?" | 44 |
| FLD-SALONS | Salons | always | "Combien de salons ?" | 46 |
| FLD-CUISINE | Cuisine | always | "Cuisine équipée ?" | 52 |
| FLD-PARKING | Parking | always | "Parking/garage ?" | 63 |
| FLD-SURFACE | Surface | always | "Surface souhaitée ?" | 49 |
| FLD-BUDGET_TYPE | Type budget | always | Derived | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-COUR | Cour | always | "Cour extérieure ?" | 47 |
| FLD-CLOTURE | Clôture | always | "Clôture ?" | 53 |
| FLD-SECURITE | Sécurité | always | "Sécurité ?" | 74 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-EAU | Eau | always | "Eau ?" | 68 |
| FLD-ELECTRICITE | Électricité | always | "Électricité ?" | 69 |
| FLD-ACCES_ROUTE | Accès route | always | "Accès routier ?" | 76 |
| FLD-JARDIN | Jardin | not specified | "Jardin ?" | 54 |
| FLD-SURFACE_TERRAIN | Surface terrain | not specified | "Taille du terrain ?" | 48 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CAUTION | Caution | RENT only | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | RENT only | "Charges incluses ?" | 73 |
| FLD-FINANCING | Financement | BUY only | "Comptant ou crédit ?" | 71 |
| FLD-DEPENDANCES | Dépendances | always | "Dépendances ?" | 56 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-BALCON | Balcon | ranking_preference | 65 |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 70 |
| FLD-FORAGE | Forage | boost (+10) | 71 |
| FLD-GARDIENNAGE | Gardien | boost (+10) | 72 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-INTERNET | Internet | ranking_preference | 66 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-MOBILITY | Flexibilité | soft_constraint |
| FLD-EMAIL | Email | informational_only |
| FLD-PISCINE | Piscine | boost (+15) |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-USAGE | BUY only | informational_only |
| FLD-FINANCING | BUY only | transaction_blocker |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-FINANCING | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-DERIVED-NOMBRE_NIVEAUX | Nombre de niveaux | always 2 for duplex |
| FLD-MEUBLE | Meublé | NON_MEUBLE (unless variant) |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Quel standing ?" | Déduire du budget/quartier/chambres |
| 2 | "Combien de pièces ?" | Utiliser chambres + salons |
| 3 | "À quel étage ?" | Duplex = 2 niveaux par définition |
| 4 | "Ascenseur ?" | Rarement applicable (2 niveaux) |

---

---

## REMAINING MATRICES (10-18)

Continuation of residential search qualification matrices.


---

## MATRIX 11: triplex

### matrix_id
MATRIX-RES-SEARCH-011

### canonical_name
Triplex — Three-Story Residence

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT, BUY

### property_or_service_type
triplex

### requester_typology
tenant, buyer, investor

### journey_stage
SEARCH

### description
Qualification matrix for a triplex rental or purchase search. A triplex is a three-level residential unit, typically with living areas on ground floor, bedrooms on first floor, and additional space (playroom, office, terrace) on the top floor. A premium property type for large families or high-income professionals.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget maximum ?" | 50 |
| FLD-CHAMBRES | Chambres | always | "Combien de chambres ?" | 42 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DOUCHES | Douches | always | "Combien de douches ?" | 44 |
| FLD-SALONS | Salons | always | "Combien de salons ?" | 46 |
| FLD-CUISINE | Cuisine | always | "Cuisine équipée ?" | 52 |
| FLD-PARKING | Parking | always | "Parking/garage ?" | 63 |
| FLD-SURFACE | Surface | always | "Surface souhaitée ?" | 49 |
| FLD-BUDGET_TYPE | Type budget | always | Derived | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-COUR | Cour | always | "Cour extérieure ?" | 47 |
| FLD-CLOTURE | Clôture | always | "Clôture ?" | 53 |
| FLD-SECURITE | Sécurité | always | "Sécurité ?" | 74 |
| FLD-ASCENSEUR | Ascenseur | always | "Ascenseur nécessaire (3 niveaux) ?" | 64 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-EAU | Eau | always | "Eau ?" | 68 |
| FLD-ELECTRICITE | Électricité | always | "Électricité ?" | 69 |
| FLD-ACCES_ROUTE | Accès route | always | "Accès routier ?" | 76 |
| FLD-JARDIN | Jardin | not specified | "Jardin ?" | 54 |
| FLD-SURFACE_TERRAIN | Surface terrain | not specified | "Taille du terrain ?" | 48 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CAUTION | Caution | RENT only | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | RENT only | "Charges incluses ?" | 73 |
| FLD-FINANCING | Financement | BUY only | "Comptant ou crédit ?" | 71 |
| FLD-DEPENDANCES | Dépendances | always | "Dépendances ?" | 56 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-BALCON | Balcon | ranking_preference | 65 |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 70 |
| FLD-FORAGE | Forage | boost (+10) | 71 |
| FLD-GARDIENNAGE | Gardien | boost (+10) | 72 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-INTERNET | Internet | ranking_preference | 66 |
| FLD-PISCINE | Piscine | boost (+15) | 57 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-MOBILITY | Flexibilité | soft_constraint |
| FLD-EMAIL | Email | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-USAGE | BUY only | informational_only |
| FLD-FINANCING | BUY only | transaction_blocker |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-FINANCING | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-DERIVED-NOMBRE_NIVEAUX | Nombre de niveaux | always 3 for triplex |
| FLD-MEUBLE | Meublé | NON_MEUBLE (unless variant) |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Quel standing ?" | Déduire du budget/quartier/chambres |
| 2 | "Combien de pièces ?" | Utiliser chambres + salons |
| 3 | "Combien d'étages ?" | Triplex = 3 niveaux par définition |


---

## MATRIX 12: maison_individuelle

### matrix_id
MATRIX-RES-SEARCH-012

### canonical_name
Maison Individuelle — Single Family House

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT, BUY

### property_or_service_type
maison_individuelle

### requester_typology
tenant, buyer

### journey_stage
SEARCH

### description
Qualification matrix for a single-family house (maison individuelle) rental or purchase search. A maison_individuelle is a standalone house, typically on its own plot, with private courtyard, parking, and garden. Less prestigious than a villa but more spacious than an apartment. Common in residential neighborhoods across Cameroonian cities.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget maximum ?" | 50 |
| FLD-CHAMBRES | Chambres | always | "Combien de chambres ?" | 42 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DOUCHES | Douches | always | "Combien de douches ?" | 44 |
| FLD-SALONS | Salons | always | "Combien de salons ?" | 46 |
| FLD-CUISINE | Cuisine | always | "Cuisine équipée ?" | 52 |
| FLD-COUR | Cour | always | "Cour extérieure ?" | 47 |
| FLD-PARKING | Parking | always | "Parking/garage ?" | 63 |
| FLD-SURFACE_TERRAIN | Surface terrain | always | "Quelle taille de terrain ?" | 48 |
| FLD-BUDGET_TYPE | Type budget | always | Derived | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-CLOTURE | Clôture | always | "Clôture nécessaire ?" | 53 |
| FLD-SECURITE | Sécurité | always | "Sécurité ?" | 74 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-SURFACE | Surface habitable | not specified | "Surface habitable ?" | 49 |
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-EAU | Eau | always | "Eau ?" | 68 |
| FLD-ELECTRICITE | Électricité | always | "Électricité ?" | 69 |
| FLD-ACCES_ROUTE | Accès route | always | "Accès routier ?" | 76 |
| FLD-JARDIN | Jardin | not specified | "Jardin ?" | 54 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CAUTION | Caution | RENT only | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | RENT only | "Charges incluses ?" | 73 |
| FLD-FINANCING | Financement | BUY only | "Comptant ou crédit ?" | 71 |
| FLD-DEPENDANCES | Dépendances | always | "Dépendances ?" | 56 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 70 |
| FLD-FORAGE | Forage | boost (+10) | 71 |
| FLD-GARDIENNAGE | Gardien | boost (+10) | 72 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-INTERNET | Internet | ranking_preference | 66 |
| FLD-BALCON | Balcon | ranking_preference | 65 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-MOBILITY | Flexibilité | soft_constraint |
| FLD-EMAIL | Email | informational_only |
| FLD-PISCINE | Piscine | boost (+15) |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-USAGE | BUY only | informational_only |
| FLD-FINANCING | BUY only | transaction_blocker |
| FLD-ETAGE | if multi-level house | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-FINANCING | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-MEUBLE | Meublé | NON_MEUBLE (unless variant) |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Quel standing ?" | Déduire du budget/quartier/chambres |
| 2 | "Combien de pièces ?" | Utiliser chambres + salons |
| 3 | "Avez-vous d'autres critères ?" | Trop vague |


---

## MATRIX 13: maison_de_ville

### matrix_id
MATRIX-RES-SEARCH-013

### canonical_name
Maison de Ville — Townhouse

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT, BUY

### property_or_service_type
maison_de_ville

### requester_typology
tenant, buyer

### journey_stage
SEARCH

### description
Qualification matrix for a townhouse rental or purchase search. A maison_de_ville is an attached or semi-detached house in an urban setting, often part of a row or compound, with shared walls but private entrance. Typically has small courtyard, limited garden, and parking. Common in central urban neighborhoods.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget maximum ?" | 50 |
| FLD-CHAMBRES | Chambres | always | "Combien de chambres ?" | 42 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DOUCHES | Douches | always | "Combien de douches ?" | 44 |
| FLD-SALONS | Salons | always | "Combien de salons ?" | 46 |
| FLD-CUISINE | Cuisine | always | "Cuisine ?" | 52 |
| FLD-PARKING | Parking | always | "Parking ?" | 63 |
| FLD-COUR | Cour | always | "Cour extérieure ?" | 47 |
| FLD-BUDGET_TYPE | Type budget | always | Derived | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-CLOTURE | Clôture | always | "Clôture ?" | 53 |
| FLD-SECURITE | Sécurité | always | "Sécurité ?" | 74 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-SURFACE | Surface | not specified | "Surface ?" | 49 |
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-EAU | Eau | always | "Eau ?" | 68 |
| FLD-ELECTRICITE | Électricité | always | "Électricité ?" | 69 |
| FLD-ACCES_ROUTE | Accès route | always | "Accès ?" | 76 |
| FLD-SURFACE_TERRAIN | Surface terrain | not specified | "Terrain ?" | 48 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CAUTION | Caution | RENT only | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | RENT only | "Charges ?" | 73 |
| FLD-FINANCING | Financement | BUY only | "Comptant ou crédit ?" | 71 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 70 |
| FLD-PROXIMITY_PREFERENCES | Proximité centre-ville | ranking_preference | 77 |
| FLD-JARDIN | Jardin | ranking_preference | 54 |
| FLD-GARDIENNAGE | Gardien | boost (+10) | 72 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-MOBILITY | Flexibilité | soft_constraint |
| FLD-EMAIL | Email | informational_only |
| FLD-BALCON | Balcon | ranking_preference |
| FLD-INTERNET | Internet | ranking_preference |
| FLD-PISCINE | Piscine | boost (+15) |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-USAGE | BUY only | informational_only |
| FLD-FINANCING | BUY only | transaction_blocker |
| FLD-ETAGE | if multi-level | informational_only |
| FLD-DEPENDANCES | if user asks | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-FINANCING | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-DERIVED-URBANISATION | Urbanisation | always URBAIN for maison_de_ville |
| FLD-MEUBLE | Meublé | NON_MEUBLE (unless variant) |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Quel standing ?" | Déduire du budget/quartier |
| 2 | "Combien de pièces ?" | Utiliser chambres + salons |
| 3 | "Grand terrain ?" | Townhouse = terrain limité par définition |


---

## MATRIX 14: chambre_hotel

### matrix_id
MATRIX-RES-SEARCH-014

### canonical_name
Chambre d'Hôtel — Hotel Room

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT (short-term)

### property_or_service_type
chambre_hotel

### requester_typology
tenant

### journey_stage
SEARCH

### description
Qualification matrix for a hotel room short-term stay search. A chambre_hotel covers hotel rooms, guesthouse rooms, and similar short-term accommodation. Services may include breakfast, cleaning, linen, and reception. Booking is by night, week-end, or week.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget par nuit/séjour ?" | 50 |
| FLD-DUREE_SEJOUR | Durée séjour | always | "Pour combien de temps ? (nuit, week-end, semaine, mois)" | 43 |
| FLD-NOMBRE_PERSONNES | Nombre personnes | always | "Combien de personnes ?" | 45 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-SERVICES_INCLUS | Services inclus | always | "Quels services sont importants ? (wifi, tv, clim, petit-déjeuner)" | 47 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (PRICE_PER_NIGHT or PRICE_PER_MONTH) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-DATE_ARRIVEE | Date d'arrivée | not specified | "Quelle date d'arrivée ?" | 58 |
| FLD-DATE_DEPART | Date de départ | not specified | "Quelle date de départ ?" | 59 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-PETIT_DEJEUNER | Petit-déjeuner | always | "Petit-déjeuner inclus important ?" | 53 |
| FLD-MENAGE | Ménage | always | "Service de ménage important ?" | 54 |
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation nécessaire ?" | 67 |
| FLD-SECURITE | Sécurité | not specified | "Sécurité ?" | 74 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-SERVICES_INCLUS | Services confirmés | always | "Confirmez-vous les services souhaités ?" | 73 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LINGE | Linge fourni | informational_only | 55 |
| FLD-INTERNET | Internet | ranking_preference | 66 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-EAU | Eau chaude | ranking_preference | 68 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-EMAIL | Email | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-ACCES_ROUTE | if specific location concerns | ranking_preference |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-MEUBLE | Meublé | always MEUBLE for hotel |
| FLD-CHAMBRES | Chambres | always 1 for hotel room (unless suite) |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Chambre d'hôtel = 1 chambre |
| 2 | "Combien de salons ?" | Non applicable |
| 3 | "Cuisine équipée ?" | Non applicable pour hôtel standard |
| 4 | "Quel standing ?" | Déduire du budget/quartier |


---

## MATRIX 15: appartement_courte_duree

### matrix_id
MATRIX-RES-SEARCH-015

### canonical_name
Appartement Courte Durée — Short-Term Apartment

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT (short-term)

### property_or_service_type
appartement_courte_duree

### requester_typology
tenant

### journey_stage
SEARCH

### description
Qualification matrix for a short-term apartment rental search. An appartement_courte_duree is a fully furnished apartment rented by the night, week, or month. Typically includes all utilities, internet, and sometimes cleaning services. Popular with business travelers, tourists, and diaspora visitors.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget par nuit/semaine/mois ?" | 50 |
| FLD-DUREE_SEJOUR | Durée séjour | always | "Pour combien de temps ?" | 43 |
| FLD-NOMBRE_PERSONNES | Nombre personnes | always | "Combien de personnes ?" | 45 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CHAMBRES | Chambres | always | "Combien de chambres ?" | 42 |
| FLD-DOUCHES | Douches | always | "Combien de douches ?" | 44 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (PRICE_PER_NIGHT or PRICE_PER_MONTH) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-DATE_ARRIVEE | Date d'arrivée | not specified | "Date d'arrivée ?" | 58 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-INTERNET | Internet | always | "Internet nécessaire ?" | 66 |
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-MENAGE | Ménage | not specified | "Ménage inclus souhaité ?" | 54 |
| FLD-SECURITE | Sécurité | always | "Sécurité ?" | 74 |
| FLD-SALONS | Salons | not specified | "Salon/séjour ?" | 46 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CHARGES | Charges (utilités) | always | "Charges incluses dans le prix ?" | 73 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LINGE | Linge fourni | informational_only | 55 |
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-PARKING | Parking | ranking_preference | 63 |
| FLD-EAU | Eau | ranking_preference | 68 |
| FLD-ELECTRICITE | Électricité | ranking_preference | 69 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-BALCON | Balcon | ranking_preference |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) |
| FLD-EMAIL | Email | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-ASCENSEUR | if etage > 2 | ranking_preference |
| FLD-ETAGE | if building context | ranking_preference |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-MEUBLE | Meublé | always MEUBLE for short-term |
| FLD-SURFACE | Surface | informational only |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Meublé ou non meublé ?" | Toujours meublé pour courte durée |
| 2 | "Caution ?" | Variable, demander au moment de la réservation |
| 3 | "Quel standing ?" | Déduire du budget/quartier |


---

## MATRIX 16: residence_meublee

### matrix_id
MATRIX-RES-SEARCH-016

### canonical_name
Résidence Meublée — Furnished Residence (Serviced Apartment)

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT (short-term, long-term)

### property_or_service_type
residence_meublee

### requester_typology
tenant

### journey_stage
SEARCH

### description
Qualification matrix for a furnished residence (résidence meublée) rental search. This covers serviced apartments, residence-hotels, and aparthotels combining hotel services with apartment space. Suitable for both short and medium-term stays. Includes services like cleaning, reception, and often breakfast.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget mensuel maximum ?" | 50 |
| FLD-DUREE_SEJOUR | Durée séjour | always | "Pour combien de temps ? (mois, semaine)" | 43 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CHAMBRES | Chambres | always | "Combien de chambres ?" | 42 |
| FLD-DOUCHES | Douches | always | "Combien de douches ?" | 44 |
| FLD-SALONS | Salons | always | "Salon/séjour ?" | 46 |
| FLD-CUISINE | Cuisine | always | "Cuisine équipée souhaitée ?" | 52 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-ETAGE | Étage | always | "À quel étage ?" | 62 |
| FLD-PARKING | Parking | always | "Besoin de parking ?" | 63 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-INTERNET | Internet | always | "Internet nécessaire ?" | 66 |
| FLD-CLIMATISATION | Climatisation | hot cities | "Climatisation ?" | 67 |
| FLD-MENAGE | Ménage | always | "Ménage inclus important ?" | 54 |
| FLD-SECURITE | Sécurité | always | "Sécurité ?" | 74 |
| FLD-SERVICES_INCLUS | Services inclus | not specified | "Quels services sont importants ?" | 51 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CHARGES | Charges | always | "Charges incluses ?" | 73 |
| FLD-CAUTION | Caution | long-term only | "Dépôt de garantie ?" | 72 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PROXIMITY_PREFERENCES | Proximité | ranking_preference | 77 |
| FLD-BALCON | Balcon | ranking_preference | 65 |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 70 |
| FLD-LINGE | Linge fourni | informational_only | 55 |
| FLD-PETIT_DEJEUNER | Petit-déjeuner | informational_only | 53 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-ASCENSEUR | Ascenseur | ranking_preference |
| FLD-FORAGE | Forage | boost (+10) |
| FLD-GARDIENNAGE | Gardien | boost (+10) |
| FLD-EMAIL | Email | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-SURFACE | if user mentions space | informational_only |
| FLD-ACCES_ROUTE | if specific location | ranking_preference |
| FLD-MOBILITY | multiple zones | soft_constraint |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-MEUBLE | Meublé | always MEUBLE for résidence meublée |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Meublé ou non meublé ?" | Toujours meublé par définition |
| 2 | "Quel standing ?" | Déduire du budget/quartier |
| 3 | "Combien de pièces ?" | Utiliser chambres + salons |


---

## MATRIX 17: colocation

### matrix_id
MATRIX-RES-SEARCH-017

### canonical_name
Colocation — Shared Housing

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT

### property_or_service_type
colocation

### requester_typology
tenant

### journey_stage
SEARCH

### description
Qualification matrix for shared housing (colocation) rental search. Colocation involves renting a room in a shared apartment or house with common areas (salon, cuisine, douches) shared among tenants. Popular among students, young professionals, and singles. Includes specific preferences for gender, age range, and shared living arrangements.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-NEIGHBORHOOD | Quartier | always | "Quel quartier ou quelle zone ?" | 40 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget mensuel maximum (part individuelle) ?" | 50 |
| FLD-NOMBRE_COLOCATAIRES | Nombre colocataires | always | "Combien de colocataires maximum ?" | 43 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-GENRE_PREFERENCE | Préférence genre | always | "Préférence de genre pour les colocataires ?" | 44 |
| FLD-DOUCHES | Douches | always | "Combien de douches partagées ?" | 45 |
| FLD-SALONS | Salons | always | "Salon partagé important ?" | 46 |
| FLD-CUISINE | Cuisine | always | "Cuisine partagée ?" | 52 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand ?" | 60 |
| FLD-MEUBLE | Meublé | always | "Chambre meublée ou non ?" | 75 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-ESPACES_PARTAGES | Espaces partagés | always | "Quels espaces partagés sont importants ? (salon, cuisine, terrasse)" | 47 |
| FLD-AGE_RANGE | Tranche d'âge | not specified | "Tranche d'âge préférée des colocataires ?" | 48 |
| FLD-SECURITE | Sécurité | not specified | "Sécurité importante ?" | 74 |
| FLD-INTERNET | Internet | always | "Internet nécessaire ?" | 66 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CAUTION | Caution | always | "Dépôt de garantie ?" | 72 |
| FLD-CHARGES | Charges | always | "Charges incluses ? (électricité, eau, internet)" | 73 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-REGLEMENT_INTERIEUR | Règlement intérieur | informational_only | 57 |
| FLD-PROXIMITY_PREFERENCES | Proximité travail/école | ranking_preference | 77 |
| FLD-CLIMATISATION | Climatisation | ranking_preference | 67 |
| FLD-BALCON | Balcon/terrasse | ranking_preference | 65 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-CITY_ALTERNATIVES | Autres villes | informational_only |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | informational_only |
| FLD-EMAIL | Email | informational_only |
| FLD-BOURSE | Statut étudiant/boursier (volontaire) | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-ANIMAUX | if user asks about pets | soft_constraint |
| FLD-ACCES_ROUTE | if specific location | ranking_preference |
| FLD-MOBILITY | multiple zones | soft_constraint |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-GENRE_PREFERENCE | Gender preference (sensitive data) |
| FLD-AGE_RANGE | Age preference (sensitive data) |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-CHAMBRES | Chambres | 1 chambre individuelle par colocataire |
| FLD-SURFACE | Surface | informational only |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | 1 chambre individuelle par personne |
| 2 | "Avez-vous des animaux ?" | Ne pas demander comme critère primaire |
| 3 | "Quel standing ?" | Déduire du budget/quartier |
| 4 | "Parking ?" | Demander seulement si pertinent |


---

## MATRIX 18: cite_universitaire

### matrix_id
MATRIX-RES-SEARCH-018

### canonical_name
Cité Universitaire — University/Campus Housing

### request_family
RESIDENTIAL_SEARCH

### transaction_type
RENT

### property_or_service_type
cite_universitaire

### requester_typology
tenant

### journey_stage
SEARCH

### description
Qualification matrix for university campus housing (cité universitaire) rental search. This covers on-campus and off-campus student housing, university residences, and student accommodations. Typically basic furnished rooms with shared facilities. Budget is very limited. Target audience is students.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-TRANSACTION | Transaction | always | "C'est pour louer, acheter, vendre ou investir ?" | 10 |
| FLD-PROPERTY_TYPE | Type de bien | always | "Quel type de bien cherchez-vous ?" | 20 |
| FLD-CITY | Ville | always | "Dans quelle ville ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CITY | Ville | always | "Dans quelle ville universitaire ?" | 30 |
| FLD-UNIVERSITE | Université | always | "Quelle université fréquentez-vous ?" | 35 |
| FLD-BUDGET_MAX | Budget max | always | "Quel budget mensuel maximum (loyer étudiant) ?" | 50 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-TYPE_CHAMBRE_UNIV | Type chambre | always | "Chambre individuelle ou partagée ?" | 42 |
| FLD-DOUCHES | Douches | always | "Douche privée ou commune ?" | 44 |
| FLD-CUISINE | Cuisine | always | "Cuisine personnelle ou commune ?" | 52 |
| FLD-BUDGET_TYPE | Type budget | always | Derived (MONTHLY_RENT) | 55 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quand voulez-vous emménager ?" | 60 |
| FLD-NOM | Nom | always | "Quel est votre nom ?" | 80 |
| FLD-TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 85 |
| FLD-CANAL_PREFERE | Canal préféré | always | "Quel canal préférez-vous pour les échanges ?" | 90 |
| FLD-DISPONIBILITE | Disponibilité | always | "À partir de quelle date (rentrée universitaire) ?" | 60 |
| FLD-MEUBLE | Meublé | always | "Meublé ou non ? (généralement meublé)" | 75 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-RESTAURATION | Restauration | always | "Restaurant/cantine universitaire important ?" | 53 |
| FLD-INTERNET | Internet | always | "Connexion internet nécessaire ?" | 66 |
| FLD-SECURITE | Sécurité | always | "Sécurité du campus importante ?" | 74 |
| FLD-ESPACES_PARTAGES | Espaces partagés | not specified | "Espaces communs importants ? (salon étudiant, laverie)" | 47 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|---|---|---|---|---|
| FLD-CHARGES | Charges | always | "Charges incluses (eau, électricité) ?" | 73 |
| FLD-CAUTION | Caution | always | "Dépôt de garantie étudiant ?" | 72 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PROXIMITY_PREFERENCES | Proximité campus | ranking_preference | 77 |
| FLD-ACCES_ROUTE | Accès transport | ranking_preference | 76 |
| FLD-ANNEE_ETUDES | Année d'études | informational_only | 45 |
| FLD-CLIMATISATION | Climatisation | ranking_preference | 67 |

### optional_fields

| FIELD-ID | description | matching_role |
|----------|-------------|---------------|
| FLD-ZONE | Zone élargie | informational_only |
| FLD-EMAIL | Email académique | informational_only |
| FLD-LINGE | Linge fourni | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-GENRE_PREFERENCE | if unisex housing requested | soft_constraint |
| FLD-BOURSE | if student mentions scholarship context | informational_only |
| FLD-NOMBRE_COLOCATAIRES | if shared room | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-TELEPHONE | Personal contact information |
| FLD-NOM | Personal identity |
| FLD-BUDGET_MAX | Financial information |
| FLD-BOURSE | Scholarship status (sensitive) |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DERIVED-STANDING | Standing | budget + quartier + property type |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs market data per type |
| FLD-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-DERIVED-PROFIL | Profil demandeur | message + context |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-BUDGET_TYPE | Type de budget | transaction (MONTHLY_RENT or TOTAL_PRICE) |
| FLD-CHAMBRES | Chambres | 1 chambre (individuelle ou partagée) |
| FLD-MEUBLE | Meublé | generally MEUBLE for university housing |
| FLD-SALONS | Salon | shared common room if applicable |
| FLD-DERIVED-PROFIL | Profil | always ETUDIANT for cite_universitaire |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Chambre universitaire = 1 chambre |
| 2 | "Combien de salons ?" | Salon commun, pas pertinent comme critère |
| 3 | "Parking ?" | Rarement pertinent pour logement étudiant |
| 4 | "Piscine ?" | Jamais pertinent pour cité universitaire |
| 5 | "Quel standing ?" | Déduire du budget/type de chambre |
| 6 | "Financement ?" | Déduire (bourse/parents) |

### matrix_notes

- University housing generally has very limited budgets (15k-50k FCFA/month)
- On-campus housing availability is tied to academic calendar (rentrée: September-October)
- Off-campus student housing may follow different rules (use maison_individuelle or appartement matrix)
- Cité_universitaire focuses on officially managed university residences


---

*Document patrimonial Gold — Matrices de qualification recherche résidentielle — 2026-07-15*
*Toute reconstruction du système de qualification LAWIM doit respecter ces matrices validées.*
