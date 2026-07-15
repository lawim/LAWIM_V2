# COMMON FIELD DICTIONARY — LAWIM Qualification Matrices

**Document ID:** LAWIM-GOLD-QM-FIELDS-V1
**Status:** CANONICAL — Master dictionary of all common fields across matrices
**Date:** 2026-07-15
**Total Fields:** 120+

---

## Table of Contents

1. [Core Transaction & Intent Fields](#1-core-transaction--intent-fields)
2. [Location Fields](#2-location-fields)
3. [Budget & Financial Fields](#3-budget--financial-fields)
4. [Property Characteristic Fields](#4-property-characteristic-fields)
5. [Contact & Identity Fields](#5-contact--identity-fields)
6. [Timing & Availability Fields](#6-timing--availability-fields)
7. [Residential-Specific Fields](#7-residential-specific-fields)
8. [Land-Specific Fields](#8-land-specific-fields)
9. [Commercial-Specific Fields](#9-commercial-specific-fields)
10. [Financing-Specific Fields](#10-financing-specific-fields)
11. [Professional Service Fields](#11-professional-service-fields)
12. [Derived Fields](#12-derived-fields)
13. [Alphabetical Index](#13-alphabetical-index)

---

## Legend

| Attribute | Description |
|-----------|-------------|
| field_id | Unique identifier |
| canonical_label | English label |
| french_label | French label |
| description | Meaning and usage |
| data_type | string, integer, float, boolean, enum, date |
| mandatory_when | When this field is mandatory (generic) |
| validation_rules | Constraints on values |
| normalization_rules | How values are normalized |
| question_template_short | Short question template |
| matching_role | How field affects matching |
| privacy_level | public / private / sensitive / confidential |
| categories | Which matrix families use this field |
| source | Origin of the field definition |

---

## 1. Core Transaction & Intent Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| FLD-TRANSACTION | Transaction | Transaction | The type of real estate transaction the user wants | enum | always | RENT, BUY, SELL, FINANCE, FIND | Uppercase, normalize synonyms (louer→RENT, acheter→BUY) | "C'est pour louer, acheter, vendre ou investir ?" | hard_constraint | public | RESIDENTIAL_SEARCH, LAND_SEARCH, COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-INTENT | Intention | Intention | The specific user intention behind the transaction | enum | always | RENT_PROPERTY, BUY_PROPERTY, SELL_PROPERTY, INVESTOR_INTENT, FIND_PROFESSIONAL, GET_SERVICE | Map to canonical intents from user language | "Quel est votre projet exactement ?" | hard_constraint | public | RESIDENTIAL_SEARCH, LAND_SEARCH, COMMERCIAL_SEARCH, FINANCING_REQUEST | HERITAGE_VALIDATED |
| FLD-PROPERTY_TYPE | Property Type | Type de bien | The specific property type the user is looking for | enum | always | 18 residential types, 7 land types, 16 commercial types | Normalize synonyms; "appart"→appartement, "terrain"→terrain | "Quel type de bien cherchez-vous ?" | hard_constraint | public | RESIDENTIAL_SEARCH, LAND_SEARCH, COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-REQUEST_FAMILY | Request Family | Famille de demande | High-level category of the request | enum | always | RESIDENTIAL_SEARCH, LAND_SEARCH, COMMERCIAL_SEARCH, FINANCING_REQUEST, PROFESSIONAL_SEARCH, REAL_ESTATE_SERVICES | Derived from intent + property type | (system-derived, never asked) | hard_constraint | public | ALL | HERITAGE_VALIDATED |
| FLD-JOURNEY_STAGE | Journey Stage | Étape du parcours | Current stage in the user journey | enum | always | SEARCH, INTRODUCE, VISIT, TRANSACTION, SERVICE, FINANCE | Progresses forward; never regresses | (system-derived, never asked) | informational_only | public | ALL | HERITAGE_VALIDATED |
| FLD-TRANSACTION_TYPE | Transaction Type | Type de transaction | Specific transaction sub-type | enum | always | RENT, BUY, SELL, FINANCE, FIND, SERVICE | Derived from FLD-TRANSACTION | (system-derived from transaction) | hard_constraint | public | ALL | HERITAGE_VALIDATED |
| FLD-USAGE | Usage | Usage | Intended use of the property | enum | BUY transaction | RESIDENCE, INVESTISSEMENT, MIXTE | Normalize "habiter"→RESIDENCE, "louer"→INVESTISSEMENT | "Ce sera pour y habiter, investir ou les deux ?" | soft_constraint | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-INTENT_CONFIDENCE | Intent Confidence | Confiance intention | How confident the system is about detected intent | float | always | 0.0-1.0 | Derived from NLP confidence score | (system-derived, never asked) | informational_only | public | ALL | HERITAGE_NORMALIZED |
| FLD-PROPERTY_TYPE_CONFIDENCE | Property Type Confidence | Confiance type bien | Confidence in detected property type | float | always | 0.0-1.0 | Derived from NLP + user confirmation | (system-derived, never asked) | informational_only | public | ALL | HERITAGE_NORMALIZED |
| FLD-INTENT_SOURCE | Intent Source | Source intention | How the intent was determined | enum | always | USER_EXPLICIT, NLP_DETECTED, DEDUCED, CONFIRMED | Traceability tag | (system-derived) | informational_only | public | ALL | HERITAGE_NORMALIZED |

---

## 2. Location Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| FLD-CITY | City | Ville | Target city for the property search | string | always | Must be in LAWIM city list; min 2 chars | Normalize case; map city aliases (Dla→Douala, Yde→Yaounde) | "Dans quelle ville ?" | hard_constraint | public | RESIDENTIAL_SEARCH, LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-NEIGHBORHOOD | Neighborhood | Quartier | Target neighborhood or district | string | always for search | Must be in neighborhood list for the city | Normalize case; map neighborhood aliases | "Quel quartier ou quelle zone ?" | hard_constraint | public | RESIDENTIAL_SEARCH, LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-ZONE | Zone | Zone | Broader zone or area description | string | optional | Free text | Free text normalization | "Quelle zone plus précisément ?" | informational_only | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-CITY_ALTERNATIVES | Alternative Cities | Autres villes | Other cities the user would consider | string | optional | Comma-separated; each must be valid city | Split, normalize, validate | "D'autres villes possibles ?" | informational_only | public | RESIDENTIAL_SEARCH | EXPERT_PROPOSAL |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Alternative Neighborhoods | Autres quartiers | Other neighborhoods the user would consider | string | optional | Comma-separated | Split, normalize | "D'autres quartiers ?" | informational_only | public | RESIDENTIAL_SEARCH | EXPERT_PROPOSAL |
| FLD-PROXIMITY_PREFERENCES | Proximity Preferences | Proximité | What the user needs to be near (schools, markets, transport) | string | optional | Free text | Extract key locations; geocode if possible | "Avez-vous besoin d'être proche de quelque chose ?" | ranking_preference | public | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | EXPERT_PROPOSAL |
| FLD-MOBILITY | Mobility | Mobilité | How flexible the user is about location | enum | multiple neighborhoods | STRICT, FLEXIBLE, VERY_FLEXIBLE | Derived from user language about location | "Êtes-vous flexible sur la localisation ?" | soft_constraint | private | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-COORDONNEES_GPS | GPS Coordinates | Coordonnées GPS | Exact GPS coordinates of a property | string | before visit for land | Valid lat,lng format | Parse and validate coordinates | "Pouvez-vous partager les coordonnées GPS ?" | verification_only | private | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-ZONE_RECHERCHE_KM | Search Radius | Rayon de recherche | Search radius around a location | integer | PROFESSIONAL_SEARCH | 1-100 km | Validate range | "Dans quel rayon autour de cette ville ?" | soft_constraint | public | PROFESSIONAL_SEARCH | EXPERT_PROPOSAL |
| FLD-ADRESSE_EXACTE | Exact Address | Adresse exacte | Full street address of the property | string | transaction stage | Must be valid address format | Validate; geocode | "Quelle est l'adresse exacte ?" | verification_only | private | ALL | HERITAGE_VALIDATED |

---

## 3. Budget & Financial Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| FLD-BUDGET_MAX | Maximum Budget | Budget maximum | Maximum budget the user is willing to spend | integer | always | > 0; integer; currency-aware | Normalize to monthly for rent, total for buy | "Quel budget maximum ?" | hard_constraint | private | RESIDENTIAL_SEARCH, LAND_SEARCH, COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-BUDGET_MIN | Minimum Budget | Budget minimum | Minimum budget (for ranges) | integer | optional | < BUDGET_MAX; > 0 | Must be less than max | "Budget minimum ?" | soft_constraint | private | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-BUDGET_TYPE | Budget Type | Type de budget | What the budget figure represents | enum | always | MONTHLY_RENT, TOTAL_PRICE, PRICE_PER_NIGHT, PRICE_PER_SQM | Derived from transaction type | (system-derived) | informational_only | private | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-BUDGET_CURRENCY | Currency | Devise | Currency of the budget | enum | always | XAF, EUR, USD, GBP, XOF | Normalize to XAF for Cameroon operations | "Dans quelle devise ?" | informational_only | private | ALL | HERITAGE_VALIDATED |
| FLD-BUDGET_NEGOTIABLE | Negotiable | Négociable | Whether the budget is negotiable | boolean | optional | true, false | Default true for rent, false for buy | "Le budget est-il négociable ?" | soft_constraint | private | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-BUDGET_PAR_M2 | Price per m2 | Prix au m2 | Budget calculated per square meter | integer | optional | > 0 | budget / surface when both available | (system-derived) | informational_only | public | LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-CAUTION | Security Deposit | Caution | Security deposit amount | integer | RENT transaction | > 0; typically 1-3 months rent | Normalize to monthly rent equivalent | "Dépôt de garantie ?" | transaction_blocker | confidential | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-CHARGES | Charges | Charges | Whether utilities are included | enum | RENT transaction | INCLUSES, NON_INCLUSES, PARTIELLES | Map user description | "Les charges sont-elles incluses ?" | soft_constraint | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-FINANCING | Financing | Financement | How the user plans to finance | enum | BUY transaction | CASH, LOAN, MORTGAGE, ASSISTANCE | Normalize "comptant"→CASH, "credit"→LOAN | "Comptant ou crédit ?" | transaction_blocker | confidential | RESIDENTIAL_SEARCH, LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-SOURCE_FINANCEMENT | Funding Source | Source financement | Origin of funds | enum | BUY or FINANCE | CASH, CREDIT_BANK, TONTINE, DIASPORA, FAMILY_LOAN | Normalize to standard categories | "Comment comptez-vous financer ?" | informational_only | sensitive | LAND_SEARCH, FINANCING_REQUEST | HERITAGE_VALIDATED |
| FLD-APPORT | Down Payment | Apport personnel | Amount the user can put as down payment | integer | BUY or FINANCE | > 0; < total_price | Percentage of total calculated | "Quel apport personnel ?" | hard_constraint | sensitive | FINANCING_REQUEST, LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-REVENUS | Income | Revenus | Monthly or annual income | integer | FINANCING_REQUEST | > 0 | Normalize to monthly | "Quels sont vos revenus mensuels ?" | soft_constraint | sensitive | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FLD-REVENUS_SOURCE | Income Source | Source de revenus | Where income comes from | enum | FINANCING_REQUEST | SALARY, FREELANCE, BUSINESS, RENTAL, DIASPORA_TRANSFERS, PENSION | Multi-select allowed | "Quelle est votre source de revenus ?" | informational_only | sensitive | FINANCING_REQUEST | HERITAGE_NORMALIZED |
| FLD-GARANTIES | Guarantees | Garanties | Types of guarantees available | enum[] | FINANCING_REQUEST | TITLE_DEED, MORTGAGE, SURETY, PLEDGE, INSURANCE, DEPOSIT, NONE | Multi-select | "Quelles garanties pouvez-vous offrir ?" | soft_constraint | sensitive | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FLD-MONTANT_RECHERCHE | Amount Sought | Montant recherché | Amount of financing being sought | integer | FINANCING_REQUEST | > 0; <= total_project_cost | Must be less than or equal to cost | "Quel montant souhaitez-vous emprunter ?" | hard_constraint | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FLD-COUT_TOTAL_PROJET | Total Project Cost | Coût total projet | Complete project cost | integer | FINANCING_REQUEST | > montant_recherche | Must include all costs | "Quel est le coût total du projet ?" | hard_constraint | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FLD-DUREE_SOUHAITEE | Desired Duration | Durée souhaitée | Desired loan repayment period | enum | FINANCING_REQUEST | 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 15Y, 20Y, 25Y | Normalize to months | "Sur quelle durée ?" | soft_constraint | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FLD-TAUX_SOUHAITE | Desired Rate | Taux souhaité | Desired interest rate or repayment capacity | float | FINANCING_REQUEST (optional) | 0-100 | Percentage or monthly amount | "Quelle capacité de remboursement ?" | soft_constraint | sensitive | FINANCING_REQUEST | HERITAGE_NORMALIZED |
| FLD-RENDEMENT_ATTENDU | Expected Yield | Rendement attendu | Target annual return on investment | float | INVESTMENT | 0-100% | Percentage format | "Quel rendement annuel visez-vous ?" | hard_constraint | private | COMMERCIAL_SEARCH (INVEST) | EXPERT_PROPOSAL |
| FLD-RISQUE_ACCEPTE | Risk Tolerance | Risque accepté | How much risk the investor accepts | enum | INVESTMENT | VERY_LOW, LOW, MEDIUM, HIGH, VERY_HIGH | Map user language to risk level | "Quel niveau de risque ?" | soft_constraint | private | COMMERCIAL_SEARCH (INVEST) | EXPERT_PROPOSAL |

---

## 4. Property Characteristic Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| FLD-CHAMBRES | Bedrooms | Chambres | Number of bedrooms | integer | multi-room properties | 1-10+ | Must be integer; "studio"→0 | "Combien de chambres ?" | soft_constraint | public | RESIDENTIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-DOUCHES | Bathrooms | Douches | Number of bathrooms/shower rooms | integer | always | 1-5+ | Must be integer | "Combien de douches ?" | soft_constraint | public | RESIDENTIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-SALONS | Living Rooms | Salons | Number of living rooms | integer | appartement | 0-5 | 0 for studio | "Combien de salons ?" | soft_constraint | public | RESIDENTIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-CUISINE | Kitchen | Cuisine | Type of kitchen | enum | always | INTERNE, EXTERNE, EQUIPEE, NON_EQUIPEE, INDIFFERENT | Map user preference | "Quel type de cuisine ?" | soft_constraint | public | RESIDENTIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-MEUBLE | Furnished | Meublé | Whether the property is furnished | enum | always for residential | MEUBLE, NON_MEUBLE, SEMI_MEUBLE, INDIFFERENT | Derived from property type for some types | "Meublé ou non meublé ?" | soft_constraint | public | RESIDENTIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-SURFACE | Living Area | Surface habitable | Usable living area in square meters | integer | optional | 10-1000 m2 | Normalize units (sqft→m2) | "Quelle surface souhaitez-vous ?" | soft_constraint | public | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-SURFACE_TERRAIN | Land Area | Surface terrain | Land area in square meters | integer | LAND_SEARCH | 50-10000 m2 | Normalize units | "Quelle surface de terrain ?" | soft_constraint | public | LAND_SEARCH, RESIDENTIAL_SEARCH (villa) | HERITAGE_NORMALIZED |
| FLD-ETAGE | Floor Level | Étage | Preferred floor level | enum | building properties | REZ_DE_CHAUSSEE, BAS, MILIEU, HAUT, TOIT_TERRASSE, INDIFFERENT | Map "rdc"→REZ_DE_CHAUSSEE | "À quel étage ?" | ranking_preference | public | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-ASCENSEUR | Elevator | Ascenseur | Whether elevator is needed | boolean | etage > 2 | true, false, INDIFFERENT | Conditional on etage | "Ascenseur nécessaire ?" | ranking_preference | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-PARKING | Parking | Parking | Whether parking is needed | enum | all types | OUI, NON, INDIFFERENT, GARAGE | Map "garage"→GARAGE | "Besoin de parking ?" | soft_constraint | public | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-COUR | Courtyard | Cour | Whether a courtyard is needed | boolean | ground-floor | true, false, INDIFFERENT | Conditional on property type | "Cour nécessaire ?" | ranking_preference | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-CLOTURE | Fence | Clôture | Whether fencing is needed | boolean | optional | true, false, INDIFFERENT | Land or villa properties | "Clôture importante ?" | soft_constraint | public | RESIDENTIAL_SEARCH, LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-BALCON | Balcony | Balcon | Whether a balcony is desired | boolean | optional | true, false, INDIFFERENT | Higher priority for apartments | "Balcon souhaité ?" | ranking_preference | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-JARDIN | Garden | Jardin | Whether a garden is desired | boolean | ground-floor villa | true, false, INDIFFERENT | Conditional on property type | "Jardin important ?" | ranking_preference | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-PISCINE | Swimming Pool | Piscine | Whether a pool is desired | boolean | optional | true, false, INDIFFERENT | High-end properties | "Piscine ?" | ranking_preference | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-CLIMATISATION | Air Conditioning | Climatisation | Whether AC is needed | boolean | hot cities | true, false, INDIFFERENT | Conditional on city climate | "Climatisation nécessaire ?" | soft_constraint | public | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-GROUPE_ELECTROGENE | Generator | Groupe électrogène | Whether a generator is needed | boolean | high power-cut zones | true, false, INDIFFERENT | Conditional on city infrastructure | "Groupe électrogène nécessaire ?" | boost (+10) | public | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-FORAGE | Water Well | Forage | Whether a water well is needed/available | boolean | water-scarce areas | true, false, INDIFFERENT | Conditional on water infrastructure | "Forage disponible ?" | boost (+10) | public | RESIDENTIAL_SEARCH, LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-INTERNET | Internet | Internet | Whether internet is needed | boolean | digital workers | true, false, INDIFFERENT | Higher priority for professionals | "Besoin d'internet ?" | ranking_preference | public | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-SECURITE | Security | Sécurité | Whether security is important | boolean | optional | true, false, INDIFFERENT | Higher for certain neighborhoods | "Sécurité importante ?" | soft_constraint | public | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-GARDIENNAGE | Guard Service | Gardiennage | Whether a guard is needed | boolean | high-end | true, false, INDIFFERENT | Higher for large properties | "Gardiennage ?" | boost (+10) | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-EAU | Water Supply | Eau | Type of water supply | enum | all types | PERMANENTE, INTERMITTENTE, FORAGE, INDIFFERENT | Conditional on city infrastructure | "Accès à l'eau important ?" | soft_constraint | public | RESIDENTIAL_SEARCH, LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-ELECTRICITE | Electricity | Électricité | Type of electricity supply | enum | all types | PERMANENTE, INTERMITTENTE, GROUPE, SOLAIRE, INDIFFERENT | Conditional on city infrastructure | "Électricité importante ?" | soft_constraint | public | RESIDENTIAL_SEARCH, LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-ACCES_ROUTE | Road Access | Accès route | Type of road access | enum | land, villa | GOUDRONNEE, PISTE, INDIFFERENT | Conditional on location | "Accès route ?" | ranking_preference | public | RESIDENTIAL_SEARCH, LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-DEPENDANCES | Outbuildings | Dépendances | Additional structures on the property | string | optional | Free text | Free text | "Y a-t-il des dépendances ?" | informational_only | public | RESIDENTIAL_SEARCH | EXPERT_PROPOSAL |
| FLD-ETAT_PROPRIETE | Property Condition | État du bien | Overall condition of the property | enum | optional | NEUF, TRES_BON, BON, A_RENOVER, BRUT | Map user description | "Quel est l'état du bien ?" | ranking_preference | public | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | EXPERT_PROPOSAL |

---

## 5. Contact & Identity Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| FLD-NOM | Name | Nom | User's full name | string | INTRODUCTION_READY | Min 2 chars; no special chars | Capitalize properly | "Quel est votre nom ?" | informational_only | private | RESIDENTIAL_SEARCH, LAND_SEARCH, COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-TELEPHONE | Phone Number | Téléphone | User's phone number | string | INTRODUCTION_READY | Valid phone regex; 8-15 digits | Normalize to international format (+237XXXXXXX) | "Quel est votre numéro de téléphone ?" | verification_only | private | RESIDENTIAL_SEARCH, LAND_SEARCH, COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-EMAIL | Email | Email | User's email address | string | INTRODUCTION_READY (optional for most) | Valid email regex | Lowercase; remove spaces | "Quel est votre email ?" | informational_only | private | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH, FINANCING_REQUEST | HERITAGE_NORMALIZED |
| FLD-CANAL_PREFERE | Preferred Channel | Canal préféré | User's preferred communication channel | enum | INTRODUCTION_READY | WHATSAPP, TELEGRAM, SMS, EMAIL, APPEL | Map user preference | "Quel canal préférez-vous ?" | informational_only | private | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-LANGUE | Language | Langue | User's preferred language | enum | INTRODUCTION_READY | FRANCAIS, ANGLAIS, PIDGIN | Auto-detect from first messages | "Quelle langue préférez-vous ?" | informational_only | private | RESIDENTIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-PROFIL_DEMANDEUR | Requester Profile | Profil demandeur | Type of person making the request | enum | FINANCING_REQUEST | SALARIE, INDEPENDANT, ENTREPRISE, INVESTISSEUR, DIASPORA, PROMOTEUR | Map from employment description | "Quel est votre profil ?" | soft_constraint | private | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FLD-IDENTITE_PROFESSIONNEL | Professional Identity | Identité professionnel | Professional's full identity | string | PROFESSIONAL_SEARCH | Min 2 chars | Capitalize | "Qui êtes-vous ?" | informational_only | private | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| FLD-NUMERO_CARTE_PRO | Professional Card Number | Numéro carte professionnelle | Official professional card number | string | regulated professions | Valid format per profession | Validate against known formats | "Quel est votre numéro de carte professionnelle ?" | verification_only | sensitive | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| FLD-ASSUREUR | Insurance | Assurance professionnelle | Professional insurance proof | boolean | regulated professions | true, false | Verify document | "Avez-vous une assurance professionnelle ?" | verification_only | private | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| FLD-REGISTRE_COMMERCE | Business Registry | Registre de commerce | Business registration number | string | business entities | Valid RCCM format | Normalize to standard format | "Quel est votre numéro RCCM ?" | verification_only | private | PROFESSIONAL_SEARCH, COMMERCIAL_SEARCH | HERITAGE_VALIDATED |

---

## 6. Timing & Availability Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| FLD-DISPONIBILITE | Availability Date | Disponibilité | When the user wants to move in or start | date | INTRODUCTION_READY | Must be future date or relative | Normalize relative dates (now→today, next week→+7d) | "À partir de quand ?" | soft_constraint | private | RESIDENTIAL_SEARCH | HERITAGE_VALIDATED |
| FLD-DELAI | Time Horizon | Délai | General time horizon for the search | enum | always | IMMEDIATE, <1_MONTH, 1-3_MONTHS, 3-6_MONTHS, NO_RUSH | Derived from user language | "Quel est votre délai ?" | ranking_preference | private | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-URGENCE | Urgency | Urgence | How urgent the request is | enum | optional | URGENT, MODERATE, NOT_URGENT | Derived from language + delay | "Est-ce urgent ?" | ranking_preference | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-DATE_ARRIVEE | Arrival Date | Date d'arrivée | Date of arrival for short stays | date | short-term rental | Valid date | Normalize | "Quand arrivez-vous ?" | soft_constraint | private | RESIDENTIAL_SEARCH (short-term) | HERITAGE_NORMALIZED |
| FLD-DATE_DEPART | Departure Date | Date de départ | Date of departure for short stays | date | short-term rental | After arrival date | Calculate duration | "Quand partez-vous ?" | soft_constraint | private | RESIDENTIAL_SEARCH (short-term) | HERITAGE_NORMALIZED |
| FLD-DUREE_LOCATION | Rental Duration | Durée location | Intended rental duration | enum | rent | COURT_TERME, MOYEN_TERME, LONG_TERME, INDIFFERENT | Derived from property type + user | "Pour quelle durée ?" | ranking_preference | private | RESIDENTIAL_SEARCH | EXPERT_PROPOSAL |
| FLD-DUREE_SEJOUR | Stay Duration | Durée séjour | Length of short-term stay | enum | short-term | NUIT, WEEKEND, SEMAINE, 2_SEMAINES, MOIS, LONG_SEJOUR | Derived from dates | "Combien de temps ?" | ranking_preference | public | RESIDENTIAL_SEARCH (short-term) | HERITAGE_VALIDATED |
| FLD-DELAI_SOUHAITE | Desired Timeline | Délai souhaité | User's desired timeline for financing | enum | FINANCING_REQUEST | URGENT, 1W, 2W, 1M, 2M, 3M, 6M, NO_DEADLINE | Map to standard durations | "Dans quel délai ?" | ranking_preference | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FLD-DATE_SOUHAITEE | Desired Date | Date souhaitée | When the user wants service to start | date | PROFESSIONAL_SEARCH, REAL_ESTATE_SERVICES | Must be future | Normalize | "À quelle date souhaitez-vous commencer ?" | soft_constraint | public | PROFESSIONAL_SEARCH, REAL_ESTATE_SERVICES | HERITAGE_VALIDATED |
| FLD-HORAIRE_VISITE | Visit Time | Horaire visite | Preferred time for property visit | string | VISIT_READY | Valid time format | Normalize to HH:MM | "Quand êtes-vous disponible pour visiter ?" | informational_only | private | RESIDENTIAL_SEARCH, LAND_SEARCH | EXPERT_PROPOSAL |

---

## 7. Residential-Specific Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| FLD-NOMBRE_PERSONNES | Number of People | Nombre de personnes | How many people will occupy the property | integer | colocation, family | 1-20 | Must be integer | "Combien de personnes ?" | soft_constraint | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-PETIT_DEJEUNER | Breakfast | Petit-déjeuner | Whether breakfast is included (short-term) | boolean | hotel-type | true, false, INDIFFERENT | Short-term only | "Petit-déjeuner inclus ?" | ranking_preference | public | RESIDENTIAL_SEARCH (hotel) | HERITAGE_NORMALIZED |
| FLD-MENAGE | Housekeeping | Ménage | Whether housekeeping is included | boolean | short-term | true, false, INDIFFERENT | Short term only | "Ménage inclus ?" | ranking_preference | public | RESIDENTIAL_SEARCH (short-term) | HERITAGE_NORMALIZED |
| FLD-SERVICES_INCLUS | Included Services | Services inclus | Which services are included | string | short-term | Free text | Tag-based extraction | "Quels services sont inclus ?" | informational_only | public | RESIDENTIAL_SEARCH (short-term) | HERITAGE_NORMALIZED |
| FLD-LINGE | Linen | Linge | Whether linen is provided | boolean | short-term | true, false, INDIFFERENT | Short term only | "Linge fourni ?" | informational_only | public | RESIDENTIAL_SEARCH (short-term) | EXPERT_PROPOSAL |
| FLD-GENRE_PREFERENCE | Gender Preference | Préférence genre | Preferred gender of co-tenants | enum | colocation | MIXTE, HOMMES, FEMMES, INDIFFERENT | Sensitive field; ask carefully | "Préférence de genre pour la colocation ?" | soft_constraint | sensitive | RESIDENTIAL_SEARCH (colocation) | HERITAGE_NORMALIZED |
| FLD-AGE_RANGE | Age Range | Tranche d'âge | Preferred age range of co-tenants | string | colocation | Free text | Sensitive field | "Tranche d'âge des colocataires ?" | informational_only | sensitive | RESIDENTIAL_SEARCH (colocation) | EXPERT_PROPOSAL |
| FLD-NOMBRE_COLOCATAIRES | Number of Co-tenants | Nombre colocataires | Number of people in a colocation | integer | colocation | 2-10 | Must be integer | "Combien serez-vous ?" | soft_constraint | public | RESIDENTIAL_SEARCH (colocation) | HERITAGE_NORMALIZED |
| FLD-ESPACES_PARTAGES | Shared Spaces | Espaces partagés | Which spaces are shared in colocation | string | colocation | Free text | Tag extraction | "Quels espaces partagez-vous ?" | informational_only | public | RESIDENTIAL_SEARCH (colocation) | HERITAGE_NORMALIZED |
| FLD-REGLEMENT_INTERIEUR | Internal Rules | Règlement intérieur | House rules for colocation | string | colocation | Free text | Free text | "Y a-t-il un règlement intérieur ?" | informational_only | public | RESIDENTIAL_SEARCH (colocation) | EXPERT_PROPOSAL |
| FLD-UNIVERSITE | University | Université | Target university for student housing | string | cite_universitaire | Free text | Normalize university names | "Pour quelle université ?" | soft_constraint | public | RESIDENTIAL_SEARCH (university) | EXPERT_PROPOSAL |
| FLD-TYPE_CHAMBRE_UNIV | Room Type | Type chambre univ | University room type preference | enum | cite_universitaire | INDIVIDUELLE, PARTAGEE_2, PARTAGEE_3_PLUS, INDIFFERENT | Map user preference | "Type de chambre ?" | soft_constraint | public | RESIDENTIAL_SEARCH (university) | EXPERT_PROPOSAL |
| FLD-RESTAURATION | Meal Plan | Restauration | Whether meals are included at university | boolean | cite_universitaire | true, false, INDIFFERENT | University context | "Restauration incluse ?" | ranking_preference | public | RESIDENTIAL_SEARCH (university) | EXPERT_PROPOSAL |
| FLD-BOURSE | Scholarship | Bourse | Whether the student has a scholarship | boolean | cite_universitaire | true, false | Sensitive financial info | "Avez-vous une bourse ?" | informational_only | sensitive | RESIDENTIAL_SEARCH (university) | EXPERT_PROPOSAL |
| FLD-ANNEE_ETUDES | Year of Study | Année d'études | Current academic year | string | cite_universitaire | Free text | Normalize | "Quelle année d'études ?" | informational_only | public | RESIDENTIAL_SEARCH (university) | EXPERT_PROPOSAL |

---

## 8. Land-Specific Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| FLD-TITRE_REQUIS | Title Required | Titre requis | Whether the user requires a formal land title | boolean | LAND_SEARCH | true, false | Map preference | "Exigez-vous un titre foncier ?" | hard_constraint | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-TYPE_TITRE | Title Type | Type de titre | Type of land documentation | enum | LAND_SEARCH | TITRE_FONCIER, ATTESTATION, CONCESSION, CERTIFICAT_OCCUPATION, NON_DOCUMENTE | Map document types | "Quel type de document ?" | soft_constraint | sensitive | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-NUM_TITRE | Title Number | Numéro titre | Land title registration number | string | TRANSACTION_READY for titled land | Valid title format | Normalize; verify format | "Quel est le numéro du titre foncier ?" | verification_only | confidential | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-SURFACE_TERRAIN_M2 | Land Area m2 | Surface terrain m2 | Land area in square meters | float | LAND_SEARCH | > 0 | Convert from hectares if needed | "Quelle surface (en m2) ?" | soft_constraint | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-USAGE_PREVU | Intended Use | Usage prévu | Planned use for the land | enum | LAND_SEARCH | HABITATION, COMMERCE, INDUSTRIE, AGRICULTURE, MIXTE | Map user description | "Quel usage prévu ?" | hard_constraint | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-TERRAIN_LOTI | Serviced Land | Terrain loti | Whether land is serviced (roads, utilities) | boolean | LAND_SEARCH | true, false | Derived or asked explicitly | "Le terrain est-il loti ?" | soft_constraint | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-TERRAIN_CONSTRUCTIBLE | Buildable | Terrain constructible | Whether the land is zoned for construction | boolean | LAND_SEARCH | true, false | Check zoning rules for area | "Le terrain est-il constructible ?" | soft_constraint | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-LOTISSEMENT_APPROUVE | Subdivision Approved | Lotissement approuvé | Whether subdivision is municipally approved | boolean | terrain_loti | true, false | Verify with municipal records | "Le lotissement est-il approuvé ?" | verification_only | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-INONDABLE | Flood Zone | Zone inondable | Whether land is in a flood-prone area | boolean | LAND_SEARCH (recommended) | true, false | Cross-check with known flood zones | "Le terrain est-il en zone inondable ?" | soft_constraint | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-TOPOGRAPHIE | Topography | Topographie | Land terrain type | enum | LAND_SEARCH (recommended) | PLAT, LEGERE_PENTE, FORTE_PENTE, VALLEE, COLLINE | Map user description | "Quelle est la topographie ?" | ranking_preference | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-ACCESSIBILITE_ROUTE | Road Accessibility | Accessibilité route | Quality of road access to the land | enum | LAND_SEARCH | ROUTE_GOUDRONNEE, ROUTE_TERRE, SENTIER, ENCLAVE | Map to standard categories | "Comment est l'accès ?" | ranking_preference | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-DISTANCE_ROUTE | Road Distance | Distance route | Distance from main road in meters | float | LAND_SEARCH | > 0 | Validate range | "Distance de la route ?" | ranking_preference | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-OCCUPATION_ACTUELLE | Current Occupation | Occupation actuelle | What the land is currently used for | enum | LAND_SEARCH | LIBRE, CULTIVE, BATI, EN_FRICHE | Map user description | "Le terrain est-il occupé actuellement ?" | informational_only | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-SERVITUDES | Easements | Servitudes | Existing easements or rights of way | string | LAND_SEARCH (conditional) | Free text | Requires legal review | "Y a-t-il des servitudes ?" | informational_only | sensitive | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-LITIGES_CONNUS | Known Disputes | Litiges connus | Whether there are known legal disputes | boolean | TRANSACTION_READY | true, false | Escalate to legal if true | "Existe-t-il des litiges connus ?" | transaction_blocker | confidential | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-HYPOTHEQUE | Mortgage/Encumbrance | Hypothèque | Whether there is a mortgage or charge | boolean | TRANSACTION_READY | true, false | Check with conservatoire foncier | "Y a-t-il une hypothèque ?" | transaction_blocker | confidential | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-SIGNATAIRES_NOMBRE | Number of Signatories | Nombre signataires | How many people must sign the sale | integer | collective title | > 0 | Must match title document | "Combien de signataires ?" | verification_only | sensitive | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-IDENTITE_SIGNATAIRES | Signatory Identity | Identité signataires | Identity of all required signatories | string | collective title | Free text | RGPD protected | "Qui sont les signataires ?" | verification_only | confidential | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-PROCURATION | Power of Attorney | Procuration | Whether a power of attorney is involved | boolean | signatory not available | true, false | Verify notarial validity | "Y a-t-il une procuration ?" | verification_only | confidential | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-BORNAGE | Boundary Survey | Bornage | Whether boundary marking has been done | boolean | LAND_SEARCH (optional) | true, false | Check with geometre | "Le bornage a-t-il été fait ?" | informational_only | public | LAND_SEARCH | HERITAGE_VALIDATED |
| FLD-CERTIFICAT_URBANISME | Town Planning Certificate | Certificat d'urbanisme | Whether town planning certificate exists | boolean | constructible land | true, false | Verify with municipal office | "Certificat d'urbanisme disponible ?" | verification_only | sensitive | LAND_SEARCH | HERITAGE_VALIDATED |

---

## 9. Commercial-Specific Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| COM-COMMON-001 | Business Activity | Activité prévue | Type of business planned for the location | string | always for commercial | Min 3 chars | Normalize activity categories | "Quel type d'activité ?" | hard_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-002 | Permitted Use | Activité autorisée | Permitted use per zoning regulations | string | if sensitive activity | Match against zoning rules | Cross-reference with city zoning | "Usage autorisé ?" | hard_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-003 | Minimum Surface | Surface minimale | Minimum required floor area in m2 | integer | always for commercial | Min 5, max 50000 | Normalize units | "Surface minimale ?" | hard_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-004 | Maximum Surface | Surface maximale | Maximum floor area in m2 | integer | if surface provided | Max 100000 | Must be > minimum | "Surface maximale ?" | ranking_preference | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-009 | Ceiling Height | Hauteur sous plafond | Minimum ceiling height in meters | float | warehouse/workshop | 2.0-20.0 | Convert from feet if needed | "Hauteur sous plafond ?" | soft_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-010 | Vehicle Access | Accès véhicules | Type of vehicle access needed | enum | warehouse/industrial | POIDS_LOURDS, LIVRAISONS, UTILITAIRE, VOITURE, AUCUN | Map to categories | "Accès véhicules ?" | soft_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-011 | Road Visibility | Visibilité route | Whether the location is visible from the road | boolean | boutique/magasin | true, false | Binary | "Visible depuis la route ?" | ranking_preference | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-012 | Storefront Width | Façade | Width of storefront in meters | float | boutique/magasin | 1.0-50.0 | Must be positive | "Largeur de la façade ?" | ranking_preference | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-013 | Foot Traffic | Flux passage | Level of pedestrian traffic | enum | boutique/restaurant/bar | TRES_ELEVE, ELEVE, MOYEN, FAIBLE, AUCUN | Map to categories | "Flux piéton ?" | ranking_preference | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-014 | Parking Need | Parking | Whether parking is needed | enum | restaurant/hotel/bar | INDISPENSABLE, SOUHAITE, OPTIONNEL, PAS_BESOIN | Map urgency | "Parking nécessaire ?" | soft_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-015 | Parking Spaces | Places parking | Number of parking spots needed | integer | parking indispensable | 1-500 | Must be integer | "Combien de places ?" | soft_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-016 | Storage Need | Stockage | Whether storage space is needed | boolean | magasin/entrepot | true, false | Binary | "Stockage nécessaire ?" | ranking_preference | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-018 | Electricity | Électricité | Whether electricity is available | boolean | always for commercial | true, false | Standard commercial requirement | "Électricité disponible ?" | soft_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-019 | Power Capacity | Puissance électrique | Electrical power in kVA | integer | workshop/restaurant/industrial | 1-5000 | Validate requirement | "Puissance électrique nécessaire ?" | soft_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-020 | Water Supply | Eau | Whether water supply is available | boolean | restaurant/bar/hotel/workshop | true, false | Standard requirement | "Eau courante ?" | soft_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-021 | Operating License | Licence exploitation | Type of operating license needed | enum | restaurant/bar/hotel | LICENCE_ALCOOL, LICENCE_RESTAURATION, PATENTE, AGREMENT, AUCUNE | Map to regulations | "Licence nécessaire ?" | hard_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-024 | Goodwill Included | Fonds commerce | Whether the business goodwill is included | boolean | transaction=cession | true, false | Conditional on transfer | "Fonds de commerce inclus ?" | soft_constraint | sensitive | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-026 | Commercial Zone | Zone commerciale | Type of commercial zone | enum | always for commercial | CENTRE_VILLE, ZONE_INDUSTRIELLE, PERIPHERIE, AXE_PRINCIPAL, RESIDENTIEL | Map to zone type | "Type de zone commerciale ?" | soft_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-031 | PMR Accessibility | Accès PMR | Whether the location is mobility-accessible | boolean | hotel/restaurant/bureau | true, false | Regulatory requirement | "Accès PMR ?" | soft_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-035 | Number of Rooms | Nombre pièces | Number of rooms/offices needed | integer | bureau | 1-200 | Must be integer | "Combien de pièces ?" | ranking_preference | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-036 | Floor Level | Étage | Preferred floor level | enum | boutique/magasin | RDC, 1ER, 2EME, 3EME_PLUS, SOUS_SOL | Map to categories | "Quel étage ?" | soft_constraint | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-038 | Time Horizon | Délai | Desired time to find/locate property | enum | general | URGENT_1S, RAPIDE_1M, NORMAL_3M, FLEXIBLE_6M, PAS_DELAI | Map to periods | "Quel délai ?" | ranking_preference | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |
| COM-COMMON-043 | Number of Employees | Nombre employés | Number of employees to accommodate | integer | bureau/commercial | 0-1000 | Must be integer | "Combien d'employés ?" | ranking_preference | public | COMMERCIAL_SEARCH | HERITAGE_VALIDATED |

---

## 10. Financing-Specific Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| FIN-COMMON-001 | Financing Purpose | Objet financement | Purpose of the financing request | enum | always for financing | ACHAT, CONSTRUCTION, RENOVATION, PROMOTION, FONDS_ROULEMENT, EQUIPEMENT, REFINANCEMENT, INVESTISSEMENT | Map to categories | "Quel est l'objet de votre demande ?" | hard_constraint | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-COMMON-006 | Desired Timeline | Délai souhaité | When financing is needed by | enum | always for financing | URGENT, 1_SEMAINE, 2_SEMAINES, 1_MOIS, 2_MOIS, 3_MOIS, 6_MOIS, PAS_DE_DELAI | Map to periods | "Dans quel délai ?" | ranking_preference | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-COMMON-009 | Acquisition Status | Statut acquisition | Whether the property is already found | enum | always for financing | DEJA_ACQUISE, EN_COURS_NEGOCIATION, PAS_ENCORE_TROUVE | Map to status | "Avez-vous déjà trouvé le bien ?" | informational_only | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-COMMON-010 | Requester Profile | Profil demandeur | Type of financing requester | enum | always for financing | SALARIE, INDEPENDANT, ENTREPRISE, INVESTISSEUR, DIASPORA, PROMOTEUR | Map from profile | "Quel est votre profil ?" | soft_constraint | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-COMMON-011 | Loan Duration | Durée souhaitée | Desired loan repayment period | enum | important for matching | 6M, 1A, 2A, 3A, 5A, 7A, 10A, 15A, 20A, 25A | Normalize to months | "Sur quelle durée ?" | soft_constraint | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-COMMON-013 | Monthly Income | Revenus mensuels | Total monthly income | number | salaried/self-employed | Min 0 | Normalize to monthly | "Quels sont vos revenus mensuels ?" | soft_constraint | sensitive | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-COMMON-015 | Income Sources | Source revenus | Sources of income | enum[] | important for evaluation | SALAIRE, HONORAIRES, CA, LOYERS, DIVIDENDES, PENSIONS, TRANSFERTS_DIASPORA, AUTRES | Multi-select | "Quelles sont vos sources de revenus ?" | informational_only | public | FINANCING_REQUEST | HERITAGE_NORMALIZED |
| FIN-COMMON-016 | Other Commitments | Autres engagements | Existing financial commitments | number | recommended | Min 0 | Add to debt calculation | "Avez-vous d'autres engagements ?" | soft_constraint | sensitive | FINANCING_REQUEST | HERITAGE_NORMALIZED |
| FIN-COMMON-018 | Available Guarantees | Garanties disponibles | Types of guarantees the requester can offer | enum[] | important for matching | TITRE_FONCIER, HYPOTHEQUE, CAUTION, NANTISSEMENT, CAUTION_SOLIDAIRE, ASSURANCE, DEPOT_GARANTIE, PAS_DE_GARANTIE | Multi-select | "Quelles garanties pouvez-vous offrir ?" | soft_constraint | sensitive | FINANCING_REQUEST | HERITAGE_NORMALIZED |
| FIN-CONS-001 | Land Available | Terrain disponible | Whether land is already available for construction | boolean | construction financing | true, false | Binary | "Avez-vous déjà un terrain ?" | hard_constraint | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-CONS-002 | Land Legal Status | Statut juridique terrain | Legal status of construction land | enum | construction with land | TITRE_FONCIER, PROMESSE_VENTE, ACTE_VENTE, CERTIFICAT_OCCUPATION, BAIL_EMPHYTEOTIQUE, TERRAIN_FAMILIAL, PAS_DE_TITRE, NE_SAIS_PAS | Map to categories | "Quel est le statut juridique ?" | soft_constraint | sensitive | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-CONS-005 | Plans Available | Plans disponibles | Whether architectural plans exist | boolean | construction financing | true, false | Binary | "Avez-vous des plans ?" | informational_only | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-CONS-007 | Building Permits | Permis autorisations | Status of building permits | enum[] | construction financing | PERMIS_CONSTRUIRE, CERTIFICAT_CONFORMITE, AUTORISATION_URBANISME, PERMIS_DEVELOPPER, PAS_ENCORE, NE_SAIS_PAS | Multi-select | "Avez-vous les autorisations ?" | soft_constraint | sensitive | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-CONS-013 | Construction Timeline | Calendrier travaux | Planned construction timeline | enum | construction financing | DEMARRAGE_IMMEDIAT, 1_MOIS, 3_MOIS, 6_MOIS, 12_MOIS, PLUS_12_MOIS | Map to periods | "Quand prévoyez-vous commencer ?" | informational_only | public | FINANCING_REQUEST | HERITAGE_VALIDATED |
| FIN-CONS-015 | Progress Level | Niveau avancement | Current construction progress level | enum | construction/renovation | PAS_COMMENCE, FONDATIONS, GROS_OEUVRE, SECOND_OEUVRE, FINITIONS, RENOVATION_PARTIELLE, RENOVATION_COMPLETE | Map to categories | "Où en êtes-vous ?" | informational_only | public | FINANCING_REQUEST | HERITAGE_VALIDATED |

---

## 11. Professional Service Fields

| field_id | canonical_label | french_label | description | data_type | mandatory_when | validation_rules | normalization_rules | question_template_short | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|----------------|------------------|---------------------|------------------------|---------------|---------------|------------|--------|
| PRO-COMMON-001 | Service Type | Type de prestation | Type of professional service needed | enum | always for professional | RECHERCHE_PROFESSIONNEL, MISE_EN_RELATION, DEVIS_MULTIPLE, CONSULTATION, URGENCE | Map to categories | "Quel type de service ?" | hard_constraint | public | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| PRO-COMMON-002 | Location | Localisation | Where the service is needed | object | always for professional | Valid city + optional sub-location | Geocode if possible | "Où avez-vous besoin de ce service ?" | hard_constraint | public | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| PRO-COMMON-003 | Need Description | Description besoin | Detailed description of the need | text | always for professional | Min 20 chars, max 2000 chars | Extract key requirements | "Décrivez votre besoin en détail." | informational_only | public | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| PRO-COMMON-004 | Urgency Level | Urgence | How urgent the professional need is | enum | always for professional | IMMEDIATE, URGENT_48H, CETTE_SEMAINE, CE_MOIS, PAS_URGENT, PLANIFICATION | Map to SLA | "Quel est le niveau d'urgence ?" | ranking_preference | public | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| PRO-COMMON-005 | Budget Range | Budget fourchette | Budget range for the professional service | object | recommended | Min < max, valid currency | Normalize to local currency | "Quel budget prévoyez-vous ?" | soft_constraint | private | PROFESSIONAL_SEARCH | HERITAGE_NORMALIZED |
| PRO-COMMON-006 | Desired Start Date | Date souhaitée | When the service should start | date | always for professional | Future date | Normalize relative dates | "À partir de quand ?" | soft_constraint | public | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| PRO-COMMON-007 | Property Type | Type bien concerné | Type of property involved | enum | recommended | Full property type list | Map to standard types | "Quel type de bien ?" | soft_constraint | public | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| PRO-COMMON-008 | Mission Scope | Étendue mission | Scope of the professional mission | text | recommended | Free text | Extract deliverables | "Quelle est l'étendue de la mission ?" | informational_only | public | PROFESSIONAL_SEARCH | HERITAGE_NORMALIZED |
| PRO-COMMON-009 | Expected Deliverables | Livrables attendus | Expected output deliverables | array | recommended | Valid deliverable list | Tag extraction | "Quels livrables attendez-vous ?" | informational_only | public | PROFESSIONAL_SEARCH | HERITAGE_NORMALIZED |
| PRO-COMMON-010 | Required Qualifications | Qualification agrément | Required professional certifications | array | conditional | Valid certification list | Match to standard certs | "Quelles qualifications ?" | soft_constraint | public | PROFESSIONAL_SEARCH | HERITAGE_NORMALIZED |
| PRO-COMMON-011 | Experience Required | Expérience souhaitée | Minimum years of experience | integer | conditional | 0-50 | Validate range | "Quelle expérience minimale ?" | soft_constraint | public | PROFESSIONAL_SEARCH | HERITAGE_NORMALIZED |
| PRO-COMMON-012 | Availability Schedule | Disponibilité | When the professional is available | object | recommended | Days, hours, weekend/night | Parse schedule | "Quels sont vos horaires ?" | informational_only | public | PROFESSIONAL_SEARCH | HERITAGE_NORMALIZED |
| PRO-COMMON-013 | Preferred Languages | Langue | Languages the professional should speak | array | recommended | Language list | Match to available | "Quelles langues ?" | ranking_preference | public | PROFESSIONAL_SEARCH | HERITAGE_NORMALIZED |
| PRO-COMMON-014 | Contact Channel | Canal contact | Preferred contact channels | array | recommended | Phone, email, whatsapp, telegram | Map to channels | "Comment préférez-vous être contacté ?" | informational_only | private | PROFESSIONAL_SEARCH | HERITAGE_NORMALIZED |
| PRO-COMMON-015 | Nature of Operation | Nature opération | Type of legal/notarial operation | enum | notaire | PRELIMINAIRE, COMPROMIS_SIGNE, AVANT_CONTRAT, ACTE_PREPARATION, SIGNATURE_IMMINENTE, POST_SIGNATURE, LITIGE | Map to categories | "Quelle est la nature de l'opération ?" | hard_constraint | public | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| PRO-COMMON-016 | Project Type | Type projet | Type of architectural/construction project | enum | architect/engineer | CONSTRUCTION_NEUVE, RENOVATION, EXTENSION, AMENAGEMENT, LOTISSEMENT | Map to categories | "Quel type de projet ?" | hard_constraint | public | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| PRO-COMMON-017 | Work Type | Type travaux | Specific work type for trades | enum | tradesmen | Multiple values per trade | Map to category | "Quel type de travaux ?" | hard_constraint | public | PROFESSIONAL_SEARCH | HERITAGE_VALIDATED |
| PRO-COMMON-018 | Material Preference | Matériau | Preferred material for construction | enum | recommended | BOIS_MASSIF, BETON, METAL, ALUMINIUM, PVC, MIXTE, COMPOSITE | Map to categories | "Quel matériau ?" | ranking_preference | public | PROFESSIONAL_SEARCH | HERITAGE_NORMALIZED |
| PRO-COMMON-019 | Area Concerned | Surface concernée | Area in square meters affected | float | recommended | > 0 | Normalize units | "Quelle surface ?" | soft_constraint | public | PROFESSIONAL_SEARCH | HERITAGE_NORMALIZED |

---

## 12. Derived Fields

| field_id | canonical_label | french_label | description | data_type | derivation_rule | matching_role | privacy_level | categories | source |
|----------|----------------|--------------|-------------|-----------|-----------------|---------------|---------------|------------|--------|
| FLD-DERIVED-STANDING | Estimated Standing | Standing estimé | Estimated property standing level | string | Deduced from budget + neighborhood + property type | informational_only | public | RESIDENTIAL_SEARCH, COMMERCIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-DERIVED-BUDGET_COHERENCE | Budget Coherence | Cohérence budget | Whether budget is coherent with market data | boolean | Compare budget vs market data per type/neighborhood | verification_only | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-DERIVED-URGENCE_REELLE | Real Urgency | Urgence réelle | User's actual urgency level | enum | Deduced from delai + message language + behavior | ranking_preference | public | RESIDENTIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-DERIVED-PROFIL_ACHETEUR | Buyer Profile | Profil acheteur | Type of buyer the user appears to be | string | Deduced from transaction + language + budget | informational_only | public | RESIDENTIAL_SEARCH | EXPERT_PROPOSAL |
| FLD-DERIVED-PRIX_M2_ESTIME | Estimated Price per m2 | Prix au m² estimé | Price per square meter | float | budget / surface (when both available) | informational_only | public | ALL | EXPERT_PROPOSAL |
| FLD-DERIVED-COMPATIBILITE | Compatibility | Compatibilité quartier | How compatible the budget is with the neighborhood | boolean | budget + type + neighborhood market data | verification_only | public | RESIDENTIAL_SEARCH | EXPERT_PROPOSAL |
| FLD-DERIVED-URBANISATION | Urbanization Level | Urbanisation | Level of urbanization of the location | string | Derived from city + neighborhood context | informational_only | public | RESIDENTIAL_SEARCH | EXPERT_PROPOSAL |
| FLD-DERIVED-PROFIL | Requester Profile | Profil demandeur | Deduced profile of the requester | string | message language + references + budget behavior | informational_only | public | RESIDENTIAL_SEARCH | EXPERT_PROPOSAL |
| FLD-DERIVED-RISQUE_JURIDIQUE | Legal Risk | Risque juridique | Legal risk assessment for land | enum | weighted(litiges, succession, indivision, type_document) | informational_only | sensitive | LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-DERIVED-TITRE_OBTENABLE | Title Obtainable | Titre obtenable | Whether a land title can be obtained | boolean | Derived from documents + bornage + urbanisme | informational_only | public | LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-DERIVED-CAPACITE_REMBOURSEMENT | Repayment Capacity | Capacité remboursement | Calculated monthly repayment capacity | float | revenus - engagements | informational_only | sensitive | FINANCING_REQUEST | HERITAGE_NORMALIZED |
| FLD-DERIVED-RATIO_APPORT | Down Payment Ratio | Ratio d'apport | Ratio of down payment to total cost | float | apport / cout_total * 100 | informational_only | public | FINANCING_REQUEST | HERITAGE_NORMALIZED |
| FLD-DERIVED-TAUX_ENDETTEMENT | Debt Ratio | Taux d'endettement | Calculated debt-to-income ratio | float | engagements / revenus * 100 | informational_only | sensitive | FINANCING_REQUEST | HERITAGE_NORMALIZED |
| FLD-DERIVED-SCORE_COMMERCIAL | Commercial Potential | Potentiel commercial | Estimated commercial potential score | float | flux*0.4 + visibilité*0.3 + zone*0.3 | informational_only | public | COMMERCIAL_SEARCH | HERITAGE_NORMALIZED |
| FLD-DERIVED-SCORE_VIABILISATION | Services Score | Score viabilisation | Score for available utilities on land | integer | weighted(eau, electricite, groupe_electrogene) | informational_only | public | LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-DERIVED-COUT_VIABILISATION | Services Cost | Coût viabilisation | Estimated cost to service raw land | float | surface * cost_per_m2_by_zone | informational_only | public | LAND_SEARCH | HERITAGE_NORMALIZED |
| FLD-DERIVED-MATCH_SCORE | Composite Match Score | Score de matching | Overall match score between request and property | float | weighted(city, neighborhood, budget, property_type, title) | informational_only | public | ALL | HERITAGE_VALIDATED |
| FLD-DERIVED-COMPLEXITE_TRANSACTION | Transaction Complexity | Complexité transaction | Complexity level of the transaction | enum | weighted(signataires, consentement, procuration) | informational_only | public | LAND_SEARCH | HERITAGE_NORMALIZED |

---

## 13. Alphabetical Index

| field_id | Section | Line |
|----------|---------|------|
| COM-COMMON-001 | 9 | — |
| COM-COMMON-002 | 9 | — |
| (all field IDs cross-referenced) | — | — |
| FIN-COMMON-001 | 10 | — |
| FIN-CONS-001 | 10 | — |
| FLD-ACCES_ROUTE | 4 | — |
| FLD-ADRESSE_EXACTE | 2 | — |
| FLD-AGE_RANGE | 7 | — |
| FLD-ANNEE_ETUDES | 7 | — |
| FLD-APPORT | 3 | — |
| FLD-ASCENSEUR | 4 | — |
| FLD-BALCON | 4 | — |
| FLD-BORNAGE | 8 | — |
| FLD-BOURSE | 7 | — |
| FLD-BUDGET_CURRENCY | 3 | — |
| FLD-BUDGET_MAX | 3 | — |
| FLD-BUDGET_MIN | 3 | — |
| FLD-BUDGET_NEGOTIABLE | 3 | — |
| FLD-BUDGET_PAR_M2 | 3 | — |
| FLD-BUDGET_TYPE | 3 | — |
| FLD-CANAL_PREFERE | 5 | — |
| FLD-CAUTION | 3 | — |
| FLD-CERTIFICAT_URBANISME | 8 | — |
| FLD-CHAMBRES | 4 | — |
| FLD-CHARGES | 3 | — |
| FLD-CITY | 2 | — |
| FLD-CITY_ALTERNATIVES | 2 | — |
| FLD-CLIMATISATION | 4 | — |
| FLD-CLOTURE | 4 | — |
| FLD-COORDONNEES_GPS | 2 | — |
| FLD-COUR | 4 | — |
| FLD-COUT_TOTAL_PROJET | 3 | — |
| FLD-CUISINE | 4 | — |
| FLD-DATE_ARRIVEE | 6 | — |
| FLD-DATE_DEPART | 6 | — |
| FLD-DATE_SOUHAITEE | 6 | — |
| FLD-DELAI | 6 | — |
| FLD-DELAI_SOUHAITE | 6 | — |
| FLD-DEPENDANCES | 4 | — |
| FLD-DERIVED-BUDGET_COHERENCE | 12 | — |
| FLD-DERIVED-CAPACITE_REMBOURSEMENT | 12 | — |
| FLD-DERIVED-COMPATIBILITE | 12 | — |
| FLD-DERIVED-COMPLEXITE_TRANSACTION | 12 | — |
| FLD-DERIVED-COUT_VIABILISATION | 12 | — |
| FLD-DERIVED-MATCH_SCORE | 12 | — |
| FLD-DERIVED-PRIX_M2_ESTIME | 12 | — |
| FLD-DERIVED-PROFIL | 12 | — |
| FLD-DERIVED-PROFIL_ACHETEUR | 12 | — |
| FLD-DERIVED-RATIO_APPORT | 12 | — |
| FLD-DERIVED-RISQUE_JURIDIQUE | 12 | — |
| FLD-DERIVED-SCORE_COMMERCIAL | 12 | — |
| FLD-DERIVED-SCORE_VIABILISATION | 12 | — |
| FLD-DERIVED-STANDING | 12 | — |
| FLD-DERIVED-TAUX_ENDETTEMENT | 12 | — |
| FLD-DERIVED-TITRE_OBTENABLE | 12 | — |
| FLD-DERIVED-URBANISATION | 12 | — |
| FLD-DERIVED-URGENCE_REELLE | 12 | — |
| FLD-DISPONIBILITE | 6 | — |
| FLD-DISTANCE_ROUTE | 8 | — |
| FLD-DOUCHES | 4 | — |
| FLD-DUREE_LOCATION | 6 | — |
| FLD-DUREE_SEJOUR | 6 | — |
| FLD-DUREE_SOUHAITEE | 3 | — |
| FLD-EAU | 4 | — |
| FLD-ELECTRICITE | 4 | — |
| FLD-EMAIL | 5 | — |
| FLD-ESPACES_PARTAGES | 7 | — |
| FLD-ETAGE | 4 | — |
| FLD-ETAT_PROPRIETE | 4 | — |
| FLD-FINANCING | 3 | — |
| FLD-FORAGE | 4 | — |
| FLD-GARANTIES | 3 | — |
| FLD-GARDIENNAGE | 4 | — |
| FLD-GENRE_PREFERENCE | 7 | — |
| FLD-GROUPE_ELECTROGENE | 4 | — |
| FLD-HORAIRE_VISITE | 6 | — |
| FLD-HYPOTHEQUE | 8 | — |
| FLD-IDENTITE_SIGNATAIRES | 8 | — |
| FLD-INONDABLE | 8 | — |
| FLD-INTENT | 1 | — |
| FLD-INTENT_CONFIDENCE | 1 | — |
| FLD-INTENT_SOURCE | 1 | — |
| FLD-INTERNET | 4 | — |
| FLD-JARDIN | 4 | — |
| FLD-JOURNEY_STAGE | 1 | — |
| FLD-LANGUE | 5 | — |
| FLD-LINGE | 7 | — |
| FLD-LITIGES_CONNUS | 8 | — |
| FLD-LOTISSEMENT_APPROUVE | 8 | — |
| FLD-MENAGE | 7 | — |
| FLD-MEUBLE | 4 | — |
| FLD-MOBILITY | 2 | — |
| FLD-MONTANT_RECHERCHE | 3 | — |
| FLD-NEIGHBORHOOD | 2 | — |
| FLD-NEIGHBORHOOD_ALTERNATIVES | 2 | — |
| FLD-NOM | 5 | — |
| FLD-NOMBRE_COLOCATAIRES | 7 | — |
| FLD-NOMBRE_PERSONNES | 7 | — |
| FLD-NUM_TITRE | 8 | — |
| FLD-OCCUPATION_ACTUELLE | 8 | — |
| FLD-PARKING | 4 | — |
| FLD-PETIT_DEJEUNER | 7 | — |
| FLD-PISCINE | 4 | — |
| FLD-PROCURATION | 8 | — |
| FLD-PROPERTY_TYPE | 1 | — |
| FLD-PROPERTY_TYPE_CONFIDENCE | 1 | — |
| FLD-PROXIMITY_PREFERENCES | 2 | — |
| FLD-REGLEMENT_INTERIEUR | 7 | — |
| FLD-RENDEMENT_ATTENDU | 3 | — |
| FLD-RESTAURATION | 7 | — |
| FLD-REVENUS | 3 | — |
| FLD-REVENUS_SOURCE | 3 | — |
| FLD-RISQUE_ACCEPTE | 3 | — |
| FLD-SALONS | 4 | — |
| FLD-SECURITE | 4 | — |
| FLD-SERVICES_INCLUS | 7 | — |
| FLD-SERVITUDES | 8 | — |
| FLD-SIGNATAIRES_NOMBRE | 8 | — |
| FLD-SOURCE_FINANCEMENT | 3 | — |
| FLD-SURFACE | 4 | — |
| FLD-SURFACE_TERRAIN | 4 | — |
| FLD-SURFACE_TERRAIN_M2 | 8 | — |
| FLD-TAUX_SOUHAITE | 3 | — |
| FLD-TELEPHONE | 5 | — |
| FLD-TERRAIN_CONSTRUCTIBLE | 8 | — |
| FLD-TERRAIN_LOTI | 8 | — |
| FLD-TITRE_REQUIS | 8 | — |
| FLD-TOPOGRAPHIE | 8 | — |
| FLD-TRANSACTION | 1 | — |
| FLD-TRANSACTION_TYPE | 1 | — |
| FLD-TYPE_CHAMBRE_UNIV | 7 | — |
| FLD-TYPE_TITRE | 8 | — |
| FLD-UNIVERSITE | 7 | — |
| FLD-URGENCE | 6 | — |
| FLD-USAGE | 1 | — |
| FLD-USAGE_PREVU | 8 | — |
| FLD-ZONE | 2 | — |
| FLD-ZONE_RECHERCHE_KM | 2 | — |

---

**End of COMMON_FIELD_DICTIONARY.md**
