# COMMERCIAL PROPERTY QUALIFICATION MATRICES — LAWIM Heritage Gold

**Mission:** LAWIM Heritage Gold — Matrices de qualification exhaustives pour tous les types de biens commerciaux et d'investissement
**Statut:** Gold Validated
**Version:** 1.0
**Date:** 2026-07-15
**Principe:** 21 matrices canoniques — 16 types commerciaux, 5 types d'investissement — chaque champ sourcé et confidentié

---

## TABLE OF CONTENTS

1. [Common Field Reference](#common-field-reference)
2. [boutique (Shop)](#boutique-shop)
3. [bureau (Office)](#bureau-office)
4. [local_commercial (Commercial Space)](#local_commercial-commercial-space)
5. [magasin (Store)](#magasin-store)
6. [entrepot (Warehouse)](#entrepot-warehouse)
7. [hangar (Shed)](#hangar-shed)
8. [atelier (Workshop)](#atelier-workshop)
9. [restaurant](#restaurant)
10. [bar](#bar)
11. [hotel (Boutique Hotel)](#hotel-boutique-hotel)
12. [auberge (Inn)](#auberge-inn)
13. [immeuble_de_rapport (Income Property)](#immeuble_de_rapport-income-property)
14. [immeuble_commercial (Commercial Building)](#immeuble_commercial-commercial-building)
15. [station_service (Gas Station)](#station_service-gas-station)
16. [site_industriel (Industrial Site)](#site_industriel-industrial-site)
17. [espace_evenementiel (Event Space)](#espace_evenementiel-event-space)
18. [investissement_locatif (Rental Investment)](#investissement_locatif-rental-investment)
19. [investissement_terrain (Land Investment)](#investissement_terrain-land-investment)
20. [investissement_immobilier_commercial (Commercial RE Investment)](#investissement_immobilier_commercial-commercial-re-investment)
21. [investissement_promotion (Development Investment)](#investissement_promotion-development-investment)
22. [syndicat_copropriete (Condo/Co-ownership)](#syndicat_copropriete-condo-co-ownership)

---

## Common Field Reference

### Common Fields for Commercial Property Types

| field_id | label | description | data_type | allowed_values | mandatory_when | optional_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COM-COMMON-001 | activité_prévue | Planned business activity | string | — | always for comm | — | min_length:3, matching:activité | "Quel type d'activité ?" | 10 | hard_constraint | public | commercial_heritage_extraction.md §6.5 | HIGH |
| COM-COMMON-002 | activité_autorisée | Permitted use per zoning | string | — | if_activité_sensible | general | matching:activité_autorisée | "Usage autorisé ?" | 20 | hard_constraint | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-003 | surface_min | Minimum surface (m²) | integer | — | always for comm | — | min:5, max:50000 | "Surface minimale ?" | 15 | hard_constraint | public | commercial_heritage_extraction.md §6.5 | HIGH |
| COM-COMMON-004 | surface_max | Maximum surface (m²) | integer | — | if_surface_min_provided | general | max:100000 | "Surface maximale ?" | 16 | ranking_preference | public | commercial_heritage_extraction.md §6.5 | HIGH |
| COM-COMMON-005 | ville | Target city | string | enum:cities_cm | always | — | in:cities_cm | "Dans quelle ville ?" | 5 | hard_constraint | public | qualification_model.md §7 | HIGH |
| COM-COMMON-006 | quartier | Neighborhood/zone | string | — | always for comm | general | in:neighborhoods_by_city | "Quartier ou zone ?" | 8 | hard_constraint | public | qualification_model.md §7 | HIGH |
| COM-COMMON-007 | budget_achat | Purchase budget (FCFA) | integer | — | transaction=buy | transaction=rent | min:100000, max:10000000000 | "Budget achat ?" | 12 | hard_constraint | public | matching_model.md §2 | HIGH |
| COM-COMMON-008 | budget_location | Monthly rent (FCFA) | integer | — | transaction=rent | transaction=buy | min:10000, max:50000000 | "Loyer max ?" | 12 | hard_constraint | public | matching_model.md §2 | HIGH |
| COM-COMMON-009 | hauteur_sous_plafond | Ceiling height (m) | float | — | type=entrepot/hangar/atelier | boutique/bureau | min:2.0, max:20.0 | "Hauteur sous plafond ?" | 30 | soft_constraint | public | 02C-INDUSTRIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-010 | accès_véhicules | Vehicle access | string | enum:poids_lourds,livraisons,utilitaire,voiture,aucun | type=entrepot/hangar/site_industriel | general | — | "Accès véhicules ?" | 25 | soft_constraint | public | 02C-INDUSTRIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-011 | visibilité_route | Road visibility | boolean | — | boutique/magasin | entrepot/atelier | — | "Visible depuis la route ?" | 28 | ranking_preference | public | commercial_heritage_extraction.md §6.5 | HIGH |
| COM-COMMON-012 | façade | Storefront width (m) | float | — | boutique/magasin | general | min:1.0, max:50.0 | "Largeur façade ?" | 29 | ranking_preference | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-013 | flux_passage | Foot traffic level | string | enum:très_élevé,élevé,moyen,faible,aucun | boutique/restaurant/bar | bureau/entrepot | — | "Flux piéton ?" | 27 | ranking_preference | public | commercial_heritage_extraction.md §6.5 | HIGH |
| COM-COMMON-014 | parking | Parking need | string | enum:indispensable,souhaité,optionnel,pas_besoin | restaurant/hotel/bar | general | — | "Parking nécessaire ?" | 35 | soft_constraint | public | commercial_heritage_extraction.md §6.5 | HIGH |
| COM-COMMON-015 | places_parking | Parking spaces | integer | — | parking=indispensable | parking=souhaité | min:1, max:500 | "Combien de places ?" | 36 | soft_constraint | public | commercial_heritage_extraction.md §6.5 | HIGH |
| COM-COMMON-016 | stockage | Storage needed | boolean | — | magasin/entrepot | — | — | "Stockage ?" | 40 | ranking_preference | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-017 | surface_stockage | Storage area (m²) | integer | — | stockage=true | stockage=false | min:1, max:10000 | "Surface stockage ?" | 41 | ranking_preference | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-018 | électricité | Electricity | boolean | — | always for comm | — | — | "Électricité ?" | 42 | soft_constraint | public | commercial_heritage_extraction.md §6.5 | HIGH |
| COM-COMMON-019 | puissance_électrique | Power (kVA) | integer | — | type=atelier/restaurant/industriel | general | min:1, max:5000 | "Puissance électrique ?" | 43 | soft_constraint | public | 02C-INDUSTRIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-020 | eau | Water supply | boolean | — | restaurant/bar/hotel/atelier | bureau | — | "Eau courante ?" | 44 | soft_constraint | public | commercial_heritage_extraction.md §6.5 | HIGH |
| COM-COMMON-021 | licence_exploitation | Operating license | string | enum:licence_alcool,licence_restauration,patente,agrément,aucune | restaurant/bar/hotel | bureau/boutique | — | "Licence nécessaire ?" | 50 | hard_constraint | public | 02B-COMMERCIAL-REFERENCE.md Ch.5 | HIGH |
| COM-COMMON-022 | nuisances | Accepted nuisances | string | enum:bruit,odeur,vibrations,fumée,poussière,aucune | atelier/industriel | boutique/bureau | — | "Nuisances acceptables ?" | 55 | soft_constraint | semi_private | 02B-COMMERCIAL-REFERENCE.md Ch.5 | HIGH |
| COM-COMMON-023 | voisinage | Preferred neighbors | string | enum:commerces,entreprises,résidentiel,industriel,mixte | general | — | — | "Type de voisinage ?" | 56 | ranking_preference | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-024 | fonds_commerce | Goodwill included | boolean | — | transaction=cession | transaction=location | — | "Fonds de commerce inclus ?" | 60 | soft_constraint | sensitive | 02B-COMMERCIAL-REFERENCE.md Ch.6 | HIGH |
| COM-COMMON-025 | chiffre_affaires | Annual revenue | integer | — | fonds_commerce=true | fonds_commerce=false | min:0 | "Chiffre d'affaires ?" | 61 | ranking_preference | sensitive | 02B-COMMERCIAL-REFERENCE.md Ch.6 | HIGH |
| COM-COMMON-026 | zone_commerciale | Commercial zone | string | enum:centre_ville,zone_industrielle,périphérie,axe_principal,résidentiel | general | — | — | "Type zone commerciale ?" | 22 | soft_constraint | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-027 | période_disponibilité | Availability date | date | — | general | fast_move | after:today | "Disponible à partir de ?" | 65 | soft_constraint | public | qualification_model.md §6 | HIGH |
| COM-COMMON-028 | documents_juridiques | Legal documents | string | enum:bail_commercial,titre_foncier,brouillon,bail_cessible,autorisation,aucun | always for comm | — | — | "Documents requis ?" | 70 | soft_constraint | semi_private | 02B-COMMERCIAL-REFERENCE.md Ch.5 | HIGH |
| COM-COMMON-029 | bail_existant | Existing lease terms | string | — | transaction=reprise | transaction=nouvelle_location | — | "Conditions bail existant ?" | 71 | soft_constraint | semi_private | 02B-COMMERCIAL-REFERENCE.md Ch.6 | HIGH |
| COM-COMMON-030 | dépôt_garantie | Security deposit (months) | integer | — | transaction=location | transaction=achat | min:1, max:24 | "Dépôt garantie (mois) ?" | 72 | ranking_preference | public | qualification_model.md §6 | HIGH |
| COM-COMMON-031 | accès_pmr | PMR accessibility | boolean | — | hotel/restaurant/bureau | general | — | "Accès PMR ?" | 45 | soft_constraint | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-032 | climatisation | Air conditioning | boolean | — | general | — | — | "Climatisation ?" | 46 | ranking_preference | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-033 | état_local | Property condition | string | enum:neuf,très_bon,bon,à_rénover,brut | general | — | — | "État du local ?" | 48 | ranking_preference | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-034 | transaction | Transaction type | string | enum:location,achat,cession,bail_commercial | always | — | in:commercial_transactions | "Location/achat/cession ?" | 3 | hard_constraint | public | qualification_model.md §6 | HIGH |
| COM-COMMON-035 | nombre_pièces | Number of rooms/offices | integer | — | type=bureau | general | min:1, max:200 | "Combien de pièces ?" | 32 | ranking_preference | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-036 | étage | Floor level | string | enum:rdc,1er,2ème,3ème+,sous-sol | boutique/magasin | general | — | "Quel étage ?" | 33 | soft_constraint | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-037 | standing | Standing level | string | enum:économique,standard,premium,luxe | general | — | — | "—"(never ask—deduce) | 38 | ranking_preference | public | deduction_only | HIGH |
| COM-COMMON-038 | délai | Time horizon | string | enum:urgent_1sem,rapide_1mois,normal_3mois,flexible_6mois,pas_délai | general | — | — | "Délai ?" | 18 | ranking_preference | public | qualification_model.md §6 | HIGH |
| COM-COMMON-039 | contact_nom | Requester name | string | — | always | — | min_length:2 | "Votre nom ?" | 80 | soft_constraint | private | qualification_model.md §6 | HIGH |
| COM-COMMON-040 | contact_téléphone | Phone number | string | — | always | — | regex:^\+?[0-9]{8,15}$ | "Téléphone ?" | 82 | soft_constraint | private | qualification_model.md §6 | HIGH |
| COM-COMMON-041 | contact_email | Email address | string | — | diaspora_investor | general | regex:^[^@]+@[^@]+$ | "Email ?" | 83 | soft_constraint | private | qualification_model.md §6 | HIGH |
| COM-COMMON-042 | urgence | Urgency | string | enum:très_urgent,urgent,moyen,pas_urgent | general | — | — | "Urgence ?" | 68 | ranking_preference | private | qualification_model.md §5 | HIGH |
| COM-COMMON-043 | nombre_employés | Number of employees | integer | — | type=bureau/commercial | general | min:0, max:1000 | "Combien d'employés ?" | 34 | ranking_preference | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-044 | ouverture_prévue | Planned opening date | date | — | general | — | after:today | "Date ouverture ?" | 66 | ranking_preference | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |
| COM-COMMON-045 | horaires_ouverture | Operating hours | string | enum:journée,soirée,24h/24,weekend,flexible | general | — | — | "Horaires ?" | 67 | ranking_preference | public | 02B-COMMERCIAL-REFERENCE.md Ch.3 | HIGH |

### Common Fields for Investment Property Types

| field_id | label | description | data_type | allowed_values | mandatory_when | optional_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INV-COMMON-001 | budget_investissement | Total investment budget (FCFA) | integer | — | always | — | min:100000, max:100000000000 | "Budget total d'investissement ?" | 10 | hard_constraint | private | investor_matrices.json | HIGH |
| INV-COMMON-002 | rendement_cible | Target annual yield (%) | float | — | always | — | min:0, max:100 | "Rendement annuel visé ?" | 15 | hard_constraint | private | investor_matrices.json | HIGH |
| INV-COMMON-003 | horizon_investissement | Investment horizon | string | enum:court(1-3ans),moyen(3-7ans),long(7-15ans),très_long(15ans+) | always | — | — | "Horizon ?" | 20 | soft_constraint | private | investor_matrices.json | HIGH |
| INV-COMMON-004 | risque_accepté | Risk tolerance | string | enum:très_faible,faible,moyen,élevé,très_élevé | always | — | — | "Niveau de risque ?" | 25 | soft_constraint | private | investor_matrices.json | HIGH |
| INV-COMMON-005 | stratégie_investissement | Investment strategy | string | enum:plus-value,revenu_locatif,mixte,rénovation,développement | always | — | — | "Stratégie ?" | 22 | soft_constraint | private | investor_matrices.json | HIGH |
| INV-COMMON-006 | ville_investissement | Target city | string | enum:cities_cm | always | — | in:cities_cm | "Ville ?" | 5 | hard_constraint | public | investor_matrices.json | HIGH |
| INV-COMMON-007 | zone_préférée_investissement | Preferred zone | string | — | general | — | in:neighborhoods_by_city | "Zone préférée ?" | 8 | soft_constraint | public | investor_matrices.json | HIGH |
| INV-COMMON-008 | expérience_immobilière | Experience level | string | enum:débutant,intermédiaire,avancé,professionnel | general | — | — | "Expérience ?" | 30 | soft_constraint | private | investor_matrices.json | HIGH |
| INV-COMMON-009 | source_financement | Funding source | string | enum:fonds_propres,crédit,partenariat,diaspora,investisseurs_privés,mixte | general | — | — | "Source de financement ?" | 35 | soft_constraint | sensitive | investor_matrices.json | HIGH |
| INV-COMMON-010 | autres_investissements | Other investments | string | — | general | débutant | — | "Autres investissements ?" | 40 | ranking_preference | private | investor_matrices.json | HIGH |
| INV-COMMON-011 | besoin_accompagnement | Need accompaniment | boolean | — | diaspora_investor | local_investor | — | "Accompagnement ?" | 50 | soft_constraint | private | investor_matrices.json | HIGH |
| INV-COMMON-012 | contact_nom_inv | Investor name | string | — | always | — | min_length:2 | "Nom ?" | 75 | soft_constraint | private | qualification_model.md §6 | HIGH |
| INV-COMMON-013 | contact_téléphone_inv | Phone number | string | — | always | — | regex:^\+?[0-9]{8,15}$ | "Téléphone ?" | 78 | soft_constraint | private | qualification_model.md §6 | HIGH |
| INV-COMMON-014 | contact_email_inv | Email | string | — | diaspora_investor | general | regex:^[^@]+@[^@]+$ | "Email ?" | 80 | soft_constraint | private | qualification_model.md §6 | HIGH |
| INV-COMMON-015 | diaspora_flag | Diaspora flag | boolean | — | automatic | — | inferred | — | 90 | ranking_preference | private | qualification_heritage_extraction.md §10 | HIGH |
| INV-COMMON-016 | proche_sur_place | Local representative | boolean | — | diaspora_investor | local_investor | — | "Proche sur place ?" | 55 | soft_constraint | private | qualification_heritage_extraction.md §10.7 | HIGH |
| INV-COMMON-017 | estimation_humaine | Human valuation needed | boolean | — | general | — | — | "Estimation humaine ?" | 60 | soft_constraint | private | qualification_heritage_extraction.md §6.7 | HIGH |
| INV-COMMON-018 | documents_souhaités | Supplementary docs | string | enum:titre,bail,diagnostics,comptes,étude,aucun | diaspora_investor | — | — | "Documents complémentaires ?" | 65 | soft_constraint | private | qualification_heritage_extraction.md §6.7 | HIGH |

### Forbidden Questions for All Commercial Types

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| COM-FBD-001 | "Âge ?" | Age discrimination prohibited | Directive/00-CONSTITUTION.md Art.14 | HIGH |
| COM-FBD-002 | "Situation matrimoniale ?" | Marital status irrelevant | Directive/00-CONSTITUTION.md Art.14 | HIGH |
| COM-FBD-003 | "Chambres à coucher ?" | Residential criterion | qualification_heritage_extraction.md §12.14 | HIGH |
| COM-FBD-004 | "Salles de bain ?" | Residential criterion | qualification_heritage_extraction.md §12.14 | HIGH |
| COM-FBD-005 | "Standing ?" (explicit) | Must be deduced | qualification_heritage_extraction.md §12.5 | HIGH |
| COM-FBD-006 | "Enfants ?" | Personal data | Directive/00-CONSTITUTION.md Art.14 | HIGH |
| COM-FBD-007 | "Revenu mensuel ?" (personal) | Not relevant for commercial | Directive/00-CONSTITUTION.md Art.14 | HIGH |
| COM-FBD-008 | "Ethnie ?" | Prohibited discrimination | Directive/00-CONSTITUTION.md Art.14 | HIGH |
| COM-FBD-009 | "Religion ?" | Prohibited discrimination | Directive/00-CONSTITUTION.md Art.14 | HIGH |
| COM-FBD-010 | "Orientation politique ?" | Prohibited discrimination | Directive/00-CONSTITUTION.md Art.14 | HIGH |
| COM-FBD-011 | "Usage résidentiel ?" | Not commercial | qualification_heritage_extraction.md §12.14 | HIGH |
| COM-FBD-012 | "Pièces principales ?" | Residential criterion | qualification_heritage_extraction.md §12.14 | HIGH |

---

## 1. boutique (Shop)

### Matrix 1.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-001 |
| canonical_name | boutique |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY, CESSION_BAIL |
| property_or_service_type | boutique |
| requester_typology | professional, business, entrepreneur |
| journey_stage | SEARCH |
| description | Matrice de qualification pour boutique / magasin de détail. |

### Matrix 1.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOU-01 | activité_prévue | Type de commerce | string | — | always | min_len:3 | "Type de commerce ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| BOU-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface minimale ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| BOU-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| BOU-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| BOU-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Location/achat/cession ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| BOU-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |

### Matrix 1.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOU-S01 | étage | Étage préféré | string | enum:rdc,1er,s/sol | "Quel étage ?" | 20 | soft_constraint | COM-COMMON-036 | HIGH |
| BOU-S02 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| BOU-S03 | façade | Largeur façade | float | — | "Largeur façade ?" | 25 | ranking_preference | COM-COMMON-012 | HIGH |
| BOU-S04 | flux_passage | Flux piéton | string | enum:très_élevé,élevé,moyen,faible | "Flux piéton ?" | 24 | ranking_preference | COM-COMMON-013 | HIGH |
| BOU-S05 | zone_commerciale | Zone commerciale | string | enum:centre_ville,axe_commercial,quartier,galerie | "Type zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |

### Matrix 1.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| BOU-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| BOU-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| BOU-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| BOU-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| BOU-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| BOU-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| BOU-M07 | flux | Flux piéton | string | ranking_preference | matching_model §22 | HIGH |

### Matrix 1.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOU-I01 | projet | Projet boutique | string | "Parlez de votre projet" | 85 | soft_constraint | qualification §6 | HIGH |
| BOU-I02 | expérience | Expérience commerce | string | "Expérience dans le commerce ?" | 86 | ranking_preference | qualification §6 | HIGH |
| BOU-I03 | date_ouverture | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |

### Matrix 1.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BOU-V01 | disponibilité | Disponibilité visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| BOU-V02 | accompagnement | Visite accompagnée | boolean | "Accompagnement ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| BOU-V03 | nb_visiteurs | Nombre visiteurs | integer | "Combien ?" | 92 | qualification §6 | HIGH |

### Matrix 1.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOU-T01 | pièce_id | Pièce identité | string | enum:cn,passport,permis | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| BOU-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| BOU-T03 | garantie | Garantie | string | enum:caution,dépôt,garant,assurance | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 1.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOU-R01 | parking | Parking | string | enum:indispensable,souhaité,optionnel,pas | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| BOU-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| BOU-R03 | vitrine | Vitrine | boolean | — | "Vitrine ?" | 26 | ranking_preference | 02B-Ch.3 | HIGH |
| BOU-R04 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| BOU-R05 | climatisation | Climatisation | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| BOU-R06 | accès_pmr | Accès PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 1.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BOU-O01 | enseigne | Enseigne | string | "Enseigne ?" | 50 | 02B-Ch.3 | HIGH |
| BOU-O02 | surface_stockage | Surface stockage | integer | "Surface stockage ?" | 41 | COM-COMMON-017 | HIGH |
| BOU-O03 | caisses | Caisses | integer | "Caisses ?" | 52 | 02B-Ch.3 | HIGH |
| BOU-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 1.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BOU-C01 | fonds_commerce | Fonds commerce | integer | cession_bail | 60 | COM-COMMON-024 | HIGH |
| BOU-C02 | chiffre_affaires | CA annuel | integer | fonds_commerce | 61 | COM-COMMON-025 | HIGH |
| BOU-C03 | bail_restant | Bail restant (mois) | integer | cession_bail | 62 | COM-COMMON-029 | HIGH |
| BOU-C04 | licence_alcool | Licence alcool | boolean | activité=bar | 50 | COM-COMMON-021 | HIGH |

### Matrix 1.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| BOU-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| BOU-SN02 | marge | Marge | float | sensitive | 02B-Ch.6 | HIGH |
| BOU-SN03 | fournisseurs | Fournisseurs | string | sensitive | 02B-Ch.6 | HIGH |
| BOU-SN04 | identité_bailleur | Identité bailleur | string | sensitive | anonymity | HIGH |

### Matrix 1.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| BOU-D01 | standing | Standing commercial | string | déduit:visibilité+flux+zone+état | deduction_only | HIGH |
| BOU-D02 | potentiel | Potentiel commercial | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| BOU-D03 | budget_mensualisé | Coût mensuel | integer | budget/120 ou budget | pricing_model | HIGH |

### Matrix 1.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| BOU-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| BOU-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| BOU-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |

---

## 2. bureau (Office)

### Matrix 2.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-002 |
| canonical_name | bureau |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY |
| property_or_service_type | bureau |
| requester_typology | professional, business, freelance, enterprise |
| journey_stage | SEARCH |
| description | Matrice de qualification pour bureaux professionnels. |

### Matrix 2.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BUR-01 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| BUR-02 | nb_pièces | Nb bureaux | integer | — | always | min:1 | "Nb bureaux ?" | 18 | soft_constraint | public | COM-COMMON-035 | HIGH |
| BUR-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| BUR-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| BUR-05 | transaction | Transaction | string | enum:location,achat | always | in:types | "Location/achat ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| BUR-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| BUR-07 | employés | Nb employés | integer | — | always | min:0 | "Combien ?" | 20 | soft_constraint | public | COM-COMMON-043 | HIGH |

### Matrix 2.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BUR-S01 | étage | Étage | string | enum:rdc,1er,2ème,3ème+,s/sol | "Étage ?" | 22 | soft_constraint | COM-COMMON-036 | HIGH |
| BUR-S02 | accès_pmr | Accès PMR | boolean | — | "PMR ?" | 24 | soft_constraint | COM-COMMON-031 | HIGH |
| BUR-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel,pas | "Parking ?" | 26 | soft_constraint | COM-COMMON-014 | HIGH |
| BUR-S04 | électricité | Électricité | boolean | — | "Électricité ?" | 30 | soft_constraint | COM-COMMON-018 | HIGH |
| BUR-S05 | zone | Zone | string | enum:centre_affaires,commerciale,résidentiel,périphérie | "Zone ?" | 20 | soft_constraint | COM-COMMON-026 | HIGH |

### Matrix 2.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| BUR-M01 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| BUR-M02 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| BUR-M03 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| BUR-M04 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| BUR-M05 | employés | Capacité | integer | soft_constraint | COM-COMMON-043 | HIGH |
| BUR-M06 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |
| BUR-M07 | accès_pmr | PMR | boolean | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 2.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BUR-I01 | activité | Activité | string | "Type activité ?" | 85 | soft_constraint | 02B-Ch.3 | HIGH |
| BUR-I02 | besoins | Besoins | string | "Besoins spécifiques ?" | 86 | ranking_preference | 02B-Ch.3 | HIGH |
| BUR-I03 | emménagement | Date emménagement | date | "Date ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |

### Matrix 2.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUR-V01 | disponibilité | Disponibilité | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| BUR-V02 | accompagnement | Accompagnement | boolean | "Accompagné ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| BUR-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 2.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BUR-T01 | pièce_entreprise | Pièce entreprise | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| BUR-T02 | registre | Registre | string | — | "Registre ?" | 96 | qualification §11.6 | HIGH |
| BUR-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |
| BUR-T04 | conditions_bail | Conditions | string | — | "Conditions bail ?" | 98 | 02B-Ch.5 | HIGH |

### Matrix 2.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BUR-R01 | open_space | Open space | boolean | — | "Open space ?" | 35 | ranking_preference | 02B-Ch.3 | HIGH |
| BUR-R02 | bureaux_fermés | Bureaux fermés | integer | — | "Nb bureaux fermés ?" | 36 | ranking_preference | 02B-Ch.3 | HIGH |
| BUR-R03 | salle_réunion | Salle réunion | boolean | — | "Salle réunion ?" | 37 | ranking_preference | 02B-Ch.3 | HIGH |
| BUR-R04 | accueil | Espace accueil | boolean | — | "Accueil ?" | 38 | ranking_preference | 02B-Ch.3 | HIGH |
| BUR-R05 | climatisation | Clim | boolean | — | "Clim ?" | 40 | ranking_preference | COM-COMMON-032 | HIGH |
| BUR-R06 | internet | Internet | boolean | — | "Internet ?" | 41 | soft_constraint | 02B-Ch.3 | HIGH |
| BUR-R07 | sécurité | Sécurité | boolean | — | "Sécurité ?" | 43 | ranking_preference | 02B-Ch.3 | HIGH |
| BUR-R08 | ascenseur | Ascenseur | boolean | — | "Ascenseur ?" | 44 | soft_constraint | 02B-Ch.3 | HIGH |

### Matrix 2.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUR-O01 | détente | Espace détente | boolean | "Détente ?" | 50 | 02B-Ch.3 | HIGH |
| BUR-O02 | serveur | Salle serveur | boolean | "Serveur ?" | 51 | 02B-Ch.3 | HIGH |
| BUR-O03 | parking_visiteur | Parking visiteur | integer | "Places visiteur ?" | 52 | COM-COMMON-015 | HIGH |
| BUR-O04 | lumière | Éclairage naturel | boolean | "Lumière naturelle ?" | 53 | 02B-Ch.3 | HIGH |

### Matrix 2.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUR-C01 | sous-location | Sous-location | boolean | location | 60 | 02B-Ch.5 | HIGH |
| BUR-C02 | meublé | Meublé | boolean | location | 61 | 02B-Ch.5 | HIGH |
| BUR-C03 | charges | Charges incluses | boolean | location | 62 | 02B-Ch.5 | HIGH |
| BUR-C04 | copropriété | Copropriété | string | achat | 63 | 02B-Ch.5 | HIGH |

### Matrix 2.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| BUR-SN01 | CA_entreprise | CA entreprise | integer | sensitive | 02B-Ch.6 | HIGH |
| BUR-SN02 | effectif | Effectif exact | integer | semi_private | 02B-Ch.6 | HIGH |
| BUR-SN03 | bailleur | Identité bailleur | string | sensitive | anonymity | HIGH |

### Matrix 2.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| BUR-D01 | standing | Standing | string | zone+étage+état+prix | deduction_only | HIGH |
| BUR-D02 | densité | Densité employés | float | surface/employés | 02B-Ch.3 | HIGH |
| BUR-D03 | coût_total | Coût total | integer | loyer+charges | pricing_model | HIGH |

### Matrix 2.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| BUR-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| BUR-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| BUR-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |

---

## 3. local_commercial (Commercial Space)

### Matrix 3.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-003 |
| canonical_name | local_commercial |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY, BAIL_COMMERCIAL |
| property_or_service_type | local_commercial |
| requester_typology | professional, business, entrepreneur |
| journey_stage | SEARCH |
| description | Matrice de qualification pour local commercial générique. |

### Matrix 3.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LOC-01 | activité | Activité | string | — | always | min_len:3 | "Activité ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| LOC-02 | surface_min | Surface min | integer | — | always | min:5 | "Surface ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| LOC-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| LOC-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| LOC-05 | transaction | Transaction | string | enum:location,achat,bail | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| LOC-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |

### Matrix 3.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LOC-S01 | étage | Étage | string | enum:rdc,1er,2ème+,s/sol | "Étage ?" | 20 | soft_constraint | COM-COMMON-036 | HIGH |
| LOC-S02 | accès_véhicules | Accès véhicules | string | enum:pl,livraisons,utilitaire,voiture | "Accès ?" | 22 | soft_constraint | COM-COMMON-010 | HIGH |
| LOC-S03 | visibilité | Visibilité | boolean | — | "Visible route ?" | 24 | ranking_preference | COM-COMMON-011 | HIGH |
| LOC-S04 | zone | Zone | string | enum:centre_ville,commerciale,axe,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| LOC-S05 | hauteur | Hauteur | float | — | "Hauteur ?" | 26 | soft_constraint | COM-COMMON-009 | HIGH |

### Matrix 3.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| LOC-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| LOC-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| LOC-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| LOC-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| LOC-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| LOC-M06 | hauteur | Hauteur | float | soft_constraint | COM-COMMON-009 | HIGH |
| LOC-M07 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |

### Matrix 3.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LOC-I01 | description | Projet | string | "Projet ?" | 85 | soft_constraint | qualification §6 | HIGH |
| LOC-I02 | date | Démarrage | date | "Date ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| LOC-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 3.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LOC-V01 | date_visite | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| LOC-V02 | accompagnement | Accompagnement | boolean | "Accompagné ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| LOC-V03 | points | Points vérification | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 3.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LOC-T01 | pièce_id | Pièce identité | string | — | "Pièce ?" | 95 | qualification §11.6 | HIGH |
| LOC-T02 | registre | Registre | string | — | "Registre ?" | 96 | qualification §11.6 | HIGH |
| LOC-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 3.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LOC-R01 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| LOC-R02 | triphasé | Triphasé | boolean | — | "Triphasé ?" | 38 | soft_constraint | COM-COMMON-019 | HIGH |
| LOC-R03 | eau | Eau | boolean | — | "Eau ?" | 40 | soft_constraint | COM-COMMON-020 | HIGH |
| LOC-R04 | état | État | string | enum:neuf,bon,à_rénover | "État ?" | 42 | ranking_preference | COM-COMMON-033 | HIGH |
| LOC-R05 | clim | Climatisation | boolean | — | "Clim ?" | 44 | ranking_preference | COM-COMMON-032 | HIGH |
| LOC-R06 | stockage | Stockage | boolean | — | "Stockage ?" | 46 | ranking_preference | COM-COMMON-016 | HIGH |

### Matrix 3.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LOC-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| LOC-O02 | vitrine | Vitrine | boolean | "Vitrine ?" | 51 | 02B-Ch.3 | HIGH |
| LOC-O03 | mezzanine | Mezzanine | boolean | "Mezzanine ?" | 52 | 02B-Ch.3 | HIGH |
| LOC-O04 | 24h | Accès 24h | boolean | "Accès 24h ?" | 53 | 02B-Ch.3 | HIGH |
| LOC-O05 | jardin | Espace extérieur | boolean | "Extérieur ?" | 54 | 02B-Ch.3 | HIGH |

### Matrix 3.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LOC-C01 | licence | Licence | string | activité_sensible | 60 | COM-COMMON-021 | HIGH |
| LOC-C02 | fonds | Fonds commerce | integer | cession | 62 | COM-COMMON-024 | HIGH |
| LOC-C03 | bail | Bail existant | string | reprise | 63 | COM-COMMON-029 | HIGH |
| LOC-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 3.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| LOC-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| LOC-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| LOC-SN03 | conditions | Conditions négociées | string | sensitive | anonymity | HIGH |

### Matrix 3.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| LOC-D01 | potentiel | Potentiel | string | flux+visibilité+zone | deduction_only | HIGH |
| LOC-D02 | coût_mensuel | Coût mensuel | integer | loyer+charges ou budget/120 | pricing_model | HIGH |
| LOC-D03 | standing | Standing | string | zone+état+prix | deduction_only | HIGH |

### Matrix 3.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| LOC-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| LOC-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| LOC-F03 | "Douches ?" | Résidentiel | qualification §12.14 | HIGH |

---

## 4. magasin (Store)

### Matrix 4.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-004 |
| canonical_name | magasin |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY |
| property_or_service_type | magasin |
| requester_typology | professional, retailer |
| journey_stage | SEARCH |
| description | Matrice pour magasin / retail store. |

### Matrix 4.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAGA-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type de magasin ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| MAGA-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface magasin ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| MAGA-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| MAGA-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| MAGA-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| MAGA-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |

### Matrix 4.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAGA-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| MAGA-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| MAGA-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| MAGA-S04 | façade | Façade | float | — | "Façade ?" | 25 | ranking_preference | COM-COMMON-012 | HIGH |
| MAGA-S05 | flux | Flux | string | enum:très_élevé,élevé,moyen | "Flux ?" | 24 | ranking_preference | COM-COMMON-013 | HIGH |

### Matrix 4.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| MAGA-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| MAGA-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| MAGA-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| MAGA-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| MAGA-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| MAGA-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| MAGA-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 4.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAGA-I01 | projet | Description projet | string | "Décrivez votre projet de magasin." | 85 | soft_constraint | qualification §6 | HIGH |
| MAGA-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| MAGA-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 4.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MAGA-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| MAGA-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| MAGA-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 4.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAGA-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| MAGA-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| MAGA-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 4.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAGA-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| MAGA-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| MAGA-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| MAGA-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| MAGA-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| MAGA-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 4.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MAGA-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| MAGA-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| MAGA-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| MAGA-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 4.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MAGA-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| MAGA-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| MAGA-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| MAGA-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 4.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| MAGA-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| MAGA-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| MAGA-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 4.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| MAGA-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| MAGA-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| MAGA-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 4.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| MAGA-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| MAGA-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| MAGA-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| MAGA-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 5. entrepot (Warehouse)

### Matrix 5.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-005 |
| canonical_name | entrepot |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY, LEASE |
| property_or_service_type | entrepot |
| requester_typology | professional, logistician |
| journey_stage | SEARCH |
| description | Matrice pour entrepôt / warehouse. |

### Matrix 5.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ENTR-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type stockage ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| ENTR-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface entrepot ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| ENTR-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| ENTR-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| ENTR-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| ENTR-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| ENTR-07 | ent-07 | type_stockage | Type stockage | — | always | string | "min:3 ?" | Type stockage | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 5.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ENTR-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| ENTR-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| ENTR-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| ENTR-S04 | accès | Accès véhicules | string | enum:pl,livraisons,utilitaire,voiture | "Accès ?" | 25 | soft_constraint | COM-COMMON-010 | HIGH |
| ENTR-S05 | hauteur | Hauteur sous plafond | float | — | "Hauteur ?" | 30 | soft_constraint | COM-COMMON-009 | HIGH |

### Matrix 5.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| ENTR-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| ENTR-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| ENTR-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| ENTR-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| ENTR-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| ENTR-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| ENTR-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 5.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ENTR-I01 | projet | Description projet | string | "Décrivez votre projet de entrepot." | 85 | soft_constraint | qualification §6 | HIGH |
| ENTR-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| ENTR-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 5.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ENTR-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| ENTR-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| ENTR-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 5.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ENTR-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| ENTR-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| ENTR-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 5.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ENTR-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| ENTR-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| ENTR-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| ENTR-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| ENTR-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| ENTR-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 5.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ENTR-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| ENTR-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| ENTR-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| ENTR-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 5.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ENTR-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| ENTR-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| ENTR-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| ENTR-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 5.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| ENTR-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| ENTR-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| ENTR-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 5.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| ENTR-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| ENTR-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| ENTR-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 5.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| ENTR-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| ENTR-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| ENTR-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| ENTR-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 6. hangar (Shed)

### Matrix 6.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-006 |
| canonical_name | hangar |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY |
| property_or_service_type | hangar |
| requester_typology | professional, industrial |
| journey_stage | SEARCH |
| description | Matrice pour hangar / shed structure. |

### Matrix 6.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HANG-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type usage hangar ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| HANG-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface hangar ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| HANG-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| HANG-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| HANG-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| HANG-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| HANG-07 | han-07 | type_hangar | Type hangar | — | always | string | "min:3 ?" | Type hangar | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 6.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HANG-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| HANG-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| HANG-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| HANG-S04 | accès | Accès véhicules | string | enum:pl,livraisons,utilitaire,voiture | "Accès ?" | 25 | soft_constraint | COM-COMMON-010 | HIGH |
| HANG-S05 | hauteur | Hauteur sous plafond | float | — | "Hauteur ?" | 30 | soft_constraint | COM-COMMON-009 | HIGH |

### Matrix 6.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| HANG-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| HANG-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| HANG-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| HANG-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| HANG-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| HANG-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| HANG-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 6.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HANG-I01 | projet | Description projet | string | "Décrivez votre projet de hangar." | 85 | soft_constraint | qualification §6 | HIGH |
| HANG-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| HANG-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 6.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HANG-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| HANG-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| HANG-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 6.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HANG-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| HANG-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| HANG-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 6.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HANG-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| HANG-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| HANG-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| HANG-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| HANG-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| HANG-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 6.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HANG-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| HANG-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| HANG-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| HANG-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 6.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HANG-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| HANG-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| HANG-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| HANG-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 6.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| HANG-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| HANG-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| HANG-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 6.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| HANG-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| HANG-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| HANG-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 6.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| HANG-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| HANG-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| HANG-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| HANG-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 7. atelier (Workshop)

### Matrix 7.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-007 |
| canonical_name | atelier |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY |
| property_or_service_type | atelier |
| requester_typology | professional, artisan |
| journey_stage | SEARCH |
| description | Matrice pour atelier / workshop. |

### Matrix 7.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ATEL-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type atelier ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| ATEL-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface atelier ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| ATEL-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| ATEL-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| ATEL-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| ATEL-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| ATEL-07 | ate-07 | type_atelier | Type atelier | — | always | string | "min:3 ?" | Type atelier | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 7.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ATEL-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| ATEL-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| ATEL-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| ATEL-S04 | puissance | Puissance élec | integer | — | "Puissance (kVA) ?" | 28 | soft_constraint | COM-COMMON-019 | HIGH |
| ATEL-S05 | accès | Accès | string | enum:pl,utilitaire,voiture | "Accès ?" | 26 | soft_constraint | COM-COMMON-010 | HIGH |

### Matrix 7.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| ATEL-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| ATEL-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| ATEL-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| ATEL-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| ATEL-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| ATEL-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| ATEL-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 7.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ATEL-I01 | projet | Description projet | string | "Décrivez votre projet de atelier." | 85 | soft_constraint | qualification §6 | HIGH |
| ATEL-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| ATEL-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 7.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATEL-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| ATEL-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| ATEL-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 7.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ATEL-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| ATEL-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| ATEL-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 7.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ATEL-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| ATEL-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| ATEL-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| ATEL-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| ATEL-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| ATEL-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 7.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATEL-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| ATEL-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| ATEL-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| ATEL-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 7.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATEL-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| ATEL-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| ATEL-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| ATEL-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 7.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| ATEL-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| ATEL-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| ATEL-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 7.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| ATEL-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| ATEL-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| ATEL-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 7.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| ATEL-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| ATEL-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| ATEL-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| ATEL-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 8. restaurant

### Matrix 8.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-008 |
| canonical_name | restaurant |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY, CESSION |
| property_or_service_type | restaurant |
| requester_typology | professional, restaurateur |
| journey_stage | SEARCH |
| description | Matrice pour restaurant. |

### Matrix 8.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REST-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type cuisine ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| REST-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface restaurant ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| REST-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| REST-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| REST-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| REST-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| REST-07 | res-07 | type_cuisine | Type cuisine | — | always | string | "min:3 ?" | Type cuisine | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 8.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REST-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| REST-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| REST-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| REST-S04 | flux | Flux piéton | string | enum:très_élevé,élevé,moyen | "Flux ?" | 24 | ranking_preference | COM-COMMON-013 | HIGH |

### Matrix 8.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| REST-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| REST-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| REST-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| REST-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| REST-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| REST-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| REST-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 8.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REST-I01 | projet | Description projet | string | "Décrivez votre projet de restaurant." | 85 | soft_constraint | qualification §6 | HIGH |
| REST-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| REST-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 8.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REST-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| REST-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| REST-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 8.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REST-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| REST-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| REST-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 8.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REST-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| REST-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| REST-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| REST-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| REST-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| REST-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 8.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REST-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| REST-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| REST-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| REST-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 8.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REST-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| REST-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| REST-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| REST-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 8.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| REST-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| REST-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| REST-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 8.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| REST-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| REST-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| REST-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 8.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| REST-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| REST-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| REST-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| REST-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 9. bar

### Matrix 9.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-009 |
| canonical_name | bar |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY, CESSION |
| property_or_service_type | bar |
| requester_typology | professional, entrepreneur |
| journey_stage | SEARCH |
| description | Matrice pour bar / nightlife. |

### Matrix 9.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BAR-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type bar ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| BAR-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface bar ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| BAR-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| BAR-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| BAR-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| BAR-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| BAR-07 | bar-07 | type_bar | Type bar | — | always | string | "min:3 ?" | Type bar | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 9.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BAR-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| BAR-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| BAR-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| BAR-S04 | flux | Flux piéton | string | enum:très_élevé,élevé,moyen | "Flux ?" | 24 | ranking_preference | COM-COMMON-013 | HIGH |

### Matrix 9.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| BAR-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| BAR-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| BAR-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| BAR-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| BAR-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| BAR-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| BAR-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 9.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BAR-I01 | projet | Description projet | string | "Décrivez votre projet de bar." | 85 | soft_constraint | qualification §6 | HIGH |
| BAR-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| BAR-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 9.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BAR-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| BAR-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| BAR-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 9.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BAR-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| BAR-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| BAR-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 9.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BAR-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| BAR-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| BAR-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| BAR-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| BAR-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| BAR-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 9.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BAR-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| BAR-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| BAR-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| BAR-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 9.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BAR-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| BAR-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| BAR-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| BAR-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 9.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| BAR-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| BAR-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| BAR-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 9.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| BAR-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| BAR-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| BAR-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 9.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| BAR-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| BAR-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| BAR-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| BAR-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 10. hotel (Boutique Hotel)

### Matrix 10.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-010 |
| canonical_name | hotel |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY |
| property_or_service_type | hotel |
| requester_typology | professional, hotelier |
| journey_stage | SEARCH |
| description | Matrice pour hôtel / boutique hotel. |

### Matrix 10.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HOTE-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type hôtel ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| HOTE-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface hotel ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| HOTE-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| HOTE-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| HOTE-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| HOTE-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| HOTE-07 | hot-07 | catégorie | Catégorie | — | always | string | "enum:1*,2*,3*,4*,5* ?" | Catégorie | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 10.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HOTE-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| HOTE-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| HOTE-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| HOTE-S04 | étoiles | Catégorie | string | enum:1*,2*,3*,4*,5*,sans | "Catégorie ?" | 20 | soft_constraint | 02F-HOTEL-REF.md | HIGH |

### Matrix 10.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| HOTE-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| HOTE-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| HOTE-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| HOTE-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| HOTE-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| HOTE-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| HOTE-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 10.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HOTE-I01 | projet | Description projet | string | "Décrivez votre projet de hotel." | 85 | soft_constraint | qualification §6 | HIGH |
| HOTE-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| HOTE-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 10.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HOTE-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| HOTE-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| HOTE-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 10.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HOTE-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| HOTE-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| HOTE-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 10.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HOTE-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| HOTE-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| HOTE-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| HOTE-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| HOTE-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| HOTE-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 10.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HOTE-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| HOTE-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| HOTE-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| HOTE-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 10.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HOTE-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| HOTE-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| HOTE-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| HOTE-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 10.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| HOTE-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| HOTE-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| HOTE-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 10.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| HOTE-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| HOTE-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| HOTE-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 10.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| HOTE-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| HOTE-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| HOTE-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| HOTE-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 11. auberge (Inn)

### Matrix 11.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-011 |
| canonical_name | auberge |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY |
| property_or_service_type | auberge |
| requester_typology | professional, host |
| journey_stage | SEARCH |
| description | Matrice pour auberge / guesthouse. |

### Matrix 11.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUBE-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type auberge ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| AUBE-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface auberge ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| AUBE-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| AUBE-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| AUBE-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| AUBE-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| AUBE-07 | aub-07 | type_auberge | Type auberge | — | always | string | "min:3 ?" | Type auberge | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 11.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUBE-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| AUBE-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| AUBE-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| AUBE-S04 | étoiles | Catégorie | string | enum:1*,2*,3*,4*,5*,sans | "Catégorie ?" | 20 | soft_constraint | 02F-HOTEL-REF.md | HIGH |

### Matrix 11.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| AUBE-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| AUBE-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| AUBE-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| AUBE-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| AUBE-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| AUBE-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| AUBE-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 11.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUBE-I01 | projet | Description projet | string | "Décrivez votre projet de auberge." | 85 | soft_constraint | qualification §6 | HIGH |
| AUBE-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| AUBE-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 11.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AUBE-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| AUBE-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| AUBE-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 11.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUBE-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| AUBE-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| AUBE-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 11.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AUBE-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| AUBE-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| AUBE-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| AUBE-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| AUBE-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| AUBE-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 11.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AUBE-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| AUBE-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| AUBE-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| AUBE-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 11.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AUBE-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| AUBE-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| AUBE-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| AUBE-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 11.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| AUBE-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| AUBE-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| AUBE-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 11.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| AUBE-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| AUBE-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| AUBE-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 11.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| AUBE-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| AUBE-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| AUBE-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| AUBE-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 12. immeuble_de_rapport (Income Property)

### Matrix 12.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-012 |
| canonical_name | immeuble_de_rapport |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | BUY, INVEST |
| property_or_service_type | immeuble_de_rapport |
| requester_typology | professional, investor |
| journey_stage | SEARCH |
| description | Matrice pour immeuble de rapport / income property. |

### Matrix 12.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type immeuble ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| IMME-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface immeuble_de_rapport ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| IMME-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| IMME-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| IMME-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| IMME-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| IMME-07 | imr-07 | nb_unités | Nb unités | — | always | integer | "min:2 ?" | Nb unités | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 12.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| IMME-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| IMME-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| IMME-S04 | accès | Accès | string | enum:pl,utilitaire,voiture | "Accès ?" | 25 | soft_constraint | COM-COMMON-010 | HIGH |

### Matrix 12.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| IMME-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| IMME-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| IMME-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| IMME-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| IMME-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| IMME-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| IMME-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 12.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-I01 | projet | Description projet | string | "Décrivez votre projet de immeuble_de_rapport." | 85 | soft_constraint | qualification §6 | HIGH |
| IMME-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| IMME-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 12.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| IMME-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| IMME-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 12.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| IMME-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| IMME-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 12.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| IMME-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| IMME-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| IMME-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| IMME-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| IMME-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 12.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| IMME-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| IMME-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| IMME-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 12.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| IMME-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| IMME-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| IMME-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 12.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| IMME-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| IMME-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| IMME-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 12.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| IMME-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| IMME-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| IMME-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 12.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| IMME-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| IMME-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| IMME-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| IMME-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 13. immeuble_commercial (Commercial Building)

### Matrix 13.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-013 |
| canonical_name | immeuble_commercial |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | BUY, INVEST |
| property_or_service_type | immeuble_commercial |
| requester_typology | professional, investor |
| journey_stage | SEARCH |
| description | Matrice pour immeuble commercial. |

### Matrix 13.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type immeuble ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| IMME-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface immeuble_commercial ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| IMME-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| IMME-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| IMME-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| IMME-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| IMME-07 | imc-07 | nb_commerces | Nb commerces | — | always | integer | "min:2 ?" | Nb commerces | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 13.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| IMME-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| IMME-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| IMME-S04 | accès | Accès | string | enum:pl,utilitaire,voiture | "Accès ?" | 25 | soft_constraint | COM-COMMON-010 | HIGH |

### Matrix 13.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| IMME-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| IMME-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| IMME-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| IMME-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| IMME-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| IMME-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| IMME-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 13.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-I01 | projet | Description projet | string | "Décrivez votre projet de immeuble_commercial." | 85 | soft_constraint | qualification §6 | HIGH |
| IMME-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| IMME-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 13.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| IMME-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| IMME-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 13.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| IMME-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| IMME-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 13.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| IMME-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| IMME-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| IMME-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| IMME-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| IMME-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 13.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| IMME-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| IMME-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| IMME-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 13.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IMME-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| IMME-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| IMME-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| IMME-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 13.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| IMME-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| IMME-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| IMME-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 13.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| IMME-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| IMME-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| IMME-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 13.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| IMME-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| IMME-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| IMME-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| IMME-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 14. station_service (Gas Station)

### Matrix 14.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-014 |
| canonical_name | station_service |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | BUY, RENT |
| property_or_service_type | station_service |
| requester_typology | professional, oil_company |
| journey_stage | SEARCH |
| description | Matrice pour station-service. |

### Matrix 14.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STAT-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type station ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| STAT-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface station_service ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| STAT-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| STAT-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| STAT-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| STAT-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| STAT-07 | sta-07 | type_station | Type station | — | always | string | "min:3 ?" | Type station | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 14.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STAT-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| STAT-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| STAT-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| STAT-S04 | accès | Accès | string | enum:pl,utilitaire,voiture | "Accès ?" | 25 | soft_constraint | COM-COMMON-010 | HIGH |

### Matrix 14.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| STAT-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| STAT-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| STAT-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| STAT-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| STAT-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| STAT-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| STAT-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 14.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STAT-I01 | projet | Description projet | string | "Décrivez votre projet de station_service." | 85 | soft_constraint | qualification §6 | HIGH |
| STAT-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| STAT-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 14.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STAT-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| STAT-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| STAT-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 14.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STAT-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| STAT-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| STAT-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 14.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STAT-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| STAT-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| STAT-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| STAT-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| STAT-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| STAT-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 14.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STAT-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| STAT-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| STAT-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| STAT-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 14.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STAT-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| STAT-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| STAT-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| STAT-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 14.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| STAT-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| STAT-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| STAT-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 14.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| STAT-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| STAT-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| STAT-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 14.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| STAT-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| STAT-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| STAT-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| STAT-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 15. site_industriel (Industrial Site)

### Matrix 15.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-015 |
| canonical_name | site_industriel |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | BUY, RENT, LEASE |
| property_or_service_type | site_industriel |
| requester_typology | professional, industrial |
| journey_stage | SEARCH |
| description | Matrice pour site industriel. |

### Matrix 15.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SITE-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type industrie ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| SITE-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface site_industriel ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| SITE-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| SITE-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| SITE-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| SITE-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| SITE-07 | sit-07 | type_industrie | Type industrie | — | always | string | "min:3 ?" | Type industrie | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 15.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SITE-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| SITE-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| SITE-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| SITE-S04 | accès | Accès véhicules | string | enum:pl,livraisons,utilitaire,voiture | "Accès ?" | 25 | soft_constraint | COM-COMMON-010 | HIGH |
| SITE-S05 | hauteur | Hauteur sous plafond | float | — | "Hauteur ?" | 30 | soft_constraint | COM-COMMON-009 | HIGH |

### Matrix 15.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| SITE-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| SITE-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| SITE-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| SITE-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| SITE-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| SITE-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| SITE-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 15.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SITE-I01 | projet | Description projet | string | "Décrivez votre projet de site_industriel." | 85 | soft_constraint | qualification §6 | HIGH |
| SITE-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| SITE-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 15.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SITE-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| SITE-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| SITE-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 15.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SITE-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| SITE-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| SITE-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 15.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SITE-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| SITE-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| SITE-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| SITE-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| SITE-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| SITE-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 15.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SITE-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| SITE-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| SITE-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| SITE-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 15.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SITE-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| SITE-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| SITE-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| SITE-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 15.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| SITE-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| SITE-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| SITE-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 15.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| SITE-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| SITE-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| SITE-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 15.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| SITE-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| SITE-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| SITE-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| SITE-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 16. espace_evenementiel (Event Space)

### Matrix 16.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | COM-MATRIX-016 |
| canonical_name | espace_evenementiel |
| request_family | COMMERCIAL_SEARCH |
| transaction_type | RENT, BUY |
| property_or_service_type | espace_evenementiel |
| requester_typology | professional, event_organizer |
| journey_stage | SEARCH |
| description | Matrice pour espace événementiel. |

### Matrix 16.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESPA-01 | activité_prévue | Activité prévue | string | — | always | min_len:3 | "Type type événement ?" | 10 | hard_constraint | public | COM-COMMON-001 | HIGH |
| ESPA-02 | surface_min | Surface min (m²) | integer | — | always | min:5 | "Surface espace_evenementiel ?" | 15 | hard_constraint | public | COM-COMMON-003 | HIGH |
| ESPA-03 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | COM-COMMON-005 | HIGH |
| ESPA-04 | quartier | Quartier | string | — | always | in:neighborhoods | "Quartier ?" | 8 | hard_constraint | public | COM-COMMON-006 | HIGH |
| ESPA-05 | transaction | Transaction | string | enum:location,achat,cession | always | in:types | "Transaction ?" | 3 | hard_constraint | public | COM-COMMON-034 | HIGH |
| ESPA-06 | budget | Budget | integer | — | always | min:10000 | "Budget ?" | 12 | hard_constraint | public | COM-COMMON-007/008 | HIGH |
| ESPA-07 | esp-07 | type_espace | Type événement | — | always | string | "enum:mariage,conférence,concert,réception ?" | Type espace | soft_constraint | public | COM-COMMON-009 | HIGH |

### Matrix 16.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESPA-S01 | visibilité | Visibilité route | boolean | — | "Visible route ?" | 22 | ranking_preference | COM-COMMON-011 | HIGH |
| ESPA-S02 | zone | Zone commerciale | string | enum:centre_ville,axe,zone,quartier | "Zone ?" | 18 | soft_constraint | COM-COMMON-026 | HIGH |
| ESPA-S03 | parking | Parking | string | enum:indispensable,souhaité,optionnel | "Parking ?" | 35 | soft_constraint | COM-COMMON-014 | HIGH |
| ESPA-S04 | accès | Accès | string | enum:pl,utilitaire,voiture | "Accès ?" | 25 | soft_constraint | COM-COMMON-010 | HIGH |

### Matrix 16.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| ESPA-M01 | activité | Activité | string | hard_constraint | COM-COMMON-001 | HIGH |
| ESPA-M02 | surface | Surface | integer | hard_constraint | COM-COMMON-003 | HIGH |
| ESPA-M03 | budget | Budget | integer | hard_constraint | matching_model §2 | HIGH |
| ESPA-M04 | ville | Ville | string | hard_constraint | matching_model §1 | HIGH |
| ESPA-M05 | quartier | Quartier | string | hard_constraint | matching_model §1 | HIGH |
| ESPA-M06 | visibilité | Visibilité | boolean | ranking_preference | matching_model §22 | HIGH |
| ESPA-M07 | parking | Parking | string | soft_constraint | COM-COMMON-014 | HIGH |

### Matrix 16.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESPA-I01 | projet | Description projet | string | "Décrivez votre projet de espace_evenementiel." | 85 | soft_constraint | qualification §6 | HIGH |
| ESPA-I02 | date | Date ouverture | date | "Date ouverture ?" | 87 | soft_constraint | COM-COMMON-044 | HIGH |
| ESPA-I03 | expérience | Expérience | string | "Expérience secteur ?" | 86 | ranking_preference | qualification §6 | HIGH |

### Matrix 16.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ESPA-V01 | disponibilité | Date visite | date | "Quand visiter ?" | 90 | qualification §6 | HIGH |
| ESPA-V02 | accompagnement | Accompagné | boolean | "Visite accompagnée ?" | 91 | domain_model GOLD-DM-066 | HIGH |
| ESPA-V03 | vérifications | Vérifications | string | "Points à vérifier ?" | 92 | 02B-Ch.3 | HIGH |

### Matrix 16.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESPA-T01 | pièce_id | Pièce identité | string | — | "Pièce identité ?" | 95 | qualification §11.6 | HIGH |
| ESPA-T02 | registre | Registre commerce | string | — | "Registre commerce ?" | 96 | qualification §11.6 | HIGH |
| ESPA-T03 | garantie | Garantie | string | enum:caution,dépôt,garant | "Garantie ?" | 97 | domain_model §9 | HIGH |

### Matrix 16.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESPA-R01 | électricité | Électricité | boolean | — | "Électricité ?" | 42 | soft_constraint | COM-COMMON-018 | HIGH |
| ESPA-R02 | eau | Eau | boolean | — | "Eau ?" | 44 | soft_constraint | COM-COMMON-020 | HIGH |
| ESPA-R03 | climatisation | Clim | boolean | — | "Clim ?" | 46 | ranking_preference | COM-COMMON-032 | HIGH |
| ESPA-R04 | état | État local | string | enum:neuf,bon,à_rénover | "État ?" | 48 | ranking_preference | COM-COMMON-033 | HIGH |
| ESPA-R05 | stockage | Stockage | boolean | — | "Stockage ?" | 40 | ranking_preference | COM-COMMON-016 | HIGH |
| ESPA-R06 | accès_pmr | PMR | boolean | — | "PMR ?" | 45 | soft_constraint | COM-COMMON-031 | HIGH |

### Matrix 16.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ESPA-O01 | entrée | Entrée indépendante | boolean | "Entrée indép ?" | 50 | 02B-Ch.3 | HIGH |
| ESPA-O02 | enseigne | Enseigne | boolean | "Enseigne ?" | 51 | 02B-Ch.3 | HIGH |
| ESPA-O03 | délai | Délai | string | "Délai ?" | 53 | COM-COMMON-038 | HIGH |
| ESPA-O04 | horaires | Horaires | string | "Horaires ?" | 55 | COM-COMMON-045 | HIGH |

### Matrix 16.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ESPA-C01 | fonds | Fonds commerce | integer | cession | 60 | COM-COMMON-024 | HIGH |
| ESPA-C02 | CA | Chiffre affaires | integer | fonds | 61 | COM-COMMON-025 | HIGH |
| ESPA-C03 | licence | Licence | string | activité_sensible | 50 | COM-COMMON-021 | HIGH |
| ESPA-C04 | dépôt | Dépôt garantie | integer | location | 64 | COM-COMMON-030 | HIGH |

### Matrix 16.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| ESPA-SN01 | CA_prévisionnel | CA prévisionnel | integer | sensitive | 02B-Ch.6 | HIGH |
| ESPA-SN02 | propriétaire | Propriétaire | string | sensitive | anonymity | HIGH |
| ESPA-SN03 | conditions | Conditions | string | sensitive | anonymity | HIGH |

### Matrix 16.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| ESPA-D01 | standing | Standing | string | zone+état+visibilité+prix | deduction_only | HIGH |
| ESPA-D02 | potentiel | Potentiel | float | flux*0.4+visibilité*0.3+zone*0.3 | matching_model §6 | HIGH |
| ESPA-D03 | coût_mensuel | Coût mensuel | integer | loyer ou budget/120 | pricing_model | HIGH |

### Matrix 16.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| ESPA-F01 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |
| ESPA-F02 | "Habiter ?" | Résidentiel | qualification §12.14 | HIGH |
| ESPA-F03 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| ESPA-F04 | "Revenu ?" | Personnel | Directive Art.14 | HIGH |

---

## 17. investissement_locatif (Rental Investment)

### Matrix 17.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | INV-MATRIX-001 |
| canonical_name | investissement_locatif |
| request_family | INVESTMENT_SEARCH |
| transaction_type | INVEST |
| property_or_service_type | investissement_locatif |
| requester_typology | investor, diaspora_investor |
| journey_stage | SEARCH |
| description | Matrice pour investissement locatif / rental investment property. |

### Matrix 17.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-01 | budget_inv | Budget investissement | integer | — | always | min:100000 | "Budget total ?" | 10 | hard_constraint | private | INV-COMMON-001 | HIGH |
| INVE-02 | rendement | Rendement cible (%) | float | — | always | min:0 | "Rendement visé ?" | 15 | hard_constraint | private | INV-COMMON-002 | HIGH |
| INVE-03 | horizon | Horizon | string | enum:court,moyen,long,très_long | always | — | "Horizon ?" | 20 | soft_constraint | private | INV-COMMON-003 | HIGH |
| INVE-04 | risque | Risque accepté | string | enum:très_faible,faible,moyen,élevé | always | — | "Risque ?" | 25 | soft_constraint | private | INV-COMMON-004 | HIGH |
| INVE-05 | stratégie | Stratégie | string | enum:plus-value,locatif,mixte,développement | always | — | "Stratégie ?" | 22 | soft_constraint | private | INV-COMMON-005 | HIGH |
| INVE-06 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | INV-COMMON-006 | HIGH |
| INL-07 | type_bien_cible | Type bien cible | string | enum:appartement,maison,studio,bureau,commercial | always | — | "Type bien cible ?" | 12 | soft_constraint | private | investor_matrices | HIGH |
| INL-08 | nb_logements | Nb logements visé | integer | — | general | min:1 | "Combien de logements ?" | 14 | ranking_preference | private | investor_matrices | HIGH |

### Matrix 17.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-S01 | zone | Zone préférée | string | — | "Zone ?" | 8 | soft_constraint | INV-COMMON-007 | HIGH |
| INVE-S02 | expérience | Expérience | string | enum:débutant,intermédiaire,avancé,pro | "Expérience ?" | 30 | soft_constraint | INV-COMMON-008 | HIGH |
| INVE-S03 | financement | Financement | string | enum:fonds_propres,crédit,partenariat | "Source financement ?" | 35 | soft_constraint | INV-COMMON-009 | HIGH |

### Matrix 17.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-M01 | rendement | Rendement | float | hard_constraint | INV-COMMON-002 | HIGH |
| INVE-M02 | budget | Budget | integer | hard_constraint | INV-COMMON-001 | HIGH |
| INVE-M03 | horizon | Horizon | string | soft_constraint | INV-COMMON-003 | HIGH |
| INVE-M04 | risque | Risque | string | soft_constraint | INV-COMMON-004 | HIGH |
| INVE-M05 | ville | Ville | string | hard_constraint | INV-COMMON-006 | HIGH |
| INVE-M06 | stratégie | Stratégie | string | soft_constraint | INV-COMMON-005 | HIGH |

### Matrix 17.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-I01 | profil | Description profil | string | "Parlez de votre profil d'investisseur." | 85 | soft_constraint | investor_matrices | HIGH |
| INVE-I02 | autres_inv | Autres investissements | string | "Autres investissements ?" | 86 | ranking_preference | INV-COMMON-010 | HIGH |
| INVE-I03 | accompagnement | Accompagnement | boolean | "Accompagnement ?" | 87 | soft_constraint | INV-COMMON-011 | HIGH |

### Matrix 17.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-V01 | proche | Proche sur place | boolean | "Proche sur place pour visiter ?" | 90 | soft_constraint | INV-COMMON-016 | HIGH |
| INVE-V02 | estimation | Estimation humaine | boolean | "Estimation humaine ?" | 91 | soft_constraint | INV-COMMON-017 | HIGH |
| INVE-V03 | documents | Documents souhaités | string | "Documents complémentaires ?" | 92 | soft_constraint | INV-COMMON-018 | HIGH |

### Matrix 17.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-T01 | nom | Nom | string | "Nom ?" | 95 | soft_constraint | INV-COMMON-012 | HIGH |
| INVE-T02 | téléphone | Téléphone | string | "Téléphone ?" | 96 | soft_constraint | INV-COMMON-013 | HIGH |
| INVE-T03 | email | Email | string | "Email ?" | 97 | soft_constraint | INV-COMMON-014 | HIGH |

### Matrix 17.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-R01 | diaspora | Diaspora | boolean | "Diaspora ?" | 40 | ranking_preference | INV-COMMON-015 | HIGH |
| INVE-R02 | type_bien_préféré | Type bien préféré | string | "Type bien cible ?" | 42 | ranking_preference | investor_matrices | HIGH |
| INVE-R03 | capital | Capital disponible total | integer | "Capital total ?" | 44 | soft_constraint | investor_matrices | HIGH |
| INVE-R04 | exit | Stratégie sortie | string | ","Stratégie sortie ?" | 46 | ranking_preference | investor_matrices | HIGH |

### Matrix 17.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-O01 | délai_investissement | Délai investissement | string | "Délai pour investir ?" | 50 | investor_matrices | HIGH |
| INVE-O02 | partenaires | Partenaires | string | "Partenaires ?" | 52 | investor_matrices | HIGH |
| INVE-O03 | conseil | Besoin conseil | boolean | "Besoin conseil ?" | 54 | investor_matrices | HIGH |

### Matrix 17.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-C01 | mandat | Mandat recherche | boolean | besoin_accompagnement | 60 | investor_matrices | HIGH |
| INVE-C02 | budget_par_bien | Budget par bien | integer | stratégie=mixte | 62 | investor_matrices | HIGH |
| INVE-C03 | pays_résidence | Pays résidence | string | diaspora | 64 | investor_matrices | HIGH |

### Matrix 17.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-SN01 | patrimoine | Patrimoine total | integer | sensitive | investor_matrices | HIGH |
| INVE-SN02 | revenus | Revenus annuels | integer | sensitive | investor_matrices | HIGH |
| INVE-SN03 | identité | Identité exacte | string | sensitive | anonymity | HIGH |

### Matrix 17.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-D01 | profil_risque | Profil risque | string | rendement+horizon+risque | matching_model | HIGH |
| INVE-D02 | capacité_invest | Capacité investissement | integer | budget_inv - autres_engagements | pricing_model | HIGH |
| INVE-D03 | classe_investisseur | Classe investisseur | string | budget+expérience+stratégie | investor_matrices | HIGH |

### Matrix 17.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| INVE-F01 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| INVE-F02 | "Nationalité ?" | Discrimination potentielle | Directive Art.14 | HIGH |
| INVE-F03 | "Situation familiale ?" | Irrelevant | Directive Art.14 | HIGH |
| INVE-F04 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |

---

## 18. investissement_terrain (Land Investment)

### Matrix 18.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | INV-MATRIX-002 |
| canonical_name | investissement_terrain |
| request_family | INVESTMENT_SEARCH |
| transaction_type | INVEST |
| property_or_service_type | investissement_terrain |
| requester_typology | investor, diaspora_investor |
| journey_stage | SEARCH |
| description | Matrice pour investissement foncier / land investment. |

### Matrix 18.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-01 | budget_inv | Budget investissement | integer | — | always | min:100000 | "Budget total ?" | 10 | hard_constraint | private | INV-COMMON-001 | HIGH |
| INVE-02 | rendement | Rendement cible (%) | float | — | always | min:0 | "Rendement visé ?" | 15 | hard_constraint | private | INV-COMMON-002 | HIGH |
| INVE-03 | horizon | Horizon | string | enum:court,moyen,long,très_long | always | — | "Horizon ?" | 20 | soft_constraint | private | INV-COMMON-003 | HIGH |
| INVE-04 | risque | Risque accepté | string | enum:très_faible,faible,moyen,élevé | always | — | "Risque ?" | 25 | soft_constraint | private | INV-COMMON-004 | HIGH |
| INVE-05 | stratégie | Stratégie | string | enum:plus-value,locatif,mixte,développement | always | — | "Stratégie ?" | 22 | soft_constraint | private | INV-COMMON-005 | HIGH |
| INVE-06 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | INV-COMMON-006 | HIGH |
| INT-07 | surface_terrain | Surface terrain (m²) | integer | — | always | min:100 | "Surface terrain ?" | 12 | hard_constraint | private | investor_matrices | HIGH |
| INT-08 | usage_visé | Usage visé | string | enum:constructible,agricole,réserve_foncière,commercial | always | — | "Usage visé ?" | 14 | soft_constraint | private | investor_matrices | HIGH |
| INT-09 | plus_value_horizon | Horizon plus-value | string | enum:court,moyen,long | general | — | "Horizon plus-value ?" | 16 | ranking_preference | private | investor_matrices | HIGH |

### Matrix 18.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-S01 | zone | Zone préférée | string | — | "Zone ?" | 8 | soft_constraint | INV-COMMON-007 | HIGH |
| INVE-S02 | expérience | Expérience | string | enum:débutant,intermédiaire,avancé,pro | "Expérience ?" | 30 | soft_constraint | INV-COMMON-008 | HIGH |
| INVE-S03 | financement | Financement | string | enum:fonds_propres,crédit,partenariat | "Source financement ?" | 35 | soft_constraint | INV-COMMON-009 | HIGH |

### Matrix 18.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-M01 | rendement | Rendement | float | hard_constraint | INV-COMMON-002 | HIGH |
| INVE-M02 | budget | Budget | integer | hard_constraint | INV-COMMON-001 | HIGH |
| INVE-M03 | horizon | Horizon | string | soft_constraint | INV-COMMON-003 | HIGH |
| INVE-M04 | risque | Risque | string | soft_constraint | INV-COMMON-004 | HIGH |
| INVE-M05 | ville | Ville | string | hard_constraint | INV-COMMON-006 | HIGH |
| INVE-M06 | stratégie | Stratégie | string | soft_constraint | INV-COMMON-005 | HIGH |

### Matrix 18.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-I01 | profil | Description profil | string | "Parlez de votre profil d'investisseur." | 85 | soft_constraint | investor_matrices | HIGH |
| INVE-I02 | autres_inv | Autres investissements | string | "Autres investissements ?" | 86 | ranking_preference | INV-COMMON-010 | HIGH |
| INVE-I03 | accompagnement | Accompagnement | boolean | "Accompagnement ?" | 87 | soft_constraint | INV-COMMON-011 | HIGH |

### Matrix 18.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-V01 | proche | Proche sur place | boolean | "Proche sur place pour visiter ?" | 90 | soft_constraint | INV-COMMON-016 | HIGH |
| INVE-V02 | estimation | Estimation humaine | boolean | "Estimation humaine ?" | 91 | soft_constraint | INV-COMMON-017 | HIGH |
| INVE-V03 | documents | Documents souhaités | string | "Documents complémentaires ?" | 92 | soft_constraint | INV-COMMON-018 | HIGH |

### Matrix 18.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-T01 | nom | Nom | string | "Nom ?" | 95 | soft_constraint | INV-COMMON-012 | HIGH |
| INVE-T02 | téléphone | Téléphone | string | "Téléphone ?" | 96 | soft_constraint | INV-COMMON-013 | HIGH |
| INVE-T03 | email | Email | string | "Email ?" | 97 | soft_constraint | INV-COMMON-014 | HIGH |

### Matrix 18.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-R01 | diaspora | Diaspora | boolean | "Diaspora ?" | 40 | ranking_preference | INV-COMMON-015 | HIGH |
| INVE-R02 | type_bien_préféré | Type bien préféré | string | "Type bien cible ?" | 42 | ranking_preference | investor_matrices | HIGH |
| INVE-R03 | capital | Capital disponible total | integer | "Capital total ?" | 44 | soft_constraint | investor_matrices | HIGH |
| INVE-R04 | exit | Stratégie sortie | string | ","Stratégie sortie ?" | 46 | ranking_preference | investor_matrices | HIGH |

### Matrix 18.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-O01 | délai_investissement | Délai investissement | string | "Délai pour investir ?" | 50 | investor_matrices | HIGH |
| INVE-O02 | partenaires | Partenaires | string | "Partenaires ?" | 52 | investor_matrices | HIGH |
| INVE-O03 | conseil | Besoin conseil | boolean | "Besoin conseil ?" | 54 | investor_matrices | HIGH |

### Matrix 18.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-C01 | mandat | Mandat recherche | boolean | besoin_accompagnement | 60 | investor_matrices | HIGH |
| INVE-C02 | budget_par_bien | Budget par bien | integer | stratégie=mixte | 62 | investor_matrices | HIGH |
| INVE-C03 | pays_résidence | Pays résidence | string | diaspora | 64 | investor_matrices | HIGH |

### Matrix 18.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-SN01 | patrimoine | Patrimoine total | integer | sensitive | investor_matrices | HIGH |
| INVE-SN02 | revenus | Revenus annuels | integer | sensitive | investor_matrices | HIGH |
| INVE-SN03 | identité | Identité exacte | string | sensitive | anonymity | HIGH |

### Matrix 18.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-D01 | profil_risque | Profil risque | string | rendement+horizon+risque | matching_model | HIGH |
| INVE-D02 | capacité_invest | Capacité investissement | integer | budget_inv - autres_engagements | pricing_model | HIGH |
| INVE-D03 | classe_investisseur | Classe investisseur | string | budget+expérience+stratégie | investor_matrices | HIGH |

### Matrix 18.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| INVE-F01 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| INVE-F02 | "Nationalité ?" | Discrimination potentielle | Directive Art.14 | HIGH |
| INVE-F03 | "Situation familiale ?" | Irrelevant | Directive Art.14 | HIGH |
| INVE-F04 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |

---

## 19. investissement_immobilier_commercial (Commercial RE Investment)

### Matrix 19.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | INV-MATRIX-003 |
| canonical_name | investissement_immobilier_commercial |
| request_family | INVESTMENT_SEARCH |
| transaction_type | INVEST |
| property_or_service_type | investissement_immobilier_commercial |
| requester_typology | investor, professional |
| journey_stage | SEARCH |
| description | Matrice pour investissement immobilier commercial. |

### Matrix 19.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-01 | budget_inv | Budget investissement | integer | — | always | min:100000 | "Budget total ?" | 10 | hard_constraint | private | INV-COMMON-001 | HIGH |
| INVE-02 | rendement | Rendement cible (%) | float | — | always | min:0 | "Rendement visé ?" | 15 | hard_constraint | private | INV-COMMON-002 | HIGH |
| INVE-03 | horizon | Horizon | string | enum:court,moyen,long,très_long | always | — | "Horizon ?" | 20 | soft_constraint | private | INV-COMMON-003 | HIGH |
| INVE-04 | risque | Risque accepté | string | enum:très_faible,faible,moyen,élevé | always | — | "Risque ?" | 25 | soft_constraint | private | INV-COMMON-004 | HIGH |
| INVE-05 | stratégie | Stratégie | string | enum:plus-value,locatif,mixte,développement | always | — | "Stratégie ?" | 22 | soft_constraint | private | INV-COMMON-005 | HIGH |
| INVE-06 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | INV-COMMON-006 | HIGH |
| IIC-07 | type_commercial | Type commercial cible | string | enum:boutique,bureau,local,immeuble,magasin | always | — | "Type commercial cible ?" | 12 | soft_constraint | private | investor_matrices | HIGH |
| IIC-08 | rendement_min | Rendement minimum (%) | float | — | always | min:0 | "Rendement min ?" | 14 | hard_constraint | private | investor_matrices | HIGH |

### Matrix 19.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-S01 | zone | Zone préférée | string | — | "Zone ?" | 8 | soft_constraint | INV-COMMON-007 | HIGH |
| INVE-S02 | expérience | Expérience | string | enum:débutant,intermédiaire,avancé,pro | "Expérience ?" | 30 | soft_constraint | INV-COMMON-008 | HIGH |
| INVE-S03 | financement | Financement | string | enum:fonds_propres,crédit,partenariat | "Source financement ?" | 35 | soft_constraint | INV-COMMON-009 | HIGH |

### Matrix 19.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-M01 | rendement | Rendement | float | hard_constraint | INV-COMMON-002 | HIGH |
| INVE-M02 | budget | Budget | integer | hard_constraint | INV-COMMON-001 | HIGH |
| INVE-M03 | horizon | Horizon | string | soft_constraint | INV-COMMON-003 | HIGH |
| INVE-M04 | risque | Risque | string | soft_constraint | INV-COMMON-004 | HIGH |
| INVE-M05 | ville | Ville | string | hard_constraint | INV-COMMON-006 | HIGH |
| INVE-M06 | stratégie | Stratégie | string | soft_constraint | INV-COMMON-005 | HIGH |

### Matrix 19.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-I01 | profil | Description profil | string | "Parlez de votre profil d'investisseur." | 85 | soft_constraint | investor_matrices | HIGH |
| INVE-I02 | autres_inv | Autres investissements | string | "Autres investissements ?" | 86 | ranking_preference | INV-COMMON-010 | HIGH |
| INVE-I03 | accompagnement | Accompagnement | boolean | "Accompagnement ?" | 87 | soft_constraint | INV-COMMON-011 | HIGH |

### Matrix 19.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-V01 | proche | Proche sur place | boolean | "Proche sur place pour visiter ?" | 90 | soft_constraint | INV-COMMON-016 | HIGH |
| INVE-V02 | estimation | Estimation humaine | boolean | "Estimation humaine ?" | 91 | soft_constraint | INV-COMMON-017 | HIGH |
| INVE-V03 | documents | Documents souhaités | string | "Documents complémentaires ?" | 92 | soft_constraint | INV-COMMON-018 | HIGH |

### Matrix 19.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-T01 | nom | Nom | string | "Nom ?" | 95 | soft_constraint | INV-COMMON-012 | HIGH |
| INVE-T02 | téléphone | Téléphone | string | "Téléphone ?" | 96 | soft_constraint | INV-COMMON-013 | HIGH |
| INVE-T03 | email | Email | string | "Email ?" | 97 | soft_constraint | INV-COMMON-014 | HIGH |

### Matrix 19.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-R01 | diaspora | Diaspora | boolean | "Diaspora ?" | 40 | ranking_preference | INV-COMMON-015 | HIGH |
| INVE-R02 | type_bien_préféré | Type bien préféré | string | "Type bien cible ?" | 42 | ranking_preference | investor_matrices | HIGH |
| INVE-R03 | capital | Capital disponible total | integer | "Capital total ?" | 44 | soft_constraint | investor_matrices | HIGH |
| INVE-R04 | exit | Stratégie sortie | string | ","Stratégie sortie ?" | 46 | ranking_preference | investor_matrices | HIGH |

### Matrix 19.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-O01 | délai_investissement | Délai investissement | string | "Délai pour investir ?" | 50 | investor_matrices | HIGH |
| INVE-O02 | partenaires | Partenaires | string | "Partenaires ?" | 52 | investor_matrices | HIGH |
| INVE-O03 | conseil | Besoin conseil | boolean | "Besoin conseil ?" | 54 | investor_matrices | HIGH |

### Matrix 19.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-C01 | mandat | Mandat recherche | boolean | besoin_accompagnement | 60 | investor_matrices | HIGH |
| INVE-C02 | budget_par_bien | Budget par bien | integer | stratégie=mixte | 62 | investor_matrices | HIGH |
| INVE-C03 | pays_résidence | Pays résidence | string | diaspora | 64 | investor_matrices | HIGH |

### Matrix 19.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-SN01 | patrimoine | Patrimoine total | integer | sensitive | investor_matrices | HIGH |
| INVE-SN02 | revenus | Revenus annuels | integer | sensitive | investor_matrices | HIGH |
| INVE-SN03 | identité | Identité exacte | string | sensitive | anonymity | HIGH |

### Matrix 19.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-D01 | profil_risque | Profil risque | string | rendement+horizon+risque | matching_model | HIGH |
| INVE-D02 | capacité_invest | Capacité investissement | integer | budget_inv - autres_engagements | pricing_model | HIGH |
| INVE-D03 | classe_investisseur | Classe investisseur | string | budget+expérience+stratégie | investor_matrices | HIGH |

### Matrix 19.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| INVE-F01 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| INVE-F02 | "Nationalité ?" | Discrimination potentielle | Directive Art.14 | HIGH |
| INVE-F03 | "Situation familiale ?" | Irrelevant | Directive Art.14 | HIGH |
| INVE-F04 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |

---

## 20. investissement_promotion (Development Investment)

### Matrix 20.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | INV-MATRIX-004 |
| canonical_name | investissement_promotion |
| request_family | INVESTMENT_SEARCH |
| transaction_type | INVEST |
| property_or_service_type | investissement_promotion |
| requester_typology | developer, promoter, investor |
| journey_stage | SEARCH |
| description | Matrice pour investissement en promotion / development project. |

### Matrix 20.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-01 | budget_inv | Budget investissement | integer | — | always | min:100000 | "Budget total ?" | 10 | hard_constraint | private | INV-COMMON-001 | HIGH |
| INVE-02 | rendement | Rendement cible (%) | float | — | always | min:0 | "Rendement visé ?" | 15 | hard_constraint | private | INV-COMMON-002 | HIGH |
| INVE-03 | horizon | Horizon | string | enum:court,moyen,long,très_long | always | — | "Horizon ?" | 20 | soft_constraint | private | INV-COMMON-003 | HIGH |
| INVE-04 | risque | Risque accepté | string | enum:très_faible,faible,moyen,élevé | always | — | "Risque ?" | 25 | soft_constraint | private | INV-COMMON-004 | HIGH |
| INVE-05 | stratégie | Stratégie | string | enum:plus-value,locatif,mixte,développement | always | — | "Stratégie ?" | 22 | soft_constraint | private | INV-COMMON-005 | HIGH |
| INVE-06 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | INV-COMMON-006 | HIGH |
| IPR-07 | type_projet | Type projet | string | enum:logement,bureau,commercial,mixte | always | — | "Type projet ?" | 12 | soft_constraint | private | investor_matrices | HIGH |
| IPR-08 | partenariat_recherché | Partenariat recherché | string | enum:seul,co-investissement,maîtrise_ouvrage,apport_terrain | general | — | "Partenariat ?" | 14 | ranking_preference | private | investor_matrices | HIGH |
| IPR-09 | budget_terrain | Budget terrain | integer | — | general | min:0 | "Budget terrain ?" | 16 | soft_constraint | private | investor_matrices | HIGH |

### Matrix 20.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-S01 | zone | Zone préférée | string | — | "Zone ?" | 8 | soft_constraint | INV-COMMON-007 | HIGH |
| INVE-S02 | expérience | Expérience | string | enum:débutant,intermédiaire,avancé,pro | "Expérience ?" | 30 | soft_constraint | INV-COMMON-008 | HIGH |
| INVE-S03 | financement | Financement | string | enum:fonds_propres,crédit,partenariat | "Source financement ?" | 35 | soft_constraint | INV-COMMON-009 | HIGH |

### Matrix 20.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-M01 | rendement | Rendement | float | hard_constraint | INV-COMMON-002 | HIGH |
| INVE-M02 | budget | Budget | integer | hard_constraint | INV-COMMON-001 | HIGH |
| INVE-M03 | horizon | Horizon | string | soft_constraint | INV-COMMON-003 | HIGH |
| INVE-M04 | risque | Risque | string | soft_constraint | INV-COMMON-004 | HIGH |
| INVE-M05 | ville | Ville | string | hard_constraint | INV-COMMON-006 | HIGH |
| INVE-M06 | stratégie | Stratégie | string | soft_constraint | INV-COMMON-005 | HIGH |

### Matrix 20.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-I01 | profil | Description profil | string | "Parlez de votre profil d'investisseur." | 85 | soft_constraint | investor_matrices | HIGH |
| INVE-I02 | autres_inv | Autres investissements | string | "Autres investissements ?" | 86 | ranking_preference | INV-COMMON-010 | HIGH |
| INVE-I03 | accompagnement | Accompagnement | boolean | "Accompagnement ?" | 87 | soft_constraint | INV-COMMON-011 | HIGH |

### Matrix 20.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-V01 | proche | Proche sur place | boolean | "Proche sur place pour visiter ?" | 90 | soft_constraint | INV-COMMON-016 | HIGH |
| INVE-V02 | estimation | Estimation humaine | boolean | "Estimation humaine ?" | 91 | soft_constraint | INV-COMMON-017 | HIGH |
| INVE-V03 | documents | Documents souhaités | string | "Documents complémentaires ?" | 92 | soft_constraint | INV-COMMON-018 | HIGH |

### Matrix 20.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-T01 | nom | Nom | string | "Nom ?" | 95 | soft_constraint | INV-COMMON-012 | HIGH |
| INVE-T02 | téléphone | Téléphone | string | "Téléphone ?" | 96 | soft_constraint | INV-COMMON-013 | HIGH |
| INVE-T03 | email | Email | string | "Email ?" | 97 | soft_constraint | INV-COMMON-014 | HIGH |

### Matrix 20.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-R01 | diaspora | Diaspora | boolean | "Diaspora ?" | 40 | ranking_preference | INV-COMMON-015 | HIGH |
| INVE-R02 | type_bien_préféré | Type bien préféré | string | "Type bien cible ?" | 42 | ranking_preference | investor_matrices | HIGH |
| INVE-R03 | capital | Capital disponible total | integer | "Capital total ?" | 44 | soft_constraint | investor_matrices | HIGH |
| INVE-R04 | exit | Stratégie sortie | string | ","Stratégie sortie ?" | 46 | ranking_preference | investor_matrices | HIGH |

### Matrix 20.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-O01 | délai_investissement | Délai investissement | string | "Délai pour investir ?" | 50 | investor_matrices | HIGH |
| INVE-O02 | partenaires | Partenaires | string | "Partenaires ?" | 52 | investor_matrices | HIGH |
| INVE-O03 | conseil | Besoin conseil | boolean | "Besoin conseil ?" | 54 | investor_matrices | HIGH |

### Matrix 20.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INVE-C01 | mandat | Mandat recherche | boolean | besoin_accompagnement | 60 | investor_matrices | HIGH |
| INVE-C02 | budget_par_bien | Budget par bien | integer | stratégie=mixte | 62 | investor_matrices | HIGH |
| INVE-C03 | pays_résidence | Pays résidence | string | diaspora | 64 | investor_matrices | HIGH |

### Matrix 20.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-SN01 | patrimoine | Patrimoine total | integer | sensitive | investor_matrices | HIGH |
| INVE-SN02 | revenus | Revenus annuels | integer | sensitive | investor_matrices | HIGH |
| INVE-SN03 | identité | Identité exacte | string | sensitive | anonymity | HIGH |

### Matrix 20.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| INVE-D01 | profil_risque | Profil risque | string | rendement+horizon+risque | matching_model | HIGH |
| INVE-D02 | capacité_invest | Capacité investissement | integer | budget_inv - autres_engagements | pricing_model | HIGH |
| INVE-D03 | classe_investisseur | Classe investisseur | string | budget+expérience+stratégie | investor_matrices | HIGH |

### Matrix 20.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| INVE-F01 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| INVE-F02 | "Nationalité ?" | Discrimination potentielle | Directive Art.14 | HIGH |
| INVE-F03 | "Situation familiale ?" | Irrelevant | Directive Art.14 | HIGH |
| INVE-F04 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |

---

## 21. syndicat_copropriete (Condo/Co-ownership)

### Matrix 21.1 — Matrix Identification

| field | value |
| --- | --- |
| matrix_id | INV-MATRIX-005 |
| canonical_name | syndicat_copropriete |
| request_family | INVESTMENT_SEARCH |
| transaction_type | MANAGE, INVEST |
| property_or_service_type | syndicat_copropriete |
| requester_typology | syndic, co-owner, investor |
| journey_stage | SEARCH |
| description | Matrice pour syndicat de copropriété / co-ownership management. |

### Matrix 21.2 — Minimum Intake Fields

| field_id | label | description | data_type | allowed_values | mandatory_when | validation_rules | question_template | question_priority | matching_role | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SYND-01 | budget_inv | Budget investissement | integer | — | always | min:100000 | "Budget total ?" | 10 | hard_constraint | private | INV-COMMON-001 | HIGH |
| SYND-02 | rendement | Rendement cible (%) | float | — | always | min:0 | "Rendement visé ?" | 15 | hard_constraint | private | INV-COMMON-002 | HIGH |
| SYND-03 | horizon | Horizon | string | enum:court,moyen,long,très_long | always | — | "Horizon ?" | 20 | soft_constraint | private | INV-COMMON-003 | HIGH |
| SYND-04 | risque | Risque accepté | string | enum:très_faible,faible,moyen,élevé | always | — | "Risque ?" | 25 | soft_constraint | private | INV-COMMON-004 | HIGH |
| SYND-05 | stratégie | Stratégie | string | enum:plus-value,locatif,mixte,développement | always | — | "Stratégie ?" | 22 | soft_constraint | private | INV-COMMON-005 | HIGH |
| SYND-06 | ville | Ville | string | enum:cities | always | in:cities | "Ville ?" | 5 | hard_constraint | public | INV-COMMON-006 | HIGH |
| SYN-07 | nb_lots | Nombre de lots | integer | — | always | min:2 | "Nombre de lots ?" | 12 | hard_constraint | private | 02B-Ch.5 | HIGH |
| SYN-08 | type_immeuble | Type immeuble | string | enum:résidentiel,commercial,mixte | always | — | "Type immeuble ?" | 14 | soft_constraint | private | 02B-Ch.5 | HIGH |
| SYN-09 | besoins_gestion | Besoins gestion | string | enum:recouvrement,entretien,conformité,contentieux | general | — | "Besoins gestion ?" | 16 | ranking_preference | private | 02B-Ch.5 | HIGH |

### Matrix 21.3 — Minimum Search Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SYND-S01 | zone | Zone préférée | string | — | "Zone ?" | 8 | soft_constraint | INV-COMMON-007 | HIGH |
| SYND-S02 | expérience | Expérience | string | enum:débutant,intermédiaire,avancé,pro | "Expérience ?" | 30 | soft_constraint | INV-COMMON-008 | HIGH |
| SYND-S03 | financement | Financement | string | enum:fonds_propres,crédit,partenariat | "Source financement ?" | 35 | soft_constraint | INV-COMMON-009 | HIGH |

### Matrix 21.4 — Minimum Matching Fields

| field_id | label | description | data_type | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| SYND-M01 | rendement | Rendement | float | hard_constraint | INV-COMMON-002 | HIGH |
| SYND-M02 | budget | Budget | integer | hard_constraint | INV-COMMON-001 | HIGH |
| SYND-M03 | horizon | Horizon | string | soft_constraint | INV-COMMON-003 | HIGH |
| SYND-M04 | risque | Risque | string | soft_constraint | INV-COMMON-004 | HIGH |
| SYND-M05 | ville | Ville | string | hard_constraint | INV-COMMON-006 | HIGH |
| SYND-M06 | stratégie | Stratégie | string | soft_constraint | INV-COMMON-005 | HIGH |

### Matrix 21.5 — Minimum Introduction Fields

| field_id | label | description | data_type | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SYND-I01 | profil | Description profil | string | "Parlez de votre profil d'investisseur." | 85 | soft_constraint | investor_matrices | HIGH |
| SYND-I02 | autres_inv | Autres investissements | string | "Autres investissements ?" | 86 | ranking_preference | INV-COMMON-010 | HIGH |
| SYND-I03 | accompagnement | Accompagnement | boolean | "Accompagnement ?" | 87 | soft_constraint | INV-COMMON-011 | HIGH |

### Matrix 21.6 — Minimum Visit Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SYND-V01 | proche | Proche sur place | boolean | "Proche sur place pour visiter ?" | 90 | soft_constraint | INV-COMMON-016 | HIGH |
| SYND-V02 | estimation | Estimation humaine | boolean | "Estimation humaine ?" | 91 | soft_constraint | INV-COMMON-017 | HIGH |
| SYND-V03 | documents | Documents souhaités | string | "Documents complémentaires ?" | 92 | soft_constraint | INV-COMMON-018 | HIGH |

### Matrix 21.7 — Minimum Transaction Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SYND-T01 | nom | Nom | string | "Nom ?" | 95 | soft_constraint | INV-COMMON-012 | HIGH |
| SYND-T02 | téléphone | Téléphone | string | "Téléphone ?" | 96 | soft_constraint | INV-COMMON-013 | HIGH |
| SYND-T03 | email | Email | string | "Email ?" | 97 | soft_constraint | INV-COMMON-014 | HIGH |

### Matrix 21.8 — Recommended Fields

| field_id | label | description | data_type | allowed_values | question_template | question_priority | matching_role | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SYND-R01 | diaspora | Diaspora | boolean | "Diaspora ?" | 40 | ranking_preference | INV-COMMON-015 | HIGH |
| SYND-R02 | type_bien_préféré | Type bien préféré | string | "Type bien cible ?" | 42 | ranking_preference | investor_matrices | HIGH |
| SYND-R03 | capital | Capital disponible total | integer | "Capital total ?" | 44 | soft_constraint | investor_matrices | HIGH |
| SYND-R04 | exit | Stratégie sortie | string | ","Stratégie sortie ?" | 46 | ranking_preference | investor_matrices | HIGH |

### Matrix 21.9 — Optional Fields

| field_id | label | description | data_type | question_template | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SYND-O01 | délai_investissement | Délai investissement | string | "Délai pour investir ?" | 50 | investor_matrices | HIGH |
| SYND-O02 | partenaires | Partenaires | string | "Partenaires ?" | 52 | investor_matrices | HIGH |
| SYND-O03 | conseil | Besoin conseil | boolean | "Besoin conseil ?" | 54 | investor_matrices | HIGH |

### Matrix 21.10 — Conditional Fields

| field_id | label | description | data_type | condition | question_priority | source | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SYND-C01 | mandat | Mandat recherche | boolean | besoin_accompagnement | 60 | investor_matrices | HIGH |
| SYND-C02 | budget_par_bien | Budget par bien | integer | stratégie=mixte | 62 | investor_matrices | HIGH |
| SYND-C03 | pays_résidence | Pays résidence | string | diaspora | 64 | investor_matrices | HIGH |

### Matrix 21.11 — Sensitive Fields

| field_id | label | description | data_type | privacy_level | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| SYND-SN01 | patrimoine | Patrimoine total | integer | sensitive | investor_matrices | HIGH |
| SYND-SN02 | revenus | Revenus annuels | integer | sensitive | investor_matrices | HIGH |
| SYND-SN03 | identité | Identité exacte | string | sensitive | anonymity | HIGH |

### Matrix 21.12 — Derived Fields

| field_id | label | description | data_type | derivation_rule | source | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| SYND-D01 | profil_risque | Profil risque | string | rendement+horizon+risque | matching_model | HIGH |
| SYND-D02 | capacité_invest | Capacité investissement | integer | budget_inv - autres_engagements | pricing_model | HIGH |
| SYND-D03 | classe_investisseur | Classe investisseur | string | budget+expérience+stratégie | investor_matrices | HIGH |

### Matrix 21.13 — Forbidden Questions

| field_id | forbidden_question | rationale | source | confidence |
| --- | --- | --- | --- | --- |
| SYND-F01 | "Âge ?" | Discrimination | Directive Art.14 | HIGH |
| SYND-F02 | "Nationalité ?" | Discrimination potentielle | Directive Art.14 | HIGH |
| SYND-F03 | "Situation familiale ?" | Irrelevant | Directive Art.14 | HIGH |
| SYND-F04 | "Chambres ?" | Résidentiel | qualification §12.14 | HIGH |

---

*Document patrimonial Gold — Matrices de qualification commerciale et investissement — 2026-07-15*
