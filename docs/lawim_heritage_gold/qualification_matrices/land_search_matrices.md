# LAND SEARCH QUALIFICATION MATRICES — LAWIM Heritage Gold

**Domain :** LAND_SEARCH
**Market :** Cameroon (Yaounde, Douala, and other Cameroonian cities)
**Date :** 2026-07-15
**Status :** VALIDATED — Canonical reference for land qualification

---

## GLOBAL RULES FOR ALL LAND TYPES

### Forbidden Questions (Never Ask)
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Residential room count — irrelevant for land |
| douches | Bathroom count — irrelevant for land |
| salon | Living room — irrelevant for land |
| pieces | Room count — irrelevant for land |
| standing | Standing level — deduced from location/price, never asked |

### Cameroon Land Sensitivity Rules
| Rule | Description |
|------|-------------|
| LAND-R01 | Always distinguish titre/non-titre — title sensitivity is critical |
| LAND-R02 | Surface is mandatory — always collect in m2 |
| LAND-R03 | Budget = global price OR price per m2 (user chooses) |
| LAND-R04 | Location: ville + quartier OR axe + village + repere |
| LAND-R05 | Never conclude legal validity from user declarations alone |
| LAND-R06 | verification_required = true for all land transactions |
| LAND-R07 | professional_review = notaire (notary) or geometre (surveyor) required |
| LAND-R08 | Usage prevu: habitation, commerce, industrie, agriculture, mixte |
| LAND-R09 | Accessibilite: road distance + quality are critical |
| LAND-R10 | Viabilisation: eau, electricite, groupe electrogene are key utilities |

### Matching Semantics for Land
| Field | Role | Tolerance |
|-------|------|-----------|
| city | hard_constraint | Exact match required |
| budget | hard_constraint | +/-15% for buy, +/-25% for invest |
| surface | soft_constraint | Nearby surfaces acceptable (+/-30%) |
| usage | hard_constraint | Exact match required |
| titre/non-titre | depends on user preference | If user requires titre → hard_constraint |
| loti/non-loti | soft_constraint | Flexible based on user preference |
| accessibilite | ranking_preference | Better access = higher rank |
| viabilisation | soft_constraint | Water/electricity preferred |
| topographie | soft_constraint | Flat preferred; pente acceptable |
| quartier | hard_constraint | Neighborhood match required |

### Standard Field Definitions
| field_id | label | data_type | description |
|----------|-------|-----------|-------------|
| ville | Ville | string | City where land is located |
| quartier | Quartier | string | Neighborhood or zone |
| axe | Axe principal | string | Main road axis or direction |
| village | Village | string | Village name (for rural lands) |
| repere | Point de repere | string | Landmark or reference point |
| surface | Surface | float | Land area in square meters (m2) |
| budget_total | Budget total | float | Maximum total budget in FCFA |
| budget_par_m2 | Budget au m2 | float | Budget per square meter in FCFA |
| usage_prevu | Usage prevu | enum | habitation, commerce, industrie, agriculture, mixte |
| titre_requis | Titre foncier requis | boolean | Whether the user requires a land title |
| type_titre | Type de titre | enum | titre_foncier, attestation, concession, certificat_occupation, non_documente |
| num_titre | Numero du titre foncier | string | Land title registration number |
| nombre_signataires | Nombre de signataires | integer | Number of signatories required for sale |
| identite_signataires | Identite des signataires | string | Identity information of signatories |
| disponibilite_signataires | Disponibilite des signataires | string | Availability of all signatories |
| type_document | Type de document | enum | certificat_propriete, plan_bornage, lotissement, acte_notarie, promesse_vente |
| certificat_propriete | Certificat de propriete | boolean | Whether property certificate exists |
| plan_bornage | Plan de bornage | boolean | Whether boundary survey plan exists |
| lotissement | Lotissement approuve | boolean | Whether subdivision is approved |
| terrain_loti | Terrain loti | boolean | Whether land is serviced (roads, utilities) |
| terrain_constructible | Terrain constructible | boolean | Whether land is buildable |
| accessibilite | Accessibilite | enum | route_goudronnee, route_terre, sentier, enclave |
| distance_route | Distance de la route | float | Distance from main road in meters |
| qualite_acces | Qualite d'acces | enum | excellente, bonne, moyenne, mediocre, difficile |
| viabilisation_eau | Eau | boolean | Whether water is available on site |
| viabilisation_electricite | Electricite | boolean | Whether electricity is available on site |
| groupe_electrogene | Groupe electrogene | boolean | Whether generator is present/needed |
| topographie | Topographie | enum | plat, legere_pente, forte_pente, vallee, colline |
| inondable | Zone inondable | boolean | Whether land is in flood zone |
| occupation_actuelle | Occupation actuelle | enum | libre, cultive, bati, en_friche |
| servitudes | Servitudes | string | Easements or rights of way affecting the land |
| litiges_connus | Litiges connus | boolean | Whether known disputes exist |
| hypotheque_charge | Hypotheque / charge | boolean | Whether mortgage or encumbrance exists |
| succession | Succession | boolean | Whether land is subject to inheritance proceedings |
| indivision | Indivision | boolean | Whether land is in co-ownership |
| procuration | Procuration | boolean | Whether power of attorney is involved |
| bornage | Bornage effectue | boolean | Whether boundary marking has been done |
| pv_bornage | PV de bornage | boolean | Whether official boundary minutes exist |
| certificat_urbanisme | Certificat d'urbanisme | boolean | Whether town planning certificate exists |
| coordonnees_gps | Coordonnees GPS | string | GPS coordinates of the land |
| photo_terrain | Photo du terrain | string | Photograph of the land |
| video_terrain | Video du terrain | string | Video of the land |
| disponibilite | Disponibilite | enum | immediate, 1_mois, 3_mois, 6_mois, a_definir |
| delai_souhaite | Delai souhaite | enum | urgent, 1_mois, 3_mois, 6_mois, pas_de_delai |
| contact_nom | Nom du contact | string | Contact person name |
| contact_telephone | Telephone | string | Contact phone number |
| contact_email | Email | string | Contact email |
| source_financement | Source de financement | enum | comptant, credit_bancaire, tontine, diaspora, pret_familial |
| besoin_notaire | Besoin d'un notaire | boolean | Whether notary services are needed |
| besoin_geometre | Besoin d'un geometre | boolean | Whether surveyor services are needed |
| visite_souhaitee | Visite souhaitee | boolean | Whether a visit is desired |
| urgence | Niveau d'urgence | enum | urgent, modere, pas_urgent |
| commentaire | Commentaire libre | string | Free-text comment |

---

## 1. terrain_titre

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_TITRE_001 |
| authoritative_name | Terrain avec titre foncier (Titled Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_titre |

### Description
Terrain disposant d'un titre foncier valide et enregistre au Cameroun. Le titre foncier est le document de propriete le plus fort dans le systeme foncier camerounais. Ce type de terrain offre la securite juridique maximale pour l'acheteur.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Dans quelle ville cherchez-vous le terrain ? | 10 |
| quartier | always | Quel quartier ou quelle zone vous interesse ? | 20 |
| surface | always | Quelle surface souhaitez-vous (en m2) ? | 30 |
| budget_total | always | Quel est votre budget maximum pour ce terrain ? | 40 |
| usage_prevu | always | Quel usage comptez-vous faire du terrain ? (habitation, commerce, industrie, agriculture, mixte) | 50 |
| num_titre | when user confirms having a titre | Quel est le numero du titre foncier ? | 60 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Dans quelle ville ? | 10 |
| quartier | always | Quel quartier precisement ? | 20 |
| surface_min | always | Surface minimale recherchee ? | 30 |
| budget_max | always | Budget maximum ? | 40 |
| usage_prevu | always | Usage prevu ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 (city=30%) |
| quartier | hard_constraint | MATCH-001 (neighborhood=25%) |
| budget_total | hard_constraint | MATCH-003 (buy=+/-15%) |
| usage_prevu | hard_constraint | PROP-001 (type match) |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| titre_disponible | hard_constraint | MATCH-007 (title_foncier=+10) |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Comment vous appelez-vous ? | 5 |
| contact_telephone | always | Quel est votre numero de telephone ? | 10 |
| ville | always | Dans quelle ville cherchez-vous ? | 15 |
| budget_total | always | Quel budget ? | 20 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Souhaitez-vous organiser une visite du terrain ? | 5 |
| disponibilite | when visit requested | Quand seriez-vous disponible pour la visite ? | 10 |
| coordonnees_gps | before visit | Je vous envoie les coordonnees GPS du terrain. | 15 |
| besoin_geometre | when visit confirmed | Souhaitez-vous qu'un geometre vous accompagne ? | 20 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| num_titre | always before transaction | Quel est le numero du titre foncier ? | 5 |
| identite_signataires | always before transaction | Qui sont les signataires autorises ? | 10 |
| nombre_signataires | always before transaction | Combien de personnes doivent signer ? | 15 |
| disponibilite_signataires | always before transaction | Les signataires sont-ils tous disponibles ? | 20 |
| besoin_notaire | always | Avez-vous besoin d'un notaire pour la transaction ? | 25 |
| source_financement | always | Comment comptez-vous financer l'achat ? | 30 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| accessibilite | Accessibilite | enum | Quel type d'acces au terrain ? | 35 |
| distance_route | Distance de la route | float | A quelle distance de la route principale ? | 36 |
| viabilisation_eau | Eau disponible | boolean | Avez-vous besoin d'eau sur le terrain ? | 37 |
| viabilisation_electricite | Electricite disponible | boolean | L'electricite est-elle necessaire ? | 38 |
| topographie | Topographie | enum | Le terrain est-il plat ou en pente ? | 39 |
| inondable | Zone inondable | boolean | Le terrain est-il en zone inondable ? | 40 |
| terrain_constructible | Constructible | boolean | Le terrain est-il constructible ? | 41 |
| qualite_acces | Qualite d'acces | enum | Quelle est la qualite de la route d'acces ? | 42 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Point de repere | string | Y a-t-il un point de repere connu ? | 45 |
| groupe_electrogene | Groupe electrogene | boolean | Un groupe electrogene est-il necessaire ? | 46 |
| occupation_actuelle | Occupation actuelle | enum | Le terrain est-il actuellement occupe ? | 47 |
| photo_terrain | Photo du terrain | string | Pouvez-vous envoyer une photo ? | 48 |
| video_terrain | Video du terrain | string | Une video du terrain est-elle disponible ? | 49 |
| commentaire | Commentaire | string | Avez-vous d'autres precisions ? | 50 |
| delai_souhaite | Delai souhaite | enum | Quel est votre delai souhaite ? | 44 |
| urgence | Niveau d'urgence | enum | Quel est le niveau d'urgence ? | 43 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| titre_verification | when titre foncier number provided | num_titre | Le titre a-t-il ete verifie au conservatoire foncier ? | 55 |
| hypotheque_charge | when titre exists | num_titre | Y a-t-il une hypotheque ou une charge sur ce titre ? | 56 |
| litiges_connus | when any legal concern | -- | Existe-t-il des litiges connus sur ce terrain ? | 57 |
| servitudes | when access or usage concern | accessibilite | Y a-t-il des servitudes sur ce terrain ? | 58 |
| certificat_urbanisme | when constructible | terrain_constructible | Le certificat d'urbanisme est-il disponible ? | 59 |
| coordonnees_gps | before visit | visite_souhaitee | Pouvez-vous partager les coordonnees GPS ? | 60 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| num_titre | confidential | HERITAGE_VALIDATED | HIGH | Only shared with verified parties after NDA |
| identite_signataires | confidential | HERITAGE_VALIDATED | HIGH | Protected under RGPD, notary-only disclosure |
| nombre_signataires | sensitive | HERITAGE_VALIDATED | HIGH | Internal use only |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate to legal team |
| hypotheque_charge | confidential | HERITAGE_VALIDATED | HIGH | Verified with conservatoire foncier |
| succession | sensitive | HERITAGE_VALIDATED | MEDIUM | Requires notary verification |
| indivision | sensitive | HERITAGE_VALIDATED | MEDIUM | Requires all co-owners consent |
| procuration | sensitive | HERITAGE_VALIDATED | MEDIUM | Verify power of attorney validity |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| titre_valide | Titre valide | derived from num_titre + conservatoire verification | boolean |
| prix_au_m2 | Prix au m2 | budget_total / surface | float |
| score_accessibilite | Score d'accessibilite | weighted(qualite_acces, distance_route) | integer |
| score_viabilisation | Score de viabilisation | weighted(eau, electricite, groupe_electrogene) | integer |
| budget_coherent | Budget coherent | derived from budget vs market price per m2 for zone | boolean |
| risque_inondation | Risque d'inondation | derived from inondable + topographie + zone | enum |
| classification_terrain | Classification | derived from surface + usage + topographie | string |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant for land qualification |
| douches | Irrelevant for land qualification |
| salon | Irrelevant for land qualification |
| pieces | Irrelevant for land qualification |
| standing | Deduced from price + location, never asked |
| nombre_etages | Irrelevant for undeveloped land |
| nombre_de_places_parking | Irrelevant for raw land |

---

## 2. terrain_non_titre

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_NON_TITRE_001 |
| authoritative_name | Terrain sans titre foncier (Untitled Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_non_titre |

### Description
Terrain ne disposant pas de titre foncier. Peut avoir des documents alternatifs: certificat de propriete, acte notarie, promesse de vente, droit coutumier. La qualification est plus exigeante car le risque juridique est plus eleve. La verification professionnelle (notaire/geometre) est obligatoire.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Dans quelle ville se trouve le terrain ? | 10 |
| quartier | always | Quel quartier ou axe ? | 20 |
| surface | always | Quelle surface approximative ? | 30 |
| budget_total | always | Quel budget prevoyez-vous ? | 40 |
| usage_prevu | always | Quel usage prevoyez-vous ? | 50 |
| type_document | always | Quel type de document est disponible ? (certificat de propriete, plan de bornage, lotissement, acte notarie, promesse de vente) | 55 |
| certificat_propriete | when type_document includes it | Avez-vous un certificat de propriete ? | 56 |
| plan_bornage | when type_document includes it | Un plan de bornage a-t-il ete etabli ? | 57 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Dans quelle ville ? | 10 |
| quartier_ou_axe | always | Quartier ou axe principal ? | 20 |
| surface_min | always | Surface minimale ? | 30 |
| budget_max | always | Budget maximum ? | 40 |
| documents_requis | always | Quels documents exigez-vous ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 (city=30%) |
| quartier | hard_constraint | MATCH-001 (neighborhood=25%) |
| budget_total | hard_constraint | MATCH-003 (buy=+/-15%) |
| usage_prevu | hard_constraint | PROP-001 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| type_document | soft_constraint | LAND-MATCH-DOCUMENT |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Quel est votre nom ? | 5 |
| contact_telephone | always | Votre numero de telephone ? | 10 |
| ville | always | Dans quelle ville cherchez-vous ? | 15 |
| budget_total | always | Quel budget approximatif ? | 20 |
| type_document | always | Quels documents avez-vous ou exigez-vous ? | 25 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Voulez-vous visiter le terrain ? | 5 |
| disponibilite | when visit requested | Quand etes-vous disponible ? | 10 |
| besoin_geometre | always | Un geometre devra confirmer les limites. | 15 |
| pv_bornage | when bornage exists | Le PV de bornage est-il disponible ? | 20 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Un notaire est obligatoire pour securiser la transaction. | 5 |
| type_document | always | Quels documents seront remis a la vente ? | 10 |
| plan_bornage | always | Un plan de bornage est-il disponible ? | 15 |
| certificat_propriete | when available | Pouvez-vous fournir le certificat de propriete ? | 20 |
| litiges_connus | always | Existe-t-il des contestations sur ce terrain ? | 25 |
| source_financement | always | Comment comptez-vous payer ? | 30 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| accessibilite | Accessibilite | enum | Quel est l'etat de la route d'acces ? | 35 |
| distance_route | Distance route | float | Distance de la route principale ? | 36 |
| viabilisation_eau | Eau | boolean | Y a-t-il une source d'eau ? | 37 |
| viabilisation_electricite | Electricite | boolean | Y a-t-il l'electricite ? | 38 |
| topographie | Topographie | enum | Le terrain est-il plat ou en pente ? | 39 |
| inondable | Inondable | boolean | Le terrain est-il inondable ? | 40 |
| occupation_actuelle | Occupation | enum | Le terrain est-il actuellement occupe ? | 41 |
| lotissement | Lotissement approuve | boolean | Le lotissement est-il approuve ? | 42 |
| terrain_constructible | Constructible | boolean | Le terrain est-il constructible ? | 43 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Point de repere | string | Y a-t-il un repere connu ? | 45 |
| groupe_electrogene | Groupe electrogene | boolean | Avez-vous besoin d'un groupe electrogene ? | 46 |
| photo_terrain | Photo | string | Photo disponible ? | 47 |
| commentaire | Commentaire | string | Autres precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai souhaite ? | 44 |
| urgence | Urgence | enum | Urgence ? | 43 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| succession | when multiple claimants | -- | Le terrain fait-il l'objet d'une succession ? | 55 |
| indivision | when multiple owners | -- | Le terrain est-il en indivision ? | 56 |
| servitudes | when access concern | accessibilite | Y a-t-il des servitudes ? | 57 |
| procuration | when owner not present | -- | Y a-t-il une procuration pour vendre ? | 58 |
| hypotheque_charge | when any debt concern | -- | Y a-t-il une hypotheque ? | 59 |
| bornage | when limits unclear | plan_bornage | Le bornage a-t-il ete realise ? | 60 |
| pv_bornage | when bornage done | bornage | Le PV de bornage est-il signe ? | 61 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| type_document | sensitive | HERITAGE_VALIDATED | HIGH | Verify authenticity with issuing authority |
| certificat_propriete | confidential | HERITAGE_VALIDATED | HIGH | Notary-only verification |
| plan_bornage | sensitive | HERITAGE_VALIDATED | MEDIUM | Cross-check with surveyor |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate to legal immediately |
| succession | confidential | HERITAGE_VALIDATED | MEDIUM | Requires full inheritance documentation |
| indivision | confidential | HERITAGE_VALIDATED | MEDIUM | Requires all co-owner consent |
| procuration | confidential | HERITAGE_VALIDATED | MEDIUM | Verify notarial validity |
| hypotheque_charge | confidential | HERITAGE_VALIDATED | HIGH | Check with conservatoire foncier |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| risque_juridique | Risque juridique | weighted(litiges, succession, indivision, type_document) | enum |
| titre_obtenable | Titre obtenable | derived from documents + bornage + urbanisme | boolean |
| prix_au_m2 | Prix au m2 | budget_total / surface | float |
| score_documentaire | Score documentaire | weighted(type_document, certificat, bornage) | integer |
| necessite_notaire | Necessite notaire | derived from risque_juridique + budget | boolean |
| delai_estime_regularisation | Delai regularisation | derived from type_document + bornage | string |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant for land |
| douches | Irrelevant for land |
| salon | Irrelevant for land |
| pieces | Irrelevant for land |
| standing | Deduced from price + location |
| num_titre | No title exists for this type |

---

## 3. terrain_loti

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_LOTI_001 |
| authoritative_name | Terrain loti (Serviced Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_loti |

### Description
Terrain viabilise et divise en lots avec acces a la route, a l'eau et a l'electricite. Le lotissement approuve par la municipalite garantit que les normes d'urbanisme sont respectees.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Dans quelle ville se trouve le terrain loti ? | 10 |
| quartier | always | Dans quel quartier ? | 20 |
| surface | always | Quelle surface du lot ? | 30 |
| budget_total | always | Quel budget ? | 40 |
| usage_prevu | always | Pour quel usage ? | 50 |
| lotissement_approuve | always | Le lotissement est-il approuve par la mairie ? | 55 |
| accessibilite | always | Quel type d'acces ? | 56 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ? | 20 |
| surface_min | always | Surface min ? | 30 |
| budget_max | always | Budget max ? | 40 |
| loti | always | Terrain loti obligatoire ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 |
| quartier | hard_constraint | MATCH-001 |
| budget_total | hard_constraint | MATCH-003 |
| usage_prevu | hard_constraint | PROP-001 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| terrain_loti | soft_constraint | LAND-MATCH-LOTI |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Votre nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| ville | always | Ville ? | 15 |
| budget_total | always | Budget ? | 20 |
| surface | always | Surface ? | 25 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite ? | 5 |
| disponibilite | when visit requested | Quand ? | 10 |
| coordonnees_gps | before visit | Coordonnees GPS ? | 15 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire requis pour l'acte. | 5 |
| lotissement_approuve | always | Copie de l'approbation du lotissement ? | 10 |
| certificat_urbanisme | always | Certificat d'urbanisme disponible ? | 15 |
| source_financement | always | Financement ? | 20 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| viabilisation_eau | Eau | boolean | Y a-t-il un raccordement eau ? | 35 |
| viabilisation_electricite | Electricite | boolean | Raccordement electrique ? | 36 |
| qualite_acces | Qualite acces | enum | Qualite de la voirie ? | 37 |
| distance_route | Distance route | float | Distance route principale ? | 38 |
| topographie | Topographie | enum | Terrain plat ou en pente ? | 39 |
| inondable | Inondable | boolean | Zone inondable ? | 40 |
| num_titre | Titre foncier | string | Le lot a-t-il un titre foncier individuel ? | 41 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo ? | 46 |
| commentaire | Commentaire | string | Autre ? | 50 |
| delai_souhaite | Delai | enum | Delai ? | 44 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| servitudes | when access shared | accessibilite | Servitudes existantes ? | 55 |
| hypotheque_charge | when titre exists | num_titre | Hypotheque sur le lot ? | 56 |
| litiges_connus | when any concern | -- | Litiges connus ? | 57 |
| certificat_urbanisme | when constructible | usage_prevu | Certificat d'urbanisme obtenu ? | 58 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| lotissement_approuve | public | HERITAGE_VALIDATED | HIGH | Verify with municipal records |
| num_titre | confidential | HERITAGE_VALIDATED | HIGH | Title-based; notary required |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate |
| hypotheque_charge | confidential | HERITAGE_VALIDATED | HIGH | Check conservatoire |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| prix_m2_loti | Prix m2 loti | budget_total / surface | float |
| score_lotissement | Score lotissement | weighted(lotissement_approuve, certificat_urbanisme) | integer |
| constructibilite | Constructibilite | derived from usage + urbanisme + lotissement | boolean |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |

---

## 4. terrain_non_loti

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_NON_LOTI_001 |
| authoritative_name | Terrain non loti (Unserviced Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_non_loti |

### Description
Terrain brut sans viabilisation ni division en lots. Pas de voirie, pas de raccordements eau/electricite. Prix plus bas mais l'acheteur doit prevoir les couts de viabilisation.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Dans quelle ville ? | 10 |
| quartier_ou_axe | always | Quartier ou axe ? | 20 |
| surface | always | Surface totale ? | 30 |
| budget_total | always | Budget ? | 40 |
| usage_prevu | always | Usage prevu ? | 50 |
| accessibilite | always | Comment accede-t-on au terrain ? | 55 |
| distance_route | always | Distance de la route principale ? | 56 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| zone | always | Zone ? | 20 |
| surface_min | always | Surface ? | 30 |
| budget_max | always | Budget ? | 40 |
| usage_prevu | always | Usage ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 |
| quartier_ou_zone | hard_constraint | MATCH-001 |
| budget_total | hard_constraint | MATCH-003 |
| usage_prevu | hard_constraint | PROP-001 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| accessibilite | ranking_preference | LAND-MATCH-ACCESS |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| ville | always | Ville ? | 15 |
| budget_total | always | Budget ? | 20 |
| surface | always | Surface souhaitee ? | 25 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite necessaire ? | 5 |
| disponibilite | when visit | Disponibilite ? | 10 |
| besoin_geometre | always | Un geometre sera utile pour delimiter. | 15 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire obligatoire. | 5 |
| type_document | always | Quels documents ? | 10 |
| plan_bornage | when bornage exists | Plan de bornage ? | 15 |
| litiges_connus | always | Litiges ou contestations ? | 20 |
| source_financement | always | Financement ? | 25 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| viabilisation_eau | Eau possible | boolean | Possibilite de raccordement eau ? | 35 |
| viabilisation_electricite | Electricite possible | boolean | Possibilite d'electrification ? | 36 |
| topographie | Topographie | enum | Topographie du terrain ? | 37 |
| inondable | Inondable | boolean | Risque d'inondation ? | 38 |
| occupation_actuelle | Occupation | enum | Occupation actuelle ? | 39 |
| terrain_constructible | Constructible | boolean | Le POS autorise-t-il la construction ? | 40 |
| qualite_acces | Qualite acces | enum | Qualite de l'acces ? | 41 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| groupe_electrogene | Groupe electrogene | boolean | Groupe electrogene necessaire ? | 46 |
| photo_terrain | Photo | string | Photo ? | 47 |
| commentaire | Commentaire | string | Precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai ? | 44 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| servitudes | when access shared | accessibilite | Servitudes ? | 55 |
| succession | when multiple owners | -- | Succession en cours ? | 56 |
| indivision | when co-ownership | -- | Indivision ? | 57 |
| certificat_urbanisme | when constructible | usage_prevu | Certificat d'urbanisme ? | 58 |
| lotissement | when subdivision intended | usage_prevu | Projet de lotissement ? | 59 |
| bornage | when limits unclear | -- | Bornage effectue ? | 60 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| type_document | sensitive | HERITAGE_VALIDATED | HIGH | Verify documents |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate |
| succession | confidential | HERITAGE_VALIDATED | MEDIUM | Notary required |
| indivision | confidential | HERITAGE_VALIDATED | MEDIUM | All owners consent |
| servitudes | sensitive | HERITAGE_VALIDATED | MEDIUM | Survey verification |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| cout_viabilisation_estime | Cout viabilisation estime | surface * cost_per_m2_by_zone | float |
| potentiel_constructibilite | Potentiel constructibilite | derived from usage + zone rules | enum |
| prix_m2_brut | Prix m2 brut | budget_total / surface | float |
| score_accessibilite | Score acces | weighted(qualite_acces, distance_route) | integer |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |
| etage | Irrelevant for raw land |

---

## 5. terrain_titre_collectif

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_TITRE_COLLECTIF_001 |
| authoritative_name | Terrain avec titre collectif (Collective Title Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_titre_collectif |

### Description
Terrain dont le titre foncier est etabli au nom de plusieurs personnes (co-indivisaires, famille, GIC, association). La vente necessite l'accord de tous les titulaires.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ? | 20 |
| surface | always | Surface ? | 30 |
| budget_total | always | Budget ? | 40 |
| usage_prevu | always | Usage ? | 50 |
| nombre_signataires | always | Combien de personnes sont sur le titre ? | 55 |
| identite_signataires | always | Qui sont les signataires ? | 56 |
| disponibilite_signataires | always | Tous les signataires sont-ils disponibles pour la vente ? | 57 |
| num_titre | always | Numero du titre collectif ? | 58 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ? | 20 |
| surface_min | always | Surface ? | 30 |
| budget_max | always | Budget ? | 40 |
| accord_collectif | always | L'accord de tous les proprietaires est-il possible ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 |
| quartier | hard_constraint | MATCH-001 |
| budget_total | hard_constraint | MATCH-003 |
| usage_prevu | hard_constraint | PROP-001 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| nombre_signataires | informational_only | LAND-MATCH-SIGNATAIRES |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| ville | always | Ville ? | 15 |
| budget_total | always | Budget ? | 20 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite ? | 5 |
| disponibilite | when visit | Quand ? | 10 |
| coordonnees_gps | before visit | Coordonnees GPS ? | 15 |
| rencontre_signataires | when visit | Pouvez-vous rencontrer les co-proprietaires ? | 20 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire obligatoire pour titre collectif. | 5 |
| nombre_signataires | always | Confirmez le nombre de signataires. | 10 |
| identite_signataires | always | Liste complete des signataires ? | 15 |
| disponibilite_signataires | always | Tous disponibles pour signer ? | 20 |
| consentement_unanime | always | Consentement unanime confirme ? | 25 |
| procuration | when absent | Procuration pour les absents ? | 30 |
| source_financement | always | Financement ? | 35 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| indivision | Indivision | boolean | Le titre est-il en indivision ? | 36 |
| succession | Succession | boolean | Le terrain provient-il d'une succession ? | 37 |
| accessibilite | Accessibilite | enum | Acces au terrain ? | 38 |
| viabilisation_eau | Eau | boolean | Eau ? | 39 |
| viabilisation_electricite | Electricite | boolean | Electricite ? | 40 |
| topographie | Topographie | enum | Topographie ? | 41 |
| inondable | Inondable | boolean | Inondable ? | 42 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo ? | 46 |
| commentaire | Commentaire | string | Autre ? | 50 |
| delai_souhaite | Delai | enum | Delai ? | 44 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| litiges_connus | when any dispute | -- | Litiges entre co-indivisaires ? | 55 |
| hypotheque_charge | when titre exists | num_titre | Hypotheque sur le titre collectif ? | 56 |
| servitudes | when access shared | accessibilite | Servitudes ? | 57 |
| procuration_details | when procuration needed | procuration | Details de la procuration ? | 58 |
| pv_assemblee | when collective decision | -- | PV d'assemblee des co-proprietaires ? | 59 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| num_titre | confidential | HERITAGE_VALIDATED | HIGH | Notary only |
| identite_signataires | confidential | HERITAGE_VALIDATED | HIGH | RGPD protected |
| nombre_signataires | sensitive | HERITAGE_VALIDATED | HIGH | Internal |
| disponibilite_signataires | sensitive | HERITAGE_VALIDATED | MEDIUM | Confirmation required |
| indivision | confidential | HERITAGE_VALIDATED | MEDIUM | Legal documentation required |
| succession | confidential | HERITAGE_VALIDATED | MEDIUM | Notary verification |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate immediately |
| procuration | confidential | HERITAGE_VALIDATED | MEDIUM | Verify notarial validity |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| consentement_atteignable | Consentement atteignable | derived from disponibilite + nombre | boolean |
| risque_indivision | Risque indivision | derived from indivision + succession + litiges | enum |
| complexite_transaction | Complexite transaction | weighted(nombre_signataires, consentement, procuration) | enum |
| delai_estime_transaction | Delai transaction estime | derived from complexite + disponibilite | string |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |

---

## 6. terrain_titre_individuel

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_TITRE_INDIVIDUEL_001 |
| authoritative_name | Terrain avec titre individuel (Individual Title Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_titre_individuel |

### Description
Terrain avec titre foncier etabli au nom d'une seule personne physique ou morale. Transaction plus simple que le titre collectif. Un seul signataire requis. Type de terrain le plus securise et le plus recherche au Cameroun.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ? | 20 |
| surface | always | Surface ? | 30 |
| budget_total | always | Budget ? | 40 |
| usage_prevu | always | Usage ? | 50 |
| num_titre | always | Numero du titre foncier ? | 55 |
| identite_proprietaire | always | Identite du proprietaire inscrit au titre ? | 56 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ? | 20 |
| surface_min | always | Surface ? | 30 |
| budget_max | always | Budget ? | 40 |
| titre_individuel_requis | always | Titre individuel obligatoire ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 |
| quartier | hard_constraint | MATCH-001 |
| budget_total | hard_constraint | MATCH-003 |
| usage_prevu | hard_constraint | PROP-001 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| titre_individuel | hard_constraint | MATCH-007 (title_foncier=+10) |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| ville | always | Ville ? | 15 |
| budget_total | always | Budget ? | 20 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite ? | 5 |
| disponibilite | when visit | Quand ? | 10 |
| coordonnees_gps | before visit | Coordonnees ? | 15 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire requis. | 5 |
| num_titre | always | Numero de titre foncier. | 10 |
| identite_proprietaire | always | Identification du proprietaire. | 15 |
| verification_conservatoire | always | Verification au conservatoire foncier requise. | 20 |
| source_financement | always | Mode de financement ? | 25 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| hypotheque_charge | Hypotheque | boolean | Y a-t-il une hypotheque sur le titre ? | 35 |
| accessibilite | Accessibilite | enum | Acces ? | 36 |
| viabilisation_eau | Eau | boolean | Eau ? | 37 |
| viabilisation_electricite | Electricite | boolean | Electricite ? | 38 |
| topographie | Topographie | enum | Topographie ? | 39 |
| inondable | Inondable | boolean | Inondable ? | 40 |
| terrain_constructible | Constructible | boolean | Constructible ? | 41 |
| certificat_urbanisme | CU | boolean | Certificat d'urbanisme ? | 42 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo ? | 46 |
| video_terrain | Video | string | Video ? | 47 |
| commentaire | Commentaire | string | Precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai ? | 44 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| litiges_connus | when any concern | -- | Litiges connus ? | 55 |
| servitudes | when access concern | accessibilite | Servitudes ? | 56 |
| succession | when inherited | -- | Succession ? | 57 |
| procuration | when owner absent | -- | Procuration ? | 58 |
| bornage | when limits unclear | -- | Bornage effectue ? | 59 |
| pv_bornage | when bornage done | bornage | PV de bornage ? | 60 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| num_titre | confidential | HERITAGE_VALIDATED | HIGH | Notary-only |
| identite_proprietaire | confidential | HERITAGE_VALIDATED | HIGH | RGPD protected |
| hypotheque_charge | confidential | HERITAGE_VALIDATED | HIGH | Conservatoire check |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate |
| procuration | confidential | HERITAGE_VALIDATED | MEDIUM | Verify |
| succession | confidential | HERITAGE_VALIDATED | MEDIUM | Notary |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| titre_valide | Titre valide | num_titre + conservatoire check | boolean |
| risque_legal | Risque legal | weighted(hypotheque, litiges, succession) | enum |
| prix_m2 | Prix m2 | budget_total / surface | float |
| score_securite | Score securite | weighted(titre, hypotheque, litiges) | integer |
| transaction_ready | Pret pour transaction | derived from all transaction fields | boolean |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |

---

## 7. terrain_sous_morcellement

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_SOUS_MORCELLEMENT_001 |
| authoritative_name | Terrain en cours de morcellement (Land Undergoing Subdivision) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_sous_morcellement |

### Description
Terrain en cours de division en parcelles (morcellement). Le processus est encadre par un geometre et doit etre approuve par la municipalite. L'acheteur peut reserver une parcelle avant la finalisation.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ? | 20 |
| surface_souhaitee | always | Surface de la parcelle souhaitee ? | 30 |
| budget_total | always | Budget ? | 40 |
| usage_prevu | always | Usage ? | 50 |
| morcellement_approuve | always | Le morcellement est-il deja approuve ? | 55 |
| geometre_responsable | always | Qui est le geometre en charge ? | 56 |
| delai_morcellement | always | Quel est le delai estime de finalisation ? | 57 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ? | 20 |
| surface_min | always | Surface ? | 30 |
| budget_max | always | Budget ? | 40 |
| morcellement_avance | always | Morcellement a quel stade ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 |
| quartier | hard_constraint | MATCH-001 |
| budget_total | hard_constraint | MATCH-003 |
| usage_prevu | hard_constraint | PROP-001 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| avancement_morcellement | ranking_preference | LAND-MATCH-MORCELLEMENT |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| ville | always | Ville ? | 15 |
| budget_total | always | Budget ? | 20 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite du site ? | 5 |
| disponibilite | when visit | Quand ? | 10 |
| rencontre_geometre | always | Rencontre avec le geometre recommandee. | 15 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire requis pour l'attribution. | 5 |
| morcellement_approuve | always | Approbation municipale du morcellement ? | 10 |
| plan_morcellement | always | Plan de morcellement approuve ? | 15 |
| promesse_attribution | always | Promesse d'attribution signee ? | 20 |
| source_financement | always | Financement ? | 25 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| num_lot | Numero de lot | string | Quel numero de lot ? | 35 |
| viabilisation_prevue | Viabilisation prevue | boolean | Viabilisation prevue ? | 36 |
| accessibilite | Accessibilite | enum | Acces ? | 37 |
| topographie | Topographie | enum | Topographie ? | 38 |
| inondable | Inondable | boolean | Inondable ? | 39 |
| certificat_urbanisme | CU | boolean | Certificat d'urbanisme du lot ? | 40 |
| etape_morcellement | Etape morcellement | enum | A quelle etape du morcellement ? (etude, depot, enquete, approbation, publication) | 41 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo ? | 46 |
| commentaire | Commentaire | string | Precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai souhaite ? | 44 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| litiges_connus | when any | -- | Litiges sur le morcellement ? | 55 |
| servitudes | when lot | num_lot | Servitudes affectant le lot ? | 56 |
| hypotheque_charge | when titre mere | -- | Hypotheque sur le titre mere ? | 57 |
| pv_enquete | when enquete publique | etape_morcellement | PV d'enquete publique disponible ? | 58 |
| titre_mere_num | Titre mere | -- | Numero du titre foncier mere ? | 59 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| geometre_responsable | public | HERITAGE_VALIDATED | HIGH | Verify with ordre des geometres |
| morcellement_approuve | public | HERITAGE_VALIDATED | HIGH | Check with municipal records |
| plan_morcellement | sensitive | HERITAGE_VALIDATED | HIGH | Surveyor document |
| titre_mere_num | confidential | HERITAGE_VALIDATED | HIGH | Notary only |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| avancement_pct | Avancement % | mapped from etape_morcellement | integer |
| delai_estime_finalisation | Delai finalisation estime | derived from etape + approval status | string |
| risque_morcellement | Risque morcellement | weighted(litiges, approbation, geometre) | enum |
| lot_attribuable | Lot attribuable | derived from avancement + plan | boolean |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |

---

## 8. terrain_agricole

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_AGRICOLE_001 |
| authoritative_name | Terrain agricole (Agricultural Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_agricole |

### Description
Terrain destine a l'exploitation agricole. Peut etre situe en zone rurale ou peri-urbaine. La surface est generalement grande (>1 ha). Criteres specifiques: qualite du sol, disponibilite en eau, acces pour engins agricoles.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Dans quelle ville ou zone rurale ? | 10 |
| village_ou_axe | always | Quel village ou axe ? | 20 |
| surface | always | Surface en hectares ou m2 ? | 30 |
| budget_total | always | Budget ? | 40 |
| type_culture | recommended | Quel type de culture ou d'exploitation ? | 50 |
| acces_engins | always | Acces pour engins agricoles ? | 55 |
| point_eau | always | Y a-t-il un point d'eau (source, forage, cours d'eau) ? | 56 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville_ou_zone | always | Ville ou zone rurale ? | 10 |
| surface_min | always | Surface minimale ? | 20 |
| budget_max | always | Budget ? | 30 |
| usage_agricole | always | Usage agricole confirme ? | 40 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville_ou_zone | hard_constraint | MATCH-001 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| budget_total | hard_constraint | MATCH-003 |
| acces_engins | ranking_preference | LAND-MATCH-AGRICOLE |
| point_eau | hard_constraint | LAND-MATCH-AGRICOLE-EAU |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| ville_ou_zone | always | Zone ? | 15 |
| budget_total | always | Budget ? | 20 |
| surface | always | Surface souhaitee ? | 25 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite du terrain agricole ? | 5 |
| disponibilite | when visit | Quand ? | 10 |
| coordonnees_gps | before visit | Coordonnees GPS ? | 15 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire requis. | 5 |
| type_document | always | Quels documents (titre, concession, certificat) ? | 10 |
| litiges_connus | always | Litiges fonciers ? | 15 |
| source_financement | always | Financement ? | 20 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| qualite_sol | Qualite du sol | enum | Quelle est la qualite du sol ? (riche, moyen, pauvre, lateritique) | 35 |
| type_culture | Type de culture | enum | Culture envisagee ? (vivriere, maraichere, plantation, elevage, mixte) | 36 |
| acces_engins | Acces engins | boolean | Acces pour tracteurs/engins ? | 37 |
| point_eau_detail | Point d'eau detail | enum | Type de point d'eau ? (source, forage, puits, cours_eau, aucun) | 38 |
| topographie | Topographie | enum | Topographie ? | 39 |
| inondable | Inondable | boolean | Risque d'inondation ? | 40 |
| distance_route | Distance route | float | Distance de la route ? | 41 |
| titre_agricole | Titre agricole | boolean | Titre foncier ou concession agricole ? | 42 |
| electricite_disponible | Electricite | boolean | Electricite a proximite ? | 43 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo du terrain ? | 46 |
| video_terrain | Video | string | Video ? | 47 |
| cloture | Cloture | boolean | Terrain cloture ? | 48 |
| batiments_agricoles | Batiments | string | Batiments agricoles existants ? | 49 |
| commentaire | Commentaire | string | Precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai ? | 44 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| analyse_sol | when intensive culture | type_culture | Analyse de sol realisee ? | 55 |
| etude_impact | when large surface | surface | Etude d'impact environnemental ? | 56 |
| autorisation_exploitation | when reglemente | -- | Autorisation d'exploitation agricole ? | 57 |
| servitudes_passage | when acces partage | acces_engins | Servitudes de passage ? | 58 |
| succession | when familial | -- | Terrain issu d'une succession ? | 59 |
| indivision | when co-ownership | -- | Indivision entre heritiers ? | 60 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| type_document | sensitive | HERITAGE_VALIDATED | HIGH | Verify |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate |
| superficie | public | HERITAGE_VALIDATED | HIGH | Cross-check with cadastre |
| succession | confidential | HERITAGE_VALIDATED | MEDIUM | Notary |
| indivision | confidential | HERITAGE_VALIDATED | MEDIUM | All owners consent |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| potentiel_agricole | Potentiel agricole | weighted(qualite_sol, point_eau, topographie) | integer |
| rendement_estime | Rendement estime | derived from type_culture + qualite_sol + surface | string |
| prix_hectare | Prix a l'hectare | budget_total / (surface / 10000) | float |
| changement_usage_possible | Changement d'usage possible | derived from zone + reglementation | boolean |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |
| etage | Irrelevant |
| loti | Agricultural land is not loti by definition |

---

## 9. terrain_industriel

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_INDUSTRIEL_001 |
| authoritative_name | Terrain industriel (Industrial Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_industriel |

### Description
Terrain destine a un usage industriel ou logistique. Situe generalement en zone industrielle ou peripherie urbaine. Criteres specifiques: accessibilite poids lourds, puissance electrique, normes environnementales.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| zone_industrielle | always | Zone industrielle specifique ? | 20 |
| surface | always | Surface necessaire ? | 30 |
| budget_total | always | Budget ? | 40 |
| acces_poids_lourds | always | Acces pour poids lourds requis ? | 50 |
| puissance_electrique | always | Puissance electrique necessaire (en kVA) ? | 55 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| zone_industrielle | always | Zone industrielle ? | 20 |
| surface_min | always | Surface ? | 30 |
| budget_max | always | Budget ? | 40 |
| acces_camion | always | Acces camion ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 |
| zone_industrielle | hard_constraint | LAND-MATCH-ZONE-INDUSTRIELLE |
| budget_total | hard_constraint | MATCH-003 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| acces_poids_lourds | hard_constraint | LAND-MATCH-INDUSTRIEL |
| puissance_electrique | soft_constraint | LAND-MATCH-INDUSTRIEL-ELEC |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| ville | always | Ville ? | 15 |
| budget_total | always | Budget ? | 20 |
| surface | always | Surface necessaire ? | 25 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite du site industriel ? | 5 |
| disponibilite | when visit | Quand ? | 10 |
| rencontre_technique | always | Une rencontre technique sur site est recommandee. | 15 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire requis. | 5 |
| type_document | always | Documents de propriete ? | 10 |
| certificat_conformite | always | Certificat de conformite environnementale ? | 15 |
| autorisation_industrielle | always | Autorisation d'exploitation industrielle ? | 20 |
| source_financement | always | Financement ? | 25 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| acces_camion | Acces camion | boolean | Acces camion semi-remorque ? | 35 |
| quai_chargement | Quai chargement | boolean | Quai de chargement necessaire ? | 36 |
| hauteur_sous_plafond | Hauteur sous plafond | float | Hauteur sous plafond requise (m) ? | 37 |
| charge_sol | Charge au sol | float | Charge au sol admissible (tonnes/m2) ? | 38 |
| viabilisation_eau | Eau industrielle | boolean | Alimentation en eau industrielle ? | 39 |
| viabilisation_electricite | Electricite HT | boolean | Electricite haute tension ? | 40 |
| groupe_electrogene | Groupe electrogene | boolean | Groupe electrogene de secours ? | 41 |
| topographie | Topographie | enum | Topographie ? | 42 |
| inondable | Inondable | boolean | Risque inondation ? | 43 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo ? | 46 |
| commentaire | Commentaire | string | Precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai ? | 47 |
| urgence | Urgence | enum | Urgence ? | 48 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| etude_impact | when heavy industry | -- | Etude d'impact environnemental realisee ? | 55 |
| normes_rejet | when pollution possible | -- | Normes de rejet conformes ? | 56 |
| permis_construire | when construction | -- | Permis de construire industriel ? | 57 |
| servitudes | when access shared | acces_poids_lourds | Servitudes de passage ? | 58 |
| litiges_connus | when any | -- | Litiges connus ? | 59 |
| hypotheque_charge | when titre | -- | Hypotheque sur le terrain ? | 60 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| type_document | sensitive | HERITAGE_VALIDATED | HIGH | Verify |
| certificat_conformite | public | HERITAGE_VALIDATED | HIGH | Check with MINEPDED |
| autorisation_industrielle | public | HERITAGE_VALIDATED | HIGH | Verify with ministry |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate |
| hypotheque_charge | confidential | HERITAGE_VALIDATED | HIGH | Conservatoire |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| compatibilite_industrielle | Compatibilite | weighted(puissance, acces, surface, normes) | integer |
| cout_estime_amenagement | Cout amenagement | derived from surface + besoins techniques | float |
| faisabilite_projet | Faisabilite projet | derived from zone, regles d'urbanisme, acces | enum |
| score_logistique | Score logistique | weighted(acces_camion, quai, distance_route) | integer |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |
| nombre_pieces | Residential criteria |
| meuble | Irrelevant |

---

## 10. terrain_commercial

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_COMMERCIAL_001 |
| authoritative_name | Terrain commercial (Commercial Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_commercial |

### Description
Terrain destine a un usage commercial: centre commercial, station-service, showroom, hotel, restaurant. Situe generalement en zone a forte circulation. La visibilite et l'accessibilite client sont primordiales.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ou axe commercial ? | 20 |
| surface | always | Surface ? | 30 |
| budget_total | always | Budget ? | 40 |
| type_commerce | always | Quel type d'activite commerciale ? | 50 |
| visibilite_route | always | Le terrain doit-il etre visible depuis la route ? | 55 |
| accessibilite_clients | always | Accessibilite pour la clientele ? | 56 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier_commercial | always | Quartier commercial ? | 20 |
| surface_min | always | Surface ? | 30 |
| budget_max | always | Budget ? | 40 |
| activite_commerciale | always | Type d'activite ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 |
| quartier_commercial | hard_constraint | LAND-MATCH-QUARTIER-COMMERCIAL |
| budget_total | hard_constraint | MATCH-003 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| type_commerce | hard_constraint | LAND-MATCH-COMMERCE |
| visibilite_route | ranking_preference | LAND-MATCH-VISIBILITE |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| ville | always | Ville ? | 15 |
| budget_total | always | Budget ? | 20 |
| type_commerce | always | Activite commerciale ? | 25 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite du terrain ? | 5 |
| disponibilite | when visit | Quand ? | 10 |
| coordonnees_gps | before visit | Coordonnees GPS ? | 15 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire requis. | 5 |
| type_document | always | Documents disponibles ? | 10 |
| certificat_urbanisme | always | Certificat d'urbanisme pour usage commercial ? | 15 |
| autorisation_commerciale | always | Autorisation d'exploitation commerciale ? | 20 |
| source_financement | always | Financement ? | 25 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| front_route | Front de route | float | Lineaire de facade sur la route (m) ? | 35 |
| parking_clients | Parking clients | boolean | Parking pour clients necessaire ? | 36 |
| viabilisation_eau | Eau | boolean | Eau necessaire pour l'activite ? | 37 |
| viabilisation_electricite | Electricite | boolean | Puissance electrique necessaire ? | 38 |
| topographie | Topographie | enum | Topographie ? | 39 |
| inondable | Inondable | boolean | Inondable ? | 40 |
| zone_commerciale | Zone commerciale | string | Zone commerciale specifique ? | 41 |
| flux_pieton | Flux pieton | enum | Flux pieton ? (eleve, moyen, faible) | 42 |
| concurrence_proximite | Concurrence | string | Concurrence a proximite ? | 43 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo ? | 46 |
| enseigne_visible | Enseigne visible | boolean | Enseigne visible depuis la route ? | 47 |
| commentaire | Commentaire | string | Precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai ? | 44 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| etude_marche | when large project | type_commerce | Etude de marche realisee ? | 55 |
| permis_construire | when construction | -- | Permis de construire commercial ? | 56 |
| normes_accessibilite | when public | -- | Normes d'accessibilite PMR respectees ? | 57 |
| servitudes | when access shared | -- | Servitudes ? | 58 |
| litiges_connus | when any | -- | Litiges ? | 59 |
| hypotheque_charge | when titre | -- | Hypotheque ? | 60 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| type_document | sensitive | HERITAGE_VALIDATED | HIGH | Verify |
| autorisation_commerciale | public | HERITAGE_VALIDATED | HIGH | Check with mairie |
| certificat_urbanisme | public | HERITAGE_VALIDATED | HIGH | Verify |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate |
| hypotheque_charge | confidential | HERITAGE_VALIDATED | HIGH | Conservatoire |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| potentiel_commercial | Potentiel commercial | weighted(flux, visibilite, parking, zone) | integer |
| score_emplacement | Score emplacement | weighted(visibilite, accessibilite, concurrence) | integer |
| faisabilite_commerciale | Faisabilite commerciale | derived from zone + autorisations + type | enum |
| estimation_chiffre_affaires | Estimation CA | derived from zone + flux + surface | string |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |
| meuble | Irrelevant |
| chambres_a_coucher | Residential criteria |

---

## 11. terrain_residentiel

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_TERRAIN_RESIDENTIEL_001 |
| authoritative_name | Terrain residentiel (Residential Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | terrain_residentiel |

### Description
Terrain destine a la construction d'une habitation (maison, villa, immeuble residentiel). Situe en zone residentielle ou a usage d'habitation autorise. Criteres: constructibilite, viabilisation, environnement residentiel, proximite commodites.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier residentiel ? | 20 |
| surface | always | Surface ? | 30 |
| budget_total | always | Budget ? | 40 |
| usage_residentiel | always | Construction d'habitation ? | 50 |
| terrain_constructible | always | Le terrain est-il constructible ? | 55 |
| viabilisation_eau | always | Eau disponible sur le terrain ? | 56 |
| viabilisation_electricite | always | Electricite disponible ? | 57 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ? | 20 |
| surface_min | always | Surface ? | 30 |
| budget_max | always | Budget ? | 40 |
| constructible | always | Constructible obligatoire ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 |
| quartier | hard_constraint | MATCH-001 |
| budget_total | hard_constraint | MATCH-003 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| terrain_constructible | hard_constraint | LAND-MATCH-CONSTRUCTIBLE |
| usage_residentiel | hard_constraint | PROP-001 |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| ville | always | Ville ? | 15 |
| budget_total | always | Budget ? | 20 |
| surface | always | Surface souhaitee ? | 25 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Souhaitez-vous visiter ? | 5 |
| disponibilite | when visit | Quand ? | 10 |
| coordonnees_gps | before visit | Coordonnees GPS ? | 15 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire requis. | 5 |
| type_document | always | Documents ? | 10 |
| certificat_urbanisme | always | Certificat d'urbanisme ? | 15 |
| source_financement | always | Financement ? | 20 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| accessibilite | Accessibilite | enum | Acces au terrain ? | 35 |
| distance_route | Distance route | float | Distance route principale ? | 36 |
| topographie | Topographie | enum | Topographie ? | 37 |
| inondable | Inondable | boolean | Inondable ? | 38 |
| qualite_acces | Qualite acces | enum | Qualite de l'acces ? | 39 |
| orientation | Orientation | enum | Exposition/orientation du terrain ? | 40 |
| proximite_ecoles | Proximite ecoles | boolean | A proximite d'ecoles ? | 41 |
| proximite_commerces | Proximite commerces | boolean | A proximite des commerces ? | 42 |
| proximite_transport | Proximite transport | boolean | Transport a proximite ? | 43 |
| securite_quartier | Securite quartier | enum | Securite du quartier ? | 44 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo ? | 46 |
| video_terrain | Video | string | Video ? | 47 |
| cloture | Cloture | boolean | Terrain cloture ? | 48 |
| commentaire | Commentaire | string | Precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai souhaite ? | 49 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| permis_construire | when constructible | terrain_constructible | Permis de construire necessaire ? | 55 |
| certificat_urbanisme | when constructible | usage_residentiel | Certificat d'urbanisme obtenu ? | 56 |
| servitudes | when access shared | accessibilite | Servitudes ? | 57 |
| litiges_connus | when any | -- | Litiges ? | 58 |
| hypotheque_charge | when titre | -- | Hypotheque ? | 59 |
| succession | when inherited | -- | Succession ? | 60 |
| indivision | when co-ownership | -- | Indivision ? | 61 |
| groupe_electrogene | when zone instable | -- | Groupe electrogene prevu ? | 62 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| type_document | sensitive | HERITAGE_VALIDATED | HIGH | Verify |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate |
| hypotheque_charge | confidential | HERITAGE_VALIDATED | HIGH | Conservatoire |
| succession | confidential | HERITAGE_VALIDATED | MEDIUM | Notary |
| indivision | confidential | HERITAGE_VALIDATED | MEDIUM | All owners |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| constructibilite_reelle | Constructibilite reelle | derived from CU + POS + zone | boolean |
| potentiel_residentiel | Potentiel residentiel | weighted(proximites, securite, accessibilite) | integer |
| prix_m2_residentiel | Prix m2 residentiel | budget_total / surface | float |
| score_environnement | Score environnement | weighted(proximites, transport, securite) | integer |
| surface_constructible | Surface constructible | surface * COS (coefficient d'occupation des sols) | float |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant -- land is not yet built |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced from price + location |
| meuble | Irrelevant for land |
| etage | Construction decision not yet made |

---

## 12. parcelle

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_PARCELLE_001 |
| authoritative_name | Parcelle (Plot/Parcel) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | parcelle |

### Description
Parcelle individuelle issue d'un lotissement ou d'un morcellement. Surface generalement entre 150 m2 et 1000 m2. Unite de base pour la construction individuelle. Tres recherchee au Cameroun.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ? | 20 |
| surface | always | Surface de la parcelle ? | 30 |
| budget_total | always | Budget ? | 40 |
| usage_prevu | always | Usage prevu ? | 50 |
| numero_lot | recommended | Numero de lot si connu ? | 55 |
| lotissement_approuve | always | Le lotissement est-il approuve ? | 56 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville | always | Ville ? | 10 |
| quartier | always | Quartier ? | 20 |
| surface_min | always | Surface minimale ? | 30 |
| surface_max | recommended | Surface maximale ? | 35 |
| budget_max | always | Budget maximum ? | 40 |
| loti | always | Parcelle lotie ou non ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville | hard_constraint | MATCH-001 |
| quartier | hard_constraint | MATCH-001 |
| budget_total | hard_constraint | MATCH-003 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| terrain_loti | soft_constraint | LAND-MATCH-LOTI |
| usage_prevu | hard_constraint | PROP-001 |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| ville | always | Ville ? | 15 |
| budget_total | always | Budget ? | 20 |
| surface | always | Surface recherchee ? | 25 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite de la parcelle ? | 5 |
| disponibilite | when visit | Quand ? | 10 |
| coordonnees_gps | before visit | Coordonnees GPS ? | 15 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire requis. | 5 |
| type_document | always | Quels documents accompagnent la parcelle ? | 10 |
| num_titre | when available | Numero de titre si individuel ? | 15 |
| source_financement | always | Financement ? | 20 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| accessibilite | Accessibilite | enum | Acces a la parcelle ? | 35 |
| distance_route | Distance route | float | Distance route principale ? | 36 |
| viabilisation_eau | Eau | boolean | Raccordement eau ? | 37 |
| viabilisation_electricite | Electricite | boolean | Raccordement electricite ? | 38 |
| topographie | Topographie | enum | Topographie ? | 39 |
| inondable | Inondable | boolean | Inondable ? | 40 |
| terrain_constructible | Constructible | boolean | Constructible ? | 41 |
| orientation_parcelle | Orientation | enum | Orientation de la parcelle ? | 42 |
| mitoyennete | Mitoyennete | boolean | Mitoyenne ? | 43 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo ? | 46 |
| cloture | Cloture | boolean | Cloturee ? | 47 |
| forme | Forme parcelle | enum | Forme ? (rectangulaire, carree, irreguliere) | 48 |
| commentaire | Commentaire | string | Precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai ? | 44 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| bornage | when limits unclear | -- | Bornage de la parcelle effectue ? | 55 |
| pv_bornage | when bornage done | bornage | PV de bornage disponible ? | 56 |
| servitudes | when acces partage | accessibilite | Servitudes sur la parcelle ? | 57 |
| litiges_connus | when any | -- | Litiges sur cette parcelle ? | 58 |
| hypotheque_charge | when titre | -- | Hypotheque ? | 59 |
| certificat_urbanisme | when constructible | usage_prevu | Certificat d'urbanisme ? | 60 |
| succession | when inherited | -- | Succession ? | 61 |
| indivision | when co-ownership | -- | Indivision ? | 62 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| num_titre | confidential | HERITAGE_VALIDATED | HIGH | Notary only |
| type_document | sensitive | HERITAGE_VALIDATED | HIGH | Verify |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate |
| hypotheque_charge | confidential | HERITAGE_VALIDATED | HIGH | Conservatoire |
| succession | confidential | HERITAGE_VALIDATED | MEDIUM | Notary |
| indivision | confidential | HERITAGE_VALIDATED | MEDIUM | All owners |
| bornage | sensitive | HERITAGE_VALIDATED | MEDIUM | Surveyor |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| prix_m2_parcelle | Prix m2 parcelle | budget_total / surface | float |
| coefficient_occupation | COS estime | derived from zone + POS rules | float |
| surface_constructible | Surface constructible | surface * COS | float |
| potentiel_construction | Potentiel construction | weighted(surface, constructibilite, viabilisation) | integer |
| score_parcelle | Score parcelle | weighted(proximites, accessibilite, titre) | integer |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant for parcel |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |
| meuble | Irrelevant |

---

## 13. domaine_rural

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_DOMAINE_RURAL_001 |
| authoritative_name | Domaine rural (Rural Domain) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | domaine_rural |

### Description
Terrain relevant du domaine rural camerounais, regi par le droit coutumier et la loi fonciere. Les transactions sont regulees par la commission consultative departementale. Usage principal: agricole, forestier, pastoral, ou residentiel rural.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| region | always | Dans quelle region ? | 10 |
| departement | always | Quel departement ? | 15 |
| arrondissement | always | Quel arrondissement ? | 20 |
| village | always | Quel village ou communaute rurale ? | 25 |
| surface | always | Surface en hectares ? | 30 |
| budget_total | always | Budget ? | 40 |
| usage_rural | always | Usage prevu (agricole, forestier, pastoral, residentiel rural) ? | 50 |
| autorisation_cession | always | Autorisation de cession obtenue ? | 55 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| region | always | Region ? | 10 |
| village_ou_zone | always | Village ou zone ? | 20 |
| surface_min | always | Surface minimale (ha) ? | 30 |
| budget_max | always | Budget ? | 40 |
| usage_rural | always | Usage rural ? | 50 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| region | hard_constraint | MATCH-001 (geo-level) |
| departement | hard_constraint | MATCH-001 |
| arrondissement | hard_constraint | MATCH-001 |
| budget_total | hard_constraint | MATCH-003 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| usage_rural | hard_constraint | PROP-001 |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| village_ou_zone | always | Quel village ou zone rurale ? | 15 |
| budget_total | always | Budget ? | 20 |
| surface | always | Surface souhaitee ? | 25 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite du domaine rural ? | 5 |
| disponibilite | when visit | Quand ? | 10 |
| accompagnement_chef_communaute | recommended | Accompagnement du chef de communaute recommande. | 15 |
| coordonnees_gps | before visit | Coordonnees GPS approximatives ? | 20 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire requis pour immatriculation. | 5 |
| autorisation_cession | always | Autorisation de la commission consultative ? | 10 |
| certificat_administratif | always | Certificat administratif du domaine ? | 15 |
| accord_communautaire | always | Accord de la communaute rurale ? | 20 |
| enquete_commissaire | always | Enquete du commissaire enqueteur effectuee ? | 25 |
| source_financement | always | Financement ? | 30 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| acces_routier | Acces routier | boolean | Acces par route carrossable ? | 35 |
| distance_ville | Distance ville | float | Distance de la ville la plus proche ? | 36 |
| point_eau | Point d'eau | enum | Point d'eau naturel ? | 37 |
| electricite_proximite | Electricite proche | boolean | Reseau electrique a proximite ? | 38 |
| topographie | Topographie | enum | Topographie ? | 39 |
| type_sol | Type de sol | enum | Type de sol ? | 40 |
| vegetation | Vegetation | enum | Type de vegetation ? | 41 |
| occupation_actuelle | Occupation | enum | Occupation actuelle ? | 42 |
| titre_immatriculation | Immatriculation | boolean | Immatriculation au titre foncier en cours ? | 43 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo du domaine ? | 46 |
| video_terrain | Video | string | Video ? | 47 |
| cloture | Cloture | boolean | Domaine cloture ? | 48 |
| batiments_existants | Batiments | string | Batiments existants ? | 49 |
| commentaire | Commentaire | string | Precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai ? | 44 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| enquete_publique | when cession | autorisation_cession | Enquete publique realisee ? | 55 |
| avis_commission | when cession | -- | Avis de la commission consultative ? | 56 |
| litiges_coutumiers | when communautaire | -- | Litiges coutumiers connus ? | 57 |
| servitudes_rurales | when usage partage | -- | Servitudes rurales (pacage, passage) ? | 58 |
| succession_coutumiere | when familial | -- | Succession coutumiere ? | 59 |
| indivision_familiale | when co-ownership | -- | Indivision familiale traditionnelle ? | 60 |
| procedure_immatriculation | when titre souhaite | -- | Procedure d'immatriculation initiee ? | 61 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| autorisation_cession | sensitive | HERITAGE_VALIDATED | HIGH | Verify with service des domaines |
| certificat_administratif | sensitive | HERITAGE_VALIDATED | HIGH | Verify |
| accord_communautaire | sensitive | HERITAGE_VALIDATED | HIGH | Documented consent required |
| litiges_coutumiers | confidential | HERITAGE_VALIDATED | HIGH | Escalate to DOA |
| succession_coutumiere | sensitive | HERITAGE_VALIDATED | MEDIUM | Traditional leader confirmation |
| indivision_familiale | sensitive | HERITAGE_VALIDATED | MEDIUM | All family consent |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| statut_domanial | Statut domanial | derived from autorisation + enquete + certificat | enum |
| risque_coutumier | Risque coutumier | weighted(litiges_coutumiers, succession, indivision) | enum |
| potentiel_immatriculation | Potentiel d'immatriculation | derived from documents + procedure | boolean |
| delai_estime_cession | Delai cession estime | derived from etape administrative + enquete | string |
| prix_hectare_rural | Prix/ha rural | budget_total / (surface / 10000) | float |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |
| loti | Domaine rural not loti |
| titre_foncier | May not exist in rural domain |
| quartier | Rural domain uses village |

---

## 14. concession

### Matrix Header
| Field | Value |
|-------|-------|
| matrix_id | LAND_SEARCH_CONCESSION_001 |
| authoritative_name | Concession (Concession Land) |
| request_family | LAND_SEARCH |
| transaction_type | BUY |
| property_or_service_type | concession |

### Description
Concession fonciere au Cameroun: droit d'occupation temporaire ou permanent accorde par l'Etat sur le domaine national ou prive de l'Etat. Peut etre agricole, forestiere, miniere, ou d'habitation. Regie par un cahier des charges.

### minimum_intake_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| ville_ou_zone | always | Ville ou zone de la concession ? | 10 |
| localisation | always | Localisation precise ? | 20 |
| surface | always | Surface de la concession ? | 30 |
| budget_total | always | Budget ? | 40 |
| type_concession | always | Type de concession ? (agricole, forestiere, miniere, d'habitation, d'exploitation) | 50 |
| numero_concession | always | Numero de la concession ? | 55 |
| autorite_attribution | always | Quelle autorite a attribue la concession ? | 56 |
| cahier_charges | always | Le cahier des charges est-il accessible ? | 57 |

### minimum_search_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| zone_concession | always | Zone de la concession ? | 10 |
| surface_min | always | Surface ? | 20 |
| budget_max | always | Budget ? | 30 |
| type_concession | always | Type de concession ? | 40 |

### minimum_matching_fields
| field_id | matching_role | matching_weight_reference |
|----------|---------------|---------------------------|
| ville_ou_zone | hard_constraint | MATCH-001 |
| surface | soft_constraint | LAND-MATCH-SURFACE |
| budget_total | hard_constraint | MATCH-003 |
| type_concession | hard_constraint | LAND-MATCH-CONCESSION |
| duree_concession | verification_only | LAND-MATCH-CONCESSION-DUREE |

### minimum_introduction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| contact_nom | always | Nom ? | 5 |
| contact_telephone | always | Telephone ? | 10 |
| zone_concession | always | Zone de la concession ? | 15 |
| budget_total | always | Budget ? | 20 |
| type_concession | always | Type de concession ? | 25 |

### minimum_visit_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| visite_souhaitee | always | Visite du site de la concession ? | 5 |
| disponibilite | when visit | Quand ? | 10 |
| coordonnees_gps | before visit | Coordonnees GPS ? | 15 |
| rdv_service_domaines | recommended | Rendez-vous au service des domaines recommande. | 20 |

### minimum_transaction_fields
| field_id | mandatory_when | question_template (FR) | question_priority |
|----------|----------------|------------------------|:-----------------:|
| besoin_notaire | always | Notaire requis pour le transfert. | 5 |
| numero_concession | always | Numero officiel de la concession. | 10 |
| autorite_attribution | always | Autorite d'attribution ? | 15 |
| cahier_charges | always | Cahier des charges a respecter ? | 20 |
| duree_concession | always | Duree restante de la concession ? | 25 |
| redevance_annuelle | always | Montant de la redevance annuelle ? | 30 |
| source_financement | always | Financement ? | 35 |

### recommended_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| accessibilite | Accessibilite | enum | Acces a la concession ? | 36 |
| distance_route | Distance route | float | Distance route principale ? | 37 |
| viabilisation_eau | Eau | boolean | Eau sur la concession ? | 38 |
| viabilisation_electricite | Electricite | boolean | Electricite ? | 39 |
| topographie | Topographie | enum | Topographie ? | 40 |
| inondable | Inondable | boolean | Inondable ? | 41 |
| occupation_actuelle | Occupation | enum | Occupation actuelle ? | 42 |
| potentiel_transformation | Transformation en titre | boolean | Possibilite de transformation en titre foncier ? | 43 |
| delai_concession | Duree | string | Duree initiale et date d'echeance ? | 44 |

### optional_fields
| field_id | label | data_type | question_template (FR) | question_priority |
|----------|-------|-----------|------------------------|:-----------------:|
| repere | Repere | string | Point de repere ? | 45 |
| photo_terrain | Photo | string | Photo ? | 46 |
| photo_concession | Document concession | string | Copie de l'acte de concession ? | 47 |
| commentaire | Commentaire | string | Precisions ? | 50 |
| delai_souhaite | Delai | enum | Delai souhaite ? | 48 |

### conditional_fields
| field_id | condition | field_id_trigger | conditional_question (FR) | question_priority |
|----------|-----------|------------------|---------------------------|:-----------------:|
| renouvellement | when near expiry | duree_concession | Possibilite de renouvellement ? | 55 |
| conditions_exploitation | when exploitation | type_concession | Conditions d'exploitation respectees ? | 56 |
| litiges_connus | when any | -- | Litiges sur la concession ? | 57 |
| servitudes_etat | when domanial | -- | Servitudes d'utilite publique ? | 58 |
| procedure_immatriculation | when titre souhaite | -- | Procedure d'immatriculation en cours ? | 59 |
| oppositions | when any contestation | -- | Oppositions connues ? | 60 |
| redevances_impayees | when financial | redevance_annuelle | Redevances impayees ? | 61 |

### sensitive_fields
| field_id | privacy_level | source | confidence | handling |
|----------|---------------|--------|:----------:|----------|
| numero_concession | confidential | HERITAGE_VALIDATED | HIGH | Verify with domain services |
| autorite_attribution | public | HERITAGE_VALIDATED | HIGH | Cross-check |
| cahier_charges | sensitive | HERITAGE_VALIDATED | HIGH | Legal review |
| duree_concession | sensitive | HERITAGE_VALIDATED | HIGH | Verify expiry |
| redevance_annuelle | sensitive | HERITAGE_VALIDATED | MEDIUM | Verify amount |
| litiges_connus | confidential | HERITAGE_VALIDATED | HIGH | Escalate |
| procedure_immatriculation | sensitive | HERITAGE_VALIDATED | MEDIUM | Track progress |

### derived_fields
| field_id | label | derivation_rule | data_type |
|----------|-------|-----------------|-----------|
| statut_concession | Statut concession | derived from duree + redevances + litiges | enum |
| potentiel_titre | Potentiel transformation | derived from type + procedure + autorite | boolean |
| viabilite_concession | Viabilite concession | weighted(duree, redevances, conditions) | integer |
| cout_annuel_total | Cout annuel total | redevance_annuelle + autres_charges | float |
| risque_resiliation | Risque resiliation | weighted(litiges, redevances, conditions) | enum |

### forbidden_questions
| Forbidden Field | Reason |
|-----------------|--------|
| chambres | Irrelevant |
| douches | Irrelevant |
| salon | Irrelevant |
| pieces | Irrelevant |
| standing | Deduced |
| loti | Concession concept different |
| titre_foncier | Concession != titre foncier |

---

## COMMON FIELD REFERENCES

### Field Definitions Reference
| field_id | label | data_type | allowed_values | validation_rules | normalization_rules | ambiguity_rules |
|----------|-------|-----------|----------------|------------------|---------------------|-----------------|
| ville | Ville | string | Yaounde, Douala, Bafoussam, Bamenda, Buea, Limbe, Kribi, Nkongsamba, Garoua, Maroua + others | Must be a known Cameroonian city | Mapping: Yde->Yaounde, Dla->Douala, Bfs->Bafoussam | If ambiguous, ask for confirmation |
| quartier | Quartier | string | Per city neighborhood list | Must match known quartiers for the city | Normalize accents and common variations | If multiple matches, propose top 3 |
| surface | Surface | float | >= 1 m2 | Positive number; m2 default | Convert ha->m2 (1 ha = 10000 m2), convert acres->m2 | If unit unclear, ask m2 or ha |
| budget_total | Budget total | float | >= 1000 FCFA | Positive number in FCFA | Convert EUR->FCFA (1 EUR ~= 655.957 FCFA), USD->FCFA | If currency unclear, confirm XAF |
| usage_prevu | Usage prevu | enum | habitation, commerce, industrie, agriculture, mixte | Must be one of allowed values | Map: residentiel->habitation, business->commerce | If multiple, ask for primary |
| type_document | Type de document | enum | certificat_propriete, plan_bornage, lotissement, acte_notarie, promesse_vente, concession, certificat_occupation, non_documente | Must be one of allowed values | Map: paper->document | If unknown, ask to describe |
| accessibilite | Accessibilite | enum | route_goudronnee, route_terre, sentier, enclave | Must be one of allowed values | Map: goudron->route_goudronnee, laterite->route_terre | If unclear, ask for photos |
| topographie | Topographie | enum | plat, legere_pente, forte_pente, vallee, colline | Must be one of allowed values | Map: pent->pente, descend->vallee | If uncertain, request photo |
| inondable | Zone inondable | boolean | true, false | Must be boolean | Map: oui->true, non->false, parfois->true | If uncertain, check historical data |
| viabilisation_eau | Eau disponible | boolean | true, false | Must be boolean | Map: oui->true, non->false | If possible/impossible, ask for confirmation |
| viabilisation_electricite | Electricite disponible | boolean | true, false | Must be boolean | Map: oui->true, non->false | If possible/impossible, ask for confirmation |
| occupation_actuelle | Occupation actuelle | enum | libre, cultive, bati, en_friche | Must be one of allowed values | N/A | If multiple, ask for primary |
| disponibilite | Disponibilite | enum | immediate, 1_mois, 3_mois, 6_mois, a_definir | Must be one of allowed values | Map: tout_de_suite->immediate | If vague, propose options |
| delai_souhaite | Delai souhaite | enum | urgent, 1_mois, 3_mois, 6_mois, pas_de_delai | Must be one of allowed values | Map: ASAP->urgent, soon->1_mois | If vague, ask for precision |
| source_financement | Source de financement | enum | comptant, credit_bancaire, tontine, diaspora, pret_familial | Must be one of allowed values | Map: cash->comptant, bank->credit_bancaire | If multiple, ask for primary |
| servitudes | Servitudes | string | Free text | No specific validation | N/A | If yes, request document |
| litiges_connus | Litiges connus | boolean | true, false | Must be boolean | Map: oui->true, non->false | If true, escalate immediately |
| hypotheque_charge | Hypotheque / charge | boolean | true, false | Must be boolean | Map: oui->true, non->false | If true, request details |
| succession | Succession | boolean | true, false | Must be boolean | Map: oui->true, non->false | If true, request notary |
| indivision | Indivision | boolean | true, false | Must be boolean | Map: oui->true, non->false | If true, list all co-owners |
| procuration | Procuration | boolean | true, false | Must be boolean | Map: oui->true, non->false | Verify notarial validity |
| bornage | Bornage effectue | boolean | true, false | Must be boolean | Map: oui->true, non->false | If true, request PV |
| pv_bornage | PV de bornage | boolean | true, false | Must be boolean | Map: oui->true, non->false | Verify with surveyor |
| certificat_urbanisme | Certificat d'urbanisme | boolean | true, false | Must be boolean | Map: oui->true, non->false | If true, verify validity period |

### Privacy Levels
| Level | Description | Access |
|-------|-------------|--------|
| public | Visible to all users and agents | Unrestricted |
| private | Visible only to the requesting user | User-only |
| sensitive | Visible only with explicit consent | Consent-gated |
| confidential | Visible only to authorized professionals (notary, lawyer) | Professional-only |

### Source Types
| Source | Description | Reliability Weight |
|--------|-------------|:-----------------:|
| HERITAGE_VALIDATED | Extracted from validated LAWIM heritage documents | 90-100% |
| HERITAGE_NORMALIZED | Normalized from heritage sources | 75-90% |
| EXTERNAL_CONFIRMED | Confirmed by external authoritative source (law, regulation) | 85-100% |
| EXPERT_PROPOSAL | Proposed by domain expert, pending validation | 50-75% |
| HUMAN_VALIDATION_REQUIRED | Requires human expert validation | < 50% |

### Confidence Levels
| Level | Description | Usage |
|-------|-------------|-------|
| HIGH | Strong evidence from validated sources | Use directly in qualification |
| MEDIUM | Some evidence but gaps exist | Use with caution, flag for review |
| LOW | Weak or indirect evidence | Review before use |

### Matching Roles
| Role | Description | Example |
|------|-------------|---------|
| hard_constraint | Property MUST match this field | city, budget, usage |
| soft_constraint | Property SHOULD match, but flexibility exists | surface, loti |
| ranking_preference | Used for ranking, not filtering | accessibilite |
| exclusion | If this field mismatches, exclude property | status=archived |
| boost | Add bonus score if field matches | titre_foncier |
| penalty | Reduce score if field mismatches | missing documents |
| informational_only | Stored for reference, not used in matching | commentaire |
| verification_only | Used only for verification after match | num_titre |
| transaction_blocker | Required before transaction can proceed | notaire, signataires |

---

## MATRIX VALIDATION SUMMARY

| # | Property Type | Matrix ID | Mandatory | Recommended | Optional | Conditional | Sensitive | Derived |
|---|---------------|-----------|:---------:|:-----------:|:--------:|:-----------:|:---------:|:-------:|
| 1 | terrain_titre | LAND_SEARCH_TERRAIN_TITRE_001 | 10 | 8 | 7 | 6 | 8 | 6 |
| 2 | terrain_non_titre | LAND_SEARCH_TERRAIN_NON_TITRE_001 | 10 | 9 | 6 | 7 | 8 | 6 |
| 3 | terrain_loti | LAND_SEARCH_TERRAIN_LOTI_001 | 9 | 7 | 5 | 4 | 4 | 3 |
| 4 | terrain_non_loti | LAND_SEARCH_TERRAIN_NON_LOTI_001 | 9 | 8 | 5 | 6 | 5 | 4 |
| 5 | terrain_titre_collectif | LAND_SEARCH_TERRAIN_TITRE_COLLECTIF_001 | 10 | 8 | 5 | 5 | 9 | 4 |
| 6 | terrain_titre_individuel | LAND_SEARCH_TERRAIN_TITRE_INDIVIDUEL_001 | 9 | 8 | 5 | 6 | 6 | 5 |
| 7 | terrain_sous_morcellement | LAND_SEARCH_TERRAIN_SOUS_MORCELLEMENT_001 | 9 | 8 | 5 | 6 | 5 | 4 |
| 8 | terrain_agricole | LAND_SEARCH_TERRAIN_AGRICOLE_001 | 9 | 9 | 7 | 6 | 5 | 4 |
| 9 | terrain_industriel | LAND_SEARCH_TERRAIN_INDUSTRIEL_001 | 9 | 9 | 5 | 6 | 5 | 4 |
| 10 | terrain_commercial | LAND_SEARCH_TERRAIN_COMMERCIAL_001 | 9 | 9 | 6 | 6 | 5 | 4 |
| 11 | terrain_residentiel | LAND_SEARCH_TERRAIN_RESIDENTIEL_001 | 9 | 10 | 6 | 8 | 5 | 5 |
| 12 | parcelle | LAND_SEARCH_PARCELLE_001 | 9 | 9 | 6 | 8 | 7 | 5 |
| 13 | domaine_rural | LAND_SEARCH_DOMAINE_RURAL_001 | 10 | 10 | 7 | 7 | 6 | 5 |
| 14 | concession | LAND_SEARCH_CONCESSION_001 | 10 | 9 | 5 | 7 | 6 | 5 |

---

## APPENDIX A: LAND MATCHING SCORE ALGORITHM

The land matching score uses the following weighted formula:

```
LAND_MATCH_SCORE =
  (GEOGRAPHIC_SCORE x 0.30) +
  (BUDGET_SCORE x 0.25) +
  (PROPERTY_TYPE_SCORE x 0.15) +
  (TITLE_SCORE x 0.10) +
  (ACCESS_SCORE x 0.10) +
  (VIABILITY_SCORE x 0.10)
```

### Geographic Score (30%)
| Condition | Score |
|-----------|:-----:|
| Exact city + exact neighborhood | 100 |
| Exact city + accepted alternative | 80 |
| Exact city + neighboring district | 60 |
| Same city only | 40 |
| Different city | 0 (excluded) |

### Budget Score (25%)
| Condition | Score |
|-----------|:-----:|
| Within +/-5% of budget | 100 |
| Within +/-10% of budget | 80 |
| Within +/-15% of budget (buy) | 60 |
| Within +/-20% of budget | 40 |
| Within +/-25% of budget (invest) | 20 |
| Outside tolerance | 0 (excluded) |

### Property Type Score (15%)
| Condition | Score |
|-----------|:-----:|
| Exact land type match | 100 |
| Compatible family (e.g., terrain_loti <-> parcelle) | 70 |
| Different family | 0 |

### Title Score (10%)
| Condition | Score |
|-----------|:-----:|
| Has titre_foncier and user requires it | 100 |
| Has titre_foncier, user flexible | 80 |
| No titre, user flexible | 50 |
| No titre, user requires it | 0 (excluded) |

### Access Score (10%)
| Condition | Score |
|-----------|:-----:|
| Route goudronnee, < 100m | 100 |
| Route goudronnee, 100-500m | 80 |
| Route terre, < 100m | 60 |
| Route terre, 100-500m | 40 |
| Sentier or > 500m | 20 |
| Enclave | 0 |

### Viability Score (10%)
| Condition | Score |
|-----------|:-----:|
| Eau + Electricite + Groupe electrogene | 100 |
| Eau + Electricite | 80 |
| Eau only | 50 |
| Electricite only | 40 |
| No utilities | 10 |

---

## APPENDIX B: QUESTION PRIORITY ORDER (1-100)

| Priority Range | Qualification Stage | Description |
|:--------------:|:-------------------:|-------------|
| 1-4 | Channel setup | Collect channel preference and contact basics |
| 5-20 | Introduction | Collect identity, location, intent, budget overview |
| 21-34 | Core qualification | Collect surface, usage, title/status requirements |
| 35-44 | Feature discovery | Collect access, utilities, topography, timing |
| 45-50 | Optional enrichment | Collect media, comments, references |
| 51-54 | Verification | Begin verification of declared information |
| 55-62 | Legal/conditional | Collect legal status, servitudes, disputes, co-ownership |
| 63-80 | Transaction preparation | Collect documents, notary, financing, signatures |
| 81-100 | Finalization | Escalation, human handoff, transaction closure |

---

## APPENDIX C: ESCALATION RULES FOR LAND TRANSACTIONS

### Mandatory Escalation Triggers (Notary Required)
| Condition | Description |
|-----------|-------------|
| Titre foncier transfer | Any transaction involving registered land title |
| Succession sale | Sale of inherited land |
| Indivision dissolution | Breaking co-ownership |
| Domaine rural cession | Any rural domain concession transfer |
| Concession transfer | Transfer of state concession |
| Purchase > 50M FCFA | Any land purchase above 50 million FCFA |

### Mandatory Escalation Triggers (Human Advisor Required)
| Condition | Description |
|-----------|-------------|
| Litiges declared | Any known dispute declared |
| Multiple signatories > 5 | More than 5 co-owners |
| Procuration without notary | Power of attorney without notarial certification |
| Hypotheque declared | Any existing mortgage |
| Price inconsistency | Budget vs surface price inconsistent for zone |
| User requests human | User explicitly asks for human assistance |

---

## APPENDIX D: KEY SOIL/TERRAIN RULES FROM HERITAGE

| ID | Rule | Source |
|----|------|--------|
| H-LAND-001 | Never ask for chambres, douches, salon, pieces, standing for any land type | QUALIFICATION_MODEL.md |
| H-LAND-002 | Always distinguish titre/non-titre in conversations | PROPERTY_MODEL.md |
| H-LAND-003 | For titled land: ask num_titre, nombre_signataires, identite_signataires, disponibilite_signataires | property-qualification-reference.md |
| H-LAND-004 | For non-titled land: ask type_document, certificat_propriete, plan_bornage, lotissement | property-qualification-reference.md |
| H-LAND-005 | Surface is critical: ask in m2 | MATCHING_MODEL.md |
| H-LAND-006 | Access: road distance + access quality | MATCHING_MODEL.md |
| H-LAND-007 | Usage prevu: habitation, commerce, industrie, agriculture | QUALIFICATION_HERITAGE_EXTRACTION.md |
| H-LAND-008 | Budget: global price OR price per m2 | minimum-fields-request.md |
| H-LAND-009 | Location: ville, quartier, axe, village, repere | PROPERTY_MODEL.md |
| H-LAND-010 | Viabilisation: eau, electricite, groupe electrogene | QUALIFICATION_HERITAGE_EXTRACTION.md |
| H-LAND-011 | Topographie: pente, plat, vallee, inondable | minimum-fields-request.md |
| H-LAND-012 | Occupation actuelle: libre, cultive, bati | conversation-qualification-questions.md |
| H-LAND-013 | Never conclude legal validity from user declarations alone | RULE_INDEX.md |
| H-LAND-014 | verification_required = true, professional_review = notaire or geometre | RULE_INDEX.md |

---

*Document patrimonial Gold — Qualification matrices for all 14 land property types in the LAWIM Cameroon market.*
*Total: 14 property types, each with 12 field categories, comprehensive French question bank, matching rules, and validation framework.*
