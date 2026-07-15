# Residential Listing Qualification Matrices — LAWIM Heritage Gold

**Document ID:** LAWIM-GOLD-MATRICES-RESIDENTIAL-LISTING-V1
**Mission:** LAWIM Heritage Gold — Qualification des demandes de mise en location/vente résidentielle
**Date:** 2026-07-15
**Statut:** CANONICAL — Reference document for architecture H1
**Principe:** Matrices exhaustives et validées pour chaque type de listing résidentiel LAWIM

---

# Table of Contents

| # | Listing Type | Matrix ID | Transaction Types |
|---|-------------|-----------|-------------------|
| 1 | mise_en_location_studio | MATRIX-LIST-RES-001 | RENT |
| 2 | mise_en_location_appartement | MATRIX-LIST-RES-002 | RENT |
| 3 | mise_en_location_maison_villa | MATRIX-LIST-RES-003 | RENT |
| 4 | mise_en_vente_appartement | MATRIX-LIST-RES-004 | SELL |
| 5 | mise_en_vente_maison_villa | MATRIX-LIST-RES-005 | SELL |
| 6 | mise_en_vente_terrain | MATRIX-LIST-RES-006 | SELL |
| 7 | mise_en_location_commercial | MATRIX-LIST-RES-007 | RENT |
| 8 | mise_en_vente_commercial | MATRIX-LIST-RES-008 | SELL |
| 9 | mandat_vente | MATRIX-LIST-RES-009 | SELL |
| 10 | mandat_location | MATRIX-LIST-RES-010 | RENT |

---

# Common Rules for All Residential Listing Matrices

## Qualification Order

All listing matrices follow this qualification order:

| Order | Step | Field(s) |
|:-----:|------|----------|
| 1 | Identité déclarant | FLD-LIST-IDENTITE_DECLARANT |
| 2 | Relation au bien | FLD-LIST-RELATION_BIEN |
| 3 | Autorisation / Mandat | FLD-LIST-AUTORISATION_MANDAT |
| 4 | Transaction | FLD-LIST-TRANSACTION |
| 5 | Type exact de bien | FLD-LIST-TYPE_EXACT |
| 6 | Localisation | FLD-LIST-LOCALISATION_VILLE, FLD-LIST-LOCALISATION_QUARTIER, FLD-LIST-LOCALISATION_ADRESSE |
| 7 | Prix | FLD-LIST-PRIX_GLOBAL, FLD-LIST-PRIX_MENSUEL, FLD-LIST-PRIX_NEGOCIABLE |
| 8 | Disponibilité | FLD-LIST-DISPONIBILITE_DATE, FLD-LIST-DISPONIBILITE_DELAI |
| 9 | Caractéristiques essentielles | FLD-LIST-SURFACE, FLD-LIST-CHAMBRES, FLD-LIST-DOUCHES, FLD-LIST-SALONS, FLD-LIST-CUISINE |
| 10 | État du bien | FLD-LIST-ETAT |
| 11 | Photos et médias | FLD-LIST-PHOTOS, FLD-LIST-VIDEOS |
| 12 | Documents | FLD-LIST-DOCUMENTS |
| 13 | Conditions | FLD-LIST-CONDITIONS |
| 14 | Contact | FLD-LIST-CONTACT_NOM, FLD-LIST-CONTACT_TELEPHONE |
| 15 | Règles de visite | FLD-LIST-REGLES_VISITE |
| 16 | Consentement publication | FLD-LIST-CONSENTEMENT_PUBLICATION |
| 17 | Confirmation | Récapitulatif |
| 18 | Escalade | Décision: publication, visite, transfert humain |

## Channel Adaptation Rules

| Channel | Pace | Format | Reference |
|---------|------|--------|-----------|
| WhatsApp | 1 question per message | Minimal, mobile-first | CONVERSATION_MODEL.md §2 |
| Telegram | 2-3 fields per message | Structured with lists | CONVERSATION_MODEL.md §2 |
| Dashboard | Full form | Complete and actionable | QUALIFICATION_MODEL.md §7 |

## Universal Stop Criteria

Qualification stops early when:
- The declarant cannot prove ownership or mandate
- The property has legal disputes blocking transaction
- The city is not covered by LAWIM's active workflow
- User explicitly asks for a human agent
- Thread becomes repetitive (3 exchanges without progress)
- User withdraws the listing intent

## Propriétaire vs Non-Propriétaire Rules

For listings, the declarant may be:
1. **Propriétaire** — Owner of the property (full authorization)
2. **Mandataire** — Agent with mandate from the owner
3. **Copropriétaire** — Co-owner needing co-owners' consent
4. **Locataire** — Tenant (only for subletting with authorization)
5. **Héritier** — Heir with succession rights

When the declarant is NOT the sole owner, additional fields are required:
- FLD-LIST-NATURE_MANDAT — Type of mandate/authorization
- FLD-LIST-IDENTITE_TITULAIRE — Identity of the title holder
- FLD-LIST-PREUVE_MANDAT — Proof of mandate document
- FLD-LIST-DUREE_MANDAT — Duration of the mandate
- FLD-LIST-POUVOIRS_ACCORDS — Specific powers granted

## Matching Role Semantics

| Role | Description | Example |
|------|-------------|---------|
| hard_constraint | Must match exactly; otherwise excluded | transaction, ville, type_exact |
| soft_constraint | Strong preference but flexible | prix, surface, meuble |
| ranking_preference | Used to rank results only | etage, balcon |
| verification_only | For identity/authorization verification | identite_declarant, preuve_mandat |
| transaction_blocker | Must be resolved before transaction | etat, conditions, documents |
| informational_only | For display only, does not affect matching | nom, email, photos |
| consent_required | Requires explicit user consent | consentement_publication |

## Source Status Definitions

| Status | Meaning |
|--------|---------|
| HERITAGE_VALIDATED | Explicit rule from LAWIM heritage documents |
| HERITAGE_NORMALIZED | Normalized from multiple heritage sources |
| EXTERNAL_CONFIRMED | Confirmed by non-LAWIM sources (market research) |
| EXPERT_PROPOSAL | Proposed by domain expert (not from heritage) |
| HUMAN_VALIDATION_REQUIRED | Needs human review before production use |

## Common Forbidden Questions (All Listing Matrices)

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Avez-vous un autre bien à mettre en location ?" | Question vide, inefficace |
| 2 | "Quel est le prix idéal selon vous ?" | Suggestive, le prix est fixé par le propriétaire |
| 3 | "Pourquoi voulez-vous louer/vendre ?" | Hors scope de qualification |
| 4 | "Le bien est-il libre de tout occupant ?" | À déduire de la disponibilité |
| 5 | "Combien de pièces ?" | "Pièces" ambigu au Cameroun, utiliser "chambres" |
| 6 | "Quel est votre revenu ?" | Non pertinent pour une mise en location/vente |
| 7 | "Avez-vous un compromis de vente ?" | Prématuré, la mise en vente précède le compromis |
| 8 | "Quel est votre motif de vente ?" | Trop intrusif, non nécessaire |
| 9 | "Avez-vous déjà eu des locataires ?" | Non pertinent pour la qualification |
| 10 | "Le bien est-il à vendre à un prix inférieur au marché ?" | Suggestif, biaise l'offre |

## Register of Validated Field IDs (Master Catalog — Listing Domain)

| FIELD-ID | label | data_type | allowed_values | privacy | source | confidence |
|----------|-------|-----------|----------------|--------|--------|------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité du déclarant | enum | PROPRIETAIRE, MANDATAIRE, COPROPRIETAIRE, LOCATAIRE, HERITIER, AUTRE | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-RELATION_BIEN | Relation avec le bien | enum | PROPRIETAIRE_UNIQUE, COPROPRIETAIRE, USUFRUITIER, LOCATAIRE_PRINCIPAL, MANDATAIRE, HERITIER, AUTRE | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-AUTORISATION_MANDAT | Autorisation / Mandat | enum | PLEINE_PROPRIETE, MANDAT_SIMPLE, MANDAT_EXCLUSIF, AUTORISATION_ECRITE, AUTORISATION_ORALE, COPROPRIETE_ACCORD, SUCCESSION_EN_COURS | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-TRANSACTION | Transaction | enum | RENT, SELL | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-TYPE_EXACT | Type exact de bien | enum | studio, appartement, maison, villa, duplex, triplex, terrain, commercial, bureau, local_professionnel, immeuble | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-LOCALISATION_VILLE | Ville | string | LAWIM city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-LOCALISATION_QUARTIER | Quartier | string | Per-city neighborhood list | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-LOCALISATION_ADRESSE | Adresse complète | string | Free text | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-LOCALISATION_ZONE | Zone | string | Free text | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-LOCALISATION_REPERE | Point de repère | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-LIST-PRIX_GLOBAL | Prix global | integer | Positive integer | private | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-PRIX_MENSUEL | Loyer mensuel | integer | Positive integer | private | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-PRIX_M2 | Prix au m² | float | Positive float | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-PRIX_CHARGES | Charges mensuelles | integer | Positive integer | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-PRIX_CAUTION | Dépôt de garantie | integer | Positive integer | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-PRIX_NEGOCIABLE | Négociable | boolean | true, false | public | HERITAGE_NORMALIZED | HIGH |
| FLD-LIST-PRIX_DEVISE | Devise | enum | XAF, EUR, USD | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-DISPONIBILITE_DATE | Date de disponibilité | date | Valid date | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-DISPONIBILITE_DELAI | Délai de disponibilité | enum | IMMEDIATE, 1_SEMAINE, 2_SEMAINES, 1_MOIS, 3_MOIS, 6_MOIS, A_DEFINIR | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-DISPONIBILITE_OCCUPATION | Occupation actuelle | enum | LIBRE, OCCUPE, EN_TRAVAUX, A_VENIR | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-SURFACE | Surface habitable | integer | 10-10000 | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-SURFACE_TERRAIN | Surface du terrain | integer | 50-100000 | public | HERITAGE_NORMALIZED | HIGH |
| FLD-LIST-CHAMBRES | Nombre de chambres | integer | 0-20 | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-DOUCHES | Nombre de douches | integer | 1-10 | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-SALONS | Nombre de salons | integer | 0-10 | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-CUISINE | Type de cuisine | enum | INTERNE, EXTERNE, EQUIPEE, NON_EQUIPEE, AMERICAINE, INDIFFERENT | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-MEUBLE | Meublé | enum | MEUBLE, NON_MEUBLE, SEMI_MEUBLE | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-ETAGE | Étage | integer | 0-50 | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-NOMBRE_ETAGES | Nombre d'étages | integer | 1-50 | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-LIST-ASCENSEUR | Ascenseur | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-PARKING | Parking | enum | OUI, NON, GARAGE, NOMBRE_PLACES | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-COUR | Cour | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-CLOTURE | Clôture | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-DEPENDANCES | Dépendances | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-LIST-BALCON | Balcon | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-JARDIN | Jardin | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-PISCINE | Piscine | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-CLIMATISATION | Climatisation | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-FORAGE | Forage | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-INTERNET | Internet | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-SECURITE | Sécurité | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-GARDIENNAGE | Gardiennage | boolean | true, false | public | HERITAGE_NORMALIZED | LOW |
| FLD-LIST-EAU | Eau | enum | PERMANENTE, INTERMITTENTE, FORAGE, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-ELECTRICITE | Électricité | enum | PERMANENTE, INTERMITTENTE, GROUPE, SOLAIRE, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-ACCES_ROUTE | Accès route | enum | GOUDRONNEE, PISTE, ROUTE_NATIONALE, INDIFFERENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-ETAT | État du bien | enum | NEUF, TRES_BON, BON, MOYEN, A_RENOVER, A_RAFRACHIR, EN_CHANTIER | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-ETAT_DETAIL | Détail état | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-LIST-ANNEE_CONSTRUCTION | Année de construction | integer | 1900-2030 | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-LIST-PHOTOS | Photos | array | URLs or base64 images | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-VIDEOS | Vidéos | array | URLs | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-VIDEO_TOUR | Visite virtuelle | string | URL | public | EXPERT_PROPOSAL | LOW |
| FLD-LIST-PLAN_ETAGE | Plan d'étage | string | URL to floorplan | public | EXPERT_PROPOSAL | LOW |
| FLD-LIST-DOCUMENTS | Documents | array | Type de document | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Titre foncier | string | URL | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-DOCUMENT_ACTE_VENTE | Acte de vente | string | URL | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-DOCUMENT_CERTIFICAT_PROPRIETE | Certificat de propriété | string | URL | confidential | HERITAGE_NORMALIZED | HIGH |
| FLD-LIST-DOCUMENT_DIAGNOSTIC | Diagnostics techniques | array | URL | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-DOCUMENT_REGLEMENT_COPROPRIETE | Règlement de copropriété | string | URL | confidential | EXPERT_PROPOSAL | MEDIUM |
| FLD-LIST-CONDITIONS | Conditions particulières | string | Free text | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-CONDITION_CAUTION | Caution exigée | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-CONDITION_GARANTIE | Garantie exigée | enum | BANCAIRE, NOTARIEE, CAUTION_SOLIDAIRE, NONE | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-CONDITION_BAIL | Type de bail | enum | 1_AN, 2_ANS, 3_ANS, 5_ANS, 7_ANS, A_DEFINIR | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-CONDITION_PREAVIS | Préavis | enum | 1_MOIS, 3_MOIS, 6_MOIS, A_DEFINIR | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-LIST-CONDITION_HONORAIRES | Honoraires agence | enum | CHARGE_PROPRIETAIRE, CHARGE_LOCATAIRE, PARTAGE | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-LIST-CONDITION_VISITE | Modalités de visite | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-LIST-CONTACT_NOM | Nom du contact | string | Free text | private | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | string | Valid phone | private | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-CONTACT_EMAIL | Email | string | Valid email | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-CONTACT_CANAL | Canal préféré | enum | WHATSAPP, TELEGRAM, SMS, EMAIL, APPEL | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-CONTACT_DISPO | Disponibilité contact | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-LIST-REGLES_VISITE | Règles de visite | string | Free text | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires de visite | string | Free text | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis visite | enum | 1H, 2H, 4H, 24H, 48H, SUR_RENDEZ_VOUS | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-LIST-REGLES_VISITE_CONDTIONS | Conditions de visite | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement publication | boolean | true, false | public | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-CONSENTEMENT_PUBLICATION_CANAUX | Canaux de publication | enum[] | LAWIM_SITE, PARTENAIRES, RESEAUX_SOCIAUX, PETITES_ANNONCES, TOUS | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-CONSENTEMENT_PUBLICATION_DUREE | Durée de publication | enum | 1_SEMAINE, 2_SEMAINES, 1_MOIS, 2_MOIS, 3_MOIS, 6_MOIS, JUSQU_A_VENTE | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau de vérification | enum | COMPLET, STANDARD, MINIMAL, NON_VERIFIE | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-NIVEAU_VERIFICATION_DATE | Date de vérification | date | Valid date | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-NATURE_MANDAT | Nature du mandat | enum | MANDAT_SIMPLE, MANDAT_EXCLUSIF, MANDAT_COEXCLUSIF, MANDAT_ORAL, PROCURATION | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-IDENTITE_TITULAIRE | Identité du titulaire | string | Full name | private | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-IDENTITE_TITULAIRE_CONTACT | Contact du titulaire | string | Phone/email | private | HERITAGE_NORMALIZED | HIGH |
| FLD-LIST-PREUVE_MANDAT | Preuve du mandat | string | URL to document | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-PREUVE_MANDAT_TYPE | Type de preuve | enum | MANDAT_ECRIT, CONTRAT_AGENCE, PROCURATION, AUTORISATION_SIMPLE | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-DUREE_MANDAT | Durée du mandat | enum | 1_MOIS, 3_MOIS, 6_MOIS, 1_AN, 2_ANS, DUREE_DETERMINEE, INDETERMINEE | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-DUREE_MANDAT_DATE_FIN | Date de fin de mandat | date | Valid date | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LIST-POUVOIRS_ACCORDS | Pouvoirs accordés | enum[] | PUBLIER_ANNONCE, NEGOCIER_PRIX, SIGNER_BAIL, SIGNER_CONTRAT, ENCAISSER_FONDS, FAIRE_VISITES, TOUS_POUVOIRS | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LIST-POUVOIRS_LIMITES | Limitations des pouvoirs | string | Free text | confidential | EXPERT_PROPOSAL | LOW |

## Non-Propriétaire Field Requirements

| FIELD-ID | mandatory_when |
|----------|----------------|
| FLD-LIST-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE |
| FLD-LIST-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE |
| FLD-LIST-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE |
| FLD-LIST-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE |
| FLD-LIST-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE |

---

## MATRIX 1: mise_en_location_studio

### matrix_id
MATRIX-LIST-RES-001

### canonical_name
Mise en location studio

### request_family
RESIDENTIAL_LISTING

### transaction_type
RENT

### property_or_service_type
mise_en_location_studio

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing a studio apartment for rent. A studio is a self-contained unit combining bedroom, living area, and kitchenette in one open space with a separate bathroom. This matrix covers the complete listing process: from declarant identification through property characteristics to publication consent and verification.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité du déclarant | always | "Êtes-vous le propriétaire du bien ou un mandataire ?" | 10 |
| FLD-LIST-RELATION_BIEN | Relation au bien | always | "Quelle est votre relation avec ce bien ?" | 20 |
| FLD-LIST-TRANSACTION | Transaction | always | Il s'agit d'une mise en location (derived) | 30 |
| FLD-LIST-TYPE_EXACT | Type exact | always | "De quel type de bien s'agit-il ?" | 40 |
| FLD-LIST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le studio ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-LOCALISATION_QUARTIER | Quartier | always | "Dans quel quartier ?" | 60 |
| FLD-LIST-LOCALISATION_ADRESSE | Adresse | always | "Quelle est l'adresse complète ?" | 65 |
| FLD-LIST-PRIX_MENSUEL | Loyer mensuel | always | "Quel est le loyer mensuel demandé ?" | 70 |
| FLD-LIST-DISPONIBILITE_DATE | Date de disponibilité | always | "À partir de quand le studio est-il disponible ?" | 80 |
| FLD-LIST-DISPONIBILITE_OCCUPATION | Occupation actuelle | always | "Le studio est-il actuellement occupé ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-SURFACE | Surface | always | "Quelle est la surface du studio (m²) ?" | 90 |
| FLD-LIST-DOUCHES | Douches | always | "Combien de douches/salles de bain ?" | 100 |
| FLD-LIST-CUISINE | Cuisine | always | "Y a-t-il une cuisine ou kitchenette ?" | 110 |
| FLD-LIST-MEUBLE | Meublé | always | "Le studio est-il meublé, semi-meublé ou non meublé ?" | 120 |
| FLD-LIST-ETAT | État | always | "Quel est l'état général du studio ?" | 130 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONTACT_NOM | Nom du contact | always | "Quel est votre nom ?" | 140 |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | always | "Quel est votre numéro de téléphone ?" | 145 |
| FLD-LIST-CONTACT_EMAIL | Email | when dashboard | "Quelle est votre adresse email ?" | 150 |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement publication | always | "Acceptez-vous que nous publiions cette annonce sur nos plateformes ?" | 160 |
| FLD-LIST-CONSENTEMENT_PUBLICATION_CANAUX | Canaux de publication | when consent given | "Sur quels canaux souhaitez-vous publier ?" | 165 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-REGLES_VISITE | Règles de visite | always | "Quelles sont les modalités de visite ?" | 170 |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires visite | always | "Quels sont les horaires disponibles pour les visites ?" | 175 |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis visite | always | "Quel préavis est nécessaire pour organiser une visite ?" | 180 |
| FLD-LIST-CONTACT_CANAL | Canal préféré | always | "Par quel canal préférez-vous être contacté pour les visites ?" | 185 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-PRIX_CAUTION | Caution | always | "Quel est le montant du dépôt de garantie ?" | 190 |
| FLD-LIST-PRIX_CHARGES | Charges | always | "Les charges sont-elles incluses ? Quel montant ?" | 195 |
| FLD-LIST-CONDITION_BAIL | Type de bail | always | "Quel type de bail proposez-vous ?" | 200 |
| FLD-LIST-CONDITION_PREAVIS | Préavis | always | "Quel est le préavis pour le locataire ?" | 205 |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau vérification | always | "Quel niveau de vérification souhaitez-vous ?" | 210 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LIST-ETAGE | Étage | ranking_preference | 215 |
| FLD-LIST-ASCENSEUR | Ascenseur | ranking_preference | 220 |
| FLD-LIST-PARKING | Parking | soft_constraint | 225 |
| FLD-LIST-CLIMATISATION | Climatisation | soft_constraint | 230 |
| FLD-LIST-SECURITE | Sécurité | ranking_preference | 235 |
| FLD-LIST-INTERNET | Internet | ranking_preference | 240 |
| FLD-LIST-BALCON | Balcon | ranking_preference | 245 |
| FLD-LIST-PHOTOS | Photos | informational_only | 250 |
| FLD-LIST-LOCALISATION_ZONE | Zone | informational_only | 255 |
| FLD-LIST-PRIX_NEGOCIABLE | Négociable | informational_only | 260 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LIST-ETAT_DETAIL | Détail état | informational_only |
| FLD-LIST-VIDEOS | Vidéos | informational_only |
| FLD-LIST-ANNEE_CONSTRUCTION | Année construction | informational_only |
| FLD-LIST-ELECTRICITE | Électricité | informational_only |
| FLD-LIST-EAU | Eau | informational_only |
| FLD-LIST-DEPENDANCES | Dépendances | informational_only |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) |
| FLD-LIST-FORAGE | Forage | boost (+5) |
| FLD-LIST-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LIST-LOCALISATION_REPERE | Point de repère | informational_only |
| FLD-LIST-PLAN_ETAGE | Plan d'étage | informational_only |
| FLD-LIST-VIDEO_TOUR | Visite virtuelle | informational_only |
| FLD-LIST-CONDITIONS | Conditions particulières | informational_only |
| FLD-LIST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-LIST-CONDITION_HONORAIRES | Honoraires agence | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LIST-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-CLOTURE | if cour = true | informational_only |
| FLD-LIST-JARDIN | if property_type includes jardin | ranking_preference |
| FLD-LIST-GARDIENNAGE | if security = true | informational_only |
| FLD-LIST-ACCES_ROUTE | if not city center | ranking_preference |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | if niveau_verification = COMPLET | verification_only |
| FLD-LIST-CONDITION_GARANTIE | if caution > 0 | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LIST-CONTACT_TELEPHONE | Personal contact information |
| FLD-LIST-CONTACT_NOM | Personal identity |
| FLD-LIST-CONTACT_EMAIL | Personal contact |
| FLD-LIST-PRIX_MENSUEL | Financial information (owner's pricing) |
| FLD-LIST-PRIX_CAUTION | Financial guarantee details |
| FLD-LIST-LOCALISATION_ADRESSE | Exact address — shared only with verified tenants |
| FLD-LIST-DOCUMENTS | Legal property documents |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Sensitive legal document |
| FLD-LIST-PREUVE_MANDAT | Legal mandate document |
| FLD-LIST-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LIST-NATURE_MANDAT | Agency mandate terms |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LIST-DERIVED-PRIX_M2 | Prix au m² | prix_mensuel / surface |
| FLD-LIST-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local par type |
| FLD-LIST-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-LIST-DERIVED-COMPLETUDE_ANNONCE | Complétude annonce | weighted(photos, description, caractéristiques) |
| FLD-LIST-DERIVED-QUALITE_PUBLICATION | Qualité publication | completeness + photos + documents |
| FLD-LIST-DERIVED-URGENCE_LOCATION | Urgence location | disponibilité + contexte |
| FLD-LIST-DERIVED-PROFIL_PROPRIETAIRE | Profil propriétaire | type+historique |
| FLD-LIST-DERIVED-MANDAT_ACTIF | Mandat actif | duree_mandat + date_fin vs date_courante |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Studio = 0 chambre séparée par définition |
| 2 | "Combien de salons ?" | Non applicable, studio = espace unique |
| 3 | "Quel standing ?" | Déduire du prix/quartier |
| 4 | "Combien de pièces ?" | Terme non canonique au Cameroun |
| 5 | "Quel est votre motif de location ?" | Non pertinent |
| 6 | "Le locataire peut-il fumer ?" | Hors scope de qualification |
| 7 | "Acceptez-vous les animaux ?" | Hors scope de qualification initiale |
| 8 | "Quel est votre salaire ?" | Non pertinent, c'est une mise en location |
| 9 | "Avez-vous déjà eu des problèmes avec des locataires ?" | Non pertinent |
| 10 | "Pour combien de temps souhaitez-vous louer ?" | Déjà couvert par le type de bail |

---

## MATRIX 2: mise_en_location_appartement

### matrix_id
MATRIX-LIST-RES-002

### canonical_name
Mise en location appartement

### request_family
RESIDENTIAL_LISTING

### transaction_type
RENT

### property_or_service_type
mise_en_location_appartement

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing an apartment for rent. Covers all apartment types (non-meublé, meublé, duplex, triplex) with full characterization: rooms, surfaces, amenities, condition, pricing, availability, visit rules, and legal documentation. Includes non-owner paths for mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité du déclarant | always | "Êtes-vous le propriétaire ou un mandataire ?" | 10 |
| FLD-LIST-RELATION_BIEN | Relation au bien | always | "Quelle est votre relation avec cet appartement ?" | 20 |
| FLD-LIST-TRANSACTION | Transaction | always | Derived (RENT) | 30 |
| FLD-LIST-TYPE_EXACT | Type exact | always | "S'agit-il d'un appartement standard, duplex ou triplex ?" | 40 |
| FLD-LIST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve l'appartement ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-LOCALISATION_QUARTIER | Quartier | always | "Dans quel quartier/zone ?" | 60 |
| FLD-LIST-LOCALISATION_ADRESSE | Adresse | always | "Quelle est l'adresse complète ?" | 65 |
| FLD-LIST-PRIX_MENSUEL | Loyer mensuel | always | "Quel est le loyer mensuel ?" | 70 |
| FLD-LIST-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand est-il disponible ?" | 80 |
| FLD-LIST-DISPONIBILITE_OCCUPATION | Occupation | always | "Est-il actuellement occupé par un locataire ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-SURFACE | Surface | always | "Quelle est la surface habitable ?" | 90 |
| FLD-LIST-CHAMBRES | Chambres | always | "Combien de chambres à coucher ?" | 100 |
| FLD-LIST-DOUCHES | Douches | always | "Combien de douches/salles de bain ?" | 105 |
| FLD-LIST-SALONS | Salons | always | "Combien de salons/séjours ?" | 110 |
| FLD-LIST-CUISINE | Cuisine | always | "Type de cuisine ?" | 115 |
| FLD-LIST-MEUBLE | Meublé | always | "Appartement meublé ou non ?" | 120 |
| FLD-LIST-ETAT | État | always | "Quel est l'état général ?" | 130 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 140 |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 145 |
| FLD-LIST-CONTACT_EMAIL | Email | optional | "Votre email ?" | 150 |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication sur nos plateformes ?" | 160 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-REGLES_VISITE | Règles de visite | always | "Modalités de visite ?" | 170 |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 175 |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 180 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-PRIX_CAUTION | Caution | always | "Montant du dépôt de garantie ?" | 190 |
| FLD-LIST-PRIX_CHARGES | Charges | always | "Charges mensuelles ? Incluses ou non ?" | 195 |
| FLD-LIST-CONDITION_BAIL | Type de bail | always | "Type de bail proposé ?" | 200 |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 210 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LIST-ETAGE | Étage | ranking_preference | 215 |
| FLD-LIST-ASCENSEUR | Ascenseur | ranking_preference | 220 |
| FLD-LIST-PARKING | Parking | soft_constraint | 225 |
| FLD-LIST-CLIMATISATION | Climatisation | soft_constraint | 230 |
| FLD-LIST-SECURITE | Sécurité | ranking_preference | 235 |
| FLD-LIST-INTERNET | Internet | ranking_preference | 240 |
| FLD-LIST-BALCON | Balcon | ranking_preference | 245 |
| FLD-LIST-JARDIN | Jardin | ranking_preference | 250 |
| FLD-LIST-COUR | Cour | ranking_preference | 255 |
| FLD-LIST-PHOTOS | Photos | informational_only | 260 |
| FLD-LIST-PRIX_NEGOCIABLE | Négociable | informational_only | 265 |
| FLD-LIST-PRIX_DEVISE | Devise | informational_only | 270 |
| FLD-LIST-CONDITION_PREAVIS | Préavis | informational_only | 275 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LIST-ETAT_DETAIL | Détail état | informational_only |
| FLD-LIST-VIDEOS | Vidéos | informational_only |
| FLD-LIST-LOCALISATION_ZONE | Zone | informational_only |
| FLD-LIST-ANNEE_CONSTRUCTION | Année construction | informational_only |
| FLD-LIST-ELECTRICITE | Électricité | informational_only |
| FLD-LIST-EAU | Eau | informational_only |
| FLD-LIST-CLOTURE | Clôture | informational_only |
| FLD-LIST-DEPENDANCES | Dépendances | informational_only |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) |
| FLD-LIST-FORAGE | Forage | boost (+5) |
| FLD-LIST-PISCINE | Piscine | boost (+15) |
| FLD-LIST-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LIST-LOCALISATION_REPERE | Point de repère | informational_only |
| FLD-LIST-PLAN_ETAGE | Plan d'étage | informational_only |
| FLD-LIST-VIDEO_TOUR | Visite virtuelle | informational_only |
| FLD-LIST-CONDITIONS | Conditions particulières | informational_only |
| FLD-LIST-CONTACT_CANAL | Canal contact | informational_only |
| FLD-LIST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-LIST-CONDITION_HONORAIRES | Honoraires agence | informational_only |
| FLD-LIST-CONDITION_GARANTIE | Garantie exigée | informational_only |
| FLD-LIST-GARDIENNAGE | Gardiennage | informational_only |
| FLD-LIST-ACCES_ROUTE | Accès route | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LIST-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-NOMBRE_ETAGES | if immeuble collectif | informational_only |
| FLD-LIST-SURFACE_TERRAIN | if terrain included | informational_only |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | niveau_verification = COMPLET | verification_only |
| FLD-LIST-DOCUMENT_REGLEMENT_COPROPRIETE | if copropriété | verification_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_DUREE | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LIST-CONTACT_TELEPHONE | Personal contact |
| FLD-LIST-CONTACT_NOM | Personal identity |
| FLD-LIST-CONTACT_EMAIL | Personal contact |
| FLD-LIST-PRIX_MENSUEL | Financial - owner pricing |
| FLD-LIST-PRIX_CAUTION | Financial guarantee |
| FLD-LIST-LOCALISATION_ADRESSE | Exact address, shared only with qualified tenants |
| FLD-LIST-DOCUMENTS | Legal property documents |
| FLD-LIST-PREUVE_MANDAT | Legal mandate document |
| FLD-LIST-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LIST-NATURE_MANDAT | Agency mandate terms |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LIST-DERIVED-PRIX_M2 | Prix au m² | prix_mensuel / surface |
| FLD-LIST-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LIST-DERIVED-COMPLETUDE_ANNONCE | Complétude annonce | champs remplis |
| FLD-LIST-DERIVED-QUALITE | Qualité annonce | complétude + photos |
| FLD-LIST-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-LIST-DERIVED-MANDAT_ACTIF | Mandat actif | duree_mandat + date_fin |
| FLD-LIST-DERIVED-URGENCE | Urgence location | disponibilité |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Quel standing ?" | Déduire du prix/quartier |
| 2 | "Combien de pièces ?" | Terme non canonique, utiliser chambres |
| 3 | "Pourquoi quittez-vous ?" | Hors scope |
| 4 | "Le locataire peut-il avoir des animaux ?" | Hors scope initial |
| 5 | "Acceptez-vous les enfants ?" | Discriminatoire, illégal |
| 6 | "Quel est votre revenu ?" | Non pertinent |
| 7 | "Combien de locataires maximum ?" | À spécifier dans conditions |
| 8 | "Avez-vous déjà eu des impayés ?" | Hors scope |

---

## MATRIX 3: mise_en_location_maison_villa

### matrix_id
MATRIX-LIST-RES-003

### canonical_name
Mise en location maison / villa

### request_family
RESIDENTIAL_LISTING

### transaction_type
RENT

### property_or_service_type
mise_en_location_maison_villa

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing a house or villa for rent. Includes detailed property characteristics specific to standalone homes: land surface, courtyard, fence, garden, pool, parking, accessibility, utilities, and outbuildings. Covers villa basse, villa étage, maison individuelle, maison de ville.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LIST-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec cette maison ?" | 20 |
| FLD-LIST-TRANSACTION | Transaction | always | Derived (RENT) | 30 |
| FLD-LIST-TYPE_EXACT | Type exact | always | "S'agit-il d'une villa basse, villa étage, maison individuelle ou maison de ville ?" | 40 |
| FLD-LIST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ?" | 60 |
| FLD-LIST-LOCALISATION_ADRESSE | Adresse | always | "Adresse complète ?" | 65 |
| FLD-LIST-PRIX_MENSUEL | Loyer mensuel | always | "Loyer mensuel demandé ?" | 70 |
| FLD-LIST-DISPONIBILITE_DATE | Date disponibilité | always | "Disponible à partir de quand ?" | 80 |
| FLD-LIST-DISPONIBILITE_OCCUPATION | Occupation | always | "Actuellement occupé ou libre ?" | 85 |
| FLD-LIST-SURFACE | Surface habitable | always | "Surface habitable en m² ?" | 90 |
| FLD-LIST-SURFACE_TERRAIN | Surface terrain | always | "Surface du terrain ?" | 95 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CHAMBRES | Chambres | always | "Nombre de chambres ?" | 100 |
| FLD-LIST-DOUCHES | Douches | always | "Nombre de douches ?" | 105 |
| FLD-LIST-SALONS | Salons | always | "Nombre de salons ?" | 110 |
| FLD-LIST-CUISINE | Cuisine | always | "Type de cuisine ?" | 115 |
| FLD-LIST-MEUBLE | Meublé | always | "Meublé ou non ?" | 120 |
| FLD-LIST-ETAT | État | always | "État général ?" | 130 |
| FLD-LIST-PARKING | Parking | always | "Y a-t-il un parking/garage ?" | 135 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONTACT_NOM | Nom | always | "Votre nom ?" | 140 |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 145 |
| FLD-LIST-CONTACT_EMAIL | Email | optional | "Votre email ?" | 150 |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication ?" | 160 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-REGLES_VISITE | Règles visite | always | "Modalités de visite ?" | 170 |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 175 |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 180 |
| FLD-LIST-CONTACT_CANAL | Canal | always | "Canal préféré ?" | 185 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-PRIX_CAUTION | Caution | always | "Montant dépôt de garantie ?" | 190 |
| FLD-LIST-PRIX_CHARGES | Charges | always | "Charges mensuelles ?" | 195 |
| FLD-LIST-CONDITION_BAIL | Type de bail | always | "Type de bail proposé ?" | 200 |
| FLD-LIST-CONDITION_PREAVIS | Préavis | always | "Préavis ?" | 205 |
| FLD-LIST-CONDITION_HONORAIRES | Honoraires | always | "Honoraires agence ?" | 207 |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 210 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LIST-COUR | Cour | soft_constraint | 215 |
| FLD-LIST-CLOTURE | Clôture | soft_constraint | 220 |
| FLD-LIST-JARDIN | Jardin | soft_constraint | 225 |
| FLD-LIST-CLIMATISATION | Climatisation | soft_constraint | 230 |
| FLD-LIST-SECURITE | Sécurité | soft_constraint | 235 |
| FLD-LIST-GARDIENNAGE | Gardiennage | ranking_preference | 240 |
| FLD-LIST-INTERNET | Internet | ranking_preference | 245 |
| FLD-LIST-ACCES_ROUTE | Accès route | soft_constraint | 250 |
| FLD-LIST-PISCINE | Piscine | boost (+20) | 255 |
| FLD-LIST-DEPENDANCES | Dépendances | informational_only | 260 |
| FLD-LIST-PHOTOS | Photos | informational_only | 265 |
| FLD-LIST-VIDEOS | Vidéos | informational_only | 270 |
| FLD-LIST-ETAGE | Étage (si villa étage) | ranking_preference | 275 |
| FLD-LIST-PRIX_NEGOCIABLE | Négociable | informational_only | 280 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LIST-ANNEE_CONSTRUCTION | Année construction | informational_only |
| FLD-LIST-ELECTRICITE | Électricité | informational_only |
| FLD-LIST-EAU | Eau | informational_only |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) |
| FLD-LIST-FORAGE | Forage | boost (+10) |
| FLD-LIST-BALCON | Balcon | ranking_preference |
| FLD-LIST-ASCENSEUR | Ascenseur | ranking_preference |
| FLD-LIST-LOCALISATION_ZONE | Zone | informational_only |
| FLD-LIST-LOCALISATION_REPERE | Point de repère | informational_only |
| FLD-LIST-ETAT_DETAIL | Détail état | informational_only |
| FLD-LIST-DISPONIBILITE_DELAI | Délai | informational_only |
| FLD-LIST-PLAN_ETAGE | Plan d'étage | informational_only |
| FLD-LIST-VIDEO_TOUR | Visite virtuelle | informational_only |
| FLD-LIST-CONDITIONS | Conditions | informational_only |
| FLD-LIST-CONDITION_GARANTIE | Garantie | informational_only |
| FLD-LIST-CONTACT_DISPO | Disponibilité contact | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LIST-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-NOMBRE_ETAGES | type = villa_etage | informational_only |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | niveau_verification = COMPLET | verification_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_DUREE | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LIST-CONTACT_TELEPHONE | Personal contact |
| FLD-LIST-CONTACT_NOM | Personal identity |
| FLD-LIST-CONTACT_EMAIL | Personal contact |
| FLD-LIST-PRIX_MENSUEL | Financial - owner pricing |
| FLD-LIST-PRIX_CAUTION | Financial guarantee |
| FLD-LIST-LOCALISATION_ADRESSE | Exact address |
| FLD-LIST-DOCUMENTS | Legal documents |
| FLD-LIST-PREUVE_MANDAT | Legal mandate document |
| FLD-LIST-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Property title |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LIST-DERIVED-PRIX_M2 | Prix au m² | prix_mensuel / surface |
| FLD-LIST-DERIVED-PRIX_M2_TERRAIN | Prix terrain m² | prix / surface_terrain |
| FLD-LIST-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |
| FLD-LIST-DERIVED-QUALITE | Qualité publication | complétude + médias |
| FLD-LIST-DERIVED-PROFIL | Profil propriétaire | historique + type |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Quel standing ?" | Déduire du prix/quartier |
| 2 | "Combien de pièces ?" | Terme non canonique |
| 3 | "Le locataire a-t-il une famille ?" | Discriminatoire |
| 4 | "Avez-vous des voisins ?" | Non pertinent |
| 5 | "Pourquoi louez-vous ?" | Hors scope |
| 6 | "Quel est votre emploi ?" | Non pertinent |

---

## MATRIX 4: mise_en_vente_appartement

### matrix_id
MATRIX-LIST-RES-004

### canonical_name
Mise en vente appartement

### request_family
RESIDENTIAL_LISTING

### transaction_type
SELL

### property_or_service_type
mise_en_vente_appartement

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing an apartment for sale. Includes purchase-specific fields: price global, condominium regulations, property title, diagnostics, co-ownership status, and transaction conditions. Full non-owner mandate path included.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous le propriétaire ou un mandataire ?" | 10 |
| FLD-LIST-RELATION_BIEN | Relation bien | always | "Quelle est votre relation ?" | 20 |
| FLD-LIST-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LIST-TYPE_EXACT | Type exact | always | "Type d'appartement ? (standard, duplex, triplex)" | 40 |
| FLD-LIST-LOCALISATION_VILLE | Ville | always | "Ville ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-LOCALISATION_QUARTIER | Quartier | always | "Quartier ?" | 60 |
| FLD-LIST-LOCALISATION_ADRESSE | Adresse | always | "Adresse ?" | 65 |
| FLD-LIST-PRIX_GLOBAL | Prix de vente | always | "Prix de vente total ?" | 70 |
| FLD-LIST-PRIX_DEVISE | Devise | always | "Devise ?" | 72 |
| FLD-LIST-DISPONIBILITE_DATE | Date disponibilité | always | "Disponible à partir de quand ?" | 80 |
| FLD-LIST-DISPONIBILITE_OCCUPATION | Occupation | always | "Actuellement occupé ?" | 85 |
| FLD-LIST-SURFACE | Surface | always | "Surface habitable ?" | 90 |
| FLD-LIST-CHAMBRES | Chambres | always | "Nombre de chambres ?" | 100 |
| FLD-LIST-DOUCHES | Douches | always | "Nombre de douches ?" | 105 |
| FLD-LIST-SALONS | Salons | always | "Nombre de salons ?" | 110 |
| FLD-LIST-CUISINE | Cuisine | always | "Type de cuisine ?" | 115 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-ETAT | État | always | "État général ?" | 130 |
| FLD-LIST-ETAGE | Étage | always | "À quel étage ?" | 132 |
| FLD-LIST-ASCENSEUR | Ascenseur | always | "Y a-t-il un ascenseur ?" | 134 |
| FLD-LIST-PARKING | Parking | always | "Parking inclu ?" | 136 |
| FLD-LIST-CLIMATISATION | Climatisation | always | "Climatisation ?" | 138 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONTACT_NOM | Nom | always | "Votre nom ?" | 140 |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 145 |
| FLD-LIST-CONTACT_EMAIL | Email | always | "Votre email ?" | 150 |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication ?" | 160 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-REGLES_VISITE | Règles visite | always | "Modalités de visite ?" | 170 |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires ?" | 175 |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 180 |
| FLD-LIST-CONTACT_CANAL | Canal | always | "Canal préféré ?" | 185 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 190 |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Titre foncier | always | "Le titre foncier est-il disponible ?" | 200 |
| FLD-LIST-DOCUMENT_ACTE_VENTE | Acte de vente | always | "L'acte de vente original est-il disponible ?" | 205 |
| FLD-LIST-CONDITIONS | Conditions particulières | always | "Y a-t-il des conditions particulières de vente ?" | 210 |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 220 |
| FLD-LIST-PRIX_DEVISE | Devise | always | "Devise ?" | 225 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LIST-BALCON | Balcon | ranking_preference | 230 |
| FLD-LIST-JARDIN | Jardin | ranking_preference | 235 |
| FLD-LIST-COUR | Cour | ranking_preference | 240 |
| FLD-LIST-SECURITE | Sécurité | ranking_preference | 245 |
| FLD-LIST-GARDIENNAGE | Gardiennage | ranking_preference | 250 |
| FLD-LIST-INTERNET | Internet | ranking_preference | 255 |
| FLD-LIST-ELECTRICITE | Électricité | informational_only | 260 |
| FLD-LIST-EAU | Eau | informational_only | 265 |
| FLD-LIST-DOCUMENT_DIAGNOSTIC | Diagnostics | verification_only | 270 |
| FLD-LIST-PHOTOS | Photos | informational_only | 275 |
| FLD-LIST-VIDEOS | Vidéos | informational_only | 280 |
| FLD-LIST-ANNEE_CONSTRUCTION | Année construction | informational_only | 285 |
| FLD-LIST-PRIX_M2 | Prix au m² | informational_only | 290 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LIST-LOCALISATION_ZONE | Zone | informational_only |
| FLD-LIST-LOCALISATION_REPERE | Point de repère | informational_only |
| FLD-LIST-ETAT_DETAIL | Détail état | informational_only |
| FLD-LIST-NOMBRE_ETAGES | Nombre d'étages immeuble | informational_only |
| FLD-LIST-DEPENDANCES | Dépendances | informational_only |
| FLD-LIST-PISCINE | Piscine | boost (+15) |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) |
| FLD-LIST-FORAGE | Forage | boost (+10) |
| FLD-LIST-DISPONIBILITE_DELAI | Délai | informational_only |
| FLD-LIST-PLAN_ETAGE | Plan d'étage | informational_only |
| FLD-LIST-VIDEO_TOUR | Visite virtuelle | informational_only |
| FLD-LIST-CONDITION_GARANTIE | Garantie | informational_only |
| FLD-LIST-CONDITION_PREAVIS | Préavis | informational_only |
| FLD-LIST-CONDITION_HONORAIRES | Honoraires agence | informational_only |
| FLD-LIST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-LIST-MEUBLE | Meublé (si vendu meublé) | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LIST-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DOCUMENT_CERTIFICAT_PROPRIETE | if titre_foncier not available | verification_only |
| FLD-LIST-DOCUMENT_REGLEMENT_COPROPRIETE | if copropriété | verification_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_DUREE | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LIST-CONTACT_TELEPHONE | Personal contact |
| FLD-LIST-CONTACT_NOM | Personal identity |
| FLD-LIST-CONTACT_EMAIL | Personal contact |
| FLD-LIST-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LIST-PRIX_NEGOCIABLE | Negotiation margin |
| FLD-LIST-LOCALISATION_ADRESSE | Exact address |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Legal property document |
| FLD-LIST-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LIST-DOCUMENT_DIAGNOSTIC | Technical diagnostics |
| FLD-LIST-PREUVE_MANDAT | Legal mandate |
| FLD-LIST-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LIST-DOCUMENTS | All legal documents |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LIST-DERIVED-PRIX_M2 | Prix au m² | prix_global / surface |
| FLD-LIST-DERIVED-PRIX_COHERENCE | Cohérence prix | vs marché local |
| FLD-LIST-DERIVED-COMPLETUDE | Complétude | weighted fields |
| FLD-LIST-DERIVED-TITRE_VALIDE | Titre valide | titre_foncier + vérification |
| FLD-LIST-DERIVED-COPRIETE | En copropriété | type + documents |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Quel standing ?" | Déduire |
| 2 | "Pourquoi vendez-vous ?" | Hors scope |
| 3 | "Combien de pièces ?" | Non canonique |
| 4 | "Avez-vous besoin de vendre rapidement ?" | Suggestif |
| 5 | "Le bien est-il hypothéqué ?" | À vérifier via documents |
| 6 | "Quel est votre prix idéal ?" | Déjà le prix global |

---

## MATRIX 5: mise_en_vente_maison_villa

### matrix_id
MATRIX-LIST-RES-005

### canonical_name
Mise en vente maison / villa

### request_family
RESIDENTIAL_LISTING

### transaction_type
SELL

### property_or_service_type
mise_en_vente_maison_villa

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing a house or villa for sale. Extensive characterization for standalone homes including land, construction details, utilities, outbuildings, and legal status. Comprehensive non-owner mandate handling with document verification requirements.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LIST-RELATION_BIEN | Relation bien | always | "Quelle est votre relation ?" | 20 |
| FLD-LIST-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LIST-TYPE_EXACT | Type exact | always | "Type de maison/villa ?" | 40 |
| FLD-LIST-LOCALISATION_VILLE | Ville | always | "Ville ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-LOCALISATION_QUARTIER | Quartier | always | "Quartier ?" | 60 |
| FLD-LIST-LOCALISATION_ADRESSE | Adresse | always | "Adresse ?" | 65 |
| FLD-LIST-PRIX_GLOBAL | Prix de vente | always | "Prix de vente ?" | 70 |
| FLD-LIST-DISPONIBILITE_DATE | Date disponibilité | always | "Disponible quand ?" | 80 |
| FLD-LIST-SURFACE | Surface habitable | always | "Surface habitable ?" | 90 |
| FLD-LIST-SURFACE_TERRAIN | Surface terrain | always | "Surface terrain ?" | 95 |
| FLD-LIST-CHAMBRES | Chambres | always | "Nombre de chambres ?" | 100 |
| FLD-LIST-DOUCHES | Douches | always | "Nombre de douches ?" | 105 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-SALONS | Salons | always | "Nombre de salons ?" | 110 |
| FLD-LIST-CUISINE | Cuisine | always | "Type de cuisine ?" | 115 |
| FLD-LIST-MEUBLE | Meublé | always | "Vendu meublé ?" | 120 |
| FLD-LIST-ETAT | État | always | "État général ?" | 130 |
| FLD-LIST-PARKING | Parking | always | "Parking/garage ?" | 135 |
| FLD-LIST-COUR | Cour | always | "Y a-t-il une cour ?" | 137 |
| FLD-LIST-CLOTURE | Clôture | always | "Y a-t-il une clôture ?" | 139 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONTACT_NOM | Nom | always | "Votre nom ?" | 140 |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | always | "Téléphone ?" | 145 |
| FLD-LIST-CONTACT_EMAIL | Email | always | "Email ?" | 150 |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement | always | "Publication acceptée ?" | 160 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-REGLES_VISITE | Règles visite | always | "Modalités visite ?" | 170 |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires ?" | 175 |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis ?" | 180 |
| FLD-LIST-CONTACT_CANAL | Canal | always | "Canal préféré ?" | 185 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-PRIX_NEGOCIABLE | Négociable | always | "Prix négociable ?" | 190 |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Titre foncier | always | "Titre foncier disponible ?" | 200 |
| FLD-LIST-DOCUMENT_ACTE_VENTE | Acte de vente | always | "Acte de vente original ?" | 205 |
| FLD-LIST-CONDITIONS | Conditions | always | "Conditions de vente ?" | 210 |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau vérification ?" | 220 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LIST-JARDIN | Jardin | soft_constraint | 225 |
| FLD-LIST-PISCINE | Piscine | boost (+20) | 230 |
| FLD-LIST-CLIMATISATION | Climatisation | soft_constraint | 235 |
| FLD-LIST-SECURITE | Sécurité | ranking_preference | 240 |
| FLD-LIST-GARDIENNAGE | Gardiennage | ranking_preference | 245 |
| FLD-LIST-ACCES_ROUTE | Accès route | soft_constraint | 250 |
| FLD-LIST-ANNEE_CONSTRUCTION | Année construction | informational_only | 255 |
| FLD-LIST-DEPENDANCES | Dépendances | informational_only | 260 |
| FLD-LIST-ETAGE | Étages | informational_only | 265 |
| FLD-LIST-NOMBRE_ETAGES | Nombre d'étages | informational_only | 270 |
| FLD-LIST-PHOTOS | Photos | informational_only | 275 |
| FLD-LIST-VIDEOS | Vidéos | informational_only | 280 |
| FLD-LIST-PRIX_DEVISE | Devise | informational_only | 285 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LIST-ELECTRICITE | Électricité | informational_only |
| FLD-LIST-EAU | Eau | informational_only |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) |
| FLD-LIST-FORAGE | Forage | boost (+10) |
| FLD-LIST-BALCON | Balcon | ranking_preference |
| FLD-LIST-INTERNET | Internet | ranking_preference |
| FLD-LIST-LOCALISATION_ZONE | Zone | informational_only |
| FLD-LIST-LOCALISATION_REPERE | Point de repère | informational_only |
| FLD-LIST-ETAT_DETAIL | Détail état | informational_only |
| FLD-LIST-DISPONIBILITE_DELAI | Délai | informational_only |
| FLD-LIST-OCCUPATION | Occupation actuelle | informational_only |
| FLD-LIST-PLAN_ETAGE | Plan d'étage | informational_only |
| FLD-LIST-VIDEO_TOUR | Visite virtuelle | informational_only |
| FLD-LIST-CONDITION_GARANTIE | Garantie | informational_only |
| FLD-LIST-CONDITION_PREAVIS | Préavis | informational_only |
| FLD-LIST-CONDITION_HONORAIRES | Honoraires | informational_only |
| FLD-LIST-DOCUMENT_DIAGNOSTIC | Diagnostics | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LIST-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DOCUMENT_CERTIFICAT_PROPRIETE | titre_foncier absent | verification_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_DUREE | consent = true | informational_only |
| FLD-LIST-PISCINE | if jardin = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LIST-CONTACT_TELEPHONE | Personal contact |
| FLD-LIST-CONTACT_NOM | Personal identity |
| FLD-LIST-CONTACT_EMAIL | Personal contact |
| FLD-LIST-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LIST-LOCALISATION_ADRESSE | Exact address |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Legal property document |
| FLD-LIST-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LIST-PREUVE_MANDAT | Legal mandate |
| FLD-LIST-IDENTITE_TITULAIRE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LIST-DERIVED-PRIX_M2 | Prix au m² | prix_global / surface |
| FLD-LIST-DERIVED-PRIX_M2_TERRAIN | Prix terrain m² | prix_global / surface_terrain |
| FLD-LIST-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |
| FLD-LIST-DERIVED-QUALITE | Qualité publication | weighted(photos, completeness) |
| FLD-LIST-DERIVED-TITRE_VALIDE | Titre valide | titre_foncier + verification |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Quel standing ?" | Déduire |
| 2 | "Pourquoi vendez-vous ?" | Hors scope |
| 3 | "Combien de pièces ?" | Non canonique |
| 4 | "Avez-vous un autre bien à vendre ?" | Hors scope |
| 5 | "Le bien a-t-il des vices cachés ?" | À traiter via diagnostics |

---

## MATRIX 6: mise_en_vente_terrain

### matrix_id
MATRIX-LIST-RES-006

### canonical_name
Mise en vente terrain

### request_family
RESIDENTIAL_LISTING

### transaction_type
SELL

### property_or_service_type
mise_en_vente_terrain

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing land for sale. Covers legal status (titré/non titré), surface, accessibility, utilities, topography, land use classification, construction viability, and legal documentation. Critical legal verification path for non-owner declarants.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LIST-RELATION_BIEN | Relation bien | always | "Quelle est votre relation ?" | 20 |
| FLD-LIST-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LIST-TYPE_EXACT | Type exact | always | Derived (TERRAIN) | 40 |
| FLD-LIST-LOCALISATION_VILLE | Ville | always | "Ville où se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-LOCALISATION_QUARTIER | Quartier/Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LIST-LOCALISATION_ADRESSE | Adresse/Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LIST-SURFACE_TERRAIN | Surface terrain | always | "Surface du terrain en m² ?" | 70 |
| FLD-LIST-PRIX_GLOBAL | Prix de vente | always | "Prix de vente ?" | 75 |
| FLD-LIST-PRIX_M2 | Prix au m² | always | "Prix au m² ?" | 77 |
| FLD-LIST-DISPONIBILITE_DATE | Date disponibilité | always | "Disponible quand ?" | 80 |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Titre foncier | always | "Le terrain a-t-il un titre foncier ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-PRIX_NEGOCIABLE | Négociable | always | "Prix négociable ?" | 90 |
| FLD-LIST-ETAT | État terrain | always | "Quel est l'état du terrain ?" | 100 |
| FLD-LIST-DISPONIBILITE_OCCUPATION | Occupation | always | "Le terrain est-il actuellement occupé ou cultivé ?" | 105 |
| FLD-LIST-ACCES_ROUTE | Accès route | always | "Type d'accès routier ?" | 110 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONTACT_NOM | Nom | always | "Votre nom ?" | 140 |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | always | "Téléphone ?" | 145 |
| FLD-LIST-CONTACT_EMAIL | Email | always | "Email ?" | 150 |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement | always | "Publication acceptée ?" | 160 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-REGLES_VISITE | Règles visite | always | "Modalités visite terrain ?" | 170 |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires visite ?" | 175 |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 180 |
| FLD-LIST-LOCALISATION_REPERE | Point repère | always | "Point de repère pour trouver le terrain ?" | 185 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Titre foncier | always | "Numéro du titre foncier ?" | 200 |
| FLD-LIST-DOCUMENT_ACTE_VENTE | Acte de vente | always | "Acte de vente original disponible ?" | 205 |
| FLD-LIST-CONDITIONS | Conditions | always | "Conditions particulières ?" | 210 |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau vérification ?" | 220 |
| FLD-LIST-PRIX_DEVISE | Devise | always | "Devise ?" | 225 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LIST-LOCALISATION_ZONE | Zone | informational_only | 230 |
| FLD-LIST-ELECTRICITE | Électricité disponible | soft_constraint | 235 |
| FLD-LIST-EAU | Eau disponible | soft_constraint | 240 |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | ranking_preference | 245 |
| FLD-LIST-FORAGE | Forage | boost (+15) | 250 |
| FLD-LIST-CLOTURE | Clôture | ranking_preference | 255 |
| FLD-LIST-PHOTOS | Photos terrain | informational_only | 260 |
| FLD-LIST-VIDEOS | Vidéos terrain | informational_only | 265 |
| FLD-LIST-PLAN_ETAGE | Plan de bornage | verification_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LIST-ETAT_DETAIL | Détail état terrain | informational_only |
| FLD-LIST-DISPONIBILITE_DELAI | Délai | informational_only |
| FLD-LIST-DOCUMENT_CERTIFICAT_PROPRIETE | Certificat propriété | verification_only |
| FLD-LIST-DOCUMENT_DIAGNOSTIC | Étude sol | verification_only |
| FLD-LIST-CONDITION_GARANTIE | Garantie | informational_only |
| FLD-LIST-CONDITION_HONORAIRES | Honoraires | informational_only |
| FLD-LIST-CONTACT_CANAL | Canal | informational_only |
| FLD-LIST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-LIST-SECURITE | Sécurité zone | informational_only |
| FLD-LIST-GARDIENNAGE | Gardiennage terrain | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LIST-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DOCUMENT_CERTIFICAT_PROPRIETE | titre_foncier absent | verification_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_DUREE | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LIST-CONTACT_TELEPHONE | Personal contact |
| FLD-LIST-CONTACT_NOM | Personal identity |
| FLD-LIST-CONTACT_EMAIL | Personal contact |
| FLD-LIST-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LIST-LOCALISATION_ADRESSE | Exact location |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Legal property document |
| FLD-LIST-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LIST-PREUVE_MANDAT | Legal mandate |
| FLD-LIST-IDENTITE_TITULAIRE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LIST-DERIVED-PRIX_M2 | Prix au m² | prix_global / surface_terrain |
| FLD-LIST-DERIVED-CONSTRUCTIBILITE | Constructibilité | type + documents + zone |
| FLD-LIST-DERIVED-ACCES | Score accessibilité | acces_route + qualite_acces |
| FLD-LIST-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-LIST-DERIVED-TITRE_VALIDE | Titre valide | titre_foncier + verification |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain = pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing ?" | Non applicable pour terrain |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |

---

## MATRIX 7: mise_en_location_commercial

### matrix_id
MATRIX-LIST-RES-007

### canonical_name
Mise en location commercial

### request_family
RESIDENTIAL_LISTING

### transaction_type
RENT

### property_or_service_type
mise_en_location_commercial

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing commercial property for rent. Covers boutiques, shops, offices, warehouses, commercial spaces with business-specific fields: commercial zoning, signage, foot traffic, loading access, business license compatibility, and lease type.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LIST-RELATION_BIEN | Relation bien | always | "Quelle est votre relation ?" | 20 |
| FLD-LIST-TRANSACTION | Transaction | always | Derived (RENT) | 30 |
| FLD-LIST-TYPE_EXACT | Type exact | always | "Type de local commercial ? (boutique, bureau, entrepôt, local professionnel)" | 40 |
| FLD-LIST-LOCALISATION_VILLE | Ville | always | "Ville ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-LOCALISATION_QUARTIER | Quartier | always | "Quartier commercial ?" | 60 |
| FLD-LIST-LOCALISATION_ADRESSE | Adresse | always | "Adresse complète ?" | 65 |
| FLD-LIST-SURFACE | Surface | always | "Surface du local (m²) ?" | 70 |
| FLD-LIST-PRIX_MENSUEL | Loyer mensuel | always | "Loyer mensuel ?" | 75 |
| FLD-LIST-PRIX_CHARGES | Charges | always | "Charges mensuelles ?" | 77 |
| FLD-LIST-DISPONIBILITE_DATE | Date disponibilité | always | "Disponible quand ?" | 80 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-ETAT | État | always | "État du local ?" | 100 |
| FLD-LIST-ACCES_ROUTE | Accès | always | "Accès route/livraison ?" | 110 |
| FLD-LIST-PARKING | Parking | always | "Parking clientèle disponible ?" | 115 |
| FLD-LIST-SECURITE | Sécurité | always | "Sécurité du quartier ?" | 120 |
| FLD-LIST-ELECTRICITE | Électricité | always | "Électricité disponible ?" | 125 |
| FLD-LIST-EAU | Eau | always | "Eau disponible ?" | 130 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONTACT_NOM | Nom | always | "Votre nom ?" | 140 |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | always | "Téléphone ?" | 145 |
| FLD-LIST-CONTACT_EMAIL | Email | always | "Email ?" | 150 |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement | always | "Publication acceptée ?" | 160 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-REGLES_VISITE | Règles visite | always | "Modalités visite ?" | 170 |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires ?" | 175 |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis ?" | 180 |
| FLD-LIST-CONTACT_CANAL | Canal | always | "Canal préféré ?" | 185 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-PRIX_NEGOCIABLE | Négociable | always | "Loyer négociable ?" | 190 |
| FLD-LIST-PRIX_CAUTION | Caution | always | "Dépôt de garantie ?" | 195 |
| FLD-LIST-CONDITION_BAIL | Type de bail | always | "Type de bail commercial ?" | 200 |
| FLD-LIST-CONDITION_PREAVIS | Préavis | always | "Préavis ?" | 205 |
| FLD-LIST-CONDITIONS | Conditions | always | "Conditions particulières ?" | 210 |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Titre foncier | always | "Titre foncier disponible ?" | 215 |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau vérification ?" | 220 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LIST-CLIMATISATION | Climatisation | soft_constraint | 225 |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | soft_constraint | 230 |
| FLD-LIST-INTERNET | Internet | soft_constraint | 235 |
| FLD-LIST-DEPENDANCES | Dépendances | informational_only | 240 |
| FLD-LIST-PHOTOS | Photos | informational_only | 245 |
| FLD-LIST-VIDEOS | Vidéos | informational_only | 250 |
| FLD-LIST-ANNEE_CONSTRUCTION | Année construction | informational_only | 255 |
| FLD-LIST-LOCALISATION_ZONE | Zone commerciale | informational_only | 260 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LIST-LOCALISATION_REPERE | Point de repère | informational_only |
| FLD-LIST-ETAT_DETAIL | Détail état | informational_only |
| FLD-LIST-DISPONIBILITE_DELAI | Délai | informational_only |
| FLD-LIST-MEUBLE | Équipé | informational_only |
| FLD-LIST-PLAN_ETAGE | Plan local | informational_only |
| FLD-LIST-FORAGE | Forage | boost (+5) |
| FLD-LIST-GARDIENNAGE | Gardiennage | informational_only |
| FLD-LIST-CONDITION_GARANTIE | Garantie | informational_only |
| FLD-LIST-CONDITION_HONORAIRES | Honoraires | informational_only |
| FLD-LIST-CONTACT_DISPO | Disponibilité contact | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LIST-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_DUREE | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LIST-CONTACT_TELEPHONE | Personal contact |
| FLD-LIST-CONTACT_NOM | Personal identity |
| FLD-LIST-CONTACT_EMAIL | Personal contact |
| FLD-LIST-PRIX_MENSUEL | Financial - owner pricing |
| FLD-LIST-LOCALISATION_ADRESSE | Exact address |
| FLD-LIST-DOCUMENTS | Legal documents |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Property title |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LIST-DERIVED-PRIX_M2 | Prix au m² | loyer / surface |
| FLD-LIST-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |
| FLD-LIST-DERIVED-QUALITE_COMMERCIALE | Qualité commerciale | weighted(acces, visibilite, securite) |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Local commercial |
| 2 | "Quel standing résidentiel ?" | Non applicable |
| 3 | "Y a-t-il une cuisine ?" | Si pertinent, client le demande |

---

## MATRIX 8: mise_en_vente_commercial

### matrix_id
MATRIX-LIST-RES-008

### canonical_name
Mise en vente commercial

### request_family
RESIDENTIAL_LISTING

### transaction_type
SELL

### property_or_service_type
mise_en_vente_commercial

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing commercial property for sale. Comprehensive characterization of commercial real estate including legal status, business compatibility, income potential (if rented), building condition, and full legal documentation.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LIST-RELATION_BIEN | Relation bien | always | "Quelle est votre relation ?" | 20 |
| FLD-LIST-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LIST-TYPE_EXACT | Type exact | always | "Type de bien commercial ?" | 40 |
| FLD-LIST-LOCALISATION_VILLE | Ville | always | "Ville ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-LOCALISATION_QUARTIER | Quartier | always | "Quartier ?" | 60 |
| FLD-LIST-LOCALISATION_ADRESSE | Adresse | always | "Adresse ?" | 65 |
| FLD-LIST-SURFACE | Surface | always | "Surface totale (m²) ?" | 70 |
| FLD-LIST-PRIX_GLOBAL | Prix de vente | always | "Prix de vente ?" | 75 |
| FLD-LIST-DISPONIBILITE_DATE | Disponibilité | always | "Disponible quand ?" | 80 |
| FLD-LIST-ETAT | État | always | "État général ?" | 100 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-ACCES_ROUTE | Accès | always | "Accès route/livraison ?" | 110 |
| FLD-LIST-PARKING | Parking | always | "Parking ?" | 115 |
| FLD-LIST-SECURITE | Sécurité | always | "Sécurité ?" | 120 |
| FLD-LIST-ELECTRICITE | Électricité | always | "Électricité ?" | 125 |
| FLD-LIST-EAU | Eau | always | "Eau ?" | 130 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONTACT_NOM | Nom | always | "Votre nom ?" | 140 |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | always | "Téléphone ?" | 145 |
| FLD-LIST-CONTACT_EMAIL | Email | always | "Email ?" | 150 |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement | always | "Publication acceptée ?" | 160 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-REGLES_VISITE | Règles visite | always | "Modalités visite ?" | 170 |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires ?" | 175 |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis ?" | 180 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-PRIX_NEGOCIABLE | Négociable | always | "Prix négociable ?" | 190 |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Titre foncier | always | "Titre foncier disponible ?" | 200 |
| FLD-LIST-DOCUMENT_ACTE_VENTE | Acte de vente | always | "Acte de vente original ?" | 205 |
| FLD-LIST-CONDITIONS | Conditions | always | "Conditions particulières ?" | 210 |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau vérification ?" | 220 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LIST-CLIMATISATION | Climatisation | soft_constraint | 225 |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | soft_constraint | 230 |
| FLD-LIST-INTERNET | Internet | soft_constraint | 235 |
| FLD-LIST-PHOTOS | Photos | informational_only | 240 |
| FLD-LIST-VIDEOS | Vidéos | informational_only | 245 |
| FLD-LIST-DEPENDANCES | Dépendances | informational_only | 250 |
| FLD-LIST-ANNEE_CONSTRUCTION | Année construction | informational_only | 255 |
| FLD-LIST-PRIX_DEVISE | Devise | informational_only | 260 |
| FLD-LIST-CONDITION_BAIL | Bail commercial existant | informational_only | 265 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LIST-LOCALISATION_ZONE | Zone | informational_only |
| FLD-LIST-LOCALISATION_REPERE | Point de repère | informational_only |
| FLD-LIST-ETAT_DETAIL | Détail état | informational_only |
| FLD-LIST-DISPONIBILITE_DELAI | Délai | informational_only |
| FLD-LIST-PLAN_ETAGE | Plan local | informational_only |
| FLD-LIST-CONDITION_GARANTIE | Garantie | informational_only |
| FLD-LIST-CONDITION_HONORAIRES | Honoraires | informational_only |
| FLD-LIST-GARDIENNAGE | Gardiennage | informational_only |
| FLD-LIST-CONTACT_CANAL | Canal | informational_only |
| FLD-LIST-CONTACT_DISPO | Disponibilité contact | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LIST-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_DUREE | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LIST-CONTACT_TELEPHONE | Personal contact |
| FLD-LIST-CONTACT_NOM | Personal identity |
| FLD-LIST-CONTACT_EMAIL | Personal contact |
| FLD-LIST-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LIST-LOCALISATION_ADRESSE | Exact address |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LIST-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LIST-PREUVE_MANDAT | Legal mandate |
| FLD-LIST-IDENTITE_TITULAIRE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LIST-DERIVED-PRIX_M2 | Prix au m² | prix_global / surface |
| FLD-LIST-DERIVED-COMPLETUDE | Complétude | weighted fields |
| FLD-LIST-DERIVED-TITRE_VALIDE | Titre valide | titre_foncier + verification |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Local commercial |
| 2 | "Quel standing résidentiel ?" | Non applicable |
| 3 | "Avez-vous un locataire ?" | Si pertinent, mentionné dans conditions |

---

## MATRIX 9: mandat_vente

### matrix_id
MATRIX-LIST-RES-009

### canonical_name
Mandat de vente

### request_family
RESIDENTIAL_LISTING

### transaction_type
SELL

### property_or_service_type
mandat_vente

### requester_typology
mandate_provider

### journey_stage
LISTING

### description
Qualification matrix for sale mandate/agency agreement. The declarant is an agent or agency seeking a mandate from a property owner to sell their property. Focuses on mandate terms, exclusivity, duration, commissions, and powers granted. Different from direct listing — the agent is the one entering the relationship.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous agent immobilier ou mandataire ?" | 10 |
| FLD-LIST-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec le propriétaire ?" | 20 |
| FLD-LIST-AUTORISATION_MANDAT | Autorisation | always | "Avez-vous un mandat écrit du propriétaire ?" | 30 |
| FLD-LIST-TRANSACTION | Transaction | always | Derived (SELL) | 35 |
| FLD-LIST-TYPE_EXACT | Type exact | always | "Type de bien à vendre ?" | 40 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-LOCALISATION_VILLE | Ville | always | "Ville du bien ?" | 50 |
| FLD-LIST-LOCALISATION_QUARTIER | Quartier | always | "Quartier ?" | 55 |
| FLD-LIST-PRIX_GLOBAL | Prix de vente | always | "Prix de vente proposé ?" | 60 |
| FLD-LIST-SURFACE | Surface | always | "Surface ?" | 65 |
| FLD-LIST-CHAMBRES | Chambres | always | "Nombre de chambres ?" | 70 |
| FLD-LIST-DOUCHES | Douches | always | "Nombre de douches ?" | 75 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-NATURE_MANDAT | Nature du mandat | always | "Type de mandat ? (simple, exclusif, co-exclusif)" | 80 |
| FLD-LIST-DUREE_MANDAT | Durée mandat | always | "Durée du mandat ?" | 85 |
| FLD-LIST-POUVOIRS_ACCORDS | Pouvoirs accordés | always | "Quels pouvoirs vous sont accordés ?" | 90 |
| FLD-LIST-IDENTITE_TITULAIRE | Identité propriétaire | always | "Nom du propriétaire mandant ?" | 95 |
| FLD-LIST-PREUVE_MANDAT | Preuve mandat | always | "Document de mandat signé disponible ?" | 100 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONTACT_NOM | Nom agent | always | "Nom de l'agent/agence ?" | 140 |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | always | "Téléphone ?" | 145 |
| FLD-LIST-CONTACT_EMAIL | Email | always | "Email professionnel ?" | 150 |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement | always | "Le propriétaire consent-il à la publication ?" | 160 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-REGLES_VISITE | Règles visite | always | "Qui organise les visites ?" | 170 |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires de visite ?" | 175 |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis pour visite ?" | 180 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONDITION_HONORAIRES | Honoraires | always | "Montant/ % des honoraires agence ?" | 190 |
| FLD-LIST-CONDITIONS | Conditions mandat | always | "Conditions particulières du mandat ?" | 195 |
| FLD-LIST-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 200 |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Titre foncier | always | "Titre foncier vérifié ?" | 205 |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau vérification propriétaire/bien ?" | 210 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LIST-ETAT | État bien | informational_only | 215 |
| FLD-LIST-MEUBLE | Meublé | informational_only | 220 |
| FLD-LIST-CLIMATISATION | Climatisation | informational_only | 225 |
| FLD-LIST-PARKING | Parking | informational_only | 230 |
| FLD-LIST-PHOTOS | Photos | informational_only | 235 |
| FLD-LIST-VIDEOS | Vidéos | informational_only | 240 |
| FLD-LIST-DISPONIBILITE_DATE | Disponibilité | informational_only | 245 |
| FLD-LIST-CUISINE | Cuisine | informational_only | 250 |
| FLD-LIST-SALONS | Salons | informational_only | 255 |
| FLD-LIST-ANNEE_CONSTRUCTION | Année construction | informational_only | 260 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LIST-ETAT_DETAIL | Détail état | informational_only |
| FLD-LIST-DEPENDANCES | Dépendances | informational_only |
| FLD-LIST-JARDIN | Jardin | informational_only |
| FLD-LIST-PISCINE | Piscine | informational_only |
| FLD-LIST-COUR | Cour | informational_only |
| FLD-LIST-CLOTURE | Clôture | informational_only |
| FLD-LIST-SECURITE | Sécurité | informational_only |
| FLD-LIST-GARDIENNAGE | Gardiennage | informational_only |
| FLD-LIST-INTERNET | Internet | informational_only |
| FLD-LIST-ELECTRICITE | Électricité | informational_only |
| FLD-LIST-EAU | Eau | informational_only |
| FLD-LIST-ACCES_ROUTE | Accès route | informational_only |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | informational_only |
| FLD-LIST-FORAGE | Forage | informational_only |
| FLD-LIST-BALCON | Balcon | informational_only |
| FLD-LIST-ASCENSEUR | Ascenseur | informational_only |
| FLD-LIST-LOCALISATION_ZONE | Zone | informational_only |
| FLD-LIST-LOCALISATION_REPERE | Point de repère | informational_only |
| FLD-LIST-DISPONIBILITE_DELAI | Délai | informational_only |
| FLD-LIST-CONTACT_CANAL | Canal | informational_only |
| FLD-LIST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-LIST-CONDITION_GARANTIE | Garantie | informational_only |
| FLD-LIST-CONDITION_PREAVIS | Préavis | informational_only |
| FLD-LIST-PLAN_ETAGE | Plan | informational_only |
| FLD-LIST-VIDEO_TOUR | Visite virtuelle | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LIST-DUREE_MANDAT_DATE_FIN | duree = DUREE_DETERMINEE | verification_only |
| FLD-LIST-POUVOIRS_LIMITES | pouvoirs != TOUS_POUVOIRS | verification_only |
| FLD-LIST-DOCUMENT_CERTIFICAT_PROPRIETE | titre_foncier absent | verification_only |
| FLD-LIST-DOCUMENT_ACTE_VENTE | if previous sale | verification_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_DUREE | consent = true | informational_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LIST-CONTACT_TELEPHONE | Professional contact |
| FLD-LIST-CONTACT_NOM | Agent/agency identity |
| FLD-LIST-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LIST-IDENTITE_TITULAIRE | Owner identity (third party) |
| FLD-LIST-PREUVE_MANDAT | Legal mandate document |
| FLD-LIST-NATURE_MANDAT | Mandate terms |
| FLD-LIST-DUREE_MANDAT | Mandate duration |
| FLD-LIST-POUVOIRS_ACCORDS | Mandate powers |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | Property title document |
| FLD-LIST-CONDITION_HONORAIRES | Agency commission structure |
| FLD-LIST-CONTACT_EMAIL | Professional contact |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LIST-DERIVED-MANDAT_ACTIF | Mandat actif | duree_mandat + date_fin vs date_courante |
| FLD-LIST-DERIVED-MANDAT_VALIDE | Mandat valide | preuve_mandat + signature |
| FLD-LIST-DERIVED-EXCLUSIVITE | Exclusivité | nature_mandat (EXCLUSIF) |
| FLD-LIST-DERIVED-PRIX_M2 | Prix au m² | prix_global / surface |
| FLD-LIST-DERIVED-COMPLETUDE | Complétude dossier | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Pourquoi le propriétaire vend-il ?" | Hors scope |
| 2 | "Quel est le salaire du propriétaire ?" | Non pertinent |
| 3 | "Le propriétaire a-t-il urgemment besoin d'argent ?" | Suggestif, contraire à l'éthique |
| 4 | "Combien de pièces ?" | Non canonique |
| 5 | "Acceptez-vous moins de commission ?" | À négocier séparément |

---

## MATRIX 10: mandat_location

### matrix_id
MATRIX-LIST-RES-010

### canonical_name
Mandat de location

### request_family
RESIDENTIAL_LISTING

### transaction_type
RENT

### property_or_service_type
mandat_location

### requester_typology
mandate_provider

### journey_stage
LISTING

### description
Qualification matrix for rental mandate/agency agreement. Similar to mandat_vente but focused on rental: mandate terms, exclusivity for rental, commission structure (typically owner pays 1 month rent), duration, and tenant-finding services included.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous agent immobilier ou mandataire ?" | 10 |
| FLD-LIST-RELATION_BIEN | Relation bien | always | "Relation avec le propriétaire ?" | 20 |
| FLD-LIST-AUTORISATION_MANDAT | Autorisation | always | "Mandat écrit du propriétaire ?" | 30 |
| FLD-LIST-TRANSACTION | Transaction | always | Derived (RENT) | 35 |
| FLD-LIST-TYPE_EXACT | Type exact | always | "Type de bien à louer ?" | 40 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-LOCALISATION_VILLE | Ville | always | "Ville du bien ?" | 50 |
| FLD-LIST-LOCALISATION_QUARTIER | Quartier | always | "Quartier ?" | 55 |
| FLD-LIST-PRIX_MENSUEL | Loyer mensuel | always | "Loyer mensuel demandé ?" | 60 |
| FLD-LIST-SURFACE | Surface | always | "Surface ?" | 65 |
| FLD-LIST-CHAMBRES | Chambres | always | "Nombre de chambres ?" | 70 |
| FLD-LIST-DOUCHES | Douches | always | "Nombre de douches ?" | 75 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-NATURE_MANDAT | Nature mandat | always | "Type de mandat location ?" | 80 |
| FLD-LIST-DUREE_MANDAT | Durée mandat | always | "Durée du mandat ?" | 85 |
| FLD-LIST-POUVOIRS_ACCORDS | Pouvoirs | always | "Pouvoirs accordés ?" | 90 |
| FLD-LIST-IDENTITE_TITULAIRE | Identité propriétaire | always | "Nom du propriétaire ?" | 95 |
| FLD-LIST-PREUVE_MANDAT | Preuve mandat | always | "Mandat signé disponible ?" | 100 |
| FLD-LIST-ETAT | État bien | always | "État du bien ?" | 105 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONTACT_NOM | Nom agent | always | "Nom agent/agence ?" | 140 |
| FLD-LIST-CONTACT_TELEPHONE | Téléphone | always | "Téléphone ?" | 145 |
| FLD-LIST-CONTACT_EMAIL | Email | always | "Email professionnel ?" | 150 |
| FLD-LIST-CONSENTEMENT_PUBLICATION | Consentement | always | "Consentement publication propriétaire ?" | 160 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-REGLES_VISITE | Règles visite | always | "Modalités visites ?" | 170 |
| FLD-LIST-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires visites ?" | 175 |
| FLD-LIST-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis visites ?" | 180 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LIST-CONDITION_HONORAIRES | Honoraires | always | "Honoraires agence ? (charge propriétaire/locataire)" | 190 |
| FLD-LIST-CONDITIONS | Conditions | always | "Conditions mandat location ?" | 195 |
| FLD-LIST-PRIX_CAUTION | Caution | always | "Dépôt de garantie ?" | 200 |
| FLD-LIST-PRIX_CHARGES | Charges | always | "Charges ?" | 205 |
| FLD-LIST-CONDITION_BAIL | Type bail | always | "Type de bail proposé ?" | 210 |
| FLD-LIST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau vérification ?" | 215 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LIST-MEUBLE | Meublé | informational_only | 220 |
| FLD-LIST-CUISINE | Cuisine | informational_only | 225 |
| FLD-LIST-SALONS | Salons | informational_only | 230 |
| FLD-LIST-PARKING | Parking | informational_only | 235 |
| FLD-LIST-CLIMATISATION | Climatisation | informational_only | 240 |
| FLD-LIST-PHOTOS | Photos | informational_only | 245 |
| FLD-LIST-VIDEOS | Vidéos | informational_only | 250 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LIST-ETAT_DETAIL | Détail état | informational_only |
| FLD-LIST-ANNEE_CONSTRUCTION | Année construction | informational_only |
| FLD-LIST-DEPENDANCES | Dépendances | informational_only |
| FLD-LIST-JARDIN | Jardin | informational_only |
| FLD-LIST-COUR | Cour | informational_only |
| FLD-LIST-CLOTURE | Clôture | informational_only |
| FLD-LIST-BALCON | Balcon | informational_only |
| FLD-LIST-ASCENSEUR | Ascenseur | informational_only |
| FLD-LIST-SECURITE | Sécurité | informational_only |
| FLD-LIST-INTERNET | Internet | informational_only |
| FLD-LIST-ELECTRICITE | Électricité | informational_only |
| FLD-LIST-EAU | Eau | informational_only |
| FLD-LIST-ACCES_ROUTE | Accès route | informational_only |
| FLD-LIST-GROUPE_ELECTROGENE | Groupe électrogène | informational_only |
| FLD-LIST-FORAGE | Forage | informational_only |
| FLD-LIST-LOCALISATION_ZONE | Zone | informational_only |
| FLD-LIST-LOCALISATION_REPERE | Point repère | informational_only |
| FLD-LIST-DISPONIBILITE_DELAI | Délai | informational_only |
| FLD-LIST-CONTACT_CANAL | Canal | informational_only |
| FLD-LIST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-LIST-CONDITION_GARANTIE | Garantie | informational_only |
| FLD-LIST-CONDITION_PREAVIS | Préavis | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LIST-DUREE_MANDAT_DATE_FIN | duree = DUREE_DETERMINEE | verification_only |
| FLD-LIST-POUVOIRS_LIMITES | pouvoirs != TOUS_POUVOIRS | verification_only |
| FLD-LIST-DOCUMENT_TITRE_FONCIER | niveau_verification = COMPLET | verification_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_DUREE | consent = true | informational_only |
| FLD-LIST-CONSENTEMENT_PUBLICATION_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LIST-CONTACT_TELEPHONE | Professional contact |
| FLD-LIST-CONTACT_NOM | Agent/agency identity |
| FLD-LIST-PRIX_MENSUEL | Financial - owner pricing |
| FLD-LIST-IDENTITE_TITULAIRE | Owner identity |
| FLD-LIST-PREUVE_MANDAT | Legal mandate |
| FLD-LIST-NATURE_MANDAT | Mandate terms |
| FLD-LIST-DUREE_MANDAT | Mandate duration |
| FLD-LIST-POUVOIRS_ACCORDS | Mandate powers |
| FLD-LIST-CONDITION_HONORAIRES | Commission structure |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LIST-DERIVED-MANDAT_ACTIF | Mandat actif | duree_mandat + date_fin |
| FLD-LIST-DERIVED-MANDAT_VALIDE | Mandat valide | preuve_mandat + signature |
| FLD-LIST-DERIVED-EXCLUSIVITE | Exclusivité | nature_mandat |
| FLD-LIST-DERIVED-PRIX_M2 | Prix au m² | prix_mensuel / surface |
| FLD-LIST-DERIVED-COMPLETUDE | Complétude dossier | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Pourquoi le propriétaire loue-t-il ?" | Hors scope |
| 2 | "Le propriétaire est-il pressé ?" | Suggestif |
| 3 | "Combien de pièces ?" | Non canonique |
| 4 | "Quel est le salaire du propriétaire ?" | Non pertinent |
| 5 | "Acceptez-vous une commission plus basse ?" | À négocier séparément |

---

# End of Document — Residential Listing Matrices
